/**
 * test-pdf-gateway.mjs
 *
 * Verifies the Telegram URL parser, the PDF metadata module, the Range
 * parser, the mock-mode client/resolver, streaming, and the public-vs-server
 * metadata projection.
 *
 * Run:  node tools/test-pdf-gateway.mjs
 *
 * These tests are offline and use the local mock Telegram fixture; they
 * do NOT contact Telegram.
 */

import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { parseTelegramUrl } from "../server/telegram/url-parser.js";
import { EkGuruTelegramClient } from "../server/telegram/client.js";
import { resolveTelegramPdf } from "../server/telegram/resolver.js";
import { streamPdf, parseRange, sanitizeFilename } from "../server/pdf/stream.js";
import { normalizeSheetRow, toPublic, derivePublicId } from "../server/pdf/metadata.js";

let passed = 0;
let failed = 0;
function test(name, fn) {
  try {
    fn();
    console.log(`  ok  - ${name}`);
    passed++;
  } catch (e) {
    console.log(`  FAIL - ${name}: ${e.message}`);
    failed++;
  }
}

console.log("[telegram/url-parser]");

test("parses public username link t.me/<user>/<mid>", () => {
  const r = parseTelegramUrl("https://t.me/EkGuru/42");
  assert.equal(r.kind, "public_username");
  assert.equal(r.peer, "EkGuru");
  assert.equal(r.messageId, 42);
});

test("parses private /c/<id>/<mid> link", () => {
  const r = parseTelegramUrl("https://t.me/c/4430299776/2/80");
  assert.equal(r.kind, "private_id");
  assert.equal(typeof r.peer, "number");
  assert.equal(r.messageId, 2);
  assert.equal(r.topicId, 80);
});

test("rejects non-telegram host", () => {
  assert.throws(() => parseTelegramUrl("https://example.com/foo/1"));
});

test("rejects url without message id", () => {
  assert.throws(() => parseTelegramUrl("https://t.me/EkGuru"));
});

console.log("\n[pdf/metadata]");
test("normalizeSheetRow extracts required fields and hides telegram url from public view", () => {
  const row = {
    course_id: "reasoning",
    title: "Calendar Questions",
    category: "reasoning",
    telegram_pdf_url: "https://t.me/c/4430299776/2/80",
    published: "true",
    sort_order: "3",
    description: "Test PDF",
  };
  const m = normalizeSheetRow(row);
  assert.ok(m);
  assert.equal(m.courseId, "reasoning");
  assert.equal(m.telegramReference, "https://t.me/c/4430299776/2/80");
  const pub = toPublic(m);
  assert.equal(pub.telegramReference, undefined);
  assert.equal(pub.telegram_pdf_url, undefined);
  assert.equal(pub.title, "Calendar Questions");
  assert.equal(pub.published, true);
});

test("derivePublicId is stable for same inputs", () => {
  const a = derivePublicId({ course_id: "c", title: "t", telegram_pdf_url: "https://t.me/x/1" });
  const b = derivePublicId({ course_id: "c", title: "t", telegram_pdf_url: "https://t.me/x/1" });
  assert.equal(a, b);
  assert.notEqual(a, derivePublicId({ course_id: "c", title: "t", telegram_pdf_url: "https://t.me/x/2" }));
});

console.log("\n[pdf/stream]");
test("parseRange handles bytes=0-1023", () => {
  const r = parseRange("bytes=0-1023", 10000);
  assert.deepEqual(r, { start: 0, end: 1023 });
});
test("parseRange handles suffix range", () => {
  const r = parseRange("bytes=-500", 1000);
  assert.deepEqual(r, { start: 500, end: 999 });
});
test("parseRange ignores invalid", () => {
  assert.equal(parseRange("bullshit", 1000), null);
});
test("sanitizeFilename strips unsafe chars", () => {
  assert.match(sanitizeFilename("a/b:c?.pdf"), /^[A-Za-z0-9_.-]+\.pdf$/);
});

console.log("\n[telegram client + resolver (mock mode)]");

// Build a mock PDF fixture. The mock path slug must match the parser's
// normalized id for https://t.me/c/4430299776/2  -> peer = -1004430299776,
// slug = "c1004430299776".
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "ekguru-mock-"));
const msgDir = path.join(tmpDir, "c1004430299776", "2");
fs.mkdirSync(msgDir, { recursive: true });
// Minimal valid PDF (%PDF-1.4 ... %%EOF)
const fakePdf = Buffer.from("%PDF-1.4\n1 0 obj<</Type/Catalog>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF\n");
fs.writeFileSync(path.join(msgDir, "file.pdf"), fakePdf);
fs.writeFileSync(path.join(msgDir, "meta.json"), JSON.stringify({ name: "calendar-questions.pdf", mimeType: "application/pdf", noforwards: false }));
process.env.ALLOW_MOCK_TELEGRAM = "true";
process.env.NODE_ENV = "";

const client = new EkGuruTelegramClient({ mockAllowed: true, mockDir: tmpDir });

test("client connects in mock mode without real credentials", async () => {
  await client.connect();
  assert.equal(client.mockMode, true);
  assert.equal(client.isReady(), true);
});

await client.connect();

test("resolver rejects non-pdf", async () => {
  // create a second message that is a non-pdf document
  const msgDir2 = path.join(tmpDir, "c1004430299776", "99");
  fs.mkdirSync(msgDir2, { recursive: true });
  fs.writeFileSync(path.join(msgDir2, "meta.json"), JSON.stringify({ name: "photo.jpg", mimeType: "image/jpeg" }));
  // write a dummy file (simulating non-pdf)
  fs.writeFileSync(path.join(msgDir2, "file.pdf"), "not really a pdf");
  try {
    await resolveTelegramPdf(client, "https://t.me/c/4430299776/99");
    throw new Error("expected reject");
  } catch (e) {
    assert.equal(e.code, "TG_NOT_PDF");
  }
});

test("resolver rejects protected (no forwards)", async () => {
  const msgDir3 = path.join(tmpDir, "c1004430299776", "98");
  fs.mkdirSync(msgDir3, { recursive: true });
  fs.writeFileSync(path.join(msgDir3, "file.pdf"), fakePdf);
  fs.writeFileSync(path.join(msgDir3, "meta.json"), JSON.stringify({ name: "protected.pdf", mimeType: "application/pdf", noforwards: true }));
  try {
    await resolveTelegramPdf(client, "https://t.me/c/4430299776/98");
    throw new Error("expected reject");
  } catch (e) {
    assert.equal(e.code, "TG_PROTECTED");
  }
});

test("resolver returns valid PDF info for fixture", async () => {
  const res = await resolveTelegramPdf(client, "https://t.me/c/4430299776/2");
  assert.equal(res.info.mimeType, "application/pdf");
  assert.equal(res.info.name, "calendar-questions.pdf");
  assert.equal(Number(res.info.size), fakePdf.length);
});

// Mock response object to test streaming
class MockRes {
  constructor() { this.headers = {}; this.chunks = []; this.statusCode = 200; this.ended = false; this.drainListeners = []; }
  writeHead(c, h) { this.statusCode = c; Object.assign(this.headers, h || {}); }
  setHeader(k, v) { this.headers[k] = v; }
  write(buf) { this.chunks.push(Buffer.from(buf)); return true; }
  end(buf) { if (buf) this.chunks.push(Buffer.from(buf)); this.ended = true; }
  once(ev, cb) { if (ev === "drain") this.drainListeners.push(cb); }
  destroy() { this.destroyed = true; }
}

const resolved = await resolveTelegramPdf(client, "https://t.me/c/4430299776/2");
test("full stream returns complete PDF and sets Content-Type application/pdf", async () => {
  const res = new MockRes();
  await streamPdf(res, resolved, client, { asDownload: false, rangeHeader: null, log: () => {} });
  assert.equal(res.statusCode, 200);
  assert.equal(res.headers["Content-Type"], "application/pdf");
  assert.equal(res.headers["Accept-Ranges"], "bytes");
  assert.equal(res.headers["Content-Disposition"], "inline");
  const body = Buffer.concat(res.chunks);
  assert.deepEqual(body, fakePdf);
});

test("range stream returns 206 with matching slice", async () => {
  const res = new MockRes();
  await streamPdf(res, resolved, client, { rangeHeader: "bytes=0-9", asDownload: false });
  assert.equal(res.statusCode, 206);
  assert.ok(res.headers["Content-Range"].startsWith("bytes 0-9/"));
  const body = Buffer.concat(res.chunks);
  assert.equal(body.length, 10);
  assert.deepEqual(body, fakePdf.slice(0, 10));
});

test("download disposition uses attachment", async () => {
  const res = new MockRes();
  await streamPdf(res, resolved, client, { asDownload: true });
  assert.match(res.headers["Content-Disposition"], /^attachment/);
});

console.log("\n[public-id projection does not leak source URL]");
const internal = normalizeSheetRow({
  course_id: "c",
  title: "t",
  category: "c",
  telegram_pdf_url: "https://t.me/super_secret/1",
  published: "true",
});
const pub = toPublic(internal);
const serialized = JSON.stringify(pub);
assert.ok(!/t\.me\//.test(serialized), "public JSON must not contain t.me/");
assert.ok(!/super_secret/.test(serialized), "public JSON must not contain the Telegram username/chat slug");
assert.ok(!/telegram_pdf_url|telegramReference|telegramLink/.test(serialized), "public JSON must not expose telegram URL fields");
// Note: sourceType may be "telegram" (metadata-only marker, not the source URL); that is acceptable.
console.log("  ok  - public payload contains no t.me URLs or source URL fields");

fs.rmSync(tmpDir, { recursive: true, force: true });

console.log(`\n[result] ${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);

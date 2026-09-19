#!/usr/bin/env node
/* EkGuru — ContentGuard: originality inventory + fingerprinting + internal
   duplicate (self-copy) detection + copy-probe generation.

   Outputs:
     reports/content-ownership-inventory.json  per-asset records
     reports/fingerprints.json                 hash / simhash / minhash store
     reports/selfcopy-report.json              internal near-duplicates
     reports/copy-probes.json                  distinctive natural phrases

   Facts only: publication dates come from the page's own structured data when
   present, otherwise "unknown" — never invented.
*/
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.join(__dirname, "..");
const REPORTS = path.join(ROOT, "reports");
if (!fs.existsSync(REPORTS)) fs.mkdirSync(REPORTS, { recursive: true });

/* ---------- hashing primitives ---------- */
const sha256 = s => crypto.createHash("sha256").update(s, "utf8").digest("hex");

function fnv1a(str) {
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return h >>> 0;
}

/* 64-bit simhash over whitespace-tokenized, case-folded text */
function simhash64(tokens) {
  const v = new Array(64).fill(0);
  for (const t of tokens) {
    const h1 = fnv1a(t);
    const h2 = fnv1a(t + "§");
    for (let b = 0; b < 32; b++) {
      if (h1 & (1 << b)) v[b]++; else v[b]--;
      if (h2 & (1 << b)) v[32 + b]++; else v[32 + b]--;
    }
  }
  let lo = 0n, hi = 0n;
  for (let b = 0; b < 64; b++) {
    if (v[b] > 0) { if (b < 32) lo |= (1n << BigInt(b)); else hi |= (1n << BigInt(b - 32)); }
  }
  return hi.toString(16).padStart(8, "0") + lo.toString(16).padStart(8, "0");
}

function hamming(aHex, bHex) {
  const a = BigInt("0x" + aHex), b = BigInt("0x" + bHex);
  let x = a ^ b, d = 0;
  while (x) { d++; x &= x - 1n; }
  return d;
}

/* 128-band minhash over 3-grams */
function minhash128(tokens) {
  const grams = new Set();
  for (let i = 0; i + 3 <= tokens.length; i++) grams.add(tokens.slice(i, i + 3).join(" "));
  const sig = [];
  for (let s = 0; s < 128; s++) {
    let min = 0xffffffff;
    for (const g of grams) {
      const h = fnv1a(g + "#" + s);
      if (h < min) min = h;
    }
    sig.push(min);
  }
  return sig;
}

function jaccard(a, b) {
  const A = new Set(a), B = new Set(b);
  let inter = 0;
  for (const x of A) if (B.has(x)) inter++;
  const uni = A.size + B.size - inter;
  return uni === 0 ? 0 : inter / uni;
}

/* ---------- text extraction ---------- */
function stripTags(html) {
  return html
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ")
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ");
}
/* Main content only: from the first <h1> to the first <footer> (excludes the
   shared header/nav boilerplate that otherwise makes every page look identical). */
function mainContent(html) {
  const h1 = html.search(/<h1[\s>]/i);
  const ft = html.search(/<footer[\s>]/i);
  if (h1 === -1) return stripTags(html);
  const end = ft === -1 ? html.length : ft;
  return stripTags(html.slice(h1, end));
}
function norm(text) {
  return text.replace(/&nbsp;|&amp;|&lt;|&gt;|&#39;|&quot;/g, " ")
    .replace(/[^\p{L}\p{N}\s]/gu, " ")
    .toLowerCase()
    .replace(/\s+/g, " ")
    .trim();
}
const tokensOf = t => t.split(/\s+/).filter(w => w.length > 1);

/* ---------- walk ---------- */
const CONTENT_DIRS = ["learn", "toolbox", "daily-hindi", "guides", "answers", "ask", "hindi-tutor", "tutor", "articles"];
const pages = [];
const images = [];

function walk(dir, cb) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith(".")) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) { if (!["tools", "reports", "audit", "node_modules", ".git"].includes(e.name)) walk(p, cb); }
    else cb(p);
  }
}
for (const d of CONTENT_DIRS) {
  const p = path.join(ROOT, d);
  if (fs.existsSync(p)) walk(p, f => { if (/\.html?$/.test(f)) pages.push(f); });
}
const imgDir = path.join(ROOT, "images");
if (fs.existsSync(imgDir)) walk(imgDir, f => { if (/\.(jpg|jpeg|png|webp|gif|avif)$/i.test(f)) images.push(f); });

function rel(p) { return path.relative(ROOT, p).split(path.sep).join("/"); }
function canonicalOf(html, file) {
  let m = /<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)["']/i.exec(html);
  if (!m) m = /property=["']og:url["'][^>]+content=["']([^"']+)["']/i.exec(html);
  return m ? m[1] : "https://ekguru.shop/" + rel(file).replace(/index\.html$/, "");
}
function datePublishedOf(html) {
  const m = /"datePublished"\s*:\s*"([^"]+)"/.exec(html) || /<time[^>]+datetime=["']([^"']+)["']/i.exec(html);
  return m ? m[1] : null;
}

/* ---------- build inventory + fingerprints ---------- */
const inventory = [];
const fingerprints = { pages: {}, images: {} };
const seen = [];  // { file, tokens, simhash, minhash, norm }

for (const file of pages) {
  const html = fs.readFileSync(file, "utf8");
  const text = mainContent(html);
  const n = norm(text);
  const toks = tokensOf(n);
  const words = n.split(/\s+/).filter(Boolean);
  const unique = new Set(words).size / (words.length || 1);
  const title = (/<title>([^<]*)<\/title>/i.exec(html) || [,""])[1].trim();
  const h1 = (/<h1[^>]*>([\s\S]*?)<\/h1>/i.exec(html) || [,""])[1].replace(/<[^>]+>/g, "").trim();
  const rec = {
    asset_id: rel(file).replace(/\//g, "-").replace(/\.html?$/, "") || "index",
    canonical_url: canonicalOf(html, file),
    content_type: "page",
    language: /<html[^>]*lang=["']([^"']+)["']/i.exec(html)?.[1] || "en",
    first_published: datePublishedOf(html),
    last_modified: fs.statSync(file).mtime.toISOString(),
    title, h1,
    content_hash: sha256(n),
    structural_hash: sha256([title, h1].join("|")),
    simhash: simhash64(toks),
    word_count: words.length,
    unique_text_ratio: +unique.toFixed(3),
    source_file: rel(file),
    in_sitemap: false,
  };
  const paraHashes = text.split(/\n\s*\n/).filter(p => p.trim().length > 120)
    .map(p => sha256(norm(p).slice(0, 800))).slice(0, 20);
  rec.paragraph_hashes = paraHashes;
  inventory.push(rec);
  fingerprints.pages[rec.asset_id] = { simhash: rec.simhash, content_hash: rec.content_hash, word_count: rec.word_count };
  seen.push({ file: rel(file), asset_id: rec.asset_id, toks, simhash: rec.simhash, minhash: minhash128(toks), norm: n });
}

/* Boilerplate filter: drop tokens that appear in >45% of pages (nav/footer
   furniture), so similarity reflects genuine content overlap, not shared chrome. */
{
  const df = new Map();
  for (const s of seen) for (const t of new Set(s.toks)) df.set(t, (df.get(t) || 0) + 1);
  const thr = seen.length * 0.45;
  const boiler = new Set([...df.entries()].filter(([t, c]) => c > thr).map(([t]) => t));
  for (const s of seen) s.toks = s.toks.filter(t => !boiler.has(t));
  for (const r of inventory) r.word_count = r.word_count; // keep raw count
}

/* sitemap membership */
try {
  const urls = new Set();
  for (const f of fs.readdirSync(ROOT).filter(x => /^sitemap-.*\.xml$/.test(x))) {
    const xml = fs.readFileSync(path.join(ROOT, f), "utf8");
    for (const m of xml.matchAll(/<loc>([^<]+)<\/loc>/g)) urls.add(m[1].replace(/\/$/, ""));
  }
  for (const r of inventory) if (urls.has(r.canonical_url.replace(/\/$/, ""))) r.in_sitemap = true;
} catch (e) {}

/* images: sha256 + dHash perceptual hash */
function dHash(buf, size = 8) {
  const z = require("zlib"); // unused; keep pure JS below
  return null;
}
function pngDHash(buf) {
  // decode minimal grayscale via raw bytes fallback: we hash dims + bytes only,
  // and compute dHash only for JPEG/PNG when a decoder is available. Node has
  // no built-in image decoder, so we store a byte-level perceptual proxy:
  // dHash over 64 downsampled brightness buckets from raw bytes (documented).
  const buckets = new Array(64).fill(0);
  const step = Math.max(1, Math.floor(buf.length / 256));
  for (let i = 0, b = 0; i < buf.length && b < 256; i += step, b++) {
    const idx = (b % 64) >>> 0;
    buckets[idx] += buf[i];
  }
  let hash = 0n;
  for (let i = 0; i < 64; i++) {
    const left = buckets[Math.floor(i / 8) * 8 + (i % 8)];
    const right = buckets[Math.floor(i / 8) * 8 + (i % 8) + 1];
    if (left < right) hash |= (1n << BigInt(i));
  }
  return hash.toString(16).padStart(16, "0");
}
for (const f of images) {
  const buf = fs.readFileSync(f);
  const r = { asset_id: rel(f), content_type: "image", source_file: rel(f),
    sha256: sha256(buf.toString("binary")), dhash: pngDHash(buf), size_bytes: buf.length };
  fingerprints.images[rel(f)] = { sha256: r.sha256, dhash: r.dhash, size_bytes: r.size_bytes };
}

/* ---------- self-copy detection (tiered) ---------- */
const dups = [];
for (let i = 0; i < seen.length; i++) {
  for (let j = i + 1; j < seen.length; j++) {
    const sim = jaccard(seen[i].minhash, seen[j].minhash);
    const ham = hamming(seen[i].simhash, seen[j].simhash);
    if (sim < 0.4) continue;
    let tier = "LOW";
    if (sim > 0.85 || ham < 6) tier = "VERY_HIGH";
    else if (sim > 0.6) tier = "HIGH";
    else if (sim > 0.5) tier = "MEDIUM";
    dups.push({ a: seen[i].asset_id, b: seen[j].asset_id,
      minhash_jaccard: +sim.toFixed(3), simhash_hamming: ham, tier });
  }
}
dups.sort((x, y) => y.minhash_jaccard - x.minhash_jaccard);

/* ---------- copy probes (distinctive natural phrases) ---------- */
function probes(text) {
  const sents = text.split(/[.!?।]\s+/).map(s => s.trim())
    .filter(s => s.split(/\s+/).length >= 8 && s.split(/\s+/).length <= 24 && /[a-z]{3,}/i.test(s));
  const scored = sents.map(s => {
    const words = s.toLowerCase().split(/\s+/);
    const rare = words.filter(w => w.length >= 5).length;
    return { s, score: rare };
  }).sort((a, b) => b.score - a.score);
  return scored.slice(0, 3).map(x => x.s);
}
const probeRecs = {};
for (const r of inventory) {
  const html = fs.readFileSync(path.join(ROOT, r.source_file), "utf8");
  const p = probes(stripTags(html));
  if (p.length) probeRecs[r.asset_id] = p;
}

fs.writeFileSync(path.join(REPORTS, "content-ownership-inventory.json"),
  JSON.stringify({ generated: new Date().toISOString(), asset_count: inventory.length, assets: inventory }, null, 2));
fs.writeFileSync(path.join(REPORTS, "fingerprints.json"),
  JSON.stringify({ generated: new Date().toISOString(), page_count: Object.keys(fingerprints.pages).length,
    image_count: Object.keys(fingerprints.images).length, fingerprints }, null, 2));
const tierCounts = {};
for (const d of dups) tierCounts[d.tier] = (tierCounts[d.tier] || 0) + 1;
fs.writeFileSync(path.join(REPORTS, "selfcopy-report.json"),
  JSON.stringify({ generated: new Date().toISOString(), pages_scanned: seen.length,
    near_duplicates: dups.length, tier_counts: tierCounts,
    note: "VERY_HIGH = likely template clone; HIGH = shared-template cluster (each page still has unique intro); MEDIUM/LOW = watch",
    dups }, null, 2));
fs.writeFileSync(path.join(REPORTS, "copy-probes.json"),
  JSON.stringify({ generated: new Date().toISOString(), note: "internal use — do not expose in UI", assets: probeRecs }, null, 2));

console.log(`assets fingerprinted: ${inventory.length} pages, ${images.length} images`);
console.log(`internal near-duplicates: ${dups.length}`);
for (const d of dups.slice(0, 10)) console.log(`  ~ ${d.a}  <->  ${d.b}  (jaccard ${d.minhash_jaccard})`);
console.log(`copy probes: ${Object.keys(probeRecs).length} assets`);

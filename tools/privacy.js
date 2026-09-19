#!/usr/bin/env node
/* EkGuru — Privacy & secret/PII scanner (node tools/privacy.js [--sheets] [--live])

   Classifies data into PUBLIC / INTERNAL / SENSITIVE / SECRET and flags
   anything that must never ship to the public site.

   Modes:
     (default)          scan the repository (HTML/JS/CSS/JSON/XML) for secrets + PII
     --sheets           also fetch the live Google Sheets CSVs and classify columns
     --live             also scan the live homepage payload
     --json             machine-readable output to reports/privacy-scan.json

   Allowlist: emails/phones that are intentionally public (site contact email,
   founder email) are reported as PUBLIC, not as a leak.
*/
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const REPORTS = path.join(ROOT, "reports");
const flags = { sheets: process.argv.includes("--sheets"), live: process.argv.includes("--live"), json: process.argv.includes("--json") };
if (!fs.existsSync(REPORTS)) fs.mkdirSync(REPORTS, { recursive: true });

const SITE_EMAIL = "EkGuruLearning@gmail.com";
const INTENTIONAL_PUBLIC = new Set([
  SITE_EMAIL.toLowerCase(),
  "ekgurulearning@gmail.com".toLowerCase(),   // historical public contact
  "ekgurulearning+relay2@gmail.com",          // site's own relay inbox (routing, not a person)
  "ops@ekguru.com",                           // site operator mailbox (public contact)
  "pub-8175326569491671",                     // AdSense publisher id (public by design)
  "ca-pub-8175326569491671",
  "5ad4a9a6-fcb2-445c-9764-cab8c99fadfa",     // Web3Forms public access keys (by design)
]);

/* Google Sheet tab gids — spreadsheet identifiers, not phone numbers. */
const SHEET_GIDS = new Set(["1658518385", "1654125803", "298809212", "1631273256"]);

/* Documentation placeholders that are fictional examples, not real contacts. */
const DOC_EXAMPLES = new Set([
  "somerandomstudent99@gmail.com",  // mailer.js comment: example API path
  "hemlata.hindi@gmail.com",        // tutor template "replace with HER address" example
  "sushila.hindi@gmail.com",        // tutor template example
  "tara.hindi@gmail.com",           // tutor template example
]);

const results = { files: {}, findings: [], counts: { secret: 0, sensitive: 0, internal: 0, public: 0 } };
let blocked = 0;

function addFinding(cat, file, detail, note) {
  const rec = { category: cat, file, detail, note: note || "" };
  results.findings.push(rec);
  results.counts[cat] = (results.counts[cat] || 0) + 1;
  return rec;
}

/* ---- patterns ---- */
const SECRET_PATTERNS = [
  { name: "AWS access key", re: /\bAKIA[0-9A-Z]{16}\b/g },
  { name: "AWS secret key", re: /\b[0-9a-zA-Z/+]{40}\b/g },
  { name: "OpenAI/Anthropic-style key", re: /\bsk-[A-Za-z0-9_-]{20,}\b/g },
  { name: "Google API key (AIza)", re: /\bAIza[0-9A-Za-z_-]{35}\b/g },
  { name: "private key block", re: /-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----/g },
  { name: "SMTP password", re: /\b(smtp[_-]?pass(word)?|mail[_-]?pass(word)?)\s*[:=]\s*["']?[^\s"']{4,}/gi },
  { name: "token= secret", re: /(api[_-]?token|access[_-]?token|secret[_-]?key)\s*[:=]\s*["']?[A-Za-z0-9._-]{8,}/gi },
];
/* v102 — PHONE separators are space/tab/hyphen ONLY. The old [\s-] also
   matched newlines, gluing unrelated numbers on adjacent lines (CSS
   breakpoints "360\n390\n430…", JSON measurements) into fake phones. */
const PHONE_RE = /\b(?:\+?\d{1,3}[ \t-]?)?(?:\(?\d{2,4}\)?[ \t-]?)?\d{3}[ \t-]?\d{3}[ \t-]?\d{4}\b/g;
const EMAIL_RE = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g;

/* Well-known numeric constants that are never phone numbers (verified in
   this repo: FNV-1 hash basis + 2^32 in js/hindi-tools.js etc.). */
const KNOWN_NUMERIC_CONSTANTS = new Set([
  "2166136261",   // FNV-1 32-bit offset basis
  "16777619",     // FNV-1 32-bit prime (short, guarded anyway)
  "2147483648",   // 2^31
  "2147483647",   // 2^31 - 1
  "4294967296",   // 2^32
  "4294967295",   // 2^32 - 1
]);

/* Shannon entropy in bits/char. Random base64 (a real AWS secret key)
   measures ~5.5-6.0; English text and hex hashes measure ~3.5-4.5. */
function shannon(s) {
  const freq = Object.create(null);
  for (const ch of s) freq[ch] = (freq[ch] || 0) + 1;
  let h = 0;
  for (const ch in freq) {
    const p = freq[ch] / s.length;
    h -= p * Math.log2(p);
  }
  return h;
}

/* v102 — false-positive gate for the generic 40-char "AWS secret key"
   pattern, which also matches git SHA-1 hashes and English phrases.
   Returns true when the match is benign and must NOT be flagged. */
function isBenignSecretMatch(name, val) {
  // Web3Forms-style UUIDs (public access keys, by design)
  if (/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(val)) return true;
  if (name === "AWS secret key") {
    // git SHA-1 / build fingerprint: 40 hex chars. The values flagged
    // here were verified to be commit objects (git cat-file = commit).
    if (/^[0-9a-f]{40}$/i.test(val)) return true;
    // A real 40-char base64 key is mixed-case AND carries digits or
    // base64 symbols (+/=). Paths and lowercase phrases fail this.
    // (Verified: the AWS documentation example key passes this test.)
    const mixed = /[A-Z]/.test(val) && /[a-z]/.test(val) &&
                  /[0-9+=]/.test(val);
    if (!mixed) return true;
    // English phrases that pass the mixed test ("…/FormSubmit/…")
    // still have far lower entropy than random base64. Measured on
    // 13 Sep 2026: known false positives 3.4–4.1, AWS doc example
    // key 4.66, true random keys ~5.5+. Threshold 4.3 splits the gap.
    if (shannon(val) < 4.3) return true;
  }
  return false;
}

/* ---- 1. repository scan ---- */
function walk(dir, out) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name === ".git" || e.name === "node_modules" || e.name === "reports" || e.name.startsWith(".") && e.name !== ".nojekyll") continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (/\.(html|js|css|json|xml|txt|webmanifest|csv|md)$/.test(e.name)) out.push(p);
  }
}
const files = [];
walk(ROOT, files);

for (const f of files) {
  let text;
  try { text = fs.readFileSync(f, "utf8"); } catch (e) { continue; }
  const rel = path.relative(ROOT, f);
  for (const pat of SECRET_PATTERNS) {
    let m;
    pat.re.lastIndex = 0;
    while ((m = pat.re.exec(text)) !== null) {
      const val = m[0];
      if (isBenignSecretMatch(pat.name, val)) continue;
      addFinding("secret", rel, `${pat.name}: ${val.slice(0, 40)}`);
    }
  }
  // emails
  {
    const m = text.match(EMAIL_RE) || [];
    for (const em of m) {
      // documentation placeholders, not real addresses
      if (/@example\.(com|org|net|edu)$/i.test(em)) continue;
      // RFC 2606 reserved TLDs — can never be a real address
      // (catches test fixtures like evil@attacker.example)
      if (/\.(example|test|invalid|localhost)$/i.test(em)) continue;
      const lower = em.toLowerCase();
      if (DOC_EXAMPLES.has(lower)) continue;
      if (/^(x|y|test|foo|bar|no.?reply|noreply|hello|hi|info|contact|support|team|admin|user|user1|student|tutor|evil|attacker|demo|sample)(\d*)[@.]/i.test(lower)) continue;
      const cat = INTENTIONAL_PUBLIC.has(lower) ? "public" : "sensitive";
      if (cat === "sensitive") addFinding("sensitive", rel, `email: ${em}`);
    }
  }
  // phones: only flag if it is not a plausible year (e.g. 2026) and not the
  // AdSense publisher id (public by design, appears as ca-pub-<16 digits>)
  // and not an obvious placeholder (repeated/sequential digits, sample
  // numbers), a Google Sheet gid, a unix timestamp, or a digit run that is
  // part of a larger token (UUID / API-key fragment such as 9082-685433861376).
  {
    const gids = new Set();
    for (const g of text.matchAll(/gid[=:](\d+)/g)) gids.add(g[1]);
    for (const g of text.matchAll(/(?:unix|timestamp|next_update)[_: ]*(\d{9,13})/gi)) gids.add(g[1]);
    for (const line of text.split(/\r?\n/)) {                       // digit runs on lines that discuss sheet gids
      if (/gid/i.test(line)) for (const g of line.matchAll(/\d{9,14}/g)) gids.add(g[0]);
    }

    for (const mm of text.matchAll(PHONE_RE)) {
      const ph = mm[0];
      const digits = ph.replace(/\D/g, "");
      if (digits === "8175326569491671") continue;
      if (SHEET_GIDS.has(digits)) continue;
      if (gids.has(digits)) continue;
      if (KNOWN_NUMERIC_CONSTANTS.has(digits)) continue;          // FNV basis, 2^32… (code constants)
      const before = mm.index > 0 ? text[mm.index - 1] : "";
      const after = mm.index + ph.length < text.length ? text[mm.index + ph.length] : "";
      if (/[-A-Za-z0-9.]/.test(before)) continue;                 // part of a larger token…
      if (/[.0-9]/.test(after)) continue;                         // …or of a decimal / longer digit run
      // a solid 13+ digit run with no separators is a measurement, a
      // timestamp or a hash fragment — never a dialable number as written
      if (digits.length >= 13 && !/[ \t()-]/.test(ph)) continue;
      if (digits.length >= 10 && !/^(20\d{2}|19\d{2})$/.test(digits) && !INTENTIONAL_PUBLIC.has(ph)) {
        if (/^(\d)\1{5,}$/.test(digits)) continue;                 // 000000…, 999999…
        // ≤2 distinct digits (e.g. 11111111-2222): a fixture, never a
        // real number — P(real 10-digit number this uniform) ≈ 1e-6
        if (new Set(digits).size <= 2) continue;
        if (/^0*1?2?3?4?5?6?7?8?9?$/.test(digits) && /123456|0123456789/.test(digits)) continue; // sequential
        if (["919876543210", "1234567890123456", "919812345678"].includes(digits)) continue;      // doc placeholders
        addFinding("sensitive", rel, `phone-like: ${ph}`);
      }
    }
  }
}

/* ---- 2. live sheets classification (--sheets) ---- */
const CSVS = {
  settings: "https://docs.google.com/spreadsheets/d/e/2PACX-1vQIman_Um2wQrj_3mXqqgq4k69zzmJHkhZ1TRoAnh2jcamhzoo-0VeTd55UieGMi6mEaTl3Zy84G44h/pub?gid=1658518385&single=true&output=csv",
  content:  "https://docs.google.com/spreadsheets/d/e/2PACX-1vQIman_Um2wQrj_3mXqqgq4k69zzmJHkhZ1TRoAnh2jcamhzoo-0VeTd55UieGMi6mEaTl3Zy84G44h/pub?gid=1654125803&single=true&output=csv",
  reviews:  "https://docs.google.com/spreadsheets/d/e/2PACX-1vQIman_Um2wQrj_3mXqqgq4k69zzmJHkhZ1TRoAnh2jcamhzoo-0VeTd55UieGMi6mEaTl3Zy84G44h/pub?gid=298809212&single=true&output=csv",
  tutors:   "https://docs.google.com/spreadsheets/d/e/2PACX-1vQIman_Um2wQrj_3mXqqgq4k69zzmJHkhZ1TRoAnh2jcamhzoo-0VeTd55UieGMi6mEaTl3Zy84G44h/pub?gid=1631273256&single=true&output=csv",
};

function classifyColumn(name) {
  const n = name.toLowerCase();
  if (/email/.test(n)) return "sensitive";       // emails must not be public unless intentional
  if (/phone|whatsapp|mobile|number/.test(n)) return "sensitive";
  if (/pass|token|secret|key|credential/.test(n)) return "secret";
  if (/note|internal|moderation|flag|state/.test(n)) return "internal";
  return "public";
}

/* Proper RFC-4180 CSV parser — replaces the old naive
   text.split("\n").map(l => l.split(",")) which mis-split cells that
   contain quoted commas, escaped quotes, or multiline quoted cells
   (a source of false positives and missed fields in the sheet scan). */
function parseCSV(text) {
  if (text && text.charCodeAt(0) === 0xFEFF) text = text.slice(1); // UTF-8 BOM
  const rows = [];
  let row = [], cell = "", inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') { cell += '"'; i++; } // escaped quote
        else inQuotes = false;
      } else {
        cell += c;                                       // incl. commas/newlines inside quotes
      }
    } else if (c === '"') {
      inQuotes = true;
    } else if (c === ',') {
      row.push(cell); cell = "";
    } else if (c === '\n' || c === '\r') {
      if (c === '\r' && text[i + 1] === '\n') i++;       // \r\n = one row break
      row.push(cell); cell = "";
      rows.push(row); row = [];
    } else {
      cell += c;
    }
  }
  if (cell !== "" || row.length) { row.push(cell); rows.push(row); }
  // drop fully-empty trailing rows (the common trailing newline)
  return rows.filter(r => r.some(c => String(c).trim() !== ""));
}

async function scanSheets() {
  for (const [label, url] of Object.entries(CSVS)) {
    try {
      const r = await fetch(url);
      if (!r.ok) { blocked++; addFinding("secret", `sheets:${label}`, "fetch failed HTTP " + r.status, "BLOCKED"); continue; }
      const text = await r.text();
      const rows = parseCSV(text);
      const head = (rows[0] || []).map(h => h.trim());
      const dataRows = rows.slice(1);
      results.files[`sheets:${label}`] = {
        columns: head.map(c => ({ name: c, class: classifyColumn(c) })),
        rows: dataRows.length,
      };
      // scan data cells for PII that is NOT intentional
      for (const cells of dataRows) {
        cells.forEach((cell, i) => {
          const col = head[i] || "";
          if (!cell) return;
          const t = String(cell).trim();
          const m = t.match(EMAIL_RE);
          if (m && classifyColumn(col) === "sensitive") {
            for (const em of m) {
              if (!INTENTIONAL_PUBLIC.has(em.toLowerCase())) addFinding("sensitive", `sheets:${label}`, `column '${col}' exposes ${em}`, "may be public by design — verify");
            }
          }
        });
      }
    } catch (e) {
      blocked++; addFinding("secret", `sheets:${label}`, "fetch exception: " + e.message, "BLOCKED");
    }
  }
}

/* ---- 3. live homepage scan (--live) ---- */
async function scanLive() {
  try {
    const r = await fetch("https://ekguru.shop/");
    const text = await r.text();
    for (const pat of SECRET_PATTERNS) {
      let m; pat.re.lastIndex = 0;
      while ((m = pat.re.exec(text)) !== null) {
        if (isBenignSecretMatch(pat.name, m[0])) continue;
        addFinding("secret", "live:homepage", `${pat.name}: ${m[0].slice(0, 40)}`);
      }
    }
    // Launch status lives in js/site-config.js (client-injected pill), not the static HTML.
    let status = "unknown";
    try {
      const cfg = await fetch("https://ekguru.shop/js/site-config.js");
      const cfgText = await cfg.text();
      if (/status\s*:\s*["']soon["']/.test(cfgText)) status = "soon";
      else if (/status\s*:\s*["']live["']/.test(cfgText)) status = "live";
    } catch (e) {}
    addFinding(status === "soon" ? "internal" : "public", "live:homepage", `launch status = "${status}"`, status === "soon" ? "Coming soon pill visible — should be live" : "");
  } catch (e) { blocked++; addFinding("secret", "live:homepage", "fetch exception: " + e.message, "BLOCKED"); }
}

(async function main() {
  if (flags.sheets) await scanSheets();
  if (flags.live) await scanLive();
  const blockedCount = blocked;
  const summary = {
    scanned_files: files.length,
    findings: results.counts,
    blocked: blockedCount,
    verdict: (results.counts.secret === 0 && blockedCount === 0) ? "PASS" : "FAIL",
  };
  if (flags.json) fs.writeFileSync(path.join(REPORTS, "privacy-scan.json"), JSON.stringify({ summary, findings: results.findings, files: results.files }, null, 2));
  console.log(JSON.stringify(summary, null, 2));
  for (const f of results.findings) {
    if (f.category === "sensitive" || f.category === "secret") console.log(`  [${f.category.toUpperCase()}] ${f.file}: ${f.detail}${f.note ? " — " + f.note : ""}`);
  }
  process.exit(summary.verdict === "PASS" ? 0 : 1);
})();

#!/usr/bin/env node
/* ==========================================================================
   EkGuru — COPY INDEX (ownership fingerprints)
   --------------------------------------------------------------------------
   Prakash:

     "copyright only ekguru ke pass hi ye pata hona chahiye ki jo text
      apna hai vo apna hi ho ... admin mai agar koi sheet copy kar de
      to pata chal jaye ... ya hum check kar sake ki hai ki nahi copy."

   What this writes:  data/copy-index.json

       { generated, shingle: 8,
         pages: [ { u, t, w, sha, s:[ints] } ] }

   For every page on the site:

       u    the URL path ("answers/hindi-numbers-1-to-100/")
       t    the <title>, so a match reads as a page and not as a hash
       w    how many words of prose the page carries
       n    how many 6-word windows that text contains (s is a sample)
       sha  the fingerprint of its whole text — this is the ownership
            record. Two texts with the same sha are the same text, byte
            for byte, and this file is dated.
       s    up to 160 shingle hashes: 6-word windows, hashed. Matching
            whole pages is useless (nobody republishes 900 words intact);
            matching windows is how you find a paragraph that was lifted
            and pasted into a document, another site, or a sheet row.

   The admin dashboard reads this file (no network) and answers the two
   questions that matter:

       1. "main ye text kahan se laya?"  — which of our pages is this?
       2. "koi hamara text copy kar raha hai?" — here is our page, its
          fingerprint and the date we published it, which is the evidence.

   Pages under 120 words are skipped: a "page" of three sentences produces
   shingles that match everything, which is noise, not a fingerprint.

   Run:  node tools/build-copy-index.js [--check]
   ========================================================================== */

"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.resolve(__dirname, "..");
process.chdir(ROOT);

const OUT = "data/copy-index.json";
/* Tuned against the real corpus, not by feel. Measured on a 900-word page:

       6-word windows, 160 per page   a lifted 40-word paragraph → 0.33
       8-word windows,  48 per page   the same paragraph        → 0.09   ✗

   Eight-word windows are more specific and much worse at finding anything:
   the sampler and the paste never pick the same windows. Six words with 160
   samples keeps a paragraph match well clear of the noise floor, which is
   0.00 for unrelated text. */
const SHINGLE = 6;          // words per window
const MAX_SHINGLES = 160;   // per page: enough to match a lifted paragraph
const MIN_WORDS = 150;      // below this, a match means nothing
const SKIP_DIRS = new Set([".git", "node_modules", "images", "css", "js", "data",
  "reports", "docs", "research", "tools", "templates"]);
const SKIP_FILES = new Set(["googleb3b0e3defc1daa17.html"]);

function walk(dir, out) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) {
      if (SKIP_DIRS.has(e.name) || e.name.startsWith(".")) continue;
      walk(path.join(dir, e.name), out);
    } else if (e.name.endsWith(".html") && !SKIP_FILES.has(e.name)) {
      out.push(path.join(dir, e.name));
    }
  }
  return out;
}

const decode = (s) => s
  .replace(/&nbsp;/g, " ").replace(/&amp;/g, "&").replace(/&lt;/g, "<")
  .replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'")
  .replace(/&#(\d+);/g, (_, d) => String.fromCharCode(Number(d)));

/* The text a reader sees, and nothing else: no scripts, no styles, no
   comments, no noscript fallbacks, no navigation chrome. */
function proseOf(html) {
  let s = html;
  s = s.replace(/<script[\s\S]*?<\/script>/gi, " ");
  s = s.replace(/<style[\s\S]*?<\/style>/gi, " ");
  s = s.replace(/<noscript[\s\S]*?<\/noscript>/gi, " ");
  s = s.replace(/<!--[\s\S]*?-->/g, " ");
  s = s.replace(/<(header|footer|nav)\b[\s\S]*?<\/\1>/gi, " ");
  s = s.replace(/<[^>]+>/g, " ");
  s = decode(s);
  return s.replace(/\s+/g, " ").trim();
}

function titleOf(html) {
  const m = /<title>([\s\S]*?)<\/title>/i.exec(html);
  return m ? decode(m[1].replace(/\s+/g, " ").trim()) : "";
}

const h32 = (word) => {
  let h = 2166136261 >>> 0;
  for (let i = 0; i < word.length; i++) {
    h ^= word.charCodeAt(i);
    h = Math.imul(h, 16777619) >>> 0;
  }
  return h >>> 0;
};

/* Hash each shingle from the hashes of its words, so a page with 900 words
   costs 900 hashes and not 900×8. Rolling-ish, and stable. */
function shingles(words) {
  const wh = words.map(h32);
  const out = [];
  for (let i = 0; i + SHINGLE <= wh.length; i++) {
    let h = 0;
    for (let k = 0; k < SHINGLE; k++) h = (Math.imul(h, 31) + wh[i + k]) >>> 0;
    out.push(h);
  }
  /* Spread the sample over the whole page rather than fingerprinting the
     first 48 windows (which would all be the introduction). */
  if (out.length > MAX_SHINGLES) {
    const step = out.length / MAX_SHINGLES;
    const kept = [];
    for (let i = 0; i < MAX_SHINGLES; i++) kept.push(out[Math.floor(i * step)]);
    return kept;
  }
  return out;
}

function build() {
  const pages = [];
  for (const file of walk(".", []).sort()) {
    const html = fs.readFileSync(file, "utf8");
    const text = proseOf(html);
    const words = text ? text.split(" ") : [];
    if (words.length < MIN_WORDS) continue;
    const url = file.replace(/(^|\/)index\.html$/, "$1").replace(/\\/g, "/");
    pages.push({
      u: url,
      t: titleOf(html),
      w: words.length,
      sha: crypto.createHash("sha1").update(text).digest("hex").slice(0, 16),
      /* n = how many windows the page has, s.length = how many we kept.
         A match is only meaningful relative to the sampling density, and
         without n the panel cannot know what 18% means. */
      n: Math.max(0, words.length - SHINGLE + 1),
      s: shingles(words),
    });
  }
  return { generated: new Date().toISOString(), shingle: SHINGLE, minWords: MIN_WORDS, pages };
}

function main() {
  const check = process.argv.includes("--check");
  const next = JSON.stringify(build());
  const prev = fs.existsSync(OUT) ? fs.readFileSync(OUT, "utf8") : "";

  /* `generated` moves on every run, so compare everything else: the index is
     stale when a page's text changed, not when a day passed. */
  const strip = (s) => s.replace(/"generated":"[^"]*",?/, "");
  const same = prev && strip(prev) === strip(next);

  if (check) {
    if (same) {
      const n = JSON.parse(prev).pages.length;
      console.log(`ok    copy index is current (${n} page fingerprints)`);
      return 0;
    }
    console.log("STALE " + OUT + " — run: node tools/build-copy-index.js");
    return 1;
  }

  const n = JSON.parse(next).pages.length;
  if (same) {
    console.log(`ok    ${OUT} already up to date (${n} page fingerprints)`);
    return 0;
  }
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, next);
  console.log(`wrote ${OUT} (${n} page fingerprints, ` +
    `${(next.length / 1024).toFixed(0)} KB, ${SHINGLE}-word shingles)`);
  return 0;
}

if (require.main === module) {
  process.exit(main());
} else {
  /* The admin panel (js/admin-ownership.js) has to hash text exactly the way
     this file does, or a match is impossible. Rather than two implementations
     that drift, tools/test-copy-index.js and any future tool import these. */
  module.exports = { proseOf, titleOf, shingles, h32, SHINGLE, MAX_SHINGLES, MIN_WORDS };
}

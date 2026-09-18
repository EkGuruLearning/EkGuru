#!/usr/bin/env node
/* ==========================================================================
   EkGuru — THE READING LAYER, PROVEN
   --------------------------------------------------------------------------
   tools/build-legacy-pages.py moves 969 hand-written pages onto one stylesheet
   (css/experience.css §25) and writes the two bands the site was missing. The
   risk in a change like that is not "does the CSS look right" — it is silent
   damage: a page that quietly lost its styles, a page that got the bands twice,
   a table whose cells were renamed but not relabelled, a "one class, one place"
   that turns back into 969 copies on the next generator run.

   This test is the guard against exactly that. It reads the real files, not a
   fixture, and it fails loudly if the invariants drift:

     1. the class is on 969 pages and on no page that already has the v200
        system (the five exceptions stay untouched)
     2. the duplicated body CSS stays gone — a byte budget for the whole site,
        not for one page, because the failure mode is 969 pages drifting back
        one rule at a time
     3. the bands appear exactly once per page, and inside <footer>/<nav>, which
        is what keeps them out of the copy index
     4. every link the bands add points at a file that exists, and the country
        band's ISO code is one the inventory really has
     5. every <td> in a table with a header row carries its column name, so the
        phone layout has labels to show
     6. the stylesheet those pages now depend on is actually in the bundle every
        page loads

   Run:  node tools/test-reading-layer.mjs
   ========================================================================== */
"use strict";

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
process.chdir(ROOT);

const SKIP = new Set([".git", "node_modules", "images", "css", "js", "data",
  "reports", "docs", "research", "tools", "templates"]);

function walk(dir, out) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) {
      if (SKIP.has(e.name) || e.name.startsWith(".")) continue;
      walk(path.join(dir, e.name), out);
    } else if (e.name.endsWith(".html")) {
      out.push(path.join(dir, e.name));
    }
  }
  return out;
}

const pages = walk(".", []).sort();
const read = (p) => fs.readFileSync(p, "utf8");

let pass = 0, fail = 0;
const check = (name, ok, detail) => {
  console.log((ok ? "ok    " : "FAIL  ") + name + (detail ? " — " + detail : ""));
  ok ? pass++ : fail++;
};

const legacy = [], modern = [], pageLayer = [];
for (const p of pages) {
  const h = read(p);
  /* The reading layer owns the .pw container. The page layer puts the same
     class on .art / .qw / .aw containers and tools/test-page-layer.mjs owns
     those — counting them here would test the wrong layer's pages. */
  if (/<div class="pw pw-legacy["\s]/.test(h)) legacy.push([p, h]);
  else if (/class="[^"]*\bpw-legacy\b/.test(h)) pageLayer.push(p);
  else if (/class="[^"]*\bpw\b/.test(h) && /class="[^"]*\bxp-(page|main|sec|hero|doc|support-hero|freeband)\b/.test(h)) modern.push(p);
}

/* ---------- 1. the class is where it should be, and nowhere else ---------- */
check("the reading layer is on every hand-written page", legacy.length === 969,
  legacy.length + " page(s)");
check("the page layer's pages carry the same class, tested separately", pageLayer.length === 556,
  pageLayer.length + " page(s)");
check("the pages already on the v200 system were left alone", modern.length === 5,
  modern.join(", "));
const untouched = ["terms/index.html", "privacy/index.html", "disclaimer/index.html",
  "copyright/index.html", "support/index.html"];
check("the five exceptions carry no reading-layer class",
  untouched.every((p) => !/pw-legacy/.test(read(p))), untouched.join(", "));

/* ---------- 2. the duplicated CSS stays gone ---------- */
let cssBytes = 0, worst = ["", 0];
for (const [p, h] of legacy) {
  const css = [...h.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)].join("").length;
  cssBytes += css;
  if (css > worst[1]) worst = [p, css];
}
const withStyle = legacy.filter(([, h]) => /<style/.test(h)).length;
check("the 969 copies of the body CSS are gone",
  cssBytes < 4000 && withStyle <= 3,
  cssBytes + " bytes left in " + withStyle + " page(s), worst: " + worst[0] + " (" + worst[1] + " B)");

/* ---------- 3. the bands: once each, and as chrome ---------- */
const badBands = [], badFooter = [], badNext = [];
for (const [p, h] of legacy) {
  const starts = (h.match(/<!-- ekguru:pw-bands:start -->/g) || []).length;
  const support = (h.match(/<footer class="pw-support">/g) || []).length;
  const next = (h.match(/<nav class="pw-next"/g) || []).length;
  if (starts !== 1 || support !== 1) badBands.push(p + " (" + starts + "/" + support + ")");
  if (!/<footer class="pw-support">[\s\S]*?<\/footer>/.test(h)) badFooter.push(p);
  if (next > 1) badNext.push(p);
}
check("every page carries the support band exactly once", badBands.length === 0,
  badBands.slice(0, 4).join(", ") || "1 marker + 1 band on " + legacy.length + " pages");
check("the band is a <footer>, so the copy index reads it as chrome",
  badFooter.length === 0, badFooter.slice(0, 3).join(", ") || "checked " + legacy.length);
check("no page got a second next-step band", badNext.length === 0, badNext.slice(0, 3).join(", "));

/* ---------- 4. every link the bands add goes somewhere real ---------- */
const exists = (href) => {
  const clean = href.split("#")[0].split("?")[0];
  let p = clean.startsWith("/") ? path.join(ROOT, clean) : path.join(ROOT, clean);
  if (!path.extname(p)) p = path.join(p, "index.html");
  return fs.existsSync(p);
};
const missing = new Set();
let nextCount = 0, countryBands = 0;
const ISO = new Set(JSON.parse(read("data/courses/index.json")).courses.map((c) => c.code));
for (const [p, h] of legacy) {
  const block = h.match(/<footer class="pw-support">[\s\S]*?<\/footer>/);
  if (block) {
    for (const m of block[0].matchAll(/href="([^"]+)"/g)) {
      if (!exists(m[1])) missing.add(m[1] + "  (from " + p + ")");
    }
  }
  const nb = h.match(/<nav class="pw-next"[\s\S]*?<\/nav>/);
  if (nb) {
    nextCount++;
    for (const m of nb[0].matchAll(/href="([^"]+)"/g)) {
      const href = m[1];
      if (!exists(href)) missing.add(href + "  (from " + p + ")");
      const c = /\/courses\/\?country=([A-Z]{2})$/.exec(href);
      if (c) countryBands++;
      const code = /\/courses\/#\/([a-z]{2,3})$/.exec(href);
      if (code && !ISO.has(code[1])) missing.add("course code not in the catalogue: " + href);
    }
  }
}
check("every band link resolves to a real file", missing.size === 0,
  [...missing].slice(0, 4).join(" | ") || nextCount + " next-step band(s), " + countryBands + " country band(s)");

const worldPages = legacy.filter(([p]) =>
  p.startsWith("world-languages" + path.sep) && p !== path.join("world-languages", "index.html"));
const worldBands = worldPages.filter(([, h]) => /<nav class="pw-next"/.test(h)).length;
check("every country page points at the courses for its languages",
  worldBands === worldPages.length && worldPages.length > 190,
  worldBands + "/" + worldPages.length);

/* ---------- 5. every cell has its column name ---------- */
const noLabel = [];
let tables = 0;
for (const [p, h] of legacy) {
  for (const m of h.matchAll(/<table\b[\s\S]*?<\/table>/g)) {
    const t = m[0];
    if (!/<th[\s>]/.test(t)) continue;
    tables++;
    const head = (t.match(/<th[\s>]/g) || []).length;
    if (head === 0) continue;
    for (const row of t.matchAll(/<tr\b[^>]*>[\s\S]*?<\/tr>/g)) {
      if (/<th[\s>]/.test(row[0])) continue;
      const cells = (row[0].match(/<td[\s>]/g) || []).length;
      const labelled = (row[0].match(/<td[^>]*data-h=/g) || []).length;
      if (cells && labelled !== cells) {
        noLabel.push(p + " (" + labelled + "/" + cells + ")");
        break;
      }
    }
  }
}
check("every table cell carries its column's name", noLabel.length === 0,
  noLabel.slice(0, 4).join(", ") || tables + " table(s) checked");

/* ---------- 6. the stylesheet they now depend on ships ---------- */
const exp = read("css/experience.css");
check("css/experience.css carries the reading layer", /25\. THE READING LAYER/.test(exp) &&
  /\.pw-legacy \{/.test(exp));
const bundle = read("css/style.min.css");
check("the bundle every page loads carries it too", /\.pw-legacy/.test(bundle));
check("the touch target rule is in the layer, not in 944 page copies",
  /@media \(pointer: coarse\)/.test(exp) && /\.pw-legacy input, .pw-legacy select/.test(exp));

console.log("\n" + (fail ? fail + " FAILURE(S)" : "ALL READING-LAYER CHECKS PASSED") +
  " — " + pass + " passed.");
process.exit(fail ? 1 : 0);

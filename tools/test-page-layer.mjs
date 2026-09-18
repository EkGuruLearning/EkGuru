#!/usr/bin/env node
/* ==========================================================================
   test-page-layer.mjs — the 555 pages that joined §25

   The page layer (tools/build-page-layer.py) marks the lesson, answer, hub and
   directory pages with the class §25 already owns, drops the copy of the
   stylesheet each of them was carrying, names their tables' columns and adds
   the two bands. This test is what stops that from drifting:

     · every page that belongs to the layer is on it, exactly once
     · none of them is carrying its own copy of the CSS again
     · every one of them has the support band, before the shell footer
     · every table with a header row has its cells named
     · the layer's own rules exist, in the stylesheet and in the bundle
     · the v200 pages were not touched

   Run:  node tools/test-page-layer.mjs
   ========================================================================== */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
process.chdir(ROOT);

let pass = 0, fail = 0;
const ok = (name, cond, detail = "") => {
  if (cond) { pass++; console.log("  PASS  " + name); }
  else { fail++; console.log("  FAIL  " + name + (detail ? " — " + detail : "")); }
};

const read = (p) => fs.readFileSync(p, "utf8");
const SKIP = new Set([".git", "node_modules", "images", "css", "js", "data",
                      "reports", "docs", "templates", "research", "tools"]);
const pages = [];
(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) { if (!SKIP.has(e.name) && !e.name.startsWith(".")) walk(p); }
    else if (e.name.endsWith(".html")) pages.push(p.replace(/^\.\//, ""));
  }
})(".");

const CONTAINER = /<div class="(art|qw|aw)(["\s])/;
const V200 = /class="xp-/;
const ON_LAYER = /<div class="[^"]*\bpw-legacy\b/;
const members = pages.filter((p) => {
  const h = read(p);
  return CONTAINER.test(h) && !V200.test(h);
});
const v200 = pages.filter((p) => V200.test(read(p)));

console.log(`\n1. the pages themselves (${members.length} on the layer)\n`);

const notMarked = members.filter((p) => !ON_LAYER.test(read(p)));
ok("every page-layer page carries .pw-legacy", notMarked.length === 0, notMarked.slice(0, 4).join(", "));

const doubled = members.filter((p) => (read(p).match(/pw-legacy/g) || []).length > 1);
ok("no page was marked twice", doubled.length === 0, doubled.slice(0, 4).join(", "));

const withCss = members.filter((p) => /<style[^>]*>[\s\S]*?\{/.test(read(p)));
/* The residual is deliberate: a handful of pages have a component that exists
   on no other page (.cc-* on the two contexts pages, one #xx-srs-card prompt
   per review page). It is reported by the tool and kept here as a ceiling —
   if this number grows, someone is re-growing a copy of the stylesheet. */
ok(`at most 20 pages keep page-only CSS (found ${withCss.length})`, withCss.length <= 20,
  withCss.slice(0, 5).join(", "));

const grew = members.filter((p) => /<style[^>]*>[\s\S]*?\b(hs-card|lang-cell|pg-note|prevnext|linklist)\b[\s\S]*?\{/.test(read(p)));
ok("no page re-grew its own copy of the layer's rules", grew.length === 0, grew.slice(0, 4).join(", "));

console.log("\n2. the two bands\n");
const noSupport = members.filter((p) => !read(p).includes('class="pw-support"'));
ok("every page carries the support band", noSupport.length === 0, noSupport.slice(0, 4).join(", "));
const badOrder = members.filter((p) => {
  const h = read(p);
  const band = h.indexOf("ekguru:pw-bands:start");
  const footer = h.indexOf("ekguru:shell-footer:start");
  return band < 0 || footer < 0 || band > footer;
});
ok("the bands sit above the shell footer, inside the page", badOrder.length === 0, badOrder.slice(0, 4).join(", "));
const nextBands = members.filter((p) => read(p).includes('class="pw-next"'));
ok(`most pages got a next step too (${nextBands.length}/${members.length})`,
  nextBands.length > members.length * 0.5);

console.log("\n3. tables\n");
const tablesNeedingNames = members.filter((p) => {
  const h = read(p);
  return /<table[\s\S]*?<th/.test(h) && !h.includes("data-h=");
});
ok("every table with a header row has named cells", tablesNeedingNames.length === 0,
  tablesNeedingNames.slice(0, 4).join(", "));

/* A row whose cell count does not match its header row (a colspan, a summary
   line) cannot be labelled by position; the tool leaves it alone rather than
   inventing a column name. Everything else must be named. */
let cells = 0, labelled = 0;
for (const p of members) {
  for (const t of read(p).matchAll(/<table\b[\s\S]*?<\/table>/g)) {
    if (!/<th[\s>]/.test(t[0])) continue;
    for (const row of t[0].matchAll(/<tr\b[^>]*>[\s\S]*?<\/tr>/g)) {
      if (/<th[\s>]/.test(row[0])) continue;
      cells += (row[0].match(/<td[\s>]/g) || []).length;
      labelled += (row[0].match(/<td[^>]*data-h=/g) || []).length;
    }
  }
}
ok(`cells are named where the column is known (${labelled}/${cells})`,
  cells === 0 || labelled / cells > 0.95);

console.log("\n4. the stylesheet\n");
const css = read("css/experience.css");
const bundle = read("css/style.min.css");
ok("§26 is the page layer", /26\. THE PAGE LAYER/.test(css));
ok("§27 is the print section", /27\. PRINT — the sheet, not the website/.test(css));
for (const sel of [".pw-legacy.art,", ".pw-legacy .hs-card", ".pw-legacy .lang-cell",
                   ".pw-legacy .country-card", ".pw-legacy .pg-note", ".pw-legacy .answer",
                   ".pw-legacy .v-grid", ".pw-legacy .g-concept", ".pw-legacy .sb-counts"]) {
  ok(`the layer styles ${sel}`, css.includes(sel));
}
ok("the layer reaches the bundle", bundle.includes(".pw-legacy .hs-card") && bundle.includes(".pw-legacy .answer"));
const si = css.indexOf("25. THE READING LAYER"), pi = css.indexOf("26. THE PAGE LAYER");
ok("the page layer comes after the reading layer (it overrides the container)",
  si > -1 && pi > si);
const printI = css.indexOf("27. PRINT — the sheet, not the website");
ok("print stays last, so paper is not styled by a page", printI > pi);

console.log("\n5. the v200 pages were left alone\n");
const v200Marked = v200.filter((p) => ON_LAYER.test(read(p)));
ok(`no v200 page was marked (${v200.length} pages checked)`, v200Marked.length === 0,
  v200Marked.slice(0, 4).join(", "));

console.log(`\n${fail ? "FAIL" : "PASS"}  ${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);

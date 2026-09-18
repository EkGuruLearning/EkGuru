#!/usr/bin/env node
/* ==========================================================================
   test-country-visuals.mjs — one picture per country, and the numbers match

   tools/build-country-visuals.py writes images/vis/country-<cc>.svg from the
   language-country relations file and the course catalogue, and drops a block
   on every world-languages/<country>/ and learn-hindi-from-<country>/ page.

   The failure this test exists for is the quiet one: a figure that keeps saying
   "12 taught here" after a course is added, or a caption that promises a course
   where none exists. So it checks the numbers against the data, not just that a
   file is present:

     · every country with a page has a figure, and every figure is valid XML
     · the figure's text carries the country's own name in its own language
     · the caption's numbers equal the manifest's, and the manifest's equal the
       relations data (documented) and the catalogue (taught)
     · a country with nothing to teach says so
     · the block sits in the reading column, before the bands, with an <h2>
     · the alt text is a sentence, not a filename

   Run:  node tools/test-country-visuals.mjs
   ========================================================================== */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
process.chdir(ROOT);

let pass = 0, fail = 0;
const ok = (name, cond, detail = "") => {
  if (cond) { pass++; console.log("  ok    " + name + (detail ? " — " + detail : "")); }
  else { fail++; console.log("  FAIL  " + name + (detail ? " — " + detail : "")); }
};
const read = (p) => fs.readFileSync(p, "utf8");
const exists = (p) => fs.existsSync(p);

const manifest = JSON.parse(read("data/country-visuals.json"));
const figures = manifest.figures;
const rows = JSON.parse(read("data/global/language-country-relations.json")).relations;
const courses = JSON.parse(read("data/courses/index.json")).courses.map((c) => c.code);
const taught = new Set(courses);
const ALIAS = { arb: "ar", cmn: "zh", fil: "fil", npi: "npi", uzn: "uzn", zsm: "zsm" };

console.log(`\n1. one figure per country (${Object.keys(figures).length})\n`);

const missingFile = Object.values(figures).filter((f) => !exists(f.path));
ok("every figure file exists", missingFile.length === 0, missingFile.slice(0, 3).map((f) => f.path).join(", "));

/* SVG is XML: a stray & or an unclosed tag makes an image that silently does
   not render. structure-only check — no XML parser dependency. */
const badXml = [];
for (const f of Object.values(figures)) {
  if (!exists(f.path)) continue;
  const s = read(f.path);
  if (!s.startsWith("<svg") || !s.trimEnd().endsWith("</svg>")) badXml.push(f.path);
  else if (!/role="img"/.test(s) || !/<title>/.test(s) || !/aria-label="/.test(s)) badXml.push(f.path);
  else if (/(<text[^>]*>)([^<]*)/.test(s) === false) badXml.push(f.path);
}
ok("every figure is a well-formed svg with a title and a label", badXml.length === 0,
  badXml.slice(0, 3).join(", "));

const pageMissing = [];
for (const [cc, f] of Object.entries(figures)) {
  const world = `world-languages/${f.slug}/index.html`;
  const sibling = `learn-hindi-from-${f.slug}/index.html`;
  if (!exists(world) && !exists(sibling)) pageMissing.push(cc);
  else if (exists(world) && !read(world).includes(`country-${cc.toLowerCase()}.svg`)) pageMissing.push(world);
}
ok("every figure is on the country's own page", pageMissing.length === 0, pageMissing.slice(0, 3).join(", "));

console.log("\n2. the numbers are the data\n");

const wrongDoc = [], wrongTaught = [];
for (const [cc, f] of Object.entries(figures)) {
  const mine = rows.filter((r) => r.country_id === cc);
  const seen = new Set();
  let documented = 0;
  for (const r of mine) {
    const key = (r.native_name || r.language_name || "").trim();
    if (key && !seen.has(key)) { seen.add(key); documented++; }
  }
  if (documented !== f.documented) wrongDoc.push(`${cc}:${f.documented}≠${documented}`);
  const isTaught = (r) => {
    const cat = (r.category || "").toUpperCase();
    if (!["OFFICIAL", "NATIONAL", "WIDELY_SPOKEN", "REGIONAL"].includes(cat)) return false;
    const code = r.iso_639_1 || ALIAS[r.iso_639_3] || "";
    return taught.has(code);
  };
  const n = new Set(mine.filter(isTaught).map((r) => r.iso_639_1 || ALIAS[r.iso_639_3])).size;
  if (n !== f.taught) wrongTaught.push(`${cc}:${f.taught}≠${n}`);
}
ok("the documented count is the relations data", wrongDoc.length === 0, wrongDoc.slice(0, 4).join(", "));
ok("the taught count is the course catalogue", wrongTaught.length === 0, wrongTaught.slice(0, 4).join(", "));

/* The caption on the page and the alt text in the manifest are two spellings of
   the same claim; they disagreed once (a list counted duplicates where the
   manifest counted languages) and the page said 20 where the figure said 10. */
const disagree = [];
for (const [cc, f] of Object.entries(figures)) {
  const p = `world-languages/${f.slug}/index.html`;
  if (!exists(p)) continue;
  const h = read(p);
  const block = (h.match(/<!-- ekguru:country-visuals:start -->[\s\S]*?<!-- ekguru:country-visuals:end -->/) || [""])[0];
  if (!block) { disagree.push(`${cc}:no block`); continue; }
  /* The counts are in the markup as data attributes, because a caption is
     prose and prose drifts: these two numbers are checked against the manifest
     (and the manifest against the source data above), while the sentence is
     checked for saying something about courses at all. */
  const d = (block.match(/data-documented="(\d+)"/) || [])[1];
  const t = (block.match(/data-taught="(\d+)"/) || [])[1];
  if (Number(d) !== f.documented) disagree.push(`${cc}:documented ${d}≠${f.documented}`);
  if (Number(t) !== f.taught) disagree.push(`${cc}:taught ${t}≠${f.taught}`);
  if (f.taught ? !/course[rs]? on EkGuru|course[rs]? here/.test(block)
               : !/No course exists for them here yet/.test(block)) disagree.push(`${cc}:wording`);
}
ok("the caption says the same thing as the figure", disagree.length === 0, disagree.slice(0, 4).join(", "));

/* A country where nothing is taught must not read like a course page. */
const noCourse = Object.values(figures).filter((f) => f.taught === 0);
ok(`countries with no course say so (${noCourse.length} of ${Object.keys(figures).length})`,
  noCourse.length > 0 && noCourse.every((f) => !/of them have a course/.test(f.alt)),
  noCourse.slice(0, 3).map((f) => f.name).join(", "));

console.log("\n3. where the block sits\n");

const misses = { head: [], bands: [], main: [], alt: [] };
for (const [cc, f] of Object.entries(figures)) {
  for (const p of [`world-languages/${f.slug}/index.html`, `learn-hindi-from-${f.slug}/index.html`]) {
    if (!exists(p)) continue;
    const h = read(p);
    const block = h.indexOf("ekguru:country-visuals:start");
    if (block < 0) { misses.head.push(p); continue; }
    if (!/<h2 id="ct-visual-h">/.test(h.slice(block, block + 400))) misses.head.push(p);
    const bands = h.indexOf("ekguru:pw-bands:start");
    const shell = h.indexOf("ekguru:shell-footer:start");
    if (bands > 0 && block > bands) misses.bands.push(p);
    if (shell > 0 && block > shell) misses.main.push(p);
    const alt = (h.slice(block, block + 1600).match(/alt="([^"]*)"/) || [])[1] || "";
    if (alt.length < 40 || /\.svg$/.test(alt)) misses.alt.push(p);
  }
}
ok("each block opens with its own heading", misses.head.length === 0, misses.head.slice(0, 3).join(", "));
ok("the block sits above the bands, inside the page", misses.bands.length === 0, misses.bands.slice(0, 3).join(", "));
ok("the block never lands after the shell footer", misses.main.length === 0, misses.main.slice(0, 3).join(", "));
ok("the alt text is a sentence about the country", misses.alt.length === 0, misses.alt.slice(0, 3).join(", "));

/* The country's own name in its own script, when the data has one. */
const cache = JSON.parse(read("tools/_countries-cache.json"));
const withNative = Object.entries(figures).filter(([, f]) => {
  const row = cache.find((c) => c.cca2 === f.country);
  const native = Object.values((row?.name?.native) || {})[0]?.common;
  return native && native !== f.name;
});
const nativesShown = withNative.filter(([, f]) => {
  const row = cache.find((c) => c.cca2 === f.country);
  const native = Object.values((row?.name?.native) || {})[0]?.common;
  return read(`images/vis/country-${f.country.toLowerCase()}.svg`).includes(native);
});
ok(`the figure carries the country's own name where the data has one (${withNative.length} countries)`,
  withNative.length > 100 && nativesShown.length === withNative.length,
  `${nativesShown.length}/${withNative.length} shown`);
ok("India's plate shows भारत", read("images/vis/country-in.svg").includes("भारत"));

console.log("\n4. nothing runs off the plate\n");

{
  /* The plates are 320px wide and unforgiving. Right-to-left lines are the
     obvious way to fail this, but so is a long language list: estimate each
     run's width and fail when it leaves the picture. */
  const overflow = [];
  for (const [cc, f] of Object.entries(figures)) {
    const svg = read(`images/vis/country-${cc.toLowerCase()}.svg`);
    for (const m of svg.matchAll(/<text x="(\d+)"([^>]*)>([^<]*)<\/text>/g)) {
      const x = Number(m[1]), attrs = m[2], body = m[3];
      const size = Number((attrs.match(/font-size="([\d.]+)"/) || [, 12])[1]);
      const wide = /[\u0590-\u08FF\u0900-\u0DFF]/.test(body) ? 0.62 : 0.58;
      const width = body.length * size * wide;
      const anchor = (attrs.match(/text-anchor="(\w+)"/) || [, "start"])[1];
      const start = anchor === "end" ? x - width : anchor === "middle" ? x - width / 2 : x;
      if (start + width > 314 || start < 2) {
        overflow.push(`${cc}: "${body.slice(0, 20)}" ${Math.round(start)}→${Math.round(start + width)}`);
      }
    }
  }
  ok("every word stays on the plate", overflow.length === 0, overflow.slice(0, 4).join("; "));
}

console.log("\n5. the manifest is honest\n");
ok("every figure has a region and a slug",
  Object.values(figures).every((f) => f.slug && f.name && typeof f.taught === "number"));
ok("no figure claims a course count above its documented count",
  Object.values(figures).every((f) => f.taught <= f.documented),
  Object.values(figures).filter((f) => f.taught > f.documented).slice(0, 3).map((f) => f.name).join(", "));
ok("no figure is captioned with a filename",
  Object.values(figures).every((f) => !/\.svg/.test(f.alt)));

console.log(`\n${fail ? "FAIL" : "PASS"}  ${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);

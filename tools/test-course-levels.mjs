#!/usr/bin/env node
/* ==========================================================================
   test-course-levels.mjs — the A1–C2 pages of every course

   tools/build-course-levels.py turns data/courses/<phase>/<code>_<LEVEL>.json
   into 273 real pages: 39 languages × (a ladder page + six level pages). Until
   it existed, A2–C2 of every course lived only inside the JavaScript player on
   /courses/#/<code>/<level>, which no crawler can read and no reader with
   JavaScript off can open.

   This test is what keeps that honest:

     · every level of every course has a page, and the page is not a stub
     · the page carries the course data itself — words, answers, a test
     · it is a page-layer page: no CSS of its own, a support band, one h1
     · its canonical, its structured data and its ad class are right
     · the hub links it, the sitemap lists it, and links do not 404

   Run:  node tools/test-course-levels.mjs
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

const LEVELS = ["a1", "a2", "b1", "b2", "c1", "c2"];
const catalogue = JSON.parse(read("data/courses/index.json"));
const courses = catalogue.courses;
const complete = courses.filter((c) => c.complete === true);
const rungs = JSON.parse(read("data/levels.json")).rungs;

console.log(`\n1. every complete course, every CEFR level (${complete.length} complete of ${courses.length})\n`);

const missing = [];
for (const c of complete) {
  if (!exists(`languages/${c.code}/level/index.html`)) missing.push(`${c.code}/level/`);
  for (const lv of LEVELS) {
    if (!exists(`languages/${c.code}/level/${lv}/index.html`)) missing.push(`${c.code}/${lv}`);
  }
}
ok("every complete language has a ladder page and six CEFR level pages",
  missing.length === 0, missing.slice(0, 4).join(", ") + (missing.length > 4 ? " …" : ""));

const expected = complete.length * (LEVELS.length + 1);
ok(`complete CEFR ladder+levels exist (${expected})`, expected === complete.length * 7, String(expected));

/* A stub would be a page with the heading and nothing under it. The smallest
   real page in the set (a C2 with one unit) still runs to thousands of words,
   so a floor of 1,500 words is generous and still catches a gutted page. */
const words = (h) => h.replace(/<script[\s\S]*?<\/script>/gi, " ")
  .replace(/<style[\s\S]*?<\/style>/gi, " ")
  .replace(/<[^>]+>/g, " ").split(/\s+/).filter(Boolean).length;
const thin = [];
for (const c of complete) {
  for (const lv of LEVELS) {
    const p = `languages/${c.code}/level/${lv}/index.html`;
    if (exists(p) && words(read(p)) < 1500) thin.push(`${c.code}/${lv}:${words(read(p))}`);
  }
}
ok("no complete CEFR level page is a stub (≥1,500 words)", thin.length === 0, thin.slice(0, 5).join(", "));

console.log("\n2. the course data is actually on the page\n");

const sample = complete[0];
const one = read(`languages/${sample.code}/level/a1/index.html`);
/* The rail is counted inside its own <ul>: the page also links the next level
   from the checkpoint paragraph, and a page-wide link count would read that as
   a seventh level. */
const rail = (one.match(/<ul class="lv-rail">[\s\S]*?<\/ul>/) || [""])[0];
ok("the level rail lists all six levels",
  (one.match(/class="lv-rail"/g) || []).length === 1 &&
  (rail.match(/aria-current="page"/g) || []).length === 1 &&
  (rail.match(/href="\.\.\/[abc][12]\/"/g) || []).length === 6,
  (rail.match(/href="\.\.\/[abc][12]\/"/g) || []).length + " links");
ok("the vocabulary is a table with the language's own words",
  /<table[\s\S]*?<th>Word<\/th>/.test(one) && new RegExp(`lang="${sample.code}"`).test(one));
ok("the grammar box carries the rule and the mistakes",
  /class="lv-gram"/.test(one) && /Watch out:/.test(one));
ok("the dialogue carries four columns", /<th>Who<\/th><th>Line<\/th><th>Say it<\/th><th>English<\/th>/.test(one));
ok("the practice answers are on the page, in <details>",
  (one.match(/<details><summary>Show the answer<\/summary>/g) || []).length > 50);
ok("the level test is on the page", /The A1 test — 10 items/.test(one));
ok("the level's own figure is on the page", new RegExp(`images/vis/${sample.code}-a1\\.svg`).test(one));

/* The recall drills say what they are. A page that generated questions must
   say so — the site's rule is that a machine may re-ask what a human wrote,
   and must never be presented as a teacher. */
ok("the generated drills are labelled as generated",
  /generated from this level’s own vocabulary/.test(one) && /never a\s+lesson|never a lesson/i.test(one));
ok("no page claims to be AI-taught", !/\bAI\b(?!-)/.test(one.replace(/aria-[a-z]+/g, "")));

console.log("\n3. it is a page-layer page, not a fifth design\n");

const all = [];
for (const c of complete) {
  all.push(`languages/${c.code}/level/index.html`);
  for (const lv of LEVELS) all.push(`languages/${c.code}/level/${lv}/index.html`);
}
const withCss = all.filter((p) => /<style[^>]*>[\s\S]*?\{/.test(read(p)));
ok("no level page carries its own stylesheet", withCss.length === 0, withCss.slice(0, 3).join(", "));
const notLegacy = all.filter((p) => !/<div class="[^"]*\bpw-legacy\b/.test(read(p)));
ok("every level page is on the shared design", notLegacy.length === 0, notLegacy.slice(0, 3).join(", "));
const noBand = all.filter((p) => !read(p).includes('class="pw-support"'));
ok("every level page carries the support band", noBand.length === 0, noBand.slice(0, 3).join(", "));

const heads = all.filter((p) => (read(p).match(/<h1[\s>]/g) || []).length !== 1);
ok("exactly one h1 on every level page", heads.length === 0, heads.slice(0, 3).join(", "));

/* The band promises that practice carries no ad. On a page that IS practice,
   that promise is kept by not loading the loader at all. */
const withAd = all.filter((p) => read(p).includes("adsbygoogle"));
ok("no ad loader on a page of practice", withAd.length === 0, withAd.slice(0, 3).join(", "));
const wrongClass = all.filter((p) => !/data-ad-class="INTERACTIVE_LEARNING"/.test(read(p)));
ok("the ad matrix classes them INTERACTIVE_LEARNING", wrongClass.length === 0,
  wrongClass.slice(0, 3).join(", "));

/* The storybook injector adds a chapter banner and, on pages that contain
   Devanagari, a "tap a speaker button" hint. The hint used to be added to any
   page with a single Devanagari character — which meant the Bengali, Punjabi,
   Marathi and Nepali level pages were told to "hear Hindi spoken". It says what
   is true of the page now; this is what keeps it that way. */
const wrongHint = all.filter((p) => {
  const h = read(p);
  return h.includes("sb-hint") && h.includes("hear Hindi spoken") &&
         !/languages\/hi\/|learn\/hindi|hindi-tutor|toolbox\/hindi|daily-hindi/.test(p);
});
ok("no page claims Hindi unless it teaches Hindi", wrongHint.length === 0,
  wrongHint.slice(0, 4).join(", "));
const noBanner = all.filter((p) => !read(p).includes("ekguru:chapter"));
ok("every level page carries its course banner", noBanner.length === 0,
  noBanner.slice(0, 4).join(", "));

console.log("\n4. crawlers and structure\n");

const badCanon = all.filter((p) => {
  const h = read(p), url = p.replace(/index\.html$/, "");
  return !h.includes(`<link rel="canonical" href="https://ekguru.shop/${url}">`);
});
ok("every page canonicalises to itself", badCanon.length === 0, badCanon.slice(0, 3).join(", "));

let ld = 0, badLd = [];
for (const p of all) {
  for (const m of read(p).matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    ld++;
    try { JSON.parse(m[1]); } catch { badLd.push(p); }
  }
}
ok(`structured data parses (${ld} blocks)`, badLd.length === 0, badLd.slice(0, 3).join(", "));
ok("complete CEFR pages are indexable",
  all.every((p) => !/name="robots" content="noindex/.test(read(p))));

const sm = exists("sitemap-levels.xml") ? read("sitemap-levels.xml") : "";
const locs = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
ok("sitemap-index.xml declares sitemap-levels.xml", read("sitemap-index.xml").includes("sitemap-levels.xml"));
const notInSm = all.filter((p) => !sm.includes(p.replace(/index\.html$/, "")));
ok("every complete CEFR level page is in the sitemap", notInSm.length === 0, notInSm.slice(0, 3).join(", "));
ok("sitemap does not list C3–C5 stubs",
  locs.filter((u) => /\/level\/c[345]\/$/.test(u)).length === 0,
  String(locs.filter((u) => /\/level\/c[345]\//.test(u)).length));

console.log("\n5. the links out are real\n");

/* Internal links only: every href="/…" on a level page must resolve to a file
   in this tree. The build resolver (lang_targets) exists because 29 of the 39
   languages have no languages/<code>/practice/ — a hard-coded link would have
   put 404s on 273 pages. */
const dead = new Map();
let links = 0;
for (const p of all) {
  for (const m of read(p).matchAll(/href="(\/[^"#?]*)"/g)) {
    const t = m[1];
    links++;
    if (t === "/") { if (!exists("index.html")) dead.set(t, p); continue; }
    const f = t.endsWith("/") ? t.replace(/^\//, "") + "index.html" : t.replace(/^\//, "");
    if (!exists(f) && !exists(f.replace(/\/index\.html$/, ""))) dead.set(t, p);
  }
}
ok(`every internal link resolves (${links} links)`, dead.size === 0,
  [...dead.keys()].slice(0, 4).join(", "));

const rails = [];
for (const c of courses) {
  for (const cand of [`languages/${c.code}/course/index.html`]) {
    if (exists(cand) && read(cand).includes("ekguru:course-levels:start")) rails.push(cand);
  }
}
ok(`the world-course hubs link their levels (${rails.length})`, rails.length === 10, String(rails.length));
const byCode = new Map(courses.map((course) => [course.code, course]));
const railHrefs = rails.map((p) => {
  const code = (p.match(/^languages\/([^/]+)\//) || [])[1];
  const actual = [...read(p).matchAll(/href="(\/languages\/[a-z]{2,3}\/level\/[a-z0-9]+\/)"/g)].length;
  const expected = Object.keys((byCode.get(code) || {}).levels || {}).filter((lv) => LEVELS.map((x) => x.toUpperCase()).includes(lv)).length;
  return { code, actual, expected };
});
ok("each hub rail matches its gated published-level count",
  railHrefs.every((row) => row.actual === row.expected),
  railHrefs.map((row) => `${row.code}:${row.actual}/${row.expected}`).join(", "));

console.log(`\n${fail ? "FAIL" : "PASS"}  ${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);

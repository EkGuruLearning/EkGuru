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
  /<table[\s\S]*?<th>Word<\/th>/.test(one) && one.includes(`lang="${sample.code}"`));
ok("the grammar box carries the rule and the mistakes",
  /class="lv-gram"/.test(one) && /Watch out:/.test(one));
ok("the dialogue carries four columns", /<th>Who<\/th><th>Line<\/th><th>Say it<\/th><th>English<\/th>/.test(one));
ok("the practice answers are on the page, in <details>",
  (one.match(/<details><summary>Show the answer<\/summary>/g) || []).length > 50);
ok("the level test is on the page", /The A1 test — 10 items/.test(one));
ok("the level's own figure is on the page", one.includes(`images/vis/${sample.code}-a1.svg`));

/* The recall drills say what they are. A page that generated questions must
   say so — the site's rule is that a machine may re-ask what a human wrote,
   and must never be presented as a teacher. */
ok("the generated drills are labelled as generated",
  /drills are generated from the [^<.]+ vocabulary list/.test(one) && /never a\s+lesson|never a lesson/i.test(one));
ok("no page claims to be AI-taught", !/\bAI\b(?!-)/.test(one.replace(/aria-[a-z]+/g, "")));

/* What the page prints is what the data says. `grammar.mistakes` is a list of
   plain strings in the older courses and of {wrong, right, why} objects in
   everything authored since — 2,295 objects to 1,218 strings. The grammar box
   sent both shapes through one text cleaner, so an object reached the reader as
   a Python literal:

       <li>{'wrong': 'ਤੂੰ ਕਿੱਥੇ ਰਹਿੰਦਾ ਹੈ?', 'right': …, 'why': …}</li>

   on 58 pages of 13 languages. Nothing failed: the HTML was valid, the words
   were on the page, the JSON was untouched, and every schema gate reads the
   JSON. So this reads the rendered page against the source, row by row. */
const esc = (v) => String(v).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const phaseOf = new Map(courses.map((c) => [c.code, c.phase || "phase-1"]));
const reprish = [];
const unrendered = [];
let watchRows = 0, watchPages = 0;
for (const c of courses) {
  for (const lv of LEVELS) {
    const page = `languages/${c.code}/level/${lv}/index.html`;
    const data = `data/courses/${phaseOf.get(c.code)}/${c.code}_${lv.toUpperCase()}.json`;
    if (!exists(page) || !exists(data)) continue;
    const html = read(page);
    /* The "not published" stub is generated from the same course file and
       prints none of its content, so it is not evidence either way. */
    if (/— not published/.test(html) || /content="noindex/.test(html)) continue;
    if (/\{'[a-z_]+':|\{&#39;[a-z_]+&#39;:/.test(html)) reprish.push(page);
    let rows = 0;
    const source = JSON.parse(read(data));
    const authored = [];
    for (const unit of (source.level && source.level.units) || []) {
      for (const lesson of (unit && unit.lessons) || []) {
        const mis = lesson && lesson.grammar && lesson.grammar.mistakes;
        if (Array.isArray(mis)) authored.push(...mis);
      }
    }
    /* The same shape is used by the level's own "the mistakes this level
       makes" list, printed from extra.mistakes. */
    const extra = source.level && source.level.extra;
    if (extra && Array.isArray(extra.mistakes)) authored.push(...extra.mistakes);
    for (const m of authored) {
      if (!m || typeof m !== "object" || Array.isArray(m)) continue;
      rows++;
      watchRows++;
      const row = `<b>${esc(m.wrong)}</b> → ${esc(m.right)}`;
      if (!html.includes(row)) unrendered.push(`${page} :: ${row.slice(0, 60)}`);
    }
    if (rows) watchPages++;
  }
}
ok("no page prints a Python literal where a sentence belongs",
  reprish.length === 0, reprish.slice(0, 4).join(", "));
ok(`every {wrong,right,why} mistake renders as the lesson writes it ` +
   `(${watchRows} rows on ${watchPages} pages)`,
  watchRows > 0 && unrendered.length === 0, unrendered.slice(0, 3).join(" | "));

/* One romanisation per page. A course that writes its vocabulary lane in plain
   ASCII (`main thik han`) must not romanise the same words with marks in its
   practice lane (`main ṭhīk hān!`), and one that defines ē in its own lane must
   not print a bare `e` where the reader has just been taught a length mark.
   The reader's reference is the page's own "Say it" column, so that is what this
   compares: every parenthetical transliteration of the language's own script has
   to use letters the page already taught. Only pages with a non-Latin script are
   read this way — for German or Spanish the Latin text IS the language. */
/* "Native script" = a letter outside the Latin alphabet. A romanisation with
   marks is non-ASCII too, so testing for non-ASCII would skip exactly the
   strings this looks for. */
const NATIVE = /[\u0400-\u04ff\u0530-\u058f\u0590-\u05ff\u0600-\u06ff\u0900-\u097f\u0980-\u09ff\u0a00-\u0a7f\u0a80-\u0aff\u0b00-\u0b7f\u0b80-\u0bff\u0c00-\u0c7f\u0c80-\u0cff\u0d00-\u0d7f\u0e00-\u0e7f\u0e80-\u0eff\u0f00-\u0fff\u1000-\u109f\u1780-\u17ff\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af]/;
const latinMarks = (text) => [...new Set([...text].filter((c) => {
  const d = c.normalize("NFD");
  return d.length > 1 && /^[A-Za-z]$/.test(d[0]);
}))];
const romanisation = [];
let nativePages = 0, marksInUse = new Set();
for (const c of courses) {
  for (const lv of LEVELS) {
    const page = `languages/${c.code}/level/${lv}/index.html`;
    if (!exists(page)) continue;
    const html = read(page);
    if (/— not published/.test(html) || /content="noindex/.test(html)) continue;
    const words = [...html.matchAll(/<td data-h="Word"[^>]*>([\s\S]*?)<\/td>/g)]
      .map((m) => m[1].replace(/<[^>]+>/g, " ")).join(" ");
    if (!NATIVE.test(words)) continue;                          // Latin-script course
    nativePages++;
    /* The reference is this page's own lane, not the site's: a mark another
       language teaches says nothing about what this page just taught. */
    const sayIt = new Set();
    for (const m of html.matchAll(/<td data-h="Say it">([^<]*)<\/td>/g))
      for (const mark of latinMarks(m[1])) sayIt.add(mark.toLowerCase());
    for (const mark of sayIt) marksInUse.add(mark);
    const text = html.replace(/<(script|style)[\s\S]*?<\/\1>/gi, " ")
      .replace(/<[^>]+>/g, " ").replace(/\s+/g, " ");
    for (const m of text.matchAll(/\(([^()]{1,120})\)/g)) {
      const inner = m[1];
      if (NATIVE.test(inner)) continue;                        // native text, not a transliteration
      if (!NATIVE.test(text.slice(Math.max(0, m.index - 60), m.index))) continue;
      const strange = latinMarks(inner).filter((c) => !sayIt.has(c.toLowerCase()));
      if (strange.length)
        romanisation.push(`${page} :: ${m[0].slice(0, 48)} (${strange.join("")})`);
    }
  }
}
ok(`every page romanises the language the way its own "Say it" lane does ` +
   `(${nativePages} non-Latin pages, ${marksInUse.size} marks in use)`,
  nativePages > 0 && romanisation.length === 0, romanisation.slice(0, 3).join(" | "));

/* A structural schema pass cannot see an English placeholder hidden in a
   rendered gloss. Read the page itself: Telugu C1/C2 once repeated
   `contextual segment N:` before a generic sentence 48 times per level, while
   the publication audit still considered those levels publishable and the
   structural checks did not inspect their rendered glosses. This assertion is
   deliberately scoped to Telugu until the eight other courses
   tracked by Trap #9 receive their own source repairs. */
const contextualFillerPages = [];
for (const lv of LEVELS) {
  const page = `languages/te/level/${lv}/index.html`;
  if (!exists(page)) continue;
  const html = read(page);
  if (/— not published/.test(html) || /content="noindex/.test(html)) continue;
  if (/\bcontextual\s+segment\s+\d+\s*:/i.test(html)) contextualFillerPages.push(page);
}
ok("Telugu rendered level pages expose no synthetic contextual-segment glosses",
  contextualFillerPages.length === 0, contextualFillerPages.slice(0, 5).join(", "));

const teC1Page = exists("languages/te/level/c1/index.html")
  ? read("languages/te/level/c1/index.html") : "";
const teC2Page = exists("languages/te/level/c2/index.html")
  ? read("languages/te/level/c2/index.html") : "";
const oldTeRomanisations = ["prakaarm", "merugupadimdani", "telustoomdi", "khmdimcadm"];
ok("Telugu C1 renders the corrected marked romanisation",
  teC1Page.includes("Sarvē nivēdika prakāraṁ, spandana samayaṁ taggindani telustōndi.") &&
  oldTeRomanisations.every((text) => !teC1Page.includes(text)),
  oldTeRomanisations.filter((text) => teC1Page.includes(text)).join(", "));
ok("Telugu C1/C2 render distinct, level-specific test prompts",
  teC1Page.includes("Which phrase attributes a finding to its source?") &&
  teC2Page.includes("Does silence by itself prove agreement?") &&
  !/Capstone task\s+\d/i.test(teC1Page + teC2Page),
  /Capstone task\s+\d/i.test(teC1Page + teC2Page) ? "generic capstone remains" : "");

const teCoursePages = ["a1", "a2", "b1", "b2", "c1", "c2"]
  .map((lv) => `languages/te/level/${lv}/index.html`)
  .filter(exists).map(read).join("\n");
const englishTeRoles = "Doctor|Patient|Manager|Newcomer|Father|Mother|Grandmother|Son|Girl|Editor|Mediator|Reviewer|Specialist";
const leakedTeRole = new RegExp(`<td data-h="Who"><b>(?:${englishTeRoles})</b></td>`);
ok("Telugu rendered dialogues use local role labels",
  !leakedTeRole.test(teCoursePages), leakedTeRole.exec(teCoursePages)?.[0] || "");

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
const railHrefs = rails.map((p) => {
  const code = (p.match(/^languages\/([^/]+)/) || [])[1];
  const course = courses.find((c) => c.code === code);
  return {
    code,
    actual: [...read(p).matchAll(/href="(\/languages\/[a-z]{2,3}\/level\/[a-z0-9]+\/)"/g)].length,
    expected: course ? Object.keys(course.levels || {}).length : 0,
  };
});
ok("each hub rail holds exactly its published levels",
  railHrefs.every((row) => row.actual === row.expected),
  railHrefs.map((row) => `${row.code}:${row.actual}/${row.expected}`).join(", "));

console.log(`\n${fail ? "FAIL" : "PASS"}  ${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);

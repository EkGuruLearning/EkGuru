#!/usr/bin/env node
/* Fail if manufactured extra-level tokens reappear, and if incomplete
   extra levels are indexable or listed in sitemap-levels.xml. */
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

const PLACEHOLDER = [
  /[a-z]{2,3}_word_\d+_\d+/i,
  /roman_\d+(_\d+)?/i,
  /related word \d+/i,
  /Example \d+ in /i,
  /Dialogue line \d+/i,
  /Practice question \d+ about /i,
  /Test question \d+ for /i,
];

function walk(dir, acc = []) {
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) walk(p, acc);
    else if (ent.name.endsWith(".json") && ent.name !== "index.json") acc.push(p);
  }
  return acc;
}

const files = walk("data/courses").filter((p) => !p.includes(`${path.sep}authored${path.sep}`));
const hits = [];
for (const f of files) {
  const t = fs.readFileSync(f, "utf8");
  for (const rx of PLACEHOLDER) {
    if (rx.test(t)) { hits.push(f); break; }
  }
}
ok("no placeholder tokens in course JSON", hits.length === 0, hits.slice(0, 8).join(", "));

const catalogue = JSON.parse(fs.readFileSync("data/courses/index.json", "utf8"));
const extras = ["A3", "B3", "C3", "C4", "C5"];
let indexedStub = 0, realExtra = 0;
for (const c of catalogue.courses) {
  for (const lv of extras) {
    const f = `data/courses/${c.phase}/${c.code}_${lv}.json`;
    if (!fs.existsSync(f)) continue;
    const j = JSON.parse(fs.readFileSync(f, "utf8"));
    if (j.content_status === "REAL") realExtra++;
    if (j.content_status === "INCOMPLETE" && j.indexable === true) indexedStub++;
  }
}
ok("incomplete extra levels are not indexable", indexedStub === 0, String(indexedStub));
ok("at least one authored extra level exists", realExtra > 0, String(realExtra));

const gen = fs.readFileSync("tools/generate-extended-courses.py", "utf8");
ok("placeholder generator refuses to write",
  /Refusing to generate placeholder/.test(gen) && !/hi_word_1_1/.test(gen));

const sm = fs.existsSync("sitemap-levels.xml") ? fs.readFileSync("sitemap-levels.xml", "utf8") : "";
const c3 = [...sm.matchAll(/\/level\/c[345]\//g)];
ok("sitemap-levels.xml has no C3–C5 URLs", c3.length === 0, String(c3.length));

const robots = fs.readFileSync("robots.txt", "utf8");
const sitemapIndex = fs.readFileSync("sitemap-index.xml", "utf8");
ok("robots.txt declares the sitemap index and the index declares level URLs",
  /sitemap-index\.xml/.test(robots) && /sitemap-levels\.xml/.test(sitemapIndex));

const mon = fs.readFileSync("js/monetization.js", "utf8");
ok("ads require advertising === true", /consent\.advertising === true/.test(mon));

console.log(`\n${fail ? "FAIL" : "PASS"}  ${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);

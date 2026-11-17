#!/usr/bin/env node
/* ============================================================
   ORPHAN TUTOR PAGE QUARANTINE (17 Nov 2026)
   ============================================================
   A sheet-only guru (approved=yes, no js/tutors/<id>.js file) gets a
   real profile page from tools/build-tutor-pages.js. When the owner later
   sets active=no, tools/sheetsync.js drops the record from the bake, so
   the id leaves the roster — and nothing owned that page any more: it
   stayed indexable, with price and booking, until this round.

   tools/quarantine-tutor-drafts.py now treats every tutor/<id>/index.html
   whose id is not in the roster (no file, not baked) as an orphan and
   rewrites it as the noindex "profile not published" stub. This test
   plants such an orphan (a copy of a public profile under a throwaway
   id), proves --check flags it, write mode neutralises it, the result is
   idempotent, and no real page changed. The throwaway directory is
   removed in a finally block.

   Run:  node tools/test-orphan-tutor-quarantine.mjs
   ============================================================ */
"use strict";
import { readFileSync, writeFileSync, mkdirSync, rmSync, existsSync, readdirSync } from "fs";
import { spawnSync } from "child_process";
import { join } from "path";

const ROOT = new URL(import.meta.url).pathname.replace(/\/tools\/[^/]+$/, "");
let passed = 0, failed = 0;
function check(name, cond, detail) {
  if (cond) { passed++; console.log("  ok    " + name); }
  else { failed++; console.log("  FAIL  " + name + (detail ? "  — " + detail : "")); }
}
function quarantine(...args) {
  const r = spawnSync("python3", ["tools/quarantine-tutor-drafts.py", ...args], { cwd: ROOT, encoding: "utf8" });
  return { code: r.status, out: (r.stdout || "") + (r.stderr || "") };
}

const SLUG = "zz-test-gone-guru";
const DIR = join(ROOT, "tutor", SLUG);
const PAGE = join(DIR, "index.html");

/* a real public profile as the donor — the orphan must look exactly like a
   page the generator wrote for a guru who was public yesterday */
const donorId = readdirSync(join(ROOT, "tutor")).find((d) => {
  const f = join(ROOT, "tutor", d, "index.html");
  return existsSync(f) && /name="robots" content="index/.test(readFileSync(f, "utf8"));
});
const donorFile = join(ROOT, "tutor", donorId, "index.html");
const donor = readFileSync(donorFile, "utf8");
const donorName = /<title>(.*?)\s+—/.exec(donor)[1];

/* every real tutor page is snapshotted so the test can prove it touched none */
const realPages = {};
for (const d of readdirSync(join(ROOT, "tutor"))) {
  const f = join(ROOT, "tutor", d, "index.html");
  if (existsSync(f)) realPages[f] = readFileSync(f, "utf8");
}

try {
  console.log("plant an orphan profile (copy of " + donorId + " as " + SLUG + ")");
  const planted = donor.split(donorName).join("Test Gone Guru").split(donorId).join(SLUG);
  mkdirSync(DIR, { recursive: true });
  writeFileSync(PAGE, planted);
  check("planted page is indexable with a real profile body", /name="robots" content="index/.test(planted) && /Book|book/.test(planted));

  console.log("quarantine --check");
  const c1 = quarantine("--check");
  check("--check exits 1 while the orphan is live", c1.code === 1, "exit " + c1.code);
  check("--check names the orphan", c1.out.includes(SLUG), c1.out.trim().split("\n").slice(-2).join(" | "));

  console.log("quarantine (write)");
  const w = quarantine();
  check("write mode exits 0", w.code === 0, w.out);
  const after = readFileSync(PAGE, "utf8");
  check("orphan is noindex", /<meta name="robots" content="noindex, follow">/.test(after));
  check("title says the profile is not published, keeping the name", /<title>Test Gone Guru — tutor profile not published \| EkGuru<\/title>/.test(after));
  check("no booking / price surface left", !/class="[^"]*\bbtn[^"]*"[^>]*>\s*Book/i.test(after) && !/data-eg-book|\$\s?\d+\s*(per|\/)\s*(lesson|50)/i.test(after));
  check("the old profile body is gone", !after.includes("pr-hero") || !/Lessons taught|Trial lesson/.test(after));
  check("Person JSON-LD replaced by a WebPage schema", !/"@type":\s*"Person"/.test(after) && /"@type":"WebPage"/.test(after));
  check("page is ad-class RESEARCH_REQUIRED", /data-ad-class="RESEARCH_REQUIRED"/.test(after));

  console.log("idempotent");
  const c2 = quarantine("--check");
  check("--check exits 0 after the rewrite", c2.code === 0, c2.out);
  const w2 = quarantine();
  check("a second write is byte-stable", readFileSync(PAGE, "utf8") === after && w2.code === 0);

  console.log("nothing else touched");
  const changed = Object.keys(realPages).filter((f) => readFileSync(f, "utf8") !== realPages[f]);
  check("every real tutor page is byte-identical", changed.length === 0, changed.join(", "));
} catch (e) {
  failed++;
  console.log("  FAIL  " + (e && e.stack || e));
} finally {
  rmSync(DIR, { recursive: true, force: true });
  check("throwaway directory removed", !existsSync(DIR));
}

console.log("\n" + (failed ? "FAIL" : "PASS") + "  " + passed + " passed, " + failed + " failed");
process.exit(failed ? 1 : 0);

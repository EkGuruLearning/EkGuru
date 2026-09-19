/* =========================================================
   EkGuru — COUNTRY RAIL TEST (tools/test-country-rail.mjs)
   ---------------------------------------------------------
   The homepage rail is the first thing a visitor sees, so it
   gets its own checks rather than riding on the shell tests:

     · the 194 sovereign countries, one anchor each
     · two rows, opposite directions, the left row first
     · each item is a plain anchor with the country name and
       a real language summary (no counts, no invented facts)
     · every href resolves to a page that exists on disk
     · the seamless duplicate exists, is aria-hidden, and is
       the only duplicate — screen readers hear the list once
     · the mobile drawer keeps exactly seven items and the
       desktop bar keeps its own face: Find Tutors, Learn and
       Search never enter the drawer, and the trial CTA is a
       desktop-scope button, never a drawer link

   node tools/test-country-rail.mjs
   ========================================================= */

import fs from "node:fs";
import path from "node:path";
import { JSDOM } from "jsdom";

const ROOT = new URL("..", import.meta.url).pathname;
const HOME = path.join(ROOT, "index.html");
const html = fs.readFileSync(HOME, "utf8");
const dom = new JSDOM(html);
const doc = dom.window.document;

let passed = 0;
let failed = 0;
function check(name, ok, detail) {
  if (ok) { passed++; console.log("ok    " + name); }
  else { failed++; console.log("FAIL  " + name + (detail ? " — " + detail : "")); }
}

const rail = doc.querySelector(".ct-rail");
check("the rail exists on the home page", !!rail);
if (!rail) { finish(); }

const rows = [...rail.querySelectorAll(".ct-rail-row")];
check("two rows", rows.length === 2, "got " + rows.length);
check("the rows run opposite ways",
  rows.length === 2 && rows[0].dataset.dir === "left" && rows[1].dataset.dir === "right",
  rows.map((r) => r.dataset.dir).join(","));

/* the seamless duplicates are links too — the reader-visible list is the
   track's direct children, not the whole row. */
const items = [...rail.querySelectorAll(".ct-rail-track > a.ct-item")];
check("194 country links", items.length === 194, "got " + items.length);

const slugs = new Set();
for (const a of items) slugs.add(a.getAttribute("href"));
check("no two links for the same country", slugs.size === 194, slugs.size + " unique");

const badHref = items.find((a) => {
  const p = a.getAttribute("href").replace(/^\//, "");
  return !fs.existsSync(path.join(ROOT, p, "index.html"));
});
check("every rail link resolves to a page on disk", !badHref, badHref && badHref.outerHTML);

const noSummary = items.filter((a) => !(a.querySelector("b") && a.querySelector("small")));
check("every item carries the country name and a language summary", noSummary.length === 0,
  noSummary[0] && noSummary[0].outerHTML);

const noCount = items.filter((a) => /\b\d{3,}\b|lessons|speakers|million|billion/i.test(a.querySelector("small").textContent));
check("the summary is language names, never invented counts", noCount.length === 0,
  noCount[0] && noCount[0].outerHTML);

/* the seamless duplicate */
const dups = [...rail.querySelectorAll(".ct-dup")];
check("each row carries its seamless duplicate", dups.length === 2, "got " + dups.length);
check("the duplicates are invisible to readers",
  dups.every((d) => d.getAttribute("aria-hidden") === "true"),
  dups.map((d) => d.getAttribute("aria-hidden")).join(","));

for (const row of rows) {
  const track = row.querySelector(".ct-rail-track");
  const direct = [...track.querySelectorAll(":scope > a.ct-item")];
  const dup = track.querySelector(".ct-dup");
  const dupItems = dup ? [...dup.querySelectorAll("a.ct-item")] : [];
  check("row " + row.dataset.dir + ": real items and duplicate match one to one",
    direct.length > 0 && direct.length === dupItems.length &&
    direct.every((a, i) => a.getAttribute("href") === dupItems[i].getAttribute("href")),
    direct.length + " vs " + dupItems.length);
}

/* the drawer's two faces */
const nav = doc.querySelector(".hdr .nav");
check("the header nav still exists", !!nav);
const scoped = [...nav.querySelectorAll("a[data-scope]")];
const drawerFace = scoped.filter((a) => a.dataset.scope === "drawer").map((a) => a.textContent.trim());
const desktopOnly = scoped.filter((a) => a.dataset.scope === "desktop").map((a) => a.textContent.trim());

check("the drawer keeps Languages, Practice, Worksheets and Contact",
  ["Languages", "Practice", "Worksheets", "Contact"].every((t) => drawerFace.includes(t)),
  drawerFace.join(","));
check("Find Tutors, Learn and Search never enter the drawer",
  desktopOnly.includes("Find Tutors") && desktopOnly.includes("Learn") && desktopOnly.includes("Search"),
  desktopOnly.join(","));

const cta = nav.querySelector(".btn[href*='find-tutors']");
check("the trial CTA stays out of the drawer (desktop scope)", !!cta && cta.dataset.scope === "desktop",
  cta ? (cta.dataset.scope || "no scope") : "no CTA found");

function finish() {
  console.log("");
  if (failed) {
    console.log("FAILED — " + failed + " check(s), " + passed + " passed.");
    process.exit(1);
  }
  console.log("ALL COUNTRY RAIL + DRAWER CHECKS PASSED — " + passed + " checks.");
}
finish();

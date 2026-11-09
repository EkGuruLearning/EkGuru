#!/usr/bin/env node
/* Tutor regression tests for the Nov 2026 tutor-bug pass:
     1. profile renders exactly ONE <main> (no nested landmark)
     2. empty Experience / Method / Speaks blocks are omitted
     3. a tutor with no weekly slots shows an honest note, not 7 dashes
     4. booking validate() must not demand a slot from such a tutor
        (their booking form was a dead end that could never send)
     5. no public tutor file claims a rating with zero reviews
     6. every tutor photo has 176/264 jpg+webp card variants
   Run: node tools/test-tutor-fixes.mjs  (needs jsdom) */
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const ROOT = path.join(path.dirname(new URL(import.meta.url).pathname), "..");
const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8");

let failures = 0;
function check(name, ok, extra = "") {
  console.log((ok ? "PASS  " : "FAIL  ") + name + (ok ? "" : "  -> " + extra));
  if (!ok) failures++;
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function renderProfile(id) {
  const dom = new JSDOM(read("tutor.html"), {
    url: "https://ekguru.shop/tutor.html?id=" + id,
    runScripts: "outside-only", pretendToBeVisual: true
  });
  const win = dom.window;
  win.fetch = () => Promise.reject(new Error("offline"));
  win.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
  for (const el of [...win.document.querySelectorAll("script[src]")]) {
    const src = el.getAttribute("src");
    if (!src || /^https?:/.test(src)) continue;
    const f = path.join(ROOT, src.replace(/^\//, ""));
    if (fs.existsSync(f)) { try { win.eval(fs.readFileSync(f, "utf8")); } catch (e) {} }
  }
  await sleep(200);
  return win.document;
}

const pinky = await renderProfile("pinky-kumari");
check("profile: exactly one <main> landmark", pinky.querySelectorAll("main").length === 1,
  String(pinky.querySelectorAll("main").length));
const panels = [...pinky.querySelectorAll("#profile .panel")].map((pn) => pn.querySelector("h2")?.textContent || "");
check("profile: no empty Experience panel for a tutor with none stated",
  !panels.some((h) => /Experience/.test(h)), panels.join(" | "));
check("profile: no empty Teaching-method panel", !panels.some((h) => /method/i.test(h)), panels.join(" | "));
check("profile: no-slot tutor shows the honest 'no fixed times' note",
  /No fixed weekly times are published/.test(pinky.querySelector("#profile").textContent));
check("profile: empty Speaks row is omitted",
  ![...pinky.querySelectorAll("#profile .kv dd")].some((dd) => dd.textContent.trim() === ""));

const sushila = await renderProfile("sushila-g");
check("profile: tutor with slots still shows the weekly grid",
  sushila.querySelectorAll("#profile .sched .slot").length >= 7,
  String(sushila.querySelectorAll("#profile .sched .slot").length));
check("profile: exactly one <main> on a full profile too", sushila.querySelectorAll("main").length === 1);

const features = read("js/features.js");
check("booking: validate() only demands a slot when the tutor has slots",
  /anySlot/.test(features) && /if \(!chosen && anySlot\) msg = t\("book\.noSlot"\)/.test(features));

for (const id of ["sushila-g", "shikha-dutta", "pinky-kumari"]) {
  const src = read(`js/tutors/${id}.js`);
  const rating = Number((src.match(/rating:\s*([\d.]+)/) || [])[1] || 0);
  const count = Number((src.match(/reviewsCount:\s*(\d+)/) || [])[1] || 0);
  check(`data: ${id} does not claim a rating with zero reviews`, !(rating > 0 && count === 0),
    `rating=${rating} reviewsCount=${count}`);
  const photo = (src.match(/photo:\s*"([^"]+)"/) || [])[1];
  if (photo && !/^https?:/.test(photo)) {
    const base = photo.replace(/\.(jpe?g|png|webp)$/i, "");
    for (const v of [`${base}-176.jpg`, `${base}-264.jpg`, `${base}-176.webp`, `${base}-264.webp`]) {
      check(`photo variant exists: ${v}`, fs.existsSync(path.join(ROOT, v)));
    }
  }
}

console.log(failures ? `\n${failures} FAILURE(S)` : "\nALL TUTOR FIX TESTS PASSED");
process.exit(failures ? 1 : 0);

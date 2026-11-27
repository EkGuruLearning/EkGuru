#!/usr/bin/env node
/* Book mode (js/book-mode.js) — the pages that opt in must really turn into a
   stepped reader, with generated practice, and every script on the page must
   still load together without an error. Runs each page in jsdom with all its
   scripts, walks every step with Next, then plays one of each exercise.

   Pages covered: the Hindi Foundation primer (18 lessons) and the Hindi level
   pages A1…C5. Hubs that happen to share the markup must NOT become books.

   Run: node tests/regression/test-book-mode.mjs            (needs node_modules/jsdom) */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const { JSDOM } = require(path.join(ROOT, "node_modules", "jsdom"));

const BOOKS = [
  ...fs.readdirSync(path.join(ROOT, "learn/hindi/foundation"), { withFileTypes: true })
    .filter((d) => d.isDirectory()).map((d) => `learn/hindi/foundation/${d.name}/index.html`),
  ...["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3", "c4", "c5"].map((l) => `languages/hi/level/${l}/index.html`),
  // other scripts: Latin, Arabic, Tamil, Bengali, CJK, Cyrillic — the same reader, the page's own language
  ...["es", "ar", "ta", "bn", "ja", "zh", "ru", "ko"].map((c) => `languages/${c}/level/a1/index.html`),
];
const NOT_BOOKS = ["learn/hindi/foundation/index.html", "languages/hi/level/index.html", "languages/es/level/index.html"];

function load(rel) {
  const html = fs.readFileSync(path.join(ROOT, rel), "utf8");
  const dom = new JSDOM(html, { url: "https://ekguru.shop/" + rel.replace(/index\.html$/, ""), runScripts: "outside-only", pretendToBeVisual: true });
  const w = dom.window, d = w.document, errs = [];
  const store = new Map();
  const fake = { getItem: (k) => (store.has(k) ? store.get(k) : null), setItem: (k, v) => store.set(k, String(v)), removeItem: (k) => store.delete(k), clear: () => store.clear(), key: (i) => [...store.keys()][i] || null, get length() { return store.size; } };
  Object.defineProperty(w, "localStorage", { value: fake });
  Object.defineProperty(w, "sessionStorage", { value: fake });
  w.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
  w.scrollTo = () => {};
  w.fetch = () => Promise.reject(new Error("offline"));
  w.matchMedia = w.matchMedia || ((q) => ({ matches: false, media: q, addEventListener() {}, removeEventListener() {}, addListener() {}, removeListener() {} }));
  w.console = { log() {}, info() {}, warn() {}, error(...a) { errs.push(String(a.join(" ")).slice(0, 120)); }, debug() {} };
  for (const s of d.querySelectorAll("script[src]")) {
    const src = s.getAttribute("src");
    if (/^https?:/.test(src)) continue;
    const f = path.join(ROOT, src.startsWith("/") ? src.slice(1) : path.join(path.dirname(rel), src));
    if (!fs.existsSync(f)) { errs.push("missing " + src); continue; }
    try { w.eval(fs.readFileSync(f, "utf8")); } catch (e) { errs.push(src + ": " + e.message.slice(0, 80)); }
  }
  for (const s of d.querySelectorAll('script:not([src]):not([type="application/ld+json"])')) {
    try { w.eval(s.textContent); } catch (e) { errs.push("inline: " + e.message.slice(0, 80)); }
  }
  d.dispatchEvent(new w.Event("DOMContentLoaded", { bubbles: true }));
  w.dispatchEvent(new w.Event("load"));
  return { w, d, errs };
}

let failed = 0, passed = 0;
function check(name, ok, detail) {
  if (ok) passed++; else failed++;
  console.log((ok ? "PASS" : "FAIL") + "  " + name + (detail ? "  — " + detail : ""));
}

for (const rel of BOOKS) {
  if (!fs.existsSync(path.join(ROOT, rel))) { check(rel, false, "missing page"); continue; }
  const { d, errs, w } = load(rel);
  const B = w.EkGuruBook;
  const steps = [...d.querySelectorAll(".bk-leaf")];
  // every text node of the original article is still on the page (book mode only wraps and adds)
  const plain = new JSDOM(fs.readFileSync(path.join(ROOT, rel), "utf8")).window;
  const walker = plain.document.createTreeWalker(plain.document.querySelector(".art"), plain.NodeFilter.SHOW_TEXT);
  const before = [];
  while (walker.nextNode()) { const t = walker.currentNode.textContent.replace(/\s+/g, " ").trim(); if (t.length > 20 && walker.currentNode.parentNode.tagName !== "SCRIPT") before.push(t); }
  const textAfter = d.querySelector(".art").textContent.replace(/\s+/g, " ");
  const lost = before.filter((t) => !textAfter.includes(t));
  let n = 0;
  try { while (B && n < steps.length - 1) { B.go(n + 1); n++; } } catch (e) { errs.push("go: " + e.message); }
  const visible = steps.filter((s) => !s.hidden).length;
  const kinds = new Set([...d.querySelectorAll(".bk-ex")].map((e) => e.dataset.kind));
  for (const ex of d.querySelectorAll(".bk-ex")) {
    const k = ex.dataset.kind;
    try {
      if (k === "match") {
        for (let g = 0; g < 40 && !ex.querySelector(".bk-score"); g++) {
          const hi = ex.querySelector(".bk-chip.hi:not(.hit)"); if (!hi) break; hi.click();
          ex.querySelector('.bk-chip.en[data-k="' + hi.dataset.k + '"]').click();
        }
      } else if (k === "listen" || k === "picture" || k === "roman") {
        const o = ex.querySelector(".bk-opt"); o && o.click();
      } else if (k === "build" || k === "order") {
        const slot = ex.querySelector(".bk-drop");
        for (let g = 0; g < 30 && !slot.classList.contains("ok"); g++) {
          for (const b of ex.querySelectorAll(".bk-tray .bk-akshar")) { if (!b.disabled) { b.click(); if (slot.classList.contains("ok")) break; } }
        }
        if (!slot.classList.contains("ok")) errs.push(k + " cannot be completed");
      }
    } catch (e) { errs.push(k + ": " + e.message.slice(0, 60)); }
  }
  const minKinds = /foundation/.test(rel) ? 1 : 4;
  const ok = !!B && steps.length >= 7 && visible === 1 && kinds.size >= minKinds && errs.length === 0 && lost.length === 0 && !!d.querySelector(".bk-nav") && !!d.querySelector(".bk-rail");
  check(rel, ok, `steps ${steps.length}, exercise kinds ${[...kinds].join("/") || "none"}, words ${B && B.words}` + (errs.length ? ", errors: " + errs.join(" | ") : "") + (lost.length ? ", lost text: " + lost[0].slice(0, 40) : ""));
}

for (const rel of NOT_BOOKS) {
  const { d, errs } = load(rel);
  check(rel + " stays a plain page", !d.querySelector(".bk-leaf") && errs.length === 0, errs.join(" | "));
}

// the akshar splitter: the unit a child writes
{
  const { w } = load(BOOKS[0]);
  const ak = w.EkGuruBook.akshar;
  const cases = [["बाजार", ["बा", "जा", "र"]], ["पाठशाला", ["पा", "ठ", "शा", "ला"]], ["क्षमा", ["क्ष", "मा"]], ["किताबें", ["कि", "ता", "बें"]]];
  for (const [word, want] of cases) check("akshar " + word, JSON.stringify(ak(word)) === JSON.stringify(want), JSON.stringify(ak(word)));
}

console.log(`\n${failed ? "FAIL" : "PASS"}  ${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);

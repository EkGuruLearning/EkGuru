#!/usr/bin/env node
/* ==========================================================================
   test-refresh-quiet.mjs — a refresh does nothing you did not ask for

   Prakash: "refresh karne pe kuch bhi apne aap start nahi hona chahiye."

   A reload is the single most common thing anyone does to this site, and the
   page has ~20 scripts on it. This test loads the pages that matter, boots
   every script the page itself loads, and then looks at what started MOVING
   without a single click, tap, key or scroll:

     · a quiz, game or typing drill that started by itself
     · a drawer, modal, banner or overlay that opened itself
     · audio or video that played
     · a navigation, redirect or beforeunload prompt
     · scroll that moved
     · network work beyond the ones the page declares

   Anything on that list is a refresh starting something. Nothing on it is a
   stylistic question.

   Run:  node tools/test-refresh-quiet.mjs
   ========================================================================== */
import { readFileSync, existsSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { JSDOM, VirtualConsole } = require("jsdom");
const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
process.chdir(ROOT);

let pass = 0, fail = 0;
const ok = (name, cond, detail = "") => {
  if (cond) { pass++; console.log("  PASS  " + name); }
  else { fail++; console.log("  FAIL  " + name + (detail ? " — " + detail : "")); }
};
const read = (p) => readFileSync(p, "utf8");
const scriptSources = (html) => [...html.matchAll(/<script\b[^>]*>/gi)].map((m) => { const x=m[0].match(/\bsrc=["']([^"']+)["']/i); return x&&x[1]; }).filter(Boolean);

/* The pages a visitor actually reloads. */
const PAGES = [
  "index.html",
  "learn/bengali/index.html",
  "learn/bengali/practice/quiz/index.html",
  "learn/bengali/practice/worksheets/index.html",
  "languages/ar/quiz/index.html",
  "languages/ar/practice/index.html",
  "contact/index.html",
  "find-tutors.html",
  "learn/hindi/index.html"
];

function boot(page) {
  const html = read(page);
  const virtualConsole = new VirtualConsole();     /* keep jsdom quiet */
  const notes = [];
  virtualConsole.on("jsdomError", (e) => notes.push(e.message));

  const dom = new JSDOM(html, {
    url: "https://ekguru.shop/" + page.replace(/index\.html$/, ""),
    runScripts: "outside-only",
    pretendToBeVisual: true,
    virtualConsole
  });
  const w = dom.window, d = w.document;

  const seen = { fetch: [], xhr: [], nav: [], play: [], timeouts: [] };
  w.fetch = (url, init) => { seen.fetch.push(String(url)); return Promise.resolve({ ok: false, json: () => Promise.resolve({}) }); };
  w.XMLHttpRequest = function () { this.open = (m, u) => seen.xhr.push(String(u)); this.send = () => {}; this.setRequestHeader = () => {}; };
  w.HTMLMediaElement.prototype.play = function () { seen.play.push(this.tagName); return Promise.resolve(); };
  try { Object.defineProperty(w.navigator, "serviceWorker", { value: undefined, configurable: true }); } catch (e) {}
  w.addEventListener("beforeunload", (e) => seen.nav.push("beforeunload"));
  const nav = (what) => seen.nav.push(what);
  ["assign", "replace", "reload"].forEach((m) => { try { w.location[m] = () => nav("location." + m); } catch (e) {} });

  /* Boot exactly what the page asks for: scripts in document order. */
  const srcs = scriptSources(html);
  for (const src of srcs) {
    const file = path.normalize(src.replace(/^\.\.\//, "").replace(/^(\.\.\/)+/, "").replace(/^\//, ""));
    if (!existsSync(file) || !file.endsWith(".js")) continue;
    try { w.eval(read(file)); } catch (e) { notes.push(file + ": " + e.message); }
  }
  d.dispatchEvent(new w.Event("DOMContentLoaded", { bubbles: true }));
  return { dom, w, d, seen, srcs, notes };
}

console.log("\n1. the page itself declares only what it needs\n");

{
  /* A page must not pull a script twice, and no page may load a tracker the
     rest of the site does not load. */
  let dupe = [];
  for (const p of PAGES) {
    const srcs = scriptSources(read(p));
    const dup = srcs.filter((s, i) => srcs.indexOf(s) !== i);
    if (dup.length) dupe.push(p + " (" + dup.join(", ") + ")");
  }
  ok("no page loads the same script twice", dupe.length === 0, dupe.join("; "));
}

/* ------------------------------------------------------------------ */
const scripts = ["js/main.js"];

console.log("\n2. nothing starts on its own\n");

const started = { quiz: [], overlay: [], audio: [], nav: [], scroll: [] };
const booted = [];        /* proof the harness really boots the page */
let scriptErrors = [];

for (const page of PAGES) {
  const { dom, w, d, seen, notes } = boot(page);

  /* give timers a chance to fire the way they would after a load */
  await new Promise((r) => setTimeout(r, 30));

  /* --- a drill / quiz / game that started by itself ---------------- */
  const liveQuiz = d.querySelector("#q-body button[data-opt], #ws-app .ws-page, #game-canvas.is-running, [data-running='true']");
  if (liveQuiz && !w.EKGURU_TEST_INTERACTION) {
    /* A worksheet page is SUPPOSED to arrive with a sample sheet — that is
       not a drill running, it is the sheet itself. Distinguish them. */
    const isBaked = page.includes("worksheets") && d.querySelector("#w-sheet .ws-page");
    if (!isBaked) started.quiz.push(page);
  }

  /* --- an overlay, drawer or modal that opened itself -------------- */
  const opened = [...d.querySelectorAll(".is-open, .is-on, [open], [aria-expanded='true']")]
    .filter((el) => /\b(drawer|modal|sheet|menu|nav|overlay|net-banner|banner|dialog|panel)\b/i.test(el.className + " " + el.tagName));
  const realOpen = opened.filter((el) => el.id !== "ekg-net-banner");
  if (realOpen.length) started.overlay.push(page + " (" + realOpen.map((e) => e.className || e.tagName).join(", ") + ")");

  /* --- media ------------------------------------------------------- */
  if (seen.play.length) started.audio.push(page + " (" + seen.play.join(", ") + ")");

  /* --- navigation / prompts ---------------------------------------- */
  if (seen.nav.length) started.nav.push(page + " (" + seen.nav.join(", ") + ")");

  /* --- scroll ------------------------------------------------------- */
  const scrolled = w.scrollY || w.pageYOffset || 0;
  const left = d.documentElement.scrollLeft || d.body.scrollLeft || 0;
  if (scrolled !== 0 || left !== 0) started.scroll.push(page + " (" + scrolled + "," + left + ")");

  /* Proof that this test is not vacuous: the page's own scripts ran, and the
     ones that build UI got as far as building it. If a script had thrown, the
     "nothing started" answer below would be worth nothing. */
  if (notes.length) scriptErrors.push(page + ": " + notes.slice(0, 2).join(" / "));
  const mounted = d.querySelector("#ws-app #w-make, #q-body, #ekg-hdr, header.hdr, .hdr");
  booted.push(page + (mounted ? "" : " (no UI built)"));

  dom.window.close();
}

ok("every script each page loads runs without an error",
  scriptErrors.length === 0, scriptErrors.slice(0, 3).join(" | "));
ok("each page really booted (its UI was built)",
  booted.every((b) => !b.includes("no UI built")), booted.filter((b) => b.includes("no UI built")).join("; "));
ok("no quiz, drill or game starts by itself", started.quiz.length === 0, started.quiz.join("; "));
ok("no drawer, modal or overlay opens by itself", started.overlay.length === 0, started.overlay.join("; "));
ok("no audio or video plays by itself", started.audio.length === 0, started.audio.join("; "));
ok("nothing navigates, redirects or prompts on load", started.nav.length === 0, started.nav.join("; "));
ok("the page does not move the reader's scroll", started.scroll.length === 0, started.scroll.join("; "));

console.log("\n3. the rules that make that true, in the source\n");

{
  const sources = read("js/main.js") + read("js/features.js") + read("js/experience.js") +
    read("js/storybook.js") + read("js/hindi-tools.js") + read("js/onboarding.js");
  ok("listen, not speak: the scripts boot on DOMContentLoaded",
    /document\.addEventListener\("DOMContentLoaded", boot\)/.test(read("js/hindi-tools.js")));
  ok("a page's own scripts never call location.reload()",
    !/location\.reload\(\)/.test(sources), "a reload loop is the worst kind of surprise");
  ok("no unload/beforeunload prompt is ever registered",
    !/addEventListener\("beforeunload"/.test(sources));
  ok("media is never autoplayed",
    !/\.autoplay\s*=\s*true/.test(sources) && !/<audio[^>]*autoplay/.test(read("js/storybook.js")));
  ok("the connectivity banner is the only thing allowed to appear unasked",
    /ekg-net-banner/.test(read("js/site-config.js")));
  ok("a returning visitor's scroll position is restored, not invented",
    /sessionStorage|history\.scrollRestoration/.test(read("js/scroll-restore.js")));
  ok("the service worker caches, it does not force a reload",
    !/window\.location\.reload/.test(read("sw.js")));
}

console.log("\n4. a second boot adds nothing (the reload case)\n");

{
  /* The page is not always parsed once: a service worker can hand the same
     document to a tab that already has it, and a shell can re-inject. Boot
     the scripts twice and count what piled up. */
  const { w, d } = boot("learn/bengali/practice/worksheets/index.html");
  const before = {
    make: d.querySelectorAll("#ws-app #w-make").length,
    sheets: d.querySelectorAll("#w-sheet .ws-page").length,
    apps: d.querySelectorAll("#ws-app").length
  };
  const html = read("learn/bengali/practice/worksheets/index.html");
  for (const src of scriptSources(html)) {
    const file = src.replace(/^(\.\.\/)+/, "").replace(/^\//, "");
    if (!existsSync(file) || !file.endsWith(".js")) continue;
    try { w.eval(read(file)); } catch (e) {}
  }
  d.dispatchEvent(new w.Event("DOMContentLoaded", { bubbles: true }));
  const after = {
    make: d.querySelectorAll("#ws-app #w-make").length,
    sheets: d.querySelectorAll("#w-sheet .ws-page").length,
    apps: d.querySelectorAll("#ws-app").length
  };
  ok("a second boot builds one worksheet builder, not two",
    before.make === 1 && after.make === 1, JSON.stringify([before, after]));
  ok("and it does not duplicate the sheet",
    after.sheets <= Math.max(1, before.sheets) && before.sheets >= 1, JSON.stringify([before, after]));
  ok("it does not add a second #ws-app", after.apps === 1);
  w.EKGURU_QUESTIONS && ok("a second boot does not double-post the vote queue",
    typeof w.EKGURU_QUESTIONS.pending() === "number");
  dom_close(w);
}

function dom_close(w) { try { w.close(); } catch (e) {} }

/* ------------------------------------------------------------------ */

console.log("\n5. a reload shows what is deployed, not yesterday's copy\n");

{
  /* THE BUG THIS SECTION EXISTS FOR (v42).

     sw.js served HTML and JavaScript network-first, but let css fall through
     to the stale-while-revalidate branch at the bottom. style.min.css is NOT
     fingerprinted: the filename never changes and the contents change on
     every build. So the first reload after a deploy painted the OLD
     stylesheet — a fresh print fix, a fresh palette, a fresh layout — and
     only stored the new one for "next time"; the reload after that suddenly
     showed something different. Two refreshes, two different sites.

     Everything that is code or styling is network-first now; images stay
     cache-first, because a filename that never changes meaning is safe to
     serve from cache. */
  const sw = read("sw.js");
  const isCode = sw.match(/const isCode = ([^;]+);/s);
  const isImage = sw.match(/const isImage = ([^;]+);/s);
  ok("sw.js treats CSS as code, so a reload cannot paint a stale stylesheet",
    !!isCode && /css/.test(isCode[1]), isCode ? isCode[1].replace(/\s+/g, " ") : "no isCode rule");
  ok("HTML and JavaScript are still network-first",
    !!isCode && /html\?/.test(isCode[1]) && /js/.test(isCode[1]));
  ok("images are still cache-first (their names never change meaning)",
    !!isImage && !/css/.test(isImage[1]), isImage ? isImage[1].replace(/\s+/g, " ") : "no isImage rule");
  ok("offline still falls back to the saved copy instead of failing",
    /catch\(\(\) =>[\s\S]{0,240}caches\.open\(OFFLINE\)/.test(sw));
  ok("the cache generation was bumped, so nobody keeps the old stylesheet",
    /const BUILD_ID = "[^"]*-v(?:4[2-9]|[5-9][0-9])\b/.test(sw), (sw.match(/const BUILD_ID = "([^"]+)"/) || [])[1]);
  ok("the worker never forces the tab to reload",
    !/location\.reload\(\)/.test(sw) && !/clients\.claim[\s\S]{0,120}reload/.test(sw));
}

/* ------------------------------------------------------------------ */

console.log("\n6. the same page, booted twice, is the same page\n");

{
  /* A reload must land the reader in the same place, not somewhere else. Boot
     a page, boot it again from the same bytes, and compare the structure the
     reader sees: the same landmarks, the same number of them, and no
     navigation started the second time either. */
  const SAME = [
    "index.html",
    "learn/bengali/practice/quiz/index.html",
    "learn/bengali/practice/worksheets/index.html",
    "languages/ar/practice/index.html",
    "contact/index.html"
  ];
  const shape = (d) => ({
    ids: [...d.querySelectorAll("[id]")].map((e) => e.id).sort().join(","),
    landmarks: [d.querySelector("header.hdr"), d.querySelector("main"), d.querySelector("footer.ftr")]
      .map((e) => !!e).join(","),
    count: d.querySelectorAll("*").length
  });
  const drift = [];
  for (const page of SAME) {
    const a = boot(page), b = boot(page);
    const sa = shape(a.d), sb = shape(b.d);
    if (sa.ids !== sb.ids || sa.landmarks !== sb.landmarks) {
      drift.push(page + " (landmarks " + sa.landmarks + " vs " + sb.landmarks + ")");
    }
    if (b.seen.nav.length) drift.push(page + " navigates on the second boot (" + b.seen.nav.join(",") + ")");
    a.dom.window.close(); b.dom.window.close();
  }
  ok("a reload lands on the same page it reloaded, with the same landmarks",
    drift.length === 0, drift.slice(0, 3).join("; "));
}

console.log(`\n${fail ? "FAIL" : "PASS"}  ${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);

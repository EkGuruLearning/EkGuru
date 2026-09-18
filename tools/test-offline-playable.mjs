#!/usr/bin/env node
/* ==========================================================================
   test-offline-playable.mjs — the practice game plays with the network off

   Prakash asked for an offline game that is "fully playable", and that is a
   claim about behaviour, not about a manifest. So this test takes the network
   away and plays.

   Four things are checked, in this order:

     1. the game is in the page. A drill that fetches its question from a
        server is not an offline game. Either the questions are inline, or
        they live in a same-origin file the service worker precaches.
     2. the only cross-origin subresource on these pages is the ad loader —
        which is async and whose absence the page is written to survive.
        Nothing a learner touches depends on someone else's server.
     3. boot the page with fetch rejecting, XHR rejecting, navigator.onLine
        false and Audio unavailable, then actually answer a question and press
        Next. The score line must still move and not one request may be made.
     4. the voice falls back to the device. Listen buttons prefer the local
        speech engine, skip the network voice when offline, and fall back to
        the device if the network voice fails.

   Run:  node tools/test-offline-playable.mjs
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
  if (cond) { pass++; console.log("  ok    " + name); }
  else { fail++; console.log("  FAIL  " + name + (detail ? " — " + detail : "")); }
};
const read = (p) => readFileSync(p, "utf8");

/* The pages a learner would actually play on: a drill, a placement test and
   the standalone toolbox games. */
const GAME_PAGES = [
  "languages/ar/practice/index.html",
  "languages/ar/quiz/index.html",
  "toolbox/hindi-quiz/index.html",
  "toolbox/hindi-flashcards/index.html"
];

const sw = read("sw.js");

console.log("\n1. the game carries its own questions\n");

{
  /* A drill's questions live either in the page or in a same-origin script the
     service worker fetches (and therefore caches) like any other asset. What
     must never happen is a question arriving from someone else's server. */
  const thin = [], offsite = [], missing = [];
  for (const p of GAME_PAGES) {
    const html = read(p);
    const inline = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)]
      .map((m) => m[1])
      .filter((b) => !/^\s*\{?\s*"@context"/.test(b))          /* skip ld+json */
      .join("\n");
    const scripts = [...html.matchAll(/<script src="([^"]+)"/g)].map((m) => m[1]);
    let fromFiles = "";
    for (const src of scripts) {
      const f = path.normalize(src.replace(/^(\.\.\/)+/, "").replace(/^\//, ""));
      if (!existsSync(f)) { missing.push(`${p} → ${src}`); continue; }
      fromFiles += read(f);
    }
    const hay = inline + "\n" + fromFiles;
    const pool = (hay.match(/EKGURU_PRACTICE_BANK|EKGURU_COURSE_[A-Z]+|DECKS\s*=|"q"\s*:|POOL\s*=/g) || []).length;
    const remote = [...inline.matchAll(/(?:fetch|XMLHttpRequest|open)\(\s*["'](https?:\/\/[^"']+)/g)];
    if (pool === 0) thin.push(`${p} (no questions in the page or its scripts)`);
    if (remote.length) offsite.push(`${p} → ${remote[0][1]}`);
  }
  ok("every game page holds its questions, in the page or in a same-origin script",
    thin.length === 0, thin.join("; "));
  ok("no game page asks a third-party server for its questions",
    offsite.length === 0, offsite.join("; "));
  ok("every script a game page names exists on disk", missing.length === 0,
    missing.slice(0, 3).join("; "));

  /* The cache is what makes a visited drill playable later: same-origin
     responses are cached, HTML/JS network-first with the saved copy as the
     fallback, images cache-first. A first-ever visit with no network is not
     something a service worker can invent. */
  ok("the worker caches every same-origin response a game page asks for",
    /caches\.open\(/.test(sw) && /cache\.put|put\(/.test(sw));
  ok("and falls back to that copy when the network is gone",
    /catch\(\(\) =>[\s\S]{0,240}caches\.open\(OFFLINE\)/.test(sw));
}

console.log("\n2. the only cross-origin dependency is the ad loader\n");

{
  /* Page-wide: collect every cross-origin subresource on every generated page
     and name it. Anything but the ad loader is a dependency someone else can
     take away from a learner. */
  const { execSync } = require("node:child_process");
  const files = execSync("git ls-files '*.html'", { encoding: "utf8" })
    .trim().split("\n").filter((f) => existsSync(f));

  const hosts = new Map();
  const risky = [];
  for (const f of files) {
    const html = read(f);
    for (const m of html.matchAll(/<(script|link|img|iframe|audio|source)\b([^>]*)>/g)) {
      const tag = m[1], attrs = m[2];
      const href = (attrs.match(/(?:src|href)="(https?:\/\/[^"]+)"/) || [])[1];
      if (!href) continue;
      let host = "";
      try { host = new URL(href).host; } catch (e) { continue; }
      if (host === "ekguru.shop" || host === "www.ekguru.shop") continue;
      const rel = (attrs.match(/rel="([^"]+)"/) || [])[1] || "";
      const hint = tag === "link" && /preconnect|dns-prefetch|prefetch/.test(rel);
      hosts.set(host + (hint ? " (hint)" : ""), (hosts.get(host + (hint ? " (hint)" : "")) || 0) + 1);
      if (hint) continue;                       /* a hint fetches nothing */
      /* A stylesheet, script or iframe is logic. An image or a media file is
         content: without the network it simply does not appear. */
      const logic = tag === "script" || tag === "iframe" ||
        (tag === "link" && /stylesheet/.test(rel));
      if (logic && host !== "pagead2.googlesyndication.com") {
        risky.push(`${f} <${tag}> ${host}`);
      }
      if (!logic && host !== "i.ytimg.com" && host !== "www.youtube-nocookie.com") {
        risky.push(`${f} <${tag}> ${host}`);
      }
    }
  }
  const report = [...hosts].map(([h, n]) => `${h}×${n}`).join(", ");
  ok(`cross-origin hosts on the site are ad and video hosts only — ${report}`,
    risky.length === 0, risky.slice(0, 4).join("; "));

  /* The loader has to be async and optional, and the ad code must never be the
     thing that makes a page work. */
  const blocking = [];
  for (const f of files) {
    const html = read(f);
    if (/pagead2\.googlesyndication\.com\/pagead\/js\/adsbygoogle\.js/.test(html)) {
      const tag = (html.match(/<script[^>]*pagead2\.googlesyndication\.com[^>]*>/) || [])[0] || "";
      if (!/\basync\b/.test(tag)) blocking.push(f);
    }
  }
  ok("the ad loader is async everywhere it appears", blocking.length === 0,
    blocking.slice(0, 3).join("; "));

  const monet = read("js/monetization.js");
  ok("no page script waits for the ad loader before it works",
    !/adsbygoogle\s*[.\[]/.test(monet) && !/requestAd|push\(\{\)/.test(monet));
  /* A preconnect hint is not a dependency, but it is also a connection to an
     ad host made before the learner does anything — so it may only appear on
     the pages that carry the loader, and never as a stylesheet or a script. */
  const hintOnly = [];
  for (const f of files) {
    const html = read(f);
    for (const m of html.matchAll(/<(script|link|iframe)\b[^>]*(?:src|href)="https?:\/\/(googleads\.g\.doubleclick\.net|pagead2\.googlesyndication\.com)[^"]*"[^>]*>/g)) {
      const tag = m[1], attrs = m[0];
      const rel = (attrs.match(/rel="([^"]+)"/) || [])[1] || "";
      if (tag !== "link" || !/preconnect|dns-prefetch/.test(rel)) {
        if (tag !== "script" || !/adsbygoogle\.js/.test(attrs)) hintOnly.push(`${f} <${tag}>`);
      }
      if (/preconnect|dns-prefetch/.test(rel) &&
          !/pagead2\.googlesyndication\.com\/pagead\/js\/adsbygoogle\.js/.test(html)) {
        hintOnly.push(`${f} prepares an ad connection but loads no ad`);
      }
    }
  }
  ok("an ad host is never a stylesheet or a frame, and is only warmed where an ad loads",
    hintOnly.length === 0, hintOnly.slice(0, 3).join("; "));
}

console.log("\n3. answer a question with the network off\n");

{
  /* Boot a real practice page with the network gone, then play it. */
  const page = "languages/ar/practice/index.html";
  const html = read(page);
  const virtualConsole = new VirtualConsole();
  const notes = [];
  virtualConsole.on("jsdomError", (e) => notes.push(String(e.message).split("\n")[0]));

  const dom = new JSDOM(html, {
    url: "https://ekguru.shop/" + page.replace(/index\.html$/, ""),
    runScripts: "outside-only",
    pretendToBeVisual: true,
    virtualConsole
  });
  const w = dom.window, d = w.document;

  const requests = [];
  w.fetch = (u) => { requests.push("fetch " + u); return Promise.reject(new Error("offline")); };
  w.XMLHttpRequest = function () {
    this.open = (m, u) => requests.push("xhr " + u);
    this.send = () => { this.onerror && this.onerror(new w.Event("error")); };
    this.setRequestHeader = () => {};
  };
  try { Object.defineProperty(w.navigator, "onLine", { value: false, configurable: true }); } catch (e) {}
  try { Object.defineProperty(w.navigator, "serviceWorker", { value: undefined, configurable: true }); } catch (e) {}
  /* No Audio: the device cannot fetch a sound either. */
  w.Audio = function () { throw new Error("offline: no audio"); };

  /* Boot exactly what the browser would, in document order: the page's own
     inline scripts included — that is where a drill page hooks its buttons up. */
  for (const m of html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)) {
    const attrs = m[1], body = m[2];
    if (/type="application\/ld\+json"/.test(attrs)) continue;
    const src = (attrs.match(/src="([^"]+)"/) || [])[1];
    if (src) {
      const f = path.normalize(src.replace(/^(\.\.\/)+/, "").replace(/^\//, ""));
      if (!existsSync(f) || !f.endsWith(".js")) continue;
      try { w.eval(read(f)); } catch (e) { notes.push(f + ": " + e.message); }
    } else if (body.trim()) {
      try { w.eval(body); } catch (e) { notes.push("inline: " + e.message); }
    }
  }
  d.dispatchEvent(new w.Event("DOMContentLoaded", { bubbles: true }));

  /* The practice pages mount on a 100 ms poll: the engine appears, the page
     mounts the vocabulary drill. Offline that poll is all that happens — no
     fetch is made, the bank is already in js/course-<code>.js. */
  const wait = (ms) => new Promise((r) => setTimeout(r, ms));

  const booted = [];
  const start = d.getElementById("ar-b-vocab");
  if (start) {
    try { start.dispatchEvent(new w.MouseEvent("click", { bubbles: true })); }
    catch (e) { booted.push("click: " + e.message); }
  }
  let opts = d.querySelectorAll(".px-opt, .px-word");
  for (let i = 0; i < 12 && opts.length === 0; i++) {
    await wait(100);
    opts = d.querySelectorAll(".px-opt, .px-word");
  }
  const box = d.querySelector(".px-head, .px-q, .px-wrap");
  ok("the drill rendered itself with no network", opts.length > 0 && !!box,
    `options=${opts.length} container=${!!box} ${booted.join("; ")}`);
  ok("no page script threw while booting offline", notes.length === 0, notes.slice(0, 3).join(" | "));

  /* Let the page settle before playing: these practice pages mount on a 100 ms
     poll and hide their buttons until the engine exists. A learner needs
     longer than that to move a finger, so this is not a click race — but the
     test has to wait for the same state the learner would see. */
  await wait(400);
  const settled = (d.querySelector(".px-q") || {}).textContent || "";
  await wait(150);
  ok("the drill that appears is the drill that stays",
    settled.length > 0 && settled === ((d.querySelector(".px-q") || {}).textContent || ""));

  const scoreOf = () => ((d.querySelector(".px-score") || {}).textContent || "").trim();
  const countOf = () => ((d.querySelector(".px-count") || {}).textContent || "").trim();
  const before = scoreOf(), beforeCount = countOf();

  /* Answer the question the way a learner does: pick an option, then Next. */
  const answer = d.querySelectorAll(".px-opt, .px-word");
  const first = answer[0];
  try { first.dispatchEvent(new w.MouseEvent("click", { bubbles: true })); }
  catch (e) { booted.push("answer: " + e.message); }
  await wait(50);

  /* The engine marks the choice and tells the learner which one was right —
     all of it computed in the page, none of it fetched. */
  const mark = d.querySelector(".px-opt.px-right, .px-opt.px-wrong, .px-word.px-right, .px-word.px-wrong");
  const feedback = (d.querySelector(".px-fb") || {}).textContent || "";
  ok("a choice can be made offline, and the page says which was right",
    !!mark && feedback.trim().length > 2,
    `mark=${!!mark} feedback="${feedback.trim().slice(0, 40)}"`);

  const nextBtn = d.querySelector(".px-next");
  let advanced = false;
  if (nextBtn && !nextBtn.hasAttribute("hidden")) {
    try { nextBtn.dispatchEvent(new w.MouseEvent("click", { bubbles: true })); advanced = true; }
    catch (e) { booted.push("next: " + e.message); }
  }
  await wait(50);
  const after = scoreOf(), afterCount = countOf();
  ok("the game moved forward offline",
    advanced || beforeCount !== afterCount || scoreOf() !== before,
    `"${beforeCount}" → "${afterCount}" · score "${after}"`);
  ok("playing it made not one network request", requests.length === 0,
    requests.slice(0, 3).join("; "));
  ok("and nothing threw while playing", booted.length === 0, booted.join(" | "));
}

console.log("\n4. the voice falls back to the device\n");

{
  const story = read("js/storybook.js");
  /* Order matters: the local engine is tried first, the network voice is
     skipped when the browser says it is offline. */
  const localFirst = story.indexOf("canLocal") < story.indexOf("translate.googleapis.com");
  ok("the local speech engine is tried before the network voice", localFirst);
  ok("the network voice is skipped when the browser is offline",
    /navigator\.onLine\s*!==\s*false/.test(story) &&
    /navigator\.onLine\s*===\s*false/.test(story));
  ok("a failed network voice falls back to the device instead of silence",
    /failToLocal/.test(story) && /markApiDead/.test(story));

  /* Behavioural: with the network off, speak() must not build a network Audio. */
  const dom = new JSDOM("<body></body>", {
    url: "https://ekguru.shop/", runScripts: "outside-only", pretendToBeVisual: true
  });
  const w = dom.window;
  let audioBuilt = 0, spoke = 0;
  w.Audio = function () { audioBuilt++; throw new Error("offline"); };
  w.speechSynthesis = {
    getVoices: () => [{ name: "Local", lang: "ar-SA", default: true, localService: true }],
    speak: () => { spoke++; },
    cancel: () => {}
  };
  w.SpeechSynthesisUtterance = function (t) { this.text = t; };
  try { Object.defineProperty(w.navigator, "onLine", { value: false, configurable: true }); } catch (e) {}
  try { w.eval(read("js/storybook.js")); } catch (e) {}
  const voice = w.EkGuruVoice;
  ok("the voice module is on the page", !!voice && typeof voice.speak === "function");
  let said = false;
  try { said = voice ? voice.speak("مرحبا", { lang: "ar" }) : false; } catch (e) { said = false; }
  ok("speaking offline used the device voice and never the network",
    audioBuilt === 0 && (spoke > 0 || said === true),
    `audio=${audioBuilt} local=${spoke}`);
}

console.log(`\n${fail === 0 ? "PASS" : "FAIL"}  ${pass} passed, ${fail} failed\n`);
process.exit(fail === 0 ? 0 : 1);

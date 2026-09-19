/* DOM smoke test for the v200 experience layer.
   Run:  node tools/test-experience-dom.mjs        (needs: npm i jsdom)
   Verifies, in a real DOM, that:
     · js/experience.js adds html.xp-anim only when it can reveal,
     · every .reveal / .stagger / .xp-rise block ends up visible,
     · the language rail is cloned for a seamless marquee,
     · js/site-search.js renders highlighted, sectioned, keyboard-reachable
       results from search-index.json and never leaves a dead end.
   Exits 1 on the first failed expectation. */
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const ROOT = new URL("..", import.meta.url).pathname.replace(/\/$/, "");

const index = JSON.parse(readFileSync(`${ROOT}/search-index.json`, "utf8"));
let failures = 0;

function check(name, ok, extra = "") {
  console.log(`${ok ? "ok  " : "FAIL"}  ${name}${extra ? "  — " + extra : ""}`);
  if (!ok) failures++;
}

function makeDom(file) {
  const html = readFileSync(`${ROOT}/${file}`, "utf8");
  const dom = new JSDOM(html, { url: "https://ekguru.shop/" + file.replace(/index\.html$/, ""), pretendToBeVisual: true, runScripts: "dangerously" });
  const { window } = dom;
  // stubs a browser gives us for free
  window.matchMedia = window.matchMedia || (() => ({ matches: false, addListener() {}, removeListener() {} }));
  window.fetch = (url) => Promise.resolve({ json: () => Promise.resolve(index) });
  window.requestAnimationFrame = (fn) => setTimeout(fn, 0);
  window.IntersectionObserver = class {
    constructor(cb) { this.cb = cb; }
    observe(el) { this.cb([{ isIntersecting: true, target: el }], this); }
    unobserve() {}
    disconnect() {}
  };
  window.navigator.connection = { saveData: false, effectiveType: "4g" };
  return dom;
}

/* Injected as a real <script> element so jsdom runs it in the window realm
   (window.eval() would leave `window` undefined) and sets currentScript the
   way a browser does. */
function evalFile(dom, file) {
  const { window } = dom;
  const s = window.document.createElement("script");
  s.textContent = readFileSync(`${ROOT}/${file}`, "utf8");
  window.document.head.appendChild(s);
}

/* js/experience.js defers its boot to DOMContentLoaded, which jsdom fires
   after the injected script has run. Wait for it (or for a short timeout). */
function waitForLoad(dom) {
  return new Promise((resolve) => {
    const { window } = dom;
    if (window.document.readyState === "complete") return resolve();
    let done = false;
    const once = () => { if (!done) { done = true; resolve(); } };
    window.addEventListener("DOMContentLoaded", once, { once: true });
    window.addEventListener("load", once, { once: true });
    setTimeout(once, 600);
  });
}

/* ---------- home page -------------------------------------------------- */
{
  const dom = makeDom("index.html");
  const { window } = dom;
  const doc = window.document;
  evalFile(dom, "js/experience.js");
  await waitForLoad(dom);

  const html = doc.documentElement;
  check("home: html gets xp-anim", html.classList.contains("xp-anim"));
  check("home: language attributes set", html.getAttribute("data-xp-lang") === "en" && html.getAttribute("data-xp-target") === "hi");

  const hidden = [...doc.querySelectorAll(".reveal, .stagger, .xp-rise, .xp-stagger")]
    .filter((el) => el.className.match(/reveal|stagger|xp-rise|xp-stagger/) && !el.classList.contains("in") && !el.classList.contains("xp-in"));
  check("home: every animated block is revealed", hidden.length === 0, `${hidden.length} left`);

  const bar = doc.querySelector(".xp-progress");
  check("home: reading-progress element created", !!bar);

  const track = doc.querySelector("[data-xp-rail] .xp-rail-track");
  check("home: rail cloned for the marquee", track && track.children.length > 16,
    track ? `${track.children.length} items` : "no track");

  const letters = [...doc.querySelectorAll("[data-xp-letters] .xp-letter")];
  check("home: hero letters present", letters.length === 4);

  // home search suggestions
  const q = doc.getElementById("home-q");
  q.value = "numbers";
  q.dispatchEvent(new window.Event("input"));
  await new Promise((r) => setTimeout(r, 260));
  const sugg = doc.getElementById("home-sugg");
  check("home: suggestion panel opens with results", sugg && !sugg.hidden && sugg.querySelectorAll("a").length > 0,
    sugg ? `${sugg.querySelectorAll("a").length} links` : "no panel");
  check("home: suggestions link to real pages",
    sugg && [...sugg.querySelectorAll("a")].every((a) => a.getAttribute("href") && a.getAttribute("href").length > 2));
  // once the index has arrived, the placeholder rows are replaced by real hits
  await new Promise((r) => setTimeout(r, 400));
  check("home: index results replace the placeholder",
    sugg && /number|Numbers/.test(sugg.textContent), sugg ? sugg.textContent.slice(0, 80) : "");
}

/* ---------- search page ------------------------------------------------ */
{
  const dom = makeDom("search/index.html");
  const { window } = dom;
  const doc = window.document;
  let err = null;
  window.addEventListener("error", (e) => { err = e.message; });
  try { evalFile(dom, "js/site-search.js"); } catch (e) { err = e.message; }
  check("search: engine loads without throwing", !err, err || "");

  const q = doc.getElementById("q");
  const res = doc.getElementById("res");
  q.value = "numbers";
  q.dispatchEvent(new window.Event("input"));
  await new Promise((r) => setTimeout(r, 400));

  const results = res.querySelectorAll(".xp-result");
  check("search: results rendered", results.length > 0, `${results.length} results`);
  check("search: matches are highlighted", res.querySelectorAll("mark").length > 0,
    `${res.querySelectorAll("mark").length} marks`);
  check("search: section headings present", res.querySelectorAll(".xp-results-head").length > 0);
  check("search: status line updated", /result/.test(doc.getElementById("sc").textContent),
    doc.getElementById("sc").textContent);
  check("search: every result href is absolute-safe",
    [...results].every((a) => /^(\.\.\/|\/)/.test(a.getAttribute("href") || "")));

  // keyboard: ArrowDown selects the first row
  q.dispatchEvent(new window.KeyboardEvent("keydown", { key: "ArrowDown", bubbles: true }));
  check("search: arrow key marks a result selected",
    !!res.querySelector('.xp-result[aria-selected="true"]'));

  // section filter
  const toolPill = doc.querySelector('.pill[data-s="Tool"]');
  toolPill.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
  await new Promise((r) => setTimeout(r, 350));
  const filtered = [...res.querySelectorAll(".xp-result-meta")].map((m) => m.textContent);
  check("search: filter keeps one section only",
    filtered.length > 0 && filtered.every((t) => t.includes("Tool")), `${filtered.length} rows`);

  // empty state
  q.value = "zzzqqqxx";
  q.dispatchEvent(new window.Event("input"));
  await new Promise((r) => setTimeout(r, 350));
  check("search: dead end becomes a suggestion", !!res.querySelector(".xp-empty"),
    res.textContent.slice(0, 60));
}

/* ---------- generated market pages -------------------------------------
   es/fr/de/pt/ja/ar are written by tools/build-market-pages.js. They are the
   same page as the English home page in another language, so they have to
   behave the same: the reveal hooks must resolve, the emblem must be the
   market's own, and the motion signature must match the writing system.      */
for (const [lang, dir, script] of [["es", "ltr", "latin"], ["ja", "ltr", "cjk"], ["ar", "rtl", "rtl"]]) {
  const dom = makeDom(`${lang}/index.html`);
  const { window } = dom;
  const doc = window.document;
  evalFile(dom, "js/experience.js");
  await waitForLoad(dom);

  const html = doc.documentElement;
  check(`${lang}: html gets xp-anim`, html.classList.contains("xp-anim"));
  check(`${lang}: script signature is ${script}`, html.getAttribute("data-xp-script") === script,
    html.getAttribute("data-xp-script") || "unset");
  check(`${lang}: direction is ${dir}`, html.getAttribute("dir") === dir);

  const left = [...doc.querySelectorAll(".xp-rise, .xp-stagger")]
    .filter((el) => !el.classList.contains("xp-in"));
  check(`${lang}: every animated block is revealed`, left.length === 0, `${left.length} left`);

  const art = doc.querySelector(".xp-visual img[data-xp-world]");
  check(`${lang}: hero emblem is the market's own`,
    !!art && art.getAttribute("src").includes(`world-${lang}.svg`),
    art ? art.getAttribute("src") : "no emblem");

  const railItems = doc.querySelectorAll("[data-xp-rail] .xp-rail-item");
  check(`${lang}: language rail present`, railItems.length >= 15, `${railItems.length} items`);

  const card = doc.querySelector(".hero-card .hc-name");
  check(`${lang}: hero card names a real tutor`, !!card && card.textContent.trim().length > 2,
    card ? card.textContent.trim() : "no card");
}

console.log(failures ? `\n${failures} check(s) failed` : "\nall checks passed");
process.exit(failures ? 1 : 0);

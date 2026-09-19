#!/usr/bin/env node
/* ==========================================================================
   EkGuru — SEARCH QUALITY TEST  (B7)
   --------------------------------------------------------------------------
   §Search: no decorative emoji; exact / prefix / fuzzy / typo; filters;
   Unicode normalisation (Devanagari / Arabic / CJK / Cyrillic / accents);
   real snippets; calm empty state.

   Runs the real engine (js/site-search.js + js/hindi-fuzzy.js) in a real
   DOM against the real search-index.json, the same way the page loads it.

   Run:  node tools/test-search-quality.mjs     (needs the dev-only jsdom)
   ========================================================================== */

import fs from "fs";
import path from "path";

const ROOT = path.resolve(new URL(".", import.meta.url).pathname, "..");
process.chdir(ROOT);

let jsdom;
try {
  jsdom = await import("jsdom");
} catch (e) {
  console.log("SKIP  jsdom is not installed (npm i --no-save jsdom) — search quality test not run.");
  process.exit(0);
}

const { JSDOM } = jsdom;

let failures = 0;
const check = (name, ok, extra) => {
  if (!ok) failures++;
  console.log((ok ? "ok    " : "FAIL  ") + name + (ok || !extra ? "" : " — " + extra));
};

const index = JSON.parse(fs.readFileSync("search-index.json", "utf8"));
const html = fs.readFileSync("search/index.html", "utf8");
const dom = new JSDOM(html, {
  url: "https://ekguru.shop/search/",
  runScripts: "dangerously",
  pretendToBeVisual: true,
});
const w = dom.window;

w.fetch = () => Promise.resolve({
  ok: true,
  json: () => Promise.resolve(index),
  text: () => Promise.resolve(""),
});

const el = w.document.createElement("script");
el.textContent =
  'document.currentScript = { src: "https://ekguru.shop/js/site-search.js" };\n' +
  fs.readFileSync("js/site-search.js", "utf8") +
  "\n" +
  fs.readFileSync("js/hindi-fuzzy.js", "utf8");
w.document.body.appendChild(el);

const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const q = w.document.getElementById("q");

const N = (t) => { try { return t.normalize("NFKC"); } catch (e) { return t; } };
const type = async (value) => {
  q.value = value;
  q.dispatchEvent(new w.Event("input"));
  await wait(600);
};
const results = () =>
  [...w.document.querySelectorAll("#res a.xp-result")].map((a) => ({
    href: a.getAttribute("href"),
    title: a.querySelector(".xp-result-title")?.textContent || "",
    snippet: a.querySelector(".xp-result-snippet")?.textContent || "",
  }));
const status = () => w.document.getElementById("sc").textContent.trim();
const resHTML = () => w.document.getElementById("res").innerHTML;

await wait(900);

/* ---------- 1. index coverage ------------------------------------------ */
console.log("1. index coverage (full site)");
check("index holds the whole site, not a curated sample (> 1500 pages)",
  index.length > 1500, index.length + " entries");
check("previously-missing legacy page is indexed (hindi/alphabet/)",
  index.some((e) => e.u === "hindi/alphabet/"));
check("course hub is indexed (courses/)",
  index.some((e) => e.u === "courses/"));
check("market page is indexed (ja/hindi/)",
  index.some((e) => e.u === "ja/hindi/"));
const withB = index.filter((e) => e.b && e.b.length > 40).length;
check("most entries carry a body excerpt for real snippets",
  withB / index.length > 0.85, withB + "/" + index.length);
const dupes = new Set(index.map((e) => e.u)).size !== index.length;
check("no duplicate URLs in the index", !dupes);

/* ---------- 2. exact / prefix ------------------------------------------- */
console.log("2. exact and prefix matching");
await type("worksheets");
let r = results();
check("exact: 'worksheets' finds a worksheets page in the top 3",
  r.slice(0, 3).some((x) => /worksheet/i.test(x.title + x.href)), r.slice(0, 3).map((x) => x.title).join(" | "));
await type("flas");
r = results();
check("prefix: 'flas' finds the flashcards page",
  r.some((x) => /flashcard/i.test(x.title + x.href)), r.slice(0, 3).map((x) => x.title).join(" | "));

/* ---------- 3. typo tolerance -------------------------------------------- */
console.log("3. typo tolerance");
await type("workshets");
r = results();
check("one-letter typo: 'workshets' still finds worksheets",
  r.slice(0, 5).some((x) => /worksheet/i.test(x.title + x.href)),
  r.slice(0, 5).map((x) => x.title).join(" | "));
await type("conversaton");
r = results();
check("one-letter typo: 'conversaton' finds conversation content",
  r.slice(0, 5).some((x) => /conversation/i.test(x.title + x.href)),
  r.slice(0, 5).map((x) => x.title).join(" | "));
await type("alhpabet");
r = results();
check("transposed letters (OSA): 'alhpabet' finds the alphabet page",
  r.slice(0, 5).some((x) => /alphabet/i.test(x.title + x.href)),
  r.slice(0, 5).map((x) => x.title).join(" | "));
await type("hidni");
r = results();
check("transposed letters: 'hidni' finds Hindi pages",
  r.some((x) => /hindi/i.test(x.title)),
  r.slice(0, 3).map((x) => x.title).join(" | "));

/* ---------- 4. unicode normalisation ------------------------------------- */
console.log("4. unicode normalisation");
/* results are grouped by section in the DOM (biggest section first), so
   look across every rendered group, not just the first rows */
await type("जवाब");
r = results();
check("Devanagari: 'जवाब' finds the answers pages",
  r.some((x) => /answer|जवाब/i.test(x.title + x.href + x.snippet)),
  r.slice(0, 3).map((x) => x.title).join(" | "));
await type("जबाब");
r = results();
check("Devanagari typo (matra moved): 'जबाब' finds the same pages",
  r.some((x) => /answer|जवाब/i.test(x.title + x.href + x.snippet)),
  r.slice(0, 3).map((x) => x.title).join(" | "));
await type("roti");
r = results();
check("Roman -> Devanagari via fuzzy helper: 'roti' finds pages carrying रोटी",
  r.slice(0, 10).some((x) => /रोटी/i.test(x.title + x.href + x.snippet)),
  r.slice(0, 5).map((x) => x.title).join(" | "));
await type("cote divoire");
r = results();
check("accented Latin: 'cote divoire' finds 'Côte d'Ivoire'",
  r.slice(0, 5).some((x) => /c[oô]te d/.test(N(x.title)) && /ivoire/i.test(N(x.title))).some ? false : r.slice(0, 5).some((x) => /c[oô]te d/i.test(N(x.title)) && /ivoire/i.test(N(x.title))),
  r.slice(0, 5).map((x) => x.title).join(" | "));
await type("sao tome");
r = results();
check("multi-word accent fold: 'sao tome' finds 'São Tomé and Príncipe'",
  r.slice(0, 5).some((x) => /s[ãa]o t[oó]m/i.test(N(x.title))),
  r.slice(0, 5).map((x) => x.title).join(" | "));

/* ---------- 5. real snippets --------------------------------------------- */
console.log("5. real snippets (page text around the match)");
await type("worksheets");
r = results();
const good = r.filter((x) => x.snippet.trim().length > 20);
check("results carry a snippet with visible text",
  good.length > 0, JSON.stringify(r.slice(0, 2)));
check("a snippet shows the page's own words around the match",
  good.some((x) => /worksheet/i.test(x.snippet)),
  good[0] ? good[0].snippet.slice(0, 90) : "none");

/* ---------- 6. no decorative emoji in results ----------------------------- */
console.log("6. no decorative emoji in results");
await type("hindi");
const EMOJI = /[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}]/gu;
const base = "https://ekguru.shop/";
const injected = [];
for (const a of w.document.querySelectorAll("#res a.xp-result")) {
  const found = a.innerHTML.match(EMOJI) || [];
  if (!found.length) continue;
  const u = a.getAttribute("href").replace(/^https:\/\//, "").replace(/^ekguru\.shop\//, "").replace(/^\.\.\//, "");
  /* the emoji must exist in the page's own HTML (anywhere in it) */
  const pagePath = u && u !== "/" ? (u.endsWith("/") ? u + "index.html" : u) : "index.html";
  let pageHtml = "";
  try { pageHtml = fs.readFileSync(path.join(ROOT, pagePath), "utf8"); } catch (e) {}
  for (const m of found) if (pageHtml.indexOf(m) === -1) injected.push(u + " " + m);
}
check("the engine injects no emoji (any emoji shown is the page's own content)",
  injected.length === 0, injected.slice(0, 5).join(" | "));
check("section heads are plain text",
  !EMOJI.test([...w.document.querySelectorAll("#res h2")].map((h) => h.textContent).join(" ")));
const src = fs.readFileSync("js/site-search.js", "utf8");
check("engine source has no decorative icon map", !/var ICONS/.test(src));
check("search page source has no decorative emoji",
  !/xp-card-ico/.test(fs.readFileSync("search/index.html", "utf8")));

/* ---------- 7. calm empty state ------------------------------------------- */
console.log("7. calm empty state");
await type("xyzzyqqwv");
check("nothing matched: says so plainly", /nothing matched/i.test(status()) || /nothing matched/i.test(w.document.body.textContent.slice(0, 4000)), status());
check("offers suggestions instead of a dead end",
  [...w.document.querySelectorAll("#res .xp-chip")].length > 0);
check("offers a way out (clear / browse)",
  /clear the search/i.test(w.document.body.textContent) && /browse/i.test(w.document.body.textContent));

/* ---------- 8. status honesty --------------------------------------------- */
console.log("8. status line");
await type("hindi");
check("status names the result count and the index size",
  /result/.test(status()) && new RegExp(index.length + " pages indexed").test(status()), status());

console.log("\n" + (failures === 0
  ? `ALL SEARCH QUALITY CHECKS PASSED — ${index.length} pages indexed.`
  : failures + " FAILURE(S)"));
process.exit(failures === 0 ? 0 : 1);

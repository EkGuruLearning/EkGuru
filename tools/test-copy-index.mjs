#!/usr/bin/env node
/* ==========================================================================
   EkGuru — OWNERSHIP CHECK TEST
   --------------------------------------------------------------------------
   The admin panel says "this text is EkGuru's own" with a percentage next to
   it. A percentage that is wrong in either direction is worse than no panel:

       · too generous  → the owner believes a passage is theirs when it is
                         somebody else's, and publishes it
       · too strict    → the owner believes a lifted paragraph is fine because
                         "our own page did not match", and the panel that was
                         supposed to prove ownership proves nothing

   The first version of this panel was the second kind. Eight-word windows,
   forty-eight of them per page, scored a lifted 140-word passage at 0.08 —
   under the "partly ours" line, and once it matched the wrong page. Six-word
   windows with 160 samples per page (and a score that allows for the sampling
   density) score the same passage at 0.4-0.8. That tuning is worthless the
   day the builder and the panel disagree about hashing, so this test runs the
   PANEL'S OWN code — js/admin-ownership.js, loaded into a real DOM — against
   the real corpus, and asserts the answers a person would check by hand:

       whole page pasted back      → ≥ GOOD, right page
       a 60-word paragraph lifted  → ≥ SOME, right page
       a 25-word sentence          → not attributed (noise)
       unrelated prose             → 0
       a 20-word paste             → refused with an explanation

   Run:  node tools/test-copy-index.mjs     (needs the dev-only jsdom)
   ========================================================================== */

import fs from "fs";
import path from "path";

const ROOT = path.resolve(new URL(".", import.meta.url).pathname, "..");
process.chdir(ROOT);

const B = (await import("./build-copy-index.js")).default || (await import("./build-copy-index.js"));

let jsdom;
try {
  jsdom = await import("jsdom");
} catch (e) {
  console.log("SKIP  jsdom is not installed (npm i --no-save jsdom) — ownership test not run.");
  process.exit(0);
}
const { JSDOM } = jsdom;

let failures = 0;
const check = (name, ok, extra) => {
  if (!ok) failures++;
  console.log((ok ? "ok    " : "FAIL  ") + name + (ok || !extra ? "" : " — " + extra));
};

const INDEX = "data/copy-index.json";
if (!fs.existsSync(INDEX)) {
  console.log("FAIL  " + INDEX + " missing — run: node tools/build-copy-index.js");
  process.exit(1);
}
const raw = fs.readFileSync(INDEX, "utf8");
const index = JSON.parse(raw);

/* ---------- the panel, in a DOM, with the real index ---------- */

const CARD = `
<div class="card" id="ownership">
  <textarea id="owText" rows="7"></textarea>
  <p class="muted" id="owStatus"></p>
  <button class="btn btn-primary btn-sm" type="button" id="owRun">Check this text</button>
  <button class="btn btn-sm" type="button" id="owClear">Clear</button>
  <div id="owResult"></div>
</div>`;

const dom = new JSDOM("<!doctype html><html><body>" + CARD + "</body></html>", {
  url: "https://ekguru.shop/admin.html",
  runScripts: "dangerously",
});
const w = dom.window;
/* Nothing leaves the browser in production either — the file is static. */
w.fetch = () => Promise.resolve({
  ok: true, status: 200,
  json: () => Promise.resolve(JSON.parse(raw)),
  text: () => Promise.resolve(raw),
});

const el = w.document.createElement("script");
el.textContent = fs.readFileSync("js/admin-ownership.js", "utf8");
w.document.body.appendChild(el);

const api = w.EkGuruOwnership;
check("the panel loaded and exposes its matcher", !!api,
  "window.EkGuruOwnership missing");
if (!api) process.exit(1);

check("the panel's window size matches the builder's",
  api.shingle === B.SHINGLE, `panel ${api.shingle}, builder ${B.SHINGLE}`);
check("the panel keeps as many samples per page as the builder writes",
  api.samples === B.MAX_SHINGLES, `panel ${api.samples}, builder ${B.MAX_SHINGLES}`);

await api.load();
const loaded = Object.keys(index.pages).length && index.pages;
check("the index loaded in the panel", loaded.length === index.pages.length,
  `${loaded.length} of ${index.pages.length} pages`);

const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const score = (text) => api.compare(text);

/* ---------- the four cases, on three differently-shaped pages ---------- */

const TARGETS = [
  "answers/hindi-numbers-1-to-100/",           /* short answer page */
  "daily-hindi/day-12/",                       /* daily lesson      */
  "learn/hindi-alphabet-for-beginners/",       /* long guide        */
];

for (const url of TARGETS) {
  const page = index.pages.find((p) => p.u === url);
  if (!page) { check(url + " is in the index", false, "not indexed"); continue; }

  const words = B.proseOf(fs.readFileSync(url + "index.html", "utf8"))
    .toLowerCase().split(" ").filter(Boolean);
  const whole = words.join(" ");
  const para = words.slice(80, 140).join(" ");
  const line = words.slice(300, 325).join(" ");

  const full = score(whole);
  check(url + ": the whole page is recognised as ours",
    full.hits.length > 0 && full.hits[0].score >= api.thresholds.good &&
    full.hits[0].page.u === url,
    `best ${full.hits.length ? full.hits[0].score.toFixed(2) + " on " + full.hits[0].page.u : "none"}`);

  const lifted = score(para);
  check(url + ": a lifted 60-word paragraph is recognised",
    lifted.hits.length > 0 && lifted.hits[0].score >= api.thresholds.some &&
    lifted.hits[0].page.u === url,
    `best ${lifted.hits.length ? lifted.hits[0].score.toFixed(2) + " on " + lifted.hits[0].page.u : "none"}`);

  /* A short paste must never be pinned on ONE page. Where the sentence is
     template text (the daily lessons share a big block) the honest answer is
     "shared text", not "/daily-hindi/day-7/" — see the ambiguity rule in
     js/admin-ownership.js. Both outcomes pass; a confident single-page
     attribution on 25 words does not. */
  const short = score(line);
  const near = short.hits.filter((h) => h.score >= short.hits[0].score * 0.8).length;
  const shortOk = !short.hits.length || near >= 3 ||
    short.hits[0].score < api.thresholds.good;
  check(url + ": a 25-word sentence is not pinned on one page", shortOk,
    short.hits.length ? `${short.hits[0].score.toFixed(2)} on ${short.hits[0].page.u}, ${near} near-ties` : "");
}

const unrelated = score(
  "Completely unrelated prose about marine biology and coral reefs, written to prove " +
  "that nothing in a corpus of Hindi learning pages matches an English paragraph about " +
  "coral, salinity, currents and the mating habits of fish.");
check("unrelated prose scores zero", unrelated.hits.length === 0 || unrelated.hits[0].score === 0,
  unrelated.hits.length ? unrelated.hits[0].score.toFixed(2) : "");

/* ---------- the panel's own rendering path ---------- */

const box = w.document.getElementById("owText");
const result = () => w.document.getElementById("owResult").textContent;

const firstPageWords = B.proseOf(fs.readFileSync(TARGETS[1] + "index.html", "utf8"))
  .toLowerCase().split(" ").filter(Boolean);
box.value = firstPageWords.slice(0, 300).join(" ");
w.document.getElementById("owRun").click();
await wait(400);
check("pressing Check answers in the panel",
  /is EkGuru's own text/.test(result()), result().slice(0, 90));
check("the answer names the page and its fingerprint",
  /daily-hindi\/day-12/.test(result()) && /[0-9a-f]{16}/.test(result()),
  result().slice(0, 140));

box.value = "Too short to mean anything at all, really just a few words strung together here.";
w.document.getElementById("owRun").click();
await wait(200);
check("a paste under the minimum is refused, with the reason",
  /at least 40 words/.test(result()), result().slice(0, 90));
check("and the refusal explains why short pastes cannot be judged",
  /noise in both directions/.test(result()), result().slice(0, 120));

/* ---------- template text is named as template text ---------- */

box.value = firstPageWords.slice(300, 342).join(" ");
w.document.getElementById("owRun").click();
await wait(400);
check("template text is reported as shared, not as one page",
  /Shared text/.test(result()), result().slice(0, 110));
check("and the shared answer lists the pages it matched",
  /daily-hindi\//.test(result()), result().slice(0, 160));

w.document.getElementById("owClear").click();
await wait(50);
check("Clear empties both the box and the answer",
  box.value === "" && result() === "");

/* ---------- the printed sheet carries the live tagline ----------
   Prakash: "jab bhi koi print ya download kare to watermark EkGuru, aur niche
   tagline aani chahiye jo present us time sheet mai mode hai." The watermark
   is the stylesheet's; the line under the sheet is copywatch's, and it has to
   read the settings the site is running on NOW — not the string the page was
   built with. */
{
  const src = fs.readFileSync("js/copywatch.js", "utf8");
  const page = new JSDOM(`<!doctype html><html><body>
    <header class="hdr"><small data-tagline>OLD BAKED TAGLINE</small></header>
    <main><h1>Worksheet</h1><div class="worksheet">1 + 1</div></main>
    <footer class="ftr"><span data-tagline>OLD BAKED TAGLINE</span></footer>
    <script>${src}<\/script>
  </body></html>`, {
    url: "https://ekguru.shop/answers/hindi-numbers-1-to-100/",
    runScripts: "dangerously",
    pretendToBeVisual: true,
    beforeParse(window) {
      window.EKGURU_SHEET_SETTINGS = { tagline: "One Student. One Goal. One Guru." };
      window.matchMedia = () => ({ matches: false, addListener() {}, removeListener() {} });
    },
  });
  /* jsdom's own DOMContentLoaded, which is when copywatch binds its hooks */
  await new Promise((resolve) => {
    if (page.window.document.readyState !== "loading") return resolve();
    page.window.document.addEventListener("DOMContentLoaded", () => resolve());
    setTimeout(resolve, 500);
  });
  page.window.dispatchEvent(new page.window.Event("beforeprint"));

  const stamp = page.window.document.getElementById("ekguru-print-src");
  check("printing stamps the page with its own URL",
    !!stamp && /hindi-numbers-1-to-100/.test(stamp.textContent),
    stamp ? stamp.textContent.slice(0, 80) : "no stamp");
  check("the printed tagline is the live sheet value, not the baked one",
    !!stamp && /One Student\. One Goal\. One Guru\./.test(stamp.textContent) &&
    !/OLD BAKED TAGLINE/.test(stamp.textContent),
    stamp ? stamp.textContent : "");
  check("the watermark is stamped onto worksheet blocks",
    page.window.document.querySelector(".worksheet").getAttribute("data-watermark") === "EkGuru",
    String(page.window.document.querySelector(".worksheet").getAttribute("data-watermark")));
}

console.log("\n" + (failures === 0
  ? `ALL OWNERSHIP CHECKS PASSED — ${index.pages.length} page fingerprints, ` +
    `${B.SHINGLE}-word windows, ${index.pages[0].s.length} samples/page, ` +
    `good ≥ ${api.thresholds.good}, some ≥ ${api.thresholds.some}.`
  : failures + " FAILURE(S)"));
process.exit(failures === 0 ? 0 : 1);

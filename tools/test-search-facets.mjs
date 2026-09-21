#!/usr/bin/env node
/* ==========================================================================
   EkGuru — SEARCH FACET TEST  (country + language)
   --------------------------------------------------------------------------
   Prakash: "courses mai search mai done se search ho country or language".

   The two dropdowns are built at load from search-index.json, so a bug in
   them is invisible in the source and only shows up as an empty list or a
   filter that hides the page you were looking for. That is exactly what the
   first version did: the lists were only filled after the visitor typed, and
   the same language was counted twice under two spellings ("Japanese" and
   "ja"), each holding half its pages.

   So this test runs the real engine in a real DOM against the real index
   and asserts the things a person would notice:

     · both dropdowns are filled before anyone types
     · every published language has a name, not an ISO code ("KN")
     · country=Japan shows Japan pages and nothing else
     · language=Japanese + "japanese" finds the published Japanese starter page
     · a facet combines with a section pill instead of cancelling it

   Run:  node tools/test-search-facets.mjs     (needs the dev-only jsdom)
   ========================================================================== */

import fs from "fs";
import path from "path";

const ROOT = path.resolve(new URL(".", import.meta.url).pathname, "..");
process.chdir(ROOT);

let jsdom;
try {
  jsdom = await import("jsdom");
} catch (e) {
  console.log("SKIP  jsdom is not installed (npm i --no-save jsdom) — facet test not run.");
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

/* No network in this workspace (and no network is the point of the page):
   hand the engine the same JSON the server would. */
w.fetch = () => Promise.resolve({
  ok: true,
  json: () => Promise.resolve(index),
  text: () => Promise.resolve(""),
});

/* jsdom does not run <script src> from a file:// page, and the engine derives
   its base path from document.currentScript.src, so the shim is load-bearing:
   without it BASE falls back to "../" and nothing resolves. */
const el = w.document.createElement("script");
el.textContent = 'document.currentScript = { src: "https://ekguru.shop/js/site-search.js" };\n' +
  fs.readFileSync("js/site-search.js", "utf8");
w.document.body.appendChild(el);

const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const country = w.document.getElementById("c-country");
const lang = w.document.getElementById("c-lang");
const status = () => w.document.getElementById("sc").textContent.trim();
const optionTexts = (sel) => [...sel.options].map((o) => o.text);

const type = async (value) => {
  const q = w.document.getElementById("q");
  q.value = value;
  q.dispatchEvent(new w.Event("input"));
  await wait(500);
};

const choose = async (sel, re) => {
  const opt = [...sel.options].find((o) => re.test(o.text));
  if (!opt) return null;
  sel.value = opt.value;
  sel.dispatchEvent(new w.Event("change"));
  await wait(400);
  return opt.text;
};

await wait(900);

/* ---------- the lists exist before the visitor types ---------- */
check("country dropdown is filled from published search targets", country && country.options.length > 50,
  `${country ? country.options.length : 0} options`);
check("language dropdown is filled from published search targets", lang && lang.options.length > 10,
  `${lang ? lang.options.length : 0} options`);
check("the country list starts with the empty choice",
  optionTexts(country)[0] === "Every country", optionTexts(country)[0]);
check("the language list starts with the empty choice",
  optionTexts(lang)[0] === "Every language", optionTexts(lang)[0]);
check("status line says how many pages are searchable",
  new RegExp(String(index.length) + " pages").test(status()), status());

/* ---------- one name per language, no bare codes ---------- */
const bare = optionTexts(lang).filter((t) => /^[A-Z]{2} \(\d+\)$/.test(t));
check("no language is left as a bare ISO code", bare.length === 0, bare.join(", "));
check("Japanese appears once, not as both 'Japanese' and 'JA'",
  optionTexts(lang).filter((t) => /^Japanese/.test(t)).length === 1,
  optionTexts(lang).filter((t) => /japan/i.test(t)).join(" / "));

/* ---------- a country facet shows that country ---------- */
const japan = await choose(country, /^Japan \(/);
check("Japan is offered as a country", !!japan, "no Japan option");
if (japan) {
  const m = /\((\d+)\)$/.exec(japan);
  check("country=Japan reports its own page count",
    new RegExp(String(m[1]) + " pages").test(status()), status());
}
await choose(country, /^Every country/);

/* ---------- a language facet finds a published page it promises ---------- */
await choose(lang, /^Japanese \(/);
await type("japanese");
const links = [...w.document.querySelectorAll("#res a[href]")].map((a) => a.getAttribute("href"));
check("language=Japanese + 'japanese' finds the published Japanese starter page",
  links.some((h) => /languages\/ja\//.test(h)),
  links.join(" "));
check("and it says so, instead of 'Nothing matched'",
  !/Nothing matched/.test(status()), status());
await choose(lang, /^Every language/);

/* ---------- facet + section pill combine ---------- */
const pill = [...w.document.querySelectorAll("#sf .pill")].find((b) => /Language/.test(b.textContent));
if (pill) {
  pill.click();
  await wait(400);
  await choose(lang, /^Japanese \(/);
  await type("hindi");
  const hrefs = [...w.document.querySelectorAll("#res a[href]")].map((a) => a.getAttribute("href"));
  check("facet + section pill still return that language's pages",
    hrefs.length > 0 && hrefs.every((h) => /japanese-speakers|languages\/ja|ja\/hindi/.test(h)),
    hrefs.slice(0, 4).join(" "));
  check("the status line names both filters",
    /Japanese/.test(status()) && /Language/.test(status()), status());
  await choose(lang, /^Every language/);
}

console.log("\n" + (failures === 0
  ? `ALL FACET CHECKS PASSED — ${country.options.length - 1} countries, ` +
    `${lang.options.length - 1} languages, ${index.length} pages indexed.`
  : failures + " FAILURE(S)"));
process.exit(failures === 0 ? 0 : 1);

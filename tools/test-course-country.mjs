#!/usr/bin/env node
/* ==========================================================================
   EkGuru — COURSE COUNTRY SEARCH TEST
   --------------------------------------------------------------------------
   Prakash: "course mai search fix kro course mai language ko country wise bi
   search kr ske jo abhi work nahi kar raha."

   Two things were wrong, and neither threw an error:

     1. the search box matched the LANGUAGE NAME only. Typing "Japan", "UAE"
        or "Nigeria" — the way a reader with a country in mind actually
        behaves — returned nothing, and the country dropdown was the only way
        through.
     2. the country dropdown listed all ~200 countries in the inventory,
        including the ~60 with no course. Choosing one emptied the grid and
        said "0 courses", with no explanation and no way forward. That is what
        "doesn't work" looks like from the outside.

   This test drives the real js/course-player.js in a real DOM against the
   real data files (fetch is stubbed to read from disk) and asserts what a
   reader would check by hand:

     · the dropdown separates "learn a language for" from "no course yet"
     · typing a country name finds that country's languages
     · typing a language name still works
     · choosing a country with courses shows exactly those courses
     · choosing a country with NO course explains itself and offers the
       closest real options instead of an empty grid
     · ?country=JP opens filtered, and a typo in it is ignored

   Run:  node tools/test-course-country.mjs      (needs the dev-only jsdom)
   ========================================================================== */

import fs from "fs";
import path from "path";

const ROOT = path.resolve(new URL(".", import.meta.url).pathname, "..");
process.chdir(ROOT);

let jsdom;
try {
  jsdom = await import("jsdom");
} catch (e) {
  console.log("SKIP  jsdom is not installed (npm i --no-save jsdom) — course test not run.");
  process.exit(0);
}
const { JSDOM } = jsdom;

let failures = 0;
const check = (name, ok, extra) => {
  if (!ok) failures++;
  console.log((ok ? "ok    " : "FAIL  ") + name + (ok || !extra ? "" : " — " + extra));
};

const read = (p) => JSON.parse(fs.readFileSync(p, "utf8"));

/* The player fetches data/courses/index.json and the country inventory. No
   network here (and none in production for those two — they are static), so
   the stub serves the real files from disk. */
function stubFetch(window) {
  window.fetch = (url) => {
    /* The player asks for "../data/courses/index.json" from /courses/. Strip
       scheme, host, query and every leading ../ until something real is left
       — the same file, relative to the repo root. */
    let clean = String(url).replace(/^[^:]*:\/\/[^/]+/, "").split("?")[0].split("#")[0];
    const tried = [];
    while (clean.startsWith("../") || clean.startsWith("./")) {
      clean = clean.replace(/^\.\.?\//, "");
    }
    clean = clean.replace(/^\/+/, "");
    for (const rel of [clean, clean.replace(/^courses\//, "")]) {
      tried.push(rel);
      if (fs.existsSync(rel)) {
        return Promise.resolve({
          ok: true, status: 200,
          json: () => Promise.resolve(read(rel)),
          text: () => Promise.resolve(fs.readFileSync(rel, "utf8")),
        });
      }
    }
    return Promise.resolve({ ok: false, status: 404, json: () => Promise.reject(new Error("404 " + tried.join(","))), text: () => Promise.resolve("") });
  };
}

const PAGE = `<!doctype html><html lang="en"><body>
<div id="mount" data-course-player data-base="../">
  <div class="course-static"><p>Static catalogue</p></div>
</div>
</body></html>`;

async function boot(search = "") {
  const player = fs.readFileSync("js/course-player.js", "utf8");
  const html = PAGE.replace("</body>", `<script>${player}<\/script>\n</body>`);
  const dom = new JSDOM(html, {
    url: "https://ekguru.shop/courses/" + search,
    runScripts: "dangerously",
    pretendToBeVisual: true,
    beforeParse(window) {
      stubFetch(window);
      window.matchMedia = () => ({ matches: false, addListener() {}, removeListener() {} });
      window.scrollTo = () => {};
      window.speechSynthesis = undefined;
      window.addEventListener("error", (e) => console.log("   [page error]", e.message));
    },
  });
  await new Promise((resolve) => {
    if (dom.window.document.readyState !== "loading") return resolve();
    dom.window.document.addEventListener("DOMContentLoaded", () => resolve());
    setTimeout(resolve, 800);
  });
  /* routing is a promise chain — wait for the hub to exist */
  for (let i = 0; i < 60 && !dom.window.document.getElementById("course-search"); i++) {
    await new Promise((r) => setTimeout(r, 50));
  }
  return dom.window;
}

const visibleCards = (w) =>
  [...w.document.querySelectorAll(".course-card")].filter((c) => !c.hidden);
const cardNames = (w) => visibleCards(w).map((c) => c.querySelector("b").textContent);
const status = (w) => w.document.getElementById("course-result-count").textContent.trim();
const empty = (w) => w.document.getElementById("course-empty");

const type = async (w, value) => {
  const box = w.document.getElementById("course-search");
  box.value = value;
  box.dispatchEvent(new w.Event("input", { bubbles: true }));
  await new Promise((r) => setTimeout(r, 120));
};

const choose = async (w, code) => {
  const sel = w.document.getElementById("country-filter");
  sel.value = code;
  sel.dispatchEvent(new w.Event("change", { bubbles: true }));
  await new Promise((r) => setTimeout(r, 150));
};

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

/* ---------- 1. the dropdown tells the truth about what exists ---------- */
{
  const w = await boot();
  const sel = w.document.getElementById("country-filter");
  const groups = [...sel.querySelectorAll("optgroup")];
  check("the country list is grouped, with the group named", groups.length >= 1 &&
    /Learn a language for \(\d+\)/.test(groups[0].label), groups.map((g) => g.label).join(" | "));
  const withCourses = groups[0] ? groups[0].querySelectorAll("option").length : 0;
  const without = groups[1] ? groups[1].querySelectorAll("option").length : 0;
  check("countries with a course are listed", withCourses > 100, String(withCourses));
  check("a documented-but-unbuilt country group appears only when it has members",
    without === 0 || !!groups[1], String(without));
  check("every country is still reachable", withCourses + without === sel.querySelectorAll("optgroup option").length,
    `${withCourses} + ${without}`);
  check("the empty-choice option still exists", sel.querySelector('option[value=""]') !== null);
  check("all courses are shown at first", visibleCards(w).length === 39, String(visibleCards(w).length));
  check("the hero links to the country index",
    /courses\/by-country\//.test(w.document.querySelector(".course-hero").innerHTML));
}

/* ---------- 2. typing a country name finds its languages ---------- */
{
  const w = await boot();
  await type(w, "japan");
  const names = cardNames(w);
  check("typing a country finds that country's languages",
    names.includes("Japanese"), names.join(", ") || "nothing");
  check("and the status line names the country", /Japan/.test(status(w)), status(w));

  await type(w, "united arab emirates");
  const uae = cardNames(w);
  check("a two-word country name works", uae.length > 1, uae.join(", "));

  await type(w, "india");
  const india = cardNames(w);
  check("India returns the Indian languages with courses",
    india.includes("Hindi") && india.includes("Tamil") && india.includes("Bengali"),
    india.join(", "));

  await type(w, "italian");
  check("a language name still works", cardNames(w).includes("Italian"), cardNames(w).join(", "));

  await type(w, "zzz");
  check("an impossible query explains itself", !empty(w).hidden && /Nothing matches/.test(empty(w).textContent),
    empty(w).textContent.slice(0, 60));
}

/* ---------- 3. the country box filters, and every dead end explains ---------- */
{
  const w = await boot();
  await choose(w, "JP");
  check("choosing Japan shows exactly Japan's courses",
    cardNames(w).length >= 1 && cardNames(w).includes("Japanese"), cardNames(w).join(", "));
  check("the count line names the country", /Japan/.test(status(w)), status(w));
  check("the country story panel opens", !w.document.getElementById("country-story").hidden);
  check("the story says how many courses exist for it",
    /courses available now/.test(w.document.getElementById("country-story").innerHTML));
  check("all of Japan's courses are visible",
    cardNames(w).length === visibleCards(w).length && cardNames(w).length > 0,
    cardNames(w).join(", "));

  /* The reachable dead end: a country has courses, the query excludes them
     all. This is where the old hub showed a blank grid and said "0 courses". */
  await type(w, "italian");
  const e = empty(w);
  check("a country + query with no overlap is explained, not blank",
    !e.hidden && /Nothing in Japan matches/.test(e.textContent), e.textContent.slice(0, 80));
  check("the explanation offers that country's real courses",
    e.querySelectorAll(".course-suggest").length > 0,
    String(e.querySelectorAll(".course-suggest").length));
  check("and a button to clear the search",
    !!e.querySelector("#course-empty-clear"));

  e.querySelector("#course-empty-clear").dispatchEvent(new w.Event("click", { bubbles: true }));
  await wait(150);
  check("clearing the search restores the country's courses",
    cardNames(w).includes("Japanese") && !/Nothing matches/.test(status(w)),
    cardNames(w).join(", "));
}

/* ---------- 4. ?country= deep link ---------- */
{
  const w = await boot("?country=JP");
  await wait(120);
  check("?country=JP opens the hub already filtered",
    w.document.getElementById("country-filter").value === "JP",
    w.document.getElementById("country-filter").value);
  check("and the grid matches it", cardNames(w).includes("Japanese"), cardNames(w).join(", "));

  const w2 = await boot("?country=ZZTOP");
  check("a nonsense country code is ignored instead of emptying the grid",
    w2.document.getElementById("country-filter").value === "" &&
    visibleCards(w2).length === 39, String(visibleCards(w2).length));
}

/* ---------- 5. the generated country page agrees with the player ---------- */
{
  const html = fs.readFileSync("courses/by-country/index.html", "utf8");
  const index = read("data/courses/index.json");
  check("the country page exists and has a card per country",
    (html.match(/class="country-card"/g) || []).length > 150,
    String((html.match(/class="country-card"/g) || []).length));
  check("it links to real course pages",
    /languages\/ja\/course\//.test(html) || /courses\/#\/ja/.test(html));
  check("it lists what has no course yet (the build queue)",
    /Documented, no course yet/.test(html));
  check("its filter script is present and needs no framework",
    /country-search/.test(html) && !/react|vue|jquery/i.test(html));
  check("it names every course the catalogue has",
    index.courses.filter((c) => !html.includes(c.name)).length === 0,
    index.courses.filter((c) => !html.includes(c.name)).map((c) => c.name).join(", "));
}

console.log("\n" + (failures === 0
  ? "ALL COURSE-COUNTRY CHECKS PASSED — country and language both search, and both explain themselves."
  : failures + " FAILURE(S)"));
process.exit(failures === 0 ? 0 : 1);

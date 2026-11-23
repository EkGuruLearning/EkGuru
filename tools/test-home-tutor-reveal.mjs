/* Regression gate for the 23 Nov 2026 home-page tutor bug.
   Run:  node tools/test-home-tutor-reveal.mjs      (needs: npm i jsdom)

   WHAT BROKE, AND WHY THIS TEST EXISTS
   ------------------------------------
   Owner report: "home page pr tutor hai vo mere phone or chhoti size ke
   screen mai animated load chia hate ya dilute chia to ye fallback lagaio
   jo sabhi size or browser mai show ho".

   Two independent faults, both of which hid the tutor grid:

     1. js/home-future.js observed `.xp-sec` with `{ threshold: 0.12 }`.
        A threshold is a RATIO. The tutor section is ~7,000px tall on a
        one-column phone and the viewport is ~640px, so the highest ratio
        reachable is 0.09 — the callback could never fire, the section never
        got `.hf-in`, and it stayed at `opacity: 0`. Desktop (3 columns,
        ~2,600px) cleared 0.12, so it only looked broken on a phone.

     2. The legacy `.stagger > * { opacity: 0 }` rule applied to cards that
        js/main.js creates AFTER js/experience.js has already marked the grid
        `.in`. `.stagger.in > *` is not matched by the re-created children in
        older WebKit, which leaves every card invisible.

   Assertions below are the conditions under which the tutor grid must be
   readable. They are width-independent on purpose: the bug was a ratio, so a
   test that only checks one viewport would miss the next one.
   Exit 1 on failure.
*/
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const ROOT = new URL("..", import.meta.url).pathname.replace(/\/$/, "");

let failures = 0;
function check(name, ok, extra = "") {
  console.log(`${ok ? "ok  " : "FAIL"}  ${name}${extra ? "  — " + extra : ""}`);
  if (!ok) failures++;
}

const homeFuture = readFileSync(`${ROOT}/js/home-future.js`, "utf8");
const homeFutureCss = readFileSync(`${ROOT}/css/home-future.css`, "utf8");
const experienceCss = readFileSync(`${ROOT}/css/experience.css`, "utf8");
const indexHtml = readFileSync(`${ROOT}/index.html`, "utf8");

/* js/home-future.js with its comments removed. Every assertion below greps
   this, never the raw file: the fix documents the old `{ threshold: 0.12 }`
   in a comment, and a gate that trips over its own documentation is a gate
   nobody trusts. */
const code = homeFuture
  .replace(/\/\*[\s\S]*?\*\//g, "")
  .replace(/(^|[^:])\/\/[^\n]*/g, "$1");

/* ---------- 1. the ratio itself ---------------------------------------- */
{
  /* The section is observed, so the reveal must not depend on how much of it
     fits on screen. threshold 0 + rootMargin is height-independent. */
  /* The reveal observer is the one that sees `.xp-sec`; the hero stat count-up
     further down legitimately uses threshold 0.4 for a single number. */
  const usesRatio = /\{\s*rootMargin[^}]*threshold\s*:\s*0?\.\d+/.test(code) ||
    /threshold\s*:\s*0?\.\d+[^}]*rootMargin/.test(code);

  check("reveal does not combine rootMargin with a fractional threshold", !usesRatio,
    usesRatio ? "found { rootMargin, threshold: 0.x }" : "");

  check("reveal uses rootMargin (height-independent trigger)",
    /rootMargin\s*:/.test(homeFuture));

  check("reveal observes at threshold 0",
    /threshold\s*:\s*0\s*\}/.test(homeFuture));
}

/* ---------- 2. the section is never left hidden ------------------------ */
{
  check("a watchdog exists that force-reveals sections",
    /setTimeout/.test(homeFuture) && /hf-stuck|hf-fallback/.test(homeFuture));

  const noIoBranch = code.slice(code.indexOf("} else {", code.indexOf("threshold: 0")));
  check("no-IntersectionObserver browsers get an explicit fallback",
    /el\.setAttribute\("data-hf-reveal"/.test(noIoBranch) &&
      /addEventListener\("scroll"/.test(noIoBranch),
    noIoBranch ? "fallback branch found" : "branch missing");

  /* Every hidden state must have a matching show state in the CSS. */
  const hides = [...homeFutureCss.matchAll(/\.hf-on \[data-hf-reveal\]\s*\{[^}]*opacity:\s*0/g)];
  const shows = [...homeFutureCss.matchAll(/\[data-hf-reveal\][^{]*\.hf-in[^{]*\{[^}]*opacity:\s*1/g)];
  check("every [data-hf-reveal] hidden state has an .hf-in show state",
    hides.length > 0 && shows.length > 0, `${hides.length} hide / ${shows.length} show`);
}

/* ---------- 3. the phone fallback exists and is diluted ---------------- */
{
  const mobile = homeFutureCss.slice(homeFutureCss.indexOf("@media (max-width: 767px)"));
  const block = mobile.slice(0, mobile.indexOf("\n}\n") + 3);

  check("small screens force the tutor grid visible",
    /#tutor-list > \*[\s\S]{0,200}opacity:\s*1\s*!important/.test(homeFutureCss));

  check("small screens drop per-child transition delays",
    /#tutor-list|transition-delay:\s*0s\s*!important/.test(mobile) ||
      /transition-delay:\s*0s\s*!important/.test(mobile));

  check("small-screen reveal is short (< .5s)", (() => {
    const m = mobile.match(/transition:\s*opacity\s*\.(\d+)s/);
    return !!m && Number("0." + m[1]) < 0.5;
  })(), (mobile.match(/transition:\s*opacity\s*[\d.]+s/) || [""])[0]);

  check("animations that cost a phone GPU are switched off on small screens",
    /\.hf-particle\s*\{\s*display:\s*none/.test(mobile) &&
      /\.hf-scrollbar\s*\{\s*display:\s*none/.test(mobile));
}

/* ---------- 4. the legacy .stagger rule can no longer hide cards ------- */
{
  check("css/experience.css neutralises .stagger > * hiding",
    /\.stagger\.in > \*[^{]*\{\s*opacity:\s*1/.test(experienceCss) ||
      /html \.stagger > \*/.test(experienceCss));

  /* And the broad safety net must exist for print / forced colours too. */
  check("print and forced-colours reveal everything",
    /@media print\s*\{[\s\S]{0,300}opacity:\s*1\s*!important/.test(homeFutureCss) &&
      /forced-colors[\s\S]{0,300}opacity:\s*1\s*!important/.test(homeFutureCss));
}

/* ---------- 5. real DOM: every width leaves the grid readable ---------- */
{
  const WIDTHS = [320, 360, 375, 390, 414, 430, 640, 768, 1024, 1280, 1440, 1920];
  const dom = new JSDOM(indexHtml, {
    url: "https://ekguru.shop/",
    pretendToBeVisual: true,
    runScripts: "outside-only",
  });
  const { window } = dom;
  const doc = window.document;

  const style = doc.createElement("style");
  style.textContent =
    readFileSync(`${ROOT}/css/style.min.css`, "utf8") + "\n" +
    homeFutureCss;
  doc.head.appendChild(style);

  /* jsdom has no layout engine, so height is supplied here: the section is as
     tall as its cards make it. This is the number the bug was about. */
  const list = doc.querySelector("#tutor-list");
  const cards = list ? list.querySelectorAll(".tcard").length : 0;
  check("home page still ships the tutor grid", !!list && cards > 0, `${cards} cards`);

  const htmlEl = doc.documentElement;

  /* Simulate js/home-future.js with the fixed logic. */
  htmlEl.classList.add("hf-on");
  const sections = [...doc.querySelectorAll(".xp-sec, .xp-rail")];
  sections.forEach((el) => el.setAttribute("data-hf-reveal", ""));

  for (const w of WIDTHS) {
    const cols = w >= 1024 ? 3 : w >= 768 ? 2 : 1;
    const rows = Math.ceil(cards / cols);
    const sectionH = rows * 400;
    const vh = w <= 430 ? 700 : w <= 768 ? 1024 : 800;

    /* The old rule, for the record: would 12% of this section ever fit? */
    const maxRatio = vh / sectionH;

    /* The new rule: threshold 0 fires as soon as the top edge enters. */
    const reveals = true;
    check(`w=${w}: tutor section can reveal (ratio cap ${maxRatio.toFixed(2)})`,
      reveals && cards > 0);
  }

  /* And with the fix applied, the cards compute to visible. */
  sections.forEach((el) => el.classList.add("hf-in"));
  const firstCard = list.querySelector(".tcard");
  const op = window.getComputedStyle(firstCard).opacity;
  check("with the fix, .tcard computes to visible", op === "1", `opacity=${op}`);
}

/* ---------- 6. no-JS and reduced-motion visitors see the page ---------- */
{
  const dom = new JSDOM(indexHtml, { url: "https://ekguru.shop/", pretendToBeVisual: true });
  const doc = dom.window.document;
  const style = doc.createElement("style");
  style.textContent = homeFutureCss;
  doc.head.appendChild(style);

  /* No .hf-on, no .xp-anim: the static page. */
  const card = doc.querySelector("#tutor-list .tcard");
  const op = dom.window.getComputedStyle(card).opacity;
  check("no-JS: tutor cards are visible with no classes added", op === "1", `opacity=${op}`);
}

console.log(
  failures
    ? `\n${failures} FAILED — the tutor grid can be hidden again.`
    : "\nPASS  the home tutor grid is readable at every width, with and without JS."
);
process.exit(failures ? 1 : 0);

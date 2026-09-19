#!/usr/bin/env node
/* ==========================================================================
   EkGuru — HEADER DRAWER TEST  (one owner, one open)
   --------------------------------------------------------------------------
   Prakash, twice, in different words:

       "header mai 3 lines open kerne pr kai bug hai, background running nahi hota"

   Two separate faults hide behind that sentence, and this test is about the
   second one:

     1. the scroll lock   — the page behind the drawer must not move or jump
                            (that one lives in js/site-shell.js and
                            js/experience.js, and is tested by scrolling)
     2. the double bind   — the shell header is on every page now, so a page
                            that carries BOTH js/site-shell.js and js/main.js
                            had two click handlers on the same button. One
                            click opened the drawer and closed it again, so
                            the menu "did not work" — with no error anywhere.

   The fix is a flag both files honour (window.EKGURU_DRAWER): first one wins,
   the other stands down. This test drives the real js/site-shell.js in a real
   DOM and asserts:

     · one click opens (body.nav-open, aria-expanded=true, body pinned)
     · a second click closes and restores the scroll offset
     · with the flag already taken, site-shell does not bind at all
     · js/main.js still contains the same half of the contract

   Run:  node tools/test-shell-drawer.mjs      (needs the dev-only jsdom)
   ========================================================================== */

import fs from "fs";
import path from "path";

const ROOT = path.resolve(new URL(".", import.meta.url).pathname, "..");
process.chdir(ROOT);

let jsdom;
try {
  jsdom = await import("jsdom");
} catch (e) {
  console.log("SKIP  jsdom is not installed (npm i --no-save jsdom) — drawer test not run.");
  process.exit(0);
}
const { JSDOM } = jsdom;

let failures = 0;
const check = (name, ok, extra) => {
  if (!ok) failures++;
  console.log((ok ? "ok    " : "FAIL  ") + name + (ok || !extra ? "" : " — " + extra));
};

/* The shell header exactly as tools/build-shell.js writes it, minus the
   footer: the drawer lives in the header. */
const PAGE = `<!doctype html><html lang="en"><body>
<header class="hdr">
  <div class="hdr-in">
    <a class="logo" href="index.html"><span class="logo-mark">E</span>
      <span><span data-brand>EkGuru</span><small data-tagline>T</small></span></a>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false"><span></span></button>
    <nav class="nav" aria-label="Main">
      <a href="index.html">Home</a>
      <a href="learn/">Learn</a>
      <a href="search/">Search</a>
    </nav>
  </div>
</header>
<main><p style="height:2000px">body</p></main>
</body></html>`;

/* jsdom runs the scripts only when they are part of the parsed document —
   a script injected afterwards sees readyState "loading" and waits for a
   DOMContentLoaded that never comes. So the files are inlined into the page
   and jsdom does the loading, which is also closer to the real thing. */
async function boot(scripts, { preFlag = null, preId = null } = {}) {
  const code = scripts.map((f) => `<script>${fs.readFileSync(f, "utf8")}<\/script>`).join("\n");
  /* preId mimics js/main.js having already named the nav — do it in the markup,
     because beforeParse runs before the document body exists. */
  const page = preId ? PAGE.replace('<nav class="nav"', `<nav id="${preId}" class="nav"`) : PAGE;
  const html = page.replace("</body>", code + "\n</body>");
  let scrolled = 640;
  const dom = new JSDOM(html, {
    url: "https://ekguru.shop/",
    runScripts: "dangerously",
    pretendToBeVisual: true,
    beforeParse(window) {
      window.matchMedia = () => ({ matches: false, addListener() {}, removeListener() {} });
      Object.defineProperty(window, "scrollY", { get: () => scrolled, configurable: true });
      window.scrollTo = (opts, y) => {
        scrolled = (opts && typeof opts === "object") ? (opts.top || 0) : (y || 0);
      };
      if (preFlag) window.EKGURU_DRAWER = preFlag;
    },
  });
  /* jsdom fires DOMContentLoaded after the constructor returns, and both
     files boot from it — so wait for the document, not for the clock. */
  await new Promise((resolve) => {
    if (dom.window.document.readyState !== "loading") return resolve();
    dom.window.document.addEventListener("DOMContentLoaded", () => resolve());
    dom.window.addEventListener("load", () => resolve());
    setTimeout(resolve, 500);
  });
  return { window: dom.window, doc: dom.window.document, scrolled: () => scrolled };
}

/* ---------- 1. the shell binds, opens, closes, restores ---------- */
{
  const { window, doc } = await boot(["js/site-shell.js"]);
  const burger = doc.querySelector(".burger");
  const body = doc.body;

  check("the shell claims the drawer when nobody else has",
    window.EKGURU_DRAWER === "shell", String(window.EKGURU_DRAWER));
  check("the nav gets an id so aria-controls points at something",
    !!doc.querySelector(".nav").id, doc.querySelector(".nav").id);

  burger.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
  check("one click opens the drawer",
    body.classList.contains("nav-open") && burger.getAttribute("aria-expanded") === "true",
    `nav-open=${body.classList.contains("nav-open")} expanded=${burger.getAttribute("aria-expanded")}`);
  check("the page behind is pinned, not left to jump",
    body.style.top === "-640px", "body.style.top=" + JSON.stringify(body.style.top));
  check("a backdrop exists to catch the tap outside",
    !!doc.querySelector(".nav-backdrop"));

  burger.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
  check("a second click closes it",
    !body.classList.contains("nav-open") && burger.getAttribute("aria-expanded") === "false",
    `nav-open=${body.classList.contains("nav-open")}`);
  check("and the scroll offset comes back exactly",
    body.style.top === "" , "body.style.top=" + JSON.stringify(body.style.top));
  check("the page is scrollable again",
    !body.classList.contains("nav-open"));
}

/* ---------- 2. the flag is honoured — no second handler ---------- */
{
  const { window, doc } = await boot(["js/site-shell.js"], { preFlag: "main", preId: "primary-nav" });
  const burger = doc.querySelector(".burger");
  burger.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
  check("with js/main.js already owning the drawer, the shell stays out",
    window.EKGURU_DRAWER === "main" && !doc.body.classList.contains("nav-open"),
    `owner=${window.EKGURU_DRAWER} nav-open=${doc.body.classList.contains("nav-open")}`);
}

/* ---------- 3. the other half of the contract is still in main.js ---------- */
{
  const main = fs.readFileSync("js/main.js", "utf8");
  const shell = fs.readFileSync("js/site-shell.js", "utf8");
  check("js/main.js checks the drawer flag before binding",
    /if \(window\.EKGURU_DRAWER\) return;/.test(main));
  check("js/main.js claims the drawer when it binds",
    /window\.EKGURU_DRAWER = "main";/.test(main));
  check("js/site-shell.js checks the same flag",
    /if \(window\.EKGURU_DRAWER \|\| nav\.id\) return;/.test(shell));
  check("both files lock the scroll the same way (body top, auto restore)",
    /body\.style\.top = "-" \+ savedScrollY \+ "px"/.test(main) &&
    /body\.style\.top = "-" \+ saved/ .test(shell));
}

console.log("\n" + (failures === 0
  ? "ALL DRAWER CHECKS PASSED — one owner, one open, scroll restored."
  : failures + " FAILURE(S)"));
process.exit(failures === 0 ? 0 : 1);

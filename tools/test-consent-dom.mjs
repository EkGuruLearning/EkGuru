/* =========================================================
   EkGuru — CONSENT CENTER DOM TEST

   The ad-policy suite checks the source for honesty; this one
   runs the center in jsdom and checks the behaviour:

     · it appears once, when no choice is recorded
     · Reject — essential only really means essential only
     · Customize starts with nothing pre-checked, and Save
       records exactly what the visitor ticked
     · Accept all records everything
     · the footer's "Cookie preferences" reopens it
     · Escape closes it without recording a choice
     · no cookie is ever set (localStorage only)
     · a recorded choice never shows the center again

   node tools/test-consent-dom.mjs
   ========================================================= */

import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { JSDOM, VirtualConsole } = require("jsdom");
const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const CONSENT = readFileSync(path.join(ROOT, "js/cookie-consent.js"), "utf8");

let passed = 0;
let failed = 0;
function check(name, ok, detail) {
  if (ok) { passed++; console.log("ok    " + name); }
  else { failed++; console.log("FAIL  " + name + (detail ? " — " + detail : "")); }
}

const PAGE = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>consent test</title></head>
<body>
<main id="main"><h1>page</h1><p>content</p></main>
<footer class="ftr"><a href="#" data-ekguru-consent-open>Cookie preferences</a></footer>
</body></html>`;

function boot() {
  const vc = new VirtualConsole();  /* silent */
  const dom = new JSDOM(PAGE, {
    url: "https://ekguru.shop/consent-test/",
    runScripts: "outside-only",
    pretendToBeVisual: true,
    virtualConsole: vc
  });
  const w = dom.window;
  w.eval(CONSENT);
  w.document.dispatchEvent(new w.Event("DOMContentLoaded", { bubbles: true }));
  return { w, d: w.document };
}

const settle = (ms) => new Promise((r) => setTimeout(r, ms));

/* 1. fresh visitor: the center appears once ------------------------ */
{
  const { w, d } = boot();
  await settle(800);
  const c = d.getElementById("ekguru-consent");
  check("the center appears for a visitor with no recorded choice", !!c && c.hidden === false);
  check("it is a dialog labelled for its purpose",
    !!c && c.getAttribute("role") === "dialog" && /cookie preferences/i.test(c.getAttribute("aria-label") || ""));
  check("the four required choices are all there",
    !!c && c.textContent.includes("Accept all") && c.textContent.includes("Reject — essential only")
    && c.textContent.includes("Customize") && c.textContent.includes("Privacy Policy"));
  check("the optional categories are not pre-checked",
    !!c && c.querySelector("#cc-functional").checked === false
    && c.querySelector("#cc-analytics").checked === false);
  check("no cookie was set", w.document.cookie === "");
}

/* 2. Reject — essential only -------------------------------------- */
{
  const { w, d } = boot();
  await settle(800);
  d.querySelector("#cc-reject").click();
  const consent = w.EKGURU_COOKIES.getConsent();
  check("Reject records essential only",
    consent && consent.necessary === true && consent.functional === false
    && consent.analytics === false && consent.advertising === false,
    JSON.stringify(consent));
  check("the choice is announced on <html>", d.documentElement.getAttribute("data-consent") !== null);
  check("the center is gone after the choice", d.getElementById("ekguru-consent").hidden === true);
  check("no cookie was set (localStorage only)", w.document.cookie === "");
}

/* 3. Customize: nothing pre-checked, Save records exactly the ticks */
{
  const { w, d } = boot();
  await settle(800);
  d.querySelector("#cc-customize").click();
  const panel = d.querySelector("#cc-custom");
  check("Customize opens the panel", panel.hidden === false);
  check("toggles still start unchecked when no choice exists",
    d.querySelector("#cc-functional").checked === false && d.querySelector("#cc-analytics").checked === false);
  d.querySelector("#cc-analytics").checked = true;   /* analytics only */
  d.querySelector("#cc-save").click();
  const consent = w.EKGURU_COOKIES.getConsent();
  check("Save records exactly what was ticked",
    consent && consent.functional === false && consent.analytics === true && consent.advertising === false,
    JSON.stringify(consent));
}

/* 4. Accept all ---------------------------------------------------- */
{
  const { w, d } = boot();
  await settle(800);
  d.querySelector("#cc-accept").click();
  const consent = w.EKGURU_COOKIES.getConsent();
  check("Accept all records every optional category",
    consent && consent.functional === true && consent.analytics === true && consent.advertising === true,
    JSON.stringify(consent));
}

/* 5. the footer link reopens the center ---------------------------- */
{
  const { w, d } = boot();
  await settle(800);
  d.querySelector("#cc-reject").click();
  check("after a choice the center is hidden", d.getElementById("ekguru-consent").hidden === true);
  const link = d.querySelector("[data-ekguru-consent-open]");
  link.dispatchEvent(new w.MouseEvent("click", { bubbles: true, cancelable: true }));
  check("the footer link reopens it", d.getElementById("ekguru-consent").hidden === false);
  check("reopening restores the recorded choice into the toggles",
    (() => { d.querySelector("#cc-customize").click();
             return d.querySelector("#cc-analytics").checked === false && d.querySelector("#cc-functional").checked === false; })());
}

/* 6. a recorded choice means no banner on the next boot ------------ */
{
  const { w, d } = boot();
  await settle(800);
  d.querySelector("#cc-reject").click();
  const stored = w.localStorage.getItem("ekguru_cookie_consent_v3");
  const vc = new VirtualConsole();
  const dom2 = new JSDOM(PAGE, { url: "https://ekguru.shop/next/", runScripts: "outside-only", pretendToBeVisual: true, virtualConsole: vc });
  dom2.window.localStorage.setItem("ekguru_cookie_consent_v3", stored);
  dom2.window.eval(CONSENT);
  dom2.window.document.dispatchEvent(new dom2.window.Event("DOMContentLoaded", { bubbles: true }));
  await settle(800);
  const el2 = dom2.window.document.getElementById("ekguru-consent");
  check("a returning visitor sees no banner", !el2 || el2.hidden === true);
  check("…but the stored choice is still applied to <html>",
    dom2.window.document.documentElement.getAttribute("data-consent") !== null);
}

/* 7. Escape closes without recording -------------------------------- */
{
  const { w, d } = boot();
  await settle(800);
  d.dispatchEvent(new w.KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
  check("Escape closes the center", d.getElementById("ekguru-consent").hidden === true);
  check("…and records no choice", w.EKGURU_COOKIES.getConsent() === null);
}

/* 8. the Analytics toggle really controls the analytics snippet -------- */
{
  const AN = readFileSync(path.join(ROOT, "js/analytics.js"), "utf8");
  function bootAnalytics(consent) {
    const vc = new VirtualConsole();
    const dom = new JSDOM("<!DOCTYPE html><html><head></head><body></body></html>",
      { url: "https://ekguru.shop/", runScripts: "outside-only", pretendToBeVisual: true, virtualConsole: vc });
    const w = dom.window;
    if (consent) w.localStorage.setItem("ekguru_cookie_consent_v3", JSON.stringify(consent));
    w.EKGURU_SITE = { analytics: { provider: "goatcounter", site: "ekguru" } };
    w.eval(AN);
    return w;
  }
  const now = Date.now();
  check("no recorded choice: analytics is not loaded",
    !bootAnalytics(null).document.head.querySelector("script[src*=zgo]"));
  check("rejected: analytics is not loaded",
    !bootAnalytics({ necessary: true, functional: true, analytics: false, advertising: false, timestamp: now })
      .document.head.querySelector("script[src*=zgo]"));
  check("accepted: analytics loads",
    !!bootAnalytics({ necessary: true, functional: true, analytics: true, advertising: true, timestamp: now })
      .document.head.querySelector("script[src*=zgo]"));
}

console.log("");
if (failed) {
  console.log("FAILED — " + failed + " check(s), " + passed + " passed.");
  process.exit(1);
}
console.log("ALL CONSENT CENTER CHECKS PASSED — " + passed + " checks.");
process.exit(0);

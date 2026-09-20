#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
let pass = 0, fail = 0;
function ok(value, name) { if (value) { pass++; console.log("PASS " + name); } else { fail++; console.error("FAIL " + name); } }
function load(window, file) { window.eval(fs.readFileSync(path.join(ROOT, file), "utf8")); }
function dom() {
  const instance = new JSDOM('<!doctype html><html data-ad-class="HIGH_CONTENT"><head></head><body><main><article><p>Lesson copy.</p></article></main></body></html>', {
    url: "https://ekguru.shop/learn/example/", runScripts: "outside-only", pretendToBeVisual: true
  });
  instance.window.EKGURU_SITE = { analytics: { provider: "goatcounter", site: "ekguru" } };
  return instance;
}

// Actual script order: analytics subscribes first; consent UI dispatches later.
{
  const instance = dom(), { window } = instance;
  const requested = [];
  const append = window.document.head.appendChild.bind(window.document.head);
  window.document.head.appendChild = (node) => { if (node.src) requested.push(node.src); return append(node); };
  load(window, "js/analytics.js");
  ok(requested.length === 0, "analytics makes no request before consent");
  load(window, "js/cookie-consent.js");
  window.document.dispatchEvent(new window.Event("DOMContentLoaded"));
  ok(!!window.document.getElementById("ekguru-cookie-settings"), "persistent Privacy settings button exists");
  window.EKGURU_COOKIES.showBanner();
  ok(window.document.getElementById("cc-advertising").disabled, "advertising checkbox is unavailable");
  window.document.getElementById("consent-reject").click();
  let saved = JSON.parse(window.localStorage.getItem("ekguru_cookie_consent_v3"));
  ok(saved.analytics === false && saved.advertising === false, "reject stores both optional purposes false");
  ok(requested.length === 0, "reject makes no analytics request");
  window.EKGURU_COOKIES.setConsent({ necessary: true, functional: false, analytics: true, advertising: true, timestamp: Date.now() });
  saved = JSON.parse(window.localStorage.getItem("ekguru_cookie_consent_v3"));
  ok(saved.analytics === true && saved.advertising === false, "even a direct API call cannot grant advertising");
  ok(requested.filter((url) => url.includes("gc.zgo.at") || url.includes("goatcounter")).length === 1, "analytics opt-in loads GoatCounter exactly once");
  window.EKGURU_COOKIES.withdrawOptional();
  saved = JSON.parse(window.localStorage.getItem("ekguru_cookie_consent_v3"));
  ok(!saved.analytics && !saved.advertising, "withdrawOptional revokes future optional processing");
  instance.window.close();
}

{
  const instance = dom(), { window } = instance;
  window.localStorage.setItem("ekguru_cookie_consent_v3", JSON.stringify({ necessary: true, functional: true, analytics: true, advertising: true, timestamp: 1 }));
  const requested = [];
  const append = window.document.head.appendChild.bind(window.document.head);
  window.document.head.appendChild = (node) => { if (node.src) requested.push(node.src); return append(node); };
  load(window, "js/monetization.js");
  window.document.dispatchEvent(new window.Event("DOMContentLoaded"));
  ok(!requested.some((url) => /googlesyndication|doubleclick/.test(url)), "monetization runtime cannot create an ad request");
  ok(window.document.querySelectorAll("ins.adsbygoogle").length === 0, "monetization runtime creates no ad units");
  ok(window.EKGURU_MONETIZATION.channels.adsense.loaderEnabled === false, "public runtime state reports the ad loader disabled");
  instance.window.close();
}

console.log(`\n${fail ? "FAIL" : "PASS"}: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);

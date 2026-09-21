#!/usr/bin/env node
/** Consent/analytics/advertising fail-closed release test in a browser DOM. */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
let pass = 0, fail = 0;
function ok(name, condition, detail = "") {
  if (condition) { pass++; console.log("PASS " + name + (detail ? " — " + detail : "")); }
  else { fail++; console.error("FAIL " + name + (detail ? " — " + detail : "")); }
}
const dom = new JSDOM('<!doctype html><html><head></head><body><main><h1>Test</h1></main></body></html>', {
  url: "https://ekguru.shop/",
  runScripts: "outside-only",
  pretendToBeVisual: true,
});
const { window } = dom;
window.scrollTo = () => {};
window.HTMLElement.prototype.scrollIntoView = () => {};
window.matchMedia = () => ({ matches: false, addEventListener() {}, removeEventListener() {} });
window.EKGURU_SITE = { analytics: { provider: "goatcounter", site: "ekguru" } };
const loaded = [];
const append = window.document.head.appendChild.bind(window.document.head);
window.document.head.appendChild = (node) => {
  if (node.tagName === "SCRIPT") loaded.push(node.src);
  return append(node);
};
function load(file) { window.eval(fs.readFileSync(path.join(ROOT, file), "utf8")); }

load("js/analytics.js");
ok("analytics is not requested before a choice", loaded.length === 0, loaded.join(","));
load("js/cookie-consent.js");
window.document.dispatchEvent(new window.Event("DOMContentLoaded"));
await new Promise((resolve) => setTimeout(resolve, 1300));
ok("new visitor sees privacy controls", !!window.document.getElementById("ekguru-consent"));
ok("advertising checkbox is disabled", window.document.getElementById("cc-advertising")?.disabled === true);
window.document.getElementById("consent-reject").click();
let state = JSON.parse(window.localStorage.getItem("ekguru_cookie_consent_v3"));
ok("reject denies analytics", state.analytics === false);
ok("reject denies advertising", state.advertising === false);
ok("reject causes no analytics request", loaded.length === 0);
await new Promise((resolve) => setTimeout(resolve, 450));
window.document.getElementById("ekguru-cookie-settings").click();
window.document.getElementById("consent-accept-all").click();
state = JSON.parse(window.localStorage.getItem("ekguru_cookie_consent_v3"));
ok("accept allows optional analytics", state.analytics === true);
ok("accept still denies unavailable advertising", state.advertising === false);
ok("analytics provider starts after accept", loaded.some((url) => /goatcounter|gc\.zgo\.at/.test(url)), loaded.join(","));

load("js/monetization.js");
window.localStorage.setItem("ekguru_cookie_consent_v3", JSON.stringify({ necessary: true, functional: true, analytics: true, advertising: true }));
window.document.dispatchEvent(new window.CustomEvent("ekguru:consent", { detail: { advertising: true } }));
await new Promise((resolve) => setTimeout(resolve, 0));
ok("global ad runtime gate prevents AdSense loader", !loaded.some((url) => /googlesyndication|doubleclick/.test(url)), loaded.join(","));
ok("global ad runtime gate creates no ad slot", window.document.querySelectorAll("ins.adsbygoogle").length === 0);
window.EKGURU_COOKIES.withdrawOptional();
state = JSON.parse(window.localStorage.getItem("ekguru_cookie_consent_v3"));
ok("withdrawal denies all optional purposes", state.functional === false && state.analytics === false && state.advertising === false);

console.log(`\n${fail ? "FAIL" : "PASS"}: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);

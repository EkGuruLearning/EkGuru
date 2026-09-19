#!/usr/bin/env node
/* =========================================================
   EkGuru — ROUTING PROBE (read-only)
   Loads the LIVE js/site-config.js + templates + mailer and
   prints which relay carries each role RIGHT NOW.
   Sends nothing.
   ========================================================= */
"use strict";
const path = require("path");
const fs = require("fs");
const ROOT = path.join(__dirname, "..");

global.window = {};
global.localStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
global.location = { href: "https://ekguru.shop/find-tutors.html" };

/* load the real config object */
const cfgSrc = fs.readFileSync(path.join(ROOT, "js", "site-config.js"), "utf8");
const cfgFn = new Function(cfgSrc + "\n;return window.EKGURU_SITE;");
window.EKGURU_SITE = cfgFn.call({ window });

window.fetch = function () {
  return Promise.resolve({ ok: true, text: () => Promise.resolve("{\"success\":\"true\"}") });
};

require(path.join(ROOT, "js", "email-templates.js"));
require(path.join(ROOT, "js", "mailer.js"));

const map = window.EkGuruMail.routingMap();
const appToken = !!((window.EKGURU_SITE.mail || {}).appsScript || {}).token;

console.log("Client token wired:", appToken);
console.log("\n=== PROVIDERS (live order + state) ===");
map.providers.forEach((p) => {
  console.log(
    "  " + p.id.padEnd(12) +
    (p.sendable ? "SENDABLE  " : "NOT-READY ") +
    "metered=" + (p.metered ? "Y" : "n") +
    "  stranger=" + (p.stranger ? "Y" : "n") +
    "  ignoresRecipient=" + (p.ignoresRecipient ? "Y" : "n")
  );
});

console.log("\n=== ROUTING (your rules → the relay actually chosen) ===");
const L = {
  bookingStudent:    "Booking  → STUDENT  (top-rank = Apps Script)",
  bookingTutor:      "Booking  → TUTOR    (top-rank = Apps Script)",
  bookingInternal:   "Booking  → EKGURU   (unlimited/FormSubmit)",
  contactVisitor:    "Contact  → VISITOR  (top-rank = Apps Script)",
  contactInternal:   "Contact  → EKGURU   (unlimited/FormSubmit)",
  adminOutbound:     "Admin    → RECIPIENT (Apps Script)",
  adminInternalCopy: "Admin    → EKGURU copy (unlimited/FormSubmit)"
};
Object.keys(L).forEach((k) => {
  console.log("  " + L[k].padEnd(46) + " →  " + (map[k] || "(none)"));
});
console.log("\nAdmin outbound fallbacks (if Apps Script fails):",
  (map.adminOutboundFallbacks || []).join(" → ") || "(none)");

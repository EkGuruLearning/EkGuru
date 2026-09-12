#!/usr/bin/env node
/* Loader smoke test: loads js/sheet.js against the LIVE production CSV
   with a minimal browser shim and asserts the schema validation and
   apply path behave. Run:  node tools/test-sheet-loader.js
*/
"use strict";
const fs = require("fs");
const path = require("path");

const cfgText = fs.readFileSync(path.join(__dirname, "..", "js", "site-config.js"), "utf8");
const m = /sheet:\s*\{[\s\S]*?csvUrl:\s*"([^"]+)"/.exec(cfgText);
if (!m) { console.error("could not find sheet.csvUrl in site-config.js"); process.exit(1); }
const CSV_URL = m[1];
console.log("sheet.csvUrl:", CSV_URL.slice(0, 70) + "…");

/* ---- browser shim ---- */
const warns = [];
const origWarn = console.warn;
console.warn = function () { warns.push([].join.call(arguments, " ")); origWarn.apply(console, arguments); };

global.window = {};
window.EKGURU_SITE = { sheet: { csvUrl: CSV_URL, cacheMinutes: 5, alwaysRevalidate: true } };
window.EKGURU_TUTORS = [
  { id: "sushila-g", name: "Sushila G." },
  { id: "hemlata", name: "Hemlata" },
  { id: "shikha-dutta", name: "Shikha Dutta" },
  { id: "tara", name: "Tara" }
];
window.EKGURU_TUTOR_DEFAULTS = { thumb: "images/placeholder-tutor.jpg", photo: null, headline: "" };
window.fetch = fetch; // sheet.js gates on `typeof window.fetch`
global.localStorage = (function () {
  const s = {};
  return { getItem: (k) => (k in s ? s[k] : null), setItem: (k, v) => { s[k] = String(v); }, removeItem: (k) => { delete s[k]; } };
})();
global.document = { addEventListener: function () {} };
global.CustomEvent = function (type, opts) { this.type = type; this.detail = (opts || {}).detail || {}; };

/* ---- load the loader ---- */
require(path.join(__dirname, "..", "js", "sheet.js"));

const deadline = Date.now() + 20000;
(function poll() {
  const info = window.EKGURU_SHEET_INFO;
  if (!info || info.loaded === undefined) {
    if (Date.now() > deadline) return finish();
    return setTimeout(poll, 250);
  }
  finish();
})();

function finish() {
  const info = window.EKGURU_SHEET_INFO || {};
  console.log("EKGURU_SHEET_INFO:", JSON.stringify(info));
  const missing = warns.filter((w) => /missing columns/.test(w));
  console.log("missing-column warnings:", missing.length);
  console.log("tutors:", window.EKGURU_TUTORS.map((t) => t.id).join(", "));

  const KNOWN = ["sushila-g", "hemlata", "shikha-dutta", "tara"];
  let ok = true;
  if (info.loaded !== true) { console.log("FAIL: sheet did not load"); ok = false; }
  if (!(info.rows >= 4)) { console.log("FAIL: expected >=4 rows, got " + info.rows); ok = false; }
  if (missing.length) { console.log("FAIL: unexpected missing-column warnings:\n" + missing.join("\n")); ok = false; }
  KNOWN.forEach((id) => {
    const t = window.EKGURU_TUTORS.find((x) => x.id === id);
    if (!t) { console.log("FAIL: tutor missing after apply: " + id); ok = false; }
    else if (!t.name) { console.log("FAIL: tutor lost its name: " + id); ok = false; }
  });

  console.log(ok ? "PASS" : "FAIL");
  process.exit(ok ? 0 : 1);
}

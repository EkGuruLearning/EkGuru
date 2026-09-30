#!/usr/bin/env node
/* Loader smoke test against the LIVE production Sheet (U0 rewrite, 30 Sep 2026).

   What it proves, in CI (this is the network step):

   1. The published Sheet is reachable through the shared fetch contract:
      output=csv first, output=tsv fallback (Google's csv endpoint for this
      workbook answers HTTP 500 while tsv answers 200). When csv is down the
      run reports the fallback — that is the PASS path, not a failure.
   2. js/sheet.js applies that live data through the exact browser code path
      (parse -> records -> applyRecords) and the roster it publishes is
      EXACTLY the publication rule:

          public tutor = in the reviewed registry  AND  sheet active=yes

      With every row active=no (the 30 Sep 2026 state) that is the empty
      roster — an empty EKGURU_TUTORS is then correct, not a failure. The
      expectations are DERIVED from the fetched rows, so flipping one row
      back to active=yes keeps this test honest without editing it.

   Run:  node tools/test-sheet-loader.js
   ============================================================ */
"use strict";
const fs = require("fs");
const path = require("path");

const SHEET_FETCH = require(path.join(__dirname, "sheet-fetch.js"));

const cfgText = fs.readFileSync(path.join(__dirname, "..", "js", "site-config.js"), "utf8");
const m = /sheet:\s*\{[\s\S]*?csvUrl:\s*"([^"]+)"/.exec(cfgText);
if (!m) { console.error("could not find sheet.csvUrl in js/site-config.js"); process.exit(1); }
const CSV_URL = m[1];
console.log("sheet.csvUrl:", CSV_URL.slice(0, 70) + "…");

const REGISTRY = (() => {
  const src = fs.readFileSync(path.join(__dirname, "..", "js", "tutors", "_registry.js"), "utf8");
  const mm = /window\.EKGURU_TUTOR_ORDER\s*=\s*\[([\s\S]*?)\]/.exec(src);
  return (mm[1].match(/"[a-z0-9-]+"/g) || []).map((s) => s.replace(/"/g, ""));
})();

(async function () {
  /* ---- 1. the live fetch, through the shared fallback contract ---- */
  let rows, fmt, usedFallback, rawText;
  try {
    const got = await SHEET_FETCH.fetchSheetRows((u) => fetch(u), CSV_URL);
    rows = got.rows; fmt = got.format; usedFallback = got.usedFallback; rawText = got.text;
  } catch (e) {
    console.log("FAIL: published Sheet unreachable in every format: " + e.message);
    process.exit(1);
  }
  console.log(`live sheet: ${rows.length} rows via output=${fmt}` +
    (usedFallback ? "  (tsv fallback — csv endpoint down, expected 30 Sep 2026)" : ""));
  if (usedFallback) console.log("PASS  csv -> tsv fallback on the live endpoint");

  const head = SHEET_FETCH.headerOf(rows);
  const recs = SHEET_FETCH.toRecords(rows);
  const isHidden = (r) => /^(no|false|0|n|hidden)$/i.test(String(r.active || "yes").trim());
  const shouldShow = recs
    .filter((r) => r.id && r.id.charAt(0) !== "#" && REGISTRY.indexOf(r.id) > -1 && !isHidden(r))
    .map((r) => r.id);

  /* ---- 2. the browser code path against the same live bytes ---- */
  const warns = [];
  const origWarn = console.warn;
  console.warn = function () { warns.push([].join.call(arguments, " ")); origWarn.apply(console, arguments); };

  global.window = {};
  window.EKGURU_SITE = { sheet: { csvUrl: CSV_URL, cacheMinutes: 5, alwaysRevalidate: true } };
  window.EKGURU_TUTORS = REGISTRY.map((id) => ({ id, name: id }));
  window.EKGURU_TUTOR_DEFAULTS = { thumb: "images/placeholder-tutor.jpg", photo: null, headline: "" };
  window.EKGURU_TUTOR_ORDER = REGISTRY.slice();

  /* Stub the network with the exact live bytes — js/sheet.js parses and
     applies them exactly as a browser would have (its own parser, its own
     csv/tsv sniff). Never a rows -> text round trip: multi-line about/bio
     cells would lose their quoting. */
  global.fetch = window.fetch = () => Promise.resolve({
    ok: true, status: 200,
    headers: { get: () => (fmt === "tsv" ? "text/tab-separated-values" : "text/csv") },
    text: () => Promise.resolve(rawText)
  });
  global.localStorage = (function () {
    const s = {};
    return { getItem: (k) => (k in s ? s[k] : null), setItem: (k, v) => { s[k] = String(v); }, removeItem: (k) => { delete s[k]; } };
  })();
  global.document = { addEventListener() {} };
  global.CustomEvent = function (type, opts) { this.type = type; this.detail = (opts || {}).detail || {}; };

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
    console.log("tutors published after apply:", window.EKGURU_TUTORS.map((t) => t.id).join(", ") || "(none)");
    console.log("expected (registry ∩ active=yes):", shouldShow.join(", ") || "(none)");

    let ok = true;
    if (info.loaded !== true) { console.log("FAIL: sheet did not load"); ok = false; }
    if (!(info.rows >= 1)) { console.log("FAIL: expected >=1 rows, got " + info.rows); ok = false; }
    if (missing.length) { console.log("FAIL: unexpected missing-column warnings:\n" + missing.join("\n")); ok = false; }

    const present = window.EKGURU_TUTORS.map((t) => t.id);
    const wrongMissing = shouldShow.filter((id) => present.indexOf(id) === -1);
    const wrongExtra = present.filter((id) => shouldShow.indexOf(id) === -1);
    if (wrongMissing.length) { console.log("FAIL: should be public but is not: " + wrongMissing.join(", ")); ok = false; }
    if (wrongExtra.length) { console.log("FAIL: published against the rule: " + wrongExtra.join(", ")); ok = false; }

    window.EKGURU_TUTORS.forEach((t) => {
      if (!t.name || t.name === t.id) {
        /* hidden rows carry no name (they are excluded anyway) */
        if (shouldShow.indexOf(t.id) > -1) { console.log("FAIL: tutor lost its name: " + t.id); ok = false; }
      }
    });

    console.log(ok ? "PASS" : "FAIL");
    process.exit(ok ? 0 : 1);
  }
})();

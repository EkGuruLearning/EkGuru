#!/usr/bin/env node
/* Loader smoke test against the LIVE production Sheet.

   What it proves, in CI (this is the network step):

   1. The published Sheet is reachable through the shared fetch contract:
      output=csv first, output=tsv fallback. When csv is down the run reports
      the fallback — that is the PASS path, not a failure.
   2. js/sheet.js applies the fetched data through the exact browser code path
      (parse -> records -> applyRecords) and publishes exactly the current
      rule: active registry tutors, plus approved=yes sheet-only tutors that
      have a safe id, name and real non-placeholder photo. Approved, active
      Sheet rows are intentional public listings; their dynamic profiles stay
      noindex until the static publication workflow runs.

   Expectations are derived from the fetched rows, so changes to the approved
   roster do not make this smoke test stale.

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
  const approved = (r) => /^(yes|true|1|y|approved)$/i.test(String(r.approved || "").trim());
  const hasRealPhoto = (r) => {
    const photo = String(r.photo || "").trim();
    return !!photo && !/placeholder/i.test(photo);
  };
  const safeId = (r) => /^[a-z0-9][a-z0-9-]{1,59}$/.test(String(r.id || ""));
  const shouldShow = recs
    .filter((r) => {
      if (!r.id || r.id.charAt(0) === "#" || isHidden(r)) return false;
      if (REGISTRY.indexOf(r.id) > -1) return true;
      return approved(r) && safeId(r) && !!String(r.name || "").trim() && hasRealPhoto(r);
    })
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
    console.log("expected (active registry + approved/photo-eligible sheet rows):", shouldShow.join(", ") || "(none)");

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

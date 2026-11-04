#!/usr/bin/env node
/* =========================================================
   EkGuru — REVIEWS SOURCE-CHAIN TESTS  (Nov 2026)
   Deterministic. No live network.
   Run:  node tools/test-reviews-fallback.js

   Pins the reviews.js fetch chain semantics (sheet-live-only
   since Nov 2026 — the baked live-sheets/reviews.csv snapshot
   was permanently deleted, so there is no snapshot step):
     live feed (if configured) -> published CSV -> same URL as TSV

   All fixture rows below are SYNTHETIC mock network bodies for
   these assertions only. They are never published anywhere.

   A. live CSV 500s, live TSV answers with mixed rows
      -> only site-native live rows publish; preply is gated,
         short-text junk is dropped; no same-origin fetch happens.
   B. Google unreachable entirely
      -> honest zero with loaded:false; nothing attached anywhere.
   C. live answers but publishes nothing (all gated/dropped)
      -> honest zero.
   ========================================================= */
"use strict";
const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");
let pass = 0, fail = 0;
function ok(name, cond, extra) {
  if (cond) { pass++; console.log("PASS " + name); }
  else { fail++; console.log("FAIL " + name + (extra ? " -- " + extra : "")); }
}
const T = "\t";
const GOOD1 = "Synthetic fixture review one for automated testing only and not a real student review at all.";
const GOOD2 = "Synthetic fixture review two for automated testing only and not a real student review at all.";
const GOOD3 = "Synthetic fixture review three for automated testing only and not a real student review at all.";
const GOOD4 = "Synthetic fixture review four for automated testing only and not a real student review at all.";
const LIVE_TSV = [
  ["tutor", "name", "date", "stars", "text", "source", "status"].join(T),
  ["sushila-g", "Marketplace User", "2026-07-12", "5", "Synthetic fixture review from an external marketplace that must never be published anywhere.", "preply", "live"].join(T),
  ["pinky-kumari", "test", "2026-06-18", "5", "msy trsdydccc", "website", "live"].join(T),
  ["sushila-g", "Fixture Student One", "2026-09-15", "5", GOOD1, "whatsapp", "live"].join(T),
  ["sushila-g", "Fixture Student Two", "2026-09-28", "4", GOOD2, "email", "live"].join(T),
  ["shikha-dutta", "Fixture Student Three", "2026-10-02", "5", GOOD3, "whatsapp", "live"].join(T),
  ["shikha-dutta", "Fixture Student Four", "2026-10-12", "4", GOOD4, "google", "live"].join(T)
].join("\n");
const LIVE_EMPTY_TSV = [
  ["tutor", "name", "date", "stars", "text", "source", "status"].join(T),
  ["sushila-g", "Marketplace User", "2026-07-12", "5", "Synthetic fixture review from an external marketplace that must never be published anywhere.", "preply", "live"].join(T),
  ["pinky-kumari", "test", "2026-06-18", "5", "msy trsdydccc", "website", "live"].join(T)
].join("\n");

function run(fetchFn) {
  delete require.cache[require.resolve(path.join(ROOT, "js", "reviews.js"))];
  const store = {};
  global.window = {
    EKGURU_SITE: { reviews: {
      csvUrl: "https://docs.google.com/spreadsheets/d/e/KEY/pub?gid=293675115&single=true&output=csv",
      cacheMinutes: 60, alwaysRevalidate: true } },
    EKGURU_TUTORS: [{ id: "sushila-g" }, { id: "shikha-dutta" }],
    EKGURU_TUTOR_FILES: {},
    document: { querySelectorAll: function () { return []; }, createEvent: function () { return { initEvent: function () {} }; } },
    dispatchEvent: function () {},
    addEventListener: function () {}
  };
  global.localStorage = {
    getItem: function (k) { return k in store ? store[k] : null; },
    setItem: function (k, v) { store[k] = String(v); },
    removeItem: function (k) { delete store[k]; }
  };
  const fetched = [];
  global.window.fetch = function (u) { fetched.push(String(u)); return fetchFn(String(u)); };
  if (!global.CustomEvent) global.CustomEvent = function (t) { this.type = t; };
  require(path.join(ROOT, "js", "reviews.js"));
  return new Promise(function (res) {
    setTimeout(function () { res({ win: global.window, fetched: fetched }); }, 300);
  });
}
function J500() {
  return Promise.resolve({ ok: false, status: 500, text: function () { return Promise.resolve(""); } });
}
function J200(body) {
  return Promise.resolve({ ok: true, text: function () { return Promise.resolve(body); } });
}
function isSameOrigin(u) { return u.indexOf("ekguru.shop") > -1; }
async function main() {
  let r = await run(function (u) {
    if (u.indexOf("output=tsv") > -1 && u.indexOf("google") > -1) return J200(LIVE_TSV);
    return J500();
  });
  let info = r.win.EKGURU_REVIEWS_INFO || {};
  ok("A: published 4 site reviews from live TSV", info.published === 4, JSON.stringify(info));
  ok("A: sushila 2 reviews at 4.5", r.win.EKGURU_TUTORS[0].reviewsCount === 2 && r.win.EKGURU_TUTORS[0].rating === 4.5);
  ok("A: no same-origin fetch attempted", !r.fetched.some(isSameOrigin), r.fetched.join(" | "));

  r = await run(function () { return J500(); });
  info = r.win.EKGURU_REVIEWS_INFO || {};
  ok("B: total outage stays 0 (no baked backfill)", (info.published || 0) === 0, JSON.stringify(info));
  ok("B: reports loaded:false", info.loaded === false, JSON.stringify(info));
  ok("B: no same-origin fetch attempted", !r.fetched.some(isSameOrigin), r.fetched.join(" | "));

  r = await run(function (u) {
    if (u.indexOf("output=tsv") > -1 && u.indexOf("google") > -1) return J200(LIVE_EMPTY_TSV);
    return J500();
  });
  info = r.win.EKGURU_REVIEWS_INFO || {};
  ok("C: live-but-empty stays 0", info.published === 0, JSON.stringify(info));

  console.log(fail ? (fail + " FAILURE(S)") : "ALL REVIEW-CHAIN TESTS PASSED");
  process.exit(fail ? 1 : 0);
}
main().catch(function (e) { console.log("THREW " + (e && e.stack || e)); process.exit(1); });

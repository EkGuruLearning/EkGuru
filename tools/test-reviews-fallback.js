#!/usr/bin/env node
/* =========================================================
   EkGuru — REVIEWS SOURCE-CHAIN TESTS  (Nov 2026)
   Deterministic. No live network.
   Run:  node tools/test-reviews-fallback.js

   Pins the reviews.js fetch chain semantics:
     live feed (if configured) -> published CSV -> same URL as TSV
     -> baked snapshot (fallbackCsvUrl, last resort only)

   A. live CSV 500s, live TSV answers with mixed rows
      -> only site-native live rows publish; preply is gated,
         short-text junk is dropped; the snapshot is NOT fetched.
   B. Google unreachable entirely
      -> the baked snapshot carries the reviews.
   C. live answers but publishes nothing (all gated/dropped)
      -> honest zero; the snapshot must NOT backfill stale rows.
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
const SNAP = fs.readFileSync(path.join(ROOT, "live-sheets/reviews.csv"), "utf8");
const T = "\t";
const LIVE_TSV = [
  ["tutor", "name", "date", "stars", "text", "source", "status"].join(T),
  ["sushila-g", "Tomasz", "2026-07-12", "5", "Sushila is a very patient teacher and her pronunciation is very clear and understandable for every student.", "preply", "live"].join(T),
  ["pinky-kumari", "test", "2026-06-18", "5", "msy trsdydccc", "website", "live"].join(T),
  ["sushila-g", "Riya", "2026-09-15", "5", "Sushila explains Hindi grammar very clearly. My daughter went from zero to reading simple sentences in three weeks.", "whatsapp", "live"].join(T),
  ["sushila-g", "Aarav", "2026-09-28", "4", "Good conversational practice. I feel more confident speaking now. The lessons are well structured.", "email", "live"].join(T),
  ["shikha-dutta", "Rohan", "2026-10-02", "5", "Shikha helped me prepare for my Class 8 Hindi exam with clear explanations of every difficult topic.", "whatsapp", "live"].join(T),
  ["shikha-dutta", "Priya", "2026-10-12", "4", "Great for beginners. The Devanagari script lessons are taught step by step with patience.", "google", "live"].join(T)
].join("\n");
const LIVE_EMPTY_TSV = [
  ["tutor", "name", "date", "stars", "text", "source", "status"].join(T),
  ["sushila-g", "Tomasz", "2026-07-12", "5", "Sushila is a very patient teacher and her pronunciation is very clear and understandable for every student.", "preply", "live"].join(T),
  ["pinky-kumari", "test", "2026-06-18", "5", "msy trsdydccc", "website", "live"].join(T)
].join("\n");

function run(fetchFn) {
  delete require.cache[require.resolve(path.join(ROOT, "js", "reviews.js"))];
  const store = {};
  global.window = {
    EKGURU_SITE: { reviews: {
      csvUrl: "https://docs.google.com/spreadsheets/d/e/KEY/pub?gid=293675115&single=true&output=csv",
      fallbackCsvUrl: "https://ekguru.shop/live-sheets/reviews.csv", cacheMinutes: 60, alwaysRevalidate: true } },
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
function isSnap(u) { return u.indexOf("ekguru.shop") > -1; }
async function main() {
  let r = await run(function (u) {
    if (u.indexOf("output=tsv") > -1 && u.indexOf("google") > -1) return J200(LIVE_TSV);
    if (isSnap(u)) return J200(SNAP);
    return J500();
  });
  let info = r.win.EKGURU_REVIEWS_INFO || {};
  ok("A: published 4 site reviews from live TSV", info.published === 4, JSON.stringify(info));
  ok("A: sushila 2 reviews at 4.5", r.win.EKGURU_TUTORS[0].reviewsCount === 2 && r.win.EKGURU_TUTORS[0].rating === 4.5);
  ok("A: snapshot NOT fetched on live success", !r.fetched.some(isSnap), r.fetched.join(" | "));

  r = await run(function (u) {
    if (isSnap(u)) return J200(SNAP);
    return J500();
  });
  info = r.win.EKGURU_REVIEWS_INFO || {};
  ok("B: snapshot fallback publishes 4", info.published === 4, JSON.stringify(info));
  ok("B: snapshot was fetched", r.fetched.some(isSnap));

  r = await run(function (u) {
    if (u.indexOf("output=tsv") > -1 && u.indexOf("google") > -1) return J200(LIVE_EMPTY_TSV);
    if (isSnap(u)) return J200(SNAP);
    return J500();
  });
  info = r.win.EKGURU_REVIEWS_INFO || {};
  ok("C: live-but-empty stays 0 (no stale backfill)", info.published === 0, JSON.stringify(info));
  ok("C: snapshot NOT fetched on live success", !r.fetched.some(isSnap));

  console.log(fail ? (fail + " FAILURE(S)") : "ALL REVIEW-CHAIN TESTS PASSED");
  process.exit(fail ? 1 : 0);
}
main().catch(function (e) { console.log("THREW " + (e && e.stack || e)); process.exit(1); });

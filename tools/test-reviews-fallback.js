#!/usr/bin/env node
/* =========================================================
   EkGuru — REVIEWS SOURCE-CHAIN TESTS  (Nov 2026)
   Deterministic. No live network.
   Run:  node tools/test-reviews-fallback.js

   Pins the reviews.js fetch chain semantics:
     live feed (if configured) -> published CSV -> same URL as TSV
     -> baked snapshot (fallbackCsvUrl — OPTIONAL, blank in
        production since Nov 2026: reviews are sheet-live-only and
        live-sheets/reviews.csv was retired, so the config must not
        point at a 404)

   A. live CSV 500s, live TSV answers with mixed rows
      -> only site-native live rows publish; preply is gated,
         short-text junk is dropped; the snapshot is NOT fetched.
   B. Google unreachable entirely, production config (no snapshot)
      -> loaded:false, nothing fetched beyond Google, no 404 probe.
   B2. Google unreachable, a snapshot IS configured
      -> the mechanism still works (last resort only).
   C. live answers but publishes nothing (all gated/dropped)
      -> honest zero; the snapshot must NOT backfill stale rows.
   D. live answers a lone header (owner deleted every row)
      -> loaded:true, published 0, cache holds [] (16 Nov 2026 fix:
         this used to throw "no rows" and keep stale reviews alive).
   E. js/site-config.js carries no dead snapshot URL.
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
/* Inline stand-in for a baked snapshot (the real file was retired). */
const SNAP = [
  '"tutor","name","date","stars","text","source","status"',
  '"sushila-g","Riya","2026-09-15","5","Sushila explains Hindi grammar very clearly. My daughter went from zero to reading simple sentences in three weeks.","whatsapp","live"',
  '"sushila-g","Aarav","2026-09-28","4","Good conversational practice. I feel more confident speaking now. The lessons are well structured.","email","live"',
  '"shikha-dutta","Rohan","2026-10-02","5","Shikha helped me prepare for my Class 8 Hindi exam with clear explanations of every difficult topic.","whatsapp","live"',
  '"shikha-dutta","Priya","2026-10-12","4","Great for beginners. The Devanagari script lessons are taught step by step with patience.","google","live"'
].join("\n");
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

function run(fetchFn, opts) {
  opts = opts || {};
  delete require.cache[require.resolve(path.join(ROOT, "js", "reviews.js"))];
  const store = opts.store || {};
  global.window = {
    EKGURU_SITE: { reviews: {
      csvUrl: "https://docs.google.com/spreadsheets/d/e/KEY/pub?gid=293675115&single=true&output=csv",
      fallbackCsvUrl: opts.snapshot ? "https://ekguru.shop/live-sheets/reviews.csv" : "", cacheMinutes: 60, alwaysRevalidate: true } },
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
    setTimeout(function () { res({ win: global.window, fetched: fetched, store: store }); }, 300);
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
  ok("B: production config, Google down -> loaded:false", info.loaded === false, JSON.stringify(info));
  ok("B: production config never probes a snapshot URL", !r.fetched.some(isSnap), r.fetched.join(" | "));
  ok("B: only the two Google attempts were made (csv, tsv)", r.fetched.length === 2, r.fetched.join(" | "));

  r = await run(function (u) {
    if (isSnap(u)) return J200(SNAP);
    return J500();
  }, { snapshot: true });
  info = r.win.EKGURU_REVIEWS_INFO || {};
  ok("B2: with a snapshot configured, the fallback publishes 4", info.published === 4, JSON.stringify(info));
  ok("B2: snapshot was fetched last", r.fetched.some(isSnap) && isSnap(r.fetched[r.fetched.length - 1]));

  r = await run(function (u) {
    if (u.indexOf("output=tsv") > -1 && u.indexOf("google") > -1) return J200(LIVE_EMPTY_TSV);
    if (isSnap(u)) return J200(SNAP);
    return J500();
  }, { snapshot: true });
  info = r.win.EKGURU_REVIEWS_INFO || {};
  ok("C: live-but-empty stays 0 (no stale backfill)", info.published === 0, JSON.stringify(info));
  ok("C: snapshot NOT fetched on live success", !r.fetched.some(isSnap));

  /* D. the owner deleted every row — a warm cache must be replaced. */
  const warmJson = () => JSON.stringify({ t: Date.now(), recs: [
    { tutor: "sushila-g", name: "Riya", date: "2026-09-15", stars: "5", text: "Sushila explains Hindi grammar very clearly, patient and structured.", source: "whatsapp", status: "live" }
  ] });
  const warm = { ekguru_reviews_v1: warmJson() };
  const HEADER_ONLY = ["tutor", "name", "date", "stars", "text", "source", "status"].join(T) + "\n";
  r = await run(function (u) {
    if (u.indexOf("output=tsv") > -1 && u.indexOf("google") > -1) return J200(HEADER_ONLY);
    if (isSnap(u)) return J200(SNAP);
    return J500();
  }, { snapshot: true, store: warm });
  info = r.win.EKGURU_REVIEWS_INFO || {};
  ok("D: header-only tab -> loaded:true, published 0", info.loaded === true && info.published === 0 && info.rows === 0, JSON.stringify(info));
  ok("D: the warm cache (1 review) was replaced by the empty sheet", r.win.EKGURU_TUTORS[0].reviewsCount === 0 && r.win.EKGURU_TUTORS[0].rating === 0, JSON.stringify(r.win.EKGURU_TUTORS[0]));
  ok("D: localStorage now holds [] (no zombie tomorrow)", JSON.parse(r.store.ekguru_reviews_v1).recs.length === 0, r.store.ekguru_reviews_v1);
  ok("D: snapshot NOT fetched — the empty tab is an answer", !r.fetched.some(isSnap), r.fetched.join(" | "));

  /* D2. junk body with no header is still refused */
  r = await run(function (u) {
    if (u.indexOf("output=tsv") > -1 && u.indexOf("google") > -1) return J200("\n");
    return J500();
  }, { store: { ekguru_reviews_v1: warmJson() } });
  info = r.win.EKGURU_REVIEWS_INFO || {};
  ok("D2: a blank body (no header) is still an error, cache kept", info.loaded === false && r.win.EKGURU_TUTORS[0].reviewsCount === 1, JSON.stringify(info));

  /* E. config hygiene */
  const cfg = fs.readFileSync(path.join(ROOT, "js/site-config.js"), "utf8");
  const m = cfg.match(/fallbackCsvUrl:\s*"([^"]*)"/);
  const snapFile = path.join(ROOT, "live-sheets/reviews.csv");
  ok("E: fallbackCsvUrl is blank, or points at a file that exists in the repo",
    !m || m[1] === "" || (/\/live-sheets\/reviews\.csv$/.test(m[1]) && fs.existsSync(snapFile)), m && m[1]);

  console.log(fail ? (fail + " FAILURE(S)") : "ALL REVIEW-CHAIN TESTS PASSED");
  process.exit(fail ? 1 : 0);
}
main().catch(function (e) { console.log("THREW " + (e && e.stack || e)); process.exit(1); });

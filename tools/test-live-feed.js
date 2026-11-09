#!/usr/bin/env node
/* =========================================================
   EkGuru: LIVE FEED TEST  (28 Oct 2026)
   ---------------------------------------------------------
   Proves the two halves of the live feed without the network:

   A. apps-script/LiveFeed.gs, run in a sandbox with fake Google
      services. It must
        · return the same CSV shape the published link does, and that
          CSV must parse with the SITE's own parser (js/sheet.js)
        · never send private columns (email, notification_email,
          formKey, whatsapp, phone-like names) or help rows
        · keep multi-line and quoted cells intact
        · cache for a short time and clear the cache on edit
        · fall back to the tab's permanent gid if the tab was renamed
        · refuse unknown tabs, and report only counts on ?tab=health

   B. The three loaders (sheet.js, reviews.js, settings.js). They must
        · ask the feed FIRST when S.feed.url is a real Apps Script /exec
        · fall back to the published CSV when the feed fails
        · never call the feed when the url is blank or malformed
        · use the identical feedUrl() function in all three files

   Run:  node tools/test-live-feed.js
   ========================================================= */
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const ROOT = path.join(__dirname, "..");

let failures = 0;
function check(name, cond, extra) {
  if (!cond) failures++;
  console.log((cond ? "PASS" : "FAIL") + "  " + name + (cond ? "" : "  ->  " + (extra || "")));
}

/* ---------- A. LiveFeed.gs in a sandbox ---------- */
function loadFeed(sheets, file) {
  const counters = { reads: 0 };
  const store = {};
  const ctx = {
    console,
    SpreadsheetApp: {
      getActive: () => ({
        getSheets: () => sheets.map((s) => ({
          getName: () => s.name,
          getSheetId: () => s.gid,
          getDataRange: () => ({ getDisplayValues: () => { counters.reads++; return s.values; } })
        }))
      })
    },
    CacheService: {
      getScriptCache: () => ({
        get: (k) => (Object.prototype.hasOwnProperty.call(store, k) ? store[k] : null),
        put: (k, v) => { store[k] = v; },
        removeAll: (ks) => ks.forEach((k) => delete store[k])
      })
    },
    ContentService: {
      MimeType: { CSV: "CSV", JSON: "JSON" },
      createTextOutput: (t) => ({
        text: t, mime: null,
        setMimeType(m) { this.mime = m; return this; },
        getContent() { return this.text; }
      })
    },
    ScriptApp: { getProjectTriggers: () => [], newTrigger: () => ({ forSpreadsheet: () => ({ onChange: () => ({ create: () => {} }) }) }) }
  };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(ROOT, "apps-script", file || "LiveFeed.gs"), "utf8"), ctx);
  return { ctx, counters, store };
}

/* The site's own parser, taken from js/sheet.js. */
function siteParser() {
  const saved = { window: global.window, localStorage: global.localStorage, document: global.document };
  global.window = { EKGURU_SITE: {} };
  global.localStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
  global.document = { addEventListener() {} };
  delete require.cache[require.resolve(path.join(ROOT, "js", "sheet.js"))];
  require(path.join(ROOT, "js", "sheet.js"));
  const parse = global.window.EkGuruSheet.parseCSV;
  Object.assign(global, saved);
  if (saved.window === undefined) delete global.window;
  return parse;
}
const parseCSV = siteParser();

const TUTOR_HEADER = ["id", "active", "approved", "name", "email", "notification_email", "formKey", "whatsapp", "phoneNumber", "bio", "priceUSD"];
const TUTOR_VALUES = [
  TUTOR_HEADER,
  ["#help", "yes / no", "yes to publish", "", "legacy", "private", "alias", "never", "private", "one paragraph per line", ""],
  ["asha-verma", "yes", "yes", "Asha Verma", "asha@example.com", "asha.private@example.com", "abc123def", "+919800000000", "9800000000",
    'First line.\nSecond line, with a comma and a "quote".', "7"],
  ["", "", "", "", "", "", "", "", "", "", ""],
  ["ravi-k", "yes", "", "Ravi K.", "", "ravi@example.com", "", "", "", "Short bio.", "6"]
];

const feed = loadFeed([
  { name: "Notes", gid: 1, values: [["x"]] },
  { name: "Tutors", gid: 1631273256, values: TUTOR_VALUES },
  { name: "reviews", gid: 293675115, values: [["tutor", "name", "date", "stars", "text", "source", "status"], ["asha-verma", "A", "2026-10-01", "5", "x".repeat(50), "site", "live"]] },
  { name: "settings", gid: 1658518385, values: [["key", "value", "what it does"], ["email", "hello@example.com", "inbox"], ["#note", "", ""]] }
]);

const out = feed.ctx.doGet({ parameter: { tab: "tutors" } });
const csv = out.getContent();
const rows = parseCSV(csv);

check("tutors feed is served as CSV", out.mime === "CSV", out.mime);
check("header keeps public columns (id, active, approved, name, bio, priceUSD)",
  ["id", "active", "approved", "name", "bio", "priceUSD"].every((h) => rows[0].indexOf(h) > -1), rows[0].join("|"));
check("private columns are removed (email, notification_email, formKey, whatsapp, phoneNumber)",
  ["email", "notification_email", "formKey", "whatsapp", "phoneNumber"].every((h) => rows[0].indexOf(h) === -1), rows[0].join("|"));
check("no private value appears anywhere in the output",
  !/asha@example|asha\.private|ravi@example|abc123def|\+919800000000|9800000000/.test(csv), "a private value leaked");
check("help row (#help) is removed", !/#help/.test(csv));
check("blank row is removed", rows.length === 3, "rows: " + rows.length);
const iBio = rows[0].indexOf("bio");
check("multi-line cell with a comma and quotes survives the round trip",
  rows[1][iBio] === 'First line.\nSecond line, with a comma and a "quote".', JSON.stringify(rows[1][iBio]));
check("the approved column reaches the site", rows[1][rows[0].indexOf("approved")] === "yes");
check("the id column is first, so the site's schema check passes", rows[0][0] === "id");

/* settings keeps its own `key` column (it must not be mistaken for a secret) */
const settingsRows = parseCSV(feed.ctx.doGet({ parameter: { tab: "settings" } }).getContent());
check("settings tab keeps the key column", settingsRows[0][0] === "key" && settingsRows[1][0] === "email", JSON.stringify(settingsRows));
check("settings help row (#note) is removed", settingsRows.length === 2);

/* cache */
const reads0 = feed.counters.reads;
feed.ctx.doGet({ parameter: { tab: "tutors" } });
check("a second request inside the cache window does not re-read the sheet", feed.counters.reads === reads0, feed.counters.reads + " vs " + reads0);
feed.ctx.onEdit({});
feed.ctx.doGet({ parameter: { tab: "tutors" } });
check("an edit clears the cache, so the next request re-reads the sheet", feed.counters.reads === reads0 + 1, feed.counters.reads + " vs " + (reads0 + 1));

/* gid fallback: tab renamed by accident */
const renamed = loadFeed([{ name: "Sheet5", gid: 1631273256, values: TUTOR_VALUES }]);
const renamedRows = parseCSV(renamed.ctx.doGet({ parameter: { tab: "tutors" } }).getContent());
check("a renamed tab is still found through its permanent gid", renamedRows.length === 3 && renamedRows[0][0] === "id");

/* missing tab never throws */
const missing = loadFeed([{ name: "Notes", gid: 1, values: [["x"]] }]);
let threw = false, missingText = "";
try { missingText = missing.ctx.doGet({ parameter: { tab: "tutors" } }).getContent(); } catch (e) { threw = true; }
check("a missing tab returns an empty CSV instead of throwing", !threw && !/\S/.test(missingText), String(missingText));

/* unknown tab and health */
const unknown = feed.ctx.doGet({ parameter: { tab: "payments-ledger" } });
check("an unknown tab is refused as JSON, never as CSV", unknown.mime === "JSON" && JSON.parse(unknown.getContent()).ok === false);
const health = feed.ctx.doGet({ parameter: { tab: "health" } });
const healthText = health.getContent();
const h = JSON.parse(healthText);
check("health reports row counts and the approved count",
  h.ok && h.tabs.tutors.rows === 2 && h.tabs.tutors.approved === 1 && h.tabs.tutors.hasApprovedColumn === true, healthText);
check("health contains no cell contents", !/Asha|asha|Ravi|example\.com/.test(healthText), healthText);

/* the feed never touches a workbook by id */
const gsText = fs.readFileSync(path.join(ROOT, "apps-script", "LiveFeed.gs"), "utf8");
check("LiveFeed.gs never opens a workbook by id (it reads only the workbook it lives in)",
  !/openById|openByUrl/.test(gsText));
check("LiveFeed.gs holds no payments key or ledger id",
  !/RAZORPAY|1u5Jkbe/.test(gsText.replace(/NEVER paste the payments workbook id or any Razorpay key[\s\S]*?separate project on purpose\./, "")));

/* ---------- A2. Unified.gs: the same halves, one file, one deployment ---------- */
function loadUnified(sheets, pending) {
  const tabs = {};
  Object.keys(pending).forEach((k) => { tabs[k] = pending[k].slice(); });
  const wrap = (name) => ({
    getLastRow: () => tabs[name].length,
    appendRow: (r) => { tabs[name].push(r); },
    setFrozenRows: () => {},
    getRange: (r, c, n) => ({ getValues: () => tabs[name].slice(r - 1, r - 1 + n).map((row) => row.slice(c - 1, c)) })
  });
  const u = loadFeed(sheets, "Unified.gs");
  u.ctx.LockService = { getScriptLock: () => ({ waitLock() {}, releaseLock() {} }) };
  u.ctx.Utilities = { formatDate: () => "2026-11-04 12:00" };
  u.ctx.PropertiesService = { getScriptProperties: () => ({ getProperty: () => null }) };
  u.ctx.Logger = { log() {} };
  u.ctx.SpreadsheetApp.getActiveSpreadsheet = () => ({
    getSheetByName: (n) => (tabs[n] ? wrap(n) : null),
    insertSheet: (n) => { tabs[n] = []; return wrap(n); }
  });
  return { ctx: u.ctx, tabs };
}

const uni = loadUnified([
  { name: "Tutors", gid: 1631273256, values: TUTOR_VALUES },
  { name: "reviews", gid: 298809212, values: [["tutor", "name", "date", "stars", "text", "source", "status"], ["asha-verma", "A", "2026-10-01", "5", "x".repeat(50), "site", "live"]] },
  { name: "settings", gid: 1658518385, values: [["key", "value"], ["email", "hello@example.com"]] },
  { name: "support", gid: 1041390059, values: [["key", "value"], ["a", "b"]] }
], {
  applications: [["timestamp", "reference", "status"]],
  reviews_pending: [["timestamp", "reference", "status"]],
  contacts: [["timestamp", "reference", "status"]],
  signups: [["timestamp", "reference", "status"]],
  bookings: [["booking_ref", "requested_at", "tutor_id"]]
});

/* the feed half routes byte-identically to standalone LiveFeed.gs */
const uniCsv = uni.ctx.doGet({ parameter: { tab: "tutors" } }).getContent();
check("unified ?tab=tutors serves the exact LiveFeed CSV", uniCsv === csv, uniCsv.slice(0, 80));
const uniHealth = JSON.parse(uni.ctx.doGet({ parameter: { tab: "health" } }).getContent());
check("unified ?tab=health is the feed health (counts only)",
  uniHealth.ok && uniHealth.tabs.tutors.rows === 2 && !/Asha/.test(JSON.stringify(uniHealth)));

/* the intake half */
const intakeHealth = JSON.parse(uni.ctx.doGet({ parameter: { action: "health" } }).getContent());
check("unified ?action=health is the intake health (v1.2.0, bound)",
  intakeHealth.ok && intakeHealth.version === "1.2.0" && intakeHealth.spreadsheetBound === true &&
  intakeHealth.pendingRows.bookings === 0, JSON.stringify(intakeHealth));
const bare = JSON.parse(uni.ctx.doGet({ parameter: {} }).getContent());
check("unified bare /exec answers combined feed+intake health",
  bare.ok && bare.unified === "2.0.0" && bare.feed.tabs.tutors.rows === 2 &&
  bare.intake.version === "1.2.0", JSON.stringify(bare).slice(0, 120));
const ping = JSON.parse(uni.ctx.doGet({ parameter: { action: "ping", token: "nope" } }).getContent());
check("unified ?action=ping without the token is refused as unknown action",
  ping.ok === false && ping.error === "unknown action", JSON.stringify(ping));
const noTab = JSON.parse(uni.ctx.doGet({ parameter: { tab: "payments-ledger" } }).getContent());
check("unified refuses an unknown tab as JSON", noTab.ok === false);

/* JSON feed format: same cells, same stripping */
const jf = JSON.parse(uni.ctx.doGet({ parameter: { tab: "tutors", format: "json" } }).getContent());
check("unified ?tab=tutors&format=json returns header+rows without private columns",
  jf.ok && jf.header[0] === "id" && jf.header.indexOf("notification_email") === -1 &&
  jf.rows.length === 2 && !/example\.com/.test(JSON.stringify(jf)), JSON.stringify(jf.header));

/* end to end: a booking lands, then a review verifies against it */
function postUni(body) {
  return JSON.parse(uni.ctx.doPost({ postData: { contents: JSON.stringify(body) } }).getContent());
}
const bk = postUni({ kind: "booking", consent: true, website: "",
  fields: { booking_ref: "EK-TESTREF", tutor_id: "asha-verma", student_name: "Priya",
    student_email: "priya@example.com", preferred_times_ist: "Mon 10am" } });
check("unified accepts a booking and stores it as its own booking_ref",
  bk.ok && bk.reference === "EK-TESTREF" && uni.tabs.bookings.length === 2 &&
  uni.tabs.bookings[1][0] === "EK-TESTREF" && uni.tabs.bookings[1][2] === "asha-verma", JSON.stringify(bk));
const bkDup = postUni({ kind: "booking", consent: true, website: "",
  fields: { booking_ref: "EK-TESTREF", tutor_id: "asha-verma", student_name: "Priya",
    student_email: "priya@example.com", preferred_times_ist: "Mon 10am" } });
check("unified booking resend is idempotent (no second row)",
  bkDup.ok && bkDup.duplicate === true && uni.tabs.bookings.length === 2, JSON.stringify(bkDup));
const rvBad = postUni({ kind: "review", consent: true, website: "",
  fields: { tutor_id: "asha-verma", reviewer_name: "Priya", stars: 5,
    text: "x".repeat(50), booking_id: "EK-NOPE" } });
check("unified refuses a review whose booking reference does not exist",
  rvBad.ok === false && uni.tabs.reviews_pending.length === 1, JSON.stringify(rvBad));
const rvWrong = postUni({ kind: "review", consent: true, website: "",
  fields: { tutor_id: "ravi-k", reviewer_name: "Priya", stars: 5,
    text: "x".repeat(50), booking_id: "EK-TESTREF" } });
check("unified refuses a review for a different tutor than the booking",
  rvWrong.ok === false && uni.tabs.reviews_pending.length === 1, JSON.stringify(rvWrong));
const rvOk = postUni({ kind: "review", consent: true, website: "",
  fields: { tutor_id: "asha-verma", reviewer_name: "Priya", stars: 5,
    text: "x".repeat(50), booking_id: "EK-TESTREF" } });
check("unified accepts a review whose booking matches tutor+reference",
  rvOk.ok && /^EG-/.test(rvOk.reference) && uni.tabs.reviews_pending.length === 2, JSON.stringify(rvOk));
const hp = postUni({ kind: "booking", consent: true, website: "bot",
  fields: { booking_ref: "EK-BOT", tutor_id: "asha-verma", student_name: "B", student_email: "b@x.com", preferred_times_ist: "x" } });
check("unified honeypot pretends success and stores nothing",
  hp.ok && uni.tabs.bookings.length === 2, JSON.stringify(hp));

/* the unified file keeps the same never-leak guarantees as LiveFeed.gs */
const uniText = fs.readFileSync(path.join(ROOT, "apps-script", "Unified.gs"), "utf8");
check("Unified.gs has exactly one doGet and one doPost",
  (uniText.match(/function doGet\(e\) \{/g) || []).length === 1 &&
  (uniText.match(/function doPost\(e\) \{/g) || []).length === 1);
check("Unified.gs opens no workbook by a hard-coded id",
  !/openById\(\s*["']1/.test(uniText));
check("Unified.gs holds no payments key or ledger id",
  !/RAZORPAY|1u5Jkbe/.test(uniText));

/* ---------- B. the three loaders ---------- */
const FEED = "https://script.google.com/macros/s/AKfycbzTESTFEED_123-abc/exec";
const CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-TEST/pub?gid=1&single=true&output=csv";

function stubFetch(plan) {
  const seen = [];
  const f = (u) => {
    seen.push(String(u));
    const rule = plan(String(u));
    if (!rule || rule.status !== 200) {
      return Promise.resolve({ ok: false, status: (rule && rule.status) || 500, text: () => Promise.resolve("") });
    }
    return Promise.resolve({ ok: true, status: 200, text: () => Promise.resolve(rule.body) });
  };
  f.seen = seen;
  return f;
}

function runSheetJs(site, plan) {
  const f = stubFetch(plan);
  global.window = { EKGURU_TUTORS: [], EKGURU_TUTOR_DEFAULTS: {}, EKGURU_SITE: site, fetch: f };
  global.fetch = f;
  global.localStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
  global.document = { addEventListener() {} };
  if (typeof global.CustomEvent !== "function") global.CustomEvent = function (t, o) { this.type = t; this.detail = (o && o.detail) || {}; };
  delete require.cache[require.resolve(path.join(ROOT, "js", "sheet.js"))];
  require(path.join(ROOT, "js", "sheet.js"));
  return f;
}

const GOOD_CSV = "id,name\r\nsomeone,Someone\r\n";
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

(async function () {
  /* feed healthy: the feed is asked first, the published CSV is not touched */
  let f = runSheetJs({ sheet: { csvUrl: CSV_URL, alwaysRevalidate: false }, feed: { url: FEED, cacheSeconds: 30 } },
    (u) => (u.indexOf("script.google.com") > -1 ? { status: 200, body: GOOD_CSV } : { status: 200, body: GOOD_CSV }));
  await wait(150);
  check("sheet.js asks the feed first", f.seen[0] && f.seen[0].indexOf(FEED + "?tab=tutors&t=") === 0, f.seen[0]);
  check("sheet.js does not touch the published CSV while the feed works", f.seen.length === 1, f.seen.join(" , "));

  /* feed down: falls back to the published CSV */
  f = runSheetJs({ sheet: { csvUrl: CSV_URL, alwaysRevalidate: false }, feed: { url: FEED } },
    (u) => (u.indexOf("script.google.com") > -1 ? { status: 500 } : { status: 200, body: GOOD_CSV }));
  await wait(150);
  check("sheet.js falls back to the published CSV when the feed fails",
    f.seen.length >= 2 && f.seen[0].indexOf(FEED) === 0 && f.seen[1] === CSV_URL, f.seen.join(" , "));

  /* feed returns an HTML error page: also a fallback */
  f = runSheetJs({ sheet: { csvUrl: CSV_URL, alwaysRevalidate: false }, feed: { url: FEED } },
    (u) => (u.indexOf("script.google.com") > -1 ? { status: 200, body: "<html>Sign in</html>" } : { status: 200, body: GOOD_CSV }));
  await wait(150);
  check("sheet.js falls back when the feed answers with a web page", f.seen[1] === CSV_URL, f.seen.join(" , "));

  /* malformed or foreign feed urls are never called */
  for (const bad of ["", "http://script.google.com/macros/s/AKfyc/exec", "https://evil.example.com/macros/s/AKfyc/exec",
    "https://script.google.com/macros/s/AKfyc/dev", "https://script.google.com/macros/s/AKfyc/exec?x=1"]) {
    f = runSheetJs({ sheet: { csvUrl: CSV_URL, alwaysRevalidate: false }, feed: { url: bad } },
      () => ({ status: 200, body: GOOD_CSV }));
    await wait(100);
    check("a bad feed url is ignored: " + (bad || "(blank)"), f.seen.length >= 1 && f.seen.every((u) => u.indexOf("script.google.com") === -1), f.seen.join(" , "));
  }

  /* the feed alone is enough to switch the loader on (no published CSV configured) */
  f = runSheetJs({ sheet: {}, feed: { url: FEED } }, () => ({ status: 200, body: GOOD_CSV }));
  await wait(150);
  check("sheet.js runs from the feed alone when no published CSV is configured", f.seen.length === 1 && f.seen[0].indexOf(FEED) === 0, f.seen.join(" , "));

  /* an EMPTY roster is still a listing page (28 Oct 2026).
     Every registry tutor is switched off in the sheet, so the baked hidden
     list leaves window.EKGURU_TUTORS as []. A newly approved guru must still
     be created there. A page with NO list at all (a pre-rendered profile)
     must create nothing. */
  const APPROVED_CSV =
    "id,active,approved,name,subject,priceUSD,photo\r\n" +
    "new-guru,yes,yes,New Guru,Hindi,8,images/new-guru.jpg\r\n" +
    "pending-guru,yes,,Pending Guru,Hindi,8,images/pending-guru.jpg\r\n";
  const runWithRoster = function (roster) {
    const fx = stubFetch(() => ({ status: 200, body: APPROVED_CSV }));
    global.window = { EKGURU_TUTOR_DEFAULTS: {}, EKGURU_SITE: { sheet: { csvUrl: CSV_URL, alwaysRevalidate: false } }, fetch: fx };
    if (roster) global.window.EKGURU_TUTORS = roster;
    global.fetch = fx;
    global.localStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
    global.document = { addEventListener() {} };
    delete require.cache[require.resolve(path.join(ROOT, "js", "sheet.js"))];
    require(path.join(ROOT, "js", "sheet.js"));
    return global.window;
  };
  let w = runWithRoster([]);
  await wait(200);
  const ids = (w.EKGURU_TUTORS || []).map((t) => t.id);
  check("an approved guru appears on a listing page whose roster is empty", ids.indexOf("new-guru") > -1, ids.join(","));
  check("an unapproved guru stays private on that same page", ids.indexOf("pending-guru") === -1, ids.join(","));

  w = runWithRoster(null);
  await wait(200);
  const idsNoList = (w.EKGURU_TUTORS || []).map((t) => t.id);
  check("a page with no tutor list at all creates nothing (profile pages stay record-only)",
    idsNoList.indexOf("new-guru") === -1, idsNoList.join(","));

  /* reviews.js: CSV→TSV fallback (4 Nov 2026). The workbook's published
     CSV answers HTTP 500; without a TSV fallback no live review ever
     reaches the browser. */
  const REV_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-TEST/pub?gid=2&single=true&output=csv";
  const REV_TSV = REV_CSV.replace("output=csv", "output=tsv");
  const GOOD_TSV = "tutor\tname\tdate\tstars\ttext\tsource\tstatus\r\nshikha-dutta\tPriya\t2026-10-01\t5\t" + "x".repeat(50) + "\tsite\tlive\r\n";
  const runReviewsJs = function (site, plan) {
    const fx = stubFetch(plan);
    global.window = { EKGURU_TUTORS: [], EKGURU_TUTOR_FILES: {},
      EKGURU_SHEET_RECORDS: { "shikha-dutta": { _recordOnly: true } },
      EKGURU_SITE: site, fetch: fx,
      addEventListener() {}, dispatchEvent() { return true; },
      document: { querySelectorAll: () => [] } };
    global.fetch = fx;
    global.localStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
    global.document = global.window.document;
    if (typeof global.CustomEvent !== "function") global.CustomEvent = function (t) { this.type = t; };
    delete require.cache[require.resolve(path.join(ROOT, "js", "reviews.js"))];
    require(path.join(ROOT, "js", "reviews.js"));
    return { seen: fx.seen, win: global.window };
  };
  let r = runReviewsJs({ reviews: { csvUrl: REV_CSV } },
    (u) => (u.indexOf("output=csv") > -1 ? { status: 500 } : { status: 200, body: GOOD_TSV }));
  await wait(200);
  check("reviews.js falls back to TSV when the published CSV answers 500",
    r.seen.length === 2 && r.seen[0] === REV_CSV && r.seen[1] === REV_TSV, r.seen.join(" , "));
  check("reviews.js loads and attaches the TSV review",
    r.win.EKGURU_REVIEWS_INFO && r.win.EKGURU_REVIEWS_INFO.loaded === true &&
    ((r.win.EKGURU_TUTOR_FILES["shikha-dutta"] || {}).reviewsCount === 1),
    JSON.stringify(r.win.EKGURU_REVIEWS_INFO));
  r = runReviewsJs({ reviews: { csvUrl: REV_CSV } }, () => ({ status: 200, body: GOOD_TSV.replace(/\t/g, ",") }));
  await wait(200);
  check("reviews.js does not touch TSV while the published CSV works",
    r.seen.length === 1 && r.seen[0] === REV_CSV, r.seen.join(" , "));

  /* the three copies of feedUrl() are identical */
  const grab = (file) => {
    const src = fs.readFileSync(path.join(ROOT, "js", file), "utf8");
    const m = /function feedUrl\(tab\) \{[\s\S]*?\n  \}/.exec(src);
    return m ? m[0] : null;
  };
  const a = grab("sheet.js"), b = grab("reviews.js"), c = grab("settings.js");
  check("feedUrl() exists in all three loaders", !!a && !!b && !!c);
  check("feedUrl() is identical in sheet.js, reviews.js and settings.js", a === b && b === c);

  /* the config keeps the feed OFF until a real url is pasted */
  const cfg = fs.readFileSync(path.join(ROOT, "js", "site-config.js"), "utf8");
  const fm = /feed:\s*\{[\s\S]*?url:\s*"([^"]*)"/.exec(cfg);
  check("js/site-config.js has a feed block", !!fm);
  check("feed.url is blank or a valid Apps Script /exec address",
    !!fm && (fm[1] === "" || /^https:\/\/script\.google\.com\/macros\/s\/[A-Za-z0-9_-]+\/exec$/.test(fm[1])), fm && fm[1]);

  console.log("\n" + (failures === 0 ? "ALL LIVE-FEED TESTS PASSED" : failures + " FAILURE(S)"));
  process.exit(failures === 0 ? 0 : 1);
})();

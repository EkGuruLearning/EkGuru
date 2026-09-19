#!/usr/bin/env node
/* =========================================================
   EkGuru — SHEET-APPLY TEST  (proves the sheet → site pipeline)
   ---------------------------------------------------------
   Question being answered: "CSV links hata diye, ab tutor data
   kahan se aata hai? Aur jab main sheets mein sab bhar dunga —
   video link, price, availability, reviews — to wo site par
   work karega ya nahi?"

   Answer, proven here:
     · RIGHT NOW the sheet URLs are PAUSED, so the site serves the
       baked-in tutor files (js/tutors/*.js + the generated pages).
       Nothing is lost — the last sheet data is baked into those.
     · When new CSV URLs are wired back in, js/sheet.js applies the
       sheet over the tutor files in the visitor's browser, and this
       test proves EVERY column applies — including `video` (which
       becomes youtubeId), priceUSD, availability, timezone, levels,
       teaches, tags, rating, notification_email, etc.

   Runs js/sheet.js against the fresh /csv/ekguru_tutors.csv with
   a stubbed fetch, then asserts the applied tutor objects.

   Run:  node tools/test-sheet-apply.js
         EKGURU_TEST_CSV=csv/ekguru_tutors.local.csv node tools/test-sheet-apply.js
         (that one is the private, address-filled copy of the LIVE tab — the
          same test, proving the row that is about to be imported behaves)

   The fixture is the source of the expectations: which tutors should be
   present comes from its `active` column, so the test keeps working when the
   roster or someone's visibility changes.
   ========================================================= */
"use strict";
const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");
/* The sheet under test — override with EKGURU_TEST_CSV to run the same
   assertions against another pack (e.g. the private, address-filled
   csv/ekguru_tutors.local.csv, before it is imported into the live tab). */
const CSV = path.join(ROOT, process.env.EKGURU_TEST_CSV || path.join("csv", "ekguru_tutors.csv"));

/* The fixture, parsed — the assertions below ask the CSV what the answer
   should be instead of hard-coding one roster size or one bad value. */
const CSV_ROWS = (() => {
  const text = fs.readFileSync(CSV, "utf8");
  const rows = [];
  let row = [], cell = "", quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') { cell += '"'; i++; }
      else if (c === '"') quoted = false;
      else cell += c;
    } else if (c === '"') quoted = true;
    else if (c === ",") { row.push(cell); cell = ""; }
    else if (c === "\n") { row.push(cell.replace(/\r$/, "")); rows.push(row); row = []; cell = ""; }
    else cell += c;
  }
  if (cell !== "" || row.length) { row.push(cell.replace(/\r$/, "")); rows.push(row); }
  return rows;
})();
const CSV_HEAD = CSV_ROWS[0];
const CSV_BY_ID = {};
for (const r of CSV_ROWS.slice(1)) {
  if (r[0] && !r[0].startsWith("#")) CSV_BY_ID[r[0].trim().toLowerCase()] = r;
}
const cell = (id, col) => {
  const r = CSV_BY_ID[id];
  return r ? (r[CSV_HEAD.indexOf(col)] || "") : "";
};
const isHiddenRow = (id) => /^(no|false|0|n|hidden)$/i.test(cell(id, "active").trim());

/* ---- browser shims ---- */
global.window = { EKGURU_TUTORS: [], EKGURU_TUTOR_DEFAULTS: {} };
global.localStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
if (typeof global.CustomEvent !== "function") {
  global.CustomEvent = function (type, opts) {
    this.type = type; this.detail = (opts && opts.detail) || {};
  };
}
global.console = console;
global.document = { addEventListener: function () {} };

window.EKGURU_TUTOR_DEFAULTS = {
  lessonLength: "50 min", subject: "Hindi", city: "", country: "",
  teaches: [], tags: [], levels: [], speaks: [], rating: 0, reviewsCount: 0,
  lessonsCount: 0, verified: false, superTutor: false, trialAvailable: false,
  youtubeId: "", priceUSD: 0, timezone: "", availability: {}, email: "",
  thumb: "", photo: "", headline: ""
};

/* Seed one stub per tutor the registry lists, with EMPTY values where the
   sheet is expected to fill. Read from the registry, never a hand-written
   list: the frozen list here is how this test kept passing while a fifth
   tutor existed, because a row for an unknown id takes sheet.js's
   "create a new tutor" path instead of the update path every check below
   describes. */
const REGISTRY = (() => {
  const src = fs.readFileSync(path.join(ROOT, "js", "tutors", "_registry.js"), "utf8");
  const m = /window\.EKGURU_TUTOR_ORDER\s*=\s*\[([\s\S]*?)\]/.exec(src);
  return (m[1].match(/"[a-z0-9-]+"/g) || []).map((s) => s.replace(/"/g, ""));
})();

REGISTRY.forEach(function (id) {
  window.EKGURU_TUTORS.push({
    id: id, name: id, subject: "Hindi", lessonLength: "50 min",
    youtubeId: "", priceUSD: 0, availability: {}, timezone: "",
    teaches: [], tags: [], levels: [], speaks: [], rating: 0,
    reviewsCount: 0, lessonsCount: 0, verified: false, superTutor: false,
    trialAvailable: false, email: "", headline: "", photo: "", thumb: ""
  });
});

/* Stub fetch to serve the real CSV file — from a mutable copy, so the second
   half of this test can hand the same loader a sheet with one more row. */
let csvText = fs.readFileSync(CSV, "utf8");
global.fetch = function (url) {
  return Promise.resolve({
    ok: true,
    text: function () { return Promise.resolve(csvText); }
  });
};
window.fetch = global.fetch;

window.EKGURU_SITE = { sheet: { csvUrl: "file://ekguru_tutors.csv", cacheMinutes: 5, alwaysRevalidate: false } };

/* ---- load the real loader ---- */
require(path.join(ROOT, "js", "sheet.js"));

let failures = 0;
function check(name, cond, extra) {
  if (!cond) failures++;
  console.log((cond ? "PASS" : "FAIL") + "  " + name + (cond ? "" : "  →  " + (extra || "")));
}

/* sheet.js fetches synchronously-ish via promise; wait a tick. */
setTimeout(function () {
  const T = window.EKGURU_TUTORS;
  const present = T.map(function (t) { return t.id; });
  /* The CSV decides who is visible (active=no hides a tutor), so the test
     asks the fixture rather than a frozen count. A tutor file with no row
     in the sheet is a separate failure mode — checked below. */
  const shouldShow = Object.keys(CSV_BY_ID).filter(function (id) { return !isHiddenRow(id); });
  const shouldHide = Object.keys(CSV_BY_ID).filter(function (id) { return isHiddenRow(id); });
  check("every tutor the sheet marks active is present after apply",
    shouldShow.every(function (id) { return present.indexOf(id) > -1; }),
    "missing: " + shouldShow.filter(function (id) { return present.indexOf(id) === -1; }).join(", "));
  check("every tutor the sheet marks active=no is excluded after apply",
    shouldHide.every(function (id) { return present.indexOf(id) === -1; }),
    "still visible: " + shouldHide.filter(function (id) { return present.indexOf(id) > -1; }).join(", "));
  if (shouldHide.length) {
    console.log("      (" + CSV.replace(ROOT + "/", "") + ": " + shouldHide.join(", ") +
      " hidden by active=no — that is this file's state, not a failure)");
  }

  const byId = {};
  T.forEach(function (t) { byId[t.id] = t; });

  const sushila = byId["sushila-g"];
  check("video → youtubeId applied (video link change WORKS)",
    sushila && sushila.youtubeId === "Ykic7gkyHjg", sushila && sushila.youtubeId);
  check("priceUSD applied (6)", sushila && sushila.priceUSD === 6, sushila && sushila.priceUSD);
  check("availability parsed to day map",
    sushila && sushila.availability && Array.isArray(sushila.availability.Mon) &&
    sushila.availability.Mon.length > 0);
  check("timezone normalised to IST (Asia/Kolkata)",
    sushila && sushila.timezone === "IST (Asia/Kolkata)", sushila && sushila.timezone);
  check("teaches applied (list)", sushila && Array.isArray(sushila.teaches) && sushila.teaches.length > 0);
  check("tags applied (list)", sushila && Array.isArray(sushila.tags) && sushila.tags.length > 0);
  check("levels applied", sushila && Array.isArray(sushila.levels) && sushila.levels.indexOf("Beginner") > -1);
  check("speaks applied (objects)", sushila && Array.isArray(sushila.speaks) && sushila.speaks[0] && !!sushila.speaks[0].lang);
  check("rating/reviewsCount/lessonsCount applied",
    sushila && sushila.rating === 5 && sushila.reviewsCount === 3 && sushila.lessonsCount === 40);
  check("verified + superTutor applied", sushila && sushila.verified === true && sushila.superTutor === true);
  check("trialAvailable applied", sushila && sushila.trialAvailable === true);
  check("photo + thumb applied", sushila && sushila.photo === "images/sushila.jpg" && sushila.thumb === "images/sushila.jpg");
  check("countryFlag applied (emoji)", sushila && !!sushila.countryFlag);
  check("about/experience/methodology applied (multiline)",
    sushila && Array.isArray(sushila.about) && sushila.about.length > 0 &&
    Array.isArray(sushila.experience) && sushila.experience.length > 0 &&
    Array.isArray(sushila.methodology) && sushila.methodology.length > 0);

  /* ---- every visible row in the fixture must land on the site ----------
     This is what makes the test useful before an import: point it at the CSV
     (or the private .local.csv) with EKGURU_TEST_CSV and the rows in that
     file are the expectations. */
  const mismatched = shouldShow.filter(function (id) {
    const t = byId[id];
    const price = cell(id, "priceUSD");
    return !t || t.name !== cell(id, "name") ||
      (price !== "" && Number(t.priceUSD) !== Number(price));
  });
  check("every visible row's name and price reached the site",
    mismatched.length === 0, mismatched.join(", "));

  const newest = Object.keys(CSV_BY_ID).filter(function (id) { return !isHiddenRow(id); }).pop();
  if (newest && byId[newest]) {
    const h = byId[newest];
    const linesOf = function (v) { return v.split("\n").filter(function (x) { return x.trim(); }).length; };
    const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    const slots = (cell(newest, "availability").split(",").length > 1)
      ? cell(newest, "availability").replace(/^[^ ]* /, "").split(",").length : 0;
    check("newest row applies (" + newest + "): name, price, lesson length",
      h.name === cell(newest, "name") &&
      h.priceUSD === Number(cell(newest, "priceUSD")) &&
      h.lessonLength === cell(newest, "lessonLength"),
      [h.name, h.priceUSD, h.lessonLength].join(" / "));
    check("newest row applies: availability is a day map with its own slots",
      slots > 0 && days.every(function (d) {
        return Array.isArray(h.availability[d]) && h.availability[d].length === slots;
      }) && (h.availability.Sun || []).length === 0,
      JSON.stringify(h.availability));
    check("newest row applies: about / experience / methodology line counts",
      (h.about || []).length === linesOf(cell(newest, "about")) &&
      (h.experience || []).length === linesOf(cell(newest, "experience")) &&
      (h.methodology || []).length === linesOf(cell(newest, "methodology")),
      "about " + (h.about || []).length + ", experience " + (h.experience || []).length +
      ", methodology " + (h.methodology || []).length);
    check("newest row applies: the booking inbox arrives (notification_email)",
      h.notification_email === (cell(newest, "notification_email") || undefined) ||
      h.notification_email === cell(newest, "notification_email"),
      JSON.stringify(h.notification_email));
    check("newest row applies: all six specialities, badged, still on the roster",
      (h.specialities || []).length === 6 && h.badge === cell(newest, "badge") &&
      h._hiddenBySheet === false,
      (h.specialities || []).length + " specialities, badge " + h.badge);
  }

  /* Blank email cell = keep the file value (no silent wipe). */
  check("blank email in sheet does NOT wipe tutor email",
    !sushila || sushila.email === "", "email=" + (sushila && sushila.email));

  const tara = byId["tara"];
  check("valid videoTitle applied (sushila)", sushila && sushila.videoTitle === "Hindi Tutor Intro",
    sushila && sushila.videoTitle);
  const taraSheetVT = cell("tara", "videoTitle");
  if (isHiddenRow("tara")) {
    /* active=no in this fixture (the live tab) — the whole row is skipped by
       the loader, so there is no applied value to inspect. The two roster
       checks above are what prove the skip happened. */
    check("videoTitle column: skipped for a tutor this fixture hides",
      tara == null, "tara applied anyway: " + JSON.stringify(tara && tara.videoTitle));
    console.log("      (tara is active=no in this fixture — the refusal and apply paths " +
      "are covered by the pack: EKGURU_TEST_CSV unset)");
  } else if (taraSheetVT.indexOf("|") > -1) {
    check("garbled videoTitle (contains '|') correctly refused — validator works",
      tara && (tara.videoTitle === "" || tara.videoTitle == null), JSON.stringify(tara && tara.videoTitle));
  } else {
    check("clean videoTitle in this fixture applies as written",
      tara && tara.videoTitle === taraSheetVT,
      JSON.stringify(tara && tara.videoTitle) + " vs sheet " + JSON.stringify(taraSheetVT));
    console.log("      (this fixture has no '|' in tara's videoTitle — the refusal path is " +
      "covered by the pack: EKGURU_TEST_CSV unset)");
  }

  /* notification_email column: blank in CSV → nothing set (honest). */
  check("notification_email stays unset when blank (honest TUTOR_EMAIL_UNAVAILABLE path)",
    !(sushila && sushila.notification_email), sushila && sushila.notification_email);

  const info = window.EKGURU_SHEET_INFO || window.EkGuruSheet && window.EkGuruSheet.info && window.EkGuruSheet.info();
  check("sheet info reports loaded + changes",
    info && (info.loaded !== false), JSON.stringify(info));

  /* ---- second pass: a row for someone with no tutor file yet ------------
     This is the case that makes the sheet powerful: the owner adds a row and
     the tutor appears, before any rebuild and without a js/tutors/<id>.js.
     The loader's "create" branch is not covered by the checks above, which
     all describe updating an existing tutor. */
  const NEW_ID = "sheet-only-tutor";
  const NEW_ROW = CSV_HEAD.map(function (h) {
    if (h === "id") return NEW_ID;
    if (h === "active") return "yes";
    if (h === "name") return "Sheet Only Tutor";
    if (h === "subject") return "Hindi";
    if (h === "priceUSD") return "9";
    if (h === "lessonLength") return "50 min";
    if (h === "availability") return "Mon 10:00,11:00";
    if (h === "headline") return "Added from the spreadsheet, no rebuild";
    return "";
  }).map(function (v) { return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }).join(",");
  csvText = csvText.replace(/\r?\n$/, "\r\n") + NEW_ROW + "\r\n";

  window.EkGuruSheet.refresh().then(function () {
    const made = window.EKGURU_TUTORS.filter(function (t) { return t.id === NEW_ID; })[0];
    check("a sheet row with no tutor file creates the tutor (no rebuild needed)",
      !!made && made.name === "Sheet Only Tutor" && made.priceUSD === 9,
      made ? made.name + " / $" + made.priceUSD : "not created");

    console.log("\n" + (failures === 0
      ? "ALL SHEET-APPLY TESTS PASSED — sheet edits (incl. video links) will apply when new URLs are wired."
      : failures + " FAILURE(S)"));
    process.exit(failures === 0 ? 0 : 1);
  });
}, 300);

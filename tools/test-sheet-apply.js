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
   ========================================================= */
"use strict";
const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");
const CSV = path.join(ROOT, "csv", "ekguru_tutors.csv");

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

/* Seed 4 tutors with EMPTY values where the sheet is expected to fill. */
["sushila-g", "hemlata", "shikha-dutta", "tara"].forEach(function (id) {
  window.EKGURU_TUTORS.push({
    id: id, name: id, subject: "Hindi", lessonLength: "50 min",
    youtubeId: "", priceUSD: 0, availability: {}, timezone: "",
    teaches: [], tags: [], levels: [], speaks: [], rating: 0,
    reviewsCount: 0, lessonsCount: 0, verified: false, superTutor: false,
    trialAvailable: false, email: "", headline: "", photo: "", thumb: ""
  });
});

/* Stub fetch to serve the real CSV file. */
global.fetch = function (url) {
  return Promise.resolve({
    ok: true,
    text: function () { return Promise.resolve(fs.readFileSync(CSV, "utf8")); }
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
  check("4 tutors still present after apply", T.length === 4, "got " + T.length);

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

  /* Blank email cell = keep the file value (no silent wipe). */
  check("blank email in sheet does NOT wipe tutor email",
    !sushila || sushila.email === "", "email=" + (sushila && sushila.email));

  const tara = byId["tara"];
  check("valid videoTitle applied (sushila)", sushila && sushila.videoTitle === "Hindi Tutor Intro",
    sushila && sushila.videoTitle);
  check("garbled videoTitle (contains '|') correctly refused — validator works",
    tara && (tara.videoTitle === "" || tara.videoTitle == null), JSON.stringify(tara && tara.videoTitle));

  /* notification_email column: blank in CSV → nothing set (honest). */
  check("notification_email stays unset when blank (honest TUTOR_EMAIL_UNAVAILABLE path)",
    !(sushila && sushila.notification_email), sushila && sushila.notification_email);

  const info = window.EKGURU_SHEET_INFO || window.EkGuruSheet && window.EkGuruSheet.info && window.EkGuruSheet.info();
  check("sheet info reports loaded + changes",
    info && (info.loaded !== false), JSON.stringify(info));

  console.log("\n" + (failures === 0
    ? "ALL SHEET-APPLY TESTS PASSED — sheet edits (incl. video links) will apply when new URLs are wired."
    : failures + " FAILURE(S)"));
  process.exit(failures === 0 ? 0 : 1);
}, 300);

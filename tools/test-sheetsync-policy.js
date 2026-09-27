#!/usr/bin/env node
/* =========================================================
   EkGuru — SHEETSYNC POLICY TEST  (build side, 27 Sep 2026)
   ---------------------------------------------------------
   The runtime side of the reputation gate is proven by
   tools/test-sheet-apply.js (third pass). This test proves the
   BUILD side: tools/sheetsync.js must never bake unverified
   marketplace values into js/tutors/_overrides.js, because the
   next sync would otherwise restore them for every visitor.

   Adversarial input (the exact stale row observed on the live
   sheet on 26-27 Sep 2026):
       rating 5, reviews 3, lessons 40, superTutor yes,
       a marketplace profile URL.

   Expected build output: none of it. Ordinary cells still
   apply (price, name, availability, …).
   ========================================================= */
"use strict";

const { buildTutor, buildReviews, MARKETPLACE_SOURCES } = require("./sheetsync");

let failures = 0;
function check(name, cond, extra) {
  if (!cond) failures++;
  console.log((cond ? "PASS" : "FAIL") + "  " + name + (cond ? "" : "  →  " + (extra || "")));
}

/* --- the stale row, exactly as the live sheet carried it ------- */
const STALE_ROW = {
  id: "sushila-g",
  active: "yes",
  name: "Sushila G.",
  subject: "Hindi",
  priceusd: "6",
  lessonlength: "50 min",
  rating: "5",
  reviewscount: "3",
  lessonscount: "40",
  supertutor: "yes",
  preplyurl: "https://preply.com/en/tutor/7717290",
  verified: "yes",
  video: "Ykic7gkyHjg"
};

const t = buildTutor(STALE_ROW);

check("buildTutor: rating is NOT baked from the sheet",
  t.rating === undefined || Number(t.rating) === 0, t.rating);
check("buildTutor: reviewsCount is NOT baked from the sheet",
  t.reviewsCount === undefined || Number(t.reviewsCount) === 0, t.reviewsCount);
check("buildTutor: lessonsCount is NOT baked from the sheet",
  t.lessonsCount === undefined || Number(t.lessonsCount) === 0, t.lessonsCount);
check("buildTutor: superTutor is NOT baked from the sheet",
  t.superTutor === undefined || t.superTutor === false, t.superTutor);
check("buildTutor: external-marketplace profile URL is NOT baked",
  !t.preplyUrl, t.preplyUrl);
check("buildTutor: verified still applies (owner flag)",
  t.verified === true, t.verified);
check("buildTutor: ordinary cells still apply (price 6, name, video id)",
  t.priceUSD === 6 && t.name === "Sushila G." && t.youtubeId === "Ykic7gkyHjg",
  JSON.stringify({ p: t.priceUSD, n: t.name, v: t.youtubeId }));

/* --- reviews: marketplace rows gated, site-native rows kept ---- */
const LONG_TEXT = "A genuinely written review that is long enough to pass the minimum length check.";
const reviews = buildReviews([
  { tutor: "sushila-g", name: "Tomasz", date: "2026-08-01", stars: "5", text: LONG_TEXT, source: "preply", status: "live" },
  { tutor: "sushila-g", name: "Jon", date: "2026-08-05", stars: "5", text: LONG_TEXT, source: "italki", status: "live" },
  { tutor: "sushila-g", name: "Aaravi", date: "2026-09-01", stars: "4", text: LONG_TEXT, source: "email", status: "live" },
  { tutor: "sushila-g", name: "Hidden", date: "2026-09-02", stars: "5", text: LONG_TEXT, source: "email", status: "hidden" }
]);
const list = reviews["sushila-g"] || [];
check("buildReviews: marketplace rows (preply/italki) are excluded",
  !list.some(r => r.name === "Tomasz" || r.name === "Jon"),
  JSON.stringify(list.map(r => r.name)));
check("buildReviews: site-native rows are kept",
  list.some(r => r.name === "Aaravi" && r.stars === 4),
  JSON.stringify(list.map(r => r.name)));
check("buildReviews: hidden rows stay hidden",
  !list.some(r => r.name === "Hidden"),
  JSON.stringify(list.map(r => r.name)));
check("gate list is the known marketplaces only",
  MARKETPLACE_SOURCES.length === 2 &&
    MARKETPLACE_SOURCES[0] === "preply" && MARKETPLACE_SOURCES[1] === "italki",
  "sources=" + MARKETPLACE_SOURCES);

console.log(failures === 0
  ? "\nALL SHEETSYNC POLICY TESTS PASSED — the build side refuses marketplace values too."
  : "\n" + failures + " FAILURE(S)");
process.exit(failures === 0 ? 0 : 1);

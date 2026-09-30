/* =========================================================
   EkGuru — ZERO-TUTOR STATE  (shared by the generators)
   ---------------------------------------------------------
   U0, 30 Sep 2026. The owner's decision: while the Google Sheet
   marks every tutor active=no, NO tutor is public anywhere — and
   every place that used to list tutors says so honestly, in the
   reader's language, and points at the free lessons, practice
   and courses, which are always open:

       "Abhi koi tutor booking ke liye available nahi hai.
        Free lessons, practice aur courses hamesha khule hain."

   One markup builder for tools/build-home-tutors.js,
   tools/build-market-pages.js, tools/build-roster-rows.js and
   tools/build-tutor-pages.js, and the same wording as
   js/main.js emptyTutorsHTML() (the live repaint). The i18n
   keys are tutors.emptyTitle / tutors.emptyBody /
   tutors.emptyCta in js/i18n.js (all 7 markets).

   `prefix` is the relative path from the page to the site root
   ("" at the root, "../" inside es/, hindi-tutor/delhi/, …).
   ========================================================= */
"use strict";

function esc(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

const EN = {
  "tutors.emptyTitle": "No tutors are available for booking right now.",
  "tutors.emptyBody": "Free lessons, practice and courses are always open.",
  "tutors.emptyCta": "Start the free course"
};

/* Resolution order: the caller's translator (market pages throw on a
   missing key on purpose), then the language's table in the i18n
   bundle, then the English table, then the literal above. */
function resolve(i18n, t, lang, key) {
  if (typeof t === "function") return t(lang, key);
  const table = (i18n && (i18n[lang] || i18n.en)) || {};
  return table[key] || (i18n && i18n.en && i18n.en[key]) || EN[key] || key;
}

/* The block itself. `tag` picks the wrapper element so the block
   drops into the exact slot the tutor cards used (div, section,
   article …). `attrs` sets the wrapper attributes (class, id,
   data-i18n keys) of the caller's choosing. */
function emptyTutorsBlock(opts) {
  const o = opts || {};
  const prefix = o.prefix || "";
  const lang = o.lang || "en";
  const tag = o.tag || "div";
  const attrs = o.attrs || 'class="t-empty empty"';
  const get = (key) => esc(resolve(o.i18n, o.t, lang, key));
  const title = get("tutors.emptyTitle");
  const body = get("tutors.emptyBody");
  const cta = get("tutors.emptyCta");

  return `<${tag} ${attrs}>
  <p class="t-empty-title"><strong>${title}</strong></p>
  <p class="t-empty-body">${body}</p>
  <p class="t-empty-links">
    <a class="btn btn-primary" href="${prefix}learn/hindi/">${cta}</a>
    · <a href="${prefix}learn/">Learn</a>
    · <a href="${prefix}courses/">Courses</a>
    · <a href="${prefix}daily-hindi/">Daily Hindi</a>
  </p>
</${tag}>`;
}

module.exports = { emptyTutorsBlock };

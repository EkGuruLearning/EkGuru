/* =========================================================
   EkGuru — TUTOR REGISTRY
   ---------------------------------------------------------
   This tiny file is the ONLY place that knows a tutor exists.

   ➕ TO ADD A NEW TUTOR — 3 steps, nothing else:
      1. Copy  js/tutors/_TEMPLATE.js  to  js/tutors/theirname.js
      2. Fill it in (every line is commented)
      3. Add ONE line to the list below:
            "theirname",
      4. Rebuild:   node tools/langsync.js && node tools/prerender.js
                    && node tools/sitemap.js && node tools/patch.js

   Step 4 puts them on the English pages, all six translated pages,
   the JSON-LD, the sitemap and their own pre-rendered profile, and
   adds the <script> tags for you.

   ⚠️ It used to say "add a <script> line to each HTML page by hand".
   That is how Shikha Dutta ended up missing from all six language
   pages — the hand edit was done for English and forgotten for the
   rest. Never edit those script tags yourself; run langsync.

   The order below is the order they appear on the site.
   Move a name up to feature that tutor higher.

   ⚠️ Names here must match the FILENAME and the tutor's `id`.
   ========================================================= */

window.EKGURU_TUTOR_ORDER = [
  "sushila-g",
  "hemlata",
  "shikha-dutta",
  "tara",
];

/* ---------------------------------------------------------
   Collector — each tutor file calls this. Do not edit.
   --------------------------------------------------------- */
window.EKGURU_TUTOR_FILES = window.EKGURU_TUTOR_FILES || {};

window.ekguruTutor = function (tutor) {
  try {
    if (!tutor || !tutor.id) {
      console.error("[EkGuru] A tutor file is missing its id.");
      return;
    }
    window.EKGURU_TUTOR_FILES[tutor.id] = tutor;
  } catch (e) {
    console.error("[EkGuru] Failed to register a tutor:", e);
  }
};

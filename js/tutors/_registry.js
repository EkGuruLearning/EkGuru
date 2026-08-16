/* =========================================================
   EkGuru — TUTOR REGISTRY
   ---------------------------------------------------------
   This tiny file is the ONLY place that knows a tutor exists.

   ➕ TO ADD A NEW TUTOR — 3 steps, nothing else:
      1. Copy  js/tutors/_TEMPLATE.js  to  js/tutors/theirname.js
      2. Fill it in (every line is commented)
      3. Add ONE line to the list below:
            "theirname",
      4. Add ONE <script> line in each HTML page:
            <script src="js/tutors/theirname.js"></script>

   The order below is the order they appear on the site.
   Move a name up to feature that tutor higher.

   ⚠️ Names here must match the FILENAME and the tutor's `id`.
   ========================================================= */

window.EKGURU_TUTOR_ORDER = [
  "sushila-g",
  "hemlata",
  "tara"
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

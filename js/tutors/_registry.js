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

/* Only profiles with a non-placeholder identity/photo and owner-reviewed
   source material are public. Draft records stay in this directory so they
   can be completed, but keeping them out of this list keeps them out of the
   roster, localized pages, feeds and generated tutor sitemaps.

   U0 (30 Sep 2026) — the publication rule has TWO gates:

      a tutor is PUBLIC  ⇔  in this registry  AND  sheet active=yes

   16 Nov 2026 — owner clarification ("jo tutor approved hai unko
   approved maan kar visible karna"): being in this registry IS the
   approval. A registry tutor with NO row in the sheet is visible with
   their file values; only an explicit active=no row hides them. The
   build (tools/sheetsync.js) always worked that way; js/sheet.js and
   js/livepatch.js now match it.

   17 Nov 2026 — the sheet can publish a guru WITHOUT a file here. A
   sheet row with approved=yes (and not active=no) is baked by
   tools/sheetsync.js into window.EKGURU_SHEET_TUTORS (js/tutors/
   _overrides.js) and joins the roster after this list — cards, profile
   page (noindex), find-tutors, feed, llms.txt, 404 links — so the first
   paint matches the sheet even when Google's CSV endpoint is down.
   notification_email / phone are never baked. This list still decides
   ORDER and which gurus have hand-written files; it is no longer the
   only way to publish. Proven by tools/test-sheet-only-bake.mjs.

   The sheet owns the second gate (js/tutors/_overrides.js, written by
   tools/sheetsync.js). A hidden tutor (active=no) keeps their profile
   page — reachable by direct link, noindex, booking off — but is absent
   from every list: home/locale cards, find-tutors, sitemaps, feed,
   llms.txt, manifest shortcuts, 404.html and the ItemList JSON-LD.
   Flipping the row back to active=yes restores everything — both
   directions are owned by the generators and proven by
   tools/test-tutor-activation.mjs. */
window.EKGURU_TUTOR_ORDER = [
  "sushila-g",
  "shikha-dutta",
  "deepika",
  "utkarsh-upadhyay",
  "pinky-kumari",
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

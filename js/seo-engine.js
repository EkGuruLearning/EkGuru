/* =========================================================
   EkGuru — SEO data stubs (was: keyword-phrase engine)
   ---------------------------------------------------------
   REMOVED (post-push audit): this file used to generate hundreds
   of keyword phrases per page and publish them across dozens of
   meta tags. Google ignores <meta name="keywords"> for ranking
   and indexing, and the pattern reads as keyword stuffing — a
   site-quality/AdSense risk. All phrase generation was removed.

   The file stays only to keep the existing <script> includes
   valid and to keep the small amount of legitimate structured
   data (schema.org "knowsAbout" entities) that js/seo.js still
   reads. Nothing here is keyword delivery anymore.
   ========================================================= */
(function () {
  "use strict";

  /* Legitimate schema.org topical entities (used by js/seo.js for
     Organization.knowsAbout). A fixed, honest list of subjects the
     site actually teaches — not a keyword list. */
  function entities() {
    return [
      "Hindi", "Hindi language", "Devanagari", "Language education",
      "Online tutoring", "Second-language acquisition", "India", "Hindustani language",
      "Private tutoring", "Distance education", "Language proficiency"
    ];
  }

  /* Former keyword-phrase API. Returns an empty list so any legacy
     caller that still asks gets nothing to publish. */
  function forPage() { return []; }

  window.EkGuruSEO = {
    total: 0,
    forPage: forPage,
    founder: function () { return []; },
    platforms: function () { return []; },
    compare: function () { return []; },
    brand: function () { return []; },
    questions: function () { return []; },
    entities: entities,
    vocab: {
      ACTION: [], QUALITY: [], SUBJECT: [], ROLE: []
    }
  };
})();

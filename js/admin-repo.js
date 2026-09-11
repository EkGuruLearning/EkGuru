/* =========================================================
   EkGuru — ADMIN DATA LAYER  (v74, Phase 14)
   ---------------------------------------------------------
       window.EkGuruAdmin.content.countries()
       window.EkGuruAdmin.tutors.ranked(ctx)
       window.EkGuruAdmin.seo.status()
       window.EkGuruAdmin.analytics.summary()

   ═══════════════════════════════════════════════════════
   THE HONEST FRAMING
   ═══════════════════════════════════════════════════════

   The brief asks for AdminRepository / ContentRepository /
   TutorRepository / AnalyticsRepository / SeoRepository with a
   StaticRepository and a FutureApiRepository implementation.

   That is the right shape, and it comes with an obligation:
   NOT to pretend the static implementation is something it is
   not. This site has no backend. Every repository below is
   read-only, reads data the browser already has, and says so.

   Specifically:

     · No repository writes. There is nowhere to write to.
       A "save" button that silently does nothing is worse
       than no button.

     · No repository invents a number. Where a figure needs a
       backend that does not exist, the method returns
       { available: false, requires: "..." } and the UI shows
       that sentence instead of a zero. A zero looks like data.

     · No repository holds a secret. Anything in this file is
       served to every visitor who guesses the URL.

   When a backend arrives, `ApiRepository` below is filled in
   and `pick()` chooses it. Nothing else in admin.html changes.
   ========================================================= */

(function () {
  "use strict";

  var SITE = window.EKGURU_SITE || {};

  /* Every method returns this shape, so the UI never has to
     guess whether it received data or an explanation. */
  function data(value, meta) {
    return Object.assign({ available: true, value: value, source: "static" }, meta || {});
  }
  function unavailable(requires, note) {
    return { available: false, value: null, requires: requires, note: note || null };
  }

  /* =========================================================
     CONTENT
     ========================================================= */
  var StaticContentRepository = {
    /* Counts are DERIVED from what the page can see, never
       typed in. A hardcoded count is wrong the first time a
       section grows, and this project has shipped that bug
       about a dozen times. */
    sections: function () {
      var s = window.EKGURU_ADMIN_STATS || null;
      if (!s) {
        return unavailable("admin-stats.json",
          "Generated at build time by tools/adminstats.js. Rebuild to populate.");
      }
      return data(s.sections, { generated: s.generated });
    },
    countries: function () {
      var s = window.EKGURU_ADMIN_STATS;
      if (!s || !s.countries) return unavailable("admin-stats.json");
      return data(s.countries, { generated: s.generated });
    },
    languages: function () {
      var s = window.EKGURU_ADMIN_STATS;
      if (!s || !s.languages) return unavailable("admin-stats.json");
      return data(s.languages, { generated: s.generated });
    },
    learningPairs: function () {
      var s = window.EKGURU_ADMIN_STATS;
      if (!s || !s.pairs) return unavailable("admin-stats.json");
      return data(s.pairs, { generated: s.generated });
    }
  };

  /* =========================================================
     TUTORS
     ========================================================= */
  var StaticTutorRepository = {
    all: function () {
      var t = window.EKGURU_TUTORS;
      return t ? data(t) : unavailable("js/tutors-data.js", "Tutor data has not loaded yet.");
    },
    ranked: function (ctx) {
      var t = window.EKGURU_TUTORS;
      if (!t) return unavailable("js/tutors-data.js");
      if (!window.EkGuruRank) return unavailable("js/ranking.js", "The ranking engine is not loaded.");
      return data(window.EkGuruRank.rank(t, ctx || {}));
    },
    rankingFactors: function (ctx) {
      if (!window.EkGuruRank) return unavailable("js/ranking.js");
      return data(window.EkGuruRank.factors(ctx || {}));
    },
    completeness: function (tutor) {
      if (!window.EkGuruRank) return unavailable("js/ranking.js");
      return data(window.EkGuruRank.completeness(tutor));
    },
    /* Deliberately absent rather than faked. */
    bookings: function () {
      return unavailable("a booking backend",
        "EkGuru is a static site. Booking requests go by email through " +
        "FormSubmit and are not recorded anywhere this page can read.");
    },
    verificationQueue: function () {
      return unavailable("a moderation backend",
        "Verification is a flag in the spreadsheet today, not a workflow.");
    }
  };

  /* =========================================================
     SEO
     ========================================================= */
  var StaticSeoRepository = {
    status: function () {
      var s = window.EKGURU_ADMIN_STATS;
      if (!s || !s.seo) {
        return unavailable("admin-stats.json",
          "Run: node tools/seocheck.js — its result is baked in at build time.");
      }
      return data(s.seo, { generated: s.generated });
    },
    /* A live crawl needs a server or CORS on every page. Both
       are absent, so this reports the last BUILD-TIME result
       rather than pretending to check now. */
    liveCrawl: function () {
      return unavailable("a crawler backend",
        "The build-time result from tools/seocheck.js is shown instead. " +
        "It is accurate as of the last deploy, not as of now.");
    }
  };

  /* =========================================================
     QUALITY / PRIVACY
     ========================================================= */
  var StaticQualityRepository = {
    privacy: function () {
      var s = window.EKGURU_ADMIN_STATS;
      if (!s || !s.privacy) return unavailable("admin-stats.json",
        "Run: node tools/privacy.js --sheets");
      return data(s.privacy, { generated: s.generated });
    },
    brokenLinks: function () {
      var s = window.EKGURU_ADMIN_STATS;
      if (!s || !s.seo) return unavailable("admin-stats.json");
      return data({ count: s.seo.brokenLinks, orphans: s.seo.orphans });
    },
    build: function () {
      var s = window.EKGURU_ADMIN_STATS;
      if (!s || !s.gate) return unavailable("admin-stats.json",
        "Run: node tools/gate.js");
      return data(s.gate, { generated: s.generated });
    }
  };

  /* =========================================================
     ANALYTICS
     ---------------------------------------------------------
     GoatCounter has a JSON API, and it needs a key that must
     not be in this file. So: no numbers are shown here. The
     dashboard links to the real dashboard instead, which is
     the honest version of "analytics in admin".
     ========================================================= */
  var StaticAnalyticsRepository = {
    summary: function () {
      var a = SITE.analytics || {};
      if (!a.code) return unavailable("an analytics provider", "None is configured.");
      return unavailable("the GoatCounter API and a key",
        "An API key cannot live in a page served from a public repository. " +
        "Open the dashboard directly: https://" + a.code + ".goatcounter.com");
    },
    dashboardUrl: function () {
      var a = SITE.analytics || {};
      return a.code ? data("https://" + a.code + ".goatcounter.com") : unavailable("an analytics provider");
    },
    events: function () {
      /* What the site EMITS is knowable from the code; what was
         RECEIVED is not. Reporting the first as if it were the
         second would be the fabrication the brief forbids. */
      return data([
        "<section>_page_view", "tutor_cta_clicked_from_<section>",
        "tool_alphabet", "tool_numbers", "tool_numbers_quiz", "tool_phrasebook",
        "tool_flashcards", "tool_quiz", "quiz_completed", "tool_level_test",
        "level_test_completed", "tool_typing", "tool_planner", "tool_verbs",
        "tool_datetime", "tool_pronunciation", "tool_vocabulary",
        "daily_hub", "daily_day_<n>", "site_search"
      ], { note: "Events the site emits. Counts are only visible in GoatCounter." });
    }
  };

  /* =========================================================
     FUTURE API — the contract, unimplemented on purpose
     ---------------------------------------------------------
     Every method throws rather than returning empty. A stub
     that returns [] looks like "no data" and gets shipped by
     accident; one that throws cannot.
     ========================================================= */
  function notImplemented(name) {
    return function () {
      throw new Error("ApiRepository." + name + " is not implemented. " +
        "EkGuru has no backend yet. See js/admin-repo.js.");
    };
  }
  var ApiRepository = {
    baseUrl: null,
    content: {
      sections: notImplemented("content.sections"),
      countries: notImplemented("content.countries"),
      languages: notImplemented("content.languages"),
      learningPairs: notImplemented("content.learningPairs")
    },
    tutors: {
      all: notImplemented("tutors.all"),
      ranked: notImplemented("tutors.ranked"),
      bookings: notImplemented("tutors.bookings"),
      verificationQueue: notImplemented("tutors.verificationQueue")
    },
    seo: { status: notImplemented("seo.status"), liveCrawl: notImplemented("seo.liveCrawl") },
    quality: { privacy: notImplemented("quality.privacy"), brokenLinks: notImplemented("quality.brokenLinks"),
               build: notImplemented("quality.build") },
    analytics: { summary: notImplemented("analytics.summary"), events: notImplemented("analytics.events"),
                 dashboardUrl: notImplemented("analytics.dashboardUrl") }
  };

  /* Choose the implementation. Today there is exactly one. */
  function pick() {
    var cfg = SITE.adminApi || {};
    if (cfg.baseUrl && cfg.enabled) {
      ApiRepository.baseUrl = cfg.baseUrl;
      return ApiRepository;
    }
    return {
      mode: "static",
      content: StaticContentRepository,
      tutors: StaticTutorRepository,
      seo: StaticSeoRepository,
      quality: StaticQualityRepository,
      analytics: StaticAnalyticsRepository
    };
  }

  var repo = pick();
  repo.data = data;
  repo.unavailable = unavailable;
  window.EkGuruAdmin = repo;
})();

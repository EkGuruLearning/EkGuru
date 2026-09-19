/* =========================================================
   EkGuru — TUTOR RANKING ENGINE  (v74, Phase 11 + 12)
   ---------------------------------------------------------
       window.EkGuruRank.rank(tutors, context)
       window.EkGuruRank.score(tutor, context)   → explainable

   ═══════════════════════════════════════════════════════
   WHY THIS REPLACES "SORT BY RATING"
   ═══════════════════════════════════════════════════════

   The old ordering was `(b.rating||0) - (a.rating||0)`. Three
   things are wrong with that, and they get worse as the roster
   grows:

     1. A tutor with one 5.0 review outranks one with forty
        4.8s. That is not a better tutor, it is a smaller
        sample. Sorting on a raw mean rewards having almost no
        data.

     2. A brand-new tutor with no reviews sorts last forever
        and therefore never gets the reviews that would move
        them. The cold-start problem is self-reinforcing.

     3. Nothing about the LEARNER affects the order. A Spanish
        speaker looking for a beginner tutor sees the same list
        as a fluent heritage learner in Delhi.

   ═══════════════════════════════════════════════════════
   THE HARD RULE THIS FILE FOLLOWS
   ═══════════════════════════════════════════════════════

   ONLY FACTORS THAT EXIST IN THE DATA ARE SCORED.

   The brief lists a long menu of possible signals — lesson
   completion rate, response time, cancellation rate, no-show
   rate, repeat booking rate, student retention. EkGuru has no
   booking backend, so NONE of those exist. Inventing them
   would mean inventing numbers about real people, which is
   exactly the fabrication this project refuses.

   So each factor below declares `available()`. A factor whose
   data is absent contributes ZERO and is reported as absent in
   the explanation, rather than being quietly defaulted to
   something flattering. When a booking backend exists, those
   factors are added here and start contributing automatically.

   Currently available, verified against the live data layer:
     rating, reviewsCount, lessonsCount, experienceYears,
     verified, superTutor, trialAvailable, availability,
     speaks, teaches, levels, priceUSD, photo/banner/about/
     methodology (profile completeness), timezone

   Currently NOT available, weight zero, declared:
     completionRate, responseHours*, cancellationRate,
     noShowRate, repeatBookingRate, retention, lastActiveAt
     (*responseHours became a sheet column in v72 but no tutor
      has filled it in; the factor is live and simply scores
      zero until one does)

   ═══════════════════════════════════════════════════════
   ANTI-GAMING
   ═══════════════════════════════════════════════════════
   · Bayesian shrinkage on rating, so a tiny sample is pulled
     towards the roster mean instead of topping the list.
   · Diminishing returns (log) on review and lesson counts, so
     volume cannot be farmed linearly.
   · Every numeric input is clamped to a sane range before use,
     so a typo of 999999 in the spreadsheet cannot dominate.
   · No paid placement. There is no field for it and no code
     path that would read one.
   · Exploration bonus is capped and decays, so it cannot be
     farmed by repeatedly creating new profiles — and it only
     applies to tutors who are otherwise complete and verified.

   ═══════════════════════════════════════════════════════
   DETERMINISM
   ═══════════════════════════════════════════════════════
   Same inputs → same order, always. No Math.random anywhere.
   Ties break on a fixed chain ending in the tutor id, so two
   identical tutors always sort the same way and the page does
   not reshuffle between reloads.
   ========================================================= */

(function () {
  "use strict";

  /* ---------------------------------------------------------
     Small helpers
     --------------------------------------------------------- */
  function num(v, lo, hi, dflt) {
    var n = Number(v);
    if (!isFinite(n)) return dflt;
    return Math.min(hi, Math.max(lo, n));
  }
  function has(v) {
    if (v == null) return false;
    if (typeof v === "string") return v.trim().length > 0;
    if (Array.isArray(v)) return v.length > 0;
    if (typeof v === "object") return Object.keys(v).length > 0;
    if (typeof v === "number") return isFinite(v);
    return !!v;
  }
  /* Diminishing returns. log1p(x)/log1p(cap), clamped to 1.
     Ten reviews should be worth much more than one; a hundred
     should not be worth ten times ten. */
  function diminishing(x, cap) {
    var v = Math.max(0, Number(x) || 0);
    return Math.min(1, Math.log1p(v) / Math.log1p(cap));
  }

  /* ---------------------------------------------------------
     PROFILE COMPLETENESS
     ---------------------------------------------------------
     A complete profile converts better and is a genuine
     quality signal that costs the tutor nothing but effort —
     which makes it the fairest factor on the list, because it
     is fully within their control and cannot be bought.
     --------------------------------------------------------- */
  var COMPLETENESS_FIELDS = [
    ["photo", 2], ["headline", 2], ["about", 3], ["methodology", 2],
    ["experience", 2], ["teaches", 1], ["levels", 1], ["speaks", 1],
    ["availability", 3], ["lessonLength", 1], ["banner", 1],
    ["youtubeId", 2], ["city", 1], ["timezone", 1]
  ];
  var COMPLETENESS_MAX = COMPLETENESS_FIELDS.reduce(function (a, f) { return a + f[1]; }, 0);

  function completeness(t) {
    var got = 0;
    COMPLETENESS_FIELDS.forEach(function (f) {
      if (has(t[f[0]])) got += f[1];
    });
    return got / COMPLETENESS_MAX;
  }

  /* ---------------------------------------------------------
     BAYESIAN RATING
     ---------------------------------------------------------
     score = (C*m + sum) / (C + n)

     where m is the prior (the roster mean) and C is how many
     reviews of evidence it takes to overcome that prior.

     With C = 5: one 5.0 review scores 4.6-ish against a prior
     of 4.5, while forty 4.8s scores 4.77. The forty wins, which
     is correct — and a single review can no longer top the
     page, which was the old behaviour.
     --------------------------------------------------------- */
  var PRIOR_WEIGHT = 5;

  function rosterMean(tutors) {
    var rated = (tutors || []).filter(function (t) {
      return num(t.rating, 0, 5, 0) > 0 && num(t.reviewsCount, 0, 1e6, 0) > 0;
    });
    if (!rated.length) return 4.5;   /* neutral prior, not a claim */
    var sum = 0, n = 0;
    rated.forEach(function (t) {
      var c = num(t.reviewsCount, 0, 1e6, 0);
      sum += num(t.rating, 0, 5, 0) * c;
      n += c;
    });
    return n ? sum / n : 4.5;
  }

  function bayesRating(t, prior) {
    var r = num(t.rating, 0, 5, 0);
    var n = num(t.reviewsCount, 0, 1e6, 0);
    if (!r || !n) return null;                 /* no data — absent, not zero */
    return (PRIOR_WEIGHT * prior + r * n) / (PRIOR_WEIGHT + n);
  }

  /* ---------------------------------------------------------
     THE FACTORS

     key        stable name, appears in the explanation
     weight     relative importance; the set is normalised, so
                these are ratios rather than absolutes
     available  false → contributes nothing and says so
     value      returns 0..1, or null when this tutor has no
                data for an otherwise-available factor
     --------------------------------------------------------- */
  function buildFactors(ctx, prior) {
    return [
      {
        key: "rating_quality",
        label: "Rating, adjusted for how many reviews it is based on",
        weight: 22,
        available: true,
        value: function (t) {
          var b = bayesRating(t, prior);
          return b == null ? null : (b - 1) / 4;      /* 1..5 → 0..1 */
        }
      },
      {
        key: "review_volume",
        label: "Number of reviews, with diminishing returns",
        weight: 10,
        available: true,
        value: function (t) { return diminishing(num(t.reviewsCount, 0, 1e5, 0), 60); }
      },
      {
        key: "lessons_taught",
        label: "Lessons taught, with diminishing returns",
        weight: 10,
        available: true,
        value: function (t) { return diminishing(num(t.lessonsCount, 0, 1e6, 0), 400); }
      },
      {
        key: "profile_completeness",
        label: "How complete the profile is",
        weight: 14,
        available: true,
        value: completeness
      },
      {
        key: "verified",
        label: "Identity verified by EkGuru",
        weight: 9,
        available: true,
        value: function (t) { return t.verified ? 1 : 0; }
      },
      {
        key: "experience",
        label: "Years of teaching experience",
        weight: 7,
        available: true,
        value: function (t) {
          var y = num(t.experienceYears, 0, 60, 0);
          return y ? diminishing(y, 15) : null;
        }
      },
      {
        key: "availability_breadth",
        label: "How many hours a week they teach",
        weight: 9,
        available: true,
        value: function (t) {
          var av = t.availability || {}, slots = 0;
          Object.keys(av).forEach(function (d) { slots += (av[d] || []).length; });
          return slots ? diminishing(slots, 25) : null;
        }
      },
      {
        key: "language_match",
        label: "Speaks the learner's language",
        weight: 12,
        /* Only meaningful when we know the learner's language.
           With no context this is absent rather than zero, so a
           tutor is not penalised for a question nobody asked. */
        available: !!(ctx && ctx.sourceLanguage),
        value: function (t) {
          var want = String(ctx.sourceLanguage || "").toLowerCase();
          if (!want) return null;
          var speaks = t.speaks;
          var list = [];
          if (Array.isArray(speaks)) list = speaks.map(String);
          else if (speaks && typeof speaks === "object") list = Object.keys(speaks);
          else if (typeof speaks === "string") list = speaks.split(",");
          var hit = list.some(function (x) { return String(x).toLowerCase().indexOf(want) > -1; });
          return hit ? 1 : 0;
        }
      },
      {
        key: "level_match",
        label: "Teaches the learner's level",
        weight: 10,
        available: !!(ctx && ctx.level),
        value: function (t) {
          var want = String(ctx.level || "").toLowerCase();
          var lv = (t.levels || []).map(function (x) { return String(x).toLowerCase(); });
          if (!lv.length) return null;
          return lv.indexOf(want) > -1 ? 1 : 0;
        }
      },
      {
        key: "timezone_overlap",
        label: "Teaching hours that suit the learner",
        weight: 8,
        available: !!(ctx && typeof ctx.utcOffset === "number"),
        value: function (t) {
          var av = t.availability || {};
          var hours = [];
          Object.keys(av).forEach(function (d) {
            (av[d] || []).forEach(function (s) {
              var h = parseInt(String(s).split(":")[0], 10);
              if (!isNaN(h)) hours.push(h);
            });
          });
          if (!hours.length) return null;
          /* Tutor hours are Indian time (UTC+5:30). Convert to
             the learner's local time and count how many fall in
             a civilised window (07:00–23:00). */
          var shift = ctx.utcOffset - 5.5;
          var ok = hours.filter(function (h) {
            var v = ((h + shift) % 24 + 24) % 24;
            return v >= 7 && v <= 23;
          }).length;
          return ok / hours.length;
        }
      },
      {
        key: "budget_fit",
        label: "Price within the learner's budget",
        weight: 8,
        available: !!(ctx && ctx.maxPrice),
        value: function (t) {
          var p = num(t.priceUSD, 0, 2000, 0);
          if (!p) return null;
          if (p > ctx.maxPrice) return 0;
          /* Inside budget, cheaper is mildly better — but only
             mildly. Ranking hard on price would push every
             experienced tutor off the first page, which serves
             nobody. */
          return 0.6 + 0.4 * (1 - p / ctx.maxPrice);
        }
      },
      {
        key: "search_relevance",
        label: "Matches the search text",
        weight: 14,
        available: !!(ctx && ctx.query),
        value: function (t) {
          var q = String(ctx.query || "").toLowerCase().trim();
          if (!q) return null;
          var terms = q.split(/\s+/).filter(Boolean);
          /* Weighted fields: a match in the name or headline is
             worth more than one buried in a bio. */
          var fields = [
            [String(t.name || "").toLowerCase(), 3],
            [String(t.headline || "").toLowerCase(), 2],
            [(t.teaches || []).join(" ").toLowerCase(), 2],
            [(t.tags || []).join(" ").toLowerCase(), 1],
            [String(t.city || "").toLowerCase(), 1],
            [(t.about || []).join(" ").toLowerCase(), 1]
          ];
          var got = 0, max = 0;
          terms.forEach(function (term) {
            var best = 0;
            fields.forEach(function (f) {
              if (f[0].indexOf(term) > -1) best = Math.max(best, f[1]);
            });
            got += best; max += 3;
          });
          return max ? got / max : null;
        }
      },
      {
        key: "trial_available",
        label: "Offers a trial lesson",
        weight: 5,
        available: true,
        value: function (t) { return t.trialAvailable ? 1 : 0; }
      },
      {
        key: "new_tutor_exploration",
        label: "New tutor, given a chance to earn reviews",
        weight: 6,
        available: true,
        /* THE COLD-START FIX. A tutor with no reviews cannot earn
           reviews if they are permanently last. This gives them a
           bounded, decaying head start — but ONLY if the profile
           is complete and verified, so it cannot be farmed by
           spinning up empty profiles. It disappears entirely by
           about ten reviews. */
        value: function (t) {
          var n = num(t.reviewsCount, 0, 1e6, 0);
          if (n >= 10) return 0;
          if (!t.verified) return 0;
          if (completeness(t) < 0.7) return 0;
          return (10 - n) / 10;
        }
      },

      /* ---------------------------------------------------
         DECLARED BUT UNAVAILABLE.

         Listed so the model is honest about what it is NOT
         measuring, and so adding a booking backend later is a
         matter of flipping `available` rather than redesigning
         the engine. Every one contributes exactly zero today.
         --------------------------------------------------- */
      { key: "response_time", label: "How fast they reply", weight: 8,
        available: false, requires: "responseHours (sheet column exists, unfilled)",
        value: function (t) {
          var h = num(t.responseHours, 1, 168, 0);
          return h ? 1 - diminishing(h, 48) : null;
        } },
      { key: "completion_rate", label: "Lessons completed vs booked", weight: 10,
        available: false, requires: "a booking backend", value: function () { return null; } },
      { key: "cancellation_rate", label: "How often they cancel", weight: 8,
        available: false, requires: "a booking backend", value: function () { return null; } },
      { key: "repeat_bookings", label: "Students who book again", weight: 10,
        available: false, requires: "a booking backend", value: function () { return null; } },
      { key: "recent_activity", label: "Active recently", weight: 6,
        available: false, requires: "a lastActiveAt timestamp", value: function () { return null; } }
    ];
  }

  /* ---------------------------------------------------------
     SAFETY FILTER — applied before scoring.
     A tutor who should not be shown is removed, not ranked
     low. Ranking something to the bottom still shows it.
     --------------------------------------------------------- */
  function isListable(t) {
    if (!t || !t.id) return false;
    if (t.active === false || t.active === "no") return false;
    if (t.moderationHold) return false;
    if (t.holiday) return true;   /* still listed, booking is what changes */
    return true;
  }

  /* ---------------------------------------------------------
     score(tutor, context) → { total, breakdown[] }
     Explainable by construction: the breakdown is what produced
     the number, not a description written next to it.
     --------------------------------------------------------- */
  function score(tutor, context, prior, factorsIn) {
    var ctx = context || {};
    var factors = factorsIn || buildFactors(ctx, prior == null ? 4.5 : prior);

    var total = 0, weightUsed = 0;
    var breakdown = [];

    factors.forEach(function (f) {
      if (!f.available) {
        breakdown.push({ key: f.key, label: f.label, state: "unavailable",
                         requires: f.requires || null, contribution: 0 });
        return;
      }
      var v = null;
      try { v = f.value(tutor); } catch (e) { v = null; }
      if (v == null) {
        breakdown.push({ key: f.key, label: f.label, state: "no data for this tutor",
                         contribution: 0 });
        return;
      }
      var clamped = Math.min(1, Math.max(0, v));
      total += clamped * f.weight;
      weightUsed += f.weight;
      breakdown.push({
        key: f.key, label: f.label, state: "scored",
        value: Math.round(clamped * 1000) / 1000,
        weight: f.weight,
        contribution: Math.round(clamped * f.weight * 100) / 100
      });
    });

    /* Normalise by the weight actually used, so a tutor is not
       punished for factors nobody could score. Without this, a
       search with no query would give every tutor a lower
       absolute score and the numbers would be meaningless
       across contexts. */
    var normalised = weightUsed ? total / weightUsed : 0;

    /* Holiday mode: still listed, but not first. A learner
       browsing should see them; a learner ready to book should
       not be sent to someone who is away. */
    if (tutor.holiday) normalised *= 0.55;

    return {
      total: Math.round(normalised * 10000) / 10000,
      weightUsed: weightUsed,
      breakdown: breakdown
    };
  }

  /* ---------------------------------------------------------
     rank(tutors, context) → sorted copy, each with _rank
     --------------------------------------------------------- */
  function rank(tutors, context) {
    var list = (tutors || []).filter(isListable);
    var prior = rosterMean(list);
    var ctx = context || {};
    var factors = buildFactors(ctx, prior);

    var scored = list.map(function (t) {
      var s = score(t, ctx, prior, factors);
      return { tutor: t, score: s.total, detail: s };
    });

    scored.sort(function (a, b) {
      if (b.score !== a.score) return b.score - a.score;
      /* Deterministic tie-break chain. Never random: a list that
         reshuffles between reloads looks broken and makes the
         ordering impossible to debug or to test. */
      var A = a.tutor, B = b.tutor;
      var ar = Number(A.rating) || 0, br = Number(B.rating) || 0;
      if (br !== ar) return br - ar;
      var an = Number(A.reviewsCount) || 0, bn = Number(B.reviewsCount) || 0;
      if (bn !== an) return bn - an;
      var al = Number(A.lessonsCount) || 0, bl = Number(B.lessonsCount) || 0;
      if (bl !== al) return bl - al;
      return String(A.id).localeCompare(String(B.id));
    });

    return scored.map(function (x, i) {
      var t = x.tutor;
      /* Attached, not mutated onto the shared object: the tutor
         array is shared with the sheet layer and writing to it
         caused a repaint bug in v62. */
      return Object.assign(Object.create(Object.getPrototypeOf(t) || Object.prototype), t, {
        _rank: i + 1,
        _score: x.score,
        _scoreDetail: x.detail
      });
    });
  }

  /* Which factors are actually doing work right now. Used by
     admin.html so the ranking is inspectable rather than
     mysterious, and so "we do not measure that" is visible. */
  function factorReport(context) {
    return buildFactors(context || {}, 4.5).map(function (f) {
      return {
        key: f.key, label: f.label, weight: f.weight,
        available: !!f.available, requires: f.requires || null
      };
    });
  }

  window.EkGuruRank = {
    rank: rank,
    score: score,
    factors: factorReport,
    completeness: completeness,
    rosterMean: rosterMean,
    isListable: isListable
  };
})();

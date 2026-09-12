/* =========================================================
   EkGuru — REVIEWS FROM A THIRD SHEET
   ---------------------------------------------------------
   WHY THIS IS A SEPARATE SHEET

   The tutor sheet has one row per tutor. A review does not
   fit that shape — one tutor has many reviews — so squeezing
   them into columns would mean review1, review2, review3 and
   a hard ceiling on how many anyone can have.

   One row per REVIEW solves it. Add a row, the review appears
   on that tutor's page within the hour, the star rating and
   review count recalculate themselves, and the AggregateRating
   schema updates with them.

   ---------------------------------------------------------
   ⚠️ THE ONLY RULE THAT MATTERS

   NEVER INVENT A REVIEW.

   Not one. Not "just to get started". Not a friend writing a
   nice thing about a tutor they have never studied with.

   Fake reviews are the single fastest way to destroy this
   site. Google's review spam policy treats them as deceptive
   content, and a manual action would take all 141 pages down
   with them — not just the tutor page that carried the fake.
   It is also illegal in the UK under the DMCC Act 2024 and
   actionable by the FTC in the US.

   Every real review is worth more than fifty invented ones,
   because a real one survives being checked.

   To make that harder to get wrong, this file:
     · refuses a row with no student name
     · refuses a rating outside 1–5
     · refuses a review under 40 characters
     · refuses a date in the future
     · marks every review with its source, so you always know
       where it came from

   ---------------------------------------------------------
   COLUMNS

     tutor    the tutor id, must match js/tutors/<id>.js
     name     the student's first name, as they gave it
     date     YYYY-MM-DD
     stars    1 to 5
     text     what they actually wrote
     source   where it came from — preply, email, whatsapp,
              google. Shown to nobody, kept for your records.
     status   live / hidden

   ---------------------------------------------------------
   HOW THE RATING IS CALCULATED

   Average of live reviews, to one decimal. reviewsCount
   becomes the number of live reviews. Both OVERRIDE whatever
   the tutor file says — the reviews are the source of truth,
   so the number on the page can never drift away from the
   reviews under it.

   A tutor with no reviews gets rating 0 and no stars shown,
   rather than a fabricated 5.0.
   ========================================================= */

(function (root) {
  "use strict";

  var S = root.EKGURU_SITE || {};
  var CFG = S.reviews || {};
  var url = String(CFG.csvUrl || "").trim();

  var CACHE_KEY = "ekguru_reviews_v1";
  var MAX_AGE = (Number(CFG.cacheMinutes) || 60) * 60 * 1000;

  /* Below this a "review" is a rating with a word attached, which is
     not social proof and does not read as genuine. */
  var MIN_TEXT = 40;

  /* ---------------------------------------------------------
     CSV parsing. Same hand-written parser as the other sheets:
     quoted fields, embedded commas, embedded newlines, doubled
     quotes. All four appear in real Google Sheets output.
     --------------------------------------------------------- */
  function parseCSV(text) {
    text = String(text).replace(/^\uFEFF/, "");
    var rows = [], row = [], field = "", q = false, i, c;
    for (i = 0; i < text.length; i++) {
      c = text.charAt(i);
      if (q) {
        if (c === '"') {
          if (text.charAt(i + 1) === '"') { field += '"'; i++; }
          else q = false;
        } else field += c;
      } else if (c === '"') q = true;
      else if (c === ",") { row.push(field); field = ""; }
      else if (c === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
      else if (c === "\r") { /* the \n after it does the work */ }
      else field += c;
    }
    if (field !== "" || row.length) { row.push(field); rows.push(row); }
    if (!rows.length) return [];

    var head = rows[0].map(function (h) { return h.trim().toLowerCase(); });
    return rows.slice(1).map(function (r) {
      var o = {};
      head.forEach(function (h, n) { o[h] = (r[n] || "").trim(); });
      return o;
    }).filter(function (o) {
      return Object.keys(o).some(function (k) { return o[k]; });
    });
  }

  /* ---------------------------------------------------------
     Validation. Every rejection is logged with a reason — a
     silently dropped review is the failure the tutor sheet had
     for eight columns, and it is worse here because you would
     think a real student's words had been published when they
     had not.
     --------------------------------------------------------- */
  function validate(r) {
    var why = [];
    if (!r.tutor) why.push("no tutor id");
    if (!r.name) why.push("no student name");

    var stars = Number(r.stars);
    if (!isFinite(stars) || stars < 1 || stars > 5) why.push('stars must be 1-5, got "' + r.stars + '"');

    var text = String(r.text || "").trim();
    if (!text) why.push("no review text");
    else if (text.length < MIN_TEXT)
      why.push("the text is " + text.length + " characters — at least " + MIN_TEXT +
        " is needed for it to read as a real review");

    if (r.date) {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(r.date)) why.push('date must be YYYY-MM-DD, got "' + r.date + '"');
      else if (new Date(r.date).getTime() > Date.now() + 86400000)
        why.push("the date is in the future");
    }
    return why;
  }

  function readCache() {
    try {
      var raw = localStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      var c = JSON.parse(raw);
      if (!c || !c.t || !Array.isArray(c.recs)) return null;
      return { stale: Date.now() - c.t > MAX_AGE, recs: c.recs };
    } catch (e) { return null; }
  }
  function writeCache(recs) {
    try { localStorage.setItem(CACHE_KEY, JSON.stringify({ t: Date.now(), recs: recs })); }
    catch (e) {}
  }

  /* ---------------------------------------------------------
     Apply. The reviews become the source of truth for rating
     and reviewsCount, so the star figure on a page can never
     disagree with the reviews printed under it.
     --------------------------------------------------------- */
  /* =========================================================
     THE LAST ROWS WE READ  (v62)
     ---------------------------------------------------------
     BUG FOUND v62 — A RACE THAT SILENTLY LOST REAL REVIEWS.

     Two sheets are fetched in parallel and there is no order
     guarantee between them. The tutor sheet can now CREATE a
     tutor (v62), so this sequence is entirely normal:

       t=180ms  the reviews sheet answers first
                → "priya" does not exist yet
                → her reviews are logged as "unknown tutor id"
                  and thrown away
       t=400ms  the tutor sheet answers
                → priya is created, with zero reviews, forever

     Nothing retried, so a genuine review was lost for the whole
     page view. On a slow connection this is a coin flip, and it
     fails in the direction that looks like the reviews sheet is
     broken.

     Fix: keep the rows and re-apply them whenever the tutor list
     changes. apply() is idempotent — it rebuilds each tutor's
     review list from scratch every time — so running it again is
     free and cannot double-count.
     ========================================================= */
  var LAST_RECS = null;

  function apply(recs) {
    if (recs) LAST_RECS = recs;
    recs = recs || LAST_RECS || [];

    var T = root.EKGURU_TUTORS || [];
    var byTutor = {}, unknown = [], skipped = [];

    /* An id is a filename and a URL, both lowercase. v62 found the
       same bug on the tutor sheet: typing "Sushila-G" — which anyone
       would, it is a name — meant the row did not match and the
       review was dropped as an unknown id. Match case-insensitively
       and store under the tutor's real id. */
    var byLower = {};
    T.forEach(function (x) { byLower[String(x.id).toLowerCase()] = x; });

    recs.forEach(function (r) {
      if (String(r.tutor || "").charAt(0) === "#") return;      /* help row */
      var status = String(r.status || "live").toLowerCase();
      if (status !== "live") return;

      var why = validate(r);
      if (why.length) { skipped.push([r.tutor + "/" + (r.name || "?"), why]); return; }

      var t = byLower[String(r.tutor || "").trim().toLowerCase()];
      if (!t) { if (unknown.indexOf(r.tutor) === -1) unknown.push(r.tutor); return; }

      (byTutor[t.id] = byTutor[t.id] || []).push({
        name: String(r.name).trim(),
        date: r.date || "",
        stars: Number(r.stars),
        text: String(r.text).trim(),
        /* Kept so you can always tell where a review came from.
           Not rendered anywhere — it is a record, not a badge. */
        source: String(r.source || "").trim()
      });
    });

    /* BUG FOUND v60 — A RATING WITH NO REVIEWS BEHIND IT.

       Three tutor files carry rating: 5 and reviewsCount: 0. The
       renderers check reviewsCount before printing stars, so nothing
       showed — but the DATA said 5.0, and the moment anything else
       read t.rating without checking the count it would have printed
       a five-star average that no student ever gave.

       Since this file makes the reviews the source of truth, it must
       also enforce the other direction: a tutor with no live reviews
       has no rating. Zero, not five. */
    T.forEach(function (t) {
      if (!byTutor[t.id]) {
        t.reviews = [];
        t.reviewsCount = 0;
        t.rating = 0;
      }
    });

    var applied = 0;
    Object.keys(byTutor).forEach(function (id) {
      var t = T.filter(function (x) { return x.id === id; })[0];
      if (!t) return;
      var list = byTutor[id];

      /* Newest first, so a tutor's most recent work is what a
         visitor reads. Undated reviews sort last rather than
         being dropped. */
      list.sort(function (a, b) { return (b.date || "").localeCompare(a.date || ""); });

      t.reviews = list;
      t.reviewsCount = list.length;
      var sum = list.reduce(function (n, r) { return n + r.stars; }, 0);
      t.rating = Math.round((sum / list.length) * 10) / 10;
      applied++;
    });

    if (skipped.length && root.console && console.warn) {
      skipped.forEach(function (s) {
        console.warn("[EkGuru] review skipped — " + s[0] + ": " + s[1].join("; "));
      });
    }
    if (unknown.length && root.console && console.warn) {
      console.warn("[EkGuru] reviews for unknown tutor id(s): " + unknown.join(", ") +
        ". An id must match a file in js/tutors/.");
    }

    root.EKGURU_REVIEWS_INFO = {
      loaded: true,
      rows: recs.length,
      tutors: applied,
      published: Object.keys(byTutor).reduce(function (n, k) { return n + byTutor[k].length; }, 0),
      skipped: skipped.length,
      unknown: unknown,
      at: new Date().toISOString()
    };
    return applied;
  }

  function announce() {
    try { root.dispatchEvent(new CustomEvent("ekguru:reviews")); }
    catch (e) {
      try {
        var ev = document.createEvent("Event");
        ev.initEvent("ekguru:reviews", true, true);
        root.dispatchEvent(ev);
      } catch (e2) {}
    }
  }

  function fetchSheet() {
    var ctrl = null, timer = null;
    try { ctrl = new AbortController(); } catch (e) {}
    if (ctrl) timer = setTimeout(function () { try { ctrl.abort(); } catch (e) {} }, 8000);

    return root.fetch(url, { signal: ctrl ? ctrl.signal : undefined, cache: "default" })
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.text();
      })
      .then(function (csv) {
        if (timer) clearTimeout(timer);
        if (/^\s*<!DOCTYPE|^\s*<html/i.test(csv)) {
          throw new Error("that URL returned a web page, not CSV — use Publish to web → CSV");
        }
        var recs = parseCSV(csv);
        if (!recs.length) throw new Error("no rows");
        writeCache(recs);
        apply(recs);
        announce();
      })
      .catch(function (e) {
        if (timer) clearTimeout(timer);
        if (root.console && console.warn) {
          console.warn("[EkGuru] reviews sheet not loaded: " + e.message +
            " — the tutor files are being used instead.");
        }
        root.EKGURU_REVIEWS_INFO = { loaded: false, error: e.message };
      });
  }

  /* The API is published whether or not a sheet is configured —
     the same lesson as v57, where an early return meant the admin
     dashboard called a function that did not exist. */
  root.EkGuruReviews = {
    info: function () { return root.EKGURU_REVIEWS_INFO || { loaded: false }; },
    refresh: function () {
      try { localStorage.removeItem(CACHE_KEY); } catch (e) {}
      return url ? fetchSheet() : Promise.resolve();
    },
    validate: validate,
    MIN_TEXT: MIN_TEXT
  };

  if (!url) return;
  if (typeof root.fetch !== "function") return;

  /* v62: same stale-while-revalidate change as js/sheet.js. A cache
     under an hour old used to block the fetch entirely, so a review
     added in the morning could be invisible all afternoon to anyone
     who had already loaded the page once. The cached copy still
     paints first, so nothing gets slower; the fetch just always
     happens behind it. */
  var cached = readCache();
  if (cached) {
    apply(cached.recs);
    announce();
    if (cached.stale || CFG.alwaysRevalidate !== false) fetchSheet();
  } else {
    fetchSheet();
  }

  /* =========================================================
     RE-APPLY WHEN THE TUTOR LIST CHANGES  (v62)
     ---------------------------------------------------------
     See the long note on LAST_RECS above. The tutor sheet can
     create, hide and restore tutors after this file has already
     run, and every one of those changes the answer to "whose
     reviews are these".

       created   her reviews were dropped as an unknown id
       restored  the same, on the second fetch
       hidden    her reviews stayed attached to an object nobody
                 renders, which is harmless, but the counts in
                 EKGURU_REVIEWS_INFO were then wrong

     Re-applying is cheap and idempotent — each tutor's list is
     rebuilt from scratch — so it cannot double-count.

     ⚠️ It must NOT announce() unconditionally afterwards. main.js
     repaints on ekguru:reviews and js/sheet.js has just fired
     ekguru:sheet, which main.js also repaints on. Announcing here
     would repaint twice for one change, and a repaint resets CSS
     animations. Only announce when something actually moved. */
  root.addEventListener("ekguru:sheet", function () {
    if (!LAST_RECS) return;
    var before = JSON.stringify((root.EKGURU_TUTORS || [])
      .map(function (t) { return t.id + ":" + (t.reviewsCount || 0) + ":" + (t.rating || 0); }));
    apply(null);
    var after = JSON.stringify((root.EKGURU_TUTORS || [])
      .map(function (t) { return t.id + ":" + (t.reviewsCount || 0) + ":" + (t.rating || 0); }));
    if (before !== after) announce();
  });

})(typeof window !== "undefined" ? window : globalThis);

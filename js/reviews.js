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
     source   where it came from — email, whatsapp, google.
              Kept for your records. Rows with an external
              marketplace as the source (preply, italki) are
              NEVER published and never feed the rating, by
              policy (27 Sep 2026 master audit): a review is
              only EkGuru's if an EkGuru student left it here.
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

  /* Live feed (28 Oct 2026). Same function as js/sheet.js and
     js/settings.js; tools/test-live-feed.js asserts all three agree.
     Blank or malformed S.feed.url means the feed is off. */
  function feedUrl(tab) {
    var F = S.feed || {};
    var base = String(F.url || "").trim();
    if (!/^https:\/\/script\.google\.com\/macros\/s\/[A-Za-z0-9_-]+\/exec$/.test(base)) return "";
    var sec = Number(F.cacheSeconds) > 0 ? Number(F.cacheSeconds) : 30;
    return base + "?tab=" + encodeURIComponent(tab) + "&t=" + Math.floor(Date.now() / (sec * 1000));
  }

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
    return rowsToRecs(rows);
  }

  /* Header row becomes object keys; blank rows are dropped. Shared by
     the CSV and TSV parsers so both formats yield identical records. */
  function rowsToRecs(rows) {
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

  /* Google's TSV export of a published tab: no quoting, one row per
     line, cells split on tabs. Only used as a fallback (below). */
  function parseTSV(text) {
    text = String(text).replace(/^\uFEFF/, "");
    var rows = [];
    var lines = text.split("\n");
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].replace(/\r$/, "");
      if (!line && i === lines.length - 1) continue;
      rows.push(line.split("\t"));
    }
    return rowsToRecs(rows);
  }

  function tsvVariant(u) {
    u = String(u || "");
    if (/[?&]output=/.test(u)) return u.replace(/([?&])output=[^&]*/, "$1output=tsv");
    return u + (u.indexOf("?") === -1 ? "?" : "&") + "output=tsv";
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

  /* Tutor ids whose EKGURU_TUTOR_FILES entry this file wrote. Only
     these are ever cleared when their rows leave the sheet — baked
     tutor-file data is left alone (see the FILES section in apply). */
  var APPLIED_FILES = {};

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

    /* =========================================================
       KNOWN IDS BEYOND THE ROSTER  (4 Nov 2026)
       ---------------------------------------------------------
       BUG FOUND — REVIEWS NEVER SHOWED ON PROFILE PAGES.

       A pre-rendered profile loads this file WITHOUT
       js/tutors-data.js, so EKGURU_TUTORS does not exist there —
       and js/sheet.js deliberately publishes only _recordOnly
       stubs (EKGURU_SHEET_RECORDS) on such pages, never roster
       entries. Matching reviews against the roster alone therefore
       dropped EVERY review on exactly the pages that print review
       lists: "No reviews yet" on Sushila's live profile while the
       sheet held two live rows for her.

       A review row may also name any id the page and the sheet
       already agree exists: the sheet's record stubs, the baked
       overrides, the registry order, or the page's own
       [data-tutor] attributes (the DOM is parsed before this
       runs, so that source works even on the first apply, before
       the sheet arrives). Genuinely unknown ids — typos for
       tutors nowhere on the page — are still reported below.
       ========================================================= */
    var knownByLower = {};
    function learnId(id) {
      id = String(id == null ? "" : id).trim();
      if (id && !knownByLower[id.toLowerCase()]) knownByLower[id.toLowerCase()] = id;
    }
    Object.keys(root.EKGURU_SHEET_RECORDS || {}).forEach(learnId);
    Object.keys(root.EKGURU_SHEET_OVERRIDES || {}).forEach(learnId);
    (root.EKGURU_TUTOR_ORDER || []).forEach(learnId);
    try {
      var tutorNodes = root.document.querySelectorAll("[data-tutor]");
      Array.prototype.forEach.call(tutorNodes, function (n) {
        learnId(n.getAttribute("data-tutor"));
      });
    } catch (e) {}

    /* =========================================================
       EXTERNAL-MARKETPLACE GATE  (27 Sep 2026 master audit)
       ---------------------------------------------------------
       A review row with source=preply (or italki, or any other
       external marketplace) is a review WRITTEN BY THAT
       MARKETPLACE'S USERS ON THAT MARKETPLACE. Publishing it —
       even with an attribution line — is still publishing
       copied third-party content, and the rating it feeds is a
       rating EkGuru never earned. This is the code-level
       enforcement of the 26 Sep 2026 decision recorded in
       js/tutors/sushila-g.js ("removed, not reworded").

       It runs here, at the single point where every published
       review passes, so a stale live sheet row with
       source=preply/status=live can never set a star rating or
       review count again — the failure this audit found live on
       ekguru.shop on 27 Sep 2026 (5.0 / 3 reviews / 40 lessons
       re-appearing from the sheet).

       Site-native sources (email, whatsapp, google, blank) are
       untouched: the owner can add real on-site reviews any
       time, and they publish as before.
       ========================================================= */
    var MARKETPLACE_SOURCES = ["preply", "italki"];

    recs.forEach(function (r) {
      if (String(r.tutor || "").charAt(0) === "#") return;      /* help row */
      var status = String(r.status || "live").toLowerCase();
      if (status !== "live") return;

      var src = String(r.source || "").trim().toLowerCase();
      if (MARKETPLACE_SOURCES.indexOf(src) !== -1) {
        skipped.push([
          r.tutor + "/" + (r.name || "?"),
          ["external-marketplace source (\"" + src + "\") — never published; site-native reviews only (27 Sep 2026 policy)"]
        ]);
        return;
      }

      var why = validate(r);
      if (why.length) { skipped.push([r.tutor + "/" + (r.name || "?"), why]); return; }

      var rowKey = String(r.tutor || "").trim().toLowerCase();
      var t = byLower[rowKey];
      /* Roster first; on roster-less pages any id the page/sheet
         already names (see KNOWN IDS above). */
      var realId = t ? t.id : (knownByLower[rowKey] || null);
      if (!realId) { if (unknown.indexOf(r.tutor) === -1) unknown.push(r.tutor); return; }

      (byTutor[realId] = byTutor[realId] || []).push({
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

    /* Also expose reviews on EKGURU_TUTOR_FILES so pre-rendered
       tutor pages (which deliberately do not load tutors-data.js
       or individual tutor files) can still show reviews.
       reviews-display.js reads from EKGURU_TUTOR_FILES, so without
       this step a tutor page with live reviews in the sheet would
       always print "No reviews yet". */
    var FILES = root.EKGURU_TUTOR_FILES || {};
    Object.keys(byTutor).forEach(function (id) {
      var f = FILES[id];
      if (!f) {
        f = { id: id, reviews: [], reviewsCount: 0, rating: 0 };
        FILES[id] = f;
      }
      var list = byTutor[id].slice();
      list.sort(function (a, b) { return (b.date || "").localeCompare(a.date || ""); });
      f.reviews = list;
      f.reviewsCount = list.length;
      var sum = list.reduce(function (n, r) { return n + r.stars; }, 0);
      f.rating = Math.round((sum / list.length) * 10) / 10;
      APPLIED_FILES[id] = 1;
    });
    /* A review removed from the sheet must disappear here too — but
       only entries THIS function wrote are ever cleared, so baked
       tutor-file data is never wiped by an empty sheet. */
    Object.keys(APPLIED_FILES).forEach(function (id) {
      if (!byTutor[id] && FILES[id]) {
        FILES[id].reviews = [];
        FILES[id].reviewsCount = 0;
        FILES[id].rating = 0;
      }
    });
    root.EKGURU_TUTOR_FILES = FILES;

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

  function fetchRecords(u, fmt) {
    var ctrl = null, timer = null;
    try { ctrl = new AbortController(); } catch (e) {}
    if (ctrl) timer = setTimeout(function () { try { ctrl.abort(); } catch (e) {} }, 8000);

    return root.fetch(u, { signal: ctrl ? ctrl.signal : undefined, cache: "default" })
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.text();
      })
      .then(function (body) {
        if (timer) clearTimeout(timer);
        if (/^\s*<!DOCTYPE|^\s*<html/i.test(body)) {
          throw new Error("that URL returned a web page, not " + (fmt === "tsv" ? "TSV" : "CSV") + " — use Publish to web");
        }
        var recs = fmt === "tsv" ? parseTSV(body) : parseCSV(body);
        if (!recs.length) throw new Error("no rows");
        return recs;
      })
      .catch(function (e) { if (timer) clearTimeout(timer); throw e; });
  }

  /* Published CSV first, then the SAME tab as TSV. Google's published-
     CSV endpoint answers HTTP 500 for this workbook while output=tsv
     answers 200 (seen 30 Sep 2026 — js/sheet.js and js/settings.js
     already carried this fallback; reviews was missing it, so a dead
     CSV endpoint meant NO live review ever reached the browser). */
  function fetchPublished(csv) {
    return fetchRecords(csv, "csv").catch(function (eCsv) {
      return fetchRecords(tsvVariant(csv), "tsv").catch(function (eTsv) {
        throw new Error(eCsv.message + " / " + eTsv.message);
      });
    });
  }

  function fetchSheet() {
    /* SHEET-LIVE ONLY (owner decision, Nov 2026): the live feed first
       (if configured), then the published reviews tab (CSV→TSV). There
       is deliberately no baked snapshot step — the old
       live-sheets/reviews.csv snapshot was permanently deleted, so
       every review on every page comes from the live sheet, in real
       time, on every page load. If Google is unreachable the page
       honestly shows no reviews rather than stale baked ones. */
    var f = feedUrl("reviews");
    var live = function () {
      return url ? fetchPublished(url) : Promise.reject(new Error("no reviews url"));
    };
    var first = f ? fetchRecords(f, "csv").catch(live) : live();
    return first
      .then(function (recs) {
        writeCache(recs);
        apply(recs);
        announce();
      })
      .catch(function (e) {
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
      return (url || feedUrl("reviews")) ? fetchSheet() : Promise.resolve();
    },
    validate: validate,
    MIN_TEXT: MIN_TEXT
  };

  if (!url && !feedUrl("reviews")) return;
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
    /* Profile pages have no EKGURU_TUTORS, so a roster-only snapshot
       would read "[]" before and after and swallow the announce that
       repaints their review lists. Include the FILES entries too. */
    function snap() {
      var roster = (root.EKGURU_TUTORS || [])
        .map(function (t) { return t.id + ":" + (t.reviewsCount || 0) + ":" + (t.rating || 0); });
      var files = Object.keys(root.EKGURU_TUTOR_FILES || {}).sort()
        .map(function (id) {
          var f = root.EKGURU_TUTOR_FILES[id] || {};
          return id + ":" + (f.reviewsCount || 0) + ":" + (f.rating || 0);
        });
      return JSON.stringify(roster) + "|" + JSON.stringify(files);
    }
    var before = snap();
    apply(null);
    if (before !== snap()) announce();
  });

})(typeof window !== "undefined" ? window : globalThis);

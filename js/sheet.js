/* =========================================================
   EkGuru — GOOGLE SHEET AS A LIVE DATA SOURCE
   ---------------------------------------------------------
   WHAT THIS DOES

   Lets you edit tutor details in a Google Sheet and have the
   live site pick them up, without touching a file or pushing
   anything.

   Change a price in the Sheet, and within an hour every
   visitor sees the new price. Add a tutor's video link, mark
   someone unavailable, correct a typo in a bio — all from a
   spreadsheet on your phone.

   ---------------------------------------------------------
   HOW IT WORKS, AND ITS ONE REAL LIMITATION

   Google can publish a Sheet as a CSV at a public URL. A
   static page can fetch that URL and read it. No server, no
   API key, no account for the visitor.

   The limitation, stated plainly: **this only updates what
   JavaScript renders.** The pre-rendered pages under /tutor/,
   the sitemap and the structured data are built by the tools
   and still need a rebuild. So:

     Sheet changes  ->  visible immediately to people
     Sheet changes  ->  NOT in the pre-rendered HTML Google
                        reads, until you run the build

   That makes the Sheet right for prices, availability, video
   links and small corrections. For a whole new tutor, still
   use tools/addtutor.js — that generates their page, their
   schema and their sitemap entry, which a spreadsheet cannot.

   ---------------------------------------------------------
   THE SHEET

   Row 1 must be the headers. Only "id" is required; every
   other column is optional and overrides that field:

     id | name | priceUSD | lessonLength | headline | city
     video | whatsapp | email | active | bio | tags | teaches

     · id        must match js/tutors/<id>.js exactly
     · video     the 11-character YouTube id, not the full URL
     · active    put "no" or "false" to hide a tutor entirely
     · tags      comma separated
     · teaches   comma separated
     · blank     a blank cell changes nothing, it does not
                 erase the value in the tutor file

   ---------------------------------------------------------
   TO SWITCH ON

     1. Make a Google Sheet with those headers
     2. File -> Share -> Publish to web
     3. Choose the sheet, format "Comma-separated values (.csv)"
     4. Copy the URL it gives you
     5. Paste it into js/site-config.js:

          sheet: { csvUrl: "https://docs.google.com/…/pub?output=csv" }

   Leave it blank and nothing is fetched — the tutor files are
   the only source, exactly as now.

   ⚠️ A published Sheet is PUBLIC to anyone with the link. Do
   not put anything private in it. Tutor phone numbers are
   stripped by js/tutors-data.js regardless, deliberately.
   ========================================================= */

(function () {
  "use strict";

  var S = window.EKGURU_SITE || {};
  var CFG = S.sheet || {};
  var url = String(CFG.csvUrl || "").trim();

  var CACHE_KEY = "ekguru_sheet_v1";
  var MAX_AGE = (Number(CFG.cacheMinutes) || 60) * 60 * 1000;

  /* =========================================================
     v62 — "CHANGE KARTE HI DIKHNA CHAHIYE"
     ---------------------------------------------------------
     BUG FOUND v62, and it is the reason sheet edits felt slow
     or dead even after v61 made the BUILD read the sheet.

     Timeline on a real visit, before this fix:

       t=0ms    tutor files load, EKGURU_TUTORS exists
       t=1ms    main.js boot() runs and DRAWS every card
       t=380ms  the sheet CSV arrives, applyRecords() rewrites
                the tutor objects
       t=380ms  …and nothing on screen changes, because the
                cards were painted 379ms ago from the old
                values and nobody redraws them

     So on a FIRST visit — which is every visit from Google —
     the sheet did nothing at all visually. On the second visit
     the cache applied before paint and it looked like it
     worked. That is the worst kind of bug: it works for the
     person testing it and not for the visitor.

     Two things fix it, and both are needed:

       1. this file announces "ekguru:sheet" with a `changed`
          count (it already did)
       2. js/main.js now LISTENS for it and repaints the cards,
          the profile and the stats (new in v62)

     Alongside that, the cache is now stale-while-revalidate:
     a cached copy paints instantly AND a fresh fetch always
     runs behind it. Before, a cache under an hour old meant no
     fetch at all, so a price changed in the sheet could sit
     invisible for up to sixty minutes on a returning visitor's
     screen even though the network was free.

     Default cache is now 5 minutes for the FIRST paint only —
     the revalidation is unconditional, so in practice a change
     shows on the very next page view. */
  var ALWAYS_REVALIDATE = CFG.alwaysRevalidate !== false;

  /* =========================================================
     GOOGLE DRIVE IMAGE LINKS  (v62)
     ---------------------------------------------------------
     Prakash asked for photos to live in Drive so that adding a
     tutor never means pushing an image file to GitHub.

     A Drive "share" link is NOT an image. Pasting

       https://drive.google.com/file/d/1AbC…/view?usp=sharing

     into an <img src> shows nothing: that URL serves an HTML
     viewer page, and Drive sends X-Frame-Options on it too.
     The old validator rejected it for the right reason (it does
     not end in .jpg) but with a useless outcome — the tutor
     silently kept the placeholder.

     The direct form that DOES hotlink is

       https://lh3.googleusercontent.com/d/<FILEID>

     so every Drive link is rewritten to that. `=w800` asks
     Google for a sensible size instead of the original, which
     on a phone photo can be 6 MB.

     ⚠️ The file must be shared as "Anyone with the link".
     A private file returns 403 and the <img> onerror handler
     in js/main.js falls back to the placeholder, so a wrong
     sharing setting degrades instead of breaking.

     This function is duplicated in tools/sheetsync.js. Any
     change must be made in BOTH — tools/test-livedata.js
     asserts the two agree, because two parsers for one format
     is how they drift apart. */
  /* v98 — display form for timezones. The sheet writes the human
     form "IST (GMT+5:30)"; the site shows "IST (Asia/Kolkata)" as
     the command requires. Same offset, so nothing is mis-parsed;
     the function only rewrites labels it already knows, and passes
     everything else through untouched (never a data change). */
  function normalizeTimezone(v) {
    var s = String(v == null ? "" : v).trim();
    if (/IST\s*\(\s*GMT\s*\+\s*5:30\s*\)/i.test(s)) return "IST (Asia/Kolkata)";
    return s;
  }

  function normalizePhoto(v) {
    v = String(v == null ? "" : v).trim();
    if (!v) return null;

    /* Drive: /file/d/<id>/…  ·  ?id=<id>  ·  /d/<id> */
    var m = /drive\.google\.com\/(?:file\/d\/|open\?id=|uc\?[^#]*id=|d\/)([A-Za-z0-9_-]{10,})/.exec(v);
    if (m) return "https://lh3.googleusercontent.com/d/" + m[1] + "=w800";

    /* already the direct Google form — leave it, but strip any
       existing size suffix so ours is the only one */
    m = /^https:\/\/lh\d\.googleusercontent\.com\/d\/([A-Za-z0-9_-]{10,})/.exec(v);
    if (m) return "https://lh3.googleusercontent.com/d/" + m[1] + "=w800";

    /* any https URL that ends in a real image extension */
    if (/^https:\/\/[^\s]+\.(jpg|jpeg|png|webp|avif)(\?[^\s]*)?$/i.test(v)) return v;

    /* image hosts that serve images from extension-less URLs.
       Kept to a known list on purpose: accepting ANY https URL
       would let a typo put a whole web page in an <img>. */
    if (/^https:\/\/(i\.imgur\.com|i\.ibb\.co|res\.cloudinary\.com|images\.unsplash\.com|lh\d\.googleusercontent\.com|[a-z0-9-]+\.githubusercontent\.com|[a-z0-9-]+\.supabase\.co|[a-z0-9-]+\.r2\.dev|[a-z0-9-]+\.imagekit\.io)\//i.test(v)) return v;

    /* a file inside the repo */
    if (/^images\/[A-Za-z0-9._-]+\.(jpg|jpeg|png|webp|avif)$/i.test(v)) return v;

    return null;
  }

  /* Responsive variants (name-176.webp and friends) only exist for
     files in images/. An external URL has none, so asking for
     "https://lh3…=w800-176.webp" is a guaranteed 404 — see the
     matching guard in js/main.js srcBase(). */
  function isExternalImage(p) { return /^https?:\/\//i.test(String(p || "")); }

  /* =========================================================
     THE API IS PUBLISHED EVEN WHEN THE SHEET IS NOT  (v57)
     ---------------------------------------------------------
     BUG FOUND v57: these two early returns skipped the whole file,
     including the window.EkGuruSheet assignment at the bottom. So
     if no Sheet was configured — or the browser had no fetch —
     EkGuruSheet did not exist at all.

     That was invisible while nothing else used it. Then the admin
     dashboard's "add a tutor" form called
     EkGuruSheet.parseAvailability() to read the hours field, got
     undefined, and silently produced a tutor with an EMPTY
     timetable. No error, and a brand-new tutor with no hours looks
     exactly like a tutor who has not filled them in.

     A module's API should not depend on its configuration. The
     helpers are pure functions of their input and are useful with
     or without a live Sheet, so they are published first and the
     network work is what gets skipped. */
  /* NOTE ON ORDER: publishAPI() is deliberately NOT called here.

     The first attempt at this fix called it on this line, above the
     FIELDS table. `var` is hoisted but its ASSIGNMENT is not, so
     FIELDS was still undefined and parseAvailability() returned
     null for every input — the exact same class of bug as the
     SPACES one in v52.

     Instead the two early returns below now jump to a label at the
     bottom of the file, after FIELDS exists. The function is
     declared, so calling it later is safe; calling it earlier is
     not. */
  var configured = !!url && typeof window.fetch === "function";

  /* ---------------------------------------------------------
     A CSV parser that handles quoted fields, because a bio
     will contain commas and a naive split would corrupt it.
     --------------------------------------------------------- */
  function parseCSV(text) {
    var rows = [], row = [], field = "", inQuotes = false;
    for (var i = 0; i < text.length; i++) {
      var c = text[i], next = text[i + 1];
      if (inQuotes) {
        if (c === '"' && next === '"') { field += '"'; i++; }
        else if (c === '"') inQuotes = false;
        else field += c;
      } else {
        if (c === '"') inQuotes = true;
        else if (c === ",") { row.push(field); field = ""; }
        else if (c === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
        else if (c !== "\r") field += c;
      }
    }
    if (field.length || row.length) { row.push(field); rows.push(row); }
    return rows.filter(function (r) { return r.some(function (c) { return c.trim(); }); });
  }

  function toRecords(rows) {
    if (rows.length < 2) return [];
    var head = rows[0].map(function (h) { return String(h).trim(); });
    return rows.slice(1).map(function (r) {
      var o = {};
      head.forEach(function (h, i) { if (h) o[h] = (r[i] || "").trim(); });
      return o;
    }).filter(function (o) { return o.id; });
  }

  /* Which spreadsheet column maps onto which tutor field, and how
     to convert it. Anything not listed here is ignored, so a stray
     column in the Sheet cannot corrupt a tutor. */
  var FIELDS = {
    name:         function (v) { return v; },
    headline:     function (v) { return v; },
    city:         function (v) { return v; },
    bio:          function (v) { return v; },
    email:        function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? v : null; },
    /* v101 — CANONICAL OPERATIONAL EMAIL (RESET §11). The one
       address booking mail is sent to for this tutor. It is NOT
       rendered on any public page — it exists only for the mailer's
       notification_email() resolution. The legacy `email` column
       stays for migration compatibility. */
    notification_email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? v : null; },
    /* v72 — the safe way for the sheet to route a tutor's booking
       mail. A FormSubmit alias delivers to their inbox without the
       address existing anywhere public. js/mailer.js already
       prefers this over `email`; before v72 the sheet had no way
       to set it, so the only route was publishing the address.
       An @ here means somebody pasted an email into the wrong
       column and recreated the leak — refuse it. */
    formKey:      function (v) { return (v && v.indexOf("@") < 0 && /^[A-Za-z0-9_-]{6,64}$/.test(v)) ? v : null; },

    /* v72 — more of the site under spreadsheet control. Must
       match the FIELDS table in tools/sheetsync.js exactly: the
       build bakes values in and this repaints them live, and the
       two disagreeing is precisely the class of bug that put a
       $3 price on six pages for nine versions. */
    holiday:        function (v) { return /^(yes|true|1|y)$/i.test(v); },
    holidayUntil:   function (v) { return /^\d{4}-\d{2}-\d{2}$/.test(v) ? v : null; },
    holidayNote:    function (v) { return v && v.length <= 160 ? v : null; },
    specialities:   function (v) { return v.split(",").map(function (x) { return x.trim(); }).filter(Boolean).slice(0, 6); },
    badge:          function (v) { return v && v.length <= 24 ? v : null; },
    trialMinutes:   function (v) { var n = Number(v); return isFinite(n) && n >= 0 && n <= 60 ? n : null; },
    packageDiscount:function (v) { var n = Number(v); return isFinite(n) && n >= 0 && n <= 60 ? n : null; },
    responseHours:  function (v) { var n = Number(v); return isFinite(n) && n >= 1 && n <= 168 ? n : null; },
    intro:          function (v) { return v && v.length <= 220 ? v : null; },
    exams:          function (v) { return v.split(",").map(function (x) { return x.trim(); }).filter(Boolean).slice(0, 8); },
    priceUSD:     function (v) {
      var n = Number(v);
      /* BUG FOUND v62 — 999999999999 WAS ACCEPTED.

         The only check was "a positive number". A slipped keypress
         or a pasted phone number became the price on a live card,
         in the Offer schema Google reads, and in the price filter —
         which then has a maximum nobody can reach, so every tutor
         disappears from the search page.

         There is no honest one-to-one language lesson at $2000, and
         a price under a dollar is a typo (someone meaning 5 and
         hitting 0.5). Refuse both, keep the old value, and say so.
         A wrong price is worse than a stale one: it is a public
         quote you would have to honour. */
      if (!isFinite(n) || n <= 0) return null;
      if (n < 1 || n > 2000) return null;
      return n;
    },
    lessonLength: function (v) { return v; },
    video:        function (v) { return v.length === 11 ? v : null; },
    youtubeId:    function (v) { return v.length === 11 ? v : null; },
    experienceYears: function (v) { var n = Number(v); return isFinite(n) ? n : null; },
    tags:         function (v) { return v.split(",").map(function (x) { return x.trim(); }).filter(Boolean); },
    teaches:      function (v) { return v.split(",").map(function (x) { return x.trim(); }).filter(Boolean); },
    trialAvailable: function (v) { return /^(yes|true|1|y)$/i.test(v); },

    /* ---------------------------------------------------------
       AVAILABILITY — the field you will change most often
       ---------------------------------------------------------
       A tutor's hours change constantly: an exam week, a holiday,
       a new job. Until now that meant editing a JavaScript file
       and pushing. This is exactly what a spreadsheet is for.

       Write it in one cell, days separated by semicolons:

         Mon 17:00,18:00; Tue 17:00,18:00; Sat 10:00

       Or use "same" to apply one set to several days:

         Mon-Fri 19:00,20:00,21:00; Sat 10:00,11:00

       An empty cell changes nothing. The word "none" clears the
       schedule entirely, which is how you mark someone away
       without hiding their profile.
       --------------------------------------------------------- */
    availability: function (v) {
      var DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
      if (/^(none|closed|away)$/i.test(v.trim())) return {};

      var out = {};
      v.split(";").forEach(function (part) {
        part = part.trim();
        if (!part) return;

        /* "Mon-Fri 19:00,20:00"  or  "Mon 19:00,20:00" */
        var m = /^([A-Za-z]{3})\s*(?:-\s*([A-Za-z]{3}))?\s+(.+)$/.exec(part);
        if (!m) return;

        var from = m[1].slice(0, 3), to = m[2] ? m[2].slice(0, 3) : null;
        var norm = function (d) {
          return DAYS.filter(function (x) { return x.toLowerCase() === d.toLowerCase(); })[0];
        };
        var a = norm(from), b = to ? norm(to) : null;
        if (!a) return;

        var days = b
          ? DAYS.slice(DAYS.indexOf(a), DAYS.indexOf(b) + 1)
          : [a];

        /* BUG FOUND v61 — "25:99" WAS ACCEPTED HERE.

           v53 fixed exactly this in js/schedule.js and missed this
           copy. The shape check only proves the entry LOOKS like a
           time; 25:99 passes it, and the calendar then rolls it into
           the next day at 02:39 — a slot the tutor never offered, on
           a day they may not teach.

           A typo in a spreadsheet must never invent availability. */
        var times = m[3].split(",").map(function (t) { return t.trim(); })
          .filter(function (t) {
            var hm = /^(\d{1,2}):(\d{2})$/.exec(t);
            if (!hm) return false;
            var h = Number(hm[1]), mi = Number(hm[2]);
            return h >= 0 && h <= 23 && mi >= 0 && mi <= 59;
          })
          .map(function (t) {
            /* normalise 9:00 to 09:00 so the two parsers agree */
            var hm = /^(\d{1,2}):(\d{2})$/.exec(t);
            return (hm[1].length === 1 ? "0" + hm[1] : hm[1]) + ":" + hm[2];
          });
        if (!times.length) return;

        days.forEach(function (d) {
          out[d] = (out[d] || []).concat(times);
        });
      });

      /* Refuse a schedule we could not read at all, rather than
         silently wiping a tutor's real hours. */
      if (!Object.keys(out).length) return null;

      /* Every day gets a key, empty where there are no hours. The
         tutor files are written that way and the booking modal walks
         all seven days, so keeping the same shape avoids a whole
         class of "undefined is not iterable" further down. */
      var full = {};
      DAYS.forEach(function (d) { full[d] = out[d] || []; });
      return full;
    },

    /* Mark a tutor as verified, or a Super Tutor, from the sheet. */
    verified:   function (v) { return /^(yes|true|1|y)$/i.test(v); },
    superTutor: function (v) { return /^(yes|true|1|y)$/i.test(v); },
    rating:     function (v) { var n = Number(v); return isFinite(n) && n >= 0 && n <= 5 ? n : null; },
    reviewsCount:  function (v) { var n = Number(v); return isFinite(n) && n >= 0 ? n : null; },
    lessonsCount:  function (v) { var n = Number(v); return isFinite(n) && n >= 0 ? n : null; },
    preplyUrl:  function (v) { return /^https?:\/\//.test(v) ? v : null; },
    calLink:    function (v) { return /^[a-z0-9-]+\/[a-z0-9-]+$/i.test(v) ? v : null; },
    /* v98 — the sheet stores "IST (GMT+5:30)"; the site displays the
       command's required form "IST (Asia/Kolkata)". Both parse to the
       same +330 minutes, so this is a display normalization, not a
       data change — the sheet is never rewritten. */
    timezone:   function (v) { return normalizeTimezone(v); },
    country:    function (v) { return v; },

    /* =========================================================
       ADDED v56 — the last eight fields
       ---------------------------------------------------------
       Every column was audited one at a time (tools/test-columns.js).
       Twenty-three worked. These eight silently did nothing, which
       is worse than not offering them: you edit the Sheet, nothing
       happens, and there is no error to tell you why.

       The reason they were left out is that they are not plain
       strings — they are lists and objects. Each needs a parser,
       and each needs to REFUSE bad input rather than write
       nonsense onto a live profile.
       ========================================================= */

    /* nickname — what the booking form calls them. */
    nickname: function (v) { return v; },

    /* subject — almost always "Hindi", but the site is built to
       take another language later without a rewrite. */
    subject: function (v) { return v; },

    /* photo — a path inside the repo, a full https URL, or a
       Google Drive share link (v62). Anything else is refused: a
       broken image on a tutor page looks worse than the
       placeholder it replaced. */
    photo: normalizePhoto,

    /* thumb — the small square used on cards and in search.
       OPTIONAL, exactly as asked: leave the cell blank and
       js/tutors-data.js copies the main photo into it. */
    thumb: normalizePhoto,

    /* banner — the wide 16:9 cover at the top of a profile.
       Also optional. The word "none" clears an existing banner,
       because a blank cell means "keep what you have" and there
       had to be some way to remove one from the spreadsheet. */
    banner: function (v) {
      if (/^(none|no|remove|clear)$/i.test(String(v).trim())) return "";
      return normalizePhoto(v);
    },

    /* videoTitle — the caption printed over the intro video.
       v97: refuse values shaped like the methodology cell — a
       newline or a " | " separator is the tell that methodology
       text was pasted into the wrong column (found live on tara's
       row, 11 Sep 2026). A garbled multi-line caption is worse
       than none. */
    videoTitle: function (v) {
      v = String(v == null ? "" : v).trim();
      if (!v) return null;
      if (v.length > 90 || v.indexOf("|") > -1 || /[\r\n]/.test(v)) return null;
      return v;
    },

    /* countryFlag — one emoji. Restricted to the regional
       indicator range so a stray letter cannot end up rendered as
       a flag. */
    countryFlag: function (v) {
      v = String(v).trim();
      return /^[\uD83C][\uDDE6-\uDDFF][\uD83C][\uDDE6-\uDDFF]$/.test(v) ? v : null;
    },

    /* levels — a comma list, matched against what the filters
       actually offer. An unrecognised level would create a filter
       option no tutor can be found under. */
    levels: function (v) {
      var ALLOWED = ["Beginner", "Intermediate", "Advanced"];
      var out = v.split(",").map(function (x) { return x.trim(); })
        .filter(Boolean)
        .map(function (x) {
          for (var i = 0; i < ALLOWED.length; i++) {
            if (ALLOWED[i].toLowerCase() === x.toLowerCase()) return ALLOWED[i];
          }
          return null;
        });
      return out.indexOf(null) > -1 ? null : (out.length ? out : null);
    },

    /* speaks — "Hindi: Native, English: C1, Bengali: Fluent".
       Stored as objects because the profile prints the level as a
       badge beside each language. A missing level defaults to
       Fluent rather than rejecting the whole cell — a language
       with no level is still useful information. */
    speaks: function (v) {
      var out = v.split(",").map(function (part) {
        var bits = part.split(":");
        var lang = (bits[0] || "").trim();
        if (!lang) return null;
        return { lang: lang, level: (bits[1] || "Fluent").trim() };
      }).filter(Boolean);
      return out.length ? out : null;
    },

    /* about / experience — one paragraph per line.
       A Sheet cell holds newlines (alt+enter), and Google's CSV
       export quotes them properly, so this works exactly as typed.
       Splitting on newline rather than a separator character means
       nothing in the text is off-limits. */
    about: function (v) {
      var out = v.split(/\r?\n/).map(function (x) { return x.trim(); }).filter(Boolean);
      return out.length ? out : null;
    },
    experience: function (v) {
      var out = v.split(/\r?\n/).map(function (x) { return x.trim(); }).filter(Boolean);
      return out.length ? out : null;
    },

    /* methodology — "Title | description" per line, because each
       point renders as a heading plus a sentence. A line with no
       pipe becomes a title with no description, which still looks
       right rather than breaking the layout. */
    methodology: function (v) {
      /* BUG FOUND v56 — THE WRONG PROPERTY NAME.

         This originally produced { title, text }. Every renderer on
         the site reads { title, desc }:

           tools/prerender.js   <dd>${esc(m.desc)}</dd>
           js/features.js       m.title + " " + m.desc

         So editing methodology in the Sheet would have printed
         "undefined" under every heading on that tutor's page, and
         the page would still have looked structurally fine — which
         is how it would have survived unnoticed.

         Caught only by the round-trip test: makesheet.js writes
         m.desc out, this read it back as m.text, and the two no
         longer matched. That is precisely what a round trip is for. */
      var out = v.split(/\r?\n/).map(function (line) {
        line = line.trim();
        if (!line) return null;
        var i = line.indexOf("|");
        if (i === -1) return { title: line, desc: "" };
        return { title: line.slice(0, i).trim(), desc: line.slice(i + 1).trim() };
      }).filter(Boolean);
      return out.length ? out : null;
    }
  };

  /* =========================================================
     THE MASTER LIST  (v62)
     ---------------------------------------------------------
     BUG FOUND v62 — HIDING A TUTOR WAS ONE-WAY, AND HID THEM
     FROM ONLY HALF THE SITE.

     The old code did this:

         window.EKGURU_TUTORS = T.filter(not hidden)

     That assigns a BRAND NEW ARRAY to the global. But js/main.js
     and js/features.js both captured the old array on line 31 and
     line 15 respectively:

         var TUTORS = window.EKGURU_TUTORS;

     A reassignment does not reach a variable that already holds
     the previous array. So after "active: no" arrived from the
     sheet: the global was correct, and every renderer kept using
     the full list. The tutor stayed on the cards, in the search
     dropdown and in the booking modal.

     Worse, the hidden tutor was now GONE from the global, so when
     the row was flipped back to "yes" there was no object left to
     unhide. Hiding was permanent until a page reload.

     Both are fixed by keeping a private master list and MUTATING
     the published array in place with splice(), which every holder
     of the reference sees.
     ========================================================= */
  var MASTER = null;

  function master() {
    if (!MASTER) MASTER = (window.EKGURU_TUTORS || []).slice();
    return MASTER;
  }

  /* Replace the CONTENTS of the live array, never the array. */
  function publish(list) {
    var T = window.EKGURU_TUTORS;
    if (!Array.isArray(T)) { window.EKGURU_TUTORS = list.slice(); return; }
    T.length = 0;
    for (var i = 0; i < list.length; i++) T.push(list[i]);
  }

  /* =========================================================
     A WHOLE TUTOR FROM A SPREADSHEET ROW  (v62)
     ---------------------------------------------------------
     Prakash: "agar mai sheet mai … new tutor add kar saku, or
     vahi se add or remove bhi ho jaye … muje kuch file na likhni
     pade kisi ko add karne ke liye".

     Before this, a row whose id had no js/tutors/<id>.js was
     logged as an "unknown id" and thrown away. Adding a tutor
     still meant creating a JavaScript file.

     Now the row itself becomes the tutor. Every field runs
     through the same validators as an override, and
     js/tutors-data.js fills in defaults for anything blank, so a
     sheet-born tutor is indistinguishable from a file-born one.

     Two halves, and both are needed:

       here          they appear for the VISITOR immediately,
                     with no rebuild and no push
       sheetsync.js  the BUILD writes js/tutors/<id>.js so they
                     also get a pre-rendered page, a sitemap
                     entry and schema — the things a crawler
                     needs and JavaScript cannot provide

     The one hard requirement is a name. A tutor card with no
     name is not a tutor, it is a bug with a photo. */
  function buildFromRow(r, lower) {
    var name = String(pick(r, lower, "name") || "").trim();
    if (!name) return null;

    var t = { id: r.id, _fromSheet: true };
    Object.keys(FIELDS).forEach(function (col) {
      var raw = pick(r, lower, col);
      if (raw === undefined || raw === "") return;
      var val = FIELDS[col](raw);
      if (val === null) return;
      t[col === "video" ? "youtubeId" : col] = val;
    });
    t.name = name;

    /* Defaults are applied by js/tutors-data.js at load time, which
       has already run by the time the sheet arrives. Apply the same
       table here so a sheet-born tutor never renders "undefined". */
    var D = window.EKGURU_TUTOR_DEFAULTS || {};
    Object.keys(D).forEach(function (k) {
      if (t[k] === undefined || t[k] === null) {
        var d = D[k];
        t[k] = Array.isArray(d) ? d.slice() : (d && typeof d === "object" ? {} : d);
      }
    });
    if (!t.thumb || t.thumb === D.thumb) t.thumb = t.photo || D.thumb;
    if (!t.email) t.email = (window.EKGURU_SITE && window.EKGURU_SITE.email) || "";
    if (!t.headline) t.headline = (t.subject || "Hindi") + " tutor" + (t.city ? " from " + t.city : "");

    /* Never publish a phone number, whatever the spreadsheet says.
       Same rule as js/tutors-data.js, enforced again here because
       this object never passes through that file. */
    t.whatsapp = "";
    return t;
  }

  /* Column lookup that does not care about capitalisation.
     A header typed "priceusd" or "PriceUSD" must work — the person
     filling the sheet in on a phone should not have to match the
     camelCase exactly. (The build side had this fixed in v61; the
     browser side did not, so the two disagreed.) */
  function pick(r, lower, col) {
    if (r[col] !== undefined) return r[col];
    return lower[col.toLowerCase()];
  }

  function applyRecords(recs) {
    var list = master().slice();
    var byId = {};
    list.forEach(function (t) { byId[t.id] = t; });

    var changed = 0, hidden = 0, added = 0, skipped = [];
    var order = [], seen = {};
    var dupes = [], rowSeen = {};   /* every row, including hidden ones */

    recs.forEach(function (r) {
      /* =========================================================
         BUG FOUND v62 — "Sushila-G" DID NOT MATCH "sushila-g".

         The id was trimmed but not lowercased. Typing the id with a
         capital letter — which anyone would, it is a name — meant
         the row did not match the existing tutor, so it fell
         through to "create a new tutor" and was then refused for
         having no name (the name cell was blank because the row was
         meant to be an edit).

         The message read "Sushila-G (no name)", which is true and
         completely unhelpful: the actual problem is the capital S,
         and the visible symptom is that an edit silently did
         nothing.

         Worse, WITH a name filled in it would have created a
         second Sushila alongside the first. Two cards, two profile
         pages, both real.

         An id is a filename and a URL. Both are lowercase here, so
         the id is lowercased on the way in and the sheet stops
         being case-sensitive about it. The same normalisation is in
         tools/sheetsync.js.
         ========================================================= */
      r.id = String(r.id || "").trim().toLowerCase();
      if (!r.id || r.id.charAt(0) === "#") return;   /* the #help row */

      /* BUG FOUND v62 — a duplicate id was silently last-wins.

         Two rows for the same tutor is a mistake every time — a
         copy-paste, or a row added when one already existed further
         up. Applying both means the second quietly overwrites the
         first and the person editing sees their change "not work"
         because they edited the wrong row.

         Still last-wins (refusing the row would be worse: the sheet
         would appear frozen), but it now says so. */
      if (rowSeen[r.id]) { if (dupes.indexOf(r.id) === -1) dupes.push(r.id); }
      rowSeen[r.id] = 1;

      var lower = {};
      Object.keys(r).forEach(function (k) { lower[String(k).toLowerCase()] = r[k]; });

      var activeCell = String(pick(r, lower, "active") || "yes").trim();
      var isHidden = /^(no|false|0|n|hidden)$/i.test(activeCell);

      var t = byId[r.id];

      if (!t) {
        if (isHidden) return;                        /* hidden and new: nothing to do */

        /* =========================================================
           BUG FOUND v65 — A PAGE WITH NO TUTOR LIST AT ALL.

           The pre-rendered profiles now load this file (see
           js/livepatch.js) but deliberately NOT tutors-data.js —
           they are the cheap, crawlable version and do not need
           90 KB of renderer to patch four numbers.

           So window.EKGURU_TUTORS does not exist there. Every row
           looked new, "sushila-g" was treated as a tutor to CREATE,
           and because an edit row has no name cell it was thrown
           out as "sushila-g (no name)". The sheet reported zero
           changes on the very page it was supposed to be fixing.

           If there is no tutor list, this is not a page that lists
           tutors — it is a page that DISPLAYS one, and livepatch.js
           reads the values straight off the record. Keep the row so
           it can, and create nothing.
           ========================================================= */
        if (!MASTER || !MASTER.length) {
          byId[r.id] = { id: r.id, _recordOnly: true };
          Object.keys(FIELDS).forEach(function (col) {
            var raw = pick(r, lower, col);
            if (raw === undefined || raw === "") return;
            var v = FIELDS[col](raw);
            if (v === null) return;
            byId[r.id][col === "video" ? "youtubeId" : col] = v;
          });
          if (!seen[r.id]) { order.push(r.id); seen[r.id] = 1; }
          changed++;
          return;
        }

        t = buildFromRow(r, lower);
        if (!t) { skipped.push(r.id + " (no name)"); return; }
        byId[r.id] = t;
        list.push(t);
        MASTER.push(t);
        added++;
        changed++;
        if (!seen[r.id]) { order.push(r.id); seen[r.id] = 1; }
        return;
      }

      if (isHidden) { t._hiddenBySheet = true; hidden++; return; }
      t._hiddenBySheet = false;
      if (!seen[r.id]) { order.push(r.id); seen[r.id] = 1; }

      Object.keys(FIELDS).forEach(function (col) {
        var raw = pick(r, lower, col);
        if (raw === undefined || raw === "") return;   /* blank changes nothing */
        var val = FIELDS[col](raw);
        if (val === null) return;                      /* failed validation */
        var target = col === "video" ? "youtubeId" : col;
        /* Compare properly. String() turns every object into
           "[object Object]", so availability, teaches and tags all
           looked unchanged and were silently never applied — the
           availability column did nothing at all until this was
           fixed. JSON comparison handles objects and arrays, and
           still works for plain strings and numbers. */
        var same;
        try { same = JSON.stringify(t[target]) === JSON.stringify(val); }
        catch (e) { same = String(t[target]) === String(val); }
        if (!same) { t[target] = val; changed++; }
      });

      /* thumb follows the photo unless the sheet set one of its own,
         so changing a photo in the sheet also changes the small
         square on the cards. Without this, a new photo appeared on
         the profile and the old one stayed on every card. */
      var thumbCell = pick(r, lower, "thumb");
      if ((thumbCell === undefined || thumbCell === "") && t.photo) t.thumb = t.photo;

      /* A phone number in the Sheet is ignored on purpose. Personal
         numbers are not published — see js/tutors-data.js. */
      if (pick(r, lower, "whatsapp")) {
        console.warn('[EkGuru] Sheet column "whatsapp" ignored for "' + r.id +
          '". Personal numbers are never published.');
      }
    });

    /* ---------------------------------------------------------
       Order. The spreadsheet's row order is the order tutors
       appear, matching what tools/sheetsync.js does to the
       registry at build time. A tutor who is in a file but not in
       the sheet keeps their place at the end rather than
       vanishing — the sheet adds and reorders, it does not
       silently delete someone whose row was never written.
       --------------------------------------------------------- */
    /* Record-only rows (see the note above) never join the rendered
       list — nothing on those pages iterates tutors. They are
       published separately for js/livepatch.js to read. */
    var records = {};
    Object.keys(byId).forEach(function (k) {
      if (byId[k] && byId[k]._recordOnly) records[k] = byId[k];
    });
    window.EKGURU_SHEET_RECORDS = records;

    var visible = list.filter(function (t) { return !t._hiddenBySheet; });
    visible.sort(function (a, b) {
      var ia = order.indexOf(a.id), ib = order.indexOf(b.id);
      if (ia === -1 && ib === -1) return 0;
      if (ia === -1) return 1;
      if (ib === -1) return -1;
      return ia - ib;
    });
    publish(visible);

    if (skipped.length) {
      console.warn("[EkGuru] Sheet rows skipped: " + skipped.join(", "));
    }
    if (dupes.length) {
      console.warn('[EkGuru] The sheet has more than one row for: ' + dupes.join(", ") +
        ". The LAST row wins. Delete the duplicate, or an edit to the first " +
        "one will look like it did nothing.");
    }

    window.EKGURU_SHEET_INFO = {
      loaded: true, rows: recs.length, changed: changed, hidden: hidden,
      added: added, unknown: skipped, at: new Date().toISOString()
    };
    return changed + hidden;
  }

  function announce() {
    try {
      window.dispatchEvent(new CustomEvent("ekguru:sheet", {
        detail: window.EKGURU_SHEET_INFO
      }));
    } catch (e) {}
  }

  function readCache() {
    try {
      var raw = localStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      var c = JSON.parse(raw);
      if (!c || !c.t || !Array.isArray(c.recs)) return null;
      return { stale: Date.now() - c.t > MAX_AGE, recs: c.recs, t: c.t };
    } catch (e) { return null; }
  }
  function writeCache(recs) {
    try { localStorage.setItem(CACHE_KEY, JSON.stringify({ t: Date.now(), recs: recs })); }
    catch (e) {}
  }

  function fetchSheet() {
    /* v97 — one silent retry after a failed fetch (a cold Google CDN
       edge on the first hit of the day is common), then the existing
       error path. The 8-second abort timeout applies per attempt. */
    function once(attempt) {
      var ctrl = null, timer = null;
      try { ctrl = new AbortController(); } catch (e) {}
      if (ctrl) timer = setTimeout(function () { try { ctrl.abort(); } catch (e) {} }, 8000);

      return fetch(url, { signal: ctrl ? ctrl.signal : undefined, cache: "default" })
        .then(function (r) { return r.ok ? r.text() : Promise.reject(new Error("HTTP " + r.status)); })
        .then(function (text) {
          if (timer) clearTimeout(timer);
          /* A Sheet that is not actually published returns an HTML
             login page, not CSV. Refuse it rather than parsing junk. */
          if (/^\s*</.test(text)) {
            throw new Error("That URL returned a web page, not CSV. " +
              "Use File → Share → Publish to web → CSV.");
          }
          var rows = parseCSV(text);
          var head = (rows[0] || []).map(function (h) { return String(h).trim().toLowerCase(); });
          /* Schema check: without an id column nothing can map, and a
             wrong tab (or an empty sheet) must be loud, not silent. */
          if (head.indexOf("id") === -1) {
            throw new Error("header row has no 'id' column (got: " +
              head.slice(0, 8).join(",") + ") — is the right tab published?");
          }
          /* Report columns the code expects but the sheet lacks, so a
             silently-dead column is visible instead of mysterious.
             'youtubeId' is the internal name of the 'video' column. */
          var missing = Object.keys(FIELDS).filter(function (f) {
            return f !== "youtubeId" && head.indexOf(f.toLowerCase()) === -1;
          });
          if (missing.length) {
            console.warn("[EkGuru] Sheet is missing columns: " + missing.join(", ") +
              " — those fields keep their file values.");
          }
          var recs = toRecords(rows);
          if (!recs.length) throw new Error("no rows with an id column");
          writeCache(recs);
          var n = applyRecords(recs);
          announce();
          if (n) console.info("[EkGuru] Sheet applied: " + n + " change(s).");
        })
        .catch(function (e) {
          if (timer) clearTimeout(timer);
          if (attempt < 2) {
            /* One quiet retry; only the final failure reports. */
            return new Promise(function (res) {
              setTimeout(function () { once(attempt + 1).catch(function () {}); res(); }, 1200);
            });
          }
          window.EKGURU_SHEET_INFO = { loaded: false, error: e.message };
          announce();
          console.warn("[EkGuru] Sheet not loaded: " + e.message +
            " — the tutor files are being used instead.");
        });
    }
    return once(1);
  }

  /* A fresh cache applies before anything renders, so the first
     paint already shows the Sheet's values. A stale one is used
     immediately and refreshed behind.

     Skipped entirely when no Sheet is configured — but the API
     below is published either way, because its helpers are pure
     functions and the admin dashboard needs them regardless. */
  /* =========================================================
     v62 — STALE-WHILE-REVALIDATE, ALWAYS
     ---------------------------------------------------------
     BUG FOUND v62: `if (cached.stale) fetchSheet()` meant a cache
     under an hour old blocked the network call entirely. Change a
     price in the sheet, reload the page, and you saw the OLD price
     for up to sixty minutes — with a perfectly good connection and
     the correct value sitting one HTTP request away.

     That is the exact complaint: "change karte hi changes dikhne
     chahiye". Now the cached copy paints instantly (so there is no
     flash of stale-then-correct on a slow line) AND a fresh fetch
     always runs behind it. The cost is one 4 KB request per page
     view; the benefit is that an edit is live on the next view.

     Google's CDN caches a published sheet for about five minutes
     of its own accord, so five minutes is the true floor here and
     no amount of client-side eagerness beats it. That number is
     printed in the admin dashboard so nobody expects zero. */
  if (configured) {
    var cached = readCache();
    if (cached) {
      applyRecords(cached.recs);
      announce();
      if (cached.stale || ALWAYS_REVALIDATE) fetchSheet();
    } else {
      fetchSheet();
    }

    /* Coming back to a tab that has been open for a while must not
       show yesterday's prices. Refetch when the tab is revealed,
       throttled so tabbing back and forth is not a request storm. */
    var lastFetch = Date.now();
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState !== "visible") return;
      if (Date.now() - lastFetch < 60000) return;
      lastFetch = Date.now();
      fetchSheet();
    });
  }

  publishAPI();

  function publishAPI() {
  window.EkGuruSheet = {
    info: function () { return window.EKGURU_SHEET_INFO || { loaded: false }; },
    refresh: function () {
      try { localStorage.removeItem(CACHE_KEY); } catch (e) {}
      return fetchSheet();
    },

    /* v57: exposed so the admin dashboard's "add a tutor" form can
       parse hours with THIS parser rather than a second copy of the
       same logic. Two parsers for one format is how they drift apart
       — the Sheet would accept a string the form rejected, or worse,
       parse it differently. One implementation, two callers. */
    parseAvailability: function (text) {
      try { return FIELDS.availability(String(text || "")); }
      catch (e) { return null; }
    },

    /* Which fields the Sheet can apply, so the dashboard's column
       reference is generated from the code instead of a hand-written
       list that can silently fall out of date. */
    fields: function () { return Object.keys(FIELDS); },

    /* v62: exposed so the admin dashboard and the tests can check a
       Drive link without a second copy of the rewriting rules. */
    photoUrl: normalizePhoto,
    isExternalImage: isExternalImage
  };
  }
})();

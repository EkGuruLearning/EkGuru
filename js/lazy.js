/* =========================================================
   EkGuru — LOAD THE BOOKING STACK WHEN IT IS NEEDED
   ---------------------------------------------------------
   Prakash: "tumne saari cheezein HTML mein kar di, JS use karte,
   advance modern use karte."

   Two separate points hiding in one sentence, and they deserve
   separate answers.

   ═══════════════════════════════════════════════════════
   1. THE HTML IS NOT THE OLD-FASHIONED PART
   ═══════════════════════════════════════════════════════

   Shipping finished HTML is not a 2010 technique that React
   replaced. It is what React ended up rediscovering and calling
   SSG/SSR, and it is what Google, Vercel and Netlify all
   recommend in 2026.

   Measured on this site, with every <script> removed — which is
   what a crawler with no JavaScript receives:

       index.html                    693 words
       learn/index.html            1,159 words
       hindi/alphabet/index.html     438 words
       answers/hindi-numbers…/       479 words

   Two things this bought, both real:

     · v84 shipped a JS SyntaxError to 318 pages. Every inline
       script on them died. The pages kept working and kept
       ranking, because the words were in the HTML. Had they been
       JS-rendered, 318 pages would have been blank.

     · The 0.159 CLS fixed in v91 was caused by the ONE div that
       waited for JavaScript. Every other section, being in the
       HTML, contributed nothing to the score.

   So the HTML stays. That is not conservatism, it is the
   measurement.

   ═══════════════════════════════════════════════════════
   2. THE ACTUAL OLD-FASHIONED PART — AND HE IS RIGHT
   ═══════════════════════════════════════════════════════

   The home page loaded TWENTY-SIX scripts, 607 KB uncompressed,
   before a visitor had done anything:

       js/mailer.js       98 KB
       js/features.js     74 KB
       js/schedule.js     15 KB
       js/calendar.js      6 KB
                        ────────
                         193 KB

   None of those four does anything until someone presses a
   booking button. They are the modal, the tutor calendar, the
   timezone picker and the mail relay. On a page where most
   visitors read and leave, that is 193 KB and a chunk of
   main-thread parse time spent on a feature they never touch.

   PageSpeed Insights, 11 Sep 2026: element render delay 2,470 ms
   with a Time to First Byte of 0 ms. Nothing was slow to arrive.
   The main thread was busy.

   ═══════════════════════════════════════════════════════
   WHAT THIS FILE DOES
   ═══════════════════════════════════════════════════════

   Loads those four on demand, and defines the trigger BEFORE
   they exist so a click during the gap still works.

     · a real <button data-book> click, OR
     · the pointer coming within 200px of one (loads early, so
       by the time the finger lands the modal is usually ready),
       OR
     · the browser going idle after everything important is done

   Whichever happens first. Each file is fetched once.

   ⚠️ WHY NOT ES MODULES AND import()
   These four files assign to window (window.EkGuruMail and so
   on) and are also loaded directly by other pages that are not
   module-aware. Converting them means touching every call site
   in 26 files, and a dynamic import() gives no benefit over a
   <script> tag we already control the timing of. The gain here
   is WHEN they load, not HOW. Rewriting the syntax would add
   risk and change nothing a visitor can feel.

   ⚠️ NOTHING HERE MAY BREAK BOOKING. Booking is the only thing
   on this site that earns money. If any part of the chain
   fails, bookOrLoad() falls back to a full page load of the
   tutor's own profile, which has the booking form server-side.
   Degraded, never lost — the same rule as the mail relay chain.
   ========================================================= */

(function () {
  "use strict";

  /* The deferred set, in dependency order. schedule and calendar
     are read by features.js, and mailer is called by it, so
     features must be last. */
  /* ═══════════════════════════════════════════════════════
     features.js IS NOT IN THIS LIST, AND THAT WAS A REAL BUG
     ───────────────────────────────────────────────────────
     The first version of v92 deferred it. tools/test-nav.js
     caught the consequence within minutes:

         FAIL  opens on click
         FAIL  aria-expanded true when open

     features.js is not "the booking modal". It is also:

         initNavMenu        the header Learn dropdown
         initLiveSearch     the search box
         initChips          topic filters
         initShare          share buttons
         initTop            scroll-to-top
         initCurrencySwitch the footer currency picker
         initReviewSlider   the reviews carousel
         initCollapsePanels
         initTimezoneToggle

     Deferring it meant the header menu did nothing until
     someone hovered near a booking button. A visitor who came
     to read would find the navigation broken. That is a far
     worse trade than 74 KB.

     So the deferred set is only what is GENUINELY booking-only:

         mailer.js    98 KB  the relay chain — used by the modal
                             and by contact.js, which loads it
                             itself on the contact page
         schedule.js  15 KB  the slot picker inside the modal
         calendar.js   6 KB  the Cal.com embed inside the modal
                     ───────
                     119 KB

     features.js stays a normal script. It is 74 KB and it runs
     the page.

     ⚠️ Read this before adding anything here: a file belongs in
     this list only if NOTHING on the page needs it until a
     booking button is pressed. Check what else is inside it
     first — features.js looked booking-shaped and was not.
     ═══════════════════════════════════════════════════════ */
  var DEFERRED = [
    /* email-templates.js must load BEFORE mailer.js — the mailer
       renders role templates at send time and reads this at call
       time, but loading it first keeps the dependency obvious. */
    "js/email-templates.js",
    "js/mailer.js",
    "js/schedule.js",
    "js/calendar.js"
  ];

  /* ═══════════════════════════════════════════════════════
     v93 — I TRIED TO DEFER seo.js AND WAS WRONG
     ───────────────────────────────────────────────────────
     js/seo.js (52 KB) and js/seo-engine.js (36 KB) looked like
     free wins. The reasoning seemed solid: all 540 GENERATED
     pages ship without them and PageSpeed scores those 100/100
     for SEO, and the four hand-written pages already carry a
     canonical, Open Graph, hreflang and JSON-LD in their HTML.
     So what were 88 KB of JavaScript adding?

     Five tests answered that within minutes:

         FAIL  the meta description follows the sheet
         FAIL  …and so does the social card description
         FAIL  the FAQ answer Google may quote follows the sheet
         FAIL  the JSON-LD is still valid after the rewrite
         FAIL  an alternate link points at the static twin

     seo.js is not a meta-tag duplicator. It is the LIVE SHEET
     applied to the head: edit the description in the settings
     spreadsheet and it changes on the site within the hour,
     without a deploy. That is a feature this project built
     deliberately in v61 and it is worth far more than 88 KB.

     The tags in the HTML are the build-time values. seo.js
     overwrites them with whatever the sheet says now. Defer it
     and the sheet silently stops working — the pages would look
     fine and be a version behind, which is the worst kind of
     broken.

     ⚠️ DO NOT defer these. The saving is real and the cost is a
     feature nobody would notice losing until the sheet was
     edited and nothing happened.

     WHAT REPLACED THE IDEA: nothing. 479 KB was the wrong
     number; 567 KB with a working live sheet is the right one.
     The genuine saving was the booking stack, which is deferred
     and proven by tools/test-lazy.js.
     ═══════════════════════════════════════════════════════ */
  var IDLE_ONLY = [];

  /* Where are we relative to the site root? The pages that carry
     this file sit at depth 0 or 1, and each already knows its own
     prefix through the same mechanism every other script uses. */
  function prefix() {
    var m = document.querySelector('script[src*="js/lazy.js"]');
    if (!m) return "";
    return (m.getAttribute("src") || "").replace(/js\/lazy\.js.*$/, "");
  }
  var P = prefix();

  /* ⚠️ TWO ATTRIBUTES, NOT ONE.
     js/main.js bookBtn() emits data-cal for a tutor who has a
     Cal.com link and data-book for everyone else. Right now no
     tutor has a calLink, so every button is data-book — but the
     day somebody adds one in the sheet, a loader that only knew
     about data-book would silently stop opening that tutor's
     booking. Found by tools/test-lazy.js on its first run.

     data-cal is handled by js/calendar.js, which is in the same
     deferred set, so the fix is the same: load, then hand over.

     Declared HERE, above every use. It was originally written
     next to the click listener, which is 50 lines below
     bookOrLoad() — `var` hoists, so nothing would have crashed;
     the value would simply have been undefined inside
     bookOrLoad and the button feedback would never appear. A
     silent half-failure is worse than a crash. */
  var TRIGGER = "[data-book],[data-cal]";

  var state = "idle";          /* idle | loading | ready | failed */
  var waiting = [];            /* callbacks queued during loading */

  function loadOne(src) {
    return new Promise(function (resolve, reject) {
      /* Already on the page — some pages include these directly
         and must not get a second copy. A double-loaded mailer
         would register its listeners twice and send every email
         twice, which is the kind of bug you find from a customer. */
      if (document.querySelector('script[src$="' + src + '"]')) return resolve();
      var s = document.createElement("script");
      s.src = P + src;
      s.async = false;         /* preserve order — features.js is last */
      s.onload = resolve;
      s.onerror = function () { reject(new Error("could not load " + src)); };
      document.head.appendChild(s);
    });
  }

  function loadAll() {
    if (state === "ready") return Promise.resolve();
    if (state === "loading") {
      return new Promise(function (res) { waiting.push(res); });
    }
    state = "loading";

    /* Sequential, because features.js reads what the others
       define at parse time. Promise.all would race. */
    var chain = Promise.resolve();
    DEFERRED.forEach(function (src) {
      chain = chain.then(function () { return loadOne(src); });
    });

    return chain.then(function () {
      state = "ready";
      waiting.forEach(function (f) { f(); });
      waiting = [];
      /* features.js wires [data-book] on its own DOMContentLoaded
         listener, which has already fired by now. Tell it to wire
         itself, if it exposes a way; otherwise the direct call in
         bookOrLoad() covers it. */
      try {
        if (window.EkGuruFeatures && window.EkGuruFeatures.rewire) {
          window.EkGuruFeatures.rewire();
        }
      } catch (e) {}
    }, function (err) {
      state = "failed";
      if (window.console && console.warn) {
        console.warn("[EkGuru] booking stack did not load:", err.message);
      }
      throw err;
    });
  }

  /* =========================================================
     THE TRIGGER, DEFINED BEFORE THE CODE EXISTS
     ---------------------------------------------------------
     features.js normally binds a delegated click on
     [data-book]. Until it loads, nothing is listening — so this
     listens instead, in the capture phase so it runs first, and
     hands over once the real handler exists.
     ========================================================= */
  function bookOrLoad(id, ev) {
    if (window.EkGuruBook && state === "ready") {
      return window.EkGuruBook(id);
    }
    if (ev) { ev.preventDefault(); ev.stopPropagation(); }

    /* Visible feedback. Loading 193 KB on a slow connection can
       take a second or two, and a button that does nothing feels
       broken — people press it again, which is how you get two
       booking requests. */
    var btn = ev && ev.target && ev.target.closest &&
              ev.target.closest(TRIGGER);
    var restore = null;
    if (btn && !btn.disabled) {
      restore = btn.innerHTML;
      btn.disabled = true;
      btn.setAttribute("aria-busy", "true");
      btn.innerHTML = "Opening…";
    }

    return loadAll().then(function () {
      if (btn) {
        btn.disabled = false;
        btn.removeAttribute("aria-busy");
        if (restore !== null) btn.innerHTML = restore;
      }
      /* Re-dispatch the original click now that the real
         handlers exist. That routes data-cal to calendar.js and
         data-book to features.js without this file having to
         know which is which — the capture listener above bails
         out once state is "ready", so it will not loop. */
      if (btn) {
        btn.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true }));
        return;
      }
      if (window.EkGuruBook) return window.EkGuruBook(id);
      /* The stack loaded but did not define the entry point.
         Should not happen; go to the profile rather than sit
         there doing nothing. */
      location.href = P + "tutor/" + encodeURIComponent(id) + "/";
    }, function () {
      if (btn) {
        btn.disabled = false;
        btn.removeAttribute("aria-busy");
        if (restore !== null) btn.innerHTML = restore;
      }
      /* ⚠️ THE FALLBACK THAT MATTERS. If the scripts cannot be
         fetched at all — offline, blocked, a bad deploy — send
         the visitor to the tutor's own page, which carries a
         booking form that works without any of this. A booking
         must never be lost to a loading failure. */
      location.href = P + "tutor/" + encodeURIComponent(id) + "/";
    });
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(TRIGGER);
    if (!b) return;
    if (state === "ready") return;        /* real handler owns it now */
    var id = b.getAttribute("data-book") || b.getAttribute("data-cal");
    bookOrLoad(id, e);
  }, true);                                /* capture: run before others */

  /* Warm it up when a pointer approaches a booking button. By the
     time a finger or cursor actually lands, the modal is usually
     already there and the click feels instant. */
  function warmNear(e) {
    if (state !== "idle") return;
    var els = document.querySelectorAll(TRIGGER);
    for (var i = 0; i < els.length; i++) {
      var r = els[i].getBoundingClientRect();
      if (e.clientX > r.left - 200 && e.clientX < r.right + 200 &&
          e.clientY > r.top - 200 && e.clientY < r.bottom + 200) {
        loadAll().catch(function () {});
        document.removeEventListener("mousemove", warmNear);
        document.removeEventListener("touchstart", warmTouch, { passive: true });
        return;
      }
    }
  }
  function warmTouch() {
    if (state !== "idle") return;
    loadAll().catch(function () {});
  }
  document.addEventListener("mousemove", warmNear);
  document.addEventListener("touchstart", warmTouch, { passive: true });

  /* And load anyway once the browser is genuinely idle, so a
     visitor who scrolls straight to a button after reading for a
     minute never waits. requestIdleCallback where available;
     a generous timeout otherwise, because the point is to be
     AFTER everything that matters, not merely late. */
  /* The idle-only set. Fetched once, whether or not anybody ever
     touches a booking button, but only after the browser says it
     has nothing better to do. */
  var idleDone = false;
  function loadIdleOnly() {
    if (idleDone) return Promise.resolve();
    idleDone = true;
    /* seo-engine.js defines what seo.js reads, so it goes first.
       async=false in loadOne() preserves that. */
    var chain = Promise.resolve();
    IDLE_ONLY.slice().reverse().forEach(function (src) {
      chain = chain.then(function () { return loadOne(src).catch(function () {}); });
    });
    return chain;
  }

  function warmIdle() {
    loadIdleOnly();
    if (state !== "idle") return;
    loadAll().catch(function () {});
  }
  if ("requestIdleCallback" in window) {
    requestIdleCallback(warmIdle, { timeout: 6000 });
  } else {
    setTimeout(warmIdle, 4000);
  }

  /* Exposed so a page can force it — the tutor profiles open the
     modal from their own code path. */
  window.EkGuruLazy = {
    load: loadAll,
    book: bookOrLoad,
    state: function () { return state; }
  };
})();

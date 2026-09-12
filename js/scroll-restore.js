/* =========================================================
   EkGuru — BACK RETURNS YOU WHERE YOU WERE          (v79)
   ---------------------------------------------------------
   WHAT PRAKASH REPORTED

     "page mein kahin se bhi kisi link par click karta hoon to
      link open ho jata hai, phir agar main back aaun to wapas
      usi jagah par aaun — ye nahi ki top par hi reh jaun."

   He is describing a real and very common failure, and it is
   worth being precise about the cause, because "the browser
   does that automatically" is the answer everyone gives and it
   is only sometimes true.

   ═══════════════════════════════════════════════════════
   WHY IT BREAKS ON THIS SITE SPECIFICALLY
   ═══════════════════════════════════════════════════════

   Browsers DO restore scroll position on back — but only if
   the page is the same height at restore time as it was when
   you left. On EkGuru it frequently is not:

     1. THE BACK/FORWARD CACHE IS OFTEN MISSED. A page that
        registered a service worker, or that ran a fetch that
        was still in flight, can be excluded from bfcache. It
        is then re-parsed from scratch and the browser restores
        a scroll offset against a document that is, for a few
        hundred milliseconds, much shorter than it was.

     2. CONTENT LANDS AFTER THE RESTORE. js/sheet.js fetches
        the Google Sheet and js/livepatch.js rewrites prices and
        names into the page. js/main.js renders the whole tutor
        list on find-tutors.html. Every one of those changes the
        document height AFTER the browser has already decided
        where to scroll. The browser restores to 4000px, the
        page is 1200px tall at that instant, so it clamps to the
        bottom — or to the top — and then the content arrives
        underneath you.

     3. IMAGES WITHOUT INTRINSIC SIZE. Any image that loads
        after layout pushes everything below it down. There are
        tutor photos on most pages.

   So this is not a case of "the browser forgot". The browser
   restored correctly against the wrong document.

   ═══════════════════════════════════════════════════════
   WHAT THIS FILE DOES
   ═══════════════════════════════════════════════════════

     · Takes manual control (history.scrollRestoration="manual")
       so the browser and this file are not fighting.

     · Saves the scroll position, keyed by the history entry,
       continuously while you scroll — throttled to one write
       per ~250ms so it costs nothing.

     · On a back navigation, restores it — and KEEPS RE-TRYING
       for a short window while the document is still growing,
       so late content cannot steal the position. It stops the
       moment you touch the page, so it can never fight you.

     · Also restores after a bfcache resume (pageshow.persisted),
       where no DOMContentLoaded fires at all.

   ═══════════════════════════════════════════════════════
   THINGS THIS DELIBERATELY DOES NOT DO
   ═══════════════════════════════════════════════════════

     · It does not touch a fresh navigation. Landing on a page
       for the first time must start at the top; restoring there
       would be bizarre.

     · It does not touch a #fragment link. If the URL names an
       anchor, that anchor wins — the visitor asked for it.

     · It does not use localStorage. Position is per history
       ENTRY, not per URL: open the same page twice at different
       depths and a URL-keyed store gives the wrong answer to
       one of them. sessionStorage keyed by history.state.k is
       correct, and it also expires with the tab, which is what
       a scroll position should do.

     · It never smooth-scrolls. html{scroll-behavior:smooth} is
       set globally in css/style.css, and animating a restore
       looks exactly like the jump this file exists to remove.
       This is the same trap that made the v74 hamburger bug
       look like a scroll bug.
   ========================================================= */

(function () {
  "use strict";

  /* Nothing to do in an environment without history or storage —
     and a failure here must never break a page, so every single
     access is wrapped. This file is loaded on 460+ pages. */
  if (typeof window === "undefined" || !window.history) return;

  var KEY_PREFIX = "ekg_sp_";
  var store = null;
  try { store = window.sessionStorage; } catch (e) { return; }
  if (!store) return;

  /* ---------------------------------------------------------
     A stable id for THIS history entry.
     history.state is ours to use; if something else owns it we
     merge rather than overwrite, because clobbering another
     script's state is how you break its back button.
     --------------------------------------------------------- */
  function entryKey() {
    var st = null;
    try { st = history.state; } catch (e) {}
    if (st && st.ekgKey) return st.ekgKey;

    var k = "e" + Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
    try {
      var merged = {};
      if (st && typeof st === "object") {
        for (var p in st) if (Object.prototype.hasOwnProperty.call(st, p)) merged[p] = st[p];
      }
      merged.ekgKey = k;
      history.replaceState(merged, document.title, location.href);
    } catch (e) {
      /* replaceState can throw on some file:// and sandboxed
         contexts. Fall back to a per-URL key: less correct when
         the same URL is in history twice, but far better than
         nothing, and it cannot throw again. */
      k = "u" + location.pathname + location.search;
    }
    return k;
  }

  var KEY = KEY_PREFIX + entryKey();

  function save(y) {
    try { store.setItem(KEY, String(y)); } catch (e) {}
  }
  function read() {
    try {
      var v = store.getItem(KEY);
      if (v === null) return null;
      var n = parseInt(v, 10);
      return isNaN(n) ? null : n;
    } catch (e) { return null; }
  }

  /* ---------------------------------------------------------
     Take manual control.
     Left on "auto", the browser restores at its own moment
     against a document that has not finished growing, and then
     this file restores again — two restores, one visible jump.
     One owner, no fight.
     --------------------------------------------------------- */
  try {
    if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  } catch (e) {}

  /* ---------------------------------------------------------
     Record the position while scrolling.
     Throttled with a trailing write: rAF alone drops the final
     position when scrolling stops between frames, and the final
     position is the only one that matters.
     --------------------------------------------------------- */
  var ticking = false, lastWrite = 0, trailing = null;

  function currentY() {
    return window.pageYOffset ||
      (document.documentElement && document.documentElement.scrollTop) || 0;
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      var now = Date.now();
      if (now - lastWrite > 250) { lastWrite = now; save(currentY()); }
      else {
        clearTimeout(trailing);
        trailing = setTimeout(function () { save(currentY()); }, 260);
      }
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });

  /* Leaving the page is the most important moment to record, and
     it is the one that is easiest to miss. `pagehide` fires in
     every case including bfcache; `visibilitychange` covers the
     iOS case where pagehide can be skipped. `unload` is
     deliberately NOT used — registering an unload handler
     disqualifies the page from bfcache entirely, which would
     CAUSE the problem this file is fixing. */
  window.addEventListener("pagehide", function () { save(currentY()); });
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") save(currentY());
  });

  /* Clicking a link is a strong signal that we are about to
     leave. Recorded synchronously so nothing can be lost to a
     navigation that starts before the next frame. */
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest && e.target.closest("a[href]");
    if (a) save(currentY());
  }, true);

  /* ---------------------------------------------------------
     RESTORE.
     ---------------------------------------------------------
     The hard part is not knowing WHERE to scroll — it is that
     the document is still growing. So we set the position, then
     keep re-asserting it for a short window, and give up the
     instant either (a) the position has held for a few frames,
     or (b) the visitor scrolls, taps or presses a key.

     Bounded by time AND by an interaction check, because an
     infinite corrector is a page you cannot scroll.
     --------------------------------------------------------- */
  function restore(target) {
    if (target == null || target <= 0) return;

    /* A #fragment is an explicit request. It wins. */
    if (location.hash && location.hash.length > 1) return;

    var cancelled = false;
    var started = Date.now();
    var holds = 0;

    function stop() { cancelled = true; }
    /* Any real interaction cancels immediately. `wheel` and
       `touchstart` fire BEFORE the scroll they cause, which is
       what makes this feel instant rather than a tug of war. */
    ["wheel", "touchstart", "keydown", "mousedown"].forEach(function (ev) {
      window.addEventListener(ev, stop, { passive: true, once: true });
    });

    function tick() {
      if (cancelled) return;
      if (Date.now() - started > 1200) return;   /* hard ceiling */

      var max = Math.max(
        document.body ? document.body.scrollHeight : 0,
        document.documentElement ? document.documentElement.scrollHeight : 0
      ) - window.innerHeight;

      /* The document is not tall enough YET. Do not clamp to the
         bottom — that is the visible symptom of this whole bug.
         Wait for the next frame instead; content is still landing. */
      if (max < target - 4) { requestAnimationFrame(tick); return; }

      if (Math.abs(currentY() - target) > 2) {
        holds = 0;
        /* behavior:"auto" defeats html{scroll-behavior:smooth}.
           Animating a restore looks exactly like the jump this
           file removes — the same trap as the v74 hamburger bug. */
        try { window.scrollTo({ top: target, behavior: "auto" }); }
        catch (e) { window.scrollTo(0, target); }
      } else if (++holds >= 3) {
        return;   /* held for three frames: the layout has settled */
      }
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  /* Was this a back/forward navigation, or a fresh one? Only a
     back should be restored — landing on a page for the first
     time must start at the top.

     Navigation Timing Level 2 first, because it is accurate.
     The deprecated Level 1 API is the fallback for older
     browsers. If neither is available we fall back to "did we
     save a position for THIS history entry", which is itself a
     decent signal: a fresh entry has no saved position. */
  function isBackForward() {
    try {
      var nav = performance.getEntriesByType &&
                performance.getEntriesByType("navigation")[0];
      if (nav && nav.type) return nav.type === "back_forward";
    } catch (e) {}
    try {
      if (performance.navigation) return performance.navigation.type === 2;
    } catch (e) {}
    return read() !== null;
  }

  function attempt() {
    if (!isBackForward()) return;
    restore(read());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", attempt);
  } else {
    attempt();
  }

  /* A bfcache resume fires NO DOMContentLoaded and no load — the
     page is simply reinstated. In that case the browser usually
     has the position right already, so we only correct it if it
     is visibly wrong, rather than scrolling a page that is
     already where it should be. */
  window.addEventListener("pageshow", function (e) {
    if (!e.persisted) return;
    var saved = read();
    if (saved == null) return;
    if (Math.abs(currentY() - saved) > 40) restore(saved);
  });

  /* Late-arriving content is the single biggest cause of this
     bug on this site: js/sheet.js fetches the spreadsheet and
     js/livepatch.js rewrites the page afterwards, and
     find-tutors.html renders its whole list from JavaScript. Both
     fire an event when they are done. Re-assert once after each,
     but ONLY on a back navigation and only if we have drifted —
     never on a fresh visit, and never if the visitor has already
     started reading somewhere else. */
  ["ekguru:sheet", "ekguru:render"].forEach(function (ev) {
    window.addEventListener(ev, function () {
      if (!isBackForward()) return;
      var saved = read();
      if (saved == null) return;
      if (Math.abs(currentY() - saved) > 40) restore(saved);
    });
  });

  /* Exposed for tools/test-scroll.js. Keeping the real functions
     reachable means the test exercises the shipped logic rather
     than a reimplementation of it — a test that reimplements the
     rule tests itself (v66, v74). */
  window.EkGuruScroll = {
    save: function () { save(currentY()); },
    saved: read,
    restore: restore,
    isBackForward: isBackForward,
    key: KEY
  };
})();

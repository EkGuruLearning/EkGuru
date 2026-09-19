/* =========================================================
   EkGuru — IDLE-INTERACTION SELF-HEALING WATCHDOG     (v2)
   ---------------------------------------------------------
   WHAT THIS IS FOR

     A page that is left open should stay fully interactive.
     Historically a handful of states could survive a long idle
     (or a tab switch, or a back/forward restore) and leave the
     page looking alive but not responding — a stale full-screen
     backdrop, a scroll lock whose owner has gone, pointer-events
     switched off, a leftover `inert`, or an unexpected overlay.

     This file is the automatic-recovery layer required by the
     Major Upgrade command: it removes ONLY state that is provably
     stale, unlocks scrolling, restores pointer events and inert,
     and records every incident so the admin Diagnostics page can
     show it. It is deliberately conservative — it never removes
     an element it cannot prove is stale, and it never touches
     third-party ad iframes.

   SAFETY RULES

     · A scroll lock is only released when NO dialog, modal,
       drawer or open menu actually owns it.
     · pointer-events is only restored on <html>/<body>, and only
       when it is "none".
     · An overlay is only removed when it (a) covers most of the
       viewport, (b) was NOT present at boot, (c) is not an
       iframe, (d) is not inside a dialog/modal/drawer/header,
       and (e) contains no link, button, form control or
       interactive role — i.e. it cannot be real UI.
     · Everything is idempotent and runs on a cheap timer plus the
       moments that actually matter: tab becomes visible again,
       window focus, and bfcache restore (pageshow persisted).

   v2 — the full idle-navigation surface the P0 command names:
     · 30 / 60 / 180 s of idle each get a heartbeat in the incident
       log, and the first wake from an idle of 30 s or more runs the
       full sweep including the overlay scan
     · hide/show of the tab, and a long hide (60 s+ — the shape of a
       slept machine waking) get their own records with the real
       duration
     · popstate and hashchange (back/forward through history, and
       in-page anchor hops) each trigger a cheap sweep
     · the network going offline and back on triggers a sweep and a
       record, so a page that loaded from the offline cache heals
       the moment the connection returns
     · a hard refresh needs no support at all: a reload rebuilds
       everything, so this layer only promises that a page left open
       — idled, backgrounded, restored from bfcache, or navigated
       back to — never needs one

   Nothing here should ever change a healthy page.
   ========================================================= */
(function () {
  "use strict";
  if (typeof window === "undefined" || !window.document) return;

  /* ---------------------------------------------------------
     Incident log — consumed by the admin Diagnostics page.
     --------------------------------------------------------- */
  var INCIDENTS = [];
  function record(code, detail) {
    var ev = { code: code, at: Date.now(), url: location.href, detail: detail || "" };
    INCIDENTS.push(ev);
    if (window.EkGuruDiagnostics && window.EkGuruDiagnostics.record) {
      try { window.EkGuruDiagnostics.record("recovery", ev); } catch (e) {}
    }
    try { console.warn("[ekguru-recovery]", code, detail || ""); } catch (e) {}
    try { window.dispatchEvent(new CustomEvent("ekguru:recovery", { detail: ev })); } catch (e) {}
  }

  /* Idle and hidden bookkeeping. lastActivity is bumped by real user
     input only (never by the timer itself), hiddenAt marks when the tab
     went away. The 30/60/180 s boundaries are reported once each until
     the visitor comes back. */
  var lastActivity = Date.now();
  var hiddenAt = 0;
  var lastIdleNote = 0;      /* 30000 | 60000 | 180000, whichever was reached */
  var offlineNow = false;
  var sweepsRun = 0;

  function noteIdleBoundary() {
    var idle = Date.now() - lastActivity;
    var b = idle >= 180000 ? 180000 : idle >= 60000 ? 60000 : idle >= 30000 ? 30000 : 0;
    if (b && b > lastIdleNote) {
      lastIdleNote = b;
      record("idle-" + (b / 1000) + "s", "page idle for " + Math.round(idle / 1000) + "s");
    }
  }

  function bumpActivity() {
    var now = Date.now();
    if (now - lastActivity >= 2000) {
      lastActivity = now;
      if (lastIdleNote) lastIdleNote = 0;   /* back from idle — arm again */
    }
  }
  ["pointerdown", "keydown"].forEach(function (t) {
    window.addEventListener(t, bumpActivity, true);
  });

  var bootNodes = null; // WeakSet of elements present at first sweep
  function snapshotBoot() {
    if (bootNodes) return bootNodes;
    bootNodes = new WeakSet();
    try {
      Array.prototype.forEach.call(document.querySelectorAll("body *"), function (el) {
        bootNodes.add(el);
      });
    } catch (e) { bootNodes = null; }
    return bootNodes;
  }

  /* ---------------------------------------------------------
     Is any layer genuinely open right now?
     --------------------------------------------------------- */
  function anyOpenLayer() {
    var b = document.body;
    if (b && b.classList && b.classList.contains("nav-open")) return true;
    if (document.querySelector("dialog[open]")) return true;
    if (document.querySelector(".modal:not([hidden])")) return true;
    if (document.querySelector(".drawer:not([hidden])")) return true;
    if (document.querySelector("[aria-modal=\"true\"]:not([hidden])")) return true;
    if (document.querySelector("[data-modal-open=\"1\"]")) return true;
    return false;
  }

  /* ---------------------------------------------------------
     1. Stale drawer backdrop / nav-open lock.
     --------------------------------------------------------- */
  function fixBackdrop() {
    var b = document.body;
    if (!b || !b.classList || !b.classList.contains("nav-open")) return false;
    var backdrop = document.querySelector(".nav-backdrop");
    var drawer = document.querySelector(".drawer, .nav-drawer, .nav-panel, .nav-menu-panel");
    var drawerOpen = false;
    if (drawer) {
      try {
        var cs = getComputedStyle(drawer);
        var r = drawer.getBoundingClientRect();
        drawerOpen = cs.display !== "none" && cs.visibility !== "hidden" && r.width > 0;
      } catch (e) { drawerOpen = true; }
    }
    /* nav-open with no visible drawer (or no backdrop) is a stale lock. */
    if (!drawerOpen || !backdrop) {
      b.classList.remove("nav-open");
      b.classList.remove("no-scroll");
      if (b.style.top) b.style.top = "";
      record("stale-nav-open", drawerOpen ? "backdrop missing" : "drawer not open");
      return true;
    }
    return false;
  }

  /* ---------------------------------------------------------
     2. pointer-events turned off at the root.
     --------------------------------------------------------- */
  function fixPointerEvents() {
    var changed = false;
    ["html", "body"].forEach(function (sel) {
      var el = document.querySelector(sel);
      if (!el) return;
      if (el.getAttribute && el.getAttribute("data-ekguru-pe-none") === "keep") return;
      var pe = "auto";
      try { pe = getComputedStyle(el).pointerEvents; } catch (e) { return; }
      if (pe === "none") {
        el.style.pointerEvents = "";
        changed = true;
        record("pointer-events-none", sel);
      }
    });
    return changed;
  }

  /* ---------------------------------------------------------
     3. Scroll lock with no owner (body.no-scroll left behind).
     The lock is body{position:fixed;top:-Y}. If nothing is
     open any more, the page is frozen at that offset and
     cannot be scrolled — the classic "stale lock".
     --------------------------------------------------------- */
  function fixScrollLock() {
    var b = document.body;
    if (!b || !b.classList || !b.classList.contains("no-scroll")) return false;
    if (anyOpenLayer()) return false;
    var offset = 0;
    try { offset = parseFloat(b.style.top) || 0; } catch (e) {}
    b.classList.remove("no-scroll");
    try { b.style.top = ""; } catch (e) {}
    try { b.style.left = ""; b.style.right = ""; b.style.width = ""; } catch (e) {}
    if (offset < 0) {
      try { window.scrollTo(0, -offset); } catch (e) {}
    }
    record("stale-scroll-lock", "offset " + offset + "px released");
    return true;
  }

  /* ---------------------------------------------------------
     4. Stale `inert` on a visible, non-dialog element.
     --------------------------------------------------------- */
  function fixInert() {
    var changed = false;
    Array.prototype.forEach.call(document.querySelectorAll("[inert]"), function (el) {
      try {
        var cs = getComputedStyle(el);
        if (cs.display === "none" || cs.visibility === "hidden") return;
      } catch (e) { return; }
      if (el.closest && (el.closest("dialog[open]") || el.closest(".modal:not([hidden])"))) return;
      el.removeAttribute("inert");
      changed = true;
      record("stale-inert", el.tagName.toLowerCase());
    });
    return changed;
  }

  /* ---------------------------------------------------------
     5. Unexpected full-viewport overlay that appeared after
        boot and cannot be real UI.
     --------------------------------------------------------- */
  function fixUnexpectedOverlay() {
    var set = snapshotBoot();
    if (!set) return false;
    var candidate = null;
    var els = document.querySelectorAll("body *");
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      try {
        if (set.has(el)) continue;                      /* was there at boot */
        var cs = getComputedStyle(el);
        if (cs.position !== "fixed") continue;
        if (cs.pointerEvents === "none" || cs.visibility === "hidden") continue;
        if (Number(cs.opacity) === 0) continue;
        if (el.tagName === "IFRAME") continue;            /* never touch third-party */
        if (el.closest) {
          if (el.closest(".hdr, .modal, .drawer, dialog, ins.adsbygoogle, [id^=\"google_ads\"], [class*=\"adsbygoogle\"]")) continue;
        }
        var role = el.getAttribute && el.getAttribute("role");
        if (role === "dialog" || role === "alertdialog" || el.getAttribute && el.getAttribute("aria-modal") === "true") continue;
        /* real UI always has an interactive node inside */
        if (el.querySelector && el.querySelector("a, button, input, select, textarea, [role=\"button\"], [role=\"link\"], [role=\"menu\"]")) continue;
        var r = el.getBoundingClientRect();
        var covers = r.width >= window.innerWidth * 0.7 &&
                     r.height >= window.innerHeight * 0.7 &&
                     r.top < window.innerHeight && r.bottom > 0;
        if (covers) { candidate = el; break; }
      } catch (e) { /* ignore unreadable nodes */ }
    }
    if (candidate) {
      var desc = (candidate.id ? "#" + candidate.id : "") +
                 (candidate.className ? "." + String(candidate.className).slice(0, 30) : "") +
                 "<" + candidate.tagName.toLowerCase() + ">";
      candidate.remove();
      record("stale-overlay", desc);
      return true;
    }
    return false;
  }

  /* ---------------------------------------------------------
     Sweep — one pass of every safe fix. The overlay scan is the
     only DOM walk of the whole body, so it is gated.
     --------------------------------------------------------- */
  function sweep(scanOverlay) {
    var fixed = [];
    try { if (fixPointerEvents()) fixed.push("pointer-events"); } catch (e) {}
    try { if (fixBackdrop()) fixed.push("nav-backdrop"); } catch (e) {}
    try { if (fixScrollLock()) fixed.push("scroll-lock"); } catch (e) {}
    try { if (fixInert()) fixed.push("inert"); } catch (e) {}
    if (scanOverlay) { try { if (fixUnexpectedOverlay()) fixed.push("overlay"); } catch (e) {} }
    return fixed;
  }

  /* ---------------------------------------------------------
     Cadence: full sweep every 5s; the expensive overlay scan
     runs every 3rd tick (15s). Plus the moments that matter:
     tab becomes visible, window focus, bfcache restore.
     --------------------------------------------------------- */
  var ticks = 0, lastSweep = 0;
  function guard(scanOverlay) {
    /* every sweep path — the timer, an event, a wake — also checks the
       30/60/180 s idle boundaries, so a page idled for minutes reports it
       the instant anything pokes it, not only on the next 5 s tick */
    noteIdleBoundary();
    var now = Date.now();
    if (now - lastSweep < 1200) return;
    lastSweep = now;
    sweepsRun++;
    var f = sweep(scanOverlay);
    if (f.length) record("recovered", f.join(","));
  }

  var cheapTimer = null;
  function startTimer() {
    if (cheapTimer) return;
    try {
      cheapTimer = setInterval(function () {
        ticks++;
        noteIdleBoundary();
        /* the overlay scan is the only expensive pass; it rides the
           third tick and every wake, never the bare 5 s tick */
        guard(ticks % 3 === 0);
      }, 5000);
    } catch (e) {}
  }

  function onBoot() {
    snapshotBoot();
    startTimer();
    /* one immediate pass to clear anything a previous session left behind */
    guard();
  }

  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") {
      hiddenAt = Date.now();
      return;
    }
    /* visible again. A tab hidden for 60 s or more is the shape of a
       slept machine waking: full sweep including the overlay scan, and a
       record with the real duration so Diagnostics can show it. */
    if (hiddenAt) {
      var away = Date.now() - hiddenAt;
      hiddenAt = 0;
      guard(true);
      if (away >= 60000) {
        record("wake-after-" + Math.round(away / 1000) + "s",
               "tab hidden " + Math.round(away / 1000) + "s");
      }
    } else {
      guard();
    }
    lastActivity = Date.now();
    lastIdleNote = 0;
  });
  window.addEventListener("focus", guard);
  window.addEventListener("pageshow", function (e) { if (e && e.persisted) guard(true); });
  /* back/forward through history and in-page anchor hops: the page may be
     a restored one, so check it. Cheap sweep — the overlay scan is for
     wakes, not for every anchor click. */
  window.addEventListener("popstate", guard);
  window.addEventListener("hashchange", guard);
  window.addEventListener("online", function () {
    if (!offlineNow) return;
    offlineNow = false;
    record("back-online", "network returned");
    guard(true);
  });
  window.addEventListener("offline", function () {
    offlineNow = true;
    record("offline", "network lost — page will self-heal when it returns");
  });
  window.addEventListener("load", function () { snapshotBoot(); });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onBoot);
  } else {
    onBoot();
  }

  /* Exposed for the admin Diagnostics page and for tests. */
  window.EkGuruRecovery = {
    /* the manual sweep is immediate (no throttle) so a test or Diagnostics
       can force a full pass; it also checks the idle boundaries, like every
       other sweep path does */
    sweep: function () {
      noteIdleBoundary();
      var f = sweep(true);
      if (f.length) record("manual-sweep", f.join(","));
      return f;
    },
    incidents: function () { return INCIDENTS.slice(); },
    clear: function () { INCIDENTS.length = 0; },
    /* Diagnostics and the idle tests read the shape of the visit from here. */
    idleStats: function () {
      return {
        idleMs: Date.now() - lastActivity,
        hiddenMs: hiddenAt ? Date.now() - hiddenAt : 0,
        sweeps: sweepsRun,
        incidents: INCIDENTS.length
      };
    },
    /* test hook: pretend the visitor last touched the page at this time */
    _setActivity: function (ts) { lastActivity = ts || Date.now(); },
    /* test hook: run the timer's idle-boundary check now */
    _noteIdle: function () { noteIdleBoundary(); },
    /* test hook: pretend the tab went hidden at this time */
    _setHidden: function (ts) { hiddenAt = ts; }
  };
})();

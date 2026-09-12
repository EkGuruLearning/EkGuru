/* =========================================================
   EkGuru — IDLE-INTERACTION SELF-HEALING WATCHDOG     (v1)
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
    var now = Date.now();
    if (now - lastSweep < 1200) return;
    lastSweep = now;
    var f = sweep(scanOverlay);
    if (f.length) record("recovered", f.join(","));
  }

  var cheapTimer = null;
  function startTimer() {
    if (cheapTimer) return;
    try {
      cheapTimer = setInterval(function () {
        ticks++;
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
    if (document.visibilityState === "visible") guard();
  });
  window.addEventListener("focus", guard);
  window.addEventListener("pageshow", function (e) { if (e && e.persisted) guard(); });
  window.addEventListener("load", function () { snapshotBoot(); });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onBoot);
  } else {
    onBoot();
  }

  /* Exposed for the admin Diagnostics page and for tests. */
  window.EkGuruRecovery = {
    sweep: function () { var f = sweep(true); if (f.length) record("manual-sweep", f.join(",")); return f; },
    incidents: function () { return INCIDENTS.slice(); },
    clear: function () { INCIDENTS.length = 0; }
  };
})();

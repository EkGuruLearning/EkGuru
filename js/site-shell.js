/* =========================================================
   EkGuru — SITE SHELL  (js/site-shell.js)
   ---------------------------------------------------------
   The 1,537 content pages get the site header and footer
   injected at build time (tools/build-shell.js). They do not
   load js/main.js — it expects to run from the site root and
   carries the whole store/mailer/routing stack with it — so
   this file is the small piece of behaviour the header needs
   on those pages, and nothing else.

   What it does:

     1. Opens and closes the menu, the way js/main.js does.
        Same technique, because the naive version is the bug
        Prakash reported twice:

            "header mai 3 lines open kerne pr kai bug hai
             background running nahi hota"

        Turning the menu on with only `body{overflow:hidden}`
        looks correct and is not: the page behind stays where
        the finger left it on some browsers, jumps to the top
        on others, and once the two disagree the visitor is
        stuck mid-page with a drawer over it.

        The fix is the one js/main.js settled on after the v74
        bug — remember the offset, pin the body with
        position:fixed and top:-<offset>px so nothing moves,
        then restore that exact offset on close with
        behavior:"auto" (or html{scroll-behavior:smooth}
        animates the restore and it reads as the jump the fix
        exists to remove).

     2. Fills the footer's year, and the brand/tagline/mode
        from the settings sheet if a live copy is on the page
        (window.EKGURU_SHEET_SETTINGS — js/livepatch.js puts it
        there on the pages that load it). The build already
        baked those values, so this is a correction, never a
        requirement: with no sheet on the page the baked
        values stand.

   It is deliberately dependency-free, ~3 KB, and does
   nothing at all if the page has no header.
   ========================================================= */

(function () {
  "use strict";

  var doc = document;

  function $(sel) { return doc.querySelector(sel); }

  /* ---------------------------------------------------------
     1. the menu — open, close, lock, restore
     --------------------------------------------------------- */
  function initMenu() {
    var nav = $(".hdr .nav"), burger = $(".hdr .burger");
    if (!nav || !burger) return;

    /* js/main.js (or js/experience.js) already bound this page's header:
       they are the ones that give the nav an id. Never fight over
       aria-expanded — two handlers means one click opens and closes, which
       is the "3 lines open karne pr kai bug hai" report.

       The flag is the same one js/main.js checks, and it is the reliable
       half of the handshake: `nav.id` only tells us who got there first,
       the flag tells both files to stay out of each other's way whichever
       order they load in. */
    if (window.EKGURU_DRAWER || nav.id) return;
    window.EKGURU_DRAWER = "shell";
    nav.id = "primary-nav";

    burger.setAttribute("aria-controls", nav.id);
    burger.setAttribute("aria-expanded", "false");

    var backdrop = $(".nav-backdrop");
    if (!backdrop) {
      backdrop = doc.createElement("div");
      backdrop.className = "nav-backdrop";
      backdrop.setAttribute("aria-hidden", "true");
      doc.body.appendChild(backdrop);
    }

    var isOpen = false;
    var savedY = 0;

    function focusables() {
      var inNav = nav.querySelectorAll("a[href],button:not([disabled]),input,select,[tabindex]:not([tabindex='-1'])");
      var out = [];
      for (var i = 0; i < inNav.length; i++) {
        if (inNav[i].offsetParent !== null) out.push(inNav[i]);
      }
      return out;
    }

    function open() {
      if (isOpen) return;
      /* read the position BEFORE anything moves it */
      savedY = window.scrollY || window.pageYOffset || 0;
      isOpen = true;
      nav.classList.add("open");
      burger.setAttribute("aria-expanded", "true");
      nav.removeAttribute("aria-hidden");
      doc.body.classList.add("nav-open");
      backdrop.setAttribute("aria-hidden", "false");
      /* the compensating offset — without it position:fixed snaps the
         view to the top, which is the same bug wearing a hat */
      doc.body.style.top = "-" + savedY + "px";
      var f = focusables();
      if (f.length) { try { f[0].focus(); } catch (e) {} }
    }

    function close(returnFocus) {
      if (!isOpen) return;
      isOpen = false;
      nav.classList.remove("open");
      burger.setAttribute("aria-expanded", "false");
      doc.body.classList.remove("nav-open");
      backdrop.setAttribute("aria-hidden", "true");
      doc.body.style.top = "";
      try { window.scrollTo({ top: savedY, behavior: "auto" }); }
      catch (e) { window.scrollTo(0, savedY); }
      if (returnFocus !== false) { try { burger.focus(); } catch (e2) {} }
    }

    burger.addEventListener("click", function (e) {
      e.stopPropagation();
      if (isOpen) close(); else open();
    });

    nav.addEventListener("click", function (e) {
      var a = e.target && e.target.closest ? e.target.closest("a") : null;
      if (a && isOpen) close(false);
    });

    doc.addEventListener("click", function (e) {
      if (isOpen && !nav.contains(e.target) && !burger.contains(e.target)) close(false);
    });

    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && isOpen) { close(); return; }
      if (e.key !== "Tab" || !isOpen) return;
      /* keep Tab inside the open drawer */
      var f = focusables();
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    /* A drawer left open while the viewport grows past the breakpoint
       would leave the page pinned: unlock it. */
    window.addEventListener("resize", function () {
      if (isOpen && window.innerWidth > 1200) close(false);
    });

    /* Coming back from the bfcache with the class still on <body> is the
       classic half-open drawer: no backdrop, page frozen. Reset it. */
    window.addEventListener("pageshow", function () {
      if (isOpen) close(false);
    });
  }

  /* ---------------------------------------------------------
     2. values the sheet owns
     --------------------------------------------------------- */
  function initValues() {
    var all = doc.querySelectorAll("[data-year]");
    var y = String(new Date().getFullYear());
    for (var i = 0; i < all.length; i++) all[i].textContent = y;

    var S = window.EKGURU_SHEET_SETTINGS;
    if (!S) return;                       /* baked values stand */

    if (S.tagline) {
      var tl = doc.querySelectorAll("[data-tagline]");
      for (var j = 0; j < tl.length; j++) {
        if (tl[j].textContent !== S.tagline) tl[j].textContent = S.tagline;
      }
    }
    if (S.mode) {
      var md = doc.querySelectorAll("[data-mode]");
      for (var k = 0; k < md.length; k++) md[k].textContent = S.mode;
    }
  }

  function boot() {
    try { initMenu(); } catch (e) {}
    try { initValues(); } catch (e) {}
    try { cleanupRemovedGame(); } catch (e2) {}
  }

  /* ---------------------------------------------------------
     3. one-time cleanup for the removed Offline Game product
     ---------------------------------------------------------
     The old Offline Game (js/offline-game.js, js/offline-games.js)
     was deleted from the site. Its floating button/dialog can no
     longer be created, but a returning visitor may still hold its
     localStorage keys and, if a stale cached page rendered the
     dialog, its DOM. Remove both once, then never touch storage
     again. Legitimate keys (progress, SRS, consent, settings)
     are never matched by the prefixes below.
     --------------------------------------------------------- */
  var GAME_CLEANED_KEY = "ekguru:game-removed:v1";
  function cleanupRemovedGame() {
    var box = null;
    try {
      if (window.localStorage) box = window.localStorage;
    } catch (e) { box = null; }
    if (box) {
      try {
        if (box.getItem(GAME_CLEANED_KEY) === "1") return;
      } catch (e) {}
      try {
        var drop = [];
        for (var i = 0; i < box.length; i++) {
          var k = box.key(i);
          if (k && (k.indexOf("ekguru:offline-game") === 0 ||
                    k.indexOf("ekguru:offline_game") === 0 ||
                    k.indexOf("ekguru:game:") === 0)) {
            drop.push(k);
          }
        }
        for (var d = 0; d < drop.length; d++) box.removeItem(drop[d]);
        box.setItem(GAME_CLEANED_KEY, "1");
      } catch (e2) {}
    }
    /* A stale cached page may still render the old dialog/button. */
    try {
      var stale = doc.querySelectorAll(
        "#ekguru-offline-game, #ekguru-offline-game-btn, .offline-game-header"
      );
      for (var s = 0; s < stale.length; s++) {
        var n = stale[s].id === "" && stale[s].className === "offline-game-header"
          ? stale[s].parentNode : stale[s];
        if (n && n.parentNode) n.parentNode.removeChild(n);
      }
    } catch (e3) {}
  }

  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", boot);
  else boot();
})();

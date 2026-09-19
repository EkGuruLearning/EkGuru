/* ==========================================================================
   EkGuru — SHARED GREETING  (v3 hardening, Gate 15)
   --------------------------------------------------------------------------
   ONE greeting system used by the homepage and the tutor profile pages.
   Any element with [data-ekguru-greeting] becomes a rotating greeting.

   Contract:
     · sequence: नमस्ते → Hello → Hola → Bonjour → Hallo → Olá →
       こんにちは → مرحبًا → (loops)
     · one shared 500 ms timer per page drives every mount (no duplicates)
     · Hindi on first render (also shipped in the HTML for no-JS/crawlers)
     · subtle fade/slide, stable line box (no vertical layout shift)
     · Arabic word carries dir="auto" so RTL shapes correctly
     · prefers-reduced-motion / no-JS: static Hindi, no timer at all
     · no network, no storage, screen-reader quiet (the animated word is
       aria-hidden; one static, visually-hidden label names the region)
     · timer pauses while the tab is hidden and stops on pagehide
   ========================================================================== */
(function (root, doc) {
  "use strict";

  if (!doc || !doc.querySelectorAll) return;
  if (root.EkGuruGreeting) return; /* loaded twice: the first copy wins */

  var WORDS = ["\u0928\u092E\u0938\u094D\u0924\u0947", "Hello", "Hola", "Bonjour",
               "Hallo", "Ol\u00E1", "\u3053\u3093\u306B\u3061\u306F",
               "\u0645\u0631\u062D\u0628\u064B\u0627"];
  var INTERVAL_MS = 500;
  var STYLE_ID = "ekguru-greeting-css";

  function reduced() {
    try {
      return !!(root.matchMedia &&
        root.matchMedia("(prefers-reduced-motion: reduce)").matches);
    } catch (e) { return false; }
  }

  function injectStyles() {
    if (doc.getElementById(STYLE_ID)) return;
    var css =
      ".ekg-greeting-line{margin:0 0 .15em;font-size:clamp(1.35rem,2.6vw,1.9rem);" +
      "font-weight:800;letter-spacing:-.01em;line-height:1.5;" +
      "color:var(--xp-a,var(--brand,#4f32d9))}" +
      "[data-ekguru-greeting]{display:inline-block;line-height:1.5;min-height:1.5em;" +
      "vertical-align:baseline}" +
      "[data-ekguru-greeting] .ekg-greet-w{display:inline-block}" +
      "[data-ekguru-greeting] .ekg-greet-w.ekg-swap{" +
      "animation:ekgGreetIn .45s cubic-bezier(.22,1,.36,1)}" +
      "@keyframes ekgGreetIn{from{opacity:0;transform:translateY(.45em)}" +
      "to{opacity:1;transform:translateY(0)}}" +
      ".ekg-greet-sr{position:absolute!important;width:1px;height:1px;margin:-1px;" +
      "overflow:hidden;clip-path:inset(50%);white-space:nowrap;border:0;padding:0}" +
      "@media (prefers-reduced-motion:reduce){" +
      "[data-ekguru-greeting] .ekg-greet-w.ekg-swap{animation:none}}" +
      "@media print{[data-ekguru-greeting] .ekg-greet-w.ekg-swap{animation:none}}";
    var st = doc.createElement("style");
    st.id = STYLE_ID;
    st.type = "text/css";
    if (st.styleSheet) st.styleSheet.cssText = css;
    else st.appendChild(doc.createTextNode(css));
    var head = doc.head || doc.getElementsByTagName("head")[0] || doc.documentElement;
    head.appendChild(st);
  }

  var mounts = [];
  var timer = null;
  var index = 0;
  var started = false;

  function prepare(el) {
    /* Ship Hindi in the HTML; here wrap it so swaps animate. */
    var inner = el.querySelector(".ekg-greet-w");
    if (!inner) {
      inner = doc.createElement("span");
      inner.className = "ekg-greet-w";
      inner.setAttribute("dir", "auto");
      inner.textContent = WORDS[0];
      el.textContent = "";
      el.appendChild(inner);
    } else {
      inner.setAttribute("dir", "auto");
      if (!inner.textContent) inner.textContent = WORDS[0];
    }
    /* The animation is decoration: hide it from assistive tech and name the
       region once, so a screen reader hears one label, not a word a second. */
    el.setAttribute("aria-hidden", "true");
    if (!el.parentNode.querySelector(".ekg-greet-sr")) {
      var sr = doc.createElement("span");
      sr.className = "ekg-greet-sr";
      sr.textContent = "Welcome";
      el.parentNode.insertBefore(sr, el.nextSibling);
    }
    return inner;
  }

  function tick() {
    if (doc.hidden) return; /* tab in background: hold the frame */
    index = (index + 1) % WORDS.length;
    for (var i = 0; i < mounts.length; i++) {
      var inner = mounts[i];
      inner.textContent = WORDS[index];
      /* Restart the entrance animation without extra timers. */
      inner.classList.remove("ekg-swap");
      try { void inner.offsetWidth; } catch (e) {}
      inner.classList.add("ekg-swap");
    }
  }

  function start() {
    if (started) return;
    var found = doc.querySelectorAll("[data-ekguru-greeting]");
    if (!found || !found.length) return;
    started = true;
    injectStyles();
    for (var i = 0; i < found.length; i++) {
      try { mounts.push(prepare(found[i])); } catch (e) {}
    }
    if (!mounts.length) return;
    if (reduced()) return; /* static Hindi, no timer */
    timer = root.setInterval(tick, INTERVAL_MS);
    var stop = function () {
      if (timer) { root.clearInterval(timer); timer = null; }
    };
    try {
      root.addEventListener("pagehide", stop);
      /* bfcache restore: one timer again, never two. */
      root.addEventListener("pageshow", function () {
        if (started && !timer && !reduced()) timer = root.setInterval(tick, INTERVAL_MS);
      });
    } catch (e) {}
  }

  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", start);
  else start();

  root.EkGuruGreeting = {
    words: WORDS.slice(),
    intervalMs: INTERVAL_MS,
    mountCount: function () { return mounts.length; },
    currentIndex: function () { return index; },
    currentWord: function () { return WORDS[index]; },
    _tick: tick
  };
})(typeof window !== "undefined" ? window : this,
   typeof document !== "undefined" ? document : null);

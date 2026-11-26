/* =========================================================
   EkGuru — REAL SITE-WIDE ANALYTICS
   ---------------------------------------------------------
   WHAT THIS SOLVES

   The Activity tab in the admin dashboard records what
   happens in ONE browser — yours. That is useful for testing
   the booking funnel and useless for answering "how many
   people visited the site yesterday".

   A static site cannot count visitors on its own. Something
   outside has to do the counting. This file wires that up,
   with a deliberate choice about which something.

   ---------------------------------------------------------
   WHY NOT GOOGLE ANALYTICS

   It is free and it is the default, so it deserves a reason.

     · It sets cookies and tracks people across sites, which
       means you need a cookie banner in the EU and the UK.
     · Your visitors' browsing becomes Google's data.
     · It is heavy — roughly 45 KB, and it slows the page.
     · Ad blockers block it, so the numbers under-report
       anyway, often by 20-40%.

   For a small tutoring site none of that is worth it. The two
   options below count visits without any of it.

   ---------------------------------------------------------
   THE TWO SUPPORTED PROVIDERS

   GOATCOUNTER — free forever for non-commercial and small
   sites, open source, ~3.5 KB, no cookies, no personal data.
   Sign up at goatcounter.com, pick a code like "ekguru", and
   your dashboard is at ekguru.goatcounter.com. This is the
   one to start with.

   PLAUSIBLE — same privacy model, better dashboard, ~1 KB.
   Paid after a 30-day trial, from about $9 a month. Worth it
   later if traffic grows.

   Neither sets a cookie. Neither needs a consent banner under
   GDPR, because neither stores personal data. Counting therefore
   runs by default; the privacy notice, Do Not Track and Global
   Privacy Control all switch it OFF (see THE GATE below).

   ---------------------------------------------------------
   TO SWITCH ON

       js/site-config.js
         analytics: { provider: "goatcounter", site: "ekguru" }

   Leave provider as "" and nothing loads at all — not a
   single request. That is the default, so the site ships
   with no third-party tracking until you decide otherwise.
   ========================================================= */

(function () {
  "use strict";

  /* Site-wide [data-eg-share-copy] click handler — must bind BEFORE any
     analytics early-return so Copy Profile Link works on localhost,
     preview hosts, and browsers that opted out of analytics. */
  if (!window.__egShareBound && typeof document !== "undefined" && document && typeof document.addEventListener === "function") {
    window.__egShareBound = true;
    document.addEventListener("click", function (ev) {
      var el = ev && ev.target && ev.target.closest ? ev.target.closest("[data-eg-share-copy]") : null;
      if (!el) return;
      var url = el.getAttribute("data-eg-share-copy");
      if (!url) return;
      var orig = el.getAttribute("data-eg-orig-label") || el.textContent;
      el.setAttribute("data-eg-orig-label", orig);
      function markDone() {
        el.textContent = "✓ Link copied";
        setTimeout(function () { el.textContent = orig; }, 1800);
        try {
          if (window.EkGuruAnalytics && window.EkGuruAnalytics.event) {
            window.EkGuruAnalytics.event("share_copy", el.getAttribute("data-eg-share-label") || url);
          }
        } catch (e) {}
      }
      if (typeof navigator !== "undefined" && navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(markDone, markDone);
      } else {
        try {
          var ta = document.createElement("textarea");
          ta.value = url;
          document.body.appendChild(ta);
          ta.select();
          document.execCommand("copy");
          document.body.removeChild(ta);
        } catch (e) {}
        markDone();
      }
    });
  }

  var S = window.EKGURU_SITE || {};
  var CFG = S.analytics || {};
  var provider = String(CFG.provider || "").toLowerCase().trim();

  if (!provider) return;                 /* nothing configured, load nothing */
  if (!CFG.site) {
    console.warn('[EkGuru] analytics.provider is set to "' + provider +
      '" but analytics.site is empty. See js/site-config.js.');
    return;
  }

  /* Never count your own visits. The admin dashboard sets this
     flag, and you can set it yourself from the console with
     localStorage.setItem("ekguru_no_track","1"). */
  try {
    if (localStorage.getItem("ekguru_no_track") === "1") {
      console.info("[EkGuru] analytics skipped — this browser is marked as yours.");
      return;
    }
  } catch (e) {}

  /* Local development should not pollute real numbers. */
  var host = location.hostname;
  if (host === "localhost" || host === "127.0.0.1" || host === "" ||
      /^192\.168\./.test(host) || /\.local$/.test(host)) {
    return;
  }

  function load(src, attrs) {
    var s = document.createElement("script");
    s.async = true;
    s.defer = true;
    s.src = src;
    Object.keys(attrs || {}).forEach(function (k) { s.setAttribute(k, attrs[k]); });
    document.head.appendChild(s);
    return s;
  }

  /* Browser-level "do not track me" signals (Do Not Track, Global Privacy
     Control) are honoured as an opt-out even though GoatCounter stores no
     cookie and no personal data. */
  function browserOptsOut() {
    try {
      if (navigator.globalPrivacyControl === true) return true;
      var dnt = navigator.doNotTrack || window.doNotTrack || navigator.msDoNotTrack;
      return dnt === "1" || dnt === "yes";
    } catch (e) { return false; }
  }

  /* ---------------------------------------------------------
     THE GATE (18 Nov 2026)

     Until this date GoatCounter loaded only after a visitor
     pressed "Accept all" in the privacy notice. The notice
     appears 1.2 s after load, most people never touch it, and
     the dashboard showed 1-3 visits a day against ~2,000 real
     page loads at the CDN. The owner could not see his own
     traffic.

     GoatCounter is cookieless, keeps no personal data and sets
     no cross-site identifier, so page counting now runs by
     default and the choice is an OPT-OUT, honoured three ways:

       · "Only essential" / Analytics unticked in the notice
         (ekguru_cookie_consent_v3.analytics === false)
       · Do Not Track or Global Privacy Control in the browser
       · ekguru_no_track (the owner's own browsers)

     An explicit "no" wins over everything. An absent record
     (no choice yet) counts the page.
     --------------------------------------------------------- */
  var started = false;
  function analyticsAllowed() {
    if (browserOptsOut()) return false;
    try {
      var consent = JSON.parse(localStorage.getItem("ekguru_cookie_consent_v3") || "null");
      if (consent && consent.analytics === false) return false;
    } catch (e) {}
    return true;
  }

  function bootAnalytics() {
    if (started || !analyticsAllowed()) return;
    started = true;

  if (provider === "goatcounter") {
    /* GoatCounter counts the page view itself on load. */
    window.goatcounter = { no_onload: false };
    load("https://gc.zgo.at/count.js", {
      "data-goatcounter": "https://" + CFG.site + ".goatcounter.com/count"
    });

    /* Record the things that matter as events, so the dashboard
       shows more than page views. Each is a path-style name so it
       groups neatly in GoatCounter's list. */
    window.addEventListener("ekguru:event", function (e) {
      try {
        if (!analyticsAllowed() || !window.goatcounter || !window.goatcounter.count) return;
        window.goatcounter.count({
          path: "event/" + (e.detail && e.detail.name || "unknown"),
          title: (e.detail && e.detail.label) || "",
          event: true
        });
      } catch (err) {}
    });
  }

  if (provider === "plausible") {
    load("https://plausible.io/js/script.tagged-events.outbound-links.js", {
      "data-domain": CFG.site
    });
    window.plausible = window.plausible || function () {
      (window.plausible.q = window.plausible.q || []).push(arguments);
    };
    window.addEventListener("ekguru:event", function (e) {
      try {
        if (!analyticsAllowed()) return;
        window.plausible((e.detail && e.detail.name) || "event",
          { props: { label: (e.detail && e.detail.label) || "" } });
      } catch (err) {}
    });
  }

  /* One small helper the rest of the site calls. It fires an event
     that both providers listen for above, and does nothing at all
     when analytics is switched off. */
  window.EkGuruAnalytics = {
    provider: provider,
    site: CFG.site,
    event: function (name, label) {
      try {
        window.dispatchEvent(new CustomEvent("ekguru:event", {
          detail: { name: name, label: label || "" }
        }));
      } catch (e) {}
    },
    /* Mark this browser so your own visits stop being counted. */
    optOut: function () {
      try { localStorage.setItem("ekguru_no_track", "1"); } catch (e) {}
    },
    optIn: function () {
      try { localStorage.removeItem("ekguru_no_track"); } catch (e) {}
    },
    isOptedOut: function () {
      try { return localStorage.getItem("ekguru_no_track") === "1"; } catch (e) { return false; }
    }
  };
  }

  // Default and "Accept": the cookieless provider starts now. "Only essential",
  // an unticked Analytics box, DNT or GPC: nothing is requested. Switching
  // analytics on later starts it without a reload; switching it off stops
  // every later EkGuru event — an already-sent page view cannot be recalled.
  bootAnalytics();
  document.addEventListener("ekguru:consent", function (event) {
    if (!event.detail) return;
    if (event.detail.analytics === true) { bootAnalytics(); return; }
    if (event.detail.analytics === false && started && window.goatcounter) {
      /* Withdrawn after the script loaded: silence every later call,
         including the direct window.goatcounter.count() calls in older
         page scripts that do not go through EkGuruAnalytics.event(). */
      try { window.goatcounter.count = function () {}; } catch (e) {}
    }
  });
})();

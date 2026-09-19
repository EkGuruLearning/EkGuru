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
   GDPR, because neither stores personal data.

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
        if (!window.goatcounter || !window.goatcounter.count) return;
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
})();

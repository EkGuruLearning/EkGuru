/* =========================================================
   EkGuru — SUPPORT TAB DYNAMIC RENDERER (v2)
   ---------------------------------------------------------
   PayPal + Razorpay are STATIC HTML in support/index.html
   (force fix, 4 Nov 2026) — they render with zero JavaScript.
   This file does only two things:

   1. UPGRADE the two static links when the sheet holds a
      different valid URL for them (override path — the sheet
      can still move either method, it just can never hide them).
   2. RENDER the extra methods (UPI, Stripe, crypto, Revolut)
      from the sheet into #support-options. An empty / "none" /
      missing extra renders nothing.

   js/settings.js loads the support/payments tab into
   EKGURU_SITE and fires "ekguru:settings"; this file re-renders
   on that event and re-polls every 60 seconds.

   No payment link is hardcoded here: the always-on hrefs live
   once in support/index.html, and tools/test-support-static.mjs
   fails if they ever drift from js/site-config.js.
   ========================================================= */
(function (root) {
  "use strict";

  /* Extra methods only — PayPal/Razorpay are static markup. */
  var OPTIONS = [
    { key: "supportUpi",      icon: "📲", label: "UPI",      kind: "link",   hint: "Scan or tap to pay via UPI" },
    { key: "supportStripe",   icon: "💳", label: "Stripe",  kind: "link",   hint: "Opens the Stripe payment page" },
    { key: "supportBtc",      icon: "₿",  label: "Bitcoin", kind: "address", hint: "Send BTC to this address" },
    { key: "supportEth",      icon: "Ξ",  label: "Ethereum", kind: "address", hint: "Send ETH to this address" },
    { key: "supportUsdt",     icon: "₮",  label: "USDT",   kind: "address", hint: "Send USDT (TRC-20) to this address" },
    { key: "supportRevolut",  icon: "🏦", label: "Revolut", kind: "link",   hint: "Opens your Revolut payment link" }
  ];

  /* Static always-on links this file may upgrade (never hide). */
  var STATIC_LINKS = [
    { key: "supportPaypal",   id: "support-link-paypal" },
    { key: "supportRazorpay", id: "support-link-razorpay" }
  ];

  function value(key) {
    var v = String((root.EKGURU_SITE || {})[key] || "").trim();
    if (/^(none|no|off)$/i.test(v)) v = "";
    /* Owner decision (4 Nov 2026): PayPal + Razorpay are always on.
       If the live value is empty — a stale pre-fix cache, a sheet
       "none", a failed fetch — fall back to the baked-in snapshot
       from js/site-config.js. A valid sheet URL still overrides. */
    if (!v) {
      var baked = String(((root.EKGURU_BAKED_SUPPORT || {})[key]) || "").trim();
      if (baked) return baked;
    }
    return v;
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  /* Point the static cards at the sheet's URL when it holds a
     different valid one. Never empties or hides them: an empty /
     "none" value is a no-op because the static href is already the
     baked default the sheet would restore. */
  function upgradeStaticLinks() {
    if (!root.document || !root.document.getElementById) return;
    STATIC_LINKS.forEach(function (s) {
      var el = root.document.getElementById(s.id);
      if (!el) return;
      var v = value(s.key);
      if (v && el.getAttribute("href") !== v) el.setAttribute("href", v);
    });
  }

  function card(o) {
    var v = value(o.key);
    if (!v) return "";
    if (o.kind === "link") {
      return '<a class="support-option" href="' + esc(v) + '" target="_blank" rel="noopener noreferrer">' +
        '<span class="support-option-icon" aria-hidden="true">' + o.icon + "</span>" +
        "<span><b>" + esc(o.label) + "</b><small>" + esc(o.hint) + "</small></span>" +
        '<span class="support-option-arrow" aria-hidden="true">→</span></a>';
    }
    return '<div class="support-option support-option-addr">' +
      '<span class="support-option-icon" aria-hidden="true">' + o.icon + "</span>" +
      "<span><b>" + esc(o.label) + "</b><small>" + esc(o.hint) + "</small>" +
      '<code class="support-option-addr-val">' + esc(v) + "</code></span>" +
      '<button type="button" class="support-option-copy" data-copy="' + esc(v) + '">Copy</button></div>';
  }

  function render() {
    upgradeStaticLinks();
    var host = root.document.getElementById("support-options");
    if (!host) return 0;
    var cards = OPTIONS.map(card).filter(function (h) { return h !== ""; });
    /* No extras is not an error state — the two static cards above
       already show. Leave the container empty, not apologetic. */
    host.innerHTML = cards.join("");
    var btns = host.querySelectorAll(".support-option-copy");
    Array.prototype.forEach.call(btns, function (b) {
      b.addEventListener("click", function () {
        var txt = b.getAttribute("data-copy");
        var done = function () { b.textContent = "✓ Copied"; setTimeout(function () { b.textContent = "Copy"; }, 1600); };
        if (root.navigator && root.navigator.clipboard && root.navigator.clipboard.writeText) {
          root.navigator.clipboard.writeText(txt).then(done, function () {});
        }
      });
    });
    return cards.length;
  }

  function renderHours() {
    var el = root.document.getElementById("support-hours");
    if (!el) return;
    var h = value("supportHours");
    el.textContent = h || "";
    el.style.display = h ? "" : "none";
  }

  var POLL_MS = 60000;
  var pollTimer = null;

  function startPolling() {
    if (pollTimer) return;
    if (!root.EkGuruSettings || !root.EkGuruSettings.refresh) return;
    pollTimer = root.setInterval(function () {
      try { root.EkGuruSettings.refresh(); } catch (e) {}
    }, POLL_MS);
  }

  function init() {
    render();
    renderHours();
    root.addEventListener("ekguru:settings", function () {
      render();
      renderHours();
    });
    startPolling();
  }

  root.EkGuruSupport = { render: render, init: init, value: value, upgradeStaticLinks: upgradeStaticLinks };
  if (root.document.readyState === "loading") {
    root.document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})(typeof window !== "undefined" ? window : globalThis);

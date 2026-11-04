/* =========================================================
   EkGuru — SUPPORT TAB DYNAMIC RENDERER (v1)
   ---------------------------------------------------------
   Every payment option on /support/ comes from the sheet.
   js/settings.js loads the support/payments tab and puts each
   value into EKGURU_SITE (supportUpi, supportPaypal,
   supportBtc, supportEth, supportUsdt, supportRazorpay,
   supportStripe, supportRevolut, supportHours).

   This file renders ONLY what the sheet sets — except PayPal and
   Razorpay, which are the owner's always-on methods (4 Nov 2026):
   for those two, an empty / "none" / missing value falls back to
   the baked-in snapshot from js/site-config.js, so both render even
   when the sheet is unreachable or a stale cache wiped them. Every
   other method with an empty, "none", or missing value renders
   nothing — deleting such a row removes the option instantly. When
   the sheet changes, settings.js fires "ekguru:settings" and this
   file re-renders.

   No payment link is hardcoded here: the fallback lives once in
   js/site-config.js (EKGURU_BAKED_SUPPORT), never in this file.
   ========================================================= */
(function (root) {
  "use strict";

  var OPTIONS = [
    { key: "supportUpi",      icon: "📲", label: "UPI",      kind: "link",   hint: "Scan or tap to pay via UPI" },
    { key: "supportPaypal",   icon: "🅿️", label: "PayPal",  kind: "link",   hint: "Opens your PayPal page" },
    { key: "supportRazorpay", icon: "⚡", label: "Razorpay", kind: "link",   hint: "Opens the hosted payment page" },
    { key: "supportStripe",   icon: "💳", label: "Stripe",  kind: "link",   hint: "Opens the Stripe payment page" },
    { key: "supportBtc",      icon: "₿",  label: "Bitcoin", kind: "address", hint: "Send BTC to this address" },
    { key: "supportEth",      icon: "Ξ",  label: "Ethereum", kind: "address", hint: "Send ETH to this address" },
    { key: "supportUsdt",     icon: "₮",  label: "USDT",   kind: "address", hint: "Send USDT (TRC-20) to this address" },
    { key: "supportRevolut",  icon: "🏦", label: "Revolut", kind: "link",   hint: "Opens your Revolut payment link" }
  ];

  function value(key) {
    var v = String((root.EKGURU_SITE || {})[key] || "").trim();
    if (/^(none|no|off)$/i.test(v)) v = "";
    /* Owner decision (4 Nov 2026): PayPal + Razorpay are always on.
       If the live value is empty — a stale pre-fix cache, a sheet
       "none", a failed fetch — fall back to the baked-in snapshot
       from js/site-config.js so both methods still render. A valid
       sheet URL still overrides (it lands in EKGURU_SITE above). */
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
    var host = root.document.getElementById("support-options");
    if (!host) return 0;
    var cards = OPTIONS.map(card).filter(function (h) { return h !== ""; });
    if (!cards.length) {
      host.innerHTML =
        '<p class="support-empty">No contribution methods are available right now. ' +
        "Please check back later, or share EkGuru with a friend — that helps just as much.</p>";
      return 0;
    }
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

  var loadingTimer = null;

  function armLoadingFallback() {
    if (loadingTimer) root.clearTimeout(loadingTimer);
    loadingTimer = root.setTimeout(clearLoading, 8000);
  }

  function clearLoading() {
    var host = root.document.getElementById("support-options");
    if (!host) return;
    var loading = host.querySelector(".support-loading");
    if (loading && !host.querySelector(".support-option, .support-empty")) {
      // Sheet never loaded — show the empty message instead of
      // leaving "Loading contribution methods…" forever.
      host.innerHTML =
        '<p class="support-empty">Contribution methods are temporarily unavailable. ' +
        "Please check back later, or share EkGuru with a friend — that helps just as much.</p>";
    }
  }

  function init() {
    render();
    renderHours();
    // If the sheet is slow or unreachable, the loading text would
    // stay forever. Clear it after 8 seconds if nothing rendered.
    armLoadingFallback();
    root.addEventListener("ekguru:settings", function () {
      render();
      renderHours();
      // Re-arm the fallback timer on each settings event.
      armLoadingFallback();
    });
    startPolling();
  }

  root.EkGuruSupport = { render: render, init: init, value: value };
  if (root.document.readyState === "loading") {
    root.document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})(typeof window !== "undefined" ? window : globalThis);

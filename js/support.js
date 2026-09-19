/* =========================================================
   EkGuru — SUPPORT PAGE  (v142)
   ---------------------------------------------------------
   Every payment detail on /support/ comes from the settings
   sheet and NOTHING is hardcoded here:

       key              value
       supportUpi       owner@upi
       supportRazorpay  https://rzp.io/l/...
       supportPaypal    https://paypal.me/ownername
       supportStripe    https://buy.stripe.com/...
       supportRevolut   https://revolut.me/username
       supportBtc       bc1...
       supportEth       0x...
       supportUsdt      T... (or 0x...)

   The owner adds/edits these rows; the site follows on the
   next page view (js/settings.js validates + refreshes, this
   file repaints on the ekguru:settings event). Unset keys
   render as "Coming soon" — never a broken button.

   Link/copy UI only: upi://pay intents, a PayPal.me link and
   copyable crypto addresses. No checkout backend, and secret
   API keys must NEVER go in the public settings sheet.
   ========================================================= */
(function () {
  "use strict";

  var METHODS = ["razorpay", "upi", "paypal", "stripe", "revolut", "btc", "eth", "usdt"];

  function val(card) {
    if (card === "razorpay") {
      var liveRzp = (window.EKGURU_SITE || {}).supportRazorpay;
      var bakedRzp = (window.EKGURU_SHEET_SETTINGS || {}).supportRazorpay;
      return String(liveRzp || bakedRzp || window.RAZORPAY_PAYMENT_LINK || "https://rzp.io/rzp/EkGuru").trim();
    }
    var key = "support" + card.charAt(0).toUpperCase() + card.slice(1);
    var live = (window.EKGURU_SITE || {})[key];
    var baked = (window.EKGURU_SHEET_SETTINGS || {})[key];
    return String(live || baked || "").trim();
  }

  function copyText(t, btn) {
    if (!t) return;
    function done(ok) {
      if (!btn) return;
      var old = btn.getAttribute("data-label") || btn.textContent;
      if (!btn.getAttribute("data-label")) btn.setAttribute("data-label", old);
      btn.textContent = ok ? "Copied ✓" : "Copy failed — long-press to copy";
      setTimeout(function () { btn.textContent = btn.getAttribute("data-label"); }, 2200);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(t).then(function () { done(true); }, function () { done(false); });
    } else {
      try {
        var ta = document.createElement("textarea");
        ta.value = t;
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        done(document.execCommand("copy"));
        document.body.removeChild(ta);
      } catch (e) { done(false); }
    }
  }

  function paint() {
    var any = false;
    METHODS.forEach(function (card) {
      var v = val(card);
      var el = document.getElementById("m-" + card);
      if (!el) return;
      if (!v) { el.classList.add("off"); return; }
      any = true;
      el.classList.remove("off");
      var idEl = el.querySelector("[data-val]");
      if (idEl) idEl.textContent = v;
      var go = el.querySelector("[data-go]");
      if (go) {
        if (card === "upi") {
          go.setAttribute("href", "upi://pay?pa=" + encodeURIComponent(v) +
            "&pn=" + encodeURIComponent("EkGuru") + "&cu=INR");
        } else {
          /* Link-type cards (PayPal/Razorpay/Stripe/Revolut): the
             sheet URL opens the provider's secure page. */
          go.setAttribute("href", v);
        }
      }
      /* Quick amounts are DERIVED from the sheet URL, never hardcoded:
         paypal.me/NAME + /5USD etc. Only the PayPal card has them.
         Query/hash (?locale.x=...) is stripped first — amounts must
         attach to the bare path or PayPal ignores them. */
      var amts = el.querySelectorAll("[data-amt]");
      var amtBase = v.split(/[?#]/)[0].replace(/\/+$/, "");
      for (var i = 0; i < amts.length; i++) {
        amts[i].setAttribute("href",
          amtBase + "/" + amts[i].getAttribute("data-amt") + "USD");
      }
      var cp = el.querySelector("[data-copy]");
      if (cp) cp.setAttribute("data-copy-text", v);
    });
    var empty = document.getElementById("support-empty");
    if (empty) empty.style.display = any ? "none" : "";
    var list = document.getElementById("support-list");
    if (list) list.style.display = any ? "" : "none";
  }

  document.addEventListener("click", function (ev) {
    var b = ev.target.closest ? ev.target.closest("[data-copy]") : null;
    if (!b) return;
    ev.preventDefault();
    copyText(b.getAttribute("data-copy-text") || "", b);
  });

  document.addEventListener("DOMContentLoaded", paint);
  window.addEventListener("ekguru:settings", paint);
  try { paint(); } catch (e) {}
})();

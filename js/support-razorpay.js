/**
 * EkGuru — Razorpay Support Client (v2 — hosted Payment Page era)
 *
 * Current user-facing payment on /support/ is the OFFICIAL Razorpay Payment
 * Page embed + direct payment link fallback — both declared in
 * support/index.html, no JS required. This file no longer drives that
 * button; it keeps the future custom multi-currency API checkout
 * (PAYMENT_MODE = "LIVE_API") intact for later reactivation, plus:
 *
 * 1. Sanitized Recent Supporters lazy loading & rendering — INDEPENDENT of
 *    the payment form, so it works whether or not the form section exists
 * 2. Future API flow (kept for reactivation):
 *    - Dynamic verified currency registry loading
 *    - Currency-aware quick amounts and decimal formatting
 *    - Customer detail collection & opt-in consent handling
 *    - Backend order creation (create-order) via the Apps Script endpoint
 *    - Razorpay Standard Checkout modal invocation with customer prefill
 *    - Server-side signature verification (verify-payment)
 *    - Authentic success/failure state rendering (guaranteed no fake success)
 *
 * SAFETY:
 * - While PAYMENT_MODE = "COMING_SOON" the custom form is inert: the submit
 *   is disabled, submit is intercepted, no create-order call is made.
 * - The local test-mode simulation modal (openMockCheckoutModal) is a
 *   development aid only and is HARD-BLOCKED on production hosts by
 *   isProductionHost(), independent of mode or payload.
 */

(function (root) {
  "use strict";

  /* Double-execution guard: a second run would bind a second submit
     listener (two create-order calls per click in LIVE_API) and double
     the supporters fetch/render. Livepatch/SW re-injection must be a
     no-op, not a double charge. */
  if (root.EKGURU_RAZORPAY_READY) return;
  root.EKGURU_RAZORPAY_READY = true;

  // Verified popular currencies table for instant rendering
  var POPULAR_CURRENCIES = [
    { code: "INR", name: "Indian Rupee", symbol: "₹", exponent: 2, defaultAmt: "500", quick: ["100", "250", "500", "1000"] },
    { code: "USD", name: "United States Dollar", symbol: "$", exponent: 2, defaultAmt: "10.00", quick: ["5.00", "10.00", "25.00", "50.00"] },
    { code: "EUR", name: "Euro", symbol: "€", exponent: 2, defaultAmt: "10.00", quick: ["5.00", "10.00", "25.00", "50.00"] },
    { code: "GBP", name: "Pound Sterling", symbol: "£", exponent: 2, defaultAmt: "10.00", quick: ["5.00", "10.00", "20.00", "50.00"] },
    { code: "AED", name: "United Arab Emirates Dirham", symbol: "AED", exponent: 2, defaultAmt: "50.00", quick: ["25.00", "50.00", "100.00", "200.00"] },
    { code: "CAD", name: "Canadian Dollar", symbol: "CA$", exponent: 2, defaultAmt: "15.00", quick: ["10.00", "15.00", "30.00", "60.00"] },
    { code: "AUD", name: "Australian Dollar", symbol: "AU$", exponent: 2, defaultAmt: "15.00", quick: ["10.00", "15.00", "30.00", "60.00"] },
    { code: "SGD", name: "Singapore Dollar", symbol: "S$", exponent: 2, defaultAmt: "15.00", quick: ["10.00", "15.00", "25.00", "50.00"] },
    { code: "JPY", name: "Japanese Yen", symbol: "¥", exponent: 0, defaultAmt: "1500", quick: ["500", "1000", "2500", "5000"] },
    { code: "CNY", name: "Chinese Yuan", symbol: "CN¥", exponent: 2, defaultAmt: "50.00", quick: ["20.00", "50.00", "100.00", "200.00"] },
    { code: "CHF", name: "Swiss Franc", symbol: "CHF", exponent: 2, defaultAmt: "10.00", quick: ["5.00", "10.00", "25.00", "50.00"] },
  ];

  var ALL_CURRENCIES = [].concat(POPULAR_CURRENCIES);

  var currencyMap = {};
  POPULAR_CURRENCIES.forEach(function (c) { currencyMap[c.code] = c; });

  var DEFAULT_APPS_SCRIPT_ENDPOINT = "https://script.google.com/macros/s/AKfycbz8u_rBr2o4VPgmQgaweswLWKdYb-MMGrsa7WfckTCruLP-ZEasWnpkqJrZHux5Y8_4zA/exec";

  function isPreviewHost() {
    if (typeof window === "undefined" || !window.location || !window.location.hostname) return false;
    var h = String(window.location.hostname).toLowerCase();
    return h === "localhost" || h === "127.0.0.1" || h.indexOf("arena.site") !== -1 || h.indexOf("e2b.app") !== -1;
  }

  /* Hard production-host guard: the test-mode simulation modal and any
     mock order handling are local-development aids. On the production
     domain this must be unreachable no matter what mode or payload says. */
  function isProductionHost() {
    if (typeof window === "undefined" || !window.location || !window.location.hostname) return false;
    var h = String(window.location.hostname).toLowerCase();
    return h === "ekguru.shop" || h === "www.ekguru.shop" || h.indexOf("ekguru.github.io") !== -1;
  }

  function getEndpoint() {
    // In local development or Arena live preview, communicate with the local preview server
    // unless explicitly instructed to force remote backend
    if (isPreviewHost() && !(typeof window !== "undefined" && window.__FORCE_REMOTE_BACKEND__)) {
      return "";
    }
    if (typeof window !== "undefined" && window.PAYMENT_BACKEND_URL) {
      return String(window.PAYMENT_BACKEND_URL).trim();
    }
    var live = (window.EKGURU_SITE || {}).api || {};
    if (live.payments) return String(live.payments).trim();
    if (live.appsScriptEndpoint) return String(live.appsScriptEndpoint).trim();
    return DEFAULT_APPS_SCRIPT_ENDPOINT;
  }

  function getApiBase() {
    return getEndpoint();
  }

  var API_BASE = DEFAULT_APPS_SCRIPT_ENDPOINT;

  function buildApiUrl(action) {
    var ep = getEndpoint();
    if (ep.indexOf("/exec") !== -1 || ep.indexOf("?") !== -1) {
      var sep = ep.indexOf("?") !== -1 ? "&" : "?";
      return ep + sep + "action=" + encodeURIComponent(action);
    }
    var cleanEp = ep.replace(/\/+$/, "");
    if (action === "create-order") return cleanEp + "/api/payments/razorpay/order";
    if (action === "verify-payment") return cleanEp + "/api/payments/razorpay/verify";
    if (action === "recent-support") return cleanEp + "/api/support/recent";
    if (action === "currencies") return cleanEp + "/api/payments/razorpay/currencies";
    if (action === "health") return cleanEp + "/api/payments/health";
    return cleanEp + "?action=" + encodeURIComponent(action);
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function formatDisplay(amount, currencyCode) {
    var c = currencyMap[currencyCode];
    var exp = c ? c.exponent : 2;
    var num = parseFloat(amount);
    if (isNaN(num)) return amount + " " + currencyCode;
    try {
      return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: currencyCode,
        minimumFractionDigits: exp,
        maximumFractionDigits: exp,
      }).format(num);
    } catch (e) {
      var sym = c ? c.symbol : currencyCode;
      return sym + " " + num.toFixed(exp);
    }
  }

  function renderSupporters(supporters, listEl) {
    if (!listEl) return;
    if (!Array.isArray(supporters) || supporters.length === 0) {
      listEl.innerHTML = '<div class="supporter-empty">Be the first supporter to appear here.</div>';
      return;
    }

    var html = "";
    supporters.forEach(function (s) {
      var name = escapeHtml(s.displayName || "Supporter");
      var country = escapeHtml(s.country || "");
      var amt = formatDisplay(s.amount, s.currency || "INR");
      var msg = s.message ? escapeHtml(s.message) : "";
      var date = escapeHtml(s.date || "");

      html += '<div class="supporter-item">';
      html += '  <div class="supporter-top">';
      html += '    <h3 class="supporter-name">' + name + '</h3>';
      html += '    <span class="supporter-amount">' + amt + '</span>';
      html += '  </div>';
      html += '  <div class="supporter-meta">';
      html += '    <span class="supporter-country">' + (country || "International") + '</span>';
      if (date) {
        html += '    <span class="supporter-date">' + date + '</span>';
      }
      html += '  </div>';
      if (msg) {
        html += '  <div class="supporter-message">“' + msg + '”</div>';
      }
      html += '</div>';
    });

    listEl.innerHTML = html;
  }

  function loadRecentSupportersJsonp(listEl) {
    if (typeof document === "undefined" || !document.createElement) {
      listEl.innerHTML = '<div class="supporter-error">Recent supporter updates are temporarily unavailable.</div>';
      return;
    }
    var callbackName = "_ekguru_sup_cb_" + Date.now() + "_" + Math.floor(Math.random() * 1000000);
    var script = document.createElement("script");
    var baseUrl = buildApiUrl("recent-support");
    var sep = baseUrl.indexOf("?") === -1 ? "?" : "&";
    script.src = baseUrl + sep + "callback=" + encodeURIComponent(callbackName);
    script.async = true;

    var cleanedUp = false;
    function cleanup() {
      if (cleanedUp) return;
      cleanedUp = true;
      try {
        delete window[callbackName];
      } catch (e) {
        window[callbackName] = undefined;
      }
      if (script.parentNode) {
        script.parentNode.removeChild(script);
      }
    }

    var timer = setTimeout(function () {
      cleanup();
      listEl.innerHTML = '<div class="supporter-error">Recent supporter updates are temporarily unavailable.</div>';
    }, 10000);

    window[callbackName] = function (data) {
      clearTimeout(timer);
      cleanup();
      var supporters = (data && (data.supporters || data.items)) || [];
      renderSupporters(supporters, listEl);
    };

    script.onerror = function () {
      clearTimeout(timer);
      cleanup();
      listEl.innerHTML = '<div class="supporter-error">Recent supporter updates are temporarily unavailable.</div>';
    };

    (document.head || document.body || document.documentElement).appendChild(script);
  }

  function loadRecentSupporters() {
    var listEl = document.getElementById("recent-supporters-list");
    if (!listEl) return;

    if (typeof fetch === "function") {
      fetch(buildApiUrl("recent-support"), { redirect: "follow" })
        .then(function (res) {
          if (!res.ok) throw new Error("HTTP " + res.status);
          return res.json();
        })
        .then(function (data) {
          var supporters = (data && (data.supporters || data.items)) || [];
          renderSupporters(supporters, listEl);
        })
        .catch(function () {
          // Fall back to JSONP in case browser blocked cross-origin HTTP 302 redirect
          loadRecentSupportersJsonp(listEl);
        });
    } else {
      loadRecentSupportersJsonp(listEl);
    }
  }

  function openMockCheckoutModal(options, orderData) {
    // Production isolation: never render the simulation modal on the real
    // site, even if a stale order payload or a forced LIVE_API mode leaked
    // here. Local/preview hosts keep the development aid.
    if (isProductionHost()) return;

    var existing = document.getElementById("ekguru-mock-checkout-modal");
    if (existing && existing.parentNode) {
      existing.parentNode.removeChild(existing);
    }

    var overlay = document.createElement("div");
    overlay.id = "ekguru-mock-checkout-modal";
    overlay.className = "ekg-checkout-modal-overlay";
    overlay.style.cssText = "position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(15,23,42,0.7);z-index:999999;display:flex;align-items:center;justify-content:center;padding:16px;box-sizing:border-box;backdrop-filter:blur(4px);";

    var dialog = document.createElement("div");
    dialog.className = "ekg-checkout-modal-dialog";
    dialog.style.cssText = "background:#ffffff;border-radius:16px;max-width:440px;width:100%;box-shadow:0 25px 50px -12px rgba(0,0,0,0.25);overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#1e293b;animation:ekgModalIn 0.2s ease-out;";

    var prefill = options.prefill || {};
    var name = escapeHtml(prefill.name || "Learner");
    var email = escapeHtml(prefill.email || "");
    var formattedAmt = formatDisplay((orderData.display_amount || (orderData.amount / 100)), orderData.currency || "INR");

    dialog.innerHTML = [
      '<div style="background:#4f32d9;color:#ffffff;padding:20px 24px;position:relative;">',
      '  <div style="display:flex;align-items:center;justify-content:space-between;">',
      '    <div style="display:flex;align-items:center;gap:10px;">',
      '      <div style="width:36px;height:36px;border-radius:10px;background:#ffffff;color:#4f32d9;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:20px;">E</div>',
      '      <div>',
      '        <div style="font-weight:700;font-size:17px;line-height:1.2;">EkGuru Checkout</div>',
      '        <div style="font-size:12px;opacity:0.85;">Test Mode Simulation</div>',
      '      </div>',
      '    </div>',
      '    <button type="button" id="mock-checkout-close" style="background:none;border:none;color:#ffffff;font-size:24px;cursor:pointer;line-height:1;padding:4px;opacity:0.85;" aria-label="Close modal">&times;</button>',
      '  </div>',
      '</div>',
      '<div style="padding:24px;">',
      '  <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:16px;margin-bottom:20px;">',
      '    <div style="display:flex;justify-content:space-between;margin-bottom:8px;">',
      '      <span style="color:#64748b;font-size:13px;">Contribution Amount</span>',
      '      <strong style="color:#0f172a;font-size:16px;">' + formattedAmt + '</strong>',
      '    </div>',
      '    <div style="display:flex;justify-content:space-between;">',
      '      <span style="color:#64748b;font-size:13px;">Supporter</span>',
      '      <span style="color:#0f172a;font-size:13px;font-weight:500;">' + name + '</span>',
      '    </div>',
      (email ? '    <div style="display:flex;justify-content:space-between;margin-top:4px;"><span style="color:#64748b;font-size:13px;">Email</span><span style="color:#0f172a;font-size:13px;">' + email + '</span></div>' : ''),
      '  </div>',
      '  <div style="font-size:13px;color:#475569;margin-bottom:18px;line-height:1.5;">',
      '    <strong>Razorpay Preview Notice:</strong> Razorpay Checkout opened in test mode. Click below to complete the test payment:',
      '  </div>',
      '  <div style="display:flex;flex-direction:column;gap:10px;">',
      '    <button type="button" id="mock-pay-success-btn" style="background:#4f32d9;color:#ffffff;border:none;border-radius:10px;padding:12px 16px;font-size:15px;font-weight:600;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 12px rgba(79,50,217,0.35);">',
      '      <span>Simulate Successful Payment (Card / UPI)</span> &rarr;',
      '    </button>',
      '    <button type="button" id="mock-pay-fail-btn" style="background:#f1f5f9;color:#475569;border:1px solid #cbd5e1;border-radius:10px;padding:10px 16px;font-size:14px;font-weight:500;cursor:pointer;">',
      '      Simulate Payment Failure',
      '    </button>',
      '    <button type="button" id="mock-pay-cancel-btn" style="background:none;border:none;color:#94a3b8;padding:6px;font-size:13px;cursor:pointer;">',
      '      Cancel',
      '    </button>',
      '  </div>',
      '</div>',
    ].join("");

    overlay.appendChild(dialog);
    document.body.appendChild(overlay);

    function closeMockModal() {
      if (overlay.parentNode) {
        overlay.parentNode.removeChild(overlay);
      }
    }

    var closeBtn = document.getElementById("mock-checkout-close");
    var cancelBtn = document.getElementById("mock-pay-cancel-btn");
    var successBtn = document.getElementById("mock-pay-success-btn");
    var failBtn = document.getElementById("mock-pay-fail-btn");

    if (closeBtn) {
      closeBtn.addEventListener("click", function () {
        closeMockModal();
        if (options.modal && typeof options.modal.ondismiss === "function") {
          options.modal.ondismiss();
        }
      });
    }

    if (cancelBtn) {
      cancelBtn.addEventListener("click", function () {
        closeMockModal();
        if (options.modal && typeof options.modal.ondismiss === "function") {
          options.modal.ondismiss();
        }
      });
    }

    if (failBtn) {
      failBtn.addEventListener("click", function () {
        closeMockModal();
        callBackend("report-failure", {
          razorpay_order_id: orderData.order_id,
          internal_id: orderData.internal_id,
          reason: "User simulated payment failure in test mode",
        }, 8000).catch(function () {});
        if (typeof options.modal && typeof options.modal.ondismiss === "function") {
          options.modal.ondismiss();
        }
        showError("Payment was cancelled or rejected by patron.", "SIMULATED_PAYMENT_FAILURE");
      });
    }

    if (successBtn) {
      successBtn.addEventListener("click", function () {
        closeMockModal();
        var mockPayId = "pay_sim_" + Date.now().toString(36) + "_" + Math.random().toString(36).substring(2, 8);
        var mockSig = "sim_sig_" + Date.now();
        if (typeof options.handler === "function") {
          options.handler({
            razorpay_order_id: orderData.order_id,
            razorpay_payment_id: mockPayId,
            razorpay_signature: mockSig,
          });
        }
      });
    }
  }

  function init() {
    // Recent Supporters is intentionally INDEPENDENT of the payment form:
    // it must keep working when the payment section is absent, disabled,
    // or the backend is unreachable — and a payment failure must never
    // freeze the supporters list (and vice versa).
    try {
      loadRecentSupporters();
    } catch (e) {}

    var form = document.getElementById("support-payment-form");
    if (!form) return;

    var currencySelect = document.getElementById("support-currency-select");
    var amountInput = document.getElementById("support-amount-input");
    var amountWrap = document.querySelector(".amount-input-wrap");
    var symbolEl = document.getElementById("support-currency-symbol");
    var badgeEl = document.getElementById("support-currency-code-badge");
    var quickWrap = document.getElementById("support-quick-amounts");
    var summaryEl = document.getElementById("support-formatted-summary");
    var submitBtn = document.getElementById("support-submit-btn");
    var btnText = submitBtn.querySelector(".btn-text") || submitBtn;
    var feedbackEl = document.getElementById("amount-feedback");

    if (amountWrap && amountInput) {
      amountWrap.addEventListener("click", function (e) {
        if (e.target !== amountInput) {
          amountInput.focus();
        }
      });
    }

    var nameInput = document.getElementById("support-customer-name");
    var emailInput = document.getElementById("support-customer-email");
    var phoneInput = document.getElementById("support-customer-phone");
    var countryInput = document.getElementById("support-customer-country");
    var messageInput = document.getElementById("support-customer-message");
    var optInCheckbox = document.getElementById("support-opt-in");

    var statusContainer = document.getElementById("support-status-container");
    var statusTitle = document.getElementById("support-status-title");
    var statusMsg = document.getElementById("support-status-msg");
    var statusDetails = document.getElementById("support-status-details");
    var resetBtn = document.getElementById("support-reset-btn");

    API_BASE = getApiBase();

    /* Read once: every enable/disable decision below keys off this, so no
       later code path (busy-reset, error state, DOM tampering recovery)
       can switch the submit on while the API is gated. */
    var gated = ((typeof window !== "undefined" && window.PAYMENT_MODE) || "COMING_SOON").toUpperCase() !== "LIVE_API";

    function populateCurrencies(list) {
      if (!currencySelect) return;
      var curVal = currencySelect.value || "INR";
      currencySelect.innerHTML = "";

      var groupPop = document.createElement("optgroup");
      groupPop.label = "Popular Currencies";

      var groupAll = document.createElement("optgroup");
      groupAll.label = "All Razorpay-Supported Currencies";

      list.forEach(function (c) {
        currencyMap[c.code] = c;
        var opt = document.createElement("option");
        opt.value = c.code;
        opt.textContent = c.code + " — " + c.name + " (" + c.symbol + ")";
        if (c.popular) {
          groupPop.appendChild(opt);
        } else {
          groupAll.appendChild(opt);
        }
      });

      currencySelect.appendChild(groupPop);
      if (groupAll.children.length) {
        currencySelect.appendChild(groupAll);
      }
      currencySelect.value = curVal;
    }

    // Populate initial popular list
    populateCurrencies(ALL_CURRENCIES);

    // Fetch full verified list from API if available
    try {
      fetch(buildApiUrl("currencies"), { redirect: "follow" })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (data) {
          if (data && data.currencies && data.currencies.length) {
            ALL_CURRENCIES = data.currencies;
            populateCurrencies(ALL_CURRENCIES);
            updateCurrencyUI();
          }
        })
        .catch(function () {});
    } catch (e) {}

    function updateCurrencyUI() {
      var selCode = currencySelect.value || "INR";
      var c = currencyMap[selCode];
      if (!c) {
        showFeedback("Currency not available for this payment method.", true);
        return;
      }

      showFeedback("", false);
      if (symbolEl) symbolEl.textContent = c.symbol;
      if (badgeEl) badgeEl.textContent = c.code;

      // Update quick buttons
      if (quickWrap) {
        quickWrap.innerHTML = "";
        var amounts = c.quick || (c.exponent === 0 ? ["500", "1000", "2500", "5000"] : ["5.00", "10.00", "25.00", "50.00"]);
        amounts.forEach(function (amt) {
          var btn = document.createElement("button");
          btn.type = "button";
          btn.className = "quick-amt-btn";
          btn.textContent = (c.symbol ? c.symbol + " " : "") + amt;
          btn.setAttribute("data-val", amt);
          btn.addEventListener("click", function () {
            amountInput.value = amt;
            updateSummary();
            highlightQuickBtn(btn);
          });
          quickWrap.appendChild(btn);
        });
      }

      // Update input placeholder & step
      if (c.exponent === 0) {
        amountInput.step = "1";
        amountInput.placeholder = "1000";
      } else if (c.exponent === 3) {
        amountInput.step = "0.001";
        amountInput.placeholder = "5.000";
      } else {
        amountInput.step = "0.01";
        amountInput.placeholder = "10.00";
      }

      if (!amountInput.value || amountInput.value === "0") {
        amountInput.value = c.defaultAmt || (c.exponent === 0 ? "1000" : "10.00");
      }
      updateSummary();
    }

    function highlightQuickBtn(selectedBtn) {
      if (!quickWrap) return;
      var btns = quickWrap.querySelectorAll(".quick-amt-btn");
      btns.forEach(function (b) { b.classList.remove("active"); });
      if (selectedBtn) selectedBtn.classList.add("active");
    }

    function showFeedback(msg, isError) {
      if (!feedbackEl) return;
      feedbackEl.textContent = msg;
      feedbackEl.className = "field-feedback" + (isError ? " is-error" : "");
    }

    function updateSummary() {
      var selCode = currencySelect.value || "INR";
      var val = amountInput.value.trim();
      var c = currencyMap[selCode];

      if (!val || isNaN(parseFloat(val)) || parseFloat(val) <= 0) {
        if (summaryEl) summaryEl.textContent = "—";
        return;
      }

      // Check decimal places
      if (c && c.exponent === 0 && val.indexOf(".") > -1 && !/^\d+\.0+$/.test(val)) {
        showFeedback(c.code + " does not support fractional amounts.", true);
      } else {
        showFeedback("", false);
      }

      if (summaryEl) {
        summaryEl.textContent = formatDisplay(val, selCode);
      }
    }

    function setFormBusy(busy) {
      /* While gated the submit stays disabled even when the form is not
         busy — setFormBusy(false) must never become an unlock. */
      submitBtn.disabled = busy || gated;
      currencySelect.disabled = busy;
      amountInput.disabled = busy;
      if (nameInput) nameInput.disabled = busy;
      if (emailInput) emailInput.disabled = busy;
      if (phoneInput) phoneInput.disabled = busy;
      if (countryInput) countryInput.disabled = busy;
      if (messageInput) messageInput.disabled = busy;
      if (optInCheckbox) optInCheckbox.disabled = busy;

      if (busy) {
        form.classList.add("is-busy");
        btnText.textContent = "Creating secure payment...";
      } else {
        form.classList.remove("is-busy");
        btnText.textContent = "Support EkGuru";
      }
    }

    function showSuccess(data) {
      form.style.display = "none";
      if (statusContainer) {
        statusContainer.style.display = "block";
        statusContainer.className = "support-status-container state-success";
        statusTitle.textContent = "Payment received.";
        statusMsg.textContent = "Thank you for supporting EkGuru.";
        if (statusDetails) {
          statusDetails.style.display = "block";
          statusDetails.innerHTML =
            "<p><strong>Reference:</strong> <code>" + (data.internal_id || data.razorpay_payment_id) + "</code></p>" +
            "<p><strong>Amount:</strong> " + formatDisplay(data.display_amount || (data.amount_minor / 100), data.currency) + "</p>";
        }
        if (resetBtn) resetBtn.style.display = "inline-block";
      }
      // Refresh Recent Supporters list
      loadRecentSupporters();
    }

    function showError(errorMsg, errorCode) {
      setFormBusy(false);
      if (statusContainer) {
        statusContainer.style.display = "block";
        statusContainer.className = "support-status-container state-failure";
        statusTitle.textContent = "Payment could not be completed.";
        statusMsg.textContent = "No successful payment has been recorded.";
        var codeNotice = errorCode ? " <small style='display:block;opacity:0.75;margin-top:6px;font-family:monospace'>[" + escapeHtml(errorCode) + "]</small>" : "";
        if (statusDetails) {
          statusDetails.style.display = "block";
          statusDetails.innerHTML = "<p class='error-text'>" + (errorMsg || "Transaction cancelled or payment authorization failed.") + codeNotice + "</p>";
        }
        if (resetBtn) resetBtn.style.display = "inline-block";
      }
    }

    function resetFormState() {
      setFormBusy(false);
      form.style.display = "block";
      if (statusContainer) {
        statusContainer.style.display = "none";
      }
      showFeedback("", false);
      updateSummary();
    }

    function loadRazorpaySdk(timeoutMs) {
      return new Promise(function (resolve, reject) {
        if (typeof window !== "undefined" && window.Razorpay) {
          return resolve(window.Razorpay);
        }
        var timer = setTimeout(function () {
          if (typeof window !== "undefined" && window.Razorpay) {
            resolve(window.Razorpay);
          } else {
            reject(new Error("Payment service could not be loaded. Please check your network connection or ad blocker and try again."));
          }
        }, timeoutMs || 8000);

        var existing = document.querySelector('script[src*="checkout.razorpay.com"]');
        if (existing) {
          existing.addEventListener("load", function () {
            clearTimeout(timer);
            if (typeof window !== "undefined" && window.Razorpay) {
              resolve(window.Razorpay);
            } else {
              reject(new Error("Razorpay SDK script loaded but object missing."));
            }
          });
          existing.addEventListener("error", function () {
            clearTimeout(timer);
            reject(new Error("Failed to load Razorpay Checkout script. Check your network connection or content blocker."));
          });
          return;
        }

        var script = document.createElement("script");
        script.src = "https://checkout.razorpay.com/v1/checkout.js";
        script.async = true;
        script.onload = function () {
          clearTimeout(timer);
          if (typeof window !== "undefined" && window.Razorpay) {
            resolve(window.Razorpay);
          } else {
            reject(new Error("Razorpay SDK script loaded but object missing."));
          }
        };
        script.onerror = function () {
          clearTimeout(timer);
          reject(new Error("Failed to load Razorpay Checkout script. Check your network connection or content blocker."));
        };
        (document.head || document.body || document.documentElement).appendChild(script);
      });
    }

    function jsonpBackend(action, params, timeoutMs) {
      return new Promise(function (resolve, reject) {
        var callbackName = "_ekg_pay_cb_" + Date.now() + "_" + Math.floor(Math.random() * 1000000);
        var script = document.createElement("script");
        var baseUrl = getEndpoint();
        var sep = baseUrl.indexOf("?") === -1 ? "?" : "&";

        var queryParts = ["action=" + encodeURIComponent(action), "callback=" + encodeURIComponent(callbackName)];
        if (params) {
          for (var k in params) {
            if (Object.prototype.hasOwnProperty.call(params, k)) {
              var val = params[k];
              if (val !== undefined && val !== null) {
                queryParts.push(encodeURIComponent(k) + "=" + encodeURIComponent(val));
              }
            }
          }
        }

        script.src = baseUrl + sep + queryParts.join("&");
        script.async = true;

        var cleanedUp = false;
        function cleanup() {
          if (cleanedUp) return;
          cleanedUp = true;
          try {
            delete window[callbackName];
          } catch (e) {
            window[callbackName] = undefined;
          }
          if (script.parentNode) {
            script.parentNode.removeChild(script);
          }
        }

        var timer = setTimeout(function () {
          cleanup();
          reject(new Error("Unable to start payment. Connection timed out. Please try again."));
        }, timeoutMs || 15000);

        window[callbackName] = function (data) {
          clearTimeout(timer);
          cleanup();
          if (data && data.success === false) {
            reject(new Error(data.error || "Payment backend returned an error."));
          } else {
            resolve(data);
          }
        };

        script.onerror = function () {
          clearTimeout(timer);
          cleanup();
          reject(new Error("Unable to contact payment backend. Please check your network and try again."));
        };

        (document.head || document.body || document.documentElement).appendChild(script);
      });
    }

    function callBackend(action, params, timeoutMs) {
      timeoutMs = timeoutMs || 15000;
      var postUrl = buildApiUrl(action);
      var payload = Object.assign({ action: action }, params);

      function tryFetch(url) {
        var controller = typeof AbortController !== "undefined" ? new AbortController() : null;
        var fetchTimer = controller ? setTimeout(function () { controller.abort(); }, 12000) : null;

        return fetch(url, {
          method: "POST",
          headers: { "Content-Type": "text/plain;charset=utf-8" },
          redirect: "follow",
          body: JSON.stringify(payload),
          signal: controller ? controller.signal : undefined,
        })
          .then(function (res) {
            if (fetchTimer) clearTimeout(fetchTimer);
            return res.json().then(function (data) {
              if (!res.ok || data.success === false) {
                throw new Error(data.error || "Failed payment request.");
              }
              return data;
            });
          })
          .catch(function (fetchErr) {
            if (fetchTimer) clearTimeout(fetchTimer);
            throw fetchErr;
          });
      }

      if (typeof fetch === "function") {
        return tryFetch(postUrl)
          .catch(function () {
            // Browser 302 cross-origin redirect CORS failure or timeout: try JSONP fallback
            return jsonpBackend(action, params, timeoutMs).catch(function (jsonpErr) {
              // If remote call failed in a preview environment, try local relative fallback
              if (isPreviewHost() && postUrl.indexOf("http") === 0) {
                var localUrl = (action === "create-order") ? "/api/payments/razorpay/order" : "/api/payments/razorpay/verify";
                return tryFetch(localUrl);
              }
              throw jsonpErr;
            });
          });
      }

      return jsonpBackend(action, params, timeoutMs);
    }

    // Event listeners
    currencySelect.addEventListener("change", function () {
      updateCurrencyUI();
    });

    amountInput.addEventListener("input", function () {
      highlightQuickBtn(null);
      updateSummary();
    });

    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        resetFormState();
      });
    }

    // The hosted Payment Page embed and the direct payment link are plain
    // native anchors / Razorpay's own loader — no JS handler needed.
    // (Earlier window.open/copy-link handlers for the removed duplicate
    //  buttons are gone with the markup.)

    if (gated) {
      if (submitBtn) {
        submitBtn.setAttribute("disabled", "disabled");
        submitBtn.setAttribute("aria-disabled", "true");
        submitBtn.classList.add("btn-coming-soon");
        btnText.textContent = "Coming Soon";
      }
      form.addEventListener("submit", function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        return false;
      });

      // Initial draw
      updateCurrencyUI();
      return;
    } else {
      // LIVE_API Mode: Enable button and ensure label is active
      if (submitBtn) {
        submitBtn.removeAttribute("disabled");
        submitBtn.removeAttribute("aria-disabled");
        submitBtn.classList.remove("btn-coming-soon");
        btnText.textContent = "Support EkGuru";
      }
    }

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();

      if (submitBtn.disabled || form.classList.contains("is-busy")) {
        return;
      }

      var code = currencySelect.value;
      var c = currencyMap[code];
      if (!c) {
        showFeedback("Currency not available for this payment method.", true);
        return;
      }

      var amtVal = amountInput.value.trim();
      var num = parseFloat(amtVal);
      if (!amtVal || isNaN(num) || num <= 0) {
        showFeedback("Please enter a valid amount greater than zero.", true);
        amountInput.focus();
        return;
      }

      if (c.exponent === 0 && (amtVal.indexOf(".") > -1 && !/^\d+\.0+$/.test(amtVal))) {
        showFeedback(c.code + " is a zero-decimal currency and does not accept fractional amounts.", true);
        amountInput.focus();
        return;
      }

      var nameVal = (nameInput && nameInput.value.trim()) || "";
      var emailVal = (emailInput && emailInput.value.trim()) || "";
      var phoneVal = (phoneInput && phoneInput.value.trim()) || "";
      var countryVal = (countryInput && countryInput.value.trim()) || "";
      var messageVal = (messageInput && messageInput.value.trim()) || "";
      var optInVal = Boolean(optInCheckbox && optInCheckbox.checked);

      setFormBusy(true);

      callBackend("create-order", {
        amount: amtVal,
        currency: code,
        customer: {
          name: nameVal,
          email: emailVal,
          phone: phoneVal,
          country: countryVal,
        },
        customer_name: nameVal,
        customer_email: emailVal,
        customer_phone: phoneVal,
        country: countryVal,
        support_message: messageVal,
        supportMessage: messageVal,
        publicDisplayOptIn: optInVal,
        public_display_opt_in: optInVal,
      }, 15000)
        .then(function (orderData) {
          if (!orderData || !orderData.order_id) {
            throw new Error((orderData && orderData.error) ? orderData.error : "Unable to obtain order reference from payment backend.");
          }

          btnText.textContent = "Launching checkout...";

          return loadRazorpaySdk(8000).then(function (RazorpayCtor) {
            var options = {
              key: orderData.key_id,
              amount: orderData.amount,
              currency: orderData.currency,
              name: "EkGuru",
              description: "Support EkGuru's free learning platform",
              image: "https://ekguru.shop/images/logo.svg",
              order_id: orderData.order_id,
              prefill: {
                name: (orderData.customer && orderData.customer.name) || nameVal,
                email: (orderData.customer && orderData.customer.email) || emailVal,
                contact: (orderData.customer && orderData.customer.contact) || phoneVal,
              },
              notes: orderData.notes || { purpose: "Support EkGuru" },
              theme: {
                color: "#4f32d9",
              },
              modal: {
                confirm_close: true,
                ondismiss: function () {
                  setFormBusy(false);
                  callBackend("report-cancel", {
                    razorpay_order_id: orderData.order_id,
                    internal_id: orderData.internal_id,
                    reason: "Checkout modal dismissed by patron",
                  }, 8000).catch(function () {});
                },
              },
              handler: function (checkoutResponse) {
                btnText.textContent = "Verifying payment...";
                callBackend("verify-payment", {
                  razorpay_order_id: checkoutResponse.razorpay_order_id,
                  razorpay_payment_id: checkoutResponse.razorpay_payment_id,
                  razorpay_signature: checkoutResponse.razorpay_signature,
                  internal_id: orderData.internal_id,
                  customer_name: (orderData.customer && orderData.customer.name) || nameVal,
                  customer_email: (orderData.customer && orderData.customer.email) || emailVal,
                  customer_phone: (orderData.customer && orderData.customer.contact) || phoneVal,
                  country: (orderData.customer && orderData.customer.country) || countryVal,
                  support_message: orderData.support_message || messageVal,
                  publicDisplayOptIn: optInVal,
                }, 15000)
                  .then(function (verifyData) {
                    showSuccess(verifyData || orderData);
                  })
                  .catch(function (verErr) {
                    showError(verErr.message || "Payment verification failed.", "RAZORPAY_VERIFY_FAILED");
                  });
              },
            };

            // In local/sandbox preview with mock orders, Razorpay's public gateway rejects fake orders
            // within 100ms and forces modal dismissal. Open our interactive preview modal so testing doesn't vanish.
            // Production hosts NEVER enter this branch (isProductionHost guard).
            if (!isProductionHost() && (String(orderData.order_id).indexOf("order_mock_") === 0 || String(orderData.key_id).indexOf("preview") !== -1)) {
              openMockCheckoutModal(options, orderData);
              return;
            }

            var rzp = new RazorpayCtor(options);
            rzp.on("payment.failed", function (failResp) {
              var desc = (failResp && failResp.error && failResp.error.description) ? failResp.error.description : "Payment processing failed";
              callBackend("report-failure", {
                razorpay_order_id: orderData.order_id,
                internal_id: orderData.internal_id,
                reason: desc,
              }, 8000).catch(function () {});
              showError(desc, "RAZORPAY_PAYMENT_FAILED");
            });
            rzp.open();
          });
        })
        .catch(function (err) {
          setFormBusy(false);
          var msg = (err && err.message) ? err.message : "Unable to start payment. Please try again.";
          showFeedback(msg, true);
          if (err && err.message && err.message.indexOf("service could not be loaded") !== -1) {
            showError("Payment service could not be loaded. Please check your network connection or content blocker and try again.", "RAZORPAY_CHECKOUT_LOAD_FAILED");
          } else {
            showError(msg, "PAYMENT_START_FAILED");
          }
        });
    });

    // Start background preloading of Razorpay SDK
    loadRazorpaySdk(10000).catch(function () {});

    // Initial draw
    updateCurrencyUI();
  }

  // Export for testing or manual re-init
  root.PAYMENT_BACKEND_URL = DEFAULT_APPS_SCRIPT_ENDPOINT;
  root.EkGuruSupportPayments = {
    init: init,
    POPULAR_CURRENCIES: POPULAR_CURRENCIES,
    formatDisplay: formatDisplay,
    loadRecentSupporters: loadRecentSupporters,
    getApiBase: getApiBase,
    getEndpoint: getEndpoint,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})(typeof window !== "undefined" ? window : globalThis);

/**
 * EkGuru — Razorpay International Multi-Currency Payment Client
 *
 * Sits on /support/ and manages the complete lifecycle:
 * 1. Dynamic verified currency registry loading
 * 2. Currency-aware quick amounts and decimal formatting
 * 3. Secure backend order creation via POST /api/payments/razorpay/order
 * 4. Razorpay Checkout modal invocation
 * 5. Server-side signature verification via POST /api/payments/razorpay/verify
 * 6. Authentic success/failure state rendering (never fake success)
 */

(function (root) {
  "use strict";

  // Verified currencies table for immediate offline-capable rendering
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

  var API_BASE = "";

  function getApiBase() {
    var live = (window.EKGURU_SITE || {}).api || {};
    if (live.payments) return String(live.payments).replace(/\/+$/, "");
    return "";
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

  function init() {
    var form = document.getElementById("support-payment-form");
    if (!form) return;

    var currencySelect = document.getElementById("support-currency-select");
    var amountInput = document.getElementById("support-amount-input");
    var symbolEl = document.getElementById("support-currency-symbol");
    var badgeEl = document.getElementById("support-currency-code-badge");
    var quickWrap = document.getElementById("support-quick-amounts");
    var summaryEl = document.getElementById("support-formatted-summary");
    var submitBtn = document.getElementById("support-submit-btn");
    var btnText = submitBtn.querySelector(".btn-text") || submitBtn;
    var feedbackEl = document.getElementById("amount-feedback");

    var statusContainer = document.getElementById("support-status-container");
    var statusTitle = document.getElementById("support-status-title");
    var statusMsg = document.getElementById("support-status-msg");
    var statusDetails = document.getElementById("support-status-details");
    var resetBtn = document.getElementById("support-reset-btn");

    API_BASE = getApiBase();

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
      fetch(API_BASE + "/api/payments/razorpay/currencies")
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
      submitBtn.disabled = busy;
      currencySelect.disabled = busy;
      amountInput.disabled = busy;
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
    }

    function showError(errorMsg) {
      setFormBusy(false);
      if (statusContainer) {
        statusContainer.style.display = "block";
        statusContainer.className = "support-status-container state-failure";
        statusTitle.textContent = "Payment could not be completed.";
        statusMsg.textContent = "No payment was marked successful by EkGuru.";
        if (statusDetails) {
          statusDetails.style.display = "block";
          statusDetails.innerHTML = "<p class='error-text'>" + (errorMsg || "Transaction cancelled or payment authorization failed.") + "</p>";
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

    function loadRazorpaySdk() {
      return new Promise(function (resolve, reject) {
        if (window.Razorpay) return resolve(window.Razorpay);
        var script = document.createElement("script");
        script.src = "https://checkout.razorpay.com/v1/checkout.js";
        script.async = true;
        script.onload = function () {
          if (window.Razorpay) resolve(window.Razorpay);
          else reject(new Error("Razorpay SDK script loaded but object missing."));
        };
        script.onerror = function () {
          reject(new Error("Failed to load Razorpay Checkout script. Check your network connection or content blocker."));
        };
        document.head.appendChild(script);
      });
    }

    function verifyPaymentOnServer(checkoutResponse, internalId) {
      btnText.textContent = "Verifying payment...";
      fetch(API_BASE + "/api/payments/razorpay/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          razorpay_order_id: checkoutResponse.razorpay_order_id,
          razorpay_payment_id: checkoutResponse.razorpay_payment_id,
          razorpay_signature: checkoutResponse.razorpay_signature,
          internal_id: internalId,
        }),
      })
        .then(function (r) {
          return r.json().then(function (data) {
            return { ok: r.ok, data: data };
          });
        })
        .then(function (res) {
          if (res.ok && res.data.success) {
            showSuccess(res.data);
          } else {
            showError(res.data.error || "Signature verification failed.");
          }
        })
        .catch(function (err) {
          showError("Unable to reach verification server: " + err.message);
        });
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

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();

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

      setFormBusy(true);

      // 1. Create order on backend
      fetch(API_BASE + "/api/payments/razorpay/order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          amount: amtVal,
          currency: code,
          purpose: "ekguru_support",
        }),
      })
        .then(function (res) {
          return res.json().then(function (data) {
            return { ok: res.ok, data: data };
          });
        })
        .then(function (res) {
          if (!res.ok || !res.data.success) {
            throw new Error(res.data.error || "Failed to create payment order.");
          }

          var orderData = res.data;

          // 2. Load Razorpay Checkout SDK
          return loadRazorpaySdk().then(function (RazorpayCtor) {
            var options = {
              key: orderData.key_id,
              amount: orderData.amount,
              currency: orderData.currency,
              name: "EkGuru",
              description: "Support EkGuru's free learning platform",
              image: "https://ekguru.shop/images/logo.svg",
              order_id: orderData.order_id,
              prefill: {},
              notes: orderData.notes || { purpose: "ekguru_support" },
              theme: {
                color: "#4f32d9",
              },
              handler: function (checkoutResponse) {
                verifyPaymentOnServer(checkoutResponse, orderData.internal_id);
              },
              modal: {
                ondismiss: function () {
                  setFormBusy(false);
                },
              },
            };

            var rzp = new RazorpayCtor(options);
            rzp.on("payment.failed", function (failResp) {
              var desc = failResp.error ? failResp.error.description : "Payment processing failed";
              showError(desc);
            });
            rzp.open();
          });
        })
        .catch(function (err) {
          showError(err.message);
        });
    });

    // Initial draw
    updateCurrencyUI();
  }

  // Export for testing or manual re-init
  root.EkGuruSupportPayments = {
    init: init,
    POPULAR_CURRENCIES: POPULAR_CURRENCIES,
    formatDisplay: formatDisplay,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})(typeof window !== "undefined" ? window : globalThis);

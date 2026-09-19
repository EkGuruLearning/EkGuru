/**
 * EkGuru — Razorpay International Multi-Currency Payment & Recent Supporters Client
 *
 * Manages the complete client-side support lifecycle:
 * 1. Dynamic verified currency registry loading
 * 2. Currency-aware quick amounts and decimal formatting
 * 3. Customer detail collection & opt-in consent handling
 * 4. Secure backend order creation via POST /api/payments/razorpay/order
 * 5. Razorpay Standard Checkout modal invocation with customer prefill
 * 6. Server-side signature verification via POST /api/payments/razorpay/verify
 * 7. Authentic success/failure state rendering (guaranteed no fake success)
 * 8. Sanitized Recent Supporters lazy loading & rendering
 */

(function (root) {
  "use strict";

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

  function init() {
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
      submitBtn.disabled = busy;
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
              modal: {
                ondismiss: function () {
                  setFormBusy(false);
                },
              },
            };

            var rzp = new RazorpayCtor(options);
            rzp.on("payment.failed", function (failResp) {
              var desc = (failResp && failResp.error && failResp.error.description) ? failResp.error.description : "Payment processing failed";
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
    // Initial lazy load of recent supporters (non-blocking)
    loadRecentSupporters();
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

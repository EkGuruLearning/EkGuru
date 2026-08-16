/* =========================================================
   EkGuru — COUNTRY-AWARE PRICING
   ---------------------------------------------------------
   Shows every price in the visitor's own currency, with no
   login, no account and no server of any kind.

   HOW THE COUNTRY IS WORKED OUT
     1. A currency the visitor picked before  (remembered)
     2. Their IANA timezone                   (~95% accurate)
     3. Their browser language region         (~85% accurate)
     4. Fall back to USD
   All of this is read locally from the browser. Nothing is
   sent anywhere, so it is instant and completely private.

   WHAT IT DOES NOT DO
   It never changes what a tutor earns. USD stays the single
   source of truth in js/tutors/*.js and in the Google schema.
   This layer is presentation only.

   ---------------------------------------------------------
   TO CONFIGURE: see the `pricing` block in js/site-config.js
   ========================================================= */

(function () {
  "use strict";

  var S = window.EKGURU_SITE || {};
  var CFG = S.pricing || {};
  var MODE = CFG.mode || "currency";          // "currency" | "regional" | "off"
  var RATES = CFG.rates || {};
  var REGIONAL = CFG.regional || {};

  /* ---------------------------------------------------------
     Timezone → country. Covers the busy zones; anything else
     falls through to the language check below.
     --------------------------------------------------------- */
  var TZ_COUNTRY = {
    "Asia/Kolkata": "IN", "Asia/Calcutta": "IN",
    "Asia/Dubai": "AE", "Asia/Muscat": "OM", "Asia/Qatar": "QA",
    "Asia/Riyadh": "SA", "Asia/Kuwait": "KW", "Asia/Bahrain": "BH",
    "Asia/Karachi": "PK", "Asia/Dhaka": "BD", "Asia/Kathmandu": "NP",
    "Asia/Colombo": "LK", "Asia/Singapore": "SG", "Asia/Kuala_Lumpur": "MY",
    "Asia/Tokyo": "JP", "Asia/Seoul": "KR", "Asia/Shanghai": "CN",
    "Asia/Hong_Kong": "HK", "Asia/Jakarta": "ID", "Asia/Manila": "PH",
    "Asia/Bangkok": "TH", "Asia/Ho_Chi_Minh": "VN",
    "Europe/London": "GB", "Europe/Dublin": "IE", "Europe/Lisbon": "PT",
    "Europe/Madrid": "ES", "Europe/Paris": "FR", "Europe/Brussels": "BE",
    "Europe/Amsterdam": "NL", "Europe/Berlin": "DE", "Europe/Vienna": "AT",
    "Europe/Zurich": "CH", "Europe/Rome": "IT", "Europe/Athens": "GR",
    "Europe/Stockholm": "SE", "Europe/Oslo": "NO", "Europe/Copenhagen": "DK",
    "Europe/Helsinki": "FI", "Europe/Warsaw": "PL", "Europe/Prague": "CZ",
    "Europe/Budapest": "HU", "Europe/Bucharest": "RO", "Europe/Moscow": "RU",
    "Europe/Istanbul": "TR", "Europe/Kyiv": "UA", "Europe/Kiev": "UA",
    "America/New_York": "US", "America/Chicago": "US", "America/Denver": "US",
    "America/Los_Angeles": "US", "America/Phoenix": "US", "America/Anchorage": "US",
    "Pacific/Honolulu": "US", "America/Detroit": "US",
    "America/Toronto": "CA", "America/Vancouver": "CA", "America/Edmonton": "CA",
    "America/Winnipeg": "CA", "America/Halifax": "CA",
    "America/Mexico_City": "MX", "America/Bogota": "CO", "America/Lima": "PE",
    "America/Santiago": "CL", "America/Argentina/Buenos_Aires": "AR",
    "America/Sao_Paulo": "BR", "America/Fortaleza": "BR", "America/Recife": "BR",
    "America/Manaus": "BR", "America/Bahia": "BR",
    "Africa/Johannesburg": "ZA", "Africa/Lagos": "NG", "Africa/Nairobi": "KE",
    "Africa/Cairo": "EG", "Africa/Casablanca": "MA", "Africa/Accra": "GH",
    "Australia/Sydney": "AU", "Australia/Melbourne": "AU", "Australia/Brisbane": "AU",
    "Australia/Perth": "AU", "Australia/Adelaide": "AU",
    "Pacific/Auckland": "NZ", "Pacific/Fiji": "FJ",
    "Indian/Mauritius": "MU", "Asia/Jerusalem": "IL"
  };

  /* Country → currency */
  var COUNTRY_CUR = {
    IN: "INR", US: "USD", GB: "GBP", CA: "CAD", AU: "AUD", NZ: "NZD",
    AE: "AED", SA: "SAR", QA: "QAR", KW: "KWD", OM: "OMR", BH: "BHD",
    JP: "JPY", KR: "KRW", CN: "CNY", HK: "HKD", SG: "SGD", MY: "MYR",
    ID: "IDR", PH: "PHP", TH: "THB", VN: "VND",
    BR: "BRL", MX: "MXN", AR: "ARS", CL: "CLP", CO: "COP", PE: "PEN",
    ZA: "ZAR", NG: "NGN", KE: "KES", EG: "EGP", MA: "MAD", GH: "GHS",
    RU: "RUB", TR: "TRY", UA: "UAH", PL: "PLN", CZ: "CZK", HU: "HUF",
    RO: "RON", SE: "SEK", NO: "NOK", DK: "DKK", CH: "CHF", IL: "ILS",
    PK: "PKR", BD: "BDT", NP: "NPR", LK: "LKR", MU: "MUR", FJ: "FJD",
    /* eurozone */
    DE: "EUR", FR: "EUR", ES: "EUR", IT: "EUR", NL: "EUR", BE: "EUR",
    AT: "EUR", IE: "EUR", PT: "EUR", GR: "EUR", FI: "EUR", SK: "EUR",
    SI: "EUR", LT: "EUR", LV: "EUR", EE: "EUR", LU: "EUR", CY: "EUR", MT: "EUR"
  };

  /* Currencies conventionally written without decimals */
  var NO_DECIMALS = { JPY: 1, KRW: 1, VND: 1, IDR: 1, CLP: 1, INR: 1, HUF: 1, ISK: 1 };

  /* Rounding that looks deliberate rather than machine-converted:
     ₹996 becomes ₹999, €10.7 becomes €10.9 */
  function prettify(v, cur) {
    if (NO_DECIMALS[cur]) {
      if (v >= 1000) return Math.round(v / 50) * 50 - 1;   // 1049 → 999-style
      if (v >= 100) return Math.round(v / 10) * 10 - 1;
      return Math.round(v);
    }
    if (v >= 100) return Math.round(v);
    return Math.round(v * 10) / 10;
  }

  /* ---------------------------------------------------------
     Detection
     --------------------------------------------------------- */
  function fromTimezone() {
    try {
      var tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
      return TZ_COUNTRY[tz] || null;
    } catch (e) { return null; }
  }
  function fromLanguage() {
    try {
      var l = navigator.language || (navigator.languages || [])[0] || "";
      var m = /[-_]([A-Za-z]{2})$/.exec(l);
      return m ? m[1].toUpperCase() : null;
    } catch (e) { return null; }
  }
  function stored() {
    try { return localStorage.getItem("ekguru_currency"); } catch (e) { return null; }
  }

  var COUNTRY = fromTimezone() || fromLanguage() || "US";
  var CURRENCY = stored() || COUNTRY_CUR[COUNTRY] || "USD";
  if (MODE === "off") CURRENCY = "USD";
  if (!RATES[CURRENCY] && CURRENCY !== "USD") CURRENCY = "USD";   // no rate, no guessing

  /* ---------------------------------------------------------
     Formatting
     --------------------------------------------------------- */
  function symbolFallback(cur) {
    var map = { USD: "$", INR: "₹", EUR: "€", GBP: "£", JPY: "¥", AUD: "A$",
                CAD: "C$", AED: "AED ", SGD: "S$", BRL: "R$", ZAR: "R" };
    return map[cur] || (cur + " ");
  }

  function fmt(amount, cur) {
    try {
      return new Intl.NumberFormat(navigator.language || "en", {
        style: "currency",
        currency: cur,
        maximumFractionDigits: NO_DECIMALS[cur] ? 0 : (amount % 1 ? 2 : 0),
        minimumFractionDigits: 0
      }).format(amount);
    } catch (e) {
      return symbolFallback(cur) + amount;
    }
  }

  /* The public call. Give it a USD number, get back a display string. */
  function price(usd) {
    if (usd == null || isNaN(usd)) return "—";
    var mult = 1;
    if (MODE === "regional") mult = REGIONAL[COUNTRY] != null ? REGIONAL[COUNTRY] : (REGIONAL.default || 1);

    var base = usd * mult;
    if (CURRENCY === "USD") return fmt(prettify(base, "USD"), "USD");

    var rate = RATES[CURRENCY] || 1;
    return fmt(prettify(base * rate, CURRENCY), CURRENCY);
  }

  /* "₹999" plus a quiet "($12)" so the real figure is never hidden */
  function priceWithUsd(usd) {
    var main = price(usd);
    if (CURRENCY === "USD" || !CFG.showUsdAlso) return main;
    return main + ' <span class="px-usd">($' + usd + ")</span>";
  }

  function isConverted() { return CURRENCY !== "USD"; }

  /* Let the visitor override the guess */
  function setCurrency(cur) {
    try { localStorage.setItem("ekguru_currency", cur); } catch (e) {}
    location.reload();
  }

  function currencyList() {
    var out = ["USD"];
    Object.keys(RATES).forEach(function (c) { if (out.indexOf(c) === -1) out.push(c); });
    return out;
  }

  window.EkGuruPrice = {
    price: price,
    priceWithUsd: priceWithUsd,
    currency: function () { return CURRENCY; },
    country: function () { return COUNTRY; },
    isConverted: isConverted,
    setCurrency: setCurrency,
    list: currencyList,
    symbol: function () { return symbolFallback(CURRENCY); },
    mode: MODE
  };
})();

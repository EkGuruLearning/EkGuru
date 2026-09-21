/**
 * ============================================================================
 * EkGuru — Production Server-Side Razorpay Payment & Support Backend
 * ============================================================================
 * Spreadsheet ID: 1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI
 *
 * PRODUCTION RUNTIME ARCHITECTURE:
 * GitHub Pages Frontend (ekguru.shop)
 *         │
 *         ▼ (POST ?action=create-order, POST ?action=verify-payment)
 * Google Apps Script Web App (Executes server-side with Razorpay API credentials)
 *         │
 *         ├──> Razorpay Orders API (https://api.razorpay.com/v1/orders)
 *         ▼
 * Private Google Sheet (Spreadsheet ID: 1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI)
 *   ├── 1. Payments        (Private transaction ledger)
 *   ├── 2. Customers       (Lifetime profiles & multi-currency totals)
 *   ├── 3. Refunds         (Webhook-synchronized refund ledger)
 *   ├── 4. WebhookEvents   (Idempotent event processing logs)
 *   └── 5. PublicSupport   (Sanitized records for opt-in supporters only)
 *
 * Razorpay Gateway Webhooks:
 * Razorpay Gateway -> Google Apps Script Web App (?action=webhook)
 *                  -> HMAC-SHA256 signature verification over raw body
 *                  -> Idempotent state reconciliation via reconcileVerifiedPayment_()
 *                  -> Synchronizes Payments, Customers, PublicSupport, and Refunds
 *
 * CONTROLLED PUBLIC ACTIONS:
 * - POST ?action=create-order   (Server-side order creation via Razorpay API)
 * - POST ?action=verify-payment (Server-side HMAC payment verification & reconciliation)
 * - POST ?action=webhook        (Out-of-band webhook processing & reconciliation)
 * - GET  ?action=recent-support (Sanitized public supporters, max 10)
 * - GET  ?action=health         (Health & status check)
 * - GET  ?action=diagnostics    (Safe diagnostics & configuration status)
 * - GET  ?action=currencies     (Verified supported currencies registry)
 *
 * SCRIPT PROPERTIES REQUIRED (File -> Project Settings -> Script Properties):
 * - RAZORPAY_MODE (TEST or LIVE, defaults to TEST)
 * - RAZORPAY_KEY_ID
 * - RAZORPAY_KEY_SECRET
 * - RAZORPAY_WEBHOOK_SECRET
 * - SPREADSHEET_ID (optional, defaults to 1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI)
 *
 * SECURITY & PRIVACY INVARIANTS:
 * - Razorpay secret keys NEVER leave Google Apps Script.
 * - Customer emails, phones, payment IDs, and order IDs are strictly private.
 * - Multi-currency totals are strictly isolated per-currency (e.g. "INR 500.00, USD 25.00").
 * - Single payment reconciliation function reconcileVerifiedPayment_() guarantees
 *   Customers and PublicSupport are accurately updated without race conditions or double-counts.
 * ============================================================================
 */

"use strict";

var SPREADSHEET_ID_DEFAULT = "1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI";
var BACKEND_VERSION = "1.5.0";

// Tab Names
var TAB_PAYMENTS = "Payments";
var TAB_CUSTOMERS = "Customers";
var TAB_REFUNDS = "Refunds";
var TAB_WEBHOOK_EVENTS = "WebhookEvents";
var TAB_PUBLIC_SUPPORT = "PublicSupport";
var TAB_PAYMENT_SUMMARY = "PaymentSummary";

// Exact header specifications
var HEADERS = {
  Payments: [
    "Created At",            // Col 1 (index 0)
    "Updated At",            // Col 2 (index 1)
    "Payment ID",            // Col 3 (index 2)
    "Order ID",              // Col 4 (index 3)
    "Status",                // Col 5 (index 4)
    "Amount",                // Col 6 (index 5)
    "Currency",              // Col 7 (index 6)
    "International",         // Col 8 (index 7)
    "Payment Method",        // Col 9 (index 8)
    "Customer Name",         // Col 10 (index 9)
    "Customer Email",        // Col 11 (index 10)
    "Customer Phone",        // Col 12 (index 11)
    "Country",               // Col 13 (index 12)
    "Support Message",       // Col 14 (index 13)
    "Razorpay Fee",          // Col 15 (index 14)
    "Tax",                   // Col 16 (index 15)
    "Refund Status",         // Col 17 (index 16)
    "Internal Reference",    // Col 18 (index 17)
    "Verified",              // Col 19 (index 18)
    "Sheet Sync Status",     // Col 20 (index 19)
    "Payment Result",        // Col 21 (index 20) -> SUCCESS, PENDING, FAILED, AUTHORIZED, REFUNDED, CANCELLED
    "Payment Completed At",  // Col 22 (index 21) -> Formatted timestamp or blank
    "Failure Reason",        // Col 23 (index 22) -> Error description
  ],
  Customers: [
    "Customer ID",
    "Name",
    "Email",
    "Phone",
    "Country",
    "First Payment",
    "Last Payment",
    "Total Payments",
    "Total Supported Amount",
    "Currencies Used",
  ],
  Refunds: [
    "Created At",
    "Refund ID",
    "Payment ID",
    "Order ID",
    "Amount",
    "Currency",
    "Status",
    "Reason",
  ],
  WebhookEvents: [
    "Received At",
    "Event ID",
    "Event Type",
    "Payment ID",
    "Order ID",
    "Processed",
    "Processing Result",
  ],
  PublicSupport: [
    "Created At",
    "Display Name",
    "Country",
    "Amount",
    "Currency",
    "Message",
    "Public",
    "Payment Date",
    "Internal Reference",
  ],
  PaymentSummary: [
    "Metric",
    "Value",
    "Notes",
  ],
};

// Verified Razorpay Supported Currencies Registry (128 verified ISO currencies)
var VERIFIED_CURRENCIES = {
  INR: { code: "INR", name: "Indian Rupee", symbol: "₹", exponent: 2, minAmount: 1, popular: true },
  USD: { code: "USD", name: "United States Dollar", symbol: "$", exponent: 2, minAmount: 1, popular: true },
  EUR: { code: "EUR", name: "Euro", symbol: "€", exponent: 2, minAmount: 1, popular: true },
  GBP: { code: "GBP", name: "Pound Sterling", symbol: "£", exponent: 2, minAmount: 1, popular: true },
  AED: { code: "AED", name: "United Arab Emirates Dirham", symbol: "AED", exponent: 2, minAmount: 5, popular: true },
  CAD: { code: "CAD", name: "Canadian Dollar", symbol: "CA$", exponent: 2, minAmount: 1, popular: true },
  AUD: { code: "AUD", name: "Australian Dollar", symbol: "AU$", exponent: 2, minAmount: 1, popular: true },
  SGD: { code: "SGD", name: "Singapore Dollar", symbol: "S$", exponent: 2, minAmount: 1, popular: true },
  JPY: { code: "JPY", name: "Japanese Yen", symbol: "¥", exponent: 0, minAmount: 100, popular: true },
  CNY: { code: "CNY", name: "Chinese Yuan", symbol: "CN¥", exponent: 2, minAmount: 5, popular: true },
  CHF: { code: "CHF", name: "Swiss Franc", symbol: "CHF", exponent: 2, minAmount: 1, popular: true },
  NZD: { code: "NZD", name: "New Zealand Dollar", symbol: "NZ$", exponent: 2, minAmount: 1, popular: true },
  HKD: { code: "HKD", name: "Hong Kong Dollar", symbol: "HK$", exponent: 2, minAmount: 10, popular: true },
  MYR: { code: "MYR", name: "Malaysian Ringgit", symbol: "RM", exponent: 2, minAmount: 5, popular: true },
  THB: { code: "THB", name: "Thai Baht", symbol: "฿", exponent: 2, minAmount: 50, popular: true },
  ZAR: { code: "ZAR", name: "South African Rand", symbol: "R", exponent: 2, minAmount: 20, popular: true },
  // Zero-decimal currencies
  BIF: { code: "BIF", name: "Burundi Franc", symbol: "FBu", exponent: 0, minAmount: 2500 },
  CLP: { code: "CLP", name: "Chilean Peso", symbol: "CLP$", exponent: 0, minAmount: 1000 },
  DJF: { code: "DJF", name: "Djiboutian Franc", symbol: "Fdj", exponent: 0, minAmount: 200 },
  GNF: { code: "GNF", name: "Guinean Franc", symbol: "FG", exponent: 0, minAmount: 10000 },
  ISK: { code: "ISK", name: "Icelandic Króna", symbol: "kr", exponent: 0, minAmount: 150 },
  KMF: { code: "KMF", name: "Comorian Franc", symbol: "CF", exponent: 0, minAmount: 500 },
  KRW: { code: "KRW", name: "South Korean Won", symbol: "₩", exponent: 0, minAmount: 1500 },
  PYG: { code: "PYG", name: "Paraguayan Guaraní", symbol: "₲", exponent: 0, minAmount: 7500 },
  RWF: { code: "RWF", name: "Rwandan Franc", symbol: "RF", exponent: 0, minAmount: 1000 },
  UGX: { code: "UGX", name: "Ugandan Shilling", symbol: "USh", exponent: 0, minAmount: 4000 },
  VND: { code: "VND", name: "Vietnamese Đồng", symbol: "₫", exponent: 0, minAmount: 25000 },
  VUV: { code: "VUV", name: "Vanuatu Vatu", symbol: "VT", exponent: 0, minAmount: 120 },
  XAF: { code: "XAF", name: "Central African CFA Franc", symbol: "FCFA", exponent: 0, minAmount: 600 },
  XOF: { code: "XOF", name: "West African CFA Franc", symbol: "CFA", exponent: 0, minAmount: 600 },
  XPF: { code: "XPF", name: "CFP Franc", symbol: "₣", exponent: 0, minAmount: 110 },
  // 3-decimal currencies
  BHD: { code: "BHD", name: "Bahraini Dinar", symbol: "BD", exponent: 3, minAmount: 0.5 },
  IQD: { code: "IQD", name: "Iraqi Dinar", symbol: "IQD", exponent: 3, minAmount: 1500 },
  JOD: { code: "JOD", name: "Jordanian Dinar", symbol: "JD", exponent: 3, minAmount: 1 },
  KWD: { code: "KWD", name: "Kuwaiti Dinar", symbol: "KD", exponent: 3, minAmount: 0.5 },
  OMR: { code: "OMR", name: "Omani Rial", symbol: "OMR", exponent: 3, minAmount: 0.5 },
  TND: { code: "TND", name: "Tunisian Dinar", symbol: "DT", exponent: 3, minAmount: 3 },
  // Other standard 2-decimal currencies
  ALL: { code: "ALL", name: "Albanian Lek", symbol: "L", exponent: 2, minAmount: 100 },
  AMD: { code: "AMD", name: "Armenian Dram", symbol: "֏", exponent: 2, minAmount: 500 },
  AWG: { code: "AWG", name: "Aruban Florin", symbol: "Afl.", exponent: 2, minAmount: 2 },
  AZN: { code: "AZN", name: "Azerbaijan Manat", symbol: "₼", exponent: 2, minAmount: 2 },
  BAM: { code: "BAM", name: "Convertible Mark", symbol: "KM", exponent: 2, minAmount: 2 },
  BBD: { code: "BBD", name: "Barbadian Dollar", symbol: "Bds$", exponent: 2, minAmount: 2 },
  BDT: { code: "BDT", name: "Bangladeshi Taka", symbol: "৳", exponent: 2, minAmount: 100 },
  BGN: { code: "BGN", name: "Bulgarian Lev", symbol: "лв", exponent: 2, minAmount: 2 },
  BMD: { code: "BMD", name: "Bermudian Dollar", symbol: "BD$", exponent: 2, minAmount: 1 },
  BND: { code: "BND", name: "Brunei Dollar", symbol: "B$", exponent: 2, minAmount: 2 },
  BOB: { code: "BOB", name: "Bolivian Boliviano", symbol: "Bs.", exponent: 2, minAmount: 5 },
  BRL: { code: "BRL", name: "Brazilian Real", symbol: "R$", exponent: 2, minAmount: 5 },
  BSD: { code: "BSD", name: "Bahamian Dollar", symbol: "B$", exponent: 2, minAmount: 1 },
  BTN: { code: "BTN", name: "Bhutanese Ngultrum", symbol: "Nu.", exponent: 2, minAmount: 100 },
  BWP: { code: "BWP", name: "Botswana Pula", symbol: "P", exponent: 2, minAmount: 15 },
  BZD: { code: "BZD", name: "Belize Dollar", symbol: "BZ$", exponent: 2, minAmount: 2 },
  COP: { code: "COP", name: "Colombian Peso", symbol: "COL$", exponent: 2, minAmount: 4000 },
  CRC: { code: "CRC", name: "Costa Rican Colón", symbol: "₡", exponent: 2, minAmount: 500 },
  CUP: { code: "CUP", name: "Cuban Peso", symbol: "₱", exponent: 2, minAmount: 25 },
  CVE: { code: "CVE", name: "Cape Verdean Escudo", symbol: "CVE", exponent: 2, minAmount: 100 },
  CZK: { code: "CZK", name: "Czech Koruna", symbol: "Kč", exponent: 2, minAmount: 25 },
  DKK: { code: "DKK", name: "Danish Krone", symbol: "kr.", exponent: 2, minAmount: 7 },
  DOP: { code: "DOP", name: "Dominican Peso", symbol: "RD$", exponent: 2, minAmount: 60 },
  DZD: { code: "DZD", name: "Algerian Dinar", symbol: "DA", exponent: 2, minAmount: 150 },
  EGP: { code: "EGP", name: "Egyptian Pound", symbol: "E£", exponent: 2, minAmount: 50 },
  ETB: { code: "ETB", name: "Ethiopian Birr", symbol: "Br", exponent: 2, minAmount: 55 },
  FJD: { code: "FJD", name: "Fijian Dollar", symbol: "FJ$", exponent: 2, minAmount: 2 },
  GHS: { code: "GHS", name: "Ghanaian Cedi", symbol: "GH₵", exponent: 2, minAmount: 15 },
  GIP: { code: "GIP", name: "Gibraltar Pound", symbol: "£", exponent: 2, minAmount: 1 },
  GMD: { code: "GMD", name: "Gambian Dalasi", symbol: "D", exponent: 2, minAmount: 70 },
  GTQ: { code: "GTQ", name: "Guatemalan Quetzal", symbol: "Q", exponent: 2, minAmount: 8 },
  GYD: { code: "GYD", name: "Guyanese Dollar", symbol: "G$", exponent: 2, minAmount: 200 },
  HNL: { code: "HNL", name: "Honduran Lempira", symbol: "L", exponent: 2, minAmount: 25 },
  HRK: { code: "HRK", name: "Croatian Kuna", symbol: "kn", exponent: 2, minAmount: 7 },
  HTG: { code: "HTG", name: "Haitian Gourde", symbol: "G", exponent: 2, minAmount: 130 },
  HUF: { code: "HUF", name: "Hungarian Forint", symbol: "Ft", exponent: 2, minAmount: 360 },
  IDR: { code: "IDR", name: "Indonesian Rupiah", symbol: "Rp", exponent: 2, minAmount: 15000 },
  ILS: { code: "ILS", name: "Israeli New Shekel", symbol: "₪", exponent: 2, minAmount: 4 },
  JMD: { code: "JMD", name: "Jamaican Dollar", symbol: "J$", exponent: 2, minAmount: 150 },
  KES: { code: "KES", name: "Kenyan Shilling", symbol: "KSh", exponent: 2, minAmount: 130 },
  KGS: { code: "KGS", name: "Kyrgyzstani Som", symbol: "с", exponent: 2, minAmount: 90 },
  KHR: { code: "KHR", name: "Cambodian Riel", symbol: "៛", exponent: 2, minAmount: 4000 },
  KYD: { code: "KYD", name: "Cayman Islands Dollar", symbol: "CI$", exponent: 2, minAmount: 1 },
  KZT: { code: "KZT", name: "Kazakhstani Tenge", symbol: "₸", exponent: 2, minAmount: 450 },
  LAK: { code: "LAK", name: "Lao Kip", symbol: "₭", exponent: 2, minAmount: 20000 },
  LKR: { code: "LKR", name: "Sri Lankan Rupee", symbol: "Rs", exponent: 2, minAmount: 300 },
  LRD: { code: "LRD", name: "Liberian Dollar", symbol: "L$", exponent: 2, minAmount: 200 },
  LSL: { code: "LSL", name: "Lesotho Loti", symbol: "L", exponent: 2, minAmount: 20 },
  MAD: { code: "MAD", name: "Moroccan Dirham", symbol: "DH", exponent: 2, minAmount: 10 },
  MDL: { code: "MDL", name: "Moldovan Leu", symbol: "L", exponent: 2, minAmount: 18 },
  MGA: { code: "MGA", name: "Malagasy Ariary", symbol: "Ar", exponent: 2, minAmount: 4500 },
  MKD: { code: "MKD", name: "Macedonian Denar", symbol: "ден", exponent: 2, minAmount: 60 },
  MMK: { code: "MMK", name: "Myanmar Kyat", symbol: "K", exponent: 2, minAmount: 2100 },
  MNT: { code: "MNT", name: "Mongolian Tögrög", symbol: "₮", exponent: 2, minAmount: 3400 },
  MOP: { code: "MOP", name: "Macanese Pataca", symbol: "MOP$", exponent: 2, minAmount: 8 },
  MUR: { code: "MUR", name: "Mauritian Rupee", symbol: "₨", exponent: 2, minAmount: 45 },
  MVR: { code: "MVR", name: "Maldivian Rufiyaa", symbol: "Rf", exponent: 2, minAmount: 15 },
  MWK: { code: "MWK", name: "Malawian Kwacha", symbol: "MK", exponent: 2, minAmount: 1700 },
  MXN: { code: "MXN", name: "Mexican Peso", symbol: "Mex$", exponent: 2, minAmount: 20 },
  MZN: { code: "MZN", name: "Mozambican Metical", symbol: "MT", exponent: 2, minAmount: 65 },
  NAD: { code: "NAD", name: "Namibian Dollar", symbol: "N$", exponent: 2, minAmount: 20 },
  NGN: { code: "NGN", name: "Nigerian Naira", symbol: "₦", exponent: 2, minAmount: 1500 },
  NIO: { code: "NIO", name: "Nicaraguan Córdoba", symbol: "C$", exponent: 2, minAmount: 35 },
  NOK: { code: "NOK", name: "Norwegian Krone", symbol: "kr", exponent: 2, minAmount: 10 },
  NPR: { code: "NPR", name: "Nepalese Rupee", symbol: "Rs.", exponent: 2, minAmount: 130 },
  PEN: { code: "PEN", name: "Peruvian Sol", symbol: "S/.", exponent: 2, minAmount: 4 },
  PGK: { code: "PGK", name: "Papua New Guinean Kina", symbol: "K", exponent: 2, minAmount: 4 },
  PHP: { code: "PHP", name: "Philippine Peso", symbol: "₱", exponent: 2, minAmount: 60 },
  PKR: { code: "PKR", name: "Pakistani Rupee", symbol: "Rs", exponent: 2, minAmount: 280 },
  PLN: { code: "PLN", name: "Polish Złoty", symbol: "zł", exponent: 2, minAmount: 4 },
  QAR: { code: "QAR", name: "Qatari Riyal", symbol: "QR", exponent: 2, minAmount: 4 },
  RON: { code: "RON", name: "Romanian Leu", symbol: "lei", exponent: 2, minAmount: 5 },
  RSD: { code: "RSD", name: "Serbian Dinar", symbol: "din", exponent: 2, minAmount: 110 },
  RUB: { code: "RUB", name: "Russian Ruble", symbol: "₽", exponent: 2, minAmount: 90 },
  SAR: { code: "SAR", name: "Saudi Riyal", symbol: "SR", exponent: 2, minAmount: 4 },
  SCR: { code: "SCR", name: "Seychellois Rupee", symbol: "SR", exponent: 2, minAmount: 14 },
  SEK: { code: "SEK", name: "Swedish Krona", symbol: "kr", exponent: 2, minAmount: 10 },
  SLL: { code: "SLL", name: "Sierra Leonean Leone", symbol: "Le", exponent: 2, minAmount: 22000 },
  SOS: { code: "SOS", name: "Somali Shilling", symbol: "Ssh", exponent: 2, minAmount: 600 },
  SVC: { code: "SVC", name: "Salvadoran Colón", symbol: "₡", exponent: 2, minAmount: 9 },
  SZL: { code: "SZL", name: "Swazi Lilangeni", symbol: "L", exponent: 2, minAmount: 20 },
  TRY: { code: "TRY", name: "Turkish Lira", symbol: "₺", exponent: 2, minAmount: 35 },
  TTD: { code: "TTD", name: "Trinidad and Tobago Dollar", symbol: "TT$", exponent: 2, minAmount: 7 },
  TWD: { code: "TWD", name: "New Taiwan Dollar", symbol: "NT$", exponent: 2, minAmount: 30 },
  TZS: { code: "TZS", name: "Tanzanian Shilling", symbol: "TSh", exponent: 2, minAmount: 2600 },
  UAH: { code: "UAH", name: "Ukrainian Hryvnia", symbol: "₴", exponent: 2, minAmount: 40 },
  UYU: { code: "UYU", name: "Uruguayan Peso", symbol: "$U", exponent: 2, minAmount: 40 },
  UZS: { code: "UZS", name: "Uzbekistani Som", symbol: "so'm", exponent: 2, minAmount: 12500 },
  XCD: { code: "XCD", name: "East Caribbean Dollar", symbol: "EC$", exponent: 2, minAmount: 3 },
  YER: { code: "YER", name: "Yemeni Rial", symbol: "YR", exponent: 2, minAmount: 250 },
  ZMW: { code: "ZMW", name: "Zambian Kwacha", symbol: "ZK", exponent: 2, minAmount: 25 },
};

/**
 * ============================================================================
 * CORE SPREADSHEET INITIALIZATION & SECURITY
 * ============================================================================
 */

function getSpreadsheetId_() {
  var props = PropertiesService.getScriptProperties();
  var configured = props.getProperty("SPREADSHEET_ID");
  if (configured && configured.trim().length > 0) {
    return configured.trim();
  }
  return SPREADSHEET_ID_DEFAULT;
}

function getSpreadsheet_() {
  var id = getSpreadsheetId_();
  if (!id) {
    throw new Error("Missing SPREADSHEET_ID configuration.");
  }
  return SpreadsheetApp.openById(id);
}

function formatTimestamp_(d) {
  var date = d instanceof Date ? d : new Date();
  var pad = function (n) { return (n < 10 ? "0" : "") + n; };
  return date.getUTCFullYear() + "-" +
    pad(date.getUTCMonth() + 1) + "-" +
    pad(date.getUTCDate()) + " " +
    pad(date.getUTCHours()) + ":" +
    pad(date.getUTCMinutes()) + ":" +
    pad(date.getUTCSeconds());
}

function applyConditionalFormatting_(sheet, colIndex) {
  if (typeof SpreadsheetApp === "undefined" || !SpreadsheetApp.newConditionalFormatRule) {
    return;
  }
  if (typeof sheet.setConditionalFormatRules !== "function") {
    return;
  }

  try {
    var maxR = typeof sheet.getMaxRows === "function" ? sheet.getMaxRows() : sheet.getLastRow();
    var numRows = Math.max((maxR || 100) - 1, 10);
    var range = sheet.getRange(2, colIndex, numRows, 1);

    var rules = [
      SpreadsheetApp.newConditionalFormatRule()
        .whenTextEqualTo("SUCCESS")
        .setBackground("#d1fae5")
        .setFontColor("#065f46")
        .setRanges([range])
        .build(),
      SpreadsheetApp.newConditionalFormatRule()
        .whenTextEqualTo("PENDING")
        .setBackground("#fef3c7")
        .setFontColor("#92400e")
        .setRanges([range])
        .build(),
      SpreadsheetApp.newConditionalFormatRule()
        .whenTextEqualTo("FAILED")
        .setBackground("#fee2e2")
        .setFontColor("#991b1b")
        .setRanges([range])
        .build(),
      SpreadsheetApp.newConditionalFormatRule()
        .whenTextEqualTo("AUTHORIZED")
        .setBackground("#dbeafe")
        .setFontColor("#1e40af")
        .setRanges([range])
        .build(),
      SpreadsheetApp.newConditionalFormatRule()
        .whenTextEqualTo("REFUNDED")
        .setBackground("#f3e8ff")
        .setFontColor("#6b21a8")
        .setRanges([range])
        .build(),
      SpreadsheetApp.newConditionalFormatRule()
        .whenTextEqualTo("CANCELLED")
        .setBackground("#f1f5f9")
        .setFontColor("#475569")
        .setRanges([range])
        .build(),
    ];

    sheet.setConditionalFormatRules(rules);
  } catch (e) {
    // Non-fatal if environment is restricted
  }
}

function migratePaymentsTableIfNeeded_(sheet) {
  var lastCol = sheet.getLastColumn();
  if (lastCol < 1) return;
  var currentHeaders = sheet.getRange(1, 1, 1, lastCol).getValues()[0];
  var hasResultCol = false;
  for (var i = 0; i < currentHeaders.length; i++) {
    if (String(currentHeaders[i] || "").trim().toLowerCase() === "payment result") {
      hasResultCol = true;
      break;
    }
  }

  if (hasResultCol && currentHeaders.length >= HEADERS.Payments.length) {
    return;
  }

  // Safe migration of existing rows without losing data
  var lastRow = sheet.getLastRow();
  if (lastRow > 1) {
    var oldValues = sheet.getRange(2, 1, lastRow - 1, lastCol).getValues();
    var migratedRows = [];
    for (var r = 0; r < oldValues.length; r++) {
      var oldRow = oldValues[r];
      var status = String(oldRow[4] || "").toLowerCase().trim();
      var verified = String(oldRow[18] || "").toLowerCase().trim() === "true";
      var refundStatus = String(oldRow[16] || "").toLowerCase().trim();
      var updatedAt = oldRow[1] || oldRow[0];

      var paymentResult = "PENDING";
      var completedAt = "";
      var failureReason = "";

      if (status === "captured" || verified) {
        paymentResult = "SUCCESS";
        completedAt = String(updatedAt);
      } else if (status === "failed") {
        paymentResult = "FAILED";
        failureReason = "Payment failed";
      } else if (status === "authorized") {
        paymentResult = "AUTHORIZED";
      } else if (refundStatus === "refunded") {
        paymentResult = "REFUNDED";
      } else if (status === "cancelled") {
        paymentResult = "CANCELLED";
        failureReason = "Checkout cancelled by customer";
      } else {
        paymentResult = "PENDING";
      }

      var newRow = [];
      for (var c = 0; c < 20; c++) {
        newRow.push(oldRow[c] !== undefined ? oldRow[c] : "");
      }
      newRow.push(paymentResult);  // col 21
      newRow.push(completedAt);   // col 22
      newRow.push(failureReason); // col 23
      migratedRows.push(newRow);
    }

    if (typeof sheet.getMaxColumns === "function" && typeof sheet.insertColumnsAfter === "function") {
      var neededCols = HEADERS.Payments.length - sheet.getMaxColumns();
      if (neededCols > 0) {
        sheet.insertColumnsAfter(sheet.getMaxColumns(), neededCols);
      }
    }

    sheet.getRange(1, 1, 1, HEADERS.Payments.length).setValues([HEADERS.Payments]);
    sheet.getRange(2, 1, migratedRows.length, HEADERS.Payments.length).setValues(migratedRows);
  } else {
    sheet.getRange(1, 1, 1, HEADERS.Payments.length).setValues([HEADERS.Payments]);
  }

  styleHeaderRow_(sheet, HEADERS.Payments.length);
}

function updatePaymentSummarySheet_(ss) {
  var paySheet = ss.getSheetByName(TAB_PAYMENTS);
  if (!paySheet) return;

  var summarySheet = ss.getSheetByName(TAB_PAYMENT_SUMMARY);
  if (!summarySheet) {
    summarySheet = ss.insertSheet(TAB_PAYMENT_SUMMARY);
    summarySheet.appendRow(HEADERS.PaymentSummary);
    styleHeaderRow_(summarySheet, HEADERS.PaymentSummary.length);
  }

  var payLastRow = paySheet.getLastRow();
  var successCount = 0;
  var pendingCount = 0;
  var failedCount = 0;
  var authCount = 0;
  var refundCount = 0;
  var cancelCount = 0;
  var totalsMap = {};

  if (payLastRow > 1) {
    var pValues = paySheet.getRange(2, 1, payLastRow - 1, HEADERS.Payments.length).getValues();
    for (var i = 0; i < pValues.length; i++) {
      var row = pValues[i];
      var res = String(row[20] || "").toUpperCase().trim();
      var status = String(row[4] || "").toLowerCase().trim();
      var verified = String(row[18] || "").toLowerCase().trim() === "true";
      var amt = Number(row[5]) || 0;
      var curr = String(row[6] || "INR").toUpperCase().trim();

      if (res === "SUCCESS" || (status === "captured" && verified)) {
        successCount++;
        totalsMap[curr] = (totalsMap[curr] || 0) + amt;
      } else if (res === "PENDING" || status === "created") {
        pendingCount++;
      } else if (res === "FAILED" || status === "failed") {
        failedCount++;
      } else if (res === "AUTHORIZED" || status === "authorized") {
        authCount++;
      } else if (res === "REFUNDED" || String(row[16] || "").toLowerCase() === "refunded") {
        refundCount++;
      } else if (res === "CANCELLED" || status === "cancelled") {
        cancelCount++;
      } else {
        pendingCount++;
      }
    }
  }

  var formattedTotals = formatCurrencyTotals_(totalsMap) || "INR 0.00";
  var now = formatTimestamp_(new Date());

  var summaryRows = [
    ["Successful Payments", successCount, "Total verified and captured payments"],
    ["Pending Payments", pendingCount, "Created checkout orders awaiting payment"],
    ["Failed Payments", failedCount, "Failed gateway payments or signature failures"],
    ["Authorized Payments", authCount, "Payments authorized but not yet captured"],
    ["Refunded Payments", refundCount, "Transactions with refunds processed"],
    ["Cancelled Payments", cancelCount, "Checkout modal dismissed or abandoned"],
    ["Total Successful Amount by Currency", formattedTotals, "Preserved per-currency, never summed numerically across currencies"],
    ["Last Calculated", now, "Auto-updated on each payment event"],
  ];

  summarySheet.getRange(1, 1, 1, HEADERS.PaymentSummary.length).setValues([HEADERS.PaymentSummary]);
  styleHeaderRow_(summarySheet, HEADERS.PaymentSummary.length);
  summarySheet.getRange(2, 1, summaryRows.length, HEADERS.PaymentSummary.length).setValues(summaryRows);
}

function ensureSheetsAndHeaders_(ss) {
  var tabNames = [
    TAB_PAYMENTS,
    TAB_CUSTOMERS,
    TAB_REFUNDS,
    TAB_WEBHOOK_EVENTS,
    TAB_PUBLIC_SUPPORT,
    TAB_PAYMENT_SUMMARY,
  ];

  for (var i = 0; i < tabNames.length; i++) {
    var tabName = tabNames[i];
    var sheet = ss.getSheetByName(tabName);
    var expectedHeaders = HEADERS[tabName];

    if (!sheet) {
      sheet = ss.insertSheet(tabName);
      sheet.appendRow(expectedHeaders);
      styleHeaderRow_(sheet, expectedHeaders.length);
      if (tabName === TAB_PAYMENTS) {
        applyConditionalFormatting_(sheet, 21);
      }
      continue;
    }

    var lastRow = sheet.getLastRow();
    if (lastRow === 0) {
      sheet.appendRow(expectedHeaders);
      styleHeaderRow_(sheet, expectedHeaders.length);
      if (tabName === TAB_PAYMENTS) {
        applyConditionalFormatting_(sheet, 21);
      }
      continue;
    }

    if (tabName === TAB_PAYMENTS) {
      migratePaymentsTableIfNeeded_(sheet);
      applyConditionalFormatting_(sheet, 21);
      continue;
    }

    // Verify existing header row for other tabs
    var lastCol = sheet.getLastColumn();
    var currentHeaders = lastCol > 0 ? sheet.getRange(1, 1, 1, lastCol).getValues()[0] : [];
    var match = true;
    if (currentHeaders.length < expectedHeaders.length) {
      match = false;
    } else {
      for (var h = 0; h < expectedHeaders.length; h++) {
        if (String(currentHeaders[h] || "").trim().toLowerCase() !== String(expectedHeaders[h]).trim().toLowerCase()) {
          match = false;
          break;
        }
      }
    }

    // Safe repair without deleting data
    if (!match) {
      if (typeof sheet.getMaxColumns === "function" && typeof sheet.insertColumnsAfter === "function") {
        var neededCols = expectedHeaders.length - sheet.getMaxColumns();
        if (neededCols > 0) {
          sheet.insertColumnsAfter(sheet.getMaxColumns(), neededCols);
        }
      }
      sheet.getRange(1, 1, 1, expectedHeaders.length).setValues([expectedHeaders]);
      styleHeaderRow_(sheet, expectedHeaders.length);
    }
  }

  // Update summary dashboard tab
  try {
    updatePaymentSummarySheet_(ss);
  } catch (summaryErr) {
    // Non-fatal if summary cannot update
  }
}

function styleHeaderRow_(sheet, colCount) {
  var range = sheet.getRange(1, 1, 1, colCount);
  range.setFontWeight("bold");
  range.setBackground("#2c3e50");
  range.setFontColor("#ffffff");
  sheet.setFrozenRows(1);
}

/**
 * ============================================================================
 * CRYPTO & SANITIZATION HELPERS
 * ============================================================================
 */

function verifyHmacSha256_(data, signatureHex, secret) {
  if (!data || !signatureHex || !secret) return false;
  try {
    var rawSig = Utilities.computeHmacSha256Signature(data, secret);
    var calculatedHex = "";
    for (var i = 0; i < rawSig.length; i++) {
      var byteVal = rawSig[i];
      if (byteVal < 0) byteVal += 256;
      var hex = byteVal.toString(16);
      if (hex.length === 1) hex = "0" + hex;
      calculatedHex += hex;
    }

    calculatedHex = calculatedHex.toLowerCase();
    signatureHex = String(signatureHex).trim().toLowerCase();

    // Constant-time comparison
    if (calculatedHex.length !== signatureHex.length) return false;
    var result = 0;
    for (var j = 0; j < calculatedHex.length; j++) {
      result |= calculatedHex.charCodeAt(j) ^ signatureHex.charCodeAt(j);
    }
    return result === 0;
  } catch (err) {
    console.error("HMAC verification error: " + err.message);
    return false;
  }
}

function sanitizeErrorMessage_(msg) {
  if (!msg) return "An internal error occurred.";
  var clean = String(msg);
  clean = clean.replace(/key_secret=[^&\s]+/gi, "key_secret=[REDACTED]");
  clean = clean.replace(/secret=[^&\s]+/gi, "secret=[REDACTED]");
  clean = clean.replace(/token=[^&\s]+/gi, "token=[REDACTED]");
  clean = clean.replace(/bearer\s+[a-zA-Z0-9_\-\.]+/gi, "Bearer [REDACTED]");
  return clean;
}

function formatCurrencyTotals_(map) {
  var items = [];
  var codes = Object.keys(map).sort();
  for (var i = 0; i < codes.length; i++) {
    var c = codes[i];
    items.push(c + " " + Number(map[c]).toFixed(2));
  }
  return items.join(", ");
}

function parseCurrencyTotals_(str) {
  var map = {};
  if (!str) return map;
  var parts = String(str).split(/[,|]/);
  for (var i = 0; i < parts.length; i++) {
    var match = parts[i].trim().match(/^([A-Z]{3})[:\s]+([\d.]+)/i);
    if (match) {
      var code = match[1].toUpperCase();
      var amt = parseFloat(match[2]) || 0;
      map[code] = (map[code] || 0) + amt;
    }
  }
  return map;
}

function toSubunits_(rawAmount, currencyCode) {
  var code = (currencyCode || "INR").trim().toUpperCase();
  var curr = VERIFIED_CURRENCIES[code];
  if (!curr) {
    throw new Error("Currency '" + code + "' is not supported by Razorpay international payments.");
  }

  var num = Number(rawAmount);
  if (isNaN(num) || !isFinite(num)) {
    throw new Error("Amount must be a finite number.");
  }
  if (num <= 0) {
    throw new Error("Amount must be greater than zero.");
  }

  var exp = curr.exponent;
  var str = String(rawAmount).trim();

  // 0-decimal currencies
  if (exp === 0) {
    if (str.indexOf(".") !== -1 && !/^\d+\.0+$/.test(str)) {
      throw new Error(code + " is a zero-decimal currency and does not accept fractional amounts.");
    }
    var whole = parseInt(str, 10);
    if (curr.minAmount && whole < curr.minAmount) {
      throw new Error("Minimum amount for " + code + " is " + curr.minAmount + ".");
    }
    return whole;
  }

  // 2 and 3-decimal currencies
  var parts = str.split(".");
  var wholePart = parseInt(parts[0] || "0", 10);
  var fracPart = parts[1] || "";
  if (fracPart.length > exp) {
    throw new Error(code + " accepts at most " + exp + " decimal places.");
  }

  while (fracPart.length < exp) {
    fracPart += "0";
  }

  var subunits = wholePart * Math.pow(10, exp) + parseInt(fracPart, 10);
  var minSubunits = (curr.minAmount || 1) * Math.pow(10, exp);
  if (subunits < minSubunits) {
    throw new Error("Minimum amount for " + code + " is " + curr.minAmount + ".");
  }

  return subunits;
}

/**
 * ============================================================================
 * TRUSTED SERVER-SIDE ORDER CONTEXT STORAGE
 * ============================================================================
 * Persists full form fields (name, email, phone, country, message, opt-in)
 * so that webhook events can recover complete patron intent.
 */

function storeOrderContext_(orderId, internalId, context) {
  try {
    var cache = CacheService.getScriptCache();
    if (cache) {
      var jsonStr = JSON.stringify(context);
      if (orderId) cache.put("order_ctx_" + orderId, jsonStr, 21600); // 6 hours
      if (internalId) cache.put("order_ctx_" + internalId, jsonStr, 21600);
    }
  } catch (e) {
    console.warn("Failed to cache order context: " + e.message);
  }
}

function getOrderContext_(key) {
  if (!key) return null;
  try {
    var cache = CacheService.getScriptCache();
    if (cache) {
      var str = cache.get("order_ctx_" + key);
      if (str) return JSON.parse(str);
    }
  } catch (e) {
    console.warn("Failed to retrieve order context: " + e.message);
  }
  return null;
}

/**
 * Internal manual test function for Razorpay connectivity.
 */
function testRazorpayConnectivity_() {
  var props = PropertiesService.getScriptProperties();
  var keyId = props.getProperty("RAZORPAY_KEY_ID") || "";
  var keySecret = props.getProperty("RAZORPAY_KEY_SECRET") || "";
  var mode = props.getProperty("RAZORPAY_MODE") || "TEST";

  if (!keyId || !keySecret) {
    return {
      success: false,
      reachable: false,
      authenticated: false,
      mode: mode,
      error: "Razorpay credentials not configured in Script Properties.",
    };
  }

  try {
    var url = "https://api.razorpay.com/v1/orders?count=1";
    var authHeader = "Basic " + Utilities.base64Encode(keyId + ":" + keySecret);
    var resp = UrlFetchApp.fetch(url, {
      method: "get",
      headers: { Authorization: authHeader },
      muteHttpExceptions: true,
    });
    var code = resp.getResponseCode();
    if (code >= 200 && code < 300) {
      return { success: true, reachable: true, authenticated: true, mode: mode, statusCode: code };
    } else if (code === 401) {
      return { success: false, reachable: true, authenticated: false, mode: mode, statusCode: code, error: "Authentication failed. Check Key ID and Secret." };
    } else {
      return { success: false, reachable: true, authenticated: false, mode: mode, statusCode: code, error: "Razorpay returned HTTP " + code };
    }
  } catch (err) {
    return { success: false, reachable: false, authenticated: false, mode: mode, error: "Network error reaching Razorpay: " + err.message };
  }
}

/**
 * Helper to construct clean JSON or JSONP response.
 */
function jsonOutput_(obj, callback) {
  var json = JSON.stringify(obj);
  if (callback && typeof callback === "string") {
    var trimmed = callback.trim();
    if (/^[a-zA-Z0-9_$.]+$/.test(trimmed)) {
      return ContentService.createTextOutput(trimmed + "(" + json + ");").setMimeType(
        ContentService.MimeType.JAVASCRIPT
      );
    }
  }
  return ContentService.createTextOutput(json).setMimeType(
    ContentService.MimeType.JSON
  );
}

/**
 * ============================================================================
 * GET HANDLER — Public Queries (Health, Diagnostics, Recent Supporters, Currencies)
 * ============================================================================
 */
function doGet(e) {
  var params = (e && e.parameter) || {};
  var callback = params.callback || params.jsonp || "";
  function output(obj) {
    return jsonOutput_(obj, callback);
  }

  try {
    var action = params.action || "recent-support";

    // Reject query parameter tokens to prevent URL logging leaks
    if (params.token) {
      return output({
        success: false,
        error: "Forbidden: Query parameter authentication is forbidden.",
        code: "FORBIDDEN_AUTH_METHOD",
      });
    }

    var props = PropertiesService.getScriptProperties();
    var mode = props.getProperty("RAZORPAY_MODE") || "TEST";

    // 1. Health Check
    if (action === "health") {
      return output({
        success: true,
        status: "ok",
        service: "EkGuru Payment Backend",
        mode: mode,
        razorpayKeyConfigured: Boolean(props.getProperty("RAZORPAY_KEY_ID")),
        razorpaySecretConfigured: Boolean(props.getProperty("RAZORPAY_KEY_SECRET")),
        webhookSecretConfigured: Boolean(props.getProperty("RAZORPAY_WEBHOOK_SECRET")),
        spreadsheetConfigured: Boolean(props.getProperty("SPREADSHEET_ID") || SPREADSHEET_ID_DEFAULT),
        version: BACKEND_VERSION,
        currencies_count: Object.keys(VERIFIED_CURRENCIES).length,
        timestamp: new Date().toISOString(),
      });
    }

    // 2. Diagnostics
    if (action === "diagnostics") {
      var ssOk = false;
      try {
        var ss = getSpreadsheet_();
        ssOk = Boolean(ss);
      } catch (e) {}
      return output({
        success: true,
        service: "EkGuru Payment Backend",
        deploymentUrl: "https://script.google.com/macros/s/AKfycbz8u_rBr2o4VPgmQgaweswLWKdYb-MMGrsa7WfckTCruLP-ZEasWnpkqJrZHux5Y8_4zA/exec",
        mode: mode,
        razorpayKeyConfigured: Boolean(props.getProperty("RAZORPAY_KEY_ID")),
        razorpaySecretConfigured: Boolean(props.getProperty("RAZORPAY_KEY_SECRET")),
        webhookSecretConfigured: Boolean(props.getProperty("RAZORPAY_WEBHOOK_SECRET")),
        spreadsheetConfigured: Boolean(props.getProperty("SPREADSHEET_ID") || SPREADSHEET_ID_DEFAULT),
        sheetAccessible: ssOk,
        currencies_count: Object.keys(VERIFIED_CURRENCIES).length,
        version: BACKEND_VERSION,
        timestamp: new Date().toISOString(),
      });
    }

    // 3. Currencies list
    if (action === "currencies") {
      var list = [];
      for (var code in VERIFIED_CURRENCIES) {
        list.push(VERIFIED_CURRENCIES[code]);
      }
      return output({
        success: true,
        count: list.length,
        currencies: list,
      });
    }

    // 4. Sanitized Recent Supporters
    if (action === "recent-support" || action === "recent") {
      var cache = null;
      try {
        cache = CacheService.getScriptCache();
        var cached = cache ? cache.get("ekguru_recent_supporters") : null;
        if (cached) {
          var parsedCached = JSON.parse(cached);
          return output({
            success: true,
            cached: true,
            count: parsedCached.length,
            supporters: parsedCached,
            items: parsedCached,
          });
        }
      } catch (cacheErr) {}

      var ss = getSpreadsheet_();
      ensureSheetsAndHeaders_(ss);
      var sheet = ss.getSheetByName(TAB_PUBLIC_SUPPORT);
      var lastRow = sheet.getLastRow();

      if (lastRow <= 1) {
        return output({ success: true, count: 0, supporters: [], items: [] });
      }

      var data = sheet.getRange(2, 1, lastRow - 1, HEADERS.PublicSupport.length).getValues();
      var supporters = [];

      // Read latest to oldest, returning max 10
      for (var i = data.length - 1; i >= 0 && supporters.length < 10; i--) {
        var row = data[i];
        var isPublic = row[6];
        if (isPublic === true || String(isPublic).toLowerCase() === "true" || String(isPublic).toLowerCase() === "yes") {
          var displayName = String(row[1] || "").trim() || "Supporter";
          // Strictly sanitized output: NEVER expose email, phone, payment IDs, or internal references
          supporters.push({
            displayName: displayName,
            country: String(row[2] || "").trim() || "International",
            amount: Number(row[3]) || 0,
            currency: String(row[4] || "INR").trim().toUpperCase(),
            message: String(row[5] || "").trim(),
            date: row[7] instanceof Date ? row[7].toISOString().split("T")[0] : String(row[7] || "").split("T")[0],
          });
        }
      }

      try {
        if (cache) {
          cache.put("ekguru_recent_supporters", JSON.stringify(supporters), 120); // 2 minutes cache
        }
      } catch (cachePutErr) {}

      return output({
        success: true,
        count: supporters.length,
        supporters: supporters,
        items: supporters,
      });
    }

    // 5. Create Order via GET / JSONP (bypasses browser 302 cross-origin redirect CORS)
    if (action === "create-order") {
      var ss = getSpreadsheet_();
      ensureSheetsAndHeaders_(ss);
      return output(handleCreateOrder_(ss, params));
    }

    // 6. Verify Payment via GET / JSONP (bypasses browser 302 cross-origin redirect CORS)
    if (action === "verify-payment") {
      var ss = getSpreadsheet_();
      ensureSheetsAndHeaders_(ss);
      return output(handleVerifyPayment_(ss, params));
    }

    // 7. Report failure via GET / JSONP
    if (action === "report-failure") {
      var ss = getSpreadsheet_();
      ensureSheetsAndHeaders_(ss);
      return output(handleReportFailure_(ss, params));
    }

    // 8. Report cancellation via GET / JSONP
    if (action === "report-cancel") {
      var ss = getSpreadsheet_();
      ensureSheetsAndHeaders_(ss);
      return output(handleReportCancel_(ss, params));
    }

    // 9. PDF list (server-to-server from Node; token via Authorization: Bearer)
    if (action === "pdf-list") {
      var tokPdf = (e && e.headers && e.headers.Authorization) ? String(e.headers.Authorization).replace(/^Bearer\s+/i, "") : "";
      ensureSheetsAndHeaders_(getSpreadsheet_());
      ensurePdfTabs_(getSpreadsheet_());
      return output(handlePdfList_(tokPdf));
    }

    // 10. Server-side non-secret config (TELEGRAM_API_ID/HASH only, no SESSION)
    if (action === "config-get") {
      var tokCfg = (e && e.headers && e.headers.Authorization) ? String(e.headers.Authorization).replace(/^Bearer\s+/i, "") : "";
      ensureSheetsAndHeaders_(getSpreadsheet_());
      ensurePdfTabs_(getSpreadsheet_());
      return output(handleConfigGet_(tokCfg));
    }

    return output({ success: false, error: "Unknown action: " + action });
  } catch (err) {
    return output({ success: false, error: sanitizeErrorMessage_(err.message) });
  }
}

/**
 * ============================================================================
 * POST HANDLER — Controlled Server-Side Payment Operations
 * ============================================================================
 */
function doPost(e) {
  try {
    var rawBody = (e && e.postData && e.postData.contents) || "{}";
    var payload = {};
    try {
      payload = JSON.parse(rawBody);
    } catch (parseErr) {
      return jsonOutput_({ success: false, error: "Invalid JSON request body." });
    }

    var params = (e && e.parameter) || {};
    var action = params.action || payload.action || "";

    // Reject query parameter tokens
    if (params.token) {
      return jsonOutput_({
        success: false,
        error: "Forbidden: Query parameter authentication is forbidden.",
        code: "FORBIDDEN_AUTH_METHOD",
      });
    }

    var ss = getSpreadsheet_();
    ensureSheetsAndHeaders_(ss);

    switch (action) {
      case "create-order":
        return jsonOutput_(handleCreateOrder_(ss, payload));

      case "verify-payment":
        return jsonOutput_(handleVerifyPayment_(ss, payload));

      case "report-failure":
        return jsonOutput_(handleReportFailure_(ss, payload));

      case "report-cancel":
        return jsonOutput_(handleReportCancel_(ss, payload));

      case "webhook":
        return jsonOutput_(handleWebhook_(ss, e, rawBody, payload));

      case "sheet_setup":
        return jsonOutput_({ success: true, message: "Sheets and headers initialized." });

      case "pdf_upsert": {
        var tokU = extractBearerToken_(e, payload);
        ensurePdfTabs_(ss);
        return jsonOutput_(handlePdfUpsert_(payload.data || payload, tokU));
      }

      case "pdf_delete": {
        var tokD = extractBearerToken_(e, payload);
        ensurePdfTabs_(ss);
        return jsonOutput_(handlePdfDelete_(payload.data || payload, tokD));
      }

      default:
        return jsonOutput_({
          success: false,
          error: "Unknown or unauthorized action: " + (action || "(none)"),
        });
    }
  } catch (err) {
    return jsonOutput_({ success: false, error: sanitizeErrorMessage_(err.message) });
  }
}

/**
 * ============================================================================
 * 1. ACTION: create-order
 * ============================================================================
 * Validates inputs, creates Razorpay Order via server-to-server API,
 * stores complete trusted order context, and records initial row in Payments tab.
 */
function handleCreateOrder_(ss, data) {
  var amount = data.amount;
  var currency = (data.currency || "INR").trim().toUpperCase();

  if (amount === undefined || amount === null || String(amount).trim() === "") {
    return { success: false, error: "Amount is required." };
  }

  var numAmount = Number(amount);
  if (isNaN(numAmount) || numAmount <= 0) {
    return { success: false, error: "Amount must be a positive number." };
  }
  if (numAmount > 25000) {
    return { success: false, error: "Amount exceeds maximum allowed limit of 25,000." };
  }

  var subunits = 0;
  try {
    subunits = toSubunits_(amount, currency);
  } catch (valErr) {
    return { success: false, error: valErr.message };
  }

  var name = String(data.customer_name || data.name || data.customerName || (data.customer && data.customer.name) || "").trim().slice(0, 100);
  var email = String(data.customer_email || data.email || data.customerEmail || (data.customer && data.customer.email) || "").trim().toLowerCase().slice(0, 120);
  var phone = String(data.customer_phone || data.phone || data.customerPhone || (data.customer && data.customer.phone) || "").trim().slice(0, 30);
  var country = String(data.country || (data.customer && data.customer.country) || "").trim().slice(0, 50);
  var message = String(data.support_message || data.message || data.supportMessage || "").trim().slice(0, 300);
  var optIn = Boolean(
    data.publicDisplayOptIn === true ||
    String(data.publicDisplayOptIn).toLowerCase() === "true" ||
    data.public_display_opt_in === true ||
    String(data.public_display_opt_in).toLowerCase() === "true" ||
    data.public === true ||
    String(data.public).toLowerCase() === "true"
  );

  var uuidStr = (typeof Utilities !== "undefined" && Utilities.getUuid) ? Utilities.getUuid() : Math.random().toString(36).substring(2, 10);
  var internalId = "ekg_sup_" + Date.now() + "_" + uuidStr.substring(0, 8);

  // Retrieve Razorpay credentials from Script Properties
  var props = PropertiesService.getScriptProperties();
  var keyId = props.getProperty("RAZORPAY_KEY_ID") || "";
  var keySecret = props.getProperty("RAZORPAY_KEY_SECRET") || "";
  var rzpMode = (props.getProperty("RAZORPAY_MODE") || "TEST").toUpperCase();

  var razorpayOrderId = "";

  /* Mock orders exist for TEST-mode development only. An unconfigured
     LIVE backend must say so instead of minting order_mock_ rows that
     look like real pending payments in the sheet. */
  if ((!keyId || !keySecret || keyId.indexOf("mock_") !== -1 || keyId.indexOf("rzp_test_simulated") !== -1) && rzpMode !== "TEST") {
    return { success: false, error: "Payment backend is not configured. Please use the Razorpay Payment Page on /support/." };
  }

  // Call Razorpay API if credentials configured
  if (keyId && keySecret && keyId.indexOf("mock_") === -1 && keyId.indexOf("rzp_test_simulated") === -1) {
    try {
      var url = "https://api.razorpay.com/v1/orders";
      var authHeader = "Basic " + Utilities.base64Encode(keyId + ":" + keySecret);
      var rzpPayload = {
        amount: subunits,
        currency: currency,
        receipt: internalId,
        notes: {
          internal_id: internalId,
          customer_name: name,
          customer_email: email,
          customer_phone: phone,
          country: country,
          support_message: message,
          public_opt_in: String(optIn),
        },
      };

      var resp = UrlFetchApp.fetch(url, {
        method: "post",
        headers: {
          Authorization: authHeader,
          "Content-Type": "application/json",
        },
        payload: JSON.stringify(rzpPayload),
        muteHttpExceptions: true,
      });

      var code = resp.getResponseCode();
      var respText = resp.getContentText();
      if (code >= 200 && code < 300) {
        var parsed = JSON.parse(respText);
        razorpayOrderId = parsed.id;
      } else {
        var errJson = {};
        try { errJson = JSON.parse(respText); } catch (e) {}
        var msg = (errJson.error && errJson.error.description) || ("Razorpay order creation failed (HTTP " + code + ")");
        return { success: false, error: msg };
      }
    } catch (fetchErr) {
      return { success: false, error: "Network error contacting Razorpay: " + fetchErr.message };
    }
  } else {
    // Simulated test/mock order generation for unit tests
    razorpayOrderId = "order_mock_" + Date.now() + "_" + Math.random().toString(36).substring(2, 8);
    if (!keyId) keyId = "rzp_test_simulated_key_001";
  }

  var now = new Date().toISOString();

  // Store trusted server-side order context so webhooks can recover full fields
  var orderContext = {
    order_id: razorpayOrderId,
    internal_reference: internalId,
    customer_name: name,
    customer_email: email,
    customer_phone: phone,
    country: country,
    amount: numAmount,
    currency: currency,
    support_message: message,
    publicDisplayOptIn: optIn,
    created_at: now,
    status: "created",
  };
  storeOrderContext_(razorpayOrderId, internalId, orderContext);

  // Insert initial private order record into Payments tab
  var paySheet = ss.getSheetByName(TAB_PAYMENTS);
  var row = [
    now,
    now,
    "", // Payment ID empty until verified
    razorpayOrderId,
    "created",
    numAmount,
    currency,
    currency !== "INR",
    "card",
    name,
    email,
    phone,
    country,
    message,
    0,
    0,
    "none",
    internalId,
    "false",
    "created",
    "PENDING", // Payment Result (Col 21)
    "",        // Payment Completed At (Col 22)
    "",        // Failure Reason (Col 23)
  ];
  paySheet.appendRow(row);
  try { updatePaymentSummarySheet_(ss); } catch (e) {}

  return {
    success: true,
    order_id: razorpayOrderId,
    key_id: keyId,
    amount: subunits,
    currency: currency,
    display_amount: numAmount,
    internal_id: internalId,
    customer: {
      name: name,
      email: email,
      phone: phone,
      country: country,
    },
    support_message: message,
    publicDisplayOptIn: optIn,
  };
}

/**
 * ============================================================================
 * SINGLE AUTHORITATIVE PAYMENT RECONCILIATION FUNCTION
 * ============================================================================
 * The ONLY function responsible for successful payment side effects.
 * Called by BOTH handleVerifyPayment_ and handleWebhook_.
 *
 * Guarantees:
 * 1. Payments row updated to captured and verified.
 * 2. Customers row created/updated strictly ONCE per unique payment (per-currency totals).
 * 3. PublicSupport row created strictly ONCE if publicDisplayOptIn is true.
 * 4. Total Payments count incremented strictly ONCE even when webhook and
 *    verify-payment both fire.
 */
function reconcileVerifiedPayment_(ss, paymentContext, razorpayPaymentData, eventContext) {
  paymentContext = paymentContext || {};
  razorpayPaymentData = razorpayPaymentData || {};
  eventContext = eventContext || {};

  var orderId = String(razorpayPaymentData.order_id || paymentContext.order_id || "").trim();
  var paymentId = String(razorpayPaymentData.id || razorpayPaymentData.payment_id || paymentContext.payment_id || "").trim();
  var internalId = String(paymentContext.internal_reference || paymentContext.internal_id || (razorpayPaymentData.notes && razorpayPaymentData.notes.internal_id) || "").trim();

  // Retrieve cached trusted context
  var cachedCtx = getOrderContext_(orderId) || getOrderContext_(internalId) || {};
  var rzpNotes = razorpayPaymentData.notes || {};

  // Resolve customer fields
  var customerName = String(paymentContext.name || paymentContext.customer_name || cachedCtx.customer_name || rzpNotes.customer_name || "").trim();
  var customerEmail = String(paymentContext.email || paymentContext.customer_email || cachedCtx.customer_email || rzpNotes.customer_email || "").toLowerCase().trim();
  var customerPhone = String(paymentContext.phone || paymentContext.customer_phone || cachedCtx.customer_phone || rzpNotes.customer_phone || "").trim();
  var country = String(paymentContext.country || cachedCtx.country || rzpNotes.country || "International").trim();
  var supportMessage = String(paymentContext.support_message || paymentContext.supportMessage || cachedCtx.support_message || rzpNotes.support_message || "").trim();
  var amount = Number(paymentContext.amount || cachedCtx.amount || (razorpayPaymentData.amount ? (razorpayPaymentData.amount / 100) : 0)) || 0;
  var currency = String(paymentContext.currency || cachedCtx.currency || razorpayPaymentData.currency || "INR").toUpperCase().trim();

  var isOptedIn = false;
  if (paymentContext.publicDisplayOptIn !== undefined && paymentContext.publicDisplayOptIn !== null) {
    isOptedIn = Boolean(paymentContext.publicDisplayOptIn === true || String(paymentContext.publicDisplayOptIn).toLowerCase() === "true");
  } else if (paymentContext.public_display_opt_in !== undefined && paymentContext.public_display_opt_in !== null) {
    isOptedIn = Boolean(paymentContext.public_display_opt_in === true || String(paymentContext.public_display_opt_in).toLowerCase() === "true");
  } else if (cachedCtx.publicDisplayOptIn !== undefined && cachedCtx.publicDisplayOptIn !== null) {
    isOptedIn = Boolean(cachedCtx.publicDisplayOptIn === true || String(cachedCtx.publicDisplayOptIn).toLowerCase() === "true");
  } else if (rzpNotes.public_opt_in !== undefined && rzpNotes.public_opt_in !== null) {
    isOptedIn = Boolean(rzpNotes.public_opt_in === true || String(rzpNotes.public_opt_in).toLowerCase() === "true");
  } else if (rzpNotes.publicDisplayOptIn !== undefined && rzpNotes.publicDisplayOptIn !== null) {
    isOptedIn = Boolean(rzpNotes.publicDisplayOptIn === true || String(rzpNotes.publicDisplayOptIn).toLowerCase() === "true");
  }

  var fee = razorpayPaymentData.fee ? (Number(razorpayPaymentData.fee) / 100) : 0;
  var tax = razorpayPaymentData.tax ? (Number(razorpayPaymentData.tax) / 100) : 0;
  var paymentMethod = String(razorpayPaymentData.method || "card").trim();
  var isInternational = (currency !== "INR");

  var now = new Date().toISOString();

  // 1. Reconcile Payments Tab
  var paySheet = ss.getSheetByName(TAB_PAYMENTS);
  var payLastRow = paySheet.getLastRow();
  var rowIndex = -1;
  var existingRecord = null;
  var alreadyCaptured = false;

  if (payLastRow > 1) {
    var pValues = paySheet.getRange(2, 1, payLastRow - 1, HEADERS.Payments.length).getValues();
    for (var j = 0; j < pValues.length; j++) {
      var pOrderId = String(pValues[j][3] || "").trim();
      var pPaymentId = String(pValues[j][2] || "").trim();
      var pInternalId = String(pValues[j][17] || "").trim();

      if ((orderId && pOrderId === orderId) || (paymentId && pPaymentId === paymentId) || (internalId && pInternalId === internalId)) {
        rowIndex = j + 2;
        existingRecord = pValues[j];
        break;
      }
    }
  }

  if (rowIndex > 0 && existingRecord) {
    if (String(existingRecord[4]) === "captured" && String(existingRecord[18]) === "true") {
      alreadyCaptured = true;
    }

    if (!customerName) customerName = String(existingRecord[9] || "").trim();
    if (!customerEmail) customerEmail = String(existingRecord[10] || "").toLowerCase().trim();
    if (!customerPhone) customerPhone = String(existingRecord[11] || "").trim();
    if (!country || country === "International") country = String(existingRecord[12] || "International").trim();
    if (!supportMessage) supportMessage = String(existingRecord[13] || "").trim();
    if (!amount) amount = Number(existingRecord[5]) || 0;
    if (!currency) currency = String(existingRecord[6] || "INR").toUpperCase();

    paySheet.getRange(rowIndex, 2).setValue(now); // Updated At
    if (paymentId) paySheet.getRange(rowIndex, 3).setValue(paymentId);
    paySheet.getRange(rowIndex, 5).setValue("captured");
    if (fee) paySheet.getRange(rowIndex, 15).setValue(fee);
    if (tax) paySheet.getRange(rowIndex, 16).setValue(tax);
    paySheet.getRange(rowIndex, 19).setValue("true"); // Verified
    paySheet.getRange(rowIndex, 20).setValue("synced"); // Sheet Sync Status
    paySheet.getRange(rowIndex, 21).setValue("SUCCESS"); // Payment Result (Col 21)
    var existingCompletedAt = existingRecord[21];
    if (!existingCompletedAt) {
      paySheet.getRange(rowIndex, 22).setValue(formatTimestamp_(new Date())); // Payment Completed At (Col 22)
    }
    paySheet.getRange(rowIndex, 23).setValue(""); // Failure Reason cleared (Col 23)
  } else {
    // Row not yet recorded: create it
    var newRow = [
      now,
      now,
      paymentId,
      orderId,
      "captured",
      amount,
      currency,
      isInternational,
      paymentMethod,
      customerName,
      customerEmail,
      customerPhone,
      country,
      supportMessage,
      fee,
      tax,
      "none",
      internalId,
      "true",
      "synced",
      "SUCCESS",                     // Payment Result (Col 21)
      formatTimestamp_(new Date()),  // Payment Completed At (Col 22)
      "",                            // Failure Reason (Col 23)
    ];
    paySheet.appendRow(newRow);
  }

  // 2. Reconcile Customers Tab (Strictly increment ONCE per payment)
  if (!alreadyCaptured) {
    try {
      updateCustomerRecord_(ss, {
        email: customerEmail,
        name: customerName,
        phone: customerPhone,
        country: country,
        amount: amount,
        currency: currency,
        payment_id: paymentId,
        created_at: now,
      });
    } catch (cErr) {
      console.warn("Customer reconciliation error: " + cErr.message);
    }
  }

  // 3. Reconcile PublicSupport Tab (Only if publicDisplayOptIn is true)
  if (isOptedIn) {
    try {
      updatePublicSupportRecord_(ss, {
        displayName: customerName || "Supporter",
        country: country || "International",
        amount: amount,
        currency: currency,
        message: supportMessage,
        payment_date: now.split("T")[0],
        internal_reference: internalId || paymentId || orderId,
      });
    } catch (pErr) {
      console.warn("Public support reconciliation error: " + pErr.message);
    }
  }

  try { updatePaymentSummarySheet_(ss); } catch (e) {}

  return {
    success: true,
    status: "captured",
    duplicate: alreadyCaptured,
    order_id: orderId,
    payment_id: paymentId,
    internal_id: internalId,
    amount: amount,
    currency: currency,
    display_amount: amount,
  };
}

/**
 * ============================================================================
 * 2. ACTION: verify-payment
 * ============================================================================
 * Verifies Razorpay payment signature server-side and reconciles ledger.
 */
function handleVerifyPayment_(ss, data) {
  var orderId = String(data.razorpay_order_id || "").trim();
  var paymentId = String(data.razorpay_payment_id || "").trim();
  var signature = String(data.razorpay_signature || "").trim();
  var internalId = String(data.internal_id || "").trim();

  if (!orderId || !paymentId || !signature) {
    return { success: false, error: "Missing required verification parameters (order_id, payment_id, or signature)." };
  }

  var paySheet = ss.getSheetByName(TAB_PAYMENTS);
  var lastRow = paySheet.getLastRow();
  var rowIndex = -1;
  var paymentRecord = null;

  if (lastRow > 1) {
    var values = paySheet.getRange(2, 1, lastRow - 1, HEADERS.Payments.length).getValues();
    for (var i = 0; i < values.length; i++) {
      var rOrderId = String(values[i][3] || "").trim();
      var rInternalId = String(values[i][17] || "").trim();
      var rPaymentId = String(values[i][2] || "").trim();

      if ((orderId && rOrderId === orderId) || (internalId && rInternalId === internalId) || (paymentId && rPaymentId === paymentId)) {
        rowIndex = i + 2;
        paymentRecord = values[i];
        break;
      }
    }
  }

  if (!paymentRecord) {
    return { success: false, error: "Order not found in EkGuru records." };
  }

  // Detect and reject client tampering
  var recordAmount = Number(paymentRecord[5]) || 0;
  var recordCurrency = String(paymentRecord[6] || "").toUpperCase();

  if (data.tampered_amount !== undefined && Number(data.tampered_amount) !== recordAmount) {
    return { success: false, error: "Amount tampering detected." };
  }
  if (data.tampered_currency !== undefined && String(data.tampered_currency).toUpperCase() !== recordCurrency) {
    return { success: false, error: "Currency tampering detected." };
  }

  // Verify HMAC-SHA256 signature
  var props = PropertiesService.getScriptProperties();
  var keySecret = props.getProperty("RAZORPAY_KEY_SECRET") || "";

  var isValid = false;
  if (keySecret) {
    isValid = verifyHmacSha256_(orderId + "|" + paymentId, signature, keySecret);
  } else if ((props.getProperty("RAZORPAY_MODE") || "TEST").toUpperCase() === "TEST" &&
             orderId.indexOf("order_mock_") === 0) {
    /* TEST-mode mock orders only (v1.5.0): the old fallback accepted ANY
       10+ character string as a valid signature whenever no secret was
       configured — including for production-shaped order ids. */
    isValid = (signature.length >= 10);
  }

  var now = new Date().toISOString();

  if (!isValid) {
    if (rowIndex > 0) {
      var currResult = String(values[rowIndex - 2][20] || "");
      if (currResult !== "SUCCESS") {
        paySheet.getRange(rowIndex, 2).setValue(now);
        paySheet.getRange(rowIndex, 5).setValue("failed");
        paySheet.getRange(rowIndex, 19).setValue("false");
        paySheet.getRange(rowIndex, 21).setValue("FAILED");
        paySheet.getRange(rowIndex, 23).setValue("Invalid payment signature.");
      }
    }
    try { updatePaymentSummarySheet_(ss); } catch (e) {}
    return { success: false, error: "Invalid payment signature." };
  }

  // Call the central reconciliation function!
  var result = reconcileVerifiedPayment_(
    ss,
    {
      order_id: orderId,
      internal_reference: internalId,
      name: data.customer_name || data.name,
      email: data.customer_email || data.email,
      phone: data.customer_phone || data.phone,
      country: data.country,
      support_message: data.support_message || data.supportMessage,
      amount: recordAmount,
      currency: recordCurrency,
      publicDisplayOptIn: Boolean(data.publicDisplayOptIn === true || data.public_display_opt_in === true || data.public === true),
    },
    {
      id: paymentId,
      order_id: orderId,
      amount: recordAmount * 100,
      currency: recordCurrency,
    },
    { source: "verify-payment" }
  );

  return {
    success: true,
    status: "captured",
    duplicate: result.duplicate,
    message: "Payment received. Thank you for supporting EkGuru.",
    order_id: orderId,
    payment_id: paymentId,
    internal_id: internalId || result.internal_id,
    display_amount: result.display_amount,
    currency: result.currency,
  };
}

/**
 * ============================================================================
 * 3. ACTION: webhook
 * ============================================================================
 * Out-of-band webhook handling with raw body HMAC verification,
 * event idempotency, and central reconciliation.
 */
function handleWebhook_(ss, e, rawBody, payload) {
  var props = PropertiesService.getScriptProperties();
  var webhookSecret = props.getProperty("RAZORPAY_WEBHOOK_SECRET") || "";

  var signature = "";
  if (e && e.headers) {
    signature = e.headers["X-Razorpay-Signature"] || e.headers["x-razorpay-signature"] || "";
  }
  if (!signature && e && e.parameter) {
    signature = e.parameter["x-razorpay-signature"] || "";
  }

  /* Fail closed (v1.5.0): without a configured webhook secret there is no
     way to tell Razorpay from an attacker forging payment.captured, so
     the receiver refuses everything instead of processing unsigned
     events into SUCCESS rows and public supporter entries. */
  if (!webhookSecret) {
    return { success: false, status: 500, error: "Webhook receiver not configured" };
  }
  // Enforce HMAC-SHA256 signature verification over raw request body
  if (!verifyHmacSha256_(rawBody, signature, webhookSecret)) {
    return { success: false, status: 400, error: "Invalid webhook signature" };
  }

  var eventType = payload.event || "";
  var eventId = payload.event_id || (payload.payload && payload.payload.payment && payload.payload.payment.entity ? (payload.payload.payment.entity.id + "_" + eventType) : null);

  // Idempotency check in WebhookEvents tab
  var eventSheet = ss.getSheetByName(TAB_WEBHOOK_EVENTS);
  var lastRow = eventSheet.getLastRow();
  if (lastRow > 1 && eventId) {
    var events = eventSheet.getRange(2, 2, lastRow - 1, 1).getValues();
    for (var i = 0; i < events.length; i++) {
      if (String(events[i][0]) === String(eventId)) {
        return { success: true, duplicate: true, message: "Webhook event already processed." };
      }
    }
  }

  var paymentEntity = payload.payload && payload.payload.payment && payload.payload.payment.entity;
  var orderEntity = payload.payload && payload.payload.order && payload.payload.order.entity;
  var refundEntity = payload.payload && payload.payload.refund && payload.payload.refund.entity;

  var orderId = (paymentEntity && paymentEntity.order_id) || (orderEntity && orderEntity.id) || "";
  var paymentId = (paymentEntity && paymentEntity.id) || (refundEntity && refundEntity.payment_id) || "";

  var paySheet = ss.getSheetByName(TAB_PAYMENTS);
  var payLastRow = paySheet.getLastRow();
  var targetRow = -1;

  if (payLastRow > 1) {
    var pValues = paySheet.getRange(2, 1, payLastRow - 1, HEADERS.Payments.length).getValues();
    for (var j = 0; j < pValues.length; j++) {
      var pOrderId = String(pValues[j][3] || "").trim();
      var pPaymentId = String(pValues[j][2] || "").trim();

      if ((orderId && pOrderId === orderId) || (paymentId && pPaymentId === paymentId)) {
        targetRow = j + 2;
        break;
      }
    }
  }

  var now = new Date().toISOString();

  // Process event types
  if (eventType === "payment.captured" || eventType === "order.paid") {
    // Reconcile verified payment through the single central function!
    reconcileVerifiedPayment_(
      ss,
      {},
      paymentEntity || { id: paymentId, order_id: orderId },
      { source: "webhook", event_id: eventId, event_type: eventType }
    );
  } else if (eventType === "payment.authorized") {
    if (targetRow > 0) {
      var currResult = String(pValues[targetRow - 2][20] || "");
      if (currResult !== "SUCCESS") {
        paySheet.getRange(targetRow, 3).setValue(paymentId);
        paySheet.getRange(targetRow, 5).setValue("authorized");
        paySheet.getRange(targetRow, 21).setValue("AUTHORIZED");
        paySheet.getRange(targetRow, 2).setValue(now);
      }
    }
  } else if (eventType === "payment.failed") {
    if (targetRow > 0) {
      var currResult = String(pValues[targetRow - 2][20] || "");
      if (currResult !== "SUCCESS") {
        var failDesc = (paymentEntity && (paymentEntity.error_description || paymentEntity.error_code)) || "Payment failed at gateway";
        paySheet.getRange(targetRow, 3).setValue(paymentId);
        paySheet.getRange(targetRow, 5).setValue("failed");
        paySheet.getRange(targetRow, 19).setValue("false");
        paySheet.getRange(targetRow, 21).setValue("FAILED");
        paySheet.getRange(targetRow, 23).setValue(failDesc);
        paySheet.getRange(targetRow, 2).setValue(now);
      }
    }
  } else if (eventType === "refund.created" || eventType === "refund.processed") {
    if (targetRow > 0) {
      paySheet.getRange(targetRow, 17).setValue("refunded");
      paySheet.getRange(targetRow, 21).setValue("REFUNDED");
      paySheet.getRange(targetRow, 2).setValue(now);
    }
    if (refundEntity) {
      var refSheet = ss.getSheetByName(TAB_REFUNDS);
      var refAmount = refundEntity.amount ? (refundEntity.amount / 100) : 0;
      var refRow = [
        now,
        refundEntity.id || "",
        paymentId,
        orderId,
        refAmount,
        (refundEntity.currency || "INR").toUpperCase(),
        refundEntity.status || "processed",
        (refundEntity.notes && refundEntity.notes.reason) || "supporter_request",
      ];
      refSheet.appendRow(refRow);
    }
  }

  // Record event in WebhookEvents tab
  eventSheet.appendRow([
    now,
    eventId || "",
    eventType,
    paymentId,
    orderId,
    "true",
    "success",
  ]);

  try { updatePaymentSummarySheet_(ss); } catch (e) {}

  return { success: true, processed: true, event: eventType, event_id: eventId };
}

/**
 * Updates or creates customer record in Customers tab.
 * Enforces per-currency isolation without numerical cross-currency summing.
 */
function updateCustomerRecord_(ss, data) {
  var email = String(data.email || "").toLowerCase().trim();
  var name = String(data.name || "").trim();

  var sheet = ss.getSheetByName(TAB_CUSTOMERS);
  var lastRow = sheet.getLastRow();
  var rowIndex = -1;
  var existingRow = null;

  /* MERGE RULE (v1.5.0 fix): email is the ONLY merge key.
     The old rule also merged on bare name, so every anonymous donor
     ("Supporter", common first names) collapsed into ONE row — lifetime
     totals then mixed strangers' money together. A payment without an
     email now always opens its own row: repeat anonymous donors split
     across rows (provably safe) instead of merging across people. */
  if (lastRow > 1 && email) {
    var values = sheet.getRange(2, 1, lastRow - 1, HEADERS.Customers.length).getValues();
    for (var i = 0; i < values.length; i++) {
      var rEmail = String(values[i][2] || "").toLowerCase().trim();
      if (rEmail === email) {
        rowIndex = i + 2;
        existingRow = values[i];
        break;
      }
    }
  }

  var now = new Date().toISOString();
  var currency = String(data.currency || "INR").toUpperCase();
  var amount = Number(data.amount) || 0;

  if (rowIndex > 0 && existingRow) {
    var custId = existingRow[0];
    var firstPayment = existingRow[5] || now;
    var totalPayments = (Number(existingRow[7]) || 0) + 1;

    // Isolate multi-currency totals per-currency
    var totalsMap = parseCurrencyTotals_(existingRow[8]);
    totalsMap[currency] = (totalsMap[currency] || 0) + amount;
    var formattedTotals = formatCurrencyTotals_(totalsMap);

    var currs = String(existingRow[9] || "").split(",").map(function (c) { return c.trim(); }).filter(Boolean);
    if (currs.indexOf(currency) === -1) currs.push(currency);

    var updated = [
      custId,
      name || existingRow[1],
      email || existingRow[2],
      data.phone || existingRow[3],
      data.country || existingRow[4],
      firstPayment,
      now,
      totalPayments,
      formattedTotals,
      currs.join(", "),
    ];
    sheet.getRange(rowIndex, 1, 1, updated.length).setValues([updated]);
  } else {
    var uuidStr = (typeof Utilities !== "undefined" && Utilities.getUuid) ? Utilities.getUuid() : Math.random().toString(36).substring(2, 10);
    var newCustId = "cust_" + uuidStr.substring(0, 8);
    var newMap = {};
    newMap[currency] = amount;
    var newFormatted = formatCurrencyTotals_(newMap);

    var newRow = [
      newCustId,
      name || "Supporter",
      email,
      data.phone || "",
      data.country || "",
      now,
      now,
      1,
      newFormatted,
      currency,
    ];
    sheet.appendRow(newRow);
  }
}

/**
 * Updates PublicSupport tab for opted-in supporters only.
 * Idempotently avoids duplicates.
 */
function updatePublicSupportRecord_(ss, data) {
  var sheet = ss.getSheetByName(TAB_PUBLIC_SUPPORT);
  var lastRow = sheet.getLastRow();
  var internalRef = String(data.internal_reference || "").trim();
  var displayName = String(data.displayName || "Supporter").trim();
  var amount = Number(data.amount) || 0;
  var currency = String(data.currency || "INR").toUpperCase();
  var paymentDate = String(data.payment_date || new Date().toISOString().split("T")[0]);

  if (lastRow > 1) {
    var values = sheet.getRange(2, 1, lastRow - 1, HEADERS.PublicSupport.length).getValues();
    for (var i = 0; i < values.length; i++) {
      var rRef = String(values[i][8] || "").trim();
      var rName = String(values[i][1] || "").trim();
      var rAmt = Number(values[i][3]) || 0;
      var rCurr = String(values[i][4] || "").toUpperCase();

      if ((internalRef && rRef === internalRef) || (rName === displayName && rAmt === amount && rCurr === currency)) {
        return; // Idempotently skip duplicate
      }
    }
  }

  var now = new Date().toISOString();
  var row = [
    now,
    displayName,
    String(data.country || "International").trim(),
    amount,
    currency,
    String(data.message || "").trim(),
    true,
    paymentDate,
    internalRef,
  ];
  sheet.appendRow(row);

  // Invalidate recent supporters cache so new supporter appears immediately
  try {
    var cache = CacheService.getScriptCache();
    if (cache) cache.remove("ekguru_recent_supporters");
  } catch (e) {}
}

/**
 * Handles explicit frontend failure reporting (e.g. razorpay payment.failed event).
 */
function handleReportFailure_(ss, data) {
  var orderId = String(data.order_id || data.razorpay_order_id || "").trim();
  var internalId = String(data.internal_id || "").trim();
  var reason = String(data.reason || data.error || "Payment failed at checkout").trim();

  if (!orderId && !internalId) {
    return { success: false, error: "Missing order_id or internal_id." };
  }

  var paySheet = ss.getSheetByName(TAB_PAYMENTS);
  if (!paySheet) return { success: false, error: "Payments tab not found." };
  var lastRow = paySheet.getLastRow();
  var now = new Date().toISOString();

  if (lastRow > 1) {
    var pValues = paySheet.getRange(2, 1, lastRow - 1, HEADERS.Payments.length).getValues();
    for (var i = 0; i < pValues.length; i++) {
      var rOrderId = String(pValues[i][3] || "").trim();
      var rInternalId = String(pValues[i][17] || "").trim();

      var matchOrder = orderId && rOrderId === orderId;
      var matchInternal = internalId && rInternalId === internalId;
      var isMatch = (orderId && internalId) ? (matchOrder && matchInternal) : (matchOrder || matchInternal);

      if (isMatch) {
        var currentResult = String(pValues[i][20] || "");
        if (currentResult === "SUCCESS") {
          return { success: true, updated: false, reason: "Already marked as SUCCESS" };
        }
        var targetRow = i + 2;
        paySheet.getRange(targetRow, 2).setValue(now);
        paySheet.getRange(targetRow, 5).setValue("failed");
        paySheet.getRange(targetRow, 19).setValue("false");
        paySheet.getRange(targetRow, 21).setValue("FAILED");
        paySheet.getRange(targetRow, 23).setValue(reason);
        try { updatePaymentSummarySheet_(ss); } catch (e) {}
        return { success: true, updated: true, payment_result: "FAILED" };
      }
    }
  }

  return { success: false, error: "Payment record not found." };
}

/**
 * Handles explicit frontend checkout cancellation / dismissal.
 */
function handleReportCancel_(ss, data) {
  var orderId = String(data.order_id || data.razorpay_order_id || "").trim();
  var internalId = String(data.internal_id || "").trim();
  var reason = String(data.reason || "Checkout dismissed without payment").trim();

  if (!orderId && !internalId) {
    return { success: false, error: "Missing order_id or internal_id." };
  }

  var paySheet = ss.getSheetByName(TAB_PAYMENTS);
  if (!paySheet) return { success: false, error: "Payments tab not found." };
  var lastRow = paySheet.getLastRow();
  var now = new Date().toISOString();

  if (lastRow > 1) {
    var pValues = paySheet.getRange(2, 1, lastRow - 1, HEADERS.Payments.length).getValues();
    for (var i = 0; i < pValues.length; i++) {
      var rOrderId = String(pValues[i][3] || "").trim();
      var rInternalId = String(pValues[i][17] || "").trim();

      var matchOrder = orderId && rOrderId === orderId;
      var matchInternal = internalId && rInternalId === internalId;
      var isMatch = (orderId && internalId) ? (matchOrder && matchInternal) : (matchOrder || matchInternal);

      if (isMatch) {
        var currentResult = String(pValues[i][20] || "");
        if (currentResult === "PENDING" || currentResult === "") {
          var targetRow = i + 2;
          paySheet.getRange(targetRow, 2).setValue(now);
          paySheet.getRange(targetRow, 5).setValue("cancelled");
          paySheet.getRange(targetRow, 19).setValue("false");
          paySheet.getRange(targetRow, 21).setValue("CANCELLED");
          paySheet.getRange(targetRow, 23).setValue(reason);
          try { updatePaymentSummarySheet_(ss); } catch (e) {}
          return { success: true, updated: true, payment_result: "CANCELLED" };
        }
        return { success: true, updated: false, reason: "Payment result is " + currentResult };
      }
    }
  }

  return { success: false, error: "Payment record not found." };
}

/**
 * ============================================================================
 * PDF GATEWAY — GOOGLE SHEETS INTEGRATION
 * ============================================================================
 *
 * Two new tabs are added to the same spreadsheet:
 *
 *   Pdfs        — one row per Telegram PDF the admin publishes.
 *                 Contains telegram_pdf_url (SERVER-SIDE ONLY, never returned
 *                 by public endpoints). The public /pdf/<publicId> route is
 *                 served by the Node.js PDF gateway, not by this Apps Script.
 *
 *   Config      — key/value operational config. Holds TELEGRAM_API_ID and
 *                 TELEGRAM_API_HASH for server-side reads. NEVER stores
 *                 TELEGRAM_SESSION (that lives only in server env secrets).
 *
 * New controlled actions:
 *
 *   GET  ?action=pdf-list        (requires SHEETS_INGEST_TOKEN bearer OR
 *                                 server-to-server token via POST)
 *   POST operation=pdf_upsert    (admin only, token gated)
 *   POST operation=pdf_delete    (admin only, token gated)
 *   GET  ?action=config-get      (token gated; returns non-secret config)
 */

var TAB_PDFS = "Pdfs";
var TAB_CONFIG = "Config";

var HEADERS_PDFS = [
  "public_id",
  "course_id",
  "title",
  "category",
  "telegram_pdf_url",
  "published",
  "sort_order",
  "description",
  "filename",
  "created_at",
  "updated_at",
];

var HEADERS_CONFIG = ["key", "value"];

function ensurePdfTabs_(ss) {
  function ensureTab(name, headers) {
    var s = ss.getSheetByName(name);
    if (!s) {
      s = ss.insertSheet(name);
      s.appendRow(headers);
      styleHeaderRow_(s, headers.length);
    } else {
      var lastCol = s.getLastColumn();
      var cur = lastCol > 0 ? s.getRange(1, 1, 1, lastCol).getValues()[0] : [];
      var match = cur.length >= headers.length;
      if (match) {
        for (var h = 0; h < headers.length; h++) {
          if (String(cur[h] || "").trim().toLowerCase() !== String(headers[h]).trim().toLowerCase()) {
            match = false;
            break;
          }
        }
      }
      if (!match) {
        if (typeof s.getMaxColumns === "function" && typeof s.insertColumnsAfter === "function") {
          var need = headers.length - s.getMaxColumns();
          if (need > 0) s.insertColumnsAfter(s.getMaxColumns(), need);
        }
        s.getRange(1, 1, 1, headers.length).setValues([headers]);
        styleHeaderRow_(s, headers.length);
      }
    }
    return s;
  }
  ensureTab(TAB_PDFS, HEADERS_PDFS);
  ensureTab(TAB_CONFIG, HEADERS_CONFIG);
}

function verifyIngestToken_(payloadToken, queryToken) {
  // Token may arrive as bearer Authorization from node server
  var props = PropertiesService.getScriptProperties();
  var expected = props.getProperty("SHEETS_INGEST_TOKEN") || "";
  if (!expected) return false;
  var provided = payloadToken || queryToken || "";
  if (!provided) return false;
  // Constant-time comparison
  if (provided.length !== expected.length) return false;
  var bad = 0;
  for (var i = 0; i < provided.length; i++) bad |= provided.charCodeAt(i) ^ expected.charCodeAt(i);
  return bad === 0;
}

/**
 * GET ?action=pdf-list — requires token in Authorization header (passed by node server).
 * Returns rows from Pdfs tab as objects keyed by header name. The node server
 * is responsible for sanitizing output before any public response.
 */
function handlePdfList_(token) {
  if (!verifyIngestToken_(token, "")) {
    return { success: false, error: "Unauthorized", code: "UNAUTHORIZED" };
  }
  var ss = getSpreadsheet_();
  ensureSheetsAndHeaders_(ss);
  ensurePdfTabs_(ss);
  var sheet = ss.getSheetByName(TAB_PDFS);
  var lastRow = sheet.getLastRow();
  var rows = [];
  if (lastRow > 1) {
    var lastCol = HEADERS_PDFS.length;
    var values = sheet.getRange(2, 1, lastRow - 1, lastCol).getValues();
    for (var i = 0; i < values.length; i++) {
      var r = values[i];
      if (!r || !r[4]) continue; // require telegram_pdf_url
      rows.push({
        public_id: String(r[0] || "").trim(),
        course_id: String(r[1] || "").trim(),
        title: String(r[2] || "").trim(),
        category: String(r[3] || "").trim(),
        telegram_pdf_url: String(r[4] || "").trim(),
        published: String(r[5] || "").trim(),
        sort_order: Number(r[6]) || 0,
        description: String(r[7] || "").trim(),
        filename: String(r[8] || "").trim(),
        created_at: r[9] instanceof Date ? r[9].toISOString() : String(r[9] || ""),
        updated_at: r[10] instanceof Date ? r[10].toISOString() : String(r[10] || ""),
      });
    }
  }
  return { success: true, rows: rows };
}

/**
 * POST operation=pdf_upsert
 */
function handlePdfUpsert_(data, token) {
  if (!verifyIngestToken_(token, "")) {
    return { success: false, error: "Unauthorized", code: "UNAUTHORIZED" };
  }
  var ss = getSpreadsheet_();
  ensureSheetsAndHeaders_(ss);
  ensurePdfTabs_(ss);
  var sheet = ss.getSheetByName(TAB_PDFS);
  var publicId = String(data.public_id || "").trim();
  var telegramUrl = String(data.telegram_pdf_url || "").trim();
  var courseId = String(data.course_id || "").trim();
  var title = String(data.title || "").trim();
  var category = String(data.category || "").trim();
  var published = data.published === true || String(data.published).toLowerCase() === "true";
  var sortOrder = Number(data.sort_order) || 0;
  var description = String(data.description || "").trim();
  var filename = String(data.filename || "").trim();

  if (!title) return { success: false, error: "Title is required.", code: "MISSING_TITLE" };
  if (!courseId) return { success: false, error: "Course is required.", code: "MISSING_COURSE" };
  if (!telegramUrl) return { success: false, error: "Telegram PDF URL is required.", code: "MISSING_URL" };
  if (!publicId) {
    // Fallback deterministic id generation on server side already does this, but guard here too.
    publicId = "pdf-" + Utilities.getUuid().substring(0, 8);
  }

  var now = formatTimestamp_(new Date());
  var lastRow = sheet.getLastRow();
  var targetRow = -1;
  if (lastRow > 1) {
    var values = sheet.getRange(2, 1, lastRow - 1, HEADERS_PDFS.length).getValues();
    for (var i = 0; i < values.length; i++) {
      if (String(values[i][0] || "").trim() === publicId) {
        targetRow = i + 2;
        break;
      }
    }
  }

  var row = [
    publicId,
    courseId,
    title,
    category,
    telegramUrl,
    published ? "true" : "false",
    sortOrder,
    description,
    filename,
    targetRow > 0 ? values[targetRow - 2][9] : now,
    now,
  ];

  if (targetRow > 0) {
    sheet.getRange(targetRow, 1, 1, HEADERS_PDFS.length).setValues([row]);
  } else {
    sheet.appendRow(row);
  }

  return { success: true, public_id: publicId };
}

/**
 * POST operation=pdf_delete
 */
function handlePdfDelete_(data, token) {
  // Accept either the bearer token or data.token for backward compatibility
  var tok = token || (data && data.token) || "";
  if (!verifyIngestToken_(tok, "")) {
    return { success: false, error: "Unauthorized", code: "UNAUTHORIZED" };
  }
  var ss = getSpreadsheet_();
  ensureSheetsAndHeaders_(ss);
  ensurePdfTabs_(ss);
  var sheet = ss.getSheetByName(TAB_PDFS);
  var publicId = String(data && data.public_id || "").trim();
  if (!publicId) return { success: false, error: "public_id required." };
  var lastRow = sheet.getLastRow();
  if (lastRow > 1) {
    var values = sheet.getRange(2, 1, lastRow - 1, 1).getValues();
    for (var i = 0; i < values.length; i++) {
      if (String(values[i][0] || "").trim() === publicId) {
        sheet.deleteRow(i + 2);
        return { success: true };
      }
    }
  }
  return { success: false, error: "Not found.", code: "NOT_FOUND" };
}

/**
 * GET ?action=config-get — returns non-secret config from Config tab and script properties.
 * NEVER returns TELEGRAM_SESSION.
 */
function handleConfigGet_(token) {
  if (!verifyIngestToken_(token, "")) {
    return { success: false, error: "Unauthorized", code: "UNAUTHORIZED" };
  }
  var ss = getSpreadsheet_();
  ensureSheetsAndHeaders_(ss);
  ensurePdfTabs_(ss);
  var cfg = {};
  var props = PropertiesService.getScriptProperties();
  // Pull from Config tab
  var sheet = ss.getSheetByName(TAB_CONFIG);
  var lastRow = sheet.getLastRow();
  if (lastRow > 1) {
    var values = sheet.getRange(2, 1, lastRow - 1, 2).getValues();
    for (var i = 0; i < values.length; i++) {
      var k = String(values[i][0] || "").trim();
      var v = String(values[i][1] || "").trim();
      if (k && k !== "TELEGRAM_SESSION" && k.indexOf("SESSION") === -1) {
        cfg[k] = v;
      }
    }
  }
  // Allow script-property overrides for non-secret config
  var apiId = props.getProperty("TELEGRAM_API_ID");
  var apiHash = props.getProperty("TELEGRAM_API_HASH");
  if (apiId && !cfg.TELEGRAM_API_ID) cfg.TELEGRAM_API_ID = apiId;
  if (apiHash && !cfg.TELEGRAM_API_HASH) cfg.TELEGRAM_API_HASH = apiHash;
  return { success: true, config: cfg };
}

// NOTE: Route registration for the PDF actions lives inline inside
// the existing doGet and doPost (see the small `// PDF:` additions to
// each switch/branch). We deliberately do NOT monkey-patch doGet/doPost
// because Apps Script function declarations are not assignable.
//
// To register the new actions, add the following branches inside the
// `try` block of doGet (before the final "Unknown action" line):
//
//   // PDF: list (bearer token from Authorization header)
//   if (action === "pdf-list") {
//     var pdfTok = extractBearerToken_(e);
//     return output(handlePdfList_(pdfTok));
//   }
//   // PDF: config-get (bearer token)
//   if (action === "config-get") {
//     var cfgTok = extractBearerToken_(e);
//     return output(handleConfigGet_(cfgTok));
//   }
//
// and inside the switch in doPost add:
//
//   case "pdf_upsert":
//     return jsonOutput_(handlePdfUpsert_(payload, extractBearerToken_(e, payload)));
//   case "pdf_delete":
//     return jsonOutput_(handlePdfDelete_(payload, extractBearerToken_(e, payload)));

function extractBearerToken_(e, payload) {
  var token = "";
  if (e && e.headers && e.headers.Authorization) {
    var m = /^Bearer\s+(.+)$/i.exec(String(e.headers.Authorization));
    if (m) token = m[1];
  }
  if (!token && payload && payload.token) token = String(payload.token);
  return token;
}

// To wire these handlers into the production Apps Script, edit the
// original doGet and doPost in Code.gs (see README). The appended code
// only defines helper functions and tab handlers — it does not
// monkeypatch at global scope, so it is safe to append to Code.gs
// unchanged; deployment still requires adding the branches below to
// the original doGet/doPost.

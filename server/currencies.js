/**
 * EkGuru — Razorpay Verified Supported Currency Registry
 *
 * Sourced directly from Razorpay's official international payment documentation:
 * https://razorpay.com/docs/payments/payments/international-payments/#supported-currencies
 *
 * Rules:
 * - 0-decimal currencies: exponent 0, subunit multiplier 1 (e.g., JPY, KRW, VND, CLP, ISK)
 * - 2-decimal currencies: exponent 2, subunit multiplier 100 (e.g., INR, USD, EUR, GBP, AED, CAD, AUD, SGD, CNY, CHF)
 * - 3-decimal currencies: exponent 3, subunit multiplier 1000 (e.g., BHD, IQD, JOD, KWD, OMR, TND)
 *
 * Only currencies present in this registry are supported. Never claim "all world currencies".
 */

"use strict";

const SUPPORTED_CURRENCIES = {
  // --- Popular / Highlighted Currencies ---
  INR: { code: "INR", name: "Indian Rupee", symbol: "₹", exponent: 2, minAmount: 1, popular: true },
  USD: { code: "USD", name: "United States Dollar", symbol: "$", exponent: 2, minAmount: 1, popular: true },
  EUR: { code: "EUR", name: "Euro", symbol: "€", exponent: 2, minAmount: 1, popular: true },
  GBP: { code: "GBP", name: "Pound Sterling", symbol: "£", exponent: 2, minAmount: 1, popular: true },
  AED: { code: "AED", name: "United Arab Emirates Dirham", symbol: "AED", exponent: 2, minAmount: 5, popular: true },
  CAD: { code: "CAD", name: "Canadian Dollar", symbol: "CA$", exponent: 2, minAmount: 1, popular: true },
  AUD: { code: "AUD", name: "Australian Dollar", symbol: "AU$", exponent: 2, minAmount: 1, popular: true },
  SGD: { code: "SGD", name: "Singapore Dollar", symbol: "S$", exponent: 2, minAmount: 1, popular: true },
  JPY: { code: "JPY", name: "Japanese Yen", symbol: "¥", exponent: 0, minAmount: 100, popular: true },
  CNY: { code: "CNY", name: "Chinese Yuan Renminbi", symbol: "CN¥", exponent: 2, minAmount: 5, popular: true },
  CHF: { code: "CHF", name: "Swiss Franc", symbol: "CHF", exponent: 2, minAmount: 1, popular: true },

  // --- Other Verified Razorpay Currencies (Alphabetical) ---
  ALL: { code: "ALL", name: "Albanian Lek", symbol: "L", exponent: 2, minAmount: 100 },
  AMD: { code: "AMD", name: "Armenian Dram", symbol: "֏", exponent: 2, minAmount: 500 },
  AWG: { code: "AWG", name: "Aruban Florin", symbol: "Afl.", exponent: 2, minAmount: 2 },
  AZN: { code: "AZN", name: "Azerbaijan Manat", symbol: "₼", exponent: 2, minAmount: 2 },
  BAM: { code: "BAM", name: "Convertible Mark", symbol: "KM", exponent: 2, minAmount: 2 },
  BBD: { code: "BBD", name: "Barbadian Dollar", symbol: "Bds$", exponent: 2, minAmount: 2 },
  BDT: { code: "BDT", name: "Bangladeshi Taka", symbol: "৳", exponent: 2, minAmount: 100 },
  BGN: { code: "BGN", name: "Bulgarian Lev", symbol: "лв", exponent: 2, minAmount: 2 },
  BHD: { code: "BHD", name: "Bahraini Dinar", symbol: "BD", exponent: 3, minAmount: 0.5 },
  BIF: { code: "BIF", name: "Burundi Franc", symbol: "FBu", exponent: 0, minAmount: 2500 },
  BMD: { code: "BMD", name: "Bermudian Dollar", symbol: "BD$", exponent: 2, minAmount: 1 },
  BND: { code: "BND", name: "Brunei Dollar", symbol: "B$", exponent: 2, minAmount: 2 },
  BOB: { code: "BOB", name: "Bolivian Boliviano", symbol: "Bs.", exponent: 2, minAmount: 5 },
  BRL: { code: "BRL", name: "Brazilian Real", symbol: "R$", exponent: 2, minAmount: 5 },
  BSD: { code: "BSD", name: "Bahamian Dollar", symbol: "B$", exponent: 2, minAmount: 1 },
  BTN: { code: "BTN", name: "Bhutanese Ngultrum", symbol: "Nu.", exponent: 2, minAmount: 100 },
  BWP: { code: "BWP", name: "Botswana Pula", symbol: "P", exponent: 2, minAmount: 15 },
  BZD: { code: "BZD", name: "Belize Dollar", symbol: "BZ$", exponent: 2, minAmount: 2 },
  CLP: { code: "CLP", name: "Chilean Peso", symbol: "CLP$", exponent: 0, minAmount: 1000 },
  COP: { code: "COP", name: "Colombian Peso", symbol: "COL$", exponent: 2, minAmount: 4000 },
  CRC: { code: "CRC", name: "Costa Rican Colon", symbol: "₡", exponent: 2, minAmount: 500 },
  CUP: { code: "CUP", name: "Cuban Peso", symbol: "₱", exponent: 2, minAmount: 25 },
  CVE: { code: "CVE", name: "Cabo Verde Escudo", symbol: "Esc", exponent: 2, minAmount: 100 },
  CZK: { code: "CZK", name: "Czech Koruna", symbol: "Kč", exponent: 2, minAmount: 25 },
  DJF: { code: "DJF", name: "Djibouti Franc", symbol: "Fdj", exponent: 0, minAmount: 200 },
  DKK: { code: "DKK", name: "Danish Krone", symbol: "kr", exponent: 2, minAmount: 5 },
  DOP: { code: "DOP", name: "Dominican Peso", symbol: "RD$", exponent: 2, minAmount: 50 },
  DZD: { code: "DZD", name: "Algerian Dinar", symbol: "DA", exponent: 2, minAmount: 150 },
  EGP: { code: "EGP", name: "Egyptian Pound", symbol: "E£", exponent: 2, minAmount: 50 },
  ETB: { code: "ETB", name: "Ethiopian Birr", symbol: "Br", exponent: 2, minAmount: 50 },
  FJD: { code: "FJD", name: "Fijian Dollar", symbol: "FJ$", exponent: 2, minAmount: 2 },
  GHS: { code: "GHS", name: "Ghanaian Cedi", symbol: "GH₵", exponent: 2, minAmount: 15 },
  GIP: { code: "GIP", name: "Gibraltar Pound", symbol: "£", exponent: 2, minAmount: 1 },
  GMD: { code: "GMD", name: "Gambian Dalasi", symbol: "D", exponent: 2, minAmount: 50 },
  GNF: { code: "GNF", name: "Guinean Franc", symbol: "FG", exponent: 0, minAmount: 10000 },
  GTQ: { code: "GTQ", name: "Guatemalan Quetzal", symbol: "Q", exponent: 2, minAmount: 10 },
  GYD: { code: "GYD", name: "Guyanese Dollar", symbol: "GY$", exponent: 2, minAmount: 200 },
  HKD: { code: "HKD", name: "Hong Kong Dollar", symbol: "HK$", exponent: 2, minAmount: 10 },
  HNL: { code: "HNL", name: "Honduran Lempira", symbol: "L", exponent: 2, minAmount: 25 },
  HRK: { code: "HRK", name: "Croatian Kuna", symbol: "kn", exponent: 2, minAmount: 5 },
  HTG: { code: "HTG", name: "Haitian Gourde", symbol: "G", exponent: 2, minAmount: 150 },
  HUF: { code: "HUF", name: "Hungarian Forint", symbol: "Ft", exponent: 2, minAmount: 400 },
  IDR: { code: "IDR", name: "Indonesian Rupiah", symbol: "Rp", exponent: 2, minAmount: 15000 },
  ILS: { code: "ILS", name: "Israeli New Shekel", symbol: "₪", exponent: 2, minAmount: 5 },
  IQD: { code: "IQD", name: "Iraqi Dinar", symbol: "ID", exponent: 3, minAmount: 1500 },
  ISK: { code: "ISK", name: "Iceland Krona", symbol: "kr", exponent: 0, minAmount: 150 },
  JMD: { code: "JMD", name: "Jamaican Dollar", symbol: "J$", exponent: 2, minAmount: 150 },
  JOD: { code: "JOD", name: "Jordanian Dinar", symbol: "JD", exponent: 3, minAmount: 1 },
  KES: { code: "KES", name: "Kenyan Shilling", symbol: "KSh", exponent: 2, minAmount: 150 },
  KGS: { code: "KGS", name: "Kyrgyzstani Som", symbol: "с", exponent: 2, minAmount: 100 },
  KHR: { code: "KHR", name: "Cambodian Riel", symbol: "៛", exponent: 2, minAmount: 4000 },
  KMF: { code: "KMF", name: "Comorian Franc", symbol: "CF", exponent: 0, minAmount: 500 },
  KRW: { code: "KRW", name: "Korean Won", symbol: "₩", exponent: 0, minAmount: 1000 },
  KWD: { code: "KWD", name: "Kuwaiti Dinar", symbol: "KD", exponent: 3, minAmount: 0.5 },
  KYD: { code: "KYD", name: "Cayman Islands Dollar", symbol: "CI$", exponent: 2, minAmount: 1 },
  KZT: { code: "KZT", name: "Kazakhstani Tenge", symbol: "₸", exponent: 2, minAmount: 500 },
  LAK: { code: "LAK", name: "Lao Kip", symbol: "₭", exponent: 2, minAmount: 20000 },
  LKR: { code: "LKR", name: "Sri Lankan Rupee", symbol: "SLRs", exponent: 2, minAmount: 300 },
  LRD: { code: "LRD", name: "Liberian Dollar", symbol: "L$", exponent: 2, minAmount: 200 },
  LSL: { code: "LSL", name: "Lesotho Loti", symbol: "L", exponent: 2, minAmount: 20 },
  MAD: { code: "MAD", name: "Moroccan Dirham", symbol: "MAD", exponent: 2, minAmount: 10 },
  MDL: { code: "MDL", name: "Moldovan Leu", symbol: "L", exponent: 2, minAmount: 20 },
  MGA: { code: "MGA", name: "Malagasy Ariary", symbol: "Ar", exponent: 2, minAmount: 5000 },
  MKD: { code: "MKD", name: "Macedonian Denar", symbol: "ден", exponent: 2, minAmount: 50 },
  MMK: { code: "MMK", name: "Myanmar Kyat", symbol: "K", exponent: 2, minAmount: 2000 },
  MNT: { code: "MNT", name: "Mongolian Tugrik", symbol: "₮", exponent: 2, minAmount: 3000 },
  MOP: { code: "MOP", name: "Macanese Pataca", symbol: "MOP$", exponent: 2, minAmount: 10 },
  MUR: { code: "MUR", name: "Mauritian Rupee", symbol: "MURs", exponent: 2, minAmount: 50 },
  MVR: { code: "MVR", name: "Maldivian Rufiyaa", symbol: "Rf", exponent: 2, minAmount: 15 },
  MWK: { code: "MWK", name: "Malawian Kwacha", symbol: "MK", exponent: 2, minAmount: 1500 },
  MXN: { code: "MXN", name: "Mexican Peso", symbol: "MX$", exponent: 2, minAmount: 20 },
  MYR: { code: "MYR", name: "Malaysian Ringgit", symbol: "RM", exponent: 2, minAmount: 5 },
  MZN: { code: "MZN", name: "Mozambique Metical", symbol: "MT", exponent: 2, minAmount: 60 },
  NAD: { code: "NAD", name: "Namibian Dollar", symbol: "N$", exponent: 2, minAmount: 20 },
  NGN: { code: "NGN", name: "Nigerian Naira", symbol: "₦", exponent: 2, minAmount: 1500 },
  NIO: { code: "NIO", name: "Nicaraguan Cordoba", symbol: "C$", exponent: 2, minAmount: 40 },
  NOK: { code: "NOK", name: "Norwegian Krone", symbol: "kr", exponent: 2, minAmount: 10 },
  NPR: { code: "NPR", name: "Nepalese Rupee", symbol: "NPRs", exponent: 2, minAmount: 150 },
  NZD: { code: "NZD", name: "New Zealand Dollar", symbol: "NZ$", exponent: 2, minAmount: 2 },
  OMR: { code: "OMR", name: "Rial Omani", symbol: "OMR", exponent: 3, minAmount: 0.5 },
  PEN: { code: "PEN", name: "Peruvian Sol", symbol: "S/.", exponent: 2, minAmount: 5 },
  PGK: { code: "PGK", name: "Papua New Guinean Kina", symbol: "K", exponent: 2, minAmount: 4 },
  PHP: { code: "PHP", name: "Philippine Peso", symbol: "₱", exponent: 2, minAmount: 50 },
  PKR: { code: "PKR", name: "Pakistani Rupee", symbol: "PKRs", exponent: 2, minAmount: 300 },
  PLN: { code: "PLN", name: "Polish Zloty", symbol: "zł", exponent: 2, minAmount: 5 },
  PYG: { code: "PYG", name: "Paraguayan Guarani", symbol: "₲", exponent: 0, minAmount: 7000 },
  QAR: { code: "QAR", name: "Qatari Riyal", symbol: "QR", exponent: 2, minAmount: 5 },
  RON: { code: "RON", name: "Romanian Leu", symbol: "lei", exponent: 2, minAmount: 5 },
  RSD: { code: "RSD", name: "Serbian Dinar", symbol: "дин.", exponent: 2, minAmount: 100 },
  RUB: { code: "RUB", name: "Russian Ruble", symbol: "₽", exponent: 2, minAmount: 100 },
  RWF: { code: "RWF", name: "Rwanda Franc", symbol: "RF", exponent: 0, minAmount: 1200 },
  SAR: { code: "SAR", name: "Saudi Arabian Riyal", symbol: "SR", exponent: 2, minAmount: 5 },
  SCR: { code: "SCR", name: "Seychellois Rupee", symbol: "SRe", exponent: 2, minAmount: 15 },
  SEK: { code: "SEK", name: "Swedish Krona", symbol: "kr", exponent: 2, minAmount: 10 },
  SLL: { code: "SLL", name: "Sierra Leonean Leone", symbol: "Le", exponent: 2, minAmount: 20000 },
  SOS: { code: "SOS", name: "Somali Shilling", symbol: "Ssh", exponent: 2, minAmount: 500 },
  SVC: { code: "SVC", name: "Salvadoran Colón", symbol: "₡", exponent: 2, minAmount: 10 },
  SZL: { code: "SZL", name: "Swazi Lilangeni", symbol: "E", exponent: 2, minAmount: 20 },
  THB: { code: "THB", name: "Thai Baht", symbol: "฿", exponent: 2, minAmount: 35 },
  TND: { code: "TND", name: "Tunisian Dinar", symbol: "DT", exponent: 3, minAmount: 3 },
  TRY: { code: "TRY", name: "Turkish Lira", symbol: "₺", exponent: 2, minAmount: 35 },
  TTD: { code: "TTD", name: "Trinidad and Tobago Dollar", symbol: "TT$", exponent: 2, minAmount: 10 },
  TWD: { code: "TWD", name: "New Taiwan Dollar", symbol: "NT$", exponent: 2, minAmount: 30 },
  TZS: { code: "TZS", name: "Tanzanian Shilling", symbol: "TSh", exponent: 2, minAmount: 2500 },
  UAH: { code: "UAH", name: "Ukrainian Hryvnia", symbol: "₴", exponent: 2, minAmount: 40 },
  UGX: { code: "UGX", name: "Uganda Shilling", symbol: "USh", exponent: 0, minAmount: 4000 },
  UYU: { code: "UYU", name: "Uruguayan Peso", symbol: "$U", exponent: 2, minAmount: 40 },
  UZS: { code: "UZS", name: "Uzbekistani So’m", symbol: "so'm", exponent: 2, minAmount: 12000 },
  VND: { code: "VND", name: "Vietnamese Dong", symbol: "₫", exponent: 0, minAmount: 25000 },
  VUV: { code: "VUV", name: "Vatu", symbol: "VT", exponent: 0, minAmount: 120 },
  XAF: { code: "XAF", name: "CFA Franc BEAC", symbol: "FCFA", exponent: 0, minAmount: 600 },
  XCD: { code: "XCD", name: "East Caribbean Dollar", symbol: "EC$", exponent: 2, minAmount: 3 },
  XOF: { code: "XOF", name: "CFA Franc BCEAO", symbol: "CFA", exponent: 0, minAmount: 600 },
  XPF: { code: "XPF", name: "CFP Franc", symbol: "FCFP", exponent: 0, minAmount: 100 },
  YER: { code: "YER", name: "Yemeni Rial", symbol: "YR", exponent: 2, minAmount: 250 },
  ZAR: { code: "ZAR", name: "South African Rand", symbol: "R", exponent: 2, minAmount: 20 },
  ZMW: { code: "ZMW", name: "Zambian Kwacha", symbol: "ZK", exponent: 2, minAmount: 25 },
};

/**
 * Checks whether a currency code is supported by Razorpay.
 * @param {string} code
 * @returns {boolean}
 */
function isSupportedCurrency(code) {
  if (!code || typeof code !== "string") return false;
  return Object.prototype.hasOwnProperty.call(SUPPORTED_CURRENCIES, code.trim().toUpperCase());
}

/**
 * Gets currency configuration for a supported currency code.
 * @param {string} code
 * @returns {object|null}
 */
function getCurrency(code) {
  if (!isSupportedCurrency(code)) return null;
  return SUPPORTED_CURRENCIES[code.trim().toUpperCase()];
}

/**
 * Returns all supported currencies as an array, sorted with popular ones first,
 * then alphabetically by name.
 * @returns {Array<object>}
 */
function listSupportedCurrencies() {
  const all = Object.values(SUPPORTED_CURRENCIES);
  return all.sort((a, b) => {
    if (a.popular && !b.popular) return -1;
    if (!a.popular && b.popular) return 1;
    return a.name.localeCompare(b.name);
  });
}

module.exports = {
  SUPPORTED_CURRENCIES,
  isSupportedCurrency,
  getCurrency,
  listSupportedCurrencies,
};

/**
 * EkGuru — Currency Amount & Subunit Utility
 *
 * Implements precise decimal handling for 0, 2, and 3-decimal currencies
 * without JavaScript floating-point errors (e.g., 0.1 + 0.2 !== 0.3).
 *
 * Validated against Razorpay API specifications:
 * - 0-decimal: JPY 1000 -> 1000 subunits (no decimal places accepted)
 * - 2-decimal: USD 10.50 -> 1050 subunits, INR 100 -> 10000 subunits
 * - 3-decimal: KWD 15.750 -> 15750 subunits (last decimal 0 as per Razorpay guidelines)
 */

"use strict";

const { getCurrency, isSupportedCurrency } = require("./currencies");

class AmountValidationError extends Error {
  constructor(message, code = "INVALID_AMOUNT") {
    super(message);
    this.name = "AmountValidationError";
    this.code = code;
  }
}

/**
 * Validates and parses an amount string or number into a clean string representation.
 * @param {number|string} rawAmount
 * @returns {string} clean amount string, e.g. "10.50"
 */
function sanitizeAmountString(rawAmount) {
  if (rawAmount === null || rawAmount === undefined) {
    throw new AmountValidationError("Amount is required.", "MISSING_AMOUNT");
  }

  let str;
  if (typeof rawAmount === "number") {
    if (!Number.isFinite(rawAmount)) {
      throw new AmountValidationError("Amount must be a finite number.", "NON_FINITE_AMOUNT");
    }
    str = rawAmount.toString();
  } else if (typeof rawAmount === "string") {
    str = rawAmount.trim();
  } else {
    throw new AmountValidationError("Amount must be a number or string.", "INVALID_TYPE");
  }

  if (str === "") {
    throw new AmountValidationError("Amount cannot be empty.", "EMPTY_AMOUNT");
  }

  // Reject negative signs explicitly
  if (str.startsWith("-")) {
    throw new AmountValidationError("Amount cannot be negative.", "NEGATIVE_AMOUNT");
  }

  // Reject non-numeric characters (allow single decimal point, no commas, no exponents)
  if (!/^\d+(\.\d+)?$/.test(str)) {
    throw new AmountValidationError("Amount contains invalid characters or malformed decimals.", "MALFORMED_AMOUNT");
  }

  return str;
}

/**
 * Converts a major currency amount (e.g., 10.50 USD) to Razorpay smallest subunits (e.g., 1050).
 * Uses exact string parsing and BigInt arithmetic to eliminate floating-point inaccuracies.
 *
 * @param {number|string} rawAmount - Major unit amount (e.g., 10.50)
 * @param {string} currencyCode - 3-letter ISO currency code (e.g., "USD")
 * @returns {number} Subunit integer for Razorpay order/payment API
 */
function toSubunits(rawAmount, currencyCode) {
  if (!currencyCode || typeof currencyCode !== "string") {
    throw new AmountValidationError("Currency code is required.", "MISSING_CURRENCY");
  }

  const code = currencyCode.trim().toUpperCase();
  const currency = getCurrency(code);
  if (!currency) {
    throw new AmountValidationError("Currency not available for this payment method.", "UNSUPPORTED_CURRENCY");
  }

  const amountStr = sanitizeAmountString(rawAmount);
  const parts = amountStr.split(".");
  const wholePartStr = parts[0];
  const fracPartStr = parts[1] || "";

  const exponent = currency.exponent;

  // Check 0-decimal currencies
  if (exponent === 0) {
    if (fracPartStr && !/^0+$/.test(fracPartStr)) {
      throw new AmountValidationError(
        `${code} is a zero-decimal currency and does not accept fractional amounts.`,
        "DECIMAL_NOT_ALLOWED"
      );
    }
    const subunits = BigInt(wholePartStr);
    if (subunits <= 0n) {
      throw new AmountValidationError("Amount must be greater than zero.", "ZERO_AMOUNT");
    }
    if (subunits > 100000000n) {
      throw new AmountValidationError("Amount exceeds maximum allowed transaction limit.", "AMOUNT_TOO_LARGE");
    }
    return Number(subunits);
  }

  // Check decimal precision for 2 and 3-decimal currencies
  if (fracPartStr.length > exponent) {
    throw new AmountValidationError(
      `${code} accepts at most ${exponent} decimal places.`,
      "EXCESS_DECIMAL_PLACES"
    );
  }

  // Pad fraction with trailing zeros up to exponent
  const paddedFrac = fracPartStr.padEnd(exponent, "0");
  let subunits = BigInt(wholePartStr) * BigInt(10 ** exponent) + BigInt(paddedFrac);

  // In Razorpay, for 3-decimal currencies (KWD, BHD, OMR), the last digit must be 0
  if (exponent === 3) {
    // Round to nearest 10 subunits as per Razorpay guideline (e.g., 99991 -> 99990)
    subunits = (subunits / 10n) * 10n;
  }

  if (subunits <= 0n) {
    throw new AmountValidationError("Amount must be greater than zero.", "ZERO_AMOUNT");
  }

  // Minimum amount validation:
  // For INR, Razorpay requires minimum 100 paise (₹1.00)
  if (code === "INR" && subunits < 100n) {
    throw new AmountValidationError("Minimum amount for INR is ₹1.00 (100 paise).", "MIN_AMOUNT_NOT_MET");
  }

  // For other 2-decimal currencies, at least 50 subunits (0.50)
  if (exponent === 2 && subunits < 50n) {
    throw new AmountValidationError(`Minimum amount for ${code} is 0.50.`, "MIN_AMOUNT_NOT_MET");
  }

  // Maximum upper limit safety guard (e.g. 50,000 USD equivalent / 100,000,000 subunits)
  if (subunits > 5000000000n) {
    throw new AmountValidationError("Amount exceeds maximum allowed transaction limit.", "AMOUNT_TOO_LARGE");
  }

  return Number(subunits);
}

/**
 * Converts subunits back to major unit float.
 * @param {number|bigint} subunits
 * @param {string} currencyCode
 * @returns {number}
 */
function fromSubunits(subunits, currencyCode) {
  const code = (currencyCode || "INR").trim().toUpperCase();
  const currency = getCurrency(code);
  const exp = currency ? currency.exponent : 2;
  const num = Number(subunits);
  if (!Number.isFinite(num)) return 0;
  return num / (10 ** exp);
}

/**
 * Formats a major amount with currency symbol and appropriate decimal places.
 * @param {number} majorAmount
 * @param {string} currencyCode
 * @param {string} [locale='en-US']
 * @returns {string}
 */
function formatAmount(majorAmount, currencyCode, locale = "en-US") {
  const code = (currencyCode || "INR").trim().toUpperCase();
  const currency = getCurrency(code);
  const exp = currency ? currency.exponent : 2;

  try {
    return new Intl.NumberFormat(locale, {
      style: "currency",
      currency: code,
      minimumFractionDigits: exp,
      maximumFractionDigits: exp,
    }).format(majorAmount);
  } catch (e) {
    const sym = currency ? currency.symbol : code;
    return `${sym} ${majorAmount.toFixed(exp)}`;
  }
}

module.exports = {
  AmountValidationError,
  sanitizeAmountString,
  toSubunits,
  fromSubunits,
  formatAmount,
};

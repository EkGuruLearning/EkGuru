/**
 * EkGuru — Razorpay Payments API Router
 *
 * Implements:
 * GET  /api/payments/razorpay/currencies
 * POST /api/payments/razorpay/order
 * POST /api/payments/razorpay/verify
 * POST /api/payments/razorpay/webhook
 */

"use strict";

const { listSupportedCurrencies, isSupportedCurrency, getCurrency } = require("./currencies");
const { AmountValidationError } = require("./amount-util");

/**
 * Sets standard JSON and CORS headers.
 */
function setCorsHeaders(req, res) {
  const origin = (req && req.headers && req.headers.origin) || "*";
  res.setHeader("Access-Control-Allow-Origin", origin);
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, X-Razorpay-Signature, Authorization");
  res.setHeader("Access-Control-Max-Age", "86400");
}

/**
 * Reads raw request body buffer.
 * @param {import('http').IncomingMessage} req
 * @returns {Promise<Buffer>}
 */
function readRawBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (chunk) => chunks.push(chunk));
    req.on("end", () => resolve(Buffer.concat(chunks)));
    req.on("error", (err) => reject(err));
  });
}

/**
 * Sends a JSON response safely.
 */
function sendJson(res, statusCode, data) {
  setCorsHeaders(null, res);
  res.statusCode = statusCode;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store, no-cache, must-revalidate, private");
  res.end(JSON.stringify(data));
}

/**
 * Handles payment API requests.
 *
 * @param {import('http').IncomingMessage} req
 * @param {import('http').ServerResponse} res
 * @param {import('./razorpay-service').RazorpayService} service
 * @returns {Promise<boolean>} true if route was handled, false otherwise
 */
async function handleApiRequest(req, res, service) {
  const parsedUrl = new URL(req.url, `http://${req.headers.host || "localhost"}`);
  const pathname = parsedUrl.pathname.replace(/\/+$/, "");

  setCorsHeaders(req, res);

  // Handle pre-flight CORS
  if (req.method === "OPTIONS") {
    res.statusCode = 204;
    res.end();
    return true;
  }

  // 1. GET /api/payments/razorpay/currencies
  if (req.method === "GET" && pathname === "/api/payments/razorpay/currencies") {
    const currencies = listSupportedCurrencies();
    sendJson(res, 200, {
      success: true,
      count: currencies.length,
      currencies,
    });
    return true;
  }

  // Read raw body for POST requests
  if (req.method === "POST") {
    const rawBuffer = await readRawBody(req);
    const rawBody = rawBuffer.toString("utf8");

    // 2. POST /api/payments/razorpay/webhook
    if (pathname === "/api/payments/razorpay/webhook") {
      const signature = req.headers["x-razorpay-signature"] || "";
      const result = await service.handleWebhook(rawBody, signature);
      sendJson(res, result.status || 200, result);
      return true;
    }

    let parsedBody = {};
    if (rawBody.trim()) {
      try {
        parsedBody = JSON.parse(rawBody);
      } catch (e) {
        sendJson(res, 400, { success: false, error: "Malformed JSON request body.", code: "MALFORMED_JSON" });
        return true;
      }
    }

    // 3. POST /api/payments/razorpay/order
    if (pathname === "/api/payments/razorpay/order") {
      try {
        const orderData = await service.createOrder({
          amount: parsedBody.amount,
          currency: parsedBody.currency,
          purpose: parsedBody.purpose || "ekguru_support",
          customerEmail: parsedBody.customer_email || parsedBody.customerEmail,
          customerName: parsedBody.customer_name || parsedBody.customerName,
        });
        sendJson(res, 200, orderData);
      } catch (err) {
        const status = err instanceof AmountValidationError ? 400 : 500;
        sendJson(res, status, {
          success: false,
          error: err.message,
          code: err.code || "ORDER_CREATION_FAILED",
        });
      }
      return true;
    }

    // 4. POST /api/payments/razorpay/verify
    if (pathname === "/api/payments/razorpay/verify") {
      try {
        const verifyResult = await service.verifyPayment({
          razorpay_order_id: parsedBody.razorpay_order_id,
          razorpay_payment_id: parsedBody.razorpay_payment_id,
          razorpay_signature: parsedBody.razorpay_signature,
          internal_id: parsedBody.internal_id,
          tampered_amount: parsedBody.tampered_amount,
          tampered_currency: parsedBody.tampered_currency,
        });

        if (!verifyResult.success) {
          sendJson(res, 400, verifyResult);
        } else {
          sendJson(res, 200, verifyResult);
        }
      } catch (err) {
        sendJson(res, 500, {
          success: false,
          error: "Internal server verification failure.",
          detail: err.message,
        });
      }
      return true;
    }
  }

  // Not handled
  if (pathname.startsWith("/api/payments/razorpay")) {
    sendJson(res, 404, { success: false, error: "Endpoint not found." });
    return true;
  }

  return false;
}

module.exports = {
  handleApiRequest,
  setCorsHeaders,
};

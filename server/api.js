/**
 * EkGuru — Razorpay Payments & Support API Router
 *
 * Implements:
 * GET  /api/payments/razorpay/currencies
 * POST /api/payments/razorpay/order
 * POST /api/payments/razorpay/verify
 * POST /api/payments/razorpay/webhook
 * GET  /api/support/recent
 * GET  /api/payments/health
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
function sendJson(res, statusCode, data, extraHeaders = {}) {
  setCorsHeaders(null, res);
  res.statusCode = statusCode;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  for (const [k, v] of Object.entries(extraHeaders)) {
    res.setHeader(k, v);
  }
  if (!res.hasHeader("Cache-Control")) {
    res.setHeader("Cache-Control", "no-store, no-cache, must-revalidate, private");
  }
  res.end(JSON.stringify(data));
}

/**
 * Handles payment and support API requests.
 *
 * @param {import('http').IncomingMessage} req
 * @param {import('http').ServerResponse} res
 * @param {import('./razorpay-service').RazorpayService} service
 * @returns {Promise<boolean>} true if route was handled, false otherwise
 */
async function handleApiRequest(req, res, service) {
  const parsedUrl = new URL(req.url, `http://${req.headers.host || "localhost"}`);
  const pathname = parsedUrl.pathname.replace(/\/+$/, "");
  const queryAction = parsedUrl.searchParams.get("action") || "";

  setCorsHeaders(req, res);

  // Handle pre-flight CORS
  if (req.method === "OPTIONS") {
    res.statusCode = 204;
    res.end();
    return true;
  }

  // 1. Currencies: GET ?action=currencies OR /api/payments/razorpay/currencies
  if (req.method === "GET" && (queryAction === "currencies" || pathname === "/api/payments/razorpay/currencies")) {
    const currencies = listSupportedCurrencies();
    sendJson(res, 200, {
      success: true,
      count: currencies.length,
      currencies,
    });
    return true;
  }

  // 2. Recent Supporters: GET ?action=recent-support OR /api/support/recent
  if (req.method === "GET" && (queryAction === "recent-support" || queryAction === "recent" || pathname === "/api/support/recent")) {
    const cb = parsedUrl.searchParams.get("callback") || parsedUrl.searchParams.get("jsonp");
    try {
      const supporters = await service.getRecentSupporters();
      const payload = {
        success: true,
        count: supporters.length,
        supporters,
        items: supporters,
      };
      if (cb && /^[a-zA-Z0-9_$.]+$/.test(cb.trim())) {
        setCorsHeaders(null, res);
        res.statusCode = 200;
        res.setHeader("Content-Type", "application/javascript; charset=utf-8");
        res.setHeader("Cache-Control", "public, max-age=60, s-maxage=120, stale-while-revalidate=300");
        res.end(`${cb.trim()}(${JSON.stringify(payload)});`);
        return true;
      }
      sendJson(
        res,
        200,
        payload,
        {
          "Cache-Control": "public, max-age=60, s-maxage=120, stale-while-revalidate=300",
        }
      );
    } catch (e) {
      const payload = { success: true, count: 0, supporters: [], items: [] };
      if (cb && /^[a-zA-Z0-9_$.]+$/.test(cb.trim())) {
        setCorsHeaders(null, res);
        res.statusCode = 200;
        res.setHeader("Content-Type", "application/javascript; charset=utf-8");
        res.end(`${cb.trim()}(${JSON.stringify(payload)});`);
        return true;
      }
      sendJson(res, 200, payload);
    }
    return true;
  }

  // 3. Health: GET ?action=health OR /api/payments/health
  if (req.method === "GET" && (queryAction === "health" || pathname === "/api/payments/health")) {
    sendJson(res, 200, {
      status: "ok",
      success: true,
      service: "EkGuru Payments & Support API",
      currencies_count: listSupportedCurrencies().length,
      timestamp: new Date().toISOString(),
    });
    return true;
  }

  // 3a. Create Order via GET / JSONP: GET ?action=create-order
  if (req.method === "GET" && queryAction === "create-order") {
    const cb = parsedUrl.searchParams.get("callback") || parsedUrl.searchParams.get("jsonp");
    try {
      const orderData = await service.createOrder({
        amount: parsedUrl.searchParams.get("amount"),
        currency: parsedUrl.searchParams.get("currency") || "INR",
        customerEmail: parsedUrl.searchParams.get("customer_email") || parsedUrl.searchParams.get("email"),
        customerName: parsedUrl.searchParams.get("customer_name") || parsedUrl.searchParams.get("name"),
        customerPhone: parsedUrl.searchParams.get("customer_phone") || parsedUrl.searchParams.get("phone"),
        country: parsedUrl.searchParams.get("country"),
        supportMessage: parsedUrl.searchParams.get("support_message") || parsedUrl.searchParams.get("message"),
        publicDisplayOptIn: parsedUrl.searchParams.get("publicDisplayOptIn") === "true" || parsedUrl.searchParams.get("public_display_opt_in") === "true",
      });
      if (cb && /^[a-zA-Z0-9_$.]+$/.test(cb.trim())) {
        setCorsHeaders(null, res);
        res.statusCode = 200;
        res.setHeader("Content-Type", "application/javascript; charset=utf-8");
        res.end(`${cb.trim()}(${JSON.stringify(orderData)});`);
        return true;
      }
      sendJson(res, 200, orderData);
    } catch (err) {
      const status = err instanceof AmountValidationError ? 400 : 500;
      const payload = { success: false, error: err.message, code: err.code || "ORDER_CREATION_FAILED" };
      if (cb && /^[a-zA-Z0-9_$.]+$/.test(cb.trim())) {
        setCorsHeaders(null, res);
        res.statusCode = 200;
        res.setHeader("Content-Type", "application/javascript; charset=utf-8");
        res.end(`${cb.trim()}(${JSON.stringify(payload)});`);
        return true;
      }
      sendJson(res, status, payload);
    }
    return true;
  }

  // 3b. Verify Payment via GET / JSONP: GET ?action=verify-payment
  if (req.method === "GET" && queryAction === "verify-payment") {
    const cb = parsedUrl.searchParams.get("callback") || parsedUrl.searchParams.get("jsonp");
    try {
      const verifyResult = await service.verifyPayment({
        razorpay_order_id: parsedUrl.searchParams.get("razorpay_order_id"),
        razorpay_payment_id: parsedUrl.searchParams.get("razorpay_payment_id"),
        razorpay_signature: parsedUrl.searchParams.get("razorpay_signature"),
        internal_id: parsedUrl.searchParams.get("internal_id"),
      });
      if (cb && /^[a-zA-Z0-9_$.]+$/.test(cb.trim())) {
        setCorsHeaders(null, res);
        res.statusCode = 200;
        res.setHeader("Content-Type", "application/javascript; charset=utf-8");
        res.end(`${cb.trim()}(${JSON.stringify(verifyResult)});`);
        return true;
      }
      sendJson(res, verifyResult.success ? 200 : 400, verifyResult);
    } catch (err) {
      const payload = { success: false, error: "Internal server verification failure.", detail: err.message };
      if (cb && /^[a-zA-Z0-9_$.]+$/.test(cb.trim())) {
        setCorsHeaders(null, res);
        res.statusCode = 200;
        res.setHeader("Content-Type", "application/javascript; charset=utf-8");
        res.end(`${cb.trim()}(${JSON.stringify(payload)});`);
        return true;
      }
      sendJson(res, 500, payload);
    }
    return true;
  }

  // 3c. Report Failure via GET / JSONP: GET ?action=report-failure
  if (req.method === "GET" && queryAction === "report-failure") {
    const cb = parsedUrl.searchParams.get("callback") || parsedUrl.searchParams.get("jsonp");
    const result = service.reportFailure({
      order_id: parsedUrl.searchParams.get("order_id") || parsedUrl.searchParams.get("razorpay_order_id"),
      internal_id: parsedUrl.searchParams.get("internal_id"),
      reason: parsedUrl.searchParams.get("reason"),
    });
    if (cb && /^[a-zA-Z0-9_$.]+$/.test(cb.trim())) {
      setCorsHeaders(null, res);
      res.statusCode = 200;
      res.setHeader("Content-Type", "application/javascript; charset=utf-8");
      res.end(`${cb.trim()}(${JSON.stringify(result)});`);
      return true;
    }
    sendJson(res, result.success ? 200 : 400, result);
    return true;
  }

  // 3d. Report Cancel via GET / JSONP: GET ?action=report-cancel
  if (req.method === "GET" && queryAction === "report-cancel") {
    const cb = parsedUrl.searchParams.get("callback") || parsedUrl.searchParams.get("jsonp");
    const result = service.reportCancel({
      order_id: parsedUrl.searchParams.get("order_id") || parsedUrl.searchParams.get("razorpay_order_id"),
      internal_id: parsedUrl.searchParams.get("internal_id"),
      reason: parsedUrl.searchParams.get("reason"),
    });
    if (cb && /^[a-zA-Z0-9_$.]+$/.test(cb.trim())) {
      setCorsHeaders(null, res);
      res.statusCode = 200;
      res.setHeader("Content-Type", "application/javascript; charset=utf-8");
      res.end(`${cb.trim()}(${JSON.stringify(result)});`);
      return true;
    }
    sendJson(res, result.success ? 200 : 400, result);
    return true;
  }

  // Read raw body for POST requests
  if (req.method === "POST") {
    const rawBuffer = await readRawBody(req);
    const rawBody = rawBuffer.toString("utf8");

    // 4. Webhook: POST ?action=webhook OR /api/payments/razorpay/webhook
    if (queryAction === "webhook" || pathname === "/api/payments/razorpay/webhook") {
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

    const effectiveAction = queryAction || parsedBody.action || "";

    // 5. Create Order: POST ?action=create-order OR /api/payments/razorpay/order
    if (effectiveAction === "create-order" || pathname === "/api/payments/razorpay/order") {
      try {
        const orderData = await service.createOrder({
          amount: parsedBody.amount,
          currency: parsedBody.currency,
          customer: parsedBody.customer,
          customerEmail: parsedBody.customer_email || parsedBody.customerEmail,
          customerName: parsedBody.customer_name || parsedBody.customerName,
          customerPhone: parsedBody.customer_phone || parsedBody.customerPhone,
          country: parsedBody.country,
          supportMessage: parsedBody.supportMessage || parsedBody.support_message,
          publicDisplayOptIn: parsedBody.publicDisplayOptIn !== undefined ? parsedBody.publicDisplayOptIn : parsedBody.public_display_opt_in,
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

    // 6. Verify Payment: POST ?action=verify-payment OR /api/payments/razorpay/verify
    if (effectiveAction === "verify-payment" || pathname === "/api/payments/razorpay/verify") {
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

    // 7. Report Failure: POST ?action=report-failure OR /api/payments/razorpay/report-failure
    if (effectiveAction === "report-failure" || pathname === "/api/payments/razorpay/report-failure") {
      const result = service.reportFailure({
        order_id: parsedBody.order_id || parsedBody.razorpay_order_id,
        internal_id: parsedBody.internal_id,
        reason: parsedBody.reason || parsedBody.error,
      });
      sendJson(res, result.success ? 200 : 400, result);
      return true;
    }

    // 8. Report Cancel: POST ?action=report-cancel OR /api/payments/razorpay/report-cancel
    if (effectiveAction === "report-cancel" || pathname === "/api/payments/razorpay/report-cancel") {
      const result = service.reportCancel({
        order_id: parsedBody.order_id || parsedBody.razorpay_order_id,
        internal_id: parsedBody.internal_id,
        reason: parsedBody.reason,
      });
      sendJson(res, result.success ? 200 : 400, result);
      return true;
    }
  }

  // Not handled
  if (pathname.startsWith("/api/payments") || pathname.startsWith("/api/support")) {
    sendJson(res, 404, { success: false, error: "Endpoint not found." });
    return true;
  }

  return false;
}

module.exports = {
  handleApiRequest,
  setCorsHeaders,
};

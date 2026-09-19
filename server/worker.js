/**
 * EkGuru — Cloudflare Workers / Serverless Edge Adapter
 *
 * Implements the Razorpay international payment API on Cloudflare Workers:
 * - GET  /api/payments/razorpay/currencies
 * - POST /api/payments/razorpay/order
 * - POST /api/payments/razorpay/verify
 * - POST /api/payments/razorpay/webhook
 *
 * Required Cloudflare Worker secrets (Settings -> Variables):
 * - RAZORPAY_KEY_ID
 * - RAZORPAY_KEY_SECRET
 * - RAZORPAY_WEBHOOK_SECRET
 */

import { listSupportedCurrencies, isSupportedCurrency } from "./currencies.js";
import { toSubunits, fromSubunits, AmountValidationError } from "./amount-util.js";
import { PaymentStore } from "./payment-store.js";
import { RazorpayService } from "./razorpay-service.js";

const edgeStore = new PaymentStore();

function corsHeaders(request) {
  const origin = request.headers.get("Origin") || "*";
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, X-Razorpay-Signature, Authorization",
    "Access-Control-Max-Age": "86400",
  };
}

function jsonResponse(data, status = 200, request = null) {
  const headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store, no-cache, must-revalidate, private",
    ...(request ? corsHeaders(request) : { "Access-Control-Allow-Origin": "*" }),
  };
  return new Response(JSON.stringify(data), { status, headers });
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const pathname = url.pathname.replace(/\/+$/, "");

    // Preflight CORS
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(request) });
    }

    const service = new RazorpayService({
      keyId: env.RAZORPAY_KEY_ID || "",
      keySecret: env.RAZORPAY_KEY_SECRET || "",
      webhookSecret: env.RAZORPAY_WEBHOOK_SECRET || "",
      store: edgeStore,
    });

    // 1. GET /api/payments/razorpay/currencies
    if (request.method === "GET" && pathname === "/api/payments/razorpay/currencies") {
      const currencies = listSupportedCurrencies();
      return jsonResponse({ success: true, count: currencies.length, currencies }, 200, request);
    }

    // 2. Webhook
    if (request.method === "POST" && pathname === "/api/payments/razorpay/webhook") {
      const rawBody = await request.text();
      const signature = request.headers.get("x-razorpay-signature") || "";
      const result = await service.handleWebhook(rawBody, signature);
      return jsonResponse(result, result.status || 200, request);
    }

    // 3. Order Creation
    if (request.method === "POST" && pathname === "/api/payments/razorpay/order") {
      try {
        const body = await request.json();
        const order = await service.createOrder({
          amount: body.amount,
          currency: body.currency,
          purpose: body.purpose || "ekguru_support",
          customerEmail: body.customer_email || body.customerEmail,
          customerName: body.customer_name || body.customerName,
        });
        return jsonResponse(order, 200, request);
      } catch (err) {
        const status = err instanceof AmountValidationError ? 400 : 500;
        return jsonResponse(
          { success: false, error: err.message, code: err.code || "ORDER_CREATION_FAILED" },
          status,
          request
        );
      }
    }

    // 4. Verification
    if (request.method === "POST" && pathname === "/api/payments/razorpay/verify") {
      try {
        const body = await request.json();
        const verifyResult = await service.verifyPayment({
          razorpay_order_id: body.razorpay_order_id,
          razorpay_payment_id: body.razorpay_payment_id,
          razorpay_signature: body.razorpay_signature,
          internal_id: body.internal_id,
          tampered_amount: body.tampered_amount,
          tampered_currency: body.tampered_currency,
        });
        return jsonResponse(verifyResult, verifyResult.success ? 200 : 400, request);
      } catch (err) {
        return jsonResponse({ success: false, error: "Internal verification failure", detail: err.message }, 500, request);
      }
    }

    // 404 for unknown endpoints
    return jsonResponse({ success: false, error: "Not Found" }, 404, request);
  },
};

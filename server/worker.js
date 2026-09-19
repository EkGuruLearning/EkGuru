/**
 * EkGuru — Cloudflare Workers / Serverless Edge Adapter
 *
 * Implements the Razorpay international payment API & Google Sheets mirror on Cloudflare Workers:
 * - GET  /api/payments/razorpay/currencies
 * - POST /api/payments/razorpay/order
 * - POST /api/payments/razorpay/verify
 * - POST /api/payments/razorpay/webhook
 * - GET  /api/support/recent
 * - GET  /api/payments/health
 *
 * Required Cloudflare Worker secrets (Settings -> Variables):
 * - RAZORPAY_KEY_ID
 * - RAZORPAY_KEY_SECRET
 * - RAZORPAY_WEBHOOK_SECRET
 * - SHEETS_INGEST_TOKEN
 * - GOOGLE_SHEETS_ENDPOINT
 *
 * Optional non-secret variable:
 * - GOOGLE_SPREADSHEET_ID = "1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI"
 */

import { listSupportedCurrencies, isSupportedCurrency } from "./currencies.js";
import { toSubunits, fromSubunits, AmountValidationError } from "./amount-util.js";
import { PaymentStore } from "./payment-store.js";
import { RazorpayService } from "./razorpay-service.js";
import { SheetsClient } from "./sheets-client.js";

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

function jsonResponse(data, status = 200, request = null, extraHeaders = {}) {
  const headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store, no-cache, must-revalidate, private",
    ...(request ? corsHeaders(request) : { "Access-Control-Allow-Origin": "*" }),
    ...extraHeaders,
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

    const sheetsClient = new SheetsClient({
      endpoint: env.GOOGLE_SHEETS_ENDPOINT || "",
      token: env.SHEETS_INGEST_TOKEN || "",
      spreadsheetId: env.GOOGLE_SPREADSHEET_ID || "1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI",
    });

    const service = new RazorpayService({
      keyId: env.RAZORPAY_KEY_ID || "",
      keySecret: env.RAZORPAY_KEY_SECRET || "",
      webhookSecret: env.RAZORPAY_WEBHOOK_SECRET || "",
      store: edgeStore,
      sheetsClient,
    });

    // 1. GET /api/payments/razorpay/currencies
    if (request.method === "GET" && pathname === "/api/payments/razorpay/currencies") {
      const currencies = listSupportedCurrencies();
      return jsonResponse({ success: true, count: currencies.length, currencies }, 200, request);
    }

    // 2. GET /api/support/recent
    if (request.method === "GET" && pathname === "/api/support/recent") {
      try {
        const supporters = await service.getRecentSupporters();
        return jsonResponse(
          { success: true, count: supporters.length, supporters },
          200,
          request,
          { "Cache-Control": "public, max-age=60, s-maxage=120, stale-while-revalidate=300" }
        );
      } catch (e) {
        return jsonResponse({ success: true, count: 0, supporters: [] }, 200, request);
      }
    }

    // 3. GET /api/payments/health
    if (request.method === "GET" && pathname === "/api/payments/health") {
      return jsonResponse(
        {
          status: "ok",
          service: "EkGuru Payments & Support Edge Worker",
          currencies_count: listSupportedCurrencies().length,
          timestamp: new Date().toISOString(),
        },
        200,
        request
      );
    }

    // 4. POST /api/payments/razorpay/webhook
    if (request.method === "POST" && pathname === "/api/payments/razorpay/webhook") {
      const rawBody = await request.text();
      const signature = request.headers.get("x-razorpay-signature") || "";
      const result = await service.handleWebhook(rawBody, signature);
      return jsonResponse(result, result.status || 200, request);
    }

    // 5. POST /api/payments/razorpay/order
    if (request.method === "POST" && pathname === "/api/payments/razorpay/order") {
      try {
        const body = await request.json();
        const order = await service.createOrder({
          amount: body.amount,
          currency: body.currency,
          customer: body.customer,
          customerEmail: body.customer_email || body.customerEmail,
          customerName: body.customer_name || body.customerName,
          customerPhone: body.customer_phone || body.customerPhone,
          country: body.country,
          supportMessage: body.supportMessage || body.support_message,
          publicDisplayOptIn: body.publicDisplayOptIn !== undefined ? body.publicDisplayOptIn : body.public_display_opt_in,
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

    // 6. POST /api/payments/razorpay/verify
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

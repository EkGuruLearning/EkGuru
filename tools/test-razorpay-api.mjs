/**
 * EkGuru — Complete 30-Gate Payment & Google Sheets Verification Suite
 *
 * Covers all 30 test gates mandated in Section 32:
 *  1. valid INR order
 *  2. valid USD order
 *  3. valid EUR order
 *  4. valid GBP order
 *  5. valid AED order
 *  6. valid JPY/zero-decimal path
 *  7. valid three-decimal currency path (KWD)
 *  8. unsupported currency rejection
 *  9. amount below minimum
 * 10. amount above maximum
 * 11. negative amount
 * 12. malformed amount
 * 13. amount tampering
 * 14. currency tampering
 * 15. invalid payment signature
 * 16. valid payment signature
 * 17. invalid webhook signature
 * 18. valid webhook
 * 19. duplicate webhook
 * 20. payment/order mismatch
 * 21. refund
 * 22. failed payment
 * 23. customer upsert
 * 24. public opt-in true
 * 25. public opt-in false
 * 26. public endpoint contains no private data
 * 27. Google Sheet temporary failure resilience
 * 28. Google Sheet retry mechanism
 * 29. secret scan (repository & public build outputs)
 * 30. frontend secret scan
 */

import fs from "fs";
import path from "path";
import crypto from "crypto";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, "..");

// Dynamic imports of server modules
const { RazorpayService } = await import("../server/razorpay-service.js");
const { PaymentStore } = await import("../server/payment-store.js");
const { SheetsClient } = await import("../server/sheets-client.js");
const { listSupportedCurrencies, isSupportedCurrency } = await import("../server/currencies.js");
const { toSubunits, fromSubunits, AmountValidationError } = await import("../server/amount-util.js");

const TEST_KEY_ID = "rzp_test_simulated_key_001";
const TEST_KEY_SECRET = "simulated_secret_test_abcdef123456";
const TEST_WEBHOOK_SECRET = "simulated_webhook_secret_xyz789";
const TEST_SHEETS_TOKEN = "simulated_sheets_token_secret999";

let passedCount = 0;
let failedCount = 0;

function assert(condition, gateNum, description, details = "") {
  if (condition) {
    passedCount++;
    console.log(`  PASS [Gate ${gateNum}] ${description}`);
  } else {
    failedCount++;
    console.error(`  FAIL [Gate ${gateNum}] ${description}`);
    if (details) console.error(`       Details: ${details}`);
  }
}

async function runTests() {
  console.log("\n=======================================================");
  console.log("  EkGuru Razorpay & Google Sheets 30-Gate Test Suite   ");
  console.log("=======================================================\n");

  const testStore = new PaymentStore();

  // Mock Sheets client that tracks calls
  const sheetsCalls = [];
  let simulateSheetsFailure = false;

  const mockSheetsFetch = async (url, opts) => {
    sheetsCalls.push({ url, opts });
    if (simulateSheetsFailure) {
      return {
        ok: false,
        status: 503,
        json: async () => ({ success: false, error: "Sheets service temporarily unavailable" }),
      };
    }
    const payload = JSON.parse(opts?.body || "{}");
    return {
      ok: true,
      status: 200,
      json: async () => ({ success: true, operation: payload.operation, status: "synced" }),
    };
  };

  const sheetsClient = new SheetsClient({
    endpoint: "https://script.google.com/macros/s/mock-deployment/exec",
    token: TEST_SHEETS_TOKEN,
    spreadsheetId: "1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI",
    fetch: mockSheetsFetch,
  });

  const service = new RazorpayService({
    keyId: TEST_KEY_ID,
    keySecret: TEST_KEY_SECRET,
    webhookSecret: TEST_WEBHOOK_SECRET,
    store: testStore,
    sheetsClient: sheetsClient,
    mockMode: true,
  });

  // 1. Valid INR order (500 INR -> 50000 paise)
  try {
    const res = await service.createOrder({
      amount: "500",
      currency: "INR",
      customer: { name: "Prakash Sharma", email: "prakash@example.com" },
    });
    assert(
      res.success && res.currency === "INR" && res.amount === 50000 && res.key_id === TEST_KEY_ID,
      1,
      "Valid INR order creation (500 INR -> 50000 paise)"
    );
  } catch (e) {
    assert(false, 1, "Valid INR order creation", e.message);
  }

  // 2. Valid USD order ($10.50 -> 1050 cents)
  try {
    const res = await service.createOrder({
      amount: "10.50",
      currency: "USD",
      customer: { name: "John Smith", email: "john@example.com" },
    });
    assert(
      res.success && res.currency === "USD" && res.amount === 1050,
      2,
      "Valid USD order creation ($10.50 -> 1050 cents)"
    );
  } catch (e) {
    assert(false, 2, "Valid USD order creation", e.message);
  }

  // 3. Valid EUR order (€15.00 -> 1500 cents)
  try {
    const res = await service.createOrder({
      amount: "15.00",
      currency: "EUR",
      customer: { name: "Claire Dupont", email: "claire@example.com" },
    });
    assert(
      res.success && res.currency === "EUR" && res.amount === 1500,
      3,
      "Valid EUR order creation (€15.00 -> 1500 cents)"
    );
  } catch (e) {
    assert(false, 3, "Valid EUR order creation", e.message);
  }

  // 4. Valid GBP order (£20.00 -> 2000 pence)
  try {
    const res = await service.createOrder({
      amount: "20.00",
      currency: "GBP",
      customer: { name: "Arthur Pendelton", email: "arthur@example.com" },
    });
    assert(
      res.success && res.currency === "GBP" && res.amount === 2000,
      4,
      "Valid GBP order creation (£20.00 -> 2000 pence)"
    );
  } catch (e) {
    assert(false, 4, "Valid GBP order creation", e.message);
  }

  // 5. Valid AED order (50.00 AED -> 5000 fils)
  try {
    const res = await service.createOrder({
      amount: "50.00",
      currency: "AED",
      customer: { name: "Ahmed Al-Mansoor", email: "ahmed@example.com", country: "United Arab Emirates" },
    });
    assert(
      res.success && res.currency === "AED" && res.amount === 5000,
      5,
      "Valid AED order creation (50.00 AED -> 5000 fils)"
    );
  } catch (e) {
    assert(false, 5, "Valid AED order creation", e.message);
  }

  // 6. Valid JPY / zero-decimal path (¥1500 -> 1500 subunits)
  try {
    const res = await service.createOrder({
      amount: "1500",
      currency: "JPY",
      customer: { name: "Kenji Sato", email: "kenji@example.com" },
    });
    let fracRejected = false;
    try {
      await service.createOrder({ amount: "1500.50", currency: "JPY" });
    } catch (err) {
      fracRejected = err instanceof AmountValidationError;
    }
    assert(
      res.success && res.currency === "JPY" && res.amount === 1500 && fracRejected,
      6,
      "Valid JPY zero-decimal handling (¥1500 -> 1500, fractions rejected)"
    );
  } catch (e) {
    assert(false, 6, "Valid JPY zero-decimal handling", e.message);
  }

  // 7. Valid 3-decimal currency path (15.750 KWD -> 15750 subunits)
  try {
    const res = await service.createOrder({
      amount: "15.750",
      currency: "KWD",
      customer: { name: "Fatima Al-Sabah", email: "fatima@example.com" },
    });
    assert(
      res.success && res.currency === "KWD" && res.amount === 15750,
      7,
      "Valid 3-decimal currency handling (15.750 KWD -> 15750 subunits)"
    );
  } catch (e) {
    assert(false, 7, "Valid 3-decimal currency handling", e.message);
  }

  // 8. Unsupported currency rejection
  try {
    let rejectedXYZ = false;
    let rejectedBTC = false;
    try {
      await service.createOrder({ amount: "10.00", currency: "XYZ" });
    } catch (e) {
      rejectedXYZ = e.code === "UNSUPPORTED_CURRENCY";
    }
    try {
      await service.createOrder({ amount: "1.00", currency: "BTC" });
    } catch (e) {
      rejectedBTC = e.code === "UNSUPPORTED_CURRENCY";
    }
    assert(rejectedXYZ && rejectedBTC, 8, "Unsupported currencies strictly rejected");
  } catch (e) {
    assert(false, 8, "Unsupported currency rejection", e.message);
  }

  // 9. Amount below minimum
  try {
    let belowMin = false;
    try {
      await service.createOrder({ amount: "0.25", currency: "USD" });
    } catch (e) {
      belowMin = e.code === "AMOUNT_TOO_LOW";
    }
    assert(belowMin, 9, "Amount below minimum rejected (0.25 USD < 1.00 min)");
  } catch (e) {
    assert(false, 9, "Amount below minimum check", e.message);
  }

  // 10. Amount above maximum
  try {
    let aboveMax = false;
    try {
      await service.createOrder({ amount: "999999", currency: "USD" });
    } catch (e) {
      aboveMax = e.code === "AMOUNT_TOO_HIGH";
    }
    assert(aboveMax, 10, "Amount above maximum rejected (999999 USD > 25000 max)");
  } catch (e) {
    assert(false, 10, "Amount above maximum check", e.message);
  }

  // 11. Negative amount
  try {
    let negativeRejected = false;
    try {
      await service.createOrder({ amount: "-25.00", currency: "USD" });
    } catch (e) {
      negativeRejected = e.code === "NEGATIVE_AMOUNT";
    }
    assert(negativeRejected, 11, "Negative amount strictly rejected");
  } catch (e) {
    assert(false, 11, "Negative amount check", e.message);
  }

  // 12. Malformed amount
  try {
    let malformedRejected = false;
    try {
      await service.createOrder({ amount: "invalid_sum", currency: "USD" });
    } catch (e) {
      malformedRejected = e.code === "MALFORMED_AMOUNT";
    }
    assert(malformedRejected, 12, "Malformed non-numeric amount rejected");
  } catch (e) {
    assert(false, 12, "Malformed amount check", e.message);
  }

  // 13. Amount tampering
  try {
    const order = await service.createOrder({ amount: "50.00", currency: "USD" });
    const paymentId = "pay_test_tamper_amt_1";
    const validSig = crypto
      .createHmac("sha256", TEST_KEY_SECRET)
      .update(`${order.order_id}|${paymentId}`)
      .digest("hex");

    const result = await service.verifyPayment({
      razorpay_order_id: order.order_id,
      razorpay_payment_id: paymentId,
      razorpay_signature: validSig,
      internal_id: order.internal_id,
      tampered_amount: 1000, // tampered from 5000 to 1000
    });

    assert(
      result.success === false && result.error.includes("Amount mismatch"),
      13,
      "Browser-supplied tampered amount detected and rejected"
    );
  } catch (e) {
    assert(false, 13, "Amount tampering check", e.message);
  }

  // 14. Currency tampering
  try {
    const order = await service.createOrder({ amount: "50.00", currency: "USD" });
    const paymentId = "pay_test_tamper_curr_1";
    const validSig = crypto
      .createHmac("sha256", TEST_KEY_SECRET)
      .update(`${order.order_id}|${paymentId}`)
      .digest("hex");

    const result = await service.verifyPayment({
      razorpay_order_id: order.order_id,
      razorpay_payment_id: paymentId,
      razorpay_signature: validSig,
      internal_id: order.internal_id,
      tampered_currency: "INR",
    });

    assert(
      result.success === false && result.error.includes("Currency mismatch"),
      14,
      "Browser-supplied tampered currency detected and rejected"
    );
  } catch (e) {
    assert(false, 14, "Currency tampering check", e.message);
  }

  // 15. Invalid payment signature
  try {
    const order = await service.createOrder({ amount: "10.00", currency: "USD" });
    const paymentId = "pay_test_inv_sig";
    const result = await service.verifyPayment({
      razorpay_order_id: order.order_id,
      razorpay_payment_id: paymentId,
      razorpay_signature: "bad_signature_deadbeef1234567890abcdef",
      internal_id: order.internal_id,
    });

    const record = testStore.getByOrderId(order.order_id);
    assert(
      result.success === false &&
      result.error.includes("Invalid payment signature") &&
      record.verification_status === "failed",
      15,
      "Invalid payment signature rejected and record marked failed"
    );
  } catch (e) {
    assert(false, 15, "Invalid payment signature check", e.message);
  }

  // 16. Valid payment signature
  try {
    const order = await service.createOrder({
      amount: "25.00",
      currency: "EUR",
      customer: { name: "Maria Garcia", email: "maria@example.com" },
    });
    const paymentId = "pay_test_valid_sig_123";
    const validSig = crypto
      .createHmac("sha256", TEST_KEY_SECRET)
      .update(`${order.order_id}|${paymentId}`)
      .digest("hex");

    const result = await service.verifyPayment({
      razorpay_order_id: order.order_id,
      razorpay_payment_id: paymentId,
      razorpay_signature: validSig,
      internal_id: order.internal_id,
    });

    const record = testStore.getByOrderId(order.order_id);
    assert(
      result.success === true &&
      result.message.includes("Payment received. Thank you for supporting EkGuru.") &&
      record.status === "captured" &&
      record.verification_status === "verified",
      16,
      "Valid payment signature verified successfully and recorded as captured"
    );
  } catch (e) {
    assert(false, 16, "Valid payment signature check", e.message);
  }

  // 17. Invalid webhook signature
  try {
    const rawBody = JSON.stringify({ event: "payment.captured", event_id: "evt_inv_wh" });
    const result = await service.handleWebhook(rawBody, "invalid_webhook_signature");
    assert(
      result.success === false && result.error.includes("Invalid webhook signature"),
      17,
      "Invalid webhook signature rejected with HTTP 400"
    );
  } catch (e) {
    assert(false, 17, "Invalid webhook signature check", e.message);
  }

  // 18. Valid webhook
  try {
    const order = await service.createOrder({ amount: "30.00", currency: "GBP" });
    const paymentId = "pay_test_webhook_valid_01";
    const webhookEvent = {
      entity: "event",
      event: "payment.captured",
      event_id: "evt_valid_test_001",
      payload: {
        payment: {
          entity: {
            id: paymentId,
            order_id: order.order_id,
            amount: 3000,
            currency: "GBP",
            status: "captured",
            method: "card",
            email: "patron@example.com",
          },
        },
      },
    };
    const rawBody = JSON.stringify(webhookEvent);
    const validWhSig = crypto
      .createHmac("sha256", TEST_WEBHOOK_SECRET)
      .update(rawBody)
      .digest("hex");

    const r = await service.handleWebhook(rawBody, validWhSig);
    const rec = testStore.getByOrderId(order.order_id);
    assert(
      r.success === true && rec.status === "captured" && rec.webhook_verified === true,
      18,
      "Valid payment.captured webhook processed and payment record updated"
    );
  } catch (e) {
    assert(false, 18, "Valid webhook check", e.message);
  }

  // 19. Duplicate webhook idempotency
  try {
    const order = await service.createOrder({ amount: "35.00", currency: "USD" });
    const paymentId = "pay_test_webhook_idem";
    const webhookEvent = {
      entity: "event",
      event: "payment.captured",
      event_id: "evt_idempotent_test_002",
      payload: {
        payment: {
          entity: {
            id: paymentId,
            order_id: order.order_id,
            amount: 3500,
            currency: "USD",
            status: "captured",
            email: "patron2@example.com",
          },
        },
      },
    };
    const rawBody = JSON.stringify(webhookEvent);
    const validWhSig = crypto
      .createHmac("sha256", TEST_WEBHOOK_SECRET)
      .update(rawBody)
      .digest("hex");

    const r1 = await service.handleWebhook(rawBody, validWhSig);
    const r2 = await service.handleWebhook(rawBody, validWhSig);
    assert(
      r1.success && r2.success && r2.duplicate === true,
      19,
      "Duplicate webhook handled idempotently without creating duplicate events"
    );
  } catch (e) {
    assert(false, 19, "Duplicate webhook check", e.message);
  }

  // 20. Payment / order mismatch
  try {
    const order = await service.createOrder({ amount: "40.00", currency: "CAD" });
    const result = await service.verifyPayment({
      razorpay_order_id: "order_different_merchant_123",
      razorpay_payment_id: "pay_mismatch_123",
      razorpay_signature: "some_sig",
      internal_id: order.internal_id,
    });
    assert(
      result.success === false && result.error.includes("Order mismatch"),
      20,
      "Payment and order ID mismatch rejected"
    );
  } catch (e) {
    assert(false, 20, "Payment/order mismatch check", e.message);
  }

  // 21. Refund event handling
  try {
    const order = await service.createOrder({ amount: "50.00", currency: "AUD" });
    const paymentId = "pay_for_refund_01";
    // Mark captured first
    testStore.updateRecord(order.internal_id, {
      razorpay_payment_id: paymentId,
      status: "captured",
      verification_status: "verified",
    });

    const refundEvent = {
      event: "refund.processed",
      event_id: "evt_refund_001",
      payload: {
        refund: {
          entity: {
            id: "rfnd_test_001",
            payment_id: paymentId,
            order_id: order.order_id,
            amount: 5000,
            currency: "AUD",
            status: "processed",
          },
        },
      },
    };
    const rawBody = JSON.stringify(refundEvent);
    const sig = crypto.createHmac("sha256", TEST_WEBHOOK_SECRET).update(rawBody).digest("hex");
    const res = await service.handleWebhook(rawBody, sig);
    const rec = testStore.getByOrderId(order.order_id);
    const refundRec = testStore.refunds.get("rfnd_test_001");

    assert(
      res.success && rec.status === "refunded" && rec.refund_status === "refunded" && refundRec && refundRec.amount === 50,
      21,
      "Refund event handled and synchronized to refund store"
    );
  } catch (e) {
    assert(false, 21, "Refund event check", e.message);
  }

  // 22. Failed payment event handling
  try {
    const order = await service.createOrder({ amount: "20.00", currency: "SGD" });
    const paymentId = "pay_failed_test_01";
    const failEvent = {
      event: "payment.failed",
      event_id: "evt_fail_001",
      payload: {
        payment: {
          entity: {
            id: paymentId,
            order_id: order.order_id,
            status: "failed",
          },
        },
      },
    };
    const rawBody = JSON.stringify(failEvent);
    const sig = crypto.createHmac("sha256", TEST_WEBHOOK_SECRET).update(rawBody).digest("hex");
    await service.handleWebhook(rawBody, sig);
    const rec = testStore.getByOrderId(order.order_id);
    assert(
      rec.status === "failed",
      22,
      "Failed payment webhook marks payment record as failed"
    );
  } catch (e) {
    assert(false, 22, "Failed payment check", e.message);
  }

  // 23. Customer upsert
  try {
    const cust1 = testStore.upsertCustomer({
      name: "Rohan Patel",
      email: "rohan@example.com",
      amount: 10,
      currency: "USD",
    });
    const cust2 = testStore.upsertCustomer({
      name: "Rohan Patel",
      email: "rohan@example.com",
      amount: 25,
      currency: "USD",
    });
    assert(
      cust1 && cust2 && cust2.total_payments === 2 && cust2.total_amount === 35,
      23,
      "Customer aggregate store accurately aggregates multiple contributions"
    );
  } catch (e) {
    assert(false, 23, "Customer upsert check", e.message);
  }

  // 24. Public opt-in true
  try {
    const order = await service.createOrder({
      amount: "25.00",
      currency: "USD",
      customer: { name: "Anil K.", country: "India" },
      supportMessage: "Keep up the great work!",
      publicDisplayOptIn: true,
    });
    const paymentId = "pay_optin_true_1";
    const validSig = crypto
      .createHmac("sha256", TEST_KEY_SECRET)
      .update(`${order.order_id}|${paymentId}`)
      .digest("hex");

    await service.verifyPayment({
      razorpay_order_id: order.order_id,
      razorpay_payment_id: paymentId,
      razorpay_signature: validSig,
      internal_id: order.internal_id,
    });

    const recent = await service.getRecentSupporters();
    const found = recent.some((s) => s.displayName === "Anil K." && s.amount === 25);
    assert(
      found,
      24,
      "Public opt-in true adds supporter to Recent Supporters view"
    );
  } catch (e) {
    assert(false, 24, "Public opt-in true check", e.message);
  }

  // 25. Public opt-in false
  try {
    const order = await service.createOrder({
      amount: "100.00",
      currency: "USD",
      customer: { name: "Secret Donor", country: "United States" },
      publicDisplayOptIn: false,
    });
    const paymentId = "pay_optin_false_1";
    const validSig = crypto
      .createHmac("sha256", TEST_KEY_SECRET)
      .update(`${order.order_id}|${paymentId}`)
      .digest("hex");

    await service.verifyPayment({
      razorpay_order_id: order.order_id,
      razorpay_payment_id: paymentId,
      razorpay_signature: validSig,
      internal_id: order.internal_id,
    });

    const recent = await service.getRecentSupporters();
    const leaked = recent.some((s) => s.displayName === "Secret Donor");
    assert(
      !leaked,
      25,
      "Public opt-in false strictly protects patron name from public view"
    );
  } catch (e) {
    assert(false, 25, "Public opt-in false check", e.message);
  }

  // 26. Public endpoint contains no private data
  try {
    const supporters = await service.getRecentSupporters();
    let hasLeak = false;
    for (const s of supporters) {
      const keys = Object.keys(s);
      if (
        keys.includes("email") ||
        keys.includes("phone") ||
        keys.includes("payment_id") ||
        keys.includes("order_id") ||
        keys.includes("internal_id")
      ) {
        hasLeak = true;
      }
    }
    assert(
      !hasLeak && supporters.length > 0,
      26,
      "Public supporters endpoint contains zero private identifiers (no email/phone/IDs)"
    );
  } catch (e) {
    assert(false, 26, "Public endpoint privacy check", e.message);
  }

  // 27. Google Sheet temporary failure resilience
  try {
    simulateSheetsFailure = true;
    const order = await service.createOrder({
      amount: "15.00",
      currency: "EUR",
      customer: { name: "Resilient Patron", email: "patron@example.com" },
    });
    const paymentId = "pay_sheets_offline_1";
    const validSig = crypto
      .createHmac("sha256", TEST_KEY_SECRET)
      .update(`${order.order_id}|${paymentId}`)
      .digest("hex");

    const result = await service.verifyPayment({
      razorpay_order_id: order.order_id,
      razorpay_payment_id: paymentId,
      razorpay_signature: validSig,
      internal_id: order.internal_id,
    });

    const rec = testStore.getByOrderId(order.order_id);
    assert(
      result.success === true && rec.status === "captured" && rec.sheet_sync_status === "failed",
      27,
      "Google Sheet temporary failure does NOT fail payment (status captured, sheet_sync_status failed)"
    );
  } catch (e) {
    assert(false, 27, "Google Sheet failure resilience check", e.message);
  }

  // 28. Google Sheet retry mechanism
  try {
    simulateSheetsFailure = false; // service restored
    const retryRes = await sheetsClient.processRetryQueue();
    assert(
      retryRes.processed > 0 && retryRes.remaining === 0,
      28,
      "Queued Sheet sync operations retried successfully after service recovery"
    );
  } catch (e) {
    assert(false, 28, "Google Sheet retry check", e.message);
  }

  // 29. Secret scan across repository & build outputs
  try {
    const publicExts = [".html", ".json", ".xml", ".txt", ".webmanifest"];
    let leakedInBuild = false;
    let checkedFiles = 0;

    function checkDir(dir) {
      for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
        if (ent.name.startsWith(".") && ent.name !== ".nojekyll") continue;
        if (["node_modules", "reports", "server", "tools", ".git"].includes(ent.name)) continue;
        const full = path.join(dir, ent.name);
        if (ent.isDirectory()) {
          checkDir(full);
        } else if (publicExts.some((ext) => ent.name.endsWith(ext))) {
          checkedFiles++;
          const content = fs.readFileSync(full, "utf8");
          if (content.includes(TEST_KEY_SECRET) || /RAZORPAY_KEY_SECRET\s*=\s*['"][^'"]+['"]/.test(content)) {
            leakedInBuild = true;
          }
        }
      }
    }

    checkDir(ROOT_DIR);
    assert(!leakedInBuild && checkedFiles > 50, 29, `Secret never appears in build output (scanned ${checkedFiles} public files)`);
  } catch (e) {
    assert(false, 29, "Secret scan check", e.message);
  }

  // 30. Frontend secret scan
  try {
    let leakedInJs = false;
    let jsFiles = 0;
    const jsDir = path.join(ROOT_DIR, "js");

    for (const ent of fs.readdirSync(jsDir, { withFileTypes: true })) {
      if (ent.isFile() && ent.name.endsWith(".js")) {
        jsFiles++;
        const content = fs.readFileSync(path.join(jsDir, ent.name), "utf8");
        if (
          content.includes(TEST_KEY_SECRET) ||
          content.includes("RAZORPAY_KEY_SECRET") ||
          content.includes(TEST_SHEETS_TOKEN) ||
          /key_secret\s*:\s*["'][^"']+["']/.test(content)
        ) {
          leakedInJs = true;
        }
      }
    }

    assert(!leakedInJs && jsFiles > 5, 30, `Secret never appears in client JS (scanned ${jsFiles} files in /js)`);
  } catch (e) {
    assert(false, 30, "Frontend secret scan check", e.message);
  }

  console.log("\n-------------------------------------------------------");
  console.log(`Results: ${passedCount} passed, ${failedCount} failed out of 30 gates.`);
  console.log("-------------------------------------------------------\n");

  if (failedCount > 0) {
    process.exit(1);
  }
}

runTests().catch((err) => {
  console.error("Test runner exception:", err);
  process.exit(1);
});

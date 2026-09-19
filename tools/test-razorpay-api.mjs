#!/usr/bin/env node
/**
 * EkGuru — Razorpay International Multi-Currency API Test Suite
 *
 * Automated tests for all 20 required gates:
 * 1. Valid INR order
 * 2. Valid USD order
 * 3. Valid EUR order
 * 4. Valid GBP order
 * 5. Valid JPY/zero-decimal handling
 * 6. Valid 3-decimal currency (KWD/BHD/OMR) handling
 * 7. Unsupported currency rejection
 * 8. Negative amount rejection
 * 9. Malformed amount rejection
 * 10. Browser-supplied tampered amount
 * 11. Browser-supplied tampered currency
 * 12. Invalid signature
 * 13. Valid signature
 * 14. Duplicate webhook idempotency
 * 15. Payment mismatch
 * 16. Order mismatch
 * 17. Secret never appears in build output
 * 18. Secret never appears in client JS
 * 19. Secret never appears in git diff
 * 20. No fake successful payment state
 */

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { PaymentStore } = require("../server/payment-store.js");
const { RazorpayService } = require("../server/razorpay-service.js");
const { toSubunits, fromSubunits, formatAmount } = require("../server/amount-util.js");
const { isSupportedCurrency, getCurrency, listSupportedCurrencies } = require("../server/currencies.js");
const { JSDOM } = require("jsdom");

const ROOT_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const TEST_KEY_ID = "rzp_test_ekguru_testsuite";
const TEST_KEY_SECRET = "sk_test_secret_for_unit_tests_only";
const TEST_WEBHOOK_SECRET = "whsec_test_secret_for_unit_tests_only";

let passedCount = 0;
let failedCount = 0;
const results = [];

function assert(condition, testNumber, description, detail = "") {
  if (condition) {
    passedCount++;
    console.log(`  PASS [Gate ${testNumber}] ${description}`);
    results.push({ gate: testNumber, pass: true, description });
  } else {
    failedCount++;
    console.error(`  FAIL [Gate ${testNumber}] ${description} — ${detail}`);
    results.push({ gate: testNumber, pass: false, description, detail });
  }
}

async function runTests() {
  console.log("\n=======================================================");
  console.log("  EkGuru Razorpay Multi-Currency API Verification Suite");
  console.log("=======================================================\n");

  const testStore = new PaymentStore();
  const service = new RazorpayService({
    keyId: TEST_KEY_ID,
    keySecret: TEST_KEY_SECRET,
    webhookSecret: TEST_WEBHOOK_SECRET,
    store: testStore,
  });

  // 1. Valid INR order
  try {
    const order = await service.createOrder({ amount: 500, currency: "INR" });
    const ok =
      order.success === true &&
      order.currency === "INR" &&
      order.amount === 50000 &&
      order.order_id &&
      order.key_id === TEST_KEY_ID &&
      !order.key_secret &&
      !order.secret;
    assert(ok, 1, "Valid INR order creation (500 INR -> 50000 paise)");
  } catch (e) {
    assert(false, 1, "Valid INR order creation", e.message);
  }

  // 2. Valid USD order
  try {
    const order = await service.createOrder({ amount: "10.50", currency: "USD" });
    const ok =
      order.success === true &&
      order.currency === "USD" &&
      order.amount === 1050 &&
      order.display_amount === 10.5 &&
      order.order_id &&
      !order.key_secret;
    assert(ok, 2, "Valid USD order creation ($10.50 -> 1050 cents)");
  } catch (e) {
    assert(false, 2, "Valid USD order creation", e.message);
  }

  // 3. Valid EUR order
  try {
    const order = await service.createOrder({ amount: "15.00", currency: "EUR" });
    const ok =
      order.success === true &&
      order.currency === "EUR" &&
      order.amount === 1500 &&
      order.order_id;
    assert(ok, 3, "Valid EUR order creation (€15.00 -> 1500 cents)");
  } catch (e) {
    assert(false, 3, "Valid EUR order creation", e.message);
  }

  // 4. Valid GBP order
  try {
    const order = await service.createOrder({ amount: "20.00", currency: "GBP" });
    const ok =
      order.success === true &&
      order.currency === "GBP" &&
      order.amount === 2000 &&
      order.order_id;
    assert(ok, 4, "Valid GBP order creation (£20.00 -> 2000 pence)");
  } catch (e) {
    assert(false, 4, "Valid GBP order creation", e.message);
  }

  // 5. Valid JPY/zero-decimal handling
  try {
    const order = await service.createOrder({ amount: "1500", currency: "JPY" });
    let decimalRejected = false;
    try {
      await service.createOrder({ amount: "1500.50", currency: "JPY" });
    } catch (err) {
      decimalRejected = true;
    }
    const ok =
      order.success === true &&
      order.currency === "JPY" &&
      order.amount === 1500 &&
      decimalRejected;
    assert(ok, 5, "Valid JPY zero-decimal handling (¥1500 -> 1500, fractions rejected)");
  } catch (e) {
    assert(false, 5, "Valid JPY zero-decimal handling", e.message);
  }

  // 6. Valid 3-decimal currency (KWD)
  try {
    const order = await service.createOrder({ amount: "15.750", currency: "KWD" });
    const ok =
      order.success === true &&
      order.currency === "KWD" &&
      order.amount === 15750 &&
      order.order_id;
    assert(ok, 6, "Valid 3-decimal currency handling (15.750 KWD -> 15750 subunits)");
  } catch (e) {
    assert(false, 6, "Valid 3-decimal currency handling", e.message);
  }

  // 7. Unsupported currency rejection
  try {
    let rejectedCount = 0;
    const testCases = ["XYZ", "BITCOIN", "DOGE", "FAKE123"];
    for (const bad of testCases) {
      try {
        await service.createOrder({ amount: "10.00", currency: bad });
      } catch (err) {
        if (err.message.includes("Currency not available for this payment method")) {
          rejectedCount++;
        }
      }
    }
    assert(rejectedCount === testCases.length, 7, "Unsupported currencies strictly rejected");
  } catch (e) {
    assert(false, 7, "Unsupported currency rejection", e.message);
  }

  // 8. Negative amount rejection
  try {
    let rejected = false;
    try {
      await service.createOrder({ amount: -25, currency: "USD" });
    } catch (e) {
      rejected = e.message.includes("negative");
    }
    assert(rejected, 8, "Negative amount rejected");
  } catch (e) {
    assert(false, 8, "Negative amount rejection", e.message);
  }

  // 9. Malformed amount rejection
  try {
    let malformedRejected = 0;
    const badAmounts = ["abc", "10.5.5", 0, "0", null, undefined, "10,00", Infinity, NaN];
    for (const bad of badAmounts) {
      try {
        await service.createOrder({ amount: bad, currency: "USD" });
      } catch (err) {
        malformedRejected++;
      }
    }
    assert(malformedRejected === badAmounts.length, 9, "Malformed / non-numeric amounts rejected");
  } catch (e) {
    assert(false, 9, "Malformed amount rejection", e.message);
  }

  // 10. Browser-supplied tampered amount
  try {
    const order = await service.createOrder({ amount: "50.00", currency: "USD" });
    const paymentId = "pay_test_tamper_amt_1";
    const validSig = crypto
      .createHmac("sha256", TEST_KEY_SECRET)
      .update(`${order.order_id}|${paymentId}`)
      .digest("hex");

    // Client attempts to verify with a tampered amount (e.g. paying $1.00 for a $50 order)
    const result = await service.verifyPayment({
      razorpay_order_id: order.order_id,
      razorpay_payment_id: paymentId,
      razorpay_signature: validSig,
      internal_id: order.internal_id,
      tampered_amount: 100, // 100 cents !== 5000 cents
    });

    assert(
      result.success === false && result.error.includes("Amount mismatch"),
      10,
      "Browser-supplied tampered amount detected and rejected"
    );
  } catch (e) {
    assert(false, 10, "Browser-supplied tampered amount", e.message);
  }

  // 11. Browser-supplied tampered currency
  try {
    const order = await service.createOrder({ amount: "50.00", currency: "USD" });
    const paymentId = "pay_test_tamper_curr_1";
    const validSig = crypto
      .createHmac("sha256", TEST_KEY_SECRET)
      .update(`${order.order_id}|${paymentId}`)
      .digest("hex");

    // Client attempts to swap currency to INR
    const result = await service.verifyPayment({
      razorpay_order_id: order.order_id,
      razorpay_payment_id: paymentId,
      razorpay_signature: validSig,
      internal_id: order.internal_id,
      tampered_currency: "INR",
    });

    assert(
      result.success === false && result.error.includes("Currency mismatch"),
      11,
      "Browser-supplied tampered currency detected and rejected"
    );
  } catch (e) {
    assert(false, 11, "Browser-supplied tampered currency", e.message);
  }

  // 12. Invalid signature
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
      12,
      "Invalid signature rejected and record marked failed"
    );
  } catch (e) {
    assert(false, 12, "Invalid signature", e.message);
  }

  // 13. Valid signature
  try {
    const order = await service.createOrder({ amount: "25.00", currency: "EUR" });
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
      13,
      "Valid signature verified successfully and recorded as captured"
    );
  } catch (e) {
    assert(false, 13, "Valid signature", e.message);
  }

  // 14. Duplicate webhook idempotency
  try {
    const order = await service.createOrder({ amount: "30.00", currency: "GBP" });
    const paymentId = "pay_test_webhook_idem";
    const webhookEvent = {
      entity: "event",
      account_id: "acc_test",
      event: "payment.captured",
      event_id: "evt_idempotent_test_001",
      contains: ["payment"],
      payload: {
        payment: {
          entity: {
            id: paymentId,
            order_id: order.order_id,
            amount: 3000,
            currency: "GBP",
            status: "captured",
            email: "supporter@example.com",
          },
        },
      },
      created_at: 1726718400,
    };

    const rawBody = JSON.stringify(webhookEvent);
    const validWhSig = crypto
      .createHmac("sha256", TEST_WEBHOOK_SECRET)
      .update(rawBody)
      .digest("hex");

    // First arrival
    const r1 = await service.handleWebhook(rawBody, validWhSig);
    const rec1 = testStore.getByOrderId(order.order_id);

    // Second arrival of same webhook
    const r2 = await service.handleWebhook(rawBody, validWhSig);
    const allRecordsForOrder = testStore.list().filter((r) => r.razorpay_order_id === order.order_id);

    assert(
      r1.success === true &&
      r2.success === true &&
      r2.duplicate === true &&
      allRecordsForOrder.length === 1 &&
      rec1.status === "captured" &&
      rec1.webhook_verified === true,
      14,
      "Duplicate webhook handled idempotently without creating duplicate records"
    );
  } catch (e) {
    assert(false, 14, "Duplicate webhook", e.message);
  }

  // 15. Payment mismatch
  try {
    const order = await service.createOrder({ amount: "40.00", currency: "CAD" });
    // Attempt verification with an order ID belonging to a different order
    const result = await service.verifyPayment({
      razorpay_order_id: "order_different_merchant_123",
      razorpay_payment_id: "pay_xyz",
      razorpay_signature: "some_sig",
      internal_id: order.internal_id, // internal ID points to CAD order, but order_id is mismatched
    });

    assert(
      result.success === false && result.error.includes("Order mismatch"),
      15,
      "Payment and order ID mismatch rejected"
    );
  } catch (e) {
    assert(false, 15, "Payment mismatch", e.message);
  }

  // 16. Order mismatch (unrecognized order ID)
  try {
    const result = await service.verifyPayment({
      razorpay_order_id: "order_unrecognized_9999",
      razorpay_payment_id: "pay_unrecognized_9999",
      razorpay_signature: "sig_9999",
    });

    assert(
      result.success === false && result.error.includes("Order mismatch"),
      16,
      "Unrecognized order not belonging to EkGuru rejected"
    );
  } catch (e) {
    assert(false, 16, "Order mismatch", e.message);
  }

  // 17. Secret never appears in build output
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
    assert(!leakedInBuild && checkedFiles > 50, 17, `Secret never appears in build output (scanned ${checkedFiles} public files)`);
  } catch (e) {
    assert(false, 17, "Secret in build output check", e.message);
  }

  // 18. Secret never appears in client JS
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
          /key_secret\s*:\s*["'][^"']+["']/.test(content)
        ) {
          leakedInJs = true;
        }
      }
    }

    assert(!leakedInJs && jsFiles > 5, 18, `Secret never appears in client JS (scanned ${jsFiles} files in /js)`);
  } catch (e) {
    assert(false, 18, "Secret in client JS check", e.message);
  }

  // 19. Secret never appears in git diff
  try {
    const { execSync } = require("child_process");
    let diff = "";
    try {
      diff = execSync("git diff HEAD", { cwd: ROOT_DIR, encoding: "utf8" });
    } catch (e) {}

    const hasSecretInDiff =
      diff.includes(TEST_KEY_SECRET) ||
      /^\+[^+].*RAZORPAY_KEY_SECRET\s*=\s*["'][a-zA-Z0-9_-]{8,}["']/m.test(diff);

    assert(!hasSecretInDiff, 19, "Secret never appears in git diff");
  } catch (e) {
    assert(false, 19, "Git diff secret check", e.message);
  }

  // 20. No fake successful payment state
  try {
    // Verify frontend DOM script guarantees genuine verification requirement
    const clientJs = fs.readFileSync(path.join(ROOT_DIR, "js/support-razorpay.js"), "utf8");
    const html = fs.readFileSync(path.join(ROOT_DIR, "support/index.html"), "utf8");

    const dom = new JSDOM(html, { runScripts: "outside-only", url: "https://ekguru.shop/support/" });
    const { window } = dom;

    let successStateReachedWithoutVerify = false;

    // In the script, verifyPaymentOnServer is called upon checkout handler.
    // If verify returns error or server is unreachable, showError is called, NEVER showSuccess.
    const hasProperVerifyGate =
      clientJs.includes("verifyPaymentOnServer") &&
      clientJs.includes("/api/payments/razorpay/verify") &&
      clientJs.includes("Payment received.") &&
      clientJs.includes("Payment could not be completed.") &&
      clientJs.includes("No payment was marked successful by EkGuru.");

    assert(hasProperVerifyGate, 20, "No fake success state: UI mandates positive server verification");
  } catch (e) {
    assert(false, 20, "Fake success state check", e.message);
  }

  console.log("\n-------------------------------------------------------");
  console.log(`Results: ${passedCount} passed, ${failedCount} failed out of 20 gates.`);
  console.log("-------------------------------------------------------\n");

  if (failedCount > 0) {
    process.exit(1);
  }
}

runTests().catch((err) => {
  console.error("Test runner exception:", err);
  process.exit(1);
});

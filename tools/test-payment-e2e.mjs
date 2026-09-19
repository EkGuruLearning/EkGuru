// tools/test-payment-e2e.mjs
// End-to-end integration test of the complete Razorpay & Google Sheets payment pipeline
// Exercises: Support Form -> Order Creation -> Checkout Prefill -> Signature Verification ->
// Single Reconciler -> Payments, Customers, PublicSupport, WebhookEvents, Refunds -> Recent Support API -> UI.

import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import crypto from 'node:crypto';
import { JSDOM } from 'jsdom';

console.log('=======================================================');
console.log('  EkGuru Support End-to-End Payment Pipeline Test      ');
console.log('=======================================================');

const codePath = path.resolve(process.cwd(), 'apps-script/Code.gs');
const codeGs = fs.readFileSync(codePath, 'utf8');

function createMockEnvironment(customProps = {}) {
  const scriptProperties = {
    RAZORPAY_MODE: 'TEST',
    RAZORPAY_KEY_ID: 'rzp_test_simulated_key_001',
    RAZORPAY_KEY_SECRET: 'test_secret_for_e2e_verification_98765',
    RAZORPAY_WEBHOOK_SECRET: 'test_webhook_secret_e2e_54321',
    SPREADSHEET_ID: '1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI',
    ...customProps,
  };

  const cacheStore = new Map();

  class MockRange {
    constructor(sheet, row, col, numRows = 1, numCols = 1) {
      this.sheet = sheet;
      this.row = row;
      this.col = col;
      this.numRows = numRows;
      this.numCols = numCols;
    }
    setValues(values) {
      for (let r = 0; r < values.length; r++) {
        for (let c = 0; c < values[r].length; c++) {
          this.sheet._setCell(this.row + r, this.col + c, values[r][c]);
        }
      }
      return this;
    }
    setValue(val) {
      this.sheet._setCell(this.row, this.col, val);
      return this;
    }
    getValues() {
      const result = [];
      for (let r = 0; r < this.numRows; r++) {
        const rowArr = [];
        for (let c = 0; c < this.numCols; c++) {
          rowArr.push(this.sheet._getCell(this.row + r, this.col + c));
        }
        result.push(rowArr);
      }
      return result;
    }
    setFontWeight() { return this; }
    setBackground() { return this; }
    setFontColor() { return this; }
  }

  class MockSheet {
    constructor(name) {
      this.name = name;
      this.grid = [];
    }
    _getCell(r, c) {
      if (r <= this.grid.length && c <= (this.grid[r - 1] || []).length) {
        return this.grid[r - 1][c - 1];
      }
      return '';
    }
    _setCell(r, c, val) {
      while (this.grid.length < r) this.grid.push([]);
      while (this.grid[r - 1].length < c) this.grid[r - 1].push('');
      this.grid[r - 1][c - 1] = val;
    }
    getLastRow() { return this.grid.length; }
    getLastColumn() {
      let max = 0;
      for (const row of this.grid) if (row.length > max) max = row.length;
      return max;
    }
    getMaxColumns() { return Math.max(this.getLastColumn(), 30); }
    appendRow(row) {
      this.grid.push([...row]);
      return this;
    }
    getRange(row, col, numRows = 1, numCols = 1) {
      return new MockRange(this, row, col, numRows, numCols);
    }
    insertColumnsAfter() { return this; }
    setFrozenRows() { return this; }
  }

  class MockSpreadsheet {
    constructor() {
      this.sheets = new Map();
    }
    getSheetByName(name) { return this.sheets.get(name) || null; }
    insertSheet(name) {
      const s = new MockSheet(name);
      this.sheets.set(name, s);
      return s;
    }
  }

  const mockSpreadsheet = new MockSpreadsheet();

  const context = {
    console,
    Math,
    Date,
    Number,
    String,
    Boolean,
    parseInt,
    parseFloat,
    isNaN,
    isFinite,
    JSON,
    Object,
    Array,
    RegExp,
    PropertiesService: {
      getScriptProperties: () => ({
        getProperty: (key) => scriptProperties[key] || null,
        setProperty: (key, val) => { scriptProperties[key] = String(val); },
      }),
    },
    CacheService: {
      getScriptCache: () => ({
        get: (key) => cacheStore.get(key) || null,
        put: (key, val) => { cacheStore.set(key, String(val)); },
        remove: (key) => { cacheStore.delete(key); },
      }),
    },
    SpreadsheetApp: {
      openById: (id) => {
        if (id !== '1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI') {
          throw new Error('Spreadsheet not found: ' + id);
        }
        return mockSpreadsheet;
      },
    },
    Utilities: {
      computeHmacSha256Signature: (data, secret) => {
        const hmac = crypto.createHmac('sha256', secret);
        hmac.update(data);
        const buf = hmac.digest();
        const signed = [];
        for (let i = 0; i < buf.length; i++) {
          const byte = buf[i];
          signed.push(byte > 127 ? byte - 256 : byte);
        }
        return signed;
      },
      base64Encode: (str) => Buffer.from(str).toString('base64'),
      getUuid: () => crypto.randomUUID(),
    },
    ContentService: {
      MimeType: { JSON: 'application/json' },
      createTextOutput: (text) => ({
        setMimeType: () => ({
          getContent: () => text,
        }),
      }),
    },
  };

  vm.createContext(context);
  vm.runInContext(codeGs, context);

  return { context, mockSpreadsheet, scriptProperties };
}

let passed = 0;
let total = 0;

function runTest(desc, fn) {
  total++;
  try {
    fn();
    console.log(`  PASS [E2E ${total}] ${desc}`);
    passed++;
  } catch (err) {
    console.error(`  FAIL [E2E ${total}] ${desc}:`, err.message);
    throw err;
  }
}

// 1. Health check returns TEST mode & configuration booleans
runTest('Health diagnostic endpoint returns clean status without secrets', () => {
  const { context } = createMockEnvironment();
  const resp = JSON.parse(context.doGet({ parameter: { action: 'health' } }).getContent());
  assert.equal(resp.success, true);
  assert.equal(resp.service, 'EkGuru Payment Backend');
  assert.equal(resp.mode, 'TEST');
  assert.equal(resp.razorpayKeyConfigured, true);
  assert.equal(resp.razorpaySecretConfigured, true);
  assert.equal(resp.webhookSecretConfigured, true);
  assert.equal(resp.spreadsheetConfigured, true);
  assert.equal(resp.currencies_count, 128);
  assert.ok(!JSON.stringify(resp).includes('secret'));
});

// 2. Diagnostics endpoint verifies sheet accessibility
runTest('Diagnostics endpoint verifies spreadsheet connectivity safely', () => {
  const { context } = createMockEnvironment();
  const resp = JSON.parse(context.doGet({ parameter: { action: 'diagnostics' } }).getContent());
  assert.equal(resp.success, true);
  assert.equal(resp.sheetAccessible, true);
  assert.equal(resp.mode, 'TEST');
  assert.ok(resp.deploymentUrl.includes('/exec'));
});

// 3. Complete INR Support Payment with Public Opt-In
runTest('Complete INR Support Payment with Public Opt-In updates all tabs', () => {
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();

  // Step 1: Create Order from Support Form
  const createResp = JSON.parse(context.doPost({
    postData: {
      contents: JSON.stringify({
        action: 'create-order',
        amount: '299',
        currency: 'INR',
        customer_name: 'Rahul Sharma',
        customer_email: 'rahul.sharma@example.com',
        customer_phone: '+919876543210',
        country: 'India',
        support_message: 'Keep learning free for everyone!',
        publicDisplayOptIn: true,
      }),
    },
  }).getContent());

  assert.equal(createResp.success, true);
  assert.ok(createResp.order_id);
  assert.equal(createResp.amount, 29900); // 299 * 100 paise
  assert.equal(createResp.currency, 'INR');
  assert.equal(createResp.publicDisplayOptIn, true);

  // Check Payments tab created state
  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  assert.equal(paySheet.grid.length, 2); // 1 header + 1 order
  assert.equal(paySheet.grid[1][4], 'created');
  assert.equal(paySheet.grid[1][5], 299);
  assert.equal(paySheet.grid[1][9], 'Rahul Sharma');

  // Step 2: Checkout completion -> Verify Payment
  const paymentId = 'pay_e2e_rahul_001';
  const sig = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET)
    .update(`${createResp.order_id}|${paymentId}`)
    .digest('hex');

  const verifyResp = JSON.parse(context.doPost({
    postData: {
      contents: JSON.stringify({
        action: 'verify-payment',
        razorpay_order_id: createResp.order_id,
        razorpay_payment_id: paymentId,
        razorpay_signature: sig,
        internal_id: createResp.internal_id,
        customer_name: 'Rahul Sharma',
        customer_email: 'rahul.sharma@example.com',
        publicDisplayOptIn: true,
      }),
    },
  }).getContent());

  assert.equal(verifyResp.success, true);
  assert.equal(verifyResp.status, 'captured');
  assert.equal(verifyResp.message, 'Payment received. Thank you for supporting EkGuru.');

  // Check Payments tab captured state
  assert.equal(paySheet.grid[1][2], paymentId);
  assert.equal(paySheet.grid[1][4], 'captured');
  assert.equal(paySheet.grid[1][18], 'true'); // Verified

  // Check Customers tab updated
  const custSheet = mockSpreadsheet.getSheetByName('Customers');
  assert.equal(custSheet.grid.length, 2); // 1 customer row
  const custRow = custSheet.grid[1];
  assert.equal(custRow[1], 'Rahul Sharma');
  assert.equal(custRow[2], 'rahul.sharma@example.com');
  assert.equal(custRow[7], 1); // Total Payments: 1
  assert.equal(custRow[8], 'INR 299.00');

  // Check PublicSupport tab updated
  const pubSheet = mockSpreadsheet.getSheetByName('PublicSupport');
  assert.equal(pubSheet.grid.length, 2); // 1 public supporter row
  const pubRow = pubSheet.grid[1];
  assert.equal(pubRow[1], 'Rahul Sharma');
  assert.equal(pubRow[2], 'India');
  assert.equal(pubRow[3], 299);
  assert.equal(pubRow[4], 'INR');
  assert.equal(pubRow[5], 'Keep learning free for everyone!');

  // Check Recent Supporters public GET
  const recentResp = JSON.parse(context.doGet({ parameter: { action: 'recent-support' } }).getContent());
  assert.equal(recentResp.success, true);
  assert.equal(recentResp.supporters.length, 1);
  assert.equal(recentResp.supporters[0].displayName, 'Rahul Sharma');
  assert.equal(recentResp.supporters[0].country, 'India');
  assert.equal(recentResp.supporters[0].amount, 299);
  assert.equal(recentResp.supporters[0].currency, 'INR');

  // Verify zero private identifiers leaked
  const str = JSON.stringify(recentResp);
  assert.ok(!str.includes('rahul.sharma@example.com'));
  assert.ok(!str.includes('9876543210'));
  assert.ok(!str.includes('pay_e2e_rahul_001'));
  assert.ok(!str.includes(createResp.order_id));
});

// 4. Private Payment (Opt-Out) preserves privacy
runTest('Private Payment (publicDisplayOptIn = false) leaves PublicSupport clean', () => {
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();

  // Create Order with publicDisplayOptIn = false
  const createResp = JSON.parse(context.doPost({
    postData: {
      contents: JSON.stringify({
        action: 'create-order',
        amount: '1000',
        currency: 'INR',
        customer_name: 'Private Patron',
        customer_email: 'private.patron@example.com',
        customer_phone: '+919123456789',
        country: 'India',
        support_message: 'Do not publish my name',
        publicDisplayOptIn: false,
      }),
    },
  }).getContent());

  const paymentId = 'pay_priv_002';
  const sig = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET)
    .update(`${createResp.order_id}|${paymentId}`)
    .digest('hex');

  context.doPost({
    postData: {
      contents: JSON.stringify({
        action: 'verify-payment',
        razorpay_order_id: createResp.order_id,
        razorpay_payment_id: paymentId,
        razorpay_signature: sig,
        internal_id: createResp.internal_id,
        publicDisplayOptIn: false,
      }),
    },
  });

  // Verify Payments and Customers updated
  assert.equal(mockSpreadsheet.getSheetByName('Payments').grid.length, 2);
  assert.equal(mockSpreadsheet.getSheetByName('Customers').grid.length, 2);

  // PublicSupport MUST have zero supporter rows
  const pubSheet = mockSpreadsheet.getSheetByName('PublicSupport');
  assert.equal(pubSheet.grid.length, 1); // Only header row

  // Recent supporters GET must be empty
  const recentResp = JSON.parse(context.doGet({ parameter: { action: 'recent-support' } }).getContent());
  assert.equal(recentResp.supporters.length, 0);
});

// 5. Webhook Reconciles Payment and Updates Customers (Root Cause Fix)
runTest('Razorpay webhook (payment.captured) updates Payments, Customers, and PublicSupport', () => {
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();

  // Create Order
  const createResp = JSON.parse(context.doPost({
    postData: {
      contents: JSON.stringify({
        action: 'create-order',
        amount: '25.00',
        currency: 'USD',
        customer_name: 'Sarah Connor',
        customer_email: 'sarah.connor@example.com',
        customer_phone: '+15551234567',
        country: 'United States',
        support_message: 'Keep up the Hindi lessons!',
        publicDisplayOptIn: true,
      }),
    },
  }).getContent());

  // Out-of-band webhook arrives from Razorpay
  const paymentId = 'pay_webhook_sarah_003';
  const webhookBody = JSON.stringify({
    event: 'payment.captured',
    event_id: 'evt_sarah_captured_001',
    payload: {
      payment: {
        entity: {
          id: paymentId,
          order_id: createResp.order_id,
          amount: 2500,
          currency: 'USD',
          status: 'captured',
          method: 'card',
          fee: 75,
          tax: 14,
          notes: {
            internal_id: createResp.internal_id,
            customer_name: 'Sarah Connor',
            customer_email: 'sarah.connor@example.com',
            public_opt_in: 'true',
            country: 'United States',
          },
        },
      },
    },
  });

  const webhookSig = crypto.createHmac('sha256', scriptProperties.RAZORPAY_WEBHOOK_SECRET)
    .update(webhookBody)
    .digest('hex');

  const hookResp = JSON.parse(context.doPost({
    parameter: { action: 'webhook' },
    headers: { 'X-Razorpay-Signature': webhookSig },
    postData: { contents: webhookBody },
  }).getContent());

  assert.equal(hookResp.success, true);

  // Check Payments tab
  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  assert.equal(paySheet.grid[1][4], 'captured');
  assert.equal(paySheet.grid[1][14], 0.75); // Fee

  // Check Customers tab updated by Webhook!
  const custSheet = mockSpreadsheet.getSheetByName('Customers');
  assert.equal(custSheet.grid.length, 2);
  assert.equal(custSheet.grid[1][1], 'Sarah Connor');
  assert.equal(custSheet.grid[1][2], 'sarah.connor@example.com');
  assert.equal(custSheet.grid[1][7], 1); // Total Payments = 1
  assert.equal(custSheet.grid[1][8], 'USD 25.00');

  // Check PublicSupport tab updated by Webhook!
  const pubSheet = mockSpreadsheet.getSheetByName('PublicSupport');
  assert.equal(pubSheet.grid.length, 2);
  assert.equal(pubSheet.grid[1][1], 'Sarah Connor');
  assert.equal(pubSheet.grid[1][3], 25);
  assert.equal(pubSheet.grid[1][4], 'USD');
});

// 6. Webhook and verify-payment Convergence Idempotency
runTest('order.paid following payment.captured converges without duplicate customer counts', () => {
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();

  // Create order
  const createResp = JSON.parse(context.doPost({
    postData: {
      contents: JSON.stringify({
        action: 'create-order',
        amount: '50.00',
        currency: 'EUR',
        customer_name: 'Elena Rostova',
        customer_email: 'elena@example.com',
        publicDisplayOptIn: true,
      }),
    },
  }).getContent());

  const paymentId = 'pay_elena_004';

  // Event 1: payment.captured webhook
  const body1 = JSON.stringify({
    event: 'payment.captured',
    event_id: 'evt_elena_captured',
    payload: {
      payment: {
        entity: {
          id: paymentId,
          order_id: createResp.order_id,
          amount: 5000,
          currency: 'EUR',
          notes: { public_opt_in: 'true', customer_name: 'Elena Rostova', customer_email: 'elena@example.com' },
        },
      },
    },
  });
  const sig1 = crypto.createHmac('sha256', scriptProperties.RAZORPAY_WEBHOOK_SECRET).update(body1).digest('hex');
  context.doPost({
    parameter: { action: 'webhook' },
    headers: { 'X-Razorpay-Signature': sig1 },
    postData: { contents: body1 },
  });

  // Event 2: order.paid webhook
  const body2 = JSON.stringify({
    event: 'order.paid',
    event_id: 'evt_elena_order_paid',
    payload: {
      order: {
        entity: {
          id: createResp.order_id,
          amount: 5000,
          currency: 'EUR',
        },
      },
      payment: {
        entity: {
          id: paymentId,
          order_id: createResp.order_id,
          amount: 5000,
          currency: 'EUR',
        },
      },
    },
  });
  const sig2 = crypto.createHmac('sha256', scriptProperties.RAZORPAY_WEBHOOK_SECRET).update(body2).digest('hex');
  context.doPost({
    parameter: { action: 'webhook' },
    headers: { 'X-Razorpay-Signature': sig2 },
    postData: { contents: body2 },
  });

  // Event 3: Client verify-payment
  const paySig = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET)
    .update(`${createResp.order_id}|${paymentId}`)
    .digest('hex');
  context.doPost({
    postData: {
      contents: JSON.stringify({
        action: 'verify-payment',
        razorpay_order_id: createResp.order_id,
        razorpay_payment_id: paymentId,
        razorpay_signature: paySig,
        internal_id: createResp.internal_id,
        publicDisplayOptIn: true,
      }),
    },
  });

  // Check Customers: Total Payments MUST be strictly 1, not 3!
  const custSheet = mockSpreadsheet.getSheetByName('Customers');
  assert.equal(custSheet.grid.length, 2);
  assert.equal(custSheet.grid[1][7], 1); // Total Payments = 1
  assert.equal(custSheet.grid[1][8], 'EUR 50.00');

  // Check PublicSupport: Strictly 1 row, not 3!
  const pubSheet = mockSpreadsheet.getSheetByName('PublicSupport');
  assert.equal(pubSheet.grid.length, 2);
});

// 7. Multi-Currency Customer Aggregation Isolation
runTest('Multi-currency contributions by same patron preserve per-currency totals', () => {
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();

  const patronEmail = 'global.patron@example.com';
  const patronName = 'Global Patron';

  const payments = [
    { amount: '500', currency: 'INR' },
    { amount: '25.00', currency: 'USD' },
    { amount: '20.00', currency: 'EUR' },
    { amount: '15.00', currency: 'GBP' },
  ];

  for (let i = 0; i < payments.length; i++) {
    const p = payments[i];
    const ord = JSON.parse(context.doPost({
      postData: {
        contents: JSON.stringify({
          action: 'create-order',
          amount: p.amount,
          currency: p.currency,
          customer_name: patronName,
          customer_email: patronEmail,
          publicDisplayOptIn: true,
        }),
      },
    }).getContent());

    const payId = 'pay_multi_' + i;
    const sig = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET)
      .update(`${ord.order_id}|${payId}`)
      .digest('hex');

    context.doPost({
      postData: {
        contents: JSON.stringify({
          action: 'verify-payment',
          razorpay_order_id: ord.order_id,
          razorpay_payment_id: payId,
          razorpay_signature: sig,
          internal_id: ord.internal_id,
          publicDisplayOptIn: true,
        }),
      },
    });
  }

  const custSheet = mockSpreadsheet.getSheetByName('Customers');
  assert.equal(custSheet.grid.length, 2); // Exactly 1 customer profile
  const row = custSheet.grid[1];
  assert.equal(row[2], patronEmail);
  assert.equal(row[7], 4); // Total Payments: 4
  // Must NOT combine into numerical addition!
  assert.equal(row[8], 'EUR 20.00, GBP 15.00, INR 500.00, USD 25.00');
  assert.equal(row[9], 'INR, USD, EUR, GBP');
});

// 8. Refund Webhook Handling
runTest('Refund webhook creates Refunds entry and updates Payments without altering customer payments', () => {
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();

  // Create & verify payment
  const ord = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '100', currency: 'USD', customer_email: 'refundee@example.com' }) }
  }).getContent());

  const payId = 'pay_to_refund_99';
  const sig = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET).update(`${ord.order_id}|${payId}`).digest('hex');
  context.doPost({
    postData: { contents: JSON.stringify({ action: 'verify-payment', razorpay_order_id: ord.order_id, razorpay_payment_id: payId, razorpay_signature: sig }) }
  });

  // Refund Webhook
  const refundBody = JSON.stringify({
    event: 'refund.processed',
    event_id: 'evt_refund_99',
    payload: {
      refund: {
        entity: {
          id: 'rfnd_test_99',
          payment_id: payId,
          amount: 10000,
          currency: 'USD',
          status: 'processed',
          notes: { reason: 'accidental_duplicate' },
        },
      },
    },
  });
  const hookSig = crypto.createHmac('sha256', scriptProperties.RAZORPAY_WEBHOOK_SECRET).update(refundBody).digest('hex');
  context.doPost({
    parameter: { action: 'webhook' },
    headers: { 'X-Razorpay-Signature': hookSig },
    postData: { contents: refundBody },
  });

  // Verify Refunds tab
  const refSheet = mockSpreadsheet.getSheetByName('Refunds');
  assert.equal(refSheet.grid.length, 2);
  assert.equal(refSheet.grid[1][1], 'rfnd_test_99');
  assert.equal(refSheet.grid[1][2], payId);
  assert.equal(refSheet.grid[1][4], 100);

  // Verify Payments tab status
  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  assert.equal(paySheet.grid[1][16], 'refunded'); // Refund Status

  // Customer payments count remains 1 (refund does not create fake customer payment)
  const custSheet = mockSpreadsheet.getSheetByName('Customers');
  assert.equal(custSheet.grid[1][7], 1);
});

// 9. Frontend Checkout Dismissal (report-cancel)
runTest('Frontend Checkout Dismissal updates Payments tab to CANCELLED without adding customer or public supporter', () => {
  const { context, mockSpreadsheet } = createMockEnvironment();

  // Create order
  const createResp = JSON.parse(context.doPost({
    postData: {
      contents: JSON.stringify({
        action: 'create-order',
        amount: '15.00',
        currency: 'USD',
        customer_name: 'David Miller',
        customer_email: 'david@example.com',
        publicDisplayOptIn: true,
      }),
    },
  }).getContent());

  assert.equal(createResp.success, true);
  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  assert.equal(paySheet.grid[1][20], 'PENDING');

  // Patron dismisses checkout modal
  const cancelResp = JSON.parse(context.doPost({
    postData: {
      contents: JSON.stringify({
        action: 'report-cancel',
        order_id: createResp.order_id,
        internal_id: createResp.internal_id,
        reason: 'Modal dismissed by user',
      }),
    },
  }).getContent());

  assert.equal(cancelResp.success, true);
  assert.equal(cancelResp.payment_result, 'CANCELLED');
  assert.equal(paySheet.grid[1][4], 'cancelled');
  assert.equal(paySheet.grid[1][20], 'CANCELLED');
  assert.equal(paySheet.grid[1][21], ''); // Completed At remains empty
  assert.equal(paySheet.grid[1][22], 'Modal dismissed by user');

  // Must NOT create customer or public supporter
  const custSheet = mockSpreadsheet.getSheetByName('Customers');
  assert.equal(custSheet.grid.length, 1); // Only header
  const pubSheet = mockSpreadsheet.getSheetByName('PublicSupport');
  assert.equal(pubSheet.grid.length, 1); // Only header
});

// 10. Frontend Payment Failure (report-failure)
runTest('Frontend Payment Failure updates Payments tab to FAILED with explicit failure reason', () => {
  const { context, mockSpreadsheet } = createMockEnvironment();

  // Create order
  const createResp = JSON.parse(context.doPost({
    postData: {
      contents: JSON.stringify({
        action: 'create-order',
        amount: '1200',
        currency: 'INR',
        customer_name: 'Anita Roy',
        customer_email: 'anita@example.com',
      }),
    },
  }).getContent());

  // Payment fails at gateway / modal reports payment.failed
  const failResp = JSON.parse(context.doPost({
    postData: {
      contents: JSON.stringify({
        action: 'report-failure',
        order_id: createResp.order_id,
        internal_id: createResp.internal_id,
        reason: 'Payment failed at bank gateway: Insufficient funds in account',
      }),
    },
  }).getContent());

  assert.equal(failResp.success, true);
  assert.equal(failResp.payment_result, 'FAILED');

  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  assert.equal(paySheet.grid[1][4], 'failed');
  assert.equal(paySheet.grid[1][20], 'FAILED');
  assert.equal(paySheet.grid[1][21], '');
  assert.equal(paySheet.grid[1][22], 'Payment failed at bank gateway: Insufficient funds in account');
});

// 11. PaymentSummary Tab Segregated Currency Totals & Transaction Counters
runTest('PaymentSummary tab calculates accurate counters and isolates currency totals', () => {
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();

  // 1. Success 1 (INR 500)
  const o1 = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '500', currency: 'INR' }) }
  }).getContent());
  const s1 = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET).update(`${o1.order_id}|pay_11_1`).digest('hex');
  context.doPost({
    postData: { contents: JSON.stringify({ action: 'verify-payment', razorpay_order_id: o1.order_id, razorpay_payment_id: 'pay_11_1', razorpay_signature: s1, internal_id: o1.internal_id }) }
  });

  // 2. Success 2 (USD 50)
  const o2 = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '50', currency: 'USD' }) }
  }).getContent());
  const s2 = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET).update(`${o2.order_id}|pay_11_2`).digest('hex');
  context.doPost({
    postData: { contents: JSON.stringify({ action: 'verify-payment', razorpay_order_id: o2.order_id, razorpay_payment_id: 'pay_11_2', razorpay_signature: s2, internal_id: o2.internal_id }) }
  });

  // 3. Pending 1 (EUR 20)
  context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '20', currency: 'EUR' }) }
  });

  // 4. Cancelled 1 (GBP 15)
  const o4 = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '15', currency: 'GBP' }) }
  }).getContent());
  context.doPost({
    postData: { contents: JSON.stringify({ action: 'report-cancel', order_id: o4.order_id, internal_id: o4.internal_id, reason: 'Patron closed modal' }) }
  });

  const sumSheet = mockSpreadsheet.getSheetByName('PaymentSummary');
  assert.ok(sumSheet, 'PaymentSummary sheet must exist');
  const metrics = {};
  for (let r = 1; r < sumSheet.grid.length; r++) {
    metrics[sumSheet.grid[r][0]] = sumSheet.grid[r][1];
  }

  assert.equal(metrics['Successful Payments'], 2);
  assert.equal(metrics['Pending Payments'], 1);
  assert.equal(metrics['Cancelled Payments'], 1);
  assert.equal(metrics['Failed Payments'], 0);
  assert.ok(metrics['Total Successful Amount by Currency'].includes('INR 500.00'));
  assert.ok(metrics['Total Successful Amount by Currency'].includes('USD 50.00'));
  // Never numerically aggregated across disparate currencies
  assert.ok(!metrics['Total Successful Amount by Currency'].includes('550'));
});

console.log('-------------------------------------------------------');
console.log(`Results: ${passed} passed, 0 failed out of ${total} E2E gates.`);
console.log('=======================================================');

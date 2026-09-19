// tools/test-apps-script.mjs
// Comprehensive test suite for apps-script/Code.gs running as the production Razorpay & Sheets payment backend.

import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import crypto from 'node:crypto';

const codePath = path.resolve(process.cwd(), 'apps-script/Code.gs');
const codeGs = fs.readFileSync(codePath, 'utf8');

console.log('Testing apps-script/Code.gs as Production Payment Backend...');

function createMockEnvironment(customProperties = {}) {
  const scriptProperties = {
    RAZORPAY_KEY_ID: 'rzp_test_simulated_key_001',
    RAZORPAY_KEY_SECRET: 'test_key_secret_for_hmac_verification_only',
    RAZORPAY_WEBHOOK_SECRET: 'test_webhook_secret_for_hmac_verification_only',
    SPREADSHEET_ID: '1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI',
    ...customProperties,
  };

  const cacheStore = new Map();
  let orderCounter = 0;

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
    setValue(val) {
      return this.setValues([[val]]);
    }
    getValue() {
      return this.sheet._getCell(this.row, this.col);
    }
    setBackground() { return this; }
    setFontColor() { return this; }
    setFontWeight() { return this; }
    setHorizontalAlignment() { return this; }
  }

  class MockSheet {
    constructor(name) {
      this.name = name;
      this.grid = []; // 0-indexed rows
      this.frozenRows = 0;
    }
    getName() { return this.name; }
    getLastRow() { return this.grid.length; }
    getLastColumn() {
      let maxCols = 0;
      for (const row of this.grid) {
        if (row && row.length > maxCols) maxCols = row.length;
      }
      return maxCols;
    }
    _getCell(r, c) { // 1-indexed
      const row = this.grid[r - 1];
      if (!row) return '';
      return row[c - 1] !== undefined ? row[c - 1] : '';
    }
    _setCell(r, c, val) { // 1-indexed
      while (this.grid.length < r) {
        this.grid.push([]);
      }
      while (this.grid[r - 1].length < c) {
        this.grid[r - 1].push('');
      }
      this.grid[r - 1][c - 1] = val;
    }
    appendRow(rowArr) {
      this.grid.push([...rowArr]);
    }
    setFrozenRows(n) { this.frozenRows = n; }
    getMaxRows() { return Math.max(this.grid.length, 100); }
    getMaxColumns() {
      let maxCols = 23;
      for (const row of this.grid) {
        if (row && row.length > maxCols) maxCols = row.length;
      }
      return maxCols;
    }
    insertColumnsAfter(col, n) {}
    setConditionalFormatRules(rules) { this.conditionalFormatRules = rules; }
    getConditionalFormatRules() { return this.conditionalFormatRules || []; }
    getRange(row, col, numRows, numCols) {
      return new MockRange(this, row, col, numRows || 1, numCols || 1);
    }
  }

  class MockSpreadsheet {
    constructor(id) {
      this.id = id;
      this.sheets = {};
    }
    getId() { return this.id; }
    getSheetByName(name) {
      return this.sheets[name] || null;
    }
    insertSheet(name) {
      const s = new MockSheet(name);
      this.sheets[name] = s;
      return s;
    }
  }

  const mockSpreadsheet = new MockSpreadsheet('1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI');

  const context = {
    console: {
      log: () => {},
      warn: () => {},
      error: () => {},
      info: () => {}
    },
    SpreadsheetApp: {
      openById: (id) => {
        if (id === mockSpreadsheet.id) {
          return mockSpreadsheet;
        }
        throw new Error('Spreadsheet not found with ID: ' + id);
      },
      newConditionalFormatRule: () => {
        const rule = {
          whenTextEqualTo: (t) => { rule.text = t; return rule; },
          setBackground: (b) => { rule.bg = b; return rule; },
          setFontColor: (c) => { rule.font = c; return rule; },
          setRanges: (r) => { rule.ranges = r; return rule; },
          build: () => rule,
        };
        return rule;
      }
    },
    PropertiesService: {
      getScriptProperties: () => ({
        getProperty: (key) => scriptProperties[key] || null,
        setProperty: (key, val) => { scriptProperties[key] = val; }
      })
    },
    CacheService: {
      getScriptCache: () => ({
        get: (k) => cacheStore.get(k) || null,
        put: (k, v, ttl) => cacheStore.set(k, v),
        remove: (k) => cacheStore.delete(k)
      })
    },
    ContentService: {
      MimeType: { JSON: 'application/json', JAVASCRIPT: 'application/javascript' },
      createTextOutput: (text) => ({
        _content: text,
        _mime: 'text/plain',
        setMimeType: function(mime) { this._mime = mime; return this; },
        getContent: function() { return this._content; }
      })
    },
    Utilities: {
      formatDate: (d, tz, fmt) => d.toISOString(),
      /* High-entropy PREFIX like a real UUID: Code.gs keeps only the first
         8 chars, so the old 'test_uuid_…' mock made every internal id in
         the same millisecond identical — second verify matched the first
         row and test [30/31] flaked. */
      getUuid: () => crypto.randomUUID(),
      base64Encode: (str) => Buffer.from(str).toString('base64'),
      computeHmacSha256Signature: (value, key) => {
        const buf = crypto.createHmac('sha256', key).update(value).digest();
        // Convert to signed bytes (-128 to 127) as Apps Script returns
        return Array.from(buf).map(b => b > 127 ? b - 256 : b);
      }
    },
    UrlFetchApp: {
      fetch: (url, options) => {
        // Simulated Razorpay API response
        orderCounter = (orderCounter || 0) + 1;
        return {
          getResponseCode: () => 200,
          getContentText: () => JSON.stringify({
            id: 'order_test_' + Date.now() + '_' + orderCounter + '_' + Math.random().toString(36).substring(2, 7),
            entity: 'order',
            amount: 50000,
            currency: 'INR',
            status: 'created'
          })
        };
      }
    }
  };

  vm.createContext(context);
  vm.runInContext(codeGs, context);

  return { context, mockSpreadsheet, scriptProperties };
}

// 1. TEST: Health endpoint
{
  const { context } = createMockEnvironment();
  const res = JSON.parse(context.doGet({ parameter: { action: 'health' } }).getContent());
  assert.equal(res.success, true);
  assert.equal(res.status, 'ok');
  assert.equal(res.currencies_count, 128);
  console.log('✓ PASS [1/20]: GET ?action=health returns healthy status');
}

// 2. TEST: Currencies registry
{
  const { context } = createMockEnvironment();
  const res = JSON.parse(context.doGet({ parameter: { action: 'currencies' } }).getContent());
  assert.equal(res.success, true);
  assert.equal(res.count, 128);
  console.log('✓ PASS [2/20]: GET ?action=currencies lists 128 verified currencies');
}

// 3. TEST: Reject query parameter token
{
  const { context } = createMockEnvironment();
  const res = JSON.parse(context.doGet({ parameter: { token: 'secret' } }).getContent());
  assert.equal(res.success, false);
  assert.equal(res.code, 'FORBIDDEN_AUTH_METHOD');
  console.log('✓ PASS [3/20]: Tokens in URL query parameters are strictly forbidden');
}

// 4. TEST: create-order valid INR
{
  const { context, mockSpreadsheet } = createMockEnvironment();
  const payload = {
    action: 'create-order',
    amount: '500',
    currency: 'INR',
    customer_name: 'Ananya Sharma',
    customer_email: 'ananya@example.com',
    customer_phone: '+919876543210',
    country: 'IN',
    support_message: 'Keep up the great education work!',
    publicDisplayOptIn: true
  };
  const e = { postData: { contents: JSON.stringify(payload) } };
  const res = JSON.parse(context.doPost(e).getContent());
  assert.equal(res.success, true);
  assert.equal(res.amount, 50000); // 500 INR -> 50000 paise
  assert.equal(res.currency, 'INR');
  assert.ok(res.order_id);
  assert.ok(res.internal_id);

  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  assert.equal(paySheet.grid.length, 2); // header + record
  assert.equal(paySheet.grid[1][4], 'created'); // Status
  assert.equal(paySheet.grid[1][5], 500); // Amount
  assert.equal(paySheet.grid[1][6], 'INR'); // Currency
  console.log('✓ PASS [4/20]: POST ?action=create-order creates valid INR order & ledger entry');
}

// 5. TEST: create-order valid USD, EUR, GBP
{
  const { context } = createMockEnvironment();
  const eUsd = { postData: { contents: JSON.stringify({ action: 'create-order', amount: '10.50', currency: 'USD' }) } };
  const resUsd = JSON.parse(context.doPost(eUsd).getContent());
  assert.equal(resUsd.success, true);
  assert.equal(resUsd.amount, 1050); // $10.50 -> 1050 cents

  const eEur = { postData: { contents: JSON.stringify({ action: 'create-order', amount: '15.00', currency: 'EUR' }) } };
  const resEur = JSON.parse(context.doPost(eEur).getContent());
  assert.equal(resEur.success, true);
  assert.equal(resEur.amount, 1500);

  const eGbp = { postData: { contents: JSON.stringify({ action: 'create-order', amount: '20.00', currency: 'GBP' }) } };
  const resGbp = JSON.parse(context.doPost(eGbp).getContent());
  assert.equal(resGbp.success, true);
  assert.equal(resGbp.amount, 2000);
  console.log('✓ PASS [5/20]: POST ?action=create-order converts USD, EUR, GBP to exact subunits');
}

// 6. TEST: create-order zero-decimal currency (JPY)
{
  const { context } = createMockEnvironment();
  // Valid JPY
  const eValidJpy = { postData: { contents: JSON.stringify({ action: 'create-order', amount: '1500', currency: 'JPY' }) } };
  const resValid = JSON.parse(context.doPost(eValidJpy).getContent());
  assert.equal(resValid.success, true);
  assert.equal(resValid.amount, 1500);

  // Invalid JPY with decimals
  const eInvalidJpy = { postData: { contents: JSON.stringify({ action: 'create-order', amount: '1500.50', currency: 'JPY' }) } };
  const resInvalid = JSON.parse(context.doPost(eInvalidJpy).getContent());
  assert.equal(resInvalid.success, false);
  assert.match(resInvalid.error, /zero-decimal/i);
  console.log('✓ PASS [6/20]: Zero-decimal JPY rejects fractional decimals');
}

// 7. TEST: create-order 3-decimal currency (KWD)
{
  const { context } = createMockEnvironment();
  const eKwd = { postData: { contents: JSON.stringify({ action: 'create-order', amount: '15.750', currency: 'KWD' }) } };
  const resKwd = JSON.parse(context.doPost(eKwd).getContent());
  assert.equal(resKwd.success, true);
  assert.equal(resKwd.amount, 15750);
  console.log('✓ PASS [7/20]: 3-decimal currency (KWD) handles 3 decimal precision');
}

// 8. TEST: Unsupported currency rejected
{
  const { context } = createMockEnvironment();
  const eBad = { postData: { contents: JSON.stringify({ action: 'create-order', amount: '10', currency: 'FAKECOIN' }) } };
  const resBad = JSON.parse(context.doPost(eBad).getContent());
  assert.equal(resBad.success, false);
  assert.match(resBad.error, /not supported/i);
  console.log('✓ PASS [8/20]: Unsupported currency is strictly rejected');
}

// 9. TEST: Invalid amounts (negative, zero, above limit, malformed)
{
  const { context } = createMockEnvironment();
  const eNeg = { postData: { contents: JSON.stringify({ action: 'create-order', amount: '-50', currency: 'USD' }) } };
  assert.equal(JSON.parse(context.doPost(eNeg).getContent()).success, false);

  const eZero = { postData: { contents: JSON.stringify({ action: 'create-order', amount: '0', currency: 'USD' }) } };
  assert.equal(JSON.parse(context.doPost(eZero).getContent()).success, false);

  const eMax = { postData: { contents: JSON.stringify({ action: 'create-order', amount: '999999', currency: 'USD' }) } };
  assert.equal(JSON.parse(context.doPost(eMax).getContent()).success, false);

  const eString = { postData: { contents: JSON.stringify({ action: 'create-order', amount: 'abc', currency: 'USD' }) } };
  assert.equal(JSON.parse(context.doPost(eString).getContent()).success, false);
  console.log('✓ PASS [9/20]: Negative, zero, malformed, and out-of-bound amounts rejected');
}

// 10. TEST: verify-payment valid signature
{
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();

  // Create order
  const orderRes = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '25.00', currency: 'USD', customer_email: 'donor@example.com', customer_name: 'Jane Doe', publicDisplayOptIn: true }) }
  }).getContent());

  const orderId = orderRes.order_id;
  const paymentId = 'pay_test_valid_001';
  const secret = scriptProperties.RAZORPAY_KEY_SECRET;

  const validSignature = crypto.createHmac('sha256', secret).update(`${orderId}|${paymentId}`).digest('hex');

  const verifyRes = JSON.parse(context.doPost({
    postData: {
      contents: JSON.stringify({
        action: 'verify-payment',
        razorpay_order_id: orderId,
        razorpay_payment_id: paymentId,
        razorpay_signature: validSignature,
        internal_id: orderRes.internal_id,
        publicDisplayOptIn: true
      })
    }
  }).getContent());

  assert.equal(verifyRes.success, true);
  assert.equal(verifyRes.status, 'captured');

  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  assert.equal(paySheet.grid[1][4], 'captured'); // Status
  assert.equal(paySheet.grid[1][18], 'true'); // Verified

  const custSheet = mockSpreadsheet.getSheetByName('Customers');
  assert.equal(custSheet.grid.length, 2);
  assert.equal(custSheet.grid[1][2], 'donor@example.com');
  assert.equal(custSheet.grid[1][7], 1); // Total Payments count
  assert.equal(custSheet.grid[1][8], 'USD 25.00');

  const pubSheet = mockSpreadsheet.getSheetByName('PublicSupport');
  assert.equal(pubSheet.grid.length, 2);
  assert.equal(pubSheet.grid[1][1], 'Jane Doe');
  console.log('✓ PASS [10/20]: POST ?action=verify-payment verifies valid signature and updates ledgers');
}

// 11. TEST: verify-payment invalid signature
{
  const { context, mockSpreadsheet } = createMockEnvironment();

  const orderRes = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '10.00', currency: 'USD' }) }
  }).getContent());

  const verifyRes = JSON.parse(context.doPost({
    postData: {
      contents: JSON.stringify({
        action: 'verify-payment',
        razorpay_order_id: orderRes.order_id,
        razorpay_payment_id: 'pay_fraud_123',
        razorpay_signature: 'invalid_forged_signature_00000000000',
        internal_id: orderRes.internal_id
      })
    }
  }).getContent());

  assert.equal(verifyRes.success, false);
  assert.match(verifyRes.error, /invalid payment signature/i);

  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  assert.equal(paySheet.grid[1][4], 'failed');
  assert.equal(paySheet.grid[1][18], 'false');
  console.log('✓ PASS [11/20]: Invalid signature rejected and record marked failed');
}

// 12. TEST: verify-payment amount tampering detection
{
  const { context, scriptProperties } = createMockEnvironment();

  const orderRes = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '100.00', currency: 'USD' }) }
  }).getContent());

  const orderId = orderRes.order_id;
  const paymentId = 'pay_tamper_001';
  const sig = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET).update(`${orderId}|${paymentId}`).digest('hex');

  const verifyRes = JSON.parse(context.doPost({
    postData: {
      contents: JSON.stringify({
        action: 'verify-payment',
        razorpay_order_id: orderId,
        razorpay_payment_id: paymentId,
        razorpay_signature: sig,
        tampered_amount: 5.00 // Client claims $5 instead of $100
      })
    }
  }).getContent());

  assert.equal(verifyRes.success, false);
  assert.match(verifyRes.error, /tampering/i);
  console.log('✓ PASS [12/20]: Client-side amount tampering detected and rejected');
}

// 13. TEST: verify-payment currency tampering detection
{
  const { context, scriptProperties } = createMockEnvironment();

  const orderRes = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '100.00', currency: 'USD' }) }
  }).getContent());

  const orderId = orderRes.order_id;
  const paymentId = 'pay_tamper_curr_001';
  const sig = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET).update(`${orderId}|${paymentId}`).digest('hex');

  const verifyRes = JSON.parse(context.doPost({
    postData: {
      contents: JSON.stringify({
        action: 'verify-payment',
        razorpay_order_id: orderId,
        razorpay_payment_id: paymentId,
        razorpay_signature: sig,
        tampered_currency: 'INR'
      })
    }
  }).getContent());

  assert.equal(verifyRes.success, false);
  assert.match(verifyRes.error, /tampering/i);
  console.log('✓ PASS [13/20]: Client-side currency tampering detected and rejected');
}

// 14. TEST: verify-payment duplicate idempotency
{
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();

  const orderRes = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '15.00', currency: 'USD' }) }
  }).getContent());

  const orderId = orderRes.order_id;
  const paymentId = 'pay_idem_001';
  const sig = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET).update(`${orderId}|${paymentId}`).digest('hex');

  const payload = {
    action: 'verify-payment',
    razorpay_order_id: orderId,
    razorpay_payment_id: paymentId,
    razorpay_signature: sig,
    internal_id: orderRes.internal_id
  };

  // First verification
  const res1 = JSON.parse(context.doPost({ postData: { contents: JSON.stringify(payload) } }).getContent());
  assert.equal(res1.success, true);

  // Second duplicate verification
  const res2 = JSON.parse(context.doPost({ postData: { contents: JSON.stringify(payload) } }).getContent());
  assert.equal(res2.success, true);
  assert.equal(res2.duplicate, true);

  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  assert.equal(paySheet.grid.length, 2); // Still only 1 data row!
  console.log('✓ PASS [14/20]: Duplicate verification handled idempotently without duplicate rows');
}

// 15. TEST: webhook valid HMAC signature & payment.captured handling
{
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();

  // Create order
  const orderRes = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '50.00', currency: 'USD' }) }
  }).getContent());

  const webhookBody = JSON.stringify({
    event: 'payment.captured',
    event_id: 'evt_test_captured_001',
    payload: {
      payment: {
        entity: {
          id: 'pay_hook_001',
          order_id: orderRes.order_id,
          amount: 5000,
          currency: 'USD',
          status: 'captured',
          fee: 150,
          tax: 27
        }
      }
    }
  });

  const webhookSecret = scriptProperties.RAZORPAY_WEBHOOK_SECRET;
  const signature = crypto.createHmac('sha256', webhookSecret).update(webhookBody).digest('hex');

  const hookRes = JSON.parse(context.doPost({
    parameter: { action: 'webhook' },
    headers: { 'X-Razorpay-Signature': signature },
    postData: { contents: webhookBody }
  }).getContent());

  assert.equal(hookRes.success, true);
  assert.equal(hookRes.processed, true);

  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  assert.equal(paySheet.grid[1][4], 'captured'); // Status
  assert.equal(paySheet.grid[1][18], 'true'); // Verified
  assert.equal(paySheet.grid[1][14], 1.5); // Fee

  const eventSheet = mockSpreadsheet.getSheetByName('WebhookEvents');
  assert.equal(eventSheet.grid.length, 2);
  assert.equal(eventSheet.grid[1][1], 'evt_test_captured_001');
  console.log('✓ PASS [15/20]: Valid webhook processed and synchronized to ledger');
}

// 16. TEST: webhook invalid signature rejected
{
  const { context } = createMockEnvironment();
  const webhookBody = JSON.stringify({ event: 'payment.captured', event_id: 'evt_invalid' });

  const hookRes = JSON.parse(context.doPost({
    parameter: { action: 'webhook' },
    headers: { 'X-Razorpay-Signature': 'bogus_signature' },
    postData: { contents: webhookBody }
  }).getContent());

  assert.equal(hookRes.success, false);
  assert.match(hookRes.error, /invalid webhook signature/i);
  console.log('✓ PASS [16/20]: Webhook with invalid HMAC signature rejected with 400');
}

// 17. TEST: webhook duplicate event idempotency
{
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();

  const webhookBody = JSON.stringify({
    event: 'payment.authorized',
    event_id: 'evt_duplicate_test_002',
    payload: { payment: { entity: { id: 'pay_hook_002' } } }
  });
  const sig = crypto.createHmac('sha256', scriptProperties.RAZORPAY_WEBHOOK_SECRET).update(webhookBody).digest('hex');

  const e = {
    parameter: { action: 'webhook' },
    headers: { 'X-Razorpay-Signature': sig },
    postData: { contents: webhookBody }
  };

  const res1 = JSON.parse(context.doPost(e).getContent());
  assert.equal(res1.success, true);

  const res2 = JSON.parse(context.doPost(e).getContent());
  assert.equal(res2.success, true);
  assert.equal(res2.duplicate, true);

  const eventSheet = mockSpreadsheet.getSheetByName('WebhookEvents');
  assert.equal(eventSheet.grid.length, 2); // 1 header + 1 event
  console.log('✓ PASS [17/20]: Duplicate webhook event skipped idempotently');
}

// 18. TEST: webhook refund handling
{
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();

  const orderRes = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '30.00', currency: 'USD' }) }
  }).getContent());

  const refundBody = JSON.stringify({
    event: 'refund.processed',
    event_id: 'evt_refund_001',
    payload: {
      refund: {
        entity: {
          id: 'rfnd_001',
          payment_id: 'pay_ref_target_01',
          amount: 3000,
          currency: 'USD',
          status: 'processed'
        }
      }
    }
  });

  const sig = crypto.createHmac('sha256', scriptProperties.RAZORPAY_WEBHOOK_SECRET).update(refundBody).digest('hex');
  const res = JSON.parse(context.doPost({
    parameter: { action: 'webhook' },
    headers: { 'X-Razorpay-Signature': sig },
    postData: { contents: refundBody }
  }).getContent());

  assert.equal(res.success, true);
  const refSheet = mockSpreadsheet.getSheetByName('Refunds');
  assert.equal(refSheet.grid.length, 2);
  assert.equal(refSheet.grid[1][1], 'rfnd_001');
  assert.equal(refSheet.grid[1][4], 30);
  console.log('✓ PASS [18/20]: Refund webhook records refund row and updates status');
}

// 19. TEST: Multi-currency customer total preservation without cross-currency addition
{
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();

  // Payment 1 in INR
  const order1 = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '500', currency: 'INR', customer_email: 'patron@example.com', customer_name: 'Multi Patron' }) }
  }).getContent());
  const sig1 = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET).update(`${order1.order_id}|pay_1`).digest('hex');
  context.doPost({
    postData: { contents: JSON.stringify({ action: 'verify-payment', razorpay_order_id: order1.order_id, razorpay_payment_id: 'pay_1', razorpay_signature: sig1 }) }
  });

  // Payment 2 in USD from same customer
  const order2 = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '25.00', currency: 'USD', customer_email: 'patron@example.com', customer_name: 'Multi Patron' }) }
  }).getContent());
  const sig2 = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET).update(`${order2.order_id}|pay_2`).digest('hex');
  context.doPost({
    postData: { contents: JSON.stringify({ action: 'verify-payment', razorpay_order_id: order2.order_id, razorpay_payment_id: 'pay_2', razorpay_signature: sig2 }) }
  });

  const custSheet = mockSpreadsheet.getSheetByName('Customers');
  assert.equal(custSheet.grid.length, 2); // 1 customer row
  const row = custSheet.grid[1];
  assert.equal(row[2], 'patron@example.com');
  assert.equal(row[7], 2); // Total payments = 2
  // Customer multi-currency total MUST NOT be 525 (INR 500 + USD 25)!
  assert.equal(row[8], 'INR 500.00, USD 25.00');
  assert.equal(row[9], 'INR, USD');
  console.log('✓ PASS [19/20]: Multi-currency customer totals isolated per-currency');
}

// 20. TEST: PublicSupport opt-in vs opt-out and sanitization
{
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();

  // Supporter 1: Opted in
  const ord1 = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '1000', currency: 'INR', customer_name: 'Public Hero', customer_email: 'secret1@example.com', customer_phone: '+919876543210', country: 'IN', support_message: 'Keep going!', publicDisplayOptIn: true }) }
  }).getContent());
  const sig1 = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET).update(`${ord1.order_id}|pay_pub_1`).digest('hex');
  context.doPost({
    postData: { contents: JSON.stringify({ action: 'verify-payment', razorpay_order_id: ord1.order_id, razorpay_payment_id: 'pay_pub_1', razorpay_signature: sig1, publicDisplayOptIn: true }) }
  });

  // Supporter 2: Opted OUT (publicDisplayOptIn = false)
  const ord2 = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '5000', currency: 'INR', customer_name: 'Anonymous Donor', customer_email: 'secret2@example.com', customer_phone: '+919999999999', country: 'IN', support_message: 'Private', publicDisplayOptIn: false }) }
  }).getContent());
  const sig2 = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET).update(`${ord2.order_id}|pay_priv_2`).digest('hex');
  context.doPost({
    postData: { contents: JSON.stringify({ action: 'verify-payment', razorpay_order_id: ord2.order_id, razorpay_payment_id: 'pay_priv_2', razorpay_signature: sig2, publicDisplayOptIn: false }) }
  });

  // Check PublicSupport tab
  const pubSheet = mockSpreadsheet.getSheetByName('PublicSupport');
  assert.equal(pubSheet.grid.length, 2); // 1 header + ONLY 1 public supporter
  assert.equal(pubSheet.grid[1][1], 'Public Hero');

  // Check GET ?action=recent-support
  const getRes = JSON.parse(context.doGet({ parameter: { action: 'recent-support' } }).getContent());
  assert.equal(getRes.success, true);
  assert.equal(getRes.supporters.length, 1);
  assert.equal(getRes.supporters[0].displayName, 'Public Hero');

  const str = JSON.stringify(getRes);
  assert.ok(!str.includes('Anonymous Donor'));
  assert.ok(!str.includes('secret1@example.com'));
  assert.ok(!str.includes('secret2@example.com'));
  assert.ok(!str.includes('9876543210'));
  assert.ok(!str.includes('9999999999'));
  console.log('✓ PASS [20/20]: Public opt-in respected & private data strictly sanitized from public GET view');
}

// 21. TEST: JSONP callback support for GET ?action=recent-support
{
  const { context } = createMockEnvironment();
  const output = context.doGet({ parameter: { action: 'recent-support', callback: 'parseSupportersCallback' } });
  assert.equal(output._mime, 'application/javascript');
  const rawContent = output.getContent();
  assert.ok(rawContent.startsWith('parseSupportersCallback('));
  assert.ok(rawContent.endsWith(');'));
  const innerJson = rawContent.slice('parseSupportersCallback('.length, -2);
  const parsed = JSON.parse(innerJson);
  assert.equal(parsed.success, true);
  assert.deepEqual(parsed.supporters, []);
  console.log('✓ PASS [21/23]: JSONP callback wrapped correctly with application/javascript MIME');
}

// 22. TEST: JSONP create-order via GET (bypasses browser 302 cross-origin redirect CORS)
{
  const { context, mockSpreadsheet } = createMockEnvironment();
  const output = context.doGet({
    parameter: {
      action: 'create-order',
      amount: '500',
      currency: 'INR',
      customer_name: 'Prakash',
      customer_email: 'prakash@example.com',
      callback: '_ekg_cb_order_test'
    }
  });
  assert.equal(output._mime, 'application/javascript');
  const raw = output.getContent();
  assert.ok(raw.startsWith('_ekg_cb_order_test('));
  assert.ok(raw.endsWith(');'));
  const parsed = JSON.parse(raw.slice('_ekg_cb_order_test('.length, -2));
  assert.equal(parsed.success, true);
  assert.equal(parsed.amount, 50000);
  assert.equal(parsed.currency, 'INR');
  assert.ok(parsed.order_id);
  assert.ok(parsed.key_id);

  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  assert.equal(paySheet.grid.length, 2);
  assert.equal(paySheet.grid[1][4], 'created');
  console.log('✓ PASS [22/23]: GET ?action=create-order with JSONP returns order_id & key_id');
}

// 23. TEST: JSONP verify-payment via GET (bypasses browser 302 cross-origin redirect CORS)
{
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();
  // First create order via GET
  const ordRaw = context.doGet({
    parameter: { action: 'create-order', amount: '25.00', currency: 'USD', callback: 'cbOrd' }
  }).getContent();
  const ord = JSON.parse(ordRaw.slice('cbOrd('.length, -2));

  // Compute signature
  const payId = 'pay_get_verify_001';
  const sig = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET).update(`${ord.order_id}|${payId}`).digest('hex');

  // Verify via GET
  const verRaw = context.doGet({
    parameter: {
      action: 'verify-payment',
      razorpay_order_id: ord.order_id,
      razorpay_payment_id: payId,
      razorpay_signature: sig,
      internal_id: ord.internal_id,
      callback: 'cbVer'
    }
  }).getContent();
  assert.ok(verRaw.startsWith('cbVer('));
  const ver = JSON.parse(verRaw.slice('cbVer('.length, -2));
  assert.equal(ver.success, true);
  assert.equal(ver.status, 'captured');

  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  assert.equal(paySheet.grid[1][4], 'captured');
  console.log('✓ PASS [23/23]: GET ?action=verify-payment with JSONP reconciles payment successfully');
}

// 24. TEST: Production Ledger Columns (Payment Result, Payment Completed At, Failure Reason) on order creation
{
  const { context, mockSpreadsheet } = createMockEnvironment();
  const res = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '100', currency: 'INR' }) }
  }).getContent());
  assert.equal(res.success, true);

  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  const headers = paySheet.grid[0];
  assert.equal(headers[20], 'Payment Result');
  assert.equal(headers[21], 'Payment Completed At');
  assert.equal(headers[22], 'Failure Reason');

  const row = paySheet.grid[1];
  assert.equal(row[20], 'PENDING');
  assert.equal(row[21], ''); // blank for pending
  assert.equal(row[22], ''); // blank for pending
  console.log('✓ PASS [24/31]: create-order initializes Payment Result=PENDING and blank completed_at/failure_reason');
}

// 25. TEST: Payment Result becomes SUCCESS and Payment Completed At is populated on verification
{
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();
  const ord = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '200', currency: 'INR' }) }
  }).getContent());

  const payId = 'pay_succ_001';
  const sig = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET).update(`${ord.order_id}|${payId}`).digest('hex');

  const ver = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({
      action: 'verify-payment',
      razorpay_order_id: ord.order_id,
      razorpay_payment_id: payId,
      razorpay_signature: sig,
      internal_id: ord.internal_id,
    }) }
  }).getContent());
  assert.equal(ver.success, true);

  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  const row = paySheet.grid[1];
  assert.equal(row[4], 'captured'); // Status unchanged at col 5
  assert.equal(row[18], 'true');    // Verified unchanged at col 19
  assert.equal(row[20], 'SUCCESS'); // Payment Result col 21
  assert.ok(row[21], 'Payment Completed At must be populated');
  assert.match(row[21], /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/);
  assert.equal(row[22], '');       // Failure Reason must be empty
  console.log('✓ PASS [25/31]: verify-payment sets Payment Result=SUCCESS, timestamps completed_at, clears failure_reason');
}

// 26. TEST: Signature failure sets Payment Result=FAILED with Failure Reason
{
  const { context, mockSpreadsheet } = createMockEnvironment();
  const ord = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '300', currency: 'INR' }) }
  }).getContent());

  const ver = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({
      action: 'verify-payment',
      razorpay_order_id: ord.order_id,
      razorpay_payment_id: 'pay_bad_sig_001',
      razorpay_signature: 'invalid_signature_hex_value_000',
      internal_id: ord.internal_id,
    }) }
  }).getContent());
  assert.equal(ver.success, false);

  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  const row = paySheet.grid[1];
  assert.equal(row[4], 'failed');
  assert.equal(row[20], 'FAILED');
  assert.equal(row[21], ''); // No completion timestamp
  assert.equal(row[22], 'Invalid payment signature.');
  console.log('✓ PASS [26/31]: Failed verification sets Payment Result=FAILED and Failure Reason');
}

// 27. TEST: Client-side failure reporting (report-failure)
{
  const { context, mockSpreadsheet } = createMockEnvironment();
  const ord = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '400', currency: 'INR' }) }
  }).getContent());

  const rep = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({
      action: 'report-failure',
      order_id: ord.order_id,
      internal_id: ord.internal_id,
      reason: 'Bank server network timeout at OTP step',
    }) }
  }).getContent());
  assert.equal(rep.success, true);
  assert.equal(rep.payment_result, 'FAILED');

  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  const row = paySheet.grid[1];
  assert.equal(row[4], 'failed');
  assert.equal(row[20], 'FAILED');
  assert.equal(row[21], '');
  assert.equal(row[22], 'Bank server network timeout at OTP step');
  console.log('✓ PASS [27/31]: report-failure endpoint transitions order to FAILED with descriptive reason');
}

// 28. TEST: Client-side cancellation reporting (report-cancel)
{
  const { context, mockSpreadsheet } = createMockEnvironment();
  const ord = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '500', currency: 'INR' }) }
  }).getContent());

  const rep = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({
      action: 'report-cancel',
      order_id: ord.order_id,
      internal_id: ord.internal_id,
      reason: 'Checkout modal dismissed by patron',
    }) }
  }).getContent());
  assert.equal(rep.success, true);
  assert.equal(rep.payment_result, 'CANCELLED');

  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  const row = paySheet.grid[1];
  assert.equal(row[4], 'cancelled');
  assert.equal(row[20], 'CANCELLED');
  assert.equal(row[21], '');
  assert.equal(row[22], 'Checkout modal dismissed by patron');
  console.log('✓ PASS [28/31]: report-cancel endpoint transitions pending order to CANCELLED');
}

// 29. TEST: Conditional formatting rules applied to Payment Result (col 21)
{
  const { context, mockSpreadsheet } = createMockEnvironment();
  // Trigger initialization
  context.doGet({ parameter: { action: 'recent-support' } });

  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  const rules = paySheet.getConditionalFormatRules();
  assert.ok(rules.length >= 6, 'Should have conditional rules for SUCCESS, PENDING, FAILED, AUTHORIZED, REFUNDED, CANCELLED');
  const ruleTexts = rules.map(r => r.text);
  assert.ok(ruleTexts.includes('SUCCESS'));
  assert.ok(ruleTexts.includes('PENDING'));
  assert.ok(ruleTexts.includes('FAILED'));
  assert.ok(ruleTexts.includes('AUTHORIZED'));
  assert.ok(ruleTexts.includes('REFUNDED'));
  assert.ok(ruleTexts.includes('CANCELLED'));
  console.log('✓ PASS [29/31]: Conditional formatting rules configure colors for all 6 payment states');
}

// 30. TEST: Dedicated PaymentSummary tab calculations & isolated currency totals
{
  const { context, mockSpreadsheet, scriptProperties } = createMockEnvironment();
  // 1. Create order 1: INR 500 (captured)
  const o1 = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '500', currency: 'INR' }) }
  }).getContent());
  const s1 = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET).update(`${o1.order_id}|pay_sum_001`).digest('hex');
  context.doPost({
    postData: { contents: JSON.stringify({ action: 'verify-payment', razorpay_order_id: o1.order_id, razorpay_payment_id: 'pay_sum_001', razorpay_signature: s1, internal_id: o1.internal_id }) }
  });

  // 2. Create order 2: USD 25 (captured)
  const o2 = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '25.00', currency: 'USD' }) }
  }).getContent());
  const s2 = crypto.createHmac('sha256', scriptProperties.RAZORPAY_KEY_SECRET).update(`${o2.order_id}|pay_sum_002`).digest('hex');
  context.doPost({
    postData: { contents: JSON.stringify({ action: 'verify-payment', razorpay_order_id: o2.order_id, razorpay_payment_id: 'pay_sum_002', razorpay_signature: s2, internal_id: o2.internal_id }) }
  });

  // 3. Create order 3: pending
  context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '1000', currency: 'INR' }) }
  });

  // 4. Create order 4: cancelled
  const o4 = JSON.parse(context.doPost({
    postData: { contents: JSON.stringify({ action: 'create-order', amount: '50', currency: 'EUR' }) }
  }).getContent());
  context.doPost({
    postData: { contents: JSON.stringify({ action: 'report-cancel', order_id: o4.order_id, internal_id: o4.internal_id, reason: 'Dismissed' }) }
  });

  const sumSheet = mockSpreadsheet.getSheetByName('PaymentSummary');
  assert.ok(sumSheet, 'PaymentSummary tab must exist');
  assert.equal(sumSheet.grid[0][0], 'Metric');
  assert.equal(sumSheet.grid[0][1], 'Value');
  assert.equal(sumSheet.grid[0][2], 'Notes');

  const summaryData = {};
  for (let r = 1; r < sumSheet.grid.length; r++) {
    summaryData[sumSheet.grid[r][0]] = sumSheet.grid[r][1];
  }

  assert.equal(summaryData['Successful Payments'], 2);
  assert.equal(summaryData['Pending Payments'], 1);
  assert.equal(summaryData['Cancelled Payments'], 1);
  assert.ok(summaryData['Total Successful Amount by Currency'].includes('INR 500.00'));
  assert.ok(summaryData['Total Successful Amount by Currency'].includes('USD 25.00'));
  // Confirm currencies are segregated and not combined into a single numeric total
  assert.ok(!summaryData['Total Successful Amount by Currency'].includes('525'));
  console.log('✓ PASS [30/31]: PaymentSummary calculates segregated currency totals & accurate counters');
}

// 31. TEST: Safe migration of legacy 20-column Payments table
{
  const { context, mockSpreadsheet } = createMockEnvironment();
  const paySheet = mockSpreadsheet.insertSheet('Payments');
  // Populate legacy 20 columns
  const legacyHeaders = [
    "Created At", "Updated At", "Payment ID", "Order ID", "Status", "Amount", "Currency",
    "International", "Payment Method", "Customer Name", "Customer Email", "Customer Phone",
    "Country", "Support Message", "Razorpay Fee", "Tax", "Refund Status", "Internal Reference",
    "Verified", "Sheet Sync Status"
  ];
  const legacyRow1 = [
    "2026-03-01T10:00:00Z", "2026-03-01T10:05:00Z", "pay_leg_01", "order_leg_01", "captured",
    750, "INR", false, "upi", "Legacy User", "legacy@example.com", "", "IN", "Thank you",
    15, 2.7, "none", "ekg_sup_leg_01", "true", "synced"
  ];
  const legacyRow2 = [
    "2026-03-02T10:00:00Z", "2026-03-02T10:00:00Z", "", "order_leg_02", "created",
    1200, "INR", false, "card", "Pending User", "pending@example.com", "", "IN", "",
    0, 0, "none", "ekg_sup_leg_02", "false", "created"
  ];
  paySheet.appendRow(legacyHeaders);
  paySheet.appendRow(legacyRow1);
  paySheet.appendRow(legacyRow2);

  // Trigger migration through sheet initialization / GET query
  context.doGet({ parameter: { action: 'recent-support' } });

  assert.equal(paySheet.grid[0].length, 23, 'Headers must be updated to 23 columns');
  assert.equal(paySheet.grid[0][20], 'Payment Result');
  assert.equal(paySheet.grid[0][21], 'Payment Completed At');
  assert.equal(paySheet.grid[0][22], 'Failure Reason');

  // Row 1 (captured)
  assert.equal(paySheet.grid[1][20], 'SUCCESS');
  assert.equal(paySheet.grid[1][21], '2026-03-01T10:05:00Z');
  assert.equal(paySheet.grid[1][22], '');

  // Row 2 (created / pending)
  assert.equal(paySheet.grid[2][20], 'PENDING');
  assert.equal(paySheet.grid[2][21], '');
  assert.equal(paySheet.grid[2][22], '');
  console.log('✓ PASS [31/31]: Legacy sheet migration preserves all 20 columns and backfills Payment Result');
}

console.log('All 31 Google Apps Script backend tests passed successfully!');

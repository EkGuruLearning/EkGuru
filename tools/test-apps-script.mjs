// tools/test-apps-script.mjs
// Comprehensive test suite for apps-script/Code.gs running with mocked Apps Script environment.

import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import vm from 'node:vm';

const codePath = path.resolve(process.cwd(), 'apps-script/Code.gs');
const codeGs = fs.readFileSync(codePath, 'utf8');

console.log('Testing apps-script/Code.gs in mocked Google Apps Script runtime...');

function createMockEnvironment() {
  const scriptProperties = {
    SHEETS_INGEST_TOKEN: 'test-secret-token-1234567890',
    SPREADSHEET_ID: '1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI',
  };

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
      }
    },
    PropertiesService: {
      getScriptProperties: () => ({
        getProperty: (key) => scriptProperties[key] || null,
        setProperty: (key, val) => { scriptProperties[key] = val; }
      })
    },
    ContentService: {
      MimeType: { JSON: 'application/json' },
      createTextOutput: (text) => ({
        _content: text,
        _mime: 'text/plain',
        setMimeType: function(mime) { this._mime = mime; return this; },
        getContent: function() { return this._content; }
      })
    },
    Utilities: {
      formatDate: (d, tz, fmt) => d.toISOString(),
      getUuid: () => '12345678-test-uuid'
    }
  };

  vm.createContext(context);
  vm.runInContext(codeGs, context);

  return { context, mockSpreadsheet, scriptProperties };
}

// TEST 1: Missing or Invalid Token Handling
{
  const { context } = createMockEnvironment();
  
  // No token in POST body
  const eNoToken = {
    postData: {
      contents: JSON.stringify({
        operation: 'payment_upsert',
        data: { payment_id: 'pay_123' }
      })
    }
  };
  const res1 = JSON.parse(context.doPost(eNoToken).getContent());
  assert.equal(res1.success, false);
  assert.match(res1.error, /Unauthorized/);
  console.log('✓ PASS: Rejects POST with missing token (401)');

  // Token passed via query parameter (strictly forbidden)
  const eQueryToken = {
    parameter: { token: 'test-secret-token-1234567890' },
    postData: {
      contents: JSON.stringify({
        operation: 'payment_upsert',
        data: { payment_id: 'pay_123' }
      })
    }
  };
  const res2 = JSON.parse(context.doPost(eQueryToken).getContent());
  assert.equal(res2.success, false);
  assert.equal(res2.code, 'FORBIDDEN_AUTH_METHOD');
  console.log('✓ PASS: Rejects POST with token in URL query parameter (403)');
}

// TEST 2: Multi-Currency Customer Totals Preservation (No Cross-Currency Summing)
{
  const { context, mockSpreadsheet } = createMockEnvironment();

  // First customer payment in INR
  const e1 = {
    postData: {
      contents: JSON.stringify({
        token: 'test-secret-token-1234567890',
        operation: 'customer_upsert',
        data: {
          email: 'patron@example.com',
          name: 'Test Patron',
          amount: 500,
          currency: 'INR'
        }
      })
    }
  };
  const res1 = JSON.parse(context.doPost(e1).getContent());
  assert.equal(res1.success, true);

  // Second customer payment in USD from same customer
  const e2 = {
    postData: {
      contents: JSON.stringify({
        token: 'test-secret-token-1234567890',
        operation: 'customer_upsert',
        data: {
          email: 'patron@example.com',
          name: 'Test Patron',
          amount: 25,
          currency: 'USD'
        }
      })
    }
  };
  const res2 = JSON.parse(context.doPost(e2).getContent());
  assert.equal(res2.success, true);

  // Check Customers tab row
  const custSheet = mockSpreadsheet.getSheetByName('Customers');
  assert.ok(custSheet);
  const rows = custSheet.grid;
  // Header row is index 0
  const custRow = rows[1];
  assert.equal(custRow[2], 'patron@example.com'); // Email
  assert.equal(custRow[7], 2); // Total Payments count = 2
  // Total Supported Amount should NOT be 525 (INR 500 + USD 25)!
  // It must be currency-separated: "INR 500.00, USD 25.00"
  assert.equal(custRow[8], 'INR 500.00, USD 25.00');
  assert.equal(custRow[9], 'INR, USD');
  console.log('✓ PASS: Preserves multi-currency customer totals without cross-currency summing');
}

// TEST 3: PublicSupport Opt-In and Sanitization
{
  const { context, mockSpreadsheet } = createMockEnvironment();

  // Payment 1: Opted in
  const eOptIn = {
    postData: {
      contents: JSON.stringify({
        token: 'test-secret-token-1234567890',
        operation: 'public_support_upsert',
        data: {
          payment_id: 'pay_PUB_01',
          order_id: 'order_PUB_01',
          status: 'captured',
          amount: 1500,
          currency: 'INR',
          displayName: 'Ananya Sharma',
          country: 'IN',
          message: 'Keep up the fantastic education work!',
          publicDisplayOptIn: true,
          internal_reference: 'EKG-TEST-001',
          verified: true
        }
      })
    }
  };
  const res1 = JSON.parse(context.doPost(eOptIn).getContent());
  assert.equal(res1.success, true);

  // Payment 2: NOT opted in
  const eNoOptIn = {
    postData: {
      contents: JSON.stringify({
        token: 'test-secret-token-1234567890',
        operation: 'public_support_upsert',
        data: {
          payment_id: 'pay_PRIV_02',
          order_id: 'order_PRIV_02',
          status: 'captured',
          amount: 5000,
          currency: 'INR',
          displayName: 'Secret Donor',
          country: 'IN',
          message: 'Private donation',
          publicDisplayOptIn: false,
          internal_reference: 'EKG-TEST-002',
          verified: true
        }
      })
    }
  };
  const res2 = JSON.parse(context.doPost(eNoOptIn).getContent());
  assert.equal(res2.success, false);
  assert.match(res2.error, /opt-in not granted/i);

  // Check PublicSupport tab
  const pubSheet = mockSpreadsheet.getSheetByName('PublicSupport');
  assert.ok(pubSheet);
  // Grid should have Header (row 0) and exactly 1 supporter (row 1)
  assert.equal(pubSheet.grid.length, 2);
  const pubRow = pubSheet.grid[1];
  assert.equal(pubRow[1], 'Ananya Sharma'); // Display Name
  assert.equal(pubRow[2], 'IN'); // Country
  assert.equal(pubRow[3], 1500); // Amount
  assert.equal(pubRow[4], 'INR'); // Currency
  assert.equal(pubRow[5], 'Keep up the fantastic education work!'); // Message
  assert.equal(pubRow[6], true); // Public

  // Check doGet output for recent support
  const eGet = { parameter: { action: 'recent-support' } };
  const getRes = JSON.parse(context.doGet(eGet).getContent());
  assert.equal(getRes.success, true);
  assert.equal(getRes.items.length, 1);
  const supporter = getRes.items[0];
  assert.equal(supporter.displayName, 'Ananya Sharma');
  assert.equal(supporter.country, 'IN');
  assert.equal(supporter.amount, 1500);
  assert.equal(supporter.currency, 'INR');
  assert.equal(supporter.message, 'Keep up the fantastic education work!');

  // Strict check: Private donor must NOT appear anywhere in public GET output
  const jsonString = JSON.stringify(getRes);
  assert.ok(!jsonString.includes('Secret Donor'));
  assert.ok(!jsonString.includes('secret_donor@example.com'));
  assert.ok(!jsonString.includes('9999999999'));
  console.log('✓ PASS: PublicSupport tab & doGet sanitize private details and obey opt-in flag');
}

// TEST 4: PublicSupport Deduplication
{
  const { context, mockSpreadsheet } = createMockEnvironment();

  const payload = {
    token: 'test-secret-token-1234567890',
    operation: 'public_support_upsert',
    data: {
      display_name: 'Devin AI',
      country: 'US',
      amount: 100,
      currency: 'USD',
      message: 'Great platform',
      public_display_opt_in: true,
      internal_reference: 'EKG-DUP-CHECK-1',
      status: 'captured',
      verified: true
    }
  };

  // Run twice with same internal_reference
  const res1 = JSON.parse(context.doPost({ postData: { contents: JSON.stringify(payload) } }).getContent());
  assert.equal(res1.success, true);
  const res2 = JSON.parse(context.doPost({ postData: { contents: JSON.stringify(payload) } }).getContent());
  assert.equal(res2.success, true);
  assert.equal(res2.deduplicated, true);

  const pubSheet = mockSpreadsheet.getSheetByName('PublicSupport');
  // Should only have 1 data row + 1 header row = 2 rows
  assert.equal(pubSheet.grid.length, 2);
  console.log('✓ PASS: public_support_upsert idempotently deduplicates repeated entries');
}

// TEST 5: Header Integrity & Safe Repair
{
  const { context, mockSpreadsheet } = createMockEnvironment();

  // Create sheet with corrupted header
  const pSheet = mockSpreadsheet.getSheetByName('Payments') || mockSpreadsheet.insertSheet('Payments');
  pSheet.appendRow(['WrongHeader1', 'WrongHeader2']);
  pSheet.appendRow(['2026-09-19', '2026-09-19', 'pay_EXISTING', 'order_EXISTING', 'captured']);

  // Call sheet setup or an operation
  const payload = {
    token: 'test-secret-token-1234567890',
    operation: 'sheet_setup',
    data: {}
  };
  const res = JSON.parse(context.doPost({ postData: { contents: JSON.stringify(payload) } }).getContent());
  assert.equal(res.success, true);

  // Header should now be repaired (20 columns), but row 2 must be intact!
  assert.equal(pSheet.grid[0][0], 'Created At');
  assert.equal(pSheet.grid[0][2], 'Payment ID');
  assert.equal(pSheet.grid[1][2], 'pay_EXISTING');
  console.log('✓ PASS: Safe header repair replaces row 1 without losing transaction data in rows >= 2');
}

// TEST 6: Explicit End-to-End Contract Test Between SheetsClient and apps-script/Code.gs
{
  const { context, mockSpreadsheet } = createMockEnvironment();

  // Create a custom fetch that delegates to context.doPost
  const customFetch = async (url, options) => {
    const e = {
      postData: {
        contents: options.body
      }
    };
    const output = context.doPost(e);
    const text = output.getContent();
    return {
      ok: true,
      status: 200,
      json: async () => JSON.parse(text)
    };
  };

  const { SheetsClient } = await import('../server/sheets-client.js');
  const client = new SheetsClient({
    endpoint: 'https://script.google.com/macros/s/AKfycbz8u_rBr2o4VPgmQgaweswLWKdYb-MMGrsa7WfckTCruLP-ZEasWnpkqJrZHux5Y8_4zA/exec',
    token: 'test-secret-token-1234567890',
    spreadsheetId: '1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI',
    fetch: customFetch
  });

  // 1. Contract Test: syncPayment
  const payRes = await client.syncPayment({
    internal_id: 'ekg_contract_pay_01',
    razorpay_payment_id: 'pay_contract_01',
    razorpay_order_id: 'order_contract_01',
    status: 'captured',
    display_amount: 125.50,
    currency: 'USD',
    customer_name: 'Contract Patron',
    customer_email: 'contract@example.com',
    customer_phone: '+14155552671',
    country: 'US',
    support_message: 'Validating end-to-end client contract',
    fee: 3.50,
    tax: 0.63,
    refund_status: 'none',
    verification_status: 'verified',
    created_at: '2026-09-19T06:30:00.000Z'
  });
  assert.equal(payRes.success, true);
  const paySheet = mockSpreadsheet.getSheetByName('Payments');
  assert.ok(paySheet);
  assert.equal(paySheet.grid.length, 2); // 1 header + 1 record
  assert.equal(paySheet.grid[1][2], 'pay_contract_01'); // Payment ID
  assert.equal(paySheet.grid[1][3], 'order_contract_01'); // Order ID
  assert.equal(paySheet.grid[1][5], 125.50); // Amount
  assert.equal(paySheet.grid[1][6], 'USD'); // Currency
  assert.equal(paySheet.grid[1][17], 'ekg_contract_pay_01'); // Internal Reference
  assert.equal(paySheet.grid[1][18], 'true'); // Verified

  // 2. Contract Test: syncCustomer
  const custRes = await client.syncCustomer({
    customer_id: 'cust_contract_01',
    email: 'contract@example.com',
    name: 'Contract Patron',
    phone: '+14155552671',
    country: 'US',
    amount: 125.50,
    currency: 'USD'
  });
  assert.equal(custRes.success, true);
  const custSheet = mockSpreadsheet.getSheetByName('Customers');
  assert.ok(custSheet);
  assert.equal(custSheet.grid.length, 2);
  assert.equal(custSheet.grid[1][0], 'cust_contract_01'); // Customer ID
  assert.equal(custSheet.grid[1][2], 'contract@example.com'); // Email
  assert.equal(custSheet.grid[1][7], 1); // Total Payments count
  assert.equal(custSheet.grid[1][8], 'USD 125.50'); // Per-currency Total Supported Amount

  // 3. Contract Test: syncRefund
  const refRes = await client.syncRefund({
    refund_id: 'rfnd_contract_01',
    payment_id: 'pay_contract_01',
    order_id: 'order_contract_01',
    amount: 50.00,
    currency: 'USD',
    status: 'processed',
    reason: 'supporter_request'
  });
  assert.equal(refRes.success, true);
  const refSheet = mockSpreadsheet.getSheetByName('Refunds');
  assert.ok(refSheet);
  assert.equal(refSheet.grid.length, 2);
  assert.equal(refSheet.grid[1][1], 'rfnd_contract_01');
  assert.equal(refSheet.grid[1][4], 50.00);

  // 4. Contract Test: syncWebhookEvent
  const hookRes = await client.syncWebhookEvent({
    event_id: 'evt_contract_01',
    event_type: 'payment.captured',
    payment_id: 'pay_contract_01',
    order_id: 'order_contract_01',
    processed: true,
    result: 'success'
  });
  assert.equal(hookRes.success, true);
  const hookSheet = mockSpreadsheet.getSheetByName('WebhookEvents');
  assert.ok(hookSheet);
  assert.equal(hookSheet.grid.length, 2);
  assert.equal(hookSheet.grid[1][1], 'evt_contract_01');
  assert.equal(hookSheet.grid[1][2], 'payment.captured');

  // 5. Contract Test: syncPublicSupport
  const pubRes = await client.syncPublicSupport({
    displayName: 'Contract Patron',
    country: 'US',
    amount: 125.50,
    currency: 'USD',
    message: 'Validating end-to-end client contract',
    publicDisplayOptIn: true,
    internal_reference: 'ekg_contract_pay_01',
    payment_id: 'pay_contract_01',
    status: 'captured',
    verified: true
  });
  assert.equal(pubRes.success, true);
  const pubSheet = mockSpreadsheet.getSheetByName('PublicSupport');
  assert.ok(pubSheet);
  assert.equal(pubSheet.grid.length, 2);
  assert.equal(pubSheet.grid[1][1], 'Contract Patron'); // Display Name
  assert.equal(pubSheet.grid[1][2], 'US'); // Country
  assert.equal(pubSheet.grid[1][3], 125.50); // Amount
  assert.equal(pubSheet.grid[1][4], 'USD'); // Currency
  assert.equal(pubSheet.grid[1][6], true); // Public

  console.log('✓ PASS: SheetsClient <-> apps-script/Code.gs end-to-end contract test (5/5 operations)');
}

console.log('All Apps Script tests passed successfully!');

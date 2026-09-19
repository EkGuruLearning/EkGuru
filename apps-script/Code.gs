/**
 * ============================================================================
 * EkGuru — Google Sheets Automated Private Payment Ledger & Public Support Mirror
 * ============================================================================
 * Spreadsheet ID: 1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI
 *
 * Operational/Reporting mirror for EkGuru Support Payments.
 * Razorpay is the primary source of truth.
 *
 * TABS MANAGED:
 * 1. Payments        — Comprehensive private ledger of all contributions.
 * 2. Customers       — Aggregate patron profiles and multi-currency contribution stats.
 * 3. Refunds         — Refund tracking synced from webhook/gateway events.
 * 4. WebhookEvents   — Webhook audit log with event-level idempotency tracking.
 * 5. PublicSupport   — Sanitized public records for opted-in supporters only.
 *
 * PRODUCTION SECURITY & PRIVACY CONTRACT:
 * - SHEETS_INGEST_TOKEN: Accepted ONLY from POST request payload body.
 *   URL query parameters for tokens are strictly rejected.
 * - Script Properties is the ONLY configuration source for SHEETS_INGEST_TOKEN.
 * - SPREADSHEET SAFETY: SpreadsheetApp.openById(id) is required.
 *   Fallback to getActiveSpreadsheet() is disabled to prevent writing to wrong sheet.
 * - HEADER INTEGRITY: Verifies full expected headers on all tabs and safely repairs
 *   missing/incorrect header rows without deleting existing transaction rows.
 * - MULTI-CURRENCY TOTALS: Totals are preserved strictly per-currency.
 *   Cross-currency arithmetic (e.g. INR + USD) is prohibited.
 * - PUBLIC SUPPORT: Only verified successful payments with explicit publicDisplayOptIn
 *   are recorded. Private identifiers (email, phone, payment IDs, order IDs) are NEVER exposed.
 * - IDEMPOTENCY: Payment upserts, customer aggregations, webhook events, and public
 *   support entries all deduplicate by unique IDs to avoid duplicate rows.
 * ============================================================================
 */

var SPREADSHEET_ID_DEFAULT = "1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI";

var TAB_PAYMENTS = "Payments";
var TAB_CUSTOMERS = "Customers";
var TAB_REFUNDS = "Refunds";
var TAB_WEBHOOK_EVENTS = "WebhookEvents";
var TAB_PUBLIC_SUPPORT = "PublicSupport";

var HEADERS = {
  Payments: [
    "Created At",
    "Updated At",
    "Payment ID",
    "Order ID",
    "Status",
    "Amount",
    "Currency",
    "International",
    "Payment Method",
    "Customer Name",
    "Customer Email",
    "Customer Phone",
    "Country",
    "Support Message",
    "Razorpay Fee",
    "Tax",
    "Refund Status",
    "Internal Reference",
    "Verified",
    "Sheet Sync Status",
  ],
  Customers: [
    "Customer ID",
    "Name",
    "Email",
    "Phone",
    "Country",
    "First Payment",
    "Last Payment",
    "Total Payments",
    "Total Supported Amount",
    "Currencies Used",
  ],
  Refunds: [
    "Created At",
    "Refund ID",
    "Payment ID",
    "Order ID",
    "Amount",
    "Currency",
    "Status",
    "Reason",
  ],
  WebhookEvents: [
    "Received At",
    "Event ID",
    "Event Type",
    "Payment ID",
    "Order ID",
    "Processed",
    "Processing Result",
  ],
  PublicSupport: [
    "Created At",
    "Display Name",
    "Country",
    "Amount",
    "Currency",
    "Message",
    "Public",
    "Payment Date",
    "Internal Reference",
  ],
};

/**
 * Gets the designated target spreadsheet.
 * Fails clearly if designated ID cannot be opened; never silently writes to active sheet.
 */
function getSpreadsheet_() {
  var prop = PropertiesService.getScriptProperties().getProperty("SPREADSHEET_ID");
  var id = (prop && prop.trim()) ? prop.trim() : SPREADSHEET_ID_DEFAULT;

  if (!id) {
    throw new Error("Target Spreadsheet ID configuration is missing.");
  }

  try {
    return SpreadsheetApp.openById(id);
  } catch (err) {
    // Fail clearly. Never fallback to getActiveSpreadsheet() or write to an arbitrary sheet.
    throw new Error("Unable to open designated payment spreadsheet (ID: " + id + "): " + err.message);
  }
}

/**
 * Verifies and safely repairs required tabs and headers without erasing existing data.
 */
function ensureSheetsAndHeaders_(ss) {
  var tabNames = [
    TAB_PAYMENTS,
    TAB_CUSTOMERS,
    TAB_REFUNDS,
    TAB_WEBHOOK_EVENTS,
    TAB_PUBLIC_SUPPORT,
  ];

  for (var i = 0; i < tabNames.length; i++) {
    var name = tabNames[i];
    var sheet = ss.getSheetByName(name);
    if (!sheet) {
      sheet = ss.insertSheet(name);
    }
    var expectedHeaders = HEADERS[name];
    var lastRow = sheet.getLastRow();

    if (lastRow === 0) {
      sheet.appendRow(expectedHeaders);
      sheet.getRange(1, 1, 1, expectedHeaders.length).setFontWeight("bold");
    } else {
      var lastCol = Math.max(sheet.getLastColumn(), expectedHeaders.length);
      var currentHeaders = sheet.getRange(1, 1, 1, lastCol).getValues()[0];
      var needsRepair = false;

      for (var c = 0; c < expectedHeaders.length; c++) {
        if (!currentHeaders[c] || String(currentHeaders[c]).trim() !== expectedHeaders[c]) {
          needsRepair = true;
          break;
        }
      }

      if (needsRepair) {
        // Safe header repair: updates row 1 only; existing data in rows >= 2 is never deleted
        sheet.getRange(1, 1, 1, expectedHeaders.length).setValues([expectedHeaders]).setFontWeight("bold");
      }
    }
  }
}

/**
 * Validates ingest token against Script Properties.
 * SECURITY: Accepts authentication ONLY from POST payload body.
 * Tokens in URL query parameters are strictly forbidden.
 */
function isAuthorized_(payload) {
  var expectedToken = PropertiesService.getScriptProperties().getProperty("SHEETS_INGEST_TOKEN");
  if (!expectedToken || typeof expectedToken !== "string" || !expectedToken.trim()) {
    return false; // Fail closed if token not configured in Script Properties
  }

  var incomingToken = (payload && typeof payload.token === "string") ? payload.token.trim() : "";
  return incomingToken.length > 0 && incomingToken === expectedToken.trim();
}

/**
 * Strips any potential secret tokens or sensitive parameters from error messages.
 */
function sanitizeErrorMessage_(msg) {
  if (!msg) return "An error occurred.";
  var clean = String(msg);
  clean = clean.replace(/token=[^&\s]+/gi, "token=[REDACTED]");
  clean = clean.replace(/bearer\s+[a-zA-Z0-9_\-\.]+/gi, "Bearer [REDACTED]");
  return clean;
}

/**
 * Standard JSON response helper.
 */
function jsonOutput_(obj) {
  var output = ContentService.createTextOutput(JSON.stringify(obj));
  output.setMimeType(ContentService.MimeType.JSON);
  return output;
}

/**
 * Parses currency-separated amounts string (e.g. "INR 500.00, USD 25.00").
 * Prevents cross-currency addition.
 */
function parseCurrencyTotals_(str) {
  var map = {};
  if (!str) return map;

  if (typeof str === "string" && str.trim().startsWith("{")) {
    try {
      var parsed = JSON.parse(str);
      for (var k in parsed) {
        map[k.toUpperCase()] = Number(parsed[k]) || 0;
      }
      return map;
    } catch (e) {}
  }

  var parts = String(str).split(/[,|]/);
  for (var i = 0; i < parts.length; i++) {
    var p = parts[i].trim();
    var match = p.match(/^([A-Z]{3})[:\s]+([\d.]+)/i);
    if (match) {
      var code = match[1].toUpperCase();
      var amt = parseFloat(match[2]) || 0;
      map[code] = (map[code] || 0) + amt;
    }
  }
  return map;
}

/**
 * Formats multi-currency map into a human- and machine-readable representation.
 */
function formatCurrencyTotals_(map) {
  var items = [];
  var codes = Object.keys(map).sort();
  for (var i = 0; i < codes.length; i++) {
    var c = codes[i];
    items.push(c + " " + Number(map[c]).toFixed(2));
  }
  return items.join(", ");
}

/**
 * GET Handler — Public sanitized view ONLY.
 * Exposes /exec?action=recent-support
 * Never exposes private tabs, emails, phones, payment IDs, or tokens.
 */
function doGet(e) {
  try {
    // Explicitly reject any query parameter tokens to prevent token leakage in URLs or logs
    if (e && e.parameter && e.parameter.token) {
      return jsonOutput_({
        success: false,
        error: "Forbidden: Tokens must never be passed in GET requests or query parameters.",
        code: "FORBIDDEN_AUTH_METHOD"
      });
    }

    var action = (e && e.parameter && e.parameter.action) || "recent-support";

    if (action === "recent-support" || action === "recent") {
      var ss = getSpreadsheet_();
      ensureSheetsAndHeaders_(ss);
      var sheet = ss.getSheetByName(TAB_PUBLIC_SUPPORT);
      var lastRow = sheet.getLastRow();

      if (lastRow <= 1) {
        return jsonOutput_({ success: true, count: 0, supporters: [] });
      }

      var data = sheet.getRange(2, 1, lastRow - 1, HEADERS.PublicSupport.length).getValues();
      var supporters = [];

      // Read from latest to oldest, returning max 10
      for (var i = data.length - 1; i >= 0 && supporters.length < 10; i--) {
        var row = data[i];
        var isPublic = row[6]; // "Public" column
        if (isPublic === true || String(isPublic).toLowerCase() === "true" || String(isPublic).toLowerCase() === "yes") {
          var displayName = String(row[1] || "").trim() || "Supporter";
          // Strictly sanitized output: NEVER expose email, phone, payment IDs, or internal references
          supporters.push({
            displayName: displayName,
            country: String(row[2] || "").trim() || "International",
            amount: Number(row[3]) || 0,
            currency: String(row[4] || "INR").trim().toUpperCase(),
            message: String(row[5] || "").trim(),
            date: row[7] instanceof Date ? row[7].toISOString().split("T")[0] : String(row[7] || "").split("T")[0],
          });
        }
      }

      return jsonOutput_({
        success: true,
        count: supporters.length,
        supporters: supporters,
        items: supporters,
      });
    }

    if (action === "health") {
      return jsonOutput_({ success: true, status: "ok", service: "EkGuru Sheets Payment Mirror" });
    }

    return jsonOutput_({ success: false, error: "Unauthorized or unknown action." });
  } catch (err) {
    return jsonOutput_({ success: false, error: sanitizeErrorMessage_(err.message) });
  }
}

/**
 * POST Handler — Authenticated ingest for private ledger operations.
 */
function doPost(e) {
  try {
    // Explicitly reject query parameter authentication to ensure tokens are never passed in URLs
    if (e && e.parameter && e.parameter.token) {
      return jsonOutput_({
        success: false,
        error: "Forbidden: Query parameter authentication is not permitted. Pass SHEETS_INGEST_TOKEN in POST body.",
        code: "FORBIDDEN_AUTH_METHOD"
      });
    }

    var rawBody = (e && e.postData && e.postData.contents) || "{}";
    var payload = {};
    try {
      payload = JSON.parse(rawBody);
    } catch (parseErr) {
      return jsonOutput_({ success: false, error: "Invalid JSON body payload." });
    }

    // Authenticate token ONLY from POST body
    if (!isAuthorized_(payload)) {
      return jsonOutput_({ success: false, error: "Unauthorized: Invalid or missing SHEETS_INGEST_TOKEN." });
    }

    var operation = payload.operation;
    if (!operation) {
      return jsonOutput_({ success: false, error: "Missing required 'operation' in payload." });
    }

    var ss = getSpreadsheet_();
    ensureSheetsAndHeaders_(ss);

    switch (operation) {
      case "sheet_setup":
        return jsonOutput_({ success: true, message: "Sheets and headers validated and initialized." });

      case "payment_insert":
      case "payment_upsert":
        return jsonOutput_(handlePaymentUpsert_(ss, payload.data));

      case "customer_upsert":
        return jsonOutput_(handleCustomerUpsert_(ss, payload.data));

      case "refund_upsert":
        return jsonOutput_(handleRefundUpsert_(ss, payload.data));

      case "webhook_event_upsert":
        return jsonOutput_(handleWebhookEventUpsert_(ss, payload.data));

      case "public_support_upsert":
        return jsonOutput_(handlePublicSupportUpsert_(ss, payload.data));

      default:
        return jsonOutput_({ success: false, error: "Unknown operation: " + operation });
    }
  } catch (err) {
    return jsonOutput_({ success: false, error: sanitizeErrorMessage_(err.message) });
  }
}

/**
 * Upserts a row into the Payments tab.
 * Deduplicates by internal reference, payment ID, or order ID.
 */
function handlePaymentUpsert_(ss, data) {
  var lookupId = data && (data.internal_id || data.internal_reference || data.payment_id || data.order_id);
  if (!lookupId) {
    return { success: false, error: "Missing required identifier (internal_id, payment_id, or order_id) for payment upsert." };
  }

  var internalId = (data.internal_id || data.internal_reference || data.payment_id || "").toString().trim();
  var paymentId = (data.payment_id || "").toString().trim();
  var orderId = (data.order_id || "").toString().trim();

  var sheet = ss.getSheetByName(TAB_PAYMENTS);
  var lastRow = sheet.getLastRow();
  var rowIndex = -1;

  if (lastRow > 1) {
    var values = sheet.getRange(2, 1, lastRow - 1, HEADERS.Payments.length).getValues();
    for (var i = 0; i < values.length; i++) {
      var rowInternalId = String(values[i][17] || "").trim(); // Internal Reference
      var rowPaymentId = String(values[i][2] || "").trim(); // Payment ID
      var rowOrderId = String(values[i][3] || "").trim(); // Order ID

      if (
        (internalId && rowInternalId === internalId) ||
        (paymentId && rowPaymentId === paymentId) ||
        (orderId && rowOrderId === orderId)
      ) {
        rowIndex = i + 2;
        break;
      }
    }
  }

  var now = new Date().toISOString();
  var rowValues = [
    data.created_at || now,
    now,
    paymentId,
    orderId,
    data.status || "created",
    data.amount != null ? data.amount : 0,
    (data.currency || "INR").toUpperCase(),
    Boolean(data.international),
    data.method || "card",
    data.customer_name || "",
    data.customer_email || "",
    data.customer_phone || "",
    data.country || "",
    data.support_message || "",
    data.fee != null ? data.fee : 0,
    data.tax != null ? data.tax : 0,
    data.refund_status || "none",
    internalId,
    data.verified === true ? "true" : "false",
    data.sheet_sync_status || "synced",
  ];

  if (rowIndex > 0) {
    // Preserve initial Created At if updating existing record
    var existingCreatedAt = sheet.getRange(rowIndex, 1).getValue();
    if (existingCreatedAt) rowValues[0] = existingCreatedAt;
    sheet.getRange(rowIndex, 1, 1, rowValues.length).setValues([rowValues]);
  } else {
    sheet.appendRow(rowValues);
  }

  return {
    success: true,
    operation: "payment_upsert",
    internal_id: internalId,
    row: rowIndex > 0 ? rowIndex : sheet.getLastRow(),
    action: rowIndex > 0 ? "updated" : "inserted",
  };
}

/**
 * Upserts a customer into the Customers tab.
 * Enforces per-currency multi-currency tracking without summing different currencies.
 */
function handleCustomerUpsert_(ss, data) {
  if (!data || (!data.email && !data.customer_id)) {
    return { success: false, error: "Missing customer email or customer_id." };
  }

  var sheet = ss.getSheetByName(TAB_CUSTOMERS);
  var lastRow = sheet.getLastRow();
  var rowIndex = -1;
  var existingRow = null;

  if (lastRow > 1) {
    var values = sheet.getRange(2, 1, lastRow - 1, HEADERS.Customers.length).getValues();
    for (var i = 0; i < values.length; i++) {
      var email = String(values[i][2]).toLowerCase().trim();
      var custId = String(values[i][0]).trim();
      if ((data.email && email === String(data.email).toLowerCase().trim()) ||
          (data.customer_id && custId === String(data.customer_id).trim())) {
        rowIndex = i + 2;
        existingRow = values[i];
        break;
      }
    }
  }

  var now = new Date().toISOString();
  var currency = (data.currency || "INR").toUpperCase();
  var paymentAmount = Number(data.amount) || 0;

  if (rowIndex > 0 && existingRow) {
    var custId = existingRow[0];
    var firstPayment = existingRow[5] || now;
    var totalPayments = (Number(existingRow[7]) || 0) + 1;

    // Multi-currency safe aggregation: NEVER sum across currencies
    var totalsMap = parseCurrencyTotals_(existingRow[8]);
    totalsMap[currency] = (totalsMap[currency] || 0) + paymentAmount;
    var totalAmountByCurrency = formatCurrencyTotals_(totalsMap);

    var currList = String(existingRow[9] || "").split(",").map(function(c) { return c.trim(); }).filter(Boolean);
    if (currList.indexOf(currency) === -1) {
      currList.push(currency);
    }

    var updatedValues = [
      custId,
      data.name || existingRow[1],
      data.email || existingRow[2],
      data.phone || existingRow[3],
      data.country || existingRow[4],
      firstPayment,
      now,
      totalPayments,
      totalAmountByCurrency,
      currList.join(", "),
    ];

    sheet.getRange(rowIndex, 1, 1, updatedValues.length).setValues([updatedValues]);
    return { success: true, operation: "customer_upsert", customer_id: custId, action: "updated" };
  } else {
    var uuidStr = (typeof Utilities !== "undefined" && Utilities.getUuid) ? Utilities.getUuid() : Math.random().toString(36).substring(2, 10);
    var newCustId = data.customer_id || "cust_" + uuidStr.substring(0, 8);
    var newTotalsMap = {};
    newTotalsMap[currency] = paymentAmount;
    var newTotalAmountByCurrency = formatCurrencyTotals_(newTotalsMap);

    var newRow = [
      newCustId,
      data.name || "",
      data.email || "",
      data.phone || "",
      data.country || "",
      now,
      now,
      1,
      newTotalAmountByCurrency,
      currency,
    ];
    sheet.appendRow(newRow);
    return { success: true, operation: "customer_upsert", customer_id: newCustId, action: "created" };
  }
}

/**
 * Upserts a refund record into Refunds tab and updates Payments tab refund status.
 */
function handleRefundUpsert_(ss, data) {
  if (!data || !data.refund_id) {
    return { success: false, error: "Missing refund_id." };
  }

  var sheet = ss.getSheetByName(TAB_REFUNDS);
  var lastRow = sheet.getLastRow();
  var rowIndex = -1;

  if (lastRow > 1) {
    var values = sheet.getRange(2, 1, lastRow - 1, HEADERS.Refunds.length).getValues();
    for (var i = 0; i < values.length; i++) {
      if (values[i][1] === data.refund_id) {
        rowIndex = i + 2;
        break;
      }
    }
  }

  var now = new Date().toISOString();
  var row = [
    data.created_at || now,
    data.refund_id,
    data.payment_id || "",
    data.order_id || "",
    data.amount != null ? data.amount : 0,
    (data.currency || "INR").toUpperCase(),
    data.status || "processed",
    data.reason || "supporter_request",
  ];

  if (rowIndex > 0) {
    sheet.getRange(rowIndex, 1, 1, row.length).setValues([row]);
  } else {
    sheet.appendRow(row);
  }

  // Update corresponding Payments tab refund_status if payment_id is known
  if (data.payment_id) {
    var paySheet = ss.getSheetByName(TAB_PAYMENTS);
    var payLastRow = paySheet.getLastRow();
    if (payLastRow > 1) {
      var payValues = paySheet.getRange(2, 1, payLastRow - 1, HEADERS.Payments.length).getValues();
      for (var p = 0; p < payValues.length; p++) {
        if (payValues[p][2] === data.payment_id) {
          paySheet.getRange(p + 2, 17).setValue(data.status || "refunded"); // Refund Status column
          paySheet.getRange(p + 2, 5).setValue("refunded"); // Status column
          break;
        }
      }
    }
  }

  return { success: true, operation: "refund_upsert", refund_id: data.refund_id, action: rowIndex > 0 ? "updated" : "inserted" };
}

/**
 * Upserts a webhook event for idempotency and audit.
 */
function handleWebhookEventUpsert_(ss, data) {
  if (!data || !data.event_id) {
    return { success: false, error: "Missing event_id." };
  }

  var sheet = ss.getSheetByName(TAB_WEBHOOK_EVENTS);
  var lastRow = sheet.getLastRow();

  if (lastRow > 1) {
    var values = sheet.getRange(2, 1, lastRow - 1, HEADERS.WebhookEvents.length).getValues();
    for (var i = 0; i < values.length; i++) {
      if (values[i][1] === data.event_id) {
        return { success: true, operation: "webhook_event_upsert", duplicate: true, event_id: data.event_id };
      }
    }
  }

  var now = new Date().toISOString();
  var row = [
    data.received_at || now,
    data.event_id,
    data.event_type || "",
    data.payment_id || "",
    data.order_id || "",
    data.processed !== false ? "true" : "false",
    data.result || "success",
  ];

  sheet.appendRow(row);
  return { success: true, operation: "webhook_event_upsert", duplicate: false, event_id: data.event_id };
}

/**
 * Upserts a sanitized entry in PublicSupport tab.
 * IDEMPOTENCY: Avoids duplicate public entries for the same payment or reference.
 * PRIVACY: Strictly avoids publishing email, phone, or payment IDs.
 */
function handlePublicSupportUpsert_(ss, data) {
  // 1. Strict public opt-in requirement
  var hasOptIn = data && (data.publicDisplayOptIn === true || data.public === true || data.public_display_opt_in === true);
  if (!hasOptIn) {
    return { success: false, error: "Public opt-in not granted." };
  }

  // 2. Only verified successful payments
  var isVerified = data && (data.verified === true || data.status === "captured" || data.verification_status === "verified");
  if (!isVerified) {
    return { success: false, error: "Only verified successful payments may be published." };
  }

  var sheet = ss.getSheetByName(TAB_PUBLIC_SUPPORT);
  var lastRow = sheet.getLastRow();
  var internalRef = data.internal_id || data.internal_reference || "";
  var paymentId = data.payment_id || "";
  var paymentDate = data.payment_date || new Date().toISOString().split("T")[0];
  var displayName = String(data.displayName || data.display_name || data.customer_name || "Supporter").trim();
  var country = String(data.country || "International").trim();
  var amount = Number(data.amount) || 0;
  var currency = String(data.currency || "INR").toUpperCase();
  var message = String(data.message || data.support_message || "").trim();

  // 3. Idempotency deduplication check: avoid duplicate public entries
  if (lastRow > 1) {
    var values = sheet.getRange(2, 1, lastRow - 1, HEADERS.PublicSupport.length).getValues();
    for (var i = 0; i < values.length; i++) {
      var rowRef = values[i][8]; // Internal Reference in column 9
      var rowName = values[i][1];
      var rowAmount = Number(values[i][3]) || 0;
      var rowCurrency = values[i][4];
      var rowDate = values[i][7] instanceof Date ? values[i][7].toISOString().split("T")[0] : String(values[i][7] || "").split("T")[0];

      if (
        (internalRef && rowRef === internalRef) ||
        (paymentId && rowRef === paymentId) ||
        (rowName === displayName && rowAmount === amount && rowCurrency === currency && rowDate === paymentDate)
      ) {
        return {
          success: true,
          operation: "public_support_upsert",
          duplicate: true,
          deduplicated: true,
          message: "Public support entry already recorded.",
        };
      }
    }
  }

  var now = new Date().toISOString();
  // Row contains strictly sanitized fields. Column 9 holds internal reference for private deduplication only.
  var row = [
    now,
    displayName,
    country,
    amount,
    currency,
    message,
    true,
    paymentDate,
    internalRef || paymentId,
  ];

  sheet.appendRow(row);
  return { success: true, operation: "public_support_upsert", duplicate: false };
}

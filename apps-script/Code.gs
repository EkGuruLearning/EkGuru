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
 * 2. Customers       — Aggregate patron profiles and lifetime contribution stats.
 * 3. Refunds         — Refund tracking synced from webhook/gateway events.
 * 4. WebhookEvents   — Webhook audit log with event-level idempotency tracking.
 * 5. PublicSupport   — Sanitized public records for opted-in supporters only.
 *
 * SECURITY & PRIVACY CONTRACT:
 * - Write operations require a valid SHEETS_INGEST_TOKEN set in Script Properties.
 * - Public GET queries return ONLY sanitized entries from PublicSupport tab.
 * - Never returns email, phone, payment ID, order ID, or private credentials publicly.
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
  ],
};

/**
 * Gets the target spreadsheet.
 */
function getSpreadsheet_() {
  var prop = PropertiesService.getScriptProperties().getProperty("SPREADSHEET_ID");
  var id = prop || SPREADSHEET_ID_DEFAULT;
  try {
    return SpreadsheetApp.openById(id);
  } catch (e) {
    return SpreadsheetApp.getActiveSpreadsheet();
  }
}

/**
 * Verifies or initializes required tabs and headers without erasing existing data.
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
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(expectedHeaders);
      sheet.getRange(1, 1, 1, expectedHeaders.length).setFontWeight("bold");
    } else {
      // Check if header row matches, repair missing if empty
      var currentHeaders = sheet.getRange(1, 1, 1, Math.max(sheet.getLastColumn(), 1)).getValues()[0];
      if (!currentHeaders || currentHeaders.length === 0 || !currentHeaders[0]) {
        sheet.getRange(1, 1, 1, expectedHeaders.length).setValues([expectedHeaders]).setFontWeight("bold");
      }
    }
  }
}

/**
 * Validates the ingest token against Script Properties.
 */
function isAuthorized_(e, payload) {
  var expectedToken = PropertiesService.getScriptProperties().getProperty("SHEETS_INGEST_TOKEN");
  // If no token has been configured yet in properties, fall back to check parameter or deny
  if (!expectedToken) {
    return false;
  }

  var incomingToken = "";
  if (e && e.parameter && e.parameter.token) {
    incomingToken = e.parameter.token;
  } else if (payload && payload.token) {
    incomingToken = payload.token;
  }

  return incomingToken === expectedToken;
}

/**
 * Standard JSON response helper.
 */
function jsonOutput_(obj, statusCode) {
  var output = ContentService.createTextOutput(JSON.stringify(obj));
  output.setMimeType(ContentService.MimeType.JSON);
  return output;
}

/**
 * GET Handler — Public sanitized view ONLY.
 * Exposes /exec?action=recent-support
 */
function doGet(e) {
  try {
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

      // Read from latest to oldest
      for (var i = data.length - 1; i >= 0 && supporters.length < 10; i--) {
        var row = data[i];
        var isPublic = row[6]; // "Public" column
        if (isPublic === true || String(isPublic).toLowerCase() === "true" || String(isPublic).toLowerCase() === "yes") {
          var displayName = String(row[1] || "").trim() || "Supporter";
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
      });
    }

    if (action === "health") {
      return jsonOutput_({ success: true, status: "ok", service: "EkGuru Sheets Payment Mirror" });
    }

    return jsonOutput_({ success: false, error: "Unauthorized or unknown action." });
  } catch (err) {
    return jsonOutput_({ success: false, error: err.message });
  }
}

/**
 * POST Handler — Authenticated ingest for private ledger operations.
 */
function doPost(e) {
  try {
    var rawBody = (e && e.postData && e.postData.contents) || "{}";
    var payload = {};
    try {
      payload = JSON.parse(rawBody);
    } catch (parseErr) {
      return jsonOutput_({ success: false, error: "Invalid JSON body." });
    }

    if (!isAuthorized_(e, payload)) {
      return jsonOutput_({ success: false, error: "Unauthorized: Invalid or missing SHEETS_INGEST_TOKEN." });
    }

    var operation = payload.operation || (e && e.parameter && e.parameter.operation);
    var ss = getSpreadsheet_();
    ensureSheetsAndHeaders_(ss);

    switch (operation) {
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
    return jsonOutput_({ success: false, error: err.message });
  }
}

/**
 * Upserts a row into the Payments tab.
 */
function handlePaymentUpsert_(ss, data) {
  if (!data || !data.internal_id) {
    return { success: false, error: "Missing internal_id" };
  }

  var sheet = ss.getSheetByName(TAB_PAYMENTS);
  var lastRow = sheet.getLastRow();
  var rowIndex = -1;

  if (lastRow > 1) {
    var values = sheet.getRange(2, 1, lastRow - 1, HEADERS.Payments.length).getValues();
    for (var i = 0; i < values.length; i++) {
      var rowInternalId = values[i][17]; // Internal Reference
      var rowPaymentId = values[i][2]; // Payment ID
      var rowOrderId = values[i][3]; // Order ID

      if (
        (data.internal_id && rowInternalId === data.internal_id) ||
        (data.payment_id && rowPaymentId === data.payment_id) ||
        (data.order_id && rowOrderId === data.order_id)
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
    data.payment_id || "",
    data.order_id || "",
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
    data.internal_id || "",
    data.verified === true ? "true" : "false",
    data.sheet_sync_status || "synced",
  ];

  if (rowIndex > 0) {
    // Preserve initial Created At if updating
    var existingCreatedAt = sheet.getRange(rowIndex, 1).getValue();
    if (existingCreatedAt) rowValues[0] = existingCreatedAt;
    sheet.getRange(rowIndex, 1, 1, rowValues.length).setValues([rowValues]);
  } else {
    sheet.appendRow(rowValues);
  }

  return { success: true, operation: "payment_upsert", internal_id: data.internal_id, row: rowIndex > 0 ? rowIndex : sheet.getLastRow() };
}

/**
 * Upserts a row into the Customers tab.
 */
function handleCustomerUpsert_(ss, data) {
  if (!data || (!data.email && !data.customer_id)) {
    return { success: false, error: "Missing customer email or customer_id" };
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
    var totalAmount = (Number(existingRow[8]) || 0) + paymentAmount;
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
      totalAmount,
      currList.join(", "),
    ];

    sheet.getRange(rowIndex, 1, 1, updatedValues.length).setValues([updatedValues]);
    return { success: true, operation: "customer_upsert", customer_id: custId, action: "updated" };
  } else {
    var newCustId = data.customer_id || "cust_" + Utilities.getUuid().substring(0, 8);
    var newRow = [
      newCustId,
      data.name || "",
      data.email || "",
      data.phone || "",
      data.country || "",
      now,
      now,
      1,
      paymentAmount,
      currency,
    ];
    sheet.appendRow(newRow);
    return { success: true, operation: "customer_upsert", customer_id: newCustId, action: "created" };
  }
}

/**
 * Upserts a refund record into Refunds tab and updates Payments tab.
 */
function handleRefundUpsert_(ss, data) {
  if (!data || !data.refund_id) {
    return { success: false, error: "Missing refund_id" };
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

  // Also update Payments tab refund_status if payment_id matches
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

  return { success: true, operation: "refund_upsert", refund_id: data.refund_id };
}

/**
 * Upserts a webhook event for idempotency and audit.
 */
function handleWebhookEventUpsert_(ss, data) {
  if (!data || !data.event_id) {
    return { success: false, error: "Missing event_id" };
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
 * Upserts a sanitized entry in PublicSupport tab ONLY if public opt-in is true.
 * Strictly avoids logging emails, phone numbers, or private internal identifiers.
 */
function handlePublicSupportUpsert_(ss, data) {
  if (!data || data.publicDisplayOptIn !== true && data.public !== true) {
    return { success: false, error: "Public opt-in not granted" };
  }

  var sheet = ss.getSheetByName(TAB_PUBLIC_SUPPORT);
  var now = new Date().toISOString();
  var paymentDate = data.payment_date || now.split("T")[0];

  var row = [
    now,
    String(data.displayName || data.display_name || data.customer_name || "Supporter").trim(),
    String(data.country || "International").trim(),
    Number(data.amount) || 0,
    String(data.currency || "INR").toUpperCase(),
    String(data.message || data.support_message || "").trim(),
    true,
    paymentDate,
  ];

  sheet.appendRow(row);
  return { success: true, operation: "public_support_upsert" };
}

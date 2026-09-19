/**
 * EkGuru — Minimal Secure Payment Record Store
 *
 * Implements the payment record model strictly adhering to PCI-DSS and EkGuru security rules.
 * DO NOT store card numbers, CVVs, bank credentials, secrets, or sensitive payment authentication data.
 */

"use strict";

let fs = null;
let path = null;
try {
  fs = require("node:fs");
  path = require("node:path");
} catch (e) {
  // Edge runtime without filesystem
}

const FORBIDDEN_FIELDS = new Set([
  "card",
  "card_number",
  "cardnumber",
  "cvv",
  "cvv2",
  "cvc",
  "pin",
  "password",
  "bank_credential",
  "secret",
  "key_secret",
  "razorpay_key_secret",
  "webhook_secret",
  "sheets_ingest_token",
]);

class PaymentStore {
  constructor(options = {}) {
    this.storagePath = options.storagePath || null;
    this.records = new Map(); // internal_id -> record
    this.orderIndex = new Map(); // razorpay_order_id -> internal_id
    this.paymentIndex = new Map(); // razorpay_payment_id -> internal_id
    this.webhookEvents = new Map(); // event_id -> eventData
    this.customers = new Map(); // email/id -> customerRecord
    this.refunds = new Map(); // refund_id -> refundRecord

    if (this.storagePath && fs.existsSync(this.storagePath)) {
      this._loadFromFile();
    }
  }

  _sanitizeData(data) {
    if (!data || typeof data !== "object") return {};
    for (const key of Object.keys(data)) {
      const lower = key.toLowerCase();
      if (FORBIDDEN_FIELDS.has(lower) || lower.includes("card_num") || lower.includes("cvv") || (lower.includes("secret") && !lower.includes("opt_in"))) {
        throw new Error(`Security Violation: Sensitive field '${key}' is strictly forbidden from payment storage.`);
      }
    }
    return data;
  }

  /**
   * Creates a new payment record.
   */
  createRecord(data) {
    this._sanitizeData(data);

    if (!data.internal_id) {
      throw new Error("Missing required payment record field: internal_id");
    }
    if (!data.currency) {
      throw new Error("Missing required payment record field: currency");
    }
    if (typeof data.amount_minor !== "number") {
      throw new Error("Missing required payment record field: amount_minor (integer)");
    }

    const now = new Date().toISOString();

    const record = {
      internal_id: String(data.internal_id),
      razorpay_order_id: data.razorpay_order_id ? String(data.razorpay_order_id) : null,
      razorpay_payment_id: data.razorpay_payment_id ? String(data.razorpay_payment_id) : null,
      currency: String(data.currency).toUpperCase(),
      amount_minor: data.amount_minor,
      display_amount: data.display_amount != null ? data.display_amount : null,
      status: data.status || "created", // created, authorized, captured, failed, refunded
      purpose: data.purpose || "ekguru_support",
      customer_email: data.customer_email ? String(data.customer_email).trim() : null,
      customer_name: data.customer_name ? String(data.customer_name).trim() : null,
      customer_phone: data.customer_phone ? String(data.customer_phone).trim() : null,
      country: data.country ? String(data.country).trim() : null,
      support_message: data.support_message ? String(data.support_message).trim() : null,
      public_display_opt_in: Boolean(data.public_display_opt_in),
      method: data.method || "card",
      international: data.international != null ? Boolean(data.international) : (String(data.currency).toUpperCase() !== "INR"),
      fee: data.fee != null ? data.fee : 0,
      tax: data.tax != null ? data.tax : 0,
      refund_status: data.refund_status || "none", // none | partial | refunded
      sheet_sync_status: data.sheet_sync_status || "pending", // pending | synced | failed | retrying
      payment_result: data.payment_result || (data.status === "captured" ? "SUCCESS" : (data.status === "failed" ? "FAILED" : (data.status === "authorized" ? "AUTHORIZED" : (data.status === "cancelled" ? "CANCELLED" : "PENDING")))),
      payment_completed_at: data.payment_completed_at || (data.status === "captured" ? now : null),
      failure_reason: data.failure_reason || null,
      created_at: data.created_at || now,
      updated_at: data.updated_at || now,
      source: data.source || "checkout", // checkout | webhook
      webhook_verified: Boolean(data.webhook_verified),
      verification_status: data.verification_status || "pending", // pending | verified | failed
    };

    this.records.set(record.internal_id, record);

    if (record.razorpay_order_id) {
      this.orderIndex.set(record.razorpay_order_id, record.internal_id);
    }
    if (record.razorpay_payment_id) {
      this.paymentIndex.set(record.razorpay_payment_id, record.internal_id);
    }

    this._saveToFile();
    return { ...record };
  }

  /**
   * Updates an existing payment record.
   */
  updateRecord(internalId, updates) {
    this._sanitizeData(updates);

    const record = this.records.get(internalId);
    if (!record) return null;

    if (updates.razorpay_order_id && updates.razorpay_order_id !== record.razorpay_order_id) {
      record.razorpay_order_id = String(updates.razorpay_order_id);
      this.orderIndex.set(record.razorpay_order_id, internalId);
    }

    if (updates.razorpay_payment_id && updates.razorpay_payment_id !== record.razorpay_payment_id) {
      record.razorpay_payment_id = String(updates.razorpay_payment_id);
      this.paymentIndex.set(record.razorpay_payment_id, internalId);
    }

    if (updates.status !== undefined) record.status = updates.status;
    if (updates.verification_status !== undefined) record.verification_status = updates.verification_status;
    if (updates.webhook_verified !== undefined) record.webhook_verified = Boolean(updates.webhook_verified);
    if (updates.source !== undefined) record.source = updates.source;
    if (updates.customer_email !== undefined) record.customer_email = updates.customer_email;
    if (updates.customer_name !== undefined) record.customer_name = updates.customer_name;
    if (updates.customer_phone !== undefined) record.customer_phone = updates.customer_phone;
    if (updates.country !== undefined) record.country = updates.country;
    if (updates.support_message !== undefined) record.support_message = updates.support_message;
    if (updates.public_display_opt_in !== undefined) record.public_display_opt_in = Boolean(updates.public_display_opt_in);
    if (updates.display_amount !== undefined) record.display_amount = updates.display_amount;
    if (updates.method !== undefined) record.method = updates.method;
    if (updates.fee !== undefined) record.fee = updates.fee;
    if (updates.tax !== undefined) record.tax = updates.tax;
    if (updates.refund_status !== undefined) record.refund_status = updates.refund_status;
    if (updates.sheet_sync_status !== undefined) record.sheet_sync_status = updates.sheet_sync_status;
    if (updates.payment_result !== undefined) record.payment_result = updates.payment_result;
    if (updates.payment_completed_at !== undefined) record.payment_completed_at = updates.payment_completed_at;
    if (updates.failure_reason !== undefined) record.failure_reason = updates.failure_reason;

    record.updated_at = new Date().toISOString();
    this._saveToFile();
    return { ...record };
  }

  getByInternalId(internalId) {
    if (!internalId) return null;
    const r = this.records.get(String(internalId));
    return r ? { ...r } : null;
  }

  getByOrderId(orderId) {
    if (!orderId) return null;
    const internalId = this.orderIndex.get(String(orderId));
    return internalId ? this.getByInternalId(internalId) : null;
  }

  getByPaymentId(paymentId) {
    if (!paymentId) return null;
    const internalId = this.paymentIndex.get(String(paymentId));
    return internalId ? this.getByInternalId(internalId) : null;
  }

  isDuplicatePayment(paymentId) {
    if (!paymentId) return false;
    const record = this.getByPaymentId(paymentId);
    return Boolean(record && (record.status === "captured" || record.verification_status === "verified"));
  }

  hasProcessedWebhook(eventId) {
    if (!eventId) return false;
    return this.webhookEvents.has(String(eventId));
  }

  recordWebhookEvent(eventId, details = {}) {
    if (!eventId) return;
    this.webhookEvents.set(String(eventId), {
      event_id: String(eventId),
      recorded_at: new Date().toISOString(),
      ...details,
    });
    this._saveToFile();
  }

  /**
   * Upserts a customer into the local customer store.
   */
  upsertCustomer(customerData) {
    this._sanitizeData(customerData);
    const email = customerData.email ? customerData.email.toLowerCase().trim() : null;
    const key = email || customerData.customer_id;
    if (!key) return null;

    const now = new Date().toISOString();
    const existing = this.customers.get(key);
    const amount = Number(customerData.amount) || 0;
    const currency = (customerData.currency || "INR").toUpperCase();

    if (existing) {
      existing.last_payment = now;
      existing.total_payments = (existing.total_payments || 1) + 1;
      existing.totals_by_currency = existing.totals_by_currency || {};
      existing.totals_by_currency[currency] = (existing.totals_by_currency[currency] || 0) + amount;

      if (!existing.currencies.includes(currency)) {
        existing.currencies.push(currency);
      }

      if (existing.currencies.length === 1) {
        existing.total_amount = (existing.total_amount || 0) + amount;
      } else {
        // Multi-currency: never sum across currencies
        existing.total_amount = Object.entries(existing.totals_by_currency)
          .map(([c, a]) => `${c} ${a.toFixed(2)}`)
          .join(", ");
      }
      existing.total_amount_by_currency = Object.entries(existing.totals_by_currency)
        .map(([c, a]) => `${c} ${a.toFixed(2)}`)
        .join(", ");

      if (customerData.name) existing.name = customerData.name;
      if (customerData.phone) existing.phone = customerData.phone;
      if (customerData.country) existing.country = customerData.country;
      this._saveToFile();
      return { ...existing };
    } else {
      const totalsByCurrency = {};
      totalsByCurrency[currency] = amount;
      const newCustomer = {
        customer_id: customerData.customer_id || `cust_${Date.now().toString(36)}`,
        name: customerData.name || "",
        email: email || "",
        phone: customerData.phone || "",
        country: customerData.country || "",
        first_payment: now,
        last_payment: now,
        total_payments: 1,
        total_amount: amount,
        totals_by_currency: totalsByCurrency,
        total_amount_by_currency: `${currency} ${amount.toFixed(2)}`,
        currencies: [currency],
      };
      this.customers.set(key, newCustomer);
      this._saveToFile();
      return { ...newCustomer };
    }
  }

  /**
   * Records a refund into the local refund store.
   */
  recordRefund(refundData) {
    this._sanitizeData(refundData);
    if (!refundData.refund_id) return null;

    const refund = {
      refund_id: String(refundData.refund_id),
      payment_id: refundData.payment_id || null,
      order_id: refundData.order_id || null,
      amount: refundData.amount,
      currency: (refundData.currency || "INR").toUpperCase(),
      status: refundData.status || "processed",
      reason: refundData.reason || "supporter_request",
      created_at: refundData.created_at || new Date().toISOString(),
    };

    this.refunds.set(refund.refund_id, refund);

    // Update payment record refund_status if linked
    if (refund.payment_id) {
      const record = this.getByPaymentId(refund.payment_id);
      if (record) {
        this.updateRecord(record.internal_id, {
          status: "refunded",
          refund_status: "refunded",
        });
      }
    }

    this._saveToFile();
    return { ...refund };
  }

  list(limit = 100) {
    return Array.from(this.records.values())
      .slice(-limit)
      .map((r) => ({ ...r }));
  }

  clear() {
    this.records.clear();
    this.orderIndex.clear();
    this.paymentIndex.clear();
    this.webhookEvents.clear();
    this.customers.clear();
    this.refunds.clear();
    this._saveToFile();
  }

  _loadFromFile() {
    try {
      const content = fs.readFileSync(this.storagePath, "utf8");
      const data = JSON.parse(content);
      if (Array.isArray(data.records)) {
        for (const r of data.records) {
          this.createRecord(r);
        }
      }
      if (Array.isArray(data.webhookEvents)) {
        for (const ev of data.webhookEvents) {
          this.webhookEvents.set(ev.event_id || ev, ev);
        }
      }
      if (Array.isArray(data.customers)) {
        for (const c of data.customers) {
          this.customers.set(c.email || c.customer_id, c);
        }
      }
      if (Array.isArray(data.refunds)) {
        for (const rf of data.refunds) {
          this.refunds.set(rf.refund_id, rf);
        }
      }
    } catch (e) {
      // Ignore initial file read errors
    }
  }

  _saveToFile() {
    if (!this.storagePath) return;
    try {
      const dir = path.dirname(this.storagePath);
      if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
      const payload = {
        records: Array.from(this.records.values()),
        webhookEvents: Array.from(this.webhookEvents.values()),
        customers: Array.from(this.customers.values()),
        refunds: Array.from(this.refunds.values()),
      };
      fs.writeFileSync(this.storagePath, JSON.stringify(payload, null, 2), "utf8");
    } catch (e) {
      // Ignore file write errors in restricted environments
    }
  }
}

// Global default singleton instance
const defaultStore = new PaymentStore();

module.exports = {
  PaymentStore,
  defaultStore,
};

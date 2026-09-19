/**
 * EkGuru — Minimal Secure Payment Record Store
 *
 * Implements the payment record model strictly adhering to PCI-DSS and EkGuru security rules.
 * DO NOT store card numbers, CVVs, bank credentials, secrets, or sensitive payment authentication data.
 */

"use strict";

const fs = require("fs");
const path = require("path");

const FORBIDDEN_FIELDS = new Set([
  "card",
  "card_number",
  "cardNumber",
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
]);

class PaymentStore {
  constructor(options = {}) {
    this.storagePath = options.storagePath || null;
    this.records = new Map(); // internal_id -> record
    this.orderIndex = new Map(); // razorpay_order_id -> internal_id
    this.paymentIndex = new Map(); // razorpay_payment_id -> internal_id
    this.webhookEvents = new Set(); // event_id -> processed

    if (this.storagePath && fs.existsSync(this.storagePath)) {
      this._loadFromFile();
    }
  }

  _sanitizeData(data) {
    if (!data || typeof data !== "object") return {};
    for (const key of Object.keys(data)) {
      const lower = key.toLowerCase();
      if (FORBIDDEN_FIELDS.has(lower) || lower.includes("card_num") || lower.includes("cvv") || lower.includes("secret")) {
        throw new Error(`Security Violation: Sensitive field '${key}' is strictly forbidden from payment storage.`);
      }
    }
    return data;
  }

  /**
   * Creates a new payment record.
   *
   * Required fields:
   * - internal_id
   * - razorpay_order_id
   * - razorpay_payment_id
   * - currency
   * - amount_minor
   * - status
   * - purpose
   * - customer_email (if available)
   * - customer_name (if available)
   * - created_at
   * - updated_at
   * - source
   * - webhook_verified
   * - verification_status
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
      status: data.status || "created", // created, authorized, captured, failed, refunded
      purpose: data.purpose || "ekguru_support",
      customer_email: data.customer_email ? String(data.customer_email).trim() : null,
      customer_name: data.customer_name ? String(data.customer_name).trim() : null,
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
   * @param {string} internalId
   * @param {object} updates
   * @returns {object|null}
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

  recordWebhookEvent(eventId) {
    if (!eventId) return;
    this.webhookEvents.add(String(eventId));
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
          this.webhookEvents.add(ev);
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
        webhookEvents: Array.from(this.webhookEvents),
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

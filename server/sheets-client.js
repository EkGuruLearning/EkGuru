/**
 * EkGuru — Google Sheets Integration Client
 *
 * Safely mirrors verified payments, customers, refunds, and webhook events
 * to Google Apps Script backend.
 *
 * Resilience Contract:
 * - If Google Sheets is temporarily unreachable, payments MUST NOT fail.
 * - Sheet sync status is maintained independently: 'pending' | 'synced' | 'failed' | 'retrying'.
 * - Failed syncs are queued and retried without creating duplicate rows.
 * - Provides sanitized caching for GET /api/support/recent (60-300s TTL).
 */

"use strict";

class SheetsClient {
  constructor(options = {}) {
    this.endpoint = options.endpoint || process.env.GOOGLE_SHEETS_ENDPOINT || "";
    this.token = options.token || process.env.SHEETS_INGEST_TOKEN || "";
    this.spreadsheetId = options.spreadsheetId || process.env.GOOGLE_SPREADSHEET_ID || "1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI";
    this.customFetch = options.fetch || null;

    // Retry queue for resilience
    this.retryQueue = [];
    this.isRetrying = false;

    // In-memory cache for recent supporters
    this.supportersCache = {
      data: [],
      timestamp: 0,
      ttlMs: options.cacheTtlMs || 120 * 1000, // 2 minutes (within 60-300s range)
    };
  }

  /**
   * Safe fetch wrapper that handles network timeouts gracefully.
   */
  async _postToAppsScript(operation, data) {
    if (!this.endpoint) {
      return { success: false, offline: true, error: "GOOGLE_SHEETS_ENDPOINT not configured." };
    }

    const payload = {
      operation,
      token: this.token,
      spreadsheet_id: this.spreadsheetId,
      data,
    };

    const fetchFn = this.customFetch || globalThis.fetch;
    if (!fetchFn) {
      return { success: false, error: "No fetch implementation available." };
    }

    try {
      const resp = await fetchFn(this.endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!resp.ok) {
        return { success: false, status: resp.status, error: `HTTP error ${resp.status}` };
      }

      const resData = await resp.json().catch(() => ({}));
      return resData;
    } catch (err) {
      return { success: false, error: err.message || "Network request failed" };
    }
  }

  /**
   * Syncs a verified payment to the Payments sheet tab.
   *
   * @param {object} record - Payment record
   * @returns {Promise<object>}
   */
  async syncPayment(record) {
    const payload = {
      internal_id: record.internal_id,
      payment_id: record.razorpay_payment_id || "",
      order_id: record.razorpay_order_id || "",
      status: record.status || "captured",
      amount: record.display_amount != null ? Number(record.display_amount) : (record.amount_minor / 100),
      currency: record.currency,
      international: record.currency !== "INR",
      method: record.method || "card",
      customer_name: record.customer_name || "",
      customer_email: record.customer_email || "",
      customer_phone: record.customer_phone || "",
      country: record.country || "",
      support_message: record.support_message || "",
      fee: record.fee != null ? record.fee : 0,
      tax: record.tax != null ? record.tax : 0,
      refund_status: record.refund_status || "none",
      verified: record.verification_status === "verified",
      sheet_sync_status: "synced",
      created_at: record.created_at,
    };

    const res = await this._postToAppsScript("payment_upsert", payload);
    if (!res.success) {
      this.enqueueRetry("payment_upsert", payload);
    }
    return res;
  }

  /**
   * Syncs customer aggregate data to the Customers sheet tab.
   */
  async syncCustomer(data) {
    const payload = {
      email: data.email || data.customer_email || "",
      name: data.name || data.customer_name || "",
      phone: data.phone || data.customer_phone || "",
      country: data.country || "",
      amount: data.amount != null ? Number(data.amount) : 0,
      currency: data.currency || "INR",
      customer_id: data.customer_id || null,
    };

    if (!payload.email && !payload.customer_id) {
      return { success: false, error: "Missing customer identifier" };
    }

    const res = await this._postToAppsScript("customer_upsert", payload);
    if (!res.success) {
      this.enqueueRetry("customer_upsert", payload);
    }
    return res;
  }

  /**
   * Syncs a refund record to the Refunds tab.
   */
  async syncRefund(data) {
    const payload = {
      refund_id: data.refund_id,
      payment_id: data.payment_id || "",
      order_id: data.order_id || "",
      amount: data.amount,
      currency: data.currency,
      status: data.status || "processed",
      reason: data.reason || "supporter_request",
      created_at: data.created_at || new Date().toISOString(),
    };

    const res = await this._postToAppsScript("refund_upsert", payload);
    if (!res.success) {
      this.enqueueRetry("refund_upsert", payload);
    }
    return res;
  }

  /**
   * Syncs a webhook event for audit and idempotency to WebhookEvents tab.
   */
  async syncWebhookEvent(data) {
    const payload = {
      event_id: data.event_id,
      event_type: data.event_type || data.event,
      payment_id: data.payment_id || "",
      order_id: data.order_id || "",
      processed: data.processed !== false,
      result: data.result || "success",
      received_at: data.received_at || new Date().toISOString(),
    };

    const res = await this._postToAppsScript("webhook_event_upsert", payload);
    if (!res.success) {
      this.enqueueRetry("webhook_event_upsert", payload);
    }
    return res;
  }

  /**
   * Syncs an entry to PublicSupport tab ONLY if user opted in.
   */
  async syncPublicSupport(data) {
    if (data.publicDisplayOptIn !== true && data.public !== true) {
      return { success: false, error: "Public opt-in not granted" };
    }

    const payload = {
      displayName: String(data.displayName || data.customer_name || "Supporter").trim(),
      country: String(data.country || "International").trim(),
      amount: data.amount,
      currency: data.currency,
      message: String(data.message || data.support_message || "").trim(),
      public: true,
      payment_date: data.payment_date || new Date().toISOString().split("T")[0],
    };

    // Update in-memory supporters cache
    this.addSupporterToCache(payload);

    const res = await this._postToAppsScript("public_support_upsert", payload);
    if (!res.success) {
      this.enqueueRetry("public_support_upsert", payload);
    }
    return res;
  }

  /**
   * Adds an opted-in public supporter to the local in-memory cache.
   */
  addSupporterToCache(supporter) {
    const entry = {
      displayName: supporter.displayName,
      country: supporter.country,
      amount: Number(supporter.amount) || 0,
      currency: String(supporter.currency).toUpperCase(),
      message: supporter.message || "",
      date: supporter.payment_date || supporter.date || new Date().toISOString().split("T")[0],
    };

    // Prepend new supporter and keep max 10
    this.supportersCache.data = [
      entry,
      ...this.supportersCache.data.filter((s) => s.displayName !== entry.displayName || s.date !== entry.date),
    ].slice(0, 10);
    this.supportersCache.timestamp = Date.now();
  }

  /**
   * Retrieves sanitized recent supporters (max 10).
   * Safe for GET /api/support/recent.
   *
   * @returns {Promise<Array<object>>}
   */
  async getRecentSupporters() {
    const now = Date.now();
    // Return cached if fresh
    if (this.supportersCache.timestamp && now - this.supportersCache.timestamp < this.supportersCache.ttlMs) {
      return [...this.supportersCache.data];
    }

    if (!this.endpoint) {
      return [...this.supportersCache.data];
    }

    const fetchFn = this.customFetch || globalThis.fetch;
    if (!fetchFn) {
      return [...this.supportersCache.data];
    }

    try {
      const getUrl = `${this.endpoint}${this.endpoint.includes("?") ? "&" : "?"}action=recent-support`;
      const resp = await fetchFn(getUrl, { method: "GET" });
      if (resp.ok) {
        const json = await resp.json().catch(() => ({}));
        if (json.success && Array.isArray(json.supporters)) {
          // Sanitize every returned entry to ensure no private fields leak
          this.supportersCache.data = json.supporters.slice(0, 10).map((s) => ({
            displayName: String(s.displayName || "Supporter").trim(),
            country: String(s.country || "").trim(),
            amount: Number(s.amount) || 0,
            currency: String(s.currency || "INR").trim().toUpperCase(),
            message: String(s.message || "").trim(),
            date: String(s.date || "").split("T")[0],
          }));
          this.supportersCache.timestamp = now;
          return [...this.supportersCache.data];
        }
      }
    } catch (e) {
      // Graceful fallback on network error
    }

    return [...this.supportersCache.data];
  }

  /**
   * Queues an operation for subsequent retry.
   */
  enqueueRetry(operation, data) {
    this.retryQueue.push({
      operation,
      data,
      queuedAt: Date.now(),
      attempts: 0,
    });
  }

  /**
   * Processes the retry queue.
   */
  async processRetryQueue() {
    if (this.isRetrying || this.retryQueue.length === 0) return { processed: 0, remaining: this.retryQueue.length };
    this.isRetrying = true;

    const remaining = [];
    let processed = 0;

    while (this.retryQueue.length > 0) {
      const item = this.retryQueue.shift();
      item.attempts++;
      const res = await this._postToAppsScript(item.operation, item.data);
      if (res && res.success) {
        processed++;
      } else if (item.attempts < 5) {
        remaining.push(item);
      }
    }

    this.retryQueue = remaining;
    this.isRetrying = false;
    return { processed, remaining: this.retryQueue.length };
  }
}

module.exports = {
  SheetsClient,
};

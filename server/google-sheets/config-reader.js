"use strict";

/**
 * Server-side configuration reader for Telegram API_ID/API_HASH.
 *
 * TELEGRAM_SESSION is ALWAYS read from process.env — NEVER from Sheets,
 * never from the public sheet, never from the browser.
 *
 * TELEGRAM_API_ID and TELEGRAM_API_HASH may come from env OR from a
 * private "Config" tab in the Google Sheet, read server-side via
 * Apps Script (action=config-get) that is gated by SHEETS_INGEST_TOKEN.
 *
 * This allows operators to rotate API credentials without redeploying,
 * without ever exposing them to the browser.
 */

class ConfigReader {
  constructor(options = {}) {
    this.endpoint = options.endpoint || process.env.GOOGLE_SHEETS_ENDPOINT || "";
    this.token = options.token || process.env.SHEETS_INGEST_TOKEN || "";
    this.fetchFn = options.fetch || globalThis.fetch;
    this._cache = null;
    this._pending = null;
    this.ttlMs = options.ttlMs || 5 * 60 * 1000; // 5 min
  }

  async _fetch() {
    if (!this.endpoint || !this.token) return null;
    const sep = this.endpoint.includes("?") ? "&" : "?";
    const url = `${this.endpoint}${sep}action=config-get&token=${encodeURIComponent(this.token)}`;
    try {
      const resp = await this.fetchFn(url, { method: "GET" });
      if (!resp.ok) return null;
      const json = await resp.json().catch(() => null);
      return json && json.success ? json.config : null;
    } catch (_e) {
      return null;
    }
  }

  async getTelegramConfig() {
    if (this._cache && Date.now() - this._cache.ts < this.ttlMs) return this._cache.data;
    if (this._pending) return this._pending;
    this._pending = (async () => {
      const fromSheet = await this._fetch();
      const data = {
        apiId: String(process.env.TELEGRAM_API_ID || (fromSheet && fromSheet.TELEGRAM_API_ID) || ""),
        apiHash: String(process.env.TELEGRAM_API_HASH || (fromSheet && fromSheet.TELEGRAM_API_HASH) || ""),
        // session ONLY from environment secret
        session: String(process.env.TELEGRAM_SESSION || ""),
      };
      this._cache = { data, ts: Date.now() };
      this._pending = null;
      return data;
    })();
    return this._pending;
  }
}

module.exports = { ConfigReader };

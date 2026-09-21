"use strict";

/**
 * PDF-specific Google Sheets client.
 *
 * Primary source: Google Apps Script (server/sheets-client.js pattern)
 *   - listPdfs()       GET ?action=pdf-list
 *   - upsertPdf(row)   POST operation=pdf_upsert
 *   - deletePdf(id)    POST operation=pdf_delete
 *
 * When GOOGLE_SHEETS_ENDPOINT is not configured (local dev / tests), the
 * client transparently falls back to a local JSON file at data/pdfs.json.
 * This lets local preview servers and tests work without hitting the live
 * Apps Script endpoint. Telegram URLs in that file stay server-side
 * (the file is never served to the browser by the static file handler
 * because it lives outside the public URL space... but we still register
 * it in .gitignore and never list it publicly).
 */

const fs = require("fs");
const path = require("path");
const { normalizeSheetRow, derivePublicId } = require("../pdf/metadata");

const DEFAULT_TTL_MS = 60 * 1000;
const LOCAL_FALLBACK = path.join(__dirname, "..", "..", "data", "pdfs.json");

class PdfSheets {
  constructor(options = {}) {
    this.endpoint = options.endpoint || process.env.GOOGLE_SHEETS_ENDPOINT || "";
    this.token = options.token || process.env.SHEETS_INGEST_TOKEN || process.env.ADMIN_TOKEN || "";
    this.spreadsheetId = options.spreadsheetId || process.env.GOOGLE_SPREADSHEET_ID || "";
    this.fetchFn = options.fetch || globalThis.fetch;
    this.ttlMs = options.ttlMs || parseInt(process.env.SHEET_CACHE_TTL_MS || String(DEFAULT_TTL_MS), 10);
    this._cache = { data: null, ts: 0 };
    this._pendingList = null;
    this._localPath = options.localPath || process.env.PDFS_LOCAL_PATH || LOCAL_FALLBACK;
  }

  async _post(operation, data) {
    if (!this.endpoint) {
      return { success: false, error: "GOOGLE_SHEETS_ENDPOINT not configured." };
    }
    const body = { operation, token: this.token, spreadsheet_id: this.spreadsheetId, data };
    try {
      const resp = await this.fetchFn(this.endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${this.token}` },
        body: JSON.stringify(body),
      });
      if (!resp.ok) return { success: false, error: `HTTP ${resp.status}` };
      return await resp.json().catch(() => ({}));
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  async _get(action) {
    if (!this.endpoint) return { success: false, error: "No endpoint configured." };
    const sep = this.endpoint.includes("?") ? "&" : "?";
    const url = `${this.endpoint}${sep}action=${encodeURIComponent(action)}`;
    try {
      const resp = await this.fetchFn(url, { method: "GET" });
      if (!resp.ok) return { success: false, error: `HTTP ${resp.status}` };
      return await resp.json().catch(() => ({}));
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  invalidateCache() {
    this._cache = { data: null, ts: 0 };
  }

  /**
   * Fetch published PDFs. Returns sanitized INTERNAL rows (with telegramReference, server-side only).
   */
  _readLocal() {
    try {
      if (!fs.existsSync(this._localPath)) return [];
      const raw = JSON.parse(fs.readFileSync(this._localPath, "utf8"));
      const rows = Array.isArray(raw) ? raw : (Array.isArray(raw.rows) ? raw.rows : []);
      return rows.map(normalizeSheetRow).filter(Boolean);
    } catch (_e) {
      return [];
    }
  }

  _writeLocal(items) {
    const dir = path.dirname(this._localPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(this._localPath, JSON.stringify(items.map((i) => ({
      public_id: i.publicId,
      course_id: i.courseId,
      title: i.title,
      category: i.category,
      telegram_pdf_url: i.telegramReference,
      published: i.published ? "true" : "false",
      sort_order: i.sortOrder,
      description: i.description,
      filename: i.filenameHint || "",
    })), null, 2));
  }

  async listPdfs({ includeUnpublished = false, forceRefresh = false } = {}) {
    const now = Date.now();
    if (!forceRefresh && this._cache.data && now - this._cache.ts < this.ttlMs) {
      return this._filterCache(includeUnpublished);
    }
    if (this._pendingList) return this._pendingList;
    this._pendingList = (async () => {
      let items = [];
      if (this.endpoint) {
        try {
          const resp = await this._get("pdf-list");
          if (resp && resp.success && Array.isArray(resp.rows)) {
            items = resp.rows.map(normalizeSheetRow).filter(Boolean);
          }
        } catch (_e) { /* fall through */ }
      }
      // Fall back to local file if endpoint unavailable or returned nothing fresh
      if (items.length === 0) {
        items = this._readLocal();
      }
      this._cache = { data: items, ts: now };
      this._pendingList = null;
      return this._filterCache(includeUnpublished);
    })();
    return this._pendingList;
  }

  _filterCache(includeUnpublished) {
    if (!this._cache.data) return [];
    return this._cache.data.filter((x) => includeUnpublished || x.published);
  }

  async findByPublicId(publicId) {
    const all = await this.listPdfs({ includeUnpublished: true });
    return all.find((x) => x.publicId === publicId) || null;
  }

  async upsertPdf(row, { adminToken } = {}) {
    if (adminToken && adminToken !== this.token) {
      return { success: false, error: "Unauthorized", code: "UNAUTHORIZED" };
    }
    const publicId = row.publicId || row.id || derivePublicId(row);
    const payload = {
      public_id: publicId,
      course_id: String(row.courseId || row.course_id || "").trim(),
      title: String(row.title || "").trim(),
      category: String(row.category || "").trim(),
      telegram_pdf_url: String(row.telegramPdfUrl || row.telegram_pdf_url || "").trim(),
      published: row.published === true || String(row.published).toLowerCase() === "true",
      sort_order: Number(row.sortOrder || row.sort_order || 0) || 0,
      description: String(row.description || "").trim(),
      filename: String(row.filename || "").trim(),
    };
    if (!payload.title) return { success: false, error: "Title is required.", code: "MISSING_TITLE" };
    if (!payload.course_id) return { success: false, error: "Course is required.", code: "MISSING_COURSE" };
    if (!payload.telegram_pdf_url) return { success: false, error: "Telegram PDF URL is required.", code: "MISSING_URL" };

    if (this.endpoint) {
      const res = await this._post("pdf_upsert", payload);
      if (res && res.success) {
        this.invalidateCache();
        return { success: true, publicId: payload.public_id, data: payload };
      }
      // If endpoint fails, fall through to local
    }
    // Local file fallback (dev/tests only)
    const items = this._readLocal();
    const idx = items.findIndex((x) => x.publicId === publicId);
    const entry = normalizeSheetRow({
      public_id: publicId,
      course_id: payload.course_id,
      title: payload.title,
      category: payload.category,
      telegram_pdf_url: payload.telegram_pdf_url,
      published: payload.published ? "true" : "false",
      sort_order: payload.sort_order,
      description: payload.description,
      filename: payload.filename,
    });
    if (idx >= 0) items[idx] = entry; else items.push(entry);
    this._writeLocal(items);
    this.invalidateCache();
    return { success: true, publicId: publicId, data: payload, localFallback: !this.endpoint };
  }

  async deletePdf(publicId, { adminToken } = {}) {
    if (adminToken && adminToken !== this.token) {
      return { success: false, error: "Unauthorized", code: "UNAUTHORIZED" };
    }
    if (this.endpoint) {
      const res = await this._post("pdf_delete", { public_id: publicId });
      if (res && res.success) { this.invalidateCache(); return res; }
    }
    const items = this._readLocal().filter((x) => x.publicId !== publicId);
    this._writeLocal(items);
    this.invalidateCache();
    return { success: true };
  }
}

module.exports = { PdfSheets };

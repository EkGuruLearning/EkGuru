"use strict";

/**
 * PDF metadata helpers.
 *
 * Responsibilities:
 *  - Derive a stable publicId from a row's fields (title + course + suffix hash).
 *  - Sanitize sheet rows into server-side internal metadata (includes telegram url).
 *  - Project internal metadata into public-safe JSON (no telegram URL, no ids/refs).
 */

const crypto = require("crypto");

function slugify(input) {
  return String(input || "")
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 60) || "pdf";
}

function shortHash(input, len = 8) {
  return crypto.createHash("sha256")
    .update(String(input))
    .digest("base64url")
    .replace(/[^a-z0-9]/gi, "")
    .slice(0, len)
    .toLowerCase();
}

/**
 * Derive a stable publicId for a PDF row.
 * Uses (course, title, telegram_pdf_url) so updates to the same URL keep the same id.
 */
function derivePublicId(row) {
  const base = slugify(`${row.course_id || "course"}-${row.title || "pdf"}`);
  const hash = shortHash(`${row.course_id || ""}|${row.telegram_pdf_url || ""}|${row.title || ""}`);
  return `${base}-${hash}`;
}

/**
 * Map a raw Google Sheet row (from our Pdfs tab) into internal metadata.
 * @param {object} raw - spreadsheet row keyed by header names
 */
function normalizeSheetRow(raw) {
  const courseId = String(raw.course_id || raw.course || raw.courseId || "").trim();
  const title = String(raw.title || "").trim();
  const category = String(raw.category || courseId || "general").trim();
  const telegramUrl = String(raw.telegram_pdf_url || raw.telegram_url || "").trim();
  const publishedRaw = String(raw.published || "").trim().toLowerCase();
  const published = ["1", "true", "yes", "y", "on", "published"].includes(publishedRaw);
  const sortOrder = Number(raw.sort_order || raw.order || 0) || 0;
  const description = String(raw.description || "").trim();
  const filename = String(raw.filename || "").trim();
  const id = String(raw.public_id || raw.id || "").trim() || null;
  if (!telegramUrl) return null;
  const derived = id || derivePublicId({ course_id: courseId, title, telegram_pdf_url: telegramUrl });
  return {
    publicId: derived,
    courseId: courseId || "general",
    title: title || derived,
    category,
    description,
    sortOrder,
    published,
    filenameHint: filename || null,
    // Internal only — never expose publicly:
    telegramReference: telegramUrl,
    sourceType: "telegram",
  };
}

/**
 * Strip server-only fields from metadata before returning to browser.
 */
function toPublic(entry) {
  return {
    id: entry.publicId,
    publicId: entry.publicId,
    title: entry.title,
    category: entry.category,
    courseId: entry.courseId,
    description: entry.description || "",
    sortOrder: entry.sortOrder,
    published: Boolean(entry.published),
    sourceType: entry.sourceType || "telegram",
    filename: entry.filenameHint || null,
  };
}

module.exports = {
  derivePublicId,
  normalizeSheetRow,
  toPublic,
  slugify,
  shortHash,
};

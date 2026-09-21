"use strict";

/**
 * PDF resolver: converts a Telegram URL/reference into usable PDF metadata
 * and a document handle for streaming.
 *
 * Responsibilities:
 *  - parse the URL (via url-parser)
 *  - fetch the message via the client
 *  - reject messages without a PDF document
 *  - reject protected (no-forward) content
 *  - return an opaque PdfDocument handle for streaming
 */

const { parseTelegramUrl } = require("./url-parser");

const PDF_MIME_TYPES = new Set([
  "application/pdf",
  "application/x-pdf",
  "application/acrobat",
  "application/vnd.pdf",
  "text/pdf",
  "application/force-download",
]);

class PdfResolverError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
}

/**
 * Resolve a Telegram URL to a PDF document handle.
 * @param {EkGuruTelegramClient} client
 * @param {string} telegramUrl
 * @returns {Promise<{info: object, doc: object, ref: object}>}
 */
async function resolveTelegramPdf(client, telegramUrl, { retries = 1 } = {}) {
  const ref = parseTelegramUrl(telegramUrl);
  let result;
  try {
    result = await client.getMessage(ref);
  } catch (err) {
    throw new PdfResolverError("TG_FETCH_FAILED", `Could not fetch Telegram message: ${err.message}`);
  }
  const { message } = result;

  if (message.noforwards || (message.media && message.media.noforwards)) {
    throw new PdfResolverError("TG_PROTECTED", "This Telegram message is marked no-forward/protected and cannot be served.");
  }

  const media = message.media || {};
  if (media.className !== "MessageMediaDocument" || !media.document) {
    // Sometimes messages wrap a document with a caption; try to surface a helpful error
    if (media.className === "MessageMediaPhoto") {
      throw new PdfResolverError("TG_NOT_PDF", "The linked Telegram message contains a photo, not a PDF document.");
    }
    throw new PdfResolverError("TG_NOT_PDF", "The linked Telegram message does not contain a file document.");
  }
  const doc = media.document;
  const info = await client.getFileInfo(doc);
  // Filename/mime check; some Telegram clients send application/octet-stream with .pdf extension, so accept by extension
  const isPdfByMime = PDF_MIME_TYPES.has(String(info.mimeType).toLowerCase());
  const isPdfByName = /\.pdf$/i.test(info.name);
  if (!isPdfByMime && !isPdfByName) {
    throw new PdfResolverError("TG_NOT_PDF", `Telegram document is not a PDF (mime=${info.mimeType}, name=${info.name}).`);
  }
  return { info, doc, ref };
}

/**
 * Re-resolve the same reference after a FILE_REFERENCE_EXPIRED error.
 * @param {EkGuruTelegramClient} client
 * @param {object} ref - the original TelegramReference
 */
async function refreshTelegramDocument(client, ref) {
  // Drop entity cache entry so the resolver fetches fresh
  if (client._entityCache && typeof ref.peer === "string") {
    client._entityCache.delete(String(ref.peer).toLowerCase());
  }
  const result = await client.getMessage(ref, { forceRefresh: true });
  const media = result.message.media || {};
  if (media.className !== "MessageMediaDocument" || !media.document) {
    throw new PdfResolverError("TG_NOT_PDF", "Message no longer contains a PDF document after refresh.");
  }
  const info = await client.getFileInfo(media.document);
  return { info, doc: media.document, ref };
}

module.exports = {
  resolveTelegramPdf,
  refreshTelegramDocument,
  PdfResolverError,
};

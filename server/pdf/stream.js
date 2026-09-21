"use strict";

/**
 * HTTP PDF streaming handler.
 *
 * Streams a Telegram document on demand with HTTP Range support.
 * Never buffers the whole document in memory; chunks are forwarded to the
 * response as they arrive, with bounded chunk size (CHUNK_SIZE).
 *
 * On FILE_REFERENCE_EXPIRED the handler refreshes the document and retries
 * the current range exactly once (more would risk loops).
 */

const CHUNK_SIZE = 256 * 1024; // 256 KiB per Telegram fetch call

const { refreshTelegramDocument, PdfResolverError } = require("../telegram/resolver");

function sanitizeFilename(name) {
  return String(name || "document.pdf")
    .replace(/[\\/:*?"<>|\x00-\x1f]+/g, "_")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 120) || "document.pdf";
}

/**
 * Parse a Range header value into {start, end} inclusive 0-based bytes.
 * Returns null if the range is invalid or absent.
 */
function parseRange(header, size) {
  if (!header) return null;
  const m = /^bytes=(\d*)-(\d*)$/.exec(String(header).trim());
  if (!m) return null;
  let start = m[1] === "" ? null : parseInt(m[1], 10);
  let end = m[2] === "" ? null : parseInt(m[2], 10);
  if (start == null && end == null) return null;
  if (start == null) {
    // suffix range: last N bytes
    start = Math.max(0, size - end);
    end = size - 1;
  } else if (end == null) {
    end = size - 1;
  }
  if (!Number.isFinite(start) || !Number.isFinite(end)) return null;
  if (end < start || start < 0) return null;
  if (end >= size) end = size - 1;
  return { start, end };
}

/**
 * Stream a resolved PDF document to the response.
 *
 * @param {object} res            - Node http ServerResponse
 * @param {object} resolved       - { info, doc, ref } from resolver
 * @param {object} client         - EkGuruTelegramClient
 * @param {object} [opts]
 * @param {boolean} [opts.asDownload=false]
 * @param {string}  [opts.rangeHeader]
 * @param {function} [opts.log]
 */
async function streamPdf(res, resolved, client, opts = {}) {
  let { info, doc, ref } = resolved;
  const { asDownload = false, rangeHeader = null, log = () => {} } = opts;

  let size = info.size;
  if (typeof size !== "number" || !Number.isFinite(size) || size <= 0) {
    // Without a known size, fall back to full streaming without Range
    size = 0;
  }

  let range = size > 0 ? parseRange(rangeHeader, size) : null;
  let statusCode = range ? 206 : 200;

  const headers = {
    "Content-Type": "application/pdf",
    "Accept-Ranges": "bytes",
    "X-Content-Type-Options": "nosniff",
    "Cache-Control": "private, no-store",
  };
  const disposition = asDownload
    ? `attachment; filename="${sanitizeFilename(info.name)}"; filename*=UTF-8''${encodeURIComponent(sanitizeFilename(info.name))}`
    : "inline";
  headers["Content-Disposition"] = disposition;

  if (range) {
    headers["Content-Range"] = `bytes ${range.start}-${range.end}/${size}`;
    headers["Content-Length"] = String(range.end - range.start + 1);
  } else if (size > 0) {
    headers["Content-Length"] = String(size);
  }

  res.writeHead(statusCode, headers);

  // If range is given, stream that slice; else stream full file (respect size if known).
  let offset = range ? range.start : 0;
  const end = range ? range.end : (size > 0 ? size - 1 : Infinity);

  try {
    while (offset <= end) {
      const remaining = end === Infinity ? CHUNK_SIZE : Math.min(CHUNK_SIZE, end - offset + 1);
      let chunk;
      try {
        chunk = await client.downloadDocumentChunk(doc, { offset, limit: remaining });
      } catch (err) {
        if (err.code === "TG_FILE_REF_EXPIRED") {
          log("warn", "[pdf] file reference expired; refreshing.");
          const refreshed = await refreshTelegramDocument(client, ref);
          doc = refreshed.doc;
          info = refreshed.info;
          chunk = await client.downloadDocumentChunk(doc, { offset, limit: remaining });
        } else {
          throw err;
        }
      }
      if (!chunk || chunk.length === 0) break;
      // Ensure we don't write past end
      const writeLen = Math.min(chunk.length, end - offset + 1);
      if (!res.write(chunk.slice(0, writeLen))) {
        // backpressure
        await new Promise((r) => res.once("drain", r));
      }
      offset += writeLen;
      if (writeLen < chunk.length) break;
    }
    res.end();
  } catch (err) {
    log("error", "[pdf] stream error", err.code || "", err.message);
    try {
      if (!res.headersSent) {
        res.writeHead(502, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ success: false, error: "PDF stream failed", code: err.code || "STREAM_FAILED" }));
      } else {
        res.destroy();
      }
    } catch (_) {}
  }
}

module.exports = {
  streamPdf,
  parseRange,
  sanitizeFilename,
};

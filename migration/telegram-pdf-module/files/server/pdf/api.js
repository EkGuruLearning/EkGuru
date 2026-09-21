"use strict";

/**
 * PDF HTTP API routes for EkGuru.
 *
 * Mounted by server.js. Returns true if the request was handled.
 *
 * Public (no auth):
 *   GET /api/pdfs
 *   GET /api/pdfs/:publicId
 *   GET /pdf/:publicId             (inline)
 *   GET /pdf/:publicId/download    (attachment)
 *
 * Admin (requires Bearer === SHEETS_INGEST_TOKEN):
 *   GET  /api/admin/pdfs
 *   POST /api/admin/pdfs           (upsert)
 *   POST /api/admin/pdfs/delete
 *
 * Internal / diagnostic (no token — does not expose secrets):
 *   GET /api/pdf/health
 */

const { toPublic } = require("./metadata");
const { streamPdf } = require("./stream");
const { parseTelegramUrl } = require("../telegram/url-parser");
const { resolveTelegramPdf, PdfResolverError } = require("../telegram/resolver");

function sendJson(res, status, data, extra = {}) {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store, private");
  for (const [k, v] of Object.entries(extra)) res.setHeader(k, v);
  res.end(JSON.stringify(data));
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => {
      try {
        const raw = Buffer.concat(chunks).toString("utf8");
        resolve(raw ? JSON.parse(raw) : {});
      } catch (e) {
        reject(e);
      }
    });
    req.on("error", reject);
  });
}

function checkAdmin(req) {
  const token = process.env.SHEETS_INGEST_TOKEN || process.env.ADMIN_TOKEN || "";
  if (!token) return false;
  const auth = req.headers.authorization || "";
  const m = /^Bearer\s+(.+)$/i.exec(auth);
  return m && m[1] === token;
}

/**
 * @param {import('http').IncomingMessage} req
 * @param {import('http').ServerResponse} res
 * @param {object} ctx
 * @param {import('../telegram/client').EkGuruTelegramClient} ctx.client
 * @param {import('../google-sheets/pdf-sheets').PdfSheets} ctx.pdfSheets
 */
async function handlePdfRequest(req, res, ctx) {
  const { client, pdfSheets } = ctx;
  const parsed = new URL(req.url, `http://${req.headers.host || "localhost"}`);
  const pathname = parsed.pathname.replace(/\/+$/, "");
  const log = ctx.log || ((...a) => {});

  // Health
  if (req.method === "GET" && (pathname === "/api/pdf/health" || pathname === "/api/pdfs/health")) {
    sendJson(res, 200, {
      success: true,
      service: "EkGuru PDF Gateway",
      mockMode: client && client.mockMode === true,
      connected: client && client.isReady(),
      timestamp: new Date().toISOString(),
    });
    return true;
  }

  // Public PDF list
  if (req.method === "GET" && pathname === "/api/pdfs") {
    try {
      const all = await pdfSheets.listPdfs();
      const publicItems = all
        .sort((a, b) => (a.sortOrder - b.sortOrder) || a.title.localeCompare(b.title))
        .map(toPublic);
      sendJson(res, 200, { success: true, items: publicItems, count: publicItems.length }, {
        "Cache-Control": "public, max-age=60, s-maxage=60",
      });
    } catch (err) {
      sendJson(res, 500, { success: false, error: "Failed to load PDF list." });
    }
    return true;
  }

  // Public single PDF metadata
  let m;
  if (req.method === "GET" && (m = /^\/api\/pdfs\/([^/]+)$/.exec(pathname))) {
    const publicId = decodeURIComponent(m[1]);
    const item = await pdfSheets.findByPublicId(publicId);
    if (!item || !item.published) {
      sendJson(res, 404, { success: false, error: "PDF not found." });
      return true;
    }
    sendJson(res, 200, { success: true, item: toPublic(item) }, {
      "Cache-Control": "public, max-age=60",
    });
    return true;
  }

  // Viewer HTML: /pdf/<id>  OR  /pdf/<id>/  -> HTML page with embed pointing to /pdf/<id>/raw
  if (req.method === "GET" && (m = /^\/pdf\/([^/]+?)(?:\/(?:index\.html)?)?$/.exec(pathname))) {
    const accept = String(req.headers.accept || "");
    // If client is asking for the PDF directly (e.g. iframe/object with no html accept), stream.
    if (accept.indexOf("application/pdf") !== -1 && accept.indexOf("text/html") === -1) {
      return servePdf(req, res, m[1], { client, pdfSheets, asDownload: false, log });
    }
    return servePdfViewer(req, res, m[1], { pdfSheets });
  }
  // Raw inline PDF stream: /pdf/<id>/raw
  if (req.method === "GET" && (m = /^\/pdf\/([^/]+)\/raw$/.exec(pathname))) {
    return servePdf(req, res, m[1], { client, pdfSheets, asDownload: false, log });
  }
  // Download: /pdf/<id>/download
  if (req.method === "GET" && (m = /^\/pdf\/([^/]+)\/download$/.exec(pathname))) {
    return servePdf(req, res, m[1], { client, pdfSheets, asDownload: true, log });
  }

  // -------- Admin routes --------
  if (pathname.startsWith("/api/admin/pdfs")) {
    if (!checkAdmin(req)) {
      sendJson(res, 401, { success: false, error: "Unauthorized admin request." });
      return true;
    }

    // List (include unpublished)
    if (req.method === "GET" && pathname === "/api/admin/pdfs") {
      const all = await pdfSheets.listPdfs({ includeUnpublished: true, forceRefresh: true });
      sendJson(res, 200, { success: true, items: all.map(toPublic), count: all.length });
      return true;
    }

    // Delete
    if (req.method === "POST" && pathname === "/api/admin/pdfs/delete") {
      let body;
      try { body = await readBody(req); } catch (_e) { sendJson(res, 400, { success: false, error: "Malformed body." }); return true; }
      if (!body.publicId) { sendJson(res, 400, { success: false, error: "publicId required." }); return true; }
      const result = await pdfSheets.deletePdf(body.publicId);
      sendJson(res, result.success ? 200 : 500, result);
      return true;
    }

    // Upsert — additionally validate the Telegram URL against real client (if not mock)
    if (req.method === "POST" && pathname === "/api/admin/pdfs") {
      let body;
      try { body = await readBody(req); } catch (_e) { sendJson(res, 400, { success: false, error: "Malformed body." }); return true; }
      // Validate URL shape up front
      try {
        parseTelegramUrl(body.telegramPdfUrl || body.telegram_pdf_url || "");
      } catch (err) {
        sendJson(res, 400, { success: false, error: err.message, code: "BAD_TELEGRAM_URL" });
        return true;
      }
      // Try to resolve PDF with Telegram client (if configured), catch errors
      if (client && client.isReady() && !client.mockMode) {
        try {
          await resolveTelegramPdf(client, body.telegramPdfUrl || body.telegram_pdf_url);
        } catch (err) {
          if (err instanceof PdfResolverError) {
            sendJson(res, 400, { success: false, error: err.message, code: err.code });
            return true;
          }
          // connection errors still allow save? safer to reject if real client
          sendJson(res, 502, { success: false, error: `Telegram validation failed: ${err.message}` });
          return true;
        }
      }
      const result = await pdfSheets.upsertPdf(body);
      sendJson(res, result.success ? 200 : 400, result);
      return true;
    }
  }

  return false;
}

/**
 * Serve an HTML viewer page for a PDF. This page loads the PDF from
 * /pdf/<publicId>/raw (same origin) in an <embed>/<iframe>, keeping the
 * browser PDF viewer but never exposing the Telegram source URL.
 */
async function servePdfViewer(req, res, publicId, { pdfSheets }) {
  publicId = decodeURIComponent(publicId);
  const item = await pdfSheets.findByPublicId(publicId);
  if (!item || !item.published) {
    res.statusCode = 404;
    res.setHeader("Content-Type", "text/html; charset=utf-8");
    res.end("<!doctype html><meta charset=utf-8><title>PDF not found</title><h1>PDF not found</h1><p>The PDF you requested does not exist or has not been published.</p><p><a href=\"/courses/pdfs/\">Back to PDF Library</a></p>");
    return true;
  }
  res.statusCode = 200;
  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.setHeader("Cache-Control", "public, max-age=60");
  res.setHeader("Content-Security-Policy", "default-src 'self'; object-src 'self'; frame-ancestors 'self'; base-uri 'self';");
  const title = String(item.title || "PDF").replace(/[&<>"]/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const cat = String(item.category || item.courseId || "").replace(/[&<>"]/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const raw = `/pdf/${encodeURIComponent(publicId)}/raw`;
  const dl = `/pdf/${encodeURIComponent(publicId)}/download`;
  res.end(`<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>${title} | PDF | EkGuru</title>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#f5f5fb;color:#111}
header{display:flex;align-items:center;gap:12px;padding:12px 16px;background:#fff;border-bottom:1px solid #e6e6ee;position:sticky;top:0;z-index:2}
header .brand{font-weight:800;color:#5736d8;text-decoration:none}
header .sp{flex:1}
header a.btn,header button{background:#5736d8;color:#fff;border:0;padding:8px 14px;border-radius:8px;font-weight:600;cursor:pointer;text-decoration:none;font-size:.9rem}
header a.btn.ghost{background:#fff;color:#111;border:1px solid #e6e6ee}
.wrap{padding:0}
.embed{width:100%;height:calc(100vh - 62px);border:0;background:#333}
.meta{padding:8px 16px 0;font-size:.85rem;color:#4a4a55}
.meta .cat{text-transform:uppercase;letter-spacing:.04em;color:#5736d8;font-weight:700;font-size:.72rem;margin-right:8px}
h1{font-size:1.05rem;margin:2px 16px 8px}
.fallback{padding:30px 16px;text-align:center}
</style>
</head><body>
<header>
  <a class="brand" href="/">EkGuru</a>
  <nav><a href="/courses/pdfs/" class="btn ghost">All PDFs</a></nav>
  <div class="sp"></div>
  <a class="btn" href="${dl}">Download</a>
</header>
<div class="meta"><span class="cat">${cat}</span></div>
<h1>${title}</h1>
<div class="wrap">
  <object class="embed" type="application/pdf" data="${raw}" aria-label="${title}">
    <div class="fallback">
      <p>Your browser cannot display the PDF inline.</p>
      <p><a class="btn" href="${dl}">Download PDF</a></p>
    </div>
  </object>
</div>
</body></html>`);
  return true;
}

async function servePdf(req, res, publicId, { client, pdfSheets, asDownload, log }) {
  publicId = decodeURIComponent(publicId);
  const item = await pdfSheets.findByPublicId(publicId);
  if (!item) {
    sendJson(res, 404, { success: false, error: "PDF not found." });
    return true;
  }
  if (!item.published) {
    sendJson(res, 404, { success: false, error: "PDF not found." });
    return true;
  }

  // Ensure client is connected
  try {
    await client.connect();
  } catch (err) {
    log("error", "[pdf] client not connected", err.message);
    sendJson(res, 503, { success: false, error: "PDF gateway unavailable." });
    return true;
  }

  // Mock-mode production guard: if NODE_ENV=production and mockMode, refuse
  if (client.mockMode && process.env.NODE_ENV === "production" && process.env.ALLOW_MOCK_TELEGRAM === "true") {
    sendJson(res, 503, { success: false, error: "Server misconfigured (mock mode enabled in production)." });
    return true;
  }

  let resolved;
  try {
    resolved = await resolveTelegramPdf(client, item.telegramReference);
  } catch (err) {
    const code = err.code || "TG_RESOLVE_FAILED";
    const status = code === "TG_PROTECTED" ? 403 : code === "TG_NOT_PDF" ? 400 : code === "TG_MSG_NOT_FOUND" ? 404 : 502;
    sendJson(res, status, { success: false, error: err.message, code });
    return true;
  }

  const rangeHeader = req.headers.range || null;
  await streamPdf(res, resolved, client, { asDownload, rangeHeader, log });
  return true;
}

module.exports = { handlePdfRequest };

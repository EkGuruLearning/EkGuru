#!/usr/bin/env node
/**
 * EkGuru — Unified HTTP Server (static + Payments API + PDF Gateway)
 *
 * RUNTIME ARCHITECTURE:
 * - Static site (GitHub Pages compatible) is served from the repo root.
 * - Payments & support API  -> Google Apps Script backend (production) or
 *                              local mock (NODE_ENV != production).
 * - PDF Gateway (Telegram)  -> runs HERE on the Node.js server. The
 *                              Google Sheet "Pdfs" tab is the metadata
 *                              source (read via Apps Script on the server
 *                              side), Telegram MTProto streams PDFs on
 *                              demand to the browser. The browser never
 *                              calls Telegram directly and never sees the
 *                              source Telegram URL.
 */

"use strict";

const http = require("http");
const fs = require("fs");
const path = require("path");
const { RazorpayService } = require("./razorpay-service");
const { handleApiRequest } = require("./api");
const { EkGuruTelegramClient } = require("./telegram/client");
const { PdfSheets } = require("./google-sheets/pdf-sheets");
const { ConfigReader } = require("./google-sheets/config-reader");
const { handlePdfRequest } = require("./pdf/api");

const PORT = parseInt(process.env.PORT || "3000", 10);
const HOST = "0.0.0.0";
const ROOT_DIR = path.resolve(__dirname, "..");

const service = new RazorpayService({
  keyId: process.env.RAZORPAY_KEY_ID || "rzp_test_ekguru_preview",
  keySecret: process.env.RAZORPAY_KEY_SECRET || "mock_secret",
  webhookSecret: process.env.RAZORPAY_WEBHOOK_SECRET || "mock_webhook_secret",
  mockMode: !process.env.RAZORPAY_KEY_ID,
});

const configReader = new ConfigReader();
const pdfSheets = new PdfSheets();

// Lazily construct Telegram client after config resolves
let _tgClient = null;
async function getTelegramClient() {
  if (_tgClient) return _tgClient;
  const cfg = await configReader.getTelegramConfig();
  _tgClient = new EkGuruTelegramClient({
    apiId: cfg.apiId,
    apiHash: cfg.apiHash,
    sessionString: cfg.session,
    mockAllowed: String(process.env.ALLOW_MOCK_TELEGRAM || "false").toLowerCase() === "true",
    logger: (level, ...args) => console.log(`[telegram:${level}]`, ...args),
  });
  return _tgClient;
}

const MIME_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".mjs": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".xml": "application/xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".ico": "image/x-icon",
  ".webp": "image/webp",
  ".webmanifest": "application/manifest+json",
  ".pdf": "application/pdf",
};

function setCommonSecurityHeaders(res) {
  // Least-privilege defaults. Do NOT weaken these for iframe embedding.
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
  res.setHeader("X-Frame-Options", "SAMEORIGIN");
  // PDF gateway responses should not be embeddable on third-party sites.
  res.setHeader("Permissions-Policy", "geolocation=(), microphone=(), camera=()");
}

function serveStaticFile(req, res) {
  const parsedUrl = new URL(req.url, `http://${req.headers.host || "localhost"}`);
  let pathname = decodeURIComponent(parsedUrl.pathname);

  if (pathname.endsWith("/")) pathname += "index.html";

  const safePath = path.normalize(path.join(ROOT_DIR, pathname));
  if (!safePath.startsWith(ROOT_DIR)) {
    res.statusCode = 403;
    res.end("Forbidden");
    return;
  }

  try {
    const stat = fs.statSync(safePath);
    if (stat.isDirectory()) {
      res.statusCode = 301;
      res.setHeader("Location", pathname + "/");
      res.end();
      return;
    }
  } catch (e) {
    const indexPath = path.join(safePath, "index.html");
    if (fs.existsSync(indexPath)) {
      res.statusCode = 301;
      res.setHeader("Location", pathname + "/");
      res.end();
      return;
    }
  }

  fs.readFile(safePath, (err, data) => {
    if (err) {
      if (err.code === "ENOENT") {
        const notFoundPath = path.join(ROOT_DIR, "404.html");
        if (fs.existsSync(notFoundPath)) {
          res.statusCode = 404;
          setCommonSecurityHeaders(res);
          res.setHeader("Content-Type", "text/html; charset=utf-8");
          res.end(fs.readFileSync(notFoundPath));
          return;
        }
        res.statusCode = 404;
        res.end("File not found");
      } else {
        res.statusCode = 500;
        res.end("Server Error");
      }
      return;
    }
    setCommonSecurityHeaders(res);
    const ext = path.extname(safePath).toLowerCase();
    res.setHeader("Content-Type", MIME_TYPES[ext] || "application/octet-stream");
    res.statusCode = 200;
    res.end(data);
  });
}

const server = http.createServer(async (req, res) => {
  setCommonSecurityHeaders(res);
  try {
    const client = await getTelegramClient();

    // PDF routes first — they may stream binary
    const handledPdf = await handlePdfRequest(req, res, {
      client,
      pdfSheets,
      log: (level, ...args) => console.log(`[pdf:${level}]`, ...args),
    });
    if (handledPdf) return;

    const handled = await handleApiRequest(req, res, service);
    if (handled) return;

    serveStaticFile(req, res);
  } catch (err) {
    console.error("[EkGuru Server Error]", err);
    if (!res.headersSent) {
      res.statusCode = 500;
      res.setHeader("Content-Type", "application/json");
      res.end(JSON.stringify({ error: "Internal Server Error", message: err.message }));
    } else {
      res.destroy();
    }
  }
});

if (require.main === module) {
  // Attempt to connect Telegram client early so logs show status; don't block startup if misconfig.
  getTelegramClient().then((c) => c.connect().catch((e) => {
    console.warn("[telegram] not connected (PDF routes will 503 until configured):", e.message);
  }));

  server.listen(PORT, HOST, () => {
    console.log(`[EkGuru Server] Listening on http://${HOST}:${PORT}`);
    console.log(`[EkGuru Server] Static site root: ${ROOT_DIR}`);
    console.log(`[EkGuru Server] PDF gateway:   /pdf/<publicId> and /pdf/<publicId>/download`);
    console.log(`[EkGuru Server] PDF API:       /api/pdfs, /api/pdf/health`);
    console.log(`[EkGuru Server] Payments API:  /api/payments/razorpay/*`);
  });
}

module.exports = {
  server,
  service,
  pdfSheets,
  getTelegramClient,
};

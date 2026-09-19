#!/usr/bin/env node
/**
 * EkGuru — Local Development & Test Preview Server
 *
 * NOTE ON RUNTIME ARCHITECTURE:
 * - PRODUCTION BACKEND: Google Apps Script Web App (NOT Cloudflare Worker).
 *   Production endpoint: https://script.google.com/macros/s/AKfycbz8u_rBr2o4VPgmQgaweswLWKdYb-MMGrsa7WfckTCruLP-ZEasWnpkqJrZHux5Y8_4zA/exec
 * - LOCAL DEV & PREVIEW: This Node.js server (`server/server.js`) is used strictly for local development,
 *   automated browser QA, and sandbox mock testing. It serves static assets and mock API endpoints.
 *
 * Serves the payment API endpoints:
 * - GET  /api/payments/razorpay/currencies
 * - POST /api/payments/razorpay/order
 * - POST /api/payments/razorpay/verify
 * - POST /api/payments/razorpay/webhook
 * - GET  /api/support/recent
 * - GET  /api/payments/health
 */

"use strict";

const http = require("http");
const fs = require("fs");
const path = require("path");
const { RazorpayService } = require("./razorpay-service");
const { handleApiRequest } = require("./api");

const PORT = parseInt(process.env.PORT || "3000", 10);
const HOST = "0.0.0.0";
const ROOT_DIR = path.resolve(__dirname, "..");

const service = new RazorpayService({
  keyId: process.env.RAZORPAY_KEY_ID || "",
  keySecret: process.env.RAZORPAY_KEY_SECRET || "",
  webhookSecret: process.env.RAZORPAY_WEBHOOK_SECRET || "",
});

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
};

/**
 * Serves static files safely without path traversal.
 */
function serveStaticFile(req, res) {
  const parsedUrl = new URL(req.url, `http://${req.headers.host || "localhost"}`);
  let pathname = decodeURIComponent(parsedUrl.pathname);

  // Default to index.html for root or directory paths
  if (pathname.endsWith("/")) {
    pathname += "index.html";
  }

  // Prevent directory traversal attacks
  const safePath = path.normalize(path.join(ROOT_DIR, pathname));
  if (!safePath.startsWith(ROOT_DIR)) {
    res.statusCode = 403;
    res.end("Forbidden");
    return;
  }

  // If path is a directory without trailing slash, redirect with trailing slash
  try {
    const stat = fs.statSync(safePath);
    if (stat.isDirectory()) {
      res.statusCode = 301;
      res.setHeader("Location", pathname + "/");
      res.end();
      return;
    }
  } catch (e) {
    // If exact path not found, try appending /index.html
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
        // Fallback to 404.html if available
        const notFoundPath = path.join(ROOT_DIR, "404.html");
        if (fs.existsSync(notFoundPath)) {
          res.statusCode = 404;
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

    const ext = path.extname(safePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || "application/octet-stream";
    res.statusCode = 200;
    res.setHeader("Content-Type", contentType);
    res.end(data);
  });
}

const server = http.createServer(async (req, res) => {
  try {
    const handled = await handleApiRequest(req, res, service);
    if (handled) return;

    serveStaticFile(req, res);
  } catch (err) {
    console.error("[EkGuru Server Error]", err);
    res.statusCode = 500;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({ error: "Internal Server Error", message: err.message }));
  }
});

if (require.main === module) {
  server.listen(PORT, HOST, () => {
    console.log(`[EkGuru Payments Server] Listening on http://${HOST}:${PORT}`);
    console.log(`[EkGuru Payments Server] API base: http://${HOST}:${PORT}/api/payments/razorpay/`);
  });
}

module.exports = {
  server,
  service,
};

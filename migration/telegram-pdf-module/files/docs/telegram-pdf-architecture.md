# EkGuru Telegram PDF Gateway — Architecture

EkGuru serves Telegram-hosted PDFs directly from `ekguru.shop` without
exposing Telegram URLs to visitors and without requiring a Telegram
account to view or download them.

## Runtime components (all inside EkGuru)

```
┌────────────────── EkGuru (single repository) ──────────────────┐
│                                                                 │
│  Browser (visitor)                                              │
│   ├─ GET /courses/pdfs/          PDF catalogue page             │
│   ├─ GET /pdf/<publicId>/        HTML viewer page               │
│   ├─ GET /pdf/<publicId>/raw     inline PDF stream              │
│   └─ GET /pdf/<publicId>/download  attachment download          │
│            │                                                    │
│            ▼ same origin                                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Node.js server (server/server.js)                        │  │
│  │   ├─ /api/pdfs                public JSON (safe fields)  │  │
│  │   ├─ /api/admin/pdfs*         token-gated admin ops      │  │
│  │   ├─ PdfSheets (server/google-sheets/pdf-sheets.js)      │  │
│  │   │     └─ Apps Script endpoint (production) or          │  │
│  │   │        data/pdfs.json (local dev fallback)           │  │
│  │   ├─ TelegramClient (server/telegram/*)                  │  │
│  │   │     └─ MTProto via teleproto (maintained GramJS fork)│  │
│  │   └─ PdfStreamer (server/pdf/stream.js)                  │  │
│   │          └─ Range-aware chunked streaming (256 KiB)     │  │
│  └───────────────────────────────────────────────────────────┘  │
│            │                                                    │
│            ├────────► Google Sheet (private)                    │
│            │           ├─ Payments, Customers, Refunds…         │
│            │           ├─ Pdfs  (admin adds rows here)          │
│            │           └─ Config (TELEGRAM_API_ID/_HASH)        │
│            │                                                    │
│            └────────► Telegram MTProto (server-side only)       │
│                      - resolves the message/document            │
│                      - rejects no-forward / protected content   │
│                      - handles FILE_REFERENCE_EXPIRED refresh   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Guarantees

- **No Telegram URLs in public responses.** The public API `/api/pdfs`
  projects server-side metadata through `toPublic()` in
  `server/pdf/metadata.js`, which strips `telegramReference`, chat ids,
  message ids, and file references.
- **No browser → Telegram traffic.** Browsers only ever request
  `ekguru.shop`. The Node server talks MTProto to Telegram.
- **No arbitrary proxy.** There is no `/proxy?url=...`. Requests are
  always resolved from a `publicId` that maps server-side to a known
  Telegram reference vetted by the admin.
- **Protected content rejected.** Messages with Telegram's
  `noforwards` flag return 403 and are not served.
- **No permanent PDF copy required.** PDFs stream directly from
  Telegram on demand; no S3/R2/disk blob is created by default. A
  bounded short-lived in-memory cache could be added later, but the
  default architecture is zero-permanent-storage.
- **Range requests.** `/pdf/<id>/raw` supports `Range: bytes=...` with
  `206 Partial Content`, `Content-Range`, `Accept-Ranges: bytes`,
  enabling browser PDF viewers to seek without downloading the whole
  file.
- **File reference expiry handled.** On `FILE_REFERENCE_EXPIRED`, the
  server re-fetches the message, obtains a fresh document reference,
  and retries the current chunk exactly once.

## Key modules

| Path | Purpose |
| --- | --- |
| `server/server.js` | HTTP server — static + payment + PDF routes. |
| `server/telegram/url-parser.js` | Parses `t.me/...` and `t.me/c/...` links. |
| `server/telegram/client.js` | MTProto client wrapper (real + mock). |
| `server/telegram/resolver.js` | Validates messages contain a non-protected PDF. |
| `server/pdf/stream.js` | HTTP Range streaming; filename sanitisation; retry on expiry. |
| `server/pdf/metadata.js` | `publicId` derivation, row normalization, public projection. |
| `server/google-sheets/pdf-sheets.js` | Pdfs tab read/write with local dev fallback. |
| `server/google-sheets/config-reader.js` | Reads non-secret Telegram config server-side. |
| `server/pdf/api.js` | HTTP routes for public, viewer, download, admin. |
| `apps-script/Code.gs` | Apps Script additions: `pdf-list`, `pdf_upsert`, `pdf_delete`, `config-get`, `Pdfs` + `Config` tabs. |
| `scripts/telegram-login.js` | One-time CLI to create `TELEGRAM_SESSION`. |
| `courses/pdfs/index.html` | Public PDF library page. |
| `admin-pdfs.html` | Admin PDF publisher. |

## Security rules

- `TELEGRAM_SESSION` is **only** read from `process.env`. It is never
  stored in Google Sheets, never returned in any API response, never
  logged, never committed.
- `TELEGRAM_API_ID`/`TELEGRAM_API_HASH` may be set via env or a
  private `Config` tab in the Google Sheet, read server-side through
  Apps Script using the `SHEETS_INGEST_TOKEN`.
- Admin routes (`/api/admin/pdfs*`) require a bearer token equal to
  `SHEETS_INGEST_TOKEN` (same token already used to gate Apps Script
  writes).
- `ALLOW_MOCK_TELEGRAM=true` is only allowed in dev/test; if
  `NODE_ENV=production` the server refuses PDF requests while in mock
  mode.
- Standard security headers (`X-Content-Type-Options`,
  `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy`) are applied
  globally. The PDF viewer uses a restrictive CSP.

# Deploying EkGuru with the PDF gateway

The EkGuru Node server now hosts three things in one process:

1. Static site assets (the GitHub Pages-compatible frontend).
2. The payments & support API (forwarded to Apps Script in production).
3. The Telegram PDF gateway.

## Environment variables

| Variable | Required | Purpose |
| --- | --- | --- |
| `PORT` | optional | Listen port (default `3000`). |
| `NODE_ENV` | recommended | Set to `production` in production (enables mock guard). |
| `GOOGLE_SHEETS_ENDPOINT` | required | Apps Script Web App URL. |
| `GOOGLE_SPREADSHEET_ID` | optional | Spreadsheet id (defaults to the main EkGuru sheet). |
| `SHEETS_INGEST_TOKEN` | required | Shared secret for admin and server-to-server Apps Script calls. |
| `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_WEBHOOK_SECRET` | for payments | As before. |
| `TELEGRAM_API_ID`, `TELEGRAM_API_HASH` | for PDFs | Can be set in env OR in the `Config` tab. |
| `TELEGRAM_SESSION` | for PDFs | **Secret.** Server env only. |
| `ALLOW_MOCK_TELEGRAM` | dev/test only | Must be `false` or unset in production. |
| `SHEET_CACHE_TTL_MS` | optional | Cache TTL for PDF list (default 60000 = 60s). |

## Setup checklist

1. Deploy this Node server behind your usual reverse proxy/host,
   bound to `0.0.0.0:$PORT` and serving traffic for `ekguru.shop`.
2. In the Google Sheet, open the Apps Script editor and paste the
   updated `apps-script/Code.gs` from this repo (the new functions are
   appended at the bottom; existing payment logic is unchanged).
3. Re-deploy the Apps Script Web App (execute as "Me", access "Anyone
   with the link" — same as before). The token is still enforced
   server-side for write operations.
4. Run `npm install` then `node scripts/telegram-login.js` locally to
   generate `TELEGRAM_SESSION` (see `docs/telegram-auth-setup.md`).
5. Add the session to your production environment (do not commit it).
6. Add `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` either to env or to
   the `Config` tab as key/value rows.
7. Start the server: `NODE_ENV=production npm start`.
8. Smoke test:
   - `GET /api/pdfs` returns `{"success":true,"items":[...]}`.
   - `GET /api/pdf/health` returns `{"mockMode":false,"connected":true}`.
   - Publish a real PDF via `/admin.html (Content → PDF Publisher tab)` and preview it.

## PDF page routing

All PDF traffic is same-origin:

- Library: `/courses/pdfs/`
- Viewer:  `/pdf/<publicId>/`
- Raw PDF: `/pdf/<publicId>/raw` (used by viewer `<object>`)
- Download: `/pdf/<publicId>/download`

Because the existing site is static, you need to route the wildcard
`/pdf/*` path through the Node server rather than serving it from
static hosting. If you currently host ekguru.shop on GitHub Pages,
deploy the Node server under the same apex (e.g. via a subdomain
proxy, Cloudflare Worker to the Node origin, or moving hosting to a
Node-capable platform).

## Storage costs

None beyond the existing static hosting and the Node runtime:

- PDFs stay in Telegram.
- No S3/R2 bucket.
- No database blob.
- The only state is the Google Sheet row (metadata) and the
  `TELEGRAM_SESSION` secret.

## Cache behaviour

- PDF list: in-memory, `SHEET_CACHE_TTL_MS` (default 60s).
- PDF streams: not cached (header `Cache-Control: private, no-store`)
  because content can be updated by the channel admin and because we
  stream on demand from Telegram. Public metadata has `max-age=60`.

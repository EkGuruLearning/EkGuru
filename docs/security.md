# EkGuru PDF Gateway — Security Notes

## Source URL secrecy

The public must never see a Telegram URL for a PDF. The invariants:

1. **Public API responses** (from `/api/pdfs`) go through
   `toPublic()` in `server/pdf/metadata.js`, which strips:
   - `telegramReference`
   - `telegram_pdf_url`
   - chat ids / message ids / file references
2. **The HTML viewer** (`/pdf/<publicId>/`) only embeds
   `/pdf/<publicId>/raw` on the same origin. It does not print the URL
   anywhere in the DOM.
3. **Download response** uses only the sanitized filename; no
   `X-Original-URL`, no `Referer`, no Telegram header is forwarded.
4. **`Referrer-Policy: strict-origin-when-cross-origin`** is set
   globally so that if a viewer follows an off-site link, the full URL
   (which may contain the publicId) is not leaked cross-origin — and
   the publicId alone never reveals the Telegram source.

A public JSON / HTML response should never match any of:

- `t.me/`
- `telegramLink`
- `telegram_pdf_url`
- `telegramReference`
- `chat_id`
- `message_id`
- `file_reference`
- `/api/resolve`
- `/go?url=`
- `telegram-gateway`
- `localhost:8000`

The audit command:

```bash
grep -rE "t\.me/|telegramLink|telegram_pdf_url|telegramReference|chat_id|message_id|file_reference|/api/resolve|telegram-gateway|localhost:8000" \
  --include="*.html" --include="*.js" --include="*.json" --include="*.css" \
  courses/ js/ admin-pdfs.html index.html 2>/dev/null
```

Only `server/` and `apps-script/` may legitimately reference those
strings, and those directories are never served to browsers as source.

## Admin auth

- `/api/admin/pdfs` and `/api/admin/pdfs/delete` require
  `Authorization: Bearer <SHEETS_INGEST_TOKEN>`.
- The Apps Script endpoints (`pdf-list`, `pdf_upsert`,
  `pdf_delete`, `config-get`) verify the same token with a
  constant-time comparison before returning anything.
- The token is **never** accepted as a query parameter (existing
  pattern in Code.gs, applied for new actions too), because query
  strings end up in reverse-proxy logs.

## Telegram secrets

- `TELEGRAM_SESSION` is only ever read from the environment. It must
  not be written to disk except for the `.telegram-session` helper
  file created by `scripts/telegram-login.js` (chmod 600, gitignored).
- `TELEGRAM_API_ID` / `TELEGRAM_API_HASH` may come from the private
  `Config` tab, but only the Node server reads that (server-side,
  gated by `SHEETS_INGEST_TOKEN`). Browsers never see it.
- The logger is configured to `"none"` for teleproto; lib-level logs
  are silenced so file reference bytes and session bytes never appear
  in logs.
- Errors returned to browsers are sanitized to stable codes
  (`TG_PROTECTED`, `TG_NOT_PDF`, `TG_MSG_NOT_FOUND`, `STREAM_FAILED`)
  rather than reflecting raw Telegram messages.

## Content protection

Before serving any document the resolver checks:

- `message.noforwards` and `media.noforwards` → 403
- document must exist and be a PDF (by mime or `.pdf` extension)

Self-destruct / disappearing messages are not served by Telegram's
API at all (they are unavailable to regular clients), so there is
nothing for EkGuru to forward.

## Headers

- `X-Content-Type-Options: nosniff` (global)
- `X-Frame-Options: SAMEORIGIN` (global)
- `Referrer-Policy: strict-origin-when-cross-origin` (global)
- `Permissions-Policy: geolocation=(), microphone=(), camera=()` (global)
- PDF viewer page adds:
  `Content-Security-Policy: default-src 'self'; object-src 'self'; frame-ancestors 'self';`
- The PDF stream never sets permissive CORS; all consumer requests
  are same-origin. There is no `Access-Control-Allow-Origin: *`.

## Production mock-mode guard

If `NODE_ENV=production` and `ALLOW_MOCK_TELEGRAM=true`, all PDF
requests return 503 with a clear misconfiguration message, preventing
accidental deployment of the test mock.

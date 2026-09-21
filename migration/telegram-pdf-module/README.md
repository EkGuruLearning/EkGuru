# Telegram PDF Module — Migration Bundle

This bundle contains the files that were integrated into EkGuru to
add the Telegram-served PDF gateway. The original EkguruTelegram
repository was not present in the workspace at the time of migration
(clone returned 404), so the working code was written against the
specifications in the arena brief and the maintained teleproto
(GramJS fork) MTProto client.

## Source reference

- Specification: this task brief (sections 0–48).
- Library used: `teleproto` (actively maintained GramJS fork). See
  https://www.npmjs.com/package/teleproto

## Files included in `files/`

Relative paths are relative to the EkGuru repo root.

| Source in bundle | Destination in EkGuru | Why it exists |
| --- | --- | --- |
| `server/telegram/url-parser.js` | `server/telegram/url-parser.js` | Parses `t.me/<user>/<mid>` and `t.me/c/<id>/<mid>` public URLs. |
| `server/telegram/client.js` | `server/telegram/client.js` | MTProto client wrapper (real + mock modes, file download chunks). |
| `server/telegram/resolver.js` | `server/telegram/resolver.js` | Resolves a parsed URL to a PDF document; rejects protected content. |
| `server/pdf/stream.js` | `server/pdf/stream.js` | HTTP Range streaming, filename sanitisation, file-reference-expiry retry. |
| `server/pdf/metadata.js` | `server/pdf/metadata.js` | `publicId` derivation, row normalization, public projection (strips Telegram URLs). |
| `server/pdf/api.js` | `server/pdf/api.js` | HTTP router: public list, viewer HTML, raw stream, download, admin upsert/delete. |
| `server/google-sheets/pdf-sheets.js` | `server/google-sheets/pdf-sheets.js` | Apps Script read/write for `Pdfs` tab with local dev fallback. |
| `server/google-sheets/config-reader.js` | `server/google-sheets/config-reader.js` | Server-side config reader (never returns TELEGRAM_SESSION). |
| `server/server.js` | `server/server.js` | Updated to mount the PDF routes alongside payments + static serving. |
| `apps-script/Code.gs.append` | Append to bottom of `apps-script/Code.gs` | Adds `Pdfs` + `Config` tabs and `pdf-list`, `pdf_upsert`, `pdf_delete`, `config-get` actions. |
| `scripts/telegram-login.js` | `scripts/telegram-login.js` | One-time CLI to authorize a Telegram session. |
| `courses/pdfs/index.html` | `courses/pdfs/index.html` | Public PDF library page. |
| `admin-pdfs.html` | `admin-pdfs.html` | Admin PDF publisher UI. |
| `tools/test-pdf-gateway.mjs` | `tools/test-pdf-gateway.mjs` | Offline unit tests for parser, resolver, stream, metadata projection. |
| `package.json.patch` | Apply to `package.json` | Adds `teleproto` dep, `telegram:login` and `test:pdf` scripts. |
| `.gitignore.patch` | Apply to `.gitignore` | Ignores `.telegram-session`, `data/pdfs.json`, mock fixtures. |
| `docs/*.md` | `docs/` | Architecture, admin, auth-setup, security, deployment docs. |

## What was NOT copied

- Any code from the inaccessible EkguruTelegram repository was
  re-implemented against the spec rather than copied.
- No secondary framework was introduced (the existing Node http
  server is extended).
- No separate Node service is required. There is no `/EkguruTelegram/`
  subdirectory at runtime.
- No arbitrary `/proxy?url=` endpoint exists.
- No permanent file storage (S3/R2/disk) is required.

## Dependencies added

```
npm install teleproto
```

(`telegram` package was intentionally not installed; teleproto is the
actively maintained successor.)

## Environment variables

See `docs/deployment.md`. Required at runtime:

- `TELEGRAM_API_ID`, `TELEGRAM_API_HASH` (env or Config tab)
- `TELEGRAM_SESSION` (env only — secret)
- `SHEETS_INGEST_TOKEN` (shared with existing Apps Script)
- `GOOGLE_SHEETS_ENDPOINT`

## Migration order

1. `npm install teleproto`.
2. Copy `server/telegram/*`, `server/pdf/*`, `server/google-sheets/*` into place.
3. Replace `server/server.js` with the updated version (it keeps all existing payment/static routes).
4. Append the contents of `apps-script/Code.gs.append` to the live Apps Script `Code.gs`.
5. Copy `scripts/telegram-login.js` and make executable.
6. Copy `courses/pdfs/index.html` and `admin-pdfs.html`.
7. Update `package.json` scripts and `.gitignore` per the patches.
8. Run `node scripts/telegram-login.js` locally to create a session, deploy `TELEGRAM_SESSION` to production.
9. Run `node tools/test-pdf-gateway.mjs` — should print `17 passed, 0 failed`.
10. Start server (`npm start`) and verify `GET /api/pdf/health` reports `mockMode: false, connected: true`.

## Test commands

```bash
node tools/test-pdf-gateway.mjs      # offline PDF module tests
npm run test:pdf                     # same
npm start                            # start server locally
curl http://localhost:3000/api/pdf/health
```

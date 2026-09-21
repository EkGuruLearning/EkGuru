# Telegram Authentication Setup

The EkGuru PDF gateway needs an authorized Telegram user session to
read messages from public channels and supergroups. This document
walks through creating that session once and rotating it.

## 1. Get an API ID / API hash

1. Go to https://my.telegram.org/ and log in with the Telegram account
   that will act as the EkGuru bot account (a regular user account;
   EkGuru does **not** use a bot token — bots cannot access all public
   message types).
2. Under **API development tools**, create an application. You'll get
   an `api_id` (integer) and `api_hash` (hex string).

These two values are non-secret identifiers for the Telegram API.
You can store them either:

- in the server environment as `TELEGRAM_API_ID` / `TELEGRAM_API_HASH`, or
- in the private `Config` tab of the EkGuru Google Sheet (rows
  `TELEGRAM_API_ID` and `TELEGRAM_API_HASH`). The Node server reads
  them server-side via Apps Script using `SHEETS_INGEST_TOKEN`.

## 2. Create a session (one-time)

From the repository:

```bash
export TELEGRAM_API_ID=123456
export TELEGRAM_API_HASH=abcdef0123456789...
node scripts/telegram-login.js
```

The script will ask locally (stdin) for:

1. Phone number (with country code, e.g. `+91...`).
2. OTP (the code Telegram sends to the account).
3. 2FA password — only if the account has two-step verification enabled.

It prints a `StringSession` and writes it to `.telegram-session`
(chmod 600, gitignored). That session is the **secret** credential.

## 3. Deploy the secret

Store the session string as `TELEGRAM_SESSION` in your server/deploy
secret store:

- local preview: `export TELEGRAM_SESSION=...` (or `.env` loaded by your runner).
- production: your platform's secret manager (e.g. Railway/Render/Fly
  env vars, Docker secrets, etc.).

**Never** put the session in:

- Google Sheets (any tab — public or not)
- Git / committed files
- Client-side JS, HTML, JSON, Next.js `NEXT_PUBLIC_*` vars
- API responses or logs

## 4. Start the server

```bash
NODE_ENV=production npm start
```

Watch the log for:

```
[telegram:info] [telegram] Client connected and authorized.
[EkGuru Server] PDF gateway:   /pdf/<publicId> and /pdf/<publicId>/download
```

If you see `Real credentials missing; using MOCK mode`, the server
could not find `TELEGRAM_API_ID` / `TELEGRAM_API_HASH` /
`TELEGRAM_SESSION` and fell back to fixtures. In
`NODE_ENV=production` mock mode refuses to serve PDFs, which is
intentional.

## 5. Revoking / rotating

To rotate a session:

1. In Telegram (the account), go to **Settings → Devices** and terminate the old session.
2. Delete the old `TELEGRAM_SESSION` from your secret manager.
3. Re-run `node scripts/telegram-login.js` and update the secret.

Logs never include the session string.

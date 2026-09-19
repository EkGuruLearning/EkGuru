# EkGuru Apps Script Mail Relay — Setup & Current Status

Turns your own Gmail (`EkGuruLearning@gmail.com`) into the **first**
mail relay in the chain — free, no per-recipient activation links, and it
sends exactly the HTML layout *we* wrote, not a relay's template.

---

## Current state (11 Sep 2026, ~10 PM IST) — LIVE & VERIFIED

You created a **new** relay project and deployed it:

| Item | Value |
|---|---|
| Script ID | `1HL_EX3V4hDvGmS9WPsVq6E33rZSod9bJ0Ggaty--JXf5k5yGnJoJvmXM` |
| Deployment | Version 1, 11 Sep 2026 9:47 PM IST |
| Deployment ID | `AKfycbzdX02U8KQU0XZpqXp4ACuNDAShrOKcHPCrMW5R3UcWOtHuWqquyouppkNusnLIz5ri` |
| Web app URL | `https://script.google.com/macros/s/AKfycbzdX02U8KQU0XZpqXp4ACuNDAShrOKcHPCrMW5R3UcWOtHuWqquyouppkNusnLIz5ri/exec` |
| Timezone | GMT+05:30 (India Standard Time – Kolkata) |
| Runtime | Chrome V8 |
| Script Property `MAILER_SHARED_TOKEN` | **set** (doGet reports `configured:true`) |
| Client token | **wired** into `js/site-config.js` via `tools/wire-token.py` |

### Live verification results (from the build sandbox)

| Check | Result |
|---|---|
| `GET /exec` health | `{"success":"true","status":"ok","script":"EkGuru Mail Relay","strangers":true,"limit":90,"configured":true}` |
| Wrong token | `{"success":"false","message":"Not authorised."}` — fail-closed ✓ |
| Unknown message type | `{"success":"false","message":"Unknown message type."}` — whitelist ✓ |
| Invalid recipient | `{"success":"false","message":"Missing or invalid recipient."}` ✓ |
| Controlled send (owner inbox) | `{"success":"true","message":"sent","state":"ACCEPTED"}` — real send from owner Gmail ✓ |
| Shipped mailer path (`testSend`) | ACCEPTED via Apps Script (`tools/test-email-live.js`) ✓ |
| Server-side idempotency | first POST → `sent`; replay of the same key → `duplicate` (no re-send) |

> Note: the sandbox is a datacenter IP. `GET` works without a browser
> User-Agent; `POST` works but Google throttles **rapid successive POSTs**
> from datacenter IPs. A real visitor's browser on a residential IP does
> not hit this. To re-run the live checks: `node tools/test-email-live.js`.

### Still required before the final PASS

1. **Confirm the `[TEST]` emails actually arrived** in
   `EkGuruLearning@gmail.com` — ACCEPTED proves Gmail dispatched them,
   only the inbox proves receipt.
2. **Deploy the release build** (the wired `js/site-config.js` + all
   email files) — GitHub push is credential-blocked from this sandbox.
3. **Two-student / two-tutor cross-routing test** in a real browser.

---

## The token — how it is wired (never committed)

The relay checks a shared token stored **server-side** as the Script
Property `MAILER_SHARED_TOKEN`. To (re)wire the client after any update:

1. Ensure the value is in `deploy-secrets.local.json` (gitignored):

   ```
   echo '{"mailerToken": "PASTE_THE_VALUE"}' > deploy-secrets.local.json
   ```

2. Inject it into the client, idempotently:

   ```
   python3 tools/wire-token.py          # inject
   python3 tools/wire-token.py --check  # confirm wired
   ```

3. `tools/release-decision.js` reports `STUDENT_EMAIL: ACCEPTED_UNVERIFIED`
   once wired (it was `BLOCKED_ON_TOKEN` before), so a forgotten token
   can never pass silently.

The token is a **shared secret, not a hard secret**: a static page must
send something with each POST, so the value sits in page source at deploy
time. It stops a drive-by who found only the bare URL; it is not
encryption. The daily cap is the real backstop.

---

## If you are (re)building the script from scratch

`tools/apps-script-mailer.gs` is a complete, drop-in `Code.gs`.

1. <https://script.google.com> → the project `1HL_EX3V4hDvGmS9WPsVq6E33rZSod9bJ0Ggaty--JXf5k5yGnJoJvmXM`.
2. Paste the whole of `tools/apps-script-mailer.gs` into `Code.gs`.
3. **Run `mintToken` once** from the editor → creates the Script
   Property `MAILER_SHARED_TOKEN` with a fresh secret (never printed,
   never committed).
4. **Deploy → New deployment → Web app** → Execute as **Me**, access **Anyone**.
5. Copy the Web app URL into `js/site-config.js` `mail.appsScript.url`,
   and wire the SAME token into `mail.appsScript.token` at deploy time
   only (do not commit the value).

> **Each code edit needs a NEW deployment version** — editing Code.gs
> alone does not change the live `/exec`.

### Fail-closed auth

`doPost` refuses mail (`"Not authorised."`) until the
`MAILER_SHARED_TOKEN` Script Property exists, and again on any mismatch.
There is no "token empty = open relay" fall-through. `doGet` health also
reports `"configured": true/false`. The client-side chain classifies
`"Not authorised."` as an AUTH error and walks to the next provider.

---

## Honest notes (do not skip)

- **This relay sends as the script owner** (EkGuruLearning@gmail.com).
  Reply-To is set separately so the visitor's address never appears in
  From.
- **ACCEPTED ≠ DELIVERED.** The script answers `"success":"true"` the
  moment Gmail accepts the message; only the recipient's mailbox can
  confirm delivery.
- **Daily cap.** The reference script enforces 90/day and then answers
  `"Daily limit exceeded"`, which the site reads as a quota signal and
  falls back on.
- **If the relay is ever down or un-tokened**, the site's chain walks
  past it — one dead relay can no longer lose a message.

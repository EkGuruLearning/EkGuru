# EkGuru Apps Script Mail Relay — Setup & Current Status

Turns your own Gmail (`EkGuruLearning@gmail.com`) into the **first**
mail relay in the chain — free, no per-recipient activation links, and it
sends exactly the HTML layout *we* wrote, not a relay's template.

---

## What we verified about YOUR deployment (11 Sep 2026)

You redeployed the relay twice on 11 Sep 2026 (from the Apps Script
"Manage deployments" page, `ee.md`):

| Version | Deployment ID (prefix) | Time |
|---|---|---|
| v3 (latest) | `AKfycbwm76fNYU54OqSSzt_HW_aA5lpg85kf-sEUPK90vaM9SaNQZ2f7D-ZN1V2P3hd7Ojzz` | 4:10 PM |
| v2 | `AKfycbwuZgVFp6YabDCQPkI_0VBYHKxKJMVj23nTADdX46X32RBES_tLNfmkobAb2L0kDtDH` | 4:08 PM |

Script ID: `1kcvADOf9OqQQ2uH3Yl4fC6aG7-fBR1asfaGpqLf9cqn_xErvkZ5TMHKm`
(library URL `…/macros/library/d/1kcvADOf9OqQQ2uH3Yl4fC6aG7-fBR1asfaGpqLf9cqn_xErvkZ5TMHKm/3`).

The client now points at the **v3** `/exec` URL. The relay is fail-closed:
with an empty token it answers `Not authorised`, and the site correctly
falls back to StaticForms/Web3Forms so no mail is lost. From this build
sandbox the `/exec` URL answers empty (Google bot-gates datacenter IPs),
so only a real visitor's browser can exercise it end-to-end.

### The one remaining step — the token

The script checks a shared token stored **server-side** as a Script
Property. To switch the relay on:

1. **Generate the token on the Apps Script side** (never in chat, never
   in the repo): in the Apps Script editor, select the `mintToken`
   function and click **Run**. It writes a fresh 32-character secret
   into the Script Property `MAILER_SHARED_TOKEN` and does **not**
   print the value.
2. **Deploy the Web App** (Deploy → New deployment → Web app → Execute
   as Me, access Anyone) so the latest code — including `mintToken` —
   is live.
3. **Wire the client ONCE, durably** (so no update ever erases it):

   ```
   echo '{"mailerToken": "PASTE_THE_VALUE"}' > deploy-secrets.local.json
   python3 tools/wire-token.py
   ```

   `deploy-secrets.local.json` is gitignored, so the token is never
   committed. `tools/wire-token.py` re-injects it into
   `js/site-config.js` after every update — run it after each
   `git pull` / before each deploy instead of re-pasting by hand.
   `tools/release-decision.js` reports `STUDENT_EMAIL:
   BLOCKED_ON_TOKEN` until it is wired, so a forgotten token can
   never pass silently.

   ```js
   mail: { …
     appsScript: {
       url: "https://script.google.com/macros/s/AKfycbwm76fNYU54OqSSzt_HW_aA5lpg85kf-sEUPK90vaM9SaNQZ2f7D-ZN1V2P3hd7Ojzz/exec",
       scriptId: "1kcvADOf9OqQQ2uH3Yl4fC6aG7-fBR1asfaGpqLf9cqn_xErvkZ5TMHKm",
       token: ""   /* ← filled by tools/wire-token.py; never commit the value */
     }
   }
   ```

4. Re-test: `python3 tools/test-email-e2e.py` → the booking/contact
   internal copy should then go out **via Google Apps Script**, and
   the Delivery tab in `admin.html` shows "Server token minted: yes /
   Client token wired: yes".

---

## If you are (re)building the script from scratch

`tools/apps-script-mailer.gs` is a complete, drop-in `Code.gs` that
implements this exact contract plus a daily cap and a token check.

1. <https://script.google.com> → open project `1kcvADOf9OqQQ2uH3Yl4fC6aG7-fBR1asfaGpqLf9cqn_xErvkZ5TMHKm`.
2. Paste the whole of `tools/apps-script-mailer.gs` into `Code.gs`.
3. **Run `mintToken` once** from the editor → it creates the Script
   Property `MAILER_SHARED_TOKEN` with a fresh secret (never printed,
   never committed).
4. **Deploy → New deployment → Web app** → Execute as **Me**, access **Anyone**.
5. Copy the Web app URL into `js/site-config.js` `mail.appsScript.url`,
   and wire the SAME token into `mail.appsScript.token` at deploy time
   only (do not commit it).

> **Each code edit needs a NEW deployment version** — editing Code.gs
> alone does not change the live `/exec`.

### Fail-closed auth (post-push hardening)

The reference `Code.gs` now **fails closed**: `doPost` refuses mail
(`"Not authorised."`) until a `MAILER_SHARED_TOKEN` Script Property
exists, and again on any mismatch. The relay therefore cannot run
unauthenticated — there is no "token empty = open relay" fall-through.
`doGet` health now also reports `"configured": true/false` so the relay
state is visible without exposing anything. The client-side chain in
`js/mailer.js` already classifies `"Not authorised."` as an AUTH error
and walks to the next provider, so no mail is lost while the token is
unset.

---

## Honest notes (do not skip)

- **The token is a shared secret, not a hard secret.** It is stored
  server-side as the `MAILER_SHARED_TOKEN` Script Property (never in the
  repo), but a static page has to send *something* with each POST, so
  the value ends up in page source at deploy time. It stops a drive-by
  who found only the bare URL; it is *not* encryption and must never be
  described as one. The daily cap is the real backstop.
- **This relay sends as the script owner** (EkGuruLearning@gmail.com).
  Reply-To is set separately so the visitor's address never appears in
  From.
- **ACCEPTED ≠ DELIVERED.** The script answers `"success":"true"` the
  moment Gmail accepts the message; only the recipient's mailbox can
  confirm delivery.
- **Daily cap.** The live script reports `remaining:100`; the reference
  script enforces 90/day and then answers `"Daily limit exceeded"`,
  which the site reads as a quota signal and falls back on.
- **If the relay is ever down or un-tokened**, the site's chain walks
  past it (v98) — one dead relay can no longer lose a message.

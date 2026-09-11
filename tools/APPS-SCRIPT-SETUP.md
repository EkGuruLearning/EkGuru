# EkGuru Apps Script Mail Relay — Setup & Current Status

Turns your own Gmail (`EkGuruLearning@gmail.com`) into the **first**
mail relay in the chain — free, no per-recipient activation links, and it
sends exactly the HTML layout *we* wrote, not a relay's template.

---

## What we verified about YOUR deployment (11 Sep 2026)

Your script is already deployed and reachable. Live probe results:

| Request | Response |
|---|---|
| `GET /exec` (health) | `{"success":"true","message":"EkGuru mail relay is deployed and reachable.","remaining":100}` |
| `POST /exec` (text/plain, empty token) | `{"success":"false","message":"Not authorised."}` |

So the endpoint is **live** and speaks the exact contract the site
expects (`success:"true"` / `success:"false"` + `message`). The only
missing piece is **the shared token**: with an empty token the script
answers `Not authorised`, and the site correctly falls back to
StaticForms/Web3Forms so no mail is lost.

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
3. **Wire the client at deploy time**: put the SAME value into
   `js/site-config.js` locally during deployment (see below). Keep it
   out of any committed file — the repository copy of `site-config.js`
   ships with `token: ""`.

   ```js
   mail: { …
     appsScript: {
       url: "https://script.google.com/macros/s/AKfycbwG978gM3Vspo0r8JmNxRojiUwA5h0tWoFd8p9vQf5x-NX9QGDB8VCr0j1LnTPoOjqtdA/exec",
       scriptId: "1dG12tEKQXs7bRKsUetBmFeVi-kqrDqMKU9S_2ahZJNM8mCYjE5nrDaM1",
       token: ""   /* ← fill only at deploy time; never commit the value */
     }
   }
   ```

4. Re-test: `python3 tools/test-email-e2e.py` → the booking/contact
   internal copy should then go out **via Google Apps Script**.

> ⚠️ If the URL you typed had an extra letter (`…LnTPoOoJqtdA`), note the
> correct deployment is `…LnTPoOjqtdA` — one `o`. The extra-letter URL
> answers "file does not exist".

---

## If you are (re)building the script from scratch

`tools/apps-script-mailer.gs` is a complete, drop-in `Code.gs` that
implements this exact contract plus a daily cap and a token check.

1. <https://script.google.com> → open project `1dG12tEKQXs7bRKsUetBmFeVi-kqrDqMKU9S_2ahZJNM8mCYjE5nrDaM1`.
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

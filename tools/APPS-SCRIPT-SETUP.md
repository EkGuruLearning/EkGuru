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

The script checks a shared word. To switch the relay on:

1. Find the word the script checks (the `TOKEN` Script Property in the
   Apps Script project, or whatever field your script compares against).
2. Paste that same word into `js/site-config.js` →

   ```js
   mail: { …
     appsScript: {
       url: "https://script.google.com/macros/s/AKfycbwG978gM3Vspo0r8JmNxRojiUwA5h0tWoFd8p9vQf5x-NX9QGDB8VCr0j1LnTPoOjqtdA/exec",
       scriptId: "1dG12tEKQXs7bRKsUetBmFeVi-kqrDqMKU9S_2ahZJNM8mCYjE5nrDaM1",
       token: "…the word…"
     }
   }
   ```

3. Re-test: `python3 tools/test-email-e2e.py` → the booking/contact
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
3. **Project Settings → Script Properties** → add `TOKEN` = a word you invent.
4. **Deploy → New deployment → Web app** → Execute as **Me**, access **Anyone**.
5. Copy the Web app URL and paste it into `js/site-config.js`
   `mail.appsScript.url`, and the word into `mail.appsScript.token`.

> **Each code edit needs a NEW deployment version** — editing Code.gs
> alone does not change the live `/exec`.

---

## Honest notes (do not skip)

- **The URL and token are public** — they live in a static page. The
  token stops a drive-by who found only the bare URL; it is *not*
  encryption and must never be described as one.
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

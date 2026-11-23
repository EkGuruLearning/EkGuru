# EkGuru application backend (six-step wizard) — setup & deployment

This is the backend for the redesigned **join.html** tutor application. It
replaces the 13-field intake contract with a 68-column schema that stores
**every** field the wizard collects, and adds four applicant emails and an
owner-only status API.

> **Nothing here is deployed.** Committing a `.gs` file does not deploy it.
> Steps 1–7 below are the manual part; they are deliberately written so that
> a wrong step fails *visibly* (`?action=ekHealth` says `ok:false`) instead of
> silently losing applications.

---

## 1. What is in the repository

| File | What it is | Where it goes |
|---|---|---|
| `apps-script/ApplicationSchema.gs` | **Single source of truth**: 69 columns, limits, statuses, allowed status moves, which transition sends which email | New file in the intake Apps Script project |
| `apps-script/ApplicationIntake.gs` | The backend: validation, migration, row building, dedupe, email, admin API, status lookup | New file in the same project |
| `apps-script/Unified.gs` | The existing router. Two small seams added (`ekApplicationAction_`, `ekApplicationGet_`); feed + intake behaviour unchanged | Overwrite the existing file |
| `apps-script/Intake.gs` | Same two seams, for projects that still run the standalone intake. The honeypot is checked **before** the seam, exactly as in `Unified.gs` (fixed in 1.3.1 — before that, a filled honeypot still stored an application) | Only if you use this file instead of Unified.gs |
| `js/join-schema.js` | **Generated** browser copy of the schema (`tools/build-join-schema.mjs`) | Deploys with the site |
| `js/join-wizard.js` | Builds the payload from the schema | Deploys with the site |
| `tools/build-join-schema.mjs` | Regenerates `js/join-schema.js` | — |
| `tools/test-application-backend.mjs` | 120 backend checks with mocked Google services | — |
| `tools/test-join-wizard.mjs` | 117 wizard checks, including a real end-to-end POST | — |

`npm test` runs both.

---

## 2. Which Apps Script project

**The EkGuru DB project** — the one bound to the tutors/reviews/settings
workbook (the project that currently runs `Unified.gs`).

- ⚠️ **Not** the payments project (`Code.gs`, the one that talks about
  Razorpay). One project cannot hold two `doGet`/`doPost` pairs.
- ⚠️ **Not** a new project created at script.google.com, unless you also set
  the spreadsheet property in step 4.

The workbook is found at runtime by `intakeSpreadsheet_()` — bound sheet
first, then the `EKGURU_DB_SPREADSHEET_ID` script property. **No spreadsheet
id is hard-coded in any of these files**, and none must ever be added.

---

## 3. Paste the files

1. Open the **EkGuru DB** sheet → **Extensions → Apps Script**.
2. **File → New → Script**, name it `ApplicationSchema`. Paste the whole of
   `apps-script/ApplicationSchema.gs`. Save.
3. **File → New → Script**, name it `ApplicationIntake`. Paste the whole of
   `apps-script/ApplicationIntake.gs`. Save.
4. Overwrite `Code.gs` (or whatever holds `Unified.gs`) with the new
   `apps-script/Unified.gs`. Save.
5. The editor must show **no red error**. If it does, a file was pasted
   half-way — select all, delete, paste again.

Keep `ApplicationSchema.gs` a **separate file** from
`ApplicationIntake.gs`. Apps Script shares one global scope across files, so
either way compiles — but separate files mean the schema can be re-pasted
without touching the logic, and the "which file is stale" question has one
honest answer.

---

## 4. Script Properties

**Project Settings → Script Properties.**

| Property | Required | Default | What it does |
|---|---|---|---|
| `EKGURU_DB_SPREADSHEET_ID` | only if the project is not bound to the sheet | — | The workbook id |
| `EK_ADMIN_TOKEN` | **yes, for admin actions** | — (admin actions are OFF) | Long random string. The only credential for `ekAdminUpdate`. Never in frontend code |
| `EK_ADMIN_NAME` | no | `owner` | Written into `reviewed_by` (e.g. `Prakash`) |
| `APPLICATION_MAIL_ENABLED` | no | `true` | Set `false` to stop all applicant email while keeping the backend live and recording `email_status` |
| `APPLICATION_OWNER_INBOX` | no | `EkGuruLearning@gmail.com` | Reply-to on every applicant email |
| `APPLICATION_SENDER_NAME` | no | `EkGuru` | Display name of the sender |
| `APPLICATION_SITE_URL` | no | `https://ekguru.shop/` | Used in the email footer |

Generate the token with something like `openssl rand -hex 24`. Keep it out of
the repository, out of the sheet, and out of any page.

---

## 5. Migrate the `applications` tab (once)

In the Apps Script editor pick **`ekMigrateApplications`** and press **Run**.
Authorise when asked. The log prints:

```
applications: 24 data rows kept, 51 columns added, 68/68 schema columns present
```

What that run did, and did not, do:

- **Added** the 51 new columns to the right of the existing 17.
- **Did not** move, rename or clear any existing column, cell or row.
- **Did not** touch `tutors`, `reviews_pending`, `settings`, `bookings`,
  `contacts`, `signups`, `dashboard` or `applications-form-archive`.
- Old applications keep their references and keep their statuses; their new
  columns are simply blank.

Running it twice adds nothing (it is idempotent, and `npm test` asserts that).

There is also an **EkGuru** menu inside the sheet (added by `onOpen`) with the
same action, plus "Application schema health".

---

## 6. Deploy

1. **Deploy → Manage deployments → ✏️ Edit** the **existing** deployment.
   - **Execute as:** Me
   - **Who has access:** Anyone
2. **Version: New version → Deploy.**
   ⚠️ Never "New deployment" — that mints a different URL and `feed.url` and
   `intake.url` in `js/site-config.js` both go stale, which silently turns
   every application back into the mailto fallback.
3. The URL does not change. `js/site-config.js` needs **no edit**.

---

## 7. Verify

Open in a browser (your URL in place of the dots):

| Address | Must show |
|---|---|
| `.../exec?action=ekHealth` | `"ok": true`, `"schema": "2.1.0"`, `"columns": {"expected": 69, "present": 69, "missing": []}` |
| `.../exec?action=health` | `"version": "1.3.0"`, and an `application` block with `"schema": "2.1.0"` |
| `.../exec` | `"unified": "2.2.0"`, `feed` and `intake` blocks, `intake.application.schema` |
| `.../exec?tab=tutors` | unchanged tutor CSV, still with **no** `email` / `notification_email` columns |

If `ekHealth` says `ok:false` with a list of missing columns, step 5 was
skipped — run it, then reload.

---

## 8. A controlled end-to-end check (no real applicant is emailed)

Do this **before** telling tutors the form is live, and use an address you
control:

1. Open `join.html`, fill every step, submit.
2. The page must show a reference like `EG-7K3Q9M`.
3. In the sheet, the newest `applications` row must have that reference and
   every field you typed — spot-check `headline`, `subjects_json`,
   `availability_json`, `timezone`, `rate_usd`, `details_json` (should be
   empty or `{}`).
4. Your inbox gets "Your EkGuru tutor application is with us (EG-…)".
5. Submit the **same** form again without changing anything: no second row.
6. Delete the test row when done. (Nothing is published by any of this —
   see "Publication" below.)

---

## 9. Review workflow (how approval/rejection actually happens)

Statuses, and the only moves the server allows:

```
pending ──► under_review ──► approved ──► rejected
   │              │
   ├──────────────┴──► needs_information ──► under_review / approved / rejected
   └──► rejected ──► under_review          (a rejection can be reopened)
```

Every move records: `status`, `previous_status`, `reviewed_by`, `reviewed_at`,
`review_notes` (why), and for a rejection `rejection_reason` (required).

**Approving or rejecting sends exactly one email, and only from this action:**

| Move | Email | Needs |
|---|---|---|
| submitted | "Your EkGuru tutor application is with us" | — |
| `approved` | "Your EkGuru tutor application is approved" | — |
| `rejected` | "About your EkGuru tutor application" **carrying the real reason** | `reason` is **required**, or the move is refused |
| `needs_information` | "We need a little more information" (lists what is missing) | `note` is **required** |

A refusal without a reason is refused by the server rather than emailed
empty. A repeat of the same transition is a no-op (the row's `email_status`
already says `<transition>:sent`), so nobody gets two approval emails.

### Changing a status

From the Apps Script editor, run:

```js
ekSetStatus_("EG-7K3Q9M", "approved", { admin: "Prakash", note: "checked on the phone" });
ekSetStatus_("EG-7K3Q9M", "rejected", { admin: "Prakash",
  reason: "The photo link was broken and no teaching experience was given." });
```

Or over HTTPS with the token (this is what an admin page would call):

```bash
curl -s -X POST '<EXEC_URL>' -H 'Content-Type: text/plain' --data '{
  "action":"ekAdminUpdate",
  "token":"<EK_ADMIN_TOKEN>",
  "reference":"EG-7K3Q9M",
  "status":"approved",
  "note":"checked on the phone"
}'
```

> **Known gap (documented, not faked):** `admin.html` has **no** application
> review screen. Until one is built, review happens in the sheet plus these
> calls. Building the screen is a separate piece of work — the API it needs
> (`ekAdminUpdate`, `ekStatus`) exists and is tested.

---

## 10. Publication rules (why nothing goes live by itself)

- This backend **never writes to the `tutors` tab.** `npm test` asserts it:
  neither approving nor rejecting changes a single tutors cell.
- `js/sheet.js` publishes a tutor row only when that row says
  `approved = yes` (or its id is in the reviewed registry). Approving an
  *application* is not the same thing as publishing a *tutor* — that copy
  step is still a human decision.
- If an approved tutor's profile is edited, the live row keeps its last
  `approved=yes` version until a human re-approves. There is no endpoint here
  that rewrites a published tutor row.

---

## 11. API reference

All POSTs are `Content-Type: text/plain` with a JSON body (Apps Script cannot
answer a CORS preflight). All answers are JSON.

### Submit (the wizard)

```json
POST {}
{
  "kind": "application",
  "consent": true,
  "consent_privacy": true,
  "website": "",
  "submission_id": "b7d1c0e2-…",
  "fields": {
    "name": "Kiran Rao", "display_name": "Kiran",
    "email": "kiran@example.com", "city": "Pune", "country": "India",
    "state": "Maharashtra", "contact_pref": "WhatsApp",
    "intro": "Warm, patient teacher…",
    "subjects": ["Conversational Hindi", "Hindi for Children"],
    "levels": ["Children", "Absolute beginners"],
    "methods": ["Conversation-based"], "teach_langs": ["Hindi"],
    "hindi_level": "Native", "english_level": "Advanced (C1)",
    "years": "6-10 years", "edu_qual": "Master's degree",
    "headline": "Patient Hindi tutor…", "bio": "…", "rate_usd": 12,
    "currency": "USD", "duration": "50 min", "trial": "Free short trial",
    "timezone": "Asia/Kolkata",
    "availability_slots": [{"day":"Mon","from":"19:00","to":"21:00"}],
    "photo_link": "https://…", "video_link": "https://youtu.be/…"
  }
}
```

```json
200 {}
{ "ok": true, "reference": "EG-7K3Q9M", "duplicate": false, "mail": "sent" }
```

Failure answers name the field, so the page can point at the box:

```json
{ "ok": false, "error": "email does not look like an email address",
  "fields": { "email": "does not look like an email address" } }
```

`duplicate: true` means nothing new was written: either the same
`submission_id` was retried, or the same email was resubmitted within 72 hours
(in which case the row was updated in place — the reference is unchanged and
the owner's review decisions are preserved).

**Identity is decided on the server.** `submission_id` is an *attempt* token, not
an identity: it may say "this is the same attempt as before" and it may never say
"this is the same person as someone else". The retry lookup is scoped to the
applicant's own row, which is resolved from the submitted email, so a value
planted or guessed by one applicant can never decide what another applicant's
submission is matched against. `submission_id` is reserved: a value supplied
inside `fields` is never used as the key, and is kept inertly as
`sent_submission_id`.

Retry detection only works for submissions stored since 2.0.2: rows written
before that have no retry key, so a retry of one of them is caught by the email
window instead.

`mail` is `sent` / `failed` / `skipped` / `off`. A mail failure **never** fails
the submission; the row is already saved and `email_status` records what
happened.

### Applicant status

```json
POST { "action": "ekStatus", "reference": "EG-7K3Q9M", "email": "kiran@example.com" }
→ { "ok": true, "reference": "EG-7K3Q9M", "status": "pending",
    "updated_at": "…", "next": "a person is reading it" }
```

Reference **and** the email that applied are both required. A wrong pair gets
the same answer as a non-existent reference, so the endpoint cannot be used to
test whether a reference exists. The answer never contains the row.

### Health

```
GET ?action=ekHealth
→ { "ok": true, "version": "2.1.0", "schema": "2.1.0", "mail": "on",
    "admin": "configured", "rows": 24,
    "columns": { "expected": 69, "present": 69, "missing": [] } }
```

`ok:false` here means the tab is not fully migrated. It is a read: it never
writes a header **and never creates the tab** — a monitoring URL cannot add an
empty sheet to the workbook.

---

## 12. Security

| Concern | How it is handled |
|---|---|
| Server-side validation | Every field validated against the schema on the server. The browser's copy is a courtesy, not the authority |
| Admin actions | `EK_ADMIN_TOKEN` script property; no property = admin actions refuse everything. The token never reaches a page |
| Applicant lookup | reference + email, one generic failure message |
| Workbook protection | No spreadsheet id in any file or page; the id lives in the bound project / script property |
| PII in responses | Health returns counts only; status returns status only; no field is ever echoed back except the reference |
| Formula injection | Any cell starting `= + - @` is prefixed with `'`; `<` and `>` are stripped |
| HTML email | Every interpolated value passes `ekEscape_` |
| Double submits | `submission_id` retry detection + one row per email per 72h + `LockService` around the whole write |
| Concurrent writes | `tryLock(25000)`; a submission that cannot get the lock is refused, not half-written |
| Abuse / rate limiting | The existing intake quota (`INTAKE_HOURLY_CAP` / `DAILY_CAP` per kind) still applies to `application` |
| Duplicate email | `email_status` records `received:sent`, `approved:sent`, …; the same transition is never re-sent |
| Uploads | This form collects **links only**. No file is uploaded anywhere, so there is no upload path to validate |
| Mail quota | A `GmailApp` failure is recorded on the row and returned as `mail:"failed"`; the application stays saved |
| Idempotency | Retry key scoped to the applicant's own row (resolved from the email on the server); a client-supplied `submission_id` is a hint only and cannot name another row. Notifications keyed by `<transition>:sent` |

**Honest limitations** (Apps Script cannot do these, so they are documented
rather than pretended):

- **No reliable client IP.** The abuse protection is a global per-kind cap,
  not per-visitor. A determined spammer can fill the queue up to the cap.
- **No CORS preflight.** The preflight is avoided with `text/plain`, which
  means a browser could in principle post from another site. The honeypot,
  the consent flag and the server validation are what stop junk, not the
  origin.
- **No true admin session.** Authorisation is a shared bearer token. Put it in
  a password manager, and rotate it if it ever appears anywhere unexpected.
- **No verified email address.** Nothing proves the applicant owns the address
  they typed. There is no OTP anywhere in this project — that is a real gap,
  not an oversight, and the email says "we will reply to this address" rather
  than "your address is verified".

---

## 13. Field map (wizard → column)

The authoritative list is `apps-script/ApplicationSchema.gs`; this table is
for reading. `src` is the key the wizard posts, `col` the sheet header.

| Group | Wizard keys → columns |
|---|---|
| Personal | `name`→name, `display_name`→display_name, `email`→email, `city`→city, `country`→country, `state`→state, `photo_link`→photo_link, `contact_pref`→contact_pref, `intro`→intro, **`whatsapp`→whatsapp** |
| Teaching | `subjects`→subjects_json, `levels`→levels_json, `methods`→methods_json, `teach_langs`→teach_langs_json, `hindi_level`→hindi_level, `english_level`→english_level, `other_langs`→other_langs, `years`→years, `online_years`→online_years, `less_exp`→less_exp, `platforms`→platforms |
| Education | `edu_qual`→edu_qual, `edu_inst`→edu_inst, `edu_year`→edu_year, `edu_extra`→edu_extra, `certs`→certs, `bed_detail`→bed_detail, `doc_refs`→doc_refs |
| Profile | `headline`→headline, `bio`→bio, `why`→why, `video_link`→video_link, `video_thumb`→video_thumb, `sample_link`→sample_link, `website2`→website, `linkedin`→linkedin, `profile_url`→profile_url |
| Pricing | `rate_usd`→rate_usd, `currency`→currency, `duration`→duration, `trial`→trial |
| Availability | `timezone`→timezone, `availability_slots`→availability_json, `availability_meta`→availability_meta (derived when the client omits it), (derived) `availability` |
| Consent | (server) → consent_privacy, consent_terms, declaration, consent_at |
| System | (server) → reference, status, approved, timestamp, created_at, updated_at, schema_version, email_status, email_sent_at |
| Derived | `subjects`→subject, `teach_langs`+levels→languages, `years`+levels→experience |
| Anything else | → `details_json` (documented overflow, never dropped) |
| A **reserved** name (anything in `EKGURU_SERVER_ONLY`) | → `details_json` as `sent_<name>`, inert |

A reserved name is one the server owns: `status`, `approved`, `reference`,
`review_notes`, `reviewed_by`, `consent_terms`, `schema_version` and the rest
of `EKGURU_SERVER_ONLY`. A client that sends one cannot move its column (that
was always true) and now cannot make it *look* moved either: the value is filed
under `sent_status`, `sent_review_notes`, … so an owner reading the cell cannot
mistake applicant text for a reviewer's note. Nothing is discarded; the
`details_json` key limit still applies.

The three **derived** columns matter: `subject`, `languages` and `experience`
existed before this change and are printed on the public profile. The wizard
collects those facts as chips and selects, so the server rebuilds the three
strings from them. That means an old client (13-field payload), a hand-made
`curl`, or a page whose schema file failed to load still produces a complete
row.

---

## 13a. The WhatsApp number (schema 2.1.0)

One new column, `whatsapp`, appended at the **end** — after `details_json`,
never in the middle, so no existing cell moves. Its physical position depends
on what the tab looked like when `ekMigrateApplications` ran: **69** on a tab
already at 2.0.0's 68 columns (the production case), **22** on a tab still at
the legacy 17 (52 columns are appended in schema order). The schema index is
22 either way. Writes are header-driven (`ekHeaderRead_` + `map[column]`), so
neither number is relied on anywhere in the code.

**It is private.** `whatsapp` is already in `FEED_PRIVATE_EXACT` in
`Unified.gs`, so even if the column were ever copied into a published feed it
is stripped by name. It is not printed on any public page, and it is not sent
to `tutors` when an application is approved (approval never writes that tab).

**It is optional.** Blank is valid and stores `""`; it never blocks Continue or
Submit, and the wizard leaves the key out of the payload entirely rather than
sending an empty string.

**Nothing is guessed.** A leading `+` is kept; without one, the digits are kept
exactly as typed. An Indian `98765 43210` stays `9876543210` and is *not*
turned into `+919876543210`, because a wrong country code is worse than an
incomplete one. Seven to fifteen digits are accepted, which covers India and
international numbers.

**No WhatsApp messages are ever sent.** The backend sends email only
(`ekSendApplicationMail_`). `contact_pref: "WhatsApp"` is a *stated
preference* for what to try next, not consent to be messaged: nothing in the
codebase reads the number and messages it.

| What a tutor types | Stored |
|---|---|
| `+91 98765 43210` | `+919876543210` |
| `98765 43210` | `9876543210` |
| `+44 7700 900123` | `+447700900123` |
| `(91) 98765-43210` | `919876543210` |
| `12` | refused — "should be 7 to 15 digits…" |
| *(blank)* | `""` |

---

## 14. Updating later

Any change to a limit, a column or an option list starts in
`ApplicationSchema.gs`:

```bash
# 1. edit apps-script/ApplicationSchema.gs
# 2. regenerate the browser copy
node tools/build-join-schema.mjs
# 3. prove both sides still agree
npm test
# 4. bump EKGURU_SCHEMA_VERSION, re-paste the file, run ekMigrateApplications,
#    then Manage deployments → Edit → New version
```

`npm test` fails if `js/join-schema.js` is stale, if a wizard field has no
column, if a column has no field, or if a limit in the page is looser than the
one the server enforces.

---

## 15. Troubleshooting

| What you see | What it means | Fix |
|---|---|---|
| `?action=ekHealth` → `ok:false`, `missing:[…]` | Tab not migrated | Run `ekMigrateApplications` |
| `?action=health` → `application:{version:"absent"}` | `ApplicationIntake.gs` not in this project | Paste it (step 3) |
| Wizard shows the email fallback | `intake.url` in `js/site-config.js` is stale, or the deployment is not "Anyone" | Check the URL, redeploy a new version |
| Application saved, no email | Gmail quota, or `APPLICATION_MAIL_ENABLED=false` | Look at `email_status` on the row; it says `failed (…)` or `off` |
| Two identical rows | The dedupe window (72h) was exceeded, or the email was typed differently | Check `email` on both rows |
| `ekAdminUpdate` → `not authorised` | Missing/incorrect `EK_ADMIN_TOKEN`, or the property is not set | Set it, then redeploy a new version |
| `ekAdminUpdate` → `switched off` | No token property at all | Same |
| Rejection refused | No `reason` given | Give one; it becomes the email |
| `availability_json` shows `[object Object]` | A client sent a live array where a string was expected — fixed in 2.0.0 | Re-paste `ApplicationIntake.gs` |
| applications tab still shows 68 columns | The 2.1.0 `whatsapp` column has not been appended yet | Run **EkGuru → Migrate applications tab**, then reload `?action=ekHealth` |

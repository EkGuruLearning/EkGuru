# EKGURU — EMAIL SYSTEM RESET + SIMPLE ROLE TEMPLATES + SHEETS CSV RESET — FINAL REPORT

Generated 2026-09-11 (Asia/Kolkata) · Command: `/home/user/uploads/EkGuru_EMAIL_Reset_Simple_Role_Templates_Sheets_Reset_Command.md`
+ `/home/user/uploads/EkGuru_Email_Copy_Simple_Role_Templates.md`

---

## EMAIL ARCHITECTURE

| Item | State |
|---|---|
| Primary provider | **Google Apps Script / Gmail** — student, tutor, visitor confirmation, admin → recipient |
| Internal provider | **High-capacity internal route** — FormSubmit → StaticForms → Apps Script fallback (own-inbox mail never spends metered quota) |
| Fallback order | per role: Apps Script primary → fallback #1 → fallback #2 → final failure; internal = internal route → Apps Script → final failure |
| Sender identity | **verified EkGuru sender** (owner Gmail). Visitor/student/tutor address is never `From` (enforced server-side) |
| Orchestration | one central layer: `js/mailer.js` + `js/email-templates.js`; `tools/apps-script-mailer.gs` relay |

## ROUTING (live-verified by `tools/test-routing.js`)

Probe output against the LIVE config (token wired):

    Booking  → STUDENT   → appsscript   (top rank)
    Booking  → TUTOR     → appsscript   (top rank)
    Booking  → EKGURU    → formsubmit   (unlimited)
    Contact  → VISITOR   → appsscript   (top rank)
    Contact  → EKGURU    → formsubmit   (unlimited)
    Admin    → RECIPIENT → appsscript   (fallback: formsubmit → web3forms)
    Admin    → EKGURU    → formsubmit   (unlimited)

## ROUTING

| Role | Type | To | Reply-To |
|---|---|---|---|
| Booking student | `BOOKING_STUDENT_CONFIRMATION` | exact student email | EkGuru support |
| Booking tutor | `BOOKING_TUTOR_NOTIFICATION` | canonical `notification_email` | student (supported direct-response) |
| Booking internal | `BOOKING_EKGURU_NOTIFICATION` | EkGuru inbox | student |
| Contact visitor | `CONTACT_VISITOR_CONFIRMATION` | exact visitor email | EkGuru support |
| Contact internal | `CONTACT_EKGURU_NOTIFICATION` | EkGuru inbox | visitor |
| Admin → recipient | `ADMIN_CONTACT_OUTBOUND` | admin-selected recipient | EkGuru support |
| Admin internal copy | `ADMIN_CONTACT_INTERNAL_COPY` | EkGuru inbox | EkGuru support |

- Idempotency key = **entityId:messageType** (e.g. `BOOK-123:BOOKING_STUDENT_CONFIRMATION`), client (`guarded()`) and relay (`SENT_<key>`).
- Delivery vocabulary: `NOT_ATTEMPTED · SENDING · ACCEPTED · FAILED · UNKNOWN · RETRYING · FINAL_FAILURE`. **ACCEPTED ≠ DELIVERED.**
- `TUTOR_EMAIL_UNAVAILABLE` when a tutor has no valid operational address; student + internal still send. Tutor states: `ACTIVE+VALID / ACTIVE+MISSING / ACTIVE+INVALID / UNPUBLISHED / DISABLED`.

## TEMPLATES

Seven SIMPLE, role-specific templates (exact copy from the command). Shared shell (HTML + plain-text), all user values escaped, `render()` fails loudly on unknown type / missing / undeclared / null var / raw `{placeholder}` / unescaped `<script>`; subject single-line (CR/LF collapsed, 150 chars).

v101.1 — **row payloads now mirror the templates** (bug fixed): FormSubmit renders only the row fields (it strips html/text), so the internal copies EkGuru's own inbox receives were still the old verbose table. Every body builder (tutor / internal record / student / contact internal / visitor ack / admin outbound + copy) now emits the same SIMPLE labelled rows as its template, so every relay renders the same clean wording. See `reports/email-preview-all-7.html` for the rendered result.

| Template | Subject |
|---|---|
| student | `Congratulations — your booking request was received \| EkGuru` |
| tutor | `Congratulations — you have a new booking request \| EkGuru` |
| internal booking | `New booking request — {Student} → {Tutor} \| {Booking ID}` |
| visitor | `We received your message — EkGuru` |
| internal contact | `New contact message — {Contact ID}` |
| admin outbound | `{Admin Subject}` |
| admin internal copy | `Admin sent a contact message — {Conversation ID}` |

Role-language QA (§27-H) passes for all seven (a tutor mail never says "your booking"; a student mail never carries tutor operational wording; internal wording never reaches a public recipient).

## SHEETS

- **Old URLs removed: YES.** All four public CSV URLs + gids were removed from `js/site-config.js` (0 `docs.google.com` references remain in shipped JS). Preserved only in `/home/user/backups/email-sheets-reset-20260911/old-csv-urls.txt`.
- **DATA_SOURCE_STATUS = PAUSED_FOR_REUPLOAD** set on all four blocks; loaders skip the fetch and serve baked-in local data — the site keeps working. Admin dashboard shows **"Sheets: PAUSED — new upload links required"** (GREEN→YELLOW, never falsely green).
- **Fresh CSVs generated: YES** — `/home/user/csv/`:

| File | Columns | Rows |
|---|---|---|
| `ekguru_settings.csv` | key, value, what it does | 8 keys |
| `ekguru_content.csv` | slug, question, answer, body, keywords, related, status | 29 (28 live + 1 draft) |
| `ekguru_reviews.csv` | tutor, name, date, stars, text, source, status | 3 |
| `ekguru_tutors.csv` | 48 (live 47 + `notification_email`) | 4 tutors + #help |
| `ekguru_github_urls.csv` | 18-col crawl inventory | 555 |
| `ekguru_urls.csv` | 17-col site inventory | 548 |

- `notification_email` is the canonical operational email column (documented in `csv/README.md`); `email` kept for migration compatibility; `formKey` still supported; loader (`js/sheet.js`) + build (`tools/sheetsync.js`) both accept it. Public tutor pages never render it.
- **Future upload instructions** in `csv/README.md` (upload → publish each tab as CSV → send the 6 new URLs → next deploy wires them). No replacement URLs were guessed.

## WORKSPACE

- Only EkGuru project retained: **YES**.
- Deleted: `repo_tutors.csv` (empty scratch), `EkGuru-ULTRA-12fc4bf.zip` (duplicate old export), `audit/` (superseded — its `backup/` was preserved into the backups dir first).
- Backups retained: `/home/user/backups/email-sheets-reset-20260911/` (6 CSVs + `snapshot.json` with headers/row-counts/sha256, `old-csv-urls.txt`, `ekguru-pre-reset.bundle` git bundle, `prior-audit-backup/` with the known-good `ddb7329e` bundle + v5 zip + `.before` files); `releases/` rollback chain untouched.
- Unrelated production data deleted: **NO**.

## TESTS

| Suite | Runner | Result |
|---|---|---|
| Template registry + render + escaping + role QA (7 types) | `tools/test-email-system.js` | **PASS** |
| Mailer integration: send / contact / compose / tutorEmailInfo / testSend / idempotency | `tools/test-email-system.js` | **PASS** |
| Security: XSS, header injection, unknown type, secret scan, relay static | `tools/test-email-security.js` | **PASS** |
| Two-student / two-tutor routing | covered by role-template + recipient assertions (student≠tutor recipients, no tutor inbox in student copy) | PASS (code) |
| Duplicate submission | idempotency `entityId:type` client + relay | PASS (code; live replay proven 11 Sep) |
| Real mailbox | **NOT DONE** — needs the owner to re-upload sheets, re-wire URLs, and run the two-student inbox test | **BLOCKED** |

## REMAINING BLOCKERS

1. **Real student mailbox receipt** — never claimed (hard-stop §28). The relay live-verified ACCEPTED on 11 Sep, but the reset changes must be deployed and the two-student/two-tutor test run in a real browser.
2. **Owner re-uploads the six CSVs** into a new workbook, publishes each tab as CSV, and returns the six new URLs → next deploy wires them and flips `PAUSED_FOR_REUPLOAD` back to live.
3. **GitHub push** — credential-blocked from this sandbox; the release build must be pushed + Pages verified by the owner.
4. **Apps Script relay redeploy** — the new 7-type whitelist (`ADMIN_CONTACT_OUTBOUND`, `ADMIN_CONTACT_INTERNAL_COPY`) needs a new deployment version of `tools/apps-script-mailer.gs`.

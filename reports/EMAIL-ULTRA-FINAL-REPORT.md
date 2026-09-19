# EKGURU EMAIL ULTRA FINAL REPORT

Generated 2026-09-11 (Asia/Kolkata) · workstream: **Email ULTRA — Apps Script Primary + Sheets Routing**
Spec: `/home/user/uploads/EkGuru_ULTRA_Email_AppsScript_Primary_Sheets_Routing_Master_Command.md` (54 sections)

> Status of this report: **everything below is verified in code and by the automated
> suites in this workspace.** The one thing a final report must never do — claim a
> real student mailbox received the email — is **NOT done** and is stated as such
> under LIVE / REMAINING. Hard-stop §50 is **not passed yet**.

---

## PRIMARY PROVIDER

| Item | State |
|---|---|
| Primary transactional route | **Google Apps Script / Gmail** (`tools/apps-script-mailer.gs`, v100) |
| Orchestration | One central layer — `js/mailer.js` renders via `js/email-templates.js`; the relay only carries html/text/type |
| Relay URL | v3 `/exec` deployed (`AKfycbwm76fNYU54OqSSzt_HW_aA5lpg85kf-sEUPK90vaM9SaNQZ2f7D-ZN1V2P3hd7Ojzz`) |
| `From` | Always the **verified EkGuru sender** (script-owner Gmail `EkGuruLearning@gmail.com`), forced server-side; the visitor/student/tutor address is **never** in `From` |
| Client token | **wired** via `tools/wire-token.py` from the gitignored `deploy-secrets.local.json` → relay answers `sent`/`ACCEPTED` (live-verified 11 Sep 2026) |
| Per-form provider mixture | Removed — `mail.contactProvider` now defaults to `"appsscript"` for the contact form too (one orchestration layer) |

## ROUTING

Five message types, one row each (source of truth: `js/email-templates.js` `ROUTES`):

| Message type | From | To | Reply-To | Template |
|---|---|---|---|---|
| `CONTACT_VISITOR_CONFIRMATION` | verified EkGuru sender | exact submitted visitor email | official support address | `contactVisitor` |
| `CONTACT_EKGURU_NOTIFICATION` | verified EkGuru sender | EkGuru internal inbox | exact visitor email | `contactInternal` |
| `BOOKING_STUDENT_CONFIRMATION` | verified EkGuru sender | exact booking student email | official support address | `bookingStudent` |
| `BOOKING_TUTOR_NOTIFICATION` | verified EkGuru sender | canonical tutor notification email | exact booking student email | `bookingTutor` |
| `BOOKING_EKGURU_NOTIFICATION` | verified EkGuru sender | EkGuru internal inbox | exact booking student email | `bookingInternal` |

- Contact is **not** a booking; there is no generic recipient array; no backend CC shares an address with another audience.
- `TUTOR_EMAIL_UNAVAILABLE` when a tutor has no verified operational address → the student receipt and the internal record still send; the internal record marks `tutorEmailState` honestly. No tutor email is ever invented.
- Machine-readable matrix: `reports/email-routing-matrix.json`.

## TEMPLATES

- One reusable design system (shared card shell, HTML + plain-text), every user value HTML-escaped, no raw user HTML.
- Variable registry per template (`allowedVars`); `render()` **fails** on unknown type, missing/undeclared/null variable, a raw `{placeholder}` left in output, or an unescaped `<script>`.
- Registered variables: `studentName, tutorName, bookingId, contactId, date, time, timezone, lessonType, studentRequirement, bookingStatus, nextStep, tutorNextAction, sourcePage, createdAt, supportEmail, siteUrl`.
- Role-language QA (`ROLE_QA`) — a student mail must not read like a tutor mail: all five pass.
- Subject is single-line (CR/LF collapsed) and capped at 150 chars — header-injection safe at both client and relay.
- Inventory: `reports/email-template-inventory.json`.

## SHEETS

- Google Sheets stays the canonical mutable source (settings/content/reviews/tutors) via `js/sheet.js` → normalized runtime model.
- Loader contract unchanged and verified: live-valid → cache → stale-cache+warn → safe-failure; never silently `[]`.
- A future tutor added via a Sheet row needs **no new mail-code branch**: the mailer resolves `notificationEmail → formKey → email → siteKey/SITE.email` through one chain (`EkGuruMail.tutorEmailInfo`).
- Lineage: `reports/email-data-lineage.json`.

## BOOKING SNAPSHOT

- A booking is persisted **before** send with an immutable snapshot (`js/store.js` + `js/features.js` `logBooking`):
  `booking_id(ref), student_name(name), student_email(email), tutor_id(tutorId), tutor_name_snapshot, tutor_email_snapshot_if_verified, requirement(goal/message), date/time(slot), timezone, lesson_type, status, created_at(at)`.
- `tutor_email_snapshot` is empty unless a verified operational address existed at booking time (never invented).
- Historical emails are never regenerated from later mutable Sheet data.
- The contact form now records the message **before** send (`js/ledger.js` `status:"sending"` → patched to `sent`/`failed`), so a crash mid-send leaves a durable trace.

## DELIVERY

- Per-role delivery state (`js/store.js` `emailDelivery.{student,tutor,internal}`) with `status / provider / lastAttempt / lastError / retryCount / messageId`, plus flat `student_email_*` columns derived (never hand-set).
- **ACCEPTED is never reported as DELIVERED.** `SUCCESS/PARTIAL_SUCCESS/FAILURE` + idempotency semantics.
- Idempotency keys: `BOOKING-{ref}-{STUDENT|TUTOR|INTERNAL}` and `CONTACT-{ref}-{VISITOR|INTERNAL}`, client-side (`guarded()`) and server-side (`SENT_<key>` Script Property, 7-day window, answered as dedup).
- Student ≠ tutor ≠ internal recipients are always separate sends.

## FALLBACK

Ranked chain, all only reached when the primary is not sendable/refused:

1. **Google Apps Script / Gmail** — PRIMARY (rank 1).
2. **Web3Forms** — FALLBACK (4 keys configured; can address strangers; metered 250/key/month).
3. **StaticForms** — FALLBACK (unlimited; only its registered inbox).
4. **FormSubmit** — FLOOR (free; per-address activation, cannot reach strangers).
5. **EmailJS** — INCOMPATIBLE (not configured).

- Retry is transient-only; a stranger-capable relay carries the student/visitor receipt; own-inbox mail never spends metered quota.
- Inventory: `reports/email-provider-inventory.json`.

## SECURITY

Relay contract (`tools/apps-script-mailer.gs`) — all present and verified statically + by `tools/test-email-security.js`:

- Token **only** in Script Property `MAILER_SHARED_TOKEN`; fail-closed (`Not authorised.`); client token wired via gitignored `deploy-secrets.local.json` + `tools/wire-token.py`; no secret in source (scanned).
- Message-type whitelist (the five types); unknown type refused before any recipient is touched (open-relay defence).
- Recipient validation + optional allow-list; forced `From` = owner (client `fromName` ignored); reply-to/cc through `firstEmail()` (header-injection safe).
- Payload size caps (60 KB html / 20 KB text); daily cap (90); server-side idempotency + `LockService`.
- Client templates escape XSS (`<script>`, `<img onerror>`) and collapse CR/LF in subjects.
- 20/20 security checks pass.

## TESTS

| Suite | Runner | Result |
|---|---|---|
| Template registry + render + role QA + escaping | `tools/test-email-system.js` | **63/63 PASS** |
| Mailer integration (send/contact/tutorEmailInfo/testSend) | `tools/test-email-system.js` | included above |
| Security (injection, XSS, unknown type, secrets, relay static) | `tools/test-email-security.js` | **20/20 PASS** |

- Fixtures used for preview/test: **Priya / Tara / BOOK-TEST-001** (never real customer data).
- Admin **Mail Ops** (new in `admin.html`): PRIMARY/SENDER/VERIFICATION/TOKEN/FALLBACK chips (GREEN/YELLOW/RED/GRAY — unknown never green), routing matrix, live template health, per-role delivery, **send-test restricted to controlled inboxes** (`[TEST]` prefix, refuses strangers), and fixture previews.

## LIVE

The relay is now **live and sendable** — verified end-to-end from the build sandbox on 11 Sep 2026 (~10 PM IST) against the new deployment:

| Check | Result |
|---|---|
| `GET /exec` health | `{"success":"true","status":"ok","script":"EkGuru Mail Relay","strangers":true,"limit":90,"configured":true}` |
| Wrong token | `{"success":"false","message":"Not authorised."}` — fail-closed ✓ |
| Unknown message type | `{"success":"false","message":"Unknown message type."}` — whitelist ✓ |
| Invalid recipient | `{"success":"false","message":"Missing or invalid recipient."}` ✓ |
| Controlled send (owner inbox) | `{"success":"true","message":"sent","state":"ACCEPTED"}` — owner Gmail dispatched it ✓ |
| Shipped mailer path (`testSend`) | ACCEPTED via Apps Script (`tools/test-email-live.js`) ✓ |
| Server-side idempotency | first POST → `sent`; replay → `duplicate` (no re-send) ✓ |

- Client token is **wired** (via `tools/wire-token.py`; `release-decision.js` now reports `STUDENT_EMAIL: ACCEPTED_UNVERIFIED` instead of `BLOCKED_ON_TOKEN`).
- Several `[TEST]` emails were dispatched to `EkGuruLearning@gmail.com`; the owner should see them in the inbox — that is the mailbox receipt to confirm.

## REMAINING

1. **Confirm the `[TEST]` emails arrived** in `EkGuruLearning@gmail.com` (mailbox receipt — ACCEPTED proves dispatch, the inbox proves receipt).
2. **Push the release build** (committed locally; GitHub push is credential-blocked in this sandbox) and verify `ekguru.shop` serves it.
   Local commits (Email ULTRA workstream): `85e3eee` → `f166ff1` → `d199a9a` → `1e212b9` (HEAD). The client token is **not** in any commit — it lives only in the gitignored `deploy-secrets.local.json` and is re-injected by `tools/wire-token.py` at deploy time.
3. **Two-student / two-tutor cross-routing test** in a real browser, with duplicate/retry and security replay tests against the live relay.
4. **Real student mailbox receipt** — the mandatory PASS that has not happened yet.

**Hard-stop §50: NOT PASSED.** No report may claim a student received their email until step 4 completes with two real inboxes.

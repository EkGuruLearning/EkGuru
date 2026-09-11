# EKGURU — ULTRA EMAIL ARCHITECTURE + APPS SCRIPT PRIMARY + SHEETS-DRIVEN ROUTING MASTER COMMAND

## PRODUCTION
`https://ekguru.shop/`

## OBJECTIVE

Take complete ownership of the **EkGuru email subsystem**. This is not only a student-mail bug fix. Rebuild the routing, sender identity, Apps Script relay, role-specific templates, Google Sheets data lineage, booking snapshots, delivery state, fallback, idempotency, admin observability, and real-mailbox verification so the system remains reliable when data changes and when new tutors are added.

### PRIMARY REQUIREMENT
**Google Apps Script/Gmail is Provider #1 / PRIMARY transactional email route**, provided the verified sender, deployment, authentication and real-mailbox E2E tests pass.

Do not keep a confusing mixture of providers for different forms. Build one central email orchestration layer with explicit message roles. Use another provider only as a genuinely configured and tested fallback.

---

# 1. NON-NEGOTIABLE RULES

1. Do not declare email fixed from source inspection, HTTP 200, provider ACK, or internal-mail receipt alone.
2. Real mailbox receipt is mandatory for final production PASS.
3. Never put a student's, visitor's, or tutor's arbitrary email into `From`.
4. `From` must be a verified EkGuru sender identity.
5. Never invent tutor email addresses.
6. If a tutor notification email is missing/invalid, use `TUTOR_EMAIL_UNAVAILABLE`; do not silently send to another tutor.
7. Student, tutor, internal/admin, and contact-visitor messages must use separate role-specific templates.
8. Never expose tutor private email, internal notes, provider details, tokens, or secrets to students/visitors.
9. Never use one generic recipient array for all roles.
10. Persist booking/contact records before email send attempts.
11. Persist an immutable booking snapshot at creation; historical emails must not be regenerated from later mutable Sheet data.
12. Google Sheets remains the canonical mutable source for ordinary tutor/site/content configuration where it already serves that role.
13. A Sheet fetch failure must not silently become `[]`; use live-valid → cache → stale-cache-with-warning → safe-failure.
14. A future tutor added to the canonical Sheet must work without a new tutor-specific code branch.
15. Secrets/tokens must never enter Git, browser JS, public CSV, public Sheets, logs, or reports.
16. Do not call `ACCEPTED`/provider ACK `DELIVERED`.
17. Every send job needs idempotency and per-role delivery state.
18. Contact routing must stay separate from booking routing.
19. Do not break existing Sheet-backed site data while fixing email.
20. After code changes: BUILD → DEPLOY → LIVE TEST → REAL MAILBOX → REGRESSION → FINAL REPORT.

---

# 2. READ THE WHOLE CURRENT SYSTEM FIRST

Inspect the entire repo, not only `mailer.js`.

At minimum inspect:

```text
js/mailer.js
js/site-config.js
js/features.js
js/store.js
js/admin.js
admin.html
booking-related HTML/JS
contact-form HTML/JS
tutor loading/data code
all Google Sheets loaders
all Apps Script files
tools/apps-script-mailer.gs
tools/APPS-SCRIPT-SETUP.md
tools/wire-token.py
all current email/provider tests
all current admin delivery/status code
```

Search for:

```text
MailApp
GmailApp
Gmail API
Apps Script
MAILER_SHARED_TOKEN
sendEmail
mailer
Web3Forms
StaticForms
FormSubmit
EmailJS
Resend
SMTP2GO
SES
recipient
Reply-To
replyTo
from
to
contact
booking
student_email
tutor_email
admin_email
```

Also detect every hard-coded email address in the repository.

Create/refresh:

```text
reports/email-system-baseline.json
reports/email-provider-inventory.json
reports/email-routing-matrix.json
reports/email-template-inventory.json
reports/email-data-lineage.json
```

---

# 3. APPS SCRIPT MUST BE FIRST PRIORITY

The first implementation gate is:

```text
inspect Apps Script
→ inspect current deployment
→ inspect Script Properties/config
→ verify sender identity
→ repair relay contract
→ deploy/version
→ verify /exec
→ real student mailbox
→ real tutor mailbox where available
→ internal mailbox
→ contact visitor mailbox
```

Do not proceed to declaring the email subsystem complete before this gate is passed.

The existing production `/exec` URL must be verified from the repo/config. Do not invent a new URL.

If deployment changes:

```text
record deployment/version
update site config
run contract tests
run live tests
```

Google's current Gmail documentation supports programmatic sending and send-as alias management; sender aliases may require verification, so validate the actual Gmail/Apps Script sender rather than inventing a branded From address. citeturn151412search0turn151412search6

Apps Script authorization and sending limits must also be checked; Google documents authorization failures and quota-related failures. citeturn151412search4turn151412search2

---

# 4. SENDER IDENTITY — DETERMINE THE REAL ONE

Do not guess the sender address.

Inventory:

```text
PRIMARY_SENDER_EMAIL
PRIMARY_SENDER_DISPLAY_NAME
INTERNAL_INBOX
SUPPORT_EMAIL
ADMIN_ALERT_EMAIL
```

Preferred model:

```text
From: EkGuru <verified-ekguru-sender>
```

Role-dependent `Reply-To` is allowed, but `From` must remain verified.

Inspect actual Gmail send-as aliases and verification state. Google documents send-as aliases and verification status. citeturn151412search0turn151412search7

If a custom EkGuru alias exists and is verified, use it. Otherwise use the real authenticated Gmail sender that is actually authorized by the Apps Script account.

Never do:

```text
From = student email
From = visitor email
From = tutor email
```

---

# 5. APPS SCRIPT SECRET/TOKEN RULE

If the existing relay uses:

```text
MAILER_SHARED_TOKEN
```

keep it only in Apps Script Project Settings → Script Properties (or the existing secure server-side secret mechanism).

Local tooling may use an ignored file such as:

```text
deploy-secrets.local.json
```

but it must never be committed.

Never place the token in:

```text
HTML
browser JS
site-config.js
public JSON
Google Sheet
public CSV
Git
reports
screenshots
```

Use the existing secure token-wiring tool when appropriate:

```bash
python3 tools/wire-token.py
```

Do not print or paste the token in the final report.

---

# 6. CENTRAL EMAIL ORCHESTRATOR

Create or upgrade one central conceptual layer. Reuse existing project structure where sensible instead of duplicating code.

Suggested responsibilities:

```text
email/orchestrator
email/routing
email/recipients
email/templates
email/providers
email/delivery-state
email/idempotency
email/sanitize
```

Every outbound message follows:

```text
EVENT
↓
IMMUTABLE SNAPSHOT
↓
MESSAGE TYPE
↓
RECIPIENT RESOLUTION
↓
TEMPLATE
↓
HTML + TEXT RENDER
↓
PRIMARY PROVIDER (Apps Script)
↓
RESULT
↓
SAFE RETRY
↓
CONFIGURED FALLBACK IF NEEDED
↓
DELIVERY STATE PERSISTENCE
↓
ADMIN OBSERVABILITY
```

No form/component should independently invent provider or recipient logic.

---

# 7. EXACT MESSAGE TYPES

## CONTACT

```text
CONTACT_VISITOR_CONFIRMATION
CONTACT_EKGURU_NOTIFICATION
```

## BOOKING

```text
BOOKING_STUDENT_CONFIRMATION
BOOKING_TUTOR_NOTIFICATION
BOOKING_EKGURU_NOTIFICATION
```

Only add lifecycle messages for product events that actually exist:

```text
BOOKING_CONFIRMED_STUDENT
BOOKING_CONFIRMED_TUTOR
BOOKING_RESCHEDULED_STUDENT
BOOKING_RESCHEDULED_TUTOR
BOOKING_CANCELLED_STUDENT
BOOKING_CANCELLED_TUTOR
```

Never send a fake “confirmed” message for a request/pending booking.

---

# 8. MASTER ROUTING MATRIX

Create one machine-readable routing matrix.

| Message | From | To | Reply-To | Template |
|---|---|---|---|---|
| CONTACT_VISITOR_CONFIRMATION | verified EkGuru | exact submitted visitor email | official support | Contact Visitor |
| CONTACT_EKGURU_NOTIFICATION | verified EkGuru | EkGuru internal inbox | exact visitor email | Contact Internal |
| BOOKING_STUDENT_CONFIRMATION | verified EkGuru | exact booking student email | official support | Booking Student |
| BOOKING_TUTOR_NOTIFICATION | verified EkGuru | canonical tutor notification email | official support/internal | Booking Tutor |
| BOOKING_EKGURU_NOTIFICATION | verified EkGuru | EkGuru internal inbox | official support/internal | Booking Internal |

Critical rule:

```text
studentRecipient = booking.studentEmail
visitorRecipient = contact.email
tutorRecipient = canonicalTutor.notificationEmail
internalRecipient = trustedConfig.internalInbox
```

Never build one generic `to[]` list and reuse it for different roles.

---

# 9. CONTACT FORM — SEPARATE SYSTEM/CONTENT

Contact is NOT a booking.

## Visitor confirmation

Message type:

```text
CONTACT_VISITOR_CONFIRMATION
```

Subject example:

```text
We received your message — EkGuru
```

Modern content:

```text
EKGURU
Message received

Hi {Visitor Name},

Thank you for contacting EkGuru.

Reference
{Contact ID}

We received your message and will review it.

Next step
{Truthful Next Step}

EkGuru
https://ekguru.shop/
{Support Email}
```

Do not reveal internal routing, provider, admin notes, private data, or secrets.

## Internal notification

Message type:

```text
CONTACT_EKGURU_NOTIFICATION
```

Subject:

```text
New contact request — {Category} — {Contact ID}
```

Include:

```text
Visitor name
Visitor email
Category/subject
Message
Timestamp
Source page
Reference ID
```

Header:

```text
From = verified EkGuru sender
To = internal inbox
Reply-To = exact visitor email
```

This is required so staff can press Reply to answer the actual visitor.

Do not put visitor email in `From`.

---

# 10. BOOKING — STUDENT TEMPLATE

Message type:

```text
BOOKING_STUDENT_CONFIRMATION
```

Subject:

```text
Booking request received — {Tutor Name} | EkGuru
```

Tone:

```text
friendly
reassuring
clear
non-technical
```

Modern template structure:

```text
EKGURU
Booking Request Received

Hi {Student Name},

We've received your request to learn with {Tutor Name}.

[REQUEST RECEIVED]

Booking ID
{Booking ID}

Tutor
{Tutor Name}

Date
{Date}

Time
{Time}

Timezone
{Timezone}

Lesson
{Lesson Type}

Your requirement
{Student Requirement}

Current status
{Booking Status}

What happens next
{Truthful Next Step}

[View EkGuru]
https://ekguru.shop/

Need help?
{Support Email}
```

Must NOT include:

```text
tutor private email
admin notes
internal routing
provider details
secrets
other users
```

The student receives only student-appropriate information.

---

# 11. BOOKING — TUTOR TEMPLATE

Message type:

```text
BOOKING_TUTOR_NOTIFICATION
```

Do NOT write:

```text
You booked Tara
Your booking request was received
```

The tutor needs an operational message.

Subject:

```text
New lesson request — {Student Name} — {Date} | EkGuru
```

Modern structure:

```text
EKGURU
New Lesson Request

Hi {Tutor Name},

A learner has requested a lesson with you.

[NEW REQUEST]

Booking ID
{Booking ID}

Learner
{Student Name}

Requested date
{Date}

Requested time
{Time}

Timezone
{Timezone}

Lesson type
{Lesson Type}

Learner requirement
{Student Requirement}

Current status
{Booking Status}

Your next action
{Tutor Next Action}

EkGuru
https://ekguru.shop/
```

Only include learner information necessary for the tutor to fulfill the lesson.

Never expose unnecessary private learner data.

---

# 12. BOOKING — ADMIN/INTERNAL TEMPLATE

Message type:

```text
BOOKING_EKGURU_NOTIFICATION
```

Subject:

```text
New booking request — {Student Name} → {Tutor Name} — {Booking ID}
```

Internal operational template may include:

```text
Booking ID
Status
Created at
Student name
Student email
Tutor name
Tutor ID
Tutor email/state
Date
Time
Timezone
Lesson type
Student requirement
Source page
Student delivery state
Tutor delivery state
Internal delivery state
Provider
Last error / retry state
Next internal action
```

Never send this full internal template to the student or tutor.

---

# 13. GOOGLE SHEETS IS THE MUTABLE CANONICAL SOURCE

Preserve the existing architecture where Google Sheets acts like the site's content/config database.

Canonical categories currently include:

```text
Settings
Content
Reviews
Tutors
GitHub URLs
EkGuru URLs
Full workbook
```

Required conceptual flow:

```text
Google Sheet
↓
validated loader
↓
normalized runtime model
↓
site / booking / email
```

Ordinary data changes must flow through without code edits:

```text
Sheet change
→ refresh/cache update
→ website displays new valid value
→ future booking uses current value
```

Do not create a second hard-coded tutor database in JavaScript.

---

# 14. VERY IMPORTANT — SHEET DATA VS BOOKING SNAPSHOT

This is one of the most important requirements.

Google Sheets controls **mutable current data**.

A booking controls an **immutable historical snapshot**.

When a booking is created, persist:

```text
booking_id
student_name
student_email
tutor_id
tutor_name_snapshot
tutor_email_snapshot_if_verified
student_requirement
requested_date
requested_time
timezone
lesson_type
booking_status
created_at
```

Then render booking emails from this stored snapshot.

DO NOT regenerate a historical booking email from the current Sheet row.

Example:

```text
Day 1
Tutor name = Tara
Tutor email = old@example.com
↓
Booking saved with snapshot

Day 10
Sheet changes tutor name/email

Old booking remains historically correct.
New booking uses the new valid Sheet data.
```

This is how the Sheet-backed database and transactional history coexist safely.

---

# 15. FUTURE TUTOR REQUIREMENT

When a new tutor is added to the canonical tutor Sheet, there must be no new mail-code branch.

Required flow:

```text
new Sheet row
→ schema validation
→ tutor ID validation
→ published/active validation
→ notification email validation
→ normalized tutor object
→ profile/search
→ booking resolution
→ tutor mail routing
```

Tutor email states:

```text
ACTIVE + VALID
ACTIVE + MISSING
ACTIVE + INVALID
UNPUBLISHED
DISABLED
```

If valid:

```text
BOOKING_TUTOR_NOTIFICATION → tutor notification email
```

If missing/invalid:

```text
BOOKING_TUTOR_NOTIFICATION → TUTOR_EMAIL_UNAVAILABLE
```

Still send:

```text
student confirmation
internal notification
```

Do NOT send to another tutor and do not invent an address.

---

# 16. TUTOR EMAIL FIELD

Inspect the real Sheet schema.

Prefer a dedicated field such as:

```text
notification_email
```

Do not assume public profile email equals operational notification email.

If a new canonical field is needed, make it migration-safe:

```text
existing field
→ compatibility mapping
→ new canonical field
```

Do not silently rename a production column.

Keep notification/private email fields out of public client payloads.

---

# 17. SHEETS DATA VALIDATION + CACHE

Every source needs:

```text
schema validation
required columns
row validation
type validation
duplicate ID detection
URL validation
email validation
date/status validation
```

Failure policy:

```text
LIVE VALID
↓
CACHE
↓
STALE CACHE + WARNING
↓
SAFE FAILURE
```

Never:

```text
LIVE ERROR → []
```

Changing a valid Sheet row should update the website on the existing refresh/cache cadence without requiring a code deployment.

---

# 18. CONTACT DATA MODEL

Keep compatibility with the existing store/schema, but ensure the record contains at least:

```text
contact_id
name
email
subject/category
message
created_at
source_page
status
internal_delivery_status
visitor_delivery_status
reply_to
```

Persist before sending.

---

# 19. BOOKING DATA MODEL

Keep compatibility with current code, but ensure the system stores:

```text
booking_id
student_name
student_email
tutor_id
tutor_name_snapshot
tutor_email_snapshot
requested_date
requested_time
timezone
lesson_type
student_requirement
booking_status
created_at
```

Per-role mail state:

```text
student_email_status
student_email_provider
student_email_message_id
student_email_last_error
student_email_retry_count

tutor_email_status
tutor_email_provider
tutor_email_message_id
tutor_email_last_error
tutor_email_retry_count

internal_email_status
internal_email_provider
internal_email_message_id
internal_email_last_error
internal_email_retry_count
```

Do not overwrite working compatibility fields blindly.

---

# 20. APPS SCRIPT RELAY CONTRACT

The relay must have one explicit production contract.

Logical request:

```json
{
  "type": "BOOKING_STUDENT_CONFIRMATION",
  "to": "student@example.com",
  "replyTo": "support@example.com",
  "subject": "Booking request received — Tara | EkGuru",
  "html": "...",
  "text": "...",
  "requestId": "BOOK-123:student",
  "idempotencyKey": "BOOK-123:BOOKING_STUDENT_CONFIRMATION",
  "metadata": {
    "bookingId": "BOOK-123",
    "site": "ekguru.shop"
  }
}
```

Exact field names may follow existing project conventions, but the semantics must be equivalent.

Relay requirements:

```text
authentication
message-type whitelist
recipient validation
sender enforcement
payload size limits
safe escaping/validation
rate limit
quota handling
structured result
safe diagnostics
```

The public site must not be able to turn the relay into an arbitrary open mail relay.

---

# 21. APPS SCRIPT MESSAGE WHITELIST

At minimum:

```text
CONTACT_VISITOR_CONFIRMATION
CONTACT_EKGURU_NOTIFICATION
BOOKING_STUDENT_CONFIRMATION
BOOKING_TUTOR_NOTIFICATION
BOOKING_EKGURU_NOTIFICATION
```

Reject unknown types.

Do not allow client-supplied `from` to override the verified sender.

Do not allow client-supplied internal recipient to override trusted configuration.

---

# 22. PROVIDER INVENTORY

Inspect every provider/path in code. Possible historical providers include:

```text
Google Apps Script
Web3Forms
StaticForms
FormSubmit
EmailJS
Resend
SMTP2GO
SES
SMTP
Cloudflare Worker/API
```

For each record:

```text
provider
purpose
configured
enabled
primary/fallback rank
endpoint
from
to capability
reply-to capability
quota/rate limits
secret location
last tested
actual mailbox result
status
```

Possible final statuses:

```text
PRIMARY
FALLBACK_1
FALLBACK_2
DISABLED
INCOMPATIBLE
UNKNOWN
```

`UNKNOWN` is not healthy.

Do not activate old providers just because they exist in source.

---

# 23. FALLBACK

Primary:

```text
Google Apps Script
```

Fallback must be:

```text
configured
verified/tested
arbitrary-recipient capable where required
sender-valid
Reply-To capable where required
rate/quota known
real-mailbox proven
```

Do not make the fallback chain longer just to look robust.

---

# 24. SAFE FALLBACK / DUPLICATE DEFENSE

A timeout does not prove that no message was delivered.

Therefore:

```text
provider attempt
→ idempotency key
→ result state
→ retry only according to policy
→ fallback only when safe/configured
```

Per-message idempotency keys:

```text
{bookingId}:student
{bookingId}:tutor
{bookingId}:internal
{contactId}:visitor
{contactId}:internal
```

Do not send duplicates because the browser repeated the request.

---

# 25. DELIVERY STATE MACHINE

Use explicit states such as:

```text
NOT_ATTEMPTED
QUEUED
SENDING
ACCEPTED
FAILED
RETRYABLE_FAILURE
FINAL_FAILURE
UNKNOWN
```

User-facing state should distinguish:

```text
QUEUED
SENT/ACCEPTED
FAILED
```

Do not call provider acceptance `DELIVERED` unless actual delivery evidence exists.

---

# 26. ERROR CLASSES

Use structured classes:

```text
INVALID_RECIPIENT
UNAUTHORIZED
FORBIDDEN
BAD_REQUEST
PROVIDER_TIMEOUT
PROVIDER_5XX
QUOTA_EXCEEDED
SENDER_NOT_VERIFIED
TUTOR_EMAIL_UNAVAILABLE
TEMPLATE_RENDER_ERROR
DATA_SOURCE_ERROR
IDEMPOTENCY_DUPLICATE
UNKNOWN
```

Do not reduce everything to `EMAIL_FAILED`.

---

# 27. RETRY POLICY

Retry only transient errors:

```text
timeout
temporary 5xx
temporary relay unavailable
```

Usually do not retry automatically:

```text
invalid recipient
wrong token
sender not verified
invalid payload
template error
missing tutor email
```

Avoid retry storms.

---

# 28. TEMPLATE SYSTEM

Build a reusable modern email design system, but keep role content separate.

Shared design:

```text
EkGuru branding
clean card layout
light neutral background
single strong accent
status badge
mobile-safe width
clear CTA
consistent footer
```

Every email must provide:

```text
HTML
plain text
```

Escape all user-controlled values.

No raw user HTML.

No secrets.

No raw placeholders.

---

# 29. TEMPLATE VARIABLE REGISTRY

Create a registry with allowed variables per template:

```text
studentName
studentEmail
tutorId
tutorName
tutorEmail
bookingId
contactId
date
time
timezone
lessonType
studentRequirement
bookingStatus
nextStep
tutorNextAction
sourcePage
createdAt
supportEmail
siteUrl
```

Each template must declare allowed variables.

Build fails/tests fail on:

```text
missing variable
undeclared variable
raw {placeholder}
undefined/null output
```

---

# 30. ROLE-LANGUAGE QA

Automated semantic tests must catch role swaps.

## Student mail must sound like:

```text
your request
your booking ID
your tutor
what happens next
```

and must NOT say:

```text
new lesson request for you
```

## Tutor mail must sound like:

```text
new lesson request
learner
schedule
requirement
action
```

and must NOT say:

```text
you booked
```

## Internal mail must be:

```text
operational
complete
```

## Contact visitor mail must be:

```text
message received
reference
next step
```

## Contact internal mail must be:

```text
support alert
visitor details
message
Reply-To
```

---

# 31. REPLY-TO RULES

```text
CONTACT_INTERNAL → Reply-To = visitor email
CONTACT_VISITOR → Reply-To = EkGuru support
BOOKING_STUDENT → Reply-To = EkGuru support unless current business flow explicitly supports another route
BOOKING_TUTOR → Reply-To = EkGuru support/internal unless current workflow explicitly supports direct coordination
BOOKING_INTERNAL → Reply-To = approved support/internal address
```

Never put arbitrary visitor/student/tutor address into `From`.

---

# 32. TIMEZONE / DATE SAFETY

Persist timezone in booking snapshot.

Display unambiguous values such as:

```text
7:00 PM IST (Asia/Kolkata)
```

or the actual selected IANA timezone.

Do not regenerate old booking times using the current browser locale.

---

# 33. ADMIN MAIL OPS

Upgrade the existing Admin mail area so it can show:

```text
Primary Provider
Sender Identity
Sender Verification
Apps Script Relay Health
Routing Matrix
Template Health
Contact Visitor Delivery
Contact Internal Delivery
Booking Student Delivery
Booking Tutor Delivery
Booking Internal Delivery
Fallback State
Retry Count
Last Error
Provider Reference
Recent Test Results
```

States:

```text
GREEN = verified healthy
YELLOW = warning/degraded
RED = failure
GRAY = unknown/not tested
```

Never make unknown green.

---

# 34. ADMIN SEND-TEST TOOL

Provide an admin-only controlled test action where practical.

Test types:

```text
Contact Visitor
Contact Internal
Booking Student
Booking Tutor
Booking Internal
```

Requirements:

```text
admin-only
rate-limited
controlled test address
preview before send
no raw HTML injection
no secret exposure
```

---

# 35. TEMPLATE PREVIEW TOOL

Preview each template using fixture data:

```text
Student: Priya
Tutor: Tara
Booking: BOOK-TEST-001
Date: 20 September 2026
Time: 7:00 PM
Timezone: Asia/Kolkata
Lesson: Trial lesson
Requirement: Conversation practice
```

No real customer data in previews.

---

# 36. DATA LINEAGE REPORT

Create:

```text
reports/email-data-lineage.json
```

Every template variable must map to its source.

Example:

```text
studentName
← booking form
← normalized/persisted booking

tutorName
← Tutors Sheet
← booking-time snapshot

tutorEmail
← Tutors Sheet notification_email
← booking-time snapshot

supportEmail
← trusted configuration

siteUrl
← site config

bookingStatus
← booking workflow state
```

Templates must not independently fetch random Sheet values.

---

# 37. LIVE SHEET UPDATE TEST

Run a controlled non-sensitive test:

1. Change a tutor public display field in the canonical Sheet.
2. Refresh according to the existing cache cadence.
3. Verify the site shows the new value.
4. Create a new booking using that tutor.
5. Verify the new email uses the current valid tutor data.
6. Verify an old booking's historical snapshot has not changed.

This is a hard acceptance test.

---

# 38. FUTURE-TUTOR TEST

Add a temporary valid tutor record in a safe test environment/controlled data source.

Verify, with no new code branch:

```text
profile/public data resolves
search resolves
booking resolves
tutor notification email resolves
student template uses correct tutor
internal template uses correct tutor
```

Then remove/archive the test row safely.

---

# 39. TWO-STUDENT / TWO-TUTOR CROSS-ROUTING TEST

Mandatory because it catches the exact current failure class.

### Booking A

```text
Student A → Tutor A
```

Expected:

```text
A gets A's student mail
Tutor A gets Tutor A's tutor mail
Internal gets A's internal mail
```

### Booking B

```text
Student B → Tutor B
```

Expected:

```text
B gets B's student mail
Tutor B gets Tutor B's tutor mail
Internal gets B's internal mail
```

Any cross-routing fails the release.

---

# 40. REAL MAILBOX E2E

Use controlled test inboxes.

At minimum:

```text
Student Test A
Student Test B
Tutor Test A
Internal Test
Contact Visitor Test
```

Record:

```text
test ID
timestamp
message type
recipient role
provider
provider reference
subject
provider result
actual receipt time
result
```

Do not store secrets.

Final PASS requires actual mailbox receipt.

---

# 41. CONTACT E2E

Submit contact form.

Verify:

```text
visitor receives visitor confirmation
internal receives support notification
Reply-To on internal message = visitor
no duplicate
contact record persisted
```

---

# 42. BOOKING E2E

Submit booking.

Verify order:

```text
booking validated
→ booking ID generated
→ snapshot persisted
→ student job
→ tutor job if valid
→ internal job
```

Verify all actual mailboxes.

---

# 43. DUPLICATE/RETRY TESTS

Test:

```text
double click
refresh
back/forward
slow network
same idempotency key twice
provider timeout
provider 5xx
wrong token
missing tutor email
```

Expected:

```text
no duplicate booking
no duplicate successful message
clear delivery state
safe retry/fallback
```

---

# 44. SECURITY TESTS

Add checks for:

```text
invalid recipient
header injection
HTML/XSS injection in name/message/requirement
unknown message type
missing token
wrong token
replay
oversized payload
open-relay attempt
malformed Sheet row
public PII leakage
secret leakage
```

The browser must not be able to control:

```text
From
trusted internal recipient
allowed template
provider secret
```

---

# 45. SHEET PRIVACY MODEL

Classify fields:

```text
PUBLIC
INTERNAL
SENSITIVE
SECRET
```

Examples:

```text
PUBLIC = published tutor name/bio/public lesson info
INTERNAL = moderation/workflow/internal IDs
SENSITIVE = private email/phone/address/support notes
SECRET = keys/tokens/passwords/credentials
```

Only PUBLIC data may be emitted to public page payloads.

---

# 46. DO NOT TREAT GOOGLE SHEETS AS EMAIL QUEUE

Use Google Sheets for its existing content/config role.

Do not make public CSV endpoints the sole transactional source for:

```text
booking history
retry state
delivery state
email attempts
```

Those belong in the existing persistent transactional/admin storage mechanism.

If the project already uses a private/internal Sheet for admin records, keep it private and safe.

---

# 47. PROVIDER QUOTA / LIMIT GATE

Validate actual applicable Apps Script/Gmail quotas before release.

Google's current Gmail API documentation describes per-minute quotas and recipient limits; design for the limits of the actual authenticated account/service, not hypothetical unlimited throughput. citeturn151412search2

Bookings normally have only a few recipients, so role-separated messages are acceptable and clearer than a generic multi-recipient message.

---

# 48. RELEASE SECRETS CHECK

Before commit/deploy:

```bash
git status
git diff
```

Run a secret scan.

Confirm none of these are committed:

```text
MAILER_SHARED_TOKEN
API keys
SMTP credentials
provider secrets
passwords
service-account secrets
```

---

# 49. FINAL DEPLOY ORDER

Execute:

```text
1. baseline
2. Apps Script primary relay
3. sender identity
4. routing
5. templates
6. Sheets/data lineage
7. booking snapshot
8. contact flow
9. booking flow
10. delivery states
11. idempotency
12. fallback
13. admin observability
14. tests
15. real mailbox tests
16. Sheet-change test
17. future-tutor test
18. full regression
19. deploy
20. live production test
21. final report
```

---

# 50. HARD STOP CONDITIONS

Do NOT declare PASS when any of these remain:

```text
student mailbox not actually tested
Apps Script sender not verified
Apps Script deployment unknown
token not securely configured
student recipient not exact booking email
tutor routing is hard-coded
contact visitor confirmation missing
Reply-To wrong
role templates are incorrectly shared
Sheet update breaks site
future tutor needs code edit
duplicate emails possible
fallback untested
secrets exposed
admin marks unknown green
```

---

# 51. FINAL REPORT FILES

Create/refresh:

```text
reports/email-system-baseline.json
reports/email-provider-inventory.json
reports/email-routing-matrix.json
reports/email-template-inventory.json
reports/email-data-lineage.json
reports/apps-script-mail-health.json
reports/email-release-report.json
```

No secrets in reports.

---

# 52. REQUIRED FINAL REPORT

Return exactly this structure:

```text
============================================================
EKGURU EMAIL ULTRA FINAL REPORT
============================================================

PRIMARY PROVIDER
- Provider:
- Status:
- Deployment:
- Sender:
- Sender verified:
- Real mailbox E2E:

ROUTING
- Contact visitor:
- Contact internal:
- Booking student:
- Booking tutor:
- Booking internal:

TEMPLATES
- Contact visitor:
- Contact internal:
- Booking student:
- Booking tutor:
- Booking internal:

SHEETS
- Canonical source:
- Live refresh:
- Cache:
- Schema validation:
- Future tutor support:

BOOKING SNAPSHOT
- Persisted before send:
- Historical stability:
- Tutor snapshot:
- Student email snapshot:

DELIVERY
- Student:
- Tutor:
- Internal:
- Contact visitor:
- Contact internal:

FALLBACK
- Configured:
- Tested:
- Duplicate-safe:

SECURITY
- Token secret:
- Sender spoofing blocked:
- Arbitrary relay blocked:
- Public PII scan:
- Secret scan:

TESTS
- Unit:
- Integration:
- Browser:
- Real mailbox:
- Two-student routing:
- Multi-tutor:
- Future tutor:
- Sheet update:
- Duplicate:
- Provider failure:
- Token failure:

LIVE
- Production tested:
- https://ekguru.shop/ :

REMAINING
- Exact blockers only
```

---

# 53. FINAL SUCCESS DEFINITION

The final architecture must behave like this:

```text
GOOGLE SHEETS
  │
  ├── current tutor/site/content configuration
  │
  ▼
VALIDATED RUNTIME MODEL
  │
  ▼
BOOKING CREATED
  │
  ├── immutable booking snapshot
  │
  ├── BOOKING_STUDENT_CONFIRMATION
  │        └── Apps Script → exact student mailbox
  │
  ├── BOOKING_TUTOR_NOTIFICATION
  │        └── Apps Script → canonical tutor mailbox
  │
  └── BOOKING_EKGURU_NOTIFICATION
           └── Apps Script → internal inbox

CONTACT CREATED
  │
  ├── CONTACT_VISITOR_CONFIRMATION
  │        └── Apps Script → exact visitor mailbox
  │
  └── CONTACT_EKGURU_NOTIFICATION
           └── Apps Script → internal inbox
```

Every path must have:

```text
correct sender
correct recipient
correct Reply-To
correct role-specific template
correct data lineage
correct status
idempotency
retry/fallback policy
admin observability
real mailbox verification
```

The important permanent rule is:

```text
Google Sheet change
→ current site/new-booking behavior changes automatically

Existing booking
→ historical snapshot remains stable
```

---

# 54. FINAL AGENT COMMAND

**Do not give another conceptual answer. Work directly in the repository.**

Read the current implementation first. Then make Google Apps Script the primary mail provider, choose and verify the real EkGuru Gmail sender, define the exact five message routes, build five role-specific modern templates, preserve Google Sheets as the mutable canonical data source, persist immutable booking snapshots before sending, make future tutors data-driven, add delivery state/idempotency/fallback/admin observability, and prove the result with real mailbox E2E tests.

The minimum proof is:

```text
STUDENT → STUDENT TEMPLATE → STUDENT MAILBOX
TUTOR → TUTOR TEMPLATE → TUTOR MAILBOX
ADMIN → INTERNAL TEMPLATE → ADMIN MAILBOX
VISITOR → VISITOR TEMPLATE → VISITOR MAILBOX
```

Also prove:

```text
Sheet change → site/new booking change
Sheet change → historical booking unchanged
new tutor row → no code change required
retry → no duplicates
wrong token → safe failure
provider failure → safe retry/fallback
```

Only then mark the subsystem production-ready.

END.

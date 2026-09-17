# EKGURU — ULTRA EMAIL ROUTING + BOOKING RECORD SYSTEM + MULTI-PROVIDER FAILOVER
# CRITICAL PRODUCTION WORKSTREAM
#
# This requirement is P0 / business-critical.
# Previous implementations were reported as present but did not actually work.
# Do not mark this task complete from code inspection only.
# A real end-to-end mailbox test is mandatory.

PRODUCTION:
https://ekguru.shop/

============================================================
0. CORE BUSINESS REQUIREMENT — DO NOT MISUNDERSTAND
============================================================

When a student books a tutor:

STUDENT
  |
  | completes booking
  v
EKGURU BOOKING SYSTEM
  |
  +----> STUDENT EMAIL
  |
  +----> SELECTED TUTOR EMAIL
  |
  +----> EKGURU INTERNAL RECORD / ADMIN ROOM
  |
  +----> EKGURU INTERNAL NOTIFICATION
  |
  +----> FALLBACK PROVIDERS if primary email path fails

The selected tutor MUST receive an email specifically about THEIR OWN booking.

The tutor email must NOT be a generic "new booking" email that loses:
- which tutor was selected
- student name
- student's stated requirement
- requested date/time
- timezone
- booking/reference ID
- relevant contact/lesson information

The STUDENT must separately receive an email confirming:
- which tutor they booked/requested
- their requirement/details
- selected date/time
- timezone
- booking status
- booking/reference ID
- next steps

EKGURU must permanently retain the booking record in the admin/operational data layer:
- who booked
- which tutor was selected
- what requirement the student submitted
- when
- date/time
- timezone
- booking status
- email delivery status
- relevant form fields
- provider message/reference IDs where available
- audit history

CONTACT FORM REQUIREMENT:

When a visitor submits the contact form:
  Visitor
      |
      +----> Visitor confirmation/copy
      |
      +----> EkGuru internal support/contact inbox
      |
      +----> persistent contact record
      |
      +----> fallback providers if primary fails

The exact recipient-routing rules must be explicit and testable.

============================================================
1. STOP REPEATING THE PREVIOUS FAILURE
============================================================

Historical problem:
- internal EkGuru email sometimes arrived
- visitor confirmation did not
- booking tutor email did not reliably arrive
- booking learner email did not reliably arrive
- providers existed but fallback behavior was not actually guaranteed
- code appeared implemented but production delivery was not verified

Therefore:

DO NOT say:
"email system implemented"
because provider code exists.

The only acceptable completion proof is:

FORM SUBMITTED
→ backend accepted
→ message persisted
→ recipient list resolved correctly
→ primary provider attempted
→ delivery/acceptance recorded
→ recipient actually receives test message
→ fallback tested separately
→ admin record exists
→ retry/duplicate protection verified

============================================================
2. INVENTORY ALL CURRENT MAIL PROVIDERS
============================================================

Discover every currently configured email provider/path.

Possible paths may include:
- Web3Forms
- FormSubmit
- Resend
- SMTP2GO
- Amazon SES
- Apps Script
- SMTP
- Cloudflare/worker endpoint
- another API provider
- existing fallback path

Do NOT assume which provider is primary.

Create:

reports/email-provider-inventory.json

For each provider record:

provider
purpose
contact_support
contact_visitor
booking_student
booking_tutor
booking_internal
fallback_order
API/endpoint
FROM
TO
REPLY_TO
success_response
failure_response
timeout
retry_policy
rate_limit
environment/config source
secret location
last_tested
status

============================================================
3. CENTRAL EMAIL ORCHESTRATOR
============================================================

Do NOT scatter provider logic throughout forms/components.

Create one server-side/email-service orchestration layer.

Concept:

EmailOrchestrator
  |
  +-- routing
  +-- template selection
  +-- recipient resolution
  +-- provider selection
  +-- retries
  +-- fallback
  +-- idempotency
  +-- delivery status
  +-- audit
  +-- observability

Every email-producing workflow must use this orchestrator.

Do not put private provider credentials in client JavaScript.

============================================================
4. MESSAGE TYPES — EXPLICIT CONTRACTS
============================================================

Define separate message types.

CONTACT_VISITOR_CONFIRMATION
CONTACT_EKGURU_NOTIFICATION

BOOKING_STUDENT_CONFIRMATION
BOOKING_TUTOR_NOTIFICATION
BOOKING_EKGURU_NOTIFICATION

BOOKING_RESCHEDULE_STUDENT
BOOKING_RESCHEDULE_TUTOR
BOOKING_RESCHEDULE_EKGURU

BOOKING_CANCEL_STUDENT
BOOKING_CANCEL_TUTOR
BOOKING_CANCEL_EKGURU

Only implement lifecycle messages that the product actually supports.

Do not send fake "confirmed" emails for pending requests.

============================================================
5. BOOKING RECIPIENT RESOLUTION
============================================================

THIS IS CRITICAL.

When student selects tutor ID/profile:

Resolve the tutor from the canonical data source.

DO NOT use:
- arbitrary email entered by student
- stale form value
- hard-coded generic tutor email
- currently logged-in admin email

Resolve:

booking.tutor_id
→ canonical tutor record
→ tutor public/private contact routing field
→ verified tutor email

Use the tutor's actual configured notification email.

If tutor email is missing/invalid:

DO NOT silently send to another tutor.

Mark:

TUTOR_EMAIL_UNAVAILABLE

Then:
- notify EkGuru
- show appropriate status to student
- retain booking
- do not lose the request

============================================================
6. BOOKING DATA SNAPSHOT
============================================================

At booking creation, store a snapshot of the key booking context.

Recommended:

booking_id
created_at
student_user_id if applicable
student_name
student_email
student_phone only if legitimately collected
tutor_id
tutor_name_snapshot
tutor_email_snapshot/status
lesson_type
student_requirement
message
requested_date
requested_time
timezone
duration
price_snapshot if applicable
currency
booking_status
source_page
source_locale
notes allowed for this workflow
created_by
last_updated_at

Why:
The tutor's profile/data can change later.
The booking record must still show who was selected at the time of booking.

Do not store more personal data than necessary.

============================================================
7. STUDENT EMAIL — EXACT PURPOSE
============================================================

The student email must be a student-facing confirmation, not an internal dump.

Subject example:

"EkGuru booking request received — {Tutor Name}"

Body should include:

Hello {Student Name},

We received your booking request for:
Tutor: {Tutor Name}
Date: {Date}
Time: {Time}
Timezone: {Timezone}
Lesson: {Lesson Type}
Booking ID: {Booking ID}

Your requirement:
{Student Requirement}

Current status:
{REQUESTED/PENDING/CONFIRMED/etc.}

Next step:
{Truthful next step}

Support:
{EkGuru contact}

Do not include:
- internal notes
- admin-only fields
- provider details
- tutor private data
- secret IDs

============================================================
8. TUTOR EMAIL — EXACT PURPOSE
============================================================

Tutor receives a tutor-specific notification.

Subject example:

"New booking request from {Student Name} — {EkGuru}"

Body:

Tutor:
{Tutor Name}

Student:
{Student Name}

Student email:
{Student Email}

Booking ID:
{Booking ID}

Requested date:
{Date}

Requested time:
{Time}

Timezone:
{Timezone}

Lesson type:
{Lesson Type}

Student requirement:
{Student Requirement}

Current status:
{Status}

Next action:
{Tutor Action}

This must be generated from the booking record.

DO NOT trust client-rendered HTML as the source of truth.

============================================================
9. EKGURU INTERNAL EMAIL
============================================================

Internal notification must contain operational detail.

Include:

booking ID
student
student contact
selected tutor
tutor contact/routing status
requirement
date/time/timezone
lesson type
price/currency if applicable
status
source
created_at
email delivery states
payment state if applicable
provider IDs where available

Internal staff must be able to understand:
WHO booked WHOM
WHAT they need
WHEN
CURRENT STATUS
WHETHER EMAILS WERE SENT

============================================================
10. PERSISTENT ADMIN BOOKING RECORD
============================================================

This is mandatory.

Every booking must be visible in the admin "Bookings" area / operational record system.

Minimum fields:

Booking ID
Created
Student
Student email
Tutor
Tutor ID
Requirement
Date
Time
Timezone
Lesson
Status
Payment status if applicable
Student email status
Tutor email status
EkGuru email status
Last delivery attempt
Last provider
Last error
Retry count
Updated

Admin must be able to open:

BOOKING DETAIL

and see:

Student
Tutor
Requirement
Timeline
Status history
Email delivery history
Provider attempts
Reference IDs
Notes
Next action

============================================================
11. CONTACT RECORD SYSTEM
============================================================

Every contact form submission creates a persistent internal record.

Fields:

contact_id
created_at
name
visitor_email
subject/category
message
source_page
locale
status
assigned_to where supported
reply_status
internal_email_status
visitor_confirmation_status
provider attempts
last error
updated_at

Admin should be able to view:

CONTACT DETAIL

with timeline:

received
validated
internal sent
visitor confirmation sent
reply/reviewed
resolved

Do not store unnecessary personal data.

============================================================
12. CONTACT FORM ROUTING
============================================================

For a valid contact:

Internal:
TO = configured EkGuru support/contact inbox

Visitor confirmation:
TO = exact visitor submitted email

Internal:
REPLY-TO = exact visitor submitted email

FROM:
verified EkGuru sender

Never:
FROM = arbitrary visitor email

This protects deliverability and allows staff to click Reply.

============================================================
13. MULTI-PROVIDER FALLBACK — REAL FAILOVER
============================================================

If there are 3–4 configured providers, use all where appropriate.

Example:

EMAIL ROUTER

Primary:
Provider A

Fallback 1:
Provider B

Fallback 2:
Provider C

Fallback 3:
Provider D

But do NOT send all providers simultaneously by default.

Correct behavior:

Provider A
→ fail
→ Provider B
→ fail
→ Provider C
→ fail
→ Provider D
→ final failure

For a provider response that means:
- rejected
- timeout
- network error
- unavailable
- quota/rate limit

allow fallback where safe.

For a provider response that means:
- accepted/sent

STOP the provider chain.

Do not duplicate the same email through B/C/D just because they are configured.

============================================================
14. FALLBACK PER MESSAGE TYPE
============================================================

Do NOT assume one provider chain is optimal for every email.

Build per-message routing.

Example:

CONTACT_VISITOR:
A → B → C

CONTACT_INTERNAL:
A → C → D

BOOKING_STUDENT:
B → A → C

BOOKING_TUTOR:
A → D → B

BOOKING_INTERNAL:
C → A → D

These are examples only.

Choose the actual order from:
- verified configuration
- reliability
- deliverability
- rate limits
- provider capabilities

Document final order.

============================================================
15. PROVIDER CAPABILITY MATRIX
============================================================

Create:

reports/email-provider-matrix.json

For each provider:

provider
send_support
reply_to_support
html
text
attachments if used
rate_limit
timeout
error_classes
delivery_events
webhook_support
sandbox/test mode
configuration status

This prevents trying to use a feature the provider does not support.

============================================================
16. IDEMPOTENCY — NO DUPLICATE EMAILS
============================================================

Every message must have a unique message key.

Examples:

CONTACT-{contact_id}-VISITOR
CONTACT-{contact_id}-INTERNAL

BOOKING-{booking_id}-STUDENT
BOOKING-{booking_id}-TUTOR
BOOKING-{booking_id}-INTERNAL

Before sending:
check whether that exact message role already succeeded.

If yes:
DO NOT SEND AGAIN.

If previous attempt failed:
retry according to policy.

This must work across:
- browser refresh
- double click
- API retry
- provider retry
- worker restart
- deployment restart

============================================================
17. EMAIL DELIVERY STATE MACHINE
============================================================

Use explicit states:

NOT_QUEUED
QUEUED
PROCESSING
PROVIDER_ATTEMPT
ACCEPTED
DELIVERED if actual delivery evidence exists
FAILED
RETRYING
EXHAUSTED
CANCELLED

Do not confuse:
ACCEPTED
with
DELIVERED

If provider does not provide delivery status:
show ACCEPTED / PROVIDER_ACCEPTED.

============================================================
18. RETRY STRATEGY
============================================================

Use bounded retries.

Example:
attempt 1 immediate
attempt 2 short delay
attempt 3 longer delay

Then fallback.

Do not retry:
- invalid recipient
- permanent rejection
- policy rejection
- malformed request

Retry only transient errors.

============================================================
19. PROVIDER ERROR CLASSIFICATION
============================================================

Normalize provider errors:

TRANSIENT
PERMANENT
RATE_LIMIT
AUTH
INVALID_RECIPIENT
CONFIGURATION
TIMEOUT
NETWORK
UNKNOWN

Routing:
TRANSIENT → retry
RATE_LIMIT → wait/fallback
TIMEOUT → retry/fallback
INVALID_RECIPIENT → do not loop; notify admin
AUTH/CONFIG → alert admin and fallback where safe

============================================================
20. OUTBOX / QUEUE
============================================================

For reliability, use an email outbox pattern where practical:

business event
→ database/outbox record
→ email worker/orchestrator
→ provider
→ delivery status

This prevents:
booking saved
but browser closes
before email is sent

The booking record must survive email provider failure.

============================================================
21. EMAIL + BOOKING ORDER
============================================================

Correct transaction order:

1. Validate booking
2. Resolve tutor
3. Create booking record
4. Commit booking
5. Create email outbox entries
6. Send notifications
7. Update delivery statuses

Never make booking existence depend exclusively on a browser email response.

============================================================
22. BOOKING EMAIL FAILURE MUST NOT DELETE BOOKING
============================================================

If email fails:

Booking remains stored.

Status should be:
EMAIL_DEGRADED
or appropriate operational status.

Admin gets alert.

Retry remains possible.

Student sees an honest status.

Do not tell student "booking failed" when only email failed.

============================================================
23. MANUAL RETRY FROM ADMIN
============================================================

Admin booking detail should offer:

Retry student email
Retry tutor email
Retry internal email

Requirements:
- permission check
- idempotent
- audit event
- reason
- result
- provider used

Admin must NOT need to re-submit the booking.

============================================================
24. CONTACT MANUAL RETRY
============================================================

Admin can retry:
- visitor confirmation
- internal notification

Do not create duplicate contact records.

============================================================
25. EMAIL TEMPLATES
============================================================

Create shared versioned templates.

Templates:
contact-visitor
contact-internal
booking-student
booking-tutor
booking-internal

Support:
HTML
plain text
mobile responsive

Add:
template_version

Do not make templates rely on client-side JS.

============================================================
26. EMAIL CONTENT SAFETY
============================================================

Never leak:
- API keys
- provider URLs
- internal admin notes
- secrets
- internal moderation data
- another student's information
- private tutor data

Student receives only student information.

Tutor receives only booking information required for the tutoring workflow.

EkGuru receives operational information.

============================================================
27. TIMEZONE / LOCALE
============================================================

Every booking email must display:

date
time
timezone

Do not send:
"7:00 PM"

Prefer:
"7:00 PM IST (Asia/Kolkata)"

Use the student's selected timezone or canonical booking timezone according to product design.

Tutor email should clearly communicate the relevant time basis.

Internal email should include both:
stored canonical time
displayed timezone

============================================================
28. TUTOR REQUIREMENT DELIVERY
============================================================

The student's requirement must reach the selected tutor exactly as entered/accepted by the booking system.

Preserve:
- Unicode
- Hindi
- punctuation
- line breaks
- emojis where safe

Do not silently truncate important requirements.

If requirement exceeds email length limits:
- preserve full requirement in booking record
- include concise email excerpt + secure booking detail link if appropriate

============================================================
29. SECURITY OF EMAIL LINKS
============================================================

If emails contain:
"View booking"

Use:
- authenticated admin link
- short-lived signed access only if appropriate
- no sensitive data directly in query strings

Never create publicly enumerable booking URLs like:

/booking/12345

without authorization.

============================================================
30. EMAIL DELIVERY DASHBOARD
============================================================

Admin health should show:

CONTACT
Visitor: GREEN/YELLOW/RED
Internal: GREEN/YELLOW/RED

BOOKING
Student: GREEN/YELLOW/RED
Tutor: GREEN/YELLOW/RED
Internal: GREEN/YELLOW/RED

Providers:
A
B
C
D

For each:
last success
last failure
success rate if measured
latency
last error
current state

============================================================
31. EMAIL INCIDENT ALERTS
============================================================

Alert EkGuru when:

- primary provider repeatedly fails
- fallback activated repeatedly
- all providers fail
- authentication expires
- invalid configuration
- rate limit reached
- delivery failures spike

Avoid alert storm.

Group related failures into one incident.

============================================================
32. TESTING — REAL MAILBOX, NOT CODE ONLY
============================================================

MANDATORY.

Create dedicated controlled test addresses.

CONTACT TEST:
1. Submit contact form
2. Confirm internal inbox receives
3. Confirm visitor inbox receives
4. Verify Reply-To
5. Verify persistent contact record
6. Verify no duplicate
7. Repeat with primary provider failure
8. Verify fallback provider sends

BOOKING TEST:
1. Select Tutor A
2. Student enters Requirement X
3. Submit booking
4. Verify booking record:
   student = correct
   tutor = Tutor A
   requirement = X
5. Verify student inbox receives Tutor A confirmation
6. Verify Tutor A inbox receives ONLY Tutor A booking
7. Verify internal inbox receives operational record
8. Verify all delivery statuses
9. Simulate Provider A failure
10. Verify fallback
11. Confirm no duplicate
12. Repeat with another tutor to prove routing changes correctly

CRITICAL:
Perform at least:
Tutor A test
Tutor B test

This catches hard-coded generic tutor-email bugs.

============================================================
33. NEGATIVE TESTS
============================================================

Test:
- invalid tutor ID
- tutor without email
- invalid student email
- empty requirement
- Unicode requirement
- extremely long requirement
- duplicate submit
- refresh after submit
- browser close after booking commit
- email provider timeout
- provider auth failure
- provider rate limit
- all providers unavailable

Expected:
- booking/contact remains correctly recorded where appropriate
- clear status
- no silent loss
- no duplicate
- admin can retry

============================================================
34. DATA MODEL / RELATIONAL INTEGRITY
============================================================

Verify:

booking.student_id
→ valid student

booking.tutor_id
→ valid tutor

booking.tutor_email_snapshot/status
→ correct routing evidence

booking.requirement
→ preserved

booking.email_event(s)
→ linked to booking

contact.contact_id
→ email events

email event
→ provider attempt
→ message role

No orphan email records.

============================================================
35. ADMIN ROOM / "RECORD ROOM"
============================================================

The admin "record room" must make it easy to answer:

WHO booked?
WHOM did they book?
WHAT did they request?
WHEN?
WHAT timezone?
WHAT is the booking status?
WAS the tutor notified?
WAS the student notified?
WAS EkGuru notified?
WHICH provider sent it?
DID fallback activate?
WHAT failed?
CAN ADMIN RETRY?

Provide filters:

date
student
tutor
status
email status
provider
failure
booking ID

Provide search by:
booking ID
student email
tutor email
student name
tutor name

============================================================
36. CONTACT RECORD ROOM
============================================================

Admin can search:

contact ID
name
email
date
status
source page

Open record:
message
timeline
internal notification status
visitor confirmation status
provider attempts
reply status
resolution

Never expose private admin notes to visitor.

============================================================
37. OBSERVABILITY
============================================================

Log safe events:

booking.created
booking.committed
email.queued
email.provider_attempt
email.accepted
email.delivered
email.failed
email.fallback
email.retry
email.exhausted
contact.created

Never log secrets.

Mask:
email where full address is not needed
phone
tokens
provider keys

============================================================
38. FALLBACK FAILURE SIMULATION
============================================================

Test each provider individually.

Scenario:
Provider A DOWN
→ B works

A DOWN + B DOWN
→ C works

A/B/C DOWN
→ D works

ALL DOWN
→ booking/contact still recorded
→ visible degraded state
→ admin alert
→ retry later

Do this in TEST/STAGING or controlled environment.
Do NOT intentionally break production providers.

============================================================
39. PROVIDER CONFIGURATION HEALTH
============================================================

Admin health must identify:

Provider configured?
Credential valid?
Last successful send?
Last failure?
Fallback position?
Rate-limit state?

Do not expose credential values.

============================================================
40. RELIABILITY OBJECTIVE
============================================================

Define internal targets:

Critical transactional email:
target high availability

Contact:
must persist request even if email is unavailable

Booking:
must persist booking before email attempt

Email:
must retry/fallback

Exact numeric SLA must be based on actual provider capability and plan.
Do not fabricate guarantees.

============================================================
41. FINAL REGRESSION
============================================================

Run:
full test suite
Doctor
Privacy
build
lint/typecheck
browser tests
contact E2E
booking E2E
email provider tests
fallback tests
data-integrity tests

Check:
- header still correct
- Sheets still work
- admin still works
- Learn/tools still work
- SEO still works
- no old-domain regression

============================================================
42. RELEASE GATE
============================================================

This workstream is NOT complete unless:

CONTACT:
internal email PASS
visitor copy PASS
Reply-To PASS
record PASS
fallback PASS

BOOKING:
correct tutor routing PASS
correct student email PASS
internal record PASS
requirement preserved PASS
timezone PASS
fallback PASS
duplicate protection PASS
admin retry PASS

PROVIDERS:
primary tested
fallback 1 tested
fallback 2 tested if configured
fallback 3 tested if configured

DATA:
booking persistent PASS
email events linked PASS
audit trail PASS

REAL MAILBOX:
Tutor A PASS
Tutor B PASS
Student PASS
Internal PASS

============================================================
43. FINAL REPORT
============================================================

Return exact evidence:

PROVIDER INVENTORY
- provider names
- intended role
- fallback order

CONTACT:
- internal delivery
- visitor delivery
- Reply-To
- record
- fallback

BOOKING:
- Tutor A routing
- Tutor B routing
- student routing
- internal routing
- requirement preservation
- timezone

RECORD ROOM:
- booking record
- email timeline
- contact record

RELIABILITY:
- retries
- idempotency
- fallback
- outbox
- failure recovery

TESTS:
- unit
- integration
- browser
- mailbox E2E
- provider-failure simulation

FILES CHANGED:
exact files

LIVE STATUS:
PASS / DEGRADED / FAIL

REMAINING BLOCKERS:
exact list

============================================================
44. NON-NEGOTIABLE FINAL RULE
============================================================

Do not mark this task complete because:
- provider code exists
- API returned 200
- email function returned success
- unit tests passed

Completion requires REAL END-TO-END evidence.

The business-critical promise is:

STUDENT BOOKS TUTOR
→ CORRECT TUTOR GETS THE CORRECT BOOKING
→ STUDENT GETS THE CORRECT CONFIRMATION
→ EKGURU RETAINS COMPLETE OPERATIONAL RECORD
→ IF PRIMARY EMAIL FAILS, FALLBACK TAKES OVER
→ IF ALL EMAIL FAILS, BOOKING IS STILL SAFE AND ADMIN CAN RETRY

CONTACT:

VISITOR SUBMITS
→ VISITOR RECEIVES CONFIRMATION
→ EKGURU RECEIVES INTERNAL COPY
→ CONTACT RECORD IS STORED
→ FALLBACK WORKS IF PRIMARY FAILS

END.

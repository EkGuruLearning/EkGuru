# EKGURU — P0 STUDENT BOOKING EMAIL DELIVERY REPAIR
# CRITICAL: STUDENT IS NOT RECEIVING BOOKING EMAIL
#
# User has directly verified in the browser that booking mail is currently
# reaching the internal/other path but NOT the student who submitted the booking.
#
# Treat this as a P0 production bug.
# Do not mark fixed from source inspection.
# Real mailbox end-to-end verification is mandatory.

PRODUCTION:
https://ekguru.shop/

============================================================
0. PROBLEM DEFINITION
============================================================

CURRENT OBSERVED BUG:

A student books a tutor from the website.

The student enters their email.

The booking request reaches the EkGuru side / another recipient,
but the student does NOT receive their own booking confirmation/receipt.

Required final behavior:

STUDENT BOOKS TUTOR
        |
        +--> BOOKING RECORD SAVED
        |
        +--> SELECTED TUTOR NOTIFICATION
        |
        +--> EKGURU INTERNAL NOTIFICATION
        |
        +--> STUDENT CONFIRMATION EMAIL
        |
        +--> DELIVERY/FALLBACK STATUS STORED
        |
        +--> ADMIN CAN SEE EVERYTHING

Do NOT declare success because:
- browser shows HTTP 200
- provider API says success
- internal inbox receives mail
- source code contains a student-send function

SUCCESS requires the actual student mailbox to receive the test email.

============================================================
1. READ THE CURRENT MAIL SYSTEM COMPLETELY
============================================================

Inspect current:

js/mailer.js
js/site-config.js
tools/apps-script-mailer.gs
tools/APPS-SCRIPT-SETUP.md
booking UI/form code
tutor configuration files
admin booking/email code
all current email tests

Map the complete call chain:

Booking submit
→ validation
→ booking ID
→ payload creation
→ recipient resolution
→ message generation
→ provider selection
→ send
→ response handling
→ fallback
→ persistence
→ admin status

Do not assume one provider.

============================================================
2. CURRENT PROVIDER INVENTORY
============================================================

Inventory every configured provider and classify correctly.

Possible providers currently present:
- Web3Forms
- StaticForms
- FormSubmit
- EmailJS
- Google Apps Script

IMPORTANT:
An unconfigured provider is NOT an active fallback.

Current known configuration state must be checked again.

For each provider record:

provider
configured
enabled
booking student
booking tutor
booking internal
contact visitor
contact internal
recipient support
reply-to support
CC support
quota
error classes
fallback position
last tested

Create:

reports/student-email-delivery-audit.json

============================================================
3. TRACE THE ACTUAL STUDENT EMAIL PATH
============================================================

Find exactly where the student's email address is extracted.

Expected source:
booking form's validated student email field.

Do NOT accidentally use:
- tutor email
- EkGuru email
- logged-in admin
- form owner email
- site contact email
- stale contact form email
- FormSubmit activation owner
- provider registration email

At the point just before sending, log only a SAFE diagnostic value:

message_role = BOOKING_STUDENT_CONFIRMATION
recipient_domain = example.com
recipient_valid = true

Do NOT log the full personal email.

============================================================
4. HARD REQUIREMENT — MESSAGE ROLES
============================================================

There must be distinct messages:

BOOKING_STUDENT
BOOKING_TUTOR
BOOKING_INTERNAL

They must never accidentally share the wrong recipient.

For one booking:

studentRecipient = booking.studentEmail
tutorRecipient = resolvedTutor.email
internalRecipient = configured EkGuru inbox

Do NOT build one generic recipient list and reuse it blindly.

============================================================
5. STUDENT RECIPIENT RESOLUTION
============================================================

At booking creation:

validate the student's email.

Normalize:
trim
lowercase where appropriate
Unicode-safe handling
basic valid email syntax

Reject invalid recipient safely.

Persist the normalized value with the booking record.

IMPORTANT:
The student's email must be stored before the send operation.

Do NOT depend on the browser DOM after the booking is saved.

============================================================
6. STUDENT BOOKING SNAPSHOT
============================================================

Persist:

booking_id
student_name
student_email
tutor_id
tutor_name_snapshot
student_requirement
requested_date
requested_time
timezone
lesson_type
booking_status
created_at

The email must be generated FROM THIS STORED BOOKING RECORD.

Do not rebuild the email from mutable DOM state.

============================================================
7. STUDENT EMAIL TEMPLATE
============================================================

Create a dedicated template:

BOOKING_STUDENT_CONFIRMATION

Subject example:

EkGuru booking request received — {Tutor Name}

Body:

Hello {Student Name},

We received your booking request.

Tutor:
{Tutor Name}

Booking ID:
{Booking ID}

Date:
{Date}

Time:
{Time}

Timezone:
{Timezone}

Lesson:
{Lesson Type}

Your requirement:
{Student Requirement}

Current status:
{Booking Status}

Next step:
{Truthful Next Step}

EkGuru:
https://ekguru.shop/

The student must receive a useful record of exactly what they submitted.

Do not include:
- provider details
- internal notes
- tutor private email
- admin-only information
- secrets

============================================================
8. PROVIDER CAPABILITY IS CRITICAL
============================================================

For the student message, use ONLY a provider that can actually send to the arbitrary student recipient.

Do NOT use a provider configuration that merely sends to:
- provider owner
- registered inbox
- EkGuru inbox

because that can create the exact current bug.

For every active student-mail provider, verify:

Can it send to an arbitrary recipient?
Can it set Reply-To?
Can it send from verified EkGuru identity?
Can it be used from current static/browser architecture?
Is current key valid?
What happens on quota/error?

============================================================
9. FORMSubmit ACTIVATION LIMIT
============================================================

FormSubmit may require recipient activation depending on routing/configuration.

Do NOT use FormSubmit as the sole student-mail provider if it cannot reliably send to arbitrary new student addresses without recipient activation.

If FormSubmit is in the student fallback chain:
- test with a fresh controlled student address
- verify actual receipt
- do not count it as PASS until real mailbox delivery occurs

If provider refuses new recipients:
classify as INCOMPATIBLE_FOR_STUDENT_PRIMARY.

============================================================
10. STATICFORMS / WEB3FORMS / EMAILJS / APPS SCRIPT
============================================================

For each current provider:

Run a controlled test to the same test student inbox.

Use identical:
- subject
- booking ID
- student name
- tutor
- requirement

Record:

Provider
HTTP response
Provider response
Message/reference ID if available
Actual mailbox received? YES/NO
Time to receipt
Fallback triggered? YES/NO

Do not infer delivery from response code.

============================================================
11. APPS SCRIPT STUDENT DELIVERY
============================================================

If Apps Script is used:

POST:
to = exact student email

The script must:
- validate recipient
- send using GmailApp/MailApp
- return explicit result
- enforce quota
- support replyTo where appropriate
- record/send status

IMPORTANT:
Do not send the student receipt to the script owner's email by mistake.

Student recipient must be the payload's validated "to".

Verify:
Apps Script Script Property token
deployment
current script version
Web App /exec URL
real browser request
actual mailbox receipt

============================================================
12. APPS SCRIPT AUTH
============================================================

Never paste secrets into source/chat.

If the relay uses:

MAILER_SHARED_TOKEN

ensure:
- Script Property configured
- deployment expects it
- client/request configuration matches the intended architecture
- secret is not committed to Git
- failure returns explicit AUTH error

If using a client-visible token:
document honestly that it is NOT a secret.
Do not pretend it is secure.

Prefer a server/edge relay for stronger production security if the architecture permits.

============================================================
13. EMAIL ORCHESTRATOR
============================================================

All booking mail should pass through one orchestrator.

Example:

sendTransactionalEmail({
  type: "BOOKING_STUDENT",
  messageId: "BOOKING-<id>-STUDENT",
  to: studentEmail,
  ...
})

The orchestrator owns:
- validation
- provider selection
- retry
- fallback
- idempotency
- status persistence
- error classification

Do not duplicate provider logic in booking UI components.

============================================================
14. IDEMPOTENCY
============================================================

Student confirmation key:

BOOKING-{booking_id}-STUDENT

Before every send:
check whether this exact role already succeeded.

If yes:
DO NOT send duplicate.

If failed:
retry/fallback.

This must survive:
refresh
double click
browser retry
worker retry
provider timeout
deployment restart

============================================================
15. EMAIL DELIVERY STATE
============================================================

Persist separately:

student_email_status
student_email_provider
student_email_last_attempt
student_email_last_error
student_email_retry_count
student_email_message_id

Allowed:
QUEUED
PROCESSING
PROVIDER_ATTEMPT
ACCEPTED
DELIVERED
FAILED
RETRYING
EXHAUSTED

Do NOT set DELIVERED when provider only says ACCEPTED.

============================================================
16. FALLBACK CHAIN
============================================================

Correct behavior:

Provider A
→ transient failure
→ Provider B
→ transient failure
→ Provider C
→ success

Do NOT send the same student email through all providers simultaneously.

Stop after a provider successfully accepts the message.

If provider returns permanent invalid-recipient error:
do not retry endlessly.

If ALL providers fail:
- keep booking
- keep student email
- mark EMAIL_DEGRADED / EXHAUSTED
- notify admin
- allow manual retry
- do not tell user booking was deleted

============================================================
17. CRITICAL: PROVIDER ERROR CLASSIFICATION
============================================================

Normalize:

TRANSIENT
TIMEOUT
NETWORK
RATE_LIMIT
AUTH
CONFIGURATION
INVALID_RECIPIENT
PERMANENT
UNKNOWN

Routing:

TRANSIENT → retry
TIMEOUT → retry/fallback
RATE_LIMIT → fallback
AUTH → fallback + admin alert
CONFIGURATION → fallback + admin alert
INVALID_RECIPIENT → stop + user/admin correction
PERMANENT → stop

============================================================
18. CONTACT FORM MUST REMAIN SEPARATE
============================================================

Do not fix student booking mail by breaking contact mail.

Contact requirements remain:

Visitor
→ visitor confirmation
→ EkGuru internal copy
→ Reply-To visitor

Run contact regression after changing mailer.

============================================================
19. TUTOR MAIL MUST REMAIN SEPARATE
============================================================

If tutor email is unavailable:

TUTOR_EMAIL_UNAVAILABLE
→ EkGuru internal fallback

Do NOT accidentally route tutor fallback to the student.

Verify:
student ≠ tutor ≠ internal recipient.

============================================================
20. ADMIN BOOKING RECORD
============================================================

Admin must show:

Booking ID
Student
Student email
Tutor
Requirement
Date
Time
Timezone
Status

EMAILS:
Student: SENT/ACCEPTED/DELIVERED/FAILED
Tutor: ...
EkGuru: ...

PROVIDER:
Student provider
Fallback provider
Last attempt
Last error
Retry count

Admin action:
Retry student email

Do not create a new booking when retrying mail.

============================================================
21. BROWSER UX
============================================================

When student submits booking:

State:
Submitting…

Then only after booking is persisted:

Booking request received.

Display:
Booking ID
Tutor
Date/time/timezone
Email confirmation status

If booking succeeds but email is degraded:
say so honestly.

Example:

"Your booking request was saved. We couldn't confirm email delivery yet; your request is safely recorded."

Do NOT show:
"Email sent"
unless verified at the appropriate level.

============================================================
22. STUDENT RECEIPT LINK
============================================================

If the email contains:
View booking

use an authorized mechanism.

Do not expose:
https://ekguru.shop/booking/12345
without access control.

Prefer:
authenticated booking dashboard
or short-lived signed link where appropriate.

============================================================
23. ACTUAL MAILBOX TEST — MANDATORY
============================================================

Use at least TWO controlled student test addresses.

Test A:
Student A books Tutor A.

Verify:
Student A receives Student A confirmation.

Test B:
Student B books Tutor B.

Verify:
Student B receives Student B confirmation.

This catches:
hard-coded recipient
provider-owner routing
wrong field
stale recipient
shared inbox bug

============================================================
24. FAILURE TESTS
============================================================

Test:
invalid email
empty email
uppercase email
leading/trailing spaces
Unicode name
Unicode requirement
long requirement
double click
refresh after submit
browser close after booking save
provider timeout
provider 500
provider rate limit
provider auth failure
provider quota exhausted
all providers unavailable

Expected:
booking remains safe
student recipient is preserved
admin can retry
no duplicate booking
no duplicate email after successful idempotent send

============================================================
25. END-TO-END TIMING
============================================================

Measure:

T_submit
T_booking_persisted
T_first_provider_start
T_provider_response
T_fallback_start
T_email_status_recorded

And actual:
T_mailbox_received

Report separately.

Do NOT report "200ms response time" as email delivery time.

============================================================
26. EMAIL CONTENT QA
============================================================

Verify in the real received email:

From
To
Reply-To
Subject
Tutor
Student
Booking ID
Requirement
Date
Time
Timezone
Status
EkGuru link

Check:
desktop email
mobile email
plain text
HTML

No broken styles.
No raw placeholders.
No escaped HTML.
No secrets.

============================================================
27. DELIVERABILITY
============================================================

Inspect:
From domain
Reply-To
SPF
DKIM
DMARC
provider sender identity

Do not put:
student@example.com
into FROM.

Use verified EkGuru sender.

Student email:
FROM = verified EkGuru sender
TO = student

Tutor:
FROM = verified EkGuru sender
TO = tutor when verified

Internal:
FROM = verified EkGuru sender
TO = EkGuru

============================================================
28. REPLAY / DUPLICATE DEFENSE
============================================================

If the same booking submit is retried:

Do NOT create:
two bookings
two student confirmations
two tutor notifications

Use:
booking ID
submission ID
idempotency key

============================================================
29. UNIT + INTEGRATION + BROWSER TESTS
============================================================

Add tests for:

recipient resolution
message generation
provider selection
fallback
idempotency
state transitions
admin record

Browser:
submit booking
inspect UI state
verify network request
verify provider attempt

Mailbox:
verify real receipt

============================================================
30. RELEASE GATE
============================================================

This P0 bug is NOT complete unless:

STUDENT:
actual mailbox received = PASS

TUTOR:
correct tutor recipient = PASS if verified tutor email exists
otherwise TUTOR_EMAIL_UNAVAILABLE = PASS

EKGURU:
internal record/email = PASS

BOOKING RECORD:
complete = PASS

FALLBACK:
tested = PASS

IDEMPOTENCY:
tested = PASS

ADMIN:
delivery status + retry = PASS

CONTACT:
still works after fix = PASS

============================================================
31. FINAL REPORT
============================================================

Return:

ROOT CAUSE:
exact reason student mail was not reaching student

CODE:
exact files changed

PROVIDERS:
provider
configured
tested
result
fallback order

BOOKING:
student recipient
tutor recipient
internal recipient

REAL MAILBOX:
Student A PASS/FAIL
Student B PASS/FAIL

TIMING:
submit
persist
provider
fallback
mailbox

ADMIN:
record
email status
retry

REGRESSION:
contact
tutor
student
booking

LIVE:
verified at https://ekguru.shop/
YES/NO

REMAINING:
exact blockers

============================================================
32. NON-NEGOTIABLE
============================================================

Do not say "student email fixed" because:
- function exists
- API returned 200
- internal inbox got mail
- provider returned success

It is fixed only when:
STUDENT SUBMITS
→ BOOKING SAVED
→ STUDENT RECIPIENT CORRECTLY RESOLVED
→ STUDENT EMAIL SENT
→ ACTUAL STUDENT TEST INBOX RECEIVES IT
→ NO DUPLICATE
→ ADMIN RECORD SHOWS THE RESULT
→ FALLBACK WORKS WHEN PRIMARY FAILS

END.

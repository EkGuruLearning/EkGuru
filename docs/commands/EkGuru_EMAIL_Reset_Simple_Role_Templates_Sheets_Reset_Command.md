# EKGURU — EMAIL SYSTEM RESET + SIMPLE ROLE TEMPLATES + SHEETS CSV RESET
# P0 — DO THIS AS THE NEW SINGLE EMAIL/DATA RESET COMMAND

PRODUCTION:
https://ekguru.shop/

============================================================
0. USER'S REQUIRED RESULT — KEEP THIS SIMPLE
============================================================

The email system is currently over-engineered from the user's point of view.

DO NOT add more visible complexity.

The final system must be simple:

BOOKING
  ├── Student gets: "Congratulations, your booking request was received"
  ├── Tutor gets: "Congratulations, you have a new booking request"
  └── EkGuru/Admin gets: complete operational record

CONTACT — VISITOR STARTS
  ├── Visitor gets: confirmation for the message they sent
  └── EkGuru gets: complete visitor message

CONTACT — ADMIN STARTS
  ├── Recipient gets: the actual message sent by EkGuru
  └── EkGuru/Admin gets: an internal copy/record of what was sent

Every role MUST get a different template and wording.

Do not send a tutor a student-style "your booking" email.
Do not send a student a tutor-style "new lesson request" email.
Do not send the admin a vague generic email.

============================================================
1. FIRST — STOP AND SNAPSHOT
============================================================

Before modifying anything:

1. Back up the current repository/config.
2. Export/snapshot the current live Google Sheet CSV data for:
   - Settings
   - Content
   - Reviews
   - Tutors
   - GitHub URLs
   - EkGuru URLs
3. Record current row counts, headers and checksums.
4. Save the backup outside the active production data path.

DO NOT destroy current data before an export succeeds.

============================================================
2. WORKSPACE CLEANUP
============================================================

The user wants the working workspace cleaned.

Within the agent's repository/workspace ONLY:

- preserve the main `EkGuru` project folder/repository,
- remove obsolete generated scratch files, duplicate exports, stale temporary bundles, and unrelated files,
- do NOT delete `.git` or repository-critical files,
- do NOT delete production source,
- do NOT delete backups created in §1,
- do NOT delete Google Sheet data.

At the end show:

WORKSPACE CLEANUP
- preserved: EkGuru project
- deleted: exact count/list
- backups: exact location
- unrelated production data deleted: NO

Do NOT interpret this as permission to delete the user's persistent Google Drive/Sheets.

============================================================
3. REMOVE OLD PUBLIC CSV LINKS FROM THE SITE
============================================================

The user wants the current Google Sheet CSV source links removed NOW.

Therefore:

Search the repository for every current production CSV URL/GID reference.

Known historical sources include:

Settings gid 764031473
Content gid 2135319947
Reviews gid 1290168568
Tutors gid 834026040
GitHub URLs gid 1240181234
EkGuru.shop URLs gid 355826593
Full workbook

Remove these live public CSV URLs from active runtime configuration.

IMPORTANT:
DO NOT break the site.

Replace live Sheet fetches temporarily with:

DATA_SOURCE_STATUS = PAUSED_FOR_REUPLOAD

and safe local/generated data where the current architecture allows it.

No public page should expose the old CSV URLs after this change.

Admin should clearly show:

Sheets: PAUSED — new upload links required

DO NOT invent replacement URLs.

============================================================
4. GENERATE FRESH CSV FILES
============================================================

Generate fresh, clean CSV files for the user to upload into new Google Sheet tabs later.

Required files:

csv/
  ekguru_settings.csv
  ekguru_content.csv
  ekguru_reviews.csv
  ekguru_tutors.csv
  ekguru_github_urls.csv
  ekguru_urls.csv

Also create:

csv/README.md

The CSVs must use the REAL CURRENT REPOSITORY SCHEMA.

DO NOT invent column names merely because they sound better.

Workflow:

1. Read current loader code.
2. Identify exact expected headers.
3. Export/normalize current data into those exact schemas.
4. Preserve existing values.
5. Remove broken/obsolete rows only when the current validator proves them invalid.
6. Add newly required fields only with a migration-safe compatibility mapping.

For the Tutors CSV specifically, support the canonical operational routing field:

`notification_email`

If the current sheet uses another email field, preserve compatibility and document:

old field → canonical notification_email

Do NOT make public tutor pages expose private notification_email.

============================================================
5. SHEETS ARCHITECTURE
============================================================

Google Sheets remains the MUTABLE CANONICAL SOURCE for:

- site settings
- published content
- reviews
- tutor profiles/configuration
- URL inventories

Flow:

Google Sheet
→ validated loader
→ normalized runtime model
→ site

Ordinary Sheet edits must not require code edits.

If a Sheet fetch fails:

LIVE VALID
→ CACHE
→ STALE CACHE + WARNING
→ SAFE FAILURE

NEVER:

LIVE ERROR
→ []

============================================================
6. VERY IMPORTANT — BOOKING SNAPSHOT
============================================================

Do NOT make booking emails dependent on a fresh Sheet fetch after the booking is created.

At booking creation persist:

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

Then generate all three booking emails from this stored snapshot.

This means:

CURRENT SHEET = current data for NEW bookings

BOOKING SNAPSHOT = historical truth for an EXISTING booking

If a tutor's name/email later changes in Sheets:
- future bookings use the new valid data
- old bookings remain unchanged

============================================================
7. BOOKING EMAIL FLOW — EXACTLY THREE EMAILS
============================================================

BOOKING SUBMITTED
   |
   +--> STUDENT EMAIL
   |
   +--> TUTOR EMAIL
   |
   +--> EKGURU INTERNAL EMAIL

Each is a separate email job.

Each has:

- separate recipient
- separate template
- separate message type
- separate delivery status
- separate idempotency key

============================================================
8. BOOKING — STUDENT TEMPLATE
============================================================

MESSAGE TYPE:
BOOKING_STUDENT_CONFIRMATION

SUBJECT:
Congratulations — your booking request was received | EkGuru

BODY COPY:

Hi {Student Name},

Congratulations! Your booking request has been received by EkGuru.

Reference Number:
{Booking ID}

You requested a lesson with:
{Tutor Name}

Your message:
{Student Requirement}

Requested date:
{Date}

Requested time:
{Time}

Timezone:
{Timezone}

Current status:
{Booking Status}

What happens next:
{Truthful Next Step}

Please keep your reference number for future communication.

EkGuru
https://ekguru.shop/

STYLE:
- simple
- modern
- reassuring
- student-focused
- no internal information
- no tutor private email
- no provider information

The student does NOT need a huge operational email.

============================================================
9. BOOKING — TUTOR TEMPLATE
============================================================

MESSAGE TYPE:
BOOKING_TUTOR_NOTIFICATION

SUBJECT:
Congratulations — you have a new booking request | EkGuru

BODY COPY:

Hi {Tutor Name},

Congratulations! You have received a new booking request.

Reference Number:
{Booking ID}

Student:
{Student Name}

Student Email:
{Student Email}

Requested date:
{Date}

Requested time:
{Time}

Timezone:
{Timezone}

Lesson:
{Lesson Type}

Student's message:
{Student Requirement}

What to do next:
Please reply to this email / use the available booking action to confirm whether you are available.

You can respond with:
- Available
- Not available
- Available at another time: {Tutor Alternative Time Instruction}

EkGuru will continue the booking process based on your response.

EkGuru
https://ekguru.shop/

IMPORTANT:
The wording must be tutor-facing.

Never say:
"You booked..."
"Your booking was received..."

The tutor RECEIVED a request; the student made the request.

If direct reply is actually supported, tell the tutor exactly how.

If direct reply is NOT supported by the current product, do not claim it is.

============================================================
10. BOOKING — EKGURU INTERNAL TEMPLATE
============================================================

MESSAGE TYPE:
BOOKING_EKGURU_NOTIFICATION

SUBJECT:
New booking request — {Student Name} → {Tutor Name} | {Booking ID}

BODY:

EKGURU INTERNAL BOOKING

Reference Number:
{Booking ID}

Student:
{Student Name}

Student Email:
{Student Email}

Tutor:
{Tutor Name}

Tutor ID:
{Tutor ID}

Tutor Email:
{Tutor Email / TUTOR_EMAIL_UNAVAILABLE}

Date:
{Date}

Time:
{Time}

Timezone:
{Timezone}

Lesson:
{Lesson Type}

Student Message:
{Student Requirement}

Booking Status:
{Booking Status}

Email Delivery:
Student: {Student Delivery Status}
Tutor: {Tutor Delivery Status}
Internal: {Internal Delivery Status}

Next Admin Action:
{Admin Next Action}

Source:
{Source Page}

This is the operational/internal version.
Do not send it to student or tutor.

============================================================
11. TUTOR EMAIL RECIPIENT RESOLUTION
============================================================

Never hard-code tutor-specific branches.

Correct:

booking.tutor_id
→ canonical Tutors row
→ validated notification_email
→ tutor recipient

Tutor states:

ACTIVE + VALID
ACTIVE + MISSING
ACTIVE + INVALID
UNPUBLISHED
DISABLED

If valid:
SEND TUTOR EMAIL

If missing/invalid:
TUTOR_EMAIL_UNAVAILABLE

Still send:
- Student email
- Internal EkGuru email

Never:
- invent a tutor email
- send to a different tutor
- send to public profile email unless the existing schema explicitly defines it as the operational email

Future tutors must work automatically after a valid row is added.

============================================================
12. CONTACT FORM — VISITOR STARTS
============================================================

A visitor may contact EkGuru through multiple public contact forms.

ALL public contact forms must go through the SAME central contact-email orchestration.

Flow:

VISITOR CONTACT
  ├──> VISITOR CONFIRMATION
  └──> EKGURU INTERNAL NOTIFICATION

Do not maintain separate inconsistent mail logic per contact form.

------------------------------------------------------------
CONTACT VISITOR TEMPLATE
------------------------------------------------------------

MESSAGE TYPE:
CONTACT_VISITOR_CONFIRMATION

SUBJECT:
We received your message — EkGuru

BODY:

Hi {Visitor Name},

Thank you for contacting EkGuru.

We have received your message.

Reference Number:
{Contact ID}

Your message:
{Message}

What happens next:
{Truthful Next Step}

EkGuru
https://ekguru.shop/

This email is ONLY for the visitor.

------------------------------------------------------------
CONTACT INTERNAL TEMPLATE
------------------------------------------------------------

MESSAGE TYPE:
CONTACT_EKGURU_NOTIFICATION

SUBJECT:
New contact message — {Contact ID}

BODY:

EKGURU INTERNAL CONTACT

Reference Number:
{Contact ID}

Name:
{Visitor Name}

Email:
{Visitor Email}

Subject:
{Subject}

Message:
{Message}

Submitted:
{Timestamp}

Source:
{Source Page}

Reply-To:
{Visitor Email}

Internal action:
{Admin Next Action}

This email is ONLY for EkGuru/admin.

============================================================
13. CONTACT FORM — ADMIN STARTS A MESSAGE
============================================================

There are two sides:

A) ADMIN → VISITOR
B) ADMIN INTERNAL COPY

When Admin sends a direct contact message:

ADMIN
  ├──> VISITOR / RECIPIENT
  └──> EKGURU INTERNAL COPY

------------------------------------------------------------
ADMIN → RECIPIENT
------------------------------------------------------------

MESSAGE TYPE:
ADMIN_CONTACT_OUTBOUND

SUBJECT:
{Admin Subject}

BODY:

Hi {Recipient Name},

{Admin Message}

Reference:
{Contact/Conversation ID}

Regards,
EkGuru
{Support Contact}

This is a direct message from EkGuru.

------------------------------------------------------------
ADMIN INTERNAL COPY
------------------------------------------------------------

MESSAGE TYPE:
ADMIN_CONTACT_INTERNAL_COPY

SUBJECT:
Admin sent a contact message — {Conversation ID}

BODY:

EKGURU INTERNAL COPY

Recipient:
{Recipient Name}

Recipient Email:
{Recipient Email}

Subject:
{Admin Subject}

Message Sent:
{Admin Message}

Reference:
{Conversation ID}

Sent By:
{Admin Identity}

Timestamp:
{Timestamp}

============================================================
14. PROVIDER RULE — SIMPLE
============================================================

Use provider roles explicitly.

PRIMARY:

Google Apps Script

Use Apps Script for:

- student email
- tutor email
- visitor confirmation
- admin → recipient message

INTERNAL UNLIMITED/RELIABLE ROUTE:

Use the configured high-capacity/internal provider for:

- EkGuru internal booking notification
- EkGuru internal contact notification
- EkGuru internal copy of admin outbound contact

Do NOT assume a provider is unlimited unless the actual configured provider/plan proves it.

If the current "unlimited" provider is the existing internal/form provider, keep it only for internal destinations after verifying its actual capability.

============================================================
15. FALLBACK ORDER
============================================================

Each role gets a provider chain.

STUDENT:
Apps Script primary
→ fallback provider #1
→ fallback provider #2
→ final failure

TUTOR:
Apps Script primary
→ fallback provider #1
→ fallback provider #2
→ final failure

VISITOR:
Apps Script primary
→ fallback provider #1
→ fallback provider #2
→ final failure

EKGURU INTERNAL:
Configured high-capacity internal provider primary
→ Apps Script fallback
→ final failure

ADMIN → RECIPIENT:
Apps Script primary
→ configured fallback
→ final failure

ADMIN INTERNAL COPY:
Configured high-capacity internal provider
→ Apps Script fallback
→ final failure

IMPORTANT:
The actual providers must be discovered from the existing repository/configuration.

Do NOT blindly turn on Web3Forms/FormSubmit/EmailJS/StaticForms/etc.

A provider is a valid fallback ONLY if:
- configured
- enabled
- arbitrary-recipient capable where required
- sender verified
- tested
- duplicate-safe

============================================================
16. FALLBACK MUST NOT DUPLICATE
============================================================

Use:

entityId + messageType

as the idempotency key.

Examples:

BOOK-123:BOOKING_STUDENT_CONFIRMATION
BOOK-123:BOOKING_TUTOR_NOTIFICATION
BOOK-123:BOOKING_EKGURU_NOTIFICATION

CONTACT-123:CONTACT_VISITOR_CONFIRMATION
CONTACT-123:CONTACT_EKGURU_NOTIFICATION

ADMIN-123:ADMIN_CONTACT_OUTBOUND
ADMIN-123:ADMIN_CONTACT_INTERNAL_COPY

If primary may have succeeded but timed out:
DO NOT blindly send fallback.

Track:

NOT_ATTEMPTED
SENDING
ACCEPTED
FAILED
UNKNOWN
RETRYING
FINAL_FAILURE

============================================================
17. FROM / TO / REPLY-TO
============================================================

ALL user-facing mail:

FROM = verified EkGuru sender

Never:
FROM = student
FROM = visitor
FROM = tutor

BOOKING STUDENT:
TO = exact booking.student_email
Reply-To = official EkGuru support

BOOKING TUTOR:
TO = canonical tutor.notification_email
Reply-To = official EkGuru support OR supported direct-response route

BOOKING INTERNAL:
TO = configured EkGuru internal inbox

CONTACT VISITOR:
TO = exact visitor.email
Reply-To = official EkGuru support

CONTACT INTERNAL:
TO = EkGuru internal inbox
Reply-To = visitor.email

ADMIN → RECIPIENT:
TO = exact admin-selected recipient
Reply-To = official EkGuru support

ADMIN INTERNAL COPY:
TO = EkGuru internal inbox

============================================================
18. MODERN DESIGN — KEEP ALL FIVE TEMPLATES DIFFERENT
============================================================

Create a shared EkGuru email shell:

- EkGuru logo/wordmark
- clean background
- centered content card
- clear heading
- one status badge
- key information rows
- one optional CTA
- simple footer
- mobile responsive
- plain-text alternative

Then role-specific content:

STUDENT:
friendly / reassuring

TUTOR:
action / request focused

ADMIN:
operational / dense / complete

VISITOR:
warm / confirmation

ADMIN OUTBOUND:
professional / direct

Do not duplicate paragraphs across roles.

============================================================
19. SHEETS LINKS — REMOVE NOW
============================================================

Remove all active public CSV URLs and old GID-based URLs from:

- site config
- runtime data config
- health dashboard
- generated static files where used
- docs that are shipped to production
- browser JS
- admin public-facing configuration

Preserve old links ONLY in a local migration/back-up report if necessary.

Do not publish the old links.

============================================================
20. FRESH CSV UPLOAD PROCESS
============================================================

Generate:

csv/ekguru_settings.csv
csv/ekguru_content.csv
csv/ekguru_reviews.csv
csv/ekguru_tutors.csv
csv/ekguru_github_urls.csv
csv/ekguru_urls.csv

The CSVs must be generated from the current source before unlinking.

Then:

1. User creates new Sheet tabs.
2. User pastes/uploads each CSV.
3. User publishes the new tabs.
4. User provides new CSV links.
5. A separate next deployment wires those new URLs.

Do NOT guess the new URLs now.

============================================================
21. CSV SCHEMA RULE
============================================================

The CSV headers MUST match the repository's actual current loader schema.

Before creating the CSV files:

- inspect loader
- inspect validation
- inspect consumers
- export current rows
- retain compatible names
- document changes

Do NOT arbitrarily rename all columns.

For Tutors:
prefer/normalize operational email as:

notification_email

while keeping migration compatibility if an existing `email` field is used.

============================================================
22. SHEET → SITE UPDATE
============================================================

After new links are provided later:

Sheet change
→ refresh/cache
→ site reflects valid new value
→ future booking uses new data

No code deployment for ordinary data edits.

But:

booking snapshot stays frozen.

============================================================
23. MULTIPLE CONTACT FORMS
============================================================

Find ALL contact-form entry points, including:

- public contact form
- admin contact/communication form
- any duplicate legacy contact forms
- modal/contact widget
- footer/secondary contact submission

Do not leave one old form on an obsolete mailer.

Every public visitor contact form must resolve to:

CONTACT_VISITOR_CONFIRMATION
+
CONTACT_EKGURU_NOTIFICATION

Admin outbound must resolve to:

ADMIN_CONTACT_OUTBOUND
+
ADMIN_CONTACT_INTERNAL_COPY

============================================================
24. DO NOT OVERBUILD THE COPY
============================================================

The user explicitly wants the mail text SIMPLE.

Do not include unnecessary:

- provider information
- long legal blocks
- huge diagnostic sections
- technical delivery explanation
- admin notes
- tutor private data
- internal routing details

Keep important information and reference number.

============================================================
25. EXACT MINIMUM BOOKING CONTENT
============================================================

STUDENT:
- congratulations
- reference number
- tutor requested
- message
- date/time/timezone
- status
- next step

TUTOR:
- congratulations / new booking request
- reference number
- who requested
- student email
- message
- date/time/timezone
- what tutor should do next

ADMIN:
- reference number
- who booked whom
- student email
- tutor + tutor email state
- message
- date/time/timezone
- status
- delivery status

============================================================
26. EXACT MINIMUM CONTACT CONTENT
============================================================

VISITOR:
- thank you
- reference number
- their message
- next step

EKGURU:
- who
- email
- subject
- complete message
- reference
- timestamp
- reply-to

ADMIN → RECIPIENT:
- message
- reference
- EkGuru identity

ADMIN INTERNAL COPY:
- who was contacted
- email
- exact message
- reference
- timestamp

============================================================
27. TESTS
============================================================

Mandatory:

A. Student booking:
Student A → receives Student template

B. Tutor booking:
Tutor A → receives Tutor template

C. Internal:
EkGuru → receives Internal template

D. Visitor contact:
Visitor → receives Visitor template
EkGuru → receives Internal template

E. Admin outbound:
Recipient → receives Admin outbound template
EkGuru → receives Internal copy

F. Two-student routing:
Student A must never receive Student B mail.

G. Two-tutor routing:
Tutor A must never receive Tutor B mail.

H. Template semantics:
Tutor template must not contain student-facing booking language.
Student template must not contain tutor operational wording.
Internal template must not leak to public recipients.

I. Duplicate submission:
one event → one effective message per role.

J. Provider failure:
primary fails → tested fallback.

============================================================
28. HARD STOP — NO GREEN WITHOUT REAL MAILBOX
============================================================

Do NOT declare:

"EMAIL FIXED"

until actual controlled inboxes receive:

- Student A
- Student B
- Tutor A if configured
- Internal EkGuru
- Visitor A
- Admin outbound recipient
- Admin internal copy

A provider HTTP 200 is NOT enough.

============================================================
29. FINAL REPORT
============================================================

Return:

EMAIL ARCHITECTURE
- primary provider
- internal provider
- fallback order
- sender identity

ROUTING
- student
- tutor
- internal
- visitor
- admin outbound
- admin internal copy

TEMPLATES
- student
- tutor
- internal
- visitor
- admin outbound
- admin internal copy

SHEETS
- old URLs removed: YES/NO
- fresh CSVs generated: YES/NO
- exact schemas
- row counts
- future upload instructions

WORKSPACE
- only EkGuru project retained: YES/NO
- stale/unrelated files removed
- backups retained

TESTS
- unit
- integration
- browser
- real mailbox
- fallback
- duplicate
- two-student
- two-tutor
- contact visitor
- admin outbound

REMAINING BLOCKERS
- exact items only

============================================================
30. FINAL IMPLEMENTATION PRINCIPLE
============================================================

DO NOT make the user manage five different email systems.

The user should only need to know:

BOOKING:
- student gets student mail
- tutor gets tutor mail
- EkGuru gets internal mail

CONTACT:
- visitor gets visitor confirmation
- EkGuru gets internal mail

ADMIN CONTACT:
- recipient gets admin's message
- EkGuru gets internal copy

Everything else:
provider selection, fallback, retry, idempotency, routing, sender enforcement, template rendering, logging and delivery-state management must happen automatically.

END.

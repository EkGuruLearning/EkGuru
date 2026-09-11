# EkGuru — ULTRA Admin + Live Health + Privacy + Every-Page Production Hardening

PRODUCTION:
https://ekguru.shop/

PURPOSE:
The current validation reports:
- Privacy scan: BLOCKED
  Run: node tools/privacy.js --sheets --live
- Doctor: 2 problem(s)
  123 checks, 1 warning(s)

The admin system and every public/admin page must be brought to production-grade / ultra-level quality.

IMPORTANT:
Do not assume "admin-only" means it can remain unfinished.
Admin, moderation, content, tutor, booking, mail, Sheets, SEO and health systems are part of the production platform and must be reliable.

Do not make destructive changes without backup/snapshot.
Do not expose private data.
Do not invent health metrics.
Do not report a green health status when critical checks are actually failing.

============================================================
1. BASELINE FIRST
============================================================

Before modifications:

Run:
node tools/privacy.js --sheets --live

Run the full doctor suite.

Record:
- every privacy check
- every doctor check
- every warning
- every error
- every blocked check
- runtime
- endpoint
- file/source responsible

Save a machine-readable baseline:

reports/admin-baseline.json

Do not overwrite the baseline after fixes.

============================================================
2. PRIVACY SCAN — UNBLOCK COMPLETELY
============================================================

Investigate why:

node tools/privacy.js --sheets --live

is BLOCKED.

DO NOT simply skip the check.

Determine whether the blocker is:
- inaccessible published CSV
- Google Sheet permission
- unexpected public data
- private field exposure
- schema mismatch
- live fetch failure
- timeout
- malformed response
- secrets
- email/PII exposure
- tutor private information
- admin-only fields leaking into public output
- Apps Script response problem

For every Sheets source:
- Settings
- Content
- Reviews
- Tutors
- GitHub URLs
- EkGuru URLs
- Full workbook

check:
- public/private status
- actual columns
- sensitive columns
- email/phone fields
- admin-only notes
- internal IDs
- secrets/tokens
- private URLs
- unpublished records

Public output must never expose unnecessary private data.

============================================================
3. SHEETS PRIVACY MODEL
============================================================

Create a clear data classification:

PUBLIC
INTERNAL
SENSITIVE
SECRET

Examples:

PUBLIC:
- published tutor name
- public tutor bio
- public lesson price
- public article content

INTERNAL:
- moderation notes
- internal workflow state
- internal IDs where not needed publicly

SENSITIVE:
- personal phone
- private email
- private address
- support notes
- private tutor details

SECRET:
- API keys
- tokens
- passwords
- credentials

Only PUBLIC data may be emitted to public web pages.

Never ship INTERNAL/SENSITIVE/SECRET fields to client JavaScript just because the browser could technically hide them.

============================================================
4. DATA SOURCE HARDENING
============================================================

Centralize:
- source URL
- gid
- schema
- field classification
- cache
- fallback
- timeout
- retry policy

Every source requires:
- schema validation
- required columns
- type validation
- row validation
- duplicate ID detection
- URL validation
- email validation
- date validation
- status validation

Never replace valid data with an empty array after a fetch failure.

Use:
LIVE VALID
→ CACHE
→ STALE CACHE WITH WARNING
→ SAFE FAILURE

not:

LIVE ERROR
→ []

============================================================
5. APPS SCRIPT HEALTH
============================================================

Audit:

https://script.google.com/macros/s/AKfycbwG978gM3Vspo0r8JmNxRojiUwA5h0tWoFd8p9vQf5x-NX9QGDB8VCr0j1LnTPoOjqtdA/exec

Test:
- latency
- HTTP status
- payload schema
- empty payload
- malformed payload
- timeout
- permissions
- rate-limit behavior
- stale deployment
- doGet/doPost
- error response consistency

Do not make public pages depend on an admin-only Apps Script path unless truly required.

============================================================
6. ULTRA LIVE HEALTH DASHBOARD
============================================================

Build/upgrade an admin health dashboard.

The dashboard must show LIVE status for:

SITE
DNS
HTTPS
CERTIFICATE
CLOUDFLARE
GITHUB PAGES
DEPLOYMENT
SITEMAP
ROBOTS
ADS.TXT

DATA
Settings CSV
Content CSV
Reviews CSV
Tutors CSV
GitHub URLs CSV
EkGuru URLs CSV
Apps Script

EMAIL
Contact provider
Contact visitor confirmation
Contact internal notification
Booking internal
Booking learner
Booking tutor
Reply-To
Mail provider
SPF
DKIM
DMARC

SEARCH
Sitemap crawl
URL count
200
3xx
4xx
5xx
canonical
noindex
orphan
old-domain references

UX
Mobile smoke test
Desktop smoke test
JS errors
broken assets
horizontal overflow

SECURITY
Secrets scan
Public PII scan
Admin exposure scan
CORS
open redirects
form abuse

HEALTH STATES:

GREEN = verified healthy
YELLOW = warning / degraded
RED = failure
GRAY = not tested / unavailable

Do not mark:
unknown = green.

============================================================
7. LIVE HEALTH UPDATE
============================================================

Health must refresh without requiring a full page reload.

Preferred:
- manual Refresh Health button
- automatic periodic refresh with a safe interval
- last checked timestamp
- duration
- status source
- previous status
- status change indicator

Example:

EMAIL
Healthy
Last checked: 10:42:31
Latency: 420ms
Previous: Healthy

Do not hit expensive providers continuously.

Use caching and rate limits.

============================================================
8. HEALTH CHECK HISTORY
============================================================

Store:
timestamp
check
status
latency
error code
safe error message

Show:
- current
- previous
- trend

Do not store sensitive payloads.

Allow:
- last 10 checks
- last 24 hours
- optionally last 7 days

============================================================
9. ALERTS
============================================================

Generate a visible admin alert when:
- Sheets fail
- Apps Script fails
- email delivery fails
- booking provider fails
- sitemap fails
- robots fails
- ads.txt fails
- production becomes HTTP
- old domain redirect breaks
- critical API latency spikes
- public PII is detected

Do not alert repeatedly every refresh.

Deduplicate alerts by incident.

============================================================
10. ADMIN DASHBOARD — DATA OPERATIONS
============================================================

Every admin data screen must support:

- loading state
- empty state
- error state
- retry
- stale data warning
- last updated
- source status

No silent zero-state.

Example:

NOT:
0 tutors

when the Tutors CSV failed.

Instead:
Tutors unavailable
Source: tutors CSV
Last valid sync: ...
Retry

============================================================
11. ADMIN CONTENT MANAGEMENT
============================================================

Content admin must provide:

- search
- filtering
- language
- topic
- status
- publish/unpublish
- last updated
- quality score
- canonical
- indexability
- duplicate risk
- translation status

Prevent publishing:
- empty content
- missing title
- missing H1
- duplicate slug
- invalid canonical
- invalid language
- broken image
- missing required fields

============================================================
12. ADMIN TUTOR MANAGEMENT
============================================================

Tutor dashboard must detect:

- missing bio
- missing image
- missing language
- invalid price
- invalid email
- duplicate profile
- broken profile URL
- stale availability
- unpublished tutor with public profile
- public/private field leakage

Use explicit states:

DRAFT
PENDING_REVIEW
APPROVED
PUBLISHED
SUSPENDED
ARCHIVED

Do not allow accidental public exposure of draft/private tutors.

============================================================
13. ADMIN REVIEW/MODERATION
============================================================

Review moderation must provide:

- pending
- approved
- rejected
- flagged
- spam

Require moderation before publishing user-generated reviews where appropriate.

Never fabricate reviews.

Do not expose reviewer private information unnecessarily.

============================================================
14. ADMIN BOOKING OPERATIONS
============================================================

Booking admin must show:

- ID
- learner
- tutor
- date
- time
- timezone
- status
- created
- updated
- email delivery status
- payment state if applicable

Actions:
- view
- approve/confirm where supported
- reschedule
- cancel
- retry notification
- inspect delivery state

No action should silently fail.

Every destructive action needs:
- confirmation
- audit event
- safe idempotency

============================================================
15. ADMIN EMAIL OPERATIONS
============================================================

Dashboard should expose safe delivery status:

CONTACT
internal notification
visitor confirmation
reply-to

BOOKING
internal
learner
tutor

Statuses:
QUEUED
SENT
ACCEPTED
DELIVERED when provider actually confirms it
FAILED
RETRYING

Do not call ACCEPTED "DELIVERED".

Provide:
- provider message ID
- timestamp
- last error
- retry action
where safe.

Never expose API credentials.

============================================================
16. ADMIN SEO CONTROL CENTER
============================================================

Build/upgrade a single SEO dashboard.

Show:
- total URLs
- intended indexable
- noindex
- redirects
- 404
- orphan
- canonical problems
- hreflang problems
- sitemap count
- old-domain references
- thin pages
- duplicate clusters

Provide direct navigation to affected pages.

============================================================
17. ADMIN PRIVACY CENTER
============================================================

Add:
- PUBLIC fields
- INTERNAL fields
- SENSITIVE fields
- SECRET detection

Run automated scan across:
- source
- build
- JSON
- CSV
- JS
- HTML
- API responses
- browser network payloads

Detect patterns for:
- email
- phone
- address
- auth token
- API key
- passwords
- private notes

Use allowlists for intentionally public fields.

Do not leak full secrets into logs.

============================================================
18. DOCTOR — FIX ALL PROBLEMS
============================================================

Run the existing Doctor.

Current reported:
123 checks
2 problems
1 warning

Find every failed/problem check.

DO NOT:
- downgrade a failed check
- mark skipped
- mute warning
- rewrite test to avoid finding the problem

Fix the underlying issue.

Then run Doctor again.

Required final:
0 problems
0 unexpected warnings

If any check genuinely cannot be executed:
mark:
BLOCKED WITH REASON
not PASS.

============================================================
19. EVERY PAGE — GLOBAL HEALTH AUDIT
============================================================

For every public page type:

Home
About
Contact
Privacy
Terms
Disclaimer
Tutor listing
Tutor profile
Guide index
Guide detail
Topic
Question
Toolbox
Tool
Daily Hindi
Daily lesson
Country
Language
Search
Directory
Booking
Any utility

Check:

HTTP
canonical
robots
title
description
H1
schema
hreflang
internal links
broken links
JS
assets
mobile
desktop
accessibility
performance

No page should be silently degraded.

============================================================
20. EVERY PAGE — ERROR STATE
============================================================

Every dynamic page must have:

LOADING
SUCCESS
EMPTY
ERROR
STALE

Do not show:
blank white page
empty card grid
0 results caused by backend failure
fake success

============================================================
21. EVERY PAGE — MOBILE QA
============================================================

Test real Chromium:

320x568
360x800
390x844
430x932
768x1024

Check:
- header
- search
- nav
- forms
- buttons
- modals
- tables
- cards
- Hindi text
- footer
- ads
- fixed elements

No horizontal clipping.

============================================================
22. EVERY PAGE — DESKTOP QA
============================================================

Test:

1024x768
1100x700
1200x800
1280x720
1366x768
1440x900
1536x864
1600x900
1920x1080

No:
- overlap
- off-screen button
- clipped content
- broken grid
- giant whitespace
- tiny unreadable text

============================================================
23. HEADER CURRENT ISSUE
============================================================

Fix the screenshot-confirmed crowding/overlap.

Header requirements remain:

NO:
Learn
Become a Tutor
Coming Soon

YES:
Logo
Search
Find Tutors
How it works
Book a trial
Language
Currency

Measure real geometry.

Do not use overflow-x clipping to hide defects.

============================================================
24. FORM RELIABILITY
============================================================

All forms:
contact
booking
newsletter where applicable
tutor application where applicable
search

must support:
- validation
- loading
- success
- partial success
- failure
- retry
- duplicate protection
- accessible labels

============================================================
25. SECURITY
============================================================

Audit:
- secrets
- API keys
- source maps
- admin endpoints
- CORS
- CSRF where applicable
- XSS
- injection
- open redirects
- SSRF where server fetches URLs
- webhook signature validation
- rate limits
- spam
- brute force

Never expose private sheet data or credentials.

============================================================
26. AUDIT LOG
============================================================

For admin actions:

who
what
when
target
result

Log:
publish
unpublish
delete
approve
reject
booking change
tutor change
review moderation
settings change

Do not log unnecessary private data.

============================================================
27. ADMIN RBAC
============================================================

Verify roles.

Examples:
SUPER_ADMIN
ADMIN
EDITOR
MODERATOR
SUPPORT

Each role gets only required actions.

Test:
- unauthorized
- read-only
- destructive actions
- direct URL access
- API authorization

Do not rely on hiding buttons for security.
Enforce server-side authorization.

============================================================
28. BACKUP / RECOVERY
============================================================

Before major data mutations:

- snapshot data
- config
- current generated site
- critical CSV schemas
- current build

Test that backups can be restored or at least parsed.

============================================================
29. PERFORMANCE OF ADMIN
============================================================

Admin pages must not load massive datasets into browser unnecessarily.

Use:
- pagination
- filtering
- lazy loading
- debounced search
- virtual lists where needed

Public website must not inherit admin-only heavy code.

============================================================
30. LIVE SMOKE TEST
============================================================

After changes deploy and verify:

Homepage
Contact
Booking
Tutor list
Tutor profile
Toolbox
Tool
Daily Hindi
Search
About
Privacy
Terms
Disclaimer

Then:
- actual contact E2E mail test
- actual booking E2E mail test
- Sheets source test
- Apps Script test
- Doctor
- Privacy scan
- full sitemap crawl
- mobile browser smoke
- desktop browser smoke

============================================================
31. FINAL GATE
============================================================

Required:

Privacy scan:
PASS
0 blocked
0 unexpected failures

Doctor:
PASS
0 problems
0 unexpected warnings

Data:
all required sources healthy or safely degraded

Email:
contact internal PASS
contact visitor PASS
Reply-To PASS
booking internal PASS
booking learner PASS
booking tutor PASS/N/A

SEO:
sitemap PASS
robots PASS
ads.txt PASS
canonical PASS
hreflang PASS/appropriate
no critical orphan pages

UX:
mobile PASS
desktop PASS
header PASS
forms PASS

Security:
no critical secret/PII leak
RBAC PASS
audit logging PASS

============================================================
32. FINAL REPORT
============================================================

Return exact:

PRIVACY:
before
after
blocked checks
fixed leaks
remaining risks

DOCTOR:
before
after
failed checks fixed
remaining

HEALTH:
number of live checks
green
yellow
red
gray

DATA:
source status
row counts
schema issues

EMAIL:
contact internal
contact visitor
reply-to
booking internal
booking learner
booking tutor
delivery evidence
duplicate protection

ADMIN:
RBAC
audit log
content
tutor
reviews
bookings
SEO
privacy

PUBLIC SITE:
page count
200
3xx
4xx
5xx
orphans
canonical problems
hreflang problems
JS errors
mobile failures
desktop failures

FILES CHANGED:
exact files

TESTS:
exact commands
passed/failed

CRITICAL:
Never declare 100% perfect.
Report real blockers honestly.

============================================================
33. FINAL OPERATING PRINCIPLE
============================================================

FIND
→ BACKUP
→ FIX
→ TEST
→ DEPLOY
→ LIVE VERIFY
→ RECHECK

Do not merely suppress warnings.
Do not hide broken health states.
Do not expose admin/private data.
Do not let failed external sources silently become empty content.
Do not let a public feature report success before the operation actually succeeds.

The admin system must become an operational control center for the entire EkGuru production platform.

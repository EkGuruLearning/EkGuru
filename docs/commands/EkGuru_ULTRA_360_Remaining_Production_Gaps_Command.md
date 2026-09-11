# EKGURU — ULTRA 360° REMAINING PRODUCTION GAP IMPLEMENTATION
# Use AFTER / ALONGSIDE the existing master commands.
# This file covers the remaining platform-level workstreams not fully covered
# by the previous SEO / AdSense / Learn / Tools / Admin / Email commands.

PRODUCTION:
https://ekguru.shop/

PRIMARY GOAL:
Take EkGuru from a technically improved learning website to a robust,
secure, recoverable, monitored, globally usable production platform.

IMPORTANT:
- Read the already-approved master commands first if they are present.
- Do NOT remove or weaken previously implemented requirements.
- Do NOT rewrite working systems unnecessarily.
- Before destructive changes, back up/snapshot.
- Every feature must be tested in the LIVE production environment where possible.
- Never claim "perfect" or "guaranteed".
- Never fabricate compliance, uptime, payment status, reviews, users, or analytics.

============================================================
PHASE 0 — MERGED BASELINE
============================================================

Before changes:

1. git status
2. current commit / branch
3. production build identity
4. existing Doctor result
5. existing Privacy result
6. full test-suite result
7. current URL count
8. current data-source status
9. current email status
10. current booking/payment status if implemented
11. current admin-health status

Write:

reports/ultra360-baseline.json

Do NOT overwrite baseline after fixes.

============================================================
PHASE 1 — AUTHENTICATION + ACCOUNT SECURITY
============================================================

Audit the entire auth stack.

Check:
- signup
- login
- logout
- email verification
- password reset
- session creation
- session expiry
- refresh
- revoked sessions
- password change
- account deletion
- data export where applicable
- device/session visibility if supported

Security requirements:
- server-side authorization
- secure session handling
- secure cookies where applicable
- CSRF protection where applicable
- rate limiting
- brute-force protection
- password hashing through a strong established library
- no passwords in logs
- no tokens in URLs
- no secrets in client bundle
- predictable error responses that do not expose account existence unnecessarily

Test:
- unauthorized direct URL
- expired session
- revoked session
- role escalation
- stale token
- concurrent sessions
- password reset replay
- repeated login failures

============================================================
PHASE 2 — ROLE-BASED ACCESS CONTROL
============================================================

If roles exist, formally define:

SUPER_ADMIN
ADMIN
EDITOR
MODERATOR
SUPPORT
TUTOR
LEARNER

Use only roles actually supported by the product.

For EVERY protected action:
- check permission server-side
- do not rely on hidden buttons
- verify object ownership where relevant
- prevent horizontal privilege escalation
- prevent vertical privilege escalation

Test:
- role A accessing role B URL
- role A calling role B API
- direct endpoint access
- manipulated IDs
- manipulated payloads

============================================================
PHASE 3 — BOOKING STATE MACHINE
============================================================

If bookings exist, formalize the lifecycle.

Possible states:

DRAFT
REQUESTED
PENDING
CONFIRMED
RESCHEDULE_REQUESTED
RESCHEDULED
CANCELLED
COMPLETED
NO_SHOW
FAILED

Only use states that the product actually supports.

Rules:
- every transition must be explicit
- invalid transitions must fail safely
- state changes must be idempotent
- every mutation needs an audit event
- user-facing status must match backend status
- email notifications must match the same state

Examples:
REQUESTED ≠ CONFIRMED
PAYMENT_PENDING ≠ PAID

Never display a stronger status than backend evidence supports.

============================================================
PHASE 4 — PAYMENT / MONEY INTEGRITY
============================================================

ONLY if payment exists or is being used:

Audit:
- payment creation
- redirect
- success callback
- failure callback
- cancellation
- webhook
- signature verification
- refund
- partial refund where supported
- duplicate webhook
- duplicate charge protection
- currency
- amount
- tax/fee display
- booking/payment reconciliation

NEVER trust a client-provided:
amount
status
payment-success flag

Server must verify provider evidence.

Implement:
idempotency keys
webhook replay protection
signature validation
transaction/reference IDs
safe reconciliation

Test:
- success
- failure
- cancel
- double click
- duplicate webhook
- delayed webhook
- out-of-order webhook
- timeout
- browser closed during payment
- refresh after payment

If no payment system is active:
report NOT_APPLICABLE and do not invent one.

============================================================
PHASE 5 — CALENDAR / TIMEZONE / AVAILABILITY
============================================================

For booking/tutor systems:

Use one canonical time handling layer.

Every stored event must have:
- UTC or canonical timestamp
- source timezone where necessary
- displayed timezone
- unambiguous local time

Test:
- India
- US
- Europe
- DST
- midnight crossing
- month/year crossing
- date rollover
- locale display

Availability rules must prevent:
- double booking
- stale slot selection
- booking unavailable time
- race condition between users

Use server-side final availability validation.

============================================================
PHASE 6 — DISASTER RECOVERY
============================================================

Create a real recovery strategy.

BACKUP:
- source/config
- critical data
- schemas
- deployment state
- content metadata
- tutor/review datasets where appropriate
- booking records
- configuration secrets metadata (NOT raw secrets in insecure backups)

Define:
RPO
RTO

If business values are not defined, choose conservative engineering defaults and clearly report them.

Create:
- backup validation
- restore procedure
- rollback procedure
- last-known-good build

Run a safe restore test on a non-production copy.

============================================================
PHASE 7 — DEPLOYMENT SAFETY
============================================================

Implement:
- pre-deploy tests
- build validation
- smoke tests
- canary/staged deploy where feasible
- post-deploy checks
- automatic or documented rollback

Deploy gate must stop production release when critical checks fail.

Critical:
- build failure
- Doctor red
- privacy red
- broken sitemap
- critical JS errors
- contact failure
- booking failure
- broken production domain

============================================================
PHASE 8 — UPTIME + OBSERVABILITY
============================================================

Create production monitoring for:

homepage
key page
contact endpoint
booking endpoint
Apps Script
CSV sources
sitemap
robots
ads.txt
email subsystem
health API
critical admin API

Track:
status
latency
error rate
last success
last failure

States:
GREEN
YELLOW
RED
UNKNOWN

Unknown MUST NOT become GREEN.

============================================================
PHASE 9 — INCIDENT MANAGEMENT
============================================================

Create incident records:

incident_id
start_time
service
severity
status
symptom
root_cause
resolution
ended_at

Severity:
SEV-1
SEV-2
SEV-3
SEV-4

Deduplicate repeated alerts.

Do not spam the admin every refresh.

Provide:
- acknowledge
- resolve
- reopen if recurring
- event history

============================================================
PHASE 10 — RATE LIMITING + ABUSE PROTECTION
============================================================

Protect:
- contact
- booking
- login
- password reset
- tutor application
- review
- search
- public APIs
- Apps Script if exposed

Use:
- IP-based limits
- account-based limits
- endpoint-specific limits
- exponential backoff
- CAPTCHA/verification where genuinely necessary

Do not punish normal users with overly aggressive limits.

Return correct rate-limit responses and user-friendly messages.

============================================================
PHASE 11 — BOT / SPAM / FRAUD DEFENSE
============================================================

Detect:
- burst contact submissions
- repeated bookings
- duplicate reviews
- fake tutor registrations
- suspicious account creation
- automated search abuse
- unusual API patterns

Signals must not automatically ban legitimate users without a review path.

Store only necessary security data.

============================================================
PHASE 12 — DATA CONSISTENCY / TRANSACTIONS
============================================================

Audit relationships:

USER
→ tutor
→ booking
→ review

TUTOR
→ availability
→ booking
→ review

CONTENT
→ language
→ topic
→ canonical
→ sitemap

URL
→ page
→ canonical
→ internal links

Find dangling references.

If multiple changes must happen atomically:
use transactions or a reliable equivalent.

Never partially update booking/customer state.

============================================================
PHASE 13 — DATA VERSIONING / SCHEMA MIGRATION
============================================================

Introduce schema versioning for critical data.

Before migration:
- snapshot
- migration plan
- compatibility plan

After migration:
- data validation
- row counts
- referential integrity
- rollback plan

Never silently reinterpret old records.

============================================================
PHASE 14 — SEARCH SYSTEM
============================================================

Upgrade site search.

Search across:
- tutors
- lessons
- guides
- tools
- questions
- topics
- vocabulary

Features:
- typo tolerance
- normalization
- Hindi/English mixed queries
- transliteration matching
- synonyms only where linguistically valid
- category filtering
- useful no-result handling

No-result UX:
“No exact match”
+
closest useful results
+
suggested tools/topics

Do not make search-result pages indexable by default.

============================================================
PHASE 15 — SITE PERSONALIZATION
============================================================

If the user opts in / uses account features:

Support:
- level
- interests
- recent learning
- weak topics
- preferred study duration
- saved words/tools

Use this to recommend:
- next lesson
- practice
- tool
- review

Avoid unnecessary personal-data collection.

Do not create discriminatory recommendations.

============================================================
PHASE 16 — PROGRESS + RETENTION
============================================================

Where appropriate:

- lesson progress
- completed practice
- weak-topic list
- streak
- saved vocabulary
- review queue
- learning path progress

Provide:
pause/resume
reset
delete local data
account data deletion where applicable

Do not use manipulative notification patterns.

============================================================
PHASE 17 — PWA / OFFLINE LEARNING
============================================================

Where useful and safe:

- installable PWA
- offline lesson shell
- cached static learning content
- offline status
- cache versioning
- safe invalidation

Do NOT cache:
- private booking data
- private messages
- sensitive account data
unless secure and explicitly required.

Test:
- first install
- offline startup
- stale cache
- new release
- cache invalidation

============================================================
PHASE 18 — MEDIA ARCHITECTURE
============================================================

For images/audio/video:

- correct MIME types
- dimensions
- compression
- lazy loading
- preload only where useful
- captions/transcripts where applicable
- poster images
- accessible controls

For video pages:
- only use video structured data where genuine video exists
- do not fake duration or upload date

For audio:
- provide transcript/text alternative where useful

============================================================
PHASE 19 — IMAGE / SOCIAL DELIVERY
============================================================

Every important content type should have:
- correct favicon
- OG title
- OG description
- OG image
- OG URL
- correct Twitter/X metadata where used

Do not generate missing social images dynamically on every request if avoidable.

No broken image URLs.

============================================================
PHASE 20 — GLOBAL LEGAL / PRIVACY READINESS
============================================================

Because EkGuru may serve international users:

Audit:
- privacy
- cookies
- analytics disclosures
- advertising disclosures
- account data
- booking data
- tutor data
- review data
- data deletion
- data export where applicable

Do NOT claim legal compliance country-by-country unless actually assessed.

Create a compliance matrix:

COUNTRY/REGION
DATA SCOPE
LEGAL BASIS / NOTICE REQUIREMENTS
COOKIE/CONSENT
RETENTION
USER RIGHTS
ACTION
REVIEW DATE

Prioritize high-traffic markets.

============================================================
PHASE 21 — INTERNATIONALIZATION CORE
============================================================

Make locale support robust:

language
region
currency
timezone
date
time
numbers
plural rules
week start
script
RTL

Test:
English
Hindi
Spanish
French
German
Portuguese
Arabic
Japanese
Korean

Only ship languages actually supported by content/UI.

No fake translations.

============================================================
PHASE 22 — RTL / SCRIPT QA
============================================================

For RTL:
- layout direction
- icons
- dropdowns
- forms
- numbers
- mixed script
- breadcrumbs

For Devanagari and complex scripts:
- line height
- shaping
- clipping
- cursor movement
- wrapping
- search
- tool output

Test real browsers and real strings.

============================================================
PHASE 23 — FEATURE FLAGS
============================================================

For high-risk new features:
- feature flag
- staged rollout
- kill switch
- metrics
- fallback

Do not hide failures behind permanent feature flags.

============================================================
PHASE 24 — ADMIN ACTION SAFETY
============================================================

Destructive actions require:
- confirmation
- clear consequence
- optional reason
- audit log
- permission check

Examples:
delete content
remove tutor
reject review
cancel booking
refund payment
change settings

No destructive GET endpoints.

============================================================
PHASE 25 — SUPPORT SYSTEM
============================================================

Create a robust support workflow if not already present:

contact
→ ticket/reference
→ status
→ assignment
→ reply
→ close

Statuses:
OPEN
IN_PROGRESS
WAITING_USER
RESOLVED
CLOSED

At minimum:
- reference ID
- timestamp
- user email
- category
- message
- status
- audit trail

Do not expose internal notes to users.

============================================================
PHASE 26 — USER-FACING ERROR QUALITY
============================================================

Every major system needs useful error messages.

NOT:
Something went wrong.

PREFER:
“We couldn't complete your booking because the selected slot is no longer available. Please choose another time.”

Do not expose:
- stack traces
- secret names
- internal paths
- provider credentials

============================================================
PHASE 27 — CUSTOMER DATA EXPORT / DELETION
============================================================

Where accounts exist:

User should be able to:
- request data export
- request account deletion
- understand deletion consequences

Deletion must:
- revoke sessions
- remove/anonimize data according to policy
- preserve legally required records where necessary
- revoke saved tokens

Do not delete data required for operational integrity without a policy decision.

============================================================
PHASE 28 — CACHE / CDN SAFETY
============================================================

Audit caching.

Public cache:
- static assets
- public pages
- public content

Private/no-store:
- account
- booking
- admin
- personal dashboard

Ensure user A can never receive user B's private cached response.

Test with multiple sessions.

============================================================
PHASE 29 — SECURITY HEADERS
============================================================

Audit:
- HSTS where appropriate
- CSP
- X-Content-Type-Options
- Referrer-Policy
- Permissions-Policy
- frame protections
- secure cookies
- cross-origin policy where appropriate

Do not ship an overly strict CSP that breaks core functionality without a rollout plan.

============================================================
PHASE 30 — SUPPLY-CHAIN / DEPENDENCY SECURITY
============================================================

Audit:
- npm dependencies
- vulnerable packages
- abandoned packages
- transitive dependencies
- unexpected scripts

Use:
npm audit / equivalent
lockfile validation
dependency update strategy

Do not blindly upgrade major dependencies without regression testing.

============================================================
PHASE 31 — SECRET MANAGEMENT
============================================================

Search repository/build/history for:
- API keys
- tokens
- passwords
- SMTP credentials
- payment secrets
- private service URLs

Rotate compromised secrets.

Do not merely delete them from source if already exposed.

Never print secrets in logs.

============================================================
PHASE 32 — API CONTRACTS
============================================================

For internal/public APIs define:

request schema
response schema
errors
auth
rate limit
version

Validate server-side and client-side.

No endpoint should randomly return:
HTML
JSON
empty body
different schema
for the same request type.

============================================================
PHASE 33 — BACKWARD COMPATIBILITY
============================================================

If old URLs/API contracts exist:
- maintain migration path
- redirect/deprecate deliberately
- do not break old production links unnecessarily

Record deprecated routes.

============================================================
PHASE 34 — REAL ANALYTICS
============================================================

Measure product outcomes:

ORGANIC:
impressions
clicks
CTR
position
landing page
country

PRODUCT:
tool use
tool completion
lesson completion
practice completion
search success
tutor click
booking start
booking completion
contact completion

RELIABILITY:
errors
latency
downtime

Avoid collecting sensitive educational or personal data unnecessarily.

============================================================
PHASE 35 — EXPERIMENTATION
============================================================

Add safe experimentation only where useful:

CTA
tool layout
learning-path presentation
onboarding
search ranking

Requirements:
- feature flag
- clear success metric
- no SEO cloaking
- no inconsistent content for crawlers/users
- rollback

============================================================
PHASE 36 — CRITICAL USER JOURNEYS
============================================================

End-to-end test these flows:

1. Google-like visitor
→ homepage
→ search
→ learn page
→ tool
→ practice

2. Visitor
→ contact
→ internal email
→ visitor confirmation
→ Reply-To

3. Learner
→ tutor search
→ tutor profile
→ booking
→ booking status
→ learner email
→ tutor email
→ internal email

4. Admin
→ login
→ health
→ data
→ content
→ tutor
→ review
→ booking
→ SEO

5. User
→ account
→ progress
→ logout
→ login again

6. Error journey
→ provider failure
→ graceful fallback
→ recovery

============================================================
PHASE 37 — CHAOS / FAILURE TESTING
============================================================

Safely simulate:
- CSV unavailable
- Apps Script timeout
- email provider unavailable
- booking provider timeout
- API 500
- slow network
- offline
- stale cache
- malformed row
- duplicate webhook
- duplicate form submission

System must:
- fail gracefully
- preserve user data
- communicate status honestly
- recover automatically where safe

============================================================
PHASE 38 — RELEASE READINESS
============================================================

Before production release:

- build
- unit tests
- integration
- browser
- accessibility
- security
- privacy
- Doctor
- sitemap
- SEO
- email E2E
- booking E2E
- health
- backup verification

Block deployment on critical failure.

============================================================
PHASE 39 — LIVE POST-DEPLOY
============================================================

After deployment:

1. homepage
2. learn
3. toolbox
4. tutor search
5. tutor profile
6. contact
7. booking
8. admin login
9. health
10. sitemap
11. robots
12. ads.txt

Then:
- live crawl
- mobile smoke
- desktop smoke
- email test
- Doctor
- Privacy
- health refresh

============================================================
PHASE 40 — ULTRA SCORECARD
============================================================

Score ONLY for internal prioritization:

AUTH/SECURITY /100
RBAC /100
BOOKING /100
PAYMENTS /100 or N/A
DATA INTEGRITY /100
BACKUP/RECOVERY /100
OBSERVABILITY /100
ABUSE PREVENTION /100
SEARCH /100
PERSONALIZATION /100
RETENTION /100
PWA/OFFLINE /100
MEDIA /100
GLOBALIZATION /100
PRIVACY /100
PERFORMANCE /100
ACCESSIBILITY /100
SUPPORT /100
ANALYTICS /100
RELEASE SAFETY /100

For every score <90:
- exact issue
- exact fix
- test
- remaining risk

============================================================
PHASE 41 — FINAL REPORT
============================================================

Return:

REMAINING GAPS FOUND
ROOT CAUSES
FIXES IMPLEMENTED
FILES CHANGED
DATA CHANGES
DB/SCHEMA CHANGES
TESTS
LIVE TESTS
BACKUP STATUS
MONITORING STATUS

CRITICAL:
- auth
- security
- booking
- payment if applicable
- data
- privacy
- email
- admin

HIGH:
- search
- support
- performance
- accessibility
- globalization
- observability

MEDIUM:
- experimentation
- personalization
- PWA
- media

============================================================
PHASE 42 — NON-NEGOTIABLE RULE
============================================================

Do not:
- suppress failures
- hide warnings
- fake health
- fake delivery
- fake payment success
- fake reviews
- fake analytics
- expose secrets
- expose private user data
- claim compliance without evidence

Use:

PASS
FAIL
BLOCKED
UNKNOWN
DEGRADED
NOT_APPLICABLE

with evidence.

FINAL EXECUTION:

FIND
→ BACKUP
→ PLAN
→ IMPLEMENT
→ TEST
→ DEPLOY
→ LIVE VERIFY
→ RECHECK
→ DOCUMENT

The remaining work is complete only when the platform is reliable not just as a website, but as a secure, recoverable, observable learning + marketplace system.

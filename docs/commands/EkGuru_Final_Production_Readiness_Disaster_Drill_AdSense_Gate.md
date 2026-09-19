# EKGURU — FINAL PRODUCTION READINESS + DISASTER DRILL + ADSENSE RE-REVIEW GATE

PRODUCTION:
https://ekguru.shop/

OLD DOMAIN:
https://ekgurulearning.github.io/EkGuru/

OBJECTIVE:
Treat the current EkGuru project as a release candidate and perform the FINAL deep production-readiness gate.

This is NOT a feature brainstorm.

This command exists to answer:
“Can EkGuru safely operate in production, survive failures, protect its data/users, deliver email/bookings, remain searchable, and be legitimately ready for another AdSense review?”

Read and preserve all earlier master-command requirements.
Do NOT weaken or delete previous fixes.

============================================================
1. READ ALL PREVIOUS MASTER COMMANDS
============================================================

Before doing anything, locate and read all previous relevant master files, including:

- EkGuru_Final_Master_Reaudit_Fix_Command.md
- EkGuru_ULTRA_Production_AdSense_Traffic_Master_Command.md
- EkGuru_Header_Ultra_Fix_Improvement_Command.md
- EkGuru_ULTRA_Admin_Live_Health_Privacy_Every_Page_Command.md
- EkGuru_Read_4_Previous_Files_Implement_Everything.md
- EkGuru_ULTRA_Advanced_Learn_Tools_Build_Command.md
- EkGuru_ULTRA_360_Remaining_Production_Gaps_Command.md
- EkGuru_ULTRA_Content_Protection_Copy_Detection_Command.md

Create one cumulative final-release checklist.

Do not treat previous “DONE/GREEN/PASS” statements as proof.
Re-verify current code and live deployment.

============================================================
2. FREEZE + BASELINE
============================================================

Before final work:

- git status
- current commit
- current branch
- deployment/build identifier
- production URL
- current Doctor result
- current Privacy result
- current full test result
- current live crawl
- current health dashboard state
- current email status
- current booking status
- current URL count
- current content/tool inventory

Save:

reports/final-release-baseline.json

Do not overwrite this baseline.

============================================================
3. CRITICAL RELEASE BLOCKERS
============================================================

The release MUST be blocked if any of these are true:

- production site unavailable
- HTTPS final destination broken
- critical auth bypass
- critical secret exposure
- critical privacy leak
- booking corruption
- duplicate payment/charge where payment exists
- contact/email completely broken
- sitemap broken
- severe robots/indexing block
- critical data corruption
- backup unavailable
- restore not possible
- large-scale JS failure
- major mobile/desktop navigation broken

Do not hide or downgrade these failures.

============================================================
4. AUTHENTICATION FINAL AUDIT
============================================================

Test:

signup
login
logout
email verification
password reset
session expiration
session revocation
password change
account deletion
protected URLs
protected API routes

Security:
- secure password hashing
- secure cookies where applicable
- server-side authorization
- CSRF where needed
- brute-force protection
- rate limits
- token expiry
- no sensitive data in URLs/logs
- no account enumeration where avoidable

Test:
- invalid credentials
- expired session
- revoked session
- manipulated session
- role escalation
- direct admin URL
- direct admin API
- replayed reset link

============================================================
5. ADMIN FINAL SECURITY
============================================================

Test all roles actually implemented.

Admin actions:
- users
- tutors
- reviews
- content
- booking
- settings
- SEO
- health
- privacy

For each:
- authorization
- audit log
- confirmation for destructive actions
- server-side enforcement

Do not trust UI button hiding.

============================================================
6. PAYMENT FINAL AUDIT
============================================================

ONLY if payments are active.

Verify:
- amount
- currency
- order/booking ID
- provider signature
- webhook signature
- duplicate webhook
- delayed webhook
- replay
- success
- failure
- cancellation
- refund
- reconciliation

NEVER trust browser success flags.

Use:
idempotency
transaction/reference IDs
server verification

If no payment system is active:
mark NOT_APPLICABLE.

============================================================
7. BOOKING FINAL AUDIT
============================================================

Run end-to-end:

search tutor
→ profile
→ select slot
→ booking
→ status
→ confirmation
→ tutor/internal notification
→ final status

Test:
- stale slot
- double booking
- duplicate click
- refresh
- timezone
- DST
- midnight crossing
- cancellation
- reschedule if supported

No incorrect “confirmed” status.

============================================================
8. CONTACT + EMAIL FINAL AUDIT
============================================================

CONTACT:
submission
→ internal EkGuru email
→ visitor confirmation
→ correct Reply-To

BOOKING:
submission
→ internal
→ learner
→ tutor where applicable

Test actual controlled inboxes.

Record:
- provider response
- message ID where available
- timestamps
- delivery/acceptance state
- duplicate behavior

Do not call API accepted = delivered.

============================================================
9. GOOGLE SHEETS / APPS SCRIPT FINAL AUDIT
============================================================

Verify every configured source:

Settings
Content
Reviews
Tutors
GitHub URLs
EkGuru URLs
Full workbook

Verify:
- source accessible
- expected schema
- required columns
- row counts
- duplicate IDs
- invalid records
- cache
- stale fallback
- failure handling
- no silent []

Apps Script:
- HTTP
- response schema
- auth/permission
- timeout
- deployment
- doGet/doPost
- safe error response

Simulate:
source unavailable

Expected:
site remains stable using valid cached data where safe,
with health status showing DEGRADED.

============================================================
10. PRIVACY FINAL GATE
============================================================

Run:

node tools/privacy.js --sheets --live

Must not remain BLOCKED.

Scan:
- source
- build
- public network payloads
- client JS
- CSV data
- Apps Script output
- admin APIs

Detect:
email
phone
address
tokens
API keys
passwords
private notes
private tutor data

Classify:
PUBLIC
INTERNAL
SENSITIVE
SECRET

Only PUBLIC data may go to public pages.

============================================================
11. DOCTOR FINAL GATE
============================================================

Run Doctor.

Current historical state:
123 checks / previous problems existed.

Now require:
0 unresolved problems
0 unexpected warnings

Do not:
- mute
- skip
- downgrade
- modify test merely to pass

If check cannot run:
BLOCKED WITH EXPLANATION.

============================================================
12. DISASTER RECOVERY
============================================================

Create and verify:

LAST_KNOWN_GOOD
CURRENT
BACKUP

Back up:
- build/source state
- critical configuration
- data schemas
- production data references
- content metadata
- tutor/review datasets where appropriate

Do NOT store raw secrets insecurely.

Define:
RPO
RTO

If product-specific targets are unknown, document chosen engineering targets.

============================================================
13. RESTORE DRILL
============================================================

Perform a safe restore test away from production.

Simulate:
- damaged content data
- broken deployment
- unavailable CSV
- unavailable Apps Script
- failed configuration

Verify:
- previous build can start
- critical pages render
- data sources recover
- restore process is documented

A backup that has never been restored is NOT considered fully verified.

============================================================
14. ROLLBACK DRILL
============================================================

Simulate a bad release.

Verify:
- previous build identified
- rollback procedure works
- DNS/domain does not need risky changes
- production returns to known-good state
- health status recognizes recovery

============================================================
15. UPTIME / LIVE MONITORING
============================================================

Verify live health checks:

homepage
learn
toolbox
tool
contact
booking
tutor profile
admin health
sitemap
robots
ads.txt
Apps Script
CSV sources
email subsystem

Track:
status
latency
last success
last failure
error

States:
GREEN
YELLOW
RED
UNKNOWN

UNKNOWN is never GREEN.

============================================================
16. INCIDENT DRILL
============================================================

Simulate one safe incident:

Example:
temporarily make a non-critical dependency unavailable in a test environment.

Verify:
- incident created
- severity
- alert
- deduplication
- admin visibility
- recovery
- resolution
- timeline

Do not create production outage intentionally.

============================================================
17. ABUSE / SPAM / BOT TEST
============================================================

Test:
- contact burst
- booking burst
- review burst
- login failures
- password reset burst
- search abuse
- API abuse

Verify:
rate limit
retry behavior
friendly response
no data corruption

Do not block legitimate normal users.

============================================================
18. COPY / CONTENT PROTECTION FINAL
============================================================

Verify:

content inventory
fingerprints
internal duplicate detection
external-copy monitoring
high-similarity alerts
evidence package
copyright workflow
scraper observability

Do not break:
Googlebot
screen readers
normal copy
normal sharing

No fake legal traps.

============================================================
19. LEARN + TOOLBOX FINAL PRODUCT AUDIT
============================================================

For EVERY existing tool:

- valid input
- invalid input
- empty input
- long input
- Hindi
- English
- Unicode
- mixed text
- copy
- reset
- mobile
- desktop
- accessibility
- performance

For Learn:

- lesson
- practice
- quiz
- flashcard
- course
- learning path
- daily practice
- progress where applicable

No broken or fake tools.

============================================================
20. EVERY IMPORTANT PAGE REACHABILITY
============================================================

Build final crawl graph.

Each indexable page must have:
- meaningful internal incoming link
- valid canonical
- HTTP 200
- no blocking noindex
- no broken parent path

Report:
orphan
sitemap-only
JS-only
excessive depth

Fix important orphans.

============================================================
21. SEO FINAL GATE
============================================================

Verify:
- sitemap
- robots
- ads.txt
- canonical
- hreflang
- title
- description
- H1
- schema
- internal links
- old-domain references
- HTTPS

Old GitHub URLs are acceptable if they cleanly redirect:

old GitHub
→ 301
→ https://ekguru.shop/...
→ 200

Do not treat old Google results as a blocker by themselves.

============================================================
22. ADSENSE RE-REVIEW GATE
============================================================

Do NOT guarantee approval.

Determine whether EkGuru is READY FOR REVIEW.

Check:
- unique original content
- sufficient useful content
- clear navigation
- site fully launched
- no under-construction appearance
- no thin-content clusters
- no copied/replicated content
- legal/trust pages
- HTTPS
- ads.txt
- usable mobile/desktop UX
- no deceptive ads
- no excessive ads
- no invalid-traffic mechanisms
- no obvious policy blockers

If the exact AdSense rejection reason is available:
map every rejection item to:
FIXED / NOT_FIXED / UNKNOWN

Do not invent a reason.

============================================================
23. MOBILE FINAL GATE
============================================================

Real Chromium:

320x568
360x800
390x844
430x932
768x1024
820x1180

Check:
header
search
menus
tools
forms
tables
Hindi text
ads
footer
modals

No clipping.
No horizontal overflow.
No unreachable controls.

============================================================
24. DESKTOP FINAL GATE
============================================================

Real Chromium:

1024x768
1100x700
1200x800
1280x720
1366x768
1440x900
1536x864
1600x900
1680x900
1920x1080

Check:
header
search
CTA
language
currency
grids
cards
tables
modals
footer

No overlap.
No off-screen controls.

============================================================
25. ACCESSIBILITY FINAL GATE
============================================================

Check:
keyboard
focus
screen-reader labels
semantic headings
forms
contrast
touch targets
modal focus
Escape
reduced motion
language attributes

============================================================
26. PERFORMANCE FINAL GATE
============================================================

Measure:
TTFB
LCP
INP
CLS

Test representative:
home
Learn
tool
tutor
guide
booking
contact

Fix major regressions.

============================================================
27. SECURITY FINAL GATE
============================================================

Audit:
secrets
dependencies
CORS
CSRF
XSS
injection
open redirects
webhooks
rate limits
admin endpoints
source maps
private data

If a secret was previously exposed:
ROTATE it.

Deleting the text from source alone is not enough.

============================================================
28. SEARCH / TRAFFIC FINAL GATE
============================================================

Use real Search Console data where available.

Identify:
high impression + low CTR
positions 5–20
high-value tools
high demand + poor coverage
declining pages
country/language opportunities

Do not create pages purely to increase count.

Prioritize:
real user intent
free utility
original learning value
strong internal linking

============================================================
29. ANALYTICS FINAL GATE
============================================================

Verify one clean analytics implementation.

Track useful events:
tool_complete
lesson_complete
practice_complete
search
tutor_view
booking_start
booking_complete
contact_success

Do not collect unnecessary sensitive data.

============================================================
30. FINAL USER JOURNEY DRILL
============================================================

Test as a normal visitor:

GOOGLE-LIKE ENTRY
→ LANDING PAGE
→ FREE TOOL
→ RESULT
→ RELATED LEARNING
→ PRACTICE
→ LEARNING PATH
→ TUTOR OPTION

Second journey:

VISITOR
→ CONTACT
→ INTERNAL EMAIL
→ VISITOR CONFIRMATION
→ REPLY-TO

Third:

LEARNER
→ TUTOR
→ BOOKING
→ EMAILS
→ STATUS

Fourth:

ADMIN
→ LOGIN
→ HEALTH
→ DATA
→ CONTENT
→ TUTOR
→ BOOKING
→ SEO
→ PRIVACY

All must work.

============================================================
31. FINAL ADVERSE-CONDITION DRILL
============================================================

Safely simulate in test/staging:

CSV unavailable
Apps Script timeout
email provider failure
booking provider timeout
slow network
offline
malformed row
duplicate webhook
duplicate form submission
stale cache

Expected:
honest error
safe fallback
no data corruption
recoverability
visible health state

============================================================
32. RELEASE DECISION
============================================================

Return exactly:

RELEASE:
GO / NO-GO

ADSense REVIEW:
READY / NOT_READY / UNKNOWN

SECURITY:
PASS / FAIL / BLOCKED

PRIVACY:
PASS / FAIL / BLOCKED

DOCTOR:
PASS / FAIL / BLOCKED

DATA:
PASS / FAIL / DEGRADED

EMAIL:
PASS / FAIL / DEGRADED

BOOKING:
PASS / FAIL / N/A

PAYMENT:
PASS / FAIL / N/A

BACKUP:
PASS / FAIL

RESTORE:
PASS / FAIL

ROLLBACK:
PASS / FAIL

LIVE MONITORING:
PASS / FAIL

SEO:
PASS / FAIL

MOBILE:
PASS / FAIL

DESKTOP:
PASS / FAIL

ACCESSIBILITY:
PASS / FAIL

PERFORMANCE:
PASS / FAIL

CONTENT:
PASS / FAIL / DEGRADED

COPY PROTECTION:
PASS / DEGRADED

============================================================
33. FINAL RELEASE REPORT
============================================================

Include:

- baseline
- all critical findings
- root causes
- exact fixes
- exact files changed
- migrations
- tests
- live verification
- screenshots for UI defects
- backup evidence
- restore evidence
- rollback evidence
- email E2E evidence
- booking E2E evidence
- privacy evidence
- Doctor evidence
- current health state
- remaining blockers

For every remaining issue:
PRIORITY
RISK
EXACT FIX
OWNER/WORKSTREAM
NEXT ACTION

============================================================
34. FINAL NON-NEGOTIABLE RULE
============================================================

Do NOT hide failures.
Do NOT mutate tests to manufacture green.
Do NOT claim approval.
Do NOT claim traffic guarantees.
Do NOT claim all URLs indexed.
Do NOT claim delivery when only API acceptance is known.
Do NOT claim payment success without provider verification.
Do NOT expose secrets/private data.

The final goal is:

SECURE
+
RECOVERABLE
+
MONITORED
+
SEARCHABLE
+
ORIGINAL
+
USEFUL
+
ACCESSIBLE
+
FAST
+
RELIABLE

EkGuru must be capable of operating as a real production learning + tutor marketplace platform, not merely passing a checklist.

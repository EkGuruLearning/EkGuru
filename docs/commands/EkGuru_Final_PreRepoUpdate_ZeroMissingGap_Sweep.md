# EKGURU — FINAL PRE-REPO-UPDATE GAP SWEEP + ZERO-MISSING-AREA AUDIT

PRODUCTION:
https://ekguru.shop/

OLD DOMAIN:
https://ekgurulearning.github.io/EkGuru/

OBJECTIVE:
Before the next repository update, perform one final "nothing left behind" audit across the ENTIRE EkGuru platform.

This is NOT another narrow feature command.

Read all previous master commands first, merge them, then identify:
1. anything already implemented but not verified,
2. anything specified but not implemented,
3. anything partially implemented,
4. anything that works locally but not live,
5. anything that works but is fragile,
6. any production risk that previous commands did not explicitly cover.

Do not start by assuming everything is complete.

============================================================
1. READ ALL PREVIOUS MASTER COMMANDS
============================================================

Locate and fully read all available previous command files, including:

- EkGuru_Final_Master_Reaudit_Fix_Command.md
- EkGuru_ULTRA_Production_AdSense_Traffic_Master_Command.md
- EkGuru_Header_Ultra_Fix_Improvement_Command.md
- EkGuru_ULTRA_Admin_Live_Health_Privacy_Every_Page_Command.md
- EkGuru_Read_4_Previous_Files_Implement_Everything.md
- EkGuru_ULTRA_Advanced_Learn_Tools_Build_Command.md
- EkGuru_ULTRA_360_Remaining_Production_Gaps_Command.md
- EkGuru_ULTRA_Content_Protection_Copy_Detection_Command.md
- EkGuru_Final_Production_Readiness_Disaster_Drill_AdSense_Gate.md
- EkGuru_ULTRA_Critical_Email_Booking_Routing_Failover_Command.md
- EkGuru_ULTRA_Modern_Animation_Motion_System_Command.md

Create:

reports/final-gap-sweep.json

For every requirement:
source
category
requirement
status
evidence
live_verified
remaining_gap
risk
priority
next_action

============================================================
2. DO NOT TRUST PREVIOUS "DONE"
============================================================

Every previous DONE/PASS/GREEN result must be reclassified as:

LIVE_VERIFIED
CODE_ONLY
PARTIAL
BROKEN
UNKNOWN
NOT_APPLICABLE

If a previous result has no current evidence:
UNKNOWN

Do not call UNKNOWN PASS.

============================================================
3. COMPLETE PLATFORM MAP
============================================================

Map every subsystem:

PUBLIC WEBSITE
LEARN
TOOLS
TUTORS
BOOKING
CONTACT
EMAIL
AUTH
USERS
ADMIN
HEALTH
SHEETS
APPS SCRIPT
SEO
CONTENT
ADSENSE
ANALYTICS
SEARCH
INTERNATIONAL
SECURITY
PRIVACY
PAYMENTS (if active)
MEDIA
PWA/OFFLINE
COPY PROTECTION
MONITORING
BACKUP
DEPLOYMENT
SUPPORT

Find any subsystem that exists in code but has:
- no tests
- no health check
- no fallback
- no admin visibility
- no error state
- no recovery procedure

============================================================
4. ENVIRONMENT / CONFIGURATION AUDIT
============================================================

Audit:
development
test
production

Check:
- env variable names
- missing env vars
- wrong production values
- duplicated config
- stale endpoints
- hardcoded URLs
- hardcoded provider settings
- secrets
- staging values in production
- debug flags
- verbose logging
- development-only feature flags

Create:
reports/environment-audit.json

No secrets in report.

============================================================
5. CI/CD FINAL AUDIT
============================================================

Check:
- build
- test
- lint/typecheck where present
- security checks
- privacy
- Doctor
- sitemap
- browser tests
- deploy
- post-deploy health checks

Verify that CI actually FAILS on critical regressions.

Test failure gates deliberately in a safe branch/test environment.

Do not weaken CI just to get green.

============================================================
6. DEPLOYMENT ARTIFACT AUDIT
============================================================

Verify production artifact contains exactly what is expected.

Look for:
- debug files
- test pages
- temporary screenshots
- old bundles
- unused data
- source maps with sensitive information
- stale manifest
- stale robots
- stale sitemap
- old domain references
- duplicate assets
- oversized assets

Do not delete source maps blindly if they are intentionally public/needed; assess security implications first.

============================================================
7. CACHE / VERSIONING / STALE BUILD
============================================================

Test:
- hard refresh
- new deployment
- browser cache
- CDN cache
- service worker cache
- stale HTML
- stale JS
- stale CSS

Ensure a new deployment becomes visible reliably.

No user should receive an incompatible combination of:
old HTML + new JS
or
new HTML + old JS

============================================================
8. ERROR TRACKING QUALITY
============================================================

Verify that errors include:
- event
- severity
- timestamp
- component
- safe contextual ID

Do not log:
passwords
tokens
full private messages
unnecessary PII

Ensure errors can be traced back to:
page
request
booking/contact ID
provider attempt where appropriate

============================================================
9. FEATURE FLAG CLEANUP
============================================================

Find:
- dead flags
- permanent temporary flags
- contradictory flags
- production flags with no owner

Every production feature flag:
- documented
- default defined
- owner identified
- rollback path

Remove obsolete flags.

============================================================
10. CRON / SCHEDULED WORK
============================================================

Find all scheduled jobs:
- health
- email retry
- content sync
- sitemap generation
- analytics
- backups
- monitoring
- copy detection

Check:
- schedule
- timezone
- duplicate execution
- locking
- retry
- missed execution
- job history

Prevent concurrent duplicate workers.

============================================================
11. QUEUES / ASYNC WORKERS
============================================================

If any background worker exists:
- retry
- dead-letter/failure state
- duplicate prevention
- ordering where necessary
- idempotency
- visibility in admin

No job should disappear silently.

============================================================
12. DATA RETENTION
============================================================

For:
contact
booking
email events
audit logs
health logs
security logs

Define:
purpose
retention period
deletion behavior
anonymization where applicable

Do not retain sensitive data indefinitely without purpose.

============================================================
13. TIME / CLOCK CONSISTENCY
============================================================

Audit all timestamps.

Store in one canonical format.

Display localized time where appropriate.

Test:
DST
midnight
year rollover
timezone conversion
server timezone differences
browser timezone differences

============================================================
14. MONEY / CURRENCY DISPLAY
============================================================

If prices exist:
- source amount
- currency
- formatting
- rounding
- locale

Never convert/display a price using stale or incorrect currency metadata.

Do not claim live exchange rates unless actually live.

============================================================
15. USER EXPERIENCE EDGE CASES
============================================================

Test:
- first visit
- returning visitor
- slow connection
- offline
- very small screen
- large text
- keyboard-only
- screen reader
- browser zoom 200%
- long names
- long email
- long tutor name
- long Hindi text
- empty data
- extremely long message
- unusual Unicode

No critical feature should fail.

============================================================
16. BROWSER COMPATIBILITY
============================================================

At least test current:
- Chrome
- Safari
- Firefox
- mobile Safari
- mobile Chrome

Where tooling permits.

Focus on:
- header
- menu
- forms
- booking
- tools
- audio
- admin
- modals

============================================================
17. SEO EDGE CASES
============================================================

Check:
- trailing slash
- .html
- uppercase/lowercase
- query parameters
- fragments
- duplicate paths
- pagination
- filters
- search pages
- print pages
- preview URLs
- staging URLs

Choose one canonical URL style.

Do not accidentally index:
- admin
- preview
- test
- internal search
- transient states

============================================================
18. SCHEMA EDGE CASES
============================================================

Check JSON-LD:
- valid JSON
- matching visible content
- correct production URLs
- no deprecated/wrong schema
- no fake ratings/reviews
- no impossible dates
- no invalid price
- no duplicate conflicting schema

============================================================
19. MEDIA RIGHTS / LICENSE AUDIT
============================================================

For:
images
icons
fonts
audio
video
illustrations

Record where appropriate:
source
license
attribution requirement
ownership status

Do not publish assets with unknown rights.

============================================================
20. CONTENT QUALITY — FINAL SELF-DUPLICATION
============================================================

Find:
- same page intent under different URLs
- identical intros
- repeated FAQs
- repeated examples
- templated country pages
- templated language pages
- low-value auto-generated pages

Classify:
legitimate reusable component
vs
content duplication problem

Fix the latter.

============================================================
21. INTERNAL LINK QUALITY
============================================================

Check links for:
- wrong destination
- irrelevant destination
- outdated anchor
- excessive repetition
- circular linking
- dead hub
- orphan
- excessive click depth

Important pages should be discoverable within a reasonable number of clicks.

============================================================
22. EXTERNAL LINK SAFETY
============================================================

Audit external links:
- destination still exists
- HTTPS where appropriate
- no suspicious redirects
- no broken links
- no malicious-looking destination
- rel attributes appropriate where needed

============================================================
23. SEARCH QUALITY
============================================================

Use real test queries:

Hindi
Roman Hindi
English
mixed Hindi/English
typos
partial words
phrases
tutor names
topic names
tool names

Verify:
- relevant results
- no-result fallback
- ranking quality
- fast response
- no private results leak

============================================================
24. SEO CRAWLER VS USER PARITY
============================================================

Verify that crawlers and users receive the same intended public content.

No:
- cloaking
- user-agent-specific SEO content
- hidden keyword blocks

Do not accidentally create different canonical/sitemap data by user agent.

============================================================
25. AD / MONETIZATION SAFETY
============================================================

If ads are active:
- ads do not overlap controls
- ads are distinguishable
- no accidental-click design
- no excessive density
- no ads on empty/private utility states
- ad scripts do not break page performance

If ads are not active yet:
ensure the system can be enabled safely later without layout breakage.

============================================================
26. CONSENT / COOKIE BEHAVIOR
============================================================

Where applicable:
- consent state
- analytics behavior
- advertising behavior
- preferences
- withdrawal
- persistence

Do not load optional tracking before the applicable consent state.

Do not claim legal compliance without evidence.

============================================================
27. SUPPORT / HUMAN OPERATIONS
============================================================

Test the operational path:

visitor issue
→ contact
→ record
→ assignment
→ response
→ resolution

Admin must be able to find:
- booking
- contact
- tutor
- student
- email event

without searching multiple disconnected systems.

============================================================
28. ADMIN USABILITY
============================================================

Test admin with:
- 1 record
- 100 records
- 1000 records if realistic

Check:
- pagination
- search
- filters
- loading
- empty
- error
- slow network

Do not load huge datasets into browser unnecessarily.

============================================================
29. ACCESSIBILITY FINAL SWEEP
============================================================

Check:
- keyboard
- focus
- heading hierarchy
- link purpose
- labels
- alt text
- errors
- modal focus
- reduced motion
- zoom 200%
- text resizing
- contrast

============================================================
30. ANIMATION FINAL SWEEP
============================================================

Use the existing motion command as the baseline.

Find remaining:
- inconsistent timing
- excessive animation
- animation-induced layout shift
- menu race condition
- modal race
- scroll lock bug
- reduced-motion failure
- motion causing CPU spikes

============================================================
31. COPY PROTECTION FINAL SWEEP
============================================================

Verify:
- fingerprints
- version history
- similarity scans
- internal duplicate detection
- copy candidate dashboard
- evidence package
- alerts
- scraper observability

Do not break:
Google
accessibility
normal copy
normal sharing

============================================================
32. BACKUP FINAL SWEEP
============================================================

Verify:
- backups actually exist
- latest timestamp
- backup integrity
- restore procedure
- restore test result
- rollback build

============================================================
33. MONITORING FINAL SWEEP
============================================================

Every critical subsystem needs:
- health check
- timestamp
- latency
- last success
- last failure
- degraded state
- alert path

No critical system should have:
NO MONITOR
NO FALLBACK
NO OWNER
without an explicit documented reason.

============================================================
34. OWNER / RUNBOOK SYSTEM
============================================================

For every critical subsystem define:

system
purpose
owner
dependency
health check
common failures
recovery steps
rollback
escalation

Examples:
Email
Booking
Sheets
Apps Script
Search
Auth
Payments
Deployment
SEO
Health
Admin

This becomes the production runbook.

============================================================
35. COST / RESOURCE CONTROL
============================================================

Audit:
- API calls
- email usage
- Google Sheets calls
- Apps Script calls
- AI/tool usage
- storage
- bandwidth
- CDN
- monitoring

Find:
- accidental loops
- repeated fetches
- duplicate emails
- wasteful polling
- unbounded logs
- excessive browser computation

Optimize without reducing reliability.

============================================================
36. LOAD / STRESS TEST
============================================================

Safely test realistic concurrency for:
- homepage
- search
- tools
- contact
- booking
- health

Measure:
latency
error rate
resource usage

Do not stress production destructively.

Use staging/controlled environment for high-load tests.

============================================================
37. DEPENDENCY FAILURE MAP
============================================================

Create:

EkGuru page
→ dependency
→ fallback
→ degraded behavior

Examples:

Tutor page
→ Tutors CSV
→ cache
→ stale data

Booking
→ booking backend
→ persistent record
→ email outbox

Contact
→ form backend
→ persistent record
→ email fallback

Health
→ provider checks
→ cached last state

No critical flow should fail catastrophically because of one non-critical dependency.

============================================================
38. RELEASE CANDIDATE CHECKSUM
============================================================

Before final repo update:
- build ID
- git commit
- generated artifact checksum
- sitemap count
- content count
- tool count
- test count

Save:
reports/release-candidate.json

============================================================
39. FINAL "NOTHING LEFT" MATRIX
============================================================

Create a final table with:

CATEGORY
REQUIREMENT
STATUS
EVIDENCE
LIVE_VERIFIED
RISK
FIX_REQUIRED
PRIORITY

Categories:
SEO
ADSENSE
CONTENT
LEARN
TOOLS
HEADER
ANIMATION
MOBILE
DESKTOP
ADMIN
HEALTH
PRIVACY
SHEETS
APPS_SCRIPT
EMAIL
BOOKING
PAYMENT
AUTH
SECURITY
BACKUP
RECOVERY
MONITORING
SEARCH
INTERNATIONAL
ACCESSIBILITY
PERFORMANCE
COPY_PROTECTION
ANALYTICS
SUPPORT
CI/CD
DEPLOYMENT
LEGAL
DATA
COST

============================================================
40. DO NOT INVENT MISSING SYSTEMS
============================================================

If a subsystem is not used by the current EkGuru product:
mark:

NOT_APPLICABLE

Do not add payment/auth/PWA/etc. simply because a checklist contains them.

But if code suggests the subsystem exists, audit it fully.

============================================================
41. FINAL ACTION RULE
============================================================

For every finding:

CRITICAL:
fix now

HIGH:
fix now unless blocked by external dependency

MEDIUM:
fix where safe before final repo update

LOW:
record as backlog

Do not expand scope into unrelated redesigns.

============================================================
42. FINAL VERIFICATION
============================================================

Run:
build
full tests
Doctor
Privacy
live crawl
SEO checks
browser tests
mobile tests
desktop tests
email E2E
booking E2E
data tests
security checks
accessibility checks
performance checks

Then deploy to a controlled/live environment as appropriate.

Re-run:
live smoke
health
critical user journeys

============================================================
43. FINAL REPORT
============================================================

Return:

TOTAL REQUIREMENTS REVIEWED
LIVE VERIFIED
CODE VERIFIED ONLY
PARTIAL
BROKEN
UNKNOWN
NOT_APPLICABLE

CRITICAL REMAINING:
list

HIGH:
list

MEDIUM:
list

LOW:
list

EXACT FILES CHANGED
EXACT TESTS RUN
LIVE URLS VERIFIED
BACKUP/RESTORE STATUS
RELEASE CANDIDATE ID

============================================================
44. FINAL RULE
============================================================

This is a GAP SWEEP, not permission to keep adding features forever.

When all realistic production gaps are:
- implemented
- tested
- live-verified
- documented

STOP.

Do not keep inventing requirements just to say more work remains.

The objective is to reach a defensible release candidate with:
high reliability
high security
high UX quality
high content quality
high search readiness
high operational visibility

END.

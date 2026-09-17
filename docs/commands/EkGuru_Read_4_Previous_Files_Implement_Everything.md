# EKGURU — READ THE 4 PREVIOUS MASTER COMMAND FILES FIRST, THEN IMPLEMENT EVERYTHING

PRODUCTION:
https://ekguru.shop/

OLD DOMAIN:
https://ekgurulearning.github.io/EkGuru/

OBJECTIVE:
You must first read and understand the four previous master-command files listed below, reconcile their requirements, then implement EVERYTHING that is still pending in the actual EkGuru codebase.

DO NOT choose only one workstream.
DO NOT skip previous requirements.
DO NOT replace the previous commands with a smaller summary.
Treat the four files together as one cumulative specification.

============================================================
1. READ THESE 4 PREVIOUS COMMAND FILES FIRST
============================================================

Read the complete contents of these files before modifying code:

1.
EkGuru_Final_Master_Reaudit_Fix_Command.md

2.
EkGuru_ULTRA_Production_AdSense_Traffic_Master_Command.md

3.
EkGuru_Header_Ultra_Fix_Improvement_Command.md

4.
EkGuru_ULTRA_Admin_Live_Health_Privacy_Every_Page_Command.md

If the files are available in the workspace/library/history under a different path/name, locate the exact corresponding files and read them fully.

IMPORTANT:
Do not begin implementation until all four are read.

Create an internal merged checklist from all four files.

Do not silently discard duplicate requirements:
- consolidate duplicates
- preserve the strongest version of the requirement
- preserve concrete test requirements
- preserve all critical fixes

============================================================
2. BUILD A CUMULATIVE REQUIREMENTS MATRIX
============================================================

Create:

reports/master-requirements.json

Fields:

id
source_file
requirement
category
priority
current_status
evidence
files_affected
implementation_plan
test
result

Categories:

HEADER
ADMIN
PRIVACY
HEALTH
SHEETS
APPS_SCRIPT
EMAIL
BOOKING
SEO
INDEXING
SITEMAP
ROBOTS
ADS.TXT
CONTENT
ADSENSE
TRAFFIC
FREE_TOOLS
INTERNATIONAL
MOBILE
TABLET
DESKTOP
ACCESSIBILITY
PERFORMANCE
SECURITY
ANALYTICS
DEPLOYMENT
REGRESSION

============================================================
3. DO NOT TRUST OLD "DONE" CLAIMS BLINDLY
============================================================

For each requirement previously marked:
DONE
FIXED
GREEN
PASS

re-verify it in the current codebase and LIVE deployment.

Previous reports are evidence, not proof of current state.

Especially re-check:
- header geometry
- old GitHub redirects
- HTTPS final destination
- Sheets data layer
- contact email
- booking email
- privacy scan
- Doctor
- live health
- all page reachability
- ads.txt
- sitemap
- canonical
- hreflang
- mobile
- desktop
- content quality

============================================================
4. BACKUP / SNAPSHOT FIRST
============================================================

Before modifying production data/code:

- git status
- record current branch
- record current commit
- snapshot configuration
- snapshot critical CSV/schema references
- record current test baseline

Do not overwrite valid data.
Do not delete production records without a verified reason.

============================================================
5. RUN THE EXISTING TEST BASELINE
============================================================

Run all existing project checks.

At minimum discover and run relevant:

Doctor
Privacy
full test suite
build
lint/typecheck if present
sitemap checks
SEO checks
browser/layout checks
email tests
data-source tests

Specifically run:

node tools/privacy.js --sheets --live

Run Doctor.

Record BEFORE results.

Do not mute failures.

============================================================
6. ADMIN + LIVE HEALTH
============================================================

Implement every admin requirement from:

EkGuru_ULTRA_Admin_Live_Health_Privacy_Every_Page_Command.md

This includes:

- privacy scan unblocked
- public/internal/sensitive/secret data classification
- Sheets privacy
- Apps Script health
- live health dashboard
- live refresh
- health history
- incident deduplication
- alerting
- data-source status
- content admin
- tutor admin
- review moderation
- booking operations
- email operations
- SEO control center
- privacy center
- RBAC
- admin audit log
- backups/recovery
- admin performance
- every page error states

Final requirement:
Do not call blocked/unknown health GREEN.

============================================================
7. HEADER
============================================================

Implement every requirement from:

EkGuru_Header_Ultra_Fix_Improvement_Command.md

Required header:

YES:
Logo
Search
Find Tutors
How it works
Book a trial
Language
Currency

REMOVE FROM HEADER:
Learn
Become a Tutor

REMOVE/REVIEW:
Coming Soon

Fix:
- screenshot collision
- search/nav overlap
- off-screen controls
- breakpoint issues
- mobile layout
- sticky behavior
- hamburger behavior
- dropdown positioning
- z-index
- touch targets
- keyboard focus

Real-browser geometry is mandatory.

Test:
1024
1100
1200
1280
1366
1440
1536
1600
1680
1920

And mobile:
320
360
390
430
768

============================================================
8. GOOGLE SHEETS + APPS SCRIPT
============================================================

Use the production source endpoints from the previous commands exactly.

Before changing:

- fetch
- inspect headers
- row count
- checksum
- schema
- mapping
- consumer

Check:
Settings
Content
Reviews
Tutors
GitHub URLs
EkGuru URLs
Full workbook

Implement:
- centralized config
- schema validation
- retries
- timeout
- cache
- stale fallback
- safe failures
- data integrity checks
- duplicate IDs
- malformed rows
- URL validation
- email validation
- relational integrity

Apps Script:
- endpoint health
- response schema
- deployment
- error behavior
- latency
- permissions
- doGet/doPost
- contract tests

Never silently turn a failed source into [].

============================================================
9. CONTACT + BOOKING EMAIL
============================================================

Implement everything from the previous email specification.

CONTACT:
internal notification
+
visitor confirmation
+
Reply-To = visitor email

BOOKING:
internal
+
learner
+
tutor where applicable

Implement:
- explicit status
- idempotency
- retry
- safe fallback
- duplicate protection
- timezone correctness
- delivery state
- provider diagnostics
- mobile/desktop forms
- actual mailbox E2E tests

Do not put visitor email into FROM.
Use verified EkGuru sender identity.

Do not claim DELIVERED when provider only says ACCEPTED.

============================================================
10. SEO / MIGRATION
============================================================

Implement the cumulative SEO requirements.

Old GitHub URLs are NOT automatically a bug.

Correct migration:

old GitHub
→ 301
→ https://ekguru.shop/...
→ 200

Wrong:

old GitHub
→ http://ekguru.shop/...
→ 200

Verify:
- HTTP/HTTPS
- www/non-www
- canonical
- hreflang
- sitemap
- internal links
- JSON-LD
- OG
- manifest
- breadcrumbs
- images

Production identity:
https://ekguru.shop/

Preserve useful old redirects.

============================================================
11. FULL URL INVENTORY
============================================================

Rebuild the current public URL inventory.

Do not assume 542 forever.

Record:

URL
page type
language
country
status
final URL
canonical
robots
indexable
title
description
H1
content length
quality
originality
inlinks
outlinks
orphan
schema
hreflang
mobile
desktop
performance
issue
action

Actions:
KEEP
IMPROVE
MERGE
NOINDEX
REMOVE

============================================================
12. EVERY IMPORTANT PAGE MUST BE REACHABLE
============================================================

Build an HTML-link reachability graph.

Every indexable page should be reachable from:
- homepage
- hub
- topic
- language
- relevant internal content

Sitemap-only pages are not considered fully reachable.

Find:
- orphan
- sitemap-only
- JS-only
- login-gated
- excessive-depth pages

Fix meaningful orphan pages.

============================================================
13. CONTENT + ADSENSE
============================================================

Implement all content-quality requirements from the previous master commands.

Do NOT:
- AI-detector evade
- fake authorship
- fake expert experience
- fake reviews
- copied content
- synonym-spin
- keyword stuffing
- doorway pages
- mass low-value country pages
- fake generators

Do:
- original explanations
- original examples
- useful exercises
- practical tools
- accurate facts
- editorial review
- clear learner purpose
- useful internal links
- strong trust pages

Classify pages:
A strong
B improve
C merge/noindex/remove

Prioritize high-value weak pages.

============================================================
14. FREE TRAFFIC VALUE
============================================================

Preserve and expand real free value.

Evaluate and implement where justified:

Hindi transliteration
Hindi typing
Name writing
Pronunciation
Dictionary/meaning
Sentence builder
Verb conjugator
Grammar practice
Vocabulary practice
Flashcards
Quizzes
Reading
Listening
Speaking
Placement test
Travel phrases
Numbers
Dates
Time
Practical conversations
Learning paths
Daily practice

No fake/broken tools.

Separate dynamic practice from indexable content.

============================================================
15. GLOBAL EXPANSION
============================================================

Use real demand evidence before creating localized pages.

For each proposed country/language:
- demand evidence
- intent
- native-quality copy
- unique value
- local context
- canonical
- hreflang
- internal links
- mobile/desktop QA

Do not make 195 copy/paste country pages.

Build only where genuine value exists.

============================================================
16. MOBILE / TABLET / DESKTOP
============================================================

Use REAL Chromium, not jsdom alone.

Mobile:
320x568
360x800
390x844
430x932
768x1024
820x1180

Desktop:
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

Find:
- horizontal overflow
- clipping
- overlap
- off-screen elements
- header collision
- search collision
- modal issues
- menu issues
- form issues
- table overflow
- long Hindi text problems
- fixed overlays
- ads covering controls
- touch target issues

Take screenshots of genuine failures.

============================================================
17. INTERACTION / JS / FORMS
============================================================

Test:
buttons
links
dropdowns
modals
search
language
currency
booking
contact
admin actions

Test:
Escape
outside click
Back
Forward
refresh
slow network
provider error
duplicate submit

No silent failure.

Console:
no unexpected uncaught exceptions
no unhandled rejections
no broken assets
no mixed content
no CORS failures where not intended

============================================================
18. PERFORMANCE
============================================================

Measure:
TTFB
LCP
INP
CLS

Audit:
JS
CSS
images
fonts
third parties
analytics
ads

Avoid adding heavy admin/public dependencies unnecessarily.

============================================================
19. ACCESSIBILITY
============================================================

Verify:
- keyboard
- focus
- labels
- semantic headings
- link names
- contrast
- touch targets
- modal focus
- Escape
- language attributes
- reduced motion where appropriate

============================================================
20. SECURITY / PRIVACY
============================================================

Audit:
- secrets
- API keys
- source maps
- private sheet data
- admin endpoints
- RBAC
- CORS
- CSRF where applicable
- XSS
- injection
- open redirects
- webhook verification
- form abuse
- rate limits

No private data in public client payloads.

============================================================
21. LEGAL / TRUST
============================================================

Verify:
About
Contact
Privacy
Terms
Disclaimer

All:
- live
- reachable
- HTTPS
- mobile
- desktop
- internally linked

No placeholder/unfinished status.

============================================================
22. SITEMAP / ROBOTS / ADS.TXT
============================================================

Verify LIVE:

https://ekguru.shop/sitemap-index.xml
https://ekguru.shop/robots.txt
https://ekguru.shop/ads.txt

Sitemap:
only canonical HTTPS indexable URLs

Robots:
does not block important content

Ads.txt exact:

google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0

============================================================
23. ANALYTICS / SEARCH CONSOLE
============================================================

Ensure one clean implementation.

Track where appropriate:
- organic landing
- query
- CTR
- position
- country
- device
- tool usage
- tutor clicks
- booking
- contact

Prepare Search Console-ready sitemap and URL inspection workflow.

============================================================
24. BUILD / DEPLOYMENT
============================================================

After changes:

1. build
2. tests
3. deploy
4. LIVE smoke
5. live crawl
6. browser audit
7. email E2E
8. privacy scan
9. Doctor
10. re-run all regression

No localhost-only success claims.

============================================================
25. DO NOT STOP AFTER FINDING ISSUES
============================================================

For every failure:

FIND
→ ROOT CAUSE
→ FIX
→ TEST
→ DEPLOY
→ LIVE VERIFY
→ RECHECK

Do not merely create a report.

Implement fixes in the codebase wherever safe.

============================================================
26. FINAL QUALITY GATE
============================================================

Required final target:

Privacy:
PASS
0 blocked
0 unexplained failures

Doctor:
0 problems
0 unexpected warnings

Data:
all required sources valid or safely degraded

Email:
contact internal PASS
contact visitor PASS
Reply-To PASS
booking learner PASS
booking internal PASS
booking tutor PASS/N/A

SEO:
sitemap PASS
robots PASS
ads.txt PASS
canonical PASS
hreflang PASS/appropriate
no critical orphan pages

Header:
no Learn
no Become a Tutor
no unexplained Coming Soon
no collision
no clipping
no off-screen controls

UX:
mobile PASS
tablet PASS
desktop PASS

Security:
no critical secret/PII exposure
RBAC PASS
audit logging PASS

Content:
no critical thin/duplicate clusters
important pages reachable
strong free value

============================================================
27. FINAL REPORT
============================================================

Return a consolidated report, not separate fragmented reports.

A. BASELINE
B. WHAT WAS ALREADY FIXED
C. WHAT WAS STILL BROKEN
D. WHAT WAS CHANGED
E. LIVE VERIFICATION
F. REGRESSION RESULTS
G. REMAINING BLOCKERS

Exact metrics:

URLs
indexable
excluded
orphans
200
3xx
4xx
5xx

SEO issues
content issues
mobile issues
desktop issues
JS errors

Sheets:
row counts
schema mismatches
data integrity

Email:
contact internal
contact visitor
Reply-To
booking internal
booking learner
booking tutor
delivery evidence
duplicate protection

Privacy:
blocked before
blocked after

Doctor:
problems before
problems after

Health:
GREEN
YELLOW
RED
GRAY

Admin:
RBAC
audit
health
content
tutors
reviews
bookings
SEO
privacy

FREE VALUE:
tools
practice systems
learning paths
localized experiences

============================================================
28. ABSOLUTE RULE
============================================================

Do NOT say:
"Everything is perfect"
"AdSense guaranteed"
"Traffic guaranteed"
"All pages indexed"

unless directly verified.

Use:
PASS
FAIL
BLOCKED
UNKNOWN
DEGRADED

with evidence.

The final deliverable is a real production implementation, not a plan.
Read all four previous files first.
Merge them.
Implement everything.
Re-test everything.
Deploy.
Verify live.
Then report.

# EKGURU — POST-PUSH DEEP RESEARCH + LIVE/REPO FORENSIC AUDIT + FIX EVERYTHING

PRODUCTION:
https://ekguru.shop/

REPOSITORY:
https://github.com/ekgurulearning/EkGuru.git
default branch: main

OBJECTIVE:
This is a fresh post-push forensic audit.

Do not trust previous reports saying "fixed", "green", "542/542", "3037 passed", etc.
Inspect CURRENT repository state and CURRENT LIVE deployment independently.

The goal is to detect and fix:
- technical bugs
- security problems
- privacy problems
- SEO mistakes
- AdSense blockers
- email/booking failures
- admin failures
- data integrity failures
- performance problems
- responsive/UI problems
- animation problems
- content-quality problems
- internationalization problems
- hidden edge cases
- deployment drift
- stale production build
- anything else that can materially harm users, search visibility, trust, or operations

IMPORTANT:
Do not stop at a report.
For controllable issues:
FIND → ROOT CAUSE → FIX → TEST → DEPLOY → LIVE VERIFY → RECHECK

============================================================
1. CURRENT REPOSITORY FORENSIC
============================================================

Record:
- HEAD SHA
- latest commit
- branch
- working tree if accessible
- total tracked files
- file type counts
- HTML count
- JS count
- CSS count
- image/media count
- tool count
- page/route count

Search the entire repo for:
TODO
FIXME
HACK
TEMP
DEBUG
DEVELOPMENT
COMING SOON
UNDER CONSTRUCTION
PLACEHOLDER
SECOND-KEY-HERE
YOUR-API
EXAMPLE
CHANGE-ME
REPLACE-ME
localhost
127.0.0.1
0.0.0.0
github.io
/EkGuru/
http://ekguru.shop
www.ekguru.shop

Classify every match:
REAL PROBLEM
DOCUMENTATION
TEST DATA
SAFE
UNKNOWN

============================================================
2. LIVE DEPLOYMENT FORENSICS
============================================================

Use multiple methods to test production, not one fetch method.

Test:
https://ekguru.shop/
https://ekguru.shop/robots.txt
https://ekguru.shop/sitemap-index.xml
https://ekguru.shop/ads.txt
https://ekguru.shop/contact/
https://ekguru.shop/privacy/
https://ekguru.shop/terms/
https://ekguru.shop/disclaimer/
https://ekguru.shop/toolbox/
https://ekguru.shop/daily-hindi/

Also test:
http://ekguru.shop/
https://www.ekguru.shop/
http://www.ekguru.shop/

Measure:
DNS resolution
TCP connect
TLS handshake
TTFB
download time
total time
response headers
content length
compression
cache headers
redirect count
final URL

If one environment cannot resolve/fetch the domain:
do NOT call it broken.
Use:
- real browser
- external/public fetch
- GitHub Pages
- Cloudflare checks
- another network/environment where available

Report the exact limitation.

============================================================
3. DEPLOYMENT DRIFT
============================================================

Compare:
CURRENT GITHUB MAIN
vs
LIVE PRODUCTION

Determine:
- same build?
- missing files?
- old HTML?
- old JS/CSS?
- old header?
- old "coming soon"?
- stale sitemap?
- stale ads.txt?
- stale manifest?
- stale config?

Use deployment/build fingerprints where possible.

If live is stale:
fix deployment, not source code unnecessarily.

============================================================
4. CRITICAL ISSUE FOUND IN CURRENT REPO — APPS SCRIPT AUTH
============================================================

Current repository inspection shows:

js/site-config.js
has an Apps Script URL but:
token: ""

Current tools/apps-script-mailer.gs:
- reads MAILER_SHARED_TOKEN from Script Properties
- only checks the token IF a server-side token is configured
- ALLOW_STRANGERS = true
- any recipient is accepted when strangers are allowed
- the Apps Script endpoint is therefore not strongly authenticated if MAILER_SHARED_TOKEN is empty

This MUST be fixed.

Do NOT solve by committing a secret token to the repository.

Preferred architecture:
- public frontend submits to a controlled backend/edge relay
- edge relay authenticates/validates the request with a server-side secret
- edge relay calls Apps Script
- Apps Script accepts only authenticated relay requests
- recipient is validated against a safe routing policy
- rate limits apply at the edge and script

If a client-shared token must remain because of the static architecture:
document that it is NOT a secret, reduce the relay's abuse surface, enforce signed/limited intent where feasible, and do not pretend client-visible tokens are secure.

============================================================
5. CRITICAL EMAIL ROUTING AUDIT
============================================================

Current repo inspection shows tutor files can have:

email: ""

and formKey: ""

For example, current Sushila record has no real tutor email.

Therefore:
- do not claim Tutor email delivery is working
- keep TUTOR_EMAIL_UNAVAILABLE honest
- route safely to EkGuru internal inbox
- preserve booking record
- preserve exact tutor ID
- preserve student requirement
- show delivery state in admin

For any tutor that later has a verified address:
student selects Tutor A
→ Tutor A email only
→ student email
→ EkGuru internal
→ fallback if needed

Test at least two different tutors.

============================================================
6. CRITICAL EMAIL PROVIDER AUDIT
============================================================

Current repo contains:
- Web3Forms
- StaticForms
- FormSubmit
- EmailJS configuration
- Apps Script relay

Current EmailJS fields are empty:
serviceId
templateId
publicKey

Therefore EmailJS is not actually active.

Do not count an unconfigured provider as a working fallback.

Build a live provider matrix:
provider
configured
healthy
message types
primary/fallback position
last success
last failure
quota
recipient capability
CC capability
delivery status support

Only list configured providers as active.

============================================================
7. APPS SCRIPT REAL END-TO-END
============================================================

Test:
GET /exec
POST contact
POST booking student
POST booking tutor if available
POST EkGuru internal

Verify:
- token
- recipient
- response
- email
- fallback
- quota handling
- retry
- duplicate prevention

Use controlled test inboxes.

Do not claim:
API 200 = email delivered.

============================================================
8. DATA / GOOGLE SHEETS
============================================================

Verify live:
Settings CSV
Content CSV
Reviews CSV
Tutors CSV
GitHub URL CSV
EkGuru URL CSV
Full workbook

For each:
- status
- headers
- row count
- duplicate IDs
- malformed rows
- stale rows
- URLs
- emails
- privacy classification

IMPORTANT:
Current privacy scanner uses simplistic line/cell CSV splitting.
Upgrade to a proper CSV parser that supports:
- quoted commas
- escaped quotes
- multiline quoted cells
- UTF-8
- BOM

Otherwise privacy/data validation can produce false positives or miss fields.

============================================================
9. PRIVACY SCANNER FORENSICS
============================================================

Run:
node tools/privacy.js --sheets --live --json

Do not simply allowlist every flagged email.

Classify:
PUBLIC
INTERNAL
SENSITIVE
SECRET

Verify:
- public tutor information
- private tutor contact
- admin notes
- booking details
- contact messages
- tokens
- API keys

The scanner must:
- fail for real secret exposure
- not fail on intentionally public data
- produce evidence
- not dump full sensitive values into reports/logs

============================================================
10. CRITICAL SEO FINDING — HREFLANG
============================================================

Current repository pages contain static hreflang sets.

The Spanish homepage currently lists:
en
es
fr
de
pt
ja
ar
x-default

That is acceptable only for actual equivalent homepage variants.

But do NOT apply the same language set mechanically to unrelated subpages.

Audit every hreflang family.

Each language alternate must:
- represent the same content intent
- exist
- return 200
- be canonical to itself
- link back reciprocally
- use correct hreflang
- not point to the wrong page type

Remove false cross-page hreflang relationships.

============================================================
11. CRITICAL SEO FINDING — META KEYWORDS
============================================================

Current Spanish page contains a very large:
<meta name="keywords" ...>

Google explicitly does not use meta keywords for Search ranking/indexing.

Remove useless keyword lists from production pages.

DO NOT replace them with keyword stuffing.

Use:
- useful title
- useful H1
- useful content
- useful internal links
- relevant descriptions
- natural language
- correct schema

Google's current documentation confirms meta-keywords are ignored. 

============================================================
12. TITLE / DESCRIPTION QUALITY
============================================================

Audit EVERY indexable page.

Detect:
- duplicate title
- near-duplicate title
- generic title
- keyword stuffing
- missing title
- duplicate meta description
- generic meta description
- inaccurate promise

Google primarily generates snippets from page content and may use meta descriptions when they better describe the page.

Create unique, accurate descriptions.

============================================================
13. CONTENT QUALITY / ADSENSE
============================================================

Google currently emphasizes:
- unique content
- relevant content
- clear navigation
- useful UX
- sufficient content
- fully launched site

Audit:
every page
every tool
every localized page
every answer
every course
every tutor page

Find:
- thin content
- auto-generated filler
- copied text
- repetitive text
- templated country pages
- templated language pages
- placeholder content
- incomplete pages
- empty tool pages

Classify:
KEEP
IMPROVE
MERGE
NOINDEX
REMOVE

Do not inflate page count.

============================================================
14. ADSENSE "COMING SOON" / LAUNCH STATE
============================================================

Current production must NOT present a misleading "COMING SOON" state if EkGuru is launched.

Search:
- site-config status
- injected status pill
- hero badges
- footer badges
- metadata
- schema
- admin status

Any "coming soon" must be factually accurate.

============================================================
15. ADSENSE CODE
============================================================

Verify:
publisher ID
script
ads.txt
site ownership
head placement
duplicate script
malformed client

Do not place ads on:
- empty utility screens
- private/admin pages
- test pages
- pages with insufficient publisher content

Do not submit solely because the code exists.

============================================================
16. SITEMAP
============================================================

Crawl complete sitemap tree.

Check:
- 200
- valid XML
- absolute HTTPS URLs
- canonical URL match
- indexable
- no redirects
- no 404
- no duplicate
- no old domain
- no private/admin
- correct lastmod

Compare sitemap URL count to actual generated page count.

============================================================
17. ROBOTS
============================================================

Verify:
- Googlebot allowed
- valuable pages crawlable
- CSS/JS resources not unnecessarily blocked
- sitemap declared
- admin/private content not exposed

Do not use robots.txt as a privacy mechanism.

============================================================
18. ALL-PAGE STATUS CRAWL
============================================================

Crawl every intended public URL.

Report:
200
3xx
4xx
5xx
soft404
timeout
redirect chain
broken assets

Also detect:
- canonical mismatch
- noindex
- orphan
- sitemap-only
- JS-only
- wrong language

============================================================
19. EVERY PAGE REACHABILITY
============================================================

Build a graph.

Every important indexable page:
- must have internal incoming links
- should be reachable from a hub
- should not exist only in sitemap
- should not require JS click discovery only

Measure:
depth
inlinks
outlinks

Fix important orphans.

============================================================
20. SEARCH / TOOL FUNCTIONALITY
============================================================

Test every existing tool with:

empty
normal
long
Unicode
Hindi
English
mixed
punctuation
emoji where relevant
copy
clear
reset
mobile keyboard
slow network
network failure

Check:
correct output
safe fallback
error state
accessibility
performance
SEO landing page

============================================================
21. LEARN SYSTEM
============================================================

Audit:
- lesson pages
- daily Hindi
- courses
- quizzes
- flashcards
- vocabulary
- grammar
- pronunciation
- reading
- listening
- speaking
- learning paths

Verify actual functionality, not just page existence.

No fake score.
No fake pronunciation score.
No broken exercises.

============================================================
22. TUTOR SYSTEM
============================================================

Audit:
- tutor data
- photos
- bios
- pricing
- schedules
- email routing
- profile URL
- booking
- reviews
- structured data
- stale data

Detect:
- fake/placeholder data
- duplicate profiles
- mismatched rating/review count
- broken external profile
- invalid availability

============================================================
23. HEADER
============================================================

Current desired:
Logo
Search
Find Tutors
How it works
Book a trial
Language
Currency

Remove:
Learn
Become a Tutor
misleading Coming Soon

Real browser test:
320
360
390
430
768
1024
1100
1200
1280
1366
1440
1536
1600
1920

Check:
overlap
clipping
offscreen
focus
touch
dropdown
sticky state

============================================================
24. ANIMATION
============================================================

Verify the motion system.

Especially:
- hamburger
- drawer
- backdrop
- dropdown
- modal
- tool result
- quiz
- form
- booking
- admin health

Test:
prefers-reduced-motion
slow device
CPU throttling
layout shift

No decorative animation should delay content.

============================================================
25. PERFORMANCE / RESPONSE TIME
============================================================

Measure separately:

DNS
TLS
TTFB
HTML download
CSS
JS
images
third-party scripts
total load
Largest Contentful Paint
Interaction to Next Paint
Cumulative Layout Shift

Do not report one "response time" for everything.

Create:
reports/performance-budget.json

For representative pages:
homepage
tool
Learn
tutor
guide
booking
contact

Record mobile and desktop.

Find:
- render-blocking
- oversized images
- unnecessary JS
- duplicate scripts
- third-party latency
- layout shifts
- excessive network requests

============================================================
26. JAVASCRIPT / CONSOLE
============================================================

Run full browser crawl and collect:

uncaught exceptions
unhandled rejections
failed fetch
CORS errors
404 assets
mixed content
timing errors
race conditions

Group by root cause.

Do not suppress errors just to get green.

============================================================
27. SECURITY
============================================================

Search code/build for:
- secrets
- API keys
- private credentials
- dangerous eval
- unsafe HTML insertion
- open redirects
- insecure URL handling
- exposed admin APIs
- CORS issues
- webhook verification
- auth bypass

If a secret has ever been exposed:
rotate it.

============================================================
28. ADMIN
============================================================

Every admin screen:

loading
success
empty
error
stale

Never show fake zero values after backend failure.

Health:
GREEN
YELLOW
RED
UNKNOWN

Unknown is not healthy.

Audit:
RBAC
audit logs
content
tutors
reviews
bookings
email
SEO
privacy

============================================================
29. BACKUP / RECOVERY
============================================================

Verify:
backup exists
integrity
restore test
rollback build

Do not consider backup complete without at least one restore verification.

============================================================
30. COPY PROTECTION
============================================================

Verify:
content fingerprints
internal duplicate detection
external monitoring
copy evidence
scraper detection
rate limiting

Do not block Googlebot or accessibility.

============================================================
31. GLOBAL / I18N
============================================================

Verify:
English
Hindi
Spanish
French
German
Portuguese
Japanese
Arabic

Test:
RTL
Unicode
line-height
dates
currency
timezone
number formatting
hreflang
canonical
localized navigation

Do not create fake localized pages.

============================================================
32. LEGAL / TRUST
============================================================

Verify:
About
Contact
Privacy
Terms
Disclaimer
Copyright

Must be:
live
reachable
accurate
internally linked
mobile
desktop

============================================================
33. ANALYTICS / SEARCH CONSOLE
============================================================

One clean analytics setup.

Track useful product events:
tool completion
lesson completion
practice completion
search
tutor view
booking start
booking completion
contact success

Do not collect unnecessary sensitive data.

============================================================
34. TEST FAILURE GATE
============================================================

A critical failure MUST block release.

Do not:
- mute
- skip
- rewrite test
- downgrade

Document any known false positive and fix the checker separately.

============================================================
35. LIVE VERIFICATION
============================================================

After fixes:
commit
deploy
wait for deployment
live smoke
live crawl
browser QA
email E2E
booking E2E
Doctor
Privacy
SEO

Then re-run everything.

============================================================
36. FINAL REPORT
============================================================

Return:

RESEARCH FINDINGS
CRITICAL
HIGH
MEDIUM
LOW

CURRENT LIVE BUILD:
matching / stale / unknown

URL HEALTH:
200
3xx
4xx
5xx
soft404
timeouts

SEO:
canonical
hreflang
sitemap
robots
metadata
schema

CONTENT:
strong
thin
duplicate
localized
orphan

TOOLS:
working
broken
degraded

EMAIL:
provider matrix
contact
student
tutor
internal
fallback

BOOKING:
routing
record
status
timezone

ADMIN:
health
privacy
RBAC
audit

PERFORMANCE:
DNS
TLS
TTFB
LCP
INP
CLS
total load

SECURITY:
critical
high
medium

ADSENSE:
exact known rejection reason if accessible
current controllable blockers
READY / NOT READY / UNKNOWN

FILES CHANGED:
exact list

TESTS RUN:
exact commands

LIVE EVIDENCE:
exact URLs/results

DO NOT claim:
"everything perfect"
"AdSense guaranteed"
"traffic guaranteed"
"all URLs indexed"

Only report verified facts.

# EKGURU — FINAL FULL PRODUCTION AUDIT + REPAIR MASTER COMMAND
# Use this command as the single source of truth.
# Do not drop previous requirements unless explicitly marked obsolete below.

PRODUCTION:
https://ekguru.shop/

OLD GITHUB PAGES:
https://ekgurulearning.github.io/EkGuru/

GOAL:
Make EkGuru genuinely production-ready for:
- AdSense review
- organic Google traffic
- international users
- mobile/tablet/desktop usability
- reliable contact + booking communication
- reliable Google Sheets/Apps Script data
- strong original content
- free useful tools
- scalable but quality-controlled expansion

IMPORTANT:
Do not promise AdSense approval or guaranteed traffic.
The job is to remove every controllable blocker and maximize quality.

============================================================
0. IMPORTANT PRINCIPLES
============================================================

1. Do not blindly create 1000–3000 low-value pages.
2. Every indexable page must have a distinct user purpose.
3. Do not use AI-detector evasion, fake authorship, fake experience, fake reviews, hidden text, keyword stuffing, synonym spinning, or copied content.
4. Do not destroy valid production data while repairing integrations.
5. Before destructive changes, snapshot/back up the current state.
6. Do not declare a fix complete from code inspection alone when live/end-to-end testing is possible.
7. Re-test the LIVE deployed site after deployment.
8. Preserve useful old GitHub URLs as redirects if they are correctly redirected to HTTPS production URLs.
9. Old GitHub URLs appearing in Google are NOT by themselves a bug.
10. Actual blockers are bad final redirects, HTTP final destinations, wrong canonical, broken links, thin/duplicate content, inaccessible pages, etc.

============================================================
1. LIVE REALITY CHECK — DO THIS FIRST
============================================================

Before changing code:

- fetch the live production homepage
- fetch sitemap
- fetch robots.txt
- fetch ads.txt
- fetch representative page types
- test HTTP/HTTPS
- test www/non-www
- test old GitHub URLs
- verify final redirect destinations

If a web/runtime fetch fails due to infrastructure/cache, report the exact limitation and use browser/curl/Playwright or another available method before assuming the site is broken.

Do not invent live results.

============================================================
2. SCREENSHOT-BASED HEADER BUG — NEW P0 UX ISSUE
============================================================

A current desktop screenshot shows the header visually crowded/overlapping:

- logo + tagline
- COMING SOON pill
- tutor search input
- "Find Tutor"
- "How it works"
- "Book a trial"
- language
- currency

The screenshot shows the search field crowding/overlapping the navigation text around the center of the header.

THIS MUST BE FIXED.

Test real browser at:
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

Do not accept a layout merely because there is no body horizontal scroll.

Check actual geometry:
- each nav item fully visible
- no overlap
- no clipping
- no element outside viewport
- no text touching adjacent control
- no z-index collision
- search box has safe width
- Book a trial remains visible and clickable
- language/currency controls remain visible and clickable
- logo/tagline remain readable
- header remains one coherent row at intended desktop widths
- responsive breakpoint changes happen before collision

Use element bounding boxes and screenshots.

If space is insufficient:
- use a deliberate breakpoint
- reduce search width gracefully
- hide/non-critical controls behind a menu at a sensible breakpoint
- or restructure spacing

Do NOT solve by making text tiny.

============================================================
3. "COMING SOON" CHECK — NEW P0/P1 TRUST + ADSENSE ISSUE
============================================================

The screenshot shows a visible "COMING SOON" pill on the live homepage/header.

Determine exactly what this badge means.

If the site is actually fully launched, REMOVE the "COMING SOON" wording from public production UI.

Replace with a truthful value/status message only if it has a genuine purpose.

Do NOT show:
- Coming Soon
- Under Construction
- Launch Soon
- Beta
- unfinished placeholder text

on a fully launched production site unless factually required.

Google AdSense guidance says a site should be fully built and launched, not effectively under construction.

============================================================
4. HEADER REQUIREMENT — PRESERVE PREVIOUS FIX
============================================================

REMOVE from HEADER on all devices:

- Learn
- Become a Tutor

Check:
- desktop
- tablet
- mobile
- sticky header
- hamburger drawer
- responsive duplicate nav

Do not delete the underlying pages.

Those pages must remain discoverable through suitable footer/contextual links where useful.

Also keep these visible header actions only if they fit without overlap:
- Find Tutors
- How it works
- Book a trial
- language
- currency

If a smaller viewport cannot fit them:
use a deliberate responsive navigation state.

============================================================
5. GOOGLE SHEETS / APPS SCRIPT — REPAIR BEFORE CONTENT REBUILD
============================================================

Production Apps Script:
https://script.google.com/macros/s/AKfycbwG978gM3Vspo0r8JmNxRojiUwA5h0tWoFd8p9vQf5x-NX9QGDB8VCr0j1LnTPoOjqtdA/exec

Data sources:

SETTINGS:
https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=764031473&single=true&output=csv

CONTENT:
https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=2135319947&single=true&output=csv

REVIEWS:
https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=1290168568&single=true&output=csv

TUTORS:
https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=834026040&single=true&output=csv

GITHUB URLS:
https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=1240181234&single=true&output=csv

EKGURU.SHOP URLS:
https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=355826593&single=true&output=csv

FULL WORKBOOK:
https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?output=csv

FIRST:
- snapshot current configuration
- fetch every source
- record status/headers/row counts/checksums
- map each gid to exact consumer
- compare source schema to code expectations
- identify mismatch
- identify missing/renamed/duplicate columns
- identify duplicate IDs
- identify malformed records
- identify empty/incomplete records

DO NOT overwrite production data automatically.

Then implement:
- one central DATA_SOURCES config
- schema validation
- timeout/retry
- cache
- stale-cache fallback
- safe empty/error state
- logging
- no silent empty-array fallback
- Apps Script contract tests

A temporary source failure must never turn the entire site blank.

============================================================
6. CONTACT FORM — FIX END TO END
============================================================

Current reported bug:
visitor contact reaches EkGuru internal mailbox, but visitor does not receive confirmation.

Required:

CONTACT FORM
→ internal EkGuru notification
→ visitor confirmation
→ Reply-To on internal notification = exact visitor email

Do NOT forge visitor as From.

Use verified EkGuru From identity + visitor Reply-To.

Test:
- valid submission
- invalid email
- empty message
- long message
- Hindi/Unicode
- repeated submission
- provider timeout
- provider failure
- mobile
- desktop
- actual mailbox delivery

Success must not be claimed merely from HTTP 200.

Use explicit:
SUCCESS
PARTIAL_SUCCESS
FAILURE

Add safe idempotency/submission IDs.

============================================================
7. BOOKING EMAILS — FIX END TO END
============================================================

Required where the product flow applies:

BOOKING
→ internal EkGuru notification
→ learner confirmation
→ tutor notification where appropriate

Learner email must contain:
- tutor
- date
- time
- timezone
- lesson type
- reference/booking ID
- status
- next step

Never claim CONFIRMED if it is only a REQUEST.

Timezone must be explicit.

Test:
- India
- US
- Europe
- DST edge cases
- date rollover
- mobile
- desktop
- duplicate click
- retries
- provider failure
- actual mailbox delivery

Do not break existing internal notification flow.

============================================================
8. OLD DOMAIN / MIGRATION — CORRECT INTERPRETATION
============================================================

Old GitHub URLs remaining in Google are acceptable if they redirect correctly.

DO NOT try to delete them manually just because they appear.

Test:

https://ekgurulearning.github.io/EkGuru/
→ 301
→ https://ekguru.shop/...
→ 200

NOT:

→ http://ekguru.shop/...
→ 200

Final destination must be HTTPS.

Search production build for:
ekgurulearning.github.io
/EkGuru/
http://ekguru.shop
http://www.ekguru.shop

Fix SEO signals:
- canonical
- og:url
- hreflang
- sitemap
- internal links
- JSON-LD
- breadcrumbs
- manifest
- image URLs

Preserve useful old redirects.

============================================================
9. SITEMAP / ROBOTS / ADS.TXT
============================================================

Verify live:

https://ekguru.shop/sitemap-index.xml
https://ekguru.shop/robots.txt
https://ekguru.shop/ads.txt

Sitemap:
- valid
- all child sitemaps valid
- no 404
- no redirect URLs
- no duplicate URLs
- no noncanonical URLs
- no accidental noindex URLs
- production HTTPS only

Robots:
- Googlebot allowed
- AdSense crawler not blocked
- no accidental Disallow: /
- CSS/JS needed for rendering not blocked
- sitemap declared

ads.txt exact line:

google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0

Must be 200/plain text.

============================================================
10. FULL 500+/542 URL INVENTORY
============================================================

Do not assume exact count.

Build:
URL
page type
language
country
HTTP
final URL
canonical
robots
indexable
title
description
H1
content length
originality
internal inlinks
internal outlinks
orphan
schema
hreflang
performance
mobile
desktop
issue
action

Actions:
KEEP
IMPROVE
MERGE
NOINDEX
REMOVE

============================================================
11. EVERY PAGE REACHABLE
============================================================

Hard requirement:

Every important indexable page must be reachable through normal crawlable HTML links.

Do not count:
- sitemap-only
- JS-only
- hidden utility pages
as fully reachable.

Build a graph:
Home
→ category/topic
→ detail
→ related content
→ tool/practice
→ learning path

Report:
- orphan pages
- sitemap-only pages
- JS-only pages
- login-gated pages
- pages reachable only after interaction

============================================================
12. CONTENT / ADSENSE QUALITY
============================================================

Google's current AdSense guidance emphasizes:
- unique content
- relevant content
- clear navigation
- useful UX
- sufficient content
- complete/finished site

Audit every indexable page.

Find:
- thin pages
- duplicate pages
- generic filler
- copied/replicated content
- unsupported claims
- fake experience
- fake reviews
- machine-translated poor text
- near-identical country pages
- near-identical language pages
- placeholder text

Do not try to “humanize AI text” to fool detectors.

Instead make content genuinely better:
- original explanations
- original examples
- practical exercises
- useful tools
- fact-checking
- editorial decisions
- real learner context

If a weak page cannot be made genuinely valuable:
MERGE / NOINDEX / REMOVE.

============================================================
13. ORIGINAL FREE VALUE / TRAFFIC ENGINE
============================================================

Build genuine free utilities based on real demand.

Priority:

Hindi transliteration
Hindi typing
Hindi name writing
Hindi pronunciation
Hindi dictionary/meaning
Hindi sentence builder
Hindi verb conjugator
Hindi grammar practice
Hindi vocabulary practice
Hindi flashcards
Hindi quiz
Hindi reading practice
Hindi listening practice
Hindi speaking practice
Hindi placement test
Hindi travel phrases
Hindi numbers
Hindi dates
Hindi time expressions
Hindi practical conversations

Each tool:
- immediately usable
- free core functionality
- explanation
- examples
- common mistakes
- related guides
- related practice
- optional tutor CTA

Do not generate thousands of indexable random tool-state URLs.

============================================================
14. GLOBAL EXPANSION
============================================================

Research demand by:
country
language
source language
learner intent
travel intent
work intent
study intent
heritage intent
translation intent
typing intent
pronunciation intent

Potential language families can be evaluated:
English
Spanish
Portuguese
French
German
Arabic
Japanese
Korean
Chinese
Russian
Turkish
Indonesian
Vietnamese
Thai
Bengali
Urdu
Punjabi
Marathi
Tamil
Telugu
Gujarati
Kannada
Malayalam
Nepali
Persian
Dutch
Polish
Italian
and others where actual demand supports quality.

Do NOT automatically publish every country/language.

For each proposed localized page require:
- demand evidence
- unique intent
- native-quality language
- unique examples
- real local context where relevant
- correct canonical/hreflang
- internal links
- real utility

No 195-country copy/paste pages.

============================================================
15. SEARCH INTENT / TOPICAL AUTHORITY
============================================================

Build clusters:

Alphabet
Pronunciation
Matras
Vocabulary
Grammar
Verbs
Gender
Sentence structure
Conversation
Travel Hindi
Typing
Transliteration
Reading
Listening
Speaking
Kids
Beginners
Culture
Questions
Tools
Learning paths

Each cluster:
Pillar
→ guides
→ tools
→ questions
→ practice
→ related topics
→ tutor option

============================================================
16. INTERNATIONALIZATION
============================================================

For real localized pages:
- correct lang
- canonical
- reciprocal hreflang
- x-default where appropriate
- locale-aware numbers
- dates
- currency
- timezone
- script
- line height
- typography
- RTL where needed
- mobile keyboard behavior

No hreflang pointing to:
404
redirect
wrong language
old domain

============================================================
17. STRUCTURED DATA
============================================================

Audit:
Organization
WebSite
BreadcrumbList
Person
Course only when genuinely a course
Quiz/educational markup only when eligible and truthful

No fake:
ratings
reviews
authors
prices
course claims

Schema must match visible page content.

============================================================
18. MOBILE REAL-BROWSER QA
============================================================

Test:
320x568
360x800
375x812
390x844
412x915
430x932
768x1024
820x1180

Detect:
- horizontal overflow
- clipped text
- clipped Hindi/Devanagari
- broken header
- hamburger
- drawer
- modal
- forms
- tables
- cards
- images
- fixed elements
- ads
- keyboard
- touch targets
- footer
- long strings

Take screenshots for actual failures.

============================================================
19. DESKTOP REAL-BROWSER QA
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
1680x900
1920x1080

Specifically re-test the screenshot's header collision.

Use bounding-box geometry, not jsdom alone.

Check every top-header element.

============================================================
20. RESPONSIVE BREAKPOINT QA
============================================================

Resize continuously:

320
→ 360
→ 390
→ 430
→ 768
→ 820
→ 1024
→ 1100
→ 1200
→ 1280
→ 1366
→ 1440
→ 1536
→ 1680
→ 1920

Find transition bugs.

============================================================
21. INTERACTION QA
============================================================

Click:
- every button
- every nav link
- every dropdown
- every modal
- language
- currency
- search
- tutor cards
- booking
- forms

Test:
- Escape
- outside click
- Back
- Forward
- refresh
- repeated submit
- slow network
- error state

No dead buttons.
No silent failures.

============================================================
22. JAVASCRIPT / ASSETS
============================================================

Find:
- uncaught exceptions
- unhandled rejections
- failed fetches
- 404 assets
- CORS
- mixed content
- broken modules
- duplicate scripts
- race conditions

Do not suppress errors.

============================================================
23. PERFORMANCE
============================================================

Measure:
TTFB
LCP
INP
CLS

Audit:
- images
- JS
- CSS
- fonts
- third parties
- analytics
- ad scripts
- layout shifts

Optimize actual UX.

============================================================
24. ACCESSIBILITY
============================================================

Check:
- keyboard
- focus
- labels
- headings
- alt
- contrast
- touch targets
- modal focus
- language attributes

============================================================
25. LEGAL / TRUST / FOOTER
============================================================

Verify:
about
contact
privacy
terms
disclaimer

All:
- live
- reachable
- production URLs
- mobile
- desktop
- internally linked

Also verify footer and legal links work after removing Learn/Become a Tutor from the header.

============================================================
26. ANALYTICS / SEARCH CONSOLE
============================================================

Ensure one clean analytics implementation.

Measure:
organic landing pages
queries
CTR
position
country
device
tool usage
tutor clicks
booking intent
contact submissions

Search Console:
- production property
- sitemap
- representative URL inspection
- indexing report
- real query/page data

Use real performance data to expand content.

============================================================
27. CONTENT FRESHNESS + FACT CHECK
============================================================

Audit:
- language facts
- grammar
- translation
- pronunciation
- cultural claims
- tutor details
- pricing

Do not invent facts.

Where needed:
- research
- cite
- review
- correct
- remove

============================================================
28. SEARCH TRAFFIC EXPANSION
============================================================

Prioritize pages/queries with:
- high impressions + low CTR
- positions 5–20
- high tool usage
- high engagement
- clear search intent

Build new pages only from demonstrated demand or a strong unique product utility.

============================================================
29. AUTOMATED REGRESSION
============================================================

Tests must catch:
- old domain SEO references
- bad final redirect
- HTTP final destination
- bad canonical
- bad hreflang
- bad sitemap
- bad robots
- ads.txt failure
- missing title
- missing H1
- accidental noindex
- orphan page
- broken link
- JS error
- horizontal overflow
- header collision
- Learn in header
- Become a Tutor in header
- Coming Soon on launched production
- contact visitor-email failure
- booking confirmation failure
- Sheets schema mismatch

============================================================
30. FINAL LIVE RE-AUDIT
============================================================

After every fix:
BUILD
→ DEPLOY
→ LIVE CRAWL
→ REAL BROWSER TEST
→ REGRESSION
→ RE-AUDIT

Do not call localhost success "production success".

============================================================
31. FINAL REPORT
============================================================

Return exact numbers:

LIVE:
- URLs
- 200
- 3xx
- 4xx
- 5xx
- redirect chains
- old-domain references

SEO:
- index-worthy
- thin
- duplicate
- noindex
- canonical issues
- hreflang issues
- orphan
- sitemap errors

CONTENT:
- pages improved
- pages merged
- pages excluded
- originality risks
- fact-check issues
- free tools
- learning paths
- global/localized pages

UX:
- mobile blockers
- tablet blockers
- desktop blockers
- header collision count
- overflow count
- JS errors
- accessibility blockers

DATA:
- settings rows
- content rows
- review rows
- tutor rows
- URL rows
- Apps Script status
- schema mismatches

EMAIL:
- contact internal
- contact visitor
- Reply-To
- booking learner
- booking tutor
- booking internal
- duplicate protection
- real mailbox E2E

ADSENSE:
- exact current rejection reason if available
- controllable blockers
- fixed blockers
- remaining blockers
- review readiness YES/NO

CRITICAL:
Do not say "AdSense approved" unless Google actually approved it.
Do not say "all pages indexed" unless Search Console evidence supports it.
Do not claim traffic is guaranteed.

The objective is a genuinely useful, original, reachable, technically stable, globally useful learning product.


============================================================
32. ULTRA EMAIL / CONTACT / BOOKING RELIABILITY
============================================================

Treat email delivery as a production subsystem, not a UI feature.

Current reported failure:
- contact message reaches EkGuru internal mailbox
- visitor does not reliably receive confirmation
- booking emails do not reliably reach the learner/tutor
- internal notification path must remain working

First map every existing email path:
- Web3Forms
- FormSubmit
- Resend
- SMTP2GO
- Apps Script
- SES
- server/API
- any fallback

For each path document:
provider
endpoint
from
to
reply-to
subject
payload
success response
failure response
timeout
retry
fallback

DO NOT blindly replace a currently working provider.

------------------------------------------------------------
32.1 CONTACT FORM REQUIRED FLOW
------------------------------------------------------------

CONTACT SUBMISSION
        |
        +--> EkGuru internal notification
        |
        +--> Visitor confirmation
        |
        +--> safe audit event

Internal email:
FROM = verified EkGuru sender
TO = EkGuru receiving inbox
REPLY-TO = exact visitor email

Visitor email:
FROM = verified EkGuru sender
TO = visitor email

Never put the visitor's arbitrary email into FROM.

Visitor confirmation must say:
- message received
- reference ID
- expected next step
- official EkGuru contact information

Do not expose:
- internal routing
- API keys
- admin notes
- other users
- private tutor data

------------------------------------------------------------
32.2 BOOKING EMAIL FLOW
------------------------------------------------------------

For an actual booking/request:

Learner
→ booking submitted
→ booking ID generated
→ booking status determined
→ internal notification
→ learner confirmation
→ tutor notification where applicable

Every email must reflect the TRUE booking status.

Statuses:
REQUEST_RECEIVED
PENDING
CONFIRMED
RESCHEDULED
CANCELLED
FAILED
PAYMENT_PENDING

Never call a REQUEST "CONFIRMED".

Learner email:
- booking ID
- tutor
- date
- time
- timezone
- lesson type
- current status
- next action

Tutor email:
- only information needed to fulfill the lesson
- no unnecessary private learner data

Internal email:
- full operational context
- source page
- user/reference ID if appropriate
- booking data
- status

------------------------------------------------------------
32.3 DELIVERY STATE MACHINE
------------------------------------------------------------

Persist safe delivery state:

contact:
internal_queued
internal_sent
visitor_queued
visitor_sent
visitor_failed

booking:
internal_sent
learner_sent
tutor_sent
learner_failed
tutor_failed

Do not resend a successfully sent message when the browser retries.

Use an idempotency key:
submission ID / booking ID.

------------------------------------------------------------
32.4 EMAIL PROVIDER FAILURE
------------------------------------------------------------

If provider A fails:

retry safely
→ fallback provider if configured
→ final failure state

Do not send duplicates.

Distinguish:
API accepted
from
provider delivered

Where provider supports delivery events/webhooks, consume them.

Do not claim "delivered" when only "accepted" is known.

------------------------------------------------------------
32.5 MAILBOX END-TO-END TEST
------------------------------------------------------------

Use controlled test inboxes.

Contact:
1. submit
2. internal inbox receives
3. visitor inbox receives
4. Reply-To is correct
5. no duplicate
6. Unicode works

Booking:
1. submit
2. learner inbox receives
3. internal inbox receives
4. tutor inbox receives if applicable
5. status is accurate
6. timezone is accurate
7. no duplicate

Record actual message IDs/provider IDs where available.

============================================================
33. ULTRA CONTACT / BOOKING UX
============================================================

Make form states explicit:

Idle
→ Validating
→ Sending
→ Success
or
→ Partial Success
or
→ Failure

Never display a fake success screen.

If internal delivery succeeds but visitor confirmation fails:
show an honest partial-success message without exposing internal technical details.

Provide safe retry.

Prevent:
double click
double tap
browser back duplicate
refresh duplicate

Use disabled submit state plus server-side idempotency.

============================================================
34. ULTRA HEADER / SCREENSHOT FIX
============================================================

The supplied production screenshot shows a visually crowded header.

Rebuild responsive header behavior from measured geometry.

Desktop:
- logo
- badge/status
- search
- navigation
- trial CTA
- language
- currency

must have explicit flex/grid constraints.

Do not let flex items silently overflow.

At each breakpoint choose a deliberate layout.

Priority order:
1. logo/brand
2. primary search/navigation
3. main CTA
4. language
5. currency
6. non-critical extras

If insufficient width:
collapse lower-priority controls into menu.

Do not:
- shrink text below readable size
- overlap controls
- hide content behind another element
- rely on overflow-x clipping

Use real browser screenshots and bounding rectangles.

============================================================
35. ULTRA SEARCH EXPERIENCE
============================================================

The tutor search box is visible in the header.

Make sure it actually works well:
- fast response
- mobile usable
- keyboard usable
- empty-state helpful
- no-results useful
- typo-tolerant where safe
- language-aware
- location-aware where supported
- tutor/profile/topic results separated clearly

No fake results.

Search result pages should not automatically become indexable query-parameter pages unless they have a legitimate standalone purpose.

============================================================
36. ULTRA FREE-UTILITY QUALITY
============================================================

Every public free tool must have:

1. immediate utility
2. clear input
3. clear output
4. examples
5. explanation
6. validation
7. error state
8. mobile UX
9. accessibility
10. related content
11. next learning step

A fake or broken generator is worse than no generator.

Google's current Search spam guidance explicitly treats deceptive/fake functionality as problematic.

============================================================
37. ULTRA CONTENT QUALITY
============================================================

For each important content page:

USER INTENT
→ DIRECT ANSWER
→ ORIGINAL EXPLANATION
→ REAL EXAMPLES
→ COMMON ERRORS
→ PRACTICE
→ FREE TOOL
→ RELATED TOPICS
→ LEARNING PATH

Do not add filler paragraphs simply to hit a word count.

No page should exist primarily to rank a keyword.

============================================================
38. ULTRA ORIGINALITY / ANTI-REPLICATION
============================================================

Search the repository/build for repeated text blocks.

Calculate similarity groups.

Flag pages with:
>80% substantial text similarity where separate pages are supposed to have different intent.

Do not automatically delete.
Classify:
- legitimate shared template
- legitimately equivalent language version
- duplicate page
- thin variant

For duplicate pages:
merge/canonicalize/noindex/remove as appropriate.

Do not use synonymizing or translation merely to disguise duplicates.

============================================================
39. ULTRA EDITORIAL QUALITY
============================================================

Create a content QA checklist:

accuracy
clarity
natural language
examples
source verification
learner usefulness
cultural sensitivity
grammar correctness
translation correctness
update need

For factual/linguistic claims that are uncertain:
research them before publishing.

Do not invent:
statistics
expert credentials
reviews
ratings
testimonials
user stories
personal experience

============================================================
40. ULTRA TRUST PAGES
============================================================

Improve:
About
Contact
Privacy
Terms
Disclaimer

Add real information where appropriate:
- what EkGuru is
- what services exist
- how tutors/content are handled
- how users can contact support
- privacy/data handling
- correction/reporting mechanism

Do not add fake company claims.

Ensure every trust page is reachable on mobile and desktop.

============================================================
41. ULTRA TUTOR MARKETPLACE QUALITY
============================================================

Every public tutor profile must be useful.

Validate:
name
photo
bio
languages
specialization
experience
pricing
availability
location where appropriate
teaching style
CTA

Detect:
duplicate profiles
empty profiles
stale profiles
invalid price
invalid URL
missing image
broken booking
fake rating/review

Do not fabricate reviews or ratings.

============================================================
42. ULTRA REVIEW SYSTEM
============================================================

Audit the review CSV/source.

Do not display reviews unless:
- source is legitimate
- review belongs to actual tutor/service context
- required moderation exists
- content is safe
- no fabricated review

If reviews are user-generated:
build moderation/reporting and avoid publishing unmoderated spam.

============================================================
43. ULTRA DATA INTEGRITY
============================================================

For Settings/Content/Reviews/Tutors/URL sources:

Validate:
primary IDs
unique IDs
required fields
URL format
language
status
date fields
price
email
image URLs
canonical URLs

Create relational checks:
review → existing tutor
booking → valid tutor
page → valid canonical
language page → valid alternate
URL row → existing page

No dangling data relationships.

============================================================
44. ULTRA ERROR OBSERVABILITY
============================================================

Create safe monitoring for:
- failed CSV fetch
- stale data
- Apps Script failure
- email provider failure
- booking failure
- contact failure
- broken URL
- JS exception
- failed asset
- failed form
- schema error

Each error should have:
event
timestamp
non-sensitive context
severity
source
request/submission ID if applicable

Do not log secrets or unnecessary personal data.

============================================================
45. ULTRA SECURITY / PRIVACY
============================================================

Audit:
- secrets
- API keys
- admin endpoints
- exposed spreadsheets
- form abuse
- XSS
- injection
- unsafe redirects
- open redirects
- CORS
- CSRF where relevant
- rate limiting
- spam
- webhook verification

Do not put private Google Sheet credentials into browser code.

Published read-only CSV URLs may be public only where that is intentionally acceptable.

============================================================
46. ULTRA SEARCH / SEO
============================================================

For every indexable page:

unique useful title
unique useful description
one primary H1
correct canonical
correct language
hreflang where appropriate
breadcrumb
meaningful internal links
HTTP 200
indexable
not orphan
useful content

Sitemap only includes intended indexable URLs.

============================================================
47. ULTRA INTERNATIONAL TRAFFIC
============================================================

Do demand research before creating regional pages.

For a new country/language page require:
- query evidence
- genuine localized intent
- native-quality copy
- unique examples
- local context
- internal links
- correct hreflang
- mobile test
- content-quality pass

Never produce country-name substitutions at scale.

============================================================
48. ULTRA SEARCH CONSOLE LOOP
============================================================

Once live data is available, create a recurring optimization process:

HIGH IMPRESSIONS + LOW CTR
→ improve title/description

POSITION 5–20
→ improve content/internal links

HIGH TRAFFIC + LOW CONVERSION
→ improve UX/CTA

HIGH TOOL USE + LOW SEARCH LANDING
→ create/improve tool landing page

HIGH DEMAND + NO GOOD PAGE
→ build genuinely useful page/tool

DECLINING PAGE
→ investigate before rewriting

Do not chase vanity metrics.

============================================================
49. ULTRA AD EXPERIENCE
============================================================

Before AdSense review, verify:
- ads do not cover buttons
- no accidental clicks
- no excessive density
- no ads on private communication screens
- no ads on empty/non-content pages
- no deceptive placement
- no intrusive popups
- no automatic unwanted redirects

Contact/private communication pages should remain usable without ad interference.

============================================================
50. ULTRA CONSENT / PRIVACY READINESS
============================================================

Review privacy and consent requirements for the markets served.

Check:
- privacy policy accuracy
- cookie/consent behavior where legally required
- analytics disclosure
- advertising disclosure
- data retention statements
- contact form data handling
- booking data handling

Do not claim legal compliance without evidence.

============================================================
51. ULTRA PERFORMANCE
============================================================

Set practical budgets.

Monitor:
TTFB
LCP
INP
CLS
JS payload
CSS payload
image weight
third-party requests

Pay special attention to:
homepage
tool pages
tutor pages
guide pages
booking
search

Do not add a third-party feature just because it looks useful if it significantly harms UX.

============================================================
52. ULTRA ACCESSIBILITY
============================================================

Test:
keyboard
screen reader labels
focus
contrast
headings
links
forms
modals
touch targets
language/script
reduced motion

No functionality should depend only on hover.

============================================================
53. ULTRA PAGE-REACHABILITY TEST
============================================================

Run graph reachability from:
homepage
main hubs
language hubs
topic hubs
tool hubs

Every indexable URL must be reachable from at least one relevant non-private page.

For each URL report:
depth from homepage
inlink count
outlink count
orphan
sitemap-only
JS-only

Investigate pages deeper than a reasonable crawl depth.

============================================================
54. ULTRA BUILD / DEPLOYMENT SAFETY
============================================================

Before deployment:
- snapshot data
- git diff
- build
- full tests
- sitemap test
- email test
- Apps Script test
- browser test
- smoke test

After deployment:
- live smoke
- full live crawl
- email E2E
- selected booking E2E
- screenshot header
- representative mobile/desktop pages

Do not deploy if critical regression fails.

============================================================
55. ULTRA ADSENSE READINESS GATE
============================================================

Use Google's actual current reasons as the checklist:

CONTENT:
- high-quality
- original
- relevant
- sufficient
- not under construction

NAVIGATION:
- clear
- functional
- no broken links
- no excessive popups
- no confusing redirects

TECHNICAL:
- live
- accessible
- SSL
- HTTP → HTTPS
- crawler accessible
- ads.txt valid

TRAFFIC:
- no artificial/invalid traffic schemes
- no misleading acquisition
- no paid-to-click
- no automated traffic

POLICY:
- no prohibited content
- no copyright infringement
- no deceptive behavior
- no fake functionality

Do not submit for review until these are actually verified.

============================================================
56. ULTRA FINAL QUALITY SCORECARD
============================================================

Return a scorecard, NOT just "green":

A. Technical SEO / 100
B. Content quality / 100
C. Navigation / 100
D. Mobile UX / 100
E. Desktop UX / 100
F. Accessibility / 100
G. Performance / 100
H. Data integrity / 100
I. Email reliability / 100
J. AdSense readiness / 100
K. Internationalization / 100
L. Free-tool usefulness / 100

For every score below 90:
list exact blockers and fixes.

This score is internal only.
It is NOT a Google ranking formula.

============================================================
57. ULTRA FINAL REPORT
============================================================

Provide:

1. Critical blockers
2. High priority issues
3. Medium priority improvements
4. Low priority polish

Then:

TOTAL URLs
INDEX-WORTHY
EXCLUDED
ORPHAN
200
3xx
4xx
5xx

MOBILE BLOCKERS
DESKTOP BLOCKERS
HEADER COLLISIONS
JS ERRORS
BROKEN LINKS
CANONICAL ISSUES
HREFLANG ISSUES
OLD DOMAIN REFERENCES
SITEMAP ISSUES
ROBOTS ISSUES
ADS.TXT STATUS

SHEETS:
source status
row counts
schema mismatches
data-integrity errors

EMAIL:
contact internal
contact visitor
contact reply-to
booking learner
booking tutor
booking internal
delivery/acceptance evidence
duplicate protection

CONTENT:
strong
needs improvement
duplicate
thin
excluded
originality risks

FREE VALUE:
tools
practice systems
learning paths
topic clusters
localized experiences

ADSENSE:
exact rejection reason if accessible
current blockers
fixed blockers
remaining blockers
READY FOR REVIEW = YES/NO

============================================================
58. NON-NEGOTIABLE FINAL RULE
============================================================

DO NOT SAY:
"AdSense guaranteed"
"traffic guaranteed"
"Google will index all pages"
"perfect"

unless the statement is directly verified.

Instead:
FIND
→ FIX
→ TEST
→ DEPLOY
→ LIVE VERIFY
→ RE-AUDIT

Only then declare the controllable work complete.

The product should be genuinely useful enough that users choose EkGuru even when ads are removed.

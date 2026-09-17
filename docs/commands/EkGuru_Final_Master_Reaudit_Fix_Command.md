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

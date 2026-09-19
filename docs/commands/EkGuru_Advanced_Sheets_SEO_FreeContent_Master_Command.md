# EkGuru — Google Sheets/Apps Script Recovery + Advanced Free Content + SEO/Traffic Build

## Production
- Primary: https://ekguru.shop/
- Old: https://ekgurulearning.github.io/EkGuru/
- Apps Script: https://script.google.com/macros/s/AKfycbwG978gM3Vspo0r8JmNxRojiUwA5h0tWoFd8p9vQf5x-NX9QGDB8VCr0j1LnTPoOjqtdA/exec

## CRITICAL: REPAIR THE SHEETS INTEGRATION WITHOUT LOSING DATA

Production CSV sources:

### Settings
https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=764031473&single=true&output=csv

### Content
https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=2135319947&single=true&output=csv

### Reviews
https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=1290168568&single=true&output=csv

### Tutors
https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=834026040&single=true&output=csv

### GitHub URLs
https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=1240181234&single=true&output=csv

### EkGuru.shop URLs
https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?gid=355826593&single=true&output=csv

### Entire workbook
https://docs.google.com/spreadsheets/d/e/2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc/pub?output=csv

## PHASE 0 — INVENTORY FIRST
1. Locate every use of the Apps Script URL, every CSV URL and every gid.
2. Identify the exact schema/columns and row counts for every source.
3. Compare live CSV schema with local code schema.
4. Detect renamed/missing/duplicate columns, blank rows and type mismatches.
5. Create a backup/hash snapshot before any change.
6. Never delete/replace production data because one fetch failed or returned an empty dataset.
7. Produce a before/after diff: added, removed, changed, invalid.

## PHASE 1 — CENTRALIZE AND HARDEN THE DATA LAYER
Create one source-of-truth data configuration. Do not scatter CSV URLs across the codebase.

Implement a resilient CSV loader with:
- timeout
- retry/backoff
- cache
- stale-cache fallback where safe
- schema validation
- row validation
- normalized data
- explicit error reporting

One broken Google Sheet must never blank the entire website.

For each source:
LIVE CSV → parse → validate → normalize → compare → intentional fix only.

Validate IDs, URLs, languages, booleans, prices, emails and required fields.

## PHASE 2 — APPS SCRIPT CONTRACT
Audit the web app endpoint and verify:
- HTTP success
- expected JSON/response contract
- no HTML error page
- no stale deployment
- doGet/doPost correctness
- CORS behavior where applicable
- rate-limit/error handling
- no hard-coded row numbers
- no silent empty response

Add contract tests. If public reads do not need Apps Script, do not unnecessarily route all public traffic through it.

## PHASE 3 — HEADER CHANGE (USER REQUIREMENT)
REMOVE `Learn` from the HEADER on every device and every header variant.
REMOVE `Become a Tutor` from the HEADER on every device and every header variant.

Test:
- desktop header
- tablet header
- mobile header
- sticky header
- scrolled header
- hamburger drawer
- responsive breakpoint variants

Remove them from navigation data/config or actual markup. Do not leave hidden duplicate menu copies. Do not delete the underlying Learn or Become-a-Tutor pages/features. Preserve useful footer/contextual links where appropriate.

After the change, assert that no rendered header/drawer contains those two labels at all tested breakpoints.

## PHASE 4 — DOMAIN / URL NORMALIZATION
Production SEO identity must be https://ekguru.shop/.
Search data, source, generated HTML, JSON, JS, CSS, CSV-driven links, canonical, hreflang, sitemap, schema, OpenGraph, internal links and email templates for:
- ekgurulearning.github.io
- /EkGuru/
- http://ekguru.shop/
- www.ekguru.shop/

Remove stale production SEO references without destructively rewriting historical source data.

## PHASE 5 — INDEXING / SEO
Crawl the complete URL inventory and classify:
A = strong index-worthy
B = index-worthy after fixing
C = duplicate/thin/private/utility

For intended indexable pages verify:
- HTTPS
- HTTP 200
- index/follow
- self-canonical
- unique title
- useful description
- one clear H1
- real content/function
- internal links
- correct language
- hreflang where appropriate
- valid schema only when truthful

## PHASE 6 — ADVANCED FREE VALUE ENGINE
Do NOT build pages just to increase URL count. Build pages/tools that solve real user problems immediately.

Prioritize these families:

### Hindi text/writing
- English→Hindi transliterator
- Hindi→Roman transliteration
- Hindi typing
- Devanagari keyboard
- Unicode converter/normalizer
- character/word/sentence counters
- text cleanup
- punctuation helper
- name-to-Hindi
- pronunciation helper

### Learning
- alphabet/swar/vyanjan practice
- matra practice
- vocabulary practice
- sentence builder
- reading/listening/speaking practice
- placement test
- daily practice
- flashcards
- quizzes

### Grammar
- verb conjugator
- tense practice
- gender/plural practice
- pronoun/postposition practice
- adjective agreement
- sentence correction
- word-order practice

### Practical Hindi
- travel
- airport
- hotel
- restaurant
- shopping
- taxi/transport
- railway
- doctor/hospital
- emergency
- office
- school
- interview
- phone-call phrases

### Reference
- numbers 1–100 / 1–1000
- ordinals
- days/months/dates/time/seasons
- colors
- family relations
- body parts
- verbs
- question words
- pronouns
- common sentence patterns

Every utility should provide the core action FREE, plus explanation, examples, mistakes, practice and related resources.

## PHASE 7 — ANSWER-FIRST LANDING PAGES
Use:
H1 → immediate answer/tool → examples → explanation → common mistakes → practice → related topics → next lesson → optional tutor CTA.

Do not force login for basic utility use. Do not put ads over the primary function.

## PHASE 8 — PRACTICE ENGINE
Build reusable randomized:
- MCQ
- fill in blank
- matching
- flashcards
- sentence building
- pronunciation practice where technically possible
- score/retry

Keep dynamically generated practice from becoming thousands of thin indexed URLs unless each page has substantial standalone value.

## PHASE 9 — LEARNING PATHS
Build reusable paths such as:
- Hindi from zero
- 7-day beginner
- 14-day beginner
- 30-day beginner
- reading
- speaking
- travel Hindi
- grammar
- vocabulary

Reuse strong content instead of duplicating it.

## PHASE 10 — INTERNAL LINK GRAPH
Build:
Topic → Guide → Tool → Practice → Related Question → Learning Path → optional Tutor.

Find all orphan pages. Use meaningful anchors and avoid link stuffing.

## PHASE 11 — GOOGLE QUALITY/POLICY SAFETY
Current Google guidance makes scaled low-value content a risk. Do not:
- mass-generate near-duplicates
- synonym-spin
- create low-value machine translations
- scrape feeds/results
- stitch pages without added value
- create keyword-only pages
- make doorway pages
- create fake generators/tools
- create ad-first pages

If a page has no independent user value: improve, merge, noindex or remove from sitemap as appropriate.

## PHASE 12 — ADSENSE READINESS
Verify live:
https://ekguru.shop/ads.txt

Exact line:
google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0

Also verify About, Contact, Privacy, Terms and Disclaimer are live, linked and accurate.

Audit ad placement, density, accidental clicks, overlays, empty pages and ad/content confusion.
Do not promise approval; remove controllable policy blockers.

## PHASE 13 — MOBILE / TABLET / DESKTOP DEEP QA
Use browser automation and screenshots.

Mobile: 320x568, 360x800, 375x812, 390x844, 412x915, 430x932
Tablet: 768x1024, 820x1180
Desktop: 1024x768, 1280x720, 1366x768, 1440x900, 1536x864, 1920x1080

Detect:
- horizontal overflow
- clipped Hindi/Devanagari text
- cut-off buttons/headings
- grid/card breakage
- menu/hamburger overflow
- modal overflow
- sticky header overlap
- footer overflow
- form/input problems
- table overflow
- fixed overlays covering content
- image overflow
- broken line wrapping

Also test live resizing: 320 → 360 → 390 → 430 → 768 → 1024 → 1280 → 1440 → 1920.

Take screenshots for every real visual failure.

## PHASE 14 — INTERACTION QA
Test every button/link/dropdown/modal; Escape; click outside; scrolling; Back/Forward; refresh; valid/invalid forms; slow network; offline-after-load.

Find dead buttons, stuck scroll, focus issues, double-submit, silent failure and race conditions.

## PHASE 15 — JAVASCRIPT / PERFORMANCE / ACCESSIBILITY
Check uncaught exceptions, rejected promises, failed fetch/assets, CORS, mixed content, duplicate scripts and render failures.

Measure TTFB, LCP, INP, CLS. Audit oversized images, JS, CSS, third-party scripts, fonts, analytics and ad scripts.

Check keyboard navigation, focus, labels, alt text, headings, contrast, touch targets, modal semantics and language attributes.

## PHASE 16 — TESTS / REGRESSION
Automate checks for:
- CSV schema and row counts
- Apps Script contract
- old-domain references
- canonical/hreflang
- sitemap/robots
- ads.txt
- broken links
- missing title/H1
- accidental noindex
- horizontal overflow
- JS errors
- header items absent
- mobile menu
- desktop header

Fail the build for critical regressions; avoid false positives.

## PHASE 17 — FINAL REPORT
Return:

### Data
settings/content/reviews/tutors/GitHub-URLs/EkGuru-URLs row counts and validation status.

### Integration
Apps Script status, CSV fetch status, schema issues, cache/fallback status.

### SEO
URL count, index-worthy count, excluded count, 200/3xx/4xx/5xx, orphan pages, canonical issues, hreflang issues, old-domain references, sitemap and robots status.

### UX
mobile/tablet/desktop failures, horizontal overflow count, JS errors, broken interactions.

### AdSense
ads.txt status, trust/legal pages, policy-risk findings, ad placement issues.

### Header
Learn removed from all headers: YES/NO.
Become a Tutor removed from all headers: YES/NO.
Underlying pages preserved: YES/NO.

### Free value
number of working tools, practice systems, strong topic clusters and genuinely indexable pages.

For every issue: FIND → FIX → TEST → RE-AUDIT.

Do not claim all pages are indexed, AdSense is approved or traffic is guaranteed. Report only verified facts.

## FINAL QUALITY RULE
Quality and genuine utility > raw page count.
The safest growth architecture is:
Google query → useful free answer/tool → practice → related content → learning path → optional tutor.

Only expand toward 1000–3000 pages when each additional page/tool/lesson represents a real, distinct user need. Current Google guidance explicitly warns against scaled content created mainly to manipulate rankings rather than help users.

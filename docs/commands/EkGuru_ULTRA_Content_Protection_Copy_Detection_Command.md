# EKGURU — ULTRA CONTENT PROTECTION + COPY DETECTION + ORIGINALITY DEFENSE

PRODUCTION:
https://ekguru.shop/

OBJECTIVE:
Make EkGuru's original content, tools, learning materials, structured data and publisher assets difficult to copy at scale, while building a reliable detection + evidence + takedown workflow.

IMPORTANT:
No technical system can make public web content literally impossible to copy.
The goal is:
1. reduce casual/automated copying where practical,
2. make content traceable,
3. detect substantial copying quickly,
4. preserve evidence,
5. identify likely source/original publication time,
6. support takedown/copyright workflows,
7. avoid harming legitimate accessibility, search crawling, sharing, or usability.

Do NOT:
- block normal Google crawling,
- block screen readers,
- disable normal keyboard use,
- use deceptive obfuscation,
- break copy/paste for accessibility,
- fake legal claims,
- harass legitimate users,
- automatically accuse someone of infringement without evidence.

============================================================
1. CONTENT OWNERSHIP INVENTORY
============================================================

Create a complete originality inventory for:

- Learn pages
- Guides
- Articles
- Lessons
- Questions
- Tool explanations
- Tool output templates
- Practice banks
- Quizzes
- Flashcards
- Course material
- Original illustrations
- Original diagrams
- Original audio
- Original video
- Tutor/marketplace editorial content
- UX copy where materially original

For every content asset record:

asset_id
canonical_url
content_type
language
first_published
last_modified
author/editor if applicable
content_hash
structural_hash
word_count
unique_text_ratio
license/ownership status
source_file
sitemap status

Create:

reports/content-ownership-inventory.json

============================================================
2. CANONICAL CONTENT FINGERPRINTING
============================================================

Build multiple fingerprints, not just one hash.

For text:
- normalized SHA-256
- paragraph-level fingerprints
- sentence-level fingerprints
- SimHash or equivalent similarity fingerprint
- MinHash/shingling for near-duplicate detection

For structured content:
- normalized JSON hash
- schema fingerprint

For images:
- SHA-256
- perceptual hash (pHash/dHash/aHash where appropriate)
- dimensions
- creation/source metadata where available

For audio/video:
- file hash
- duration
- metadata fingerprint

Store fingerprints safely.

Do not expose internal hashes publicly.

============================================================
3. ORIGINALITY REGISTER
============================================================

Create a local/source-of-truth register:

asset_id
original_url
publication timestamp
content hash
source commit
build ID
language
owner
evidence path

Use this to establish that EkGuru had the content at a specific time.

Whenever significant original content is published:
- record commit
- build
- publication time
- content fingerprint

Do not falsify publication dates.

============================================================
4. PUBLIC CONTENT SIGNATURE
============================================================

Where appropriate, embed a subtle machine-readable ownership signal in page source.

Examples:

- canonical URL
- `og:url`
- structured data publisher/creator fields where truthful
- content identifier
- version/update timestamp where appropriate

Do NOT stuff hidden copyright text into the page solely for detection.

The page should remain clean and user-first.

============================================================
5. ORIGINALITY MARKERS
============================================================

For high-value educational content, add useful visible attribution where appropriate:

© EkGuru
Original educational content by EkGuru

or an accurate author/editor attribution.

Do not claim ownership of third-party material.

Clearly distinguish:
- original EkGuru content
- licensed content
- public-domain content
- user-generated content
- third-party references

============================================================
6. DETECTION ENGINE — INTERNAL
============================================================

Create a content-copy monitoring pipeline.

Pipeline:

published content
→ fingerprint
→ monitoring queue
→ candidate match
→ similarity analysis
→ human/automated review
→ evidence package
→ action

Do not automatically accuse sites from weak similarity alone.

============================================================
7. WEB COPY DISCOVERY
============================================================

Where legally and technically feasible, periodically search the public web for:

- exact distinctive phrases
- rare sentence combinations
- unique headings
- unique examples
- unique tool descriptions
- unique course names
- unique educational explanations

Use multiple search probes per important page.

Do NOT search for every sentence.
Use high-signal phrases.

For high-value pages generate:

COPY_PROBE_1
COPY_PROBE_2
COPY_PROBE_3
...

Store probe phrases internally.

Do not expose private probe data in the UI.

============================================================
8. PHRASE CANARY SYSTEM
============================================================

For selected original content, create natural distinctive phrase patterns that are useful to the user but also help identify copying.

IMPORTANT:
Do not insert nonsense phrases, invisible text, keyword stuffing, or deceptive traps.

Canaries must be natural content.

If a distinctive paragraph appears verbatim elsewhere, use it as strong evidence for investigation.

============================================================
9. SIMILARITY SCORING
============================================================

For candidate pages calculate:

exact_match_ratio
sentence_match_ratio
n_gram_similarity
paragraph_similarity
structure_similarity
heading_similarity
image_similarity
unique_phrase_overlap

Produce:

LOW
MEDIUM
HIGH
VERY_HIGH

Do not classify by one metric.

Suggested internal logic:
- low: weak overlap
- medium: investigate
- high: likely substantial copying
- very high: strong candidate for manual review

These are internal signals, not legal judgments.

============================================================
10. COPY SOURCE DETECTION
============================================================

When a candidate match is found, compare:

EkGuru first-known publication date
candidate publication/index/discovery date
content version
shared distinctive passages
images
headings
structure
tool text

Generate a timeline.

Do not claim who copied whom solely from dates without evidence.

============================================================
11. DETECT SCRAPERS / MIRROR SITES
============================================================

Look for:
- entire-site copies
- copied tool pages
- copied course pages
- copied navigation
- copied page titles
- copied structured data
- copied images
- copied footer/legal text

Generate a cluster:

SOURCE:
EkGuru page

COPIES:
candidate URLs

MATCH:
percentage + evidence

============================================================
12. IMAGE COPY DETECTION
============================================================

For original EkGuru images:

- maintain asset hash
- perceptual hash
- filename
- canonical asset URL

Monitor candidate matches where feasible.

Do NOT watermark every image automatically if it harms UX.

For high-value original illustrations, consider subtle visible attribution/watermark.

============================================================
13. CODE / TOOL COPY DETECTION
============================================================

Protect original tool implementations.

Search public repositories/web for distinctive:
- function names
- UI strings
- generated text
- unique algorithms where publicly visible
- rare variable structures only when legitimately detectable

Do NOT publish secrets.

Important:
Client-side JavaScript can be copied by users because the browser receives it.
Therefore, keep sensitive logic/server secrets server-side.

============================================================
14. SERVER-SIDE PROTECTION FOR PROPRIETARY LOGIC
============================================================

Where a tool has genuinely proprietary logic:

Do not ship all logic to the browser.

Move sensitive logic to:
- server/API
- protected backend
- validated endpoint

But do NOT move simple UI logic server-side unnecessarily.

Never expose:
API secrets
private keys
provider credentials

============================================================
15. SCRAPING / BOT OBSERVABILITY
============================================================

Monitor public traffic for abnormal patterns.

Signals:
- extremely high request rate
- sequential crawling of every page
- same user agent + impossible request frequency
- repeated HTML fetches without assets
- abnormal endpoint enumeration
- suspicious query patterns

Classify:
NORMAL
FAST_BOT
SUSPICIOUS
BLOCKED

Do not block:
- Googlebot verified through reverse+forward DNS
- legitimate search bots where desired
- accessibility tools
- normal users

Bot identity must not be trusted solely from User-Agent.

============================================================
16. RATE LIMITING FOR SCRAPERS
============================================================

For suspicious non-legitimate traffic:

- rate limit
- slow down
- challenge
- temporarily block
- monitor

Do not punish ordinary users.

Use:
IP
session
user agent
ASN/provider signals where lawful and appropriate
behavioral patterns

Do not rely on one signal.

============================================================
17. ROBOTS.TXT — DO NOT ABUSE
============================================================

Do NOT add broad robots blocks to try to stop copying.

Robots.txt is not a copyright protection system.

Keep Google crawling and indexing working.

Use robots only for crawl policy, not as a security mechanism.

============================================================
18. HOTLINK PROTECTION
============================================================

For original media where appropriate:

- prevent unauthorized hotlinking where technically safe
- preserve social sharing
- preserve image search where desirable
- do not break legitimate embeds unintentionally

Test:
- direct image
- page image
- social preview
- legitimate browser
- CDN cache

============================================================
19. CONTENT ACCESS / UX
============================================================

Do NOT disable:
- right click
- Ctrl+C
- keyboard shortcuts
- text selection
- screen readers

These are weak barriers and harm accessibility/usability.

Focus on:
attribution
detection
monitoring
evidence
rate limiting for abuse

============================================================
20. STRUCTURED DATA OWNERSHIP SIGNALS
============================================================

Where truthful, include appropriate:
- Organization
- WebSite
- Person/creator
- publisher
- canonical
- datePublished
- dateModified

Do not invent author names.

Do not use structured data to claim ownership of content you do not own.

============================================================
21. COPYRIGHT / NOTICE PAGE
============================================================

Create/improve a clear copyright/content-use page if appropriate.

Explain:
- EkGuru original content
- permitted linking/sharing
- attribution expectations
- how to report infringement
- how to request permission

Do not claim rights over:
- public-domain text
- third-party licensed material
- user-generated content
- standard facts
- common language examples

============================================================
22. COPYRIGHT REPORTING WORKFLOW
============================================================

Build an internal infringement report workflow.

Fields:
reporter
relationship to content
original URL
candidate copied URL
description
evidence
screenshots
date
contact
status

Statuses:
NEW
UNDER_REVIEW
VALIDATED
REJECTED
NOTICE_PREPARED
RESOLVED
ESCALATED

Do not automatically send accusations.

============================================================
23. EVIDENCE PACKAGE
============================================================

When high-similarity copying is found, generate an evidence package:

original URL
candidate URL
first-known publication
latest EkGuru version
content hashes
matched passages
similarity score
screenshots
timestamps
source commit
build ID
asset hashes if applicable

Keep copies of evidence where legally and technically appropriate.

============================================================
24. CHANGE HISTORY
============================================================

For high-value pages retain:
- previous version
- new version
- date
- commit
- editor/reviewer
- reason

This helps distinguish legitimate evolution from copying.

============================================================
25. COPY DETECTION DASHBOARD
============================================================

Add admin view:

TOTAL MONITORED ASSETS
RECENT MATCHES
HIGH-CONFIDENCE MATCHES
OPEN REVIEWS
RESOLVED
FALSE POSITIVES

Filters:
- content type
- language
- date
- similarity
- domain
- status

Each result:
EkGuru source
candidate
similarity
matched text evidence
timeline
action

============================================================
26. ALERTING
============================================================

Create alerts only for meaningful events:

VERY_HIGH similarity
entire-page copy
entire-tool copy
large content cluster copy
original images copied at scale

Do not alert for:
- common phrases
- short generic sentences
- ordinary language examples
- standard definitions
- legally permissible quotations/usage

Deduplicate repeated alerts for same site/content cluster.

============================================================
27. COPY MONITORING SCHEDULE
============================================================

Priority:

Tier A high-value pages:
weekly monitoring

Tier B:
monthly

Tier C:
quarterly or on demand

Monitoring frequency can be adjusted by actual risk.

Do not create expensive full-web scans unnecessarily.

============================================================
28. CANARY CONTENT
============================================================

For selected original pages, maintain 2–3 distinctive natural phrases.

Rotate when content is materially changed.

Keep an internal record:
asset
phrase
version
date

Do not make the phrase awkward or deceptive.

============================================================
29. SEARCH CONSOLE / INDEX MONITORING
============================================================

Monitor when useful:
- copied-looking pages outranking original
- unexpected domains using exact titles
- canonical confusion
- duplicate clusters

Do not assume Google Search Console alone can prove infringement.

============================================================
30. LEGAL / POLICY SAFETY
============================================================

Do not automatically threaten legal action.

Use evidence first.

Where action is needed:
- contact website owner
- hosting provider
- CDN/provider
- search engine copyright reporting channels
- formal notice
only with truthful evidence and appropriate legal process.

EkGuru should keep records of:
who sent notice
when
what evidence
what response
what resolution

============================================================
31. ORIGINAL CONTENT GENERATION SAFETY
============================================================

For all new Learn/Tool content:
- store source metadata
- store fingerprint
- store editor/reviewer
- record publication
- record version

Do not publish generated content without quality review.

============================================================
32. CONTENT DIFFERENTIATION
============================================================

If multiple pages are intentionally related:

give each page distinct:
- user intent
- examples
- exercises
- tool state
- explanations
- internal link role

Do not clone a template with tiny substitutions.

This protects against:
- thin content
- doorway patterns
- accidental self-duplication
- search cannibalization

============================================================
33. SELF-COPY DETECTION
============================================================

Before publishing a new page, compare it against all existing EkGuru content.

Detect:
- internal duplicate
- near duplicate
- canonical conflict
- overlapping search intent
- repeated paragraphs
- repeated examples

Require review if similarity is high.

This is as important as detecting external copying.

============================================================
34. CONTENT VERSION API
============================================================

For original high-value content, maintain a lightweight internal content record:

asset_id
version
hash
published_at
updated_at
source_commit
reviewed_by
review_status

Do not expose private editorial metadata publicly.

============================================================
35. EXPORTABLE EVIDENCE
============================================================

Allow admin to export an evidence bundle:

JSON
CSV
screenshots
matched text report
hash report

Do not expose this publicly.

============================================================
36. PERFORMANCE SAFETY
============================================================

Protection systems must not slow every public page.

Use:
- asynchronous monitoring
- cached fingerprints
- background jobs
- sampled traffic analysis
- batch similarity scans

Do not run expensive external searches during every page request.

============================================================
37. PRIVACY
============================================================

Do not collect more visitor data than necessary to detect abuse.

Avoid storing:
- unnecessary IP history
- sensitive personal data
- private form content

Use retention limits for abuse logs.

Document data handling.

============================================================
38. ROBOTS / INDEXING PROTECTION
============================================================

Never solve copy detection by blocking:
- Google
- users
- screen readers
- normal rendering
- site navigation

SEO and accessibility remain intact.

============================================================
39. FINAL VALIDATION
============================================================

Run:

1. Originality inventory
2. Internal duplicate scan
3. Fingerprint generation
4. Existing content crawl
5. Copy-monitoring test with known controlled test pages
6. scraper/rate-limit test
7. privacy test
8. accessibility test
9. SEO regression
10. performance regression

Create controlled test content in a safe/local environment.
Do not publish fake copyright traps to production.

============================================================
40. SUCCESS CRITERIA
============================================================

PASS requires:

- high-value content fingerprinted
- internal duplicate detection working
- external copy-monitoring pipeline working or clearly documented limitations
- evidence package generation working
- admin dashboard working
- alerts deduplicated
- scraper observability working
- rate limiting working
- legitimate Google/user access unaffected
- no accessibility regression
- no SEO regression
- no privacy regression
- no secrets exposed

============================================================
41. FINAL REPORT
============================================================

Return:

MONITORED ASSETS
TEXT
IMAGES
AUDIO
VIDEO
TOOLS
COURSES

FINGERPRINTS:
count

INTERNAL DUPLICATES:
count

EXTERNAL MATCH CANDIDATES:
count

HIGH-CONFIDENCE:
count

FALSE POSITIVES:
count

SCRAPER EVENTS:
count

RATE-LIMIT EVENTS:
count

EVIDENCE PACKAGES:
count

OPEN CASES:
count

RESOLVED:
count

FILES CHANGED:
exact

TESTS:
exact commands
results

LIMITATIONS:
what cannot technically be prevented/detected reliably

============================================================
42. FINAL PRINCIPLE
============================================================

EkGuru should be protected by:

ORIGINAL CONTENT
+
VERSION HISTORY
+
FINGERPRINTS
+
DISTINCTIVE NATURAL PHRASES
+
WEB MONITORING
+
SIMILARITY ANALYSIS
+
SCRAPER OBSERVABILITY
+
RATE LIMITING
+
EVIDENCE PACKAGES
+
ADMIN WORKFLOW
+
TRUSTWORTHY COPYRIGHT PROCESS

NOT by:
- disabling copy
- blocking search engines
- fake obfuscation
- hidden traps
- accessibility-breaking scripts

END.

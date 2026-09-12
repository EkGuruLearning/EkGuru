# EKGURU — NEXT REMAINING ULTRA WORKSTREAM
## Learn + Advanced Tools + Power Admin + P0 Email/Release Verification

PRODUCTION: https://ekguru.shop/
REPO: https://github.com/ekgurulearning/EkGuru.git

IMPORTANT:
Read the latest agent report and all previous master commands first.
Current known state:
- Header: locally verified, not live until deployment.
- Student booking email: code repaired, actual mailbox test BLOCKED on owner-side Apps Script token.
- GitHub push: credential-blocked.
- Learn/Tools/Admin expansion: NOT STARTED.
Do not redo completed work unless regression is found.

============================================================
1. LEARN QUALITY AUDIT
============================================================

Inventory every:
Learn page, lesson, guide, answer, course, Daily Hindi, quiz,
flashcard, vocabulary, grammar, pronunciation, reading, listening,
speaking, practice, learning path, toolbox and tool.

Create:
reports/learn-tools-quality-baseline.json

Record:
URL, intent, quality, depth, originality, examples, practice,
tool linkage, internal links, SEO, mobile, desktop, accessibility,
performance, duplicate risk, bugs, priority.

Classify:
A Strong / B Improve / C Thin / D Broken / E Duplicate.

Do not increase page count before improving weak high-value material.

============================================================
2. LEARN HUB + PATHS
============================================================

Turn Learn into a real product:

Start Here
Speaking
Listening
Reading
Writing
Vocabulary
Grammar
Pronunciation
Conversation
Practice
Tools
Learning Paths

Create real paths:
Hindi From Zero
Speaking Starter
Reading Hindi
Travel Hindi
Everyday Hindi
Grammar Foundations

Each path:
goal, level, modules, lessons, practice, quiz, review, completion, next step.

Prevent dead ends, missing lessons and circular paths.

============================================================
3. HIGH-QUALITY LESSON STANDARD
============================================================

Important lessons should include only useful blocks:
objective/direct answer
explanation
original examples
guided practice
common mistakes
quick check
related tool
related lesson
next step

No filler or keyword-padding.

============================================================
4. ADVANCED LEARNING SYSTEMS
============================================================

Implement/upgrade:

Vocabulary engine
Grammar Lab
Sentence Builder 2.0
Verb Lab 2.0
Pronunciation Lab
Listening Lab
Reading Lab
Writing/Devanagari Lab
Speaking/Conversation Lab
Practice Engine
Daily 5/10/20
Mastery/Review
Placement/Diagnostic

Do not claim formal certification or automatic pronunciation scoring unless genuinely supported.

============================================================
5. TOOLBOX — FIX ALL EXISTING TOOLS
============================================================

Test every current tool.

For each:
logic
accuracy
empty state
error state
copy/reset
examples
explanation
accessibility
mobile
desktop
performance
SEO
related learning

A page opening is NOT proof the tool works.

============================================================
6. NEW ADVANCED TOOLS
============================================================

Only add genuine user-value tools:

Writing:
Hindi Typing
Transliteration
Name Writer
Sentence Builder
Text Cleaner
Devanagari Converter
Unicode Hindi Checker
Character/Word Counter
Matra Checker
Reading Helper

Vocabulary:
Word Meaning
Phrase Meaning
Topic Vocabulary
Vocabulary Quiz
Flashcard Maker
Sentence-from-word Practice

Grammar:
Gender Practice
Plural Practice
Verb Practice
Tense Practice
Question Builder
Postposition Helper
Sentence Pattern Explorer
Grammar Checker ONLY if trustworthy

Real-life:
Travel
Restaurant
Shopping
Directions
Time/Date
Numbers
Money
Emergency
Railway/Transport
Hotel
Workplace
Family

No fake/broken generators.

============================================================
7. TOOL PAGE STANDARD
============================================================

Every major tool:
H1
purpose
working tool
how to use
examples
limitations
common mistakes
related learning
related tools

Do not surround tiny utilities with filler.

============================================================
8. ADMIN — LEARN OPERATIONS
============================================================

Upgrade Admin with:

Learning Operations dashboard
Content Quality Score
Content Editor
Practice Bank
Tool Control Center
Learning Path Builder
Learn Analytics
Search Insights
Content Gap Engine
Freshness Engine
Originality Center
Live Learning Health
One-click Diagnostics
Release Gate

Quality score should consider:
title, H1, answer, depth, examples, practice, tools,
internal links, originality, metadata, schema, accessibility,
mobile, performance, freshness.

Internal score only; not a Google ranking score.

============================================================
9. ADMIN — PRACTICE + TOOL CONTROL
============================================================

Practice Bank:
questions, flashcards, listening, reading, exercises.

Detect:
duplicates
ambiguous answers
wrong keys
missing explanations.

Tool Control:
status
version
last tested
test result
usage
error rate
mobile
desktop
performance
dependencies
fallback
owner

Critical disable = confirmation + audit.

============================================================
10. ADMIN — LEARNING PATH + GAP ENGINE
============================================================

Learning graph:
PATH → MODULE → LESSON → PRACTICE → QUIZ → REVIEW

Detect:
circular dependency
dead end
missing prerequisite
orphan lesson.

Search/content-gap workflow:
QUERY
→ existing page?
→ existing tool?
→ quality?
→ coverage?
→ action

Actions:
IMPROVE
CREATE TOOL
CREATE LESSON
CREATE PRACTICE
MERGE
NOINDEX

Never auto-generate thousands of pages.

============================================================
11. ADMIN — HEALTH + DIAGNOSTICS
============================================================

Health:
Learn
Tools
Questions
Practice
Search
Tutors
Booking
Contact
Email
Sheets
Apps Script
Sitemap
Robots
Ads.txt
JS errors
Performance

States:
GREEN / YELLOW / RED / UNKNOWN
Unknown is never green.

One-click:
Doctor
Privacy
SEO
Sitemap
Live Crawl
Data Sources
Tool Tests
Learn Tests
Email E2E
Booking E2E
Accessibility
Performance

============================================================
12. FREE-VALUE LOOP
============================================================

Design every major learner flow around:

Google
→ useful answer
→ tool
→ result
→ practice
→ learning path
→ return

Tutor CTA must remain contextual, not forced.

============================================================
13. MOBILE + DESKTOP QA
============================================================

Real browser:

Mobile:
320, 360, 390, 430, 768

Desktop:
1024, 1280, 1366, 1440, 1536, 1920

Check:
tools, tables, audio, dropdowns, modals, Devanagari,
long text, header, inputs and outputs.

============================================================
14. ACCESSIBILITY + PERFORMANCE
============================================================

Keyboard
focus
labels
screen-reader status
touch targets
reduced motion
text resizing
contrast

Measure:
TTFB
LCP
INP
CLS
JS size
network requests

Use code splitting/lazy loading where appropriate.

============================================================
15. SEO
============================================================

Each intended indexable Learn/Tool page:
unique title
useful description
H1
canonical
correct hreflang where applicable
eligible schema
internal links
reachable
not thin
not duplicate

Do not index random quiz states, filters, user-specific states or admin pages.

============================================================
16. CONTENT ORIGINALITY
============================================================

Every new content asset:
learning objective
original explanation
original examples
practice
review state
version
fingerprint

No copied text, keyword stuffing, fake expertise, fake reviews,
doorway pages or mass copy/paste country pages.

============================================================
17. P0 STUDENT EMAIL — KEEP BLOCKED UNTIL REAL TEST
============================================================

Latest report says student email is BLOCKED_ON_TOKEN.

Do not weaken the fix.

Once owner token is available:
1. wire it using the durable tool
2. deploy
3. Student A → Tutor A
4. Student B → Tutor B
5. verify actual student inboxes
6. verify tutor routing
7. verify EkGuru record
8. verify no duplicate
9. test fallback

Do NOT call API 200 or internal delivery "student email delivered."

============================================================
18. HEADER — PRESERVE
============================================================

Header local fix is already Chromium-verified.
Do not regress it.

It is LIVE only after a real deployment and live screenshot verification.

============================================================
19. RELEASE + REGRESSION
============================================================

After Learn/Tools/Admin work:
build
full tests
Doctor
Privacy
SEO
live crawl
browser
accessibility
performance
email regression
booking regression

Then commit and report SHA.

If GitHub credentials are unavailable:
do not claim deployment.

============================================================
20. FINAL REPORT
============================================================

Return exact:
Learn inventory / improved / new / remaining weak
Tools existing / fixed / upgraded / new / broken
Admin controls added
Quality score distribution
Learning paths
Practice systems
Search/content gaps
Mobile/Desktop results
Accessibility/Performance
P0 email status + mailbox evidence
Header status LOCAL_VERIFIED/LIVE_VERIFIED
Exact files changed
Exact commands/tests
Live verification status

STOP WHEN:
- major learner intents have strong answer/tool/practice flows
- major existing tools are reliable
- weak high-value pages are improved
- admin can operate normal Learn/Tools work without code edits
- learning graph has no critical gaps
- mobile/desktop/accessibility/performance pass
- no critical regression

END.

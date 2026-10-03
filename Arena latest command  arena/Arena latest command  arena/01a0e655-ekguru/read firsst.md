 EKGURU — ADSENSE APPROVAL DEEP COMMAND v4
### Complete fix — every rejection reason researched, audited and addressed
### Date: 2 October 2026 · Repo: EkGuruLearning/EkGuru · Site: https://ekguru.shop
---
## PART A — EVERY ADSENSE REJECTION REASON (researched from10+ sources)
### R-1. Low Value Content (THE #1 REJECTION REASON)
**What Google means:** Pages that don't provide enough useful, original, or meaningful information.
**Triggers:**
- Pages under400 words of own text
- Generic/templated paragraphs repeated across pages
- Auto-generated text without human editing
- Pages that exist primarily to show ads, not help users
- "Cookie-cutter" pages with only names changed
**EkGuru status:** ⚠️ RISK —237 repeated paragraph groups exist (mostly UI boilerplate: bylines, draft notices, section headers). The actual lesson content IS language-specific and unique. But Google may flag the shared boilerplate.
### R-2. Insufficient Content
**What Google means:** Not enough published content for Google to assess site purpose.
**Triggers:**
- Fewer than20-30 high-quality articles
- Pages under600 words
- Empty category pages
- "Under construction" pages
**EkGuru status:** ✅ OK —2643 pages total,1006 indexable,0 thin indexable. But some languages only have A1-B2 (4 levels), not full A1-C2.
### R-3. Missing Trust Pages
**What Google means:** No About, Contact, Privacy Policy pages.
**EkGuru status:** ✅ ALL PRESENT — about/, contact/, privacy/, terms/, disclaimer/, cookie-policy/, copyright/, editorial-policy/
### R-4. Policy Violations
**What Google means:** Adult content, illegal content, hate speech, copyrighted material.
**EkGuru status:** ✅ CLEAN — language learning site, no policy violations detected.
### R-5. Poor Navigation / UX
**What Google means:** Confusing navigation, broken links, mobile-unfriendly.
**EkGuru status:** ✅ GOOD —0 broken links, responsive design, clean navigation.
### R-6. Copyright / Copied Content
**What Google means:** Content copied from other sites without adding value.
**EkGuru status:** ✅ ORIGINAL — copy-index shows1670 unique page fingerprints, ownership checks pass.
### R-7. Unsupported Language
**What Google means:** Content in a language AdSense doesn't support.
**EkGuru status:** ✅ SUPPORTED —17 of18 published languages are AdSense-supported. Panjabi (pa) is not officially listed but Hindi (hi) covers the same audience.
### R-8. AI-Generated Content Without Editing
**What Google means:** Raw AI output without human curation, expertise, or originality.
**EkGuru status:** ⚠️ RISK — content is AI-assisted. Need to ensure every page has unique, human-like writing with real examples, cultural context, and honest bylines.
### R-9. Domain Age / New Site
**What Google means:** Very new sites (under3-6 months) get extra scrutiny.
**EkGuru status:** ✅ MATURE — domain ekguru.shop is established.
### R-10. Invalid Traffic
**What Google means:** Bot traffic, click farms, incentivized clicks.
**EkGuru status:** ✅ CLEAN — no paid traffic sources detected.
### R-11. Incomplete Website
**What Google means:** Half-built site, placeholder pages, empty categories.
**EkGuru status:** ⚠️ PARTIAL — some languages only have A1-B2 levels. Need to either complete to C1-C2 or ensure partial courses are clearly marked.
### R-12. Bad Ad Placement (post-approval)
**What Google means:** Ads before content, near buttons, intrusive.
**EkGuru status:** ✅ CORRECT — ads only on HIGH_CONTENT and MEDIUM_CONTENT pages, excluded from courses/practice/quiz/legal/contact.
---
## PART B — CURRENT SITE AUDIT RESULTS
### What's GOOD (keep):
- ✅ All trust pages exist (about, contact, privacy, terms, disclaimer, cookie-policy, copyright, editorial-policy)
- ✅0 broken links,0 orphan indexable pages
- ✅0 duplicate titles,0 duplicate meta descriptions
- ✅1006 indexable pages in sitemap
- ✅18 published languages (17 AdSense-supported)
- ✅10 Indian languages with29 topic guides each
- ✅ AdSense loader on504 pages (HIGH_CONTENT + MEDIUM_CONTENT)
- ✅ Runtime flags OFF (correct — approval pending)
- ✅ All tests green (build-all.py, test-ad-policy, test-voice, test-retention, etc.)
- ✅ Unified learn/ hub with all languages
- ✅ Googlebot parity test passes (no cloaking)
### What NEEDS FIXING:
- ⚠️237 repeated paragraph groups (UI boilerplate shared across pages)
- ⚠️ Some languages only have A1-B2 (need C1-C2 or clear "coming soon" marking)
- ⚠️ Content depth per language varies — some have fewer lessons
- ⚠️ Voice integration needs to be verified for all languages
- ⚠️ Blog-style readable content is thin — need more human-readable guides
- ⚠️ Per-language level pages (Beginner/Elementary/Intermediate/Advanced) need content parity with Hindi
---
## PART C — MASTER FIX COMMANDS (paste one per Arena session)
---
### PHASE1: CONTENT DEPTH — EVERY LANGUAGE GETS FULL LEVELS
**ROLE:** Senior curriculum designer + content architect
**MODEL HINT:** strong writing model
```
ROLE: Tum CEFR-aligned senior curriculum designer ho. Repo EkGuruLearning/EkGuru.
Goal: Har published language ke liye A1-C2 levels complete karo ya clearly mark karo.
CONTEXT:
- Currently18 languages have published courses
- Hindi has the deepest content (A1-C2,34 topic guides)
- Other languages have A1-B2 or A1-C2 but content depth varies
- Google AdSense rejects sites with "thin content" — har language ke level page pe
  substantial, unique content hona chahiye
KAAM:
1. Har language ke liye jo levels missing hain unko build karo:
   python3 tools/build-course-levels.py
   
2. Har level page pe minimum yeh content hona chahiye:
   - Language-specific introduction (150+ unique words, NOT templated)
   - Real vocabulary with native script + romanisation + IPA
   - Grammar explanation with language-specific examples
   - Dialogue with cultural context
   - Practice exercises (minimum10 items)
   - Quiz with feedback
   - Voice tags for pronunciation
3. Level labels jo Hindi mein hain woh har language mein hone chahiye:
   🌱 Beginner (A1-A2) — script, first words, simple sentences
   🌿 Elementary (A2-B1) — real conversation, tenses, register
   🌳 Intermediate (B1-B2) — politeness, verb tenses, mistakes, culture
   🚀 Advanced (C1-C2) — real topics: clinic, office, school, weather, home, festivals
4. Har level page ka opening paragraph UNIQUE hona chahiye:
   - Language name + script mention
   - Specific cultural reference (e.g., Arabic→right-to-left, Japanese→particles)
   - Real example from that language
   - NOT copy-paste from another language's page
5. Verify:
   python3 tools/build-all.py check
   python3 tools/audit-adsense-readiness.py
GATES:
- build-all.py check green
- Har language ke liye kam se kam A1-B2 levels published
- Har level page pe minimum500 words of unique content
- Voice tags present for all vocabulary items
- No templated intros — har page ka opening alag
ACCEPTANCE REPORT: per-language level counts, word counts, voice tag coverage.
```
---
### PHASE2: INDIAN LANGUAGE CONTENT PARITY (hindi jaisa content har language mein)
**ROLE:** Indian language curriculum specialist
**MODEL HINT:** strong writing model
```
ROLE: Tum Indian language curriculum specialist ho. Repo EkGuruLearning/EkGuru.
Goal: Hindi mein jitna content hai utna hi content har Indian language mein hona chahiye.
CONTEXT:
- Hindi has34 topic guides (alphabet, greetings, numbers, family, grammar, etc.)
- Other Indian languages (bengali, gujarati, marathi, punjabi, tamil, telugu, urdu, kannada, malayalam)
  have18 topic dirs each
- Each topic dir has sub-pages (basics, beginner, intermediate, advanced, etc.)
- Google wants substantial, unique content per language
KAAM:
1. Har Indian language ke liye missing topics add karo:
   - Alphabet/script guide (with stroke order, pronunciation)
   - Numbers1-100 (with native script)
   - Greetings (with cultural context)
   - Family words (with regional variations)
   - Grammar basics (sentence structure, verb forms)
   - Travel phrases (with real scenarios)
   - Business vocabulary
   - Cinema/entertainment (Bollywood for Hindi, Kollywood for Tamil, Tollywood for Telugu, etc.)
   - Common mistakes (specific to that language)
   - Formal vs informal register
2. Har topic page pe minimum yeh content:
   - Introduction paragraph (language-specific, NOT templated)
   - Real vocabulary with native script + romanisation
   - Cultural context (e.g., Tamil→Dravidian roots, Urdu→Nastaliq script)
   - Common mistakes section
   - Practice exercises
   - Voice buttons for pronunciation
3. Level-based content (Beginner/Elementary/Intermediate/Advanced):
   🌱 Beginner — script, first words, simple sentences
   🌿 Elementary — real conversation, tenses, register
   🌳 Intermediate — politeness, verb tenses, mistakes, culture
   🚀 Advanced — real topics: clinic, office, school, weather, home, festivals
4. Verify:
   python3 tools/build-all.py check
GATES:
- Har Indian language ke liye minimum29 topic directories
- Har topic page pe minimum400 words of unique content
- Voice tags present
- No templated intros
ACCEPTANCE REPORT: per-language topic counts, word counts, voice coverage.
```
---
### PHASE3: BLOG-STYLE READABLE CONTENT (learn tab ke liye)
**ROLE:** Content writer + education blogger
**MODEL HINT:** strong writing model
```
ROLE: Tum education blogger ho jo language learning content likhta hai.
Repo EkGuruLearning/EkGuru.
Goal: Learn tab ke liye blog-style readable content banao jo padhne mein easy ho.
CONTEXT:
- Google AdSense reviewers manually check content quality
- Blog-style content with headings, paragraphs, examples is preferred
- Content should be conversational, not robotic
- Each article should answer a specific question or solve a specific problem
KAAM:
1. Har language ke liye yeh blog posts likho (minimum1000 words each):
   - "How to learn [Language] from scratch — a complete beginner's guide"
   - "[Language] alphabet: every letter explained with examples"
   - "100 most common [Language] words with pronunciation"
   - "[Language] grammar basics: sentence structure explained"
   - "Common mistakes when learning [Language] — and how to avoid them"
   - "[Language] for travel: essential phrases for tourists"
   - "How to read [Language] script — a step-by-step guide"
   - "[Language] vs Hindi: what's different and what's similar"
   - "Best way to practice [Language] speaking alone"
   - "[Language] numbers: counting from1 to100"
2. Blog post structure:
   - Hook paragraph (language-specific, engaging)
   - Clear headings (H2, H3)
   - Real examples with native script + romanisation
   - Cultural context
   - Common mistakes section
   - Practice exercises
   - Links to related pages (internal linking)
3. Writing style:
   - Conversational, not robotic
   - "You" language (not "one should")
   - Real examples from daily life
   - Honest about difficulty level
   - No filler text
4. Place these in: learn/[language]/ directory
5. Verify:
   python3 tools/build-all.py check
GATES:
- Minimum10 blog posts per published language
- Each post minimum1000 words
- Unique content (not templated)
- Proper headings and structure
- Internal links to course pages
ACCEPTANCE REPORT: per-language blog post count, word counts, link structure.
```
---
### PHASE4: VOICE INTEGRATION — EVERY LANGUAGE
**ROLE:** Speech/audio engineer
**MODEL HINT:** strong coding model
```
ROLE: Tum language-learning apps ke speech/audio engineer ho.
Repo EkGuruLearning/EkGuru.
Goal: Har published language ke liye voice integration complete karo.
CONTEXT:
- Voice.js exists and handles Web Speech API
- Har language ke liye BCP-47 tag chahiye
- Voice buttons vocabulary, dialogues, examples pe hone chahiye
- Browser mein voice nahi hai to honest fallback dikhao
KAAM:
1. Verify har language ka BCP-47 tag:
   python3 -c "import json; reg=json.load(open('data/languages/registry.json')); [print(f'{l[\"code\"]}: {l[\"speech_tag\"]}') for l in reg['languages'] if l.get('course')]"
2. Har level page pe voice buttons add karo:
   - Vocabulary items: 🔊 button per word
   - Dialogue lines: 🔊 button per line
   - Example sentences: 🔊 button
   - Grammar examples: 🔊 button
3. Voice fallback:
   - Agar browser mein voice nahi hai → button disabled + text "Your browser has no [Language] voice"
   - Kabhi galat language ki voice se mat bolao
   - Synthetic voice ko "Synthetic voice" label karo
4. Listening practice:
   - "Listen and choose" items voice.js use karein
   - Voice unavailable to item skip + reason dikhe
5. Verify:
   node tools/test-voice.mjs
GATES:
- test-voice PASS
- Har course language ka BCP-47 tag registry mein
- No autoplay anywhere
- aria-label on every voice button
ACCEPTANCE REPORT: languages with voice, languages with recordings, bundle size.
```
---
### PHASE5: ADSENSE-SPECIFIC FIXES (review se pehle)
**ROLE:** AdSense policy compliance auditor
**MODEL HINT:** strong reasoning model
```
ROLE: Tum Google AdSense policy compliance expert ho.
Repo EkGuruLearning/EkGuru.
Goal: Site ko AdSense review ke liye prepare karo — har possible rejection reason fix karo.
KAAM:
1. Low value content fix:
   python3 tools/audit-adsense-readiness.py
   - Jo pages indexable hain unka content depth check karo
   - Har indexable page pe minimum400 words of unique text
   - Repeated paragraphs jo UI boilerplate hain unke liye:
     * Bylines: already auto-generated, OK
     * Section headers: already language-specific, OK
     * "Coming soon" pages: noindex karo agar content nahi hai
2. Trust pages verify:
   - about/index.html: founder info, mission, team (if any)
   - contact/index.html: working form or mailto
   - privacy/index.html: mentions Google AdSense, cookies
   - terms/index.html: terms of use
   - disclaimer/index.html: content disclaimer
   - cookie-policy/index.html: cookie usage
   - editorial-policy/index.html: how content is created, AI policy
3. Navigation verify:
   - Header links work on all pages
   - Footer links work on all pages
   - Mobile menu works
   - No broken links
4. Content quality:
   - No "Lorem ipsum" anywhere
   - No "TODO" or "[translate]" placeholders
   - No "coming soon" on indexable pages
   - All images have alt text
   - All pages have proper title and description
5. Technical:
   python3 tools/inject-ads.py --check
   node tools/test-ad-policy.mjs
   python3 tools/build-all.py check
GATES:
- audit-adsense-readiness.py: thin_indexable = 0
- inject-ads.py --check: ok
- test-ad-policy: PASS
- build-all.py check: green
- All trust pages present and complete
- No policy violations
ACCEPTANCE REPORT: audit numbers, trust page status, navigation test results.
```
---
### PHASE6: ADD MORE LANGUAGES (traffic + coverage)
**ROLE:** Language expansion specialist
**MODEL HINT:** strong reasoning model
```
ROLE: Tum language expansion specialist ho. Repo EkGuruLearning/EkGuru.
Goal: AdSense-supported languages mein se jo missing hain unko add karo.
CONTEXT:
- AdSense supports these languages: ar, bn, zh, cs, da, nl, en, et, fil, fi, fr, de, el, gu, he, hi, hu, id, it, ja, kn, ko, lv, lt, ms, ml, mr, no, pl, pt, ro, ru, sr, sk, sl, es, sv, ta, te, th, tr, uk, ur, vi
- Currently18 languages published
- Missing high-demand languages: Vietnamese, Thai, Turkish, Indonesian, Polish, Romanian, Swedish, Norwegian, Danish, Czech, Finnish, Greek, Hebrew, Hungarian, Ukrainian, Serbian, Slovak, Slovenian, Lithuanian, Latvian, Estonian, Filipino
KAAM:
1. Top priority languages (by learner demand):
   - Vietnamese (vi) —90M+ speakers
   - Thai (th) —60M+ speakers
   - Turkish (tr) —80M+ speakers
   - Indonesian (id) —270M+ speakers
   - Polish (pl) —45M+ speakers
   - Ukrainian (uk) —40M+ speakers
   - Greek (el) —13M+ speakers
   - Hebrew (he) —9M+ speakers
2. Har nayi language ke liye minimum:
   - A1-A2 levels with lessons
   - Script/alphabet guide
   - Greetings and basic phrases
   - Numbers1-20
   - Common vocabulary (50+ words)
   - Voice tags
3. Build:
   python3 tools/build-course-levels.py
   python3 tools/build-all.py check
GATES:
- New languages added to registry
- A1-A2 levels published
- Voice tags present
- build-all.py check green
ACCEPTANCE REPORT: new language count, level coverage, voice status.
```
---
### PHASE7: FINAL QA + REVIEW SUBMIT
**ROLE:** QA lead + release manager
**MODEL HINT:** strong reasoning model
```
ROLE: Tum QA lead aur release manager ho. Repo EkGuruLearning/EkGuru.
Goal: Final review battery chalao — sab green hone pe owner ko batao ki review submit karo.
KAAM:
1. Full build check:
   python3 tools/build-all.py check
2. AdSense readiness:
   python3 tools/inject-ads.py --check
   node tools/test-ad-policy.mjs
   node tools/test-consent-release.mjs
   python3 tools/audit-adsense-readiness.py
3. Content quality:
   python3 tools/audit-adsense-readiness.py
   - thin_indexable = 0
   - duplicate_title_groups = 0
   - No "coming soon" on indexable pages
4. Navigation:
   python3 tools/build-full-page-inventory.py
   - broken = 0
   - orphan_indexable = 0
5. Voice:
   node tools/test-voice.mjs
6. Retention:
   node tools/test-retention.mjs
7. Googlebot parity:
   node tools/test-googlebot-parity.mjs
8. Live checks (if network available):
   curl -s https://ekguru.shop/ | grep adsbygoogle
   curl -s https://ekguru.shop/ads.txt
   node tools/adsready.js
9. Weekly guard:
   bash tools/weekly-guard.sh
GATES:
- ALL tests green
- build-all.py check green
- audit shows thin_indexable = 0
- All trust pages present
- Voice working for all languages
- No policy violations
ACCEPTANCE REPORT: test results, audit numbers, "READY FOR REVIEW" or "NOT READY".
```
---
## PART D — REJECTION RECOVERY (sirf tab jab Google REJECT kare)
### D-1. "Low Value Content" Rejection
**Fix:**
1. python3 tools/audit-adsense-readiness.py
2. Har indexable page pe minimum600 words of unique content
3. Repeated paragraphs ko unique banao (D-24 pattern se)
4. Thin pages ko noindex karo
5.15-20 naye deep articles publish karo (1500+ words each)
6.2 hafte wait karo, phir review submit karo
### D-2. "Insufficient Content" Rejection
**Fix:**
1. Har language ke liye minimum A1-B2 levels complete karo
2. Har topic page pe minimum400 words
3. Blog posts add karo (10+ per language,1000+ words each)
4.4 hafte wait karo, phir review submit karo
### D-3. "Policy Violation" Rejection
**Fix:**
1. Rejection email mein jo URLs listed hain unko check karo
2. Offending content remove/rewrite karo
3. Affiliate disclosure check karo
4.2 hafte wait karo, phir review submit karo
### D-4. "Under Construction" Rejection
**Fix:**
1. Sab "coming soon" pages ko noindex karo
2. Empty categories ko remove ya noindex karo
3. Placeholder pages ko complete ya delete karo
4.1 hafte wait karo, phir review submit karo
---
## PART E — PASTE INDEX
| Situation | Kya paste karna |
|---|---|
| Content depth | PHASE1 |
| Indian language parity | PHASE2 |
| Blog content | PHASE3 |
| Voice integration | PHASE4 |
| AdSense fixes | PHASE5 |
| More languages | PHASE6 |
| Final QA | PHASE7 |
| Rejected | PART D |
---
## PART F — GOLDEN RULES (kabhi na tootey)
1. Googlebot aur insaan ko bilkul same content dikhao (R-1)
2. Koi page tab tak index nahi hoga jab tak uske paas apna asli content na ho (R-2)
3. "Native tutor", "verified", "certified" — sirf tab jab data mein proof ho (R-3)
4. Ad loader sirf policy gate se lagega (R-4)
5. Generated page ko haath se edit nahi karna — generator badlo (R-5)
6. Merge sirf CI green par (R-6)
7. Noindex / domain / canonical status bina owner ki permission ke mat badlo (R-7)
8. Har page: LCP ≤2.5s, CLS ≤0.1, INP ≤200ms (R-8)
9. WCAG2.2 AA: contrast, keyboard, focus ring, alt text (R-9)
10. Har phase ka apna test (R-10)

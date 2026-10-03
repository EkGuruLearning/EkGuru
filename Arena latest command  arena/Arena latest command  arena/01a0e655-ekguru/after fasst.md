# EKGURU — PHASES 8-20: DEEP EXPANSION COMMANDS
### Every country, every language, every tool, every feature — word to word
### Date: 2 October 2026 · Repo: EkGuruLearning/EkGuru
---
## PHASE8: EVERY COUNTRY LANGUAGE EXPANSION (700+ languages, big scale)
**ROLE:** Language expansion architect + computational linguist
**MODEL HINT:** strong reasoning model
```
ROLE: Tum language expansion architect ho. Repo EkGuruLearning/EkGuru.
Goal: Har UN member country ki primary language + major minority languages add karo.
Scale:700+ languages,3 tiers (T1 full, T2 starter, T3 reference).
CONTEXT:
- Registry mein700 languages hain (data/languages/registry.json)
- Currently18 published,71 research required
- Google AdSense supports44 languages
- Har language ke liye minimum A1-A2 levels chahiye AdSense approval ke liye
KAAM:
1. Priority order mein languages add karo:
   WAVE 1 — Top20 AdSense-supported languages (traffic potential):
   Vietnamese (vi), Thai (th), Turkish (tr), Indonesian (id), Polish (pl),
   Ukrainian (uk), Greek (el), Hebrew (he), Hungarian (hu), Czech (cs),
   Romanian (ro), Swedish (sv), Norwegian (no), Danish (da), Finnish (fi),
   Slovak (sk), Slovenian (sl), Lithuanian (lt), Latvian (lv), Estonian (et)
   WAVE 2 — High-demand languages:
   Swahili (sw), Tagalog/Filipino (fil), Malay (ms), Persian (fa),
   Nepali (npi), Sinhala (si), Khmer (km), Lao (lo), Burmese (my),
   Georgian (ka), Armenian (hy), Azerbaijani (az), Kazakh (kk),
   Uzbek (uzn), Mongolian (mn), Tibetan (bo)
   WAVE 3 — Regional languages (India + neighbors):
   Assamese, Odia, Sindhi, Konkani, Maithili, Dogri, Kashmiri,
   Santali, Bodo, Manipuri (Meitei), Nepali, Sinhala, Dhivehi
   WAVE 4 — African languages:
   Yoruba (yo), Igbo (ig), Hausa (ha), Zulu (zu), Xhosa (xh),
   Amharic (am), Somali (so), Oromo, Tigrinya, Kinyarwanda (rw),
   Lingala, Wolof, Twi, Akan, Shona
   WAVE 5 — European minority + less common:
   Basque (eu), Catalan (ca), Galician, Welsh (cy), Irish (ga),
   Scottish Gaelic, Icelandic (is), Maltese (mt), Luxembourgish,
   Faroese, Sami languages, Breton, Corsican, Sardinian
2. Har nayi language ke liye minimum content:
   - A1 level: Greetings, numbers1-20, basic vocabulary (50 words),
     self-introduction, alphabet/script guide
   - A2 level: Simple sentences, common phrases, basic grammar,
     travel vocabulary, food vocabulary
   - Voice tags for all vocabulary
   - Cultural context paragraph (language-specific)
   - Script/alphabet page with native characters
3. Har language ka page structure:
   languages/[code]/index.html — language hub
   languages/[code]/level/a1/index.html — A1 level
   languages/[code]/level/a2/index.html — A2 level
   languages/[code]/lessons/greetings-and-introductions/index.html
   languages/[code]/lessons/numbers-1-to-20/index.html
   languages/[code]/lessons/basic-sentences/index.html
   languages/[code]/course/index.html — course overview
4. Build tools:
   python3 tools/build-course-levels.py
   python3 tools/build-language-registry.py
   python3 tools/build-all.py check
5. Quality gate:
   python3 tools/language-gate.py
   - Har language ka content unique hona chahiye (85%+ unique text)
   - Script Unicode ranges sahi hone chahiye
   - Romanisation present for non-Latin scripts
   - No placeholder text
GATES:
- WAVE 1:20 languages with A1-A2 levels published
- WAVE 2:16 languages with A1 level published
- build-all.py check green
- language-gate PASS for new languages
- Voice tags present for all vocabulary
- Hreflang tags correct for all language pairs
ACCEPTANCE REPORT: per-wave language count, level coverage, voice status,
unique content percentage, gate results.
```
---
## PHASE9: INTERACTIVE TOOLS (flashcards, quizzes, worksheets, practice)
**ROLE:** Interactive learning tools engineer
**MODEL HINT:** strong coding model
```
ROLE: Tum interactive learning tools engineer ho. Repo EkGuruLearning/EkGuru.
Goal: Har language ke liye interactive tools banao — flashcards, quizzes,
worksheets, practice exercises, typing practice, pronunciation practice.
CONTEXT:
- Existing tools: toolbox/ directory (alphabet explorer, numbers, flashcards, quiz, typing)
- js/retention.js — SRS system exists
- js/voice.js — voice system exists
- js/adaptive-practice.js — practice system exists
- But these are Hindi-focused. Har language ke liye chahiye.
KAAM:
1. FLASHCARD SYSTEM (per language):
   - data/flashcards/[code].json — vocabulary deck for each language
   - Front: native script word
   - Back: romanisation + English translation + pronunciation
   - SRS scheduling (already in js/retention.js)
   - Categories: greetings, numbers, food, travel, family, body, colors, verbs
   - Minimum200 cards per published language
   - Flip animation (CSS3, prefers-reduced-motion support)
   - Progress tracking (localStorage)
2. QUIZ SYSTEM (per language, per level):
   - Multiple choice (4 options)
   - Fill in the blank
   - Match pairs (word ↔ meaning)
   - Reorder sentence (drag and drop)
   - Listening comprehension (hear → choose)
   - Reading comprehension (passage → questions)
   - Minimum20 quiz items per level per language
   - Immediate feedback with explanation
   - Score tracking
3. WORKSHEETS (printable, per language):
   - Alphabet/script practice sheet (trace and write)
   - Vocabulary lists (with checkboxes)
   - Grammar reference tables
   - Verb conjugation charts
   - Number practice sheets
   - Dialogue scripts (for reading aloud)
   - PDF format, print-ready
   - data/worksheets/[code]/ directory
4. PRACTICE EXERCISES (interactive):
   - Sentence builder (drag words into correct order)
   - Gap fill (type the missing word)
   - Pronunciation practice (SpeechRecognition)
   - Listening dictation (hear → type)
   - Reading aloud (voice.js + score)
   - Conversation practice (chatbot-style)
   - Minimum10 exercises per topic per language
5. TYPING PRACTICE (per script):
   - Devanagari typing (Hindi, Marathi, Sanskrit)
   - Arabic typing (Arabic, Urdu, Persian)
   - CJK typing (Chinese, Japanese, Korean)
   - Cyrillic typing (Russian, Ukrainian, Bulgarian)
   - Thai typing
   - Virtual keyboard with key mapping
   - Speed test (WPM tracking)
6. FLASHCARD DECK BUILDER:
   - User can create custom decks
   - Import from vocabulary lists
   - Export to Anki format (.apkg)
   - Share decks via URL
7. Build:
   python3 tools/build-flashcards.py
   python3 tools/build-worksheets.py
   python3 tools/build-practice.py
   python3 tools/build-all.py check
GATES:
- Har published language ke liye minimum:
  -200 flashcards
  -20 quiz items per level
  -5 worksheets
  -10 practice exercises
- SRS scheduling works correctly
- Print-ready worksheets
- Voice integration on all interactive elements
- build-all.py check green
ACCEPTANCE REPORT: per-language tool counts, flashcard deck sizes,
quiz item counts, worksheet counts, practice exercise counts.
```
---
## PHASE10: VISUALS, THEMES & ANIMATION (per language, per culture)
**ROLE:** Visual design + animation engineer
**MODEL HINT:** strong frontend model
```
ROLE: Tum visual design aur animation engineer ho. Repo EkGuruLearning/EkGuru.
Goal: Har language ke liye unique visual identity banao — themes, colors,
patterns, animations, illustrations, OG images.
CONTEXT:
- css/tokens.css — design tokens exist
- css/themes/[code].css — per-language themes exist (90 themes)
- tools/build-themes.py — theme generator exists
- tools/test-theme-contrast.mjs — contrast test exists
- But themes need more cultural depth and unique visuals
KAAM:
1. CULTURAL THEMES (per language):
   - data/themes/[code].json — theme definition
   - accent: language-specific color (e.g., Hindi→saffron, Arabic→green)
   - pattern: SVG pattern inspired by culture
     * Hindi→rangoli/jaali pattern
     * Arabic→geometric Islamic pattern
     * Japanese→sakura/wave pattern
     * Chinese→cloud/dragon pattern
     * Korean→hanbok pattern
     * French→fleur-de-lis pattern
     * Spanish→azulejo pattern
     * Russian→khokhloma pattern
     * Thai→lotus/kranok pattern
     * Turkish→tulip/Ebru pattern
   - font stack: script-appropriate fonts (self-hosted Noto family)
   - line-height: script-specific (Devanagari needs more, CJK needs more)
   - direction: rtl for Arabic, Hebrew, Urdu, Persian, Pashto
2. ILLUSTRATIONS (per lesson, per language):
   - SVG illustrations for key lessons
   - Market scene, family tree, clock, map, food table
   - Generated from data (tools/build-visuals.py)
   - Alt text specific to content
   - Dark mode aware via CSS variables
   - ≤20 KB per SVG
   - Lazy loading
3. OG IMAGES (per page, per language):
   -1200×630 PNG for social sharing
   - Generated at build time (SVG→PNG via resvg)
   - Unique per language/level
   - Language name + level + script sample
   - tools/build-og-images.py
4. ANIMATIONS:
   - Reveal on scroll (IntersectionObserver)
   - Card lift on hover
   - Progress ring animation
   - Streak flame animation
   - Level-up confetti (canvas,1.5s, click to dismiss)
   - Stroke-order animation for letters (SVG path dash-offset)
   - Flashcard flip animation (3D CSS transform)
   - Quiz answer feedback animation (correct=green pulse, wrong=red shake)
   - Loading skeleton animation
   - ALL respect prefers-reduced-motion: reduce
5. ICON SYSTEM:
   - Per-language script icons (Devanagari, Arabic, CJK, Cyrillic, etc.)
   - Level icons (🌱🌿🌳🚀)
   - Tool icons (flashcard, quiz, worksheet, practice, voice)
   - Status icons (complete, in-progress, locked, coming-soon)
   - SVG sprite sheet
6. RESPONSIVE DESIGN:
   - Mobile-first (320px minimum)
   - Tablet (768px breakpoint)
   - Desktop (1024px breakpoint)
   - Large desktop (1440px breakpoint)
   - Print styles (hide navigation, show content)
7. Build:
   python3 tools/build-themes.py
   python3 tools/build-visuals.py
   python3 tools/build-og-images.py
   python3 tools/build-all.py check
   node tools/test-theme-contrast.mjs
GATES:
- Har published language ka unique theme
- All SVGs have alt text
- Total image weight per page ≤300 KB
- All animations respect prefers-reduced-motion
- OG images generated for all published pages
- Contrast test PASS for all themes
- build-all.py check green
ACCEPTANCE REPORT: theme count, illustration count, OG image count,
animation list, bundle sizes, contrast test results.
```
---
## PHASE11: VOICE SYSTEM PERFECTION (every language, every feature)
**ROLE:** Speech/audio engineer for language learning
**MODEL HINT:** strong coding model
```
ROLE: Tum language-learning apps ke speech/audio engineer ho.
Repo EkGuruLearning/EkGuru.
Goal: Voice system ko perfect banao — har language, har feature working.
CONTEXT:
- js/voice.js (≤10 KB) exists — Web Speech API speechSynthesis
- js/voice-languages.js — language tag registry
- data/audio-manifest/[code].json — pre-recorded audio manifests
- test-voice.mjs — voice test suite (26/26 pass)
- But need to verify and expand for ALL languages
KAAM:
1. VOICE TAG REGISTRY (verify all languages):
   - Har published language ka BCP-47 tag verify karo:
     * Hindi: hi-IN ✅
     * Bengali: bn-IN ✅
     * Gujarati: gu-IN ✅
     * Marathi: mr-IN ✅
     * Punjabi: pa-IN ✅
     * Tamil: ta-IN ✅
     * Telugu: te-IN ✅
     * Urdu: ur-PK ✅
     * Arabic: ar-SA ✅
     * French: fr-FR ✅
     * German: de-DE ✅
     * Spanish: es-ES ✅
     * Italian: it-IT ✅
     * Japanese: ja-JP ✅
     * Korean: ko-KR ✅
     * Portuguese: pt-BR ✅
     * Russian: ru-RU ✅
     * Mandarin: zh-CN ✅
     + New languages from Phase8
2. VOICE BUTTONS (on every page):
   - Vocabulary items: 🔊 button per word
   - Dialogue lines: 🔊 button per line
   - Example sentences: 🔊 button
   - Grammar examples: 🔊 button
   - Alphabet letters: 🔊 button
   - Numbers: 🔊 button
   - Keyboard accessible (Enter/Space to activate)
   - aria-label: "Play [word] in [Language]"
   - Speed control:0.6x /0.8x /1x
   - Slow and Repeat buttons
3. HONEST FALLBACK:
   - Agar browser mein voice nahi hai:
     * Button disabled
     * Text: "Your browser has no [Language] voice. Romanisation is shown instead."
     * Kabhi galat language ki voice se mat bolao
   - Voice picker: browser mein jo voices hain unki list
   - User choice localStorage mein save
4. PRE-RECORDED AUDIO (optional, better quality):
   - data/audio-manifest/[code].json
   - Agar kisi word ka human recording ho to woh pehle chale
   - Label: "Recorded by [name]"
   - Synthetic ho to label: "Synthetic voice"
   - Kabhi synthetic ko human mat batao (R-3)
5. LISTENING PRACTICE:
   - "Listen and choose" items
   - "Dictation" items (hear → type)
   - Voice unavailable to item skip + reason
6. SPEAKING PRACTICE:
   - SpeechRecognition (jahan supported)
   - "We heard: …" transcript
   - Score nahi dikhana jab tak reliable na ho
   - Microphone permission sirf button click par
7. STROKE ORDER ANIMATION:
   - SVG path dash-offset animation
   - Har letter ka stroke order dikhao
   - Speed control
   - Replay button
   - Devanagari, Arabic, CJK, Cyrillic scripts
8. Build:
   node tools/build-runtime.mjs
   python3 tools/build-all.py check
   node tools/test-voice.mjs
GATES:
- test-voice PASS (26/26+)
- Har course language ka BCP-47 tag registry mein
- No autoplay anywhere
- Voice buttons on all vocabulary, dialogues, examples
- Keyboard accessible
- Stroke order animation for all scripts
- Fallback working for unsupported languages
- build-all.py check green
ACCEPTANCE REPORT: languages with browser voice, languages with recordings,
voice button coverage, stroke order animation count, bundle size.
```
---
## PHASE12: SEO ARCHITECTURE (every language, every page)
**ROLE:** Technical + international SEO lead
**MODEL HINT:** strong reasoning model
```
ROLE: Tum technical aur international SEO lead ho. Repo EkGuruLearning/EkGuru.
Goal: "learn [language]" search mein EkGuru ka page aaye — har language ke liye.
CONTEXT:
- Site structure: /languages/[code]/ (hub) → /level/[lvl]/ → lesson anchors
- /learn/[lang]/ — topic guides
- /learn-hindi-from-[country]/ — country pages
- Hreflang tags on all pages
- Sitemaps generated by tools/build-sitemaps.py
KAAM:
1. KEYWORD RESEARCH (per language):
   - "learn [language]" — main keyword
   - "[language] alphabet" — high volume
   - "[language] for beginners" — high volume
   - "[language] greetings" — medium volume
   - "[language] numbers" — medium volume
   - "[language] grammar" — medium volume
   - "how to say [phrase] in [language]" — long-tail
   - "[language] vs [other language]" — comparison
   - Har language ke liye alag keyword research
   - data/seo/keywords/[code].json
2. ON-PAGE SEO (per page):
   - Title: unique, ≤60 chars, keyword in beginning
   - Meta description: unique, ≤155 chars, compelling
   - H1: one per page, keyword included
   - H2/H3: structured headings with keywords
   - Image alt text: descriptive, keyword-relevant
   - Internal links: minimum3 per page
   - External links: to authoritative sources (if relevant)
   - URL slug: short, descriptive, keyword-rich
3. STRUCTURED DATA (per page type):
   - Course + CourseInstance (free, online)
   - LearningResource
   - BreadcrumbList
   - FAQPage (visible FAQ ke hi sawal)
   - QAPage (ask/)
   - DefinedTerm for vocab
   - Organization + founder Person
   - Article (for blog posts)
   - HowTo (for tutorials)
   - VideoObject (for video lessons, future)
4. HREFLANG (per language):
   - Har page pe hreflang tags for all language versions
   - x-default = English
   - Reciprocal hreflang (A→B, B→A)
   - Correct ISO codes (not country codes)
   - Self-referencing hreflang
5. SITEMAPS (per content type):
   - sitemap-index.xml — master index
   - sitemap-learn.xml — learn pages
   - sitemap-languages.xml — language course pages
   - sitemap-blog.xml — blog posts
   - sitemap-tools.xml — tool pages
   - sitemap-[code].xml — per-language sitemaps
   - Lastmod: only on content change
   - Noindex pages NOT in sitemap
6. INTERNAL LINKING (per section):
   - Hub pages link to all child pages
   - Child pages link back to hub
   - Cross-links between related topics
   - Breadcrumbs on all pages
   - "Related lessons" section
   - "Next lesson" / "Previous lesson" navigation
   - Orphan pages = 0
7. BLOG CONTENT (SEO traffic magnet):
   - Per language, minimum10 blog posts:
     * "How to learn [Language] — complete beginner's guide"
     * "[Language] alphabet explained"
     * "100 most common [Language] words"
     * "[Language] grammar basics"
     * "Common mistakes in [Language]"
     * "[Language] for travel"
     * "How to read [Language] script"
     * "[Language] vs Hindi — differences"
     * "Best way to practice [Language] speaking"
     * "[Language] numbers1-100"
   - Each post:1000+ words, proper H2/H3, images, internal links
   - SEO-optimized title and meta description
   - FAQ section at end (for featured snippets)
8. CORE WEB VITALS:
   - LCP ≤2.5s (mobile)
   - CLS ≤0.1
   - INP ≤200ms
   - JS per page ≤150 KB gzip
   - web-vitals.js (≤2 KB) for field data
9. Build:
   python3 tools/build-sitemaps.py
   python3 tools/build-full-page-inventory.py
   python3 tools/build-all.py check
GATES:
- seocheck PASS
- Rich Results sample0 errors
- Orphan pages0
- Duplicate titles/meta0
- Hreflang reciprocity100%
- Sitemap URLs match disk files
- Blog posts: minimum10 per published language
- Core Web Vitals within budget
ACCEPTANCE REPORT: indexable page count by type, schema coverage,
hreflang pairs, blog post count, CWV scores, sitemap counts.
```
---
## PHASE13: TRAFFIC GENERATION (SEO + content marketing + social)
**ROLE:** Growth hacker + content marketer
**MODEL HINT:** strong reasoning model
```
ROLE: Tum growth hacker aur content marketer ho. Repo EkGuruLearning/EkGuru.
Goal: Site pe organic traffic lao — AdSense approval ke liye minimum50-100
daily visitors chahiye, aur earning ke liye zyada.
CONTEXT:
- Site has2643 pages but needs organic traffic
- Blog posts are the primary traffic magnet
- Multilingual SEO = rank in multiple languages
- Social media + community = secondary traffic sources
KAAM:
1. BLOG CONTENT STRATEGY (per language):
   - Har published language ke liye20 blog posts (1000+ words each)
   - Target long-tail keywords:
     * "how to learn [language] from scratch"
     * "[language] alphabet for beginners"
     * "100 most common [language] words with pronunciation"
     * "[language] grammar explained simply"
     * "common mistakes when learning [language]"
     * "[language] for travel — essential phrases"
     * "how to read [language] script"
     * "[language] vs [related language] — what's different"
     * "best way to practice [language] speaking alone"
     * "[language] numbers counting guide"
     * "[language] greetings and introductions"
     * "[language] food vocabulary"
     * "[language] family words"
     * "[language] verb conjugation basics"
     * "[language] sentence structure"
     * "[language] pronunciation guide"
     * "[language] typing — how to type in [script]"
     * "[language] movies for learning"
     * "[language] music for learning"
     * "is [language] hard to learn"
   - Blog post structure:
     * SEO title (≤60 chars, keyword in beginning)
     * Meta description (≤155 chars, compelling)
     * H1 with keyword
     * Introduction paragraph (hook + what reader will learn)
     * H2 sections with keywords
     * Real examples with native script + romanisation
     * Images with alt text
     * Internal links to course pages
     * FAQ section (for featured snippets)
     * Related posts section
     * Author byline
2. MULTILINGUAL SEO (per language):
   - Har language ke liye localized keywords
   - Don't just translate keywords — research what people actually search
   - data/seo/keywords/[code].json
   - Localized meta titles and descriptions
   - Hreflang tags for all language versions
   - Language-specific sitemaps
3. CONTENT CLUSTERS (topical authority):
   - Hindi learning cluster:30+ articles around "learn Hindi"
   - Arabic learning cluster:20+ articles around "learn Arabic"
   - French learning cluster:20+ articles around "learn French"
   - Spanish learning cluster:20+ articles around "learn Spanish"
   - Japanese learning cluster:20+ articles around "learn Japanese"
   - etc. for all published languages
   - Internal linking within clusters
4. SOCIAL MEDIA PRESENCE:
   - YouTube channel: language learning videos (future)
   - Pinterest: infographics, vocabulary cards
   - Twitter/X: daily vocabulary, language facts
   - Instagram: visual vocabulary cards
   - Reddit: r/languagelearning, r/Hindi, etc. (helpful answers, not spam)
   - data/social/ directory with templates
5. COMMUNITY ENGAGEMENT:
   - Quora answers about language learning
   - Stack Exchange answers
   - Language learning forums
   - Guest posts on language blogs
   - Collaborations with language YouTubers
6. INTERNAL LINKING STRATEGY:
   - Hub pages link to all child pages
   - Blog posts link to relevant course pages
   - Course pages link to related blog posts
   - "Related lessons" on every page
   - "Popular articles" section
   - Breadcrumbs everywhere
7. SEARCH CONSOLE OPTIMIZATION:
   - Submit all sitemaps
   - Monitor coverage errors
   - Fix crawl errors
   - Track keyword rankings
   - Optimize for featured snippets
   - docs/gsc-setup.md for owner
8. Build:
   python3 tools/build-all.py check
GATES:
- Blog posts: minimum20 per published language
- Internal links: minimum3 per page
- Hreflang: correct for all language pairs
- Sitemaps: all published pages included
- No orphan pages
- Featured snippet optimization
ACCEPTANCE REPORT: blog post count, keyword targets, internal link count,
sitemap coverage, social media templates.
```
---
## PHASE14: WORKSHEETS & PRINTABLES (per language, per level)
**ROLE:** Educational materials designer
**MODEL HINT:** strong writing model
```
ROLE: Tum educational materials designer ho. Repo EkGuruLearning/EkGuru.
Goal: Har language ke liye printable worksheets banao — practice, review, reference.
CONTEXT:
- materials/ directory exists with some Hindi worksheets
- Need to expand to ALL languages
- Worksheets should be print-ready (A4, clean layout)
KAAM:
1. WORKSHEET TYPES (per language):
   a) ALPHABET/SCRIPT PRACTICE:
   - Trace and write letters
   - Letter recognition (match letter to sound)
   - Stroke order guide
   - Common letter combinations
   - data/worksheets/[code]/alphabet.pdf
   b) VOCABULARY LISTS:
   - Top100 words with checkboxes
   - Categorized: greetings, numbers, food, family, body, colors, verbs, adjectives
   - Native script + romanisation + English
   - Space for user's own notes
   - data/worksheets/[code]/vocabulary-[category].pdf
   c) GRAMMAR REFERENCE:
   - Verb conjugation tables
   - Noun gender/case tables
   - Sentence structure patterns
   - Common grammatical patterns
   - data/worksheets/[code]/grammar-reference.pdf
   d) DIALOGUE SCRIPTS:
   - Lesson dialogues in script form
   - Speaker A / Speaker B format
   - Translation below each line
   - Pronunciation guide
   - data/worksheets/[code]/dialogues.pdf
   e) NUMBER PRACTICE:
   - Number writing practice
   - Math problems in target language
   - Phone number reading practice
   - Date and time practice
   - data/worksheets/[code]/numbers.pdf
   f) SENTENCE BUILDING:
   - Word order exercises
   - Fill-in-the-blank
   - Sentence translation exercises
   - data/worksheets/[code]/sentences.pdf
   g) CULTURAL NOTES:
   - Cultural etiquette guide
   - Common gestures and meanings
   - Festival and holiday vocabulary
   - Food and dining vocabulary
   - data/worksheets/[code]/culture.pdf
2. WORKSHEET DESIGN:
   - A4 format, print-ready
   - Clean, minimal design
   - Large fonts for handwriting practice
   - Answer key on separate page
   - Brand colors (light theme for printing)
   - QR code linking to online version
   - PDF generated at build time
3. GENERATOR:
   - tools/build-worksheets.py
   - Reads from data/courses/[phase]/[code]_*.json
   - Generates PDF using reportlab or similar
   - data/worksheets/[code]/ directory
4. INTEGRATION:
   - Download links on lesson pages
   - "Print this lesson" button
   - Worksheet index page: materials/[code]/
   - Sitemap entry for worksheet index pages
5. Build:
   python3 tools/build-worksheets.py
   python3 tools/build-all.py check
GATES:
- Har published language ke liye minimum7 worksheet types
- PDF format, print-ready
- Answer keys included
- Download links on lesson pages
- Sitemap entries
- build-all.py check green
ACCEPTANCE REPORT: per-language worksheet count, total PDF count,
file sizes, download link coverage.
```
---
## PHASE15: PROGRESS TRACKING & GAMIFICATION (retention + engagement)
**ROLE:** Learning experience (LX) + product engineer
**MODEL HINT:** strong frontend model
```
ROLE: Tum learning experience designer aur product engineer ho.
Repo EkGuruLearning/EkGuru.
Goal: Learner ko wapas laane ke liye progress tracking, streaks, XP, badges.
CONTEXT:
- js/retention.js — SRS system exists
- js/global-srs.js — global SRS exists
- test-retention.mjs — tests pass (20/20)
- localStorage-based (no account needed)
KAAM:
1. PROGRESS PAGE (/learn/progress/):
   - Per language progress:
     * Words learned (count + percentage)
     * Levels completed
     * Lessons completed
     * Quiz scores (average + best)
     * Time spent learning
     * Accuracy rate
   - Overall stats:
     * Total words learned across all languages
     * Total time spent
     * Current streak
     * Longest streak
     * Total XP earned
   - Visual progress bars
   - Language comparison chart
   - Export/import JSON
2. STREAK SYSTEM:
   - Daily study streak
   - Streak freeze (1 per week)
   - Streak milestones:7,30,100,365 days
   - Streak flame animation
   - "Continue your streak" reminder
3. XP SYSTEM:
   - Complete lesson: +10 XP
   - Complete quiz: +20 XP
   - Perfect quiz score: +50 XP
   - Practice session: +5 XP
   - Flashcard review: +2 XP per card
   - Daily login: +5 XP
   - XP levels: Beginner (0-100), Learner (100-500), Student (500-1000),
     Scholar (1000-5000), Master (5000+)
4. BADGES:
   - "First Steps" — complete first lesson
   - "Alphabet Master" — learn all letters
   - "Vocabulary Builder" — learn100 words
   - "Grammar Guru" — complete all grammar lessons
   - "Polyglot" — study3+ languages
   - "Streak Champion" —30-day streak
   - "Quiz Whiz" —10 perfect quiz scores
   - "Explorer" — visit all language hubs
   - "Voice Master" — use voice feature100 times
   - Badge display on profile
   - Badge animation on unlock
5. DAILY PLAN ("Today" widget):
   -1 lesson to review
   -10 flashcards to review
   -1 listening exercise
   -1 quiz question
   -10-15 minute session
   - Shown on homepage and learn/ page
6. CONTINUE WHERE YOU LEFT OFF:
   - Last visited lesson per language
   - "Continue learning [Language]" button
   - Shown on homepage and language hub pages
7. OFFLINE MODE:
   - Service worker caches visited lessons
   - "Download level for offline" button
   - Offline indicator
   - Sync when back online
8. Build:
   python3 tools/build-all.py check
   node tools/test-retention.mjs
GATES:
- test-retention PASS (20/20+)
- Progress page working
- Streak system functional
- XP system functional
- Badges unlockable
- Daily plan widget
- Continue button working
- Offline mode working
- build-all.py check green
ACCEPTANCE REPORT: feature list, storage keys, badge count,
daily plan items, offline cache size.
```
---
## PHASE16: CONTENT QUALITY DEEP DIVE (per page, per paragraph)
**ROLE:** Content quality auditor + editor
**MODEL HINT:** strong writing model
```
ROLE: Tum content quality auditor aur editor ho. Repo EkGuruLearning/EkGuru.
Goal: Har indexable page ka content Google ki quality standards pass kare.
CONTEXT:
-237 repeated paragraph groups exist (mostly UI boilerplate)
- Some languages have thinner content than Hindi
- Google rejects "low value content" — the #1 rejection reason
- Each page needs1000+ words of unique, helpful content
KAAM:
1. CONTENT AUDIT (per page):
   python3 tools/audit-adsense-readiness.py
   - Har indexable page ka word count check karo
   - Minimum400 words of unique text (not including boilerplate)
   - Pages under400 words: either expand or noindex
2. UNIQUE INTRO PARAGRAPHS (per page):
   - Har page ka opening paragraph UNIQUE hona chahiye
   - NOT copy-paste from another page
   - Language-specific hook
   - Cultural context
   - Real example from that language
   - What reader will learn
3. CONTENT DEPTH (per level page):
   - A1: Script, greetings, numbers, basic vocabulary, simple sentences
   - A2: Everyday conversation, past/future tense, shopping, travel
   - B1: Opinions, stories, news, formal/informal register
   - B2: Complex grammar, idioms, professional language
   - C1: Nuance, register, academic language, literature
   - C2: Near-native fluency, cultural references, humor
4. EXTRA CONTENT (per level — makes pages unique):
   - Culture note (real, sourced)
   - Reading passage (level-appropriate, original)
   - Listening passage (script + voice)
   -10 idioms/expressions (literal + real meaning)
   - Common mistakes (specific to that language)
   - Real-life task ("order food", "write email", "give presentation")
5. HONEST BYLINES:
   - "Written by: [author]" — only when author is recorded
   - "Reviewed by: not yet reviewed by a native speaker" — when true
   - "Updated: [date]" — real date, not rebuild timestamp
   - Editorial policy link
6. NO PLACEHOLDER TEXT:
   - grep -r "lorem ipsum" → 0
   - grep -r "TODO" → 0
   - grep -r "[translate]" → 0
   - grep -r "coming soon" on indexable → 0
   - grep -r "placeholder" → 0
7. Build:
   python3 tools/audit-adsense-readiness.py
   python3 tools/build-all.py check
GATES:
- thin_indexable = 0
- No placeholder text on indexable pages
- Har indexable page ≥400 words unique content
- Unique intro paragraphs (no copy-paste)
- Honest bylines on all pages
- build-all.py check green
ACCEPTANCE REPORT: thin page count, placeholder count,
word count distribution, unique intro coverage.
```
---
## PHASE17: MOBILE-FIRST & PERFORMANCE (Core Web Vitals)
**ROLE:** Frontend performance engineer
**MODEL HINT:** strong frontend model
```
ROLE: Tum frontend performance engineer ho. Repo EkGuruLearning/EkGuru.
Goal: Har page mobile pe fast load ho — LCP ≤2.5s, CLS ≤0.1, INP ≤200ms.
CONTEXT:
- Site is static HTML (GitHub Pages)
- CSS: style.min.css (bundled), tokens.css, ultra.css, themes/*.css
- JS: multiple deferred scripts
- Images: SVG mostly, some PNG
KAAM:
1. PERFORMANCE BUDGET:
   - LCP (Largest Contentful Paint): ≤2.5s mobile
   - CLS (Cumulative Layout Shift): ≤0.1
   - INP (Interaction to Next Paint): ≤200ms
   - JS per page: ≤150 KB gzip
   - CSS per page: ≤100 KB gzip
   - Images per page: ≤300 KB total
2. CSS OPTIMIZATION:
   - Critical CSS inline in <head>
   - Non-critical CSS deferred
   - CSS variables for theming (no duplicate rules)
   - Minimal specificity (flat selectors)
   - No unused CSS (tree-shake)
3. JS OPTIMIZATION:
   - All scripts defer or async
   - No render-blocking JS
   - Code splitting (load per page type)
   - Minimal polyfills
   - Tree-shake unused code
4. IMAGE OPTIMIZATION:
   - SVG inline for icons and illustrations
   - Lazy loading for below-fold images
   - width/height attributes (prevent CLS)
   - WebP format for photos (if any)
   - Responsive images (srcset)
5. FONT OPTIMIZATION:
   - Self-hosted Noto family subsets
   - font-display: swap
   - Subset per script (≤60 KB per script)
   - No Google Fonts CDN (privacy + speed)
6. CACHING:
   - Service worker (network-first for HTML)
   - Cache-first for static assets
   - Build ID in cache name
   - Stale-while-revalidate for CSS
7. WEB VITALS MONITORING:
   - web-vitals.js (≤2 KB) on all pages
   - Send to analytics endpoint (privacy-safe)
   - Monitor LCP, CLS, INP, FCP, TTFB
   - Weekly report
8. Build:
   python3 tools/build-all.py check
GATES:
- LCP ≤2.5s mobile (PageSpeed test)
- CLS ≤0.1
- INP ≤200ms
- JS ≤150 KB gzip
- No render-blocking resources
- All images have width/height
- Font-display: swap on all fonts
ACCEPTANCE REPORT: PageSpeed scores, bundle sizes, CWV metrics.
```
---
## PHASE18: ACCESSIBILITY (WCAG2.2 AA)
**ROLE:** Accessibility engineer
**MODEL HINT:** strong reasoning model
```
ROLE: Tum accessibility engineer ho. Repo EkGuruLearning/EkGuru.
Goal: WCAG2.2 AA compliance — sabke liye accessible.
KAAM:
1. CONTRAST: All text ≥4.5:1 ratio (test-theme-contrast.mjs)
2. KEYBOARD: All interactive elements keyboard accessible
3. FOCUS: Visible focus ring on all focusable elements
4. ALT TEXT: All images have descriptive alt text
5. LANG ATTRIBUTE: Correct lang on all language blocks
6. RTL: dir="rtl" on Arabic, Hebrew, Urdu, Persian, Pashto pages
7. ARIA: Proper ARIA labels on all interactive elements
8. SKIP LINK: "Skip to content" link on all pages
9. FORM LABELS: All form inputs have labels
10. ERROR MESSAGES: Clear, descriptive error messages
11. MOTION: prefers-reduced-motion respected
12. SCREEN READER: All content readable by screen readers
GATES:
- test-theme-contrast PASS (contrast ratios)
- Lighthouse accessibility ≥95
- No missing alt text
- No missing lang attributes
- Keyboard navigation working
- Screen reader compatible
ACCEPTANCE REPORT: contrast test results, Lighthouse scores,
accessibility audit results.
```
---
## PHASE19: MONETIZATION PREPARATION (post-approval)
**ROLE:** Monetization ops engineer
**MODEL HINT:** any
```
ROLE: Tum monetization ops engineer ho. Repo EkGuruLearning/EkGuru.
Goal: AdSense approval ke baad ads enable karo — policy-compliant placement.
CONTEXT:
- js/monetization.js: ADS_RUNTIME_ENABLED = false (wait for approval)
- js/cookie-consent.js: ADVERTISING_AVAILABLE = false (wait for approval)
- data/monetization/google-monetization.json: loader_allowed: ['HIGH_CONTENT', 'MEDIUM_CONTENT']
- inject-ads.py: injects ad loader on eligible pages
KAAM (sirf jab Google APPROVED bole):
1. js/monetization.js:
   var ADS_RUNTIME_ENABLED = false → true
2. js/cookie-consent.js:
   ADVERTISING_AVAILABLE = false → true
3. AdSense dashboard:
   - Auto ads ON (start: "Non-UI recommended/optimized")
   - Formats: "in-page" ON, "anchors" ON, "vignettes" OFF
   - Tune after2 weeks
4. Ad placement rules:
   - HIGH_CONTENT pages: up to3 ad slots
   - MEDIUM_CONTENT pages: up to2 ad slots
   - NEVER on: courses, practice, quiz, test, legal, contact, 404, search, join, booking
   - Never before content
   - Never near buttons/quiz options
   - Mobile: max1 sticky/anchor ad
   - CLS ≤0.1 with ad slots
5. Tests:
   node tools/test-ad-policy.mjs
   node tools/test-consent-release.mjs
   python3 tools/build-all.py check
GATES:
- test-ad-policy PASS
- test-consent-release PASS
- build-all.py check green
- No ads on excluded pages
- CLS ≤0.1
ACCEPTANCE REPORT: test results, ad slot counts, excluded page list.
```
---
## PHASE20: WEEKLY MAINTENANCE & MONITORING (always running)
**ROLE:** Site reliability + content maintenance
**MODEL HINT:** any
```
ROLE: Tum EkGuru ke weekly maintainer ho.
Har hafte yeh karo:
1. GUARD RUN:
   bash tools/weekly-guard.sh
2. COURSE HEALTH:
   python3 tools/course-health.py
3. LANGUAGE GATE:
   python3 tools/language-gate.py
4. CONTENT AUDIT:
   python3 tools/audit-adsense-readiness.py
5. BROKEN LINKS:
   python3 tools/build-full-page-inventory.py
6. SEARCH CONSOLE:
   - Coverage errors check
   - Sitemap status
   - Keyword rankings
   - Owner screenshot bhejega
7. LEARNER ERRORS:
   - Questions API se reported errors
   - Fix and deploy
8. STALE SOURCES:
   - Sources older than12 months update karo
9. SHEET HEALTH:
   - python3 tools/test-data-sources.py
10. OUTPUT:
    - PR "weekly maintenance [date]"
    - CI green
    - Owner ke liye10-line summary:
      * Kya theek hua
      * Kya owner ko karna hai
      * Kya traffic status hai
      * Kya AdSense status hai
```
---
## PASTE INDEX (updated)
| Phase | Kya karna | Agent type |
|---|---|---|
| PHASE8 | Every country language expansion | computational linguist |
| PHASE9 | Interactive tools (flashcards, quizzes, worksheets) | interactive tools engineer |
| PHASE10 | Visuals, themes & animation | visual design engineer |
| PHASE11 | Voice system perfection | speech/audio engineer |
| PHASE12 | SEO architecture | technical SEO lead |
| PHASE13 | Traffic generation | growth hacker |
| PHASE14 | Worksheets & printables | educational materials designer |
| PHASE15 | Progress tracking & gamification | LX engineer |
| PHASE16 | Content quality deep dive | content auditor |
| PHASE17 | Mobile-first & performance | performance engineer |
| PHASE18 | Accessibility | accessibility engineer |
| PHASE19 | Monetization (post-approval) | monetization ops |
| PHASE20 | Weekly maintenance | site reliability |
---
## EXECUTION ORDER
```
PHASE8 (languages) → PHASE12 (SEO) → PHASE13 (traffic)
PHASE9 (tools) → PHASE10 (visuals) → PHASE11 (voice)
PHASE14 (worksheets) → PHASE15 (gamification)
PHASE16 (content quality) → PHASE17 (performance) → PHASE18 (accessibility)
PHASE19 (monetization — only after approval)
PHASE20 (weekly — always)
```
Har phase ek naya Arena session hai. Phase ka command paste karo → agent karega → push karega → next phase.

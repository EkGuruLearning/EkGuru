# EKGURU — ULTRA MASTER COMMAND v3
### (Naye sessions ke liye. Har phase = ek alag naya session = ek specialist agent)
Repo: `EkGuruLearning/EkGuru` · Domain: `https://ekguru.shop` · Publisher: `pub-8175326569491671`
Base: `main` @ `506e6d0` (PR #19 merged) · Likha gaya: 30 Sep 2026
---
## 0. ISE KAISE USE KARNA HAI (sabse pehle padho)
1. **Har phase ek naya Arena session hai.** Phase ka poora block (``` ke andar wala) word-to-word paste karo.
   Ek session mein ek hi phase. Phase khatam → PR → CI green → merge → agla session, agla phase.
2. **Har phase ke upar "ROLE" likha hai.** Woh us agent ki specialist identity hai. Paste karte waqt
   ROLE line bhi paste hoti hai, taaki agent usi expert ki tarah soche.
   Arena har session ke liye model khud chunta hai. Agar aapko model chunne ka option dikhe, to har
   phase ke saath di gayi "MODEL HINT" ke hisaab se chuno (lambi coding/refactor ke liye strong coding
   model, content likhne ke liye strong writing model, design ke liye strong frontend model).
3. **Order strict hai:** U0 → U1 → U2 → U3 → U4 → U5 → U6 → U7 → U8 → U9 → U10. U11 hamesha chalta hai.
   U0 aur U1 ke bina AdSense review submit mat karna.
4. **Har phase ke end mein agent se "ACCEPTANCE REPORT" maango.** Har block ke end mein uska format likha hai.
   Ek bhi gate FAIL = merge nahi.
5. Agent koi cheez "unclear" paaye to ruk kar aapse poochhe. Guess karke publish na kare.
---
## 1. GOLDEN RULES (har phase ke command mein inhe maana hua samjho)
Yeh rules har agent par lagu hain. Inhe todna = AdSense rejection ya Google penalty.
**R-1 · Ek hi page sab ke liye.** Googlebot aur insaan ko bilkul same HTML, same text, same links.
Koi user-agent check, koi "bot ke liye alag content", koi hidden text, koi keyword stuffing,
koi doorway page, koi sneaky redirect nahi. (Cloaking = permanent ban. Yeh rule kabhi nahi tootega.)
**R-2 · Scale se pehle quality.** Koi page tab tak `index` nahi hoga jab tak uske paas apna asli,
us page ke liye specific content na ho. Template se bane pages jinme sirf naam badla ho = `noindex`
+ sitemap se bahar. Machine se bina review likha content publish nahi hoga.
**R-3 · Sach bolo.** "native tutor", "verified", "certified", ratings, reviews, student counts —
sirf tab jab data mein proof ho. AI/synthetic voice ko "synthetic voice" hi likho. Koi fake review nahi.
**R-4 · Ads sirf policy gate se.** Ad loader sirf `data/monetization/google-monetization.json` +
`tools/inject-ads.py` se lagega. Lesson, practice, quiz, test, course player, legal, contact, 404,
search, join, tutor booking pages par kabhi ad nahi. `ADS_RUNTIME_ENABLED` aur
`ADVERTISING_AVAILABLE` approval se pehle `false` hi rahenge.
**R-5 · Generator hi source of truth.** Generated page ko haath se edit nahi karna — generator
badlo, phir build chalao. `python3 tools/build-all.py check` hamesha green.
**R-6 · Merge sirf CI green par.** Rollback hamesha `git revert -m 1 <merge-sha>`.
**R-7 · Noindex / domain / canonical status bina owner ki permission ke mat badlo.**
**R-8 · Performance budget.** Har page: LCP ≤ 2.5s (mobile), CLS ≤ 0.1, INP ≤ 200ms, JS per page
≤ 150 KB gzip, koi animation `prefers-reduced-motion` ko ignore nahi karega.
**R-9 · Accessibility.** WCAG 2.2 AA: contrast, keyboard, focus ring, alt text, `lang` attribute har
language block par, RTL languages (ar, fa, he, ur) mein `dir="rtl"`.
**R-10 · Har phase ka apna test.** Jo naya feature bane, uska automated test bhi usi PR mein bane,
aur `tools/build-all.py check` aur CI mein jude.
---
## 2. SACH — "700 languages" ke baare mein (owner ke liye)
- Duniya mein ~7,000 languages hain; Google aur AdSense ko count nahi, **quality** chahiye.
- Agar 700 languages × 11 levels ke pages ek saath machine se bane, to Google unhe "scaled content
  abuse" maanega aur **poori site** ka approval ruk jayega. Isliye plan 3 tiers mein hai:
| Tier | Kya milega | Index? | Kitni languages |
|---|---|---|---|
| **T1 · Full course** | A1 → C2 + har level par extra content, voice, theme, test | Haan (quality gate pass hone par) | Pehle 40, phir har mahine +10 |
| **T2 · Starter pack** | Script/alphabet, 300 words, 50 phrases, 10 dialogues, voice | Haan (gate pass) | 150 tak |
| **T3 · Language reference** | Country + language facts, script sample, speakers, sources | Sirf jab 400+ unique words aur sources hon | 700+ tak |
- Har language **dhire dhire ek tier upar** jaati hai, sirf jab uska quality gate (U4 mein) pass ho.
- Isse 700+ languages ka lakshya bhi poora hota hai, aur Google approval bhi bachta hai.
---
## 3. PHASES — WORD-TO-WORD COMMANDS
---
### U0 · DATA SOURCE FIX + SAARE TUTORS HIDE (sabse pehle)
**ROLE:** Senior data-pipeline engineer · **MODEL HINT:** strong coding model
```
ROLE: Tum senior data-pipeline engineer ho. Repo EkGuruLearning/EkGuru, base main.
PROBLEM (verified 30 Sep 2026):
- Published Google Sheet "EkGuru DB" ke saare "pub?...&output=csv" links HTTP 500 dete hain
  (Google side). Wahi tabs "output=tsv" se 200 dete hain. pubhtml bhi chalta hai.
- Isliye CI ka step "Data-source tests (network: published Sheet endpoints)" fail hai, aur site
  purane baked data par chal rahi hai.
- Tutors tab (gid=1631273256) mein SAARE tutors active=no hain. Owner ka faisla: abhi koi tutor
  public nahi dikhna chahiye. Jab kisi row mein active=yes hoga, tab hi uski profile dikhe.
KAAM:
1. Ek shared fetch helper banao (browser: js/sheet.js me; build: tools/sheet-fetch.js ya sheetsync
   ke andar; test: tools/test-data-sources.py). Order: pehle output=csv, agar non-200 ya non-csv
   to wahi URL output=tsv ke saath. TSV parser likho jo tab-separated fields, quoted fields aur
   multi-line cells (about, bio, experience, methodology) ko sahi parse kare. Parser ke unit tests
   likho, jinme real tutors-sheet ki ek fixture file ho (tests/fixtures/tutors.tsv — personal
   email/phone hata kar).
2. js/site-config.js ke 4 csvUrl same rahen (backward compatible); fallback helper ke andar ho.
3. tools/test-data-sources.py: LIVE mode me csv FAIL ho aur tsv PASS ho to "PASS (tsv fallback)"
   likhe; dono fail hon to FAIL. Header/schema checks dono formats par chalein.
4. Zero-tutor state ko first-class banao:
   - tools/sheetsync.js: active=no wale sab hidden; hidden list report karo.
   - js/tutors/_registry.js aur jo bhi "reviewed public registry" hai, woh sheet ke active flag ko
     maane. Public tutor = registry me ho AND sheet me active=yes.
   - Jin builders ko khaali list par error aata hai (e.g. build-market-pages.js "the tutor registry
     is empty", build-home-tutors.js, build-tutor-pages.js, build-roster-rows.js, langsync.js),
     unhe 0 tutors par chalna sikhao.
   - 0 tutors par har jagah ek saaf, sach bolne wala empty state: "Abhi koi tutor booking ke liye
     available nahi hai. Free lessons, practice aur courses hamesha khule hain." + links
     (/learn/, /courses/, /daily-hindi/). Yeh text EN + ar/de/es/fr/ja/pt i18n me.
   - Inactive tutor ki profile page: noindex, sitemap-tutors.xml se bahar, feed.xml se bahar,
     llms.txt se bahar, manifest.webmanifest shortcuts se bahar, find-tutors/home/locale pages ke
     cards aur "#tutors" ItemList JSON-LD se bahar, 404.html links se bahar. Booking form band.
   - llms.txt "Facts": "Tutors listed: 0" + price/trial lines hatao jab 0 ho.
   - "Find a tutor" CTA jahan bhi hai (hindi-tutor/<city>, learn-hindi-from-*, answers CTA), 0 tutors
     par use "Start the free course" CTA se badlo — generator se, haath se nahi.
5. Re-activation test: fixture me ek tutor active=yes karo → build → uski profile, card, ItemList,
   sitemap entry wapas aaye. Wapas active=no → sab gayab. Yeh test tools/test-tutor-activation.mjs
   me, CI me jodo.
6. PR #20 (llms.txt 2 tutors) ko close karo — is PR ne use superseded kar diya.
GATES:
- python3 tools/build-all.py check → green
- python3 tools/test-data-sources.py → PASS (tsv fallback)
- node tools/test-tutor-activation.mjs → PASS
- python3 tools/inject-ads.py --check, node tools/test-ad-policy.mjs → green
- node tools/test-tutor-claims.js, node tools/test-no-competitor-attribution.js → green
- CI (ci.yml + playwright) green
ACCEPTANCE REPORT: tutors public count (expected 0), pages jahan se tutor hata, TSV fallback proof
(konsa tab kis format se aaya), naye tests ke naam, CI run link.
```
---
### U1 · ADSENSE + GOOGLE-BOT READINESS AUDIT (honest, no tricks)
**ROLE:** Google Search Quality + AdSense policy auditor · **MODEL HINT:** strong reasoning model
```
ROLE: Tum Google Search Quality Rater guidelines aur AdSense program policies ke expert auditor ho.
Tumhara kaam site ko waisa banana hai jaisa Google ka reviewer aur Googlebot sach me dekhta hai —
koi trick nahi (Golden Rule R-1). Repo EkGuruLearning/EkGuru, base main.
KAAM:
1. Googlebot jaisa render check: har page type ka 1 sample (home, hindi/, learn/<guide>, ask/,
   answers/, daily-hindi/day-N, languages/<code>/, languages/<code>/level/a1, learn-hindi-from-<cc>,
   hindi-tutor/<city>, world-languages/<cc>, toolbox/<tool>, courses/) ko jsdom/Playwright se
   JavaScript OFF aur ON dono me render karo. Main content JS OFF me bhi visible hona chahiye.
   Report: jo content sirf JS se aata hai.
2. "Low value content" checks (AdSense ki sabse common rejection):
   - thin pages (<300 words of own text, chrome ke bina) jo index hain → list + fix plan
   - duplicate/templated paragraphs → tools/audit-adsense-readiness.py + copy-index se list
   - navigation-only pages, "coming soon", placeholder, empty sections → list
   - indexable redirect stubs (jaise languages/index.html jo meta-refresh se /courses/ jaata hai)
     → owner se poochho: noindex+sitemap-out ya 301-style canonical to target.
3. Trust pages: about/, contact/ (working form), privacy/, terms/, disclaimer/, cookie-policy/,
   editorial-policy/ (naya: kaun likhta hai, kaise review hota hai, AI/synthetic voice policy,
   corrections email). Har content page par "Written by / Reviewed by / Updated" line jo sach ho.
4. E-E-A-T: author page(s) — founder ka real profile (already in llms.txt), aur har course ke liye
   "Reviewed by" sirf tab jab real reviewer ho; warna "Not yet reviewed by a native speaker" badge.
5. Ads placement plan (Phase 8 ke liye, abhi OFF): har page type ke liye max ad slots, kabhi
   content se pehle nahi, kabhi buttons/quiz ke paas nahi, mobile par sticky/anchor sirf 1.
6. Ek naya gate: tools/test-googlebot-parity.mjs — same URL ko Googlebot UA aur Chrome UA se
   serve (local static server) → HTML byte-identical honi chahiye. CI me jodo.
GATES: build-all check green · test-googlebot-parity PASS · adsready --local 13/13 · seocheck PASS
ACCEPTANCE REPORT: FAIL list page-type wise, har FAIL ka fix PR ya owner-question, thin/duplicate
indexable counts (target: thin 0, duplicate-touched indexable < 50).
```
---
### U2 · DESIGN SYSTEM v2 — THEMES PER LANGUAGE + ANIMATION
**ROLE:** Senior product designer + frontend engineer (design systems) · **MODEL HINT:** strong frontend model
```
ROLE: Tum senior product designer aur design-system frontend engineer ho. Repo EkGuruLearning/EkGuru.
Site ke existing CSS layers (css/style.min.css, css/experience.css, css/storybook.css,
tools/bundle-experience-css.py) ko samjho, phir unhe tod kar nahi, extend karke v2 banao.
KAAM:
1. Design tokens file: css/tokens.css — color, type scale, spacing, radius, shadow, motion
   (duration/easing), z-index. Light + dark + high-contrast themes. System preference follow +
   user toggle (localStorage), bina flash of wrong theme (inline 1-line script in <head>).
2. Per-language theme: data/themes/<code>.json → accent, accent-contrast, pattern (SVG, us culture
   ke textile/architecture se inspired, stereotype nahi), script font stack, line-height (Devanagari,
   Arabic, Thai, CJK ke liye alag), dir (rtl/ltr). tools/build-themes.py → css/themes/<code>.css.
   Har theme ka contrast test (WCAG AA) automatic: tools/test-theme-contrast.mjs.
3. Fonts: sirf system + self-hosted subset (Noto family), font-display: swap, har script ka subset
   ≤ 60 KB. Google Fonts CDN nahi (privacy + speed).
4. Motion library (vanilla, no heavy framework): reveal-on-scroll, card lift, progress ring,
   streak flame, level-up confetti (canvas, 1.5s, click par band), stroke-order animation for
   letters (SVG path dash-offset). Sab `prefers-reduced-motion: reduce` par band ya fade-only.
   JS ≤ 12 KB gzip.
5. Components: lesson card, vocab table (audio button per row), dialogue bubbles, flashcard flip,
   quiz option states (correct/wrong with icon + text, sirf color nahi), level ladder, badge,
   empty state, toast. Storybook-style demo page: /design/ (noindex).
6. Visual regression: Playwright screenshots of 12 key templates × 3 themes × 2 viewports,
   CI me diff threshold.
GATES: build-all check green · test-theme-contrast PASS · Lighthouse mobile (local) perf ≥ 85,
a11y ≥ 95 on 5 sample pages · CLS ≤ 0.1 · no new console errors.
ACCEPTANCE REPORT: tokens list, themes count, bundle sizes before/after, Lighthouse table,
screenshot diff link.
```
---
### U3 · VOICE IN EVERY LANGUAGE
**ROLE:** Speech/audio engineer for language learning · **MODEL HINT:** strong coding model
```
ROLE: Tum language-learning apps ke speech/audio engineer ho. Repo EkGuruLearning/EkGuru.
Existing TTS (storybook injector "Hindi TTS", js ke speech tags, phase7 registries ke "speech
tags") ko audit karo, phir sab languages ke liye ek hi voice system banao.
KAAM:
1. js/voice.js (≤ 10 KB): Web Speech API speechSynthesis. Har text ke liye BCP-47 lang tag
   (data registry se). Voice picker: browser me jo voices us language ki hain unki list; user ki
   choice localStorage me. Speed 0.6x / 0.8x / 1x. "Slow" aur "Repeat" buttons.
2. Honest fallback: agar browser me us language ki voice nahi hai → button disabled + text
   "Your browser has no <Language> voice. Romanisation is shown instead." Kabhi galat language ki
   voice se nahi bolna.
3. Pre-recorded audio (optional, better quality): data/audio-manifest/<code>.json. Agar kisi
   word ka human recording (licensed, CC-BY ya owner-recorded) ho to woh pehle chale; label
   "Recorded by <name>". Synthetic ho to label "Synthetic voice". Kabhi synthetic ko human mat
   batao (R-3).
4. Har vocab row, dialogue line, example sentence, alphabet letter par 🔊 button; keyboard se bhi.
   Level pages (languages/<code>/level/*) HTML me button server-side render ho (JS OFF me hidden,
   JS ON me enabled) — layout shift nahi.
5. Listening practice: "listen and choose", "dictation" items voice.js use karein; agar voice
   unavailable to item skip + reason dikhe.
6. Speaking practice (optional): SpeechRecognition jahan supported; score nahi dikhana jab tak
   reliable na ho — sirf "we heard: …" transcript. Microphone permission sirf button click par.
7. Tests: tools/test-voice.mjs (jsdom mock speechSynthesis): sahi lang tag, fallback text,
   no autoplay, reduced-motion unaffected.
GATES: build-all check green · test-voice PASS · har course language ka BCP-47 tag registry me ·
no autoplay anywhere · a11y: har button ka aria-label "Play <word> in <Language>".
ACCEPTANCE REPORT: languages with browser voice (Chrome/Android/iOS table), languages with
recordings, pages touched, bundle size.
```
---
### U4 · LANGUAGE FACTORY + QUALITY GATE (700+ ka sahi raasta)
**ROLE:** Computational linguist + content-pipeline architect · **MODEL HINT:** strong reasoning model
```
ROLE: Tum computational linguist aur content pipeline architect ho. Repo EkGuruLearning/EkGuru.
Existing pieces samjho: data/courses*, data/lang-*.json, data/course-factory-state.json,
tools/build-world-course.py, tools/build-course-levels.py, tools/build-phase7-*.py,
world-languages/ (195 pages), languages/ (course hubs), learn/<indian-lang>/.
GOAL: 700+ languages ko 3 tiers (T1 full course, T2 starter pack, T3 reference) me laana, aur har
language sirf quality gate pass karke hi upar ke tier ya index me jaaye (Golden Rule R-2).
KAAM:
1. Language registry: data/languages/registry.json — har language: ISO 639-3, BCP-47, name
   (English + endonym), scripts (ISO 15924), countries (ISO 3166) with speaker estimate + source
   URL, direction, family, tier, status (draft/review/published), reviewer (name or null).
   Sources sirf citable (Ethnologue public pages, Glottolog, CLDR, government census, UNESCO).
   Har number ke saath source URL. Source nahi = number nahi.
2. Country ↔ language map: har country (195) ki official + major languages. world-languages/<cc>
   pages is registry se banen. Jahan EkGuru course hai wahan link.
3. Content schema per tier (JSON Schema files in data/schemas/):
   - T3: facts, script sample (Unicode, CLDR exemplar chars), 20 greetings/phrases with source,
     "how to start learning" guide (language-specific, ≥ 400 unique words), sources list.
   - T2: alphabet/script lesson, 300 core words (with romanisation + IPA where known), 50 phrases,
     10 dialogues, 5 grammar notes, 3 practice sets, voice tags.
   - T1: A1, A1+, A2, A2+, B1, B1+, B2, B2+, C1, C1+, C2 — har level: 3–5 units, har unit 3–5
     lessons, vocab (romanisation + IPA), grammar box, dialogue, practice (10+ item types),
     quiz, worksheet, level test (10–20 items), "extra content" (culture note, reading passage,
     listening passage, idioms, common mistakes, real-life task), sab voice ke saath.
4. QUALITY GATE (tools/language-gate.py) — ek language tab tak index nahi:
   a. schema valid; b. unique-text ratio vs other languages ≥ 85% (copy-index shingles);
   c. har vocab item ka script Unicode range sahi (e.g. Tamil words Tamil block me);
   d. romanisation present; e. koi "lorem", "TODO", "[translate]" nahi;
   f. sources present for facts; g. native-speaker review status = reviewed (T1/T2 ke liye) —
      warna page `noindex` + badge "Draft: not yet reviewed by a native speaker";
   h. voice tag valid; i. min word counts per tier.
   Gate report: data/quality/language-gate.json. CI me gate chale.
5. Generation workflow (machine help allowed, blind publish nahi):
   draft (agent/LLM ya contributor) → automatic gate → native reviewer checklist (docs/review-
   checklist.md, reviewer form via Apps Script) → published. Reviewer ka naam page par sirf
   unki permission se.
6. Rollout order (index sirf gate pass par):
   Wave 1 (T1): existing 32–39 courses ko gate se guzaro, jo fail hon unhe fix ya noindex.
   Wave 2 (T1): top languages by learner demand — es, fr, de, ja, ko, zh, ar, pt, it, ru, tr, hi,
     ur, bn, pa, ta, te, mr, gu, kn, ml, id, vi, th, sw, nl, pl, fa, he, uk (jo pehle se nahi).
   Wave 3 (T2): har country ki official language jiska T1 nahi (≈ 150).
   Wave 4 (T3): baaki 500+ documented languages, sirf reference pages, sirf jab ≥ 400 unique
     words + sources.
7. Maintenance: tools/course-health.py weekly — broken audio tags, stale sources (> 12 months),
   reviewer gaps, learner-reported errors (questions API) → data/quality/course-health.json +
   GitHub issue auto-create (label: course-health).
GATES: build-all check green · language-gate CI step green · no language indexed with gate FAIL ·
hreflang only for real translations.
ACCEPTANCE REPORT: tier counts (T1/T2/T3 published vs draft), gate FAIL reasons top 10,
sitemap counts, sample of 5 languages with links.
```
---
### U5 · COURSE CONTENT — BEGINNER SE MASTER (per language, per wave)
**ROLE:** Senior curriculum designer (CEFR) + native-language editor · **MODEL HINT:** strong writing model
*(Is phase ko har language wave ke liye alag session me chalao. `<LANG>` ki jagah language code likho, e.g. `es`.)*
```
ROLE: Tum CEFR-aligned senior curriculum designer ho, aur <LANG> ke editor ho. Repo
EkGuruLearning/EkGuru. Language: <LANG>. Registry: data/languages/registry.json.
Schema: data/schemas/course-t1.schema.json. Gate: tools/language-gate.py.
KAAM:
1. <LANG> ka T1 course likho/upgrade karo: A1 → C2 + 5 half-steps, har level ke units, lessons,
   vocab (romanisation + IPA), grammar, dialogues, practice (multiple choice, fill-blank,
   translation both ways, matching, reorder, error correction, dictation, listening, reading
   comprehension, speaking prompt), quiz, worksheet, level test.
2. Har level par EXTRA CONTENT (yeh page ko unique banata hai, Google ko value dikhta hai):
   - culture note (us level ki situation se juda, real, sourced)
   - reading passage (level-appropriate, original writing — kahin se copy nahi)
   - listening passage (script + voice)
   - 10 idioms/expressions (with literal + real meaning)
   - "common mistakes for English/Hindi speakers" (specific to <LANG>)
   - one real-life task ("order food", "write a complaint email", "give a 2-min talk")
3. Beginner-first explanation: har grammar point pehle simple English me, phir example, phir
   exception. "Zero knowledge" learner ke liye alphabet/script lesson stroke-order animation ke saath.
4. Original content only. Koi textbook, Duolingo, Wikipedia paragraph copy nahi. Copy-index
   ownership check pass hona chahiye.
5. Native review: har level ka reviewer checklist docs/review/<LANG>/<level>.md me; review
   hone tak level page noindex + draft badge.
6. Build: python3 tools/build-course-levels.py → pages, fir poora build-all (decorators) — generated
   pages haath se edit nahi (R-5).
GATES: language-gate <LANG> PASS (review pending allowed but then noindex) · test-course-levels
PASS · copy-index ownership PASS · build-all check green.
ACCEPTANCE REPORT: per level counts (units, lessons, words, questions, extra items), gate result,
review status, 3 sample URLs.
```
---
### U6 · SEO ARCHITECTURE — "learning ke liye EkGuru" search me aaye
**ROLE:** Technical + international SEO lead · **MODEL HINT:** strong reasoning model
```
ROLE: Tum technical aur international SEO lead ho. Repo EkGuruLearning/EkGuru. Sirf white-hat
(R-1). Goal: "learn <language>", "<language> alphabet", "<language> for beginners", "<phrase> in
<language>" jaisi searches me EkGuru ka helpful page aaye.
KAAM:
1. Information architecture: /languages/<code>/ (hub) → /level/<lvl>/ → lesson anchors;
   /learn-<language>-from-<country>/ sirf jab us country ka specific content ho (warna nahi banana).
   Har hub par breadcrumb, related languages, next step.
2. Structured data (sirf jo page par visible hai): Course + CourseInstance (free, online),
   LearningResource, BreadcrumbList, FAQPage (visible FAQ ke hi sawal), QAPage (ask/), DefinedTerm
   for vocab (optional), Organization + founder Person. Rich Results test sample 20 pages.
3. hreflang: sirf jab real translation ho. x-default = English. Translated UI pages (ar, de, es,
   fr, ja, pt) ka full content usi language me (half-English block nahi).
4. Sitemaps: per tier + per content type, lastmod sirf content change par, noindex pages kabhi nahi.
   sitemap-index me sirf non-empty sitemaps.
5. Internal linking: har lesson ↔ related guide ↔ toolbox tool ↔ practice. Orphans 0.
6. Titles/meta: unique, human, ≤ 60/155 chars, keyword natural. Duplicate 0.
7. Core Web Vitals: field data ke liye web-vitals.js (≤ 2 KB) → Apps Script endpoint (privacy-safe,
   no cookies). Report weekly.
8. Search Console: owner ke liye docs/gsc-setup.md (verify, sitemap submit, international targeting
   nahi — site global hai).
9. llms.txt + humans.txt updated, sach ke saath.
GATES: seocheck PASS · build-full-page-inventory PASS · Rich Results sample 0 errors ·
orphan 0 · dup titles/meta 0 · hreflang reciprocity 100%.
ACCEPTANCE REPORT: indexable page count by type, schema coverage table, hreflang pairs, CWV.
```
---
### U7 · RETENTION — "ek baar aaya to wapas aaye"
**ROLE:** Learning-experience (LX) + product engineer · **MODEL HINT:** strong frontend model
```
ROLE: Tum learning-experience designer aur product engineer ho. Repo EkGuruLearning/EkGuru.
Sab kuch on-device (localStorage/IndexedDB), no account, no tracking cookies (privacy page sach rahe).
KAAM:
1. Placement test (/start/): 5–10 adaptive questions → recommended level per language.
2. Daily plan: "Today" widget — 1 lesson + 10 review cards + 1 listening, 10–15 min.
3. Spaced repetition (SM-2 ya FSRS-lite) for vocab across all languages; review deck per language.
4. Streaks + XP + badges (honest: kisi paid feature ka jhootha vaada nahi). Streak freeze 1/week.
5. Progress page: per language, per level, words learned, accuracy, time; export/import JSON.
6. Offline: service worker caches visited lessons + audio manifests; "Download level for offline".
7. Web push reminders sirf user opt-in par, time chosen by user; unsubscribe 1 click.
8. "Continue where you left off" on home and every language hub.
9. Accessibility: sab keyboard-operable; screen-reader announcements for correct/wrong.
10. Tests: tools/test-retention.mjs (jsdom): SRS scheduling, streak math, export/import, SW cache list.
GATES: build-all check green · test-retention PASS · no third-party tracker · privacy page updated.
ACCEPTANCE REPORT: features shipped, storage keys, SW cache size, screenshots.
```
---
### U8 · VISUALS + ILLUSTRATION SYSTEM
**ROLE:** Illustration + data-visualization engineer · **MODEL HINT:** strong frontend model
```
ROLE: Tum illustration system aur data-viz engineer ho. Repo EkGuruLearning/EkGuru.
Existing generated SVG plates (tools/build-visuals.py, build-country-visuals.py,
build-toolbox-visuals.py, build-world-art.py) ko extend karo.
KAAM:
1. Har language hub: script showcase plate (CLDR exemplar characters, real glyphs), speaker map
   (simplified world SVG, countries from registry, source cited), level ladder figure.
2. Har lesson: 1 contextual SVG illustration from lesson data (market, family tree, clock, map) —
   generated from data, stock art nahi, alt text specific.
3. Alphabet: animated stroke-order SVG for scripts where stroke data available (KanjiVG CC-BY-SA
   for Japanese, open Devanagari/Hangul data); license credit visible.
4. Sab SVG inline-able, ≤ 20 KB each, lazy, width/height set (CLS 0), dark-mode aware via tokens.
5. OG images per page (1200×630) generated at build (SVG→PNG via resvg), unique per language/level.
GATES: build-all check green · all images alt present · total image weight per page ≤ 300 KB ·
licenses file docs/asset-licenses.md complete.
ACCEPTANCE REPORT: plates count by type, sizes, license list, 5 sample screenshots.
```
---
### U9 · QA + FINAL READINESS BATTERY
**ROLE:** QA lead + release manager · **MODEL HINT:** strong reasoning model
```
ROLE: Tum QA lead aur release manager ho. Repo EkGuruLearning/EkGuru.
KAAM:
1. Poori PART F battery (file "1 command", 100 checks) + is file ke naye gates chalao.
2. Playwright journeys: new learner (home → start → A1 lesson → practice → quiz → review),
   RTL language journey, offline journey, zero-tutor journey, voice-unavailable journey.
3. Cross-browser: Chromium, WebKit, Firefox; mobile viewport 360×800.
4. Link checker (internal 0 broken), HTML validity (tag balance 0 errors), JSON-LD 0 broken.
5. Copy review sample: 30 random indexable pages — koi placeholder, galat claim, broken voice nahi.
6. bash tools/weekly-guard.sh → ALL GREEN (live).
GATES: sab green. Ek bhi FAIL = review submit nahi.
ACCEPTANCE REPORT: TOTAL n/100 + naye gates, FAIL list with fixes, "READY FOR REVIEW" ya "NOT READY".
```
---
### U10 · ADSENSE SUBMIT + APPROVAL KE BAAD (owner + agent)
**ROLE:** Monetization ops · **MODEL HINT:** any
```
OWNER (manual):
1. AdSense → Sites → ekguru.shop → "Request review". Auto ads OFF.
2. Payment profile, identity verification complete.
3. EEA/UK traffic > 5% ho to pehle Google-certified CMP (TCF v2.2) — plan "1 command" Phase 9.
AGENT (sirf "Approved" ke baad, naye session me):
- ROLE: monetization ops engineer. google-monetization.json me approval_status = APPROVED,
  ADS_RUNTIME_ENABLED = true, ADVERTISING_AVAILABLE = true (consent ke saath), U1 ka placement
  plan implement (max slots per template), lesson/practice/quiz/test/course player/legal/contact/
  404/search/join/booking par 0 ads. CLS ≤ 0.1 ad slots ke saath (reserved height).
- Gates: test-ad-policy, test-consent-release, Lighthouse CLS, weekly-guard green.
REJECT hua to: rejection reason exact text owner bhejega → "1 command" Phase 7 (R-1..R-8 playbook).
```
---
### U11 · HAMESHA — WEEKLY MAINTENANCE
**ROLE:** Site reliability + content maintenance · **MODEL HINT:** any
```
ROLE: Tum EkGuru ke weekly maintainer ho.
Har hafte: bash tools/weekly-guard.sh · python3 tools/course-health.py · language-gate report ·
Search Console coverage errors (owner screenshot bheje) · learner-reported errors (questions API) ·
broken links · stale sources (> 12 months) · Sheet data source health (csv/tsv).
Output: ek PR "weekly maintenance <date>" sirf fixes ke saath, CI green, aur owner ke liye 10-line
summary: kya theek hua, kya owner ko karna hai.
```
---
## 4. PASTE INDEX
| Kab | Kya paste karna hai |
|---|---|
| Abhi, sabse pehle | U0 |
| U0 merge ke baad | U1 |
| Design/voice | U2, phir U3 |
| Languages | U4 (ek baar), phir U5 har language/wave ke liye |
| SEO + retention + visuals | U6, U7, U8 |
| Submit se pehle | U9 |
| Submit / approval | U10 |
| Har hafte | U11 |
## 5. JO KABHI NAHI KARNA
- Googlebot ko alag content dikhana, hidden text, fake reviews/ratings, "native/verified" bina proof
- Ek saath sainkdon machine-generated pages index karna
- Lesson/quiz/test/legal/booking pages par ads
- Runtime ad flags approval se pehle true karna
- CI red par merge

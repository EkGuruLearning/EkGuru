# EkGuru — Phase 7C Handoff

- **repo**: EkGuru (GitHub Pages static site)
- **branch**: main
- **SHA**: fc06a0c414467c20f264381c88980c584e79100c
- **verdict**: GREEN_GLOBAL_ENGINE_PRODUCTION_READY (45/45)

## Completed batches
- tranche 1: content graph + registries + live inventory
- tranche 2: conversation engine (Gate C)
- tranche 3: goals/script/grammar/vocab/search + My Learning (Gate D)
- tranche 4: country-context + India visitor + heritage (Gate E)
- tranche 5: admin global language ops (Gate F)
- tranche 6: child/family privacy mode (device-only toggle; no child content) + SRS card globalization
- tranche 7: multi-viewport gate (Gate G), real SEO-scale crawl (Gate H), automation pipeline (16/16), search-index integration (578 entries), contexts hub, intermediate page de-orphaned
- tranche 8 (Stage 2): language-pack reuse proof — Spanish starter pack (BETA) renders through the same engines (Gate I); content schema + graph reports; es stays BETA, hi stays the only PRODUCTION language
- tranche 9 (Stage 3): multi-language starter packs — 9 authored BETA packs (en/es/bn/ta/te/mr/gu/pa/ur) with per-language indexable pages, home-page section/nav/global-nav reachability, PLANNED languages stay page-less (Gate J)
- tranche 10 (Stage 4): starter-pack learning experience — browser-TTS Listen buttons (computer voice, BCP-47 tags fixed: bn-IN/ta-IN/te-IN/mr-IN/gu-IN/pa-IN/ur-PK) + deterministic rule-based starter check, all through the shared engines; Hindi PRODUCTION unchanged (Gate K)
- tranche 11 (Stage 5): authored starter packs for all remaining PLANNED languages — 20 more packs (fr/ar/de/ja/ko/zh/ru/pt/it/nl/pl/tr/fa/he/th/vi/id/ms/sw/uk) => 29 BETA packs total, 0 PLANNED; RTL speech tags fixed (ar-SA/fa-IR/he-IL/ms-MY); Hindi stays the only PRODUCTION language (Gate L)
- tranche 12 (Stage 6): everyday polish — 'More on EkGuru' block renamed 'Learn languages' (home + inner pages); browser-TTS Listen buttons mounted on the languages hub (all 30 cells), SRS review card and vocabulary practice; practice questions rotate daily via deterministic dayShuffle (rule-based, not AI) (Gate M)
- tranche 13 (Stage 7): first full non-Hindi course — authored Spanish course (6 lessons, 12 vocab + 12 grammar practice on the shared engine, 20-question daily-rotating topic quiz, 24-card SRS review deck) wired into the hub/pack page/courses registry; all verified in real Chromium with es-ES computer voice, 0 page errors (Gate N); es stays BETA
- tranche 14 (Stage 8): second course + generator generalization — build-language-course.py is now one language-parameterized engine over tools/course-data/{code}.py; authored French course (fr-FR) built and verified in real Chromium with the same Gate N battery (now iterating every course in data/courses.json); fr stays BETA

## Pending
- full courses for the remaining 27 BETA languages, one by one, popular first (user directive) — each needs lessons + practice + quiz + review + recorded-audio decision, then browser QA before PRODUCTION
- flashcards/toolbox pages: extend the same Listen buttons to the flashcards deck and phrasebook
- child-specific lesson content (privacy mode ships; lessons not authored)
- large-scale SEO batches — never before quality gates

## Next exact command
```
python3 tools/build-language-course.py && python3 tools/build-phase7c-registries.py && python3 tools/build-phase7-pages.py && python3 tools/build-hindi-pages.py && python3 tools/test-phase7c-stage7.py
```

## Test command
```
python3 tools/test-phase7c.py && python3 tools/test-phase7c-conversation.py && python3 tools/test-phase7c-engines.py && python3 tools/test-phase7c-context.py && python3 tools/test-phase7c-admin.py && python3 tools/test-phase7c-langpack.py && python3 tools/test-phase7c-langs.py && python3 tools/test-phase7c-starter.py && python3 tools/test-phase7c-stage6.py && python3 tools/test-phase7c-stage7.py && python3 tools/test-phase7-browser.py && python3 tools/test-phase6-matrix.py && python3 tools/test-card-interactions.py
```

## Unresolved errors
- none

## Honesty notes
- LIVE deploy is STALE and behind local HEAD: live ekguru.shop returns 404 for /learn/my-learning/ and the other Phase 7C pages; only pre-7C pages are live.
- GitHub origin/main holds only 'Initial commit' — the real history (50+ commits) exists only in this workspace; no remote URL is configured, so this agent cannot push. The workspace snapshot + git history are the continuity layer.
- The one canonical alias tutor.html -> /tutor/ is an intentional legacy redirect, not a defect.

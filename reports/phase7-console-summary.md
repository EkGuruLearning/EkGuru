# EK GURU — PHASE 7 GLOBAL LANGUAGE SYSTEM

**Verdict: `YELLOW_PARTIAL`** (14/22 gate items green) — the global **foundation** is built and
proven in real Chromium; the **advanced** systems are next. Generated 2026-09-12.

## RESEARCH
- Studied: HindiPod101, Mango Languages, Duolingo, Memrise, Ling, Rocket Languages, Preply, Anki.
- Adopted: goal→level paths, conversation-first + audio-first with transcripts, SRS review,
  progress dashboards, culture modules, offline, tutor bridge.
- Rejected: gamification-as-product, English-heavy podcasts, thin "advanced" promises,
  mass-generated language×country pages, uniform flashcard loops.
- `reports/global-language-product-research-phase7.md`

## LANGUAGES
- **29 target languages** in the registry (`reports/language-registry-phase7.json` + runtime
  `js/languages.js`), each with ISO 639-1/3, native name, script, direction, transliteration,
  speech tag, audio status, content maturity, levels, goals, production status.
- **PRODUCTION: Hindi only** (15 lessons, 45 quizzes, 6 paths, 3 practice tools, SRS, offline).
- **PLANNED: 28** (Spanish, French, Arabic, German, Japanese, Korean, Chinese, Russian, …) —
  listed honestly as "Coming"; **zero empty lessons created**.

## COUNTRIES
- **250 ISO 3166-1 entities · 194 sovereign states** in `reports/country-registry-phase7.json`
  (cca2/cca3, region, subregion, official languages, independence/UN membership, contexts,
  whether a source-country page already exists).
- **Data, not pages** — no page is generated from the registry. 153 countries already have a
  real source-country page; the rest are honest gaps.

## HINDI
- Remains the reference implementation; all Phase 5/6 behaviour re-verified green this phase.

## ADVANCED
- **Audio abstraction** ✅ `EkGuruAudioProvider` (BROWSER_TTS|RECORDED|API_TTS|UNAVAILABLE);
  resolves hi-IN/es-ES → BROWSER_TTS with honest "computer voice" labelling.
- **Onboarding** ✅ deterministic goal→level→time→script→context recommender (`/start/`,
  `js/onboarding.js`), explicitly not AI; verified for Hindi (real links) and Spanish (honest "planned").
- **Language hub** ✅ `/languages/` renders from the registry (29 cards, Available/Coming).
- Speech, conversation engine, My Learning, per-script search, country modules, secure API layer:
  **pending** (documented in `phase7-gap-map.json`, P1/P2).

## SEO
- Scale gate (`reports/global-seo-scale-audit.json`): 158 country pages avg 6,051 chars each
  (not thin) but **max pairwise 5-gram similarity 0.65 → WARN** — real de-templating work queued.
- `seocheck`: 615 pages, **0 broken links, 0 orphans, 608 sitemap URLs**.
- No thin mass generation; `languages/` + `start/` are indexable with unique title/desc/H1/canonical.

## GITHUB
- Everything new is static: HTML/CSS/JS + JSON registries + localStorage. Server/API features are
  explicitly out of scope until a secure relay exists; nothing ships a client-side secret.

## VERIFIED (measured, Chromium)
- Registry/schema/route/secret tests PASS (`phase7-registry-tests.json`).
- Onboarding + language hub + audio provider PASS (`phase7-browser.json`).
- Layout matrix **45/45** (320–1920).
- Phase 5 cards 19/19 · matrix 146/146 · P0 recovery PASS.
- Phase 6 quizzes/audio/SRS/progress/practice/offline/fuzzy search all PASS.

## BLOCKED
- None hard-blocking. Secure server-side relay for real APIs remains unavailable on static hosting
  (documented; nothing shipped with secrets).

## TOP 10 NEXT OPPORTUNITIES (evidence-backed)
1. De-template the 158 country pages (0.65 max similarity → real §21 risk).
2. Language-aware search (per-script aliases beyond Devanagari).
3. Deterministic conversation scenario engine.
4. Generalize My Hindi → My Learning (device-only honesty).
5. Map 12 tools to the reusable toolbox categories.
6. India-visitor + NRI/heritage context modules (registry metadata already exists).
7. Recorded audio for the top 100 Hindi words (replaces TTS honestly).
8. Admin global-language ops board (languages/countries health).
9. Goal-based onboarding → path auto-start (deep link into paths with ?goal=).
10. hreflang for the 16 localized home pages (equivalent pages only).

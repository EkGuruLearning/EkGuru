# Hindi Academy 2.0 — implementation checkpoint (2026-11-28)

## Homepage and architecture continuation — current status

This section supersedes the historical checkpoint below where they disagree. The existing `/learn/hindi/` is now the Academy entry: the global shell, canonical, byline, draft disclosure, old directory, topic fragment IDs, all previous links and optional independent tutor discovery are retained. The legacy directory is a native disclosure left open so old fragment URLs also work without JavaScript. The Storybook automatic TOC is disabled only on this hub because it was overwriting stable H2 IDs at runtime. No tutor, payment or non-Hindi course code was changed.

### Implemented inventory

- `data/hindi-academy/curriculum.json` is v2 and separates languages, curated age-oriented tracks, courses, levels, phases, chapters, lessons, activities, resources, vocabulary, skills, goals and age/proficiency metadata. Current registration: 1 language, 5 curated tracks, 1 existing Foundation course, 1 introductory level, 4 Foundation phases, 1 companion chapter, 19 lesson records (18 existing Foundation lessons and the companion), 1 activity, 2 resource references and 3 draft vocabulary records. These counts are *registry coverage*, not claims that the rest of the existing website or the target 200 chapters has been migrated.
- `tools/lib/academy_registry.py` validates IDs, relationships, local URLs/fragments and supports bounded lesson navigation, related resources, breadcrumbs, derived search metadata and course/phase/lesson counts. `tools/build-hindi-academy.py` generates marked static catalogue/track/navigation regions and the small `data/hindi-academy/search-index.json`. `tools/build-hindi-hub.py` reads the same manifest for the new homepage; both are registered in the existing build workflow. Existing page generators remain authoritative for their content.
- `/learn/hindi/academy/catalogue/` is a static HTML Foundation catalogue, enhanced by a separately loaded static index for search and filters. It currently covers only registered Foundation lessons, not the full Hindi library; the hub keeps the full existing directory. The catalogue, companion, worksheet and answer sheet remain `noindex` pending review and owner approval. The existing sitemap publication gate adds only eligible self-canonical, indexable pages; it deliberately does not publish these drafts. No new search-engine ranking claims are made.
- Homepage includes five pathways, course/level explorer, local Continue using `EkGuruRetention`, studios, daily Hindi, journal/review, FAQs and tutor/other-language links. Global theme preferences use the existing system/light/dark/contrast store; text-size preference is separate and local. Hero image is original generated artwork, encoded as an 86 KB WebP. Shared shell CSS/JS is namespaced and avoids loading vocabulary/audio on the homepage.
- The vowel companion records its last open location in the existing device journal and still uses the legacy Hindi progress store for its own completion/quiz. It does not migrate or overwrite existing data. Hindi font precedence on the worksheet was corrected after a real Chromium print inspection. The repository's existing print watermark remains.

### Extensibility fixture

`tests/unit/test-academy-registry.py` uses a temporary directory, not the repository's public tree. It adds one course, phase, chapter, lesson, vocabulary record, worksheet and audio reference, then checks counts, rendered home/course entries, catalogue, search fields, derived worksheet/audio flags, breadcrumbs, related-resource and next-lesson links. It also invokes the existing sitemap gate on temporary self-canonical pages and verifies noindex removal. It does **not** prove production build generation for thousands of complete chapters or the availability/licensing of a real audio recording. No fixture content is published.

### Verification

- `python3 tools/build-all.py check`: **PASS** after regeneration, including Academy registry/fixture tests, existing indexing contract, sitemap, editorial/quality inventory, voice, learner-storage migrations and SEO/AEO/GEO gates. This pass preceded final scoped CSS contrast/font refinements, stricter audio/publication validation and small fixture-test updates; focused tests were rerun afterward. It is not an editorial or production release approval.
- `npm test`: **PASS** (existing tutor/application and payment tests use their documented mocks/contracts; no live deployment test).
- Real Chromium, static server: hub at widths 320, 375, 390, 430, 768, 1024, 1280, 1440 and 1920; no document overflow, reduced motion, legacy hash preservation, no-JS catalogue/legacy links, local larger-text and theme persistence, filter/reset/keyboard search, returning-user Continue, old progress preservation, canvas drawing/undo and print-only controls. Browser script: `tests/e2e/test-hindi-academy-browser.mjs`; Playwright and Chromium were temporarily installed outside package manifests for this run. Screenshots/PDFs are scratch artifacts in ignored `.artifacts/academy-qa/`, not public assets.
- Real Chromium print-to-PDF: one page for A4 and US Letter; visual inspection found Hindi font selection issue, which was fixed. The source-line watermark remains by existing site policy. Printer/physical-device behavior is unverified.
- Axe-core automated WCAG-tagged checks on the new homepage region at 390px in light and dark and on catalogue/companion main regions in light: no violations after fixing detected contrast and link-distinction issues. This is a scoped automated check, **not** a WCAG 2.2 AA certification or a screen-reader/manual audit.
- `build-public-dist.py --check`: PASS, 1,576 existing sitemap URLs present; no private paths in public output. `git diff --check`, both Academy generators' `--check`, isolated fixture and focused Hindi Academy regression: PASS. No field Core Web Vitals, actual Hindi device-voice quality or Search Console data measured.

### Remaining work / deployment readiness

This is an extensible foundation, not the entire requested academy. Existing graded courses, labs and other languages are not yet registered in the v2 manifest; searches cannot filter material not registered. The catalogue renders all registered lesson links on its own page, so pagination/sharding and search-index partitioning are required before thousands of lessons. Course registration still requires authoring real pages, adding registry records and rebuilding; it does not generate substantive lessons. Chapter-level navigation, universal shell rollout, all-track age-specific curricula, curriculum coverage, approved stroke paths, recordings, full assessments/worksheets and human educational review remain open. Sitemap and site-wide search generation remain governed by existing publication policy rather than automatically overriding `noindex`. Optional language expansion requires language-specific content and editorial review.

The automated build is green, but visual/assistive-technology QA on real devices, broader print/contrast coverage, performance metrics, write-mode end-to-end publishing and qualified editorial review remain outstanding. **Do not deploy or merge without owner approval and release verification.**

### Exact changed-file inventory (cumulative branch work)

- Existing: `index.html`, `learn/hindi/index.html`, `js/storybook.js`, `tools/build-all.py`, `tools/build-hindi-hub.py`, `data/copy-index.json`, `data/editorial/page-metadata.json`, `data/quality/full-page-inventory.json`, `data/quality/phase2-content-inventory.json`, `data/quality/phase3-originality-audit.json`.
- New: `css/academy-shell.css`, `css/hindi-academy.css`, `data/hindi-academy/curriculum.json`, `data/hindi-academy/search-index.json`, `images/hindi-academy-hero.webp`, `js/academy-catalogue.js`, `js/academy-home.js`, `js/hindi-academy.js`, `learn/hindi/academy/index.html`, `learn/hindi/academy/catalogue/index.html`, `learn/hindi/academy/vowels/index.html`, `learn/hindi/academy/worksheet/index.html`, `learn/hindi/academy/answers/index.html`, `tools/build-hindi-academy.py`, `tools/lib/academy_registry.py`, `tests/e2e/test-hindi-academy-browser.mjs`, `tests/regression/test-hindi-academy.mjs`, `tests/unit/test-academy-registry.py`, `docs/hindi-academy-2-checkpoint.md`.

---
## Historical checkpoint (previous batch)

## Status and scope

This is an incremental implementation, **not** a completed 200-chapter academy or a publication approval. No production deployment or merge has occurred. The new resources are draft, not native-speaker reviewed, and intentionally `noindex, follow`: the existing foundation generator says new index decisions require owner approval. The sitemap, robots policy, existing canonicals, tutor flow, other languages and legacy learning data have not been changed.

## Repository inventory and reuse map

| Existing asset | Where | Academy migration/use |
| --- | --- | --- |
| One Hindi hub, 74 lessons/guides, 34 topic chapters, 25 labs/tools, 15 materials | `learn/hindi/index.html`, `hindi/`, `materials/`; generated by `tools/build-hindi-hub.py` | Kept; generator adds an Academy link, never removes content. Counts overlap and aren't unique lessons. |
| Foundation: 18 lessons | `learn/hindi/foundation/`; `tools/hindi-foundation-content.py`, `build-hindi-foundation.py`, `data/content/hindi-foundation-depth.json` | The vowel companion links to the substantive existing `swar` lesson and consonant/matra lessons. Existing URLs and their review notices stay intact. |
| Daily course | `daily-hindi/` (30 day directories plus index) | Still available from the original hub. |
| Graded course | `data/courses/`, `languages/hi/level/`, `/courses/` | Existing hub advertises 98 graded lessons. A1–C2 remains a separate dimension; A3/B3/C3–C5 are EkGuru extensions, not CEFR. Existing materials must be audited before interpreting these as independently assessed proficiency. |
| Practice library | `js/hindi-learning-library-data.js`, `js/hindi-learning-library.js`, `tools/build-hindi-learning-library.py` | Existing QA inventory: 1,540 distinct models, including 1,014 words/expressions, 463 sentence models, 49 letter/sound models and 14 readings. These are reused source items, not a new 10,000-entry dictionary or reviewed count. See `docs/hindi-learning-library-qa.md`. |
| Speech | `js/voice.js`, `js/hindi-audio.js`, `data/audio-manifest/hi.json` | Existing Hindi manifest has no licensed recordings. New companion uses the existing shared voice adapter, which prefers licensed recordings where available and otherwise uses matching Hindi device speech; no English fallback or microphone. Four unique word strings have controls, normal/slow and stop. Voice and quality are device-dependent. |
| Writing and barakhadi | `js/storybook.js`, `learn/hindi-barakhadi/`, `learn/hindi-how-to-write-vowels/`, `learn/practice/writing/` | Existing trace-grid renders SVG text, not verified stroke data. New canvas supports 11 independent vowels as printed visual guides, free drawing, undo and clear; it makes no claim about stroke order or recognition. |
| Journal and review | `js/hindi-progress.js`, `js/hindi-srs.js`, `learn/hindi/my-progress/` | Companion uses existing v1 journal and export/import, without migrating or replacing stored data. Existing SRS is linked through the hub. |
| Publishing and discovery | `tools/build-hindi-hub.py`, `tools/build-all.py`, `tools/build-sitemaps.py`, `tools/build-public-dist.py`, `robots.txt`, `sitemap-index.xml` | Existing content/canonicals preserved. New draft pages are self-canonical and noindex, deliberately excluded from sitemaps pending review and indexing approval. Build integration and remaining gate status below. |
| Tutor applications and booking | `join.html`, `tutor/`, `apps-script/` and integration tests | Untouched. |

This is a targeted inventory, not a complete audit of every page, duplicate, image, content item, backlink or legacy link. Existing review disclosures are not evidence of native review. Search Console and live search-intent research were not available in this environment; no search-volume or ranking claims are made.

## Coverage matrix

| Track | Four phase entry points | New complete chapters | Reviewed chapters | Remaining |
| --- | ---: | ---: | ---: | --- |
| Kids | 4 curated existing links | 0 | 0 claimed | age-band-specific stories, lessons, games and review |
| Absolute beginners | 4 curated links | 0 | 0 claimed | companion is partial; full chapter structure, pedagogy and assessments |
| Intermediate | 4 curated existing links | 0 | 0 claimed | authored track, skills coverage and editorial review |
| Advanced | 4 curated existing links | 0 | 0 claimed | professional, literature and discourse curriculum and review |
| Adults and older adults | 4 curated links | 0 | 0 claimed | adult-oriented situations, accessibility research and review |

The five tracks and 20 phase links are **curated routes**, not 20 authored phases or a claim that the existing linked pages are age-adapted. There is one new vowel companion, not a complete reference chapter. No new centralized vocabulary entries, verified stroke paths, recordings, stories or generated PDFs are claimed. The companion has three vocabulary cards, four spoken word strings, a three-question quiz, one tracing activity, one print/save-as-PDF worksheet and one separate printable answer key. The worksheet provides copy boxes rather than numbered stroke or dotted paths. Audio availability is conditional on a matching device voice. The source manifest (`data/hindi-academy/curriculum.json`) governs the directory; it is not yet an authoritative chapter-level navigation manifest.

## Files and generator ownership

- `data/hindi-academy/curriculum.json` — stable IDs and curated paths.
- `tools/build-hindi-academy.py` → marked track region in `learn/hindi/academy/index.html` (run with `--check` to compare); registered in `tools/build-all.py`.
- `learn/hindi/academy/vowels/index.html`, `worksheet/index.html`, `answers/index.html` — static, readable without JavaScript.
- `css/hindi-academy.css`, `js/hindi-academy.js` — scoped styles and optional interactions.
- `tools/build-hindi-hub.py` → `learn/hindi/index.html` — additive discovery link; `index.html` adds home link.
- `tests/regression/test-hindi-academy.mjs` — focused tests, registered in `tools/build-all.py`.
- `data/copy-index.json`, `data/editorial/page-metadata.json`, `data/quality/full-page-inventory.json`, `data/quality/phase2-content-inventory.json`, `data/quality/phase3-originality-audit.json` — refreshed existing generated inventories; these are mechanical, not evidence of editorial approval.
- This private checkpoint under `docs/` is excluded by the existing public deploy builder.

## Verification performed

- Baseline `npm test`: passed, including existing tutor/application and payment-related mock tests; live external contracts were not contacted due to network restrictions.
- Baseline `build-hindi-foundation.py --check`, `build-hindi-hub.py --check`, `test-hindi-foundation-depth.py` (6), `test-hindi-audio.py`: passed.
- After changes: Academy manifest builder `--check`, hub generator `--check`, new Node/jsdom regression, `npm run test:courses`, `test-hindi-learning-features.py`, `test-hindi-learning-library.mjs` (16), `test-hindi-quizzes.py`, `build-public-dist.py --check` (1,576 sitemap URLs present) and `git diff --check`: passed. The course pronunciation audit reported its existing editorial gate **BLOCKED** for missing source-referenced IPA (not a technical failure).
- The new test checks all new-page internal URLs/fragments, duplicate IDs, canonical/noindex, manifest paths, mock audio availability and refusal of an English voice, quiz, journal preservation/export/import, and basic canvas controls. Canvas rendering and pointer input are not real-browser tested.
- The first `python3 tools/build-all.py check` stopped on missing shell decoration. The pages were then shell-decorated, the directory generator changed to update only a marked track region, copy fingerprints, editorial metadata and inventory reports regenerated, and ad policy aligned. The latest full check passed those gates and the indexing contract, but **failed** at the shared voice regression because the companion initially used speech synthesis directly. It was changed to use `EkGuruVoice`; the direct `test-voice.mjs` now passes (28 mocked cases), as do the Academy, shell, editorial metadata, full-page inventory and copy-index checks. The full build was not rerun after that correction, so subsequent gates and write-mode rebuild compatibility remain unverified. Do not deploy until the complete build passes.
- A local static preview is available in this session. No browser binary was available for real-browser, viewport, print-preview, screen-reader, colour contrast or Web Vitals testing; no screenshots, performance targets or WCAG conformance are claimed. JSDOM is not a substitute for these checks.

## Next work, in order

1. Complete the full `build-all.py check` and validate existing shell/ultra/page-layer ownership and inventory freshness. Resolve any failures without changing existing indexing contracts; verify write-mode rebuilds preserve all Academy content.
2. Commission a qualified Hindi educator to review the new copy, translations, quiz and all reused resources; record actual review dates, credentials/permissions only when known. Commission pedagogically verified, reusable stroke data with handwriting variants. Do not infer paths from font outlines.
3. Establish a chapter/lesson manifest and validate traversal, unique IDs, full reachability, prev/next and phase transitions; map existing material before authoring genuinely missing chapters. Build no-JS navigation, responsive sidebar/drawer and local continue/progress without damaging legacy data.
4. Finish vowel chapter objectives, dialogues, listening, assessment, accessibility, worksheet variants and verified stroke-order instructions. Then develop Devanagari, kids, beginner, intermediate, advanced and adult content in reviewed batches. Track actual counts against the 200 chapter / 10k vocabulary / 5k sentences / 4k assessments / 1k activities / 200 packs / 100 stories targets, without filler.
5. Consolidate vocabulary without losing provenance, use the existing shared voice adapter and licensed recording manifest, expand games and print layouts. Add genuine offline and keyboard equivalents; test storage denial, corruption and migrations.
6. Obtain owner approval before indexing; add sitemap entries only for eligible reviewed pages, validate metadata/structured data and reciprocal hreflang only for genuine equivalents. No GEO markup guarantees discovery.
7. Test all requested widths (320–1920), print A4/Letter, no-JS, pointer/touch/stylus, real Hindi voices and unsupported devices, accessibility with assistive tech, performance in the field, SEO and complete regression. Only then seek owner deployment approval.

# Existing Hindi page expansion: Foundation batch 1

## Owner-confirmed scope

The owner selected **expand 1,000+ existing pages**, with **3,000+ substantive words per selected page** as the long-term target, starting with Hindi Foundation/beginner. This is a new scope beyond the earlier 1,540-item practice collection. Neither 1,000 expanded pages nor the ten-chapter batch is complete. No release of this expansion is claimed.

This implementation starts with **one existing URL**, not a new competing lesson:
`/learn/hindi/foundation/swar/`.

### Implemented chapter

- **3,293 newly authored English explanatory words**, independently counted from paragraph fields only. Existing text, headings, Hindi models, romanisation, questions/answers, navigation and button labels are not used to reach the 3,000-word floor.
- **17 topic-specific sections**, plus an introductory heading: learning goals, script orientation, independent vowels versus matras, six sound/shape comparisons, ऋ, anusvara/visarga, keyword reading, writing/correction routine, honest listening, mixed recall, error repair, self-check and a follow-up practice plan.
- Hindi examples with romanisation/meaning and user-triggered Listen through existing `EkGuruVoice`. Five native disclosure self-checks with explanatory answers.
- Existing letter cards, quizzes/questions, trace tools, optional lesson-completion control, previous/next links, book-mode storage keys and step/whole-lesson controls are retained.
- Corrected this chapter's source and rendered introductory guidance: eleven independent vowels plus two additional chart forms; vowel quality/duration with context-dependent timing, rather than an exact duration rule; anusvara/visarga pronunciation not reduced to one universal English sound.
- Existing title, h1, canonical, breadcrumb and **noindex, follow** decision preserved. Description, Open Graph/Twitter descriptions and existing LearningResource description now reflect the richer actual content. No FAQ schema, new indexable URL, unsupported author/reviewer claim or SEO ranking guarantee.

## First ten existing chapters

Counts below are the generated report's current own-text tokens, not an editorial word-count certification: whitespace-delimited tokens containing a letter after shared chrome exclusions. The strict 3,000-word gate instead counts only newly authored English prose. The report distinguishes those measurements deliberately.

| Chapter | Existing slug | Current own-text tokens | Expansion status / next focus |
|---|---|---:|---|
| 1 | swar | 4,320 | Expanded draft: 3,293 added prose words; native review pending |
| 2 | vyanjan-1 | 492 | Pending: place of articulation, aspiration, voiced pairs, listening/error routines |
| 3 | vyanjan-2 | 518 | Pending: dental/retroflex distinctions, comparison practice, nukta preview |
| 4 | vyanjan-3 | 570 | Pending: lips, semivowels, sibilants, conjuncts versus single consonants |
| 5 | bina-matra | 1,015 | Pending: inherent vowel, blending, schwa caveats, worked word reading |
| 6 | aa-ki-matra | 1,070 | Pending: independent आ versus dependent ा, reading/writing error correction |
| 7 | i-ki-matra | 944 | Pending: pre-base written placement versus spoken order, controlled decoding |
| 8 | ee-ki-matra | 1,005 | Pending: compare ि/ी, word reading and source-appropriate meanings |
| 9 | u-ki-matra | 915 | Pending: below-base sign recognition, legibility, cumulative reading |
| 10 | oo-ki-matra | 977 | Pending: distinguish ु/ू and cumulative listening/reading practice |

Machine-readable tracker: `data/quality/hindi-foundation-expansion.json`. This is a first-ten census, **not** a completed census or editorial plan for all 1,000+ pages. Further topic planning should avoid copying the same explanations onto every chapter merely to meet a number. Do not expand utility, legal, payment or tutor-profile pages into artificial language lessons.

## Implementation and regeneration

- Authored source: `data/content/hindi-foundation-depth.json`.
- Additive builder: `tools/build-hindi-foundation-depth.py`; `--check` is read-only and detects stale generated chapter content/report.
- Existing Foundation generator also consumes the source, so rebuilding the original lesson retains the expansion. The additive builder is registered in `tools/build-all.py`.
- Scoped stylesheet: `css/hindi-foundation-depth.css`. No new JS, libraries, package manifest changes, new progress/SRS storage or audio system.
- Prose under the floor, duplicate paragraphs, duplicate section IDs and invalid listening examples fail validation. Each future chapter requires its own authored content, not a loop that multiplies generic paragraphs.
- Browser book mode reads the new direct h2 sections as ordinary steps. Storybook runtime rewrites heading IDs; QA uses accessible heading names rather than assuming source IDs survive runtime. No links to the new section IDs are advertised.

## QA performed

- `python3 -B tests/regression/test-hindi-foundation-depth.py`: **6 regression tests pass**. Conservative word count, duplicate/underlength rejection, static metadata/schema consistency, existing links/voice labels, original generator retention without writing files, honest ten-chapter tracker.
- `python3 -B tools/build-hindi-foundation.py --check`: existing cumulative-sign primer validation passes. New models use the existing vowel-chart forms and keyword previews; no claim that all preview keywords are independently decodable at lesson one.
- `node tests/regression/test-book-mode.mjs`: **44 checks pass**, including the expanded swar page (27 steps) and existing Hindi/other-language book pages. jsdom logs its known missing canvas-rendering implementation; no canvas package was installed and the tests report 0 failed.
- Chromium **158.0.8127.0**, local static server with external requests blocked: 390/768/1280px, keyboard step selection, whole-lesson mode, keyboard answer disclosure, unchanged completion control. No local HTTP errors, page exceptions or document overflow in those cases.
- Additional 320px reduced-motion light/dark/contrast layouts: no document overflow.
- JavaScript disabled: all 18 added headings and self-check disclosures remain readable.
- Simulated installed `hi-IN` voice through the real shared adapter: exact selected letter passed to speech, no autoplay. No real-device voice quality or pronunciation review claim.
- Inspected mobile/light and 320px/dark paragraph/model screenshots. Whole-element screenshot captures include the existing fixed header/book rail/dock while scrolling; no new chrome system was introduced.
- `python3 tools/build-all.py check`: **PASS** after this expansion, including existing learning collection, original pilot, generated inventories, SEO/discovery, storage and offline-worker checks. Excluded log: `.cache/hindi-depth-build-check.log`.
- Excluded browser harness/evidence: `.cache/hindi-pilot-qa/depth-browser.cjs`, `.cache/hindi-depth-qa/`.

## Explicit remaining work

Nine chapters in this first batch still need authored expansion; the wider 1,000+ page program needs an eligible-page census and topic-by-topic plan. Native Hindi editorial review and real-voice listening review are not recorded. No physical-device, screen-reader, field-performance, production browser, publication or ranking evidence is asserted. Changes remain on the active branch, with no deployment of this new work.

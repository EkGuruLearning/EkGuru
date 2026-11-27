# Hindi learning collection — implementation and QA

## Scope and entry points

Implemented on the existing `/learn/hindi/practice/#hindi-learning-library` hub, linked from the Hindi hub's practice section and the sentence-structure pilot's “Keep going” grid. No new indexable URLs or competing course, SRS or progress system. This expansion is prepared on the active working branch. A branch commit/push is not a merge or live deployment; no live release is claimed here.

**1,540 distinct Hindi learning models:** 49 letter/sound models, 1,014 words/expressions, 463 sentence models, 14 connected paragraph readings. Activity variants, comprehension questions, Listen buttons and repeated source text are not counted as additional items. “1,000+” refers to combined learning items, not pages or newly authored lessons.

- Reuse: Foundation letter models/keywords/grouped words/sentences and six canonical A1/A2/B1/B2/C1/C2 course vocabulary, grammar examples and dialogue turns. Each has a working source lesson/fragment link. Half-step and extension courses are not imported.
- New content: two fictional paragraphs per stage, Foundation through C2, with romanisation, English meaning, focus, comprehension question and model answer. Input: `data/content/hindi-library-readings.json`.
- Generator: `tools/build-hindi-learning-library.py`, with a read-only `--check`; integrated into `tools/build-all.py`. The legacy `practice_hub()` generator retains the collection and assets.
- Deduplication: NFC, case folding and removal of whitespace/common punctuation. Hindi vowel marks, nukta and other combining characters are retained. First source wins; stable SHA-256-derived IDs; stage order then letters → words → sentences → paragraphs. This is textual deduplication, not a claim that near-synonymous items are unique concepts.

## Learning behavior

Stage/activity/search filters, explicit start and paragraph-room shortcuts, bounded previous/next navigation with focus returned to the current item. A keyboard-submittable item-number form jumps within the current selection; invalid, fractional and out-of-range numbers are refused with accessible feedback, and empty selections disable the form. Romanisation and English are native disclosure controls. All 1,014 vocabulary items also offer a native radio-button meaning exercise with explicit check, retry and clear feedback. Choices are source glosses from the same stage, with exact duplicates and substring-overlapping gloss variants excluded; this is a source-gloss match, not a claim about every possible meaning or a native-reviewed assessment. No scores or new stores are introduced, and these activity variants do not inflate the item count. Sentence models offer button/keyboard word assembly with explicit model-only feedback (not a rejection of all other valid Hindi word orders). Paragraphs provide whole-text and individual-sentence Listen buttons, optional typed notes and a disclosed model answer. Notes explicitly are not saved and clear when selecting another item.

Uses existing `EkGuruVoice` only: user-triggered matching Hindi browser/system TTS, no English fallback or microphone. Existing picker, speed, stop and repeat controls remain owned by the shared adapter. No claimed native recordings. No actual installed voice, pronunciation quality or universal offline-audio guarantee was tested.

“Add to review” uses `EkGuruGlobalSRS.add`, its existing Hindi deck, deduplication and write-failure/corruption handling. Opening, listening and model building do not award completion or certify proficiency. No new storage keys, network API, dependency, analytics, paywall, autoplay, worker policy change or package manifest change.

Existing offline pin controls/worker save the page and its public JS/CSS assets. Without JavaScript the original source lesson links and all 14 new paragraph texts/translations/questions/answers remain available. If library assets fail to load, an honest fallback message and source links remain.

## Checks executed

- `node tests/regression/test-hindi-learning-library.mjs`: **16 checks pass**: advertised counts/unique Hindi/IDs, aligned search/social metadata and introduction with preserved indexing, stage order, every source/fragment exists, no initialization storage/autoplay/network, exact-text shared voice, filtering/empty states, validated direct navigation, word-practice feedback/retry/reset in all seven stages, exhaustive four-choice/unique-gloss checks for all 1,014 vocabulary items, sentence builder feedback, paragraph controls, existing review deduplication/persistence, corrupt deck preservation, unavailable Hindi voice, no-JS/legacy links/reduced motion.
- `node --check js/hindi-learning-library.js`: pass.
- `python3 tools/build-hindi-learning-library.py --check`: current, 0 stale outputs.
- Exercised the real legacy `practice_hub()` regeneration in a try/finally that restored decorated HTML: one collection and one copy of each required script retained.
- Chromium **158.0.8127.0**, local static server: 390/768/1280/1440px viewports; initial letter, direct navigation with Enter and invalid-jump feedback, native word-choice selection with Space/check/clear, keyboard tile entry/check/clear, C2 paragraph/model answer, navigation boundaries/focus. No local 4xx/5xx, page exceptions or document overflow in these cases.
- Additional 320px reduced-motion checks in light/dark/contrast themes: paragraph and word-choice layouts, no document overflow. Inspected generated letter/mobile/advanced-reading screenshots; whole-element captures can include fixed global chrome while scrolling.
- JavaScript disabled: 14 native reading disclosures, first text opened/readable; interactive app hidden.
- Shared voice browser test with a **simulated** installed `hi-IN` voice: no autoplay, whole paragraph and individual sentence text passed correctly. No real native audio quality claim.
- Real service-worker test: explicitly pin practice hub; network off; reload all 1,540 items; select/read C2 paragraph; reconnect and remove pin successfully. Audio is device-dependent and is not bundled.
- `python3 tools/build-all.py check`: **PASS**, including existing pilot, SEO, discovery, storage, retention, offline-worker, inventories, ownership fingerprints and generated-layer checks. Log: `.cache/hindi-library-build-check.log` (excluded).
- Browser evidence and result JSON: `.cache/hindi-library-qa/` (excluded). Browser harness: `.cache/hindi-pilot-qa/library-browser.cjs` (temporary tooling; no package changes).

Generated assets: CSS 4,819 bytes (1,553 bytes gzip), UI 13,006 bytes (4,100 bytes gzip), content 406,108 bytes (78,275 bytes gzip). One current item is rendered, not 1,540 DOM cards. No Lighthouse, field CWV, physical-device, real screen-reader, OS-zoom or native editorial review claim.

## Remaining limits

Foundation paragraphs are guided readings after the letter/matra primer, not strictly cumulative-sign drills. A1–C2 are intended stages inherited from the existing course, not CEFR certification or evidence of mastery. New and reused text is explicitly not marked native-reviewed; a qualified Hindi editor should review pronunciation guides, translations, stage suitability and source material before any editorial approval claim. Existing course content was reused rather than silently “correcting” unrelated quizzes or lessons. No independent production test or deployment of this expansion has occurred.

# Phase 4 — Original Content Rebuild (in progress)

**Status:** In progress; Batch 1 is repository-checked, not editorially or natively reviewed.  
**Batch date:** 2026-10-05  
**Scope:** Ten world-course quiz pages and their ten course-hub summaries.

## Batch 1 — course quiz pages

Pages updated:

- `/languages/ar/quiz/`
- `/languages/de/quiz/`
- `/languages/es/quiz/`
- `/languages/fr/quiz/`
- `/languages/it/quiz/`
- `/languages/ja/quiz/`
- `/languages/ko/quiz/`
- `/languages/pt/quiz/`
- `/languages/ru/quiz/`
- `/languages/zh/quiz/`

The source-level comparison found two concrete issues in the generated quiz experience. First, visible copy exposed internal `EKGURU_COURSE_*` identifiers. Second, the positional `%s` template had shifted internal identifiers into the emitted JavaScript: for example, the page referenced a lower-case `window.ar` while the course bank exports `window.EKGURU_COURSE_AR`, and feedback element IDs did not consistently match the markup. The generated output therefore had a source-level wiring mismatch; the browser gate was not available in this environment, so no browser-runtime result is claimed.

The builder now uses named literal replacement tokens for visible language names, course-bank globals, and control IDs. The rebuilt pages:

- show a per-topic question count and links to the corresponding course lessons, derived from the repository's current quiz and lesson data;
- offer only round lengths the selected topic can supply, plus an “All available” option for smaller banks;
- link each answer explanation back to the question's source lesson;
- report the round score and prevent a second answer click from incrementing it again; and
- describe the daily shuffle accurately: a shorter round can select a different subset, while a full-topic round changes order rather than inventing questions.

The ten course hubs now say that the 20-question bank is divided across lesson topics and that available round lengths vary by topic. Existing page shells, notices, voice/audio controls, indexing directives, and course data were preserved. No course questions were deleted, and no publication/indexing state was changed.

## Repository checks

Passed:

- `python3 tools/test-world-course-quiz-content.py` — all 10 quiz pages match the source builder's generated content/script fragment; topic counts, lesson links, course-bank bindings, and JavaScript syntax checked.
- `python3 tools/test-phase3-originality-audit.py` — the Phase 3 baseline still has 2,720 inventoried pages and continues to claim zero completed human, native-language, source/fact, or external-similarity reviews.
- `python3 tools/test-partial-course-publication.py` — partial-course publication boundary remains intact.
- `python3 -m py_compile tools/build-world-course.py tools/test-world-course-quiz-content.py`
- `git diff --check`

Not completed:

- `python3 tools/test-phase7c-stage7.py` could not start because the environment lacks the Python `playwright` package (`ModuleNotFoundError`). The temporary local HTTP server was stopped. No live production HTTP check was made.
- No human editorial review, native-language review, source/fact verification, external similarity review, AdSense/Search Console check, or production crawl was performed.

## Remaining Phase 4 work

The Phase 3 artifact remains a point-in-time baseline, so its visible-token flags and P1 counts describe pre-rebuild repository content, not current page state. It contained 88 `P1_REVIEW` observations. This batch rebuilt the ten world-course quiz pages; the remaining 78 observations have not been individually adjudicated. They include answer/article pages, language lessons, and Indian-language learning and practice pages. Their heuristic queue status is not a finding that every page is defective or requires more prose.

Phase 4 remains open. Continue by inspecting each remaining candidate and its actual source/template, preserving short utility pages when the brevity fits their purpose. Do not force word-count targets, remove content automatically, or treat this repository-only rebuild as human/native approval or factual verification.

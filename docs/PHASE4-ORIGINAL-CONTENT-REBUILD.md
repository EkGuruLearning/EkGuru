# Phase 4 — Original Content Rebuild (in progress)

- **Status:** In progress; Batches 1–2 are repository-checked, not editorially or natively reviewed.
- **Batch date:** 2026-10-05
- **Scope so far:** Ten world-course quiz pages and their course hubs, plus two world-course number lessons.

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

The ten course hubs now say that the question bank is divided across lesson topics and that available round lengths vary by topic. Existing page shells, notices, voice/audio controls, indexing directives, and course data were preserved. No course questions were deleted, and no publication/indexing state was changed.

## Batch 2 — Spanish and French numbers lessons

Pages updated:

- `/languages/es/lessons/numbers-1-to-20/`
- `/languages/fr/lessons/numbers-1-to-20/`

Each lesson's explanatory paragraphs already named the numbers from 1 through 20, but its reference table contained only 12 selected entries. The source tables now provide all 20 values in order. A short recall task asks learners to reproduce the range and check spelling cues that already appear in that lesson's own explanation; the existing quiz/course links remain in place. This makes the table match the page's stated 1–20 intent without adding unsupported number forms or claiming native review.

The page shells, review notices, browser-voice disclosure, indexing directives, and navigation were retained. The source lesson data remains the generator input.

## Repository triage note

Not every short Phase 3 candidate needs more copy. Source inspection shows the seven Indian-language `advanced/` pages are topic-navigation hubs: each lists module-specific titles and ledes that route to substantial word, phrase, and dialogue modules. The Hindi advanced page is a separate, more detailed guide with audience/context, topic cards, and practice links. They were left compact in this batch rather than padded solely to cross a word-count threshold. This is repository-level triage only, not human editorial or native-language approval.

## Repository checks

Passed:

- `python3 tools/test-world-course-quiz-content.py` — all 10 quiz content/script fragments match the source builder; topic counts, lesson links, course-bank bindings, and JavaScript syntax checked.
- `python3 tools/test-world-course-numbers-content.py` — Spanish and French tables each contain 20 ordered rows matching their source data; existing page layers remain present.
- `python3 tools/test-phase3-originality-audit.py` — the Phase 3 baseline still has 2,720 inventoried pages and claims zero completed human, native-language, source/fact, or external-similarity reviews.
- `python3 tools/test-partial-course-publication.py` — partial-course publication boundary remains intact.
- `python3 -m py_compile tools/build-world-course.py tools/build-all.py tools/course-data/es.py tools/course-data/fr.py tools/test-world-course-quiz-content.py tools/test-world-course-numbers-content.py`
- `git diff --check`

Not completed:

- `python3 tools/test-phase7c-stage7.py` could not start because the environment lacks the Python `playwright` package (`ModuleNotFoundError`). No browser-runtime result is claimed. The temporary local HTTP server from Batch 1 was stopped.
- No human editorial review, native-language review, source/fact verification, external similarity review, AdSense/Search Console check, or production crawl was performed.

## Remaining Phase 4 work

The Phase 3 artifact remains a point-in-time baseline, so its visible-token flags and P1 counts describe pre-rebuild repository content, not current page state. It contained 88 `P1_REVIEW` observations. Batches 1–2 rebuilt 12 of those pages (ten quizzes and two lessons); 76 observations have not received a Phase 4 rebuild. Some candidates have received limited repository-only triage, including the compact advanced hubs above, but none of that is human/native approval or a current defect finding.

Continue by inspecting each remaining candidate and its actual source/template, preserving short utility pages when the brevity fits their purpose. Do not force word-count targets, remove content automatically, or treat this repository-only rebuild as human/native approval or factual verification.

# Phase 4 — Original Content Rebuild (in progress)

- **Status:** In progress; Batches 1–4 are repository-checked, not editorially or natively reviewed.
- **Batch date:** 2026-10-06
- **Scope so far:** Ten world-course quiz pages and their course hubs, two world-course number lessons, one Daily Hindi lesson, one Hindi hunger answer, and band-only corrections on ten related Hindi answer/ask pages.

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

## Batch 3 — Daily Hindi Day 23, future forms

Page updated:

- `/daily-hindi/day-23/`

The Day 23 row in the frozen Phase 3 audit is a `P1_REVIEW` queue candidate, not a confirmed defect. Inspection found a compressed, incomplete future-tense rule and a “mistake to avoid” section that did not identify a mistake. The lesson now explains how the four shown forms change with the subject, labels the table as a starter example rather than a full conjugation chart, and replaces the empty warning with a concrete agreement and `कल` context note. The weekly practice now asks for seven future-tense sentences, uses at least one of the day's four verbs, and includes an aloud check. The page shell, word list, navigation, canonical URL, and indexing directives were retained; the summary descriptions were updated to match the lesson.

The four example forms are also present in the repository's `data/courses/phase-2/hi_A2.json` future lesson. This is an internal consistency check only, not external source verification or linguistic approval. The lesson text lives in the checked-in HTML; inspection found no dedicated Day 23 content generator. No word-count target was used.

## Batch 4 — Hindi hunger answer and next-step routing

Pages updated:

- `/answers/how-to-say-i-am-hungry-in-hindi/` — `P1_REVIEW` candidate; answer copy and generated band.
- Band-only corrections on ten `P2_REVIEW` Hindi pages:
  - `/answers/how-to-say-i-am-learning-hindi/`
  - `/ask/how-to-say-what-is-your-name-in-hindi/`
  - `/ask/how-to-say-yes-and-no-in-hindi/`
  - `/ask/is-duolingo-good-for-hindi/`
  - `/ask/is-hindi-hard-to-learn/`
  - `/ask/is-hindi-or-spanish-easier-to-learn/`
  - `/ask/is-hindi-useful-to-learn/`
  - `/ask/is-italki-or-preply-better-for-hindi/`
  - `/ask/what-is-the-best-age-to-learn-hindi/`
  - `/ask/what-is-the-hardest-part-of-hindi/`

The hunger answer now uses phrases that are present in repository learning sources: `मुझे भूख लगी है` and `मुझे प्यास लगी है` from the Hindi phrasebook, `मुझे ठंड लग रही है` from the B1 weather lesson, and `मुझे एक थाली दीजिए` (“Please give me one plate”) from A2 restaurant lesson `A2-U3-L3`. The previous blanket judgement about `main bhookha hoon` and the `खाना चाहिए` restaurant recommendation were removed because they were not supported by the inspected repository sources. The copy was not expanded to meet a word-count threshold. A stray quote in the course-link `href` was also corrected. These are repository consistency checks, not external factual verification or native-language approval.

The shared page-layer selector now resolves the Hindi roots (`answers/`, `ask/`, `daily-hindi/`, and `name-in-hindi/`) before inspecting individual path segments. This prevents Hindi slugs from being mistaken for language codes embedded within words: the two answer pages had Amharic bands, while a full generator check also found nine ask-page bands routed to Icelandic or Norwegian. Only generated next-step bands were changed on those ten adjacent P2 pages; their authored answer text was left unchanged.

## Repository triage note

Not every short Phase 3 candidate needs more copy. Source inspection shows the seven Indian-language `advanced/` pages are topic-navigation hubs: each lists module-specific titles and ledes that route to substantial word, phrase, and dialogue modules. The Hindi advanced page is a separate, more detailed guide with audience/context, topic cards, and practice links. They were left compact in this batch rather than padded solely to cross a word-count threshold. This is repository-level triage only, not human editorial or native-language approval.

## Repository checks

Passed:

- `python3 tools/test-world-course-quiz-content.py` — all 10 quiz content/script fragments match the source builder; topic counts, lesson links, course-bank bindings, and JavaScript syntax checked.
- `python3 tools/test-world-course-numbers-content.py` — Spanish and French tables each contain 20 ordered rows matching their source data; existing page layers remain present.
- `python3 tools/test-daily-hindi-future-content.py` — the Day 23 forms match the in-repository example, and the task, metadata, and responsive table labels are present. This is repository consistency, not linguistic validation.
- `python3 tools/test-hindi-hunger-answer-content.py` — the answer copy, summary metadata, QAPage text, restaurant example, and Hindi route bands match repository sources and the page-layer selector. Native-language review remains pending.
- `python3 tools/build-page-layer.py --check` — all generated page-layer pages are current after the Hindi route correction.
- `node tools/test-page-layer.mjs` — all 24 existing checks pass across 1,703 pages.
- `python3 -m py_compile tools/build-page-layer.py tools/test-hindi-hunger-answer-content.py`
- `python3 tools/test-phase3-originality-audit.py` — the Phase 3 baseline still has 2,720 inventoried pages and claims zero completed human, native-language, source/fact, or external-similarity reviews.
- `python3 tools/test-partial-course-publication.py` — partial-course publication boundary remains intact.
- `python3 tools/build-legacy-pages.py --check --only daily-hindi/day-23/index.html` — the edited page remains on the reading layer.
- `python3 -m py_compile tools/build-world-course.py tools/course-data/es.py tools/course-data/fr.py tools/test-world-course-quiz-content.py tools/test-world-course-numbers-content.py`
- `python3 -m py_compile tools/build-all.py tools/test-daily-hindi-future-content.py`
- `git diff --check`

Not completed:

- `python3 tools/test-phase7c-stage7.py` could not start because the environment lacks the Python `playwright` package (`ModuleNotFoundError`). No browser-runtime result is claimed. The temporary local HTTP server from Batch 1 was stopped.
- `node tools/test-voice.mjs` could not start because `jsdom` is not installed. No voice-runtime result is claimed for this batch.
- No independent human editorial or native-language review, external source/fact verification or similarity review, AdSense/Search Console check, or production crawl was performed.

## Remaining Phase 4 work

The Phase 3 artifact remains a point-in-time baseline, so its visible-token flags and P1 counts describe pre-rebuild repository content, not current page state. It contained 88 `P1_REVIEW` observations. Batches 1–4 rebuilt 14 of those pages (ten quizzes, two lessons, one Daily Hindi lesson, and one Hindi answer); 74 observations have not received a Phase 4 rebuild. The ten related P2 pages in Batch 4 received only next-step-band corrections and are not counted as P1 rebuilds. Some candidates have received limited repository-only triage, including the compact advanced hubs above, but none of that is human/native approval or a current defect finding.

Continue by inspecting each remaining candidate and its actual source/template, preserving short utility pages when the brevity fits their purpose. Do not force word-count targets, remove content automatically, or treat this repository-only rebuild as human/native approval or factual verification.

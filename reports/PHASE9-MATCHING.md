# Phase 9 — matching-pairs interaction slice

**Status:** one focused increment; Phase 9 is not complete.

**Source command:** `Arena latest command  arena/Arena latest command  arena/01a0e655-ekguru/after fasst.md` — Phase 9.

**Existing handoff:** `reports/PHASE9-FLASHCARDS.md` identifies quiz question types as an open slice.

## What changed

- `js/course-player.js` now renders `type: "matching"` lesson-practice items as word-to-meaning pairs, using that lesson's existing vocabulary (`t` → `en`). It also accepts explicit `{left, right}` pairs for future final-test items.
- Meaning choices are shuffled; each native-script prompt has a labelled select; the learner must complete the set before checking. Results are scored once, wrong rows are marked, and the answer key is shown.
- Duplicate/empty terms or glosses are excluded to avoid ambiguous matching. When fewer than two unambiguous pairs remain, the existing interaction is retained rather than inventing content.
- Matching history uses a new key version so an old single-choice result is not presented as history for the new pair activity.

## Coverage and checks

`node tools/test-course-matching.mjs` exercises pair construction, explicit pairs, ambiguity fallback, accessible labels, incomplete submission, scoring, and answer reveal. It also scans the current course files: **1,446 of 1,832** existing matching prompts have at least two distinct pairs and can use the new UI. This is a data-shape coverage measure, not a linguistic-quality or native-speaker review.

`npm run test:courses` exited successfully: the placeholder, level-page, voice-button, and matching checks passed. Its pronunciation audit still reports **BLOCKED** because 0/5,694 published vocabulary items have source-referenced IPA; that is pre-existing and outside this slice.

## Still open

- Broader quiz coverage for other required types (including fill-in, reorder, listening, and reading) and richer authored question data.
- Printable worksheets (coordinate with the existing print-sheet pipeline), non-Latin-script typing coverage, and the custom deck builder.
- Independent linguistic/native-speaker review of the reused lesson vocabulary and all course content remains pending.

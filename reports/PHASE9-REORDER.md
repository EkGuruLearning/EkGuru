# Phase 9 — sentence-reordering interaction slice

**Status:** one focused increment; Phase 9 is not complete.

**Source command:** `Arena latest command  arena/Arena latest command  arena/01a0e655-ekguru/after fasst.md` — Phase 9.

**Previous increment:** `reports/PHASE9-MATCHING.md` records the matching-pairs activity.

## What changed

- Lesson-practice reorder types now share one renderer with final-test `type: "reorder"` items in `js/course-player.js`.
- Reorder words are native `<button type="button">` controls instead of clickable spans. Buttons have per-token accessible names (including an occurrence number), the course language and automatic text direction, and a visible keyboard-focus style.
- The available words are shuffled, each token can occur only once in the assembled order, and a polite live region announces it. Selecting a pressed token removes it; the button stays enabled while composing so keyboard focus is not lost. The learner can also clear a partial order; incomplete submissions are not scored. A completed answer is locked and checked against the existing authored answer. Incorrect answers reveal that answer through the established feedback.
- Existing one-token reorder prompts fall back to text entry; splitting such an answer into word tiles would create a trivial activity.
- `sw.js` now advances the cache generation so the revised course player is also refreshed for offline course use.
- No course text or answers were edited.

## Coverage and checks

`node tools/test-course-reorder.mjs` exercises the production reorder builder using a small fake DOM: semantic and labelled buttons, language/direction metadata, live preview, reversible selection without disabling the focused button, clear/reset, incomplete and completed submission, single-use scoring, answer reveal, and the one-token fallback. It scans the current course JSON: **1,813 of 1,912** lesson-practice reorder prompts contain multiple whitespace-separated tokens and can use the reorder UI; the other 99 keep text entry. This is data-shape coverage, not linguistic review. The current final-test data scan found no `type: "reorder"` items, so the final-test call site is implemented but has no current authored rows to exercise.

`npm run test:courses` exited successfully: placeholder checks passed (7), level-page checks passed (37), voice controls covered 12,599 authored items, matching checks passed (8), and reorder checks passed (6). The pronunciation sub-audit remains **BLOCKED**: 0/5,694 published vocabulary items have source-referenced IPA. That is not a passing pronunciation review.

`node --check` passed for the player and reorder test, `package.json` parsed, and `git diff --check` passed. No browser, keyboard-only session, or assistive-technology session was run; manual interaction/accessibility QA remains pending.

## Still open

- Broader quiz coverage for other required types (including fill-in, listening, and reading), richer authored question data, and any further interaction gaps.
- Printable worksheets (coordinate with the existing print-sheet pipeline), non-Latin-script typing coverage, and the custom deck builder.
- Independent linguistic/native-speaker review of reorder prompts, answers, lesson vocabulary, and all course content remains pending.

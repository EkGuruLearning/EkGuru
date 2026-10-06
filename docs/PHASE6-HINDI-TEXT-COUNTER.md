# Phase 6 — Hindi text counter (first utility increment)

**Date:** 2026-10-06
**Status:** First free utility delivered in the working tree; the wider Phase 6 writing-tool list is not complete.

## What this increment adds

`/toolbox/hindi-text-counter/` provides a browser-side counter for Hindi, English and mixed-script text. It is linked from the toolbox hub, listed in the tool registry, and included in the toolbox visual manifest, functional-test recipe and tool sitemap. The tool has no account, upload or Hindi-language API dependency. The counter script does not persist the input; the optional clipboard operation runs only after the visitor presses **Copy text**.

## Counting contract

- **Words** are runs of non-whitespace characters. This is not Hindi tokenization; punctuation stays attached and words without spaces are not guessed.
- **Unicode code points** count each code point once, including spaces and line breaks. They are not grapheme clusters or a promise of the number of visible letters.
- **Code points excluding whitespace** use JavaScript's whitespace definition; punctuation and emoji remain counted.
- **Sentence endings** are approximate groups of `.`, `?`, `!`, `।` or `॥`. The tool does not parse grammar, and abbreviations, decimals, ellipses or unmarked sentence endings can mislead it.
- **Paragraphs** are non-empty blocks separated by a blank line. A single line break inside a block does not start another paragraph.

The displayed Hindi sample is a demonstration string, not a reviewed language lesson. Native-speaker review of the page and its Hindi copy remains pending.

## Checks and limits

- `node tools/test-hindi-text-counter.mjs` — passed. Covers the counting rules, mixed Hindi/English input, Unicode edge cases, paragraph splitting, simulated UI events, copy fallback and static page contract. The UI simulation is not a real browser test.
- `node tools/test-toolbox-visuals.mjs` — passed (8 checks); `python3 tools/build-toolbox-visuals.py --check` — passed (14 plates, no stale pages).
- `python3 tools/build-sitemaps.py --check` — passed (1,007 indexed URL memberships, 0 invalid at the time of the check).
- `node tools/test-page-skeleton.mjs` — passed (2,723 pages; one main landmark and shell ordering).
- Local static-server GETs for the page, counter script, SVG and stylesheet returned HTTP 200; this is not a production HTTP check.
- Python/Node syntax checks for the edited scripts — passed.
- Real Chromium interaction, screen-reader/accessibility review, native-speaker review and production HTTP verification have **not** been performed. The tool registry records real-browser `last_tested` as `pending` rather than implying a QA pass.

This increment does not close the Phase 6 plan, and it does not close the separate Phase 4 queue: 74 of its frozen 88 P1 observations remain open.

# Phase 10 — level-gallery loading and asset budget

**Status:** scoped visual-delivery increment; Phase 10 is not complete.

**Source command:** `Arena latest command  arena/Arena latest command  arena/01a0e655-ekguru/after fasst.md` — Phase 10.

## What changed

- The generated language-hub level figures keep native `loading="lazy"` and now also use `decoding="async"`.
- `tools/build-visuals.py` enforces a maximum of 20 KB per SVG and a 300 KB aggregate limit for the eleven generated level figures on each language hub. The check covers the generated level-gallery assets only, not every image or other visual resource on the page.
- `tools/test-level-visuals.mjs` checks those per-file and per-gallery budgets, the rendered loading/decode attributes, and that the page's alt strings match the level/language manifest.

## Checks and measurements

- `python3 tools/build-visuals.py --check` passes for 32 languages × 11 figures and 32 hubs.
- `node tools/test-level-visuals.mjs` passes: **39 checks, 0 failures**.
- The 352 level SVGs are each below 20 KB; the largest measured file is **2,227 bytes**. The largest eleven-image gallery is **21,870 bytes** (about 21.9 KB).
- `python3 -m py_compile tools/build-visuals.py`, `node --check tools/test-level-visuals.mjs`, and `git diff --check` pass.
- `npm run test:courses` exits 0. Its pronunciation sub-audit remains **BLOCKED**: 0/5,694 published vocabulary items have source-referenced IPA; the course checks measure data/rendering coverage, not independent linguistic review.

The image checks are structural and byte-count checks, not a browser performance test. Non-empty, manifest-derived alt text has not received screen-reader, native-speaker or other human review. No live HTTP/production verification was performed.

## Still open in Phase 10

- Check dark-mode behavior, responsive rendering and print behavior in browsers; review the illustrations and alt text with appropriate human reviewers.
- Measure the complete image/resource weight of pages; the 300 KB assertion here covers only each hub's generated level gallery.
- Verify OG-image coverage and the icon system, and complete broader visual/reduced-motion browser review.
- Keep all human, linguistic, visual-browser and production reviews marked pending until actually performed.

# Phase 10 — neutral per-language patterns and reduced-motion follow-up

**Status:** one focused increment; Phase 10 is not complete.

**Source command:** `Arena latest command  arena/Arena latest command  arena/01a0e655-ekguru/after fasst.md` — Phase 10.

## What changed

- `tools/build-themes.py` now derives an abstract line-pattern angle and spacing deterministically from each language code. The 90 generated theme definitions have 90 distinct pattern configurations. Their metadata explicitly says these are decorative geometric patterns, not cultural motifs; no cultural meaning has been assigned.
- `css/ultra.css` applies the generated `--eg-pattern` to the language-page appearance panel, where the pattern token was previously defined but unused.
- The sentence-reorder tiles keep their hover lift and transition only for users who have not requested reduced motion; the `prefers-reduced-motion: reduce` rule removes both.
- `sw.js` advances the shell cache generation for the updated shared styles/player.

## Checks and limits

- `python3 tools/build-themes.py --check` passes for 90 themes.
- `node tools/test-theme-contrast.mjs` passes: **90 themes × 3 modes, 90 unique abstract patterns, 4,320 semantic contrast pairs**, plus the existing motion/voice hooks.
- `npm run test:courses` exits 0: placeholder checks (7), level-page checks (37), matching checks (8), and reorder checks (7) pass; voice controls cover 12,599 authored items. The pronunciation sub-audit remains **BLOCKED**: 0/5,694 published vocabulary items have source-referenced IPA.
- `node --check` passes for the player, service worker and JavaScript test scripts; `python3 -m py_compile tools/build-themes.py` and `git diff --check` pass.
- Full `python3 tools/build-all.py check` was not run; its pipeline begins with the separate live-sheet sync gate.

The reduced-motion regression check is source-level; no real-browser preference emulation was run. The theme patterns are neutral generated decoration—not native-speaker-reviewed cultural design—and 90 unique patterns do not mean 90 culturally distinct identities. No cultural, linguistic, factual or production review was performed.

## Still open in Phase 10

- Review language-specific colors, typography and any future cultural motifs with appropriate human/native-speaker or design reviewers; do not treat code-derived geometry as cultural representation.
- Expand review of illustrations and alt text beyond the generated level galleries, including dark-mode behavior and a full-page image-weight audit. The 32-hub gallery's lazy loading, async decode and SVG/gallery byte limits are covered in `reports/PHASE10-VISUAL-ASSET-BUDGET.md`; this is not a full-page budget or human review.
- Verify OG image coverage, the icon system, responsive breakpoints and print behavior against the command's gates.
- Run a broad reduced-motion browser matrix across components and pages.

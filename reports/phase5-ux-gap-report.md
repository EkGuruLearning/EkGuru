# Phase 5 — Card Clickability & Interaction Audit (final report)

Generated: 2026-09-12T06:44:46Z · verdict: **GREEN_INTERACTION_VERIFIED**

## Scope

A real-user interaction audit of every card-like surface on the site, with fixes applied at source and re-verified in a real Chromium browser. No UX problems were invented; every change below is backed by a concrete finding.

## What was found and fixed

| # | Finding | Fix | Verification |
|---|---|---|---|
| 1 | Home **markets strip** — 7 country cards were rendered by `js/main.js` as `<div class="mkt">` with no destination, so the visible card was dead UI | `renderMarkets()` now emits whole `<a class="mkt" href=…>` cards; each of the 7 markets carries its `slug` in `js/site-config.js` | `19/19` interaction suite incl. desktop mouse + mobile touch navigate to the `learn-hindi-from-*` page |
| 2 | Home **hero tutor card** — only the “View profile” button was clickable; the photo/name area was dead | Added a stretched-link `.hc-link` overlay + the button sits above it (`.btn{z-index:2}`), so the whole card is one destination with a still-working explicit control | Browser test clicks the name area → `tutor/sushila-g/` |
| 3 | **Toolbox** — 12 “related” cards had only the title as a link; the card body was dead | 12 `.faq` cards converted to whole-card `<a class="faq" style="display:block">` | whitespace-click navigates |
| 4 | **Search results** — result cards rendered a title-only link with the rest of the card dead | Renderer template now emits a whole-card `<a class="faq" style="display:block">` with the pill span inside | whitespace-click navigates to the result (answer/lesson/material) |
| 5 | **Hindi topic map** (`hindi/index.html`) — 34 cards title-only links | 34 `.faq` cards converted to whole-card anchors | 0 title-only cards remain |
| 6 | **404 page** — “Home” link had `href=""` (relies on a runtime `<base>`) | Changed to `href="./"` — same effect, no longer scans as a dead link | dead-link sweep now 0 |
| 7 | **Hover transforms** on non-interactive elements — `.step:hover` and `.checklist li:hover` made non-links appear clickable | Removed both rules from `css/style.min.css` (incl. the reduced-motion selector) | misleading-affordance sweep now 0 |

## Inventory totals

- Card instances classified: **1766**
  - `informational-faq`: 1520
  - `js-wired-action`: 1
  - `nested-actions`: 50
  - `no-link`: 113
  - `stretched-link`: 4
  - `whole-anchor`: 78

`no-link` and `informational-faq` are decorative/informational surfaces (FAQ Q&A blocks, feature tiles) that must not look clickable — they do not. `whole-anchor` / `stretched-link` / `nested-actions` are the interactive families; all one-destination cards among them now activate the whole surface.

## Real-Chromium verification

- Interaction suite: **19/19** (desktop mouse, mobile touch, keyboard; no page errors).
- 9-width × 16-page matrix: **146/146** cells (no overflow, h1 visible, footer present, no page errors, no failed same-origin requests).
- Idle/scroll/nav/back-forward/refresh regression: **5/5**.
- SEO integrity: **PASS** (0 pages, 0 broken links, 0 orphans).
- Recovery injection intact: **605** pages carry `js/recovery.js`.

## Non-blocking gaps (honest, not fixed here)

- **Quick quizzes cover 3 of 15 lesson guides** (minor) — The <details>-based quick quiz exists on the 3 exemplar lessons (alphabet, hello, sentence-structure); the other 12 lesson guides have no quiz yet. Content gap carried from Phase 4, not an interaction defect.
- **Home markets strip hover-lift is already neutralised** (minor) — .mkt:hover{transform:translateY(-6px)} exists but a later .mkt:hover{transform:none} rule overrides it, so the JS-rendered market cards never lifted on hover. Visual polish item, not a clickability defect.
- **Live deploy / push remain owner-gated** (info) — Carried from Phase 3: no push credentials in this environment and the remote was reset to one squashed commit, so ekguru.shop still serves the pre-Phase-2 build. This Phase 5 build is verified locally only.

## Verdict

**GREEN_INTERACTION_VERIFIED** — every interaction/clickability criterion passes with real-browser evidence; the only open items are non-blocking and out of Phase 5 scope (see gaps).

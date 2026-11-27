# Hindi sentence-structure pilot — implementation and QA

Editorial date: 2026-11-24. Scope: `/learn/hindi-sentence-structure/` only.

## Implementation

- Kept the existing URL, title/H1, canonical, indexability, breadcrumbs, three quick-check questions/answers, four vocabulary flip cards and course/resource relationships.
- Added explicit objectives, a labelled subject/object/verb-phrase example, explanatory highlights and three native-button sentence-building tasks. Incorrect feedback explains the neutral model without declaring other Hindi orders impossible. Incomplete attempts are unscored; revealing is not counted; repeated checks do not increase the visit-only built count.
- Qualified absolute verb-order and learning-timeline promises. Retained the longer Reena worked example and postposition comparison. Existing generated quiz answers remain unchanged, with a neutral-pattern context note immediately above them.
- Linked the existing sentence-builder lab, sentence-pattern reference, postposition reference and local review deck. This lesson does not automatically create review cards.
- Scoped CSS/JS to this lesson. No shared component, service-worker, storage key, progress/completion semantics, SRS, dependency manifest, payment, booking, advertising configuration or tutor code changed. Existing theme accents remain shared.
- Kept the shared storybook owner of card flipping. Added pressed-state synchronization and prevented a nested Listen keypress from flipping its parent card.
- Restored the pilot's stable heading anchors after storybook's TOC generation, updating those TOC links locally. Shared storybook source is untouched.
- Updated this page's descriptions and actual modification date without claiming a native review. Refreshed its editorial metadata, copy fingerprint, and the three existing inventory reports. Other inventory changes are inbound counts on four newly linked destinations, not edits to those pages.

Primary files: `learn/hindi-sentence-structure/index.html`, `css/hindi-sentence-lesson.css`, `js/hindi-sentence-lesson.js`, `tools/test-hindi-sentence-lesson.mjs`.

## Browser evidence

Headless Chromium **158.0.8127.0**, local Python static server on port 4173. Temporary Playwright/Chromium/font packages were installed outside project dependencies with approval. Hindi glyphs used a temporary Noto Sans Devanagari font. External requests were blocked consistently: this is not a production/network-services audit.

Local, non-Git evidence: `reports/hindi-sentence-pilot-qa/`. This directory is locally excluded from Git and the existing public deploy builder excludes all of `reports/`. Temporary packages remain under `.cache/hindi-pilot-qa/`, also excluded from the public deploy set. The copied `pilot-browser.cjs` and `remaining.cjs` record the browser assertions; their runtime dependencies are temporary rather than project dependencies.

| Check | Result |
| --- | --- |
| Before/after at 390, 768, 1280, 1440 CSS px | PASS: no horizontal document overflow or page errors, one H1 and three retained quick checks |
| Three authored sentence models | PASS: incomplete, incorrect, correct, repeated check, clear, reveal, next and reload |
| Completion check-in | PASS: existing completion control survives reload using existing Hindi progress storage |
| Native keyboard | PASS: Enter/Space select and remove a word; card flip state; nested Listen does not flip card |
| No JavaScript (after) | PASS: static models and card backs readable; nonfunctional exercise and demo controls stay hidden |
| Reduced motion (after) | PASS: same highlight teaching state, no highlight transform |
| Appearance modes | PASS: light/dark/high-contrast controls, no document overflow; screenshots captured |
| Reflow | PASS at 320px and 640px CSS viewport; this is not an OS/browser-toolbar zoom measurement |
| No Hindi voice | PASS: honest unavailable state; no claim of native or offline audio availability |
| Offline | PASS: save with existing control, reload with network disabled, render and build a model, reconnect, reload saved state and remove |
| Local HTTP errors | Zero in the final extra-interaction/offline run |

Evidence names include `before-{width}-{top,full}.png`, `after-{width}-{top,full}.png`, `after-{width}-builder.png`, `after-nojs.png`, `after-dark-reduced.png`, `after-{light,dark,contrast}-builder.png`, `after-320-reflow.png`, `after-offline-builder.png`, `browser-results.json` and `remaining-results.json`.

Before captures were initially taken before editing. The final comparison rerenders the original HEAD lesson HTML in the same browser environment against the unchanged shared assets. Before no-JS/reduced-motion screenshots are **not available**: a supplementary capture attempt failed at Chromium startup. After no-JS/reduced-motion assertions and screenshots succeeded. Fixed shared navigation can overlay content in element/full-page screenshots as it does during scrolling; the native controls remain in the existing shell.

## Repeatable repository checks

Run the new dependency-free-at-runtime regression test using the repository's existing jsdom dev dependency:

```sh
node tools/test-hindi-sentence-lesson.mjs
```

Result: **13 checks passed**. The test also verifies this lesson's exact copy fingerprint and resolves local resource links. New CSS + JS: **5,070 bytes combined gzip**, measured independently with Node zlib. This is an added-asset budget, not total page weight or a Core Web Vitals result.

Also passed after implementation:

- `node --check js/hindi-sentence-lesson.js` and `git diff --check`.
- `python3 tools/ultra/contract.py`: zero indexing/canonical freeze violations.
- `python3 tools/apply-ultra.py --check`: zero stale pages.
- `python3 tools/update-editorial-metadata.py --check --date 2026-11-24`: zero newly measured pages.
- `python3 tools/build-full-page-inventory.py --check`: current, 3,014 pages.
- `python3 tools/build-phase2-content-inventory.py --check`: current.
- `python3 tools/build-phase3-originality-audit.py --check`: current; human review remains pending.
- `python3 tools/build-public-dist.py --check`: public-path/privacy checks passed.
- Existing learning storage 10/10, learning worker 13/13, voice UX 8/8, voice 28/28, course reorder 7 checks, book mode 44/44, menu/search and shell drawer checks.
- Shared theme suite: 90 themes × 3 modes / 4,320 semantic color pairs. This is not a standalone accessibility certification of the pilot.

Book-mode jsdom runs emitted the existing missing-canvas implementation warnings; its assertions passed. Browser runs did not report page errors.

## Known repository issue and limits

**Resolved in the subsequently approved global technical pass:** `node tools/build-copy-index.js --check` now passes, as does the existing ownership-matcher suite. At pilot completion the site-wide index had 1,869 unrelated stale rows, which were deliberately left alone under the pilot-only scope. The user then approved global technical fixes, allowing the existing generator to refresh all current fingerprints without editing those pages. See [global discovery QA](global-discovery-qa.md) for the follow-up shared SEO changes. The pilot test still verifies its own row. No all-green master-build claim is made here.

No human/native Hindi review, screen-reader session, physical Android/iOS test, production external-service test, field performance measurement or real-device TTS quality review was performed. Native review status remains “not recorded.” No commit, push, pull request, merge or deployment was performed. This is a reviewable one-lesson pilot, not a course-wide rollout.

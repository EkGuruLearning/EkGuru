# Phase 31 — global language, AdSense and monetization audit

Recorded: 2026-09-27T16:12:54Z

This phase measured the current tree instead of repeating an old report.

## Findings that were real

1. Live rendered homepage (previous deploy) showed draft tutors and a 0 tutor count. Root cause: `js/sheet.js` created tutors from any active Sheet row, and `countUp` started at 0.
2. Public copy claimed reviews, a 24-hour reply, a `$6 to $6` price range, and that tutors are native speakers as a site fact.
3. `tutor/index.html` structured data listed two noindex drafts.
4. Eighteen level titles said `EkGuru | EkGuru`.
5. The country hub linked 142 research pages and was itself noindex, so published country guides had no honest index.

## Findings that were not adopted as rules

Article count, word count, the `.shop` TLD, and "Google cannot read JavaScript" were treated as hypotheses. They were not implemented as quotas. A blog was not created to satisfy a number.

## Result

Repository gates for the issues above pass. Production does not change until this branch is on `main` and Pages finishes. AdSense approval remains Google's decision.

# Runbook: add a page, a course level or a language

## The indexing freeze

Existing index, noindex and canonical settings are frozen by
`data/quality/indexing-baseline.json` and enforced by `tools/ultra/contract.py`
(also run first in CI). The `pages` map in the baseline has fixed counts and
must not be edited to make a new page pass.

**A new page is noindex by default.** To make a new page indexable, the owner
approves it and the approval is recorded:

1. Generate the page.
2. In `data/quality/indexing-baseline.json`, add it under
   `owner_approved_new_indexable`:

   ```json
   "hindi-tutor/qatar/index.html": {"indexable": true, "canonical": "https://ekguru.shop/hindi-tutor/qatar/"}
   ```

   and update `owner_approved_new_indexable_recorded_on`.
3. Write `docs/decisions/YYYY-MM-DD-<topic>.md` naming the approver and scope.
   `docs/decisions/2026-11-13-country-pages.md` is the model.
4. Add the page to the right sitemap through its generator, not by hand.
5. Update the count in `tools/test-reading-layer.mjs`.
6. Run [`regenerate-and-gate.md`](regenerate-and-gate.md).

## Add a course level (data)

- File: `data/courses/phase-N/<code>_<LEVEL>.json`. Look at an existing file in
  the same phase for the shape: `level.units[].lessons[]`, each lesson with
  `learn`, `vocab`, `grammar`, `dialogue`, `practice`, `quiz`, `worksheet`.
- A level needs to be listed in `data/courses/index.json` to publish.
  `tools/build-course-levels.py` refuses levels that fail its publication
  audit (placeholder text, repeated model answers, empty lessons).
- **Do not bulk-generate course text.** The language gate
  (`data/quality/language-gate.json`) needs 11 rungs for tier 1 and a **native
  reviewer's record** in `data/reviews/<code>.json`. Code cannot create that
  record. A language without it stays BLOCKED.
- Regenerate level pages: `docs/REGENERATING-LEVEL-PAGES.md` and the sequence
  in [`regenerate-and-gate.md`](regenerate-and-gate.md).

## Add a language

1. Source data under `tools/lang-data/` and course JSON under `data/courses/`.
2. Add it to the language registry via `tools/build-language-registry.py`.
3. Follow `docs/REGENERATING-LANGUAGE-COURSES.md`.
4. All new pages ship noindex until the owner approves (see above).

## Add a tutor

Tutors live in the Google Sheet. Follow [`../ADD-A-TUTOR.md`](../ADD-A-TUTOR.md).
Never commit a tutor's email, phone number or a private Drive link. Photos
that must be public go in `images/`.

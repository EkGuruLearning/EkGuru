# Consolidated requirements and verification status

**Date:** 3 November 2026
**Repository:** EkGuru
**Branch:** `arena/84e8fd94-ekguru`

This document consolidates the user's standing instructions, later scope decisions, and the status verified in this work session. It is a concise source of truth, not a 10,000-line padded file. It contains no private applicant, student, or tutor cell contents.

## 1. Booking email

### Required behavior

- Booking messages may go only to the booked tutor and the student.
- The owner/internal booking-email route must remain disabled and fail closed as `NOT_SENT_BY_POLICY`.
- Missing or invalid recipient addresses must not be redirected to the owner or another recipient.
- The private sheet remains the owner-side booking record.
- Do not claim that live provider delivery works until a real, controlled delivery is verified.

### Verified status

- Mailer, templates, relay whitelist, admin UI, and tests encode the owner-route prohibition.
- Automated routing, security, and mail-flow tests passed in this workspace.
- No message was sent during these changes. Provider delivery remains unverified; Apps Script deployment/live verification is not established.

## 2. Google Sheets tables and data safety

### Standing safety rules and latest scope decision

- The earlier instruction was to preserve all existing cell data and formulas. The user later explicitly selected a full-dataset replacement, including cell contents/formulas, and requested bilingual Hindi/English text.
- That replacement is **not authorized for execution until the replacement workbook/data and intended schema/formulas are supplied**. No replacement data may be invented, and no cell values or formulas have been rewritten.
- The owner asked to redesign every row and column and rewrite all text. Implement only against a supplied replacement dataset; preserve the private payments ledger and `applications-form-archive` unless the user specifically changes that scope.
- A live intake, booking, application, or review submission is not part of table formatting and must not be used as a test.

### Verified table coverage

- Structured tables are verified on 11 of the 12 requested tabs.
- Exact ranges, header names/order, and available column types are recorded in [`GOOGLE-SHEET-TABLES-2026-11-03.md`](GOOGLE-SHEET-TABLES-2026-11-03.md).
- Verified defined types include `tutors.active` and `tutors.approved` dropdowns and `reviews.date` as `DATE`; other columns retain their existing/unset types and formats. Do not force type conversions without an approved schema.
- Existing values, formulas, validations, frozen rows, and filters were not rewritten during the 11-table setup.

### Remaining blocker

- Intended table: `applications!A1:Q8` (`tbl_applications`).
- Current basic filter: `applications!A1:Q102`, overlapping the intended table range.
- The connector's previous clear-filter attempt failed (`No grid with id: 0`); metadata confirmed the filter remained. Do not retry that same invalid operation. The owner must remove the filter in Google Sheets or a valid clear-filter operation must become available before table creation.
- No `tbl_applications` table exists. Do not claim all 12 tables are complete while this remains blocked.

## 3. Generated-site and indexing requirements

- Do not hand-edit generated HTML. Change the source/generator and regenerate outputs.
- Preserve existing canonical URLs, indexability, `noindex`, and robots behavior while restoring generated page layers.
- Do not claim live HTTP checks, native-speaker review, source verification, publication approval, or release readiness unless separately verified.

### Verified status

- `python3 tools/build-all.py check` completed successfully. Its own result explicitly limits the claim to generated layers; it is not native-review, publication, AdSense, or release-readiness approval.
- `python3 tools/ultra/contract.py` passed with zero indexing/canonical violations.
- Phase 2 inventories cover 2,723 repository-backed public pages and 1,006 indexable memberships; live HTTP status remains pending.
- Phase 3 audit remains repository-signal-only; human, source, native-language, and external review remains pending.
- Print-sheet checks passed: 65 structural, 17 DOM, and 27 visible-print checks. The print generator was updated to emit `lang` labels for text in the target script; generated pages were regenerated.
- Existing language-quality and course-health reports continue to show their known blocked/attention states; passing the master generated-layer check does not clear those independent review gaps.

## 4. Requested complete rewrite and prerequisites

The requested full row/column redesign and bilingual rewrite is pending. To execute it safely, the user must provide the complete replacement workbook or equivalent per-tab replacement rows, column names/types, bilingual wording, and intended formulas. Until then:

1. Do not replace live sheet values or formulas.
2. Do not invent applicant, tutor, booking, review, or other factual records.
3. Do not claim the full spreadsheet redesign is complete.
4. Resolve the `applications` basic-filter blocker before adding its table.

## 5. Verification and limitations

- Repository master generated-layer check: passed on 3 November 2026.
- Indexing/canonical contract: passed, zero violations.
- Spreadsheet table coverage: 11/12 requested tabs; `applications` blocked as above.
- Booking policy tests: passed; actual provider delivery: unverified.
- No private sheet cell values are reproduced in this document.

## 6. Booking -> sheet path fix (3 November 2026, later session)

**Report:** "jo koi bhi booking karta hai vo sheet mein bhi nahi aa rahi" — bookings were not reaching the sheet.

### Root causes found in the full path (`js/features.js` -> `js/intake.js` -> `apps-script/Intake.gs` -> EkGuru DB `bookings` tab)

1. **Primary:** `js/site-config.js` `intake.url` is blank, and the owner confirmed the Intake web app was never deployed. Blank = `EkGuruIntake.ready()` false = the booking button is disabled and no submission is ever sent, so no sheet row can exist.
2. **Standalone-project trap (fixed in Intake.gs v1.1.0):** `SpreadsheetApp.getActive()` returns null for a project created at script.google.com instead of bound to the workbook, so every POST failed with a generic "could not save". Now the script also honours the `EKGURU_DB_SPREADSHEET_ID` script property and health reports `spreadsheetBound:false` instead of failing silently.
3. **False success (fixed in `js/intake.js`):** any `{"ok":true}` reply — e.g. from the health action of a wrong/old deployment — was treated as "saved". Success now requires the reference that was written into the sheet row.
4. **Whole-booking refusals (fixed in `js/intake.js` + `js/features.js`):** the browser never validated `student_email` (it checked a non-existent `email` field), and unclipped fields (`student_goal` > 200 chars, `source_page` = full `location.href` > 300 chars with tracking parameters) made the server refuse the entire submission. All booking fields are now validated/clipped to the exact server limits; `source_page` is origin+path only.
5. **Duplicates / lost first row (fixed in Intake.gs):** a retry with the same `booking_ref` now returns `duplicate:true` without a second row (writes are lock-serialised), and an existing-but-empty tab gets its header row before the first booking.

### Verified status

- `node tools/test-intake.js` passes, including new checks for: empty-tab header, duplicate `booking_ref`, unbound-project refusal, script-property binding, reference-less false success, and bad `student_email` caught client-side.
- **Deployment done by owner (3 Nov 2026, 20:35 IST):** deployment id `AKfycbwWJiuu…TV3LtN`; its `/exec` URL is now wired as `intake.url` in `js/site-config.js`. Health was verified live from this workspace on 3 Nov 2026: `{"ok":true,"version":"1.0.0","pendingRows":{"applications":11,"reviews_pending":0,"signups":0,"bookings":4}}` — the project is bound to the correct workbook (the `bookings` count matches `tbl_bookings` A1:T5) and the endpoint answers.
- **Two steps remain before "bookings reach the sheet" is fully claimed:** (1) the deployed editor code is still Intake.gs **v1.0.0** (the pasted screenshot shows the old `SpreadsheetApp.getActive()` health function) — paste v1.1.0 into the same project and re-deploy the **same** deployment as a New version (URL unchanged), after which health must show `"version":"1.1.0"` and `"spreadsheetBound":true`; (2) merge the PR so GitHub Pages serves the wired `intake.url`, then make one real test booking and see exactly one new `bookings` row with status `requested`. No live booking was sent as a test from this workspace, per section 2.

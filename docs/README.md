# EkGuru documentation index

Start with the repository [`README.md`](../README.md). Dated or historical
documents are marked; trust a document's date, and prefer the runbooks over
older audits.

## Architecture and structure

| Document | What it is |
|---|---|
| [`architecture/REPO-STRUCTURE.md`](architecture/REPO-STRUCTURE.md) | Folder-by-folder map, where new work goes, migration status |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | System design, data flow, target layout, migration plan |
| [`architecture/known-cycles.md`](architecture/known-cycles.md) | Generator ordering traps |
| [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) | Design tokens and components |
| [`GLOBAL_QUALITY_STANDARD.md`](GLOBAL_QUALITY_STANDARD.md) | Quality bar for published pages |
| [`offline-and-learning-data.md`](offline-and-learning-data.md) | Offline and on-device learning data |

## Runbooks (how to do a job)

| Runbook | Job |
|---|---|
| [`runbooks/regenerate-and-gate.md`](runbooks/regenerate-and-gate.md) | Regenerate pages and pass the master gate |
| [`runbooks/add-page-or-language.md`](runbooks/add-page-or-language.md) | New page, level, language; indexing freeze |
| [`runbooks/pr-and-merge.md`](runbooks/pr-and-merge.md) | Branch, PR, CI, merge |
| [`runbooks/owner-manual-steps.md`](runbooks/owner-manual-steps.md) | Steps only the owner can do |
| [`ADD-A-TUTOR.md`](ADD-A-TUTOR.md) | Add a tutor through the sheet |
| [`REGENERATING-LANGUAGE-COURSES.md`](REGENERATING-LANGUAGE-COURSES.md) | Regenerate language course pages |
| [`REGENERATING-LEVEL-PAGES.md`](REGENERATING-LEVEL-PAGES.md) | Regenerate level pages |
| [`review-checklist.md`](review-checklist.md) | Review checklist |

## Work in progress

| Document | What it is |
|---|---|
| [`ROADMAP-FIXES.md`](ROADMAP-FIXES.md) | Prioritised fixes with owners |
| [`resource-editorial-plan.md`](resource-editorial-plan.md) | Editorial plan for resources |

## Decisions

[`decisions/`](decisions/): owner decisions, one file per decision, named
`YYYY-MM-DD-<topic>.md`.

## Integrations and payments

[`GOOGLE-SHEET-TABLES-2026-11-03.md`](GOOGLE-SHEET-TABLES-2026-11-03.md),
[`GOOGLE_SHEETS_PAYMENT_SETUP.md`](GOOGLE_SHEETS_PAYMENT_SETUP.md),
[`QUESTIONS-API-SETUP.md`](QUESTIONS-API-SETUP.md),
[`RAZORPAY_PAYMENT_SETUP.md`](RAZORPAY_PAYMENT_SETUP.md),
[`RAZORPAY_INTERNATIONAL_API.md`](RAZORPAY_INTERNATIONAL_API.md),
[`COPY-PROTECTION.md`](COPY-PROTECTION.md). Apps Script setup notes are in
[`../apps-script/`](../apps-script/).

## Monetisation and compliance

[`GOOGLE_MONETIZATION.md`](GOOGLE_MONETIZATION.md),
[`GOOGLE_AD_MANAGER_SCALE_PLAN.md`](GOOGLE_AD_MANAGER_SCALE_PLAN.md),
[`ADSENSE-RESUBMISSION.md`](ADSENSE-RESUBMISSION.md),
[`ADSENSE-FINAL-REVIEW-PACKET.md`](ADSENSE-FINAL-REVIEW-PACKET.md),
[`PHASE-31-GLOBAL-LANGUAGE-ADSENSE-MONETIZATION-AUDIT.md`](PHASE-31-GLOBAL-LANGUAGE-ADSENSE-MONETIZATION-AUDIT.md).

## Historical (point-in-time records, not current instructions)

| Document | Note |
|---|---|
| [`HANDOVER-FOR-AI.md`](HANDOVER-FOR-AI.md) | Snapshot of 2 Nov 2026. State and branch names are out of date |
| [`AUDIT-2026-11-03.md`](AUDIT-2026-11-03.md), [`AUDIT-AND-ISSUES-2026-11-03.md`](AUDIT-AND-ISSUES-2026-11-03.md), [`REQUIREMENTS-2026-11-03.md`](REQUIREMENTS-2026-11-03.md) | 3 Nov 2026 audit and requirements |
| [`ULTRA-session-status.md`](ULTRA-session-status.md) | Session status of the ultra layer |
| `PHASE1-…` to `PHASE7-…` files | Phase write-ups: content depth, inventory, originality, rebuild, original value, Hindi text counter, answer-first |
| [`commands/`](commands/) | Past owner command prompts, kept for reference |

Planned: move dated audits to `docs/audits/` and old command prompts to
`docs/commands/archive/` (roadmap item 24).

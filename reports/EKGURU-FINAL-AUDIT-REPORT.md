# EkGuru final audit report

Recorded: 2026-09-27T16:12:54Z
Branch: `arena/01a0e390-ekguru`
Start SHA: `f22ed8bf5e2d4d038648405453c227697b2d11d1`

## Evidence, not a promise

Google AdSense approval is Google's decision. Nothing in this report is an approval, a prediction, or a guarantee.

## Inventory

| Measure | Value |
| --- | --- |
| Pages | 2638 |
| Indexable | 1008 |
| Noindex | 1630 |
| Thin indexable | 0 |
| Broken links | 0 |
| Indexable missing from sitemap | 0 |
| Noindex in sitemap | 0 |
| Orphan indexable | 0 |
| Duplicate title groups | 0 |
| Canonical mismatches | 0 |

## What changed

The live homepage, on the previous deploy, rendered draft tutors and flashed a tutor count of 0. Static HTML already listed two reviewed profiles. The Sheet create-path and the count-up animation caused the rendered mismatch. Both are fixed in this branch. Production will keep the old behaviour until `main` is redeployed.

Other repairs: review claims removed from the how-it-works step, broken `$6 to $6` price copy, double brand titles, unverified marketplace fee table, 24-hour reply promise, and the blanket native-speaker claim. Navigation now exposes Learn, Tutors, About and Contact without JavaScript.

## What was not invented

No tutors, reviews, ratings, lesson counts, traffic, offices, registrations, affiliate IDs, or AdSense approval were created. `support@ekguru.shop` is listed because the task requires a public domain address and `mail.ekguru.shop` resolves to a Brevo host. Delivery of that mailbox was not tested. The working form still uses `EkGuruLearning@gmail.com`.

## Tests run here

- `tools/test-sheet-apply.js` PASS, including refusal of sheet-only tutors
- `tools/test-sheetsync-policy.js` PASS
- `tools/test-no-competitor-attribution.js` PASS
- `tools/test-ad-policy.mjs` PASS (0 loader pages)
- `tools/test-consent-release.mjs` 12/12 PASS
- `tools/test-shell-drawer.mjs` PASS
- `tools/test-browser-qa.mjs` 26 PASS
- `tools/test-runtime-qa.mjs` 142 PASS
- `tools/build-shell.js --check` PASS
- Playwright: not run
- Googlebot user-agent fetch: not run (sandbox TLS failure)

## Status

See `reports/EKGURU-MASTER-EVIDENCE.json`. Do not read a repository pass as a production pass until the Pages build for the merge commit is checked.

# apps-script/

Google Apps Script sources. **Merging a change here does not deploy it.** The
owner pastes the file into the sheet's Apps Script project and creates a new
deployment version (`docs/runbooks/owner-manual-steps.md` §1).

| File | Job | Setup notes |
|---|---|---|
| `Unified.gs` | Intake and live feed in one project (recommended) | `UNIFIED-SETUP.md` |
| `Intake.gs` | Applications, bookings, reviews and sign-ups into the sheet; duplicate guard | `INTAKE-SETUP.md` |
| `LiveFeed.gs` | Read-only feed of tutors, reviews and settings | `LIVE-FEED-SETUP.md` |
| `Code.gs` | Razorpay payment and support backend for the separate payments-ledger sheet | `docs/GOOGLE_SHEETS_PAYMENT_SETUP.md` |

The site stays in "feed off" mode until a deployed `/exec` URL is set at
`feed.url` in `js/site-config.js`.

Tests: `node tools/test-intake.js`, `node tools/test-live-feed.js`,
`node tools/test-apps-script.mjs`.

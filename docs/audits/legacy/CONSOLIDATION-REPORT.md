# EkGuru — Apps Script Backend Consolidated into ONE File

**Deliverable:** `apps-script/combined/Code.gs` — **3290 lines / 161,276 bytes (~157 KB)**
**Branch:** `arena/2046092b-ekguru` @ `7ad9f99`
**Date:** 2026-11-23
**Status:** built, verified, `npm test` green (13/13 suites). Nothing deleted. Nothing deployed.

---

## 1. Files inspected

All 8 `.gs` files in the repo were read in full before anything was built.

| File | Lines | Functions | Role | Verdict |
|---|---|---|---|---|
| `apps-script/ApplicationSchema.gs` | 329 | 7 | 69-column schema, statuses, email triggers | **merged → PART 1** |
| `apps-script/ApplicationIntake.gs` | 1470 | 51 | validation, rows, dedupe, emails, admin API | **merged → PART 2** |
| `apps-script/Unified.gs` | 1357 | 46 | canonical router: `doGet`/`doPost`, feed + intake | **merged → PART 3** |
| `apps-script/Code.gs` | 1898 | 27 | **Razorpay payments backend** | **not merged** (§4) |
| `apps-script/Intake.gs` | 604 | 15 | legacy standalone intake | **not merged** (§4) |
| `apps-script/LiveFeed.gs` | 283 | 13 | legacy standalone feed | **not merged** (§4) |
| `tools/apps-script-mailer.gs` | 385 | — | separate mailer project | out of scope |
| `tools/apps-script-questions.gs` | 170 | — | separate quiz project | out of scope |

**Dependency trace:** the three merged files form one closed unit — Schema defines the constants Intake validates against, Intake exposes `ekApplicationAction_()` / `ekApplicationGet_()`, and Unified's router calls exactly those two seams. No file outside the trio is referenced. The three have **0 shared function names**, **0 shared global `var`s**, and exactly one `doGet`/`doPost` between them (both in Unified) — which is why they can legally share one global scope.

---

## 2. Final structure of `Code.gs`

```
lines   1–100    Header — what this is, which project it goes in, setup,
                 Script Properties, entry points, size, "use strict" note
line    100      "use strict";        <- the only one in the file
lines  104–438   PART 1 of 3 — SCHEMA            (ApplicationSchema.gs, verbatim)
lines  444–1918  PART 2 of 3 — APPLICATION BACKEND (ApplicationIntake.gs, verbatim)
lines 1925–3284  PART 3 of 3 — UNIFIED ROUTER    (Unified.gs, verbatim)
```

Key positions: `onOpen` 695 · `doGet` 2126 · `doPost` 2167 · `onEdit` 3274. **104 functions, one `doGet`, one `doPost`, one `onOpen`, one `onEdit`.**

The header states explicitly that this is the **form project** (tutors / reviews / settings / bookings / contacts / signups / applications) and **not** the Razorpay payments project, with the exact `?tab=` / `?kind=` surface it serves and the 5-step bound-project deploy procedure.

> A note in the header explains the numbering: the three parts are **PART 1/2/3**; inside PART 3, `Unified.gs` numbers its *own* internal sections "SECTION 1 EK_ CONFIG / SECTION 2 THE ROUTER / SECTION 3 FUTURE MODULES". Those were left exactly as their author wrote them, so the two numbering schemes never collide.

---

## 3. What was removed or altered — and why

**Verbatim integrity: 3,156 source lines checked, 0 not found in the output.**

| Change | Count | Reason |
|---|---|---|
| Header added | 1 block | Without it, a pasted file gives no hint which project it belongs to |
| PART banners added | 3 | Locate each source file inside a 3,290-line file |
| Duplicate `"use strict";` commented out | **2** | A repeated directive is a parse error in one global scope. The first is kept as the file's first statement, so **all three parts still run in strict mode** — a stricter outcome, not a looser one |
| Logic, functions, constants, comments | **0 changed** | — |

No function was renamed, no constant re-valued, no route added or dropped, no validation relaxed, no comment reworded, no blank line removed.

---

## 4. Files NOT merged — and why

These are deliberate exclusions, not oversights. Merging any of them would break a working deployment.

**`apps-script/Code.gs` — the Razorpay payments backend.** This is the blocker reported in `docs/audits/legacy/CONSOLIDATION-INSPECTION-BLOCKED.md`. It is a live, **frozen** backend with its own `doGet` (:816) and `doPost` (:992) serving `health / diagnostics / currencies / recent-support / create-order / verify-payment / webhook / report-failure / report-cancel`, and it hard-codes its own workbook `SPREADSHEET_ID_DEFAULT`. Pasting it into the same project would put **two `doGet` and two `doPost` in one global scope** (the second silently wins — whichever loads last), and would let payment code and form code resolve the same spreadsheet. Renaming or overwriting it is off the table: payments are frozen. **It was not read into the output, not modified, and not renamed.**

**`Intake.gs` + `LiveFeed.gs` — legacy standalone alternates.** These 23 shared global function names with `Unified.gs` (`doGet`, `doPost`, `feedGet_`, `intakePost_`, …). Apps Script has one global scope per project, so they are **deploy-time alternatives, not merge candidates** — pasting them together produces duplicate declarations. `Unified.gs` supersedes both. They stay in the repo as history; the docs already say not to deploy them in place of the unified backend (`UNIFIED-SETUP.md:37,44`, `APPLICATION-BACKEND.md:38,56`).

**`tools/apps-script-mailer.gs`, `tools/apps-script-questions.gs`** — separate projects by design, out of scope.

**No `.gs` file was deleted, moved, or renamed.** The old files remain the source of truth for `tools/build-combined-code.mjs` — deleting them would make the consolidated file unrebuildable. If you later want the legacy pair gone, that is a separate, explicitly approved cleanup.

---

## 5. Exact test results

`npm test` — **exit 0**, **13/13 suites, 0 failures**:

| Suite | Result |
|---|---|
| `test-razorpay-api` (payments, unchanged) | 30/30 gates |
| `test-join-wizard` | all pass |
| `test-application-backend` | 120 checks |
| `test-defect-regressions` (DEF-1…DEF-4) | 153 passed, 0 failed |
| `test-wizard-sheets-e2e` | 77 passed, 0 failed |
| **`test-combined-code` (new)** | **42 passed, 0 failed** |
| `test-browser-qa` | 26 passed |
| `test-runtime-qa` | 143 passed |
| `test-wizard-sheets-e2e` E2E gates | 11/11 |
| contract gates | 8/8 |
| live-feed | all pass |

### The new consolidation suite — `tests/integration/test-combined-code.mjs` (42 checks)

Permanent, registered in `npm test`, so this stays true on every future run. It loads the **combined file alone** in a mocked Apps Script environment and compares it against the three source files loaded separately in an identical environment.

*Completeness* — every source line present verbatim · exactly one `"use strict"` · one `doGet` · one `doPost` · three PART banners · numbering note · payments warning.

*Collisions* — no duplicate function declarations · no duplicate top-level `var`s · function inventory identical to the three sources (104).

*Behaviour equivalence* — 8 GET routes **byte-identical** (`?action=health`, bare `/exec`, `?tab=health`, `?tab=tutors` CSV, `?tab=tutors&format=json`, `?tab=settings`, `?tab=unknown`, `?action=ping` bad token); submit produces the same ok/duplicate/mail outcome, the same row count, the same email count and the same `details_json` keys.

*Security invariants* — WhatsApp number, applicant email and the `whatsapp` header **absent** from the public tutors CSV; honeypot writes no row, sends no mail, still answers with a believable `EG-` success; retry dedupes to one row with no second email and the same reference; a planted `submission_id` cannot suppress a stranger; `ekFindSubmission_` fails closed (`""`) without a server-resolved scope.

*Schema & contracts* — version `2.1.0` · 69 logical fields · 69 header columns · the legacy 17 columns still first in order · all 24 public/entry-point functions present · owner `ekAdminUpdate` returns `ok:true`.

*Payment isolation* — `apps-script/Code.gs` still contains the Razorpay code · the consolidated file contains **no** Razorpay *code* (the word appears only in comments warning against mixing projects) · no payment tab constants · no payment spreadsheet id.

### Build tool — `tools/build-combined-code.mjs`

Reproducible generation (`node tools/build-combined-code.mjs`) instead of a one-off heredoc, so the file can be regenerated after any source edit. It asserts one `doGet` and one `doPost` on every build.

---

## 6. Risks and deployment notes

1. **Three earlier temporary facts are now permanent artefacts.** `tools/build-combined-code.mjs` and `tests/integration/test-combined-code.mjs` are new files; `package.json` gained one suite. Nothing else in the repo changed.

2. **Deploy target matters.** Paste this into the **form project** (bound to the EkGuru DB workbook — the one currently running `Unified.gs`), replacing its `Code.gs`. **Not** the payments project. If the project is bound to the sheet, do not set `EKGURU_DB_SPREADSHEET_ID` as well.

3. **Deploy by editing the existing deployment** — *Manage deployments → Edit → New version → Deploy*. A "New deployment" mints a new `/exec` URL and both `feed.url` and `intake.url` in `js/site-config.js` go stale.

4. **Equivalent but not identical runtime.** Everything is byte-identical in the mocked harness, but that harness is a local mock. It cannot verify: real Sheets quota/locking under concurrency, real Gmail send/reply-to behaviour, real `Utilities.formatDate` timezone rendering, or the Apps Script editor's own parse. **Run `selfTest_` once after pasting and check the Apps Script editor shows no red error — that is the real parse test.**

5. **`"use strict"` is now global.** All three parts run in strict mode. Each source already opted in individually, so behaviour should be unchanged — and the harness confirms it — but strict mode is where an accidental undeclared assignment (which used to create a silent global) now throws. If `selfTest_` throws a `ReferenceError` on a variable that worked before, that is the cause, and it is a latent bug being surfaced, not introduced.

6. **Do not paste the payments `Code.gs` in here**, and do not paste this file there. Two `doGet`s in one scope = one of the two backends silently stops answering.

7. **Not verified, needs a human:** the deployed URL answering over HTTPS from a browser, the Google Sheet menu (`onOpen`) appearing, and the installable `onEdit` trigger still being attached after re-pasting (re-run `installTriggers()` if it is not).

---

## 7. Command reference

```bash
node tools/build-combined-code.mjs     # regenerate apps-script/combined/Code.gs
node tests/integration/test-combined-code.mjs      # 42 consolidation checks
npm test                               # all 13 suites
```

**Nothing was committed, staged, or pushed.** Working tree: 6 modified (from earlier work) + new files, per `git status` above. The live preview on `:3001` was not touched.

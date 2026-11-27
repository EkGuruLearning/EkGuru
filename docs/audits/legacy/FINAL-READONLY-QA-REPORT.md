# EkGuru — Final READ-ONLY QA

**Branch:** `arena/2046092b-ekguru` · **HEAD verified:** `7ad9f992f0351e10bd11b249eb58488a5437cf2a` (`7ad9f99`) ✅
**Mode:** strictly read-only. No source edit, no install, no lockfile change, no production access, no email, no Sheet write, no deploy, no commit/push/stage/reset.

---

## Verdict

> # `READY FOR HUMAN BROWSER QA`
>
> Code, security and schema checks all pass. The **only** outstanding item is real-browser
> visual QA, which is **NOT VERIFIED** in this environment — no browser exists here. That is
> exactly what the verdict names: ready for a human to do that last pass.

---

## ⚠️ Discrepancies with the brief (reporting before acting, as instructed)

| # | Brief said | Actual | Action |
|---|---|---|---|
| 1 | "Saare **16** untracked files" | **17** | Reported, not changed. The 17th is `docs/audits/legacy/VISUAL-QA-REPORT.md` (created by the previous QA turn). Making it 16 would require deleting a file — forbidden. |
| 2 | — | `Unified.gs` has a stray comment paragraph about the seam placed *above* the honeypot block, out of order | **Cosmetic only**, no behavioural effect. Left untouched (read-only). Noted as R1. |

Both were surfaced rather than silently reconciled.

---

## 1. Repository integrity — **PASS**

| Check | Result | Evidence |
|---|---|---|
| HEAD | **PASS** | `7ad9f992f0351e10bd11b249eb58488a5437cf2a` = expected `7ad9f99` |
| Branch | **PASS** | `arena/2046092b-ekguru` |
| `git status --short` | **PASS** | 7 modified, 17 untracked, **0 staged** |
| `git diff --stat` | **PASS** | 7 files, +719 / −39 |
| `git diff` (full, read) | **PASS** | all 7 files read; `join.html` deletions are only the old flat form |
| All untracked files inspected | **PASS** | see below |
| No unexpected file | **PASS** | every path is form/backend/test/report related |
| No secret / credential | **PASS** | 0 matches for API keys, tokens, `rzp_live`, `sk_live`, `AKIA`, `ghp_`, private keys |
| No spreadsheet ID leak | **PASS** | 0 `1XXXX…`-length IDs in changed/untracked files |
| No deployment URL leak | **PASS** | 0 `/macros/s/…` identifiers in changed/untracked files |
| No production config change | **PASS** | `js/site-config.js` **not modified**; no `.env`, `wrangler`, `netlify`, `vercel`, `CNAME`, `_headers`, robots/sitemap change |

**Scope of the 7 modified:** `apps-script/Intake.gs`, `apps-script/Unified.gs`, `join.html`, `js/intake.js`, `package.json`, `tests/integration/test-intake.js`, `tests/integration/test-live-feed.js` — all application-form.

**The 17 untracked:** 6 reports · `APPLICATION-BACKEND.md` · `ApplicationIntake.gs` · `ApplicationSchema.gs` · `css/join-wizard.css` · `js/join-schema.js` · `js/join-wizard.js` · `build-join-schema.mjs` · 4 test suites.

Only prose mentions of the words "secret"/"token" exist (e.g. "It holds NO secrets", "Authorisation is a shared bearer token"). No live value anywhere.

## 2. Automated regression — **PASS**

`npm test` → **exit code 0**, **0 real FAIL lines** (538 PASS lines).

| Suite | Exit | PASS | FAIL |
|---|---|---|---|
| `test-razorpay-api.mjs` | 0 | 30 gates | 0 |
| `test-join-wizard.mjs` | 0 | 117 | 0 |
| `test-application-backend.mjs` | 0 | 120 | 0 |
| `test-defect-regressions.mjs` | 0 | 153 | 0 |
| `test-wizard-sheets-e2e.mjs` | 0 | 77 | 0 |
| `test-browser-qa.mjs` | 0 | 27 | 0 |
| `test-runtime-qa.mjs` | 0 | 143 | 0 |
| `test-apps-script.mjs` | 0 | 31 | 0 |
| `test-payment-e2e.mjs` | 0 | 11 | 0 |
| `test-live-payment-contract.mjs` | 0 | 8 | 0 |
| `test-home-tutor-reveal.mjs` | 0 | 1 | 0 |
| `test-live-feed.js` | 0 | 69 | 0 |

`test-intake.js` (not in the `npm test` chain) also run separately: **26/26, exit 0**.

⚠️ **One false alarm, resolved:** `grep FAIL` initially flagged `test-apps-script.mjs` and
`test-payment-e2e.mjs`. Those are test *names* — `"…sets Payment Result=FAILED…"`, `"Payment
Failure updates Payments tab to FAILED…"`. Re-checked against real failure markers (`✗`,
`FAIL [`): **0** in both. No failure occurred; nothing was fixed.

## 3. Security-critical verification — **PASS**

| Check | Result | Evidence |
|---|---|---|
| Honeypot before seam in `Intake.gs` | **PASS** | honeypot @ byte 10792 < seam @ 11269 |
| Honeypot before seam in `Unified.gs` | **PASS** | honeypot @ byte 36673 < seam @ 36873 |
| `submission_id` not authoritative identity | **PASS** | reserved via `reservedNames.submission_id = 1` (line 400); stored inertly as `sent_submission_id` |
| Row lookup email-scoped | **PASS** | scope = `ekFindRecentByEmail_(email)` → `{row: own.index}`; lookup skips `i + 2 !== scope.row` |
| Fail-closed without scope | **PASS** | `if (!scope \|\| !scope.row) return "";` — never a tab-wide match |
| Cross-applicant ID cannot suppress | **PASS** | reproduced attack: planted id → third applicant `duplicate:false`, **3 rows, 3 emails** |
| Same-email concurrent retry | **PASS** | two identical posts → **1 row, 1 email**, same reference |
| LockService critical section | **PASS** | acquired on submit path; `tryLock(25000)` |
| Lock release | **PASS** | `finally { lock.releaseLock(); }`; verified released, none held |
| Lock fail-closed | **PASS** | simulated busy lock → submit **refused** (`busy`), 0 rows, 0 emails |
| Payment files unchanged | **PASS** | `server/api.js`, `server/razorpay-service.js` **untouched** (`git diff server/` empty) |

An independent 18-check harness (mocked services only) passed **18/18**.

**On "concurrent":** true parallelism cannot be executed in this sandbox — the evidence is
the serial double-tap plus static proof that the whole write is inside one
`tryLock`/`finally` critical section. A genuinely simultaneous race is **NOT VERIFIED**
(see R3).

## 4. Schema & data integrity — **PASS**

| Check | Result | Evidence |
|---|---|---|
| Schema version | **PASS** | `2.1.0` |
| Column count | **PASS** | **69** logical, **69** physical, **69** unique, 0 duplicates |
| Legacy first 17 unchanged | **PASS** | `timestamp,reference,status,approved,name,email,city,country,subject,experience,rate_usd,availability,bio,photo_link,video_link,languages,notes` — order identical |
| `ApplicationSchema.gs` ⇄ `ApplicationIntake.gs` contract | **PASS** | backend builds from `EKGURU_APPLICATION_FIELDS`/`HEADER` (single source); header still exactly 69 |
| `ApplicationSchema.gs` ⇄ `js/join-schema.js` | **PASS** | version, field count, header, serverOnly list and every per-field `src/col/max/type` **identical** |
| WhatsApp not exposed publicly | **PASS** | in `FEED_PRIVATE_EXACT`; `applications` is **not** a feed tab (`tutors, reviews, settings, support`). Empirical: mocked tutors tab carrying `whatsapp` + `email` → public CSV = `name,approved,city,bio` only; phone and email **absent** |

## 5. Browser QA status — **NOT VERIFIED**

| Item | Status |
|---|---|
| Real browser available | **NOT VERIFIED — none exists** (no Playwright, Puppeteer, Chrome, Chromium, Firefox, Edge; no `~/.cache/ms-playwright`; `$DISPLAY` unset) |
| 1366 × 768 desktop | **NOT VERIFIED** |
| 768 × 1024 tablet | **NOT VERIFIED** |
| 360 × 800 mobile | **NOT VERIFIED** |
| Horizontal overflow | **NOT VERIFIED** |
| 7-step navigation, Prev/Next | **NOT VERIFIED** |
| Required/optional validation | **NOT VERIFIED** |
| Empty defaults (duration/currency/hindi_level) | **NOT VERIFIED** visually |
| Review screen rendering | **NOT VERIFIED** visually |
| Keyboard nav, focus rings | **NOT VERIFIED** |
| Screenshots | **NONE** — none can exist without a renderer |

**No jsdom or static result is reported as a visual PASS anywhere in this document.** jsdom
has no layout engine: it cannot compute overflow, contrast, or paint. `tests/regression/test-browser-qa.mjs`
is itself jsdom and is not visual evidence.

## 6. Final table

| Check | Status | Evidence | Remaining risk |
|---|---|---|---|
| HEAD = `7ad9f99` | **PASS** | `git rev-parse HEAD` | none |
| Working tree scope | **PASS** | 7 modified / 17 untracked / 0 staged | brief said 16 — the extra is `docs/audits/legacy/VISUAL-QA-REPORT.md` |
| No secrets / IDs / prod config | **PASS** | 0 pattern matches; `site-config.js` untouched | none |
| `npm test` | **PASS** | exit 0, 0 real FAIL | 2 suites print `FAILED` as test *names* |
| Honeypot ordering (both routers) | **PASS** | byte offsets | none |
| `submission_id` not authoritative | **PASS** | reserved + row-scoped + fail-closed | pre-2.0.2 rows carry no retry key |
| Cross-applicant suppression | **PASS** | 3 rows / 3 emails on attack | none |
| Lock section + release + fail-closed | **PASS** | `tryLock`/`finally`, busy → refuse | true parallel race not executable here |
| Payment code unchanged | **PASS** | `server/` diff empty | none |
| Schema 2.1.0 / 69 columns | **PASS** | runtime introspection | none |
| Legacy 17 preserved | **PASS** | exact order match | none |
| Schema contracts agree | **PASS** | per-field identical | none |
| WhatsApp not public | **PASS** | denylist + empirical CSV | none |
| Real-browser visual QA | **NOT VERIFIED** | no browser installed | **all visual/layout items unproven** |
| 3 viewports | **NOT VERIFIED** | no browser | 360/768/1366 unproven |
| Screenshots | **NOT VERIFIED** | cannot be produced | none captured |

---

## Remaining risks

| # | Risk | Severity |
|---|---|---|
| **R1** | `Unified.gs` has an out-of-order comment paragraph (seam comment sits above the honeypot block). Cosmetic. | Cosmetic |
| **R2** | **All visual QA unproven** — layout at 360/768/1366, focus rings, contrast, overflow, `<select>` on iOS/Firefox. Needs a human pass. | **Medium — the one real blocker** |
| **R3** | A truly simultaneous double-submit is not executed; the guarantee rests on the `tryLock` critical section (fail-closed if the lock is unavailable). | Low |
| **R4** | Rows written before 2.0.2 have no retry key; a retry of one is caught by the 72-hour email window. | Low |
| **R5** | Clearing `currency`/`duration` snaps to the schema default (`USD`/`50 min`) rather than blanking. Pre-existing. | Low |
| **R6** | `availability_meta` has two valid shapes; consumers must tolerate both. | Low |
| **R7** | `sent_*` keys share the details key budget, so a flood of reserved names can crowd out genuine overflow answers. | Low |

---

## Confirmation

- **No source file modified.** `git status` at end = start: **7 modified, 17 untracked, 0 staged**, `HEAD` **`7ad9f99`**.
- **No package installed, no lockfile change**; `package.json` only carries its pre-existing 1-line diff from earlier work.
- **No commit, push, staging, or reset.**
- **No production access:** no Sheet read/written, no deployment, no Script Property, **no real email** (all mail went to in-memory mocks).
- **No temp files left behind** — probe scripts were written and removed; `git status` shows none.
- Test artifacts written by suites (if any) were **not** modified or deleted.

**READY FOR HUMAN BROWSER QA** — code, security and schema are green; only the human visual pass remains.

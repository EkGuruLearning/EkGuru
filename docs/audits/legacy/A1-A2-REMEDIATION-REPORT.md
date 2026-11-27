# A1 / A2 Remediation Report — focused fix

**Branch:** `arena/2046092b-ekguru` @ `7ad9f99` (branched from `main`)
**Scope:** only the two findings raised in `docs/audits/legacy/PREFLIGHT-AUDIT.md`. Nothing else.
**Status:** fixes complete and green. **Nothing deployed, nothing committed, nothing pushed.**

---

## 1. What was actually wrong

Both findings come from the same root cause: **identity was being taken from the client.**

| Finding | Root cause | Consequence |
|---|---|---|
| **A1** | `Intake.gs` ran the application seam *before* the honeypot. `Unified.gs` had already been reordered; `Intake.gs` had not, so the two routers disagreed. | On a standalone deployment a bot that filled the hidden field still got a stored row and an email to the owner. |
| **A2** | `ekFindSubmission_` matched the client's `submission_id` against `details_json.submission_id` in **every row of the tab**, and the insert path never wrote the server's own key. | One applicant could plant a value and make an unrelated applicant's later submission look like a retry — it was answered `duplicate: true`, never stored, and never acknowledged. Also: a first submission stored no retry key at all. |

A2 was **broader than the audit's first write-up**. My previous pass reserved the name and wrote the key on insert, which stopped the *named-key* variant, but the retry lookup was still tab-wide — so a planted `sent_`-free value could still name another row. Your instruction — *never trust a client-supplied `submission_id` as the authoritative dedupe identity* — is what exposed it.

---

## 2. What changed

### `apps-script/Intake.gs` — v1.3.0 → v1.3.1
`doPost` now checks the honeypot **before** the application seam, matching `Unified.gs`, with the same explanatory comment. No routing logic duplicated, no second backend, still one `doGet` / one `doPost`.

Verified order in **both** routers now:
`parse → honeypot → application seam (→ quota → lock → write → email) → owner action → kind dispatch → quota → write → email`

### `apps-script/ApplicationIntake.gs` — v2.0.0 → v2.0.2

**`ekFindSubmission_(tab, map, submissionId, scope)`** — now takes a **server-resolved scope** and fails closed:
- `!scope || !scope.row` → returns `""` (never a tab-wide match);
- otherwise only the caller's own row is examined.

**`ekSubmitApplication_`** — resolves identity *before* any lookup:

```js
var email = String(values.email || "").toLowerCase();   // the applicant's own answer
var own   = ekFindRecentByEmail_(tab, map, email);
var scope = { row: own ? own.index : 0 };
```

`submission_id` is now explicitly an **attempt token**, not an identity: it may say *"this is the same attempt as before"*, it may never say *"this is the same person as someone else."*

**Also in place from the same fix:** `submission_id` is reserved (a value inside `fields` is diverted and kept inertly as `sent_submission_id`), and the insert path writes the server's own key after `ekBuildRow_`.

*No schema change. Schema stays **2.1.0 / 69 columns**; `ApplicationSchema.gs` and `js/join-schema.js` are byte-unchanged.*

### `tests/regression/test-defect-regressions.mjs` — 59 → **153 checks**
A1 and A2 blocks rewritten to run **both routers** through their real `doPost`.

### `apps-script/APPLICATION-BACKEND.md`
Corrected the idempotency section (it claimed a retried `submission_id` was always deduped — false on the insert path, and it overstated how far the key reaches), documented the server-side identity rule, refreshed stale counts (68→69 columns, 87→120 backend checks, 61→117 wizard checks), and recorded the A1 fix.

### `tests/integration/test-live-feed.js` — **version assertions only**
Four assertions moved to `1.3.1` / `2.2.0`. No payment, booking, feed, review or tutor-publishing logic was touched; this file only *reads* those versions. `tests/integration/test-intake.js` was not modified this pass.

---

## 3. Failing-before / fixed-after evidence

Each mutant reconstructs a real prior state; the suite must fail. Run on a copy under `/tmp`, never in the repo.

| Mutant | What it restores | Result |
|---|---|---|
| **MUT-1** | `Intake.gs` honeypot below the seam | **exit 1, 11 FAIL** — *a filled honeypot writes no row* → `rows=1` |
| **MUT-2** | `Unified.gs` honeypot below the seam | **exit 1, 11 FAIL** |
| **MUT-3** | `submission_id` reservation removed | **exit 1, 6 FAIL** |
| **MUT-4** | insert-path server key removed | **exit 1, 5 FAIL** |
| **MUT-5** | **the audit's undetected mutation** — row scope removed (tab-wide match) | **exit 1, 1 FAIL** (clean assertion, no crash) |
| **MUT-6** | fail-closed guard removed | **exit 1, 1 FAIL** — *the retry lookup refuses to match without a server-resolved scope* |

**PRE** — all four halves reverted together (the genuine pre-fix file) — reproduces the complete attack:

- BEFORE: first submission stores **no** retry key; a planted value **does** become the dedupe key; a stranger sending it is told *"already received"*; **2 rows, 2 emails** (stranger lost).
- AFTER: own key stored; planted value diverted to `sent_submission_id`; stranger **not** suppressed; **3 rows, 3 emails**.

Isolation checks confirm which half is load-bearing: M1 alone cannot suppress a stranger (the reservation holds); M3 alone stores no key at all and still cannot suppress.

**Adversarial / behavioural coverage now in the suite (both routers):**
planted reference · guessed id · duplicate retry · legitimate resubmission · email deduplication · existing data preservation · whitespace honeypot (documented as *treated as a person* — `trim()`, deliberate and identical in both routers) · empty honeypot still works · **owner action with no honeypot field still works** (the reorder must not lock the owner out).

---

## 4. Test results

`npm test` — **exit 0**, zero `FAIL` lines.

| Suite | Result |
|---|---|
| gates | 30/30 |
| application backend | 120/120 |
| **defect regressions** | **153/153** (was 59) |
| wizard ⇄ Sheets e2e | 77/77 |
| wizard | 117 |
| intake | 26/26 |
| Runtime QA | 143/143 |
| Apps Script | 31 |
| E2E | 11/11 |
| contract | 8/8 |
| live feed | pass |

Both routers exercised with mocked services throughout; no network, no Google API, no real Sheet.

---

## 5. Remaining risks

| # | Risk | Severity |
|---|---|---|
| R1 | **A1 / A2 — closed**, each with a mutant that proves the test bites. | — |
| R2 | Rows written **before 2.0.2** have no retry key; a retry of one is caught by the 72-hour email window instead. Documented; no migration needed or wanted. | Low |
| R3 | **No real-browser visual QA.** No browser in this environment; all UI evidence is jsdom. 360 px layout, focus rings, contrast, iOS/Firefox `<select>` remain **NOT VERIFIED — pending a human pass**. | Medium |
| R4 | Clearing `currency` / `duration` snaps to the schema default (`USD` / `50 min`) rather than blanking — `default` always wins in `ekBuildRow_`. Pre-existing, arguably intended. | Low |
| R5 | A stale cached client can still send an explicit `50 min` / `USD` / `Native`, which the server accepts as a real answer. | Low |
| R6 | `availability_meta` has two valid shapes (`{days,timezone,format}` vs `{days,slots,timezone,format}`); consumers must tolerate both. | Low |
| R7 | `sent_*` keys share the `EKGURU_DETAILS_MAX_KEYS` budget, so a flood of reserved names can crowd out genuine overflow answers. | Low |
| R8 | Retry scoping keys on `email + 72 h`, so an applicant who changes their email *and* retries gets a new row. This is correct (a different person), but worth knowing. | Low |

---

## 6. Explicit confirmation

- **No deployment.** Nothing pasted, no Apps Script version created, no `js/site-config.js` change.
- **No commit, no push, no stage, no reset.** `git status`: **7 modified, 15 untracked, 0 staged**; `HEAD` still `7ad9f99`.
- **No production Sheets read or written**, no migration run, no **Script Properties** changed, **no email sent**.
- **Standalone `Intake.gs` was not deployed and is not proposed as a replacement** for the unified backend. It was reordered *only* so that the two entry points cannot disagree; `Unified.gs` remains the live shape.
- **No schema change** — 2.1.0 / 69 columns, both schema files untouched.
- **No payment, booking, tutor-publishing, feed, review or unrelated admin behaviour changed.**

**Stopping here. Deployment awaits separate explicit authorization.**

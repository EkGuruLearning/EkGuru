# EkGuru — independent pre-deployment audit (read-only)

**Branch:** `arena/2046092b-ekguru` @ `7ad9f99` — branched from `main`
**Scope:** DEF-1 … DEF-4 and the surrounding surface, audited *before* any deployment.
**Audit mode:** strictly read-only. No file edited, nothing installed, no migration, no
production Sheet read or written, no Script Property touched, no email sent, nothing
staged, committed, pushed or reset.

> ### Verdict in one line
> **The four fixes are correct (DEF-1…DEF-4 all PASS).** The audit also found two
> pre-existing defects — **A1** (honeypot bypass on a *standalone* `Intake.gs`
> deployment) and **A2** (a client-supplied `submission_id` could become the stored
> dedupe key). **Both are now FIXED** in a follow-up pass, each with a failing-before /
> fixed-after regression block. See the addendum at the end of this file; the A1/A2
> sections below are preserved as the audit found them.

---

## 0. What was and was not possible

| | |
|---|---|
| Browser / visual QA | **NOT VERIFIED — pending.** No real browser (no Playwright, Puppeteer or Chrome) exists in this environment. Every UI statement below is from **jsdom**, which has no layout engine. 360 px layout, focus rings, colour contrast, iOS/Firefox `<select>` rendering and touch behaviour are **untested**. |
| Production Sheet | **Not accessed.** All Sheets evidence comes from in-memory sheet fakes. |
| Emails | **Not sent.** The mail path was exercised against a mock mailbox only. |
| Live endpoint | **Not called.** `intake.url` was never contacted. |

Read-only was honoured literally: every probe ran from a temporary script that was
deleted afterwards, and two destructive-looking checks (generator drift, mutation testing)
were run on **copies under `/tmp`**, never in the repository. Final state is unchanged:
**7 modified, 14 untracked, 0 staged**, `HEAD` still `7ad9f99`.

---

## 1. `git status` and the complete diff — **PASS**

**7 modified, 14 untracked, nothing staged, nothing committed.**

| Modified | What changed |
|---|---|
| `apps-script/Intake.gs` | 1.2.0 → 1.3.0; two seam calls added |
| `apps-script/Unified.gs` | 2.1.1 → 2.2.0; two seams + `application` block in health |
| `join.html` | full wizard markup (620-line diff), one form, two deferred scripts |
| `js/intake.js` | mints/sends `submission_id`, clears it only on acceptance |
| `package.json` | `test` chains the new suites |
| `tests/integration/test-intake.js` | +13 assertions (one form, deferred wizard, `id="jw-form"`) |
| `tests/integration/test-live-feed.js` | +8 assertions (versions 1.3.0 / 2.2.0) |

| Untracked | Purpose |
|---|---|
| `apps-script/ApplicationSchema.gs`, `ApplicationIntake.gs` | the new backend (single source of truth + implementation) |
| `apps-script/APPLICATION-BACKEND.md` | operator runbook |
| `js/join-schema.js`, `js/join-wizard.js`, `css/join-wizard.css` | the wizard (schema copy is generated) |
| `tools/build-join-schema.mjs` | generator |
| `tools/test-{application-backend,join-wizard,defect-regressions,wizard-sheets-e2e}.mjs` | suites |
| `docs/audits/legacy/DEFECT-FIXES-REPORT.md`, `docs/audits/legacy/FINAL-VERIFICATION-REPORT.md`, `docs/audits/legacy/FINAL-IMPLEMENTATION-REPORT.md` | prior reports |

The diff of every modified file was read in full (for `join.html`, the deletion +
`form`/`script`/`razorpay`/`payment`/`booking`/`review`/`tutors` lines).

## 2. Is every changed file in scope? — **PASS**

Every path belongs to the application-form work: the two Apps Script seams, the three
wizard assets, the generated schema, the generator, one intake client file, five test
files, three reports and the runbook. **No payment, Razorpay, booking, review, tutor-feed
or unrelated page file is modified or added.**

## 3. DEF-1 — untouched selects keep their existing values — **PASS**

Verified at both ends, independently of the existing suite.

- **Markup.** `#jw-duration`, `#jw-currency`, `#jw-hindi-level` each start with an empty
  `<option value="" …>`, carry a `data-label`, and contain **no `selected` attribute** —
  nothing forces a value the applicant did not pick.
- **Payload.** With the form untouched, `buildPayload()` emits **none** of the three keys
  (`undefined`), so an untouched select is *absent*, not silently defaulted.
- **Server, first submit.** Chosen values persist (`duration="90 min"`, `currency="INR"`,
  `hindi_level="Native"`).
- **Server, resubmit that omits them** → all three **survive**; the change that *was*
  sent (`city`) still lands; one row, updated in place. This is the actual defect, and it
  is fixed.
- **Explicitly emptied field** → cleared, as the code comment documents, *unless* the
  field carries a schema `default` (see R4).

**Mutation check (on a `/tmp` copy):** reverting the empty-option fix makes the suite
exit non-zero immediately — the "before" copy genuinely crashes/short-circuits because
the untouched form starts sending `50 min` / `USD` / `Native`.

## 4. DEF-2 — applicant input cannot reach a server-owned field — **PASS, with A2 caveat**

Direct evidence:

- **Server-owned columns.** Planting `status`, `approved`, `review_notes`, `reference`,
  `timestamps`… in `fields` changes **nothing**: every status stayed `pending`, every
  `approved` blank, no review note written, the real `reference` untouched. The planted
  value is recorded inertly under `sent_<name>` where it can never be mistaken for the
  real thing.
- **Status transitions / admin authorization.** `ekSetStatus_` / `ekAdminUpdate_` take
  their authority from `EK_ADMIN_TOKEN` only and never read `details_json`. A token
  planted inside `fields` is ignored; the real token still works unchanged; the
  transition writes only its own columns.
- **Downstream consumers.** `details_json` is read in exactly three places in
  `ApplicationIntake.gs` (the writer, the retry scan, the merge). **No other file in the
  repository references it.** `FEED_TABS` exposes `tutors`, `reviews`, `settings`,
  `support` — **`applications` is not a feed tab**, so no applicant free text can reach a
  public page.
- **Cardinality.** The header is still exactly **69 columns**; no invented `sent_*`
  column.
- **Mutation check (on `/tmp`):** removing the divert makes 5 checks fail.

### FINDING A2 — a client-supplied `submission_id` becomes the stored dedupe key — **FAIL (pre-existing, low impact)**

`ekValidateApplication_` diverts `EKGURU_SERVER_ONLY` names, but **`submission_id` is not
a schema column and not in `EKGURU_SERVER_ONLY`**, so it is a *free-text answer*. On the
**insert** path the row builder writes `details_json` from the applicant's free text
(`ekBuildRow_`, line 589-ish), and afterwards line ~748 only overwrites it **if a
submission id exists**:

```
var row = ekBuildRow_(map, values, meta);      /* details_json = client's free text */
if (map.reference !== undefined) row[...] = ref;
if (map.submission_id !== undefined && submissionId) row[...] = submissionId;
```

`submission_id` is not a column, so that second `if` never fires, and
`if (submissionId) details.submission_id = submissionId;` exists **only in the update
path** (`ekUpdateExisting_`, line 874). The consequence, reproduced end-to-end:

1. A normal applicant submits. `details_json` ends up **empty** — the retry key is *not*
   stored on the insert path at all.
2. A second party sends `fields: { submission_id: "<any value>" }`. That value **becomes
   the dedupe key** of their row.
3. A third, unrelated person who happens to send the same id is answered
   `duplicate: true, reference: <the second party's EG->`, is told their application was
   already received, is **not stored**, and **no acknowledgement email is sent**.

*Impact:* bounded — an attacker must know a real id (which is the applicant's own
`EG-` reference), no stored row is modified, no status/admin/data path is reachable, and
nothing is public. It is a silent-loss/notification-suppression primitive, not a
privilege escalation. The correct fix is to add `submission_id` to the reserved-name set
(so it is diverted and the server's own value is written last on **both** paths), plus a
regression check; **`tests/regression/test-defect-regressions.mjs` does not currently catch this**
(proved by mutation: flipping the update-path overwrite to `if (!details.submission_id)`
still leaves **59/59 green**).

Because it is pre-existing and confined to the idempotency bookkeeping, it **does not
block deployment**, but it should be fixed next, before the retry feature is advertised.

Related documentation drift (same root cause): `APPLICATION-BACKEND.md` says a retried
`submission_id` "was retried, or the same email resubmitted within 72 h" — in practice
prevention rests on the **email + 72 h** path, not the id, on a first submission.

## 5. DEF-3 — markup and preview selectors match — **PASS**

Both directions, mechanically:

- **Selector → markup.** All 21 distinct `[data-jw-*]` selectors that `join-wizard.js`
  queries are present in `join.html`; `[data-jw-pv-head]` occurs **exactly once**, is the
  `.jw-preview-head` block, and that block contains the `h3`, `p` and
  `.jw-preview-avatar` the renderer writes.
- **Markup → selector.** The only element inside the header that no renderer touches is
  an anonymous text wrapper `<div>`; the `.jw-pv-edit` affordance is intentionally static
  and its handler is verified present. **No unexplained empty container.**
- **Behaviour.** Driving the real wizard to the review step (7/7 steps) with the real
  `.jw-next` button and the 80 ms lock, the header shows **`Asha Verma`**, **`Jaipur,
  India`**, avatar **`AV`** — the applicant's own answers, never the `Your name` /
  `City, country` / `?` placeholders.
- **Mutation check (on `/tmp`):** removing `data-jw-pv-head` makes 6 checks fail,
  including its own "the before-copy really lost the attribute" setup guard.

## 6. DEF-4 — missing / null / empty / valid `availability_meta` — **PASS**

All four states, one by one, plus the degenerate fifth:

| Payload | Result |
|---|---|
| key absent | accepted; meta **derived** from the one slot (`days:1, slots:1`), timezone carried, `availability_json` filled |
| `null` | same as absent — derived |
| `""` | same as absent — derived |
| valid object | accepted **as given**, not recomputed (`days:3, slots:3` preserved) |
| no slots at all | accepted; meta stays **empty** — nothing invented |

No state produces `[object Object]`, an unparseable cell, or a rejected submission.
**Mutation check (on `/tmp`):** restoring the narrow guard (`== null` only) makes 7
checks fail.

## 7. Do the new tests prove failing-before / fixed-after? — **PASS, with one gap**

- **Genuine before/after.** Each defect block builds a "before" copy by reverting
  *exactly* that one edit, asserts the revert really applied (`DEF-n setup: the
  before-copy really lost …`), then runs the **same** probe against both copies and
  requires before = bug visible, after = fixed. That is a real differential test, not a
  snapshot of current behaviour.
- **The harness is not self-satisfying.** I mutated the production code four times in a
  `/tmp` copy and re-ran the real suite each time:

| Mutation | Suite result |
|---|---|
| DEF-1 empty-option restored to a forced value | **exit 1** (before-copy setup + flow breaks) |
| DEF-2 divert at line 513 removed | **5 FAIL** |
| DEF-3 `data-jw-pv-head` removed | **6 FAIL** |
| DEF-4 guard narrowed to `== null` | **7 FAIL** |
| **A2:** update-path overwrite weakened to `if (!details.submission_id)` | **59/59 still PASS** ← the gap |

So the suite genuinely fails when the four fixes are undone — **except** it has no
assertion over the insert-path `submission_id` overwrite (finding A2).
- **`test-join-wizard.mjs` is a shallow staleness gate**, not a full drift check: it only
  proves every header/field name *appears* in `js/join-schema.js`. I therefore verified
  drift properly, on a `/tmp` copy: a fresh `build-join-schema.mjs` run is
  **byte-identical** to the committed `js/join-schema.js` — **no drift**. The browser copy
  legitimately contains all 69 field definitions (including the 18 server-only columns,
  which the wizard explicitly skips via `SCHEMA.serverOnly`, line 703); that is by design,
  not a leak.
- **No test was weakened.** The two modified test files only *add* assertions
  (`test-intake.js` +13, `test-live-feed.js` +8). No assertion was deleted or relaxed in
  the diff.

## 8. Existing payment / booking / feed / publishing / admin workflows — **PASS for static + router evidence; NOT VERIFIED for live**

- **Payment.** **Zero** payment, Razorpay or booking files are modified or added; the diff
  contains no payment markup or code. The payment suites are untouched. *(Per standing
  instruction, payment code was not audited further.)*
- **Router shape.** Still exactly **one `doGet` and one `doPost`**; neither function
  signature appears in the diff.
- **Behaviour preserved through the real router** (all checked): unknown kind refused;
  contact without consent refused; a review without a matching booking still refused by
  the genuine-review gate; feed CSV and JSON both answer; unknown tab refused;
  `?action=health` still answers as intake health; a wrong-token `?action=ping` still
  refused; the maintenance switch still blocks everything; a bare `/exec` still reports
  `unified: 2.2.0`.
- **Seam isolation.** `ekApplicationAction_` returns `null` for `booking`/`contact`, and
  `ekApplicationGet_` returns `null` for `health` — so a booking POST is **not** hijacked
  by the application seam.
- **Tutor publishing / admin.** Nothing writes the `tutors` tab on approval (approval
  only writes its own columns); the sheet menu only gains the two new items.
- **NOT VERIFIED:** a live end-to-end payment or booking transaction against the deployed
  endpoint, and a real Sheet read. Only static + mocked-router evidence is available here.

## 9. Deployment prerequisites, rollback and residual risks

### FINDING A1 — honeypot runs *after* the application seam in standalone `Intake.gs` — **FAIL (pre-existing, deployment-shape dependent)**

`Unified.gs` `intakePost_` checks the honeypot **before** calling
`ekApplicationAction_` and documents why. **`apps-script/Intake.gs` was not reordered**:
the seam is at line 212-213, the honeypot at line 226. `ApplicationIntake.gs` does not
check the honeypot itself — it says the router already did. So on a *standalone* intake
deployment a bot that fills the hidden field is **stored and emailed**:

| Deployment shape | Filled honeypot |
|---|---|
| `Unified.gs` (the live shape) | **0 rows, 0 emails** — pretend-success, nothing stored |
| `Intake.gs` standalone | **1 row written, 1 email sent** |

The comment at `ApplicationIntake.gs:1289` — *"the honeypot has already been checked by
the router"* — is only true for `Unified.gs`. Harmless today (the site posts to the
unified URL), but it **invalidates the claim that `Intake.gs` is a drop-in equivalent**.
Either fix the ordering or delete the seam from `Intake.gs`.

### Prerequisites — mandatory, in order

1. **Deploy shape: do NOT paste `Intake.gs`.** Keep the standalone `Intake.gs` out of the
   project, or fix A1 first.
2. Open the intake Apps Script project (bound to the workbook, or with
   `EKGURU_DB_SPREADSHEET_ID` set).
3. **File → New → Script → `ApplicationSchema`** — paste `apps-script/ApplicationSchema.gs`
   whole.
4. **File → New → Script → `ApplicationIntake`** — paste
   `apps-script/ApplicationIntake.gs` whole. The editor must show **no red error**.
5. **Overwrite** the existing `Unified.gs` with the repository copy (version must read
   **2.2.0**).
6. Set **`EK_ADMIN_TOKEN`** (long random, `openssl rand -hex 24`). Without it every admin
   action refuses — that is the safe default, not a failure.
7. Consider **`APPLICATION_MAIL_ENABLED=false`** for the first hour, so a bad template is
   caught before it reaches applicants.
8. Run **`ekMigrateApplications`** once; expect
   `68/68`-style output with **69 columns present** and "0 rows moved".
9. **Deploy → Manage deployments → ✏️ Edit → New version.** **Never "New deployment"** —
   it mints a new URL and silently sends every application back to the mailto fallback.
10. Verify `?action=health` shows the application block as present (not `absent`), and
    `?tab=tutors&format=json` still answers.

### Rollback

- **Frontend only** (safest, instant): deploy the previous `join.html` + `js/` pair. The
  wizard is inert without `js/join-wizard.js`; the form still has a `mailto:` action as a
  last resort.
- **Backend only:** `Deploy → Manage deployments → Edit →` select the **previous version**
  → Deploy. The URL does not change. The new columns are additive and harmless to the old
  code, so no reverse migration is needed.
- **Full:** revert both. The `applications` tab keeps the added columns (blank for old
  rows); no applicant data is lost by rolling back.
- **Do not** run any migration "down" script — none exists, and none is needed.

### Residual risks

| # | Risk | Severity |
|---|---|---|
| R1 | **A1** — standalone `Intake.gs` stores honeypot submissions | High **only** if that shape is deployed; none on `Unified.gs` |
| R2 | **A2** — a client-supplied `submission_id` becomes the dedupe key; a third party sharing that value is silently told "already received", no row, no email | Low, not blocking; fix by reserving the name |
| R3 | **Visual/UX unverified** — no real browser: 360 px layout, focus ring, contrast, iOS/Firefox `<select>` | Medium; needs a human pass |
| R4 | Clearing `currency`/`duration` snaps back to the schema default (`USD`/`50 min`) instead of blanking — `default` always wins in `ekBuildRow_` | Low, and arguably intended |
| R5 | A stale cached client can still explicitly send `50 min` / `USD` / `Native`, which the server accepts as a real answer | Low |
| R6 | `availability_meta` has two valid shapes (`{days,timezone,format}` vs `{days,slots,timezone,format}`); any consumer must tolerate both | Low |
| R7 | `sent_*` keys share the `EKGURU_DETAILS_MAX_KEYS` budget, so a flood of reserved names can crowd out genuine overflow answers | Low |
| R8 | `teach_langs_json` / `notes` / `source` are unreachable by any form control; `EK_MAIL_MAX_PER_RUN` is unused | Cosmetic / dead config |
| R9 | Documentation overstates idempotency (`submission_id` is not stored on the insert path) | Low; same root cause as R2 |

---

## Exact final column count — **69**

`schema version 2.1.0` · **69 logical fields** · **69 physical columns** · **69 unique**
(no duplicates) · **18 server-only** · the original 17 legacy columns are all present, in
their original order, as the first 17.

---

## Confirmation

No production Sheet was read or written. No deployment or Script Property was changed. No
email was sent. No file was edited. Nothing was staged, committed, pushed or reset.
`git status` remains **7 modified, 14 untracked, 0 staged**; `HEAD` remains `7ad9f99`.

**The audit ended there, and no deployment was performed.**

---

# Addendum — A1 and A2 fixed (follow-up pass)

The audit above was read-only and found two FAILs. They have since been fixed, with the
same failing-before / fixed-after discipline as DEF-1…DEF-4. **Nothing is deployed.**

### A1 — fixed (`apps-script/Intake.gs`, 1.3.0 → 1.3.1)

The honeypot check now runs **before** `ekApplicationAction_(body)`, matching `Unified.gs`,
with the same explanatory comment. Verified through the standalone router:

| | before | after |
|---|---|---|
| filled honeypot → rows written | **1** | **0** |
| filled honeypot → emails sent | **1** | **0** |
| bot still sees a believable success | yes | yes |
| a genuine submission still stored + emailed | yes | yes |

`Unified.gs` is unchanged and still writes 0 rows / 0 emails for a bot.

### A2 — fixed (`apps-script/ApplicationIntake.gs`, 2.0.0 → 2.0.1)

Two changes, both needed:

1. **`submission_id` is now reserved** alongside `EKGURU_SERVER_ONLY`, so it is never
   treated as a free-text answer. A planted value is diverted and kept inertly as
   `sent_submission_id`.
2. **The insert path now writes the server's retry key** into `details_json` after
   `ekBuildRow_`, mirroring the update path. Before this, a first submission stored **no**
   retry key at all.

| | before | after |
|---|---|---|
| first submission stores its own retry key | **no** | **yes** |
| a planted value becomes the dedupe key | **yes** | **no** |
| an unrelated third party sharing that value is short-circuited | **yes** (not stored, told "already received", no email) | **no** (stored, acknowledged) |
| a genuine retry of the same id still dedupes | — | **yes**, one row, same reference |
| the honest applicant's row is disturbed | no | no |

### Regression coverage

`tests/regression/test-defect-regressions.mjs` gained **23 checks** (59 → **82**), in the same style:
a "before" copy is built by reverting *exactly* the fix, its applicability is asserted, and
the same probe must show the bug before and the fix after. Two of those checks exist
specifically because the first draft of this harness was wrong — the A1 revert initially
inserted the seam *after* the honeypot, and the A2 revert un-reserved the name without
removing the insert-path write, so the "before" copies did not reproduce the bug.

`npm test` now: **exit 0**, zero FAIL — defect-regressions **82/82**, wizard-sheets-e2e
77/77, backend 120/120, wizard 117, intake 26, Runtime QA 143, Apps Script 31, E2E 11,
contract 8, gates 30/30.

### Documentation corrected

`apps-script/APPLICATION-BACKEND.md` overstated idempotency (it claimed a retried
`submission_id` was always deduped, which was false on the insert path) and called
`Intake.gs` a drop-in equivalent. Both statements now match the code, and the
"68 columns" / "87 backend checks" / "61 wizard checks" figures were refreshed to
69 / 120 / 117.

### Residual

- **R2 is closed.** The remaining risks are R3 (no real-browser visual QA — still
  **NOT VERIFIED / pending**), R4 (`currency`/`duration` snap to their schema default when
  explicitly cleared), R5 (a stale cached client can still send an explicit value), R6
  (two valid `availability_meta` shapes), R7 (`sent_*` sharing the details key budget),
  R8 (unreachable fields / unused config), and R10 below.
- **R10 (new, low):** rows already stored before 2.0.1 carry no retry key, so a retry of
  one of those is caught by the 72-hour email window rather than by the id. This is
  documented in the runbook; no migration is needed or wanted.

**No deployment, no migration, no Sheet access and no email took place in this pass either.**

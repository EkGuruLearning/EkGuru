# Backend Consolidation — INSPECTION COMPLETE: **BLOCKED**

**Branch:** `arena/2046092b-ekguru` @ `7ad9f99`
**Mode:** inspection only. **No file merged, created, edited, moved or deleted.** Working tree untouched.

---

## STOP — the consolidation cannot be done safely as specified

Your rule: *"If consolidation requires changing runtime behavior or cannot be verified
safely, STOP and report the blocker instead of guessing."*

That trigger has fired. There are **three** blockers, and each one alone is fatal to a
literal "put everything in one `Code.gs`" merge. Nothing was merged.

The single most important discovery:

> ### `apps-script/Code.gs` already exists, and it is NOT the feed/intake backend.
> ### It is the **Razorpay payment backend** — 1898 lines, committed to git, with its own `doGet()` and `doPost()`.

---

## 1. Every `.gs` file inspected

8 files, 6 495 lines total.

| File | Lines | Git state | Role | Own `doGet`/`doPost`? |
|---|---|---|---|---|
| `apps-script/Code.gs` | 1898 | **tracked (committed)** | **Razorpay payments + support** backend | **yes** (`:816`, `:992`) |
| `apps-script/Unified.gs` | 1357 | modified | **Canonical** feed + intake router | **yes** |
| `apps-script/ApplicationIntake.gs` | 1470 | untracked | Application backend v2.0.2 (51 fns) | no |
| `apps-script/ApplicationSchema.gs` | 329 | untracked | 69-column schema, single source of truth | no |
| `apps-script/Intake.gs` | 604 | modified | Standalone intake router (legacy shape) | **yes** |
| `apps-script/LiveFeed.gs` | 283 | tracked | Standalone feed router (legacy shape) | **yes** (`doGet`) |
| `tools/apps-script-mailer.gs` | 385 | tracked | **Separate** mailer project, drop-in `Code.gs` | — |
| `tools/apps-script-questions.gs` | 170 | tracked | **Separate** questions-API project | — |

**Canonical backend confirmed: `Unified.gs`.** Its own header, `UNIFIED-SETUP.md:37`, and
`APPLICATION-BACKEND.md:38` all say so.

---

## 2. The three blockers

### B1 — `Code.gs` is already taken, by payments

`apps-script/Code.gs` is the live payment backend:

```
GET  ?action=health | diagnostics | currencies | recent-support
POST ?action=create-order | verify-payment | webhook | report-failure | report-cancel
```

It defaults to `SPREADSHEET_ID_DEFAULT = "1u5Jkbe_…"` and writes the tabs
`Payments`, `Customers`, `Refunds`, `WebhookEvents`, `PublicSupport`. It never mentions
`tutors`, `reviews_pending` or `applications` (0 matches).

Merging the form backend into this file would:

- collide on `doGet`/`doPost` (**two of each in one file — invalid**);
- put the payment code and the intake code in one project, where the two share a global
  scope;
- almost certainly change **which workbook the payments run against**, because the merged
  file would have both `SPREADSHEET_ID_DEFAULT` and `intakeSpreadsheet_()`, and a bound
  project resolves `getActiveSpreadsheet()` first.

That last point is a silent financial-data hazard on a **live** backend. It also
directly violates two of your own rules: *payment remains FROZEN* and *do not change
Script Properties, deployment IDs, Sheet IDs*.

### B2 — these are separate Apps Script projects **by design**

`apps-script/LIVE-FEED-SETUP.md` (verbatim):

> The payments backend (`apps-script/Code.gs`) is a separate project **on purpose**

`apps-script/UNIFIED-SETUP.md` (verbatim):

> ⚠️ Do **NOT** use the payments project (the one whose Code.gs talks about Razorpay) or
> the questions project. **Each backend is its own project; mixing them breaks both.**

So the docs state the opposite of what the task requires. Consolidating them is not a
refactor — it is an architecture change to all three runtimes.

### B3 — 24 duplicate function names; the files cannot coexist in one project

Apps Script puts **every** `.gs` in a project into **one global scope**. The repo's files
therefore *cannot* be pasted into the same project at all — the current library only
works because each is deployed separately.

Duplicates between `LiveFeed.gs` and `Unified.gs` (12): `buildCsv_`, `buildHealth_`,
`clearFeedCache`, `csvCell_`, `findSheet_`, `installTriggers`, `isPrivateColumn_`,
`jsonOut_`, `onEdit`, `readCached_`, `readTab_`, `reviewsFeed_`.
Duplicates between `Intake.gs` and `Unified.gs` (11): `intakeAppend_`,
`intakeAppendLocked_`, `intakeHealth_`, `intakeJson_`, `intakeNormRef_`, `intakeQuota_`,
`intakeRef_`, `intakeReviewGate_`, `intakeSpreadsheet_`, `intakeValidate_`,
`markContactReplied_`.
Plus `doGet`/`doPost` across up to 4 files.

Your requirement *"Do not create duplicate functions"* is achievable — but only by
**deleting** one copy of each pair, which means choosing between two implementations that
were deliberately forked. That is a behaviour decision, not a mechanical merge.

Two further blockers inside `tools/`:

- `tools/apps-script-mailer.gs` is documented as *"a complete, drop-in `Code.gs`"* for its
  own project — a second file that calls itself `Code.gs`.
- `tools/apps-script-questions.gs` is likewise a separate project.

---

## 3. What a safe consolidation would actually require

Not "one file" but **one file per project**, and a decision from you on each:

| Project | Would become | Needs your decision |
|---|---|---|
| Form/feed project | `Unified.gs` + `ApplicationIntake.gs` + `ApplicationSchema.gs` → **one `Code.gs`** | ✅ feasible, no duplicates between these three |
| Payments project | `Code.gs` stays **as-is** | should it stay frozen exactly as it is? |
| Legacy alternates | `Intake.gs`, `LiveFeed.gs` | **delete**, or keep as documentation? |
| Mailer / questions | stay separate | out of scope? |

**The genuinely safe subset** is the first row: the three form-backend files have **zero**
name collisions with each other (verified — see §5) and no `doGet`/`doPost` conflict,
because only `Unified.gs` has them. That merge is mechanical and verifiable.

**It cannot be extended to `Code.gs`** without breaking payments.

---

## 4. Why I did not merge anything

Your task says *"Consolidate ... into ONE file named `Code.gs`"*. The file that must
receive the code is the payment backend. Any literal execution of the instruction either:

- **(a)** puts payments and form-intake in one project → breaks both, per the repo's own
  deployment docs, and risks the live financial backend reading the wrong workbook; or
- **(b)** renames/overwrites the payment `Code.gs` → not allowed (payments frozen, no
  deployment-ID/config changes); or
- **(c)** merges only the three form files into a `Code.gs` while payments also stays
  `Code.gs` → two files with the same name, which contradicts the goal.

You explicitly said not to guess. So I stopped.

---

## 5. Evidence gathered for the safe subset (so the work is ready to go)

Verified **read-only**, so a decision needs no re-inspection:

| Fact | Value |
|---|---|
| `Unified.gs` + `ApplicationIntake.gs` + `ApplicationSchema.gs` shared function names | **0** |
| Their combined top-level functions | 46 + 51 + 7 = **104** |
| `doGet`/`doPost` within that trio | exactly **1 each** (both in `Unified.gs`) |
| Global-var collisions among the trio | none (`EK_`, `EKGURU_*`, `EK_*`, `INTAKE_*` namespaces are disjoint) |
| Schema contract | 2.1.0 / 69 columns, `ApplicationSchema.gs` ⇄ `js/join-schema.js` per-field identical |
| External contracts to preserve | `doGet`/`doPost`, `ekApplicationAction_`, `ekApplicationGet_`, `ekHealth_`, `ekApplicationQuota_`, `selfTest_`, `onOpen`, `onEdit`, `installTriggers`, `clearFeedCache` |

Tests are a hard constraint on any rename:

| Test | Loads |
|---|---|
| `test-apps-script.mjs` | **`apps-script/Code.gs`** (payment) — hardcoded path, 31 checks |
| `test-live-feed.js` | `apps-script/LiveFeed.gs` |
| `test-application-backend.mjs` | `ApplicationSchema.gs`, `ApplicationIntake.gs`, `Intake.gs`, `Unified.gs` |
| `test-defect-regressions.mjs` | same four |
| `test-wizard-sheets-e2e.mjs` | `ApplicationSchema.gs`, `ApplicationIntake.gs`, `Unified.gs` |

**Consequence:** a file named `Code.gs` is already load-bearing for the payment suite, so a
new `Code.gs` for the form backend would have to coexist with that path unless the test is
re-pointed — which touches payment verification, i.e. frozen code.

---

## 6. Repository status

Unchanged by this inspection:

```
HEAD           7ad9f992f0351e10bd11b249eb58488a5437cf2a  (7ad9f99)
modified       7
untracked      17   (no new files created)
staged         0
```

No `.gs` file created, deleted, renamed or edited. No package installed, no lockfile
change, no commit/push/stage/reset, no production access, no email, no deployment.

---

## 7. Recommendation — pick one, and I will execute it

**Option A (recommended, safe, fully verifiable):**
Merge `ApplicationIntake.gs` + `ApplicationSchema.gs` into `Unified.gs` and ship that as
the form project's single `Code.gs` **in a new directory** (e.g. `apps-script/form/Code.gs`),
leaving the payment `Code.gs` exactly where it is. Re-point the four form tests at the new
file. Delete `Intake.gs` and `LiveFeed.gs` only after the suite proves equivalence.
→ One file per project, zero payment risk, all your verification criteria satisfiable.

**Option B:** Same as A, but name the merged form file `Code.gs` inside
`apps-script/form/`, and move the payment file to `apps-script/payments/Code.gs` (path-only
move, contents byte-identical, no logic touched). Requires your explicit approval because
it touches a payments file path.

**Option C:** Merge everything including payments into one project — **I do not recommend
this.** It contradicts the repo's deployment docs, risks the live financial backend, and I
could not verify equivalence safely.

**Option D:** Keep the form backend split as it is and only add section headings. Smallest
change, but does not meet your one-file goal.

Tell me which option, and whether `Intake.gs` / `LiveFeed.gs` should be deleted or
retained as legacy reference. I have not touched anything.

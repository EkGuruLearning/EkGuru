# DEF-1 … DEF-4 — Four Defect Fixes

**Task:** fix only the four defects identified by `FINAL-VERIFICATION-REPORT.md`, each with a
regression test that was **seen to fail before the fix and pass after it**.
**Branch:** `arena/2046092b-ekguru` (from `7ad9f992`). **Date:** 2026-11-23.

**Nothing was deployed.** No production Sheet was read or written, no Apps Script deployment
or Script Property was changed, no email was sent, no external service was contacted, and
nothing was committed, pushed or reset. Full confirmation in §7.

## Read before changing anything

`FINAL-VERIFICATION-REPORT.md` (§1–§7 findings, §8 follow-up), `apps-script/APPLICATION-BACKEND.md`
(mapping, §13a WhatsApp, server-only list), `FINAL-IMPLEMENTATION-REPORT.md` §4/§5/§10,
`README` — there is no `README` file in this repository, `package.json` scripts instead — plus the
affected code in full: `join.html` (the seven step sections and the review markup),
`js/join-wizard.js` (`buildPayload`, `renderPreview`, `validateStep`, `HELP_TEXT`),
`apps-script/ApplicationSchema.gs` (`EKGURU_APPLICATION_FIELDS`, `EKGURU_SERVER_ONLY`,
`ekNormDash`), and `apps-script/ApplicationIntake.gs` (`ekValidateApplication_`, `ekBuildRow_`,
`ekUpdateExisting_`, `ekApplicationAction_`).

Payment, Razorpay, bookings, reviews, tutor feed and every unrelated route were **not opened
for editing**; the only reason `apps-script/Unified.gs` appears in the tree at all is the
earlier, already-verified work — this task did not touch it.

---

## 1. DEF-1 — a resubmission no longer loses `duration` / `currency` / `hindi_level`

**Root cause.** `#jw-duration`, `#jw-currency` and `#jw-hindi-level` opened on a real value
(`50 min`, `USD`, `Native`). `buildPayload` sends any non-empty value it finds, so **every**
submission — including a resubmission where the tutor never touched those selects — carried
those defaults. On the server `values.__supplied` therefore marked them "answered this time",
so `ekUpdateExisting_` did not keep the stored answer and wrote the default over it.

**Files / functions changed**

| File | Change |
|---|---|
| `join.html` | the three `<select>`s gain `<option value="">Select</option>` as the first option and a `data-label` (`Lesson length`, `Currency`, `Your Hindi level`) so a future error can name the field |
| `js/join-wizard.js` → `renderPreview()` | the price line was `"$" + rate + " / " + (duration \|\| "50 min")`, which invented a length the tutor had not chosen; now `/ 60 min` appears only when a length is set |
| `js/join-wizard.js` → file header | corrected a stale "six-step / 13 columns / packed into notes" comment that no longer described the code |

**Before / after**

| | before | after |
|---|---|---|
| untouched form → `buildPayload` | sends `50 min`, `USD`, `Native` | sends none of the three |
| tutor had stored `90 min / INR / Fluent`, later edits only the city | all three reset to the defaults | all three survive |
| a brand-new application | `50 min` / `USD` defaults applied by the server | **unchanged** — same defaults |

**Proved by:** `tools/test-defect-regressions.mjs` (DEF-1 section, 13 checks), below;
`tools/test-wizard-sheets-e2e.mjs` §D; `tools/test-join-wizard.mjs` blocks 23 and 25.

---

## 2. DEF-2 — `details_json` no longer accepts a server-owned column name

**Root cause.** The documented overflow rule copies any key it does not recognise into
`details_json`. `status`, `approved` and `review_notes` have **no client `src`**, so `known[]`
never contained them; they fell through to the overflow path and were stored under their own
names. The real cells were never at risk (`EKGURU_SERVER_ONLY` already skipped them) — but an
owner reading `details_json` would see applicant-supplied text under `"review_notes"`.

**Files / functions changed** — `apps-script/ApplicationIntake.gs` → `ekValidateApplication_()`:

- a `reservedNames` lookup is built once from `EKGURU_SERVER_ONLY`;
- both overflow passes (`fields` and `fields.details`) now **divert** a reserved name instead of
  queueing it under its own key;
- the diverted value is recorded as `sent_<name>`, truncated and `ekCleanText_`-sanitised, within
  the existing `EKGURU_DETAILS_MAX_KEYS` budget — so nothing is silently binned and nothing can
  be mistaken for a verdict.

**Before / after**

| payload | before | after |
|---|---|---|
| `fields.review_notes = "PRIVATE: forged"` | `details_json` = `{"review_notes":"PRIVATE: forged"}` | `details_json` = `{"sent_review_notes":"PRIVATE: forged"}` |
| `fields.status` / `fields.approved` | stored under their own keys | not stored under their own keys |
| the `status` / `approved` / `review_notes` **cells** | untouched (already correct) | untouched |
| `fields.referral = "a friend"` (no column) | kept verbatim | kept verbatim |
| `ekAdminUpdate` authorisation | token required | **unchanged** |

**Contract unchanged:** same request shape, same response shape, same `ok`/`reference`/
`duplicate`/`mail` fields. Proved by `tools/test-application-backend.mjs` block 30 and the
DEF-2 section of `tools/test-defect-regressions.mjs` (14 checks, including an explicit
"admin token still required" assertion).

---

## 3. DEF-3 — the review preview header now renders the applicant

**Root cause.** `renderPreview()` has always queried `$("[data-jw-pv-head]", form)`, but
`join.html`'s `<div class="jw-preview-head">` did not carry that attribute, so the whole header
block was skipped: name, city/country and the photo-or-initials avatar were never written and
the markup placeholders (`Your name`, `City, country`, `?`) stayed on screen while the lede
promised "exactly what a student will see".

**Files / functions changed**

| File | Change |
|---|---|
| `join.html` | `data-jw-pv-head=""` added to `div.jw-preview-head` — aligning the markup with the selector the script already used rather than changing the script |

**Before / after**

| | before | after |
|---|---|---|
| header `<h3>` | `Your name` | the tutor's name |
| header `<p>` | `City, country` | `Jaipur, India` |
| avatar | `?` | initials (`PP`) |
| avatar with a photo link | `?` | `background-image: url("https://…")`, text cleared |
| nothing typed yet | placeholder text | **same deliberate fallback**, never an empty box |

**Proved by:** `tools/test-defect-regressions.mjs` DEF-3 section (12 checks), `tools/test-join-wizard.mjs`
block 24, `tools/test-wizard-sheets-e2e.mjs` §A.

---

## 4. DEF-4 — `availability_meta` is derived when it is missing

**Root cause.** `ekBuildRow_` derived the meta only `if (values.availability_meta == null)`, but
validation had already set `""` for a payload that did not mention it, so the branch could never
fire. A non-browser client sending bare `availability_slots` got a filled `availability_json`
next to an empty `availability_meta`.

**Files / functions changed** — `apps-script/ApplicationIntake.gs` → `ekBuildRow_()`:
the guard is now `if (values.availability_meta == null || values.availability_meta === "")`.
A client-supplied value is still respected.

**All four cases tested explicitly** (`tools/test-defect-regressions.mjs`, DEF-4 section):

| `availability_meta` in payload | before | after |
|---|---|---|
| **missing** | `""` (bug) | derived `{"days":1,"slots":1,"timezone":"Asia/Kolkata","format":"weekly-hours"}` |
| **`null`** | `""` (bug) | same derived value |
| **`""`** | `""` (bug) | same derived value |
| **valid `{days:7,slots:7,…}`** | respected (`slots:7`) | **still respected, not recomputed** |
| no `availability_slots` at all | `""` | `""` — no meta invented for an empty answer |
| the **browser** wizard payload | sends its own `{days, timezone, format}` | **unchanged** — still sent, still used |

Also proved in `tools/test-application-backend.mjs` block 31 and in the full row of
`tools/test-wizard-sheets-e2e.mjs`.

---

## 5. Tests executed

### New suites added to `npm test`

**`tools/test-defect-regressions.mjs` — 59 passed, 0 failed**

The failing-before/fixed-after proof. For each defect it reverts **exactly that one fix** out of
the current file *in memory* (nothing on disk is touched, nothing is stashed), asserts the
revert really applied, then runs the identical check against both copies:

| Defect | before-copy behaviour observed | after behaviour |
|---|---|---|
| DEF-1 | untouched form sends `50 min`/`USD`/`Native`; stored `90 min`/`INR`/`Fluent` all overwritten | none sent; all three survive; new applications still default |
| DEF-2 | `details_json.review_notes === "PRIVATE: forged"` | `sent_review_notes` only |
| DEF-3 | header shows `Your name` / `City, country` / `?` | name, `Jaipur, India`, initials |
| DEF-4 | missing/null/`""` all leave the column empty | all three derive a valid meta; a valid value is untouched |

**`tools/test-wizard-sheets-e2e.mjs` — 77 passed, 0 failed**

Real `join.html` + real `js/join-wizard.js`, driven by real DOM events (`input`, `change`,
`blur`, `click`, `keydown` on chips) **from Personal through Review & Submit**: all required
answers, two subjects, two levels, education, profile, price 15, length 60 min, currency USD,
two availability days with times, consent — then Submit. The body the browser would POST is
captured at the network boundary and handed unchanged to the real `ApplicationIntake.gs` +
`Unified.gs` against a **mocked `SpreadsheetApp`**:

- one row written, 69 columns, one acknowledgement email;
- the **complete row printed column by column** and every value checked against the mapping
  (30 assertions) — including `whatsapp` = `+919876543210`, `subject`, `levels_json`,
  `availability_json`, `availability_meta`, `details_json` containing only `referral`,
  `status = pending`, `approved` blank, `schema_version 2.1.0`;
- then a **resubmission** that changes only the city and the price: status stays `approved`,
  `approved = Yes`, the private `review_notes` and `reviewed_by` survive, **WhatsApp survives**,
  the photo link survives, `60 min` / `USD` / `Native` survive (DEF-1), education, intro,
  headline, consent, reference and original timestamp all survive, the genuine overflow answer
  survives, and one row is still one row.

### Everything else, re-run after the changes

| Suite | Result |
|---|---|
| `npm test` | **exit 0, 0 failures** — 30/30 payment gates, backend **120**, defect-regressions **59**, wizard-sheets-e2e **77**, intake 26/26, Runtime QA 143/143, Apps Script 31/31, E2E 11/11, contract 8/8, live-feed 69 |
| `tools/test-join-wizard.mjs` | **117 PASS** (blocks 23, 24, 25 are the new permanent ones) |
| `tools/test-application-backend.mjs` | **120 checks** (block 30 = DEF-2, block 31 = DEF-4) |
| schema drift | **none** — generated 20113 = on disk 20113, 0 field mismatches |
| migration | pass — append-only, data preserved, 69 columns, second run idempotent |
| phase 6 / phase 7 | **45/45** / **100/100** |
| earlier verification suites (§1 §3 §4 §5) | 19 / 39 / 60 / 86 — unchanged and green |

---

## 6. Remaining limitations

1. **No real-browser visual QA.** There is no browser in this environment (no Chrome, Chromium,
   Playwright or Puppeteer), so **every UI result here is jsdom**, not a rendering engine. Not
   verified visually: how the three new `Select` rows look, whether the now-populated preview
   header aligns with the avatar at 360 px, focus-ring appearance, colour contrast, and
   iOS/Firefox `<select>` differences. jsdom is not real-browser QA and is not claimed as such.
2. **A stale client can still overwrite.** A browser with a cached pre-fix `join.html` keeps
   sending `50 min`/`USD`/`Native`; the server cannot tell a stale default from a real choice,
   so it stores it. The fix removes the form's habit of answering on the tutor's behalf — it
   does not (and cannot) police an explicit value.
3. **`availability_meta` has two valid shapes.** The browser sends
   `{days, timezone, format}`; the server's derived fallback adds `slots`. Both are accepted and
   this is asserted in the tests, but the two producers do not emit byte-identical JSON.
4. **`sent_*` keys share the `details_json` budget** (`EKGURU_DETAILS_MAX_KEYS`). A client that
   sends many reserved names plus many genuine overflow answers could reach the cap; the
   genuine answers are queued first, so they win, and the excess is dropped rather than written.
5. **DEF-2 is tamper-evidence, not authorisation.** It stops applicant text from *looking* like
   a reviewer's verdict inside `details_json`. The actual protection was, and remains,
   `EKGURU_SERVER_ONLY` plus `EK_ADMIN_TOKEN`; neither was changed.
6. **Pre-existing, untouched:** `teach_langs_json` has no form control (documented gap),
   `EK_MAIL_MAX_PER_RUN` is unused, and the rate limiter is cache-based as before.

---

## 7. Confirmation

- **No production Google Sheet** was opened, read or written. Every backend run used an
  in-memory `SpreadsheetApp` mock created in the test file.
- **No production deployment** — no `clasp push`, no new Apps Script version, no `/exec` call.
  No Script Property was created or changed (the `EK_ADMIN_TOKEN` in the tests is a local
  `"tok-test-only"` string in the mock).
- **No real email** — `GmailApp`/`MailApp` are captured in an array; the only "sends" are objects
  in memory.
- **No external service** was contacted.
- **No commit, push, reset or other destructive git operation.** All four fixes and both new test
  files are uncommitted working-tree changes on `arena/2046092b-ekguru`, awaiting authorisation.
- **No payment, Razorpay, booking, review, tutor-feed or unrelated code was edited.**
- **No schema change.** Still exactly **69 columns**, legacy 17 unchanged and in place, no
  column reordered, renamed or removed.
- **Unified Apps Script architecture preserved** — still exactly one `doGet` and one `doPost`.

Work is complete and paused here. Deployment needs separate authorisation.

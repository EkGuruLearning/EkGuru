# EkGuru Tutor Application — Wizard, Validation & Sheets Fix

**Branch:** `arena/2046092b-ekguru` @ `7ad9f99` · **Date:** 2026-11-23 · **Schema:** 2.1.0 (69 columns)

Nothing deployed, nothing committed, no push. No live spreadsheet touched, no real email sent, no Script Property changed. Payment, Razorpay, bookings, reviews and the tutor feed were not modified.

---

## 1. Exact root cause of the Pricing/Timing failure

**The day rows were rendered dead and nothing ever revived them.**

`join.html` shipped all seven rows as:

```html
<div class="jw-day is-off" data-day="Mon">
  <input name="day-mon" type="checkbox"/>
  <input name="mon-from" type="time" disabled=""/>
  <input name="mon-to"   type="time" disabled=""/>
</div>
```

The checkbox had **no handler**. There was no `removeAttribute("disabled")` for a day time input anywhere in `js/` — the only re-enabler was `syncConditionals()`, which loops over `[data-when]` conditional blocks, and the day rows are not one.

So the sequence a real tutor hit was:

1. Tick Monday → the row keeps `class="is-off"`, both time inputs stay `disabled`.
2. A disabled input cannot be focused or typed into, so the hours can never be filled.
3. Press Continue → `validateStep` correctly says *"Mon: add a start and time"*.
4. That message is **unsatisfiable**. The applicant is permanently stuck on step 5, and because Pricing lives on the same step, the price error behind it is never the one they can act on.

**Fixed** with a small explicit state machine (`setDayState` / `syncDayRows`). On tick: row loses `is-off`, both time inputs are enabled, `aria-expanded` goes true, focus moves into the start time. On untick: the inputs are disabled again and the row returns to `is-off`. It runs on change, on every `showStep`, and once at init (so a browser-restored tick comes back live). The checkbox itself is never disabled — otherwise the tick could not be undone.

## 2. Root cause of every other silent failure

| # | Symptom | Cause | Fix |
|---|---|---|---|
| 2.1 | Submit did nothing, no error, on step 7 | `refreshSubmit()` set `sb.disabled = !allGood`. A disabled button swallows the click, so the `submit` handler — and all its error rendering — never ran. | Submit is now disabled **only** while a request is in flight. There is also a live hint under it ("2 steps still need an answer — Submit will take you there"). |
| 2.2 | Consent failure gave no field-level message | The two consent boxes had no error element at all; `#jw-consent-e` was a single shared line that nothing wrote to. | Each box now has its own `.jw-err` and its own sentence ("Please confirm that the details you have given are true…"), plus a short summary label. |
| 2.3 | **Email field showed no error at all** | `#jw-email-e` did not exist in the markup. `showError()` looked for it, found nothing, and silently dropped the message — only the step summary mentioned it. | 37 missing error boxes added across all steps; every answerable field now has one. |
| 2.4 | Error boxes were inside `<select>`/`<textarea>` | The markup generator inserted them before `</select>`, i.e. inside the element. Invalid HTML; the browser relocates or drops them. | Moved to after the closing tag. Verified zero remain inside a control. |
| 2.5 | Only one broken day reported at a time | `availabilityProblem()` returned the **first** problem only. Fix Monday → press Continue → discover Tuesday was broken too. | `availabilityIssues()` returns one entry per broken day; the shared line under the days block joins them all. |
| 2.6 | A day's message had nowhere to appear | The time inputs sit in `.jw-slots` with no `.jw-err`; the shared box is a **sibling** of `.jw-days`, not a child, so `$(".jw-err", block)` found nothing. | `dayGroupBox()` resolves it properly; `paintErrors()` owns the shared line so no single field can overwrite the others' messages. |
| 2.7 | Network retry risked a duplicate row | The page never sent `submission_id`, so the server's idempotent-retry branch was unreachable; only the email-dedupe window stood in the way. | `js/intake.js` mints a per-attempt id in `sessionStorage`, sends it, and clears it only after the server accepts. |
| 2.8 | Resubmission erased earlier answers | `ekUpdateExisting_` rewrote the whole row; any optional column absent from the new payload became `""`. | Row-level **merge**: a field the request did not mention keeps its stored value. A field present but empty *does* clear, because that is what emptying a box means. |
| 2.9 | Honeypot filled → row written + email sent | In `Unified.gs` the application seam ran *before* the honeypot check. | Honeypot check moved above the seam. |
| 2.10 | Rate limit never applied to applications | Same ordering: the seam returns before `intakeQuota_()`. 40 posts were accepted with a cap of 30. | `ekApplicationQuota_()` runs inside the seam, before any write or send. |
| 2.11 | `?action=ekHealth` created an `applications` tab | `ekTab_()` always called `insertSheet`. | `ekTab_(false)` for read-only callers; health reports "no tab yet" and creates nothing. |

## 3. Files changed

| File | What |
|---|---|
| `join.html` | Day-row wiring target, 37 error boxes, consent blocks rebuilt with per-box `.jw-err` + `*`, WhatsApp field, submit hint, `data-label` for consent, optional markers on Lesson length / Trial |
| `js/join-wizard.js` | `setDayState`/`syncDayRows`/`dayGroupBox`/`refreshDayErrors`/`paintErrors`, `availabilityIssues` + full weekday names, `normalisePhone`, Submit never disabled for unanswered questions, consent messages, `phone` rule |
| `js/intake.js` | Per-attempt `submission_id` (mint, send, clear on success) |
| `css/join-wizard.css` | Per-consent-box error layout |
| `js/join-schema.js` | Regenerated from the schema (69 fields, 2.1.0) |
| `apps-script/ApplicationSchema.gs` | `whatsapp` column, `phone` type, version 2.1.0 |
| `apps-script/ApplicationIntake.gs` | Phone validation, merge-on-resubmit, application quota, read-only health tab, `retry_mail`, blank-fill after migration |
| `apps-script/Unified.gs` | Honeypot moved before the application seam |
| `tests/integration/test-application-backend.mjs` | +16 checks (migration safety, WhatsApp); schema version read from the schema instead of hard-coded |
| `tests/regression/test-join-wizard.mjs` | +17 step-5/step-7 regression checks driven by real clicks |
| `apps-script/APPLICATION-BACKEND.md` | 69 columns, 2.1.0, new §13a on the WhatsApp field, health-is-read-only, troubleshooting row |

## 4. Wizard → Sheets field map

| Step | Frontend field | Backend key | Sheet column | Req/Opt |
|---|---|---|---|---|
| 1 | `#jw-name` | `name` | `name` | **Required** |
| 1 | `#jw-display` | `display_name` | `display_name` | Optional |
| 1 | `#jw-email` | `email` | `email` | **Required** |
| 1 | `#jw-city` | `city` | `city` | **Required** |
| 1 | `#jw-country` | `country` | `country` | **Required** |
| 1 | `#jw-state` | `state` | `state` | Optional |
| 1 | `#jw-whatsapp` | `whatsapp` | `whatsapp` | Optional · **private** |
| 1 | `#jw-photo` | `photo_link` | `photo_link` | Optional |
| 1 | `#jw-intro` | `intro` | `intro` | Optional |
| 2 | `subjects` chips | `subjects` | `subjects_json` + derived `subject` | **Required (≥1)** |
| 2 | `levels` chips | `levels` | `levels_json` | **Required (≥1)** |
| 2 | `#jw-hindi-level` | `hindi_level` | `hindi_level` | Optional |
| 2 | `#jw-english-level` | `english_level` | `english_level` | Optional |
| 2 | `#jw-other-langs` | `other_langs` | `other_langs` | Optional |
| 2 | `#jw-years` | `years` | `years` | Optional |
| 2 | `#jw-online-years` | `online_years` | `online_years` | Optional |
| 2 | `#jw-less-exp` | `less_exp` | `less_exp` | Required **only if** years = "Less than 1 year" |
| 2 | `#jw-platforms` | `platforms` | `platforms` | Optional |
| 2 | `methods` chips | `methods` | `methods_json` | Optional |
| 2 | `teachLangs` chips | `teach_langs` | `teach_langs_json` + derived `languages` | Optional |
| 3 | `#jw-edu-qual` | `edu_qual` | `edu_qual` | Optional |
| 3 | `#jw-edu-year` | `edu_year` | `edu_year` | Optional |
| 3 | `#jw-edu-inst` | `edu_inst` | `edu_inst` | Optional |
| 3 | `#jw-certs` | `certs` | `certs` | Optional |
| 3 | `#jw-doc-refs` | `doc_refs` | `doc_refs` | Optional |
| 3 | `#jw-bed-detail` | `bed_detail` | `bed_detail` | Required **only if** qual is a B.Ed |
| 3 | `#jw-edu-extra` | `edu_extra` | `edu_extra` | Optional |
| 4 | `#jw-headline` | `headline` | `headline` | Optional |
| 4 | `#jw-bio` | `bio` | `bio` | **Required** |
| 4 | `#jw-video` | `video_link` | `video_link` | Optional |
| 4 | `#jw-sample` | `sample_link` | `sample_link` | Optional |
| 4 | `#jw-thumb` | `video_thumb` | `video_thumb` | Optional |
| 4 | `#jw-profileurl` | `profile_url` | `profile_url` | Optional |
| 4 | `#jw-linkedin` | `linkedin` | `linkedin` | Optional |
| 4 | `#jw-website` | `website2` | `website` | Optional |
| 5 | `#jw-price` | `rate_usd` | `rate_usd` | **Required** (1–200, whole) |
| 5 | `#jw-duration` | `duration` | `duration` | Optional |
| 5 | `#jw-trial` | `trial` | `trial` | Optional |
| 5 | `#jw-tz` | `timezone` | `timezone` | **Required** |
| 5 | day rows | `availability_slots` | `availability_json` + `availability_meta` + derived `availability` | **Required (≥1 day, both times, end > start)** |
| 6 | `#jw-why` | `why` | `why` | Optional |
| 6 | `#jw-currency` | `currency` | `currency` | Optional |
| 6 | `#jw-contact-pref` | `contact_pref` | `contact_pref` | Optional |
| 6 | `#jw-referral` | `referral` | → `details_json` | Optional (documented overflow) |
| 7 | `#jw-consent-data` | top-level `consent` | `consent_terms` | **Required** |
| 7 | `#jw-consent-privacy` | server-inferred | `consent_privacy` | **Required** |
| — | derived | `years`+`levels` | `experience` | server-built |
| — | server | — | `reference`, `status`, `approved`, `timestamp`, `created_at`, `updated_at`, `schema_version`, `declaration`, `consent_at`, `email_status`, `email_sent_at`, review columns | server-owned |

No intended field is dropped. Anything with no column of its own (`referral` today) lands in `details_json` and is never lost.

## 5. Final column count and order — **69**

The first 17 are byte-identical and in their original positions: `timestamp, reference, status, approved, name, email, city, country, subject, experience, rate_usd, availability, bio, photo_link, video_link, languages, notes`.

Then 18–69, append-only: `display_name, state, contact_pref, intro,` **`whatsapp`** `, subjects_json, levels_json, methods_json, teach_langs_json, hindi_level, english_level, other_langs, years, online_years, less_exp, platforms, edu_qual, edu_inst, edu_year, edu_extra, certs, bed_detail, doc_refs, headline, why, video_thumb, sample_link, website, linkedin, profile_url, currency, duration, trial, timezone, availability_json, availability_meta, consent_privacy, consent_terms, declaration, consent_at, schema_version, created_at, updated_at, email_status, email_sent_at, review_notes, rejection_reason, reviewed_by, reviewed_at, previous_status, source, details_json`.

`whatsapp` is the **22nd name in the schema array** (1-based), inside the personal/contact group, exactly where the brief asked.

**Correction (added during verification — see `docs/audits/legacy/FINAL-VERIFICATION-REPORT.md` §1).** An earlier draft of this line said "column 22" without qualification, which conflates the *logical* schema position with the *physical* spreadsheet column. The two are only equal for one migration path:

| Tab state when `ekMigrateApplications` runs | Columns appended | Physical column of `whatsapp` |
|---|---|---|
| Still the legacy 17-column tab | 52, in schema order | **22** |
| Already at 2.0.0's 68 columns (**the realistic production case**) | 1 (`whatsapp`) | **69** |

In the production case physical column 22 remains `subjects_json`, and a pre-existing row's `whatsapp` cell is left empty. Nothing in `ApplicationIntake.gs` depends on either number: every read and write goes through the header map (`map[column]`), which was proved by physically dragging `whatsapp` to column 1 and still getting the value into the correct cell.

Migration was tested against a simulated live 68-column tab holding a real-looking approved row: one column appended at the end, all 68 headers unmoved, every cell byte-identical, legacy 17 untouched, row count unchanged, and a second run is a no-op.

## 6. WhatsApp field

- Label is exactly **"Personal WhatsApp Number (Optional)"** with an `optional` badge; blank never blocks Next or Submit and the key is omitted from the payload rather than sent empty.
- Stored in the private `whatsapp` column. `applications` is **not** a feed tab (the allow-list is `tutors, reviews, settings, support`), approval never writes `tutors`, and `whatsapp` is already in the feed's `FEED_PRIVATE_EXACT` list as a second line of defence.
- India and international are both supported; the country code is **never invented**: `98765 43210` → `9876543210`, `+91 98765 43210` → `+919876543210`, `+44 7700 900123` → `+447700900123`. 7–15 digits, refused below that with a clear sentence.
- **No WhatsApp message is ever sent by anything.** The only sender is `ekSendApplicationMail_` (email). `contact_pref: "WhatsApp"` is a stated preference, not consent.

## 7. Before / after

| Suite | Before | After |
|---|---|---|
| `tests/regression/test-join-wizard.mjs` | 81 | **97 ✓** |
| `tests/integration/test-application-backend.mjs` | 87 | **103 ✓** |
| `tests/integration/test-apps-script.mjs` | 31 | 31 ✓ |
| `tests/regression/test-runtime-qa.mjs` | 143 | 143 ✓ |
| `tests/integration/test-razorpay-api.mjs` | 30 | 30 ✓ |
| `tests/integration/test-payment-e2e.mjs` | 11 | 11 ✓ |
| `tests/integration/test-live-payment-contract.mjs` | 8 | 8 ✓ |
| `tests/regression/test-browser-qa.mjs` | 26 | 26 ✓ |
| `tests/integration/test-live-feed.js` | 69 | 69 ✓ |
| Schema drift | 0 | **0** (20 113 chars, generated = on-disk) |
| `npm test` | exit 0 | **exit 0**, zero FAIL lines |

Plus two purpose-built runs on the changed code: **Phase 7 = 100/100** (the 23 requested cases, all driven by real `.click()`/dispatched events) and **Phase 6 = 45/45**.

**Not tested in a real browser.** No browser binary, Playwright or Puppeteer exists in this environment, so there is no visual, contrast or mobile-viewport verification here. Everything above is jsdom + DOM events. Report section D from the earlier audit stays NOT TESTED.

## 8. Backend security fixes

| Item | Status |
|---|---|
| Honeypot before accepting an application | ✅ moved above the seam — a filled honeypot now writes no row and sends no mail |
| Rate limit before writing / emailing | ✅ `ekApplicationQuota_()` inside the seam — 30/hour, 200/day; 40 posts now stop at 30 with 30 rows |
| Public request cannot approve or publish | ✅ verified: forged `status`/`approved`/`reference`/`email_status` ignored, `tutors` untouched, only the acknowledgement email |
| Optional answers preserved on resubmission | ✅ merge-by-supplied-key; omitted survives, explicitly emptied clears |
| Idempotent retries | ✅ `submission_id` minted per attempt; three identical posts → one row, one email, same reference |
| Failed email never destroys the record | ✅ row saved, `received:failed` written, response says "may be delayed" |
| Safe retry of a failed transition email | ✅ opt-in `retry_mail: true` re-sends only the missing one; a second retry sends nothing |
| Health GET is read-only | ✅ `ekTab_(false)`; reports "no applications tab yet", creates nothing |
| `onOpen` collision | ✅ checked first: exactly one `onOpen` in the project, one `doGet` and one `doPost` in `Unified.gs` — nothing added or changed |
| Admin behind `EK_ADMIN_TOKEN` | ✅ unset / wrong / missing all refuse; right token accepted |

Bookings, reviews, sign-ups and contacts are untouched: a contact submission still works and its honeypot still stores nothing.

## 9. Legacy data protection

- Columns 1–17 keep their names, order and meaning — the dashboard formulas that count `applications!C:C` still point at `status`.
- Migration **appends only** and is idempotent; nothing is renumbered or rewritten.
- Resubmission no longer clears cells the new payload omits.
- No real spreadsheet, Script Property or deployment was touched at any point.

## 10. Remaining limitations

1. **No real-browser pass.** Keyboard-only traversal, focus-ring appearance, reduced motion, 360 px layout and contrast are still unverified in a browser.
2. **`referral` has no column** — it is preserved in `details_json` by design; promoting it to a column is a schema decision, not a bug.
3. **`consent_privacy` is server-inferred** from `consent`; the stored `yes` is not independent evidence of a separate tick. Fixing that means the browser sending it, which would change the request contract.
4. **The rate limiter is cache-based**, like the existing `intakeQuota_` — a cold cache resets it. It bounds a flood, it is not a defence against a distributed attacker.
5. **The quota counts retries**: a retry carrying the same `submission_id` is deduped before anything is written, but the counter still ticks once per POST.
6. `EKGURU_MAX_BYTES`, `EKGURU_DETAILS_MAX_KEYS` (count, not size) and `EK_MAIL_MAX_PER_RUN` remain unused — pre-existing, left alone deliberately.

### Defects found during verification — all four now fixed

Discovered while proving the work (`docs/audits/legacy/FINAL-VERIFICATION-REPORT.md` §1–§6), then fixed in a follow-up pass. Each has a permanent regression test.

7. **DEF-1 — a resubmission could overwrite three answers with their defaults.** `duration` (`50 min`), `currency` (`USD`) and `hindi_level` (`Native`) had no empty first option, so `buildPayload` sent a value for them on *every* submission, and `values.__supplied` marked them "answered now". **Fixed:** each select now opens on `<option value="">Select</option>` (with a `data-label` so the future error can name it), and the preview price no longer invents `/ 50 min` for an unpicked length. Wizard suite block 23/25; end-to-end proof in `docs/audits/legacy/FINAL-VERIFICATION-REPORT.md` §8.
8. **DEF-2 — `details_json` accepted the *names* of server-owned columns.** `status`/`approved`/`review_notes` sent in `fields` never moved their cells, but the applicant's text was filed under a reviewer-shaped key. **Fixed:** a name in `EKGURU_SERVER_ONLY` is diverted and recorded inertly as `sent_<name>`; genuine overflow (`referral`) is untouched. Backend suite block 30.
9. **DEF-3 — the review screen's preview header never rendered.** `js/join-wizard.js:848` looked for `[data-jw-pv-head]`, which `join.html` did not have, so the placeholders `Your name` / `City, country` / `?` stayed on screen. **Fixed:** the attribute is on `div.jw-preview-head`; the name, city/country, photo-or-initials now render. Wizard suite block 24.
10. **DEF-4 — `availability_meta`'s derived fallback was dead code.** The guard was `if (values.availability_meta == null)` but validation stores `""`, so it never fired. **Fixed** to `== null || === ""`; a client-supplied value is still respected. Backend suite block 31.

## 11. Migration and deployment steps (for later — not done here)

1. **Back up** the `applications` tab (File → Make a copy).
2. Apps Script editor: paste `apps-script/ApplicationSchema.gs` and `apps-script/ApplicationIntake.gs`, and re-paste `apps-script/Unified.gs` (the honeypot ordering change lives there).
3. Open the bound spreadsheet → menu **EkGuru → Migrate applications tab**. It should log `1 columns added` and `69/69 schema columns present`.
4. Verify `.../exec?action=ekHealth` → `"schema":"2.1.0"`, `"columns":{"expected":69,"present":69,"missing":[]}`.
5. **Deploy → Manage deployments → Edit → New version → Deploy.** Keep the same `/exec` URL.
6. Hard-refresh the site so `js/join-schema.js` is not served from cache; confirm the WhatsApp field appears on step 1.
7. Manual smoke test on the live page: tick a day → the time inputs must become usable; leave a consent box unticked and press Submit → an error must appear beside it, not silence.
8. If anything looks wrong, **Migrate** is idempotent and can be re-run; it never removes a column.

Do not run `tools/build-join-schema.mjs` casually — it has no `--check` mode and overwrites `js/join-schema.js`. The drift check regenerates into memory and diffs.

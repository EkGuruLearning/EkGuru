# EkGuru: handover for another AI or developer

Last updated: 2 Nov 2026. Read this whole file before changing anything.
This file holds no applicant contact details. Look those up in the sheet.

## 1. What this is

EkGuru is a static site on GitHub Pages (ekguru.shop). Pages are built by
`tools/*.py|js|mjs`. The live data (tutors, reviews, settings) comes from a
Google Sheet through an Apps Script feed. Applications, reviews and bookings
go in through Apps Script intake endpoints, or by email as a fallback.

- Repo: github.com/EkGuruLearning/EkGuru
- Branch in progress: `fix/live-sheet-tutors-en-in-legal` (PR #30). Do not
  merge until CI is green and the owner confirms the language-gate position.
- Sheet "EkGuru DB": id `1_GO1HVsmZyc-fXTnmZywjfxAyRfwp8qvVzCe6EvxkOc`
- Sender for mail: `ekgurulearning@gmail.com`. Keep this sender. The owner
  confirmed it on 2 Nov 2026.

## 2. Sheet tabs (EkGuru DB)

| Tab | Use | Notes |
|---|---|---|
| tutors | One row per tutor (A to AW). AX is a formula. | `approved` (AW) and `active` (B) decide "live". AX shows `live (approved=yes)` when both are yes. Do not type in AX. |
| applications | Join-form and email applications | Column D `approved`. Approving here does not publish; the tutor row does. |
| bookings | Booking requests, 20 columns | Full detail: lesson, price, level, goal, timezone, source, sent_via, email_delivery. Written by the `booking` intake kind. |
| reviews / reviews_pending | Reviews | Status `live` or `hidden`. |
| signups | Newsletter/sign-ups | |
| settings, content, support, url-inventory, README | Site settings and docs | |
| dashboard | COUNTIF totals | Reads applications!C/D, tutors!B/AW, reviews_pending!C, reviews!G, signups!C, bookings!H. Keep bookings status in column H. |
| applications-form-archive | Old Google Form responses | Personal data. Keep private. |
| EkGuru Payments Ledger | Payments | Separate sheet (id 1u5Jkbe...). Private. Owner decision. |

## 3. Current state (2 Nov 2026)

Done:
- Nine applications are marked approved (applications!D2:D10 = yes).
- Tutors live in the sheet (publish_check = live): sushila-g, hemlata,
  shikha-dutta, tara, sarshtee-baliyan, ashwani-yadav, anju-chauhan,
  prem-lata, sudhir-sharma, pinkal-badhan, rohit-seth.
- Four booking requests recorded in bookings (EK-TE3WYA, EK-D8QFW4,
  EK-SM7J7Y, EK-QZC64X). EK-QZC64X is a test. EK-D8QFW4 and EK-SM7J7Y may be tests.
- Nine approval emails are saved as Gmail drafts (not sent). Review and send.
- Homepage has a "Find a Hindi tutor" button. The phone currency notice
  sits at the bottom edge.
- Phone-width overflow check passes on index, find-tutors, courses, join,
  live-class, learn/hindi, and a tutor page.

Not done, and why:
- **The site does not show sheet tutors yet.** `js/site-config.js` `feed.url`
  is blank, so the site reads only its static tutor files. Live status in
  the sheet has no public effect until LiveFeed.gs is deployed (step 4.1).
- **Bookings do not reach the sheet yet.** `intake.url` is blank. The
  booking code path is ready (js/features.js calls `EkGuruIntake.submit("booking", ...)`
  when intake is on) but inactive (step 4.2).
- **Pinky Kumari (MAIL-01) is not live.** Her application has no price (she
  quoted ₹500 per 50 minutes) and no photos in the sheet. The draft asks her
  for both. Add her row when those arrive.
- **Tutor booking mail for sushila-g, hemlata and tara** still goes to the
  EkGuru inbox, because they have no notification_email. The owner must
  supply one. Applicants' emails are now in notification_email for the new
  rows.
- **Language gate** (data/quality/language-gate.json) is BLOCKED: needs
  native-speaker review and references. This is content work.
- **CI** fails on the `lang-topics` fingerprint (314 stale Indian-language
  topic pages). The fix needs the owner's decision on the v158 design block,
  then a regeneration in this order: strip ultra head, generate, re-apply
  ultra, shell, inject ads. Do not run build-lang-topics.py without the
  strip step: it dropped the ultra head and data-ad-class on 314 pages.

## 4. Steps the owner must do (cannot be done from the repo)

4.1 Deploy the live feed
  1. In Apps Script (script.google.com, logged in as ekgurulearning@gmail.com),
     create a new project and paste `apps-script/LiveFeed.gs`.
  2. Deploy as a web app: Execute as Me, access Anyone. Copy the /exec URL.
  3. Paste it into `js/site-config.js` at `feed.url`. The URL must look like
     `https://script.google.com/macros/s/<id>/exec`.
  4. Steps in `apps-script/LIVE-FEED-SETUP.md`.
  5. Check: `curl "<url>?action=health"` returns JSON. Then reload the
     homepage. The tutor cards should match the sheet.

4.2 Deploy the intake (applications, reviews, sign-ups, bookings)
  1. Create a SECOND Apps Script project. Paste `apps-script/Intake.gs`.
     Deploy: Execute as Me, access Anyone.
  2. Paste the /exec URL into `js/site-config.js` at `intake.url`.
  3. Steps in `apps-script/INTAKE-SETUP.md`.
  4. Check: the join form sends an application; a row appears in the
     `applications` tab as `pending`. A booking appears in `bookings` with
     status `requested`.

4.3 Set notification addresses. Put each tutor's booking address in tutors
   column Z (notification_email): sushila-g, hemlata, tara.

## 5. Rules that must not be broken

- Never publish applicant personal data (email, WhatsApp, phone, the
  applicant's login email). Keep it in private tabs. Use it only to contact
  the applicant.
- New pages are noindex, by owner freeze (tools/ultra/contract.py).
- Ad policy: data/monetization/google-monetization.json; run
  `node tools/test-ad-policy.mjs`.
- Indian English: `python3 tools/indian-english.py --check` must report 0.
  Fix with `--apply`.
- Booking emails use the sender `ekgurulearning@gmail.com`.
- Do not claim a profile is "live on the site" to an applicant until step 4.1
  is done and the card shows on ekguru.shop.
- The owner's gate `approved = yes` stays in force. Do not set it on a
  tutor the owner has not approved.

## 6. Checks to run before any push

```
python3 tools/build-all.py check        # master check; see CI for the expected failures above
node tools/test-ad-policy.mjs
node tools/test-intake.js
python3 tools/indian-english.py --check
node --check js/features.js && node --check js/intake.js
```

Known failing: `lang-topics` fingerprint (section 3).

## 7. Where things are

- Tutor cards and the booking form: `js/features.js`, `js/main.js`,
  `js/sheet.js` (feed reader; rejects a non-/exec URL).
- Mail: `js/mailer.js` (providers: Apps Script relay, then Web3Forms,
  EmailJS, StaticForms, FormSubmit; quota fallback per month).
- Intake client: `js/intake.js`. Server: `apps-script/Intake.gs`.
- Feed server: `apps-script/LiveFeed.gs`.
- Site config: `js/site-config.js`.
- Tutor static files: `js/tutors/*.js` (sushila-g, hemlata, shikha-dutta,
  tara, sarshtee-baliyan).

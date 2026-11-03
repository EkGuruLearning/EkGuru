# EkGuru online forms: set-up

The Join page now has an **Apply online** form. A visitor can also send a
**review** or a **learner sign-up** through the same script. Everything sent
arrives as a **pending** row in your sheet. Nothing goes live until you approve it.

Until you do the set-up below, the form still works the way it did before: it
opens an email to EkGuruLearning@gmail.com. Nothing breaks.

## Before you start

Use a **new, separate** Apps Script project. Do not paste this into the
payments project or the questions project. Each project has its own `doPost`,
and mixing them causes errors and risk.

## Steps (about ten minutes)

1. Open the **EkGuru DB** sheet (the workbook that already has the
   `bookings`, `tutors` and `reviews` tabs).
2. In that sheet click **Extensions → Apps Script**. This opens a project
   *bound* to the workbook — that binding is what lets a submission become
   a sheet row. Name the project `EkGuru Intake`.
3. Delete the sample code. Paste the whole of `apps-script/Intake.gs` into
   `Code.gs`. Click **Save**.

   ⚠️ **Do NOT create the project from https://script.google.com instead.**
   A standalone project is not connected to any workbook: v1.0.0 of the
   script then failed every submission, which is exactly how bookings
   could be "sent" and still never appear in the sheet. If you must use a
   standalone project, open **Project Settings → Script Properties** and add
   `EKGURU_DB_SPREADSHEET_ID` = the id from the EkGuru DB sheet URL
   (`docs.google.com/spreadsheets/d/<this part>/edit`). The script uses
   that property only when no workbook is bound; no id is hard-coded.

   Tabs are created the first time a form is sent, if they are missing:
   `applications`, `reviews_pending`, `signups`, `bookings`. A tab that
   already exists (like `bookings`) is used as-is; an existing but empty
   tab gets its header row written before the first booking.
4. Click **Deploy**, then **New deployment**, then the gear icon, then **Web app**.
   - **Execute as:** Me
   - **Who has access:** Anyone
5. Click **Deploy** and allow the permissions it asks for. The script only needs
   to read and write its own sheet.
6. Copy the **Web app URL** (it ends in `/exec`).
7. Open `js/site-config.js` and set:

   ```js
   intake: {
     url: "https://script.google.com/macros/s/AKfycb.../exec"
   },
   ```

8. Commit and let GitHub Pages deploy.

## Check it

Open `https://script.google.com/macros/s/.../exec?action=health` in a browser.
You should see `"ok": true`, `"spreadsheetBound": true`, `"version": "1.1.0"`
and the pending counts. It shows counts only. If you instead see
`"spreadsheetBound": false`, the project is not connected to the workbook
(step 1–2 above, or the script property) and **no form will save** until
that is fixed — redeploy after fixing it.

Then send one test application from the Join page, using your own details, and
check that a row with status `pending` appears in `applications`. Delete the test
row afterwards.

**Then verify a booking (the important one):** open Find Tutors, book any
tutor with your own name/email, and check that exactly one new row with
status `requested` and your `booking_ref` appears in the `bookings` tab.
Sending the same booking again does not create a second row — the script
answers `duplicate: true` for the same `booking_ref`. Delete the test row
afterwards.

## Approving someone

**A tutor application** (tab `applications`):
1. Read the row. Check the person, their identity, documents and consent.
2. If they are approved, add them to the **tutors** tab (copy the row's name,
   subject, rate, bio, photo link and availability into a new row), set
   `approved` to `yes` and `active` to `yes`. Their profile appears on the site
   within seconds, through the live feed.
3. Set the `status` cell in `applications` to `approved` (or `declined`). This
   keeps your record. Do not delete it unless they ask you to.

**A review** (tab `reviews_pending`):
1. Check it is from a real lesson. If it is genuine, copy the row into the
   **reviews** tab. Set `status` to `live`.
2. Set `status` in `reviews_pending` to `published`.

**A learner sign-up** (tab `signups`): private. Use it only to reply to the
person. Do not publish it.

## What the script will never do

- It never writes to the public tabs (tutors, reviews, settings, support).
- It never returns what a visitor typed, only a short reference such as `EG-K3Q9AP`.
- It never stores an IP address, a browser id or a cookie.
- It refuses a submission without consent, with the honeypot filled, or with a
  bad email, link, number or option. It caps sends at 30 an hour and 150 a day
  for each kind, for the whole site.

## Limits to know about

- Anyone can still send junk up to the caps. Look at the pending tabs about once
  a week and delete junk rows.
- There is no per-person limit. Apps Script cannot see an address.
- A deleted row can still exist in the sheet's version history, and in any email
  you already received. If someone asks you to delete their data, delete the
  row, and clear the version history if you want the copy gone.

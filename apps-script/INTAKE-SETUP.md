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

1. Open https://script.google.com and click **New project**. Name it
   `EkGuru Intake`.
2. Delete the sample code. Paste the whole of `apps-script/Intake.gs` into
   `Code.gs`. Click **Save**.
3. Open the sheet you want the rows in (it can be the EkGuru DB sheet, or a new
   one). Its tabs are created the first time a form is sent: `applications`,
   `reviews_pending`, `signups`. **To keep the forms and the live feed in one
   place, bind this project to the EkGuru DB sheet** by opening that sheet, then
   Extensions, Apps Script, and pasting the file there instead. Only do one of
   the two, not both.
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
You should see `"ok": true` and the pending counts. It shows counts only.

Then send one test application from the Join page, using your own details, and
check that a row with status `pending` appears in `applications`. Delete the test
row afterwards.

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

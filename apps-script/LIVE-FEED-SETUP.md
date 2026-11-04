> **RECOMMENDED NOW: the unified file.** `apps-script/Unified.gs` serves this feed AND the intake from one project with one URL — same behaviour, half the maintaining. Follow `apps-script/UNIFIED-SETUP.md` instead. This page stays for the standalone feed file.

# EkGuru live feed: set-up in five minutes

This makes a change in the **EkGuru DB** sheet show on ekguru.shop within a few
seconds, instead of after Google's own delay of about five minutes.

You do this once. Until you do, nothing breaks: the site keeps reading the
published CSV links exactly as it does today.

## Why it is needed

"Publish to web" links are cached by Google for about five minutes. The site
cannot shorten that from the browser. The live feed is a small read-only
script that lives inside your sheet, reads the cells directly, and tells the
site what they say right now.

- It only **reads**. It cannot change a single cell.
- It sends only the public tabs: `tutors`, `reviews`, `settings`, `support`.
- It removes private columns before anything leaves Google: `email`,
  `notification_email`, `formKey`, `whatsapp`, and any column whose name looks
  like a phone, mobile, password, token, bank, UPI or card field. This is done
  inside the script, so a mistake in the sheet cannot publish an address.
- It removes help rows (a row whose first cell starts with `#`) and blank rows.
- Its cache lasts 30 seconds and is cleared the moment the sheet is edited.

## Steps

1. Open the **EkGuru DB** sheet (the tutors, reviews, settings workbook).
2. Click **Extensions**, then **Apps Script**.
3. Delete the sample code. Create a file called `LiveFeed` and paste the whole
   of `apps-script/LiveFeed.gs` from this repository into it. Click **Save**.
4. Click **Deploy**, then **New deployment**. Click the gear icon and choose
   **Web app**.
   - **Execute as:** Me
   - **Who has access:** Anyone
5. Click **Deploy**. Google asks you to authorise the script. Choose your
   account, then **Advanced**, then **Go to EkGuru (unsafe)**, then **Allow**.
   The warning appears because the script is new and unreviewed by Google. It
   asks only to read the spreadsheet it lives in.
6. Copy the **Web app URL**. It ends in `/exec`.
7. In the editor, choose the function `installTriggers` and click **Run** once.
   This makes pasted imports and inserted rows clear the cache as well.
8. Open `js/site-config.js` and paste the URL:

   ```js
   feed: {
     url: "https://script.google.com/macros/s/AKfycb.../exec",
     cacheSeconds: 30
   },
   ```

9. Commit, merge and let GitHub Pages deploy.

## Check that it works

Open this address in a browser, with your own URL in place of the dots:

    https://script.google.com/macros/s/.../exec?tab=health

You should see a short block of figures: how many rows each tab has, how many
private columns were removed, and for the tutors tab how many rows say
`approved=yes`. It never shows cell contents. If `found` is `false` for a tab,
its name was changed. The script also finds a tab by its permanent number, so
the site keeps working, but rename it back when you can.

Then open `...exec?tab=tutors`. You should see the tutors CSV with **no** email,
phone, `formKey` or `whatsapp` column. If you see any of those, stop and tell
us: the feed must not be used until that is fixed.

## Changing the script later

When you change the script, choose **Deploy**, **Manage deployments**, the
pencil icon, **Version: New version**, **Deploy**. The URL stays the same. If
you make a **New deployment** instead, the URL changes and `feed.url` must be
updated.

## If something looks wrong

| What you see | What it means | What to do |
|---|---|---|
| The site shows old data after an edit | The feed is off or the URL is wrong. The site fell back to the published CSV | Check `feed.url`, then open `?tab=health` |
| `?tab=health` asks you to sign in | **Who has access** is not **Anyone** | Deploy a new version with access set to **Anyone** |
| A tab shows `found: false` | The tab was renamed | Rename it back: `tutors`, `reviews`, `settings`, `support` |
| A new guru does not appear | `approved` is not `yes`, `active` is `no`, there is no real photo, or the id has capitals or spaces | Open the browser console on ekguru.shop. It names the row and the reason |

## What this feed must never contain

Never paste the **payments** workbook id or any Razorpay key into this file.
The payments backend (`apps-script/Code.gs`) is a separate project on purpose,
and the feed reads only the workbook it is attached to.

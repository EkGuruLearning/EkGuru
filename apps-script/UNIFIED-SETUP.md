# EkGuru unified backend: set-up in ten minutes (RECOMMENDED)

One file, one deployment, one URL — for **both** the live feed (sheet →
site, read-only) and the intake (site → sheet, pending rows only).

- Paste `apps-script/Unified.gs` into **one** Apps Script project bound to
  the **EkGuru DB** sheet.
- Paste the **same** `/exec` URL into `js/site-config.js` twice: `feed.url`
  **and** `intake.url`.
- Behaviour is identical to `LiveFeed.gs` v1.0.0 + `Intake.gs` v1.2.0 —
  `tools/test-live-feed.js` proves it on every run.

The two separate files (`LiveFeed.gs`, `Intake.gs`) still work and are
still in this folder. Use the unified file unless you have a reason not
to: one project to maintain, one URL that can never go half-stale.

## If your editor shows a red syntax error right now

That happens when the feed and the intake were pasted into one file by
hand: the file ends up with **two** `doGet` functions (Apps Script keeps
only the last one, so one half silently dies) and the torn comment
between the two halves is itself a syntax error (`Unexpected token '*'`).

Fix, in this order:

1. Select **all** the code in the editor (`Ctrl+A`) and delete it.
2. Paste the **whole** of `apps-script/Unified.gs` — first line to last
   line, nothing skipped. Click **Save**. The red error must disappear;
   if it does not, you pasted only half the file — repeat step 1.
3. Continue below. Do **not** paste anything else into this project.

## Steps

1. Open the **EkGuru DB** sheet (the tutors/reviews/settings/bookings
   workbook) → **Extensions → Apps Script**. The project **must** open
   from that sheet (a *bound* project). Name it `EkGuru Unified`.
   - ⚠️ Do **NOT** use the payments project (the one whose Code.gs talks
     about Razorpay) or the questions project. Each backend is its own
     project; mixing them breaks both.
   - ⚠️ Do **NOT** create the project from script.google.com instead,
     unless you also do step 6. A standalone project sees no workbook
     and every submission fails.
2. Delete the sample code. Paste the whole of
   `apps-script/Unified.gs` into `Code.gs`. Click **Save** — no red
   error may remain.
3. In the toolbar, choose the function `selfTest_` and click **Run**.
   Authorise when asked. The log (View → Logs) shows every feed tab
   found with its row count, plus intake health. Fix what it names
   **before** deploying.
4. **Deploy → New deployment** → gear icon → **Web app**.
   - **Execute as:** Me
   - **Who has access:** Anyone
5. Click **Deploy**, allow the permissions. Copy the **Web app URL**
   (ends in `/exec`).
6. Standalone projects **only**: Project Settings → Script Properties →
   add `EKGURU_DB_SPREADSHEET_ID` = the id in the EkGuru DB sheet URL
   (`docs.google.com/spreadsheets/d/<this part>/edit`). Bound projects
   skip this.
7. In the editor, run `installTriggers` once, so pasted imports and
   inserted rows also clear the 30-second feed cache.
8. Open `js/site-config.js` and paste the **same** URL twice:

   ```js
   feed: {
     url: "https://script.google.com/macros/s/AKfycb.../exec",
     cacheSeconds: 30
   },
   intake: {
     url: "https://script.google.com/macros/s/AKfycb.../exec"
   },
   ```

9. Commit, merge, let GitHub Pages deploy.

## Check that it works

Open these in a browser (your URL in place of the dots):

| Address | Must show |
|---|---|
| `.../exec?tab=health` | `"ok": true`, per-tab row counts, `privateColumnsRemoved`. Counts only — never cell contents |
| `.../exec?tab=tutors` | Tutors CSV with **no** `email`, `notification_email`, `formKey`, `whatsapp` or phone column. If any appears: stop, do not use the feed |
| `.../exec?action=health` | `"ok": true`, `"version": "1.2.0"`, `"spreadsheetBound": true`, pending counts |
| `.../exec` (bare) | Combined health: `"unified": "2.0.0"` plus a `feed` and an `intake` block |

Then send one test booking from Find Tutors with your own details and
check that exactly one row (`requested`, your `booking_ref`) appears in
`bookings`. Send it again: no second row (`duplicate: true`). Delete the
test row afterwards. Then send one test review quoting that booking
reference: without it the review is refused (the genuine-review gate).

## Updating later (URL must not change)

1. Paste the new `Unified.gs` over the old file, **Save**.
2. **Deploy → Manage deployments → ✏️ Edit** (the existing deployment)
   → **Version: New version → Deploy**. Never “New deployment” — that
   mints a different URL and both `feed.url` and `intake.url` go stale.
3. Re-open `?action=health` and the bare URL; confirm the versions.

## Future options (the EK_ block, top of the file)

Every option is a flag, not new code. Flip it, save, redeploy the
**same** deployment. All are off unless the table says otherwise.

| Flag | What it does |
|---|---|
| `maintenance` | Whole backend answers “in maintenance”. The site falls back to published tabs; forms show their offline path |
| `jsonFormat` (default ON) | `?tab=tutors&format=json` answers `{header, rows}` — same cells, same stripping. Purely additive |
| `adminPing` | `?action=ping&token=…` answers `pong` for dashboards/monitors. Needs the `EK_ADMIN_TOKEN` script property; without it every ping is refused as “unknown action” |
| `auditLog` + `auditTab` | Every accepted submission also appends `{at, kind, reference, tutor}` to `audit_log`. Never changes the visitor's answer |
| `digest` + `digestTab` | `dailyDigest_()` appends one pending-counts row a day to `digest_log`. Needs a daily time trigger on that function too. Sends no email, ever |
| `combinedHealth` (default ON) | Bare `/exec` answers feed+intake health together |

## If something looks wrong

| What you see | What it means | What to do |
|---|---|---|
| Red error in the editor | Half-pasted file, or two backends in one project | Delete all, paste the whole file again; keep payments/questions separate |
| `?action=health` says `spreadsheetBound: false` | Project not bound, no script property | Redo steps 1–2 or step 6, then redeploy (New version) |
| `?tab=health` asks you to sign in | **Who has access** is not **Anyone** | Redeploy a new version with access **Anyone** |
| A tab shows `found: false` | The tab was renamed | Rename it back: `tutors`, `reviews`, `settings`, `support` |
| The site shows old data after an edit | Feed off / wrong URL — the site fell back to published output | Check `feed.url`, then open `?tab=health` |
| A booking “sends” but no row appears | Intake URL stale or unbound | Check `intake.url` equals the deployed URL, then `?action=health` |

## What this file must never contain

Never paste the **payments** workbook id or any Razorpay key here, and
never paste this file into the payments project. The payments backend
(`apps-script/Code.gs`) stays a separate project on purpose.

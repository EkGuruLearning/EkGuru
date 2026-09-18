# Adding a tutor to EkGuru

Six places decide whether a tutor exists. This is the whole list, in order,
and every one of them is now written by a tool — the only file a human writes
is the tutor's own.

| # | What | Where | Written by |
|---|---|---|---|
| 1 | the tutor's data | `js/tutors/<id>.js` | **you** (copy `js/tutors/sarshtee-baliyan.js`) |
| 2 | who exists | `js/tutors/_registry.js` | you: one line, `"<id>",` |
| 3 | the `<script>` tags | every page that loads the registry | `node tools/langsync.js` |
| 4 | the profile page | `tutor/<id>/index.html`<br>+ `sitemap-tutors.xml`, `sitemap.xml`, `feed.xml` | `node tools/build-tutor-pages.js` |
| 5 | the cards on the home pages | `index.html`, `es/ fr/ de/ pt/ ja/ ar/` | `node tools/build-home-tutors.js`<br>`node tools/build-market-pages.js` |
| 6 | the long-tail lists | 37 `hindi-tutor/*` pages, `tutor/index.html`, the six `*/find-tutors.html` | `node tools/build-roster-rows.js` |
| 7 | the sheet row | `csv/ekguru_tutors.csv`, plus the private paste copy | you, then `python3 tools/make-tutor-row.py` |

Then the spreadsheet row (below) and one commit.

```bash
# after steps 1 and 2, from the repo root:
node tools/langsync.js                 # 3 — the script tags, all 23 pages
node tools/build-tutor-pages.js        # 4 — their page, sitemaps, feed
node tools/build-home-tutors.js        # 5 — the English home page cards
node tools/build-market-pages.js       # 5 — the six translated home pages
node tools/build-roster-rows.js        # 6 — every other page that lists tutors

python3 tools/make-tutor-row.py <id> --email their@address   # 7 — the sheet row

# every one of them takes --check and exits 1 if a file is out of date:
python3 tools/build-all.py check       # all eight layers, plus the DOM test
```

Step 6 is the one that used to be forgotten because the lists were hand-written:
44 pages carried four tutors while the registry held five, and three of them
quoted a price the `data-usd` next to it contradicted. The tool rewrites only
the run of tutor blocks and keeps each page's own prose, headings and relative
paths; `--check` fails while any of those pages is behind.

`node tools/langsync.js --check` is the one to run in CI. Forgetting it is the
mistake that hid Shikha Dutta from all six translated pages.

---

## The spreadsheet row

`csv/ekguru_tutors.csv` is the schema-exact upload pack (48 columns, header
row + `#help` row included). A new tutor is one more row with the same 48
cells in the same order — see `csv/README.md` for the column table.

`csv/sarshtee-baliyan-row.local.csv` is a ready-to-paste copy of the row for
Sarshtee Baliyan: header, the sheet's own `#help` row, then her row. Import it
into the tutors tab (File → Import → *Insert new rows*) or copy the last line
and paste it below the existing tutors. Rebuild it whenever it is missing or
her address changes:

```bash
python3 tools/make-tutor-row.py sarshtee-baliyan --email her@example.com
```

**It is not committed, and it is regenerated, not hand-edited.** The
repository is public, and her personal address
belongs in the spreadsheet, not in Git — that is exactly why `tools/sheetsync.js`
refuses to write emails into `js/tutors/_overrides.js`, and why `js/sheet.js`
keeps `email` separate from `notification_email`. `.gitignore` covers
`*.local.csv` for this reason.

### What each of her cells says, and why

| Column | Value | Note |
|---|---|---|
| `id` | `sarshtee-baliyan` | ⛔ never change it after this: it is her URL |
| `active` | `yes` | `no` hides her everywhere, without deleting anything |
| `priceUSD` | `8` | she quoted **$8–10 to start**; the site shows one number, so this is her starting price — change this cell when she settles on a rate |
| `availability` | `Mon-Sat 17:00,18:00,19:00,20:00` | lesson **start** times, 24-hour, each lesson 50 min. Her window is 5–9 PM IST, so the last lesson starts at 20:00 and ends 20:50 |
| `video` | *(blank)* | no intro video yet. Paste the 11-character YouTube id when she records one |
| `verified` / `superTutor` | `no` / `no` | both are earned: `verified` after her documents are checked, `superTutor` only with the record to support it |
| `notification_email` | her address | the canonical operational inbox — every booking request is delivered there. **Not published on any page** |
| `email` | *(blank)* | the legacy column. Blank is correct: it is the one that would print her address on a public page |
| `formKey` | *(blank)* | optional FormSubmit alias (no `@`); only needed if she wants a public address that is not hers |
| `photo` / `thumb` | *(blank)* | blank keeps whatever her tutor file has, which is the placeholder until she sends a photo. When it arrives: save it as `images/sarshtee-baliyan.jpg`, then set both cells (or the two lines in her tutor file) to that path |
| `trialMinutes` | *(blank)* | she offers a trial; the length is not fixed yet. `30` would say "a free 30-minute trial" |
| `about` | 3 paragraphs | one paragraph per line (alt+enter inside the cell) |
| `experience` | 5 lines | one bullet per line |
| `methodology` | 4 lines | `Title \| description`, one per line |

### Email, phone, and what is deliberately absent

* Her **email** is in the sheet's `notification_email` column only. Booking
  mail reaches her from there; the public page shows the EkGuru contact address.
  One-time step: open `tools/mail-activate.html`, press the button on her row,
  and ask her to click **Activate Form** in the mail that arrives.
* Her **WhatsApp number is not published anywhere.** `js/tutors-data.js` strips
  personal numbers from every tutor object as a hard rule, with one escape
  hatch: `allowPhone: true` in the tutor's own file, and only with her written
  consent and a *business* number. The spreadsheet has no `whatsapp` column for
  the same reason. If she wants WhatsApp buttons on her profile, get that in
  writing first.

---

## Check it worked

```bash
python3 tools/build-all.py check          # everything below, in one command:
#   langsync / build-tutor-pages / build-home-tutors / build-market-pages /
#   build-roster-rows --check, the CSS bundle, the emblems, the course hub,
#   and tools/test-experience-dom.mjs (needs: npm i jsdom)
```

Then look at `https://ekguru.shop/tutor/sarshtee-baliyan/` (a hard refresh —
`sw.js` caches pages) and at the home page, where her card should sit last in
the grid until you move her line up in `js/tutors/_registry.js`.

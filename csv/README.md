# EkGuru — Fresh CSV Upload Pack

These six CSVs are the **clean, schema-exact** data files to re-upload into a
**new** Google Sheets workbook. They were exported from the live production
data on 11 Sep 2026 **before** the old public CSV links were removed from the
site. Every header matches the repository's actual loader schema — nothing was
renamed or invented.

> The site's sheet links are currently **PAUSED_FOR_REUPLOAD**. Upload these,
> publish the new tabs, and hand the new published CSV URLs back so they can be
> wired in (see step 6).

## The files

| File | Tab name (suggested) | Columns | Rows |
|---|---|---|---|
| `ekguru_settings.csv` | settings | `key, value, what it does` | 8 keys |
| `ekguru_content.csv` | content | `slug, question, answer, body, keywords, related, status` | 29 (28 live + 1 draft example) |
| `ekguru_reviews.csv` | reviews | `tutor, name, date, stars, text, source, status` | 3 live reviews |
| `ekguru_tutors.csv` | tutors | 48 columns (see below) | 5 tutors + 1 `#help` row |
| `ekguru_github_urls.csv` | github_urls | URL crawl inventory (18 cols) | 555 |
| `ekguru_urls.csv` | urls | site URL inventory (17 cols) | 548 |

## Tutors columns — canonical schema

`id, active, name, nickname, subject, priceUSD, lessonLength, availability,
video, headline, city, country, timezone, teaches, tags, levels, speaks,
trialAvailable, experienceYears, verified, superTutor, rating, reviewsCount,
lessonsCount, email, notification_email, formKey, calLink, preplyUrl, holiday,
holidayUntil, holidayNote, specialities, badge, trialMinutes, packageDiscount,
responseHours, intro, exams, photo, thumb, banner, videoTitle, countryFlag,
about, experience, methodology, bio`

### The operational email field (`notification_email`)

- **`notification_email` is the canonical operational inbox** for a tutor's
  booking mail. Fill it with a real, verified address the tutor owns.
- **`email` is the legacy field** — keep it **blank** so no private address is
  ever published on a public tutor page. (`email` values are blank in this pack.)
- **`formKey`** remains supported as a hidden FormSubmit alias (no `@` symbol).
- Resolution order used by the site: `notification_email` → `formKey` → `email`
  → EkGuru inbox. A tutor with none of the first three is reported honestly as
  `TUTOR_EMAIL_UNAVAILABLE` (the student and the internal record still send).

### `videoTitle` — one short line only

The intro-video caption (`videoTitle`) must be a **single line, no `|`
character, 90 characters or fewer**. The loader deliberately refuses anything
else (a pasted methodology block is the common mistake — tara's production row
currently has one, so it is ignored on purpose). Fix it in the new sheet to
make the caption appear.

### Adding a tutor

A new tutor is one more row with the same 48 cells. `csv/ekguru_tutors.csv`
carries Sarshtee Baliyan's row; the paste-ready copy of it, including her
`notification_email`, is kept out of Git on purpose (`.gitignore` → `*.local.csv`)
because this repository is public. See `docs/ADD-A-TUTOR.md` for the whole
procedure and for what each of her cells means.

Regenerate that private copy at any time — it is a derived file, nothing is
lost if it goes away:

```bash
# just the one tutor: header + the sheet's #help row + their row
#   → Import ▸ Insert new sheet(s), then copy the row into the tutors tab
python3 tools/make-tutor-row.py sarshtee-baliyan --email her@example.com

# the whole tutors tab, every row, in sheet order
#   → select A1 in the tutors tab ▸ Import ▸ Replace data at selected cell
python3 tools/make-tutor-row.py sarshtee-baliyan --email her@example.com --full
```

`--full` is built from `live-sheets/tutors.csv` — the copy of the owner's
current tab — not from this pack. That matters: the pack is a fresh-workbook
file, and two of its cells disagree with the live tab (`hemlata` and `tara` are
`active=no` live, and tara's production `videoTitle` still holds the pasted
methodology block the loader refuses). Replacing a live tab with the pack would
silently un-hide two tutors; `--full` adds only the new row.

Before importing, prove the file behaves — the same test the build runs, with
the file itself as the source of the expectations:

```bash
EKGURU_TEST_CSV=csv/ekguru_tutors.local.csv node tools/test-sheet-apply.js
```

### Rules that already hold (do not fight them)

- Blank cell = **keep the current value**, never "erase". The word `none`
  clears a field where that is supported.
- `active: no` hides a tutor from the site.
- A phone number in `whatsapp` is ignored on purpose — personal numbers are
  never published.

## Upload steps

1. Create a **new** Google Sheets workbook (File → New → Spreadsheet).
2. One tab per file. File → Import → **Upload** → select the CSV → **Replace
   data at selected cell** with `A1` selected (never "Replace spreadsheet" —
   that replaces every tab in the workbook).
3. Rename each tab to the name in the table above.
4. For each tab: File → Share → **Publish to web** → choose that tab →
   **Comma-separated values (.csv)** → Publish.
5. Copy each tab's published URL (ends in `?output=csv`).
6. Send the six URLs back — they will be wired into `js/site-config.js`
   (`sheet.csvUrl`, `reviews.csvUrl`, `settings.csvUrl`, `content.csvUrl`),
   and the site flips from `PAUSED_FOR_REUPLOAD` back to live.

> Do not paste any of these CSVs back over the old published workbook until the
> new links are wired — the old links are intentionally disconnected now.

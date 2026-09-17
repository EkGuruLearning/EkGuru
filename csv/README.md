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
| `ekguru_tutors.csv` | tutors | 48 columns (see below) | 4 tutors + 1 `#help` row |
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

### Rules that already hold (do not fight them)

- Blank cell = **keep the current value**, never "erase". The word `none`
  clears a field where that is supported.
- `active: no` hides a tutor from the site.
- A phone number in `whatsapp` is ignored on purpose — personal numbers are
  never published.

## Upload steps

1. Create a **new** Google Sheets workbook (File → New → Spreadsheet).
2. One tab per file. File → Import → **Upload** → select the CSV →
   **Replace current sheet** (never "Replace spreadsheet" — that changes the
   tab's gid and breaks links).
3. Rename each tab to the name in the table above.
4. For each tab: File → Share → **Publish to web** → choose that tab →
   **Comma-separated values (.csv)** → Publish.
5. Copy each tab's published URL (ends in `?output=csv`).
6. Send the six URLs back — they will be wired into `js/site-config.js`
   (`sheet.csvUrl`, `reviews.csvUrl`, `settings.csvUrl`, `content.csvUrl`),
   and the site flips from `PAUSED_FOR_REUPLOAD` back to live.

> Do not paste any of these CSVs back over the old published workbook until the
> new links are wired — the old links are intentionally disconnected now.

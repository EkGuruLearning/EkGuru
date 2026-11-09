# EkGuru DB — table format and preservation record

**Updated:** 3 November 2026
**Workbook:** `EkGuru DB`
**Scope:** The 12 owner-requested tabs; this document contains headers and table metadata only, not applicant contact details.

## Outcome

Structured Google Sheets table metadata is now present on **11 of the 12 requested tabs**. Existing cell contents and formulas were not rewritten, moved, sorted, cleared, or deleted. Table definitions were added around the existing cells, with no per-column type conversions requested. Google Sheets retained the existing dropdown rules on `tutors.active` and `tutors.approved`, and the `DATE` type on `reviews.date`; other table columns remain untyped (`null`/existing General cell formats).

`applications` remains the one blocker: metadata verification confirms its existing basic filter is still present on `A1:Q102`, overlapping the intended table range. The earlier clear attempt returned `No grid with id: 0`; the follow-up metadata confirms that it did not remove the filter. This connector exposes setting/updating a basic filter but no valid clear operation, so I did not retry or change the filter range. No data or formulas were touched. The owner must remove the filter (or enable the Sheets `clearBasicFilter` operation), after which `tbl_applications` can be added over `applications!A1:Q8`.

The separate `applications-form-archive` table and hidden `EkGuru Payments Ledger` were not changed.

## Exact table definitions

The table range includes the header row. Ranges are from the current non-empty extent at the time of this update. Existing header spelling and column order are preserved exactly.

| Tab | Table name | Range | Table rows | Table column names (left to right) |
|---|---|---:|---:|---|
| `tutors` | `tbl_tutors` | `A1:AX14` | 14 incl. header | `id, active, name, nickname, subject, priceUSD, lessonLength, availability, video, headline, city, country, timezone, teaches, tags, levels, speaks, trialAvailable, experienceYears, verified, superTutor, rating, reviewsCount, lessonsCount, email, notification_email, formKey, calLink, preplyUrl, holiday, holidayUntil, holidayNote, specialities, badge, trialMinutes, packageDiscount, responseHours, intro, exams, photo, thumb, banner, videoTitle, countryFlag, about, experience, methodology, bio, approved, publish_check` |
| `applications` | **not created** | proposed `A1:Q8` | 8 incl. header | `timestamp, reference, status, approved, name, email, city, country, subject, experience, rate_usd, availability, bio, photo_link, video_link, languages, notes` |
| `bookings` | `tbl_bookings` | `A1:T5` | 5 incl. header | `booking_ref, requested_at, tutor_id, student_name, student_email, student_whatsapp, preferred_times_ist, status, confirmed_time_ist, tutor_reply_at, notes, lesson, price_usd, student_level, student_goal, student_timezone, source_page, tutor_email, sent_via, email_delivery` |
| `reviews` | `tbl_reviews` | `A1:G5` | 5 incl. header | `tutor, name, date, stars, text, source, status` |
| `reviews_pending` | `tbl_reviews_pending` | `A1:J1` | header only | `timestamp, reference, status, tutor_id, reviewer_name, stars, text, lesson_date, contact_email, notes` |
| `signups` | `tbl_signups` | `A1:I1` | header only | `timestamp, reference, status, name, email, goal, level, source, notes` |
| `settings` | `tbl_settings` | `A1:C10` | 10 incl. header | `key, value, what it does` |
| `support` | `tbl_support` | `A1:B11` | 11 incl. header | `key, value` |
| `content` | `tbl_content` | `A1:F31` | 31 incl. header | `slug, question, answer, body, keywords, related` |
| `url-inventory` | `tbl_url_inventory` | `A1:R556` | 556 incl. header | `URL, REDIRECTS_TO, TYPE, LANG, STATUS, CANONICAL, ROBOTS, INDEXABLE, TITLE, DESCRIPTION, H1, WORDS, INBOUND, ORPHAN, SCHEMA, HREFLANG, GRADE, ISSUES` |
| `README` | `tbl_readme` | `A2:B19` | 18 incl. header | `Tab, What it is and the rule` |
| `dashboard` | `tbl_dashboard` | `A2:B11` | 10 incl. header | `Measure, Count` |

## Type and formatting contract

- Existing values, formulas, headers, cell formats, validations, frozen rows, and existing filters were preserved; no column type was forcibly converted.
- The table metadata reports `tutors.active` and `tutors.approved` as `DROPDOWN`; `tutors.active` retains its existing `yes`/`no` validation. `reviews.date` is `DATE`. Other table column types are unset, leaving their existing cell formats in place.
- `README!A1` title remains outside `tbl_readme`. `dashboard!A1` title and the row-12 private-tabs note remain outside `tbl_dashboard`; formulas in `Count` remain in place.
- Existing helper/note values within the defined data extents were not edited. The `applications` basic filter remains intact until its owner-approved removal; its table range is therefore still pending.
- No applicant or student names, emails, WhatsApp numbers, login emails, or message text are included in this document.

## Verification

The workbook metadata was re-read after creating the tables. Eleven named table objects are present on the requested tabs, with the ranges and header names above. The existing `applications` filter remains and no `tbl_applications` object exists. No live intake, booking, application, or review submission was performed during this formatting update.

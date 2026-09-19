# Copy protection — the watermark, the copy line, and the ownership check

EkGuru's text is the only asset the site has that a scraper can take without
paying for it. This document is the whole of what protects it, what it proves,
and what to do when something looks copied.

There are four pieces, and they answer four different questions.

| Piece | Question it answers | Where it lives |
| --- | --- | --- |
| Watermark | "Whose page is this, when it is printed or saved as PDF?" | `css/experience.css` §22, `js/copywatch.js` |
| Copy line | "Where did this sentence come from?" | `js/copywatch.js` |
| Fingerprint record | "Was this text ours on a date I can prove?" | `data/copy-index.json`, `tools/build-copy-index.js` |
| Ownership panel | "Which EkGuru page is this pasted text from?" | `admin.html` card "Is this text ours?" |

## 1. The watermark

Printing and "Save as PDF" are the two ways a worksheet leaves the site in a
form that carries no site chrome — the header, the footer and the links are
gone, and what is left is a page of Hindi that could have come from anywhere.

So every page prints with:

- the text **EkGuru · ekguru.shop · © EkGuru** as a watermark on the sheet
  (drawn with `body::after`, so it prints even when the browser is set to
  *not* print background images — a background image watermark would silently
  disappear for those readers);
- a footer line carrying the full URL of the page it was printed from and the
  sheet's current tagline;
- `header`, `nav` and interactive controls hidden, so the sheet is content;
- on worksheet-like blocks (`.worksheet`, `.sheet`, `.print-area`, `.ws`,
  `.flashcards`, `.quiz-sheet`) a repeat of the watermark inside the block
  itself, through `[data-watermark]::after`.

The tagline in that footer is **not** a string baked into the CSS. It is read
at print time from the settings the site is running on
(`EKGURU_SHEET_SETTINGS.tagline`, written by `tools/sheetsync.js` from the
settings tab of the spreadsheet), so if the tagline in the sheet changes, the
printed footer changes with it — the same rule as the site footer itself.

## 2. The copy line

Copying 80 characters or more from a page appends a source line to the
clipboard:

```
— EkGuru · https://ekguru.shop/<page>/ · © EkGuru
```

The threshold matters: two or three words are a phrase and blocking them would
be hostile, while a paragraph is content. `js/copywatch.js` also stamps the
clipboard on `Ctrl/⌘+S` and on the browser's `beforeprint` event.

Nothing is blocked. Copying is allowed under the terms — quoting with
attribution is explicitly fine — the line just makes the attribution travel
with the text.

## 3. The fingerprint record

`node tools/build-copy-index.js` walks every page, extracts its prose (title,
body text, no navigation, no scripts), and writes
`data/copy-index.json`: one record per page.

```
{ "u": "answers/hindi-numbers-1-to-100/", "t": "…", "w": 480,
  "sha": "9f2c…", "n": 475, "s": [ … 160 window hashes … ] }
```

- `w` — words of prose on the page
- `sha` — sha1 of the whole text, truncated to 16 hex characters: the dated
  fingerprint of that page
- `n` — how many 6-word windows the page contains
- `s` — up to 160 of those windows, hashed

The file is committed. It is the record that EkGuru held this text on the date
in `generated`, and it is what makes "this is ours" a statement with evidence
rather than a claim. Rebuild it after editing pages — `python3
tools/build-all.py check` fails if it is stale, which is how it stays honest.

### Why 6-word windows and 160 samples

Measured on this corpus, not chosen by feel:

| Paste | 8-word × 48 (old) | 6-word × 160 (now) |
| --- | --- | --- |
| whole page | 1.00 | 1.00 |
| 60-word paragraph lifted from the page | 0.09 – 0.13 | 0.40 – 0.80 |
| unrelated prose | 0.00 | 0.00 |

Eight-word windows are more specific and much worse at *finding* anything: the
sampler on the page and the sampler on the paste pick different windows, so a
real lift scored below the "partly ours" line. One run of the old settings even
attributed a lifted paragraph to the wrong page. Longer windows also break on a
single edited word.

## 4. The ownership panel (admin)

`admin.html` → **Is this text ours? (ownership check)**. Paste a paragraph, a
page, or a competitor's article:

- **This is EkGuru's own text** (≥ 45%) — one page matches clearly. The answer
  names the page, its word count and its 16-character fingerprint.
- **Shared text** — three or more pages match equally well. This is template
  text (365 daily lessons, 196 country funnels, the course shell). It is ours,
  but it does not identify one page, and the panel says so instead of picking
  the alphabetically lucky one.
- **Partly ours** (≥ 15%) — a passage was probably reused in a new page. Check
  the two pages say different things before publishing both: Google treats
  near-duplicates as one page and drops one.
- **Nothing** — common phrasing, not copied text. The panel still fingerprints
  the paste so the owner has a dated copy.

Pastes under 40 words are refused with the reason: on this corpus a 25-word
paste lands on the wrong page about half the time, and a wrong answer is worse
than no answer.

The index is a static file fetched once and cached; nothing is sent anywhere,
and there is no server to send it to.

### Tests

```
node tools/test-copy-index.mjs      # the panel's own matcher, in a DOM, real corpus
node tools/test-search-facets.mjs   # country + language facets (see docs/DESIGN-SYSTEM.md)
```

`test-copy-index.mjs` loads `js/admin-ownership.js` itself rather than
re-implementing its hashing, because a builder and a panel that disagree about
what a fingerprint is fail silently — the panel just says "not ours" to the
site's own text. Both tests run inside `python3 tools/build-all.py check`.

## What to do when text looks copied

1. Paste it into the ownership panel. Note the page and the `sha`.
2. If it is a competitor's site, check the copy line is present. If it is not,
   the Wayback Machine timestamp plus `data/copy-index.json`'s `generated` date
   is the record.
3. Write to the site's contact address (the one in the footer). Most sites
   remove it on the first ask; the record is what is used if they do not.

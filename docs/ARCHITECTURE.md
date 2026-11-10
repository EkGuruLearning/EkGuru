# EkGuru — System Architecture and Repository Structure

Status: proposal + current-state reference. Owner decision needed before any
folder move (see §7). Nothing in this document changes a published URL.

## 1. What the system is

EkGuru is a static learning site (about 2,700 HTML pages) with a small Node
server for payments. Content is authored in Google Sheets and in JSON course
files, compiled by build tools into static pages, and checked by a single
quality gate before it ships.

```
 Google Sheets (CMS, published CSV)        Course JSON (data/courses)
            │                                        │
            ▼                                        ▼
   tools/sheetsync.js ─► overrides        tools/build-*.py (generators)
            │                                        │
            └──────────────► static pages ◄──────────┘
                                 │
                 tools/build-all.py check  (quality gate, must exit 0)
                                 │
                       static hosting (the site)
                                 │
                browser ─► js/ (runtime) ─► intake / live feed (Apps Script)
                                 │
                       server/ (payments, Razorpay)
```

## 2. Layers

| Layer | Responsibility | Lives in (today) |
|---|---|---|
| Content source | Hand-authored text, course units, tutor and review rows | `data/courses/`, `tools/lang-data/`, Google Sheets |
| Generators | Turn sources into HTML, JSON, CSV, sitemaps | `tools/*.py`, `tools/*.js` |
| Generated site | What the browser loads. Never edited by hand | Language folders at repo root, `learn/`, `languages/`, `tutor/`, `courses/`, `world-languages/` |
| Runtime | Browser behaviour: booking, search, progress, reviews | `js/`, `css/` |
| Integration | Sheets intake and live feed | `apps-script/*.gs` (deployed by owner) |
| Server | Payments and order store | `server/`, `src/runtime/` |
| Quality gates | Publish checks, language gate, indexing contract | `tools/build-all.py check`, `tools/language-gate.py`, `tools/ultra/contract.py` |
| Governance | Decisions, policies, audits | `docs/`, `data/quality/` |

## 3. Current layout (what is in the repo today)

- Roughly 330 tool scripts in `tools/`, mixing generators, tests and one-off
  audits. Tests and generators share one folder.
- Public URLs are folder names at the root (`learn-hindi-from-india/`,
  `languages/bn/`, `tutor/…`). Build scripts hard-code these paths.
- Generated pages and hand-written pages sit side by side in the same folders.
- `data/` mixes source data, generated indexes and quality reports.
- `src/` and `server/` hold the only non-static code, and are small.

This works, but it makes it hard to tell which files are safe to edit,
which are generated, and which are tests.

## 4. Target layout

The target separates **source**, **generators**, **generated output**,
**tests**, **integrations** and **docs**. The public site keeps its URLs.

```
ekguru/
├── src/                         # SOURCE — edit these
│   ├── content/                 # course JSON, lesson text, tutor and review rows
│   │   ├── courses/             #   (was data/courses/)
│   │   ├── languages/           #   (was tools/lang-data/)
│   │   └── tutors/
│   ├── site/                    # page templates, shell, design tokens
│   ├── runtime/                 # browser JS (was js/ + src/runtime/)
│   └── styles/                  # CSS source (was css/experience.css etc.)
├── generators/                  # BUILD — one folder, one job each
│   ├── pages/                   # *.py / *.js that write HTML
│   ├── data/                    # sheetsync, indexes, sitemaps, copy index
│   ├── visuals/                 # figures and OG cards
│   └── gates/                   # quarantine, language-gate, contract checks
├── tests/                       # TESTS — no generator logic here
│   ├── unit/
│   ├── data-sources/            # network tests (run in CI only)
│   └── e2e/                     # Playwright browser tests
├── integrations/
│   ├── apps-script/             # was apps-script/ (owner deploys)
│   └── sheets/                  # sheet schemas and setup notes
├── server/                      # payments API (Node)
├── docs/
│   ├── architecture/            # this file, ADRs
│   ├── runbooks/                # how to add a tutor, regenerate courses, deploy
│   ├── decisions/               # owner decisions with date and approver
│   └── audits/                  # dated audit reports (was docs/AUDIT-*.md)
├── site/                        # GENERATED — the published static site
│   ├── learn/ languages/ tutor/ courses/ world-languages/ …
│   └── assets/                  # images, fonts, bundled CSS and JS
└── data/                        # GENERATED reports and indexes only
    └── quality/                 # language gate, indexing baseline, coverage
```

Rules that go with this layout:

1. `site/` is never edited by hand. Only generators write it.
2. `src/` is the only place a human edits content or design.
3. `tests/` may read `site/` and `src/`, but generators never import from `tests/`.
4. `data/quality/` is written by gates only.
5. Every generator states its inputs and output in a header comment.

## 5. Data flow

**Content.** Sheet tabs are published as CSV. `sheetsync` writes overrides
into the build. Course JSON is validated against `data/schemas/` before any
page is written. A row that fails validation is quarantined, not published.

**Booking.** Browser → `js/features.js` → intake (Apps Script) → private
bookings sheet. The sheet write happens **first**. Only after it succeeds are
the three emails sent: to the student (receipt), to the booked tutor (request),
and to the owner (copy). If the sheet write fails, the booking is refused and
nothing is emailed. Tutor email falls back to the owner inbox when the tutor
has no `notification_email` (today Deepika and Utkarsh have none).

**Reviews.** Published reviews come from the live reviews tab
(gid `293675115`). The tab was recreated on 4 Nov 2026; the old gid
`298809212` must not be used.

**Indexing.** `data/quality/indexing-baseline.json` is the contract. Existing
index, noindex and canonical settings are preserved. New pages are noindex.
Tutor profile pages are noindex until the owner lifts the freeze.

## 6. Build and quality pipeline

`python3 tools/build-all.py check` runs the whole gate (about 100 checks) and
must exit 0 before a merge. Order that matters:

1. Strip the decorative layer (`apply-ultra --strip`) for legacy checks.
2. Regenerate data and pages in dependency order: course levels, country and
   course hubs, quarantines, page layer, visuals, flashcards, copy index,
   site shell, inventories.
3. Re-decorate and run the tests.

Generators that rewrite each other's output must be run to a fixed point in
the stripped state. Current known cycles are documented in
`docs/architecture/known-cycles.md` (to be written with the first fix).

**Language gate.** `tools/language-gate.py` writes `data/quality/language-gate.json`.
A language is OPEN only with a verified native review record in
`data/reviews/{code}.json`. Without it the publication status is BLOCKED.
Code cannot create those records. Waivers are owner decisions and are written
to `docs/decisions/`, not to the review files.

## 7. Migration plan (no URL changes until approved)

Moving folders changes URLs and breaks generators that hard-code paths. Do it
in phases, each one a separate PR that keeps `build-all.py check` green.

| Phase | Work | URL risk |
|---|---|---|
| 0 | Write this document. Add `docs/decisions/` and `docs/runbooks/`. | None |
| 1 | Move tests out of `tools/` into `tests/` (paths only; no logic change). | None |
| 2 | Move generators into `generators/` and fix their path constants. | None |
| 3 | Move sources into `src/content` and `src/styles`. Build still writes to the same URLs. | None |
| 4 | Build output into `site/` and point hosting at it. Add a redirect map from old paths. | **High** — needs redirect map and owner sign-off |
| 5 | Remove the old copies. | Only after phase 4 is stable for a full crawl cycle |

Owner decision needed: approve phases 0–3 now, and decide on phase 4 (needs
hosting configuration and a redirect map).

## 8. Conventions

- Dated audit reports: `docs/audits/YYYY-MM-DD-<topic>.md`.
- Owner decisions: `docs/decisions/YYYY-MM-DD-<topic>.md`, with approver and scope.
- Branch names: `fix/…` or `feat/…`, one PR per concern.
- Commits: imperative subject, body says what and why, attribution lines last.
- A PR that changes generated output must also change its generator or source.
- No file in `site/` is reviewed line by line. Review the generator and the source.

## 9. Known risks and open items

- Language gate BLOCKED: 700 languages lack native review records.
- Master check depends on several generators that rewrite shared pages. Fixed
  in one place at a time. The cycles are a maintenance risk until phase 2 makes
  ordering explicit.
- Live sheet and Apps Script depend on owner-side deployment settings (the CI
  Apps Script check currently gets 403 from the deployed endpoint).
- Two tutors have no notification email. Booked-tutor mail falls back to the
  owner inbox for them.

# EkGuru repository structure: where everything lives and where new work goes

Status: current-state map plus rules for new work. Written 18 Nov 2026, phase 0
of the migration in [`../ARCHITECTURE.md`](../ARCHITECTURE.md) §7. **Nothing in
this document moves a file or changes a published URL.**

## 1. The one rule that shapes this repo

The site is served straight from the repository root by GitHub Pages
(`CNAME`, `.nojekyll`). **A folder name at the root is a public URL.**
`hindi/`, `learn/`, `languages/` are the website, not code organisation.
Moving one changes its URL, breaks inbound links and search rankings, and
breaks every generator that hard-codes the path. So:

- Folders that are URLs stay where they are until phase 4 (see §6).
- Source, tooling, tests and docs are the part that can be tidied safely,
  and they are tidied in phases 1 to 3.
- New work follows the placement rules in §4 from today.

## 2. The map

Legend for **Kind**: `URL` published page folder, `SRC` hand-edited source,
`GEN` written by a generator (do not hand-edit), `RUN` browser runtime,
`OPS` integration or server, `QA` gate or report, `DOC` documentation.

### 2.1 Published URL folders (generated unless noted)

"Pages / indexable" is read from `data/quality/full-page-inventory.json`
(2,731 pages, 1,012 indexable on 18 Nov 2026), so it matches what the gates
see. "Writer" is filled in only where it has been confirmed in code; for the
rest, find the writer with `grep -l "<folder>/" tools/build-*` and read its
header. The full chain and its order are in `tools/build-all.py`.

| Folder (root) | Kind | What it is | Pages / indexable | Writer (confirmed) |
|---|---|---|---|---|
| `index.html`, `find-tutors.html`, `join.html`, `tutor.html`, `admin.html`, `404.html` | URL | Top-level pages | 5 / 3 | hand-edited, then the regeneration sequence |
| `languages/` | URL | Per-language hub and starter pack (`languages/<code>/`), the A1–C5 ladder (`languages/<code>/level/`) | 1,200 / 211 | `build-course-levels.py` (level pages), `build-phase7-pages.py` (hubs, starter packs) |
| `learn/` | URL | Learn-tab posts (1,000+ word gate) | 415 / 259 | — |
| `learn-hindi-from-<country>/` | URL | Country pages | 196 / 54 | — |
| `learn-hindi-for-<language>-speakers/` | URL | "Hindi for speakers of X" | 141 / 0 (noindex) | `build-phase7-pages.py` |
| `learn-hindi-by-country/` | URL | Country index | 1 / 0 | — |
| `world-languages/` | URL | Country-by-language pages | 195 / 0 (noindex) | — |
| `hindi-tutor/` | URL | Tutor-finder pages by city and country | 39 / 39 | `apply-tutor-location-specifics.py` from `data/content/tutor-location-specifics.json` |
| `tutor/` | URL | One page per tutor. Profile pages stay noindex until the owner lifts the freeze | 9 / 1 | `build-tutor-pages.js` |
| `hindi/` | URL | Hindi learning hub | 35 / 35 | — |
| `bengali/ gujarati/ marathi/ punjabi/ tamil/ telugu/ urdu/` | URL | One hub per Indian language, 34 pages each | 34 each / 32–33 | — |
| `kannada/ malayalam/` | URL | Same layout, **noindex** (course incomplete, see language gate) | 34 each / 0 | — |
| `ar/ bn/ de/ es/ fr/ id/ it/ ja/ ko/ pl/ pt/ ru/ tr/ ur/ vi/ zh/` | URL | Source-language packs | 1–4 each / all | — |
| `answers/`, `ask/` | URL | Question and answer pages | 29 / 28 and 44 / 44 | — |
| `daily-hindi/`, `toolbox/`, `materials/`, `name-in-hindi/` | URL | Daily phrase, tools, printable materials | 31, 14, 16, 1 | — |
| `courses/` | URL | Course player and course hub | 2 / 2 | — |
| `start/`, `live-class/`, `design/`, `review/`, `search/`, `support/` | URL | Product pages | 1 each | `start/` by `build-phase7-pages.py` |
| `about/ authors/ contact/ privacy/ terms/ disclaimer/ cookie-policy/ copyright/ editorial-policy/ monetization-disclosure/ faq/ how-levels-work/` | URL | Trust, legal and policy pages | 12 | — |
| `live-sheets/` | URL | Published CSV snapshots of sheet tabs | not pages | — |
| `sitemap-*.xml`, `sitemap.xml`, `robots.txt`, `feed.xml`, `search-index.json`, `llms.txt`, `manifest.webmanifest`, `sw.js` | GEN | Crawler and PWA files | not pages | `build-search-index.py` writes `search-index.json`; sitemap builders are inside the course and country builders |
| `CNAME`, `.nojekyll`, `ads.txt`, `googleb3b0e3defc1daa17.html`, `f28bc2b1708bb36cf11365b735f24f14.txt` | URL | Hosting and verification files. **Never move or rename.** | — | hand |

### 2.2 Source, runtime, tooling

| Folder | Kind | What it is | Edit by hand? |
|---|---|---|---|
| `data/courses/` | SRC | Course JSON: `phase-N/<code>_<level>.json`, about 1,070 files | Yes, content work. Never bulk-generate (see language gate) |
| `data/schemas/`, `data/editorial/`, `data/reviews/` | SRC | Schemas, editorial rules, native-review records | Yes, reviews only by a human reviewer |
| `data/quality/` | QA | Language gate, indexing baseline, audits | **No.** Gates write it. Exception: `owner_approved_new_indexable` in the baseline (owner decision) |
| `data/*.json`, `data/flashcards/`, `data/themes/`, `data/audio-manifest/`, `data/learning/` | GEN/SRC | Indexes and datasets used by builders and runtime | Check the writer first |
| `js/` | RUN | Browser scripts: booking, sheet loader, course player, voice, flashcards | Yes. `js/site-config.js` holds site settings |
| `css/` | RUN | Styles. `tokens.css` is the design-token source | Yes. `style.min.css` is a bundle |
| `src/runtime/` | RUN | New home for runtime source (phase 3). Today only `voice.js` | Yes |
| `images/` | SRC | Images, tutor photos, OG cards (`og-cover.jpg`) | Yes. Tutor photos belong here, not in private Drive links |
| `tools/` | GEN | About 330 scripts. 111 tests, 109 build/audit/apply scripts, helpers | Yes, but see §3 |
| `tools/lang-data/`, `tools/course-data/`, `tools/*-phase3-content/` | SRC | Authored inputs for generators | Yes |
| `tools/lib/`, `tools/ultra/`, `tools/templates/`, `tools/assets/` | GEN | Shared helpers, indexing contract, page templates, fonts | Yes, with care. `ultra/contract.py` enforces the indexing freeze |
| `tests/fixtures/` | QA | Fixtures for tests | Yes |
| `server/` | OPS | Node payments API (Razorpay) | Yes. Not served as pages |
| `apps-script/` | OPS | Google Apps Script sources. The owner deploys them | Yes, but deployment is manual |
| `csv/` | OPS | Upload pack for rebuilding the sheet | Rarely. Keep tutor emails out |
| `reports/` | QA | Generated and dated reports, evidence JSON | **No.** Written by tools |
| `research/` | DOC | Language and platform research notes | Yes |
| `docs/` | DOC | Architecture, runbooks, decisions, audits, owner commands | Yes |
| `.github/workflows/` | OPS | CI: `ci.yml` (checks, journeys), `course-health.yml`, `live-guard.yml`, `playwright.yml` | Yes. Changing it changes what blocks a merge |
| `Arena latest command  arena/` | DOC | Stray scratch folder (note the double space). Referenced by `tools/ultra/contract.py`; see [`../ROADMAP-FIXES.md`](../ROADMAP-FIXES.md) | No |

## 3. What is hard to see today, and how to tell

- **Generated or hand-written?** Every generator should say, in its header,
  its inputs and its output folder (many older ones do not; fixing that is on
  the roadmap). If a page's folder is in §2.1 and has a confirmed writer, edit
  the writer or its source, never the page. If the writer is unknown, search
  `tools/` for the folder name before touching the page.
- **Test or generator?** In `tools/`, `test-*.{py,js,mjs}` are tests (111);
  they write nothing the site serves. Everything named `build-*`, `apply-*`,
  `author-*`, `inject-*`, `repair-*`, `make-*` writes files.
- **Is this folder a URL?** If it is in §2.1, yes.

## 4. Where new work goes (from today)

| You are adding | Put it | Also do |
|---|---|---|
| A new language course level | `data/courses/phase-N/<code>_<level>.json` | Run the regeneration sequence; language gate stays BLOCKED until a native reviewer signs |
| A new topic page for an existing language | The generator's source data, not the page | Regenerate; new pages are **noindex** unless the owner approves (below) |
| A new indexable page | Generate it, then record the owner approval | Add the path to `owner_approved_new_indexable` in `data/quality/indexing-baseline.json` and a note in `docs/decisions/` |
| A new generator | `tools/` for now, named `build-<thing>.py`, with a header (inputs, output, how to run) | Register it in `tools/build-all.py` if its output is checked |
| A new test | `tools/test-<thing>.{py,mjs}` for now. After phase 1: `tests/unit/` | Add it to `ci.yml` or `build-all.py` so it blocks a merge |
| New browser code | `js/<feature>.js` for now. After phase 3: `src/runtime/` | No framework. Keep it under the page weight budget |
| A new tutor | The Google Sheet, then see [`../ADD-A-TUTOR.md`](../ADD-A-TUTOR.md) | Never commit a tutor email or phone number |
| An owner decision | `docs/decisions/YYYY-MM-DD-<topic>.md` | Name the approver and scope |
| A dated audit | `docs/audits/YYYY-MM-DD-<topic>.md` | No applicant or customer personal data in a public repo |
| A how-to for a repeated job | `docs/runbooks/<job>.md` | Link it from `docs/README.md` |

## 5. Naming and header conventions

- Folders and files: lowercase, hyphens. Pages are `<folder>/index.html`.
- Course data: `<iso-code>_<LEVEL>.json` (`hi_A1.json`, `hi_A1+.json`).
- Tools: `build-`, `apply-`, `audit-`, `author-`, `inject-`, `repair-`, `test-`.
  One verb per file; if a file does two jobs, split it.
- Every tool starts with a docstring or comment: purpose, inputs, outputs,
  command. `tools/build-course-levels.py` is a good model.
- Branches: `feat/…`, `fix/…`, `docs/…`, `seo/…`. One concern per PR.
- Commits: imperative subject, a body that says what and why.

## 6. Migration status

Plan and rationale: [`../ARCHITECTURE.md`](../ARCHITECTURE.md) §4 and §7.

| Phase | Work | Status | URL risk |
|---|---|---|---|
| 0 | Documents, runbooks, contributor files, per-folder READMEs | **Done in this change** | None |
| 1 | Move tests out of `tools/` into `tests/unit/` (about 111 files, fix root paths, CI and `package.json`) | Next. Own PR, `build-all.py check` must exit 0 | None |
| 2 | Move generators into `generators/` and fix path constants | After phase 1 | None |
| 3 | Move sources into `src/` | After phase 2 | None |
| 4 | Build output into `site/`, hosting pointed at it, redirect map | **Needs owner sign-off and hosting change** | High |
| 5 | Remove old copies | Only after phase 4 survives a full crawl cycle | Low |

Phase 4 is the only phase that can hurt rankings. Until it is approved, the
root folders in §2.1 are the site.

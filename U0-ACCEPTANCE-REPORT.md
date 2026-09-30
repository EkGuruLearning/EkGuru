# U0 ACCEPTANCE REPORT — Zero-Tutor State + Sheet CSV→TSV Fallback
**Phase:** U0 (ULTRA MASTER COMMAND v3) · **Branch:** `arena/01a0f024-ekguru` · **Commits:** `342d682`, `00fae57`, `c9cc995`
**Status:** ✅ MERGE-READY — **CI GREEN on PR #21**: https://github.com/EkGuruLearning/EkGuru/pull/21
(checks 1m55s ✔ · journeys 50s ✔ — run 36668906748 / 36668906780). Superseded **PR #20 closed** with a note.

---

## 1. Public tutor count: **0**
`public tutor = in js/tutors/_registry.js AND sheet active=yes`. The live tutors tab
carries 5 rows + 1 `#help` row and **every row is `active=no`**, so the public roster is
empty. Hidden (but content kept, noindex): `sushila-g`, `hemlata`, `shikha-dutta`,
`tara`, `sarshtee-baliyan` (last 3 also out of registry). Rebuild with `active=yes`
restores everything — proven in §5.

## 2. TSV fallback proof
- Published CSV endpoints answer **HTTP 500**; `output=tsv` answers **200** (verified
  against the live workbook; sandbox network is blocked, so the live fetch path is
  exercised in CI by `tools/test-data-sources.py` + `tools/test-sheet-loader.js`).
- New shared helper `tools/sheet-fetch.js` (+ browser twin in `js/sheet.js`):
  `output=csv` → fallback `output=tsv`, one RFC-4180 parser for both formats with
  quoted + multi-line cells (about/bio/experience/methodology survive intact).
- `js/site-config.js` 4 `csvUrl` fields **unchanged** (fallback lives in the helper).
- `tools/test-data-sources.py` now reports **`PASS (tsv fallback)`** when csv fails and
  tsv passes, FAIL only when both fail; schema checks run identically on both formats;
  offline fixture mode (`EKGURU_TEST_FIXTURE_DIR=tests/fixtures`) verified here:
  `21 checks, 0 failures`.

## 3. Zero-tutor state (R-5, generator-owned both directions)
| Surface | Zero-state behaviour (verified on disk) |
|---|---|
| Hidden profile page | full content kept, `<meta name="robots" content="noindex, follow">`, WebPage-only JSON-LD, booking replaced by honest notice + free-course CTA, no `tutor.html?id=` anywhere |
| sitemap-tutors.xml / sitemap.xml / feed.xml | 0 tutor URLs (prune+upsert keeps other generators' entries) |
| find-tutors.html + tutor/index.html ItemList JSON-LD | `numberOfItems: 0`, `itemListElement: []` |
| llms.txt | "Tutors listed: 0", price-range/trial lines removed, no per-tutor links, no "from $N per lesson" claim |
| manifest.webmanifest | "Book with X" shortcuts gone; "Start the free course" shortcut instead |
| 404.html | no tutor links; free-course door |
| Home grid + hero card + 6 locale cards | honest empty state (EN + ar/de/es/fr/ja/pt) linking `/learn/`, `/courses/`, `/daily-hindi/` |
| "Find a tutor" CTAs | → "Start the free course" via generator (build-shell header, build-roster-rows families: hindi-tutor/, learn-hindi-from-*, answers/) |
| langsync.js + all builders | tolerate 0 tutors (no throw) |

## 4. Pages touched
**2670+ files** across the U0 commits (`342d682` + CI-observability `00fae57` +
LIVE-mode fix `c9cc995`). Tooling (22 files): `tools/sheet-fetch.js`,
`tools/lib/zero-state.js`, `tools/test-sheet-fetch.mjs`, `tools/test-tutor-activation.mjs`,
`tests/fixtures/*.tsv` (new); `js/sheet.js`, `js/i18n.js`, `js/main.js`,
`js/tutors/_registry.js`, `tools/{sheetsync,langsync,build-home-tutors,build-market-pages,
build-roster-rows,build-shell,build-tutor-pages,test-journeys}.js|mjs`,
`tools/lib/site-data.js`, `tools/test-{data-sources.py,sheet-loader.js,experience-dom.mjs}`,
`.github/workflows/ci.yml` (edited). Rest = regenerated site pages (roster rows 263,
shell refresh 2636, profiles, sitemaps, feed, llms.txt, manifest, 404, homes, markets,
copy-index, search index).

## 5. New tests (R-10)
- `tools/test-sheet-fetch.mjs` — **35/35** (csv→tsv fallback, quoted/multi-line TSV,
  CSV↔TSV parity, fetch retries, 5 sheets' required columns, privacy scan).
- `tools/test-tutor-activation.mjs` — **45/45**. Flips fixture row `sushila-g`
  `active=yes` ⇄ `active=no` through the real generators (sheetsync → build-tutor-pages
  → build-home-tutors → build-market-pages) and asserts the FULL restore in both
  directions (profile indexability, booking, Person/WebPage JSON-LD, sitemaps, feed,
  llms.txt, manifest, 404, ItemLists, home/market cards + hero). Restores the working
  tree byte-for-byte. It caught a real 0→1 bug (sitemap upsert had no anchor when zero
  tutor blocks existed) — fixed.
- Rewritten: `tools/test-sheet-loader.js` (live, expectations derived from the fetched
  rows — registry ∩ active=yes), `tools/test-data-sources.py` (above).

## 6. Gates (all green, run locally)
| Gate | Result |
|---|---|
| `python3 tools/build-all.py check` | **EXIT 0** ✔ every generated layer up to date |
| **CI `checks` (PR #21)** | **PASS 1m55s** ✔ incl. build-all check, preflights, inventory, live data-source (csv→tsv fallback), loader smoke, sheet policy, re-activation, public-output, jsdom QA |
| **CI `journeys` (PR #21)** | **PASS 50s** ✔ five Playwright user journeys |
| `node tools/test-tutor-activation.mjs` | 45/45 |
| `node tools/test-sheet-fetch.mjs` | 35/35 |
| `python3 tools/test-data-sources.py` | 21/21 offline fixture mode; live "PASS (tsv fallback)" green in CI |
| `python3 tools/inject-ads.py --check` | inside build-all check, green |
| `node tools/test-ad-policy.mjs` | 22/22 |
| `node tools/test-tutor-claims.js` | PASS (2741 files) |
| `node tools/test-no-competitor-attribution.js` | PASS |
| `node tools/test-sheet-apply.js` / `test-sheetsync-policy.js` | PASS |
| `node tools/test-browser-qa.mjs` / `test-experience-dom.mjs` | 26/26 · all checks passed |

## 7. CI — GREEN
`ci.yml` runs the new suites as dedicated steps (sheet fetch unit tests + loader live
smoke + tutor re-activation cycle), and the two network steps write their verdict to the
step summary and emit `::error` annotations on failure. **PR #21:**
https://github.com/EkGuruLearning/EkGuru/pull/21 · green run:
https://github.com/EkGuruLearning/EkGuru/actions/runs/36668906748 (checks, incl. the
live data-source step with csv→tsv fallback) and
https://github.com/EkGuruLearning/EkGuru/actions/runs/36668906780 (journeys).
PR #20 closed as superseded.

### CI fixes made while getting to green (all R-5/R-10: generator or test owned)
1. `tools/test-journeys.mjs` J1/J2 asserted a live tutor exists (`#stat-tutors` not "0";
   click "Sushila") — a direct conflict with the real all-`active=no` sheet. Both now
   follow whichever state is honest: roster → profile, zero → empty state + free course.
2. `tools/test-data-sources.py` LIVE mode was **unreachable**: `Path("")` is
   `PosixPath('.')` (truthy, a dir), so the test always ran OFFLINE mode and CI hunted
   for `./tutors.tsv`. The env var alone now decides. Diagnosed with a monkeypatched
   `urlopen` dry run of the LIVE path (csv HTTP 500 → tsv fallback → "PASS (tsv
   fallback)" verdict) and by verifying all four live tab headers against the schema
   checks.

## 8. Notes
- Golden Rules honoured: no cloaking (empty states are honest text, hidden pages keep
  real content and say so), R-5 (every change generator-owned, nothing hand-edited),
  R-7 (noindex applied exactly as the U0 command authorises), runtime ad flags still
  `false`, no new indexable page classes.
- Fixed decisions preserved: hidden profile = full page + noindex + booking-off; header
  "Find tutors" CTA → "Start the free course" when 0 public; nav "Tutors" links and the
  find-tutors page itself stay (they show the honest empty state).

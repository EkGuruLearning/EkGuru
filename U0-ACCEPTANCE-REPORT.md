# U0 ACCEPTANCE REPORT — Zero-Tutor State + Sheet CSV→TSV Fallback
**Phase:** U0 (ULTRA MASTER COMMAND v3) · **Branch:** `arena/01a0f024-ekguru` · **Commit:** `190b963`
**Status:** ALL GATES GREEN locally. Push/PR blocked only by an expired GitHub token (Arena reconnect needed).

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
**2670 files** in commit `190b963`. Tooling (21 files): `tools/sheet-fetch.js`,
`tools/lib/zero-state.js`, `tools/test-sheet-fetch.mjs`, `tools/test-tutor-activation.mjs`,
`tests/fixtures/*.tsv` (new); `js/sheet.js`, `js/i18n.js`, `js/main.js`,
`js/tutors/_registry.js`, `tools/{sheetsync,langsync,build-home-tutors,build-market-pages,
build-roster-rows,build-shell,build-tutor-pages}.js`, `tools/lib/site-data.js`,
`tools/test-{data-sources.py,sheet-loader.js,experience-dom.mjs}`,
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
| `node tools/test-tutor-activation.mjs` | 45/45 |
| `node tools/test-sheet-fetch.mjs` | 35/35 |
| `python3 tools/test-data-sources.py` | 21/21 offline fixture mode; live "PASS (tsv fallback)" is the CI path |
| `python3 tools/inject-ads.py --check` | inside build-all check, green |
| `node tools/test-ad-policy.mjs` | 22/22 |
| `node tools/test-tutor-claims.js` | PASS (2741 files) |
| `node tools/test-no-competitor-attribution.js` | PASS |
| `node tools/test-sheet-apply.js` / `test-sheetsync-policy.js` | PASS |
| `node tools/test-browser-qa.mjs` / `test-experience-dom.mjs` | 26/26 · all checks passed |

## 7. CI
`ci.yml` gains the two new steps (fetch tests + tutor re-activation cycle). **CI run link
pending** — the GitHub token in this sandbox (`GH_TOKEN`) is expired
("authentication failed … no longer valid"), so `git push`/`gh` are blocked. Once GitHub
is reconnected in Arena: push `arena/01a0f024-ekguru`, open the PR, require the ci run,
close superseded **PR #20** with a note (its scope is included here), and append the CI
run URL to this report.

## 8. Notes
- Golden Rules honoured: no cloaking (empty states are honest text, hidden pages keep
  real content and say so), R-5 (every change generator-owned, nothing hand-edited),
  R-7 (noindex applied exactly as the U0 command authorises), runtime ad flags still
  `false`, no new indexable page classes.
- Fixed decisions preserved: hidden profile = full page + noindex + booking-off; header
  "Find tutors" CTA → "Start the free course" when 0 public; nav "Tutors" links and the
  find-tutors page itself stay (they show the honest empty state).

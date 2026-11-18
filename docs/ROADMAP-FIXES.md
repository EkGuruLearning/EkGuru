# EkGuru: prioritised fixes and who does them

Written 18 Nov 2026 from the state of `main` after PR #52. This is the working
list. Update it in the same PR that closes an item. No personal data here;
applicant-level sheet findings stay in the private audit, not in this public
repository.

**Who:** `Owner` needs a Google, Cloudflare or GitHub setting or a decision.
`Agent` can be done in the repo, one small PR each, gate green.
`Reviewer` needs a native-speaker or subject reviewer; code cannot do it.

**Done when** is the check that closes the item.

## P0: the site does not do what it says until these are done

| # | Fix | Who | Where | Done when |
|---|---|---|---|---|
| 1 | Live feed is off: `feed.url` is empty, so sheet tutors and reviews have no public effect | Owner, then Agent PR | `apps-script/Unified.gs`, `js/site-config.js` (~line 751) | `curl "<url>?action=health"` returns JSON and a sheet-only tutor appears on the site |
| 2 | Redeploy the intake Apps Script so the duplicate-application guard (PR #49) is live | Owner | `apps-script/Intake.gs` | New version deployed; a repeat submission is marked superseded, not duplicated |
| 3 | Tutor photos in the sheet are private Drive links and some tutors use a placeholder, so profiles show no real face | Owner, Agent | sheet `tutors.photo`, `images/` | Every live tutor has a public image; no private Drive links |
| 4 | Language gate is BLOCKED for 700 languages: no native review records | Reviewer, Owner | `data/reviews/<code>.json`, `docs/decisions/` | Per-language record exists, or a dated owner waiver is written |
| 5 | Search Console: submit `sitemap.xml` and `sitemap-places.xml`; request indexing for the six approved country pages | Owner | Search Console | Sitemaps show "Success"; pages inspected |

## P1: content and SEO quality

| # | Fix | Who | Where | Done when |
|---|---|---|---|---|
| 6 | **No lecture-wise syllabus.** Each language ladder (`languages/<code>/level/`) lists levels only. Level pages are one 100–160 KB page each, with lessons anchored (`#a1-u1-l1`) but no lecture numbers, no per-language syllabus and no previous/next lesson links | Agent | `tools/build-course-levels.py` (`ladder_page`, `level_page`) | Ladder page lists every unit and lesson in order with links to the anchors; each lesson links to the next; `ItemList` schema covers lectures; gate green |
| 7 | **Level 0 (script) is in the data but not on the page.** The A1 files for hi, bn, ta, te, mr, gu, pa, ur and ml carry `alphabet`, `pronunciation` and `counting` blocks. For Hindi the A1 level page does not contain the alphabet block's title, so the block appears to be unrendered (confirm per language before building). Rendering them gives each script-based language a script lesson | Agent | `data/courses/phase-*/<code>_A1.json`, `build-course-levels.py` | A1 pages for hi, bn, ta, te, mr, gu, pa, ur show letters, pronunciation tips and counting |
| 8 | Malayalam has 11 of 16 rungs; Kannada has no published course levels. Author them, do not bulk-generate | Reviewer + Agent | `data/courses/` | Levels pass `language-gate.py` structure checks |
| 9 | No courses yet for as, or, sa, ks, kok, mai, mni, sd, brx, doi, sat | Reviewer + Agent | `data/courses/` | Per-language plan accepted, then levels authored with review |
| 10 | Hindi topic folders under `learn/hindi/` are mostly index-only (basics, elementary, intermediate, and others); the standalone `learn/hindi-*` topic pages are not linked as lectures | Agent | `learn/hindi/`, `tools/build-hindi-*.py` | Level hub links lectures in order; each lecture has objective, examples, practice, quiz, next link |
| 11 | The shared share image (`images/og-cover.jpg`) makes claims ("Verified native tutors", a language count) that must match the sheet and the course catalogue | Owner, Agent | `images/og-cover.jpg`, `tools/build-og-images.py` | Claims on the image are true on the day it ships |
| 12 | 891 pages have no inbound link (all noindex today) | Agent | `data/quality/full-page-inventory.json` | Orphans linked from a hub, or deliberately left out |

## P2: engineering structure (the migration)

Plan: [`ARCHITECTURE.md`](ARCHITECTURE.md) §7 and
[`architecture/REPO-STRUCTURE.md`](architecture/REPO-STRUCTURE.md) §6.

| # | Fix | Who | Done when |
|---|---|---|---|
| 13 | Phase 1: move the 111 `test-*` scripts from `tools/` to `tests/unit/`, fix repo-root resolution (about 100 files use `parents[1]`, `__dirname/..`, `import.meta.url`), update `ci.yml`, `package.json` and `build-all.py` references | Agent | Gate and both CI jobs green, no file left in `tools/` named `test-*` |
| 14 | Phase 2: move generators to `generators/` with an inputs/outputs header on each | Agent | Same, plus header lint passes |
| 15 | Phase 3: move sources into `src/` | Agent | Same |
| 16 | Phase 4: build output to `site/` with a redirect map and hosting change | Owner decision first | A full crawl cycle shows no lost rankings |
| 17 | `tools/test-reading-layer.mjs` has a hard-coded page count that every new page breaks | Agent | Count is derived from the inventory |
| 18 | Add a header (inputs, output, command) to every generator that lacks one | Agent | Header check passes |

## P3: tidy-up (each a tiny PR)

| # | Fix | Notes |
|---|---|---|
| 19 | Remove the stray `Arena latest command  arena/` folder | Referenced by `tools/ultra/contract.py`, `tools/lib/ultra_content.py` and `tools/test-tutor-claims.js`; change those first |
| 20 | `playwright.yml` still lists branch `arena/01a0e390-ekguru` | Remove the stale branch trigger |
| 21 | Root clutter: `FINAL_REPORT.md`, `U0-ACCEPTANCE-REPORT.md` | Move to `docs/audits/`; several reports reference them, so update links |
| 22 | `tools/_as2_patch*.txt`, `tools/_countries-cache.json` | Delete if no script reads them |
| 23 | `js/email-templates-backup.js` and `js/email-templates-v300.js` beside `js/email-templates.js` | Delete if no page loads them |
| 24 | Dated audits and owner command files sit loose in `docs/` | Move to `docs/audits/` and `docs/commands/archive/`; keep `HANDOVER-FOR-AI.md` but mark it as a 2 Nov snapshot |
| 25 | Enable CODEOWNERS and branch protection (require `checks` and `journeys`) | Owner: needs a GitHub user or team handle for the org `EkGuruLearning` |
| 26 | Sheet hygiene: dashboard cell showing `#REF!`, test bookings counted as open, empty `reviews` tab, blank spare tabs, missing `notification_email` for some tutors | Owner; detail is in the private sheet audit |
| 27 | Owner decision: build side shows tutors by `active`, runtime by `approved` plus `active` | Owner; record in `docs/decisions/` |

## Order of work

1. P0 items 1, 2, 5 first: they are settings, take minutes, and unlock the rest.
2. Item 6 and 7 together (one generator, one PR each): the biggest gain for
   learners and for "0 to hero" structure, with no new pages and no indexing risk.
3. Migration phase 1 in its own PR, never mixed with content changes.
4. Everything else as capacity allows.

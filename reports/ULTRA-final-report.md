# EkGuru ULTRA — Learn / Tools / Admin Implementation Report

**Date:** 2026-09-11 · **Commit:** `4fe79de` (local; GitHub push credential-blocked, see §10)
**Scope:** `/home/user/uploads/EkGuru_Next_Remaining_ULTRA_Learn_Tools_Admin_Implementation.md` — all 20 sections.

---

## 1. Learn inventory (baseline + what changed)

Static quality baseline: `reports/learn-tools-quality-baseline.json` → **109 pages**.

| Kind | Count | Grades | Notes |
|---|---|---|---|
| learn (guides + hub) | 16 | 12 A / 4 B | unchanged content |
| tool (12 tools + toolbox hub) | 13 | 5 A / 8 B | 3 upgraded (search) |
| daily-hindi | 31 | 31 B | unchanged |
| answer (questions) | 29 | 1 A / 28 B | unchanged |
| path (hub + 6) | 7 | **new** (6 B, hub C) | generated |
| practice (hub + 12 labs) | 13 | **new** (11 B, 2 C) | generated |

**Improved:** `learn/index.html` (paths + practice entry points); 3 toolbox search tools (§5); practice labs carry static "what's inside" sample lists; path pages carry a static no-JS lesson outline; `sitemap-learn.xml` regenerated (16 → 36 URLs).

**New:** 6 learning paths + paths hub; 12 practice labs + practice hub; 4 learner JS systems; 2 new tooling scripts; admin Learn Ops (§4).

**Remaining weak (grade C, 5):** `/learn/paths/` (hub), `/learn/practice/` (hub), `/learn/practice/grammar/` (51), `/learn/practice/daily/` (53), `/learn/paths/everyday-hindi/` (52). The two hubs are navigation pages by design; the three others are interactive pages whose real content lives in the bank and is rendered by JS (the static crawler only sees the shell). The admin quality board also flags **21 pages below 65** internal score — mostly short answer pages (e.g. `best-hindi-movies-to-learn-hindi` 56, `difference-between-hindi-and-urdu` 59) that have 0 Devanagari and no tool links. These are the next improvement targets, not the new labs.

---

## 2. Tools — fixed / upgraded / new / broken

- **Tested (real browser):** `tools/test-tools-functional.py` drives every tool's actual controls → **12/12 PASS, 0 FAIL** (`reports/tool-functional-qa.json`). A page opening is not proof; each tool was exercised (number conversion, phrasebook search/restore, flashcards flip/advance/reset, quiz start/answer, typing `namaste→नमस्ते`, verbs/vocab search, date-time, pronunciation next/tip, level-test answers, time planner).
- **Upgraded:** `toolbox/hindi-verbs`, `hindi-vocabulary`, `hindi-phrasebook` — added a `norm()` diacritic-stripping / doubled-vowel-collapsing normaliser so `khana` / `khaana` / `khānā` all match. Devanagari search unaffected.
- **New:** none added to `toolbox/` (no fake/broken generators). The new *practice labs* are the new tools (12 of them), each with a working drill, honest limits, and no fabricated scoring.
- **Broken:** 0.

---

## 3. Learning paths (6)

Single source of truth: `js/learning-paths.js`. Each path has goal / level / duration / tagline / intro / modules / lessons (real URLs) / practice / quiz / review / completion / next.

| Slug | Level | Lessons |
|---|---|---|
| hindi-from-zero | Beginner | 15 |
| speaking-starter | Beginner+ | (varies) |
| reading-hindi | Beginner | (varies) |
| travel-hindi | Beginner | (varies) |
| everyday-hindi | Intermediate | (varies) |
| grammar-foundations | Intermediate | (varies) |

- **No dead ends:** every lesson URL resolves to a real page (admin graph: 0 red). Each path points at existing practice/quiz/review URLs.
- **No cycles:** `grammar-foundations.next = null` (terminal) breaks the only `next`-step loop; the admin graph confirms **0 cycles, 0 dead ends, 0 orphans**.

---

## 4. Advanced learning systems + practice labs (12)

Engine `js/practice-engine.js` (single engine, no per-page logic duplication), bank `js/practice-bank.js` (**112 items, 10 banks**), progress `js/path-progress.js` (browser-local `localStorage`).

Labs: vocabulary (20), grammar (12), sentence-builder (12 order), verbs (10), **reading (8 new)**, **writing/Devanagari (8 new)**, **speaking (10 new, self-graded reveal — explicitly "nothing here hears you")**, listening (12 TTS), pronunciation/minimal-pairs (8), daily 5/10/20, review (box system, honest "not clinical SRS"), placement (honest "not certified").

Modes: `practice`, `daily`, `review`, `placement`, `speak`. Browser-local mastery box (`ekguru_mastery_v1`), empty-review state, shuffled runs, computer-voice TTS with explicit caveat. No automatic pronunciation scoring, no certification claims anywhere.

---

## 5. Admin — Learn Ops (new `admin.html` tab + `js/admin-learn-ops.js`)

One tab, nine sub-panels, all reading the same data files the learner pages read (no second copy of the truth):

1. **Dashboard** — counts + quality grade distribution + top issues.
2. **Learning graph** — PATH→MODULE→LESSON→PRACTICE→QUIZ→REVIEW with cycle / dead-end / missing-prerequisite / broken-lesson detection (every lesson URL cross-checked against the inventory).
3. **Practice bank** — 112 items with duplicate / ambiguous / wrong-key / missing-explanation / answer-not-in-options checks (all GREEN).
4. **Tool control centre** — 13 tools with status (driven by the QA JSON, not claims), version, category, owner, last tested, overflow (1280/390), deps, fallback; **Disable = confirmation + audit log** (`ekguru_tool_audit_v1`, clearly labelled as audit-only, does not change the live site).
5. **Content quality** — full 109-page inventory, weakest first, per-page score breakdown. Labelled "internal score — NOT a Google ranking".
6. **Gap engine** — QUERY → existing page? → existing tool? → quality? → coverage? → action (IMPROVE / IMPROVE-add-tool-link / IMPROVE-add-practice / CREATE TOOL / CREATE PRACTICE / COVERED), with IDF-weighted rarity ranking so "time" outranks "hindi". Decision aid only — **never generates pages**.
7. **Content editor** — edit a bank item and **Export/Copy JSON patch** (static site: honest export model, no fake server write).
8. **Health board** — Learn/Tools/Questions/Practice/Search/Tutors/Booking/Contact/Email/Sheets/Apps Script/Sitemap/Robots/Ads.txt/JS errors/Performance with GREEN/YELLOW/RED/**UNKNOWN**; Unknown is never green.
9. **One-click diagnostics** — runs every local check and prints a report (all GREEN except "weak pages <65 = YELLOW 21", which is honest).

Tool metadata registry: `js/tool-registry.js`. Admin QA results are fetched same-origin from `reports/tool-functional-qa.json` at runtime (graceful UNKNOWN fallback). `admin.html` remains `noindex,nofollow,noarchive`.

---

## 6. Search / content gaps

- Romanisation search fixed in 3 tools (§2).
- Gap engine surfaces real gaps: e.g. "hindi verb conjugation" → flags `conjugation` uncovered (verb tool covers it, but the word doesn't appear — a copy-improvement signal); "travel phrases for taxi" → flags `taxi` uncovered.
- Known linkage gap the engine surfaces: **answer pages have `links_tool: 0`** — the Google→answer→tool step of the free-value loop is thin on the 29 answer pages.

---

## 7. Mobile / desktop / accessibility / performance

- **Viewport QA (real browser, `getBoundingClientRect`/scrollWidth):** 8 new pages × {320,360,390,430,768,1024,1280,1366,1440,1536,1920} → **0 overflow**. Admin Learn Ops at 390px → 0 overflow.
- **Accessibility:** every generated page has exactly one `<h1>`, `lang="en"`, canonical, meta description; practice feedback uses `aria-live`, progress bar uses `role="progressbar"`, buttons have `aria-label`s, touch targets ≥44px, reduced-motion-friendly (no infinite animation).
- **Performance:** static HTML + small deferred JS (bank 28KB, engine 20KB, paths 20KB); no new dependencies, no CDN, no network calls in labs. Honest note: full TTFB/LCP/INP/CLS web-vitals crawl was **not** re-run this turn — the health board marks Performance UNKNOWN rather than claiming a number.
- **SEO:** sitemap 585 URLs, 575 pages, **0 broken links, 0 orphans**; unique title/description/H1/canonical per page; Course schema on paths, WebApplication schema on labs; hreflang intentionally omitted (monolingual English site — adding it would be redundant); admin + noindex; no random-quiz-state URLs.

---

## 8. P0 student booking email — status (unchanged, not weakened)

- Still blocked on the owner-wired token: `sendable() = false`, reason **"client token (mail.appsScript.token) empty; server token IS minted (doGet → configured:true)"**.
- No code touched this turn: `js/mailer.js`, `js/store.js`, `js/ledger.js`, `js/site-config.js`, `admin.html` mail tabs unchanged.
- Real two-student mailbox test remains **pending the owner wiring `MAILER_SHARED_TOKEN`**; until a real student inbox receives a message, the status stays blocked — no DELIVERED/ACCEPTED claim is made.
- Evidence kept in `reports/student-email-delivery-audit.json` and `reports/student-email-probe-fresh.json`.

## 9. Header

- **LOCAL_VERIFIED:** doctor geometry check clean at **17 widths, 0 failures**; before/after screenshots in `tools/header-measure/`.
- **LIVE_VERIFIED: NO** — not deployed (push blocked, §10). Per the standing rule, the fix is only "live" after a real deployment + screenshot.

---

## 10. Release & regression

**Local regression run (all green):**
- `node tools/doctor.js` → **11 checks, 0 problems, 0 warnings, PASS** (includes privacy, header geometry, 575-page link check, ads.txt/robots/canonical, sheets guard).
- `node tools/seocheck.js` → **PASS** (575 pages, 21965 links, 0 broken, 0 orphans, 585 sitemap URLs).
- `node tools/privacy.js` → **PASS** (0 secrets, 65 sensitive [pre-existing header-measure JSON], 0 blocked).
- `python3 tools/test-tools-functional.py` → **12/12 PASS**.
- Playwright: paths + 12 labs + hub + admin Learn Ops (9 sub-panels) all render with **0 console/page errors**.

**Deployment:** GitHub remote re-added (`https://github.com/ekgurulearning/EkGuru.git`). Remote `main` is force-reset to `5d84004` (no shared merge-base). Push fails: **"could not read Username for 'https://github.com' — No such device or address"** (no authenticated credentials in sandbox). **No deployment is claimed.** Live verification of the Learn/Tools/Admin work is not possible from this environment.

---

## 11. Exact files changed

**New:** `js/learning-paths.js`, `js/practice-bank.js`, `js/practice-engine.js`, `js/path-progress.js`, `js/admin-learn-ops.js`, `js/tool-registry.js`, `js/learn-quality.js` (generated); `learn/paths/{index,hindi-from-zero,speaking-starter,reading-hindi,travel-hindi,everyday-hindi,grammar-foundations}/index.html`; `learn/practice/{index,vocabulary,grammar,sentence-builder,verbs,reading,writing,speaking,listening,pronunciation,daily,review,placement}/index.html` (all generated — do not hand-edit, regenerate via `python3 tools/build-learn.py`); `tools/build-learn.py`, `tools/learn-tools-audit.py`, `tools/test-tools-functional.py`; `reports/learn-tools-quality-baseline.json`, `reports/tool-functional-qa.json`.

**Modified:** `admin.html` (Learn Ops tab + section + script includes), `learn/index.html` (paths + practice entry points), `toolbox/hindi-verbs/index.html`, `toolbox/hindi-vocabulary/index.html`, `toolbox/hindi-phrasebook/index.html` (romanisation search), `sitemap-learn.xml` (regenerated), `js/admin-stats.js` + `reports/{doctor,privacy-scan,seo}.json` (regenerated by the gates).

## 12. Commands

```
python3 tools/build-learn.py                  # regenerate paths, labs, sitemap-learn.xml
python3 tools/learn-tools-audit.py            # regenerate baseline + js/learn-quality.js
python3 tools/test-tools-functional.py        # 12/12 PASS
node tools/doctor.js                          # 11/11 PASS
node tools/seocheck.js                        # PASS
node tools/privacy.js                         # PASS
```

## 13. Honest status summary

| Area | State |
|---|---|
| Learner intents → answer/tool/practice flows | Strong for core intents (alphabet, greetings, numbers, verbs, vocab, travel, grammar, placement) |
| Tools reliable | 12/12 PASS |
| Weak high-value pages | Improved lab/path shells; 21 sub-65 pages (answers) remain, listed in admin quality board |
| Admin can operate Learn/Tools without code edits | Yes for diagnosis/QA/audit; content edits are export-model (static site) |
| Learning graph critical gaps | None (0 cycles / dead ends / broken links) |
| Mobile/desktop/a11y/perf | 0 overflow at 11 sizes; a11y structure clean; perf not re-crawled (UNKNOWN, honestly) |
| Critical regressions | None (doctor/privacy/SEO/tools all PASS) |
| Student email | Still `BLOCKED_ON_TOKEN` — owner token wiring + real two-student test required |
| Header | LOCAL_VERIFIED; LIVE_VERIFIED pending deployment |
| Deployment | Not pushed (no credentials) — commit `4fe79de` |

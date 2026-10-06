# PHASE 9 — interactive tools, slice 1: flashcards (2 October 2026 command)

**Branch:** `arena/01a102f8-ekguru` · **Date:** 4 Oct 2026
**Command source:** `Arena latest command  arena/Arena latest command  arena/01a0e655-ekguru/after fasst.md` — PHASE 9
**Scope of this slice:** cards + the surface that studies them. The rest of PHASE 9 (worksheets,
typing per script, practice-exercise surfaces, the custom deck builder) is listed under *Still open*
with the exact state of the data, so the next session starts from facts, not from a summary.

---

## 1. What PHASE 9 asked for, and what this slice delivers

| PHASE 9 gate | State after this slice | Evidence |
|---|---|---|
| `data/flashcards/[code].json` per language | **Built** — 38 decks (every language that authors vocabulary) | `data/flashcards/*.json` |
| ≥ 200 flashcards per published language | **Met for the 38 languages with course content**: min 288, max 300 (cap), total 11,232 | `data/quality/flashcard-coverage.json` |
| Front native script / back romanisation + meaning + reading | **Built** — front = authored target, back = authored English gloss, reading line kept separate | `tools/lib/flashcard_section.py` |
| SRS scheduling | **Wired** — “＋ Add to review” calls the one shared store `js/global-srs.js` (`EkGuruGlobalSRS.add`), no second scheduler | `js/flashcard-ui.js` |
| Categories (greetings, numbers, food, travel, family, body, colours, verbs…) | **Built** — 13 categories, filter chips with counts, from the authored part of speech + lesson title | deck `categories` |
| Flip animation + `prefers-reduced-motion` | **Built** — animation only under `(prefers-reduced-motion: no-preference)`; the card also carries `data-reduced-motion` | `css/experience.css` §37 |
| Progress tracking (localStorage) | **Built** — `ekguru:flashcards:<lang>:v1` (seen count, saved cards), try/catch for private mode | `js/flashcard-ui.js` |
| Every published language | **Not yet** — the registry has 89 published languages; 38 author vocabulary today. The other 51 are PHASE 8 (expansion) work; a language is never given a deck it cannot fill | §4 |
| `python3 tools/build-flashcards.py` | **Built**, with `--check` | this report §3 |
| `build-all.py check` green | Registered; the full chain cannot run in this sandbox (no network for `sheetsync`), every gate was run individually | §3 |

## 2. The 51 languages without a deck are reported, never padded

`tools/build-flashcards.py` copies authored vocabulary and nothing else. Card ids are stable
(`<code>.<level>.<target-slug>[-n]`), unique inside a deck, SRS-safe
(`[a-zA-Z0-9_.:-]{1,150}`, reserved words refused), and derived from the **target**, not the English
gloss — the expanded decks reuse a gloss across several targets (“discourse segment in …”), and a
gloss-only id silently dropped real vocabulary (it did, in the first build: 7,008 cards; the fix
raised it to 11,232 without inventing a single card).

Kannada is the visible gap: `learn/kannada/practice/` exists with quiz, typing and worksheets, but
`data/courses/` has no `kn_*.json`, so there is no deck and **no lab is injected**. The injector skips
it and this report records it; the fix belongs to PHASE 8 (Kannada course data), not to a padded deck.

## 3. What was built

| File | Role |
|---|---|
| `tools/build-flashcards.py` | deck builder; `--check` exits 1 on drift. Cap 300 cards/language, level order A1→C2 first. Writes `data/flashcards/<code>.json`, `js/flashcards-<code>.js`, `data/quality/flashcard-coverage.json` |
| `js/flashcard-ui.js` | the lab: flip, arrow keys, category chips, shuffle, speak, add-to-review, progress. **No speech engine of its own** — playback goes through `js/voice.js` (js/ is allowed exactly one, enforced by `tools/test-voice.mjs`) |
| `tools/lib/flashcard_section.py` | the shared block: heading, honest note, 12 real cards rendered at build time (a crawler and a no-JS reader see the language's own vocabulary), `<noscript>` line |
| `tools/inject-flashcards.py` | idempotent injector (`--check`); marker pair `ekguru:flashcards:start/end`; skips any language without a deck |
| `css/experience.css` §37 | styles, bundled into `css/style.min.css` (231,400 B stylesheet, 122,508 B layer) |
| `tools/test-flashcards.mjs` | 24-check gate: deck sizes, ids, JSON↔JS parity, page wiring, and the lab in a real DOM (flip, keyboard, chips, SRS, no autoplay, reduced motion) |
| `tools/build-all.py` | registered in `ULTRA_BUILDS` (build + inject) and `ULTRA_TESTS` (test) |

**Surface:** `languages/<code>/practice/` (10 world courses) and `learn/<slug>/practice/` (9 Indian
languages) — 19 pages carry the lab. `build-world-course.py` also emits the block itself now, so a
future full rebuild produces the same page as the injector, and `inject-flashcards.py --check` stays
the guard.

## 4. Gates run (all individually; `build-all.py` needs network for `sheetsync`)

| Gate | Result |
|---|---|
| `node tools/test-flashcards.mjs` | **all checks passed** (24 checks) |
| `python3 tools/build-flashcards.py --check` / `inject-flashcards.py --check` | pass (38 decks · 11,232 cards · 38 ≥ 200 · 19 pages) |
| `python3 tools/test-voice.mjs` | **26/26** — including “voice.js is the only speech engine in js/”, which this slice had to satisfy by routing Speak through the shared provider |
| `python3 tools/bundle-experience-css.py --check` | pass (122,508 B layer) |
| `python3 tools/apply-ultra.py --check` · `test-ultra-integration.py` | 0 stale · 2687 pages, 0 problems |
| `python3 tools/inject-ads.py --check` · `node tools/test-ad-policy.mjs` | 2689 pages match the matrix · 22/22 (practice pages stay ad-free) |
| `node tools/test-googlebot-parity.mjs` | identical HTML for Googlebot and Chrome |
| `node tools/build-shell.js --check` | 2688 pages carry the same shell |
| `node tools/dedupe-script-tags.py --check` | no page loads the same script twice |
| `node tools/test-usability-home.mjs` · `test-experience-dom.mjs` | all checks passed |
| `node tools/test-retention.mjs` · `test-runtime-qa.mjs` · `test-browser-qa.mjs` | 20/20 · 142/0 · 26/0 |
| `node tools/test-course-levels.mjs` · `test-course-placeholders.mjs` | 29/0 · 7/0 |

## 5. Still open in PHASE 9 (facts, not estimates)

* **Worksheets** — `data/courses` already carries a per-lesson `worksheet` (107–115 lessons for the
  world courses); `tools/build-worksheets.py` and `data/worksheets/<code>/` do **not** exist yet.
  PHASE 14 (printables, A4) owns the print/PDF side; the tool must not duplicate the print sheet
  pipeline (`tools/build-print-sheets.py`, `test-print-sheets.mjs`) — reuse it.
* **Typing per script** — Indian languages have typing trainers (`learn/<slug>/practice/typing/`);
  Arabic, CJK, Cyrillic and Thai typing pages do not exist for the world courses.
* **Practice exercises ≥ 10 per topic** — **already satisfied in data**: 906 topics, min 24 items,
  median 24; the practice pages already render them (`js/practice-engine.js`).
* **Quiz ≥ 20 items per level** — **already satisfied in data**: 312 levels, min 30, median 40; the
  quiz pages already ship. Two focused `js/course-player.js` interaction slices now cover matching
  pairs and sentence reordering (`reports/PHASE9-MATCHING.md` and
  `reports/PHASE9-REORDER.md`). They do not complete the wider five-type requirement
  (fill-in-the-blank, matching, reorder, listening, reading), and they do not audit all practice
  engines or authored question diversity. Their coverage counts are schema/rendering measures, not
  native-speaker or linguistic approval; broader quiz work remains open.
* **Deck builder (custom decks, import, Anki export, share URL)** — not built.
* **`build-practice.py`** — not built; the practice pages are generator-owned
  (`build-world-course.py`, `build-language-course.py`, `build-learn.py`) and adding a fourth writer
  would create the duplicate-owner problem the repo has been burned by before.

## 6. Commands

```bash
python3 tools/build-flashcards.py          # write decks + coverage report
python3 tools/build-flashcards.py --check  # CI: exit 1 on drift
python3 tools/inject-flashcards.py         # put the lab on every practice page with a deck
python3 tools/inject-flashcards.py --check # CI: exit 1 on a missing/stale lab
node tools/test-flashcards.mjs             # the PHASE 9 gate for this slice
```

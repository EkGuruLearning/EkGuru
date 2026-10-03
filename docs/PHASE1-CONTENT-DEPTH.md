# PHASE 1 — content depth: every published language gets full levels

Scope note: PHASE 1 of the AdSense command says "har published language". That is
**18 courses**, not the 89 T1 courses the language gate audits. The other 71 are
already quarantined as research-only by `tools/quarantine-language-surfaces.py`
(noindex, `data-ad-class="RESEARCH_REQUIRED"`), so authoring them is a different
phase — PHASE 6 (add more languages), not this one.

Published (2026-10-03): `ar bn de es fr gu hi it ja ko mr pa pt ru ta te ur zh`.

## What "done" means, mechanically

The requirements are not invented in this doc — they are read out of the same
validator the language gate runs:

- `data/schemas/course-t1.schema.json` — the schema
- `tools/lib/validate-language-schema.mjs` — Ajv runner (Node), called by
  `tools/language-gate.py: run_schema()`

For a file `data/courses/<phase>/<code>_<rung>.json`:

| rule | value | today |
|---|---|---|
| top-level required | `code`, `name`, `file_level`, `level` | ok |
| `level.required` | `title`, `goals`, `units`, `test`, `extra` | **`extra` missing everywhere** |
| `level.units` | 3–5 items | ok (count varies) |
| `unit.required` | `id`, `title`, `lessons` | ok |
| `unit.lessons` | **3–5 items** | **2 everywhere** |
| `lesson.required` | `id`, `title`, `learn`, `vocab`, `grammar`, `dialogue`, `practice`, `quiz`, `worksheet` | ok |
| `test.items` | 10–20 | ok for the 18 published |
| `extra.required` | `culture`, `reading`, `listening`, `idioms`, `mistakes`, `task` | — |

Rungs (`tools/language-gate.py: RUNGS`):

```
A1  A1+  A2  A2+  B1  B1+  B2  B2+  C1  C1+  C2      # 11
```

Every published course carries 6 (`A1 A2 B1 B2 C1 C2`). The five legacy bridge
files `A3` (EkGuru A2→B1 bridge) and `B3` (B2→C1 bridge) already exist as
`INCOMPLETE` stubs and map cleanly onto `A2+` and `B2+`; `C3/C4/C5` are
post-C2 extensions with no CEFR equivalent and stay as they are.

## The measured gap

```
python3 tools/audit-phase1-gap.py            # report
python3 tools/audit-phase1-gap.py --check    # exit 1 while gaps remain
```

2026-10-03 (start): **90 rung files to author · 108 rung(s) missing `extra` ·
108 unit(s) short of the 3rd lesson**, spread evenly (5 rungs / 6 extras / 6
short units per language).

2026-10-03 (after the Hindi pilot): **90 rung files · 102 `extra` blocks · 108
short units**. Hindi's six CEFR rungs now carry the block:
`tools/author-hindi-levels.py` holds the authored content, and
`tools/build-course-levels.py` renders it (`extra_block()`), which the page
builder did not do before — until this change no course file carried `extra` and
no tool read it, so the schema had required a block that could not be seen.

2026-10-03 (after Japanese — 9 of 18): **65 rung files · 78 `extra` blocks · 78 short
units**. The nine authored courses (hi, ar, bn, de, es, fr, it, gu, ja) each read
`11/11` in the audit; the gate row for each is `FAIL ['no_native_review']` only —
`unique_text_ratio` 0.986 (hi) / 0.977 (ja) / 0.947 (gu) / 0.946 (ar) / 0.928 (es)
/ 0.919 (fr) / 0.918 (it) / 0.912 (bn) / 0.906 (de), `script_mismatch` 0 — against
0.85 for the flag, which is the mechanical part of "no templated intros"; native
review is the one reason that cannot be generated. The modules are
`tools/depth-content/{ar,bn,de,es,fr,gu,it,ja}.py`. Gujarati was the first
**phase-2** course to go through `tools/author-depth.py` — `course_dir()` globs
`data/courses/*/{code}_A1.json`, so the phase is resolved from the file it finds
rather than assumed, and all 12 new rung files landed in `data/courses/phase-2/`
with no change to the tool.

2026-10-03 (after Korean — 10 of 18): **40 rung files · 48 `extra` blocks · 48 short
units**. ko reads `11/11` in the audit; its gate row is `FAIL ['no_native_review']`
only, `unique_text_ratio` 0.976 and `script_mismatch` 0 against 0.85 and 0 for the
flags. Two defects surfaced while authoring it and were fixed rather than worked
around: the English speaker labels (see the fifth trap below) and a script range
too narrow to recognise Korean stem patterns (`tools/lib/text.py`, sixth trap).

The modules are `tools/depth-content/{ar,bn,de,es,fr,gu,it,ja,ko}.py`; the five
half-step rungs of ko pick their own themes — a day and a call, bank and phone
shop, CV and interview, contract and negotiation, synthesis and citation — so
that no theme is shared with ja.

The audit also counts a content defect the schema cannot see: an English speaker
label in a dialogue of a course taught in another language. The factory left the
four C1/C2 roles in English (`Analyst`, `Editor`, `Mediator`, `Reviewer`) in
twelve courses, and in Gujarati it left English labels through A1-B2 as well,
while the same files label other lessons natively and the Hindi pilot labelled
every role natively — so one course showed two languages side by side in the same
dialogue block. All thirteen shipped/queued courses whose files were mixed are
now fully native (672 dialogue lines re-labelled). Marathi followed in its own
pass — 144 `sp` labels and the ten practice prompts that named the same speakers
— and the sweep's leftovers went with it: fourteen Gujarati practice prompts and
four German labels (two in a C2 listening transcript, two in a C2 dialogue). The
four courses that are still English throughout (pa, ta, te, ur — 308 labels) are
fixed as each is authored, and the audit keeps counting them until then.

Six traps worth recording, all found while authoring the first ten languages:

- the gate's capitalised `\bTODO\b` marker matched Spanish `TODO` inside
  all-caps emphasis (`SIGA TODO RECTO`, `POR TODO LO ANTERIOR`, `EN TODO CASO`)
  and failed the whole course with `placeholder_text`. The content module now
  keeps `todo` lowercase inside emphasised phrases, and
  `grep -E '\bTODO\b|\bTBD\b' data/courses/**/*.json` must stay empty after
  every Spanish run.
- `build-course-levels.py`'s `worksheet_block()` used to splice the task rows
  into its table template and then apply one `%`-format to the whole string, so
  a worksheet key containing a percent sign (French `en hausse de 4 %`) made the
  builder abort with `TypeError: not enough arguments for format string`
  mid-run, leaving the level pages half written. The heading is now formatted
  before the rows are spliced in, which is output-neutral for every other
  language.
- **a `mistakes` entry whose `wrong` text was itself correct.** French carried
  `Je travaille dans la logistique depuis trois ans ✓`, `Il a été convenu que
  Léa coordonne (correct) ✓` and a Spanish `¿Cuánto cuesta el alquiler al
  mes? ✓`, each paired with a `why` that opened "Correct as written" or "Both
  are correct". Every automated walk passed — the schema, the word counts, the
  worksheet lengths — because the defect lives in the teaching, not the shape:
  an exercise that shows a correct sentence as the error teaches nothing.
  `tools/audit-phase1-gap.py` now walks every `{wrong,right,why}` object in the
  rung files, counts a `✓`/`(correct)`/`(fine)` inside `wrong` or one of those
  `why` openings as a PHASE 1 gap, and lists the offending path. Author run,
  schema walk and audit must all be clean before a language lands; the six
  entries in es and fr were rewritten as genuine errors in the same pass.

Each remaining language costs **6 `extra` blocks, 18 third lessons and 5
half-step rung files** (45 lessons). One language per commit, end to end:
content module → `author-depth.py --lang <code>` → the level-page recipe → the
stale chain → `build-all.py check` → gate + audit → commit.

- **A fabricated BCP-47 region tag.** `tools/build-lang-packs.py` defaulted a
  missing speech tag to `code + "-" + code.upper()`, writing `ja-JA`, `ko-KO`,
  `uk-UK` and `vi-VI` into `data/language-packs.json`. The language registry
  prefers a pack tag over `js/course-player.js`'s (correct) `TTS_LANG`, so the
  invented regions reached `js/voice-languages.js` and every page that inlines
  it — a device-voice request no browser can match, with no gate failing,
  because the tag is still shaped like a tag. The canonical map now lives in
  `tools/lib/speech_tags.py` and `speech_tag()` falls back to the bare language
  code (valid BCP-47) instead of inventing a region; `build-lang-packs.py`,
  `build-world-course.py`, `build-phase7-registries.py` and
  `test-phase7c-stage7.py` all use it. `build-voice-languages.py` also corrects
  an existing *empty* manifest whose `lang` drifted — a manifest with entries is
  owner-supplied and is reported, never rewritten.
## Acceptance (from the command doc)

- `python3 tools/build-all.py check` green
- every language has at least A1–B2 published
- every level page carries **500+ words of unique content**
- voice tags on all vocabulary items
- **no templated intros** — every page's opening paragraph differs

The last two are the reason this cannot be closed by schema shape alone: the
existing course text is templated (`"...analyse or produce the <Language> model
with correct word order, negation, scope, and register"`), and the language gate
already flags five languages with `unique_text_below_85` for exactly that. A
generated file that satisfies the schema but repeats another language's
sentences is not a PHASE 1 completion — see PART F (golden rules) and the
"no templated intros" gate.

- **A speaker label is rendered content, not metadata.** `dialogue[].sp` is
  printed beside the line on the level page, so an English role word in a
  non-English dialogue is visible to the learner — and because only *some*
  lessons of a file were localised, the same page showed `Editor` in one block
  and `संपादक` in the next. It is invisible to every structural walk (the value
  is a non-empty string) and to the language gate (a Latin label is legal in
  German). `tools/audit-phase1-gap.py` now counts it against a closed vocabulary
  of factory role words, with a per-language allowlist for words that are also
  ordinary words of the target language (German `Reporter`, Portuguese
  `editor`), so names such as `Lena` or `Ana` are never flagged. Fix the module
  (`D("…")` labels and the `listening=` transcript, never the English
  `listening_gloss`) and re-run `tools/author-depth.py` for half-steps; the CEFR
  rungs are hand-maintained data and are edited directly.

  Repair, for the courses that still ship those labels: `tools/localise-speaker-labels.py
  --lang <code>` rewrites `sp` and the practice prompt that names the same speaker from a
  per-language role map. The English gloss of a line is not a label and stays English, and a map
  that would merge two speakers of one dialogue into one word is refused (Writer and Author are
  both લેખક). Marathi went first — 144 labels and 10 prompts — which took the audit count from
  452 English labels to 308 (pa 48 · ta 104 · te 128 · ur 28).

- **A script range that is too narrow fails correct content.** `in_script()` in
  `tools/lib/text.py` decides whether a vocabulary entry is written in the
  language's own script, and its Hangul range held only precomposed syllables
  and conjoining jamo. Korean grammar patterns are written with the
  compatibility jamo block — `-(으)ㄹ 거예요`, `-ㄴ 셈이다` — so the gate reported
  four script mismatches against correct Korean, and the tempting repair was to
  rewrite the content. The range was extended instead, in the same spirit as the
  Latn entry above it that had to grow for Uzbek `oʻ`, and `--selftest` now
  covers Hangul syllables, a compat-jamo pattern, and Latin failing Hangul.

## What the pilot settled

- The `extra` block renders as a real page section: culture note (source **named,
  not linked** — the public surface is closed to outbound hosts outside the
  calibrated allowlist in `tools/test-no-competitor-attribution.js`), an
  original reading text with a plain-English gloss, a listening script tagged
  `hi-IN`, ten idioms, the level's own mistakes, and a task.
- Level-page word counts rose by roughly 600 words each: Hindi A1 6,799 →
  7,310, B2 7,149 → 7,814, C2 10,401 → 10,768.
- The language gate's `t1:extra_content_missing` reason is gone for Hindi.
- Level pages are regenerated with **docs/REGENERATING-LEVEL-PAGES.md**, not the
  course recipe: `apply-ultra --strip` → `build-course-levels` → `inject-ads` →
  `build-legacy-pages` (before the shell) → `build-page-layer` → `build-shell` →
  `dedupe-script-tags` → `apply-ultra`, then the copy-index window and
  `update-editorial-metadata`, then `git checkout -- 'languages/*/level/index.html'`
  for the 18 known `twitter:title` ladder pages. Running `build-course-levels`
  twice, or without `build-legacy-pages`, silently drops the shell or the
  `pw-bands`.
- After any `data/courses/**` change, `data/quality/language-gate.json` must be
  regenerated (`python3 tools/language-gate.py`) or `build-all.py check` stops on
  the stale gate report.

## The half-step rungs (A1+ A2+ B1+ B2+ C1+)

The eleven rungs are the six CEFR levels plus the half-step after each of the
first five; `data/levels.json` argues for them (A1+ is what language schools
write) and every CEFR level page already describes its own half-step in the
"After A1: the A1+ checkpoint" section. What was missing was the data.

A half-step rung file is a **level, not a page stub**: the player resolves
`data/courses/<phase>/<code>_<level>.json` by name (js/course-player.js
`fetchLevel`), so authoring the file makes it playable at `/courses/#/hi/A1+`
while the static level pages stay the six CEFR ones. Two things follow:

- `hi.levels` in `data/courses/index.json` keeps the six CEFR keys — that dict
  drives hub link rendering, and a level with no page would produce a dead link.
  Only `hi.files` lists the half-step, which is a manifest of what is on disk.
- Building static pages for half-steps is a separate decision (paths like
  `languages/hi/level/a1p/`, rails, ladder links). It is not needed for the rung
  to be real and playable.

`tools/build-courses.py` (the legacy six-level validator) learned the half-step
filenames so a real A1+ file stops being reported as a filename error. It still
exits 1 on the pre-existing `A3/B3/C3/C4/C5` extension files, so its manifest
write does not run; the manifest entry is maintained by hand until that is fixed.

Authoring is `tools/author-hindi-halfsteps.py` (see the pattern for adding the
next rung to `HALF_STEPS`).

## Doing it for the other languages

Hindi has hand-written tools because it was the pilot. Everything after it is
data-driven:

```
tools/depth_kit.py            # the authoring DSL (V/X/G/D/T/WS/L/EXTRA)
tools/author-depth.py         # the machinery, per language:
                              #   python3 tools/author-depth.py --lang ar
                              #   ... --check            drift report
                              #   ... --only extras|third|rungs|manifest
tools/depth-content/<code>.py # the content: EXTRAS, THIRD, HALFSTEPS
```

One command writes all three surfaces: the five half-step rungs (as real level
files, playable at `/courses/#/<code>/A1+`), the `extra` block on the six CEFR
rungs, a third lesson in every unit, and the `files` / lesson-count fields in
`data/courses/index.json`. The lesson expansion (twelve practice types, quiz,
worksheet, SRS) lives in the tool, so a new language is content only.

Arabic went first (`tools/depth-content/ar.py`): A1 6/11 → 11/11, `extra` on all
six rungs, a third lesson in all eighteen units, `unique_text_ratio` 0.911 →
0.965. Its level pages were regenerated with the recipe above — adding `extra`
changes what the pages render, so a language is not finished until
`python3 tools/build-course-levels.py --check` says 0 stale, and
`python3 tools/build-all.py check` is green.

Two things to keep in the same commit as a language: the regenerated level
pages (the ladder page's lesson/word/question counts move — ar went 24 → 36
lessons) and `python3 tools/build-learning-data.py`, which rebuilds
`data/learning/` from the course files and is checked separately.

## Work order

1. One language end to end as a pilot: author `A1+`, patch the five existing
   rungs (`extra` + a third lesson per unit), then run
   `python3 tools/audit-phase1-gap.py` and `python3 tools/build-all.py check`.
2. Repeat per language; keep each language one commit.
3. Convert the A3/B3 bridges into real `A2+`/`B2+` rungs once their content is
   authored, rather than shipping the stubs under a new name.
4. After any `data/courses/**` change, regenerate the pages that read it
   (`tools/build-course-levels.py`, then the rest of the documented order) and
   re-run the gates.

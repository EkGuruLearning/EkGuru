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

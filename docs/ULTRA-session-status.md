# ULTRA v3 current session

Branch `arena/01a0f33e-ekguru`, original commit `bc8c0bd09e01100fbe04c465748aa417bd905925`.
**No merge. Existing indexing/canonicals frozen. Ads and advertising consent OFF. No fake review/approval/source verification. New drafts noindex.**

## Workspace reconciliation — 1 October 2026

On each interrupted continuation the checkout had returned to the original commit and did not contain the previously described runtime/tests/generated assets. These earlier test/browser claims are not current acceptance evidence. The cause is unknown; no workspace-loss diagnosis is asserted. Source-only bounded checkpoints are now being saved with completed turns, avoiding bulk generated HTML.

U0 PR #21 was verified MERGED by read-only GitHub access. Real inactive tutor rows are not changed. No commit/push/PR/merge performed in this continuation.

`tools/ultra/contract.py --restore-original` reconstructs the missing original contract from the SAME immutable Git object (2636 pages / 1006 indexable), never a current-tree recapture. It refuses to overwrite an existing file. Normal operation is a read-only preservation test.

U1–U11 are NOT COMPLETE in this reconciled checkout. Reports must be regenerated, not copied from missing work. Native/editorial evidence, source years, account approval, live field CWV, mobile/cross-engine validation and visual approval remain unverified. Code/report freshness never means editorial/AdSense acceptance.

## AdSense v4 session — branch `arena/01a0ff98-ekguru`, 3 October 2026

34 commits, PR **#24** open against `main`. PHASE 3 (long-form Learn posts) is
closed, and PHASE 1 (content depth) is authored for **12 of the 18** published
languages — `hi ar bn de es fr it gu ja ko mr pa` — each with six `extra`
blocks, a third lesson in every unit and the five half-step rungs A1+ … C1+, so
every authored course now carries 11 of the 11 CEFR rungs.

Local gates at the branch tip (`2f931b7`): `build-all.py check` green,
course-levels 29/0, placeholders 7/0, ad-policy 22/0, `inject-ads.py --check`
ok, the PHASE 3 content gate PASS, registries PASS, page inventory 2690 pages
with `thin_indexable 0`.

CI on the PR: `journeys` PASS (46s); `checks` PASS (4m8s) on `68722f0`, then
**FAIL on the next, docs-only commit `98e1c41`** — the same single network check
both times: `[FAIL] Apps Script: reachable — The read operation timed out`
(`MODE=LIVE: 27 checks, 1 failures`). Every build, SEO and policy step before it
passed on both runs, and nothing in the branch touches that endpoint, so the
probe is flaky rather than the branch being broken. Fixed at the source rather
than re-run until green: `tools/test-data-sources.py` now retries that one probe
three times, 5s apart, prints the attempt it answered on, and still fails the run
if the endpoint never answers (verified against a stubbed flaky/dead/healthy
fetcher, not against the live host — the sandbox cannot reach it).

Two things worth keeping: a red `checks` job is not by itself a content
regression — read the annotation first (`gh api
repos/<repo>/check-runs/<id>/annotations`), which names the failing check and its
reason; and the token here cannot re-run a job (`POST
.../rerun-failed-jobs` → 403), so the only way to retrigger CI is a push.

Still open by design: `no_native_review` for every T1 language (an owner-verified
review record is not something a generator may invent), PHASE 1 for
`pt ru ta te ur zh`, and the prose-rewrite polish pass. Runtime flags OFF;
indexing and canonicals untouched.

## Defect found on the live site after the merge — 3 October 2026

The merge was followed by reading the deployed page rather than trusting the
gates, and `https://ekguru.shop/languages/pa/level/a1/` was printing this to
readers:

```html
<li>{'wrong': 'ਤੂੰ ਕਿੱਥੇ ਰਹਿੰਦਾ ਹੈ?', 'right': '…', 'why': '…'}</li>
```

A Python dictionary literal, in a "Watch out:" list. 58 level pages of 13
languages carried it (6 each for `es fr gu mr pa`, 4 each for
`ar bn de it ja ko`, 2 each for `te zh`) — and 12 of the 18 gates stayed green
while it shipped, which is the part worth remembering.

**Cause.** `grammar.mistakes` is a list of plain strings in the older courses and
of `{wrong, right, why}` objects in everything authored since — 2,295 objects to
1,218 strings, plus 400 object rows in `level.extra.mistakes`. The extra
renderer (`tools/build-course-levels.py`, `extra_block`) has always known both
shapes; the grammar box did not, and sent every item through `_clean()`, so a
dict became `str(dict)`. The JSON was valid, the schema and audit gates read the
JSON, the rendered HTML was valid and the words were on the page: nothing in the
pipeline compares what the reader sees with what the lesson says.

**Fix.** One formatter, `mistake_row()` in the same file, now serves both
renderers; object rows print `<b>wrong</b> → right <span class="muted">why</span>`
and string rows are byte-identical to before. Regenerated with the documented
level-page recipe, so the 58 pages are generated output, not hand edits.

**Gate.** `tools/test-course-levels.mjs` (runs in `build-all.py check` and in CI)
now reads the rendered page against the course file, row by row: no page may
print a Python literal, and every authored `{wrong, right, why}` row — grammar
and extra — must appear on its page exactly as the lesson writes it. 556 rows
across 64 pages are checked. Both halves were proofed by mutating a page until
they failed (a row turned back into a literal; a row deleted) and restoring it
byte-for-byte.

**Still open from the same live read:** the practice prompts on the deployed
Punjabi A1 page print IAST (`main ṭhīk hān! te tusīn?`) while the same page's
vocabulary column uses plain ASCII (`main theek haan`) — the two-romanisation
trap again, this time inside generated practice text. Fixing it means deciding
which scheme is canonical and teaching the drills to use it, which is a content
decision, not a formatter bug.

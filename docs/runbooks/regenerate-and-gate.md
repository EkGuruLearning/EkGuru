# Runbook: regenerate pages and pass the master gate

Use this after any change to a generator, a generator's source data, or a
page that a generator also writes. The gate is the only thing that decides
whether a change can merge:

```bash
python3 tools/build-all.py check     # exit 0 = green
```

## Why a fixed order

Several generators rewrite each other's output, and the decorative "ultra"
layer is added on top of pages after they are generated. Running a generator
on pages that still carry the layer, or the layer step on pages that have
none, drops it from hundreds of files. The cure is to work in the **stripped
state** and re-decorate once, at the end.

## The sequence

Run from the repository root. Do every step, in this order.

```bash
python3 tools/apply-ultra.py --strip              # 1. remove the decorative layer
# 2. run the generator(s) you changed here, in the stripped state
#    e.g. python3 tools/build-course-levels.py
node    tools/build-copy-index.js                 # 3. rebuild the copy index
python3 tools/apply-ultra.py                      # 4. re-apply the layer
python3 tools/build-full-page-inventory.py        # 5. page inventory (SEO, sitemap, noindex gates)
python3 tools/build-phase2-content-inventory.py   # 6. content inventory
python3 tools/build-phase3-originality-audit.py   # 7. originality audit
python3 tools/update-editorial-metadata.py        # 8. editorial metadata
python3 tools/build-all.py check                  # 9. the gate
```

For a hand edit to a page that no generator writes, steps 3 to 9 are enough.

## If it was interrupted

If a run stops between steps 1 and 4, `git status` shows hundreds of modified
files (pages left stripped). Do not commit that. Run the whole sequence again
from step 1. The modified count should fall back to the files you meant to
change.

## Reading a failure

| Symptom | Likely cause | Fix |
|---|---|---|
| Fingerprint or "generated layers are stale" | A generator was not re-run, or step order was broken | Re-run the sequence from step 1 |
| `reading-layer` page-count mismatch | Pages were added or removed | Update the count constant in `tools/test-reading-layer.mjs` |
| `contract.py` "new page must be noindex" | New page is indexable without owner approval | Make it noindex, or record approval (see `add-page-or-language.md`) |
| Editorial metadata or inventory stale | Step 5 to 8 skipped | Run them, then the gate again |
| Ultra head or `data-ad-class` missing on many pages | A generator ran on decorated pages | Re-run from step 1 |

Known generator cycles are listed in
[`../architecture/known-cycles.md`](../architecture/known-cycles.md).

## Before you push

- `python3 tools/build-all.py check` exits 0 locally.
- `git status` shows only the files you intended.
- No personal data in the diff (emails, phone numbers, private Drive links).

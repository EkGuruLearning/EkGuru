# Regenerating the `languages/<code>/level/**` pages

`python3 tools/build-all.py` (the write path) starts with `tools/sheetsync.js`,
which needs the live published Google Sheet and credentials. On a checkout
without them the full pipeline stops at step one and writes nothing, so a
generator change that touches course level pages cannot be applied the normal
way.

The level pages are still reproducible. They are written by
`tools/build-course-levels.py`, and five other tools run after it and add the
layers it does not write itself. Run those six in this order.

```bash
python3 tools/apply-ultra.py --strip          # 1. peel the ultra decoration
python3 tools/build-course-levels.py          # 2. write the pages
python3 tools/inject-ads.py                   # 3. ad loader / data-ad-class
python3 tools/build-legacy-pages.py           # 4. pw-bands  (BEFORE the shell)
python3 tools/build-page-layer.py             # 5. page layer
node   tools/build-shell.js                   # 6. header + footer
python3 tools/dedupe-script-tags.py           # 7. duplicate <script> tags
python3 tools/apply-ultra.py                  # 8. re-apply the decoration
```

Then rebuild the two derived indexes, each in the phase it is checked in:

```bash
python3 tools/apply-ultra.py --strip
node tools/build-copy-index.js                # checked against STRIPPED pages
python3 tools/apply-ultra.py
python3 tools/update-editorial-metadata.py    # checked against DECORATED pages
python3 tools/build-all.py check              # must end "generated layers are current"
```

## The two orderings that matter

**`build-legacy-pages.py` must run before `build-shell.js`.** It splices the
`ekguru:pw-bands` block at `band_anchor()`, which returns the position of the
`ekguru:shell-footer` marker if that marker exists and otherwise falls back to
its own in-`<main>` anchors. Run it after the shell and every band lands *after*
`</main>` instead of inside it — 1068 pages wrong in one step, with no error.

**`build-copy-index.js` is checked against the stripped pages**, so it has to be
rebuilt while the ultra decoration is off. `update-editorial-metadata.py` is the
opposite: it runs in `ULTRA_TESTS`, after the decoration is restored.

`tools/inject-consent.py` is *not* part of this sequence. The committed level
pages carry no `ekguru:consent` marker, and running it adds one.

## A page that is richer than its generator

`tools/build-phase7-pages.py` owns `languages/index.html`,
`languages/<code>/index.html` and `start/index.html`, and it writes them raw —
the shell and the ultra decoration are added by the sequence above. If a
committed page carries content the generator does not produce, rerunning it
deletes that content silently: no marker, no error, no gate.

That is what happened to `/start/`: the page's crawlable rule set (written
because the onboarding form is JavaScript) was hand-added, the generator still
held only its short template, and one regeneration took the page from 606 to 228
words. Every gate stayed green — the page is valid and indexable — and the only
symptom was `thin_indexable` 0 → 1 in `tools/build-full-page-inventory.py`.

Before regenerating one of those pages, compare its visible word count with the
generator's output. If the page has more, the content belongs in the generator
(`START_RULE_SET` in `tools/build-phase7-pages.py` is the repaired example);
never re-add it to the HTML.

## Verifying a recipe like this

Strip and decorate are a lossless round trip, so you can prove the sequence
before you rely on it: apply no change, run the whole sequence, and
`git status --short` must come back empty.

```bash
python3 tools/apply-ultra.py --strip && python3 tools/apply-ultra.py
git status --short        # must be empty
```

Doing that is what found both orderings above.

## Known residual difference

Running the sequence on an unmodified checkout leaves exactly 18 files dirty —
the published `languages/<code>/level/index.html` ladder pages — each differing
by one line:

```html
<!-- committed -->
<meta name="twitter:title" content="Arabic levels — A1, A2, B1, B2 available | EkGuru">
<!-- regenerated -->
<meta name="twitter:title" content="Arabic levels — A1, A2, B1, B2 available">
```

The head template in `tools/build-hindi-pages.py` gives `<title>` and
`og:title` the `| EkGuru` suffix but leaves `twitter:title` bare, so the
regenerated page drops a suffix the committed page has. Site-wide, 1080 pages
carry a `twitter:title` without the suffix and only 7 carry it with — the
consistent form is the one the 18 ladder pages have, and fixing it means
changing the shared head template and every page that uses it. That is a
separate decision, not a side effect of a content fix, so a change that has
nothing to do with the head should restore those 18 files rather than regress
them:

```bash
git checkout -- 'languages/*/level/index.html'
```

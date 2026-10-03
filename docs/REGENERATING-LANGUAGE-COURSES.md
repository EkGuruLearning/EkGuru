# Regenerating the `learn/<slug>/**` language courses

The nine Indian-language courses under `learn/<slug>/` (bengali, gujarati,
kannada, malayalam, marathi, punjabi, tamil, telugu, urdu) are written by
`tools/build-language-course.py` from `tools/lang-data/<slug>.json`. That tool
writes *only* its own content — the layers every page needs (ad class, page
layer, shell, ultra decoration, the baked worksheet sample) come from the tools
that run after it, which is why running the generator alone "breaks" a course.

`python3 tools/build-all.py` (the write path) cannot run in a checkout without
the live Google Sheet, so the reproduction order below is the way to apply a
generator change. It is the order in `tools/build-all.py`'s write path, cut down
to the steps that touch these pages.

```bash
# 0. start from a clean tree for the surfaces you are not changing
git checkout -- 'languages/'

python3 tools/apply-ultra.py --strip           # 1. peel the decoration
for s in bengali gujarati kannada malayalam marathi punjabi tamil telugu urdu; do
  python3 tools/build-language-course.py $s    # 2. write the course + quiz bank
done
python3 tools/inject-ads.py                    # 3. ad class + loader (policy gate)
python3 tools/quarantine-country-funnels.py    # 4. research quarantine (see below)
python3 tools/quarantine-language-surfaces.py  # 5. publication quarantine
python3 tools/inject-storybook.py              # 6. data-topic="lang-<slug>" + chapters
git checkout -- 'languages/'                   # 7. drop step 6's level-page edits
python3 tools/build-legacy-pages.py            # 8. reading layer / pw-bands
python3 tools/build-page-layer.py              # 9. page layer
python3 tools/build-visuals.py                 # 10. level visuals
python3 tools/build-print-sheets.py            # 11. bake the worksheet sample
python3 tools/inject-questions-api.py          # 12. votes on question pages
python3 tools/dedupe-script-tags.py            # 13. duplicate <script> tags
node   tools/build-shell.js                    # 14. header + footer
python3 tools/build-course-levels.py           # 15. the level rail inside each hub
git checkout -- 'languages/'                   # 16. undo step 15's level-page rewrite
python3 tools/build-sitemaps.py                # 17. sitemap supplement
python3 tools/build-search-index.py            # 18. search index
python3 tools/apply-ultra.py --strip           # 19. copy index is checked stripped
node   tools/build-copy-index.js               # 20. copy index
python3 tools/apply-ultra.py                   # 21. re-apply the decoration
python3 tools/update-editorial-metadata.py     # 22. own-content dates
python3 tools/build-all.py check               # must end "generated layers are current"
```

## The steps that are easy to miss, and what they cost

**`inject-storybook.py` (7) must run before `build-print-sheets.py` (12).**
It is what puts `data-topic="lang-<slug>"` on the page, which is how
`build-print-sheets.py` finds the language behind a worksheet and bakes five
real questions into `#ws-app`. Skip it and the worksheet prints nothing with
JavaScript off — `node tools/test-print-sheets.mjs` fails with "worksheets ship a
sheet in the file".

**Step 8 reverses step 7's side effect.** `inject-storybook.py` is a site-wide
pass: it also injects chapter blocks into `languages/<code>/level/**`, which the
committed tree does not carry. Reverting `languages/` afterwards keeps this
change scoped to the courses. (The generator's pages keep their chapters; the
level pages were never part of this phase.)

**`quarantine-country-funnels.py` (5) and `quarantine-language-surfaces.py` (6)
must run after `inject-ads.py` (4).** Both set `data-ad-class` and `robots` as a
quality decision, and the ad injector would overwrite the class. The country
funnel quarantine is what keeps `languages/<code>/level/**` at
`RESEARCH_REQUIRED` for unpublished courses — without it those 1068 pages show up
as dirty with an `INTERACTIVE_LEARNING` class.

**`build-copy-index.js` (20) runs in the stripped phase (19), before the decoration.**
`tools/build-all.py check` strips the ultra decoration before the legacy checks
and restores it afterwards, so an index built while decorated is stale the
moment the check looks at it. `update-editorial-metadata.py` (20) is the
opposite: it runs decorated.

**`build-course-levels.py` (15) has to run after the shell, not before it** — even
though `tools/build-all.py`'s write path lists it earlier. A regenerated hub is a
plain page with no `<main>` and no level-visuals strip, so `splice_rail()` finds no
anchor and reports "hub no anchor"; the rail only lands once the shell (14) and the
visuals (10) have written one. On an *already built* hub the rail is replaced
between its own markers, which is why the ordering never showed up before.

Step 15 also rewrites all 1068 level pages, dropping their layers. Nothing in this
phase touches those pages, so step 16 restores them from git — and that restore is
why the recipe starts from a clean `languages/` tree in the first place.

## Indexing: new pages stay noindex

`tools/ultra/contract.py` holds the owner's immutable index/noindex contract
against `data/quality/indexing-baseline.json` (2636 pages, 1006 indexable, from
commit `bc8c0bd`). Any file that is not in that baseline must be `noindex`, and
no existing page's `robots` or `canonical` may change.

So every new page added by the course generator goes in the generator's `NOINDEX`
set and carries `<meta name="robots" content="noindex, follow">`. Promoting them
is an owner decision, never a generator's. As of this writing that is the five
PHASE 3 posts per language: `common-words/`, `mistakes/`, `reading/`,
`vs-hindi/`, `speaking-alone/`.

## The phase test

```bash
python3 tools/test-phase3-content.py
```

Checks all ten PHASE 3 post types per language: page exists, ≥1000 words, one
`<main>` and one `<h1>`, at least four `<h2>` sections, links to at least two
other guides, is linked from its course hub, is noindex when it is a new page,
and has not changed the recorded indexability of a page that already existed.
It runs in CI after the master build check.

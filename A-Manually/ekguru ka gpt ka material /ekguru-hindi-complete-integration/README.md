# EkGuru Hindi — Complete Integration & Advanced Study Studio (draft)

This is the combined **offline development package**, not a production release. It combines the six previously delivered textbooks under their original `/learn/hindi/` paths. It adds a working cross-course Study Studio, a shared navigation layer and four links from the final academic lessons to the next books. No original curriculum is removed.

## Open the entire combined website

Extract ZIP, enter the package folder and run:

```sh
python3 -m http.server 8000 --directory site
```

Open `http://localhost:8000/learn/hindi/`, or `http://localhost:8000/learn/hindi/studio/`. The local Hindi index is only an offline launcher and is excluded from repository installation. The existing production Hindi V1 hub remains the real entry point. `preview.html` is a self-contained visual/interactive preview of Studio; its course links require the full site served at the correct route.

## What exists

- Five academic textbooks and one independent adult path: 240 chapters, 480 lessons, 240 worksheets, five adult stage assessments, 996 textbook HTML pages.
- 998 local HTML pages including Study Studio and offline launcher.
- 965 indexed chapter/lesson/worksheet/assessment routes; 2,513 study cards, deduplicated by book + Hindi + meaning (not 2,513 unique Hindi words globally).
- Search across Hindi/English titles, lesson words and meanings; adult entries also include Roman Hindi phrases. Filter by textbook, resource type or bookmarked resources. Show 24 results at a time.
- Self-rated revision with intervals of 10 minutes, 1, 3, 7, 21 days. Dictation with exact normalized text match, not automated language proficiency scoring. Audio uses device Hindi voice only.
- Read-only aggregation of existing textbook completion and last-lesson keys, preserving the existing progress schema. Studio saves its own bookmarks, review schedule and appearance settings separately. Export/import affects only Studio state, not learner drafts or existing progress.
- No dependencies added for site runtime, no accounts, paid services or backend.
- 511 identical file copies reconciled from the six input site trees; retained each unique path once. Six original reader engines are deliberately retained to avoid unverified regressions; common navigation and Studio are shared, not a fully unified engine.

## Build and tests

`python3 build.py` rebuilds the six original authored generators from `source/books` in a temporary staging tree and merges their outputs with seed assets. This updates the Studio index from the actual generated book manifests, without manual per-chapter HTML edits. `assets/` is the build seed, `site/` is output; only `site/` is potentially publishable. Existing illustrations are local vector artwork; art-generation scripts and design data are retained for future work, not executed by the build. Keep the package private or place it in an excluded repository development folder.

```sh
python3 build.py
python3 tests/test_integration.py
python3 tests/test_install.py
node --check source/studio.js
python3 tests/embedded_browser_test.py
```

Static integration suite: 7 tests passed (counts, every local link, cards, lesson IDs, SVG XML, shared nav, noindex). Installer: 2 tests passed. Embedded Chromium: search/filter, pagination, bookmark, revision, exact dictation, theme, text scale, progress aggregation via storage shim, safe backup import, nine widths, no-JS directory passed. `tests/browser_test.py` is the additional hosted test; this environment blocked navigation with ERR_BLOCKED_BY_ADMINISTRATOR. Real origin storage persistence and actual hosted navigation were NOT verified. No claims of live SEO or Core Web Vitals results.

## Integrate into the current EkGuru branch

1. Back up branch/working tree. Inspect existing owning generators, registry, canonical/indexing contract, and existing Hindi pages. Do not deploy the offline launcher.
2. Run `python3 install.py /path/to/EkGuru --keep-existing-roots` (read-only). It excludes the preview hub, retains differing existing course roots only when the flag is specified, and refuses all other differing paths. Already integrated older package pages will differ because of new shared navigation; reconcile them in the owning generators, not by overwriting the repo. Review the conflict report. No deletion or automatic registry mutation.
3. After conflicts are resolved and only expected new/identical paths remain, run the same command with `--apply`. Reconcile the retained course roots to link the actual new phase/stage pages. Register the integrated books using existing registry conventions (`existing`, not `published`, until approval). Add a clear Study Studio link to the Hindi V1 hub, and connect its existing practice/worksheet links to this page as appropriate. Preserve all legacy resources, progress and public routes. Do not replace the Hindi V1 hub with the offline launcher.
4. Integrate private source generators into the actual build pipeline. Source files and test fixtures must be excluded from the published artifact. Avoid running the package's standalone build in the repository root. Resolve shell/theme/reader integration in existing owners, preserving functionality.
5. Validate all original and new URLs/anchors and canonical tags, full build, browser navigation, a11y, print pages, storage, and actual device Hindi voices. Preserve the current indexing contract. All new pages are noindex. No auto sitemap expansion or ranking promise.

## Still required

Native-speaker editorial review of all textbooks, recorded audio, verified handwriting stroke order, all-repository legacy migration, common reader-engine consolidation, actual production shell and pipeline integration, separate language-specific SEO/GEO review and approved indexability. Adult course is an initial 40-chapter curriculum, not the previously suggested 200-chapter expanded adult pathway. Studio does not replace the need for those tasks.

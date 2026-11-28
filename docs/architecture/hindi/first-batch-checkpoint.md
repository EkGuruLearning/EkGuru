# Hindi textbook migration — first batch checkpoint

2026-11-28 · branch `arena/28510265-ekguru` · base `d8f572a63694dd03c9256bec04214114c7f9183c`

## What changed

Architecture preceded this navigation change: see `textbook-architecture.md` for fifteen diagrams and explicit distinctions between current implementation and intended system. The new read-only `tools/audit-hindi-textbook.py` generated `resource-inventory.json`: 950 heuristic HTML candidates and 78 name-matched source/assets. This is a starting snapshot, **not** the requested complete inventory. Inbound counts are from identified pages, not all of the site; asset identification, human editorial review, value and course assignment remain unresolved. Candidate URL actions currently preserve existing locations; no route is declared migrated or redundant based on this scan.

The root `/learn/hindi/` no longer puts the separate Academy home above an appended legacy directory. It presents existing Foundation, Beginner, Elementary, Intermediate and Advanced collections, then existing topics, guides, practice, materials, questions and optional tutors on the same page. It explicitly says the five new books are not complete and age-specific books are still needed. The old ten `#hh-*` links remain; Academy vowel practice, worksheet and answer links are retained in practice. `/learn/hindi/academy/` and its four existing child pages remain unchanged as compatibility-accessible static pages, **not** server redirects. The indexability/canonical policy of existing pages is unchanged. Existing stores are not rewritten.

## Scope and coverage

This is a navigation and discovery checkpoint, not a completed digital textbook. It does not implement the target Course → Phase → Chapter → Lesson model, kids or older-adults route, substantive new chapters, fully reviewed character coverage, complete Barakhadi, illustrated vocabulary, verified stroke order, recorded Hindi audio, new worksheets/answer keys, integrated search or cross-course resume. No native speaker or handwriting expert review was performed. The existing Foundation has 18 lessons and the earlier Academy registry lists 19 lessons including its draft vowel companion; these are not five complete courses. The earlier companion has one worksheet and separate answer page; the tracing surface is a visual self-check, not validated handwriting recognition. Its audio uses a supported device Hindi voice or an unavailable message, not an invented recording. No new illustration, audio recording or worksheet was created in this batch. Detailed pedagogical character and media coverage has not yet been audited.

## Validation executed for this batch

- `python3 tests/regression/test-hindi-textbook-hub.py`: 10 old fragment IDs exactly once, 9 priority routes present, 161 region links examined for local file existence. Other-page fragment targets and all site inbound links are not comprehensively checked.
- Real Chromium `tests/e2e/test-hindi-academy-browser.mjs`: widths 320, 375, 390, 430, 768, 1024, 1280, 1440, 1920; no horizontal overflow or page errors; existing catalogue filters, journal preservation, trace controls, print CSS and no-JS hub/compatibility catalogue checks. Hub screenshots reviewed at 390 and 1440 and saved in ignored `.artifacts/textbook-first-batch/`; on narrow screens the existing site-wide floating controls occupy considerable viewport space, which still needs reader-design work. This is not a full visual review of five textbooks or accessibility audit.
- `tools/build-hindi-hub.py --check`, `tools/build-page-layer.py --check` (1,760 pages), `tools/build-hindi-academy.py --check`, two Academy registry unit tests, `tests/regression/test-hindi-academy.mjs`, `tests/regression/test-phase3-content.py`, and `git diff --check`: passed. Page-layer check was initially run while a concurrently created `_site` was present and reported 32 artifact copies as stale; after removing that generated artifact, it passed.
- `tools/build-public-dist.py` rebuilt 5,512 files. Confirmed hub included and `docs/` excluded. `_site` was removed afterwards to avoid interfering with repository-wide scanners; no deployment occurred. A complete build/check and full browser/accessibility/content audit have **not** been rerun for this new batch.

## Before → after URLs

- `/learn/hindi/` → same URL, primary discovery page; no canonical change.
- `/learn/hindi/{foundation,beginner,elementary,intermediate,advanced}/` → same URLs, exposed as existing material, not newly authored books.
- `/learn/hindi/academy/`, `/learn/hindi/academy/{catalogue,vowels,worksheet,answers}/` → same URLs and current content, retained for compatibility. Their future target mapping and canonical strategy require review.
- `/hindi/` → existing static meta refresh/canonical to `/learn/hindi/#hh-topics`; unchanged by this batch.
- `/learn/hindi/{kids,older-adults}/` → not yet implemented. No fake route is published.
- All other identified candidates → same URL pending review. This is a conservative identity mapping, not a complete old-to-new migration plan.

## Changed files

New or updated in this batch: `tools/audit-hindi-textbook.py`, `docs/architecture/hindi/resource-inventory.json`, `docs/architecture/hindi/textbook-architecture.md`, `docs/architecture/hindi/first-batch-checkpoint.md`, `tools/build-hindi-hub.py`, generated `learn/hindi/index.html` and `hindi/index.html`, `tests/regression/test-hindi-textbook-hub.py`, `tests/e2e/test-hindi-academy-browser.mjs`, `tools/build-all.py`. The topic-index change is the generator's shared inline CSS only. Earlier uncommitted work is retained: modified `data/copy-index.json`, `data/editorial/page-metadata.json`, `data/quality/full-page-inventory.json`, `data/quality/phase2-content-inventory.json`, `data/quality/phase3-originality-audit.json`, `index.html`, `js/storybook.js`; untracked `css/academy-shell.css`, `css/hindi-academy.css`, `data/hindi-academy/{curriculum.json,search-index.json}`, `docs/hindi-academy-2-checkpoint.md`, `images/hindi-academy-hero.webp`, `js/{academy-catalogue,academy-home,hindi-academy}.js`, `learn/hindi/academy/{index.html,catalogue/index.html,vowels/index.html,worksheet/index.html,answers/index.html}`, `tests/regression/test-hindi-academy.mjs`, `tests/unit/test-academy-registry.py`, `tools/build-hindi-academy.py` and `tools/lib/academy_registry.py`.

## Next gates

Finish cross-repository resource/asset/link mapping and human review; design and validate the central course graph; audit real source coverage and author/review missing course content; integrate resources into textbook chapters while preserving URLs, fragments, SEO and both progress stores; implement and verify the reader, illustrations, reviewed strokes, media, exercises and keys; run the full requested compatibility, content, performance, accessibility, print, responsive and deployment-artifact checks. Owner approval is required before release.

---

# Continuation checkpoint — inventory, model and first reader component

2026-11-28 · **project remains open; batches 2 and 3 are not complete**. No deploy or merge.

## Batch 2 work actually implemented

- `tools/audit-hindi-textbook.py` now scans all 3,021 publisher-eligible HTML files for static anchor inbound links. It records sitemap membership, canonical/robots, title/H1, linked media/styles/scripts and local file existence. `resource-inventory.json` contains 1,119 Hindi-related candidates, of which 825 occur in a sitemap; `resource-inbound-links.json` contains full static same-host inbound source lists for those candidates. There are 79 path-name-matched Hindi/Devanagari sources/assets. Zero missing local `src`/stylesheet/script references were found among these candidates. Zero **exact normalized main-text** duplicate groups were found; this says nothing about partial or semantic duplication.
- This is a more systematic **candidate** inventory, not the requested fully verified inventory: relevance, content quality, copyrights, unreferenced or dynamically referenced media, stylesheet imports, external links, external inbound links, source trees without matching names and pedagogical assignments need human review. The snapshot can contain false positives and omit hidden content. Identity `KEEP` actions avoid irreversible changes; they are not final migration decisions. Of the candidates, only the 18 existing Foundation lesson URLs have a preliminary curriculum assignment.
- Extended the existing `data/hindi-academy/curriculum.json` instead of introducing a parallel source tree: five intended books, four planned phases each, prerequisites and 18 actual Foundation lesson references under Beginner → Devanagari foundations. Planned routes do not publish pages and empty phases are explicitly incomplete. This is a working graph, not five authored courses. The graph validation rejects unsafe/duplicate planned routes, invalid relationships, false completeness and missing character records.
- The same manifest records 72 required character/form entries: 11 independent vowels, 3 chart forms, 33 consonants, 7 additional letters, 4 conjuncts, 10 vowel signs, 4 marks, plus an inherent-vowel coverage entry. Existing grouped-lesson references are evidence of existing material only, not completed individual lessons. Every individual lesson and stroke sequence remains incomplete/unverified; the character records make no audio, worksheet, illustration or editorial approval claims.

## Batch 3 work actually implemented

- `tools/build-hindi-textbook-reader.py` adds one manifest-driven chapter navigation component to the 18 existing Foundation pages. It provides real Hindi → Beginner context and a native `<details>` chapter list, with a fixed collapsible desktop side menu and compact mobile menu. It reuses the lesson pages and their existing previous/next controls; it does not create new course, phase or chapter URLs, duplicate lesson prose, change canonical/indexing metadata, or rewrite local progress. The Foundation legacy generator applies the same transform on rebuild. `css/hindi-textbook-reader.css` loads the existing OFL-licensed local Devanagari font for tagged Hindi text in these pages.
- This component is **not** the requested complete reader or visual redesign. Existing Foundation page content and book-mode, quizzes, audio, tracing and navigation still have legacy designs and behavior. Other chapters are not yet integrated. No new substantive lessons, images, verified strokes, audio recordings or worksheets were authored in this continuation. The 390px screenshot shows the expanded menu and the site-wide floating controls consume substantial screen area; further mobile design review is needed.

## Validation actually run

- `python3 tools/build-all.py check`: PASS after regenerating copy index, editorial metadata and quality inventories. Intermediate failures exposed stale generated files and an oversized shared inline CSS block on `/hindi/`; the CSS was scoped to the hub and the existing reading-layer assertion passed without weakening it. This check explicitly is not editorial or release approval.
- `npm test`: PASS; sandbox blocks outbound TLS to the live Apps Script, so live service behavior remains unverified and relevant tests use their fallback/contract path.
- `python3 tools/build-public-dist.py --check`: PASS, 5,513 public files, 1,576 sitemap URLs resolved, no private-path leakage.
- Model tests: 3 passed, including invalid relationships, false completeness, coverage and a fixture reusing a lesson. Reader tests: 2 passed, including all 18 actual source pages, one current item and static 18-link contents, idempotence, legacy progress markers and fixture expansion. Existing Foundation depth test: 6 passed. Foundation primer validator, reader generator `--check`, page layer and `git diff --check` passed.
- Real Chromium reader navigation at 320, 375, 390, 430, 768, 1024, 1280, 1440, 1920px: no page errors or horizontal overflow, contents open and actual next-page navigation worked. No-JS reading and menu were checked at 390px. Screenshots at 390 and 1440 were reviewed; locally bundled Hindi font renders the Hindi heading and menu. This is not a complete accessibility audit, all-chapter visual review or comprehensive print test.

## Exact continuation changes

Added: `css/hindi-textbook-reader.css`, `tools/build-hindi-textbook-reader.py`, `tests/unit/test-hindi-textbook-model.py`, `tests/regression/test-hindi-textbook-reader.py`, `tests/e2e/test-hindi-textbook-reader.mjs`, `docs/architecture/hindi/resource-inbound-links.json`.

Updated: `data/hindi-academy/curriculum.json`, `tools/lib/academy_registry.py`, `tools/audit-hindi-textbook.py`, `docs/architecture/hindi/resource-inventory.json`, `docs/architecture/hindi/textbook-architecture.md`, this checkpoint, `tools/build-hindi-foundation.py`, `tools/build-all.py`, `tools/build-hindi-hub.py`, `data/copy-index.json`, `data/editorial/page-metadata.json`, `data/quality/full-page-inventory.json`, `data/quality/phase2-content-inventory.json`, `data/quality/phase3-originality-audit.json`, and the 18 `learn/hindi/foundation/{swar,vyanjan-1,vyanjan-2,vyanjan-3,bina-matra,aa-ki-matra,i-ki-matra,ee-ki-matra,u-ki-matra,oo-ki-matra,e-ki-matra,ai-ki-matra,o-ki-matra,au-ki-matra,anusvar-visarg-chandrabindu,ri-ki-matra,sanyukt-akshar,pahli-kahani}/index.html` files. Earlier first-batch changes remain as listed above. `/hindi/index.html` is no longer changed by the current patchset: its shared CSS was restored to the baseline output.

## Exact next steps

Continue **Batch 2** with manual candidate classification, repository-wide content/source/media/rights review, complete route mapping and meaningful duplicate and missing-concept review. Continue **Batch 3** by making the graph usable for real course/phase/chapter/lesson generation, introducing a single accessible reader across all educational content without breaking generators or URLs, integrating chapter/lesson previous-next, local progress, search and print. Then complete vowels first (Batch 4), followed by consonants, matras/conjuncts/Barakhadi and the other books. All 72 forms lack verified individual teaching and stroke-order review; do not mistake grouped existing pages for completion. Known editorial issues to investigate include the current Foundation source using a blueberry emoji for अनार and presenting रंग as if the written form contains ङ: it actually contains anusvara. Neither item has yet been corrected or reviewed in this batch. Native-language editorial review and independently verified handwriting data remain essential release gates.

---

# Continuation checkpoint — corrected pathways and supplied visual pack

2026-11-28 · branch `arena/28510265-ekguru`. **The digital Hindi school is not complete or production-ready.** No deployment, merge or credentialing.

## User-supplied package and integration

The package was retrieved from `A-Manually/ekguru-hindi-visual-pack` at GitHub commit `8c94adc830929a8057b026d26439fda94fa93fd5` without switching branches. The attached `README.md`, `install.py`, `illustrations.json` and `preview.html` matched the retrieved copies by SHA-256. Inspected `preview.html` in Chromium: all 49 illustration files decoded. The separate preview did not have the checkout's local Hindi font, whereas the integrated chapters do. The 49 SVGs were XML-parsed and scanned for scripts, event attributes, foreign objects and external references. The pack's two fixture tests passed. Installer dry-run passed with 49 exact character/word matches and 56 pending files; `--apply` succeeded, and an immediate second dry-run reported zero pending files. After that, integrated output was adapted to add descriptive Hindi image alt text and correct an existing linguistic issue; the unmodified installer would overwrite those adaptations if run again. Do not blindly rerun `--apply`.

The user describes these as original EkGuru assets; the package records `original-vector`, with `draft-visual-review-required`. This is not independent rights or subject-matter verification. Exactly 49 local SVG illustrations now appear in the actual existing chapters: `swar` 13, `vyanjan-1` 10, `vyanjan-2` 10, `vyanjan-3` 16. Their user-supplied mapping is retained at `data/learning/hindi-textbook-illustrations.json`; the 72-form coverage model references the 49 matching examples without claiming an individual lesson, reviewed strokes or complete coverage. Existing pronunciation, trace grid, local completion, quizzes and worksheet functionality have not been replaced. The क/ख airflow comparison is a schematic, not a handwriting animation; it respects reduced motion and can be replayed by reopening its disclosure.

The earlier issue treating the written word रंग as containing ङ was corrected in both `tools/hindi-foundation-content.py` and the generated `vyanjan-1` page. It is now described as anusvara representing a nasal sound before ग; ञ is identified within ज्ञ in ज्ञान. The library data was rebuilt. The existing pomegranate emoji was replaced by the supplied pomegranate SVG. Both wording and art still require native-speaker/educational review; all other flagged quality issues are not presumed resolved.

## Corrected independent pathways

`data/hindi-academy/curriculum.json` now models `LearningPath → Textbook → Phase → Chapter → Lesson`: five ordered academic textbooks (Kids, Beginner, Intermediate, Advanced, Mastery) and five ordered independent adult stages (Foundation, Beginner, Intermediate, Advanced, Mastery). Each has four planned phases, prerequisite progression and preliminary competency, vocabulary, grammar, reading, writing, speaking, listening and assessment scope. Academic ages/classes are curriculum-design analogies, not accreditation or age gates. Placement by proficiency remains a design requirement, not an implemented placement system.

The 100 requested academic topics and 100 preliminary adult topics are explicit planning labels, **not 200 implemented chapters**. The 18 pre-existing Foundation lessons remain preliminarily assigned only to academic Beginner; adult stages currently have no authored chapters. Validation rejects cross-path prerequisites, duplicate lesson counting, invalid routes, unsupported completeness claims and missing/mismatched asset references. The shared reader is software, not a single textbook shared by both pathways. Existing routes and canonical/indexing decisions are unchanged; `/learn/hindi/mastery/`, `/learn/hindi/older-adults/` and their proposed children have **not** been published as empty placeholders. The updated architecture document includes both pathway graphs and a progression diagram. Detailed chapter-level objectives, real content, assessments, accommodations, dependency matrix and differentiated learning outcomes still need development and review.

## Verification

- Pack tests: 2 passed; dry-run, apply and immediate idempotence passed as described above.
- `python3 tools/build-all.py check`: PASS after refreshing generated learning-library data, copy index, editorial metadata, Foundation-depth report and quality inventories. This is the comprehensive **check mode**, not native review or a release approval.
- Full write-mode `python3 tools/build-all.py` was attempted in a separate copy of the current working tree to preserve uncommitted work. It **failed at its first live sheetsync step** because the published Google Sheet cannot be reached from the sandbox (`csv` and `tsv` fetch failed). Its deliberate stop-on-failure policy was not bypassed; the full write-mode build therefore did not complete.
- `npm test`: PASS. The sandbox cannot reach the live Apps Script, so contract/mock tests do not verify the deployed service.
- `tools/build-public-dist.py --check`: PASS, 5,563 files, all 1,576 sitemap URLs present and no private-path references. A separate public-file listing confirmed all 49 SVGs and their manifest are included, while the supplied installer, preview and pack tests are not. No `_site` deployment was created.
- New visual regression: 3 tests passed for all 49 SVGs, exact lesson images/alt text, generator output parity, script/reference safety, airflow reduced-motion and the corrected nasal explanation. Model: 3 tests passed (two paths, 10 distinct stages, 200 clearly planned topic labels, 72 coverage entries, 49 draft images and invalid/duplicate/cross-path rejection). Foundation depth: 6 passed. Existing Academy and textbook reader browser suites also passed.
- Real Chromium: all 49 images loaded/decoded in all four real chapter pages; reduced-motion airflow, 9 widths (320, 375, 390, 430, 768, 1024, 1280, 1440, 1920), no horizontal overflow, and no-JS visual reading passed. The mobile and desktop integrated lesson screenshots were inspected. Existing site floating controls and book-mode still take considerable space on mobile.
- A4 and US Letter PDFs generated from the existing illustrated vowel lesson, not a new worksheet; their page boxes and embedded `NotoSansDevanagari-Bold` were inspected in PDF metadata. The whole extended lesson produces 20 A4 / 21 Letter pages, so print layout still needs work. `pdfinfo`/`pdffonts` were unavailable; page and font fields were inspected directly in the PDF bytes, not by visual PDF review.
- Indexing freeze, hub and reader generator `--check`, `git diff --check`: PASS. A scratch package preview inside `.artifacts` was removed from the workspace before regenerating quality reports because a legacy audit scanner otherwise counted it as a page. No pack installer or preview is published.

## Remaining critical work

The mature adult curriculum and five academic books do not yet contain their intended distinct substantive lessons, and neither pathway has final assessments or a Hindi Hero award. Most existing material is not yet classified into either pathway. The reader is only a shared navigation component on 18 Foundation lessons, not the unified textbook reader across all Hindi chapters. Individual vowel and consonant lessons, additional-letter lessons, full matra/Barakhadi instruction, age-appropriate illustrations beyond this starter pack, licensed native audio, verified handwriting instructions/animation, new meaningful worksheets and answers, search, complete migration mapping and full editorial/accessibility/visual/print reviews remain open. The 49 illustrations do not change the 72-form completion status.

## Exact current working-tree changed files

The following includes retained earlier work as well as this continuation; generated screenshots and logs in ignored `.artifacts` are not deliverables.

```text
 M css/foundation.css
 M data/copy-index.json
 M data/editorial/page-metadata.json
 M data/quality/full-page-inventory.json
 M data/quality/hindi-foundation-expansion.json
 M data/quality/phase2-content-inventory.json
 M data/quality/phase3-originality-audit.json
 M index.html
 M js/hindi-learning-library-data.js
 M js/storybook.js
 M learn/hindi/foundation/aa-ki-matra/index.html
 M learn/hindi/foundation/ai-ki-matra/index.html
 M learn/hindi/foundation/anusvar-visarg-chandrabindu/index.html
 M learn/hindi/foundation/au-ki-matra/index.html
 M learn/hindi/foundation/bina-matra/index.html
 M learn/hindi/foundation/e-ki-matra/index.html
 M learn/hindi/foundation/ee-ki-matra/index.html
 M learn/hindi/foundation/i-ki-matra/index.html
 M learn/hindi/foundation/o-ki-matra/index.html
 M learn/hindi/foundation/oo-ki-matra/index.html
 M learn/hindi/foundation/pahli-kahani/index.html
 M learn/hindi/foundation/ri-ki-matra/index.html
 M learn/hindi/foundation/sanyukt-akshar/index.html
 M learn/hindi/foundation/swar/index.html
 M learn/hindi/foundation/u-ki-matra/index.html
 M learn/hindi/foundation/vyanjan-1/index.html
 M learn/hindi/foundation/vyanjan-2/index.html
 M learn/hindi/foundation/vyanjan-3/index.html
 M learn/hindi/index.html
 M tools/build-all.py
 M tools/build-hindi-foundation.py
 M tools/build-hindi-hub.py
 M tools/hindi-foundation-content.py
?? css/academy-shell.css
?? css/hindi-academy.css
?? css/hindi-textbook-reader.css
?? data/hindi-academy/curriculum.json
?? data/hindi-academy/search-index.json
?? data/learning/hindi-textbook-illustrations.json
?? docs/architecture/hindi/first-batch-checkpoint.md
?? docs/architecture/hindi/resource-inbound-links.json
?? docs/architecture/hindi/resource-inventory.json
?? docs/architecture/hindi/textbook-architecture.md
?? docs/hindi-academy-2-checkpoint.md
?? images/hindi-academy-hero.webp
?? images/hindi-textbook/0905-0902.svg
?? images/hindi-textbook/0905-0903.svg
?? images/hindi-textbook/0905.svg
?? images/hindi-textbook/0906.svg
?? images/hindi-textbook/0907.svg
?? images/hindi-textbook/0908.svg
?? images/hindi-textbook/0909.svg
?? images/hindi-textbook/090a.svg
?? images/hindi-textbook/090b.svg
?? images/hindi-textbook/090f.svg
?? images/hindi-textbook/0910.svg
?? images/hindi-textbook/0913.svg
?? images/hindi-textbook/0914.svg
?? images/hindi-textbook/0915-094d-0937.svg
?? images/hindi-textbook/0915.svg
?? images/hindi-textbook/0916.svg
?? images/hindi-textbook/0917.svg
?? images/hindi-textbook/0918.svg
?? images/hindi-textbook/0919.svg
?? images/hindi-textbook/091a.svg
?? images/hindi-textbook/091b.svg
?? images/hindi-textbook/091c-094d-091e.svg
?? images/hindi-textbook/091c.svg
?? images/hindi-textbook/091d.svg
?? images/hindi-textbook/091e.svg
?? images/hindi-textbook/091f.svg
?? images/hindi-textbook/0920.svg
?? images/hindi-textbook/0921.svg
?? images/hindi-textbook/0922.svg
?? images/hindi-textbook/0923.svg
?? images/hindi-textbook/0924-094d-0930.svg
?? images/hindi-textbook/0924.svg
?? images/hindi-textbook/0925.svg
?? images/hindi-textbook/0926.svg
?? images/hindi-textbook/0927.svg
?? images/hindi-textbook/0928.svg
?? images/hindi-textbook/092a.svg
?? images/hindi-textbook/092b.svg
?? images/hindi-textbook/092c.svg
?? images/hindi-textbook/092d.svg
?? images/hindi-textbook/092e.svg
?? images/hindi-textbook/092f.svg
?? images/hindi-textbook/0930.svg
?? images/hindi-textbook/0932.svg
?? images/hindi-textbook/0935.svg
?? images/hindi-textbook/0936.svg
?? images/hindi-textbook/0937.svg
?? images/hindi-textbook/0938.svg
?? images/hindi-textbook/0939.svg
?? js/academy-catalogue.js
?? js/academy-home.js
?? js/hindi-academy.js
?? learn/hindi/academy/answers/index.html
?? learn/hindi/academy/catalogue/index.html
?? learn/hindi/academy/index.html
?? learn/hindi/academy/vowels/index.html
?? learn/hindi/academy/worksheet/index.html
?? tests/e2e/test-hindi-academy-browser.mjs
?? tests/e2e/test-hindi-foundation-illustrations.mjs
?? tests/e2e/test-hindi-textbook-reader.mjs
?? tests/regression/test-hindi-academy.mjs
?? tests/regression/test-hindi-foundation-illustrations.py
?? tests/regression/test-hindi-textbook-hub.py
?? tests/regression/test-hindi-textbook-reader.py
?? tests/unit/test-academy-registry.py
?? tests/unit/test-hindi-textbook-model.py
?? tools/audit-hindi-textbook.py
?? tools/build-hindi-academy.py
?? tools/build-hindi-textbook-reader.py
?? tools/lib/academy_registry.py
```

---

# Continuation — print and offline-font reliability (2026-11-28)

This is another partial batch, not a completed curriculum. On actual Chromium A4 and Letter PDFs, the prior vowel chart split the first row of illustrated cards across a page boundary; its SVG trace letters also rendered as empty boxes when the device lacked a Hindi font. With JavaScript disabled, the character cards themselves could render as boxes because the reader font selector depended on a script-created theme attribute. The Foundation CSS generator and its generated stylesheet now keep individual cards together in print, show unvisited trace models, use the local Devanagari font for SVG models, and suppress frozen audio/input-only book-mode rounds rather than representing them as paper worksheets. The reader's local Hindi font now applies with or without JavaScript, including fallback for mixed-script body text. The original lesson copy, URLs, progress stores, print watermark and interactive on-screen exercises remain in place. This is not a verified stroke-order tool.

Verification: the new optional `tests/e2e/test-hindi-foundation-print.mjs` rendered A4, Letter and no-JavaScript A4 PDFs, checked print styles, local font and PDF embedding; the vowel-chart pages were visually inspected with PyMuPDF. Card clipping and missing glyphs were fixed in those inspected pages. Full-lesson layout still needs complete page-by-page print review and native-speaker editorial review. The existing 49-image browser test was updated to use the actual privacy notice's Only essential control before interacting with the lessons; it retains all previous image, responsive and reduced-motion assertions.

The branch also contains the earlier privacy-panel redesign. Since current `main` contains uploaded `A-Manually/` development packs, `tools/build-public-dist.py` now excludes that directory and the root `Manually` sentinel, without deleting or changing the uploads. `tests/unit/test-public-upload-pack.py` verifies exclusion using a fixture even on a checkout where those inputs do not exist; the integrated 49 local SVGs remain public. The independent academic/adult curricula, full inventory classification, reviewed handwriting and audio, meaningful worksheets, assessments and overall editorial approval remain open.

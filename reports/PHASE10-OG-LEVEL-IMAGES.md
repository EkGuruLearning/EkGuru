# Phase 10 — first-wave CEFR level OG cards

**Status:** implementation increment complete for the explicit eight-language font-coverage allowlist. Phase 10, full-site OG coverage, and visual/browser review are not complete.

**Source command:** `Arena latest command  arena/Arena latest command  arena/01a0e655-ekguru/after fasst.md` — Phase 10.

## Scope and output

- `sitemap-levels.xml` is the publication boundary. It contains 92 published CEFR level URLs across 18 languages and 18 level-ladder URLs. This increment generates cards for 38 of the 92 CEFR pages: Arabic (`ar`), German (`de`), Spanish (`es`), French (`fr`), Italian (`it`), Portuguese (`pt`), Russian (`ru`) and Urdu (`ur`).
- Coverage is an explicit language-to-script allowlist in `data/og-image-coverage.json`; it does not automatically expand when another language is published. The other 54 CEFR pages and all 18 ladder pages keep the shared cover, as do non-level pages.
- Each card is a 1200×630 PNG rendered from generated SVG by `@resvg/resvg-js`, using the bundled DejaVu Sans regular/bold files and their license. The neutral card includes EkGuru, language, CEFR level, and the first authored bold term in that page's native-language Word cell. The term is source-page content selected by a script, not an independently checked translation or reviewed example.
- The 38 PNGs total 2,356,532 bytes; the largest is 71,603 bytes. These figures cover only the generated OG batch, not total page resources. The renderer checks dimensions, deterministic bytes, duplicate image output and a 300 KB per-image ceiling.
- Supported published CEFR pages receive PNG Open Graph and Twitter image URLs, type/dimensions and alt metadata through `tools/build-course-levels.py`. The OG builder validates sitemap membership, page metadata and samples before rendering; its check mode is wired into `tools/build-all.py`.

## Checks run

- `python3 tools/build-course-levels.py --check` — 0 stale pages.
- `python3 tools/build-og-images.py --check` — 38 deterministic 1200×630 PNGs, all within the per-image limit; coverage reports 38 images across 8 languages and 54 published levels awaiting fonts.
- `node tools/test-course-levels.mjs` — 37 passed, 0 failed.
- `node tools/test-level-visuals.mjs` — 39 passed, 0 failed.
- Locally opened the Arabic, Russian and Spanish A1 PNGs for a limited layout spot-check. This is not human/native-speaker review, browser testing or a platform preview.
- `npm run test:courses` — exits 0. Its separate pronunciation audit remains **BLOCKED**: 0/5,694 published vocabulary items have source-referenced IPA; the test output explicitly does not claim independent linguistic review.
- Python/Node syntax checks and `git diff --check` pass.

## Not reviewed / still open

- No native-speaker, linguistic, source-verification or independent review was performed on the sample terms, typography or cards. Do not treat the extracted terms as validated teaching examples.
- No production HTTP request, social-network scraper/cache test or platform preview was run. The generated metadata and local assets passing checks are not evidence of production fetchability.
- Fonts for Indic, CJK and the other uncovered scripts are not included in this batch. Add and test suitable licensed fonts before expanding the allowlist; do not render missing-glyph boxes or silently infer coverage from a broad script family.
- The other 54 published CEFR pages, 18 ladder pages, and the rest of the site's OG images still need coverage review. Broader illustration/alt-text review, icon use, responsive and print behavior, reduced-motion browser coverage, and full-page visual/browser review remain open.
- `python3 tools/build-all.py check` was not run because that command begins with the separate live-sheet sync gate. No live HTTP or production verification is claimed.

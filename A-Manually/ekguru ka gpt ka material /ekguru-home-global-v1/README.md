# EkGuru Global Homepage V1 — design preview and integration source

Target: the existing `/` homepage (`index.html`), not `/learn/` or a new Academy. Original editorial vector illustration; no external images or new runtime dependencies. Standalone preview uses embedded CSS, JS and SVG, with real external EkGuru navigation links. It is not a deployed page. Preview is noindex.

## Included
- `preview.html`: standalone interactive design, open in Chrome or Safari.
- `source/languages.json`: snapshot of the 18 existing published paths observed in the earlier repository audit and homepage navigation. Hindi and seven other Indian languages first, ten world languages next. Kannada and Malayalam remain excluded pending approval. Other languages (including English) should be added only when real courses are ready.
- `source/render.py`: build-time renderer. `python3 source/render.py` regenerates preview and `source/home-region.html`.
- `source/home-region.html`: proposed replacement content, not an automatic overwrite patch.
- `css/home-global.css`, `js/home-global.js`, `images/conversation.svg`: standalone assets.
- `tests/`: registry and Chromium preview checks.

## Arena integration
1. Audit current actual branch and all homepage owners. In particular preserve generated `home-tutors`, `home-courses`, `languages-home`, shared shell, consent, analytics, trust/footer, SEO/schema, locale alternatives, progress and indexing contracts. Do not publish this preview or internal package as a public asset.
2. Reconcile the layout through the real homepage generators rather than replacing index.html wholesale. The package stylesheet is intentionally standalone: scope it to the homepage/content region, reconcile shell class names and CSS tokens, and use the existing real EkGuru logo. Maintain the site's theme (including contrast mode if present). Do not load two shell/theme systems. Wire the optional theme control to the existing controller or remove the redundant control. Current preview logo is a design mark only.
3. Replace snapshot registry input with the existing validated language registry and publication state; fail on missing routes, preserve real course paths and indexing decisions. Do not claim new textbooks are live until actual integration is verified. The illustrated book covers are a design concept and link through the existing Hindi hub, not placeholders for direct unverified course links.
4. Copy artwork to `images/home-global/conversation.svg`. Move stylesheet and script to the appropriate production asset locations; avoid CSS clashes. Keep search and filtering progressive; all real links render as HTML before JS. The homepage must not fetch the full course corpus.
5. Restore actual dynamic tutor profile data through its owner, if a profile preview is desired. Never invent profiles, reviews, ratings, prices, languages taught, or booking availability. Free self-study and independent Hindi tutor discovery remain separate. No payment, commission, login requirement or new backend.
6. Preserve useful legacy routes and content; remove only redundant homepage presentations after verifying access elsewhere. Validate legal/editorial disclosures and production metadata. Run full build/regression, actual hosted routes, storage persistence, accessibility and performance checks before release.

## Verified here
`python3 tests/test_registry.py`: 3 tests, 100 synthetic additional registry entries.
`node --check js/home-global.js`: syntax.
`python3 tests/test_browser.py`: embedded Chromium 18 cards, show more, native-script search, filter, dark mode, nine viewport widths, no-JS navigation anchors, no page exceptions. The tests use set_content, not hosted browser navigation. Full repo integration, link HTTP responses, persistence across reload, contrast audit, production performance and SEO tests are pending. Chromium executable path can be adjusted for other machines.

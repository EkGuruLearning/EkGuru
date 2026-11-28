# EkGuru Learn — Catalogue V3

**Scope:** upgraded design of the first deliverable, `/learn/` only. V3 supersedes V2. This is not the complete Hindi curriculum. The current Hindi and other language pages remain unchanged. The actual repository's `tools/build-learn-index.py` was inspected via GitHub. No repository changes or deployment were performed.

## Preview
Open `preview.html` after extracting the ZIP. It uses the same catalogue renderer with a snapshot of 8 Indian and 10 world-language entries. Preview links lead to the existing live EkGuru website; they do not simulate completed courses. The preview header/footer are illustrative; actual integration retains the current site shell. `preview-standalone.html` embeds its CSS, JS and artwork for convenient local viewing. No paid service, network dependency or remote font is required to render this preview. Native-script glyph appearance depends on available device fonts.

## Integrate on Arena's actual branch
From the extracted package (not the public website root):

```sh
python3 install.py /path/to/EkGuru
python3 install.py /path/to/EkGuru --apply
```

V3 supports the inspected original generator or an already-installed V2 hook. Old V2 assets are retained for dependency review; no deletion is automatic. Default mode is read-only; it rejects an unexpected generator layout or conflicting assets. Inspect the diff. If the Arena branch has reorganized the generator or source files, adapt the small renderer hook manually rather than reverting the branch. The hook uses the original validated language registry and schema generation. It preserves existing `/learn/` metadata/canonical/robots behavior except intentionally updated title/description, and moves previously linked resources into a compact disclosure. Kannada and Malayalam remain excluded by the existing indexability guard until approved. Existing world-language primary URLs are retained; do not invent `/learn/<language>/` routes or publish held pages to force consistency. No delete operation is included.

Use the branch's actual publishing pipeline (inspect CI and build docs first). On the inspected default-branch layout the generator documented this sequence:

```sh
python3 tools/apply-ultra.py --strip
python3 tools/build-hindi-hub.py
python3 tools/build-learn-index.py
python3 tools/apply-ultra.py
```

Run the full existing build and regression suite; validate the generated page, navigation, legacy fragments, old resource URLs, schema, sitemap/indexing, actual site shell and theme. Check the site's CSS bundling and CSP policy. Do not publish the ZIP, preview, installer or test files; only integrate the four listed production assets and the existing generator hook. Reconcile any exact-copy legacy tests against their original purpose; do not remove coverage. Do not change unrelated generators or tutor functionality. No new framework, payment system, server or mandatory login.

## Architecture
`validated registry + existing generator -> renderer -> static HTML -> CSS + small deferred JS enhancement`

- One prominent Hindi entry, then other released Indian languages, then released world languages.
- Search supports native scripts and Latin names; filter buttons and empty state.
- All main links rendered serverlessly as HTML; JavaScript is optional for search/filter only.
- CSS entrance, floating glyph, orbit, sparkle and hover animations respect reduced-motion preferences; automatic decorative motion is finite. Each category initially shows at most 12 cards when JS is available; Show more reveals the next 12, and search always covers the entire catalogue. Without JS, every link remains visible. Local SVG artwork, no third-party requests from catalogue component.
- The shared renderer consumes available rows. New approved Indian languages need registry entries; world languages already derive from `data/courses.json`. Neither route creation nor course content generation is performed by this package.
- `li-hindi`, `li-indian`, `li-world`, `li-shared`, `li-tutors` legacy anchors retained.
- Existing English-language legal/editorial disclosures retained. No fabricated course counts or certification claims.

## Tests
```sh
python3 tests/test_catalogue.py
node --check js/learn-catalogue-v3.js
python3 tests/browser_test.py  # Python Playwright + Chromium; optional
```

Five isolated unit tests passed, including original and V2 hook migration and a 100-row renderer fixture. JavaScript syntax validation passed. Standalone Chromium browser testing using set_content passed: 18 real catalogue entries, native-script search, Latin accent folding, category filters, empty state, dark mode, nine viewport widths, no-JS navigation, and a 50-record synthetic expansion fixture (12 → 24 cards, search finds an initially hidden item). The fixture is test-only. Screenshots were taken from the standalone preview, not live EkGuru. Full repository build, live link crawl, actual shell integration, accessibility audit and measured Core Web Vitals remain unverified. No production commit. No claim of complete Hindi course or production readiness.

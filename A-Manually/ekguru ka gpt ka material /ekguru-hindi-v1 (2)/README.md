# EkGuru Hindi hub — V1

A Hindi-first, modern textbook catalogue for the existing `/learn/hindi/` route. It matches the green/gold Learn V3 visual identity. This is a main-page upgrade, not a complete curriculum or a replacement site.

## Preview
Open `preview-standalone.html` in a browser. It is fully self-contained; lesson links go to the existing live site. The preview uses a representative fixture of existing resources, not a full repository build. The actual renderer reads the legacy generator's entire link inventory and discovers chapter pages in approved book directories.

## Integration
Extract this ZIP outside the public deployment tree. Run the following from the extracted package:

```
python3 install.py /path/to/EkGuru
python3 install.py /path/to/EkGuru --apply
```

The first invocation is read-only. The installer refuses unknown generator structures and conflicting files. It modifies the existing `tools/build-hindi-hub.py` source, not generated HTML. If the Arena branch has reorganized the generator or uses a different renderer, adapt the explicit `render_hindi_hub(legacy_region, href, ROOT)` hook manually rather than reverting changes. Do not append a second hub.

Use the existing build pipeline; the default branch generator documents the sequence `tools/apply-ultra.py --strip`, `tools/build-hindi-hub.py`, `tools/apply-ultra.py`. Run the complete pipeline and its regression tests, including `build-hindi-hub.py --check`. Verify the site shell, link destinations, all existing fragment targets, indexing contract, and the separate `/hindi/` compatibility route. The existing generator's legacy region is still constructed, then compacted into a searchable library. The topic-index renderer is untouched. The actual repository and publisher have not been executed in this package environment.

Other pipeline tools can append old course-level and level-visual bands outside the hub markers. Inspect the integrated page and consolidate those redundant sections in their owning generators for this route only, retaining links, disclosures, progress and required functions. Do not delete these shared components globally. Keep review disclosures and legal/footer content. Do not publish preview, tests, installer or ZIP.

## Future content
Update `data/learning/hindi-textbook-catalogue.json`: each academic or adult record has its own route and status (`planned`, `existing`, `published`). `planned` is intentionally not clickable even if a directory exists. `existing` means available legacy lessons, not a complete new textbook. Change to `published` only after genuine editorial and curriculum approval. The renderer requires the destination file to exist before rendering an active link. Future books and their nested chapter pages are discovered without editing the page layout. Adult paths remain distinct from academic stages. The master curriculum itself, age-specific lessons, audio recordings, handwriting instruction and worksheet assets are separate deliverables.

## Tests
`python3 tests/test_hub.py` (5 unit tests), `node --check js/hindi-textbook-hub.js`, `python3 preview/build_preview.py`, `python3 tests/browser_test.py` (Playwright + Chromium; path `/usr/bin/chromium`). Tested standalone only: native Hindi search, empty result, details, theme, 9 viewport widths, JavaScript-disabled access; synthetic future book and chapter fixture. No measured production Core Web Vitals, full accessibility audit or production deployment. CSS/JS use zero added runtime dependencies.

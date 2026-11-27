# Global technical discovery fixes

Date: 2026-11-24. Scope approved by the user: site-wide technical checks and verified fixes, not a course redesign or new country landing pages. The preceding [Hindi lesson pilot](hindi-sentence-pilot-qa.md) is preserved.

## Verified issues fixed

1. **Generic language annotations disappeared after JavaScript.** `js/seo.js` removed static hreflang links and then incorrectly skipped the generic language tag whenever a locale began with the same language code. For example `en-US` caused `en` to be skipped, and `es-ES` caused `es` to be skipped. The runtime now retains language-wide annotations alongside regional ones for the seven existing translations. All destinations are existing files with matching static canonicals; no country-specific content or translations were invented. The strengthened test failed against the original runtime before the fix.
2. **The translated page family's default URL varied by selected language.** `x-default` now consistently points to the existing root fallback for that page family (home, directory or application page), matching the static markup. Language selection, query-string behavior and existing canonical decisions are unchanged. The intentionally noindex tutor shell no longer receives an empty x-default href; its noindex and absent canonical remain unchanged.
3. **Social locale annotations accumulated on runtime re-evaluation.** Generated `og:locale:alternate` metadata is replaced instead of appended repeatedly. No duplicate alternate locale tags after a second evaluation.
4. **Sitemap check mode wrote files despite promising read-only validation.** `tools/build-sitemaps.py --check` no longer rewrites the dated audit report or creates its directory. Tests cover both passing and failing validation, preserve non-zero failure exits, and verify that existing report content stays untouched. Write mode still produces the report as before. No sitemap URL, lastmod or robots/canonical setting changed.
5. **The site-wide ownership index was stale.** Regenerated `data/copy-index.json` using the existing tool after global scope approval. Its 1,874-page membership is unchanged. This is a derived fingerprint refresh, not new page content or editorial review. Its check and the existing ownership matcher now pass.

Source/test changes for this pass: `js/seo.js`, `tools/test-seo-runtime.mjs`, `tools/build-sitemaps.py`, `tools/test-sitemap-freshness.py`; derived data: `data/copy-index.json`. No dependency manifests, service worker, payment/booking logic, tutor content, storage keys or country publication decisions changed.

## Validation

| Check | Result |
| --- | --- |
| Expanded `node tools/test-seo-runtime.mjs` | PASS: 84 combinations (4 browser locales × 3 page families × 7 existing UI language choices), plus existing static-metadata guard tests and noindex-shell check |
| Real Chromium local homepage checks | PASS: en-IN/390px, es-MX/768px, pt-PT/1280px, ar-SA/1440px; all seven generic tags retained, expected canonical and stable default, zero page errors or horizontal document overflow |
| `python3 tools/discovery_integrity.py` | PASS: 3,016 public HTML files, 249,442 internal references, zero missing-public-target/reciprocity errors |
| `python3 tools/build-guide-hreflang.py --check` | PASS: 16 existing localized guides, zero stale |
| `python3 tools/build-sitemaps.py --check` | PASS: 1,561 indexed memberships, zero invalid; report unchanged |
| `python3 tools/test-sitemap-freshness.py` | PASS: 3 tests, including read-only and failure-exit coverage |
| `python3 tools/test-discovery-integrity.py` | PASS: 10 tests |
| `python3 tools/audit-country-language-quality.py --check` | PASS: classifications current; no evidence upgrades |
| `python3 tools/build-seo-aeo-geo.py --check` | PASS: existing OpenSearch, robots, discovery summaries and checked structured data |
| Local HTTP discovery gate | PASS: 54 probes, 29 HTML samples, 1,561 sitemap URLs |
| Copy index check and matcher | PASS: 1,874 fingerprints |
| Indexing freeze contract | PASS: zero violations |
| Existing menu/search, drawer and learner-trust tests | PASS |
| Existing Googlebot parity test (`--local`) | PASS: 15 file-level comparisons; not a live production HTTP result |
| Hindi pilot regression test | PASS: 13 checks; pilot CSS/JS unchanged in this pass |
| Syntax and whitespace | `node --check js/seo.js`, `git diff --check`: PASS |

The local HTTP command was:

```sh
python3 tools/live-seo-gate.py --base http://127.0.0.1:4173 \
  --discovery --sample-size 24 --report .cache/global-technical-http.json
```

Chromium 158.0.8127.0 used the already approved temporary tooling. External requests were blocked; browser locale emulation does not mean requests originated in four countries. Test artifacts and runner are local-only under `reports/hindi-sentence-pilot-qa/global-*` and excluded from public deployment. No project dependency was installed or updated in this pass.

## Limits and follow-up

- Global discoverability improvements are **not** a promise of ranking, indexing, inclusion in AI answers or recommendation in every country. Search engines make those decisions.
- No live production crawl, Search Console/account access, field Core Web Vitals, physical mobile device, screen reader or native-language review was performed.
- Static country-language records retain their existing verification/publication states. We did not publish noindex/held pages or create doorway pages to target more countries.
- A legacy exploratory `tools/test-phase6-seo.py` run reported missing descriptions/canonicals because its regular expressions assume attribute order; those tags are present. Its output is not treated as evidence of real missing metadata. That legacy report's incidental write was reverted; the parser-based and runtime checks above are the verification used here.
- Some noindex lesson pages carry redundant self-only language annotations. These do not establish multilingual coverage and were not mass-rewritten; their indexation is intentionally unchanged.
- Full `tools/build-all.py check` was not run because it strips/restores generated page layers across the repository. The checks listed above are the exact tested scope, not a full master-build claim.

No commit, push, pull request, merge or deployment performed.

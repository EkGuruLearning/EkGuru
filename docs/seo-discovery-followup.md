# Search discovery: technical fixes and remaining ranking risks

This is implementation/audit evidence, **not** a promise of rankings, actual search-engine indexing, AI citations or a complete editorial approval.

## Fixed in this branch

- Root-relative assumptions in the `/hindi-classes/` and `/hindi-tutor-near-me/` generators broke CSS, JS, icons, reference files and body CTAs when served under their actual directory URLs. Relocation now edits actual HTML attributes, not JavaScript string literals; existing shell prefixes remain idempotent.
- Removed 12 nonexistent translated landing-page alternate URLs. No translation pages were invented.
- Rebuilt reciprocal hreflang on the 16 existing localized Hindi beginner guides. Removed the old English `/hindi/` destination because it canonicals to the course, not to an equivalent localized beginner guide. No canonical or publication decision was changed.
- Stopped `js/seo.js` from interpreting nested `index.html` pages as the homepage and replacing their titles/canonicals/schema. Original home/directory/intake/tutor-shell behavior remains in scope.
- Replaced the nonexistent `css/site.css` reference on six non-Indic name tools with the existing stylesheet, including the source generator.
- Fixed the Marathi lesson's full-number-chart link to `/numbers-in-marathi/`.
- Added a public-deploy-set crawl-target/asset/hreflang gate plus offline regression tests and DOM runtime tests to the master build.
- Replaced the old live SEO report-only script (which exited successfully even with failed requests) with a failing HTTP gate. It checks sitemap XML, canonical and robots headers/meta, missing-page HTTP status, crawler UA probes, optional AI/browser-discovery endpoints and HTTP/www normalization. Cloudflare/WAF challenges and network failures remain failures; no local fallback is presented as live success.
- Added weekly/manual HTTP evidence collection to the existing `live-guard` workflow; artifacts are retained even on failure.

## Local evidence

- Discovery integrity: **3,016 public HTML files** (3,014 content pages plus verification files), **249,226 internal HTML references**, **0 missing public link/asset or hreflang reciprocity/canonical errors**. Static href/src/poster scan only: not dynamic-JS navigation, CSS url(), srcset, external links or proof of server responses.
- Offline regression tests: **10 passed**; static runtime metadata checks: **9 routes passed**.
- Full `python3 tools/build-all.py check`: passed. This validates generated consistency and policy, not publication/readiness.
- HTTP sampling against local preview: **FAIL**, correctly exposing missing H1/content on country daily-phrase pages. A passing build must not be mistaken for a passing live-quality audit.

## Blocking / unresolved: do not hide these with more metadata

### 1. 196 empty country daily-phrase bodies

`learn-hindi-from-*/daily-phrases/index.html` currently has no H1 or authored phrase body; only shared navigation/support content remains. All 196 are indexable in the existing inventory. Examples: `/learn-hindi-from-ghana/daily-phrases/` and `/learn-hindi-from-philippines/daily-phrases/`.

**Recommended:** consolidate these duplicate-intent pages into the strongest shared phrase resource, update inbound links, and remove retired URLs from sitemaps. Prefer real HTTP redirects where the host supports them. Otherwise use an explicitly approved canonical/noindex transition appropriate to the host; do not invent unsupported GitHub Pages `_redirects` rules.

**Permission boundary:** the repository's immutable owner indexing/canonical contract explicitly forbids quality quarantine without separate approval. This branch does not silently rewrite that contract, mass-noindex pages, or pad 196 pages with the same generated text just to make an H1 check green. Owner approval is needed for consolidation/publication changes. Genuine unique country content is an alternative only when it is useful and verifiable.

### 2. GitHub Pages origin certificate renewal / HTTPS configuration

The authenticated Pages API reports:

- `cname`: `ekguru.shop`
- `build_type`: `workflow`
- `https_enforced`: `false`
- certificate state: `bad_authz`
- certificate description: `The ACME authorization is in a bad state. We need to start over.`
- reported certificate expiry: `2026-12-09`
- domains: `ekguru.shop`, `www.ekguru.shop`

This is **origin configuration evidence**, not proof that the public Cloudflare edge is currently serving a broken certificate. The Pages DNS-health API returned HTTP 403 for the integration, so DNS/CAA/ACME health could not be confirmed here.

**Owner/hosting actions:** inspect apex/www DNS and CAA/ACME validation in the actual DNS/hosting accounts; confirm the custom domain remains correctly connected; repair certificate issuance before enabling origin HTTPS enforcement; then verify valid TLS and one-hop HTTP/www redirects to `https://ekguru.shop/`. Do not toggle DNS/proxy/TLS modes blindly or bypass WAF security with a spoofable User-Agent rule.

### 3. Editorial quality and measurable search performance

Existing reports still show language reviewer/source-verification gaps and 196 thin indexable pages. Technical metadata cannot replace trustworthy, useful, reviewed content. No Search Console or Bing Webmaster account data, query impressions, actual index coverage, field Core Web Vitals, verified crawler-IP access, backlink audit or external competitor/ranking comparison was available in this workspace.

Next measurement loop: inspect Search Console indexing + selected canonicals, submit the canonical sitemap, sample URL Inspection on priority pages, examine real-user CWV, and prioritize content revisions from impressions/query intent. Only use verified account access; never manufacture reviews, backlinks, authority claims or ranking evidence.

## Reproduce

```sh
python3 tools/discovery_integrity.py
python3 tools/test-discovery-integrity.py
node tools/test-seo-runtime.mjs
python3 tools/build-all.py check
# Strict live checks; unavailable outbound traffic is a failure, not success:
python3 tools/live-seo-gate.py --check-origins
# After this branch is deployed, also require new discovery endpoints:
python3 tools/live-seo-gate.py --check-origins --discovery
# Local HTTP behavior (not production evidence):
python3 tools/live-seo-gate.py --base http://127.0.0.1:8080 --discovery --report /tmp/ekguru-preview-seo.json
```

No changes are live until the PR is merged and the Pages deployment succeeds.

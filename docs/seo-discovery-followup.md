# Search discovery: implemented fixes and remaining owner action

Implementation/audit evidence only — not a promise of rankings, indexing, AI citations or editorial approval. Changes are not live until the PR is merged and Pages deploys successfully.

## Technical repairs

- Repaired root-relative assumptions in `/hindi-classes/` and `/hindi-tutor-near-me/`: CSS, JS, icons, reference files and body CTAs now resolve at their actual directory depth.
- Removed 12 nonexistent translated landing-page alternates. Kept reciprocal/self-canonical hreflang on the 16 existing localized Hindi beginner guides; no translation URLs were invented.
- Stopped legacy runtime SEO from replacing nested pages' titles, canonicals and schema with homepage metadata.
- Fixed the nonexistent stylesheet reference on six name tools and the Marathi full-number-chart link.
- Added deploy-set link/asset/hreflang checks, regression tests and strict HTTP diagnostics. WAF challenges and network failures never become a synthetic live pass.

## Approved follow-up: 196 empty country phrase URLs consolidated

The owner replied **“continue remaining”** after the explicit approval request to consolidate the 196 empty country daily-phrase pages and adjust canonical/noindex as needed. The exact sources and approval context are recorded in `data/quality/indexing-baseline.json`, under `owner_approved_country_phrase_consolidation`.

Destination: **https://ekguru.shop/learn/hindi/conversation/** — an existing self-canonical, crawlable hub with links to greetings, politeness, everyday conversation, practice and phrase guides. Parent country guides were not changed.

Implemented:

- All 196 old URLs remain available for bookmarks, but canonical to the shared destination and immediately navigate there using an HTML refresh.
- A clear H1 and visible destination link work without JavaScript; a country-parent link is also available if automatic navigation is suppressed.
- Kept `index, follow` on source wrappers so crawlers can process the move signal. Did **not** mix cross-canonical consolidation with noindex, block them in robots.txt or claim that they have already disappeared from search results.
- Removed all 196 URLs from sitemaps. Search now excludes non-self-canonical routes, including the earlier `/hindi/` merge (499 published search targets remain).
- Removed misleading FAQ/QAPage claims from the retired wrappers. Classified them as ad-free UTILITY routes and changed the old generator so it cannot republish location-swapped phrase pages.
- Original immutable baseline remains **2,636 pages / 1,006 original indexable entries**; earlier approvals remain as history. Only the exact 196 new consolidation exceptions were added.
- No genuine HTTP 301 is claimed: GitHub Pages does not support repository `_redirects` rules. Canonical + immediate HTML navigation is the host-compatible fallback. Search engines still decide how to process it.

### Truthful sitemap dates

The sitemap builder previously set every supplement URL and sitemap-index child to the rebuild date. It now preserves existing URL dates, omits unknown optional dates on newly discovered URLs, and omits unverified sitemap-index child dates. Regression tests ensure rebuilds do not invent editorial freshness.

## Verification

- Public HTML scope: **3,016 files** (3,014 content files plus verification files).
- Internal href/src/poster references: **249,034 checked, zero missing-target/hreflang errors**. Not a scan of dynamic navigation, CSS URLs, srcset or external links.
- Strict local HTTP audit: **PASS**, 1,561 unique sitemap URLs discovered, 29 canonical HTML samples and 58 probes including discovery files, old phrase URLs and their destination.
- Full `python3 tools/build-all.py check`: **PASS**; immutable contract and ad-policy checks pass.
- Consolidation regression tests cover every one of the 196 routes. Freshness tests prove stable sitemap regeneration.
- Added real-browser journeys for JavaScript-disabled automatic navigation and keyboard fallback with automatic refresh suppressed. Execution results are recorded in the PR's Playwright check, not inferred from static markup.

The inventory deliberately preserves raw robots permission: 1,758 pages permit indexing, of which **1,561 are self-canonical**, while 197 are crawlable noncanonical routes (the 196 phrase wrappers plus the earlier Hindi hub merge). The raw `thin_indexable` list still includes the short redirect wrappers; `standalone_thin_indexable` is empty. This is a classification distinction, not a claim of full content quality or actual Google indexing.

## Remaining owner action: GitHub Pages “Enforce HTTPS”

The earlier Pages certificate state was `bad_authz`. On recheck it is now:

- certificate: **approved** (`The certificate has been approved.`)
- domain: `ekguru.shop`
- reported expiry: **2027-02-24**
- `https_enforced`: **false**

Attempted to enable HTTPS enforcement with the authenticated Pages API. GitHub rejected the write with **HTTP 403 — Resource not accessible by integration**. No DNS, proxy or TLS modes were changed. The API's origin certificate state is separate from the Cloudflare edge certificate.

A repository admin must open **Settings → Pages → Enforce HTTPS** and enable it, then confirm HTTP/www normalization and valid TLS. The Pages DNS-health endpoint is also permission-denied for this integration. No credentials should be sent in chat; use the account's normal settings UI or appropriately permissioned connection.

## Remaining quality and measurement boundaries

Language reviewer/source-verification gaps remain in the existing quality reports. No Search Console/Bing Webmaster account data, actual index coverage, field Core Web Vitals, backlink audit or competitor/ranking measurements were available. Technical improvements cannot guarantee outranking larger companies.

Next measurement loop: canonical sitemap submission, URL Inspection on priority URLs, monitor old-URL consolidation, real-user CWV and query/impression-based content improvements. Do not manufacture reviews, backlinks or authority claims.

## Reproduce

```sh
python3 tools/build-country-phrases.py --check
python3 tests/regression/test-country-phrase-consolidation.py
python3 tests/unit/test-sitemap-freshness.py
python3 tools/discovery_integrity.py
python3 tools/build-all.py check
# Local HTTP (not production evidence):
python3 tools/live-seo-gate.py --base http://127.0.0.1:8080 --discovery --check-consolidations --report /tmp/ekguru-preview-seo.json
# After deployment; failures must remain visible:
python3 tools/live-seo-gate.py --check-origins --discovery --check-consolidations
```

Earlier production probes failed on empty Ghana/Philippines phrase pages before this consolidation. Until deployment, production is still expected to show the old behavior; local success is not a live-site success claim.

# EkGuru main forensic and working-tree reconciliation

Generated: 2026-09-20

Reference: `2066d27b3b41ccb3cb63c59d58dce4803d3d33a2`

Branch: `arena/01a0bd05-ekguru`
Readiness: **NOT_READY_DO_NOT_APPLY**

## Executive finding

The reference tree was not safe to treat as publication or monetization evidence. It contained a client-side mail relay credential, broad structural course-completeness claims, generated country/language claims without relation-level publication gates, and AdSense-loader occurrences. The working implementation now fails closed: the client token is empty, unsupported course/research surfaces are noindex and absent from sitemaps, and advertising/affiliate tracking is disabled.

This is **not** a PASS. Real-browser execution, production HTTP verification, live mail delivery, a real support-payment transaction, native-speaker review and certified advertising consent/account setup remain incomplete or owner-only.

## Main versus working implementation

| Signal | Reference main | Working implementation |
|---|---:|---:|
| Tracked files / public HTML | 5,109 / 2,636 | 5,130 tracked / 2,636 public HTML |
| Client mail token | PRESENT_REQUIRES_ROTATION | EMPTY |
| HTML files containing AdSense loader URL | 1,443 | 0 |
| HTML files with a noindex signal | 813 | 1,454 |
| Course publication states | structural claims not accepted | 10 complete, 8 partial, 71 research-required |
| CEFR publication gate | not authoritative | 92 allowed, 442 blocked |
| Country-language relations | agent-compiled breadth | 232 verified, 196 provisional, 1555 research-required |
| Sitemap policy gate | no deterministic noindex/self-canonical gate | PASS |

## File-level reconciliation

The JSON companion contains every changed/untracked path and status. Changes by top-level area:

- `(root)`: 15
- `data`: 8
- `images`: 161
- `js`: 11
- `languages`: 1,200
- `learn`: 333
- `learn-hindi-for-*`: 141
- `learn-hindi-from-*`: 196
- `other-pages`: 570
- `reports`: 15
- `tools`: 27
- `world-languages`: 195

Key source/configuration changes (first 120; generated page rows are in the JSON and page matrix):

- `M` `data/country-visuals.json`
- `M` `data/courses/index.json`
- `A` `data/monetization/affiliate-readiness.json`
- `M` `data/monetization/google-monetization.json`
- `M` `data/quality/adsense-readiness.json`
- `A` `data/quality/country-language-verification.json`
- `A` `data/quality/course-publication-audit.json`
- `A` `data/quality/sitemap-audit.json`
- `M` `js/analytics.js`
- `M` `js/cookie-consent.js`
- `M` `js/country-languages.js`
- `M` `js/country-marquee.js`
- `M` `js/course-player.js`
- `M` `js/i18n.js`
- `M` `js/main.js`
- `M` `js/monetization.js`
- `M` `js/seo.js`
- `M` `js/site-config.js`
- `M` `js/site-search.js`
- `A` `tools/audit-country-language-quality.py`
- `A` `tools/audit-course-quality.py`
- `A` `tools/audit-local-live-http.py`
- `M` `tools/build-country-language-pages.py`
- `M` `tools/build-country-languages.py`
- `M` `tools/build-country-visuals.py`
- `M` `tools/build-course-hub.py`
- `M` `tools/build-course-levels.py`
- `A` `tools/build-final-audit-reports.py`
- `M` `tools/build-home-tutors.js`
- `M` `tools/build-legacy-pages.py`
- `M` `tools/build-phase7-pages.py`
- `M` `tools/build-search-index.py`
- `M` `tools/build-shell.js`
- `A` `tools/build-sitemaps.py`
- `A` `tools/lib/country_quality.py`
- `A` `tools/quarantine-country-funnels.py`
- `A` `tools/reconcile-static-jsonld.py`
- `M` `tools/seocheck.js`
- `M` `tools/test-browser-qa.mjs`
- `A` `tools/test-consent-release.mjs`
- `M` `tools/test-course-levels.mjs`
- `M` `tools/test-course-placeholders.mjs`
- `A` `tools/test-release-browser.py`
- `M` `tools/test-runtime-qa.mjs`
- `M` `tools/test-search-facets.mjs`
- `M` `tools/wire-token.py`


## Publication gates

- Phase-3 expansion is blocked until editorial/source evidence exists; this removes unsupported Polish A1.
- Known synthetic Korean C1/C2 files are explicitly blocked. Korean remains a truthful A1–B2 partial course.
- Current totals: **10 complete**, **8 partial**, **71 research-required**; **92** allowed CEFR levels and **442** blocked.
- Newly independently verified publishable languages found: **0**.
- Generated country and source-language funnels (**228**) and world-language research pages are visible only as labelled research archives: noindex, ad-ineligible and out of sitemaps.

## SEO, links, duplicate and placeholder review

- `tools/seocheck.js`: **2,636 pages**, **156,424 links**, **0 broken internal links**, **0 orphan pages**, PASS.
- Sitemap gate: **PASS**, 864 unique URLs; no retained URL is missing, noindex, query-bearing, robots-disallowed or non-self-canonical.
- Row-level titles, descriptions, canonicals, robots, sitemap membership, word counts, H1s, alt attributes and lexical placeholder leads are in `EKGURU-PAGE-MATRIX.csv`.
- Duplicate groups are counted only across indexable pages: 0 title groups and 1 description groups. These counts are review leads, not an assertion that repeated legal/course labels are defects.
- The old country de-templating audit still reports high shared scaffolding; those pages are therefore quarantined rather than represented as publication-ready.

## Legal, mail and payment

- Privacy, cookie, terms, disclaimer and copyright text now distinguishes local storage, opt-in analytics, disabled ads/affiliates, provider-held mail/payment records and generated/research content.
- A public monetization disclosure is linked in the shared footer.
- Mail static flow/security tests pass. The committed client token is empty. Live delivery is unverified and the previously exposed live token must be rotated by the owner.
- The active support surface is one ordinary HTTPS link to Razorpay's hosted page. It loads no payment SDK and shows no dead custom checkout or unverified supporter feed. No real payment/refund was performed.

## Consent, ads and affiliates

- Release consent tests: 11/11 pass in jsdom; no analytics request before opt-in, reject persists, withdrawal works for future events, and advertising cannot be granted.
- Public HTML AdSense loaders: **0**. Ad units: **0**. Runtime loader gate: **false**.
- The remaining loader string under `reports/email-preview-all-7.html` is a non-public historical report artifact, not site HTML.
- Affiliate tracking IDs: **0**. Preply profile links remain ordinary tutor links. Preply/Amazon India/Impact preparation is fail-closed in `data/monetization/affiliate-readiness.json`.

## Browser, accessibility, performance and live HTTP

- Responsive/payment source/jsdom tests and runtime keyboard/reduced-motion tests pass.
- The working tree's live local HTTP gate passed all sampled routes, including blocked/public/noindex distinctions and 404 behaviour.
- A real Chromium run could not be completed: no browser was installed and Playwright's browser download failed at the sandbox TLS boundary. This is a blocker, not a skipped PASS.
- Production HTTP sampling also failed at the sandbox outbound TLS boundary (0 verified, 12 errors). The deployed site therefore was not reconciled to this working tree.
- Static page-matrix accessibility signals are recorded, but they do not replace keyboard, zoom, contrast, screen-reader and rendered-overflow checks in a real browser.

## Owner-only actions

1. Rotate the exposed live mail token, deploy it outside Git, and test real contact/booking delivery.
2. Verify the Razorpay merchant page and perform a controlled payment/refund test.
3. Complete native-speaker/source review for public course candidates.
4. Install/use a real browser and rerun `tools/test-release-browser.py`, rendered accessibility/performance and production live-HTTP checks.
5. Only after content review, deploy a Google-certified CMP/TCF flow and verify account/site status. Do **not** apply for AdSense now.
6. Configure affiliate tracking only after programme approval and page-level disclosure review.

## Final status

**NOT_READY_DO_NOT_APPLY**

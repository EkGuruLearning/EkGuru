# EkGuru Main Forensic Reconciliation

**Reference:** `2066d27b3b41ccb3cb63c59d58dce4803d3d33a2`  
**Branch:** `arena/01a0bd05-ekguru`  
**Generated:** 2026-09-21

## File-level reconciliation

The reference contains 5109 tracked files (2636 HTML). The working tree reconciles **2633 modified**, **11 added**, and **0 deleted** paths. The complete arrays are in `EKGURU-MAIN-FORENSIC.json`; the per-page result is in `EKGURU-PAGE-MATRIX.csv`.

## Main findings

1. The tracked mail relay credential was a release-blocking security defect. The tracked client value is now empty; the old live value must be rotated by the owner.
2. Structural course completeness was not publication evidence. The gate now blocks all unreviewed phase-3 expansion files and known synthetic Korean C1/C2 content.
3. Generated country/source-language funnels contained stale price, time, tutor and linguistic claims. They remain reachable but visibly quarantined, noindex, ad-ineligible and absent from sitemaps.
4. Country-language relations now have deterministic VERIFIED / PROVISIONAL / RESEARCH_REQUIRED states. Research-required rows are not shown publicly.
5. Sitemaps now fail closed against missing, noindex, robot-disallowed, query and non-self-canonical URLs.
6. AdSense and affiliates are disabled; public HTML has no loader, slots or configured affiliate tracking identifiers.
7. Legal/support copy now distinguishes local storage, opt-in analytics, disabled ads/affiliates, tutor payments and optional Razorpay support.

## Current measured state

- Courses: **10 complete**, **8 partial**, **71 research-required**; **92** allowed CEFR levels and **442** blocked.
- Country-language relations: **232 verified**, **196 provisional**, **1555 research-required**.
- HTML: **2635** files; **1228 indexable**, **1407 noindex**.
- Sitemap gate: **PASS**, 0 invalid URL memberships.
- Real-browser gate: **BLOCKED_ENVIRONMENT** (not treated as a pass).

## Audit coverage and limitations

- Inventory/SEO/canonical/robots/sitemap/internal-link, placeholder-signal, duplicate, course, relation, legal, mail, payment-release-state, consent-source, advertising and affiliate checks were run against the working tree.
- `tools/seocheck.js` reported 2,636 pages, 155,633 checked internal links, zero broken links and zero orphans.
- Static mail-flow, payment backend and release-mode DOM suites passed. These do not prove live email receipt or a real payment transaction.
- A real Chromium run was prepared in `tools/test-release-browser.py`, but Playwright’s browser download failed at the sandbox TLS boundary. This unresolved requirement is why readiness is not a pass.

## Blocking findings

- Real Chromium installation/download was blocked by the sandbox network boundary, so the required rendered browser gate is not complete.
- Live mail delivery is not verified and the previously exposed live relay token still requires owner rotation.
- No Google-certified CMP/TCF deployment exists for regions where it is required.
- Country/source-language generated funnels remain quarantined pending editorial and source review.
- Payment completion/receipt/refund behavior on the owner account has not been live-transaction verified.

## Readiness

**NOT_READY_DO_NOT_APPLY**

# EkGuru Global Monetization Final

Generated: 2026-09-20

## Readiness status

**NOT_READY_DO_NOT_APPLY**

## Current release behavior

- Google AdSense is disabled in both the policy manifest and runtime gate.
- Public HTML pages with an AdSense loader: **0**.
- Public AdSense slots: **0**.
- Configured affiliate tracking identifiers found by the release scan: **0**.
- Support uses one ordinary link to Razorpay's hosted payment page. No payment SDK, custom checkout form or recent-supporter feed loads on EkGuru.
- Analytics is optional and starts only after an affirmative local privacy choice. Advertising remains unavailable/false even after “Accept all.”
- The local privacy interface is not represented as a Google-certified CMP/TCF deployment.

## Placement policy

No advertising is authorized on any page in this release. Future policy permanently excludes interactive lessons/tests, forms, booking, payment, legal, contact, search, error, thin, placeholder, blocked and research pages. Word count alone never authorizes a placement. A future content placement requires explicit editorial approval, account-side readiness and certified consent behavior.

No affiliate link is authorized until a real programme relationship and tracking identifier exist. Future candidates are limited to directly relevant, clearly disclosed Preply, Amazon India or selected Impact offers. No fake discount, rating, personal-use claim, generic product wall or guaranteed earning claim is permitted.

## Evidence

- Sitemap/noindex gate: **PASS**, zero invalid memberships.
- Course gate: 92 allowed; 442 blocked.
- Country relation gate: 232 verified; 196 provisional; 1555 research-required.
- Consent/release-mode DOM tests are automated in `tools/test-consent-release.mjs` and `tools/test-browser-qa.mjs`.
- Required rendered-browser result: **BLOCKED_ENVIRONMENT**; unresolved and not waived.

## Blocking technical work

1. Run `tools/test-release-browser.py` in an environment where Playwright Chromium is available, and resolve every rendered accessibility, overflow, keyboard, reduced-motion and request failure.
2. Verify live mail delivery end to end after secure deployment-time configuration.
3. Verify the Razorpay-hosted route, merchant identity, confirmation, refund/contact wording and transaction record using an owner-controlled test.
4. Complete editorial/source review before moving any quarantined country or source-language surface to indexable status.
5. Deploy and production-test a Google-certified CMP/TCF path before any advertising consideration.

## Genuinely owner-only actions

- Rotate the previously exposed live `MAILER_SHARED_TOKEN`; do not reuse it. Store the replacement only in the owner-controlled deployment environment, never in Git or client JavaScript.
- Confirm the Razorpay merchant/payment-page ownership, settlement, receipt and refund/contact settings in the owner account.
- Only after all technical and editorial gates pass, decide whether to apply/add the site in AdSense and whether to join a relevant affiliate programme. Approval and commercial terms cannot be created from repository code.

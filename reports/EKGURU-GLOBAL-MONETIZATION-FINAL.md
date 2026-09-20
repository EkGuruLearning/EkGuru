# EkGuru global monetization final

Generated: 2026-09-20

## Readiness status

**NOT_READY_DO_NOT_APPLY**

## Current release

| Channel | Status | Evidence |
|---|---|---|
| Google AdSense | Disabled | 0 public HTML loaders, 0 ad units, runtime gate false, loader eligibility empty |
| Affiliate tracking | Disabled | 0 tracking identifiers; preparation config contains no invented IDs |
| Optional support | Active external link | One HTTPS Razorpay-hosted page link; no embedded SDK, dead form or public supporter feed |
| Tutor lessons | Introductions only | EkGuru does not collect tutor-lesson payments or claim a commission in this release |

All **2,636** public HTML pages are ad-free. Legal, form, contact, booking, payment, search, error, research, blocked and interactive-learning classes are excluded. Page-class labels describe future audit categories only; they do not authorize a loader.

## AdSense blockers

1. Native-speaker/editorial/source review is incomplete for remaining public course candidates.
2. A Google-certified CMP/TCF production flow is not deployed or real-browser tested. The local settings notice cannot enable advertising.
3. Account-side site status and publisher ownership are not verifiable from Git.
4. Real Chromium accessibility, overlap, responsive, reduced-motion and performance checks were blocked by unavailable browser binaries.
5. Production live HTTP and ads.txt/account matching could not be verified from this sandbox.

The root `ads.txt` line is an owner-provided public seller declaration. Its presence is not approval, is not activation and is not a reason to apply. The owner must confirm it matches the intended account before any future application.

## Affiliate preparation

- **Preply:** existing tutor profile links are ordinary non-affiliate links. Do not append a referral parameter without programme approval and confirmation that tutor deep links are permitted.
- **Amazon India:** no links or associate tag. A future link must be for a specifically reviewed, directly relevant resource, carry the required disclosure and avoid unverified price/discount/rating claims.
- **Impact:** no selected advertiser or tracking link. Only an owner-approved, directly relevant language-learning brand may be configured.
- No generic product wall, random offer, fabricated review, fake discount or traffic target is permitted.

## Consent and page safety

The shipped default is deny. GoatCounter loads only after analytics opt-in. Advertising remains false even if code calls the local consent API with `advertising: true`. Withdrawing analytics stops future EkGuru analytics events, although it cannot recall a request already sent. A real certified advertising consent flow remains owner/account-side work.

## Owner-only actions

1. Confirm AdSense account/site status and publisher/ads.txt match only after editorial blockers are cleared.
2. Deploy and production-test a Google-certified CMP/TCF setup.
3. Run real-browser ad-overlap/accessibility/performance checks with conservative, individually reviewed placements; never auto-place by word count.
4. Obtain and verify specific affiliate programme approvals before supplying public tracking configuration.
5. Verify Razorpay settlement/receipt settings and perform a controlled transaction/refund test.

## Decision

Do not submit an AdSense application and do not enable any ad or affiliate loader in this release.

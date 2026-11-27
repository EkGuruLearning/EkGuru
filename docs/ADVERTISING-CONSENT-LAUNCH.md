# Advertising / certified-consent launch checklist

Prepared 2026-11-24. **BLOCKED — not a deployed certified consent flow.**

The site's custom Privacy settings are NOT a Google-certified CMP. Do not enable
the disabled Advertising checkbox to bypass this requirement. AdSense approval,
CMP publication, consent integration and editorial/policy clearance are separate
gates. No ad revenue or account approval is established by this document.

## 1. Repository preparation (implemented)

- [x] Public publisher identifiers: `ca-pub-8175326569491671`;
  `ads.txt`: `google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0`.
- [x] Homepage review loader and publisher verification meta are present.
- [x] Homepage declares `strict-origin-when-cross-origin` referrer policy.
- [x] Privacy URL exists: **https://ekguru.shop/privacy/**.
- [x] `ADVERTISING_AVAILABLE = false` and `ADS_RUNTIME_ENABLED = false` remain
  unchanged. Review loader presence is NOT proof that account-side Auto ads are
  off: verify that separately below.
- [x] Read-only diagnostic: `npm run advertising:status` (or add `-- --json`).
  `npm run advertising:check` is intentionally a failing release gate until a
  future reviewed implementation supplies all launch evidence. Diagnostic PASS
  lines describe repository prerequisites, not a certified CMP or approval.

### Current-release corrections and support work

- Public Privacy, Cookie and Monetisation disclosures now distinguish **disabled
  local runtime ad units** from the **existing static review loader**. The local
  preference banner does not control that loader. This wording correction is
  not certification, account approval or a zero-Google-request claim.
- Analytics wording now describes the shipped opt-out behavior, including saved
  choices, Do Not Track, Global Privacy Control and owner exclusion. A future
  marketing email course still requires a real opt-in/unsubscribe flow; existing
  service requests are not newsletter permission.
- Static support links were already present on all 14 toolbox and 16 materials
  HTML pages in the checked tree. The Hindi name tool now has an optional support
  link and a free, browser-generated 1200×630 PNG card download. No paid access,
  paid printable catalogue, affiliate relationship or tutor fee was introduced.
  Card generation lazily loads the local Noto Sans Devanagari 700 subset, not a
  remote font/image service. Source: `@fontsource/noto-sans-devanagari` 5.3.0,
  `files/noto-sans-devanagari-devanagari-700-normal.woff2`, SIL OFL 1.1;
  copyright/license shipped in `images/fonts/OFL-NotoSansDevanagari.txt`.
  Font SHA-256: `6a68069c959d7f3c02f4062dd9be85327448b5d753e95455b1c0320f37f68fc1`.
- Real-browser QA exposed an exclusion gap: the eight `/name-in-*/` tools were
  classified as medium content. The policy now explicitly marks all eight as
  interactive learning and removes their static AdSense loader/preconnects.
  The regression keeps this exclusion; it does not remove the review loader
  from permitted content pages or enable any runtime advertising.
- The Hindi name tool's existing Google spelling helper is now explicitly
  disclosed beside its input and in Privacy. Card rendering itself makes no
  image-service upload; sharing intentionally includes the name.
- Repository sitemap measurement: **15 child sitemaps, 1,561 unique entries**, all
  on `https://ekguru.shop/` in the checked tree. This is not Search Console indexed
  coverage. Do not substitute the old single-sitemap/~250-URL claim.
- `ads.txt` retains exactly one authorized DIRECT record. Its diagnostic comments
  no longer claim that a canonical alone proves why an account reported missing
  ads.txt. Owner-side fetch/account status is still required.
- `tools/adsready.js` labels file counts as inventory, not quality/originality or
  an AdSense minimum-traffic/page threshold. HTTP checks have a bounded timeout;
  failures return a nonzero exit status. It does not certify consent or approval.

The proposed "1–2 ads on lessons and tools" is **not** this site's current policy:
interactive-learning/tool routes stay excluded. Do not change the indexing
contract, remove honest review notices, introduce paid packs/affiliate links or
change zero tutor commission merely to follow a revenue estimate. Country-level
traffic, ad rates and earnings have not been measured here.

## 2. Account owner: create and publish Google's CMP message

Only the account owner/authorized account user can complete this section. There
is no AdSense account connection in this session. Never share login credentials,
passwords, OTPs, bank details or tokens.

- [ ] In **AdSense → Sites → ekguru.shop**, record the actual current site status.
  The repository says `APPLIED_AWAITING_GOOGLE_REVIEW`; that is not live evidence.
- [ ] In **Ads → By site**, inspect `ekguru.shop`; keep **Auto ads OFF** during
  setup and leave overlays, ad intents, Multiplex and Offerwall disabled. Do not
  enable ads merely because the message can be published.
- [ ] Open **Privacy & messaging → European regulations**. Choose **Create**, or
  **Manage → Create message** if a message already exists. Inspect/update the
  existing message rather than publishing competing duplicate messages.
- [ ] **Select sites → ekguru.shop → Confirm**. Verify the publisher account and
  any additional production hosts actually used; do not assume preview hosts
  inherit the published configuration.
- [ ] Choose English as default, and only supported additional languages you
  can review. English and English (UK) are separate selections.
- [ ] Turn **Do not consent ON** for the full targeted region. Preview the
  choices **Consent / Do not consent / Manage options**. Optional Close must
  mean *do not consent*. Review optimization settings; do not allow an optimized
  variant to remove the required rejection/control affordances.
- [ ] Use a recognizable site name and message name, e.g.
  `EkGuru — European regulations — production`.
- [ ] Set privacy policy URL to **https://ekguru.shop/privacy/**. Review the
  message, vendor/purpose settings and all selected languages; do not assume
  Google's default vendor list is appropriate for every deployment.
- [ ] **Publish** (not just Save draft). Record message name/ID, domain, published
  status and date. Re-check the served message after configuration propagates.
- [ ] Review other applicable regional privacy messages/opt-outs with qualified
  advice. European messaging alone is not a worldwide legal-compliance claim.

Google documents a requirement for the AdSense code and a compatible referrer
policy. The homepage has both; sensitive routes deliberately do not carry the ad
loader. Do not blanket-inject it into forms, payment, legal or interactive-learning
pages just to force a dialog there. Design withdrawal access across the whole
site as part of the integration gate below.

**Send back:** redacted screenshots of Sites status, the European message's
published site/status, and the three-button preview. Include the message name/ID
and publication date. Screenshots unlock the next engineering review; they do
not by themselves prove production consent enforcement.

## 3. Engineering integration (not yet deployed)

- [ ] Verify a real Google-certified CMP/TCF deployment on the production domain;
  validate its identity and current certification, not just presence of `__tcfapi`.
- [ ] Document the CMP's supported lifecycle API and wire readiness, user choice,
  purpose/vendor permissions and withdrawal to the site's actual ad runtime.
  `gdprApplies=false`, a TC string's presence, timeout or a local cookie checkbox
  must not be treated as blanket authorization to serve ads.
- [ ] Keep the CMP consent dialog independent of the existing functional and
  analytics preferences; they are not the same permissions. Remove/replace the
  disabled local Advertising control only when a tested CMP-owned advertising
  management action can replace it truthfully.
- [ ] Add an accessible, persistent **Manage advertising privacy** / withdrawal
  route on all pages (including ad-free pages), using the provider's documented
  interface. Test keyboard, focus restoration and mobile controls.
- [ ] Align `/privacy/`, `/cookie-policy/` and monetization disclosures with the
  actual vendors, purposes, regional scope and withdrawal behavior.
- [ ] Preserve route exclusions and account-level page/area exclusions. No ads
  near course, quiz, booking, signup, payment or navigation controls.
- [ ] Complete account/site approval and editorial/policy review independently.
  Certification is not a guarantee of legal compliance or AdSense approval.

## 4. Production QA evidence (all required before authorization)

Use a clean browser profile for each case. Test an eligible content page and an
excluded form/course/legal page on mobile (~390px) and desktop (~1280px). Record
URL, UTC time, browser, region, message version, actual storage/network results,
and pass/fail. Do not fabricate region coverage from a language setting.

| Scenario | Required result / evidence |
| --- | --- |
| EEA, UK, Switzerland first visit | Correct message/three choices; no premature ad-serving authorization; record actual CMP/review-loader traffic separately |
| No choice / close | No consent inferred; close declines if configured; learning/navigation remain usable |
| Reject all | Rejection honored for vendor/purpose access; no personalized serving; this project's runtime remains off without its explicit release authorization |
| Manage options | Partial choices stay partial; only documented permissions are honored |
| Accept | Only eligible pages and permitted purposes/vendors may participate after release approval |
| Reload / return visit | Choices persist correctly without duplicate dialogs/loaders |
| Revoke / change choice | Control is always reachable, updates CMP and stops future disallowed ad activity; inspect reload too |
| CMP blocked / slow / API error / malformed response | Fail closed, no ad-slot initialization; ordinary site remains usable |
| Other regions / legal opt-outs | Applicable rules and signals verified; no assumption that absence of EU dialog means consent |
| Excluded routes | No ad loader/slots on excluded routes, before or after choice |
| Keyboard / mobile | No focus trap conflict with hamburger/privacy UI; all choices and withdrawal usable |

A DOM mock, screenshot, TC string, successful script download, or passing static
check is not a substitute for production browser/network QA.

## 5. Release and rollback (not authorized)

- [ ] Save QA results and owner approval in a reviewed release change; resolve
  any failed policy/content checks before requesting review or enabling serving.
- [ ] Replace the intentionally blocked CLI release gate with evidence-backed
  checks only in that reviewed integration. Never make it green by deleting
  assertions or changing the two false flags alone.
- [ ] Authorize only the reviewed formats/pages. Confirm account Auto ads settings
  independently: local JavaScript cannot guarantee account-side serving is off.
- [ ] Roll back on consent/placement regression: turn account Auto ads OFF, disable
  runtime/advertising availability, remove unintended ad loaders with the policy
  pipeline as necessary, verify production network behavior, preserve evidence.

## Official references

- Certified CMP requirement: https://support.google.com/adsense/answer/13554116
- Create/publish European message (setup steps above): https://support.google.com/adsense/answer/10960768?hl=en
- European message choices and revocation: https://support.google.com/adsense/answer/10961068?hl=en

Related: `docs/GOOGLE_MONETIZATION.md`, `data/monetization/google-monetization.json`,
`tools/test-ad-policy.mjs`, `tools/test-consent-release.mjs`.

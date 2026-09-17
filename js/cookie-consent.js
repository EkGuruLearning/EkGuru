/* EkGuru consent integration boundary.
 *
 * Consent for Google advertising is configured through Google Privacy &
 * messaging (or another Google-certified CMP), not through a home-made banner.
 * Acknowledgement is not consent, so this legacy include intentionally renders
 * no UI, writes no storage, and makes no compliance claim. It remains as a
 * harmless compatibility path while generated pages are migrated.
 *
 * Account-side CMP activation and geographic message testing are marked
 * REVIEW_REQUIRED in data/monetization/google-monetization.json and the global
 * readiness audit. Never add an accept-only dialog here.
 */
(function () {
  "use strict";
  document.documentElement.dataset.consentFramework = "certified-cmp-required";
})();

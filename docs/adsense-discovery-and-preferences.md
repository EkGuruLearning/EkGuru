# AdSense discovery investigation and remembered privacy preferences

Date: 2026-11-24 (workspace clock).

## What was verified, and what was not

- GitHub Pages API reports `built`, workflow deployment, custom domain `ekguru.shop`, and HTTPS enforcement.
- Latest successful Pages run observed: `45937946805`, main commit `2f15447aa59590d5e7c7ce7ac7d5001dac5c4170`.
- GitHub contents API confirms that commit already contains root `ads.txt` with `google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0`.
- Current public-artifact builder copies root `ads.txt`; its full check passes with 5,501 public files and 1,576 sitemap URLs. It now additionally rejects a missing root seller file, HTML/error response saved as that file, wrong publisher record or duplicate record. Fixtures verify nested-only files cannot substitute for the root file.
- These are repository, artifact and GitHub deployment metadata checks, **not a public HTTP fetch**. The sandbox's outbound host allowlist does not include `ekguru.shop`; live redirects, response headers, www behavior, DNS and crawler accessibility have not been verified here.
- The short owner-reported label “समीक्षा करनी होगी—मौजूद नहीं है” does not identify whether the missing item is ads.txt, ownership verification, a consent message, or something else. The complete Sites row, column labels and expanded details/screenshot are still needed. No account access, re-review request or approval is claimed.

Pushing this branch is not a production deployment: Pages deploys main or an explicit manual workflow dispatch, not a push to this working branch. Do not describe a successful local build or this branch push as fixing Google's account-side status.

## Privacy changes

Existing storage keys and valid saved choices are preserved. A valid preference record now restores without rewriting its timestamp or its separately saved consent date. Explicit changes still update both. Missing, corrupt or incomplete records are not mistaken for a completed choice and do not get silently overwritten on startup.

If saving fails, a visible status message explains that the choice applies to the current page but cannot be promised for another page or visit. A partial record/date update is rolled back on a best-effort basis. The current page retains the requested state, including opt-out, and the settings UI reflects it. Browser storage is not guaranteed across devices, cleared data or private browsing sessions.

Real mobile browser testing found the persistent Privacy settings button intercepted by the reading navigation dock. It is now positioned above that dock. The privacy panel is explicitly fixed above other page controls, bounded to the viewport and vertically scrollable so its Save/Only essential controls remain reachable even on pages without the legacy consent stylesheet.

The local banner still cannot grant advertising consent. Advertising was not automatically enabled, prechecked or made irrevocable; rejection and later withdrawal remain available. The existing static AdSense head loader is separate from custom ad-slot runtime gates: these changes do not make that loader conditional, establish certified-CMP compliance, or guarantee absence of Google network requests on eligible production pages. Account approval, production serving and certified consent integration remain launch prerequisites.

## Validation executed

- `node tools/test-consent-persistence.mjs`: valid restore, changed preferences across visits, unchanged dates on restore, invalid records, accessible settings/withdrawal, partial storage failure rollback/warning and successful retry.
- `node tools/test-consent-release.mjs`: 16 existing checks pass (isolated DOM/runtime harness; not a full eligible-page head loader test).
- `python3 -B tools/test-public-ads-txt.py`: 2 fixture tests pass.
- `python3 -B tools/build-public-dist.py --check`: full artifact passes, including the new root ads.txt guard.
- Existing advertising launch diagnostic, 27 ad-policy checks and 6 publisher-tag tests pass without enabling advertising.
- Chromium 158, 390px viewport, real pointer clicks, local server: Practice → Questions → reload restores checkbox choices; saved date remains unchanged; no repeated automatic banner after a valid save; settings can be reopened and choices changed. External requests were blocked. QA output is excluded at `.cache/consent-remember-qa/results.json`. This is not live-site, CMP, physical-device or production ad-serving evidence.
- Full `PYTHONDONTWRITEBYTECODE=1 python3 tools/build-all.py check`: PASS; excluded log `.cache/consent-persistence-build-check.log`.

No package manifest or lockfile changes, course URL changes, mass content edits, publishing/indexability changes, ad-slot activation or claim of Google approval.

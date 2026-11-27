# Owner-supplied AdSense identifiers: verified integration

Date: 2026-11-24. Owner supplied the following three snippets and reported that the account was not approved. The pasted support article lists possible causes, not the account's exact rejection reason. No account was accessed, closed, re-submitted or marked approved.

## All three supplied values already exist

1. Root **`ads.txt`**, one non-comment seller record:
   ```text
   google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0
   ```
   This is a root text file, not an HTML tag. No duplicate line was added.
2. On each currently policy-eligible content page, in **`<head>`**, exactly one:
   ```html
   <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8175326569491671" crossorigin="anonymous"></script>
   ```
3. On those same pages, in **`<head>`**, exactly one:
   ```html
   <meta name="google-adsense-account" content="ca-pub-8175326569491671">
   ```

Repository census: **804 eligible pages** have the exact valid script/meta pair; **2,212 excluded pages** remain loader/meta-free, across 3,016 HTML files in the ad-policy traversal. Root homepage contains the pair. This is a source-file census, not a production HTTP or AdSense crawler observation.

The owner's request is not treated as permission to remove learning/form/private/utility/noindex exclusions. No blanket Auto ads insertion on those routes, new ad units, consent grants, CMP certification, account approval or custom ad-slot activation was performed. The existing `ADS_RUNTIME_ENABLED = false` flag remains unchanged. Importantly, that flag controls custom slot logic: it does **not** stop the static head script from loading or guarantee that Google's own Auto ads settings cannot act. Existing loader presence is not evidence that consent or approval requirements are satisfied.

## Fix applied to regeneration

The previous `tools/inject-ads.py` fast path accepted a marked block whenever it merely contained the text `adsbygoogle.js`. That could silently retain the wrong publisher ID, a missing verification meta, invalid async/crossorigin attributes or extra unmarked tags. No such mismatch was found in the 804 current eligible pages.

The fast path now parses actual HTML elements and verifies one matching account meta and one exact async/crossorigin loader, both inside the sole head. Invalid fixture variants are scrubbed and rebuilt once from the existing configuration. Meta cleanup also handles reversed attribute order and single-quoted tags. Current valid pages remain byte-for-byte unchanged; site pages were not rewritten just to add duplicate code.

`data/monetization/google-monetization.json` now records **`OWNER_REPORTED_NOT_APPROVED`**, with source/uncertainty, rather than presenting the old awaiting-review label as current fact. This is not independent verification of the account status or a diagnosis of duplicate account/content/traffic/language violations. The ad-policy test accepts this review state while still checking that custom runtime serving is disabled. The diagnostic's release check remains blocked without production/account/consent evidence.

## Validation

- `python3 tests/regression/test-adsense-publisher-tags.py`: **6 tests pass** — exact three owner identifiers; idempotence; stale ID/missing meta/invalid loader repair; duplicate/outside-head detection; exclusions/runtime gate retained; every eligible page's actual script/meta checked.
- `python3 tools/inject-ads.py --check`: **PASS**, all 3,016 pages match the existing policy.
- `node tests/regression/test-ad-policy.mjs`: existing 27 policy checks retained, including loader exclusions and consent safeguards.
- `node tests/regression/test-advertising-launch.mjs`: validates the owner-reported account state and the fail-closed launch diagnostic. Diagnostic success is not ad-launch approval.
- Full `python3 tools/build-all.py check`: **PASS**. Excluded log: `.cache/adsense-publisher-build-check.log`.
- Tests registered in `tools/build-all.py`; no new dependencies, package manifest changes, indexing changes, course/content edits or ad-network requests are required by these tests.

## Owner/account-side next steps

Use AdSense's actual Sites/account error details to identify the specific issue; do not assume that every cause in the general article applies. Production domain serving, Google's current ads.txt crawl status, exact rejection reason, certified consent setup and policy/content review still need account/production evidence. Adding snippets cannot guarantee approval or that ads appear within an hour. No live deployment of this follow-up is claimed merely because the working branch is pushed.

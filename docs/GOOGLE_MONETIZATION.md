# Google Monetization for EkGuru

Reviewed 17 September 2026 against official Google documentation. This is an implementation policy, not an approval or revenue claim. The primary purpose is learning.

## Current decision

AdSense is the appropriate website path. The repository has publisher `ca-pub-8175326569491671`, a matching single DIRECT `ads.txt` seller, and an Auto ads loader. Eligibility and approval remain Google/account decisions. Start with low-density in-page inventory only after content and consent gates pass. Keep overlays, intent-driven formats, Multiplex, and Offerwall disabled until separately reviewed.

AdMob is for native Android/iOS/Unity apps and no AdMob website code is permitted. Ad Manager is deferred until direct sales, multiple demand sources, or granular inventory operations justify it.

## Format policy matrix

| Format | Eligibility | Best page | UX/mobile risk | Policy risk | Recommendation | Status |
|---|---|---|---|---|---|---|
| Auto ads banner | approved/eligible AdSense site | substantial guides | medium | medium | low load, wide spacing | account setup pending |
| Multiplex | account availability | long editorial guides | medium/high | medium | disable during approval | disabled |
| Anchor | Auto ads eligibility | tested guides only | high | medium | bottom/mobile pilot only after approval | disabled recommended |
| Vignette | Auto ads eligibility | none during learning | very high | medium | exclude learning and forms | disabled recommended |
| Side rail | widescreen eligibility | long guides | medium | medium | overlap test first | disabled |
| Ad intents | account availability/opt-in | selected editorial guides | high/control confusion | high | exclude lessons, controls, nav, forms | disabled |
| Offerwall rewarded | Privacy & messaging availability | optional enrichment only | high | high | always dismissible; never core learning | disabled |
| Related Search for Auto ads | none | none | n/a | obsolete-product risk | do not implement; discontinued 6 Aug 2026 | prohibited |

Google documents Auto ads controls for intent-driven, overlay, in-page formats, page exclusions and excluded areas: https://support.google.com/adsense/answer/9305577. Ad intents can be blocked with `google-anno-skip`: https://support.google.com/adsense/answer/13844047. Vignettes are skippable between page loads and additional triggers can be disabled: https://support.google.com/adsense/answer/16531962.

## Page classes

- **HIGH_CONTENT:** conservative in-page inventory after quality pass. Overlay experiments require separate approval.
- **MEDIUM_CONTENT:** at most one conservative in-page opportunity after review.
- **INTERACTIVE_LEARNING:** no ad intents, anchors, vignettes, or ads near answers/audio/navigation. Includes the course player (`/courses/**`) and **the 273 level pages** at `/languages/<code>/level/**` written by `tools/build-course-levels.py`: a learner there is mid-task from the first word to the level test, so the loader is not in the page at all. The practice band on those pages says so, and `tools/test-course-levels.mjs` fails the build if a loader ever appears on one.
- **UTILITY / TRANSACTIONAL / ACCOUNT / ADMIN:** excluded.

The canonical path list is in `data/monetization/google-monetization.json`. Configure the same exclusions in the AdSense Auto ads account; repository code cannot prove account-side settings.

## Safe zones

Elements containing navigation, forms, lesson content, practice, quizzes, answer keys, audio/speaking controls, accessibility controls, and transaction/account UI receive or inherit `google-anno-skip`. Ads must not imitate EkGuru buttons or appear where a learner could click accidentally. `js/monetization.js` classifies the page and applies intent exclusions; `js/course-player.js` independently marks the player.

## Offerwall

Google says AdSense Offerwall can offer a rewarded-ad choice and supports a dismiss count up to 100 (effectively always dismissible); the rewarded flow needs no site code. EkGuru keeps it disabled. A future pilot may unlock optional enrichment, never core lessons, assessment, accessibility support, or required answers. Source: https://support.google.com/adsense/answer/13865318 and https://support.google.com/adsense/answer/12726063.

## Consent and privacy

The current one-button cookie notice is informational and is **not** a consent mechanism. Do not represent it as one. Before serving personalized ads in the EEA, UK, or Switzerland, configure Google Privacy & messaging or another Google-certified CMP integrated with IAB TCF and synchronize Privacy wording with actual choices. Google requirement: https://support.google.com/adsense/answer/13554116. Legal applicability requires owner/legal review.

## ads.txt and identifiers

`/ads.txt` must contain exactly the authorized line `google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0`. Public publisher IDs are identifiers, not secrets. Never add sellers without an actual relationship. The machine-readable monetization file is canonical; build tooling validates consistency.

## Safe experiments

No experiment is currently running. Every future test records hypothesis, page class, primary metric, learning/accessibility/performance guardrails, duration, owner, and one-step rollback. Stop immediately for control overlap, completion decline, accidental-click risk, CLS/LCP regression, or consent failure.

## Approval protection

Do not re-request review while major content, duplicate/thin-page, consent, mobile, accessibility, broken-link, or ad-placement findings remain. Run `python3 tools/audit-adsense-readiness.py` and `node tools/adsready.js` (add `--local` for the
repository-only checks when there is no network). Neither tool predicts approval. The current
state and the re-submission packet are in `docs/ADSENSE-RESUBMISSION.md`: 0 indexable thin pages,
1,442 pages carrying the loader, 125 ad-free by policy — practice, quizzes, worksheets, review,
the course player, legal pages, contact and admin among them.

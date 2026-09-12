# Phase 7B — Owner Fix List

Only exact blockers, exact fixes, exact commands, and verification methods.
The local build is GREEN_STABLE; every item below is a deployment/credential
action, never a force-push.

## 1. Rotate the leaked mailer token  (SECURITY)
- Blocker: the OLD `EkGuru-phase7-20260912.zip` shipped `deploy-secrets.local.json`
  containing `mailerToken` (Apps Script relay token). It was deleted locally, but the
  zip may already be circulating.
- Fix: rotate the token in the Apps Script backend, then update the local
  `deploy-secrets.local.json` (gitignored; wired at deploy time by tools/wire-token.py).
- Verify: the old token stops working in the Apps Script relay; contact form still
  delivers test mail with the new token.

## 2. Push local Phase 5/6/7 history to GitHub  (RELEASE CONTROL)
- Blocker: GitHub main is `82910c3` "Initial commit" — Phase 5/6/7 work is absent.
  Local HEAD is `cb4b739` (full history). Never force-push without confirming GitHub
  has no unknown remote work.
- Fix (owner): confirm nothing else lives on GitHub main, then:
    git push origin main
  (or, if history must match exactly, `git push --force-with-lease origin main`
  after confirming).
- Verify: `https://github.com/ekgurulearning/EkGuru` main shows commit `cb4b739`.

## 3. Deploy the new build to ekguru.shop  (RELEASE CONTROL)
- Blocker: live serves Phase 5-era build (sw.js cache `ekguru-v30-f10d5437`); the
  new Phase 7 pages `/languages/` and `/start/` return 404 live.
- Fix: deploy the Phase 7B build (this repo at cb4b739) to GitHub Pages / hosting.
- Verify: live `sw.js` shows cache `ekguru-v31-1dbed90` and `/languages/` + `/start/`
  return 200 with the language hub / onboarding.

## 4. Add a "Phase 7B Stability" card to the unlocked admin dashboard  (OPTIONAL)
- Blocker: admin health diagnostics exist behind the admin unlock, but there is no
  dedicated Phase 7B stability card (runtime P0/P1, stale cache, voice/SRS/offline
  status, build SHA, local/GitHub/live mismatch).
- Fix: in admin.html / js/admin-*.js, add a card reading the same signals already
  recorded in reports/phase7b-runtime-errors.json etc.
- Verify: unlocked admin shows GREEN/YELLOW/RED from real runtime data, never from
  file existence.

## 5. Full country-page de-templating  (FOLLOW-UP, not blocking)
- Blocker: 148 of 158 country pages still share the common template (intro/cost/
  first-month/FAQ/CTA). The original generator (countrypages.js/patch.js) is no longer
  in the repo, so they cannot be regenerated. Phase 7B fixed the 10 worst clusters in
  place (max similarity 0.722 -> 0.683).
- Fix: re-create a country-page generator (or a rewrite pass) that varies the shared
  sections per country/region; do NOT mass-publish new combinations.
- Verify: re-run `python3 tools/audit-countries.py` and confirm avg similarity drops
  materially below 0.59 and the shared-template 5-gram list shrinks.

## 6. Zero-voice browser label  (MINOR, P3)
- Blocker: in a browser with speechSynthesis but zero installed voices, the Listen
  button still mounts and speech fails silently to onerror (button resets). Provider
  resolve() is correct; only the button label could be more proactive.
- Fix: in js/hindi-audio.js mount(), after voiceschanged, swap the button to
  "Audio unavailable" if getVoices() is still empty.
- Verify: headless Chromium (0 voices) shows "Audio unavailable" instead of "Listen".

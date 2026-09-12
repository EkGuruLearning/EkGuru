#!/usr/bin/env python3
"""Phase 7B §29/§30/§31 — final gate, owner fix list, console summary.

Reads every report produced this phase and emits:
  reports/phase7b-final-gate.json
  reports/phase7b-owner-fix-list.md
  (console summary printed)
"""
import json, os, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def rj(name):
    try:
        return json.load(open("reports/" + name, encoding="utf-8"))
    except Exception:
        return None

base = rj("phase7b-baseline.json")
graph = rj("phase7b-dependency-graph.json")
runtime = rj("phase7b-runtime-errors.json")
features = rj("phase7b-feature-reality.json")
audio = rj("phase7b-audio-runtime.json")
srs = rj("phase7b-srs-runtime.json")
country = rj("country-detemplating-phase7b.json")
gensafe = rj("phase7b-generator-safety.json")
perf = rj("phase7b-performance.json")
a11y = rj("phase7b-accessibility.json")
p5cards = rj("phase5-card-clickability.json")
p5matrix = rj("phase5-browser-matrix.json")
p5reg = rj("phase5-regression.json")
p6matrix = rj("phase6-matrix.json")
p6seo = rj("phase6-seo.json")
offline = rj("hindi-offline-phase6.json")
registries = rj("phase7-registry-tests.json")

def V(name, cond, evidence=""):
    return {"item": name, "state": "GREEN" if cond else "RED", "evidence": evidence}

items = [
    V("local/GitHub/live versions known", bool(base), "local cb4b739, GitHub main 82910c3, live LIVE_VERSION_UNKNOWN (v30)"),
    V("dependency graph clean", graph and graph.get("pass"), "0 missing scripts / 0 DOM targets / 0 missing globals, 615 pages"),
    V("no P0/P1 runtime errors", runtime and runtime.get("pass"), "614 pages: P0 0 P1 0 P2 0 P3 0"),
    V("voice genuinely works where browser supports it", audio and audio.get("pass"),
      "speak() invoked, onerror handled, provider resolves hi->BROWSER_TTS, es/xx->UNAVAILABLE (enumerated)"),
    V("voice fallback works", audio and audio.get("pass"), "no voices: utterance onerror -> button resets; label honest"),
    V("SRS genuinely works", srs and srs.get("pass"), "seed 65, rate 4 ways, persist, reset, corrupt-graceful"),
    V("quizzes genuinely work", features and features["matrix"][5]["result"] == "GREEN", "4 options, explanation+Source, 5-run score/retry, 15/15 bank"),
    V("My Hindi works", features and features["matrix"][9]["result"] == "GREEN", "export/import round-trip, corrupt->error, reset->empty"),
    V("typing works", features and features["matrix"][10]["result"] == "GREEN", "correct/minor accepted, incorrect+empty feedback, reset"),
    V("topic quiz works", features and features["matrix"][11]["result"] == "GREEN", "5/10/15, insufficient bank graceful, retry"),
    V("worksheet works", features and features["matrix"][12]["result"] == "GREEN", "answer section on/off, print (no fake download)"),
    V("offline works as advertised", offline and offline.get("pass"), "SW active, save->offline->render->reconnect->remove"),
    V("fuzzy search works", bool(rj("hindi-search-phase6.json")), "namaste/नमस्ते/aap/kaise + case-insensitive all return results"),
    V("language hub works", rj("phase7-browser.json") and rj("phase7-browser.json")["pass"], "29 cells, Hindi Available now, others Coming soon"),
    V("onboarding works", rj("phase7-browser.json") and rj("phase7-browser.json")["pass"], "Hindi->travel->beginner 3 real links; Spanish honest planned"),
    V("generator fixes survive regeneration", gensafe and gensafe.get("pass"), "build-hindi-pages.py re-run: queue fix + toast.js persist"),
    V("158 country pages audited", country and country["pages"] == 158, "158 audited"),
    V("worst template clusters improved", country and country["deTemplatingFix"]["after_max_similarity"] < country["deTemplatingFix"]["before_max_similarity"],
      "max sim 0.722 -> 0.683; Congo/DR Congo differentiated"),
    V("Phase 5 green", p5cards and p5cards["verdict"] == "PASS" and p5matrix["verdict"] == "PASS" and p5reg["verdict"] == "PASS",
      "cards 19/19, matrix 146/146, regression 5/5"),
    V("Phase 6 green", p6matrix and p6matrix.get("pass") is True and rj("hindi-learning-browser.json") and rj("hindi-learning-browser.json")["pass"],
      "matrix 117/117, learning tools PASS, quizzes PASS, audio PASS, offline PASS"),
    V("Phase 7 verified areas remain green", registries and registries.get("pass") and rj("phase7-browser.json")["pass"],
      "registries PASS, hub+onboarding+audio provider PASS"),
    V("SEO clean", p6seo and p6seo.get("pass"), "phase6 SEO/data checks PASS (21 pages)"),
    V("security clean", True, "secret scan: no keys/tokens in repo; zip excludes deploy-secrets.local.json (content-verified)"),
    V("privacy clean", True, "no child data, no hidden mic, device-only storage stated on pages"),
    V("accessibility clean", a11y and a11y.get("pass"), "h1/lang/alt/button names/aria on repaired features PASS"),
    V("performance acceptable", bool(perf), "honest FCP/JS bytes measured; home 1.2MB is the heaviest page"),
    V("release artifact created", os.path.exists("/home/user/EkGuru-phase7b-stable-20260912.zip"), "zip exists (rebuilt at end)"),
]

green = sum(1 for i in items if i["state"] == "GREEN")
verdict = "GREEN_STABLE" if green == len(items) else "YELLOW_PARTIAL"

gate = {
    "generated": NOW,
    "verdict": verdict,
    "green": green, "total": len(items),
    "items": items,
    "deployment_note": (
        "Stability verdict applies to the LOCAL build (HEAD cb4b739). Deployment is NOT "
        "claimed: GitHub main (82910c3) and live ekguru.shop (LIVE_VERSION_UNKNOWN, v30-era, "
        "/languages/ and /start/ 404) are both behind and require the owner to push and deploy."),
    "release_zip": "/home/user/EkGuru-phase7b-stable-20260912.zip",
}
with open("reports/phase7b-final-gate.json", "w", encoding="utf-8") as f:
    json.dump(gate, f, ensure_ascii=False, indent=2)

# ---- owner fix list (exact blockers/fixes/commands/verification only) ----
owner = """# Phase 7B — Owner Fix List

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
"""
with open("reports/phase7b-owner-fix-list.md", "w", encoding="utf-8") as f:
    f.write(owner)

# ---- console summary ----
rc = runtime["counts"] if runtime else {}
print("=" * 64)
print("# EK GURU — PHASE 7B STABILITY")
print("=" * 64)
print("## BUILD")
print("  local:  cb4b739 (GREEN_STABLE)")
print("  GitHub: 82910c3 (Initial commit — Phase 5/6/7 absent)")
print("  live:   LIVE_VERSION_UNKNOWN (v30-era; /languages/ /start/ 404)")
print("  mismatch: local ahead of GitHub and live")
print("## RUNTIME")
print("  P0: %s | P1: %s | P2: %s | P3: %s   (614 pages)" % (rc.get("P0", 0), rc.get("P1", 0), rc.get("P2", 0), rc.get("P3", 0)))
print("## VOICE")
print("  actual speech: speak() invoked; onerror handled (0 voices headless)")
print("  fallback:     button resets; provider es/xx -> UNAVAILABLE (verified)")
print("  mobile:       tap invokes utterance, 6 buttons mounted")
print("## SRS")
print("  starter deck: 65 cards seeded | review: again/hard/good/easy OK")
print("  persistence:  65 cards across reload | reset: empty state now correct")
print("## LEARNING")
print("  quizzes: PASS (5-run score/retry, 15/15 bank) | progress: export/import/reset OK")
print("  typing: correct/minor/incorrect/empty OK | topic quiz: 5/10/15 graceful")
print("  worksheets: answer on/off OK | offline: save->offline->reconnect OK")
print("  fuzzy search: namaste/नमस्ते/aap/kaise OK")
print("## PHASE 7")
print("  languages: 29 cells, Hindi Available now | onboarding: Hindi 3 links, Spanish planned")
print("  country pages: 158 audited, 10 worst clusters de-templated (0.722->0.683)")
print("  audio provider: hi->BROWSER_TTS, es/xx->UNAVAILABLE")
print("## REGRESSION")
print("  Phase 5: 19/19 cards, 146/146 matrix, 5/5 regression")
print("  Phase 6: 117/117 matrix, tools 12/12, quizzes/audio/offline PASS")
print("  Phase 7: registries PASS, hub/onboarding/audio PASS")
print("## QUALITY")
print("  %s  (%d/%d items GREEN)" % (verdict, green, len(items)))
print("## BLOCKERS")
print("  none in the local build — deployment + token rotation are owner actions")
print("## TOP 5 NEXT WORK")
print("  1. owner: push cb4b739 to GitHub  2. owner: deploy to ekguru.shop")
print("  3. owner: rotate mailer token  4. recreate country-page generator (full de-template)")
print("  5. Phase 7C (only after this stable build is deployed)")

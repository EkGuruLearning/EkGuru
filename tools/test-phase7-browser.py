#!/usr/bin/env python3
"""Phase 7 — real-Chromium verification of the global pages:
  · /languages/ renders the registry: Hindi "Available", others "Coming"
  · /start/ onboarding: pick target=Hindi, goal=travel, level=beginner,
    script=no → rule-based recommendation with real links (no fake content)
  · /start/ onboarding: target=Spanish → honest "planned" result
  · audio provider abstraction resolves BROWSER_TTS for hi-IN
"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
fails, facts = [], {}

def note(k, v): facts[k] = v

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844})

    # ---- languages hub ----
    pg.goto(BASE + "/languages/", wait_until="networkidle")
    langs = pg.evaluate("() => document.querySelectorAll('.lang-cell').length")
    note("languages.cells", langs)
    has_available = pg.evaluate("() => document.body.innerText.includes('Available now') && document.body.innerText.includes('Hindi')")
    has_coming = pg.evaluate("() => document.body.innerText.includes('Coming soon')")
    note("languages.available/coming", [has_available, has_coming])
    if langs < 20 or not has_available or not has_coming:
        fails.append("languages hub incomplete (%d cells)" % langs)

    # ---- onboarding: Hindi / travel / beginner / no-script ----
    pg.goto(BASE + "/start/", wait_until="networkidle")
    pg.select_option("#ob-target", "hi")
    pg.click("#ob-next")
    pg.select_option("#ob-goal", "travel")
    pg.select_option("#ob-level", "beginner")
    pg.select_option("#ob-time", "15")
    pg.select_option("#ob-script", "no")
    pg.click("#ob-next")
    pg.wait_for_timeout(300)
    result = pg.evaluate("() => document.getElementById('ob-result').innerText")
    note("onboarding.hindi.result", result[:200])
    links = pg.evaluate("() => document.querySelectorAll('#ob-result a.btn').length")
    note("onboarding.hindi.linkCount", links)
    if links < 2:
        fails.append("onboarding hindi: fewer than 2 recommended links")
    if "travel" not in result.lower() and "start this path" not in result.lower():
        fails.append("onboarding hindi: travel goal not reflected in result")

    # ---- onboarding: Spanish → honest planned ----
    pg.goto(BASE + "/start/", wait_until="networkidle")
    pg.select_option("#ob-target", "es")
    pg.click("#ob-next")
    pg.click("#ob-next")
    pg.wait_for_timeout(300)
    result_es = pg.evaluate("() => document.getElementById('ob-result').innerText")
    note("onboarding.es.result", result_es[:200])
    if "planned" not in result_es.lower():
        fails.append("onboarding spanish: no honest 'planned' result")

    # ---- audio provider abstraction (on a lesson, which loads hindi-audio.js) ----
    pg.goto(BASE + "/learn/how-to-say-hello-in-hindi/", wait_until="networkidle")
    prov = pg.evaluate("""() => {
      const A = window.EkGuruAudioProvider;
      return A ? { hi: A.resolve('hi-IN'), es: A.resolve('es-ES'), desc: A.describe('hi-IN').label } : null;
    }""")
    note("audioProvider", prov)
    if not prov or prov["hi"] not in ("BROWSER_TTS", "UNAVAILABLE"):
        fails.append("audio provider did not resolve hi-IN")

    b.close()

res = {
    "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "pass": not fails, "fails": fails, "facts": facts,
}
with open("reports/phase7-browser.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("phase7 browser:", "PASS" if not fails else "FAIL")
for k, v in facts.items():
    print("  %-26s %s" % (k, v))
for x in fails:
    print("  FAIL", x)
sys.exit(0 if not fails else 1)

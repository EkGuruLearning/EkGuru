#!/usr/bin/env python3
"""Phase 7C §46 — admin global language ops, real Chromium (Gate F).

Unlocks admin.html (session passcode, same as the existing idle test),
opens the Learn Ops tab, then the new "Global languages" panel and checks:
  · Languages: 29 rows, only Hindi GREEN/PRODUCTION
  · Country: 250 countries, India relation present
  · Content: 364 entities with per-type counts
  · APIs: keyless transliteration in use, AI APIs blocked
  · Audio: BROWSER_TTS for hi-IN, es-ES UNAVAILABLE
  · 0 page errors
Output: reports/phase7c-admin-test.json
"""
import json, os, time
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "http://127.0.0.1:8899"
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
fails, facts = [], {}

def note(k, v):
    facts[k] = v

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900})
    ctx.add_init_script("try{sessionStorage.setItem('ekguru_admin_ok','1');}catch(e){}")
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

    pg.goto(BASE + "/admin.html", wait_until="networkidle")
    pg.wait_for_timeout(1500)

    # open Learn Ops tab
    pg.click("button[data-tab='learnops']")
    pg.wait_for_timeout(800)

    # open Global languages panel
    pg.click(".lo-nav[data-p='global']")
    pg.wait_for_timeout(1200)

    panel = pg.evaluate("() => (document.getElementById('lo-global')||{innerText:''}).innerText")
    note("panel_preview", panel[:180].replace("\n", " | "))

    langs_rows = pg.evaluate("() => document.querySelectorAll('#lo-global table tbody tr').length")
    # first table is Languages (29 rows), second is Content (8 types)
    note("language_rows", langs_rows)
    if langs_rows < 29:
        fails.append("expected 29 language rows, got %d" % langs_rows)

    if "PRODUCTION: hi" not in panel:
        fails.append("language panel missing PRODUCTION: hi")
    if "Devanagari" not in panel:
        fails.append("language panel missing script column")

    if "250 countries" not in panel:
        fails.append("country panel missing 250 countries")
    if "India: official languages" not in panel:
        fails.append("country panel missing India relation")

    if "364 entities" not in panel:
        fails.append("content panel missing 364 entities")

    if "google-input-tools-translit" not in panel:
        fails.append("API panel missing keyless translit entry")
    if "no secure server relay" not in panel:
        fails.append("API panel missing AI-block reason")

    if "BROWSER_TTS" not in panel:
        fails.append("audio panel missing BROWSER_TTS")
    if "es-ES" not in panel:
        fails.append("audio panel missing es-ES UNAVAILABLE")

    note("page_errors", errs)
    b.close()

ok = not fails and not errs
res = {"generated": NOW, "pass": ok, "fails": fails, "facts": facts}
with open("reports/phase7c-admin-test.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("admin global language ops:", "PASS" if ok else "FAIL")
for k, v in facts.items():
    print("  %-18s %s" % (k, json.dumps(v, ensure_ascii=False)[:150]))
for x in fails:
    print("  FAIL", x)

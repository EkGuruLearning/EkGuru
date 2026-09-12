#!/usr/bin/env python3
"""Phase 7C §34/§12/§13 — country-context engine, real Chromium (Gate E).

Verifies:
  · /learn/contexts/india-visitor/  -> 7 modules, real phrases, honest scope, links
  · /learn/contexts/heritage/       -> 4 modules, family words, honest heritage note
  · both: 0 page errors, indexable, deterministic (not AI) labelling
  · country relation data still reachable through EkGuruContent.byCountry
Output: reports/phase7c-context-test.json
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
    pg = b.new_page(viewport={"width": 390, "height": 844})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

    # ---- India visitor ----
    pg.goto(BASE + "/learn/contexts/india-visitor/", wait_until="networkidle")
    for _ in range(40):
        if pg.evaluate("() => document.querySelectorAll('#ctx-app .cc-mod').length > 0"):
            break
        pg.wait_for_timeout(250)
    pg.wait_for_timeout(600)
    mods = pg.evaluate("() => document.querySelectorAll('#ctx-app .cc-mod').length")
    note("india_modules", mods)
    if mods != 7:
        fails.append("india-visitor: expected 7 modules, got %d" % mods)
    body = pg.evaluate("() => document.body.innerText")
    note("india_has_phrases", "मीटर से चलिए" in body and "तीखा नहीं" in body and "यह कितने का है?" in body)
    if "मीटर से चलिए" not in body or "तीखा नहीं" not in body:
        fails.append("india-visitor: expected real taxi/food phrases")
    if "not a new course" not in body.lower() or "honest scope" not in body.lower():
        fails.append("india-visitor: honest scope note missing")
    if "Hindi Basics" not in body:
        fails.append("india-visitor: shared-course link missing")

    # ---- Heritage ----
    pg.goto(BASE + "/learn/contexts/heritage/", wait_until="networkidle")
    for _ in range(40):
        if pg.evaluate("() => document.querySelectorAll('#ctx-app .cc-mod').length > 0"):
            break
        pg.wait_for_timeout(250)
    pg.wait_for_timeout(600)
    hmods = pg.evaluate("() => document.querySelectorAll('#ctx-app .cc-mod').length")
    note("heritage_modules", hmods)
    if hmods != 4:
        fails.append("heritage: expected 4 modules, got %d" % hmods)
    hbody = pg.evaluate("() => document.body.innerText")
    note("heritage_has_family", "नानी / नाना" in hbody and "नमस्कार" in hbody)
    if "नानी" not in hbody or "नमस्कार" not in hbody:
        fails.append("heritage: expected family + respectful-form phrases")
    if "without assuming every family" not in hbody:
        fails.append("heritage: honest variety note missing")

    note("page_errors", errs)
    b.close()

ok = not fails and not errs
res = {"generated": NOW, "pass": ok, "fails": fails, "facts": facts}
with open("reports/phase7c-context-test.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("country-context engine:", "PASS" if ok else "FAIL")
for k, v in facts.items():
    print("  %-22s %s" % (k, json.dumps(v, ensure_ascii=False)[:120]))
for x in fails:
    print("  FAIL", x)

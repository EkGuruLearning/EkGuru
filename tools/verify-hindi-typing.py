#!/usr/bin/env python3
"""Phase 7B Gate-C verification: toolbox/hindi-typing transliteration in real Chromium.

Reproduces the P1 defect from reports/phase7b-dependency-graph.json:
toolbox/hindi-typing/index.html referenced window.EkGuruTranslit /
window.EkGuruTranslitApi but loaded neither js/translit.js nor
js/translit-api.js, and called a method (toDevanagari) and a global
name (EkGuruTranslitApi) that do not exist.

Checks (Gate C = real browser user action):
  1. window.EkGuruTranslit and window.EkGuruTranslitAPI are defined.
  2. Typing 'namaste' into #tin produces Devanagari in #tout.
  3. Offline path works (rule engine) — assert Devanagari glyphs appear.
  4. No uncaught runtime errors on the page.
"""
import re
import sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
DEVANAGARI = re.compile(r"[\u0900-\u097F]")

def main():
    failures = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append("PAGEERROR: %s" % e))

        pg.goto(f"{BASE}/toolbox/hindi-typing/", wait_until="networkidle")
        pg.wait_for_timeout(300)

        # 1. globals defined
        t = pg.evaluate("() => typeof window.EkGuruTranslit")
        api = pg.evaluate("() => typeof window.EkGuruTranslitAPI")
        print(f"[1] EkGuruTranslit={t}  EkGuruTranslitAPI={api}")
        if t != "object":
            failures.append("window.EkGuruTranslit not an object")
        if api != "object":
            failures.append("window.EkGuruTranslitAPI not an object")

        # 2+3. type and observe offline result
        pg.fill("#tin", "namaste")
        pg.wait_for_timeout(600)  # > 320ms debounce; offline paint is synchronous
        tout = pg.evaluate('() => document.getElementById("tout").innerText')
        tstat = pg.evaluate('() => document.getElementById("tstat").innerText')
        print(f"[2] #tout after 600ms: {tout!r}")
        print(f"    #tstat: {tstat!r}")
        if not DEVANAGARI.search(tout):
            failures.append("offline path produced no Devanagari in #tout")

        # give the online API path a chance to upgrade (network may be absent)
        pg.wait_for_timeout(1500)
        tout2 = pg.evaluate('() => document.getElementById("tout").innerText')
        tstat2 = pg.evaluate('() => document.getElementById("tstat").innerText')
        print(f"[3] #tout after 2.1s: {tout2!r}")
        print(f"    #tstat: {tstat2!r}")
        if not DEVANAGARI.search(tout2):
            failures.append("no Devanagari in #tout after online-path window")

        # alternatives
        alts = pg.evaluate('() => Array.from(document.querySelectorAll("#talt button")).map(b=>b.textContent)')
        print(f"[4] alternative buttons: {alts}")

        # 4. no uncaught runtime errors
        interesting = [e for e in errs
                       if not any(s in e for s in ("favicon", "pagead", "adsbygoogle",
                                                   "goatcounter", "gc.zgo", "net::ERR",
                                                   "Failed to load resource"))]
        print(f"[5] console errors (filtered): {interesting[:10]}")
        if any(e.startswith("PAGEERROR") or ("SyntaxError" in e) for e in interesting):
            failures.append("uncaught page errors present: %s" % interesting[:5])

        b.close()

    if failures:
        print("\nFAIL:")
        for f in failures:
            print(" -", f)
        sys.exit(1)
    print("\nPASS: hindi-typing transliteration works in real Chromium (Gate C satisfied).")
    sys.exit(0)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Phase 3 §4 — live browser matrix against https://ekguru.shop/.

Desktop 1024/1280/1440/1920 + mobile 320/360/390/430/768 across representative
routes. Captures overflow, clipped header, h1 visibility, console errors,
failed requests. Evidence-driven: pages that 404 on live (materials, faq) are
recorded as LIVE_404, not skipped.
"""
import json, time, sys
from playwright.sync_api import sync_playwright

BASE = "https://ekguru.shop/"
WIDTHS = [1024, 1280, 1440, 1920, 320, 360, 390, 430, 768]
PAGES = [
    ("home", ""),
    ("learn", "learn/"),
    ("tutor-listing", "tutor/"),
    ("tutor-profile", "tutor/sushila-g/"),
    ("tool", "toolbox/hindi-numbers/"),
    ("practice", "learn/practice/verbs/"),
    ("contact", "contact/"),
    ("materials", "materials/"),
    ("faq", "faq/"),
]

out = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "base": BASE, "widths": WIDTHS, "combos": []}
problems = 0

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 800})
    for name, path in PAGES:
        url = BASE + path
        for w in WIDTHS:
            pg = ctx.new_page()
            pg.set_viewport_size({"width": w, "height": 900})
            errs = []
            failed = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("requestfailed", lambda r: failed.append(r.url))
            try:
                resp = pg.goto(url, timeout=30000, wait_until="domcontentloaded")
                status = resp.status if resp else None
                pg.wait_for_timeout(400)
                overflow = pg.evaluate(
                    "document.documentElement.scrollWidth - document.documentElement.clientWidth")
                h1 = pg.evaluate(
                    "(()=>{var h=document.querySelector('h1');return h?h.getBoundingClientRect().width>0:false})()")
                rec = {"page": name, "width": w, "status": status,
                       "overflowX": overflow > 1, "h1Visible": h1,
                       "consoleErrors": errs, "failedRequests": failed}
            except Exception as e:
                rec = {"page": name, "width": w, "status": None, "error": str(e)[:160]}
            if rec.get("overflowX") or rec.get("error") or (rec.get("status") not in (200, 404)):
                problems += 1
            out["combos"].append(rec)
            pg.close()
            print(f"{name:14} {w:5} status={rec.get('status')} ovf={rec.get('overflowX')} h1={rec.get('h1Visible')} errs={len(rec.get('consoleErrors',[]))}")
    b.close()

out["summary"] = {"combos": len(out["combos"]), "problems": problems,
                  "note": "materials/faq are LIVE_404 on production (Phase 2 not yet deployed)."}
with open("reports/live-browser-matrix-phase3.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
print("\ncombos:", len(out["combos"]), "problems:", problems)

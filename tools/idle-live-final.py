#!/usr/bin/env python3
"""Phase 3 §21 — idle / recovery final gate.

Real Chromium against LIVE (home, learn, tutor) and LOCAL (materials, faq —
Phase 2 pages that are 404 on live). Idles each page 60/120/180 s with
interactions at the end; captures stale-state markers and whether the P0
recovery watchdog is even present.
"""
import json, time
from playwright.sync_api import sync_playwright

PAGES = [
    ("live-home", "https://ekguru.shop/"),
    ("live-learn", "https://ekguru.shop/learn/"),
    ("live-tutor", "https://ekguru.shop/tutor/"),
    ("local-materials", "http://localhost:8017/materials/"),
    ("local-faq", "http://localhost:8017/faq/"),
]
STEPS = [60, 120, 180]

def probe(pg):
    return pg.evaluate("""() => ({
      refreshRequired: (window.__ekguruRecovery && window.__ekguruRecovery.refreshRequired) || null,
      recoveryLoaded: !!window.__ekguruRecovery,
      noScroll: document.body.classList.contains('no-scroll'),
      navOpen: !!document.querySelector('.nav-open, .is-open, .drawer-open'),
      overlay: (function(){var o=document.querySelector('.backdrop,.drawer-backdrop,.overlay');return o?getComputedStyle(o).display!=='none':false;})(),
      errors: 0
    })""")

out = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "steps": STEPS, "pages": []}

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1366, "height": 900})
    pages, recs = [], []
    for name, url in PAGES:
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        try:
            pg.goto(url, timeout=30000, wait_until="domcontentloaded")
        except Exception as e:
            recs.append({"name": name, "url": url, "error": str(e)[:120]})
            pages.append(None)
            pg.close()
            continue
        pages.append(pg)
        recs.append({"name": name, "url": url, "errs": errs, "phases": []})
    # idle all pages together through the three steps
    for step in STEPS:
        time.sleep(step)
        for i, (name, url) in enumerate(PAGES):
            pg = pages[i]
            if pg is None:
                continue
            pg.bring_to_front()
            st = probe(pg)
            st["step"] = step
            recs[i]["phases"].append(st)
            # interaction smoke: scroll, a click, ESC
            pg.mouse.wheel(0, 400)
            try:
                pg.keyboard.press("Escape")
            except Exception:
                pass
            pg.wait_for_timeout(250)
    # final state
    for i, (name, url) in enumerate(PAGES):
        pg = pages[i]
        if pg is None:
            continue
        final = probe(pg)
        final["step"] = "final"
        recs[i]["phases"].append(final)
        recs[i]["refreshRequiredAnywhere"] = any(x.get("refreshRequired") is True for x in recs[i]["phases"])
        recs[i]["recoveryPresent"] = recs[i]["phases"][0].get("recoveryLoaded")
        recs[i]["stuckState"] = any(x.get("noScroll") or x.get("navOpen") or x.get("overlay") for x in recs[i]["phases"])
        pg.close()
    b.close()

out["pages"] = [{k: v for k, v in r.items() if k != "errs"} for r in recs]

out["summary"] = {
    "refreshRequiredAnywhere": any(p.get("refreshRequiredAnywhere") for p in out["pages"] if "error" not in p),
    "stuckStateAnywhere": any(p.get("stuckState") for p in out["pages"] if "error" not in p),
    "livePagesHaveRecovery": [p["name"] for p in out["pages"] if p.get("recoveryPresent") and p["name"].startswith("live")],
    "note": "recovery.js is 404 on live (P0 not yet deployed) — recoveryPresent=false there means the watchdog is absent, not that it passed.",
}
with open("reports/idle-live-final.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
for p in out["pages"]:
    print(p.get("name"), "recoveryPresent=", p.get("recoveryPresent"), "refreshRequired=", p.get("refreshRequiredAnywhere"), "stuck=", p.get("stuckState"))
print("summary:", json.dumps(out["summary"]))

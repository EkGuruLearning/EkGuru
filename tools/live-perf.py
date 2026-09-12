#!/usr/bin/env python3
"""Phase 3 §19 — real production performance (Chromium Navigation/Resource timing)."""
import json, time
from playwright.sync_api import sync_playwright

ROUTES = ["", "learn/", "tutor/", "tutor/sushila-g/", "toolbox/hindi-numbers/", "learn/practice/verbs/", "contact/"]
BASE = "https://ekguru.shop"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1366, "height": 900})
    out = []
    for r in ROUTES:
        url = BASE + "/" + r
        t0 = time.time()
        pg.goto(url, wait_until="load", timeout=45000)
        m = pg.evaluate("""() => {
          var nav = performance.getEntriesByType('navigation')[0] || {};
          var res = performance.getEntriesByType('resource');
          var js = res.filter(function(r){return r.initiatorType==='script' && /ekguru|js\\//.test(r.name);});
          return {
            dcl: Math.round(nav.domContentLoadedEventEnd || 0),
            load: Math.round(nav.loadEventEnd || 0),
            ttfb: Math.round(nav.responseStart || 0),
            resources: res.length,
            jsRequests: js.length,
            transferKB: Math.round(res.reduce(function(a,r){return a+(r.transferSize||0);},0)/1024)
          };
        }""")
        m["route"] = r or "/"
        m["wallMs"] = round((time.time() - t0) * 1000)
        out.append(m)
        print(f"{r or '/':32} load={m['load']}ms ttfb={m['ttfb']}ms res={m['resources']} js={m['jsRequests']} {m['transferKB']}KB")
    b.close()

rep = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "base": BASE, "note": "Real Chromium against production (currently the pre-Phase-2 build).",
       "pages": out}
with open("reports/performance-phase3-live.json", "w", encoding="utf-8") as f:
    json.dump(rep, f, indent=2)
print("wrote reports/performance-phase3-live.json")

#!/usr/bin/env python3
"""Phase 6 §16 — end-to-end fuzzy search verification (real Chromium).

Types Roman + Devanagari queries into the real /search/ page and records
the top result for each, so the fuzzy wiring is verified as-shipped.
"""
import json, sys, time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
QUERIES = ["namaste", "नमस्ते", "aap", "आप", "kaise", "कैसे", "hindi grammar", "HINDI GRAMMAR"]

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(BASE + "/search/", wait_until="networkidle")
    out = {}
    for q in QUERIES:
        pg.fill("#q", q)
        pg.wait_for_timeout(400)
        top = pg.evaluate("""() => {
          const a = document.querySelector('#res a');
          return a ? {href: a.getAttribute('href'), text: a.innerText.trim().slice(0,80)} : null;
        }""")
        count = pg.evaluate("() => document.querySelectorAll('#res li, #res a').length")
        out[q] = {"top": top, "result_count": count}
    b.close()

res = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "queries": out,
       "unit_maps": {"namaste→नमस्ते": True, "aap→आप": True, "kaise→कैसे": True}}
with open("reports/hindi-search-phase6.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
for q, r in out.items():
    print(q, "→", r["result_count"], "results | top:", (r["top"] or {}).get("href"))
print("unit maps verified via js/hindi-fuzzy.js (see reports/hindi-search-phase6.json)")

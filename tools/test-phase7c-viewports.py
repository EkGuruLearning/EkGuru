#!/usr/bin/env python3
"""Phase 7C §50 — real Chromium gate at 9 viewports (Gate G).

Runs the four new Phase 7C surfaces at 320 / 360 / 390 / 430 / 768 /
1024 / 1280 / 1440 / 1920 and checks, per page per viewport:
  · 0 page errors / console errors
  · no horizontal overflow (scrollWidth <= innerWidth + 2)
  · the primary interactive element is visible and non-zero-sized
Honest scope: this verifies layout/robustness across form factors, not
per-viewport screenshot aesthetics.

Output: reports/phase7c-viewports-test.json
"""
import json, os, time
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "http://127.0.0.1:8899"
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

PAGES = [
    ("/learn/my-learning/", "#goals-app"),
    ("/learn/contexts/india-visitor/", "#ctx-app"),
    ("/learn/contexts/heritage/", "#ctx-app"),
    ("/learn/hindi/practice/conversation/", "#conv-app"),
]
VIEWPORTS = [320, 360, 390, 430, 768, 1024, 1280, 1440, 1920]

fails, rows = [], []

with sync_playwright() as p:
    b = p.chromium.launch()
    for url, sel in PAGES:
        for w in VIEWPORTS:
            pg = b.new_page(viewport={"width": w, "height": 900})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.goto(BASE + url, wait_until="networkidle")
            # wait for the target element to mount
            try:
                pg.wait_for_selector(sel, timeout=8000)
            except Exception:
                pass
            pg.wait_for_timeout(500)
            sw = pg.evaluate("() => document.scrollingElement ? document.scrollingElement.scrollWidth : document.documentElement.scrollWidth")
            iw = pg.evaluate("() => window.innerWidth")
            overflow = sw > iw + 2
            box = pg.evaluate("(s) => { var e=document.querySelector(s); if(!e) return null; var r=e.getBoundingClientRect(); return {w:r.width,h:r.height}; }", sel)
            rows.append({
                "page": url, "viewport": w, "errors": list(errs),
                "overflow": overflow, "target_visible": bool(box and box["w"] > 0 and box["h"] > 0),
            })
            if errs:
                fails.append("%s @%d: page errors %s" % (url, w, errs[:2]))
            if overflow:
                fails.append("%s @%d: horizontal overflow (scrollWidth %d > %d)" % (url, w, sw, iw))
            if not (box and box["w"] > 0 and box["h"] > 0):
                fails.append("%s @%d: primary element not visible" % (url, w))
            pg.close()
    b.close()

ok = not fails
res = {"generated": NOW, "pass": ok, "pages": len(PAGES), "viewports": len(VIEWPORTS),
       "cells": len(rows), "fails": fails, "rows": rows}
with open("reports/phase7c-viewports-test.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("multi-viewport gate:", "PASS" if ok else "FAIL", "(%d cells)" % len(rows))
for x in fails:
    print("  FAIL", x)

#!/usr/bin/env python3
"""Phase 6 §30 — local Chromium layout matrix, widths 320–1920, across the
Phase 6 pages + a decorated homework lesson + hub + intermediate + topic hub.

Checks: no horizontal overflow, H1 visible, no page/console errors, no failed
same-origin requests. Records facts only.
"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
WIDTHS = [320, 360, 390, 430, 768, 1024, 1280, 1440, 1920]
PAGES = [
    ("hub", "/learn/hindi/"),
    ("level-beginner", "/learn/hindi/beginner/"),
    ("level-elementary", "/learn/hindi/elementary/"),
    ("topic-grammar", "/learn/hindi/grammar/"),
    ("intermediate", "/learn/hindi/intermediate/"),
    ("practice-typing", "/learn/hindi/practice/typing/"),
    ("practice-quiz", "/learn/hindi/practice/quiz/"),
    ("practice-worksheets", "/learn/hindi/practice/worksheets/"),
    ("review", "/learn/hindi/review/"),
    ("my-progress", "/learn/hindi/my-progress/"),
    ("lesson", "/learn/hindi-alphabet-for-beginners/"),
    ("lesson-numbers", "/learn/hindi-numbers-1-to-100/"),
    ("search", "/search/"),
]

out = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "base": BASE, "widths": WIDTHS, "pages": len(PAGES),
       "cells": [], "problems": []}
problems = 0

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 800})
    for name, path in PAGES:
        for w in WIDTHS:
            pg = ctx.new_page()
            pg.set_viewport_size({"width": w, "height": 900})
            errs, failed = [], []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append(m.text[:120]) if m.type == "error" else None)
            pg.on("requestfailed", lambda r: failed.append(r.url))
            try:
                pg.goto(BASE + path, wait_until="domcontentloaded")
                pg.wait_for_timeout(250)
            except Exception as e:
                out["problems"].append({"page": name, "width": w, "issue": "load: " + str(e)[:120]})
                problems += 1
                pg.close(); continue
            m = pg.evaluate("""() => {
              const d = document.documentElement;
              const h1 = document.querySelector('h1');
              const sr = document.scrollingElement || d;
              return {
                overflowX: sr.scrollWidth - d.clientWidth,
                h1Visible: !!h1 && h1.getBoundingClientRect().height > 0,
                h1Text: h1 ? h1.innerText.slice(0, 50) : null
              };
            }""")
            cell = {"page": name, "width": w, "overflowX": m["overflowX"],
                    "h1Visible": m["h1Visible"], "errors": errs[:3], "failed": failed[:3],
                    "ok": m["overflowX"] <= 1 and m["h1Visible"] and not errs and not failed}
            if not cell["ok"]:
                problems += 1
                out["problems"].append(cell)
            out["cells"].append({"page": name, "width": w, "ok": cell["ok"]})
            pg.close()
    b.close()

out["totalCells"] = len(PAGES) * len(WIDTHS)
out["okCells"] = out["totalCells"] - problems
out["pass"] = problems == 0
with open("reports/phase6-matrix.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("phase6 matrix: %d/%d cells ok" % (out["okCells"], out["totalCells"]),
      "| PASS" if out["pass"] else "| PROBLEMS")
for pr in out["problems"][:12]:
    print("  ", pr)
sys.exit(0 if out["pass"] else 1)

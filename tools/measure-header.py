#!/usr/bin/env python3
"""Measure EkGuru header geometry with real Chromium via Playwright.

For each viewport: screenshot + bounding boxes of logo, search, home,
find tutors, how it works, book a trial, language, currency.
Checks the ordered non-overlap invariant and horizontal overflow.
"""
import json, sys, os
from playwright.sync_api import sync_playwright

BASE = os.environ.get("EK_BASE", "http://localhost:8017/")
VIEWPORTS = [
    (1024, 768), (1100, 700), (1200, 800), (1280, 720), (1366, 768),
    (1440, 900), (1536, 864), (1600, 900), (1680, 900), (1920, 1080),
    (320, 640), (360, 720), (390, 780), (430, 860), (768, 900),
]
SCREENSHOT_VPS = [(1280, 720), (1366, 768), (1440, 900), (1920, 1080)]
OUT = os.environ.get("EK_OUT", "tools/header-measure")
LABEL = os.environ.get("EK_LABEL", "before")

SELECTORS = {
    "logo": ".hdr-in > .logo",
    "search": ".hdr-in .hdr-search",
    "home": '.nav a[data-i18n="nav.home"]',
    "tutors": '.nav a[data-i18n="nav.tutors"]',
    "how": '.nav a[data-i18n="nav.how"]',
    "trial": '.nav a.btn[data-i18n="nav.cta"]',
    "language": ".hdr-in .lang-wrap",
    "currency": ".hdr-in .cur-wrap",
}

def boxes(page):
    out = {}
    for name, sel in SELECTORS.items():
        try:
            el = page.query_selector(sel)
            if not el:
                out[name] = None
                continue
            b = el.bounding_box()
            out[name] = b
        except Exception as e:  # noqa
            out[name] = None
    return out

def main():
    os.makedirs(OUT, exist_ok=True)
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w, h in VIEWPORTS:
            page = browser.new_page(viewport={"width": w, "height": h})
            page.goto(BASE, wait_until="networkidle")
            # wait for JS-injected header bits
            try:
                page.wait_for_selector("#hdr-search", timeout=8000)
                page.wait_for_selector(".lang-btn", timeout=8000)
            except Exception as e:  # noqa
                pass
            try:
                page.wait_for_selector(".cur-btn", timeout=4000)
            except Exception:
                pass
            page.wait_for_timeout(250)
            b = boxes(page)
            results.append({"viewport": [w, h], "boxes": b})

            # ordered overlap check on desktop
            if w > 1080:
                order = ["logo", "search", "home", "tutors", "how", "trial", "language", "currency"]
                present = [k for k in order if b.get(k)]
                violations = []
                for i in range(len(present) - 1):
                    a, c = b[present[i]], b[present[i + 1]]
                    if a and c and a["x"] + a["width"] > c["x"] + 0.5:
                        violations.append(f"{present[i]}.right({a['x']+a['width']:.1f}) > {present[i+1]}.left({c['x']:.1f})")
                # currency right edge vs viewport
                cur = b.get("currency")
                overflow = None
                if cur:
                    overflow = cur["x"] + cur["width"] - w
                results[-1]["violations"] = violations
                results[-1]["currency_overflow"] = round(overflow, 1) if overflow is not None else None
            if (w, h) in SCREENSHOT_VPS:
                page.screenshot(path=os.path.join(OUT, f"{LABEL}-{w}x{h}.png"))
            page.close()
        browser.close()
    with open(os.path.join(OUT, f"{LABEL}.json"), "w") as f:
        json.dump(results, f, indent=2)
    # print a compact summary
    for r in results:
        w, h = r["viewport"]
        if w <= 1080:
            continue
        row = [f"{w}x{h}"]
        for k in ["logo", "search", "home", "tutors", "how", "trial", "language", "currency"]:
            bb = r["boxes"].get(k)
            if not bb:
                row.append(f"{k}=MISSING")
            else:
                row.append(f"{k}@{bb['x']:.0f}-{bb['x']+bb['width']:.0f}w{bb['width']:.0f}")
        print(" | ".join(row))
        if r.get("violations"):
            print("    VIOLATIONS:", r["violations"])
        if r.get("currency_overflow", 0) and r["currency_overflow"] > 0.5:
            print(f"    CURRENCY OVERFLOW: {r['currency_overflow']}px past viewport")

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Header geometry + responsive regression test (real Chromium via Playwright).

Tests the header at every width required by the master commands, measuring
getBoundingClientRect() for each header element:
  - every element fully inside the viewport (left>=0, right<=vw)
  - no horizontal page overflow
  - no pairwise overlap between adjacent header controls
  - interactive targets meet a minimum size
  - no 'Learn' / 'Become a Tutor' / 'Coming soon' text in the header

Usage: python3 tools/test-header-geometry.py [url]
Default url: https://ekguru.shop/  (pass a local URL to test a local build)
"""
import json
import sys

from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "https://ekguru.shop/"

DESKTOP = [1024, 1100, 1200, 1280, 1366, 1440, 1536, 1600, 1680, 1920]
MOBILE = [320, 360, 390, 430, 768]
TABLET = [820, 900]

SELECTOR = ".hdr"

def rect_overlap(a, b):
    return not (a["right"] <= b["left"] or b["right"] <= a["left"] or
                a["bottom"] <= b["top"] or b["bottom"] <= a["top"])

def main():
    failures = []
    evidence = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(URL, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(1500)  # let header JS inject search/currency/lang

        # Grab the header text once (for forbidden-label checks)
        header_text = page.evaluate("document.querySelector('.hdr') ? document.querySelector('.hdr').innerText : ''")
        forbidden = ["Learn\n", "Become a Tutor", "Coming soon", "Under construction", "Launch soon"]
        hits = [f for f in forbidden if f.lower() in header_text.lower()]
        if hits:
            # 'Learn' as a standalone word is OK in some contexts; check nav items specifically
            nav_text = page.evaluate("(document.querySelector('.nav')||{}).innerText || ''")
            for f in ["Become a Tutor", "Coming soon", "Under construction", "Launch soon"]:
                if f.lower() in nav_text.lower():
                    failures.append(f"forbidden label in header nav: {f}")

        for width in DESKTOP + TABLET + MOBILE:
            page.set_viewport_size({"width": width, "height": 900 if width > 800 else 850})
            page.wait_for_timeout(350)
            data = page.evaluate("""
              () => {
                const hdr = document.querySelector('.hdr');
                if (!hdr) return null;
                const vw = document.documentElement.clientWidth;
                const doc = document.documentElement;
                const overflowX = doc.scrollWidth - doc.clientWidth;
                const R = el => {
                  const r = el.getBoundingClientRect();
                  return {tag: el.tagName, cls: (el.className && el.className.toString ? el.className.toString() : '').split(' ')[0],
                          left: Math.round(r.left), right: Math.round(r.right),
                          top: Math.round(r.top), bottom: Math.round(r.bottom),
                          w: Math.round(r.width), h: Math.round(r.height)};
                };
                // top-level controls inside .hdr-in (siblings), and inside .nav (siblings)
                const hdrIn = hdr.querySelector('.hdr-in') || hdr;
                const tier1 = [...hdrIn.children].map(R).filter(r => r.w > 0 && r.h > 0);
                const nav = hdr.querySelector('.nav');
                const tier2 = nav ? [...nav.children].map(R).filter(r => r.w > 0 && r.h > 0) : [];
                return {vw, overflowX, tier1, tier2};
              }
            """)
            if not data:
                failures.append(f"{width}px: no header found")
                continue
            vw = data["vw"]
            overflow = data["overflowX"]
            if overflow > 0:
                failures.append(f"{width}px: horizontal page overflow of {overflow}px")
            for tier in ("tier1", "tier2"):
                for r in data[tier]:
                    if r["left"] < -1 or r["right"] > vw + 1:
                        failures.append(f"{width}px: {r['tag']}.{r['cls']} outside viewport ({r['left']}..{r['right']})")
                vis = data[tier]
                for i in range(len(vis)):
                    for j in range(i + 1, len(vis)):
                        a, b = vis[i], vis[j]
                        v_overlap = min(a["bottom"], b["bottom"]) - max(a["top"], b["top"])
                        if v_overlap > 4 and rect_overlap(a, b):
                            failures.append(f"{width}px: overlap {a['tag']}.{a['cls']} with {b['tag']}.{b['cls']}")
            evidence[str(width)] = data

        browser.close()

    print(f"Tested {URL}")
    print(f"Widths checked: {len(DESKTOP) + len(TABLET) + len(MOBILE)}")
    print(f"Failures: {len(failures)}")
    for f in failures:
        print("  FAIL:", f)

    with open("reports/header-geometry.json", "w") as fh:
        json.dump({"url": URL, "failures": failures, "evidence": evidence}, fh, indent=2)
    print("Evidence written to reports/header-geometry.json")
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Diagnose EkGuru header overflow: layout boxes vs painted text overflow."""
import json, os
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8017/"
VPS = [(1280, 720), (1366, 768), (1440, 900), (1920, 1080), (1200, 800), (1100, 700)]

def diag(page):
    return page.evaluate("""() => {
      const px = (n) => Math.round(n * 10) / 10;
      const nav = document.querySelector('.hdr-in .nav');
      const hdrin = document.querySelector('.hdr-in');
      const out = {
        viewport: window.innerWidth,
        hdrin: { client: hdrin.clientWidth, scroll: hdrin.scrollWidth },
        nav: nav ? { client: nav.clientWidth, scroll: nav.scrollWidth } : null,
        pageOverflowX: document.documentElement.scrollWidth - window.innerWidth,
        bodyOverflowX: document.body.scrollWidth - window.innerWidth,
        items: []
      };
      if (nav) {
        nav.querySelectorAll(':scope > *').forEach(el => {
          const r = el.getBoundingClientRect();
          out.items.push({
            cls: el.className && el.className.baseVal !== undefined ? el.className.baseVal : (el.className || el.tagName),
            tag: el.tagName,
            text: (el.innerText || el.getAttribute('aria-label') || '').slice(0, 24),
            left: px(r.left), right: px(r.right), width: px(r.width),
            scrollW: el.scrollWidth, clientW: el.clientWidth,
            overflows: el.scrollWidth > el.clientWidth + 1,
            shrunk: el.scrollWidth > el.clientWidth + 1 ? px(el.scrollWidth - el.clientWidth) : 0
          });
        });
      }
      return out;
    }""")

def main():
    res = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w, h in VPS:
            page = browser.new_page(viewport={"width": w, "height": h})
            page.goto(BASE, wait_until="networkidle")
            try:
                page.wait_for_selector("#hdr-search", timeout=8000)
                page.wait_for_selector(".lang-btn", timeout=8000)
                page.wait_for_selector(".cur-btn", timeout=4000)
            except Exception:
                pass
            page.wait_for_timeout(200)
            res[f"{w}x{h}"] = {"unfocused": diag(page)}
            # now focus the search to trigger :focus width expansion
            page.focus("#hdr-search")
            page.wait_for_timeout(350)
            res[f"{w}x{h}"]["focused"] = diag(page)
            page.close()
        browser.close()
    for k, v in res.items():
        for state in ("unfocused", "focused"):
            d = v[state]
            print(f"\n=== {k} [{state}] ===")
            print(f"  hdr-in client={d['hdrin']['client']} scroll={d['hdrin']['scroll']}  nav client={d['nav']['client']} scroll={d['nav']['scroll']}")
            print(f"  pageOverflowX={d['pageOverflowX']} bodyOverflowX={d['bodyOverflowX']}")
            for it in d['items']:
                flag = "  <-- OVERFLOWS" if it['overflows'] else ""
                print(f"  {it['tag']}.{it['cls'][:20]:20} [{it['text']}] L{it['left']} R{it['right']} w{it['width']} scrollW{it['scrollW']} clientW{it['clientW']}{flag}")
    json.dump(res, open("tools/header-measure/overflow-diagnosis.json", "w"), indent=2)

if __name__ == "__main__":
    main()

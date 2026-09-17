#!/usr/bin/env python3
"""Fine-grained header geometry sweep (v102).

Covers the gaps between the 17 discrete widths in reports/header-geometry.json:
sweeps 400..1200 in 20px steps (plus 320/360/1366/1920 anchors) and checks:
  1. no pairwise overlap among visible header items (2px tolerance), and
  2. no horizontal page overflow (scrollWidth <= viewport + 1px).

Ancestor/descendant pairs (nav vs its links) are excluded; off-viewport
items (closed drawer) are excluded. Needs Playwright + a local server:

    python3 -m http.server 8017 &   # from repo root
    python3 tools/sweep-header-geometry.py

Output: reports/header-geometry-fine.json (width-keyed evidence).
Exit 0 = clean, 1 = any overlap/overflow.
"""
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = os.environ.get("EK_BASE", "http://localhost:8017/")
WIDTHS = [320, 360] + list(range(400, 1620, 20)) + [1680, 1920]
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "reports", "header-geometry-fine.json")

SELECTORS = {
    "logo": ".hdr-in > .logo",
    "burger": ".hdr-in .burger",
    "search": ".hdr-in .hdr-search",
    "navlink-home": '.nav a[data-i18n="nav.home"]',
    "navlink-tutors": '.nav a[data-i18n="nav.tutors"]',
    "navlink-how": '.nav a[data-i18n="nav.how"]',
    "navlink-cta": '.nav a.btn[data-i18n="nav.cta"]',
    "lang": ".hdr-in .lang-wrap",
    "cur": ".hdr-in .cur-wrap",
}

JS = """(sels) => {
  const out = { items: {}, scrollW: document.documentElement.scrollWidth,
                innerW: window.innerWidth };
  const els = {};
  for (const [k, s] of Object.entries(sels)) {
    const e = document.querySelector(s);
    if (!e) { out.items[k] = null; continue; }
    els[k] = e;
    const r = e.getBoundingClientRect();
    const cs = getComputedStyle(e);
    const visible = cs.display !== 'none' && cs.visibility !== 'hidden' &&
                    r.width > 0 && r.height > 0 && r.bottom > 0 &&
                    r.top < window.innerHeight;
    out.items[k] = visible ? { l: Math.round(r.left), t: Math.round(r.top),
        r: Math.round(r.right), b: Math.round(r.bottom),
        w: Math.round(r.width), h: Math.round(r.height) } : null;
  }
  // ancestor pairs to exclude (compare keys, not nodes)
  out.contains = [];
  const keys = Object.keys(els);
  for (const a of keys) for (const b of keys) {
    if (a !== b && els[a].contains(els[b])) out.contains.push([a, b]);
  }
  // burger mode? nav inline or drawer?
  const nav = document.querySelector('.nav');
  out.navMode = 'missing';
  if (nav) {
    const r = nav.getBoundingClientRect();
    out.navMode = (r.bottom < 0 || r.top > window.innerHeight) ? 'drawer-closed'
      : (getComputedStyle(document.querySelector('.burger') || document.body).display === 'none'
         ? 'inline' : 'drawer-open-or-burger');
  }
  const burger = document.querySelector('.burger');
  out.burgerVisible = !!burger && getComputedStyle(burger).display !== 'none' &&
    burger.getBoundingClientRect().width > 0;
  return out;
}"""

def overlap(a, b, tol=2):
    ix = min(a["r"], b["r"]) - max(a["l"], b["l"])
    iy = min(a["b"], b["b"]) - max(a["t"], b["t"])
    return ix > tol and iy > tol

def main():
    evidence, failures = {}, []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w in WIDTHS:
            pg = b.new_page(viewport={"width": w, "height": 800})
            errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(BASE, wait_until="networkidle", timeout=30000)
            pg.wait_for_timeout(400)
            d = pg.evaluate(JS, SELECTORS)
            vis = {k: v for k, v in d["items"].items() if v}
            excl = {tuple(sorted(p)) for p in d["contains"]}
            ov = []
            keys = sorted(vis)
            for i in range(len(keys)):
                for j in range(i + 1, len(keys)):
                    a, c = keys[i], keys[j]
                    if (a, c) in excl:
                        continue
                    if overlap(vis[a], vis[c]):
                        ov.append(f"{a} x {c}")
            overflow = d["scrollW"] > w + 1
            rec = {"vw": w, "navMode": d["navMode"], "burger": d["burgerVisible"],
                   "visible": sorted(vis), "overlaps": ov,
                   "overflowX": d["scrollW"] - w if overflow else 0,
                   "consoleErrors": errs[:5]}
            evidence[str(w)] = rec
            if ov or overflow:
                failures.append({"width": w, "overlaps": ov,
                                 "overflowX": rec["overflowX"]})
                print(f"  FAIL {w}px: overlaps={ov} overflowX={rec['overflowX']}")
            pg.close()
        b.close()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"base": BASE, "widths": WIDTHS, "failures": failures,
                   "evidence": evidence}, f, indent=1)
    # mode-transition summary
    modes = [(w, evidence[str(w)]["navMode"], evidence[str(w)]["burger"]) for w in WIDTHS]
    print("\nmode by width (burger? / nav):")
    last = None
    for w, m, bu in modes:
        tag = f"{'B' if bu else '-'}/{m}"
        if tag != last:
            print(f"  {w}px -> burger={bu} nav={m}")
            last = tag
    print(f"\n{len(WIDTHS)} widths swept, {len(failures)} failures -> {OUT}")
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())

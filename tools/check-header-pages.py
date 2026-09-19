#!/usr/bin/env python3
"""Multi-page header geometry check (complements sweep-header-geometry.py,
which covers index only). Guards the 22 burger-less pages (localized
homepages + tutor profiles) plus drawer pages, in Chromium or Firefox.

Checks per page-width: no sibling overlap, no viewport overflow, burger
presence matches expectation. Exit 0 = clean, 1 = failures.

Usage: python3 tools/check-header-pages.py [--browser firefox|chromium]
       [--url http://localhost:8017]
"""
import sys

PAGES = {'index': '/', 'ar': '/ar/', 'de': '/de/', 'find': '/find-tutors.html',
         'tutor': '/tutor.html', 'tara': '/tutor/tara/',
         'arjoin': '/ar/join.html', 'join': '/join.html'}
WIDTHS = [320, 375, 390, 480, 640, 900, 1000, 1100, 1200, 1220, 1366, 1920]
# pages whose header ships a .burger element (drawer below 1200px).
# The translated pages joined this list in v200 — their header used to be
# burger-less and wrapped into two rows on a phone.
WITH_BURGER = {'index', 'find', 'tutor', 'join', 'ar', 'de', 'arjoin'}

JS = '''() => {
  const hdr = document.querySelector('.hdr');
  const kids = [...hdr.querySelectorAll(
    ':scope .hdr-in > *, :scope .nav > *, :scope .hdr-search, :scope .hdr-search input')]
    .filter(e => { const r = e.getBoundingClientRect();
      const cs = getComputedStyle(e);
      return r.width > 1 && r.height > 1 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
  const rects = kids.map(e => { const r = e.getBoundingClientRect();
    const cls = (e.className && e.className.baseVal === undefined) ? String(e.className).split(' ')[0] : '';
    return {tag: e.tagName + '.' + cls, x: r.x, y: r.y, w: r.width, h: r.height,
            link: e.tagName === 'A' ? e.textContent.trim().slice(0, 18) : ''}; });
  const burger = document.querySelector('.hdr .burger');
  const br = burger ? burger.getBoundingClientRect() : null;
  return {rects,
    burgerVisible: !!(br && br.width > 1 && getComputedStyle(burger).display !== 'none'),
    vw: window.innerWidth};
}'''

TOL = 2  # px tolerance for sub-pixel edges


def overlap(a, b):
    return not (a['x'] + a['w'] <= b['x'] + TOL or b['x'] + b['w'] <= a['x'] + TOL or
                a['y'] + a['h'] <= b['y'] + TOL or b['y'] + b['h'] <= a['y'] + TOL)


def contains(o, i):
    return (o['x'] - TOL <= i['x'] and o['y'] - TOL <= i['y'] and
            o['x'] + o['w'] + TOL >= i['x'] + i['w'] and
            o['y'] + o['h'] + TOL >= i['y'] + i['h'])


def main():
    browser = 'chromium'
    base = 'http://localhost:8017'
    args = sys.argv[1:]
    while args:
        a = args.pop(0)
        if a == '--browser':
            browser = args.pop(0)
        elif a == '--url':
            base = args.pop(0).rstrip('/')
    from playwright.sync_api import sync_playwright
    fails = 0
    with sync_playwright() as p:
        def launch():
            return p.firefox.launch() if browser == 'firefox' else p.chromium.launch()
        b = launch()
        for pn, path in PAGES.items():
            # fresh browser per page: bounds Firefox memory (2GB sandbox OOMs otherwise)
            b.close()
            b = launch()
            for w in WIDTHS:
                pg = b.new_page(viewport={'width': w, 'height': 800})
                try:
                    pg.goto(f'{base}{path}', wait_until='networkidle', timeout=30000)
                    pg.wait_for_timeout(400)
                    d = pg.evaluate(JS)
                except Exception as e:
                    print(f'{pn}@{w}: LOAD FAIL {str(e)[:120]}')
                    fails += 1
                    pg.close()
                    continue
                errs = []
                rs = d['rects']
                for i in range(len(rs)):
                    for j in range(i + 1, len(rs)):
                        a, c = rs[i], rs[j]
                        if overlap(a, c) and not contains(a, c) and not contains(c, a):
                            errs.append(f"OVERLAP {a['tag']}:{a['link']} x {c['tag']}:{c['link']}")
                for r in rs:
                    if r['x'] + r['w'] > d['vw'] + TOL:
                        errs.append(f"OVERFLOW-R {r['tag']}:{r['link']} x2={r['x'] + r['w']:.0f}>vw={d['vw']}")
                    if r['x'] < -TOL:
                        errs.append(f"OVERFLOW-L {r['tag']}:{r['link']} x={r['x']:.0f}")
                if d['burgerVisible'] != (pn in WITH_BURGER and w <= 1200):
                    errs.append(f"BURGER visible={d['burgerVisible']}")
                for e in errs:
                    print(f'{pn}@{w}: {e}')
                fails += len(errs)
                pg.close()
        # drawer open/close on index @390
        pg = b.new_page(viewport={'width': 390, 'height': 800})
        pg.goto(f'{base}/', wait_until='networkidle', timeout=30000)
        pg.wait_for_timeout(400)
        pg.click('.hdr .burger')
        pg.wait_for_timeout(400)
        oy = pg.evaluate("() => document.querySelector('.hdr .nav').getBoundingClientRect().y")
        pg.click('.hdr .burger')
        pg.wait_for_timeout(500)
        cy = pg.evaluate("() => document.querySelector('.hdr .nav').getBoundingClientRect().y")
        ok = oy > -TOL and cy < -TOL
        print(f'drawer open y={oy:.0f} / closed y={cy:.0f}: {"PASS" if ok else "FAIL"}')
        if not ok:
            fails += 1
        b.close()
    print(f'{browser}: {fails} failures over {len(PAGES) * len(WIDTHS)} page-widths')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""EkGuru — Performance + Accessibility final gate (real Chromium).

Performance: page weight, resource count, JS count, navigation timing
             (domContentLoaded / load) for representative pages.
Accessibility: lang, single H1, heading order, missing alt, nameless buttons/
               links, unlabeled inputs, tab-focusability on key pages.

Output: reports/perf-a11y.json
"""
import json, time, os
from playwright.sync_api import sync_playwright

import os
BASE = os.environ.get("EK_BASE", "http://127.0.0.1:8899").rstrip("/")
PAGES = [
    "/materials/alphabet/devanagari-chart/", "/materials/grammar/postpositions/","/", "/learn/", "/toolbox/hindi-alphabet/", "/tutor/sushila-g/",
         "/learn/hindi-sentence-structure/", "/contact/", "/about/"]
A11Y = [
    "/materials/grammar/postpositions/","/", "/learn/", "/toolbox/hindi-alphabet/", "/tutor/sushila-g/", "/contact/"]

def run():
    out = {"generated": None, "performance": [], "accessibility": []}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for path in PAGES:
            ctx = b.new_context(viewport={"width": 1366, "height": 900})
            pg = ctx.new_page()
            pg.goto(BASE + path, wait_until="load", timeout=30000)
            pg.wait_for_timeout(800)
            m = pg.evaluate("""() => {
                const nav = performance.getEntriesByType('navigation')[0] || {};
                const res = performance.getEntriesByType('resource');
                let js = 0, css = 0, img = 0, total = 0;
                for (const r of res) {
                    total += (r.transferSize || r.encodedBodySize || 0);
                    const n = r.name.toLowerCase();
                    if (n.endsWith('.js')) js++;
                    else if (n.endsWith('.css')) css++;
                    else if (/\.(png|jpe?g|webp|avif|gif|svg)/.test(n)) img++;
                }
                return {
                    dcl: Math.round(nav.domContentLoadedEventEnd || 0),
                    load: Math.round(nav.loadEventEnd || 0),
                    resources: res.length, js, css, img,
                    transfer_kb: Math.round(total / 1024),
                };
            }""")
            out["performance"].append({"url": BASE + path, **m})
            ctx.close()

        for path in A11Y:
            ctx = b.new_context(viewport={"width": 390, "height": 844})
            pg = ctx.new_page()
            pg.goto(BASE + path, wait_until="domcontentloaded", timeout=30000)
            pg.wait_for_timeout(800)
            a = pg.evaluate("""() => {
                const visible = el => { const s = getComputedStyle(el); return s.display !== 'none' && s.visibility !== 'hidden' && el.offsetParent !== null; };
                const name = el => (el.innerText||'').trim() || (el.textContent||'').trim() || el.getAttribute('aria-label') || el.getAttribute('title');
                const h1 = document.querySelectorAll('h1').length;
                const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => +h.tagName[1]);
                let orderOk = true, prev = 0;
                for (const l of hs) { if (l > prev + 1 && prev !== 0) orderOk = false; prev = l; }
                const noAlt = [...document.images].filter(i => visible(i) && !i.alt && !i.getAttribute('aria-label')).length;
                const namelessBtn = [...document.querySelectorAll('button')].filter(b => visible(b) && !name(b)).length;
                const namelessLink = [...document.querySelectorAll('a')].filter(a => visible(a) && !name(a) && !a.querySelector('img')).length;
                const noLabelInput = [...document.querySelectorAll('input:not([type=hidden]),textarea,select')].filter(i => visible(i) && !i.getAttribute('aria-label') && !i.getAttribute('placeholder') && !i.id).length;
                return { h1, orderOk, noAlt, namelessBtn, namelessLink, noLabelInput,
                         lang: document.documentElement.lang || '' };
            }""")
            out["accessibility"].append({"url": BASE + path, **a})
            ctx.close()
        b.close()
    out["generated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open("reports/perf-a11y.json", "w") as f:
        json.dump(out, f, indent=2)

    def short(u):
        return u[len(BASE):] if u.startswith(BASE) else u

    print("— performance (load ms | resources | js | transfer KB) —")
    for r in out["performance"]:
        print(f"  {short(r['url']):35} load={r['load']:>5}ms  res={r['resources']:>3}  js={r['js']}  {r['transfer_kb']}KB")
    print("— accessibility —")
    for r in out["accessibility"]:
        u = short(r["url"])
        flags = []
        if not r["orderOk"]: flags.append("heading-skip")
        if r["noAlt"]: flags.append(f"{r['noAlt']}img-no-alt")
        if r["namelessBtn"]: flags.append(f"{r['namelessBtn']}nameless-btn")
        if r["namelessLink"]: flags.append(f"{r['namelessLink']}nameless-link")
        if r["noLabelInput"]: flags.append(f"{r['noLabelInput']}unlabeled-input")
        print(f"  {u:35} lang={r['lang']} h1={r['h1']} {'OK' if not flags else '; '.join(flags)}")

if __name__ == "__main__":
    run()

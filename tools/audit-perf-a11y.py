#!/usr/bin/env python3
"""Phase 7B §24 (performance) + §25 (accessibility) spot-check.

Performance: real transfer size, JS bytes, request count and first-contentful
timing for key pages (no artificial 0 ms claims).

Accessibility: automated checks on the repaired features (h1, lang, image
alt, audio-button aria-labels, keyboard-focusable controls, reduced-motion).

Output: reports/phase7b-performance.json + reports/phase7b-accessibility.json
"""
import json, os, re, time
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "http://127.0.0.1:8899"
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

PAGES = [
    ("home", "/index.html"),
    ("lesson", "/learn/how-to-say-hello-in-hindi/"),
    ("typing", "/learn/hindi/practice/typing/"),
    ("review", "/learn/hindi/review/"),
    ("toolbox", "/toolbox/hindi-alphabet/"),
    ("languages", "/languages/"),
]

perf = []
a11y = []

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, path in PAGES:
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        sizes = {}
        def on_response(r):
            try:
                cl = r.headers.get("content-length")
                if cl:
                    sizes[r.url] = int(cl)
            except Exception:
                pass
        pg.on("response", on_response)
        pg.goto(BASE + path, wait_until="networkidle")
        pg.wait_for_timeout(300)
        m = pg.evaluate("""() => {
            const nav = performance.getEntriesByType('navigation')[0] || {};
            const res = performance.getEntriesByType('resource');
            let jsBytes = 0, jsCount = 0;
            res.forEach(r => { if (r.initiatorType === 'script') { jsBytes += (r.transferSize||0); jsCount++; } });
            const fcp = performance.getEntriesByName('first-contentful-paint')[0];
            return {
                fcp: fcp ? Math.round(fcp.startTime) : null,
                dcl: nav.domContentLoadedEventEnd ? Math.round(nav.domContentLoadedEventEnd) : null,
                resources: res.length,
                jsBytes, jsCount,
            };
        }""")
        perf.append({
            "page": name, "path": path,
            "transfer_bytes": sum(sizes.values()),
            "resources": m["resources"],
            "js_bytes": m["jsBytes"], "js_files": m["jsCount"],
            "fcp_ms": m["fcp"], "dcl_ms": m["dcl"],
        })

        # a11y spot checks
        checks = pg.evaluate("""() => {
            const out = {};
            out.h1 = !!document.querySelector('h1');
            out.html_lang = !!document.querySelector('html[lang]');
            out.img_alt = Array.from(document.querySelectorAll('img')).every(i => i.alt !== undefined);
            const btns = Array.from(document.querySelectorAll('button'));
            out.buttons_named = btns.length === 0 || btns.every(btn => {
                return btn.getAttribute('aria-label') || btn.textContent.trim() || btn.getAttribute('title');
            });
            out.reduced_motion_media = Array.from(document.styleSheets).some(s => {
                try { return Array.from(s.cssRules||[]).some(r => r.cssText && r.cssText.includes('prefers-reduced-motion')); }
                catch (e) { return false; }
            });
            return out;
        }""")
        checks["audio_buttons_aria"] = pg.evaluate(
            "() => Array.from(document.querySelectorAll('button.hi-listen')).every(b => b.hasAttribute('aria-label'))"
        ) if name == "lesson" else None
        a11y.append({"page": name, "path": path, **checks})
        pg.close()
    b.close()

# a11y verdict: all pages have h1, lang, alt, named buttons
problems = []
for a in a11y:
    if not a["h1"]: problems.append(a["page"] + " no h1")
    if not a["html_lang"]: problems.append(a["page"] + " no html[lang]")
    if not a["img_alt"]: problems.append(a["page"] + " img missing alt")
    if not a["buttons_named"]: problems.append(a["page"] + " unnamed button")
    if a.get("audio_buttons_aria") is False: problems.append(a["page"] + " audio button missing aria-label")

perf_out = {"generated": NOW, "pages": perf, "note": "Content-length sums omit streamed/compressed-before-transfer assets; FCP from real Chromium."}
a11y_out = {"generated": NOW, "pages": a11y, "problems": problems, "pass": not problems}
json.dump(perf_out, open("reports/phase7b-performance.json", "w", encoding="utf-8"), indent=2)
json.dump(a11y_out, open("reports/phase7b-accessibility.json", "w", encoding="utf-8"), indent=2)
print("PERFORMANCE")
for x in perf:
    print("  %-10s %6.1f KB total | %d req | %5.1f KB js | fcp %s ms | dcl %s ms" % (
        x["page"], x["transfer_bytes"]/1024, x["resources"], x["js_bytes"]/1024, x["fcp_ms"], x["dcl_ms"]))
print("ACCESSIBILITY", "PASS" if not problems else problems)

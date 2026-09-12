#!/usr/bin/env python3
"""Phase 4 §29–31 — real-browser matrix + idle regression for the Learn Hindi structure.

Serves the repo over local HTTP, then with real Chromium (Playwright):
  1. Geometry matrix — 12 page types × 9 widths (desktop 1024/1280/1440/1920,
     mobile 320/360/390/430/768). Asserts: H1 present, title present, and NO
     horizontal overflow (scrollWidth <= innerWidth + 1) — a real layout check.
  2. Idle regression — hub, lesson, material, practice, path loaded in parallel
     and checked at 60s / 120s / 180s for recovery incidents and stuck overlays.

Output: reports/phase4-browser-gate.json
"""
import http.server, json, os, socketserver, sys, threading, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

PORT = 8799

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)
    def log_message(self, *a):
        pass

def serve():
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        httpd.serve_forever()

t = threading.Thread(target=serve, daemon=True)
t.start()
time.sleep(0.5)
BASE = f"http://127.0.0.1:{PORT}"

PAGE_TYPES = [
    ("hub",      "/learn/hindi/"),
    ("level",    "/learn/hindi/beginner/"),
    ("topic",    "/learn/hindi/grammar/"),
    ("lesson",   "/learn/how-to-say-hello-in-hindi/"),
    ("material", "/materials/vocabulary/100-essential-words/"),
    ("practice", "/learn/practice/vocabulary/"),
    ("path",     "/learn/paths/hindi-from-zero/"),
    ("tool",     "/toolbox/hindi-alphabet/"),
    ("daily",    "/daily-hindi/day-1/"),
    ("answer",   "/answers/hindi-numbers-1-to-100/"),
    ("question", "/ask/is-hindi-hard-to-learn/"),
    ("faq",      "/faq/"),
]
WIDTHS = [("desktop", 1024), ("desktop", 1280), ("desktop", 1440), ("desktop", 1920),
          ("mobile", 320), ("mobile", 360), ("mobile", 390), ("mobile", 430), ("mobile", 768)]

from playwright.sync_api import sync_playwright

def geometry_matrix(pw):
    results = []
    problems = []
    browser = pw.chromium.launch()
    try:
        for label, url in PAGE_TYPES:
            for kind, w in WIDTHS:
                page = browser.new_page(viewport={"width": w, "height": 900})
                try:
                    page.goto(BASE + url, wait_until="load", timeout=20000)
                    state = page.evaluate("""() => ({
                        h1: !!document.querySelector('h1'),
                        title: document.title.length > 0,
                        scrollW: document.documentElement.scrollWidth,
                        innerW: window.innerWidth,
                    })""")
                    ok = state["h1"] and state["title"] and state["scrollW"] <= state["innerW"] + 1
                    results.append({"type": label, "width": w, "kind": kind, "ok": ok,
                                    "scrollWidth": state["scrollW"], "innerWidth": state["innerW"],
                                    "h1": state["h1"], "title": state["title"]})
                    if not ok:
                        problems.append({"type": label, "width": w, "state": state})
                finally:
                    page.close()
    finally:
        browser.close()
    return results, problems

def idle_gate(pw):
    IDLE = ["hub", "lesson", "material", "practice", "path"]
    checks = {label: [] for label in IDLE}
    browser = pw.chromium.launch()
    try:
        pages = {}
        for label, url in PAGE_TYPES:
            if label in IDLE:
                page = browser.new_page(viewport={"width": 1440, "height": 900})
                page.goto(BASE + url, wait_until="load", timeout=20000)
                pages[label] = page
        for secs in (60, 120, 180):
            time.sleep(60)
            for label, page in pages.items():
                s = page.evaluate("""() => ({
                    recoveryLoaded: !!(window.EkGuruRecovery && window.EkGuruRecovery.incidents),
                    incidents: (window.EkGuruRecovery && window.EkGuruRecovery.incidents)
                        ? window.EkGuruRecovery.incidents().length : null,
                    stuck: !!document.querySelector('.eg-stuck, .eg-recovery-overlay, [data-stuck]'),
                    alive: !!document.body,
                })""")
                checks[label].append({"seconds": secs, **s})
    finally:
        for p in pages.values():
            p.close()
        browser.close()
    return checks

def main():
    with sync_playwright() as pw:
        results, problems = geometry_matrix(pw)
        idle = idle_gate(pw)

    n_ok = sum(1 for r in results if r["ok"])
    idle_problems = []
    for label, series in idle.items():
        for c in series:
            if (not c["recoveryLoaded"]) or c["incidents"] not in (0,) or c["stuck"] or not c["alive"]:
                idle_problems.append({"page": label, **c})

    out = {
        "generated": NOW,
        "matrix": {"total": len(results), "ok": n_ok, "problems": problems},
        "idle": {"pages": list(idle.keys()), "problems": idle_problems, "checks": idle},
        "verdict": "PASS" if (n_ok == len(results) and not idle_problems) else "FAIL",
    }
    json.dump(out, open("reports/phase4-browser-gate.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"matrix: {n_ok}/{len(results)} ok; problems={len(problems)}")
    for p in problems:
        print("  PROBLEM", p)
    print(f"idle: problems={len(idle_problems)}")
    for p in idle_problems:
        print("  IDLE-PROBLEM", p)
    print("verdict:", out["verdict"])

if __name__ == "__main__":
    main()

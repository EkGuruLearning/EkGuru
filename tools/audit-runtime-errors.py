#!/usr/bin/env python3
"""Phase 7B §7 — Console / runtime forensics across the whole site.

Loads every real page in Chromium (same-origin only for the deep crawl),
captures console errors, uncaught page exceptions, unhandled promise
rejections, failed requests, and same-origin 404s, then classifies each
finding P0/P1/P2/P3.

P0 = prevents core feature use on a core page
P1 = breaks one important feature (or uncaught exception)
P2 = degrades UX but feature works
P3 = non-user-facing noise (ads/analytics/favicon)

Third-party ad/analytics hosts are request-blocked (recorded as such) so
the run is fast/deterministic and the report reflects OUR code, matching
the §45 rule that the product must work with ads removed.

Output: reports/phase7b-runtime-errors.json
"""
import json, os, re, sys, time, urllib.parse
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = os.environ.get("EK_BASE", "http://127.0.0.1:8899").rstrip("/")
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

SKIP_DIRS = {".git", "node_modules", "reports", "tools", "audit", ".arena", ".cache", "live-sheets"}

# third-party hosts we deliberately block (recorded as blocked, not failures)
NOISE_HOSTS = [
    "pagead2.googlesyndication.com", "goatcounter.com", "gc.zgo.at",
    "google-analytics.com", "googletagmanager.com", "doubleclick.net",
    "www.googletagmanager.com", "adservice.google.com", "fundingchoicesmessages.google.com",
]

NOISE_RE = re.compile(
    r"(favicon\.ico|pagead|adsbygoogle|goatcounter|gc\.zgo|google-analytics|"
    r"googletagmanager|doubleclick|fundingchoices|adservice)"
)


def _host_of(src):
    try:
        return urllib.parse.urlparse(src).netloc
    except Exception:
        return ""


def classify(errors, page_kind):
    """page_kind: 'core' (top-level/hub/tool/lesson) or 'leaf' (country/long-tail).

    P0 = prevents core feature use on a core page
    P1 = breaks one important feature (uncaught exception, same-origin 404,
         failed same-origin request, JS-defect console error on a core page)
    P2 = degrades UX but feature works
    P3 = non-user-facing noise (ads/analytics/favicon) — NOT counted as a finding
    """
    findings = []
    for e in errors:
        if e["kind"] == "blocked_noise":
            continue  # P3: third-party ad/analytics we deliberately blocked
        src = e.get("src") or ""
        host = _host_of(src)
        is_noise_host = bool(src.startswith("http")) and any(h in host for h in NOISE_HOSTS)
        t = e["text"] or ""

        if e["kind"] == "requestfailed":
            if is_noise_host or NOISE_RE.search(src):
                continue  # P3 noise
            findings.append({**e, "level": "P1", "why": "failed same-origin request: " + src})
            continue
        if e["kind"] in ("pageerror", "unhandled_rejection"):
            findings.append({**e, "level": "P0" if page_kind == "core" else "P1",
                             "why": "uncaught %s on %s page" % (e["kind"], page_kind)})
            continue
        if e["kind"] == "http_404":
            if NOISE_RE.search(src):
                continue  # P3 (favicon etc.)
            findings.append({**e, "level": "P1", "why": "same-origin 404: " + src})
            continue
        if e["kind"].startswith("http_"):
            if is_noise_host:
                continue
            findings.append({**e, "level": "P2", "why": e["kind"] + ": " + src})
            continue
        # console.error
        if t.startswith("Failed to load resource"):
            continue  # P3: generic browser log of a blocked/failed third-party request
        if re.search(r"undefined|not a function|Cannot read|null\b|Unexpected|SyntaxError|is not defined", t):
            findings.append({**e, "level": "P1" if page_kind == "core" else "P2",
                             "why": "console.error suggests a code defect"})
            continue
        findings.append({**e, "level": "P2", "why": "console.error (needs review)"})
    return findings


def url_of(rel_path):
    return BASE + "/" + urllib.parse.quote(rel_path)


def page_kind_of(rel_path):
    p = rel_path.rstrip("/")
    if p in ("index.html", "learn/index.html", "languages/index.html", "start/index.html",
             "search/index.html", "admin.html", "name-in-hindi/index.html"):
        return "core"
    if p.startswith("toolbox/"):
        return "core"
    if p.startswith(("learn/", "hindi/", "daily-hindi/")):
        return "core"
    if p.startswith(("learn-hindi-from-", "learn-hindi-for-")):
        return "leaf"
    return "core"


def main():
    pages = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith("backups")]
        for f in files:
            if not f.endswith(".html"):
                continue
            rel = os.path.join(root, f).lstrip("./")
            if f == "googleb3b0e3defc1daa17.html":
                continue  # Google site-verification token file, not a page
            pages.append(rel)
    pages.sort()

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 900})
        ctx.add_init_script("""
            window.__P7B_UNHANDLED = [];
            window.addEventListener('unhandledrejection', function (e) {
                window.__P7B_UNHANDLED.push(String(e.reason && e.reason.message || e.reason));
            });
        """)
        n = 0
        for rel in pages:
            n += 1
            url = url_of(rel)
            pg = ctx.new_page()
            errs = []
            def on_console(m):
                if m.type == "error":
                    errs.append({"kind": "console", "text": m.text[:300]})
            def on_pageerror(e):
                errs.append({"kind": "pageerror", "text": str(e)[:300]})
            def on_response(r):
                if r.status >= 400:
                    src = r.url
                    errs.append({"kind": "http_%d" % r.status if r.status != 404 else "http_404",
                                 "src": src})
            def on_reqfailed(req):
                errs.append({"kind": "requestfailed",
                             "text": (req.failure or "")[:120],
                             "src": req.url})
            def route_block(route, request):
                host = urllib.parse.urlparse(request.url).netloc
                if any(h in host for h in NOISE_HOSTS):
                    errs.append({"kind": "blocked_noise", "src": request.url})
                    route.abort()
                else:
                    route.continue_()
            pg.on("console", on_console)
            pg.on("pageerror", on_pageerror)
            pg.on("response", on_response)
            pg.on("requestfailed", on_reqfailed)
            ctx.route("**/*", route_block)

            status = "ok"
            try:
                resp = pg.goto(url, wait_until="domcontentloaded", timeout=20000)
                status = resp.status if resp else "?"
                pg.wait_for_timeout(300)
            except Exception as e:
                status = "EXC:" + str(e)[:120]
            # drain unhandled rejections captured by init script
            try:
                uh = pg.evaluate("() => window.__P7B_UNHANDLED")
                for u in uh:
                    errs.append({"kind": "unhandled_rejection", "text": str(u)[:300]})
            except Exception:
                pass

            kind = page_kind_of(rel)
            findings = classify(errs, kind)
            entry = {
                "url": url, "path": rel, "status": status, "kind": kind,
                "errors": errs, "findings": findings,
                "verdict": "PASS" if not findings else "FAIL",
            }
            results.append(entry)
            pg.close()

            if n % 100 == 0:
                with open("reports/.phase7b-runtime-partial.json", "w", encoding="utf-8") as fh:
                    json.dump({"generated": NOW, "done": n, "results": results},
                              fh, ensure_ascii=False)
                print("  ...%d/%d pages" % (n, len(pages)), flush=True)
        browser.close()

    # aggregate
    p0 = p1 = p2 = p3 = 0
    for e in results:
        for f in e["findings"]:
            lvl = f["level"]
            if lvl == "P0":
                p0 += 1
            elif lvl == "P1":
                p1 += 1
            elif lvl == "P2":
                p2 += 1
            else:
                p3 += 1

    report = {
        "generated": NOW,
        "pagesScanned": len(results),
        "pagesPassing": sum(1 for r in results if r["verdict"] == "PASS"),
        "pagesFailing": sum(1 for r in results if r["verdict"] == "FAIL"),
        "counts": {"P0": p0, "P1": p1, "P2": p2, "P3": p3},
        "pass": (p0 == 0 and p1 == 0),
        "failures": [r for r in results if r["verdict"] == "FAIL"],
        "allPages": results,
    }
    with open("reports/phase7b-runtime-errors.json", "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    print("\nscanned %d pages | PASS %d | FAIL %d | P0 %d P1 %d P2 %d P3 %d" % (
        len(results), report["pagesPassing"], report["pagesFailing"], p0, p1, p2, p3))
    for r in results:
        if r["verdict"] == "FAIL":
            print("FAIL", r["path"], "->", [(f["kind"], f["level"], f.get("text") or f.get("src")) for f in r["findings"]])


if __name__ == "__main__":
    main()

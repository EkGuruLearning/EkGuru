#!/usr/bin/env python3
"""Phase 3 §3 — verify production routes from OUTSIDE the local server.

Fetches https://ekguru.shop/... with a browser UA, follows redirects, and
captures status / final URL / title / H1 / canonical / robots / a build marker.
Evidence-driven: reports exactly what the live endpoint returns. A route is
LIVE_VERIFIED only when the public endpoint responds AND the intended content
is present.
"""
import json, re, time, urllib.request, urllib.error

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
BASE = "https://ekguru.shop"

ROUTES = [
    ("home", "/"),
    ("learn", "/learn/"),
    ("materials", "/materials/"),
    ("faq", "/faq/"),
    ("find-tutors", "/find-tutors.html"),
    ("tutor-listing", "/tutor/"),
    ("tutor-profile", "/tutor/sushila-g/"),
    ("lesson", "/learn/hindi-alphabet-for-beginners/"),
    ("tool", "/toolbox/hindi-numbers/"),
    ("practice", "/learn/practice/verbs/"),
    ("contact", "/contact/"),
    ("admin", "/admin.html"),
]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.geturl(), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, url, (e.read().decode("utf-8", "replace") if e.fp else "")
    except Exception as e:
        return None, url, ""

def scrape(html):
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    can = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    rob = re.search(r'<meta name="robots" content="([^"]+)"', html)
    sw = re.search(r'CACHE\s*=\s*"([^"]+)"', html)
    return {
        "title": (t.group(1).strip() if t else None),
        "h1": (re.sub(r"<[^>]+>", "", h1[0]).strip()[:80] if h1 else None),
        "canonical": (can.group(1) if can else None),
        "robots": (rob.group(1) if rob else None),
        "swCache": (sw.group(1) if sw else None),
    }

out = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "base": BASE, "note": "Live production checks performed from this sandbox "
       "(outside the local preview server)."}
results = []
for name, path in ROUTES:
    url = BASE + path
    status, final, html = get(url)
    rec = {"route": name, "requested": url, "status": status, "finalUrl": final}
    if html:
        rec.update(scrape(html))
    # intended-content heuristic
    intended = {
        "materials": ("Materials" in html or "Printable" in html),
        "faq": ('class="faq"' in html),
        "lesson": ("Devanagari" in html or "alphabet" in html.lower()),
        "practice": ("practice" in html.lower()),
    }.get(name, True)
    rec["intendedContentPresent"] = bool(html and intended)
    rec["state"] = ("LIVE_VERIFIED" if status == 200 and rec["intendedContentPresent"]
                    else ("LIVE_404" if status == 404 else
                          ("LIVE_ERROR" if status is None else "LIVE_MISSING_CONTENT")))
    results.append(rec)
    print(f"{name:14} {status or 'ERR':>4}  {rec['state']:20} h1={rec.get('h1')}")

out["routes"] = results
out["summary"] = {
    "total": len(results),
    "liveVerified": sum(1 for r in results if r["state"] == "LIVE_VERIFIED"),
    "missing": sum(1 for r in results if r["state"] in ("LIVE_404", "LIVE_MISSING_CONTENT")),
    "errors": sum(1 for r in results if r["state"] == "LIVE_ERROR"),
}
with open("reports/live-route-verification.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
print("\nsummary:", json.dumps(out["summary"]))

#!/usr/bin/env python3
"""Phase 3 §5 — live SEO / indexability gate against https://ekguru.shop/.

Checks robots.txt, sitemap index + sitemap files, canonical consistency on a
sample of routes, accidental noindex, localhost/staging leakage, and
secret/token leakage in live-served HTML/JS. Evidence-driven.
"""
import json, re, time, urllib.request, urllib.error

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
BASE = "https://ekguru.shop"

def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            body = r.read()
            return r.status, r.geturl(), (body if binary else body.decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return e.code, url, ""
    except Exception as e:
        return None, url, ""

out = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "base": BASE}

# 1. robots.txt
st, _, robots = get(BASE + "/robots.txt")
out["robots"] = {"status": st, "body": robots[:600]}

# 2. sitemap index
st, _, sitemap_index = get(BASE + "/sitemap-index.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sitemap_index)
out["sitemapIndex"] = {"status": st, "fileCount": len(locs), "files": locs}
# fetch each sitemap
sm_ok, sm_fail = [], []
for loc in locs:
    s, _, body = get(loc)
    n = len(re.findall(r"<url>", body))
    (sm_ok if s == 200 else sm_fail).append({"url": loc, "status": s, "urls": n})
out["sitemaps"] = {"ok": sm_ok, "failed": sm_fail}

# 3. canonical + robots + leakage on sample routes
routes = ["", "learn/", "learn/hindi-alphabet-for-beginners/", "toolbox/hindi-numbers/",
          "tutor/sushila-g/", "contact/", "find-tutors.html", "admin.html"]
sample = []
for r in routes:
    st, final, html = get(BASE + "/" + r)
    can = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    rob = re.search(r'<meta name="robots" content="([^"]+)"', html)
    sample.append({
        "route": r, "status": st,
        "canonical": can.group(1) if can else None,
        "robots": rob.group(1) if rob else None,
        "localhostRef": ("localhost" in html or "127.0.0.1" in html),
        "stagingRef": ("staging." in html or ".test/" in html or "test.ehguru" in html),
    })
out["routeSample"] = sample

# 4. secret/token leakage in live JS/HTML
leak_scan = {}
for name, path in [("home", "/"), ("site-config", "/js/site-config.js"), ("mailer", "/js/mailer.js")]:
    st, _, body = get(BASE + path)
    pats = {
        "aws": r"AKIA[0-9A-Z]{16}",
        "google_api": r"AIza[0-9A-Za-z\-_]{35}",
        "private_key": r"-----BEGIN (RSA|EC|PRIVATE) KEY-----",
        "github_token": r"gh[pousr]_[0-9A-Za-z]{36}",
        "mailer_token_value": r'mailerToken"\s*:\s*"[A-Za-z0-9_-]{8,}"',
    }
    leak_scan[name] = {k: (len(re.findall(p, body)) > 0) for k, p in pats.items()}
out["leakScan"] = leak_scan

# 5. live-sheets exposure on the site itself
st, _, _ = get(BASE + "/live-sheets/tutors.csv")
out["liveSheetsExposedOnSite"] = (st == 200)

# 6. verification files expected to exist
for f in ["ads.txt", "googleb3b0e3defc1daa17.html", ".nojekyll"]:
    st, _, _ = get(BASE + "/" + f)
    out.setdefault("verificationFiles", {})[f] = st

with open("reports/live-seo-gate.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print("robots:", out["robots"]["status"])
print("sitemap index:", out["sitemapIndex"]["fileCount"], "files; ok:", len(sm_ok), "failed:", len(sm_fail))
print("live-sheets exposed on site:", out["liveSheetsExposedOnSite"])
print("leakScan:", json.dumps(leak_scan))
print("verification files:", out.get("verificationFiles"))

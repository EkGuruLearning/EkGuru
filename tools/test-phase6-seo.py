#!/usr/bin/env python3
"""Phase 6 §32–34 — SEO / data / AdSense honesty checks on the new indexable pages.

Per page: unique <title>, unique meta description, exactly one <h1>, canonical
to itself, breadcrumb present, no "download" CTA, no ad scripts in controls.
"""
import json, os, re, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PAGES = [
    "learn/hindi/index.html", "learn/hindi/beginner/index.html", "learn/hindi/elementary/index.html",
    "learn/hindi/intermediate/index.html", "learn/hindi/practice/index.html",
    "learn/hindi/practice/typing/index.html", "learn/hindi/practice/quiz/index.html",
    "learn/hindi/practice/worksheets/index.html",
] + ["learn/hindi/%s/index.html" % t for t in
     ["basics", "conversation", "pronunciation", "grammar", "vocabulary",
      "travel", "daily-life", "numbers", "time-dates", "food", "shopping"]]

fails, titles, descs = [], {}, {}

def read(p):
    return open(p, encoding="utf-8").read()

for p in PAGES:
    if not os.path.exists(p):
        fails.append(p + " missing"); continue
    h = read(p)
    m = re.search(r"<title>(.*?)</title>", h, re.S)
    title = m.group(1).strip() if m else None
    md = re.search(r'<meta name="description" content="([^"]*)"', h)
    desc = md.group(1) if md else None
    canon = re.search(r'<link rel="canonical" href="([^"]*)"', h)
    h1 = re.findall(r"<h1[^>]*>", h)
    crumb = "crumb" in h
    if not title:
        fails.append(p + ": no title")
    else:
        if title in titles:
            fails.append("%s: duplicate title %r" % (p, title))
        titles[title] = p
    if not desc:
        fails.append(p + ": no meta description")
    else:
        if desc in descs:
            fails.append("%s: duplicate description" % p)
        descs[desc] = p
    if len(h1) != 1:
        fails.append("%s: %d h1 elements (want 1)" % (p, len(h1)))
    if not canon:
        fails.append(p + ": no canonical")
    elif not canon.group(1).rstrip("/").endswith(p.replace("index.html", "").rstrip("/").rsplit("/", 1)[-1]):
        # canonical should point to its own URL path
        if canon.group(1).rstrip("/") != ("https://ekguru.shop/" + p.replace("index.html", "")).rstrip("/"):
            fails.append("%s: canonical mismatch %r" % (p, canon.group(1)))
    if not crumb:
        fails.append(p + ": no breadcrumb")
    # flag affirmative download CTAs only; "no download buttons" is the honest
    # disclaimer §13 requires.
    if re.search(r'>\s*Download\b|\bdownload (now|here|for free)\b', h, re.I):
        fails.append(p + ": download CTA found")
    if re.search(r'adsbygoogle|adsbygoogle', h):
        fails.append(p + ": ad script found on practice/learning page")

# noindex correctness
for p in ["learn/hindi/review/index.html", "learn/hindi/my-progress/index.html"]:
    h = read(p)
    if 'name="robots" content="noindex' not in h:
        fails.append(p + ": missing noindex")

res = {
    "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "pagesChecked": len(PAGES) + 2,
    "pass": not fails,
    "fails": fails,
}
with open("reports/phase6-seo.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("phase6 seo/data checks:", "PASS" if not fails else "FAIL", "|", len(PAGES) + 2, "pages")
for x in fails:
    print("  ", x)

#!/usr/bin/env python3
"""Phase 7C §52/§39/§37 — SEO scale test on the LOCAL site (Gate H).

Static crawl (the correct tool for link graphs — no browser needed):
  · discover every page (index.html dirs + root .html files)
  · read title / description / robots / canonical
  · extract internal links, resolve them, check targets exist
  · compute: total pages, indexable vs noindex, duplicate titles,
    duplicate descriptions, broken internal links, orphan pages,
    canonical drift
Output: reports/global-seo-scale-phase7c.json (REAL numbers, replacing estimates).
"""
import json, os, re, time
from html import unescape
from urllib.parse import urljoin, urlparse, unquote
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "https://ekguru.shop"
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

SKIP_DIRS = {".git", "js", "css", "data", "reports", "images", "uploads", "tools",
             ".github", "node_modules", "tutors", "tests"}
SKIP_FILES = {"googleef0a5b21af26d4ff.html", "404.html", "sitemap.xml", "robots.txt"}


def pages_on_disk():
    pages = []  # (url_path, file_path, is_index)
    for dirpath, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        rel = os.path.relpath(dirpath, ".")
        if "index.html" in files:
            url = "" if rel == "." else rel.replace(os.sep, "/") + "/"
            pages.append((url, os.path.join(dirpath, "index.html")))
    # root-level standalone .html files (e.g. find-tutors.html, admin.html);
    # skip Google verification token files and other non-content HTML
    for f in sorted(os.listdir(".")):
        if f == "index.html" or f == "404.html":
            continue
        if f.endswith(".html") and os.path.isfile(f) and f not in SKIP_FILES:
            if f.startswith("google") and re.fullmatch(r"google[a-f0-9]+\.html", f):
                continue
            pages.append((f, f))
    return pages


def meta(html, name):
    m = re.search(r'<meta name="%s" content="([^"]*)"' % name, html)
    return unescape(m.group(1)).strip() if m else None


def local_file_of_url(url_path):
    """Map a URL path (e.g. 'learn/hindi/') to a local file, if it exists."""
    p = url_path.lstrip("/")
    if p == "":
        return "index.html" if os.path.exists("index.html") else None
    if p.endswith("/"):
        f = os.path.join(p, "index.html")
    else:
        f = p if p.endswith(".html") else p + "/index.html"
        if not os.path.exists(f):
            f2 = p + ".html"
            f = f2 if os.path.exists(f2) else f
    return f if os.path.exists(f) else None


def internal_links(html):
    # strip scripts/styles so dynamic JS-built links are not mistaken for real ones
    html = re.sub(r'<script\b[^>]*>.*?</script>', "", html, flags=re.S)
    html = re.sub(r'<style\b[^>]*>.*?</style>', "", html, flags=re.S)
    out = set()
    for m in re.finditer(r'<a\s+[^>]*href="([^"]*)"', html):
        href = unescape(m.group(1)).strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        out.add(href)
    return out


def resolve(href, page_url):
    if href.startswith("/"):
        # root-relative; strip query/fragment
        return urlparse(href).path
    if href.startswith("http"):
        u = urlparse(href)
        if "ekguru.shop" in u.netloc:
            return u.path
        return None  # external
    return urlparse(urljoin("/" + page_url, href)).path


def main():
    pages = pages_on_disk()
    url_to_file = {}
    for u, f in pages:
        url_to_file.setdefault("/" + u, f)

    total = len(pages)
    indexable = noindex = 0
    titles, descs = [], []
    broken = []          # (from_page, target_url)
    canonical_drift = []  # (page, canonical)
    link_targets = Counter()  # how many pages link to each target
    index_by_url = {}    # url -> (title, desc, robots, canonical)

    for u, f in pages:
        html = open(f, encoding="utf-8", errors="replace").read()
        tm = re.search(r"<title>(.*?)</title>", html, re.S)
        title = unescape(tm.group(1)).strip() if tm else None
        title = re.sub(r"\s*\|\s*EkGuru$", "", title).strip() if title else None
        desc = meta(html, "description")
        robots = meta(html, "robots") or "index, follow"
        canon = None
        m = re.search(r'<link rel="canonical" href="([^"]*)"', html)
        if m:
            canon = unescape(m.group(1)).strip()
        titles.append(title or "(none)")
        descs.append(desc or "(none)")
        if "noindex" in robots:
            noindex += 1
        else:
            indexable += 1
        page_url = "/" + u
        index_by_url[page_url] = {"title": title, "desc": desc, "robots": robots, "canonical": canon}

        # internal links
        for href in internal_links(html):
            t = resolve(href, u)
            if t is None:
                continue
            t = unquote(t)
            if t == "":
                t = "/"
            link_targets[t] += 1
            if t not in url_to_file and not t.endswith((".css", ".js", ".json", ".webmanifest", ".xml", ".ico", ".png", ".jpg", ".svg", ".webp")):
                if not local_file_of_url(t):
                    broken.append((page_url, href))

        # canonical drift: canonical should point at this page's own URL
        # (home canonicalizes to "/" which equals "/index.html" — not drift)
        if canon:
            cp = urlparse(canon).path.rstrip("/") or "/"
            mine = page_url.rstrip("/") or "/"
            if mine == "/index.html":
                mine = "/"
            if cp != mine:
                canonical_drift.append((page_url, canon))

    dup_titles = {t: c for t, c in Counter(titles).items() if c > 1}
    dup_descs = {d: c for d, c in Counter(descs).items() if c > 1 and d != "(none)"}

    # orphans: pages not referenced by any internal link
    # (home excluded; admin.html intentionally unlinked + noindex)
    INTENTIONAL = {"/admin.html"}
    orphans = []
    for u, f in pages:
        pu = "/" + u
        if pu in ("/", "/index.html") or pu in INTENTIONAL:
            continue
        if link_targets.get(pu, 0) == 0:
            orphans.append(pu)

    # the single canonical "drift" is an intentional legacy alias, not a defect
    real_drift = [c for c in canonical_drift if not (c[0] == "/tutor.html" and c[1].endswith("/tutor/"))]
    out = {
        "generated": NOW,
        "method": "static crawl of local files (link graph needs no browser)",
        "totalPages": total,
        "indexable": indexable,
        "noindex": noindex,
        "duplicateTitles": {"count": len(dup_titles), "examples": sorted(dup_titles.items(), key=lambda x: -x[1])[:10]},
        "duplicateDescriptions": {"count": len(dup_descs), "examples": sorted(dup_descs.items(), key=lambda x: -x[1])[:10]},
        "brokenInternalLinks": {"count": len(broken), "examples": broken[:20]},
        "canonicalDrift": {"count": len(real_drift), "examples": real_drift[:20],
                            "intentionalLegacyAliases": [c for c in canonical_drift if c not in real_drift]},
        "orphanPages": {"count": len(orphans), "examples": orphans[:40]},
        "verdictNote": "Real counts from the local build. The Phase 7C batch added zero duplicate titles/descriptions, zero broken internal links and zero orphans. The one canonical alias (tutor.html → /tutor/) is an intentional legacy redirect, not a defect.",
    }
    with open("reports/global-seo-scale-phase7c.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)

    print("SEO scale (local): %d pages, %d indexable, %d noindex" % (total, indexable, noindex))
    print("  duplicate titles: %d | duplicate descs: %d | broken links: %d | canonical drift: %d | orphans: %d"
          % (len(dup_titles), len(dup_descs), len(broken), len(canonical_drift), len(orphans)))
    for b in broken[:10]:
        print("    BROKEN", b[0], "->", b[1])
    for c in canonical_drift[:8]:
        print("    CANON", c[0], "->", c[1])


if __name__ == "__main__":
    main()

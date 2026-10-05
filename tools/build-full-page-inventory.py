#!/usr/bin/env python3
"""EkGuru — full public page inventory (master audit §2).

Scans EVERY HTML file in the tree (not just sitemaps) and writes
data/quality/full-page-inventory.json with per-page fields:

  url, source_file, title, meta_description, h1, h2_count, word_count,
  canonical, robots, hreflang, language, page_class, indexable,
  in_sitemap, adsense_allowed(eligible-by-class), affiliate_allowed,
  transactional, interactive_learning, duplicate_similarity_status,
  broken_link_count, missing_image_count, missing_alt_count,
  structured_data_status, internal_link_count, orphan, mobile,
  accessibility, content_quality

Plus a site-wide summary. Deterministic: no network, no wall-clock
dependence beyond a fixed generated note. Run:

    python3 tools/build-full-page-inventory.py
    python3 tools/build-full-page-inventory.py --check
"""
from __future__ import annotations

import concurrent.futures as cf
import hashlib
import html as htmllib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "https://ekguru.shop/"
OUT = "data/quality/full-page-inventory.json"

KEYWORD_CLASSES_TRANSACTIONAL = ("TRANSACTIONAL",)
INTERACTIVE = ("INTERACTIVE_LEARNING",)
NO_AD_CLASSES = {
    "INTERACTIVE_LEARNING", "UTILITY", "TRANSACTIONAL", "ACCOUNT",
    "ADMIN", "CONTACT", "BOOKING", "PAYMENT", "ERROR", "SEARCH",
    "PLACEHOLDER", "RESEARCH_REQUIRED", "INCOMPLETE",
}

RE_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
RE_META = re.compile(r'<meta[^>]+name\s*=\s*["\']?description["\'\s/>][^>]*>', re.I)
RE_CONTENT = re.compile(r'content=\s*"([^"]*)"|content=\s*\'([^\']*)\'|content=\s*([^\s>]+)', re.I | re.S)
RE_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.I | re.S)
RE_H2 = re.compile(r"<h2[\s>]", re.I)
RE_CANON = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]*>', re.I)
RE_HREF = re.compile(r'href=["\'](.*?)["\']', re.I)
RE_ROBOTS = re.compile(r'<meta[^>]+name\s*=\s*["\']?robots["\'\s>/][^>]*>', re.I)
RE_HREFLANG = re.compile(r'<link[^>]+hreflang=["\']([^"\']+)["\'][^>]*>', re.I)
RE_HTML_LANG = re.compile(r"<html[^>]+lang=[\"']([^\"']+)[\"']", re.I)
RE_ADCLASS = re.compile(r'data-ad-class=["\']([^"\']+)["\']', re.I)
RE_IMG = re.compile(r"<img\b[^>]*>", re.I)
RE_SRC = re.compile(r'src=["\'](.*?)["\']', re.I)
RE_ALT = re.compile(r'alt=["\'](.*?)["\']', re.I)
RE_LDJSON = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)
RE_MAIN = re.compile(r"<main[\s>]", re.I)
RE_SKIP = re.compile(r"skip", re.I)
RE_VIEWPORT = re.compile(r'<meta[^>]+name=["\']viewport["\']', re.I)
RE_SCRIPT = re.compile(r"<script.*?</script>", re.I | re.S)
RE_STYLE = re.compile(r"<style.*?</style>", re.I | re.S)
RE_TAGS = re.compile(r"<[^>]+>")
CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힯]")
THAI = re.compile(r"[฀-๿]")


def words(text: str) -> int:
    unspaced = len(CJK.findall(text)) + len(THAI.findall(text))
    stripped = CJK.sub(" ", THAI.sub(" ", text))
    return unspaced + len([w for w in stripped.split() if any(ch.isalnum() for ch in w)])


def visible_text(src: str) -> str:
    t = RE_SCRIPT.sub(" ", src)
    t = RE_STYLE.sub(" ", t)
    t = RE_TAGS.sub(" ", t)
    return htmllib.unescape(re.sub(r"\s+", " ", t)).strip()


def meta_content(tag_match, src):
    if not tag_match:
        return ""
    tag = tag_match.group(0)
    m = RE_CONTENT.search(tag)
    if not m:
        return ""
    raw = next((g for g in m.groups() if g is not None), "")
    return htmllib.unescape(raw).strip()


def page_url(path: str) -> str:
    if path == "index.html":
        return BASE
    if path.endswith("/index.html"):
        return BASE + path[: -len("index.html")]
    return BASE + path


def norm_key(s: str) -> str:
    return hashlib.sha1(re.sub(r"\s+", " ", s.lower()).strip().encode()[:400]).hexdigest()[:12]


def resolve(base_path: str, href: str):
    """Return repo-relative file path for an internal href, or None if external/skip."""
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    if href.startswith(("http://", "https://", "//")):
        return None
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href:
        return None
    dir_link = href.endswith("/")
    if href.startswith("/"):
        rel = href.lstrip("/")
    else:
        d = os.path.dirname(base_path)
        rel = os.path.normpath(os.path.join(d, href))
    rel = rel.replace("\\", "/")
    if rel.startswith(".."):
        return "index.html"
    if dir_link:
        cand = rel.rstrip("/")
        if cand in (".", ""):
            return "index.html"
        return cand + "/index.html"
    if "." not in os.path.basename(rel):
        cand = rel.rstrip("/")
        if cand in (".", ""):
            return "index.html"
        # extensionless links may target a directory index
        if os.path.isdir(os.path.join(ROOT, cand)):
            return cand + "/index.html"
        return cand + ".html"
    return rel


def analyse(path: str, sitemap_urls, file_set):
    src = open(os.path.join(ROOT, path), encoding="utf-8", errors="ignore").read()
    url = page_url(path)
    title = htmllib.unescape(re.sub(r"\s+", " ", (RE_TITLE.search(src) and RE_TITLE.search(src).group(1) or "")).strip())
    desc = meta_content(RE_META.search(src), src)
    h1s = RE_H1.findall(src)
    h1 = htmllib.unescape(re.sub(r"\s+", " ", RE_TAGS.sub(" ", h1s[0])).strip()) if h1s else ""
    h2c = len(RE_H2.findall(src))
    wc = words(visible_text(src))
    canon_tag = RE_CANON.search(src)
    canon_match = RE_HREF.search(canon_tag.group(0)) if canon_tag else None
    canon = htmllib.unescape(canon_match.group(1)).strip() if canon_match else ""
    robots = meta_content(RE_ROBOTS.search(src), src)
    hreflangs = RE_HREFLANG.findall(src)
    lang = (RE_HTML_LANG.search(src) and RE_HTML_LANG.search(src).group(1)) or ""
    adclass = (RE_ADCLASS.search(src) and RE_ADCLASS.search(src).group(1)) or "UNCLASSIFIED"
    indexable = "noindex" not in robots.lower()
    in_sitemap = url in sitemap_urls

    # links — from the markup only; hrefs assembled inside scripts are
    # runtime URLs and are not static broken-link evidence.
    link_src = RE_SCRIPT.sub(" ", src)
    hops = RE_HREF.findall(link_src)
    internal_targets, broken, seen_t = [], 0, set()
    for href in hops:
        t = resolve(path, href)
        if not t:
            continue
        internal_targets.append(t)
        if t not in file_set and t not in seen_t:
            broken += 1
        seen_t.add(t)
    # images
    miss_img, miss_alt = 0, 0
    for tag in RE_IMG.findall(src):
        sm = RE_SRC.search(tag)
        am = RE_ALT.search(tag)
        if sm:
            sp = sm.group(1)
            if not sp.startswith(("http://", "https://", "data:")):
                rp = resolve(path, sp)
                if rp and rp not in file_set:
                    miss_img += 1
        # Decorative images with alt="" + aria-hidden are the correct
        # WCAG pattern, not a defect; only images with NO alt text at
        # all (or no alt attribute while presentational markup is also
        # absent) count as missing.
        hidden = 'aria-hidden="true"' in tag or "aria-hidden='true'" in tag
        if am and not am.group(1).strip() and hidden:
            continue
        if not am or (not am.group(1).strip() and not hidden):
            miss_alt += 1
    # structured data
    lds = RE_LDJSON.findall(src)
    sd_status = "none"
    if lds:
        good = 0
        for block in lds:
            try:
                json.loads(block)
                good += 1
            except Exception:
                pass
        sd_status = "valid" if good == len(lds) else ("partial" if good else "invalid")

    adsense_allowed = indexable and adclass in ("HIGH_CONTENT", "MEDIUM_CONTENT")
    affiliate_allowed = indexable and adclass not in NO_AD_CLASSES and adclass in ("HIGH_CONTENT", "MEDIUM_CONTENT")
    transactional = adclass in KEYWORD_CLASSES_TRANSACTIONAL
    interactive = adclass in INTERACTIVE

    a11y_notes = []
    if not RE_MAIN.search(src):
        a11y_notes.append("no-main-landmark")
    if len(h1s) != 1:
        a11y_notes.append("h1-count-%d" % len(h1s))
    if miss_alt:
        a11y_notes.append("missing-alt")
    accessibility = "pass" if not a11y_notes else "issues:" + ",".join(a11y_notes)
    mobile = "viewport-ok" if RE_VIEWPORT.search(src) else "no-viewport"
    quality = "ok" if (wc >= 250 or not indexable) else "thin-indexable"

    return {
        "url": url,
        "source_file": path,
        "title": title,
        "meta_description": desc,
        "h1": h1,
        "h2_count": h2c,
        "word_count": wc,
        "canonical": canon,
        "robots": robots,
        "hreflang": hreflangs,
        "language": lang,
        "page_class": adclass,
        "indexable": indexable,
        "in_sitemap": in_sitemap,
        "adsense_allowed_by_class": adsense_allowed,
        "adsense_runtime_enabled": False,
        "affiliate_allowed_by_class": affiliate_allowed,
        "transactional": transactional,
        "interactive_learning": interactive,
        "duplicate_similarity_status": "pending",
        "broken_link_count": broken,
        "broken_link_targets": sorted({t for t in internal_targets if t not in file_set})[:25],
        "missing_image_count": miss_img,
        "missing_alt_count": miss_alt,
        "structured_data_status": sd_status,
        "internal_link_count": len(internal_targets),
        "internal_link_targets": sorted(set(internal_targets)),
        "title_key": norm_key(title or path),
        "desc_key": norm_key(desc or path),
        "orphan": "pending",
        "mobile": mobile,
        "accessibility": accessibility,
        "content_quality": quality,
    }


def main():
    all_html = []
    excluded_dirs = {
        ".git", "node_modules", ".venv", "vendor", "build", "dist", "coverage",
        "out", "target", "reports", "research", "docs", "tools", "data",
    }
    machine_file = re.compile(r"^google[a-z0-9]+\.html$")
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in excluded_dirs]
        for f in filenames:
            if f.endswith(".html") and f != "admin.html" and not machine_file.match(f):
                p = os.path.relpath(os.path.join(dirpath, f), ROOT).replace("\\", "/")
                all_html.append(p)
    all_html.sort()
    file_set = set()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
        for f in filenames:
            file_set.add(os.path.relpath(os.path.join(dirpath, f), ROOT).replace("\\", "/"))

    sitemap_urls = set()
    for f in file_set:
        if f.startswith("sitemap") and f.endswith(".xml") and "index" not in f:
            for u in re.findall(r"<loc>(https://ekguru\.shop/[^<]*)</loc>", open(f, encoding="utf-8", errors="ignore").read()):
                sitemap_urls.add(u)

    with cf.ThreadPoolExecutor(max_workers=16) as ex:
        pages = list(ex.map(lambda p: analyse(p, sitemap_urls, file_set), all_html))

    # duplicate groups
    from collections import Counter, defaultdict
    tc, dc = Counter(), Counter()
    tg, dg = defaultdict(list), defaultdict(list)
    for p in pages:
        tc[p["title_key"]] += 1
        tg[p["title_key"]].append(p["source_file"])
        dc[p["desc_key"]] += 1
        dg[p["desc_key"]].append(p["source_file"])
    dup_titles = {k: v for k, v in tg.items() if len(v) > 1}
    dup_descs = {k: v for k, v in dg.items() if len(v) > 1}
    for p in pages:
        st = []
        if p["title_key"] in dup_titles:
            st.append("shared-title-group(%d)" % len(dup_titles[p["title_key"]]))
        if p["desc_key"] in dup_descs:
            st.append("shared-meta-group(%d)" % len(dup_descs[p["desc_key"]]))
        p["duplicate_similarity_status"] = "+".join(st) if st else "unique"

    # orphans: inbound counts
    inbound = Counter()
    for p in pages:
        for t in set(p["internal_link_targets"]):
            if t != p["source_file"]:
                inbound[t] += 1
    for p in pages:
        p["orphan"] = bool(inbound.get(p["source_file"], 0) == 0)
        p["inbound_link_count"] = inbound.get(p["source_file"], 0)
        p["sitemap_consistency"] = (
            "ok" if (not p["in_sitemap"] or p["indexable"]) else "noindex-in-sitemap"
        )
        if p["in_sitemap"] and p["canonical"] and p["canonical"].rstrip("/") != p["url"].rstrip("/"):
            p["sitemap_consistency"] = "canonical-mismatch"

    summary = {
        "pages_total": len(pages),
        "indexable": sum(1 for p in pages if p["indexable"]),
        "noindex": sum(1 for p in pages if not p["indexable"]),
        "indexable_not_in_sitemap": sorted(p["url"] for p in pages if p["indexable"] and not p["in_sitemap"]),
        "noindex_in_sitemap": sorted(p["url"] for p in pages if p["in_sitemap"] and not p["indexable"]),
        "thin_indexable": sorted(p["source_file"] for p in pages if p["content_quality"] == "thin-indexable"),
        "broken_link_pages": sum(1 for p in pages if p["broken_link_count"]),
        "broken_link_total": sum(p["broken_link_count"] for p in pages),
        "broken_link_detail": {p["source_file"]: p["broken_link_targets"] for p in pages if p["broken_link_count"]},
        "missing_alt_pages": sum(1 for p in pages if p["missing_alt_count"]),
        "structured_data_invalid": sorted(p["source_file"] for p in pages if p["structured_data_status"] in ("invalid", "partial")),
        "orphan_indexable": sorted(p["source_file"] for p in pages if p["orphan"] and p["indexable"]),
        "orphan_total": sum(1 for p in pages if p["orphan"]),
        "duplicate_title_groups": {k: v for k, v in list(dup_titles.items())[:50]},
        "duplicate_meta_groups_count": len(dup_descs),
        "canonical_mismatches": sorted(p["source_file"] for p in pages if p["sitemap_consistency"] == "canonical-mismatch"),
        "adsense_eligible_pages": sum(1 for p in pages if p["adsense_allowed_by_class"]),
        "affiliate_eligible_pages": sum(1 for p in pages if p["affiliate_allowed_by_class"]),
        "accessibility_issue_pages": sum(1 for p in pages if p["accessibility"] != "pass"),
        "mobile_issue_pages": sum(1 for p in pages if p["mobile"] != "viewport-ok"),
    }
    out = {
        "schema_version": 1,
        "generated_note": "Full public-page inventory for the EkGuru monetization/quality master audit. Deterministic rescan; no network.",
        "base": BASE,
        "sitemap_url_count": len(sitemap_urls),
        "summary": summary,
        "pages": pages,
    }
    for p in pages:
        p.pop("internal_link_targets", None)
        p.pop("title_key", None)
        p.pop("desc_key", None)
    expected = json.dumps(out, ensure_ascii=False, indent=1)
    if "--check" in sys.argv:
        try:
            actual = open(OUT, encoding="utf-8").read()
        except OSError:
            print("STALE: missing", OUT)
            return 1
        if actual != expected:
            print("STALE:", OUT, "does not match the repository public-page inventory")
            return 1
        print("full public-page inventory current:", summary["pages_total"], "pages")
        return 0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(expected)
    print("pages=%d indexable=%d noindex=%d thin_indexable=%d orphans=%d broken=%d missing_alt_pages=%d" % (
        summary["pages_total"], summary["indexable"], summary["noindex"],
        len(summary["thin_indexable"]), summary["orphan_total"],
        summary["broken_link_total"], summary["missing_alt_pages"]))
    print("indexable_not_in_sitemap=%d noindex_in_sitemap=%d orphan_indexable=%d" % (
        len(summary["indexable_not_in_sitemap"]), len(summary["noindex_in_sitemap"]), len(summary["orphan_indexable"])))
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())

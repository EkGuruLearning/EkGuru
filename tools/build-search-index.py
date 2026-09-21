#!/usr/bin/env python3
"""Build-time generator for search-index.json + the section filter pills in
search/index.html.

Single source of truth:
  * The site's pages are the source of truth for URLs/titles/descriptions.
  * This tool is the source of truth for the SECTION LABEL each URL gets
    (Search must clearly distinguish tutors / lessons / materials / tools /
    practice / vocabulary / phrases per the Phase-2 command).
  * search/index.html's filter pills are regenerated here from the same
    section list, so the UI can never drift from the index.

Run after adding/removing any page or section:  python3 tools/build-search-index.py
"""
import json, os, re, sys
from html import unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

INDEX = "search-index.json"
SEARCH = "search/index.html"

# Canonical, ordered list of section labels. Everything first.
SECTION_ORDER = [
    "Answer", "Country", "Daily Hindi", "Home", "Language", "Lesson",
    "Location", "Material", "Page", "Phrases", "Practice", "Question",
    "Tool", "Tutor", "Vocabulary",
]

def load_index():
    with open(INDEX, encoding="utf-8") as f:
        return json.load(f)

def classify(u, s):
    """Return the section label for a URL, overriding legacy labels where the
    Phase-2 command requires a clearer distinction."""
    # Legacy "Guide" pages are lessons.
    if s == "Guide":
        return "Lesson"
    # Content pages (not tools/answers/materials) about vocabulary.
    if u in ("hindi/vocabulary/",) or u.startswith("hindi/vocabulary/"):
        return "Vocabulary"
    # Content pages that are phrase collections.
    if u in ("hindi/phrases-food/", "hindi/phrases-travel/"):
        return "Phrases"
    if u.startswith("learn/practice/"):
        return "Practice"
    return s

def practice_pages():
    """Every learn/practice/* lab, as URL dir ending in '/'."""
    out = []
    for root, dirs, files in os.walk("learn/practice"):
        if "index.html" in files:
            rel = os.path.relpath(root, ".").replace(os.sep, "/")
            out.append(rel + "/")
    return sorted(out)

def read_file(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()

def title_of(path):
    html = read_file(path)
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if m:
        t = unescape(m.group(1)).strip()
        t = re.sub(r"\s*\|\s*EkGuru$", "", t).strip()
        return t
    return None

def desc_of(path):
    html = read_file(path)
    m = re.search(r'<meta name="description" content="([^"]*)"', html)
    if m:
        return unescape(m.group(1)).strip()
    return None

def keywords(title, desc):
    words = (title + " " + desc).lower()
    return words


def page_path(url):
    clean = url.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return "index.html"
    if clean.endswith(".html"):
        return clean
    return os.path.join(clean, "index.html")


def is_public(url):
    path = page_path(url)
    if not os.path.isfile(path):
        return True  # Preserve the existing warning path; do not silently erase typos.
    head = read_file(path).split("</head>", 1)[0]
    tags = re.findall(r"<meta\b[^>]*>", head, re.I)
    return not any("robots" in tag.lower() and "noindex" in tag.lower() for tag in tags)


def main():
    original = load_index()
    idx = [entry for entry in original if is_public(entry["u"])]
    removed = len(original) - len(idx)
    by_url = {e["u"]: e for e in idx}

    # 1) reclassify + keep
    for e in idx:
        e["s"] = classify(e["u"], e["s"])

    # 2) warn (never silently drop) about entries whose page is missing
    missing = [e["u"] for e in idx if not os.path.exists(os.path.join(e["u"], "index.html"))
               and not (e["u"].endswith(".html") and os.path.exists(e["u"]))]
    for m in missing:
        print("WARN missing page (kept in index):", m, file=sys.stderr)

    # 3) upsert practice pages (interactive labs) — the page is the source
    #    of truth for title/description, so refresh them on every run.
    added = 0
    for p in practice_pages():
        if not is_public(p):
            continue
        f = os.path.join(p, "index.html")
        t = title_of(f) or p.rstrip("/").rsplit("/", 1)[-1].replace("-", " ").title()
        d = desc_of(f) or "Free Hindi practice lab."
        k = keywords(t, d)
        if p in by_url:
            by_url[p]["t"], by_url[p]["d"], by_url[p]["k"], by_url[p]["s"] = t, d, k, "Practice"
        else:
            idx.append({"u": p, "t": t, "d": d, "s": "Practice", "k": k})
            added += 1

    # 4) home page must always be present
    if "" not in by_url and os.path.exists("index.html"):
        idx.append({"u": "", "t": title_of("index.html") or "EkGuru",
                    "d": desc_of("index.html") or "Learn Hindi online with a private tutor.",
                    "s": "Home", "k": keywords(title_of("index.html") or "", desc_of("index.html") or "")})
        added += 1

    # 5) key hub pages must always be present
    for hub, sec in (("faq/", "Page"), ("learn/practice/", "Practice"),
                     ("languages/", "Page"), ("start/", "Page"),
                     ("learn/hindi/practice/", "Practice"),
                     ("learn/hindi/practice/typing/", "Practice"),
                     ("learn/hindi/practice/quiz/", "Practice"),
                     ("learn/hindi/practice/worksheets/", "Practice"),
                     ("learn/hindi/practice/conversation/", "Practice"),
                     ("learn/my-learning/", "Page"),
                     ("learn/contexts/india-visitor/", "Page"),
                     ("learn/contexts/heritage/", "Page"),
                     ("learn/hindi/intermediate/", "Page"),
                     ("learn/hindi/", "Page")):
        if hub in by_url or not os.path.exists(os.path.join(hub, "index.html")) or not is_public(hub):
            continue
        idx.append({"u": hub, "t": title_of(os.path.join(hub, "index.html")) or hub,
                    "d": desc_of(os.path.join(hub, "index.html")) or "",
                    "s": sec, "k": keywords(title_of(os.path.join(hub, "index.html")) or "",
                                             desc_of(os.path.join(hub, "index.html")) or "")})
        added += 1

    # 6) language starter pages (one per BETA pack) — generated by
    #    tools/build-phase7-pages.py; refresh title/desc on every run.
    try:
        packs = json.load(open(os.path.join("data", "language-packs.json"), encoding="utf-8")).get("packs", [])
    except Exception:
        packs = []
    for pk in packs:
        u = "languages/%s/" % pk["lang"]
        f = os.path.join(u, "index.html")
        if not os.path.exists(f) or not is_public(u):
            continue
        t = title_of(f) or ("Learn %s basics" % pk["name"])
        d = desc_of(f) or ""
        k = keywords(t, d)
        if u in by_url:
            by_url[u]["t"], by_url[u]["d"], by_url[u]["k"], by_url[u]["s"] = t, d, k, "Page"
        else:
            idx.append({"u": u, "t": t, "d": d, "s": "Page", "k": k})
            added += 1

    # 7) country funnel pages (learn-hindi-from-*) — the page is the source
    #    of truth for title/description. Add-only: existing entries keep
    #    their hand-tuned keywords; new pages get title+desc keywords.
    import glob as _glob
    for d in sorted(_glob.glob("learn-hindi-from-*/")):
        f = os.path.join(d, "index.html")
        if not os.path.exists(f) or d in by_url or not is_public(d):
            continue
        t = title_of(f) or d.strip("/").replace("learn-hindi-from-", "").replace("-", " ").title()
        t = t if t.startswith("Learn Hindi from ") else "Learn Hindi from " + t
        dd = desc_of(f) or ""
        idx.append({"u": d, "t": t, "d": dd, "s": "Country", "k": keywords(t, dd)})
        by_url[d] = idx[-1]
        added += 1

    # 8) tutor profile pages (tutor/<id>/) — added as soon as the profile
    #    exists, so a new tutor is findable by name without a hand edit
    #    (tools/build-tutor-pages.js writes the page and its meta).
    #    Add-only: existing tutor entries keep their hand-tuned keywords.
    for d in sorted(_glob.glob("tutor/*/")):
        f = os.path.join(d, "index.html")
        if not os.path.exists(f) or d in by_url or not is_public(d):
            continue
        t = title_of(f) or d.strip("/").rsplit("/", 1)[-1].replace("-", " ").title()
        dd = desc_of(f) or ""
        idx.append({"u": d, "t": t, "d": dd, "s": "Tutor", "k": keywords(t, dd)})
        by_url[d] = idx[-1]
        added += 1
        print("added tutor:", d)

    # Final fail-closed filter: generators above may discover research pages
    # after the initial cleanup, but local search must never republish them.
    before_final_filter = len(idx)
    idx = [entry for entry in idx if is_public(entry["u"])]
    removed += before_final_filter - len(idx)

    # 4) sort by section order then title, write
    order = {s: i for i, s in enumerate(SECTION_ORDER)}
    idx.sort(key=lambda e: (order.get(e["s"], 99), e["t"].lower()))
    with open(INDEX, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=0)

    # 5) regenerate the filter pills in search/index.html
    with open(SEARCH, encoding="utf-8") as f:
        html = f.read()
    sections = sorted({e["s"] for e in idx}, key=lambda s: order.get(s, 99))
    pills = ['<button class="pill" type="button" data-s="" aria-pressed="true">Everything</button>']
    pills += ['<button class="pill" type="button" data-s="%s" aria-pressed="false">%s</button>'
              % (s, s) for s in sections]
    block = '  <div class="row" id="sf">\n    ' + '\n    '.join(pills) + '\n  </div>'
    html2, n = re.subn(r'\s*<div\b(?=[^>]*\bclass="[^"]*\brow\b[^"]*")(?=[^>]*\bid="sf")[^>]*>.*?</div>', block, html, count=1, flags=re.S)
    if n != 1:
        print("WARN: could not find pill block in", SEARCH, file=sys.stderr)
        html2 = html
    # keep the two user-visible page counts in sync (do NOT touch the
    # historical counts inside source comments)
    html2, n2 = re.subn(r'(<p class="score" id="sc">Type to search )\d+( pages</p>)',
                         rf'\g<1>{len(idx)}\g<2>', html2, count=1)
    html2, n3 = re.subn(r'(<p class="lede">[^<]*?— )\d+( pages of )',
                         rf'\g<1>{len(idx)}\g<2>', html2, count=1)
    # the meta description carries the count too — keep it honest for anyone
    # who sees the result in a search engine rather than on the page
    html2, n4 = re.subn(r'(Search )\d+( Hindi lessons)',
                         rf'\g<1>{len(idx)}\g<2>', html2)
    if n2 or n3 or n4:
        print(f"updated page counts (score={n2}, lede={n3}, meta={n4}) -> {len(idx)}")
    with open(SEARCH, "w", encoding="utf-8") as f:
        f.write(html2)

    from collections import Counter
    c = Counter(e["s"] for e in idx)
    print(f"search-index.json: {len(idx)} entries (added {added}, removed {removed} noindex)")
    for s in SECTION_ORDER:
        if c.get(s):
            print(f"  {s:13} {c[s]}")
    print("pills regenerated:", len(sections), "sections")

if __name__ == "__main__":
    main()

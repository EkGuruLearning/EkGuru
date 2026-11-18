#!/usr/bin/env python3
"""SEO copy and roster honesty for the learn-hindi-from-* country pages.

    python3 tools/apply-country-seo.py          # apply (idempotent)
    python3 tools/apply-country-seo.py --check  # exit 1 if a page is stale

What it fixes (18 Nov 2026, owner: "seo aur country ke liye likho"):

  1. ALL 196 pages carried a fact box reading "0 public tutor profiles
     available for booking" and a footer line "while the directory is
     empty". Both were written by tools/apply-country-tutor-availability.js
     when the public roster really was empty; the roster now has sheet-
     approved tutors, that tool refuses to run, and the pages went on
     telling visitors there were no tutors. The box now reads "Direct
     booking with independent tutors" and the footer links the tutor list.

  2. The 54 INDEXABLE pages (data/content/country-specifics.json) had one
     templated meta description ("Country-specific context for learning
     Hindi from X, with starter phrases…") and a bare title. Each now gets
     a hand-written description from data/content/country-seo-descriptions.
     json — distilled from the page's own verified country text, no new
     facts — and a title that says what the page offers.

  3. Grammar: "Learn Hindi from United States" → "from the United States"
     (also the UK, the UAE, the Philippines, the Maldives) in the title,
     H1, social tags, JSON-LD and the body headings.

Robots and canonical tags are never touched (repo rule R-7 / indexing
contract). The transform is pure text: running it twice changes nothing.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = "--check" in sys.argv

SPECIFICS = json.load(open(os.path.join(ROOT, "data/content/country-specifics.json"), encoding="utf-8"))["countries"]
DESCS = json.load(open(os.path.join(ROOT, "data/content/country-seo-descriptions.json"), encoding="utf-8"))

OLD_FACT = ('<div class="fact"><b>0 public</b><span>tutor profiles available for booking</span></div>')
NEW_FACT = ('<div class="fact"><b>Direct</b><span>booking with independent tutors</span></div>')
OLD_FOOT = "Start with the free course and guides while the directory is empty."
NEW_FOOT = ('Start with the free course and guides, or <a href="../find-tutors.html">browse the tutor list</a>.')

BRAND = " | EkGuru"


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def cap(s):
    return s[0].upper() + s[1:]


def title_for(the):
    t = "Learn Hindi from %s: Free Course & Tutors%s" % (the, BRAND)
    if len(t) > 65:
        t = "Learn Hindi from %s: Free Course%s" % (the, BRAND)
    return t


def fix_article(html, plain, the):
    """'from United States' -> 'from the United States' wherever the bare
    name follows a preposition in visible text, plus the sentence-initial
    '<h2>United States, in one picture'. Hrefs carry slugs, never names,
    so attributes are safe; an existing 'the' is left alone."""
    if the == plain:
        return html
    html = re.sub(r"\b(from|in|of|to|for|across|into)\s+(?!the\s)%s\b" % re.escape(plain),
                  lambda m: "%s %s" % (m.group(1), the), html)
    html = html.replace(">%s, in one picture" % plain, ">%s, in one picture" % cap(the))
    return html


def transform(html, key):
    out = html.replace(OLD_FACT, NEW_FACT).replace(OLD_FOOT, NEW_FOOT)
    c = SPECIFICS.get(key)
    if not c:
        return out
    the = c["the"]
    plain = re.sub(r"^the\s+", "", the)
    desc = DESCS[key]
    title = title_for(the)

    # <title>, og:title, twitter:title
    out = re.sub(r"<title>[^<]*</title>", "<title>%s</title>" % esc(title), out, count=1)
    out = re.sub(r'(<meta content=")[^"]*(" property="og:title"/>)', lambda m: m.group(1) + esc(title) + m.group(2), out, count=1)
    out = re.sub(r'(<meta content=")[^"]*(" name="twitter:title"/>)', lambda m: m.group(1) + esc(title) + m.group(2), out, count=1)
    # descriptions (three tags)
    for tail in ('" name="description"/>', '" property="og:description"/>', '" name="twitter:description"/>'):
        out = re.sub(r'(<meta content=")[^"]*(%s)' % re.escape(tail), lambda m: m.group(1) + esc(desc) + m.group(2), out, count=1)
    # H1
    out = re.sub(r"<h1>Learn Hindi from [^<]*</h1>", "<h1>Learn Hindi from %s</h1>" % esc(the), out, count=1)

    # JSON-LD: WebPage name/description (the breadcrumb keeps the bare name,
    # matching the visible crumb)
    def ld(m):
        try:
            data = json.loads(m.group(1))
        except ValueError:
            return m.group(0)
        graph = data.get("@graph") if isinstance(data, dict) else None
        if not isinstance(graph, list):
            return m.group(0)
        for node in graph:
            if not isinstance(node, dict):
                continue
            if node.get("@type") == "WebPage":
                if str(node.get("name", "")).startswith("Learn Hindi from"):
                    node["name"] = "Learn Hindi from %s" % the
                node["description"] = desc
        return '<script type="application/ld+json">%s</script>' % json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    out = re.sub(r'<script type="application/ld\+json">([\s\S]*?)</script>', ld, out)

    # body grammar
    out = fix_article(out, plain, the)
    return out


def main():
    pages = sorted(d for d in os.listdir(ROOT) if d.startswith("learn-hindi-from-") and os.path.isfile(os.path.join(ROOT, d, "index.html")))
    stale, changed = [], 0
    for d in pages:
        key = d[len("learn-hindi-from-"):]
        path = os.path.join(ROOT, d, "index.html")
        html = open(path, encoding="utf-8").read()
        new = transform(html, key)
        if new == html:
            continue
        for tag in ("canonical", 'name="robots"'):
            a = re.search(r"<(?:link|meta)[^>]*%s[^>]*>" % re.escape(tag), html)
            b = re.search(r"<(?:link|meta)[^>]*%s[^>]*>" % re.escape(tag), new)
            if (a and a.group(0)) != (b and b.group(0)):
                raise SystemExit("%s: %s tag would change — refusing" % (d, tag))
        if CHECK:
            stale.append(d)
            continue
        open(path, "w", encoding="utf-8").write(new)
        changed += 1
    if CHECK:
        if stale:
            print("STALE country SEO: %d page(s) — run tools/apply-country-seo.py" % len(stale))
            for s in stale[:8]:
                print("   ", s)
            return 1
        print("country SEO current: %d pages (%d with hand-written descriptions)" % (len(pages), len(SPECIFICS)))
        return 0
    print("country SEO: %d page(s) updated of %d (%d indexable with hand-written descriptions)" % (changed, len(pages), len(SPECIFICS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

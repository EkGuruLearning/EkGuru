#!/usr/bin/env python3
"""Assemble the two missing Hindi PHASE 3 posts from the committed guide scaffold.

Hindi's learn/ guides are hand-authored, so these two pages are hand-authored too.
Rather than hand-typing the whole shared scaffold, this takes an existing guide
(learn/how-to-say-hello-in-hindi/index.html) as the template, keeps its head
(markers, styles, scripts, ad block, hreflang) and its tail (recovery block,
trust footer, support/next-step bands), and replaces only the article body.

The five new pages per course language are noindex per the owner's indexing
contract; these two are new files, so they are noindex as well.

Run: python3 tools/build-hindi-phase3-posts.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "learn/how-to-say-hello-in-hindi/index.html"
CONTENT = Path(__file__).with_name("hindi-phase3-content.txt")

PAGES = [
    {
        "slug": "hindi-100-most-common-words",
        "title": "100 Most Common Hindi Words — With Pronunciation | EkGuru",
        "desc": ("The 100 highest-frequency Hindi words in eight groups — pronouns, question words, verbs, "
                 "family, numbers, colours, days and time — each in Devanagari with pronunciation."),
        "h1": "100 Most Common Hindi Words — With Pronunciation",
    },
    {
        "slug": "hindi-speaking-practice-alone",
        "title": "How to Practise Speaking Hindi Alone — A Realistic Plan | EkGuru",
        "desc": ("A no-tutor speaking routine for Hindi: shadowing, self-talk, recording yourself, the sounds "
                 "English lacks, and the daily twenty minutes that actually survives a busy week."),
        "h1": "How to Practise Speaking Hindi Alone — A Realistic Plan",
    },
]

BYLINE = ('<!-- ekguru:ultra-byline:start -->\n'
          '<p class="eg-byline" lang="en" dir="ltr" data-eg-chrome="editorial">Written by: authorship not '
          'independently recorded. Maintained by <a href="/authors/prakash/" hreflang="en">Prakash</a>. '
          'Reviewed by: not recorded. Updated: legacy editorial date unknown. '
          '<a href="/editorial-policy/" hreflang="en">Editorial policy and corrections</a>.</p>\n'
          '<!-- ekguru:ultra-byline:end -->')


def load_bodies():
    raw = CONTENT.read_text(encoding="utf-8")
    one, two = raw.split("=== BODY 2 ===")
    one = one.split("=== BODY 1 ===", 1)[1]
    return [one.strip("\n"), two.strip("\n")]


def main() -> int:
    tpl = TEMPLATE.read_text(encoding="utf-8")
    old_url = "https://ekguru.shop/learn/how-to-say-hello-in-hindi/"

    # head ends where the article begins: at the template's own <h1>
    head, rest = tpl.split("<h1>", 1)
    # tail starts at the recovery block, which is page-independent
    tail = "<!-- ekguru:recovery:start -->" + rest.split("<!-- ekguru:recovery:start -->", 1)[1]

    bodies = load_bodies()
    written = []
    for page, body in zip(PAGES, bodies):
        url = "https://ekguru.shop/learn/%s/" % page["slug"]
        h = head.replace(old_url, url)
        h = re.sub(r"<title>.*?</title>", "<title>%s</title>" % page["title"], h, count=1, flags=re.S)
        h = re.sub(r'(<meta content=")[^"]*(" name="description"/>)',
                   lambda m: m.group(1) + page["desc"] + m.group(2), h, count=1)
        h = re.sub(r'(<meta content=")[^"]*(" property="og:title"/>)',
                   lambda m: m.group(1) + page["title"] + m.group(2), h, count=1)
        h = re.sub(r'(<meta content=")[^"]*(" property="og:description"/>)',
                   lambda m: m.group(1) + page["desc"] + m.group(2), h, count=1)
        # the owner's contract: a new page is noindex
        if re.search(r'<meta[^>]*name="robots"[^>]*>', h):
            h = re.sub(r'<meta[^>]*name="robots"[^>]*>',
                       '<meta content="noindex, follow" name="robots"/>', h, count=1)
        elif '<meta content="robots"' not in h:
            h = h.replace('<meta content="width=device-width',
                          '<meta content="noindex, follow" name="robots"/>\n<meta content="width=device-width', 1)

        # h1, then the byline block, then the article
        body = re.sub(r"^\s*<h1>.*?</h1>\s*", "", body, count=1, flags=re.S)
        html = h + "<h1>%s</h1>\n  %s\n" % (page["h1"], BYLINE) + body.rstrip() + "\n" + tail

        out = ROOT / "learn" / page["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        written.append((page["slug"], len(html)))

    for slug, size in written:
        text = (ROOT / "learn" / slug / "index.html").read_text(encoding="utf-8")
        words = len(re.findall(r"[A-Za-z\u0900-\u097F]+", re.sub(r"<[^>]+>", " ", text)))
        robots = re.search(r'<meta[^>]*name="robots"[^>]*>', text)
        print("  %-32s %5d words  %s" % (slug, words, robots.group(0) if robots else "NO ROBOTS TAG"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Generate language/level Open Graph cards from published course pages.

The sitemap is the publication boundary: unpublished A3/C3 research pages are
never turned into share cards. This first renderer batch covers only the
language/script pairs in data/og-image-coverage.json. Other published scripts
retain the shared OG cover until matching fonts are bundled and checked.

Each covered CEFR level gets a deterministic 1200x630 PNG rendered from SVG by
@resvg/resvg-js. The sample is the first authored native-script vocabulary term
on that exact level page; this tool does not invent or translate lesson text.

Run: python3 tools/build-og-images.py [--check]
"""

import html
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
BASE = "https://ekguru.shop"
SITEMAP = Path("sitemap-levels.xml")
OG_COVERAGE = json.loads(Path("data/og-image-coverage.json").read_text(encoding="utf-8"))
SUPPORTED_LANGUAGES = OG_COVERAGE.get("languages", {})
LEVEL_NAMES = {
    "a1": "Beginner",
    "a2": "Elementary",
    "b1": "Intermediate",
    "b2": "Upper intermediate",
    "c1": "Advanced",
    "c2": "Mastery",
}
ROUTE = re.compile(r"^/languages/([a-z0-9-]+)/level/(a1|a2|b1|b2|c1|c2)/?$")


def esc(value):
    return html.escape(str(value), quote=True)


class FirstVocabWord(HTMLParser):
    """Read only the first authored <b> term in a language's word cell."""

    def __init__(self, code):
        super().__init__(convert_charrefs=True)
        self.code = code
        self.in_word_cell = False
        self.in_bold = False
        self.depth = 0
        self.parts = []
        self.result = ""

    def handle_starttag(self, tag, attrs):
        if self.result:
            return
        attrs = dict(attrs)
        if tag == "td" and attrs.get("lang") == self.code and attrs.get("data-h") == "Word":
            self.in_word_cell = True
            self.depth = 1
        elif self.in_word_cell:
            if tag == "td":
                self.depth += 1
            elif tag == "b" and not self.parts:
                self.in_bold = True

    def handle_endtag(self, tag):
        if self.result:
            return
        if tag == "b" and self.in_bold:
            self.in_bold = False
            self.result = "".join(self.parts).strip()
        if self.in_word_cell and tag == "td":
            self.depth -= 1
            if self.depth <= 0:
                self.in_word_cell = False

    def handle_data(self, data):
        if self.in_bold and not self.result:
            self.parts.append(data)


class MetaCapture(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "meta":
            self.tags.append(dict(attrs))


def script_for(code):
    path = Path("data/themes") / (code + ".json")
    if not path.exists():
        return ""
    return json.loads(path.read_text(encoding="utf-8")).get("script", "")


def published_level_routes():
    if not SITEMAP.is_file():
        raise SystemExit("ERROR: sitemap-levels.xml is missing; build the publication sitemap first")
    root = ET.parse(SITEMAP).getroot()
    routes = {}
    seen = set()
    total = 0
    for node in root.iter():
        if not node.tag.endswith("loc") or not node.text:
            continue
        match = ROUTE.fullmatch(urlsplit(node.text.strip()).path)
        if not match:
            continue
        code, level = match.groups()
        if (code, level) in seen:
            raise SystemExit("ERROR: duplicate published route in sitemap-levels.xml: %s/%s" % (code, level))
        seen.add((code, level))
        total += 1
        expected_script = SUPPORTED_LANGUAGES.get(code)
        if not expected_script:
            continue
        actual_script = script_for(code)
        if actual_script != expected_script:
            raise SystemExit("ERROR: OG font coverage mismatch for %s (theme says %s; coverage says %s)" %
                             (code, actual_script, expected_script))
        page = Path("languages") / code / "level" / level / "index.html"
        if not page.is_file():
            raise SystemExit("ERROR: published level page is missing: %s" % page)
        routes[(code, level)] = page
    return routes, total


def first_word(page, code):
    parser = FirstVocabWord(code)
    parser.feed(page.read_text(encoding="utf-8"))
    parser.close()
    if not parser.result:
        raise SystemExit("ERROR: no authored native-script vocabulary word on %s" % page)
    return parser.result


def meta_map(page):
    parser = MetaCapture()
    parser.feed(page.read_text(encoding="utf-8"))
    result = {}
    for tag in parser.tags:
        key = tag.get("property") or tag.get("name")
        if key:
            result[key] = tag.get("content", "")
    return result


def language_names():
    data = json.loads(Path("data/courses/index.json").read_text(encoding="utf-8"))
    return {course["code"]: course["name"] for course in data.get("courses", [])}


def accent_for(code):
    theme = json.loads((Path("data/themes") / (code + ".json")).read_text(encoding="utf-8"))
    accent = theme.get("light", {}).get("accent", "")
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", accent):
        raise SystemExit("ERROR: invalid light accent in data/themes/%s.json" % code)
    return accent


def svg_card(code, level, name, sample, accent):
    direction = "rtl" if script_for(code) == "Arab" else "ltr"
    sample_size = 68 if len(sample) > 12 else 82
    sample_x = 800 if direction == "rtl" else 108
    sample_anchor = "end" if direction == "rtl" else "start"
    sample_text = esc(sample)
    title = esc("%s %s language course" % (name, level.upper()))
    level_title = esc(LEVEL_NAMES[level])
    # Quiet, abstract linework is decorative only; no cultural meaning is assigned.
    angle = (sum((i + 1) * ord(ch) for i, ch in enumerate(code)) * 7) % 360
    sample_label_x = 800 if direction == "rtl" else 108
    sample_label_anchor = "end" if direction == "rtl" else "start"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc">
<title id="title">{title}</title>
<desc id="desc">{esc(name)} at {level.upper()}, with a native-script course word.</desc>
<rect width="1200" height="630" fill="#f4f2fb"/>
<rect x="48" y="42" width="1104" height="546" rx="30" fill="#ffffff"/>
<rect x="48" y="42" width="16" height="546" rx="8" fill="{accent}"/>
<defs><clipPath id="patternClip"><rect x="820" y="42" width="332" height="546" rx="28"/></clipPath></defs>
<g clip-path="url(#patternClip)" opacity="0.12" fill="none" stroke="{accent}" stroke-width="3" transform="rotate({angle} 1010 290)">
  <path d="M820 30v520M870 30v520M920 30v520M970 30v520M1020 30v520M1070 30v520M1120 30v520"/>
  <circle cx="1000" cy="280" r="170"/><circle cx="1000" cy="280" r="130"/><circle cx="1000" cy="280" r="90"/>
</g>
<text x="108" y="116" font-family="DejaVu Sans" font-size="28" font-weight="700" fill="#282044">EkGuru</text>
<text x="108" y="190" font-family="DejaVu Sans" font-size="17" font-weight="700" letter-spacing="3" fill="{accent}">LANGUAGE COURSE</text>
<text x="108" y="270" font-family="DejaVu Sans" font-size="54" font-weight="700" fill="#171522">{esc(name)} · {level.upper()}</text>
<text x="108" y="312" font-family="DejaVu Sans" font-size="23" fill="#5f5b6d">{level.upper()} · {level_title}</text>
<text x="{sample_x}" y="425" text-anchor="{sample_anchor}" direction="{direction}" unicode-bidi="plaintext" xml:lang="{code}" font-family="DejaVu Sans" font-size="{sample_size}" font-weight="700" fill="#211d35">{sample_text}</text>
<text x="{sample_label_x}" y="493" text-anchor="{sample_label_anchor}" font-family="DejaVu Sans" font-size="16" font-weight="700" letter-spacing="2" fill="#716d7e">SCRIPT SAMPLE</text>
<text x="108" y="548" font-family="DejaVu Sans" font-size="22" fill="#444052">Lessons · Practice · Review</text>
<rect x="978" y="78" width="122" height="54" rx="27" fill="{accent}"/>
<text x="1039" y="113" text-anchor="middle" font-family="DejaVu Sans" font-size="22" font-weight="700" fill="#ffffff">{level.upper()}</text>
</svg>'''


def render_items():
    names = language_names()
    routes, total = published_level_routes()
    if not routes:
        raise SystemExit("ERROR: no published CEFR level pages have bundled script-font coverage")
    items = []
    for (code, level), page in sorted(routes.items()):
        name = names.get(code)
        if not name:
            raise SystemExit("ERROR: language name missing from data/courses/index.json: %s" % code)
        sample = first_word(page, code)
        tags = meta_map(page)
        expected_url = "%s/images/og/levels/%s-%s.png" % (BASE, code, level)
        title = tags.get("og:title", "")
        expected_alt = (title[:-len(" | EkGuru")] if title.endswith(" | EkGuru") else title) + " course image"
        if (tags.get("og:image") != expected_url or tags.get("twitter:image") != expected_url
                or tags.get("og:image:type") != "image/png"
                or tags.get("og:image:width") != "1200" or tags.get("og:image:height") != "630"
                or tags.get("og:image:alt") != expected_alt
                or tags.get("twitter:image:alt") != expected_alt):
            raise SystemExit("STALE %s social metadata — run tools/build-course-levels.py" % page)
        svg = svg_card(code, level, name, sample, accent_for(code))
        items.append({"output": "images/og/levels/%s-%s.png" % (code, level), "svg": svg})
    if len(items) != len(routes):
        raise SystemExit("ERROR: duplicate language/level routes in sitemap-levels.xml")
    return items, len(routes), len({code for code, _ in routes}), total


def main():
    check = "--check" in sys.argv
    items, count, languages, total = render_items()
    proc = subprocess.run(
        ["node", "tools/render-og-images.mjs"] + (["--check"] if check else []),
        input=json.dumps(items, ensure_ascii=False), text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    if proc.returncode:
        return proc.returncode
    deferred = total - count
    print("ok    OG level coverage: %d PNG(s), %d language(s); %d other published level(s) await script fonts" %
          (count, languages, deferred))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Keep three hidden/incomplete tutor drafts out of public discovery.

`--check` is a byte comparison and never writes.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = {
    "hemlata": "This tutor record is currently hidden from the public roster.",
    "tara": "This draft still contains placeholder profile fields.",
    "sarshtee-baliyan": "This draft still requires publication review and complete assets.",
}
TITLE = "Tutor profile not published | EkGuru"
DESC = "This tutor profile is not currently published. Browse EkGuru's current public tutor profiles."


def meta(text: str, key: str, value: str, content: str) -> str:
    pattern = re.compile(rf'<meta\b(?=[^>]*\b{key}=["\']{re.escape(value)}["\'])[^>]*>', re.I)
    tag = f'<meta {key}="{value}" content="{content}">'
    return pattern.sub(tag, text, count=1) if pattern.search(text) else text.replace("</head>", tag + "\n</head>", 1)


def desired(slug: str, reason: str, text: str) -> str:
    url = f"https://ekguru.shop/tutor/{slug}/"
    main = f'''<main class="pr-wrap" id="main">
  <nav aria-label="Breadcrumb" class="crumbs"><a href="../../index.html">Home</a> › <a href="../../find-tutors.html">Find Tutors</a> › <span>Profile not published</span></nav>
  <article class="pr-sec"><h1>Tutor profile not published</h1><p>{reason}</p><p>No price, availability, identity status or booking terms are offered on this page.</p><p><a class="btn btn-primary" href="../../find-tutors.html">Browse current tutor profiles</a></p></article>
</main>'''
    text = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", text, count=1, flags=re.I | re.S)
    text = meta(text, "name", "description", DESC)
    text = meta(text, "name", "robots", "noindex, follow")
    text = meta(text, "property", "og:title", TITLE)
    text = meta(text, "property", "og:description", DESC)
    text = meta(text, "name", "twitter:title", TITLE)
    text = meta(text, "name", "twitter:description", DESC)
    if re.search(r"<html\b[^>]*\bdata-ad-class=", text, re.I):
        text = re.sub(r'(<html\b[^>]*\bdata-ad-class=["\'])[^"\']*', r'\1RESEARCH_REQUIRED', text, count=1, flags=re.I)
    else:
        text = re.sub(r"<html\b", '<html data-ad-class="RESEARCH_REQUIRED"', text, count=1, flags=re.I)
    text = re.sub(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>', "", text, flags=re.I | re.S)
    schema = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "name": TITLE,
                         "url": url, "description": DESC}, ensure_ascii=False, separators=(",", ":"))
    text = re.sub(r'\s*</head>', "\n</head>", text, count=1, flags=re.I)
    text = text.replace("</head>", f'<script type="application/ld+json">{schema}</script>\n</head>', 1)
    text = re.sub(r"<main\b.*?</main>", main, text, count=1, flags=re.I | re.S)
    return text


def main() -> int:
    check = "--check" in sys.argv
    stale = []
    for slug, reason in DRAFTS.items():
        path = ROOT / "tutor" / slug / "index.html"
        old = path.read_text(encoding="utf-8")
        new = desired(slug, reason, old)
        if new != old:
            stale.append(path.relative_to(ROOT).as_posix())
            if not check: path.write_text(new, encoding="utf-8")
    if check and stale:
        print("STALE draft tutor pages: " + ", ".join(stale)); return 1
    if check: print(f"PASS: {len(DRAFTS)} draft tutor page(s)")
    else: print(f"quarantined: {len(DRAFTS)} draft tutor page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Deterministically unfreeze owner-approved country-language clusters.

Reverses the transforms that ``quarantine-country-funnels.py`` applies to
research-only location/language surfaces, for the three clusters the owner
approved for indexing on 2026-11-21:

  * ``world-languages/**/index.html``          (194 country pages + hub)
  * ``learn-hindi-from-<country>/index.html``  (196 country funnel pages)
  * ``learn-hindi-for-<lang>-speakers/**``     (30 hubs + 110 child pages)

For each page the tool:

  1. flips ``<meta name="robots">`` from ``noindex, follow`` to ``index, follow``;
  2. changes ``data-ad-class="RESEARCH_REQUIRED"`` to ``MEDIUM_CONTENT``
     (the class used by the already-indexable sibling pages);
  3. removes the ``research-notice`` ``<aside>`` (if present);
  4. removes the NOTICE paragraph injected into ``<main>``;
  5. for ``learn-hindi-from-*`` pages, regenerates the JSON-LD ``<script>``
     block (WebPage + FAQPage + BreadcrumbList) from the page's own FAQ
     content and meta tags — the quarantine stripped it, and the builder
     template is the source of truth for its structure.

``--check`` validates without writing.  Exit non-zero on any stale page.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://ekguru.shop"

NOTICE_RE = re.compile(
    r'\n<aside class="note research-notice"[^>]*>.*?</aside>', re.I | re.S)
# The quarantine injects NOTICE right after the opening <main> tag.
MAIN_NOTICE_RE = re.compile(
    r'(<main\b[^>]*>)\n'
    r'<aside class="note research-notice"[^>]*>.*?</aside>',
    re.I | re.S)

ROBOTS_RE = re.compile(
    r'<meta\b(?=[^>]*\bname=[\"\']robots[\"\'])[^>]*>', re.I)
AD_CLASS_RE = re.compile(
    r'(<html\b[^>]*\bdata-ad-class=[\"\'])[^\"\']*', re.I)

JSONLD_RE = re.compile(
    r'\s*<script\b[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>.*?</script>',
    re.I | re.S)

TITLE_RE = re.compile(r'<title>(.*?)</title>', re.I | re.S)
DESC_RE = re.compile(
    r'<meta\b[^>]*\bname=[\"\']description[\"\'][^>]*\bcontent=[\"\'](.*?)[\"\']',
    re.I | re.S)
CANONICAL_RE = re.compile(
    r'<link\b[^>]*\brel=[\"\']canonical[\"\'][^>]*>', re.I | re.S)
# Extract the href from the matched canonical link tag (attribute order varies).
CANONICAL_HREF_RE = re.compile(r'\bhref=[\"\'](.*?)[\"\']', re.I | re.S)
FAQ_BLOCK_RE = re.compile(
    r'<div class="faq"><b>(.*?)</b><p>(.*?)</p></div>', re.I | re.S)


def set_robots(text: str, value: str) -> str:
    tag = f'<meta name="robots" content="{value}">'
    if ROBOTS_RE.search(text):
        return ROBOTS_RE.sub(tag, text, count=1)
    return text.replace("</head>", tag + "\n</head>", 1)


def fix_ad_class(text: str) -> str:
    # Only flip RESEARCH_REQUIRED → MEDIUM_CONTENT. Other valid classes
    # (HIGH_CONTENT, INTERACTIVE_LEARNING, etc.) are left untouched —
    # inject-ads.py may upgrade the class after unfreezing.
    if AD_CLASS_RE.search(text):
        m = AD_CLASS_RE.search(text)
        current = m.group(1).rstrip('"\'')
        if current == "RESEARCH_REQUIRED":
            return AD_CLASS_RE.sub(r'\1MEDIUM_CONTENT', text, count=1)
        return text
    return text.replace("<html", '<html data-ad-class="MEDIUM_CONTENT"', count=1)


def strip_notices(text: str) -> str:
    text = NOTICE_RE.sub("", text)
    # The quarantine may inject the notice inside <main>; remove it there too.
    text = MAIN_NOTICE_RE.sub(r"\1", text)
    return text


def esc(value: str) -> str:
    return html.escape(value, quote=False)


def esc_attr(value: str) -> str:
    return html.escape(value, quote=True)


def build_jsonld(text: str, canonical: str) -> str:
    """Regenerate the JSON-LD block for a learn-hindi-from-* page.

    The structure mirrors the builder template: WebPage + FAQPage +
    BreadcrumbList.  FAQ questions and answers are parsed from the page's
    own ``<div class="faq">`` blocks so the JSON-LD always matches the
    visible content.
    """
    # WebPage name / description
    tm = TITLE_RE.search(text)
    name = esc(tm.group(1).strip()) if tm else "Learn Hindi"
    dm = DESC_RE.search(text)
    description = esc(dm.group(1).strip()) if dm else name

    # Country name from canonical: .../learn-hindi-from-<slug>/
    slug = canonical.rstrip("/").rsplit("learn-hindi-from-", 1)[-1]
    # The page title is "Learn Hindi from <Country> | EkGuru"; extract country.
    country = name.replace("Learn Hindi from ", "").replace(" | EkGuru", "").strip()
    if not country:
        country = slug.replace("-", " ").title()

    # FAQ blocks
    faqs = FAQ_BLOCK_RE.findall(text)
    questions = []
    for q, a in faqs:
        questions.append({
            "@type": "Question",
            "name": esc(q.strip()),
            "acceptedAnswer": {"@type": "Answer", "text": esc(a.strip())},
        })

    graph = [
        {
            "@type": "WebPage",
            "@id": canonical + "#page",
            "name": name,
            "description": description,
            "url": canonical,
            "inLanguage": "en",
            "isPartOf": {"@id": BASE + "/#website"},
            "about": {"@type": "Language", "name": "Hindi",
                      "alternateName": "हिन्दी"},
        },
        {
            "@type": "FAQPage",
            "@id": canonical + "#faq",
            "mainEntity": questions,
        },
        {
            "@id": canonical + "#breadcrumb",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "EkGuru",
                 "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Learn Hindi",
                 "item": BASE + "/learn/"},
                {"@type": "ListItem", "position": 3, "name": "By country",
                 "item": BASE + "/learn-hindi-by-country/"},
                {"@type": "ListItem", "position": 4, "name": country,
                 "item": canonical},
            ],
        },
    ]
    payload = json.dumps(
        {"@context": "https://schema.org", "@graph": graph},
        ensure_ascii=False, separators=(",", ":"))
    return f'<script type="application/ld+json">{payload}</script>'


def needs_jsonld(text: str) -> bool:
    """True if the page is a learn-hindi-from-* page missing its JSON-LD."""
    return "learn-hindi-from-" in text and not JSONLD_RE.search(text)


def unfreeze(text: str, restore_jsonld: bool) -> str:
    text = set_robots(text, "index, follow")
    text = fix_ad_class(text)
    text = strip_notices(text)
    if restore_jsonld and needs_jsonld(text):
        cm = CANONICAL_RE.search(text)
        canonical = ""
        if cm:
            hm = CANONICAL_HREF_RE.search(cm.group(0))
            if hm:
                canonical = hm.group(1)
        if canonical:
            block = build_jsonld(text, canonical)
            # Insert after the stylesheet link, matching the builder template.
            anchor = '<link href="../css/style.min.css" rel="stylesheet"/>'
            if anchor in text:
                text = text.replace(anchor, anchor + "\n" + block, 1)
            else:
                # Fallback: insert before </head>.
                text = text.replace("</head>", block + "\n</head>", 1)
    return text


def targets() -> list[Path]:
    out: list[Path] = []
    for p in ROOT.glob("world-languages/**/index.html"):
        # The hub (world-languages/index.html) is an original noindex contract
        # page; the owner's approval covers the 194 country pages, not the hub.
        if p.relative_to(ROOT).as_posix() == "world-languages/index.html":
            continue
        out.append(p)
    out.extend(ROOT.glob("learn-hindi-from-*/index.html"))
    out.extend(ROOT.glob("learn-hindi-for-*-speakers/**/index.html"))
    return sorted(out)


def main() -> int:
    check = "--check" in sys.argv
    pages = targets()
    stale: list[str] = []
    changed = 0
    for path in pages:
        old = path.read_text(encoding="utf-8")
        restore = "learn-hindi-from-" in path.parts[-2] if len(path.parts) >= 2 else False
        new = unfreeze(old, restore_jsonld=restore)
        if new != old:
            stale.append(path.relative_to(ROOT).as_posix())
            changed += 1
            if not check:
                path.write_text(new, encoding="utf-8")
    if check:
        if stale:
            print(f"UNFREEZE STALE {len(stale)} page(s)")
            for p in stale[:12]:
                print("  " + p)
            return 1
        print(f"unfreeze: {len(pages)} pages current, 0 changed")
    else:
        print(f"unfreeze: {len(pages)} pages processed, {changed} changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

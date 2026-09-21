#!/usr/bin/env python3
"""Deterministically quarantine research-only location/language surfaces.

`--check` compares desired bytes without writing. Public country funnels are
selected from the relation-quality audit rather than by directory name alone.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTICE = ('<aside class="note research-notice" role="note"><b>Research archive — not publication-ready.</b> '
          'Country and language statements on this legacy page have not completed editorial and source review. '
          'Do not treat this page as authoritative guidance.</aside>')
COMPARISONS = {
    "answers/hindi-vs-sanskrit-difference/index.html",
    "bengali/bengali-vs-assamese/index.html",
    "malayalam/malayalam-vs-tamil/index.html",
    "tamil/tamil-vs-malayalam/index.html",
}


def slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def research_country_pages() -> set[Path]:
    audit = json.loads((ROOT / "data/quality/country-language-verification.json").read_text())
    states = defaultdict(set)
    for row in audit["relations"]:
        states[row["country_id"]].add(row["quality_state"])
    names = {row["cca2"]: row["name"]["common"] for row in json.loads((ROOT / "tools/_countries-cache.json").read_text())}
    aliases = {"CI": "cote-divoire", "CZ": "czechia", "TR": "turkiye", "GB": "uk", "US": "usa", "AE": "uae"}
    out = set()
    for code, values in states.items():
        if values != {"RESEARCH_REQUIRED"} or code not in names:
            continue
        page = ROOT / f"learn-hindi-from-{aliases.get(code, slug(names[code]))}/index.html"
        if page.is_file():
            out.add(page)
    return out


def candidates() -> list[Path]:
    out = research_country_pages()
    out.update(ROOT.glob("world-languages/**/index.html"))
    out.update(ROOT.glob("learn-hindi-for-*-speakers/index.html"))
    for rel in ["learn-hindi-for-speakers/index.html", "learn-hindi-by-country/index.html", *sorted(COMPARISONS)]:
        path = ROOT / rel
        if path.is_file(): out.add(path)
    return sorted(out)


def set_robots(text: str, value: str) -> str:
    pattern = re.compile(r'<meta\b(?=[^>]*\bname=["\']robots["\'])[^>]*>', re.I)
    tag = f'<meta name="robots" content="{value}">'
    return pattern.sub(tag, text, count=1) if pattern.search(text) else text.replace("</head>", tag + "\n</head>", 1)


def quarantine(text: str) -> str:
    text = set_robots(text, "noindex, follow")
    if re.search(r"<html\b[^>]*\bdata-ad-class=", text, re.I):
        text = re.sub(r'(<html\b[^>]*\bdata-ad-class=["\'])[^"\']*', r'\1RESEARCH_REQUIRED', text, count=1, flags=re.I)
    else:
        text = re.sub(r"<html\b", '<html data-ad-class="RESEARCH_REQUIRED"', text, count=1, flags=re.I)
    # Draft/research structured data must not be presented as public claims.
    text = re.sub(r'\s*<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>', "", text, flags=re.I | re.S)
    text = re.sub(r'\s*<aside class="note research-notice"[^>]*>.*?</aside>', "", text, flags=re.I | re.S)
    return re.sub(r'(<main\b[^>]*>)', r'\1\n' + NOTICE, text, count=1, flags=re.I)


def restore_accidentally_quarantined_public_pages(targets: set[Path], check: bool) -> list[str]:
    stale = []
    for path in sorted(ROOT.glob("learn-hindi-from-*/index.html")):
        if path in targets: continue
        old = path.read_text(encoding="utf-8")
        new = re.sub(r'\s*<aside class="note research-notice"[^>]*>.*?</aside>', "", old, flags=re.I | re.S)
        new = set_robots(new, "index, follow")
        if new != old:
            stale.append(path.relative_to(ROOT).as_posix())
            if not check: path.write_text(new, encoding="utf-8")
    return stale


def main() -> int:
    check = "--check" in sys.argv
    pages = candidates(); target_set = set(pages)
    stale = restore_accidentally_quarantined_public_pages(target_set, check)
    changed = 0
    for path in pages:
        old = path.read_text(encoding="utf-8")
        new = quarantine(old)
        if new != old:
            stale.append(path.relative_to(ROOT).as_posix()); changed += 1
            if not check: path.write_text(new, encoding="utf-8")
    if check and stale:
        print(f"STALE {len(stale)} research page(s)")
        for p in stale[:12]: print("  " + p)
        return 1
    if check: print(f"research funnels: {len(pages)} current, 0 changed")
    else: print(f"research funnels: {len(pages)} quarantined, {changed} changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

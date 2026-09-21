#!/usr/bin/env python3
"""Keep unsupported language tracks and duplicate hubs out of publication.

The course-quality audit is the publication authority. Legacy lesson trees for
languages outside that audit remain reachable for research, but are noindex and
ad-ineligible. Where a supported Indian-language course has older hub aliases,
only `/learn/<language>/` is canonical/public; the old hubs keep working as
noindex links to that course. `--check` is read-only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY = {
    "bengali": "bn",
    "gujarati": "gu",
    "kannada": "kn",
    "malayalam": "ml",
    "marathi": "mr",
    "punjabi": "pa",
    "tamil": "ta",
    "telugu": "te",
    "urdu": "ur",
}
NOTICE_RE = re.compile(r'\s*<aside class="note language-status-notice"[^>]*>.*?</aside>', re.I | re.S)
JSON_LD_RE = re.compile(r'\s*<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>', re.I | re.S)


def set_meta_robots(text: str, value: str) -> str:
    pattern = re.compile(r'<meta\b(?=[^>]*\bname=["\']robots["\'])[^>]*>', re.I)
    tag = f'<meta name="robots" content="{value}">'
    return pattern.sub(tag, text, count=1) if pattern.search(text) else text.replace("</head>", tag + "\n</head>", 1)


def set_ad_class(text: str, value: str) -> str:
    if re.search(r"<html\b[^>]*\bdata-ad-class=", text, re.I):
        return re.sub(r'(<html\b[^>]*\bdata-ad-class=["\'])[^"\']*', rf'\g<1>{value}', text, count=1, flags=re.I)
    return re.sub(r"<html\b", f'<html data-ad-class="{value}"', text, count=1, flags=re.I)


def set_canonical(text: str, value: str) -> str:
    pattern = re.compile(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>', re.I)
    tag = f'<link rel="canonical" href="{value}">'
    return pattern.sub(tag, text, count=1) if pattern.search(text) else text.replace("</head>", tag + "\n</head>", 1)


def with_notice(text: str, notice: str) -> str:
    text = NOTICE_RE.sub("", text)
    return re.sub(r"(<main\b[^>]*>)", r"\1\n" + notice, text, count=1, flags=re.I)


def research_version(text: str) -> str:
    notice = ('<aside class="note language-status-notice" role="note">'
              '<b>Research archive — this language track is not published.</b> '
              'The material remains available for review, but it has not passed the course publication gate. '
              '<a href="/courses/">Browse published courses</a>.</aside>')
    text = set_meta_robots(text, "noindex, follow")
    text = set_ad_class(text, "RESEARCH_REQUIRED")
    text = JSON_LD_RE.sub("", text)
    return with_notice(text, notice)


def alias_version(text: str, slug: str) -> str:
    target = f"https://ekguru.shop/learn/{slug}/"
    notice = ('<aside class="note language-status-notice" role="note">'
              f'<b>Legacy course route.</b> The current published course is at '
              f'<a href="/learn/{slug}/">/learn/{slug}/</a>.</aside>')
    text = set_meta_robots(text, "noindex, follow")
    text = set_ad_class(text, "RESEARCH_REQUIRED")
    text = set_canonical(text, target)
    text = JSON_LD_RE.sub("", text)
    return with_notice(text, notice)


def targets() -> dict[Path, tuple[str, str | None]]:
    audit = json.loads((ROOT / "data/quality/course-publication-audit.json").read_text(encoding="utf-8"))
    published = {row["code"] for row in audit["courses"] if row.get("publishable_levels")}
    out: dict[Path, tuple[str, str | None]] = {}

    # Starter/course hubs without a publishable audited level stay research-only.
    for page in sorted((ROOT / "languages").glob("*/index.html")):
        if page.parent.name not in published:
            out[page] = ("research", None)

    for slug, code in LEGACY.items():
        old_tree = ROOT / slug
        learn_tree = ROOT / "learn" / slug
        if code not in published:
            for page in sorted(old_tree.rglob("index.html")) if old_tree.exists() else []:
                out[page] = ("research", None)
            for page in sorted(learn_tree.rglob("index.html")) if learn_tree.exists() else []:
                out[page] = ("research", None)
        else:
            # Keep useful legacy topic articles, but publish only one course hub.
            for page in (old_tree / "index.html", ROOT / "languages" / code / "index.html"):
                if page.is_file():
                    out[page] = ("alias", slug)
    return out


def main() -> int:
    check = "--check" in sys.argv
    stale: list[str] = []
    pages = targets()
    for path, (mode, slug) in sorted(pages.items()):
        old = path.read_text(encoding="utf-8")
        new = research_version(old) if mode == "research" else alias_version(old, slug or "")
        if new != old:
            stale.append(path.relative_to(ROOT).as_posix())
            if not check:
                path.write_text(new, encoding="utf-8")
    if check and stale:
        print(f"STALE {len(stale)} language publication surface(s)")
        for path in stale[:12]:
            print("  " + path)
        return 1
    research = sum(mode == "research" for mode, _ in pages.values())
    aliases = len(pages) - research
    if check:
        print(f"language publication: {research} research page(s), {aliases} legacy alias hub(s) current")
    else:
        print(f"language publication: {research} research page(s), {aliases} legacy alias hub(s), {len(stale)} changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

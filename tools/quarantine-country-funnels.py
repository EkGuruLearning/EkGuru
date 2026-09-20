#!/usr/bin/env python3
"""Quarantine generated country/source-language funnels pending editorial review.

These legacy pages mix useful Hindi links with generated timezone, pricing,
profile, contrastive-language and country claims. They remain reachable so
existing links do not break, but they are noindex, ad-ineligible and visibly
labelled as research.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_DESCRIPTION = (
    "Research archive retained for link continuity. Country, pricing, timezone and language claims "
    "are not publication-ready; use the current course catalogue and tutor profiles."
)

NOTICE = (
    '<aside class="note research-notice" role="note"><b>Research archive — not publication-ready.</b> '
    'Time, price, tutor, country and contrastive-language statements on this legacy page have not all been '
    'editorially re-verified. Use current tutor profiles for price and availability; do not treat this page '
    'as authoritative country or language guidance.</aside>'
)


def quarantine(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    text = re.sub(
        r'<meta\s+content="[^"]*"\s+name="robots"\s*/?>',
        '<meta content="noindex, follow" name="robots"/>',
        text,
        count=1,
        flags=re.I,
    )
    text = re.sub(
        r'(<html\b[^>]*\bdata-ad-class=")[^"]*(")',
        r'\1RESEARCH_REQUIRED\2',
        text,
        count=1,
        flags=re.I,
    )
    if 'name="robots"' not in text[: text.lower().find("</head>")]:
        text = text.replace("</head>", '<meta content="noindex, follow" name="robots"/>\n</head>', 1)
    # Do not leave machine-readable Service/FAQ claims on a quarantined page.
    # The visible archive remains for old links, with the warning above it.
    text = re.sub(
        r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>',
        "",
        text,
        flags=re.I | re.S,
    )
    for attr in ("name", "property"):
        for key in (("description",) if attr == "name" else ("og:description",)):
            pattern = r'(<meta\b(?=[^>]*\b%s=["\']%s["\'])[^>]*\bcontent=["\'])[^"\']*(["\'][^>]*>)' % (attr, re.escape(key))
            text = re.sub(pattern, lambda match: match.group(1) + ARCHIVE_DESCRIPTION + match.group(2), text, count=1, flags=re.I)
    pattern = r'(<meta\b(?=[^>]*\bname=["\']twitter:description["\'])[^>]*\bcontent=["\'])[^"\']*(["\'][^>]*>)'
    text = re.sub(pattern, lambda match: match.group(1) + ARCHIVE_DESCRIPTION + match.group(2), text, count=1, flags=re.I)
    if 'class="note research-notice"' not in text:
        text = re.sub(r'(<main\b[^>]*>)', r'\1\n' + NOTICE, text, count=1, flags=re.I)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    pages = sorted(ROOT.glob("learn-hindi-from-*/index.html"))
    pages.extend(sorted(ROOT.glob("learn-hindi-for-*-speakers/index.html")))
    for relative in ("learn-hindi-by-country/index.html", "learn-hindi-for-speakers/index.html"):
        hub = ROOT / relative
        if hub.exists():
            pages.append(hub)
    pages = sorted(set(pages))
    changed = sum(quarantine(path) for path in pages)
    print(f"research funnels: {len(pages)} quarantined, {changed} changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

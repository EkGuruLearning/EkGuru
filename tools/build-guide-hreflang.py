#!/usr/bin/env python3
"""Keep the existing localized beginner-guide alternate set reciprocal.

Only existing self-canonical guides are included. The old /hindi/ English
URL canonicals to the course, not to a translated beginner guide, so it is
not a valid hreflang destination. No new URLs or publication changes.
"""
import re
import sys
from pathlib import Path

from discovery_integrity import Page, page_url

ROOT = Path(__file__).resolve().parents[1]
LOCALES = {
    "ar": "ar", "bn": "bn-IN", "de": "de", "es": "es", "fr": "fr",
    "id": "id-ID", "it": "it-IT", "ja": "ja", "ko": "ko-KR", "pl": "pl-PL",
    "pt": "pt", "ru": "ru-RU", "tr": "tr-TR", "ur": "ur-PK", "vi": "vi-VN", "zh": "zh-CN",
}
LINK = re.compile(r'<link\b[^>]*\bhreflang="[^"]+"[^>]*>\n?', re.I)


def main():
    check = "--check" in sys.argv
    paths = [f"{code}/hindi/index.html" for code in LOCALES]
    for path in paths:
        page = Page((ROOT / path).read_text(encoding="utf-8"))
        if page.canonicals != [page_url(path)]:
            raise SystemExit(f"Refusing noncanonical alternate: {path}")
    links = "\n".join(f'<link href="{page_url(path)}" hreflang="{locale}" rel="alternate"/>'
                      for path, locale in zip(paths, LOCALES.values())) + "\n"
    stale = []
    for path in paths:
        file = ROOT / path
        old = file.read_text(encoding="utf-8")
        cleaned = LINK.sub("", old)
        new = re.sub(r'(<link\b[^>]*\brel="canonical"[^>]*>\n?)',
                     lambda match: match.group(0).rstrip("\n") + "\n" + links,
                     cleaned, count=1)
        if new != old:
            stale.append(path)
            if not check:
                file.write_text(new, encoding="utf-8")
    print(f"Guide hreflang: {len(paths)} existing guides, {len(stale)} {'stale' if check else 'updated'}")
    return int(check and bool(stale))


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Check real public-deploy links, assets and search language annotations.

No network, metadata invention, index/noindex changes or external-link claims.
Run: python3 tools/discovery_integrity.py
"""
from __future__ import annotations

import re
import runpy
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://ekguru.shop"


def page_url(path: str) -> str:
    return SITE + "/" + (path[:-10] if path.endswith("index.html") else path)


class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.refs = []
        self.alternates = {}
        self.canonicals = []
        self.base = ""
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "base" and not self.base:
            self.base = attrs.get("href", "")
        if tag in {"a", "link", "img", "script", "source", "video", "audio", "iframe", "input"}:
            for key in ("href", "src", "poster"):
                if attrs.get(key):
                    self.refs.append((tag, key, attrs[key]))
        if tag == "link":
            rel = attrs.get("rel", "").lower().split()
            if "alternate" in rel and attrs.get("hreflang"):
                self.alternates[attrs["hreflang"].lower()] = attrs.get("href", "")
            if "canonical" in rel:
                self.canonicals.append(attrs.get("href", ""))


def prefix_relative_references(text: str, prefix: str = "../") -> str:
    """Relocate a root-page shell without touching script/style text or ../ links.

    HTMLParser gives exact offsets; only href/src/poster attribute values in
    actual start tags change. No DOM serialisation or author-copy rewriting.
    """
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    edits = []

    class Rewriter(HTMLParser):
        def handle_starttag(self, tag, attrs):
            raw = self.get_starttag_text()
            row, col = self.getpos()
            start = offsets[row - 1] + col
            for match in re.finditer(r'\b(?:href|src|poster)\s*=\s*([\"\'])(.*?)\1', raw, re.I | re.S):
                value = match.group(2)
                if not value or value.startswith(("/", "#", ".", "?")) or urlsplit(value).scheme:
                    continue
                edits.append((start + match.start(2), prefix))

        handle_startendtag = handle_starttag

    Rewriter(convert_charrefs=False).feed(text)
    for offset, value in reversed(edits):
        text = text[:offset] + value + text[offset:]
    return text


def public_target(url: str, public: set[str]) -> str | None:
    parsed = urlsplit(url)
    if parsed.netloc != "ekguru.shop" or parsed.scheme not in {"http", "https"}:
        return None
    path = unquote(parsed.path).lstrip("/")
    if not path or path.endswith("/"):
        path += "index.html"
    if path in public:
        return path
    if path + "/index.html" in public:
        return path + "/index.html"
    return ""


def audit(public: set[str], pages: dict[str, Page]) -> tuple[list[str], int]:
    errors = []
    checked = 0
    for source, page in sorted(pages.items()):
        base = urljoin(page_url(source), page.base)
        for tag, key, ref in page.refs:
            target = public_target(urljoin(base, ref), public)
            if target is None:
                continue
            checked += 1
            if not target:
                errors.append(f"{source}: missing public {tag}[{key}] target {ref}")
        for language, ref in page.alternates.items():
            url = urljoin(base, ref)
            target = public_target(url, public)
            if target not in pages:
                # A missing href is already a broken-reference error above.
                continue
            alternate = pages[target]
            if alternate.canonicals != [url]:
                errors.append(f"{source}: hreflang {language} target is not self-canonical: {url}")
            if page_url(source) not in alternate.alternates.values():
                errors.append(f"{source}: hreflang {language} has no return link: {url}")
    return errors, checked


def main() -> int:
    builder = runpy.run_path(str(ROOT / "tools/build-public-dist.py"))
    public = set(builder["iter_public"]())
    pages = {path: Page((ROOT / path).read_text(encoding="utf-8"))
             for path in sorted(public) if path.endswith(".html")}
    errors, checked = audit(public, pages)
    print(f"Discovery integrity: {len(pages)} public HTML files, {checked} internal references, {len(errors)} errors")
    for error in errors[:80]:
        print("  " + error)
    if errors:
        print("Error groups:", dict(Counter(error.split(": ", 1)[-1].split(":", 1)[0] for error in errors)))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())

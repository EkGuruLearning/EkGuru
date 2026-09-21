#!/usr/bin/env python3
"""Fail if local search exposes quarantined/noindex or stale pages."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def page_path(url: str) -> Path:
    clean = url.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return ROOT / "index.html"
    if clean.endswith(".html"):
        return ROOT / clean
    return ROOT / clean / "index.html"


def main() -> int:
    entries = json.loads((ROOT / "search-index.json").read_text(encoding="utf-8"))
    failures: list[str] = []
    counts = Counter(row.get("u") for row in entries)
    for url, count in counts.items():
        if count > 1:
            failures.append(f"duplicate search URL ({count}): {url}")
    for row in entries:
        url = row.get("u", "")
        path = page_path(url)
        if not path.is_file():
            failures.append(f"missing search target: {url}")
            continue
        head = path.read_text(encoding="utf-8", errors="replace").split("</head>", 1)[0]
        tags = re.findall(r"<meta\b[^>]*>", head, re.I)
        if any("robots" in tag.lower() and "noindex" in tag.lower() for tag in tags):
            failures.append(f"noindex search target: {url}")
    page = (ROOT / "search/index.html").read_text(encoding="utf-8")
    visible_counts = {int(value) for value in re.findall(r"(?:Type to search |Search )(\d+)(?: pages| Hindi lessons)", page)}
    if visible_counts != {len(entries)}:
        failures.append(f"search page count {sorted(visible_counts)} != index count {len(entries)}")
    if failures:
        print(f"FAIL search publication: {len(failures)} issue(s)")
        for failure in failures[:20]:
            print("  " + failure)
        return 1
    print(f"PASS search publication: {len(entries)} unique, existing, indexable targets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

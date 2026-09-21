#!/usr/bin/env python3
"""Remove repeated external script tags from public HTML pages.

A shared script is initialized once per document. Repeating the same `src` can
double-bind listeners, timers and network work even when the module happens to
have a guard. Attribute order does not matter. `--check` is read-only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "reports", "tools", "data", "research", "templates"}
SCRIPT = re.compile(r"[ \t]*<script\b([^>]*)>\s*</script>[ \t]*\n?", re.I)
SRC = re.compile(r"\bsrc\s*=\s*([\"'])(.*?)\1", re.I | re.S)


def pages() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.html")
                  if not any(part in SKIP or part.startswith(".") for part in p.relative_to(ROOT).parts[:-1]))


def desired(text: str) -> tuple[str, int]:
    seen: set[str] = set()
    removed = 0

    def keep_once(match: re.Match[str]) -> str:
        nonlocal removed
        source = SRC.search(match.group(1))
        if not source:
            return match.group(0)
        value = source.group(2).strip()
        if value not in seen:
            seen.add(value)
            return match.group(0)
        removed += 1
        return ""

    return SCRIPT.sub(keep_once, text), removed


def main() -> int:
    check = "--check" in sys.argv
    stale: list[tuple[str, int]] = []
    changed = removed = 0
    for path in pages():
        old = path.read_text(encoding="utf-8", errors="replace")
        new, count = desired(old)
        if not count:
            continue
        stale.append((path.relative_to(ROOT).as_posix(), count))
        removed += count
        if not check:
            path.write_text(new, encoding="utf-8")
            changed += 1
    if check and stale:
        print(f"STALE duplicate scripts: {removed} tag(s) on {len(stale)} page(s)")
        for path, count in stale[:12]:
            print(f"  {path}: {count}")
        return 1
    if check:
        print("ok    no page loads the same external script twice")
    else:
        print(f"script dedupe: removed {removed} duplicate tag(s) from {changed} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

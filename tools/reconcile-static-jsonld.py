#!/usr/bin/env python3
"""Remove unsupported biographical details from pre-rendered JSON-LD.

Runtime schema is maintained in js/seo.js. This tool keeps the static fallback
consistent without adding education, birthplace, credential, or job-title
claims that have not passed a separate evidence review.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = re.compile(
    r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.IGNORECASE | re.DOTALL,
)


def sanitize(value):
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    if not isinstance(value, dict):
        return value

    cleaned = {key: sanitize(item) for key, item in value.items()}
    founder = cleaned.get("founder")
    if isinstance(founder, dict) and founder.get("name") == "Prakash":
        cleaned["founder"] = {
            "@type": "Person",
            "name": "Prakash",
            "url": "https://ekguru.shop/about/",
        }
    if cleaned.get("@type") == "Person" and cleaned.get("name") == "Prakash":
        return {
            "@type": "Person",
            "@id": cleaned.get("@id", "https://ekguru.shop/#founder"),
            "name": "Prakash",
            "jobTitle": "Site operator, EkGuru",
            "url": "https://ekguru.shop/about/",
        }
    return cleaned


def reconcile(path: Path) -> bool:
    source = path.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        try:
            payload = json.loads(match.group(2))
        except json.JSONDecodeError:
            return match.group(0)
        updated = sanitize(payload)
        if updated == payload:
            return match.group(0)
        return match.group(1) + json.dumps(updated, ensure_ascii=False, separators=(",", ":")) + match.group(3)

    updated = SCRIPT.sub(replace, source)
    if updated == source:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*.html"):
        if any(part in {".git", "node_modules", ".venv"} for part in path.parts):
            continue
        changed += reconcile(path)
    print(f"reconciled static JSON-LD: {changed} files")


if __name__ == "__main__":
    main()

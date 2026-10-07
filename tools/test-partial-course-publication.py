#!/usr/bin/env python3
"""Check that partial Phase 1 courses do not present C1/C2 as published.

The course audit owns the content state; the rendered level page must make the
same boundary visible in its title and H1 and remain noindex. A1-B2 remain the
published path for every partial course.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/quality/course-publication-audit.json"


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def clean_text(fragment: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def main() -> int:
    try:
        report = json.loads(AUDIT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL cannot read course publication audit: {exc}")
        return 1

    errors: list[str] = []
    partial = [c for c in report.get("courses", [])
               if c.get("phase") == "phase-1"
               and c.get("quality_status") == "PUBLISHABLE_PARTIAL"]
    if not partial:
        fail("no partial Phase 1 courses found in the publication audit", errors)

    checked = 0
    for course in partial:
        code = course.get("code", "")
        levels = {row.get("level"): row for row in course.get("levels", [])}
        published = set(course.get("publishable_levels", []))
        if not {"A1", "A2", "B1", "B2"}.issubset(published):
            fail(f"{code}: partial course does not declare A1-B2 as published", errors)
        for level in ("A1", "A2", "B1", "B2"):
            row = levels.get(level, {})
            if row.get("state") != "PUBLISHABLE_EXISTING":
                fail(f"{code} {level}: expected PUBLISHABLE_EXISTING, got {row.get('state')}", errors)
            page = ROOT / "languages" / code / "level" / level.lower() / "index.html"
            if not page.is_file():
                fail(f"{code} {level}: published level page is missing", errors)

        for level in ("C1", "C2"):
            row = levels.get(level)
            if not row:
                fail(f"{code} {level}: state missing from publication audit", errors)
                continue
            page = ROOT / "languages" / code / "level" / level.lower() / "index.html"
            if row.get("state") in {"PUBLIC_CONTENT_BUG", "REVIEW_REQUIRED"}:
                if not page.is_file():
                    fail(f"{code} {level}: held page is missing instead of being clearly unpublished", errors)
                    continue
                raw = page.read_text(encoding="utf-8", errors="replace")
                title = re.search(r"<title\b[^>]*>(.*?)</title>", raw, re.I | re.S)
                h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", raw, re.I | re.S)
                robots = re.search(
                    r"<meta\b[^>]*\bname=[\"']robots[\"'][^>]*\bcontent=[\"']([^\"']+)",
                    raw, re.I,
                )
                title_text = clean_text(title.group(1)) if title else ""
                h1_text = clean_text(h1.group(1)) if h1 else ""
                if not re.search(r"not published|partial", title_text, re.I):
                    fail(f"{code} {level}: title does not clearly mark the level unpublished: {title_text!r}", errors)
                if not re.search(r"not published|partial", h1_text, re.I):
                    fail(f"{code} {level}: visible H1 does not clearly mark the level unpublished: {h1_text!r}", errors)
                if not robots or "noindex" not in robots.group(1).lower():
                    fail(f"{code} {level}: unpublished level is not noindex", errors)
            elif row.get("state") == "NOT_AUTHORED":
                if page.exists():
                    raw = page.read_text(encoding="utf-8", errors="replace")
                    title = re.search(r"<title\b[^>]*>(.*?)</title>", raw, re.I | re.S)
                    h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", raw, re.I | re.S)
                    text = " ".join(clean_text(m.group(1)) for m in (title, h1) if m)
                    if not re.search(r"not published|partial|not authored|coming soon", text, re.I):
                        fail(f"{code} {level}: unauthored level exists without a visible boundary", errors)
            # A1-B2 are the active path, so C1/C2 may be absent only when the
            # audit explicitly says no authored page exists. Any other state
            # is allowed only if its rendered publication is not being hidden.
            elif row.get("state") not in {"PUBLISHABLE_EXISTING", "NOT_AUTHORED"}:
                fail(f"{code} {level}: unexpected publication state {row.get('state')}", errors)
            checked += 1

    if errors:
        print(f"FAIL partial-course publication boundary ({len(errors)} issue(s)):")
        for error in errors:
            print(" - " + error)
        return 1
    print(f"PASS partial-course publication boundary: {len(partial)} partial Phase 1 courses; "
          f"A1-B2 published and {checked} C1/C2 pages clearly unpublished/partial.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

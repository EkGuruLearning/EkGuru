#!/usr/bin/env python3
"""Check the Spanish and French 1–20 lesson tables against course source data."""
from __future__ import annotations

import importlib.util
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))


class Tables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables: list[list[list[str]]] = []
        self.table: list[list[str]] | None = None
        self.row: list[str] | None = None
        self.cell: list[str] | None = None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.table = []
        elif tag == "tr" and self.table is not None:
            self.row = []
        elif tag in ("th", "td") and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("th", "td") and self.cell is not None and self.row is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None and self.table is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == "table" and self.table is not None:
            self.tables.append(self.table)
            self.table = None


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("numbers_course_" + path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load course data: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    errors: list[str] = []
    for code in ("es", "fr"):
        course = load_module(ROOT / f"tools/course-data/{code}.py")
        lesson = next((row for row in course.LESSONS if row["slug"] == "numbers-1-to-20"), None)
        page_path = ROOT / f"languages/{code}/lessons/numbers-1-to-20/index.html"
        if lesson is None or not page_path.exists():
            errors.append(f"{code}: source lesson or generated page is missing")
            continue

        headers, expected_rows = lesson["table"]
        expected = [[str(value) for value in row] for row in expected_rows]
        if [row[0] for row in expected] != [str(n) for n in range(1, 21)]:
            errors.append(f"{code}: course source table is not a complete 1–20 sequence")

        page = page_path.read_text(encoding="utf-8")
        parser = Tables()
        parser.feed(page)
        actual_table = next((table for table in parser.tables if table and table[0] == list(headers)), None)
        if actual_table is None:
            errors.append(f"{code}: rendered page has no {headers[0]} table")
        elif actual_table[1:] != expected:
            errors.append(f"{code}: rendered number table differs from source data")
        for header in headers:
            if page.count(f'data-h="{header}"') < 20:
                errors.append(f"{code}: responsive table label {header!r} is missing from one or more rows")
        if "Recall check" not in page:
            errors.append(f"{code}: page lacks the table-specific recall task")
        if "computer voice, not a native recording" not in page:
            errors.append(f"{code}: honest computer-voice limitation was lost")
        if "<!-- ekguru:shell-header:start -->" not in page or "<!-- ekguru:ultra-notice:start -->" not in page:
            errors.append(f"{code}: existing page shell or native-review notice was lost")

    if errors:
        print(f"FAIL world-course numbers content ({len(errors)} issue(s)):")
        for error in errors:
            print(" - " + error)
        return 1

    print("PASS Spanish and French 1–20 lesson tables: 20 source-matched rows each; page layers preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

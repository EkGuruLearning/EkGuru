#!/usr/bin/env python3
"""Repository-consistency checks for Daily Hindi Day 23.

These checks guard the page examples against the current in-repository course
example and keep the lesson structure intact. They do not establish Hindi
accuracy, naturalness, native-speaker approval, or external source verification.
"""
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "daily-hindi/day-23/index.html"
COURSE = ROOT / "data/courses/phase-2/hi_A2.json"
DESCRIPTION = (
    "Day 23 of a free 30-day Hindi course: four practice verbs, a worked "
    "example of gendered future forms, and a seven-sentence task."
)
FORMS = (
    ("I will eat", "मैं खाऊँगा।"),
    ("I will eat", "मैं खाऊँगी।"),
    ("He will eat", "वह खाएगा।"),
    ("She will eat", "वह खाएगी।"),
)


class LessonParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.future_table = False
        self.future_table_found = False
        self.rows: list[list[str]] = []
        self.data_h_rows: list[list[str | None]] = []
        self.row: list[str] | None = None
        self.row_data_h: list[str | None] | None = None
        self.cell: list[str] | None = None
        self.cell_data_h: str | None = None
        self.descriptions: list[str] = []
        self.jsonld: list[str] = []
        self.in_jsonld = False
        self.script_data: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "meta":
            is_description = (
                values.get("name") == "description"
                or values.get("name") == "twitter:description"
                or values.get("property") == "og:description"
            )
            if is_description and values.get("content") is not None:
                self.descriptions.append(values["content"] or "")
        elif tag == "script" and values.get("type") == "application/ld+json":
            self.in_jsonld = True
            self.script_data = []
        elif tag == "table" and values.get("aria-label") == "Four future forms of खाना":
            self.future_table = True
            self.future_table_found = True
        elif self.future_table and tag == "tr":
            self.row = []
            self.row_data_h = []
        elif self.future_table and tag in ("th", "td") and self.row is not None:
            self.cell = []
            self.cell_data_h = values.get("data-h") if tag == "td" else None

    def handle_data(self, data: str) -> None:
        if self.future_table and self.cell is not None:
            self.cell.append(data)
        if self.in_jsonld:
            self.script_data.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.future_table and tag in ("th", "td") and self.cell is not None:
            if self.row is not None:
                self.row.append(" ".join("".join(self.cell).split()))
            if tag == "td" and self.row_data_h is not None:
                self.row_data_h.append(self.cell_data_h)
            self.cell = None
            self.cell_data_h = None
        elif self.future_table and tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.data_h_rows.append(self.row_data_h or [])
            self.row = None
            self.row_data_h = None
        elif tag == "table" and self.future_table:
            self.future_table = False
        elif tag == "script" and self.in_jsonld:
            self.jsonld.append("".join(self.script_data))
            self.in_jsonld = False
            self.script_data = []


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL: " + message)


def future_lesson(course: dict) -> dict:
    matches = [
        lesson
        for unit in course["level"]["units"]
        for lesson in unit.get("lessons", [])
        if lesson.get("title") == "Future: खाऊँगा/खाएगा"
    ]
    require(len(matches) == 1, "expected exactly one repository A2 future lesson")
    return matches[0]


def main() -> int:
    html = PAGE.read_text(encoding="utf-8")
    parser = LessonParser()
    parser.feed(html)

    require(parser.future_table_found, "future-forms example table is missing")
    require(
        parser.rows
        and parser.rows[0] == ["English", "Hindi", "What the form matches"],
        "future-forms table headers changed",
    )
    expected_mobile_labels = ["English", "Hindi", "What the form matches"]
    require(
        parser.data_h_rows[1:] == [expected_mobile_labels] * len(FORMS),
        "every future-form table cell must carry its responsive column label",
    )
    for meaning, form in FORMS:
        require(
            any(
                len(row) >= 2 and row[0] == meaning and row[1].startswith(form)
                for row in parser.rows[1:]
            ),
            f"table is missing the {meaning!r} example {form!r}",
        )

    course = json.loads(COURSE.read_text(encoding="utf-8"))
    source_text = json.dumps(future_lesson(course), ensure_ascii=False)
    for _, form in FORMS:
        require(form.rstrip("।") in source_text, f"example {form!r} is not in the repository course source")

    require(len(parser.descriptions) == 3, "expected description, Open Graph, and Twitter metadata")
    require(all(value == DESCRIPTION for value in parser.descriptions), "page metadata descriptions disagree")
    schema_descriptions = []
    for script in parser.jsonld:
        data = json.loads(script)
        for item in data.get("@graph", []):
            if item.get("@type") == "LearningResource":
                schema_descriptions.append(item.get("description"))
    require(schema_descriptions == [DESCRIPTION], "LearningResource description is missing or inconsistent")

    for text in ("चलना", "मिलना", "रहना", "लेना"):
        require(text in html, f"today's practice verb {text!r} is missing")
    require("one future-tense sentence for each day" in html, "the seven-sentence task is missing")
    require("कल" in html and "verb tense and context" in html, "the कल ambiguity note is missing")
    require("This is a starter example, not a complete future-tense chart" in html,
            "the table's limited scope is not stated")
    require("The most regular of the three tenses" not in html, "the oversimplified rule remains")
    require("Nothing much. This one is genuinely easy" not in html, "the non-instructional mistake note remains")

    print("PASS: Day 23 examples match the repository A2 source and the page's lesson structure is intact.")
    print("NOTE: repository consistency only; this is not linguistic, native-speaker, or external verification.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

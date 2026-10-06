#!/usr/bin/env python3
"""Repository-consistency test for the Phase 5 Hindi numbers recall exercise.

This confirms that the exercise uses the same forms as EkGuru's local numbers
tool. It is not an independent Hindi-language or native-speaker review.
"""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "hindi/numbers/index.html"
NUMBER_TOOL = ROOT / "toolbox/hindi-numbers/index.html"
EXPECTED_SUMMARIES = [
    "Check the 29 pair",
    "Reveal the 39 pair",
    "Check the lakh value",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL: " + message)


def main() -> int:
    page = PAGE.read_text(encoding="utf-8")
    tool = NUMBER_TOOL.read_text(encoding="utf-8")

    match = re.search(r"\bvar N=(\[[\s\S]*?\]);", tool)
    require(match is not None, "could not find the Hindi numbers tool data")
    rows = json.loads(match.group(1))
    by_number = {row["n"]: row["hi"] for row in rows}
    expected = {20: "बीस", 29: "उनतीस", 30: "तीस", 39: "उनतालीस", 40: "चालीस"}
    for value, form in expected.items():
        require(by_number.get(value) == form,
                f"tool source changed for {value}: expected {form!r}, found {by_number.get(value)!r}")

    section_match = re.search(
        r'<section class="lv-drills" aria-label="Hindi numbers recall practice">'
        r"([\s\S]*?)</section>",
        page,
    )
    require(section_match is not None, "the page is missing its in-context recall practice")
    exercise = section_match.group(1)
    summaries = re.findall(r"<summary>(.*?)</summary>", exercise, flags=re.S)
    require(summaries == EXPECTED_SUMMARIES,
            "expected three clearly labelled HTML <details> answer reveals")

    for value, form in expected.items():
        require(f'<span lang="hi">{form}</span> ({value})' in exercise,
                f"the exercise does not show the tool's {value} form {form!r}")
    require("<span lang=\"hi\">चालीस</span> (40).</p>" in exercise,
            "the revealed 39-to-40 answer does not match the tool")
    require("<span lang=\"hi\">लाख</span> is 100,000, written 1,00,000." in exercise,
            "the lakh check is missing or differs from the visible lesson")
    require("A lakh (लाख) is 100,000" in tool,
            "the lakh value is not present in the repository number tool")
    require('href="../../toolbox/hindi-numbers/"' in exercise,
            "the exercise is not connected to the full numbers tool")
    require("उनतीस (29) rhymes with तीस (30)" in page
            and "उनतालीस (39) rhymes with चालीस (40)" in page,
            "the exercise no longer reinforces the lesson's own number pattern")
    require('rel="canonical"' in page and 'name="robots"' in page,
            "the page's canonical or indexing directive is missing")

    parser = HTMLParser(convert_charrefs=True)
    parser.feed(page)
    parser.close()

    print("PASS: the Hindi numbers recall exercise matches the repository number tool and page examples.")
    print("NOTE: repository consistency only; independent Hindi accuracy and native review remain pending.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

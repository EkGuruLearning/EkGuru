#!/usr/bin/env python3
"""Repository-consistency checks for the Hindi hunger answer and its route band.

The checks compare page copy with local learning data and exercise the band
selector. They do not verify Hindi independently or constitute native review.
"""
from __future__ import annotations

import importlib.util
import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "answers/how-to-say-i-am-hungry-in-hindi/index.html"
RELATED_PAGE = ROOT / "answers/how-to-say-i-am-learning-hindi/index.html"
COURSE = ROOT / "data/courses/phase-2/hi_A2.json"
WEATHER_COURSE = ROOT / "data/courses/phase-2/hi_B1.json"
PHRASEBOOK = ROOT / "toolbox/hindi-phrasebook/index.html"
DESCRIPTION = (
    "Learn मुझे भूख लगी है (“I am hungry”), compare Hindi expressions for thirst "
    "and cold, and see a specific restaurant request."
)


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.descriptions: dict[str, str] = {}
        self.jsonld: list[str] = []
        self.in_jsonld = False
        self.script_data: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "meta":
            key = values.get("name") or values.get("property")
            if key in ("description", "og:description", "twitter:description"):
                self.descriptions[key] = values.get("content") or ""
        elif tag == "script" and values.get("type") == "application/ld+json":
            self.in_jsonld = True
            self.script_data = []

    def handle_data(self, data: str) -> None:
        if self.in_jsonld:
            self.script_data.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self.in_jsonld:
            self.jsonld.append("".join(self.script_data))
            self.script_data = []
            self.in_jsonld = False


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL: " + message)


def restaurant_lesson(course: dict) -> dict:
    matches = [
        lesson
        for unit in course["level"]["units"]
        for lesson in unit.get("lessons", [])
        if lesson.get("id") == "A2-U3-L3"
    ]
    require(len(matches) == 1, "expected one repository Hindi A2 restaurant lesson")
    return matches[0]


def load_page_layer():
    path = ROOT / "tools/build-page-layer.py"
    spec = importlib.util.spec_from_file_location("phase4_page_layer", path)
    require(spec is not None and spec.loader is not None, "could not load the page-layer builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    html = PAGE.read_text(encoding="utf-8")
    for phrase in (
        "मुझे भूख लगी है",
        "मुझे प्यास लगी है",
        "मुझे ठंड लग रही है",
        "मुझे एक थाली दीजिए।",
    ):
        require(phrase in html, f"answer is missing {phrase!r}")
    require("मैं भूखा हूँ" not in html and "मैं भूखी हूँ" not in html,
            "unverified adjective-pattern alternatives were added")
    require("मुझे भूख लगी है</span> tells someone you are hungry; it is not itself an order." in html,
            "the answer does not distinguish stating hunger from ordering")
    require("खाना चाहिए" not in html, "the underspecified restaurant advice remains")
    require("sounds like a translation" not in html, "the unsupported blanket judgement remains")
    require('href="../../learn/hindi/"">' not in html, "the malformed course link remains")
    require('name="robots"' in html and 'rel="canonical"' in html,
            "indexing directives or canonical are missing")

    course = json.loads(COURSE.read_text(encoding="utf-8"))
    source = json.dumps(restaurant_lesson(course), ensure_ascii=False)
    require("मुझे एक थाली दीजिए" in source and "Please give me one plate" in source,
            "restaurant request is not present in the repository A2 lesson")
    phrasebook = PHRASEBOOK.read_text(encoding="utf-8")
    require("मुझे भूख लगी है" in phrasebook and "hunger has attached to me" in phrasebook,
            "the main phrase or its note is not present in the repository phrasebook")
    require("मुझे प्यास लगी है" in phrasebook and "मुझे ठंड लग रही है" in WEATHER_COURSE.read_text(encoding="utf-8"),
            "thirst or cold example is not present in its repository learning source")

    metadata = MetadataParser()
    metadata.feed(html)
    require(
        metadata.descriptions == {
            "description": DESCRIPTION,
            "og:description": DESCRIPTION,
            "twitter:description": DESCRIPTION,
        },
        "page summary metadata is missing or inconsistent",
    )
    answers = []
    for script in metadata.jsonld:
        data = json.loads(script)
        for item in data.get("@graph", []):
            if item.get("@type") == "QAPage":
                answers.append(item["mainEntity"]["acceptedAnswer"]["text"])
    require(len(answers) == 1 and "मुझे एक थाली दीजिए" in answers[0],
            "QAPage answer text is missing or inconsistent with the visible answer")

    page_layer = load_page_layer()
    routes = (
        "answers/how-to-say-i-am-hungry-in-hindi/index.html",
        "answers/how-to-say-i-am-learning-hindi/index.html",
        "ask/how-to-say-what-is-your-name-in-hindi/index.html",
        "ask/how-to-say-yes-and-no-in-hindi/index.html",
        "ask/is-duolingo-good-for-hindi/index.html",
        "ask/is-hindi-hard-to-learn/index.html",
        "ask/is-hindi-or-spanish-easier-to-learn/index.html",
        "ask/is-hindi-useful-to-learn/index.html",
        "ask/is-italki-or-preply-better-for-hindi/index.html",
        "ask/what-is-the-best-age-to-learn-hindi/index.html",
        "ask/what-is-the-hardest-part-of-hindi/index.html",
    )
    for route in routes:
        band = page_layer.band_for(route, {}, {})
        require(band is not None and "Learn Hindi properly" in band,
                f"{route} did not receive its Hindi next-step band")
        require("Amharic" not in band, f"{route} was misrouted to Amharic")
        rendered = (ROOT / route).read_text(encoding="utf-8")
        require("Learn Hindi properly" in rendered and "Learn Amharic properly" not in rendered,
                f"the rendered next-step band is wrong for {route}")

    print("PASS: hunger answer, restaurant phrase, metadata, and Hindi next-step routing match repository data.")
    print("NOTE: repository consistency only; Hindi accuracy and native-language review remain pending.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

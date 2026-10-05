#!/usr/bin/env python3
"""Check course-level voice controls and optional, source-supplied IPA output.

The course pages remain readable with JavaScript off. Each generated voice
control is hidden until js/voice.js mounts it, is click-triggered, and uses the
same-language entry in the BCP-47 voice registry. This test checks all levels
currently listed for publication, not just a sample page.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
spec = importlib.util.spec_from_file_location(
    "course_level_builder", ROOT / "tools/build-course-levels.py")
assert spec and spec.loader
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class VoiceMarkup(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.cells: list[str | None] = []
        self.buttons: list[dict[str, str | None]] = []
        self.current_button: int | None = None
        self.ipa_cells: list[str] = []
        self._in_ipa = False
        self._current_ipa: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag == "td":
            self.cells.append(a.get("data-h"))
            if a.get("data-h") == "IPA":
                self._in_ipa = True
                self._current_ipa = []
        if tag == "button" and "eg-voice" in (a.get("class") or "").split() \
                and a.get("data-voice-kind"):
            self.buttons.append({
                "cell": self.cells[-1] if self.cells else None,
                "kind": a.get("data-voice-kind"),
                "text": a.get("data-voice-text"),
                "lang": a.get("data-voice-lang"),
                "type": a.get("type"),
                "hidden": "hidden" if "hidden" in a else None,
                "aria-label": a.get("aria-label"),
                "aria-pressed": a.get("aria-pressed"),
                "button_text": "",
            })
            self.current_button = len(self.buttons) - 1

    def handle_data(self, data: str) -> None:
        if self._in_ipa:
            self._current_ipa.append(data)
        if self.current_button is not None:
            self.buttons[self.current_button]["button_text"] += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "button":
            self.current_button = None
        if tag == "td":
            if self._in_ipa:
                self.ipa_cells.append("".join(self._current_ipa))
                self._in_ipa = False
                self._current_ipa = []
            if self.cells:
                self.cells.pop()


def add_expected(counter: Counter, items: list, kind: str, cell: str | None,
                 code: str) -> None:
    for item in items:
        if not isinstance(item, dict):
            continue
        text = str(item.get("t") or "").strip()
        if text:
            counter[(kind, code, text, cell)] += 1


def expected_for(data: dict, code: str) -> Counter:
    expected: Counter = Counter()
    level = data.get("level") or {}
    for unit in level.get("units") or []:
        for lesson in unit.get("lessons") or []:
            add_expected(expected, lesson.get("vocab") or [], "vocabulary", "Word", code)
            add_expected(expected, (lesson.get("grammar") or {}).get("examples") or [],
                         "example", "Word", code)
            add_expected(expected, lesson.get("dialogue") or [], "dialogue", "Line", code)
    extra = level.get("extra") or {}
    add_expected(expected, extra.get("idioms") or [], "idiom", "Idiom", code)
    for kind, key in (("reading", "text"), ("listening", "script")):
        text = str((extra.get(kind) or {}).get(key) or "").strip()
        if text:
            expected[(kind, code, text, None)] += 1
    return expected


def parse(html: str) -> VoiceMarkup:
    parser = VoiceMarkup()
    parser.feed(html)
    parser.close()
    return parser


def main() -> int:
    errors: list[str] = []
    catalogue = json.loads((ROOT / "data/courses/index.json").read_text(encoding="utf-8"))
    registry_data = json.loads((ROOT / "data/languages/registry.json").read_text(encoding="utf-8"))
    registry = {row["code"]: row for row in registry_data.get("languages", [])}
    course_schema = json.loads((ROOT / "data/schemas/course-t1.schema.json").read_text(encoding="utf-8"))
    starter_schema = json.loads((ROOT / "data/schemas/starter-t2.schema.json").read_text(encoding="utf-8"))
    course_vocab = course_schema["$defs"]["lesson"]["properties"]["vocab"]["items"]
    starter_word = starter_schema["properties"]["words"]["items"]
    for label, schema in (("course T1", course_vocab), ("starter T2", starter_word)):
        if schema.get("dependentRequired", {}).get("ipa") != ["ipa_source"]:
            errors.append(f"{label} schema does not require a citation with supplied IPA")
        if "ipa_source" not in schema.get("properties", {}):
            errors.append(f"{label} schema has no IPA source-reference field")
    voice_js = (ROOT / "js/voice-languages.js").read_text(encoding="utf-8")
    match = re.search(r"window\.EKGURU_VOICE_LANGUAGES=(\{[^\n]*\});", voice_js)
    if not match:
        errors.append("js/voice-languages.js does not expose the generated voice map")
        voice_map = {}
    else:
        voice_map = json.loads(match.group(1))

    published_courses = 0
    published_levels = 0
    expected_total = 0
    for course in catalogue.get("courses", []):
        code = course.get("code", "")
        phase = course.get("phase") or "phase-1"
        levels = course.get("levels") or {}
        if not levels:
            continue
        published_courses += 1
        registry_row = registry.get(code) or {}
        speech_tag = registry_row.get("speech_tag")
        mapped = voice_map.get(code) or {}
        if not speech_tag or mapped.get("tag") != speech_tag:
            errors.append(f"{code}: no matching BCP-47 speech tag in the generated voice registry")

        for level in ("A1", "A2", "B1", "B2", "C1", "C2"):
            if level not in levels:
                continue
            published_levels += 1
            source_path = ROOT / "data/courses" / phase / f"{code}_{level}.json"
            page_path = ROOT / "languages" / code / "level" / level.lower() / "index.html"
            if not source_path.is_file():
                errors.append(f"{source_path.relative_to(ROOT)}: published course source is missing")
                continue
            if not page_path.is_file():
                errors.append(f"{page_path.relative_to(ROOT)}: published level page is missing")
                continue

            source = json.loads(source_path.read_text(encoding="utf-8"))
            page_html = page_path.read_text(encoding="utf-8")
            markup = parse(page_html)
            expected = expected_for(source, code)
            actual = Counter(
                (button["kind"], button["lang"], button["text"], button["cell"])
                for button in markup.buttons
            )
            expected_total += sum(expected.values())
            missing = expected - actual
            extra = actual - expected
            for (kind, lang, text, cell), count in missing.items():
                errors.append(
                    f"{page_path.relative_to(ROOT)}: {count} missing {kind} voice button(s) "
                    f"for {text[:55]!r} in {cell or 'reading/listening'}"
                )
            for (kind, lang, text, cell), count in extra.items():
                errors.append(
                    f"{page_path.relative_to(ROOT)}: {count} unexpected {kind} voice button(s) "
                    f"for {text[:55]!r} in {cell or 'reading/listening'}"
                )

            for button in markup.buttons:
                if button["lang"] != code:
                    errors.append(f"{page_path.relative_to(ROOT)}: voice button language is not {code}")
                if button["type"] != "button" or button["hidden"] is None:
                    errors.append(f"{page_path.relative_to(ROOT)}: voice button must be a hidden type=button before JS mounts")
                if button["aria-pressed"] != "false" or not button["aria-label"]:
                    errors.append(f"{page_path.relative_to(ROOT)}: voice button is missing its initial accessible state/name")
                if button["button_text"]:
                    errors.append(f"{page_path.relative_to(ROOT)}: server-rendered UI glyph leaks into authored course text")

            # If IPA is supplied later, the page must carry exactly that value
            # in the IPA lane. Empty data must not become guessed or placeholder
            # IPA, and the optional column should not be rendered without data.
            expected_ipa: Counter = Counter()
            for unit in (source.get("level") or {}).get("units") or []:
                for lesson in unit.get("lessons") or []:
                    table_sets = (
                        (lesson.get("vocab") or [], "vocabulary"),
                        ((lesson.get("grammar") or {}).get("examples") or [], "example"),
                    )
                    for items, voice_kind in table_sets:
                        for item in items:
                            if isinstance(item, dict) and isinstance(item.get("ipa"), str) \
                                    and item["ipa"].strip():
                                expected_ipa[item["ipa"].strip()] += 1
                        has_ipa = any(isinstance(item, dict) and
                                      isinstance(item.get("ipa"), str) and item["ipa"].strip()
                                      for item in items)
                        if not items:
                            continue
                        # Render the same table helper with real source rows to
                        # validate its optional IPA column without relying on a
                        # fake transcription in production data.
                        rendered = builder.vocab_table(items, code, course.get("name", code),
                                                       voice_kind)
                        if has_ipa and "<th>IPA</th>" not in rendered:
                            errors.append(f"{page_path.relative_to(ROOT)}: IPA data is not rendered")
                        if not has_ipa and "<th>IPA</th>" in rendered:
                            errors.append(f"{page_path.relative_to(ROOT)}: an empty IPA column is rendered")
                        if has_ipa:
                            for item in items:
                                if isinstance(item, dict) and isinstance(item.get("ipa"), str) and item["ipa"].strip():
                                    if builder.ipa_value(item) not in rendered:
                                        errors.append(f"{page_path.relative_to(ROOT)}: supplied IPA is missing from the generated table")
                    for item in lesson.get("dialogue") or []:
                        if isinstance(item, dict) and isinstance(item.get("ipa"), str) \
                                and item["ipa"].strip():
                            expected_ipa[item["ipa"].strip()] += 1
            actual_ipa = Counter(value.strip() for value in markup.ipa_cells if value.strip())
            if actual_ipa != expected_ipa:
                errors.append(f"{page_path.relative_to(ROOT)}: rendered IPA cells do not match the authored IPA data")

    # Exercise the optional renderer's escaping and exact-data behavior with a
    # synthetic fixture. The value is a test string, not a linguistic claim.
    fixture_target = 'नमस्ते "दोस्त"'
    fixture = builder.vocab_table([{
        "t": fixture_target,
        "r": "namaste dost",
        "ipa": "/nə.məs.teː/",
        "ipa_source": "test fixture only",
        "en": "hello friend",
    }], "hi", "Hindi")
    fixture_parse = parse(fixture)
    if '<th>IPA</th>' not in fixture or '/nə.məs.teː/' not in fixture:
        errors.append("optional source-supplied IPA does not render in its own table column")
    if len(fixture_parse.buttons) != 1 or fixture_parse.buttons[0]["text"] != fixture_target:
        errors.append("voice-control text is not safely escaped and recovered as authored")
    no_ipa = builder.vocab_table([{"t": "नमस्ते", "r": "namaste", "en": "hello"}], "hi", "Hindi")
    if "<th>IPA</th>" in no_ipa:
        errors.append("the generator invents or reserves an empty IPA column when the source has none")

    extra_fixture = builder.extra_block({
        "reading": {"text": "यह एक छोटा पाठ है।"},
        "listening": {"script": "नमस्ते।\nफिर मिलेंगे।", "voice_tag": "hi-IN"},
        "idioms": [{"t": "आँखों का तारा", "literal": "star of the eyes", "meaning": "a beloved person"}],
    }, "Hindi", "A1", "hi")
    extra_controls = parse(extra_fixture).buttons
    if Counter(button["kind"] for button in extra_controls) != Counter(
            {"reading": 1, "listening": 1, "idiom": 1}):
        errors.append("reading, listening and idiom voice controls are missing from the extra-section renderer")
    if 'lang="und"' in extra_fixture:
        errors.append("reading/listening text is not tagged with its course language")
    if "playback starts only after a click" not in extra_fixture:
        errors.append("listening copy does not state that playback is click-triggered")

    if errors:
        for error in errors[:50]:
            print("FAIL", error)
        if len(errors) > 50:
            print(f"… {len(errors) - 50} more")
        return 1
    print(
        f"PASS: voice controls cover {expected_total} authored vocabulary, example, dialogue, "
        f"idiom, reading and listening items across {published_levels} published levels "
        f"in {published_courses} languages; optional IPA rendering is data-only"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

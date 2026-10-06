#!/usr/bin/env python3
"""Add language-aware speaker markup to scoped Indian course and topic HTML.

The migration changes only target-script attribution, speaker-button semantics,
fingerprints, and its own marker. It never replaces authored wording or page
chrome. The generated builders are the source of truth for future fresh pages.
"""
from __future__ import annotations

import argparse
import html
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = {
    "bengali": "bn", "gujarati": "gu", "kannada": "kn",
    "malayalam": "ml", "marathi": "mr", "punjabi": "pa",
    "tamil": "ta", "telugu": "te", "urdu": "ur",
}
COURSE_MARKER = "<!-- ekguru:course-voice-controls:v1 -->"
TOPIC_MARKER = "<!-- ekguru:topic-voice-controls:v1 -->"
TOPIC_HUB_MARKER = "<!-- ekguru:topic-hub-voice-controls:v2 -->"
OLD_TOPIC_HUB_MARKER = "<!-- ekguru:topic-hub-voice-controls:v1 -->"


def load_builder(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


COURSE = load_builder("language_voice_course_builder", "build-language-course.py")
TOPICS = load_builder("language_voice_topic_builder", "build-lang-topics.py")


def get_attr(tag: str, name: str) -> str | None:
    match = re.search(r'''(?:^|\s)''' + re.escape(name) + r'''\s*=\s*(["'])(.*?)\1''', tag, re.I)
    return html.unescape(match.group(2)) if match else None


def set_attr(tag: str, name: str, value: str) -> str:
    pattern = re.compile(r'''(\s''' + re.escape(name) + r'''\s*=\s*)(["'])(.*?)\2''', re.I)
    escaped = html.escape(str(value), quote=True)
    if pattern.search(tag):
        return pattern.sub(lambda m: m.group(1) + m.group(2) + escaped + m.group(2), tag, count=1)
    return tag[:-1] + f' {name}="{escaped}">'


def update_fingerprint(page: str, attr: str, value: str) -> str:
    pattern = re.compile(r'''(\b''' + re.escape(attr) + r'''\s*=\s*)(["'])[^"']*\2''', re.I)
    return pattern.sub(lambda m: m.group(1) + m.group(2) + value + m.group(2), page, count=1)


def add_marker(page: str, marker: str) -> str:
    if marker in page:
        return page
    match = re.search(r"</body\s*>", page, re.I)
    if match:
        return page[:match.start()] + marker + "\n" + page[match.start():]
    return page + "\n" + marker + "\n"


def patch_storybook_chapter(page: str, code: str, language_name: str, *, topic: bool) -> str:
    """Tag the banner injected after builders have emitted their page marker."""
    pattern = re.compile(
        r'''(<div\b[^>]*\bclass\s*=\s*(["'])[^"']*\bsb-chapter\b[^"']*\2[^>]*>)'''
        r'''([\s\S]*?)(</div\s*>)''', re.I)

    def fix(match):
        opening, inside, closing = match.group(1), match.group(3), match.group(4)
        if "data-voice-lang=" in inside:
            return match.group(0)
        if topic:
            inside = TOPICS._speaker_controls_in_text_nodes(inside, code, language_name)
        else:
            inside = COURSE.add_course_speaker_controls(inside, code, language_name)
        return opening + inside + closing

    return pattern.sub(fix, page, count=1)


def tag_topic_phrase_cells(page: str, code: str) -> str:
    def fix(match):
        tag = match.group(0)
        if "bn" not in (get_attr(tag, "class") or "").split():
            return tag
        tag = set_attr(tag, "lang", code)
        return set_attr(tag, "dir", "auto")
    return re.sub(r"<td\b[^>]*>", fix, page, flags=re.I)


def update_topic_speaker_buttons(page: str, code: str, language_name: str) -> str:
    def fix(match):
        opening = "<button" + match.group("attrs") + ">"
        spoken = get_attr(opening, "data-sb-say")
        if spoken is None:
            return match.group(0)
        for attr, value in (("type", "button"), ("data-voice-lang", code),
                            ("aria-label", "Play %s in %s" % (spoken, language_name)),
                            ("aria-pressed", "false")):
            opening = set_attr(opening, attr, value)
        inside = match.group("inside")
        if html.unescape(re.sub(r"<[^>]*>", "", inside)).strip() == "🔊":
            inside = '<span aria-hidden="true">🔊</span>'
        return opening + inside + "</button>"
    return re.sub(r"<button\b(?P<attrs>[^>]*)>(?P<inside>[\s\S]*?)</button>", fix, page, flags=re.I)


def transform_course(path: Path, code: str, name: str) -> str:
    page = path.read_text(encoding="utf-8")
    if COURSE_MARKER in page:
        return patch_storybook_chapter(page, code, name, topic=False)
    page = COURSE.tag_language_cells(page, code, name)
    page = COURSE.add_course_speaker_controls(page, code, name)
    page = add_marker(page, COURSE_MARKER)
    return patch_storybook_chapter(page, code, name, topic=False)


def expected_fingerprint(config: dict, topic: dict | None = None) -> str | None:
    fingerprint = getattr(TOPICS, "content_fingerprint", None)
    return fingerprint(config, topic) if callable(fingerprint) else None


def transform_topic(path: Path, config: dict, topic: dict) -> str:
    code = config["code"]
    language_name = re.sub(r"^Learn\s+", "", config["title"])
    page = path.read_text(encoding="utf-8")
    expected = expected_fingerprint(config, topic)
    if TOPIC_MARKER in page:
        if expected:
            page = update_fingerprint(page, "data-topic-fingerprint", expected)
        return patch_storybook_chapter(page, code, language_name, topic=True)
    page = tag_topic_phrase_cells(page, code)
    page = update_topic_speaker_buttons(page, code, language_name)
    body_transform = getattr(TOPICS, "_speaker_controls_in_body", TOPICS._speaker_controls_in_text_nodes)
    page = body_transform(page, code, language_name, topic["slug"])
    if expected:
        page = update_fingerprint(page, "data-topic-fingerprint", expected)
    page = add_marker(page, TOPIC_MARKER)
    return patch_storybook_chapter(page, code, language_name, topic=True)


def transform_hub(path: Path, config: dict) -> str:
    page = path.read_text(encoding="utf-8")
    expected = expected_fingerprint(config)
    if TOPIC_HUB_MARKER in page:
        if expected:
            page = update_fingerprint(page, "data-topic-hub-fingerprint", expected)
        return patch_storybook_chapter(
            page, config["code"], re.sub(r"^Learn\s+", "", config["title"]), topic=True)
    page = page.replace(OLD_TOPIC_HUB_MARKER, "")
    language_name = re.sub(r"^Learn\s+", "", config["title"])
    body_transform = getattr(TOPICS, "_speaker_controls_in_body", TOPICS._speaker_controls_in_text_nodes)
    page = body_transform(page, config["code"], language_name)
    if expected:
        page = update_fingerprint(page, "data-topic-hub-fingerprint", expected)
    page = add_marker(page, TOPIC_HUB_MARKER)
    return patch_storybook_chapter(
        page, config["code"], re.sub(r"^Learn\s+", "", config["title"]), topic=True)


def process(path: Path, transform, check: bool) -> tuple[bool, str | None]:
    if not path.is_file():
        return False, f"missing scoped page: {path.relative_to(ROOT)}"
    before = path.read_text(encoding="utf-8")
    after = transform()
    if before == after:
        return False, None
    if check:
        return False, f"stale speaker/language markup: {path.relative_to(ROOT)}"
    path.write_text(after, encoding="utf-8")
    return True, None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report stale pages without writing")
    args = parser.parse_args()
    changed = 0
    errors: list[str] = []

    for slug, code in LANGUAGES.items():
        data_path = ROOT / "tools" / "lang-data" / (slug + ".json")
        if not data_path.is_file():
            errors.append(f"missing course data: {data_path.relative_to(ROOT)}")
            continue
        data = json.loads(data_path.read_text(encoding="utf-8"))
        name = data.get("name", slug.title())
        if data.get("voice_code") != code:
            errors.append(f"{data_path.relative_to(ROOT)}: voice_code must be {code}")
            continue
        for path in sorted((ROOT / "learn" / slug).rglob("index.html")):
            did_change, error = process(path, lambda p=path, c=code, n=name: transform_course(p, c, n), args.check)
            changed += did_change
            if error:
                errors.append(error)

    for data_path in sorted((ROOT / "data" / "topics").glob("*.json")):
        config = json.loads(data_path.read_text(encoding="utf-8"))
        code = data_path.stem
        if config.get("code") != code:
            errors.append(f"{data_path.relative_to(ROOT)}: code does not match its file name")
            continue
        hub = ROOT / config["dir"] / "index.html"
        did_change, error = process(hub, lambda p=hub, cfg=config: transform_hub(p, cfg), args.check)
        changed += did_change
        if error:
            errors.append(error)
        for topic in config.get("topics") or []:
            path = ROOT / config["dir"] / topic["slug"] / "index.html"
            did_change, error = process(path, lambda p=path, cfg=config, tp=topic: transform_topic(p, cfg, tp), args.check)
            changed += did_change
            if error:
                errors.append(error)

    for error in errors:
        print("ERROR:", error, file=sys.stderr)
    if errors:
        return 1
    print(("CHECK" if args.check else "UPDATED") +
          f": {changed} scoped language-course/topic page(s) changed; authored wording and page chrome retained.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

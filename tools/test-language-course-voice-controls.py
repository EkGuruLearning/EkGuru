#!/usr/bin/env python3
"""Structural speaker-control and target-script audit for Indian courses/topics.

No real browser keyboard, assistive technology, device voice, human review, or
pronunciation-quality claim is made by this source/HTML test.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import re
import shutil
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = {
    "bengali": "bn", "gujarati": "gu", "kannada": "kn",
    "malayalam": "ml", "marathi": "mr", "punjabi": "pa",
    "tamil": "ta", "telugu": "te", "urdu": "ur",
}
SCRIPT_RANGES = {
    "bn": r"\u0980-\u09FF", "gu": r"\u0A80-\u0AFF",
    "kn": r"\u0C80-\u0CFF", "ml": r"\u0D00-\u0D7F",
    "mr": r"\u0900-\u097F", "pa": r"\u0A00-\u0A7F",
    "ta": r"\u0B80-\u0BFF", "te": r"\u0C00-\u0C7F",
    "ur": r"\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF",
}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TextContent(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.stack: list[tuple[str, bool]] = []

    def handle_starttag(self, tag: str, attrs):
        values = dict(attrs)
        parent_hidden = any(hidden for _, hidden in self.stack)
        hidden = parent_hidden or tag in {"script", "style", "noscript"} or values.get("aria-hidden", "").lower() == "true"
        self.stack.append((tag, hidden))

    def handle_endtag(self, tag: str):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                self.stack = self.stack[:index]
                break

    def handle_data(self, data: str):
        if not any(hidden for _, hidden in self.stack):
            self.parts.append(data)

    def text(self) -> str:
        return " ".join("".join(self.parts).split())


class MarkupAudit(HTMLParser):
    def __init__(self, code: str):
        super().__init__(convert_charrefs=True)
        self.code = code
        self.script = re.compile("[" + SCRIPT_RANGES[code] + "]")
        self.stack: list[tuple[str, str | None, bool]] = []
        self.buttons: list[dict[str, str | None]] = []
        self.nested_voice_controls: list[str] = []
        self.unlabelled_target_text: list[tuple[str, str]] = []
        self.visible_text: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        values = dict(attrs)
        if tag == "button" and "data-sb-say" in values:
            self.buttons.append(values)
            if any(parent == "a" for parent, _, _ in self.stack):
                self.nested_voice_controls.append(values.get("data-sb-say", ""))
        if tag not in VOID:
            self.stack.append((tag, values.get("lang"), values.get("aria-hidden", "").lower() == "true"))

    def handle_startendtag(self, tag: str, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                self.stack = self.stack[:index]
                break

    def handle_data(self, data: str):
        if not any(tag == "body" for tag, _, _ in self.stack):
            return
        if any(tag in {"script", "style", "noscript"} or hidden
               for tag, _, hidden in self.stack):
            return
        self.visible_text.append(data)
        if not self.script.search(data):
            return
        langs = [lang for _, lang, _ in self.stack if lang]
        nearest = langs[-1] if langs else ""
        primary = nearest.lower().split("-", 1)[0]
        # Hindi-labelled cells/spans are intentionally excluded from Marathi coverage.
        if primary in {self.code, "hi"}:
            return
        self.unlabelled_target_text.append((nearest, data.strip()[:120]))


def audit_html(path: Path, code: str, allow_hindi_controls: bool = False) -> tuple[int, list[str]]:
    errors: list[str] = []
    parser = MarkupAudit(code)
    try:
        parser.feed(path.read_text(encoding="utf-8"))
        parser.close()
    except Exception as exc:
        return 0, [f"{path}: HTML parser failed: {exc}"]

    allowed = {code}
    if allow_hindi_controls:
        allowed.add("hi")
    for spoken in parser.nested_voice_controls:
        errors.append(f"{path}: speaker control for {spoken!r} is nested inside an anchor")
    visible = " ".join(" ".join(parser.visible_text).split())
    for button in parser.buttons:
        voice_lang = (button.get("data-voice-lang") or "").lower().split("-", 1)[0]
        if button.get("type") != "button":
            errors.append(f"{path}: speaker control lacks type=button")
        if voice_lang not in allowed:
            errors.append(f"{path}: unexpected speaker language {voice_lang!r}; expected {sorted(allowed)}")
        if not (button.get("aria-label") or "").strip():
            errors.append(f"{path}: speaker control has no accessible name")
        if button.get("aria-pressed") != "false":
            errors.append(f"{path}: speaker control must start aria-pressed=false")
        spoken = (button.get("data-sb-say") or "").strip()
        if not spoken:
            errors.append(f"{path}: speaker control has empty spoken text")
        elif spoken not in visible:
            errors.append(f"{path}: speaker text {spoken!r} is not visibly preserved")

    for lang, sample in parser.unlabelled_target_text:
        errors.append(f"{path}: target-script prose lacks lang={code} or lang=hi (nearest={lang!r}): {sample!r}")
    return len(parser.buttons), errors


def check_marathi_comparison(topic_builder, config: dict, errors: list[str], label: str):
    topics = config.get("topics") or []
    index = next((i for i, topic in enumerate(topics) if topic.get("slug") == "marathi-vs-hindi"), None)
    if index is None:
        errors.append(f"{label}: Marathi-vs-Hindi topic fixture is missing")
        return
    page = topic_builder.topic_page(
        config, topics[index], topics[index - 1] if index else None,
        topics[index + 1] if index + 1 < len(topics) else None, topics)
    parser = MarkupAudit("mr")
    parser.feed(page)
    parser.close()
    controls = [(button.get("data-sb-say"), button.get("data-voice-lang")) for button in parser.buttons]
    explicit_hindi = {"नमस्ते", "पानी", "खाना", "माँ", "पैसे", "मैं", "आप", "तुम",
                      "नहीं", "हाँ", "मुझे", "हिंदी", "नाम", "ल", "घर"}
    missing = sorted(text for text in explicit_hindi if (text, "hi") not in controls)
    if missing:
        errors.append(f"{label}: explicit Hindi examples/glosses lack Hindi controls: {', '.join(missing)}")
    unambiguous_hindi = explicit_hindi - {"पैसे", "घर"}  # shared words can legitimately have both tags
    misattributed = sorted(text for text in unambiguous_hindi if (text, "mr") in controls)
    if misattributed:
        errors.append(f"{label}: explicit Hindi examples received Marathi controls: {', '.join(misattributed)}")
    for shared in {"पैसे", "घर"}:
        if (shared, "mr") not in controls:
            errors.append(f"{label}: shared target word {shared!r} lacks its Marathi target control")
    for text in {"नमस्कार", "पाणी", "आई", "नाही", "मला", "मी", "तुम्ही", "ळ"}:
        if (text, "mr") not in controls:
            errors.append(f"{label}: Marathi target form {text!r} lacks a Marathi control")


def run_temporary_generators(errors: list[str]) -> tuple[int, int, int]:
    course_builder = load_module("course_voice_audit", ROOT / "tools/build-language-course.py")
    topic_builder = load_module("topic_voice_audit", ROOT / "tools/build-lang-topics.py")
    patcher = load_module("voice_markup_patcher_audit", ROOT / "tools/patch-language-voice-controls.py")
    course_pages = topic_pages = hub_pages = 0

    # Markup transformations must add language semantics without changing any
    # author-visible words (including explicit Hindi examples in Marathi text).
    course_fixture = ('<html><body><p>मराठी — Hindi: नमस्ते; Marathi: नाही &amp; पाणी.</p>'
                      '<table><tr><td data-h="Hindi">आप</td><td data-h="Marathi">मला</td></tr></table></body></html>')
    course_after = course_builder.language_markup(course_fixture, "Marathi")
    before_text, after_text = TextContent(), TextContent()
    before_text.feed(course_fixture); after_text.feed(course_after)
    if before_text.text() != after_text.text():
        errors.append("course language markup changed visible authored text in mixed Hindi/Marathi fixture")

    topic_fixture = ('<html><body><p>मराठी शब्द — मला ... against मुझे; हिंदी: नमस्ते.</p>'
                     '<table><tr><td class="bn">मराठी</td></tr></table></body></html>')
    topic_after = topic_builder._speaker_controls_in_text_nodes(
        topic_fixture, "mr", "Marathi", "marathi-vs-hindi")
    topic_after = topic_builder._speaker_controls_in_text_nodes(
        topic_after, "mr", "Marathi", "marathi-vs-hindi")
    before_text, after_text = TextContent(), TextContent()
    before_text.feed(topic_fixture); after_text.feed(topic_after)
    if before_text.text() != after_text.text():
        errors.append("topic speaker markup changed visible authored text in Marathi/Hindi fixture")
    elif topic_after.count("data-sb-say=") < 2:
        errors.append("topic mixed-language fixture did not add both Marathi and Hindi controls")

    injected_chapter = ('<html><body>' + patcher.COURSE_MARKER
                        + '<div class="sb-chapter"><span>Marathi <i>मराठी</i></span>'
                        + '<span class="sb-ch-floats" aria-hidden="true">अ आ इ</span></div>'
                        + '</body></html>')
    chapter_after = patcher.patch_storybook_chapter(
        injected_chapter, "mr", "Marathi", topic=False)
    chapter_twice = patcher.patch_storybook_chapter(
        chapter_after, "mr", "Marathi", topic=False)
    before_text, after_text = TextContent(), TextContent()
    before_text.feed(injected_chapter); after_text.feed(chapter_after)
    if before_text.text() != after_text.text():
        errors.append("injected chapter speaker markup changed visible authored wording")
    if chapter_after == injected_chapter or 'data-voice-lang="mr"' not in chapter_after:
        errors.append("post-storybook chapter banner did not receive a Marathi control")
    if chapter_twice != chapter_after:
        errors.append("post-storybook chapter transform is not idempotent")

    link_fixture = ('<html><body><p><a href="/bengali/">Learn '
                    '<span lang="bn" dir="auto">বাংলা</span>'
                    '<button type="button" data-sb-say="বাংলা" data-voice-lang="bn" '
                    'aria-label="Play বাংলা in Bengali" aria-pressed="false">'
                    '<span aria-hidden="true">🔊</span></button></a></p>'
                    '<script>const sample = "<a><button data-sb-say=\\\"keep\\\">";</script></body></html>')
    link_after = patcher.detach_voice_buttons_from_links(link_fixture)
    before_text, after_text = TextContent(), TextContent()
    before_text.feed(link_fixture); after_text.feed(link_after)
    if before_text.text() != after_text.text():
        errors.append("moving a speaker control out of a link changed visible authored text")
    if '</a><button type="button" data-sb-say="বাংলা"' not in link_after:
        errors.append("speaker control was not moved after the closing link")
    if '<script>const sample = "<a><button data-sb-say=\\\"keep\\\">";</script>' not in link_after:
        errors.append("link cleanup changed an inert script template")
    if patcher.detach_voice_buttons_from_links(link_after) != link_after:
        errors.append("link speaker cleanup is not idempotent")

    with tempfile.TemporaryDirectory(prefix="ekguru-voice-controls-") as tmp_name:
        temp = Path(tmp_name)
        (temp / "tools/lang-data").mkdir(parents=True)
        (temp / "js").mkdir()
        for source in (ROOT / "tools/lang-data").glob("*.json"):
            shutil.copy2(source, temp / "tools/lang-data" / source.name)
        registry = json.loads((ROOT / "data/languages/registry.json").read_text(encoding="utf-8"))
        registry_by_code = {row["code"]: row for row in registry["languages"]}
        voice_js = (ROOT / "js/voice-languages.js").read_text(encoding="utf-8")
        voice_match = re.search(r"window\.EKGURU_VOICE_LANGUAGES=(\{.*\});", voice_js)
        if not voice_match:
            errors.append("js/voice-languages.js: generated language map was not found")
            voice_map = {}
        else:
            voice_map = json.loads(voice_match.group(1))
        for slug, code in LANGUAGES.items():
            row = registry_by_code.get(code, {})
            voice = voice_map.get(code, {})
            if not row or voice.get("tag") != row.get("speech_tag"):
                errors.append(f"{slug}: voice tag does not match data/languages/registry.json")
        course_builder.ROOT = str(temp)
        course_builder._COURSE_VOICE_CODES = None
        with contextlib.redirect_stdout(io.StringIO()):
            for slug, code in LANGUAGES.items():
                data = json.loads((ROOT / "tools/lang-data" / f"{slug}.json").read_text(encoding="utf-8"))
                if data.get("voice_code") != code:
                    errors.append(f"tools/lang-data/{slug}.json: voice_code must be {code}")
                course_builder.build(slug)
                output = temp / "learn" / slug
                files = sorted(output.rglob("index.html"))
                course_pages += len(files)
                if not files:
                    errors.append(f"temporary course build for {slug} emitted no pages")
                for page in files:
                    _, page_errors = audit_html(page, code, allow_hindi_controls=(code == "mr"))
                    errors.extend(page_errors)
                required = {
                    "vocabulary": "vocabulary/index.html",
                    "dialogues": "practice/conversation/index.html",
                    "grammar/examples": "grammar/index.html",
                    "alphabet": "pronunciation/index.html",
                    "numbers": "numbers/index.html",
                }
                for category, rel in required.items():
                    page = output / rel
                    count, page_errors = audit_html(page, code, allow_hindi_controls=(code == "mr"))
                    errors.extend(page_errors)
                    if not page.is_file() or count < 1:
                        errors.append(f"temporary {slug} {category} page has no speaker control")

        for source in sorted((ROOT / "data/topics").glob("*.json")):
            config = json.loads(source.read_text(encoding="utf-8"))
            code = source.stem
            topics = config.get("topics") or []
            for index, topic in enumerate(topics):
                page = topic_builder.topic_page(
                    config, topic, topics[index - 1] if index else None,
                    topics[index + 1] if index + 1 < len(topics) else None, topics)
                fixture = temp / "topic.html"
                fixture.write_text(page, encoding="utf-8")
                count, page_errors = audit_html(fixture, code, allow_hindi_controls=(code == "mr"))
                errors.extend(page_errors)
                topic_pages += 1
                if count < 1:
                    errors.append(f"temporary topic {code}/{topic['slug']} has no speaker controls")
            hub = topic_builder.hub_page(config, topics, [])
            hub_fixture = temp / "hub.html"
            hub_fixture.write_text(hub, encoding="utf-8")
            count, hub_errors = audit_html(hub_fixture, code, allow_hindi_controls=(code == "mr"))
            errors.extend(hub_errors)
            hub_pages += 1
            if count < 1:
                errors.append(f"temporary topic hub {code} has no speaker controls")
            if code == "mr":
                check_marathi_comparison(topic_builder, config, errors, "temporary source")

        fixture = course_builder.language_markup('<p>Hindi: आप/तुम; Marathi: नाही</p>', "Marathi")
        langs = re.findall(r'data-voice-lang="([^"]+)"', fixture)
        if langs != ["hi", "hi", "mr"]:
            errors.append("course renderer did not keep explicit Hindi gloss runs separate from Marathi text")
    return course_pages, topic_pages, hub_pages


def main() -> int:
    errors: list[str] = []
    temp_courses, temp_topics, temp_hubs = run_temporary_generators(errors)
    disk_courses = disk_topics = disk_hubs = 0
    for slug, code in LANGUAGES.items():
        root = ROOT / "learn" / slug
        if not root.is_dir():
            errors.append(f"missing on-disk course directory learn/{slug}")
            continue
        for page in sorted(root.rglob("index.html")):
            _, page_errors = audit_html(page, code, allow_hindi_controls=(code == "mr"))
            errors.extend(page_errors)
            disk_courses += 1

    topic_builder = load_module("topic_voice_disk_audit", ROOT / "tools/build-lang-topics.py")
    for source in sorted((ROOT / "data/topics").glob("*.json")):
        config = json.loads(source.read_text(encoding="utf-8"))
        code = source.stem
        hub_page = ROOT / config["dir"] / "index.html"
        if not hub_page.is_file():
            errors.append(f"missing on-disk topic hub {hub_page.relative_to(ROOT)}")
        else:
            _, page_errors = audit_html(hub_page, code, allow_hindi_controls=(code == "mr"))
            errors.extend(page_errors)
            disk_hubs += 1
        for topic in config.get("topics") or []:
            page = ROOT / config["dir"] / topic["slug"] / "index.html"
            if not page.is_file():
                errors.append(f"missing on-disk topic page {page.relative_to(ROOT)}")
                continue
            _, page_errors = audit_html(page, code, allow_hindi_controls=(code == "mr"))
            errors.extend(page_errors)
            disk_topics += 1
        if code == "mr":
            check_marathi_comparison(topic_builder, config, errors, "on-disk source context")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: markup fixtures retain visible authored wording; explicit Hindi examples stay separate from Marathi controls.")
    print(f"PASS: temporary builders emitted labelled controls in {temp_courses} course pages, {temp_topics} topic pages, and {temp_hubs} topic hubs.")
    print(f"PASS: on-disk audit covered {disk_courses} course pages, {disk_topics} topic pages, and {disk_hubs} topic hubs; Hindi-labelled cells and lang=hi runs are excluded from Marathi counts.")
    print("LIMIT: source/HTML audit only. No native linguistic review, real browser keyboard or assistive-technology test, device voice availability, or audio-quality test was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

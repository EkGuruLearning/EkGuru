#!/usr/bin/env python3
"""Audit native, non-nested voice controls across all generated HTML pages.

This is a structural source/output check. It does not test a real browser,
keyboard, assistive technology, device voice inventory, or audio quality.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", ".arena", ".cache", ".venv", "node_modules", "build", "coverage", "dist", "out"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}
VOICE_DATA = {"data-sb-say", "data-voice-text", "data-say", "data-voice-kind"}


class VoiceMarkup(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.stack: list[tuple[str, dict[str, str | None]]] = []
        self.errors: list[str] = []
        self.controls = 0

    def handle_starttag(self, tag: str, attrs):
        values = dict(attrs)
        classes = set((values.get("class") or "").split())
        is_voice = bool(VOICE_DATA.intersection(values) or classes.intersection({"eg-voice", "spk"}))
        if is_voice:
            self.controls += 1
            label = f"{self.path}: voice control #{self.controls}"
            if tag.lower() != "button":
                self.errors.append(f"{label} is <{tag}>, not a native button")
            if any(parent == "a" and parent_attrs.get("href") is not None
                   for parent, parent_attrs in self.stack):
                self.errors.append(f"{label} is nested inside a link")
            if any(parent == "form" for parent, _ in self.stack) and values.get("type") != "button":
                self.errors.append(f"{label} inside a form must declare type=button")
            if values.get("aria-hidden", "").lower() == "true":
                self.errors.append(f"{label} is hidden from assistive technology")
        if tag.lower() not in VOID:
            self.stack.append((tag.lower(), values))

    def handle_startendtag(self, tag: str, attrs):
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str):
        tag = tag.lower()
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                self.stack = self.stack[:index]
                break


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDED for part in path.relative_to(ROOT).parts)


def main() -> int:
    html_files = [path for path in ROOT.rglob("*.html") if not should_skip(path)]
    errors: list[str] = []
    pages_with_controls = 0
    controls = 0
    for path in html_files:
        parser = VoiceMarkup(path.relative_to(ROOT))
        try:
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()
        except Exception as exc:  # malformed markup should be reported with its path
            errors.append(f"{path.relative_to(ROOT)}: HTML parse failed: {exc}")
            continue
        if parser.controls:
            pages_with_controls += 1
            controls += parser.controls
        errors.extend(parser.errors)

    if not controls:
        errors.append("no voice controls were found; page-wide audit must not pass vacuously")
    if errors:
        for error in errors[:50]:
            print("FAIL", error)
        if len(errors) > 50:
            print(f"… {len(errors) - 50} more structural issues")
        return 1

    print(f"PASS voice page coverage: {controls} native voice controls across "
          f"{pages_with_controls}/{len(html_files)} HTML pages; none nested in links; "
          "form controls explicitly use type=button")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

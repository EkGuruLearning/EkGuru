#!/usr/bin/env python3
"""Phase 7 structural regression: search-driven Hindi Q&A pages lead with an answer.

This verifies placement only. It does not judge linguistic accuracy, sourcing,
originality, usefulness, or whether a human/native-speaker review occurred.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path

ANSWER_CLASSES = {"answer", "ans"}
CHROME_CLASSES = {
    "eg-byline", "eg-voice-note", "sb-hint", "sb-voicenudge",
    "sb-chapter", "crumb", "crumbs",
}
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


class AnswerFirstPage(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, dict[str, str | None]]] = []
        self.main_depth = 0
        self.h1_count = 0
        self.h1_open = False
        self.after_h1 = False
        self.order = 0
        self.answer_order: int | None = None
        self.first_h2_order: int | None = None
        self.answer_text: list[str] = []
        self.preamble_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.order += 1
        attr = dict(attrs)
        in_main = self.main_depth > 0

        if tag == "main":
            self.main_depth += 1
        elif in_main and tag == "h1":
            self.h1_count += 1
            self.h1_open = True
        elif in_main and self.after_h1:
            if tag == "h2" and self.first_h2_order is None:
                self.first_h2_order = self.order
            classes = set((attr.get("class") or "").split())
            if tag == "div" and classes & ANSWER_CLASSES and self.answer_order is None:
                self.answer_order = self.order

        if tag not in VOID_TAGS:
            self.stack.append((tag, attr))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        self.order += 1
        if tag == "h1" and self.h1_open:
            self.h1_open = False
            self.after_h1 = True

        if tag == "main" and self.main_depth:
            self.main_depth -= 1

        stack_tags = [name for name, _ in self.stack]
        if tag in stack_tags:
            index = len(stack_tags) - 1 - stack_tags[::-1].index(tag)
            self.stack = self.stack[:index]

    def handle_data(self, data: str) -> None:
        if not data.strip():
            return
        if self.h1_open:
            return
        if not self.after_h1 or self.main_depth == 0:
            return
        if any(name in {"script", "style", "noscript", "template"} for name, _ in self.stack):
            return
        if any("hidden" in attrs for _, attrs in self.stack):
            return

        in_answer = any(
            name == "div" and set((attrs.get("class") or "").split()) & ANSWER_CLASSES
            for name, attrs in self.stack
        )
        if in_answer:
            self.answer_text.append(data.strip())
            return

        is_chrome = any(
            attrs.get("data-eg-chrome") is not None
            or set((attrs.get("class") or "").split()) & CHROME_CLASSES
            for _, attrs in self.stack
        )
        if self.answer_order is None and not is_chrome:
            self.preamble_text.append(data.strip())


def audit_page(path: Path) -> list[str]:
    parser = AnswerFirstPage()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        return [f"cannot read page: {error}"]

    errors: list[str] = []
    if parser.h1_count != 1:
        errors.append(f"expected one main H1, found {parser.h1_count}")
    if parser.answer_order is None:
        errors.append("no text-bearing .answer/.ans block after the H1")
        return errors
    if parser.first_h2_order is not None and parser.first_h2_order < parser.answer_order:
        errors.append("a section heading appears before the direct answer")
    if len(" ".join(parser.answer_text)) < 20:
        errors.append("the direct-answer block has too little visible text")
    preamble = " ".join(parser.preamble_text)
    if len(preamble.split()) > 20:
        errors.append(f"{len(preamble.split())} non-chrome words appear before the direct answer")
    return errors


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                     help="site root to inspect (defaults to the repository root)")
    args = cli.parse_args()
    root = args.root.resolve()

    pages: list[tuple[str, Path]] = []
    for section in ("ask", "answers"):
        section_root = root / section
        if not section_root.is_dir():
            continue
        pages.extend(
            (section, page)
            for page in sorted(section_root.rglob("index.html"))
            if page != section_root / "index.html"
        )

    failures: list[str] = []
    counts = {"ask": 0, "answers": 0}
    for section, page in pages:
        counts[section] += 1
        for error in audit_page(page):
            failures.append(f"{page.relative_to(root).as_posix()}: {error}")

    if not pages:
        print("FAIL  answer-first audit found no Q&A detail pages")
        return 1
    if failures:
        print(f"FAIL  answer-first placement: {len(failures)} issue(s) across {len(pages)} detail pages")
        for failure in failures:
            print("  ", failure)
        return 1

    print(
        "PASS  answer-first placement: "
        f"{len(pages)} detail pages ({counts['ask']} ask, {counts['answers']} answers); "
        "a concise answer block precedes section headings."
    )
    print("NOTE  structural check only; factual, native-speaker and editorial reviews are separate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

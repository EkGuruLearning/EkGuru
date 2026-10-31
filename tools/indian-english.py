#!/usr/bin/env python3
"""EkGuru: keep the English copy in Indian English.

    python3 tools/indian-english.py --check     exit 1 if an American form is found
    python3 tools/indian-english.py --apply     fix them in place
    python3 tools/indian-english.py --report    print counts only, change nothing

The word list lives in tools/lib/en_in.py and is deliberately small: only forms
that are wrong in Indian English and cannot be a correct word in a language the
site teaches. Read that file's header before adding to it.

What is scanned
---------------
1. English HTML pages (<html lang="en...">), outside the translated trees
   (es, fr, de, pt, ja, ar). In each page:
     * visible text, including <title>;
     * the human-facing attributes: title, alt, aria-label, placeholder, and
       the content of <meta> tags;
     * the prose values of JSON-LD (<script type="application/ld+json">).
   Never touched: scripts, styles, comments, URLs, ids, classes, data-*.

2. The sources those pages are built from, so the next rebuild cannot bring the
   American forms back:
     * data/courses, data/topics, data/learning, data/flashcards, data/global
       and data/lang-en.json: prose string VALUES only. Keys, identifiers and
       slugs (a value with no space in it) are never changed;
     * the English block of js/i18n.js (lines between `en: {` and `es: {`).

Why a tool and not a find-and-replace
-------------------------------------
A plain replace would also have changed "colors" in a CSS array, the schema.org
type "Organization", and Portuguese or Spanish example sentences. This tool
changes prose only, and --check keeps it that way.
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools", "lib"))
import en_in  # noqa: E402

TRANSLATED_DIRS = {"es", "fr", "de", "pt", "ja", "ar"}
SKIP_DIRS = {"node_modules", ".git", "reports", "docs", "tools", "apps-script",
             ".github", "csv", "live-sheets", "data", "js", "css", "images"}

# Data trees that feed learner-facing English. Internal reports and audits are
# deliberately not here: they are not shown to learners.
DATA_SOURCES = ["data/courses", "data/topics", "data/learning",
                "data/flashcards", "data/global"]
DATA_FILES = ["data/lang-en.json"]

TOKEN = re.compile(r"(<!--.*?-->|<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<[^>]+>)",
                   re.S | re.I)
HUMAN_ATTR = re.compile(
    r"""(\b(?:title|alt|aria-label|aria-description|placeholder|content)\s*=\s*)("([^"]*)"|'([^']*)')""",
    re.I)
LDJSON = re.compile(r'^<script\b[^>]*type\s*=\s*["\']application/ld\+json["\'][^>]*>', re.I)
LANG_EN = re.compile(r'<html[^>]*\blang\s*=\s*["\']en', re.I)


def _convert_attrs(tag: str) -> str:
    def repl(m: "re.Match[str]") -> str:
        quoted = m.group(2)
        quote, inner = quoted[0], quoted[1:-1]
        new = en_in.convert(inner)
        return m.group(1) + quote + new + quote
    return HUMAN_ATTR.sub(repl, tag)


def convert_html(raw: str) -> tuple[str, int]:
    """Return (converted_html, replacements). Bytes outside prose are untouched."""
    count = 0
    out: list[str] = []
    for i, part in enumerate(TOKEN.split(raw)):
        if i % 2 == 0:                       # text between tags
            new, k = en_in.WORD_RE.subn(en_in._sub, part)
            count += k
            out.append(new)
            continue
        if part.startswith("<!--") or part[:7].lower() == "<style":
            out.append(part)
            continue
        if part[:7].lower() == "<script":
            m = LDJSON.match(part)
            if m:
                head_end = m.end()
                close = part.lower().rfind("</script>")
                body = part[head_end:close]
                new_body, k = en_in.convert_json_text(body)
                count += k
                out.append(part[:head_end] + new_body + part[close:])
            else:
                out.append(part)
            continue
        new_tag = _convert_attrs(part)
        if new_tag != part:
            count += len(en_in.find(part)) if False else sum(
                len(en_in.find(m.group(2)[1:-1])) for m in HUMAN_ATTR.finditer(part))
        out.append(new_tag)
    return "".join(out), count


def find_in_html(raw: str) -> list[str]:
    """US forms that would be changed, for --check and --report."""
    _, _n = convert_html(raw)
    hits: list[str] = []
    for i, part in enumerate(TOKEN.split(raw)):
        if i % 2 == 0:
            hits += en_in.find(part)
        elif part[:7].lower() == "<script":
            m = LDJSON.match(part)
            if m:
                close = part.lower().rfind("</script>")
                body = part[m.end():close]
                new_body, _k = en_in.convert_json_text(body)
                if new_body != body:
                    hits += en_in.find(body)
        elif not part.startswith("<!--") and part[:7].lower() != "<style":
            for a in HUMAN_ATTR.finditer(part):
                hits += en_in.find(a.group(2)[1:-1])
    return hits


def english_pages():
    for d, dirs, files in os.walk(ROOT):
        rel = os.path.relpath(d, ROOT)
        if rel == ".":
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS and x not in TRANSLATED_DIRS
                       and not x.startswith(".")]
        else:
            dirs[:] = [x for x in dirs if not x.startswith(".")]
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(d, f)


def data_files():
    for base in DATA_SOURCES:
        for d, _dirs, files in os.walk(os.path.join(ROOT, base)):
            for f in files:
                if f.endswith(".json"):
                    yield os.path.join(d, f)
    for f in DATA_FILES:
        p = os.path.join(ROOT, f)
        if os.path.exists(p):
            yield p


def i18n_english_block(raw: str) -> tuple[int, int] | None:
    start = re.search(r"^  en: \{\s*$", raw, re.M)
    end = re.search(r"^  es: \{\s*$", raw, re.M)
    if not start or not end or end.start() <= start.start():
        return None
    return start.end(), end.start()


def main(argv: list[str]) -> int:
    apply_ = "--apply" in argv
    check = "--check" in argv
    report = "--report" in argv or not (apply_ or check)
    total = {"html": 0, "data": 0, "i18n": 0}
    dirty: list[str] = []
    words: dict[str, int] = {}

    def note(path: str, hits: list[str]) -> None:
        dirty.append(os.path.relpath(path, ROOT))
        for h in hits:
            words[h] = words.get(h, 0) + 1

    # 1. English HTML
    for p in english_pages():
        try:
            raw = open(p, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError):
            continue
        if not LANG_EN.search(raw[:4000]):
            continue
        hits = find_in_html(raw)
        if not hits:
            continue
        total["html"] += len(hits)
        note(p, hits)
        if apply_:
            new, _ = convert_html(raw)
            if new != raw:
                open(p, "w", encoding="utf-8", newline="").write(new)

    # 2a. data
    for p in data_files():
        try:
            raw = open(p, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError):
            continue
        new, k = en_in.convert_json_text(raw)
        if not k:
            continue
        total["data"] += k
        note(p, en_in.find(raw))
        if apply_:
            open(p, "w", encoding="utf-8", newline="").write(new)

    # 2b. js/i18n.js, English block only
    p = os.path.join(ROOT, "js", "i18n.js")
    raw = open(p, encoding="utf-8").read()
    span = i18n_english_block(raw)
    if span:
        a, b = span
        block = raw[a:b]
        new_block, k = en_in.convert_json_text(block)
        if k:
            total["i18n"] += k
            note(p, en_in.find(block))
            if apply_:
                open(p, "w", encoding="utf-8", newline="").write(raw[:a] + new_block + raw[b:])
    else:
        print("indian-english: could not find the English block of js/i18n.js", file=sys.stderr)
        return 2

    n = sum(total.values())
    label = "fixed" if apply_ else "found"
    print("indian-english: %s %d American form(s): %d in HTML, %d in data, %d in js/i18n.js "
          "(%d files)" % (label, n, total["html"], total["data"], total["i18n"], len(set(dirty))))
    if report or n:
        for w, c in sorted(words.items(), key=lambda kv: -kv[1])[:25]:
            print("  %5d  %s -> %s" % (c, w, en_in.LEXICON[w]))
    if check and n:
        for f in sorted(set(dirty))[:15]:
            print("  e.g. " + f)
        print("Run: python3 tools/indian-english.py --apply")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

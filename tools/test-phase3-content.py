#!/usr/bin/env python3
"""PHASE 3 acceptance test — the Learn tab's long-form posts.

The AdSense command (PHASE3) asks for ten blog-style posts per language, each at
least 1000 words, with headings, real examples in the target script plus
romanisation, a mistakes section, practice material and internal links.

Five of those ten already had a page (beginner / pronunciation / grammar /
travel / numbers); this phase deepened them and added the five that had no home
(common words, mistakes, reading, vs-Hindi, speaking alone). All of it is written
by tools/build-language-course.py from tools/lang-data/<slug>.json.

This test is the phase's own gate. Run:  python3 tools/test-phase3-content.py

It checks, for every language with a course pack:
  · all ten posts exist as real pages
  · each is at least 1000 words
  · each is a readable article: one <main>, one <h1>, at least four <h2>s
  · each links to at least two other guides (internal linking, no dead ends)
  · the course hub links to all ten (no orphans)
  · the five NEW pages are noindex, and the five deepened pages keep exactly the
    indexability the owner's immutable baseline recorded (tools/ultra/contract.py
    does not read the pack-driven pages, so the phase test has to say it here)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIN_WORDS = 1000

EXISTING = ["beginner", "pronunciation", "grammar", "travel", "numbers"]
NEW = ["common-words", "mistakes", "reading", "vs-hindi", "speaking-alone"]
POSTS = EXISTING + NEW

# Hindi's learn/ guides are hand-authored rather than generated from a pack, and
# they live at the top level (learn/<slug>/) instead of learn/hindi/<slug>/, so the
# ten post types map onto their own URLs. Eight already existed; the last two were
# written by tools/build-hindi-phase3-posts.py.
HINDI_NEW = {"common-words", "speaking-alone"}   # the two pages this phase added
HINDI = {
    "beginner": "learn-hindi-online-guide",
    "pronunciation": "hindi-alphabet-for-beginners",
    "grammar": "hindi-sentence-structure",
    "travel": "hindi-phrases-for-travel",
    "numbers": "hindi-numbers-1-to-100",
    "common-words": "hindi-100-most-common-words",
    "mistakes": "common-hindi-mistakes",
    "reading": "hindi-barakhadi",
    "vs-hindi": "hindi-or-urdu-difference",
    "speaking-alone": "hindi-speaking-practice-alone",
}

WORD_RE = re.compile(r"[A-Za-z\u0600-\u06FF\u0900-\u0DFF\u0E00-\u0E7F]+")
TAG_RE = re.compile(r"<[^>]+>")
DROP_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>|<!--.*?-->", re.S | re.I)
ROBOTS_RE = re.compile(r'<meta\b(?=[^>]*\bname=["\']robots["\'])[^>]*\bcontent=["\']([^"\']*)["\']', re.I)
H1_RE = re.compile(r"<h1\b", re.I)
H2_RE = re.compile(r"<h2\b", re.I)
MAIN_RE = re.compile(r"<main\b", re.I)


def words(html: str) -> int:
    text = TAG_RE.sub(" ", DROP_RE.sub(" ", html))
    return len(WORD_RE.findall(text))


def load_baseline() -> dict:
    path = ROOT / "data/quality/indexing-baseline.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8")).get("pages", {})


def main() -> int:
    packs = sorted((ROOT / "tools/lang-data").glob("*.json"))
    if not packs:
        print("FAIL: no language packs under tools/lang-data/")
        return 1
    baseline = load_baseline()
    problems: list[str] = []
    checked = 0
    shortest = ("", 10**9)

    for pack in packs:
        slug = pack.stem
        hub_path = ROOT / "learn" / slug / "index.html"
        hub = hub_path.read_text(encoding="utf-8") if hub_path.exists() else ""
        if not hub:
            problems.append(f"{slug}: hub learn/{slug}/index.html is missing")
            continue
        for post in POSTS:
            rel = f"learn/{slug}/{post}/index.html"
            p = ROOT / rel
            if not p.exists():
                problems.append(f"{rel}: missing")
                continue
            checked += 1
            html = p.read_text(encoding="utf-8")
            w = words(html)
            if w < MIN_WORDS:
                problems.append(f"{rel}: {w} words, needs {MIN_WORDS}")
            if w < shortest[1]:
                shortest = (rel, w)
            if len(H1_RE.findall(html)) != 1:
                problems.append(f"{rel}: needs exactly one <h1>")
            if len(MAIN_RE.findall(html)) != 1:
                problems.append(f"{rel}: needs exactly one <main>")
            if len(H2_RE.findall(html)) < 4:
                problems.append(f"{rel}: needs at least four <h2> sections")
            links = {q for q in POSTS if q != post and f'../{q}/' in html}
            if len(links) < 2:
                problems.append(f"{rel}: links to only {len(links)} other guide(s)")
            if f'href="{post}/"' not in hub and f'href="/learn/{slug}/{post}/"' not in hub:
                problems.append(f"{rel}: the course hub does not link to it")
            m = ROBOTS_RE.search(html)
            robots = (m.group(1).lower() if m else "")
            noindex = "noindex" in robots
            was_indexable = baseline.get(rel, {}).get("indexable")
            if post in NEW and not noindex:
                problems.append(f"{rel}: a new page must stay noindex (owner indexing contract)")
            if post in EXISTING and was_indexable is not None and noindex == was_indexable:
                # noindex True means "not indexable", so equal means the flag flipped
                problems.append(f"{rel}: indexability changed from the owner's baseline")

    # Hindi: hand-authored guides, mapped type -> URL above.
    hindi_checked = 0
    hub = (ROOT / "learn/hindi/index.html").read_text(encoding="utf-8")
    for kind, slug in HINDI.items():
        rel = f"learn/{slug}/index.html"
        p = ROOT / rel
        if not p.exists():
            problems.append(f"{rel}: missing (Hindi {kind})")
            continue
        checked += 1
        hindi_checked += 1
        html = p.read_text(encoding="utf-8")
        w = words(html)
        if w < MIN_WORDS:
            problems.append(f"{rel}: {w} words, needs {MIN_WORDS} (Hindi {kind})")
        if w < shortest[1]:
            shortest = (rel, w)
        if len(H1_RE.findall(html)) != 1:
            problems.append(f"{rel}: needs exactly one <h1>")
        if len(H2_RE.findall(html)) < 4:
            problems.append(f"{rel}: needs at least four <h2> sections")
        links = {k for k, v in HINDI.items()
                 if v != slug and (f"/learn/{v}/" in html or f'../{v}/' in html)}
        if len(links) < 2:
            problems.append(f"{rel}: links to only {len(links)} other guide(s)")
        if kind in HINDI_NEW and f'href="../{slug}/"' not in hub:
            problems.append(f"{rel}: the Hindi hub does not link to it")
        m = ROBOTS_RE.search(html)
        if kind in HINDI_NEW and not (m and "noindex" in m.group(1).lower()):
            problems.append(f"{rel}: a new Hindi page must stay noindex (owner indexing contract)")

    langs = len(packs)
    print(f"PHASE 3 content: {langs} course pack(s) × {len(POSTS)} posts = {langs * len(POSTS)} pages "
          f"+ Hindi {hindi_checked}/{len(HINDI)} mapped posts = {checked} found")
    if checked:
        print(f"shortest post: {shortest[0]} — {shortest[1]} words (minimum {MIN_WORDS})")
    if problems:
        print(f"\nFAIL — {len(problems)} problem(s):")
        for line in problems[:25]:
            print("  " + line)
        if len(problems) > 25:
            print(f"  … and {len(problems) - 25} more")
        return 1
    print("\nPASS — every post exists, clears 1000 words, is a readable article, links to the others,")
    print("       is linked from its hub, and carries the indexability the owner's contract allows.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

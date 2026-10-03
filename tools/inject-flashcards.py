#!/usr/bin/env python3
"""Inject the PHASE 9 flashcard lab into every practice page that has a deck.

WHY AN INJECTOR AND NOT A GENERATOR REWRITE
-------------------------------------------
The practice pages are written by two different generators (build-world-course.py
for the ten world courses, build-language-course.py for the ten Indian ones),
and every page on disk has since been post-processed by the shell, the recovery
blocks, the consent block, apply-ultra decoration and inject-ads. Rewriting a
page from its generator would drop all of that — tried once: a 120/179-line
"diff" that was mostly deleted decoration. So the lab is added the way the rest
of this repo adds site-wide blocks: one idempotent pass, one marker pair, the
generator that owns it in tools/ and CI.

The block is byte-stable: run twice, get the same page. `--check` exits 1 when
any practice page with a deck is missing or carrying a stale block.

Scope: languages/<code>/practice/index.html and learn/<slug>/practice/index.html
for the languages that have data/flashcards/<code>.json. A language without a
deck is skipped, never given a link that cannot open.

Run:  python3 tools/inject-flashcards.py [--check]
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

from lib.flashcard_section import flashcard_section, mount_script  # noqa: E402

START = "<!-- ekguru:flashcards:start -->"
END = "<!-- ekguru:flashcards:end -->"
ANCHOR = "<!-- ekguru:trust-footer:start -->"
ANCHOR_FALLBACK = "</main>"

INDIAN = {"hindi": "hi", "bengali": "bn", "gujarati": "gu", "kannada": "kn",
          "malayalam": "ml", "marathi": "mr", "punjabi": "pa", "tamil": "ta",
          "telugu": "te", "urdu": "ur"}


def deck_exists(code):
    return os.path.exists("data/flashcards/%s.json" % code)


def names(code):
    """Human name + speech tag for the mount call, straight from the deck."""
    import json
    with open("data/flashcards/%s.json" % code, encoding="utf-8") as f:
        d = json.load(f)
    return d.get("name") or code, d.get("speech") or code


def page_targets():
    """(path, code) for every practice page that should carry a lab."""
    out = []
    for path in sorted(glob.glob("languages/*/practice/index.html")):
        code = path.split("/")[1]
        if deck_exists(code):
            out.append((path, code))
    for path in sorted(glob.glob("learn/*/practice/index.html")):
        slug = path.split("/")[1]
        code = INDIAN.get(slug)
        if code and deck_exists(code):
            out.append((path, code))
    return out


def block_for(code):
    name, speech = names(code)
    html, scripts = flashcard_section(code, name)
    if not html:
        return None
    tags = "".join('<script src="/js/%s" defer></script>\n' % s for s in scripts)
    return "%s\n%s%s%s\n%s\n" % (START, tags, html, mount_script(code, name, speech), END)


def insert(raw, want):
    """Insert the block immediately before the last trust-footer marker (the
    body copy), never inside a decorative earlier block. `want` already ends
    in one newline, so block + anchor round-trips byte-for-byte."""
    anchor = ANCHOR if ANCHOR in raw else ANCHOR_FALLBACK
    if anchor == ANCHOR:
        head, _, tail = raw.rpartition(ANCHOR)
        return head + want + ANCHOR + tail
    return raw.replace(anchor, want + anchor, 1)


def strip_block(raw):
    pat = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)
    return pat.sub("", raw)


def main():
    check = "--check" in sys.argv
    targets = page_targets()
    missing, stale, written = [], [], 0
    for path, code in targets:
        raw = open(path, encoding="utf-8").read()
        want = block_for(code)
        if want is None:
            continue
        has = START in raw
        if not has:
            if check:
                missing.append(path)
                continue
            new = insert(raw, want)
            open(path, "w", encoding="utf-8").write(new)
            written += 1
            continue
        rebuilt = insert(strip_block(raw), want)
        if rebuilt != raw:
            if check:
                stale.append(path)
            else:
                open(path, "w", encoding="utf-8").write(rebuilt)
                written += 1

    if check and (missing or stale):
        print("STALE flashcards: %d page(s) missing, %d stale — run tools/inject-flashcards.py"
              % (len(missing), len(stale)))
        for p in (missing + stale)[:8]:
            print("   ", p)
        return 1

    print("flashcard lab: %d practice page(s) carry it (%d languages with a deck)"
          % (len(targets) - len(missing), len(glob.glob("data/flashcards/*.json"))))
    if not check:
        print("wrote %d page(s)" % written)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Bundle css/experience.css into css/style.min.css.

WHY A BUNDLE AND NOT A SECOND <link>
------------------------------------
css/style.min.css is the one stylesheet every page loads — hand-written pages,
the 460 shell-generated pages, the course hub, the 190 country funnels and the
six translated home pages all link it through their own depth prefix. Adding a
second stylesheet would mean editing ~1,560 files and every future generator,
and one missed generator produces a page with a violet hero on an /ar/ site.

So the language-aware layer rides along with the file that is already there,
exactly as css/world-redesign.css did (see the EKGURU_WORLD_REDESIGN_BUNDLED
marker at the end of the current stylesheet).

WHAT IT DOES
------------
  1. reads  css/experience.css  (the readable, hand-maintained source)
  2. strips comments and collapses indentation — the stylesheet ships
     semi-minified, and GitHub Pages gzips the rest
  3. replaces the block between

         /* EKGURU_EXPERIENCE_BUNDLED */
         ...
         /* /EKGURU_EXPERIENCE_BUNDLED */

     in css/style.min.css, or appends it the first time

Idempotent: run it twice and the second run produces a byte-identical file.
That matters because this repo has shipped stale CSS twice before — the fix
was always "one source, one place".

Run:  python3 tools/bundle-experience-css.py [--check]
      --check exits 1 if the bundle is out of date (CI/gate use).
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SRC = "css/experience.css"
BUNDLE = "css/style.min.css"
START = "/* EKGURU_EXPERIENCE_BUNDLED */"
END = "/* /EKGURU_EXPERIENCE_BUNDLED */"


def strip_comments(css):
    """Remove /* … */ comments. The source contains no comment-like text
    inside strings, no url() and no escaped delimiters — a plain non-greedy
    match is exact here, and a stricter parser would only add a dependency."""
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def compact(css):
    """Conservative compaction: collapse every run of whitespace to one space,
    then remove the spaces that are unambiguously optional around structure.
    Values, quotes and unicode are untouched — a stray space inside a
    `content:` string is a rendering bug, so nothing here rewrites values."""
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};])\s*", r"\1", css)
    css = re.sub(r";}", "}", css)
    css = re.sub(r"\s*,\s*", ",", css)
    css = re.sub(r"\s*:\s*", ":", css)
    css = re.sub(r"\s*([>+~])\s*", r"\1", css)
    return css.strip()


def build_block():
    with open(SRC, encoding="utf-8") as f:
        raw = f.read()
    body = compact(strip_comments(raw))
    if not body:
        raise SystemExit("ERROR: %s produced an empty stylesheet" % SRC)
    if body.count("{") != body.count("}"):
        raise SystemExit(
            "ERROR: unbalanced braces in %s (%d { vs %d })"
            % (SRC, body.count("{"), body.count("}"))
        )
    return START + "\n" + body + "\n" + END + "\n"


def main():
    check = "--check" in sys.argv
    with open(BUNDLE, encoding="utf-8") as f:
        current = f.read()

    block = build_block()

    if START in current:
        head, rest = current.split(START, 1)
        if END not in rest:
            raise SystemExit("ERROR: %s has a start marker with no end marker" % BUNDLE)
        _, tail = rest.split(END, 1)
        tail = tail.lstrip("\n")
        updated = head + block + ("\n" + tail if tail else "")
    else:
        sep = "" if current.endswith("\n") else "\n"
        updated = current + sep + block

    if updated == current:
        print("experience bundle already up to date (%d bytes)" % len(block))
        return 0

    if check:
        print("STALE: %s is out of date — run tools/bundle-experience-css.py" % BUNDLE)
        return 1

    with open(BUNDLE, "w", encoding="utf-8") as f:
        f.write(updated)

    print(
        "bundled %s -> %s (%d bytes of layer, stylesheet now %d bytes)"
        % (SRC, BUNDLE, len(block), len(updated))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

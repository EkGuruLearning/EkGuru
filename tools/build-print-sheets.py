#!/usr/bin/env python3
"""EkGuru — WHICH PAGES PRINT AS A SHEET (and what exactly prints).

Prakash: "print worksheet pura page hi print karti hai, par humein sirf
worksheet hi print karni hai."

css/experience.css §26 does the printing. It cannot know, by itself, which
element on a page IS the sheet — that depends on the page. This tool marks it:

  · <body data-print="sheet">        this page prints as a sheet, not a page
  · the sheet element gets           data-print-target

Marked automatically, from what the page actually contains:

  · a worksheet builder (#ws-app) — the ten languages' worksheet pages. The
    sheet inside it is #w-sheet, which js/hindi-tools.js fills; the controls
    that build it are not printed.
  · a printable guide (.art on the /materials/ pages) — 40-odd charts and
    revision sheets whose whole point is a piece of paper.

Everything else keeps normal printing: §26 still turns the chrome off, so a
lesson or an answer prints its content and nothing else either.

IDEMPOTENT: the body attribute and the target are set once. Run it twice and
the second run writes nothing.

Run:  python3 tools/build-print-sheets.py [--check]
      --check exits 1 listing pages that are not marked yet (CI / build-all)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SKIP_DIRS = {".git", "node_modules", "images", "css", "js", "data", "reports",
             "docs", "templates", "research", "tools"}
MARK = "data-print"

# The sheet, per page kind. A page is only a sheet when printing it is the
# point of the page: the ten worksheet builders, and the printed guides under
# /materials/ that carry their own Print button. Lessons, answers and hubs
# print as content with the chrome off — they are not sheets.
def judge(path, html):
    """(target_regex, kind) for this page, or None."""
    if '<div id="ws-app"' in html:
        return re.compile(r'(<div id="ws-app")'), "worksheet builder"
    if "materials/" in path and re.search(r"window\.print\s*\(\s*\)", html):
        m = re.compile(r'(<div class="art")')
        if m.search(html):
            return m, "printed guide"
    return None


def pages():
    out = []
    for dirpath, dirs, files in os.walk("."):
        parts = [x for x in dirpath.split(os.sep) if x and x != "."]
        if any(part in SKIP_DIRS or part.startswith(".") for part in parts):
            continue
        for f in sorted(files):
            if f.endswith(".html"):
                out.append(os.path.join(dirpath, f))
    return sorted(out)


def mark(path, html):
    """Returns (new_html, kind|None)."""
    found = judge(path, html)
    if not found:
        return html, None
    target, kind = found
    out = html

    if not re.search(r"<body[^>]*\b%s=" % MARK, out):
        out = re.sub(r"<body([^>]*)>", r'<body\1 %s="sheet">' % MARK, out, count=1)

    m = target.search(out)
    if m and "data-print-target" not in out:
        out = out[:m.end(0)] + " data-print-target" + out[m.end(0):]
    return out, kind


def main():
    check = "--check" in sys.argv
    unmarked, marked, written = [], 0, 0
    for p in pages():
        with open(p, encoding="utf-8") as fh:
            html = fh.read()
        new, kind = mark(p, html)
        if kind:
            marked += 1
            if new == html:
                continue
        if new == html:
            continue
        if check:
            unmarked.append(p)
            continue
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(new)
        written += 1
    if check:
        if unmarked:
            print("STALE %d page(s) — run: python3 tools/build-print-sheets.py" % len(unmarked))
            for p in unmarked[:12]:
                print("  " + p)
            return 1
        print("ok    %d printable page(s) marked, nothing else to do" % marked)
        return 0
    print("print sheets: %d written, %d printable page(s) known" % (written, marked))
    return 0


if __name__ == "__main__":
    sys.exit(main())

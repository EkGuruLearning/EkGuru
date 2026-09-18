#!/usr/bin/env python3
"""EkGuru — put the questions API on every page that asks questions.

js/question-api.js is what lets one learner's flag reach the next learner, so
it has to be loaded wherever a question is answered:

  · the ten language quiz pages and the Hindi quiz page  (js/hindi-tools.js)
  · the ten language worksheet pages                     (same builder)
  · the typing trainers                                  (same builder)
  · the world-course quiz/practice/review pages          (js/practice-engine.js)

The script is a sibling of js/hindi-tools.js and js/practice-engine.js, so it
is injected immediately before whichever of those the page already loads. The
depth prefix is taken from that tag, which is why this is a tool and not a
sed one-liner. Idempotent: a page that already has the tag is left alone.

Run:  python3 tools/inject-questions-api.py [--check]
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SKIP_DIRS = {".git", "node_modules", "images", "css", "js", "data", "reports",
             "docs", "templates", "research", "tools"}

# The tools that render questions on the page.
HOSTS = ("js/hindi-tools.js", "js/practice-engine.js")
# The world-course pages (languages/<code>/quiz, /practice, /review) render
# questions through their own course bundle, so that is a host too.
COURSE = re.compile(r'<script src="((?:\.\./)*)(js/course-[a-z-]+\.js)"')
TAG = '<script src="%sjs/question-api.js" defer></script>'
MARK = "<!-- ekguru:questions-api -->"


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


def host_tag(html):
    """The tag for one of HOSTS, with its own depth prefix."""
    for host in HOSTS:
        m = re.search(r'<script src="((?:\.\./)*)' + re.escape(host) + r'"', html)
        if m:
            return m.start(), m.group(1)
    m = COURSE.search(html)
    if m:
        return m.start(), m.group(1)
    return None, None


def inject(html):
    if MARK in html or "js/question-api.js" in html:
        return html, False
    at, prefix = host_tag(html)
    if at is None:
        return html, False
    tag = MARK + "\n" + TAG % (prefix if prefix is not None else "")
    return html[:at] + tag + "\n" + html[at:], True


def main():
    check = "--check" in sys.argv
    stale, written, seen = [], 0, 0
    for p in pages():
        with open(p, encoding="utf-8") as fh:
            html = fh.read()
        new, changed = inject(html)
        if not changed and MARK not in new:
            continue
        seen += 1
        if not changed:
            continue
        if check:
            stale.append(p)
            continue
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(new)
        written += 1
    if check:
        if stale:
            print("STALE %d page(s) — run: python3 tools/inject-questions-api.py" % len(stale))
            for p in stale[:10]:
                print("  " + p)
            return 1
        print("ok    questions API on %d question page(s)" % seen)
        return 0
    print("questions api: %d page(s) updated, %d question page(s) known" % (written, seen))
    return 0


if __name__ == "__main__":
    sys.exit(main())

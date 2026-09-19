#!/usr/bin/env python3
"""
EkGuru — remove a retired <script> tag from every page.

Some scripts get retired instead of patched (a system the site has outgrown
— js/visual-learning.js was one: emoji headings, invented motifs, and the
Taj Mahal/Diwali/Biryani boilerplate the command explicitly bans). The tag
lives in 2,600+ pages, so it comes out of every page by one tool run, not
by hand.

  python3 tools/remove-script.py js/visual-learning.js
  python3 tools/remove-script.py js/visual-learning.js --check

Idempotent: a second run changes nothing. --check exits non-zero while any
page still carries the tag.
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
os.chdir(ROOT)

SKIP_DIRS = {".git", "node_modules", "images", "css", "js", "data", "reports",
             "docs", "templates", "research", "tools", "csv"}


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    script = sys.argv[1]
    check_only = "--check" in sys.argv[2:]

    # the tag may carry any prefix of ../ and any attribute set
    tag_re = re.compile(
        r'<script\b[^>]*src="((?:\.\./)*%s)"[^>]*>\s*</script>\s*' % re.escape(script),
        re.IGNORECASE,
    )

    still, changed = 0, 0
    for root, dirs, files in os.walk(ROOT):
        rel_root = Path(root).relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel_root.parts):
            continue
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            if not f.endswith(".html"):
                continue
            p = Path(root) / f
            try:
                content = p.read_text(encoding="utf-8")
            except Exception:
                continue
            hits = tag_re.findall(content)
            if not hits:
                continue
            if check_only:
                still += 1
                if still <= 5:
                    print("STILL LOADING %s: %s" % (script, p))
            else:
                new = tag_re.sub("", content)
                if new != content:
                    p.write_text(new, encoding="utf-8")
                    changed += 1

    if check_only:
        if still:
            print("%d page(s) still load %s" % (still, script))
            sys.exit(1)
        print("clean: no page loads %s" % script)
    else:
        print("removed %s from %d page(s)" % (script, changed))


if __name__ == "__main__":
    main()

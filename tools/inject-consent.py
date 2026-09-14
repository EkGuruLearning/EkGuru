#!/usr/bin/env python3
"""Inject js/cookie-consent.js into every HTML page (idempotent).

The notice links the Privacy Policy (ads + opt-outs) and remembers
dismissal. Unlike ads, consent shows everywhere including support/ —
only /amp/ pages are skipped (custom JS is invalid AMP).

Run from the project root:  python3 tools/inject-consent.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "<!-- ekguru:consent -->"
TAG_RE = re.compile(r"[ \t]*<script[^>]*cookie-consent\.js[^>]*></script>[ \t]*\n?")


def rel_js(html_path):
    rel_dir = os.path.relpath(os.path.dirname(html_path), ROOT)
    depth = 0 if rel_dir == "." else rel_dir.count(os.sep) + 1
    return ("../" * depth) + "js/cookie-consent.js"


def inject(path):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    if "cookie-consent.js" in src:
        return "have"
    if "</body>" not in src:
        return "nobody"
    block = MARK + '\n<script src="%s" defer></script>' % rel_js(path)
    src = src.replace("</body>", block + "\n</body>", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    return "added"


def main():
    counts = {"added": 0, "have": 0, "amp": 0, "nobody": 0}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in ("node_modules", ".git")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
            if rel.startswith("amp/") or "/amp/" in rel:
                counts["amp"] += 1
                continue
            counts[inject(p)] += 1
    print("consent injector: %(added)d tagged, %(have)d already had it, "
          "%(amp)d amp skipped, %(nobody)d skipped (no body)." % counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

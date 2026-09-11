#!/usr/bin/env python3
"""Inject js/recovery.js into every HTML page (idempotent).

Single source of truth: js/recovery.js. This tool re-applies the
<script> tag after it (or the surrounding block) changes, and is safe
to run repeatedly on an already-injected tree.

Run from the project root:  python3 tools/inject-recovery.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = "<!-- ekguru:recovery:start -->"
END = "<!-- ekguru:recovery:end -->"
BLOCK_RE = re.compile(
    r"[ \t]*" + re.escape(START) + r".*?" + re.escape(END) + r"[ \t]*\n?", re.S)

def rel_js(html_path):
    rel_dir = os.path.relpath(os.path.dirname(html_path), ROOT)
    if rel_dir == ".":
        depth = 0
    else:
        depth = rel_dir.count(os.sep) + 1
    return ("../" * depth) + "js/recovery.js"

def inject(path):
    with open(path, encoding="utf-8") as f:
        src = f.read()

    # already injected -> remove old block so it can be re-applied cleanly
    if "js/recovery.js" in src:
        src = BLOCK_RE.sub("", src)
        if "js/recovery.js" in src:  # stray manual tag outside marker
            src = re.sub(r"[ \t]*<script[^>]*recovery\.js[^>]*></script>[ \t]*\n?", "", src)

    rel = rel_js(path)
    block = f"{START}\n<script src=\"{rel}\" defer></script>\n{END}"

    # anchor points, in order of preference
    anchors = [
        ("<!-- ekguru:scroll-restore:end -->", True),   # after this comment
        ("</script>", None),  # fallback handled below
        ("</body>", False),
    ]
    inserted = False
    if "<!-- ekguru:scroll-restore:end -->" in src:
        src = src.replace("<!-- ekguru:scroll-restore:end -->",
                          "<!-- ekguru:scroll-restore:end -->\n" + block, 1)
        inserted = True
    elif re.search(r'<script src="[^"]*scroll-restore\.js"></script>', src):
        src = re.sub(r'(<script src="[^"]*scroll-restore\.js"></script>)',
                     r"\1\n" + block, src, count=1)
        inserted = True
    elif re.search(r'<script src="[^"]*analytics\.js"[^>]*></script>', src):
        src = re.sub(r'(<script src="[^"]*analytics\.js"[^>]*></script>)',
                     r"\1\n" + block, src, count=1)
        inserted = True
    elif "</body>" in src:
        src = src.replace("</body>", block + "\n</body>", 1)
        inserted = True

    if not inserted:
        return False

    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    return True

def main():
    n = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in ("node_modules", ".git")]
        for fn in filenames:
            if fn.endswith(".html"):
                p = os.path.join(dirpath, fn)
                if inject(p):
                    n += 1
    print(f"injected js/recovery.js into {n} pages")
    return 0

if __name__ == "__main__":
    sys.exit(main())

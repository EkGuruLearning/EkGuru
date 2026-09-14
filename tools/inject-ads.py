#!/usr/bin/env python3
"""Inject the AdSense Auto-Ads head snippet into content pages (idempotent).

Auto Ads only (one account script; Google places units) — no manual ad
units near buttons, so no accidental-click policy risk.

Policy/trust exclusions (never get ads):
  support/ ........ donations page (money + ads = policy + trust risk)
  admin.html, admin/  owner console
  404.html, offline*.html, google*.html  utility pages
  /amp/ pages  classic script is invalid AMP

Pages whose builder already embeds adsbygoogle.js are left untouched.

Run from the project root:  python3 tools/inject-ads.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "<!-- ekguru:ads -->"
SNIPPET = (
    MARK + "\n"
    '<meta name="google-adsense-account" '
    'content="ca-pub-8175326569491671">\n'
    '<script async src="https://pagead2.googlesyndication.com/pagead/js/'
    'adsbygoogle.js?client=ca-pub-8175326569491671" '
    'crossorigin="anonymous"></script>'
)

SKIP_DIRS = ("support", "admin")
SKIP_FILES = ("404.html", "admin.html", "offline.html")


def excluded(rel):
    rel = rel.replace(os.sep, "/")
    if rel.startswith("amp/") or "/amp/" in rel:
        return True
    if os.path.basename(rel).startswith("google") and rel.endswith(".html"):
        return True
    if os.path.basename(rel) in SKIP_FILES:
        return True
    first = rel.split("/")[0]
    if first in SKIP_DIRS:
        return True
    return False


def inject(path):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    if "adsbygoogle.js" in src:
        return "have"
    if "</head>" not in src:
        return "nohead"
    src = src.replace("</head>", SNIPPET + "\n</head>", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    return "added"


def main():
    counts = {"added": 0, "have": 0, "excluded": 0, "nohead": 0}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in ("node_modules", ".git")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, ROOT)
            if excluded(rel):
                counts["excluded"] += 1
                continue
            counts[inject(p)] += 1
    print("ads injector: %(added)d tagged, %(have)d already had it, "
          "%(excluded)d excluded, %(nohead)d skipped (no head)." % counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

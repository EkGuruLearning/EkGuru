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


COUNTER_RE = re.compile(r"<script[^>]*\bsrc=\"[^\"]*js/(site-config|analytics)\.js\"[^>]*></script>")


def ensure_counter(src, path):
    """The cookieless page counter (js/analytics.js, which reads its provider
    from js/site-config.js) belongs on every page the consent notice is on.
    245 indexable pages — the root Indian topic trees — had the notice but
    not the counter, so their visits were never counted (18 Nov 2026).
    Missing tags go in just before the consent tag, config first, so the
    deferred scripts run in that order; a page that already has one of the
    two gets only the other."""
    have = set(m.group(1) for m in COUNTER_RE.finditer(src))
    want = [n for n in ("site-config", "analytics") if n not in have]
    if not want:
        return src, False
    prefix = rel_js(path)[: -len("js/cookie-consent.js")]
    tags = "".join('<script src="%sjs/%s.js" defer></script>\n' % (prefix, n) for n in want)
    # Anchor: the analytics tag when only the config is missing (the config
    # must execute first), otherwise the consent tag.
    anchor = None
    if want == ["site-config"]:
        for m in COUNTER_RE.finditer(src):
            if m.group(1) == "analytics":
                anchor = m
                break
    if anchor is None:
        anchor = TAG_RE.search(src)
        if not anchor:
            return src, False
    tag = anchor.group(0).lstrip()
    return src[: anchor.start()] + tags + tag + src[anchor.end():], True


def inject(path):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    if "cookie-consent.js" in src:
        src2, changed = ensure_counter(src, path)
        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write(src2)
            return "counter"
        return "have"
    if "</body>" not in src:
        return "nobody"
    block = MARK + '\n<script src="%s" defer></script>' % rel_js(path)
    src = src.replace("</body>", block + "\n</body>", 1)
    src, _ = ensure_counter(src, path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    return "added"


def main():
    counts = {"added": 0, "have": 0, "counter": 0, "amp": 0, "nobody": 0}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # reports/ holds build evidence (email previews, audits) — files, not
        # pages anyone visits; tools/ templates are not pages either.
        dirnames[:] = [d for d in dirnames if d not in ("node_modules", ".git", "reports", "tools", "A-Manually")]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
            if fn.startswith("google") and fn.endswith(".html") and "/" not in rel:
                # Search Console ownership token: Google wants that file's
                # bytes as issued, not a page with scripts in it.
                continue
            if rel.startswith("amp/") or "/amp/" in rel:
                counts["amp"] += 1
                continue
            counts[inject(p)] += 1
    print("consent injector: %(added)d tagged, %(have)d already had it, "
          "%(counter)d given the page counter, "
          "%(amp)d amp skipped, %(nobody)d skipped (no body)." % counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""EkGuru — STORYBOOK INJECTOR (v143).

    python3 tools/inject-storybook.py

Gives EVERY Hindi page the Barakhadi treatment: storybook.css
(reveal animations, cards) + storybook.js (auto 🔊 on Hindi text,
global speed pill, scroll reveal) + an English TTS hint line on
pages that actually contain Hindi.

Why an injector instead of editing 6 builders: the Hindi sections
(learn, hindi, materials, toolbox, ask, answers, daily-hindi) are
produced by different generators. A last-step injector covers all
present AND future pages in one place, the same pattern as
tools/patch.js and tools/inject-recovery.py.

Safety:
  - idempotent: pages already carrying storybook (or the
    <!-- ekguru:storybook --> marker) are skipped;
  - the css/js prefix is DERIVED from the page's own
    style.min.css href, so depth is always right (fallback:
    directory depth);
  - AMP pages are skipped (custom JS is forbidden there);
  - every write asserts the file still ends with </html>
    (the v140 truncation lesson).
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SECTIONS = ["learn", "hindi", "materials", "toolbox", "ask", "answers",
            "daily-hindi"]
MARK = "<!-- ekguru:storybook -->"
HINT = ('<p class="sb-hint">🔊 <b>Tap any speaker button to hear Hindi spoken.</b> '
        "Too fast or slow? Use the <b>speed</b> button at the "
        "bottom-right of the page.</p>")
DEVA = re.compile(r"[\u0900-\u097F]")


def prefix_of(html, path):
    """Relative prefix (../../) derived from the page's own CSS href."""
    m = re.search(r'href="([^"]*css/style\.min\.css)"', html)
    if m:
        return m.group(1)[: -len("css/style.min.css")]
    return "../" * (len(path.split("/")) - 1)


def process(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        h = f.read()
    if MARK in h:
        return "skip-have"
    if "</body>" not in h or "</head>" not in h:
        return "skip-nobody"
    pre = prefix_of(h, path)
    did = []

    # CSS, unless the page's own builder already added it.
    if "storybook.css" not in h:
        css_tag = "\n%s\n" % MARK + \
            '<link rel="stylesheet" href="%scss/storybook.css">' % pre
        m = re.search(r"<link[^>]*css/style\.min\.css\"[^>]*>", h)
        if m:
            h = h[:m.end()] + css_tag + h[m.end():]
        else:
            h = h.replace("</head>", css_tag + "\n</head>", 1)
        did.append("css")

    # Hint, once, on pages that actually contain Hindi.
    if DEVA.search(h) and "</h1>" in h and "sb-hint" not in h:
        h = h.replace("</h1>", "</h1>\n" + MARK + "\n" + HINT, 1)
        did.append("hint")

    # JS, unless the page's own builder already added it.
    if "storybook.js" not in h:
        js_tag = MARK + "\n" + \
            '<script src="%sjs/storybook.js" defer></script>\n' % pre
        h = h.replace("</body>", js_tag + "</body>", 1)
        did.append("js")

    if not did:
        return "skip-have"
    # v140 lesson: never save a damaged file. Presence + growth, not
    # tail order (fixed shells now close cleanly; old pages may not).
    assert "</html>" in h, "no-html-close: " + path
    assert len(h) > len(open(path, encoding="utf-8",
                              errors="replace").read()), "shrunk: " + path
    with open(path, "w", encoding="utf-8") as f:
        f.write(h)
    return "hint" if "hint" in did else "js"


def main():
    counts = {"hint": 0, "js": 0, "skip-have": 0, "skip-nobody": 0,
              "skip-amp": 0}
    odd = []
    for section in SECTIONS:
        for path in sorted(glob.glob(section + "/**/*.html", recursive=True)):
            if "/amp/" in path or path.startswith("amp/"):
                counts["skip-amp"] += 1
                continue
            try:
                counts[process(path)] += 1
            except AssertionError as e:
                odd.append(str(e))
    print("storybook injector: %d pages got CSS+JS (%d with Hindi hint), "
          "%d already had it, %d skipped (no body), %d amp skipped."
          % (counts["hint"] + counts["js"], counts["hint"],
             counts["skip-have"], counts["skip-nobody"], counts["skip-amp"]))
    if odd:
        print("REFUSED (left untouched):")
        for o in odd:
            print("  ", o)
    with open("reports/inject-storybook.json", "w", encoding="utf-8") as f:
        json.dump({"counts": counts, "refused": odd}, f, ensure_ascii=False,
                  indent=2)


if __name__ == "__main__":
    main()

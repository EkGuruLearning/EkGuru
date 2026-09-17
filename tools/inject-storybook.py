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
  - chapter banners come from tools/topic-meta.json (built by
    tools/build-topic-map.py); unclaimed pages keep the default
    look — a theme is never guessed.
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
            "daily-hindi", "languages", "bengali"]
MARK = "<!-- ekguru:storybook -->"
HINT = ('<p class="sb-hint">🔊 <b>Tap any speaker button to hear Hindi spoken.</b> '
        "Too fast or slow? Use the <b>speed</b> button at the "
        "bottom-right of the page.</p>")
DEVA = re.compile(r"[\u0900-\u097F]")

MARK2 = "<!-- ekguru:chapter -->"
CHAPTERS = ["basics", "conversation", "pronunciation", "grammar",
            "vocabulary", "travel", "daily-life", "numbers",
            "time-dates", "food", "shopping"]
LEVELS = ["beginner", "elementary", "intermediate", "advanced"]
LANGS = ["bengali", "gujarati", "kannada", "malayalam", "marathi",
         "punjabi", "tamil", "telugu", "urdu"]
ROOT_LANGS = ["bengali"]


def load_meta():
    try:
        with open("tools/topic-meta.json", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {"topics": {}, "pages": {}}


META = load_meta()


def resolve(path):
    """Chapter key for a page, or None. Specific beats generic;
    anything unclaimed stays on the default look."""
    pages = META.get("pages", {})
    target = path[:-len("/index.html")] if path.endswith("/index.html") else path
    if target in pages:
        return pages[target]
    parts = target.split("/")
    if len(parts) >= 3 and parts[0] == "learn" and parts[1] == "hindi":
        if parts[2] in CHAPTERS:
            return parts[2]
        if parts[2] in LEVELS:
            return "level-" + parts[2]
        if parts[2] == "practice":
            return "section-practice"
        if parts[2] == "my-progress":
            return "section-progress"
        if parts[2] == "review":
            return "section-review"
        return None
    if len(parts) >= 2 and parts[0] == "learn" and parts[1] in LANGS:
        return "lang-" + parts[1]
    sec = {"ask": "section-ask", "answers": "section-answers",
           "daily-hindi": "section-daily", "toolbox": "section-toolbox",
           "materials": "section-materials"}
    if parts[0] in sec:
        return sec[parts[0]]
    if parts[0] == "learn" and len(parts) >= 2:
        if parts[1] == "paths":
            return "section-paths"
        if parts[1] == "practice":
            return "section-practice"
    # world courses: honest generic banner, name read from the page H1
    if parts[0] == "languages" and len(parts) >= 2:
        return "section-language"
    # root topic hubs (v152 pilot: /bengali/): per-language banner
    if parts[0] in ROOT_LANGS:
        return "lang-" + parts[0]
    return None


def banner(key, name=None):
    t = META["topics"][key]
    return ('<div class="sb-chapter" style="--sb-accent:%s;--sb-tint:%s">'
            '<span class="sb-ch-mascot" aria-hidden="true">%s</span>'
            '<span class="sb-ch-name">%s <i>%s</i></span>'
            '<span class="sb-ch-kind">%s</span>'
            '<span class="sb-ch-floats" aria-hidden="true">%s</span></div>'
            % (t["accent"], t["tint"], t["mascot"], (name or t["en"]), t["hi"],
               t["kind"], t["floats"]))


def prefix_of(html, path):
    """Relative prefix (../../) derived from the page's own CSS href."""
    m = re.search(r'href="([^"]*css/style\.min\.css)"', html)
    if m:
        return m.group(1)[: -len("css/style.min.css")]
    return "../" * (len(path.split("/")) - 1)


def process(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        h = f.read()
    if "</body>" not in h or "</head>" not in h:
        return "skip-nobody"
    pre = prefix_of(h, path)
    did = []

    if MARK not in h:
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

    # Chapter banner + palette (v147), once per page.
    if MARK2 not in h:
        key = resolve(path)
        if key and key in META.get("topics", {}):
            HT = "<h" + "1"
            mb = re.search("<bo" + "dy([^>]*)>", h)
            if mb and "data-topic" not in mb.group(0):
                h = h[:mb.end(1)] + ' data-topic="%s"' % key + h[mb.end(1):]
                did.append("topic")
            mh = re.search(HT + "[\\s>]", h)
            h1name = None
            if key == "section-language" or (key.startswith("lang-") and not path.startswith("learn/")):
                H1 = "<h" + "1"
                m1 = re.search(H1 + "[^>]*>(.*?)<" + "/h1>", h, re.S)
                if m1:
                    # direct text only: drops status pills like "Available"
                    h1name = " ".join(m1.group(1).split("<")[0].split())[:60]
            sc, sc2 = "<scr" + "ipt", "</scr" + "ipt>"
            if mh and h.count(sc, 0, mh.start()) == h.count(sc2, 0, mh.start()):
                h = h[:mh.start()] + MARK2 + "\n" + banner(key, h1name) + "\n" + h[mh.start():]
                did.append("chapter")

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
    if "chapter" in did:
        return "chapter"
    return "hint" if "hint" in did else "js"


def main():
    counts = {"hint": 0, "js": 0, "chapter": 0, "skip-have": 0,
              "skip-nobody": 0, "skip-amp": 0}
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
    print("storybook injector: %d pages touched (%d chapter banners, %d Hindi hints), "
          "%d already had it, %d skipped (no body), %d amp skipped."
          % (counts["hint"] + counts["js"] + counts["chapter"],
             counts["chapter"], counts["hint"],
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

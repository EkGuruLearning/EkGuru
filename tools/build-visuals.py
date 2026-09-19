#!/usr/bin/env python3
"""EkGuru — the level visuals: the same learner, from A1 to C5.

v2 of the ladder (2026-09-19): the figure is ONE neutral learner at every
level. What changes with the level is the band (start -> expert): the prop
beside the figure carries more of the page as the contexts get more complex.
The old age-staged figures (a child at A1, an elder at C2) treated age as
level eligibility; the site no longer does that, and nothing about the
picture claims a level belongs to an age group.

  · colours come from the language's own theme (the same accent its course
    pages use), so a page looks like the language it teaches
  · the level label and the native name are part of the picture, not
    decoration added later: the file itself says "B1 · Independent / Deutsch"
  · every figure is a plain SVG (2-4 KB), no fonts to load, no requests

Output:  images/vis/<code>-<rung>.svg          (per language x 11 levels)
         data/visuals.json                     (the manifest: band, cefr, alt)
         the gallery on every course hub       (languages/<code>/course/)

The ladder itself is data/levels.json — eleven levels: A1 A2 A3 B1 B2 B3
C1 C2 C3 C4 C5. A3/B3/C3/C4/C5 are EkGuru Extended Mastery, not CEFR.

Run:  python3 tools/build-visuals.py [--check]
"""

import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

OUT = "images/vis"
MARK_START = "<!-- ekguru:level-visuals:start -->"
MARK_END = "<!-- ekguru:level-visuals:end -->"

# A theme per language: the same families the course pages already use.
THEMES = {
    "hi": ("#e0682a", "#b5430b"), "bn": ("#3f8f5b", "#226b3c"),
    "gu": ("#0f7b8a", "#0a5b66"), "kn": ("#8a5ab8", "#5f3a8c"),
    "ml": ("#2f7d32", "#1c5a20"), "mr": ("#c2571a", "#8a3a0d"),
    "pa": ("#b8860b", "#8a6408"), "ta": ("#b3261e", "#7f1a13"),
    "te": ("#1f6feb", "#14509e"), "ur": ("#2b5f3f", "#1b3f29"),
    "ar": ("#1f7a5c", "#125240"), "zh": ("#c0392b", "#8e2a1f"),
    "ja": ("#b03060", "#7d1f43"), "ko": ("#2b6cb0", "#1c4c80"),
    "fr": ("#3b5bdb", "#28409e"), "de": ("#4b4b58", "#2f2f38"),
    "es": ("#d97706", "#a35705"), "it": ("#0e8a6d", "#0a6350"),
    "pt": ("#137a4b", "#0d5735"), "ru": ("#3f67a8", "#2b4877"),
    "en": ("#5b4bd6", "#3f31a0"), "fa": ("#0f766e", "#0b554f"),
    "he": ("#2563b0", "#1a4780"), "id": ("#b45309", "#833a06"),
    "ms": ("#15803d", "#0f5c2b"), "nl": ("#ea580c", "#b23f08"),
    "pl": ("#b91c1c", "#871414"), "sw": ("#047857", "#03553e"),
    "th": ("#7c3aed", "#5a25b0"), "tr": ("#0e7490", "#0a5568"),
    "uk": ("#1d4ed8", "#153aa0"), "vi": ("#ca8a04", "#946406"),
}

DEFAULT_THEME = ("#4f32d9", "#3a2299")

# An English name for any language whose data file did not carry one, so a
# figure is never captioned with a bare two-letter code.
NAMES = {
    "en": "English", "hi": "Hindi", "bn": "Bengali", "gu": "Gujarati",
    "kn": "Kannada", "ml": "Malayalam", "mr": "Marathi", "pa": "Punjabi",
    "ta": "Tamil", "te": "Telugu", "ur": "Urdu", "ar": "Arabic",
    "zh": "Chinese", "ja": "Japanese", "ko": "Korean", "fr": "French",
    "de": "German", "es": "Spanish", "it": "Italian", "pt": "Portuguese",
    "ru": "Russian", "fa": "Persian", "he": "Hebrew", "id": "Indonesian",
    "ms": "Malay", "nl": "Dutch", "pl": "Polish", "sw": "Swahili",
    "th": "Thai", "tr": "Turkish", "uk": "Ukrainian", "vi": "Vietnamese",
}


def themes_for(code):
    return THEMES.get(code, DEFAULT_THEME)


# Where a language's own hub page lives. The first existing path wins.
INDIAN = {"hi": "hindi", "bn": "bengali", "gu": "gujarati", "kn": "kannada",
          "ml": "malayalam", "mr": "marathi", "pa": "punjabi", "ta": "tamil",
          "te": "telugu", "ur": "urdu"}


def hub_for(code):
    for cand in ("languages/%s/course/index.html" % code,
                 "learn/%s/index.html" % INDIAN.get(code, ""),
                 "languages/%s/index.html" % code):
        if cand and "//" not in cand and os.path.exists(cand):
            return cand
    return ""


def courses():
    """Every language that has a page on the site, with the route to it.

    `data/courses.json` covers the ten world courses; the Indian languages and
    Hindi live in `learn/`. The list is read from the site rather than kept by
    hand here, so a new language appears the day its page does — and a language
    with no page yet simply does not get a figure.
    """
    out = {}
    if os.path.exists("data/courses.json"):
        data = json.load(open("data/courses.json", encoding="utf-8"))
        for c in data.get("courses", []):
            out[c["lang"]] = {"name": c["name"], "native": c.get("native", ""),
                              "url": c.get("url", ""), "speech": c.get("speechTag", "")}
    for code in sorted(set(list(out) + list(INDIAN) +
                           [d[5:7] for d in os.listdir("data") if re.fullmatch(r"lang-[a-z]{2}\.json", d)])):
        info = out.setdefault(code, {"name": code, "native": "", "url": "", "speech": ""})
        f = "data/lang-%s.json" % code
        if os.path.exists(f):
            d = json.load(open(f, encoding="utf-8"))
            tl = d.get("target_language") or {}
            if isinstance(tl, dict):
                info["name"] = tl.get("name") or info["name"]
                info["native"] = tl.get("native_name") or info.get("native", "")
        if code == "hi":
            info.update({"name": "Hindi", "native": "हिन्दी", "speech": "hi-IN"})
        hub = hub_for(code)
        if not hub:
            out.pop(code)
            continue
        info["url"] = hub
        info["page"] = hub
        if info["name"] == code:
            info["name"] = NAMES.get(code, code.upper())
    return out


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# The figure is a single neutral learner on every rung. What changes with the
# level is the BAND (start -> expert): the prop beside the figure carries more
# and more of the page, which is the honest way to show growing complexity
# without assigning a level to an age group. (v2 of the ladder: age was the
# old proxy and is gone — see data/levels.json.)
BANDS = {
    "start":  {"body": 34.0, "shoulder": 22.0, "head": 24.0},
    "grow":   {"body": 42.0, "shoulder": 25.0, "head": 24.0},
    "mature": {"body": 50.0, "shoulder": 27.0, "head": 23.5},
    "deep":   {"body": 56.0, "shoulder": 29.0, "head": 23.0},
    "expert": {"body": 60.0, "shoulder": 30.0, "head": 22.5},
}


def props_for(band, a):
    """The prop says what the level is FOR: more of the page, level by level."""
    if band == "start":
        return ('<rect x="222" y="136" width="30" height="30" rx="6" fill="#fff" stroke="%s" stroke-width="2"/>'
                '<text x="237" y="157" font-size="17" text-anchor="middle" fill="%s" '
                'font-family="system-ui,sans-serif">A</text>' % (a, a))
    if band == "grow":
        return ('<rect x="220" y="134" width="36" height="26" rx="4" fill="#fff" stroke="%s" stroke-width="2"/>'
                '<path d="M226 144 h24 M226 152 h18" stroke="%s" stroke-width="2"/>' % (a, a))
    if band == "mature":
        return ('<rect x="216" y="130" width="46" height="30" rx="4" fill="#fff" stroke="%s" stroke-width="2"/>'
                '<rect x="221" y="152" width="36" height="4" rx="2" fill="%s" opacity=".5"/>'
                '<path d="M221 140 h20" stroke="%s" stroke-width="2"/>' % (a, a, a))
    if band == "deep":
        return ('<rect x="216" y="128" width="44" height="32" rx="4" fill="#fff" stroke="%s" stroke-width="2"/>'
                '<path d="M238 128 v32" stroke="%s" stroke-width="1.6" opacity=".5"/>'
                '<path d="M221 138 h34 M221 146 h26" stroke="%s" stroke-width="2" opacity=".8"/>' % (a, a, a))
    return ('<rect x="214" y="126" width="48" height="34" rx="4" fill="#fff" stroke="%s" stroke-width="2"/>'
            '<path d="M238 126 v34" stroke="%s" stroke-width="1.6" opacity=".5"/>'
            '<path d="M219 136 h38 M219 144 h30 M219 152 h36" stroke="%s" stroke-width="2" opacity=".8"/>'
            '<circle cx="257" cy="136" r="2.5" fill="%s"/>' % (a, a, a, a))


def figure(code, lang, rung, index):
    """One SVG: the same neutral learner at every level, a busier prop at each band."""
    a, b = themes_for(code)
    label = rung["label"]
    band = rung.get("band") or "start"
    p = BANDS[band]
    body_h, shoulder, head = p["body"], p["shoulder"], p["head"]
    cx = 160.0
    head_y = 96.0 - body_h - head / 2 + 26
    torso_top = head_y + head - 2
    r8 = lambda v: round(v, 1)
    props = props_for(band, a)

    hair = ('<path d="M%s %s a%s %s 0 0 1 %s 0 q%s -%s -%s -%s q-%s 0 -%s %s z" fill="#3a3a44"/>'
            % (r8(cx - head / 2), r8(head_y - head * 0.16), r8(head / 2), r8(head * 0.6),
               r8(head), r8(head * 0.5), r8(head * 0.5), r8(head * 0.5), r8(head * 0.2),
               r8(head * 0.5), r8(head * 0.5), r8(head * 0.5)))
    head_shape = ('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#f3c9a8"/>'
                  % (r8(cx), r8(head_y), r8(head / 2), r8(head / 2 + 3)))

    native = esc(lang.get("native") or lang["name"])
    name = esc(lang["name"])
    can = esc(rung["can"])
    direction = "rtl" if code in ("ar", "fa", "he", "ur") else "ltr"
    stage_name = rung["name"].split(" · ")[-1]

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="320" height="200" '
        'role="img" aria-label="%s at level %s: %s">\n'
        '<title>%s at %s \u2014 %s</title>\n'
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="%s" stop-opacity=".16"/>'
        '<stop offset="1" stop-color="%s" stop-opacity=".3"/></linearGradient></defs>\n'
        '<rect width="320" height="200" rx="14" fill="url(#bg)"/>\n'
        '<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".18"/>\n'
        '<rect x="0" y="168" width="320" height="32" fill="%s" opacity=".1"/>\n'
        '<g><rect x="%s" y="%s" width="%s" height="%s" rx="10" fill="%s"/>'
        '<rect x="%s" y="%s" width="%s" height="%s" rx="8" fill="#f3c9a8"/>%s%s</g>\n'
        '%s\n'
        '<text x="16" y="26" font-size="13" font-weight="700" fill="%s" '
        'font-family="system-ui,-apple-system,Segoe UI,sans-serif">%s</text>\n'
        '<text x="16" y="44" font-size="11" fill="%s" direction="%s" '
        'font-family="system-ui,-apple-system,Segoe UI,sans-serif">%s</text>\n'
        '<text x="304" y="44" text-anchor="end" font-size="10" fill="%s" '
        'font-family="system-ui,-apple-system,Segoe UI,sans-serif">%s</text>\n'
        '<text x="16" y="190" font-size="10" fill="%s" '
        'font-family="system-ui,-apple-system,Segoe UI,sans-serif">%s \u2014 %s</text>\n'
        '</svg>\n'
        % (name, label, can, name, label, esc(stage_name),
           a, b,
           r8(cx), r8(head_y), r8(head * 1.7), a,
           a,
           r8(cx - shoulder / 2), r8(torso_top - 4), r8(shoulder), r8(body_h + 10), "#f3c9a8",
           r8(cx - head / 2), r8(head_y - head / 2), r8(head), r8(head),
           head_shape, hair,
           props,
           a, label, b, direction, native,
           b, esc(stage_name),
           b, name, esc(stage_name))
    )


def gallery(code, lang, page, rungs, manifest):
    """The strip of eleven figures a language hub carries.

    Written with the page's own depth (`../../`), the way every other link and
    image on the site is written: a root-absolute `/images/...` would break the
    moment the site is served from a folder rather than a domain root, and the
    local preview is exactly that.
    """
    prefix = "../" * (page.count("/") - 0) if "/" in page else ""
    prefix = "../" * page.count("/")
    items = []
    for r in rungs:
        info = manifest["figures"]["%s-%s" % (code, r["id"])]
        extra = " · EkGuru Extended Mastery" if r.get("cefr") is False else ""
        items.append(
            '<figure class="lv-fig%s">'
            '<img src="%s%s" width="320" height="200" loading="lazy" alt="%s">'
            '<figcaption><b>%s</b> %s%s</figcaption></figure>'
            % (" lv-fig-extended" if r.get("cefr") is False else "",
               prefix, info["path"], esc(info["alt"]), r["label"],
               esc(r["name"].split(" · ")[-1]), extra))
    return (
        MARK_START + "\n"
        '<section class="lv-visuals" aria-labelledby="lv-visuals-h">\n'
        '<h2 id="lv-visuals-h">The same learner, from %s to %s</h2>\n'
        '<p>The same ladder every language here climbs, in eleven rungs: the six '
        'official CEFR levels, and the EkGuru Extended Mastery levels (A3, B3, C3, '
        'C4, C5) that go beyond them. The figure is the same person at every level — '
        'the level is not an age group, and a learner of any age can study any rung. '
        '<a href="%show-levels-work/">Here is how the eleven levels work</a>.</p>\n'
        '<div class="lv-strip">\n%s\n</div>\n'
        '</section>\n'
        % (rungs[0]["label"], rungs[-1]["label"], prefix, "\n".join(items)) +
        MARK_END + "\n")


def main():
    check = "--check" in sys.argv
    levels = json.load(open("data/levels.json", encoding="utf-8"))
    rungs = levels["rungs"]
    langs = courses()
    os.makedirs(OUT, exist_ok=True)

    manifest = {"version": 1, "generated_note": "generated by tools/build-visuals.py",
                "rungs": [r["id"] for r in rungs], "languages": {}, "figures": {}}
    written = 0
    for code in sorted(langs):
        lang = langs[code]
        manifest["languages"][code] = {"name": lang["name"], "native": lang.get("native", ""),
                                       "url": lang.get("url", ""), "theme": list(themes_for(code))}
        for i, r in enumerate(rungs):
            path = "%s/%s-%s.svg" % (OUT, code, r["id"])
            svg = figure(code, lang, r, i)
            key = "%s-%s" % (code, r["id"])
            manifest["figures"][key] = {
                "path": path, "language": code, "language_name": lang["name"], "rung": r["id"],
                "label": r["label"], "band": r.get("band", "start"), "cefr": r.get("cefr", True),
                "alt": "Learner at level %s studying %s — %s%s" % (
                    r["label"], lang["name"], r.get("can", ""),
                    " (EkGuru Extended Mastery, not official CEFR)" if r.get("cefr") is False else ""),
            }
            if os.path.exists(path) and open(path, encoding="utf-8").read() == svg:
                continue
            if check:
                print("STALE %s — run tools/build-visuals.py" % path)
                return 1
            open(path, "w", encoding="utf-8").write(svg)
            written += 1

    body = json.dumps(manifest, indent=1, ensure_ascii=False, sort_keys=True) + "\n"
    if not (os.path.exists("data/visuals.json") and open("data/visuals.json", encoding="utf-8").read() == body):
        if check:
            print("STALE data/visuals.json — run tools/build-visuals.py")
            return 1
        open("data/visuals.json", "w", encoding="utf-8").write(body)
        written += 1

    # The gallery goes on every course hub, once.
    hubs = 0
    for code, lang in sorted(langs.items()):
        page = lang.get("page") or ""
        if not page or not os.path.exists(page):
            continue
        original = open(page, encoding="utf-8").read()
        html = original
        block = gallery(code, lang, page, rungs, manifest)
        if MARK_START in html:                     # a rebuild moves the strip, never stacks it
            start = html.index(MARK_START)
            end = html.index(MARK_END) + len(MARK_END)
            html = html[:start] + html[end:]
        # inside the page's content, at the end of it: after </main> the strip
        # would sit in the chrome band, outside the reading column and outside
        # anything a reader-mode or a plugin keeps.
        anchor = html.rfind("</main>")
        if anchor < 0:
            anchor = html.find("<!-- ekguru:shell-footer:start -->")
        if anchor < 0:
            anchor = html.find("<footer")
        if anchor < 0:
            continue
        new = html[:anchor].rstrip("\n") + "\n" + block + html[anchor:]
        # compare against the page as it was on disk, not against the copy the
        # old strip was just cut out of — otherwise a page that already carries
        # a strip can never check clean.
        if new != original:
            if check:
                print("STALE %s — run tools/build-visuals.py" % page)
                return 1
            open(page, "w", encoding="utf-8").write(new)
            written += 1
        hubs += 1

    if check:
        print("ok    level visuals: %d language(s) x %d rungs, %d hub(s)" % (len(langs), len(rungs), hubs))
        return 0
    print("level visuals: %d file(s) written — %d language(s) x %d rungs, %d hub(s)"
          % (written, len(langs), len(rungs), hubs))
    return 0


if __name__ == "__main__":
    sys.exit(main())

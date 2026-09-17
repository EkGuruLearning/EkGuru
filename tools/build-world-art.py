#!/usr/bin/env python3
"""Design the per-language world artwork — writes images/xp/world-*.svg.

WHY VECTOR ART AND NOT PHOTOGRAPHS
----------------------------------
Every market page used to show the same violet illustration, and a /ar/ visitor
read right-to-left text next to a picture drawn left-to-right. Photography also
solves the wrong problem here: a stock photo of "a person learning" cannot say
*Devanagari*, and it costs 80-200 KB per market on the connection a first-time
visitor is most likely to have.

So each world gets one drawn emblem:

  · 640x640, hand-built paths, no webfont, no raster, 3-6 KB
  · the abstract geometry of that writing system — the Devanagari headstroke
    and its hanging stems, the connected Arabic baseline with its dots, the
    CJK tile grid, the Latin baseline/diagonal/counter
  · the palette of that market, read out of css/experience.css so the drawing
    can never drift from the colours the page actually uses

RULES
-----
1. No flags, no religious symbols, no faces, no letters of the Latin alphabet
   spelling anything. Abstract script geometry only.
2. Every path is written by hand below; this file is the source of truth for
   the artwork and is safe to re-run — identical input gives identical bytes.
3. The artwork is decorative. Every page that shows it also carries the same
   information as text, so alt="" + aria-hidden is correct and a screen reader
   never hears a description of a drawing.

Palettes come from css/experience.css, keys come from tools/build-market-pages.py.

Run:  python3 tools/build-world-art.py [--check]
      --check exits 1 if an SVG on disk is out of date (CI/gate use).
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

OUT_DIR = "images/xp"
CSS = "css/experience.css"

# The market default palette — the :root fallback in css/experience.css.
FALLBACK = ("#4f32d9", "#8b5cf6", "#f0a020")

# Selector that carries each world's palette. `en` has no rule of its own: it
# rides on :root, which is exactly what an English visitor sees.
LANG_SELECTOR = {
    "en": None,
    "hi": "hi",
    "es": "es",
    "fr": "fr",
    "de": "de",
    "pt": "pt",
    "ja": "ja",
    "ar": "ar",
}

# Which drawing belongs to which market. The market's own writing system decides
# the centre mark; `multi` is the one emblem that is not a single script.
FAMILY = {
    "en": "latin",
    "hi": "devanagari",
    "es": "latin",
    "fr": "latin",
    "de": "latin",
    "pt": "latin",
    "ja": "cjk",
    "ar": "arabic",
    "multi": "multi",
}

# How each family is labelled inside the drawing (kept in the <title> only, so
# the information exists for anyone who opens the file directly).
FAMILY_LABEL = {
    "devanagari": "Devanagari",
    "arabic": "Arabic",
    "cjk": "CJK",
    "latin": "Latin",
    "multi": "many scripts",
}


def read_palettes():
    """Pull --xp-a / --xp-b / --xp-c out of css/experience.css.

    The stylesheet is the design source of truth; copying hex codes into this
    file is how the two drift apart six months later. Parsing is deliberately
    narrow: find the selector for a language, take the three tokens from that
    block only.
    """
    with open(CSS, encoding="utf-8") as f:
        css = f.read()

    palettes = {"multi": ("#4f32d9", "#8b5cf6", "#f0a020")}

    for lang, selector in LANG_SELECTOR.items():
        if selector is None:
            palettes[lang] = FALLBACK
            continue

        # html[lang="es"], html[lang="fr"], html[lang^="zh"] { … }
        match = None
        for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
            head = m.group(1)
            if re.search(r'html\[lang[^\]]*"%s"' % re.escape(selector), head):
                if "--xp-a:" in m.group(2):
                    match = m.group(2)
                    break
        if not match:
            print("WARN: no palette block for %s — using the default" % lang)
            palettes[lang] = FALLBACK
            continue

        vals = []
        for token in ("--xp-a", "--xp-b", "--xp-c"):
            mm = re.search(re.escape(token) + r"\s*:\s*([^;]+);", match)
            vals.append(mm.group(1).strip() if mm else "#4f32d9")
        palettes[lang] = tuple(vals)

    return palettes


def mix(hex_a, hex_b, t):
    """Blend two hex colours. SVG has no color-mix() that older renderers
    understand, and these files are opened directly by browsers and by the
    og:image pipeline, so the blend is baked at build time."""
    ah = [int(hex_a[i:i + 2], 16) for i in (1, 3, 5)]
    bh = [int(hex_b[i:i + 2], 16) for i in (1, 3, 5)]
    out = [round(a + (b - a) * t) for a, b in zip(ah, bh)]
    return "#%02x%02x%02x" % tuple(out)


def alpha(hex_col, a):
    """Hex + opacity → rgba() for the hairlines."""
    h = [int(hex_col[i:i + 2], 16) for i in (1, 3, 5)]
    return "rgba(%d,%d,%d,%s)" % (h[0], h[1], h[2], a)


# ---------------------------------------------------------------------------
# the centre mark of each world
# ---------------------------------------------------------------------------

def marks_devanagari(a, b, c):
    """A headstroke (शिरोरेखा) with stems hanging from it, the anusvāra dot
    above and a matra loop below. Reads as Devanagari at a glance without
    spelling a word."""
    stem = dict(fill="none", stroke=a, stroke_width=17, stroke_linecap="round")
    thin = dict(fill="none", stroke=a, stroke_width=13, stroke_linecap="round")
    return """
    <!-- शिरोरेखा: one uninterrupted headstroke across the whole family -->
    <path d="M196 250 H444" fill="none" stroke="{a}" stroke-width="19" stroke-linecap="round"/>
    <circle cx="320" cy="211" r="13" fill="{c}"/>
    <!-- hanging stems: straight, hooked, looped, forked -->
    <path d="M240 250 V344 q0 26 22 26" {stem}/>
    <path d="M300 250 V394 H268" {stem}/>
    <path d="M372 250 V322 q0 30 -30 30 h-16" {thin}/>
    <path d="M420 250 V292 q34 6 34 40 q0 30 -30 30" {thin}/>
    <path d="M258 416 q62 34 124 0" fill="none" stroke="{b}" stroke-width="11"
          stroke-linecap="round" opacity=".75"/>
    """.format(a=a, b=b, c=c, stem=" ".join("%s=\"%s\"" % (k.replace("_", "-"), v) for k, v in stem.items()),
               thin=" ".join("%s=\"%s\"" % (k.replace("_", "-"), v) for k, v in thin.items()))


def marks_arabic(a, b, c):
    """A connected baseline with two bowls, a tall alif, and the dots that
    carry meaning in Arabic script. The tail sweeps in the reading direction."""
    return """
    <!-- alif: the straight stroke every Arabic page is measured against -->
    <path d="M288 398 V212" fill="none" stroke="{a}" stroke-width="18" stroke-linecap="round"/>
    <!-- connected baseline: two bowls, then a rising tail -->
    <path d="M166 398 q50 0 66 -32 q16 -32 56 -32 q40 0 56 32 q16 32 66 32 q40 0 60 -26"
          fill="none" stroke="{b}" stroke-width="16" stroke-linecap="round"/>
    <!-- i'jam: one dot above, two below — the shape that changes the letter -->
    <circle cx="288" cy="178" r="11" fill="{c}"/>
    <circle cx="216" cy="436" r="10" fill="{a}"/>
    <circle cx="250" cy="436" r="10" fill="{a}"/>
    <!-- the tail lifts: it is the same line, drawn from the right -->
    <path d="M436 386 q36 -4 54 -32" fill="none" stroke="{c}" stroke-width="13"
          stroke-linecap="round"/>
    """.format(a=a, b=b, c=c)


def marks_cjk(a, b, c):
    """三 / 十 / 日 / 田 — four tiles every CJK reader recognises, drawn on the
    strict grid the writing system is built on."""
    return """
    <g stroke-linecap="square" fill="none">
      <!-- 三 : three, counted in strokes -->
      <path d="M196 214 H300 M196 252 H300 M196 290 H300" stroke="{a}" stroke-width="15"/>
      <!-- 十 : ten, the cross -->
      <path d="M420 196 V326 M368 261 H472" stroke="{b}" stroke-width="15"/>
      <!-- 日 : the sun, framed -->
      <rect x="196" y="352" width="104" height="118" rx="4" stroke="{c}" stroke-width="13"/>
      <path d="M196 411 H300" stroke="{c}" stroke-width="11"/>
      <!-- 田 : the field, divided -->
      <rect x="366" y="352" width="106" height="118" rx="4" stroke="{a}" stroke-width="13"/>
      <path d="M419 352 V470 M366 411 H472" stroke="{a}" stroke-width="10"/>
    </g>
    """.format(a=a, b=b, c=c)


def marks_latin(a, b, c):
    """A baseline, a capital A and a lowercase a — the two heights every Latin
    text block is built from, with the x-height rule dashed in between."""
    return """
    <!-- baseline: the line everything stands on -->
    <path d="M176 408 H464" fill="none" stroke="{a}" stroke-width="12" stroke-linecap="round" opacity=".45"/>
    <!-- A : two diagonals and the crossbar that opens the counter -->
    <path d="M212 408 L272 244 L332 408" fill="none" stroke="{a}" stroke-width="18"
          stroke-linejoin="round" stroke-linecap="round"/>
    <path d="M238 344 H306" fill="none" stroke="{b}" stroke-width="13" stroke-linecap="round"/>
    <!-- a : the x-height letter, bowl plus stem -->
    <circle cx="410" cy="352" r="42" fill="none" stroke="{b}" stroke-width="16"/>
    <path d="M452 310 V408" fill="none" stroke="{c}" stroke-width="14" stroke-linecap="round"/>
    <!-- x-height rule, dashed: the invisible grid of a Latin page -->
    <path d="M186 292 H454" fill="none" stroke="{a}" stroke-width="5" stroke-linecap="round"
          stroke-dasharray="2 18" opacity=".55"/>
    """.format(a=a, b=b, c=c)


def marks_multi(a, b, c):
    """The one emblem that is not a single script: four marks, one per world,
    around a shared centre — what the courses hub actually is."""
    return """
    <g stroke-linecap="round" fill="none">
      <!-- top-left: the Devanagari headstroke and its stems -->
      <path d="M168 232 H272" stroke="{a}" stroke-width="13"/>
      <path d="M196 232 V278 M238 232 V298 H218" stroke="{a}" stroke-width="10"/>
      <circle cx="220" cy="202" r="7" fill="{c}" stroke="none"/>
      <!-- top-right: the Arabic baseline, read from the right -->
      <path d="M366 286 q28 -44 60 -18 q16 12 40 -6" stroke="{b}" stroke-width="13"/>
      <circle cx="404" cy="228" r="8" fill="{c}" stroke="none"/>
      <!-- bottom-left: the CJK grid -->
      <path d="M168 380 H274 M168 414 H274 M221 358 V444" stroke="{b}" stroke-width="11"/>
      <!-- bottom-right: the Latin A -->
      <path d="M368 444 L414 354 L460 444" stroke="{c}" stroke-width="13"/>
      <path d="M388 408 H440" stroke="{a}" stroke-width="10"/>
      <!-- the shared centre: what every script has in common -->
      <circle cx="318" cy="330" r="24" fill="none" stroke="{a}" stroke-width="11"/>
      <circle cx="318" cy="330" r="7" fill="{c}" stroke="none"/>
    </g>
    """.format(a=a, b=b, c=c)


MARK = {
    "devanagari": marks_devanagari,
    "arabic": marks_arabic,
    "cjk": marks_cjk,
    "latin": marks_latin,
    "multi": marks_multi,
}


def build_svg(code, palette):
    """Compose one emblem. Structure is identical across worlds so a page can
    swap the file and keep the same layout box."""
    a, b, c = palette
    family = FAMILY[code]
    dark = mix(a, "#10131f", 0.35)
    surface = mix(a, "#ffffff", 0.93)

    # 24 ticks around the rim: a compass, not a clock — no numbers.
    ticks = []
    for i in range(24):
        width = 3 if i % 2 else 5
        ticks.append(
            '<path d="M320 24 V%d" stroke="%s" stroke-width="%d" stroke-linecap="round" '
            'transform="rotate(%d 320 320)"/>'
            % (38 if i % 2 else 48, alpha(a, .30 if i % 2 else .45), width, i * 15)
        )

    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640" width="640" height="640"
     role="img" aria-labelledby="t">
  <title id="t">EkGuru world emblem — {family}</title>
  <defs>
    <radialGradient id="bg" cx="50%" cy="42%" r="62%">
      <stop offset="0" stop-color="{surface}"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{a}" stop-opacity=".55"/>
      <stop offset="1" stop-color="{b}" stop-opacity=".35"/>
    </linearGradient>
  </defs>

  <!-- The backdrop is a circle, not a square: on the dark heroes (support/,
       courses/) a square panel shows its corners and reads as a broken image. -->
  <circle cx="320" cy="320" r="288" fill="url(#bg)"/>
  <circle cx="320" cy="320" r="288" fill="{surface}" fill-opacity=".55"/>

  <!-- rim: dashed orbit, ticks, and the three study nodes -->
  <circle cx="320" cy="320" r="288" fill="none" stroke="{a}" stroke-opacity=".16"
          stroke-width="2" stroke-dasharray="10 14"/>
  <circle cx="320" cy="320" r="252" fill="none" stroke="url(#ring)" stroke-width="2"/>
  <g opacity=".8">{ticks}</g>

  <g class="eg-nodes">
    <circle cx="320" cy="76" r="13" fill="{c}"/>
    <circle cx="546" cy="466" r="10" fill="{b}"/>
    <circle cx="104" cy="446" r="9" fill="{a}"/>
  </g>

  {mark}

  <!-- the four corners carry the same motif the page background repeats -->
  <g opacity=".45" fill="none" stroke="{a}" stroke-width="3">
    <path d="M92 132 h34 M92 132 v34"/>
    <path d="M548 132 h-34 M548 132 v34"/>
    <path d="M92 508 h34 M92 508 v-34"/>
    <path d="M548 508 h-34 M548 508 v-34"/>
  </g>
</svg>
""".format(family=FAMILY_LABEL[family], surface=surface, a=a, b=b, c=c,
           ring_dark=dark, ticks="".join(ticks), mark=MARK[family](a, b, c))


def main():
    check = "--check" in sys.argv
    palettes = read_palettes()
    os.makedirs(OUT_DIR, exist_ok=True)

    stale = []
    for code in sorted(FAMILY):
        svg = build_svg(code, palettes[code])
        path = os.path.join(OUT_DIR, "world-%s.svg" % code)
        old = None
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                old = f.read()
        if old == svg:
            continue
        stale.append(path)
        if not check:
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg)
            print("wrote %s (%d bytes, %s palette %s)"
                  % (path, len(svg), FAMILY[code], palettes[code][0]))

    # The repository keeps a 2x social card and a favicon next to these; an
    # orphaned world-*.svg would silently ship forever.
    for name in sorted(os.listdir(OUT_DIR)):
        if name.startswith("world-") and name.endswith(".svg"):
            code = name[6:-4]
            if code not in FAMILY:
                print("WARN: %s/%s has no world definition" % (OUT_DIR, name))

    if check and stale:
        print("STALE: %s — run tools/build-world-art.py" % ", ".join(stale))
        return 1
    if not stale:
        print("world artwork already up to date (%d emblems)" % len(FAMILY))
    return 0


if __name__ == "__main__":
    sys.exit(main())

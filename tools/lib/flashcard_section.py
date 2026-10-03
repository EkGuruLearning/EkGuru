#!/usr/bin/env python3
"""Shared flashcard section for the practice labs (PHASE 9).

Every practice page gets the same block, built from the deck that
tools/build-flashcards.py already wrote for that language:

    <section class="fc-lab" data-eg-flashcards="<code>">
      <h2>…</h2>
      <p class="fc-note">…</p>
      <ul class="fc-static"> 12 real cards, rendered at build time  </ul>
      <p class="fc-static-note">…how many cards the deck has…</p>
      <noscript>…the honest no-JavaScript line…</noscript>
    </section>

WHY A STATIC LIST AS WELL
-------------------------
js/flashcard-ui.js replaces the section's contents with the interactive lab
when JavaScript runs. Until then — a slow connection, a crawler, a reader who
blocks scripts — the page still shows the language's own vocabulary, in the
language's own script. Nothing about the block is a promise the deck cannot
keep: the cards are the authored course vocabulary, the reading is the one the
course data already printed, and the note never claims native audio.

The section is skipped entirely for a language with no deck, so no page ever
links to a lab that cannot open.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_CARDS = 12
EMPTY = ("", [])


def _load(code):
    path = os.path.join(ROOT, "data", "flashcards", "%s.json" % code)
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def flashcard_section(code, name, script_name="", limit=STATIC_CARDS):
    """(html, scripts) for a language's flashcard block, or ("", []) if none.

    `limit` only bounds the static list; the deck file has the full set.
    """
    deck = _load(code)
    if not deck or not deck.get("cards"):
        return EMPTY

    cards = deck["cards"]
    lang_attr = html.escape(code)
    rid = "fc-h-%s" % html.escape(code)
    rtl = (deck.get("direction") or "ltr") == "rtl"
    rows = []
    for c in cards[:limit]:
        target = html.escape(c["t"])
        meaning = html.escape(c["en"])
        roman = (" · <span class=\"fc-roman\" dir=\"ltr\">%s</span>" % html.escape(c["r"])) if c.get("r") else ""
        # dir="auto" lets the word follow its own script (Arabic, Hebrew) while
        # the list itself stays in the page direction.
        rows.append("      <li><b lang=\"%s\" dir=\"auto\">%s</b>%s — %s</li>" % (lang_attr, target, roman, meaning))

    note = (
        "Front: the %s word, exactly as the course writes it. Back: its meaning and the "
        "reading the course prints. Nothing on this page is scored, and the computer voice "
        "is a device voice — not a native recording." % html.escape(name)
    )
    total = deck.get("total_available") or len(cards)
    if total > len(cards):
        static_note = (
            "This language's deck carries %d of the %d words the course authors, and the lab "
            "practises that deck. The lab shows one card at a time, flips on Enter or Space, "
            "moves with the arrow keys, and can save a card to your review queue." % (len(cards), total)
        )
    else:
        static_note = (
            "This language's published deck has %d cards. The interactive lab shows one card at "
            "a time, flips on Enter or Space, moves with the arrow keys, and can save a card to "
            "your review queue." % len(cards)
        )
    if script_name:
        static_note += " The written form is %s." % html.escape(script_name)

    block = (
        '<section class="fc-lab" data-eg-flashcards="%s" aria-labelledby="%s">\n'
        '  <h2 class="fc-title" id="%s">%s flashcards</h2>\n'
        '  <p class="fc-note">%s</p>\n'
        '  <ul class="fc-static">\n%s\n  </ul>\n'
        '  <p class="fc-static-note">%s</p>\n'
        '  <noscript><p class="fc-empty">The interactive flashcards need JavaScript. '
        'The vocabulary above is the same deck.</p></noscript>\n'
        '</section>\n'
    ) % (html.escape(code), rid, rid, html.escape(name), note, "\n".join(rows), static_note)

    scripts = ["flashcards-%s.js" % code, "flashcard-ui.js"]
    return block, scripts


def mount_script(code, name, speech):
    """The mount call every practice page gets, in one place so the wiring
    cannot drift between generators.

    Deferred scripts run in order *before* DOMContentLoaded, so waiting for
    that event is what guarantees the deck and the lab are both defined when
    mount() is called — no polling loop, no race.
    """
    return (
        '\n<script>\n'
        '  (function () {\n'
        '    function go() {\n'
        '      var el = document.querySelector("[data-eg-flashcards=\\"%s\\"]");\n'
        '      if (el && window.EkGuruFlashcards) {\n'
        '        window.EkGuruFlashcards.mount(el, {code:"%s", name:%s, speech:"%s"});\n'
        '      }\n'
        '    }\n'
        '    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", go);\n'
        '    else go();\n'
        '  })();\n'
        '</script>\n'
    ) % (
        code,
        code,
        json.dumps(name, ensure_ascii=False),
        speech,
    )

#!/usr/bin/env python3
"""Phase 6 §4/§5/§7 — tag key vocabulary for Listen (computer voice) + Add to Review.

Reuses the site's established speechSynthesis mechanism (hi-IN) via the new
shared js/hindi-audio.js, which mounts accessible Listen buttons for any
element carrying `data-hi-audio`. This tool only ADDS the data attributes to
vocab/phrases that already exist verbatim in each lesson (never invents text),
and the same element carries `data-hi-card` so js/hindi-srs.js can offer an
"Add to review" control.

Honest scoping (§4): buttons are added only to key vocabulary, example
sentences and useful phrases — not to every fragment. Individual letters of
the alphabet are deliberately NOT tagged (letter-by-letter TTS is misleading).

Run: python3 tools/build-hindi-audio.py
"""
import json, os, re, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# (devanagari, roman, meaning) — curated from each lesson's own content.
AUDIO = {
    "how-to-say-hello-in-hindi": [
        ("नमस्ते", "namaste", "hello / goodbye"),
        ("आप कैसे हैं?", "aap kaise hain?", "how are you? (formal, to a man)"),
        ("तुम कैसे हो?", "tum kaise ho?", "how are you? (informal)"),
        ("क्या हाल है?", "kya haal hai?", "how's it going? (casual)"),
        ("फिर मिलेंगे", "phir milenge", "we'll meet again"),
        ("अलविदा", "alvida", "goodbye (final)"),
    ],
    "hindi-numbers-1-to-100": [
        ("एक", "ek", "one"),
        ("दो", "do", "two"),
        ("तीन", "teen", "three"),
        ("सौ", "sau", "one hundred"),
        ("ग्यारह", "gyaarah", "eleven"),
    ],
    "hindi-days-months-time": [
        ("सोमवार", "somvaar", "Monday"),
        ("रविवार", "ravivaar", "Sunday"),
        ("ढाई", "dhai", "two and a half"),
        ("साढ़े", "saadhe", "half past"),
    ],
    "hindi-family-words": [
        ("चाचा", "chaacha", "father's younger brother"),
        ("मामा", "maama", "mother's brother"),
        ("दादा", "daada", "paternal grandfather"),
        ("नाना", "naana", "maternal grandfather"),
    ],
    "aap-tum-tu-hindi": [
        ("आप", "aap", "you (respectful)"),
        ("तुम", "tum", "you (familiar)"),
        ("तू", "tu", "you (intimate)"),
    ],
    "hindi-verbs-present-past-future": [
        ("करना", "karnaa", "to do"),
        ("होना", "honaa", "to be"),
        ("जाना", "jaanaa", "to go"),
        ("खाना", "khaanaa", "to eat"),
    ],
    "hindi-phrases-for-travel": [
        ("यह कितने का है?", "yah kitne ka hai?", "how much is this?"),
        ("धन्यवाद", "dhanyavaad", "thank you"),
        ("ठीक है", "theek hai", "okay / fine"),
    ],
    "hindi-gender-masculine-feminine": [
        ("लड़का", "ladkaa", "boy (masculine)"),
        ("लड़की", "ladkii", "girl (feminine)"),
    ],
}

SKIP = "hindi-alphabet-for-beginners"  # letters: TTS per letter is misleading


def esc_attr(s):
    """Escape for embedding inside a single-quoted HTML attribute value."""
    return s.replace("&", "&amp;").replace("'", "&#39;").replace("<", "&lt;")


def tag_attr(opening, attrs):
    """Add data-hi-audio + data-hi-card to an OPENING tag (<strong ...>)."""
    if "data-hi-audio" in opening:
        return opening  # already mounted
    return opening.rstrip(">") + attrs + ">"


def main():
    tagged = {}
    not_found = []
    for slug, items in AUDIO.items():
        path = os.path.join("learn", slug, "index.html")
        if not os.path.exists(path):
            not_found.append(slug + ":page-missing")
            continue
        html = open(path, encoding="utf-8").read()
        found_here = []
        for deva, roman, meaning in items:
            card = json.dumps({"p": deva, "a": roman + " — " + meaning},
                              ensure_ascii=False, separators=(",", ":"))
            attrs = ' data-hi-audio="%s" data-hi-card=\'%s\'' % (
                deva.replace("&", "&amp;").replace('"', "&quot;"), esc_attr(card))
            # opening tag captured separately; content may carry a roman gloss,
            # a meaning, and nested inline tags (e.g. <td>देव <em>roman</em></td>).
            # Restricted to inline/list/cell tags so we never tag a whole <p>.
            pat = re.compile(r'(<(td|th|strong|b|li|em|span|h2|h3)([^>]*)>)' +
                             re.escape(deva) + r'((?:(?!</\2>).)*?)</\2>')
            m = pat.search(html)
            if not m:
                not_found.append(slug + ":" + deva)
                continue
            opening = m.group(1)
            opening2 = tag_attr(opening, attrs)
            if opening2 != opening:
                html = html.replace(opening, opening2, 1)
                found_here.append(deva)
        if found_here:
            open(path, "w", encoding="utf-8").write(html)
            tagged[slug] = found_here

    report = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mechanism": "Web Speech API (speechSynthesis), lang hi-IN — reused from practice-engine.js",
        "labeling": "Listen (computer voice) — never 'native' or 'recorded'",
        "controls": ["play", "stop", "replay"],
        "autoplay": False,
        "fallback": "button replaced by 'Audio unavailable' note when speechSynthesis unsupported",
        "skippedLetters": SKIP + " (letter-by-letter TTS is misleading)",
        "lessonsTagged": tagged,
        "totalButtons": sum(len(v) for v in tagged.values()),
        "notFound": not_found,
    }
    with open("reports/hindi-audio-phase6.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("audio tagged: %d lessons, %d buttons" % (len(tagged), report["totalButtons"]))
    print("not found (skipped):", not_found or "none")


if __name__ == "__main__":
    main()

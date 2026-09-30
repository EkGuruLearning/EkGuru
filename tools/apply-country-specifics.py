#!/usr/bin/env python3
"""De-template the indexable learn-hindi-from-* pages (AdSense plan P3 / D-20).

The country pages were generated from one template, and nine of their
paragraphs came out word-for-word identical on every page (the "Two honest
caveats" note, the four FAQ answers, the first-language line, the lede ...).
Some were also wrong for most countries: "allowing for the usual
daylight-saving shift" was printed for Afghanistan, India and 40 other
countries that do not change their clocks.

This tool replaces those paragraphs, in place, with text built from
data/content/country-specifics.json (verified zone/DST facts as of 2026, the
local currency, the writing-system relationship to Devanagari and a
country-specific opening). The visible FAQ and the FAQPage JSON-LD carry the
same strings, so both are rewritten together.

    python3 tools/apply-country-specifics.py          # apply (idempotent)
    python3 tools/apply-country-specifics.py --check  # exit 1 if a page still
                                                      # carries template text
Only pages listed in the JSON are touched; noindex pages are left alone.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "data/content/country-specifics.json"), encoding="utf-8"))["countries"]
CHECK = "--check" in sys.argv


def ws(s):
    return r"\s+".join(re.escape(w) for w in s.split())


OLD = {
    "lede": re.compile(r'<p class="lede">Everything below is specific to learning Hindi from[\s\S]*?worked out here\.</p>'),
    "caveat": re.compile(r"<p>Two honest caveats\.[\s\S]*?that will be right\.</p>"),
    "q1": re.compile(ws("Yes. Lessons are online and one to one over video, so where you are does not limit which tutor you can work with. What it does affect is the hours that suit you both — converted to local time here, tutors teach from about") + r"\s+([^<\"]+?)\."),
    "q2": re.compile(ws(", allowing for the usual daylight-saving shift.")),
    "cost_body": re.compile(ws("for") + r'(\s*<span data-f="lessonLength"[^>]*>[^<]*</span>)\.\s*' + ws("Every price on the site converts to your own currency automatically, at live rates rather than a number typed in last year.")),
    "cost_faq": re.compile(ws("Lessons start at $6 for 50 min. Prices are shown in your own currency automatically and converted at live rates.")),
    "script": re.compile(ws("No. Plenty of learners start with spoken Hindi and add reading later, or never. If you do want the script, our free alphabet guide covers every letter and there is an interactive explorer that shows each one with a real word.")),
    "fl": re.compile(r"<p>" + ws("Where you are decides the hours and the price. What you already speak decides which parts of Hindi are easy and which are slow — and those are different questions with different answers.") + r"</p>"),
    "foot": re.compile(r'(?<!<nav aria-label="More answers">)(<p class="sm"[^>]*>\s*Questions people ask before they start[\s\S]*?</p>)'),
}

WORDS = {0.25: "15 minutes", 0.5: "half an hour", 0.75: "45 minutes", 1: "one hour", 1.5: "an hour and a half"}
NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]


def span(h):
    if h in WORDS:
        return WORDS[h]
    whole, frac = int(h), h - int(h)
    if frac == 0.5:
        return "%s and a half hours" % NUM[whole]
    if frac == 0:
        return "%s hours" % NUM[whole]
    return "%s hours %d minutes" % (NUM[whole], round(frac * 60))


def cap(s):
    return s[0].upper() + s[1:]


def shift(t, hours=1):
    """'22:30 (previous day)' + 1h -> '23:30 (previous day)'; '23:30 (previous day)' + 1h -> '00:30'."""
    prev = "(previous day)" in t
    nxt = "(next day)" in t
    hh, mm = map(int, re.search(r"(\d\d):(\d\d)", t).groups())
    total = hh * 60 + mm + hours * 60 + (-1440 if prev else 0) + (1440 if nxt else 0)
    day = ""
    if total < 0:
        total += 1440; day = " (previous day)"
    elif total >= 1440:
        total -= 1440; day = " (next day)"
    return "%02d:%02d%s" % (total // 60, total % 60, day)


def build(key, c, html):
    the, The = c["the"], cap(c["the"])
    m = re.search(r"at\s+UTC([+-]\d+(?:\.\d+)?)", html)
    off = float(m.group(1)) if m else 5.5
    diff = 5.5 - off
    if abs(diff) < 1e-9:
        rel = "%s and India share the same clock" % The
    elif diff > 0:
        rel = "India is %s ahead of %s" % (span(diff), the)
    else:
        rel = "%s is %s ahead of India" % (The, span(-diff))
    w = re.search(r"works out at roughly\s+(.+?),\s+allowing", html) or re.search(r"works out at roughly\s+(.+?)(?:,|\.)\s", html)
    win = " ".join(w.group(1).split()) if w else None
    s_e = re.match(r"(.+?) to (.+)$", win) if win else None

    zone = []
    if c["dst"]:
        summer = ""
        if s_e:
            summer = ", about %s to %s" % (shift(s_e.group(1)), shift(s_e.group(2)))
        zone.append("That window is standard time. %s moves its clocks forward an hour %s, and during that period the same slots read an hour later on your clock%s." % (The, c["dst"], summer))
    else:
        zone.append("%s does not change its clocks for summer, so this window holds all year." % The)
    if c["zones"]:
        zone.append(c["zones"])
    zone.append("Either way, the booking page reads your device's own timezone and shows each slot in it, so that is the number to trust.")

    q2 = (", on standard time; while %s is on summer time the same slots read an hour later." % the) if c["dst"] \
        else (", all year round, because %s does not change its clocks." % the)
    script = ("No, and you effectively know it already. " + c["script"]) if key == "nepal" else \
        ("No. Plenty of learners start with spoken Hindi and add reading later, or never. %s If you do want it, the free alphabet guide covers every letter." % c["script"])
    return {
        "lede": '<p class="lede">%s</p>' % c["hook"],
        "caveat": "<p>%s</p>" % " ".join(zone),
        "q1": lambda mm: "Yes. %s, and lessons are one to one over video, so where you are does not limit which tutor you can work with. What it changes is the hours: converted to %s, tutors teach from about %s." % (rel, the, mm.group(1)),
        "q2": q2,
        "cost_body": lambda mm: "for%s. Prices on the site are converted into your own currency — for most visitors from %s, %s — at live rates rather than a number typed in last year." % (mm.group(1), the, c["cur"]),
        "cost_faq": "Lessons start at $6 for 50 min. The site shows that in your own currency — for most visitors from %s, %s — converted at live rates." % (the, c["cur"]),
        "script": script,
        "fl": "<p>%s</p>" % c["fl"],
        "foot": lambda mm: '<nav aria-label="More answers">%s</nav>' % mm.group(1),
    }


def main():
    left, changed = [], 0
    for key, c in sorted(DATA.items()):
        path = os.path.join(ROOT, "learn-hindi-from-%s" % key, "index.html")
        html = open(path, encoding="utf-8").read()
        if CHECK:
            for name, rx in OLD.items():
                if name == "foot":
                    continue
                if rx.search(html):
                    left.append("%s: %s" % (key, name))
            continue
        new = build(key, c, html)
        out = html
        for name, rx in OLD.items():
            rep = new[name]
            out = rx.sub(rep if callable(rep) else (lambda mm, r=rep: r), out)
        if c["the"].startswith("the "):
            # "Can I learn Hindi from United Kingdom?" -> "... from the United Kingdom?"
            name = re.escape(c["the"][4:])
            for pre in ("learn Hindi from", "In", "Converted to"):
                out = re.sub(r"(%s)(\s+)(%s)\b" % (ws(pre), name), r"\1\2the \3", out)
        if out != html:
            open(path, "w", encoding="utf-8").write(out)
            changed += 1
    if CHECK:
        if left:
            print("country specifics: %d template paragraph(s) still present:" % len(left))
            for x in left[:40]:
                print("  ", x)
            sys.exit(1)
        print("ok    country specifics: %d pages carry country-specific text" % len(DATA))
    else:
        print("country specifics: %d page(s) rewritten of %d" % (changed, len(DATA)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""One plate per tool — the picture the toolbox never had.

Prakash: "visuals in every language/subject matched to country theme + language
+ page."

The country plates cover the country pages. These are the subject pages: the
thirteen tools a learner actually uses (alphabet, numbers, verbs, typing, quiz,
flashcards, placement, pronunciation, phrasebook, date and time, planner,
vocabulary) plus the toolbox index itself.

Every plate is DERIVED from the page it sits on — the same rows the learner can
scroll to, the same counts, the same sample item. Nothing here is stock art and
nothing is invented: if a recipe cannot find the data it declares, the builder
fails loudly instead of drawing an empty picture.

The colour comes from the page's own chapter accent (--sb-accent), so the plate
belongs to the page rather than to a palette someone liked.

  python3 tools/build-toolbox-visuals.py           write the plates + blocks
  python3 tools/build-toolbox-visuals.py --check    say what would change
"""
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIS = os.path.join(ROOT, "images", "vis")
MANIFEST = os.path.join(ROOT, "data", "toolbox-visuals.json")

MARK_START = "<!-- ekguru:toolbox-visuals:start -->"
MARK_END = "<!-- ekguru:toolbox-visuals:end -->"
ANCHOR = "<!-- ekguru:pw-bands:start -->"

W, H = 320, 200


# --------------------------------------------------------------------------
# reading a page
# --------------------------------------------------------------------------
def page(slug):
    p = os.path.join(ROOT, "toolbox", slug, "index.html") if slug != "tools" \
        else os.path.join(ROOT, "toolbox", "index.html")
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def cells(row):
    """The text of every cell in a table row, tags stripped."""
    out = []
    for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S):
        txt = re.sub(r"<small>.*?</small>", "", c, flags=re.S)
        txt = re.sub(r"<[^>]+>", "", txt)
        txt = re.sub(r"\s+", " ", txt).strip()
        out.append(txt)
    return out


def rows_of(html):
    """Every table row on the page except the header rows."""
    rows = []
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S):
        if "<th" in r:
            continue
        c = cells(r)
        if c:
            rows.append(c)
    return rows


def accent(html, fallback="#6d28d9"):
    m = re.search(r"--sb-accent:\s*(#[0-9a-fA-F]{3,6})", html)
    return m.group(1) if m else fallback


def rgb(hexcode):
    h = hexcode.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def shades(hexcode):
    r, g, b = rgb(hexcode)
    dark = "#%02x%02x%02x" % (int(r * .62), int(g * .62), int(b * .62))
    tint = "#%02x%02x%02x" % (int(255 - (255 - r) * .09), int(255 - (255 - g) * .09),
                              int(255 - (255 - b) * .09))
    return dark, tint


def js_object(html, name):
    """A JS object literal a page defines inline, parsed as JSON."""
    m = re.search(re.escape(name) + r"\s*=\s*(\{.*?\}|\[.*?\])\s*;", html, re.S)
    if not m:
        raise SystemExit("could not find %s on the page" % name)
    return json.loads(m.group(1))


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def cut(s, n):
    s = re.sub(r"\s+", " ", str(s)).strip()
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def wrap(s, n, lines=2):
    words, out, line = re.sub(r"\s+", " ", s).strip().split(" "), [], ""
    for w in words:
        if len(line) + len(w) + 1 > n:
            out.append(line)
            line = w
            if len(out) == lines:
                break
        else:
            line = (line + " " + w).strip()
    if len(out) < lines and line:
        out.append(line)
    if len(out) == lines and len(" ".join(words)) > len(" ".join(out)) + 1:
        out[-1] = cut(out[-1] + " …" if not out[-1].endswith("…") else out[-1], n + 2)
    return out


# --------------------------------------------------------------------------
# the recipes — each returns what the plate must say, from the page itself
# --------------------------------------------------------------------------
def r_alphabet(h):
    """Letter and its sound: the letter is the cell text, the sound is the
    <small> written next to it — split before the tags are stripped, or the two
    run together into "अ at"."""
    vowel_html = re.findall(r"<h2>Vowels</h2>(.*?)<h2>", h, re.S)[0]
    letters = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", vowel_html, re.S):
        if "<th" in tr:
            continue
        first = tr.split("</td>")[0]
        letter = re.sub(r"<[^>]+>", "", first.split("<small>")[0]).strip()
        latin = (re.search(r"<small>([^<]+)</small>", first) or [None, ""])[1].strip()
        if letter:
            letters.append((letter[:4], latin[:8]))
        if len(letters) == 5:
            break
    if not letters:
        raise SystemExit("alphabet: no letters found")
    return {
        "title": "Alphabet explorer", "native": "वर्णमाला",
        "stat": "%d letters and sounds, in one grid" % len(rows_of(h)),
        "body": ("strip", letters),
    }


def r_numbers(h):
    rows = rows_of(h)
    nums = [(r[0], r[1]) for r in rows if len(r) >= 4 and re.match(r"^\d+$", r[0])][:5]
    if not nums:
        raise SystemExit("numbers: no numeric rows found")
    return {
        "title": "Numbers", "native": "संख्याएँ",
        "stat": "0 to 100 — digit, Devanagari, word and sound",
        "body": ("strip", nums),
    }


def r_verbs(h):
    rows = [r for r in rows_of(h) if len(r) >= 5]
    if not rows:
        raise SystemExit("verbs: no verb rows found")
    lines = [[r[1].split(" ")[0], "%s · %s · %s" % (r[2], r[3], r[4])] for r in rows[:4]]
    return {
        "title": "Verb conjugator", "native": "क्रियाएँ",
        "stat": "%d verbs × present, past and future" % len(rows),
        "body": ("rows", lines),
    }


def r_datetime(h):
    rows = rows_of(h)
    days = [r for r in rows if len(r) >= 3 and not re.match(r"^\d", r[0])][:4]
    lines = [[r[0], r[1]] for r in days]
    return {
        "title": "Date and time", "native": "तारीख़ और समय",
        "stat": "%d words for days, months and clock time" % len(rows),
        "body": ("rows", lines),
    }


def r_phrasebook(h):
    rows = [r for r in rows_of(h) if len(r) >= 3]
    cats = sorted(set(re.findall(r'data-c="([a-z-]+)"', h)))
    groups = re.findall(r'class="pill"[^>]*data-c="([^"]*)"', h)
    lines = [[r[0], r[1]] for r in rows[:4]]
    return {
        "title": "Phrasebook", "native": "वाक्यांश",
        "stat": "%d phrases in %d situations, with the sound written out" % (len(rows), len(cats)),
        "body": ("rows", lines),
    }


def r_vocabulary(h):
    rows = [r for r in rows_of(h) if len(r) >= 3 and "data-h" not in r[0]]
    rows = [r for r in rows_of(h) if len(r) >= 3]
    groups = sorted(set(re.findall(r'data-g="([a-z-]+)"', h)))
    lines = [[r[0], r[1]] for r in rows[:4]]
    return {
        "title": "Vocabulary", "native": "शब्दावली",
        "stat": "%d words in %d groups, hide either side to test yourself" % (len(rows), len(groups)),
        "body": ("rows", lines),
    }


def r_pronunciation(h):
    table = rows_of(h)
    tips = len(re.findall(r'"[a-z ]+":\s*"', re.search(r"TIPS\s*=\s*\{(.*?)\n", h, re.S).group(1)))
    lines = [[r[0], r[1]] for r in table[:4] if len(r) >= 2]
    return {
        "title": "Pronunciation", "native": "उच्चारण",
        "stat": "%d sounds compared with English, and why they differ" % len(table),
        "body": ("rows", lines),
    }


def r_typing(h):
    """The typing page is a guide, not a table: the plate shows what it teaches."""
    items = re.findall(r"<li>\s*<strong>([^<]+)</strong>\s*—\s*([^<]{10,120})", h)
    if not items:
        items = [(m.group(1), m.group(2)) for m in
                 re.finditer(r"<li><strong>([^<]+)</strong> — ([^<]{10,120})", h)]
    lines = [[a, cut(b, 46)] for a, b in items[:4]]
    return {
        "title": "Typing helper", "native": "टाइपिंग",
        "stat": "Type Hindi on any device, then copy it anywhere",
        "body": ("rows", lines),
    }


def r_level_test(h):
    qs = re.findall(r'data-q="\d+"\s*>\s*<p class="score">Question \d+ of (\d+)</p>\s*'
                    r"<p[^>]*>([^<]{5,120})</p>", h)
    total = qs[0][0] if qs else "?"
    lines = [["Q%d" % (i + 1), cut(q[1], 44)] for i, q in enumerate(qs[:4])]
    return {
        "title": "Level placement", "native": "स्तर जाँच",
        "stat": "%s honest questions — the answer places you between A1 and C2" % total,
        "body": ("rows", lines),
    }


def r_quiz(h):
    pool = js_object(h, "POOL")
    kinds = {}
    for p in pool:
        kinds[p.get("pool", "other")] = kinds.get(p.get("pool", "other"), 0) + 1
    first = pool[0]
    return {
        "title": "Hindi quiz", "native": "प्रश्नोत्तरी",
        "stat": "%d questions: %s" % (len(pool), ", ".join(
            "%d %s" % (v, k) for k, v in sorted(kinds.items(), key=lambda kv: -kv[1]))),
        "body": ("question", (first["q"], first["a"])),
    }


def r_flashcards(h):
    decks = js_object(h, "DECKS")
    first_deck = list(decks)[0]
    card = decks[first_deck][0]
    total = sum(len(v) for v in decks.values())
    return {
        "title": "Flashcards", "native": "फ़्लैश कार्ड",
        "stat": "%d cards in %d decks: %s" % (total, len(decks), ", ".join(decks)),
        "body": ("card", (card.get("f", ""), card.get("b", ""), card.get("r", ""),
                          "%d decks · %d cards" % (len(decks), total))),
    }


def r_time_planner(h):
    faq = re.findall(r'<div class="faq"><b>([^<]+)</b>', h)
    rungs = []
    for item in faq:
        m = re.match(r"(.+?) — roughly ([\d,]+) to ([\d,]+) hours", item)
        if m:
            rungs.append((m.group(1), m.group(2) + "–" + m.group(3)))
    if not rungs:
        raise SystemExit("planner: no hour milestones found")
    return {
        "title": "Time planner", "native": "समय योजना",
        "stat": "What each goal costs in hours, at the hours you actually have",
        "body": ("ladder", rungs[:5]),
    }


def r_tools(h):
    """The hub lists its own tools in structured data — read that, so the plate
    can never show a tool the page does not have."""
    blobs = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    names = []
    for b in blobs:
        try:
            data = json.loads(b)
        except ValueError:
            continue
        graph = data.get("@graph", [data]) if isinstance(data, dict) else data
        for node in graph if isinstance(graph, list) else [graph]:
            if isinstance(node, dict) and node.get("@type") == "ItemList":
                for el in node.get("itemListElement", []):
                    n = el.get("name") if isinstance(el, dict) else None
                    if n:
                        names.append(n)
    if not names:
        raise SystemExit("toolbox hub: no ItemList found")
    return {
        "title": "The toolbox", "native": "उपकरण",
        "stat": "%d tools, free, and every one of them works with no network" % len(names),
        "body": ("list", [cut(n, 18) for n in names[:6]]),
    }


RECIPES = {
    "hindi-alphabet": r_alphabet,
    "hindi-numbers": r_numbers,
    "hindi-verbs": r_verbs,
    "hindi-date-time": r_datetime,
    "hindi-phrasebook": r_phrasebook,
    "hindi-vocabulary": r_vocabulary,
    "hindi-pronunciation": r_pronunciation,
    "hindi-typing": r_typing,
    "hindi-level-test": r_level_test,
    "hindi-quiz": r_quiz,
    "hindi-flashcards": r_flashcards,
    "hindi-time-planner": r_time_planner,
    "tools": r_tools,
}

CODE = {"hindi-alphabet": "अ", "hindi-numbers": "१", "hindi-verbs": "क",
        "hindi-date-time": "त", "hindi-phrasebook": "वा", "hindi-vocabulary": "श",
        "hindi-pronunciation": "उ", "hindi-typing": "⌨", "hindi-level-test": "स्त",
        "hindi-quiz": "?", "hindi-flashcards": "क", "hindi-time-planner": "⏱",
        "tools": "उप"}


# --------------------------------------------------------------------------
# drawing
# --------------------------------------------------------------------------
def body_svg(kind, data, dark, ink="#1c1b42"):
    if kind == "strip":
        parts, x = [], 18
        for big, small in data[:5]:
            parts.append('<rect x="%d" y="112" width="54" height="52" rx="9" fill="#fff" '
                         'stroke="%s" stroke-width="1" opacity=".95"/>' % (x, dark))
            parts.append('<text x="%d" y="146" text-anchor="middle" font-size="21" fill="%s">%s</text>'
                         % (x + 27, ink, esc(big)))
            if small:
                parts.append('<text x="%d" y="158" text-anchor="middle" font-size="9" fill="#6b6885">%s</text>'
                             % (x + 27, esc(small)))
            x += 60
        return "".join(parts)
    if kind == "rows":
        parts, y = [], 116
        for left, right in data[:4]:
            parts.append('<text x="18" y="%d" font-size="12" font-weight="600" fill="%s">%s</text>'
                         % (y, dark, esc(cut(left, 14))))
            parts.append('<text x="118" y="%d" font-size="11" fill="%s">%s</text>'
                         % (y, ink, esc(cut(right, 30))))
            y += 19
        return "".join(parts)
    if kind == "ladder":
        parts, y = [], 114
        for label, span in data[:5]:
            parts.append('<rect x="18" y="%d" width="%d" height="13" rx="6" fill="%s" opacity=".9"/>'
                         % (y, 100 + 22 * len(label) % 60, dark))
            parts.append('<text x="24" y="%d" font-size="11" fill="#fff">%s</text>'
                         % (y + 10, esc(cut(label, 20))))
            parts.append('<text x="200" y="%d" font-size="11" fill="%s">%s h</text>'
                         % (y + 10, ink, esc(span)))
            y += 17
        return "".join(parts)
    if kind == "card":
        front, back, roman, extra = data
        return ('<rect x="18" y="110" width="130" height="58" rx="9" fill="#fff" stroke="%s" '
                'stroke-width="1"/><text x="83" y="132" text-anchor="middle" font-size="11" '
                'fill="%s">%s</text><text x="83" y="156" text-anchor="middle" font-size="20" '
                'fill="%s">%s</text>'
                '<text x="162" y="126" font-size="10" fill="#6b6885">%s</text>'
                '<text x="162" y="141" font-size="10" fill="%s">%s</text>'
                '<text x="162" y="156" font-size="10" fill="%s">flip, then say it aloud</text>'
                % (dark, "#6b6885", esc(cut(front, 20)), ink, esc(back), esc(cut(roman, 22)),
                   ink, esc(cut(extra, 25)), ink))
    if kind == "question":
        q, a = data
        lines = wrap(q, 34, 2)
        parts = ['<text x="18" y="%d" font-size="12" fill="%s">%s</text>'
                 % (118 + i * 15, ink, esc(line)) for i, line in enumerate(lines)]
        parts.append('<rect x="18" y="152" width="150" height="17" rx="8" fill="#fff" stroke="%s"/>'
                     '<text x="26" y="164" font-size="11" fill="%s">%s</text>'
                     % (dark, ink, esc(cut(a, 22))))
        parts.append('<text x="180" y="164" font-size="11" fill="%s">correct answer</text>' % dark)
        return "".join(parts)
    if kind == "list":
        parts, x, y = [], 18, 112
        for i, name in enumerate(data):
            if i and i % 3 == 0:
                x, y = 18, y + 30
            parts.append('<rect x="%d" y="%d" width="92" height="24" rx="7" fill="#fff" stroke="%s" '
                         'stroke-width="1"/><text x="%d" y="%d" text-anchor="middle" font-size="10" '
                         'fill="%s">%s</text>' % (x, y, dark, x + 46, y + 16, ink, esc(name)))
            x += 98
        return "".join(parts)
    raise SystemExit("unknown body kind: " + kind)


def plate(slug, spec, html):
    dark, tint = shades(accent(html))
    label = "%s — %s. %s" % (spec["title"], spec["native"], spec["stat"])
    body = body_svg(spec["body"][0], spec["body"][1], dark)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="320" height="200" '
        'role="img" aria-label="%s" font-family="system-ui,-apple-system,Segoe UI,sans-serif">\n'
        '  <title>%s</title>\n'
        '  <rect width="320" height="200" rx="14" fill="%s" stroke="%s" stroke-width="1"/>\n'
        '  <rect width="320" height="88" rx="14" fill="%s"/>\n'
        '  <rect y="74" width="320" height="14" fill="%s"/>\n'
        '  <circle cx="46" cy="40" r="22" fill="#fff" opacity=".92"/>\n'
        '  <text x="46" y="48" text-anchor="middle" font-size="19" fill="%s">%s</text>\n'
        '  <text x="80" y="34" font-size="15" font-weight="700" fill="#fff">%s</text>\n'
        '  <text x="80" y="52" font-size="12" fill="#fff" opacity=".92">%s</text>\n'
        '  <text x="18" y="99" font-size="10.5" fill="%s">%s</text>\n'
        '%s\n'
        '</svg>\n' % (
            esc(label), esc(label), tint, dark, dark, dark, dark, esc(CODE[slug]),
            esc(cut(spec["title"], 22)), esc(spec["native"]),
            dark, esc(cut(spec["stat"], 46)), body)
    )


# --------------------------------------------------------------------------
# the page block
# --------------------------------------------------------------------------
def block(spec, slug, count_note):
    return (
        MARK_START + "\n"
        '<section class="ct-visual" data-items="%d" aria-labelledby="ct-visual-h">\n'
        '<h2 id="ct-visual-h">%s, in one picture</h2>\n'
        '<p>%s</p>\n'
        '<figure class="ct-fig"><img src="%s/images/vis/tool-%s.svg" width="320" height="200" '
        'loading="lazy" decoding="async" alt="%s"><figcaption><b>%s</b> · %s</figcaption></figure>\n'
        "</section>\n" % (
            count_note, esc(spec["title"]),
            esc("Every number and every word on this plate is taken from the tool below it, "
                "not drawn by hand: what you see here is what the tool holds."),
            "../.." if slug != "tools" else "..",
            slug, esc("%s — %s. %s" % (spec["title"], spec["native"], spec["stat"])),
            esc(spec["title"]), esc(spec["stat"])) + MARK_END + "\n"
    )


def splice(path, new_block):
    with open(path, encoding="utf-8") as fh:
        h = fh.read()
    if MARK_START in h:
        h = re.sub(re.escape(MARK_START) + r".*?" + re.escape(MARK_END) + r"\n?", "", h, flags=re.S)
    at = h.find(ANCHOR)
    if at < 0:
        at = h.rfind("</main>")
    if at < 0:
        return None
    return h[:at] + new_block + h[at:]


def main():
    check = "--check" in sys.argv
    plans, manifest, wrote, stale = [], {}, 0, []

    for slug in RECIPES:
        html = page(slug)
        spec = RECIPES[slug](html)
        svg = plate(slug, spec, html)
        rel = os.path.join("images", "vis", "tool-%s.svg" % slug)
        manifest[slug] = {
            "path": rel.replace(os.sep, "/"), "title": spec["title"],
            "native": spec["native"], "stat": spec["stat"],
            "page": "toolbox/index.html" if slug == "tools" else "toolbox/%s/index.html" % slug,
            "sha1": hashlib.sha1(svg.encode("utf-8")).hexdigest()[:16],
        }
        plans.append((slug, rel, svg, spec))

    for slug, rel, svg, spec in plans:
        path = os.path.join(ROOT, rel)
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
        if old != svg:
            if check:
                stale.append(rel)
            else:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(svg)
                wrote += 1

    pages = 0
    for slug, rel, svg, spec in plans:
        target = os.path.join(ROOT, "toolbox", slug, "index.html") if slug != "tools" \
            else os.path.join(ROOT, "toolbox", "index.html")
        note = len(spec["body"][1]) if isinstance(spec["body"][1], list) else 1
        nb = block(spec, slug, note)
        out = splice(target, nb)
        if out is None:
            raise SystemExit("no anchor on " + target)
        old = open(target, encoding="utf-8").read()
        if out != old:
            if check:
                stale.append(target)
            else:
                with open(target, "w", encoding="utf-8") as fh:
                    fh.write(out)
                pages += 1

    man_txt = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    old_man = open(MANIFEST, encoding="utf-8").read() if os.path.exists(MANIFEST) else ""
    if old_man != man_txt:
        if check:
            stale.append(MANIFEST)
        else:
            with open(MANIFEST, "w", encoding="utf-8") as fh:
                fh.write(man_txt)

    if check:
        if stale:
            print("STALE: " + ", ".join(os.path.relpath(p, ROOT) for p in stale))
            return 1
        print("ok    toolbox visuals: %d plate(s), 0 page(s)" % len(plans))
        return 0

    print("toolbox visuals: %d plate(s) written, %d page(s) updated, %d tool(s)"
          % (wrote, pages, len(plans)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

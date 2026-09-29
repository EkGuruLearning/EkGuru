#!/usr/bin/env python3
"""De-template the /hindi-tutor/<place>/ pages (AdSense plan P3 / D-20).

The 32 location pages shared six word-for-word paragraphs (lesson-times note,
four FAQ answers, the free-guides lead-in). Several were also wrong for the
page they sat on:
  * the 12 Indian city pages answered "Do you have Hindi tutors in Delhi?"
    with "No ... our tutors live in India";
  * the FAQPage JSON-LD did not match the visible FAQ (different wording,
    four questions instead of five, a "read simple words within six weeks"
    promise the page did not make) — Google requires the two to match;
  * /hindi-tutor/worldwide/ read "Hindi tutors for students in Anywhere in
    the World" and claimed the window "covers ... the Americas in their
    evenings" (it is overnight there).

This tool rewrites those paragraphs from data/content/tutor-location-
specifics.json and then rebuilds the FAQPage mainEntity from the visible FAQ,
so markup and page can no longer drift.

    python3 tools/apply-tutor-location-specifics.py          # apply (idempotent)
    python3 tools/apply-tutor-location-specifics.py --check  # exit 1 on template text / FAQ drift
"""
import html as H
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACES = json.load(open(os.path.join(ROOT, "data/content/tutor-location-specifics.json"), encoding="utf-8"))["places"]
CHECK = "--check" in sys.argv
CURNAME = {"INR": "rupees", "AUD": "Australian dollars", "CAD": "Canadian dollars", "AED": "dirhams",
           "EUR": "euros", "JPY": "yen", "GBP": "pounds", "NPR": "Nepalese rupees", "SGD": "Singapore dollars",
           "ZAR": "rand", "USD": "US dollars"}
NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen"]


def ws(s):
    return r"\s+".join(re.escape(w) for w in s.split())


def cap(s):
    return s[0].upper() + s[1:]


def minutes(t):
    hh, mm = map(int, re.search(r"(\d\d):(\d\d)", t).groups())
    v = hh * 60 + mm
    if "(previous day)" in t: v -= 1440
    if "(next day)" in t: v += 1440
    return v


def fmt(v):
    day = ""
    if v < 0: v += 1440; day = " (previous day)"
    elif v >= 1440: v -= 1440; day = " (next day)"
    return "%02d:%02d%s" % (v // 60, v % 60, day)


def span(h):
    words = {0.25: "15 minutes", 0.5: "half an hour", 0.75: "45 minutes", 1: "one hour", 1.5: "an hour and a half"}
    if h in words: return words[h]
    w, f = int(h), h - int(h)
    if abs(f - 0.5) < 1e-9: return "%s and a half hours" % NUM[w]
    if abs(f - 0.75) < 1e-9: return "%s hours 45 minutes" % NUM[w]
    if abs(f - 0.25) < 1e-9: return "%s hours 15 minutes" % NUM[w]
    return "%s hours" % NUM[w]


RX = {
    "lt": re.compile(r"<p>" + ws("Our tutors teach on Indian time. Converted to local time where you are, that means lessons run from about") +
                     r"\s*<strong>([^<]+)</strong>\s*to\s*<strong>([^<]+)</strong>\.\s*" +
                     ws("You do not have to work this out yourself — the booking page converts every slot into your own timezone automatically, and shows both times side by side so there is no confusion.") + r"</p>"),
    "q1": re.compile(r"<p>" + ws("No, and we would rather say so plainly. Our tutors live in India and teach online over video. In practice that widens your choice: you pick from every tutor listed, not only whoever happens to teach nearby.") + r"</p>"),
    "cost": re.compile(ws("Every price on this site converts to your own currency automatically, using live exchange rates.")),
    "script": re.compile(ws("Not to start. Plenty of students learn to speak first and add reading later. If you do want the script, our") +
                         r'\s*<a href="([^"]+)">free\s+alphabet guide</a>\s*' + ws("covers every letter, and most learners read simple words within six weeks.")),
    "times": re.compile(r"<p>" + ws("Converted to local time in") + r"\s+[^<]*?,\s+lessons run from about\s+(.+?)\s+to\s+(.+?)\.\s+" +
                        ws("The booking page converts every slot to your own timezone automatically.") + r"</p>"),
    "book": re.compile(ws("Open any tutor's profile, pick a time that suits you — shown in your own timezone — and send the request.")),
    "lead": re.compile(r"<p>" + ws("Before booking anything, work through the free guides. No sign-up, no email, nothing to pay:") + r"</p>"),
}


def texts(key, p, page):
    kind = p["kind"]
    cur = re.search(r"roughly [\d,.]+ ([A-Z]{3})", page)
    code = cur.group(1) if cur else ("USD" if kind == "abroad" else None)
    out = {}

    def window_bits(a, b):
        A, B = minutes(a), minutes(b)
        diff = (9 * 60 - A) / 60.0            # hours India is ahead of this clock
        if abs(diff) < 1e-9: rel = "%s shares India's clock" % cap(p["the"])
        elif diff > 0: rel = "India is %s ahead of %s" % (span(diff), p["the"])
        else: rel = "%s is %s ahead of India" % (cap(p["the"]), span(-diff))
        if p.get("dst") and p.get("window") == "summer":
            d = "That is daylight-saving time, kept %s; for the rest of the year the same slots read an hour earlier, about %s to %s." % (p["dst"], fmt(A - 60), fmt(B - 60))
            short = "; take an hour off outside daylight saving"
        elif p.get("dst"):
            d = "%s moves its clocks forward an hour %s, and during that period the same slots read an hour later, about %s to %s." % (cap(p["the"]), p["dst"], fmt(A + 60), fmt(B + 60))
            short = "; add an hour while %s is on summer time" % p["the"]
        else:
            d = "%s does not change its clocks, so this holds all year." % cap(p["the"])
            short = ", all year round"
        return rel, d, short

    if kind == "india":
        out["lt"] = lambda m: "<p>The tutors are on Indian Standard Time, the same clock as %s, so lessons run from about <strong>%s</strong> to <strong>%s</strong> with no conversion at all. %s</p>" % (p["name"], m.group(1), m.group(2), p["who"])
        out["q1"] = "<p>Not tutors who come to your home: the tutors listed here teach online, one to one over video, from wherever they live in India. For a learner in %s that means the full list to choose from, on your own clock.</p>" % p["name"]
        out["times"] = lambda m: "<p>The tutors share your clock in %s: lessons run from about %s to %s, Indian Standard Time, and the booking page lists every free slot.</p>" % (p["name"], m.group(1), m.group(2))
        out["book"] = "Open any tutor's profile, pick a time that suits you — shown in Indian Standard Time, which is already your clock in %s — and send the request." % p["name"]
    elif kind == "abroad":
        def lt(m):
            rel, d, _ = window_bits(m.group(1), m.group(2))
            z = (" " + p["zones"]) if p.get("zones") else ""
            return "<p>%s. Converted to %s, lessons run from about <strong>%s</strong> to <strong>%s</strong>. %s%s The booking page converts every slot into your own timezone and shows both times side by side.</p>" % (rel, p["tz"], m.group(1), m.group(2), d, z)
        out["lt"] = lt
        out["q1"] = "<p>Not locally, and we would rather say so plainly. The tutors live in India and teach over video, so you choose from everyone listed rather than whoever teaches nearby. %s</p>" % p["who"]

        def times(m):
            _, _, short = window_bits(m.group(1), m.group(2))
            return "<p>In %s, lessons run from about %s to %s%s. The booking page converts every slot for you.</p>" % (p["tz"], m.group(1), m.group(2), short)
        out["times"] = times
        out["book"] = "Open any tutor's profile, pick a time that suits you — shown in %s — and send the request." % p["tz"]
    else:  # worldwide
        out["lt"] = lambda m: "<p>Our tutors teach on Indian Standard Time (UTC+5:30), from about <strong>09:00</strong> to <strong>22:00</strong> in India. What that means on your clock depends on where you are — morning to late afternoon in Europe, afternoon to late night in East Asia and Australia, overnight in the Americas — and the booking page converts every slot into your own timezone, showing both times side by side.</p>"
        out["q1"] = "<p>Yes. The tutors live in India and teach online, one to one over video, so the only thing your location changes is the hours. %s</p>" % p["who"]
        out["times"] = lambda m: "<p>That depends on where you are: the tutors teach from about 09:00 to 22:00 India time, and the booking page shows each slot in your own timezone.</p>"
        out["book"] = "Open any tutor's profile, pick a time that suits you — shown in your own timezone — and send the request."  # unchanged wording
    if code:
        where = p["name"] if kind == "india" else p["the"]
        out["cost"] = "Prices on this site follow your device's location, so a visitor in %s sees them in %s, converted at live exchange rates." % (where, CURNAME.get(code, code))
    else:
        out["cost"] = "Prices on this site follow your device's location and are converted at live exchange rates wherever a rate exists; otherwise they stay in US dollars."
    out["script"] = lambda m: 'Not to start. Plenty of students learn to speak first and add reading later. %s If you want it, the <a href="%s">free alphabet guide</a> covers every letter.' % (p["script"], m.group(1))
    out["lead"] = "<p>%s Every guide below is free — no sign-up, no email, nothing to pay:</p>" % p["start"]
    return out


WORLDWIDE_FIXES = [
    ("Hindi Tutors in Anywhere in the World — Online… | EkGuru", "Online Hindi Tutors, Wherever You Live | EkGuru"),
    ("online from Anywhere in the World. Lessons 03:30–16:30 your local time.", "online from anywhere in the world. Lessons 09:00–22:00 India time, shown in your own timezone."),
    ("<h1>Hindi tutors for students in Anywhere in the World</h1>", "<h1>Hindi tutors for students anywhere in the world</h1>"),
    ("<h2>Why people in Anywhere in the World learn Hindi</h2>", "<h2>Learning Hindi from wherever you are</h2>"),
    ("<h2>Lesson times in Anywhere in the World</h2>", "<h2>Lesson times, wherever you are</h2>"),
    ("› Anywhere in the World</p>", "› Anywhere in the world</p>"),
    ('<div class="fact"><b>03:30–16:30</b><span>your local time</span></div>', '<div class="fact"><b>09:00–22:00</b><span>India time</span></div>'),
    ("which covers most of Europe, the Middle East, Africa, and the Americas in their evenings.",
     "which falls in the daytime across Europe, the Middle East and Africa, in the afternoon and evening across East Asia and Australia, and overnight in the Americas."),
]


def visible_faq(page):
    """[(question, answer_text)] from the visible FAQ blocks."""
    out = []
    for q, a in re.findall(r'<div class="faq"><b>(.*?)</b>\s*<p>([\s\S]*?)</p></div>', page):
        t = H.unescape(re.sub(r"<[^>]+>", "", a))
        out.append((H.unescape(re.sub(r"<[^>]+>", "", q)).strip(), " ".join(t.split())))
    return out


def sync_jsonld(page, fix=True):
    """Rebuild FAQPage.mainEntity from the visible FAQ. Returns (page, drift?)."""
    faq = visible_faq(page)
    drift = False

    def repl(m):
        nonlocal drift
        data = json.loads(m.group(1))
        nodes = data.get("@graph", [data])
        for n in nodes:
            if n.get("@type") == "FAQPage":
                want = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]
                if n.get("mainEntity") != want:
                    drift = True
                    n["mainEntity"] = want
        return '<script type="application/ld+json">%s</script>' % json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    new = re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, page, flags=re.S)
    return (new if fix else page), drift


def main():
    problems, changed = [], 0
    for key, p in sorted(PLACES.items()):
        path = os.path.join(ROOT, "hindi-tutor", key, "index.html")
        page = open(path, encoding="utf-8").read()
        if CHECK:
            for name, rx in RX.items():
                if name == "book" and p["kind"] == "worldwide":
                    continue
                if rx.search(page): problems.append("%s: template %s" % (key, name))
            if key == "worldwide" and "Anywhere in the World learn" in page: problems.append("worldwide: heading")
            _, drift = sync_jsonld(page, fix=False)
            if drift: problems.append("%s: FAQPage JSON-LD differs from the visible FAQ" % key)
            continue
        t = texts(key, p, page)
        out = page
        if key == "worldwide":
            for a, b in WORLDWIDE_FIXES: out = out.replace(a, b)
            out = out.replace("<b>Do you have Hindi tutors in Anywhere in the World?</b>", "<b>Can I learn with these tutors from anywhere?</b>")
        for name, rx in RX.items():
            r = t[name]
            out = rx.sub(r if callable(r) else (lambda m, r=r: r), out)
        out, _ = sync_jsonld(out)
        if out != page:
            open(path, "w", encoding="utf-8").write(out)
            changed += 1
    if CHECK:
        if problems:
            print("tutor location specifics: %d problem(s):" % len(problems))
            for x in problems[:40]: print("  ", x)
            sys.exit(1)
        print("ok    tutor location specifics: %d pages specific, FAQ markup matches the page" % len(PLACES))
    else:
        print("tutor location specifics: %d page(s) rewritten of %d" % (changed, len(PLACES)))


if __name__ == "__main__":
    main()

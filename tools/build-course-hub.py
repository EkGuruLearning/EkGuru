#!/usr/bin/env python3
"""Structured course setup — writes the static course hub and the home teaser.

WHAT PROBLEM THIS SOLVES
------------------------
/courses/ was a JavaScript shell: <div data-course-player> containing a loading
skeleton. A crawler, a slow connection or a visitor with JS disabled saw
"Loading your worldwide course library…" and nothing else — on the page that is
supposed to be the structured entry point to 39 language courses.

The interactive player (js/course-player.js) is good at what it does — search,
country context, progress, voice — but it must not be the ONLY way the page
exists. So this tool writes the same catalogue as real HTML first:

  · hero with the true counts (courses, levels, lessons, tests)
  · one section per phase, each course a real <a> to its course page
  · the A1→C2 ladder explained
  · an ItemList JSON-LD block describing the catalogue

The player replaces that markup on load, so nobody sees it twice; anyone who
never runs JS gets a complete, crawlable page instead of a spinner.

Also writes the home-page teaser (same data, six courses + a link to the hub)
between its markers.

SOURCES OF TRUTH
  data/courses/index.json                     which courses exist
  data/global/language-country-relations.json native name, script, countries

Run:  python3 tools/build-course-hub.py [--check]
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

CATALOGUE = "data/courses/index.json"
RELATIONS = "data/global/language-country-relations.json"
HUB = "courses/index.html"
HOME = "index.html"

HUB_START = "<!-- ekguru:course-hub:start -->"
HUB_END = "<!-- ekguru:course-hub:end -->"
HOME_START = "<!-- ekguru:home-courses:start -->"
HOME_END = "<!-- ekguru:home-courses:end -->"

LEVEL_NAMES = {
    "A1": "Beginner", "A2": "Elementary", "B1": "Intermediate",
    "B2": "Upper intermediate", "C1": "Advanced", "C2": "Mastery",
}

PHASE_TITLES = {
    "phase-1": "Collection I — first release",
    "phase-2": "Collection II — second release",
    "phase-3": "Collection III — worldwide release",
}


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


# The catalogue is keyed by ISO 639-1 ("ar", "zh"), and most relation rows
# carry iso_639_1 too — but six languages only appear under their ISO 639-3
# id. Without this bridge their cards lost the native name and the country
# count and printed the English name twice (Arabic read "Arabic / Arabic").
# ISO 3166-1 alpha-2 → English name. tools/_countries-cache.json is the copy
# the repo already carries (used by the phase-7 registries), so country names
# on the course cards come from data, not from a list typed into this file.
COUNTRIES_CACHE = "tools/_countries-cache.json"


def country_names():
    try:
        with open(COUNTRIES_CACHE, encoding="utf-8") as f:
            return {c["cca2"]: (c.get("name") or {}).get("common") or c["cca2"]
                    for c in json.load(f) if c.get("cca2")}
    except Exception:
        return {}


ISO3_ALIAS = {
    "arb": "ar",     # Standard Arabic
    "cmn": "zh",     # Mandarin
    "fil": "fil",    # Filipino
    "npi": "npi",    # Nepali
    "uzn": "uzn",    # Northern Uzbek
    "zsm": "zsm",    # Standard Malay
}


def load():
    with open(CATALOGUE, encoding="utf-8") as f:
        data = json.load(f)
    courses = data.get("courses", [])
    levels = data.get("levels", ["A1", "A2", "B1", "B2", "C1", "C2"])

    meta = {}
    try:
        with open(RELATIONS, encoding="utf-8") as f:
            rel = json.load(f).get("relations", [])
    except Exception:
        rel = []
    for row in rel:
        code = row.get("iso_639_1") or ISO3_ALIAS.get(row.get("iso_639_3") or "")
        if not code:
            continue
        entry = meta.setdefault(code, {"native": "", "script": "", "countries": set()})
        if row.get("native_name") and not entry["native"]:
            entry["native"] = row["native_name"]
        if row.get("script") and not entry["script"]:
            entry["script"] = row["script"]
        if row.get("country_id"):
            entry["countries"].add(row["country_id"])
    return courses, levels, meta


def course_href(code, levels):
    """Prefer a pre-rendered page over the player route, always.

    The card used to fall back to `/courses/#/<code>` for every language with no
    `languages/<code>/course/` directory — which, since
    tools/build-course-levels.py, means eleven languages whose whole course (six
    levels, every lesson, every practice question and answer) is real HTML at
    `languages/<code>/level/`. A hash route is not a page: the card sent a
    crawler, and a reader without JavaScript, to a spinner when a complete
    course page existed. The player route is the last resort, not the first."""
    if os.path.isdir(os.path.join("languages", code, "course")):
        return "/languages/%s/course/" % code
    if os.path.isdir(os.path.join("learn", code)):
        return "/learn/%s/" % code
    if os.path.exists(os.path.join("languages", code, "level", "index.html")):
        return "/languages/%s/level/" % code
    return "/courses/#/%s" % code


def hue_for(code):
    """Stable per-language hue — the player uses the same idea, so the static
    card and the interactive card are the same colour."""
    return sum(ord(c) for c in code) * 37 % 360


def counts(courses, levels):
    lessons = 0
    tests = 0
    for c in courses:
        for lv in levels:
            info = (c.get("levels") or {}).get(lv) or {}
            lessons += int(info.get("lessons") or 0)
            tests += int(info.get("test_items") or 0)
    return lessons, tests


def card(course, levels, meta, deep_prefix="..", names=None):
    code = course["code"]
    name = course["name"]
    lv = sorted(course.get("levels") or {}, key=lambda x: levels.index(x) if x in levels else 99)
    info = meta.get(code, {})
    native = info.get("native") or ""
    names = names or {}
    codes = sorted(info.get("countries") or [])
    countries = len(codes)
    # Named, not counted. "30 country contexts" told a reader nothing and told
    # a search engine less; the four biggest are the ones people look for
    # (India · United States · United Arab Emirates · +26 more).
    named = [names.get(c, c) for c in codes]
    named.sort()
    href = course_href(code, levels)
    if href.startswith("/"):
        # /courses/ links a page up (deep_prefix ".."); the home page sits at
        # the site root, so it links relatively — a leading slash breaks any
        # preview served from a sub-directory.
        href = deep_prefix.rstrip("/") + href if deep_prefix else href[1:]
    monogram = (native or name)[:2]
    lvline = " · ".join(lv) if lv else "A1–C2"
    # The native name is a real translation aid when it differs from the
    # English name ("español" under "Spanish") and useless noise when it does
    # not ("Filipino" under "Filipino"), so it is only emitted when it adds
    # something — and with the language tag the screen reader needs.
    native_line = ('<span class="native-name" lang="%s" dir="auto">%s</span>'
                   % (esc(code), esc(native))
                   if native and native.strip().lower() != name.strip().lower()
                   else "")
    return (
        '<article class="card course-card" style="--course-hue:{hue}" data-code="{code}" data-countries="{country_attr}">'
        '<a class="course-link" href="{href}" aria-label="Open the {name} course">'
        '<span class="course-monogram" aria-hidden="true">{mono}</span>'
        '<span class="course-copy">'
        '<b>{name}</b>'
        '{native_line}'
        '<span class="sub">{lvline} · {n} lessons</span>'
        '<span class="country-chips">{chips}</span>'
        "</span>"
        '<span class="course-arrow" aria-hidden="true">→</span>'
        "</a></article>"
    ).format(
        hue=hue_for(code), code=esc(code), href=esc(href), name=esc(name),
        mono=esc(monogram), native_line=native_line,
        lvline=esc(lvline), n=6 * len(lv) if lv else 24,
        chips=("".join("<em>%s</em>" % esc(x) for x in named[:4]) +
               ("<em>+%d more</em>" % (countries - 4) if countries > 4 else "")
               if countries else "<em>documented</em>"),
        country_attr=esc(" ".join(codes)),
    )


def build_hub(courses, levels, meta, names=None):
    lessons, tests = counts(courses, levels)
    # Countries the COURSES cover — not every country in the inventory. The
    # hero used to count every country any language is documented in, which
    # overstates what a visitor can actually learn today.
    countries_with_courses = {c for course in courses
                              for c in (meta.get(course["code"], {}).get("countries") or [])}
    by_phase = {}
    for c in courses:
        by_phase.setdefault(c.get("phase") or "phase-3", []).append(c)

    out = []
    out.append(HUB_START)
    out.append(
        '<!-- Static course catalogue. Written by tools/build-course-hub.py;\n'
        "     js/course-player.js replaces this with the interactive hub on load.\n"
        "     A crawler, and anyone with JS off, gets the whole catalogue. -->"
    )
    out.append('<div class="course-static">')

    out.append(
        '<section class="course-hero">'
        # The world emblem (images/xp/world-multi.svg, built by
        # tools/build-world-art.py). Four scripts around one centre — the
        # honest picture of a hub that teaches 39 languages. Decorative, so
        # alt is empty; data-xp-world="multi" fixes it to this world and
        # stops js/experience.js swapping it for a single market's emblem.
        '<img class="xp-world xp-world-herochip" data-xp-world="multi" '
        'src="../images/xp/world-multi.svg" alt="" aria-hidden="true" '
        'width="430" height="430" loading="lazy" decoding="async">'
        '<span class="pill">Worldwide · A1–C2 · free</span>'
        "<h1>Choose your language journey</h1>"
        "<p>One complete learning space for courses, country contexts, lessons, deep "
        "practice, review history and level tests. Every course below is free, runs in "
        "your browser and keeps its progress on your own device. "
        "Not sure which language? <a href=\"../courses/by-country/\"><b>Browse courses by "
        "country</b></a> — %d countries, each with the languages we can teach for it.</p>"
        '<div class="course-hero-stats">'
        "<span><b>%d</b> languages</span>"
        "<span><b>6</b> levels each</span>"
        "<span><b>%d</b> lessons</span>"
        "<span><b>%d</b> test items</span>"
        "<span><b>%d</b> country contexts</span>"
        "</div>"
        '<div class="course-orbit" aria-hidden="true"><i>अ</i><i>Α</i><i>ع</i><i>あ</i><i>മ</i></div>'
        "</section>" % (
            len(countries_with_courses),        # the sentence in the lede
            len(courses), lessons, tests,
            len(countries_with_courses),        # the stat
        )
    )

    out.append(
        '<section class="xp-sec" style="padding-block-start:0">'
        '<div class="xp-head" style="text-align:start;margin-inline:0">'
        "<h2>How a course is built</h2>"
        "<p>Six levels, six lessons per level, and a test that unlocks the next step.</p>"
        "</div>"
        '<div class="xp-grid xp-grid-3 xp-stagger">'
        '<div class="xp-card"><div class="xp-card-ico" aria-hidden="true">🔤</div>'
        "<h3>Start with the script</h3><p>A1 opens with the alphabet and counting — "
        "each letter with its sound, its romanisation and stroke order to copy.</p></div>"
        '<div class="xp-card"><div class="xp-card-ico" aria-hidden="true">🗣️</div>'
        "<h3>Say it from lesson one</h3><p>Vocabulary and dialogue carry a romanisation "
        "on every line, so a total beginner can speak before they can read.</p></div>"
        '<div class="xp-card"><div class="xp-card-ico" aria-hidden="true">🧪</div>'
        "<h3>Then prove it</h3><p>Five or more practice types per lesson, a worksheet, "
        "and a ten-item level test before the next level opens.</p></div>"
        "</div></section>"
    )

    for phase in sorted(by_phase):
        rows = by_phase[phase]
        out.append(
            '<section class="course-phase" id="%s"><h2>%s</h2>'
            '<div class="grid course-grid course-cards">%s</div></section>' % (
                esc(phase), esc(PHASE_TITLES.get(phase, phase.title())),
                "".join(card(c, levels, meta, names=names) for c in rows),
            )
        )

    out.append(
        '<section class="xp-sec">'
        '<div class="xp-head"><h2>The A1 → C2 ladder</h2>'
        "<p>Each course runs the same six steps, because the steps are what make a "
        "language stick: words first, then sentences, then real conversation.</p>"
        '<div class="xp-rule" aria-hidden="true"></div></div>'
        '<div class="xp-grid xp-grid-3 xp-stagger">%s</div></section>' % "".join(
            '<div class="xp-step"><b>%s · %s</b><p>%s</p></div>' % (
                lv, LEVEL_NAMES[lv], desc
            ) for lv, desc in (
                ("A1", "Alphabet, sounds, numbers and 200 core words — the level where "
                       "you stop being a stranger to the language."),
                ("A2", "Everyday sentences: family, food, shopping, travel, and the "
                       "present and past tenses that carry them."),
                ("B1", "Real conversation. Opinions, plans, complaints and stories — "
                       "with listening practice at natural speed."),
                ("B2", "Longer texts, subordinate clauses and register. You read a news "
                       "paragraph and summarise it in your own words."),
                ("C1", "Nuance: idioms, implied meaning, argument and style. Idiom "
                       "interpretation and discourse ordering start here."),
                ("C2", "Mastery work — paraphrase, guided composition and style rewriting, "
                       "measured against the level test."),
            )
        )
    )

    out.append(
        '<section class="xp-sec soft">'
        '<div class="xp-head"><h2>Pick by purpose, not just by name</h2>'
        "<p>Whatever brought you here, there is a route that starts today.</p></div>"
        '<div class="xp-grid xp-grid-3 xp-stagger">'
        '<a class="xp-card" href="/start/"><div class="xp-card-ico" aria-hidden="true">🧭</div>'
        "<h3>Find my level</h3><p>Five questions, then a starting point — so you are not "
        "re-reading A1 when you already speak.</p>"
        '<span class="xp-card-link">Take the placement</span></a>'
        '<a class="xp-card" href="/learn/practice/"><div class="xp-card-ico" aria-hidden="true">🎯</div>'
        "<h3>Practice labs</h3><p>Drills for the parts that need repetition: script, "
        "numbers, postpositions, verb endings.</p>"
        '<span class="xp-card-link">Open the labs</span></a>'
        '<a class="xp-card" href="/materials/"><div class="xp-card-ico" aria-hidden="true">🖨️</div>'
        "<h3>Worksheets</h3><p>Printable sheets and charts to take away from the screen — "
        "alphabet charts, grammar tables, word lists.</p>"
        '<span class="xp-card-link">See materials</span></a>'
        "</div></section>"
    )

    out.append("</div>")

    # ItemList — tells a search engine this page IS the catalogue.
    items = []
    for i, c in enumerate(courses, 1):
        href = course_href(c["code"], levels)
        if href.startswith("/"):
            href = "https://ekguru.shop" + href
        items.append({
            "@type": "ListItem",
            "position": i,
            "item": {
                "@type": "Course",
                "name": "%s %s course (A1–C2)" % (c["name"], c["code"]),
                "description": "Free %s course with six levels, 24 lessons, practice "
                               "sets and level tests." % c["name"],
                "url": href,
                "inLanguage": c["code"],
                "provider": {"@type": "Organization", "name": "EkGuru",
                             "url": "https://ekguru.shop/"},
                "isAccessibleForFree": True,
                "hasCourseInstance": [
                    {"@type": "CourseInstance", "courseMode": "online",
                     "courseWorkload": "PT30M"}
                ],
            },
        })
    out.append('<script type="application/ld+json">%s</script>' % json.dumps(
        {"@context": "https://schema.org", "@type": "ItemList",
         "name": "EkGuru free language courses", "numberOfItems": len(items),
         "itemListElement": items}, ensure_ascii=False, separators=(",", ":")))
    out.append(HUB_END)
    return "\n".join(out)


def build_home(courses, levels, meta):
    featured = ["ar", "es", "fr", "ja", "zh", "hi"]
    picked = [c for c in courses if c["code"] in featured]
    order = {code: i for i, code in enumerate(featured)}
    picked.sort(key=lambda c: order.get(c["code"], 99))
    lessons, _ = counts(courses, levels)

    return "\n".join([
        HOME_START,
        "<!-- Written by tools/build-course-hub.py — re-run after a course is added. -->",
        '<section class="xp-sec soft" id="courses">',
        '  <div class="xp-wrap">',
        '    <div class="xp-head xp-rise">',
        '      <span class="xp-kicker">Free courses</span>',
        "      <h2>39 languages, A1 to C2 — free, in your browser</h2>",
        "      <p>%s lessons across %d languages, each with its own alphabet, "
        "vocabulary, dialogues and level tests. Nothing to install, nothing to pay, "
        "progress saved on your device.</p>" % (lessons, len(courses)),
        '      <div class="xp-rule" aria-hidden="true"></div>',
        "    </div>",
        '    <div class="grid course-grid xp-stagger">',
        "".join(card(c, levels, meta, deep_prefix="") for c in picked),
        "    </div>",
        '    <p class="center" style="margin-top:28px">'
        '<a class="btn btn-primary btn-lg" href="courses/">Open the full course library</a> '
        '<a class="btn btn-ghost btn-lg" href="start/">Find my level first</a></p>',
        "  </div>",
        "</section>",
        HOME_END,
    ])


def splice(path, block, start, end, check):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if start in html and end in html:
        updated = re.sub(re.escape(start) + r".*?" + re.escape(end), block, html,
                         count=1, flags=re.S)
    elif start in html or end in html:
        raise SystemExit("ERROR: %s has one marker of the %s pair" % (path, start))
    else:
        raise SystemExit("ERROR: %s is missing the %s marker pair" % (path, start))
    if updated == html:
        return False
    if check:
        print("STALE: %s needs tools/build-course-hub.py" % path)
        return "stale"
    with open(path, "w", encoding="utf-8") as f:
        f.write(updated)
    return True


def main():
    check = "--check" in sys.argv
    courses, levels, meta = load()
    names = country_names()
    hub = build_hub(courses, levels, meta, names)
    home = build_home(courses, levels, meta)

    stale = []
    for block, path, s, e in ((hub, HUB, HUB_START, HUB_END),
                              (home, HOME, HOME_START, HOME_END)):
        res = splice(path, block, s, e, check)
        if res == "stale":
            stale.append(path)
        elif res:
            print("wrote %s (%d bytes)" % (path, len(block)))
        else:
            print("%s already up to date" % path)

    if stale:
        return 1
    print("course hub: %d courses, %d phases" % (
        len(courses), len({c.get("phase") for c in courses})))
    return 0


if __name__ == "__main__":
    sys.exit(main())

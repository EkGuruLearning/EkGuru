#!/usr/bin/env python3
"""Build long-form Learn posts for world-course languages with authored packs.

Each track's ten article bodies are hand-authored under
``tools/<language>-phase3-content/``. New pages remain noindex until reviewed.
The source markers let ``build-all.py check`` verify generated output without
rewriting the site's layered HTML.

Run all configured tracks, one track, or check them:
    python3 tools/build-world-phase3.py
    python3 tools/build-world-phase3.py ar
    python3 tools/build-world-phase3.py --check
"""
from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-10-04"

ES_POSTS = [
    ("beginner", "How to Learn Spanish from Scratch — A Complete Beginner’s Guide",
     "A practical first-month plan for Spanish: choose a variety, learn useful phrases, build listening and speaking habits, and avoid common beginner traps."),
    ("pronunciation", "The Spanish Alphabet — Every Letter, Sound and Example",
     "A clear guide to the 27 Spanish letters, silent h, c and g rules, accents, r and rr, with everyday examples and pronunciation cues."),
    ("common-words", "100 Common Spanish Words with Pronunciation",
     "One hundred high-use Spanish words grouped by task, with English meanings, approximate pronunciation and short phrases you can use."),
    ("grammar", "Spanish Grammar Basics — Sentence Structure Explained",
     "Build Spanish sentences from the ground up: word order, gender, articles, adjective agreement, present-tense verbs, questions and negation."),
    ("mistakes", "Common Mistakes When Learning Spanish — and How to Fix Them",
     "A practical guide to ser and estar, false friends, gender, accents, por and para, pronouns, pronunciation and the habits that fix them."),
    ("travel", "Spanish for Travel — Essential Phrases for Real Situations",
     "Useful Spanish for airports, hotels, cafés, transport, directions and emergencies, with pronunciation cues and regional context."),
    ("reading", "How to Read Spanish — A Step-by-Step Guide",
     "Spanish uses the Latin alphabet, but accents and letter patterns matter. Learn to decode signs, menus and short sentences without guessing."),
    ("vs-hindi", "Spanish vs Hindi — What Is Different and What Is Similar?",
     "A careful comparison of Spanish and Hindi: language families, scripts, word order, gender, verbs, sounds and the knowledge that transfers."),
    ("speaking-alone", "How to Practise Speaking Spanish Alone — A Realistic Plan",
     "A sustainable solo-speaking routine using shadowing, self-talk, recordings, role-play and short daily practice—plus the limits of studying alone."),
    ("numbers", "Spanish Numbers 1 to 100 — Counting, Prices and Time",
     "Learn Spanish numbers from uno to cien, the patterns behind tens and units, accent marks, agreement, prices and practical counting drills."),
]

AR_POSTS = [
    ("beginner", "How to Learn Arabic from Scratch — A Complete Beginner’s Guide",
     "A realistic first-month plan for Arabic: choose a learning variety, learn the script, use essential phrases and build a speaking routine."),
    ("pronunciation", "The Arabic Alphabet — 28 Letters, Shapes and Sounds",
     "Learn the Arabic letters, how they connect, short-vowel marks, right-to-left reading and the sounds English learners should practise."),
    ("common-words", "100 Common Arabic Words with Transliteration",
     "One hundred practical Modern Standard Arabic words grouped by use, with English meanings, readable transliteration and short examples."),
    ("grammar", "Arabic Grammar Basics — Sentence Structure Explained",
     "An approachable guide to Arabic word order, gender, definiteness, adjective agreement, verb patterns, negation and everyday sentence building."),
    ("mistakes", "Common Mistakes When Learning Arabic — and How to Fix Them",
     "Avoid predictable problems with letter shapes, short vowels, gender, the definite article, dialect choice and word-for-word translation."),
    ("travel", "Arabic for Travel — Useful Phrases and Regional Context",
     "Polite Arabic for greetings, transport, directions, food and asking for help, with a clear note on Modern Standard Arabic and local dialects."),
    ("reading", "How to Read Arabic Script — A Step-by-Step Guide",
     "Move from right-to-left letter recognition to joined words and short-vowelled sentences, then learn how to approach unvowelled text."),
    ("vs-hindi", "Arabic vs Hindi — Scripts, Grammar and What Transfers",
     "Compare Arabic and Hindi carefully: language families, writing direction, word order, gender, verb patterns and shared vocabulary history."),
    ("speaking-alone", "How to Practise Speaking Arabic Alone — A Realistic Plan",
     "A practical solo routine for Arabic using short recordings, shadowing, self-talk and role-play, while respecting the limits of solo practice."),
    ("numbers", "Arabic Numbers 1 to 100 — Digits, Words and Counting",
     "Read Arabic-Indic digits and practise common number words, tens, prices and dates while learning why counted nouns can change the form."),
]

DE_POSTS = [
    ("beginner", "How to Learn German from Scratch — A Complete Beginner’s Guide",
     "A realistic first-month German plan covering pronunciation, articles, useful phrases, study routines and regional variation."),
    ("pronunciation", "German Pronunciation — Umlauts, Ch, R and the Alphabet",
     "A practical guide to German spelling and sound: umlauts, ß, ch, w, v, z, word stress and listening practice."),
    ("common-words", "100 Common German Words with Pronunciation",
     "A curated set of useful German words and phrases with meanings, spelling notes, practical pronunciation cues and examples."),
    ("grammar", "German Grammar Basics — Articles, Cases and Word Order",
     "Build clear German sentences with noun gender, articles, cases, adjective endings, verb position, questions and negation."),
    ("mistakes", "Common German Mistakes — and How to Fix Them",
     "Fix common problems with der, die and das, cases, verb-second order, word endings, false friends and du versus Sie."),
    ("travel", "German for Travel — Useful Phrases and Regional Context",
     "Polite Standard German for greetings, trains, hotels, cafés and asking for help, with careful notes on local usage."),
    ("reading", "How to Read German — A Step-by-Step Guide",
     "Learn to decode German spelling, capitalization, compounds, verb brackets and signs without translating every word."),
    ("vs-hindi", "German vs Hindi — Scripts, Grammar and What Transfers",
     "Compare German and Hindi language families, scripts, word order, gender, cases, pronouns and shared study strategies."),
    ("speaking-alone", "How to Practise Speaking German Alone — A Realistic Plan",
     "A sustainable German speaking routine using shadowing, self-talk, recordings and role-play, with honest limits and feedback tips."),
    ("numbers", "German Numbers 1 to 100 — Counting, Prices and Time",
     "Learn German numbers, the units-before-tens pattern, dates, time and prices with short practice activities."),
]

TRACKS = {
    "es": {
        "name": "Spanish", "native": "español", "folder": "spanish",
        "content_dir": "spanish-phase3-content", "posts": ES_POSTS,
        "course_url": "/languages/es/course/",
        "hub_desc": "Ten long-form Spanish guides with examples, pronunciation cues, regional context and practice.",
        "hub_lede": ("A first set of readable Spanish guides for English-speaking learners. Each article tackles one real question, "
                     "pairs Spanish examples with a plain pronunciation cue, and links back to the free authored course. Spanish "
                     "is spoken across many communities; where usage differs by region, the guides say so instead of pretending "
                     "there is one universal conversation."),
        "pronunciation_note": ("Spanish examples appear in the original Latin alphabet. “Say it” cues in these articles are broad "
                               "English-friendly approximations, not IPA and not a claim that every Spanish-speaking region sounds "
                               "identical. Listen to more than one speaker, keep the regional model you are learning consistent, "
                               "and use the spelling rules on the alphabet and reading pages as your reliable reference."),
    },
    "de": {
        "name": "German", "native": "Deutsch", "folder": "german",
        "content_dir": "german-phase3-content", "posts": DE_POSTS,
        "course_url": "/languages/de/course/",
        "hub_desc": "Ten long-form Standard German guides with examples, pronunciation cues, regional context and practice.",
        "hub_lede": ("A first set of readable German guides for English-speaking learners. In German the language is called "
                     "<span lang=\"de\">Deutsch</span>. These articles use Standard German as a shared learning base, "
                     "with labelled examples and approachable pronunciation cues. German is used across Germany, Austria, "
                     "Switzerland and other communities; everyday words, accents and conventions can vary by place and setting."),
        "pronunciation_note": ("German already uses the Latin alphabet, so no transliteration is needed. Any English-friendly "
                               "pronunciation cue in these guides is a learner aid, not IPA and not a substitute for listening. "
                               "The focus is Standard German; regional accents and vocabulary differ, and Swiss Standard German "
                               "uses ss where other standards may use ß."),
    },
    "ar": {
        "name": "Arabic", "native": "العربية", "folder": "arabic",
        "content_dir": "arabic-phase3-content", "posts": AR_POSTS,
        "course_url": "/languages/ar/course/",
        "hub_desc": "Ten long-form Arabic guides with Arabic-script examples, transliteration, Modern Standard Arabic context and practice.",
        "hub_lede": ("A first set of readable Arabic guides for English-speaking learners. The name in Arabic is "
                     "<bdi lang=\"ar\" dir=\"rtl\">العربية</bdi>. The examples focus on Modern Standard Arabic "
                     "and clearly mark Arabic text right to left alongside a simple Latin transliteration. Arabic-speaking communities "
                     "use many regional dialects; these guides explain where a phrase belongs to formal MSA and where everyday speech "
                     "may differ."),
        "pronunciation_note": ("Arabic examples are marked right to left and paired with a readable transliteration. The transliteration "
                               "is a learning aid, not a single universal standard or IPA; sounds such as ʿayn and emphatic consonants "
                               "need listening practice. The course uses Modern Standard Arabic, while everyday conversations use "
                               "regional dialects that can differ substantially."),
    },
}


def load_page_helpers():
    path = ROOT / "tools/build-hindi-pages.py"
    spec = importlib.util.spec_from_file_location("build_hindi_pages_for_world_phase3", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load the shared article scaffold")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_body(track: dict, slug: str) -> str:
    path = ROOT / "tools" / track["content_dir"] / (slug + ".html")
    if not path.is_file():
        raise FileNotFoundError("Missing hand-authored Phase 3 body: " + str(path))
    text = path.read_text(encoding="utf-8").strip()
    if not text or "<h2" not in text:
        raise ValueError("Phase 3 body needs content and section headings: " + str(path))
    return text


def source_marker(code: str, slug: str, text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:20]
    return "<!-- ekguru:phase3-world:%s:%s:%s -->" % (code, slug, digest)


def sibling_links(track: dict, current: str) -> str:
    rows = []
    for slug, title, desc in track["posts"]:
        if slug == current:
            continue
        rows.append('<li><a href="../%s/">%s</a><span>%s</span></li>' %
                    (slug, title, desc))
    return ("<section aria-labelledby=\"related-guides\"><h2 id=\"related-guides\">More %s guides</h2>" %
            track["name"] + '<ul class="linklist">' + "".join(rows) + "</ul></section>")


def hub_body(track: dict) -> str:
    rows = []
    for slug, title, desc in track["posts"]:
        rows.append('<li><a href="%s/">%s</a><span>%s</span></li>' % (slug, title, desc))
    return ('''<p class="crumb"><a href="../../">EkGuru</a> › <a href="../">Learn</a> › %(name)s</p>
<h1>%(name)s — practical long-form guides</h1>
<p class="lede">%(lede)s</p>
<h2>Choose a question</h2>
<ul class="linklist">%(rows)s</ul>
<h2>Use the full course too</h2>
<p>These guides are companions, not a replacement for practice. The <a href="%(course_url)s">%(name)s course hub</a> links to lessons, a practice lab, a quiz and review. Start with the guide that answers the question you have today, then use the course to repeat the pattern until it comes out without translating.</p>
<h2>About writing and pronunciation</h2>
<p>%(pronunciation)s</p>
''' % {"name": track["name"], "lede": track["hub_lede"], "rows": "".join(rows),
       "course_url": track["course_url"], "pronunciation": track["pronunciation_note"]})


def page_html(helper, *, code: str, track: dict, slug: str, title: str,
              desc: str, body: str, is_hub: bool = False) -> str:
    depth = "../../" if is_hub else "../../../"
    route = "learn/%s/" % track["folder"] if is_hub else "learn/%s/%s/" % (track["folder"], slug)
    html = helper.head(title, desc, route, depth, index=False)
    html = re.sub(r"<html([^>]*)>", r'<html\1 data-learning-language="%s">' % code, html, count=1)
    html = re.sub(r'(<meta property="article:published_time" content=")[^"]*(">)',
                  r"\g<1>" + TODAY + r"\2", html, count=1)
    if is_hub:
        page_body = source_marker(code, "hub", body) + "\n" + body
    else:
        page_body = source_marker(code, slug, body) + "\n" + body + "\n" + sibling_links(track, slug)
    return html + page_body + helper.foot(depth)


def expected_markers(helper, code: str, track: dict) -> dict[str, str]:
    root = "learn/" + track["folder"]
    hub = hub_body(track)
    expected = {root + "/index.html": source_marker(code, "hub", hub)}
    for slug, title, desc in track["posts"]:
        source = "<h1>%s</h1>\n%s" % (title, read_body(track, slug))
        expected[root + "/" + slug + "/index.html"] = source_marker(code, slug, source)
    return expected


def check_current(expected: dict[str, str], name: str) -> int:
    missing = []
    for rel, marker in expected.items():
        path = ROOT / rel
        if not path.is_file() or marker not in path.read_text(encoding="utf-8"):
            missing.append(rel)
    if missing:
        print("STALE %s Phase 3 pages (rebuild): %s" % (name, ", ".join(missing)))
        return 1
    print("%s Phase 3: hub + ten authored posts are current" % name)
    return 0


def build_track(helper, code: str, track: dict) -> int:
    bodies = {slug: read_body(track, slug) for slug, _title, _desc in track["posts"]}
    out = ROOT / "learn" / track["folder"]
    out.mkdir(parents=True, exist_ok=True)

    hub_title = track["name"] + " — Practical Learn Guides | EkGuru"
    hub_html = page_html(helper, code=code, track=track, slug="", title=hub_title,
                         desc=track["hub_desc"], body=hub_body(track), is_hub=True)
    (out / "index.html").write_text(hub_html, encoding="utf-8")

    for slug, title, desc in track["posts"]:
        body = "<h1>%s</h1>\n%s" % (title, bodies[slug])
        page = page_html(helper, code=code, track=track, slug=slug, title=title + " | EkGuru",
                         desc=desc, body=body)
        target = out / slug / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page, encoding="utf-8")
    print("%s Phase 3: wrote hub + %d long-form posts (all noindex pending review)" %
          (track["name"], len(track["posts"])))
    return 0


def main() -> int:
    args = [x for x in sys.argv[1:] if not x.startswith("-")]
    check = "--check" in sys.argv[1:]
    codes = args or sorted(TRACKS)
    unknown = [code for code in codes if code not in TRACKS]
    if unknown:
        print("Unknown world Phase 3 track(s): " + ", ".join(unknown))
        return 2
    helper = load_page_helpers()
    failed = 0
    for code in codes:
        track = TRACKS[code]
        if check:
            failed |= check_current(expected_markers(helper, code, track), track["name"])
        else:
            failed |= build_track(helper, code, track)
    return failed


if __name__ == "__main__":
    raise SystemExit(main())

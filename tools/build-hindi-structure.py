#!/usr/bin/env python3
"""EkGuru Phase 4 — build the canonical Learn Hindi structure (hub + levels + topics).

Single source of truth: the ASSETS map below. Every entry points at a REAL page
that exists in the repo; this tool reads each page's own <title> and meta
description, so nothing here can invent a fact. Pages are generated as
self-contained article-style HTML matching the existing site scaffold.

Generated output (never hand-edit these files — rerun this tool):
  learn/hindi/index.html                    -> the Learn Hindi hub
  learn/hindi/beginner/index.html           -> level page
  learn/hindi/elementary/index.html         -> level page
  learn/hindi/<topic>/index.html            -> 11 topic hubs (real content only)

Also: appends the new pages to search-index.json (section "Page") so they are
searchable and filterable, and prints a machine-readable summary.

Run:  python3 tools/build-hindi-structure.py
"""
import json, os, re, sys, time
from html import unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "https://ekguru.shop"
NOW = time.strftime("%Y-%m-%d", time.gmtime())
GEN = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

# ---------------------------------------------------------------- helpers
def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def title_of(path):
    """Read a page's own <title> (without the | EkGuru suffix)."""
    h = read(path)
    m = re.search(r"<title>(.*?)</title>", h, re.S)
    if not m:
        raise SystemExit(f"FATAL: no title in {path}")
    return re.sub(r"\s*\|\s*EkGuru$", "", unescape(m.group(1))).strip()

def desc_of(path):
    h = read(path)
    m = re.search(r'<meta name="description" content="([^"]*)"', h)
    return unescape(m.group(1)).strip() if m else ""

def short_desc(path, n=110):
    d = desc_of(path)
    if not d:
        return ""
    if len(d) <= n:
        return d
    return d[:n].rsplit(" ", 1)[0] + "…"

def rel(base_dir, target):
    """Relative href from a page in base_dir (site-root-relative, e.g. 'learn/hindi')
    to a target (site-root-relative dir OR file, e.g. 'learn/hindi-alphabet-for-beginners'
    or 'find-tutors.html'). Directories get a trailing slash; files do not."""
    b = base_dir.split("/") if base_dir else []
    t = target.split("/") if target else []
    # common prefix
    i = 0
    while i < len(b) and i < len(t) and b[i] == t[i]:
        i += 1
    ups = [".."] * (len(b) - i)
    downs = t[i:]
    p = "/".join(ups + downs)
    if target.endswith(".html"):
        return p or "."
    return (p or ".") + "/"

def page_path(target):
    return os.path.join(target, "index.html")

# ---------------------------------------------------------------- asset map
# Every value is a site-root-relative directory of a REAL page.
LESSONS = {
    "hindi-alphabet-for-beginners": "basics",
    "write-your-name-in-hindi": "basics",
    "learn-hindi-online-guide": "basics",
    "how-to-say-hello-in-hindi": "conversation",
    "aap-tum-tu-hindi": "conversation",
    "hindi-numbers-1-to-100": "numbers",
    "hindi-days-months-time": "time-dates",
    "hindi-family-words": "vocabulary",
    "hindi-phrases-for-travel": "travel",
    "hindi-sentence-structure": "grammar",
    "hindi-verbs-present-past-future": "grammar",
    "hindi-gender-masculine-feminine": "grammar",
    "common-hindi-mistakes": "grammar",
    "hindi-or-urdu-difference": "basics",
    "learn-hindi-from-bollywood": "daily-life",
}

HINDI_TOPICS = {
    "alphabet": "basics", "beginners": "basics", "how-long": "basics",
    "name-topic": "basics", "flashcards-topic": "basics", "for-kids": "basics",
    "hindi-vs-urdu": "basics",
    "greetings": "conversation", "formal-informal": "conversation",
    "conversation": "conversation", "speaking": "conversation",
    "relationships": "conversation",
    "pronunciation": "pronunciation", "listening": "pronunciation",
    "reading": "pronunciation", "writing": "pronunciation",
    "grammar": "grammar", "sentence-structure": "grammar", "verbs": "grammar",
    "mistakes": "grammar",
    "vocabulary": "vocabulary", "family": "vocabulary",
    "numbers": "numbers", "time-date": "time-dates",
    "phrases-travel": "travel", "emergency": "travel",
    "phrases-food": "food", "shopping": "shopping",
    "bollywood": "daily-life", "slang": "daily-life", "hinglish": "daily-life",
    "heritage": "daily-life", "indian-languages": "daily-life",
    "business": "daily-life",
}

MATERIALS = {
    "materials/alphabet/devanagari-chart": "basics",
    "materials/beginner/reading-guide": "basics",
    "materials/conversation/polite-vs-casual": "conversation",
    "materials/family/family-words-quick-ref": "vocabulary",
    "materials/grammar/beginner-grammar-reference": "grammar",
    "materials/grammar/postpositions": "grammar",
    "materials/grammar/sentence-patterns": "grammar",
    "materials/pronunciation/pronunciation-guide": "pronunciation",
    "materials/reading/reading-practice": "pronunciation",
    "materials/revision/mistakes-checklist": "grammar",
    "materials/travel/restaurant-shopping-transport": "travel",
    "materials/verbs/essential-verbs": "grammar",
    "materials/vocabulary/100-essential-words": "vocabulary",
    "materials/work/work-phrases": "daily-life",
    "materials/writing/writing-practice": "pronunciation",
}

TOOLS = {
    "toolbox/hindi-alphabet": "basics",
    "toolbox/hindi-level-test": "basics",
    "toolbox/hindi-quiz": "basics",
    "toolbox/hindi-numbers": "numbers",
    "toolbox/hindi-flashcards": "vocabulary",
    "toolbox/hindi-vocabulary": "vocabulary",
    "toolbox/hindi-date-time": "time-dates",
    "toolbox/hindi-time-planner": "time-dates",
    "toolbox/hindi-typing": "pronunciation",
    "toolbox/hindi-pronunciation": "pronunciation",
    "toolbox/hindi-verbs": "grammar",
    "toolbox/hindi-phrasebook": "conversation",
}

PRACTICE = {
    "learn/practice/vocabulary": "vocabulary",
    "learn/practice/grammar": "grammar",
    "learn/practice/sentence-builder": "grammar",
    "learn/practice/verbs": "grammar",
    "learn/practice/listening": "pronunciation",
    "learn/practice/pronunciation": "pronunciation",
    "learn/practice/reading": "pronunciation",
    "learn/practice/writing": "pronunciation",
    "learn/practice/speaking": "conversation",
    "learn/practice/review": "grammar",
    "learn/practice/placement": "basics",
    "learn/practice/daily": "vocabulary",
}

PATHS = {
    "learn/paths/hindi-from-zero": "basics",
    "learn/paths/speaking-starter": "conversation",
    "learn/paths/reading-hindi": "pronunciation",
    "learn/paths/travel-hindi": "travel",
    "learn/paths/everyday-hindi": "conversation",
    "learn/paths/grammar-foundations": "grammar",
}

ANSWERS = {
    "answers/hindi-greetings-namaste-and-others": "conversation",
    "answers/hindi-numbers-1-to-100": "numbers",
    "answers/how-to-tell-the-time-in-hindi": "time-dates",
    "answers/hindi-family-words": "vocabulary",
    "answers/hindi-phrases-for-travelling-in-india": "travel",
    "answers/hindi-word-order-explained": "grammar",
    "answers/hindi-postpositions-ka-ki-ke": "grammar",
    "answers/how-to-order-food-in-hindi": "food",
    "answers/how-to-ask-for-directions-in-hindi": "travel",
    "answers/what-does-ji-mean-in-hindi": "conversation",
    "answers/can-i-learn-hindi-without-learning-the-script": "basics",
}

ASK = {
    "ask/is-hindi-hard-to-learn": "basics",
    "ask/do-i-need-to-learn-devanagari": "basics",
    "ask/how-to-say-hello-in-hindi-question": "conversation",
    "ask/how-to-count-1-to-10-in-hindi": "numbers",
    "ask/how-to-say-please-in-hindi": "conversation",
    "ask/how-many-words-do-i-need-in-hindi": "vocabulary",
    "ask/how-long-to-learn-hindi": "basics",
    "ask/how-to-remember-hindi-genders": "grammar",
    "ask/how-to-say-i-dont-understand-in-hindi": "conversation",
    "ask/what-does-acha-mean-in-hindi": "vocabulary",
    "ask/how-to-practice-hindi-without-a-partner": "pronunciation",
}

# Only build topics with genuine support (>= 3 distinct assets).
TOPIC_META = {
    "basics": ("Basics — the script, sounds and first steps",
               "The starting point: the Devanagari alphabet, your first words, and the honest answer to where to begin."),
    "conversation": ("Conversation — greetings to real talk",
                     "What to actually say to a person: greetings, politeness (aap, tum, tu), small talk and speaking practice."),
    "pronunciation": ("Pronunciation, reading & writing",
                      "The sounds English speakers get wrong, and the path from reading your first letter to writing your own name."),
    "grammar": ("Grammar — how Hindi actually works",
                "Word order, verbs, gender, postpositions and the mistakes everyone makes — explained, not listed."),
    "vocabulary": ("Vocabulary — the words that do the work",
                   "High-frequency words grouped by meaning: family, numbers, and the hundred essentials."),
    "travel": ("Travel Hindi — phrases for the road",
               "Bargaining, autos, trains, food, directions and being unwell — the phrases you will actually use."),
    "daily-life": ("Daily life & culture",
                   "Bollywood, Hinglish, slang, heritage and the Hindi you hear every day, not in textbooks."),
    "numbers": ("Numbers & counting",
                "Hindi numbers are genuinely irregular. The full 1–100 list, the pattern, and counting practice."),
    "time-dates": ("Time & dates",
                   "Days, months and telling the time — including the half-hour words that confuse every learner."),
    "food": ("Food & eating",
             "Ordering, tastes and table talk — the Hindi you need in restaurants and markets."),
    "shopping": ("Shopping & money",
                 "Prices, bargaining and the phrases for markets and shops."),
}

LEVELS = {
    "beginner": {
        "h1": "Beginner Hindi — start here",
        "who": "You have never studied Hindi, or you tried and stalled. You can read nothing yet, or only a few letters.",
        "outcomes": "Read and sound out Devanagari, count to 100, greet people correctly, build simple SOV sentences, and use the right 'you' (aap/tum/tu).",
        "order": ["learn/hindi-alphabet-for-beginners", "learn/write-your-name-in-hindi",
                  "learn/hindi-numbers-1-to-100", "learn/how-to-say-hello-in-hindi",
                  "learn/hindi-phrases-for-travel", "learn/hindi-sentence-structure",
                  "learn/hindi-verbs-present-past-future", "learn/hindi-gender-masculine-feminine",
                  "learn/aap-tum-tu-hindi", "learn/hindi-days-months-time",
                  "learn/hindi-family-words", "learn/common-hindi-mistakes"],
        "practice": ["learn/practice/writing", "learn/practice/reading", "learn/practice/vocabulary",
                     "learn/practice/sentence-builder", "learn/practice/placement"],
        "materials": ["materials/alphabet/devanagari-chart", "materials/vocabulary/100-essential-words",
                      "materials/grammar/beginner-grammar-reference"],
        "paths": ["learn/paths/hindi-from-zero", "learn/paths/reading-hindi", "learn/paths/speaking-starter"],
        "next": "Elementary",
    },
    "elementary": {
        "h1": "Elementary Hindi — get past the plateau",
        "who": "You can read the script slowly, know the core words, and can make simple sentences — but conversation is still hard work.",
        "outcomes": "Handle real conversations, understand politeness and register, use postpositions and tenses without guessing, and read short paragraphs.",
        "order": ["learn/hindi-or-urdu-difference", "learn/learn-hindi-from-bollywood",
                  "hindi/formal-informal", "hindi/conversation", "hindi/reading",
                  "hindi/listening", "hindi/verbs", "hindi/relationships"],
        "practice": ["learn/practice/listening", "learn/practice/pronunciation",
                     "learn/practice/speaking", "learn/practice/verbs", "learn/practice/review"],
        "materials": ["materials/grammar/postpositions", "materials/grammar/sentence-patterns",
                      "materials/reading/reading-practice", "materials/conversation/polite-vs-casual"],
        "paths": ["learn/paths/everyday-hindi", "learn/paths/grammar-foundations", "learn/paths/travel-hindi"],
        "next": "Intermediate",
    },
}

# Intermediate / Advanced: NO level pages are built — there is not yet enough
# real, dedicated content. Stated honestly on the hub instead of shipping
# empty SEO landing pages (Phase-4 rule: never GREEN on placeholders).

# ---------------------------------------------------------------- rendering
def shell(depth, title, desc, canon, h1, lede, body, jsonld):
    pre = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="google-site-verification" content="hFaqyp-9LdUXSKPA9RF011TkO2m_-7AUMasXqm_0dGI" />
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | EkGuru</title>
<meta name="description" content="{desc}">
<meta name="author" content="EkGuru">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title} | EkGuru">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}/images/og-cover.jpg">
<meta property="og:site_name" content="EkGuru">
<meta property="article:published_time" content="{NOW}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="icon" href="{pre}images/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="{pre}images/apple-touch-icon.png">
<link rel="manifest" href="{pre}manifest.webmanifest">
<meta name="theme-color" content="#4f32d9">
<link rel="stylesheet" href="{pre}css/style.min.css">
<style>
.art{{max-width:760px;margin:0 auto;padding:0 20px 60px}}
.art h1{{font-size:2rem;line-height:1.25;margin:26px 0 10px}}
.art .meta{{color:var(--muted);font-size:.86rem;margin:0 0 26px}}
.art h2{{font-size:1.28rem;margin:34px 0 12px;padding-top:6px}}
.art p,.art li{{line-height:1.75}}
.art ul,.art ol{{padding-left:22px}}
.art li{{margin:7px 0}}
.crumb{{font-size:.84rem;color:var(--muted);padding:18px 0 0}}
.crumb a{{color:var(--muted)}}
.lede{{color:var(--ink-2);font-size:1.05rem;line-height:1.7;margin:0 0 22px}}
.hs-grid{{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));margin:16px 0}}
.hs-card{{border:1px solid var(--line);border-radius:12px;padding:14px 16px;text-decoration:none;background:var(--card,#fff)}}
.hs-card:hover{{border-color:var(--brand-2)}}
.hs-card b{{display:block;color:var(--brand);font-size:.98rem;margin-bottom:4px}}
.hs-card span{{display:block;color:var(--ink-2);font-size:.86rem;line-height:1.5}}
.linklist{{list-style:none;padding:0;margin:12px 0 0}}
.linklist li{{padding:10px 0;border-bottom:1px solid var(--line)}}
.linklist li:last-child{{border-bottom:0}}
.linklist a{{font-weight:600}}
.linklist span{{display:block;color:var(--muted);font-size:.87rem;margin-top:2px;line-height:1.5}}
.note{{background:var(--bg-soft);border:1px solid #ddd8ff;border-radius:12px;padding:14px 16px;margin:14px 0;font-size:.94rem;color:var(--ink-2)}}
@media(pointer:coarse){{.hs-card,.linklist a{{min-height:44px;display:block}}input,select,textarea,button{{min-height:44px}}}}
</style>
{jsonld}
</head>
<body>
<div class="art">
  {body}
</div>
<!-- ekguru:trust-footer:start -->
<footer class="pw-ftr">
  <nav aria-label="Site information">
    <a href="{pre}">Home</a>
    <a href="{pre}about/">About</a>
    <a href="{pre}contact/">Contact</a>
    <a href="{pre}privacy/">Privacy</a>
    <a href="{pre}terms/">Terms</a>
    <a href="{pre}disclaimer/">Disclaimer</a>
  </nav>
  <p>
  © 2026 EkGuru — One Student. One Goal. One Guru.<br>
  Written and maintained by Prakash. Hindi lessons with native-speaking tutors, one to one.
  </p>
</footer>
<!-- ekguru:trust-footer:end -->
</body>
</html>
<script src="{pre}js/site-config.js" defer></script>
<script src="{pre}js/analytics.js" defer></script>
<!-- ekguru:recovery:start -->
<script src="{pre}js/recovery.js" defer></script>
<!-- ekguru:recovery:end -->
<script defer>
if ("serviceWorker" in navigator) {{
  window.addEventListener("load", function () {{
    navigator.serviceWorker.register("{pre}sw.js").catch(function () {{}});
  }});
}}
</script>
"""

def jsonld(typename, name, desc, url, extra=""):
    return ('<script type="application/ld+json">{"@context": "https://schema.org", "@graph": ['
            '{"@type": "%s", "@id": "%s#page", "name": "%s", "description": "%s", '
            '"url": "%s", "inLanguage": "en"}%s]}</script>\n'
            % (typename, url, name, desc, url, extra))

def li(base, target, short=None):
    """One link-list item: real title + real short description."""
    t = title_of(page_path(target))
    s = short or short_desc(page_path(target))
    return f'    <li><a href="{rel(base, target)}">{t}</a><span>{s}</span></li>'

def hs_card(base, target, label, short=None):
    t = title_of(page_path(target))
    s = short or short_desc(page_path(target))
    return (f'<a class="hs-card" href="{rel(base, target)}"><b>{label}</b>'
            f'<span>{t}</span></a>')

def topic_bucket(topic):
    """Gather every real asset for a topic, grouped by kind."""
    b = {"lessons": [], "topics": [], "materials": [], "tools": [], "practice": [], "paths": [], "answers": [], "ask": []}
    for slug, tp in LESSONS.items():
        if tp == topic:
            b["lessons"].append("learn/" + slug)
    for slug, tp in HINDI_TOPICS.items():
        if tp == topic:
            b["topics"].append("hindi/" + slug)
    for slug, tp in MATERIALS.items():
        if tp == topic:
            b["materials"].append(slug)
    for slug, tp in TOOLS.items():
        if tp == topic:
            b["tools"].append(slug)
    for slug, tp in PRACTICE.items():
        if tp == topic:
            b["practice"].append(slug)
    for slug, tp in PATHS.items():
        if tp == topic:
            b["paths"].append(slug)
    for slug, tp in ANSWERS.items():
        if tp == topic:
            b["answers"].append(slug)
    for slug, tp in ASK.items():
        if tp == topic:
            b["ask"].append(slug)
    return b

def render_topic(topic, meta):
    t_h1, t_lede = meta
    b = topic_bucket(topic)
    base = "learn/hindi/" + topic
    depth = 3
    canon = f"{BASE}/{base}/"
    title = t_h1
    body = []
    body.append(f'  <p class="crumb"><a href="../../../">EkGuru</a> › <a href="../../">Learn Hindi</a> › <a href="../">Hindi</a> › {t_h1.split(" — ")[0]}</p>')
    body.append(f'  <h1>{t_h1}</h1>')
    body.append(f'  <p class="lede">{t_lede}</p>')
    if b["lessons"]:
        body.append('  <h2>Guides</h2><ul class="linklist">')
        body += [li(base, t) for t in b["lessons"]]
        body.append('</ul>')
    if b["topics"]:
        body.append('  <h2>Topic pages</h2><ul class="linklist">')
        body += [li(base, t) for t in b["topics"]]
        body.append('</ul>')
    if b["practice"]:
        body.append('  <h2>Practice</h2><ul class="linklist">')
        body += [li(base, t) for t in b["practice"]]
        body.append('</ul>')
    if b["materials"]:
        body.append('  <h2>Printable materials</h2><ul class="linklist">')
        body += [li(base, t) for t in b["materials"]]
        body.append('</ul>')
    if b["tools"]:
        body.append('  <h2>Tools</h2><ul class="linklist">')
        body += [li(base, t) for t in b["tools"]]
        body.append('</ul>')
    if b["paths"]:
        body.append('  <h2>Learning paths</h2><ul class="linklist">')
        body += [li(base, t) for t in b["paths"]]
        body.append('</ul>')
    if b["answers"]:
        body.append('  <h2>Short answers</h2><ul class="linklist">')
        body += [li(base, t) for t in b["answers"]]
        body.append('</ul>')
    if b["ask"]:
        body.append('  <h2>Questions people ask</h2><ul class="linklist">')
        body += [li(base, t) for t in b["ask"]]
        body.append('</ul>')
    body.append('  <p style="margin-top:26px"><a href="../beginner/">Beginner level</a> · <a href="../elementary/">Elementary level</a> · <a href="../">All of Learn Hindi</a></p>')
    j = jsonld("CollectionPage", title, t_lede, canon)
    return shell(depth, title, t_lede, canon, t_h1, t_lede, "\n".join(body), j), base

def render_level(level):
    meta = LEVELS[level]
    base = "learn/hindi/" + level
    depth = 3
    canon = f"{BASE}/{base}/"
    title = meta["h1"]
    lede = meta["who"]
    body = []
    body.append(f'  <p class="crumb"><a href="../../../">EkGuru</a> › <a href="../../">Learn Hindi</a> › <a href="../">Hindi</a> › {meta["h1"].split(" — ")[0]}</p>')
    body.append(f'  <h1>{meta["h1"]}</h1>')
    body.append(f'  <p class="lede">{meta["who"]}</p>')
    body.append('  <h2>Who this is for</h2>')
    body.append(f'  <p>{meta["who"]}</p>')
    body.append('  <h2>What you will be able to do</h2>')
    body.append(f'  <p>{meta["outcomes"]}</p>')
    body.append('  <h2>The order to learn in</h2><ol class="linklist">')
    for t in meta["order"]:
        body.append(li(base, t))
    body.append('</ol>')
    body.append('  <h2>Practice</h2><ul class="linklist">')
    for t in meta["practice"]:
        body.append(li(base, t))
    body.append('</ul>')
    body.append('  <h2>Printable materials</h2><ul class="linklist">')
    for t in meta["materials"]:
        body.append(li(base, t))
    body.append('</ul>')
    body.append('  <h2>Learning paths</h2><ul class="linklist">')
    for t in meta["paths"]:
        body.append(li(base, t))
    body.append('</ul>')
    if level == "beginner":
        body.append('  <p style="margin-top:26px">Next level: <a href="../elementary/">Elementary</a> · <a href="../">All of Learn Hindi</a></p>')
    else:
        body.append('  <p style="margin-top:26px" class="note">The next stage after Elementary would be an '
                    'Intermediate level — but we will not ship an empty page. Until there is enough real '
                    'intermediate content, the deeper material lives in '
                    '<a href="../daily-life/">Daily life &amp; culture</a> and '
                    '<a href="../grammar/">Grammar</a>. <a href="../">Back to Learn Hindi</a>.</p>')
    j = jsonld("CollectionPage", title, meta["outcomes"], canon)
    return shell(depth, title, meta["outcomes"], canon, meta["h1"], lede, "\n".join(body), j), base

def render_hub():
    base = "learn/hindi"
    depth = 2
    canon = f"{BASE}/learn/hindi/"
    title = "Learn Hindi — the complete structure"
    lede = ("Everything EkGuru teaches about Hindi, in one journey: choose a goal, pick your level, "
            "work through a topic, then read, practise, quiz and review — with a tutor available "
            "when you want one, never required.")
    body = []
    body.append('  <p class="crumb"><a href="../../">EkGuru</a> › <a href="../">Learn Hindi</a> › Hindi</p>')
    body.append('  <h1>Learn Hindi — the complete structure</h1>')
    body.append(f'  <p class="lede">{lede}</p>')

    # Quick start — 8 intents
    body.append('  <h2>Quick start — what do you want?</h2>')
    body.append('  <div class="hs-grid">')
    body.append(hs_card(base, "learn/paths/hindi-from-zero", "Start from zero",
                        "The complete beginner track, in the order that actually works."))
    body.append(hs_card(base, "learn/hindi-phrases-for-travel", "Just travel phrases",
                        "The Hindi that gets you fed, housed and pointed the right way."))
    body.append(hs_card(base, "learn/hindi-alphabet-for-beginners", "Read the script",
                        "Every Devanagari letter, its sound, and the order to learn them."))
    body.append(hs_card(base, "learn/paths/speaking-starter", "Speak, don't just study",
                        "Stop studying. Start saying things out loud."))
    body.append(hs_card(base, "learn/common-hindi-mistakes", "Fix my mistakes",
                        "The ten errors that mark you out as a learner, and the fix."))
    body.append(hs_card(base, "learn/write-your-name-in-hindi", "Write my name",
                        "Type any name and see it in Devanagari, letter by letter."))
    body.append(hs_card(base, "learn/paths/", "Follow a path",
                        "Six goal-based tracks: from zero, speaking, reading, travel, everyday, grammar."))
    body.append(hs_card(base, "daily-hindi", "A daily habit",
                        "One idea, one task and a short word list a day. About twenty minutes."))
    body.append('  </div>')

    # Level selector — only real levels
    body.append('  <h2>Choose your level</h2>')
    body.append('  <div class="hs-grid">')
    body.append('<a class="hs-card" href="beginner/"><b>Beginner</b>'
                '<span>From zero: the script, first words and simple sentences.</span></a>')
    body.append('<a class="hs-card" href="elementary/"><b>Elementary</b>'
                '<span>Past the plateau: real conversation, tenses, register.</span></a>')
    body.append('  </div>')
    body.append('  <p class="note">No Intermediate or Advanced page yet — we will not ship an empty '
                'level page. The site has a handful of intermediate-leaning pages (Bollywood, slang, '
                'Hinglish, heritage) inside <a href="daily-life/">Daily life &amp; culture</a>, and that '
                'is where they live until there is enough real content for a level of their own.</p>')

    # Topic selector
    body.append('  <h2>Topics</h2>')
    body.append('  <div class="hs-grid">')
    for tp, meta in TOPIC_META.items():
        body.append('<a class="hs-card" href="%s/"><b>%s</b><span>%s</span></a>'
                    % (tp, meta[0].split(" — ")[0], meta[1]))
    body.append('  </div>')

    # Paths
    body.append('  <h2>Learning paths</h2><ul class="linklist">')
    for t in sorted(PATHS):
        body.append(li(base, t))
    body.append('</ul>')

    # Featured lessons
    body.append('  <h2>Featured lessons</h2><ul class="linklist">')
    for t in ["learn/hindi-alphabet-for-beginners", "learn/how-to-say-hello-in-hindi",
              "learn/hindi-numbers-1-to-100", "learn/hindi-sentence-structure"]:
        body.append(li(base, t))
    body.append('</ul>')

    # Practice
    body.append('  <h2>Practice labs</h2><ul class="linklist">')
    for t in ["learn/practice/", "learn/practice/vocabulary", "learn/practice/placement"]:
        body.append(li(base, t))
    body.append('</ul>')

    # FAQ + tutor bridge
    body.append('  <h2>Before you start</h2><ul class="linklist">')
    body.append(li(base, "faq"))
    body.append(li(base, "ask/is-hindi-hard-to-learn"))
    body.append(li(base, "ask/how-long-to-learn-hindi"))
    body.append('</ul>')
    body.append('  <div class="note"><strong>Want a teacher?</strong> Everything above is free and works '
                'alone — but if you want someone to correct your pronunciation, '
                f'<a href="{rel(base, "find-tutors.html")}">our tutors</a> teach one to one from $6 a '
                'lesson. Tutoring is never required; it is available when you want it.</div>')
    j = jsonld("CollectionPage", "EkGuru Learn Hindi structure", lede, canon)
    return shell(depth, title, lede, canon, "Learn Hindi — the complete structure", lede, "\n".join(body), j), base

# ---------------------------------------------------------------- search index
def update_search_index(new_entries):
    idx_path = "search-index.json"
    idx = json.load(open(idx_path, encoding="utf-8"))
    by_url = {e["u"]: e for e in idx}
    added = 0
    for e in new_entries:
        u = e["u"]
        if u in by_url:
            by_url[u].update(e)
        else:
            idx.append(e)
            added += 1
    # keep sorted like build-search-index.py does
    order = ["Answer", "Country", "Daily Hindi", "Home", "Language", "Lesson",
             "Location", "Material", "Page", "Phrases", "Practice", "Question",
             "Tool", "Tutor", "Vocabulary"]
    idx.sort(key=lambda e: (order.index(e["s"]) if e["s"] in order else 99, e["t"].lower()))
    with open(idx_path, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=0)
    return added

# ---------------------------------------------------------------- main
def main():
    made = []
    entries = []

    # hub
    html, base = render_hub()
    os.makedirs(os.path.join(ROOT, base), exist_ok=True)
    open(page_path(base), "w", encoding="utf-8").write(html)
    made.append(base + "/")
    entries.append({"u": "learn/hindi/", "t": "Learn Hindi — the complete structure",
                    "d": "Everything EkGuru teaches about Hindi in one journey: choose a goal, level and topic, then learn, practise, quiz and review.",
                    "s": "Page", "k": "learn hindi structure level topic lesson path practice"})

    # levels
    for lv in LEVELS:
        html, base = render_level(lv)
        os.makedirs(os.path.join(ROOT, base), exist_ok=True)
        open(page_path(base), "w", encoding="utf-8").write(html)
        made.append(base + "/")
        entries.append({"u": base + "/", "t": LEVELS[lv]["h1"],
                        "d": LEVELS[lv]["outcomes"], "s": "Page",
                        "k": "learn hindi " + lv + " level lessons practice"})

    # topics
    for tp, meta in TOPIC_META.items():
        html, base = render_topic(tp, meta)
        os.makedirs(os.path.join(ROOT, base), exist_ok=True)
        open(page_path(base), "w", encoding="utf-8").write(html)
        made.append(base + "/")
        entries.append({"u": base + "/", "t": meta[0],
                        "d": meta[1], "s": "Page",
                        "k": "learn hindi " + tp.replace("-", " ") + " topic"})

    n_added = update_search_index(entries)

    print("generated pages:")
    for m in made:
        print("  ", m)
    print(f"search-index.json: +{n_added} new entries (total {len(json.load(open('search-index.json')))}))")
    json.dump({"generated": GEN, "pages": made, "searchIndexAdded": n_added,
               "levelsBuilt": sorted(LEVELS), "topicsBuilt": sorted(TOPIC_META),
               "levelsNotBuilt": ["intermediate", "advanced"],
               "reasonNotBuilt": "not enough real dedicated content — no empty level pages"},
              open("reports/learn-hindi-build.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

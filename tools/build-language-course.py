#!/usr/bin/env python3
"""Build a complete trilingual (EN + HI + target) language course under learn/<slug>/.

Mirrors the learn/hindi/ structure (22 pages) but every lesson is SELF-CONTAINED
trilingual content — not hubs pointing at supporting pages that don't exist yet
(the Hindi course itself refuses to ship empty levels, and so do we).

Usage: python3 tools/build-language-course.py <slug>   # reads tools/lang-data/<slug>.json
Emits: learn/<slug>/**/index.html (22 pages) + js/<slug>-quiz-bank.js

Interactive labs reuse js/hindi-tools.js through the EKGURU_*_ACTIVE globals
(quiz, typing, worksheets); review/my-progress/conversation are honest static
pages with localStorage checklists because the Hindi SRS/conversation engines
have Hindi data baked in and must not show Hindi words inside another language.
"""
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://ekguru.shop"
TODAY = "2026-09-13"

ART_CSS = """.art{max-width:760px;margin:0 auto;padding:0 20px 60px}
.art h1{font-size:clamp(1.7rem,4.6vw,2.1rem);line-height:1.2;margin:22px 0 10px;letter-spacing:-.01em;text-wrap:balance}
.art .meta{color:var(--muted);font-size:.86rem;margin:0 0 26px}
.art h2{font-size:1.28rem;margin:34px 0 12px;padding-top:6px}
.art p,.art li{line-height:1.75}
.art ul,.art ol{padding-left:22px}
.art li{margin:7px 0}
.crumb{font-size:.84rem;color:var(--muted);padding:18px 0 0}
.crumb a{color:var(--muted)}
.lede{color:var(--ink-2);font-size:1.05rem;line-height:1.7;margin:0 0 22px}
.hs-grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));margin:18px 0}
.hs-card{position:relative;overflow:hidden;border:1px solid var(--line);border-radius:16px;padding:18px 16px 16px;text-decoration:none;background:var(--card,#fff);box-shadow:var(--sh-1);transition:transform .18s ease,box-shadow .18s ease}
.hs-card::before{content:"";position:absolute;left:0;right:0;top:0;height:4px;background:linear-gradient(90deg,#4f32d9,#8b5cf6)}.hs-card:hover{transform:translateY(-3px);box-shadow:var(--sh-2)}
.hs-card b{display:block;color:var(--brand);font-size:.98rem;margin-bottom:4px}
.hs-card span{display:block;color:var(--ink-2);font-size:.86rem;line-height:1.5}
.linklist{list-style:none;padding:0;margin:14px 0 0}
.linklist li{padding:12px 14px;border:1px solid var(--line);border-radius:12px;margin-bottom:10px;background:var(--card,#fff);transition:transform .15s ease,box-shadow .15s ease}.linklist li:hover{transform:translateX(3px);box-shadow:var(--sh-1)}
.linklist li:last-child{border-bottom:0}
.linklist a{font-weight:600}
.linklist span{display:block;color:var(--muted);font-size:.87rem;margin-top:2px;line-height:1.5}
.note{background:var(--bg-soft);border:1px solid #ddd8ff;border-left:4px solid #4f32d9;border-radius:12px;padding:15px 18px;margin:16px 0;font-size:.94rem;color:var(--ink-2);box-shadow:var(--sh-1)}
.tri td:nth-child(3){font-weight:600}.tbl{border-collapse:collapse;width:100%;margin:16px 0;font-size:.94rem}.tbl th,.tbl td{border-bottom:1px solid var(--line);padding:10px 13px;text-align:left;line-height:1.6}.tbl thead th{background:var(--bg-soft);font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;color:var(--ink-2)}.tbl tbody tr:nth-child(even){background:var(--bg-soft)}
@media(pointer:coarse){.hs-card,.linklist a{min-height:44px;display:block}input,select,textarea,button{min-height:44px}}
.prevnext{display:flex;justify-content:space-between;gap:12px;margin:34px 0 8px}
.prevnext a{flex:1;border:1px solid var(--line);border-radius:14px;padding:14px 16px;text-decoration:none;color:var(--ink);background:var(--card,#fff);box-shadow:var(--sh-1);transition:transform .15s ease,box-shadow .15s ease}
.prevnext a:hover{transform:translateY(-2px);box-shadow:var(--sh-2)}
.prevnext .k{display:block;font-size:.78rem;color:var(--muted)}
.prevnext .t{font-weight:600}"""

TRUST_FTR = """<!-- ekguru:trust-footer:start -->
<footer class="pw-ftr">
  <nav aria-label="Site information">
    <a href="{r}">Home</a>
    <a href="{r}about/">About</a>
    <a href="{r}contact/">Contact</a>
    <a href="{r}privacy/">Privacy</a>
    <a href="{r}terms/">Terms</a>
    <a href="{r}disclaimer/">Disclaimer</a>
  </nav>
  <p>
  © 2026 EkGuru — One Student. One Goal. One Guru.<br>
  Written and maintained by Prakash. Free {name} lessons in English, Hindi and {name}.
  </p>
</footer>
<!-- ekguru:trust-footer:end -->"""

SCRIPTS = """<script src="{r}js/site-config.js" defer></script>
<script src="{r}js/analytics.js" defer></script>
<!-- ekguru:recovery:start -->
<script src="{r}js/recovery.js" defer></script>
<!-- ekguru:recovery:end -->
{extra}<script defer>
if ("serviceWorker" in navigator) {{
  window.addEventListener("load", function () {{
    navigator.serviceWorker.register("{r}sw.js").catch(function () {{}});
  }});
}}
</script>"""


def E(s):
    return html.escape(str(s))


_COURSE_VOICE_CODES = None
COURSE_MARKER = "<!-- ekguru:course-voice-controls:v1 -->"
_TARGET_SCRIPT_BLOCKS = {
    "bn": r"\u0980-\u09FF", "gu": r"\u0A80-\u0AFF",
    "kn": r"\u0C80-\u0CFF", "ml": r"\u0D00-\u0D7F",
    "mr": r"\u0900-\u097F", "pa": r"\u0A00-\u0A7F",
    "ta": r"\u0B80-\u0BFF", "te": r"\u0C00-\u0C7F",
    "ur": r"\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF",
}
_TARGET_SCRIPT_PATTERNS = {}


def course_voice_code(language_name):
    """Resolve speech tags from authored course metadata, not a name heuristic."""
    global _COURSE_VOICE_CODES
    if _COURSE_VOICE_CODES is None:
        _COURSE_VOICE_CODES = {}
        for path in glob.glob(os.path.join(ROOT, "tools", "lang-data", "*.json")):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            code = data.get("voice_code")
            name = str(data.get("name") or "").strip().casefold()
            if code and name:
                if name in _COURSE_VOICE_CODES and _COURSE_VOICE_CODES[name] != code:
                    raise ValueError("Ambiguous course voice code for " + name)
                _COURSE_VOICE_CODES[name] = str(code)
    return _COURSE_VOICE_CODES.get(str(language_name or "").strip().casefold())


def target_script_pattern(language_name):
    code = course_voice_code(language_name)
    block = _TARGET_SCRIPT_BLOCKS.get(code)
    if not block:
        return None
    if code not in _TARGET_SCRIPT_PATTERNS:
        char = "[" + block + "]"
        join = r"(?:[\u200c\u200d]*" + char + r"+)*(?:[\s\u00a0]+" + char + r"+(?:[\u200c\u200d]*" + char + r"+)*)*"
        _TARGET_SCRIPT_PATTERNS[code] = re.compile(char + r"+" + join)
    return _TARGET_SCRIPT_PATTERNS[code]


def speaker_button(text, voice_code, language_name):
    text = str(text or "").strip()
    if not text or not voice_code:
        return ""
    return ('<button type="button" class="say" data-sb-say="%s" data-voice-lang="%s" '
            'aria-label="%s" aria-pressed="false"><span aria-hidden="true">🔊</span></button>') % (
                html.escape(text, quote=True), html.escape(voice_code, quote=True),
                html.escape("Play %s in %s" % (text, language_name), quote=True))


def _tagged_speaker_text(text, voice_code, language_name):
    return ('<bdi lang="%s" dir="auto">%s</bdi>%s' % (
        html.escape(voice_code, quote=True), E(text),
        speaker_button(text, voice_code, language_name)))


def explicit_foreign_voice(text, start, end, language_name):
    """Honor an explicit Hindi label in shared Devanagari text, especially Marathi glosses."""
    if course_voice_code(language_name) != "mr":
        return None
    value = str(text or "")
    before = value[max(0, start - 120):start]
    after = value[end:end + 80]
    labels = list(re.finditer(r"\b(Hindi|Marathi)\s*[:=]\s*", before, re.I))
    if labels and labels[-1].group(1).casefold() == "hindi":
        return ("hi", "Hindi")
    if re.search(r"\bHindi\s+$", before, re.I) or re.match(r"\s*\(\s*Hindi\s*\)", after, re.I):
        return ("hi", "Hindi")
    return None


def tag_language_cells(page, code, language_name):
    def fix(match):
        tag = match.group(0)
        if not re.match(r"<td\b", tag, re.I):
            return tag
        heading = re.search(r'''\bdata-h\s*=\s*(["'])(.*?)\1''', tag, re.I)
        heading = html.unescape(heading.group(2)).strip().casefold() if heading else ""
        lang = "hi" if heading == "hindi" else code if heading == str(language_name).casefold() else None
        if not lang:
            return tag
        if re.search(r"\blang\s*=", tag, re.I):
            tag = re.sub(r'''\blang\s*=\s*(["'])[^"']*\1''', 'lang="%s"' % lang, tag, count=1, flags=re.I)
        else:
            tag = tag[:-1] + ' lang="%s">' % lang
        if not re.search(r"\bdir\s*=", tag, re.I):
            tag = tag[:-1] + ' dir="auto">'
        return tag
    return re.sub(r"<td\b[^>]*>", fix, page, flags=re.I)


def add_course_speaker_controls(page, code, language_name):
    pattern = target_script_pattern(language_name)
    if not pattern:
        return page
    void = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
    chunks = re.split(r"(<[^>]*>)", page)
    stack, output = [], []
    for chunk in chunks:
        if chunk.startswith("<"):
            parsed = re.match(r"<\s*(/?)\s*([A-Za-z][\w:-]*)\b", chunk)
            if parsed:
                closing, tag = parsed.groups(); tag = tag.lower()
                if closing:
                    for i in range(len(stack) - 1, -1, -1):
                        if stack[i][0] == tag:
                            stack = stack[:i]
                            break
                elif tag not in void and not chunk.rstrip().endswith("/>"):
                    lang_match = re.search(r'''\blang\s*=\s*(["'])(.*?)\1''', chunk, re.I)
                    lang = html.unescape(lang_match.group(2)) if lang_match else None
                    hidden = re.search(r'''\baria-hidden\s*=\s*(["'])true\1''', chunk, re.I)
                    is_hindi_cell = tag == "td" and re.search(r'''\bdata-h\s*=\s*(["'])Hindi\1''', chunk, re.I)
                    skip = tag in {"script", "style", "noscript", "button"} or bool(hidden or is_hindi_cell) or (lang or "").lower().split("-", 1)[0] == "hi"
                    stack.append((tag, lang, skip))
            output.append(chunk)
            continue
        if any(item[2] for item in stack):
            output.append(chunk); continue
        langs = [item[1] for item in stack if item[1]]
        nearest = langs[-1].lower().split("-", 1)[0] if langs else ""
        pieces, cursor = [], 0
        for match in pattern.finditer(chunk):
            pieces.append(chunk[cursor:match.start()])
            foreign = explicit_foreign_voice(chunk, match.start(), match.end(), language_name)
            if foreign:
                marked = _tagged_speaker_text(match.group(0), *foreign)
            elif nearest == code:
                # Keep the authored target text visible; controls are additive.
                marked = match.group(0) + speaker_button(match.group(0), code, language_name)
            else:
                marked = _tagged_speaker_text(match.group(0), code, language_name)
            pieces.append(marked); cursor = match.end()
        pieces.append(chunk[cursor:]); output.append("".join(pieces))
    return "".join(output)


def language_markup(body, language_name):
    code = course_voice_code(language_name)
    return add_course_speaker_controls(tag_language_cells(body, code, language_name), code, language_name) if code else body



def shell(d, path, title, desc, body, depth, extra_scripts="", robots="index, follow"):  # noqa: E501
    r = "../" * depth
    canon = f"{BASE}/learn/{d['slug']}/{path}"
    ld = {"@context": "https://schema.org", "@graph": [{
        "@type": "CollectionPage", "@id": canon + "#page", "name": title,
        "description": desc, "url": canon, "inLanguage": "en"}]}
    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="google-site-verification" content="hFaqyp-9LdUXSKPA9RF011TkO2m_-7AUMasXqm_0dGI" />
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | EkGuru</title>
<meta name="description" content="{E(desc)}">
<meta name="author" content="EkGuru">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="article">
<meta property="og:title" content="{E(title)} | EkGuru">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}/images/og-cover.jpg">
<meta property="og:site_name" content="EkGuru">
<meta property="article:published_time" content="{TODAY}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<link rel="icon" href="{r}images/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="{r}images/apple-touch-icon.png">
<link rel="manifest" href="{r}manifest.webmanifest">
<meta name="theme-color" content="#4f32d9">
<link rel="stylesheet" href="{r}css/style.min.css">
<style>
{ART_CSS}
</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>

</head>
<body>
<div class="art">
{body}</div>
{TRUST_FTR.format(r=r, name=E(d['name']))}
{SCRIPTS.format(r=r, extra=extra_scripts)}
{COURSE_MARKER}
</body>
</html>
"""


def crumb(d, trail):
    # trail: [(href|None, label)] after the fixed EkGuru › Learn X › X part
    links = [f'<a href="{{r}}">EkGuru</a> › <a href="{{r}}learn/">Learn {E(d["name"])}</a> › <a href="{{r}}learn/{d["slug"]}/">{E(d["name"])}</a>']
    for href, label in trail:
        links.append(f'<a href="{href}">{E(label)}</a>' if href else E(label))
    return '<p class="crumb">' + " › ".join(links) + "</p>"


def tri_table(rows, col3="target", note_key="note"):
    out = ['<table class="tbl tri"><thead><tr><th>English</th><th>Hindi</th>',
           f'<th>{E(col3)}</th><th>Say it</th></tr></thead><tbody>']
    for w in rows:
        cells = (f'<td data-h="English">{E(w["en"])}</td>'
                 f'<td data-h="Hindi">{E(w["hi"])}</td>'
                 f'<td data-h="{E(col3)}">{E(w["t"])}</td>'
                 f'<td data-h="Say it">{E(w["r"])}</td>')
        if w.get(note_key):
            cells += f"</tr><tr><td></td><td colspan=\"3\" style=\"color:var(--muted);font-size:.85rem\">{E(w[note_key])}</td>"
        out.append("<tr>" + cells + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def alpha_table(rows):
    out = ['<table class="tbl"><thead><tr><th>Letter</th><th>Sound</th><th>Like…</th></tr></thead><tbody>']
    for w in rows:
        out.append(f"<tr><td style=\"font-size:1.4rem\">{E(w['t'])}</td><td><b>{E(w['r'])}</b></td><td>{E(w['hint'])}</td></tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


# ---------------------------------------------------------------- pages

def p_index(d):
    n = d["name"]
    topics = [("basics", "Basics", "The starting point: the script, your first words, and where to begin."),
              ("conversation", "Conversation", "What to actually say to a person: greetings, politeness and small talk."),
              ("pronunciation", "Pronunciation, reading & writing", "The sounds learners get wrong, and the path to reading your first letter."),
              ("grammar", "Grammar", "Word order, verbs, pronouns and the mistakes everyone makes — explained, not listed."),
              ("vocabulary", "Vocabulary", "High-frequency words grouped by meaning: family, colours, and core nouns."),
              ("travel", "Travel phrases", "Stations, directions, fares and hotels — the phrases you will actually use."),
              ("daily-life", "Daily life & culture", "Festivals, food culture and the phrases of everyday life."),
              ("numbers", "Numbers & counting", "1–20, the tens, and 100 — with the counting pattern."),
              ("time-dates", "Time & dates", "Days, today/tomorrow, and telling the time."),
              ("food", "Food & eating", "Ordering, tastes and table talk — in restaurants and markets."),
              ("shopping", "Shopping & money", "Prices, bargaining and the phrases for markets and shops.")]
    cards = "".join(f'<a class="hs-card" href="{s}/"><b>{t}</b><span>{x}</span></a>' for s, t, x in topics)
    guide_cards = "\n".join(
        '<a class="hs-card" href="' + s + '/"><b>' + t + '</b><span>' + x + '</span></a>'
        for s, t, x in PHASE3_EXISTING + PHASE3_POSTS)
    adv = ""
    if d.get("advanced_modules"):
        cards2 = "".join(f'<a class="hs-card" href="advanced/{m["slug"]}/"><b>{m["title"]}</b><span>{m["lede"]}</span></a>' for m in d["advanced_modules"])
        adv = f'\n  <h2>Advanced topics</h2>\n  <div class="hs-grid">\n{cards2}\n  </div>'
    return (f"Learn {n} — the complete course",
            f"Free {n} course in three languages side by side: every word in English, Hindi and {n} — levels, topics, quizzes and practice labs.",
            f"""{crumb(d, [])}
  <h1>Learn {E(n)} — the complete course</h1>
  <p class="lede">Everything below is free and trilingual: every word and phrase in <b>English, Hindi and {E(n)}</b> ({E(d['native'])}, {E(d['roman_native'])}) side by side — with pronunciation for each one. {E(d['speakers'])} people speak {E(n)}: {E(d['where'])}</p>
  <div class="note"><b>How to use this course.</b> Start at Beginner, work down the topics in order, and quiz yourself after each one. {E(d['difficulty'])}</div>
  <h2>Choose your level</h2>
  <div class="hs-grid">
<a class="hs-card" href="beginner/"><b>Beginner</b><span>From zero: the script, first words and simple sentences.</span></a>
<a class="hs-card" href="elementary/"><b>Elementary</b><span>Past the first plateau: tenses, real conversation, daily topics.</span></a>
<a class="hs-card" href="intermediate/"><b>Intermediate</b><span>Politeness, complex sentences and natural speech — modest and honest.</span></a>
  </div>
  <h2>Topics</h2>
  <div class="hs-grid">
{cards}
  </div>{adv}
  <h2>Guides — read one a day</h2>
  <p>The ten long-form guides for this course: two are written for beginners, two for people who already
  read the script, and one is honest about how close this language is to Hindi. Each runs to well over a
  thousand words and links to the others.</p>
  <div class="hs-grid">
{guide_cards}
  </div>
  <h2>Practice labs</h2><ul class="linklist">
    <li><a href="practice/">Practice labs</a><span>Quiz, typing trainer, worksheets and conversation scenarios.</span></li>
    <li><a href="practice/quiz/">Topic quiz</a><span>Multiple-choice questions from the lesson bank, with explanations.</span></li>
    <li><a href="practice/typing/">{E(n)} typing trainer</a><span>Roman prompt → type it in {E(d['script_name'])}.</span></li>
    <li><a href="practice/worksheets/">Worksheets</a><span>Printable prompts with writing space and answers.</span></li>
    <li><a href="practice/conversation/">Conversation scenarios</a><span>Trilingual dialogues: market, tea stall, asking the way.</span></li>
    <li><a href="review/">Review deck</a><span>The 20 core words — tick them off as they stick.</span></li>
    <li><a href="my-progress/">My progress</a><span>Your local checklist (this device only).</span></li>
  </ul>
  <div class="note"><strong>Want a teacher?</strong> Everything above is free and works alone. Our tutors teach Hindi one to one — the {E(n)} course itself needs no tutor and no sign-up.</div>""")


def p_basics(d):
    n = d["name"]
    return (f"{n} basics — the script, sounds and first steps",
            f"The starting point for {n}: the {d['script_name']}, your first words, and the honest order to learn in.",
            f"""{crumb(d, [(None, "Basics")])}
  <h1>{E(n)} basics — the script, sounds and first steps</h1>
  <p class="lede">The starting point: the {E(d['script_name'])}, your first words, and the honest answer to where to begin. {E(d['script_note'])}</p>
  <h2>The alphabet at a glance</h2>
  <p>The {E(d['script_name'] if 'script' in d['script_name'].lower() else d['script_name'] + ' script')} has {len(d['vowels'])} vowels and {len(d['consonants'])} consonants. The full tables with sounds are on the <a href="../pronunciation/">pronunciation page</a> — learn to recognise them before you memorise any words.</p>
  <h2>Your first five words</h2>
  {tri_table(d['greetings'][:5], col3=n)}
  <h2>The order to learn in</h2>
  <ol>
    <li><a href="../pronunciation/">Script + sounds</a> — {E(n)} is phonetic: learn the letters and you can read anything.</li>
    <li><a href="../conversation/">Greetings + pronouns</a> — say hello, introduce yourself, ask where.</li>
    <li><a href="../numbers/">Numbers 1–20</a> — prices, time and quantities unlock immediately.</li>
    <li><a href="../grammar/">Word order + present tense</a> — one pattern ({E(d['sov']['t'])}) builds a thousand sentences.</li>
    <li>Topics (<a href="../food/">food</a>, <a href="../travel/">travel</a>, <a href="../shopping/">shopping</a>) — learn what your life needs first.</li>
  </ol>
  <div class="note"><b>Honest note.</b> {E(d['difficulty'])}</div>""")


def level_page(d, slug, title, lede, goals, order, can_do):
    n = d["name"]
    return (f"{n} {title}",
            lede,
            f"""{crumb(d, [(None, title)])}
  <h1>{E(n)} {E(title)}</h1>
  <p class="lede">{E(lede)}</p>
  <h2>Who this is for</h2>
  <ul>{"".join(f"<li>{E(g)}</li>" for g in goals)}</ul>
  <h2>The order to learn in</h2>
  <ol>{"".join(f"<li>{x}</li>" for x in order)}</ol>
  <h2>What you will be able to do</h2>
  <ul>{"".join(f"<li>{E(c)}</li>" for c in can_do)}</ul>
  <h2>Practice</h2><ul class="linklist">
    <li><a href="../practice/quiz/">Topic quiz</a><span>Filter by topic and level; every answer has an explanation.</span></li>
    <li><a href="../review/">Review deck</a><span>The 20 core words — tick them off as they stick.</span></li>
  </ul>""")


def p_beginner(d):
    return level_page(d, "beginner", "Beginner",
        f"From zero: the {d['script_name']}, first words and simple sentences.",
        ["You know no words yet, or only hello and thank-you.",
         "You cannot read the script yet — the course assumes nothing."],
        ['<a href="../pronunciation/">Script + sounds</a> — recognise every letter.',
         '<a href="../conversation/">Greetings + pronouns</a> — hello, I/you, where/what.',
         '<a href="../numbers/">Numbers 1–10</a> — then to 20 when they stick.',
         '<a href="../grammar/">Word order + “I” forms of 6 verbs</a> — your first real sentences.',
         '<a href="../practice/quiz/">Quiz yourself</a> on basics + numbers before moving on.'],
        ["Read any word slowly, greet people politely, count to 20, and build simple I-sentences."])


def p_elementary(d):
    n = d["name"]
    return level_page(d, "elementary", "Elementary",
        f"Past the first plateau: tenses, real conversation and daily topics in {n}.",
        ["You can read slowly and hold a 30-second exchange.",
         "You know 100+ words and the present tense."],
        ['<a href="../grammar/">Full pronouns + past and future</a> — talk about yesterday and tomorrow.',
         '<a href="../food/">Food</a> + <a href="../shopping/">shopping</a> — order, pay, bargain.',
         '<a href="../travel/">Travel</a> + <a href="../time-dates/">time</a> — directions, days, the clock.',
         '<a href="../practice/conversation/">Conversation scenarios</a> — rehearse the dialogues aloud.',
         '<a href="../practice/typing/">Typing trainer</a> — write what you can say.'],
        ["Handle a market, a tea stall and directions; talk about past and future; read short real texts."])


def p_intermediate(d):
    n = d["name"]
    return level_page(d, "intermediate", "Intermediate",
        f"Politeness, complex sentences and natural {n} speech — a modest, honest level.",
        ["You handle daily situations but sound blunt or textbook-like.",
         "You want formality tiers, negation and joined sentences."],
        ['Re-read <a href="../grammar/">grammar</a>: formality tiers, negation, postpositions — then use them in the dialogues.',
         'Study <a href="../daily-life/">daily life &amp; culture</a> — festivals, register, how people really talk.',
         'Shadow the <a href="../practice/conversation/">scenarios</a>: repeat each line aloud until it flows.',
         'Write 5 sentences a day and check them in the <a href="../practice/quiz/">quiz</a> explanations.'],
        ["Choose the right level of politeness, join sentences naturally, and follow everyday conversation."])


def p_conversation(d):
    n = d["name"]
    return (f"{n} conversation — greetings and first dialogues",
            f"What to actually say to a person in {n}: greetings, introductions and small talk, trilingual.",
            f"""{crumb(d, [(None, "Conversation")])}
  <h1>{E(n)} conversation</h1>
  <p class="lede">What to actually say to a person in {E(n)}: greetings, introductions and the small talk that opens every door.</p>
  <h2>Greetings</h2>
  {tri_table(d['greetings'], col3=n)}
  <h2>Introducing yourself</h2>
  {tri_table(d['daily_phrases'][3:7], col3=n)}
  <h2>Full dialogues</h2>
  <p>Three everyday scenes, with every line in English, Hindi and {E(n)} side by side, are on the <a href="../practice/conversation/">{E(n)} conversation scenarios</a> page.</p>""")


def p_pronunciation(d):
    n = d["name"]
    return (f"{n} pronunciation, reading & writing",
            f"The {d['script_name']} letter by letter, the sounds learners get wrong, and how to practise them.",
            f"""{crumb(d, [(None, "Pronunciation")])}
  <h1>{E(n)} pronunciation, reading &amp; writing</h1>
  <p class="lede">The {E(n)} sounds learners get wrong, and the path from your first letter to reading real words. {E(d['script_note'])}</p>
  <h2>Vowels ({len(d['vowels'])})</h2>
  {alpha_table(d['vowels'])}
  <h2>Consonants ({len(d['consonants'])})</h2>
  {alpha_table(d['consonants'])}
  <h2>How to practise</h2>
  <ol>
    <li>Read the tables aloud twice a day for a week — recognition before recall.</li>
    <li>Then <a href="../practice/typing/">type the words</a>: roman prompt → {E(d['script_name'])}.</li>
    <li>Finally read the <a href="../numbers/">numbers</a> and <a href="../vocabulary/">core words</a> without the roman column.</li>
  </ol>""")


def p_grammar(d):
    n = d["name"]
    s = d["sov"]
    prows = "".join(f"<tr><td>{E(p['who_en'])}</td><td>{E(p['who_t'])}</td><td><b>{E(p['verb_t'])}</b></td><td>{E(p['verb_r'])}</td></tr>" for p in d["present_table"])
    pf = "".join(f"<tr><td>{E(x['en'])}</td><td>{E(x['hi'])}</td><td><b>{E(x['t'])}</b></td><td>{E(x['r'])}</td></tr>" for x in d["past_future"])
    post = "".join(f"<tr><td>{E(p['en'])}</td><td>{E(p['hi'])}</td><td><b>{E(p['t'])}</b></td><td>{E(p['ex_t'])} ({E(p['ex_r'])}) — {E(p['ex_en'])}</td></tr>" for p in d["postpositions"])
    # `t` is the target-language text. It used to be read from `en` because the
    # classifiers list carried the target text there and no `t` at all; that
    # shape also made tools/language-gate.py read an empty word. The data now
    # matches every other list in the file (see
    # tools/normalize-lang-data-classifiers.py); the table is unchanged.
    clf = "".join(f"<tr><td><b>{E(c['t'])}</b> ({E(c['r'])})</td><td>{E(c['hi'])}</td><td>{E(c['note'])}</td></tr>" for c in d["classifiers"])
    # v104+ — per-language prose (Bengali defaults keep the first course byte-identical)
    gender_title = E(d.get("gender_title", "No grammatical gender"))
    gender_note = E(d.get("gender_note", "Unlike Hindi, adjectives never change: the word for \u201cgood\u201d stays the same for boys, girls and books. One less thing to memorise."))
    present_note = E(d.get("present_note", "Notice formal and familiar forms differ \u2014 the verb tells you the relationship."))
    negation_title = E(d.get("negation_title", "Negation is one word"))
    negation_note = d.get("negation_note", "Put <b>\u09a8\u09be</b> (na) after a present-tense verb: \u0986\u09ae\u09bf \u099c\u09be\u09a8\u09bf \u09a8\u09be (ami jani na) \u2014 I don't know. Past tense tucks it inside: \u0996\u09be\u0987\u09a8\u09bf (khaini) \u2014 didn't eat.")
    counting_note = d.get("counting_note", "Things take \u099f\u09be, people take \u099c\u09a8:")
    return (f"{n} grammar — word order, verbs and pronouns",
            f"{n} word order, verbs, pronouns and negation — explained with trilingual examples, not listed.",
            f"""{crumb(d, [(None, "Grammar")])}
  <h1>{E(n)} grammar</h1>
  <p class="lede">{E(n)} word order, verbs, pronouns and the mistakes everyone makes — explained, not listed.</p>
  <h2>1. The verb goes last</h2>
  <p>{E(n)} is subject–object–verb: <b>{E(s['t'])}</b> ({E(s['r'])}) — {E(s['hi'])} — “{E(s['en'])}”. Learn this once and every sentence parses.</p>
  <h2>2. {gender_title}</h2>
  <p>{gender_note}</p>
  <h2>3. Pronouns</h2>
  {tri_table(d['pronouns'], col3=n)}
  <h2>4. Present tense — one full verb</h2>
  <p>“To eat” ({E(d['verbs'][0]['t'])}) in the present. {present_note}</p>
  <table class="tbl"><thead><tr><th>Who</th><th></th><th>Verb</th><th>Say it</th></tr></thead><tbody>{prows}</tbody></table>
  <h2>5. Past and future (first steps)</h2>
  <table class="tbl tri"><thead><tr><th>English</th><th>Hindi</th><th>{E(n)}</th><th>Say it</th></tr></thead><tbody>{pf}</tbody></table>
  <h2>6. {negation_title}</h2>
  <p>{negation_note}</p>
  <h2>7. Postpositions (not prepositions)</h2>
  <table class="tbl"><thead><tr><th>Meaning</th><th>Hindi</th><th>{E(n)}</th><th>Example</th></tr></thead><tbody>{post}</tbody></table>
  <h2>8. Counting words</h2>
  <p>{counting_note}</p>
  <table class="tbl"><thead><tr><th>{E(n)}</th><th>Hindi</th><th>Note</th></tr></thead><tbody>{clf}</tbody></table>""")


def p_vocabulary(d):
    n = d["name"]
    return (f"{n} vocabulary — family, colours and core words",
            f"High-frequency {n} words grouped by meaning: family, colours and the nouns you need first.",
            f"""{crumb(d, [(None, "Vocabulary")])}
  <h1>{E(n)} vocabulary</h1>
  <p class="lede">High-frequency {E(n)} words grouped by meaning. Learn each group, then test it in the <a href="../practice/quiz/">quiz</a>.</p>
  <h2>Family</h2>
  {tri_table(d['family'], col3=n)}
  <h2>Colours</h2>
  {tri_table(d['colors'], col3=n)}
  <h2>Core nouns</h2>
  {tri_table(d['core_nouns'], col3=n)}
  <h2>Core verbs (I-form)</h2>
  <table class="tbl tri"><thead><tr><th>English</th><th>Hindi</th><th>{E(n)}</th><th>I …</th></tr></thead><tbody>
  {"".join(f"<tr><td>{E(v['en'])}</td><td>{E(v['hi'])}</td><td><b>{E(v['t'])}</b> ({E(v['r'])})</td><td><b>{E(v['ami'])}</b> ({E(v['ami_r'])})</td></tr>" for v in d['verbs'])}
  </tbody></table>""")


def p_travel(d):
    n = d["name"]
    survival_trio = d.get("survival_trio", "X \u0995\u09cb\u09a5\u09be\u09af\u09bc? (where is X?), \u09ad\u09be\u09a1\u09bc\u09be \u0995\u09a4? (how much?), \u098f\u0996\u09be\u09a8\u09c7 \u09a5\u09be\u09ae\u09c1\u09a8 (stop here). These three handle 80% of travel.")
    return (f"{n} for travel — stations, directions and fares",
            f"{n} travel phrases: stations, directions, fares and hotels — the sentences you will actually use.",
            f"""{crumb(d, [(None, "Travel")])}
  <h1>{E(n)} for travel</h1>
  <p class="lede">Stations, directions, fares and hotels — the {E(n)} phrases you will actually use.</p>
  <h2>Key words</h2>
  {tri_table(d['travel_words'], col3=n)}
  <h2>Phrases</h2>
  {tri_table(d['travel_phrases'], col3=n)}
  <div class="note"><b>Survival trio.</b> {survival_trio}</div>""")


def p_daily(d):
    n = d["name"]
    cult = "".join(f"<li><b>{E(c['t'])}</b> ({E(c['r'])}) — {E(c['en'])}</li>" for c in d["culture"])
    return (f"{n} daily life & culture",
            f"Everyday {n} life: daily phrases plus the festivals and culture behind the words.",
            f"""{crumb(d, [(None, "Daily life")])}
  <h1>{E(n)} daily life &amp; culture</h1>
  <p class="lede">The {E(n)} phrases of everyday life, plus the culture that makes them make sense.</p>
  <h2>Daily phrases</h2>
  {tri_table(d['daily_phrases'], col3=n)}
  <h2>Culture in five words</h2>
  <ul>{cult}</ul>""")


def p_numbers(d):
    n = d["name"]
    rows = "".join(f"<tr><td><b>{w['n']}</b></td><td>{E(w['hi'])}</td><td><b>{E(w['t'])}</b></td><td>{E(w['r'])}</td></tr>" for w in d["numbers"])
    # The topic page at /<lang>/numbers/ already owns "<Language> numbers
    # 1–100"; this is the course lesson, so it says so.
    return (f"Counting in {n}: 1 to 100 (A1 lesson)",
            f"{n} numbers 1–20, the tens and 100 — with pronunciation and the counting pattern.",
            f"""{crumb(d, [(None, "Numbers")])}
  <h1>{E(n)} numbers</h1>
  <p class="lede">{E(n)} 1–20 by heart, then the tens — that covers every price, time and quantity you will meet.</p>
  <table class="tbl tri"><thead><tr><th>#</th><th>Hindi</th><th>{E(n)}</th><th>Say it</th></tr></thead><tbody>{rows}</tbody></table>
  <div class="note"><b>Pattern.</b> After 20, most numbers are regular compounds — learn the tens above and 21–99 assemble themselves. Test yourself in the <a href="../practice/quiz/">quiz</a>.</div>""")


def p_time(d):
    n = d["name"]
    return (f"{n} time & dates — days and the clock",
            f"Days of the week, today and tomorrow, and telling the time in {n}.",
            f"""{crumb(d, [(None, "Time")])}
  <h1>{E(n)} time &amp; dates</h1>
  <p class="lede">{E(n)} days, today and tomorrow, and the clock.</p>
  <h2>Days of the week</h2>
  {tri_table(d['days'], col3=n)}
  <h2>Time words</h2>
  {tri_table(d['time_words'], col3=n)}""")


def p_food(d):
    n = d["name"]
    return (f"{n} food & eating — ordering and table talk",
            f"{n} food words and ordering phrases — restaurants, tea stalls and markets.",
            f"""{crumb(d, [(None, "Food")])}
  <h1>{E(n)} food &amp; eating</h1>
  <p class="lede">Ordering, tastes and table talk — the {E(n)} you need in restaurants and markets.</p>
  <h2>Food words</h2>
  {tri_table(d['food_words'], col3=n)}
  <h2>Phrases</h2>
  {tri_table(d['food_phrases'], col3=n)}""")


def p_shopping(d):
    n = d["name"]
    bargaining_script = d.get("bargaining_script", "\u098f\u099f\u09be\u09b0 \u09a6\u09be\u09ae \u0995\u09a4? \u2192 \u0996\u09c1\u09ac \u09a6\u09be\u09ae\u09bf! \u2192 \u098f\u0995\u099f\u09c1 \u0995\u09ae \u0995\u09b0\u09c1\u09a8 \u2192 \u09a0\u09bf\u0995 \u0986\u099b\u09c7, \u09a8\u09c7\u09ac\u09cb. Smile through all four steps.")
    return (f"{n} shopping & money — prices and bargaining",
            f"{n} shopping phrases: prices, bargaining and market talk.",
            f"""{crumb(d, [(None, "Shopping")])}
  <h1>{E(n)} shopping &amp; money</h1>
  <p class="lede">{E(n)} prices, bargaining and the phrases for markets and shops.</p>
  <h2>Key words</h2>
  {tri_table(d['shopping_words'], col3=n)}
  <h2>Phrases</h2>
  {tri_table(d['shopping_phrases'], col3=n)}
  <div class="note"><b>Bargaining script.</b> {bargaining_script}</div>""")


def p_practice(d):
    n = d["name"]
    return (f"{n} practice labs",
            f"Free {n} practice: topic quiz, typing trainer, worksheets and conversation scenarios.",
            f"""{crumb(d, [(None, "Practice")])}
  <h1>{E(n)} practice labs</h1>
  <p class="lede">Free {E(n)} practice that works alone: quiz yourself, type the script, print worksheets, rehearse dialogues.</p>
  <ul class="linklist">
    <li><a href="quiz/">Topic quiz</a><span>Pick a topic and level — {len(d['quiz'])} questions with explanations.</span></li>
    <li><a href="typing/">{E(n)} typing trainer</a><span>Roman prompt → type it in {E(d['script_name'])}.</span></li>
    <li><a href="worksheets/">Worksheets</a><span>Printable prompts with writing space and answers.</span></li>
    <li><a href="conversation/">Conversation scenarios</a><span>Trilingual dialogues for real situations.</span></li>
  </ul>
  <h2>What each {E(n)} lab does</h2>
  <p>The quiz pulls multiple-choice questions out of this course's own {E(n)} lesson bank, so the answer you get wrong links back to the exact lesson that explains it. The typing trainer gives you a Roman prompt and asks for the word in {E(d['script_name'])} — useful precisely because producing a word is harder than recognising it. The worksheet builder turns any topic into a printable page you can write on, and the conversation scenarios are short {E(n)} dialogues you read aloud line by line.</p>
  <h2>How to practise</h2>
  <p>Ten focused minutes beats an hour of scrolling: pick one {E(n)} topic, take five of its {len(d['quiz'])} questions, then read the explanations for everything you missed. Come back to the same topic tomorrow — the question set rotates with the date, so the second pass tests memory rather than the question order. Nothing here is timed and nothing is sent anywhere: the score stays in this browser unless you clear it.</p>
  <div class="note">Scores here are recognition scores, not fluency measures — nothing is a certified test.</div>""")


def lab_shell(d, slug, title, desc, app_div, note, crumb_extra):
    extra = (f'<script src="{{r}}js/toast.js" defer></script>\n'
             .replace("{r}", ""))  # placeholder fixed below
    return title, desc, app_div, note, crumb_extra


def p_quiz(d):
    n = d["name"]
    return (f"{n} topic quiz",
            f"Free {n} quiz: pick a topic and level, answer multiple-choice questions from the lesson bank, get explanations.",
            "quiz-app", "quiz")


def p_typing(d):
    n = d["name"]
    return (f"{n} typing trainer",
            f"Type {n} words in {d['script_name']}: roman prompt on screen, you type the script. Free, instant, no sign-up.",
            "typing-app", "typing")


def p_worksheets(d):
    n = d["name"]
    return (f"{n} worksheets",
            f"Printable {n} worksheets: pick a topic, get prompts with writing space and an answer section.",
            "ws-app", "worksheets")


def lab_page(d, kind):
    n = d["name"]
    slug = d["slug"]
    title, desc, appid, _ = {"quiz": p_quiz(d), "typing": p_typing(d), "worksheets": p_worksheets(d)}[kind]
    # The blurb names the language: the same sentence on nine quiz pages was
    # one of the duplicate-intro groups the AdSense audit flagged.
    blurbs = {"quiz": f"Pick a {n} topic and level, then answer 5, 10 or 15 questions. Every answer comes with an explanation and a link back to the source lesson.",
              "typing": f"Type the {n} word in {d['script_name']}. Small differences in spacing or punctuation count as “minor format”, not wrong.",
              "worksheets": f"Pick a {n} topic, print the prompts, write your answers, then check the answer section."}
    r = "../../../../"
    scripts = {"quiz": f'<script src="{r}js/toast.js" defer></script>\n<script src="{r}js/{slug}-quiz-bank.js" defer></script>\n<script src="{r}js/hindi-progress.js" defer></script>\n<script src="{r}js/hindi-tools.js" defer></script>\n',
               "typing": f'<script src="{r}js/toast.js" defer></script>\n<script src="{r}js/{slug}-quiz-bank.js" defer></script>\n<script src="{r}js/hindi-fuzzy.js" defer></script>\n<script src="{r}js/hindi-progress.js" defer></script>\n<script src="{r}js/hindi-tools.js" defer></script>\n',
               "worksheets": f'<script src="{r}js/toast.js" defer></script>\n<script src="{r}js/{slug}-quiz-bank.js" defer></script>\n<script src="{r}js/hindi-tools.js" defer></script>\n'}[kind]
    explainers = {
        "quiz": f"""  <h2>How the {E(n)} quiz works</h2>
  <p>Every question is drawn from this course's own {E(n)} lesson bank, not from a generic list. Choose a topic and a length — five questions for a coffee break, fifteen for a proper session — and each answer comes back with a short explanation plus a link to the lesson it came from. The set rotates with the date, so the same topic gives you different questions tomorrow; that is deliberate, because recognising a question is not the same as knowing the word.</p>
  <h2>Getting the most out of a score</h2>
  <p>Read the explanations for the ones you missed before starting another round, and treat anything under half as a signal to re-read that {E(n)} lesson rather than to grind more questions. Wrong answers are the useful ones — they tell you which word has not stuck yet.</p>""",
        "typing": f"""  <h2>How the {E(n)} typing check works</h2>
  <p>You get a Roman prompt and type the word in {E(d['script_name'])}. The trainer compares what you typed with the stored spelling and accepts spacing and equivalent punctuation as minor format rather than marking them wrong — this is a practice tool, not an exam. Every prompt comes from the {E(n)} vocabulary on this site, so what you type is what you will actually read later.</p>
  <h2>Why typing beats re-reading</h2>
  <p>Recognition is cheap: a {E(n)} word can look familiar long before you can produce it. Typing forces the harder step — recalling the {E(d['script_name'])} letters and their order — and the mistakes it exposes are exactly the letters you keep mixing up. Ten words a day is a better routine than a hundred once a month.</p>""",
        "worksheets": f"""  <h2>How the {E(n)} worksheet is built</h2>
  <p>Choose a topic and a number of prompts, and the builder lays out a printable {E(n)} worksheet with writing space and an answer section at the end. It is designed for paper: one topic per sheet, prompts in a readable size, answers on their own block so they can be folded away. Printing from the browser prints just the sheet, with the watermark and this site's name kept on it.</p>
  <h2>Marking and reusing a sheet</h2>
  <p>Write your answers first, then check them against the answer block and note which {E(n)} words needed a second attempt — those are the ones to review tomorrow. Nothing is stored for you, so print a fresh sheet for a fresh attempt; a set of five finished sheets makes an honest revision pack.</p>""",
    }
    body = f"""{crumb(d, [("../", "Practice"), (None, title.split(" — ")[0].replace(n + " ", "").title())])}
  <h1>{E(title)}</h1>
  <p class="lede">{E(blurbs[kind])}</p>
  <div id="{appid}"></div>
  {explainers[kind]}
  <div class="note">The score is a recognition score, not a fluency measure — nothing here is a certified test.</div>"""
    return title, desc, body, scripts


def p_conversation_lab(d):
    n = d["name"]
    blocks = []
    for dg in d["dialogues"]:
        rows = "".join(
            f"<tr><td><b>{E(l['sp'])}</b></td><td><b>{E(l['t'])}</b><br><span style=\"color:var(--muted)\">{E(l['r'])}</span></td><td>{E(l['hi'])}</td><td>{E(l['en'])}</td></tr>"
            for l in dg["lines"])
        blocks.append(f"<h2>{E(dg['title'])}</h2>\n<table class=\"tbl\"><thead><tr><th></th><th>{E(n)}</th><th>Hindi</th><th>English</th></tr></thead><tbody>{rows}</tbody></table>")
    return (f"{n} conversation scenarios",
            f"Everyday {n} dialogues in three languages: meeting someone, the tea stall, asking the way.",
            f"""{crumb(d, [( "../", "Practice"), (None, "Conversation")])}
  <h1>{E(n)} conversation scenarios</h1>
  <p class="lede">Everyday scenes with every line in English, Hindi and {E(n)}. Read them, then say each line aloud — shadowing beats re-reading.</p>
  {"".join(blocks)}""")


def p_review(d):
    n = d["name"]
    slug = d["slug"]
    items = "".join(
        f"<li><label style=\"display:flex;gap:10px;align-items:baseline;cursor:pointer\"><input type=\"checkbox\" data-w=\"{i}\"> <span><b>{E(w['t'])}</b> ({E(w['r'])}) — {E(w['en'])}</span></label></li>"
        for i, w in enumerate(d["review_deck"]))
    js = f"""<script>
(function(){{
  var K="ekg-review-{slug}", box=document.getElementById("deck"), n=document.getElementById("deck-n");
  var done={{}}; try{{done=JSON.parse(localStorage.getItem(K)||"{{}}");}}catch(e){{}}
  function paint(){{var c=0;box.querySelectorAll("input").forEach(function(b,i){{b.checked=!!done[i];if(b.checked)c++;}});n.textContent=c+" of {len(d['review_deck'])} sticking";}}
  box.addEventListener("change",function(){{box.querySelectorAll("input").forEach(function(b,i){{done[i]=b.checked;}});try{{localStorage.setItem(K,JSON.stringify(done));}}catch(e){{}}paint();}});
  paint();
}})();
</script>"""
    return (f"{n} review deck",
            f"The 20 core {n} words in one review list — tick them off as they stick. Saved on this device only.",
            f"""{crumb(d, [(None, "Review")])}
  <h1>{E(n)} review deck</h1>
  <p class="lede">The 20 {E(n)} words worth reviewing until they are automatic. Tick each one when you know it cold — progress saves on this device only.</p>
  <p class="note" id="deck-n"></p>
  <ul class="linklist" id="deck">{items}</ul>
  {js}""")


def p_progress(d):
    n = d["name"]
    slug = d["slug"]
    pages = [("basics", "Basics"), ("pronunciation", "Pronunciation"), ("conversation", "Conversation"),
             ("numbers", "Numbers"), ("grammar", "Grammar"), ("vocabulary", "Vocabulary"),
             ("food", "Food"), ("travel", "Travel"), ("shopping", "Shopping"),
             ("time-dates", "Time & dates"), ("daily-life", "Daily life"),
             ("practice/quiz", "Quiz (all topics)"), ("practice/typing", "Typing trainer"),
             ("practice/conversation", "Dialogues aloud"), ("review", "Review deck: 20/20")]
    for m in d.get("advanced_modules", []):
        pages.append((f"advanced/{m['slug']}", f"Advanced: {m['title']}"))
    items = "".join(
        f"<li><label style=\"display:flex;gap:10px;align-items:baseline;cursor:pointer\"><input type=\"checkbox\" data-w=\"{i}\"> <span><a href=\"../{s}/\">{t}</a></span></label></li>"
        for i, (s, t) in enumerate(pages))
    js = f"""<script>
(function(){{
  var K="ekg-progress-{slug}", box=document.getElementById("prog"), n=document.getElementById("prog-n");
  var done={{}}; try{{done=JSON.parse(localStorage.getItem(K)||"{{}}");}}catch(e){{}}
  function paint(){{var c=0;box.querySelectorAll("input").forEach(function(b,i){{b.checked=!!done[i];if(b.checked)c++;}});n.textContent=c+" of {len(pages)} done";}}
  box.addEventListener("change",function(){{box.querySelectorAll("input").forEach(function(b,i){{done[i]=b.checked;}});try{{localStorage.setItem(K,JSON.stringify(done));}}catch(e){{}}paint();}});
  paint();
}})();
</script>"""
    return (f"My {n} progress",
            f"Your {n} course checklist on this device: lessons, quiz, typing and review in one place.",
            f"""{crumb(d, [(None, "My progress")])}
  <h1>My {E(n)} progress</h1>
  <p class="lede">Your {E(n)} course checklist — this device only, no account, no sync. Honest rule: tick a lesson only after its quiz.</p>
  <h2>How to use this checklist</h2>
  <p>Tick a {E(n)} lesson only when you could explain it to somebody else, not when you have read it once. The list follows the course order for a reason: each unit assumes the one before it, and skipping the script lessons makes the later vocabulary much harder than it needs to be. If a lesson's quiz went badly, leave the tick off and repeat it after a night's sleep — spaced repetition is doing the work, not the checkbox.</p>
  <p class="note" id="prog-n"></p>
  <ul class="linklist" id="prog">{items}</ul>
  {js}""")


def dialogue_html(lines):
    out = []
    for ln in lines:
        out.append(f"<p><b>{E(ln['sp'])}:</b> {E(ln['t'])}<br><span style=\"color:var(--muted)\">{E(ln['r'])}</span> — {E(ln['hi'])} — <i>{E(ln['en'])}</i></p>")
    return "\n".join(out)


def p_advanced_hub(d):
    n = d["name"]
    items = "".join(
        f"<li><a href=\"{m['slug']}/\">{E(m['title'])}</a><span>{E(m['lede'])}</span></li>"
        for m in d["advanced_modules"])
    total = sum(len(m["words"]) for m in d["advanced_modules"])
    return (f"{n} advanced topics — beyond the basics",
            f"Advanced {n} vocabulary by topic: {total} extra words with phrases and dialogues.",
            f"""{crumb(d, [(None, "Advanced")])}
  <h1>{E(n)} advanced topics</h1>
  <p class="lede">Beyond the basics: {total} extra words across {len(d["advanced_modules"])} topics — every word in English, Hindi and {E(n)} with pronunciation. Each module adds its own quiz questions.</p>
  <ul class="linklist">{items}</ul>""")


def p_advanced_module(d, m):
    n = d["name"]
    body = f"""{crumb(d, [("{r}learn/" + d["slug"] + "/advanced/", "Advanced"), (None, m["title"])])}
  <h1>{E(n)}: {E(m["title"])}</h1>
  <p class="lede">{E(m["lede"])}</p>
  <h2>Words ({len(m["words"])})</h2>
  {tri_table(m["words"], col3=n)}
  <h2>Phrases</h2>
  {tri_table(m["phrases"], col3=n)}"""
    if m.get("dialogue"):
        dg = m["dialogue"]
        body += f'\n  <h2>Dialogue: {E(dg["title"])}</h2>\n  {dialogue_html(dg["lines"])}'
    body += '\n  <div class="note"><b>Quiz yourself.</b> This module adds questions to the <a href="../../practice/quiz/">topic quiz</a> — pick its topic and test yourself.</div>'
    return (f"{n}: {m['title']} — advanced words and phrases",
            f"Advanced {n} {m['title'].lower()}: {len(m['words'])} words, phrases and a dialogue.",
            body)


QUIZ_BANK_TMPL = """/* =========================================================
   EkGuru — {NAME} QUIZ BANK  (single source of truth · v1)
   ---------------------------------------------------------
   Same contract as js/hindi-quiz-bank.js: the data object is
   deliberately valid JSON; js/hindi-tools.js renders quiz,
   typing and worksheets from the EKGURU_*_ACTIVE globals this
   file sets. Conservative, checked {name} — quiz answers test
   recognition, never fluency.
   ========================================================= */
window.EKGURU_{GLOBAL}_QUIZ =
{data};
window.EKGURU_QUIZ_ACTIVE = window.EKGURU_{GLOBAL}_QUIZ;
window.EKGURU_QUIZ_NAME = "{slug}-quiz";
window.EKGURU_COURSE_LANG = {{ name: "{Name}", script: "{script}" }};
window.EKGURU_TYPING_ACTIVE =
{typing};
"""


# Reading-page order for prev/next navigation (hub, practice labs, review
# and progress are intentionally excluded — they are tools, not reading).
# ---------------------------------------------------------------- phase 3 blog posts
#
# PHASE 3 of the AdSense command: blog-style, readable posts (>= 1000 words) for
# the Learn tab. Ten post types per language; five of them already had a home
# (beginner / pronunciation / grammar / travel / numbers) and five had none, so
# they are new pages here. Every fact on these pages comes from
# tools/lang-data/<slug>.json — the tables are the data itself, never invented.
#
# Note on style: Python 3.11 is the supported interpreter, so no f-string in this
# block may contain a nested f-string or a backslash inside its expression part.
# Every fragment is therefore computed into a variable first.

PHASE3_POSTS = [
    # The count is not hard-coded to 100: the packs hold 100-104 words in these
    # eight groups, and the page states its own true total in the heading rather
    # than rounding it to a nicer number.
    ("common-words", "Most common words",
     "The highest-frequency words, in eight groups, with pronunciation for each."),
    ("mistakes", "Common mistakes",
     "The traps learners fall into in this language, and the fix for each one."),
    ("reading", "How to read the script",
     "A step-by-step path from letters to reading real sentences."),
    ("vs-hindi", "vs Hindi",
     "What Hindi speakers already know, and what trips everyone else up."),
    ("speaking-alone", "Practise speaking alone",
     "Shadowing, self-talk and a routine you can keep without a tutor."),
]

PHASE3_EXISTING = [
    ("beginner", "Beginner's guide", "How to learn from scratch, and the honest first 30 days."),
    ("pronunciation", "Alphabet, letter by letter", "Every letter with the sound it makes."),
    ("grammar", "Grammar basics", "Word order, verbs and the sentence ladder."),
    ("travel", "Phrases for travel", "Stations, hotels, fares and the phrases you will use."),
    ("numbers", "Numbers 1 to 100", "Counting, prices and time — with the counting pattern."),
]

# Language family, stated plainly. Hindi is this site's bridge language, so the
# "vs Hindi" guide has to be honest about how close the two really are.
LANG_FAMILY = {
    "bengali": ("Indo-Aryan", "a cousin of Hindi"),
    "gujarati": ("Indo-Aryan", "a cousin of Hindi"),
    "marathi": ("Indo-Aryan", "a cousin of Hindi"),
    "punjabi": ("Indo-Aryan", "a cousin of Hindi"),
    "urdu": ("Indo-Aryan", "the closest major relative of Hindi"),
    "kannada": ("Dravidian", "not related to Hindi at all"),
    "malayalam": ("Dravidian", "not related to Hindi at all"),
    "tamil": ("Dravidian", "not related to Hindi at all"),
    "telugu": ("Dravidian", "not related to Hindi at all"),
}


def _h2(t):
    return "  <h2>" + t + "</h2>"


def _h3(t):
    return "  <h3>" + t + "</h3>"


def _p(*paras):
    return "\n".join("  <p>" + p + "</p>" for p in paras)


def _ul(items):
    return "  <ul>\n" + "\n".join("    <li>" + x + "</li>" for x in items) + "\n  </ul>"


def _ol(items):
    return "  <ol>\n" + "\n".join("    <li>" + x + "</li>" for x in items) + "\n  </ol>"


def _callout(title, body):
    return '  <div class="note"><b>' + title + "</b> " + body + "</div>"


def _rows_table(rows, col3, with_hi=True):
    """en/native/roman table with a leading row number.

    with_hi=False for the review deck, which stores only the target language and
    its meaning — printing an empty Hindi column would be a lie about the data.
    """
    out = ['<table class="tbl tri"><thead><tr><th>#</th><th>English</th>']
    if with_hi:
        out.append('<th>Hindi</th>')
    out.append('<th>' + E(col3) + '</th><th>Say it</th></tr></thead><tbody>')
    for i, w in enumerate(rows, 1):
        cells = ["<tr><td>" + str(i) + "</td><td>" + E(w.get("en", "")) + "</td>"]
        if with_hi:
            cells.append("<td>" + E(w.get("hi", "")) + "</td>")
        cells.append("<td><b>" + E(w["t"]) + "</b></td><td>" + E(w["r"]) + "</td></tr>")
        out.append("".join(cells))
    out.append("</tbody></table>")
    return "\n".join(out)


def _num_table(rows, lang):
    out = ['<table class="tbl tri"><thead><tr><th>#</th><th>Hindi</th><th>' + E(lang)
           + '</th><th>Say it</th></tr></thead><tbody>']
    for w in rows:
        out.append("<tr><td><b>" + str(w["n"]) + "</b></td><td>" + E(w["hi"]) + "</td>"
                   "<td><b>" + E(w["t"]) + "</b></td><td>" + E(w["r"]) + "</td></tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def _pf_table(d):
    """past / future sentences, four columns."""
    out = ['<table class="tbl tri"><thead><tr><th>English</th><th>Hindi</th><th>'
           + E(d["name"]) + '</th><th>Say it</th></tr></thead><tbody>']
    for x in d["past_future"]:
        out.append("<tr><td>" + E(x["en"]) + "</td><td>" + E(x["hi"]) + "</td><td><b>"
                   + E(x["t"]) + "</b></td><td>" + E(x["r"]) + "</td></tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def _guide_links(d, here):
    """Cross-links between the ten phase-3 posts, minus the current one."""
    items = []
    for slug, label, blurb in PHASE3_EXISTING + PHASE3_POSTS:
        if slug == here:
            continue
        link = '<a href="../' + slug + '/">' + E(label) + " — " + E(d["name"]) + "</a>"
        items.append("<li>" + link + "<span>" + E(blurb) + "</span></li>")
    return ('<h2>More guides in this course</h2>\n  <ul class="linklist">\n    '
            + "\n    ".join(items) + "\n  </ul>")


# ---------------------------------------------------------------- 5 new posts

def p_common_words(d):
    n = d["name"]
    groups = [
        ("Greetings and politeness", d["greetings"]),
        ("Pronouns", d["pronouns"]),
        ("The 18 verbs you will use every day", d["verbs"]),
        ("Family", d["family"]),
        ("Colours", d["colors"]),
        ("Core nouns", d["core_nouns"]),
        ("Time words", d["time_words"]),
        ("Days of the week", d["days"]),
    ]
    total = sum(len(rows) for _t, rows in groups)
    blocks = []
    for title, rows in groups:
        blocks.append(_h2(title + " (" + str(len(rows)) + ")"))
        blocks.append(_rows_table(rows, n))
    tables = "\n".join(blocks)

    lede = ("If you learn one thing first, learn this. Every word below is high-frequency — you will hear it in "
            "the first hour of any real conversation. There are " + str(total) + " words here, in eight groups you "
            "can take one at a time, and every one is written three ways: <b>English</b>, <b>Hindi</b> and <b>"
            + E(n) + "</b> (" + E(d["native"]) + ") with a pronunciation column.")
    why = _p(
        "<b>Why start with frequency?</b> A language is not a wall you climb; it is a snowball. The first "
        + str(total) + " words unlock the parts of " + E(n) + " that repeat every day — greeting someone, saying "
        "what you want, saying who you mean, and saying when. Grammar without vocabulary is silent, and vocabulary "
        'without grammar is a shopping list. Start here, then let the <a href="../grammar/">grammar page</a> show '
        "you how to bolt these words together.",
        "A useful rule of thumb: with a few hundred high-frequency words and one verb pattern, a learner can "
        "already manage greetings, shops and simple questions. This page is the densest part of that set.")
    howto = _callout(
        "How to use this page.",
        "Do not swallow all " + str(total) + " words in one sitting. Take one group a day, read the column aloud, "
        "cover the pronunciation column and say each word. Then test yourself with the "
        '<a href="../practice/quiz/">topic quiz</a> and keep the ones that will not stick in the '
        '<a href="../review/">review deck</a>.')
    after = _h2("What to do after these " + str(total)) + _p(
        "You now own the skeleton of " + E(n) + ". The next step is not more words — it is sentences. Take five "
        "verbs from the list above and build one sentence each about your own day. Then read the "
        '<a href="../grammar/">grammar basics guide</a> for the word order (' + E(d["sov"]["t"]) + "), and the "
        '<a href="../speaking-alone/">speaking-alone plan</a> so the words come out of your mouth and not just '
        "off the page.")
    body = "\n".join([
        crumb(d, [(None, "100 most common words")]),
        "  <h1>" + E(n) + " — the " + str(total) + " most common words</h1>",
        '  <p class="lede">' + lede + "</p>",
        why, howto, tables, after,
        _guide_links(d, "common-words"),
    ])
    return ("{0} — the {1} most common words with pronunciation".format(n, total),
            "The {0} highest-frequency {1} words in eight groups — greetings, pronouns, verbs, family, colours, "
            "nouns, time and days — each with Hindi, {1} script and how to say it.".format(total, n),
            body)


def p_mistakes(d):
    n = d["name"]
    lede = ("Nobody fails at " + E(n) + " because it is impossible. People stall because they repeat five or six "
            "specific habits for months. Here they are, honestly, with the fix for each.")
    lede2 = _p("None of these mistakes means you are bad at languages. They are the normal fault lines of "
               + E(n) + " — the places where your instincts, usually English instincts, pull in the wrong "
               "direction.")
    m1 = _h2("Mistake 1 — Translating word for word") + _p(
        "English builds sentences as <b>subject – verb – object</b>. " + E(n) + " does not. The pattern here is <b>"
        + E(d["sov"]["t"]) + "</b> — " + E(d["sov"]["en"]) + ".",
        "If you translate one English word at a time you get sentences that are technically understandable and "
        "permanently foreign. Train the other order until it feels normal: take three sentences you would say today "
        "in English and rebuild them in the " + E(n) + " order, out loud, before you look anything up.")
    m1f = _callout("The fix.", "Learn sentence patterns, not words in isolation. The "
                  '<a href="../grammar/">grammar page</a> has the present-tense table to copy — say every row '
                  "aloud once and you have the shape of the language.")
    m2 = _h2("Mistake 2 — Skipping the script") + _p(
        "The " + E(d["script_name"]) + " looks like the biggest mountain at the start, so learners put it off and "
        "survive on romanisation. " + E(d["script_note"]),
        "Romanisation is a crutch that quietly caps your ceiling: you cannot read a menu, a sign or a message, and "
        "your pronunciation drifts further from the real thing every week, because roman letters carry English "
        "sounds into " + E(n) + ".")
    m2f = _callout("The fix.", 'Twenty minutes a day for two weeks on the '
                  '<a href="../pronunciation/">letter tables</a>, then type every word you learn in the '
                  '<a href="../practice/typing/">typing trainer</a>. The '
                  '<a href="../reading/">step-by-step reading guide</a> walks the whole path.')
    m3 = _h2("Mistake 3 — Assuming gender works like English") + _p(
        E(d["gender_title"]) + ".",
        "English hides gender except in pronouns, so learners either ignore it or guess. Guessing is worse than "
        "ignoring, because the shape of a noun is usually where its gender lives, and the verb often agrees with it.")
    m3f = _callout("The fix.", "Learn every new noun <i>with</i> a sentence you can use it in, never as a bare word, "
                  "and check the past-tense forms in the tables on this site before you memorise them.")
    m4 = _h2("Mistake 4 — Treating the verb as the hard part") + _p(
        E(d["present_note"]),
        "Learners hunt for the exact equivalent of \"I am doing\" or \"I have done\", and instead of accepting that "
        + E(n) + " divides the work differently, they freeze.")
    m4f = _callout("The fix.", 'Practise the I/you/he rows of the <a href="../grammar/">present-tense table</a> '
                  "until they are automatic, then change only the verb. The "
                  '<a href="../practice/quiz/">quiz</a> mixes them so you cannot copy the tense you saw last.')
    m5 = _h2("Mistake 5 — Getting negation wrong") + _p(
        E(d["negation_title"]) + ".",
        "Say \"I don't understand\" wrong once at the wrong moment and you will avoid the phrase for a month. "
        "Negation is short, frequent, and worth an hour of your week.")
    m5f = _callout("The fix.", "Take any five sentences you already know and make each one negative. Drill them as a "
                  "pair: positive, negative, positive, negative.")
    m6 = _h2("Mistake 6 — Counting with English grammar") + _p(
        E(d["counting_note"]),
        "Numbers feel easy, so learners skip the small differences around counting — and then get tripped by "
        "\"two people\" or \"three books\" the first time they need them in a shop.")
    m6f = _callout("The fix.", 'Use the <a href="../numbers/">numbers and counting guide</a> and count real things '
                  "in your house: two chairs, three books, five people. Context is what makes the pattern stick.")
    m7 = _h2("Mistake 7 — Waiting until you are ready to speak") + _p(
        "Almost every learner waits for a magic morning when the language suddenly feels safe. That morning never "
        "comes. Speaking badly early is not a failure mode; it is the method.",
        "Start with the phrases you cannot get wrong — " + E(d.get("survival_trio", "greetings, thanks, and where "
        "is X")) + " — and use them with a real person at the first opportunity.")
    m7f = _callout("The fix.", 'The <a href="../speaking-alone/">speaking-alone routine</a> lets you build the habit '
                  "privately before you use it publicly. Ten minutes a day beats one three-hour session a week.")
    check = _h2("A two-minute self-check") + _ul([
        "Can you read a simple sentence aloud without the roman column?",
        "Can you make five sentences negative on demand?",
        "Do you know the gender behaviour of the last ten nouns you learned?",
        "Can you count to twenty and use a number with a noun?",
        "Did you say anything out loud in the last 24 hours?"])
    close = _p("Every \"no\" is not a verdict — it is just the next hour of study, with a clear target.",
               "And one asymmetry worth remembering: understanding a language always runs ahead of speaking it, by "
               "months. You will feel like you are failing long after you have started succeeding. The corrections "
               "above are not there to make you doubt yourself — they are there so that the effort you are already "
               "putting in stops leaking.")
    body = "\n".join([
        crumb(d, [(None, "Common mistakes")]),
        "  <h1>Common mistakes when learning " + E(n) + " — and how to fix them</h1>",
        '  <p class="lede">' + lede + "</p>", lede2,
        m1, m1f, m2, m2f, m3, m3f, m4, m4f, m5, m5f, m6, m6f, m7, m7f, check, close,
        _guide_links(d, "mistakes"),
    ])
    return ("Common mistakes when learning {0} — and how to fix them".format(n),
            "The {0} traps that slow learners down: word order, gender, negation, counting and the script — each "
            "with the fix and a drill.".format(n),
            body)


def p_reading(d):
    n = d["name"]
    vowels = d["vowels"]
    consonants = d["consonants"]
    step1 = _h2("Step 1 — Meet the vowels") + _p(
        "The " + E(d["script_name"]) + " has " + str(len(vowels)) + " vowels, shown below with the sound each one "
        "makes.",
        "Read the table left to right, out loud. Do not try to memorise it in one pass: recognition first, recall "
        "later. Two passes today and two tomorrow beats an hour tonight.") + alpha_table(vowels)
    step2 = _h2("Step 2 — Meet the consonants") + _p(
        "Then the " + str(len(consonants)) + " consonants. This is the part people find intimidating, and it is "
        "mostly an illusion created by an unfamiliar script: the table below gives you the sound of every letter, "
        "in words you already know.") + alpha_table(consonants)
    pace = _callout("A realistic pace.", "Two letters a day with five minutes of writing each. In about three weeks "
                    "the alphabet stops being a wall and becomes a slightly slow tool — which is exactly what it "
                    "should feel like.")
    step3 = (_h2("Step 3 — Read numbers first") + _p(
        "Numbers are the ideal first reading exercise: short, repetitive, and you already know what they mean from "
        'the <a href="../numbers/">counting page</a>. Read these out loud without looking at the Hindi or English '
        "column, then cover the last column and read them again. If you can read 1–10, you can read a price board.")
        + _num_table(d["numbers"][:10], n))
    step4 = _h2("Step 4 — Read real words") + _p(
        "Now real vocabulary. These twelve words are the ones you will use most; read the " + E(n) + " column first "
        "and only then check the pronunciation column.") + _rows_table(d["review_deck"][:12], n, with_hi=False)
    step5 = _h2("Step 5 — Read a whole sentence") + _p(
        "Reading words is one skill; reading a sentence is a second one. Start with the word order you already "
        "know — <b>" + E(d["sov"]["t"]) + "</b> — then read slowly, then at speaking speed.",
        "Read each phrase below aloud three times. When you can read them without pausing, you have crossed from "
        "decoding to reading.") + tri_table(d["daily_phrases"][:6], col3=n)
    step6 = _h2("Step 6 — Make it a habit") + _ol([
        "Five minutes reading the letter tables aloud, every day.",
        "Five minutes typing the words you learned in the practice typing trainer.",
        "Once a week, re-read a page you have already studied and notice how much faster it goes.",
        "Never read only in your head: the mouth learns the script faster than the eye does."])
    close = _p('When reading starts to feel routine, push on to the <a href="../grammar/">grammar basics</a> and '
               'the <a href="../speaking-alone/">speaking-alone plan</a> — reading is the door, not the room.')
    lede = (E(d["script_note"]) + " Below is the path that gets you from \"those are just shapes\" to reading a "
            "real " + E(n) + " sentence, in six steps you can work through in a fortnight of short sessions.")
    body = "\n".join([
        crumb(d, [(None, "How to read the script")]),
        "  <h1>How to read " + E(n) + " script — a step-by-step guide</h1>",
        '  <p class="lede">' + lede + "</p>",
        step1, step2, pace, step3, step4, step5, step6, close,
        _guide_links(d, "reading"),
    ])
    return ("How to read {0} script — a step-by-step guide".format(n),
            "A practical path to reading {0}: the {1} letter by letter, then real words and numbers, in the order "
            "that actually works.".format(n, d["script_name"]),
            body)


def p_vs_hindi(d):
    n = d["name"]
    fam, rel = LANG_FAMILY.get(d["slug"], ("", "related to Hindi in different ways"))
    same_script = "Devanagari" in d.get("script_name", "")
    if same_script:
        script_para = ("Good news first: " + E(n) + " is written in " + E(d["script_name"]) + ", the same script "
                       "Hindi uses. If you can read Hindi, you can already read the letters on every " + E(n) +
                       " page of this course — you are learning new words and new grammar, not a new alphabet.")
    else:
        script_para = ("First, the difference you cannot ignore: Hindi is written in Devanagari, and " + E(n) +
                       " is written in " + E(d["script_name"]) + ". That is a separate reading skill to build. " +
                       E(d["script_note"]))
    lede = ("This site teaches every " + E(n) + " word in three languages at once, with Hindi sitting right next to "
            "English, which hides a fair question: if you already speak Hindi, how much of " + E(n) + " do you get "
            "for free? " + E(n) + " is " + E(fam.lower()) + " — " + E(rel) + ". Here is the honest breakdown.")
    script = _h2("The script") + _p(script_para)
    order = _h2("Word order") + _p(
        "Here the two languages agree: " + E(n) + " puts the verb last. The pattern is <b>" + E(d["sov"]["t"]) +
        "</b> — " + E(d["sov"]["en"]) + ". Hindi works the same way, so if Hindi word order is already in your ear, "
        "that is one fewer thing to unlearn.")
    words = _h2("Words you may already know") + _p(
        "Look down the Hindi and " + E(n) + " columns together. Where the two are similar, that is usually a word "
        "that travelled — through Sanskrit, through Persian, or through centuries of trade and administration. "
        "Where they differ, the everyday word is usually native. Numbers are the clearest test:") \
        + _num_table(d["numbers"][:10], n) + _p(
        "Compare each Hindi number with its " + E(n) + " partner above. Similar ones are free vocabulary. The "
        "different ones are words you must memorise deliberately — and they are worth it, because a number is the "
        "word you use when you buy something.")
    side = _h3("Everyday words, side by side") + _rows_table(d["family"][:6] + d["colors"][:4], n)
    warn = _callout("Do not assume — check.",
                    "The most common mistake a Hindi speaker makes is assuming a similar-sounding word means exactly "
                    "the same thing. It usually means something close, and \"close\" is where misunderstandings "
                    "live. Read the English column too, even when the Hindi one looks familiar.")
    gram = _h2("Grammar: where the two part company") + _p(
        "<b>Gender.</b> " + E(d["gender_title"]) + ".",
        "<b>Verbs.</b> " + E(d["present_note"]),
        "<b>Negation.</b> " + E(d["negation_title"]) + ".",
        "<b>Counting.</b> " + E(d["counting_note"]))
    if_hi = _h2("If you already speak Hindi") + _ul([
        "Skip nothing: the script and word order transfer, the grammar does not.",
        "Use the Hindi column as a shortcut for meaning, then read the " + E(n) + " column aloud twice.",
        "Watch the verb endings first — that is where the transfer stops working.",
        "Watch gender agreement in the past tense, the usual first serious stumble."])
    if_not = _h2("If you do not speak Hindi") + _p(
        "Then treat the Hindi column as a bonus rather than a prerequisite: every page on this site gives you "
        "English and " + E(n) + " with pronunciation, so you can learn " + E(n) + " without a word of Hindi. What "
        "the Hindi column buys you is a second reference point when a word refuses to stick.",
        "It is also worth knowing that Hindi is a genuinely useful bridge language in India: the numbers and a few "
        "hundred shared words turn up everywhere, and the reflex of putting the verb at the end is the same.")
    sound = _h2("Pronunciation: the part nobody warns you about") + _p(
        "Similar vocabulary and a shared word order make a Hindi speaker feel at home early, which is exactly when "
        "pronunciation gets neglected. Words that look familiar are the ones you are most likely to say with Hindi "
        "vowels and Hindi stress.",
        "The fix is unglamorous: read the pronunciation column even on the words you think you already know, and "
        "read the letter tables once properly, out loud. Ten minutes of honesty at the start saves a year of "
        "corrections later — and people will understand you far more easily once the sounds are right.")
    if fam:
        fam_line = E(n) + " is " + E(fam.lower()) + " — " + E(rel) + "."
    else:
        fam_line = E(n) + " and Hindi are related in different ways."
    short = _h2("The short version") + _ul([
        fam_line,
        "Same word order" + (" and the same script" if same_script else ", different script"),
        "A comparable verb-last sentence shape, with different verb machinery",
        "Shared vocabulary where history put it; native vocabulary where it matters most — everyday life"])
    close = _p('Now put it to work: the <a href="../common-words/">100 most common words</a> page is laid out so '
               'you can compare the two columns line by line, and the <a href="../mistakes/">mistakes guide</a> '
               "covers the traps that catch bilingual speakers in particular.",
               "The comparison is also a useful test of your own intuition. Read a handful of words you think you "
               "already know, cover the English column, and see whether the Hindi meaning is genuinely the same. "
               "Where it is not, you have found the exact place to spend your next study session.")
    body = "\n".join([
        crumb(d, [(None, E(n) + " vs Hindi")]),
        "  <h1>" + E(n) + " vs Hindi — what's different and what's similar</h1>",
        '  <p class="lede">' + lede + "</p>",
        script, order, words, side, warn, gram, if_hi, if_not, sound, short, close,
        _guide_links(d, "vs-hindi"),
    ])
    return ("{0} vs Hindi — what is different and what is similar".format(n),
            "How close {0} and Hindi really are: script, word order, verbs, gender and vocabulary — with the words "
            "you already know if you speak Hindi.".format(n),
            body)


def p_speaking_alone(d):
    n = d["name"]
    first = d["greetings"][0]
    dlg_html = ""
    if d.get("dialogues"):
        dlg = d["dialogues"][0]
        dlg_html = (_h2("Shadow the dialogues (" + str(len(d["dialogues"])) + " on this site)")
                    + _p("Below is the first dialogue in the course, \"" + E(dlg["title"]) + "\". Read it aloud line "
                         "by line, copying the rhythm rather than the words. Shadowing means speaking <i>at the "
                         "same time</i> as the model, not after it — that is what forces your mouth to keep up.")
                    + dialogue_html(dlg["lines"])
                    + _p("Then close the page and say the whole conversation from memory. You will lose half of "
                         "it. Do the same tomorrow and you will not."))
    lede = ("You can get genuinely far in " + E(n) + " without a teacher or a conversation partner. Not all the "
            "way — nobody learns to handle real speech alone — but far enough that your first real conversation "
            "will not be your first spoken " + E(n) + " sentence. Here is the routine, in the order it should be "
            "built.")
    s1 = _h2("1. Shadow before you speak") + _p(
        "Shadowing is copying speech in real time. Take a phrase from the "
        '<a href="../conversation/">conversation page</a> — ' + E(first["t"]) + " (" + E(first["r"]) + ") is a good "
        "first one — and say it while you read it, out loud, five times. Then say it without the page. The point is "
        "not comprehension; it is making your mouth move in an unfamiliar way until it stops being unfamiliar.")
    s2 = _h2("2. Talk to yourself on a schedule") + _p(
        "Narrate your day in " + E(n) + " for two minutes, twice a day. Keep it dull on purpose: what you are "
        "doing, what you want, what is next. Dull sentences repeat, and repeated sentences are the ones that stick.",
        'Use the <a href="../daily-life/">daily phrases</a> as scaffolding at first, then swap in words from the '
        '<a href="../common-words/">100 most common words</a>. If you cannot say a sentence, say the closest one '
        "you can, note the gap, and look it up afterwards. Gaps are data.")
    s3 = _h2("3. Record yourself once a week") + _ol([
        "Read ten words from the pronunciation letter tables aloud and record them.",
        "Play it back and compare with the pronunciation column on the page. Listen for sounds, not for accent.",
        "Record the same ten words next week. The improvement is the motivation."]) + _p(
        "Recording is uncomfortable for about three weeks, and then it becomes the most useful habit on this list, "
        "because it is the only way to hear what other people actually hear.")
    s4 = _h2("4. Drill the sounds you cannot hear") + _p(
        E(d["script_note"]),
        "That matters for speaking: the letters you cannot distinguish are the letters you will not pronounce "
        "differently. Take the vowels and consonants marked as tricky on the "
        '<a href="../pronunciation/">pronunciation page</a> and make one sentence with each, then say it until it '
        "is smooth.")
    s4b = _callout("A useful trick.", "Exaggerate the difficult sound on purpose while practising. You will feel "
                   "silly, and you will hear the difference. When you drop back to normal speed your mouth will be "
                   "in the right place.")
    s5 = _h2("5. Feed the habit with spaced repetition") + _p(
        "Speaking practice fails when the words are not there yet. Spend ten minutes on the "
        '<a href="../review/">review deck</a> or the <a href="../practice/typing/">typing trainer</a> every day, so '
        "that speaking practice is about building sentences rather than hunting for vocabulary.")
    s6 = _h2("6. Know when you are ready for a person") + _ul([
        "You can greet, thank and ask where something is without translating in your head.",
        "You can say what you did yesterday, even badly.",
        "You can ask someone to repeat themselves — and catch the first three words of the answer."]) + _p(
        "That is the point to find a human: a tutor, a colleague, a market stall, an online exchange. Before that, "
        "the person is mostly doing the work your own routine should be doing.")
    s7 = _h2("The honest limits of practising alone") + _p(
        "No amount of shadowing teaches you to understand an unfamiliar voice at natural speed, and it cannot "
        "correct an error you cannot hear. A routine alone is a strong bridge and a bad destination. Our tutors "
        "teach Hindi one to one, and this " + E(n) + " course stays free either way.")
    s8 = _h2("The daily twenty minutes") + _ol([
        "5 minutes: read the letter tables aloud.",
        "5 minutes: ten words from the review deck, spoken and typed.",
        "5 minutes: shadow one dialogue or narrate your day.",
        "5 minutes: write two sentences — including one negative sentence."]) + _p(
        "Keep it that small and it will survive a busy week, which is the only test that matters.")
    body = "\n".join([
        crumb(d, [(None, "Practise speaking alone")]),
        "  <h1>How to practise speaking " + E(n) + " alone — a realistic plan</h1>",
        '  <p class="lede">' + lede + "</p>",
        s1, dlg_html, s2, s3, s4, s4b, s5, s6, s7, s8,
        _guide_links(d, "speaking-alone"),
    ])
    return ("How to practise speaking {0} alone — a realistic plan".format(n),
            "A no-tutor speaking routine for {0}: shadowing, self-talk, recording yourself and spaced repetition — "
            "plus the honest limits of practising alone.".format(n),
            body)


# ---------------------------------------------------------------- deepening the five that already existed

def deep_beginner(d):
    n = d["name"]
    greetings = d.get("greetings") or []
    first_greeting = greetings[0] if greetings else {}
    greeting_target = E(first_greeting.get("t") or n)
    greeting_roman = E(first_greeting.get("r") or "")
    greeting_meaning = E(first_greeting.get("en") or "greeting")
    script_name = E(d.get("script_name") or "writing system")
    script_note = E(d.get("script_note") or "Practise reading the script alongside its romanisation.")
    difficulty = E(d.get("difficulty") or "Build the routine from short, repeatable sessions.")
    weeks = _ol([
        "<b>Week 1 — sounds.</b> The pronunciation vowel and consonant tables, two letters a day, said aloud. "
        "Add five greetings from the conversation page.",
        "<b>Week 2 — numbers and reading.</b> Numbers 1–20 from the numbers guide, then the tens. Read each one "
        "aloud without the roman column.",
        "<b>Week 3 — your first sentences.</b> The grammar page, present tense, I/you/we rows. Build five sentences "
        "about your own day, then make each one negative.",
        "<b>Week 4 — real situations.</b> Food, shopping and travel phrases. Role-play them out loud as if the "
        "person were in front of you."])
    plan = _h2("Your first 30 days, week by week") + _p(
        "Most courses fail because they never say what to do <i>on Tuesday</i>. Here is a four-week plan built on "
        "the pages of this site, sized for twenty minutes a day. If you miss a day, do not restart the week — just "
        "carry on. For " + E(n) + ", anchor the first session to <b>" + greeting_target + "</b> (" + greeting_roman +
        "): " + greeting_meaning + ". Then keep this " + script_name + " note beside you: " + script_note) + weeks
    keep = _h2("What to learn first — and what to ignore for now") + _ul([
        "<b>Learn now:</b> greetings, pronouns, numbers to 20, the present tense, and the words you use about "
        "yourself.",
        "<b>Ignore for now:</b> literary vocabulary, perfect tenses, regional dialect, and every exception you meet "
        "in a grammar table before it appears in a real sentence.",
        "<b>Never skip:</b> pronunciation. Everything you drill later is built on how you said it first."])
    ready = _callout("How to know you are ready to move on.",
                     "You can read ten short words aloud without help, greet someone politely, count to twenty, and "
                     "build five simple sentences about your day. That is the whole beginner bar — there is nothing "
                     "mysterious waiting behind it.")
    hello = _h2("How to say hello, out loud") + tri_table(d["greetings"][:8], col3=n) + _p(
        "Say every row aloud twice, then close the table and try from memory. Start with <b>" + greeting_target +
        "</b> (" + greeting_roman + ") — “" + greeting_meaning + "” — and then return to the " + script_name +
        " spelling without the romanisation. The other greetings on this " + E(n) + " table show how the setting "
        "or relationship changes the words you choose.")
    memory = _h2("How to remember the words") + _p(
        "Three techniques do most of the work in the first month, and none of them requires an app. For " +
        E(n) + ", make the first remembered item <b>" + greeting_target + "</b> (" + greeting_roman +
        ") rather than a disconnected sound on a list.",
        "<b>Say it out loud.</b> Words you only read are stored weakly. Compare " + greeting_target + " with its " +
        greeting_roman + " reading, then say it again without looking. The " + script_name + " detail above tells you " +
        "what to notice in the written form.",
        "<b>Attach it to something.</b> Put " + greeting_target + " into a real scene: imagine the person, choose " +
        "the greeting that fits, then add one sentence about your own day using a word from the " + E(n) +
        " vocabulary table. A word learned in a true sentence is easier to retrieve than one learned alone.",
        "<b>Meet it again.</b> Schedule " + greeting_target + " for a short review on three separate days, then use " +
        "the " + E(n) + " review deck and quiz to check other words. Five minutes spread across the week is more useful " +
        "than one hour of cramming.") + _ul([
        "<b>Ten spare minutes?</b> Read the letter tables aloud and run ten words through the review deck.",
        "<b>Thirty spare minutes?</b> Twenty minutes on the current week's page, then ten minutes of quiz questions.",
        "<b>A whole evening?</b> Do not study for three hours. Do the usual twenty minutes and watch something in "
        "the language instead — listening is not wasted time."]) + _p(
        "The learners who reach the end are not necessarily the ones with the most free time. They are the ones "
        "who keep a " + E(n) + " session small enough to survive a bad week: repeat " + greeting_target +
        ", review one card, and return tomorrow.")
    expects = _h2("What this level is, and what it is not") + _p(
        "The beginner stage is not a smaller version of fluency. For " + E(n) + ", its first finish line is concrete: " +
        "read <b>" + greeting_target + "</b> without leaning on " + greeting_roman + ", handle the numbers on the page, " +
        "and build simple sentences about your own life in the " + script_name + ".",
        "It is normal at this stage to understand far more than you can say, and it is normal to forget a word you "
        "learned yesterday. Neither means you are doing it wrong. In " + E(n) + ", keep the daily session short, say " +
        "the greeting and its romanisation aloud, then return to the written form. Here is the language-specific " +
        "difficulty to plan around: " + difficulty,
        "When the four weeks above are done, do not jump to advanced material. Take one topic at a time — food, " +
        "shopping, travel or time — and make it usable before moving on. For " + E(n) + ", your check is to read " +
        "<b>" + greeting_target + "</b>, recall its meaning, and then continue with a word from the next topic. A learner " +
        "who can really use five topics will out-converse a learner who has skimmed fifteen.",
        "Treat the difficulty note as a planning cue, not a deadline. In " + E(n) + ", revisit the written greeting " +
        "and its romanisation each week; notice when you can read " + greeting_target + " without leaning on " +
        greeting_roman + ", then move on to the next line in the table.")
    return plan + keep + ready + hello + memory + expects


def refresh_beginner_content(slug):
    """Refresh only the generator-owned beginner depth section in a live page.

    Legacy pages carry shared layers (storybook, shell, consent, theme, review
    notice and editorial metadata). A content-only refresh preserves those
    layers and, importantly, never rewrites robots or canonical decisions.
    """
    if not slug or not slug.isascii() or not slug.isalpha() or slug.lower() != slug:
        raise ValueError("expected one language slug")
    data_path = os.path.join(ROOT, "tools", "lang-data", slug + ".json")
    page_path = os.path.join(ROOT, "learn", slug, "beginner", "index.html")
    if not os.path.isfile(data_path) or not os.path.isfile(page_path):
        raise FileNotFoundError("missing language data or beginner page for " + slug)
    with open(data_path, encoding="utf-8") as f:
        d = json.load(f)
    with open(page_path, encoding="utf-8") as f:
        page = f.read()

    start = "<h2>Your first 30 days, week by week</h2>"
    end = "<h2>More guides in this course</h2>"
    if page.count(start) != 1 or page.count(end) != 1 or page.index(start) >= page.index(end):
        raise ValueError("beginner content boundaries are missing or ambiguous: " + page_path)
    left = page.index(start)
    right = page.index(end, left)
    section = deep_beginner(d)
    # The page already has its own indentation immediately before the heading.
    # Remove the generator's leading indentation so it is not doubled on insert.
    if section.startswith("  "):
        section = section[2:]
    refreshed = page[:left] + section + page[right:]
    if refreshed != page:
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(refreshed)
        print(f"{slug}: refreshed beginner content only; page shell and indexing preserved")
    else:
        print(f"{slug}: beginner content already current")


def deep_pronunciation(d):
    n = d["name"]
    keys = ("no ", "not ", "never", "unlike", "harder", "between", "roll", "breath", "both")
    tricky = [c for c in d["consonants"] if any(w in c["hint"].lower() for w in keys)][:5]
    tricky_html = ""
    if tricky:
        items = ["<b>" + E(c["t"]) + "</b> (" + E(c["r"]) + ") — " + E(c["hint"]) for c in tricky]
        tricky_html = (_h2("The letters that actually need work")
                       + _p("Every alphabet has a few letters that learners hear as \"the same\". They are not the "
                            "same, and they are the ones worth drilling deliberately.")
                       + _ul(items))
    read10 = (_h2("Read these ten words out loud")
              + _p("Reading practice works better with real words than with letter drills. These are ten "
                   "high-value words from the course — read the " + E(n) + " column first, then check the "
                   "pronunciation column underneath.")
              + _rows_table(d["review_deck"][:10], n, with_hi=False))
    write = (_h2("Writing: hand before keyboard")
             + _p("Write each new letter by hand five times. Handwriting forces you to notice the strokes and the "
                  "joins, which typing lets you skip. Once you can write it, the typing trainer turns that knowledge "
                  "into speed.",
                  "A realistic goal for the first fortnight is not beauty, it is legibility to yourself. "
                  "Handwriting in " + E(n) + " improves the same way it does in English: slowly, and by doing it in "
                  "short bursts often.")
             + _callout("When you get stuck.",
                        "If a letter refuses to stick, it is almost always because you are learning it in isolation. "
                        "Attach it to a word you already know from the numbers or greetings tables, and learn the "
                        "pair."))
    fortnight = _h2("The first fortnight, day by day") + _ol([
        "<b>Days 1–5.</b> Two vowels a day, written by hand five times each and read aloud. No vocabulary yet.",
        "<b>Days 6–10.</b> Two consonants a day the same way. By now you should recognise the vowels on sight.",
        "<b>Days 11–12.</b> Read the numbers table without the roman column. Slow is fine — accurate is the goal.",
        "<b>Day 13.</b> Read the ten words above and check yourself against the pronunciation column.",
        "<b>Day 14.</b> Type ten words in the practice typing trainer, then read the greetings table aloud unaided."])
    fortnight += _p("Fourteen short sessions is genuinely enough to read slowly, which is all the beginner stage "
                    "asks. Everything after that is speed, and speed comes from reading things you already "
                    "understand.")
    return tricky_html + read10 + write + fortnight


def deep_grammar(d):
    n = d["name"]
    ladder = _h2("The sentence ladder") + _p(
        "Do not learn grammar as a list of rules. Learn it as a ladder with seven rungs, where every rung is "
        "something you can say out loud today.") + _ol([
        "<b>Say what you are.</b> Simple I-sentences with no verb change.",
        "<b>Say what you want.</b> The same pattern with a noun from the common words list.",
        "<b>Say what you do.</b> The present-tense table above, first person only.",
        "<b>Say what someone else does.</b> The same table, third person — this is where the endings move.",
        "<b>Say what happened.</b> Past tense, five sentences about yesterday.",
        "<b>Say what will happen.</b> Future tense, five sentences about tomorrow.",
        "<b>Say what does not happen.</b> Negative forms of five sentences you have already built."])
    pf = _h2("Past and future, in five sentences each") + _pf_table(d)
    small = (_h2("Small words, big sentences") + _p(
        "Two groups of small words turn correct sentences into natural ones: the little words that mean in, at or "
        "to, and the words used when counting things.") + tri_table(d["postpositions"], col3=n)
        + _p("And the counting words:") + tri_table(d["classifiers"], col3=n))
    rule = _callout("The grammar rule that matters most.",
                    E(d["present_note"]) + " Learn the pattern, then change one thing at a time — verb, then "
                    "person, then tense. Learners who change everything at once produce sentences they cannot debug.")
    return ladder + pf + small + rule


def deep_travel(d):
    n = d["name"]
    tp = d["travel_phrases"][0]
    station = (_h2("At the station") + _h3("Buying a ticket") + _p(
        "Travel conversations are short, repetitive and predictable — which makes them the best possible practice "
        "ground. The exchange below covers almost every ticket window; learn your half of it until it is automatic.")
        + _ul([
            "<b>You:</b> " + E(tp["t"]) + " (" + E(tp["r"]) + ") — " + E(tp["en"]),
            "<b>You:</b> say the destination, then the number of tickets using a number from the table below.",
            "<b>Them:</b> a number. You will hear it faster than you expect — listen for the tens.",
            "<b>You:</b> thank them. This is the moment the greeting table pays off."]))
    hotel = _h2("At the hotel") + _p(
        "Three phrases cover most of a check-in: that you have a booking, that you want a room, and what it costs. "
        "Everything else is numbers.",
        "Say the price aloud back to them. It is polite, it confirms your listening, and it is the single most "
        "useful habit in a place where you are still counting slowly.")
    fares = _h2("Fares, money and bargaining") + _p(
        "Numbers are the vocabulary of travel, and markets are where you will use them most. "
        + E(d.get("bargaining_script", ""))) + _num_table(d["numbers"][:12], n)
    food = _h2("Food on the road") + _p(
        "Ordering is a script you can rehearse at home. Read the phrases below out loud, then order an imaginary "
        "meal three times.") + tri_table(d["food_phrases"], col3=n)
    culture = _h2("Cultural context, briefly") + _ul(
        ["<b>" + E(c["t"]) + "</b> (" + E(c["r"]) + ") — " + E(c["en"]) for c in d["culture"]])
    warn = _callout("The one thing to remember when you travel.",
                    "Speak less and listen more in the first two days. Your pronunciation improves faster from "
                    "hearing real speech than from any table on this site — and people will correct you kindly if "
                    "you give them the chance.")
    stuck = _h2("When you get stuck mid-sentence") + _p(
        "You will get stuck, and that is not a failure — it happens to everyone in the first week of using a "
        "language for real. What matters is having a way out that does not involve switching to English immediately.",
        "Three moves cover almost every situation: repeat the last word you understood as a question, ask the "
        "person to say it again more slowly, and fall back on the survival trio you already know. If none of that "
        "works, point at the phrase on your screen — nobody minds, and you will have used the language anyway.",
        "Then, afterwards, write down the sentence you could not finish. That one sentence is the most efficient "
        "vocabulary lesson you will get all week, because you will never forget the moment it failed you.")
    rehearse = _h2("Rehearse these three scenes before you go") + _ol([
        "Buying a ticket, including saying the destination and asking the price.",
        "Checking into a room, including saying how many nights and asking what time breakfast is.",
        "Ordering food, including saying what you do not eat and asking for the bill."])
    return station + hotel + fares + food + culture + rehearse + stuck + warn


def deep_number(d):
    n = d["name"]
    how = _h2("How the counting system actually works") + _p(
        "Beyond twenty, most numbers in " + E(n) + " are built from parts you already know: tens plus units. The "
        "table above gives you the building blocks; the pattern gives you the rest.",
        E(d["counting_note"]))
    used = _h2("Numbers you will use more than you think") + _ul([
        "<b>Prices.</b> Read the price aloud back to the seller — it confirms the number and practises it.",
        "<b>Time.</b> Hours first, then minutes. Learn \"half past\" as one phrase rather than assembling it.",
        "<b>Quantities.</b> Two of something, three of something — this is where the counting words appear.",
        "<b>Phone numbers.</b> The fastest way to make digits automatic: read your own number aloud every day."])
    trap = _h2("The counting trap") + _p(
        "Numbers feel easy early, which is why the exception around counting things catches learners late. Count "
        "real objects at home — two chairs, three books, five people — and say each one in " + E(n) + ". Ten "
        "minutes of real counting beats an hour of reciting the list.")
    drill = _callout("A five-minute drill.",
                     "Count to twenty out loud. Then count backwards from twenty. Then count a real object in front "
                     "of you. Then read the numbers table above without the Hindi column. Repeat tomorrow — this is "
                     "one of the few parts of a language that improves measurably in a week.")
    why = _h2("Why numbers are worth a whole week") + _p(
        "Numbers are the cheapest fluency in any language. They are finite, they repeat constantly, and they appear "
        "in the situations where you most need to be understood quickly: paying, asking how far, agreeing on a time.",
        "Most learners learn to count and then stop, which is a mistake. Counting is reciting; using numbers is a "
        "different skill. In a shop you do not need to count from one — you need to hear a price and understand it "
        "the first time, and you need to say a number someone else will understand on the first try.",
        "That is why every drill below is about real use rather than recitation.")
    plan = _h2("A week with the numbers") + _ol([
        "<b>Day 1.</b> Read 1–10 aloud ten times, then type them in the training lab.",
        "<b>Day 2.</b> Read 11–20 aloud, then cover the roman column and read them again.",
        "<b>Day 3.</b> The tens only — they are the skeleton of every number up to 100.",
        "<b>Day 4.</b> Read the whole table top to bottom without the Hindi column.",
        "<b>Day 5.</b> Count real objects at home, out loud, including two of something and five of something.",
        "<b>Day 6.</b> Say your age, your house number and your phone number in the language.",
        "<b>Day 7.</b> Take the topic quiz without looking at this page, then re-read the rows you missed."])
    clock = (_h2("Telling the time") + _p(
        "Once you can count, the clock is mostly a matter of two numbers and one pattern. Say the hour first, then "
        "the minutes — the same order you already learned for any quantity.",
        "Learn the time words below as whole phrases rather than assembling them from parts. They are short, they "
        "repeat every day, and being able to say when something happens is what turns a vocabulary list into a "
        "conversation about your actual life.") + tri_table(d["time_words"], col3=n) + _p(
        "A practical exercise: for one week, say the time out loud every time you check your phone. It takes two "
        "seconds and it makes the words automatic within days — far faster than revisiting the table.",
        "The same trick works for dates. Say today's date aloud in the morning and tomorrow's at night, and you "
        "will have the vocabulary you need for appointments, buses and bookings without ever sitting down to "
        "memorise a calendar."))
    test = _h2("The test that actually matters") + _p(
        "Ask someone to say ten numbers between one and a hundred and write down what you hear. If you get eight "
        "right, your numbers are genuinely working — the two you missed are the ones to drill tomorrow. Reciting "
        "1–100 in order proves much less than that single exercise.")
    return how + used + trap + why + plan + clock + test + drill


DEEPEN = {
    "beginner/": deep_beginner,
    "pronunciation/": deep_pronunciation,
    "grammar/": deep_grammar,
    "travel/": deep_travel,
    "numbers/": deep_number,
}


# The reading order the prev/next chain walks. The five PHASE 3 posts slot in at
# the point in the sequence where a learner would want them, rather than being
# appended at the end: words before numbers, mistakes once there is vocabulary
# to get wrong, reading once there is grammar to read with, the comparison and
# the speaking routine last before the intermediate sequence.
READ_ORDER = [
    ("basics/", "Basics"), ("beginner/", "Beginner"),
    ("pronunciation/", "Pronunciation"), ("common-words/", "Most common words"),
    ("numbers/", "Numbers"),
    ("time-dates/", "Time & dates"), ("conversation/", "Conversation"),
    ("vocabulary/", "Vocabulary"), ("mistakes/", "Common mistakes"),
    ("grammar/", "Grammar"),
    ("elementary/", "Elementary"), ("food/", "Food"),
    ("shopping/", "Shopping"), ("travel/", "Travel"),
    ("reading/", "Reading practice"),
    ("daily-life/", "Daily life"), ("vs-hindi/", "Compared with Hindi"),
    ("speaking-alone/", "Practising alone"),
    ("intermediate/", "Intermediate"),
]


def prevnext_nav(prev_pair, next_pair):
    """prev_pair/next_pair: (href, label) or None. Returns '' if neither."""
    if not prev_pair and not next_pair:
        return ""
    cells = []
    if prev_pair:
        cells.append('<a href="%s"><span class="k">← Previous</span>'
                     '<span class="t">%s</span></a>'
                     % (prev_pair[0], E(prev_pair[1])))
    else:
        cells.append("<span></span>")
    if next_pair:
        cells.append('<a href="%s" style="text-align:right"><span class="k">Next →</span>'
                     '<span class="t">%s</span></a>'
                     % (next_pair[0], E(next_pair[1])))
    return ('<nav class="prevnext" aria-label="More lessons">'
            + "".join(cells) + "</nav>")


def build(slug):
    with open(os.path.join(ROOT, "tools", "lang-data", slug + ".json"), encoding="utf-8") as f:
        d = json.load(f)
    out = os.path.join(ROOT, "learn", slug)
    wrote = []

    # review/ and my-progress/ are private local state (mirrors Hindi).
    # The five PHASE 3 posts are NEW FILES: the owner's immutable indexing
    # contract (tools/ultra/contract.py, data/quality/indexing-baseline.json)
    # requires every page that is not in the 2026-10-01 baseline to be noindex.
    # They stay reachable and linked; promoting them to index is an owner
    # decision, not a generator's.
    NOINDEX = {"review/", "my-progress/", "common-words/", "mistakes/",
               "reading/", "vs-hindi/", "speaking-alone/"}

    # full prev/next chain: topics + advanced hub + advanced modules
    _mods = d.get("advanced_modules", [])
    CHAIN = list(READ_ORDER)
    if _mods:
        CHAIN.append(("advanced/", "Advanced"))
        for m in _mods:
            CHAIN.append((f"advanced/{m['slug']}/", m["title"]))
    CHAIN_POS = {p: i for i, (p, _l) in enumerate(CHAIN)}

    def emit(relpath, title, desc, body, depth, extra=""):
        # fix crumb root-relative placeholders produced with {{r}}
        body = body.replace("{r}", "../" * depth)
        # prev/next navigation (post-process: p_* emitters untouched)
        if relpath in CHAIN_POS:
            i = CHAIN_POS[relpath]
            here = os.path.join(out, relpath)

            def href(target):
                h = os.path.relpath(os.path.join(out, target), here)
                return h.replace(os.sep, "/") + "/"

            prev_pair = None
            next_pair = None
            if i > 0:
                prev_pair = (href(CHAIN[i - 1][0]), CHAIN[i - 1][1])
            if i < len(CHAIN) - 1:
                next_pair = (href(CHAIN[i + 1][0]), CHAIN[i + 1][1])
            body += "\n  " + prevnext_nav(prev_pair, next_pair)
        # PHASE 3 depth: the five guides that already had a page get their long-form
        # section, and all ten link to one another (internal linking).
        if relpath in DEEPEN:
            body += "\n" + DEEPEN[relpath](d) + "\n" + _guide_links(d, relpath[:-1])
        body = language_markup(body, d["name"])
        robots = "noindex, follow" if relpath in NOINDEX else "index, follow, max-snippet:-1, max-image-preview:large"
        page = shell(d, relpath, title, desc, body, depth, extra, robots)
        fp = os.path.join(out, relpath, "index.html")
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(page)
        wrote.append(relpath or "/")

    # -- course home + levels + topics (depths: home=2, topics=3)
    t, ds, b = p_index(d)
    emit("", t, ds, b, 2)
    for fn in [p_basics, p_beginner, p_elementary, p_intermediate, p_conversation,
               p_pronunciation, p_grammar, p_vocabulary, p_travel, p_daily,
               p_numbers, p_time, p_food, p_shopping]:
        t, ds, b = fn(d)
        slugmap = {"basics": "basics", "beginner": "beginner", "elementary": "elementary",
                   "intermediate": "intermediate", "conversation": "conversation",
                   "pronunciation": "pronunciation", "grammar": "grammar", "vocabulary": "vocabulary",
                   "travel": "travel", "daily": "daily-life", "numbers": "numbers",
                   "time": "time-dates", "food": "food", "shopping": "shopping"}
        key = fn.__name__.split("_", 1)[1]
        emit(slugmap[key] + "/", t, ds, b, 3)
    # -- PHASE 3 blog posts (five new pages; the other five post types are the
    #    deepened guides emitted above)
    for post_slug, post_fn in zip(["common-words", "mistakes", "reading", "vs-hindi", "speaking-alone"],
                                  [p_common_words, p_mistakes, p_reading, p_vs_hindi, p_speaking_alone]):
        t, ds, b = post_fn(d)
        emit(post_slug + "/", t, ds, b, 3)
    # -- practice hub + labs
    t, ds, b = p_practice(d)
    emit("practice/", t, ds, b, 3)
    for kind in ["quiz", "typing", "worksheets"]:
        t, ds, b, scripts = lab_page(d, kind)
        emit(f"practice/{kind}/", t, ds, b, 4, scripts)
    t, ds, b = p_conversation_lab(d)
    emit("practice/conversation/", t, ds, b, 4)
    # -- advanced modules (optional; absent for most languages)
    mods = d.get("advanced_modules", [])
    if mods:
        t, ds, b = p_advanced_hub(d)
        emit("advanced/", t, ds, b, 3)
        for m in mods:
            t, ds, b = p_advanced_module(d, m)
            emit(f"advanced/{m['slug']}/", t, ds, b, 4)
    # -- review + progress
    t, ds, b = p_review(d)
    emit("review/", t, ds, b, 3)
    t, ds, b = p_progress(d)
    emit("my-progress/", t, ds, b, 3)

    # -- quiz bank JS (base bank + advanced-module questions, IDs must stay unique)
    questions = list(d["quiz"]) + [q for m in mods for q in m.get("quiz", [])]
    ids = [q["id"] for q in questions]
    assert len(ids) == len(set(ids)), f"duplicate quiz ids in {slug}"
    bank = {"version": 1, "questions": questions}
    data = json.dumps(bank, ensure_ascii=False, indent=1)
    typing = json.dumps(d["typing"], ensure_ascii=False, indent=1)
    js = QUIZ_BANK_TMPL.format(NAME=d["name"].upper(), GLOBAL=d["name"].upper(),
                               data=data, slug=slug, Name=d["name"],
                               script=d["script_name"], name=d["name"].lower(),
                               typing=typing)
    # validate the data object parses as JSON (same contract as Hindi bank)
    json.loads(data)
    jpath = os.path.join(ROOT, "js", slug + "-quiz-bank.js")
    with open(jpath, "w", encoding="utf-8") as f:
        f.write(js)
    wrote.append("js/" + slug + "-quiz-bank.js")
    print(f"{slug}: wrote {len(wrote)} files")
    return wrote


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[2] == "--refresh-beginner-content":
        refresh_beginner_content(sys.argv[1])
    elif len(sys.argv) == 2:
        build(sys.argv[1])
    else:
        raise SystemExit(
            "Usage: python3 tools/build-language-course.py <slug> "
            "[--refresh-beginner-content]"
        )

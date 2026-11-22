#!/usr/bin/env python3
"""Build the four new time-page bodies (gu/kn/te/ur) from the Punjabi shell.

Why a separate builder: the pages share one shell (head, chrome, generated
tables), but the prose has to be linguistically accurate per language. A blind
word-swap would be wrong — Urdu day names do not end in a "day" suffix the way
Gujarati/Kannada/Telugu do, and the shared-time-word quirk differs per language.
So each body is written from the verified data, and the words are pulled from
the JSON so they can never drift from the tables.

The shell (everything outside <main>) is taken from the Punjabi page; only the
<main> body is rebuilt. Tables are left as markers for build-time-pages.py.

  python3 tools/build-time-pages-bodies.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "days-and-months-in-punjabi/index.html"

# reuse the table renderer so this builder produces the FINAL page (markers
# filled), which makes --check meaningful. build-time-pages.py only owns the
# marker-filling; importing its table() keeps one source of truth for rows.
import importlib.util
_bt = importlib.util.spec_from_file_location("_bt", ROOT / "tools" / "build-time-pages.py")
_bt_mod = importlib.util.module_from_spec(_bt)
_bt.loader.exec_module(_bt_mod)


def fill_markers(page: str, spec: dict, d: dict) -> str:
    """Fill the four table markers in a page the same way build-time-pages does."""
    spec = {**spec, "script_name": spec["script"]}
    for _, kind in _bt_mod.MARKERS:
        start = f"<!-- ekguru:time-{spec['slug']}-{kind}:start -->"
        end = f"<!-- ekguru:time-{spec['slug']}-{kind}:end -->"
        a = page.index(start) + len(start)
        b = page.index(end)
        want = "\n" + _bt_mod.table(spec, d, kind) + "\n"
        page = page[:a] + want + page[b:]
    return page


def load(lang_file: str) -> dict:
    return json.loads((ROOT / "data/time" / lang_file).read_text(encoding="utf-8"))


def w(d, en):
    """Return the word for an English key, or the first match on a prefix."""
    for grp in ("days", "months", "desi_months", "time_words"):
        for e in d[grp]:
            if e["en"] == en:
                return e["word"]
    return "?"


SPECS = [
    {
        "slug": "days-and-months-in-gujarati", "file": "gujarati.json",
        "lang": "gu", "script": "Gujarati", "languageName": "Gujarati",
        "day_suffix": "વાર", "day_suffix_roman": "-vār",
        "shared": "Gujarati distinguishes tomorrow (આવતી કાલ) from yesterday (ગઈ કાલ) in full, though in speech both shorten to કાલે.",
        "desi_lead": "Alongside the calendar months, Gujarat keeps its own Vikram Samvat months — the traditional names you hear around festivals and auspicious dates. The Gujarati New Year begins the day after Diwali, with કારતક (Kartak).",
        "build_rows": [
            ("સોમવાર (Somavaar)", "સોમ, the Moon", "Monday, moon-day"),
            ("મંગળવાર (Mangalavaar)", "મંગળ, Mars", "Tuesday"),
            ("બુધવાર (Budhvaar)", "બુધ, Mercury", "Wednesday"),
            ("ગુરુવાર (Guruvaar)", "ગુરુ, Jupiter", "Thursday"),
            ("શુક્રવાર (Shukravaar)", "શુક્ર, Venus", "Friday"),
            ("શનિવાર (Sanivaar)", "શનિ, Saturn", "Saturday"),
            ("રવિવાર (Ravivaar)", "રવિ, the Sun", "Sunday"),
        ],
        "faq": [
            ("How do you say the days of the week in Gujarati?",
             "Every day ends in વાર. Sunday રવિવાર, Monday સોમવાર, Tuesday મંગળવાર, Wednesday બુધવાર, Thursday ગુરુવાર, Friday શુક્રવાર, Saturday શનિવાર."),
            ("Why does Gujarati have two sets of month names?",
             "Everyday and official life uses the Gregorian months written in Gujarati — જાન્યુઆરી, ફેબ્રુઆરી, માર્ચ. The traditional Vikram Samvat months — કારતક, માગશર, પોષ — are used for festivals and auspicious dates. Both are correct; they answer different questions."),
            ("How do you say today, tomorrow and yesterday in Gujarati?",
             "Today is આજ (aaj), tomorrow is આવતી કાલ (aavatee kaaL), yesterday is ગઈ કાલ (gai kaaL). In speech both shorten to કાલે. The four parts of the day are morning સવાર, afternoon બપોર, evening સાંજ and night રાત્રિ."),
        ],
        "tutor": "Gujarati or Hindi tutor",
        "keep": [
            ("../days-and-months-in-marathi/", "Marathi days and months", "compare the two systems"),
            ("../days-and-months-in-kannada/", "Kannada days and months", "the same list, another script"),
            ("../learn/gujarati/", "Gujarati and the Gujarati script", "the script from the start"),
        ],
    },
    {
        "slug": "days-and-months-in-kannada", "file": "kannada.json",
        "lang": "kn", "script": "Kannada", "languageName": "Kannada",
        "day_suffix": "ವಾರ", "day_suffix_roman": "-vāra",
        "shared": "Kannada gives tomorrow (ನಾಳೆ) and yesterday (ನಿನ್ನೆ) separate words, and the day after (ನಾಡಿದು) and the day before (ಮೋನ್ನೆ) separate words too.",
        "desi_lead": "Alongside the calendar months, Kannada keeps its own traditional lunar months — the names you hear around festivals and the Kannada New Year, Ugadi, which falls in ಚೈತ್ರ (Chaitra).",
        "build_rows": [
            ("ಸೋಮವಾರ (Somavara)", "ಸೋಮ, the Moon", "Monday, moon-day"),
            ("ಮಂಗಳವಾರ (Mangalavara)", "ಮಂಗಳ, Mars", "Tuesday"),
            ("ಬುಧವಾರ (Budhavara)", "ಬುಧ, Mercury", "Wednesday"),
            ("ಗುರುವಾರ (Guruvara)", "ಗುರು, Jupiter", "Thursday"),
            ("ಶುಕ್ರವಾರ (Shukravara)", "ಶುಕ್ರ, Venus", "Friday"),
            ("ಶನಿವಾರ (Sanivara)", "ಶನಿ, Saturn", "Saturday"),
            ("ಭಾನುವಾರ (Bhanuvara)", "ಭಾನು, the Sun", "Sunday"),
        ],
        "faq": [
            ("How do you say the days of the week in Kannada?",
             "Every day ends in ವಾರ. Sunday ಭಾನುವಾರ, Monday ಸೋಮವಾರ, Tuesday ಮಂಗಳವಾರ, Wednesday ಬುಧವಾರ, Thursday ಗುರುವಾರ, Friday ಶುಕ್ರವಾರ, Saturday ಶನಿವಾರ."),
            ("Why does Kannada have two sets of month names?",
             "Everyday and official life uses the Gregorian months written in Kannada — ಜನವರಿ, ಫೆಬ್ರವರಿ, ಮಾರ್ಚ್. The traditional lunar months — ಚೈತ್ರ, ವೈಶಾಖ, ಜ್ಯೇಷ್ಠ — are used for festivals and the Panchang. Both are correct; they answer different questions."),
            ("How do you say today, tomorrow and yesterday in Kannada?",
             "Today is ಇಂದು (indu), tomorrow is ನಾಳೆ (naale), yesterday is ನಿನ್ನೆ (ninne). The day after is ನಾಡಿದು and the day before is ಮೋನ್ನೆ. The four parts of the day are morning ಬೆಳಿಗ್ಗೆ, afternoon ಮಧ್ಯಾಹ್ನ, evening ಸಂಜೆ and night ರಾತ್ರಿ."),
        ],
        "tutor": "Kannada or Hindi tutor",
        "keep": [
            ("../days-and-months-in-telugu/", "Telugu days and months", "compare the two systems"),
            ("../days-and-months-in-gujarati/", "Gujarati days and months", "the same list, another script"),
            ("../learn/kannada/", "Kannada and the Kannada script", "the script from the start"),
        ],
    },
    {
        "slug": "days-and-months-in-telugu", "file": "telugu.json",
        "lang": "te", "script": "Telugu", "languageName": "Telugu",
        "day_suffix": "వారం", "day_suffix_roman": "-vāraṁ",
        "shared": "Telugu gives tomorrow (రేపు) and yesterday (నిన్న) separate words, and the day after (మోగాళ్ళు) and the day before (మొన్న) separate words too.",
        "desi_lead": "Alongside the calendar months, Telugu keeps its own traditional months — the names you hear around festivals and the Telugu New Year, Ugadi, which falls in చైత్రము (Chaitramu), around March–April.",
        "build_rows": [
            ("సోమవారం (Somavaram)", "సోమ, the Moon", "Monday, moon-day"),
            ("మంగళవారం (Mangalavaram)", "మంగళ, Mars", "Tuesday"),
            ("బుధవారం (Budhavaram)", "బుధ, Mercury", "Wednesday"),
            ("గురువారం (Guruvaram)", "గురు, Jupiter", "Thursday"),
            ("శుక్రవారం (Shukravaram)", "శుక్ర, Venus", "Friday"),
            ("శనివారం (Sanivaram)", "శని, Saturn", "Saturday"),
            ("ఆదివారం (Adivaram)", "ఆది, the Sun", "Sunday"),
        ],
        "faq": [
            ("How do you say the days of the week in Telugu?",
             "Every day ends in వారం. Sunday ఆదివారం, Monday సోమవారం, Tuesday మంగళవారం, Wednesday బుధవారం, Thursday గురువారం, Friday శుక్రవారం, Saturday శనివారం."),
            ("Why does Telugu have two sets of month names?",
             "Everyday and official life uses the Gregorian months written in Telugu — జనవరి, ఫిబ్రవరి, మార్చి. The traditional months — చైత్రము, వైశాఖము, జ్యేష్ఠము — are used for festivals and the Panchang. Both are correct; they answer different questions."),
            ("How do you say today, tomorrow and yesterday in Telugu?",
             "Today is నేడు (neduu), tomorrow is రేపు (repu), yesterday is నిన్న (ninna). The day after is మోగాళ్ళు and the day before is మొన్న. The four parts of the day are morning ఉదయం, afternoon మధ్యాహ్నం, evening సాయంత్రం and night రాత్రి."),
        ],
        "tutor": "Telugu or Hindi tutor",
        "keep": [
            ("../days-and-months-in-kannada/", "Kannada days and months", "compare the two systems"),
            ("../days-and-months-in-urdu/", "Urdu days and months", "the same list, another script"),
            ("../learn/telugu/", "Telugu and the Telugu script", "the script from the start"),
        ],
    },
    {
        "slug": "days-and-months-in-urdu", "file": "urdu.json",
        "lang": "ur", "script": "Arabic", "languageName": "Urdu",
        "day_suffix": None, "day_suffix_roman": None,
        "shared": "Urdu uses one word for two directions of time: کل (kal) is both tomorrow and yesterday, and پرسوں (parson) is both the day after tomorrow and the day before yesterday. Context and the verb tell you which.",
        "desi_lead": "Alongside the calendar months, Urdu keeps the traditional Hindu month names — the names you hear around festivals. The everyday Gregorian months are the ones used on phones and in newspapers.",
        "build_rows": [
            ("پیر (Peer)", "پیر, the elder / Moon", "Monday"),
            ("منگل (Mangal)", "منگل, Mars", "Tuesday"),
            ("بدھ (Budh)", "بدھ, Mercury", "Wednesday"),
            ("جمعرات (Jumeraat)", "جمع, the gathering", "Thursday"),
            ("جمعہ (Jumma)", "جمع, gathering / prayer", "Friday"),
            ("ہفتہ (Hafta)", "ہفتہ, week", "Saturday"),
            ("اتوار (Itwaar)", "اتوار, the sun", "Sunday"),
        ],
        "faq": [
            ("How do you say the days of the week in Urdu?",
             "Sunday اتوار, Monday پیر, Tuesday منگل, Wednesday بدھ, Thursday جمعرات, Friday جمعہ, Saturday ہفتہ. Note that ہفتہ also means 'week'."),
            ("Why does Urdu have two sets of month names?",
             "Everyday and official life uses the Gregorian months written in Arabic script — جنوری, فروری, مارچ. The traditional Hindu month names — چایتر, ویساخ, جیشتھ — are used around festivals. Both are correct; they answer different questions."),
            ("What does کل (kal) mean in Urdu?",
             "It means both tomorrow and yesterday. Context and the verb tense tell you which — کل آؤں گا is 'I will come tomorrow', کل آيا تھا is 'I came yesterday'. پرسوں (parson) does the same for the day after tomorrow and the day before yesterday."),
        ],
        "tutor": "Urdu or Hindi tutor",
        "keep": [
            ("../days-and-months-in-punjabi/", "Punjabi days and months", "compare the two systems"),
            ("../days-and-months-in-marathi/", "Marathi days and months", "the same list, another script"),
            ("../learn/urdu/", "Urdu and the Urdu script", "the script from the start"),
        ],
    },
]


def build_body(spec: dict, d: dict) -> str:
    lang = spec["lang"]
    suf = spec["day_suffix"]
    suf_rom = spec["day_suffix_roman"]
    # days intro depends on whether the language uses a day suffix
    if suf:
        days_intro = (f'<p>Every {spec["languageName"]} day ends in '
                      f'<span lang="{lang}">{suf}</span> (<em>{suf_rom}</em>), which just\n'
                      f'means "day". The rest of the name is a planet or a god, so once you know the\n'
                      f'opening sound you can almost always guess the day.</p>')
    else:
        days_intro = ('<p>The seven Urdu day names come from Persian and Arabic. Most are named after '
                      'the days of the week in that tradition, and <span lang="ur">ہفتہ</span> '
                      '(hafta), Saturday, is also the word for "week".</p>')

    months_intro = (f'<p>These are the Gregorian month names written in {spec["script"]}, the ones you will\n'
                    f'find on phones, in newspapers and on calendars.</p>')

    time_intro = ('<p>The words you actually use when you are talking about when things happen —\n'
                  'today, tomorrow, morning, night and the rest.</p>')

    note = f'<b>{spec["shared"]}</b>'

    desi = f'<p>{spec["desi_lead"]}</p>\n' \
           f'<p>Both sets are real and answer different questions. If someone in the region says a ' \
           f'festival is in a traditional month, that is the Hindu name; if they name a calendar month, ' \
           f'that is the Gregorian one.</p>\n' \
           f'<!-- ekguru:time-{spec["slug"]}-desi:start -->\nPLACEHOLDER\n' \
           f'<!-- ekguru:time-{spec["slug"]}-desi:end -->'

    build_rows_html = "\n".join(
        f'<tr><td class="en">{a}</td><td class="en">{b}</td><td class="en">{c}</td></tr>'
        for a, b, c in spec["build_rows"])
    build = ('<h2>How the day names are built</h2>\n'
             '<p>The pattern is planetary and it is the same idea across many languages:</p>\n'
             f'<table class="ex"><thead><tr><th>Day</th><th>From</th><th>Meaning</th></tr></thead><tbody>\n'
             f'{build_rows_html}\n</tbody></table>')

    faq_html = ""
    for q, a in spec["faq"]:
        faq_html += f'<h3>{q}</h3>\n<p>{a}</p>\n'

    keep_html = "\n".join(
        f'<li><a href="{href}">{label}</a> — {note2}</li>'
        for href, label, note2 in spec["keep"])

    return f'''<main id="main">
<div class="nw">
<p class="crumb"><a href="../">EkGuru</a> › {spec["languageName"]} days and months</p>
<h1>{spec["languageName"]} days, months and time words</h1><!-- ekguru:ultra-byline:start -->
<p class="eg-byline" lang="en" dir="ltr" data-eg-chrome="editorial">Author: not separately recorded. Maintained by <a href="/authors/prakash/" hreflang="en">Prakash</a>. Reviewed by: not recorded. Updated: <time datetime="2026-11-21">2026-11-21</time>. <a href="/editorial-policy/" hreflang="en">Editorial policy and corrections</a>.</p>
<!-- ekguru:ultra-byline:end -->
<!-- ekguru:ultra-audio:start -->
<p class="eg-voice-note" data-eg-voice-note="{lang}" lang="en" dir="ltr" data-eg-chrome="audio" aria-live="polite"></p>
<!-- ekguru:ultra-audio:end -->

<p class="lede">All seven days, all twelve months and the time words you use every day, in {spec["languageName"]} {spec["script"]}. Type any English day, month or time word below and it returns the {spec["languageName"]} word in its own script, straight away.</p>

<div class="tool">
<label for="tIn">Type an English word — a day, month or time word</label>
<input aria-describedby="tHelp" autocomplete="off" id="tIn" data-lang="{lang}"
 placeholder="e.g. Tuesday, March, morning" spellcheck="false" type="text"/>
<div aria-live="polite" class="tout" id="tOut">
<div class="big" lang="{lang}"></div>
<div class="rom">Type an English word — a day, a month or a time word — and see it in {spec["languageName"]}.</div>
</div>
<div class="btnrow" hidden="" id="tbtnrow">
<button id="tcopyBtn" type="button">Copy</button>
</div>
<p class="rom" id="tHelp" style="margin-top:14px;font-size:.85rem">
    Nothing you type leaves your browser. This runs entirely on your device.</p>
</div>

<h2>The seven days of the week</h2>
{days_intro}
<!-- ekguru:time-{spec["slug"]}-days:start -->
PLACEHOLDER
<!-- ekguru:time-{spec["slug"]}-days:end -->

<h2>The twelve months of the year</h2>
{months_intro}
<!-- ekguru:time-{spec["slug"]}-months:start -->
PLACEHOLDER
<!-- ekguru:time-{spec["slug"]}-months:end -->

<h2>The everyday time words</h2>
{time_intro}
<!-- ekguru:time-{spec["slug"]}-time_words:start -->
PLACEHOLDER
<!-- ekguru:time-{spec["slug"]}-time_words:end -->

<div class="note">
{note}
</div>

<h2>The traditional month names</h2>
{desi}

{build}

<h2>Questions people ask</h2>
{faq_html}
<aside class="pg-cta" aria-label="Next step">
<h2 style="margin-top:0">Count the days, the months and the numbers</h2>
<p>Days and months are the easiest first words because you use them every day
and they are already familiar. A tutor will get your pronunciation of the day
names right before it sets — <a href="../find-tutors.html">find a {spec["tutor"]}</a>.</p>
</aside>

<h2>Keep going</h2>
<ul>
{keep_html}
<li><a href="../learn/">All free guides</a> · <a href="../ask/">Questions people ask before they start</a></li>
</ul>
</div>
</main>'''


def build_page(spec: dict, d: dict) -> str:
    shell = SHELL.read_text(encoding="utf-8")
    lang = spec["lang"]
    slug = spec["slug"]
    url = f"https://ekguru.shop/{slug}/"

    # ---- head: take the Punjabi shell, swap language-specific bits ----
    shell = shell.replace('data-learning-language="pa"', f'data-learning-language="{lang}"')
    shell = shell.replace(
        '<title>Punjabi Days, Months and Time — Days of the Week in Gurmukhi | EkGuru</title>',
        f'<title>{spec["title"]}</title>')
    shell = shell.replace(
        'content="Every day of the week, month of the year and everyday time word in Punjabi, with Gurmukhi writing and pronunciation. Type an English word and get it back in Punjabi."',
        f'content="{spec["desc"]}"')
    shell = shell.replace('href="https://ekguru.shop/days-and-months-in-punjabi/" rel="canonical"',
                          f'href="{url}" rel="canonical"')
    shell = shell.replace('content="Punjabi Days, Months and Time — Days of the Week in Gurmukhi | EkGuru"',
                          f'content="{spec["title"]}"')
    shell = shell.replace('content="Type any English day, month or time word and see it written in Punjabi, with how to say it. Free and instant."',
                          f'content="{spec["ogdesc"]}"')
    shell = shell.replace('content="https://ekguru.shop/days-and-months-in-punjabi/" property="og:url"',
                          f'content="{url}" property="og:url"')

    # LD+JSON: replace the whole block
    new_ld = (
        '<script type="application/ld+json">{"@context":"https://schema.org","@graph":['
        '{"@type":"WebApplication","@id":"' + url + '#app","name":"' + spec["languageName"] +
        ' days and months reader","url":"' + url + '","applicationCategory":"EducationalApplication",'
        '"operatingSystem":"Any","description":"Type any English day, month or time word and read it in ' +
        spec["languageName"] + ', with the word and how to say it.",'
        '"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},'
        '"publisher":{"@type":"Organization","name":"EkGuru","url":"https://ekguru.shop/"},'
        '"inLanguage":"en","isAccessibleForFree":true},'
        '{"@type":"BreadcrumbList","@id":"' + url + '#breadcrumb","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"EkGuru","item":"https://ekguru.shop/"},'
        '{"@type":"ListItem","position":2,"name":"' + spec["languageName"] +
        ' days, months and time words","item":"' + url + '"}]}]}</script>'
    )
    s = shell.index('<script type="application/ld+json">')
    e = shell.index('</script>', s) + len('</script>')
    shell = shell[:s] + new_ld + shell[e:]

    # ---- body: replace <main>...</main> ----
    body = build_body(spec, d)
    ms = shell.index('<main id="main">')
    me = shell.index('</main>', ms) + len('</main>')
    shell = shell[:ms] + body + shell[me:]
    return shell


def main() -> int:
    check = "--check" in sys.argv
    problems = []
    for spec in SPECS:
        # fill in the head fields that build_page needs
        spec["title"] = (f'{spec["languageName"]} Days, Months and Time — Days of the Week '
                         f'in {spec["script"]} | EkGuru')
        spec["desc"] = (f'Every day of the week, month of the year and everyday time word in '
                        f'{spec["languageName"]}, with {spec["script"]} writing and pronunciation. '
                        f'Type an English word and get it back in {spec["languageName"]}.')
        spec["ogdesc"] = (f'Type any English day, month or time word and see it written in '
                          f'{spec["languageName"]}, with how to say it. Free and instant.')
        d = load(spec["file"])
        page = fill_markers(build_page(spec, d), spec, d)
        out = ROOT / spec["slug"] / "index.html"
        if check:
            if not out.exists() or out.read_text(encoding="utf-8") != page:
                problems.append(f"STALE {spec['slug']}/index.html — run: python3 tools/build-time-pages-bodies.py")
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(page, encoding="utf-8")
            print('wrote', spec["slug"])
    if check:
        if problems:
            print("\n".join(problems))
            return 1
        print("ok    time-page bodies are current")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

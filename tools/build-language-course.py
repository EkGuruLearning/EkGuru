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
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://ekguru.shop"
TODAY = "2026-09-13"

ART_CSS = """.art{max-width:760px;margin:0 auto;padding:0 20px 60px}
.art h1{font-size:2rem;line-height:1.25;margin:26px 0 10px}
.art .meta{color:var(--muted);font-size:.86rem;margin:0 0 26px}
.art h2{font-size:1.28rem;margin:34px 0 12px;padding-top:6px}
.art p,.art li{line-height:1.75}
.art ul,.art ol{padding-left:22px}
.art li{margin:7px 0}
.crumb{font-size:.84rem;color:var(--muted);padding:18px 0 0}
.crumb a{color:var(--muted)}
.lede{color:var(--ink-2);font-size:1.05rem;line-height:1.7;margin:0 0 22px}
.hs-grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));margin:16px 0}
.hs-card{border:1px solid var(--line);border-radius:12px;padding:14px 16px;text-decoration:none;background:var(--card,#fff)}
.hs-card:hover{border-color:var(--brand-2)}
.hs-card b{display:block;color:var(--brand);font-size:.98rem;margin-bottom:4px}
.hs-card span{display:block;color:var(--ink-2);font-size:.86rem;line-height:1.5}
.linklist{list-style:none;padding:0;margin:12px 0 0}
.linklist li{padding:10px 0;border-bottom:1px solid var(--line)}
.linklist li:last-child{border-bottom:0}
.linklist a{font-weight:600}
.linklist span{display:block;color:var(--muted);font-size:.87rem;margin-top:2px;line-height:1.5}
.note{background:var(--bg-soft);border:1px solid #ddd8ff;border-radius:12px;padding:14px 16px;margin:14px 0;font-size:.94rem;color:var(--ink-2)}
.tri td:nth-child(3){font-weight:600}
@media(pointer:coarse){.hs-card,.linklist a{min-height:44px;display:block}input,select,textarea,button{min-height:44px}}
.prevnext{display:flex;justify-content:space-between;gap:12px;margin:34px 0 8px}
.prevnext a{flex:1;border:1px solid var(--line);border-radius:12px;padding:12px 14px;text-decoration:none;color:var(--ink);background:var(--card,#fff)}
.prevnext a:hover{border-color:var(--brand-2)}
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
        cells = f"<td>{E(w['en'])}</td><td>{E(w['hi'])}</td><td>{E(w['t'])}</td><td>{E(w['r'])}</td>"
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
  <p>{len(d['vowels'])} vowels and {len(d['consonants'])} consonants. The full tables with sounds are on the <a href="../pronunciation/">pronunciation page</a> — learn to recognise them before you memorise any words.</p>
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
  <p class="lede">What to actually say to a person: greetings, introductions and the small talk that opens every door.</p>
  <h2>Greetings</h2>
  {tri_table(d['greetings'], col3=n)}
  <h2>Introducing yourself</h2>
  {tri_table(d['daily_phrases'][3:7], col3=n)}
  <h2>Full dialogues</h2>
  <p>Three everyday scenes with every line in three languages: on the <a href="../practice/conversation/">convers<p>Three everyday scenes with every line in three languages: on the <a href="../practice/conversation/">conversation scenarios</a> page.</p>""")


def p_pronunciation(d):
    n = d["name"]
    return (f"{n} pronunciation, reading & writing",
            f"The {d['script_name']} letter by letter, the sounds learners get wrong, and how to practise them.",
            f"""{crumb(d, [(None, "Pronunciation")])}
  <h1>{E(n)} pronunciation, reading &amp; writing</h1>
  <p class="lede">The sounds learners get wrong, and the path from your first letter to reading real words. {E(d['script_note'])}</p>
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
    clf = "".join(f"<tr><td><b>{E(c['en'])}</b> ({E(c['r'])})</td><td>{E(c['hi'])}</td><td>{E(c['note'])}</td></tr>" for c in d["classifiers"])
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
  <p class="lede">Word order, verbs, pronouns and the mistakes everyone makes — explained, not listed.</p>
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
  <p class="lede">High-frequency words grouped by meaning. Learn each group, then test it in the <a href="../practice/quiz/">quiz</a>.</p>
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
  <p class="lede">Stations, directions, fares and hotels — the phrases you will actually use.</p>
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
  <p class="lede">The phrases of everyday life, plus the culture that makes them make sense.</p>
  <h2>Daily phrases</h2>
  {tri_table(d['daily_phrases'], col3=n)}
  <h2>Culture in five words</h2>
  <ul>{cult}</ul>""")


def p_numbers(d):
    n = d["name"]
    rows = "".join(f"<tr><td><b>{w['n']}</b></td><td>{E(w['hi'])}</td><td><b>{E(w['t'])}</b></td><td>{E(w['r'])}</td></tr>" for w in d["numbers"])
    return (f"{n} numbers 1–100",
            f"{n} numbers 1–20, the tens and 100 — with pronunciation and the counting pattern.",
            f"""{crumb(d, [(None, "Numbers")])}
  <h1>{E(n)} numbers</h1>
  <p class="lede">1–20 by heart, then the tens — that covers every price, time and quantity you will meet.</p>
  <table class="tbl tri"><thead><tr><th>#</th><th>Hindi</th><th>{E(n)}</th><th>Say it</th></tr></thead><tbody>{rows}</tbody></table>
  <div class="note"><b>Pattern.</b> After 20, most numbers are regular compounds — learn the tens above and 21–99 assemble themselves. Test yourself in the <a href="../practice/quiz/">quiz</a>.</div>""")


def p_time(d):
    n = d["name"]
    return (f"{n} time & dates — days and the clock",
            f"Days of the week, today and tomorrow, and telling the time in {n}.",
            f"""{crumb(d, [(None, "Time")])}
  <h1>{E(n)} time &amp; dates</h1>
  <p class="lede">Days, today/tomorrow, and the clock.</p>
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
  <p class="lede">Prices, bargaining and the phrases for markets and shops.</p>
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
  <p class="lede">Free practice that works alone: quiz yourself, type the script, print worksheets, rehearse dialogues.</p>
  <ul class="linklist">
    <li><a href="quiz/">Topic quiz</a><span>Pick a topic and level — {len(d['quiz'])} questions with explanations.</span></li>
    <li><a href="typing/">{E(n)} typing trainer</a><span>Roman prompt → type it in {E(d['script_name'])}.</span></li>
    <li><a href="worksheets/">Worksheets</a><span>Printable prompts with writing space and answers.</span></li>
    <li><a href="conversation/">Conversation scenarios</a><span>Trilingual dialogues for real situations.</span></li>
  </ul>
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
    blurbs = {"quiz": f"Pick a topic and level, then answer 5, 10 or 15 questions. Every answer comes with an explanation and a link back to the source lesson.",
              "typing": f"Type the {n} word in {d['script_name']}. Small differences in spacing or punctuation count as “minor format”, not wrong.",
              "worksheets": "Pick a topic, print the prompts, write your answers, then check the answer section."}
    r = "../../../../"
    scripts = {"quiz": f'<script src="{r}js/toast.js" defer></script>\n<script src="{r}js/{slug}-quiz-bank.js" defer></script>\n<script src="{r}js/hindi-progress.js" defer></script>\n<script src="{r}js/hindi-tools.js" defer></script>\n',
               "typing": f'<script src="{r}js/toast.js" defer></script>\n<script src="{r}js/{slug}-quiz-bank.js" defer></script>\n<script src="{r}js/hindi-fuzzy.js" defer></script>\n<script src="{r}js/hindi-progress.js" defer></script>\n<script src="{r}js/hindi-tools.js" defer></script>\n',
               "worksheets": f'<script src="{r}js/toast.js" defer></script>\n<script src="{r}js/{slug}-quiz-bank.js" defer></script>\n<script src="{r}js/hindi-tools.js" defer></script>\n'}[kind]
    body = f"""{crumb(d, [("../", "Practice"), (None, title.split(" — ")[0].replace(n + " ", "").title())])}
  <h1>{E(title)}</h1>
  <p class="lede">{E(blurbs[kind])}</p>
  <div id="{appid}"></div>
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
  <p class="lede">The 20 words worth reviewing until they are automatic. Tick each one when you know it cold — progress saves on this device only.</p>
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
  <p class="lede">Your course checklist — this device only, no account, no sync. Honest rule: tick a lesson only after its quiz.</p>
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
READ_ORDER = [
    ("basics/", "Basics"), ("beginner/", "Beginner"),
    ("pronunciation/", "Pronunciation"), ("numbers/", "Numbers"),
    ("time-dates/", "Time & dates"), ("conversation/", "Conversation"),
    ("vocabulary/", "Vocabulary"), ("grammar/", "Grammar"),
    ("elementary/", "Elementary"), ("food/", "Food"),
    ("shopping/", "Shopping"), ("travel/", "Travel"),
    ("daily-life/", "Daily life"), ("intermediate/", "Intermediate"),
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

    NOINDEX = {"review/", "my-progress/"}  # private local state, mirrors Hindi

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
    build(sys.argv[1])

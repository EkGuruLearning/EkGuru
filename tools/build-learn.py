#!/usr/bin/env python3
"""EkGuru — regenerate Learn Paths + Practice lab pages (v100).

Single source of truth:
  · js/learning-paths.js  -> learn/paths/<slug>/index.html
  · PRACTICE_PAGES below  -> learn/practice/<slug>/index.html

Every generated page is self-contained article-style HTML (like the
existing learn guides): unique title/description/H1/intro prose +
JSON-LD, with the interactive parts rendered at runtime from the
shared js (learning-paths.js, practice-bank.js, practice-engine.js,
path-progress.js). Run after editing the data:  python3 tools/build-learn.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://ekguru.shop"

# ---------------------------------------------------------------- CSS
PATH_CSS = """
.pp-bar{background:var(--bg-soft);border-radius:999px;height:10px;overflow:hidden;margin:6px 0 4px}
.pp-bar span{display:block;height:100%;background:var(--grad);border-radius:999px;transition:width .3s var(--ease)}
.pp-count{color:var(--muted);font-size:.88rem;margin:0 0 22px}
.pp-mod h2{font-size:1.18rem;margin:30px 0 10px}
.pp-list{list-style:none;padding:0;margin:0}
.pp-list li{border:1px solid var(--line);border-radius:12px;margin:0 0 8px;background:var(--card,#fff)}
.pp-list li.is-done{background:var(--bg-soft)}
.pp-row{display:flex;align-items:center;gap:12px;padding:12px 14px;text-decoration:none;min-height:44px}
.pp-row input{width:20px;height:20px;flex:none;accent-color:var(--brand)}
.pp-kind{flex:none;font-size:.72rem;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:var(--brand);background:var(--bg-soft);border:1px solid var(--line);padding:3px 8px;border-radius:999px;white-space:nowrap}
.pp-txt{display:flex;flex-direction:column;line-height:1.4}
.pp-txt a{color:var(--ink);font-weight:600}
.pp-txt small{color:var(--muted);font-size:.8rem;margin-top:2px}
.pp-link{display:flex;width:100%}
.pp-actions{margin:14px 0 0}
.pp-done{border:1px solid var(--line);border-radius:16px;padding:24px;margin:26px 0 0;background:var(--grad-soft);text-align:center}
.pp-done-ic{width:44px;height:44px;border-radius:50%;background:var(--green,#147a3d);color:#fff;display:grid;place-items:center;font-size:1.3rem;margin:0 auto 10px}
.pp-done h2{margin:0 0 8px}
.pp-done p{color:var(--ink-2)}
"""

PRACTICE_CSS = """
.px-wrap{border:1px solid var(--line);border-radius:16px;padding:22px;margin:0 0 10px;background:var(--card,#fff)}
.px-head{display:flex;justify-content:space-between;font-size:.85rem;color:var(--muted);margin:0 0 10px}
.px-bar{background:var(--bg-soft);height:6px;border-radius:999px;overflow:hidden;margin:0 0 16px}
.px-bar span{display:block;height:100%;background:var(--grad);border-radius:999px;transition:width .25s var(--ease)}
.px-q{font-size:1.12rem;font-weight:700;margin:0 0 16px;line-height:1.5}
.px-opts{display:grid;gap:9px}
.px-opt{padding:12px 14px;border:1px solid var(--line);border-radius:12px;background:var(--bg-soft);font:inherit;font-size:.98rem;text-align:left;cursor:pointer;min-height:44px}
.px-opt:hover{border-color:var(--brand-2);background:var(--card,#fff)}
.px-opt.px-right{border-color:var(--green,#147a3d);background:#eef7f0;font-weight:600}
.px-opt.px-wrong{border-color:var(--brand-3,#c2407d);background:#fdeef4}
.px-word{display:inline-block;margin:0 6px 6px 0;padding:10px 16px;border:1px solid var(--line);border-radius:999px;background:var(--bg-soft);font:inherit;font-size:1rem;cursor:pointer;min-height:44px}
.px-word.px-used{opacity:.35;pointer-events:none}
.px-order{margin:0 0 12px}
.px-answer{min-height:52px;border:2px dashed var(--line);border-radius:12px;padding:12px 14px;margin:0 0 10px;font-size:1.05rem;background:var(--bg-soft)}
.px-order-btns{display:flex;gap:8px;margin:0 0 14px}
.px-fb{padding:13px 15px;border-radius:12px;font-size:.95rem;line-height:1.5;margin:14px 0 0}
.px-fb.ok{background:#eef7f0;border:1px solid #bfe3c9;color:#12532a}
.px-fb.bad{background:#fdeef4;border:1px solid #f3c3d8;color:#8f1d4e}
.px-explain{color:var(--ink-2);font-size:.88rem;margin-top:6px}
.px-next-wrap{margin:14px 0 0;text-align:right}
.px-note{color:var(--muted);font-size:.82rem;line-height:1.6;margin:16px 0 0;padding-top:12px;border-top:1px solid var(--line)}
.px-play{min-height:44px}
.px-tts-note{color:var(--muted);font-size:.8rem;margin-left:8px}
.px-done{text-align:center;padding:26px 10px}
.px-done-ic{width:46px;height:46px;border-radius:50%;background:var(--green,#147a3d);color:#fff;display:grid;place-items:center;font-size:1.3rem;margin:0 auto 12px}
.px-done h3{margin:0 0 8px}
.px-done p{color:var(--ink-2)}
.px-done-btns{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:16px}
.mp-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.95rem}
.mp-table th,.mp-table td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line)}
.mp-table th{font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}
"""

# ---------------------------------------------------------------- shared chrome
def head(title, desc, path, schema, rel):
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
<link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title} | EkGuru">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{BASE}/images/og-cover.jpg">
<meta property="og:site_name" content="EkGuru">
<meta property="article:published_time" content="2026-09-11">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="icon" href="{rel}images/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="{rel}images/apple-touch-icon.png">
<link rel="manifest" href="{rel}manifest.webmanifest">
<meta name="theme-color" content="#4f32d9">
<link rel="stylesheet" href="{rel}css/style.min.css">
<style>
.art{{max-width:760px;margin:0 auto;padding:0 20px 60px}}
.art h1{{font-size:2rem;line-height:1.25;margin:26px 0 10px}}
.art .meta{{color:var(--muted);font-size:.86rem;margin:0 0 26px}}
.art h2{{font-size:1.28rem;margin:34px 0 12px;padding-top:6px}}
.art p,.art li{{line-height:1.75}}
.art table{{width:100%;border-collapse:collapse;margin:18px 0;font-size:.95rem}}
.art th,.art td{{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line)}}
.art th{{font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}}
.art ul,.art ol{{padding-left:22px}}
.art li{{margin:7px 0}}
.crumb{{font-size:.84rem;color:var(--muted);padding:18px 0 0}}
.crumb a{{color:var(--muted)}}
.lede{{color:var(--ink-2);font-size:1.05rem;line-height:1.7;margin:0 0 22px}}
.related{{margin:40px 0 0;padding-top:26px;border-top:1px solid var(--line)}}
.related h2{{margin:0 0 12px;font-size:1.05rem}}
.rel-list{{list-style:none;padding:0;margin:14px 0 0}}
.rel-list li{{padding:11px 0;border-bottom:1px solid var(--line)}}
.rel-list li:last-child{{border-bottom:0}}
.rel-list a{{font-weight:600;display:block}}
.rel-list span{{display:block;color:var(--muted);font-size:.88rem;margin-top:2px;line-height:1.5}}
@media(pointer:coarse){{.pill,.px-opt,.px-word,.pp-row a,.rel-list a{{min-height:44px}}input,select,textarea,button{{min-height:44px}}}}
</style>
<script type="application/ld+json">{schema}</script>
</head>
<body>
<div class="art">
"""

FOOT = """
</div>
<!-- ekguru:trust-footer:start -->
<footer class="pw-ftr">
  <nav aria-label="Site information">
    <a href="__REL__">Home</a>
    <a href="__REL__about/">About</a>
    <a href="__REL__contact/">Contact</a>
    <a href="__REL__privacy/">Privacy</a>
    <a href="__REL__terms/">Terms</a>
    <a href="__REL__disclaimer/">Disclaimer</a>
  </nav>
  <p>
  © 2026 EkGuru — One Student. One Goal. One Guru.<br>
  Written and maintained by Prakash. Hindi lessons with native-speaking tutors, one to one.
  </p>
</footer>
<!-- ekguru:trust-footer:end -->
</body>
</html>
"""

SCRIPTS_COMMON = """<script src="__REL__js/site-config.js" defer></script>
<script src="__REL__js/analytics.js" defer></script>
<script defer>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("__REL__sw.js").catch(function () {});
  });
}
</script>
"""


def load_paths():
    import subprocess
    script = (
        "const fs=require('fs');"
        "global.window={};"
        "eval(fs.readFileSync(process.cwd()+'/js/learning-paths.js','utf8'));"
        "console.log(JSON.stringify(window.EKGURU_PATHS));"
    )
    res = subprocess.run(["node", "-e", script], capture_output=True, text=True, cwd=ROOT)
    if res.returncode != 0:
        raise SystemExit("node parse failed: " + res.stderr)
    return json.loads(res.stdout.strip())


def load_bank():
    import subprocess
    script = (
        "const fs=require('fs');"
        "global.window={};"
        "eval(fs.readFileSync(process.cwd()+'/js/practice-bank.js','utf8'));"
        "console.log(JSON.stringify(window.EKGURU_PRACTICE_BANK));"
    )
    res = subprocess.run(["node", "-e", script], capture_output=True, text=True, cwd=ROOT)
    if res.returncode != 0:
        raise SystemExit("node parse failed: " + res.stderr)
    return json.loads(res.stdout.strip())


def path_outline_html(p):
    """Static, no-JS lesson outline for a path page. Rendered server-side
    from learning-paths.js so the page is informative without JavaScript
    (and for crawlers). path-progress.js hides it once it mounts the
    interactive tracker, so JS users see one list, not two."""
    out = '<section id="path-outline" style="margin:4px 0 8px">\n'
    out += "  <h2>What's in this path</h2>\n"
    out += "  <ol>\n"
    for mod in p["modules"]:
        out += f'    <li><b>{mod["title"]}</b>\n      <ul>\n'
        for l in mod["lessons"]:
            out += f'        <li><a href="{l["url"]}">{l["title"]}</a>'
            if l.get("minutes"):
                out += f' <span style="color:var(--muted);font-size:.85rem">· {l["minutes"]} min</span>'
            out += "</li>\n"
        out += "      </ul>\n    </li>\n"
    out += "  </ol>\n"
    out += "</section>\n"
    return out


def sample_html(bank):
    """A short static 'what's inside' list rendered from the real bank,
    so the page is informative without JavaScript and carries real
    Devanagari examples. Generated — never hand-edited."""
    items = bank[:5]
    out = '<section class="whats-inside" style="margin:26px 0 0;padding-top:6px">\n'
    out += "  <h2>What you will practise</h2>\n"
    out += "  <ul>\n"
    for it in items:
        q = it.get("q") or " ".join(it.get("words") or [])
        a = it.get("a") or " ".join(it.get("answer") or []) or "—"
        out += f'    <li><b>{q}</b> — {a}</li>\n'
    out += "  </ul>\n"
    out += "  <p style=\"color:var(--muted);font-size:.82rem\">A few of the items in this lab; the run draws from the full bank and shuffles each time.</p>\n"
    out += "</section>\n"
    return out


def course_schema(path):
    p = path
    items = []
    for mod in p["modules"]:
        for l in mod["lessons"]:
            items.append({"@type": "ListItem", "name": l["title"], "url": BASE + l["url"]})
    return json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "Course", "@id": BASE + "/learn/paths/" + p["slug"] + "/#course",
         "name": p["title"] + " — EkGuru learning path",
         "description": p["goal"], "url": BASE + "/learn/paths/" + p["slug"] + "/",
         "inLanguage": "en", "teaches": "Hindi", "isAccessibleForFree": True,
         "educationalLevel": p["level"],
         "provider": {"@type": "Organization", "name": "EkGuru", "url": BASE + "/"},
         "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "online",
                                "courseWorkload": "PT4H"}},
        {"@type": "ItemList", "@id": BASE + "/learn/paths/" + p["slug"] + "/#list",
         "name": p["title"] + " lessons", "numberOfItems": len(items),
         "itemListElement": items},
    ]}, ensure_ascii=False)


def webapp_schema(name, desc, path):
    return json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "@id": BASE + path + "#app", "name": name,
         "description": desc, "url": BASE + path,
         "applicationCategory": "EducationalApplication",
         "operatingSystem": "Any modern browser", "inLanguage": "en",
         "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    ]}, ensure_ascii=False)


def build_paths_index(paths):
    """learn/paths/index.html — the hub listing every path."""
    rel = "../../"          # learn/paths/ is two levels deep
    url = "/learn/paths/"
    schema = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": BASE + "/learn/paths/#page",
         "name": "EkGuru Hindi learning paths",
         "description": "Six goal-based Hindi learning paths built from the free EkGuru guides, tools and practice labs.",
         "url": BASE + "/learn/paths/", "inLanguage": "en"}
    ]}, ensure_ascii=False)
    html = head("Hindi Learning Paths — Six Free Goal-Based Tracks",
                "Six free goal-based Hindi learning paths: from zero, speaking, reading, travel, everyday and grammar. Each with modules, practice, quizzes and review.",
                url, schema, rel)
    html += f'  <p class="crumb"><a href="{rel}">EkGuru</a> › <a href="../">Learn Hindi</a> › Learning paths</p>\n\n'
    html += '  <h1>Learning paths</h1>\n'
    html += '  <p class="meta">Six goal-based tracks · free, self-paced · updated 2026-09-11</p>\n\n'
    html += ('  <p class="lede">A path is a sequence: read a guide, use a tool, practise, check '
             'yourself, review. Pick the goal that matches where you are — not the one that '
             'sounds most impressive. You can always switch.</p>\n')
    html += '  <div class="rel-list">\n'
    for p in paths:
        html += ('    <div style="border:1px solid var(--line);border-radius:12px;margin:0 0 10px;padding:16px 18px">\n'
                 f'      <a href="{p["slug"]}/" style="font-weight:700;font-size:1.05rem">{p["title"]}</a>\n'
                 f'      <p style="color:var(--ink-2);margin:6px 0 2px">{p["tagline"]}</p>\n'
                 f'      <p style="color:var(--muted);font-size:.85rem;margin:0">{p["level"]} · {p["duration"]} · {sum(len(m["lessons"]) for m in p["modules"])} lessons</p>\n'
                 '    </div>\n')
    html += '  </div>\n'
    html += ('  <p style="color:var(--muted);font-size:.88rem;margin-top:18px">Not sure which path? '
             'Take the <a href="../practice/placement/">placement check</a> — a rough guide, not a certified test.</p>\n')
    html += FOOT.replace("__REL__", rel)
    html += SCRIPTS_COMMON.replace("__REL__", rel)
    os.makedirs(os.path.join(ROOT, "learn", "paths"), exist_ok=True)
    with open(os.path.join(ROOT, "learn", "paths", "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return ["learn/paths/"]


def build_paths(paths):
    out = []
    rel = "../../../"     # learn/paths/<slug>/ is three levels deep
    for p in paths:
        url = "/learn/paths/" + p["slug"] + "/"
        html = head(p["title"], p["goal"][:156], url, course_schema(p), rel)
        html += f'  <p class="crumb"><a href="{rel}">EkGuru</a> › <a href="../">Learning paths</a></p>\n\n'
        html += f'  <h1>{p["title"]}</h1>\n'
        html += f'  <p class="meta">{p["level"]} · {p["duration"]} · free, self-paced · updated 2026-09-11</p>\n\n'
        html += f'  <p class="lede">{p["tagline"]}</p>\n'
        for para in p["intro"]:
            html += f"<p>{para}</p>\n"
        html += "\n" + path_outline_html(p)
        html += f'  <div id="path-modules" data-path="{p["slug"]}"></div>\n'
        html += '\n  <section class="related">\n    <h2>All learning paths</h2>\n    <ul class="rel-list">\n'
        for o in paths:
            if o["slug"] == p["slug"]:
                continue
            html += f'      <li><a href="../{o["slug"]}/">{o["title"]}</a><span>{o["tagline"]}</span></li>\n'
        html += '    </ul>\n  </section>\n'
        html += FOOT.replace("__REL__", rel)
        html += SCRIPTS_COMMON.replace("__REL__", rel)
        html += '<script src="' + rel + 'js/learning-paths.js" defer></script>\n'
        html += '<script src="' + rel + 'js/path-progress.js" defer></script>\n'
        os.makedirs(os.path.join(ROOT, "learn", "paths", p["slug"]), exist_ok=True)
        with open(os.path.join(ROOT, "learn", "paths", p["slug"], "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        out.append("learn/paths/" + p["slug"] + "/")
    return out


# ---------------------------------------------------------------- practice pages
PRACTICE_PAGES = {
    "index.html": {
        "slug": "",
        "title": "Hindi Practice — Drills That Actually Help",
        "desc": "Free Hindi practice labs: vocabulary, grammar, sentence building, verbs, listening and a placement check. Recognition drills with honest limits — no fake fluency scores.",
        "h1": "Hindi practice — drills that actually help",
        "intro": [
            "These labs turn the guides into something you <em>do</em> rather than read. Each one is a short, repeatable drill with immediate feedback, stored in your own browser only.",
            "An honest word first: multiple-choice drills measure recognition and recall of forms — the easiest language skill. They do not measure speaking, and they do not measure following a native speaker at full speed. Use them to keep words and rules fresh; use a tutor for the rest."
        ],
        "hub": True,
    },
    "vocabulary": {
        "slug": "vocabulary",
        "title": "Hindi Vocabulary Practice — Word Meaning Drill",
        "desc": "Practise the most useful Hindi words: see the Devanagari, pick the meaning, get the explanation. Free, no sign-up, saved in your browser.",
        "h1": "Vocabulary practice",
        "intro": [
            "The twenty most useful everyday Hindi words, drilled in both directions. Read the Devanagari, pick the English meaning, and read the one-line explanation that makes the word stick.",
            "Vocabulary is the one thing repetition genuinely fixes, which is why this lab exists. Wrong answers come back sooner in your review queue."
        ],
        "bank": "vocabulary", "mode": "practice",
    },
    "grammar": {
        "slug": "grammar",
        "title": "Hindi Grammar Practice — Gender, Plural, Agreement",
        "desc": "Practise Hindi gender, plurals, verb agreement and tense with short multiple-choice drills and explanations. Free, no sign-up.",
        "h1": "Grammar practice",
        "intro": [
            "Gender, plurals, verb agreement and tenses — the four rules that decide whether your sentences are understood as you mean them. Each question explains the rule after you answer.",
            "This is recognition practice: picking the right form from options is easier than producing it in speech. Once the forms feel automatic here, they will come out right under pressure more often."
        ],
        "bank": "grammar", "mode": "practice",
    },
    "sentence-builder": {
        "slug": "sentence-builder",
        "title": "Hindi Sentence Builder — Put the Words in Order",
        "desc": "Arrange Hindi words into correct sentences and internalise Subject–Object–Verb word order. Free interactive practice with instant feedback.",
        "h1": "Sentence builder",
        "intro": [
            "Hindi puts the verb last, and that single difference makes early sentences feel backwards. This lab gives you scrambled words and asks you to rebuild the sentence — the fastest way to stop translating word by word.",
            "Tap the words in the order you think is right, then check. Getting the order wrong here is cheap; getting it wrong in a conversation is the expensive version."
        ],
        "bank": "sentences", "mode": "practice",
    },
    "verbs": {
        "slug": "verbs",
        "title": "Hindi Verb Practice — Endings and Tenses",
        "desc": "Practise Hindi verb endings: who is speaking, which gender, which tense. Fill-in drills with the rule explained after each answer.",
        "h1": "Verb practice",
        "intro": [
            "Hindi verbs change with the speaker's gender, the politeness level and the tense — three moving parts at once. This lab isolates them: pick the form that fits, then read why.",
            "Drill the forms here so that in real speech the ending chooses itself."
        ],
        "bank": "verbs", "mode": "practice",
    },
    "listening": {
        "slug": "listening",
        "title": "Hindi Listening Practice — Hear It, Choose It",
        "desc": "Hear Hindi words and phrases spoken aloud and pick what you heard. Uses your browser's computer voice — good for recognition, not a native accent.",
        "h1": "Listening practice",
        "intro": [
            "You hear a Hindi word or phrase spoken aloud, then choose what was said. An honest limitation: this is your browser's computer voice, not a native speaker — useful for training your ear to recognise words, not for learning a natural accent.",
            "If nothing plays, your browser has no speech synthesis; the text is shown so you can still use the drill."
        ],
        "bank": "listening", "mode": "practice",
    },
    "pronunciation": {
        "slug": "pronunciation",
        "title": "Hindi Pronunciation Lab — Minimal Pairs",
        "desc": "The Hindi sound pairs that English speakers confuse, with playback and plain explanations. No automatic pronunciation scoring — nothing here hears you.",
        "h1": "Pronunciation lab",
        "intro": [
            "Hindi distinguishes sounds English runs together — aspirated and unaspirated consonants, retroflex and dental t's. The pairs below are the ones worth practising, with a playback button that speaks each letter.",
            "Straight honesty: no automatic scoring here. A web page cannot hear your accent, and any tool that claims to grade your pronunciation is flattering you. Playback is a computer voice. The real check is a native speaker listening to you — which is exactly what a trial lesson is for."
        ],
        "bank": "minimalPairs", "mode": "practice",
    },
    "placement": {
        "slug": "placement",
        "title": "Hindi Placement Check — Where Should You Start?",
        "desc": "Twelve quick questions that suggest where to start or continue. A rough guide, not a certified placement test.",
        "h1": "Placement check",
        "intro": [
            "Twelve quick questions across the script, words and grammar, then a suggested starting path. This is a rough guide, not a certified test — no certificate, no level claim, just a sensible next step."
        ],
        "bank": "placement", "mode": "placement",
    },
    "daily": {
        "slug": "daily",
        "title": "Daily Hindi Practice — 5, 10 or 20 Questions",
        "desc": "A short mixed Hindi practice run every day: five, ten or twenty questions across vocabulary, grammar and verbs. Free, saved in your browser.",
        "h1": "Daily practice",
        "intro": [
            "A short mixed run every day beats a long session once a week. Pick your length — five, ten or twenty questions — drawn across vocabulary, grammar, sentence order and verbs.",
            "Consistency is the point, not the score. No account, no upload: your streak lives in this browser."
        ],
        "daily": True,
    },
    "review": {
        "slug": "review",
        "title": "Hindi Review — What Is Getting Wobbly",
        "desc": "Review the Hindi practice items you got wrong or haven't seen in a while. A simple box system, honestly not clinical spaced repetition.",
        "h1": "Review",
        "intro": [
            "Everything you have practised feeds a review queue: items you get wrong come back sooner, items you get right wait longer before they show up again.",
            "This is a simple box system — effective, but not clinical spaced repetition, and it does not pretend to be. Use it to stop words quietly falling out of your head."
        ],
        "mode": "review",
    },
    "reading": {
        "slug": "reading",
        "title": "Hindi Reading Lab — Read It, Get the Meaning",
        "desc": "Read short Hindi sentences in Devanagari and pick the meaning. Builds the habit of reading whole sentences instead of decoding word by word.",
        "h1": "Reading lab",
        "intro": [
            "Eight short, everyday sentences in Devanagari. Read the whole sentence, then pick what it means — the habit of taking in a sentence at once, rather than decoding it letter by letter.",
            "If the script is still slow for you, run the alphabet guide first, then come back here. Reading speed is just the script plus repetition."
        ],
        "bank": "reading", "mode": "practice",
    },
    "writing": {
        "slug": "writing",
        "title": "Hindi Writing & Devanagari Lab — Know the Letters",
        "desc": "Recognise the Devanagari letters by sound, then practise typing them in the typing tutor. Free, instant, no sign-up.",
        "h1": "Writing & Devanagari lab",
        "intro": [
            "Before you can write, you have to know which letter is which sound. This lab shows you a sound and asks you to pick the letter — recognition first, production second.",
            "Then take it to the typing tutor: writing Hindi on your phone is a genuinely useful everyday skill, and it drills the letters the same way handwriting does."
        ],
        "bank": "devanagari", "mode": "practice",
    },
    "speaking": {
        "slug": "speaking",
        "title": "Hindi Speaking Lab — Say It, Then Check",
        "desc": "Say useful Hindi phrases out loud, then reveal the answer and grade yourself. Honest prompted speaking — nothing here pretends to hear you.",
        "h1": "Speaking lab",
        "intro": [
            "Speaking is a physical skill, and a web page cannot hear you. So this lab does the one thing it honestly can: give you a phrase, make you say it out loud before you reveal the answer, and let you grade yourself.",
            "Playback is a computer voice — fine for checking you have the words right, useless for learning a natural accent. For that, a five-minute trial with a native speaker beats a hundred self-graded rounds."
        ],
        "bank": "speaking", "mode": "speak",
    },
}

RELATED = {
    "reading": [("The alphabet guide", "/learn/hindi-alphabet-for-beginners/"), ("Reading Hindi path", "/learn/paths/reading-hindi/"), ("Vocabulary practice", "/learn/practice/vocabulary/")],
    "writing": [("Hindi typing tutor", "/toolbox/hindi-typing/"), ("The alphabet guide", "/learn/hindi-alphabet-for-beginners/"), ("Pronunciation lab", "/learn/practice/pronunciation/")],
    "speaking": [("Hindi phrasebook", "/toolbox/hindi-phrasebook/"), ("Speaking Starter path", "/learn/paths/speaking-starter/"), ("Book a trial lesson", "/find-tutors.html")],
    "vocabulary": [("Hindi vocabulary tool", "/toolbox/hindi-vocabulary/"), ("Flashcards", "/toolbox/hindi-flashcards/"), ("The alphabet guide", "/learn/hindi-alphabet-for-beginners/")],
    "grammar": [("Gender — the full guide", "/learn/hindi-gender-masculine-feminine/"), ("Word order", "/learn/hindi-sentence-structure/"), ("Verbs guide", "/learn/hindi-verbs-present-past-future/")],
    "sentence-builder": [("Word order guide", "/learn/hindi-sentence-structure/"), ("Verb practice", "/learn/practice/verbs/"), ("Grammar practice", "/learn/practice/grammar/")],
    "verbs": [("Verbs guide", "/learn/hindi-verbs-present-past-future/"), ("Verb explorer tool", "/toolbox/hindi-verbs/"), ("Sentence builder", "/learn/practice/sentence-builder/")],
    "listening": [("Pronunciation lab", "/learn/practice/pronunciation/"), ("Phrasebook", "/toolbox/hindi-phrasebook/"), ("Travel phrases", "/learn/hindi-phrases-for-travel/")],
    "pronunciation": [("Pronunciation tool", "/toolbox/hindi-pronunciation/"), ("The alphabet guide", "/learn/hindi-alphabet-for-beginners/"), ("Listening practice", "/learn/practice/listening/")],
    "placement": [("All learning paths", "/learn/paths/"), ("Level test tool", "/toolbox/hindi-level-test/"), ("All practice", "/learn/practice/")],
    "daily": [("Daily Hindi — 30 days", "/daily-hindi/"), ("Flashcards", "/toolbox/hindi-flashcards/"), ("All practice", "/learn/practice/")],
    "review": [("All practice", "/learn/practice/"), ("Daily practice", "/learn/practice/daily/"), ("Flashcards", "/toolbox/hindi-flashcards/")],
}


def build_practice(bank):
    out = []
    hub_links = []
    for key, cfg in PRACTICE_PAGES.items():
        if key == "index.html":
            rel = "../../"        # learn/practice/ is two levels deep
            path = "/learn/practice/"
        else:
            rel = "../../../"     # learn/practice/<slug>/ is three deep
            path = "/learn/practice/" + cfg["slug"] + "/"
        html = head(cfg["title"], cfg["desc"], path, webapp_schema(cfg["title"], cfg["desc"], path), rel)
        if key == "index.html":
            html += f'  <p class="crumb"><a href="{rel}">EkGuru</a> › <a href="../">Learn Hindi</a> › Practice</p>\n\n'
        else:
            html += f'  <p class="crumb"><a href="{rel}">EkGuru</a> › <a href="../../">Learn Hindi</a> › <a href="../">Practice</a></p>\n\n'
        html += f'  <h1>{cfg["h1"]}</h1>\n'
        html += '  <p class="meta">A free EkGuru practice lab · updated 2026-09-11</p>\n\n'
        for para in cfg["intro"]:
            html += f"<p>{para}</p>\n"

        if cfg.get("bank") and bank.get(cfg["bank"]):
            html += sample_html(bank[cfg["bank"]])

        if cfg.get("hub"):
            # practice hub — static list of all labs
            labs = [
                ("Vocabulary", "vocabulary/", "Word meaning drill — the most useful everyday words."),
                ("Grammar", "grammar/", "Gender, plurals, agreement and tense."),
                ("Sentence builder", "sentence-builder/", "Put scrambled Hindi words back in order."),
                ("Verbs", "verbs/", "Endings, gender and tenses."),
                ("Reading", "reading/", "Read a Devanagari sentence, pick the meaning."),
                ("Writing & Devanagari", "writing/", "Know the letters by sound, then practise typing."),
                ("Speaking", "speaking/", "Say it aloud, then check yourself. No auto-scoring."),
                ("Listening", "listening/", "Hear it, choose it — computer voice, honest limits."),
                ("Pronunciation", "pronunciation/", "Minimal pairs with playback. No auto-scoring."),
                ("Daily practice", "daily/", "Five, ten or twenty mixed questions a day."),
                ("Review", "review/", "What is getting wobbly comes back sooner."),
                ("Placement check", "placement/", "Where should you start? A rough guide."),
            ]
            html += '<div class="rel-list">\n'
            for title, u, d in labs:
                html += f'<div class="pp-row" style="border:1px solid var(--line);border-radius:12px;margin:0 0 8px">' \
                        f'<a href="{u}" style="display:flex;width:100%;padding:14px 16px;text-decoration:none">' \
                        f'<span style="flex:1"><b style="color:var(--brand)">{title}</b><br>' \
                        f'<span style="color:var(--muted);font-size:.88rem">{d}</span></span>' \
                        f'<span style="color:var(--muted)">→</span></a></div>\n'
            html += "</div>\n"
        else:
            if cfg.get("daily"):
                html += ('  <p style="color:var(--muted)">Each run draws a fresh mix from the '
                         'vocabulary, grammar, sentence-order and verb banks — ' + str(len(bank.get("vocabulary", [])) + len(bank.get("grammar", [])) + len(bank.get("sentences", [])) + len(bank.get("verbs", []))) +
                         ' questions in total, shuffled every time.</p>\n')
                html += ('  <div class="px-wrap" id="daily-pick">\n'
                         '    <p><b>How long today?</b></p>\n'
                         '    <div style="display:flex;gap:8px;flex-wrap:wrap">\n'
                         '      <button type="button" class="btn btn-primary" data-n="5">5 questions</button>\n'
                         '      <button type="button" class="btn btn-ghost" data-n="10">10 questions</button>\n'
                         '      <button type="button" class="btn btn-ghost" data-n="20">20 questions</button>\n'
                         '    </div>\n'
                         '    <div id="practice-root"></div>\n'
                         '  </div>\n'
                         '  <script>\n'
                         '  document.getElementById("daily-pick").addEventListener("click", function(e){\n'
                         '    var b = e.target.closest("button[data-n]"); if(!b) return;\n'
                         '    var r = document.getElementById("practice-root");\n'
                         '    if (window.EkGuruPractice) EkGuruPractice.mount(r, {mode:"daily", count: +b.getAttribute("data-n")});\n'
                         '  });\n'
                         '  </script>\n')
            else:
                html += '  <div class="px-wrap"><div id="practice-root"></div></div>\n'
                html += ('  <script>\n'
                         '  document.addEventListener("DOMContentLoaded", function(){\n'
                         '    var r = document.getElementById("practice-root");\n'
                         f'    if (r && window.EkGuruPractice) EkGuruPractice.mount(r, {{bank:"{cfg.get("bank", "")}", mode:"{cfg["mode"]}"}});\n'
                         '  });\n'
                         '  </script>\n')

            # related learning
            rels = RELATED.get(cfg["slug"], [])
            if rels:
                html += '  <section class="related">\n    <h2>Related learning</h2>\n    <ul class="rel-list">\n'
                for t, u in rels:
                    html += f'      <li><a href="{u}">{t}</a></li>\n'
                html += '    </ul>\n  </section>\n'

        html += FOOT.replace("__REL__", rel)
        html += SCRIPTS_COMMON.replace("__REL__", rel)
        if not cfg.get("hub"):
            html += '<script src="' + rel + 'js/practice-bank.js" defer></script>\n'
            html += '<script src="' + rel + 'js/practice-engine.js" defer></script>\n'

        rel_dir = os.path.join(ROOT, "learn", "practice", key.replace("index.html", ""))
        if key == "index.html":
            os.makedirs(os.path.join(ROOT, "learn", "practice"), exist_ok=True)
            with open(os.path.join(ROOT, "learn", "practice", "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
            out.append("learn/practice/")
        else:
            os.makedirs(os.path.join(ROOT, "learn", "practice", cfg["slug"]), exist_ok=True)
            with open(os.path.join(ROOT, "learn", "practice", cfg["slug"], "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
            out.append("learn/practice/" + cfg["slug"] + "/")
    return out


def build_sitemap():
    """Regenerate sitemap-learn.xml from the learn/ file tree so the new
    paths and practice labs are discoverable. Single source of truth:
    every learn*/index.html in the repo. Guides rank 0.8, paths 0.7,
    practice labs 0.7 (interactive but with unique static content)."""
    urls = []   # (loc, priority)
    learn_root = os.path.join(ROOT, "learn")
    for dirpath, dirs, files in os.walk(learn_root):
        if "index.html" not in files:
            continue
        # Phase 6: never put noindex utility pages (review, my-progress) in the
        # sitemap — they are private local state, not searchable content.
        try:
            page = open(os.path.join(dirpath, "index.html"), encoding="utf-8").read()
            if 'name="robots" content="noindex' in page:
                continue
        except Exception:
            pass
        rel = os.path.relpath(dirpath, ROOT).replace(os.sep, "/")
        # rel is already e.g. "learn/aap-tum-tu-hindi" — build the URL from it
        # directly. (Fixed: previously prepended "/learn/" to a path that already
        # began with "learn/", emitting /learn/learn/… which 404s.)
        url = BASE + "/" + rel + "/"
        prio = "0.7" if ("/paths/" in url or "/practice/" in url) else "0.8"
        urls.append((url, prio))
    urls.sort()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<!-- Generated by tools/build-learn.py — do not hand-edit. -->',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, prio in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append("    <lastmod>2026-09-11</lastmod>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap-learn.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return len(urls)


def main():
    paths = load_paths()
    bank = load_bank()
    made_paths_index = build_paths_index(paths)
    made_paths = build_paths(paths)
    made_practice = build_practice(bank)
    n_sitemap = build_sitemap()
    print("generated paths index:")
    for p in made_paths_index:
        print("  ", p)
    print("generated paths:")
    for p in made_paths:
        print("  ", p)
    print("generated practice:")
    for p in made_practice:
        print("  ", p)
    print("sitemap-learn.xml: %d urls" % n_sitemap)


if __name__ == "__main__":
    main()

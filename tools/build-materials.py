#!/usr/bin/env python3
"""EkGuru — build the /materials/ learning-resource hub (Phase 2).

Single source of truth for every materials page. Re-running this file
regenerates the hub and every material from the data below, so a fix
applies everywhere instead of being hand-edited on 15 pages.

Material pages are QUICK-REFERENCE resources: printable tables, charts,
practice and checklists that point at the deep /learn/ guides and the
/toolbox/ tools. They are deliberately different from the guides — a
learner prints these, a reader reads those.

Usage:  python3 tools/build-materials.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://ekguru.shop"
TODAY = "2026-09-12"

CATS = [
    ("beginner", "Beginner Hindi"),
    ("alphabet", "Alphabet"),
    ("pronunciation", "Pronunciation"),
    ("vocabulary", "Vocabulary"),
    ("grammar", "Grammar"),
    ("verbs", "Verbs"),
    ("conversation", "Conversation"),
    ("reading", "Reading"),
    ("writing", "Writing"),
    ("travel", "Travel"),
    ("work", "Work"),
    ("family", "Family"),
    ("revision", "Revision"),
]
CAT_LABEL = dict(CATS)

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def depth(rel_dir):
    # rel_dir is a directory path ending in "/" (page is index.html inside it).
    # One "../" per path segment reaches the site root, matching the rest of
    # the site, which uses depth-relative links (never root-relative, since
    # GitHub Pages can serve the site from a project subpath).
    return "../" * len([s for s in rel_dir.split("/") if s])

STYLE = """
.art{max-width:760px;margin:0 auto;padding:0 20px 60px}
.art h1{font-size:2rem;line-height:1.25;margin:26px 0 10px}
.art .meta{color:var(--muted);font-size:.86rem;margin:0 0 26px}
.art h2{font-size:1.28rem;margin:34px 0 12px;padding-top:6px}
.art p,.art li{line-height:1.75}
.art table{width:100%;border-collapse:collapse;margin:18px 0;font-size:.95rem}
.art th,.art td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line)}
.art th{font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}
.art ul,.art ol{padding-left:22px}
.art li{margin:7px 0}
.crumb{font-size:.84rem;color:var(--muted);padding:18px 0 0}
.crumb a{color:var(--muted)}
.pg-note{border:1px solid var(--warn-line,#f0dfae);background:var(--warn-soft,#fff8e6);
  border-radius:12px;padding:15px 18px;margin:0 0 26px;font-size:.9rem;line-height:1.65}
.pg-note b{display:block;margin:0 0 5px;color:var(--ink)}
.pg-note p{margin:0;color:var(--ink-2);max-width:none}
.lvl{display:inline-block;font-size:.78rem;font-weight:800;letter-spacing:.06em;
  text-transform:uppercase;color:var(--brand);background:#f1edff;padding:5px 12px;border-radius:999px;margin:0 0 14px}
.rel{margin:36px 0 0;padding-top:24px;border-top:1px solid var(--line)}
.rel h2{margin:0 0 12px;font-size:1.05rem}
.rel a{display:block;padding:9px 0;color:var(--brand);text-decoration:none;border-bottom:1px solid var(--line)}
.rel a:last-child{border-bottom:0}
.rel a:hover{text-decoration:underline}
.pg-cta-box{margin:36px 0 0;padding:22px 20px;border:1px solid var(--line);border-radius:14px;background:var(--bg-soft)}
.pg-cta-box h2{margin:0 0 8px;font-size:1.05rem}
.pg-cta-box p{margin:8px 0}
.pg-cta-box a{color:var(--brand)}
details{margin:12px 0;border:1px solid var(--line);border-radius:10px;padding:12px 15px;background:var(--bg-soft)}
details summary{cursor:pointer;font-weight:700}
details p{margin:10px 0 0;color:var(--ink-2)}
.dv{font-family:"Noto Sans Devanagari","Nirmala UI",system-ui,sans-serif;line-height:1.85}
.art-nav{display:flex;gap:12px;justify-content:space-between;margin:34px 0 0;font-size:.9rem;flex-wrap:wrap}
@media print{.no-print,.rel,.art-nav,.pg-cta-box,ins,.adsbygoogle{display:none!important}.art{max-width:none;padding:0}}
@media(pointer:coarse){.rel a{display:inline-block;padding-block:10px}input,select,textarea,button{min-height:44px}}
"""

def render_blocks(blocks):
    out = []
    for block in blocks:
        kind = block[0]
        payload = block[1:]
        if kind == "p":
            out.append("<p>%s</p>" % payload[0])
        elif kind == "table":
            head, rows = payload[0]
            out.append('<div class="scroll"><table>')
            if head:
                out.append("<tr>" + "".join("<th>%s</th>" % c for c in head) + "</tr>")
            for r in rows:
                out.append("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>")
            out.append("</table></div>")
        elif kind == "ul":
            out.append("<ul>" + "".join("<li>%s</li>" % i for i in payload[0]) + "</ul>")
        elif kind == "ol":
            out.append("<ol>" + "".join("<li>%s</li>" % i for i in payload[0]) + "</ol>")
        elif kind == "note":
            out.append('<div class="pg-note"><b>%s</b><p>%s</p></div>' % (payload[0], payload[1]))
    return "\n".join(out)

def jsonld(mat):
    url = SITE + "/materials/%s/%s/" % (mat["category"], mat["slug"])
    crumb = [{"@type": "ListItem", "position": 1, "name": "EkGuru", "item": SITE + "/"},
             {"@type": "ListItem", "position": 2, "name": "Materials", "item": SITE + "/materials/"},
             {"@type": "ListItem", "position": 3, "name": CAT_LABEL[mat["category"]], "item": SITE + "/materials/#" + mat["category"]},
             {"@type": "ListItem", "position": 4, "name": mat["title"], "item": url}]
    return {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "@id": url + "#article", "headline": mat["title"],
             "description": mat["meta"], "inLanguage": "en",
             "datePublished": TODAY, "dateModified": TODAY,
             "author": {"@type": "Organization", "name": "EkGuru", "url": SITE + "/"},
             "publisher": {"@type": "Organization", "name": "EkGuru", "url": SITE + "/",
                           "logo": {"@type": "ImageObject", "url": SITE + "/images/logo.svg"}},
             "mainEntityOfPage": url, "about": {"@type": "Thing", "name": "Hindi language"},
             "isAccessibleForFree": True},
            {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": crumb},
            {"@type": "LearningResource", "@id": url + "#resource", "name": mat["title"],
             "description": mat["meta"], "educationalLevel": mat["level"],
             "learningResourceType": "Worksheet", "teaches": "Hindi language",
             "inLanguage": "en", "isAccessibleForFree": True,
             "provider": {"@type": "Organization", "name": "EkGuru", "url": SITE + "/"}},
        ],
    }

def head(mat=None, rel_dir="materials/"):
    d = depth(rel_dir)
    if mat is None:
        title = "Hindi Learning Materials — Charts, Worksheets & Quick References | EkGuru"
        meta = "Printable Hindi learning materials: Devanagari charts, vocabulary lists, grammar references, verb tables and practice worksheets. Free, no sign-up."
        url = SITE + "/materials/"
    else:
        title = mat["title"] + " | EkGuru"
        meta = mat["meta"]
        url = SITE + "/materials/%s/%s/" % (mat["category"], mat["slug"])
    out = ['<!DOCTYPE html>\n<html lang="en" dir="ltr">\n<head>',
           '<meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width,initial-scale=1">',
           "<title>%s</title>" % esc(title),
           '<meta name="description" content="%s">' % esc(meta),
           '<meta name="author" content="EkGuru">',
           '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">',
           '<link rel="canonical" href="%s">' % url,
           '<meta property="og:type" content="article">',
           '<meta property="og:title" content="%s">' % esc(title),
           '<meta property="og:description" content="%s">' % esc(meta),
           '<meta property="og:url" content="%s">' % url,
           '<meta property="og:image" content="%s/images/og-cover.jpg">' % SITE,
           '<meta property="og:site_name" content="EkGuru">',
           '<meta property="article:published_time" content="%s">' % TODAY,
           '<meta name="twitter:card" content="summary_large_image">',
           '<link rel="icon" href="%simages/favicon.ico" sizes="any">' % d,
           '<link rel="apple-touch-icon" href="%simages/apple-touch-icon.png">' % d,
           '<link rel="manifest" href="%smanifest.webmanifest">' % d,
           '<meta name="theme-color" content="#4f32d9">',
           '<link rel="stylesheet" href="%scss/style.min.css">' % d,
           "<style>" + STYLE + "</style>",
           '<script type="application/ld+json">%s</script>' % json.dumps(jsonld(mat) if mat else {"@context":"https://schema.org","@type":"WebPage","name":title,"url":url}, ensure_ascii=False),
           '<!-- ekguru:adsense:start -->',
           '<link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin>',
           '<link rel="preconnect" href="https://googleads.g.doubleclick.net" crossorigin>',
           '<meta name="google-adsense-account" content="ca-pub-8175326569491671">',
           '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8175326569491671" crossorigin="anonymous"></script>',
           '<!-- ekguru:adsense:end -->',
           "</head>\n<body>"]
    return "\n".join(out), d

def tail(d):
    return ('<script src="%sjs/site-config.js" defer></script>\n'
            '<!-- ekguru:scroll-restore:start -->\n'
            '<script src="%sjs/scroll-restore.js"></script>\n'
            '<!-- ekguru:scroll-restore:end -->\n'
            '<!-- ekguru:recovery:start -->\n'
            '<script src="%sjs/recovery.js" defer></script>\n'
            '<!-- ekguru:recovery:end -->\n'
            '<script src="%sjs/analytics.js" defer></script>\n'
            '<script defer>\n'
            'if ("serviceWorker" in navigator) {\n'
            '  window.addEventListener("load", function () {\n'
            '    navigator.serviceWorker.register("%ssw.js").catch(function () {});\n'
            '  });\n'
            '}\n'
            '</script>\n'
            '<!-- ekguru:trust-footer:start -->\n'
            '<footer class="pw-ftr">\n'
            '  <nav aria-label="Site information">\n'
            '    <a href="%s">Home</a>\n'
            '    <a href="%sabout/">About</a>\n'
            '    <a href="%scontact/">Contact</a>\n'
            '    <a href="%sprivacy/">Privacy</a>\n'
            '    <a href="%sterms/">Terms</a>\n'
            '    <a href="%sdisclaimer/">Disclaimer</a>\n'
            '    <a href="%sfaq/">FAQ</a>\n'
            '  </nav>\n'
            '  <p>\n'
            '  \u00a9 2026 EkGuru \u2014 One Student. One Goal. One Guru.<br>\n'
            '  Written and maintained by Prakash. Hindi lessons with native-speaking tutors, one to one.\n'
            '  </p>\n'
            '</footer>\n'
            '<!-- ekguru:trust-footer:end -->\n'
            "</body>\n</html>\n") % ((d,) * 12)

def rel_block(title, links, d):
    if not links:
        return ""
    items = "".join('<a href="%s%s">%s<span>%s</span></a>' % (d, u.lstrip("/"), t, s)
                    for t, s, u in links)
    return '<div class="rel"><h2>%s</h2>%s</div>' % (title, items)

def build_material(mat):
    rel_dir = "materials/%s/%s/" % (mat["category"], mat["slug"])
    d = depth(rel_dir)
    h, _ = head(mat, rel_dir)
    body = ['<div class="art">']
    body.append('<p class="crumb"><a href="%s">EkGuru</a> \u203a <a href="%smaterials/">Materials</a> \u203a <a href="%smaterials/#%s">%s</a> \u203a %s</p>'
               % (d, d, d, mat["category"], CAT_LABEL[mat["category"]], esc(mat["title"])))
    body.append('<h1>%s</h1>' % esc(mat["title"]))
    body.append('<p class="meta">A free EkGuru material \u00b7 updated %s</p>' % TODAY)
    body.append('<span class="lvl">%s</span>' % esc(mat["level"]))
    body.append('<div class="pg-note"><b>What this is for</b><p>%s</p></div>' % esc(mat["purpose"]))
    body.append('<h2>What you will learn</h2>')
    body.append('<ul>' + "".join('<li>%s</li>' % esc(i) for i in mat["learn"]) + "</ul>")
    if mat.get("quickref"):
        body.append('<h2>Quick reference</h2>')
        body.append(render_blocks([("table", mat["quickref"])]))
    for sec in mat.get("sections", []):
        body.append("<h2>%s</h2>" % esc(sec["h"]))
        body.append(render_blocks(sec["body"]))
    if mat.get("mistakes"):
        body.append('<h2>Common mistakes</h2>')
        body.append(render_blocks([("table", (["Wrong", "Right", "Why"], mat["mistakes"]))]))
    if mat.get("practice"):
        body.append('<h2>Practice</h2>')
        body.append(render_blocks([("ol", mat["practice"])]))
    if mat.get("quiz"):
        body.append('<h2>Mini quiz</h2>')
        for i, q in enumerate(mat["quiz"], 1):
            body.append('<details><summary>%d. %s</summary><p>%s</p></details>'
                        % (i, esc(q["q"]), esc(q["a"])))
    body.append(rel_block("Related tools", mat.get("tools", []), d))
    body.append(rel_block("Related lessons", mat.get("lessons", []), d))
    body.append(rel_block("Related material", mat.get("material", []), d))
    # Journey: content → material → tool → practice → lesson → path → tutor.
    # Every material closes with the same three next actions, so a learner
    # never dead-ends on a printable sheet.
    body.append('<div class="pg-cta-box"><h2>Keep going</h2>'
                '<p>A chart helps only once you use it. Drill these same points in the '
                '<a href="%slearn/practice/">practice labs</a>, follow a '
                '<a href="%slearn/paths/">learning path</a> to keep the order right, '
                'or practise one to one with a native-speaking tutor.</p>'
                '<p><a class="btn btn-primary" href="%sfind-tutors.html">See the tutors</a> '
                '<a class="btn btn-ghost" href="%slearn/practice/">Practise this</a> '
                '<a class="btn btn-ghost" href="%slearn/paths/">Learning paths</a></p></div>'
                % (d, d, d, d, d))
    nxt = mat.get("next")
    if nxt:
        body.append('<div class="art-nav"><button class="btn btn-ghost no-print" onclick="window.print()">\U0001F5A8 Print / save as PDF</button>'
                    '<a class="btn btn-primary" href="%s%s">Next: %s</a></div>' % (d, nxt[1].lstrip("/"), esc(nxt[0])))
    else:
        body.append('<div class="art-nav"><button class="btn btn-ghost no-print" onclick="window.print()">\U0001F5A8 Print / save as PDF</button>'
                    '<a class="btn btn-primary" href="%smaterials/">All materials</a></div>' % d)
    body.append("</div>")
    html = h + "\n" + "\n".join(body) + "\n" + tail(d)
    path = os.path.join(ROOT, rel_dir, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path

def build_hub(mats):
    d = "../"
    h, _ = head(None, "materials/")
    body = ['<div class="art">',
            '<p class="crumb"><a href="../">EkGuru</a> \u203a Materials</p>',
            "<h1>Hindi learning materials</h1>",
            '<p class="meta">Printable charts, worksheets and quick references \u00b7 updated %s</p>' % TODAY,
            "<p>Everything here is made to be <strong>used and printed</strong> \u2014 a chart to pin up, a list to memorise, a worksheet to scribble on. The <a href=\"../learn/\">guides</a> explain the why; these materials are the what-you-need-in-front-of-you. Nothing is hidden behind a sign-up, and every download button on this site is a real print button, never a fake one.</p>",
            '<div class="pg-note"><b>Honest note on levels</b><p>"Beginner" means no prior Hindi; "high beginner" means you can read the script and hold a short, slow conversation. No page here promises fluency by a date \u2014 materials keep knowledge fresh, they do not manufacture it.</p></div>']
    by_cat = {}
    for m in mats:
        by_cat.setdefault(m["category"], []).append(m)
    for slug, label in CATS:
        items = by_cat.get(slug, [])
        body.append('<h2 id="%s">%s</h2>' % (slug, label))
        if items:
            body.append('<div class="rel-list" style="list-style:none;padding:0;margin:0">')
            for m in items:
                body.append('<a href="%s/%s/" style="display:block;padding:13px 16px;border:1px solid var(--line);border-radius:12px;margin:0 0 8px;text-decoration:none">'
                            '<b style="color:var(--brand)">%s</b><br>'
                            '<span style="color:var(--muted);font-size:.88rem">%s \u00b7 %s</span></a>'
                            % (slug, m["slug"], esc(m["title"]), esc(m["level"]), esc(m["purpose"])))
            body.append("</div>")
        else:
            body.append('<p class="muted">Coming in the next batch \u2014 for now see the related <a href="../learn/">guide</a>.</p>')
    body.append('<div class="rel"><h2>Use these together</h2>'
                '<a href="../learn/">Free guides<span>The explanations these materials reference.</span></a>'
                '<a href="../toolbox/">Interactive tools<span>Alphabet explorer, flashcards, quiz, typing \u2014 free, no sign-up.</span></a>'
                '<a href="../learn/practice/">Practice labs<span>Turn the lists into recall with short drills.</span></a>'
                '<a href="../learn/paths/">Learning paths<span>Six goal-based tracks that sequence it all.</span></a></div>')
    body.append("</div>")
    html = h + "\n" + "\n".join(body) + "\n" + tail(d)
    path = os.path.join(ROOT, "materials", "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path

# --------------------------------------------------------------------------
# MATERIAL DATA
# --------------------------------------------------------------------------
M = []

M.append({
    "slug": "devanagari-chart", "category": "alphabet",
    "title": "Devanagari Vowels & Consonants \u2014 Quick Chart",
    "meta": "One printable chart of every Devanagari vowel and consonant with its Romanised sound and an English word that holds the same sound. Free, no sign-up.",
    "level": "Beginner",
    "purpose": "A single sheet to pin above your desk while the letter shapes stop looking like drawings and start looking like words. Pair it with the alphabet guide for the full explanation.",
    "learn": ["The 12 vowels and their sounds", "The 33 consonants, grouped the way Hindi speakers group them", "The matras (vowel signs) that attach to consonants", "The two nasal marks and the halant"],
    "quickref": (["Letter", "Romanised", "Sound (English hint)"], [
        ["\u0905", "a", "the 'u' in 'bus'"], ["\u0906", "\u0101", "the 'a' in 'father'"],
        ["\u0907", "i", "the 'i' in 'sit'"], ["\u0908", "\u012b", "the 'ee' in 'see'"],
        ["\u0909", "u", "the 'u' in 'put'"], ["\u090a", "\u016b", "the 'oo' in 'food'"],
        ["\u090f", "e", "the 'e' in 'they'"], ["\u0910", "ai", "the 'a' in 'cat' + 'y'"],
        ["\u0913", "o", "the 'o' in 'go'"], ["\u0914", "au", "the 'ow' in 'cow'"],
        ["\u0905\u0902", "\u1e43 (anusv\u0101ra)", "nasal, like 'n' in 'bank'"],
        ["\u0905\u0903", "\u1e25 (visarga)", "a breathy 'h' at the end"],
    ]),
    "sections": [
        {"h": "The consonants, in Hindi's own order", "body": [
            ("p", "Hindi groups its consonants by where the tongue makes them \u2014 back of the mouth to the lips. Each group runs unaspirated, aspirated, voiced, then voiced-aspirated. You do not need the Sanskrit names; you need to notice that <b>क and ख</b> are a pair, <b>प and फ</b> are a pair, and so on."),
            ("table", (["Group", "Consonants"], [
                ["k-group (velar)", "<span class=\"dv\">\u0915 ka \u00b7 \u0916 kha \u00b7 \u0917 ga \u00b7 \u0918 gha \u00b7 \u0919 \u1e45a</span>"],
                ["c-group (palatal)", "<span class=\"dv\">\u091a ca \u00b7 \u091b cha \u00b7 \u091c ja \u00b7 \u091d jha \u00b7 \u091e \u00f1a</span>"],
                ["\u1e6d-group (retroflex)", "<span class=\"dv\">\u091f \u1e6da \u00b7 \u0920 \u1e6dha \u00b7 \u0921 \u1e0da \u00b7 \u0922 \u1e0dha \u00b7 \u0923 \u1e47a</span>"],
                ["t-group (dental)", "<span class=\"dv\">\u0924 ta \u00b7 \u0925 tha \u00b7 \u0926 da \u00b7 \u0927 dha \u00b7 \u0928 na</span>"],
                ["p-group (labial)", "<span class=\"dv\">\u092a pa \u00b7 \u092b pha \u00b7 \u092c ba \u00b7 \u092d bha \u00b7 \u092e ma</span>"],
                ["semivowels", "<span class=\"dv\">\u092f ya \u00b7 \u0930 ra \u00b7 \u0932 la \u00b7 \u0935 va</span>"],
                ["sibilants + h", "<span class=\"dv\">\u0936 \u015ba \u00b7 \u0937 \u1e63a \u00b7 \u0938 sa \u00b7 \u0939 ha</span>"],
            ])),
        ]},
        {"h": "Matras \u2014 the vowel signs", "body": [
            ("p", "A consonant by itself carries an implied short 'a'. To change the vowel you hang a sign (matra) on the consonant. \u0915 (ka) becomes:"),
            ("table", (["ka + sign", "Result", "Romanised"], [
                ["\u0915", "\u0915", "ka"], ["\u0915\u093e", "\u0915\u093e", "k\u0101"],
                ["\u0915\u093f", "\u0915\u093f", "ki"], ["\u0915\u0940", "\u0915\u0940", "k\u012b"],
                ["\u0915\u0941", "\u0915\u0941", "ku"], ["\u0915\u0942", "\u0915\u0942", "k\u016b"],
                ["\u0915\u0947", "\u0915\u0947", "ke"], ["\u0915\u0948", "\u0915\u0948", "kai"],
                ["\u0915\u094b", "\u0915\u094b", "ko"], ["\u0915\u094c", "\u0915\u094c", "kau"],
                ["\u0915\u094d", "\u0915\u094d", "k (halant \u2014 no vowel)"],
            ])),
            ("note", "One habit that saves you hours", "Read a word right-to-left in sound terms: the sign after a consonant belongs to the consonant before it. \u0915\u093f\u0924\u093e\u092c is k+i = ki, then t+\u0101 = t\u0101, then b = ba \u2192 ki-t\u0101-b, 'book'."),
        ]},
    ],
    "mistakes": [
        ["Reading \u0915\u093f as 'kai'", "\u0915\u093f is 'ki' (short i)", "The \u093f sign sits before the consonant in writing but is spoken after it."],
        ["Ignoring the aspirated pairs", "क (ka) and ख (kha) are different letters", "ख has a puff of air; they change meaning (\u0915\u093e\u0932 era vs \u0916\u093e\u0932 skin)."],
        ["Forgetting the implied 'a'", "\u0915\u092e is 'kam', not 'km'", "A bare consonant carries a short 'a'."],
    ],
    "practice": [
        "Sound out, then check: \u0915\u092e\u0932 (ka-mal, lotus), \u0928\u092e\u0938\u094d\u0924\u0947 (na-mas-te), \u0927\u0928\u094d\u092f\u0935\u093e\u0926 (dhan-ya-v\u0101d).",
        "Write your first name in Devanagari using the chart, one sound at a time.",
        "Cover the Romanised column and read the chart aloud once a day for a week.",
    ],
    "quiz": [
        {"q": "Which sound does \u0906 (\u0101) make?", "a": "A long 'a' like the 'a' in 'father' \u2014 distinct from \u0905, the short 'u'-like 'a'."},
        {"q": "What is the difference between क and ख?", "a": "ख (kha) is aspirated \u2014 a puff of air after the k. English speakers hear them as the same sound, but they are different letters."},
        {"q": "How do you write 'ki'?", "a": "\u0915\u093f \u2014 the \u093f sign is written before the consonant but pronounced after it: k + i."},
    ],
    "tools": [("Alphabet explorer", "See and hear every letter, click by click.", "/toolbox/hindi-alphabet/")],
    "lessons": [("The Hindi Alphabet \u2014 full guide", "Vowels, consonants and matras explained in depth, with the order to learn them in.", "/learn/hindi-alphabet-for-beginners/")],
    "material": [("Reading Devanagari in a week", "Turn this chart into reading with a daily plan.", "/materials/beginner/reading-guide/")],
    "next": ("Read Devanagari in a week", "/materials/beginner/reading-guide/"),
})

M.append({
    "slug": "reading-guide", "category": "beginner",
    "title": "Reading Devanagari in a Week \u2014 A Practical Plan",
    "meta": "A day-by-day plan to start reading Hindi script in a week: what to learn each day, ten words to sound out, and the habits that make it stick. Free.",
    "level": "Beginner",
    "purpose": "Reading the script is the single biggest unlock in Hindi \u2014 everything you look at stops being decoration. This is a one-week plan, not a promise: a week gets you sounding words out, not reading novels.",
    "learn": ["Why Devanagari is easier than it looks (it is phonetic)", "A seven-day order that respects how the letters actually build words", "The two habits that stop learners getting stuck", "Ten practice words with the sounding-out shown"],
    "quickref": (["Day", "Learn", "Do"], [
        ["1", "Vowels \u0905 \u0906 \u0907 \u0908 \u0909 \u090a", "Say each five times; write each five times"],
        ["2", "Consonants \u0915 \u0916 \u0917 \u0918 \u091a \u091b \u091c \u091d", "Copy them; notice the unaspirated/aspirated pairs"],
        ["3", "Consonants \u091f \u0920 \u0921 \u0922 \u0924 \u0925 \u0926 \u0927 \u0928", "Learn the retroflex vs dental split \u2014 it is the hard one"],
        ["4", "Consonants \u092a \u092b \u092c \u092d \u092e + \u092f \u0930 \u0932 \u0935", "Add the semivowels; start joining two letters"],
        ["5", "\u0936 \u0937 \u0938 \u0939 + the matras", "Read the matra table; write ka, k\u0101, ki, k\u012b, ku, k\u016b, ke, ko"],
        ["6", "Halant and the first conjuncts", "Sound out the ten practice words below"],
        ["7", "Read something real", "Read shop signs, your own name, the practice words without help"],
    ]),
    "sections": [
        {"h": "Two habits that do the work", "body": [
            ("ul", [
                "<b>Sound, never memorise.</b> Devanagari is phonetic \u2014 every letter is one sound, every time. You are not memorising 600 spellings, you are learning 45 sounds and combining them.",
                "<b>Read the vowel after the consonant.</b> In \u0915\u093f\u0924\u093e\u092c the \u093f comes before the \u0915 in writing but is said after it: ki-t\u0101-b. This one habit fixes most early misreadings.",
            ]),
        ]},
        {"h": "Ten words to sound out", "body": [
            ("p", "Cover the Romanised column. Sound each word out letter by letter, then check."),
            ("table", (["Word", "Sounded out", "Meaning"], [
                ["\u0915\u092e\u0932", "ka-mal", "lotus"], ["\u0928\u092e\u0938\u094d\u0924\u0947", "na-mas-te", "hello"],
                ["\u0927\u0928\u094d\u092f\u0935\u093e\u0926", "dhan-ya-v\u0101d", "thank you"], ["\u0915\u093f\u0924\u093e\u092c", "ki-t\u0101-b", "book"],
                ["\u092a\u093e\u0928\u0940", "p\u0101-n\u012b", "water"], ["\u0906\u0926\u092e\u0940", "\u0101d-m\u012b", "man"],
                ["\u0914\u0930\u0924", "au-rat", "woman"], ["\u092c\u091a\u094d\u091a\u093e", "bac-ch\u0101", "child"],
                ["\u0926\u094b\u0938\u094d\u0924", "dost", "friend"], ["\u0938\u094d\u0915\u0942\u0932", "sk\u016bl", "school"],
            ])),
        ]},
    ],
    "mistakes": [
        ["Waiting to 'know' the alphabet before reading", "Start sounding out words on day one", "You learn letters by meeting them in words, not by memorising the chart cold."],
        ["Reading \u0938\u094d\u0915\u0942\u0932 as 'sa-ka-ula'", "The halant \u094d joins the s to the k: 'sk\u016bl'", "The halant strips a letter's vowel and glues it to the next."],
        ["Expecting silent letters", "Every letter sounds, every time", "There is no English-style silent 'e' \u2014 that is the point of a phonetic script."],
    ],
    "practice": [
        "Day 1\u20133: copy each day's letters five times while saying the sound.",
        "Day 4\u20136: sound out the ten words daily, timed; aim under two minutes by day seven.",
        "Day 7: write your name and three words you see around you (signs, packaging, your phone).",
    ],
    "quiz": [
        {"q": "Why is Devanagari easier to read than English spelling?", "a": "It is phonetic \u2014 one letter, one sound, every time. English spelling is historical and irregular; Devanagari spelling follows speech."},
        {"q": "What does the halant (\u094d) do?", "a": "It removes a consonant's implied 'a' and joins it to the next letter, as in \u0938\u094d\u0915\u0942\u0932 (sk\u016bl)."},
    ],
    "tools": [("Alphabet explorer", "Click a letter, hear it, see it in a word.", "/toolbox/hindi-alphabet/"), ("Typing tutor", "Start typing the letters you are learning.", "/toolbox/hindi-typing/")],
    "lessons": [("The Hindi Alphabet \u2014 full guide", "The deeper explanation behind this plan.", "/learn/hindi-alphabet-for-beginners/")],
    "material": [("Devanagari chart", "The one-page chart this plan uses.", "/materials/alphabet/devanagari-chart/")],
    "next": ("Hindi sounds English speakers get wrong", "/materials/pronunciation/pronunciation-guide/"),
})

M.append({
    "slug": "pronunciation-guide", "category": "pronunciation",
    "title": "Hindi Sounds English Speakers Get Wrong",
    "meta": "The Hindi sound pairs English speakers confuse most \u2014 aspirated vs plain, retroflex vs dental \u2014 with minimal pairs to practise aloud. Free.",
    "level": "Beginner",
    "purpose": "Hindi has a handful of sounds English does not. Get these six pairs right and your Hindi stops sounding like an accent and starts sounding like Hindi \u2014 this is the highest-value pronunciation work there is.",
    "learn": ["The aspirated vs plain consonant pairs", "The retroflex vs dental split (\u091f/\u0924, \u0921/\u0926)", "Why the short/long vowel length matters", "Minimal pairs to practise each contrast aloud"],
    "quickref": (["Contrast", "Sound 1", "Sound 2", "Example pair"], [
        ["plain vs aspirated (k)", "\u0915 ka (no puff)", "\u0916 kha (puff of air)", "\u0915\u093e\u0932 k\u0101l (era) / \u0916\u093e\u0932 kh\u0101l (skin)"],
        ["plain vs aspirated (p)", "\u092a pa (no puff)", "\u092b pha (puff of air)", "\u092a\u0932 pal (moment) / \u092b\u0932 phal (fruit)"],
        ["dental vs retroflex (d)", "\u0926 da (tongue on teeth)", "\u0921 \u1e0da (tongue curled back)", "\u0926\u093e\u0932 d\u0101l (lentils) / \u0921\u093e\u0932 \u1e0d\u0101l (branch)"],
        ["dental vs retroflex (t)", "\u0924 ta (teeth)", "\u091f \u1e6da (curled back)", "\u0924\u093e\u0932 t\u0101l (rhythm) / \u091f\u093e\u0932 \u1e6d\u0101l (postpone)"],
        ["short vs long vowel", "\u0907 i (short)", "\u0908 \u012b (long)", "\u0926\u093f\u0928 din (day) / \u0926\u0940\u0928 d\u012bn (poor)"],
        ["short vs long vowel", "\u0909 u (short)", "\u090a \u016b (long)", "\u092a\u0941\u0932 pul? (rare) / \u092a\u0942\u0932 p\u016bl? \u2014 use \u0938\u0941\u0928\u093e sun\u0101 vs \u0938\u0942\u0928\u093e?"],
    ]),
    "sections": [
        {"h": "Aspirated consonants: the puff of air", "body": [
            ("p", "Hold a hand in front of your mouth and say <b>pin</b>, then <b>spin</b>. The 'p' in pin has a puff of air; the one in spin does not. Hindi treats those two as different letters across k, c, t, p. English speakers usually produce the plain sound and lose the distinction \u2014 which changes words."),
        ]},
        {"h": "Retroflex: the tongue curls back", "body": [
            ("p", "For \u091f \u0920 \u0921 \u0922 \u0923 the tongue tip curls up and back to touch the roof of the mouth. For \u0924 \u0925 \u0926 \u0927 \u0928 it stays at the teeth, like the English 't' in 'ten'. English has no retroflex series, so every learner flattens them at first \u2014 \u0926\u093e\u0932 (lentils) and \u0921\u093e\u0932 (branch) must sound different."),
            ("note", "Why it matters", "\u092a\u093e\u0928\u0940 is water, but a retroflex-flavoured \u092a\u093e\u0923\u0940 is a completely different word. A small tongue movement changes what you said."),
        ]},
        {"h": "Vowel length is real", "body": [
            ("p", "Hindi distinguishes short and long vowels: \u0907/\u0908, \u0909/\u090a, and the short 'a' in \u0915\u092e (kam, less) versus the long in \u0915\u093e\u092e (k\u0101m, work). Lengthening or shortening a vowel can change the word, so do not borrow English's habit of stretching vowels for emphasis."),
        ]},
    ],
    "mistakes": [
        ["Saying 'kam' and 'khaam' interchangeably", "Keep क plain and ख aspirated", "The puff of air is the whole difference between two letters."],
        ["Flattening \u0921 into \u0926", "Curl the tongue back for \u0921", "English has no retroflex sounds, so this needs deliberate practice, not just listening."],
        ["Stretching short vowels for emphasis", "Keep \u0907/\u0909 short even when excited", "Vowel length is phonemic in Hindi; stretching it changes the word."],
    ],
    "practice": [
        "Say each minimal pair aloud, hand in front of your mouth for the aspirated sounds \u2014 you should feel the puff on the second word.",
        "Record yourself on your phone saying the six pairs; listen back the next day and spot the flattened ones.",
        "Practise the retroflex series \u091f \u0920 \u0921 \u0922 with your tongue curled back until it stops feeling strange.",
    ],
    "quiz": [
        {"q": "What is the difference between प and फ?", "a": "फ (pha) is aspirated \u2014 it carries a puff of air that प (pa) does not. पल means 'moment', फल means 'fruit'."},
        {"q": "Where does the tongue go for a retroflex consonant?", "a": "The tip curls up and back to the roof of the mouth \u2014 not at the teeth. That is what makes ड different from द."},
        {"q": "Is vowel length important in Hindi?", "a": "Yes \u2014 it is phonemic. कम (kam, less) and काम (kām, work) differ only in vowel length."},
    ],
    "tools": [("Pronunciation lab", "Minimal pairs with playback \u2014 a computer voice, not a native one.", "/learn/practice/pronunciation/")],
    "lessons": [("The Hindi Alphabet \u2014 full guide", "Where every sound sits in the script.", "/learn/hindi-alphabet-for-beginners/")],
    "material": [("Devanagari chart", "The letters this guide refers to.", "/materials/alphabet/devanagari-chart/")],
    "next": ("100 essential Hindi words", "/materials/vocabulary/100-essential-words/"),
})

M.append({
    "slug": "100-essential-words", "category": "vocabulary",
    "title": "100 Essential Hindi Words \u2014 Grouped to Memorise",
    "meta": "100 high-frequency Hindi words in ten groups of ten \u2014 greetings, pronouns, numbers, time, family, food, places, objects, verbs, adjectives \u2014 with Romanisation. Free.",
    "level": "Beginner",
    "purpose": "These are the words that do the most work in everyday Hindi \u2014 the hundred you should know cold before worrying about anything rarer. Grouped by meaning because memory likes categories.",
    "learn": ["100 core words, grouped so they are easier to remember", "The Romanisation and English for each", "Which groups to learn first (greetings, pronouns, food, places)", "A simple way to turn this list into recall"],
    "quickref": (["Group", "The ten words"], [
        ["Greetings & politeness", "<span class=\"dv\">\u0928\u092e\u0938\u094d\u0924\u0947 namaste (hello) \u00b7 \u0927\u0928\u094d\u092f\u0935\u093e\u0926 dhanyav\u0101d (thanks) \u00b7 \u0936\u0941\u0915\u094d\u0930\u093f\u092f\u093e shukriy\u0101 (thanks) \u00b7 \u0915\u0943\u092a\u092f\u093e kripay\u0101 (please) \u00b7 \u0939\u093e\u0901 h\u0101\u0303 (yes) \u00b7 \u0928\u0939\u0940\u0902 nah\u012b\u0303 (no) \u00b7 \u092e\u093e\u092b \u0915\u0940\u091c\u093f\u090f m\u0101f k\u012bjie (sorry) \u00b7 \u0920\u0940\u0915 \u0939\u0948 \u1e6dh\u012bk hai (okay) \u00b7 \u092b\u093f\u0930 \u092e\u093f\u0932\u0947\u0902\u0917\u0947 phir milenge (see you) \u00b7 \u0938\u094d\u0935\u093e\u0917\u0924 sv\u0101gat (welcome)</span>"],
        ["Pronouns", "<span class=\"dv\">\u092e\u0948\u0902 main (I) \u00b7 \u0906\u092a \u0101p (you, polite) \u00b7 \u0924\u0941\u092e tum (you, casual) \u00b7 \u0935\u0939 vah (he/she/that) \u00b7 \u092f\u0939 yah (this) \u00b7 \u0939\u092e ham (we) \u00b7 \u0935\u0947 ve (they/those) \u00b7 \u092e\u0947\u0930\u093e mer\u0101 (my) \u00b7 \u0906\u092a\u0915\u093e \u0101pk\u0101 (your) \u00b7 \u0915\u094c\u0928 kaun (who)</span>"],
        ["Numbers 1\u201310", "<span class=\"dv\">\u090f\u0915 ek (1) \u00b7 \u0926\u094b do (2) \u00b7 \u0924\u0940\u0928 t\u012bn (3) \u00b7 \u091a\u093e\u0930 ch\u0101r (4) \u00b7 \u092a\u093e\u0901\u091a p\u0101\u0303ch (5) \u00b7 \u091b\u0939 chhah (6) \u00b7 \u0938\u093e\u0924 s\u0101t (7) \u00b7 \u0906\u0920 \u0101\u1e6dh (8) \u00b7 \u0928\u094c nau (9) \u00b7 \u0926\u0938 das (10)</span>"],
        ["Time", "<span class=\"dv\">\u0906\u091c \u0101j (today) \u00b7 \u0915\u0932 kal (yesterday/tomorrow) \u00b7 \u0905\u092d\u0940 abh\u012b (now) \u00b7 \u092c\u093e\u0926 \u092e\u0947\u0902 b\u0101d me\u1e43 (later) \u00b7 \u0938\u0941\u092c\u0939 subah (morning) \u00b7 \u0936\u093e\u092e sh\u0101m (evening) \u00b7 \u0930\u093e\u0924 r\u0101t (night) \u00b7 \u0926\u093f\u0928 din (day) \u00b7 \u0938\u092e\u092f samay (time) \u00b7 \u0918\u0902\u091f\u093e ghan\u1e6d\u0101 (hour)</span>"],
        ["Family", "<span class=\"dv\">\u092e\u093e\u0901 m\u0101\u0303 (mother) \u00b7 \u092a\u093f\u0924\u093e pit\u0101 (father) \u00b7 \u092d\u093e\u0908 bh\u0101\u012b (brother) \u00b7 \u092c\u0939\u0928 bah\u012bn (sister) \u00b7 \u092c\u0947\u091f\u093e be\u1e6d\u0101 (son) \u00b7 \u092c\u0947\u091f\u0940 be\u1e6d\u012b (daughter) \u00b7 \u0926\u094b\u0938\u094d\u0924 dost (friend) \u00b7 \u092a\u0930\u093f\u0935\u093e\u0930 pariv\u0101r (family) \u00b7 \u092c\u091a\u094d\u091a\u093e bachch\u0101 (child) \u00b7 \u0938\u093e\u0925\u0940 s\u0101th\u012b (companion)</span>"],
        ["Food & drink", "<span class=\"dv\">\u0916\u093e\u0928\u093e kh\u0101n\u0101 (food) \u00b7 \u092a\u093e\u0928\u0940 p\u0101n\u012b (water) \u00b7 \u091a\u093e\u092f ch\u0101y (tea) \u00b7 \u0930\u094b\u091f\u0940 ro\u1e6d\u012b (flatbread) \u00b7 \u091a\u093e\u0935\u0932 ch\u0101val (rice) \u00b7 \u0926\u093e\u0932 d\u0101l (lentils) \u00b7 \u0926\u0942\u0927 d\u016bdh (milk) \u00b7 \u092b\u0932 phal (fruit) \u00b7 \u0938\u092c\u094d\u091c\u0940 sabz\u012b (vegetable) \u00b7 \u092e\u0940\u0920\u093e m\u012b\u1e6dh\u0101 (sweet)</span>"],
        ["Places", "<span class=\"dv\">\u0918\u0930 ghar (house) \u00b7 \u0938\u094d\u0915\u0942\u0932 sk\u016bl (school) \u00b7 \u0926\u0941\u0915\u093e\u0928 duk\u0101n (shop) \u00b7 \u092c\u093e\u091c\u093c\u093e\u0930 b\u0101z\u0101r (market) \u00b7 \u0930\u093e\u0938\u094d\u0924\u093e r\u0101st\u0101 (road) \u00b7 \u0936\u0939\u0930 shahar (city) \u00b7 \u0917\u093e\u0901\u0935 g\u0101\u0303v (village) \u00b7 \u0905\u0938\u094d\u092a\u0924\u093e\u0932 aspit\u0101l (hospital) \u00b7 \u0938\u094d\u091f\u0947\u0936\u0928 s\u1e6de\u015ban (station) \u00b7 \u0939\u094b\u091f\u0932 ho\u1e6dal (hotel)</span>"],
        ["Everyday objects", "<span class=\"dv\">\u0915\u093f\u0924\u093e\u092c kit\u0101b (book) \u00b7 \u0915\u0932\u092e kalam (pen) \u00b7 \u0926\u0930\u0935\u093e\u091c\u093c\u093e darv\u0101z\u0101 (door) \u00b7 \u0916\u093f\u0921\u093c\u0915\u0940 khi\u1e5bk\u012b (window) \u00b7 \u092e\u0947\u091c mez (table) \u00b7 \u0915\u0941\u0930\u094d\u0938\u0940 kurs\u012b (chair) \u00b7 \u092b\u093c\u094b\u0928 fon (phone) \u00b7 \u092a\u0948\u0938\u093e pais\u0101 (money) \u00b7 \u0915\u092a\u0921\u093c\u0947 kap\u1e5be (clothes) \u00b7 \u0918\u0921\u093c\u0940 gha\u1e5b\u012b (watch/clock)</span>"],
        ["Common verbs", "<span class=\"dv\">\u0939\u094b\u0928\u093e hon\u0101 (to be) \u00b7 \u0915\u0930\u0928\u093e karn\u0101 (to do) \u00b7 \u091c\u093e\u0928\u093e j\u0101n\u0101 (to go) \u00b7 \u0906\u0928\u093e \u0101n\u0101 (to come) \u00b7 \u0916\u093e\u0928\u093e kh\u0101n\u0101 (to eat) \u00b7 \u092a\u0940\u0928\u093e p\u012bn\u0101 (to drink) \u00b7 \u0926\u0947\u0916\u0928\u093e dekhn\u0101 (to see) \u00b7 \u092c\u094b\u0932\u0928\u093e boln\u0101 (to speak) \u00b7 \u0938\u0941\u0928\u0928\u093e sunn\u0101 (to hear) \u00b7 \u0938\u094b\u0928\u093e son\u0101 (to sleep)</span>"],
        ["Adjectives", "<span class=\"dv\">\u0905\u091a\u094d\u091b\u093e achchh\u0101 (good) \u00b7 \u092c\u0941\u0930\u093e bur\u0101 (bad) \u00b7 \u092c\u0921\u093c\u093e ba\u1e5b\u0101 (big) \u00b7 \u091b\u094b\u091f\u093e chho\u1e6d\u0101 (small) \u00b7 \u0928\u092f\u093e nay\u0101 (new) \u00b7 \u092a\u0941\u0930\u093e\u0928\u093e pur\u0101n\u0101 (old) \u00b7 \u0917\u0930\u092e garam (hot) \u00b7 \u0920\u0902\u0921\u093e \u1e6dhan\u1e0d\u0101 (cold) \u00b7 \u092e\u0939\u0901\u0917\u093e mah\u0101\u0303g\u0101 (expensive) \u00b7 \u0938\u0938\u094d\u0924\u093e sast\u0101 (cheap)</span>"],
    ]),
    "sections": [
        {"h": "How to actually memorise these", "body": [
            ("ol", [
                "Learn one group a day for ten days \u2014 do not try to swallow the list whole.",
                "Cover the English column and test yourself; the recall (not re-reading) is what builds the memory.",
                "Put each day's words into the daily practice drill so they come back on a schedule.",
            ]),
        ]},
    ],
    "mistakes": [
        ["Re-reading the list and calling it study", "Cover one column and recall", "Recognition is not recall \u2014 you must produce the word, not recognise it."],
        ["Ignoring gender", "Learn each noun with its gender", "Adjectives and verbs agree with the noun's gender, so a noun without its gender is half-learned."],
    ],
    "practice": [
        "Day one: learn the greetings group; put it into the vocabulary practice lab.",
        "Each day add one group and review the previous day's group from memory.",
        "After ten days, run the mixed daily practice to keep all ten groups warm.",
    ],
    "quiz": [
        {"q": "What does \u092a\u093e\u0928\u0940 mean?", "a": "Water \u2014 one of the first words you will use daily in India."},
        {"q": "Which group should you learn first and why?", "a": "Greetings and politeness \u2014 they are the words you need on arrival, and they give you a win on day one."},
        {"q": "Why learn each noun with its gender?", "a": "Because adjectives and verbs agree with the noun's gender \u2014 a noun without its gender is half-learned."},
    ],
    "tools": [("Vocabulary practice", "Drill these words until they are automatic.", "/learn/practice/vocabulary/"), ("Flashcards", "Flip-card review with optional audio.", "/toolbox/hindi-flashcards/")],
    "lessons": [("Hindi Numbers 1 to 100", "The full number system beyond the first ten.", "/learn/hindi-numbers-1-to-100/"), ("Hindi Family Words", "The family terms in depth, with the logic behind them.", "/learn/hindi-family-words/")],
    "material": [("25 essential verbs", "The verb forms behind the verbs column.", "/materials/verbs/essential-verbs/")],
    "next": ("25 essential Hindi verbs", "/materials/verbs/essential-verbs/"),
})

M.append({
    "slug": "beginner-grammar-reference", "category": "grammar",
    "title": "Beginner Grammar Reference \u2014 One Page",
    "meta": "One printable page of the Hindi grammar you need first: SOV word order, noun gender, plurals, the verb 'to be', postpositions and adjective agreement. Free.",
    "level": "Beginner",
    "purpose": "The whole skeleton of Hindi on a single page \u2014 the rules that explain almost everything you will say in your first months. Keep it printed; the deep explanations live in the guides this links to.",
    "learn": ["The Subject\u2013Object\u2013Verb order, with examples", "How to guess a noun's gender (and when you cannot)", "The three plural patterns", "The present tense of 'to be' and basic verb agreement", "How postpositions replace English prepositions"],
    "quickref": (["Rule", "Form", "Example"], [
        ["Word order", "Subject + Object + Verb", "\u092e\u0948\u0902 \u0915\u093f\u0924\u093e\u092c \u092a\u0922\u093c\u0924\u093e \u0939\u0942\u0901 (I book read = I read a book)"],
        ["Gender \u2014 masculine", "nouns in -\u0101 (\u0906)", "\u0932\u0921\u093c\u0915\u093e la\u1e5bk\u0101 (boy)"],
        ["Gender \u2014 feminine", "nouns in -\u012b (\u0908)", "\u0932\u0921\u093c\u0915\u0940 la\u1e5bk\u012b (girl)"],
        ["Plural \u2014 masc -\u0101", "-\u0101 \u2192 -e", "\u0932\u0921\u093c\u0915\u093e \u2192 \u0932\u0921\u093c\u0915\u0947 la\u1e5bke"],
        ["Plural \u2014 fem -\u012b", "-\u012b \u2192 -iy\u0101\u0303", "\u0932\u0921\u093c\u0915\u0940 \u2192 \u0932\u0921\u093c\u0915\u093f\u092f\u093e\u0901 la\u1e5bkiy\u0101\u0303"],
        ["'To be' present", "\u0939\u0942\u0901 / \u0939\u0948 / \u0939\u0948\u0902 / \u0939\u094b", "main h\u016b\u0303, vah hai, ve hai\u1e43, tum ho"],
        ["Postpositions", "after the noun, not before", "\u0918\u0930 \u092e\u0947\u0902 ghar me\u1e43 (in the house)"],
        ["Adjectives agree", "-\u0101 / -\u012b / -e", "\u0905\u091a\u094d\u091b\u093e \u0932\u0921\u093c\u0915\u093e, \u0905\u091a\u094d\u091b\u0940 \u0932\u0921\u093c\u0915\u0940"],
    ]),
    "sections": [
        {"h": "The verb goes last", "body": [
            ("p", "English says <b>I read a book</b>; Hindi says <b>I book read</b> \u2014 \u092e\u0948\u0902 \u0915\u093f\u0924\u093e\u092c \u092a\u0922\u093c\u0924\u093e \u0939\u0942\u0901. Almost every sentence you build is Subject, then Object, then Verb. Once this feels natural, the rest of the grammar slots into place around it."),
        ]},
        {"h": "Gender: the two endings that matter", "body": [
            ("p", "Most masculine nouns end in \u0906 (-\u0101): \u0932\u0921\u093c\u0915\u093e. Most feminine nouns end in \u0908 (-\u012b): \u0932\u0921\u093c\u0915\u0940. Words ending in a consonant are usually masculine, but there are common exceptions (\u0915\u093f\u0924\u093e\u092c, book, is feminine) \u2014 learn those as you meet them."),
        ]},
        {"h": "Postpositions come after", "body": [
            ("p", "Where English puts a word before the noun (in the house), Hindi puts a short word after it: \u0918\u0930 \u092e\u0947\u0902 (ghar me\u1e43, house-in). They are called postpositions for exactly that reason, and \u0915\u093e/\u0915\u0940/\u0915\u0947 (of) is the one that changes to agree with the noun it belongs to."),
        ]},
    ],
    "mistakes": [
        ["Copying English word order", "Put the verb last", "SOV is the frame; English SVO sentences sound wrong even when every word is right."],
        ["Guessing gender from meaning", "Learn gender from the ending, then the exceptions", "There is no logic to why \u0915\u093f\u0924\u093e\u092c is feminine \u2014 you just learn it."],
        ["Using 'of' as one word", "का / की / के agree with the following noun", "\u0932\u0921\u093c\u0915\u0947 \u0915\u0940 \u0915\u093f\u0924\u093e\u092c (the boy's book) \u2014 \u0915\u0940 because \u0915\u093f\u0924\u093e\u092c is feminine."],
    ],
    "practice": [
        "Write five sentences about your day in SOV order, then check each verb is last.",
        "Take ten nouns from the vocabulary list and write their plurals.",
        "Make each adjective agree: \u0905\u091a\u094d\u091b\u093e \u0918\u0930, \u0905\u091a\u094d\u091b\u0940 \u0915\u093f\u0924\u093e\u092c, \u0905\u091a\u094d\u091b\u0947 \u0932\u0921\u093c\u0915\u0947.",
    ],
    "quiz": [
        {"q": "Put in Hindi order: 'I drink water'.", "a": "\u092e\u0948\u0902 \u092a\u093e\u0928\u0940 \u092a\u0940\u0924\u093e \u0939\u0942\u0901 (main p\u0101n\u012b p\u012bt\u0101 h\u016b\u0303) \u2014 Subject, Object, Verb."},
        {"q": "What is the plural of \u0932\u0921\u093c\u0915\u093e?", "a": "\u0932\u0921\u093c\u0915\u0947 (la\u1e5bke) \u2014 masculine nouns in -\u0101 change to -e."},
        {"q": "Why is it 'ladke k\u012b kit\u0101b' and not 'ladke k\u0101 kit\u0101b'?", "a": "Because \u0915\u093e/\u0915\u0940/\u0915\u0947 agrees with the noun that follows \u2014 \u0915\u093f\u0924\u093e\u092c is feminine, so \u0915\u0940."},
    ],
    "tools": [("Grammar practice", "Gender, plurals and agreement drills.", "/learn/practice/grammar/")],
    "lessons": [("Hindi Word Order", "SOV explained with worked examples.", "/learn/hindi-sentence-structure/"), ("Hindi Gender", "The full rules and the patterns that let you guess.", "/learn/hindi-gender-masculine-feminine/")],
    "material": [("Postpositions", "The postposition table this page refers to.", "/materials/grammar/postpositions/")],
    "next": ("Postpositions \u2014 the small words that hold sentences together", "/materials/grammar/postpositions/"),
})

import sys
from materials_b import M_B
M += M_B
from materials_c import M_C
M += M_C

def main():
    mats = M
    hub = build_hub(mats)
    pages = [build_material(m) for m in mats]
    # write a manifest for admin + search indexing
    manifest = [{"slug": m["slug"], "category": m["category"], "title": m["title"],
                 "level": m["level"], "path": "/materials/%s/%s/" % (m["category"], m["slug"]),
                 "meta": m["meta"], "purpose": m["purpose"],
                 "lessons": len(m.get("lessons", [])), "tools": len(m.get("tools", [])),
                 "quiz": len(m.get("quiz", [])), "sections": len(m.get("sections", [])),
                 "hasPractice": bool(m.get("practice")), "hasMistakes": bool(m.get("mistakes")),
                 "hasQuickref": bool(m.get("quickref"))} for m in mats]
    with open(os.path.join(ROOT, "reports/materials-manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    # registry for the admin Materials Ops panel (same single source of truth)
    reg = ('/* GENERATED by tools/build-materials.py — do not edit.\n'
           '   Materials registry, consumed by the admin Learn Ops / Materials panel.\n'
           '   Single source of truth is tools/build-materials.py + materials_b/c. */\n'
           'window.EKGURU_MATERIALS = ' + json.dumps(manifest, ensure_ascii=False) + ';\n')
    with open(os.path.join(ROOT, "js/materials-registry.js"), "w", encoding="utf-8") as f:
        f.write(reg)
    print("built %d materials + hub + js/materials-registry.js" % len(mats))
    for p in pages:
        print("  ", os.path.relpath(p, ROOT))
    return 0

if __name__ == "__main__":
    sys.exit(main())

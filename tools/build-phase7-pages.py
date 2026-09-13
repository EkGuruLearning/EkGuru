#!/usr/bin/env python3
"""Phase 7 — build the global language hub + goal-based onboarding page.

Both pages read the SAME data files the learner uses (js/languages.js,
js/learning-paths.js) — so a new language becomes visible on the hub by
adding one registry row, never by editing HTML.

Generated (never hand-edit; rerun this tool):
  languages/index.html      — global language hub (indexable)
  languages/{code}/index.html — one page per BETA starter pack (indexable)
  start/index.html          — goal-based onboarding (indexable; deterministic, not AI)
"""
import json, os, re, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "https://ekguru.shop"
NOW = time.strftime("%Y-%m-%d", time.gmtime())

CORE_STYLE = """
.art{max-width:820px;margin:0 auto;padding:0 20px 60px}
.art h1{font-size:2rem;line-height:1.25;margin:26px 0 10px}
.art h2{font-size:1.28rem;margin:34px 0 12px;padding-top:6px}
.art p,.art li{line-height:1.75}
.crumb{font-size:.84rem;color:var(--muted);padding:18px 0 0}
.crumb a{color:var(--muted)}
.lede{color:var(--ink-2);font-size:1.05rem;line-height:1.7;margin:0 0 22px}
.note{background:var(--bg-soft);border:1px solid #ddd8ff;border-radius:12px;padding:14px 16px;margin:14px 0;font-size:.94rem;color:var(--ink-2)}
.btn{margin:6px 6px 6px 0}
.ob-row{margin:14px 0}
.ob-row label{display:block;font-weight:600;margin:0 0 6px}
.ob-row select,.ob-row input{width:100%;max-width:420px;padding:10px 12px;font-size:1rem;border:1px solid var(--line);border-radius:10px;background:var(--card,#fff);color:var(--ink)}
.ob-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:14px 0}
.ob-card{border:1px solid var(--line);border-radius:12px;padding:14px;display:flex;flex-direction:column;justify-content:space-between;gap:10px;background:var(--card,#fff)}
.lang-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin:14px 0}
.lang-cell{border:1px solid var(--line);border-radius:12px;padding:12px;background:var(--card,#fff)}
.lang-cell .nm{font-weight:700}
.lang-cell .sub{display:block;color:var(--muted);font-size:.82rem;margin-top:2px}
.tag{display:inline-block;border-radius:999px;padding:2px 10px;font-size:.72rem;font-weight:700;color:#fff}
.tag.on{background:#1a7f37}
.tag.soon{background:#7f8c8d}
.tag.beta{background:#9a6700}
.lp-box{border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin:26px 0;background:var(--card,#fff)}
.lp-box h2{font-size:1.15rem;margin:0 0 8px}
.lp-head{margin-bottom:14px}
.lp-head h3{font-size:1.05rem;margin:0 0 6px}
.lp-tag{display:inline-block;border-radius:999px;padding:2px 10px;font-size:.72rem;font-weight:700;color:#fff;vertical-align:2px}
.lp-tag.beta{background:#9a6700}
.v-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin:8px 0 16px}
.v-item{border:1px solid var(--line);border-radius:12px;padding:12px 13px;background:var(--bg-soft)}
.v-target{font-size:1.15rem;font-weight:600;margin:0}
.v-roman{color:var(--muted);font-size:.85rem;margin:2px 0 6px}
.v-meaning{margin:0;color:var(--ink-2);font-size:.92rem}
.g-concept{border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:12px 0;background:var(--bg-soft)}
.g-concept h3{margin:0 0 6px;font-size:1.02rem}
.g-pattern{margin:0 0 8px}
.g-meta{font-size:.8rem;color:var(--muted);margin:0 0 10px}
.g-ex,.g-exc,.g-mis{padding-left:20px;margin:6px 0}
.g-ex li,.g-exc li,.g-mis li{margin:4px 0;line-height:1.55}
.g-target{font-weight:600;font-size:1.02rem}
.g-roman{color:var(--muted);font-size:.86rem;margin:0 6px}
.g-gloss{color:var(--ink-2);font-size:.88rem}
.g-note{font-size:.92rem;color:var(--ink-2)}
.hi-review-add{margin-left:8px}
.hi-listen{display:inline-flex;align-items:center;gap:5px;margin:0 0 0 8px;padding:4px 10px;font-size:.82rem;line-height:1.4;border-radius:999px;border:1px solid var(--line);background:var(--bg-soft);color:var(--ink);cursor:pointer;vertical-align:middle}
.hi-listen.playing{background:var(--brand);border-color:var(--brand);color:#fff}
.sc-box{border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:10px 0;background:var(--bg-soft)}
.sc-word{font-size:1.5rem;font-weight:700;margin:4px 0}
.sc-count{font-size:.82rem;color:var(--muted);margin:0 0 4px}
.sc-opts{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}
.sc-opt:disabled{cursor:default;opacity:.92}
.sc-opt.sc-right{border-color:#1a7f37;color:#1a7f37;background:#e8f6ec}
.sc-opt.sc-wrong{border-color:#b42318;color:#b42318;background:#fdeceb}
.sc-fb{font-size:.95rem;min-height:1.4em;margin:8px 0}
.sc-nav{min-height:40px}
"""


def head(title, desc, url, up=""):
    return """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s | EkGuru</title>
<meta name="description" content="%s">
<meta name="author" content="EkGuru">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="%s/%s">
<meta property="og:type" content="article">
<meta property="og:title" content="%s | EkGuru">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s/%s">
<meta property="og:site_name" content="EkGuru">
<meta property="article:published_time" content="%s">
<link rel="stylesheet" href="%scss/style.min.css">
<style>%s</style>
</head>
<body>
<div class="art">
""" % (title, desc, BASE, url, title, desc, BASE, url, NOW, up, CORE_STYLE)


def foot(up="", scripts=()):
    s = ""
    for src in scripts:
        s += '\n<script src="%sjs/%s" defer></script>' % (up, src)
    return """
</div>
<footer class="pw-ftr">
  <nav aria-label="Site information">
    <a href="%s">Home</a>
    <a href="%sabout/">About</a>
    <a href="%scontact/">Contact</a>
    <a href="%sprivacy/">Privacy</a>
    <a href="%sterms/">Terms</a>
    <a href="%sdisclaimer/">Disclaimer</a>
  </nav>
  <p>© 2026 EkGuru — One Student. One Goal. One Guru.<br>
  Written and maintained by Prakash. Hindi lessons with native-speaking tutors, one to one.</p>
</footer>
<!-- ekguru:recovery:start -->
<script src="%sjs/recovery.js" defer></script>
<!-- ekguru:recovery:end -->
%s
<script defer>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("%ssw.js").catch(function () {});
  });
}
</script>
</body>
</html>
""" % (up, up, up, up, up, up, up, s, up)


STD_NOTE = ("BETA proof of engine reuse. Not PRODUCTION: Hindi is the only production language. "
            "This is starter reference content only — not a course.")


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def languages_page():
    # Phase 7C: read the 7C registry (BETA packs included); fall back to Phase 7
    try:
        langs = json.load(open("reports/language-registry-phase7c.json"))["languages"]
    except Exception:
        langs = json.load(open("reports/language-registry-phase7.json"))["languages"]
    prod = [l for l in langs if l["productionStatus"] == "PRODUCTION"]
    beta = sorted([l for l in langs if l["productionStatus"] == "BETA"], key=lambda x: x["name"])
    planned = [l for l in langs if l["productionStatus"] not in ("PRODUCTION", "BETA")]

    prod_cards = "".join(
        '<div class="lang-cell"><span class="nm">%s <span class="tag on">Available</span></span>' % esc(l["name"]) +
        '<span class="sub">%s · %s script · free</span>' % (esc(l["nativeName"]), esc(l["script"])) +
        '<p><a class="btn" href="/learn/hindi/">Start learning %s</a></p></div>' % esc(l["name"])
        for l in prod)

    beta_cells = "".join(
        '<a class="lang-cell" href="/languages/%s/">' % esc(l["id"]) +
        '<span class="nm">%s <span class="tag beta">Starter · beta</span></span>' % esc(l["name"]) +
        '<span class="sub">%s · %s script</span>' % (esc(l["nativeName"]), esc(l["script"])) +
        '<span class="sub">%d words · %d phrases · %d grammar — free</span>' % (
            (l.get("starterCounts") or {}).get("vocab", 0),
            (l.get("starterCounts") or {}).get("phrase", 0),
            (l.get("starterCounts") or {}).get("grammar", 0)) +
        '</a>'
        for l in beta)

    planned_cells = "".join(
        '<div class="lang-cell"><span class="nm">%s</span>' % esc(l["name"]) +
        '<span class="sub">%s · %s script</span>' % (esc(l["nativeName"]), esc(l["script"])) +
        '<span class="tag soon" style="margin-top:6px">Coming</span></div>'
        for l in planned)

    body = (
        '  <p class="crumb"><a href="/">EkGuru</a> › Languages</p>\n'
        '  <h1>Learn a language with EkGuru</h1>\n'
        '  <p class="lede">One platform, many languages — English → Hindi today, with more targets coming. '
        "We only list a language as available when real, reviewed content exists. No empty lessons, no placeholder courses.</p>\n"
        '  <h2>Available now</h2>\n'
        '  <div class="lang-grid">' + prod_cards + "</div>\n"
        '  <p class="muted" id="cg-stats">Counting live content…</p>\n'
        + (('  <h2>Beta starter</h2>\n'
            '  <p class="muted">A starter pack proves the engines work across languages. It is BETA reference content — '
            "not a course, and never labelled available until a full reviewed course exists.</p>\n"
            '  <div class="lang-grid">' + beta_cells + "</div>\n") if beta else "") +
        (('  <h2>Coming soon</h2>\n'
            '  <p class="muted">These are the next targets in the architecture. Each becomes available only when its lessons, audio and review content are real.</p>\n'
            '  <div class="lang-grid">' + planned_cells + "</div>\n") if planned else "") +
        '  <div class="note"><b>Not sure where to begin?</b> Answer three quick questions and get a rule-based starting point — <a href="/start/">find your starting point</a>. This is a deterministic recommendation, not AI.</div>\n'
        + (('  <div id="lp-proof" class="lp-box">\n'
            '    <h2>Engine reuse proof — starter packs</h2>\n'
            '    <p class="muted">Every starter pack below is rendered live by the <b>same</b> '
            "vocabulary, phrase and grammar engines that render Hindi — including the same device-only spaced-repetition "
            "“Add to review” hook. Pick a language to see it rendered. This is an architecture proof, not a course.</p>\n"
            '    <label class="ob-row" for="lp-select">Preview a starter pack\n'
            '      <select id="lp-select" style="width:100%;max-width:420px">'
            + "".join('<option value="%s"%s>%s</option>' % (esc(l["id"]), ' selected' if l["id"] == "es" else "", esc(l["name"])) for l in beta)
            + '</select></label>\n'
            '    <div id="langpack-app"><p class="muted">Loading Spanish starter pack…</p></div>\n'
            '  </div>\n') if beta else "") +
        '  <script defer>\n'
        '  (function(){\n'
        '    var el=document.getElementById("cg-stats");\n'
        '    if(!el){return;}\n'
        '    function whenReady(cb){\n'
        '      if(window.EkGuruContent){cb(window.EkGuruContent);return;}\n'
        '      var n=0,t=setInterval(function(){\n'
        '        if(window.EkGuruContent){clearInterval(t);cb(window.EkGuruContent);}\n'
        '        else if(++n>30){clearInterval(t);\n'
        '          el.textContent="Content inventory unavailable right now — the rest of this page works normally.";}\n'
        '      },100);\n'
        '    }\n'
        '    whenReady(function(C){\n'
        '      C.ready().then(function(){\n'
        '        var s=C.stats();\n'
        '        el.textContent="Live content inventory: "+s.total+" items — "\n'
        '          +s.byType.lesson+" lessons · "+s.byType.quiz+" quiz questions · "\n'
        '          +s.byType.phrase+" phrases · "+s.byType.review_card+" review cards. "\n'
        '          +"Counts are read from the content graph, not typed by hand.";\n'
        '      }).catch(function(){\n'
        '        el.textContent="Content inventory unavailable right now — the rest of this page works normally.";\n'
        '      });\n'
        '    });\n'
        + (('    // Stage 2/3: render a starter pack through the shared engines\n'
            '    var lp=document.getElementById("langpack-app");\n'
            '    var sel=document.getElementById("lp-select");\n'
            '    if(lp){\n'
            '      function lpReady(cb){\n'
            '        if(window.EkGuruLangPack && window.EkGuruVocab && window.EkGuruGrammar){cb();return;}\n'
            '        var n=0,t=setInterval(function(){\n'
            '          if(window.EkGuruLangPack && window.EkGuruVocab && window.EkGuruGrammar){clearInterval(t);cb();}\n'
            '          else if(++n>40){clearInterval(t);lp.innerHTML=\'<p class="muted">Language pack unavailable right now.</p>\';}\n'
            '        },100);\n'
            '      }\n'
            '      function show(code){\n'
            '        lp.innerHTML=\'<p class="muted">Loading starter pack…</p>\';\n'
            '        window.EkGuruLangPack.ready().then(function(){\n'
            '          window.EkGuruLangPack.render(lp, code);\n'
            '        }).catch(function(){lp.innerHTML=\'<p class="muted">Language pack unavailable right now.</p>\';});\n'
            '      }\n'
            '      lpReady(function(){ show(sel ? sel.value : "es"); });\n'
            '      if(sel){ sel.addEventListener("change", function(){ show(sel.value); }); }\n'
            '    }\n') if beta else "") +
        '  })();\n'
        '  </script>\n'
    )
    write("languages/index.html", "../", "Learn a language with EkGuru — available now and coming soon",
          "EkGuru teaches Hindi today, with more languages coming. See what is available now, and get a rule-based starting point for your goal.",
          "languages/", body, scripts=["content-graph.js", "vocab-phrase-engine.js", "grammar-engine.js",
                                       "hindi-srs.js", "language-pack.js"])




def _langpack_script(code):
    """Deterministic inline script: render one starter pack through the shared
    engines (vocab + phrases + grammar + SRS hook). No AI, no network beyond the
    pack JSON already in the repo."""
    return ('  <script defer>\n'
            '  (function(){\n'
            '    var el=document.getElementById("langpack-app");\n'
            '    if(!el){return;}\n'
            '    function ready(cb){\n'
            '      if(window.EkGuruLangPack && window.EkGuruVocab && window.EkGuruGrammar){cb();return;}\n'
            '      var n=0,t=setInterval(function(){\n'
            '        if(window.EkGuruLangPack && window.EkGuruVocab && window.EkGuruGrammar){clearInterval(t);cb();}\n'
            '        else if(++n>40){clearInterval(t);el.innerHTML=\'<p class="muted">Language pack unavailable right now.</p>\';}\n'
            '      },100);\n'
            '    }\n'
            '    ready(function(){\n'
            '      window.EkGuruLangPack.ready().then(function(){\n'
            '        window.EkGuruLangPack.render(el, "%s");\n'
            '      }).catch(function(){el.innerHTML=\'<p class="muted">Language pack unavailable right now.</p>\';});\n'
            '    });\n'
            '  })();\n'
            '  </script>\n') % esc(code)


def _startercheck_script(code):
    return ('  <script defer>\n'
            '  (function(){\n'
            '    var el=document.getElementById("starter-check");\n'
            '    if(!el){return;}\n'
            '    function ready(cb){\n'
            '      if(window.EkGuruStarter){cb();return;}\n'
            '      var n=0,t=setInterval(function(){\n'
            '        if(window.EkGuruStarter){clearInterval(t);cb();}\n'
            '        else if(++n>40){clearInterval(t);el.innerHTML=\'<p class="muted">Starter check unavailable right now.</p>\';}\n'
            '      },100);\n'
            '    }\n'
            '    ready(function(){ window.EkGuruStarter.renderCheck(el, "%s"); });\n'
            '  })();\n'
            '  </script>\n') % esc(code)


def lang_pages():
    """One indexable page per BETA starter pack, authored and honest.
    Only languages with an authored pack get a page — PLANNED languages stay
    on the hub (no thin pages generated for zero content)."""
    try:
        packs = json.load(open("data/language-packs.json", encoding="utf-8"))["packs"]
    except Exception:
        packs = []
    try:
        langs = json.load(open("reports/language-registry-phase7c.json", encoding="utf-8"))["languages"]
    except Exception:
        langs = []
    by_id = {l["id"]: l for l in langs}
    made = 0
    for p in packs:
        code = p["lang"]
        l = by_id.get(code)
        if not l or l["productionStatus"] != "BETA":
            continue
        try:
            d = json.load(open(p["file"], encoding="utf-8"))
        except Exception:
            d = {}
        name = esc(p["name"])
        about = esc(d.get("about", "") or p.get("honestNote", ""))
        title = "Learn %s basics — free starter pack" % p["name"]
        body = (
            '  <p class="crumb"><a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › %s</p>\n'
            '  <h1>Learn %s basics</h1>\n'
            '  <p class="lede"><span class="tag beta" style="vertical-align:2px">BETA — starter</span> '
            'Starter reference content, not a course.</p>\n'
            '  <div class="note"><b>Honest status.</b> %s</div>\n'
            '  <p>%s</p>\n'
            '  <h2>Starter pack preview</h2>\n'
            '  <p class="muted">%d words · %d phrases · %d grammar concepts — rendered live by the same '
            'engines that render Hindi, with the same device-only “Add to review” hook. The 🔊 Listen '
            'button is your browser’s computer voice, not a native recording.</p>\n'
            '  <div class="lp-box"><div id="langpack-app"><p class="muted">Loading %s starter pack…</p></div></div>\n'
            '  <h2>Starter check</h2>\n'
            '  <p class="muted">A fixed rule-based check over this pack’s words — the same questions every '
            'time. Not an exam, not AI, nothing is saved.</p>\n'
            '  <div id="starter-check"><p class="muted">Loading starter check…</p></div>\n'
            '  <div class="note"><b>This is not a full course.</b> There are no lesson pages and no recorded '
            'audio here. When real lessons exist for a language, it moves up — for now the only full course '
            'is <a href="/learn/hindi/">Hindi</a>.</div>\n'
            '  <p><a class="btn" href="/languages/">All languages</a> '
            '<a class="btn" href="/learn/hindi/">Start learning Hindi</a></p>\n'
        ) % (name, name, esc(d.get("honestNote", "") or STD_NOTE), about,
             (p.get("counts") or {}).get("vocab", 0),
             (p.get("counts") or {}).get("phrase", 0),
             (p.get("counts") or {}).get("grammar", 0), name) + _langpack_script(code) + _startercheck_script(code)
        write("languages/%s/index.html" % code, "../../", title, d.get("about", ""),
              "languages/%s/" % code, body,
              scripts=["vocab-phrase-engine.js", "grammar-engine.js", "hindi-srs.js",
                       "language-pack.js", "hindi-audio.js", "starter-practice.js"])
        made += 1
    return made


def start_page():
    body = (
        '  <p class="crumb"><a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › Start</p>\n'
        '  <h1>Find your starting point</h1>\n'
        '  <div id="onboarding-app"></div>\n'
        '  <div class="note" style="margin-top:18px"><b>Private by design.</b> Nothing you pick here is saved or uploaded. '
        "The suggestion comes from simple rules — your goal, level, time and reading preference — not from AI or a profile.</div>\n"
    )
    write("start/index.html", "../", "Find your starting point — a rule-based plan",
          "Answer three quick questions and get a rule-based starting point for learning Hindi — which path, which lesson, which practice. Deterministic, private, free.",
          "start/", body, scripts=["languages.js", "learning-paths.js", "onboarding.js"])


def write(path, up, title, desc, url, body, scripts=()):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    html = head(title, desc, url, up) + body + foot(up, scripts)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def patch_home():
    """Deterministic, idempotent injection into the hand-maintained home page:
    a nav link, a 'Languages' section and a global-nav entry — so every language
    is reachable from the home page. Guarded by markers; re-running never
    duplicates. Reads the same registry as the hub (single source of truth)."""
    path = "index.html"
    html = open(path, encoding="utf-8").read()
    orig = html
    try:
        langs = json.load(open("reports/language-registry-phase7c.json", encoding="utf-8"))["languages"]
    except Exception:
        langs = []
    prod = [l for l in langs if l["productionStatus"] == "PRODUCTION"]
    beta = sorted([l for l in langs if l["productionStatus"] == "BETA"], key=lambda x: x["name"])
    planned = [l for l in langs if l["productionStatus"] not in ("PRODUCTION", "BETA")]
    changed = False

    # 1) nav link (before the Book-a-trial CTA)
    if 'data-navlink="languages/index.html"' not in html:
        html = html.replace(
            '<a class="btn btn-primary btn-sm" data-navlink="find-tutors.html" data-i18n="nav.cta" href="find-tutors.html">Book a trial</a>',
            '<a data-navlink="languages/index.html" href="languages/index.html">Languages</a>\n'
            '      <a class="btn btn-primary btn-sm" data-navlink="find-tutors.html" data-i18n="nav.cta" href="find-tutors.html">Book a trial</a>',
            1)
        changed = True

    # 2) Languages section (before the "Why EkGuru" section)
    pills = "".join(
        '<a class="lang-pill on" href="/learn/hindi/">%s <small>full course</small></a>' % esc(l["name"])
        for l in prod)
    pills += "".join(
        '<a class="lang-pill beta" href="/languages/%s/">%s</a>' % (esc(l["id"]), esc(l["name"]))
        for l in beta)
    pills += ('<a class="lang-pill soon" href="/languages/">+ %d more coming</a>' % len(planned)) if planned else ""
    names = ", ".join(l["name"] for l in beta[:4]) + (", …" if len(beta) > 4 else "")
    section = (
        '<!-- ekguru:languages-home:start (generated by tools/build-phase7-pages.py) -->\n'
        '<section class="sec" id="languages">\n'
        '  <div class="wrap">\n'
        '    <div class="sec-head reveal">\n'
        '      <span class="kicker">Free language packs</span>\n'
        '      <h2>One engine, many languages</h2>\n'
        '      <p class="lead">Hindi is our full course. Free starter packs — %s — run on the same '
        'engines with the same device-only review. Beta reference content, not full courses.</p>\n'
        '    </div>\n'
        '    <div class="lang-strip reveal center">%s</div>\n'
        '    <p class="center" style="margin-top:18px"><a class="btn btn-ghost btn-sm" href="/languages/">See all languages</a></p>\n'
        '  </div>\n'
        '</section>\n'
        '<style>\n'
        '.lang-strip{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:6px}\n'
        '.lang-pill{display:inline-flex;align-items:center;gap:7px;padding:10px 16px;border-radius:999px;font-weight:700;font-size:.92rem;border:1px solid var(--line);background:var(--card,#fff);color:var(--ink)}\n'
        '.lang-pill small{font-weight:600;color:var(--muted);font-size:.75rem}\n'
        '.lang-pill.on{border-color:#1a7f37;color:#1a7f37}\n'
        '.lang-pill.beta{border-color:#9a6700;color:#9a6700}\n'
        '.lang-pill.soon{border-color:var(--line);color:var(--muted)}\n'
        '@media(pointer:coarse){.lang-pill{min-height:44px}}\n'
        '</style>\n'
        '<!-- ekguru:languages-home:end -->\n'
    ) % (names, pills)
    if "ekguru:languages-home:start" in html:
        i = html.index("<!-- ekguru:languages-home:start")
        j = html.index("<!-- ekguru:languages-home:end -->") + len("<!-- ekguru:languages-home:end -->")
        html = html[:i] + section.rstrip("\n") + html[j:]
        changed = True
    else:
        anchor = ('</section>\n\n<section class="sec">\n  <div class="wrap">\n'
                  '    <div class="sec-head reveal">\n'
                  '      <span class="kicker" data-i18n="why.kicker">Why EkGuru</span>')
        if anchor in html:
            html = html.replace(anchor, '</section>\n\n' + section + '\n<section class="sec">\n  <div class="wrap">\n'
                                '    <div class="sec-head reveal">\n'
                                '      <span class="kicker" data-i18n="why.kicker">Why EkGuru</span>', 1)
            changed = True

    # 3) global-nav entry
    if 'href="languages/"' not in html.split('ekguru:global-nav:start')[1].split('ekguru:global-nav:end')[0]:
        html = html.replace(
            '<ul class="eg-gn-list">',
            '<ul class="eg-gn-list">\n'
            '    <li><a href="languages/"><b>Learn other languages</b><span>Free starter packs — '
            'Bengali, Tamil, Telugu, Marathi, Gujarati, Punjabi, Urdu, Spanish and English basics. '
            'One engine, many languages.</span></a></li>', 1)
        changed = True

    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("patched: index.html (languages nav + section + global-nav)")
    else:
        print("home already has the languages section (no change)")


def main():
    languages_page()
    n = lang_pages()
    start_page()
    patch_home()
    print("generated: languages/index.html, %d language pages, start/index.html, home synced" % n)


if __name__ == "__main__":
    main()

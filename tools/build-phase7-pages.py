#!/usr/bin/env python3
"""Phase 7 — build the global language hub + goal-based onboarding page.

Both pages read the SAME data files the learner uses (js/languages.js,
js/learning-paths.js) — so a new language becomes visible on the hub by
adding one registry row, never by editing HTML.

Generated (never hand-edit; rerun this tool):
  languages/index.html   — global language hub (indexable)
  start/index.html       — goal-based onboarding (indexable; deterministic, not AI)
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


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def languages_page():
    # Phase 7C: read the 7C registry (BETA packs included); fall back to Phase 7
    try:
        langs = json.load(open("reports/language-registry-phase7c.json"))["languages"]
    except Exception:
        langs = json.load(open("reports/language-registry-phase7.json"))["languages"]
    prod = [l for l in langs if l["productionStatus"] == "PRODUCTION"]
    beta = [l for l in langs if l["productionStatus"] == "BETA"]
    planned = [l for l in langs if l["productionStatus"] not in ("PRODUCTION", "BETA")]

    prod_cards = "".join(
        '<div class="lang-cell"><span class="nm">%s <span class="tag on">Available</span></span>' % esc(l["name"]) +
        '<span class="sub">%s · %s script · free</span>' % (esc(l["nativeName"]), esc(l["script"])) +
        '<p><a class="btn" href="/learn/hindi/">Start learning %s</a></p></div>' % esc(l["name"])
        for l in prod)

    beta_cells = "".join(
        '<div class="lang-cell"><span class="nm">%s <span class="tag beta">Starter · beta</span></span>' % esc(l["name"]) +
        '<span class="sub">%s · %s script</span>' % (esc(l["nativeName"]), esc(l["script"])) +
        '<p class="muted" style="margin:6px 0 0;font-size:.8rem">Starter reference content only — not a course. See the proof below.</p></div>'
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
        '  <h2>Coming soon</h2>\n'
        '  <p class="muted">These are the next targets in the architecture. Each becomes available only when its lessons, audio and review content are real.</p>\n'
        '  <div class="lang-grid">' + planned_cells + "</div>\n"
        '  <div class="note"><b>Not sure where to begin?</b> Answer three quick questions and get a rule-based starting point — <a href="/start/">find your starting point</a>. This is a deterministic recommendation, not AI.</div>\n'
        + (('  <div id="es-proof" class="lp-box">\n'
            '    <h2>Engine reuse proof — Spanish starter pack</h2>\n'
            '    <p class="muted">Below is a small authored Spanish starter pack rendered live by the <b>same</b> '
            "vocabulary, phrase and grammar engines that render Hindi — including the same device-only spaced-repetition "
            "“Add to review” hook. This is the Stage 2 architecture proof, not a Spanish course.</p>\n"
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
        + (('    // Stage 2: render the Spanish starter pack through the shared engines\n'
            '    var lp=document.getElementById("langpack-app");\n'
            '    if(lp){\n'
            '      function lpReady(cb){\n'
            '        if(window.EkGuruLangPack && window.EkGuruVocab && window.EkGuruGrammar){cb();return;}\n'
            '        var n=0,t=setInterval(function(){\n'
            '          if(window.EkGuruLangPack && window.EkGuruVocab && window.EkGuruGrammar){clearInterval(t);cb();}\n'
            '          else if(++n>40){clearInterval(t);lp.innerHTML=\'<p class="muted">Language pack unavailable right now.</p>\';}\n'
            '        },100);\n'
            '      }\n'
            '      lpReady(function(){\n'
            '        window.EkGuruLangPack.ready().then(function(){\n'
            '          window.EkGuruLangPack.render(lp, "es");\n'
            '        }).catch(function(){lp.innerHTML=\'<p class="muted">Language pack unavailable right now.</p>\';});\n'
            '      });\n'
            '    }\n') if beta else "") +
        '  })();\n'
        '  </script>\n'
    )
    write("languages/index.html", "../", "Learn a language with EkGuru — available now and coming soon",
          "EkGuru teaches Hindi today, with more languages coming. See what is available now, and get a rule-based starting point for your goal.",
          "languages/", body, scripts=["content-graph.js", "vocab-phrase-engine.js", "grammar-engine.js",
                                       "hindi-srs.js", "language-pack.js"])




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


def main():
    languages_page()
    start_page()
    print("generated: languages/index.html, start/index.html")


if __name__ == "__main__":
    main()

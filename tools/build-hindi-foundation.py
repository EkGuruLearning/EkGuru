#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EkGuru — build the Hindi Foundation section (हिंदी की नींव).

Eighteen lessons in the order every Indian class-1 primer uses:
  स्वर → व्यंजन → बिना मात्रा के शब्द → one मात्रा per lesson → अं/अः/ँ → ऋ →
  आधे अक्षर → पहली कहानी.

Output (never hand-edit; rerun this tool):
  learn/hindi/foundation/index.html          the hub, with per-lesson progress
  learn/hindi/foundation/<slug>/index.html   one page per lesson

Content lives in tools/hindi-foundation-content.py. The builder REFUSES to write
if a word list breaks the primer rule — every word in lesson N uses only the signs
taught in lessons ≤ N — so a slip in the data cannot reach the site.

New pages are noindex: the indexing contract (tools/ultra/contract.py) freezes the
owner's index decisions and new pages need an explicit approval entry.

Run:  python3 tools/build-hindi-foundation.py            # build
      python3 tools/build-hindi-foundation.py --check    # validate only
"""
import html as H
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

C = _load("hindi_foundation_content", os.path.join(ROOT, "tools", "hindi-foundation-content.py"))
P = _load("build_hindi_pages", os.path.join(ROOT, "tools", "build-hindi-pages.py"))
D = _load("foundation_depth", os.path.join(ROOT, "tools", "build-hindi-foundation-depth.py"))
R = _load("textbook_reader", os.path.join(ROOT, "tools", "build-hindi-textbook-reader.py"))
DEPTH_CHAPTERS = {chapter['slug']: chapter for chapter in D.content()['chapters']}

BASE = "https://ekguru.shop"
SECTION = "learn/hindi/foundation"
UP_HUB = "../../../"          # learn/hindi/foundation/ → root
UP_LESSON = "../../../../"    # learn/hindi/foundation/<slug>/ → root
ACCENT, TINT = "#b45309", "#fff7ed"
STORE_KEY = "ekguru.foundation"

MATRA = C.MATRA
ALL_SIGNS = set(MATRA.values())
NUKTA = "\u093c"
INDEPENDENT_VOWELS = set("अआइईउऊऋएऐओऔ")
SIGHT = {w for w, _, _ in C.SIGHT_WORDS}
# Words the sentences may use before their sign is taught, beyond the sight list.
# Kept deliberately tiny: these are the Hindi 'to be' forms a reader meets in
# every second sentence. Everything else must obey the ladder.
SIGHT_EXTRA = {"था", "थी", "थे", "हूँ", "हो", "एक"}


# ------------------------------------------------------------------ validate
def signs_in(word):
    return {ch for ch in word if ch in ALL_SIGNS}

def allowed_set(lesson):
    return {MATRA[k] for k in lesson.get("allow", set())}

def check_word(word, allowed):
    """Return a list of problems for one word under the lesson's allowed signs."""
    bad = []
    extra = signs_in(word) - allowed
    if extra:
        bad.append("uses " + " ".join(sorted(extra)))
    for i, ch in enumerate(word):
        if ch == NUKTA and word[i - 1] not in "डढ":
            bad.append("nukta on " + word[i - 1])
    return bad

def validate():
    problems = []
    for L in C.LESSONS:
        if L["kind"] == "letters":
            continue
        allowed = allowed_set(L)
        for title, words in L.get("groups", []):
            for dev, rom, en in words:
                for b in check_word(dev, allowed):
                    problems.append("lesson %d word %s: %s" % (L["n"], dev, b))
        def sentence(dev, where):
            for tok in re.split(r"[\s,।?!—\-–]+", dev):
                tok = tok.strip("।?!,.")
                if not tok or tok in SIGHT or tok in SIGHT_EXTRA:
                    continue
                for b in check_word(tok, allowed):
                    problems.append("lesson %d %s '%s' word %s: %s" % (L["n"], where, dev, tok, b))
        for dev, rom, en in L.get("sentences", []):
            sentence(dev, "sentence")
        if L.get("passage"):
            for dev, rom, en in L["passage"][1]:
                sentence(dev, "passage")
        for story in L.get("stories", []):
            for dev, rom, en in story[3]:
                sentence(dev, "story")
    # slugs unique, numbers consecutive
    slugs = [L["slug"] for L in C.LESSONS]
    if len(set(slugs)) != len(slugs):
        problems.append("duplicate slug")
    if [L["n"] for L in C.LESSONS] != list(range(1, len(C.LESSONS) + 1)):
        problems.append("lesson numbers not consecutive")
    return problems


# ------------------------------------------------------------------ helpers
def e(s):
    return H.escape(str(s), quote=True)

def say(dev, label="🔊"):
    """A native speaker button (tests/regression/test-voice-page-coverage.py: every voice
    control must be a <button>, never a span that speaks itself)."""
    return '<button class="spk" type="button" data-sb-say="%s" aria-label="Play %s">%s</button>' % (e(dev), e(dev), label)

def voiced(dev, tag="span", cls="", extra=""):
    """Devanagari text followed by its own speaker button."""
    c = (' class="%s"' % cls) if cls else ""
    return '<%s%s lang="hi"%s>%s</%s> %s' % (tag, c, extra, e(dev), tag, say(dev))

SPK_SPAN = re.compile(r'<span class="spk" lang="hi">([^<]*)</span>')

def fix_inline(html_text):
    """Authored notes write <span class="spk" lang="hi">X</span>; render as text + button."""
    return SPK_SPAN.sub(lambda m: '<b lang="hi">%s</b> %s' % (m.group(1), say(H.unescape(m.group(1)))), html_text)

def chapter_band(up):
    return ('<div class="sb-chapter" style="--sb-accent:%s;--sb-tint:%s">'
            '<span aria-hidden="true" class="sb-ch-mascot">📖</span>'
            '<span class="sb-ch-name">Hindi Foundation <i>हिंदी की नींव</i></span>'
            '<span class="sb-ch-kind">Primer</span>'
            '<span aria-hidden="true" class="sb-ch-floats">क</span></div>\n') % (ACCENT, TINT)

STYLE = """
.fd-sub{color:var(--muted);font-size:1.02rem;margin:-4px 0 18px}
.fd-sign{display:grid;grid-template-columns:repeat(auto-fit,minmax(90px,1fr));gap:10px;align-items:center;text-align:center;margin:18px 0;padding:16px;border:1px solid var(--line);border-radius:16px;background:var(--bg-soft)}
.fd-sign b{display:block;font-size:2.6rem;line-height:1.1;font-weight:700}
.fd-sign small{display:block;color:var(--muted);font-size:.84rem;margin-top:4px}
.fd-sign .op{font-size:1.6rem;color:var(--muted)}
.fd-letters{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin:18px 0}
.fd-letter{border:1px solid var(--line);border-radius:16px;padding:14px 12px 12px;background:var(--bg,#fff);text-align:center}
.fd-letter .lt{display:block;font-size:2.8rem;line-height:1.1;font-weight:700}
.fd-letter .rm{display:block;color:var(--muted);font-size:.86rem;margin:2px 0 8px}
.fd-letter .kw{display:block;font-size:1.25rem;line-height:1.3}
.fd-letter .kw i{font-style:normal;font-size:1.5rem;display:block}
.fd-letter .fd-picture{display:block;width:min(100%%,180px);height:auto;aspect-ratio:4/3;object-fit:contain;margin:4px auto 9px;border-radius:10px}
.fd-air-demo{margin:18px 0;padding:14px;border:1px solid var(--line);border-radius:12px;background:var(--bg,#fff)}
.fd-air-demo summary{cursor:pointer;font-weight:600}
.fd-air-demo svg{display:block;width:min(100%%,480px);height:auto;margin:10px auto}
.fd-air-demo .air{transform-box:fill-box;transform-origin:center;opacity:.75}
.fd-air-demo[open] .air{animation:fd-air-puff 1.5s ease-out 2}
.fd-air-demo[open] .air.strong{animation-delay:.2s}
@keyframes fd-air-puff{0%%{transform:translateX(-12px) scale(.6);opacity:.2}60%%{opacity:1}100%%{transform:translateX(18px) scale(1.08);opacity:.75}}
@media(prefers-reduced-motion:reduce){.fd-air-demo[open] .air{animation:none}}
/* Trace glyphs need the locally supplied font even without a system Hindi font. */
main:has(>.htr-nav) .trace-cell text{font-family:TextbookDevanagari,system-ui,sans-serif}
@media print{
  .fd-letter .fd-picture{width:95px}
  .fd-air-demo .air{animation:none!important}
  /* Avoid splitting character cards between pages and expose all trace models,
     including those not yet scrolled into view in the interactive lesson. */
  .fd-letter,.trace-cell{break-inside:avoid;page-break-inside:avoid}
  html.sb-js .trace-cell{opacity:1!important;transform:none!important}
  /* Book-mode activities need input or audio; a frozen round is not a worksheet. */
  .art .bk-ex{display:none!important}
}
.fd-letter .en{display:block;color:var(--ink-2);font-size:.82rem;margin-top:2px}
.fd-letter .hint{display:block;color:var(--muted);font-size:.78rem;margin-top:6px;line-height:1.35}
.fd-letter .spk{margin-top:8px;font-size:.84rem}
.fd-lines{list-style:none;padding:0;margin:14px 0}
.fd-lines li{padding:12px 14px;border:1px solid var(--line);border-radius:12px;margin:8px 0;background:var(--bg,#fff)}
.fd-lines .dv{font-size:1.45rem;line-height:1.5;display:block}
.fd-lines .rm{color:var(--muted);font-size:.9rem;display:block}
.fd-lines details{margin-top:4px;font-size:.9rem}
.fd-lines summary{cursor:pointer;color:var(--muted)}
.fd-passage{border-left:5px solid %(accent)s;background:%(tint)s;border-radius:12px;padding:14px 18px;margin:18px 0}
.fd-passage h3{margin:0 0 8px;font-size:1.3rem}
.fd-task{border:1px solid #f0dfae;border-left:5px solid #f59e0b;background:#fff8e6;border-radius:12px;padding:14px 16px;margin:18px 0}
.fd-sight{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}
.fd-sight span{border:1px solid var(--line);border-radius:999px;padding:6px 12px;background:var(--bg,#fff)}
.fd-sight span b{font-size:1.2rem;margin-right:6px}
.fd-ladder{list-style:none;padding:0;margin:14px 0;counter-reset:fd}
.fd-ladder li{display:grid;grid-template-columns:44px 1fr auto;gap:12px;align-items:center;padding:12px 14px;border:1px solid var(--line);border-radius:12px;margin:8px 0;background:var(--bg,#fff)}
.fd-ladder li .num{font-weight:700;color:%(accent)s;font-size:1.2rem}
.fd-ladder li a{font-weight:600}
.fd-ladder li .hi{display:block;color:var(--muted);font-size:.9rem}
.fd-ladder li.done{background:#f0fdf4;border-color:#86efac}
.fd-ladder li.done .num::after{content:" ✓"}
.fd-phase{margin:26px 0 6px;font-size:1.05rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.vcard .vface .lt{font-size:1.7rem}
.vcards{grid-template-columns:repeat(auto-fill,minmax(140px,1fr))}
@media (max-width:520px){.fd-sign b{font-size:2.1rem}.fd-letter .lt{font-size:2.3rem}}
""" % {"accent": ACCENT, "tint": TINT}


# Original picture-word illustrations; match both character and keyword.
# Future changed or unmapped keywords retain the existing fallback until illustrated.
_PICTURE_FILE = os.path.join(ROOT, "data", "learning", "hindi-textbook-illustrations.json")
with open(_PICTURE_FILE, encoding="utf-8") as _picture_file:
    _PICTURES = {(r["character"], r["word"]): r["path"] for r in json.load(_picture_file)}

def letter_illustration(lt, kw, emo):
    asset = _PICTURES.get((lt, kw))
    if not asset:
        return '<i aria-hidden="true">%s</i>' % e(emo)
    return '<img class="fd-picture" src="/%s" width="240" height="180" alt="चित्र: %s" loading="lazy" decoding="async">' % (e(asset), e(kw))


def vcard(dev, rom, en, mt=""):
    return ('<div aria-label="%s" class="vcard wide"><div class="in">'
            '<div class="vface"><span class="lt">%s</span><span class="sd">%s · tap me</span></div>'
            '<div class="vface back"><span class="en">%s</span>%s'
            '<button class="spk" type="button" data-sb-say="%s">🔊 hear it</button></div></div></div>'
            ) % (e(dev), e(dev), e(rom), e(en), ('<span class="mt">%s</span>' % e(mt)) if mt else "", e(dev))

def lines_block(items, cls="fd-lines"):
    out = ['<ul class="%s">' % cls]
    for dev, rom, en in items:
        out.append('<li><span class="dv" lang="hi">%s %s</span><span class="rm">%s</span>'
                   '<details><summary>English</summary>%s</details></li>' % (e(dev), say(dev), e(rom), e(en)))
    out.append("</ul>")
    return "\n".join(out)

def quiz_block(qs):
    out = ['<section aria-label="Quick check" class="quiz" style="background:var(--bg-soft);border:1px solid #ddd8ff;border-radius:14px;padding:16px 18px;margin:30px 0">'
           '<h2 style="margin:0 0 12px;font-size:1.15rem">Quick check</h2>']
    for q, a in qs:
        out.append('<details style="margin:10px 0;border:1px solid var(--line);border-radius:10px;padding:12px 14px">'
                   '<summary style="cursor:pointer;font-weight:600;color:var(--ink)">%s</summary>'
                   '<p style="margin:10px 0 0;color:var(--ink-2)">%s</p></details>' % (e(q), e(a)))
    out.append("</section>")
    return "\n".join(out)

def progress_script(n, total):
    return """
<script defer>
(function(){
  var N=%d,T=%d,K=%s;
  function get(){try{return JSON.parse(localStorage.getItem(K)||"[]")}catch(e){return []}}
  function set(a){try{localStorage.setItem(K,JSON.stringify(a))}catch(e){}}
  var btn=document.getElementById("fd-mark"),pr=document.getElementById("fd-prog");
  if(!btn)return;
  function paint(){var d=get(),done=d.indexOf(N)>-1;
    btn.textContent=done?"Lesson "+N+" done — tap to undo":"Mark lesson "+N+" complete";
    btn.setAttribute("aria-pressed",done?"true":"false");
    if(pr)pr.textContent=d.length+" of "+T+" lessons done";}
  btn.addEventListener("click",function(){var d=get(),i=d.indexOf(N);if(i>-1)d.splice(i,1);else d.push(N);set(d);paint();
    try{if(window.goatcounter)window.goatcounter.count({path:"event/foundation_"+N,event:true});}catch(e){}});
  paint();
})();
</script>
""" % (n, total, json.dumps(STORE_KEY))


CSS_PATH = "css/foundation.css"

def head(title, desc, url, up):
    """The shared pre-shell head, with the section stylesheet LINKED (not inlined:
    tests/regression/test-page-layer.mjs caps pages that carry their own <style> rules)."""
    h = P.head(title, desc, url, up, index=False)
    h = h.replace('<html lang="en" dir="ltr" data-ad-class="HIGH">',
                  '<html lang="en" dir="ltr" data-learning-language="hi" data-ad-class="HIGH_CONTENT">')
    h = h.replace('<link rel="stylesheet" href="%scss/storybook.css">' % up,
                  '<link rel="stylesheet" href="%scss/storybook.css">\n<link rel="stylesheet" href="%s%s">'
                  '\n<link rel="stylesheet" href="%scss/book-mode.css">' % (up, up, CSS_PATH, up))
    return h

def write_css():
    with open(CSS_PATH, "w", encoding="utf-8") as f:
        f.write("/* EkGuru — Hindi Foundation (learn/hindi/foundation/). Generated by\n"
                "   tools/build-hindi-foundation.py; edit STYLE there, not this file. */\n" + STYLE.strip() + "\n")



# ------------------------------------------------------------------ structured data
# (17 Nov 2026) Schema.org for the primer: the hub is a free Course whose
# hasPart lists the eighteen lessons; each lesson is a LearningResource with a
# BreadcrumbList. Emitted in the body like the level pages do. The pages are
# noindex until the owner approves indexing, so this is groundwork, not a
# ranking claim — it is still read by social cards and by the Course test.
def ld_json(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

def lesson_ld(L, title, desc, total):
    url = "%s/%s/%s/" % (BASE, SECTION, L["slug"])
    teaches = [L["en"], L["hi"]]
    if L.get("kind") == "letters":
        teaches += ["%s (%s)" % (x[0], x[1]) for x in L.get("letters", []) if isinstance(x, (tuple, list)) and len(x) > 1][:12]
    return ld_json({"@context": "https://schema.org", "@graph": [
        {"@type": "LearningResource", "@id": url + "#lesson", "name": title, "description": desc, "url": url,
         "inLanguage": "en", "about": {"@type": "Language", "name": "Hindi", "alternateName": "hi"},
         "learningResourceType": "lesson", "educationalLevel": "beginner", "isAccessibleForFree": True,
         "teaches": [t for t in teaches if t], "position": L["n"],
         "isPartOf": {"@type": "Course", "@id": "%s/%s/#course" % (BASE, SECTION), "name": "Hindi Foundation"},
         "audience": {"@type": "EducationalAudience", "educationalRole": "student"},
         "provider": {"@type": "Organization", "name": "EkGuru", "url": BASE + "/"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "EkGuru", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Learn Hindi", "item": BASE + "/learn/"},
            {"@type": "ListItem", "position": 3, "name": "Hindi Foundation", "item": "%s/%s/" % (BASE, SECTION)},
            {"@type": "ListItem", "position": 4, "name": "Lesson %d of %d: %s" % (L["n"], total, L["en"]), "item": url}]}]})

def hub_ld(title, desc):
    url = "%s/%s/" % (BASE, SECTION)
    return ld_json({"@context": "https://schema.org", "@graph": [
        {"@type": "Course", "@id": url + "#course", "name": "Hindi Foundation — हिंदी की नींव", "description": desc, "url": url,
         "inLanguage": "en", "about": {"@type": "Language", "name": "Hindi", "alternateName": "hi"},
         "educationalLevel": "beginner", "isAccessibleForFree": True, "numberOfLessons": len(C.LESSONS),
         "teaches": ["Devanagari vowels and consonants", "the twelve matras", "anusvar, visarg, chandrabindu", "conjunct letters", "reading a first Hindi story"],
         "provider": {"@type": "Organization", "name": "EkGuru", "url": BASE + "/"},
         "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "online", "courseWorkload": "PT20M"},
         "hasPart": [{"@type": "LearningResource", "@id": "%s%s/#lesson" % (url, L["slug"]), "name": "%d. %s — %s" % (L["n"], L["en"], L["hi"]), "url": "%s%s/" % (url, L["slug"]), "position": L["n"]} for L in C.LESSONS]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "EkGuru", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Learn Hindi", "item": BASE + "/learn/"},
            {"@type": "ListItem", "position": 3, "name": "Hindi Foundation", "item": url}]}]})

# ------------------------------------------------------------------ lesson page
def lesson_page(L, prev, nxt, total):
    up = UP_LESSON
    url = "%s/%s/" % (SECTION, L["slug"])
    title = "Hindi Foundation %d: %s — %s" % (L["n"], L["en"], L["hi"])
    desc = ("Lesson %d of the Hindi primer: %s (%s). %s" % (L["n"], L["en"], L["hi"], L["sub"]))[:158]
    crumb = ('<a href="%s">EkGuru</a> › <a href="%slearn/">Learn Hindi</a> › '
             '<a href="../">Hindi Foundation</a> › Lesson %d') % (up, up, L["n"])
    b = [chapter_band(up)]
    b.append('<h1>%d. %s <span lang="hi">%s</span></h1>' % (L["n"], e(L["en"]), e(L["hi"])))
    b.append('<p class="fd-sub">%s</p>' % e(L["sub"]))
    b.append('<p class="sb-hint">🔊 <b>Tap any Hindi word to hear it.</b> Too fast or slow? Use the <b>speed</b> button at the bottom-right of the page. '
             'This lesson opens <b>one step at a time</b> — press <b>Next</b> to turn the page, or choose <b>Whole lesson</b> to read it straight through.</p>')
    b.append('<div class="row" style="margin:12px 0"><button class="pill" id="fd-mark" type="button">Mark lesson %d complete</button> <span class="score" id="fd-prog"></span></div>' % L["n"])
    b.append('<p class="lede">%s</p>' % L["lede"])

    if L["kind"] == "letters":
        letters = L["letters"]
        b.append("<h2>The letters</h2>")
        b.append('<div class="trace-grid" data-traces="%s" data-roman="%s"></div>' % (
            e(",".join(x[0] for x in letters)), e(",".join(x[1] for x in letters))))
        b.append("<h2>Each letter with its word</h2>")
        b.append("<p>This is how the chart hangs on an Indian classroom wall: the letter, and the one word "
                 "every child learns it by. Say the letter, say the word, tap to hear both.</p>")
        b.append('<div class="fd-letters">')
        for lt, rm, hint, kw, kwr, kwe, emo in letters:
            b.append('<div class="fd-letter"><span class="lt" lang="hi">%s</span><span class="rm">%s</span>'
                     '<span class="kw" lang="hi">%s%s</span><span class="en">%s · %s</span>'
                     '<span class="hint">%s</span><div>%s %s</div></div>' % (
                         e(lt), e(rm), letter_illustration(lt, kw, emo), e(kw), e(kwr), e(kwe), e(hint), say(lt, "🔊 " + lt), say(kw, "🔊 " + kw)))
        b.append("</div>")
        if L["slug"] == "vyanjan-1":
            b.append('<details class="fd-air-demo"><summary lang="hi">क और ख — हवा का अंतर (Airflow)</summary><p lang="hi">हथेली मुँह के सामने रखिए। क बोलिए, फिर ख। ख में हवा का झोंका अधिक महसूस होता है।</p><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 124" role="img" aria-label="Schematic: a smaller air puff for ka, a stronger puff for kha"><rect x="1" y="1" width="318" height="122" rx="12" fill="#fff9ed" stroke="#d5cbb7"/><g stroke="#294d43" stroke-width="3" stroke-linecap="round" fill="none"><path d="M30 12Q65 11 65 27L76 31 66 37Q65 46 45 47M30 74Q65 73 65 89L76 93 66 99Q65 108 45 109"/><path d="M190 12V48M190 74V110" stroke="#8d7456" stroke-width="8"/></g><g fill="#357f93"><g class="air"><circle cx="104" cy="32" r="4"/><circle cx="124" cy="32" r="3"/></g><g class="air strong"><circle cx="103" cy="93" r="7"/><circle cx="125" cy="82" r="5"/><circle cx="126" cy="103" r="5"/><circle cx="148" cy="93" r="6"/><circle cx="168" cy="93" r="3"/></g></g><g fill="#23463d" font-family="sans-serif" font-size="13"><text x="208" y="35">ka</text><text x="208" y="97">kha</text></g></svg><p><small>Illustrative airflow, not an anatomical or measured diagram. Close and reopen to replay. Reduced-motion settings keep it still.</small></p></details>')
        b.append("<h2>What to notice</h2><ul>")
        for n in L["notes"]:
            b.append("<li>%s</li>" % fix_inline(n))
        b.append("</ul>")
    elif L["kind"] == "words":
        if L.get("sign"):
            sg, sgr, cons, form, formr = L["sign"]
            b.append("<h2>The sign</h2>")
            b.append('<div class="fd-sign">'
                     '<div><b lang="hi">%s</b><small>%s</small>%s</div><div class="op">+</div>'
                     '<div><b lang="hi">%s</b><small>the sign · %s</small></div><div class="op">=</div>'
                     '<div><b lang="hi">%s</b><small>%s</small>%s</div></div>' % (
                         e(cons), "ka", say(cons), e(sg), e(sgr), e(form), e(formr), say(form)))
            row = ["क", "ख", "ग", "च", "ज", "ट", "त", "द", "न", "प", "ब", "म", "र", "ल", "स", "ह"]
            forms = [c + sg for c in row]
            roms = [r + ("" if sgr == "halant" else sgr) for r in
                    ["k", "kh", "g", "ch", "j", "ṭ", "t", "d", "n", "p", "b", "m", "r", "l", "s", "h"]]
            b.append("<h3>The sign on sixteen letters</h3>")
            b.append("<p>Read the row aloud left to right, then tap any cell that gave you trouble.</p>")
            b.append('<div class="trace-grid" data-traces="%s" data-roman="%s"></div>' % (e(",".join(forms)), e(",".join(roms))))
        if L.get("sight"):
            b.append("<h2>The little words — learn their shape now</h2>")
            b.append("<p>These appear in almost every Hindi sentence. They carry signs you have not met yet, "
                     "so children learn them the way English children learn 'the' and 'is': by sight. "
                     "Their matras will make sense within a few lessons.</p>")
            b.append('<div class="fd-sight">')
            for dev, rom, en in C.SIGHT_WORDS:
                b.append('<span><b lang="hi">%s</b>%s · %s %s</span>' % (e(dev), e(rom), e(en), say(dev)))
            b.append("</div>")
        b.append("<h2>Words</h2>")
        b.append("<p>Sound out each word letter by letter, blend it, then tap the card to check the meaning. "
                 "Every word on this page uses only the signs taught so far.</p>")
        for gt, words in L["groups"]:
            b.append("<h3>%s</h3>" % e(gt))
            b.append('<div class="vcards">')
            for dev, rom, en in words:
                b.append(vcard(dev, rom, en))
            b.append("</div>")
        b.append("<h2>Sentences · वाक्य</h2>")
        b.append("<p>Read the Hindi first. Open the English only to check.</p>")
        b.append(lines_block(L["sentences"]))
        if L.get("passage"):
            pt, plines = L["passage"]
            b.append('<div class="fd-passage"><h3 lang="hi">%s %s</h3>' % (e(pt), say(pt)))
            b.append("<p>A reading passage — the kind that closes every primer chapter. Read it aloud, start to finish.</p>")
            b.append(lines_block(plines))
            b.append("</div>")
    elif L["kind"] == "reader":
        for st_hi, st_rom, st_en, slines in L["stories"]:
            b.append('<div class="fd-passage"><h3 lang="hi">%s %s</h3><p class="rm" style="color:var(--muted);margin:0 0 8px">%s · %s</p>' % (e(st_hi), say(st_hi), e(st_rom), e(st_en)))
            b.append(lines_block(slines))
            b.append("</div>")
        b.append("<h2>Questions · प्रश्न</h2>")
        b.append("<p>Answer in Hindi, aloud, before you open the answer.</p>")
        b.append('<ul class="fd-lines">')
        for q, qr, qe, a in L["questions"]:
            b.append('<li><span class="dv" lang="hi">%s %s</span><span class="rm">%s · %s</span>'
                     '<details><summary>Answer</summary>%s</details></li>' % (e(q), say(q), e(qr), e(qe), e(a)))
        b.append("</ul>")

    b.append('<div class="fd-task"><b>Today\'s task · आज का काम</b><p>%s</p></div>' % e(L["task"]))
    b.append(quiz_block(L["quiz"]))

    # prev / next
    b.append('<div class="row" style="margin:26px 0">')
    if prev:
        b.append('<a class="btn btn-ghost" href="../%s/">← Lesson %d</a>' % (prev["slug"], prev["n"]))
    b.append('<a class="btn btn-ghost" href="../">All %d lessons</a>' % total)
    if nxt:
        b.append('<a class="btn btn-primary" href="../%s/">Lesson %d →</a>' % (nxt["slug"], nxt["n"]))
    else:
        b.append('<a class="btn btn-primary" href="%sdaily-hindi/day-12/">Daily Hindi, day 12 →</a>' % up)
    b.append("</div>")

    b.append('<aside class="note" role="note"><b>A note on the Hindi spellings</b>'
             '<p>Devanagari is easy to get slightly wrong when it is typed by hand — a missing matra, the '
             'wrong nukta. If something here looks off to you, trust a native speaker over this page and '
             'please <a href="%scontact/?topic=Spelling">tell us</a> so it gets fixed. Romanised spellings '
             'are a guide to the sound, not a standard.</p></aside>' % up)
    b.append('<aside class="cta" aria-label="Next step"><b>Read it to a person</b>'
             '<p>Reading aloud to someone who can correct you is worth five silent repetitions. '
             'A single lesson with a tutor at this stage fixes the two or three sounds you cannot hear yourself getting wrong.</p>'
             '<a class="btn btn-primary" href="%sfind-tutors.html">Find a Hindi Guru</a>'
             '<a class="btn btn-ghost" href="%slearn/">Free Hindi guides</a></aside>' % (up, up))
    b.append("<h2>Also useful</h2><div class=\"chips\">"
             '<a href="%stoolbox/hindi-alphabet/">Alphabet explorer</a>'
             '<a href="%slearn/hindi-barakhadi/">Barakhadi chart</a>'
             '<a href="%slearn/hindi-how-to-write-vowels/">How to write the vowels</a>'
             '<a href="%slearn/hindi-how-to-write-consonants/">How to write the consonants</a>'
             '<a href="%stoolbox/hindi-flashcards/">Flashcards</a>'
             '<a href="%sdaily-hindi/">Daily Hindi — 30 days</a></div>' % ((up,) * 6))
    b.append(lesson_ld(L, title, desc, total))
    body = "\n".join(b) + progress_script(L["n"], total)
    html = head(title, desc, url, up)
    html += '    <p class="crumb">%s</p>\n' % crumb
    html += body
    # book-mode.js (17 Nov 2026) turns the article into a stepped reader with
    # generated practice; it reads the markup above, so nothing else changes.
    html += P.foot(up, ("book-mode.js",))
    if L['slug'] in DEPTH_CHAPTERS:
        html = D.transformed(html, DEPTH_CHAPTERS[L['slug']])
    html = R.transformed(html, R.load(), 'foundation-' + L['slug'])
    path = os.path.join(SECTION, L["slug"], "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


# ------------------------------------------------------------------ hub page
PHASES = [
    ("अक्षर · the letters", 1, 4),
    ("मात्रा · the vowel signs", 5, 14),
    ("बाकी चिह्न · the remaining marks", 15, 17),
    ("पढ़ना · reading", 18, 18),
]

def hub_page(total):
    up = UP_HUB
    url = SECTION + "/"
    title = "Hindi Foundation — Learn to Read Hindi the Way Indian Children Do (वर्णमाला, मात्रा, शब्द)"
    desc = ("A free 18-lesson Hindi primer in the classic Indian textbook order: vowels, consonants, "
            "words without matras, then one matra per lesson with graded word lists, sentences and a "
            "reading passage. Ends with your first story.")
    crumb = '<a href="%s">EkGuru</a> › <a href="%slearn/">Learn Hindi</a> › Hindi Foundation' % (up, up)
    b = [chapter_band(up)]
    b.append('<h1>Hindi Foundation <span lang="hi">हिंदी की नींव</span></h1>')
    b.append('<p class="fd-sub">Learn to read Hindi the way every Indian child does: letters, then signs, then words, then a story.</p>')
    b.append('<p class="sb-hint">🔊 <b>Tap any Hindi word to hear it.</b> Progress is ticked off in your own browser and never leaves it.</p>')
    b.append('<div class="row" style="margin:12px 0"><span class="score" id="fd-prog">Nothing marked yet</span> '
             '<a class="btn btn-primary" id="fd-resume" href="%s/">Start at lesson 1</a> '
             '<button class="pill" id="fd-reset" type="button">Reset progress</button></div>' % C.LESSONS[0]["slug"])
    b.append(fix_inline('<p class="lede">Open any class-1 Hindi reader printed in India and the order is always the same. '
             'First the <b>स्वर</b> (vowels) and <b>व्यंजन</b> (consonants), each with the one picture-word a child learns it by. '
             'Then words made of bare letters — <span class="spk" lang="hi">कमल</span>, <span class="spk" lang="hi">नमक</span>. '
             'Then <b>one मात्रा per chapter</b>: आ की मात्रा के शब्द, इ की मात्रा के शब्द, and so on through all twelve, '
             'each chapter with a word ladder, a handful of sentences and a short passage that uses <i>only</i> what has been taught. '
             'Then the dots, the half letters, and finally a real story. This section is that book, free, with sound on every word.</p>'))
    b.append('<div class="sb-callout"><b>Who this is for.</b> Anyone starting Devanagari from zero — adult learners, '
             'children of the diaspora, parents teaching at home. It assumes nothing. If you already read Hindi slowly, '
             'start at lesson 5 and use the word ladders as speed drills.</div>')
    b.append("<h2>The eighteen lessons</h2>")
    for ph, a, z in PHASES:
        b.append('<p class="fd-phase">%s</p>' % e(ph))
        b.append('<ol class="fd-ladder" start="%d">' % a)
        for L in C.LESSONS[a - 1:z]:
            b.append('<li data-n="%d"><span class="num">%d</span><span><a href="%s/">%s</a><span class="hi" lang="hi">%s · %s</span></span>'
                     '<a class="btn btn-ghost" href="%s/">Open</a></li>' % (L["n"], L["n"], L["slug"], e(L["en"]), e(L["hi"]), e(L["sub"]), L["slug"]))
        b.append("</ol>")
    b.append("<h2>How to use it</h2><ol>"
             "<li><b>One lesson a day,</b> twenty minutes. The matra lessons are the slow ones; give them two days if you need to.</li>"
             "<li><b>Say everything aloud.</b> Tap the speaker, copy it, tap again. Silent reading builds recognition; speech builds reading.</li>"
             "<li><b>Write what you read.</b> Each lesson ends with a copying or dictation task. That is the step textbooks have and apps skip.</li>"
             "<li><b>Do not jump ahead.</b> Every word in lesson 9 uses only the signs from lessons 1 to 9. The ladder only works if you climb it in order.</li>"
             "<li><b>Turn the pages.</b> Each lesson opens one step at a time — the sign, the words, then six short practice pages "
             "(match, listen, build the word, picture, read it, order the sentence) made from that lesson's own words — and ends with the quick check. "
             "Press <b>Next</b>, or choose <b>Whole lesson</b> to read it straight through.</li>"
             "</ol>")
    b.append("<h2>Where this fits</h2>"
             "<p>This section teaches <i>reading</i>. It deliberately avoids grammar, gender and tenses — those are in "
             '<a href="%sdaily-hindi/">Daily Hindi</a> (days 16 onward) and the <a href="%scourses/#/hi">A1 course</a>. '
             'The <a href="%slearn/hindi-alphabet-for-beginners/">alphabet guide</a> explains the system in one sitting; '
             'the <a href="%slearn/hindi-barakhadi/">barakhadi chart</a> drills all twelve signs on every letter; this section is the '
             "slow, graded walk between the two — the one a child actually takes.</p>" % (up, up, up, up))
    b.append('<aside class="cta" aria-label="Next step"><b>Finished all eighteen?</b>'
             '<p>You can read. Now get the sounds checked by a person — a single lesson fixes the two or three letters you cannot hear yourself mispronouncing.</p>'
             '<a class="btn btn-primary" href="%sfind-tutors.html">Find a Hindi Guru</a>'
             '<a class="btn btn-ghost" href="%sdaily-hindi/">Daily Hindi — 30 days</a></aside>' % (up, up))
    b.append('<h2>Also on the site</h2><div class="chips">'
             '<a href="%stoolbox/hindi-alphabet/">Alphabet explorer</a>'
             '<a href="%slearn/hindi-barakhadi/">Barakhadi chart</a>'
             '<a href="%slearn/hindi-how-to-write-vowels/">Writing the vowels</a>'
             '<a href="%slearn/hindi-how-to-write-consonants/">Writing the consonants</a>'
             '<a href="%smaterials/alphabet/devanagari-chart/">Printable Devanagari chart</a>'
             '<a href="%slearn/">All free guides</a></div>' % ((up,) * 6))
    b.append("""
<script defer>
(function(){
  var T=%d,K=%s,SL=%s;
  function get(){try{return JSON.parse(localStorage.getItem(K)||"[]")}catch(e){return []}}
  var d=get(),pr=document.getElementById("fd-prog"),rs=document.getElementById("fd-resume"),rt=document.getElementById("fd-reset");
  function paint(){d=get();
    if(pr)pr.textContent=d.length?d.length+" of "+T+" lessons done":"Nothing marked yet";
    var items=document.querySelectorAll(".fd-ladder li[data-n]");
    for(var i=0;i<items.length;i++){items[i].classList.toggle("done",d.indexOf(Number(items[i].getAttribute("data-n")))>-1);}
    if(rs){var nx=1;while(nx<=T&&d.indexOf(nx)>-1)nx++;if(nx>T)nx=T;rs.textContent=d.length?"Resume at lesson "+nx:"Start at lesson 1";rs.setAttribute("href",SL[nx-1]+"/");}
  }
  if(rt)rt.addEventListener("click",function(){if(confirm("Clear your Hindi Foundation progress on this device?")){try{localStorage.removeItem(K)}catch(e){}paint();}});
  paint();
})();
</script>
""" % (total, json.dumps(STORE_KEY), json.dumps([L["slug"] for L in C.LESSONS])))
    b.append(hub_ld(title, desc))
    html = head(title, desc, url, up)
    html += '    <p class="crumb">%s</p>\n' % crumb
    html += "\n".join(b)
    html += P.foot(up, ())
    path = os.path.join(SECTION, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


# ------------------------------------------------------------------ main
def main():
    problems = validate()
    if problems:
        print("REFUSING TO BUILD — %d primer-rule violations:" % len(problems))
        for p in problems:
            print("  " + p)
        return 1
    print("primer rule: PASS (every word uses only the signs taught so far)")
    if "--check" in sys.argv:
        return 0
    total = len(C.LESSONS)
    write_css()
    written = [hub_page(total)]
    for i, L in enumerate(C.LESSONS):
        prev = C.LESSONS[i - 1] if i else None
        nxt = C.LESSONS[i + 1] if i + 1 < total else None
        written.append(lesson_page(L, prev, nxt, total))
    words = sum(len(w) for L in C.LESSONS for _, w in L.get("groups", []))
    sents = sum(len(L.get("sentences", [])) + (len(L["passage"][1]) if L.get("passage") else 0) for L in C.LESSONS)
    sents += sum(len(s[3]) for L in C.LESSONS for s in L.get("stories", []))
    print("wrote %d pages · %d words in ladders · %d sentences/lines" % (len(written), words, sents))
    for w in written:
        print("  " + w)
    return 0


if __name__ == "__main__":
    sys.exit(main())

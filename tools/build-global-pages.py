#!/usr/bin/env python3
"""Phase 7C §32/§33 — generate the GLOBAL learning dashboard.

Builds:
  /learn/my-learning/   My Learning — device-only dashboard (noindex)

The page integrates the reusable Phase 7C engines on one real surface:
  · EkGuruGoals          goal system with honest availability
  · EkGuruSearch         language-aware learning search
  · EkGuruScript         script registry (direction / status)
  · EkGuruGrammar        grammar engine (6 authored concepts)
  · EkGuruVocab          vocabulary/phrase engine (authored items)
  · EkGuruProgress / EkGuruSRS / EkGuruOffline   device-only state

Honesty rules: everything is clearly "saved on this device", nothing is
uploaded, no account exists, and the search index is built from real
content (content graph + authored engine data) — never from invented pages.

Also (idempotently) adds a "My Learning" card link to /learn/index.html.

Run: python3 tools/build-global-pages.py
"""
import os
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "https://ekguru.shop"

# Reuse the Phase 6 head/foot/write_page helpers (single source of truth).
_spec = importlib.util.spec_from_file_location("hindi_pages", os.path.join(ROOT, "tools", "build-hindi-pages.py"))
_hp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hp)
head, foot, write_page = _hp.head, _hp.foot, _hp.write_page

MYLEARN_CSS = """
.dash{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:18px 0}
.dash .k{background:var(--bg-soft);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.dash .k b{display:block;font-size:1.25rem;color:var(--ink)}
.dash .k span{font-size:.76rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.box{border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:22px 0;background:var(--card,#fff)}
.box h2{font-size:1.12rem;margin:0 0 10px}
.goal-list{list-style:none;padding:0;margin:8px 0 0}
.goal{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px;padding:9px 0;border-bottom:1px solid var(--line)}
.goal:last-child{border-bottom:0}
.goal-name{font-weight:600}
.goal-status{font-size:.74rem;border-radius:999px;padding:2px 9px;border:1px solid var(--line)}
.goal-status.available{background:#e7f6ec;color:#1a7a3c;border-color:#bfe7cb}
.goal-status.partial{background:#fff6e0;color:#9a6700;border-color:#f0dcae}
.goal-status.planned{background:var(--bg-soft);color:var(--muted)}
.goal-blurb{flex-basis:100%;margin:0;color:var(--ink-2);font-size:.92rem;line-height:1.55}
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
.v-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.v-item{border:1px solid var(--line);border-radius:12px;padding:12px 13px;background:var(--bg-soft)}
.v-target{font-size:1.15rem;font-weight:600;margin:0}
.v-roman{color:var(--muted);font-size:.85rem;margin:2px 0 6px}
.v-meaning{margin:0;color:var(--ink-2);font-size:.92rem}
.v-pos,.v-reg,.v-topic{font-size:.72rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:1px 7px;margin-right:4px}
.searchbox{width:100%;padding:12px 14px;font-size:1.02rem;border:1px solid var(--line);border-radius:10px;min-height:44px;color:var(--ink);background:#fff}
.searchbox:focus{outline:2px solid var(--focus);outline-offset:1px}
.search-results{list-style:none;padding:0;margin:10px 0 0}
.s-item{padding:9px 0;border-bottom:1px solid var(--line)}
.s-item:last-child{border-bottom:0}
.s-type{font-size:.7rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:1px 7px;margin-right:8px;vertical-align:1px}
.s-item a,.s-title{font-weight:600;color:var(--brand)}
.s-sub{display:block;color:var(--ink-2);font-size:.88rem;margin-top:2px}
.s-meta{display:block;color:var(--muted);font-size:.78rem;margin-top:2px}
.scr{border:1px solid var(--line);border-radius:12px;padding:11px 14px;margin:8px 0;background:var(--bg-soft)}
.scr b{font-weight:600}
.scr .st{font-size:.72rem;border-radius:999px;padding:1px 8px;margin-left:8px;vertical-align:1px}
.st-prod{background:#e7f6ec;color:#1a7a3c;border:1px solid #bfe7cb}
.st-plan{background:var(--bg-soft);color:var(--muted);border:1px solid var(--line)}
.offline-list{list-style:none;padding:0;margin:6px 0 0;font-size:.92rem}
.offline-list li{margin:5px 0;color:var(--ink-2)}
"""


def my_learning_page():
    up = "../../"
    body = """  <h1>My Learning</h1>
  <p class="lede">One dashboard for everything you are learning on EkGuru —
  your progress, your review queue, your goals and a search across all the
  learning content, in your browser.</p>
  <div class="note"><b>Saved on this device.</b> Nothing on this page is uploaded.
  There is no account and no server copy — if you clear your browser data or switch
  devices, your progress does not travel with you. (That is the honest trade-off of
  a private, account-free product.)</div>

  <div class="box" id="progress-box">
    <h2>Your progress</h2>
    <div class="dash" id="progress-dash"><p class="muted">Reading your local progress…</p></div>
  </div>

  <div class="box" id="goals-box">
    <h2>Your goals</h2>
    <div id="goals-app"><p class="muted">Loading goals…</p></div>
  </div>

  <div class="box" id="search-box">
    <h2>Search learning content</h2>
    <p class="muted" style="margin:0 0 10px">Find a Hindi word by its Devanagari
    spelling, its romanisation (<em>paani</em>) or its English meaning (<em>water</em>).
    Matches lessons, phrases, grammar concepts, conversation scenarios and paths —
    ranked, with typo tolerance.</p>
    <input class="searchbox" type="search" id="learn-q" aria-label="Search learning content" placeholder="e.g. paani, पानी, water, past tense, travel" autocomplete="off">
    <div id="learn-res"><p class="muted">Start typing to search.</p></div>
  </div>

  <div class="box" id="grammar-box">
    <h2>Grammar at a glance</h2>
    <div id="grammar-app"><p class="muted">Loading grammar…</p></div>
  </div>

  <div class="box" id="vocab-box">
    <h2>Vocabulary to start</h2>
    <div class="v-grid" id="vocab-app"><p class="muted">Loading vocabulary…</p></div>
  </div>

  <div class="box" id="offline-box">
    <h2>Saved offline</h2>
    <div id="offline-app"><p class="muted">Reading your saved pages…</p></div>
  </div>

  <div class="box" id="family-box">
    <h2>Family & children</h2>
    <p class="muted" style="margin:0 0 10px">A privacy mode for parents and family learners,
    saved on this device only. When on, it stops visitor counting and hides the
    tutor/booking contact points on pages that carry them.</p>
    <p class="muted" style="margin:0 0 10px"><b>What it never does:</b> no child profile, no
    messaging, no child contact details, no social features for minors, no hidden recording —
    the microphone is only ever used after an explicit tap, and there is no account to collect
    anything anyway.</p>
    <p class="muted" style="margin:0 0 10px"><b>Honest scope:</b> this is a privacy mode, not
    child lesson content — no child-specific lessons have been authored yet.</p>
    <div id="family-app"></div>
  </div>

  <div class="box" id="script-box">
    <h2>Script support</h2>
    <div id="script-app"><p class="muted">Loading script registry…</p></div>
  </div>

  <script defer>
  (function () {
    "use strict";
    function when(name, cb, tries) {
      if (window[name]) { cb(window[name]); return; }
      var n = 0, t = setInterval(function () {
        if (window[name]) { clearInterval(t); cb(window[name]); }
        else if (++n > (tries || 60)) { clearInterval(t); }
      }, 100);
    }
    function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

    /* ---- progress ---- */
    function progress() {
      var el = document.getElementById("progress-dash");
      if (!el) return;
      var P = window.EkGuruProgress;
      if (!P || typeof P.snapshot !== "function") { el.innerHTML = '<p class="muted">Progress tracking did not load.</p>'; return; }
      var s;
      try { s = P.snapshot(); } catch (e) { el.innerHTML = '<p class="muted">Could not read progress.</p>'; return; }
      var quizzes = 0;
      try { quizzes = Object.keys(s.quizzes || {}).length; } catch (e) {}
      el.innerHTML =
        '<div class="k"><b>' + (s.lessonsOpened || 0) + '</b><span>lessons opened</span></div>' +
        '<div class="k"><b>' + (s.lessonsCompleted || 0) + '</b><span>lessons completed</span></div>' +
        '<div class="k"><b>' + quizzes + '</b><span>quizzes taken</span></div>' +
        '<div class="k"><b>' + (s.reviewCards || 0) + '</b><span>review cards</span></div>' +
        '<div class="k"><b>' + (s.reviewDue || 0) + '</b><span>reviews due</span></div>' +
        '<div class="k"><b>' + (s.pathsStarted || 0) + '</b><span>paths started</span></div>';
    }

    /* ---- goals ---- */
    function goals() {
      var el = document.getElementById("goals-app");
      if (!el || !window.EkGuruGoals) return;
      window.EkGuruGoals.ready().then(function () { window.EkGuruGoals.render(el); })
        .catch(function () { el.innerHTML = '<p class="muted">Goals are unavailable (content graph missing).</p>'; });
    }

    /* ---- search ---- */
    function search() {
      var input = document.getElementById("learn-q"), res = document.getElementById("learn-res");
      if (!input || !res || !window.EkGuruSearch) return;
      var timer = null;
      input.addEventListener("input", function () {
        clearTimeout(timer);
        var q = input.value;
        timer = setTimeout(function () {
          window.EkGuruSearch.ready().then(function () {
            window.EkGuruSearch.render(res, q);
          }).catch(function () { res.innerHTML = '<p class="muted">Search index unavailable.</p>'; });
        }, 120);
      });
    }

    /* ---- grammar ---- */
    function grammar() {
      var el = document.getElementById("grammar-app");
      if (!el || !window.EkGuruGrammar) return;
      window.EkGuruGrammar.ready().then(function () { window.EkGuruGrammar.renderAll(el); })
        .catch(function () { el.innerHTML = '<p class="muted">Grammar unavailable.</p>'; });
    }

    /* ---- vocabulary ---- */
    function vocab() {
      var el = document.getElementById("vocab-app");
      if (!el || !window.EkGuruVocab) return;
      window.EkGuruVocab.ready().then(function () {
        window.EkGuruVocab.renderList(el, function (i) { return i.type === "word"; });
      }).catch(function () { el.innerHTML = '<p class="muted">Vocabulary unavailable.</p>'; });
    }

    /* ---- offline ---- */
    function offline() {
      var el = document.getElementById("offline-app");
      if (!el) return;
      var OFF = window.EkGuruOffline;
      if (!OFF || typeof OFF.savedList !== "function") { el.innerHTML = '<p class="muted">Offline saving did not load.</p>'; return; }
      var list = [];
      try { list = OFF.savedList() || []; } catch (e) {}
      if (!list.length) { el.innerHTML = '<p class="muted">You have not saved any pages for offline reading yet. Use “Save for offline” on any lesson.</p>'; return; }
      el.innerHTML = '<ul class="offline-list">' + list.map(function (u) {
        return '<li><a href="' + esc(u) + '">' + esc(u) + '</a></li>';
      }).join("") + "</ul>";
    }

    /* ---- family mode ---- */
    function family() {
      var el = document.getElementById("family-app");
      if (!el || !window.EkGuruFamilyMode) return;
      window.EkGuruFamilyMode.mount(el);
    }

    /* ---- scripts ---- */
    function scripts() {
      var el = document.getElementById("script-app");
      if (!el || !window.EkGuruScript) return;
      window.EkGuruScript.ready().then(function () {
        var list = window.EkGuruScript.list();
        el.innerHTML = list.map(function (s) {
          var cls = s.productionStatus === "PRODUCTION" ? "st-prod" : "st-plan";
          var note = esc(s.note || "");
          return '<div class="scr"><b>' + esc(s.name) + '</b> <span class="st ' + cls + '">' + esc(s.productionStatus.toLowerCase()) + '</span>'
            + '<span class="s-meta">direction: ' + esc(s.direction) + ' · transliteration: ' + esc(s.transliteration || "none yet") + '</span>'
            + '<span class="s-meta">' + note + '</span></div>';
        }).join("");
      }).catch(function () { el.innerHTML = '<p class="muted">Script registry unavailable.</p>'; });
    }

    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", function () {
        progress(); goals(); search(); grammar(); vocab(); offline(); family(); scripts();
        when("EkGuruProgress", progress); when("EkGuruGoals", goals); when("EkGuruSearch", search);
        when("EkGuruGrammar", grammar); when("EkGuruVocab", vocab); when("EkGuruScript", scripts);
        when("EkGuruFamilyMode", family);
      });
    } else {
      progress(); goals(); search(); grammar(); vocab(); offline(); family(); scripts();
      when("EkGuruProgress", progress); when("EkGuruGoals", goals); when("EkGuruSearch", search);
      when("EkGuruGrammar", grammar); when("EkGuruVocab", vocab); when("EkGuruScript", scripts);
      when("EkGuruFamilyMode", family);
    }
  })();
  </script>
"""
    scripts = ("content-graph.js", "goals.js", "script-engine.js", "grammar-engine.js",
               "vocab-phrase-engine.js", "global-search.js", "hindi-srs.js",
               "hindi-progress.js", "hindi-offline.js", "family-mode.js")
    write_page("learn/my-learning/index.html", up,
               "My Learning — your progress, goals and review on this device",
               "Your Hindi progress, spaced-repetition review queue, goals and a language-aware search across every lesson, phrase and grammar concept — saved on this device, never uploaded.",
               "learn/my-learning/",
               '<a href="../../">EkGuru</a> › <a href="../">Learn</a> › My Learning',
               body, scripts=scripts, index=False, extra_style=MYLEARN_CSS)
    return "learn/my-learning/index.html"


CC_CSS = """
.cc-head h2{margin:0 0 6px;font-size:1.3rem}
.cc-sub{color:var(--ink-2);margin:0 0 8px;line-height:1.6}
.cc-note{font-size:.9rem}
.cc-shared{font-size:.9rem;color:var(--ink-2);margin:12px 0}
.cc-mod{border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:14px 0;background:var(--bg-soft)}
.cc-mod h3{margin:0 0 10px;font-size:1.05rem}
.cc-phrases{list-style:none;padding:0;margin:0 0 4px}
.cc-phrase{padding:7px 0;border-bottom:1px dashed var(--line)}
.cc-phrase:last-child{border-bottom:0}
.cc-target{font-weight:600;font-size:1.02rem}
.cc-roman{display:block;color:var(--muted);font-size:.85rem;margin:1px 0}
.cc-meaning{color:var(--ink-2);font-size:.9rem}
.cc-links{list-style:none;padding:0;margin:10px 0 0}
.cc-links li{margin:6px 0}
.cc-links a{font-weight:600}
"""


def _context_page(cid, up, title, desc, url, crumb, lede, scripts):
    body = '  <h1>%s</h1>\n  <p class="lede">%s</p>\n  <div class="note"><b>Honest scope.</b> This is a curated path built from '
    body += 'real published phrases and lessons — a context on top of the shared Hindi course, not a new course. '
    body += 'Nothing here is AI-generated; every phrase is copied from a page that already exists on EkGuru.</div>\n'
    body += '  <div id="ctx-app"><p class="muted">Loading…</p></div>\n'
    body += """  <script defer>
  (function(){
    var el=document.getElementById("ctx-app");
    if(!el)return;
    function whenReady(cb){
      if(window.EkGuruCountryContext){cb();return;}
      var n=0,t=setInterval(function(){
        if(window.EkGuruCountryContext){clearInterval(t);cb();}
        else if(++n>40){clearInterval(t);el.innerHTML='<p class="muted">Context unavailable right now.</p>';}
      },100);
    }
    whenReady(function(){
      window.EkGuruCountryContext.ready().then(function(){
        window.EkGuruCountryContext.render(el, "%s");
      }).catch(function(){el.innerHTML='<p class="muted">Context unavailable right now.</p>';});
    });
  })();
  </script>
"""
    body = body % (title, lede, cid)
    return write_page(url + "index.html", up, title, desc, url, crumb, body, scripts=scripts, index=True, extra_style=CC_CSS)


def context_pages():
    up = "../../../"
    made = []
    made.append(_context_page(
        "india-visitor", up,
        "Learn Hindi for India — the visitor's phrase path",
        "Survive a trip to India: greetings, taxis, directions, restaurant, shopping, trains and help — real phrases with romanisation, rehearsed on top of the shared Hindi course.",
        "learn/contexts/india-visitor/",
        '<a href="../../../">EkGuru</a> › <a href="../../">Learn</a> › <a href="../">Contexts</a> › India visitor',
        "A visitor's path through Hindi: the phrases that handle a trip — airport, taxi, hotel, food, money and help — organised so you can rehearse each situation before you land.",
        ("country-context.js", "hindi-srs.js")))
    made.append(_context_page(
        "heritage", up,
        "Hindi for Family & Heritage Learners",
        "Reconnect with family and culture: Hindi family words, respectful forms, culture and reading progression for NRI and heritage learners — built from real published content.",
        "learn/contexts/heritage/",
        '<a href="../../../">EkGuru</a> › <a href="../../">Learn</a> › <a href="../">Contexts</a> › Family & heritage',
        "A path for heritage learners: the family words, respectful forms and culture notes that matter at home — without assuming every family speaks the same variety.",
        ("country-context.js", "hindi-srs.js")))
    return made


def contexts_hub():
    up = "../../"
    body = """  <h1>Learn Hindi for your context</h1>
  <p class="lede">The same Hindi course, framed for how you will actually use it.
  A context is a lens — a curated path of real phrases and lessons — on top of the
  shared <a href="../hindi/">Hindi course</a>. It is not a separate course and it
  does not duplicate the lessons; it re-uses them for your situation.</p>
  <div class="note"><b>Honest scope.</b> Today there are two contexts: the India
  visitor and the family/heritage learner. Every phrase in them is copied from a
  page that already exists on EkGuru — nothing here is AI-generated or invented
  for SEO.</div>
  <h2>Choose your context</h2>
  <ul class="linklist">
    <li><a href="india-visitor/">Learn Hindi for India — the visitor's path</a><span>Greetings, taxis, restaurant, shopping, trains and help — the phrases that handle a trip, organised so you can rehearse each situation.</span></li>
    <li><a href="heritage/">Hindi for Family &amp; Heritage Learners</a><span>Family words, respectful forms, culture and reading progression — for reconnecting with family, without assuming every family speaks the same variety.</span></li>
  </ul>
  <h2>Prefer the full course?</h2>
  <p>If you want the complete beginner-to-intermediate track, start with the
  <a href="../hindi/">Hindi course hub</a> or pick a <a href="../paths/">goal-based learning path</a>.</p>
"""
    return write_page("learn/contexts/index.html", up,
                      "Learn Hindi for your context — India visitor & heritage paths",
                      "Two curated Hindi paths on top of the shared course: survive a trip to India, or reconnect with family as a heritage learner. Real phrases from real pages.",
                      "learn/contexts/",
                      '<a href="../../">EkGuru</a> › <a href="../">Learn</a> › Contexts',
                      body, scripts=(), index=True, extra_style="")


def patch_learn_hub():
    """Idempotently add My Learning + Contexts cards to /learn/index.html."""
    p = "learn/index.html"
    h = open(p, encoding="utf-8").read()
    anchor = '<h2>Practise, don\'t just read</h2>'
    changed = False
    if 'href="./my-learning/"' not in h and 'href="../my-learning/"' not in h:
        card = ('  <div class="lcard" style="margin-top:26px">\n'
                '    <h2>Your learning, in one place</h2>\n'
                '    <p>Progress, review queue, goals and a language-aware search across\n'
                '    every lesson and phrase — saved on this device, never uploaded.</p>\n'
                '    <a class="btn btn-ghost" href="./my-learning/">Open My Learning →</a>\n'
                '  </div>\n\n')
        if anchor in h:
            h = h.replace(anchor, card + anchor, 1)
            changed = True
    if 'href="./contexts/"' not in h:
        ctx_card = ('  <div class="lcard" style="margin-top:26px">\n'
                    '    <h2>Learning for your context</h2>\n'
                    '    <p>India visitor or family/heritage learner? Two curated paths\n'
                    '    reuse the same Hindi course for your situation.</p>\n'
                    '    <a class="btn btn-ghost" href="./contexts/">Choose your context →</a>\n'
                    '  </div>\n\n')
        if anchor in h:
            h = h.replace(anchor, ctx_card + anchor, 1)
            changed = True
    if changed:
        open(p, "w", encoding="utf-8").write(h)
    return changed


def main():
    made = []
    made.append(my_learning_page())
    made += context_pages()
    made.append(contexts_hub())
    hub = patch_learn_hub()
    print("generated:")
    for m in made:
        print("   %s" % m)
    print("learn hub card added: %s" % hub)


if __name__ == "__main__":
    main()

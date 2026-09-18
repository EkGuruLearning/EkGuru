#!/usr/bin/env python3
"""Every course, readable at every level: the A1–C2 pages.

WHY THIS FILE EXISTS
--------------------
`data/courses/<phase>/<code>_<LEVEL>.json` has been the real course data since
phase 1 — six levels per language, three units per level, six authored lessons
per level, each lesson carrying a learn text, a vocabulary list with
romanisation, a grammar point with examples and a mistakes note, a dialogue,
twelve practice items, five quiz items, a worksheet and an SRS selection; and a
ten-item level test on top.

Until now that material was reachable only through the JavaScript course player
on `/courses/#/<code>/<level>` — a hash route no crawler can index and nobody
without JavaScript can open. The static pages under `languages/<code>/lessons/`
covered six lessons per language: the A1 sampler. Everything above it, and the
whole of A2–C2, existed in the repository and nowhere a reader could go.

So this tool writes it out as real pages:

  languages/<code>/level/index.html              the ladder for that language
  languages/<code>/level/<a1..c2>/index.html     one level, in full

Every page is plain HTML: the learn text, the vocabulary table, the grammar
(examples and the mistakes people make), the dialogue with romanisation, all
twelve practice items, the quiz with its explanations, the worksheet with its
key, the ten-item level test, and recall drills generated from that level's own
word list in both directions.

NOTHING IS INVENTED. The drills are re-asks of the authored vocabulary, and the
page says so. Grammar, dialogues, examples and answers come from the course
data unchanged — this tool formats, it does not author. (The site's rule for
generated practice: a machine may re-order and re-ask what a human wrote, and
must never be described as a teacher.)

Also patched, by design:
  · the level rail on the language's own hub, between the
    `ekguru:course-levels` markers, so the hub links the level pages;
  · sitemap-levels.xml, declared in sitemap-index.xml.

WHY THE LEVEL PAGES CARRY NO AD
-------------------------------
A learner on this page is mid-task from top to bottom — lesson, dialogue,
practice, quiz, worksheet, level test. The site's promise, printed on every one
of them, is that the practice itself carries no ad. A page that says that and
then loads an ad script would be lying in the same file. The page class is
INTERACTIVE_LEARNING (data/monetization/google-monetization.json), which is what
tells tools/inject-ads.py not to put the loader here.

Run:  python3 tools/build-course-levels.py [--check] [--lang XX]
"""

import hashlib
import importlib.util
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# build-hindi-pages.py has a hyphen in its name, so import it by path — the
# same head/foot/write_page the world courses and the lesson pages use, so
# these pages are the same site and not a second design.
_spec = importlib.util.spec_from_file_location(
    "build_hindi_pages", os.path.join(ROOT, "tools", "build-hindi-pages.py"))
_bhp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bhp)
head, foot, write_page = _bhp.head, _bhp.foot, _bhp.write_page


CATALOGUE = "data/courses/index.json"
LEVEL_FILE = "data/levels.json"
VISUALS = "data/visuals.json"
SITEMAP = "sitemap-levels.xml"
INDEX = "sitemap-index.xml"
BASE = "https://ekguru.shop"

RAIL_START = "<!-- ekguru:course-levels:start -->"
RAIL_END = "<!-- ekguru:course-levels:end -->"

# Where a language's hub lives, so the rail can be spliced onto the page a
# visitor actually lands on. Same resolution order as tools/build-visuals.py:
# the rendered course page, then the /learn/ hub of an Indian language, then
# the language's own starter page. Eleven of the 39 catalogue languages have no
# hub page at all — for those the rail has nowhere to go, and the /courses/
# catalogue links their level pages directly.
INDIAN = {"hi": "hindi", "bn": "bengali", "gu": "gujarati", "kn": "kannada",
          "ml": "malayalam", "mr": "marathi", "pa": "punjabi", "ta": "tamil",
          "te": "telugu", "ur": "urdu"}

# The level → ladder rung bridge. The ladder has eleven rungs (six CEFR levels
# plus the half-step after each of the first five — see data/levels.json); a
# course has the six. A level page takes its figure from its own rung.
LEVEL_RUNG = {"A1": "a1", "A2": "a2", "B1": "b1", "B2": "b2", "C1": "c1", "C2": "c2"}
NEXT_RUNG = {"A1": "a1p", "A2": "a2p", "B1": "b1p", "B2": "b2p", "C1": "c1p", "C2": ""}

LEVEL_NAMES = {"A1": "Beginner", "A2": "Elementary", "B1": "Intermediate",
               "B2": "Upper intermediate", "C1": "Advanced", "C2": "Mastery"}

TYPE_LABEL = {
    "multiple_choice": "multiple choice", "word_selection": "choose the word",
    "matching": "matching", "reading_comprehension": "reading",
    "paragraph_comprehension": "paragraph", "reorder": "put it in order",
    "sentence_building": "build the sentence", "fill_in_the_blank": "fill the gap",
    "listening_comprehension": "listening", "translation": "translate",
    "error_correction": "find the mistake", "dialogue_completion": "finish the dialogue",
    "reverse_translation": "translate into the language", "dictation": "dictation",
    "listen_and_choose": "listen and choose", "inference": "what is meant",
    "listen_and_reorder": "listen, then order", "main_idea": "the main idea",
    "repeat_after_audio": "repeat it", "detail_identification": "spot the detail",
    "listen_and_fill": "listen and fill", "pronunciation": "pronunciation",
    "shadowing": "shadow the audio", "guided_speaking": "guided speaking",
    "roleplay": "role play", "sentence_writing": "write a sentence",
    "free_response": "answer in your own words", "short_writing": "short writing",
    "paraphrase": "say it another way", "summary": "summarise",
    "guided_composition": "guided composition", "register_transformation": "change the register",
    "tone_identification": "read the tone", "semantic_distinction": "which one fits",
    "contextual_meaning": "meaning in context", "discourse_ordering": "order the text",
    "argument_construction": "build the argument", "style_rewriting": "rewrite the style",
    "idiom_interpretation": "explain the idiom", "implied_meaning": "read between the lines",
    "translate_en": "translate into the language", "translate_t": "translate into English",
    "fill": "fill the gap", "choose": "choose", "speak": "say it out loud",
}


_clean = lambda t: str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def compose(up, title, desc, url, crumb, body, index=True):
    """The exact page write_page() would write, without writing it.

    --check has to compare content, not just existence: a level page that
    exists but still shows last week's data is a stale page, and a build that
    only looked for the file would call it current."""
    return (head(title, desc, url, up, index=index)
            + '    <p class="crumb">%s</p>\n' % crumb
            + body
            + foot(up))


FP = "<!-- ekguru:course-levels:fp:"


def stamp(html):
    """Put a fingerprint of the page's own content into the page.

    The page is decorated after this tool writes it — the storybook injector
    adds a chapter banner and the TTS hint, inject-ads.py writes the ad class
    onto <html>, the page layer adds the bands. So --check cannot compare the
    file byte for byte: every decorated page would look stale forever, and the
    fix (rebuilding) would throw the decoration away. The fingerprint covers
    what this tool owns — the content it generated — and survives anything
    added around it. A page whose data has moved on has the wrong fingerprint,
    which is exactly the drift the check exists to catch.
    """
    digest = hashlib.sha1(html.encode("utf-8")).hexdigest()[:16]
    return html.replace("</body>", "\n" + FP + digest + " -->\n</body>", 1), digest


def emit(path, html, check, stale):
    html, digest = stamp(html)
    if check:
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if old is None or (FP + digest + " -->") not in old:
            stale.append(path)
            print("STALE: %s needs tools/build-course-levels.py" % path)
        return 0
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return 1


def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def catalogue():
    data = load_json(CATALOGUE, {}) or {}
    return data.get("courses", []), data.get("levels") or ["A1", "A2", "B1", "B2", "C1", "C2"]


def level_data(code, phase, level):
    path = "data/courses/%s/%s_%s.json" % (phase, code, level)
    if not os.path.exists(path):
        return None
    return load_json(path)


def rungs():
    return {r["id"]: r for r in (load_json(LEVEL_FILE, {}) or {}).get("rungs", [])}


def figures():
    return (load_json(VISUALS, {}) or {}).get("figures", {})


def hub_for(code):
    for cand in ("languages/%s/course/index.html" % code,
                 "learn/%s/index.html" % INDIAN.get(code, ""),
                 "languages/%s/index.html" % code):
        if cand and "//" not in cand and os.path.exists(cand):
            return cand
    return ""


def lang_targets(code):
    """Every page this language really has — never a link that 404s.

    The catalogue has 39 languages; ten of them (the world courses) carry
    languages/<code>/{course,practice,quiz,review}/, the ten Indian ones live
    under learn/<slug>/, others have only a starter page, and eleven have
    nothing but the level pages this tool writes. Hard-coding any one shape
    would have put dead links on 273 pages."""
    slug = INDIAN.get(code, "")

    def first(*cands):
        for c in cands:
            if c and "//" not in c and os.path.exists(c):
                return c
        return ""
    return {
        "course": first("languages/%s/course/index.html" % code,
                        "learn/%s/index.html" % slug,
                        "languages/%s/index.html" % code),
        "practice": first("languages/%s/practice/index.html" % code,
                          "learn/%s/practice/index.html" % slug),
        "quiz": first("languages/%s/quiz/index.html" % code,
                      "learn/%s/quiz/index.html" % slug),
        "review": first("languages/%s/review/index.html" % code,
                        "learn/%s/review/index.html" % slug),
    }


def href_of(path):
    """A site path ('learn/bengali/index.html') as a URL ('/learn/bengali/')."""
    if not path:
        return ""
    return "/" + (path[:-len("index.html")] if path.endswith("index.html") else path)


# ---------------------------------------------------------------------------
# page furniture
# ---------------------------------------------------------------------------

def rail(code, levels, current):
    items = []
    for lv in levels:
        cur = ' aria-current="page"' if lv == current else ""
        items.append('<li><a href="../%s/"%s>%s</a></li>' % (lv.lower(), cur, lv))
    return ('<nav aria-label="Levels of this course"><ul class="lv-rail">'
            + "".join(items) + "</ul></nav>")


def figure_html(code, rung_id, figs, rung=None, tail=""):
    """The level's own figure — the same picture the hub and the ladder show."""
    fig = figs.get("%s-%s" % (code, rung_id))
    if not fig:
        return ""
    rung = rung or {}
    caption = ("%s — on the ladder this level is %s, age %s: by the end of it "
               "the learner can %s."
               % (_clean(rung.get("label", fig.get("label", ""))),
                  _clean(rung.get("who", "a learner")), fig.get("age", ""),
                  _clean(rung.get("can", "read and speak a little")).rstrip(".")))
    return ('<figure class="lv-fig"><img src="../../../%s" width="320" height="200" '
            'loading="lazy" decoding="async" alt="%s"><figcaption>%s%s</figcaption></figure>'
            % (fig.get("path", ""), _clean(fig.get("alt", "")), caption,
               (" " + tail) if tail else ""))


def vocab_table(items, lang="und"):
    if not items:
        return ""
    rows = []
    for v in items:
        rows.append('<tr><td data-h="%s" lang="%s" dir="auto"><b>%s</b></td>'
                    '<td data-h="%s">%s</td><td data-h="%s">%s</td></tr>'
                    % ("Word", _clean(lang), _clean(v.get("t", "")),
                       "Say it", _clean(v.get("r", "")),
                       "Meaning", _clean(v.get("en", ""))))
    return ('<div class="lv-wrap"><table><thead><tr><th>Word</th><th>Say it</th>'
            "<th>Meaning</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>")


def dialogue_table(lines, lang="und"):
    if not lines:
        return ""
    rows = []
    for ln in lines:
        rows.append('<tr><td data-h="Who"><b>%s</b></td>'
                    '<td data-h="Line" lang="%s" dir="auto">%s</td>'
                    '<td data-h="Say it">%s</td><td data-h="English">%s</td></tr>'
                    % (_clean(ln.get("sp", "")), _clean(lang), _clean(ln.get("t", "")),
                       _clean(ln.get("r", "")), _clean(ln.get("en", ""))))
    return ('<div class="lv-wrap"><table><thead><tr><th>Who</th><th>Line</th>'
            "<th>Say it</th><th>English</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table></div>")


def grammar_box(g, lang="und"):
    if not g:
        return ""
    out = ['<div class="lv-gram"><b>%s</b><p>%s</p>'
           % (_clean(g.get("title", "")), _clean(g.get("explain", "")))]
    if g.get("pattern"):
        out.append('<span class="pat">%s</span>' % _clean(g["pattern"]))
    if g.get("examples"):
        out.append(vocab_table(g["examples"], lang))
    mis = g.get("mistakes")
    if isinstance(mis, (list, tuple)):
        mis = [m for m in mis if m]
        if mis:
            out.append('<div class="mis"><b>Watch out:</b><ul>%s</ul></div>'
                       % "".join("<li>%s</li>" % _clean(m) for m in mis))
    elif mis:
        out.append('<p class="mis"><b>Watch out:</b> %s</p>' % _clean(mis))
    out.append("</div>")
    return "".join(out)


def practice_item(item, n):
    tag = TYPE_LABEL.get(item.get("type", ""), str(item.get("type", "")).replace("_", " "))
    out = ['<li class="lv-q"><p><span class="tag">%s</span>%s</p>'
           % (_clean(tag), _clean(item.get("q", "")))]
    opts = item.get("options") or []
    if opts:
        out.append('<ol type="a">' + "".join("<li>%s</li>" % _clean(o) for o in opts) + "</ol>")
    if item.get("audio_source"):
        out.append('<p class="tag">audio drill — play it in the course player</p>')
    if item.get("answer"):
        out.append('<details><summary>Show the answer</summary><p class="ans" dir="auto">%s</p>'
                   "</details>" % _clean(item["answer"]))
    out.append("</li>")
    return "".join(out)


def quiz_item(item):
    opts = item.get("options") or []
    ans = item.get("answer")
    if isinstance(ans, int) and 0 <= ans < len(opts):
        ans_text = opts[ans]
    else:
        ans_text = ans
    out = ['<li class="lv-q"><p><span class="tag">quick check</span>%s</p>' % _clean(item.get("q", ""))]
    if opts:
        out.append('<ol type="a">' + "".join("<li>%s</li>" % _clean(o) for o in opts) + "</ol>")
    out.append('<details><summary>Show the answer</summary><p class="ans" dir="auto">%s</p>'
               % _clean(ans_text or ""))
    if item.get("why"):
        out.append("<p>%s</p>" % _clean(item["why"]))
    out.append("</details></li>")
    return "".join(out)


def worksheet_block(ws):
    tasks = (ws or {}).get("tasks") or []
    if not tasks:
        return ""
    rows = []
    for t in tasks:
        rows.append('<tr><td data-h="Task">%s</td><td data-h="Prompts">%s</td>'
                    '<td data-h="Key">%s</td></tr>'
                    % (_clean(t.get("instruction", "")),
                       "<br>".join(_clean(i) for i in (t.get("items") or [])) or "—",
                       "<br>".join(_clean(k) for k in (t.get("key") or [])) or "—"))
    return ('<h4>Worksheet: %s</h4><div class="lv-wrap"><table><thead><tr><th>Task</th>'
            "<th>Prompts</th><th>Key</th></tr></thead><tbody>" + "".join(rows)
            + "</tbody></table></div>") % _clean((ws or {}).get("title", ""))


def drills_for(lesson, name):
    """Two asks per word — recognition and production. Re-ordering, not authoring."""
    out = []
    for v in (lesson.get("vocab") or []):
        out.append(("What does “%s” mean?" % v.get("t", ""), v.get("en", "")))
        if v.get("r"):
            out.append(("How do you say “%s” in %s?" % (v.get("en", ""), name),
                        "%s — say it “%s”" % (v.get("t", ""), v.get("r", ""))))
        else:
            out.append(("How do you say “%s” in %s?" % (v.get("en", ""), name), v.get("t", "")))
    return out


def drill_table(rows):
    body = "".join('<tr><td data-h="Ask">%s</td><td data-h="Answer" dir="auto">%s</td></tr>'
                   % (_clean(q), _clean(a)) for q, a in rows)
    return ('<div class="lv-wrap"><table><thead><tr><th>Ask</th><th>Answer</th></tr></thead>'
            "<tbody>" + body + "</tbody></table></div>")


def lessons_of(data):
    return [l for u in ((data or {}).get("level") or {}).get("units") or []
            for l in (u.get("lessons") or [])]


def counts_of(data, code, name):
    lessons = lessons_of(data)
    return {
        "units": len(((data or {}).get("level") or {}).get("units") or []),
        "lessons": len(lessons),
        "vocab": sum(len(l.get("vocab") or []) for l in lessons),
        "practice": sum(len(l.get("practice") or []) for l in lessons),
        "quiz": sum(len(l.get("quiz") or []) for l in lessons),
        "drills": sum(len(drills_for(l, name)) for l in lessons),
        "test": len((((data or {}).get("level") or {}).get("test") or {}).get("items") or []),
    }


# ---------------------------------------------------------------------------
# the level page
# ---------------------------------------------------------------------------

def level_page(code, course, level, data, rungmap, figs, levels):
    name = course["name"]
    lv = (data or {}).get("level") or {}
    units = lv.get("units") or []
    if not units:
        return None, "no units"

    n = counts_of(data, code, name)
    questions = n["practice"] + n["quiz"] + n["drills"] + n["test"]
    rung = rungmap.get(LEVEL_RUNG.get(level, level.lower()))
    targets = lang_targets(code)

    title = "%s %s — %s" % (name, level, lv.get("title", LEVEL_NAMES.get(level, level)))
    desc = ("%s at level %s (%s): %d lessons in %d units, %d words with romanisation, "
            "%d questions with answers including a %d-item level test — free, in your browser."
            % (name, level, LEVEL_NAMES.get(level, level), n["lessons"], n["units"],
               n["vocab"], questions, n["test"]))

    body = ['<div class="lv-main">']
    body.append('<h1 id="lv-h1">%s %s — %s</h1>'
                % (_clean(name), level, _clean(lv.get("title", LEVEL_NAMES.get(level, level)))))
    body.append(
        '<p class="lv-lede">The whole %s %s level as one readable page: %d units, %d lessons, '
        "%d words, %d questions with every answer shown, a worksheet and a %d-item level test. "
        "Nothing here is behind JavaScript, and nothing needs an account.</p>"
        % (name, level, n["units"], n["lessons"], n["vocab"], questions, n["test"]))
    if rung:
        body.append('<div class="note"><b>Who this level is for.</b> %s is one of the six CEFR '
                    "levels and the %s rung on this site’s ladder: the learner in the picture is "
                    "%s, because on this site age is the rung — the same learner grows up the "
                    "ladder as the language grows. By the end of it you can %s.</div>"
                    % (level, _clean(rung.get("label", level)), _clean(rung.get("who", "a learner")),
                       _clean(rung.get("can", "hold a simple conversation")).rstrip(".")))
    body.append(figure_html(code, LEVEL_RUNG.get(level, level.lower()), figs, rung=rung,
                            tail="The same figure is on the course hub and in "
                                 "<a href=\"/how-levels-work/\">how the eleven rungs work</a>."))
    body.append(rail(code, levels, level))

    goals = lv.get("goals") or []
    if goals:
        body.append("<h2>What you can do when %s is finished</h2><ul>%s</ul>"
                    % (level, "".join("<li>%s</li>" % _clean(g) for g in goals)))

    body.append("<h2>%s, unit by unit</h2>" % level)
    for u in units:
        body.append("<h3>%s</h3>" % _clean(u.get("title", u.get("id", ""))))
        for l in (u.get("lessons") or []):
            body.append('<h4 id="%s">%s</h4>'
                        % (_clean(l.get("id", "")).lower(), _clean(l.get("title", ""))))
            if l.get("learn"):
                body.append("<p>%s</p>" % _clean(l["learn"]))
            body.append(vocab_table(l.get("vocab"), code))
            body.append(grammar_box(l.get("grammar"), code))
            if l.get("dialogue"):
                body.append("<p><b>Dialogue.</b> Read it aloud twice — once for each speaker.</p>")
                body.append(dialogue_table(l["dialogue"], code))
            prac = l.get("practice") or []
            if prac:
                body.append("<p><b>Practice (%d).</b> Answer first, then open the answer.</p>"
                            % len(prac))
                seen, targets_list = set(), []
                for it in prac:
                    t = (it.get("skill_target") or "").strip()
                    if t and t not in seen:
                        seen.add(t); targets_list.append(t)
                if targets_list:
                    body.append('<p class="note"><b>What this practice tests.</b> %s</p>'
                                % _clean(" ".join(targets_list)))
                body.append('<ol class="prac">%s</ol>'
                            % "".join(practice_item(i, k) for k, i in enumerate(prac)))
            quiz = l.get("quiz") or []
            if quiz:
                body.append("<p><b>Quick check (%d).</b></p>" % len(quiz))
                body.append('<ol class="quiz">%s</ol>' % "".join(quiz_item(i) for i in quiz))
            body.append(worksheet_block(l.get("worksheet")))
            srs = l.get("srs_candidates") or []
            if srs:
                body.append('<p class="note"><b>Review list.</b> %s</p>'
                            % _clean(" · ".join(srs)))

    body.append("<h2>Recall drills — %d more questions from the %s words</h2>"
                % (n["drills"], level))
    body.append('<p class="note">These drills are generated from this level’s own vocabulary '
                "list, in both directions: recognition (word → meaning) and production "
                "(meaning → word). They re-ask what the course data already contains; no answer "
                "here was written by a machine, and a generated drill is practice, never a "
                "lesson.</p>")
    for u in units:
        rows = []
        for l in (u.get("lessons") or []):
            rows += drills_for(l, name)
        if rows:
            body.append('<details class="lv-drills"><summary>%s — %d drills</summary>%s</details>'
                        % (_clean(u.get("title", "")), len(rows), drill_table(rows)))

    test = (lv.get("test") or {}).get("items") or []
    if test:
        body.append("<h2>The %s test — %d items</h2>" % (level, len(test)))
        body.append("<p>The level test closes the level. Answers are shown; in the course player "
                    "the same test decides whether the next level unlocks.</p>")
        body.append('<ol class="test">%s</ol>' % "".join(practice_item(i, k) for k, i in enumerate(test)))

    nxt = NEXT_RUNG.get(level, "")
    nxt_rung = rungmap.get(nxt) if nxt else None
    i = levels.index(level) if level in levels else -1
    nxt_level = levels[i + 1] if 0 <= i < len(levels) - 1 else ""
    if nxt_rung:
        body.append('<h2 id="checkpoint">After %s: the %s checkpoint</h2>'
                    % (level, _clean(nxt_rung["label"])))
        body.append("<p>%s is not a certificate — it is the half-step between this level and the "
                    "next one, and it is on this site’s ladder because language schools use it. "
                    "You are at %s when you can %s. Get there by working the recall drills above "
                    "and the review deck until nothing on this page surprises you%s.</p>"
                    % (_clean(nxt_rung["label"]), _clean(nxt_rung["label"]),
                       _clean(nxt_rung.get("can", "the level feels easy")).rstrip("."),
                       (", then open the <a href=\"../%s/\">%s pages</a>" % (nxt_level.lower(), nxt_level))
                       if nxt_level else ""))

    cards = []
    if targets["practice"]:
        cards.append('<div class="lv-card"><b>Practice lab</b><span>Quiz, typing, worksheets and '
                     "conversation scenarios for %s.</span><a href=\"%s\">Open the labs</a></div>"
                     % (_clean(name), href_of(targets["practice"])))
    if targets["quiz"]:
        cards.append('<div class="lv-card"><b>Topic quiz</b><span>Multiple-choice questions from '
                     'this course, with explanations.</span><a href="%s">Take the quiz</a></div>'
                     % href_of(targets["quiz"]))
    if targets["review"]:
        cards.append('<div class="lv-card"><b>Review deck</b><span>The core words ticked off until '
                     'they stick.</span><a href="%s">Open the deck</a></div>'
                     % href_of(targets["review"]))
    if targets["course"]:
        cards.append('<div class="lv-card"><b>Course pages</b><span>This language’s own pages — '
                     "alphabet, lessons and starter pack.</span><a href=\"%s\">Open the course</a>"
                     "</div>" % href_of(targets["course"]))
    cards.append('<div class="lv-card"><b>All levels</b><span>The ladder for %s: six levels and '
                 "the half-steps between them.</span><a href=\"../\">See every level</a></div>"
                 % _clean(name))
    cards.append('<div class="lv-card"><b>Play this level</b><span>Keeps score and unlocks the next '
                 'level on this device.</span><a href="/courses/#/%s/%s">Open the player</a></div>'
                 % (code, level.lower()))
    body.append("<h2>Keep going</h2>")
    body.append('<div class="lv-cards">%s</div>' % "".join(cards))

    body.append("</div>")

    parent = href_of(targets["course"]) or "/languages/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Course", "@id": "%s/languages/%s/level/%s/#course" % (BASE, code, level.lower()),
         "name": title, "description": desc,
         "url": "%s/languages/%s/level/%s/" % (BASE, code, level.lower()),
         "inLanguage": code, "educationalLevel": level, "isAccessibleForFree": True,
         "provider": {"@type": "Organization", "name": "EkGuru", "url": BASE + "/"},
         "teaches": [g for g in goals][:6]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "EkGuru", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": BASE + parent},
            {"@type": "ListItem", "position": 3, "name": "%s levels" % name,
             "item": "%s/languages/%s/level/" % (BASE, code)},
            {"@type": "ListItem", "position": 4, "name": "%s %s" % (name, level),
             "item": "%s/languages/%s/level/%s/" % (BASE, code, level.lower())},
        ]},
    ]}
    body.append('<script type="application/ld+json">%s</script>'
                % json.dumps(ld, ensure_ascii=False, separators=(",", ":")))

    url = "languages/%s/level/%s/" % (code, level.lower())
    crumb = ('<a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › '
             '<a href="%s">%s</a> › <a href="/languages/%s/level/">Levels</a> › %s'
             % (parent, _clean(name), code, level))
    return (title, desc, url, crumb, "".join(body)), None


# ---------------------------------------------------------------------------
# the ladder page for one language
# ---------------------------------------------------------------------------

def ladder_page(code, course, levels, loaded, rungmap, figs):
    name = course["name"]
    targets = lang_targets(code)
    body = ['<div class="lv-main">']
    body.append('<h1 id="lv-h1">%s levels — all six, A1 to C2</h1>' % _clean(name))
    body.append('<p class="lv-lede">%s runs the same six levels as every other course here, and '
                "the same eleven rungs as the rest of the site. Below is the whole ladder for %s: "
                "what each level holds, how many questions are in it, and who the learner in the "
                "picture is — a child at the first rung, an elder by the last.</p>"
                % (_clean(name), _clean(name)))

    total = dict(lessons=0, vocab=0, questions=0)
    cards = []
    for lv, data in zip(levels, loaded):
        if data is None:
            continue
        n = counts_of(data, code, name)
        total["lessons"] += n["lessons"]
        total["vocab"] += n["vocab"]
        total["questions"] += n["practice"] + n["quiz"] + n["drills"] + n["test"]
        cards.append(
            '<div class="lv-card"><b><a href="%s/">%s · %s</a></b>'
            "<span>%s</span><span>%d lessons · %d words · %d questions</span></div>"
            % (lv.lower(), lv, _clean(((data.get("level") or {}).get("title") or LEVEL_NAMES.get(lv, lv))),
               _clean((rungmap.get(LEVEL_RUNG.get(lv, "")) or {}).get("can", "")),
               n["lessons"], n["vocab"], n["practice"] + n["quiz"] + n["test"]))
    body.append('<p class="note"><b>The whole course, counted.</b> %d lessons, %d words with '
                "romanisation and %d questions with answers — every one of them readable on the "
                "level pages below.</p>" % (total["lessons"], total["vocab"], total["questions"]))

    body.append("<h2>The six levels</h2>")
    body.append('<div class="lv-cards">%s</div>' % "".join(cards))

    body.append("<h2>The eleven rungs, in pictures</h2>")
    body.append("<p>CEFR has six levels. This site also names the half-step after each of the "
                "first five — A1+, A2+, B1+, B2+, C1+ — because that is the honest label for the "
                "learner who has finished the lessons but is not yet ready for the next level. "
                "There is no A3 and no C3–C5; a page that prints them is a page an examiner stops "
                "trusting. <a href=\"/how-levels-work/\">The full explanation is here.</a></p>")
    cells = []
    for rid, r in rungmap.items():
        fig = figs.get("%s-%s" % (code, rid))
        if not fig:
            continue
        cells.append('<figure><img src="../../../%s" width="320" height="200" loading="lazy" '
                     'decoding="async" alt="%s"><figcaption><b>%s</b> %s · age %s</figcaption>'
                     "</figure>"
                     % (fig["path"], _clean(fig.get("alt", "")), _clean(r.get("label", rid)),
                        _clean(r.get("who", "")), fig.get("age", "")))
    if cells:
        body.append('<div class="lv-grid">%s</div>' % "".join(cells))

    cards = ['<div class="lv-card"><b>Not sure of your level?</b><span>Five questions, then a '
             'starting point.</span><a href="/start/">Find my level</a></div>']
    if targets["practice"]:
        cards.append('<div class="lv-card"><b>Practice lab</b><span>Quiz, typing, worksheets, '
                     'conversation.</span><a href="%s">Open the labs</a></div>'
                     % href_of(targets["practice"]))
    if targets["course"]:
        cards.append('<div class="lv-card"><b>Course pages</b><span>Alphabet, lessons and the '
                     "course home for %s.</span><a href=\"%s\">Open the course</a></div>"
                     % (_clean(name), href_of(targets["course"])))
    cards.append('<div class="lv-card"><b>Course player</b><span>Progress, scoring, unlocking — '
                 'kept on your own device.</span><a href="/courses/#/%s/a1">Open the player</a>'
                 "</div>" % code)
    cards.append('<div class="lv-card"><b>Levels across the site</b><span>How the ladder works, '
                 'and what every rung means.</span><a href="/how-levels-work/">The ladder</a>'
                 "</div>")
    body.append("<h2>Where to start</h2>")
    body.append('<div class="lv-cards">%s</div>' % "".join(cards))

    body.append("</div>")

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": "%s/languages/%s/level/#page" % (BASE, code),
         "name": "%s levels — A1 to C2" % name,
         "description": "%s levels: %d lessons, %d words and %d questions with answers across the "
                        "six levels." % (name, total["lessons"], total["vocab"], total["questions"]),
         "url": "%s/languages/%s/level/" % (BASE, code), "inLanguage": "en"},
        {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": "%s %s" % (name, lv),
             "url": "%s/languages/%s/level/%s/" % (BASE, code, lv.lower())}
            for i, lv in enumerate(levels)]},
    ]}
    body.append('<script type="application/ld+json">%s</script>'
                % json.dumps(ld, ensure_ascii=False, separators=(",", ":")))

    title = "%s levels — A1 to C2, lesson by lesson" % name
    desc = ("Every %s level in full: %d lessons, %d words with romanisation and %d questions with "
            "answers, from A1 to C2." % (name, total["lessons"], total["vocab"], total["questions"]))
    url = "languages/%s/level/" % code
    crumb = ('<a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › '
             '<a href="%s">%s</a> › Levels'
             % (href_of(targets["course"]) or "/languages/", _clean(name)))
    return title, desc, url, crumb, "".join(body)


# ---------------------------------------------------------------------------
# the rail on the parent hub
# ---------------------------------------------------------------------------

def rail_block(code, course, levels, loaded):
    rows = []
    for lv, data in zip(levels, loaded):
        n = counts_of(data, code, course["name"])
        rows.append('<li><a href="/languages/%s/level/%s/"><b>%s</b> %s'
                    "<span>%d lessons · %d questions</span></a></li>"
                    % (code, lv.lower(), lv, _clean(((data or {}).get("level") or {}).get("title", "")),
                       n["lessons"], n["practice"] + n["quiz"] + n["test"]))
    return (RAIL_START + "\n"
            '<section class="lv-levels" aria-labelledby="lv-levels-h">\n'
            '<h2 id="lv-levels-h">This course, level by level, in plain HTML</h2>\n'
            "<p>The player above keeps your progress; these pages keep the content. Every level of "
            "the %s course — its lessons, vocabulary, grammar, dialogues, practice questions, quiz, "
            "worksheet and level test, with all the answers — is also a page you can read without "
            "JavaScript, print, or link to. "
            '<a href="/languages/%s/level/">The %s ladder in full →</a></p>\n'
            '<ul class="lv-level-list">%s</ul>\n'
            "</section>\n" % (_clean(course["name"]), code, _clean(course["name"]), "".join(rows))
            + RAIL_END + "\n")


RAIL_STYLE = """
.lv-level-list{list-style:none;padding:0;margin:14px 0 0;display:grid;
  grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.lv-level-list li{margin:0}
.lv-level-list a{display:block;border:1px solid var(--line);border-radius:12px;
  padding:12px 14px;text-decoration:none;background:#fff}
.lv-level-list a b{display:block;font-size:1rem}
.lv-level-list a span{display:block;color:var(--muted);font-size:.85rem;margin-top:3px}
.lv-levels{margin:26px 0 0}
"""


def splice_rail(path, block, check):
    """Put the rail into the hub, between markers this tool owns."""
    if not os.path.exists(path):
        return "missing"
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if RAIL_START in html and RAIL_END in html:
        start = html.index(RAIL_START)
        end = html.index(RAIL_END) + len(RAIL_END)
        out = html[:start] + block.rstrip("\n") + html[end:]
    else:
        # A fresh hub: the block goes in before the level-visuals strip (written
        # by tools/build-visuals.py, which owns the end of <main>).
        for anchor in ("<!-- ekguru:level-visuals:start -->", "</main>"):
            if anchor in html:
                out = html.replace(anchor, block + anchor, 1)
                break
        else:
            return "no anchor"
    if ".lv-level-list" not in out and "</style>" in out:
        out = out.replace("</style>", RAIL_STYLE + "</style>", 1)
    if out == html:
        return "ok"
    if check:
        print("STALE: %s needs tools/build-course-levels.py" % path)
        return "stale"
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    return "wrote"


# ---------------------------------------------------------------------------
# the sitemap
# ---------------------------------------------------------------------------

def update_sitemap(urls, check):
    stamp = time.strftime("%Y-%m-%d", time.gmtime())
    body = "\n".join('  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n'
                     "    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>"
                     % (u, stamp) for u in urls)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<!-- Generated by tools/build-course-levels.py — do not hand-edit. -->\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n")
    old = open(SITEMAP, encoding="utf-8").read() if os.path.exists(SITEMAP) else ""
    stale = []
    if old != xml:
        if check:
            stale.append(SITEMAP)
            print("STALE: %s needs tools/build-course-levels.py" % SITEMAP)
        else:
            with open(SITEMAP, "w", encoding="utf-8") as f:
                f.write(xml)
            print("sitemap: %s (%d URLs)" % (SITEMAP, len(urls)))
    with open(INDEX, encoding="utf-8") as f:
        idx = f.read()
    if "<loc>%s/%s</loc>" % (BASE, SITEMAP) not in idx:
        entry = ("  <sitemap>\n    <loc>%s/%s</loc>\n    <lastmod>%s</lastmod>\n"
                 "  </sitemap>\n" % (BASE, SITEMAP, stamp))
        if check:
            print("STALE: %s is missing %s" % (INDEX, SITEMAP))
            stale.append(INDEX)
        else:
            with open(INDEX, "w", encoding="utf-8") as f:
                f.write(idx.replace("</sitemapindex>", entry + "</sitemapindex>", 1))
            print("sitemap: %s declared in %s" % (SITEMAP, INDEX))
    return stale


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    check = "--check" in sys.argv
    only = sys.argv[sys.argv.index("--lang") + 1] if "--lang" in sys.argv else ""

    courses, levels = catalogue()
    rungmap, figs = rungs(), figures()
    if not courses or not rungmap:
        raise SystemExit("ERROR: catalogue or level ladder unreadable")

    pages, stale, rails, problems = 0, [], {"wrote": 0, "ok": 0}, []
    site_urls = []

    for course in courses:
        code = course["code"]
        if only and code != only:
            continue
        phase = course.get("phase") or "phase-1"
        loaded = []
        for lv in levels:
            data = level_data(code, phase, lv)
            if data is None:
                problems.append("%s %s: no data file" % (code, lv))
            loaded.append(data)

        title, desc, url, crumb, body = ladder_page(code, course, levels, loaded, rungmap, figs)
        pages += emit("languages/%s/level/index.html" % code,
                      compose("../../../", title, desc, url, crumb, body), check, stale)
        site_urls.append("%s/%s" % (BASE, url))

        for lv, data in zip(levels, loaded):
            if data is None:
                continue
            made, why = level_page(code, course, lv, data, rungmap, figs, levels)
            if made is None:
                problems.append("%s %s: %s" % (code, lv, why))
                continue
            title, desc, url, crumb, body = made
            pages += emit("languages/%s/level/%s/index.html" % (code, lv.lower()),
                          compose("../../../", title, desc, url, crumb, body), check, stale)
            site_urls.append("%s/%s" % (BASE, url))

        hub = hub_for(code)
        if hub:
            r = splice_rail(hub, rail_block(code, course, levels, loaded), check)
            if r in ("wrote", "ok"):
                rails[r] += 1
            elif r == "stale":
                stale.append(hub)
            else:
                problems.append("%s: hub %s" % (code, r))
        # else: no hub page exists for this language yet. The /courses/
        # catalogue links its level pages, so nothing is orphaned.

    # Only a full run may rewrite the sitemap: a --lang run would otherwise
    # declare one language's pages and drop the other 38 from the file.
    if not only:
        stale += update_sitemap(sorted(site_urls), check)

    for p in problems:
        print("problem: %s" % p)
    print("levels: %d page(s) written · rails %d written / %d current · %d stale"
          % (pages, rails["wrote"], rails["ok"], len(set(stale))))
    if problems:
        return 1
    return 1 if (check and stale) else 0


if __name__ == "__main__":
    sys.exit(main())

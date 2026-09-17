#!/usr/bin/env python3
"""Phase 7C §9 — build the NORMALIZED GLOBAL CONTENT GRAPH from real content.

Extracts every real content entity already on the site into one normalized,
machine-readable graph with stable IDs (schema: reports/global-content-schema-phase7.json):

  lesson       learn/<slug>/ (15) + materials/<cat>/<topic>/ (16) + daily-hindi/<day>/ (31)
  quiz         js/hindi-quiz-bank.js (45 questions)
  practice     js/practice-bank.js (vocabulary / grammar / verbs drills)
  phrase       toolbox/hindi-phrasebook (69 phrases, 8 categories)
  review_card  derived from the SRS starter deck source (quiz bank + practice vocab)
  grammar      grammar guides (materials/grammar/* + grammar lessons)
  pronunciation  pronunciation/alphabet guides
  culture      culture/daily-life content

Outputs:
  data/content-graph.json   — canonical normalized data (source of truth)
  js/content-graph.js       — query ENGINE only (no data copy): fetch + index + query

No fabricated content: every entity traces to an existing file/URL.
"""
import json, os, re, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

SRC = "en"          # source language (learner-facing)
TGT = "hi"          # target language (Hindi reference implementation)
STATUS = "PRODUCTION"

def slug_id(typ, slug):
    return "%s:%s" % (typ, slug)

def h1_of(path):
    try:
        h = open(path, encoding="utf-8").read()
        m = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", h)
        if m:
            return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    except Exception:
        pass
    return None

def load_js_object(path, varname):
    """Load a `window.X = {...};` data file via node (handles JS object-literal
    syntax: bare keys, comments, curly quotes) and return a Python dict."""
    import subprocess
    varname = varname.replace("window.", "").replace("\\.", "")
    js = (
        "const fs=require('fs'); global.window={}; "
        "eval(fs.readFileSync(process.argv[1],'utf8')); "
        "process.stdout.write(JSON.stringify(window[process.argv[2]]));"
    )
    try:
        out = subprocess.run(["node", "-e", js, path, varname],
                             capture_output=True, text=True, timeout=30)
        if out.returncode != 0 or not out.stdout.strip():
            raise RuntimeError(out.stderr[:200])
        return json.loads(out.stdout)
    except Exception as e:
        raise RuntimeError("load_js_object(%s) failed: %s" % (path, e))

graph = {"version": 1, "generated": NOW,
         "source_language": SRC, "target_language": TGT, "entities": []}
ent = graph["entities"]
seen = set()

def add(e):
    if e["id"] in seen:
        return
    seen.add(e["id"])
    ent.append(e)

def base(typ, slug, title, level="beginner", topic=None, url=None):
    return {
        "id": slug_id(typ, slug), "type": typ, "slug": slug, "title": title,
        "source_language": SRC, "target_language": TGT, "level": level,
        "topic": topic, "status": STATUS, "url": url,
        "version": 1, "source": url or ("js/" + slug),
    }

# ---- 1. lessons: learn/<slug>/ ----
LEARN_SLUGS = ["aap-tum-tu-hindi", "common-hindi-mistakes", "hindi-alphabet-for-beginners",
               "hindi-days-months-time", "hindi-family-words", "hindi-gender-masculine-feminine",
               "hindi-numbers-1-to-100", "hindi-or-urdu-difference", "hindi-phrases-for-travel",
               "hindi-sentence-structure", "hindi-verbs-present-past-future",
               "how-to-say-hello-in-hindi", "learn-hindi-from-bollywood",
               "learn-hindi-online-guide", "write-your-name-in-hindi"]
LEARN_TOPIC = {
    "aap-tum-tu-hindi": "register", "common-hindi-mistakes": "grammar",
    "hindi-alphabet-for-beginners": "script", "hindi-days-months-time": "time",
    "hindi-family-words": "family", "hindi-gender-masculine-feminine": "grammar",
    "hindi-numbers-1-to-100": "numbers", "hindi-or-urdu-difference": "culture",
    "hindi-phrases-for-travel": "travel", "hindi-sentence-structure": "grammar",
    "hindi-verbs-present-past-future": "grammar", "how-to-say-hello-in-hindi": "greetings",
    "learn-hindi-from-bollywood": "culture", "learn-hindi-online-guide": "meta",
    "write-your-name-in-hindi": "script",
}
for slug in LEARN_SLUGS:
    url = "https://ekguru.shop/learn/%s/" % slug
    title = h1_of("learn/%s/index.html" % slug) or slug.replace("-", " ").title()
    e = base("lesson", slug, title, level="beginner", topic=LEARN_TOPIC.get(slug), url=url)
    e["section"] = "learn"
    add(e)

# ---- 2. materials/<cat>/<topic>/ ----
for cat in sorted(os.listdir("materials")):
    cdir = os.path.join("materials", cat)
    if not os.path.isdir(cdir):
        continue
    for topic in sorted(os.listdir(cdir)):
        tdir = os.path.join(cdir, topic)
        if not os.path.isdir(tdir):
            continue
        slug = "%s-%s" % (cat, topic)
        url = "https://ekguru.shop/materials/%s/%s/" % (cat, topic)
        title = h1_of(os.path.join(tdir, "index.html")) or slug.replace("-", " ").title()
        e = base("lesson", slug, title, level="beginner", topic=cat, url=url)
        e["section"] = "materials"
        add(e)

# ---- 3. daily-hindi/<day>/ ----
for day in sorted(os.listdir("daily-hindi"), key=lambda x: int(re.sub(r"\D", "", x) or 0)):
    ddir = os.path.join("daily-hindi", day)
    if not os.path.isdir(ddir):
        continue
    url = "https://ekguru.shop/daily-hindi/%s/" % day
    title = h1_of(os.path.join(ddir, "index.html")) or day.replace("-", " ").title()
    e = base("lesson", day, title, level="beginner", topic="daily-life", url=url)
    e["section"] = "daily-hindi"
    add(e)

# ---- 4. quizzes ----
quiz = load_js_object("js/hindi-quiz-bank.js", "EKGURU_HINDI_QUIZ")
quiz_count = 0
if quiz and "questions" in quiz:
    for q in quiz["questions"]:
        e = base("quiz", q["id"], q["q"][:80], level=q.get("level", "beginner"),
                 topic=q.get("topic"), url="https://ekguru.shop/learn/hindi/practice/quiz/")
        e.update({"prompt": q["q"], "answer": q["a"], "options": q["opts"],
                  "explanation": q["explain"], "qtype": q.get("type"), "lesson": q.get("lesson")})
        add(e)
        quiz_count += 1

# ---- 5. practice drills ----
practice = load_js_object("js/practice-bank.js", "EKGURU_PRACTICE_BANK")
practice_count = 0
if practice:
    for section, items in practice.items():
        if not isinstance(items, list):
            continue
        for i, it in enumerate(items):
            slug = "hi-%s-%d" % (section, i + 1)
            e = base("practice", slug, it.get("q", "")[:80], level="beginner",
                     topic=section, url="https://ekguru.shop/learn/practice/vocabulary/")
            e.update({"prompt": it.get("q"), "answer": it.get("a"),
                      "options": it.get("opts"), "explanation": it.get("explain"),
                      "drill_section": section})
            add(e)
            practice_count += 1

# ---- 6. phrases ----
ph = open("toolbox/hindi-phrasebook/index.html", encoding="utf-8").read()
phrase_rows = re.findall(r'<tr data-cat="([^"]+)"[^>]*>\s*<td>([\s\S]*?)</td>\s*<td class="dv">([\s\S]*?)</td>\s*<td>([\s\S]*?)</td>\s*<td>([\s\S]*?)</td>\s*</tr>', ph)
for i, (cat, en, hi, rom, note) in enumerate(phrase_rows):
    clean = lambda s: re.sub(r"<[^>]+>", "", s).strip()
    slug = "hi-phrase-%s-%d" % (cat, i + 1)
    e = base("phrase", slug, clean(en)[:80], level="beginner", topic=cat,
             url="https://ekguru.shop/toolbox/hindi-phrasebook/")
    e.update({"target_text": clean(hi), "romanization": clean(rom),
              "meaning": clean(en), "usage_note": clean(note)})
    add(e)

# ---- 7. review cards (SRS starter-deck source: quiz bank + practice vocab) ----
# js/hindi-srs.js seeds the starter deck from quiz questions + practice vocabulary.
rc = 0
if quiz and "questions" in quiz:
    for q in quiz["questions"]:
        e = base("review_card", "rc-quiz-" + q["id"], q["q"][:80], level=q.get("level", "beginner"),
                 topic=q.get("topic"), url="https://ekguru.shop/learn/hindi/review/")
        e.update({"prompt": q["q"], "answer": q["a"], "category": q.get("topic", "quiz")})
        add(e)
        rc += 1
if practice and isinstance(practice.get("vocabulary"), list):
    for i, it in enumerate(practice["vocabulary"]):
        e = base("review_card", "rc-vocab-%d" % (i + 1), it.get("q", "")[:80],
                 level="beginner", topic="vocabulary", url="https://ekguru.shop/learn/hindi/review/")
        e.update({"prompt": it.get("q"), "answer": it.get("a"), "category": "vocabulary"})
        add(e)
        rc += 1

# ---- 8. grammar entities (guides) ----
GRAMMAR = {"materials-grammar-beginner-grammar-reference": "beginner",
           "materials-grammar-postpositions": "beginner",
           "materials-grammar-sentence-patterns": "elementary",
           "hindi-sentence-structure": "beginner",
           "hindi-gender-masculine-feminine": "elementary",
           "hindi-verbs-present-past-future": "elementary"}
for gslug, lvl in GRAMMAR.items():
    title = None
    if gslug.startswith("materials-"):
        parts = gslug.split("-", 1)[1]
        cat, topic = parts.split("-", 1)
        title = h1_of("materials/%s/%s/index.html" % (cat, topic))
    else:
        title = h1_of("learn/%s/index.html" % gslug)
    if not title:
        continue
    e = base("grammar", gslug, title, level=lvl, topic="grammar")
    add(e)

# ---- 9. pronunciation entities ----
PRON = {"materials-pronunciation-pronunciation-guide": "beginner",
        "materials-alphabet-devanagari-chart": "beginner",
        "hindi-alphabet-for-beginners": "beginner"}
for pslug, lvl in PRON.items():
    title = None
    if pslug.startswith("materials-"):
        cat, topic = pslug.split("-", 1)[1].split("-", 1)
        title = h1_of("materials/%s/%s/index.html" % (cat, topic))
    else:
        title = h1_of("learn/%s/index.html" % pslug)
    if not title:
        continue
    e = base("pronunciation", pslug, title, level=lvl, topic="pronunciation")
    add(e)

# ---- 10. culture entities ----
CULTURE = {"materials-conversation-polite-vs-casual": "beginner",
           "hindi-or-urdu-difference": "elementary",
           "learn-hindi-from-bollywood": "intermediate",
           "materials-family-family-words-quick-ref": "beginner"}
for cslug, lvl in CULTURE.items():
    title = None
    if cslug.startswith("materials-"):
        cat, topic = cslug.split("-", 1)[1].split("-", 1)
        title = h1_of("materials/%s/%s/index.html" % (cat, topic))
    else:
        title = h1_of("learn/%s/index.html" % cslug)
    if not title:
        continue
    e = base("culture", cslug, title, level=lvl, topic="culture")
    add(e)

# ---- summary ----
by_type = {}
for e in ent:
    by_type[e["type"]] = by_type.get(e["type"], 0) + 1

os.makedirs("data", exist_ok=True)
with open("data/content-graph.json", "w", encoding="utf-8") as f:
    json.dump(graph, f, ensure_ascii=False, separators=(",", ":"))

print("content graph entities:", len(ent), dict(sorted(by_type.items())))
print("  quiz:", quiz_count, "| practice:", practice_count,
      "| phrases:", len(phrase_rows), "| review cards:", rc)

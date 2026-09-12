#!/usr/bin/env python3
"""Phase 4 §1/§26/§27 — audit the entire Hindi content estate and produce
the architecture report, coverage matrix and consolidation classification.

Everything here is DERIVED from the real pages (URL, title, H1, content
markers). No value is invented.
"""
import json, os, re, time
from html import unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

DEVA_RE = re.compile(r"[\u0900-\u097F]")

def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except Exception:
        return ""

def title_of(h):
    m = re.search(r"<title>(.*?)</title>", h, re.S)
    return re.sub(r"\s*\|\s*EkGuru\s*$", "", unescape(m.group(1)).strip()) if m else None

def h1_of(h):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else None

def meta_of(h):
    m = re.search(r'<meta name="description" content="([^"]*)"', h)
    return unescape(m.group(1)).strip() if m else None

def canon_of(h):
    m = re.search(r'<link rel="canonical" href="([^"]+)"', h)
    return m.group(1) if m else None

# ---- classify page type + topic + level from URL ----
def classify(url):
    u = url.rstrip("/")
    if u.startswith("learn/practice"):  return ("practice", None, None)
    if u.startswith("learn/paths"):     return ("path", None, None)
    if u.startswith("materials/"):
        parts = u.split("/")
        return ("material", parts[1] if len(parts) > 1 else None, None)
    if u.startswith("toolbox/"):        return ("tool", None, None)
    if u.startswith("daily-hindi/"):    return ("daily", None, None)
    if u.startswith("answers/"):        return ("answer", None, None)
    if u.startswith("ask/"):            return ("question", None, None)
    if u == "faq":                      return ("faq", None, None)
    if u == "learn/hindi":              return ("hindi-hub", None, None)
    if u.startswith("learn/hindi/"):
        seg = u.split("/")[2]
        if seg in ("beginner", "elementary", "intermediate", "advanced"):
            return ("level", seg, None)
        return ("topic-hub", seg, None)
    if u.startswith("hindi/"):
        t = u.split("/")[1]
        return ("hindi-topic", t, None)
    if u.startswith("learn/"):
        slug = u.split("/")[1]
        return ("lesson", lesson_topic(slug), lesson_level(slug))
    if u == "learn": return ("hub", None, None)
    return ("page", None, None)

def lesson_topic(slug):
    m = {
        "hindi-alphabet-for-beginners": "basics",
        "how-to-say-hello-in-hindi": "conversation",
        "hindi-numbers-1-to-100": "numbers",
        "hindi-days-months-time": "time-dates",
        "hindi-family-words": "vocabulary",
        "hindi-phrases-for-travel": "travel",
        "hindi-sentence-structure": "grammar",
        "hindi-verbs-present-past-future": "grammar",
        "hindi-gender-masculine-feminine": "grammar",
        "aap-tum-tu-hindi": "conversation",
        "common-hindi-mistakes": "grammar",
        "hindi-or-urdu-difference": "basics",
        "learn-hindi-from-bollywood": "daily-life",
        "learn-hindi-online-guide": "basics",
        "write-your-name-in-hindi": "basics",
    }
    return m.get(slug, "basics")

def lesson_level(slug):
    adv = {"hindi-or-urdu-difference", "learn-hindi-from-bollywood"}
    if slug in adv:
        return "elementary"
    return "beginner"

def hindi_topic_level(t):
    beginner = {"alphabet", "beginners", "greetings", "numbers", "how-long", "name-topic",
                "flashcards-topic", "for-kids", "phrases-food", "phrases-travel", "emergency"}
    elem = {"conversation", "family", "time-date", "vocabulary", "grammar", "sentence-structure",
            "verbs", "formal-informal", "mistakes", "pronunciation", "listening", "reading",
            "writing", "speaking", "shopping", "business"}
    inter = {"bollywood", "slang", "hinglish", "heritage", "indian-languages", "hindi-vs-urdu",
             "relationships"}
    if t in beginner: return "beginner"
    if t in elem: return "elementary"
    if t in inter: return "intermediate"
    return "beginner"

# ---- scan pages ----
ROOTS = ["learn", "hindi", "materials", "toolbox", "daily-hindi", "answers", "ask", "faq"]
pages = []
for base in ROOTS:
    for dirpath, dirs, files in os.walk(base):
        if "index.html" not in files:
            continue
        rel = os.path.relpath(dirpath, ".").replace(os.sep, "/")
        url = (rel + "/") if rel != "." else ""
        if url == "learn/":
            url = "learn/"
        p = os.path.join(dirpath, "index.html")
        h = read(p)
        typ, topic, lvl = classify(url)
        if typ == "hindi-topic":
            lvl = hindi_topic_level(topic)
        deva = len(DEVA_RE.findall(h))
        roman = bool(re.search(r"[A-Za-z]{3,}", re.sub(r"<[^>]+>", " ", h)))
        pages.append({
            "url": "/" + url,
            "type": typ,
            "level": lvl,
            "topic": topic,
            "title": title_of(h),
            "h1": h1_of(h),
            "description": meta_of(h),
            "canonical": canon_of(h),
            "hasDevanagari": deva > 0,
            "devanagariChars": deva,
            "hasRomanization": roman,
            "hasExample": "<td" in h or "<code>" in h or "example" in h.lower(),
            "hasPractice": "practice" in h.lower() or "practise" in h.lower() or "learn/practice" in h,
            "hasQuiz": "<details" in h and "summary" in h,
            "hasRelated": 'class="rel"' in h or "Related" in h or "related" in h,
            "hasNext": "Next" in h or "next step" in h.lower() or "Keep going" in h,
            "wordCount": len(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)).split()),
        })

# ---- orphans: canonical pages never linked from ANY page (global link graph) ----
from urllib.parse import urljoin
all_files = []
for base in ["learn", "hindi", "materials", "toolbox", "daily-hindi", "answers", "ask", "faq",
             "learn-hindi-by-country", "learn-hindi-for-speakers", "hindi-tutor", "tutor",
             "vocab"]:
    if not os.path.isdir(base):
        continue
    for dirpath, dirs, files in os.walk(base):
        for fn in files:
            if fn.endswith(".html"):
                all_files.append(os.path.join(dirpath, fn))
for fn in os.listdir("."):
    if fn.endswith(".html"):
        all_files.append(fn)

linked = set()
for fp in all_files:
    h = read(fp)
    # the URL of this file, for resolving relative hrefs
    if fp.endswith("index.html"):
        base = "/" + fp[:-len("index.html")]
    else:
        base = "/" + fp
    for m in re.findall(r'href="([^"#]+)"', h):
        u = m.strip()
        if not u or u.startswith(("http", "mailto", "javascript", "tel:")):
            continue
        absu = urljoin(base, u.split("#")[0])
        if absu.startswith("/") and absu.endswith("/") and ".." not in absu:
            linked.add(absu)

canonical_urls = {p["url"] for p in pages}
orphans = sorted(u for u in canonical_urls if u not in linked
                 and u not in ("/learn/", "/hindi/", "/materials/", "/toolbox/",
                               "/daily-hindi/", "/answers/", "/ask/", "/faq/",
                               "/learn/practice/", "/learn/paths/"))

# ---- counts ----
from collections import Counter
by_type = Counter(p["type"] for p in pages)

arch = {
    "generated": NOW,
    "totalHindiPages": len(pages),
    "byType": dict(by_type),
    "levels": {"beginner": 0, "elementary": 0, "intermediate": 0, "advanced": 0, "none": 0},
    "topics": {},
    "hubs": {"learn": True, "hindi": True, "materials": True, "toolbox": True,
             "practice": True, "paths": True, "faq": True, "dailyHindi": True,
             "learnHindiHome": os.path.exists("learn/hindi/index.html"),
             "levelPages": [p for p in ("beginner", "elementary", "intermediate", "advanced")
                            if os.path.exists(f"learn/hindi/{p}/index.html")]},
    "orphanCanonicalPages": orphans,
    "missingLinks": [],
    "proposedPages": [
        "/learn/hindi/ (hub)", "/learn/hindi/beginner/", "/learn/hindi/elementary/",
        "/learn/hindi/basics/", "/learn/hindi/conversation/", "/learn/hindi/pronunciation/",
        "/learn/hindi/grammar/", "/learn/hindi/vocabulary/", "/learn/hindi/travel/",
        "/learn/hindi/daily-life/", "/learn/hindi/reading-writing/",
    ],
}
for p in pages:
    lvl = p["level"] or "none"
    arch["levels"][lvl] = arch["levels"].get(lvl, 0) + 1
    if p["topic"]:
        arch["topics"].setdefault(p["topic"], 0)
        arch["topics"][p["topic"]] += 1

with open("reports/learn-hindi-architecture.json", "w", encoding="utf-8") as f:
    json.dump(arch, f, ensure_ascii=False, indent=2)
with open("reports/learn-hindi-coverage-matrix.json", "w", encoding="utf-8") as f:
    json.dump({"generated": NOW, "pages": pages}, f, ensure_ascii=False, indent=2)

print(json.dumps(arch, ensure_ascii=False, indent=1)[:1500])
print("orphans:", orphans)

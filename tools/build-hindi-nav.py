#!/usr/bin/env python3
"""EkGuru Phase 4 — wire the canonical Learn Hindi structure into existing pages.

Does three jobs (all idempotent, rerunnable):
  1. Breadcrumbs — rewrite each lesson's visible breadcrumb + JSON-LD
     BreadcrumbList to the canonical chain:
     Home → Learn Hindi → Hindi → Level → Topic → Lesson (§20).
  2. Quick quiz — inject an original, fact-checked <details> quick quiz into
     the three exemplar lessons (alphabet / hello / sentence structure) so the
     13-section lesson standard (§7) is demonstrated where it matters most.
  3. Hub pointers — add a discoverable link to /learn/hindi/ from the
     /learn/ hub and the /hindi/ topic map (no header overload).

Single source of truth: imports LESSONS + TOPIC_META from build-hindi-structure.py.
Never hand-edit generated output — rerun this tool after changing the maps.

Run:  python3 tools/build-hindi-nav.py
"""
import importlib.util, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "https://ekguru.shop"

# load the structure builder's data (no side effects: main() is guarded)
spec = importlib.util.spec_from_file_location(
    "hindi_structure", os.path.join(ROOT, "tools", "build-hindi-structure.py"))
HS = importlib.util.module_from_spec(spec)
spec.loader.exec_module(HS)
LESSONS = HS.LESSONS
TOPIC_META = HS.TOPIC_META

LESSON_LEVEL = {
    "hindi-or-urdu-difference": "elementary",
    "learn-hindi-from-bollywood": "elementary",
}

def topic_label(topic):
    return TOPIC_META[topic][0].split(" — ")[0]

def lesson_title(path):
    h = open(path, encoding="utf-8").read()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""

def apply_breadcrumbs(slug):
    path = f"learn/{slug}/index.html"
    h = open(path, encoding="utf-8").read()
    topic = LESSONS[slug]
    level = LESSON_LEVEL.get(slug, "beginner")
    title = lesson_title(path)

    # 1) visible crumb
    new_crumb = ('<p class="crumb"><a href="../../">EkGuru</a> › <a href="../">Learn Hindi</a> › '
                 '<a href="../hindi/">Hindi</a> › <a href="../hindi/%s/">%s</a> › '
                 '<a href="../hindi/%s/">%s</a> › %s</p>'
                 % (level, level.capitalize(), topic, topic_label(topic), title))
    h, n1 = re.subn(r'<p class="crumb">.*?</p>', new_crumb, h, count=1, flags=re.S)

    # 2) JSON-LD BreadcrumbList -> 6 items
    items = [
        ('EkGuru', BASE + '/'),
        ('Learn Hindi', BASE + '/learn/'),
        ('Hindi', BASE + '/learn/hindi/'),
        (level.capitalize(), BASE + '/learn/hindi/%s/' % level),
        (topic_label(topic), BASE + '/learn/hindi/%s/' % topic),
        (title, BASE + '/learn/%s/' % slug),
    ]
    parts = ','.join('{"@type":"ListItem","position":%d,"name":"%s","item":"%s"}'
                     % (i + 1, nm, url) for i, (nm, url) in enumerate(items))
    new_ld = ('{"@type":"BreadcrumbList","@id":"%s/learn/%s/#breadcrumb","itemListElement":[%s]}'
              % (BASE, slug, parts))
    h, n2 = re.subn(r'\{"@type":"BreadcrumbList".*?\]\}', new_ld, h, count=1)
    open(path, "w", encoding="utf-8").write(h)
    return n1, n2

# ---- original, fact-checked quick quizzes for the three exemplar lessons ----
QUIZZES = {
    "hindi-alphabet-for-beginners": [
        ("How many letters are there in the Devanagari alphabet?",
         "44 — each with one sound. That finite size is why the alphabet comes first: once you know the letters you can read anything."),
        ("Why is the alphabet the right place to start, before vocabulary?",
         "Because Hindi is phonetic and finite. Two or three weeks on the letters and you can sound out any word, which makes vocabulary easier, not harder."),
        ("What does the guide give you to help the letters stick?",
         "A printable chart and the order to learn the letters in — pin the chart up and work through the letters in that order."),
    ],
    "how-to-say-hello-in-hindi": [
        ("Is namaste always the right greeting?",
         "No — it is sometimes the wrong word. Which greeting to use changes by time of day, age, religion and situation."),
        ("Which of these is a time-of-day greeting?",
         "सुप्रभात (suprabhat) — good morning. Namaste is general; suprabhat is only for the morning."),
        ("What matters more than the greeting itself?",
         "The follow-up question — asking how the person is — which matters more than which greeting you opened with."),
    ],
    "hindi-sentence-structure": [
        ("Where does the verb go in a Hindi sentence?",
         "At the end — Hindi is subject-object-verb, so the action is the last thing you hear."),
        ("What does Hindi use instead of English prepositions like \u201cin\u201d and \u201con\u201d?",
         "Postpositions — small words that go AFTER the noun, not before it."),
        ("Why do Hindi sentences feel \u201cbackwards\u201d at first?",
         "Because the verb comes last, so you wait for the whole sentence before you know the action."),
    ],
}

def apply_quiz(slug):
    path = f"learn/{slug}/index.html"
    h = open(path, encoding="utf-8").read()
    if '<section class="quiz"' in h:
        return 0, 0
    items = QUIZZES[slug]
    blocks = []
    for q, a in items:
        blocks.append('<details style="margin:10px 0;border:1px solid var(--line);border-radius:10px;padding:12px 14px">'
                      '<summary style="cursor:pointer;font-weight:600;color:var(--ink)">%s</summary>'
                      '<p style="margin:10px 0 0;color:var(--ink-2)">%s</p></details>' % (q, a))
    quiz_html = ('<section class="quiz" aria-label="Quick check" '
                 'style="background:var(--bg-soft);border:1px solid #ddd8ff;border-radius:14px;'
                 'padding:16px 18px;margin:30px 0">'
                 '<h2 style="margin:0 0 12px;font-size:1.15rem">Quick check</h2>'
                 + "\n".join(blocks) + '</section>\n\n  ')
    h, n = re.subn(r'(<h2>Keep going</h2>)', quiz_html + r'\1', h, count=1)
    open(path, "w", encoding="utf-8").write(h)
    return n, 1

def add_hub_pointer(path, hub_href, link_text, blurb):
    """Insert a callout after the lede paragraph, idempotently."""
    h = open(path, encoding="utf-8").read()
    marker = "<!-- ekguru:hindi-hub-pointer -->"
    if marker in h:
        return 0
    callout = ('%s\n<p style="background:var(--bg-soft,#f7f6ff);border:1px solid #ddd8ff;'
               'border-radius:12px;padding:16px 18px;margin:0 0 24px">'
               '<strong>New:</strong> the complete Hindi structure is at '
               '<a href="%s">%s</a> — %s</p>\n' % (marker, hub_href, link_text, blurb))
    h, n = re.subn(r'(<p class="lede">.*?</p>)', r'\1\n' + callout, h, count=1, flags=re.S)
    open(path, "w", encoding="utf-8").write(h)
    return n

def main():
    total_crumb = total_ld = 0
    for slug in LESSONS:
        n1, n2 = apply_breadcrumbs(slug)
        total_crumb += n1
        total_ld += n2
        print(f"  breadcrumbs {slug}: crumb={n1} jsonld={n2}")

    total_quiz = 0
    for slug in QUIZZES:
        n, _ = apply_quiz(slug)
        total_quiz += n
        print(f"  quiz {slug}: injected={n}")

    n = add_hub_pointer("learn/index.html", "hindi/",
                        "Learn Hindi — the complete structure",
                        "choose a goal, pick your level, work through a topic, then learn, practise, quiz and review.")
    print(f"  learn hub pointer: {n}")
    n = add_hub_pointer("hindi/index.html", "../learn/hindi/",
                        "Learn Hindi — the complete structure",
                        "the same topics, organised as a journey from level to topic to lesson.")
    print(f"  hindi topic-map pointer: {n}")

    print(f"done: {total_crumb} crumbs, {total_ld} JSON-LD lists, {total_quiz} quizzes")

if __name__ == "__main__":
    main()

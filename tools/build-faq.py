#!/usr/bin/env python3
"""Generate /faq/ — genuine learner FAQs with contextual journey links.

Single source of truth: this file. Reuses the page shell (head/tail/esc/depth)
from build-materials.py so the FAQ page stays byte-consistent with every other
generated page (recovery.js markers, trust footer, service worker, adsense
block, depth-relative links).

FAQ rules (per the Phase-2 command): real learner questions, concise honest
answers, links that continue a journey (content → material → tool → practice →
lesson → path → tutor). No repetitive SEO FAQ blocks, no keyword stuffing.
"""
import os, sys, json, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

# import build-materials helpers without running its main()
spec = importlib.util.spec_from_file_location("bm", os.path.join(ROOT, "tools", "build-materials.py"))
bm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bm)
esc = bm.esc
depth = bm.depth

SITE = "https://ekguru.shop/"
D = depth("faq/")          # "../" — one segment deep
TODAY = "2026-09-12"

FAQ = [
    ("Getting started", [
        ("Is Hindi hard to learn?",
         "Moderately. For an English speaker it takes real time — the US Foreign Service "
         "Institute groups it with the harder languages — but nothing about it is unfair. "
         "The script is regular, the sounds are learnable, and the grammar has few surprises "
         "once you meet its patterns. See <a href=\"%shindi/how-long/\">how long Hindi really takes</a> "
         "and try the <a href=\"%stoolbox/hindi-time-planner/\">time planner</a> to turn your "
         "weekly hours into a realistic timeline." % (D, D)),
        ("Do I have to learn the Devanagari script?",
         "Not to begin speaking, but for reading and for independent learning it is the single "
         "biggest unlock, and it is far more regular than English spelling. If you only want to "
         "speak, romanisation is a legitimate route — "
         "<a href=\"%sanswers/can-i-learn-hindi-without-learning-the-script/\">here is the honest trade-off</a>. "
         "When you are ready, print the <a href=\"%smaterials/alphabet/devanagari-chart/\">Devanagari chart</a> "
         "and click through the <a href=\"%stoolbox/hindi-alphabet/\">alphabet explorer</a>." % (D, D, D)),
        ("Where do I start as a complete beginner?",
         "Follow a path rather than collecting random pages. The "
         "<a href=\"%slearn/paths/\">learning paths</a> order the steps — alphabet first, then "
         "greetings and numbers, then sentence patterns — and the "
         "<a href=\"%slearn/hindi-alphabet-for-beginners/\">alphabet guide</a> covers the first "
         "milestone in one sitting. Bookmark the <a href=\"%smaterials/\">materials</a> you will want "
         "to pin up as you go." % (D, D, D)),
        ("How long until I can hold a conversation?",
         "With a tutor and a few hours a week, most learners manage simple conversations — "
         "introductions, ordering, directions — within a couple of months. There is no honest "
         "fixed number, which is why the <a href=\"%stoolbox/hindi-time-planner/\">time planner</a> "
         "asks for your real hours instead of promising a date." % D),
    ]),
    ("Materials & tools", [
        ("Are the learning materials really free?",
         "Yes, and there is no account. Every <a href=\"%smaterials/\">material</a> is a page you can "
         "read in the browser or print to PDF with the browser's own print button — nothing to "
         "download and no email wall. The same goes for every <a href=\"%stoolbox/\">tool</a>." % (D, D)),
        ("What should I use to build vocabulary?",
         "Different tools for different stages: the <a href=\"%smaterials/vocabulary/100-essential-words/\">100 "
         "essential words</a> to know what to learn first, the "
         "<a href=\"%stoolbox/hindi-vocabulary/\">vocabulary explorer</a> to search by situation, and "
         "<a href=\"%stoolbox/hindi-flashcards/\">flashcards</a> for spaced repetition, which is what "
         "actually makes words stick." % (D, D, D)),
        ("Can I practise speaking without a partner?",
         "Partially. You can shadow audio, record yourself and narrate your day — "
         "<a href=\"%sanswers/how-to-practice-hindi-speaking-alone/\">these techniques work</a> — but "
         "nothing corrects a sound the way a person does. When you want that, a "
         "<a href=\"%sfind-tutors.html\">tutor</a> is the step up, and the "
         "<a href=\"%slearn/practice/speaking/\">speaking lab</a> bridges the gap in between." % (D, D, D)),
    ]),
    ("Lessons & tutors", [
        ("How do lessons work and what do they cost?",
         "One-to-one video lessons with native-speaking tutors, typically from about $6 an hour, "
         "booked through each tutor's page. Times, prices and the tutor's own description are on the "
         "<a href=\"%sfind-tutors.html\">find a tutor</a> page and on every "
         "<a href=\"%stutor/\">tutor profile</a>." % (D, D)),
        ("Will I actually speak with a native speaker?",
         "Yes — EkGuru tutors are native Hindi speakers, and the point of a lesson is speaking and "
         "being corrected, not watching slides. The "
         "<a href=\"%slearn/hindi-alphabet-for-beginners/\">free guides</a> give you the material; the "
         "lesson gives you the feedback." % D),
        ("Is the trial lesson free?",
         "Many tutors offer a trial, but terms differ per tutor, so check the tutor's own page before "
         "booking rather than assuming. There is no automatic free trial across the whole site."),
    ]),
    ("Practice & progress", [
        ("How do I find my current level?",
         "Two quick checks: the <a href=\"%slearn/practice/placement/\">placement check</a> (twelve "
         "questions) and the <a href=\"%stoolbox/hindi-level-test/\">self-assessment</a>. Both are rough "
         "guides, not certificates — they exist to tell you where to start, not to score you." % (D, D)),
        ("I keep forgetting words. What actually helps?",
         "Spaced repetition, and using the word in a sentence you made yourself. The "
         "<a href=\"%stoolbox/hindi-flashcards/\">flashcards</a> handle the spacing, and the "
         "<a href=\"%slearn/practice/review/\">review lab</a> queues up exactly the items you have been "
         "getting wrong." % (D, D)),
        ("How do I know I am improving?",
         "Notice what you can now do that you could not do last month — read a sign, understand a "
         "greeting at full speed, finish a sentence without stalling. The "
         "<a href=\"%slearn/practice/\">practice labs</a> track your right/wrong rate per area so you can "
         "see which skills are firming up and which are wobbling." % D),
    ]),
    ("About EkGuru", [
        ("Is there an app, and do I need an account?",
         "No app and no account. Every tool, material and guide runs in your browser, and progress "
         "is kept in your own browser's storage. You can start at "
         "<a href=\"%slearn/\">the free guides</a> right now." % D),
        ("How is this different from a language app?",
         "Apps are excellent for vocabulary and daily streaks; a tutor is what gets you speaking and "
         "corrected. EkGuru pairs free self-study material (guides, tools, practice labs) with "
         "one-to-one lessons, and is honest about which part does what — see "
         "<a href=\"%sask/cheapest-way-to-learn-hindi/\">the cheapest way to learn Hindi</a> for the "
         "straight version." % D),
        ("I found a mistake in a Hindi word. What should I do?",
         "Tell us through the <a href=\"%scontact/\">contact form</a> — pick the \"Hindi spelling looks "
         "wrong\" topic and name the page. Hand-typed Devanagari goes wrong in small ways and a "
         "native speaker's eye is worth more than our proofreading; corrections land in the next build." % D),
    ]),
]

def faq_jsonld():
    items = []
    for _group, qs in FAQ:
        for q, a in qs:
            items.append({"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": a}})
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": items, "@id": SITE + "faq/#faq"}

def head():
    title = "Hindi Learning FAQ — Real Answers to Real Questions | EkGuru"
    meta = ("Honest answers to the questions learners actually ask: is Hindi hard, do I need the "
            "script, where do I start, how do lessons work and what do they cost.")
    out = ['<!DOCTYPE html>\n<html lang="en" dir="ltr">\n<head>',
           '<meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width,initial-scale=1">',
           "<title>%s</title>" % esc(title),
           '<meta name="description" content="%s">' % esc(meta),
           '<meta name="author" content="EkGuru">',
           '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">',
           '<link rel="canonical" href="%sfaq/">' % SITE,
           '<meta property="og:type" content="website">',
           '<meta property="og:title" content="%s">' % esc(title),
           '<meta property="og:description" content="%s">' % esc(meta),
           '<meta property="og:url" content="%sfaq/">' % SITE,
           '<meta property="og:site_name" content="EkGuru">',
           '<link rel="icon" href="%simages/favicon.ico" sizes="any">' % D,
           '<link rel="apple-touch-icon" href="%simages/apple-touch-icon.png">' % D,
           '<link rel="manifest" href="%smanifest.webmanifest">' % D,
           '<meta name="theme-color" content="#4f32d9">',
           '<link rel="stylesheet" href="%scss/style.min.css">' % D,
           '<style>%s</style>' % bm.STYLE,
           '<script type="application/ld+json">%s</script>' % json.dumps(faq_jsonld(), ensure_ascii=False),
           '<!-- ekguru:adsense:start -->',
           '<link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin>',
           '<link rel="preconnect" href="https://googleads.g.doubleclick.net" crossorigin>',
           '<meta name="google-adsense-account" content="ca-pub-8175326569491671">',
           '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8175326569491671" crossorigin="anonymous"></script>',
           '<!-- ekguru:adsense:end -->',
           "</head>\n<body>"]
    return "\n".join(out)

def main():
    body = ['<p class="crumb"><a href="%s">EkGuru</a> \u203a FAQ</p>' % D,
            '<h1>Hindi learning FAQ</h1>',
            '<p class="meta">Honest answers — no upsells, no inflated promises.</p>']
    for group, qs in FAQ:
        body.append('<h2>%s</h2>' % esc(group))
        for q, a in qs:
            body.append('<div class="faq"><b>%s</b><p>%s</p></div>' % (esc(q), a))
    body.append('<p>Something not covered? <a href="%scontact/">Write to us</a> — a person reads '
                'every message.</p>' % D)
    body.append("</div>")
    html = head() + "\n<div class=\"art\">\n" + "\n".join(body) + "\n" + bm.tail(D)
    path = os.path.join(ROOT, "faq", "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote faq/index.html (%d questions)" % sum(len(qs) for _g, qs in FAQ))
    return 0

if __name__ == "__main__":
    sys.exit(main())

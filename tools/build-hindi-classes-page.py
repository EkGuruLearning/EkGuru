#!/usr/bin/env python3
"""Build the `hindi-classes` hub page from the find-tutors.html shell.

Why: the GSC export has `hindi classes near me` at 189 impressions and 0
clicks — a high-volume local/near-me intent with no page serving it. The
existing `hindi-tutor/` hub is about tutors by location; `find-tutors.html`
is the tutor-profile directory. Neither is the "classes near me" answer.

EkGuru is an online-only service: it has no physical classrooms and must not
pretend to local presence. So this page serves the near-me intent honestly —
every class is online, "near me" means the lesson time fits your day and your
timezone, and the page links to the tutor-by-location hub, the free self-study
course and the tools a learner searches for next.

The shell (head markers, ultra assets, global-nav, footer) is taken from
find-tutors.html unchanged so apply-ultra stays idempotent; only the head
meta, schema and <main> body are rewritten. Tables are not involved here, so
no ekguru:...:start/end table markers are added.

  python3 tools/build-hindi-classes-page.py [--check]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from discovery_integrity import prefix_relative_references

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "find-tutors.html"
OUT = ROOT / "hindi-classes" / "index.html"

CANONICAL = "https://ekguru.shop/hindi-classes/"
TITLE = "Hindi Classes Near Me — Online Hindi Classes | EkGuru"
DESC = ("Searching for Hindi classes near me? EkGuru's Hindi classes are online, "
        "so the best class for you is wherever the lesson time fits your day. "
        "Free self-study course, live tutor classes, and a guide to choosing the "
        "right class — no sign-up to start.")
OGDESC = ("Hindi classes near me, online: a free self-study course and live tutor "
          "classes that fit your timezone. Learn how to pick the right class and "
          "start today.")

BODY = """<main id="main">
<section class="pf-hero">
<div class="wrap">
<nav aria-label="Breadcrumb" class="crumbs">
<a data-i18n="nav.home" data-navlink="index.html" href="index.html">Home</a> ›
      <span>Hindi classes near me</span>
</nav>
<span class="pill">📘 <span>Online classes</span></span>
<h1 style="margin:0 0 6px">Hindi classes near me — online, in your timezone</h1>
<p class="muted" style="margin:0">Every EkGuru Hindi class is online. There is no building to travel to; "near me" means the lesson time fits your day and your timezone. Start free, add a live tutor when you want speaking practice.</p>
</div>
</section>
<section class="sec">
<div class="wrap">
<h2>What "Hindi classes near me" means on EkGuru</h2>
<p>A search for <strong>Hindi classes near me</strong> usually means one of two things: you want a class close to where you are, or you want the class to fit around your schedule. Because EkGuru classes run online, location does not limit which class you can join — it only sets the timezone the lesson time is shown in. That makes every class on this page available to you, wherever you are.</p>
<p>Two ways to take a Hindi class here, both open right now:</p>
<ul class="rel" style="list-style:none;padding:0;display:grid;gap:14px">
<li><b>Free self-study class.</b> A complete Hindi course you work through at your own pace: the alphabet and sounds, vocabulary, grammar and practice, with no sign-up and no payment. Best when you want to explore before committing. <a href="learn/hindi/">Start the free Hindi course →</a></li>
<li><b>Live tutor class.</b> One-to-one lessons with a Hindi tutor, booked by the lesson and taken over video. Best when you want to speak, get correction, and keep a regular schedule. <a href="find-tutors.html">Browse tutor profiles →</a></li>
</ul>
<p class="sm">Not sure which fits? The guide below walks through choosing a class; the <a href="faq/">Hindi learning FAQ</a> answers the common questions first.</p>
</div>
</section>
<section class="wrap sec">
<h2>How to choose the right Hindi class</h2>
<p>Pick the class that matches the goal you can describe. The questions below are the ones people actually ask before starting, and answering them here is the difference between a class you keep and one you drop after a week.</p>
<h3>Decide: self-study or live class</h3>
<p>If you are disciplined and curious, the free course is enough for the early stages — letters, sounds, first words and grammar. If you want to actually speak Hindi, a live class is the step that matters: a person corrects you, answers your questions and pushes you past the point where a course stalls. Many learners do both: the course for structure, a tutor for conversation.</p>
<h3>Check what the class actually covers</h3>
<p>A class is only right if it covers what you need. For reading and writing, it must teach the Devanagari script, not romanisation only. For speaking, it must give you chances to talk, not just listen. For school or heritage learning, check the level and topics. The <a href="learn/hindi/">Hindi course</a> lists every topic and level so you can confirm coverage before you start.</p>
<h3>Check the time against your day</h3>
<p>For a live class, the lesson time is what "near me" really decides. Each tutor location page works out the lesson hours in your own timezone, so you can see whether a slot lands in your morning, evening or late night. <a href="hindi-tutor/">See Hindi tutors by location →</a></p>
<h3>Confirm cost and terms before committing</h3>
<p>The self-study course is free. A live class is booked per lesson at a price the tutor states on their profile; EkGuru takes no commission on tutor lessons and adds no platform fee to the displayed price in this release, and EkGuru does not collect tutor-lesson payments. Do not assume every tutor offers the same trial, duration or cancellation terms — check the profile and confirm directly before you commit. A lesson request is an enquiry until current availability and terms are confirmed in a reply.</p>
<h2>Common questions</h2>
<div class="faq"><b>Are there Hindi classes physically near me?</b>
<p>EkGuru runs online Hindi classes only — there is no physical classroom or local branch to visit. Every class is taken over the internet, so "near me" means the lesson time and timezone fit your day rather than a location you travel to.</p></div>
<div class="faq"><b>Do I need to pay to start a Hindi class?</b>
<p>No. The self-study Hindi course, the practice tools and the questions section are free and need no sign-up. You only pay for a live tutor class, and only at the price the tutor states on their profile.</p></div>
<div class="faq"><b>Can I learn Hindi online without the script?</b>
<p>You can begin with speech and romanisation, but romanisation is inconsistent and cannot show every sound clearly. If reading is part of your goal, the <a href="learn/hindi-alphabet-for-beginners/">free alphabet guide</a> is the right place to start.</p></div>
<div class="faq"><b>How long until I can hold a conversation?</b>
<p>There is no reliable universal timetable. It depends on your language background, how often you practice, whether you take live classes, and the kind of conversation you mean. Ask a prospective tutor for a plan tied to your goal rather than a guaranteed date.</p></div>
<div class="faq"><b>Can a child take a Hindi class here?</b>
<p>Use a tutor profile that explicitly states experience with children, and have a parent or guardian handle booking, supervision, privacy and any payment. The free course is also suitable for a child working with a grown-up.</p></div>
<p class="sm">More: <a href="learn/hindi/">free Hindi course</a> ·
    <a href="find-tutors.html">find a Hindi tutor</a> ·
    <a href="hindi-tutor/">Hindi tutors by location</a> ·
    <a href="name-in-hindi/">write your name in Hindi</a></p>
</section>
<div class="wrap"><p class="text-versions" id="text-versions"></p></div>
</main>
"""


def repl(text: str, pattern: str, value: str) -> str:
    new, n = re.subn(pattern, lambda m: value, text, count=1)
    if n == 0:
        raise SystemExit(f"anchor not found: {pattern!r}")
    return new


def _prefix_block(block: str, prefix: str) -> str:
    """Prefix relative href/src links inside a shell block with the depth prefix.

    build-shell.js writes header/footer links relative to each page's depth.
    The shell source (find-tutors.html) is at the root, so its header/footer
    links are root-relative; for a depth-1 page they must become ../-prefixed.
    Absolute (/, http, mailto, #, data:) links are left alone.
    """
    def fix(m: re.Match) -> str:
        attr, val = m.group(1), m.group(2)
        if re.match(r"^(/|https?:|mailto:|#|data:|javascript:)", val):
            return m.group(0)
        return f'{attr}="{prefix}{val}"'
    return re.sub(r'\b(href|src)="([^"]+)"', fix, block)


def build() -> str:
    text = SHELL.read_text(encoding="utf-8")

    # --- head meta: title, description, canonical, og/twitter ---
    text = repl(text, r'<title>Find a Hindi tutor \| EkGuru</title>', f"<title>{TITLE}</title>")
    text = repl(text,
                r'<meta content="Browse public Hindi tutor profiles\. Review tutor-provided details and confirm current terms and availability before sending an enquiry\." name="description"/>',
                f'<meta content="{DESC}" name="description"/>')
    text = repl(text, r'<link href="https://ekguru\.shop/find-tutors\.html" rel="canonical"/>',
                f'<link href="{CANONICAL}" rel="canonical"/>')
    text = repl(text, r'<meta content="Find a Hindi tutor \| EkGuru" property="og:title"/>',
                f'<meta content="{TITLE}" property="og:title"/>')
    text = repl(text,
                r'<meta content="Browse public Hindi tutor profiles\. Review tutor-provided details and confirm current terms and availability before sending an enquiry\." property="og:description"/>',
                f'<meta content="{OGDESC}" property="og:description"/>')
    text = repl(text, r'<meta content="https://ekguru\.shop/find-tutors\.html" property="og:url"/>',
                f'<meta content="{CANONICAL}" property="og:url"/>')
    text = repl(text, r'<meta content="Find a Hindi tutor \| EkGuru" name="twitter:title"/>',
                f'<meta content="{TITLE}" name="twitter:title"/>')
    text = repl(text, r'<meta name="twitter:image:alt" content="Find a Hindi tutor \| EkGuru">',
                f'<meta name="twitter:image:alt" content="{TITLE}">')
    text = repl(text,
                r'<meta content="Browse public Hindi tutor profiles\. Review tutor-provided details and confirm current terms and availability before sending an enquiry\." name="twitter:description"/>',
                f'<meta content="{OGDESC}" name="twitter:description"/>')

    # No translated equivalents exist for this landing page. Do not invent
    # alternate URLs or inherit the unrelated tutor-directory language set.
    text = re.sub(r'<link\b[^>]*\bhreflang="[^"]+"[^>]*>\n?', '', text)
    text = text.replace('</head>',
                        f'<link href="{CANONICAL}" hreflang="en" rel="alternate"/>\n'
                        f'<link href="{CANONICAL}" hreflang="x-default" rel="alternate"/>\n</head>', 1)

    # --- schema: breadcrumb + FAQ, no tutor ItemList ---
    schema_old = re.search(r'<!-- EKGURU:SCHEMA -->.*?<!-- /EKGURU:SCHEMA -->', text, re.S).group(0)
    faq = {
        "@context": "https://schema.org", "@type": "FAQPage", "@id": f"{CANONICAL}#faq",
        "mainEntity": [
            {"@type": "Question", "name": "Are there Hindi classes physically near me?",
             "acceptedAnswer": {"@type": "Answer", "text": "EkGuru runs online Hindi classes only — there is no physical classroom or local branch to visit. Every class is taken over the internet, so 'near me' means the lesson time and timezone fit your day rather than a location you travel to."}},
            {"@type": "Question", "name": "Do I need to pay to start a Hindi class?",
             "acceptedAnswer": {"@type": "Answer", "text": "No. The self-study Hindi course, the practice tools and the questions section are free and need no sign-up. You only pay for a live tutor class, and only at the price the tutor states on their profile."}},
            {"@type": "Question", "name": "Can I learn Hindi online without the script?",
             "acceptedAnswer": {"@type": "Answer", "text": "You can begin with speech and romanisation, but romanisation is inconsistent and cannot show every sound clearly. If reading is part of your goal, the free alphabet guide is the right place to start."}},
            {"@type": "Question", "name": "How long until I can hold a conversation?",
             "acceptedAnswer": {"@type": "Answer", "text": "There is no reliable universal timetable. It depends on your language background, how often you practice, whether you take live classes, and the kind of conversation you mean. Ask a prospective tutor for a plan tied to your goal rather than a guaranteed date."}},
        ],
    }
    import json
    breadcrumb = {
        "@context": "https://schema.org", "@graph": [
            {"@type": ["Organization", "EducationalOrganization"], "@id": "https://ekguru.shop/#org", "name": "EkGuru",
             "url": "https://ekguru.shop/", "description": "One Student. One Goal. One Guru.",
             "email": "EkGuruLearning@gmail.com", "areaServed": "Worldwide",
             "sameAs": ["https://www.youtube.com/@ekguru_india", "https://www.facebook.com/profile.php?id=61596855810597", "https://www.instagram.com/ekguru.in", "https://x.com/ekguru_india", "https://www.linkedin.com/company/ekguru"],
             "logo": {"@type": "ImageObject", "url": "https://ekguru.shop/images/icon-512.png", "width": 512, "height": 512},
             "founder": {"@type": "Person", "name": "Prakash", "jobTitle": "Founder & CEO, EkGuru",
                         "alumniOf": {"@type": "CollegeOrUniversity", "name": "Malaviya National Institute of Technology Jaipur", "url": "https://www.mnit.ac.in/"},
                         "sameAs": ["https://www.linkedin.com/in/itstheprakash/"]},
             "contactPoint": {"@type": "ContactPoint", "contactType": "customer support",
                              "email": "EkGuruLearning@gmail.com", "url": "https://ekguru.shop/contact/",
                              "availableLanguage": ["English", "Hindi"]}},
            {"@type": "WebPage", "@id": f"{CANONICAL}#page", "url": CANONICAL,
             "name": "Online Hindi Classes — 1-on-1 Live Lessons & Free Course",
             "isPartOf": {"@id": "https://ekguru.shop/#website"},
             "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".hero h1", ".hero p.lead", ".faq b"]}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "EkGuru", "item": "https://ekguru.shop/"},
                {"@type": "ListItem", "position": 2, "name": "Hindi classes", "item": CANONICAL}]},
            faq,
        ],
    }
    new_schema = "<!-- EKGURU:SCHEMA -->\n<script type=\"application/ld+json\">" + json.dumps(breadcrumb, ensure_ascii=False) + "</script>\n<!-- /EKGURU:SCHEMA -->"
    text = text.replace(schema_old, new_schema, 1)

    # --- main body ---
    text = re.sub(r'<main id="main">.*?</main>\n', BODY, text, count=1, flags=re.S)

    # --- normalise header/footer link prefixes to this page's depth ---
    # build-shell.js writes header/footer links relative to the page depth
    # (../ for a depth-1 page). The shell source is at the root, so its
    # header/footer links are root-relative; prefix them here to match what
    # the shell writer produces, so build-shell.js --check stays idempotent.
    prefix = "../"  # hindi-classes/index.html is one level deep
    text = re.sub(
        r'(<!-- ekguru:shell-header:start -->)(.*?)(<!-- ekguru:shell-header:end -->)',
        lambda m: m.group(1) + _prefix_block(m.group(2), prefix) + m.group(3),
        text, count=1, flags=re.S)
    text = re.sub(
        r'(<!-- ekguru:shell-footer:start -->)(.*?)(<!-- ekguru:shell-footer:end -->)',
        lambda m: m.group(1) + _prefix_block(m.group(2), prefix) + m.group(3),
        text, count=1, flags=re.S)

    # The rest of this root-level shell (assets, body CTAs and scripts)
    # also needs relocation, not just the header/footer.
    return prefix_relative_references(text)


ULTRA_STRIP = re.compile(r'<!-- ekguru:ultra-[a-z]+:start -->\n[\s\S]*?<!-- ekguru:ultra-[a-z]+:end -->\n')


def _strip_ultra(raw: str) -> str:
    raw = ULTRA_STRIP.sub('', raw)
    return re.sub(r'(<html\b[^>]*?) data-learning-language="[^"]*"', r'\1', raw, count=1, flags=re.I)


def main() -> int:
    check = "--check" in sys.argv
    page = build()
    if check:
        if not OUT.exists() or _strip_ultra(OUT.read_text(encoding="utf-8")) != _strip_ultra(page):
            print(f"STALE {OUT.relative_to(ROOT)} — run: python3 tools/build-hindi-classes-page.py")
            return 1
        print("ok    hindi-classes page is current")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print("wrote hindi-classes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

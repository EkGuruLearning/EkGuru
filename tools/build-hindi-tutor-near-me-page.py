#!/usr/bin/env python3
"""Build the `hindi-tutor-near-me` hub page from the find-tutors.html shell.

Why: the GSC export has `hindi tutor near me` at 37 impressions and 0
clicks. The `hindi-tutor/` hub is a location directory and
`find-tutors.html` is the tutor-profile browser; neither is the direct
answer to the near-me intent, and the exact phrase "hindi tutor near me"
does not appear as a page's purpose anywhere.

EkGuru tutors teach online only — there is no in-person tutor to find
"near" you, and the site must not pretend to local tutor availability.
So this page serves the intent honestly: every tutor is online, "near
me" means the lesson time and timezone fit your day, and the page links
to the tutor directory, the by-location hub and the free course.

The shell (head markers, ultra assets, global-nav, footer) is taken from
find-tutors.html unchanged so apply-ultra stays idempotent; only the head
meta, schema and <main> body are rewritten.

  python3 tools/build-hindi-tutor-near-me-page.py [--check]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "find-tutors.html"
OUT = ROOT / "hindi-tutor-near-me" / "index.html"

CANONICAL = "https://ekguru.shop/hindi-tutor-near-me/"
TITLE = "Hindi Tutor Near Me — Online Hindi Tutors | EkGuru"
DESC = ("Searching for a Hindi tutor near me? EkGuru's Hindi tutors teach "
        "online, so the right tutor is one whose lesson time fits your day "
        "and timezone. Browse tutor profiles, see tutors by location, or "
        "start the free course — no sign-up to begin.")
OGDESC = ("Hindi tutor near me, online: browse tutor profiles and see lesson "
          "times in your timezone. Find the right online Hindi tutor and "
          "start learning today.")

BODY = """<main id="main">
<section class="pf-hero">
<div class="wrap">
<nav aria-label="Breadcrumb" class="crumbs">
<a data-i18n="nav.home" data-navlink="index.html" href="index.html">Home</a> ›
      <span>Hindi tutor near me</span>
</nav>
<span class="pill">🧑‍🏫 <span>Online tutors</span></span>
<h1 style="margin:0 0 6px">Hindi tutor near me — online, in your timezone</h1>
<p class="muted" style="margin:0">EkGuru's Hindi tutors teach online, one to one. There is no in-person tutor to travel to; "near me" means the lesson time fits your day and your timezone. Browse tutor profiles below, or see tutors by your location.</p>
</div>
</section>
<section class="sec">
<div class="wrap">
<h2>What "Hindi tutor near me" means on EkGuru</h2>
<p>A search for <strong>Hindi tutor near me</strong> usually means you want a tutor who is convenient to you — close by, or available at a time that suits your day. Because every EkGuru tutor teaches online, location does not limit which tutor you can take: it only sets the timezone the lesson time is shown in. That means any tutor on this page is available to you, wherever you are.</p>
<p>Two ways to learn Hindi here, both open right now:</p>
<ul class="rel" style="list-style:none;padding:0;display:grid;gap:14px">
<li><b>Browse tutor profiles.</b> Each profile states the tutor's subjects, levels, teaching description, price and any stated availability. You enquire directly and confirm the time and terms with the tutor before a lesson is booked. <a href="find-tutors.html">Browse tutor profiles →</a></li>
<li><b>See tutors by location.</b> Every tutor lives in India and teaches online, so the location pages work out the lesson hours that fit your timezone and the price in your currency. <a href="hindi-tutor/">Hindi tutors by location →</a></li>
</ul>
<p class="sm">Not ready for a tutor? The <a href="learn/hindi/">free Hindi course</a> is a complete self-study class you can start with no sign-up.</p>
</div>
</section>
<section class="wrap sec">
<h2>How to find the right Hindi tutor</h2>
<p>Pick the tutor whose profile matches the goal you can describe. The questions below are the ones people actually ask before booking, and answering them here is the difference between a tutor you keep and one you drop after a lesson.</p>
<h3>Start from your goal, not the tutor</h3>
<p>Decide what you want first: conversation, reading and the Devanagari script, school support, heritage learning, or something specific. Then compare that goal with each profile's subjects, levels and teaching description. A listing is not a guarantee that a tutor currently has the right slot or accepts every request — confirm directly.</p>
<h3>Check the lesson time against your day</h3>
<p>For "near me", the lesson time is what really matters. Each tutor location page shows the lesson hours in your own timezone, so you can see whether a slot lands in your morning, evening or late night. <a href="hindi-tutor/">See tutors by location →</a></p>
<h3>Check trial, price and terms before committing</h3>
<p>Do not assume every tutor offers the same trial, lesson duration, payment or cancellation terms. Each profile shows the tutor's base lesson price; any converted amount is an estimate based on an exchange rate. Check the profile and confirm the amount, payment method and terms directly before you commit. A lesson request is an enquiry until current availability and terms are confirmed in a reply.</p>
<h3>Language background and qualifications</h3>
<p>Profiles contain tutor-provided statements about language background, experience and qualifications. EkGuru has not independently verified every statement; ask how the tutor would teach your particular goal before booking.</p>
<h2>Common questions</h2>
<div class="faq"><b>Can I find a Hindi tutor physically near me?</b>
<p>EkGuru tutors teach online only — there is no in-person tutor or local branch to visit. Every lesson is taken over the internet, so "near me" means the lesson time and timezone fit your day rather than a location you travel to.</p></div>
<div class="faq"><b>Do the tutors speak Hindi natively?</b>
<p>Every tutor on EkGuru lives in India and uses Hindi daily. Profiles state the languages each tutor teaches in, so you can check before booking whether they will explain grammar in English or in Hindi.</p></div>
<div class="faq"><b>Can a complete beginner book a tutor?</b>
<p>Yes, and beginners are the most common starting point. Choose a profile that explicitly lists beginners or your current level, and state what you already know. The free self-study course is also a good place to start before your first lesson.</p></div>
<div class="faq"><b>How long until I can hold a conversation?</b>
<p>There is no reliable universal timetable. It depends on prior languages, speaking practice, lesson frequency, feedback and the kind of conversation you mean. Ask a prospective tutor for a plan tied to your goal rather than a guaranteed date.</p></div>
<div class="faq"><b>Can I learn without a tutor first?</b>
<p>Yes. The <a href="learn/hindi/">free Hindi course</a>, the practice tools and the questions section need no payment and no sign-up. Book a tutor when you want conversation and correction.</p></div>
<p class="sm">More: <a href="find-tutors.html">find a Hindi tutor</a> ·
    <a href="hindi-tutor/">Hindi tutors by location</a> ·
    <a href="learn/hindi/">free Hindi course</a> ·
    <a href="name-in-hindi/">write your name in Hindi</a></p>
</section>
<div class="wrap"><p class="text-versions" id="text-versions"></p></div>
</main>
"""


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


def repl(text: str, pattern: str, value: str) -> str:
    new, n = re.subn(pattern, lambda m: value, text, count=1)
    if n == 0:
        raise SystemExit(f"anchor not found: {pattern!r}")
    return new


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
    text = repl(text,
                r'<meta content="Browse public Hindi tutor profiles\. Review tutor-provided details and confirm current terms and availability before sending an enquiry\." name="twitter:description"/>',
                f'<meta content="{OGDESC}" name="twitter:description"/>')

    # --- hreflang set: point every alternate at the new URL ---
    text = text.replace('<link href="https://ekguru.shop/find-tutors.html" hreflang="en" rel="alternate"/>',
                        f'<link href="{CANONICAL}" hreflang="en" rel="alternate"/>', 1)
    text = text.replace('hreflang="en" rel="alternate"/>\n<link href="https://ekguru.shop/es/find-tutors.html"',
                        f'hreflang="en" rel="alternate"/>\n<link href="https://ekguru.shop/es/hindi-tutor-near-me/"', 1)
    text = text.replace('hreflang="es" rel="alternate"/>\n<link href="https://ekguru.shop/fr/find-tutors.html"',
                        'hreflang="es" rel="alternate"/>\n<link href="https://ekguru.shop/fr/hindi-tutor-near-me/"', 1)
    text = text.replace('hreflang="fr" rel="alternate"/>\n<link href="https://ekguru.shop/de/find-tutors.html"',
                        'hreflang="fr" rel="alternate"/>\n<link href="https://ekguru.shop/de/hindi-tutor-near-me/"', 1)
    text = text.replace('hreflang="de" rel="alternate"/>\n<link href="https://ekguru.shop/pt/find-tutors.html"',
                        'hreflang="de" rel="alternate"/>\n<link href="https://ekguru.shop/pt/hindi-tutor-near-me/"', 1)
    text = text.replace('hreflang="pt" rel="alternate"/>\n<link href="https://ekguru.shop/ja/find-tutors.html"',
                        'hreflang="pt" rel="alternate"/>\n<link href="https://ekguru.shop/ja/hindi-tutor-near-me/"', 1)
    text = text.replace('hreflang="ja" rel="alternate"/>\n<link href="https://ekguru.shop/ar/find-tutors.html"',
                        'hreflang="ja" rel="alternate"/>\n<link href="https://ekguru.shop/ar/hindi-tutor-near-me/"', 1)
    text = text.replace('hreflang="ar" rel="alternate"/>\n<link href="https://ekguru.shop/find-tutors.html" hreflang="x-default"',
                        'hreflang="ar" rel="alternate"/>\n<link href="https://ekguru.shop/hindi-tutor-near-me/" hreflang="x-default"', 1)

    # --- schema: breadcrumb + FAQ, no tutor ItemList ---
    schema_old = re.search(r'<!-- EKGURU:SCHEMA -->.*?<!-- /EKGURU:SCHEMA -->', text, re.S).group(0)
    faq = {
        "@context": "https://schema.org", "@type": "FAQPage", "@id": f"{CANONICAL}#faq",
        "mainEntity": [
            {"@type": "Question", "name": "Can I find a Hindi tutor physically near me?",
             "acceptedAnswer": {"@type": "Answer", "text": "EkGuru tutors teach online only — there is no in-person tutor or local branch to visit. Every lesson is taken over the internet, so 'near me' means the lesson time and timezone fit your day rather than a location you travel to."}},
            {"@type": "Question", "name": "Do the tutors speak Hindi natively?",
             "acceptedAnswer": {"@type": "Answer", "text": "Every tutor on EkGuru lives in India and uses Hindi daily. Profiles state the languages each tutor teaches in, so you can check before booking whether they will explain grammar in English or in Hindi."}},
            {"@type": "Question", "name": "Can a complete beginner book a tutor?",
             "acceptedAnswer": {"@type": "Answer", "text": "Yes, and beginners are the most common starting point. Choose a profile that explicitly lists beginners or your current level, and state what you already know. The free self-study course is also a good place to start before your first lesson."}},
            {"@type": "Question", "name": "How long until I can hold a conversation?",
             "acceptedAnswer": {"@type": "Answer", "text": "There is no reliable universal timetable. It depends on prior languages, speaking practice, lesson frequency, feedback and the kind of conversation you mean. Ask a prospective tutor for a plan tied to your goal rather than a guaranteed date."}},
        ],
    }
    breadcrumb = {
        "@context": "https://schema.org", "@graph": [
            {"@type": "Organization", "@id": "https://ekguru.shop/#org", "name": "EkGuru",
             "url": "https://ekguru.shop/", "description": "One Student. One Goal. One Guru.",
             "email": "EkGuruLearning@gmail.com",
             "logo": {"@type": "ImageObject", "url": "https://ekguru.shop/images/og-cover.jpg"},
             "founder": {"@type": "Person", "name": "Prakash", "jobTitle": "Founder & CEO, EkGuru",
                         "alumniOf": {"@type": "CollegeOrUniversity", "name": "Malaviya National Institute of Technology Jaipur", "url": "https://www.mnit.ac.in/"},
                         "sameAs": ["https://www.linkedin.com/in/itstheprakash/"]},
             "contactPoint": {"@type": "ContactPoint", "contactType": "customer support",
                              "email": "EkGuruLearning@gmail.com", "url": "https://ekguru.shop/contact/",
                              "availableLanguage": ["English", "Hindi"]}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "EkGuru", "item": "https://ekguru.shop/"},
                {"@type": "ListItem", "position": 2, "name": "Hindi tutor near me", "item": CANONICAL}]},
            faq,
        ],
    }
    new_schema = "<!-- EKGURU:SCHEMA -->\n<script type=\"application/ld+json\">" + json.dumps(breadcrumb, ensure_ascii=False) + "</script>\n<!-- /EKGURU:SCHEMA -->"
    text = text.replace(schema_old, new_schema, 1)

    # --- main body ---
    text = re.sub(r'<main id="main">.*?</main>\n', BODY, text, count=1, flags=re.S)

    # --- normalise header/footer link prefixes to this page's depth ---
    prefix = "../"  # hindi-tutor-near-me/index.html is one level deep
    text = re.sub(
        r'(<!-- ekguru:shell-header:start -->)(.*?)(<!-- ekguru:shell-header:end -->)',
        lambda m: m.group(1) + _prefix_block(m.group(2), prefix) + m.group(3),
        text, count=1, flags=re.S)
    text = re.sub(
        r'(<!-- ekguru:shell-footer:start -->)(.*?)(<!-- ekguru:shell-footer:end -->)',
        lambda m: m.group(1) + _prefix_block(m.group(2), prefix) + m.group(3),
        text, count=1, flags=re.S)

    return text


def main() -> int:
    check = "--check" in sys.argv
    page = build()
    if check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != page:
            print(f"STALE {OUT.relative_to(ROOT)} — run: python3 tools/build-hindi-tutor-near-me-page.py")
            return 1
        print("ok    hindi-tutor-near-me page is current")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print("wrote hindi-tutor-near-me")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

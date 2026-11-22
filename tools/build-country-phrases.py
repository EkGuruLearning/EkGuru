#!/usr/bin/env python3
"""Generate country-specific daily-phrases SEO landing pages.

For every learn-hindi-from-{country}/ directory, creates a
learn-hindi-from-{country}/daily-phrases/index.html page targeting
daily-search queries like "hindi daily phrases {country}",
"learn hindi greetings {country}", "hindi phrases for beginners {country}".

Each page contains 39 daily-search Hindi phrases grouped into 4 sections
(Greetings, Everyday Questions, Polite Expressions, Everyday Statements),
each linking to the corresponding ask/how-to-say-{phrase}-in-hindi/ page.
Includes FAQ, QAPage/FAQPage/BreadcrumbList structured data, and a CTA
back to the parent country page.

  python3 tools/build-country-phrases.py
  python3 tools/build-country-phrases.py --check
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 39 daily-search phrases grouped into 4 sections.
# Each entry: (phrase_slug, english_label, hindi, romanisation)
SECTIONS = [
    ("Greetings", [
        ("good-night", "Good night", "शुभ रात्रि", "shubh raatri"),
        ("good-evening", "Good evening", "शुभ संध्या", "shubh sandhya"),
        ("good-afternoon", "Good afternoon", "नमस्ते", "namaste"),
        ("welcome", "Welcome", "स्वागत है", "svaagat hai"),
        ("nice-to-meet-you", "Nice to meet you", "आपसे मिलकर बहुत अच्छा लगा", "aapase mil kar bahut achhaa lagaa"),
        ("see-you-later", "See you later", "बाद में मिलते हैं", "baad meN milte hain"),
        ("see-you-tomorrow", "See you tomorrow", "कल मिलते हैं", "kal milte hain"),
        ("happy-birthday", "Happy birthday", "जन्मदिन मुबारक", "janmadin mubaanrak"),
    ]),
    ("Everyday Questions", [
        ("how-much", "How much is this?", "कितने", "kitne"),
        ("where-is", "Where is it?", "कहाँ है", "kahaan hai"),
        ("what-time-is-it", "What time is it?", "कितने बजे हैं", "kitne baje hain"),
        ("how-old-are-you", "How old are you?", "आपकी आयु क्या है", "aapkii aayu kyaa hai"),
        ("where-are-you-from", "Where are you from?", "आप कहाँ से हैं?", "aap kahaan se hain?"),
        ("where-do-you-live", "Where do you live?", "आप कहाँ रहते हैं?", "aap kahaan rehte hain?"),
        ("what-is-your-name", "What is your name?", "आपका नाम क्या है?", "aapkaa naam kyaa hai?"),
        ("what-do-you-do", "What do you do?", "आप क्या करते हैं?", "aap kyaa karte hain?"),
        ("what-is-this", "What is this?", "यह क्या है?", "yah kyaa hai"),
    ]),
    ("Polite Expressions", [
        ("excuse-me", "Excuse me", "क्षमा करें", "kshamaa karein"),
        ("no-problem", "No problem", "कोई बात नहीं", "koi baat nahin"),
        ("i-am-sorry", "I am sorry", "माफ़ करें", "maaf karein"),
        ("congratulations", "Congratulations", "शुभकामनाएँ", "shubhkaamanaaen"),
        ("good-luck", "Good luck", "शुभकामनाएँ", "shubhkaamanaaen"),
        ("take-care", "Take care", "आप अपना ख्याल रखिए", "aap aapana khayaal rakhiye"),
        ("i-need-help", "I need help", "मुझे मदद चाहिए", "mujhe maadad chaahiye"),
        ("happy-new-year", "Happy new year", "नये साल की शुभकामनाएँ", "naye saal kii shubhkaamanaaen"),
    ]),
    ("Everyday Statements", [
        ("i-dont-know", "I don't know", "मुझे नहीं पता", "mujhe nahin pataa"),
        ("do-you-speak-english", "Do you speak English?", "क्या आप अंग्रेज़ी जानते हैं?", "kyaa aap angrezii jaante hain?"),
        ("i-am-lost", "I am lost", "मैं रास्ता खो चुका हूँ", "main rastaa kho chukaa hoon"),
        ("i-am-tired", "I am tired", "मैं थक गया हूँ", "main thak gaa ya hoon"),
        ("i-like-it", "I like it", "मुझे यह पसंद है", "mujhe yah pasand hai"),
        ("where-is-the-bathroom", "Where is the bathroom?", "शौचालय कहाँ है?", "shouchaalay kahaan hai?"),
        ("i-am-fine", "I am fine", "मैं ठीक हूँ", "main thiik hoon"),
        ("my-name-is", "My name is …", "मेरा नाम … है", "meraa naam ... hai"),
        ("i-dont-speak-hindi", "I don't speak Hindi", "मैं हिंदी नहीं बोलता", "main hindi nahin boltaa"),
        ("i-am-happy", "I am happy", "मैं खुश हूँ", "main khush hoon"),
        ("i-am-sad", "I am sad", "मैं उदास हूँ", "main udaas hoon"),
        ("i-am-busy", "I am busy", "मैं व्यस्त हूँ", "main vyast hoon"),
        ("i-am-here", "I am here", "मैं यहाँ हूँ", "main yahaan hoon"),
        ("i-am-learning-hindi", "I am learning Hindi", "मैं हिंदी सीख रहा हूँ", "main hindi seekh rahaa hoon"),
    ]),
]

FAQ_PAIRS = [
    ("What are the most useful Hindi phrases for a beginner?",
     "Start with greetings (namaste, shubh raatri), polite words (dhanyavaad, maaf karein), and survival phrases (mujhe madad chaahiye, kahaan hai). These 39 daily phrases cover the situations you will actually encounter every day."),
    ("How do I learn Hindi phrases for daily conversation?",
     "Learn one section at a time — greetings first, then everyday questions. Each phrase on this page links to a full guide with usage notes, alternative forms, and pronunciation tips. Practice aloud daily for best results."),
    ("Is Hindi hard to learn for daily conversation?",
     "Hindi is phonetic — once you learn the sound system, words are read exactly as written. Daily conversation uses a limited vocabulary, so the 39 phrases on this page will carry you through most everyday situations."),
    ("Can I learn Hindi for free on EkGuru?",
     "Yes. The Hindi course, starter guides, and practice tools on EkGuru are free. Each phrase page includes detailed usage notes. EkGuru also lists independent Hindi tutors who take direct bookings."),
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def get_countries() -> list[dict]:
    """Find all learn-hindi-from-{slug}/ directories with their display names."""
    countries = []
    for d in sorted(ROOT.iterdir()):
        if d.is_dir() and d.name.startswith("learn-hindi-from-"):
            slug = d.name[len("learn-hindi-from-"):]
            name = slug.replace("-", " ").title()
            parent_html = d / "index.html"
            if parent_html.exists():
                text = parent_html.read_text(encoding="utf-8")[:5000]
                m = re.search(r'<title>Learn Hindi from (?:the )?(.+?):', text)
                if m:
                    name = m.group(1).strip()
            countries.append({"slug": slug, "name": name})
    return countries


def build_page(country_slug: str, country_name: str) -> str:
    """Build the full HTML for one country daily-phrases page."""
    canonical = f"https://ekguru.shop/learn-hindi-from-{country_slug}/daily-phrases/"
    title = f"Hindi Daily Phrases for {country_name}: Greetings, Everyday Words | EkGuru"
    desc = (f"Learn 39 essential Hindi daily phrases for {country_name} — greetings, "
            f"everyday questions, polite expressions and statements. Free Hindi "
            f"phrases with pronunciation guide for beginners in {country_name}.")
    desc = desc.replace('"', "&quot;")

    # FAQ structured data
    faq_json = []
    for q, a in FAQ_PAIRS:
        faq_json.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "QAPage",
                "@id": canonical + "#qa",
                "mainEntity": {
                    "@type": "Question",
                    "name": f"What are the best Hindi daily phrases for {country_name}?",
                    "text": f"What are the best Hindi daily phrases for {country_name}?",
                    "answerCount": 1,
                    "author": {"@type": "Organization", "name": "EkGuru"},
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": (f"The most useful Hindi daily phrases for {country_name} are greetings like "
                                 f"namaste (नमस्ते), polite expressions like dhanyavaad (धन्यवाद), and survival "
                                 f"phrases like mujhe madad chaahiye (मुझे मदद चाहिए). This page lists 39 essential "
                                 f"phrases grouped by situation."),
                        "author": {"@type": "Organization", "name": "EkGuru", "url": "https://ekguru.shop/"},
                    },
                },
            },
            {
                "@type": "FAQPage",
                "@id": canonical + "#faq",
                "mainEntity": faq_json,
            },
            {
                "@type": "BreadcrumbList",
                "@id": canonical + "#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "EkGuru", "item": "https://ekguru.shop/"},
                    {"@type": "ListItem", "position": 2, "name": "Learn Hindi", "item": "https://ekguru.shop/learn/"},
                    {"@type": "ListItem", "position": 3, "name": "By country", "item": "https://ekguru.shop/learn-hindi-by-country/"},
                    {"@type": "ListItem", "position": 4, "name": country_name, "item": f"https://ekguru.shop/learn-hindi-from-{country_slug}/"},
                    {"@type": "ListItem", "position": 5, "name": "Daily phrases", "item": canonical},
                ],
            },
        ],
    }
    ld_json = json.dumps(ld, ensure_ascii=False)

    parts = []

    # --- head ---
    parts.append('<!DOCTYPE html>\n\n')
    parts.append('<html data-learning-language="hi" dir="ltr" lang="en" data-ad-class="HIGH_CONTENT">\n')
    parts.append('<head><!-- ekguru:ultra-head:start -->\n')
    parts.append('<script>(function(){var t;try{t=localStorage.getItem(\'ekguru:theme:v2\')}catch(e){}if([\'light\',\'dark\',\'contrast\'].indexOf(t)<0)t=typeof matchMedia===\'function\'&&matchMedia(\'(prefers-color-scheme:dark)\').matches?\'dark\':\'light\';document.documentElement.dataset.theme=t;document.documentElement.classList.add(\'eg-js\')})()</script>\n')
    parts.append('<script src="/js/voice-languages.js" defer></script>\n')
    parts.append('<script src="/js/voice.js" defer></script>\n')
    parts.append('<script src="/js/ui-motion.js" defer></script>\n')
    parts.append('<!-- ekguru:ultra-head:end -->\n\n')
    parts.append('<meta charset="utf-8"/>\n')
    parts.append('<meta content="width=device-width,initial-scale=1" name="viewport"/>\n')
    parts.append(f'<title>{esc(title)}</title>\n')
    parts.append(f'<meta content="{esc(desc)}" name="description"/>\n')
    parts.append('<meta name="robots" content="index, follow">\n')
    parts.append(f'<link href="{canonical}" rel="canonical"/>\n')
    parts.append('<meta content="hFaqyp-9LdUXSKPA9RF011TkO2m_-7AUMasXqm_0dGI" name="google-site-verification"/>\n')
    parts.append('<meta content="website" property="og:type"/>\n')
    parts.append('<meta content="EkGuru" property="og:site_name"/>\n')
    parts.append('<meta content="en_US" property="og:locale"/>\n')
    parts.append(f'<meta content="{esc(title)}" property="og:title"/>\n')
    parts.append(f'<meta content="{esc(desc)}" property="og:description"/>\n')
    parts.append(f'<meta content="{canonical}" property="og:url"/>\n')
    parts.append('<meta content="https://ekguru.shop/images/og-cover.jpg" property="og:image"/>\n')
    parts.append('<meta content="1200" property="og:image:width"/>\n')
    parts.append('<meta content="630" property="og:image:height"/>\n')
    parts.append('<meta property="og:image:alt" content="EkGuru — free, self-paced Hindi learning">\n')
    parts.append('<meta content="summary_large_image" name="twitter:card"/>\n')
    parts.append(f'<meta content="{esc(title)}" name="twitter:title"/>\n')
    parts.append(f'<meta content="{esc(desc)}" name="twitter:description"/>\n')
    parts.append('<meta content="https://ekguru.shop/images/og-cover.jpg" name="twitter:image"/>\n')
    parts.append('<meta content="EkGuru — free, self-paced Hindi learning" name="twitter:image:alt"/>\n')
    parts.append('<link href="../../images/favicon.ico" rel="icon" sizes="any"/>\n')
    parts.append('<link href="../../images/apple-touch-icon.png" rel="apple-touch-icon"/>\n')
    parts.append('<link href="../../manifest.webmanifest" rel="manifest"/>\n')
    parts.append('<meta content="#4f32d9" name="theme-color"/>\n')
    parts.append('<link href="../../css/style.min.css" rel="stylesheet"/>\n')
    parts.append(f'<script type="application/ld+json">{ld_json}</script>\n')
    # AdSense block
    parts.append('<!-- ekguru:adsense:start -->\n')
    parts.append('<!-- Auto ads: one account loader, and Google places the units. Whether\n')
    parts.append('     this block is in the page at all is decided by the page class\n')
    parts.append('     (html[data-ad-class]) and data/monetization/google-monetization.json\n')
    parts.append('     -> ad_policy. tools/inject-ads.py enforces it. -->\n')
    parts.append('<link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin>\n')
    parts.append('<link rel="preconnect" href="https://googleads.g.doubleclick.net" crossorigin>\n')
    parts.append('<meta name="google-adsense-account" content="ca-pub-8175326569491671">\n')
    parts.append('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8175326569491671" crossorigin="anonymous"></script>\n')
    parts.append('<!-- ekguru:adsense:end -->\n')
    parts.append('<!-- ekguru:ultra-assets:start -->\n')
    parts.append('<link rel="stylesheet" href="/css/tokens.css">\n')
    parts.append('<link rel="stylesheet" href="/css/ultra.css">\n')
    parts.append('<!-- ekguru:ultra-assets:end -->\n')
    parts.append('</head>\n')

    # --- body + shell header ---
    parts.append('<body>\n')
    parts.append('<!-- ekguru:shell-header:start -->\n')
    parts.append('<header class="hdr">\n')
    parts.append('  <a class="skip" href="#main">Skip to content</a>\n')
    parts.append('  <div class="hdr-in">\n')
    parts.append('    <a class="logo" href="../../index.html">\n')
    parts.append('      <img class="logo-img" src="../../images/logo.svg" width="38" height="38" alt="EkGuru">\n')
    parts.append('      <span><span data-brand>EkGuru</span><small data-tagline>One Student. One Goal. One Guru.</small></span>\n')
    parts.append('    </a>\n')
    parts.append('    <button class="burger" type="button" aria-label="Menu" aria-expanded="false"><span></span></button>\n')
    parts.append('    <nav class="nav" aria-label="Main">\n')
    parts.append('      <a href="../../index.html">Home</a>\n')
    parts.append('      <a href="../../learn/">Learn</a>\n')
    parts.append('      <a href="../../find-tutors.html">Tutors</a>\n')
    parts.append('      <a href="../../about/">About</a>\n')
    parts.append('      <a href="../../contact/">Contact</a>\n')
    parts.append('      <a class="btn btn-primary btn-sm" href="../../find-tutors.html">Find tutors</a>\n')
    parts.append('    </nav>\n')
    parts.append('  </div>\n')
    parts.append('</header>\n')
    parts.append('<script src="../../js/site-shell.js" defer></script>\n')
    parts.append('<script src="../../js/copywatch.js" defer></script>\n')
    parts.append('<!-- ekguru:shell-header:end -->\n')

    # --- main content ---
    parts.append('<main id="main">\n')
    parts.append('<div class="art">\n')
    parts.append('<!-- ekguru:pw-bands:start -->\n')

    # Breadcrumb
    parts.append(f'<p class="crumb"><a href="../../">EkGuru</a> › <a href="../../learn/">Learn Hindi</a> › <a href="../../learn-hindi-by-country/">By country</a> › <a href="../">{esc(country_name)}</a> › Daily phrases</p>\n')

    # H1 + lede
    parts.append(f'<h1>Hindi Daily Phrases for {esc(country_name)}</h1>\n\n')
    parts.append(f'<p class="lede">Learn the 39 Hindi phrases you will actually use every day in {esc(country_name)} — greetings, everyday questions, polite expressions, and common statements. Each phrase links to a full guide with usage notes and pronunciation tips.</p>\n\n')

    # Phrase sections
    for section_name, phrases in SECTIONS:
        parts.append(f'<h2>{esc(section_name)}</h2>\n')
        parts.append('<table class="tbl">\n')
        parts.append('<tr><th>English</th><th>Hindi</th><th>Sounds like</th><th>Learn more</th></tr>\n')
        for slug, label, hindi, roman in phrases:
            ask_url = f"../../../ask/how-to-say-{slug}-in-hindi/"
            parts.append(
                f'<tr><td>{esc(label)}</td>'
                f'<td class="dv">{esc(hindi)}</td>'
                f'<td>{esc(roman)}</td>'
                f'<td><a href="{ask_url}">How to say it</a></td></tr>\n'
            )
        parts.append('</table>\n\n')

    # FAQ section
    parts.append('<h2>Frequently asked questions</h2>\n')
    for q, a in FAQ_PAIRS:
        parts.append(f'<h3>{esc(q)}</h3>\n')
        parts.append(f'<p>{esc(a)}</p>\n')

    # CTA
    parts.append(f'<p><a class="btn btn-primary" href="../">Back to learning Hindi from {esc(country_name)}</a></p>\n')
    parts.append(f'<p>Ready to go deeper? <a href="../../learn/hindi/">Open the free Hindi course</a> or <a href="../../ask/">browse all Hindi questions</a>.</p>\n')

    parts.append('<!-- ekguru:pw-bands:end -->\n')
    parts.append('</div>\n')
    parts.append('</main>\n')

    # --- shell footer ---
    parts.append('<!-- ekguru:ultra-appearance:start -->\n')
    parts.append('<section class="eg-appearance" lang="en" dir="ltr" data-eg-chrome="appearance"><label>Appearance <select data-eg-theme><option value="system">System</option><option value="light">Light</option><option value="dark">Dark</option><option value="contrast">High contrast</option></select></label> · <a href="/editorial-policy/" hreflang="en">Editorial policy</a> · <a href="/learn/progress/" hreflang="en">Learning journal</a></section>\n')
    parts.append('<!-- ekguru:ultra-appearance:end -->\n')
    parts.append('<!-- ekguru:shell-footer:start -->\n')
    parts.append('<footer class="ftr">\n')
    parts.append('  <div class="wrap ftr-in">\n')
    parts.append('    <div>\n')
    parts.append('      <a class="logo" href="../../index.html">\n')
    parts.append('        <img class="logo-img" src="../../images/logo.svg" width="38" height="38" alt="EkGuru">\n')
    parts.append('        <span><span data-brand>EkGuru</span><small data-tagline>One Student. One Goal. One Guru.</small></span>\n')
    parts.append('      </a>\n')
    parts.append('      <p style="margin-top:14px">Online Hindi lessons with independent tutor profiles.</p>\n')
    parts.append('    </div>\n')
    parts.append('    <div>\n')
    parts.append('      <h3>Site</h3>\n')
    parts.append('      <a href="../../index.html">Home</a>\n')
    parts.append('      <a href="../../find-tutors.html">Find Tutors</a>\n')
    parts.append('      <a href="../../join.html">Become a tutor</a>\n')
    parts.append('      <a href="../../tutor/">All tutors — text directory</a>\n')
    parts.append('      <a href="../../hindi-tutor/">Hindi tutors by location</a>\n')
    parts.append('      <a href="../../search/">Search the site</a>\n')
    parts.append('    </div>\n')
    parts.append('    <div>\n')
    parts.append('      <h3>Learn Hindi</h3>\n')
    parts.append('      <a href="../../learn/hindi/">Learn Hindi — everything in one place</a>\n')
    parts.append('      <a href="../../learn/">Every language, one page</a>\n')
    parts.append('      <a href="../../learn/hindi/#hh-topics">Hindi topics — all 34 chapters</a>\n')
    parts.append('      <a href="../../toolbox/">Interactive tools</a>\n')
    parts.append('      <a href="../../daily-hindi/">Daily Hindi — 30 days</a>\n')
    parts.append('      <a href="../../ask/">Questions answered</a>\n')
    parts.append('      <a href="../../answers/">Short answers</a>\n')
    parts.append('      <a href="../../learn/countries/">Published country guides</a>\n')
    parts.append('    </div>\n')
    parts.append('    <div>\n')
    parts.append('      <h3>Contact &amp; legal</h3>\n')
    parts.append('      <a href="../../contact/">Contact form</a>\n')
    parts.append('      <a href="mailto:EkGuruLearning@gmail.com">EkGuruLearning@gmail.com</a>\n')
    parts.append('      <a href="mailto:support@ekguru.shop">support@ekguru.shop</a>\n')
    parts.append('      <a href="../../about/">About EkGuru</a>\n')
    parts.append('      <a href="../../privacy/">Privacy policy</a>\n')
    parts.append('      <a href="../../terms/">Terms of use</a>\n')
    parts.append('      <a href="../../monetization-disclosure/">Monetisation disclosure</a>\n')
    parts.append('      <a href="../../disclaimer/">Disclaimer</a>\n')
    parts.append('      <a href="../../copyright/">Copyright</a>\n')
    parts.append('      <a href="../../cookie-policy/">Cookie policy</a>\n')
    parts.append('    </div>\n')
    parts.append('  </div>\n')
    parts.append('  <div class="wrap ftr-bot">\n')
    parts.append('    <p class="ftr-founder">Written and maintained by Prakash in Jaipur, India.</p>\n')
    parts.append('    <p>© <span data-year>2026</span> <span data-brand>EkGuru</span> — <span data-tagline>One Student. One Goal. One Guru.</span></p>\n')
    parts.append('  </div>\n')
    parts.append('</footer>\n')
    parts.append('<!-- ekguru:shell-footer:end -->\n')
    parts.append('<script src="../../js/monetization.js" defer></script>\n')
    parts.append('<script src="../../js/print-sheet.js" defer></script>\n')
    parts.append('<script src="../../js/level-visuals.js" defer></script>\n')
    parts.append('<script src="../../js/visual-learning.js" defer></script>\n')
    parts.append('<script src="../../js/practice-api.js" defer></script>\n')
    parts.append('<script src="../../js/refresh-guard.js" defer></script>\n')
    parts.append('<script src="../../js/course-player.js" defer></script>\n')
    parts.append('<script src="../../js/adaptive-practice.js" defer></script>\n')
    parts.append('<script src="../../js/global-srs.js" defer></script>\n')
    parts.append('</body>\n')
    parts.append('</html>\n')

    return "".join(parts)


def main():
    check_only = "--check" in sys.argv
    countries = get_countries()
    written = 0
    stale = 0

    for c in countries:
        out_dir = ROOT / f"learn-hindi-from-{c['slug']}" / "daily-phrases"
        out_file = out_dir / "index.html"
        html = build_page(c["slug"], c["name"])

        if check_only:
            if not out_file.exists() or out_file.read_text(encoding="utf-8") != html:
                print(f"STALE {out_file.relative_to(ROOT)}")
                stale += 1
        else:
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file.write_text(html, encoding="utf-8")
            written += 1

    if check_only:
        if stale:
            print(f"stale: {stale} page(s)")
            sys.exit(1)
        print(f"all {len(countries)} country daily-phrases pages current")
    else:
        print(f"wrote {written} country daily-phrases page(s)")


if __name__ == "__main__":
    main()

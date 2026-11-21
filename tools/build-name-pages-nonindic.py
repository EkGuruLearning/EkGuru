#!/usr/bin/env python3
"""Generate name-in-<lang> pages for non-Indic scripts.

The Indic name pages (name-in-hindi, name-in-punjabi) convert
through Devanagari via script-map.js. Non-Indic scripts — Arabic,
Greek, Cyrillic, Hangul, Kana, Ethiopic — have entirely different
orthographies and use the engine in js/non-indic-scripts.js instead.

Each page is self-contained, inline-styled, and loads the same
controller (js/name-in-script.js) with a different data-script.
The controller is script-agnostic: it reads data-script and routes
to the correct engine.

  python3 tools/build-name-pages-nonindic.py
  python3 tools/build-name-pages-nonindic.py --check
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "name-in-arabic"

# Each entry: (slug, display_name, script_key, variant, description, howto_steps, faq)
PAGES = [
    {
        "slug": "name-in-arabic",
        "title": "Write Your Name in Arabic — Free Tool | EkGuru",
        "description": "Type your name and see it written in Arabic script instantly, with the spelling Arabic speakers actually use. Free, works offline, nothing to sign up for.",
        "script": "arabic",
        "variant": None,
        "display": "Arabic",
        "howto_name": "How to write your name in Arabic",
        "howto_desc": "Transliterate an English name into Arabic script, sound by sound.",
        "howto_steps": [
            ("Say the name aloud", "Arabic is written phonetically. Ignore the English spelling and read the sounds: 'John' is the sounds j-aw-n, not letter by letter."),
            ("Map consonants first", "Arabic is an abjad — consonants carry meaning and vowels are written as diacritics. Each consonant gets its letter, then vowel marks are added on top."),
            ("Add vowel diacritics", "Short vowels use small marks above or below the consonant. Long vowels use alif (ا), waw (و), or ya (ي). The full diacritics make the reading unambiguous."),
            ("Handle ligatures", "Some letter pairs connect. The tool writes each word as a connected sequence, the way it appears in real Arabic text."),
        ],
        "faq": [
            ("Why does my name look different in Arabic than in English?",
             "Because Arabic is an abjad — consonants carry the meaning and vowels are written as small marks. English writes vowels as full letters, so the same name can look longer or shorter in Arabic. The diacritics are there to tell you exactly how to read it."),
            ("Is there one correct Arabic spelling of my name?",
             "No. Arabic has several dialects and many spelling conventions. What matters is that an Arabic speaker reading it aloud produces your name. This tool writes the standard phonetic spelling, and for common names the curated list gives the spelling people actually use."),
            ("Does this work for non-Arabic names?",
             "Yes, by sound. It works reasonably well for most names, but it is weakest on sounds Arabic does not have — like the English 'v' (Arabic uses ف for both v and f) or the German 'ch'."),
            ("Can I write a full name, first and last?",
             "Yes. Type both words. Each word is converted separately and the space is kept, which is correct in Arabic too."),
            ("Why are some letters connected?",
             "Arabic letters connect to the next letter when the preceding letter allows it. This is normal Arabic orthography — the tool writes the connected form so it reads correctly."),
        ],
    },
    {
        "slug": "name-in-greek",
        "title": "Write Your Name in Greek — Free Tool | EkGuru",
        "description": "Type your name and see it written in Greek script instantly, with the spelling Greek speakers actually use. Free, works offline, nothing to sign up for.",
        "script": "greek",
        "variant": None,
        "display": "Greek",
        "howto_name": "How to write your name in Greek",
        "howto_desc": "Transliterate an English name into Greek script, sound by sound.",
        "howto_steps": [
            ("Say the name aloud", "Greek is written phonetically. Ignore the English spelling and read the sounds: 'John' is the sounds j-o-n, mapped to Greek letters by sound."),
            ("Map consonants to Greek letters", "English consonants map to Greek equivalents: b→β, p→π, t→τ, d→δ, th→θ, g→γ, k→κ, l→λ, m→μ, n→ν, s→σ, z→ζ, r→ρ, f→φ, v→β."),
            ("Map vowels", "Greek has five vowels: a→α, e→ε, i→ι, o→ο, u→υ. English 'u' usually becomes ου or υ depending on the name."),
            ("Handle digraphs", "English 'ch', 'th', 'ph', 'ps' each map to a single Greek letter: χ, θ, φ, ψ respectively."),
        ],
        "faq": [
            ("Why does my name look different in Greek than in English?",
             "Greek has its own alphabet with different letters. The mapping is phonetic — English sounds map to Greek letters that produce the closest sound. Some names look longer or shorter because Greek does not have a direct equivalent for every English letter."),
            ("Is there one correct Greek spelling of my name?",
             "No. Personal names have no official spelling. What matters is that a Greek speaker reading it aloud produces your name. This tool writes the standard phonetic spelling."),
            ("Does this work for non-English names?",
             "Yes, by sound. It works well for most names. It is weakest on sounds Greek does not have — like the English 'v', which uses the same letter as 'b' (β) in modern Greek."),
            ("Can I write a full name, first and last?",
             "Yes. Type both words. Each word is converted separately and the space is kept."),
        ],
    },
    {
        "slug": "name-in-russian",
        "title": "Write Your Name in Russian (Cyrillic) — Free Tool | EkGuru",
        "description": "Type your name and see it written in Russian Cyrillic script instantly, with the spelling Russian speakers actually use. Free, works offline, nothing to sign up for.",
        "script": "cyrillic",
        "variant": "ru",
        "display": "Russian",
        "howto_name": "How to write your name in Russian",
        "howto_desc": "Transliterate an English name into Russian Cyrillic script, sound by sound.",
        "howto_steps": [
            ("Say the name aloud", "Russian is written phonetically. Ignore the English spelling and read the sounds: 'John' is the sounds j-o-n, mapped to Cyrillic by sound."),
            ("Map consonants to Cyrillic", "English consonants map to Cyrillic equivalents: b→б, p→п, t→т, d→д, th→т, g→г, k→к, l→л, m→м, n→н, s→с, z→з, r→р, f→ф, v→в, c→ц."),
            ("Map vowels", "Cyrillic vowels map directly: a→а, e→е, i→и, o→о, u→у. English 'y' becomes й."),
            ("Handle diphthongs", "English 'yu' becomes ю, 'ya' becomes я, 'ye' becomes е, 'yo' becomes ё. These are common in transliterated names."),
        ],
        "faq": [
            ("Why does my name look different in Russian than in English?",
             "Cyrillic is a separate alphabet with its own letters. The mapping is phonetic — English sounds map to Cyrillic letters that produce the closest sound. Some names look longer because Cyrillic sometimes needs two letters for one English sound."),
            ("Is there one correct Russian spelling of my name?",
             "No. Personal names have no official spelling. What matters is that a Russian speaker reading it aloud produces your name. This tool writes the standard phonetic spelling."),
            ("Does this work for non-English names?",
             "Yes, by sound. It works well for most names. It is weakest on sounds Russian does not have — like the English 'w', which is written as в, or the 'th' sound."),
            ("Can I write a full name, first and last?",
             "Yes. Type both words. Each word is converted separately and the space is kept."),
        ],
    },
    {
        "slug": "name-in-korean",
        "title": "Write Your Name in Korean (Hangul) — Free Tool | EkGuru",
        "description": "Type your name and see it written in Korean Hangul script instantly, with the spelling Korean speakers actually use. Free, works offline, nothing to sign up for.",
        "script": "hangul",
        "variant": None,
        "display": "Korean",
        "howto_name": "How to write your name in Korean",
        "howto_desc": "Transliterate an English name into Hangul script, sound by sound.",
        "howto_steps": [
            ("Say the name aloud", "Hangul is written phonetically. Ignore the English spelling and read the sounds. Each syllable of the name becomes one Hangul block."),
            ("Break into syllables", "Hangul writes one syllable per block. A name like 'John' is one syllable; 'Sarah' is two. Each block is built from an initial consonant, a vowel, and optional final consonant."),
            ("Build each block", "Each Hangul block combines an initial consonant (ㄱ, ㄴ, ㄷ, etc.), a vowel (ㅏ, ㅓ, ㅗ, etc.), and an optional final consonant. The tool constructs the correct block for each syllable."),
            ("Check the final consonant", "Not every syllable has a final consonant. If the syllable ends in a vowel sound, the block has no final. The tool handles this automatically."),
        ],
        "faq": [
            ("Why does my name look different in Korean than in English?",
             "Hangul is a syllabic alphabet — each syllable is written as a single block combining an initial consonant, a vowel, and an optional final consonant. The same sounds look very different from Latin letters because they are grouped into syllable blocks."),
            ("Is there one correct Korean spelling of my name?",
             "No. Personal names have no official spelling in Hangul. What matters is that a Korean speaker reading it aloud produces your name. This tool writes the standard phonetic spelling."),
            ("Does this work for non-English names?",
             "Yes, by sound. It works well for most names. It is weakest on sounds Korean does not have — like the 'f' sound, which Koreans usually write with the 'p' consonant."),
            ("Can I write a full name, first and last?",
             "Yes. Type both words. Each word is converted separately and the space is kept."),
        ],
    },
    {
        "slug": "name-in-japanese",
        "title": "Write Your Name in Japanese (Kana) — Free Tool | EkGuru",
        "description": "Type your name and see it written in Japanese kana script instantly, with the spelling Japanese speakers actually use. Free, works offline, nothing to sign up for.",
        "script": "kana",
        "variant": None,
        "display": "Japanese",
        "howto_name": "How to write your name in Japanese",
        "howto_desc": "Transliterate an English name into Japanese kana script, sound by sound.",
        "howto_steps": [
            ("Say the name aloud", "Kana is written phonetically. Ignore the English spelling and read the sounds. Each syllable of the name becomes one kana character."),
            ("Map to hiragana", "This tool uses hiragana, the phonetic script used for native Japanese words. Each syllable — a consonant plus vowel, or just a vowel — gets one kana character."),
            ("Handle consonant-vowel pairs", "Kana syllables are either a vowel alone (あ, い, う, え, お) or a consonant + vowel (か, き, く, け, こ). The tool maps each English sound to the correct kana."),
            ("Handle digraphs", "English 'ch', 'sh', 'ts' each map to a single kana: ち, し, つ. Palatalized sounds like 'ky' or 'py' map to their own kana."),
        ],
        "faq": [
            ("Why does my name look different in Japanese than in English?",
             "Kana is a syllabic script — each syllable is one character. The same sounds look very different from Latin letters because they are grouped into syllables. Each English sound maps to the kana that produces the closest sound."),
            ("Is there one correct Japanese spelling of my name?",
             "No. Foreign names in Japanese are written phonetically and there is no official spelling. What matters is that a Japanese speaker reading it aloud produces your name. This tool writes the standard phonetic spelling."),
            ("Why use kana and not kanji?",
             "Kana is the phonetic script — it can represent any sound. Kanji characters carry meaning and there is no standard set for foreign names. Most foreign names in Japanese are written in kana, sometimes followed by kanji in parentheses for the meaning."),
            ("Does this work for non-English names?",
             "Yes, by sound. It works well for most names. It is weakest on sounds Japanese does not have — like the 'v' sound, which Japanese writes as a blend of 'b' and 'u'."),
            ("Can I write a full name, first and last?",
             "Yes. Type both words. Each word is converted separately and the space is kept."),
        ],
    },
    {
        "slug": "name-in-amharic",
        "title": "Write Your Name in Amharic (Ethiopic) — Free Tool | EkGuru",
        "description": "Type your name and see it written in Amharic Ethiopic script instantly, with the spelling Amharic speakers actually use. Free, works offline, nothing to sign up for.",
        "script": "ethiopic",
        "variant": None,
        "display": "Amharic",
        "howto_name": "How to write your name in Amharic",
        "howto_desc": "Transliterate an English name into Ethiopic script, sound by sound.",
        "howto_steps": [
            ("Say the name aloud", "Amharic is written phonetically. Ignore the English spelling and read the sounds. Each consonant-vowel pair becomes one Ethiopic glyph."),
            ("Map consonants", "Ethiopic has 26 basic consonants. Each English consonant maps to the Ethiopic letter with the closest sound. The tool builds the consonant for each sound."),
            ("Add vowel marks", "Ethiopic is an abugida — each consonant carries a default vowel, and vowel marks change it. The tool adds the correct vowel mark for each vowel sound."),
            ("Combine into glyphs", "Each consonant-vowel pair is written as a single glyph. The tool combines them into the correct Amharic characters."),
        ],
        "faq": [
            ("Why does my name look different in Amharic than in English?",
             "Ethiopic is an abugida — each consonant carries a built-in vowel, and vowel marks modify it. The same sounds look very different from Latin letters because they are written as consonant-vowel units."),
            ("Is there one correct Amharic spelling of my name?",
             "No. Personal names have no official spelling. What matters is that an Amharic speaker reading it aloud produces your name. This tool writes the standard phonetic spelling."),
            ("Does this work for non-English names?",
             "Yes, by sound. It works well for most names. It is weakest on sounds Amharic does not have — like the 'v' sound, which Amharic writes with the same letter as 'f'."),
            ("Can I write a full name, first and last?",
             "Yes. Type both words. Each word is converted separately and the space is kept."),
        ],
    },
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def json_ld(page: dict) -> str:
    slug = page["slug"]
    url = f"https://ekguru.shop/{slug}/"
    steps_json = [
        {"@type": "HowToStep", "position": i + 1, "name": name, "text": text}
        for i, (name, text) in enumerate(page["howto_steps"])
    ]
    faq_json = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in page["faq"]
    ]
    graph = [
        {
            "@type": "WebApplication",
            "@id": f"{url}#app",
            "name": f"Write Your Name in {page['display']}",
            "url": url,
            "applicationCategory": "EducationalApplication",
            "operatingSystem": "Any",
            "description": f"Free tool that writes any name in {page['display']} and explains the spelling.",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "publisher": {"@type": "Organization", "name": "EkGuru", "url": "https://ekguru.shop/"},
            "inLanguage": "en",
            "isAccessibleForFree": True,
        },
        {
            "@type": "HowTo",
            "@id": f"{url}#howto",
            "name": page["howto_name"],
            "description": page["howto_desc"],
            "totalTime": "PT2M",
            "step": steps_json,
        },
        {
            "@type": "FAQPage",
            "@id": f"{url}#faq",
            "mainEntity": faq_json,
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{url}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "EkGuru", "item": "https://ekguru.shop/"},
                {"@type": "ListItem", "position": 2, "name": f"Write your name in {page['display']}", "item": url},
            ],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def placeholder_native(page: dict) -> str:
    """Placeholder text in the target script."""
    script = page["script"]
    if script == "arabic":
        return "اسمك"
    if script == "greek":
        return "Το όνομά σας"
    if script == "cyrillic":
        return "Ваше имя"
    if script == "hangul":
        return "이름"
    if script == "kana":
        return "お名前"
    if script == "ethiopic":
        return "ስሙ"
    return "Your name"


def placeholder_rom(page: dict) -> str:
    """Placeholder text in roman script (English reading)."""
    script = page["script"]
    if script == "arabic":
        return 'ismak — "your name". Start typing above.'
    if script == "greek":
        return 'to onoma sas — "your name". Start typing above.'
    if script == "cyrillic":
        return 'Vashe ime — "your name". Start typing above.'
    if script == "hangul":
        return 'ireum — "your name". Start typing above.'
    if script == "kana":
        return 'onamae — "your name". Start typing above.'
    if script == "ethiopic":
        return 'simu — "your name". Start typing above.'
    return 'your name. Start typing above.'


def faq_html(page: dict) -> str:
    rows = ""
    for q, a in page["faq"]:
        rows += f'<details class="faq-item"><summary>{esc(q)}</summary><div class="faq-answer"><p>{esc(a)}</p></div></details>\n'
    return rows


def howto_html(page: dict) -> str:
    steps = ""
    for i, (name, text) in enumerate(page["howto_steps"]):
        steps += f'<li><b>{esc(name)}.</b> {esc(text)}</li>\n'
    return f'<ol class="howto">\n{steps}</ol>\n'


def render(page: dict) -> str:
    slug = page["slug"]
    url = f"https://ekguru.shop/{slug}/"
    script = page["script"]
    variant_attr = f' data-variant="{page["variant"]}"' if page["variant"] else ""
    ld = json_ld(page)
    p_native = placeholder_native(page)
    p_rom = placeholder_rom(page)
    faq = faq_html(page)
    howto = howto_html(page)

    theme_script = (
        "(function(){var t;try{t=localStorage.getItem('ekguru:theme:v2')}catch(e){}"
        "if(['light','dark','contrast'].indexOf(t)<0)t=typeof matchMedia==='function'"
        "&&matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';"
        "document.documentElement.dataset.theme=t;"
        "document.documentElement.classList.add('eg-js')})()"
    )

    return f"""<!DOCTYPE html>

<html dir="ltr" lang="en" data-ad-class="MEDIUM_CONTENT">
<head><!-- ekguru:ultra-head:start -->
<script>{theme_script}</script>
<script src="/js/voice-languages.js" defer></script>
<script src="/js/voice.js" defer></script>
<script src="/js/ui-motion.js" defer></script>
<!-- ekguru:ultra-head:end -->

<meta charset="utf-8"/>
<meta content="hFaqyp-9LdUXSKPA9RF011TkO2m_-7AUMasXqm_0dGI" name="google-site-verification"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>{esc(page['title'])}</title>
<meta content="{esc(page['description'])}" name="description"/>
<meta content="index, follow, max-snippet:-1, max-image-preview:large" name="robots"/>
<link href="{url}" rel="canonical"/>
<meta content="website" property="og:type"/>
<meta content="{esc(page['title'])}" property="og:title"/>
<meta content="{esc(page['description'])}" property="og:description"/>
<meta content="{url}" property="og:url"/>

           <meta content="https://ekguru.shop/images/og-cover.jpg" property="og:image"/>
           <meta property="og:image:width" content="1200">
           <meta property="og:image:height" content="630">
           <meta property="og:image:alt" content="EkGuru — free, self-paced Hindi learning">
<link href="../images/favicon.ico" rel="icon" sizes="any"/>
<link href="../manifest.webmanifest" rel="manifest"/>
<link href="../images/apple-touch-icon.png" rel="apple-touch-icon"/>
<meta content="#4f32d9" name="theme-color"/>
<link href="../css/site.css" rel="stylesheet" type="text/css"/>

<script type="application/ld+json">{ld}</script>

<style>
.name-tool-wrap {{ max-width: 720px; margin: 0 auto; padding: 24px 20px; }}
.name-tool-wrap h1 {{ font-size: 1.6rem; margin: 0 0 6px; line-height: 1.3; }}
.name-tool-wrap .lede {{ font-size: 1rem; color: #555; margin: 0 0 28px; line-height: 1.5; }}
.name-tool-card {{ background: #fff; border: 1px solid #e0e0e0; border-radius: 12px; padding: 28px; margin-bottom: 32px; }}
.name-tool-card label {{ display: block; font-weight: 600; font-size: 0.95rem; margin-bottom: 8px; }}
.name-tool-card input[type="text"] {{ width: 100%; box-sizing: border-box; padding: 12px 14px; font-size: 1.1rem; border: 2px solid #d0d0d0; border-radius: 8px; outline: none; transition: border-color 0.15s; }}
.name-tool-card input[type="text"]:focus {{ border-color: #4f32d9; }}
.name-tool-card .help {{ font-size: 0.82rem; color: #888; margin: 8px 0 16px; }}
.name-tool-out {{ min-height: 60px; margin-bottom: 12px; }}
.name-tool-out .big {{ font-size: 2.2rem; font-weight: 700; line-height: 1.3; margin-bottom: 4px; }}
.name-tool-out .rom {{ font-size: 0.95rem; color: #666; }}
.btnrow {{ display: flex; gap: 8px; margin-top: 12px; }}
.btnrow button {{ padding: 8px 16px; font-size: 0.88rem; border: 1px solid #d0d0d0; border-radius: 6px; background: #f5f5f5; cursor: pointer; transition: background 0.15s; }}
.btnrow button:hover {{ background: #e8e8e8; }}
.explain {{ margin-top: 16px; padding-top: 16px; border-top: 1px solid #eee; font-size: 0.88rem; }}
.explain table.ex {{ width: 100%; border-collapse: collapse; }}
.explain table.ex th, .explain table.ex td {{ border: 1px solid #e0e0e0; padding: 6px 8px; text-align: left; }}
.explain table.ex th {{ background: #f5f5f5; }}
.explain .rom {{ color: #888; }}
.section-title {{ font-size: 1.2rem; margin: 32px 0 12px; }}
.howto {{ padding-left: 20px; line-height: 1.6; }}
.howto li {{ margin-bottom: 8px; }}
.faq-item {{ border: 1px solid #e0e0e0; border-radius: 8px; margin-bottom: 8px; padding: 0; }}
.faq-item summary {{ padding: 12px 16px; font-weight: 600; cursor: pointer; font-size: 0.95rem; }}
.faq-item[open] summary {{ border-bottom: 1px solid #eee; }}
.faq-answer {{ padding: 12px 16px; font-size: 0.9rem; line-height: 1.5; color: #444; }}
.footer-links {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 0.85rem; }}
.footer-links a {{ color: #4f32d9; text-decoration: none; }}
.footer-links a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<main class="name-tool-wrap" data-template="name-in-script">

<h1>Write Your Name in {esc(page['display'])}</h1>
<p class="lede">Type your name and see it written in {esc(page['display'])} script instantly. Free, works offline, nothing to sign up for.</p>

<div class="name-tool-card">
  <label for="nameIn">Your name</label>
  <input aria-describedby="outHelp" autocomplete="off" id="nameIn" data-script="{script}" data-placeholder-native="{esc(p_native)}" data-placeholder-rom="{esc(p_rom)}"{variant_attr} placeholder="e.g. Sarah, Michael, Priya" spellcheck="false" type="text"/>
  <div class="help" id="outHelp">Type any name — first name, full name, or surname.</div>
  <div aria-live="polite" class="name-tool-out" id="out">
    <div class="big">{esc(p_native)}</div>
    <div class="rom">{esc(p_rom)}</div>
  </div>
  <div class="btnrow" id="btnrow" hidden>
    <button id="copyBtn" type="button">Copy</button>
    <button id="explainBtn" type="button">Show every letter</button>
  </div>
  <div class="explain" id="explain" data-open="0"></div>
</div>

<h2 class="section-title">{esc(page['howto_name'])}</h2>
{howto}

<h2 class="section-title">Questions people ask</h2>
{faq}

<div class="footer-links">
  <a href="../learn/">All free guides</a> · <a href="../ask/">Questions people ask before they start</a> · <a href="../name-in-hindi/">Write your name in Hindi</a> · <a href="../name-in-punjabi/">Write your name in Punjabi</a>
</div>

</main>

<script defer src="../js/translit.js"></script>
<script defer src="../js/non-indic-scripts.js"></script>
<script defer src="../js/names-data.js"></script>
<script defer src="../js/name-in-script.js"></script>

</body>
</html>
"""


def strip_shell(html: str) -> str:
    """Remove the site shell header/footer blocks that build-shell.js
    adds after generation, plus the ultra decoration blocks that
    apply-ultra.py injects, plus the data-learning-language attribute,
    so --check compares only the generated content against the file."""
    import re
    # Ultra head/foot blocks
    html = re.sub(
        r"<!-- ekguru:ultra-head:start -->.*?<!-- ekguru:ultra-head:end -->\n?",
        "", html, flags=re.DOTALL)
    html = re.sub(
        r"<!-- ekguru:ultra-foot:start -->.*?<!-- ekguru:ultra-foot:end -->\n?",
        "", html, flags=re.DOTALL)
    # AdSense block
    html = re.sub(
        r"<!-- ekguru:adsense:start -->.*?<!-- ekguru:adsense:end -->\n?",
        "", html, flags=re.DOTALL)
    # Ultra assets block
    html = re.sub(
        r"<!-- ekguru:ultra-assets:start -->.*?<!-- ekguru:ultra-assets:end -->\n?",
        "", html, flags=re.DOTALL)
    # Ultra byline block
    html = re.sub(
        r"<!-- ekguru:ultra-byline:start -->.*?<!-- ekguru:ultra-byline:end -->\n?",
        "", html, flags=re.DOTALL)
    # Ultra appearance block
    html = re.sub(
        r"<!-- ekguru:ultra-appearance:start -->.*?<!-- ekguru:ultra-appearance:end -->\n?",
        "", html, flags=re.DOTALL)
    # Shell header/footer blocks
    html = re.sub(
        r"<!-- ekguru:shell-header:start -->.*?<!-- ekguru:shell-header:end -->\n?",
        "", html, flags=re.DOTALL)
    html = re.sub(
        r"<!-- ekguru:shell-footer:start -->.*?<!-- ekguru:shell-footer:end -->\n?",
        "", html, flags=re.DOTALL)
    # Strip the data-learning-language attribute that apply-ultra injects
    html = re.sub(r' data-learning-language="[^"]*"', "", html, count=1)
    # Strip the id="main" that the shell injects on <main>
    html = re.sub(r'<main(?=[\s>])', '<main', html, count=1)
    html = html.replace('<main id="main" ', '<main ', 1)
    return html


def main() -> int:
    check = "--check" in sys.argv
    generated = {}
    for page in PAGES:
        slug = page["slug"]
        body = render(page)
        generated[slug] = body
        path = ROOT / slug / "index.html"

        if check:
            if not path.exists():
                print(f"MISSING {path.relative_to(ROOT)} — run: python3 tools/build-name-pages-nonindic.py")
                return 1
            on_disk = strip_shell(path.read_text(encoding="utf-8"))
            generated_stripped = strip_shell(body)
            if on_disk != generated_stripped:
                print(f"STALE {path.relative_to(ROOT)} — run: python3 tools/build-name-pages-nonindic.py")
                return 1
            print(f"ok    {slug}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
            print(f"wrote {slug}/index.html ({len(body) // 1024} KB)")

    if check:
        print(f"ok    all {len(PAGES)} pages current")
        return 0
    print(f"done  {len(PAGES)} pages generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

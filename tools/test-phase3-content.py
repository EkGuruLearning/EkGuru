#!/usr/bin/env python3
"""PHASE 3 acceptance test — the Learn tab's long-form posts.

The AdSense command (PHASE3) asks for ten blog-style posts per language, each at
least 1000 words, with headings, real examples in the target script plus
romanisation or a suitable pronunciation aid, a mistakes section, practice material and internal links.

For each of the nine Indian course packs, five posts already had a page
(beginner / pronunciation / grammar / travel / numbers); this phase deepened
them and added five more (common words, mistakes, reading, vs-Hindi, speaking
alone). Those pages are generated from the authored course data.

This test is the phase's own gate. Run:  python3 tools/test-phase3-content.py

It checks, for every Indian course pack:
  · all ten posts exist as real pages and each is at least 1000 words
  · each is a readable article: one <main>, one <h1>, and at least four <h2>s
  · each links to at least two other guides and is linked from its hub
  · the five NEW pages are noindex, and the five deepened pages retain the
    indexability in the owner's immutable baseline

Hindi's ten hand-authored mappings receive structure, length, sibling-link,
and direct-hub-link checks; its two newly added pages remain noindex.
Spanish, Arabic and German have hand-authored world-course sets of ten long-form
posts each; all thirty posts and their hubs remain noindex pending review. Their
pages receive length, structure, hub-link and sibling-link checks. Arabic guides
need marked right-to-left examples and explicit MSA context. German guides need
marked German examples and a learner pronunciation note (German already uses the
Latin alphabet). Both tracks also need clearly headed mistakes and practice sections.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIN_WORDS = 1000

EXISTING = ["beginner", "pronunciation", "grammar", "travel", "numbers"]
NEW = ["common-words", "mistakes", "reading", "vs-hindi", "speaking-alone"]
POSTS = EXISTING + NEW

# Hindi's learn/ guides are hand-authored rather than generated from a pack, and
# they live at the top level (learn/<slug>/) instead of learn/hindi/<slug>/, so the
# ten post types map onto their own URLs. Eight already existed; the last two were
# written by tools/build-hindi-phase3-posts.py.
HINDI_NEW = {"common-words", "speaking-alone"}   # the two pages this phase added
HINDI = {
    "beginner": "learn-hindi-online-guide",
    "pronunciation": "hindi-alphabet-for-beginners",
    "grammar": "hindi-sentence-structure",
    "travel": "hindi-phrases-for-travel",
    "numbers": "hindi-numbers-1-to-100",
    "common-words": "hindi-100-most-common-words",
    "mistakes": "common-hindi-mistakes",
    "reading": "hindi-barakhadi",
    "vs-hindi": "hindi-or-urdu-difference",
    "speaking-alone": "hindi-speaking-practice-alone",
}
SPANISH = ["beginner", "pronunciation", "common-words", "grammar", "mistakes",
           "travel", "reading", "vs-hindi", "speaking-alone", "numbers"]
ARABIC = ["beginner", "pronunciation", "common-words", "grammar", "mistakes",
          "travel", "reading", "vs-hindi", "speaking-alone", "numbers"]
GERMAN = ["beginner", "pronunciation", "common-words", "grammar", "mistakes",
          "travel", "reading", "vs-hindi", "speaking-alone", "numbers"]
ARABIC_BDI_RE = re.compile(
    r'<bdi\b(?=[^>]*\blang=["\']ar["\'])(?=[^>]*\bdir=["\']rtl["\'])[^>]*>(.*?)</bdi>',
    re.I | re.S,
)
ARABIC_SCRIPT_RE = re.compile(r"[\u0600-\u06FF]")
GERMAN_SPAN_RE = re.compile(
    r'<span\b(?=[^>]*\blang=["\']de["\'])[^>]*>(.*?)</span>', re.I | re.S,
)
GERMAN_TEXT_RE = re.compile(r"[A-Za-zÄÖÜäöüß]+")
WORD_RE = re.compile(r"[A-Za-z\u0600-\u06FF\u0900-\u0DFF\u0E00-\u0E7F]+")
TAG_RE = re.compile(r"<[^>]+>")
DROP_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>|<!--.*?-->", re.S | re.I)
ROBOTS_RE = re.compile(r'<meta\b(?=[^>]*\bname=["\']robots["\'])[^>]*\bcontent=["\']([^"\']*)["\']', re.I)
H1_RE = re.compile(r"<h1\b", re.I)
H2_RE = re.compile(r"<h2\b", re.I)
MAIN_RE = re.compile(r"<main\b", re.I)


def words(html: str) -> int:
    text = TAG_RE.sub(" ", DROP_RE.sub(" ", html))
    return len(WORD_RE.findall(text))


def load_baseline() -> dict:
    path = ROOT / "data/quality/indexing-baseline.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8")).get("pages", {})


def main() -> int:
    packs = sorted((ROOT / "tools/lang-data").glob("*.json"))
    if not packs:
        print("FAIL: no language packs under tools/lang-data/")
        return 1
    baseline = load_baseline()
    problems: list[str] = []
    checked = 0
    shortest = ("", 10**9)

    for pack in packs:
        slug = pack.stem
        hub_path = ROOT / "learn" / slug / "index.html"
        hub = hub_path.read_text(encoding="utf-8") if hub_path.exists() else ""
        if not hub:
            problems.append(f"{slug}: hub learn/{slug}/index.html is missing")
            continue
        for post in POSTS:
            rel = f"learn/{slug}/{post}/index.html"
            p = ROOT / rel
            if not p.exists():
                problems.append(f"{rel}: missing")
                continue
            checked += 1
            html = p.read_text(encoding="utf-8")
            w = words(html)
            if w < MIN_WORDS:
                problems.append(f"{rel}: {w} words, needs {MIN_WORDS}")
            if w < shortest[1]:
                shortest = (rel, w)
            if len(H1_RE.findall(html)) != 1:
                problems.append(f"{rel}: needs exactly one <h1>")
            if len(MAIN_RE.findall(html)) != 1:
                problems.append(f"{rel}: needs exactly one <main>")
            if len(H2_RE.findall(html)) < 4:
                problems.append(f"{rel}: needs at least four <h2> sections")
            links = {q for q in POSTS if q != post and f'../{q}/' in html}
            if len(links) < 2:
                problems.append(f"{rel}: links to only {len(links)} other guide(s)")
            if f'href="{post}/"' not in hub and f'href="/learn/{slug}/{post}/"' not in hub:
                problems.append(f"{rel}: the course hub does not link to it")
            m = ROBOTS_RE.search(html)
            robots = (m.group(1).lower() if m else "")
            noindex = "noindex" in robots
            was_indexable = baseline.get(rel, {}).get("indexable")
            if post in NEW and not noindex:
                problems.append(f"{rel}: a new page must stay noindex (owner indexing contract)")
            if post in EXISTING and was_indexable is not None and noindex == was_indexable:
                # noindex True means "not indexable", so equal means the flag flipped
                problems.append(f"{rel}: indexability changed from the owner's baseline")

    # Hindi: hand-authored guides, mapped type -> URL above.
    hindi_checked = 0
    hub = (ROOT / "learn/hindi/index.html").read_text(encoding="utf-8")
    for kind, slug in HINDI.items():
        rel = f"learn/{slug}/index.html"
        p = ROOT / rel
        if not p.exists():
            problems.append(f"{rel}: missing (Hindi {kind})")
            continue
        checked += 1
        hindi_checked += 1
        html = p.read_text(encoding="utf-8")
        w = words(html)
        if w < MIN_WORDS:
            problems.append(f"{rel}: {w} words, needs {MIN_WORDS} (Hindi {kind})")
        if w < shortest[1]:
            shortest = (rel, w)
        if len(MAIN_RE.findall(html)) != 1:
            problems.append(f"{rel}: needs exactly one <main>")
        if len(H1_RE.findall(html)) != 1:
            problems.append(f"{rel}: needs exactly one <h1>")
        if len(H2_RE.findall(html)) < 4:
            problems.append(f"{rel}: needs at least four <h2> sections")
        links = {k for k, v in HINDI.items()
                 if v != slug and (f"/learn/{v}/" in html or f'../{v}/' in html)}
        if len(links) < 2:
            problems.append(f"{rel}: links to only {len(links)} other guide(s)")
        if (f'href="../{slug}/"' not in hub
                and f'href="/learn/{slug}/"' not in hub):
            problems.append(f"{rel}: the Hindi hub does not link to it")
        m = ROBOTS_RE.search(html)
        if kind in HINDI_NEW and not (m and "noindex" in m.group(1).lower()):
            problems.append(f"{rel}: a new Hindi page must stay noindex (owner indexing contract)")

    # World-course Phase 3 tracks: Spanish and Arabic, each with ten authored posts.
    spanish_hub_path = ROOT / "learn/spanish/index.html"
    spanish_hub = spanish_hub_path.read_text(encoding="utf-8") if spanish_hub_path.exists() else ""
    spanish_checked = 0
    learn_index = (ROOT / "learn/index.html").read_text(encoding="utf-8")
    if 'href="./spanish/"' not in learn_index:
        problems.append("learn/: Spanish long-form guide hub is not linked from the Learn home")
    if not spanish_hub:
        problems.append("Spanish: hub learn/spanish/index.html is missing")
    else:
        m = ROBOTS_RE.search(spanish_hub)
        if not (m and "noindex" in m.group(1).lower()):
            problems.append("learn/spanish/: new hub must stay noindex pending review")
        if 'href="/languages/es/course/"' not in spanish_hub:
            problems.append("learn/spanish/: hub must link to the Spanish course")
    for post in SPANISH:
        rel = f"learn/spanish/{post}/index.html"
        p = ROOT / rel
        if not p.exists():
            problems.append(f"{rel}: missing (Spanish Phase 3)")
            continue
        checked += 1
        spanish_checked += 1
        html = p.read_text(encoding="utf-8")
        w = words(html)
        if w < MIN_WORDS:
            problems.append(f"{rel}: {w} words, needs {MIN_WORDS} (Spanish)")
        if w < shortest[1]:
            shortest = (rel, w)
        if len(MAIN_RE.findall(html)) != 1:
            problems.append(f"{rel}: needs exactly one <main>")
        if len(H1_RE.findall(html)) != 1:
            problems.append(f"{rel}: needs exactly one <h1>")
        if len(H2_RE.findall(html)) < 4:
            problems.append(f"{rel}: needs at least four <h2> sections")
        links = {q for q in SPANISH if q != post and f"../{q}/" in html}
        if len(links) < 2:
            problems.append(f"{rel}: links to only {len(links)} other Spanish guide(s)")
        if (f'href="{post}/"' not in spanish_hub
                and f'href="/learn/spanish/{post}/"' not in spanish_hub):
            problems.append(f"{rel}: the Spanish hub does not link to it")
        if 'lang="es"' not in html:
            problems.append(f"{rel}: needs Spanish-language examples marked lang=es")
        m = ROBOTS_RE.search(html)
        if not (m and "noindex" in m.group(1).lower()):
            problems.append(f"{rel}: a new Spanish page must stay noindex pending review")

    # Arabic: world-course Phase 3 articles focus on MSA while qualifying the
    # substantial differences between formal writing and spoken regional dialects.
    arabic_hub_path = ROOT / "learn/arabic/index.html"
    arabic_hub = arabic_hub_path.read_text(encoding="utf-8") if arabic_hub_path.exists() else ""
    arabic_checked = 0
    for sitemap in ROOT.glob("sitemap*.xml"):
        sitemap_text = sitemap.read_text(encoding="utf-8")
        for world_slug in ("spanish", "arabic", "german"):
            if f"/learn/{world_slug}/" in sitemap_text:
                problems.append(f"{sitemap.name}: noindex {world_slug} Phase 3 pages must stay out of sitemaps")
    if 'href="./arabic/"' not in learn_index:
        problems.append("learn/: Arabic long-form guide hub is not linked from the Learn home")
    if not arabic_hub:
        problems.append("Arabic: hub learn/arabic/index.html is missing")
    else:
        m = ROBOTS_RE.search(arabic_hub)
        if not (m and "noindex" in m.group(1).lower()):
            problems.append("learn/arabic/: new hub must stay noindex pending review")
        if 'href="/languages/ar/course/"' not in arabic_hub:
            problems.append("learn/arabic/: hub must link to the Arabic course")
        if not ARABIC_BDI_RE.search(arabic_hub):
            problems.append("learn/arabic/: Arabic-script examples need lang=ar and dir=rtl")
        if ARABIC_SCRIPT_RE.search(ARABIC_BDI_RE.sub("", arabic_hub)):
            problems.append("learn/arabic/: Arabic-script text outside a lang=ar, dir=rtl example")
        if "transliteration" not in arabic_hub.lower():
            problems.append("learn/arabic/: hub must explain transliteration as a learner aid")

    for post in ARABIC:
        rel = f"learn/arabic/{post}/index.html"
        p = ROOT / rel
        if not p.exists():
            problems.append(f"{rel}: missing (Arabic Phase 3)")
            continue
        checked += 1
        arabic_checked += 1
        html = p.read_text(encoding="utf-8")
        w = words(html)
        if w < MIN_WORDS:
            problems.append(f"{rel}: {w} words, needs {MIN_WORDS} (Arabic)")
        if w < shortest[1]:
            shortest = (rel, w)
        if len(MAIN_RE.findall(html)) != 1:
            problems.append(f"{rel}: needs exactly one <main>")
        if len(H1_RE.findall(html)) != 1:
            problems.append(f"{rel}: needs exactly one <h1>")
        if len(H2_RE.findall(html)) < 4:
            problems.append(f"{rel}: needs at least four <h2> sections")
        headings = [TAG_RE.sub(" ", item).lower()
                    for item in re.findall(r"<h2\b[^>]*>(.*?)</h2>", html, re.I | re.S)]
        if not re.search(r"\b(?:mistake|mistakes|trap|traps|error|errors)\b", " ".join(headings)):
            problems.append(f"{rel}: needs a clearly headed mistakes/traps section")
        if not re.search(r"\b(?:practice|practise|drill)\b", " ".join(headings)):
            problems.append(f"{rel}: needs a clearly headed practice section")
        links = {q for q in ARABIC if q != post and f"../{q}/" in html}
        if len(links) < 2:
            problems.append(f"{rel}: links to only {len(links)} other Arabic guide(s)")
        if (f'href="{post}/"' not in arabic_hub
                and f'href="/learn/arabic/{post}/"' not in arabic_hub):
            problems.append(f"{rel}: the Arabic hub does not link to it")
        if 'data-learning-language="ar"' not in html:
            problems.append(f"{rel}: page must identify Arabic as its learning language")
        if "AI-assisted draft for owner review" not in html:
            problems.append(f"{rel}: must remain clearly labelled as an unreviewed AI-assisted draft")
        examples = ARABIC_BDI_RE.findall(html)
        if not examples or not any(ARABIC_SCRIPT_RE.search(example) for example in examples):
            problems.append(f"{rel}: needs Arabic-script examples marked lang=ar and dir=rtl")
        unmarked = ARABIC_BDI_RE.sub("", html)
        if ARABIC_SCRIPT_RE.search(unmarked):
            problems.append(f"{rel}: Arabic-script text outside a lang=ar, dir=rtl example")
        if "transliteration" not in html.lower():
            problems.append(f"{rel}: needs a clearly labelled transliteration learner aid")
        if not re.search(r"Modern Standard Arabic|\bMSA\b", html, re.I):
            problems.append(f"{rel}: needs to identify the Modern Standard Arabic focus")
        m = ROBOTS_RE.search(html)
        if not (m and "noindex" in m.group(1).lower()):
            problems.append(f"{rel}: a new Arabic page must stay noindex pending review")

    # German: standard-language articles use the original Latin spelling and
    # a deliberately qualified pronunciation aid instead of transliteration.
    german_hub_path = ROOT / "learn/german/index.html"
    german_hub = german_hub_path.read_text(encoding="utf-8") if german_hub_path.exists() else ""
    german_checked = 0
    if 'href="./german/"' not in learn_index:
        problems.append("learn/: German long-form guide hub is not linked from the Learn home")
    if not german_hub:
        problems.append("German: hub learn/german/index.html is missing")
    else:
        m = ROBOTS_RE.search(german_hub)
        if not (m and "noindex" in m.group(1).lower()):
            problems.append("learn/german/: new hub must stay noindex pending review")
        if 'href="/languages/de/course/"' not in german_hub:
            problems.append("learn/german/: hub must link to the German course")
        if not GERMAN_SPAN_RE.search(german_hub):
            problems.append("learn/german/: examples need lang=de")
        if "not IPA" not in german_hub and "not a phonetic transcription" not in german_hub:
            problems.append("learn/german/: pronunciation cues must be labelled as learner aids, not IPA")
        if not re.search(r"Standard German", german_hub, re.I):
            problems.append("learn/german/: hub must identify its Standard German focus")

    for post in GERMAN:
        rel = f"learn/german/{post}/index.html"
        p = ROOT / rel
        if not p.exists():
            problems.append(f"{rel}: missing (German Phase 3)")
            continue
        checked += 1
        german_checked += 1
        html = p.read_text(encoding="utf-8")
        w = words(html)
        if w < MIN_WORDS:
            problems.append(f"{rel}: {w} words, needs {MIN_WORDS} (German)")
        if w < shortest[1]:
            shortest = (rel, w)
        if len(MAIN_RE.findall(html)) != 1:
            problems.append(f"{rel}: needs exactly one <main>")
        if len(H1_RE.findall(html)) != 1:
            problems.append(f"{rel}: needs exactly one <h1>")
        if len(H2_RE.findall(html)) < 4:
            problems.append(f"{rel}: needs at least four <h2> sections")
        headings = [TAG_RE.sub(" ", item).lower()
                    for item in re.findall(r"<h2\b[^>]*>(.*?)</h2>", html, re.I | re.S)]
        if not re.search(r"\b(?:mistake|mistakes|trap|traps|error|errors)\b", " ".join(headings)):
            problems.append(f"{rel}: needs a clearly headed mistakes/traps section")
        if not re.search(r"\b(?:practice|practise|drill)\b", " ".join(headings)):
            problems.append(f"{rel}: needs a clearly headed practice section")
        links = {q for q in GERMAN if q != post and f"../{q}/" in html}
        if len(links) < 2:
            problems.append(f"{rel}: links to only {len(links)} other German guide(s)")
        if (f'href="{post}/"' not in german_hub
                and f'href="/learn/german/{post}/"' not in german_hub):
            problems.append(f"{rel}: the German hub does not link to it")
        if 'data-learning-language="de"' not in html:
            problems.append(f"{rel}: page must identify German as its learning language")
        examples = GERMAN_SPAN_RE.findall(html)
        if not examples or not any(GERMAN_TEXT_RE.search(example) for example in examples):
            problems.append(f"{rel}: needs German-language examples marked lang=de")
        if "learner aid" not in html.lower() or "not ipa" not in html.lower():
            problems.append(f"{rel}: pronunciation cues must be labelled as learner aids, not IPA")
        if not re.search(r"Standard German", html, re.I):
            problems.append(f"{rel}: needs to identify the Standard German focus")
        if "AI-assisted draft for owner review" not in html:
            problems.append(f"{rel}: must remain clearly labelled as an unreviewed AI-assisted draft")
        m = ROBOTS_RE.search(html)
        if not (m and "noindex" in m.group(1).lower()):
            problems.append(f"{rel}: a new German page must stay noindex pending review")

    langs = len(packs)
    print(f"PHASE 3 content: {langs} course pack(s) × {len(POSTS)} posts = {langs * len(POSTS)} pages "
          f"+ Hindi {hindi_checked}/{len(HINDI)} + Spanish {spanish_checked}/{len(SPANISH)} "
          f"+ Arabic {arabic_checked}/{len(ARABIC)} + German {german_checked}/{len(GERMAN)} mapped posts "
          f"= {checked} found")
    if checked:
        print(f"shortest post: {shortest[0]} — {shortest[1]} words (minimum {MIN_WORDS})")
    if problems:
        print(f"\nFAIL — {len(problems)} problem(s):")
        for line in problems[:25]:
            print("  " + line)
        if len(problems) > 25:
            print(f"  … and {len(problems) - 25} more")
        return 1
    print("\nPASS — every post exists, clears 1000 words, is a readable article, links to the others,")
    print("       is linked from its hub, and carries the indexability the owner's contract allows.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

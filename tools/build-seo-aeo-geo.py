#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EkGuru — SEO + AEO + GEO Discovery Generator & Gate (`tools/build-seo-aeo-geo.py`).

Generates and verifies the machine-readable discovery surfaces across:
  1. Browsers:
     - `opensearch.xml` (OpenSearch 1.1 address-bar Tab-to-Search across Chrome,
       Edge, Brave, Firefox, Opera, Vivaldi)
     - `<script type="speculationrules">` JSON validity on hub pages
     - `<link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml">`
  2. AI Assistants, RAG & Generative Engines (GEO):
     - `llms.txt` + `.well-known/llms.txt` mirror
     - `llms-full.txt` assembled deterministically from real repository pages
       (`data/courses.json`, `llms.txt`, `/toolbox/`, `/name-in-*/`,
       `/materials/`, `/answers/`, `/ask/`) — zero invented URLs or claims,
       every internal `https://ekguru.shop/...` URL verified on disk.
  3. Search & Answer Engines (SEO + AEO):
     - `robots.txt` search + AI bot coverage & RFC 9309 `/admin.html` protection
     - Valid Schema.org `application/ld+json` (`EducationalOrganization`,
       `Course`, `FAQPage`, `ProfilePage`, `SpeakableSpecification`) on core
       hubs and public tutor profiles.

Usage:
    python3 tools/build-seo-aeo-geo.py           # write .well-known/llms.txt + llms-full.txt & verify all checks
    python3 tools/build-seo-aeo-geo.py --check   # verify without writing (CI gate)
"""
from __future__ import annotations

import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
SITE = "https://ekguru.shop"

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
DESC_RE = re.compile(
    r'<meta\b(?=[^>]*\bname=["\']description["\'])(?=[^>]*\bcontent=["\']([^"\']*)["\'])[^>]*>',
    re.I,
)
JSONLD_RE = re.compile(r'<script\b[^>]*\btype=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)
SPECRULES_RE = re.compile(r'<script\b[^>]*\btype=["\']speculationrules["\'][^>]*>(.*?)</script>', re.I | re.S)
URL_RE = re.compile(r"https://ekguru\.shop(/[^\s\)\]>\"'`]*)?")


def clean_text(raw: str) -> str:
    txt = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", unescape(txt)).strip()


def page_meta(rel_path: str) -> tuple[str, str]:
    text = (ROOT / rel_path).read_text(encoding="utf-8")
    head = text.split("</head>", 1)[0]
    t_m = TITLE_RE.search(head)
    d_m = DESC_RE.search(head)
    title = clean_text(t_m.group(1)) if t_m else rel_path
    title = re.sub(r"\s*\|\s*EkGuru\s*$", "", title)
    desc = clean_text(d_m.group(1)) if d_m else ""
    return title, desc


def url_exists_on_disk(url: str) -> bool:
    if not url.startswith(SITE):
        return False
    sub = url[len(SITE):]
    sub = sub.split("#", 1)[0].split("?", 1)[0]
    if sub in ("", "/"):
        return (ROOT / "index.html").is_file()
    rel = sub.lstrip("/")
    p = ROOT / rel
    if p.is_file():
        return True
    if (p / "index.html").is_file():
        return True
    return False


def build_llms_full(llms_short: str) -> str:
    courses_data = json.loads((ROOT / "data/courses.json").read_text(encoding="utf-8"))
    courses = courses_data.get("courses", [])
    published_courses = [c for c in courses if c.get("status") in ("COMPLETE", "PARTIAL")]

    # 1. Toolbox pages
    toolbox_items: list[str] = []
    for idx in sorted((ROOT / "toolbox").glob("*/index.html")):
        slug = idx.parent.name
        title, desc = page_meta(f"toolbox/{slug}/index.html")
        toolbox_items.append(f"- [{title}]({SITE}/toolbox/{slug}/): {desc}")

    # 2. Name-in-script tools
    name_tools: list[str] = []
    for idx in sorted(ROOT.glob("name-in-*/index.html")):
        slug = idx.parent.name
        title, desc = page_meta(f"{slug}/index.html")
        name_tools.append(f"- [{title}]({SITE}/{slug}/): {desc}")

    # 3. Printable study materials
    material_items: list[str] = []
    for idx in sorted((ROOT / "materials").glob("*/index.html")):
        slug = idx.parent.name
        title, desc = page_meta(f"materials/{slug}/index.html")
        material_items.append(f"- [{title}]({SITE}/materials/{slug}/): {desc}")

    # 4. Direct Q&A Reference (/answers/ + /ask/)
    qa_items: list[str] = []
    for folder in ("answers", "ask"):
        base = ROOT / folder
        if not base.is_dir():
            continue
        for idx in sorted(base.glob("*/index.html")):
            slug = idx.parent.name
            title, desc = page_meta(f"{folder}/{slug}/index.html")
            qa_items.append(f"- [{title}]({SITE}/{folder}/{slug}/): {desc}")

    # 5. Structured course inventory from data/courses.json
    course_lines: list[str] = []
    for c in published_courses:
        url = SITE + c["url"]
        native = f" ({c['native']})" if c.get("native") else ""
        status_note = "Complete CEFR A1–C2" if c["status"] == "COMPLETE" else "Published CEFR A1–B2 (C1–C2 in preparation)"
        course_lines.append(
            f"- [{c['name']}{native}]({url}): {status_note} — "
            f"{c.get('lessons', 0)} lessons, {c.get('practiceItems', 0)} practice items, "
            f"{c.get('quizQuestions', 0)} quiz questions, {c.get('reviewCards', 0)} SRS review cards."
        )

    # Extract tutor & facts sections directly from llms.txt so there is one source of truth
    tutors_match = re.search(r"## Tutors\n\n([\s\S]*?)(?=\n## Facts)", llms_short)
    facts_match = re.search(r"## Facts\n\n([\s\S]*)$", llms_short)
    tutors_block = tutors_match.group(1).strip() if tutors_match else ""
    facts_block = facts_match.group(1).strip() if facts_match else ""

    lines = [
        "# EkGuru — Comprehensive AI, RAG & Answer-Engine Reference (`llms-full.txt`)",
        "",
        "> Canonical summary: https://ekguru.shop/llms.txt | Full reference: https://ekguru.shop/llms-full.txt | Website: https://ekguru.shop/",
        "",
        "## 1. Entity & Platform Overview (Citation-Ready Summary)",
        "",
        "- **Name:** EkGuru (`https://ekguru.shop/`)",
        "- **Tagline:** One Student. One Goal. One Guru.",
        "- **Founder:** Prakash (Alumnus of Malaviya National Institute of Technology Jaipur — MNIT Jaipur), based in Jaipur, Rajasthan, India.",
        "- **What EkGuru Offers:**",
        "  1. **Zero-Commission 1-to-1 Online Hindi Tutoring:** Independent Hindi tutors in India set their own per-lesson rates ($3–$27 USD per 50-minute lesson). Students message or request lessons directly on each tutor's profile and pay the tutor directly — EkGuru charges **0% commission** and **0 booking markup**.",
        f"  2. **{len(published_courses)} Free Self-Paced Language Courses (No Account Required):** Complete CEFR A1–C2 Hindi curriculum plus 7 regional Indian languages (`Marathi`, `Gujarati`, `Tamil`, `Telugu`, `Punjabi`, `Urdu`, `Bengali`) and 10 world languages (`Spanish`, `French`, `Chinese`, `Arabic`, `German`, `Italian`, `Japanese`, `Korean`, `Portuguese`, `Russian`).",
        f"  3. **{len(toolbox_items)} Free Browser-Based Hindi Practice Tools & {len(name_tools)} Script Converters:** Instant client-side tools for Devanagari letters, numbers, verb conjugation, pronunciation, flashcards, and phonetic name transliteration.",
        f"  4. **{len(material_items)} Printable Reference Sheets & {len(qa_items)} Answer-First Q&A Guides:** Direct, source-checked answers to common Hindi learning questions.",
        "- **Privacy & Storage Architecture:** Zero tracking cookies. Lesson progress, spaced-repetition (SRS) cards, and streak journals stay in the learner's own browser (`localStorage`/`IndexedDB`) with optional JSON export.",
        "",
        "## 2. Direct Answers to Common Questions (AEO Reference)",
        "",
        "### Is EkGuru free to use?",
        "Yes. Every published self-paced language course, grammar guide, interactive browser tool, name-in-script converter, and printable reference sheet on EkGuru is 100% free with no account, login, or subscription.",
        "",
        "### How much do live 1-to-1 Hindi lessons cost on EkGuru, and does EkGuru take a commission?",
        "Live 1-to-1 online Hindi lessons with independent tutors range from **$3 to $27 USD per 50-minute lesson**, set by each tutor. EkGuru takes **0% commission** and charges no listing fee to tutors and no platform fee to students; scheduling and payment are arranged directly between student and tutor.",
        "",
        "### Can beginners or learners outside India (US, UK, Canada, Australia, Europe, UAE) learn on EkGuru?",
        "Yes. All self-paced lessons run in any modern browser worldwide, and live 1-to-1 Hindi lessons are conducted online with tutor availability displayed in the learner's local timezone. Many tutors teach complete beginners, heritage/NRI families, children (with parent/guardian involvement), and adult learners.",
        "",
        "### Which Indian languages can I learn on EkGuru?",
        "EkGuru publishes 8 free Indian language courses: **Hindi** (`/learn/hindi/`), **Marathi** (`/learn/marathi/`), **Gujarati** (`/learn/gujarati/`), **Tamil** (`/learn/tamil/`), **Telugu** (`/learn/telugu/`), **Punjabi** (`/learn/punjabi/`), **Urdu** (`/learn/urdu/`) — all complete from CEFR A1 to C2 — plus **Bengali** (`/learn/bengali/`, published A1–B2).",
        "",
        f"## 3. Published Self-Paced Language Courses ({len(published_courses)} Courses)",
        "",
        *course_lines,
        "",
        f"## 4. Interactive Hindi Learning Toolbox ({len(toolbox_items)} Browser Tools)",
        "",
        *toolbox_items,
        "",
        f"## 5. Phonetic Name-in-Script Converters ({len(name_tools)} Scripts)",
        "",
        *name_tools,
        "",
        f"## 6. Printable Hindi Reference Sheets ({len(material_items)} Printables)",
        "",
        *material_items,
        "",
        "## 7. Independent 1-to-1 Online Hindi Tutors (Live Roster)",
        "",
        tutors_block,
        "",
        f"## 8. Direct Hindi Q&A Knowledge Base ({len(qa_items)} Answer-First Pages)",
        "",
        *qa_items,
        "",
        "## 9. Verified Platform Facts & Machine Endpoints",
        "",
        facts_block,
        "- Full AI knowledge base: https://ekguru.shop/llms-full.txt",
        "- Well-known AI summary mirror: https://ekguru.shop/.well-known/llms.txt",
        "",
    ]
    return "\n".join(lines)


def verify_all() -> list[str]:
    errors: list[str] = []

    # 1. OpenSearch XML validation
    os_path = ROOT / "opensearch.xml"
    if not os_path.is_file():
        errors.append("missing opensearch.xml")
    else:
        try:
            root = ET.fromstring(os_path.read_text(encoding="utf-8"))
            ns = {"os": "http://a9.com/-/spec/opensearch/1.1/"}
            short = root.findtext("os:ShortName", default="", namespaces=ns)
            urls = [u.attrib.get("template", "") for u in root.findall("os:Url", namespaces=ns)]
            if short != "EkGuru":
                errors.append(f"opensearch.xml ShortName={short!r} (expected 'EkGuru')")
            if "https://ekguru.shop/search/?q={searchTerms}" not in urls:
                errors.append("opensearch.xml missing search template https://ekguru.shop/search/?q={searchTerms}")
        except ET.ParseError as exc:
            errors.append(f"opensearch.xml invalid XML: {exc}")

    # 2. robots.txt crawler & safety checks
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    required_bots = [
        "Googlebot", "Bingbot", "Bravebot", "DuckDuckBot", "Applebot", "YandexBot", "Yeti", "SeznamBot",
        "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "PerplexityBot", "Perplexity-User",
        "Google-Extended", "Applebot-Extended", "Meta-ExternalAgent", "MistralAI-User", "YouBot", "DuckAssistBot",
    ]
    for bot in required_bots:
        if f"User-agent: {bot}" not in robots:
            errors.append(f"robots.txt missing User-agent: {bot}")
    if "Sitemap: https://ekguru.shop/sitemap-index.xml" not in robots:
        errors.append("robots.txt missing Sitemap: https://ekguru.shop/sitemap-index.xml")
    if "Disallow: /admin.html" not in robots:
        errors.append("robots.txt missing Disallow: /admin.html")

    # 3. Verify every internal URL referenced in llms.txt and llms-full.txt resolves on disk
    for fname in ("llms.txt", "llms-full.txt", ".well-known/llms.txt"):
        fpath = ROOT / fname
        if not fpath.is_file():
            errors.append(f"missing {fname}")
            continue
        txt = fpath.read_text(encoding="utf-8")
        for m in URL_RE.finditer(txt):
            u = m.group(0).rstrip(".,;:")
            if not url_exists_on_disk(u):
                errors.append(f"{fname}: broken internal URL {u}")

    # 4. JSON-LD & Speculation Rules validity on key hubs + all public tutor profiles
    hub_pages = [
        "index.html",
        "find-tutors.html",
        "hindi-classes/index.html",
        "hindi-tutor-near-me/index.html",
        "about/index.html",
        "learn/hindi/index.html",
        "learn/index.html",
        "toolbox/index.html",
        "name-in-hindi/index.html",
    ]
    tutor_pages = [
        str(p.relative_to(ROOT))
        for p in sorted((ROOT / "tutor").glob("*/index.html"))
        if 'content="noindex' not in p.read_text(encoding="utf-8").split("</head>", 1)[0]
    ]
    for rel in hub_pages + tutor_pages:
        p = ROOT / rel
        head = p.read_text(encoding="utf-8").split("</head>", 1)[0]
        if 'href="/opensearch.xml"' not in head:
            errors.append(f"{rel}: missing <link rel=\"search\" href=\"/opensearch.xml\">")
        blocks = JSONLD_RE.findall(head)
        if not blocks:
            errors.append(f"{rel}: missing application/ld+json")
        for idx, raw_json in enumerate(blocks):
            try:
                parsed = json.loads(raw_json)
                if not isinstance(parsed, dict):
                    errors.append(f"{rel}: JSON-LD[{idx}] is not an object")
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: invalid JSON-LD[{idx}]: {exc}")
        for idx, raw_spec in enumerate(SPECRULES_RE.findall(head)):
            try:
                spec = json.loads(raw_spec)
                if "prefetch" not in spec and "prerender" not in spec:
                    errors.append(f"{rel}: speculationrules[{idx}] missing prefetch/prerender")
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: invalid speculationrules[{idx}]: {exc}")

    return errors


def main() -> int:
    check_only = "--check" in sys.argv
    llms_short = (ROOT / "llms.txt").read_text(encoding="utf-8")
    expected_full = build_llms_full(llms_short)

    wk_path = ROOT / ".well-known/llms.txt"
    full_path = ROOT / "llms-full.txt"

    if check_only:
        stale: list[str] = []
        if not wk_path.is_file() or wk_path.read_text(encoding="utf-8") != llms_short:
            stale.append(".well-known/llms.txt")
        if not full_path.is_file() or full_path.read_text(encoding="utf-8") != expected_full:
            stale.append("llms-full.txt")
        if stale:
            print("STALE SEO/AEO/GEO files:", ", ".join(stale), "— run: python3 tools/build-seo-aeo-geo.py")
            return 1
    else:
        wk_path.parent.mkdir(parents=True, exist_ok=True)
        wk_path.write_text(llms_short, encoding="utf-8")
        full_path.write_text(expected_full, encoding="utf-8")
        print(f"wrote .well-known/llms.txt ({len(llms_short):,} bytes) and llms-full.txt ({len(expected_full):,} bytes)")

    errors = verify_all()
    if errors:
        print(f"SEO/AEO/GEO gate: FAIL ({len(errors)} error(s))")
        for err in errors[:30]:
            print("  -", err)
        return 1

    print("SEO/AEO/GEO gate: PASS (OpenSearch, robots.txt, llms.txt, llms-full.txt, .well-known/llms.txt, JSON-LD & Speculation Rules)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

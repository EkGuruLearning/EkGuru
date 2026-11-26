#!/usr/bin/env python3
"""Owner-approved consolidation of 196 empty country daily-phrase URLs.

GitHub Pages cannot serve repository-configured 301s. Existing URLs therefore
keep a crawlable index/follow canonical signal plus an immediate HTML redirect
and a visible, JavaScript-free fallback. They are not standalone search pages.
No location-specific phrase content or FAQ/QA claims are generated.

    python3 tools/build-country-phrases.py [--check]

Only the exact approved source list may change; parent country pages stay put.
"""
from __future__ import annotations

import json
import re
import sys
from html import escape
from pathlib import Path

from discovery_integrity import Page

ROOT = Path(__file__).resolve().parents[1]
TARGET = "https://ekguru.shop/learn/hindi/conversation/"
TARGET_PATH = "/learn/hindi/conversation/"
ULTRA = re.compile(r'<!-- ekguru:ultra-[a-z]+:start -->\n[\s\S]*?<!-- ekguru:ultra-[a-z]+:end -->\n')


def strip_ultra(text):
    text = ULTRA.sub("", text)
    return re.sub(r'(<html\b[^>]*?) data-learning-language="[^"]*"', r'\1', text, count=1, flags=re.I)


def approved_sources():
    baseline = json.loads((ROOT / "data/quality/indexing-baseline.json").read_text())
    approval = baseline["owner_approved_country_phrase_consolidation"]
    sources = approval["sources"]
    if approval["canonical"] != TARGET or len(sources) != 196 or len(set(sources)) != 196:
        raise ValueError("Consolidation must match the exact 196-page owner approval")
    if any(not re.fullmatch(r"learn-hindi-from-[a-z0-9-]+/daily-phrases/index\.html", path) for path in sources):
        raise ValueError("Approval contains an out-of-scope route")
    disk = {path.relative_to(ROOT).as_posix() for path in ROOT.glob("learn-hindi-from-*/daily-phrases/index.html")}
    if set(sources) != disk:
        raise ValueError("Approved sources do not match existing country phrase files")
    return sources


def consolidate(text, source):
    name = source.split("/", 1)[0][len("learn-hindi-from-"):].replace("-", " ").title()
    title = "Hindi Daily Phrases Have Moved | EkGuru"
    desc = "Use the shared Hindi conversation guide for greetings, polite expressions and everyday speaking practice."
    # Retired landing claims must not survive in rich-result or social metadata.
    text = re.sub(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>', "", text, flags=re.I | re.S)
    text = re.sub(r'<link\b[^>]*\bhreflang=["\'][^"\']+["\'][^>]*>\s*', "", text, flags=re.I)
    text = re.sub(r'<meta\b[^>]*http-equiv=["\']refresh["\'][^>]*>\s*', "", text, flags=re.I)
    text = re.sub(r'<title>.*?</title>', f"<title>{title}</title>", text, count=1, flags=re.S)
    def meta(match):
        tag = match.group(0)
        if re.search(r'\b(?:name|property)=["\'](?:description|og:description|twitter:description)["\']', tag, re.I):
            return re.sub(r'\bcontent=["\'][^"\']*["\']', f'content="{desc}"', tag)
        if re.search(r'\b(?:name|property)=["\'](?:og:title|twitter:title)["\']', tag, re.I):
            return re.sub(r'\bcontent=["\'][^"\']*["\']', f'content="{title}"', tag)
        if re.search(r'\bproperty=["\']og:url["\']', tag, re.I):
            return re.sub(r'\bcontent=["\'][^"\']*["\']', f'content="{TARGET}"', tag)
        return tag
    text = re.sub(r'<meta\b[^>]*>', meta, text, flags=re.I)
    text = re.sub(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>', f'<link href="{TARGET}" rel="canonical"/>', text, count=1, flags=re.I)
    # Deliberately do not mix cross-canonical consolidation with noindex.
    # Retired URLs stay crawlable so engines can process the move signal.
    redirect = f'<meta http-equiv="refresh" content="0;url={TARGET_PATH}">\n'
    text = text.replace("</head>", redirect + "</head>", 1)
    body = f'''<main id="main">
<div class="wrap sec" data-eg-country-phrase-merge>
<h1>Hindi daily phrases have moved</h1>
<p>Greetings and everyday expressions now live in the shared Hindi conversation guide, rather than separate country copies.</p>
<p><a class="btn btn-primary" href="{TARGET_PATH}">Open Hindi greetings and conversation</a></p>
<p>If automatic navigation is unavailable, use the link above. You can also return to <a href="../">the Hindi learning guide for {escape(name)}</a>.</p>
</div>
</main>'''
    text = re.sub(r'<main\b[^>]*>.*?</main>', lambda _: body, text, count=1, flags=re.I | re.S)
    return text


def main():
    check = "--check" in sys.argv
    target_file = ROOT / TARGET_PATH.strip("/") / "index.html"
    destination = target_file.read_text(encoding="utf-8")
    if Page(destination).canonicals != [TARGET] or re.search(r'<meta\b[^>]*(?:noindex|nofollow)', destination.split("</head>", 1)[0], re.I):
        raise ValueError("Merge destination must remain existing, self-canonical and indexable")
    changed = []
    for source in approved_sources():
        path = ROOT / source
        old = path.read_text(encoding="utf-8")
        new = consolidate(old, source)
        if strip_ultra(old) != strip_ultra(new):
            changed.append(source)
            if not check:
                path.write_text(new, encoding="utf-8")
    print(f"Country phrase consolidation: 196 approved routes; {len(changed)} {'stale' if check else 'updated'}; target {TARGET_PATH}")
    for source in changed[:5] if check else []:
        print("  " + source)
    return int(check and bool(changed))


if __name__ == "__main__":
    raise SystemExit(main())

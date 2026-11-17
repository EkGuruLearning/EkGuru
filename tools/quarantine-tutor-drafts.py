#!/usr/bin/env python3
"""Keep hidden/incomplete tutor profile pages out of public discovery.

Two sources of pages to quarantine:
  1. DRAFTS below — hand-written tutor files that are not in the registry
     (and not published by the sheet).
  2. 17 Nov 2026 — ORPHANS: any tutor/<id>/index.html whose id is no longer
     in the build roster at all. This happens when a sheet-only guru (baked
     from an approved=yes row, see tools/sheetsync.js) is later set
     active=no: the next bake drops the record, tools/build-tutor-pages.js
     no longer owns the page, and without this step the old profile would
     stay indexable with booking on. The page is rewritten as the same
     noindex "profile not published" stub (name taken from the old title),
     so a direct link still resolves and nothing private or bookable is
     left. Flipping the row back to active=yes rebuilds the real profile.

`--check` is a byte comparison and never writes.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = {
    "hemlata": ("Hemlata", "This tutor record is currently hidden from the public roster."),
    "tara": ("Tara", "This draft still contains placeholder profile fields."),
    "sarshtee-baliyan": ("Sarshtee Baliyan", "This draft still requires publication review and complete assets."),
}
DESC = "This tutor profile is not currently published. Browse EkGuru's current public tutor profiles."


def meta(text: str, key: str, value: str, content: str) -> str:
    pattern = re.compile(rf'<meta\b(?=[^>]*\b{key}=["\']{re.escape(value)}["\'])[^>]*>', re.I)
    tag = f'<meta {key}="{value}" content="{content}">'
    return pattern.sub(tag, text, count=1) if pattern.search(text) else text.replace("</head>", tag + "\n</head>", 1)


def desired(slug: str, name: str, reason: str, text: str) -> str:
    url = f"https://ekguru.shop/tutor/{slug}/"
    # Unique title/H1 per draft: three identical titles across these pages
    # was the one duplicate-title group left in the repository audit.
    title = f"{name} — tutor profile not published | EkGuru"
    h1 = f"{name} — tutor profile not published"
    desc = f"The {name} tutor profile is not currently published. Browse EkGuru's current public tutor profiles."
    main = f'''<main class="pr-wrap" id="main">
  <nav aria-label="Breadcrumb" class="crumbs"><a href="../../index.html">Home</a> › <a href="../../find-tutors.html">Find Tutors</a> › <span>Profile not published</span></nav>
  <article class="pr-sec"><h1>{h1}</h1><p>{reason}</p><p>No price, availability, identity status or booking terms are offered on this page.</p><p><a class="btn btn-primary" href="../../find-tutors.html">Browse current tutor profiles</a></p></article>
</main>'''
    text = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", text, count=1, flags=re.I | re.S)
    text = meta(text, "name", "description", desc)
    text = meta(text, "name", "robots", "noindex, follow")
    text = meta(text, "property", "og:title", title)
    text = meta(text, "property", "og:description", desc)
    text = meta(text, "name", "twitter:title", title)
    text = meta(text, "name", "twitter:description", desc)
    if re.search(r"<html\b[^>]*\bdata-ad-class=", text, re.I):
        text = re.sub(r'(<html\b[^>]*\bdata-ad-class=["\'])[^"\']*', r'\1RESEARCH_REQUIRED', text, count=1, flags=re.I)
    else:
        text = re.sub(r"<html\b", '<html data-ad-class="RESEARCH_REQUIRED"', text, count=1, flags=re.I)
    if re.search(r"<html\b[^>]*\bdata-publication-state=", text, re.I):
        text = re.sub(r'(<html\b[^>]*\bdata-publication-state=["\'])[^"\']*', r'\1research-required', text, count=1, flags=re.I)
    else:
        text = re.sub(r"<html\b", '<html data-publication-state="research-required"', text, count=1, flags=re.I)
    text = re.sub(r'\s*<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>\s*', "\n", text, flags=re.I | re.S)
    schema = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "name": title,
                         "url": url, "description": desc}, ensure_ascii=False, separators=(",", ":"))
    schema_tag = f'<script type="application/ld+json">{schema}</script>'
    text = re.sub(r'\s*</head>', "\n</head>", text, count=1, flags=re.I)
    # apply-ultra owns the marked asset block. Keep this page-level schema
    # before that block when decorated, so a later --strip/restore cycle stays
    # byte-stable instead of making the quarantine check look stale on every
    # full build.
    ultra_assets = "<!-- ekguru:ultra-assets:start -->"
    if ultra_assets in text:
        text = text.replace(ultra_assets, schema_tag + "\n" + ultra_assets, 1)
    else:
        text = text.replace("</head>", schema_tag + "\n</head>", 1)
    text = re.sub(r"<main\b.*?</main>", main, text, count=1, flags=re.I | re.S)
    return text


def roster_ids() -> tuple:
    """(public, roster, unlisted) as the build sees them. public = registry +
    approved sheet rows, minus active=no. 17 Nov 2026: the sheet is the
    source of truth, so a draft listed above is only quarantined while the
    sheet does NOT publish it; once the owner writes approved=yes /
    active=yes the real profile from tools/build-tutor-pages.js is left
    alone. roster = every id that still has data (registry files + baked
    sheet-only gurus); unlisted = tutor files outside the registry."""
    import subprocess
    try:
        out = subprocess.run(
            ["node", "-e", "const {loadSite}=require('./tools/lib/site-data');const s=loadSite();"
             "process.stdout.write(JSON.stringify({public:s.publicTutors.map(t=>t.id),"
             "roster:s.tutors.map(t=>t.id),unlisted:s.unlisted}))"],
            capture_output=True, text=True, cwd=ROOT, timeout=60)
        d = json.loads(out.stdout or "{}")
        return set(d.get("public", [])), set(d.get("roster", [])), set(d.get("unlisted", []))
    except Exception as exc:  # a broken roster must not silently quarantine anyone
        print(f"warn: could not read the public roster ({exc}); quarantining nothing")
        return set(DRAFTS), None, set()


def public_ids() -> set:
    return roster_ids()[0]


def page_name(text: str, slug: str) -> str:
    """The guru's display name from an existing page: the part of <title>
    before the first em dash ("Neelam Dawar — Online Hindi Tutor Profile |
    EkGuru" and the quarantined form both start with the name)."""
    m = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    raw = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    name = re.split(r"\s+[—|-]\s+", raw, maxsplit=1)[0].strip() if raw else ""
    return name or slug.replace("-", " ").title()


def orphans(roster, unlisted) -> dict:
    """tutor/<id>/ directories with a page but no data source anywhere."""
    if roster is None:
        return {}
    found = {}
    for d in sorted((ROOT / "tutor").iterdir()):
        page = d / "index.html"
        if not d.is_dir() or not page.is_file():
            continue
        slug = d.name
        if slug in roster or slug in unlisted or slug in DRAFTS:
            continue
        name = page_name(page.read_text(encoding="utf-8"), slug)
        found[slug] = (name, "This tutor profile is currently hidden from the public roster.")
    return found


def main() -> int:
    check = "--check" in sys.argv
    stale = []
    live, roster, unlisted = roster_ids()
    drafts = {k: v for k, v in DRAFTS.items() if k not in live}
    skipped = [k for k in DRAFTS if k in live]
    if skipped:
        print("published by the sheet, not quarantined: " + ", ".join(skipped))
    gone = orphans(roster, unlisted)
    if gone:
        print("no longer in the roster (sheet active=no / unapproved), quarantined: " + ", ".join(gone))
    drafts.update(gone)
    for slug, (name, reason) in drafts.items():
        path = ROOT / "tutor" / slug / "index.html"
        old = path.read_text(encoding="utf-8")
        new = desired(slug, name, reason, old)
        if new != old:
            stale.append(path.relative_to(ROOT).as_posix())
            if not check: path.write_text(new, encoding="utf-8")
    if check and stale:
        print("STALE draft tutor pages: " + ", ".join(stale)); return 1
    if check: print(f"PASS: {len(drafts)} draft tutor page(s)")
    else: print(f"quarantined: {len(drafts)} draft tutor page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

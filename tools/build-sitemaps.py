#!/usr/bin/env python3
"""Prune sitemap URLs against the files that can actually be indexed.

A sitemap URL is retained only when it is local, query-free, backed by an HTML
file, indexable, self-canonical and not disallowed for the generic crawler.
The command also writes a machine-readable gate report. Use --check in CI.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://ekguru.shop"
REPORT = ROOT / "data/quality/sitemap-audit.json"
EXCLUDED_FROM_INDEX = {"sitemap-index.xml", "sitemap-world-languages.xml", "sitemap-countries.xml", "sitemap-source-languages.xml"}
REQUIRED_CORE = [
    "/",
    "/about/",
    "/privacy/",
    "/terms/",
    "/cookie-policy/",
    "/monetization-disclosure/",
    "/contact/",
    "/support/",
]

URL_BLOCK_RE = re.compile(r"\s*<url>.*?</url>\s*", re.S | re.I)
LOC_RE = re.compile(r"<loc>(.*?)</loc>", re.S | re.I)
CANONICAL_RE = re.compile(r'<link\b(?=[^>]*\brel=["\']canonical["\'])(?=[^>]*\bhref=["\']([^"\']+)["\'])[^>]*>', re.I)
ROBOTS_RE = re.compile(r'<meta\b(?=[^>]*\bname=["\']robots["\'])(?=[^>]*\bcontent=["\']([^"\']*)["\'])[^>]*>', re.I)


def normalized_url(value: str) -> str | None:
    parsed = urlsplit(html.unescape(value.strip()))
    if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() != "ekguru.shop":
        return None
    if parsed.query or parsed.fragment:
        return None
    path = unquote(parsed.path or "/")
    path = re.sub(r"/{2,}", "/", path)
    if path.endswith("/index.html"):
        path = path[:-10] or "/"
    return BASE + path


def url_to_file(value: str) -> Path | None:
    norm = normalized_url(value)
    if not norm:
        return None
    path = urlsplit(norm).path.lstrip("/")
    if not path:
        return ROOT / "index.html"
    candidate = ROOT / path
    if urlsplit(norm).path.endswith("/") or candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate


def generic_disallows() -> list[str]:
    lines = (ROOT / "robots.txt").read_text(encoding="utf-8").splitlines()
    active = False
    rules: list[str] = []
    for raw in lines:
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.lower().startswith("user-agent:"):
            agent = line.split(":", 1)[1].strip()
            if active and agent != "*":
                break
            active = agent == "*"
        elif active and line.lower().startswith("disallow:"):
            value = line.split(":", 1)[1].strip()
            if value:
                rules.append(value)
    return rules


def inspect_url(value: str, disallows: list[str]) -> tuple[bool, str]:
    norm = normalized_url(value)
    if not norm:
        return False, "external-query-or-fragment"
    parsed = urlsplit(norm)
    if any(parsed.path.startswith(rule) for rule in disallows):
        return False, "robots-disallow"
    file = url_to_file(value)
    if not file or not file.is_file():
        return False, "missing-file"
    try:
        text = file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False, "non-html-file"
    head = text.split("</head>", 1)[0]
    robots = ROBOTS_RE.search(head)
    if robots and "noindex" in robots.group(1).lower():
        return False, "noindex"
    canonical = CANONICAL_RE.search(head)
    if not canonical:
        return False, "missing-canonical"
    if normalized_url(canonical.group(1)) != norm:
        return False, "non-self-canonical"
    return True, "ok"


def ensure_core_urls() -> None:
    path = ROOT / "sitemap-core.xml"
    text = path.read_text(encoding="utf-8")
    existing = {html.unescape(loc.strip()) for loc in LOC_RE.findall(text)}
    additions = []
    for relative in REQUIRED_CORE:
        loc = BASE + relative
        if loc not in existing:
            additions.append(
                "  <url>\n"
                f"    <loc>{loc}</loc>\n"
                f"    <lastmod>{date.today().isoformat()}</lastmod>\n"
                "  </url>\n"
            )
    if additions:
        text = text.replace("</urlset>", "".join(additions) + "</urlset>")
        path.write_text(text, encoding="utf-8")


def prune_file(path: Path, disallows: list[str], write: bool) -> tuple[int, Counter, list[dict]]:
    text = path.read_text(encoding="utf-8")
    removed: Counter = Counter()
    details: list[dict] = []

    def decide(match: re.Match[str]) -> str:
        block = match.group(0)
        found = LOC_RE.search(block)
        if not found:
            removed["missing-loc"] += 1
            return "" if write else block
        loc = html.unescape(found.group(1).strip())
        ok, reason = inspect_url(loc, disallows)
        if not ok:
            removed[reason] += 1
            details.append({"url": loc, "reason": reason})
            return "" if write else block
        return block

    blocks = URL_BLOCK_RE.findall(text)
    if write:
        text = URL_BLOCK_RE.sub(decide, text)
        # Keep the XML readable after block removal.
        text = re.sub(r"\n{3,}", "\n", text)
        path.write_text(text, encoding="utf-8")
    else:
        for block in blocks:
            decide(re.match(r".*", block, re.S))
    return len(blocks) - sum(removed.values()), removed, details


def rebuild_index(sitemaps: list[Path]) -> None:
    today = date.today().isoformat()
    body = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in sitemaps:
        if path.name in EXCLUDED_FROM_INDEX:
            continue
        count = len(LOC_RE.findall(path.read_text(encoding="utf-8")))
        if not count:
            continue
        body.extend([
            "  <sitemap>",
            f"    <loc>{BASE}/{path.name}</loc>",
            f"    <lastmod>{today}</lastmod>",
            "  </sitemap>",
        ])
    body.append("</sitemapindex>")
    (ROOT / "sitemap-index.xml").write_text("\n".join(body) + "\n", encoding="utf-8")


def audit_all() -> dict:
    disallows = generic_disallows()
    maps = sorted(path for path in ROOT.glob("sitemap*.xml") if path.name != "sitemap-index.xml")
    failures: list[dict] = []
    by_map: dict[str, dict] = {}
    all_locs: list[str] = []
    for path in maps:
        text = path.read_text(encoding="utf-8")
        locs = [html.unescape(value.strip()) for value in LOC_RE.findall(text)]
        all_locs.extend(locs)
        reasons = Counter()
        for loc in locs:
            ok, reason = inspect_url(loc, disallows)
            if not ok:
                reasons[reason] += 1
                failures.append({"sitemap": path.name, "url": loc, "reason": reason})
        by_map[path.name] = {"urls": len(locs), "failures": dict(sorted(reasons.items()))}
    index_text = (ROOT / "sitemap-index.xml").read_text(encoding="utf-8")
    index_maps = [Path(urlsplit(html.unescape(v)).path).name for v in LOC_RE.findall(index_text)]
    index_failures = [name for name in index_maps if not (ROOT / name).is_file() or not LOC_RE.findall((ROOT / name).read_text(encoding="utf-8"))]
    return {
        "generated": date.today().isoformat(),
        "status": "PASS" if not failures and not index_failures else "FAIL",
        "sitemaps": by_map,
        "indexed_sitemaps": index_maps,
        "invalid_index_entries": index_failures,
        "failures": failures,
        "duplicate_url_memberships": sum(count - 1 for count in Counter(all_locs).values() if count > 1),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="read-only validation; exit non-zero on a gate failure")
    args = parser.parse_args()
    disallows = generic_disallows()
    if not args.check:
        ensure_core_urls()
        maps = sorted(path for path in ROOT.glob("sitemap*.xml") if path.name != "sitemap-index.xml")
        totals = Counter()
        for path in maps:
            _, removed, _ = prune_file(path, disallows, write=True)
            totals.update(removed)
        rebuild_index(maps)
        print("removed:", json.dumps(dict(sorted(totals.items())), sort_keys=True))
    result = audit_all()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    total = sum(item["urls"] for item in result["sitemaps"].values())
    print(f"sitemap gate: {result['status']} ({total} URL memberships, {len(result['failures'])} invalid)")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

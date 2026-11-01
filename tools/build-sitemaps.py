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
EXCLUDED_FROM_INDEX = {"sitemap-index.xml", "sitemap.xml", "sitemap-world-languages.xml", "sitemap-countries.xml", "sitemap-source-languages.xml"}
SUPPLEMENT = "sitemap-published.xml"
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


def file_to_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return BASE + "/"
    if rel.endswith("/index.html"):
        return BASE + "/" + rel[:-10]
    return BASE + "/" + rel


def eligible_public_urls(disallows: list[str]) -> set[str]:
    """Every crawlable, self-canonical public HTML URL must be discoverable."""
    pages = sorted(
        path for path in ROOT.rglob("*.html")
        if not any(part in {".git", "node_modules", ".venv", "reports"} for part in path.parts)
    )
    out = set()
    for page in pages:
        url = file_to_url(page)
        ok, _ = inspect_url(url, disallows)
        if ok:
            out.add(url)
    return out


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


def dedupe_indexed_maps(sitemaps: list[Path]) -> int:
    """Keep each URL in one focused child sitemap (the complete map is separate)."""
    seen: set[str] = set()
    removed = 0
    for path in sorted(sitemaps):
        if path.name in EXCLUDED_FROM_INDEX or path.name == SUPPLEMENT:
            continue
        text = path.read_text(encoding="utf-8")

        def once(match: re.Match[str]) -> str:
            nonlocal removed
            found = LOC_RE.search(match.group(0))
            normalized = normalized_url(found.group(1)) if found else None
            if normalized and normalized in seen:
                removed += 1
                return ""
            if normalized:
                seen.add(normalized)
            return match.group(0)

        new = URL_BLOCK_RE.sub(once, text)
        if new != text:
            path.write_text(re.sub(r"\n{3,}", "\n", new), encoding="utf-8")
    return removed


def rebuild_supplement(disallows: list[str]) -> None:
    """Add indexable pages omitted by legacy category sitemap generators."""
    represented: set[str] = set()
    for path in sorted(ROOT.glob("sitemap*.xml")):
        if path.name in EXCLUDED_FROM_INDEX or path.name == SUPPLEMENT:
            continue
        represented.update(
            normalized for value in LOC_RE.findall(path.read_text(encoding="utf-8"))
            if (normalized := normalized_url(value))
        )
    missing = sorted(eligible_public_urls(disallows) - represented)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    today = date.today().isoformat()
    for loc in missing:
        lines.extend([
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{today}</lastmod>",
            "  </url>",
        ])
    lines.append("</urlset>")
    (ROOT / SUPPLEMENT).write_text("\n".join(lines) + "\n", encoding="utf-8")


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
    indexed_locs: list[str] = []
    for name in index_maps:
        path = ROOT / name
        if path.is_file():
            indexed_locs.extend(
                normalized for value in LOC_RE.findall(path.read_text(encoding="utf-8"))
                if (normalized := normalized_url(value))
            )
    indexed_counts = Counter(indexed_locs)
    duplicate_memberships = sum(count - 1 for count in indexed_counts.values() if count > 1)
    failures.extend(
        {"sitemap": "sitemap-index.xml", "url": url, "reason": "duplicate-indexed-membership"}
        for url, count in indexed_counts.items() if count > 1
    )
    eligible = eligible_public_urls(disallows)
    missing = sorted(eligible - set(indexed_locs))
    failures.extend({"sitemap": "sitemap-index.xml", "url": url, "reason": "indexable-url-omitted"} for url in missing)
    other_locs: set[str] = set()
    for name in index_maps:
        if name == SUPPLEMENT or not (ROOT / name).is_file():
            continue
        other_locs.update(
            normalized for value in LOC_RE.findall((ROOT / name).read_text(encoding="utf-8"))
            if (normalized := normalized_url(value))
        )
    expected_supplement = eligible - other_locs
    supplement_path = ROOT / SUPPLEMENT
    actual_supplement = {
        normalized for value in LOC_RE.findall(supplement_path.read_text(encoding="utf-8"))
        if (normalized := normalized_url(value))
    } if supplement_path.is_file() else set()
    supplement_drift = sorted(expected_supplement ^ actual_supplement)
    failures.extend({"sitemap": SUPPLEMENT, "url": url, "reason": "supplement-drift"} for url in supplement_drift)
    return {
        "generated": date.today().isoformat(),
        "status": "PASS" if not failures and not index_failures else "FAIL",
        "sitemaps": by_map,
        "indexed_sitemaps": index_maps,
        "invalid_index_entries": index_failures,
        "indexable_public_urls": len(eligible),
        "indexed_url_memberships": len(indexed_locs),
        "indexed_unique_urls": len(set(indexed_locs)),
        "missing_indexable_urls": len(missing),
        "supplement_urls": len(actual_supplement),
        "supplement_drift": len(supplement_drift),
        "failures": failures,
        "duplicate_url_memberships": duplicate_memberships,
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
        duplicate_removals = dedupe_indexed_maps(maps)
        if duplicate_removals:
            totals["duplicate-membership"] += duplicate_removals
        rebuild_supplement(disallows)
        maps = sorted(path for path in ROOT.glob("sitemap*.xml") if path.name != "sitemap-index.xml")
        rebuild_index(maps)
        print("removed:", json.dumps(dict(sorted(totals.items())), sort_keys=True))
    result = audit_all()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    total = result["indexed_url_memberships"]
    print(f"sitemap gate: {result['status']} ({total} indexed URL memberships, {len(result['failures'])} invalid)")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

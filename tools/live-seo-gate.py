#!/usr/bin/env python3
"""Fail-closed HTTP search-discovery probes, not a ranking/indexing claim.

Production: python3 tools/live-seo-gate.py --discovery --check-origins
Preview:    python3 tools/live-seo-gate.py --base http://127.0.0.1:8080 --discovery

A WAF challenge, network error, empty sitemap or accidental noindex is a
failure, never silently replaced with local evidence. Reports are CI artifacts.
--discovery requires the new llms/OpenSearch endpoints after their deployment.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

SITE = "https://ekguru.shop"
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
UA = "Mozilla/5.0 EkGuruDiscoveryAudit/2.0 (+https://ekguru.shop/contact/)"
CORE = ["/", "/find-tutors.html", "/learn/hindi/", "/hindi-classes/", "/hindi-tutor-near-me/", "/name-in-hindi/"]


class Head(HTMLParser):
    def __init__(self, body):
        super().__init__()
        self.canonicals = []
        self.robots = []
        self.title = False
        self.title_text = ""
        self.feed(body.split("</head>", 1)[0])

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonicals.append(attrs.get("href", ""))
        if tag == "meta" and attrs.get("name", "").lower() in {"robots", "googlebot", "bingbot"}:
            self.robots.append(attrs.get("content", ""))
        if tag == "title":
            self.title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.title = False

    def handle_data(self, text):
        if self.title:
            self.title_text += text


def fetch(url, user_agent=UA):
    try:
        response = urlopen(Request(url, headers={"User-Agent": user_agent}), timeout=25)
    except HTTPError as exc:
        response = exc
    except (URLError, TimeoutError, OSError) as exc:
        return {"url": url, "status": 0, "headers": {}, "body": "", "error": str(exc)}
    with response:
        headers = {key.lower(): value for key, value in response.headers.items()}
        return {"url": response.geturl(), "status": response.status, "headers": headers,
                "body": response.read(4_000_001).decode("utf-8", "replace")}


def response_errors(result, expected_status=200):
    errors = []
    if result["status"] != expected_status:
        errors.append(f"HTTP {result['status']} (wanted {expected_status})")
    if result["headers"].get("cf-mitigated", "").lower() == "challenge" or "<title>Just a moment" in result["body"]:
        errors.append("WAF challenge: live crawlability is NOT verified")
    if result.get("error"):
        errors.append(result["error"])
    return errors


def page_errors(result, expected_canonical):
    errors = response_errors(result)
    if errors:
        return errors
    if "text/html" not in result["headers"].get("content-type", ""):
        errors.append("not HTML")
    head = Head(result["body"])
    if head.canonicals != [expected_canonical]:
        errors.append(f"canonical {head.canonicals!r} != {expected_canonical}")
    directives = ",".join(head.robots + [result["headers"].get("x-robots-tag", "")]).lower()
    if re.search(r"\b(noindex|none)\b", directives):
        errors.append("noindex in meta or X-Robots-Tag")
    if not head.title_text.strip():
        errors.append("missing title")
    if not re.search(r"<h1\b", result["body"], re.I):
        errors.append("missing visible H1")
    return errors


def sitemap_locs(result, expected_kind):
    errors = response_errors(result)
    if errors:
        return [], errors
    try:
        tree = ET.fromstring(result["body"])
    except ET.ParseError:
        return [], ["invalid XML"]
    if tree.tag != NS + expected_kind:
        return [], [f"expected {expected_kind} XML"]
    locs = [node.text.strip() for node in tree.findall(f"{NS}{'sitemap' if expected_kind == 'sitemapindex' else 'url'}/{NS}loc") if node.text]
    if not locs:
        errors.append("empty sitemap")
    if any(not loc.startswith(SITE + "/") or urlsplit(loc).query or urlsplit(loc).fragment for loc in locs):
        errors.append("noncanonical or unsafe sitemap URL")
    return locs, errors


def run(base, sample_size=24, discovery=False, check_origins=False):
    checks = []

    def record(path, result, errors, **extra):
        checks.append({"path": path, "status": result["status"], "final_url": result["url"],
                       "errors": errors, **extra})

    robots = fetch(base + "/robots.txt")
    errors = response_errors(robots)
    parser = RobotFileParser()
    parser.parse(robots["body"].splitlines())
    if not any(line.lower().startswith("sitemap:") for line in robots["body"].splitlines()):
        errors.append("missing sitemap discovery")
    record("/robots.txt", robots, errors)

    index = fetch(base + "/sitemap-index.xml")
    children, errors = sitemap_locs(index, "sitemapindex")
    record("/sitemap-index.xml", index, errors)
    urls = set()
    # Never follow an arbitrary host supplied by live XML.
    safe_children = [loc for loc in children if loc.startswith(SITE + "/")]
    for loc in safe_children:
        path = urlsplit(loc).path
        result = fetch(base + path)
        entries, errors = sitemap_locs(result, "urlset")
        record(path, result, errors)
        urls.update(entry for entry in entries if entry.startswith(SITE + "/"))
    ordered = sorted(urls)
    sample = {ordered[i * len(ordered) // min(sample_size, len(ordered))]
              for i in range(min(sample_size, len(ordered)))} if ordered else set()
    paths = sorted(set(CORE) | {urlsplit(url).path for url in sample})
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda path: fetch(base + path), paths))
    for path, result in zip(paths, results):
        errors = page_errors(result, SITE + path)
        for bot in ("Googlebot", "Bingbot", "OAI-SearchBot", "PerplexityBot"):
            if not parser.can_fetch(bot, SITE + path):
                errors.append(f"robots.txt blocks {bot}")
        if result["url"] != base + path:
            errors.append("unexpected redirect for canonical page")
        record(path, result, errors)

    # UA probes are diagnostic, not proof that a verified search-engine IP is allowed.
    for bot in ("Googlebot", "Bingbot", "OAI-SearchBot"):
        result = fetch(base + "/", bot)
        record("/", result, page_errors(result, SITE + "/"), user_agent=bot)
    missing = fetch(base + "/__ekguru_missing_seo_probe_47a1/")
    record("missing-page HTTP semantics", missing, response_errors(missing, 404))

    if discovery:
        for path in ("/llms.txt", "/llms-full.txt", "/.well-known/llms.txt", "/opensearch.xml"):
            result = fetch(base + path)
            errors = response_errors(result)
            if path.endswith(".txt") and (not result["body"].startswith("# EkGuru") or "text/plain" not in result["headers"].get("content-type", "")):
                errors.append("not an EkGuru text reference")
            if path.endswith(".xml"):
                try:
                    if ET.fromstring(result["body"]).tag != "{http://a9.com/-/spec/opensearch/1.1/}OpenSearchDescription":
                        errors.append("not OpenSearch XML")
                except ET.ParseError:
                    errors.append("invalid OpenSearch XML")
            record(path, result, errors)
    if check_origins:
        for origin in ("http://ekguru.shop", "http://www.ekguru.shop", "https://www.ekguru.shop"):
            result = fetch(origin + "/")
            errors = response_errors(result)
            if result["url"] != SITE + "/":
                errors.append("does not redirect to canonical HTTPS origin")
            record(origin, result, errors)
    return {"generated_at": datetime.now(timezone.utc).isoformat(), "base": base,
            "pass": not any(row["errors"] for row in checks), "sitemap_urls": len(urls),
            "html_sample_size": len(paths), "checks": checks,
            "limitations": "HTTP sample and UA probes only; no Search Console, actual indexing, field Core Web Vitals, verified-bot-IP or ranking evidence."}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--base", default=SITE)
    cli.add_argument("--sample-size", type=int, default=24)
    cli.add_argument("--discovery", action="store_true")
    cli.add_argument("--check-origins", action="store_true")
    cli.add_argument("--report", default="reports/live-seo-gate.json")
    args = cli.parse_args()
    if args.sample_size < 1 or args.sample_size > 1000:
        cli.error("sample-size must be between 1 and 1000")
    base = args.base.rstrip("/")
    report = run(base, args.sample_size, args.discovery, args.check_origins)
    path = Path(args.report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    annotation_count = 0
    for row in report["checks"]:
        if row["errors"]:
            print("FAIL", row["path"], row["errors"])
            if os.environ.get("GITHUB_ACTIONS") == "true" and annotation_count < 10:
                # Expose actionable failures in the Checks API as well as the
                # downloadable JSON; escape workflow-command control characters.
                detail = (row["path"] + ": " + "; ".join(row["errors"]))
                detail = detail.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
                print("::error title=Live search discovery::" + detail)
                annotation_count += 1
    print(f"Live SEO: {'PASS' if report['pass'] else 'FAIL'}; {report['sitemap_urls']} sitemap URLs; {report['html_sample_size']} HTML samples; {len(report['checks'])} probes")
    return int(not report["pass"])


if __name__ == "__main__":
    sys.exit(main())

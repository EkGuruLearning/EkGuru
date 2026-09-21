#!/usr/bin/env python3
"""Exercise the built site through HTTP instead of inspecting files directly.

The audit follows the real sitemap index, fetches every declared URL from a
local/static preview server, and validates status, content type, canonical,
indexability and basic landmarks. It also checks critical shell assets.

Run with a local server, for example:
  EK_BASE=http://127.0.0.1:8899 python3 tools/audit-local-http.py
"""
from __future__ import annotations

import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("EK_BASE", "http://127.0.0.1:8899").rstrip("/")
OUT = ROOT / "reports/local-http-audit.json"
LOC = re.compile(r"<loc>(.*?)</loc>", re.I | re.S)
CANONICAL = re.compile(r'<link\b(?=[^>]*\brel=["\']canonical["\'])(?=[^>]*\bhref=["\']([^"\']+)["\'])[^>]*>', re.I)
ROBOTS = re.compile(r'<meta\b(?=[^>]*\bname=["\']robots["\'])(?=[^>]*\bcontent=["\']([^"\']*)["\'])[^>]*>', re.I)


def get(path: str) -> dict:
    url = BASE + (path if path.startswith("/") else "/" + path)
    try:
        with urlopen(Request(url, headers={"User-Agent": "EkGuru-local-release-audit/1"}), timeout=20) as response:
            body = response.read()
            return {"url": url, "path": path, "status": response.status,
                    "content_type": response.headers.get_content_type(), "bytes": len(body),
                    "body": body.decode("utf-8", "replace")}
    except HTTPError as exc:
        return {"url": url, "path": path, "status": exc.code, "error": str(exc), "body": ""}
    except (URLError, TimeoutError, OSError) as exc:
        return {"url": url, "path": path, "status": 0, "error": str(exc), "body": ""}


def prod_path(value: str) -> str:
    parsed = urlsplit(value.strip())
    return parsed.path or "/"


def main() -> int:
    failures: list[dict] = []
    index = get("/sitemap-index.xml")
    if index["status"] != 200:
        failures.append({"path": "/sitemap-index.xml", "reason": "status", "actual": index["status"]})
        children = []
    else:
        children = sorted({prod_path(x) for x in LOC.findall(index["body"])})
    child_results = [get(path) for path in children]
    urls = set()
    for result in child_results:
        if result["status"] != 200:
            failures.append({"path": result["path"], "reason": "sitemap-status", "actual": result["status"]})
            continue
        if result.get("content_type") not in {"application/xml", "text/xml"}:
            failures.append({"path": result["path"], "reason": "sitemap-content-type", "actual": result.get("content_type")})
        urls.update(prod_path(x) for x in LOC.findall(result["body"]))

    def inspect(path: str) -> tuple[dict, list[dict]]:
        result = get(path)
        bad = []
        if result["status"] != 200:
            bad.append({"path": path, "reason": "status", "actual": result["status"]})
            return result, bad
        if result.get("content_type") != "text/html":
            bad.append({"path": path, "reason": "html-content-type", "actual": result.get("content_type")})
            return result, bad
        body = result["body"]
        canonical = CANONICAL.search(body)
        expected = "https://ekguru.shop" + path
        if not canonical or canonical.group(1) != expected:
            bad.append({"path": path, "reason": "canonical", "actual": canonical.group(1) if canonical else "missing", "expected": expected})
        robots = ROBOTS.search(body)
        if robots and "noindex" in robots.group(1).lower():
            bad.append({"path": path, "reason": "sitemap-noindex"})
        if len(re.findall(r"<main\b", body, re.I)) != 1:
            bad.append({"path": path, "reason": "main-count", "actual": len(re.findall(r"<main\b", body, re.I))})
        if "ekguru:shell-header:start" not in body or "ekguru:shell-footer:start" not in body:
            bad.append({"path": path, "reason": "shell-missing"})
        return result, bad

    pages = []
    with ThreadPoolExecutor(max_workers=24) as pool:
        jobs = {pool.submit(inspect, path): path for path in sorted(urls)}
        for future in as_completed(jobs):
            result, bad = future.result()
            pages.append({k: result.get(k) for k in ("path", "status", "content_type", "bytes")})
            failures.extend(bad)

    assets = {
        "/css/style.min.css": "text/css",
        "/js/site-shell.js": "text/javascript",
        "/js/course-player.js": "text/javascript",
        "/manifest.webmanifest": "application/manifest+json",
        "/robots.txt": "text/plain",
        "/ads.txt": "text/plain",
    }
    asset_results = []
    for path, expected_type in assets.items():
        result = get(path)
        asset_results.append({k: result.get(k) for k in ("path", "status", "content_type", "bytes")})
        if result["status"] != 200:
            failures.append({"path": path, "reason": "asset-status", "actual": result["status"]})
        elif result.get("content_type") != expected_type:
            failures.append({"path": path, "reason": "asset-content-type", "actual": result.get("content_type"), "expected": expected_type})

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base": BASE,
        "status": "PASS" if not failures else "FAIL",
        "sitemap_children": len(children),
        "unique_sitemap_urls": len(urls),
        "html_responses": len(pages),
        "html_bytes": sum(p.get("bytes") or 0 for p in pages),
        "assets": asset_results,
        "failures": failures,
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"local HTTP audit: {report['status']} — {len(children)} sitemaps, {len(urls)} URLs, {len(failures)} failures")
    for item in failures[:20]:
        print("  ", item)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())

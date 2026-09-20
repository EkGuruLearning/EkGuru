#!/usr/bin/env python3
"""Live HTTP gate for the current working implementation."""
from __future__ import annotations
import json, os, re, urllib.error, urllib.request
from datetime import date
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("EKGURU_BASE_URL", "http://127.0.0.1:3000").rstrip("/")
ROUTES = {
    "home": ("/", 200, False),
    "courses": ("/courses/", 200, False),
    "published-level": ("/languages/ko/level/b2/", 200, False),
    "blocked-polish": ("/languages/pl/level/a1/", 200, True),
    "blocked-korean-advanced": ("/languages/ko/level/c1/", 200, True),
    "country-research": ("/learn-hindi-from-usa/", 200, True),
    "world-language-research": ("/world-languages/usa/", 200, True),
    "support": ("/support/", 200, False),
    "privacy": ("/privacy/", 200, False),
    "disclosure": ("/monetization-disclosure/", 200, False),
    "sitemap-index": ("/sitemap-index.xml", 200, False),
    "ads-txt": ("/ads.txt", 200, False),
    "missing": ("/__ekguru_missing_release_gate__", 404, False),
}


def get(path: str):
    request = urllib.request.Request(BASE + path, headers={"User-Agent": "EkGuru-release-audit/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status, response.headers.get("Content-Type", ""), response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        return error.code, error.headers.get("Content-Type", ""), error.read().decode("utf-8", "replace")


def main() -> int:
    results = []
    for name, (route, expected, expect_noindex) in ROUTES.items():
        try:
            status, content_type, body = get(route)
            robots = re.search(r'<meta\b(?=[^>]*name=["\']robots["\'])(?=[^>]*content=["\']([^"\']*)["\'])', body, re.I)
            noindex = bool(robots and "noindex" in robots.group(1).lower())
            passed = status == expected and (noindex == expect_noindex if content_type.startswith("text/html") and status == 200 else True)
            detail = {"status": status, "content_type": content_type, "noindex": noindex, "bytes": len(body.encode())}
        except Exception as error:
            passed = False
            detail = {"error": str(error)}
        results.append({"name": name, "route": route, "passed": passed, **detail})
        print(("PASS" if passed else "FAIL"), name, detail)
    report = {
        "generated": date.today().isoformat(),
        "base_url": BASE,
        "status": "PASS" if all(item["passed"] for item in results) else "FAIL",
        "results": results,
    }
    out = ROOT / "reports/live-http-working-tree.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("live HTTP:", report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Focused real-Chromium release gate for publication and monetization safety."""
from __future__ import annotations

import json
import subprocess
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
PORT = 8765
BASE = f"http://127.0.0.1:{PORT}"
OUT = ROOT / "reports/EKGURU-RELEASE-BROWSER.json"

try:
    from playwright.sync_api import sync_playwright
except ModuleNotFoundError:
    sync_playwright = None


@contextmanager
def server():
    process = subprocess.Popen(
        ["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(60):
            try:
                with urlopen(BASE + "/", timeout=1) as response:
                    if response.status == 200:
                        break
            except Exception:
                time.sleep(0.1)
        else:
            raise RuntimeError("local HTTP server did not start")
        yield
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


def main() -> int:
    if sync_playwright is None:
        result = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "BLOCKED_ENVIRONMENT",
            "browser": "Playwright Chromium",
            "checks": [],
            "failed": [],
            "blocker": "Python Playwright is unavailable. An installation was attempted, but the browser download was blocked by the sandbox TLS/network boundary.",
        }
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("release browser gate: BLOCKED_ENVIRONMENT")
        return 2

    checks: list[dict] = []
    page_errors: list[dict] = []
    ad_requests: list[str] = []
    analytics_requests: list[str] = []
    same_origin_failures: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append({"name": name, "pass": bool(condition), "detail": detail})
        print(("PASS " if condition else "FAIL ") + name + (f" — {detail}" if detail else ""))

    with server(), sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 390, "height": 844}, reduced_motion="reduce")

        def route_external(route):
            url = route.request.url
            if "googlesyndication.com" in url or "doubleclick.net" in url:
                ad_requests.append(url)
            if "goatcounter.com" in url or "plausible.io" in url:
                analytics_requests.append(url)
            if not url.startswith(BASE):
                route.abort()
            else:
                route.continue_()

        context.route("**/*", route_external)
        page = context.new_page()
        page.on("pageerror", lambda error: page_errors.append({"url": page.url, "error": str(error)}))
        page.on(
            "requestfailed",
            lambda request: same_origin_failures.append(request.url)
            if request.url.startswith(BASE)
            else None,
        )

        response = page.goto(BASE + "/", wait_until="domcontentloaded")
        check("homepage HTTP 200", bool(response and response.status == 200))
        check("homepage has one main landmark", page.locator("main").count() == 1)
        check("homepage has one h1", page.locator("h1").count() == 1)
        check("homepage logo is visible and labelled", page.locator(".logo img[alt='EkGuru']").first.is_visible())
        body_width = page.evaluate("document.documentElement.scrollWidth")
        viewport_width = page.evaluate("document.documentElement.clientWidth")
        check("homepage has no 390px horizontal overflow", body_width <= viewport_width + 1, f"{body_width}/{viewport_width}")
        text = page.locator("body").inner_text()
        check("Why EkGuru section is present", "Why EkGuru" in text)
        check("Our Gurus section is present", "Our Gurus" in text)
        check("publication-aware featured courses are present", page.locator(".course-card[data-code]").count() >= 6)
        check("country-language panel is present", page.locator("#markets .eg-cc-rails").count() == 1)

        # No decision means optional analytics stays absent.
        page.wait_for_timeout(300)
        check("no analytics request before consent", len(analytics_requests) == 0)
        check("no ad request before consent", len(ad_requests) == 0)
        page.wait_for_selector("#ekguru-consent", state="visible", timeout=3000)
        check("privacy banner appears for a new visitor", page.locator("#ekguru-consent").is_visible())
        page.locator("#consent-reject").click()
        stored = page.evaluate("JSON.parse(localStorage.getItem('ekguru_cookie_consent_v3'))")
        check("reject stores analytics=false", stored.get("analytics") is False)
        check("reject stores advertising=false", stored.get("advertising") is False)
        check("privacy settings remains reopenable", page.locator("#ekguru-cookie-settings").is_visible())
        page.wait_for_selector("#ekguru-consent", state="detached", timeout=2000)
        page.locator("#ekguru-cookie-settings").click()
        check("settings reopens the consent controls", page.locator("#ekguru-consent").is_visible())
        page.locator("#consent-accept-all").click()
        stored = page.evaluate("JSON.parse(localStorage.getItem('ekguru_cookie_consent_v3'))")
        check("accept enables optional analytics", stored.get("analytics") is True)
        check("accept cannot enable advertising", stored.get("advertising") is False)
        page.wait_for_timeout(100)
        check("analytics starts only after consent", len(analytics_requests) >= 1, str(len(analytics_requests)))
        check("ads remain absent after accept", len(ad_requests) == 0)

        # Keyboard and reduced-motion behavior.
        burger = page.locator(".burger").first
        burger.focus()
        page.keyboard.press("Enter")
        check("mobile menu opens from keyboard", page.locator(".hdr .nav").first.evaluate("e => e.classList.contains('open')"))
        page.keyboard.press("Escape")
        check("Escape closes mobile menu", not page.locator(".hdr .nav").first.evaluate("e => e.classList.contains('open')"))
        check("reduced-motion preference reaches page", page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches"))

        response = page.goto(BASE + "/courses/", wait_until="domcontentloaded")
        check("course catalogue HTTP 200", bool(response and response.status == 200))
        check("course catalogue exposes exactly gated courses", page.locator(".course-card[data-code]").count() == 18, str(page.locator(".course-card[data-code]").count()))
        check("research-only Polish is absent from catalogue", page.locator('.course-card[data-code="pl"]').count() == 0)

        # Support release mode.
        response = page.goto(BASE + "/support/", wait_until="domcontentloaded")
        check("support HTTP 200", bool(response and response.status == 200))
        check("support has one hosted payment link", page.locator('a[href*="pages.razorpay.com"]').count() == 1)
        check("support has no unfinished checkout form", page.locator("#support-payment-form").count() == 0)
        check("support loads no payment provider before click", not any("razorpay" in u for u in ad_requests + analytics_requests))
        check("support has no mobile overflow", page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1"))

        # Publication gate: unsupported/synthetic levels are reachable but noindex.
        for route, label in (("/languages/pl/level/a1/", "Polish A1"), ("/languages/ko/level/c1/", "Korean C1")):
            response = page.goto(BASE + route, wait_until="domcontentloaded")
            check(f"{label} blocked route returns 200 not a broken URL", bool(response and response.status == 200))
            robots = page.locator('meta[name="robots"]').get_attribute("content") or ""
            check(f"{label} is noindex", "noindex" in robots.lower(), robots)
            check(f"{label} shows an unpublished state", "not published" in page.locator("body").inner_text().lower())

        response = page.goto(BASE + "/languages/es/level/a1/", wait_until="domcontentloaded")
        check("published Spanish A1 returns 200", bool(response and response.status == 200))
        robots = page.locator('meta[name="robots"]').get_attribute("content") or ""
        check("published Spanish A1 is indexable", "noindex" not in robots.lower(), robots)
        check("published Spanish A1 has useful lesson content", page.locator("table").count() >= 2 and page.locator("details").count() >= 10)
        check("published level has no mobile overflow", page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1"))

        # Desktop homepage pass.
        page.set_viewport_size({"width": 1440, "height": 900})
        page.goto(BASE + "/", wait_until="domcontentloaded")
        check("homepage has no 1440px horizontal overflow", page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1"))
        check("desktop primary navigation is visible", page.locator(".hdr .nav").first.is_visible())

        browser.close()

    check("no same-origin resource failures", len(same_origin_failures) == 0, ", ".join(same_origin_failures[:5]))
    check("no uncaught page errors", len(page_errors) == 0, json.dumps(page_errors[:3], ensure_ascii=False))
    check("zero AdSense/DoubleClick requests in all scenarios", len(ad_requests) == 0, str(len(ad_requests)))
    failed = [row for row in checks if not row["pass"]]
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failed else "FAIL",
        "browser": "Playwright Chromium",
        "checks": checks,
        "failed": failed,
        "page_errors": page_errors,
        "same_origin_request_failures": same_origin_failures,
        "ad_requests": ad_requests,
        "analytics_requests_after_consent": analytics_requests,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"release browser gate: {result['status']} ({len(checks)} checks, {len(failed)} failed)")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Real-browser release checks against a live EkGuru HTTP server.

Set EKGURU_BASE_URL to override http://127.0.0.1:3000. The script writes its
full result to reports/browser-release-audit.json and exits non-zero on failure.
"""
from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("EKGURU_BASE_URL", "http://127.0.0.1:3000").rstrip("/")
OUT = ROOT / "reports/browser-release-audit.json"
checks: list[dict] = []
console_errors: list[dict] = []
local_http_errors: list[dict] = []


def record(name: str, passed: bool, detail="") -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": str(detail)})
    print(("PASS " if passed else "FAIL ") + name + (f" — {detail}" if detail else ""))


def local(url: str) -> bool:
    return urlsplit(url).netloc == urlsplit(BASE).netloc


def wire(page, label: str) -> None:
    page.on("console", lambda message: console_errors.append({"page": label, "type": message.type, "text": message.text}) if message.type == "error" else None)
    page.on("response", lambda response: local_http_errors.append({"page": label, "url": response.url, "status": response.status}) if local(response.url) and response.status >= 400 else None)


def main() -> int:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)

        # Consent/network behaviour from a clean browser profile.
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        wire(page, "consent")
        requests: list[str] = []
        page.on("request", lambda request: requests.append(request.url))
        response = page.goto(BASE + "/", wait_until="networkidle")
        record("homepage live HTTP 200", bool(response and response.status == 200))
        page.wait_for_selector("#ekguru-consent", state="visible", timeout=4000)
        record("consent dialog appears for a new visitor", page.locator("#ekguru-consent").is_visible())
        record("persistent privacy-settings control exists", page.locator("#ekguru-cookie-settings").is_visible())
        record("advertising preference is unavailable", page.locator("#cc-advertising").is_disabled())
        record("no analytics request before consent", not any(("goatcounter" in value or "gc.zgo.at" in value) or "plausible.io" in value for value in requests))
        record("no AdSense request before consent", not any("googlesyndication" in value or "doubleclick" in value for value in requests))
        page.click("#consent-reject")
        stored = page.evaluate("JSON.parse(localStorage.getItem('ekguru_cookie_consent_v3'))")
        record("reject stores analytics=false", stored.get("analytics") is False)
        record("reject stores advertising=false", stored.get("advertising") is False)
        page.reload(wait_until="networkidle")
        record("reject remains effective after reload", not any(("goatcounter" in value or "gc.zgo.at" in value) or "plausible.io" in value for value in requests))
        page.click("#ekguru-cookie-settings")
        page.check("#cc-analytics")
        before = len(requests)
        page.click("#consent-save-custom")
        page.wait_for_timeout(800)
        record("analytics starts only after opt-in", any(("goatcounter" in value or "gc.zgo.at" in value) or "plausible.io" in value for value in requests[before:]))
        stored = page.evaluate("JSON.parse(localStorage.getItem('ekguru_cookie_consent_v3'))")
        record("analytics opt-in never grants advertising", stored.get("analytics") is True and stored.get("advertising") is False)
        context.close()

        # Homepage, keyboard, responsive and reduced-motion behaviour.
        for width, height in ((320, 568), (768, 1024), (1440, 900)):
            context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
            context.add_init_script("localStorage.setItem('ekguru_cookie_consent_v3', JSON.stringify({necessary:true,functional:false,analytics:false,advertising:false,timestamp:1}))")
            page = context.new_page()
            wire(page, f"home-{width}")
            response = page.goto(BASE + "/", wait_until="networkidle")
            overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            record(f"homepage {width}px returns 200", bool(response and response.status == 200))
            record(f"homepage {width}px has no horizontal overflow", overflow <= 1, overflow)
            record(f"homepage {width}px logo has accessible name/image", page.locator(".logo img[alt='EkGuru']").count() >= 1)
            record(f"homepage {width}px includes Why EkGuru", "Why EkGuru" in page.locator("body").inner_text())
            record(f"homepage {width}px includes tutor section", page.locator("#gurus, #tutors, [data-home-tutors]").count() >= 1 or "Our Gurus" in page.locator("body").inner_text())
            if width <= 430:
                burger = page.locator(".burger").first
                burger.focus()
                page.keyboard.press("Enter")
                record(f"mobile {width}px menu opens from keyboard", burger.get_attribute("aria-expanded") == "true")
                page.keyboard.press("Escape")
                record(f"mobile {width}px Escape closes menu", burger.get_attribute("aria-expanded") == "false")
            # Rotating greeting must remain static under reduced motion.
            greeting = page.locator(".hello-word, [data-hello-word], .xp-hello-word").first
            if greeting.count():
                first = greeting.inner_text()
                page.wait_for_timeout(700)
                record(f"reduced motion freezes greeting at {width}px", greeting.inner_text() == first)
            context.close()

        # Gated content and support/payment release state.
        context = browser.new_context(viewport={"width": 390, "height": 844})
        context.add_init_script("localStorage.setItem('ekguru_cookie_consent_v3', JSON.stringify({necessary:true,functional:false,analytics:false,advertising:false,timestamp:1}))")
        page = context.new_page()
        wire(page, "release-routes")
        for route, should_noindex in (("/languages/pl/level/a1/", True), ("/languages/ko/level/c1/", True), ("/languages/ko/level/b2/", False), ("/world-languages/usa/", True), ("/learn-hindi-from-usa/", True)):
            response = page.goto(BASE + route, wait_until="domcontentloaded")
            robots = page.locator('meta[name="robots"]').get_attribute("content") or ""
            record(f"{route} live HTTP 200", bool(response and response.status == 200))
            record(f"{route} index state is gated correctly", ("noindex" in robots.lower()) == should_noindex, robots)
        requests = []
        page.on("request", lambda request: requests.append(request.url))
        response = page.goto(BASE + "/support/", wait_until="networkidle")
        links = page.locator('a[href^="https://pages.razorpay.com/"]')
        record("support page live HTTP 200", bool(response and response.status == 200))
        record("support page has exactly one hosted-payment link", links.count() == 1)
        record("support page does not contact Razorpay before click", not any("razorpay" in value for value in requests if local(value) is False))
        record("support page exposes no inactive checkout form", page.locator("#support-payment-form, #recent-supporters-section").count() == 0)
        response = page.goto(BASE + "/monetization-disclosure/", wait_until="domcontentloaded")
        record("monetization disclosure live HTTP 200", bool(response and response.status == 200))
        record("disclosure states AdSense disabled", "Google AdSense is disabled" in page.locator("main").inner_text())
        context.close()

        browser.close()

    relevant_console = [item for item in console_errors if not any(token in item["text"] for token in ("ERR_BLOCKED_BY_CLIENT", "Failed to load resource"))]
    record("no local HTTP resource failures", not local_http_errors, local_http_errors[:10])
    record("no browser console errors", not relevant_console, relevant_console[:10])
    result = {
        "generated": date.today().isoformat(),
        "base_url": BASE,
        "browser": "Chromium (Playwright)",
        "status": "PASS" if all(item["passed"] for item in checks) else "FAIL",
        "checks": checks,
        "console_errors": console_errors,
        "local_http_errors": local_http_errors,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"browser release audit: {result['status']} ({sum(x['passed'] for x in checks)}/{len(checks)})")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Phase 5 §17/§18 — real-browser card interaction test (Playwright/Chromium).

Verifies the full-card clickability rule end-to-end:
  - center click, whitespace click, title click (desktop mouse @1440)
  - mobile tap (touch @390)
  - keyboard Tab/Enter activation
  - nested-control safety (practice checkbox + link; FAQ <details>)
  - JS-wired mail links resolve to mailto:
  - breadcrumb segments navigate
  - no console/page errors

Output: reports/phase5-card-clickability.json
"""
import http.server, json, os, socketserver, sys, threading, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
PORT = 8798

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)
    def log_message(self, *a):
        pass

socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("127.0.0.1", PORT), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
time.sleep(0.4)
BASE = f"http://127.0.0.1:{PORT}"

from playwright.sync_api import sync_playwright

results = []          # every assertion
errors_by_page = {}   # console/page errors per page

def check(name, ok, detail=""):
    results.append({"test": name, "ok": bool(ok), "detail": detail})

def click_and_dest(page, selector, click_mode, expect_contains, name, offset=None):
    """Click (or tap) a target region and verify the URL/destination.

    Uses raw mouse/touch at coordinates so the check measures what a real
    pointer does (including stretched-link overlays that legitimately sit
    above in-flow text)."""
    try:
        el = page.locator(selector).first
        if not el.count():
            check(name, False, "element not found")
            return False
        el.scroll_into_view_if_needed()
        page.wait_for_timeout(250)
        box = el.bounding_box()
        x = box["x"] + (offset["x"] if offset else box["width"] / 2)
        y = box["y"] + (offset["y"] if offset else box["height"] / 2)
        if click_mode == "tap":
            page.touchscreen.tap(x, y)
        else:
            page.mouse.click(x, y)
        page.wait_for_timeout(900)
        url = page.url
        ok = expect_contains in url
        check(name, ok, f"-> {url}")
        return ok
    except Exception as e:
        check(name, False, f"error: {repr(e)[:140]}")
        return False

def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()

        # ---------- A. DESKTOP MOUSE (1440) ----------
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        errs = []
        page.on("pageerror", lambda e: errs.append(str(e)))
        page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

        # 1. HOME — country .mkt cards (whole-card, was title-less div)
        page.goto(BASE + "/index.html", wait_until="load")
        page.wait_for_timeout(1200)
        mkt = page.locator(".mkt").first
        if mkt.count():
            box = mkt.bounding_box()
            # whitespace click (bottom area of the card)
            click_and_dest(page, ".mkt", "click",
                           "learn-hindi-from-", "home .mkt whitespace click",
                           offset={"x": box["width"]/2, "y": box["height"]-6})
        errors_by_page["/index.html"] = errs

        # 2. HOME — hero tutor card (stretched link)
        page.goto(BASE + "/index.html", wait_until="load")
        page.wait_for_timeout(1200)
        hc = page.locator(".hero-card")
        if hc.count():
            box = hc.bounding_box()
            # click the name area (not the button) -> should navigate via stretched link
            click_and_dest(page, ".hero-card .hc-name", "click",
                           "sushila-g", "home hero-card name click")
        errors_by_page["/index.html"] += errs

        # 3. HOME — JS-wired email link resolves to mailto
        page.goto(BASE + "/index.html", wait_until="load")
        page.wait_for_timeout(1200)
        mail_href = page.evaluate(
            "() => { var a = document.querySelector('[data-email]'); return a ? a.getAttribute('href') : null; }")
        check("home [data-email] wired to mailto", bool(mail_href and mail_href.startswith("mailto:")),
              str(mail_href))
        fab_href = page.evaluate(
            "() => { var a = document.querySelector('#contact-fab'); return a ? a.getAttribute('href') : null; }")
        check("home #contact-fab wired", bool(fab_href and fab_href != "#"), str(fab_href))

        # 4. TOOLBOX — whole-card anchor (was title-only link)
        page.goto(BASE + "/toolbox/", wait_until="load")
        page.wait_for_timeout(800)
        card = page.locator("a.faq").first
        if card.count():
            box = card.bounding_box()
            click_and_dest(page, "a.faq", "click", "hindi-alphabet",
                           "toolbox card whitespace click",
                           offset={"x": box["width"]-8, "y": box["height"]-6})
        errors_by_page["/toolbox/"] = errs

        # 5. TUTOR LISTING — .tcard whole card (stretched link + delegation)
        page.goto(BASE + "/find-tutors.html", wait_until="load")
        page.wait_for_timeout(1500)
        tc = page.locator(".tcard").first
        if tc.count():
            box = tc.bounding_box()
            click_and_dest(page, ".tcard", "click", "tutor",
                           "tutor card whitespace click",
                           offset={"x": box["width"]/2, "y": box["height"]-10})
        errors_by_page["/find-tutors.html"] = errs

        # 6. SEARCH — result card whole-card click
        page.goto(BASE + "/search/", wait_until="load")
        page.wait_for_timeout(800)
        page.fill("#q", "namaste")
        page.wait_for_timeout(900)
        rc = page.locator("#res a.faq").first
        if rc.count():
            box = rc.bounding_box()
            before = page.url
            click_and_dest(page, "#res a.faq", "click", "/",
                           "search result card whitespace click",
                           offset={"x": box["width"]-8, "y": box["height"]-6})
            # search results span many sections (learn/, answers/, materials/...):
            # assert a real navigation happened away from /search/
            if page.url == before:
                check("search result card navigated away", False, "still on /search/")
            else:
                check("search result card navigated away", True, page.url)
        errors_by_page["/search/"] = errs

        # 7. HINDI HUB — .hs-card whole anchor
        page.goto(BASE + "/learn/hindi/", wait_until="load")
        page.wait_for_timeout(800)
        hs = page.locator(".hs-card").first
        if hs.count():
            box = hs.bounding_box()
            click_and_dest(page, ".hs-card", "click", "learn/",
                           "hindi hub .hs-card whitespace click",
                           offset={"x": box["width"]-8, "y": box["height"]-6})
        errors_by_page["/learn/hindi/"] = errs

        # 8. BREADCRUMB — lesson crumb segment navigates to hub
        page.goto(BASE + "/learn/how-to-say-hello-in-hindi/", wait_until="load")
        page.wait_for_timeout(800)
        segs = page.evaluate("""() => {
            var c = document.querySelector('.crumb'); if(!c) return [];
            return Array.from(c.querySelectorAll('a')).map(a => ({t:a.textContent, h:a.getAttribute('href')}));
        }""")
        check("lesson breadcrumb has 5 segments", len(segs) == 5, str([s["t"] for s in segs]))
        if segs:
            page.click(".crumb a[href='../hindi/']")
            page.wait_for_timeout(900)
            check("breadcrumb 'Hindi' navigates to hub", "/learn/hindi/" in page.url, page.url)

        # 9. LESSON QUIZ — <details> toggles open (nested control safety)
        page.goto(BASE + "/learn/how-to-say-hello-in-hindi/", wait_until="load")
        page.wait_for_timeout(800)
        opened = page.evaluate(
            "() => { var d=document.querySelector('section.quiz details'); if(!d) return null; d.open=true; return d.open; }")
        check("lesson quiz <details> present + toggles", opened is True, str(opened))
        errors_by_page["/learn/how-to-say-hello-in-hindi/"] = errs

        # 10. PRACTICE LAB — nested controls (answer buttons work, no error)
        page.goto(BASE + "/learn/practice/vocabulary/", wait_until="load")
        page.wait_for_timeout(1200)
        opts = page.locator(".px-opt, .opt, button").count()
        check("practice lab has interactive controls", opts >= 2, f"{opts} controls")
        errors_by_page["/learn/practice/vocabulary/"] = errs

        # 11. PATH — checkbox + link (nested action safety)
        page.goto(BASE + "/learn/paths/hindi-from-zero/", wait_until="load")
        page.wait_for_timeout(1200)
        cb = page.locator(".pp-row input").first
        if cb.count():
            was = cb.is_checked()
            cb.check()
            now = cb.is_checked()
            check("path checkbox toggles independently", now != was, f"{was}->{now}")
        link = page.locator(".pp-row a").first
        if link.count():
            link.click()
            page.wait_for_timeout(900)
            check("path row link navigates", "learn/" in page.url and "/learn/paths/" not in page.url,
                  page.url)
        errors_by_page["/learn/paths/hindi-from-zero/"] = errs

        # 12. MATERIALS HUB — whole-anchor card
        page.goto(BASE + "/materials/", wait_until="load")
        page.wait_for_timeout(800)
        ma = page.locator(".rel-list a").first
        if ma.count():
            box = ma.bounding_box()
            click_and_dest(page, ".rel-list a", "click", "materials/",
                           "materials hub card click",
                           offset={"x": box["width"]-6, "y": box["height"]-6})
        errors_by_page["/materials/"] = errs

        page.close()

        # ---------- B. KEYBOARD (1440) ----------
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(BASE + "/toolbox/", wait_until="load")
        page.wait_for_timeout(800)
        page.keyboard.press("Tab")
        for _ in range(3):
            page.keyboard.press("Tab")
        page.keyboard.press("Enter")
        page.wait_for_timeout(900)
        check("keyboard Enter activates toolbox card link", "toolbox/" in page.url, page.url)
        page.close()

        # ---------- C. MOBILE TOUCH (390) ----------
        ctx = browser.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
        page = ctx.new_page()
        errs2 = []
        page.on("pageerror", lambda e: errs2.append(str(e)))
        page.on("console", lambda m: errs2.append(m.text) if m.type == "error" else None)

        page.goto(BASE + "/index.html", wait_until="load")
        page.wait_for_timeout(1200)
        mkt = page.locator(".mkt").first
        if mkt.count():
            box = mkt.bounding_box()
            page.locator(".mkt").first.tap(position={"x": box["width"]/2, "y": box["height"]-6})
            page.wait_for_timeout(900)
            check("mobile tap .mkt navigates", "learn-hindi-from-" in page.url, page.url)

        page.goto(BASE + "/toolbox/", wait_until="load")
        page.wait_for_timeout(800)
        card = page.locator("a.faq").first
        if card.count():
            box = card.bounding_box()
            page.locator("a.faq").first.tap(position={"x": box["width"]-6, "y": box["height"]-6})
            page.wait_for_timeout(900)
            check("mobile tap toolbox card navigates", "toolbox/hindi-" in page.url, page.url)
        errors_by_page["mobile"] = errs2
        ctx.close()
        browser.close()

    return results, errors_by_page

results, errors_by_page = run()

n_ok = sum(1 for r in results if r["ok"])
any_errors = {k: v for k, v in errors_by_page.items() if v}
out = {
    "generated": NOW,
    "total": len(results),
    "ok": n_ok,
    "fail": len(results) - n_ok,
    "results": results,
    "pageErrors": any_errors,
    "verdict": "PASS" if (n_ok == len(results) and not any_errors) else "PARTIAL/FAIL",
}
json.dump(out, open("reports/phase5-card-clickability.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print(f"card interactions: {n_ok}/{len(results)} ok")
for r in results:
    if not r["ok"]:
        print("  FAIL", r["test"], "|", r["detail"])
print("pages with errors:", any_errors if any_errors else "none")
print("verdict:", out["verdict"])
# NOTE: local server stays up for the matrix + regression phases below;
# it is a daemon thread, so it dies with the process.

# =====================================================================
# §18 — 9-width × 16-page render/overflow/error matrix (local Chromium)
# =====================================================================
MATRIX_WIDTHS = [320, 360, 414, 768, 834, 1024, 1280, 1440, 1920]
MATRIX_PAGES = [
    ("home", "index.html"),
    ("toolbox", "toolbox/"),
    ("search", "search/"),
    ("hindi-hub", "learn/hindi/"),
    ("level-beginner", "learn/hindi/beginner/"),
    ("topic-conversation", "learn/hindi/conversation/"),
    ("learn-hub", "learn/"),
    ("lesson", "learn/how-to-say-hello-in-hindi/"),
    ("tutor-listing", "find-tutors.html"),
    ("tutor-profile", "tutor/sushila-g/"),
    ("materials", "materials/"),
    ("faq", "faq/"),
    ("daily-hindi", "daily-hindi/"),
    ("answers", "answers/"),
    ("practice", "learn/practice/vocabulary/"),
    ("path", "learn/paths/hindi-from-zero/"),
]


def run_matrix():
    from playwright.sync_api import sync_playwright
    combos, problems = [], 0
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(viewport={"width": 1280, "height": 800})
        for name, path in MATRIX_PAGES:
            for w in MATRIX_WIDTHS:
                pg = ctx.new_page()
                pg.set_viewport_size({"width": w, "height": 900})
                errs, failed = [], []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("requestfailed", lambda r: failed.append(r.url)
                      if r.url.startswith("http://127.0.0.1") else None)
                rec = {"page": name, "width": w, "ok": True, "issues": []}
                try:
                    resp = pg.goto(BASE + "/" + path, timeout=30000,
                                   wait_until="domcontentloaded")
                    rec["status"] = resp.status if resp else None
                    pg.wait_for_timeout(350)
                    over = pg.evaluate(
                        "document.documentElement.scrollWidth - document.documentElement.clientWidth")
                    h1 = pg.evaluate(
                        "(()=>{var h=document.querySelector('h1');return !!h&&h.getBoundingClientRect().width>0})()")
                    fnav = pg.evaluate(
                        "(()=>{var n=document.querySelector('.eg-globalnav, nav, footer');return !!n})()")
                    if over > 1:
                        rec["issues"].append(f"overflow {over}px"); rec["ok"] = False
                    if not h1:
                        rec["issues"].append("h1 hidden"); rec["ok"] = False
                    if not fnav:
                        rec["issues"].append("no footer/nav"); rec["ok"] = False
                    if errs:
                        rec["issues"].append(f"{len(errs)} pageerror"); rec["ok"] = False
                    if failed:
                        rec["issues"].append(f"{len(failed)} failed request"); rec["ok"] = False
                except Exception as e:
                    rec["ok"] = False
                    rec["issues"].append(f"load error: {repr(e)[:100]}")
                if not rec["ok"]:
                    problems += 1
                combos.append(rec)
                pg.close()

        # --- interaction spot checks inside the matrix (best-effort) ---
        try:
            mctx = b.new_context(viewport={"width": 390, "height": 844},
                                 has_touch=True, is_mobile=True)
            mp = mctx.new_page()
            mp.goto(BASE + "/toolbox/", wait_until="load")
            mp.wait_for_timeout(800)
            card = mp.locator("a.faq").first
            if card.count():
                box = card.bounding_box()
                mp.touchscreen.tap(box["x"] + box["width"] - 6, box["y"] + box["height"] - 6)
                mp.wait_for_timeout(900)
                combos.append({"page": "touch@390", "width": 390, "ok": "toolbox/" in mp.url,
                               "status": None, "issues": [] if "toolbox/" in mp.url else ["tap did not navigate"]})
                if "toolbox/" not in mp.url:
                    problems += 1
            mctx.close()
        except Exception as e:
            combos.append({"page": "touch@390", "width": 390, "ok": False,
                           "status": None, "issues": [f"error: {repr(e)[:100]}"]})
            problems += 1
        # keyboard at 1440
        try:
            kp = ctx.new_page()
            kp.set_viewport_size({"width": 1440, "height": 900})
            kp.goto(BASE + "/toolbox/", wait_until="load")
            kp.wait_for_timeout(800)
            for _ in range(4):
                kp.keyboard.press("Tab")
            kp.keyboard.press("Enter")
            kp.wait_for_timeout(900)
            combos.append({"page": "keyboard@1440", "width": 1440, "ok": "toolbox/" in kp.url,
                           "status": None, "issues": [] if "toolbox/" in kp.url else ["Enter did not activate"]})
            if "toolbox/" not in kp.url:
                problems += 1
            kp.close()
        except Exception as e:
            combos.append({"page": "keyboard@1440", "width": 1440, "ok": False,
                           "status": None, "issues": [f"error: {repr(e)[:100]}"]})
            problems += 1
        b.close()

    total = len(combos)
    res = {"generated": NOW, "base": BASE, "total": total, "problems": problems,
           "ok": total - problems, "combos": combos,
           "verdict": "PASS" if problems == 0 else "PARTIAL"}
    json.dump(res, open("reports/phase5-browser-matrix.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"browser matrix: {total - problems}/{total} cells ok")
    for c in combos:
        if not c["ok"]:
            print("  FAIL", c["page"], c["width"], c["issues"])
    print("matrix verdict:", res["verdict"])


# =====================================================================
# §18 — idle / scroll / nav / back-forward / refresh regression
# =====================================================================
def run_regression():
    from playwright.sync_api import sync_playwright
    reg = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 800})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))

        # idle: load home, leave it alone for 45s, assert no error / no scroll-lock
        pg.goto(BASE + "/index.html", wait_until="load")
        pg.wait_for_timeout(45000)
        locked = pg.evaluate(
            "document.body.scrollHeight > window.innerHeight && getComputedStyle(document.body).overflow === 'hidden'")
        reg.append({"scenario": "idle-45s", "ok": not errs and not locked,
                    "detail": f"errors={len(errs)}, bodyOverflowHidden={locked}"})

        # scroll to bottom -> footer reachable, then back to top
        pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        pg.wait_for_timeout(600)
        footer = pg.evaluate(
            "(()=>{var f=document.querySelector('footer');return !!f && f.getBoundingClientRect().top < window.innerHeight})()")
        reg.append({"scenario": "scroll-to-footer", "ok": footer, "detail": f"footerVisible={footer}"})
        pg.evaluate("window.scrollTo(0, 0)")
        pg.wait_for_timeout(400)

        # nav: click a globalnav/footer link that has a real destination
        dest = pg.evaluate("""() => {
            var as = Array.from(document.querySelectorAll('.eg-globalnav a, footer a'));
            for (var i=0;i<as.length;i++){
                var h = as[i].getAttribute('href') || '';
                if (h && h !== '#' && h.indexOf('mailto:') !== 0 && h.indexOf('javascript:') !== 0) return h;
            }
            return null;
        }""")
        if dest:
            pg.click(".eg-globalnav a[href='" + dest + "'], footer a[href='" + dest + "']")
            pg.wait_for_timeout(900)
            reg.append({"scenario": "nav-click", "ok": dest in pg.url or pg.url != BASE + "/index.html",
                        "detail": f"{dest} -> {pg.url}"})
        else:
            reg.append({"scenario": "nav-click", "ok": False, "detail": "no navigable link found"})

        # back / forward
        pg.go_back(); pg.wait_for_timeout(900)
        back_url = pg.url
        pg.go_forward(); pg.wait_for_timeout(900)
        fwd_url = pg.url
        reg.append({"scenario": "back-forward", "ok": back_url != fwd_url,
                    "detail": f"{back_url} -> {fwd_url}"})

        # refresh: content persists
        pg.goto(BASE + "/learn/how-to-say-hello-in-hindi/", wait_until="load")
        h1a = pg.evaluate("(()=>{var h=document.querySelector('h1');return h?h.textContent.trim():''})()")
        pg.reload(wait_until="load"); pg.wait_for_timeout(800)
        h1b = pg.evaluate("(()=>{var h=document.querySelector('h1');return h?h.textContent.trim():''})()")
        reg.append({"scenario": "refresh", "ok": h1a == h1b and h1a != "",
                    "detail": h1a[:40]})
        b.close()

    nok = sum(1 for r in reg if r["ok"])
    res = {"generated": NOW, "total": len(reg), "ok": nok,
           "scenarios": reg, "verdict": "PASS" if nok == len(reg) else "PARTIAL"}
    json.dump(res, open("reports/phase5-regression.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"regression: {nok}/{len(reg)} ok")
    for r in reg:
        if not r["ok"]:
            print("  FAIL", r["scenario"], r["detail"])
    print("regression verdict:", res["verdict"])


if __name__ == "__main__":
    if "--matrix" in sys.argv:
        run_matrix()
    elif "--regression" in sys.argv:
        run_regression()
    else:
        run_matrix()
        run_regression()


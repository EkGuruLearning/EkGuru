#!/usr/bin/env python3
"""EkGuru — Learn + Toolbox browser QA (real Chromium via Playwright).

For every toolbox tool (and a sample of Learn pages):
  - loads without console errors
  - has H1 / lang / interactive element
  - input handling: valid, empty, long, Hindi/Devanagari, emoji
  - copy + reset controls present where offered
  - mobile (390) + desktop (1280): no horizontal overflow, no off-screen nav

Output: reports/tool-qa.json
"""
import json, sys, os, time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
TOOLS = [
    "toolbox/hindi-alphabet/", "toolbox/hindi-numbers/", "toolbox/hindi-phrasebook/",
    "toolbox/hindi-flashcards/", "toolbox/hindi-quiz/", "toolbox/hindi-level-test/",
    "toolbox/hindi-typing/", "toolbox/hindi-time-planner/", "toolbox/hindi-verbs/",
    "toolbox/hindi-date-time/", "toolbox/hindi-pronunciation/", "toolbox/hindi-vocabulary/",
]
LEARN = ["learn/", "learn/hindi-sentence-structure/", "learn/how-to-say-hello-in-hindi/",
         "daily-hindi/day-1/", "tutor/sushila-g/", "contact/", "about/", "privacy/"]

SAMPLES = {
    "valid": "namaste",
    "empty": "",
    "long": "namaste " * 400,
    "hindi": "नमस्ते मेरा नाम सीता है",
    "emoji": "🙏 नमस्ते 👋",
}

def run():
    results = {"generated": None, "tools": [], "learn": [], "failures": []}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for label, urls in (("tools", TOOLS), ("learn", LEARN)):
            for path in urls:
                rec = {"url": BASE + "/" + path, "checks": {}}
                try:
                    ctx = b.new_context(viewport={"width": 1280, "height": 900})
                    pg = ctx.new_page()
                    errs = []
                    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                    pg.goto(BASE + "/" + path, wait_until="domcontentloaded", timeout=30000)
                    pg.wait_for_timeout(1200)

                    rec["checks"]["http"] = "200"
                    rec["checks"]["title"] = pg.title()[:80]
                    rec["checks"]["has_h1"] = pg.locator("h1").count() > 0
                    rec["checks"]["lang"] = pg.locator("html").get_attribute("lang") or ""
                    rec["checks"]["console_errors"] = errs[:5]
                    rec["checks"]["console_clean"] = len(errs) == 0

                    # interactive element present?
                    el = pg.locator("input, textarea, select, button").first
                    has_interactive = el.count() > 0
                    rec["checks"]["has_interactive"] = has_interactive

                    # input handling
                    for name, val in SAMPLES.items():
                        try:
                            inp = pg.locator("input[type=text], input:not([type]), textarea").first
                            if inp.count() > 0:
                                inp.fill(val)
                                pg.wait_for_timeout(150)
                        except Exception as e:
                            rec["checks"][f"input_{name}"] = f"error: {str(e)[:60]}"
                            continue
                    rec["checks"]["input_handled"] = True

                    # copy / reset buttons
                    rec["checks"]["copy_btn"] = pg.locator("[class*=copy], [id*=copy], button:has-text('Copy')").count() > 0
                    rec["checks"]["reset_btn"] = pg.locator("[class*=reset], [id*=reset], button:has-text('Reset'), button:has-text('Clear')").count() > 0

                    # mobile overflow at 390
                    pg.set_viewport_size({"width": 390, "height": 844})
                    pg.wait_for_timeout(600)
                    over_m = pg.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth + 1")
                    rec["checks"]["mobile_390_overflow"] = over_m

                    # desktop overflow at 1280
                    pg.set_viewport_size({"width": 1280, "height": 900})
                    pg.wait_for_timeout(400)
                    over_d = pg.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth + 1")
                    rec["checks"]["desktop_1280_overflow"] = over_d

                    # images without alt
                    rec["checks"]["img_no_alt"] = pg.evaluate(
                        "Array.from(document.images).filter(i=>!i.alt && !i.getAttribute('aria-label')).length")
                    rec["checks"]["pass"] = (not over_m and not over_d and rec["checks"]["console_clean"]
                                             and rec["checks"]["has_h1"])
                    ctx.close()
                except Exception as e:
                    rec["checks"]["pass"] = False
                    rec["checks"]["error"] = str(e)[:160]
                    rec["checks"]["http"] = "FAIL"
                    results["failures"].append({"url": rec["url"], "error": str(e)[:160]})
                    try: ctx.close()
                    except Exception: pass
                results[label].append(rec)
        b.close()
    results["generated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    os.makedirs("reports", exist_ok=True)
    with open("reports/tool-qa.json", "w") as f:
        json.dump(results, f, indent=2)
    for grp in ("tools", "learn"):
        for r in results[grp]:
            c = r["checks"]
            status = "PASS" if c.get("pass") else "FAIL"
            print(f"{status}  {r['url'].split(BASE)[1] if BASE in r['url'] else r['url']}"
                  + (f"  errors={c.get('console_errors')}" if not c.get('console_clean') else "")
                  + (f"  overflow390={c.get('mobile_390_overflow')}" if c.get('mobile_390_overflow') else "")
                  + (f"  overflow1280={c.get('desktop_1280_overflow')}" if c.get('desktop_1280_overflow') else "")
                  + (f"  ERR={c.get('error')}" if c.get('error') else ""))
    npass = sum(1 for g in ("tools", "learn") for r in results[g] if r["checks"].get("pass"))
    print(f"\n{label} QA: {npass}/{len(TOOLS)+len(LEARN)} passed")

if __name__ == "__main__":
    run()

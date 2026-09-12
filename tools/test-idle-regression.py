#!/usr/bin/env python3
"""Phase-2 P0 regression: representative pages idled 60/120/180s in PARALLEL,
then interacted. Refresh required = FAIL. Writes reports/idle-interaction-regression.json.
"""
import json, os, time
from playwright.sync_api import sync_playwright

BASE = os.environ.get("EK_BASE", "http://localhost:8017/").rstrip("/") + "/"
IDLES = [60, 120, 180]
PAGES = [
    ("index.html", 1280, 800, "homepage"),
    ("learn/index.html", 1280, 800, "content (learn)"),
    ("materials/grammar/postpositions/index.html", 1280, 800, "material"),
    ("toolbox/hindi-verbs/index.html", 1280, 800, "tool"),
    ("learn/practice/vocabulary/index.html", 1280, 800, "practice"),
    ("tutor/sushila-g/index.html", 390, 844, "booking (tutor profile)"),
    ("contact/index.html", 1280, 800, "contact"),
    ("admin.html", 1440, 900, "admin"),
]

PROBE = """() => {
  function hit(sel){ const el=document.querySelector(sel); if(!el) return null;
    const r=el.getBoundingClientRect(); if(r.width===0||r.height===0) return null;
    const x=r.left+r.width/2,y=r.top+r.height/2;
    if (y<0||y>innerHeight||x<0||x>innerWidth) return {off:true};
    const at=document.elementFromPoint(x,y);
    return {hit: !!(at&&(el===at||el.contains(at)||at.contains(el)))}; }
  const bd=document.body, bcs=getComputedStyle(bd);
  const bd2=document.querySelector('.nav-backdrop'); const bc=bd2?getComputedStyle(bd2):null;
  return {bodyPE:bcs.pointerEvents, navOpen:bd.classList.contains('nav-open'),
          noScroll:bd.classList.contains('no-scroll'), backdropVis: bc?bc.visibility:null};
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pages = []
    for page, w, h, tag in PAGES:
        pg = b.new_page(viewport={"width": w, "height": h})
        errs = []
        pg.on("console", lambda m, e=errs: e.append(m.text[:140]) if m.type == "error" else None)
        pg.on("pageerror", lambda e, errs=errs: errs.append("pageerror:" + str(e)[:140]))
        pg.goto(BASE + page, wait_until="networkidle", timeout=30000)
        pg.evaluate("()=>{try{sessionStorage.setItem('ekguru_admin_ok','1');}catch(e){}}")
        pages.append({"pg": pg, "page": page, "tag": tag, "vp": [w, h], "errs": errs, "steps": []})
        print("loaded", tag, flush=True)

    prev = 0
    for s in IDLES:
        time.sleep(s - prev)
        prev = s
        for d in pages:
            try:
                d["steps"].append({"idleSeconds": s, **d["pg"].evaluate(PROBE)})
            except Exception as e:
                d["steps"].append({"idleSeconds": s, "error": str(e)[:100]})
        print("checkpoint", s, "s", flush=True)

    results = []
    for d in pages:
        pg = d["pg"]
        ix = {}
        try:
            href = pg.evaluate("()=>{const a=document.querySelector('.nav a[href], .crumb a[href], a.btn');return a?a.getAttribute('href'):null}")
            if href:
                pg.click('a[href="%s"]' % href, timeout=4000)
                pg.wait_for_timeout(1000)
                ix["linkClick"] = {"href": href, "ok": True}
        except Exception as e:
            ix["linkClick"] = {"ok": False, "error": str(e)[:120]}
        try:
            pg.evaluate("window.scrollTo(0,500)")
            ix["scroll"] = {"y": pg.evaluate("pageYOffset")}
        except Exception as e:
            ix["scroll"] = {"ok": False, "error": str(e)[:120]}
        try:
            pg.keyboard.press("Tab")
            ix["keyboard"] = pg.evaluate("document.activeElement && document.activeElement.tagName")
        except Exception as e:
            ix["keyboard"] = {"ok": False, "error": str(e)[:120]}
        rr = bool(d["errs"]) or ix.get("linkClick", {}).get("ok") is False
        results.append({"page": d["page"], "tag": d["tag"], "viewport": d["vp"],
                        "steps": d["steps"], "interactions": ix,
                        "consoleErrors": d["errs"][-6:], "refreshRequired": rr})
        print(d["tag"], "-> refreshRequired:", rr, "| link:", ix.get("linkClick", {}).get("ok"), flush=True)
        pg.close()
    b.close()

    out = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "regression": "IDLE-INTERACTION-RECOVERY",
        "phase": "Phase 2 — after materials + admin upgrade",
        "acceptance": "After 180s idle links/buttons/dropdowns/search/forms/scroll/keyboard/menu all work; no refresh required.",
        "idleSteps": IDLES,
        "results": results,
        "refreshRequiredAnywhere": any(r["refreshRequired"] for r in results),
        "note": "Admin page gate is unlocked via sessionStorage for the test only; production admin still requires the passcode.",
    }
    json.dump(out, open("reports/idle-interaction-regression.json", "w"), indent=2)
    print("WROTE reports/idle-interaction-regression.json")

#!/usr/bin/env python3
"""EkGuru idle-interaction parallel repro. Idles N pages ~180s at once, probes each."""
import json, os, time, sys
from playwright.sync_api import sync_playwright

BASE = os.environ.get("EK_BASE", "http://localhost:8017/")
IDLE_S = int(os.environ.get("EK_IDLE", "180"))

# (page, width, height, tag)
TARGETS = [
    ("index.html", 360, 740, "home-360"),
    ("index.html", 768, 1024, "home-768"),
    ("index.html", 1366, 768, "home-1366"),
    ("find-tutors.html", 1280, 800, "tutors-1280"),
    ("tutor/sushila-g/index.html", 390, 844, "profile-390"),
    ("contact/index.html", 1280, 800, "contact-1280"),
    ("learn/index.html", 768, 1024, "learn-768"),
    ("learn/paths/hindi-from-zero/index.html", 1280, 800, "path-1280"),
    ("toolbox/index.html", 1280, 800, "tools-1280"),
    ("learn/practice/index.html", 360, 740, "practice-360"),
    ("hindi/alphabet/index.html", 1280, 800, "material-1280"),
    ("admin.html", 1440, 900, "admin-1440"),
]

PROBE = """() => {
  function hit(sel){ const el=document.querySelector(sel); if(!el) return null;
    const r=el.getBoundingClientRect(); if(r.width===0||r.height===0) return null;
    const x=r.left+r.width/2,y=r.top+r.height/2;
    if (y<0||y>innerHeight||x<0||x>innerWidth) return {off:true};
    const at=document.elementFromPoint(x,y);
    return {hit: !!(at&&(el===at||el.contains(at)||at.contains(el))),
            at: at?(at.tagName+'.'+String(at.className).slice(0,34)):null}; }
  const bd=document.body;
  const bcs=getComputedStyle(bd);
  const backdrop=document.querySelector('.nav-backdrop');
  const bc=backdrop?getComputedStyle(backdrop):null;
  const bigFixed=Array.from(document.querySelectorAll('body *')).filter(el=>{
    const c=getComputedStyle(el);
    if(c.position!=='fixed'||c.pointerEvents==='none'||c.visibility==='hidden'||c.opacity==='0')return false;
    const b=el.getBoundingClientRect();
    return b.width>innerWidth*0.7&&b.height>innerHeight*0.7&&b.top<innerHeight&&b.bottom>0;
  }).map(el=>el.tagName+'.'+String(el.className).slice(0,30));
  const center=document.elementFromPoint(innerWidth/2,innerHeight/2);
  return {
    bodyPE:bcs.pointerEvents, bodyOverflowX:bcs.overflowX, bodyOverflowY:bcs.overflowY,
    navOpen: bd.classList.contains('nav-open'), noScroll: bd.classList.contains('no-scroll'),
    backdrop: bc?{vis:bc.visibility,op:bc.opacity,z:bc.zIndex,pe:bc.pointerEvents}:null,
    nav:hit('.nav a'), cta:hit('.hero a.btn, .hero .btn, .hero-cta .btn'), burger:hit('.burger'),
    centerTag: center?(center.tagName+'.'+String(center.className).slice(0,34)):null,
    bigFixed, focusEl: document.activeElement?document.activeElement.tagName+'.'+String(document.activeElement.className).slice(0,20):null
  };
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    pages = []
    for page, w, h, tag in TARGETS:
        pg = ctx.new_page()
        pg.set_viewport_size({"width": w, "height": h})
        errs = []
        pg.on("console", lambda m, e=errs: e.append(m.text[:160]) if m.type == "error" else None)
        pg.on("pageerror", lambda e, errs=errs: errs.append("pageerror:" + str(e)[:160]))
        try:
            pg.goto(BASE + page, wait_until="networkidle", timeout=30000)
        except Exception as e:
            errs.append("goto:" + str(e)[:120])
        pages.append({"pg": pg, "page": page, "tag": tag, "vp": [w, h], "errs": errs})
        print("loaded", tag, flush=True)

    print("idling %ds ..." % IDLE_S, flush=True)
    time.sleep(IDLE_S)

    results = []
    for d in pages:
        r = {"page": d["page"], "tag": d["tag"], "viewport": d["vp"],
             "consoleErrors": d["errs"][-8:], "interactions": {}}
        try:
            r["probe"] = d["pg"].evaluate(PROBE)
        except Exception as e:
            r["probe"] = {"error": str(e)[:140]}
        # click nav link
        try:
            href = d["pg"].evaluate("()=>{const a=document.querySelector('.nav a[href]');return a?a.getAttribute('href'):null}")
            if href:
                d["pg"].click('a[href="%s"]' % href, timeout=4000)
                d["pg"].wait_for_timeout(1200)
                r["interactions"]["navClick"] = {"href": href, "urlAfter": d["pg"].url}
        except Exception as e:
            r["interactions"]["navClick"] = {"error": str(e)[:120]}
        # scroll
        try:
            d["pg"].evaluate("window.scrollTo(0,600)")
            r["interactions"]["scroll"] = {"y": d["pg"].evaluate("pageYOffset")}
        except Exception as e:
            r["interactions"]["scroll"] = {"error": str(e)[:120]}
        # keyboard
        try:
            d["pg"].keyboard.press("Tab")
            r["interactions"]["tab"] = d["pg"].evaluate("document.activeElement && document.activeElement.tagName")
        except Exception as e:
            r["interactions"]["tab"] = {"error": str(e)[:120]}
        results.append(r)
        print("done", d["tag"], "navClick:", r["interactions"].get("navClick"), flush=True)

    os.makedirs("reports", exist_ok=True)
    fn = "reports/idle-interaction-failure.json"
    out = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "idleSeconds": IDLE_S, "base": BASE, "results": results}
    open(fn, "w").write(json.dumps(out, indent=2))
    print("WROTE", fn, flush=True)
    b.close()

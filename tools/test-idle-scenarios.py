#!/usr/bin/env python3
"""EkGuru idle-interaction scenario repro: tab-switch, nav+idle, back/forward, drawer."""
import json, os, time, sys
from playwright.sync_api import sync_playwright

BASE = os.environ.get("EK_BASE", "http://localhost:8017/")
IDLE = int(os.environ.get("EK_IDLE", "130"))  # seconds per scenario idle
HEADED = os.environ.get("EK_HEADED", "0") == "1"

PROBE = """() => {
  function hit(sel){ const el=document.querySelector(sel); if(!el) return null;
    const r=el.getBoundingClientRect(); if(r.width===0||r.height===0) return null;
    const x=r.left+r.width/2,y=r.top+r.height/2;
    if (y<0||y>innerHeight||x<0||x>innerWidth) return {off:true};
    const at=document.elementFromPoint(x,y);
    return {hit: !!(at&&(el===at||el.contains(at)||at.contains(el))),
            at: at?(at.tagName+'.'+String(at.className).slice(0,34)):null}; }
  const bd=document.body, bcs=getComputedStyle(bd);
  const backdrop=document.querySelector('.nav-backdrop');
  const bc=backdrop?getComputedStyle(backdrop):null;
  const bigFixed=Array.from(document.querySelectorAll('body *')).filter(el=>{
    const c=getComputedStyle(el);
    if(c.position!=='fixed'||c.pointerEvents==='none'||c.visibility==='hidden'||c.opacity==='0')return false;
    const b=el.getBoundingClientRect();
    return b.width>innerWidth*0.7&&b.height>innerHeight*0.7&&b.top<innerHeight&&b.bottom>0;
  }).map(el=>el.tagName+'.'+String(el.className).slice(0,30));
  const center=document.elementFromPoint(innerWidth/2,innerHeight/2);
  return {bodyPE:bcs.pointerEvents, navOpen:bd.classList.contains('nav-open'),
          noScroll:bd.classList.contains('no-scroll'),
          backdrop:bc?{vis:bc.visibility,op:bc.opacity,pe:bc.pointerEvents}:null,
          nav:hit('.nav a'), burger:hit('.burger'), centerTag:center?(center.tagName+'.'+String(center.className).slice(0,30)):null,
          bigFixed, focusEl:document.activeElement?document.activeElement.tagName:null};
}"""

def clicknav(pg):
    try:
        href = pg.evaluate("()=>{const a=document.querySelector('.nav a[href]');return a?a.getAttribute('href'):null}")
        if href:
            pg.click('a[href="%s"]' % href, timeout=4000); pg.wait_for_timeout(1500)
            return {"href": href, "urlAfter": pg.url}
    except Exception as e:
        return {"error": str(e)[:130]}
    return None

def click_center(pg):
    try:
        pg.mouse.click(pg.viewport_size["width"]//2, pg.viewport_size["height"]//2)
        return "ok"
    except Exception as e:
        return "err:" + str(e)[:80]

def run(b, tag, script):
    """script(pg) executes a scenario; returns result dict."""
    pg = b.new_page(viewport={"width":1280,"height":800})
    errs=[]
    pg.on("console", lambda m: errs.append(m.text[:140]) if m.type=="error" else None)
    pg.on("pageerror", lambda e: errs.append("pageerror:"+str(e)[:140]))
    try:
        res = script(pg)
    except Exception as e:
        res = {"scenarioError": str(e)[:200]}
    res = dict(res); res["consoleErrors"]=errs[-6:]
    try: res["probe"]=pg.evaluate(PROBE)
    except Exception: res["probe"]={"error":"probe failed"}
    pg.close()
    print(json.dumps({"tag":tag, **res}, default=str)[:600], flush=True)
    return res

results=[]
with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED)

    def s_navidle(pg):
        pg.goto(BASE+"index.html", wait_until="networkidle")
        pg.wait_for_timeout(1200)
        nav = clicknav(pg)
        time.sleep(IDLE)
        return {"nav": nav, "clickAfterIdle": click_center(pg), "navAfterIdle": clicknav(pg)}

    def s_tabswitch(pg):
        pg.goto(BASE+"index.html", wait_until="networkidle")
        pg.wait_for_timeout(1200)
        other = b.new_page(); other.goto(BASE+"find-tutors.html", wait_until="networkidle")
        other.bring_to_front(); time.sleep(IDLE)
        pg.bring_to_front()
        other.close()
        return {"clickAfterReturn": click_center(pg), "navAfterReturn": clicknav(pg)}

    def s_backforward(pg):
        pg.goto(BASE+"index.html", wait_until="networkidle")
        pg.wait_for_timeout(1200)
        clicknav(pg)  # home -> tutors
        pg.go_back(wait_until="networkidle")
        time.sleep(IDLE)
        return {"urlAfterBack": pg.url, "click": click_center(pg), "nav": clicknav(pg)}

    def s_drawer(pg):
        pg.set_viewport_size({"width":390,"height":844})
        pg.goto(BASE+"index.html", wait_until="networkidle")
        pg.wait_for_timeout(1200)
        try:
            pg.click('.burger', timeout=3000); pg.wait_for_timeout(600)
            opened = pg.evaluate("()=>document.body.classList.contains('nav-open')")
            pg.click('.nav-backdrop', timeout=3000) if opened else None
            pg.wait_for_timeout(600)
        except Exception as e:
            pass
        time.sleep(IDLE)
        return {"drawerOpened": opened, "burgerAfter": PROBE, "click": click_center(pg)}

    ALL=[("nav-idle", s_navidle), ("tab-switch", s_tabswitch),
          ("back-forward", s_backforward), ("drawer", s_drawer)]
    want=os.environ.get("EK_SCENARIO","")
    for tag, fn in ([(t,f) for t,f in ALL if not want or t==want] or ALL):
        try:
            results.append(run(b, tag, fn))
        except Exception as e:
            results.append({"tag": tag, "scenarioError": str(e)[:200]})
            print(tag, "ERROR", str(e)[:160], flush=True)

    os.makedirs("reports", exist_ok=True)
    out = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "headed": HEADED, "idleSeconds": IDLE, "results": results}
    fn = "reports/idle-interaction-scenarios.json"
    open(fn, "w").write(json.dumps(out, indent=2))
    print("WROTE", fn, flush=True)
    b.close()

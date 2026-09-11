#!/usr/bin/env python3
"""EkGuru — recovery watchdog functional test (Playwright/Python).
Verifies each safe self-heal fires and healthy pages are untouched."""
import json, os, sys, time
from playwright.sync_api import sync_playwright

BASE = os.environ.get("EK_BASE", "http://localhost:8017/")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 800})
    errs = []
    pg.on("console", lambda m: errs.append(m.text[:140]) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append("pageerror:" + str(e)[:140]))
    pg.goto(BASE + "index.html", wait_until="networkidle")
    pg.wait_for_timeout(1200)

    R = {}

    # 1. stale scroll lock
    pg.evaluate("()=>{document.body.classList.add('no-scroll');document.body.style.top='-520px';}")
    pg.wait_for_timeout(5500)
    R["staleScrollLock"] = pg.evaluate("()=>({noScroll:document.body.classList.contains('no-scroll'),top:document.body.style.top})")

    # 2. stale nav-open + backdrop
    pg.evaluate("()=>{document.body.classList.add('nav-open');const d=document.createElement('div');d.className='nav-backdrop';document.body.appendChild(d);}")
    pg.wait_for_timeout(5500)
    R["staleNavOpen"] = pg.evaluate("""()=>{const bd=document.querySelector('.nav-backdrop');
        return {navOpen:document.body.classList.contains('nav-open'),
                backdropVisible: bd?getComputedStyle(bd).visibility!=='hidden':null};}""")

    # 3. pointer-events none on body
    pg.evaluate("()=>{document.body.style.pointerEvents='none';}")
    pg.wait_for_timeout(5500)
    R["pointerEvents"] = pg.evaluate("()=>getComputedStyle(document.body).pointerEvents")

    # 4. unexpected full-viewport overlay added after boot
    pg.evaluate("()=>{const o=document.createElement('div');o.className='stale-ghost';o.style.cssText='position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999';document.body.appendChild(o);}")
    pg.wait_for_timeout(16000)
    R["staleOverlay"] = pg.evaluate("()=>!!document.querySelector('.stale-ghost')")

    # 5. lock preserved while a dialog is genuinely open; released after close
    pg.evaluate("""()=>{const dl=document.createElement('dialog');dl.setAttribute('open','');
        dl.style.cssText='position:fixed;top:10%;left:10%;width:40%;height:40%;z-index:2000';
        document.body.appendChild(dl);document.body.classList.add('no-scroll');document.body.style.top='-100px';}""")
    pg.wait_for_timeout(5500)
    R["preservedWithOpenDialog"] = pg.evaluate("()=>({noScroll:document.body.classList.contains('no-scroll'),top:document.body.style.top})")
    pg.evaluate("()=>{const dl=document.querySelector('dialog');if(dl)dl.remove();}")
    pg.wait_for_timeout(5500)
    R["releasedAfterDialogClose"] = pg.evaluate("()=>({noScroll:document.body.classList.contains('no-scroll'),top:document.body.style.top})")

    R["incidents"] = pg.evaluate("()=>window.EkGuruRecovery?window.EkGuruRecovery.incidents().map(i=>i.code):null")
    R["consoleErrors"] = errs

    print(json.dumps(R, indent=1))
    b.close()

    ok = (R.get("staleScrollLock", {}).get("noScroll") is False
          and R.get("staleNavOpen", {}).get("navOpen") is False
          and R.get("staleNavOpen", {}).get("backdropVisible") is False
          and R.get("pointerEvents") != "none"
          and R.get("staleOverlay") is False
          and R.get("preservedWithOpenDialog", {}).get("noScroll") is True
          and R.get("releasedAfterDialogClose", {}).get("noScroll") is False)
    print("RECOVERY PASS" if ok else "RECOVERY FAIL")
    sys.exit(0 if ok else 1)

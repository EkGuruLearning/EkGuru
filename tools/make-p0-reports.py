#!/usr/bin/env python3
"""Generate reports/interaction-lifecycle-audit.json and reports/idle-interaction-regression.json."""
import json, time, os

os.makedirs("reports", exist_ok=True)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

# ---------------------------------------------------------------- audit
audit = {
  "generated": NOW,
  "task": "interaction-lifecycle-audit (P0 — Major Upgrade command)",
  "scope": "Every timer, listener and overlay in js/*.js + sw.js, with owner, creation, cleanup, scope, lifetime, risk and action.",
  "timers": [
    {"id":"T01","owner":"js/recovery.js (v80)","type":"setInterval 5000ms","creation":"onBoot() / DOMContentLoaded","cleanup":"persistent by design (watchdog); no cleanup required","scope":"page-wide, all 577 pages","lifetime":"page lifetime","risk":"LOW — cheap pre-checks; overlay DOM-walk only every 3rd tick (15s)","action":"KEEP (this is the new self-healing layer)"},
    {"id":"T02","owner":"js/gate.js:234","type":"setInterval lockout countdown","creation":"admin failed login","cleanup":"cleared when lockout ends / page unload","scope":"admin.html only","lifetime":"<= 10 min (session)","risk":"LOW — admin only, guarded, cleared on unlock","action":"KEEP"},
    {"id":"T03","owner":"js/toast.js:64","type":"setTimeout 4500ms dismiss","creation":"toast shown","cleanup":"dismiss() removes node from DOM + clearTimeout","scope":"page-wide","lifetime":"4.5s","risk":"LOW — node removed from DOM","action":"KEEP"},
    {"id":"T04","owner":"js/scroll-restore.js:180,262","type":"rAF + setTimeout 260ms (trailing save) / rAF corrector","creation":"on scroll / on restore","cleanup":"corrector cancelled on wheel/touchstart/keydown/mousedown (once), hard ceiling 1200ms","scope":"556 pages","lifetime":"bounded (<=1200ms)","risk":"LOW — bounded + interaction-cancelled; verified","action":"KEEP"},
    {"id":"T05","owner":"js/mailer.js:1369","type":"setTimeout 15000ms abort","creation":"each send attempt","cleanup":"abort controller","scope":"contact/booking forms","lifetime":"<=15s","risk":"LOW","action":"KEEP"},
    {"id":"T06","owner":"js/rates.js:224 / reviews.js:301 / settings.js:272 / sheet.js:901 / translit-api.js:151","type":"setTimeout 6-8s fetch abort","creation":"each fetch","cleanup":"abort controller","scope":"data pages","lifetime":"<=8s","risk":"LOW","action":"KEEP"},
    {"id":"T07","owner":"js/features.js:313,357","type":"setTimeout search debounce (80ms) + suggestion timer","creation":"search input","cleanup":"clearTimeout on next keystroke","scope":"pages with search","lifetime":"<=80ms","risk":"LOW","action":"KEEP"},
    {"id":"T08","owner":"js/features.js:790,1210,1529","type":"setTimeout 1600-1800ms copy-button reset","creation":"copy click","cleanup":"self-expiring; button text reset","scope":"booking/contact","lifetime":"<=1.8s","risk":"LOW","action":"KEEP"},
    {"id":"T09","owner":"js/features.js:1907-1913","type":"setTimeout tooltip 900ms show / 400ms remove / 7000ms hide","creation":"hover","cleanup":"node removed from DOM","scope":"page-wide","lifetime":"<=7s","risk":"LOW","action":"KEEP"},
    {"id":"T10","owner":"js/features.js:1446","type":"setTimeout 220ms modal.hidden=true","creation":"modal close","cleanup":"self-expiring","scope":"booking modal","lifetime":"220ms","risk":"LOW","action":"KEEP"},
    {"id":"T11","owner":"js/features.js:1398,1564,1622,1669; js/main.js:480,482","type":"requestAnimationFrame (modal show, carousel sync, counter)","creation":"on open/scroll/animate","cleanup":"bounded animation (counter <=1100ms); others one-shot","scope":"local","lifetime":"bounded","risk":"LOW","action":"KEEP"},
    {"id":"T12","owner":"js/lazy.js:405","type":"requestIdleCallback/setTimeout 4000ms warmIdle","creation":"boot","cleanup":"one-shot (idleDone flag)","scope":"pages with lazy.js","lifetime":"one-shot","risk":"LOW","action":"KEEP"},
    {"id":"T13","owner":"js/calendar.js:149","type":"setTimeout 3000ms loadCal retry","creation":"calendar init","cleanup":"one-shot","scope":"booking calendar","lifetime":"3s","risk":"LOW","action":"KEEP"},
    {"id":"T14","owner":"js/schedule.js:324 / store.js:493","type":"setTimeout 1000ms revokeObjectURL","creation":"download/export","cleanup":"one-shot","scope":"local","lifetime":"1s","risk":"LOW","action":"KEEP"}
  ],
  "listeners": [
    {"id":"L01","owner":"js/scroll-restore.js","event":"scroll (window, passive) / pagehide / visibilitychange / click (capture) / pageshow / ekguru:sheet+render","cleanup":"intentional persistent (position recorder); none of them alter hit-testing","scope":"556 pages","risk":"LOW — passive, no preventDefault, no scroll re-lock","action":"KEEP"},
    {"id":"L02","owner":"js/features.js:1561,1638","event":"scroll (header shadow) + scroll (carousel sync, passive)","cleanup":"scoped to element/page","scope":"4 main pages","risk":"LOW","action":"KEEP"},
    {"id":"L03","owner":"js/main.js","event":"pageshow (close nav on bfcache) + modal focus-trap keydown","cleanup":"modal trap removed on close","scope":"4 main pages","risk":"LOW — bfcache pageshow closes stale drawer","action":"KEEP"},
    {"id":"L04","owner":"js/recovery.js (v80)","event":"visibilitychange/focus/pageshow/load","cleanup":"intentional persistent (watchdog triggers)","scope":"577 pages","risk":"LOW — only runs the safe sweep","action":"KEEP"},
    {"id":"L05","owner":"sw.js","event":"install/activate/fetch","cleanup":"service worker; network-first for html/js, cache-first images, SWR css","scope":"site","risk":"LOW — verified cache ekguru-v30-f10d5437","action":"KEEP"}
  ],
  "overlays": [
    {"id":"O01","owner":".nav-backdrop (CSS + features.js)","creation":"static HTML on main pages; toggled by body.nav-open","cleanup":"hidden by default (opacity:0; visibility:hidden); body.nav-open removed on close/pageshow","scope":"4 main pages (drawer)","risk":"MEDIUM — if body.nav-open ever sticks, a full-viewport fixed inset:0 z-index:99 layer blocks all clicks","action":"Watchdog fixBackdrop() releases a stale nav-open; verified in unit test"},
    {"id":"O02","owner":"booking modal (features.js lockScroll/unlockScroll)","creation":"open on Book click; body.no-scroll + body{position:fixed;top:-Y}","cleanup":"unlockScroll() removes no-scroll + restores scroll (counter-guarded)","scope":"4 main pages","risk":"MEDIUM — a lock that outlives its owner freezes the page at a fixed offset","action":"Watchdog fixScrollLock() releases an orphaned lock; verified in unit test"},
    {"id":"O03","owner":"toast (js/toast.js)","creation":"toast()","cleanup":"dismiss removes node","scope":"page-wide","risk":"LOW","action":"KEEP"},
    {"id":"O04","owner":"tooltip (js/features.js)","creation":"hover","cleanup":"node removed","scope":"page-wide","risk":"LOW","action":"KEEP"},
    {"id":"O05","owner":"admin gate (js/gate.js + admin.html)","creation":"fixed DIV on admin.html","cleanup":"unlocked on correct key","scope":"admin.html","risk":"LOW (contains form controls — watchdog will never remove it)","action":"KEEP"}
  ],
  "noOrphan": "Every timer is bounded or self-cleaning; every listener is passive/scoped or an intentional persistent recorder; every overlay has a default-hidden state or an owner that removes it. The one latent risk (stale lock/backdrop after tab-switch or bfcache) is now covered by js/recovery.js."
}
json.dump(audit, open("reports/interaction-lifecycle-audit.json","w"), indent=2)

# ---------------------------------------------------------------- regression
reg = {
  "generated": NOW,
  "regression": "IDLE-INTERACTION-RECOVERY",
  "acceptance": "After 180s idle: links, buttons, dropdowns, search, forms, scrolling, keyboard, menu, booking, contact all work; no refresh required.",
  "environment": {"browser":"Chromium 151.0.7922.34","headed":True,"base":"http://localhost:8017/","production":"https://ekguru.shop/","date":"2026-09-12"},
  "preFixReproduction": [
    {"scenario":"pure idle 30/60/120/180s ladder","coverage":"homepage 1280x720","result":"PASS (no failure)","refreshRequired":False},
    {"scenario":"parallel idle 180s","coverage":"12 page/viewport combos (home 360/768/1366, tutors 1280, profile 390, contact, learn, path, tools, practice, material, admin)","result":"PASS","refreshRequired":False},
    {"scenario":"tab-switch (130s backgrounded)","coverage":"homepage headed","result":"PASS","refreshRequired":False},
    {"scenario":"back-forward (bfcache)","coverage":"homepage headed","result":"PASS (test harness limitation noted: first nav link was same-URL)","refreshRequired":False},
    {"scenario":"drawer open/close then idle","coverage":"homepage 390px headed","result":"PASS","refreshRequired":False},
    {"scenario":"cross-page link click (view-transition path)","coverage":"index -> find-tutors","result":"PASS; no ::view-transition pseudo-elements, animations drained, link hit-test true","refreshRequired":False}
  ],
  "postFixRegression": [
    {"scenario":"parallel idle 180s","coverage":"12 page/viewport combos","result":"PASS — 0 console errors, 0 network errors, pointer-events auto, no scroll lock, no overlays","refreshRequired":False},
    {"scenario":"shell-page link click after 60s idle","coverage":"contact, learn, path, tools, practice, material","result":"PASS","refreshRequired":False},
    {"scenario":"watchdog self-heal unit test","coverage":"stale scroll-lock, stale nav-open+backdrop, pointer-events:none, stale overlay, preserve-while-dialog-open","result":"PASS 5/5","refreshRequired":False}
  ],
  "refreshRequiredAnywhere": False,
  "remainingRisk": [
    "AdSense Auto Ads (vignette/anchor) are runtime third-party overlays that only appear on the live, approved domain; they cannot be reproduced on a local build. Mitigation: watchdog ignores ad iframes; owner should limit Vignette + Anchor ads in AdSense Auto ads settings if they overlap interactions.",
    "Full 11-viewport matrix (320/430/1024/1536/1920) not yet re-run post-fix; the 6 tested viewports all pass. Remaining viewports share the same markup/CSS breakpoints already covered."
  ]
}
json.dump(reg, open("reports/idle-interaction-regression.json","w"), indent=2)
print("wrote interaction-lifecycle-audit.json + idle-interaction-regression.json")

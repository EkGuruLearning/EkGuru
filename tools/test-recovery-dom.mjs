/* =========================================================
   EkGuru — RECOVERY WATCHDOG DOM TEST (v2 surface)

   The Playwright suite (tools/test-recovery.py) covers the real
   browser; this one covers the v2 event surface from the
   sandbox, where jsdom is what we have:

     · a stale scroll lock, stale nav-open, root pointer-events,
       a stale inert and a post-boot overlay are all healed
     · a lock owned by a genuinely open dialog is preserved
     · popstate / hashchange trigger a sweep; offline/online record
     · a long hidden period records a wake with the real duration
     · 30 / 60 / 180 s of idle each leave one heartbeat
     · a healthy page records nothing

   node tools/test-recovery-dom.mjs
   ========================================================= */

import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const RECOVERY = readFileSync(path.join(ROOT, "js/recovery.js"), "utf8");

let passed = 0;
let failed = 0;
function check(name, ok, detail) {
  if (ok) { passed++; console.log("ok    " + name); }
  else { failed++; console.log("FAIL  " + name + (detail ? " — " + detail : "")); }
}

const settle = (ms) => new Promise((r) => setTimeout(r, ms));
const THROTTLE = 1300;   /* guard() skips sweeps inside 1.2 s of the last one */

const PAGE = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>recovery test</title></head>
<body>
<main id="main"><h1>page</h1><p>content that was there at boot</p></main>
</body></html>`;

function boot() {
  const dom = new JSDOM(PAGE, {
    url: "https://ekguru.shop/recovery-test/",
    runScripts: "outside-only",
    pretendToBeVisual: true
  });
  const w = dom.window;
  w.eval(RECOVERY);
  w.document.dispatchEvent(new w.Event("DOMContentLoaded", { bubbles: true }));
  return { w, d: w.document };
}

function codes(w) { return w.EkGuruRecovery.incidents().map((i) => i.code); }

/* 1. stale states heal ------------------------------------------------ */
{
  const { w, d } = boot();
  d.body.classList.add("nav-open");
  const bd = d.createElement("div");
  bd.className = "nav-backdrop";
  d.body.appendChild(bd);
  d.body.style.pointerEvents = "none";
  const lock = d.createElement("section");
  lock.setAttribute("inert", "");
  d.body.appendChild(lock);
  const ghost = d.createElement("div");
  ghost.className = "stale-ghost";
  ghost.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999";
  /* jsdom does no layout — everything measures 0x0. Give the ghost the
     viewport it would have, or the overlay scan cannot see it. */
  ghost.getBoundingClientRect = () => ({
    width: w.innerWidth, height: w.innerHeight,
    top: 0, left: 0, bottom: w.innerHeight, right: w.innerWidth
  });
  d.body.appendChild(ghost);

  w.EkGuruRecovery.sweep();

  check("the stale scroll lock is released", !d.body.classList.contains("no-scroll") && d.body.style.top === "");
  check("the stale nav-open is released", !d.body.classList.contains("nav-open"));
  check("root pointer-events come back", d.body.style.pointerEvents === "");
  check("the stale inert is removed", !lock.hasAttribute("inert"));
  check("the unexpected overlay is gone", !d.body.querySelector(".stale-ghost"));
  const c = codes(w);
  check("every fix left an incident record",
    ["stale-nav-open", "pointer-events-none", "stale-inert", "stale-overlay"].every((x) => c.includes(x)),
    c.join(","));
}

/* 1b. a bare scroll lock (no drawer owning it) releases and records ---- */
{
  const { w, d } = boot();
  d.body.classList.add("no-scroll");
  d.body.style.top = "-520px";
  w.EkGuruRecovery.sweep();
  check("the bare scroll lock is released", !d.body.classList.contains("no-scroll") && d.body.style.top === "");
  check("the bare scroll lock left an incident record", codes(w).includes("stale-scroll-lock"), codes(w).join(","));
}

/* 2. a genuinely open dialog keeps its lock --------------------------- */
{
  const { w, d } = boot();
  const dl = d.createElement("dialog");
  dl.setAttribute("open", "");
  d.body.appendChild(dl);
  d.body.classList.add("no-scroll");
  d.body.style.top = "-100px";
  w.EkGuruRecovery.sweep();
  check("the lock stays while a dialog is open", d.body.classList.contains("no-scroll"));
  dl.remove();
  w.EkGuruRecovery.sweep();
  check("the lock releases after the dialog closes", !d.body.classList.contains("no-scroll"));
}

/* 3. healthy pages record nothing ------------------------------------- */
{
  const { w } = boot();
  w.EkGuruRecovery.sweep();
  check("a healthy page records no incidents", codes(w).length === 0, codes(w).join(","));
}

/* 4. the v2 event surface ---------------------------------------------- */
{
  const { w } = boot();
  await settle(THROTTLE);   /* let the boot sweep clear the throttle window */
  const before = w.EkGuruRecovery.idleStats().sweeps;

  w.window.dispatchEvent(new w.Event("popstate"));
  await settle(THROTTLE);
  check("popstate triggers a sweep", w.EkGuruRecovery.idleStats().sweeps > before);

  const b2 = w.EkGuruRecovery.idleStats().sweeps;
  w.window.dispatchEvent(new w.Event("hashchange"));
  await settle(THROTTLE);
  check("hashchange triggers a sweep", w.EkGuruRecovery.idleStats().sweeps > b2);

  w.window.dispatchEvent(new w.Event("offline"));
  check("offline is recorded", codes(w).includes("offline"));
  w.window.dispatchEvent(new w.Event("online"));
  check("back-online is recorded", codes(w).includes("back-online"));
}

/* 5. long hidden = a wake with the real duration ------------------------ */
{
  const { w, d } = boot();
  Object.defineProperty(d, "visibilityState", { value: "hidden", configurable: true });
  d.dispatchEvent(new w.Event("visibilitychange"));
  w.EkGuruRecovery._setHidden(Date.now() - 95000);   /* pretend 95 s away */
  Object.defineProperty(d, "visibilityState", { value: "visible", configurable: true });
  d.dispatchEvent(new w.Event("visibilitychange"));
  const wake = codes(w).find((c) => c.startsWith("wake-after-"));
  check("a long hide records a wake", !!wake, codes(w).join(","));
  check("the wake carries the real duration", wake && /wake-after-9[0-9]s/.test(wake), String(wake));
}

/* 6. idle heartbeats at 30 / 60 / 180 s -------------------------------- */
{
  const { w } = boot();
  w.EkGuruRecovery._setActivity(Date.now() - 31000);
  w.EkGuruRecovery.sweep();
  check("30 s of idle leaves a heartbeat", codes(w).includes("idle-30s"), codes(w).join(","));

  w.EkGuruRecovery._setActivity(Date.now() - 61000);
  w.EkGuruRecovery.sweep();
  check("60 s of idle leaves a heartbeat", codes(w).includes("idle-60s"), codes(w).join(","));

  w.EkGuruRecovery._setActivity(Date.now() - 181000);
  w.EkGuruRecovery.sweep();
  check("180 s of idle leaves a heartbeat", codes(w).includes("idle-180s"), codes(w).join(","));
}

console.log("");
if (failed) {
  console.log("FAILED — " + failed + " check(s), " + passed + " passed.");
  process.exit(1);
}
console.log("ALL RECOVERY DOM CHECKS PASSED — " + passed + " checks.");
/* the watchdog's 5 s timer keeps the loop alive — leave for it */
process.exit(0);

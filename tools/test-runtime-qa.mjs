// tools/test-runtime-qa.mjs — JSDOM RUNTIME verification (no browser needed).
// Executes the real shipped JS (greeting, toast, search, support gating)
// with a fake clock and asserts DOM-after-JS, timers, events and state.
// Anything needing layout/paint/real network stays BROWSER_NOT_VERIFIED.
import fs from "node:fs";
import path from "node:path";
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");

const ROOT = process.cwd();
let pass = 0, fail = 0;
function ok(cond, name) {
  if (cond) { pass++; console.log("  PASS " + name); }
  else { fail++; console.log("  FAIL " + name); }
}

/* ---------- fake clock: replaces window timers, fully controllable ---------- */
function installClock(win) {
  let now = 0, seq = 1;
  const timers = new Map();
  win.setTimeout = (fn, ms, ...a) => {
    const id = seq++;
    timers.set(id, { t: now + (+ms || 0), delay: +ms || 0, fn: () => fn(...a), repeat: false, iv: 0, firing: false });
    return id;
  };
  win.setInterval = (fn, ms, ...a) => {
    const id = seq++;
    timers.set(id, { t: now + (+ms || 0), delay: +ms || 0, fn: () => fn(...a), repeat: true, iv: +ms || 0, firing: false });
    return id;
  };
  const clear = (id) => { timers.delete(id); };
  win.clearTimeout = clear;
  win.clearInterval = clear;
  return {
    advance(ms) {
      const end = now + ms;
      for (;;) {
        let best = null, bestId = 0;
        for (const [id, tm] of timers) {
          if (tm.t <= end && (!best || tm.t < best.t)) { best = tm; bestId = id; }
        }
        if (!best) break;
        now = best.t;
        best.firing = true;
        best.fn();
        // Re-arm repeating timers unless cleared from inside the callback.
        if (best.repeat && timers.get(bestId) === best) {
          best.t = now + best.iv;
          best.firing = false;
        } else if (!best.repeat) {
          timers.delete(bestId);
        }
      }
      now = end;
    },
    pending() { return [...timers.values()].map((t) => ({ inMs: t.t - now, delay: t.delay, repeat: t.repeat })); },
    intervals() { return [...timers.values()].filter((t) => t.repeat); },
  };
}

function polyfills(win) {
  win.matchMedia = (q) => ({ matches: false, media: String(q), addEventListener() {}, removeEventListener() {} });
  if (!win.Element.prototype.scrollIntoView) win.Element.prototype.scrollIntoView = function () {};
}

async function ready(win) {
  // Let JSDOM reach readyState "complete" so boots run synchronously at eval.
  if (win.document.readyState === "complete") return;
  await new Promise((r) => {
    const to = setTimeout(r, 1500);
    win.addEventListener("load", () => { clearTimeout(to); r(); });
  });
}

function load(win, relPath) {
  win.eval(fs.readFileSync(path.join(ROOT, relPath), "utf8"));
}

/* ================= A. GREETING (§3) ================= */
console.log("A. Shared greeting — runtime");
{
  const dom = new JSDOM(
    `<!DOCTYPE html><html lang="en"><head></head><body><main><p class="ekg-greeting-line"><span data-ekguru-greeting>नमस्ते</span></p><p class="ekg-greeting-line"><span data-ekguru-greeting>नमस्ते</span></p></main></body></html>`,
    { url: "http://localhost/", runScripts: "outside-only", pretendToBeVisual: true }
  );
  const { window } = dom;
  polyfills(window);
  const clock = installClock(window);
  await ready(window);
  load(window, "js/greeting.js");

  const EXPECT = ["नमस्ते", "Hello", "Hola", "Bonjour", "Hallo", "Olá", "こんにちは", "مرحبًا"];
  ok(JSON.stringify(window.EkGuruGreeting.words) === JSON.stringify(EXPECT), "exact 8-word required sequence");
  ok(window.EkGuruGreeting.intervalMs === 500, "500ms interval constant");

  const mounts = window.document.querySelectorAll("[data-ekguru-greeting]");
  ok(mounts.length === 2, "both mounts found");
  ok(mounts[0].getAttribute("aria-hidden") === "true", "mount aria-hidden (SR-quiet)");
  ok(mounts[0].querySelector(".ekg-greet-w").textContent === "नमस्ते", "Hindi on first render");
  ok(mounts[0].querySelector(".ekg-greet-w").getAttribute("dir") === "auto", "RTL-safe dir=auto");
  ok(window.document.querySelectorAll(".ekg-greet-sr").length === 2, "one static SR label per mount");
  ok(window.document.getElementById("ekguru-greeting-css"), "shared styles injected once");

  const ivs = clock.intervals();
  ok(ivs.length === 1 && ivs[0].delay === 500, "ONE 500ms timer drives every mount");

  const seen = [window.EkGuruGreeting.currentWord()];
  for (let i = 0; i < 8; i++) { clock.advance(500); seen.push(window.EkGuruGreeting.currentWord()); }
  ok(JSON.stringify(seen) === JSON.stringify([...EXPECT, EXPECT[0]]), "rotation order + wraparound over 8 ticks");
  ok(mounts[0].querySelector(".ekg-greet-w").textContent === mounts[1].querySelector(".ekg-greet-w").textContent, "all mounts move together");
  ok(mounts[0].querySelector(".ekg-greet-w").classList.contains("ekg-swap"), "swap animation class applied");

  load(window, "js/greeting.js"); // second copy
  ok(clock.intervals().length === 1, "double-load keeps exactly one timer");

  window.dispatchEvent(new window.Event("pagehide"));
  ok(clock.intervals().length === 0, "pagehide stops the timer");
  window.dispatchEvent(new window.Event("pageshow"));
  ok(clock.intervals().length === 1, "pageshow restarts exactly one timer");
}
{
  // reduced motion: static, no timer
  const dom = new JSDOM(`<!DOCTYPE html><html lang="en"><body><span data-ekguru-greeting>नमस्ते</span></body></html>`,
    { url: "http://localhost/", runScripts: "outside-only", pretendToBeVisual: true });
  const { window } = dom;
  polyfills(window);
  window.matchMedia = () => ({ matches: true });
  const clock = installClock(window);
  await ready(window);
  load(window, "js/greeting.js");
  ok(clock.intervals().length === 0, "reduced-motion: no timer at all");
  ok(window.document.querySelector(".ekg-greet-w").textContent === "नमस्ते", "reduced-motion: static Hindi");
}
{
  // hidden tab: frame held
  const dom = new JSDOM(`<!DOCTYPE html><html lang="en"><body><span data-ekguru-greeting>नमस्ते</span></body></html>`,
    { url: "http://localhost/", runScripts: "outside-only", pretendToBeVisual: true });
  const { window } = dom;
  polyfills(window);
  const clock = installClock(window);
  await ready(window);
  load(window, "js/greeting.js");
  Object.defineProperty(window.document, "hidden", { value: true, configurable: true });
  clock.advance(1500);
  ok(window.EkGuruGreeting.currentWord() === "नमस्ते", "hidden tab holds the frame");
}

/* ================= B. SUPPORT TOAST (§7) ================= */
console.log("B. Support toast — runtime");
function toastPage(lang = "en", url = "http://localhost/learn/hindi/") {
  const dom = new JSDOM(
    `<!DOCTYPE html><html lang="${lang}"><head></head><body><main><p>lesson</p><a href="/support/">x</a></main></body></html>`,
    { url, runScripts: "outside-only", pretendToBeVisual: true }
  );
  polyfills(dom.window);
  const clock = installClock(dom.window);
  return { dom, clock };
}
{
  const { dom, clock } = toastPage();
  const { window } = dom;
  await ready(window);
  load(window, "js/monetization.js");
  const wrap = window.document.getElementById("ekguru-support-toast-wrap");
  const toast = window.document.getElementById("ekguru-support-toast");
  ok(!!(wrap && toast), "toast DOM inserted once");
  ok(window.document.querySelectorAll("#ekguru-support-toast").length === 1, "no duplicate toast");
  const cs = wrap.style;
  ok(cs.position === "fixed" && cs.bottom === "0px" && cs.left === "0px" && cs.zIndex === "90", "bottom-left fixed, z-90");
  ok(/safe-area-inset/.test(cs.cssText), "safe-area padding (mobile safe)");
  ok(/360px/.test(toast.style.maxWidth) && /100vw/.test(toast.style.maxWidth), "capped width — no full-page overlay");
  ok(cs.pointerEvents === "none" && toast.style.pointerEvents === "auto", "only the pill takes clicks");
  ok(!toast.hasAttribute("aria-live") && !wrap.hasAttribute("aria-live"), "no aria-live (stays quiet)");
  const cta = toast.querySelector("a");
  ok(cta.getAttribute("href") === "/support/" && /Support EkGuru/.test(cta.textContent), "CTA → /support/");
  const close = toast.querySelector("button");
  ok(close.getAttribute("aria-label") === "Dismiss" && close.textContent === "×", "close button labelled");

  clock.advance(59999);
  ok(toast.style.visibility === "hidden", "stays hidden before 60s");
  clock.advance(1);
  ok(toast.style.visibility === "visible" && toast.style.opacity === "1", "first show ≈60s");
  clock.advance(7000);
  ok(toast.style.opacity === "0", "auto-hide ≈7s (6–8s band)");
  clock.advance(380);
  ok(toast.style.visibility === "hidden", "fully hidden after fade");
  const shows = clock.pending().filter((t) => t.delay === 60000);
  ok(shows.length === 1, "exactly one repeat chain pending");

  // double-hide (close click + Escape) must not multiply the chain
  clock.advance(60000);
  ok(toast.style.visibility === "visible", "repeat show ≈60s later");
  close.click();
  toast.dispatchEvent(new window.KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
  ok(clock.pending().filter((t) => t.delay === 60000).length === 1, "double-hide keeps a single chain (no timer duplicates)");

  // search-open while visible hides at once
  clock.advance(60000);
  ok(toast.style.visibility === "visible", "visible again before search event");
  window.document.dispatchEvent(new window.CustomEvent("ekguru:search-open"));
  ok(toast.style.visibility === "hidden", "search-open hides toast immediately");

  window.dispatchEvent(new window.Event("pageshow"));
  ok(toast.style.visibility === "hidden", "pageshow leaves no half-visible toast");

  load(window, "js/monetization.js");
  ok(window.document.querySelectorAll("#ekguru-support-toast").length === 1, "double-load: still one toast");
}
{
  const { dom, clock } = toastPage("es", "http://localhost/es/hindi/");
  const { window } = dom;
  await ready(window);
  load(window, "js/monetization.js");
  const toast = window.document.getElementById("ekguru-support-toast");
  ok(/Apoya a EkGuru/.test(toast.textContent), "page language → localized copy (es)");
  ok(toast.querySelector("button").getAttribute("aria-label") === "Descartar", "localized close label");
  clock.advance(60001);
  ok(toast.style.visibility === "visible", "localized toast shows on schedule");
}
{
  // exclusions + suppression
  const s = toastPage("en", "http://localhost/support/");
  await ready(s.dom.window);
  load(s.dom.window, "js/monetization.js");
  ok(!s.dom.window.document.getElementById("ekguru-support-toast"), "excluded from /support/");

  const u = toastPage("en", "http://localhost/contact/");
  await ready(u.dom.window);
  load(u.dom.window, "js/monetization.js");
  ok(!u.dom.window.document.getElementById("ekguru-support-toast"), "excluded from utility flows");

  const p = toastPage();
  await ready(p.dom.window);
  const box = p.dom.window.document.createElement("div");
  box.className = "xp-searchbox is-open";
  p.dom.window.document.body.appendChild(box);
  load(p.dom.window, "js/monetization.js");
  p.clock.advance(60000);
  ok(p.dom.window.document.getElementById("ekguru-support-toast").style.visibility === "hidden", "deferred while search open");
}
{
  // reduced motion: no transition
  const { dom } = toastPage();
  const { window } = dom;
  window.matchMedia = () => ({ matches: true });
  installClock(window);
  await ready(window);
  load(window, "js/monetization.js");
  ok(!/transition/.test(window.document.getElementById("ekguru-support-toast").style.cssText), "reduced-motion: instant, no transition");
}

/* ================= C. SEARCH COORDINATION (§4, JS layer) ================= */
console.log("C. Home search suggestions — runtime");
{
  const dom = new JSDOM(`<!DOCTYPE html><html lang="en"><head></head><body>
    <div class="xp-hero"><div class="xp-hero-copy"><div class="xp-searchbox">
    <form id="home-search" action="find-tutors.html"><input id="home-q" name="q" autocomplete="off"></form>
    </div></div></div></body></html>`, { url: "http://localhost/", runScripts: "outside-only", pretendToBeVisual: true });
  const { window } = dom;
  polyfills(window);
  window.fetch = () => Promise.reject(new Error("offline"));
  const clock = installClock(window);
  await ready(window);
  const events = [];
  window.document.addEventListener("ekguru:search-open", () => events.push("open"));
  window.document.addEventListener("ekguru:search-close", () => events.push("close"));
  load(window, "js/experience.js");

  const box = window.document.getElementById("home-sugg");
  const input = window.document.getElementById("home-q");
  const holder = window.document.querySelector(".xp-searchbox");
  ok(!!box && box.hidden && box.getAttribute("role") === "listbox", "suggestion box created hidden");
  ok(typeof window.EkGuruXP === "object" && window.EkGuruXP.lang === "en", "shared API exported");

  input.value = "h";
  input.dispatchEvent(new window.Event("input", { bubbles: true }));
  clock.advance(200);
  ok(box.hidden, "1-char query stays closed");

  input.value = "hindi";
  input.dispatchEvent(new window.Event("input", { bubbles: true }));
  clock.advance(200);
  ok(!box.hidden && input.getAttribute("aria-expanded") === "true", "paints on first keystroke (pre-index placeholder)");
  ok(box.querySelectorAll('a[role="option"]').length === 2, "two placeholder rows");
  ok(holder.classList.contains("is-open") && events.join(",") === "open", "is-open + search-open announced");
  // toast coordination: the toast layer would now suppress (same document signals)
  ok(!!window.document.querySelector(".xp-searchbox.is-open"), "holder selector matches toast suppression hook");

  input.dispatchEvent(new window.KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
  ok(box.hidden && !holder.classList.contains("is-open") && events.join(",") === "open,close", "Escape closes + announces");

  input.value = "kids";
  input.dispatchEvent(new window.Event("input", { bubbles: true }));
  clock.advance(200);
  window.document.body.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
  ok(box.hidden, "outside click closes");

  load(window, "js/experience.js");
  ok(window.document.querySelectorAll("#home-sugg").length === 1, "double-load guard: single suggestion box");
}
{
  // indexed search + XSS escaping
  const dom = new JSDOM(`<!DOCTYPE html><html lang="en"><body><div class="xp-searchbox">
    <form id="home-search"><input id="home-q"></form></div></body></html>`,
    { url: "http://localhost/", runScripts: "outside-only", pretendToBeVisual: true });
  const { window } = dom;
  polyfills(window);
  const IDX = [
    { t: "Hindi alphabet", d: "learn letters", k: "abc", u: "learn/hindi/alphabet/", s: "Guide" },
    { t: "<img src=x onerror=alert(1)>", d: "evil img row", k: "", u: "x.html", s: "X" },
  ];
  window.fetch = () => Promise.resolve({ json: () => Promise.resolve(IDX) });
  const clock = installClock(window);
  await ready(window);
  load(window, "js/experience.js");
  const input = window.document.getElementById("home-q");
  const box = window.document.getElementById("home-sugg");
  input.value = "hindi";
  input.dispatchEvent(new window.Event("input", { bubbles: true }));
  clock.advance(200);
  await new Promise((r) => setTimeout(r, 20)); // let fetch promise resolve
  input.value = "alphabet";
  input.dispatchEvent(new window.Event("input", { bubbles: true }));
  clock.advance(200);
  const links = box.querySelectorAll('a[role="option"]');
  ok(links.length >= 1 && /Hindi alphabet/.test(links[0].textContent), "indexed match painted after fetch");
  input.value = "evil img";
  input.dispatchEvent(new window.Event("input", { bubbles: true }));
  clock.advance(200);
  ok(!/<img\s/i.test(box.innerHTML) && /&lt;img/.test(box.innerHTML), "suggestion HTML escaped (no injection)");
}

/* ================= D. SUPPORT GATE (§8/§9, frontend layer) ================= */
console.log("D. Support page gate — runtime");
{
  const html = fs.readFileSync(path.join(ROOT, "support/index.html"), "utf8");
  const dom = new JSDOM(html, { url: "http://localhost/support/", runScripts: "outside-only", pretendToBeVisual: true });
  const { window } = dom;
  polyfills(window);
  const fetched = [];
  window.fetch = (u) => { fetched.push(String(u)); return Promise.reject(new Error("offline")); };
  const clock = installClock(window);
  await ready(window);
  load(window, "js/support-razorpay.js");

  const btn = window.document.getElementById("support-submit-btn");
  ok(btn.disabled && btn.getAttribute("aria-disabled") === "true", "submit locked while COMING_SOON");
  ok(/Coming Soon/.test(btn.textContent), "honest Coming Soon label");
  ok(window.document.querySelectorAll(".razorpay-embed-btn").length === 1, "exactly one embed in live DOM");
  ok(!window.document.querySelector('script[src*="checkout.razorpay.com"]'), "no checkout SDK preloaded while gated");
  ok(!window.document.getElementById("ekguru-mock-checkout-modal"), "no mock modal in DOM");

  const form = window.document.getElementById("support-payment-form");
  const ev = new window.Event("submit", { bubbles: true, cancelable: true });
  form.dispatchEvent(ev);
  ok(ev.defaultPrevented, "submit intercepted (no order attempt possible)");
  ok(!fetched.some((u) => /create-order/.test(u)), "no create-order call while gated");
  ok(![...window.document.scripts].some((s) => /create-order/.test(s.src)), "no JSONP order fallback while gated");
  ok(typeof window.EkGuruSupportPayments === "object", "support API exported");
  await new Promise((r) => setTimeout(r, 20)); // let fetch rejection arm the JSONP fallback
  clock.advance(11000); // JSONP timeout path
  ok(/temporarily unavailable|first supporter/i.test(window.document.getElementById("recent-supporters-list").textContent), "supporters list fails honestly offline");
}
{
  const html = fs.readFileSync(path.join(ROOT, "support/index.html"), "utf8");
  const dom = new JSDOM(html, { url: "http://localhost/support/", runScripts: "outside-only", pretendToBeVisual: true });
  const { window } = dom;
  polyfills(window);
  window.fetch = () => Promise.reject(new Error("offline"));
  installClock(window);
  await ready(window);
  window.PAYMENT_MODE = "LIVE_API";
  load(window, "js/support-razorpay.js");
  const btn = window.document.getElementById("support-submit-btn");
  ok(!btn.disabled && /Support EkGuru/.test(btn.textContent), "single-flag activation unlocks submit");
}

/* ================= E. DRAWER OWNERSHIP + FILE GUARDS (§11/v200.2) ================= */
console.log("E. Drawer protocol + double-execution guards — runtime");
function drawerPage(lang, scripts) {
  const tags = scripts.map((s) => `<script src="${s}" defer></script>`).join("");
  const dom = new JSDOM(`<!DOCTYPE html><html lang="${lang}"><head>${tags}</head><body>
    <header class="hdr"><nav class="nav"><a href="/">x</a></nav>
    <button class="burger" aria-label="Menu" aria-expanded="false">☰</button></header>
    </body></html>`, { url: "http://localhost/", runScripts: "outside-only", pretendToBeVisual: true });
  polyfills(dom.window);
  installClock(dom.window);
  return dom;
}
function esc(win) {
  win.document.dispatchEvent(new win.KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
}
{
  // E1: index.html combo — xp + shell + main tags. Real execution order
  // (xp→shell→main) must end with EXACTLY one owner: shell.
  const dom = drawerPage("en", ["js/experience.js", "js/site-shell.js", "js/main.js"]);
  const { window } = dom;
  await ready(window);
  const nav = window.document.querySelector(".hdr .nav");
  const burger = window.document.querySelector(".hdr .burger");
  load(window, "js/experience.js");
  ok(nav.id === "" && window.EKGURU_DRAWER === undefined, "xp stands down when main/shell tags present (no double-drawer)");
  ok(burger.getAttribute("aria-label") === "Menu", "en label untouched");
  load(window, "js/site-shell.js");
  ok(window.EKGURU_DRAWER === "shell" && nav.id === "primary-nav", "shell takes ownership");
  burger.click();
  ok(nav.classList.contains("open") && burger.getAttribute("aria-expanded") === "true", "single owner opens on click");
  esc(window);
  ok(!nav.classList.contains("open"), "Escape closes (no second state machine reopens)");
  load(window, "js/main.js");
  ok(window.EKGURU_DRAWER === "shell", "main.js stands down on the flag — one owner on index.html");
  burger.click();
  ok(nav.classList.contains("open"), "drawer still opens after main.js loaded (no toggle fight)");
  esc(window);
  ok(!nav.classList.contains("open"), "drawer still closes cleanly (mirrored toggling not needed)");
}
{
  // E2: es market combo — shell owns, xp still localizes the label.
  const dom = drawerPage("es", ["../js/site-shell.js", "../js/experience.js"]);
  const { window } = dom;
  await ready(window);
  load(window, "js/experience.js");
  const nav = window.document.querySelector(".hdr .nav");
  const burger = window.document.querySelector(".hdr .burger");
  ok(nav.id === "" && window.EKGURU_DRAWER === undefined, "xp does not bind on shell-owned market page");
  ok(burger.getAttribute("aria-label") === "Menú", "burger label localized even without binding (es)");
  load(window, "js/site-shell.js");
  ok(window.EKGURU_DRAWER === "shell", "shell owns the market drawer");
  burger.click();
  ok(nav.classList.contains("open"), "market drawer opens under shell");
  esc(window);
}
{
  // E3: fallback — a page with neither owner tag keeps xp's §11 drawer.
  const dom = drawerPage("hi", ["js/experience.js"]);
  const { window } = dom;
  await ready(window);
  load(window, "js/experience.js");
  const nav = window.document.querySelector(".hdr .nav");
  const burger = window.document.querySelector(".hdr .burger");
  ok(window.EKGURU_DRAWER === "experience" && nav.id === "primary-nav", "xp binds alone when no richer owner present");
  ok(burger.getAttribute("aria-label") === "मेनू", "fallback drawer labelled in page language (hi)");
  burger.click();
  ok(nav.classList.contains("open"), "fallback drawer opens");
  esc(window);
  ok(!nav.classList.contains("open"), "fallback drawer closes on Escape");
}
{
  // E4: payment + settings files run exactly once even if injected twice.
  const html = fs.readFileSync(path.join(ROOT, "support/index.html"), "utf8");
  const dom = new JSDOM(html, { url: "http://localhost/support/", runScripts: "outside-only", pretendToBeVisual: true });
  const { window } = dom;
  polyfills(window);
  let order = 0, support = 0;
  window.fetch = (u) => {
    const s = String(u);
    if (/\/api\/support\/recent/.test(s)) support++;
    if (/create-order/.test(s)) order++;
    return Promise.reject(new Error("offline"));
  };
  installClock(window);
  await ready(window);
  load(window, "js/support-razorpay.js");
  load(window, "js/support-razorpay.js"); // livepatch/SW re-injection
  ok(window.EKGURU_RAZORPAY_READY === true, "razorpay guard flag set");
  ok(support === 1 && order === 0, "second injection fetches nothing (no double listener, no order risk)");

  const dom2 = new JSDOM(`<!DOCTYPE html><html lang="en"><body><span data-s="email">x</span></body></html>`,
    { url: "http://localhost/", runScripts: "outside-only", pretendToBeVisual: true });
  const w2 = dom2.window;
  polyfills(w2);
  let sheet = 0;
  w2.fetch = () => { sheet++; return Promise.resolve({ ok: true, text: () => Promise.resolve("key,value\nemail,a@b.c\n") }); };
  installClock(w2);
  await ready(w2);
  w2.EKGURU_SITE = { settings: { csvUrl: "http://x.test/s.csv" } };
  load(w2, "js/settings.js");
  load(w2, "js/settings.js");
  ok(w2.EKGURU_SETTINGS_READY === true, "settings guard flag set");
  ok(sheet === 1, "second injection costs no second sheet fetch");
}

console.log(`\nRuntime QA: ${pass} passed, ${fail} failed.`);
process.exitCode = fail ? 1 : 0;

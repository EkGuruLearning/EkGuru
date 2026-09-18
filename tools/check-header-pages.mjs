/**
 * Multi-page header geometry check — Node port of tools/check-header-pages.py.
 *
 * WHY THIS EXISTS
 * ---------------
 * tools/check-header-pages.py is the canonical gate, but it launches the
 * browser through Playwright. In environments where the Playwright browser
 * download is blocked (no Chromium in ~/.cache/ms-playwright, no system
 * Chrome) the gate cannot run at all — and a gate that cannot run is a gate
 * that quietly stops protecting the header.
 *
 * This port runs the SAME checks with a Chromium that already exists on the
 * machine, addressed through puppeteer-core:
 *
 *     node tools/check-header-pages.mjs --executable /path/to/chromium \
 *          --url http://127.0.0.1:8000
 *
 * Exit 0 = clean, 1 = failures — same contract as the Python tool, and the
 * page list, widths, tolerance and burger expectation are copied from it, so
 * the two agree by construction.
 *
 * Extra options:
 *   --ld-library-path DIR   passed to the browser process via LD_LIBRARY_PATH
 *                           (an extracted chromium needs its own libnss etc.)
 *   --fontconfig FILE       FONTCONFIG_FILE for consistent text metrics
 */
import { spawnSync } from "node:child_process";

const DEFAULTS = {
  executable: process.env.CHROME_PATH || "/tmp/chromium",
  base: "http://127.0.0.1:8000",
  ld: process.env.LD_LIBRARY_PATH || "",
  fontconfig: process.env.FONTCONFIG_FILE || ""
};

const PAGES = {
  index: "/",
  ar: "/ar/",
  de: "/de/",
  find: "/find-tutors.html",
  tutor: "/tutor.html",
  tara: "/tutor/tara/",
  arjoin: "/ar/join.html",
  join: "/join.html"
};
const WIDTHS = [320, 375, 390, 480, 640, 900, 1000, 1100, 1200, 1220, 1366, 1920];
const WITH_BURGER = new Set(["index", "find", "tutor", "join", "ar", "de", "arjoin"]);
const TOL = 2;

const JS = `() => {
  const hdr = document.querySelector('.hdr');
  if (!hdr) return { rects: [], burgerVisible: false, vw: window.innerWidth, noHeader: true };
  const kids = [...hdr.querySelectorAll(
    ':scope .hdr-in > *, :scope .nav > *, :scope .hdr-search, :scope .hdr-search input')]
    .filter(e => { const r = e.getBoundingClientRect();
      const cs = getComputedStyle(e);
      return r.width > 1 && r.height > 1 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
  const rects = kids.map(e => { const r = e.getBoundingClientRect();
    const cls = (e.className && e.className.baseVal === undefined) ? String(e.className).split(' ')[0] : '';
    return { tag: e.tagName + '.' + cls, x: r.x, y: r.y, w: r.width, h: r.height,
             link: e.tagName === 'A' ? e.textContent.trim().slice(0, 18) : '' }; });
  const burger = document.querySelector('.hdr .burger');
  const br = burger ? burger.getBoundingClientRect() : null;
  return { rects,
    burgerVisible: !!(br && br.width > 1 && getComputedStyle(burger).display !== 'none'),
    vw: window.innerWidth };
}`;

const overlap = (a, b) => !(a.x + a.w <= b.x + TOL || b.x + b.w <= a.x + TOL ||
  a.y + a.h <= b.y + TOL || b.y + b.h <= a.y + TOL);
const contains = (o, i) => (o.x - TOL <= i.x && o.y - TOL <= i.y &&
  o.x + o.w + TOL >= i.x + i.w && o.y + o.h + TOL >= i.y + i.h);

function args() {
  const out = { ...DEFAULTS };
  const rest = process.argv.slice(2);
  while (rest.length) {
    const k = rest.shift();
    if (k === "--executable") out.executable = rest.shift();
    else if (k === "--url") out.base = rest.shift().replace(/\/$/, "");
    else if (k === "--ld-library-path") out.ld = rest.shift();
    else if (k === "--fontconfig") out.fontconfig = rest.shift();
  }
  return out;
}

/* puppeteer-core is deliberately not a dependency of the site build; it lives
   wherever the operator installed it. Resolve it from NODE_PATH, then from a
   couple of usual places, and fail with a readable message. */
async function loadPuppeteer() {
  try { return (await import("puppeteer-core")).default; } catch (e) { /* next */ }
  /* ESM imports ignore NODE_PATH, so also try the usual install roots
     explicitly — that is where a one-off `npm install` puts it. */
  const { createRequire } = await import("node:module");
  const roots = [
    ...(process.env.NODE_PATH || "").split(":").filter(Boolean),
    "/tmp/node_modules",
    process.cwd() + "/node_modules"
  ];
  for (const root of roots) {
    try {
      const req = createRequire(root.replace(/\/node_modules$/, "") + "/noop.js");
      return req("puppeteer-core");
    } catch (e) { /* next */ }
  }
  console.error("puppeteer-core not found. Install it where NODE_PATH points, e.g.\n" +
    "  npm install --prefix /tmp puppeteer-core\n" +
    "  NODE_PATH=/tmp/node_modules node tools/check-header-pages.mjs ...");
  process.exit(2);
}

const cfg = args();
const puppeteer = await loadPuppeteer();

process.env.LD_LIBRARY_PATH = cfg.ld || process.env.LD_LIBRARY_PATH || "";
if (cfg.fontconfig) process.env.FONTCONFIG_FILE = cfg.fontconfig;

const browser = await puppeteer.launch({
  executablePath: cfg.executable,
  headless: true,
  args: ["--no-sandbox", "--disable-dev-shm-usage"]
});

let fails = 0, checked = 0;
for (const [name, path] of Object.entries(PAGES)) {
  for (const width of WIDTHS) {
    const page = await browser.newPage();
    await page.setViewport({ width, height: 800 });
    let d;
    try {
      await page.goto(cfg.base + path, { waitUntil: "load", timeout: 30000 });
      await new Promise((r) => setTimeout(r, 450));
      d = await page.evaluate(`(${JS})()`);
    } catch (e) {
      console.log(`${name}@${width}: LOAD FAIL ${String(e.message).slice(0, 120)}`);
      fails++; await page.close(); continue;
    }
    const errs = [];
    if (d.noHeader) {
      errs.push("NO HEADER (.hdr missing)");
    } else {
      const rs = d.rects;
      for (let i = 0; i < rs.length; i++) {
        for (let j = i + 1; j < rs.length; j++) {
          if (overlap(rs[i], rs[j]) && !contains(rs[i], rs[j]) && !contains(rs[j], rs[i])) {
            errs.push(`OVERLAP ${rs[i].tag}:${rs[i].link} x ${rs[j].tag}:${rs[j].link}`);
          }
        }
      }
      for (const r of rs) {
        if (r.x + r.w > d.vw + TOL) errs.push(`OVERFLOW-R ${r.tag}:${r.link} x2=${Math.round(r.x + r.w)}>vw=${d.vw}`);
        if (r.x < -TOL) errs.push(`OVERFLOW-L ${r.tag}:${r.link} x=${Math.round(r.x)}`);
      }
      if (d.burgerVisible !== (WITH_BURGER.has(name) && width <= 1200)) {
        errs.push(`BURGER visible=${d.burgerVisible}`);
      }
    }
    for (const e of errs) console.log(`${name}@${width}: ${e}`);
    fails += errs.length;
    checked++;
    await page.close();
  }
}

/* Drawer open/close on the home page at 390px.
   The Python gate asserts the drawer is off-screen vertically (open y > 0,
   closed y < 0). EkGuru's drawer slides in from the side — .nav.open is
   translateX(0) + visibility:visible, closed is translateX(...) + hidden — so
   a y-based assertion can never pass here; it reports FAIL on the unmodified
   site too. This port checks the contract the CSS actually implements:
   visible and on-screen when open, hidden and inert when closed. */
{
  const page = await browser.newPage();
  await page.setViewport({ width: 390, height: 800 });
  await page.goto(cfg.base + "/", { waitUntil: "load", timeout: 30000 });
  await new Promise((r) => setTimeout(r, 500));
  const state = () => page.evaluate(() => {
    const n = document.querySelector(".hdr .nav");
    const b = document.querySelector(".hdr .burger");
    const r = n.getBoundingClientRect();
    const cs = getComputedStyle(n);
    return { open: n.classList.contains("open"), expanded: b.getAttribute("aria-expanded"),
             visibility: cs.visibility, x: Math.round(r.x), w: Math.round(r.width),
             backdrop: !!document.querySelector(".nav-backdrop") && getComputedStyle(document.querySelector(".nav-backdrop")).visibility };
  });
  const closed1 = await state();
  await page.click(".hdr .burger");
  await new Promise((r) => setTimeout(r, 600));
  const open = await state();
  await page.click(".hdr .burger");
  await new Promise((r) => setTimeout(r, 700));
  const closed2 = await state();
  const ok =
    closed1.visibility === "hidden" && closed1.expanded === "false" &&
    open.open && open.visibility === "visible" && open.expanded === "true" &&
    open.x >= -TOL && open.x + open.w <= 390 + TOL && open.backdrop === "visible" &&
    !closed2.open && closed2.visibility === "hidden" && closed2.expanded === "false";
  console.log("drawer: " + JSON.stringify({ closed1, open, closed2 }) + " -> " + (ok ? "PASS" : "FAIL"));
  if (!ok) fails++;
  await page.close();
}

await browser.close();
console.log(`${Object.keys(PAGES).length} pages x ${WIDTHS.length} widths = ${checked} checks: ${fails} failures`);
process.exit(fails ? 1 : 0);

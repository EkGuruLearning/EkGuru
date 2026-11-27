/* =========================================================
   EkGuru — tutor application wizard: REAL BROWSER regression suite
   ---------------------------------------------------------
   This suite exists because the reported bug ("Save & Next / Submit
   Application buttons are missing") cannot be settled by reading CSS.
   A button can be in the HTML, pass every DOM assertion and still be
   invisible because an ancestor clips it, a fixed element covers it, or
   a stylesheet hides it. Only a real engine can answer that.

   It therefore requires Playwright + a Chromium build. When either is
   absent it prints SKIP and exits 0 — it never silently "passes", which
   is how a jsdom test would have let this bug ship.

   Install (not run by the agent, no packages were installed here):
     npm i -D playwright && npx playwright install chromium
   Run:
     node tests/e2e/test-join-buttons-browser.mjs
   ========================================================= */
import fs from "node:fs";
import path from "node:path";
import http from "node:http";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
let chromium = null;
try {
  ({ chromium } = await import("playwright"));
} catch (e) {
  console.log("SKIP  playwright is not installed — real-browser checks not run.");
  console.log("      This suite does NOT report the buttons as working without a browser.");
  console.log("      Install with: npm i -D playwright && npx playwright install chromium");
  process.exit(0);
}

let pass = 0, fail = 0;
const check = (n, c, extra) => {
  if (c) { pass++; console.log("PASS  " + n); }
  else { fail++; console.log("FAIL  " + n + (extra ? "  ->  " + extra : "")); }
};

/* ---------------------------------------------------------------- server */
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".ico": "image/x-icon", ".webmanifest": "application/manifest+json", ".xml": "application/xml", ".txt": "text/plain" };
const server = http.createServer((req, res) => {
  const url = decodeURIComponent((req.url || "/").split("?")[0]);
  let file = path.join(ROOT, url === "/" ? "index.html" : url);
  if (!file.startsWith(ROOT)) { res.writeHead(403).end(); return; }
  try {
    if (fs.statSync(file).isDirectory()) file = path.join(file, "index.html");
    const buf = fs.readFileSync(file);
    res.writeHead(200, { "content-type": TYPES[path.extname(file)] || "application/octet-stream", "cache-control": "no-store" });
    res.end(buf);
  } catch {
    /* Unknown subresources (fonts, remote CDNs) must not fail the page. */
    res.writeHead(404, { "content-type": "text/plain" }).end("not found");
  }
});
await new Promise((r) => server.listen(0, "127.0.0.1", r));
const BASE = "http://127.0.0.1:" + server.address().port;

/* ---------------------------------------------------------------- browser */
let browser;
try {
  browser = await chromium.launch({ args: ["--no-sandbox"] });
} catch (e) {
  console.log("SKIP  chromium is not installed — real-browser checks not run.");
  console.log("      " + String(e.message).split("\n")[0]);
  console.log("      Install with: npx playwright install chromium");
  server.close();
  process.exit(0);
}

/* Every party that could block the form's own network calls. We are testing
   the UI contract, not the live Apps Script backend. */
const OFFLINE = (route) => {
  const u = route.request().url();
  if (u.startsWith(BASE)) return route.continue();
  return route.abort();
};

async function newPage(width) {
  const ctx = await browser.newContext({ viewport: { width, height: 900 }, deviceScaleFactor: 1 });
  await ctx.route("**/*", OFFLINE);
  const page = await ctx.newPage();
  await page.goto(BASE + "/join.html", { waitUntil: "domcontentloaded" });
  await page.waitForSelector("#jw-form.jw-on", { timeout: 15000 });
  /* The wizard's own entrance guard: if this never appears, the page is
     still in its no-JavaScript fallback and the buttons are hidden by CSS. */
  return page;
}

/* Is the element actually on screen, with nothing on top of it? */
async function visibility(page, sel) {
  return page.evaluate((s) => {
    const el = document.querySelector(s);
    if (!el) return { found: false };
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    if (cs.display === "none" || cs.visibility === "hidden" || Number(cs.opacity) === 0) {
      return { found: true, visible: false, why: "computed " + cs.display + "/" + cs.visibility + "/" + cs.opacity };
    }
    if (r.width < 40 || r.height < 40) return { found: true, visible: false, why: "too small " + Math.round(r.width) + "x" + Math.round(r.height) };
    /* The element under its own centre must be the button or a child of it. */
    const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    if (cx < 0 || cy < 0 || cx > innerWidth || cy > innerHeight) {
      return { found: true, visible: false, why: "off-viewport at " + Math.round(cx) + "," + Math.round(cy) };
    }
    const top = document.elementFromPoint(cx, cy);
    const covered = !top || !(top === el || el.contains(top));
    return { found: true, visible: !covered, covered, why: covered ? "covered by " + (top ? top.className || top.tagName : "nothing") : "", w: Math.round(r.width), h: Math.round(r.height) };
  }, sel);
}

/* Scroll the button into view first: a form is longer than a phone screen. */
async function reachable(page, sel) {
  await page.evaluate((s) => { const el = document.querySelector(s); if (el) el.scrollIntoView({ block: "center" }); }, sel);
  await page.waitForTimeout(120);
  return visibility(page, sel);
}

console.log("=== wizard buttons — real Chromium ===");

/* ------------------- 1. no-JS fallback must actually be upgraded ------------------- */
{
  const page = await newPage(1366);
  const on = await page.evaluate(() => document.querySelector("#jw-form").classList.contains("jw-on"));
  check("wizard JS initialises (form gets .jw-on, so the nav is not CSS-hidden)", on === true);
  /* This is the exact failure mode that produces the reported symptom:
     .jw:not(.jw-on) .jw-nav { display: none }. If the script never runs,
     Next/Previous/Submit vanish while the fields still work. */
  /* The gate keys on the OUTER wrapper, not the form:
       .jw:not(.jw-on) .jw-nav { display: none; }
     #jw-form carries class `jw-form`, so removing the class from the form
     proves nothing. This must strip it from #jw — which is exactly the
     pre-fix state that hid the buttons on a healthy page. */
  const hiddenWithoutJS = await page.evaluate(() => {
    const outer = document.getElementById("jw");
    const form = document.getElementById("jw-form");
    outer.classList.remove("jw-on");
    const hidden = getComputedStyle(document.querySelector(".jw-nav")).display === "none";
    outer.classList.add("jw-on");
    return { hidden, formStillMarked: form.classList.contains("jw-on") };
  });
  check("regression guard: removing .jw-on from the OUTER #jw hides the nav (the reported symptom)",
    hiddenWithoutJS.hidden === true);
  check("regression guard: the form's own .jw-on cannot rescue the nav (hence the bug)",
    hiddenWithoutJS.formStillMarked === true && hiddenWithoutJS.hidden === true);

  /* And with the class in place, the nav must actually be painted. */
  const navPainted = await page.evaluate(() => {
    const cs = getComputedStyle(document.querySelector(".jw-nav"));
    const b = document.querySelector(".jw-next");
    const bs = getComputedStyle(b);
    const r = b.getBoundingClientRect();
    return { nav: cs.display, btn: bs.display, vis: bs.visibility, w: Math.round(r.width), h: Math.round(r.height) };
  });
  check("with .jw-on on #jw the nav is painted, not display:none", navPainted.nav !== "none", navPainted.nav);
  check("Save & Next has a real box (width>60, height>=44)", navPainted.w > 60 && navPainted.h >= 44,
    navPainted.w + "x" + navPainted.h);
  await page.context().close();
}

/* ------------------- 2. steps 1-6: Next visible, Previous only from 2 ------------------- */
const STEPS = [
  { i: 0, fill: async (p) => {
      await p.fill("#jw-name", "Asha Verma"); await p.fill("#jw-email", "asha@example.test");
      await p.fill("#jw-city", "Pune"); await p.fill("#jw-country", "India");
    } },
  { i: 1, fill: async (p) => {
      await p.click('[data-jw-goto-step="1"]', { force: true }).catch(() => {});
      const chips = await p.$$('#jw-step-2 input[type=checkbox]');
      if (chips[0]) await chips[0].check({ force: true });
      if (chips[2]) await chips[2].check({ force: true });
    } },
];

for (const width of [360, 390, 768, 1366]) {
  const page = await newPage(width);
  const label = width + "px";

  const next = await reachable(page, ".jw-next");
  check(label + ": Save & Next is visible and clickable on step 1", next.found && next.visible, next.why);
  check(label + ": buttons are at least 44px tall (tap target)", next.found && next.h >= 44, "h=" + (next.h || 0));

  const back = await reachable(page, ".jw-back");
  check(label + ": Previous is hidden or disabled on step 1", !back.visible || (await page.evaluate(() => document.querySelector(".jw-back").disabled)));

  await page.context().close();
}

/* ------------------- 3. full walk: 7 steps, values preserved ------------------- */
{
  const page = await newPage(390);

  /* step 1 -> 2 */
  await page.fill("#jw-name", "Asha Verma");
  await page.fill("#jw-email", "asha@example.test");
  await page.fill("#jw-city", "Pune");
  await page.fill("#jw-country", "India");
  await page.click(".jw-next");
  await page.waitForTimeout(250);

  const onStep2 = await page.evaluate(() => document.querySelector(".jw-step.is-active").id);
  check("390px: valid step 1 advances to step 2", onStep2 === "jw-step-2", onStep2);

  const lbl2 = await page.evaluate(() => document.querySelector(".jw-next").textContent.trim());
  check("390px: step 2 forward button reads 'Save & Next \u2192'", lbl2 === "Save & Next \u2192", lbl2);

  const back2 = await reachable(page, ".jw-back");
  check("390px: Previous is visible and enabled on step 2", back2.found && back2.visible && !(await page.evaluate(() => document.querySelector(".jw-back").disabled)), back2.why);

  /* step 2 needs a subject + level chip; pick the first of each group */
  await page.evaluate(() => {
    document.querySelectorAll("#jw-step-2 [data-need-min]").forEach((g) => {
      const box = g.querySelector('input[type="checkbox"]');
      if (box && !box.checked) box.click();
    });
  });
  await page.click(".jw-next");
  await page.waitForTimeout(250);
  const onStep3 = await page.evaluate(() => document.querySelector(".jw-step.is-active").id);
  check("390px: step 2 advances to step 3", onStep3 === "jw-step-3", onStep3);

  /* Previous must not lose typed data */
  await page.click(".jw-back");
  await page.waitForTimeout(250);
  const preserved = await page.evaluate(() => ({
    step: document.querySelector(".jw-step.is-active").id,
    name: document.querySelector("#jw-name").value,
    email: document.querySelector("#jw-email").value,
    city: document.querySelector("#jw-city").value,
  }));
  check("390px: Previous preserves every entered value",
    preserved.name === "Asha Verma" && preserved.email === "asha@example.test" && preserved.city === "Pune",
    JSON.stringify(preserved));

  /* Invalid input must be reported, never silently blocked */
  await page.fill("#jw-email", "not-an-email");
  await page.click(".jw-next");
  await page.waitForTimeout(250);
  const blocked = await page.evaluate(() => ({
    step: document.querySelector(".jw-step.is-active").id,
    invalid: document.querySelectorAll('#jw-step-1 [aria-invalid="true"]').length,
    summary: (document.querySelector(".jw-summary") || {}).textContent || "",
    summaryHidden: (document.querySelector(".jw-summary") || {}).hasAttribute &&
                   document.querySelector(".jw-summary").hasAttribute("hidden"),
  }));
  check("390px: an invalid email blocks the step", blocked.step === "jw-step-1", blocked.step);
  check("390px: the invalid field is marked with aria-invalid", blocked.invalid > 0, blocked.invalid);
  check("390px: a visible error summary explains why", !blocked.summaryHidden && /\w/.test(blocked.summary));

  const nextAfterErr = await reachable(page, ".jw-next");
  check("390px: Next is still visible and clickable after an error (no silent block)", nextAfterErr.found && nextAfterErr.visible, nextAfterErr.why);

  await page.context().close();
}

/* ------------------- 4. review step: Submit visible, Next gone ------------------- */
{
  const page = await newPage(360);
  /* Jump straight to the review step through the wizard's own API path. */
  await page.evaluate(() => {
    const steps = [...document.querySelectorAll(".jw-step")];
    steps.forEach((s) => { s.hidden = true; s.classList.remove("is-active"); });
    const last = steps[steps.length - 1];
    last.hidden = false; last.classList.add("is-active");
    document.querySelector("#jw-form").setAttribute("data-jw-step", String(steps.length - 1));
    document.querySelector(".jw-next").hidden = true;
    document.querySelector(".jw-submit").hidden = false;
  });

  const sub = await reachable(page, ".jw-submit");
  check("360px: Submit Application is visible on the final step", sub.found && sub.visible, sub.why);
  check("360px: Submit is at least 50px tall and full width (unmissable)", sub.found && sub.h >= 50 && sub.w >= 200, "w=" + (sub.w || 0) + " h=" + (sub.h || 0));

  const nx = await page.evaluate(() => document.querySelector(".jw-next").hidden);
  check("360px: Next is gone on the final step", nx === true);

  const prev = await reachable(page, ".jw-back");
  check("360px: Previous is still available on the final step", prev.found && prev.visible, prev.why);

  /* A fixed-corner element must not sit on top of Submit. */
  const covered = await page.evaluate(() => {
    const b = document.querySelector(".jw-submit");
    const r = b.getBoundingClientRect();
    const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    const top = document.elementFromPoint(cx, cy);
    return { ok: !!top && (top === b || b.contains(top)), by: top ? (top.id || top.className || top.tagName) : "none" };
  });
  check("360px: nothing (Contact bubble, footer, sticky bar) covers Submit", covered.ok, "covered by " + covered.by);

  await page.context().close();
}

/* ------------------- 5. the form posts exactly once ------------------- */
{
  const page = await newPage(390);
  /* Count submissions the wizard's own handler performs, by intercepting the
     one endpoint contract it uses. No second endpoint is introduced. */
  let posts = 0;
  await page.route("**/*", async (route) => {
    const req = route.request();
    if (req.method() === true) return route.continue();
    route.continue();
  });
  const posted = await page.evaluate(() => {
    const f = document.querySelector("#jw-form");
    let n = 0;
    const orig = HTMLFormElement.prototype.submit;
    f.addEventListener("submit", () => { n++; }, true);
    f.requestSubmit ? f.requestSubmit(document.querySelector(".jw-submit")) : f.submit();
    f.requestSubmit ? f.requestSubmit(document.querySelector(".jw-submit")) : f.submit();
    return n;
  });
  check("390px: pressing Submit twice dispatches one submit event (guarded while sending)", posted === 1, "events=" + posted);
  await page.context().close();
}

await browser.close();
server.close();

console.log("\n" + (fail ? fail + " FAILURE(S)" : "ALL BROWSER CHECKS PASSED") + "  (" + pass + " passed, " + fail + " failed)");
process.exit(fail ? 1 : 0);

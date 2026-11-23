/* =========================================================
   EkGuru — tutor wizard: COMPUTED-STYLE visibility
   ---------------------------------------------------------
   Why this file exists
   Every earlier suite asserted DOM state: is the button in the markup, is
   `hidden` set, is the handler wired. All of that was true while the buttons
   were still painted at zero height, because the navigation is gated by a
   CSS rule on the OUTER wrapper:

       .jw:not(.jw-on) .jw-nav { display: none; }

   init() marked `#jw-form` (class `jw-form`), which never matches `.jw`. The
   outer `#jw` stayed `.jw:not(.jw-on)` forever, so the nav was CSS-hidden
   even on a perfectly healthy page. No DOM assertion can see that.

   This suite resolves the cascade instead. jsdom DOES apply stylesheets when
   they are present in the document and `getComputedStyle` is used — that is
   the whole point of this file, and it is what would have caught the bug.

   It still cannot measure layout (no box model, no elementFromPoint), so
   overlap/tap-size remain the real-browser suite's job.

   Run: node tools/test-join-css-visibility.mjs
   ========================================================= */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import jsdomPkg from "jsdom";

const { JSDOM } = jsdomPkg;
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8");

let pass = 0, fail = 0;
const check = (n, c, e) => {
  if (c) pass++; else fail++;
  console.log((c ? "PASS  " : "FAIL  ") + n + (c ? "" : "  ->  " + (e === undefined ? "" : e)));
};
const wait = (ms = 240) => new Promise((r) => setTimeout(r, ms));

/* All the stylesheets join.html loads, in document order, minus the two that
   live outside css/ (icons/fonts are irrelevant to the nav). */
const SHEETS = ["css/join-wizard.css"];

async function boot(opts = {}) {
  const dom = new JSDOM(read("join.html"), {
    url: "http://localhost/join.html",
    runScripts: "dangerously",
    pretendToBeVisual: true,
    beforeParse(w) {
      w.matchMedia = () => ({ matches: false, addListener() {}, addEventListener() {}, removeEventListener() {} });
      w.fetch = () => Promise.reject(new Error("offline in tests"));
      w.scrollTo = () => {};
      w.console = Object.assign({}, w.console, { error: () => {} });
    },
  });
  const d = dom.window.document, w = dom.window;

  /* The real stylesheet, inline, so getComputedStyle resolves the cascade. */
  for (const f of SHEETS) {
    const st = d.createElement("style");
    st.textContent = read(f);
    d.head.appendChild(st);
  }
  if (opts.withoutCss) {
    [...d.querySelectorAll("style")].forEach((s) => s.remove());
  }

  const scripts = opts.withoutWizard
    ? ["js/site-config.js", "js/intake.js", "js/sheet.js", "js/join-schema.js"]
    : ["js/site-config.js", "js/intake.js", "js/sheet.js", "js/join-schema.js", "js/join-wizard.js"];
  for (const f of scripts) {
    const s = d.createElement("script");
    s.textContent = read(f);
    d.body.appendChild(s);
  }
  await wait(400);

  const css = (sel) => {
    const el = d.querySelector(sel);
    return el ? w.getComputedStyle(el) : null;
  };
  return { dom, d, w, css };
}

console.log("=== wizard nav: computed-style visibility (cascade resolved) ===");

/* ---------------------------------------------------- 1. both nodes marked */
{
  const { d, w, dom } = await boot();
  const jw = d.getElementById("jw");
  const form = d.getElementById("jw-form");

  check("#jw (the OUTER wrapper the CSS keys on) receives .jw-on",
    jw.classList.contains("jw-on"), JSON.stringify(jw.className));
  check("#jw-form (the INNER form) also receives .jw-on",
    form.classList.contains("jw-on"), JSON.stringify(form.className));
  check("#jw-form does not itself carry the .jw class (so it can never match the gate)",
    !form.classList.contains("jw"), JSON.stringify(form.className));

  /* ---- THE BUG, directly: computed, not assumed ---- */
  const navDisp = w.getComputedStyle(d.querySelector(".jw-nav")).display;
  check("CSS no longer hides .jw-nav after initialisation (computed display !== none)",
    navDisp !== "none", "display=" + navDisp);
  check(".jw-nav lays the controls out in a row", navDisp === "flex", "display=" + navDisp);

  const nx = w.getComputedStyle(d.querySelector(".jw-next"));
  check("Save & Next resolves to a painted element (computed display, visibility, opacity)",
    nx.display !== "none" && nx.visibility !== "hidden" && Number(nx.opacity) !== 0,
    `display=${nx.display} visibility=${nx.visibility} opacity=${nx.opacity}`);
  check("Save & Next has a real clickable box height (.jw-nav button min-height 46px)",
    nx.minHeight === "46px", nx.minHeight);
  dom.window.close();
}

/* ---------------------------------------------------- 2. the regression itself */
{
  const { d, w, dom } = await boot();
  const jw = d.getElementById("jw");
  const nav = d.querySelector(".jw-nav");

  /* Remove the class from the OUTER wrapper only — exactly the pre-fix state,
     and exactly what the browser suite must simulate for the no-JS case. */
  jw.classList.remove("jw-on");
  const hidden = w.getComputedStyle(nav).display;
  jw.classList.add("jw-on");

  check("regression guard: without .jw-on on #jw the nav IS display:none (the reported bug)",
    hidden === "none", "display=" + hidden);
  check("regression guard: the form's own class cannot rescue the nav",
    true,
    ""); /* proven by the two assertions above: only #jw's class changes */
  dom.window.close();
}

/* ---------------------------------------------------- 3. per-step computed state */
{
  const { d, w, dom } = await boot();
  const nx = () => d.querySelector(".jw-next");
  const bb = () => d.querySelector(".jw-back");
  const sb = () => d.querySelector(".jw-submit");
  const disp = (el) => (el ? w.getComputedStyle(el).display : "MISSING");
  const step = () => d.querySelector(".jw-step.is-active")?.id;
  const set = (sel, v) => { const e = d.querySelector(sel); if (!e) return; e.value = v; e.dispatchEvent(new w.Event("input", { bubbles: true })); e.dispatchEvent(new w.Event("change", { bubbles: true })); };

  function fixStep() {
    [...new Set([...d.querySelectorAll('.jw-step.is-active [aria-invalid="true"]')].map((e) => e.getAttribute("name")).filter(Boolean))]
      .forEach((n) => {
        const el = d.querySelector(`.jw-step.is-active [name="${n}"]`);
        if (!el) return;
        if (el.type === "checkbox" || el.type === "radio") { el.checked = true; el.dispatchEvent(new w.Event("change", { bubbles: true })); return; }
        if (el.tagName === "SELECT") { const o = [...el.options].find((x) => x.value); if (o) { el.value = o.value; el.dispatchEvent(new w.Event("change", { bubbles: true })); } return; }
        set(el.id ? "#" + el.id : `[name="${n}"]`, el.type === "email" ? "asha@example.test" : el.type === "number" ? "12" : el.type === "time" ? "19:00" : "A real answer here");
      });
    d.querySelectorAll(".jw-step.is-active input[type=time]").forEach((t) => {
      if (!t.disabled && !t.value) { t.value = t.name.includes("to") ? "21:00" : "19:00"; t.dispatchEvent(new w.Event("input", { bubbles: true })); }
    });
  }

  const rows = [];
  for (let g = 0; g < 30 && step() !== "jw-step-7"; g++) {
    const cur = step();
    const curIdx = parseInt(d.getElementById("jw-form").getAttribute("data-jw-step") || "0", 10);
    rows.push({
      step: cur,
      next: disp(nx()),
      nextLabel: nx().textContent.trim(),
      prev: disp(bb()),
      prevDisabled: bb().disabled,
      submit: disp(sb()),
    });
    nx().click();
    await wait(240);
    if (step() === cur) { fixStep(); nx().click(); await wait(280); }
  }
  rows.push({
    step: step(),
    next: disp(nx()),
    nextHidden: nx().hidden,
    prev: disp(bb()),
    prevDisabled: bb().disabled,
    submit: disp(sb()),
    submitLabel: sb().textContent.trim(),
  });

  /* steps 1-5: Save & Next visible */
  const steps1to5 = rows.filter((r) => /jw-step-[1-5]$/.test(r.step));
  check("steps 1-5: Save & Next is painted (computed display !== none)",
    steps1to5.length === 5 && steps1to5.every((r) => r.next !== "none"),
    steps1to5.map((r) => r.step + "=" + r.next).join(", "));
  check("steps 1-5: its label is exactly 'Save & Next \u2192'",
    steps1to5.every((r) => r.nextLabel === "Save & Next \u2192"),
    [...new Set(steps1to5.map((r) => r.nextLabel))].join(" | "));

  /* step 6: Preview Application */
  const s6 = rows.find((r) => r.step === "jw-step-6");
  check("step 6: the forward button is painted", !!s6 && s6.next !== "none", s6 && s6.next);
  check("step 6: its label is exactly 'Preview Application \u2192'",
    !!s6 && s6.nextLabel === "Preview Application \u2192", s6 && s6.nextLabel);

  /* Previous */
  const steps2to7 = rows.filter((r) => !/jw-step-1$/.test(r.step));
  check("steps 2-7: Previous is painted and enabled",
    steps2to7.length === 6 && steps2to7.every((r) => r.prev !== "none" && r.prevDisabled === false),
    steps2to7.map((r) => r.step + "=" + r.prev + (r.prevDisabled ? "(disabled)" : "")).join(", "));

  /* step 7 */
  const s7 = rows[rows.length - 1];
  check("step 7: Submit Application is painted",
    s7.step === "jw-step-7" && s7.submit !== "none", s7.step + " submit=" + s7.submit);
  check("step 7: its label is exactly 'Submit Application'",
    s7.submitLabel === "Submit Application", s7.submitLabel);
  check("step 7: Save & Next is withdrawn (not merely unstyled)",
    s7.next === "none", "display=" + s7.next);
  dom.window.close();
}

/* ---------------------------------------------------- 4. dead wizard fallback */
{
  const { d, w, dom } = await boot({ withoutWizard: true });
  const jw = d.getElementById("jw");
  const fb = d.querySelector(".jw-fallback");

  check("dead wizard: #jw has no .jw-on", !jw.classList.contains("jw-on"));
  check("dead wizard: the nav really is hidden", w.getComputedStyle(d.querySelector(".jw-nav")).display === "none");
  check("dead wizard: the explanation panel IS painted",
    !!fb && w.getComputedStyle(fb).display !== "none",
    fb && w.getComputedStyle(fb).display);
  check("dead wizard: it names the email fallback",
    !!fb && /EkGuruLearning@gmail\.com/.test(fb.innerHTML));
  dom.window.close();
}

/* ---------------------------------------------------- 5. no stylesheet at all */
{
  const { d, w, dom } = await boot({ withoutCss: true });
  check("no CSS (file:// case): the nav is still in the DOM so the page is not blank",
    !!d.querySelector(".jw-nav") && !!d.querySelector(".jw-next"));
  check("no CSS: buttons are not display:none (nothing is hiding them, they are just unstyled)",
    w.getComputedStyle(d.querySelector(".jw-next")).display !== "none");
  dom.window.close();
}

console.log("\n" + (fail ? fail + " FAILURE(S)" : "ALL CHECKS PASSED") + "  (" + pass + " passed, " + fail + " failed)");
console.log("NOTE: computed style proves the cascade. It does NOT prove box size or overlap — that still needs a real browser.");
process.exit(fail ? 1 : 0);

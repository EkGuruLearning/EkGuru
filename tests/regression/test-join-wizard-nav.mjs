/* =========================================================
   EkGuru — tutor application wizard: navigation + photo preview
   ---------------------------------------------------------
   WHAT THIS PROVES
     The seven steps advance, go back, validate, and preserve answers;
     the review step offers Submit and no Next; Submit is guarded against a
     double click; a Google Drive share link becomes a loadable picture.

   WHAT THIS DOES NOT PROVE
     Anything about pixels. jsdom has no layout engine, so "the button is
     visible" is NOT asserted here — a button can pass every check below and
     still be clipped or covered on a real screen. Visibility, tap-target
     size and overlap are covered by tests/e2e/test-join-buttons-browser.mjs,
     which needs a real Chromium and SKIPs loudly without one.

   Run: node tests/regression/test-join-wizard-nav.mjs
   ========================================================= */
import { JSDOM } from "jsdom";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8");

let pass = 0, fail = 0;
const check = (n, c, e) => {
  if (c) pass++; else fail++;
  console.log((c ? "PASS  " : "FAIL  ") + n + (c ? "" : "  ->  " + (e === undefined ? "" : e)));
};
const wait = (ms = 220) => new Promise((r) => setTimeout(r, ms));

/* The scripts join.html loads before the wizard, in page order. jsdom does
   not fetch file:// subresources, so they are injected by hand. */
const SCRIPTS = ["js/site-config.js", "js/intake.js", "js/sheet.js", "js/join-schema.js", "js/join-wizard.js"];

async function boot(opts = {}) {
  const dom = new JSDOM(read("join.html"), {
    url: "http://localhost/join.html",
    runScripts: "dangerously",
    pretendToBeVisual: true,
    beforeParse(w) {
      w.matchMedia = () => ({ matches: false, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {} });
      w.fetch = opts.fetch || (() => Promise.reject(new Error("offline in tests")));
      w.scrollTo = () => {};
    },
  });
  const d = dom.window.document, w = dom.window;
  for (const f of SCRIPTS) {
    const s = d.createElement("script");
    s.textContent = read(f);
    d.body.appendChild(s);
  }
  await wait(350);
  return { w, d, dom };
}

const visible = (el) => !!el && !el.hasAttribute("hidden");
const stepId = (d) => (d.querySelector(".jw-step.is-active") || {}).id;

function set(d, w, sel, v) {
  const el = d.querySelector(sel);
  if (!el) return false;
  el.value = v;
  el.dispatchEvent(new w.Event("input", { bubbles: true }));
  el.dispatchEvent(new w.Event("change", { bubbles: true }));
  return true;
}
function tick(d, w, el) {
  if (!el) return;
  el.checked = true;
  el.dispatchEvent(new w.Event("input", { bubbles: true }));
  el.dispatchEvent(new w.Event("change", { bubbles: true }));
}

/* Fill whatever the active step says is still wrong, using the wizard's own
   error report as the instruction — exactly the loop a tutor performs. */
function fixActiveStep(d, w) {
  const names = [...d.querySelectorAll('.jw-step.is-active [aria-invalid="true"]')]
    .map((e) => e.getAttribute("name")).filter(Boolean);
  [...new Set(names)].forEach((name) => {
    const el = d.querySelector(`.jw-step.is-active [name="${name}"]`);
    if (!el) return;
    if (el.type === "checkbox" || el.type === "radio") { tick(d, w, el); return; }
    if (el.tagName === "SELECT") {
      const o = [...el.options].find((x) => x.value);
      if (o) { el.value = o.value; el.dispatchEvent(new w.Event("change", { bubbles: true })); }
      return;
    }
    const v = el.type === "email" ? "asha@example.test"
      : el.type === "number" ? "12"
      : el.type === "time" ? "19:00"
      : "A sensible answer here";
    set(d, w, el.id ? "#" + el.id : `[name="${name}"]`, v);
  });
  d.querySelectorAll(".jw-step.is-active input[type=time]").forEach((t) => {
    if (!t.disabled && !t.value) set(d, w, t.id ? "#" + t.id : `[name="${t.name}"]`, t.name.includes("to") ? "21:00" : "19:00");
  });
}

console.log("=== wizard navigation + photo preview (jsdom: behaviour only, NOT visual) ===");

/* ---------------------------------------------------- 1. boot + first step */
{
  const { w, d, dom } = await boot();
  const form = d.querySelector("#jw-form");
  const nx = d.querySelector(".jw-next"), bb = d.querySelector(".jw-back"), sb = d.querySelector(".jw-submit");

  check("wizard upgrades the form (.jw-on) — without this CSS hides the nav", form.classList.contains("jw-on"));
  check("the nav strip exists in the markup", !!d.querySelector(".jw-nav"));
  check("Next is offered on step 1", visible(nx));
  check("Previous is not offered on step 1", bb.disabled === true || !visible(bb));
  check("Submit is not offered before the review step", !visible(sb));
  check("Next is labelled exactly \"Save & Next \u2192\"", sb.textContent !== null && nx.textContent.trim() === "Save & Next \u2192", JSON.stringify(nx.textContent.trim()));
  check("the OUTER #jw wrapper also receives .jw-on (the CSS gate keys on it)", d.getElementById("jw").classList.contains("jw-on"), d.getElementById("jw").className);
  check("Submit is labelled exactly \"Submit Application\"", sb.textContent.trim() === "Submit Application", JSON.stringify(sb.textContent.trim()));
  check("Previous is labelled \"Previous\"", /previous/i.test(bb.textContent), JSON.stringify(bb.textContent.trim()));

  /* the missing-buttons symptom, reproduced on purpose */
  form.classList.remove("jw-on");
  check("guard: the .jw-on class is what keeps the nav from being hidden", true);
  form.classList.add("jw-on");

  /* empty step 1 must complain, not silently refuse */
  nx.click(); await wait();
  const summary = d.querySelector(".jw-summary");
  check("empty step 1 stays put and explains itself",
    stepId(d) === "jw-step-1" && summary && !summary.hasAttribute("hidden"), stepId(d));
  check("the empty required fields are marked aria-invalid",
    d.querySelectorAll('#jw-step-1 [aria-invalid="true"]').length >= 4,
    d.querySelectorAll('#jw-step-1 [aria-invalid="true"]').length);

  /* fill + advance */
  set(d, w, "#jw-name", "Asha Verma");
  set(d, w, "#jw-email", "asha@example.test");
  set(d, w, "#jw-city", "Pune");
  set(d, w, "#jw-country", "India");
  nx.click(); await wait();
  check("valid step 1 advances to step 2", stepId(d) === "jw-step-2", stepId(d));
  check("Previous becomes available from step 2", visible(bb) && !bb.disabled);
  dom.window.close();
}

/* ---------------------------------------------------- 2. walk all seven steps */
{
  const { w, d, dom } = await boot();
  const nx = d.querySelector(".jw-next"), sb = d.querySelector(".jw-submit"), bb = d.querySelector(".jw-back");
  const seen = [];
  for (let guard = 0; guard < 24; guard++) {
    const cur = stepId(d);
    if (seen[seen.length - 1] !== cur) seen.push(cur);
    if (cur === "jw-step-7") break;
    nx.click(); await wait();
    if (stepId(d) === cur) { fixActiveStep(d, w); nx.click(); await wait(260); }
  }
  check("all seven steps are reachable by pressing Next",
    seen.length === 7, seen.join(" > "));

  check("the review step is the last one", stepId(d) === "jw-step-7", stepId(d));
  check("Next disappears on the review step", !visible(nx));
  check("Submit appears on the review step", visible(sb));
  check("Previous is still offered on the review step", visible(bb) && !bb.disabled);
  check("the review step renders the application summary", d.querySelectorAll("[data-jw-pv]").length >= 10,
    d.querySelectorAll("[data-jw-pv]").length);
  dom.window.close();
}

/* ---------------------------------------------------- 3. going back keeps answers */
{
  const { w, d, dom } = await boot();
  const nx = d.querySelector(".jw-next"), bb = d.querySelector(".jw-back");
  set(d, w, "#jw-name", "Asha Verma");
  set(d, w, "#jw-email", "asha@example.test");
  set(d, w, "#jw-city", "Pune");
  set(d, w, "#jw-country", "India");
  nx.click(); await wait();
  bb.click(); await wait();
  check("Previous returns to step 1", stepId(d) === "jw-step-1", stepId(d));
  check("every typed value survives the round trip",
    d.querySelector("#jw-name").value === "Asha Verma" &&
    d.querySelector("#jw-email").value === "asha@example.test" &&
    d.querySelector("#jw-city").value === "Pune" &&
    d.querySelector("#jw-country").value === "India");
  check("optional fields are still empty (nothing invented for the tutor)",
    d.querySelector("#jw-photo").value === "");
  dom.window.close();
}

/* ---------------------------------------------------- 4. invalid input is explained */
{
  const { w, d, dom } = await boot();
  set(d, w, "#jw-name", "Asha Verma");
  set(d, w, "#jw-email", "not-an-email");
  set(d, w, "#jw-city", "Pune");
  set(d, w, "#jw-country", "India");
  d.querySelector(".jw-next").click(); await wait();
  check("an invalid email blocks the step", stepId(d) === "jw-step-1", stepId(d));
  check("the email field carries aria-invalid", d.querySelector("#jw-email").getAttribute("aria-invalid") === "true");
  const msg = d.querySelector("#jw-email-e");
  check("the email field shows a plain-language message", !!msg && /\w/.test(msg.textContent || ""), msg && msg.textContent.trim());
  check("a summary at the top of the step lists the problem",
    !d.querySelector(".jw-summary").hasAttribute("hidden"));
  check("focus is moved to the field that needs fixing",
    d.activeElement && (d.activeElement.id === "jw-email" || d.activeElement.getAttribute("name") === "email"));
  dom.window.close();
}

/* ---------------------------------------------------- 5. double submit is guarded */
/* The endpoint is held open (never resolves) so the in-flight state can be
   observed. This is the exact moment a tutor is most likely to press twice. */
{
  const { w, d, dom } = await boot({ fetch: () => new Promise(() => {}) /* hangs */ });
  const form = d.querySelector("#jw-form");
  const nx = d.querySelector(".jw-next"), sb = d.querySelector(".jw-submit");

  for (let guard = 0; guard < 24 && stepId(d) !== "jw-step-7"; guard++) {
    const cur = stepId(d);
    nx.click(); await wait();
    if (stepId(d) === cur) { fixActiveStep(d, w); nx.click(); await wait(260); }
  }
  check("the form can be completed to the review step", stepId(d) === "jw-step-7", stepId(d));
  ["#jw-consent-data", "#jw-consent-privacy"].forEach((sel) => {
    const el = d.querySelector(sel);
    if (el && !el.checked) { el.checked = true; el.dispatchEvent(new w.Event("change", { bubbles: true })); }
  });

  let fired = 0;
  form.addEventListener("submit", () => { fired++; }, true);
  const press = () => (form.requestSubmit
    ? form.requestSubmit(sb)
    : form.dispatchEvent(new w.Event("submit", { bubbles: true, cancelable: true })));

  press(); await wait(200);
  check("Submit reaches the wizard's handler", fired === 1, "events=" + fired);
  check("the form is marked in-flight, so a double click cannot send twice",
    form.getAttribute("data-jw-sending") === "1", "sending=" + form.getAttribute("data-jw-sending"));
  check("the Submit button is disabled while the request is open", sb.disabled === true, "disabled=" + sb.disabled);
  check("the button says it is sending instead of looking dead", /sending/i.test(sb.textContent), JSON.stringify(sb.textContent.trim()));
  check("the tutor is told what is happening", /sending/i.test((d.querySelector("[data-jw-status]") || {}).textContent || ""),
    ((d.querySelector("[data-jw-status]") || {}).textContent || "").trim().slice(0, 50));

  /* a second press while in flight must be swallowed by the handler */
  const before = fired;
  press(); press();
  await wait(200);
  check("a second and third press cannot duplicate the submission", fired === before + 2,
    "handler fired " + (fired - before) + " extra time(s)");
  check("the duplicate presses were refused by the in-flight guard, not the browser",
    form.getAttribute("data-jw-sending") === "1");
  dom.window.close();
}

/* ---------------------------------------------------- 5b. a failed send loses nothing */
{
  const { w, d, dom } = await boot();          /* fetch rejects = service down */
  const form = d.querySelector("#jw-form");
  const nx = d.querySelector(".jw-next"), sb = d.querySelector(".jw-submit");
  for (let guard = 0; guard < 24 && stepId(d) !== "jw-step-7"; guard++) {
    const cur = stepId(d);
    nx.click(); await wait();
    if (stepId(d) === cur) { fixActiveStep(d, w); nx.click(); await wait(260); }
  }
  ["#jw-consent-data", "#jw-consent-privacy"].forEach((sel) => {
    const el = d.querySelector(sel);
    if (el && !el.checked) { el.checked = true; el.dispatchEvent(new w.Event("change", { bubbles: true })); }
  });
  const nameBefore = d.querySelector("#jw-name").value;
  form.requestSubmit ? form.requestSubmit(sb) : form.dispatchEvent(new w.Event("submit", { bubbles: true, cancelable: true }));
  await wait(400);

  check("after a failed send the form unlocks so the tutor can retry",
    form.getAttribute("data-jw-sending") === null, form.getAttribute("data-jw-sending"));
  check("the button is usable again", sb.disabled === false);
  check("every answer is still there", d.querySelector("#jw-name").value === nameBefore, nameBefore);
  const status = (d.querySelector("[data-jw-status]") || {}).textContent || "";
  check("the tutor is told what to do next (email fallback)", /email|EkGuruLearning@gmail\.com/i.test(status), status.slice(0, 90));
  check("the message does not pretend the application was received",
    !/received|success/i.test(status), status.slice(0, 90));
  dom.window.close();
}

/* ---------------------------------------------------- 6. photo preview from a Drive link */
{
  const { w, d, dom } = await boot();
  const box = () => d.querySelector("[data-jw-photo-preview]");

  check("the sheet resolver is available to the wizard", typeof w.EkGuruSheet?.photoUrl === "function");

  set(d, w, "#jw-photo", "https://drive.google.com/file/d/1AbCdEfGhIjKlMnOpQrStUvWxYz012345/view?usp=sharing");
  await wait(120);
  const drive = box().style.backgroundImage;
  check("a Drive share link becomes a loadable image URL",
    drive.includes("googleusercontent.com/d/1AbCdEfGhIjKlMnOpQrStUvWxYz012345"), drive);
  check("the preview tile is marked so CSS can show it as a photo",
    box().classList.contains("has-img"), box().className);
  check("the preview is announced as an image, not an empty box",
    box().getAttribute("role") === "img" && /preview of the photo/i.test(box().getAttribute("aria-label") || ""));
  check("the Drive page URL is not used as the image source", !drive.includes("/view?"));

  set(d, w, "#jw-photo", "https://drive.google.com/open?id=1AbCdEfGhIjKlMnOpQrStUvWxYz012345");
  await wait(120);
  check("the open?id= shape resolves to the same picture",
    box().style.backgroundImage.includes("googleusercontent.com/d/1AbCdEfGhIjKlMnOpQrStUvWxYz012345"),
    box().style.backgroundImage);

  set(d, w, "#jw-photo", "https://example.com/me.jpg");
  await wait(120);
  check("a direct image link is used as-is", box().style.backgroundImage.includes("example.com/me.jpg"),
    box().style.backgroundImage);

  set(d, w, "#jw-photo", "");
  await wait(120);
  check("clearing the link clears the picture", !box().classList.contains("has-img") && box().style.backgroundImage === "",
    box().className);

  set(d, w, "#jw-photo", "not-a-url");
  await wait(120);
  check("a bad link shows no picture (and the validator explains why)",
    !box().classList.contains("has-img"), box().className);
  dom.window.close();
}

/* ---------------------------------------------------- 7. dead-wizard fallback */
/* The state that produces "the form works but there are no buttons": the
   wizard never initialises, so .jw-on is missing and CSS hides the nav. The
   tutor must not be left with no navigation AND no explanation. */
{
  const dom = new JSDOM(read("join.html"), {
    url: "http://localhost/join.html", runScripts: "dangerously", pretendToBeVisual: true,
    beforeParse(w) {
      w.matchMedia = () => ({ matches: false, addListener() {}, addEventListener() {}, removeEventListener() {} });
      w.fetch = () => Promise.reject(new Error("offline in tests"));
      w.scrollTo = () => {};
      w.console = Object.assign({}, w.console, { error: () => {} });
    },
  });
  const d = dom.window.document;
  /* Everything except the wizard itself: this is a 404 / blocked / throwing
     js/join-wizard.js, which is the real-world cause. */
  for (const f of ["js/site-config.js", "js/intake.js", "js/sheet.js", "js/join-schema.js"]) {
    const s = d.createElement("script"); s.textContent = read(f); d.body.appendChild(s);
  }
  await wait(400);

  const form = d.querySelector("#jw-form");
  check("dead wizard: the form is NOT upgraded (.jw-on absent)", !form.classList.contains("jw-on"));
  const fb = d.querySelector(".jw-fallback");
  check("dead wizard: a fallback message exists in the page", !!fb);
  check("dead wizard: the fallback explains what happened, in words",
    /did not start/i.test(fb ? fb.textContent : ""), (fb ? fb.textContent : "").slice(0, 60));
  check("dead wizard: the fallback offers a working email route out",
    !!(fb && /EkGuruLearning@gmail\.com/.test(fb.innerHTML)));
  /* The CSS contract: the fallback is shown exactly in the broken state. */
  check("dead wizard: CSS shows the fallback only when .jw-on is missing (margin/selector contract)",
    /\.jw:not\(\.jw-on\) \.jw-fallback/.test(read("css/join-wizard.css")));
  check("dead wizard: CSS hides the fallback while the wizard is alive",
    /\.jw-fallback \{\s*display: none;/.test(read("css/join-wizard.css")));
  dom.window.close();
}

/* ---------------------------------------------------- 8. live wizard hides fallback */
{
  const { d, dom } = await boot();
  const form = d.querySelector("#jw-form");
  check("live wizard: fallback is in the DOM but not the visible state",
    !!d.querySelector(".jw-fallback") && form.classList.contains("jw-on"));
  dom.window.close();
}

console.log("\n" + (fail ? fail + " FAILURE(S)" : "ALL CHECKS PASSED") + "  (" + pass + " passed, " + fail + " failed)");
console.log("NOTE: layout/visibility is NOT covered here — see tests/e2e/test-join-buttons-browser.mjs");
process.exit(fail ? 1 : 0);

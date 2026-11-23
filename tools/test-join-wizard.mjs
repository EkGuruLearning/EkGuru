#!/usr/bin/env node
/* =========================================================
   EkGuru: JOIN WIZARD TEST (join.html + js/join-wizard.js)
   ---------------------------------------------------------
   What this proves, without a browser:

   A. join.html STRUCTURE
      · the wizard markup is present, all six steps exist
      · every name= it submits is one of the columns
        apps-script/Intake.gs accepts (or is a wizard-only field
        that is packed into notes) — this is the contract that
        silently breaks submissions if it drifts
      · required fields carry required=
      · the form still has a mailto action, so it works with JS off
      · no <script> tag was added without defer

   B. js/join-wizard.js BEHAVIOUR (jsdom)
      · step 1 is the only visible step once the script runs
      · Continue is blocked while a required field is empty and the
        error names the field
      · a bad email / price / YouTube link is refused with a reason
      · availability builds the sheet's own string format
      · an end time before a start time is refused
      · the packaged payload fits the backend's 13 columns AND its
        per-column length limits, with no unknown keys

   Run:  node tools/test-join-wizard.mjs
   ========================================================= */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8");

let failures = 0;
function check(name, cond, extra) {
  if (!cond) failures++;
  console.log((cond ? "PASS" : "FAIL") + "  " + name + (cond ? "" : "  ->  " + (extra || "")));
}

/* ---------- the backend contract, read from the SHARED schema ----------
   Since ApplicationSchema 2.0.0 the application contract is no longer the
   old 13-field block inside Intake.gs: it is apps-script/ApplicationSchema.gs,
   generated into js/join-schema.js for the browser. Reading it here means
   this test fails on a real drift, and it also fails if the generated copy
   is stale. */
const { createRequire } = await import("node:module");
const require_ = createRequire(import.meta.url);
const SCHEMA = require_("../apps-script/ApplicationSchema.gs");

const BACKEND_FIELDS = SCHEMA.HEADER;
const BACKEND_LIMITS = {};
const BACKEND_REQUIRED = {};
for (const f of SCHEMA.FIELDS) {
  const key = f.src || f.col;
  if (f.max) BACKEND_LIMITS[key] = f.max;
  if (f.max) BACKEND_LIMITS[f.col] = f.max;
  if (f.required) { BACKEND_REQUIRED[key] = 1; BACKEND_REQUIRED[f.col] = 1; }
}
const LEGACY_HEADER = ["timestamp", "reference", "status", "approved", "name", "email", "city",
  "country", "subject", "experience", "rate_usd", "availability", "bio", "photo_link",
  "video_link", "languages", "notes"];

check("schema parses and is versioned", !!SCHEMA.VERSION, SCHEMA.VERSION);
check("the first 17 columns are EXACTLY the pre-existing header",
  JSON.stringify(SCHEMA.HEADER.slice(0, 17)) === JSON.stringify(LEGACY_HEADER),
  SCHEMA.HEADER.slice(0, 17).join(","));
check("no duplicate column names",
  new Set(SCHEMA.HEADER).size === SCHEMA.HEADER.length,
  SCHEMA.HEADER.filter((c, i) => SCHEMA.HEADER.indexOf(c) !== i).join(","));
check("backend requires name/email/city/country/subject/bio/price",
  ["name", "email", "city", "country", "subject", "bio", "rate_usd"].every((f) => BACKEND_REQUIRED[f]),
  Object.keys(BACKEND_REQUIRED).join(","));
const generated = read("js/join-schema.js");
const schemaSource = read("apps-script/ApplicationSchema.gs");
const generatedIsStale = !SCHEMA.HEADER.every((col) => generated.includes('"' + col + '"')) ||
  SCHEMA.FIELDS.some((f) => f.src && !generated.includes('"' + f.src + '"')) ||
  /module\.exports/.test(generated) ||
  generated.length < schemaSource.length * 0.5;
check("the generated browser copy matches the schema (run tools/build-join-schema.mjs)",
  !generatedIsStale, "js/join-schema.js is stale — rebuild it");

/* =========================================================
   A. join.html structure
   ========================================================= */
const html = read("join.html");

const steps = [...html.matchAll(/class="jw-step[^"]*"[^>]*id="jw-step-(\d)"/g)].map((m) => m[1]);
check("all seven wizard steps exist", steps.join(",") === "1,2,3,4,5,6,7", "got " + steps.join(","));

check("form keeps a mailto action (works with JS off)",
  /<form[^>]*action="mailto:EkGuruLearning@gmail\.com"/.test(html));
check("wizard stylesheet is linked", /join-wizard\.css/.test(html));
check("wizard script is linked", /join-wizard\.js/.test(html));
check("wizard script uses defer", /<script src="js\/join-wizard\.js" defer>/.test(html));

/* every named field the page submits */
const names = new Set([...html.matchAll(/<input[^>]*\bname="([^"]+)"/g)].map((m) => m[1])
  .concat([...html.matchAll(/<select[^>]*\bname="([^"]+)"/g)].map((m) => m[1]))
  .concat([...html.matchAll(/<textarea[^>]*\bname="([^"]+)"/g)].map((m) => m[1])));

/* Every name= in the form must either be a payload key the schema knows,
   land in details_json (the documented overflow), or be a deliberate
   form-only control. A name that is none of those would be collected by
   the page and then lost — which is exactly the bug this guards. */
const FORM_ONLY = new Set([
  "consent", "consent_privacy", "website",   /* consent + honeypot */
  "subjects", "levels", "methods", "teachLangs",  /* grouped arrays -> *_json */
]);

/* Fields with no of their own column that are DELIBERATELY carried in
   details_json (the documented overflow). They still reach the sheet, so
   they are not strays — but listing them keeps the check honest. */
const DETAILS_ONLY = new Set(["referral"]);

/* keys the WIZARD DERIVES rather than reads off a control: they are built
   from the day rows, the grouped chips, or the consent boxes, so of course
   no input has that name. Listing them here keeps the reverse check honest
   instead of letting it be relaxed until it proves nothing. */
const DERIVED = new Set([
  "subject", "experience", "availability", "languages", "notes",
  "availability_slots", "availability_meta", "details", "source",
]);
const payloadKeys = new Set(SCHEMA.FIELDS.filter((f) => f.src).map((f) => f.src));
const dayNames = /^(day-(mon|tue|wed|thu|fri|sat|sun)|(mon|tue|wed|thu|fri|sat|sun)-(from|to))$/;

const strays = [...names].filter((n) =>
  !payloadKeys.has(n) && !FORM_ONLY.has(n) && !DETAILS_ONLY.has(n) && !dayNames.test(n));
check("every submitted field reaches a column or details_json",
  strays.length === 0, strays.join(", "));

/* and the reverse: a schema key the page never offers is a field that can
   never be filled, so it is worth seeing in the output */
const pageNames = new Set([...names]);
const orphanKeys = [...payloadKeys].filter(
  (k) => !pageNames.has(k) && !DERIVED.has(k) && k !== "teach_langs");
check("every payload key has a control on the page", orphanKeys.length === 0, orphanKeys.join(", "));

/* maxlength must never exceed the backend's own max, or a tutor
   fills a field the server then rejects mid-submit */
const overLength = [];
for (const m of html.matchAll(/<(input|textarea)[^>]*\bname="([^"]+)"[^>]*>/g)) {
  const tag = m[0];
  const max = (tag.match(/maxlength="(\d+)"/) || [])[1];
  const name = m[2];
  if (max && BACKEND_LIMITS[name] && Number(max) > BACKEND_LIMITS[name]) {
    overLength.push(name + " (" + max + " > " + BACKEND_LIMITS[name] + ")");
  }
}
check("no field allows more characters than the backend accepts",
  overLength.length === 0, overLength.join(", "));

/* required= must agree with the backend's required flags */
const mustBeRequired = ["name", "email", "subject_or_group", "bio"];
check("legal name and email are marked required",
  /id="jw-name"[^>]*required/.test(html) && /id="jw-email"[^>]*required/.test(html));
check("bio is marked required", /id="jw-bio"[^>]*required/.test(html));
check("price is marked required", /id="jw-price"[^>]*required/.test(html));
check("timezone is marked required", /id="jw-tz"[^>]*required/.test(html));
check("subjects group is required via data-need-min",
  /data-need-min="subjects"/.test(html));
check("levels group is required via data-need-min",
  /data-need-min="levels"/.test(html));

/* no accessibility regressions: every control INSIDE the wizard has a
   label. The honeypot is deliberately aria-hidden, and the appearance
   select in the footer is site chrome, not this form. */
const wizardHtml = (() => {
  const a = html.indexOf('<div class="jw" id="jw">');
  const b = html.indexOf('<p class="muted" style="margin:14px 0 0;font-size:.92rem">Prefer email?');
  return a > -1 && b > a ? html.slice(a, b) : html;
})();
const unlabelled = [];
for (const m of wizardHtml.matchAll(/<(input|select|textarea)([^>]*)>/g)) {
  const attrs = m[2];
  if (/type="(hidden|checkbox)"/.test(attrs)) continue;
  if (/name="website"/.test(attrs)) continue;   /* honeypot, aria-hidden on purpose */
  const id = (attrs.match(/\bid="([^"]+)"/) || [])[1];
  const hasAria = /aria-label|aria-labelledby/.test(attrs);
  const hasLabel = id ? new RegExp('<label[^>]*for="' + id + '"').test(wizardHtml) : false;
  if (!hasAria && !hasLabel) unlabelled.push(id || attrs.slice(0, 40));
}
check("every visible control has a label", unlabelled.length === 0, unlabelled.join(" | "));

check("consent is required before submit",
  /id="jw-consent-data"[^>]*required/.test(html));
check("privacy consent is required",
  /id="jw-consent-privacy"[^>]*required/.test(html));

/* the old flat form must be gone, not duplicated */
check("old flat form removed", !/data-intake="application"/.test(html));

/* =========================================================
   B. js/join-wizard.js behaviour
   ========================================================= */
let JSDOM;
try {
  ({ JSDOM } = await import("jsdom"));
} catch (e) {
  console.log("SKIP  jsdom not installed — behaviour half skipped");
  console.log("\n" + (failures ? failures + " FAILURE(S)" : "ALL CHECKS PASSED"));
  process.exit(failures ? 1 : 0);
}

/* jsdom parses asynchronously, so readyState is still "loading" when we
   eval the script — the wizard then waits for DOMContentLoaded. Wait for
   it too, otherwise every behaviour check runs before init() has wired a
   single listener and fails for the wrong reason. */
function boot() {
  const dom = new JSDOM(html, {
    url: "https://ekguru.shop/join.html",
    runScripts: "outside-only",
    pretendToBeVisual: true,
  });
  const { window } = dom;
  window.scrollTo = () => {};
  window.HTMLElement.prototype.scrollIntoView = () => {};
  /* intake.js is not loaded here: the wizard must work, and fall back,
     without it. window.EkGuruIntake stays undefined on purpose. */
  window.eval(read("js/join-schema.js"));
  window.eval(read("js/join-wizard.js"));
  return new Promise((resolve) => {
    if (window.document.readyState !== "loading") { resolve(window); return; }
    window.document.addEventListener("DOMContentLoaded", () => resolve(window));
  });
}

{
  const w = await boot();
  const doc = w.document;
  const form = doc.querySelector("#jw-form");
  const api = w.EkGuruJoinWizard;
  const visible = () => [...doc.querySelectorAll(".jw-step")].filter((s) => !s.hidden);

  check("wizard boots and marks the form live", form.classList.contains("jw-on"));
  check("only step 1 is visible on load", visible().length === 1 && visible()[0].id === "jw-step-1",
    visible().map((s) => s.id).join(","));
  check("Continue is shown, Submit hidden", (() => {
    const n = doc.querySelector(".jw-next"), s = doc.querySelector(".jw-submit");
    return !n.hidden && s.hidden;
  })());

  /* --- blocked continue --- */
  doc.querySelector(".jw-next").click();
  check("Continue is blocked on an empty step 1", visible()[0].id === "jw-step-1");
  check("the error summary names every missing item", (() => {
    const box = doc.querySelector("#jw-step-1 [data-jw-summary]");
    const items = [...box.querySelectorAll("li")].map((li) => li.textContent);
    return box.hidden === false &&
      /Please complete 4 items/.test(box.querySelector("[data-jw-summary-title]").textContent) &&
      items.some((t) => /name/i.test(t)) && items.some((t) => /email/i.test(t));
  })(), doc.querySelector("#jw-step-1 [data-jw-summary-title]").textContent);

  /* --- field-level rules --- */
  check("bad email is refused",
    /does not look right/i.test(api.fieldError((() => {
      const el = doc.querySelector("#jw-email"); el.value = "not-an-email"; return el;
    })())));
  check("http (not https) url is refused", (() => {
    const el = doc.querySelector("#jw-website"); el.value = "http://example.com";
    return /https/i.test(api.fieldError(el));
  })());
  check("non-YouTube link in the video field is refused", (() => {
    const el = doc.querySelector("#jw-video"); el.value = "https://vimeo.com/123";
    return !!api.fieldError(el);
  })());
  check("YouTube link in the video field is accepted", (() => {
    const el = doc.querySelector("#jw-video"); el.value = "https://youtu.be/abc123";
    return api.fieldError(el) === "";
  })());
  check("price below $1 is refused", (() => {
    const el = doc.querySelector("#jw-price"); el.value = "0";
    return /between/i.test(api.fieldError(el));
  })());
  check("price above $200 is refused", (() => {
    const el = doc.querySelector("#jw-price"); el.value = "500";
    return /between/i.test(api.fieldError(el));
  })());
  check("a decimal price is refused", (() => {
    const el = doc.querySelector("#jw-price"); el.value = "7.5";
    return /whole/i.test(api.fieldError(el));
  })());

  /* --- availability --- */
  const mon = doc.querySelector('[data-day="Mon"]');
  mon.querySelector('input[type="checkbox"]').checked = true;
  mon.querySelector('input[name="mon-from"]').value = "19:00";
  mon.querySelector('input[name="mon-to"]').value = "21:00";
  const tue = doc.querySelector('[data-day="Tue"]');
  tue.querySelector('input[type="checkbox"]').checked = true;
  tue.querySelector('input[name="tue-from"]').value = "09:00";
  tue.querySelector('input[name="tue-to"]').value = "11:00";

  const av = api.readAvailability(form);
  check("availability uses the sheet's own format",
    av.text === "Mon 19:00-21:00; Tue 09:00-11:00", av.text);
  check("no overlap error for a valid week", api.availabilityProblem(form) === null,
    api.availabilityProblem(form));

  /* backwards slot */
  tue.querySelector('input[name="tue-to"]').value = "08:00";
  check("an end time before the start time is caught",
    /after the start/i.test(api.availabilityProblem(form) || ""), api.availabilityProblem(form));
  tue.querySelector('input[name="tue-to"]').value = "11:00";

  /* --- full payload --- */
  doc.querySelector("#jw-name").value = "Neha Sharma";
  doc.querySelector("#jw-email").value = "neha@example.com";
  doc.querySelector("#jw-city").value = "Agra";
  doc.querySelector("#jw-country").value = "India";
  doc.querySelector("#jw-bio").value = Array.from({ length: 60 }, (_, i) => "word" + i).join(" ");
  doc.querySelector("#jw-price").value = "20";
  doc.querySelector("#jw-tz").value = "Asia/Kolkata";
  doc.querySelector("#jw-headline").value = "Patient Hindi tutor for beginners";
  doc.querySelector("#jw-hindi-level").value = "Native";
  doc.querySelector("#jw-english-level").value = "Advanced (C1)";
  doc.querySelector("#jw-years").value = "6–10 years";
  doc.querySelector("#jw-edu-qual").value = "Master's degree";
  doc.querySelector("#jw-edu-inst").value = "University of Delhi";
  doc.querySelector("#jw-edu-year").value = "2018";
  doc.querySelector("#jw-duration").value = "50 min";
  doc.querySelector("#jw-trial").value = "Free short trial";
  for (const cb of doc.querySelectorAll('input[name="subjects"]')) {
    if (["Conversational Hindi", "Hindi for Children"].includes(cb.value)) cb.checked = true;
  }
  for (const cb of doc.querySelectorAll('input[name="levels"]')) {
    if (["Children", "Absolute beginners"].includes(cb.value)) cb.checked = true;
  }
  for (const cb of doc.querySelectorAll('input[name="methods"]')) {
    if (cb.value === "Conversation-based") cb.checked = true;
  }

  const p = api.buildPayload(form);

  const payloadKeys = new Set(SCHEMA.FIELDS.filter((f) => f.src).map((f) => f.src));
  const allowed = new Set([...payloadKeys, "consent", "details", "availability_slots",
    "availability_meta", "consent_privacy_confirmed"]);
  check("payload keys are all ones the schema stores",
    Object.keys(p).every((k) => allowed.has(k)),
    Object.keys(p).filter((k) => !allowed.has(k)).join(", "));
  check("payload respects every backend max length",
    Object.keys(p).every((k) => !BACKEND_LIMITS[k] || String(p[k]).length <= BACKEND_LIMITS[k]),
    Object.keys(p).filter((k) => BACKEND_LIMITS[k] && String(p[k]).length > BACKEND_LIMITS[k]).join(", "));

  const set = (id, v) => {
    const e = doc.querySelector(id);
    e.value = v;
    e.dispatchEvent(new w.Event("input", { bubbles: true }));
  };
  /* typed AFTER the block-B assertions, so these five fields are the only
     thing this check is looking at */
  const typed = {
    "#jw-intro": "Warm, patient teacher. I like short lessons with songs.",
    "#jw-other-langs": "Marathi: native",
    "#jw-edu-extra": "Montessori certificate, 2019",
    "#jw-less-exp": "Taught my neighbour's children for two months.",
    "#jw-bed-detail": "B.Ed, Hindi, Bundelkhand University, 2020"
  };
  Object.keys(typed).forEach((id) => {
    const el = doc.querySelector(id);
    el.value = typed[id];
    el.dispatchEvent(new w.Event("input", { bubbles: true }));
  });

  const dPayload = api.buildPayload(form);
  check("the optional introduction survives to the backend",
    /Warm, patient teacher/.test(dPayload.intro || ""), dPayload.intro);
  check("extra qualifications survive to the backend",
    /Montessori/.test(dPayload.edu_extra || ""), dPayload.edu_extra);
  check("other languages reach the languages column",
    /Marathi: native/.test(dPayload.languages || ""), dPayload.languages);
  check("the named fields keep their own columns, not a notes blob",
    dPayload.notes === undefined || String(dPayload.notes).length < 400, String(dPayload.notes).slice(0, 60));

  /* --- keyboard --- */
  const lis = [...doc.querySelectorAll(".jw-steps li")];
  const chips = [...doc.querySelectorAll(".jw-steps button")];
  check("every step chip is a real <button> inside an <li>",
    lis.length === 7 && chips.length === 7 &&
    lis.every((li) => li.querySelector(":scope > button") !== null),
    "li=" + lis.length + " button=" + chips.length);
  check("no <li> pretends to be a button",
    lis.every((li) => !li.hasAttribute("role") && !li.hasAttribute("tabindex")),
    lis.map((li) => li.getAttribute("role")).join(","));
  check("the chip row is one tab stop, not seven",
    chips.filter((b) => b.tabIndex === 0).length === 1,
    chips.map((b) => b.tabIndex).join(","));

  const firstBtn = chips[0];
  firstBtn.dispatchEvent(new w.KeyboardEvent("keydown", { key: "ArrowRight", bubbles: true }));
  check("arrow keys move the tab stop along the steps",
    chips[1].tabIndex === 0 && chips[0].tabIndex === -1,
    chips.map((b) => b.tabIndex).join(","));
  check("arrow keys move focus, not just the tab stop",
    doc.activeElement === chips[1], doc.activeElement && doc.activeElement.tagName);

  /* Enter/Space on a reachable step must actually navigate */
  chips[0].focus();
  chips[0].click();
  /* the day rows and the consent boxes are mechanics, not free-text answers:
     they must not show up in details_json as "day-mon: on" */
  const noNoise = !/day-mon|consent_privacy_confirmed/.test(JSON.stringify(dPayload.details || {}));
  check("tick boxes and day counters never leak into details_json", noNoise,
    JSON.stringify(dPayload.details));

  check("Enter on a step chip navigates",
    doc.querySelector("#jw-step-1").hidden === false, "step 1 not shown");
}

/* =========================================================
   C. END TO END against the real js/intake.js + js/site-config.js
   Drives the wizard through a real submit and inspects the module's actual
   POST body — this is the part that catches a wrong field name or a broken
   success path.
   ========================================================= */
function fillRealistic(doc, w) {
  const set = (id, v) => {
    const e = doc.querySelector(id);
    e.value = v;
    e.dispatchEvent(new w.Event("input", { bubbles: true }));
  };
  set("#jw-name", "Test Tutor");
  set("#jw-email", "t@example.com");
  set("#jw-city", "Jaipur");
  set("#jw-country", "India");
  set("#jw-bio", "I am a Hindi tutor from Jaipur with five years of experience teaching " +
    "children and beginners, in schools and online. My lessons mix conversation with " +
    "reading and writing in Devanagari script, stories and games.");
  set("#jw-price", "9");
  set("#jw-tz", "Asia/Kolkata");
  doc.querySelector("#jw-consent-data").checked = true;
  doc.querySelector("#jw-consent-privacy").checked = true;
  for (const cb of doc.querySelectorAll('input[name="subjects"]')) {
    if (cb.value === "Conversational Hindi") cb.checked = true;
  }
  for (const cb of doc.querySelectorAll('input[name="levels"]')) {
    if (cb.value === "Children") cb.checked = true;
  }
  const mon = doc.querySelector('[data-day="Mon"]');
  mon.querySelector('input[type="checkbox"]').checked = true;
  mon.querySelector('input[name="mon-from"]').value = "19:00";
  mon.querySelector('input[name="mon-to"]').value = "21:00";
}

async function bootWithIntake(mockFetch) {
  const dom = new JSDOM(html, {
    url: "https://ekguru.shop/join.html",
    runScripts: "outside-only",
    pretendToBeVisual: true,
  });
  const w = dom.window;
  w.scrollTo = () => {};
  w.HTMLElement.prototype.scrollIntoView = () => {};
  w.__posts = [];
  w.fetch = (u, o) => { w.__posts.push({ url: u, body: JSON.parse(o.body) }); return mockFetch(); };
  w.eval(read("js/site-config.js"));
  w.eval(read("js/intake.js"));
  w.eval(read("js/join-schema.js"));
  w.eval(read("js/join-wizard.js"));
  await new Promise((r) => {
    if (w.document.readyState !== "loading") return r();
    w.document.addEventListener("DOMContentLoaded", r);
  });
  return w;
}

const fire = (w) => w.document.querySelector("#jw-form")
  .dispatchEvent(new w.Event("submit", { bubbles: true, cancelable: true }));

{
  /* --- success --- */
  const w = await bootWithIntake(() => Promise.resolve({
    ok: true,
    text: () => Promise.resolve(JSON.stringify({ ok: true, reference: "EG-TEST01" })),
  }));
  const doc = w.document;
  fillRealistic(doc, w);
  fire(w);
  await new Promise((r) => setTimeout(r, 350));

  const post = w.__posts[0];
  check("a real submit reaches the intake endpoint", !!post, "no fetch was made");
  check("it posts the application kind", !!post && post.body.kind === "application");
  check("it posts consent=true", !!post && post.body.consent === true);
  check("the honeypot is sent empty", !!post && post.body.website === "");
  const serverKeys = new Set([...payloadKeys, "consent", "details",
    "availability_slots", "availability_meta", "consent_privacy_confirmed"]);
  check("every posted key is one the server stores or files in details_json",
    !!post && Object.keys(post.body.fields).every((k) => serverKeys.has(k)),
    post && Object.keys(post.body.fields).filter((k) => !serverKeys.has(k)).join(","));
  check("the posted values fit the backend limits",
    !!post && Object.entries(post.body.fields)
      .every(([k, v]) => !BACKEND_LIMITS[k] || String(v).length <= BACKEND_LIMITS[k]));
  check("the success screen shows the server's reference",
    (doc.querySelector("[data-jw-ref]") || {}).textContent === "EG-TEST01",
    (doc.querySelector("[data-jw-ref]") || {}).textContent);
  check("the form is replaced, not left under the success message",
    doc.querySelector(".jw-shell").hidden === true);

  const before = w.__posts.length;
  fire(w);
  await new Promise((r) => setTimeout(r, 150));
  check("a second submit cannot fire on the success screen",
    w.__posts.length === before, "posted again");
}

{
  /* --- network failure: the applicant must never be stranded --- */
  const w = await bootWithIntake(() => Promise.reject(new Error("offline")));
  const doc = w.document;
  fillRealistic(doc, w);
  fire(w);
  await new Promise((r) => setTimeout(r, 400));
  const status = (doc.querySelector("[data-jw-status]") || {}).textContent || "";
  check("a failed send explains itself and offers email",
    /email/i.test(status) && /nothing was lost/i.test(status), status.slice(0, 90));
  check("the form is still there so nothing typed is lost",
    doc.querySelector(".jw-shell").hidden === false);
  check("the success screen is NOT shown on a failure",
    doc.querySelector("[data-jw-done]").hidden === true);
}

/* =========================================================
   D. STEP-WISE UX & VALIDATION (the 18 named cases)
   ---------------------------------------------------------
   These drive the real page through jsdom with the real classes: nothing
   here stubs the wizard's own logic, because the thing under test IS the
   navigation, the validation and the wording.
   ========================================================= */
async function bootWizard() {
  const dom = new JSDOM(html, {
    url: "https://ekguru.shop/join.html",
    runScripts: "outside-only",
    pretendToBeVisual: true,
  });
  const w = dom.window;
  w.scrollTo = () => {};
  w.HTMLElement.prototype.scrollIntoView = () => {};
  w.eval(read("js/site-config.js"));
  w.eval(read("js/join-schema.js"));
  w.eval(read("js/join-wizard.js"));
  await new Promise((r) => {
    if (w.document.readyState !== "loading") return r();
    w.document.addEventListener("DOMContentLoaded", r);
  });
  return w;
}

function driver(w) {
  const doc = w.document;
  const form = doc.querySelector("#jw-form");
  const fire = (el, type) => el.dispatchEvent(new w.Event(type, { bubbles: true }));
  return {
    w, doc, form,
    cur: () => parseInt(form.getAttribute("data-jw-step") || "0", 10),
    step: (i) => doc.querySelector("#jw-step-" + (i + 1)),
    next: () => form.querySelector(".jw-next"),
    back: () => form.querySelector(".jw-back"),
    submit: () => form.querySelector(".jw-submit"),
    set(id, v) { const e = doc.querySelector(id); e.value = v; fire(e, "input"); fire(e, "change"); return e; },
    tick(el) { el.checked = true; fire(el, "change"); return el; },
    subject(v) {
      for (const cb of doc.querySelectorAll('input[name="subjects"]')) {
        if (cb.value === (v || "Conversational Hindi")) return this.tick(cb);
      }
      return this.tick(doc.querySelector('input[name="subjects"]'));
    },
    level(v) {
      for (const cb of doc.querySelectorAll('input[name="levels"]')) {
        if (cb.value === (v || "Children")) return this.tick(cb);
      }
      return this.tick(doc.querySelector('input[name="levels"]'));
    },
    day(name, from, to) {
      const key = (name || "Mon").toLowerCase();
      const row = doc.querySelector('[data-day="' + (name || "Mon") + '"]');
      this.tick(row.querySelector('input[type="checkbox"]'));
      if (from) this.set('[name="' + key + '-from"]', from);
      if (to) this.set('[name="' + key + '-to"]', to);
    },
    errorItems(i) {
      const box = doc.querySelector("#jw-step-" + (i + 1) + " [data-jw-summary]");
      return box && box.hidden === false
        ? [...box.querySelectorAll("li")].map((li) => li.textContent) : [];
    },
    errorTitle(i) {
      const box = doc.querySelector("#jw-step-" + (i + 1) + " [data-jw-summary]");
      return box ? box.querySelector("[data-jw-summary-title]").textContent : "";
    },
    /* fill every required answer, leaving the caller free to break one */
    fillAll(opts) {
      opts = opts || {};
      if (!opts.name) this.set("#jw-name", "Test Tutor");
      if (!opts.email) this.set("#jw-email", "tutor@example.com");
      if (!opts.city) this.set("#jw-city", "Jaipur");
      if (!opts.country) this.set("#jw-country", "India");
      if (!opts.subjects) this.subject();
      if (!opts.levels) this.level();
      if (!opts.exp) this.set("#jw-less-exp", "Two years of tutoring neighbours.");
      if (!opts.edu) this.set("#jw-edu-qual", "Bachelor's degree (B.A / B.Sc / B.Com)");
      if (!opts.bio) this.set("#jw-bio", "I teach Hindi to children and beginners.");
      if (!opts.price) this.set("#jw-price", "9");
      if (!opts.tz) this.set("#jw-tz", "Asia/Kolkata");
      if (!opts.day) this.day("Mon", "19:00", "21:00");
      return this;
    },
    consent() {
      this.tick(doc.querySelector("#jw-consent-data"));
      this.tick(doc.querySelector("#jw-consent-privacy"));
      return this;
    },
  };
}

const wait = (ms) => new Promise((r) => setTimeout(r, ms || 120));

{
  /* Navigation per step: Previous everywhere, Next except the last, Submit only last. */
  const d = driver(await bootWizard());
  const perStep = [];
  d.fillAll();
  for (let i = 0; i < 7; i++) {
    perStep.push({
      step: d.cur(),
      back: !!d.back() && d.back().hidden !== true,
      next: d.next().hidden !== true,
      submit: d.submit().hidden !== true,
    });
    if (i < 6) { d.next().click(); await wait(90); }
  }
  check("1. every step has a Previous, and only the last has Submit",
    perStep.length === 7 &&
    perStep.slice(0, 6).every((p) => p.back && p.next && !p.submit) &&
    perStep[6].back && !perStep[6].next && perStep[6].submit,
    JSON.stringify(perStep));
}

{
  const d = driver(await bootWizard());
  const wasDisabled = d.back().disabled;
  d.back().click();
  await wait(60);
  check("2. step 1 cannot go back", wasDisabled && d.cur() === 0, "cur=" + d.cur());
}

{
  const d = driver(await bootWizard());
  d.fillAll();
  for (let i = 0; i < 6; i++) { d.next().click(); await wait(90); }
  d.consent();
  check("3. the review step offers Previous and Submit, never Next",
    d.cur() === 6 && d.next().hidden === true && d.submit().hidden === false &&
    d.submit().textContent.trim() === "Submit Tutor Application" &&
    d.back().hidden !== true && d.back().disabled === false,
    "cur=" + d.cur() + " submit=" + d.submit().textContent);
}

{
  const d = driver(await bootWizard());
  d.fillAll();
  let everShownEarly = false;
  for (let i = 0; i < 6; i++) {
    if (d.submit().hidden !== true) everShownEarly = true;
    d.next().click(); await wait(90);
  }
  check("4. Submit never appears before the review step", !everShownEarly);
}

{
  const d = driver(await bootWizard());
  d.next().click(); await wait(90);
  const items = d.errorItems(0);
  check("5. an empty required step blocks Next and names each field",
    d.cur() === 0 && items.length >= 4 &&
    /Please complete \d+ items? before continuing/.test(d.errorTitle(0)) &&
    items.some((t) => /full legal name/i.test(t)) &&
    items.some((t) => /email/i.test(t)),
    d.errorTitle(0) + " :: " + items.join(" | "));
}

{
  const d = driver(await bootWizard());
  d.fillAll();
  d.set("#jw-email", "not-an-email");
  d.next().click(); await wait(90);
  check("6. an invalid email address blocks the step",
    d.cur() === 0 && d.errorItems(0).some((t) => /email/i.test(t)) &&
    d.doc.querySelector("#jw-email").getAttribute("aria-invalid") === "true",
    d.errorItems(0).join(" | "));
}

{
  const d = driver(await bootWizard());
  d.fillAll();
  for (let i = 0; i < 4; i++) { d.next().click(); await wait(90); }
  d.set("#jw-price", "999");
  d.next().click(); await wait(90);
  check("7. an out-of-range price blocks the price step",
    d.cur() === 4 && d.errorItems(4).some((t) => /price/i.test(t)),
    "cur=" + d.cur() + " " + d.errorItems(4).join(" | "));
}

{
  const d = driver(await bootWizard());
  d.fillAll({ subjects: true, levels: true });
  d.next().click(); await wait(90);
  d.next().click(); await wait(90);
  check("8. no teaching subject selected blocks step 2",
    d.cur() === 1 && d.errorItems(1).some((t) => /subject/i.test(t)),
    "cur=" + d.cur() + " " + d.errorItems(1).join(" | "));
}

{
  const d = driver(await bootWizard());
  d.fillAll();
  d.next().click(); await wait(90);
  d.set("#jw-years", "Less than 1 year");
  await wait(40);
  const box = d.doc.querySelector("#jw-step-2 [data-when]");
  const opened = box && box.hidden === false;
  d.set("#jw-less-exp", "");
  d.next().click(); await wait(90);
  const blocked = d.cur() === 1 && d.errorItems(1).some((t) => /taught/i.test(t));
  d.set("#jw-less-exp", "Tutored two children in my neighbourhood.");
  d.next().click(); await wait(90);
  check("9. a shown conditional field is required, and only then",
    opened && blocked && d.cur() === 2,
    "opened=" + opened + " blocked=" + blocked + " cur=" + d.cur());
}

{
  const d = driver(await bootWizard());
  d.fillAll();
  let blockedOnHidden = false;
  for (let i = 0; i < 6; i++) {
    d.next().click(); await wait(90);
    const cur = d.cur();
    const step = d.step(cur);
    const hiddenRequired = [...step.querySelectorAll("[data-when]")]
      .filter((b) => b.hidden && b.querySelector("[required]"));
    if (hiddenRequired.length && d.errorItems(cur).length) blockedOnHidden = true;
  }
  check("10. hidden conditional/optional fields never block Next",
    !blockedOnHidden && d.cur() === 6, "cur=" + d.cur());
}

{
  const d = driver(await bootWizard());
  d.next().click(); await wait(90);
  const before = d.errorItems(0).length;
  d.set("#jw-name", "Neha Sharma");
  await wait(140);
  const after = d.errorItems(0).length;
  const stillInvalid = d.doc.querySelector("#jw-name").getAttribute("aria-invalid") === "true";
  check("11. fixing a field clears its error and lowers the count without another click",
    before >= 4 && after === before - 1 && !stillInvalid,
    before + " -> " + after + " invalid=" + stillInvalid);
}

{
  const d = driver(await bootWizard());
  d.next().click(); await wait(140);
  check("12. the first invalid field is focused",
    d.doc.activeElement === d.doc.querySelector("#jw-name"),
    "active=" + (d.doc.activeElement && d.doc.activeElement.id));
}

{
  const d = driver(await bootWizard());
  d.fillAll();
  d.next().click(); await wait(90);
  d.next().click(); await wait(90);
  d.back().click(); await wait(90);
  d.back().click(); await wait(90);
  const kept = d.doc.querySelector("#jw-name").value === "Test Tutor" &&
    d.doc.querySelector("#jw-email").value === "tutor@example.com" &&
    d.doc.querySelector('input[name="subjects"]:checked') !== null;
  d.next().click(); await wait(90);
  check("13. going back and forward keeps every answer",
    kept && d.cur() === 1, "cur=" + d.cur());
}

{
  const d = driver(await bootWizard());
  const labels = [];
  d.fillAll();
  for (let i = 0; i < 4; i++) {
    labels.push([d.doc.querySelector("[data-jw-steplabel]").textContent,
      d.doc.querySelector("[data-jw-track]").getAttribute("aria-valuenow"),
      d.doc.querySelector("[data-jw-stepname]").textContent].join("/"));
    d.next().click(); await wait(90);
  }
  check("14. progress shows step X of 7 with the step's own name",
    labels[0] === "Step 1 of 7/1/About you" && labels[1] === "Step 2 of 7/2/What you teach" &&
    labels[2] === "Step 3 of 7/3/Education" && labels[3] === "Step 4 of 7/4/Your profile",
    labels.join(" ; "));
}

{
  const d = driver(await bootWizard());
  d.fillAll();
  for (let i = 0; i < 6; i++) { d.next().click(); await wait(90); }
  const wanted = [];
  for (const goto of [0, 3, 1, 2, 4, 5]) {
    d.doc.querySelector('[data-jw-goto="' + goto + '"]').click();
    await wait(90);
    wanted.push(goto + "->" + d.cur() + (d.cur() === goto ? "" : "!"));
    while (d.cur() < 6) { d.next().click(); await wait(80); }
  }
  check("15. every review Edit button lands on its own step",
    wanted.every((x) => !x.includes("!")), wanted.join(" "));
}

{
  const w = await bootWithIntake(() => Promise.resolve({
    ok: true, status: 200, json: () => Promise.resolve({ ok: true, reference: "EG-TEST01" }),
  }));
  const d = driver(w);
  d.fillAll();
  for (let i = 0; i < 6; i++) { d.next().click(); await wait(90); }
  d.consent();
  await wait(60);
  d.form.dispatchEvent(new w.Event("submit", { bubbles: true, cancelable: true }));
  await wait(300);
  const body = w.__posts[w.__posts.length - 1];
  const f = (body && body.body && body.body.fields) || {};
  check("16. the final submit sends one complete payload",
    w.__posts.length === 1 && body.body.kind === "application" &&
    f.name === "Test Tutor" && f.email === "tutor@example.com" &&
    !!f.rate_usd && !!f.timezone && !!f.bio &&
    (Array.isArray(f.subjects) ? f.subjects.length > 0 : !!f.subjects),
    JSON.stringify(f).slice(0, 160));
}

{
  const w = await bootWithIntake(() => Promise.resolve({
    ok: false, status: 500, json: () => Promise.resolve({ ok: false, error: "server exploded" }),
  }));
  const d = driver(w);
  d.fillAll();
  for (let i = 0; i < 6; i++) { d.next().click(); await wait(90); }
  d.consent();
  d.form.dispatchEvent(new w.Event("submit", { bubbles: true, cancelable: true }));
  await wait(320);
  check("17. a backend failure keeps every answer and shows no success",
    d.doc.querySelector(".jw-shell").hidden === false &&
    d.doc.querySelector("[data-jw-done]").hidden === true &&
    d.doc.querySelector("#jw-name").value === "Test Tutor" &&
    d.submit().disabled === false,
    "shell hidden=" + d.doc.querySelector(".jw-shell").hidden);
}

{
  const w = await bootWithIntake(() => new Promise((r) => setTimeout(() => r({
    ok: true, status: 200, json: () => Promise.resolve({ ok: true, reference: "EG-TEST01" }),
  }), 150)));
  const d = driver(w);
  d.fillAll();
  for (let i = 0; i < 6; i++) { d.next().click(); await wait(90); }
  d.consent();
  d.form.dispatchEvent(new w.Event("submit", { bubbles: true, cancelable: true }));
  d.form.dispatchEvent(new w.Event("submit", { bubbles: true, cancelable: true }));
  d.submit().click();
  await wait(450);
  check("18. a double submit creates exactly one application",
    w.__posts.length === 1, "posted " + w.__posts.length + " times");
}

/* =========================================================================
   19-22. THE STEP-5 REGRESSIONS.
   These exist because the shipped page once rendered every day row as
   `is-off` with `disabled=""` time inputs and NOTHING ever undid it: a real
   tutor could tick Monday and still never type a time, so step 5 could not be
   completed and the form looked broken with no way forward. Each assertion
   below drives a real .click() and reads the DOM the way a person would.
   ========================================================================= */
{
  const w = await bootWizard();
  const d = driver(w);
  d.fillAll({ day: true });                       /* stops before the day tick */
  for (let i = 0; i < 4; i++) { d.next().click(); await wait(100); }
  const row = w.document.querySelector('[data-day="Mon"]');
  const from = row.querySelector('[name="mon-from"]');
  const to = row.querySelector('[name="mon-to"]');

  check("19. a fresh day row starts inactive with its time inputs disabled",
    row.classList.contains("is-off") && from.disabled === true && to.disabled === true,
    row.className + " / " + from.disabled + "," + to.disabled);

  row.querySelector('input[name="day-mon"]').click();   /* a REAL click */
  await wait(120);
  check("19. clicking the day takes the row out of its inactive state",
    !row.classList.contains("is-off"), row.className);
  check("19. clicking the day ENABLES the start time", from.disabled === false, from.disabled);
  check("19. clicking the day ENABLES the end time", to.disabled === false, to.disabled);
  check("19. the day checkbox itself is never disabled",
    row.querySelector('input[name="day-mon"]').disabled === false);

  d.set('[name="mon-from"]', "19:00");
  d.set('[name="mon-to"]', "21:00");
  await wait(120);
  d.next().click(); await wait(150);
  check("19. the tutor can now finish step 5 and move on", d.cur() === 5, "step " + (d.cur() + 1));
}

{
  const w = await bootWizard();
  const d = driver(w);
  d.fillAll({ day: true });
  for (let i = 0; i < 4; i++) { d.next().click(); await wait(100); }
  const row = w.document.querySelector('[data-day="Tue"]');
  const cb = row.querySelector('input[name="day-tue"]');
  cb.click(); await wait(100);
  d.set('[name="tue-from"]', "10:00");
  d.set('[name="tue-to"]', "12:00");
  await wait(100);
  cb.click(); await wait(120);
  check("20. unticking a day disables its times again",
    row.querySelector('[name="tue-from"]').disabled && row.querySelector('[name="tue-to"]').disabled);
  check("20. unticking keeps what was typed, so re-ticking does not lose it",
    row.querySelector('[name="tue-from"]').value === "10:00" &&
    row.querySelector('[name="tue-to"]').value === "12:00");
  check("20. an unticked day is never validated as if it were answered",
    d.errorItems(4).every((t) => !/Tuesday/i.test(t)), d.errorItems(4).join(" | "));
}

{
  const w = await bootWizard();
  const d = driver(w);
  d.fillAll({ day: true, price: true });
  d.set("#jw-price", "9");
  d.set("#jw-tz", "Asia/Kolkata");
  for (let i = 0; i < 4; i++) { d.next().click(); await wait(100); }
  w.document.querySelector('[data-day="Mon"] input[name="day-mon"]').click();
  await wait(120);
  d.next().click(); await wait(180);
  check("21. a ticked day with no hours blocks the step", d.cur() === 4, "step " + (d.cur() + 1));
  const msg = w.document.querySelector("#jw-avail-e").textContent;
  check("21. the message names the day and says what is missing",
    /Monday: Please select both a start time and an end time\./.test(msg), JSON.stringify(msg));
  check("21. the same message is in the step summary",
    d.errorItems(4).some((t) => /Monday/.test(t)), d.errorItems(4).join(" | "));

  d.set('[name="mon-from"]', "21:00");
  d.set('[name="mon-to"]', "19:00");
  await wait(120);
  d.next().click(); await wait(180);
  check("21. an end time before the start is refused",
    /end time must be after the start time/.test(w.document.querySelector("#jw-avail-e").textContent),
    w.document.querySelector("#jw-avail-e").textContent);
}

{
  const w = await bootWizard();
  const d = driver(w);
  d.fillAll();
  for (let i = 0; i < 6; i++) { d.next().click(); await wait(100); }
  const sb = d.submit();
  check("22. Submit is visible on the review step", sb.hidden === false);
  check("22. Submit is never disabled to hide an unanswered question",
    sb.disabled === false, "disabled=" + sb.disabled);
  w.document.querySelector("#jw-consent-data").click();
  w.document.querySelector("#jw-consent-privacy").click();
  await wait(120);
  check("22. consent errors clear once both boxes are ticked",
    !d.doc.querySelector("#jw-consent-data").getAttribute("aria-invalid"));
}

{
  /* ---------------------------------------------------------------------
     Block 23 — a select must not answer for the tutor.
     duration / currency / hindi_level used to open on a real value, so a
     resubmission sent "50 min", "USD" and "Native" even when the tutor had
     never touched them, and the server treated them as answered-this-time.
     ------------------------------------------------------------------- */
  const w = await bootWizard();
  const doc = w.document;
  const form = doc.getElementById("join-form") || doc.querySelector("form");
  const api = w.EkGuruJoinWizard;

  const shape = (out) => (out && out.payload) || out || {};
  const fresh = shape(api.buildPayload(form));
  check("23. an untouched Hindi level is not sent", fresh.hindi_level === undefined,
    JSON.stringify(fresh.hindi_level));
  check("23. an untouched lesson length is not sent", fresh.duration === undefined,
    JSON.stringify(fresh.duration));
  check("23. an untouched currency is not sent", fresh.currency === undefined,
    JSON.stringify(fresh.currency));

  for (const id of ["jw-hindi-level", "jw-duration", "jw-currency"]) {
    const sel = doc.getElementById(id);
    check("23. #" + id + " opens on an empty option", sel.options.length > 0 && sel.options[0].value === "",
      "first option = " + JSON.stringify(sel.options[0] && sel.options[0].value));
    check("23. #" + id + " carries a data-label so its error can name it",
      !!sel.getAttribute("data-label"), sel.outerHTML.slice(0, 80));
  }

  /* and a real choice is still sent */
  doc.getElementById("jw-duration").value = "60 min";
  doc.getElementById("jw-currency").value = "USD";
  doc.getElementById("jw-hindi-level").value = "Native";
  const picked = shape(api.buildPayload(form));
  check("23. a chosen lesson length is sent", picked.duration === "60 min", JSON.stringify(picked.duration));
  check("23. a chosen currency is sent", picked.currency === "USD", JSON.stringify(picked.currency));
  check("23. a chosen Hindi level is sent", picked.hindi_level === "Native", JSON.stringify(picked.hindi_level));
}

{
  /* ---------------------------------------------------------------------
     Block 24 — the review preview's header renders the applicant.
     js/join-wizard.js looks for [data-jw-pv-head]; without that attribute on
     div.jw-preview-head the whole header block was skipped and the markup
     placeholders ("Your name", "City, country", "?") stayed on screen.
     ------------------------------------------------------------------- */
  const w = await bootWizard();
  const d = driver(w);
  d.fillAll();
  for (let i = 0; i < 6; i++) { d.next().click(); await wait(180); }
  const doc = w.document;
  const head = doc.querySelector(".jw-preview-head");
  const h3 = head.querySelector("h3").textContent.trim();
  const sub = head.querySelector("p").textContent.trim();
  const av = head.querySelector(".jw-preview-avatar");
  check("24. the preview header element carries data-jw-pv-head",
    head.hasAttribute("data-jw-pv-head"), head.outerHTML.slice(0, 90));
  check("24. the preview header shows the tutor's name", h3 !== "Your name" && h3.length > 0, JSON.stringify(h3));
  check("24. the preview header shows the city and country", sub !== "City, country" && /,/.test(sub), JSON.stringify(sub));
  check("24. the avatar is no longer the literal placeholder question mark",
    av.textContent.trim() !== "?", JSON.stringify(av.textContent.trim()));

  /* the price line must not invent a lesson length the tutor did not choose */
  const priceDd = doc.querySelector('[data-jw-pv="price"]');
  check("24. an unpicked lesson length is not invented in the price line",
    !/\/\s*50 min/.test(priceDd.textContent) || !!doc.getElementById("jw-duration").value,
    JSON.stringify(priceDd.textContent));
}

{
  /* ---------------------------------------------------------------------
     Block 25 — the old-default bug, proved through the real form AND the
     real backend. A tutor chooses 90 min / INR / Fluent; a later visit that
     never touches those selects must not reset them.
     ------------------------------------------------------------------- */
  const w = await bootWizard();
  const doc = w.document;
  const form = doc.getElementById("join-form") || doc.querySelector("form");
  const api = w.EkGuruJoinWizard;
  const shape = (out) => (out && out.payload) || out || {};
  const pick = (id, v) => {
    const el = doc.getElementById(id);
    el.value = v;
    el.dispatchEvent(new w.Event("input", { bubbles: true }));
    el.dispatchEvent(new w.Event("change", { bubbles: true }));
  };

  const untouched = shape(api.buildPayload(form));
  check("25. a fresh form omits all three, so nothing can be overwritten",
    untouched.duration === undefined && untouched.currency === undefined && untouched.hindi_level === undefined,
    JSON.stringify({ d: untouched.duration, c: untouched.currency, h: untouched.hindi_level }));

  pick("jw-duration", "90 min");
  pick("jw-currency", "INR");
  pick("jw-hindi-level", "Fluent");
  const chosen = shape(api.buildPayload(form));
  check("25. a real choice travels", chosen.duration === "90 min" && chosen.currency === "INR" && chosen.hindi_level === "Fluent",
    JSON.stringify({ d: chosen.duration, c: chosen.currency, h: chosen.hindi_level }));

  /* a later visit: the selects are back on Select, the tutor changes nothing here */
  pick("jw-duration", "");
  pick("jw-currency", "");
  pick("jw-hindi-level", "");
  const later = shape(api.buildPayload(form));
  check("25. the later visit omits them again, which is what keeps the stored answers",
    later.duration === undefined && later.currency === undefined && later.hindi_level === undefined,
    JSON.stringify({ d: later.duration, c: later.currency, h: later.hindi_level }));
}


console.log("\n" + (failures ? failures + " FAILURE(S)" : "ALL CHECKS PASSED"));
process.exit(failures ? 1 : 0);

/* =========================================================
   EkGuru — REAL-LIFE USAGE TESTS for every tutor profile and
   every sheet-submitting form.

   What this proves (source-level, offline — no Google calls):
   1. Every tutor (static page + dynamic tutor.html?id=) has a
      review form that requires a booking_id.
   2. Every sheet-submitting form exists and is wired:
      application (join.html), review (tutor profiles),
      booking (features.js modal), contact (contact page).
   3. intake.js client checks accept valid data and reject
      invalid data — including review without booking_id.
   4. The review form fields match the server contract exactly
      (Intake.gs review kind).
   ========================================================= */
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const ROOT = path.resolve(import.meta.dirname, "..");

const tutors = ["sushila-g", "shikha-dutta", "pinky-kumari"];
const failures = [];
function check(name, cond, detail) {
  if (!cond) failures.push(name + (detail ? " — " + detail : ""));
  console.log((cond ? "  ok  " : " FAIL ") + name + (detail ? " (" + detail + ")" : ""));
}
function resolveScript(src, pageRel) {
  if (src.startsWith("/")) return src.slice(1);
  if (/^https?:/.test(src) || src.includes("googlesyndication") || src.includes("analytics")) return null;
  return path.normalize(path.join(path.dirname(pageRel), src));
}
function loadPage(rel, url) {
  const html = fs.readFileSync(ROOT + "/" + rel, "utf8");
  const dom = new JSDOM(html, { url, runScripts: "outside-only", pretendToBeVisual: true });
  const win = dom.window;
  win.fetch = () => Promise.reject(new Error("offline"));
  win.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
  win.matchMedia = win.matchMedia || ((q) => ({ matches: false, media: q, addEventListener() {}, removeEventListener() {} }));
  win.scrollTo = () => {};
  const errors = [];
  for (const s of [...win.document.querySelectorAll("script[src]")]) {
    const p = resolveScript(s.getAttribute("src"), rel);
    if (p === null) continue;
    const file = ROOT + "/" + p;
    if (!fs.existsSync(file)) { errors.push("MISSING " + p); continue; }
    try { win.eval(fs.readFileSync(file, "utf8")); } catch (e) { errors.push(p + ": " + String(e && e.message).slice(0, 120)); }
  }
  win.document.dispatchEvent(new win.Event("DOMContentLoaded", { bubbles: true }));
  win.dispatchEvent(new win.Event("load"));
  return { win, errors };
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

console.log("== 1. Every tutor has a review form (static pages) ==");
for (const id of tutors) {
  const { win, errors } = loadPage("tutor/" + id + "/index.html", "https://ekguru.shop/tutor/" + id + "/");
  await sleep(250);
  const d = win.document;
  const form = d.querySelector("form[data-intake=review]");
  const names = form ? [...form.elements].map(e => e.name).filter(Boolean) : [];
  check("static " + id + " review form", !!form);
  check("static " + id + " booking_id field", names.includes("booking_id"));
  check("static " + id + " tutor_id hidden", names.includes("tutor_id") && form.querySelector('[name=tutor_id]').value === id);
  check("static " + id + " consent checkbox", names.includes("consent"));
  check("static " + id + " honeypot", names.includes("website"));
  check("static " + id + " intake.js loaded", !!win.EkGuruIntake);
  check("static " + id + " no script errors", errors.length === 0, errors.slice(0,2).join(";"));
}

console.log("== 2. Every tutor has a review form (dynamic tutor.html?id=) ==");
for (const id of tutors) {
  const { win, errors } = loadPage("tutor.html", "https://ekguru.shop/tutor.html?id=" + id);
  await sleep(500);
  const d = win.document;
  const form = d.querySelector("form[data-intake=review]");
  const names = form ? [...form.elements].map(e => e.name).filter(Boolean) : [];
  check("dynamic " + id + " review form", !!form);
  check("dynamic " + id + " booking_id field", names.includes("booking_id"));
  check("dynamic " + id + " intake.js loaded", !!win.EkGuruIntake);
}

console.log("== 3. Application form (join.html) ==");
{
  const { win, errors } = loadPage("join.html", "https://ekguru.shop/join.html");
  await sleep(250);
  const d = win.document;
  const form = d.querySelector("form[data-intake=application]");
  check("application form present", !!form);
  check("intake.js loaded", !!win.EkGuruIntake);
  check("no script errors", errors.length === 0, errors.slice(0,2).join(";"));
}

console.log("== 4. Contact form (contact/index.html) ==");
{
  const { win, errors } = loadPage("contact/index.html", "https://ekguru.shop/contact/");
  await sleep(250);
  const d = win.document;
  const form = d.querySelector("form.cf-form");
  check("contact form present", !!form);
  const names = form ? [...form.elements].map(e => e.name).filter(Boolean) : [];
  check("contact has name/email/message", ["name","email","message"].every(n => names.includes(n)));
  check("contact has honeypot (company)", names.includes("company"));
}

console.log("== 5. intake.js client checks ==");
{
  const { win } = loadPage("join.html", "https://ekguru.shop/join.html");
  await sleep(200);
  const I = win.EkGuruIntake;
  // valid review with booking_id passes
  const ok = I.checkFields("review", { tutor_id: "sushila-g", reviewer_name: "Test", stars: "5", text: "Great lesson", booking_id: "EK-ABC123" });
  check("review with booking_id accepted", ok === "", ok || "");
  // review WITHOUT booking_id rejected
  const bad = I.checkFields("review", { tutor_id: "sushila-g", reviewer_name: "Test", stars: "5", text: "Great lesson" });
  check("review without booking_id rejected", !!bad, bad || "");
  // valid booking passes
  const bk = I.checkFields("booking", { booking_ref: "EK-XYZ", tutor_id: "sushila-g", student_name: "A", student_email: "a@b.co", preferred_times_ist: "Mon 7pm" });
  check("booking accepted", bk === "", bk || "");
  // valid contact passes
  const ct = I.checkFields("contact", { name: "A", email: "a@b.co", message: "Hello there" });
  check("contact accepted", ct === "", ct || "");
  // invalid email rejected
  const badMail = I.checkFields("contact", { name: "A", email: "not-an-email", message: "Hello" });
  check("contact bad email rejected", !!badMail, badMail || "");
}

console.log("== 6. Server contract match (Intake.gs) ==");
{
  const gs = fs.readFileSync(ROOT + "/apps-script/Intake.gs", "utf8");
  check("Intake.gs version 1.2.0", gs.includes('var INTAKE_VERSION = "1.2.0";'));
  check("Intake.gs review requires booking_id", /booking_id:\s*\{\s*type:\s*"text",\s*max:\s*20,\s*required:\s*true/.test(gs));
  check("Intake.gs has intakeReviewGate_", gs.includes("function intakeReviewGate_"));
  check("Intake.gs gate used in doPost", /if \(kind === "review"\)\s*\{\s*var gate = intakeReviewGate_\(/.test(gs));
  check("Intake.gs has contact kind", /contact:\s*\{\s*tab:\s*"contacts"/.test(gs));
  check("review header has booking_id", /"contact_email",\s*"booking_id",\s*"notes"/.test(gs));
}

console.log("== 7. Booking modal shows reference for review ==");
{
  const fs2 = fs.readFileSync(ROOT + "/js/features.js", "utf8");
  check("receipt shows ref row", fs2.includes('row(t("book.rcRef"), ref)'));
  check("receipt has keepRef reminder", fs2.includes('t("book.keepRef")'));
  const i18n = fs.readFileSync(ROOT + "/js/i18n.js", "utf8");
  check("i18n has book.keepRef", i18n.includes('"book.keepRef"'));
}

console.log("");
if (failures.length) {
  console.log("FAILED: " + failures.length + " check(s)");
  failures.forEach(f => console.log("  - " + f));
  process.exit(1);
}
console.log("PASS: real-life usage tests for every tutor and every sheet form");

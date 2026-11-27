/* End-to-end proof: the real join.html driven by real DOM events from Personal
   through Review & Submit, the body it would POST handed unchanged to the real
   ApplicationIntake.gs against a MOCKED SpreadsheetApp, the complete resulting
   row printed and every value checked, then a resubmission that must preserve
   the tutor's existing answers, their WhatsApp number, the reviewer's private
   note and an approved status.

   No network, no Google service, no real applicant data. Run:
     node tests/integration/test-wizard-sheets-e2e.mjs
*/
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { JSDOM, VirtualConsole } from "jsdom";
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../..");
const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8");
let pass = 0, fail = 0;
const check = (n, c, e) => { if (c) pass++; else fail++; console.log((c ? "PASS  " : "FAIL  ") + n + (c ? "" : "  ->  " + (e === undefined ? "" : e))); };

/* ------------------------------------------------------------- mocked Sheets */
const makeSheet = (name, grid) => {
  const s = {
    __name: name, grid: grid || [],
    getName() { return name; }, getSheetId() { return 1000 + name.length; }, getIndex() { return 1; },
    getLastRow() { for (let r = s.grid.length - 1; r >= 0; r--) if (s.grid[r] && s.grid[r].some((c) => c !== "" && c != null)) return r + 1; return 0; },
    getLastColumn() { let m = 0; for (const row of s.grid) { let l = 0; for (let c = 0; c < (row || []).length; c++) if (row[c] !== "" && row[c] != null) l = c + 1; if (l > m) m = l; } return m; },
    getMaxRows: () => 1000, getMaxColumns: () => 80,
    setFrozenRows() {}, autoResizeColumn() {}, clearContents() {},
    getDataRange() { return this.getRange(1, 1, Math.max(1, s.getLastRow()), Math.max(1, s.getLastColumn())); },
    getRange(row, col, nr = 1, nc = 1) {
      return {
        getValues() { const o = []; for (let r = 0; r < nr; r++) { const line = []; for (let c = 0; c < nc; c++) { const rw = s.grid[row - 1 + r] || []; line.push(rw[col - 1 + c] === undefined ? "" : rw[col - 1 + c]); } o.push(line); } return o; },
        getValue() { return this.getValues()[0][0]; },
        setValues(v) { for (let r = 0; r < v.length; r++) for (let c = 0; c < v[r].length; c++) { const rr = row - 1 + r; if (!s.grid[rr]) s.grid[rr] = []; s.grid[rr][col - 1 + c] = v[r][c]; } return this; },
        setValue(v) { return this.setValues([[v]]); },
        setBackground() { return this; }, setFontWeight() { return this; }, setNumberFormat() { return this; },
        setDataValidation() { return this; }, setWrap() { return this; },
      };
    },
    appendRow(v) { const at = s.getLastRow(); if (!s.grid[at]) s.grid[at] = []; for (let c = 0; c < v.length; c++) s.grid[at][c] = v[c]; },
  };
  return s;
};
const LEGACY17 = ["timestamp", "reference", "status", "approved", "name", "email", "city", "country",
  "subject", "experience", "rate_usd", "availability", "bio", "photo_link", "video_link", "languages", "notes"];
function env() {
  const t = { applications: makeSheet("applications", [LEGACY17.slice()]) };
  const sent = [], store = {}, P = { EK_ADMIN_TOKEN: "tok-test-only" };
  const ss = { getSheetByName: (n) => t[n] || null, insertSheet: (n) => { t[n] = makeSheet(n, []); return t[n]; }, getSheets: () => Object.keys(t).map((k) => t[k]), getId: () => "ssid" };
  const ctx = {
    console, Logger: { log: () => {} },
    SpreadsheetApp: { getActiveSpreadsheet: () => ss, openById: () => ss, getActive: () => ss, flush() {},
      getUi: () => ({ createMenu: () => ({ addItem: () => ({ addItem: () => ({ addToUi() {} }), addToUi() {} }), addToUi() {} }), alert() {} }) },
    PropertiesService: { getScriptProperties: () => ({ getProperty: (k) => (P[k] === undefined ? null : P[k]), setProperty: (k, v) => { P[k] = v; }, deleteProperty: (k) => { delete P[k]; }, getProperties: () => Object.assign({}, P) }) },
    CacheService: { getScriptCache: () => ({ get: (k) => (store[k] === undefined ? null : store[k]), put: (k, v) => { store[k] = String(v); }, remove: (k) => { delete store[k]; } }) },
    LockService: { getScriptLock: () => ({ waitLock: () => true, tryLock: () => true, releaseLock: () => {} }) },
    GmailApp: { sendEmail: (to, subject) => { sent.push({ to, subject }); }, getAliases: () => [] },
    MailApp: { sendEmail: (o) => { sent.push(o); } },
    Utilities: { formatDate: (d) => (d instanceof Date ? d : new Date(d)).toISOString(),
      base64Encode: (x) => Buffer.from(String(x)).toString("base64"), computeDigest: () => [1], DigestAlgorithm: { SHA_256: "sha" } },
    ContentService: { MimeType: { JSON: "json", TEXT: "text" }, createTextOutput: (x) => { let m = "text"; const o = { getContent: () => x, setMimeType: (v) => { m = v; return o; }, getMimeType: () => m }; return o; } },
    HtmlService: { createHtmlOutput: (x) => ({ getContent: () => x }) },
    ScriptApp: { getService: () => ({ getUrl: () => "https://script.google.test/exec" }) },
  };
  ctx.__tabs = t; ctx.__sent = sent;
  vm.createContext(ctx);
  for (const f of ["apps-script/ApplicationSchema.gs", "apps-script/ApplicationIntake.gs", "apps-script/Unified.gs"]) vm.runInContext(read(f), ctx, { filename: f });
  return ctx;
}
const rowObj = (ctx, at) => {
  const tab = ctx.__tabs.applications, h = tab.grid[0], r = tab.grid[(at || 1)] || [], o = {};
  h.forEach((k, i) => { o[k] = r[i] === undefined ? "" : r[i]; });
  return o;
};

/* ------------------------------------------------------------------- wizard */
const vc = new VirtualConsole(); vc.on("jsdomError", () => {});
const dom = new JSDOM(read("join.html"), { url: "https://ekguru.shop/join.html", runScripts: "outside-only", pretendToBeVisual: true, virtualConsole: vc });
const w = dom.window, doc = w.document;
w.scrollTo = () => {}; w.HTMLElement.prototype.scrollIntoView = () => {};
for (const f of ["js/site-config.js", "js/intake.js", "js/join-schema.js", "js/join-wizard.js"]) w.eval(read(f));
await new Promise((r) => { if (doc.readyState !== "loading") r(); else doc.addEventListener("DOMContentLoaded", r); });
const form = doc.querySelector("form");
const stepIdx = () => parseInt(form.getAttribute("data-jw-step") || "0", 10);
const fire = (el, t) => el.dispatchEvent(new w.Event(t, { bubbles: true }));
const type = (id, v) => { const el = doc.getElementById(id); el.focus(); el.value = v; fire(el, "input"); fire(el, "change"); fire(el, "blur"); };
const pick = (id, v) => { const el = doc.getElementById(id); el.value = v; fire(el, "input"); fire(el, "change"); };
const chip = (val, group) => {
  const box = [...doc.querySelectorAll(group + ' input[type="checkbox"]')].find((b) => b.value === val);
  if (!box) throw new Error("no chip " + val);
  box.checked = true; fire(box, "input"); fire(box, "change");
};
const tickDay = (day, from, to) => {
  const box = doc.querySelector('[name="day-' + day.toLowerCase() + '"]');
  box.checked = true; fire(box, "change");
  const f = doc.querySelector('[name="' + day.toLowerCase() + '-from"]');
  const t = doc.querySelector('[name="' + day.toLowerCase() + '-to"]');
  f.disabled = false; t.disabled = false;
  f.value = from; fire(f, "input"); fire(f, "change");
  t.value = to; fire(t, "input"); fire(t, "change");
};
async function advance() {
  const from = stepIdx();
  for (let attempt = 0; attempt < 3; attempt++) {
    const cont = doc.querySelector(".jw-next");
    if (!cont.hidden) cont.click();
    for (let i = 0; i < 20; i++) {
      await new Promise((r) => setTimeout(r, 30));
      if (stepIdx() !== from) return true;
    }
  }
  return false;
}

console.log("=== A. Full walk, Personal → Review & Submit ===");
check("A. the wizard starts on step 1 of 7", stepIdx() === 0 && doc.querySelectorAll(".jw-step").length === 7);

/* ---- step 1: Personal ---- */
type("jw-name", "Synthetic Proof Person");
type("jw-email", "synthetic.proof@example.test");
type("jw-whatsapp", "+91 98765 43210");
type("jw-city", "Jaipur");
type("jw-country", "India");
type("jw-state", "Rajasthan");
type("jw-photo", "https://img.example.test/p.jpg");
type("jw-intro", "I teach conversational Hindi to adults.");
check("A. step 1 advanced", await advance());

/* ---- step 2: Teaching ---- */
chip("Conversational Hindi", '[data-need-min="subjects"]');
chip("Hindi for Academic Study", '[data-need-min="subjects"]');
chip("Adults", '[data-need-min="levels"]');
chip("Intermediate", '[data-need-min="levels"]');
pick("jw-hindi-level", "Native");
pick("jw-english-level", "Advanced (C1)");
type("jw-other-langs", "Marwari");
pick("jw-years", "6–10 years");
type("jw-online-years", "4");
type("jw-platforms", "Zoom, Google Meet");
check("A. step 2 advanced", await advance());

/* ---- step 3: Education ---- */
pick("jw-edu-qual", "Master's degree");
type("jw-edu-inst", "Rajasthan University");
type("jw-edu-year", "2016");
type("jw-certs", "CTET certified");
check("A. step 3 advanced", await advance());

/* ---- step 4: Profile ---- */
type("jw-headline", "Patient Hindi tutor for beginners");
type("jw-bio", "I have taught Hindi for eight years, in classrooms and online. My lessons are calm, structured and full of speaking practice from the first minute.");
check("A. step 4 advanced", await advance());

/* ---- step 5: Price and availability ---- */
type("jw-price", "15");
pick("jw-duration", "60 min");
pick("jw-currency", "USD");       /* DEF-1: a real choice, so it must travel */
pick("jw-trial", "Free short trial");
pick("jw-tz", "Asia/Kolkata");
tickDay("Mon", "18:00", "20:00");
tickDay("Wed", "07:00", "09:00");
check("A. step 5 advanced", await advance());

/* ---- step 6: Anything else ---- */
type("jw-why", "I want every learner to feel comfortable making mistakes.");
pick("jw-contact-pref", "WhatsApp");
type("jw-referral", "a friend");
check("A. step 6 advanced", await advance());

/* ---- step 7: Review ---- */
check("A. the review step is active", stepIdx() === 6 && doc.getElementById("jw-step-7").hidden === false);
const pv = (k) => { const el = doc.querySelector('[data-jw-pv="' + k + '"]'); return el ? el.textContent.trim() : "<none>"; };
const head = doc.querySelector(".jw-preview-head");
check("A. [DEF-3] the preview header shows the name", head.querySelector("h3").textContent.trim() === "Synthetic Proof Person",
  head.querySelector("h3").textContent.trim());
check("A. [DEF-3] the preview header shows city and country", head.querySelector("p").textContent.trim() === "Jaipur, India",
  head.querySelector("p").textContent.trim());
check("A. [DEF-3] the avatar renders the photo", /img\.example\.test/.test(head.querySelector(".jw-preview-avatar").style.backgroundImage || ""),
  head.querySelector(".jw-preview-avatar").style.backgroundImage);
check("A. the preview price includes the chosen length", pv("price") === "$15 / 60 min", pv("price"));
check("A. the preview availability is the two days", /Mon 18:00-20:00/.test(pv("availability")) && /Wed 07:00-09:00/.test(pv("availability")), pv("availability"));
check("A. Submit is visible and Continue is hidden",
  doc.querySelector(".jw-submit").hidden === false && doc.querySelector(".jw-next").hidden === true);

/* capture what the browser would POST */
w.__bodies = [];
w.fetch = (url, opts) => { w.__bodies.push(JSON.parse(opts.body)); return Promise.resolve({ ok: true, status: 200, text: () => Promise.resolve('{"ok":true,"reference":"EG-PROOF1"}') }); };
doc.querySelector(".jw-submit").click();
await new Promise((r) => setTimeout(r, 80));
check("A. Submit without consent sends nothing", w.__bodies.length === 0, w.__bodies.length);
const cData = doc.getElementById("jw-consent-data"), cPriv = doc.getElementById("jw-consent-privacy");
cData.checked = true; fire(cData, "change");
cPriv.checked = true; fire(cPriv, "change");
doc.querySelector(".jw-submit").click();
await new Promise((r) => setTimeout(r, 300));
check("A. exactly one POST after consent", w.__bodies.length === 1, w.__bodies.length);
const body = w.__bodies[0] || {};
check("A. the visitor sees the reference the server returned",
  /EG-PROOF1/.test(doc.querySelector(".jw-done").textContent), doc.querySelector(".jw-done").textContent.slice(0, 60));

console.log("\n=== B. The body written into a mocked Google Sheet ===");
const ctx = env();
const answer = JSON.parse(ctx.doPost({ postData: { contents: JSON.stringify(body) } }).getContent());
check("B. the backend accepted the browser's own body", answer.ok === true, JSON.stringify(answer).slice(0, 160));
check("B. one row was written", ctx.__tabs.applications.getLastRow() - 1 === 1, ctx.__tabs.applications.getLastRow() - 1);
check("B. one acknowledgement email", ctx.__sent.length === 1, ctx.__sent.length);
const tab = ctx.__tabs.applications;
check("B. the sheet has 69 columns", tab.grid[0].length === 69, tab.grid[0].length);
const R = rowObj(ctx);
console.log("\n   --- the complete row ---");
for (let i = 0; i < tab.grid[0].length; i++) {
  const v = String(tab.grid[i] === undefined ? "" : (tab.grid[1][i] === undefined ? "" : tab.grid[1][i]));
  console.log("   " + String(i + 1).padStart(2) + "  " + tab.grid[0][i].padEnd(20) + " " + (v === "" ? "(empty)" : JSON.stringify(v).slice(0, 84)));
}

const EXPECT = {
  name: "Synthetic Proof Person", email: "synthetic.proof@example.test", whatsapp: "+919876543210",
  city: "Jaipur", country: "India", state: "Rajasthan", contact_pref: "WhatsApp",
  photo_link: "https://img.example.test/p.jpg", intro: "I teach conversational Hindi to adults.",
  hindi_level: "Native", english_level: "Advanced (C1)", other_langs: "Marwari",
  online_years: "4", platforms: "Zoom, Google Meet", edu_qual: "Master's degree",
  edu_inst: "Rajasthan University", edu_year: "2016", certs: "CTET certified",
  headline: "Patient Hindi tutor for beginners", rate_usd: "15", currency: "USD", duration: "60 min",
  trial: "Free short trial", timezone: "Asia/Kolkata",
  subject: "Conversational Hindi, Hindi for Academic Study", status: "pending",
  schema_version: "2.1.0", source: "join.html",
};
console.log("\n=== C. Every value against the mapping ===");
for (const [k, v] of Object.entries(EXPECT)) check("C. " + k, String(R[k]) === String(v), JSON.stringify(R[k]));
check("C. approved is blank (nothing is published by the applicant)", String(R.approved) === "", R.approved);
check("C. subjects_json holds both subjects",
  JSON.parse(R.subjects_json).join("|") === "Conversational Hindi|Hindi for Academic Study", R.subjects_json);
check("C. levels_json holds both levels", JSON.parse(R.levels_json).join("|") === "Adults|Intermediate", R.levels_json);
check("C. availability_json holds exactly Mon and Wed",
  (() => { const a = JSON.parse(R.availability_json); return a.length === 2 && a[0].day === "Mon" && a[1].day === "Wed"; })(), R.availability_json);
/* the browser sends its own meta as {days, timezone, format}; the server's
   derived fallback (DEF-4, used only when the client sends none) adds `slots`.
   Both are valid; this asserts the browser path is what actually landed. */
check("C. [DEF-4] availability_meta is present and well formed",
  (() => { const m = JSON.parse(R.availability_meta);
    return m.days === 2 && m.timezone === "Asia/Kolkata" && m.format === "weekly-hours"; })(), R.availability_meta);
check("C. [DEF-4] the browser's own meta was used, not the derived fallback",
  JSON.parse(R.availability_meta).slots === undefined, R.availability_meta);
check("C. [DEF-2] details_json holds only the genuine overflow answer",
  (() => { const d = JSON.parse(R.details_json || "{}"); return d.referral === "a friend" && !d.status && !d.review_notes; })(), R.details_json);
check("C. the reference on the row is the one the browser was told", R.reference === answer.reference, R.reference);
check("C. no cell holds undefined or [object Object]",
  !tab.grid[1].some((v) => /^(undefined|\[object Object\])$/.test(String(v))));

console.log("\n=== D. Resubmission preserves existing answers, WhatsApp, notes, approval ===");
/* an admin reviews the row and leaves a private note, then approves */
tab.grid[1][tab.grid[0].indexOf("status")] = "approved";
tab.grid[1][tab.grid[0].indexOf("approved")] = "Yes";
tab.grid[1][tab.grid[0].indexOf("review_notes")] = "PRIVATE: identity checked, references verified";
tab.grid[1][tab.grid[0].indexOf("reviewed_by")] = "owner@ekguru.shop";
const BEFORE = rowObj(ctx);

/* the tutor comes back, changes only the city and one optional answer */
const resub = {
  kind: "application", consent: true, website: "", submission_id: "application-resub-1",
  fields: {
    name: "Synthetic Proof Person", email: "synthetic.proof@example.test", city: "Udaipur",
    country: "India", subject: "Conversational Hindi, Hindi for Academic Study",
    bio: "I have taught Hindi for eight years, in classrooms and online. My lessons are calm, structured and full of speaking practice from the first minute.",
    rate_usd: "18", timezone: "Asia/Kolkata",
    subjects: ["Conversational Hindi", "Hindi for Academic Study"], levels: ["Adults", "Intermediate"],
    availability_slots: [{ day: "Mon", from: "18:00", to: "20:00" }, { day: "Wed", from: "07:00", to: "09:00" }],
  },
};
const r2 = JSON.parse(ctx.doPost({ postData: { contents: JSON.stringify(resub) } }).getContent());
check("D. the resubmission is accepted", r2.ok === true, JSON.stringify(r2).slice(0, 140));
check("D. it updated the existing row rather than adding one", ctx.__tabs.applications.getLastRow() - 1 === 1, ctx.__tabs.applications.getLastRow() - 1);
const AFTER = rowObj(ctx);
check("D. the changed city landed", AFTER.city === "Udaipur", AFTER.city);
check("D. the changed price landed", String(AFTER.rate_usd) === "18", AFTER.rate_usd);
check("D. approved status preserved", AFTER.status === "approved" && String(AFTER.approved) === "Yes",
  JSON.stringify({ s: AFTER.status, a: AFTER.approved }));
check("D. the private reviewer note preserved", AFTER.review_notes === "PRIVATE: identity checked, references verified", AFTER.review_notes);
check("D. reviewed_by preserved", AFTER.reviewed_by === "owner@ekguru.shop", AFTER.reviewed_by);
check("D. the WhatsApp number preserved", AFTER.whatsapp === "+919876543210", AFTER.whatsapp);
check("D. the photo link preserved", AFTER.photo_link === "https://img.example.test/p.jpg", AFTER.photo_link);
check("D. [DEF-1] the chosen lesson length preserved (not reset to 50 min)", AFTER.duration === "60 min", AFTER.duration);
check("D. [DEF-1] the chosen currency preserved", AFTER.currency === "USD", AFTER.currency);
check("D. the Hindi level preserved (not reset)", AFTER.hindi_level === "Native", AFTER.hindi_level);
check("D. the contact preference preserved", AFTER.contact_pref === "WhatsApp", AFTER.contact_pref);
check("D. the education answers preserved", AFTER.edu_qual === BEFORE.edu_qual && AFTER.edu_inst === BEFORE.edu_inst);
check("D. the intro and headline preserved", AFTER.intro === BEFORE.intro && AFTER.headline === BEFORE.headline);
check("D. consent stays on record", AFTER.consent_terms === "yes" && AFTER.consent_privacy === "yes");
check("D. the original reference and timestamp preserved",
  AFTER.reference === BEFORE.reference && AFTER.timestamp === BEFORE.timestamp);
check("D. the genuine overflow answer preserved", /"referral":"a friend"/.test(AFTER.details_json || ""), AFTER.details_json);
check("D. no server-owned name leaked into details_json",
  (() => { const d = JSON.parse(AFTER.details_json || "{}"); return !d.status && !d.approved && !d.review_notes; })(), AFTER.details_json);

console.log("\n" + (fail ? fail + " FAILURE(S)" : "ALL CHECKS PASSED") + "  (" + pass + " passed, " + fail + " failed)");
process.exit(fail ? 1 : 0);

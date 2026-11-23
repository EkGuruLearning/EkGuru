/* DEF-1 … DEF-4, A1, A2: failing-before / fixed-after regression suite.
   ---------------------------------------------------------------------------
   For each defect this file builds a "before" copy by reverting EXACTLY that
   one fix out of the current file (in memory — nothing on disk is touched),
   asserts the revert really applied, then runs the SAME check against both
   copies and requires before = the bug showing, after = fixed.

   That is the point of the file: a regression test that has never been seen
   to fail proves nothing. `git stash` is not used, no file outside os.tmpdir()
   is written, and no network or Google service is contacted.

   Run: node tools/test-defect-regressions.mjs
*/
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import vm from "node:vm";
import { JSDOM, VirtualConsole } from "jsdom";

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8");
let pass = 0, fail = 0;
const check = (n, c, e) => { if (c) pass++; else fail++; console.log((c ? "PASS  " : "FAIL  ") + n + (c ? "" : "  ->  " + (e === undefined ? "" : e))); };
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), "ekg-ab-"));

/* ============================ wizard bootstrap ============================ */
const makeDom = (html) => {
  const vc = new VirtualConsole(); vc.on("jsdomError", () => {});
  const dom = new JSDOM(html, { url: "https://ekguru.shop/join.html", runScripts: "outside-only", pretendToBeVisual: true, virtualConsole: vc });
  const w = dom.window;
  w.scrollTo = () => {};
  w.HTMLElement.prototype.scrollIntoView = () => {};
  for (const f of ["js/site-config.js", "js/intake.js", "js/join-schema.js"]) w.eval(read(f));
  return { dom, w, doc: w.document };
};
const evalWizard = (w, src) => w.eval(src);

/* a minimal wizard driver: fill the required answers, jump to review */
async function boot(html, wizardSrc) {
  const { w, doc } = makeDom(html);
  evalWizard(w, wizardSrc);
  await new Promise((r) => { if (doc.readyState !== "loading") r(); else doc.addEventListener("DOMContentLoaded", r); });
  await new Promise((r) => setTimeout(r, 80));
  return { w, doc };
}

async function driveToReview(w, doc) {
  const fire = (el, t) => el.dispatchEvent(new w.Event(t, { bubbles: true }));
  const set = (id, v) => { const el = doc.getElementById(id); if (!el) return; el.value = v; fire(el, "input"); fire(el, "change"); fire(el, "blur"); };
  const pick = (id, v) => set(id, v);
  set("jw-name", "Preview Person"); set("jw-email", "preview@example.test"); set("jw-city", "Jaipur");
  set("jw-country", "India"); set("jw-bio", "A calm, structured introduction to conversational Hindi.");
  set("jw-price", "15"); set("jw-tz", "Asia/Kolkata");
  for (const cb of doc.querySelectorAll('input[name="subjects"]')) if (cb.value === "Conversational Hindi") { cb.checked = true; fire(cb, "change"); }
  for (const cb of doc.querySelectorAll('input[name="levels"]')) if (cb.value === "Adults") { cb.checked = true; fire(cb, "change"); }
  const day = doc.querySelector('[name="day-mon"]'); day.checked = true; fire(day, "change");
  const f = doc.querySelector('[name="mon-from"]'), t = doc.querySelector('[name="mon-to"]');
  f.disabled = false; t.disabled = false; f.value = "18:00"; fire(f, "change"); t.value = "20:00"; fire(t, "change");
  /* walk the steps with the real Continue button: the wizard validates the
     step it is on and allows exactly one step forward, and it ignores a click
     that lands inside its 80ms anti-double-tap lock */
  const form = doc.querySelector("form");
  const stepIdx = () => parseInt(form.getAttribute("data-jw-step") || "0", 10);
  const cont = () => doc.querySelector(".jw-next");
  while (stepIdx() < 6) {
    const from = stepIdx();
    let moved = false;
    for (let attempt = 0; attempt < 3 && !moved; attempt++) {
      if (!cont().hidden) cont().click();
      for (let i = 0; i < 20; i++) {
        await new Promise((r) => setTimeout(r, 30));
        if (stepIdx() !== from) { moved = true; break; }
      }
    }
    if (!moved) break;
  }
  const s7 = doc.getElementById("jw-step-7");
  for (let i = 0; i < 20 && s7 && s7.hidden; i++) await new Promise((r) => setTimeout(r, 50));
  return stepIdx() === 6;
}

/* ============================ backend bootstrap =========================== */
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
/* `router` picks which router the seam is exercised through:
     "unified"     Unified.gs — the live deployment shape
     "standalone"  Intake.gs  — the legacy drop-in file (A1 lives here) */
function env(intakeSrc, router, routerSrc) {
  const t = { applications: makeSheet("applications", [LEGACY17.slice()]) };
  const sent = [], store = {}, P = {};
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
  P.EK_ADMIN_TOKEN = "test-admin-token";
  ctx.__tabs = t; ctx.__sent = sent;
  vm.createContext(ctx);
  vm.runInContext(read("apps-script/ApplicationSchema.gs"), ctx, { filename: "ApplicationSchema.gs" });
  vm.runInContext(intakeSrc, ctx, { filename: "ApplicationIntake.gs" });
  if (router === "standalone") {
    vm.runInContext(routerSrc || read("apps-script/Intake.gs"), ctx, { filename: "Intake.gs" });
  } else {
    vm.runInContext(routerSrc || read("apps-script/Unified.gs"), ctx, { filename: "Unified.gs" });
  }
  return ctx;
}
const LEGACY17 = ["timestamp", "reference", "status", "approved", "name", "email", "city", "country",
  "subject", "experience", "rate_usd", "availability", "bio", "photo_link", "video_link", "languages", "notes"];
const rowObj = (ctx, at) => {
  const tab = ctx.__tabs.applications, h = tab.grid[0], r = tab.grid[(at || 1)] || [], o = {};
  h.forEach((k, i) => { o[k] = r[i] === undefined ? "" : r[i]; });
  return o;
};
const post = (ctx, body) => JSON.parse(ctx.doPost({ postData: { contents: JSON.stringify(body) } }).getContent());

/* ========================================================================== */
/* DEF-1 — an untouched select must not answer for the tutor                  */
/* ========================================================================== */
console.log("=== DEF-1 — duration / currency / hindi_level defaults ===");
{
  const CUR = read("join.html");
  let BEFORE = CUR;
  for (const id of ["jw-duration", "jw-currency", "jw-hindi-level"]) {
    const re = new RegExp('(id="' + id + '"[^>]*>\\s*)<option value="">Select</option>\\s*');
    if (!re.test(BEFORE)) throw new Error("cannot build the DEF-1 'before' copy for " + id);
    BEFORE = BEFORE.replace(re, "$1");
  }
  check("DEF-1 setup: the before-copy really lost the empty option",
    !/id="jw-duration"[^>]*>\s*<option value="">/.test(BEFORE) && /id="jw-duration"[^>]*>\s*<option value="">/.test(CUR));

  const run = async (html) => {
    const { w, doc } = await boot(html, read("js/join-wizard.js"));
    const out = w.EkGuruJoinWizard.buildPayload(doc.querySelector("form"));
    return (out && out.payload) || out || {};
  };
  const before = await run(BEFORE);
  const after = await run(CUR);
  check("DEF-1 before: an untouched form DOES send duration (the bug shows)", before.duration !== undefined, JSON.stringify(before.duration));
  check("DEF-1 before: an untouched form DOES send currency", before.currency !== undefined, JSON.stringify(before.currency));
  check("DEF-1 before: an untouched form DOES send hindi_level", before.hindi_level !== undefined, JSON.stringify(before.hindi_level));
  check("DEF-1 after: an untouched form sends none of the three",
    after.duration === undefined && after.currency === undefined && after.hindi_level === undefined,
    JSON.stringify({ d: after.duration, c: after.currency, h: after.hindi_level }));

  /* and the consequence on a real row, before vs after */
  const resubmit = (ctx, fields) => {
    post(ctx, { kind: "application", consent: true, consent_privacy: true, website: "", submission_id: "application-a1",
      fields: { name: "Guard", email: "guard@example.test", city: "Pune", country: "India", subject: "Hindi",
        bio: "A real introduction.", rate_usd: "18", timezone: "Asia/Kolkata", duration: "90 min", currency: "INR", hindi_level: "Fluent",
        availability_slots: [{ day: "Mon", from: "18:00", to: "20:00" }] } });
    post(ctx, { kind: "application", consent: true, consent_privacy: true, website: "", submission_id: "application-a2",
      fields: { name: "Guard", email: "guard@example.test", city: "Nashik", country: "India", subject: "Hindi",
        bio: "A real introduction.", rate_usd: "18", timezone: "Asia/Kolkata",
        availability_slots: [{ day: "Mon", from: "18:00", to: "20:00" }], ...fields } });
    return rowObj(env(read("apps-script/ApplicationIntake.gs")) && ctx);
  };
  const ctxB = env(read("apps-script/ApplicationIntake.gs"));
  post(ctxB, { kind: "application", consent: true, consent_privacy: true, website: "", submission_id: "b1",
    fields: { name: "Guard", email: "guard@example.test", city: "Pune", country: "India", subject: "Hindi",
      bio: "A real introduction.", rate_usd: "18", timezone: "Asia/Kolkata", duration: "90 min", currency: "INR", hindi_level: "Fluent",
      availability_slots: [{ day: "Mon", from: "18:00", to: "20:00" }] } });
  const beforeSend = { duration: before.duration, currency: before.currency, hindi_level: before.hindi_level };
  post(ctxB, { kind: "application", consent: true, consent_privacy: true, website: "", submission_id: "b2",
    fields: { name: "Guard", email: "guard@example.test", city: "Nashik", country: "India", subject: "Hindi",
      bio: "A real introduction.", rate_usd: "18", timezone: "Asia/Kolkata",
      availability_slots: [{ day: "Mon", from: "18:00", to: "20:00" }], ...beforeSend } });
  const rowB = rowObj(ctxB);
  check("DEF-1 before: the stored 90 min was overwritten by the form default",
    rowB.duration === "50 min", "stored = " + JSON.stringify(rowB.duration));
  check("DEF-1 before: INR was overwritten by USD", rowB.currency === "USD", rowB.currency);
  check("DEF-1 before: Fluent was overwritten by Native", rowB.hindi_level === "Native", rowB.hindi_level);

  const ctxA = env(read("apps-script/ApplicationIntake.gs"));
  post(ctxA, { kind: "application", consent: true, consent_privacy: true, website: "", submission_id: "a1",
    fields: { name: "Guard", email: "guard@example.test", city: "Pune", country: "India", subject: "Hindi",
      bio: "A real introduction.", rate_usd: "18", timezone: "Asia/Kolkata", duration: "90 min", currency: "INR", hindi_level: "Fluent",
      availability_slots: [{ day: "Mon", from: "18:00", to: "20:00" }] } });
  post(ctxA, { kind: "application", consent: true, consent_privacy: true, website: "", submission_id: "a2",
    fields: { name: "Guard", email: "guard@example.test", city: "Nashik", country: "India", subject: "Hindi",
      bio: "A real introduction.", rate_usd: "18", timezone: "Asia/Kolkata",
      availability_slots: [{ day: "Mon", from: "18:00", to: "20:00" }] } });
  const rowA = rowObj(ctxA);
  check("DEF-1 after: 90 min survives the resubmission", rowA.duration === "90 min", rowA.duration);
  check("DEF-1 after: INR survives", rowA.currency === "INR", rowA.currency);
  check("DEF-1 after: Fluent survives", rowA.hindi_level === "Fluent", rowA.hindi_level);
  check("DEF-1 after: the change that WAS made still lands", rowA.city === "Nashik", rowA.city);
  check("DEF-1 after: new applications still get the documented defaults",
    (() => {
      const c = env(read("apps-script/ApplicationIntake.gs"));
      post(c, { kind: "application", consent: true, consent_privacy: true, website: "", submission_id: "n1",
        fields: { name: "New", email: "new@example.test", city: "Pune", country: "India", subject: "Hindi",
          bio: "A real introduction.", rate_usd: "18", timezone: "Asia/Kolkata",
          availability_slots: [{ day: "Mon", from: "18:00", to: "20:00" }] } });
      const r = rowObj(c);
      return r.duration === "50 min" && r.currency === "USD" && r.hindi_level === "";
    })());
}

/* ========================================================================== */
/* DEF-2 — a server-owned name is never stored under its own key              */
/* ========================================================================== */
console.log("\n=== DEF-2 — details_json and server-owned names ===");
{
  const CUR = read("apps-script/ApplicationIntake.gs");
  let BEFORE = CUR.replace(
    '    if (reservedNames[key]) { reserved[key] = 1; continue; }   /* a column we own, not a free-text answer */\n', "");
  BEFORE = BEFORE.replace(
    '      if (reservedNames[dk]) { reserved[dk] = 1; continue; }\n', "");
  check("DEF-2 setup: the before-copy really lost the divert",
    !/a column we own, not a free-text answer/.test(BEFORE) && /a column we own, not a free-text answer/.test(CUR));

  const run = (src) => {
    const ctx = env(src);
    const r = post(ctx, { kind: "application", consent: true, consent_privacy: true, website: "", submission_id: "application-d2",
      fields: { name: "Sec", email: "sec@example.test", city: "Pune", country: "India", subject: "Hindi",
        bio: "A real introduction.", rate_usd: "12", timezone: "Asia/Kolkata",
        availability_slots: [{ day: "Mon", from: "19:00", to: "21:00" }],
        status: "approved", approved: "Yes", review_notes: "PRIVATE: forged" } });
    const row = rowObj(ctx);
    return { res: r, row, det: JSON.parse(row.details_json || "{}") };
  };
  const b = run(BEFORE), a = run(CUR);
  check("DEF-2 before: review_notes IS filed under its own key (the bug shows)",
    b.det.review_notes === "PRIVATE: forged", JSON.stringify(b.det));
  check("DEF-2 before: the real cell is still safe (never was the risk)", b.row.review_notes === "", JSON.stringify(b.row.review_notes));
  check("DEF-2 after: review_notes is not under its own key", a.det.review_notes === undefined, JSON.stringify(a.det));
  check("DEF-2 after: status is not under its own key", a.det.status === undefined, JSON.stringify(a.det));
  check("DEF-2 after: approved is not under its own key", a.det.approved === undefined, JSON.stringify(a.det));
  check("DEF-2 after: it is recorded inertly as sent_*", a.det.sent_review_notes === "PRIVATE: forged", JSON.stringify(a.det));
  check("DEF-2 after: nothing is silently binned", Object.keys(a.det).length >= 3, JSON.stringify(a.det));
  check("DEF-2 after: the verdict cells are untouched", a.row.status === "pending" && String(a.row.approved) === "",
    JSON.stringify({ s: a.row.status, ap: a.row.approved }));

  /* legitimate fields must survive, and the contract must not move */
  const leg = env(CUR);
  const r1 = post(leg, { kind: "application", consent: true, consent_privacy: true, website: "", submission_id: "application-l1",
    fields: { name: "Legit", email: "legit@example.test", city: "Pune", country: "India", subject: "Hindi",
      bio: "A real introduction.", rate_usd: "12", timezone: "Asia/Kolkata", referral: "a friend", why: "I love teaching",
      availability_slots: [{ day: "Mon", from: "19:00", to: "21:00" }] } });
  const L = rowObj(leg);
  const ldet = JSON.parse(L.details_json || "{}");
  check("DEF-2 after: a legitimate overflow answer is kept verbatim", ldet.referral === "a friend", JSON.stringify(ldet));
  check("DEF-2 after: a mapped field still lands in its column", L.why === "I love teaching", L.why);
  check("DEF-2 after: the submission contract is unchanged",
    r1.ok === true && /^EG-/.test(r1.reference || "") && r1.duplicate === false, JSON.stringify(r1));
  const invented = leg.__tabs.applications.grid[0].filter((h) => /^sent_/.test(String(h)) || /PRIVATE/i.test(String(h)));
  check("DEF-2 after: the header gained no invented column", invented.length === 0, invented.join(","));
  check("DEF-2 after: the header is still exactly the 69 schema columns",
    leg.__tabs.applications.grid[0].length === 69, leg.__tabs.applications.grid[0].length);
  check("DEF-2 after: no authorisation surface was touched (admin token still required)",
    (() => {
      const c = env(CUR);
      const r = post(c, { action: "ekAdminUpdate", reference: "EG-AAAAAA", status: "approved" });
      return r.ok === false && /not authorised|switched off/.test(String(r.error));
    })());
}

/* ========================================================================== */
/* DEF-3 — the review preview header renders the applicant                    */
/* ========================================================================== */
console.log("\n=== DEF-3 — review preview header ===");
{
  const CUR = read("join.html");
  const BEFORE = CUR.replace('<div class="jw-preview-head" data-jw-pv-head="">', '<div class="jw-preview-head">');
  check("DEF-3 setup: the before-copy really lost the attribute",
    !/jw-preview-head" data-jw-pv-head/.test(BEFORE) && /jw-preview-head" data-jw-pv-head/.test(CUR));

  const run = async (html) => {
    const { w, doc } = await boot(html, read("js/join-wizard.js"));
    const reached = await driveToReview(w, doc);
    const head = doc.querySelector(".jw-preview-head");
    return {
      reached,
      name: String((head.querySelector("h3") || {}).textContent || "").trim(),
      sub: String((head.querySelector("p") || {}).textContent || "").trim(),
      avatar: head.querySelector(".jw-preview-avatar"),
    };
  };
  const b = await run(BEFORE), a = await run(CUR);
  check("DEF-3 before: the review step was reached (so this is not a navigation artefact)", b.reached === true);
  check("DEF-3 before: the header still says the placeholder name", b.name === "Your name", JSON.stringify(b.name));
  check("DEF-3 before: the header still says the placeholder city", b.sub === "City, country", JSON.stringify(b.sub));
  check("DEF-3 before: the avatar is still the literal '?'", String(b.avatar.textContent).trim() === "?", JSON.stringify(b.avatar.textContent));
  check("DEF-3 after: the review step is reached", a.reached === true);
  check("DEF-3 after: the header shows the applicant's name", a.name === "Preview Person", JSON.stringify(a.name));
  check("DEF-3 after: the header shows city and country", a.sub === "Jaipur, India", JSON.stringify(a.sub));
  check("DEF-3 after: the avatar shows initials instead of '?'",
    String(a.avatar.textContent).trim() !== "?" && String(a.avatar.textContent).trim().length > 0,
    JSON.stringify(a.avatar.textContent));

  /* the intentional fallback: no photo -> initials, no name -> the placeholder */
  /* a fresh page where nothing has been typed yet: the markup placeholders are
     the intentional fallback, not an empty box */
  {
    const { w, doc } = await boot(CUR, read("js/join-wizard.js"));
    const head = doc.querySelector(".jw-preview-head");
    check("DEF-3 after: before anything is typed the header shows a deliberate fallback, never blank",
      head.querySelector("h3").textContent.trim().length > 0 &&
      head.querySelector("p").textContent.trim().length > 0 &&
      String(head.querySelector(".jw-preview-avatar").textContent).trim() === "?",
      JSON.stringify({ n: head.querySelector("h3").textContent.trim(), p: head.querySelector("p").textContent.trim() }));
  }

  /* a photo URL wins over initials, and is referenced safely */
  const { w, doc } = await boot(CUR, read("js/join-wizard.js"));
  const fire = (el, t) => el.dispatchEvent(new w.Event(t, { bubbles: true }));
  const set = (id, v) => { const el = doc.getElementById(id); el.value = v; fire(el, "input"); fire(el, "change"); };
  set("jw-photo", 'https://img.example.test/a.jpg');
  await driveToReview(w, doc);
  const head = doc.querySelector(".jw-preview-head");
  const av = head.querySelector(".jw-preview-avatar");
  check("DEF-3 after: a photo URL becomes the avatar background",
    /url\("https:\/\/img\.example\.test\/a\.jpg"\)/.test(av.style.backgroundImage || ""), av.style.backgroundImage);
  check("DEF-3 after: and the initials text is cleared", String(av.textContent).trim() === "", JSON.stringify(av.textContent));
}

/* ========================================================================== */
/* DEF-4 — availability_meta: missing / null / "" / valid                     */
/* ========================================================================== */
console.log("\n=== DEF-4 — availability_meta fallback ===");
{
  const CUR = read("apps-script/ApplicationIntake.gs");
  const BEFORE = CUR.replace('if (values.availability_meta == null || values.availability_meta === "") {',
    "if (values.availability_meta == null) {");
  check("DEF-4 setup: the before-copy really has the narrow guard",
    /if \(values\.availability_meta == null\) \{/.test(BEFORE) &&
    /values\.availability_meta === ""/.test(CUR));

  const base = { name: "Meta", email: "meta@example.test", city: "Pune", country: "India", subject: "Hindi",
    bio: "A real introduction.", rate_usd: "12", timezone: "Asia/Kolkata",
    availability_slots: [{ day: "Mon", from: "19:00", to: "21:00" }] };
  const run = (src, patch) => {
    const ctx = env(src);
    const fields = Object.assign({}, base);
    if (patch === "omit") { /* nothing */ }
    else if (patch === "null") fields.availability_meta = null;
    else if (patch === "empty") fields.availability_meta = "";
    else if (patch === "valid") fields.availability_meta = { days: 7, slots: 7, timezone: "Asia/Kolkata", format: "weekly-hours" };
    const r = post(ctx, { kind: "application", consent: true, consent_privacy: true, website: "", submission_id: "application-m1", fields });
    const row = rowObj(ctx);
    let parsed = null;
    try { parsed = JSON.parse(row.availability_meta || "null"); } catch (e) { parsed = "UNPARSEABLE"; }
    return { res: r, raw: String(row.availability_meta || ""), parsed, json: String(row.availability_json || "") };
  };

  for (const [label, patch] of [["missing", "omit"], ["null", "null"], ["empty string", "empty"]]) {
    const b = run(BEFORE, patch), a = run(CUR, patch);
    check("DEF-4 before: a " + label + " meta leaves the column empty (the bug)", b.raw === "", JSON.stringify(b.raw));
    check("DEF-4 after: a " + label + " meta is derived", a.raw.length > 0 && a.parsed && a.parsed.slots === 1,
      JSON.stringify(a.raw));
    check("DEF-4 after: the derived meta is well formed for a " + label + " meta",
      a.parsed && a.parsed.days === 1 && a.parsed.timezone === "Asia/Kolkata" && a.parsed.format === "weekly-hours",
      JSON.stringify(a.parsed));
    check("DEF-4 after: availability_json is filled either way for a " + label + " meta", /Mon/.test(a.json), a.json.slice(0, 40));
  }
  const bv = run(BEFORE, "valid"), av2 = run(CUR, "valid");
  check("DEF-4 before: a valid client value was already respected", bv.parsed && bv.parsed.slots === 7, bv.raw);
  check("DEF-4 after: a valid client value is still respected, not recomputed", av2.parsed && av2.parsed.slots === 7, av2.raw);
  check("DEF-4 after: the submission is accepted in every one of the four cases",
    run(CUR, "omit").res.ok === true && run(CUR, "null").res.ok === true &&
    run(CUR, "empty").res.ok === true && run(CUR, "valid").res.ok === true);
  check("DEF-4 after: no availability at all still means an empty meta",
    (() => { const c = env(CUR); const f = Object.assign({}, base); delete f.availability_slots;
      post(c, { kind: "application", consent: true, consent_privacy: true, website: "", submission_id: "application-m9", fields: f });
      return String(rowObj(c).availability_meta || "") === ""; })());

  /* the browser wizard's own payload must still carry a meta, so both halves agree */
  {
    const { w, doc } = await boot(read("join.html"), read("js/join-wizard.js"));
    const fire = (el, t) => el.dispatchEvent(new w.Event(t, { bubbles: true }));
    const day = doc.querySelector('[name="day-mon"]'); day.checked = true; fire(day, "change");
    const f = doc.querySelector('[name="mon-from"]'), t = doc.querySelector("[name=\"mon-to\"]");
    f.disabled = false; t.disabled = false; f.value = "18:00"; fire(f, "change"); t.value = "20:00"; fire(t, "change");
    const out = w.EkGuruJoinWizard.buildPayload(doc.querySelector("form"));
    const p = (out && out.payload) || out || {};
    check("DEF-4 after: the browser still sends availability_meta itself",
      !!p.availability_meta && p.availability_meta.days === 1, JSON.stringify(p.availability_meta));
    check("DEF-4 after: the browser still sends availability_slots",
      Array.isArray(p.availability_slots) && p.availability_slots.length === 1, JSON.stringify(p.availability_slots));
  }
}


/* ========================================================================== */
/* A1 — a filled honeypot must be caught BEFORE any application write/email   */
/*                                                                             */
/* Before the fix, Intake.gs ran the application seam before the honeypot, so  */
/* a bot that filled the hidden box still produced a stored row and an email   */
/* to the owner. Unified.gs had already been reordered; Intake.gs had not.     */
/* Both routers are exercised here, through their real doPost.                 */
/* ========================================================================== */
console.log("\n=== A1 — honeypot ordering, both routers ===");
{
  const ROUTERS = { unified: "apps-script/Unified.gs", standalone: "apps-script/Intake.gs" };
  const AI = read("apps-script/ApplicationIntake.gs");

  const base = { name: "Spam Bot", email: "bot@spam.example", city: "X", country: "India",
    subject: "Hindi", bio: "buy cheap followers now", rate_usd: "5", timezone: "Asia/Kolkata",
    availability_slots: [{ day: "Mon", from: "19:00", to: "21:00" }] };
  const bot = (hp) => ({ kind: "application", consent: true, consent_privacy: true, website: hp,
    submission_id: "application-bot", fields: base });

  /* ---- the exact revert: seam back ABOVE the honeypot ----
     Anchored on the CODE, not on a comment, because the two routers document the
     seam differently (Unified.gs has no leading comment for it at all). */
  const SEAM = `    if (typeof ekApplicationAction_ === "function") {
      var ekHandled = ekApplicationAction_(body);
      if (ekHandled) return ekHandled;
    }`;
  const HP = `    if (String(body.website || "").trim() !== "") {
      return intakeJson_({ ok: true, reference: "EG-" + intakeRef_() });
    }`;
  const revert = (src) => {
    const seamAt = src.indexOf(SEAM);
    const hpAt = src.indexOf(HP);
    if (seamAt === -1 || hpAt === -1) return src;
    if (seamAt < hpAt) return src;   /* already the old shape: seam above honeypot */
    /* pull the seam out, then drop it immediately before the honeypot */
    const without = src.slice(0, seamAt) + src.slice(seamAt + SEAM.length);
    const newHpAt = without.indexOf(HP);
    return without.slice(0, newHpAt) + SEAM + "\n\n" + without.slice(newHpAt);
  };

  for (const [name, file] of Object.entries(ROUTERS)) {
    const CUR = read(file);
    const REVERTED = revert(CUR);
    check("A1 [" + name + "] setup: the before-copy really puts the seam above the honeypot",
      REVERTED !== CUR && REVERTED.indexOf("ekApplicationAction_(body)") < REVERTED.indexOf("body.website"));
    check("A1 [" + name + "] after: the shipped file checks the honeypot first",
      CUR.indexOf("body.website") < CUR.indexOf("ekApplicationAction_(body)"));

    const run = (routerSrc, hp) => {
      const c = env(AI, name, routerSrc);
      const res = post(c, bot(hp));
      return { res, rows: c.__tabs.applications.getLastRow() - 1, mails: c.__sent.length, c };
    };

    const before = run(REVERTED, "http://spam.example");
    check("A1 [" + name + "] BEFORE: a filled honeypot stores a row and sends an email (the bug)",
      before.rows === 1 && before.mails === 1, "rows=" + before.rows + " mails=" + before.mails);
    check("A1 [" + name + "] BEFORE: and answers as a real submission",
      before.res.duplicate === false && before.res.mail === "sent", JSON.stringify(before.res));

    for (const hp of ["http://spam.example", "x", "https://spam.example/offer"]) {
      const a = run(CUR, hp);
      check("A1 [" + name + "] AFTER: honeypot '" + hp.slice(0, 22) + "' writes no row", a.rows === 0, a.rows);
      check("A1 [" + name + "] AFTER: honeypot '" + hp.slice(0, 22) + "' sends no email", a.mails === 0, a.mails);
      check("A1 [" + name + "] AFTER: the bot still sees a believable success",
        a.res.ok === true && /^EG-/.test(a.res.reference || ""), JSON.stringify(a.res));
      check("A1 [" + name + "] AFTER: it is the pretend-success, not a stored answer",
        a.res.duplicate === undefined && a.res.mail === undefined, JSON.stringify(a.res));
    }

    /* whitespace-only is intentionally NOT a honeypot hit: the check trims, so
       a blank-looking value is treated as a person. Asserted so the behaviour
       is deliberate and identical in both routers. */
    const ws = run(CUR, "   ");
    check("A1 [" + name + "] a whitespace-only honeypot is treated as a person (trim, by design)",
      ws.rows === 1, ws.rows);

    /* the fix must not have switched real submissions or the owner off */
    const real = run(CUR, "");
    check("A1 [" + name + "] AFTER: an empty honeypot still stores and emails",
      real.res.ok === true && real.rows === 1 && real.mails === 1,
      "rows=" + real.rows + " mails=" + real.mails);
    const ref = (() => { const t = real.c.__tabs.applications, h = t.grid[0];
      return t.grid[1][h.indexOf("reference")]; })();
    const admin = post(real.c, { action: "ekAdminUpdate", token: "test-admin-token", reference: ref,
      status: "under_review", reason: "checked" });
    check("A1 [" + name + "] after: an owner action (no honeypot field) is not blocked",
      admin.ok === true, JSON.stringify(admin).slice(0, 110));
  }

  /* one write site and one mail site, both after the gate */
  check("A1 there is exactly one application row write in the backend",
    (read("apps-script/ApplicationIntake.gs").match(/tab\.appendRow\(row\)/g) || []).length === 1);
  check("A1 the application seam is called from exactly the two routers",
    (read("apps-script/Unified.gs").match(/ekApplicationAction_\(body\)/g) || []).length === 1 &&
    (read("apps-script/Intake.gs").match(/ekApplicationAction_\(body\)/g) || []).length === 1);
}

/* ========================================================================== */
/* A2 — the retry identity is scoped on the server, never chosen by a client  */
/*                                                                             */
/* The audit's undetected mutation: the retry lookup scanned the WHOLE tab for  */
/* the client's value, so anyone could plant a value and make another          */
/* applicant's later submission look like a retry of the planted row —         */
/* acknowledged as "already received", never stored, never emailed.            */
/* ========================================================================== */
console.log("\n=== A2 — submission identity: planted / guessed / retried ===");
{
  const CUR = read("apps-script/ApplicationIntake.gs");
  const ROUTERS = ["unified", "standalone"];

  const base = { name: "Legit", email: "legit@example.test", city: "Pune", country: "India",
    subject: "Hindi", bio: "A real introduction.", rate_usd: "12", timezone: "Asia/Kolkata",
    availability_slots: [{ day: "Mon", from: "19:00", to: "21:00" }] };
  const det = (c, at) => { try { return JSON.parse(rowObj(c, at).details_json || "{}"); } catch (e) { return null; } };

  /* ---- the exact mutations ---- */
  /* The honest "before" state combines all three reverts, because the pre-fix
     code had none of the three: it did not reserve the name, it did not write
     the server's retry key on insert, and its retry lookup matched the client's
     value in EVERY row. Each mutant below isolates one half so the suite can
     say which half is load-bearing. */
  /* M1 — the audit's undetected mutation: the retry lookup matched the client's
     value tab-wide, including another applicant's row. */
  const M1 = CUR.replace("    if (i + 2 !== scope.row) continue;                 /* only the caller's own row */\n", "", 1);
  check("A2 setup: M1 (tab-wide retry scan) really applies",
    M1 !== CUR && M1.indexOf("only the caller's own row") === -1);
  /* M2 — the name was not reserved, so a client value could become the key */
  const M2 = CUR.replace("  reservedNames.submission_id = 1;\n", "", 1);
  check("A2 setup: M2 (reservation removed) really applies", M2 !== CUR);
  /* M3 — the insert path did not write the server's retry key (reservation
     left intact, so this isolates the insert-write fix on its own) */
  const M3 = CUR.replace("      if (submissionId) dj.submission_id = submissionId;\n      row[map.details_json]",
    "      row[map.details_json]", 1);
  check("A2 setup: M3 (insert-path write removed, reservation intact) really applies",
    M3 !== CUR && M3.indexOf("reservedNames.submission_id = 1;") !== -1);
  /* PRE — everything the fix added is gone, including the fail-closed guard,
     so this is the file as it stood before the remediation. */
  const PRE = M1
    .replace("  reservedNames.submission_id = 1;\n", "", 1)
    .replace("      if (submissionId) dj.submission_id = submissionId;\n      row[map.details_json]",
             "      row[map.details_json]", 1)
    .replace('  if (!scope || !scope.row) return "";\n', "", 1);
  check("A2 setup: PRE really restores the pre-fix state (all four halves gone)",
    PRE.indexOf("reservedNames.submission_id") === -1 &&
    PRE.indexOf("only the caller's own row") === -1 &&
    PRE.indexOf("if (submissionId) dj.submission_id") === -1 &&
    PRE.indexOf("if (!scope || !scope.row)") === -1);

  /* the exploit, three moves, against whichever build we are given */
  const exploit = (router, src) => {
    const c = env(src, router);
    /* the victim is the FIRST row, so the pre-fix global scan can be reproduced */
    const victim = post(c, { kind: "application", consent: true, website: "",
      submission_id: "application-victim", fields: base });
    /* an unrelated person plants the victim's reference as a free-text key */
    const attacker = post(c, { kind: "application", consent: true, website: "",
      submission_id: "application-attacker",
      fields: Object.assign({}, base, { email: "attacker@example.test",
        submission_id: victim.reference }) });
    /* a third, unrelated person sends that same value */
    const third = post(c, { kind: "application", consent: true, website: "",
      submission_id: victim.reference,
      fields: Object.assign({}, base, { email: "third@example.test" }) });
    return { c, victim, attacker, third, rows: c.__tabs.applications.getLastRow() - 1,
      mails: c.__sent.length, first: det(c, 1), second: det(c, 2) };
  };

  for (const router of ROUTERS) {
    /* ---------------- BEFORE: the real pre-fix file -------------------------- */
    const b = exploit(router, PRE);
    check("A2 [" + router + "] BEFORE: a first submission stores no retry key (the original audit finding)",
      b.first && b.first.submission_id === undefined, JSON.stringify(b.first));
    check("A2 [" + router + "] BEFORE: a planted value DOES become the dedupe key",
      b.second && b.second.submission_id === b.victim.reference, JSON.stringify(b.second));
    check("A2 [" + router + "] BEFORE: a stranger sending that value is told 'already received'",
      b.third.duplicate === true, JSON.stringify(b.third));
    check("A2 [" + router + "] BEFORE: so the stranger is silently NOT stored",
      b.rows === 2, b.rows);
    check("A2 [" + router + "] BEFORE: and receives no acknowledgement email",
      b.mails === 2, b.mails);

    /* each half on its own, so the suite names which one is load-bearing */
    const onlyM1 = exploit(router, M1);
    check("A2 [" + router + "] M1 alone is not enough to suppress a stranger (the reservation still holds)",
      onlyM1.third.duplicate === false, JSON.stringify(onlyM1.third));
    const onlyM3 = exploit(router, M3);
    check("A2 [" + router + "] M3 alone: no retry key is stored at all (the insert-write fix is load-bearing)",
      onlyM3.first && onlyM3.first.submission_id === undefined, JSON.stringify(onlyM3.first));
    check("A2 [" + router + "] M3 alone: the reservation still keeps the planted value out of the key",
      onlyM3.second && onlyM3.second.submission_id === undefined &&
      onlyM3.second.sent_submission_id === onlyM3.victim.reference, JSON.stringify(onlyM3.second));
    check("A2 [" + router + "] M3 alone: and the stranger is still not suppressed",
      onlyM3.third.duplicate === false, JSON.stringify(onlyM3.third));

    /* ---------------- AFTER: the shipped build ------------------------------- */
    const a = exploit(router, CUR);
    check("A2 [" + router + "] AFTER: the applicant's own retry key is stored",
      a.first && a.first.submission_id === "application-victim", JSON.stringify(a.first));
    check("A2 [" + router + "] AFTER: a planted value is not the dedupe key",
      a.second && a.second.submission_id === "application-attacker", JSON.stringify(a.second));
    check("A2 [" + router + "] AFTER: the planted value is recorded inertly instead",
      a.second && a.second.sent_submission_id === a.victim.reference, JSON.stringify(a.second));
    check("A2 [" + router + "] AFTER: the stranger is not suppressed",
      a.third.duplicate === false, JSON.stringify(a.third));
    check("A2 [" + router + "] AFTER: the stranger is stored",
      a.rows === 3, a.rows);
    check("A2 [" + router + "] AFTER: the stranger is acknowledged",
      a.mails === 3, a.mails);
    check("A2 [" + router + "] AFTER: the victim's row is untouched",
      rowObj(a.c, 1).email === "legit@example.test", rowObj(a.c, 1).email);

    /* a guessed id: plant it, then a stranger uses the same value */
    const g = env(CUR, router);
    post(g, { kind: "application", consent: true, website: "", submission_id: "shared-guess", fields: base });
    post(g, { kind: "application", consent: true, website: "",
      submission_id: "shared-guess", fields: Object.assign({}, base, { email: "b@example.test" }) });
    const str = post(g, { kind: "application", consent: true, website: "",
      submission_id: "shared-guess", fields: Object.assign({}, base, { email: "c@example.test" }) });
    check("A2 [" + router + "] a guessed id does not suppress a third person",
      str.duplicate === false && g.__tabs.applications.getLastRow() - 1 === 3,
      "dup=" + str.duplicate + " rows=" + (g.__tabs.applications.getLastRow() - 1));

    /* ---------------- the feature the id exists for ------------------------- */
    const r = env(CUR, router);
    const r1 = post(r, { kind: "application", consent: true, website: "", submission_id: "application-retry", fields: base });
    const rowsBefore = r.__tabs.applications.getLastRow(), mailsBefore = r.__sent.length;
    const r2 = post(r, { kind: "application", consent: true, website: "", submission_id: "application-retry", fields: base });
    check("A2 [" + router + "] a duplicate retry creates no second row",
      r.__tabs.applications.getLastRow() === rowsBefore, r.__tabs.applications.getLastRow());
    check("A2 [" + router + "] a duplicate retry sends no second acknowledgement",
      r.__sent.length === mailsBefore, r.__sent.length);
    check("A2 [" + router + "] the retry reports duplicate with the same reference",
      r2.duplicate === true && r2.reference === r1.reference, JSON.stringify(r2));

    /* ---------------- a legitimate resubmission ----------------------------- */
    const u = env(CUR, router);
    const u1 = post(u, { kind: "application", consent: true, website: "", submission_id: "application-u1", fields: base });
    const u2 = post(u, { kind: "application", consent: true, website: "", submission_id: "application-u2",
      fields: Object.assign({}, base, { city: "Nashik" }) });
    check("A2 [" + router + "] a legitimate resubmission updates the same row",
      u.__tabs.applications.getLastRow() - 1 === 1 && u2.duplicate === true && u2.updated === true,
      JSON.stringify(u2));
    check("A2 [" + router + "] the edit lands and the reference is kept",
      rowObj(u, 1).city === "Nashik" && u2.reference === u1.reference, JSON.stringify(u2));
    check("A2 [" + router + "] a resubmission sends no extra acknowledgement",
      u.__sent.length === 1, u.__sent.length);
    /* and it must not erase answers the applicant left untouched this time */
    const p = env(CUR, router);
    post(p, { kind: "application", consent: true, website: "", submission_id: "application-p1",
      fields: Object.assign({}, base, { headline: "Hindi for beginners", currency: "INR", duration: "90 min" }) });
    post(p, { kind: "application", consent: true, website: "", submission_id: "application-p2",
      fields: Object.assign({}, base, { city: "Mumbai" }) });
    check("A2 [" + router + "] existing applicant data survives a resubmission",
      rowObj(p, 1).headline === "Hindi for beginners" && rowObj(p, 1).currency === "INR" &&
      rowObj(p, 1).duration === "90 min" && rowObj(p, 1).city === "Mumbai",
      JSON.stringify({ h: rowObj(p, 1).headline, c: rowObj(p, 1).currency, d: rowObj(p, 1).duration }));
  }

  /* the lookup must fail closed rather than fall back to a tab-wide scan */
  /* Fail-closed, proved without relying on a throw: the stored row carries the
     id, so a lookup that ignored the missing scope would return its reference
     and a lookup that respects it returns "". */
  check("A2 the retry lookup refuses to match without a server-resolved scope", (() => {
    try {
      const c = env(CUR, "unified");
      post(c, { kind: "application", consent: true, website: "", submission_id: "application-x", fields: base });
      const tab = c.__tabs.applications;
      const map = c.ekHeaderMap_(tab).map;
      const withScope = c.ekFindSubmission_(tab, map, "application-x", { row: 2 });
      const noScope = c.ekFindSubmission_(tab, map, "application-x", null);
      return /^EG-/.test(String(withScope)) && noScope === "";
    } catch (e) { return false; }
  })());
  check("A2 the retry lookup only honours the caller's own row", (() => {
    try {
      const c = env(CUR, "unified");
      post(c, { kind: "application", consent: true, website: "", submission_id: "application-row2", fields: base });
      post(c, { kind: "application", consent: true, website: "", submission_id: "application-row3",
        fields: Object.assign({}, base, { email: "other@example.test" }) });
      const tab = c.__tabs.applications;
      const map = c.ekHeaderMap_(tab).map;
      /* row 3's id, asked for with row 2's scope, must not match */
      return c.ekFindSubmission_(tab, map, "application-row3", { row: 2 }) === "" &&
             /^EG-/.test(String(c.ekFindSubmission_(tab, map, "application-row3", { row: 3 })));
    } catch (e) { return false; }
  })());
}
console.log("\n" + (fail ? fail + " FAILURE(S)" : "ALL CHECKS PASSED") + "  (" + pass + " passed, " + fail + " failed)");
process.exit(fail ? 1 : 0);

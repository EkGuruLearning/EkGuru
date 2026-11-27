/* =========================================================
   EkGuru — end-to-end application pipeline
   ---------------------------------------------------------
   Proves the WHOLE path the task asks about, with no network and no
   production Sheet:

     join.html form  ->  join-wizard.js buildPayload()
                     ->  js/intake.js request body
                     ->  Apps Script doPost()  (Unified.gs router)
                     ->  ekValidateApplication_ / ekBuildRow_ (ApplicationIntake.gs)
                     ->  one Google Sheets row, 69 columns

   Nothing is mocked except the Google services themselves, which are
   stubbed exactly as the other suites stub them. The payload comes from the
   REAL wizard, not a hand-written fixture — that is the point, because a
   hand-written fixture cannot catch the form and the schema drifting apart.

   Run: node tests/integration/test-application-pipeline.mjs
   ========================================================= */
import fs from "node:fs";
import vm from "node:vm";
import path from "node:path";
import { fileURLToPath } from "node:url";
import jsdomPkg from "jsdom";

const { JSDOM } = jsdomPkg;
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8");

let pass = 0, fail = 0;
const check = (n, c, e) => {
  if (c) pass++; else fail++;
  console.log((c ? "PASS  " : "FAIL  ") + n + (c ? "" : "  ->  " + (e === undefined ? "" : e)));
};
const wait = (ms = 220) => new Promise((r) => setTimeout(r, ms));

/* ------------------------------------------------------------ sheet stub */
function makeSheet(name, grid) {
  const s = {
    __name: name, grid: grid || [],
    getName: () => name, getSheetId: () => 1, getIndex: () => 1,
    getLastRow() { for (let r = s.grid.length - 1; r >= 0; r--) if (s.grid[r] && s.grid[r].some((c) => c !== "" && c != null)) return r + 1; return 0; },
    getLastColumn() { let m = 0; for (const row of s.grid) { let l = 0; for (let c = 0; c < (row || []).length; c++) if (row[c] !== "" && row[c] != null) l = c + 1; if (l > m) m = l; } return m; },
    getMaxRows: () => 999, getMaxColumns: () => 80, setFrozenRows() {}, clearContents() {},
    getDataRange() { return this.getRange(1, 1, Math.max(1, s.getLastRow()), Math.max(1, s.getLastColumn())); },
    getRange(row, col, nr = 1, nc = 1) {
      return {
        getValues() { const o = []; for (let i = 0; i < nr; i++) { const L = []; for (let j = 0; j < nc; j++) { const rw = s.grid[row - 1 + i] || []; L.push(rw[col - 1 + j] === undefined ? "" : rw[col - 1 + j]); } o.push(L); } return o; },
        getDisplayValues() { return this.getValues().map((x) => x.map(String)); },
        getValue() { return this.getValues()[0][0]; },
        setValues(v) { for (let i = 0; i < v.length; i++) for (let j = 0; j < v[i].length; j++) { const rr = row - 1 + i; if (!s.grid[rr]) s.grid[rr] = []; s.grid[rr][col - 1 + j] = v[i][j]; } return this; },
        setValue(v) { return this.setValues([[v]]); },
        setBackground() { return this; }, setFontWeight() { return this; }, setNumberFormat() { return this; },
        setDataValidation() { return this; }, setWrap() { return this; },
      };
    },
    appendRow(v) { const at = s.getLastRow(); if (!s.grid[at]) s.grid[at] = []; for (let c = 0; c < v.length; c++) s.grid[at][c] = v[c]; },
  };
  return s;
}

function makeBackend() {
  const S = { console, Logger: { log() {} } };
  const tabs = {
    applications: makeSheet("applications", []),
    bookings: makeSheet("bookings", [["timestamp"]]),
    contacts: makeSheet("contacts", [["timestamp"]]),
    signups: makeSheet("signups", [["timestamp"]]),
    reviews_pending: makeSheet("reviews_pending", [["timestamp"]]),
    tutors: makeSheet("tutors", [["name", "approved", "city", "whatsapp", "email"], ["Asha", "yes", "Pune", "+919876543210", "asha@example.test"]]),
  };
  const ss = { getSheetByName: (n) => tabs[n] || null, insertSheet: (n) => (tabs[n] = makeSheet(n, [])), getSheets: () => Object.values(tabs), getId: () => "ss" };
  const P = {};
  const mails = [];
  Object.assign(S, {
    SpreadsheetApp: { getActiveSpreadsheet: () => ss, openById: () => ss, getActive: () => ss, flush() {} },
    PropertiesService: { getScriptProperties: () => ({ getProperty: (k) => (P[k] === undefined ? null : P[k]), setProperty: (k, v) => { P[k] = v; }, deleteProperty: (k) => { delete P[k]; }, getProperties: () => ({ ...P }) }) },
    CacheService: { getScriptCache: () => ({ get: () => null, put() {}, remove() {} }) },
    LockService: { getScriptLock: () => ({ tryLock: () => true, waitLock() {}, releaseLock() {} }) },
    GmailApp: { sendEmail: (o) => { mails.push(o); }, getAliases: () => [] },
    MailApp: { sendEmail: (o) => { mails.push(o); } },
    Utilities: { formatDate: (x) => String(x), base64Encode: (x) => String(x), computeDigest: () => [1], DigestAlgorithm: { SHA_256: "s" } },
    ContentService: { MimeType: { JSON: "j", TEXT: "t" }, createTextOutput: (x) => ({ getContent: () => x, setMimeType() { return this; }, getMimeType: () => "t" }) },
    HtmlService: { createHtmlOutput: (x) => ({ getContent: () => x }) },
    ScriptApp: { getService: () => ({ getUrl: () => "u" }) },
  });
  vm.createContext(S);
  for (const f of ["apps-script/ApplicationSchema.gs", "apps-script/ApplicationIntake.gs", "apps-script/Unified.gs"]) {
    vm.runInContext(read(f), S, { filename: f });
  }
  S.__tabs = tabs; S.__mails = mails;
  return S;
}

/* ------------------------------------------------------------ wizard stub */
async function bootWizard() {
  const dom = new JSDOM(read("join.html"), {
    url: "http://localhost/join.html", runScripts: "dangerously", pretendToBeVisual: true,
    beforeParse(w) {
      w.matchMedia = () => ({ matches: false, addListener() {}, addEventListener() {}, removeEventListener() {} });
      w.fetch = () => Promise.reject(new Error("offline in tests"));
      w.scrollTo = () => {};
    },
  });
  const d = dom.window.document, w = dom.window;
  for (const f of ["js/site-config.js", "js/intake.js", "js/sheet.js", "js/join-schema.js", "js/join-wizard.js"]) {
    const s = d.createElement("script"); s.textContent = read(f); d.body.appendChild(s);
  }
  await wait(350);
  return { d, w, dom };
}

const set = (d, w, el, v) => { el.value = v; el.dispatchEvent(new w.Event("input", { bubbles: true })); el.dispatchEvent(new w.Event("change", { bubbles: true })); };

/* Fill the form the way a real tutor would, using each select's real options. */
function fillForm(d, w) {
  d.querySelectorAll("input,select,textarea").forEach((el) => {
    const n = el.getAttribute("name");
    if (!n || el.disabled || el.value) return;
    if (el.type === "checkbox") { if (!el.closest(".jw-day")) { el.checked = true; el.dispatchEvent(new w.Event("change", { bubbles: true })); } return; }
    if (el.type === "radio") return;
    if (el.type === "email") set(d, w, el, "asha@example.test");
    else if (el.type === "number") set(d, w, el, "12");
    else if (el.type === "tel") set(d, w, el, "+91 98765 43210");
    else if (el.type === "time") set(d, w, el, n.includes("to") ? "21:00" : "19:00");
    else if (el.type === "url") set(d, w, el, "https://example.com/me.jpg");
    else if (n === "edu_year") set(d, w, el, "2018");
    else if (n === "online_years") set(d, w, el, "4");
    else if (el.tagName === "SELECT") { const o = [...el.options].find((x) => x.value); if (o) set(d, w, el, o.value); }
    else set(d, w, el, "A real answer typed by a tutor");
  });
  /* Chip groups (subjects / levels / methods / teachLangs) each need at least
     one tick before the step is valid, and `subject` is DERIVED from them. */
  d.querySelectorAll("[data-need-min]").forEach((grp) => {
    const box = grp.querySelector('input[type="checkbox"]');
    if (box && !box.checked) { box.checked = true; box.dispatchEvent(new w.Event("change", { bubbles: true })); }
  });
  const mon = d.querySelector('[data-day="Mon"] input[type=checkbox]');
  if (mon) { mon.checked = true; mon.dispatchEvent(new w.Event("change", { bubbles: true })); }
  const mf = d.querySelector('[name="mon-from"]'), mt = d.querySelector('[name="mon-to"]');
  if (mf) set(d, w, mf, "19:00");
  if (mt) set(d, w, mt, "21:00");
}

console.log("=== application pipeline: wizard -> intake -> doPost -> sheet ===");

/* ---------------------------------------------------- 1. schema/form agreement */
{
  const { d, w, dom } = await bootWizard();
  const F = w.EKGURU_APP_SCHEMA.fields;
  let checked = 0, bad = [];
  ["years", "edu_qual", "hindi_level", "english_level", "duration", "trial", "timezone", "currency", "contact_pref"].forEach((name) => {
    const sel = d.querySelector(`select[name="${name}"]`);
    if (!sel) return;
    const f = F.find((x) => x.col === name);
    const allowed = f && f.values ? f.values : null;
    if (!allowed) return;
    [...sel.options].forEach((o) => {
      if (o.value === "") return;                    /* placeholder, never sent */
      checked++;
      const norm = (x) => String(x).replace(/[\u2010-\u2015]/g, "-").toLowerCase();
      if (!allowed.map(norm).includes(norm(o.value))) bad.push(`${name}: ${JSON.stringify(o.value)}`);
    });
  });
  check(`every dropdown option the form can submit is a legal schema value (${checked} checked)`,
    bad.length === 0 && checked > 40, bad.join(" | ") || "only " + checked + " checked");
  dom.window.close();
}

/* ---------------------------------------------------- 2. payload -> row */
let payloadFor;
{
  const { d, w, dom } = await bootWizard();
  fillForm(d, w);
  const payload = w.EkGuruJoinWizard.buildPayload(d.querySelector("#jw-form"));
  payloadFor = payload;

  const F = w.EKGURU_APP_SCHEMA.fields;
  const legit = new Set(F.map((f) => f.col).concat(F.map((f) => f.src).filter(Boolean)));
  const orphan = Object.keys(payload).filter((k) => !legit.has(k) && k !== "details" && k !== "availability_slots" && k !== "availability_meta");
  check("every payload key maps to a schema column (no invented fields)", orphan.length === 0, orphan.join(", "));
  check("availability is sent as slots + a human line",
    Array.isArray(payload.availability_slots) && payload.availability_slots.length === 1 && /Mon 19:00-21:00/.test(payload.availability || ""),
    JSON.stringify(payload.availability_slots));
  check("consent is NOT smuggled inside fields", payload.consent === undefined);

  const S = makeBackend();
  const body = JSON.stringify({ kind: "application", consent: true, website: "", submission_id: "pipe-1", fields: payload });
  const res = JSON.parse(S.doPost({ postData: { contents: body } }).getContent());

  check("backend accepts the real wizard payload", res.ok === true, JSON.stringify(res).slice(0, 140));
  check("backend returns a reference only after the row is written",
    /^EG-[A-Z0-9]+$/.test(res.reference || ""), res.reference);
  check("exactly one row was written for one submission",
    S.__tabs.applications.getLastRow() === 2, "lastRow=" + S.__tabs.applications.getLastRow());

  const grid = S.__tabs.applications.grid;
  const header = grid[0] || [], row = grid[1] || [];
  check("the header is the 69-column schema", header.length === 69, header.length);

  const col = (k) => row[header.indexOf(k)];
  check("name / email / city / country reached the sheet",
    col("name") && col("email") === "asha@example.test" && col("city") && col("country"));
  check("reference and status are set by the server",
    /^EG-/.test(String(col("reference"))) && col("status") === "pending", JSON.stringify([col("reference"), col("status")]));
  check("schema_version is stamped", col("schema_version") === "2.1.0", col("schema_version"));
  check("availability text reached its legacy column", /Mon 19:00-21:00/.test(String(col("availability"))), col("availability"));
  check("WhatsApp was stored privately on the row", /^\+?[0-9]{7,15}$/.test(String(col("whatsapp"))), col("whatsapp"));

  /* the security invariant: the private number must not reach the public feed */
  const feed = S.doGet({ parameter: { tab: "tutors" } }).getContent();
  check("WhatsApp does NOT appear in the public tutor feed", !/9876543210/.test(feed), feed.slice(0, 90));
  check("applicant email does NOT appear in the public tutor feed", !/asha@example\.test/.test(feed));

  /* no data lost: every non-empty payload key is either a column value or in details */
  const details = col("details_json") ? JSON.parse(col("details_json")) : {};
  const lost = Object.keys(payload).filter((k) => {
    if (k === "details" || k === "availability_slots" || k === "availability_meta") return false;
    const v = payload[k];
    if (v === "" || v == null || (Array.isArray(v) && !v.length)) return false;
    const f = F.find((x) => x.src === k);
    const colName = f ? f.col : k;
    if (String(col(colName) || "").trim() !== "") return false;
    if (details[k] != null && String(details[k]).trim() !== "") return false;
    return true;
  });
  check("no typed value is silently dropped (column or details_json)", lost.length === 0, lost.join(", "));

  /* duplicates: the same submission_id must not make a second row */
  const before = S.__tabs.applications.getLastRow();
  const res2 = JSON.parse(S.doPost({ postData: { contents: body } }).getContent());
  check("a retried submission does not create a second row",
    S.__tabs.applications.getLastRow() === before, "rows went " + before + " -> " + S.__tabs.applications.getLastRow());
  check("the retry is answered as a duplicate with the same reference",
    res2.duplicate === true && res2.reference === res.reference, JSON.stringify(res2).slice(0, 120));
  dom.window.close();
}

/* ---------------------------------------------------- 3. failure + retry */
{
  const { d, w, dom } = await bootWizard();
  fillForm(d, w);
  const S = makeBackend();
  const body = JSON.stringify({ kind: "application", consent: true, website: "", submission_id: "pipe-bad",
    fields: Object.assign({}, payloadFor, { email: "not-an-email" }) });
  const bad = JSON.parse(S.doPost({ postData: { contents: body } }).getContent());
  check("an invalid field is rejected, not written", bad.ok === false && S.__tabs.applications.getLastRow() === 0,
    JSON.stringify(bad).slice(0, 120));
  check("the rejection names the field so it can be shown inline", !!bad.fields && !!bad.fields.email, JSON.stringify(bad.fields));

  const good = JSON.parse(S.doPost({ postData: { contents: JSON.stringify({ kind: "application", consent: true, website: "", submission_id: "pipe-bad", fields: payloadFor }) } }).getContent());
  check("retrying after the fix succeeds and writes exactly one row",
    good.ok === true && S.__tabs.applications.getLastRow() === 2, JSON.stringify([good.ok, S.__tabs.applications.getLastRow()]));
  dom.window.close();
}

/* ---------------------------------------------------- 4. honeypot */
{
  const S = makeBackend();
  const bot = JSON.parse(S.doPost({ postData: { contents: JSON.stringify({ kind: "application", consent: true, website: "http://spam", submission_id: "bot-1", fields: payloadFor }) } }).getContent());
  check("honeypot writes no row", S.__tabs.applications.getLastRow() === 0, S.__tabs.applications.getLastRow());
  check("honeypot sends no email", S.__mails.length === 0, S.__mails.length);
  check("honeypot still answers with a believable success", bot.ok === true && /^EG-/.test(bot.reference || ""), JSON.stringify(bot));
}

console.log("\n" + (fail ? fail + " FAILURE(S)" : "ALL CHECKS PASSED") + "  (" + pass + " passed, " + fail + " failed)");
process.exit(fail ? 1 : 0);

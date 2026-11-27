/* =========================================================
   EkGuru — consolidation test for apps-script/combined/Code.gs
   ---------------------------------------------------------
   The single-file backend is generated from three sources. This suite proves
   the generated file is (a) complete, (b) collision-free, (c) behaviourally
   identical to the three files loaded separately.

   Nothing here touches Google services: every check runs against the mocked
   SpreadsheetApp/Gmail/etc. environment below, as the other suites do.

   Run: node tests/integration/test-combined-code.mjs
   Rebuild the file with: node tools/build-combined-code.mjs
   ========================================================= */
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8");
let pass = 0, fail = 0;
const check = (n, c, e) => {
  if (c) pass++; else fail++;
  console.log((c ? "PASS  " : "FAIL  ") + n + (c ? "" : "  ->  " + (e === undefined ? "" : e)));
};

const COMBINED = "apps-script/combined/Code.gs";
const SOURCES = ["apps-script/ApplicationSchema.gs", "apps-script/ApplicationIntake.gs", "apps-script/Unified.gs"];

/* ------------------------------------------------------------------ mocks */
const LEGACY17 = ["timestamp", "reference", "status", "approved", "name", "email", "city", "country",
  "subject", "experience", "rate_usd", "availability", "bio", "photo_link", "video_link", "languages", "notes"];
const makeSheet = (name, grid) => {
  const s = {
    __name: name, grid: grid || [],
    getName() { return name; },
    getSheetId() { return s.gid || 1000; },
    getIndex() { return 1; },
    getLastRow() {
      for (let r = s.grid.length - 1; r >= 0; r--) if (s.grid[r] && s.grid[r].some((c) => c !== "" && c != null)) return r + 1;
      return 0;
    },
    getLastColumn() {
      let m = 0;
      for (const row of s.grid) { let l = 0; for (let c = 0; c < (row || []).length; c++) if (row[c] !== "" && row[c] != null) l = c + 1; if (l > m) m = l; }
      return m;
    },
    getMaxRows: () => 999, getMaxColumns: () => 80,
    setFrozenRows() {}, clearContents() {},
    getDataRange() { return this.getRange(1, 1, Math.max(1, s.getLastRow()), Math.max(1, s.getLastColumn())); },
    getRange(row, col, nr = 1, nc = 1) {
      return {
        getValues() {
          const o = [];
          for (let r = 0; r < nr; r++) { const line = []; for (let c = 0; c < nc; c++) { const rw = s.grid[row - 1 + r] || []; line.push(rw[col - 1 + c] === undefined ? "" : rw[col - 1 + c]); } o.push(line); }
          return o;
        },
        getDisplayValues() { return this.getValues().map((r) => r.map((v) => String(v))); },
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

function env(files) {
  const t = {
    applications: makeSheet("applications", [LEGACY17.slice()]),
    contacts: makeSheet("contacts", [["timestamp", "reference"]]),
    bookings: makeSheet("bookings", [["timestamp", "booking_ref"]]),
    signups: makeSheet("signups", [["timestamp", "email"]]),
    reviews_pending: makeSheet("reviews_pending", [["timestamp", "reference"]]),
    tutors: makeSheet("tutors", [
      ["name", "approved", "city", "whatsapp", "email", "bio"],
      ["Asha", "yes", "Pune", "+919876543210", "asha@example.test", "Hindi tutor"],
    ]),
  };
  t.tutors.gid = 1631273256;
  const store = {}, P = { EK_ADMIN_TOKEN: "tok" }, sent = [];
  const ss = {
    getSheetByName: (n) => t[n] || null,
    insertSheet: (n) => { t[n] = makeSheet(n, []); return t[n]; },
    getSheets: () => Object.keys(t).map((k) => t[k]),
    getId: () => "ssid",
  };
  const ctx = {
    console, Logger: { log: () => {} },
    SpreadsheetApp: {
      getActiveSpreadsheet: () => ss, openById: () => ss, getActive: () => ss, flush() {},
      getUi: () => ({ createMenu: () => ({ addItem: () => ({ addItem: () => ({ addToUi() {} }), addToUi() {} }), addToUi() {} }), alert() {} }),
    },
    PropertiesService: { getScriptProperties: () => ({ getProperty: (k) => (P[k] === undefined ? null : P[k]), setProperty: (k, v) => { P[k] = v; }, deleteProperty: (k) => { delete P[k]; }, getProperties: () => Object.assign({}, P) }) },
    CacheService: { getScriptCache: () => ({ get: (k) => (store[k] === undefined ? null : store[k]), put: (k, v) => { store[k] = String(v); }, remove: (k) => { delete store[k]; } }) },
    LockService: { getScriptLock: () => ({ tryLock: () => true, waitLock() {}, releaseLock() {} }) },
    GmailApp: { sendEmail: (to) => { sent.push(String(to)); }, getAliases: () => [] },
    MailApp: { sendEmail: (o) => { sent.push(String(o.to)); } },
    Utilities: {
      formatDate: (d) => (d instanceof Date ? d : new Date(d)).toISOString(),
      base64Encode: (x) => Buffer.from(String(x)).toString("base64"),
      computeDigest: () => [1], DigestAlgorithm: { SHA_256: "sha" },
    },
    ContentService: { MimeType: { JSON: "json", TEXT: "text" }, createTextOutput: (x) => { let m = "text"; const o = { getContent: () => x, setMimeType: (v) => { m = v; return o; }, getMimeType: () => m }; return o; } },
    HtmlService: { createHtmlOutput: (x) => ({ getContent: () => x }) },
    ScriptApp: { getService: () => ({ getUrl: () => "https://script.google.test/exec" }) },
  };
  ctx.__tabs = t; ctx.__sent = sent;
  vm.createContext(ctx);
  for (const f of files) vm.runInContext(read(f), ctx, { filename: f });
  return ctx;
}

const post = (c, body) => JSON.parse(c.doPost({ postData: { contents: JSON.stringify(body) } }).getContent());
const rawGet = (c, p) => c.doGet({ parameter: p }).getContent();
/* two separate runs must be comparable despite Date.now()/new Date() */
const scrub = (s) => String(s)
  .replace(/"(at|created_at|updated_at|consent_at|email_sent_at|reviewed_at)":"[^"]*"/g, '"$1":"<t>"')
  .replace(/\d{4}-\d{2}-\d{2}T[\d:.]+Z/g, "<t>");

const BASE = {
  name: "Asha V", email: "asha@example.test", city: "Pune", country: "India",
  subject: "Hindi", bio: "A real introduction here.", rate_usd: "12",
  timezone: "Asia/Kolkata", availability_slots: [{ day: "Mon", from: "19:00", to: "21:00" }],
};

console.log("=== consolidation — combined/Code.gs ===");

/* -------------------------------------------------- 1. completeness */
{
  const combined = read(COMBINED);
  let missing = [];
  let strictKept = false;
  for (const p of SOURCES) {
    const src = read(p);
    let seen = false;
    for (const line of src.split("\n")) {
      if (line.trim() === '"use strict";' && !seen) { seen = true; strictKept = true; continue; }
      if (line.trim() === "") continue;
      if (!combined.includes(line)) missing.push(p + ": " + line.slice(0, 70));
    }
  }
  check("every source line is present verbatim in Code.gs", missing.length === 0, missing.slice(0, 3).join(" | "));
  check("exactly one \"use strict\" directive survives", (combined.match(/^"use strict";/gm) || []).length === 1);
  check("exactly one doGet()", (combined.match(/^function doGet\(/gm) || []).length === 1);
  check("exactly one doPost()", (combined.match(/^function doPost\(/gm) || []).length === 1);
  check("has the three part banners",
    /PART 1 of 3 — SCHEMA/.test(combined) && /PART 2 of 3 — APPLICATION BACKEND/.test(combined) && /PART 3 of 3 — UNIFIED ROUTER/.test(combined));
  check("warns it is not the payments project", /NOT the payments project/.test(combined));
  check("explains the PART vs Unified.gs SECTION numbering",
    /NOTE ON NUMBERING/.test(combined));
}

/* -------------------------------------------------- 2. no duplicate declarations */
{
  const combined = read(COMBINED);
  const fns = (combined.match(/^function [A-Za-z0-9_]+/gm) || []).map((s) => s.replace("function ", ""));
  const dupFns = fns.filter((f, i) => fns.indexOf(f) !== i);
  check("no duplicate function declarations", dupFns.length === 0, dupFns.join(", "));

  const vars = (combined.match(/^var [A-Za-z0-9_]+/gm) || []).map((s) => s.replace("var ", ""));
  const dupVars = vars.filter((v, i) => vars.indexOf(v) !== i);
  check("no duplicate top-level var declarations", dupVars.length === 0, dupVars.join(", "));

  const trioFns = SOURCES
    .map((p) => (read(p).match(/^function [A-Za-z0-9_]+/gm) || []).map((s) => s.replace("function ", "")))
    .flat().sort();
  check("function inventory matches the three sources exactly",
    JSON.stringify(trioFns) === JSON.stringify(fns.slice().sort()),
    trioFns.length + " vs " + fns.length);
}

/* -------------------------------------------------- 3. behaviour equivalence */
{
  const trio = env(SOURCES);
  const comb = env([COMBINED]);

  const routes = [
    ["?action=health", { action: "health" }],
    ["bare /exec", {}],
    ["?tab=health", { tab: "health" }],
    ["?tab=tutors (CSV)", { tab: "tutors" }],
    ["?tab=tutors&format=json", { tab: "tutors", format: "json" }],
    ["?tab=settings", { tab: "settings" }],
    ["?tab=unknown", { tab: "nope" }],
    ["?action=ping (bad token)", { action: "ping", token: "x" }],
  ];
  for (const [label, p] of routes) {
    const a = scrub(rawGet(trio, p)), b = scrub(rawGet(comb, p));
    check("GET " + label + " is byte-identical", a === b, "trio: " + a.slice(0, 90) + " | combined: " + b.slice(0, 90));
  }

  const s1 = post(trio, { kind: "application", consent: true, website: "", submission_id: "app-1", fields: BASE });
  const s2 = post(comb, { kind: "application", consent: true, website: "", submission_id: "app-1", fields: BASE });
  check("submit: same ok/duplicate/mail outcome",
    s1.ok === s2.ok && s1.duplicate === s2.duplicate && s1.mail === s2.mail,
    JSON.stringify([s1.duplicate, s2.duplicate, s1.mail, s2.mail]));
  check("submit: same row count", trio.__tabs.applications.getLastRow() === comb.__tabs.applications.getLastRow());
  check("submit: same email count", trio.__sent.length === comb.__sent.length);

  const dj = (c) => {
    const t = c.__tabs.applications;
    return (t.grid[1] || [])[t.grid[0].indexOf("details_json")] || "";
  };
  check("submit: details_json carries the same keys",
    JSON.stringify(Object.keys(JSON.parse(dj(trio) || "{}")).sort()) ===
    JSON.stringify(Object.keys(JSON.parse(dj(comb) || "{}")).sort()),
    dj(trio) + " | " + dj(comb));
}

/* -------------------------------------------------- 4. security invariants */
{
  const comb = env([COMBINED]);

  const csv = rawGet(comb, { tab: "tutors" });
  check("public tutor CSV never carries whatsapp", !/9876543210/.test(csv) && !/whatsapp/i.test(csv), csv);
  check("public tutor CSV never carries email", !/asha@example\.test/i.test(csv));

  const bot = post(comb, { kind: "application", consent: true, consent_privacy: true, website: "http://spam",
    submission_id: "app-bot", fields: Object.assign({}, BASE, { email: "bot@spam.test" }) });
  /* the fixture sheet starts with its LEGACY17 header row, so "no data rows"
     is getLastRow() === 1, not 0 */
  check("honeypot writes no row", comb.__tabs.applications.getLastRow() === 1, comb.__tabs.applications.getLastRow());
  check("honeypot sends no email", comb.__sent.length === 0, comb.__sent.length);
  check("honeypot still answers with a pretend success",
    bot.ok === true && /^EG-/.test(bot.reference || ""), JSON.stringify(bot));

  const a = post(comb, { kind: "application", consent: true, website: "", submission_id: "app-retry", fields: BASE });
  const b = post(comb, { kind: "application", consent: true, website: "", submission_id: "app-retry", fields: BASE });
  check("retry dedupes to one data row", comb.__tabs.applications.getLastRow() === 2, comb.__tabs.applications.getLastRow());
  check("retry sends no second email", comb.__sent.length === 1, comb.__sent.length);
  check("retry reports the same reference", b.duplicate === true && b.reference === a.reference, JSON.stringify(b));

  const before = comb.__tabs.applications.getLastRow();
  const stranger = post(comb, { kind: "application", consent: true, website: "", submission_id: "app-planted",
    fields: Object.assign({}, BASE, { email: "stranger@example.test" }) });
  check("a planted/guessed id cannot suppress a stranger",
    stranger.duplicate === false && comb.__tabs.applications.getLastRow() === before + 1,
    JSON.stringify(stranger) + " rows=" + comb.__tabs.applications.getLastRow());

  check("retry lookup fails closed without a server-resolved scope",
    comb.ekFindSubmission_(comb.__tabs.applications, comb.ekHeaderMap_(comb.__tabs.applications).map, "app-retry", null) === "");
}

/* -------------------------------------------------- 5. schema intact */
{
  const comb = env([COMBINED]);
  check("schema version 2.1.0", comb.EKGURU_SCHEMA_VERSION === "2.1.0", comb.EKGURU_SCHEMA_VERSION);
  check("69 logical fields", comb.EKGURU_APPLICATION_FIELDS.length === 69, comb.EKGURU_APPLICATION_FIELDS.length);
  check("69 header columns", comb.EKGURU_APPLICATION_HEADER.length === 69, comb.EKGURU_APPLICATION_HEADER.length);
  check("the legacy 17 columns are still first, in order",
    JSON.stringify(comb.EKGURU_APPLICATION_HEADER.slice(0, 17)) === JSON.stringify(LEGACY17));
}

/* -------------------------------------------------- 6. contracts available */
{
  const comb = env([COMBINED]);
  const required = [
    "doGet", "doPost", "onOpen", "onEdit", "selfTest_", "installTriggers", "clearFeedCache",
    "feedGet_", "intakePost_", "intakeHealth_", "intakeQuota_", "markContactReplied_",
    "ekApplicationAction_", "ekApplicationGet_", "ekHealth_", "ekApplicationQuota_",
    "ekMigrateApplications", "ekValidateApplication_", "ekBuildRow_", "ekFindSubmission_",
    "ekAdminUpdate_", "ekSendApplicationMail_", "ekStatusLookup_", "intakeSpreadsheet_",
  ];
  const absent = required.filter((f) => typeof comb[f] !== "function");
  check("all " + required.length + " public/entry-point functions survive consolidation",
    absent.length === 0, absent.join(", "));

  const ref = (() => { const t = comb.__tabs.applications; return null; })();
  post(comb, { kind: "application", consent: true, website: "", submission_id: "app-adm", fields: BASE });
  const t = comb.__tabs.applications, h = t.grid[0];
  const rowRef = t.grid[1][h.indexOf("reference")];
  const adm = post(comb, { action: "ekAdminUpdate", token: "tok", reference: rowRef, status: "under_review", reason: "ok" });
  check("owner admin action works on the consolidated file", adm.ok === true, JSON.stringify(adm).slice(0, 120));
}

/* -------------------------------------------------- 7. payments untouched */
{
  const pay = read("apps-script/Code.gs");
  const combined = read(COMBINED);
  check("payments backend is a different file and was not touched by the build",
    /Razorpay/.test(pay) && /Payments/.test(pay));
  /* The word "Razorpay" DOES appear in the consolidated file - only inside
     comments warning the reader not to mix the two projects. What must not
     appear is payment CODE: no payment tabs, no payment constants. */
  const razorpayCodeLines = combined.split("\n").filter((l) => {
    if (!/Razorpay/i.test(l)) return false;
    const t = l.trim();
    return !(t.startsWith("*") || t.startsWith("/*") || t.startsWith("//"));
  });
  check("the consolidated form file contains no Razorpay payment code (comments only)",
    razorpayCodeLines.length === 0, razorpayCodeLines.slice(0, 2).join(" | "));
  check("no payment tab constants or payment spreadsheet id",
    !/TAB_PAYMENTS|TAB_CUSTOMERS|TAB_PUBLIC_SUPPORT|SPREADSHEET_ID_DEFAULT/.test(combined));
  check("the consolidated file does not hard-code the payments spreadsheet id",
    !/1u5Jkbe_2lMoLWsaDPQkxTWhNACewRaOyZLLANy2dfVI/.test(combined));
}

console.log("\n" + (fail ? fail + " FAILURE(S)" : "ALL CHECKS PASSED") + "  (" + pass + " passed, " + fail + " failed)");
process.exit(fail ? 1 : 0);

#!/usr/bin/env node
/* =========================================================
   EkGuru: APPLICATION BACKEND TEST  (ApplicationSchema + ApplicationIntake)
   ---------------------------------------------------------
   Runs the REAL Apps Script files in a sandbox with fake Google services —
   SpreadsheetApp, LockService, PropertiesService, GmailApp, Utilities — and
   checks the twenty things the brief asks for, in order:

     1  every wizard field maps to a column
     2  every field is saved in the sheet
     3  an old 13-field payload still works
     4  schema migration adds columns and keeps data
     5  missing required fields are refused
     6  a bad email is refused
     7  bad pricing is refused
     8  bad availability is refused
     9  a duplicate submission does not create a second row
    10  concurrent submissions do not both pass the duplicate check
    11  references are unique and well formed
    12  the confirmation email is sent once
    13  the approval email is sent, with the right subject
    14  the rejection email carries the ACTUAL reason
    15  the same transition is never emailed twice
    16  pending applications never appear in the public tutors feed
    17  rejected applications never appear in the public tutors feed
    18  an approved profile is preserved until review (no auto-publish)
    19  admin authorisation
    20  private applicant data never comes back out

   Run:  node tools/test-application-backend.mjs
   ========================================================= */
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8");

let failures = 0;
let passes = 0;
function check(name, cond, extra) {
  if (cond) passes++;
  else failures++;
  console.log((cond ? "PASS" : "FAIL") + "  " + name + (cond ? "" : "  ->  " + (extra === undefined ? "" : extra)));
}

/* -------------------------------------------------------------------------
   A fake workbook. Grid is a 2-D array per tab, 1-based like Apps Script:
   grid[row-1][col-1]. Enough of the API for this backend, and nothing more —
   if the .gs code calls something that is not here, the test FAILS loudly
   instead of quietly passing.
   ------------------------------------------------------------------------- */
function makeSheet(name, grid) {
  const sheet = {
    __name: name,
    grid: grid || [],
    frozen: 0,
    getName: () => name,
    getLastRow() {
      for (let r = sheet.grid.length - 1; r >= 0; r--) {
        if (sheet.grid[r] && sheet.grid[r].some((c) => c !== "" && c !== null && c !== undefined)) return r + 1;
      }
      return 0;
    },
    getLastColumn() {
      let max = 0;
      for (const row of sheet.grid) {
        const len = row ? row.length : 0;
        /* trailing blanks do not count, like the real thing */
        let last = 0;
        for (let c = 0; c < len; c++) if (row[c] !== "" && row[c] !== null && row[c] !== undefined) last = c + 1;
        if (last > max) max = last;
      }
      return max;
    },
    setFrozenRows(n) { sheet.frozen = n; },
    getRange(row, col, numRows, numCols) {
      numRows = numRows === undefined ? 1 : numRows;
      numCols = numCols === undefined ? 1 : numCols;
      return {
        getValues() {
          const out = [];
          for (let r = 0; r < numRows; r++) {
            const line = [];
            for (let c = 0; c < numCols; c++) {
              const rowArr = sheet.grid[row - 1 + r] || [];
              line.push(rowArr[col - 1 + c] === undefined ? "" : rowArr[col - 1 + c]);
            }
            out.push(line);
          }
          return out;
        },
        getValue() { return this.getValues()[0][0]; },
        setValues(values) {
          for (let r = 0; r < values.length; r++) {
            for (let c = 0; c < values[r].length; c++) {
              const rr = row - 1 + r;
              if (!sheet.grid[rr]) sheet.grid[rr] = [];
              sheet.grid[rr][col - 1 + c] = values[r][c];
            }
          }
          return this;
        },
        setValue(v) { return this.setValues([[v]]); },
        setBackground() { return this; },
        setFontWeight() { return this; },
        setNumberFormat() { return this; },
      };
    },
    appendRow(values) {
      const at = sheet.getLastRow();
      if (!sheet.grid[at]) sheet.grid[at] = [];
      for (let c = 0; c < values.length; c++) sheet.grid[at][c] = values[c];
    },
    insertSheet() { return sheet; },
  };
  return sheet;
}

function createEnv(opts) {
  opts = opts || {};
  const tabs = {};
  (opts.tabs || []).forEach((t) => { tabs[t.name] = makeSheet(t.name, t.grid); });

  const props = Object.assign({}, opts.properties || {});
  const sent = [];
  const errors = [];
  const cache = new Map();
  let lockHeld = false;

  const ss = {
    getSheetByName: (n) => tabs[n] || null,
    insertSheet: (n) => { tabs[n] = makeSheet(n, []); return tabs[n]; },
    getSheets: () => Object.keys(tabs).map((k) => tabs[k]),
  };

  const ctx = {
    console,
    Logger: { log: () => {} },
    SpreadsheetApp: {
      getActiveSpreadsheet: () => (opts.unbound ? null : ss),
      openById: () => ss,
      getUi: () => ({ createMenu: () => ({ addItem: () => ({ addItem: () => ({ addToUi: () => {} }) }), addToUi: () => {} }), alert: () => {} }),
    },
    PropertiesService: {
      getScriptProperties: () => ({
        getProperty: (k) => (props[k] === undefined ? null : props[k]),
        setProperty: (k, v) => { props[k] = v; },
      }),
    },
    CacheService: {
      getScriptCache: () => ({
        get: (k) => (cache.has(k) ? cache.get(k) : null),
        put: (k, v) => cache.set(k, v),
      }),
    },
    LockService: {
      getScriptLock: () => ({
        waitLock: () => { lockHeld = true; },
        tryLock: () => { if (lockHeld) return false; lockHeld = true; return true; },
        releaseLock: () => { lockHeld = false; },
      }),
    },
    GmailApp: {
      sendEmail: (to, subject, body, options) => {
        if (opts.mailThrows) throw new Error("Service invoked too many times: email quota");
        sent.push({ to, subject, body, options: options || {} });
      },
    },
    MailApp: { sendEmail: (o) => sent.push({ to: o.to, subject: o.subject, body: o.body, options: o }) },
    Utilities: {
      formatDate: (d, tz, fmt) => {
        const dt = d instanceof Date ? d : new Date(d);
        if (fmt === "yyyy-MM-dd'T'HH:mm:ss") return dt.toISOString().slice(0, 19);
        if (fmt === "d MMM yyyy, HH:mm") return dt.toISOString().slice(0, 16).replace("T", " ");
        return dt.toISOString();
      },
    },
    ContentService: {
      MimeType: { JSON: "application/json" },
      createTextOutput: (s) => ({ getContent: () => s, setMimeType: () => ({ getContent: () => s }) }),
    },
  };
  ctx.__tabs = tabs;
  ctx.__sent = sent;
  ctx.__errors = errors;
  ctx.__props = props;

  vm.createContext(ctx);

  /* Load order matters and mirrors the Apps Script project: the schema is a
     separate .gs file, the intake file uses it. */
  for (const file of ["apps-script/ApplicationSchema.gs", "apps-script/ApplicationIntake.gs"]) {
    try {
      vm.runInContext(read(file), ctx, { filename: file });
    } catch (err) {
      errors.push(file + ": " + err.message);
    }
  }
  return ctx;
}

function parse(res) {
  try { return JSON.parse(res.getContent()); } catch (e) { return { __raw: res && res.getContent && res.getContent() }; }
}

/* Which column holds a header, in this env's applications tab. */
function colOf(ctx, header) {
  const tab = ctx.__tabs.applications;
  /* the backend migrates on first use (ekHeaderMap_); asserting column
     contents only makes sense after that has run once */
  ctx.ekMigrateApplications();
  const row = tab.grid[0] || [];
  const at = row.indexOf(header);
  if (at === -1) throw new Error("no column " + header);
  return at;
}
function cellOf(ctx, rowIndex1, header) {
  const tab = ctx.__tabs.applications;
  return (tab.grid[rowIndex1 - 1] || [])[colOf(ctx, header)];
}
function dataRows(ctx) {
  const tab = ctx.__tabs.applications;
  return Math.max(0, tab.getLastRow() - 1);
}

const LEGACY_HEADER = ["timestamp", "reference", "status", "approved", "name", "email", "city",
  "country", "subject", "experience", "rate_usd", "availability", "bio", "photo_link",
  "video_link", "languages", "notes"];

function legacyTab(rows) {
  return { name: "applications", grid: [LEGACY_HEADER.slice()].concat(rows || []) };
}

/* -------------------------------------------------------------------------
   The payload a real wizard submission produces. Kept as one fixture so a
   change to the schema shows up as a test failure here too.
   ------------------------------------------------------------------------- */
const WIZARD_FIELDS = {
  name: "Kiran Rao",
  display_name: "Kiran",
  email: "kiran@example.com",
  city: "Pune",
  country: "India",
  state: "Maharashtra",
  contact_pref: "WhatsApp",
  intro: "Warm, patient teacher. I like short lessons with songs.",
  subjects: ["Conversational Hindi", "Hindi for Children"],
  levels: ["Children", "Absolute beginners"],
  methods: ["Conversation-based", "Games and interactive"],
  teach_langs: ["Hindi", "English"],
  hindi_level: "Native",
  english_level: "Advanced (C1)",
  other_langs: "Marathi: native",
  years: "6-10 years",
  online_years: "4",
  platforms: "Preply, private tuition",
  edu_qual: "Master's degree",
  edu_inst: "University of Delhi",
  edu_year: "2018",
  edu_extra: "Montessori certificate, 2019",
  certs: "CTET 2016",
  doc_refs: "B.Ed certificate no. 1234, Bundelkhand University",
  headline: "Patient Hindi tutor for children and beginners",
  bio: "I am a Hindi tutor from Pune with six years of experience teaching children and " +
       "beginners, in schools and online. My lessons mix conversation with reading and " +
       "writing in Devanagari script, stories and games.",
  why: "I want to teach children abroad to speak with their grandparents.",
  video_link: "https://youtu.be/abc123",
  video_thumb: "https://example.com/thumb.jpg",
  sample_link: "https://youtu.be/sample1",
  website2: "https://kiranhindi.example",
  linkedin: "https://linkedin.com/in/kiran",
  profile_url: "https://preply.com/en/tutor/123",
  rate_usd: "12",
  currency: "USD",
  duration: "50 min",
  trial: "Free short trial",
  timezone: "Asia/Kolkata",
  availability_slots: [{ day: "Mon", from: "19:00", to: "21:00" }, { day: "Wed", from: "18:00", to: "20:00" }],
  availability_meta: { days: 2, timezone: "Asia/Kolkata", format: "weekly-hours" },
  photo_link: "https://example.com/kiran.jpg",
  source: "join.html"
};

function submit(ctx, overrides) {
  const body = {
    kind: "application",
    consent: true,
    consent_privacy: true,
    website: "",
    submission_id: (overrides && overrides.submission_id) || "sub-" + Math.random().toString(36).slice(2),
    fields: Object.assign({}, WIZARD_FIELDS, (overrides && overrides.fields) || {})
  };
  if (overrides && overrides.drop) for (const k of overrides.drop) delete body.fields[k];
  return parse(ctx.ekApplicationAction_(body));
}

/* =========================================================================
   1 + 2. Every wizard field reaches a column, and is actually saved.
   ========================================================================= */
{
  const ctx = createEnv({ tabs: [legacyTab()], properties: { EK_ADMIN_TOKEN: "tok-123" } });
  const res = submit(ctx);
  check("1. a full wizard submission is accepted", res.ok === true, JSON.stringify(res).slice(0, 200));
  check("1. it returns a reference", /^EG-[2-9A-HJ-NP-Z]{6}$/.test(res.reference || ""), res.reference);

  const row = 2;
  const expect = {
    name: "Kiran Rao", display_name: "Kiran", email: "kiran@example.com", city: "Pune",
    country: "India", state: "Maharashtra", contact_pref: "WhatsApp",
    intro: "Warm, patient teacher", headline: "Patient Hindi tutor",
    hindi_level: "Native", english_level: "Advanced (C1)", other_langs: "Marathi: native",
    years: "6-10 years", online_years: "4", edu_qual: "Master's degree",
    edu_inst: "University of Delhi", certs: "CTET 2016", doc_refs: "B.Ed certificate",
    video_link: "https://youtu.be/abc123", video_thumb: "https://example.com/thumb.jpg",
    sample_link: "https://youtu.be/sample1", website: "https://kiranhindi.example",
    linkedin: "https://linkedin.com/in/kiran", profile_url: "https://preply.com/en/tutor/123",
    currency: "USD", duration: "50 min", trial: "Free short trial",
    timezone: "Asia/Kolkata", photo_link: "https://example.com/kiran.jpg",
    status: "pending", source: "join.html",
    /* Read from the schema itself, never hard-coded: pinning this literal
       meant a schema-version bump looked like a field-mapping failure. */
    schema_version: ctx.EKGURU_SCHEMA_VERSION
  };
  const wrong = [];
  for (const k of Object.keys(expect)) {
    const got = String(cellOf(ctx, row, k));
    if (got.indexOf(expect[k]) === -1) wrong.push(k + "=" + JSON.stringify(got));
  }
  check("2. every scalar field is stored in its own column", wrong.length === 0, wrong.join(", "));

  const lists = ["subjects_json", "levels_json", "methods_json", "teach_langs_json"];
  const badList = lists.filter((c) => { try { return !Array.isArray(JSON.parse(cellOf(ctx, row, c))); } catch (e) { return true; } });
  check("2. arrays are stored as JSON, not flattened", badList.length === 0, badList.join(","));

  const slots = JSON.parse(cellOf(ctx, row, "availability_json") || "[]");
  check("2. availability is stored as structured slots",
    slots.length === 2 && slots[0].day === "Mon" && slots[0].from === "19:00",
    JSON.stringify(slots));
  check("2. the legacy availability text is still filled",
    /Mon 19:00-21:00/.test(String(cellOf(ctx, row, "availability"))),
    String(cellOf(ctx, row, "availability")));
  check("2. edu_year is stored as a number, not text",
    Number(cellOf(ctx, row, "edu_year")) === 2018, cellOf(ctx, row, "edu_year"));
  check("2. consent is recorded with a timestamp",
    cellOf(ctx, row, "consent_terms") === "yes" && !!cellOf(ctx, row, "consent_at"),
    cellOf(ctx, row, "consent_terms"));
  check("1. no field fell into details_json",
    !String(cellOf(ctx, row, "details_json") || "").match(/intro|other_langs|edu_extra|less_exp|bed_detail/),
    String(cellOf(ctx, row, "details_json")).slice(0, 120));
}

/* =========================================================================
   1b. A field with no column of its own still survives (details_json).
   ========================================================================= */
{
  const ctx = createEnv({ tabs: [legacyTab()] });
  const res = submit(ctx, { fields: { something_new: "value that has no column" } });
  check("1b. an unknown field is accepted, not dropped", res.ok === true, JSON.stringify(res));
  const dj = JSON.parse(cellOf(ctx, 2, "details_json") || "{}");
  check("1b. the unknown field is preserved in details_json",
    dj.something_new === "value that has no column", JSON.stringify(dj));
}

/* =========================================================================
   3. The old 13-field payload still works.
   ========================================================================= */
{
  const ctx = createEnv({ tabs: [legacyTab()] });
  const old = {
    name: "Old Applicant", email: "old@example.com", city: "Agra", country: "India",
    subject: "Hindi", experience: "3 years", rate_usd: "20",
    availability: "Mon-Fri 18:00-22:00", bio: "A legacy application sent by Intake.gs v1.2.0.",
    photo_link: "", video_link: "", languages: "Hindi: Native", notes: "sent by the old form"
  };
  const res = parse(ctx.ekApplicationAction_({ kind: "application", consent: true, fields: old }));
  check("3. a 13-field legacy payload is accepted", res.ok === true, JSON.stringify(res));
  check("3. it lands in the same columns", String(cellOf(ctx, 2, "notes")) === "sent by the old form");
  check("3. it gets the same pending status", cellOf(ctx, 2, "status") === "pending");
  check("3. legacy rows are not forced to fill the new columns",
    cellOf(ctx, 2, "display_name") === "" && cellOf(ctx, 2, "details_json") === "",
    cellOf(ctx, 2, "display_name"));
}

/* =========================================================================
   4. Migration: adds columns, keeps data, no duplicates, idempotent.
   ========================================================================= */
{
  const existingRows = [
    ["2026-11-17", "EG-OLD001", "approved", "yes", "Jagrati", "j@example.com", "Jaipur", "India",
      "Hindi", "5 years", 18, "All day", "A real old row.", "", "", "Hindi", "an old note"]
  ];
  const ctx = createEnv({ tabs: [legacyTab(existingRows)] });
  const health0 = parse(ctx.ekApplicationGet_({ parameter: { action: "ekHealth" } }));
  check("4. health reports a half-migrated tab as NOT ok", health0.ok === false, JSON.stringify(health0).slice(0, 160));
  check("4. health names the missing columns",
    health0.columns.missing.indexOf("display_name") !== -1, JSON.stringify(health0.columns.missing).slice(0, 80));

  const mig = ctx.ekMigrateApplications();
  check("4. migration adds every missing column",
    mig.columns.missing.length === 0, JSON.stringify(mig.columns.missing));
  check("4. migration reports the data rows it kept", mig.rows === 1, mig.rows);

  const tab = ctx.__tabs.applications;
  check("4. the old row survived untouched",
    tab.grid[1][4] === "Jagrati" && tab.grid[1][12] === "A real old row.",
    JSON.stringify(tab.grid[1].slice(0, 5)));
  check("4. the first 17 header names did not move",
    JSON.stringify(tab.grid[0].slice(0, 17)) === JSON.stringify(LEGACY_HEADER),
    tab.grid[0].slice(0, 17).join(","));
  check("4. no duplicate header names",
    new Set(tab.grid[0]).size === tab.grid[0].length,
    tab.grid[0].filter((h, i) => tab.grid[0].indexOf(h) !== i).join(","));

  const before = tab.grid[0].slice();
  const mig2 = ctx.ekMigrateApplications();
  check("4. a second migration adds nothing (idempotent)",
    mig2.added.length === 0 && JSON.stringify(tab.grid[0]) === JSON.stringify(before),
    mig2.added.join(","));

  const health1 = parse(ctx.ekApplicationGet_({ parameter: { action: "ekHealth" } }));
  check("4. health is ok once the tab has every column", health1.ok === true, JSON.stringify(health1).slice(0, 120));
  check("4. health counts the existing rows", health1.rows === 1, health1.rows);
}

/* =========================================================================
   5–8. Validation.
   ========================================================================= */
{
  const ctx = createEnv({ tabs: [legacyTab()] });
  const cases = [
    ["5. missing name", { name: "" }, /name/],
    ["5. missing email", { email: "" }, /email/],
    ["5. missing bio", { bio: "" }, /bio/],
    ["5. missing price", { rate_usd: "" }, /rate/],
    ["5. missing city", { city: "" }, /city/],
    ["5. consent not given", { __consent: false }, /consent/],
    ["6. bad email", { email: "not-an-email" }, /email/],
    ["6. email with no dot", { email: "a@b" }, /email/],
    ["7. price zero", { rate_usd: "0" }, /at least/],
    ["7. price too high", { rate_usd: "500" }, /at most/],
    ["7. price decimal", { rate_usd: "7.5" }, /whole/],
    ["8. unknown availability day", { availability_slots: [{ day: "Funday", from: "10:00", to: "11:00" }] }, /day/],
    ["8. bad time format", { availability_slots: [{ day: "Mon", from: "9am", to: "11:00" }] }, /HH:MM/],
    ["8. end before start", { availability_slots: [{ day: "Mon", from: "21:00", to: "19:00" }] }, /after/],
    ["8. same day twice", { availability_slots: [{ day: "Mon", from: "10:00", to: "11:00" }, { day: "Mon", from: "12:00", to: "13:00" }] }, /twice/],
    ["5. url that is not https", { website2: "http://nope.example" }, /https/],
    ["5. headline over the limit", { headline: "x".repeat(121) }, /too long/],
  ];
  let bad = [];
  for (const [label, override, want] of cases) {
    const fields = Object.assign({}, override);
    delete fields.__consent;
    const bodyConsent = override.__consent === undefined ? true : override.__consent;
    const res = parse(ctx.ekApplicationAction_({
      kind: "application", consent: bodyConsent, consent_privacy: bodyConsent, website: "",
      submission_id: "v-" + label,
      fields: Object.assign({}, WIZARD_FIELDS, fields)
    }));
    if (res.ok !== false || !want.test(String(res.error || ""))) {
      bad.push(label + " -> " + JSON.stringify(res).slice(0, 90));
    }
  }
  check("5-8. every invalid payload is refused with a reason", bad.length === 0, bad.join(" | "));
  check("5-8. nothing was written by a refused payload", dataRows(ctx) === 0, dataRows(ctx));

  /* field-level messages, so the page can point at the box */
  const res = parse(ctx.ekApplicationAction_({
    kind: "application", consent: true, consent_privacy: true, website: "",
    submission_id: "vl-1", fields: Object.assign({}, WIZARD_FIELDS, { email: "bad" })
  }));
  check("5. a refusal names the offending field, not just a sentence",
    res.fields && res.fields.email, JSON.stringify(res.fields));
}

/* =========================================================================
   9. Duplicate submission.
   ========================================================================= */
{
  const ctx = createEnv({ tabs: [legacyTab()] });
  const a = submit(ctx, { submission_id: "same-1" });
  const b = submit(ctx, { submission_id: "same-1" });
  check("9. the same submission_id does not create a second row", dataRows(ctx) === 1, dataRows(ctx));
  check("9. the retry is answered with the same reference",
    a.reference === b.reference && b.duplicate === true, a.reference + " / " + b.reference);
  check("9. the retry does not re-send the email", ctx.__sent.length === 1, ctx.__sent.length);

  /* same person, new submission id, within the dedupe window → one row,
     updated in place, reference preserved */
  const c = submit(ctx, { submission_id: "same-2", fields: { city: "Mumbai", rate_usd: "15" } });
  check("9. a correction from the same email updates the same row",
    dataRows(ctx) === 1, dataRows(ctx));
  check("9. the applicant keeps their original reference", c.reference === a.reference, c.reference);
  check("9. the correction actually landed", String(cellOf(ctx, 2, "city")) === "Mumbai", cellOf(ctx, 2, "city"));
}

/* =========================================================================
   10. Concurrency: the second writer must not pass the duplicate scan while
   the first still holds the lock.
   ========================================================================= */
{
  const ctx = createEnv({ tabs: [legacyTab()] });
  const lock = ctx.LockService.getScriptLock();
  lock.tryLock();             /* someone else is mid-write */
  const blocked = parse(ctx.ekApplicationAction_({
    kind: "application", consent: true, consent_privacy: true, website: "",
    submission_id: "c-1", fields: WIZARD_FIELDS
  }));
  lock.releaseLock();
  check("10. a submission that cannot get the lock is refused, not written",
    blocked.ok === false && dataRows(ctx) === 0, JSON.stringify(blocked).slice(0, 120));
  const ok = submit(ctx, { submission_id: "c-2" });
  check("10. it succeeds once the lock is free", ok.ok === true && dataRows(ctx) === 1);
}

/* =========================================================================
   11. Application ID generation.
   ========================================================================= */
{
  const ctx = createEnv({ tabs: [legacyTab()] });
  const refs = new Set();
  for (let i = 0; i < 8; i++) {
    const r = submit(ctx, { submission_id: "id-" + i, fields: { email: "p" + i + "@example.com" } });
    refs.add(r.reference);
  }
  check("11. eight submissions get eight different references", refs.size === 8, [...refs].join(","));
  check("11. references avoid the characters a person misreads",
    [...refs].every((r) => !/[01OIL]/.test(r.slice(3))), [...refs].join(","));
  check("11. every reference is stored on its row",
    dataRows(ctx) === 8 && refs.has(String(cellOf(ctx, 5, "reference"))),
    String(cellOf(ctx, 5, "reference")));
}

/* =========================================================================
   12–15. Email.
   ========================================================================= */
{
  const ctx = createEnv({ tabs: [legacyTab()], properties: { EK_ADMIN_TOKEN: "tok-123", EK_ADMIN_NAME: "Prakash" } });
  const sub = submit(ctx);
  const received = ctx.__sent.filter((m) => /with us/.test(m.subject));
  check("12. a submission sends exactly one confirmation", received.length === 1, ctx.__sent.length);
  check("12. the confirmation goes to the applicant", received[0] && received[0].to === "kiran@example.com", received[0] && received[0].to);
  check("12. the confirmation carries the reference",
    received[0] && received[0].subject.indexOf(sub.reference) !== -1 && received[0].body.indexOf(sub.reference) !== -1);
  check("12. the confirmation says a person will review it",
    received[0] && /person reads every application/i.test(received[0].body));
  check("12. the confirmation does NOT say approved", received[0] && !/approved/i.test(received[0].subject));
  check("12. the row records the delivery", /received:sent/.test(String(cellOf(ctx, 2, "email_status"))),
    cellOf(ctx, 2, "email_status"));

  /* approval */
  const appr = ctx.ekSetStatus_(sub.reference, "approved", { admin: "owner-token", note: "looks good" });
  check("13. approval is accepted", appr.ok === true, JSON.stringify(appr));
  const apprMail = ctx.__sent.filter((m) => /is approved/.test(m.subject));
  check("13. approval sends exactly one email", apprMail.length === 1, apprMail.length);
  check("13. the approval email explains the next steps",
    apprMail[0] && /before it goes live/i.test(apprMail[0].body));
  check("13. the sheet records approved=yes and the reviewer",
    cellOf(ctx, 2, "approved") === "yes" && String(cellOf(ctx, 2, "reviewed_by")).length > 0,
    cellOf(ctx, 2, "approved") + "/" + cellOf(ctx, 2, "reviewed_by"));
  check("13. previous_status is kept", cellOf(ctx, 2, "previous_status") === "pending",
    cellOf(ctx, 2, "previous_status"));

  /* 15. duplicate email prevention */
  const again = ctx.ekSetStatus_(sub.reference, "approved", { admin: "owner-token" });
  check("15. re-applying the same status changes nothing",
    again.ok === true && again.unchanged === true, JSON.stringify(again));

  /* 14. rejection with the real reason */
  const ctx2 = createEnv({ tabs: [legacyTab()], properties: { EK_ADMIN_TOKEN: "tok-123" } });
  const s2 = submit(ctx2, { fields: { email: "rej@example.com" } });
  const noReason = ctx2.ekSetStatus_(s2.reference, "rejected", { admin: "owner" });
  check("14. a rejection WITHOUT a reason is refused",
    noReason.ok === false && /reason/.test(noReason.error), JSON.stringify(noReason));
  check("14. the refusal is not emailed", ctx2.__sent.length === 1, ctx2.__sent.length);

  const reason = "The profile photo link was broken and the application had no teaching experience.";
  const rej = ctx2.ekSetStatus_(s2.reference, "rejected", { admin: "owner", reason: reason });
  check("14. a rejection with a reason is accepted", rej.ok === true, JSON.stringify(rej));
  const rejMail = ctx2.__sent.filter((m) => /About your EkGuru tutor application/.test(m.subject));
  check("14. the rejection email is sent once", rejMail.length === 1, rejMail.length);
  check("14. the rejection email carries the ACTUAL reason",
    rejMail[0] && rejMail[0].body.indexOf(reason) !== -1,
    rejMail[0] && rejMail[0].body.slice(0, 120));
  check("14. the rejection email stays respectful",
    rejMail[0] && /thank you/i.test(rejMail[0].body) && /very welcome to apply again/i.test(rejMail[0].body));
  check("14. the reason is stored on the row",
    String(cellOf(ctx2, 2, "rejection_reason")).indexOf("broken") !== -1,
    cellOf(ctx2, 2, "rejection_reason"));

  /* status machine */
  const backwards = ctx2.ekSetStatus_(s2.reference, "pending", { admin: "owner" });
  check("14. a rejected application cannot be walked back to pending",
    backwards.ok === false, JSON.stringify(backwards));
  const revive = ctx2.ekSetStatus_(s2.reference, "under_review", { admin: "owner" });
  check("14. it CAN be reopened for review", revive.ok === true, JSON.stringify(revive));
}

/* =========================================================================
   12b. Mail quota failure must not lose the application.
   ========================================================================= */
{
  const ctx = createEnv({ tabs: [legacyTab()], opts: {}, properties: {} });
  ctx.__props.APPLICATION_MAIL_ENABLED = "true";
  /* make Gmail throw by swapping the object in the context */
  vm.runInContext("GmailApp = { sendEmail: function () { throw new Error('quota'); } };", ctx);
  const res = submit(ctx);
  check("12b. a mail failure still saves the application", res.ok === true, JSON.stringify(res));
  check("12b. the row records the failure, not a lie",
    /received:failed/.test(String(cellOf(ctx, 2, "email_status"))), cellOf(ctx, 2, "email_status"));
  check("12b. the response tells the page the mail is delayed",
    res.mail === "failed" && !!res.mail_note, JSON.stringify(res).slice(0, 160));
}

/* =========================================================================
   16–18. Publication rules. The public tutors feed is a different tab; this
   backend must never write to it, and an approved application must not
   publish itself.
   ========================================================================= */
{
  const tutorsGrid = [
    ["id", "active", "name", "approved"],
    ["sushila-g", "yes", "Sushila G.", "yes"]
  ];
  const ctx = createEnv({
    tabs: [legacyTab(), { name: "tutors", grid: tutorsGrid.map((r) => r.slice()) }],
    properties: { EK_ADMIN_TOKEN: "tok-123" }
  });
  const sub = submit(ctx);
  const tutorsRows = () => ctx.__tabs.tutors.getLastRow() - 1;

  check("16. a pending application never reaches the tutors tab",
    tutorsRows() === 1, tutorsRows());
  ctx.ekSetStatus_(sub.reference, "approved", { admin: "owner" });
  check("18. approving an application does NOT publish a tutor row",
    tutorsRows() === 1, "the backend wrote to the public tutors tab");
  check("18. approval only records the decision in applications",
    cellOf(ctx, 2, "approved") === "yes" && cellOf(ctx, 2, "status") === "approved");

  const s2 = submit(ctx, { fields: { email: "rej2@example.com" } });
  ctx.ekSetStatus_(s2.reference, "rejected", { admin: "owner", reason: "not suitable" });
  check("17. a rejected application never reaches the tutors tab",
    tutorsRows() === 1, "the backend wrote to the public tutors tab");
  check("17. nothing in the tutors tab changed at all",
    JSON.stringify(ctx.__tabs.tutors.grid) === JSON.stringify(tutorsGrid));
}

/* =========================================================================
   19. Admin authorisation.
   ========================================================================= */
{
  const ctx = createEnv({ tabs: [legacyTab()], properties: { EK_ADMIN_TOKEN: "tok-123" } });
  const sub = submit(ctx);

  const noToken = parse(ctx.ekApplicationAction_({
    action: "ekAdminUpdate", reference: sub.reference, status: "approved"
  }));
  check("19. an admin action with no token is refused", noToken.ok === false, JSON.stringify(noToken));
  check("19. and the status did not change", cellOf(ctx, 2, "status") === "pending");

  const wrong = parse(ctx.ekApplicationAction_({
    action: "ekAdminUpdate", token: "guess", reference: sub.reference, status: "approved"
  }));
  check("19. a wrong token is refused", wrong.ok === false, JSON.stringify(wrong));

  const okRes = parse(ctx.ekApplicationAction_({
    action: "ekAdminUpdate", token: "tok-123", reference: sub.reference,
    status: "approved", note: "verified by phone"
  }));
  check("19. the right token is accepted", okRes.ok === true, JSON.stringify(okRes).slice(0, 120));
  check("19. the change went through", cellOf(ctx, 2, "status") === "approved");

  /* a project with no token configured refuses every admin action */
  const ctx2 = createEnv({ tabs: [legacyTab()] });
  const s2 = submit(ctx2);
  const off = parse(ctx2.ekApplicationAction_({
    action: "ekAdminUpdate", token: "", reference: s2.reference, status: "approved"
  }));
  check("19. admin actions are OFF until a token is set",
    off.ok === false && /switched off/.test(off.error), JSON.stringify(off));
}

/* =========================================================================
   20. Private information protection.
   ========================================================================= */
{
  const ctx = createEnv({ tabs: [legacyTab()], properties: { EK_ADMIN_TOKEN: "tok-123" } });
  const sub = submit(ctx);

  /* the applicant lookup needs reference AND email */
  const onlyRef = parse(ctx.ekApplicationAction_({ action: "ekStatus", reference: sub.reference }));
  check("20. a reference alone reveals nothing", onlyRef.ok === false, JSON.stringify(onlyRef));

  const wrongEmail = parse(ctx.ekApplicationAction_({
    action: "ekStatus", reference: sub.reference, email: "someone@else.com"
  }));
  check("20. the wrong email reveals nothing", wrongEmail.ok === false, JSON.stringify(wrongEmail));

  const good = parse(ctx.ekApplicationAction_({
    action: "ekStatus", reference: sub.reference, email: "kiran@example.com"
  }));
  check("20. the right pair returns the status", good.ok === true && good.status === "pending",
    JSON.stringify(good));
  check("20. the status answer carries no row contents",
    !JSON.stringify(good).match(/kiran@example\.com|Pune|Maharashtra|bio|token/),
    JSON.stringify(good));

  const health = parse(ctx.ekApplicationGet_({ parameter: { action: "ekHealth" } }));
  check("20. health exposes counts, never applicant data",
    !JSON.stringify(health).match(/kiran|Pune|example\.com|tok-123/),
    JSON.stringify(health).slice(0, 200));

  check("20. the schema file holds no spreadsheet id, url or key",
    !/1_[A-Za-z0-9_-]{20,}|script\.google\.com|AKfycb|rzp_/.test(read("apps-script/ApplicationSchema.gs")));
  check("20. the schema file holds no admin token",
    !/EK_ADMIN_TOKEN\s*[:=]\s*["'][^"']+["']/.test(read("apps-script/ApplicationSchema.gs")));
}

/* =========================================================================
   21. MIGRATION SAFETY — adding a column must never disturb what is there.

   The 69th column (whatsapp) is appended to a tab that may already hold a
   year of real applications. This asserts the three things that matter:
   existing headers keep their position, existing cell values are byte
   identical, and the older legacy 17 columns are untouched.
   ========================================================================= */
{
  const schemaEnv = createEnv({ tabs: [legacyTab()] });
  const header = schemaEnv.EKGURU_APPLICATION_HEADER.filter((c) => c !== "whatsapp");
  const known = {
    timestamp: "10 Nov 2026, 09:15", reference: "EG-KEEP01", status: "approved",
    approved: "yes", name: "Existing Tutor", email: "keep@example.com", city: "Jaipur",
    country: "India", subject: "Hindi", experience: "6-10 years", rate_usd: 12,
    availability: "Mon 19:00-21:00", bio: "A real stored bio.",
    photo_link: "https://example.com/p.jpg", languages: "Hindi, English",
    notes: "an owner note", headline: "Existing headline", certs: "CTET 2015"
  };
  const row = header.map((c) => (Object.prototype.hasOwnProperty.call(known, c) ? known[c] : "v-" + c));
  const tab = legacyTab();
  tab.grid[0] = header.slice();
  tab.grid[1] = row.slice();
  const env = createEnv({ tabs: [tab] });
  const beforeHeader = env.__tabs.applications.grid[0].slice();
  const beforeRow = env.__tabs.applications.grid[1].slice();

  const r = env.ekMigrateApplications();
  const afterHeader = env.__tabs.applications.grid[0];
  const afterRow = env.__tabs.applications.grid[1];

  check("21. the migration adds exactly one column", r.added.length === 1 && r.added[0] === "whatsapp",
    JSON.stringify(r.added));
  check("21. the tab now has 69 columns", afterHeader.length === 69, afterHeader.length);
  check("21. every pre-existing header kept its exact position",
    JSON.stringify(afterHeader.slice(0, 68)) === JSON.stringify(beforeHeader));
  check("21. the new column is appended at the END, never in the middle",
    afterHeader[68] === "whatsapp", afterHeader[68]);
  check("21. every pre-existing cell value is unchanged",
    JSON.stringify(afterRow.slice(0, 68)) === JSON.stringify(beforeRow));
  check("21. the legacy 17 columns are byte identical",
    JSON.stringify(afterRow.slice(0, 17)) === JSON.stringify(beforeRow.slice(0, 17)));
  check("21. no data row was added or removed",
    env.__tabs.applications.getLastRow() - 1 === 1, env.__tabs.applications.getLastRow() - 1);
  check("21. the new cell is empty, not undefined",
    afterRow[68] === "", JSON.stringify(afterRow[68]));

  env.ekMigrateApplications();
  check("21. running the migration twice does not duplicate anything",
    env.__tabs.applications.grid[0].length === 69 && env.__tabs.applications.getLastRow() - 1 === 1,
    env.__tabs.applications.grid[0].length + " cols / " + (env.__tabs.applications.getLastRow() - 1) + " rows");
}

/* =========================================================================
   22. THE WHATSAPP FIELD — optional, private, never invented.
   ========================================================================= */
{
  const env = createEnv({ tabs: [legacyTab()] });
  const f = env.ekSchemaField("whatsapp");
  check("22. whatsapp has its own column in the schema", !!f && f.col === "whatsapp", JSON.stringify(f));
  check("22. it is optional in the schema", !f || f.required !== true);
  check("22. it is NOT a server-only field (the applicant may send it)",
    env.EKGURU_SERVER_ONLY.indexOf("whatsapp") === -1);
  const cases = [
    ["+91 98765 43210", "+919876543210"],
    ["98765 43210", "9876543210"],
    ["+44 7700 900123", "+447700900123"],
    ["(91) 98765-43210", "919876543210"]
  ];
  const base = { name: "N", email: "n@example.com", city: "C", country: "Co",
    subject: "Hindi", bio: "b", rate_usd: "12" };
  const bad = [];
  for (const [input, want] of cases) {
    const r = env.ekValidateApplication_(Object.assign({ whatsapp: input }, base),
      { consent: true, consent_privacy: true });
    const got = r.values && r.values.whatsapp;
    if (got !== want) bad.push(JSON.stringify(input) + "->" + JSON.stringify(got));
  }
  check("22. Indian and international numbers are kept as typed, never guessed",
    bad.length === 0, bad.join(" | "));
  const short = env.ekValidateApplication_(Object.assign({ whatsapp: "12" }, base),
    { consent: true, consent_privacy: true });
  check("22. a too-short number is refused with a clear reason",
    !!(short.fields && short.fields.whatsapp), JSON.stringify(short.fields));
  const blank = env.ekValidateApplication_(Object.assign({}, base),
    { consent: true, consent_privacy: true });
  check("22. a blank number is accepted and stored empty",
    !!(blank.values && blank.values.whatsapp === ""), JSON.stringify(blank.fields));
  check("22. the feed's private-column list already removes a whatsapp column",
    (function () {
      const u = read("apps-script/Unified.gs");
      const m = u.match(/FEED_PRIVATE_EXACT\s*=\s*\[([\s\S]*?)\]/);
      return !!m && /"whatsapp"/.test(m[1]);
    })());
}

/* =========================================================================
   X. Cross-file guards: the two router seams exist, and the feed half of
   Unified.gs was not disturbed.
   ========================================================================= */
{
  const unified = read("apps-script/Unified.gs");
  check("X. Unified.gs calls the application seam on POST",
    /ekApplicationAction_\(body\)/.test(unified));
  check("X. Unified.gs calls the application seam on GET",
    /ekApplicationGet_\(e\)/.test(unified));
  check("X. Unified.gs still has exactly one doGet and one doPost",
    (unified.match(/^function doGet\(/gm) || []).length === 1 &&
    (unified.match(/^function doPost\(/gm) || []).length === 1);
  check("X. Unified.gs still names no spreadsheet id",
    !/Spreadsheet ID:\s*[A-Za-z0-9_-]{20,}/.test(unified));
  check("X. the application backend never hard-codes a workbook id",
    !/openById\(\s*["'][A-Za-z0-9_-]{20,}/.test(read("apps-script/ApplicationIntake.gs")));
  check("X. Intake.gs keeps working when ApplicationIntake.gs is absent",
    /typeof ekApplicationAction_ === "function"/.test(read("apps-script/Intake.gs")));
}

/* Read row 1 as an object keyed by header (Block 30/31 need the whole row). */
function rowObject(ctx, at) {
  const tab = ctx.__tabs.applications;
  const head = tab.grid[0] || [];
  const row = tab.grid[(at || 1)] || [];
  const o = {};
  head.forEach((h, i) => { o[h] = row[i] === undefined ? "" : row[i]; });
  return o;
}

/* =========================================================================
   Block 30 — a server-owned name in the payload is diverted, not stored.
   ========================================================================= */
{
  const ctx = createEnv({ tabs: [legacyTab()], properties: { EK_ADMIN_TOKEN: "tok-123" } });
  const res = submit(ctx, {
    fields: {
      status: "approved",
      approved: "Yes",
      review_notes: "PRIVATE: forged",
      reference: "EG-HACKED"
    }
  });
  check("30. the submission is still accepted", res.ok === true, JSON.stringify(res).slice(0, 160));
  const obj = rowObject(ctx);
  check("30. status is the server's own initial value", obj.status === "pending", obj.status);
  check("30. approved is blank", String(obj.approved || "") === "", obj.approved);
  check("30. review_notes is blank", String(obj.review_notes || "") === "", obj.review_notes);
  check("30. the reference is the one the server minted", obj.reference === res.reference, obj.reference);

  const details = JSON.parse(obj.details_json || "{}");
  check("30. a reserved name is not stored under its own key", details.status === undefined &&
    details.approved === undefined && details.review_notes === undefined, JSON.stringify(details));
  check("30. it is recorded, inert, under sent_*", details.sent_review_notes === "PRIVATE: forged",
    JSON.stringify(details));
  check("30. no row gains an invented column", !ctx.__tabs.applications.grid[0].includes("PRIVATE: forged"));

  /* a free-text answer with no column still goes to details_json unchanged */
  const res2 = submit(ctx, { fields: { referral: "a friend", email: "second@example.test" } });
  check("30. a second applicant creates a second row", ctx.__tabs.applications.getLastRow() - 1 === 2,
    ctx.__tabs.applications.getLastRow() - 1);
  const obj2 = rowObject(ctx, 2);
  const det2 = JSON.parse(obj2.details_json || "{}");
  check("30. a genuine overflow answer is still kept verbatim", det2.referral === "a friend", JSON.stringify(det2));
  check("30. the second row carries none of the first row's diverted names",
    det2.sent_review_notes === undefined && det2.sent_status === undefined, JSON.stringify(det2));
}

/* =========================================================================
   Block 31 — availability_meta is derived when the client omits it.
   `== null` could never fire, because validation stores "" for an omitted
   field, so a non-browser client got availability_json next to an empty meta.
   ========================================================================= */
{
  const ctx = createEnv({ tabs: [legacyTab()] });
  const d = submit(ctx, { drop: ["availability_meta"] });
  check("31. the submission is accepted without availability_meta", d.ok === true, JSON.stringify(d).slice(0, 160));
  const obj = rowObject(ctx);
  check("31. availability_json is still filled", /Mon/.test(String(obj.availability_json)), obj.availability_json);
  check("31. availability_meta is derived, not left empty", String(obj.availability_meta || "").length > 0,
    JSON.stringify(obj.availability_meta));
  const meta = JSON.parse(obj.availability_meta);
  check("31. the derived meta is well formed",
    meta.slots === 2 && meta.days === 2 && meta.timezone === "Asia/Kolkata" && meta.format === "weekly-hours",
    obj.availability_meta);

  /* a client-supplied value is respected */
  const ctx2 = createEnv({ tabs: [legacyTab()] });
  submit(ctx2, { fields: { availability_meta: { days: 9, slots: 9, timezone: "Asia/Kolkata", format: "weekly-hours" } } });
  const obj2 = rowObject(ctx2);
  check("31. a client-supplied meta is not overwritten", JSON.parse(obj2.availability_meta).slots === 9,
    obj2.availability_meta);

  /* no availability at all -> the meta stays empty rather than inventing one */
  const ctx3 = createEnv({ tabs: [legacyTab()] });
  submit(ctx3, { drop: ["availability_meta", "availability_slots"] });
  const obj3 = rowObject(ctx3);
  check("31. no slots means no invented meta", String(obj3.availability_meta || "") === "",
    JSON.stringify(obj3.availability_meta));
}

console.log("\n" + (failures ? failures + " FAILURE(S)" : "ALL APPLICATION BACKEND TESTS PASSED") +
  "  (" + passes + " checks)");
process.exit(failures ? 1 : 0);

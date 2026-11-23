/**
 * ============================================================================
 * EkGuru — APPLICATION INTAKE v2 (six-step wizard backend)
 * ============================================================================
 * The application half of the intake backend. It replaces nothing: it sits
 * BESIDE apps-script/Intake.gs and is reached through two small delegation
 * seams that Intake.gs / Unified.gs already call (see "HOW IT PLUGS IN").
 * If this file is missing from the project, the old behaviour is exactly
 * what it is today.
 *
 * FILES THIS DEPENDS ON (all in the same Apps Script project)
 *   ApplicationSchema.gs   the field table, limits, statuses, moves
 *   Unified.gs             the router (or Intake.gs + LiveFeed.gs)
 *
 * ---------------------------------------------------------------------------
 * HOW IT PLUGS IN
 * ---------------------------------------------------------------------------
 * In Unified.gs (and in Intake.gs) intakePost_ does this immediately after
 * it has parsed the request body:
 *
 *     if (typeof ekApplicationAction_ === "function") {
 *       var ekHandled = ekApplicationAction_(body);
 *       if (ekHandled) return ekHandled;
 *     }
 *
 * and doGet answers `?action=ekHealth` the same way. Nothing else in those
 * files is touched, so the feed, bookings, reviews, contacts and sign-ups
 * keep running exactly as they do now.
 *
 * ---------------------------------------------------------------------------
 * ACTIONS
 * ---------------------------------------------------------------------------
 *   GET  ?action=ekHealth
 *        → {ok, schema, applications, columns:{expected, present, missing}, mail}
 *
 *   POST {kind:"application", consent:true, website:"",
 *         fields:{…}, submission_id:"…"}
 *        → {ok:true, reference:"EG-XXXXXX", duplicate:false, mail:"sent"|"skipped"}
 *        → {ok:false, error:"…", fields:{name:"…"}}   (field-level messages)
 *
 *   POST {action:"ekStatus", reference:"EG-XXXXXX", email:"…"}
 *        → {ok:true, status, submitted_at, note}
 *        Applicant lookup needs the reference AND the email that applied.
 *        A reference on its own is not authorisation, and the answer never
 *        contains the row's contents.
 *
 *   POST {action:"ekAdminUpdate", token:"…", reference:"EG-XXXXXX",
 *         status:"approved", reason:"…", note:"…"}
 *        Owner-only. `token` must equal the EK_ADMIN_TOKEN script property.
 * ============================================================================
 */

"use strict";

var EK_APP_VERSION = "2.0.2";

/* How long a second submission from the same email is treated as "the same
   application, corrected" rather than a fresh one. Anything older is a new
   application (people do apply again a year later). */
var EK_DEDUPE_HOURS = 72;

/* A guard so one script execution cannot mail a whole tab. */
var EK_MAIL_MAX_PER_RUN = 10;

/** The workbook. Reuses the intake project's own resolver when present, so
 *  there is ONE place that knows about the bound sheet / script property. */
function ekSheet_() {
  if (typeof intakeSpreadsheet_ === "function") return intakeSpreadsheet_();
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) throw new Error("no spreadsheet");
  return ss;
}

/* `create` defaults to true for every write path. Health and any other
   read-only caller passes false: asking "is my tab healthy?" must not
   CREATE the tab it is asking about, or a typo'd monitoring URL silently
   adds an empty sheet to the owner's workbook. */
function ekTab_(create) {
  var ss = ekSheet_();
  var tab = ss.getSheetByName("applications");
  if (tab) return tab;
  if (create === false) return null;
  return ss.insertSheet("applications");
}

function ekNow_() { return new Date(); }

function ekIso_(d) {
  try { return Utilities.formatDate(d, "Asia/Kolkata", "yyyy-MM-dd'T'HH:mm:ss") + "+05:30"; }
  catch (err) { return String(d); }
}

function ekStamp_(d) {
  try { return Utilities.formatDate(d, "Asia/Kolkata", "d MMM yyyy, HH:mm") + " IST"; }
  catch (err) { return String(d); }
}

/* ---------------------------------------------------------------------------
   Script properties. Nothing is hard-coded: no spreadsheet id, no token, no
   inbox. See apps-script/APPLICATION-BACKEND.md for the setup table.
   -------------------------------------------------------------------------- */
function ekProp_(name, fallback) {
  try {
    var v = PropertiesService.getScriptProperties().getProperty(name);
    return v == null || v === "" ? (fallback || "") : String(v);
  } catch (err) { return fallback || ""; }
}

function ekAdminToken_() { return ekProp_("EK_ADMIN_TOKEN", ""); }

function ekMailEnabled_() {
  return String(ekProp_("APPLICATION_MAIL_ENABLED", "true")).toLowerCase() !== "false";
}

function ekOwnerInbox_() {
  return ekProp_("APPLICATION_OWNER_INBOX", ekProp_("BOOKING_OWNER_INBOX", "EkGuruLearning@gmail.com"));
}

function ekFromName_() { return ekProp_("APPLICATION_SENDER_NAME", "EkGuru"); }

function ekSiteUrl_() {
  var u = ekProp_("APPLICATION_SITE_URL", "https://ekguru.shop/");
  return /^https:\/\//.test(u) ? u : "https://ekguru.shop/";
}

/* ---------------------------------------------------------------------------
   HEADER MAP + MIGRATION
   ---------------------------------------------------------------------------
   Reading and writing go through a {header: 0-based column} map built from
   row 1, never from a hardcoded index. If the owner inserts a column by
   hand, or an old tab is missing the new columns entirely, this fixes the
   shape once and every later write is by name.

   Migration policy:
     · an existing header cell is NEVER moved, renamed or cleared;
     · missing columns are APPENDED to the right, in schema order;
     · a duplicated header name keeps its FIRST column (the one that already
       holds data) and the later copy is left untouched and unused;
     · a tab with no rows at all gets the full header;
     · nothing is written into data rows — old applications simply have
       blank cells in the columns that did not exist when they arrived.
   -------------------------------------------------------------------------- */
/* PURE READ. Never writes. Used by health, by the status lookup and by the
   row reader — a GET must not add 51 header cells to the owner's sheet. */
function ekHeaderRead_(tab) {
  var header = [];
  var last = tab.getLastColumn();
  if (tab.getLastRow() >= 1 && last >= 1) {
    header = tab.getRange(1, 1, 1, last).getValues()[0].map(function (h) {
      return String(h == null ? "" : h).trim();
    });
  }
  var map = {};
  for (var i = 0; i < header.length; i++) {
    if (!header[i]) continue;
    if (map[header[i]] === undefined) map[header[i]] = i;   /* first wins */
  }
  return { map: map, header: header };
}

/* Map + migrate. The ONLY function that adds columns, and it is called from
   the write paths (submit, status change) and from the owner's menu action —
   never from a read. */
function ekHeaderMap_(tab) {
  var header = [];
  var last = tab.getLastColumn();
  if (tab.getLastRow() >= 1 && last >= 1) {
    header = tab.getRange(1, 1, 1, last).getValues()[0].map(function (h) {
      return String(h == null ? "" : h).trim();
    });
  }
  /* A tab created by hand may have no header at all. */
  var hasAny = header.some(function (h) { return h; });
  var map = {};
  var i;
  for (i = 0; i < header.length; i++) {
    if (!header[i]) continue;
    if (map[header[i]] === undefined) map[header[i]] = i;   /* first wins */
  }
  var added = [];
  var next = Math.max(tab.getLastColumn(), 0);
  for (i = 0; i < EKGURU_APPLICATION_HEADER.length; i++) {
    var col = EKGURU_APPLICATION_HEADER[i];
    if (map[col] !== undefined) continue;
    next++;
    tab.getRange(1, next, 1, 1).setValue(col);
    map[col] = next - 1;
    added.push(col);
  }
  if (!hasAny) tab.setFrozenRows(1);
  /* A cell that was never written reads back as undefined in the fake sheet
     and as "" in a real one. Settle any such cell to "" so the tab is
     rectangular and a dashboard formula does not see a hole. */
  if (added.length && tab.getLastRow() >= 2) {
    var firstNew = map[added[0]];
    var width = Math.max(tab.getLastColumn() - firstNew, 1);
    var body = tab.getRange(2, firstNew + 1, tab.getLastRow() - 1, width).getValues();
    var patch = [];
    for (var r = 0; r < body.length; r++) {
      var line = [];
      for (var c2 = 0; c2 < width; c2++) line.push(body[r][c2] === undefined || body[r][c2] === null ? "" : body[r][c2]);
      patch.push(line);
    }
    tab.getRange(2, firstNew + 1, patch.length, width).setValues(patch);
  }
  return { map: map, added: added, columns: next };
}

/* Health answer for the applications tab: how many of the schema's columns
   the live tab actually has, and which are missing. Used by ?action=ekHealth
   and by the test suite so a half-migrated tab is visible, not silent. */
function ekColumnReport_(tab) {
  var map = ekHeaderRead_(tab).map;
  var missing = [];
  for (var i = 0; i < EKGURU_APPLICATION_HEADER.length; i++) {
    if (map[EKGURU_APPLICATION_HEADER[i]] === undefined) missing.push(EKGURU_APPLICATION_HEADER[i]);
  }
  return {
    expected: EKGURU_APPLICATION_HEADER.length,
    present: EKGURU_APPLICATION_HEADER.length - missing.length,
    missing: missing
  };
}

/* Run by hand from the editor after pasting this file (or from the menu).
   Idempotent: a second run adds nothing and touches no data. */
function ekMigrateApplications() {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var tab = ekTab_();
    var before = tab.getLastRow();
    var out = ekHeaderMap_(tab);
    var report = ekColumnReport_(tab);
    Logger.log("applications: %s data rows kept, %s columns added, %s/%s schema columns present",
      Math.max(0, before - 1), out.added.length, report.present, report.expected);
    return { ok: true, rows: Math.max(0, before - 1), added: out.added, columns: report };
  } finally {
    lock.releaseLock();
  }
}

/* Adds an "EkGuru" menu so the owner can migrate without the editor. */
function onOpen() {
  try {
    SpreadsheetApp.getUi()
      .createMenu("EkGuru")
      .addItem("Migrate applications tab", "ekMigrateApplications")
      .addItem("Application schema health", "ekSchemaHealthDialog")
      .addToUi();
  } catch (err) { /* not every execution context has a UI */ }
}

function ekSchemaHealthDialog() {
  try {
    var r = ekColumnReport_(ekTab_());
    SpreadsheetApp.getUi().alert("This project runs ApplicationSchema " + EKGURU_SCHEMA_VERSION +
      ".\n\nYour applications tab has " + r.present + " of " + r.expected + " columns." +
      (r.missing.length ? "\n\nMissing (run Migrate to add):\n" + r.missing.join(", ") : "\n\nNothing to add."));
  } catch (err) { /* swallow: a dialog must never break a write path */ }
}

/* ---------------------------------------------------------------------------
   VALIDATION — schema driven
   ---------------------------------------------------------------------------
   Every rule comes from EKGURU_APPLICATION_FIELDS, so the browser copy of the
   schema and the server cannot disagree about a limit. The server is the
   authority: the browser checks the same things only to save a round trip.
   -------------------------------------------------------------------------- */

function ekCleanText_(s) {
  /* Strip angle brackets (no markup reaches the sheet), collapse control
     characters, and neutralise formula injection: a cell starting with
     = + - @ is a formula in Google Sheets. */
  var v = String(s == null ? "" : s).replace(/[<>]/g, "").replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, " ");
  v = v.replace(/\r\n/g, "\n").trim();
  if (/^[=+\-@]/.test(v)) v = "'" + v;
  return v;
}

function ekIsEmail_(s) {
  return /^[^\s@<>"']+@[^\s@<>"']+\.[^\s@<>"']{2,}$/.test(String(s || ""));
}

function ekIsUrl_(s) {
  return /^https:\/\/[^\s<>"']+$/.test(String(s || ""));
}

/* Availability. Accepts an array of {day, from, to}. Everything else about
   it is checked: known day, 24-hour HH:MM, end after start, no duplicate
   day, at most 7 entries. Returns the cleaned array or an error. */
function ekValidateAvailability_(raw) {
  if (raw == null) return { slots: [] };
  if (Object.prototype.toString.call(raw) !== "[object Array]") {
    return { error: "availability must be a list of days" };
  }
  if (raw.length > 7) return { error: "availability can have at most 7 days" };
  var seen = {};
  var out = [];
  for (var i = 0; i < raw.length; i++) {
    var d = raw[i] || {};
    var day = String(d.day || "").trim();
    var from = String(d.from || "").trim();
    var to = String(d.to || "").trim();
    if (EKGURU_DAYS.indexOf(day) === -1) return { error: "availability day is not valid: " + day };
    if (seen[day]) return { error: "availability has " + day + " twice" };
    seen[day] = 1;
    if (!/^([01]\d|2[0-3]):[0-5]\d$/.test(from) || !/^([01]\d|2[0-3]):[0-5]\d$/.test(to)) {
      return { error: "availability times must be HH:MM (24 hour) on " + day };
    }
    if (to <= from) return { error: "the " + day + " finish time must be after the start time" };
    out.push({ day: day, from: from, to: to });
  }
  /* Monday-first, whatever order the browser sent them in. */
  out.sort(function (a, b) { return EKGURU_DAYS.indexOf(a.day) - EKGURU_DAYS.indexOf(b.day); });
  return { slots: out };
}

/* The human line the old site and the owner's eye both want:
   "Mon 19:00-21:00; Tue 09:00-11:00" — this feeds the pre-existing
   `availability` column so nothing that already reads it has to change. */
/* The slots, whether they arrived as a live array (fresh validation) or as
   the stored JSON string (a row read back from the sheet). */
function ekSlotsOf_(v) {
  if (Object.prototype.toString.call(v) === "[object Array]") return v;
  if (typeof v === "string" && v) {
    try { var parsed = JSON.parse(v); return Object.prototype.toString.call(parsed) === "[object Array]" ? parsed : []; }
    catch (e) { return []; }
  }
  return [];
}

function ekAvailabilityText_(slots) {
  return (slots || []).map(function (s) { return s.day + " " + s.from + "-" + s.to; }).join("; ");
}

/* The three legacy columns that a six-step client derives from chips and
   selects rather than typing: subject, languages, experience. Deriving them
   HERE as well as in the browser means an old client, a hand-made curl, or
   a page whose schema file failed to load still produces a complete row —
   and the "subject is needed" refusal only fires when the tutor really did
   not say what they teach. */
function ekDeriveLegacy_(fields) {
  var out = {};
  for (var k in fields) if (Object.prototype.hasOwnProperty.call(fields, k)) out[k] = fields[k];

  var subjects = Object.prototype.toString.call(out.subjects) === "[object Array]" ? out.subjects : [];
  if (!out.subject && subjects.length) {
    out.subject = subjects.join(", ").slice(0, 60);
  }
  var teach = Object.prototype.toString.call(out.teach_langs) === "[object Array]" ? out.teach_langs : [];
  if (!out.languages && (teach.length || out.hindi_level || out.english_level || out.other_langs)) {
    var bits = [];
    if (teach.length) bits.push(teach.join(", "));
    if (out.hindi_level) bits.push("Hindi: " + out.hindi_level);
    if (out.english_level) bits.push("English: " + out.english_level);
    if (out.other_langs) bits.push(out.other_langs);
    out.languages = bits.join(", ").slice(0, 120);
  }
  if (!out.experience && (out.years || Object.prototype.toString.call(out.levels) === "[object Array]")) {
    var exp = [];
    if (out.years) exp.push(out.years);
    var levels = Object.prototype.toString.call(out.levels) === "[object Array]" ? out.levels : [];
    if (levels.length) exp.push("Teaches: " + levels.join(", "));
    out.experience = exp.join(" \u00b7 ").slice(0, 300);
  }
  return out;
}

function ekValidateApplication_(fields, meta) {
  fields = ekDeriveLegacy_(fields || {});
  meta = meta || {};
  var errors = {};
  var values = {};
  var details = {};
  var known = {};
  /* Which client fields were ACTUALLY present in this payload. A resubmit
     that leaves an optional answer out must not blank the stored one, so the
     merge step needs to tell "the tutor cleared this" (present but empty)
     apart from "this request did not mention it" (absent). */
  var supplied = {};
  var suppliedAny = 0;
  /* A server-owned column name that a client sent is not "unknown" — it is
     RESERVED. Without this, the overflow rule below files the applicant's
     text in details_json under a reviewer-shaped key ("status", "approved",
     "review_notes"), which never moves the real cell but reads as if it did.
     Recorded (truncated, inert) under a `sent_` prefix instead, so nothing
     is silently binned and nothing can be mistaken for a verdict. */
  var reserved = {};
  var reservedNames = {};
  for (var rs = 0; rs < EKGURU_SERVER_ONLY.length; rs++) reservedNames[EKGURU_SERVER_ONLY[rs]] = 1;
  /* submission_id has no column of its own: it is bookkeeping that lives in
     details_json and is written by the server at the end of the write, on both
     the insert and the update path. If it were treated as a free-text answer,
     an applicant could choose the value the retry lookup matches on, and a
     later unrelated submission carrying the same value would be answered
     "already received" without being stored or acknowledged. Reserved here so
     the server's value always wins; the client's attempt is kept inertly under
     sent_submission_id. */
  reservedNames.submission_id = 1;

  for (var i = 0; i < EKGURU_APPLICATION_FIELDS.length; i++) {
    var f = EKGURU_APPLICATION_FIELDS[i];
    if (!f.src) continue;
    known[f.src] = 1;
    if (EKGURU_SERVER_ONLY.indexOf(f.col) !== -1) continue;   /* ignored, not trusted */

    var raw = fields[f.src];
    if (raw !== undefined) { supplied[f.src] = 1; suppliedAny++; }
    var isList = f.type === "list";
    var isJson = f.type === "json";

    if (isList) {
      if (raw == null || raw === "") { values[f.src] = []; continue; }
      if (Object.prototype.toString.call(raw) !== "[object Array]") {
        errors[f.src] = "must be a list";
        continue;
      }
      if (f.maxItems && raw.length > f.maxItems) { errors[f.src] = "has too many items"; continue; }
      var list = [];
      var tooLong = false;
      for (var j = 0; j < raw.length; j++) {
        var item = ekCleanText_(raw[j]);
        if (!item) continue;
        if (f.itemMax && item.length > f.itemMax) { tooLong = true; break; }
        if (list.indexOf(item) === -1) list.push(item);
      }
      if (tooLong) { errors[f.src] = "has an item that is too long"; continue; }
      values[f.src] = list;
      continue;
    }

    if (isJson) {
      if (raw == null || raw === "") { values[f.src] = ""; continue; }
      /* Accept both shapes: an already-serialised string (what a client
         sends), and a live object/array (what availability_slots is after
         validation). Everything is stored as a compact JSON string, because
         a Sheet cell in a dropdown column would otherwise keep
         "[object Object]". */
      var packed = "";
      if (typeof raw === "string") {
        try { packed = JSON.stringify(JSON.parse(raw)); }
        catch (e) { errors[f.src] = "is not valid JSON"; continue; }
      } else {
        try { packed = JSON.stringify(raw); } catch (e2) { packed = ""; }
      }
      if (!packed || packed === "null") { errors[f.src] = "is not valid JSON"; continue; }
      if (f.max && packed.length > f.max) { errors[f.src] = "is too large"; continue; }
      values[f.src] = packed;
      continue;
    }

    var s = ekCleanText_(raw);
    if (!s) {
      if (f.required) { errors[f.src] = "is needed"; continue; }
      values[f.src] = "";
      continue;
    }
    if (f.max && s.length > f.max) { errors[f.src] = "is too long (max " + f.max + " characters)"; continue; }

    if (f.type === "email") {
      if (!ekIsEmail_(s)) { errors[f.src] = "does not look like an email address"; continue; }
      s = s.toLowerCase();
    } else if (f.type === "url") {
      if (!ekIsUrl_(s)) { errors[f.src] = "must start with https://"; continue; }
    } else if (f.type === "int") {
      var n = Number(s);
      if (!isFinite(n) || Math.round(n) !== n) { errors[f.src] = "must be a whole number"; continue; }
      if (f.min != null && n < f.min) { errors[f.src] = "must be at least " + f.min; continue; }
      if (f.max != null && n > f.max) { errors[f.src] = "must be at most " + f.max; continue; }
      s = String(n);
    } else if (f.type === "phone") {
      /* Accept the shapes people actually type: +91 98765 43210, 09876543210,
         (91) 98765-43210, +44 7700 900123. A leading "+" means the country
         code is explicit and is KEPT. Without a "+" the digits are kept as
         typed (an Indian 10-digit number stays 10 digits); we never invent a
         country code, because guessing one is how a number silently becomes
         wrong. */
      /* ekCleanText_ prefixes "= + - @" with an apostrophe to defuse formula
         injection. For a number that would corrupt a legitimate leading "+"
         into "'+91…", so undo exactly that one case here — the value that
         follows is digits only, which cannot be a formula. */
      var raw = String(fields[f.src] == null ? "" : fields[f.src]).trim();
      var plus = /^\+/.test(raw) || /^'\+/.test(s);
      var digits = s.replace(/[^0-9]/g, "");
      if (digits.length < 7 || digits.length > 15) {
        errors[f.src] = "should be 7 to 15 digits, including the country code";
        continue;
      }
      s = (plus ? "+" : "") + digits;
    } else if (f.type === "enum") {
      var want = ekNormDash(s).toLowerCase();
      var hit = "";
      for (var k = 0; k < (f.values || []).length; k++) {
        if (ekNormDash(f.values[k]).toLowerCase() === want) { hit = f.values[k]; break; }
      }
      if (!hit) { errors[f.src] = "is not one of the allowed options"; continue; }
      s = hit;
    }
    values[f.src] = s;
  }

  /* ---- availability (has its own column and a legacy text twin) ---- */
  var av = ekValidateAvailability_(fields.availability_slots);
  if (av.error) errors["availability_slots"] = av.error;
  /* Stored as ONE json string, not a live JS array: availability_json is a
     dropdown-typed column in the sheet, and a live array would be saved as
     "[object Object]" — which is unreadable for the owner and unparseable
     for the site. The array itself is still returned to the caller in
     values.availability_slots, which is what the row builder and the
     legacy `availability` text are built from. */
  values.availability_slots = JSON.stringify(av.slots || []);

  /* ---- server-only keys a client might try to send ----
     A name in EKGURU_SERVER_ONLY is never a free-text answer, whether or not
     the schema also gives it a client `src` (status/reference have none, so
     `known` alone would miss them). Diverted here, recorded under sent_. */
  var ignored = [];
  for (var key in fields) {
    if (!Object.prototype.hasOwnProperty.call(fields, key)) continue;
    if (known[key]) { if (reservedNames[key]) reserved[key] = 1; continue; }
    if (reservedNames[key]) { reserved[key] = 1; continue; }   /* a column we own, not a free-text answer */
    ignored.push(key);
  }

  /* ---- unknown keys land in details_json, never in the bin ---- */
  var detailSource = fields.details;
  if (detailSource && typeof detailSource === "object") {
    for (var dk in detailSource) {
      if (!Object.prototype.hasOwnProperty.call(detailSource, dk)) continue;
      if (known[dk]) { if (reservedNames[dk]) reserved[dk] = 1; continue; }
      if (reservedNames[dk]) { reserved[dk] = 1; continue; }
      ignored.push(dk);
    }
  }
  var used = 0;
  for (var u = 0; u < ignored.length; u++) {
    var name = String(ignored[u]);
    if (name === "details") continue;
    var val = fields[name];
    if (detailSource && typeof detailSource === "object" && detailSource[name] !== undefined) {
      val = detailSource[name];
    }
    var dv = typeof val === "string" ? ekCleanText_(val) : String(val == null ? "" : val);
    if (!dv) continue;
    if (used >= EKGURU_DETAILS_MAX_KEYS) break;
    details[name.slice(0, 40)] = dv.slice(0, EKGURU_DETAILS_MAX_VALUE);
    used++;
  }
  /* Reserved names are recorded, never honoured: "sent_review_notes" cannot
     be mistaken for the reviewer's own note. */
  for (var rk in reserved) {
    if (!Object.prototype.hasOwnProperty.call(reserved, rk)) continue;
    var rv = ekCleanText_(String(fields[rk] == null ? "" : fields[rk]));
    if (!rv) continue;
    if (used >= EKGURU_DETAILS_MAX_KEYS) break;
    details[("sent_" + rk).slice(0, 40)] = rv.slice(0, EKGURU_DETAILS_MAX_VALUE);
    used++;
  }
  values.details = Object.keys(details).length ? details : null;

  /* ---- consent: the server's own copy of the truth ---- */
  if (meta.consent !== true) errors.consent = "is needed so we can reply to you";
  if (meta.consent_privacy !== true) errors.consent_privacy = "is needed before we store your details";

  var keys = Object.keys(errors);
  if (keys.length) {
    var first = keys[0];
    return {
      error: first.replace(/_json$/, "").replace(/_/g, " ") + " " + errors[first],
      fields: errors
    };
  }
  values.__supplied = supplied;
  values.__suppliedAny = suppliedAny;
  return { values: values };
}

/* ---------------------------------------------------------------------------
   ROW BUILDING
   ---------------------------------------------------------------------------
   The row is built from the SCHEMA, position by position, using the header
   map of the live tab. A schema column that the payload has no value for is
   written as "" — the sheet stays rectangular and an admin reading row 400
   sees the same columns as row 2.
   -------------------------------------------------------------------------- */

function ekBool_(v) { return v === true || String(v).toLowerCase() === "true" || String(v) === "1" ? "yes" : "no"; }

function ekBuildRow_(map, values, meta) {
  var now = ekNow_();
  var row = [];
  var width = 0;
  for (var c in map) { if (map[c] + 1 > width) width = map[c] + 1; }

  for (var i = 0; i < width; i++) row.push("");

  function put(col, v) {
    var at = map[col];
    if (at === undefined) return;
    row[at] = v;
  }

  /* --- what the client sent, by column --- */
  for (var k = 0; k < EKGURU_APPLICATION_FIELDS.length; k++) {
    var f = EKGURU_APPLICATION_FIELDS[k];
    if (!f.src) continue;
    if (EKGURU_SERVER_ONLY.indexOf(f.col) !== -1) continue;
    var v = values[f.src];
    if (v === undefined) continue;
    if (f.type === "list") {
      put(f.col, v.length ? JSON.stringify(v) : "");
    } else if (f.type === "json") {
      put(f.col, v || "");
    } else if (f.type === "int") {
      put(f.col, v === "" ? "" : Number(v));
    } else {
      put(f.col, v == null ? "" : v);
    }
  }

  /* --- derived: the legacy human-readable twins --- */
  var slots = ekSlotsOf_(values.availability_slots);
  var avText = ekAvailabilityText_(slots);
  if (!values.availability && avText) {
    var tz = values.timezone || "";
    put("availability", (avText + (tz ? " | " + tz : "")).slice(0, 400));
  }
  /* "absent OR empty", not `== null`: validation sets "" for a payload that
     did not mention availability_meta, so an `== null` test could never fire
     and a non-browser client got a filled availability_json next to an empty
     availability_meta. A client-supplied value is still respected. */
  if (values.availability_meta == null || values.availability_meta === "") {
    put("availability_meta", slots.length ? JSON.stringify({
      days: slots.length,
      slots: slots.length,
      timezone: values.timezone || "",
      format: "weekly-hours"
    }) : "");
  }
  if (!values.currency) put("currency", "USD");
  if (!values.duration) put("duration", "50 min");
  if (!values.source) put("source", "join.html");

  /* --- system + consent --- */
  put("timestamp", now);
  put("created_at", now);
  put("updated_at", now);
  put("schema_version", EKGURU_SCHEMA_VERSION);
  put("status", ekInitialStatus());
  put("approved", "");
  put("consent_privacy", meta.consent_privacy === true ? "yes" : "no");
  put("consent_terms", meta.consent === true ? "yes" : "no");
  put("declaration", "true and mine");
  put("consent_at", now);
  put("email_status", "");
  put("details_json", values.details ? JSON.stringify(values.details) : "");

  return row;
}

/* A reference that is not already in the tab. 6 characters from a 31-letter
   alphabet (no 0/O/1/I/L) so a person can read it down the phone. */
function ekNewRef_(tab, map) {
  var chars = "23456789ABCDEFGHJKMNPQRSTUVWXYZ";
  var at = map.reference;
  var existing = null;
  if (at !== undefined && tab.getLastRow() > 1) {
    existing = {};
    var col = tab.getRange(2, at + 1, tab.getLastRow() - 1, 1).getValues();
    for (var i = 0; i < col.length; i++) {
      var r = String(col[i][0] || "").trim().toUpperCase();
      if (r) existing[r] = 1;
    }
  }
  for (var attempt = 0; attempt < 12; attempt++) {
    var s = "";
    for (var c = 0; c < 6; c++) s += chars.charAt(Math.floor(Math.random() * chars.length));
    var ref = "EG-" + s;
    if (!existing || !existing[ref]) return ref;
  }
  /* Astronomically unlikely; still never silently reuse one. */
  return "EG-" + String(new Date().getTime()).slice(-6);
}

function ekRowToObject_(map, row) {
  var out = {};
  for (var col in map) {
    out[col] = row[map[col]] === undefined ? "" : row[map[col]];
  }
  return out;
}

/* Find a row by reference. Returns {index, row, obj} (index is 1-based sheet
   row) or null. One column read to find it, one short read for the row. */
function ekFindByRef_(tab, map, reference) {
  var at = map.reference;
  if (at === undefined) return null;
  var want = String(reference || "").trim().toUpperCase();
  if (!want) return null;
  var last = tab.getLastRow();
  if (last < 2) return null;
  var col = tab.getRange(2, at + 1, last - 1, 1).getValues();
  for (var i = 0; i < col.length; i++) {
    if (String(col[i][0] || "").trim().toUpperCase() === want) {
      var rowIndex = i + 2;
      var width = tab.getLastColumn();
      var row = tab.getRange(rowIndex, 1, 1, width).getValues()[0];
      return { index: rowIndex, row: row, obj: ekRowToObject_(map, row) };
    }
  }
  return null;
}

/* ---------------------------------------------------------------------------
   SUBMIT
   ---------------------------------------------------------------------------
   One application, one row. Three cases:
     1. the same submission_id arrives twice (a retry after a timeout, a
        double tap) → the existing row is returned, nothing written;
     2. the same email arrives again within EK_DEDUPE_HOURS → the row is
        UPDATED in place: the applicant keeps their reference, and the
        owner's decisions (status, approved, review columns) are preserved;
     3. anything else → a new row.
   The whole thing runs under the script lock, because two applicants
   submitting in the same second must not both pass the duplicate scan.
   -------------------------------------------------------------------------- */
function ekSubmitApplication_(body) {
  var fields = body.fields || {};
  var meta = {
    consent: body.consent === true,
    consent_privacy: body.consent_privacy === true || body.consent === true
  };
  var check = ekValidateApplication_(fields, meta);
  if (check.error) {
    return ekJson_({ ok: false, error: check.error, fields: check.fields || {} });
  }
  var values = check.values;
  var submissionId = String(body.submission_id || "").slice(0, 60).replace(/[^A-Za-z0-9._-]/g, "");

  var lock = LockService.getScriptLock();
  if (!lock.tryLock(25000)) {
    return ekJson_({ ok: false, error: "the form is very busy, please try again in a moment" });
  }
  try {
    var tab = ekTab_();
    var map = ekHeaderMap_(tab).map;

    /* --- 1. who is calling, decided on the server --- */
    /* Identity comes from the submitted answers, not from anything the client
       chose to call itself. The email is the applicant's own verified-format
       answer and is what every other path in this file already keys on, so it
       is the natural scope for a retry. `submission_id` is only an ATTEMPT
       token: it may say "this is the same attempt as before", it may never say
       "this is the same person as someone else". */
    var email = String(values.email || "").toLowerCase();
    var own = ekFindRecentByEmail_(tab, map, email);
    var scope = { row: own ? own.index : 0 };

    /* --- 2. the same submission, retried --- */
    if (submissionId) {
      var dup = ekFindSubmission_(tab, map, submissionId, scope);
      if (dup) {
        return ekJson_({ ok: true, reference: dup, duplicate: true, mail: "skipped" });
      }
    }

    /* --- 3. the same person, correcting their application --- */
    var prior = own;
    if (prior) {
      var kept = ekUpdateExisting_(tab, map, prior, values, submissionId);
      return ekJson_({ ok: true, reference: kept.reference, duplicate: true, updated: true, mail: "skipped" });
    }

    /* --- 4. a new application --- */
    var ref = ekNewRef_(tab, map);
    var row = ekBuildRow_(map, values, meta);
    if (map.reference !== undefined) row[map.reference] = ref;
    if (map.submission_id !== undefined && submissionId) row[map.submission_id] = submissionId;
    /* The retry key is server bookkeeping, not an answer. ekBuildRow_ has
       already serialised the free-text details cell, so fold the server's own
       value in here: without this the first submission stored no retry key at
       all, and a client-supplied value could stand in for it and decide what a
       later submission is matched against. Written last, so the server wins on
       both the insert path and the update path (ekUpdateExisting_). */
    if (map.details_json !== undefined) {
      var dj = {};
      var rawDj = row[map.details_json];
      if (rawDj) {
        try {
          var parsedDj = JSON.parse(String(rawDj));
          if (parsedDj && typeof parsedDj === "object") dj = parsedDj;
        } catch (e) { dj = {}; }
      }
      if (submissionId) dj.submission_id = submissionId;
      row[map.details_json] = Object.keys(dj).length ? JSON.stringify(dj) : "";
    }
    tab.appendRow(row);

    var mail = ekSendApplicationMail_(ref, "received", values);
    var answer = { ok: true, reference: ref, duplicate: false, mail: mail };
    if (mail !== "sent") answer.mail_note = "your application is saved; our acknowledgement email may be delayed";
    return ekJson_(answer);
  } finally {
    lock.releaseLock();
  }
}

/* Retry lookup — see ekSubmitApplication_ for how identity is scoped.
   ---------------------------------------------------------------------------
   The client's submission_id lives in details_json (no column of its own, so
   no schema churn for a value only used for retry detection).

   `scope` (v2.0.2) is the applicant's own row, resolved on the SERVER from the
   submitted email. Without it this scan searched every row in the tab, which
   let one applicant's id decide what another applicant's submission would be
   matched against: a value planted in row A made a later submission carrying
   the same value look like a retry of row A, so it was acknowledged as
   "already received" without being stored or emailed. Scoped to the caller's
   own row the same value can only ever match that caller's own submission,
   which is the only thing a retry key is entitled to mean.

   `scope.row` null  -> the email has no row of its own; nothing to match.
   `scope.row` set   -> search that one row.
   Used only for the row pick; the returned reference still names the row. */
function ekFindSubmission_(tab, map, submissionId, scope) {
  var last = tab.getLastRow();
  if (last < 2) return "";
  var dj = map.details_json, rf = map.reference;
  if (dj === undefined || rf === undefined) return "";
  /* Fail closed: without a caller-supplied scope the old tab-wide scan would
     come back, so refuse to match anything rather than match too much. */
  if (!scope || !scope.row) return "";
  var rows = tab.getRange(2, 1, last - 1, tab.getLastColumn()).getValues();
  for (var i = rows.length - 1; i >= 0; i--) {
    if (i + 2 !== scope.row) continue;                 /* only the caller's own row */
    var raw = String(rows[i][dj] || "");
    if (raw.indexOf(submissionId) === -1) continue;
    var parsed = null;
    try { parsed = JSON.parse(raw); } catch (e) { parsed = null; }
    if (parsed && String(parsed.submission_id || "") === submissionId) {
      return String(rows[i][rf] || "");
    }
  }
  return "";
}

function ekFindRecentByEmail_(tab, map, email) {
  var last = tab.getLastRow();
  if (last < 2 || !email) return null;
  var em = map.email, ts = map.timestamp, rf = map.reference;
  if (em === undefined || ts === undefined) return null;
  var rows = tab.getRange(2, 1, last - 1, tab.getLastColumn()).getValues();
  var cutoff = new Date().getTime() - EK_DEDUPE_HOURS * 3600 * 1000;
  for (var i = rows.length - 1; i >= 0; i--) {
    if (String(rows[i][em] || "").trim().toLowerCase() !== email) continue;
    var when = new Date(rows[i][ts]).getTime();
    /* An unreadable timestamp must not turn into "infinitely recent". */
    if (!isFinite(when) || when < cutoff) continue;
    var status = String(rows[i][map.status] || "").toLowerCase();
    if (status === "superseded") continue;
    return { index: i + 2, row: rows[i], obj: ekRowToObject_(map, rows[i]), reference: String(rows[i][rf] || "") };
  }
  return null;
}

/* Write the new answers over the old ones, keeping every decision a human
   has made. Returns {reference}. */
function ekUpdateExisting_(tab, map, prior, values, submissionId) {
  var meta = { consent: true, consent_privacy: true };
  var fresh = ekBuildRow_(map, values, meta);
  var keep = ["reference", "status", "approved", "review_notes", "rejection_reason",
              "reviewed_by", "reviewed_at", "previous_status", "email_status",
              "email_sent_at", "created_at", "timestamp"];
  var index = prior.index;
  var width = tab.getLastColumn();
  for (var i = 0; i < keep.length; i++) {
    var at = map[keep[i]];
    if (at === undefined) continue;
    fresh[at] = prior.row[at];
  }

  /* ---- MERGE, do not overwrite -------------------------------------------
     ekBuildRow_ writes "" for every schema column the payload did not carry.
     Written over an existing row that silently ERASES answers the applicant
     gave last time but left out this time (headline, certs, photo_link,
     linkedin…). So for every client field the request did not mention, the
     stored value is kept.

     "Mentioned but empty" is treated as a deliberate clear and DOES blank the
     cell, because that is what a tutor emptying a box means. Absent means
     "not asked again", which is not the same thing.

     Server-computed columns (the derived legacy twins, availability text,
     schema_version, defaults) are left as ekBuildRow_ produced them: they are
     recomputed from the merged answers and are never a source of truth on
     their own.
     -------------------------------------------------------------------- */
  var supplied = values.__supplied || {};
  for (var fi = 0; fi < EKGURU_APPLICATION_FIELDS.length; fi++) {
    var fdef = EKGURU_APPLICATION_FIELDS[fi];
    if (!fdef.src) continue;
    if (EKGURU_SERVER_ONLY.indexOf(fdef.col) !== -1) continue;
    if (supplied[fdef.src]) continue;                 /* the tutor answered it now */
    var colAt = map[fdef.col];
    if (colAt === undefined) continue;
    var was = prior.row[colAt];
    if (was === undefined || was === null || was === "") continue;
    fresh[colAt] = was;
  }
  /* details_json merges the same way: old keys survive unless overwritten. */
  var mergedDetails = {};
  if (map.details_json !== undefined) {
    try {
      var oldRaw = prior.row[map.details_json];
      var oldObj = oldRaw ? JSON.parse(String(oldRaw)) : null;
      if (oldObj && typeof oldObj === "object") {
        for (var ok in oldObj) if (Object.prototype.hasOwnProperty.call(oldObj, ok)) mergedDetails[ok] = oldObj[ok];
      }
    } catch (e) { /* an unparseable cell must never block a resubmit */ }
  }

  var now = ekNow_();
  if (map.updated_at !== undefined) fresh[map.updated_at] = now;
  if (map.details_json !== undefined) {
    var details = values.details || {};
    for (var dk in mergedDetails) if (Object.prototype.hasOwnProperty.call(mergedDetails, dk)) {
      if (details[dk] === undefined) details[dk] = mergedDetails[dk];
    }
    if (submissionId) details.submission_id = submissionId;
    fresh[map.details_json] = Object.keys(details).length ? JSON.stringify(details) : "";
  }
  /* A tutor who corrects their application after being asked for changes is
     ready to be looked at again. Their status only moves forward from
     needs_information — it never resets an approval. */
  var status = String(prior.row[map.status] || "").toLowerCase();
  if (status === "needs_information" && map.status !== undefined) {
    fresh[map.status] = "under_review";
    if (map.previous_status !== undefined) fresh[map.previous_status] = status;
  }
  tab.getRange(index, 1, 1, width).setValues([fresh]);
  return { reference: prior.reference };
}

/* ---------------------------------------------------------------------------
   EMAIL
   ---------------------------------------------------------------------------
   Four transitions, four templates. Rules that are enforced here, not by
   convention:
     · a submission only ever triggers "received" — never "approved";
     · "rejected" is only ever sent from ekSetStatus_ AFTER a human supplied
       a reason, and the reason is the one on the row;
     · each transition is sent at most once per reference: the row records
       email_status as "<transition>:sent <stamp>" / "<transition>:failed <why>"
       and a repeat of the same transition is a no-op;
     · a quota or transport failure is recorded on the row and NEVER fails
       the submission — the application is already saved.
   -------------------------------------------------------------------------- */

function ekMailSent_(to, subject, html, text, replyTo) {
  var name = ekFromName_();
  if (typeof GmailApp !== "undefined" && GmailApp.sendEmail) {
    var opts = { htmlBody: html, name: name };
    if (replyTo) opts.replyTo = replyTo;
    GmailApp.sendEmail(to, subject, text, opts);
    return;
  }
  if (typeof MailApp !== "undefined" && MailApp.sendEmail) {
    MailApp.sendEmail({ to: to, subject: subject, body: text, htmlBody: html, name: name });
    return;
  }
  throw new Error("no mail service");
}

function ekEscape_(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

/* One responsive template shell, so all four mails look like EkGuru and a
   plain-text version always exists. Inline CSS only: Gmail strips <style>. */
function ekEmailShell_(heading, bodyHtml, footNote) {
  return '<div style="margin:0;padding:0;background:#f6f6fb">' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f6f6fb;padding:24px 12px">' +
    '<tr><td align="center">' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" ' +
    'style="max-width:560px;background:#ffffff;border:1px solid #e8e9f3;border-radius:14px;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif">' +
    '<tr><td style="padding:22px 24px 6px;font-size:15px;font-weight:700;color:#5b3df5">EkGuru</td></tr>' +
    '<tr><td style="padding:0 24px 8px;font-size:20px;font-weight:700;color:#111827;line-height:1.3">' + ekEscape_(heading) + '</td></tr>' +
    '<tr><td style="padding:0 24px 22px;font-size:15px;line-height:1.65;color:#374151">' + bodyHtml + '</td></tr>' +
    '<tr><td style="padding:14px 24px 22px;border-top:1px solid #eef0f6;font-size:12px;line-height:1.6;color:#6b7280">' +
    footNote + '<br>EkGuru · One Student. One Goal. One Guru.<br>' +
    '<a href="' + ekEscape_(ekSiteUrl_()) + '" style="color:#5b3df5">' + ekEscape_(ekSiteUrl_()) + '</a>' +
    '</td></tr></table></td></tr></table></div>';
}

function ekPara_(t) { return '<p style="margin:0 0 12px">' + t + '</p>'; }

function ekTemplate_(kind, ref, f) {
  var name = ekEscape_(f.name || "there");
  var site = ekEscape_(ekSiteUrl_());
  var refLine = '<p style="margin:0 0 12px;font-size:13px;color:#6b7280">Reference ' +
    '<b style="color:#111827;letter-spacing:.5px">' + ekEscape_(ref) + '</b></p>';

  if (kind === "received") {
    var html =
      ekPara_("Hello " + name + ",") +
      ekPara_("Thank you — your tutor application has reached us and is saved.") +
      refLine +
      ekPara_("<b>A person reads every application.</b> Nothing you sent is public yet, and it will not be " +
        "published until we have reviewed it and agreed your profile with you.") +
      ekPara_("What happens next: we usually reply within 3–5 working days. If we need a photo, a video or a " +
        "correction we will say so in that email and tell you exactly what to send.") +
      ekPara_("You can reply to this email at any time — please keep your reference in the subject line.") +
      ekPara_('<a href="' + site + '" style="color:#5b3df5">Visit EkGuru</a>');
    var text =
      "Hello " + (f.name || "there") + ",\n\n" +
      "Thank you — your tutor application has reached us and is saved.\n\n" +
      "Reference: " + ref + "\n\n" +
      "A person reads every application. Nothing you sent is public yet, and it will not be published " +
      "until we have reviewed it and agreed your profile with you.\n\n" +
      "What happens next: we usually reply within 3–5 working days. If we need a photo, a video or a " +
      "correction we will say so in that email and tell you exactly what to send.\n\n" +
      "You can reply to this email at any time — please keep your reference in the subject line.\n\n" +
      "EkGuru · " + ekSiteUrl_() + "\n";
    return { subject: "Your EkGuru tutor application is with us (" + ref + ")", html: html, text: text };
  }

  if (kind === "approved") {
    var htmlA =
      ekPara_("Hello " + name + ",") +
      ekPara_("<b>Good news — your EkGuru tutor application has been approved.</b>") +
      refLine +
      ekPara_("What happens next:") +
      '<ol style="margin:0 0 12px 20px;padding:0">' +
      "<li style=\"margin-bottom:6px\">We prepare your public profile from the details you sent.</li>" +
      "<li style=\"margin-bottom:6px\">We email you the finished profile to check <b>before</b> it goes live.</li>" +
      "<li>Once you confirm it, your profile appears on Find Tutors and you can receive lesson requests.</li>" +
      "</ol>" +
      ekPara_("Nothing is published until you have seen the profile and said yes to it.") +
      ekPara_("If any of your details have changed since you applied — price, availability, city — reply to this " +
        "email and we will update them before publishing.");
    var textA =
      "Hello " + (f.name || "there") + ",\n\n" +
      "Good news — your EkGuru tutor application has been approved.\n\n" +
      "Reference: " + ref + "\n\n" +
      "What happens next:\n" +
      "1. We prepare your public profile from the details you sent.\n" +
      "2. We email you the finished profile to check BEFORE it goes live.\n" +
      "3. Once you confirm it, your profile appears on Find Tutors and you can receive lesson requests.\n\n" +
      "Nothing is published until you have seen the profile and said yes to it.\n\n" +
      "If any of your details have changed since you applied — price, availability, city — reply to this " +
      "email and we will update them before publishing.\n\n" +
      "EkGuru · " + ekSiteUrl_() + "\n";
    return { subject: "Your EkGuru tutor application is approved (" + ref + ")", html: htmlA, text: textA };
  }

  if (kind === "rejected") {
    var reason = String(f.rejection_reason || "").trim();
    var reasonHtml = reason
      ? '<div style="margin:0 0 14px;padding:12px 14px;background:#faf7ff;border-left:3px solid #5b3df5;' +
        'font-size:14px;color:#374151">' + ekEscape_(reason).replace(/\n/g, "<br>") + "</div>"
      : "";
    var htmlR =
      ekPara_("Hello " + name + ",") +
      ekPara_("Thank you for applying to teach Hindi with EkGuru, and for the time you put into the form.") +
      refLine +
      ekPara_("After reading your application we are not able to take it forward at the moment.") +
      (reasonHtml ? ekPara_("<b>This is why:</b>") + reasonHtml
                  : ekPara_("<b>This is why:</b> we could not confirm enough of the details we need to " +
                            "publish a tutor profile responsibly.")) +
      ekPara_("If that is something you can change, you are very welcome to apply again once you have it — " +
        "you can use the same form, and you do not need to mention this email.") +
      ekPara_("If you think we have got something wrong, reply to this email and tell us — a person will read it.");
    var textR =
      "Hello " + (f.name || "there") + ",\n\n" +
      "Thank you for applying to teach Hindi with EkGuru, and for the time you put into the form.\n\n" +
      "Reference: " + ref + "\n\n" +
      "After reading your application we are not able to take it forward at the moment.\n\n" +
      "This is why:\n" + (reason || "we could not confirm enough of the details we need to publish a tutor " +
        "profile responsibly.") + "\n\n" +
      "If that is something you can change, you are very welcome to apply again once you have it — you can " +
      "use the same form, and you do not need to mention this email.\n\n" +
      "If you think we have got something wrong, reply to this email and tell us — a person will read it.\n\n" +
      "EkGuru · " + ekSiteUrl_() + "\n";
    return { subject: "About your EkGuru tutor application (" + ref + ")", html: htmlR, text: textR };
  }

  if (kind === "needs_information") {
    var ask = String(f.review_notes || "").trim();
    var askHtml = ask
      ? '<div style="margin:0 0 14px;padding:12px 14px;background:#fffdf3;border-left:3px solid #b45309;' +
        'font-size:14px;color:#374151">' + ekEscape_(ask).replace(/\n/g, "<br>") + "</div>"
      : "";
    var htmlN =
      ekPara_("Hello " + name + ",") +
      ekPara_("We have started reading your application and we need a little more information " +
        "before we can finish it.") +
      refLine +
      (askHtml ? ekPara_("<b>What we need:</b>") + askHtml
               : ekPara_("<b>What we need:</b> a little more detail about your teaching experience " +
                         "and your weekly availability.")) +
      ekPara_("You do not need to fill the whole form in again. Reply to this email with the missing " +
        "details, or open the form and send it once more with the corrections — we will match it to your " +
        "reference.") +
      ekPara_("Your application stays saved and nothing is published while we wait.");
    var textN =
      "Hello " + (f.name || "there") + ",\n\n" +
      "We have started reading your application and we need a little more information before we can " +
      "finish it.\n\n" +
      "Reference: " + ref + "\n\n" +
      "What we need:\n" + (ask || "a little more detail about your teaching experience and your weekly " +
        "availability.") + "\n\n" +
      "You do not need to fill the whole form in again. Reply to this email with the missing details, or " +
      "open the form and send it once more with the corrections — we will match it to your reference.\n\n" +
      "Your application stays saved and nothing is published while we wait.\n\n" +
      "EkGuru · " + ekSiteUrl_() + "\n";
    return { subject: "We need a little more information (" + ref + ")", html: htmlN, text: textN };
  }

  return null;
}

/* Send one notification for one application. `extra` carries the review
   reason/notes for the transitions that use them. Best effort: the return
   value is "sent", "skipped", "failed" or "off" and never throws. */
function ekSendApplicationMail_(ref, kind, f, extra) {
  if (!ekMailEnabled_()) return "off";
  var to = String((f && f.email) || "").trim();
  if (!ekIsEmail_(to)) return "skipped";
  var merged = {};
  for (var k in f) if (Object.prototype.hasOwnProperty.call(f, k)) merged[k] = f[k];
  extra = extra || {};
  for (var e in extra) if (Object.prototype.hasOwnProperty.call(extra, e)) merged[e] = extra[e];

  var tpl = ekTemplate_(kind, ref, merged);
  if (!tpl) return "skipped";
  try {
    ekMailSent_(to, tpl.subject, tpl.html, tpl.text, ekOwnerInbox_());
    ekNoteEmail_(ref, kind, "sent", "");
    return "sent";
  } catch (err) {
    /* Quota exceeded is the usual cause. Log the fact, not the address. */
    ekNoteEmail_(ref, kind, "failed", String(err && err.message ? err.message : "error").slice(0, 80));
    return "failed";
  }
}

/* Write the delivery outcome onto the row, and use it as the duplicate guard:
   if the row already says "<kind>:sent", the caller must not send it again. */
function ekNoteEmail_(ref, kind, outcome, why) {
  try {
    var tab = ekTab_();
    var map = ekHeaderMap_(tab).map;
    var found = ekFindByRef_(tab, map, ref);
    if (!found) return;
    var stamp = ekStamp_(ekNow_());
    var line = kind + ":" + outcome + " " + stamp + (why ? " (" + why + ")" : "");
    if (map.email_status !== undefined) {
      tab.getRange(found.index, map.email_status + 1, 1, 1).setValue(line.slice(0, 300));
    }
    if (outcome === "sent" && map.email_sent_at !== undefined) {
      tab.getRange(found.index, map.email_sent_at + 1, 1, 1).setValue(ekNow_());
    }
  } catch (err) { /* a note must never break a send */ }
}

function ekAlreadyMailed_(rowObj, kind) {
  return String(rowObj.email_status || "").indexOf(kind + ":sent") === 0;
}

/* ---------------------------------------------------------------------------
   ADMIN — status changes
   ---------------------------------------------------------------------------
   Called only from an owner-held token. Every change records who, when, from
   what, to what, and why; then triggers that transition's email exactly once.
   -------------------------------------------------------------------------- */

function ekSetStatus_(reference, toStatus, opts) {
  opts = opts || {};
  var admin = String(opts.admin || "").slice(0, 120) || "owner";
  var reason = String(opts.reason || "").slice(0, 1000);
  var note = String(opts.note || "").slice(0, 2000);
  var to = String(toStatus || "").toLowerCase().trim();

  if (EKGURU_STATUSES.indexOf(to) === -1) {
    return { ok: false, error: "unknown status" };
  }
  /* A rejection without a reason would produce the exact email the brief
     forbids: a rejection that does not say why. Refuse it here, where the
     admin sees the message, rather than send something hollow. */
  if (to === "rejected" && !reason) {
    return { ok: false, error: "a rejection needs a reason — it is the reason the applicant is emailed" };
  }
  if (to === "needs_information" && !note) {
    return { ok: false, error: "say what is missing, so the email can ask for it" };
  }

  var lock = LockService.getScriptLock();
  if (!lock.tryLock(20000)) return { ok: false, error: "busy, try again" };
  try {
    var tab = ekTab_();
    var map = ekHeaderMap_(tab).map;
    var found = ekFindByRef_(tab, map, reference);
    if (!found) return { ok: false, error: "no application with that reference" };

    var from = String(found.obj.status || "pending").toLowerCase();
    if (from === to) {
      /* --- retry of a transition email that failed -------------------------
         A status change is emailed exactly once. If that send failed (quota,
         transport), the row says "<transition>:failed …" and the owner is
         left with an approved applicant who was never told. `retry_mail`
         re-attempts ONLY that missing email: the status does not move, and a
         transition that already shows ":sent" is never emailed again.

         Deliberately opt-in (retry_mail: true) rather than automatic on every
         repeat call, so a stray double-click cannot send anything. */
      var retryKind = ekMailFor(to);
      var answer = { ok: true, unchanged: true, status: to, mail: "skipped" };
      if (opts.retry_mail === true && retryKind) {
        if (ekAlreadyMailed_(found.obj, retryKind)) {
          answer.mail = "already sent";
          answer.already_sent = true;
          return answer;
        }
        var who = {
          name: found.obj.name, email: found.obj.email,
          rejection_reason: found.obj.rejection_reason, review_notes: found.obj.review_notes
        };
        answer.mail = ekSendApplicationMail_(reference, retryKind, who, {});
        answer.retried = true;
        return answer;
      }
      return answer;
    }
    if (!ekCanMove(from, to)) {
      return { ok: false, error: "cannot move an application from " + from + " to " + to };
    }

    var now = ekNow_();
    function put(col, v) {
      if (map[col] !== undefined) tab.getRange(found.index, map[col] + 1, 1, 1).setValue(v);
    }
    put("status", to);
    put("previous_status", from);
    put("reviewed_by", admin);
    put("reviewed_at", now);
    put("updated_at", now);
    put("approved", to === "approved" ? "yes" : "");
    if (to === "rejected") put("rejection_reason", reason);
    if (note) put("review_notes", note);

    /* Re-read so the email carries the stored reason, not a local variable. */
    var after = ekFindByRef_(tab, map, reference);
    var obj = after ? after.obj : found.obj;
    var kind = ekMailFor(to);
    var mail = "skipped";
    if (kind && !ekAlreadyMailed_(obj, kind)) {
      var who = {
        name: obj.name, email: obj.email,
        rejection_reason: obj.rejection_reason, review_notes: obj.review_notes
      };
      mail = ekSendApplicationMail_(reference, kind, who, {});
    }
    return { ok: true, reference: String(obj.reference || reference), from: from, to: to,
             mail: mail, reviewed_by: admin, at: ekIso_(now) };
  } finally {
    lock.releaseLock();
  }
}

function ekAdminUpdate_(body) {
  var token = String(body.token || "");
  var want = ekAdminToken_();
  if (!want) {
    return ekJson_({ ok: false, error: "admin actions are switched off: set the EK_ADMIN_TOKEN script property" });
  }
  if (!token || token !== want) {
    return ekJson_({ ok: false, error: "not authorised" });
  }
  var out = ekSetStatus_(String(body.reference || ""), String(body.status || ""), {
    admin: ekProp_("EK_ADMIN_NAME", "owner"),
    reason: body.reason,
    note: body.note,
    retry_mail: body.retry_mail === true
  });
  return ekJson_(out);
}

/* ---------------------------------------------------------------------------
   APPLICANT STATUS LOOKUP
   ---------------------------------------------------------------------------
   Reference + the email that applied. Both must match (case-insensitive on
   the address). The answer carries the status and when it was last touched —
   never the row, never the reviewer's private notes, never the rejection
   text (that is in the email, which is the place for it).
   -------------------------------------------------------------------------- */
function ekStatusLookup_(body) {
  var ref = String(body.reference || "").trim();
  var email = String(body.email || "").trim().toLowerCase();
  if (!ref || !ekIsEmail_(email)) return ekJson_({ ok: false, error: "reference and email are both needed" });

  var lock = LockService.getScriptLock();
  if (!lock.tryLock(15000)) return ekJson_({ ok: false, error: "busy, try again" });
  try {
    var tab = ekTab_();
    var map = ekHeaderRead_(tab).map;
    var found = ekFindByRef_(tab, map, ref);
    /* Same answer for "no such reference" and "wrong email", so the endpoint
       cannot be used to test whether a reference exists. */
    if (!found || String(found.obj.email || "").trim().toLowerCase() !== email) {
      return ekJson_({ ok: false, error: "no application matches that reference and email" });
    }
    var status = String(found.obj.status || "").toLowerCase();
    return ekJson_({
      ok: true,
      reference: String(found.obj.reference || ref),
      status: status,
      updated_at: String(found.obj.updated_at || found.obj.timestamp || ""),
      next: status === "approved" ? "we will email your profile before it goes live"
          : status === "rejected" ? "see the email we sent about this application"
          : status === "needs_information" ? "check your inbox — we asked for a detail"
          : "a person is reading it"
    });
  } finally {
    lock.releaseLock();
  }
}

/* ---------------------------------------------------------------------------
   ROUTER SEAMS
   ---------------------------------------------------------------------------
   These two functions are what Unified.gs / Intake.gs call. Returning null
   means "not mine, carry on with the old behaviour".
   -------------------------------------------------------------------------- */

function ekApplicationAction_(body) {
  if (!body) return null;
  var action = String(body.action || "");
  if (action === "ekAdminUpdate") return ekAdminUpdate_(body);
  if (action === "ekStatus") return ekStatusLookup_(body);
  if (action === "ekHealth") return ekJson_(ekHealth_());
  if (body.kind === "application") {
    /* The honeypot has already been checked by whichever router called this
       seam (Unified.gs, or Intake.gs for standalone deployments), and both do
       it BEFORE the seam, so anything reaching here is treated as a person.

       The hourly/daily cap used to live only in the router's shared
       intakeQuota_(), which this seam returns BEFORE. A test posting 40
       applications was accepted 40 times with INTAKE_HOURLY_CAP = 30. The
       counter is incremented here, before any row is written and before any
       email leaves, so a flood cannot fill the tab or the mailbox.

       A resubmit by the same person is not counted: it updates their existing
       row instead of creating a new one. */
    var cap = ekApplicationQuota_();
    if (!cap.ok) return ekJson_({ ok: false, error: cap.error });
    return ekSubmitApplication_(body);
  }
  return null;
}

/* ---------------------------------------------------------------------------
   RATE LIMIT — per hour and per day, site-wide, for the whole application kind
   --------------------------------------------------------------------------
   Deliberately simple and shared-state based (the script cache), the same
   mechanism intakeQuota_() uses, so there is one place to reason about. The
   caps are the ones already documented for this project; they are NOT new
   limits invented for this change.
   -------------------------------------------------------------------------- */
function ekApplicationQuota_() {
  var hourly = 30;
  var daily = 200;
  var cache = null;
  try { cache = CacheService.getScriptCache(); } catch (err) { cache = null; }
  if (!cache) return { ok: true };              /* never fail closed on a cache miss */
  var now = ekNow_();
  var day = Utilities.formatDate(now, "GMT+05:30", "yyyyMMdd");
  var hour = Utilities.formatDate(now, "GMT+05:30", "yyyyMMddHH");
  var hKey = "ek-app-h-" + hour;
  var dKey = "ek-app-d-" + day;
  var h = 0, d = 0;
  try { h = Number(cache.get(hKey) || 0); d = Number(cache.get(dKey) || 0); } catch (err) { h = 0; d = 0; }
  if (h >= hourly) return { ok: false, error: "too many applications in the last hour, please try again a little later" };
  if (d >= daily) return { ok: false, error: "too many applications today, please email us instead" };
  try {
    cache.put(hKey, String(h + 1), 3700);
    cache.put(dKey, String(d + 1), 90000);
  } catch (err) { /* a cache write failure must not block a real application */ }
  return { ok: true };
}

function ekApplicationGet_(e) {
  var p = (e && e.parameter) || {};
  if (String(p.action || "").toLowerCase() !== "ekhealth") return null;
  return ekJson_(ekHealth_());
}

function ekHealth_() {
  var out = {
    ok: true,
    version: EK_APP_VERSION,
    schema: EKGURU_SCHEMA_VERSION,
    mail: ekMailEnabled_() ? "on" : "off",
    admin: ekAdminToken_() ? "configured" : "not configured",
    columns: null,
    rows: 0
  };
  try {
    /* create=false: this is a READ. A monitoring GET must never create the
       tab it is reporting on. */
    var tab = ekTab_(false);
    if (!tab) {
      out.ok = false;
      out.columns = { expected: EKGURU_APPLICATION_HEADER.length, present: 0,
                      missing: EKGURU_APPLICATION_HEADER.slice() };
      out.rows = 0;
      out.error = "there is no applications tab yet; the first application creates it";
      return out;
    }
    out.rows = Math.max(0, tab.getLastRow() - 1);
    out.columns = ekColumnReport_(tab);
    /* Health must report a half-migrated tab as NOT ok, or the owner will
       deploy a backend that silently writes into the wrong shape. */
    out.ok = out.columns.missing.length === 0;
    if (!out.ok) out.error = "applications tab is missing " + out.columns.missing.length + " column(s); run ekMigrateApplications";
  } catch (err) {
    out.ok = false;
    out.error = "could not read the applications tab";
  }
  return out;
}

function ekJson_(obj) {
  if (typeof intakeJson_ === "function") return intakeJson_(obj);
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

/* Editor-only smoke test: validates a payload the way the wizard would send
   it, without writing a row and without sending an email. Run it before
   deploying changes. */
function ekSelfTest() {
  var sample = {
    kind: "application", consent: true, consent_privacy: true, website: "",
    fields: {
      name: "Test Tutor", email: "test@example.com", city: "Jaipur", country: "India",
      subject: "Conversational Hindi", bio: "A sample bio used by the self test only.",
      rate_usd: 9, timezone: "Asia/Kolkata",
      availability_slots: [{ day: "Mon", from: "19:00", to: "21:00" }],
      subjects: ["Conversational Hindi"], levels: ["Children"]
    }
  };
  var check = ekValidateApplication_(sample.fields, { consent: true, consent_privacy: true });
  if (check.error) {
    Logger.log("SELF TEST FAILED at validation: %s", check.error);
    return { ok: false, error: check.error };
  }
  var tab = ekTab_();
  var map = ekHeaderMap_(tab).map;
  var row = ekBuildRow_(map, check.values, { consent: true, consent_privacy: true });
  var empty = [];
  for (var i = 0; i < row.length; i++) if (row[i] === "" || row[i] === null) empty.push(i);
  Logger.log("SELF TEST OK — %s columns filled, %s empty, availability text %s",
    row.length - empty.length, empty.length, ekAvailabilityText_(check.values.availability_slots));
  Logger.log("SELF TEST schema %s, applications tab %s/%s columns", EKGURU_SCHEMA_VERSION,
    ekColumnReport_(tab).present, EKGURU_APPLICATION_HEADER.length);
  return { ok: true, columns: row.length, values: check.values };
}

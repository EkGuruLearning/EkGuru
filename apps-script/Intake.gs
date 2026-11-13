/**
 * ============================================================================
 * EkGuru: INTAKE (applications, reviews, sign-ups, bookings, contact)  ·  write-only, pending-only
 * ============================================================================
 * Lets a visitor send a tutor application, a student review, a learner
 * sign-up, a lesson booking or a contact message straight from the site,
 * without a server of ours. Every submission
 * lands as a PENDING row in this workbook. Nothing here ever reaches the
 * public site by itself:
 *
 *   applications   ->  you check the person, then set approved = yes in the
 *                      tutors tab (or add the row there) to publish them
 *   reviews_pending->  you check the review, then copy it into the reviews tab
 *                      with status = live. A review must carry the booking
 *                      reference of a booking that exists for that tutor, so a
 *                      review cannot be written by someone who never booked.
 *   contacts        ->  contact-form messages, private, reply material only
 *   bookings        ->  lesson booking requests, the owner-side booking record
 *   signups        ->  private. Used only to send the learner a reply and to
 *                      count interest. Never published, never sent back out.
 *
 * SEPARATE PROJECT ON PURPOSE. Paste this into its OWN Apps Script project.
 * It does not share a doPost with the mailer or the questions API, because
 * two doPost functions in one project will not compile.
 *
 * ⚠️ BOUND PROJECT, OR THE SHEET NEVER SEES A ROW. Open it from the
 * EkGuru DB sheet itself (that sheet → Extensions → Apps Script) so
 * SpreadsheetApp.getActiveSpreadsheet() finds the workbook. A standalone
 * project has no active workbook; intakeSpreadsheet_() then falls back to
 * the EKGURU_DB_SPREADSHEET_ID script property and refuses (health reports
 * "spreadsheetBound":false) if neither is set. Deploy:
 *
 *     Execute as:      Me
 *     Who has access:  Anyone
 *
 * Then paste the /exec URL into js/site-config.js as  intake: { url: "…" }.
 *
 * THE CONTRACT WITH js/intake.js
 * ------------------------------
 *   GET   ?action=health      → {"ok":true,"tabs":{…counts…}}  (counts only)
 *   POST  Content-Type text/plain, body = JSON string:
 *         {"kind":"application"|"review"|"signup"|"booking"|"contact",
 *          "consent":true,
 *          "website":"",                    (honeypot: must stay empty)
 *          "fields":{…}}
 *         → {"ok":true,"reference":"EG-7K3Q9A"}
 *         → {"ok":false,"error":"…"}
 *
 * WHY text/plain: an Apps Script web app cannot answer a CORS preflight, so the
 * browser sends a simple request and this script parses the string itself.
 *
 * WHAT IS CHECKED (server side, always; the browser checks too, for speed)
 * ----------------------------------------------------------------------
 *   · the kind is one of five known kinds
 *   · consent is true (the person has agreed that we keep and reply to them)
 *   · the honeypot is empty (bots fill every box)
 *   · every field has a length limit and a type (email, enum, plain text)
 *   · at most HOURLY_CAP and DAILY_CAP submissions per kind, for the whole site
 *     (there is no reliable IP on Apps Script, so the cap is global; it stops a
 *     flood, it does not identify a spammer)
 *   · the payload is at most 12 KB
 *
 * WHAT IS NEVER DONE
 *   · no field is echoed back, except a short random reference
 *   · no IP address, user agent or cookie is stored
 *   · no row is written to the public tabs (tutors, reviews, settings, support)
 *   · the feed (LiveFeed.gs) serves only its own four tabs, so none of these
 *     three tabs can leak through it
 *
 * HONEST LIMITS
 *   · A determined spammer can still fill the pending tabs up to the cap. Look
 *     at the pending tabs once a week and delete junk rows.
 *   · Deleting a row does not delete a copy in your Gmail or the sheet's
 *     version history. Tell the person if you remove their data on request.
 * ============================================================================
 */

"use strict";

var INTAKE_VERSION = "1.2.0";
var INTAKE_MAX_BYTES = 12000;
var INTAKE_HOURLY_CAP = 30;   /* per kind, whole site */
var INTAKE_DAILY_CAP = 150;   /* per kind, whole site */

/* Every field the site may send, with its rule. Anything not listed is dropped. */
var INTAKE_KINDS = {
  application: {
    tab: "applications",
    header: ["timestamp", "reference", "status", "approved", "name", "email", "city", "country",
             "subject", "experience", "rate_usd", "availability", "bio", "photo_link",
             "video_link", "languages", "notes"],
    fields: {
      name:         { type: "text",  max: 80,   required: true },
      email:        { type: "email", max: 120,  required: true },
      city:         { type: "text",  max: 80 },
      country:      { type: "text",  max: 60 },
      subject:      { type: "text",  max: 60,   required: true },
      experience:   { type: "text",  max: 300 },
      rate_usd:     { type: "int",   min: 1, max: 200 },
      availability: { type: "text",  max: 300 },
      bio:          { type: "text",  max: 1500, required: true },
      photo_link:   { type: "url",   max: 300 },
      video_link:   { type: "url",   max: 300 },
      languages:    { type: "text",  max: 120 },
      notes:        { type: "text",  max: 500 }
    }
  },
  review: {
    tab: "reviews_pending",
    header: ["timestamp", "reference", "status", "tutor_id", "reviewer_name", "stars",
             "text", "lesson_date", "contact_email", "booking_id", "notes"],
    fields: {
      tutor_id:      { type: "slug",  max: 60,  required: true },
      reviewer_name: { type: "text",  max: 60,  required: true },
      stars:         { type: "int",   min: 1, max: 5, required: true },
      text:          { type: "text",  max: 800, required: true },
      lesson_date:   { type: "date" },
      contact_email: { type: "email", max: 120 },
      /* GENUINE-REVIEW GATE (v1.2.0). The reviewer must enter the booking
         reference they were given when they booked the lesson. The server
         then checks that a booking row exists in the bookings tab with that
         booking_ref AND that row's tutor_id matches the tutor under review.
         A review without a matching booking is refused: it keeps the review
         list a record of real students, not of strangers. */
      booking_id:    { type: "text",  max: 20,  required: true }
    }
  },
  /* Contact-form messages (v1.2.0). Same contract as the other kinds:
     pending row for the owner, nothing echoed back except a reference. */
  contact: {
    tab: "contacts",
    header: ["timestamp", "reference", "status", "name", "email", "subject",
             "topic", "message", "page", "ref"],
    fields: {
      name:    { type: "text",  max: 80,  required: true },
      email:   { type: "email", max: 120, required: true },
      subject: { type: "text",  max: 120 },
      topic:   { type: "text",  max: 60 },
      message: { type: "text",  max: 4000, required: true },
      page:    { type: "url",   max: 300 }
    }
  },
  signup: {
    tab: "signups",
    header: ["timestamp", "reference", "status", "name", "email", "goal", "level", "source", "notes"],
    fields: {
      name:   { type: "text",  max: 60 },
      email:  { type: "email", max: 120, required: true },
      goal:   { type: "enum",  values: ["Speak with family", "Travel", "Work", "Study", "Culture", "Just curious"], required: true },
      level:  { type: "enum",  values: ["Never studied", "A1 to A2", "B1 and above", "Not sure"] },
      source: { type: "text",  max: 60 }
    }
  },
  /* A lesson booking request. Columns match the "bookings" tab, which
     keeps every detail the booking email carries, so nothing is lost if
     an email is deleted or a mail provider fails. */
  booking: {
    tab: "bookings",
    header: ["booking_ref", "requested_at", "tutor_id", "student_name", "student_email",
             "student_whatsapp", "preferred_times_ist", "status", "confirmed_time_ist",
             "tutor_reply_at", "notes", "lesson", "price_usd", "student_level", "student_goal",
             "student_timezone", "source_page", "tutor_email", "sent_via", "email_delivery"],
    fields: {
      booking_ref:        { type: "text",  max: 20,  required: true },
      tutor_id:           { type: "slug",  max: 60,  required: true },
      student_name:       { type: "text",  max: 60,  required: true },
      student_email:      { type: "email", max: 120, required: true },
      student_whatsapp:   { type: "text",  max: 30 },
      preferred_times_ist:{ type: "text",  max: 120, required: true },
      lesson:             { type: "text",  max: 60 },
      price_usd:          { type: "text",  max: 12 },
      student_level:      { type: "text",  max: 60 },
      student_goal:       { type: "text",  max: 200 },
      student_timezone:   { type: "text",  max: 60 },
      source_page:        { type: "url",   max: 300 },
      tutor_email:        { type: "email", max: 120 },
      sent_via:           { type: "text",  max: 60 },
      email_delivery:     { type: "text",  max: 120 }
    }
  }
};

/* ----------------------------------------------------------------------------
   Entry points
   -------------------------------------------------------------------------- */
function doGet(e) {
  var action = String((e && e.parameter && e.parameter.action) || "health");
  if (action !== "health") return intakeJson_({ ok: false, error: "unknown action" });
  return intakeJson_(intakeHealth_());
}

function doPost(e) {
  try {
    var raw = String((e && e.postData && e.postData.contents) || "");
    if (!raw) return intakeJson_({ ok: false, error: "empty request" });
    if (raw.length > INTAKE_MAX_BYTES) return intakeJson_({ ok: false, error: "too large" });

    var body;
    try { body = JSON.parse(raw); } catch (err) { return intakeJson_({ ok: false, error: "not JSON" }); }

    /* Honeypot: a real person never sees this box. Pretend success, store nothing. */
    if (String(body.website || "").trim() !== "") {
      return intakeJson_({ ok: true, reference: "EG-" + intakeRef_() });
    }

    var kind = String(body.kind || "");
    var spec = INTAKE_KINDS[kind];
    if (!spec) return intakeJson_({ ok: false, error: "unknown kind" });
    if (body.consent !== true) return intakeJson_({ ok: false, error: "consent is needed so we can reply to you" });

    var clean = intakeValidate_(spec, body.fields || {});
    if (clean.error) return intakeJson_({ ok: false, error: clean.error });

    /* GENUINE-REVIEW GATE — verify the booking reference against the
       bookings tab BEFORE anything is written. If the booking does not
       exist (or belongs to another tutor), the review is refused and
       nothing lands in reviews_pending. */
    if (kind === "review") {
      var gate = intakeReviewGate_(clean.values.booking_id, clean.values.tutor_id);
      if (!gate.ok) return intakeJson_({ ok: false, error: gate.error });
    }

    var quota = intakeQuota_(kind);
    if (!quota.ok) return intakeJson_({ ok: false, error: quota.error });

    var ref = intakeRef_();
    var saved = intakeAppend_(kind, spec, ref, clean.values);
    /* A booking is confirmed by its own booking_ref (the same code the
       student sees and the email carries), not by a second server code. */
    return intakeJson_({ ok: true, reference: saved.reference, duplicate: saved.duplicate === true });
  } catch (err) {
    /* never leak a stack trace or a field value to the visitor */
    return intakeJson_({ ok: false, error: "could not save, please email us instead" });
  }
}

/* ----------------------------------------------------------------------------
   Validation
   -------------------------------------------------------------------------- */
function intakeValidate_(spec, fields) {
  var out = {};
  var names = Object.keys(spec.fields);
  for (var i = 0; i < names.length; i++) {
    var name = names[i];
    var rule = spec.fields[name];
    var raw = fields[name];
    var s = raw === undefined || raw === null ? "" : String(raw).trim();

    if (!s) {
      if (rule.required) return { error: name.replace(/_/g, " ") + " is needed" };
      out[name] = "";
      continue;
    }
    if (s.length > (rule.max || 500)) return { error: name.replace(/_/g, " ") + " is too long" };

    if (rule.type === "email") {
      if (!/^[^\s@<>"']+@[^\s@<>"']+\.[^\s@<>"']{2,}$/.test(s)) return { error: "that email does not look right" };
    } else if (rule.type === "url") {
      if (!/^https:\/\/[^\s<>"']+$/.test(s)) return { error: name.replace(/_/g, " ") + " must start with https://" };
    } else if (rule.type === "int") {
      var n = Math.round(Number(s));
      if (!isFinite(n) || n < rule.min || n > rule.max) return { error: name.replace(/_/g, " ") + " must be a whole number from " + rule.min + " to " + rule.max };
      s = String(n);
    } else if (rule.type === "slug") {
      if (!/^[a-z0-9][a-z0-9-]{1,59}$/.test(s)) return { error: "tutor id is not valid" };
    } else if (rule.type === "date") {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) return { error: "date must be YYYY-MM-DD" };
    } else if (rule.type === "enum") {
      if (rule.values.indexOf(s) === -1) return { error: name.replace(/_/g, " ") + " is not one of the options" };
    } else {
      /* plain text: no markup, no formula injection */
      s = s.replace(/[<>]/g, "");
      if (/^[=+\-@]/.test(s)) s = "'" + s;
    }
    out[name] = s;
  }
  return { values: out };
}

/* ----------------------------------------------------------------------------
   Genuine-review gate (v1.2.0)
   The review's booking_id must match a row in the bookings tab whose
   tutor_id is the tutor being reviewed. Read-only: never writes.
   ---------------------------------------------------------------------------- */
function intakeReviewGate_(bookingId, tutorId) {
  var id = String(bookingId || "").trim();
  if (!id) return { ok: false, error: "booking reference is needed to verify this review" };
  try {
    var ss = intakeSpreadsheet_();
    var tab = ss.getSheetByName(INTAKE_KINDS.booking.tab);
    if (!tab) return { ok: false, error: "that booking reference was not found" };
    var last = tab.getLastRow();
    if (last < 2) return { ok: false, error: "that booking reference was not found" };
    /* Column A is booking_ref, column C is tutor_id. Read the column pair
       at once — one getRange pair, not a per-row read. */
    var refs = tab.getRange(2, 1, last - 1, 1).getValues();
    var tutors = tab.getRange(2, 3, last - 1, 1).getValues();
    for (var i = 0; i < refs.length; i++) {
      if (String(refs[i][0] || "").trim() === id) {
        var tid = String((tutors[i] && tutors[i][0]) || "").trim();
        if (tid === String(tutorId || "").trim()) return { ok: true };
        /* The booking exists but for a different tutor: the reviewer may
           have mistyped the reference, or is reviewing the wrong tutor. */
        return { ok: false, error: "that booking reference belongs to a different tutor" };
      }
    }
    return { ok: false, error: "that booking reference was not found" };
  } catch (err) {
    /* A gate failure must not take the whole intake down; fail closed
       (refuse the review) rather than write an unverified one. */
    return { ok: false, error: "we could not verify that booking reference, so the review was not saved" };
  }
}

/* ----------------------------------------------------------------------------
   Quota. Stored in CacheService (cleared after its window), no identity.
   -------------------------------------------------------------------------- */
function intakeQuota_(kind) {
  var cache = CacheService.getScriptCache();
  var day = Utilities.formatDate(new Date(), "GMT+05:30", "yyyyMMdd");
  var hour = Utilities.formatDate(new Date(), "GMT+05:30", "yyyyMMddHH");
  var hKey = "intake-h-" + kind + "-" + hour;
  var dKey = "intake-d-" + kind + "-" + day;
  var h = Number(cache.get(hKey) || 0);
  var d = Number(cache.get(dKey) || 0);
  if (h >= INTAKE_HOURLY_CAP) return { ok: false, error: "too many in the last hour, please try again later" };
  if (d >= INTAKE_DAILY_CAP) return { ok: false, error: "too many today, please email us instead" };
  cache.put(hKey, String(h + 1), 3700);
  cache.put(dKey, String(d + 1), 90000);
  return { ok: true };
}

/* ----------------------------------------------------------------------------
   Storage
   -------------------------------------------------------------------------- */
/* WHICH WORKBOOK. getActive() only works when this project is BOUND to a
   sheet (EkGuru DB -> Extensions -> Apps Script). A standalone project
   created at script.google.com returns null there, and v1.0.0 then failed
   EVERY submission with "could not save" — a booking could look sent and
   still never reach the sheet. v1.1.0 therefore also accepts the workbook
   id from a Script Property (Project Settings -> Script Properties):
       EKGURU_DB_SPREADSHEET_ID = <the id in the EkGuru DB sheet URL>
   No workbook id is hard-coded in this file. */
function intakeSpreadsheet_() {
  var ss = null;
  try { ss = SpreadsheetApp.getActiveSpreadsheet(); } catch (err) {}
  if (ss) return ss;
  var props = PropertiesService.getScriptProperties();
  var id = String(props.getProperty("EKGURU_DB_SPREADSHEET_ID") ||
                  props.getProperty("INTAKE_SPREADSHEET_ID") || "").trim();
  if (id) return SpreadsheetApp.openById(id);
  throw new Error("Intake is not connected to a spreadsheet: bind this " +
    "project to the EkGuru DB sheet, or set the EKGURU_DB_SPREADSHEET_ID script property.");
}

function intakeAppend_(kind, spec, ref, values) {
  var ss = intakeSpreadsheet_();
  /* One writer at a time: two students booking in the same second must
     not race appendRow / the duplicate scan below. */
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    return intakeAppendLocked_(kind, spec, ref, values, ss);
  } finally {
    lock.releaseLock();
  }
}

function intakeAppendLocked_(kind, spec, ref, values, ss) {
  var tab = ss.getSheetByName(spec.tab);
  if (!tab) tab = ss.insertSheet(spec.tab);
  /* A tab that exists but is still empty (created by hand, or by an
     earlier half-finished setup) gets its header first — otherwise the
     first booking becomes the "header" row and is invisible to filters,
     tables and the dashboard counts that assume row 1 is the header. */
  if (tab.getLastRow() === 0) {
    tab.appendRow(spec.header);
    tab.setFrozenRows(1);
  }
  var isBooking = (spec === INTAKE_KINDS.booking);
  var ownRef = isBooking ? (values.booking_ref || ("EK-" + ref)) : ("EG-" + ref);
  /* Idempotency for bookings: a double-click, a browser retry after a
     timeout, or a re-opened modal re-sends the SAME booking_ref. Scan
     column A and answer success without writing a second row, so one
     booking is always exactly one sheet row. */
  if (isBooking && tab.getLastRow() > 1) {
    var refs = tab.getRange(2, 1, tab.getLastRow() - 1, 1).getValues();
    for (var i = 0; i < refs.length; i++) {
      if (String(refs[i][0] || "").trim() === ownRef) {
        return { reference: ownRef, duplicate: true };
      }
    }
  }
  /* One applicant, one row. If this email already applied, the newest
     application replaces the old details in place (the applicant keeps the
     first reference; the owner's status and approved cells are kept). */
  if (spec === INTAKE_KINDS.application && tab.getLastRow() > 1) {
    var wanted = String(values.email || "").trim().toLowerCase();
    var emailAt = spec.header.indexOf("email");
    if (wanted) {
      var rows = tab.getRange(2, 1, tab.getLastRow() - 1, spec.header.length).getValues();
      for (var r = rows.length - 1; r >= 0; r--) {
        if (String(rows[r][emailAt] || "").trim().toLowerCase() === wanted) {
          return intakeUpdateApplicationRow_(tab, spec, r + 2, rows[r], new Date(), values);
        }
      }
    }
  }
  var when = new Date();
  var row = spec.header.map(function (h) {
    if (h === "timestamp") return when;
    if (h === "requested_at") {
      return Utilities.formatDate(when, "Asia/Kolkata", "yyyy-MM-dd HH:mm") + " IST";
    }
    if (h === "reference") return "EG-" + ref;
    if (h === "booking_ref") return values.booking_ref || ("EK-" + ref);
    if (h === "status") return spec === INTAKE_KINDS.booking ? "requested" : "pending";
    if (h === "approved") return "";
    if (h === "notes") return values.notes || "";
    return values[h] !== undefined ? values[h] : "";
  });
  tab.appendRow(row);
  return { reference: ownRef, duplicate: false };
}

/* Rewrites an existing application row with the newest submitted details.
   Kept from the old row: the reference (so the applicant's first reference
   still works), status and approved (the owner's decisions). */
function intakeUpdateApplicationRow_(tab, spec, rowNumber, oldRow, when, values) {
  var keep = { reference: true, status: true, approved: true };
  var row = spec.header.map(function (h, idx) {
    if (keep[h]) return oldRow[idx];
    if (h === "timestamp") return when;
    if (h === "requested_at") {
      return Utilities.formatDate(when, "Asia/Kolkata", "yyyy-MM-dd HH:mm") + " IST";
    }
    if (h === "notes") return values.notes || oldRow[idx] || "";
    return values[h] !== undefined ? values[h] : "";
  });
  tab.getRange(rowNumber, 1, 1, row.length).setValues([row]);
  return { reference: String(oldRow[spec.header.indexOf("reference")] || ""), duplicate: true };
}

function intakeHealth_() {
  var ss;
  try {
    ss = intakeSpreadsheet_();
  } catch (err) {
    /* Health must be able to SAY "not connected" — throwing here would
       only show the owner a generic Apps Script error page. */
    return { ok: false, version: INTAKE_VERSION, spreadsheetBound: false,
             error: "not connected to a spreadsheet (bind the project to the " +
                    "EkGuru DB sheet or set EKGURU_DB_SPREADSHEET_ID)" };
  }
  var tabs = {};
  Object.keys(INTAKE_KINDS).forEach(function (k) {
    var name = INTAKE_KINDS[k].tab;
    var t = ss.getSheetByName(name);
    tabs[name] = t ? Math.max(0, t.getLastRow() - 1) : 0;
  });
  return { ok: true, version: INTAKE_VERSION, spreadsheetBound: true,
           at: new Date().toISOString(), pendingRows: tabs };
}

function intakeRef_() {
  var chars = "23456789ABCDEFGHJKMNPQRSTUVWXYZ";
  var s = "";
  for (var i = 0; i < 6; i++) s += chars.charAt(Math.floor(Math.random() * chars.length));
  return s;
}

function intakeJson_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

/* One-time cleanup for applications that were written before the email
   merge above existed. Run it by hand from the Apps Script editor.
   For every email with more than one row, the NEWEST row stays as it is;
   every older row gets status = "superseded" and a note. Nothing is deleted,
   so the owner can review before removing anything. */
function intakeMarkDuplicateApplications() {
  var spec = INTAKE_KINDS.application;
  var tab = intakeSpreadsheet_().getSheetByName(spec.tab);
  if (!tab || tab.getLastRow() < 3) return { marked: 0 };
  var emailAt = spec.header.indexOf("email");
  var statusAt = spec.header.indexOf("status");
  var notesAt = spec.header.indexOf("notes");
  var rows = tab.getRange(2, 1, tab.getLastRow() - 1, spec.header.length).getValues();
  var newest = {};
  for (var r = 0; r < rows.length; r++) {
    var key = String(rows[r][emailAt] || "").trim().toLowerCase();
    if (!key) continue;
    var ts = new Date(rows[r][spec.header.indexOf("timestamp")]).getTime() || 0;
    if (!newest[key] || ts >= newest[key].ts) newest[key] = { row: r, ts: ts };
  }
  var marked = 0;
  for (var s = 0; s < rows.length; s++) {
    var k = String(rows[s][emailAt] || "").trim().toLowerCase();
    if (!k || newest[k].row === s) continue;
    tab.getRange(s + 2, statusAt + 1).setValue("superseded");
    tab.getRange(s + 2, notesAt + 1).setValue("older duplicate of a newer application (same email)");
    marked++;
  }
  return { marked: marked };
}

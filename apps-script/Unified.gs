/**
 * ============================================================================
 * EkGuru: UNIFIED BACKEND  (live feed + intake, one file, one deployment)
 * ============================================================================
 * WHAT THIS IS
 *   The read side (LIVE FEED: serves the public tabs as CSV) and the write
 *   side (INTAKE: receives applications, reviews, sign-ups, bookings and
 *   contact messages as pending rows) in a SINGLE Apps Script file with a
 *   SINGLE deployment and a SINGLE /exec URL.
 *
 *   Before this file the two halves lived in two projects with two URLs.
 *   Pasting them into one file by hand breaks in two ways that are both
 *   invisible until deploy time: the file ends up with TWO doGet functions
 *   (Apps Script keeps only the last one, so one half silently dies) and
 *   the torn comment between the two halves is a syntax error
 *   ("Unexpected token '*'"). This file is that merge done properly: one
 *   doGet that routes, one doPost, every helper prefixed so nothing
 *   collides. The feed half is byte-identical in behaviour to
 *   apps-script/LiveFeed.gs v1.0.0 and the intake half to
 *   apps-script/Intake.gs v1.2.0 — tools/test-live-feed.js proves it.
 *
 * SETUP (once, about ten minutes)
 *   1. Open the EkGuru DB sheet itself, Extensions, Apps Script. The
 *      project MUST open from that sheet (a bound project). A standalone
 *      project works only if you ALSO do step 6.
 *   2. Delete whatever is in Code.gs and paste THIS whole file.
 *      ⚠️ Do NOT paste this into the payments project (the one whose
 *      Code.gs talks about Razorpay) — two backends in one project break
 *      both. This file belongs to the EkGuru DB workbook, nothing else.
 *   3. Save. The editor must show NO red error. If it does, you pasted
 *      only half the file — select all, paste again.
 *   4. Run selfTest_ once (select it in the toolbar, Run). The log shows
 *      every tab found with its row count, plus intake health. Fix what
 *      it names BEFORE deploying.
 *   5. Deploy, New deployment, Web app. Execute as: Me. Who has access:
 *      Anyone. Copy the /exec URL.
 *   6. (Standalone projects only) Project Settings, Script Properties,
 *      add EKGURU_DB_SPREADSHEET_ID = the id in the EkGuru DB sheet URL.
 *      Bound projects skip this — getActive() already finds the workbook.
 *   7. Paste the SAME /exec URL into js/site-config.js twice: feed.url
 *      AND intake.url. Commit, let Pages deploy. Then open:
 *        <url>?tab=health      feed health (counts only, never contents)
 *        <url>?action=health   intake health (pending-row counts)
 *      Both must say "ok":true. A bare <url> with no parameters answers
 *      a COMBINED health object (feed + intake in one page).
 *   8. Run installTriggers() once, so pasted or imported sheet edits also
 *      clear the 30 second feed cache.
 *   9. UPDATING LATER: paste the new file over the old one, then Manage
 *      deployments, Edit, Version: New version, Deploy. Editing the
 *      EXISTING deployment keeps the URL unchanged — never create a new
 *      deployment for an update, or the site's pasted URL goes stale.
 *
 * THE CONTRACT WITH THE SITE
 *   GET  ?tab=tutors|reviews|settings|support   CSV of that tab (private
 *                                               columns and #help rows removed)
 *   GET  ?tab=tutors&format=json                the same tab as JSON
 *                                               {header, rows} (Section 3)
 *   GET  ?tab=health  (or ?tab=, legacy)        feed health, counts only
 *   GET  ?action=health                         intake health, pending counts
 *   GET  ?action=ping&token=…                   pong, ONLY with the right
 *                                               EK_ADMIN_TOKEN (Section 3)
 *   GET  (bare, no parameters)                  combined feed+intake health
 *   POST Content-Type text/plain, JSON body     one intake submission
 *        {kind, consent:true, website:"", fields} → {ok, reference}
 *        kinds: application | review | signup | booking | contact
 *
 * WHAT IS NEVER DONE (these are load-bearing, not decorative)
 *   · the feed never sends a private column (email, notification_email,
 *     formKey, whatsapp, phone-like names) or a #help row — enforced in
 *     readTab_, so a sheet mistake cannot publish an address
 *   · intake never writes to the public tabs (tutors, reviews, settings,
 *     support) — every submission lands pending/requested for the owner
 *   · intake never echoes a field back — only a short random reference
 *   · intake never stores an IP address, user agent or cookie
 *   · no workbook id and no Razorpay key is hard-coded anywhere here;
 *     the only id the file knows comes from a Script Property you set
 *
 * FUTURE OPTIONS (Section 1: the EK_ block). Every option below is a flag,
 * not new code: flip it, save, redeploy the SAME deployment. Nothing here
 * needs a second file, ever.
 *   maintenance      whole backend answers "in maintenance" (feeds fall
 *                    back to published output; forms show their offline path)
 *   jsonFormat       ?format=json on any feed tab (default ON — additive)
 *   adminPing        token-gated pong for dashboards and uptime monitors
 *   auditLog         every accepted submission also appends one audit row
 *   digest           dailyDigest_() writes one pending-counts row a day
 *                    (needs a daily time trigger installing on that function)
 *   combinedHealth   bare /exec answers feed+intake health together
 *
 * SECTIONS (search for "SECTION n —" to jump)
 *   0  this header                3  future modules (all flag-gated)
 *   1  EK_ config: every knob     4  live feed (from LiveFeed.gs v1.0.0)
 *   2  the router: doGet/doPost   5  intake (from Intake.gs v1.2.0)
 *                                    6  triggers: onEdit, installTriggers
 * ============================================================================
 */

"use strict";

/* ============================================================================
   SECTION 1 — EK_ CONFIG: EVERY KNOB IN ONE PLACE
   ----------------------------------------------------------------------------
   Flip a flag, save, redeploy the SAME deployment (Manage deployments →
   Edit → New version → Deploy). No other edit is ever needed: each flag
   below is read live on every request.
   ========================================================================== */
var EK_UNIFIED_VERSION = "2.0.0";

var EK_ = {
  /* Whole-backend maintenance switch. While true, EVERY GET and POST
     answers {ok:false, error:maintenanceMessage}. The site survives this:
     the loaders fall back to the published tabs and the forms show their
     offline path. Default OFF. */
  maintenance: false,
  maintenanceMessage: "EkGuru backend is in maintenance, please try again in a few minutes.",

  /* ?tab=tutors&format=json answers {ok, tab, header, rows} instead of CSV.
     Same cells, same privacy stripping, read-only. Default ON: it is purely
     additive — no CSV client changes behaviour because of it. */
  jsonFormat: true,

  /* ?action=ping&token=… answers {ok:true, pong:true, unified, at} for
     dashboards and uptime monitors. The token MUST equal the EK_ADMIN_TOKEN
     script property; with no property set (the default) every ping is
     refused as "unknown action", so scanners learn nothing. */
  adminPing: true,

  /* Every ACCEPTED submission also appends one row {at, kind, reference,
     tutor} to the audit tab: a small who-submitted-what journal for the
     owner. It never changes the visitor's response, and a failure writing
     it is swallowed. Default OFF — turn on when you want the journal. */
  auditLog: false,
  auditTab: "audit_log",

  /* dailyDigest_() appends one row of pending-row counts a day to the
     digest tab: "12 applications still waiting" without opening the sheet.
     TWO steps to arm: set this true AND install a daily time trigger on
     dailyDigest_ (Triggers → Add trigger → dailyDigest_ → Time-driven →
     Day timer). Default OFF. It sends no email, ever. */
  digest: false,
  digestTab: "digest_log",

  /* A bare /exec (no tab=, no action=) answers combined feed+intake health
     in one object. Legacy clients always send tab= or action=, so this
     changes nothing for the site. Default ON. */
  combinedHealth: true
};

/* ============================================================================
   SECTION 2 — THE ROUTER: ONE doGet, ONE doPost
   ----------------------------------------------------------------------------
   WHY. Apps Script allows only one doGet and one doPost per project. The old
   setup kept them in two projects; this file keeps them in two FUNCTIONS
   (feedGet_ in Section 4, intakeGet_/intakePost_ in Section 5) and routes:

     a tab= parameter      → the feed (CSV, or JSON with &format=json)
     ?action=health        → intake health (pending-row counts)
     ?action=ping&token=…  → pong iff the token matches EK_ADMIN_TOKEN
     any other action=     → {ok:false, error:"unknown action"}
     neither               → combined health (or legacy feed health)

   If BOTH tab= and action= arrive, tab= wins — no legacy client sends both.
   ========================================================================== */
function doGet(e) {
  if (EK_.maintenance) return intakeJson_({ ok: false, error: EK_.maintenanceMessage });
  var p = (e && e.parameter) || {};
  var tab = String(p.tab || "").toLowerCase();
  var action = String(p.action || "").toLowerCase();

  /* Feed routes — behaviour identical to standalone LiveFeed.gs. */
  if (tab) {
    if (EK_.jsonFormat && String(p.format || "").toLowerCase() === "json" &&
        tab !== "" && tab !== "health") {
      return feedJson_(tab);
    }
    return feedGet_(e);
  }

  /* Intake routes — behaviour identical to standalone Intake.gs. */
  if (action === "health") return intakeGet_(e);
  if (action === "ping") return adminPing_(String(p.token || ""));
  if (action) return intakeJson_({ ok: false, error: "unknown action" });

  /* Bare /exec: combined health. Handy in a browser tab after deploying. */
  if (EK_.combinedHealth) {
    return intakeJson_({
      ok: true,
      unified: EK_UNIFIED_VERSION,
      at: new Date().toISOString(),
      feed: buildHealth_(),
      intake: intakeHealth_()
    });
  }
  return feedGet_(e);
}

function doPost(e) {
  if (EK_.maintenance) return intakeJson_({ ok: false, error: EK_.maintenanceMessage });
  var res = intakePost_(e);

  /* Optional audit row (EK_.auditLog). intakePost_ has already answered;
     this never changes the visitor's response. */
  if (EK_.auditLog) {
    try {
      var body = JSON.parse(String((e && e.postData && e.postData.contents) || "{}"));
      var out = JSON.parse(res.getContent());
      if (out && out.ok && body && body.kind && INTAKE_KINDS[body.kind]) {
        audit_(body, out.reference);
      }
    } catch (err) { /* an audit failure must never fail a submission */ }
  }
  return res;
}

/* ============================================================================
   SECTION 3 — FUTURE MODULES. Every one is flag-gated in EK_ above.
   Nothing here runs unless its flag says so.
   ========================================================================== */

/* ?tab=X&format=json — the same cells the CSV carries (same privacy
   stripping, same #help removal), as {ok, tab, header, rows}. For future
   dashboards and scripts; the site's loaders keep using CSV. */
function feedJson_(tab) {
  if (!FEED_TABS[tab]) {
    return intakeJson_({ ok: false, error: "unknown tab", tabs: Object.keys(FEED_TABS) });
  }
  var t = readTab_(tab);
  return intakeJson_({
    ok: true,
    tab: tab,
    header: t.header,
    rows: t.rows,
    privateColumnsRemoved: t.dropped
  });
}

/* ?action=ping&token=… — pong for dashboards and uptime monitors. Refusals
   deliberately mimic "unknown action" so a scanner cannot tell the ping
   exists. Set the token in Project Settings → Script Properties:
   EK_ADMIN_TOKEN = a long random string only you know. */
function adminPing_(token) {
  var want = "";
  try {
    want = String(PropertiesService.getScriptProperties().getProperty("EK_ADMIN_TOKEN") || "");
  } catch (err) {}
  if (!EK_.adminPing || !want || String(token || "") !== want) {
    return intakeJson_({ ok: false, error: "unknown action" });
  }
  return intakeJson_({ ok: true, pong: true, unified: EK_UNIFIED_VERSION, at: new Date().toISOString() });
}

/* One audit row per accepted submission. Called by the doPost router only
   while EK_.auditLog is true. Columns: at | kind | reference | tutor. */
function audit_(body, reference) {
  var ss = intakeSpreadsheet_();
  var tab = ss.getSheetByName(EK_.auditTab);
  if (!tab) tab = ss.insertSheet(EK_.auditTab);
  if (tab.getLastRow() === 0) {
    tab.appendRow(["at", "kind", "reference", "tutor"]);
    tab.setFrozenRows(1);
  }
  var f = (body && body.fields) || {};
  tab.appendRow([new Date(), String((body && body.kind) || ""),
    String(reference || ""), String(f.tutor_id || f.tutor || "")]);
}

/* One digest row a day: pending counts across the five intake tabs, so the
   owner sees "12 applications still waiting" without opening the sheet.
   Arming takes TWO steps (see EK_.digest): the flag AND a daily time
   trigger on this function. Sends no email, ever. */
function dailyDigest_() {
  if (!EK_.digest) return "digest is off (EK_.digest is false)";
  var ss = intakeSpreadsheet_();
  var tab = ss.getSheetByName(EK_.digestTab);
  if (!tab) tab = ss.insertSheet(EK_.digestTab);
  if (tab.getLastRow() === 0) {
    tab.appendRow(["at", "applications", "reviews_pending", "contacts", "signups", "bookings"]);
    tab.setFrozenRows(1);
  }
  var h = intakeHealth_();
  var p = (h && h.pendingRows) || {};
  tab.appendRow([new Date(), p.applications || 0, p.reviews_pending || 0,
    p.contacts || 0, p.signups || 0, p.bookings || 0]);
  return "digest written";
}

/* Run this from the editor BEFORE deploying (toolbar → selfTest_ → Run).
   It reads every feed tab and the intake health and logs one JSON summary.
   It writes NOTHING (no rows, no tabs) — the only way it can fail is if a
   tab the file needs is missing or the project is not bound to the EkGuru
   DB sheet (see setup step 6 in the header). */
function selfTest_() {
  var out = { unified: EK_UNIFIED_VERSION, tabs: {}, intake: null };
  Object.keys(FEED_TABS).forEach(function (t) {
    try {
      var r = readTab_(t);
      out.tabs[t] = { found: !r.missing, rows: r.rows.length, columns: r.header.length };
    } catch (err) {
      out.tabs[t] = { error: String(err).slice(0, 120) };
    }
  });
  try {
    out.intake = intakeHealth_();
  } catch (err) {
    out.intake = { error: String(err).slice(0, 160) };
  }
  var text = JSON.stringify(out);
  try { Logger.log(text); } catch (err) {}
  return text;
}

/* ==========================================================================
   SECTION 4 - LIVE FEED (behaviour-identical to LiveFeed.gs v1.0.0)
   --------------------------------------------------------------------------
   Only two things changed from the standalone file: the old doGet is now
   feedGet_ (the router in Section 2 calls it), and the cache-clearing
   triggers moved to Section 6. Everything else is verbatim.
   ========================================================================== */
var FEED_VERSION = "1.0.0";
var FEED_CACHE_SECONDS = 30;
var FEED_CACHE_PREFIX = "ekguru-feed-v1:";

/* Tab name (case-insensitive) first, then the permanent gid from the old
   published links as a backstop. (A gid survives renames but not delete-and-recreate: the reviews tab was recreated on 4 Nov 2026, gid 298809212 -> 293675115.) */
var FEED_TABS = {
  tutors:   { names: ["tutors"],                          gid: 1631273256 },
  reviews:  { names: ["reviews"],                         gid: 293675115 },
  settings: { names: ["settings"],                        gid: 1658518385 },
  support:  { names: ["support", "payments", "support-payments"], gid: 1041390059 }
};

/* Columns removed by exact name (case-insensitive). */
var FEED_PRIVATE_EXACT = [
  "email", "notification_email", "notificationemail", "formkey",
  "whatsapp", "phone", "mobile", "contact"
];

/* Columns removed because the name looks sensitive. "key" is NOT in this
   list on purpose: the settings tab has a column called key. */
var FEED_PRIVATE_PATTERN = /phone|mobile|password|passcode|secret|token|aadhaar|aadhar|bank|upi|ifsc|account.?no|card/i;

/* ----------------------------------------------------------------------------
   Feed entry — called by the router doGet() above. Behaviour is identical
   to the standalone LiveFeed.gs: ?tab=tutors|reviews|settings|support serves
   CSV, ?tab=health (or an empty tab) serves feed health JSON.
   -------------------------------------------------------------------------- */
function feedGet_(e) {
  var tab = String((e && e.parameter && e.parameter.tab) || "").toLowerCase();

  if (tab === "" || tab === "health") {
    return jsonOut_(buildHealth_());
  }
  if (!FEED_TABS[tab]) {
    return jsonOut_({ ok: false, error: "unknown tab", tabs: Object.keys(FEED_TABS) });
  }

  var csv = readCached_(tab);
  return ContentService.createTextOutput(csv).setMimeType(ContentService.MimeType.CSV);
}

/* ----------------------------------------------------------------------------
   Cache. 30 seconds, cleared on every edit. A value over 100 KB cannot be
   cached by Apps Script, so it is simply rebuilt each time.
   -------------------------------------------------------------------------- */
function readCached_(tab) {
  var cache = CacheService.getScriptCache();
  var key = FEED_CACHE_PREFIX + tab;
  var hit = cache.get(key);
  if (hit !== null && hit !== undefined) return hit;

  var csv = buildCsv_(tab);
  try { cache.put(key, csv, FEED_CACHE_SECONDS); } catch (err) { /* too large: skip */ }
  return csv;
}

/* ----------------------------------------------------------------------------
   Building the CSV
   -------------------------------------------------------------------------- */
function findSheet_(tab) {
  var spec = FEED_TABS[tab];
  var ss = SpreadsheetApp.getActive();
  var sheets = ss.getSheets();
  var i, n;

  for (i = 0; i < sheets.length; i++) {
    n = String(sheets[i].getName()).trim().toLowerCase();
    if (spec.names.indexOf(n) !== -1) return sheets[i];
  }
  for (i = 0; i < sheets.length; i++) {
    if (sheets[i].getSheetId() === spec.gid) return sheets[i];
  }
  return null;
}

function isPrivateColumn_(header) {
  var h = String(header || "").trim().toLowerCase();
  if (!h) return false;
  if (FEED_PRIVATE_EXACT.indexOf(h) !== -1) return true;
  return FEED_PRIVATE_PATTERN.test(h);
}

/* Returns { header: [...], rows: [[...]], dropped: [...] } with private
   columns and help rows already removed. */
function readTab_(tab) {
  var sheet = findSheet_(tab);
  if (!sheet) return { header: [], rows: [], dropped: [], missing: true };

  var values = sheet.getDataRange().getDisplayValues();
  if (!values.length) return { header: [], rows: [], dropped: [] };

  var header = values[0].map(function (h) { return String(h).trim(); });
  var keep = [];
  var dropped = [];
  header.forEach(function (h, idx) {
    if (isPrivateColumn_(h)) { if (h) dropped.push(h); }
    else keep.push(idx);
  });

  var rows = [];
  for (var r = 1; r < values.length; r++) {
    var row = values[r];
    var first = String(row[0] == null ? "" : row[0]).trim();
    var blank = row.every(function (c) { return String(c).trim() === ""; });
    if (blank) continue;
    if (first.charAt(0) === "#") continue;      /* the help row */
    rows.push(keep.map(function (idx) { return row[idx] === undefined ? "" : row[idx]; }));
  }

  return {
    header: keep.map(function (idx) { return header[idx]; }),
    rows: rows,
    dropped: dropped
  };
}

function csvCell_(v) {
  var s = String(v == null ? "" : v);
  return /[",\r\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}

function buildCsv_(tab) {
  var t = readTab_(tab);
  var lines = [t.header.map(csvCell_).join(",")];
  t.rows.forEach(function (row) { lines.push(row.map(csvCell_).join(",")); });
  return lines.join("\r\n") + "\r\n";
}

/* ----------------------------------------------------------------------------
   Health: counts only. Never any cell contents.
   -------------------------------------------------------------------------- */
function buildHealth_() {
  var out = { ok: true, version: FEED_VERSION, at: new Date().toISOString(), cacheSeconds: FEED_CACHE_SECONDS, tabs: {} };
  Object.keys(FEED_TABS).forEach(function (tab) {
    var t = readTab_(tab);
    var info = { found: !t.missing, rows: t.rows.length, columns: t.header.length, privateColumnsRemoved: t.dropped.length };
    if (tab === "tutors" && !t.missing) {
      var a = t.header.map(function (h) { return h.toLowerCase(); }).indexOf("approved");
      info.hasApprovedColumn = a !== -1;
      if (a !== -1) {
        info.approved = t.rows.filter(function (r) { return /^(yes|true|1|y|approved)$/i.test(String(r[a]).trim()); }).length;
      }
    }
    out.tabs[tab] = info;
  });
  return out;
}

function jsonOut_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
/* ==========================================================================
   SECTION 5 - INTAKE (behaviour-identical to Intake.gs v1.2.0)
   --------------------------------------------------------------------------
   Only the entry names changed from the standalone file: doGet is now
   intakeGet_ and doPost is now intakePost_ (the router in Section 2 calls
   them). Everything else is verbatim.
   ========================================================================== */
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
   Intake entries — called by the router doGet()/doPost() above.
   intakeGet_ answers ?action=health; intakePost_ accepts the five
   submission kinds. Behaviour is identical to Intake.gs v1.2.0.
   -------------------------------------------------------------------------- */
function intakeGet_(e) {
  var action = String((e && e.parameter && e.parameter.action) || "health");
  if (action !== "health") return intakeJson_({ ok: false, error: "unknown action" });
  return intakeJson_(intakeHealth_());
}

function intakePost_(e) {
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
/* ==========================================================================
   SECTION 6 - TRIGGERS (from LiveFeed.gs, verbatim)
   --------------------------------------------------------------------------
   onEdit clears the feed cache on every manual edit; installTriggers (run
   once) adds the installable onChange trigger so pasted/imported edits and
   inserted rows clear it too.
   ========================================================================== */
function clearFeedCache() {
  var keys = Object.keys(FEED_TABS).map(function (t) { return FEED_CACHE_PREFIX + t; });
  CacheService.getScriptCache().removeAll(keys);
}

/* Simple trigger: fires on a manual edit in the sheet. */
function onEdit(e) {
  try { clearFeedCache(); } catch (err) { /* a simple trigger must never throw */ }
}

/* Installable trigger: fires on pasted imports, inserted rows and other
   structural changes that onEdit does not see. Run this function once. */
function installTriggers() {
  var ss = SpreadsheetApp.getActive();
  var have = ScriptApp.getProjectTriggers().some(function (t) {
    return t.getHandlerFunction() === "clearFeedCache";
  });
  if (!have) {
    ScriptApp.newTrigger("clearFeedCache").forSpreadsheet(ss).onChange().create();
  }
  return have ? "already installed" : "installed";
}

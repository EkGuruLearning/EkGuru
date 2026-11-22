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
 *                                               columns and #help rows removed;
 *                                               reviews = approved rows of
 *                                               reviews_pending, public shape)
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
 *   · intake never writes to the public tabs (tutors, settings, support) —
 *     every submission lands pending/requested for the owner; reviews are
 *     published from reviews_pending only once the owner marks them approved
 *   · v2.1.0: a saved booking emails the BOOKED TUTOR (private address from
 *     the tutors tab) and the student, with the owner inbox as the fallback
 *     when the tutor has no address — see bookingMail_ in Section 5
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
var EK_UNIFIED_VERSION = "2.1.1";

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
  combinedHealth: true,

  /* v2.1.0 — BOOKING MAIL FROM THE SERVER.
     The browser cannot know a tutor's private address (the feed strips
     email / notification_email on purpose), so a booking mail sent from the
     page could only ever reach the relay owner's inbox — which is exactly the
     bug reported: "mail EkGuruLearning ke paas hi aata hai, tutor ke paas
     nahi". This script HAS the tutors tab, so it sends the notification
     itself, as the deploying Gmail account, the moment a booking row is saved:
       1. tutor notification   → tutors.notification_email, else tutors.email,
                                 else tutors.formkey (when it is an address)
       2. student receipt      → the student's own address
       3. FALLBACK             → when the tutor has no usable address, or
                                 Gmail refuses, the owner inbox gets the same
                                 notification with a [FORWARD TO <tutor>] subject
                                 so a booking is never silent.
     Every outcome is written back into the booking row (tutor_email,
     email_delivery) and returned to the page as {mail:{tutor,student}} so the
     site can skip its own duplicate send. Script Properties override these:
       BOOKING_MAIL_ENABLED = false   switch it off
       BOOKING_OWNER_INBOX  = …       where the fallback goes */
  bookingMail: true,
  bookingOwnerInbox: "EkGuruLearning@gmail.com",
  bookingSenderName: "EkGuru",
  bookingSiteUrl: "https://ekguru.shop/"
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
var FEED_VERSION = "1.0.1";
var FEED_CACHE_SECONDS = 30;
var FEED_CACHE_PREFIX = "ekguru-feed-v1:";

/* Tab name (case-insensitive) first, then the permanent gid from the old
   published links. A gid never changes, a name can be edited by accident. */
var FEED_TABS = {
  tutors:   { names: ["tutors"],                          gid: 1631273256 },
  /* v2.1.0 — ONE review tab. The old separate "reviews" tab is retired:
     every review a student submits lands in reviews_pending, the owner
     approves it THERE (status = approved, or approved = yes), and the feed
     publishes only those rows — mapped to the public column names the site
     has always read (tutor, name, date, stars, text, source, status). The
     old "reviews" tab is no longer read at all; delete it from the workbook
     when convenient. See reviewsFeed_() below. */
  reviews:  { names: ["reviews_pending"],                 gid: -1, pending: true },
  settings: { names: ["settings"],                        gid: 1658518385 },
  support:  { names: ["support", "payments", "support-payments"], gid: 1041390059 }
};

/* Values in reviews_pending.status (or an optional approved column) that
   publish a review. Anything else — pending, blank, rejected, hidden,
   spam — stays private. Case-insensitive. */
var REVIEW_APPROVED_VALUES = ["approved", "approve", "live", "published", "publish", "yes", "y", "true", "1", "ok"];

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
  if (FEED_TABS[tab] && FEED_TABS[tab].pending) return reviewsFeed_(tab);
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

/* ----------------------------------------------------------------------------
   v2.1.0 — PUBLISHED REVIEWS COME FROM reviews_pending, APPROVED ROWS ONLY
   ----------------------------------------------------------------------------
   reviews_pending columns (written by intake):
     timestamp | reference | status | tutor_id | reviewer_name | stars | text |
     lesson_date | contact_email | booking_id | notes
   Public shape the site reads (js/reviews.js, unchanged):
     tutor | name | date | stars | text | source | status
   A row is published when status (or an optional "approved" column) is one of
   REVIEW_APPROVED_VALUES. contact_email, booking_id, reference, timestamp and
   notes are never sent — the public shape simply has no column for them.
   -------------------------------------------------------------------------- */
function reviewsFeed_(tab) {
  var sheet = findSheet_(tab);
  var out = { header: ["tutor", "name", "date", "stars", "text", "source", "status"],
              rows: [], dropped: ["contact_email", "booking_id", "reference", "timestamp", "notes"] };
  if (!sheet) { out.missing = true; return out; }
  var range = sheet.getDataRange();
  var values = range.getDisplayValues();
  /* raw cells too: a date the owner typed, or the form's timestamp, is a real
     Date object here, and formatting THAT is the only locale-proof way to get
     YYYY-MM-DD (the display text is 16/11/2026 in this en_GB workbook). */
  var raw = range.getValues();
  if (values.length < 2) return out;
  var header = values[0].map(function (h) { return String(h).trim().toLowerCase(); });
  function col(name) { return header.indexOf(name); }
  var cStatus = col("status"), cApproved = col("approved"), cTutor = col("tutor_id"),
      cName = col("reviewer_name"), cStars = col("stars"), cText = col("text"),
      cDate = col("lesson_date"), cTs = col("timestamp");
  if (cTutor === -1) cTutor = col("tutor");
  if (cName === -1) cName = col("name");
  if (cDate === -1) cDate = col("date");
  for (var r = 1; r < values.length; r++) {
    var row = values[r];
    var first = String(row[0] == null ? "" : row[0]).trim();
    if (first.charAt(0) === "#") continue;
    if (row.every(function (c) { return String(c).trim() === ""; })) continue;
    var flag = "";
    if (cApproved !== -1) flag = String(row[cApproved] || "").trim().toLowerCase();
    if (!flag && cStatus !== -1) flag = String(row[cStatus] || "").trim().toLowerCase();
    if (REVIEW_APPROVED_VALUES.indexOf(flag) === -1) continue;   /* pending / rejected: private */
    /* lesson_date is optional on the form; fall back to the day the review
       arrived. v2.1.1 (17 Nov 2026): BUG — the fallback read the DISPLAY text
       "16/11/2026 11:24:13" as month/day and emitted "2026-16-11", which the
       site's validator rejected, so every approved review without a lesson
       date was silently dropped. Dates now come from the raw Date cell when
       there is one, else are parsed day-first (the workbook locale). */
    var date = isoDate_(cDate !== -1 ? raw[r][cDate] : null, cDate !== -1 ? row[cDate] : "");
    if (!date && cTs !== -1) date = isoDate_(raw[r][cTs], row[cTs]);
    out.rows.push([
      cTutor !== -1 ? String(row[cTutor] || "").trim().toLowerCase() : "",
      cName !== -1 ? String(row[cName] || "").trim() : "",
      date,
      cStars !== -1 ? String(row[cStars] || "").trim() : "",
      cText !== -1 ? String(row[cText] || "").trim() : "",
      "ekguru",
      "live"
    ]);
  }
  return out;
}

/* YYYY-MM-DD from a sheet cell: a Date object (formatted in the script's
   timezone), an ISO string, or a day-first d/m/yyyy display string. Month-first
   is only assumed when the first number cannot be a day (e.g. 11/16/2026). */
function isoDate_(rawCell, display) {
  if (rawCell instanceof Date && !isNaN(rawCell.getTime())) {
    return Utilities.formatDate(rawCell, Session.getScriptTimeZone() || "Asia/Kolkata", "yyyy-MM-dd");
  }
  var v = String(display == null ? (rawCell == null ? "" : rawCell) : display).trim();
  var m = /^(\d{4})-(\d{1,2})-(\d{1,2})/.exec(v);
  if (m) {
    var mo = Number(m[2]), d = Number(m[3]);
    if (mo > 12 && d <= 12) { var t = mo; mo = d; d = t; }
    if (mo < 1 || mo > 12 || d < 1 || d > 31) return "";
    return m[1] + "-" + ("0" + mo).slice(-2) + "-" + ("0" + d).slice(-2);
  }
  m = /^(\d{1,2})[\/.\-](\d{1,2})[\/.\-](\d{4})/.exec(v);
  if (m) {
    var a = Number(m[1]), b = Number(m[2]), day = a, mon = b;
    if (a <= 12 && b > 12) { day = b; mon = a; }
    if (mon < 1 || mon > 12 || day < 1 || day > 31) return "";
    return m[3] + "-" + ("0" + mon).slice(-2) + "-" + ("0" + day).slice(-2);
  }
  return "";
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
    if (tab === "reviews") info.source = "reviews_pending (approved rows only)";
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
             "topic", "message", "page", "ref", "replied_at", "reply_note"],
    fields: {
      name:    { type: "text",  max: 80,  required: true },
      email:   { type: "email", max: 120, required: true },
      subject: { type: "text",  max: 120 },
      topic:   { type: "text",  max: 60 },
      message: { type: "text",  max: 4000, required: true },
      page:    { type: "url",   max: 300 },
      ref:     { type: "text",  max: 20 }
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

    /* Owner action, not a visitor submission: the admin dashboard
       calls this AFTER a reply email has been sent, so the contacts
       tab shows status = "replied". No consent, no quota, no new row. */
    if (String(body.action || "") === "markReplied") {
      return intakeJson_(markContactReplied_(
        String(body.ref || ""), String(body.email || ""), String(body.note || "")));
    }

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
      /* Store the reference the way the bookings tab spells it, so the
         owner can match the two rows by eye. */
      clean.values.booking_id = intakeNormRef_(clean.values.booking_id);
    }

    var quota = intakeQuota_(kind);
    if (!quota.ok) return intakeJson_({ ok: false, error: quota.error });

    var ref = intakeRef_();
    var saved = intakeAppend_(kind, spec, ref, clean.values);
    /* A booking is confirmed by its own booking_ref (the same code the
       student sees and the email carries), not by a second server code. */
    var answer = { ok: true, reference: saved.reference, duplicate: saved.duplicate === true };
    /* v2.1.0 — notify the booked tutor from here (see bookingMail_). A
       duplicate submit never re-sends; a mail failure never fails the
       booking — the row is already saved and the outcome is written on it. */
    if (kind === "booking" && saved.duplicate !== true) {
      try { answer.mail = bookingMail_(saved.reference, clean.values); }
      catch (mailErr) { answer.mail = { tutor: "failed", student: "failed", note: "mail error" }; }
    }
    return intakeJson_(answer);
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
/* How a human types a booking reference (16 Nov 2026, real-life test):
   "ek-ab2cd3", " EK-AB2CD3 ", "EK AB2CD3", "EKAB2CD3", "EK–AB2CD3" (a
   phone's long dash). All of them mean EK-AB2CD3, and all of them used
   to be refused as "not found" because the gate compared raw strings.
   Both sides of the comparison now pass through this. */
function intakeNormRef_(v) {
  var s = String(v == null ? "" : v).toUpperCase();
  s = s.replace(/[\u2010-\u2015\u2212]/g, "-");   /* unicode dashes -> "-" */
  s = s.replace(/[\s_]+/g, "");                    /* no spaces anywhere */
  s = s.replace(/^EK-*/, "EK-");                   /* EKAB2CD3 / EK--AB2CD3 -> EK-AB2CD3 */
  return s;
}

function intakeReviewGate_(bookingId, tutorId) {
  var id = intakeNormRef_(bookingId);
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
      if (intakeNormRef_(refs[i][0]) === id) {
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

/* ============================================================================
   v2.1.0 — BOOKING MAIL (tutor notification + student receipt + owner fallback)
   ========================================================================== */
function bookingMailEnabled_() {
  var p = String(PropertiesService.getScriptProperties().getProperty("BOOKING_MAIL_ENABLED") || "").trim().toLowerCase();
  if (p === "false" || p === "0" || p === "no" || p === "off") return false;
  if (p === "true" || p === "1" || p === "yes" || p === "on") return true;
  return EK_.bookingMail !== false;
}
function bookingOwnerInbox_() {
  var p = String(PropertiesService.getScriptProperties().getProperty("BOOKING_OWNER_INBOX") || "").trim();
  return isEmailAddr_(p) ? p : EK_.bookingOwnerInbox;
}
function isEmailAddr_(s) {
  s = String(s == null ? "" : s).trim();
  return /^[^\s@<>"',;]+@[^\s@<>"',;]+\.[^\s@<>"',;]{2,}$/.test(s);
}
function firstEmailIn_(s) {
  var m = /[^\s@<>"',;]+@[^\s@<>"',;]+\.[A-Za-z]{2,}/.exec(String(s || ""));
  return m ? m[0] : "";
}

/* Look the tutor up in the tutors tab by id. Returns
   { found, name, email, source } — email is the first usable private
   address in precedence order notification_email → email → formkey. */
function tutorContact_(tutorId) {
  var out = { found: false, name: "", email: "", source: "" };
  var id = String(tutorId || "").trim().toLowerCase();
  if (!id) return out;
  var sheet = findSheet_("tutors");
  if (!sheet) return out;
  var range = sheet.getDataRange();
  var values = range.getDisplayValues();
  /* raw cells too: a date the owner typed, or the form's timestamp, is a real
     Date object here, and formatting THAT is the only locale-proof way to get
     YYYY-MM-DD (the display text is 16/11/2026 in this en_GB workbook). */
  var raw = range.getValues();
  if (values.length < 2) return out;
  var header = values[0].map(function (h) { return String(h).trim().toLowerCase(); });
  var cId = header.indexOf("id"), cName = header.indexOf("name");
  if (cId === -1) return out;
  var candidates = ["notification_email", "notificationemail", "email", "formkey"];
  for (var r = 1; r < values.length; r++) {
    if (String(values[r][cId] || "").trim().toLowerCase() !== id) continue;
    out.found = true;
    out.name = cName !== -1 ? String(values[r][cName] || "").trim() : "";
    for (var c = 0; c < candidates.length; c++) {
      var idx = header.indexOf(candidates[c]);
      if (idx === -1) continue;
      var v = firstEmailIn_(values[r][idx]);
      if (v) { out.email = v; out.source = candidates[c]; break; }
    }
    return out;
  }
  return out;
}

function esc_(s) {
  return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
  });
}

/* The two bodies. Plain text first (every client reads it), HTML second. */
function bookingTutorMessage_(ref, f, tutorName, forwardNote) {
  var rows = [
    ["Reference", ref],
    ["Student", f.student_name],
    ["Student email", f.student_email],
    ["WhatsApp", f.student_whatsapp || "—"],
    ["Preferred time (IST)", f.preferred_times_ist || "Not chosen"],
    ["Student timezone", f.student_timezone || "—"],
    ["Level", f.student_level || "—"],
    ["Goal", f.student_goal || "—"],
    ["Lesson", (f.lesson || "Trial lesson") + (f.price_usd ? " · $" + f.price_usd : "")],
    ["Booked from", f.source_page || EK_.bookingSiteUrl]
  ];
  var subject = "New lesson request " + ref + " — " + f.student_name + " wants a trial with " + (tutorName || "you");
  var text = (forwardNote ? forwardNote + "\n\n" : "") +
    "Namaste " + (tutorName || "Guru") + ",\n\n" +
    "A student has requested a trial lesson with you on EkGuru.\n\n" +
    rows.map(function (r) { return r[0] + ": " + r[1]; }).join("\n") +
    "\n\nWHAT TO DO NOW\n" +
    "1. Reply to this email (it goes straight to the student) or message them on WhatsApp within 24 hours.\n" +
    "2. Confirm the time in IST and in the student's timezone.\n" +
    "3. Tell EkGuru (" + bookingOwnerInbox_() + ") if you cannot take this lesson, so we can help the student.\n\n" +
    "— EkGuru · " + EK_.bookingSiteUrl;
  var html = '<div style="font-family:Inter,Arial,sans-serif;max-width:600px;margin:auto;color:#10131f">' +
    (forwardNote ? '<p style="background:#fff3cd;border:1px solid #f0c36d;padding:10px 14px;border-radius:8px"><b>' + esc_(forwardNote) + "</b></p>" : "") +
    '<h2 style="margin:0 0 6px">New lesson request <span style="color:#4f32d9">' + esc_(ref) + "</span></h2>" +
    "<p>Namaste " + esc_(tutorName || "Guru") + ", a student has requested a trial lesson with you on EkGuru.</p>" +
    '<table cellpadding="8" style="border-collapse:collapse;width:100%;font-size:15px">' +
    rows.map(function (r) {
      return '<tr><td style="border:1px solid #e4e4ef;background:#f8f7fd;width:38%"><b>' + esc_(r[0]) + "</b></td>" +
             '<td style="border:1px solid #e4e4ef">' + esc_(r[1]) + "</td></tr>";
    }).join("") + "</table>" +
    '<h3 style="margin:18px 0 6px">What to do now</h3><ol>' +
    "<li><b>Reply to this email</b> (it goes straight to the student) or WhatsApp them within 24 hours.</li>" +
    "<li>Confirm the time in IST <i>and</i> in the student's timezone.</li>" +
    "<li>Cannot take it? Tell EkGuru at " + esc_(bookingOwnerInbox_()) + " so we can help the student.</li></ol>" +
    '<p style="color:#5f6577;font-size:13px">EkGuru · <a href="' + esc_(EK_.bookingSiteUrl) + '">' + esc_(EK_.bookingSiteUrl) + "</a></p></div>";
  return { subject: subject, text: text, html: html };
}

function bookingStudentMessage_(ref, f, tutorName, tutorReached) {
  var next = tutorReached
    ? tutorName + " has been emailed and will reply to confirm the time."
    : "EkGuru will confirm " + tutorName + "'s availability with you shortly.";
  var subject = "Your EkGuru lesson request " + ref + " — " + tutorName;
  var text = "Namaste " + f.student_name + ",\n\n" +
    "Your trial lesson request with " + tutorName + " has been received.\n\n" +
    "Reference: " + ref + "\n" +
    "Preferred time (IST): " + (f.preferred_times_ist || "Not chosen") + "\n" +
    "Lesson: " + (f.lesson || "Trial lesson") + (f.price_usd ? " · $" + f.price_usd : "") + "\n\n" +
    next + " Keep this reference — quote it in any reply.\n\n" +
    "Questions? Reply to this email.\n— EkGuru · " + EK_.bookingSiteUrl;
  var html = '<div style="font-family:Inter,Arial,sans-serif;max-width:600px;margin:auto;color:#10131f">' +
    '<h2 style="margin:0 0 6px">Request received <span style="color:#4f32d9">' + esc_(ref) + "</span></h2>" +
    "<p>Namaste " + esc_(f.student_name) + ", your trial lesson request with <b>" + esc_(tutorName) + "</b> has been received.</p>" +
    '<table cellpadding="8" style="border-collapse:collapse;width:100%;font-size:15px">' +
    '<tr><td style="border:1px solid #e4e4ef;background:#f8f7fd;width:38%"><b>Reference</b></td><td style="border:1px solid #e4e4ef">' + esc_(ref) + "</td></tr>" +
    '<tr><td style="border:1px solid #e4e4ef;background:#f8f7fd"><b>Preferred time (IST)</b></td><td style="border:1px solid #e4e4ef">' + esc_(f.preferred_times_ist || "Not chosen") + "</td></tr>" +
    '<tr><td style="border:1px solid #e4e4ef;background:#f8f7fd"><b>Lesson</b></td><td style="border:1px solid #e4e4ef">' + esc_((f.lesson || "Trial lesson") + (f.price_usd ? " · $" + f.price_usd : "")) + "</td></tr>" +
    "</table><p>" + esc_(next) + " Keep this reference — quote it in any reply.</p>" +
    '<p style="color:#5f6577;font-size:13px">Questions? Reply to this email. · EkGuru · <a href="' + esc_(EK_.bookingSiteUrl) + '">' + esc_(EK_.bookingSiteUrl) + "</a></p></div>";
  return { subject: subject, text: text, html: html };
}

function gmailSend_(to, msg, replyTo, name) {
  var opts = { htmlBody: msg.html, name: name || EK_.bookingSenderName };
  if (replyTo && isEmailAddr_(replyTo)) opts.replyTo = replyTo;
  /* GmailApp first (sends as the deploying account, lands in Sent); MailApp
     is the fallback when the Gmail scope was not granted at deploy time. */
  try { GmailApp.sendEmail(to, msg.subject, msg.text, opts); return "gmail"; }
  catch (e1) {
    try { MailApp.sendEmail({ to: to, subject: msg.subject, body: msg.text, htmlBody: msg.html, replyTo: opts.replyTo || "", name: opts.name }); return "mailapp"; }
    catch (e2) { throw e2; }
  }
}

/* Writes tutor_email + email_delivery back onto the booking row. */
function bookingRowNote_(ref, tutorEmail, delivery) {
  try {
    var tab = intakeSpreadsheet_().getSheetByName(INTAKE_KINDS.booking.tab);
    if (!tab || tab.getLastRow() < 2) return;
    var header = tab.getRange(1, 1, 1, tab.getLastColumn()).getValues()[0].map(function (h) { return String(h).trim(); });
    var cRef = header.indexOf("booking_ref"), cTe = header.indexOf("tutor_email"), cDel = header.indexOf("email_delivery");
    if (cRef === -1) return;
    var refs = tab.getRange(2, cRef + 1, tab.getLastRow() - 1, 1).getValues();
    for (var i = refs.length - 1; i >= 0; i--) {
      if (String(refs[i][0] || "").trim() === ref) {
        if (cTe !== -1 && tutorEmail) tab.getRange(i + 2, cTe + 1).setValue(tutorEmail);
        if (cDel !== -1) tab.getRange(i + 2, cDel + 1).setValue(delivery);
        return;
      }
    }
  } catch (e) { /* the row note is best-effort; the mail already went */ }
}

/* The orchestrator. Never throws to the caller; returns
   { tutor: sent|owner_fallback|failed|disabled, student: sent|failed|disabled,
     tutorEmailSource, note } */
function bookingMail_(ref, f) {
  var result = { tutor: "disabled", student: "disabled", tutorEmailSource: "", note: "" };
  if (!bookingMailEnabled_()) { result.note = "BOOKING_MAIL_ENABLED=false"; return result; }
  var owner = bookingOwnerInbox_();
  var contact = tutorContact_(f.tutor_id);
  var tutorName = contact.name || String(f.tutor_id || "").replace(/-/g, " ").replace(/\b\w/g, function (c) { return c.toUpperCase(); });
  var studentEmail = isEmailAddr_(f.student_email) ? String(f.student_email).trim() : "";
  var tutorEmail = contact.email;
  var remaining = 0;
  try { remaining = MailApp.getRemainingDailyQuota(); } catch (e) { remaining = 100; }
  if (remaining < 2) {
    result.tutor = "failed"; result.student = "failed"; result.note = "daily Gmail quota exhausted";
    bookingRowNote_(ref, tutorEmail, "QUOTA_EXHAUSTED — forward by hand");
    return result;
  }

  /* 1. tutor */
  var tutorMsg = bookingTutorMessage_(ref, f, tutorName, "");
  var tutorReached = false;
  if (tutorEmail && tutorEmail.toLowerCase() !== owner.toLowerCase()) {
    try {
      gmailSend_(tutorEmail, tutorMsg, studentEmail, EK_.bookingSenderName);
      result.tutor = "sent"; result.tutorEmailSource = contact.source; tutorReached = true;
    } catch (e) {
      result.note = "tutor send failed: " + String(e && e.message || e).slice(0, 120);
    }
  } else {
    result.note = contact.found ? "tutor has no notification_email / email in the tutors tab" : "tutor id not in tutors tab";
  }
  /* 2. owner fallback — only when the tutor could not be reached */
  if (!tutorReached) {
    try {
      var fwd = "FORWARD TO " + tutorName + (tutorEmail ? " <" + tutorEmail + ">" : " (no address on file)") + " — " + result.note;
      var ownerMsg = bookingTutorMessage_(ref, f, tutorName, fwd);
      ownerMsg.subject = "[FORWARD TO " + tutorName + "] " + ownerMsg.subject;
      gmailSend_(owner, ownerMsg, studentEmail, EK_.bookingSenderName);
      result.tutor = "owner_fallback";
    } catch (e2) {
      result.tutor = "failed";
      result.note += " | owner fallback failed: " + String(e2 && e2.message || e2).slice(0, 120);
    }
  }
  /* 3. student receipt — replies go to EkGuru, never to the tutor's private address */
  if (studentEmail) {
    try {
      gmailSend_(studentEmail, bookingStudentMessage_(ref, f, tutorName, tutorReached), owner, EK_.bookingSenderName);
      result.student = "sent";
    } catch (e3) {
      result.student = "failed";
      result.note += " | student receipt failed: " + String(e3 && e3.message || e3).slice(0, 120);
    }
  } else {
    result.student = "failed"; result.note += " | no student email";
  }
  bookingRowNote_(ref, tutorEmail,
    "tutor:" + result.tutor + (result.tutorEmailSource ? "(" + result.tutorEmailSource + ")" : "") +
    " student:" + result.student + " via Apps Script " + Utilities.formatDate(new Date(), "Asia/Kolkata", "yyyy-MM-dd HH:mm") +
    (result.note ? " — " + result.note : ""));
  return result;
}

/* Run this ONCE from the editor after pasting v2.1.0: it grants the Gmail
   scope and sends a single test notification to the owner inbox. */
function bookingMailSelfTest_() {
  var r = bookingMail_("EK-TEST", {
    tutor_id: "self-test", student_name: "Test Student", student_email: bookingOwnerInbox_(),
    student_whatsapp: "", preferred_times_ist: "Sat 10:00 IST", lesson: "Trial lesson, 50 min",
    price_usd: "5", student_level: "Beginner", student_goal: "Self test of booking mail",
    student_timezone: "Asia/Kolkata", source_page: EK_.bookingSiteUrl
  });
  Logger.log(JSON.stringify(r));
  return r;
}

/* Mark one contacts row as replied. Matches by the visitor-facing
   reference (column "ref", e.g. C-PA0KN4) first, then by email
   (newest row wins). Header-driven, so it works on a tab that still
   has the old 10 columns: the two reply columns are appended to the
   header first. Never creates a row — a reply with no matching
   contact row is reported, not invented. */
function markContactReplied_(ref, email, note) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var ss = intakeSpreadsheet_();
    var tab = ss.getSheetByName(INTAKE_KINDS.contact.tab);
    if (!tab || tab.getLastRow() < 2) {
      return { ok: false, error: "no matching contact row" };
    }
    var spec = INTAKE_KINDS.contact;
    var header = tab.getRange(1, 1, 1, tab.getLastColumn()).getValues()[0];
    var at = function (name) { return header.indexOf(name); };
    /* Old tabs may not have the reply columns yet. */
    if (at("replied_at") < 0 || at("reply_note") < 0) {
      var next = tab.getLastColumn() + 1;
      if (at("replied_at") < 0) { tab.getRange(1, next, 1, 1).setValue("replied_at"); next++; }
      if (at("reply_note") < 0) { tab.getRange(1, next, 1, 1).setValue("reply_note"); next++; }
      header = tab.getRange(1, 1, 1, tab.getLastColumn()).getValues()[0];
    }
    var refAt = at("ref"), emailAt = at("email"), statusAt = at("status"),
        refRowAt = at("reference"), repliedAt = at("replied_at"), noteAt = at("reply_note");
    var wantRef = String(ref || "").trim().toUpperCase();
    var wantEmail = String(email || "").trim().toLowerCase();
    if (!wantRef && !wantEmail) return { ok: false, error: "ref or email needed" };
    var rows = tab.getRange(2, 1, tab.getLastRow() - 1, tab.getLastColumn()).getValues();
    var hit = -1;
    for (var r = rows.length - 1; r >= 0; r--) {
      if (wantRef && refAt >= 0 &&
          String(rows[r][refAt] || "").trim().toUpperCase() === wantRef) { hit = r; break; }
    }
    if (hit < 0 && wantEmail && emailAt >= 0) {
      for (var e = rows.length - 1; e >= 0; e--) {
        if (String(rows[e][emailAt] || "").trim().toLowerCase() === wantEmail) { hit = e; break; }
      }
    }
    if (hit < 0) return { ok: false, error: "no matching contact row" };
    var rowNumber = hit + 2;
    tab.getRange(rowNumber, statusAt + 1, 1, 1).setValue("replied");
    tab.getRange(rowNumber, repliedAt + 1, 1, 1).setValue(
      Utilities.formatDate(new Date(), "Asia/Kolkata", "yyyy-MM-dd HH:mm") + " IST");
    tab.getRange(rowNumber, noteAt + 1, 1, 1).setValue(String(note || "").slice(0, 500));
    return { ok: true, reference: refRowAt >= 0 ? String(rows[hit][refRowAt] || "") : "" };
  } catch (err) {
    return { ok: false, error: "could not mark replied" };
  } finally {
    lock.releaseLock();
  }
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

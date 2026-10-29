/**
 * ============================================================================
 * EkGuru: LIVE FEED (read-only)
 * ============================================================================
 * Serves the public tabs of the "EkGuru DB" workbook as CSV, straight from the
 * spreadsheet, so a change made in the sheet shows on the site within seconds.
 *
 * WHY THIS EXISTS
 *   Google's "Publish to web" CSV is cached by Google for about five minutes
 *   and the browser cannot shorten that. This script reads the live cells, so
 *   the only delay left is the 30 second cache below, and that cache is
 *   cleared the moment somebody edits the sheet (see onEdit and onChange).
 *
 * HOW THE SITE USES IT
 *   js/sheet.js, js/reviews.js and js/settings.js ask this feed first and fall
 *   back to the published CSV if the feed is slow, down or not deployed. The
 *   feed returns the same CSV the published link does, so no parser changed.
 *
 *     GET <exec url>?tab=tutors    the tutors tab
 *     GET <exec url>?tab=reviews   the reviews tab
 *     GET <exec url>?tab=settings  the settings tab
 *     GET <exec url>?tab=support   the support tab
 *     GET <exec url>?tab=health    row counts only, no cell contents
 *
 * WHAT IS NEVER SENT
 *   Columns that hold private contact details (email, notification_email,
 *   formKey, whatsapp and anything that looks like a phone, password, token or
 *   bank detail) are removed before the CSV is built. Help rows (first cell
 *   starts with #) are removed too. This is enforced here, in the script, so a
 *   mistake in the sheet cannot publish an address.
 *
 * SETUP (once, about five minutes). Full steps: apps-script/LIVE-FEED-SETUP.md
 *   1. Open the EkGuru DB sheet, Extensions, Apps Script.
 *   2. Paste this file as LiveFeed.gs. Keep it in the sheet's OWN script
 *      project. It uses getActive(), so it reads this workbook and nothing else.
 *   3. Deploy, New deployment, Web app. Execute as: Me. Who has access: Anyone.
 *   4. Copy the /exec URL into js/site-config.js, feed.url.
 *   5. Run installTriggers() once so that pasted or imported edits also clear
 *      the cache.
 *
 * NEVER paste the payments workbook id or any Razorpay key into this file. The
 * payments backend (Code.gs) is a separate project on purpose.
 * ============================================================================
 */

"use strict";

var FEED_VERSION = "1.0.0";
var FEED_CACHE_SECONDS = 30;
var FEED_CACHE_PREFIX = "ekguru-feed-v1:";

/* Tab name (case-insensitive) first, then the permanent gid from the old
   published links. A gid never changes, a name can be edited by accident. */
var FEED_TABS = {
  tutors:   { names: ["tutors"],                          gid: 1631273256 },
  reviews:  { names: ["reviews"],                         gid: 298809212 },
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
   Entry point
   -------------------------------------------------------------------------- */
function doGet(e) {
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

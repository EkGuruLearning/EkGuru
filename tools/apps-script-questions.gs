/**
 * ============================================================
 *  EKGURU — QUESTIONS API  (shared flags + likes)
 * ============================================================
 *  Paste this into its OWN Apps Script project (extensions →
 *  Apps Script from a new Google Sheet works too — see
 *  docs/QUESTIONS-API-SETUP.md) and deploy as a Web App:
 *
 *      Execute as:      Me
 *      Who has access:  Anyone
 *
 *  Then paste the /exec URL into js/site-config.js:
 *
 *      api: { questions: "https://script.google.com/macros/s/…/exec" }
 *
 *  WHY A SEPARATE PROJECT
 *  ----------------------
 *  tools/apps-script-mailer.gs already owns doPost() for mail. Two doPost()
 *  functions in one project is a redeclaration error, and merging them would
 *  mean a mail bug could break voting. This script is deliberately small and
 *  has no mail rights at all: the worst it can do is write a row.
 *
 *  THE CONTRACT WITH js/question-api.js
 *  ------------------------------------
 *  GET  ?bank=<slug>&action=top
 *       → {"ok":true,"bank":"bengali","counts":{"bq-01":{"flags":3,"likes":12}}}
 *
 *  POST  (Content-Type: text/plain — an Apps Script Web App cannot
 *         answer a CORS preflight, so the client sends a JSON *string*)
 *       {"action":"flag","bank":"bengali","id":"bq-01",
 *        "reason":"wrong answer","client":"c8f2a1…"}
 *       → {"ok":true,"bank":"bengali","id":"bq-01","flags":4,"likes":12}
 *
 *  WHAT IS STORED
 *  --------------
 *  One row per vote: timestamp, bank, question id, action, reason, client-hash.
 *  The client id is a random value the browser makes; only a SALTED HASH of it
 *  is written, so one device can be counted once per question without the
 *  sheet holding anything that identifies a person. No names, no emails, no
 *  IPs, and the reason is checked against a fixed menu.
 *
 *  LIMITS (honest ones)
 *  --------------------
 *  · Free Apps Script quotas: ~20k reads/day with this shape of access, and
 *    writes are per-cell, so this is built for hundreds of voters, not
 *    millions. It is a real API for a small site, not a fantasy of scale.
 *  · A "flag" is a signal for a human to review, never an automatic delete.
 *  · Deleting the sheet deletes the votes; nothing else depends on it.
 * ============================================================
 */

var SHEET_PROP = "QUESTIONS_SHEET_ID";     /* Script Property, set once */
var TAB = "votes";
var SALT_PROP = "QUESTIONS_SALT";
var MAX_PER_DAY = 60;                      /* per client, all questions */

var ACTIONS = { flag: 1, unflag: 1, like: 1, unlike: 1 };
var REASONS = {
  "wrong answer": 1, "typo or spelling": 1, "confusing wording": 1,
  "duplicate question": 1, "not in the lesson": 1
};

function sheet() {
  var id = PropertiesService.getScriptProperties().getProperty(SHEET_PROP);
  if (!id) throw new Error("Set the Script Property " + SHEET_PROP + " to a Google Sheet id");
  var ss = SpreadsheetApp.openById(id);
  var tab = ss.getSheetByName(TAB);
  if (!tab) {
    tab = ss.insertSheet(TAB);
    tab.appendRow(["at", "bank", "question", "action", "reason", "clientHash", "day"]);
    tab.setFrozenRows(1);
  }
  return tab;
}

function salt() {
  var props = PropertiesService.getScriptProperties();
  var s = props.getProperty(SALT_PROP);
  if (!s) {
    s = Utilities.getUuid();
    props.setProperty(SALT_PROP, s);
  }
  return s;
}

function hashClient(client) {
  if (!client || typeof client !== "string" || client.length > 64) return "";
  var raw = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, salt() + "|" + client);
  return raw.map(function (b) { return ((b + 256) % 256).toString(16).slice(-2); }).join("").slice(0, 24);
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function rowsOf(tab) {
  var values = tab.getDataRange().getValues();
  values.shift();                        /* header */
  return values;
}

function countsFor(bank) {
  var out = {};
  var rows = rowsOf(sheet());
  var latest = {};                       /* clientHash|id → action */
  rows.forEach(function (r) {
    var b = String(r[1] || "");
    if (b !== bank) return;
    latest[String(r[5] || "") + "|" + String(r[2])] = String(r[3] || "");
  });
  Object.keys(latest).forEach(function (k) {
    var id = k.split("|").slice(1).join("|");
    var a = latest[k];
    if (a !== "flag" && a !== "like") return;
    out[id] = out[id] || { flags: 0, likes: 0 };
    if (a === "flag") out[id].flags++;
    else out[id].likes++;
  });
  return out;
}

function doGet(e) {
  try {
    var p = (e && e.parameter) || {};
    var bank = String(p.bank || "").slice(0, 40).replace(/[^a-zA-Z0-9_-]/g, "");
    if (!bank) return json({ ok: false, error: "bank required" });
    return json({ ok: true, bank: bank, counts: countsFor(bank), at: new Date().toISOString() });
  } catch (err) {
    return json({ ok: false, error: String(err && err.message || err) });
  }
}

function doPost(e) {
  try {
    var body = JSON.parse((e && e.postData && e.postData.contents) || "{}");
    var action = String(body.action || "");
    var bank = String(body.bank || "").slice(0, 40).replace(/[^a-zA-Z0-9_-]/g, "");
    var id = String(body.id || "").slice(0, 80).replace(/[<>]/g, "");
    var client = hashClient(body.client);
    if (!ACTIONS[action]) return json({ ok: false, error: "unknown action" });
    if (!bank || !id) return json({ ok: false, error: "bank and id required" });
    if (!client) return json({ ok: false, error: "client required" });

    var tab = sheet();
    var today = Utilities.formatDate(new Date(), Session.getScriptTimeZone() || "GMT+05:30", "yyyy-MM-dd");
    var rows = rowsOf(tab);
    var mineToday = 0;
    rows.forEach(function (r) {
      if (String(r[5] || "") === client && String(r[6] || "") === today) mineToday++;
    });
    if (mineToday >= MAX_PER_DAY) return json({ ok: false, error: "daily limit reached" });

    var reason = String(body.reason || "");
    if (!REASONS[reason]) reason = "";
    tab.appendRow([new Date(), bank, id, action, reason, client, today]);

    var counts = countsFor(bank);
    var c = counts[id] || { flags: 0, likes: 0 };
    return json({ ok: true, bank: bank, id: id, flags: c.flags, likes: c.likes });
  } catch (err) {
    return json({ ok: false, error: String(err && err.message || err) });
  }
}

/* Run once from the editor if you want the tab created before the first vote. */
function setup() {
  var tab = sheet();
  Logger.log("Questions API ready — sheet: " + tab.getParent().getId());
}

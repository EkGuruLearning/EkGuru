/**
 * ============================================================
 *  EKGURU — APPS SCRIPT MAIL RELAY  (v98 · 11 Sep 2026)
 * ============================================================
 *  This is the WHOLE script. Paste it into Code.gs of the Apps
 *  Script project and deploy as a Web App (see
 *  tools/APPS-SCRIPT-SETUP.md for the click-by-click).
 *
 *  It is the front line of the mail chain: it sends from
 *  EkGuruLearning@gmail.com (your own Gmail) with no per-recipient
 *  activation link, about 100 recipients a day, and it is the only
 *  relay whose email body WE write — the HTML table below is ours,
 *  not a relay's.
 *
 *  THE CONTRACT WITH js/mailer.js
 *  ------------------------------
 *  The site POSTs to /exec with Content-Type: text/plain
 *  (NOT application/json — an Apps Script Web App cannot answer the
 *  CORS preflight that a JSON content-type triggers). The body is a
 *  JSON string:
 *
 *      {
 *        "token":     "the word shared with js/site-config.js",
 *        "to":        "recipient@example.com",
 *        "subject":   "Booking request EK123 — Aarav",
 *        "replyTo":   "student@example.com",
 *        "cc":        "" (usually empty — the site sends separately),
 *        "fromName":  "EkGuru",
 *        "rows":      { "Reference": "EK123", "Student name": "Aarav", ... }
 *      }
 *
 *  A successful send answers  {"success":"true", "message":"sent"}.
 *  Anything else is a failure the site treats as a normal fallback.
 *
 *  ⚠️  HONEST LIMITS (read them, they matter)
 *  · A free Gmail account allows roughly 100 recipients/day
 *    (some accounts up to 500). DAILY_LIMIT below defaults to 90
 *    and is enforced here so we never burn the account silently.
 *  · The deployment URL is PUBLIC (it sits in the page source), so
 *    this script REQUIRES a token by default. The token is NOT a
 *    secret — anyone who reads the page source can copy it — but it
 *    stops a drive-by who found the bare URL. The daily cap is the
 *    real backstop. Never describe the token as encryption.
 *  · It sends AS the script owner. Reply-To is set separately, so
 *    a visitor's address never appears in the From field (the
 *    "visitor email in FROM" bug this project fixed).
 * ============================================================
 */

var SCRIPT_NAME = "EkGuru Mail Relay";

/** A shared word you invent, stored as a Script Property named
 *  "TOKEN". Paste the SAME word into js/site-config.js under
 *  mail.appsScript.token. Empty here means "no token required" —
 *  allowed, but then anyone with the URL can send as you. */
function token() {
  return String(props().getProperty("TOKEN") || "").trim();
}

/** Addresses this relay is ALWAYS allowed to write to (your own
 *  inboxes and each tutor's personal address, once they provide one).
 *  When ALLOW_STRANGERS is false, ONLY these addresses are accepted. */
function allowedRecipients() {
  return [
    "EkGuruLearning@gmail.com"
    // , "tutor@example.com"   ← add each tutor's real address here
  ];
}

/** Students (strangers) must receive their own booking receipt, so
 *  stranger addresses have to be accepted. Set this to false to lock
 *  the relay down to allowedRecipients() only — the site will then
 *  route student receipts through the other providers. */
var ALLOW_STRANGERS = true;

/** Daily ceiling. Keep it below Gmail's own cap so we fail gracefully
 *  (with a quota message the site recognises) instead of hitting a
 *  hard Gmail block. */
var DAILY_LIMIT = 90;

/** ------------------------------------------------------------------
 *  WEB APP ENTRY POINTS
 *  ------------------------------------------------------------------ */
function doGet() {
  // Health check. Open the /exec URL in a browser and you should see
  // {"success":"true","status":"ok",...}. If you see a Google error
  // page, the deployment is not set to "Anyone".
  return json({
    success: "true",
    status: "ok",
    script: SCRIPT_NAME,
    strangers: ALLOW_STRANGERS,
    limit: DAILY_LIMIT
  });
}

function doPost(e) {
  // One request at a time: Gmail is fine with bursts, but the daily
  // counter below must never double-count two racing requests.
  var lock = LockService.getScriptLock();
  try { lock.waitLock(30000); } catch (err) {
    return json({ success: "false", message: "Busy, try again." });
  }
  try {
    return handle(e);
  } catch (err) {
    return json({
      success: "false",
      message: String((err && err.message) || err)
    });
  } finally {
    try { lock.releaseLock(); } catch (e) {}
  }
}

/** ------------------------------------------------------------------
 *  THE WORK
 *  ------------------------------------------------------------------ */
function handle(e) {
  var raw = e && e.postData && e.postData.contents;
  if (!raw) return json({ success: "false", message: "Empty request." });

  var body = {};
  try { body = JSON.parse(raw); } catch (err) {
    // Some clients still send urlencoded; tolerate it.
    body = parseQuery(raw);
  }
  if (!body || typeof body !== "object") {
    return json({ success: "false", message: "Malformed payload." });
  }

  // 1. Token — fail closed when one is configured.
  var expected = token();
  if (expected && String(body.token || "") !== expected) {
    return json({ success: "false", message: "bad token" });
  }

  // 2. Recipient — must be a real address we are willing to write to.
  var to = String(body.to || "").trim();
  if (!isEmail(to)) {
    return json({ success: "false", message: "Missing or invalid recipient." });
  }
  var known = allowedRecipients().some(function (a) {
    return a.toLowerCase() === to.toLowerCase();
  });
  if (!known && !ALLOW_STRANGERS) {
    return json({ success: "false", message: "Recipient not allowed." });
  }

  // 3. Daily cap — refuse BEFORE sending, with a message the site's
  //    quota fallback recognises ("limit exceeded").
  var day = Utilities.formatDate(new Date(), "GMT", "yyyy-MM-dd");
  var used = parseInt(props().getProperty("USED_" + day) || "0", 10);
  if (used >= DAILY_LIMIT) {
    return json({ success: "false", message: "Daily limit exceeded." });
  }

  // 4. Build the message — our layout, our wording.
  var subject = String(body.subject || "EkGuru").slice(0, 150);
  var replyTo = firstEmail(body.replyTo);
  var cc = firstEmail(body.cc);
  var fromName = String(body.fromName || "EkGuru").slice(0, 60);
  var rows = body.rows && typeof body.rows === "object" ? body.rows : {};
  var html = renderHtml(rows, fromName);
  var text = renderText(rows, fromName);

  var opts = { htmlBody: html, name: fromName };
  if (replyTo) opts.replyTo = replyTo;
  if (cc) opts.cc = cc;

  GmailApp.sendEmail(to, subject, text, opts);

  props().setProperty("USED_" + day, String(used + 1));
  return json({ success: "true", message: "sent" });
}

/** ------------------------------------------------------------------
 *  RENDERING — the table the recipient actually sees
 *  ------------------------------------------------------------------ */
function renderHtml(rows, fromName) {
  var inner = [];
  Object.keys(rows).forEach(function (label) {
    if (label === "_subject" || label === "_template" || label === "_captcha") return;
    var value = String(rows[label] == null ? "" : rows[label]);
    if (!label || !value) return;
    inner.push(
      "<tr>" +
      "<td style='padding:8px 12px;border:1px solid #e5e7eb;background:#f8fafc;" +
      "color:#64748b;font-size:12px;white-space:nowrap;vertical-align:top;'>" +
      esc(label) + "</td>" +
      "<td style='padding:8px 12px;border:1px solid #e5e7eb;color:#0f172a;" +
      "font-size:13px;white-space:pre-wrap;'>" + esc(value) + "</td>" +
      "</tr>"
    );
  });
  return (
    "<div style='font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;" +
    "color:#0f172a;'>" +
    "<table style='border-collapse:collapse;width:100%;max-width:640px;'>" +
    inner.join("") +
    "</table>" +
    "<p style='color:#94a3b8;font-size:11px;margin-top:14px;'>" +
    "Sent by " + esc(fromName || "EkGuru") + " — the EkGuru mail relay." +
    "</p></div>"
  );
}

function renderText(rows, fromName) {
  var out = [];
  Object.keys(rows).forEach(function (label) {
    if (label === "_subject" || label === "_template" || label === "_captcha") return;
    var value = String(rows[label] == null ? "" : rows[label]);
    if (!label || !value) return;
    out.push(label + ": " + value);
  });
  out.push("");
  out.push("Sent by " + (fromName || "EkGuru") + " — the EkGuru mail relay.");
  return out.join("\n");
}

/** ------------------------------------------------------------------
 *  HELPERS
 *  ------------------------------------------------------------------ */
function props() {
  return PropertiesService.getScriptProperties();
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function isEmail(s) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(s || ""));
}

function firstEmail(s) {
  var v = String(s || "").split(/[\s,;]+/)[0].trim();
  return isEmail(v) ? v : "";
}

function esc(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function parseQuery(qs) {
  var out = {};
  String(qs || "").split("&").forEach(function (pair) {
    var kv = pair.split("=");
    if (kv.length === 2) {
      out[decodeURIComponent(kv[0])] = decodeURIComponent(kv[1].replace(/\+/g, " "));
    }
  });
  return out;
}

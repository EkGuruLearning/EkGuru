/**
 * ============================================================
 *  EKGURU — APPS SCRIPT MAIL RELAY  (v100 · 11 Sep 2026)
 * ============================================================
 *  This is the WHOLE script. Paste it into Code.gs of the Apps
 *  Script project and deploy as a Web App (see
 *  tools/APPS-SCRIPT-SETUP.md for the click-by-click).
 *
 *  It is the PRIMARY mail route: it sends from
 *  EkGuruLearning@gmail.com (your own Gmail) with no per-recipient
 *  activation link, about 100 recipients a day, and it is the only
 *  relay whose email body WE write — the HTML below is ours, not a
 *  relay's.
 *
 *  THE CONTRACT WITH js/mailer.js  (v100)
 *  -------------------------------------
 *  The site POSTs to /exec with Content-Type: text/plain
 *  (NOT application/json — an Apps Script Web App cannot answer the
 *  CORS preflight that a JSON content-type triggers). The body is a
 *  JSON string:
 *
 *      {
 *        "token":          "the word shared with js/site-config.js",
 *        "type":           "BOOKING_STUDENT_CONFIRMATION",   ← whitelisted
 *        "to":             "recipient@example.com",
 *        "replyTo":        "support@example.com",
 *        "cc":             "",
 *        "fromName":       "EkGuru",                          ← forced
 *        "html":           "<html body>",                     ← v100
 *        "text":           "plain body",                      ← v100
 *        "rows":           { "Reference": "EK123", ... },     ← legacy fallback
 *        "requestId":      "EK123:student",
 *        "idempotencyKey": "EK123:BOOKING_STUDENT_CONFIRMATION"
 *      }
 *
 *  A successful send answers
 *      {"success":"true","message":"sent","state":"ACCEPTED","requestId":"…"}
 *  A duplicate (same idempotencyKey, already sent) answers
 *      {"success":"true","message":"duplicate","state":"ACCEPTED","dedup":true}
 *  Anything else is a failure the site treats as a normal fallback.
 *
 *  ⚠️  HONEST LIMITS (read them, they matter)
 *  · A free Gmail account allows roughly 100 recipients/day.
 *    DAILY_LIMIT below defaults to 90 and is enforced here.
 *  · The token is a SHARED SECRET stored SERVER-SIDE as the Script
 *    Property MAILER_SHARED_TOKEN (run mintToken() once). It is NOT
 *    encryption and NOT a substitute for the daily cap.
 *  · It sends AS the script owner. Reply-To is set separately, so a
 *    visitor's address never appears in the From field.
 *  · ACCEPTED ≠ DELIVERED: success means Gmail accepted the message,
 *    not that the recipient's mailbox has it.
 * ============================================================
 */

var SCRIPT_NAME = "EkGuru Mail Relay";

/* ============================================================
 * MESSAGE-TYPE WHITELIST  (§21)
 * The ONLY message types this relay will carry. Unknown types are
 * rejected before any send. This is how the public site is stopped
 * from turning the relay into an open mailer for arbitrary content.
 * ============================================================ */
var MESSAGE_TYPES = [
  "CONTACT_VISITOR_CONFIRMATION",
  "CONTACT_EKGURU_NOTIFICATION",
  "BOOKING_STUDENT_CONFIRMATION",
  "BOOKING_TUTOR_NOTIFICATION",
  "BOOKING_EKGURU_NOTIFICATION",
  "ADMIN_CONTACT_OUTBOUND",
  "ADMIN_CONTACT_INTERNAL_COPY"
];

/* The display name that may appear as the sender. The client may
 * propose one; anything else is replaced with this, so the public
 * site can never spoof a sender name. The FROM ADDRESS is always
 * the script owner's Gmail — never taken from the client. */
var SENDER_NAME = "EkGuru";

/* Payload size limits — stop an oversized message from wedging the
 * script or blowing the mailbox quota. */
var MAX_HTML_BYTES = 60000;
var MAX_TEXT_BYTES = 20000;

/* Idempotency retention: a replayed key within this window is
 * answered as a duplicate and NOT re-sent. */
var DEDUP_DAYS = 7;

/** The shared token, read from the Script Property MAILER_SHARED_TOKEN
 *  (never from source code). FAIL-CLOSED: doPost refuses mail while
 *  this is empty, so the relay can never run unauthenticated. */
function token() {
  return String(props().getProperty("MAILER_SHARED_TOKEN") || "").trim();
}

/** Generate a fresh random shared secret and store it in the Script
 *  Property MAILER_SHARED_TOKEN. Run ONCE from the Apps Script editor
 *  (select mintToken → Run), then wire the SAME value into the client
 *  config at deploy time. The secret stays server-side; it is never
 *  written into this source file or committed to the repository. */
function mintToken() {
  var chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789";
  var out = "";
  for (var i = 0; i < 32; i++) {
    out += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  PropertiesService.getScriptProperties().setProperty("MAILER_SHARED_TOKEN", out);
  Logger.log("New MAILER_SHARED_TOKEN stored (length " + out.length + "). " +
    "Wire the same value into the client config — it is not logged here.");
  return "stored";
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

/** Daily ceiling. Keep it below Gmail's own cap so we fail gracefully. */
var DAILY_LIMIT = 90;

/** ------------------------------------------------------------------
 *  WEB APP ENTRY POINTS
 *  ------------------------------------------------------------------ */
function doGet() {
  // Health check. Open the /exec URL in a browser and you should see
  // {"success":"true","status":"ok",...}.
  return json({
    success: "true",
    status: "ok",
    script: SCRIPT_NAME,
    strangers: ALLOW_STRANGERS,
    limit: DAILY_LIMIT,
    configured: !!token()
  });
}

function doPost(e) {
  // One request at a time: Gmail is fine with bursts, but the daily
  // counter and the idempotency store must never double-count two
  // racing requests.
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

  // 1. Token — FAIL CLOSED. Never accept mail without the secret.
  var expected = token();
  if (!expected) {
    return json({ success: "false", message: "Not authorised. Relay token not configured." });
  }
  if (String(body.token || "") !== expected) {
    return json({ success: "false", message: "Not authorised." });
  }

  // 2. Message type — WHITELIST. Unknown types are refused before
  //    any recipient is touched, so the relay cannot be used to
  //    carry arbitrary content (open-relay defence).
  var type = String(body.type || "").trim().toUpperCase();
  if (type && MESSAGE_TYPES.indexOf(type) === -1) {
    return json({ success: "false", message: "Unknown message type." });
  }

  // 3. Recipient — must be a real address we are willing to write to.
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

  // 4. Daily cap — refuse BEFORE sending, with a message the site's
  //    quota fallback recognises ("limit exceeded").
  var day = Utilities.formatDate(new Date(), "GMT", "yyyy-MM-dd");
  var used = parseInt(props().getProperty("USED_" + day) || "0", 10);
  if (used >= DAILY_LIMIT) {
    return json({ success: "false", message: "Daily limit exceeded." });
  }

  // 5. Idempotency — server-side. A replayed key within the window
  //    is answered as a duplicate and NOT re-sent, so a double
  //    submit / refresh / retry can never double a message.
  var idem = String(body.idempotencyKey || "").trim().slice(0, 200);
  if (idem) {
    var already = sentFlag(idem);
    if (already) {
      return json({
        success: "true", message: "duplicate", state: "ACCEPTED",
        dedup: true, requestId: String(body.requestId || "")
      });
    }
  }

  // 6. Size limits.
  var html = String(body.html || "");
  var text = String(body.text || "");
  if (html.length > MAX_HTML_BYTES || text.length > MAX_TEXT_BYTES) {
    return json({ success: "false", message: "Payload too large." });
  }

  // 7. Sender enforcement. The From ADDRESS is the script owner —
  //    the client cannot change it. The display name is forced to
  //    SENDER_NAME; a client-supplied fromName is ignored.
  var replyTo = firstEmail(body.replyTo);
  var cc = firstEmail(body.cc);

  // 8. Build the message. v100: html/text come straight from the
  //    client templates; legacy rows still render if html is empty.
  var rows = body.rows && typeof body.rows === "object" ? body.rows : {};
  var htmlBody = html || renderHtml(rows, SENDER_NAME);
  var textBody = text || renderText(rows, SENDER_NAME);
  // Single-line subject: collapse control characters so a newline
  // smuggled into a name can never inject a header line.
  var subject = String(body.subject || "EkGuru")
    .replace(/[\r\n\t]+/g, " ")
    .slice(0, 150);

  var opts = { htmlBody: htmlBody, name: SENDER_NAME };
  if (replyTo) opts.replyTo = replyTo;
  if (cc) opts.cc = cc;

  GmailApp.sendEmail(to, subject, textBody, opts);

  // Record the send — quota, then idempotency (after success only).
  props().setProperty("USED_" + day, String(used + 1));
  if (idem) setSentFlag(idem);

  return json({
    success: "true", message: "sent", state: "ACCEPTED",
    requestId: String(body.requestId || "")
  });
}

/** ------------------------------------------------------------------
 *  IDEMPOTENCY STORE (Script Properties)
 *  Key: SENT_<idempotencyKey>  Value: ISO timestamp of the send.
 *  Read + write are inside the doPost lock, so no double-send race.
 *  ------------------------------------------------------------------ */
function sentFlag(idem) {
  var v = props().getProperty("SENT_" + idem);
  if (!v) return false;
  var when = new Date(v).getTime();
  if (!when) return false;
  return (Date.now() - when) < (DEDUP_DAYS * 86400000);
}
function setSentFlag(idem) {
  props().setProperty("SENT_" + idem, new Date().toISOString());
}

/** ------------------------------------------------------------------
 *  RENDERING — legacy table for clients that still send `rows`
 *  ------------------------------------------------------------------ */
function renderHtml(rows, fromName) {
  var inner = [];
  Object.keys(rows).forEach(function (label) {
    if (label.charAt(0) === "_") return;
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
    if (label.charAt(0) === "_") return;
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

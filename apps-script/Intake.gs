/**
 * ============================================================================
 * EkGuru: INTAKE (applications, reviews, sign-ups)  ·  write-only, pending-only
 * ============================================================================
 * Lets a visitor send a tutor application, a student review or a learner
 * sign-up straight from the site, without a server of ours. Every submission
 * lands as a PENDING row in this workbook. Nothing here ever reaches the
 * public site by itself:
 *
 *   applications   ->  you check the person, then set approved = yes in the
 *                      tutors tab (or add the row there) to publish them
 *   reviews_pending->  you check the review, then copy it into the reviews tab
 *                      with status = live
 *   signups        ->  private. Used only to send the learner a reply and to
 *                      count interest. Never published, never sent back out.
 *
 * SEPARATE PROJECT ON PURPOSE. Paste this into its OWN Apps Script project
 * (Extensions → Apps Script from a new sheet is fine). It does not share a
 * doPost with the mailer or the questions API, because two doPost functions in
 * one project will not compile. Deploy:
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
 *         {"kind":"application"|"review"|"signup",
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
 *   · the kind is one of three known kinds
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

var INTAKE_VERSION = "1.0.0";
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
             "text", "lesson_date", "contact_email", "notes"],
    fields: {
      tutor_id:      { type: "slug",  max: 60,  required: true },
      reviewer_name: { type: "text",  max: 60,  required: true },
      stars:         { type: "int",   min: 1, max: 5, required: true },
      text:          { type: "text",  max: 800, required: true },
      lesson_date:   { type: "date" },
      contact_email: { type: "email", max: 120 }
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

    var quota = intakeQuota_(kind);
    if (!quota.ok) return intakeJson_({ ok: false, error: quota.error });

    var ref = intakeRef_();
    intakeAppend_(kind, spec, ref, clean.values);
    return intakeJson_({ ok: true, reference: "EG-" + ref });
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
function intakeAppend_(kind, spec, ref, values) {
  var ss = SpreadsheetApp.getActive();
  var tab = ss.getSheetByName(spec.tab);
  if (!tab) {
    tab = ss.insertSheet(spec.tab);
    tab.appendRow(spec.header);
    tab.setFrozenRows(1);
  }
  var when = new Date();
  var row = spec.header.map(function (h) {
    if (h === "timestamp") return when;
    if (h === "reference") return "EG-" + ref;
    if (h === "status") return "pending";
    if (h === "approved") return "";
    if (h === "notes") return values.notes || "";
    return values[h] !== undefined ? values[h] : "";
  });
  tab.appendRow(row);
}

function intakeHealth_() {
  var ss = SpreadsheetApp.getActive();
  var tabs = {};
  Object.keys(INTAKE_KINDS).forEach(function (k) {
    var name = INTAKE_KINDS[k].tab;
    var t = ss.getSheetByName(name);
    tabs[name] = t ? Math.max(0, t.getLastRow() - 1) : 0;
  });
  return { ok: true, version: INTAKE_VERSION, at: new Date().toISOString(), pendingRows: tabs };
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

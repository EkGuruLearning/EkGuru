/**
 * ============================================================================
 * EkGuru — TUTOR APPLICATION + LIVE FEED BACKEND  (single-file, consolidated)
 * ============================================================================
 *
 * GENERATED FILE — do not hand-edit.
 * Rebuild with:  node tools/build-combined-code.mjs
 *
 * WHAT THIS IS
 * The complete EkGuru *form* Apps Script backend in ONE file, made by
 * concatenating these three source files verbatim, in this order:
 *
 *   1. ApplicationSchema.gs   -> PART 1  (schema, 69 columns)
 *   2. ApplicationIntake.gs   -> PART 2  (application backend)
 *   3. Unified.gs             -> PART 3  (the one doGet / doPost)
 *
 * Nothing was rewritten: every function, constant, comment and blank line from
 * the three files is present. The only edits are this header, a banner before
 * each part, and the duplicate `"use strict";` directives (see below).
 *
 * NOTE ON NUMBERING: the three parts below are labelled PART 1/2/3. Inside
 * PART 3, Unified.gs numbers its own internal sections "SECTION 1 EK_ CONFIG",
 * "SECTION 2 THE ROUTER", "SECTION 3 FUTURE MODULES" — those are unrelated to
 * the PART numbers and are left exactly as their author wrote them.
 *
 * WHY THIS FILE EXISTS
 * Apps Script puts every .gs file in a project into ONE global scope, so the
 * three sources could not simply be pasted side by side — each opened with its
 * own `"use strict";`, and a repeated directive is a parse error. They are
 * otherwise collision-free: 0 shared function names, 0 shared global vars,
 * exactly one doGet() and one doPost().
 *
 * "use strict"
 * Only the FIRST `"use strict";` is kept, as the first statement of the file,
 * so it applies to the whole script. The other two are commented out. This is
 * the only semantic difference from the separate files, and it is a STRICTER
 * outcome, not a looser one: all three sections now run in strict mode, which
 * each of them asked for individually anyway.
 *
 * ---------------------------------------------------------------------------
 * WHICH APPS SCRIPT PROJECT THIS GOES INTO
 * ---------------------------------------------------------------------------
 * This is the FORM project — also called "EkGuru Unified" — the project bound
 * to the EkGuru DB workbook (tutors / reviews / settings / bookings / contacts /
 * signups / applications). It is the project whose Code.gs serves:
 *
 *   ?tab=tutors|reviews|settings|support      ?action=health
 *   POST kinds: booking | contact | review | signup | application
 *
 * This is NOT the payments project. The payments backend lives in
 * apps-script/Code.gs and talks about Razorpay, Payments, Customers, Refunds
 * and WebhookEvents. It stays a SEPARATE project on purpose — see
 * apps-script/LIVE-FEED-SETUP.md and apps-script/UNIFIED-SETUP.md
 * ("Each backend is its own project; mixing them breaks both").
 * Do NOT paste this file into the payments project, and do not paste the
 * payments Code.gs in here.
 *
 * ---------------------------------------------------------------------------
 * SETUP  (full walkthrough: apps-script/UNIFIED-SETUP.md)
 * ---------------------------------------------------------------------------
 * 1. Open the EkGuru DB sheet -> Extensions -> Apps Script.
 *    The project MUST be created from that sheet (a bound project).
 * 2. Delete the sample code. Paste ALL of this file into Code.gs. Save.
 *    The editor must show no red error.
 * 3. Run the function `selfTest_` once and authorise. View -> Logs shows every
 *    feed tab with its row count, plus intake and application health.
 * 4. Deploy -> Manage deployments -> Edit the EXISTING deployment ->
 *    Version: New version -> Deploy.
 *    Never "New deployment" — it mints a new URL and both feed.url and
 *    intake.url in js/site-config.js go stale.
 * 5. Check ?action=health — the "application" block must not say "absent".
 *
 * SCRIPT PROPERTIES (File -> Project Settings -> Script Properties)
 *   EKGURU_DB_SPREADSHEET_ID  only if the project is not bound to the sheet
 *   EK_ADMIN_TOKEN            required for the owner/admin actions
 *   EK_ADMIN_NAME             optional, written into reviewed_by
 *   APPLICATION_MAIL_ENABLED  optional, "false" stops applicant email
 *   APPLICATION_OWNER_INBOX   optional, reply-to on applicant emails
 *   APPLICATION_SENDER_NAME   optional, display name of the sender
 *   APPLICATION_SITE_URL      optional, used in the email footer
 *
 * PUBLIC ENTRY POINTS (contracts unchanged from the separate files)
 *   doGet(e)   ?tab=tutors|reviews|settings|support  -> CSV
 *              ?tab=health | bare                     -> combined health JSON
 *              ?action=health                         -> intake health
 *              ?action=ping&token=...                 -> admin ping
 *              ?action=ekHealth                       -> application health
 *   doPost(e)  JSON body, kind: booking|contact|review|signup|application
 *              action: markReplied | ekAdminUpdate | ekStatus | ekHealth
 *   onOpen(e)  adds the EkGuru menu to the spreadsheet
 *   onEdit(e)  installable edit hook (unchanged from LiveFeed.gs)
 *   selfTest_(), installTriggers(), clearFeedCache()   <- run manually
 *
 * SIZE
 * ~3,300 lines / ~160 KB. Well inside the Apps Script per-file limit
 * (about 500 KB of code), so no splitting is needed.
 * ============================================================================
 */

"use strict";


/* ==========================================================================
   PART 1 of 3 — SCHEMA  (source: ApplicationSchema.gs)
   -----------------------------------------------------------------------
   The 69-column application schema: field definitions, limits, statuses,
   allowed status moves, which transition sends which email, and the
   server-only column list. This is the single source of truth that
   js/join-schema.js is generated from.
   ========================================================================== */

/**
 * ============================================================================
 * EkGuru — APPLICATION SCHEMA (single source of truth)
 * ============================================================================
 * This file is loaded by BOTH sides:
 *
 *   · the browser  — join.html → js/join-schema.js is a generated copy of
 *                    this file (tools/build-join-schema.mjs), so the page
 *                    never needs a second request;
 *   · Apps Script  — pasted into the intake project as ApplicationSchema.gs,
 *                    which is what makes server-side validation impossible
 *                    to drift from what the wizard can send.
 *
 * It holds NO secrets: no spreadsheet id, no deployment url, no key. It is
 * a description of fields, limits and column names, nothing else.
 *
 * ---------------------------------------------------------------------------
 * THE ONE RULE THIS FILE EXISTS TO ENFORCE
 * ---------------------------------------------------------------------------
 * Every field the wizard collects is written to a NAMED COLUMN or into the
 * documented `details_json` column. Nothing is silently dropped. The server
 * builds its stored row FROM THIS TABLE, so a field that exists in the table
 * but not in a submitted payload is stored as "" (never as a missing column),
 * and a field in the payload but not in the table is refused loudly — not
 * quietly ignored, which is what happened before this file existed
 * (Intake.gs v1.2.0 dropped any unknown key with no error, so a renamed
 * wizard field lost the applicant's text and nobody found out).
 *
 * ---------------------------------------------------------------------------
 * COMPATIBILITY, DELIBERATELY
 * ---------------------------------------------------------------------------
 * The first 17 columns are EXACTLY the pre-existing applications header:
 *
 *   timestamp, reference, status, approved, name, email, city, country,
 *   subject, experience, rate_usd, availability, bio, photo_link,
 *   video_link, languages, notes
 *
 * So a row written by Intake.gs v1.2.0 (13 fields) and a row written by this
 * schema (60+ fields) live in the same tab, in the same shape, and the
 * dashboard formulas (dashboard!B3 = COUNTIF(applications!C:C,"pending") …)
 * keep working untouched. New columns are ADDED after `notes`; existing
 * columns are never moved, renamed or removed.
 *
 * Column ORDER here is only the order new columns are appended in. Reading
 * and writing is by HEADER NAME at runtime (intakeHeaderMap_), never by a
 * hardcoded index — so if the owner inserts a column by hand in the middle
 * of the tab, nothing breaks.
 * ============================================================================
 */

/* "use strict"; — hoisted to the top of this file (one directive for the whole script) */

var EKGURU_SCHEMA_VERSION = "2.1.0";

/* ---------------------------------------------------------------------------
   Column types understood by both sides
     text    plain single-line text, HTML-stripped, formula-injection-safe
     long    multi-line text (bio, notes, json blobs)
     email   RFC-ish mailbox check
     url     must be https://
     phone   contact number, digits only after cleaning, 7-15 digits so both
             an Indian 10-digit number and an international one fit
     int     whole number inside [min, max]
     enum    one of values (case-insensitive on the way in, stored as given)
     bool    "yes" / "no"
     list    array of strings, stored as JSON, each item <= itemMax
     json    free-form JSON object, stored as a JSON string
     date    YYYY-MM-DD
     stamp   ISO timestamp, server-set only
   --------------------------------------------------------------------------- */

/* The availability contract. One object per day, MONDAY FIRST
   (JavaScript's getDay() is Sunday-first — this list is not indexed by it).
   A day with no teaching time simply has no entry; an empty array means the
   tutor is not available at all. Times are 24-hour "HH:MM" in the tutor's
   own timezone, which is stored in the `timezone` column next to it, so
   nothing has to be guessed later. */
var EKGURU_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

/* Submission statuses. These are the ONLY values the state machine allows.
   `pending`, `approved`, `rejected` already exist in the live tab and in
   Intake.gs v1.2.0, so they are kept verbatim. The rest are additions that
   do not change the meaning of a single existing row:
     pending            → submitted, waiting for a human (dashboard counts it)
     needs_information  → a reviewer asked the applicant for corrections
     under_review       → someone has opened it; no decision yet
     approved           → reviewed and accepted (dashboard!B4 counts approved=yes)
     rejected           → reviewed and refused, WITH A REASON in review notes
     superseded         → an older row replaced by a newer submission
                          (written by intakeMarkDuplicateApplications, kept) */
var EKGURU_STATUSES = [
  "pending", "needs_information", "under_review", "approved", "rejected", "superseded"
];

/* Allowed status moves. Anything not listed is refused by the server, so a
   stray edit or a replayed request cannot walk an application backwards
   from rejected to approved without going through review again. */
var EKGURU_STATUS_MOVES = {
  pending:           ["under_review", "needs_information", "approved", "rejected"],
  under_review:      ["needs_information", "approved", "rejected"],
  needs_information: ["under_review", "approved", "rejected"],
  approved:          ["rejected"],
  rejected:          ["under_review"],
  superseded:        []
};

/* Which transition an applicant should be emailed about, and the template
   key that produces it. `null` = change the sheet, send nothing. Keeping
   this table here (not inside the mailer) means "do we email on this
   transition?" is one visible list, not a fact buried in an if-statement. */
var EKGURU_MAIL_ON = {
  pending:           "received",
  needs_information: "needs_information",
  approved:          "approved",
  rejected:          "rejected"
};

/* ---------------------------------------------------------------------------
   THE COLUMNS
   ---------------------------------------------------------------------------
   col      header written into row 1 of `applications`
   src      the key the wizard sends inside `fields` ("" = server fills it)
   group    wizard step, for documentation and the admin view
   type     see above
   max      character limit (hard: the server refuses, it does not truncate)
   --------------------------------------------------------------------------- */
var EKGURU_APPLICATION_FIELDS = [
  /* -------- 1–17: the pre-existing header, unchanged, same order -------- */
  { col: "timestamp",    src: "",                group: "system",   type: "stamp" },
  { col: "reference",    src: "",                group: "system",   type: "text",  max: 20 },
  { col: "status",       src: "",                group: "system",   type: "enum",  values: EKGURU_STATUSES },
  { col: "approved",     src: "",                group: "system",   type: "bool" },
  { col: "name",         src: "name",            group: "personal", type: "text",  max: 80,  required: true },
  { col: "email",        src: "email",           group: "personal", type: "email", max: 120, required: true },
  { col: "city",         src: "city",            group: "personal", type: "text",  max: 80,  required: true },
  { col: "country",      src: "country",         group: "personal", type: "text",  max: 60,  required: true },
  { col: "subject",      src: "subject",         group: "teaching", type: "text",  max: 60,  required: true },
  { col: "experience",   src: "experience",      group: "teaching", type: "text",  max: 300 },
  { col: "rate_usd",     src: "rate_usd",        group: "pricing",  type: "int",   min: 1, max: 200, required: true },
  { col: "availability", src: "availability",    group: "schedule", type: "text",  max: 400 },
  { col: "bio",          src: "bio",             group: "profile",  type: "long",  max: 1500, required: true },
  { col: "photo_link",   src: "photo_link",      group: "profile",  type: "url",   max: 300 },
  { col: "video_link",   src: "video_link",      group: "profile",  type: "url",   max: 300 },
  { col: "languages",    src: "languages",       group: "teaching", type: "text",  max: 120 },
  { col: "notes",        src: "notes",           group: "review",   type: "long",  max: 2000 },

  /* -------- 18+: every field the six-step wizard actually collects ------ */
  { col: "display_name",   src: "display_name",   group: "personal", type: "text", max: 60 },
  { col: "state",          src: "state",          group: "personal", type: "text", max: 80 },
  { col: "contact_pref",   src: "contact_pref",   group: "personal", type: "enum",
    values: ["Email", "WhatsApp", "Video call"] },
  { col: "intro",          src: "intro",          group: "personal", type: "long", max: 400 },
  /* Personal WhatsApp number. Genuinely optional, PRIVATE (never printed on
     the public profile and never in a feed), and stored in E.164-ish text so
     the country code is never guessed away. `phone` keeps its own separate
     role in the feed's private-column list; this is a distinct column. */
  { col: "whatsapp",       src: "whatsapp",       group: "personal", type: "phone", max: 24 },

  { col: "subjects_json",  src: "subjects",       group: "teaching", type: "list", itemMax: 60, maxItems: 11 },
  { col: "levels_json",    src: "levels",         group: "teaching", type: "list", itemMax: 40, maxItems: 7 },
  { col: "methods_json",   src: "methods",        group: "teaching", type: "list", itemMax: 40, maxItems: 7 },
  { col: "teach_langs_json", src: "teach_langs",  group: "teaching", type: "list", itemMax: 40, maxItems: 6 },
  { col: "hindi_level",    src: "hindi_level",    group: "teaching", type: "enum",
    values: ["Native", "Fluent", "Advanced"] },
  { col: "english_level",  src: "english_level",  group: "teaching", type: "enum",
    values: ["Beginner", "Intermediate (B1)", "Upper intermediate (B2)", "Advanced (C1)",
             "Native / bilingual"] },
  { col: "other_langs",    src: "other_langs",    group: "teaching", type: "text", max: 100 },
  { col: "years",          src: "years",          group: "teaching", type: "enum",
    values: ["Less than 1 year", "1-2 years", "3-5 years", "6-10 years", "More than 10 years"] },
  { col: "online_years",   src: "online_years",   group: "teaching", type: "text", max: 20 },
  { col: "less_exp",       src: "less_exp",       group: "teaching", type: "long", max: 300 },
  { col: "platforms",      src: "platforms",      group: "teaching", type: "text", max: 160 },

  { col: "edu_qual",       src: "edu_qual",       group: "education", type: "enum",
    values: ["Secondary school", "Higher secondary / 12th", "Bachelor's degree", "Master's degree",
             "M.Phil or PhD", "Teaching diploma (B.Ed / D.El.Ed / equivalent)", "Other"] },
  { col: "edu_inst",       src: "edu_inst",       group: "education", type: "text", max: 120 },
  { col: "edu_year",       src: "edu_year",       group: "education", type: "int", min: 1950, max: 2100 },
  { col: "edu_extra",      src: "edu_extra",      group: "education", type: "long", max: 400 },
  { col: "certs",          src: "certs",          group: "education", type: "long", max: 400 },
  { col: "bed_detail",     src: "bed_detail",     group: "education", type: "text", max: 160 },
  { col: "doc_refs",       src: "doc_refs",       group: "education", type: "text", max: 300 },

  { col: "headline",       src: "headline",       group: "profile", type: "text", max: 120 },
  { col: "why",            src: "why",            group: "profile", type: "long", max: 500 },
  { col: "video_thumb",    src: "video_thumb",    group: "profile", type: "url", max: 300 },
  { col: "sample_link",    src: "sample_link",    group: "profile", type: "url", max: 300 },
  { col: "website",        src: "website2",       group: "profile", type: "url", max: 300 },
  { col: "linkedin",       src: "linkedin",       group: "profile", type: "url", max: 300 },
  { col: "profile_url",    src: "profile_url",    group: "profile", type: "url", max: 300 },

  { col: "currency",       src: "currency",       group: "pricing", type: "enum",
    values: ["USD", "INR"], default: "USD" },
  { col: "duration",       src: "duration",       group: "pricing", type: "enum",
    values: ["30 min", "50 min", "60 min", "90 min"], default: "50 min" },
  { col: "trial",          src: "trial",          group: "pricing", type: "enum",
    values: ["Free short trial", "Discounted trial", "Full price from the first lesson"] },

  { col: "timezone",       src: "timezone",       group: "schedule", type: "enum",
    values: ["Asia/Kolkata", "Asia/Karachi", "Asia/Dhaka", "Asia/Kathmandu", "Asia/Dubai",
             "Asia/Riyadh", "Asia/Singapore", "Asia/Tokyo", "Australia/Sydney",
             "Europe/London", "Europe/Paris", "Europe/Berlin", "America/New_York",
             "America/Chicago", "America/Denver", "America/Los_Angeles", "America/Toronto",
             "America/Vancouver", "America/Sao_Paulo", "Africa/Nairobi"] },
  { col: "availability_json", src: "availability_slots", group: "schedule", type: "json", max: 2000 },
  { col: "availability_meta", src: "availability_meta", group: "schedule", type: "json", max: 400 },

  { col: "consent_privacy", src: "",              group: "consent", type: "bool" },
  { col: "consent_terms",   src: "",              group: "consent", type: "bool" },
  { col: "declaration",     src: "",              group: "consent", type: "text", max: 120 },
  { col: "consent_at",      src: "",              group: "consent", type: "stamp" },

  { col: "schema_version",  src: "",              group: "system", type: "text", max: 12 },
  { col: "created_at",      src: "",              group: "system", type: "stamp" },
  { col: "updated_at",      src: "",              group: "system", type: "stamp" },
  { col: "email_status",    src: "",              group: "system", type: "text", max: 300 },
  { col: "email_sent_at",   src: "",              group: "system", type: "stamp" },
  { col: "review_notes",    src: "",              group: "review", type: "long", max: 2000 },
  { col: "rejection_reason", src: "",             group: "review", type: "long", max: 1000 },
  { col: "reviewed_by",     src: "",              group: "review", type: "text", max: 120 },
  { col: "reviewed_at",     src: "",              group: "review", type: "stamp" },
  { col: "previous_status", src: "",              group: "review", type: "text", max: 20 },
  { col: "source",          src: "source",        group: "system", type: "text", max: 40 },
  { col: "details_json",    src: "details",       group: "system", type: "long", max: 4000 }
];

/* Columns the server owns. A browser that sends one of these is ignored on
   that key (never merged into the row), so a visitor cannot mark themselves
   approved, write their own reference, or forge an email_status. */
var EKGURU_SERVER_ONLY = [
  "timestamp", "reference", "status", "approved", "consent_privacy", "consent_terms",
  "declaration", "consent_at", "schema_version", "created_at", "updated_at",
  "email_status", "email_sent_at", "review_notes", "rejection_reason",
  "reviewed_by", "reviewed_at", "previous_status"
];

/* The header this schema wants, in order. The migration appends whatever is
   missing at the END and never reorders what is already there. */
var EKGURU_APPLICATION_HEADER = EKGURU_APPLICATION_FIELDS.map(function (f) { return f.col; });

/* Payload size guard. The wizard's biggest realistic payload (every field
   filled, all boxes ticked) is roughly 6 KB; 16 KB leaves room without
   letting a hostile client post a megabyte. Apps Script's own postData
   ceiling is ~50 MB, so this is our limit, not theirs. */
var EKGURU_MAX_BYTES = 16000;

/* Details JSON is the documented overflow bucket (see Phase 2 of the
   brief: "a structured, documented additional-data field"). Anything the
   wizard wants to send that has no column of its own lands here as
   {key: value}, and the server keeps it verbatim after length checks. */
var EKGURU_DETAILS_MAX_KEYS = 30;
var EKGURU_DETAILS_MAX_VALUE = 300;

/* ---------------------------------------------------------------------------
   Small helpers shared by both sides. Deliberately ES5: Apps Script's V8
   runtime accepts ES2019, but the browser copy also has to run in whatever
   the visitor's phone has, and this file must stay paste-safe.
   --------------------------------------------------------------------------- */

function ekSchemaField(srcOrCol) {
  for (var i = 0; i < EKGURU_APPLICATION_FIELDS.length; i++) {
    var f = EKGURU_APPLICATION_FIELDS[i];
    if (f.col === srcOrCol || (f.src && f.src === srcOrCol)) return f;
  }
  return null;
}

/* Fields a browser may send (everything with a src that is not server-only). */
function ekSchemaClientFields() {
  var out = [];
  for (var i = 0; i < EKGURU_APPLICATION_FIELDS.length; i++) {
    var f = EKGURU_APPLICATION_FIELDS[i];
    if (!f.src) continue;
    if (EKGURU_SERVER_ONLY.indexOf(f.col) !== -1) continue;
    out.push(f.src);
  }
  return out;
}

/* Which header a given payload key lands in. null = no dedicated column,
   so it belongs in details_json (never silently dropped). */
function ekSchemaColumnFor(src) {
  var f = ekSchemaField(src);
  return f ? f.col : null;
}

/* "1-2 years" as typed in some places, "1–2 years" as the page renders it
   with an en dash. Normalise en/em dashes to a hyphen so an option list
   cannot fail on typography. */
function ekNormDash(s) {
  return String(s == null ? "" : s).replace(/[\u2010-\u2015\u2212]/g, "-");
}

/* The status a submitted application starts in. */
function ekInitialStatus() { return "pending"; }

/* Can `from` move to `to`? Pure, so the frontend tests and the server agree. */
function ekCanMove(from, to) {
  var allowed = EKGURU_STATUS_MOVES[String(from || "")] || [];
  return allowed.indexOf(String(to || "")) !== -1;
}

/* The mail template for a transition, or "" when nothing should be sent. */
function ekMailFor(to) {
  return EKGURU_MAIL_ON[String(to || "")] || "";
}

/* Exported for Node tests and for the Apps Script project. In Apps Script
   every top-level function is global already, so this is a no-op there. */
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    VERSION: EKGURU_SCHEMA_VERSION,
    DAYS: EKGURU_DAYS,
    STATUSES: EKGURU_STATUSES,
    MOVES: EKGURU_STATUS_MOVES,
    MAIL_ON: EKGURU_MAIL_ON,
    FIELDS: EKGURU_APPLICATION_FIELDS,
    HEADER: EKGURU_APPLICATION_HEADER,
    SERVER_ONLY: EKGURU_SERVER_ONLY,
    MAX_BYTES: EKGURU_MAX_BYTES,
    field: ekSchemaField,
    clientFields: ekSchemaClientFields,
    columnFor: ekSchemaColumnFor,
    canMove: ekCanMove,
    mailFor: ekMailFor,
    normDash: ekNormDash
  };
}


/* ==========================================================================
   PART 2 of 3 — APPLICATION BACKEND  (source: ApplicationIntake.gs)
   -----------------------------------------------------------------------
   Validation, row building, dedupe/retry identity, the four applicant
   emails, the owner-only admin API and the status lookup. Called from the
   router in Section 3 through the two seams ekApplicationAction_() and
   ekApplicationGet_().
   ========================================================================== */

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

/* "use strict"; — hoisted to the top of this file (one directive for the whole script) */

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


/* ==========================================================================
   PART 3 of 3 — UNIFIED ROUTER  (source: Unified.gs)
   -----------------------------------------------------------------------
   The ONE doGet() and doPost(): feed tabs, intake (bookings / contacts /
   reviews / sign-ups), the application seam, owner actions, quota, and the
   EkGuru sheet menu. Contains the consolidated backend's self-test
   (selfTest_) and the onOpen/onEdit entry points.
   ========================================================================== */

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

/* "use strict"; — hoisted to the top of this file (one directive for the whole script) */

/* ============================================================================
   SECTION 1 — EK_ CONFIG: EVERY KNOB IN ONE PLACE
   ----------------------------------------------------------------------------
   Flip a flag, save, redeploy the SAME deployment (Manage deployments →
   Edit → New version → Deploy). No other edit is ever needed: each flag
   below is read live on every request.
   ========================================================================== */
var EK_UNIFIED_VERSION = "2.2.0";

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

  /* Application backend v2 (ApplicationIntake.gs). Answers only its own
     action and returns null for anything else, so every route below is
     unchanged when that file is not pasted yet. */
  if (typeof ekApplicationGet_ === "function") {
    var ekGet = ekApplicationGet_(e);
    if (ekGet) return ekGet;
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
var INTAKE_VERSION = "1.3.1";
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

    /* Application backend v2 (ApplicationIntake.gs). Handles kind
       "application" and the three ek* actions; returns null for
       everything else, so reviews, bookings, contacts and sign-ups keep
       going through the code below exactly as before. */
    /* Honeypot: a real person never sees this box. Pretend success, store
       nothing. This MUST run before any handler that writes a row — the
       application seam below used to run first, so a filled honeypot still
       produced a stored application and an email to the owner. Owner actions
       carry no `website` field, so they are unaffected. */
    if (String(body.website || "").trim() !== "") {
      return intakeJson_({ ok: true, reference: "EG-" + intakeRef_() });
    }

    if (typeof ekApplicationAction_ === "function") {
      var ekHandled = ekApplicationAction_(body);
      if (ekHandled) return ekHandled;
    }

    /* Owner action, not a visitor submission: the admin dashboard
       calls this AFTER a reply email has been sent, so the contacts
       tab shows status = "replied". No consent, no quota, no new row. */
    if (String(body.action || "") === "markReplied") {
      return intakeJson_(markContactReplied_(
        String(body.ref || ""), String(body.email || ""), String(body.note || "")));
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
  var out = { ok: true, version: INTAKE_VERSION, spreadsheetBound: true,
              at: new Date().toISOString(), pendingRows: tabs };
  /* Is the six-step wizard backend (ApplicationIntake.gs) in this project? */
  if (typeof ekHealth_ === "function") {
    var ek = ekHealth_();
    out.application = { version: ek.version, schema: ek.schema, ok: ek.ok,
                        columns: ek.columns ? { expected: ek.columns.expected, present: ek.columns.present } : null };
    if (!ek.ok) out.application.error = ek.error;
  } else {
    out.application = { version: "absent", ok: false,
                        error: "ApplicationIntake.gs is not pasted into this project" };
  }
  return out;
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

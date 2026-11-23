/* =========================================================
   EkGuru — application schema (GENERATED, do not edit by hand)
   ---------------------------------------------------------
   Source: apps-script/ApplicationSchema.gs
   Rebuild: node tools/build-join-schema.mjs

   js/join-wizard.js reads window.EKGURU_APP_SCHEMA to decide what to send;
   apps-script/ApplicationIntake.gs uses the same table to decide what to
   accept and where to write it. One list, two runtimes — so a field can
   never be collected by the page and unknown to the server.
   ========================================================= */
(function () {
  "use strict";
  if (window.EKGURU_APP_SCHEMA) return;
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

  "use strict";

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

  /* (Node exports removed in the browser copy.) */

  window.EKGURU_APP_SCHEMA = {
    version: EKGURU_SCHEMA_VERSION,
    days: EKGURU_DAYS,
    statuses: EKGURU_STATUSES,
    moves: EKGURU_STATUS_MOVES,
    mailOn: EKGURU_MAIL_ON,
    fields: EKGURU_APPLICATION_FIELDS,
    header: EKGURU_APPLICATION_HEADER,
    serverOnly: EKGURU_SERVER_ONLY,
    maxBytes: EKGURU_MAX_BYTES,
    field: ekSchemaField,
    clientFields: ekSchemaClientFields,
    columnFor: ekSchemaColumnFor,
    canMove: ekCanMove,
    mailFor: ekMailFor,
    normDash: ekNormDash
  };
})();

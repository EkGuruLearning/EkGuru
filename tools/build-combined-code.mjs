#!/usr/bin/env node
/* =========================================================
   EkGuru: build apps-script/combined/Code.gs

   Concatenates the three form-backend sources into ONE file for a single
   Apps Script project, in this order:

     1. ApplicationSchema.gs   -> SECTION 1 (schema)
     2. ApplicationIntake.gs   -> SECTION 2 (application backend)
     3. Unified.gs             -> SECTION 3 (the one doGet / doPost)

   The sources are copied VERBATIM. The only edits are:
     - the file header (generated, explains what this is);
     - a banner before each section;
     - `"use strict";` — each source opens with one; in a single file it may
       appear once, as the first statement. The first is kept, the others are
       commented out with a pointer to that note.

   Run: node tools/build-combined-code.mjs
   Then paste apps-script/combined/Code.gs into the FORM Apps Script project.

   This does NOT touch the payments backend (apps-script/Code.gs), which stays
   its own project on purpose.
   ========================================================= */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const OUT = path.join(ROOT, "apps-script", "combined", "Code.gs");

const SECTIONS = [
  {
    file: "apps-script/ApplicationSchema.gs",
    title: "PART 1 of 3 — SCHEMA  (source: ApplicationSchema.gs)",
    blurb: [
      "The 69-column application schema: field definitions, limits, statuses,",
      "allowed status moves, which transition sends which email, and the",
      "server-only column list. This is the single source of truth that",
      "js/join-schema.js is generated from.",
    ],
  },
  {
    file: "apps-script/ApplicationIntake.gs",
    title: "PART 2 of 3 — APPLICATION BACKEND  (source: ApplicationIntake.gs)",
    blurb: [
      "Validation, row building, dedupe/retry identity, the four applicant",
      "emails, the owner-only admin API and the status lookup. Called from the",
      "router in Section 3 through the two seams ekApplicationAction_() and",
      "ekApplicationGet_().",
    ],
  },
  {
    file: "apps-script/Unified.gs",
    title: "PART 3 of 3 — UNIFIED ROUTER  (source: Unified.gs)",
    blurb: [
      "The ONE doGet() and doPost(): feed tabs, intake (bookings / contacts /",
      "reviews / sign-ups), the application seam, owner actions, quota, and the",
      "EkGuru sheet menu. Contains the consolidated backend's self-test",
      "(selfTest_) and the onOpen/onEdit entry points.",
    ],
  },
];

const HEADER = `/**
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
 * each part, and the duplicate \`"use strict";\` directives (see below).
 *
 * NOTE ON NUMBERING: the three parts below are labelled PART 1/2/3. Inside
 * PART 3, Unified.gs numbers its own internal sections "SECTION 1 EK_ CONFIG",
 * "SECTION 2 THE ROUTER", "SECTION 3 FUTURE MODULES" — those are unrelated to
 * the PART numbers and are left exactly as their author wrote them.
 *
 * WHY THIS FILE EXISTS
 * Apps Script puts every .gs file in a project into ONE global scope, so the
 * three sources could not simply be pasted side by side — each opened with its
 * own \`"use strict";\`, and a repeated directive is a parse error. They are
 * otherwise collision-free: 0 shared function names, 0 shared global vars,
 * exactly one doGet() and one doPost().
 *
 * "use strict"
 * Only the FIRST \`"use strict";\` is kept, as the first statement of the file,
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
 * 3. Run the function \`selfTest_\` once and authorise. View -> Logs shows every
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
`;

function banner(title, blurb) {
  const bar = "=".repeat(74);
  const dash = "-".repeat(71);
  return (
    "/* " + bar + "\n" +
    "   " + title + "\n" +
    "   " + dash + "\n" +
    blurb.map((l) => "   " + l + "\n").join("") +
    "   " + bar + " */\n\n"
  );
}

let out = HEADER;
for (const s of SECTIONS) {
  const src = fs.readFileSync(path.join(ROOT, s.file), "utf8");
  out += "\n\n" + banner(s.title, s.blurb);
  let strictDone = false;
  const kept = src.split("\n").map((line) => {
    if (line.trim() === '"use strict";' && !strictDone) {
      strictDone = true;
      return '/* "use strict"; — hoisted to the top of this file (one directive for the whole script) */';
    }
    return line;
  });
  out += kept.join("\n").replace(/\n+$/, "") + "\n";
}

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, out, "utf8");

const lines = out.split("\n").length;
console.log("built apps-script/combined/Code.gs");
console.log("  " + lines + " lines, " + out.length + " bytes");
console.log("  doGet:  " + (out.match(/^function doGet\(/gm) || []).length);
console.log("  doPost: " + (out.match(/^function doPost\(/gm) || []).length);

#!/usr/bin/env node
/* =========================================================
   EkGuru: build js/join-schema.js from apps-script/ApplicationSchema.gs
   ---------------------------------------------------------
   The wizard and the Apps Script backend must agree, exactly, on every field
   name and every character limit. Two hand-maintained lists drift — that is
   how `intro`, `other_langs`, `edu_extra`, `less_exp` and `bed_detail` were
   silently dropped by an earlier build of the wizard.

   So there is ONE source (apps-script/ApplicationSchema.gs) and this script
   copies it into the browser as js/join-schema.js. `tools/test-application-
   schema.mjs` fails the build if the copy is stale.

   Run:  node tools/build-join-schema.mjs
   ========================================================= */
import fs from "node:fs";
import path from "node:path";

const ROOT = path.join(import.meta.dirname, "..");
const SRC = path.join(ROOT, "apps-script", "ApplicationSchema.gs");
const OUT = path.join(ROOT, "js", "join-schema.js");

const source = fs.readFileSync(SRC, "utf8");

const banner = `/* =========================================================
   EkGuru — application schema (GENERATED, do not edit by hand)
   ---------------------------------------------------------
   Source: apps-script/ApplicationSchema.gs
   Rebuild: node tools/build-join-schema.mjs

   js/join-wizard.js reads window.EKGURU_APP_SCHEMA to decide what to send;
   apps-script/ApplicationIntake.gs uses the same table to decide what to
   accept and where to write it. One list, two runtimes — so a field can
   never be collected by the page and unknown to the server.
   ========================================================= */
`;

const body = `(function () {
  "use strict";
  if (window.EKGURU_APP_SCHEMA) return;
${source
  .split("\n")
  .map((line) => (line.trim() === "" ? "" : "  " + line))
  .join("\n")}
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
`;

const out = banner + body;

/* The generated file must not carry the Node export block: it would throw
   in a browser (no `module`). Strip it from the copy only. */
const cleaned = out.replace(
  /  \/\* Exported for Node tests[\s\S]*?^  \}$/m,
  "  /* (Node exports removed in the browser copy.) */"
);

fs.writeFileSync(OUT, cleaned, "utf8");
console.log(`wrote ${path.relative(ROOT, OUT)} (${cleaned.length} bytes)`);

#!/usr/bin/env node
/* Renders every email template fixture and prints a JSON summary the
   Python report builder consumes. Single source of truth: the code. */
"use strict";
const path = require("path");
global.window = {};
require(path.join(__dirname, "..", "js", "email-templates.js"));
const E = window.EKGURU_EMAIL;

const KEY2TYPE = {
  contactVisitor: "CONTACT_VISITOR_CONFIRMATION",
  contactInternal: "CONTACT_EKGURU_NOTIFICATION",
  bookingStudent: "BOOKING_STUDENT_CONFIRMATION",
  bookingTutor: "BOOKING_TUTOR_NOTIFICATION",
  bookingInternal: "BOOKING_EKGURU_NOTIFICATION",
  adminOutbound: "ADMIN_CONTACT_OUTBOUND",
  adminInternalCopy: "ADMIN_CONTACT_INTERNAL_COPY"
};

const out = { whitelist: E.WHITELIST, routes: E.ROUTES, templates: [] };
Object.keys(E.FIXTURES).forEach((k) => {
  const r = E.render(k, E.FIXTURES[k]);
  const byType = E.render(KEY2TYPE[k], E.FIXTURES[k]);
  const qa = E.ROLE_QA[k] || { mustSay: [], mustNotSay: [] };
  const txt = r.ok ? (r.subject + " " + r.html + " " + r.text).toLowerCase() : "";
  const qaBad = [];
  qa.mustSay.forEach((m) => { if (txt.indexOf(m.toLowerCase()) === -1) qaBad.push("missing:" + m); });
  qa.mustNotSay.forEach((m) => { if (txt.indexOf(m.toLowerCase()) > -1) qaBad.push("says:" + m); });
  const tpl = E.TEMPLATES[k];
  out.templates.push({
    key: k,
    type: KEY2TYPE[k],
    role: tpl.role,
    allowedVars: tpl.allowedVars,
    subject: r.subject || "",
    render_ok: r.ok,
    type_name_render_ok: byType.ok,
    render_errors: r.errors || [],
    role_qa: { mustSay: qa.mustSay, mustNotSay: qa.mustNotSay, violations: qaBad, pass: qaBad.length === 0 }
  });
});
process.stdout.write(JSON.stringify(out, null, 2));

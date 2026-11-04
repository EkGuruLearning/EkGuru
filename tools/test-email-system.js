#!/usr/bin/env node
/* =========================================================
   EkGuru — EMAIL SYSTEM TESTS  (v101 — SIMPLE ROLE TEMPLATES)
   ---------------------------------------------------------
   Loads js/email-templates.js + js/mailer.js against a minimal
   browser shim and verifies the EMAIL RESET contract:

     1. six routable message types are whitelisted; the legacy booking
        internal template can render for compatibility but cannot be sent;
     2. the registry rejects unknown / missing / undeclared vars
        and raw {placeholders};
     3. user values are HTML-escaped (no raw <script> survives);
     4. role-language QA (§27-H) — a tutor mail must not read
        like a student mail, internal wording never leaks;
     5. booking sends reach only tutor + student (never owner); contact
        sends retain their separate internal record;
     6. tutorEmailInfo() classifies tutors (ACTIVE+VALID / MISSING
        / INVALID / UNPUBLISHED / DISABLED) and
        TUTOR_EMAIL_UNAVAILABLE routing holds.

   Run:  node tools/test-email-system.js
   ========================================================= */
"use strict";
const path = require("path");
const ROOT = path.join(__dirname, "..");

/* ------------------------- browser shim ------------------------- */
global.window = {};
global.localStorage = (function () {
  const s = {};
  return {
    getItem: (k) => (k in s ? s[k] : null),
    setItem: (k, v) => { s[k] = String(v); },
    removeItem: (k) => { delete s[k]; },
    clear: () => { for (const k in s) delete s[k]; }
  };
})();
global.location = { href: "https://ekguru.shop/find-tutors.html" };

window.EKGURU_SITE = {
  brand: "EkGuru",
  tagline: "Learn Hindi online",
  baseUrl: "https://ekguru.shop/",
  email: "EkGuruLearning@gmail.com",
  founder: { name: "Prakash", linkedin: "" },
  mail: {
    enabled: true,
    copyToStudent: true,
    copyToSite: false,
    contactProvider: "",
    appsScript: {
      url: "https://script.google.com/macros/s/AKfycbTEST/exec",
      token: "test-client-token"
    },
    web3formsKeys: ["11111111-2222-3333-4444-555555555555"],
    staticFormsKey: "test-static",
    siteKey: "EkGuruLearning@gmail.com"
  }
};

/* fake relay: answers a JSON success over text/plain */
const POSTED = [];
global.fetch = function (url, opts) {
  const body = String(opts && opts.body || "");
  let parsed = {};
  try { parsed = JSON.parse(body); } catch (e) { /* urlencoded/formdata */ }
  POSTED.push({ url: String(url), raw: body, parsed: parsed });
  return Promise.resolve({
    ok: true,
    text: () => Promise.resolve(JSON.stringify({ success: "true", sent: true }))
  });
};
window.fetch = global.fetch;

/* ------------------------- load ------------------------- */
require(path.join(ROOT, "js", "email-templates.js"));
require(path.join(ROOT, "js", "mailer.js"));

const E = window.EKGURU_EMAIL;
const M = window.EkGuruMail;

let failures = 0;
function check(name, cond, extra) {
  const ok = !!cond;
  if (!ok) failures++;
  console.log((ok ? "PASS" : "FAIL") + "  " + name + (ok ? "" : "  →  " + (extra || "")));
}

/* =========================== 1. registry =========================== */
check("EKGURU_EMAIL exposed", !!E);
check("EkGuruMail exposed", !!M);
const routeMap = M.routingMap();
check("booking owner route is absent and explicitly policy-blocked",
  routeMap.bookingInternal === null && routeMap.bookingInternalPolicy === "NOT_SENT_BY_POLICY",
  JSON.stringify({ bookingInternal: routeMap.bookingInternal, policy: routeMap.bookingInternalPolicy }));
const TYPES = ["contact_submitter_confirmation", "contact_internal_record",
  "booking_student_confirmation", "booking_tutor_notification",
  "ADMIN_CONTACT_OUTBOUND", "ADMIN_CONTACT_INTERNAL_COPY"];
check("WHITELIST = six routable message types; booking owner email excluded",
  TYPES.every((t) => (E.WHITELIST || []).indexOf(t) > -1) && E.WHITELIST.length === 6 &&
    E.WHITELIST.indexOf("booking_internal_record") === -1,
  JSON.stringify(E.WHITELIST));

/* =========================== 2. render =========================== */
const KEY2TYPE = {
  contactVisitor: "contact_submitter_confirmation",
  contactInternal: "contact_internal_record",
  bookingStudent: "booking_student_confirmation",
  bookingStudentPending: "booking_student_pending",
  bookingTutor: "booking_tutor_notification",
  bookingInternal: "booking_internal_record",
  adminOutbound: "ADMIN_CONTACT_OUTBOUND",
  adminInternalCopy: "ADMIN_CONTACT_INTERNAL_COPY"
};
Object.keys(E.FIXTURES).forEach((k) => {
  const r = E.render(k, E.FIXTURES[k]);
  check("fixture renders: " + k, r.ok && r.subject && r.html && r.text, (r.errors || []).join(", "));
  const byType = E.render(KEY2TYPE[k], E.FIXTURES[k]);
  check("type-name renders: " + KEY2TYPE[k], byType.ok && byType.template === k);
});

check("unknown type rejected", E.render("NOT_A_TYPE", {}).ok === false);
check("missing vars omitted (still renders)",
  E.render("bookingStudent", { studentName: "X" }).ok === true);
check("undeclared extra var ignored",
  E.render("bookingStudent", Object.assign({}, E.FIXTURES.bookingStudent, { extraVar: "x" })).ok === true);

/* =========================== 3. escaping =========================== */
const evil = Object.assign({}, E.FIXTURES.bookingStudent, {
  studentName: "<script>alert(1)</script>Priya"
});
const evilR = E.render("bookingStudent", evil);
check("no raw <script> survives escaping", evilR.ok && !/<script/i.test(evilR.html) && /&lt;script/i.test(evilR.html));
check("raw {placeholder} never survives", !/\{[A-Za-z_]+\}/.test(evilR.html + evilR.text + evilR.subject));

/* =========================== 4. role language =========================== */
Object.keys(E.ROLE_QA).forEach((k) => {
  const r = E.render(k, E.FIXTURES[k]);
  const qa = E.ROLE_QA[k];
  if (!r.ok) { check("role-language render: " + k, false, (r.errors || []).join(", ")); return; }
  const text = (r.subject + " " + r.html + " " + r.text).toLowerCase();
  const bad = [];
  qa.mustSay.forEach((m) => { if (text.indexOf(m.toLowerCase()) === -1) bad.push("missing '" + m + "'"); });
  qa.mustNotSay.forEach((m) => { if (text.indexOf(m.toLowerCase()) > -1) bad.push("says '" + m + "'"); });
  check("role-language QA: " + k, bad.length === 0, bad.join("; "));
});

/* =========================== 5. send() =========================== */
const tara = {
  id: "tara", name: "Tara", lessonLength: "50 min", trialAvailable: true,
  email: "tara@example.com"
};
const sendPayload = {
  tutor: tara,
  name: "Priya", email: "priya@example.com",
  slot: "20 September 2026, 7:00 PM", timezone: "Asia/Kolkata",
  level: "Beginner", goal: "Conversation practice",
  message: "I want to speak better.",
  price: "Free trial", ref: "EK-TEST-01"
};

function byType(type) { return POSTED.filter((p) => p.parsed && p.parsed.type === type); }
function internalRows() {
  return POSTED.filter((p) => p.parsed && p.parsed["Reference Number"] && !p.parsed.type);
}

(async function () {
  localStorage.clear();
  POSTED.length = 0;
  let res;
  try {
    res = await M.send(sendPayload);
  } catch (e) {
    check("send() resolves (tutor WITH email)", false, e.message);
    res = null;
  }
  if (res) {
    check("send() resolves (tutor WITH email)", !!res.ok, JSON.stringify(res));
    const tutor = byType("booking_tutor_notification");
    const student = byType("booking_student_confirmation");
    check("tutor job stamped booking_tutor_notification", tutor.length === 1, "got " + tutor.length);
    check("student job stamped booking_student_confirmation", student.length === 1, "got " + student.length);
    const internalTyped = byType("booking_internal_record");
    check("booking never sends an internal/owner copy",
      internalTyped.length === 0 && internalRows().length === 0,
      "typed=" + internalTyped.length + ", rows=" + internalRows().length);
    check("booking recipients are only the tutor and student",
      POSTED.length === 2 && POSTED.every((p) =>
        ["tara@example.com", "priya@example.com"].indexOf(String(p.parsed.to || "").toLowerCase()) >= 0),
      JSON.stringify(POSTED.map((p) => p.parsed.to)));
    if (tutor[0]) {
      check("tutor payload has html + text", !!tutor[0].parsed.html && !!tutor[0].parsed.text);
      check("tutor idempotencyKey = entity|template|recipient",
        tutor[0].parsed.idempotencyKey === "EK-TEST-01|booking_tutor_notification|tara@example.com",
        JSON.stringify(tutor[0].parsed.idempotencyKey));
      check("tutor subject is the tutor notification subject",
        /new booking on ekguru/i.test(tutor[0].parsed.subject || ""),
        tutor[0].parsed.subject);
      check("tutor html rendered by template", /you have a new booking/i.test(tutor[0].parsed.html));
      check("tutor payload recipient = tutor email", tutor[0].parsed.to === "tara@example.com");
      check("tutor copy replyTo = student (supported direct-response)",
        (tutor[0].parsed.replyTo || "").toLowerCase() === "priya@example.com");
    }
    if (student[0]) {
      check("student recipient = student email", student[0].parsed.to === "priya@example.com");
      check("student html is the STUDENT template (not tutor's)",
        /your booking is confirmed/i.test(student[0].parsed.html) &&
        !/you have a new booking/i.test(student[0].parsed.html));
      check("student html does not expose tutor inbox",
        !/tara@example\.com/i.test(student[0].parsed.html));
      check("student idempotencyKey = entity|template|recipient",
        student[0].parsed.idempotencyKey === "EK-TEST-01|booking_student_confirmation|priya@example.com");
    }
  }

  /* ---- TUTOR WITHOUT an email → TUTOR_EMAIL_UNAVAILABLE ---- */
  const info = M.tutorEmailInfo({ id: "newtutor", name: "New Tutor" });
  check("tutorEmailInfo: missing → ACTIVE+MISSING / not available",
    info.state === "ACTIVE+MISSING" && info.available === false, JSON.stringify(info));
  check("tutorEmailInfo: valid email → ACTIVE+VALID",
    M.tutorEmailInfo(tara).state === "ACTIVE+VALID" && M.tutorEmailInfo(tara).available === true);
  check("tutorEmailInfo: bad email → ACTIVE+INVALID",
    M.tutorEmailInfo({ id: "x", name: "X", email: "not-an-email" }).state === "ACTIVE+INVALID");
  check("tutorEmailInfo: active:no → DISABLED",
    M.tutorEmailInfo({ id: "x", name: "X", email: "x@y.com", active: "no" }).state === "DISABLED");
  check("tutorEmailInfo: notification_email (snake) → ACTIVE+VALID",
    M.tutorEmailInfo({ id: "x", name: "X", notification_email: "tutor@x.com" }).state === "ACTIVE+VALID");
  const badAlias = M.tutorEmailInfo({ id: "x", name: "X", formKey: "not-an-email" });
  check("tutorEmailInfo: invalid legacy alias is refused, not sent to owner",
    badAlias.state === "ACTIVE+INVALID" && !badAlias.available && !badAlias.target, JSON.stringify(badAlias));
  const routeInfo = M.resolveRecipients("booking", {
    tutor: tara, studentEmail: "priya@example.com"
  });
  check("booking recipient resolution exposes tutor + student only (no internal inbox)",
    routeInfo.tutor === "tara@example.com" && routeInfo.student === "priya@example.com" &&
    !Object.prototype.hasOwnProperty.call(routeInfo, "internal"), JSON.stringify(routeInfo));

  /* ---- TUTOR WITHOUT an email → DEGRADED (owner decision, 4 Nov 2026) ----
     The booking still goes through: exactly one post, to the STUDENT
     only, with the honest pending receipt. The owner inbox is never a
     recipient; the owner relays via the bookings sheet. */
  POSTED.length = 0;
  const ghost = { id: "newtutor", name: "New Tutor", lessonLength: "50 min" };
  let dres = null, dErr = "";
  try {
    dres = await M.send(Object.assign({}, sendPayload, { tutor: ghost, ref: "EK-TEST-02" }));
  } catch (e) { dErr = e.message; }
  check("degraded: missing tutor address RESOLVES (sheet row + student receipt)",
    !!dres && dres.ok === true, dErr);
  check("degraded: exactly one post, addressed to the STUDENT only",
    POSTED.length === 1 && String(POSTED[0].parsed.to || "").toLowerCase() === "priya@example.com",
    JSON.stringify(POSTED.map((p) => p.parsed.to)));
  check("degraded: owner inbox never a recipient",
    POSTED.every((p) => String(p.parsed.to || "").toLowerCase() !== "ekgurulearning@gmail.com"),
    JSON.stringify(POSTED.map((p) => p.parsed.to)));
  check("degraded: tutorEmailStatus TUTOR_EMAIL_UNAVAILABLE + flag set",
    !!dres && dres.tutorEmailStatus === "TUTOR_EMAIL_UNAVAILABLE" && dres.tutorEmailUnavailable === true,
    JSON.stringify(dres && { s: dres.tutorEmailStatus, f: dres.tutorEmailUnavailable }));
  check("degraded: emailStates tutor=TUTOR_EMAIL_UNAVAILABLE, student=ACCEPTED",
    !!dres && dres.emailStates.tutor === "TUTOR_EMAIL_UNAVAILABLE" && dres.emailStates.student === "ACCEPTED",
    JSON.stringify(dres && dres.emailStates));
  check("degraded: student post stamped booking_student_pending",
    byType("booking_student_pending").length === 1, "got " + byType("booking_student_pending").length);
  check("degraded: student receipt never says confirmed",
    POSTED.length === 1 && !/booking is confirmed/i.test(POSTED[0].parsed.html || "") &&
    !/booking is confirmed/i.test(POSTED[0].parsed.subject || ""),
    POSTED.length ? POSTED[0].parsed.subject : "no post");
  check("degraded: student idempotencyKey = entity|pending-template|recipient",
    POSTED.length === 1 &&
    POSTED[0].parsed.idempotencyKey === "EK-TEST-02|booking_student_pending|priya@example.com",
    JSON.stringify(POSTED.length ? POSTED[0].parsed.idempotencyKey : null));

  /* ---- degradedBooking:false restores the old fail-closed block ---- */
  window.EKGURU_SITE.mail.degradedBooking = false;
  POSTED.length = 0;
  let missingAddressRejected = false;
  try {
    await M.send(Object.assign({}, sendPayload, { tutor: ghost, ref: "EK-TEST-03" }));
  } catch (e) { missingAddressRejected = /tutor.*address/i.test(e.message); }
  check("flag-off: missing tutor address fails closed; nothing posted",
    missingAddressRejected && POSTED.length === 0, JSON.stringify(POSTED));
  window.EKGURU_SITE.mail.degradedBooking = true;

  /* =========================== 6. contact() =========================== */
  POSTED.length = 0;
  let cres;
  try {
    cres = await M.contact({
      name: "Aarav", email: "aarav@example.com", topic: "General",
      subject: "Question about lessons",
      message: "Do you teach absolute beginners?",
      pageUrl: "https://ekguru.shop/contact/"
    });
  } catch (e) {
    check("contact() resolves", false, e.message);
    cres = null;
  }
  if (cres) {
    check("contact() resolves", !!cres.ok);
    const vis = byType("contact_submitter_confirmation");
    check("visitor ack stamped contact_submitter_confirmation", vis.length === 1, "got " + vis.length);
    const intl = byType("contact_internal_record").concat(
      internalRows().filter((p) => p.parsed["Name"] === "Aarav")
    );
    check("internal contact stamped contact_internal_record", intl.length >= 1, "got " + intl.length);
    if (vis[0]) {
      check("visitor ack recipient = visitor email", vis[0].parsed.to === "aarav@example.com");
      check("visitor ack replyTo = support (not a bounce-back to self)",
        (vis[0].parsed.replyTo || "").toLowerCase() === "ekgurulearning@gmail.com");
      check("visitor ack idempotencyKey = entity|template|recipient",
        /\|contact_submitter_confirmation\|aarav@example\.com$/i.test(vis[0].parsed.idempotencyKey || ""),
        JSON.stringify(vis[0].parsed.idempotencyKey));
    }
    if (intl[0]) {
      check("internal contact replyTo = visitor email",
        (intl[0].parsed.email || intl[0].parsed.replyTo || "").toLowerCase() === "aarav@example.com");
      check("internal contact not via FormSubmit",
        !/formsubmit\.co/i.test(intl[0].url), intl[0].url.slice(0, 80));
    }
  }

  /* =========================== 7. compose() =========================== */
  POSTED.length = 0;
  let ores;
  try {
    ores = await M.compose({
      to: "student@example.com", subject: "Your lesson time is confirmed",
      message: "Your trial lesson with Tara is confirmed. See you then!"
    });
  } catch (e) {
    check("compose() resolves", false, e.message);
    ores = null;
  }
  if (ores) {
    check("compose() resolves", !!ores.ok);
    const outbound = byType("ADMIN_CONTACT_OUTBOUND");
    check("outbound stamped ADMIN_CONTACT_OUTBOUND", outbound.length === 1, "got " + outbound.length);
    const intl = byType("ADMIN_CONTACT_INTERNAL_COPY").concat(
      internalRows().filter((p) => p.parsed["Message Sent"])
    );
    check("admin internal copy sent to own inbox", intl.length >= 1, "got " + intl.length);
    check("compose returns a conversation ref", /^ADMIN-/.test(ores.ref || ""), ores.ref);
    check("compose returns the internal copy result", !!ores.internalCopy);
    if (outbound[0]) {
      check("outbound idempotencyKey = entity|template|recipient",
        /\|ADMIN_CONTACT_OUTBOUND\|student@example\.com$/i.test(outbound[0].parsed.idempotencyKey || ""),
        JSON.stringify(outbound[0].parsed.idempotencyKey));
      check("outbound replyTo = support",
        (outbound[0].parsed.replyTo || "").toLowerCase() === "ekgurulearning@gmail.com");
    }
    if (intl[0]) {
      check("admin internal copy carries recipient + message",
        JSON.stringify(intl[0].parsed).toLowerCase().indexOf("student@example.com") > -1 &&
        /confirmed/i.test(JSON.stringify(intl[0].parsed)),
        JSON.stringify(intl[0].parsed).slice(0, 180));
    }
  }

  /* =========================== 8. send-test =========================== */
  POSTED.length = 0;
  try {
    const t = await M.testSend("booking_student_confirmation", "EkGuruLearning@gmail.com",
      E.FIXTURES.bookingStudent);
    check("testSend to controlled inbox resolves", !!t.ok && t.state === "ACCEPTED", JSON.stringify(t));
    check("testSend subject prefixed [TEST]", /^\[TEST\]/i.test(t.subject || ""), t.subject);
  } catch (e) {
    check("testSend to controlled inbox resolves", false, e.message);
  }
  try {
    await M.testSend("booking_student_confirmation", "stranger@example.com", E.FIXTURES.bookingStudent);
    check("testSend REFUSES a non-controlled address", false, "should have rejected");
  } catch (e) {
    check("testSend REFUSES a non-controlled address", /control/i.test(e.message), e.message);
  }
  const beforeOwnerPolicyTest = POSTED.length;
  try {
    await M.testSend("booking_internal_record", "EkGuruLearning@gmail.com", E.FIXTURES.bookingInternal);
    check("testSend refuses booking owner copy before relay", false, "should have rejected");
  } catch (e) {
    check("testSend refuses booking owner copy before relay",
      /disabled by policy|private sheet/i.test(e.message) && POSTED.length === beforeOwnerPolicyTest,
      e.message);
  }

  console.log("\n" + (failures === 0 ? "ALL EMAIL-SYSTEM TESTS PASSED" : failures + " FAILURE(S)"));
  process.exit(failures === 0 ? 0 : 1);
})();

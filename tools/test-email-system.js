#!/usr/bin/env node
/* =========================================================
   EkGuru — EMAIL SYSTEM TESTS  (v101 — SIMPLE ROLE TEMPLATES)
   ---------------------------------------------------------
   Loads js/email-templates.js + js/mailer.js against a minimal
   browser shim and verifies the EMAIL RESET contract:

     1. seven message types render (by template key AND by the
        contractual relay type name);
     2. the registry rejects unknown / missing / undeclared vars
        and raw {placeholders};
     3. user values are HTML-escaped (no raw <script> survives);
     4. role-language QA (§27-H) — a tutor mail must not read
        like a student mail, internal wording never leaks;
     5. mailer.send() / mailer.contact() / mailer.compose()
        render the SIMPLE template at send time, stamp
        type / html / text / idempotencyKey (entityId:type) onto
        the Apps Script payload, and route internal copies via the
        internal high-capacity relay;
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
    copyToSite: true,
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
const TYPES = ["CONTACT_VISITOR_CONFIRMATION", "CONTACT_EKGURU_NOTIFICATION",
  "BOOKING_STUDENT_CONFIRMATION", "BOOKING_TUTOR_NOTIFICATION",
  "BOOKING_EKGURU_NOTIFICATION", "ADMIN_CONTACT_OUTBOUND", "ADMIN_CONTACT_INTERNAL_COPY"];
check("WHITELIST = seven message types",
  TYPES.every((t) => (E.WHITELIST || []).indexOf(t) > -1) && E.WHITELIST.length === 7,
  JSON.stringify(E.WHITELIST));

/* =========================== 2. render =========================== */
const KEY2TYPE = {
  contactVisitor: "CONTACT_VISITOR_CONFIRMATION",
  contactInternal: "CONTACT_EKGURU_NOTIFICATION",
  bookingStudent: "BOOKING_STUDENT_CONFIRMATION",
  bookingTutor: "BOOKING_TUTOR_NOTIFICATION",
  bookingInternal: "BOOKING_EKGURU_NOTIFICATION",
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
check("missing var rejected",
  E.render("bookingStudent", { studentName: "X" }).ok === false);
check("undeclared var rejected",
  E.render("bookingStudent", Object.assign({}, E.FIXTURES.bookingStudent, { extraVar: "x" })).ok === false);

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
    const tutor = byType("BOOKING_TUTOR_NOTIFICATION");
    const student = byType("BOOKING_STUDENT_CONFIRMATION");
    check("tutor job stamped BOOKING_TUTOR_NOTIFICATION", tutor.length === 1, "got " + tutor.length);
    check("student job stamped BOOKING_STUDENT_CONFIRMATION", student.length === 1, "got " + student.length);
    check("internal record goes via the internal route (rows, not Apps Script)",
      internalRows().length === 1, "got " + internalRows().length);
    if (tutor[0]) {
      check("tutor payload has html + text", !!tutor[0].parsed.html && !!tutor[0].parsed.text);
      check("tutor idempotencyKey = entityId:type",
        tutor[0].parsed.idempotencyKey === "EK-TEST-01:BOOKING_TUTOR_NOTIFICATION",
        JSON.stringify(tutor[0].parsed.idempotencyKey));
      check("tutor subject is the SIMPLE tutor subject",
        /congratulations — you have a new booking request/i.test(tutor[0].parsed.subject || ""),
        tutor[0].parsed.subject);
      check("tutor html rendered by template", /you have received a new booking request/i.test(tutor[0].parsed.html));
      check("tutor payload recipient = tutor email", tutor[0].parsed.to === "tara@example.com");
      check("tutor copy replyTo = student (supported direct-response)",
        (tutor[0].parsed.replyTo || "").toLowerCase() === "priya@example.com");
    }
    if (student[0]) {
      check("student recipient = student email", student[0].parsed.to === "priya@example.com");
      check("student html is the STUDENT template (not tutor's)",
        /your booking request has been received/i.test(student[0].parsed.html) &&
        !/you have received a new booking request/i.test(student[0].parsed.html));
      check("student html does not expose tutor inbox",
        !/tara@example\.com/i.test(student[0].parsed.html));
      check("student idempotencyKey = entityId:type",
        student[0].parsed.idempotencyKey === "EK-TEST-01:BOOKING_STUDENT_CONFIRMATION");
    }
    const rec = internalRows()[0];
    if (rec) {
      check("internal record via the free internal relay (FormSubmit endpoint)",
        /formsubmit\.co\/ajax\//i.test(rec.url), rec.url.slice(0, 60));
      check("internal record carries delivery state row",
        /Student: sending/.test(rec.parsed["Email Delivery"] || "") &&
        /Tutor: sending/.test(rec.parsed["Email Delivery"] || ""));
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

  POSTED.length = 0;
  const ghost = { id: "newtutor", name: "New Tutor", lessonLength: "50 min" };
  try {
    res = await M.send(Object.assign({}, sendPayload, { tutor: ghost, ref: "EK-TEST-02" }));
  } catch (e) {
    check("send() resolves (tutor WITHOUT email)", false, e.message);
    res = null;
  }
  if (res) {
    check("send() resolves (tutor WITHOUT email)", !!res.ok, JSON.stringify(res));
    check("NO tutor job when tutor email unavailable",
      byType("BOOKING_TUTOR_NOTIFICATION").length === 0,
      "got " + byType("BOOKING_TUTOR_NOTIFICATION").length);
    check("student still gets their receipt",
      byType("BOOKING_STUDENT_CONFIRMATION").length === 1);
    const rec = internalRows()[0];
    check("internal record still written", !!rec);
    if (rec) {
      check("internal record marks tutor email state honestly",
        rec.parsed["Tutor Email"] === "TUTOR_EMAIL_UNAVAILABLE");
    }
  }

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
    const vis = byType("CONTACT_VISITOR_CONFIRMATION");
    check("visitor ack stamped CONTACT_VISITOR_CONFIRMATION", vis.length === 1, "got " + vis.length);
    const intl = internalRows().filter((p) => p.parsed["Name"] === "Aarav");
    check("internal contact goes via the internal route", intl.length === 1, "got " + intl.length);
    if (vis[0]) {
      check("visitor ack recipient = visitor email", vis[0].parsed.to === "aarav@example.com");
      check("visitor ack replyTo = support (not a bounce-back to self)",
        (vis[0].parsed.replyTo || "").toLowerCase() === "ekgurulearning@gmail.com");
      check("visitor ack idempotencyKey = entityId:type",
        /^C-[A-Z0-9]+:CONTACT_VISITOR_CONFIRMATION$/.test(vis[0].parsed.idempotencyKey || ""),
        JSON.stringify(vis[0].parsed.idempotencyKey));
    }
    if (intl[0]) {
      check("internal contact replyTo = visitor email",
        (intl[0].parsed.email || "").toLowerCase() === "aarav@example.com");
      check("internal contact via the free internal relay (FormSubmit endpoint)",
        /formsubmit\.co\/ajax\//i.test(intl[0].url), intl[0].url.slice(0, 60));
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
    const intl = internalRows().filter((p) => p.parsed["Message Sent"]);
    check("admin internal copy sent to own inbox", intl.length === 1, "got " + intl.length);
    check("compose returns a conversation ref", /^ADMIN-/.test(ores.ref || ""), ores.ref);
    check("compose returns the internal copy result", !!ores.internalCopy);
    if (outbound[0]) {
      check("outbound idempotencyKey = entityId:type",
        /^ADMIN-[A-Z0-9]+:ADMIN_CONTACT_OUTBOUND$/.test(outbound[0].parsed.idempotencyKey || ""),
        JSON.stringify(outbound[0].parsed.idempotencyKey));
      check("outbound replyTo = support",
        (outbound[0].parsed.replyTo || "").toLowerCase() === "ekgurulearning@gmail.com");
    }
    if (intl[0]) {
      check("admin internal copy carries recipient + message",
        intl[0].parsed["Recipient Email"] === "student@example.com" &&
        /confirmed/.test(intl[0].parsed["Message Sent"]));
    }
  }

  /* =========================== 8. send-test =========================== */
  POSTED.length = 0;
  try {
    const t = await M.testSend("BOOKING_STUDENT_CONFIRMATION", "EkGuruLearning@gmail.com",
      E.FIXTURES.bookingStudent);
    check("testSend to controlled inbox resolves", !!t.ok && t.state === "ACCEPTED", JSON.stringify(t));
    check("testSend subject prefixed [TEST]", /^\[TEST\]/i.test(t.subject || ""), t.subject);
  } catch (e) {
    check("testSend to controlled inbox resolves", false, e.message);
  }
  try {
    await M.testSend("BOOKING_STUDENT_CONFIRMATION", "stranger@example.com", E.FIXTURES.bookingStudent);
    check("testSend REFUSES a non-controlled address", false, "should have rejected");
  } catch (e) {
    check("testSend REFUSES a non-controlled address", /control/i.test(e.message), e.message);
  }

  console.log("\n" + (failures === 0 ? "ALL EMAIL-SYSTEM TESTS PASSED" : failures + " FAILURE(S)"));
  process.exit(failures === 0 ? 0 : 1);
})();

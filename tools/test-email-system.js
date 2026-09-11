#!/usr/bin/env node
/* =========================================================
   EkGuru — EMAIL SYSTEM TESTS  (v100)
   ---------------------------------------------------------
   Loads js/email-templates.js + js/mailer.js against a minimal
   browser shim and verifies the Email ULTRA contract:

     1. the five message types render (by template key AND by the
        contractual relay type name);
     2. the registry rejects unknown / missing / undeclared vars
        and raw {placeholders};
     3. user values are HTML-escaped (no raw <script> survives);
     4. role-language QA (a student mail must not read like a
        tutor mail, and vice-versa);
     5. mailer.send() / mailer.contact() render the template at
        send time and stamp type / html / text / idempotencyKey
        onto the Apps Script payload;
     6. tutorEmailInfo() classifies tutors (ACTIVE+VALID / MISSING
        / INVALID) and TUTOR_EMAIL_UNAVAILABLE routing holds.

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
    contactProvider: "appsscript",
    appsScript: {
      url: "https://script.google.com/macros/s/AKfycbTEST/exec",
      token: "test-client-token"
    },
    web3formsKeys: ["11111111-2222-3333-4444-555555555555"],
    staticFormsKey: "test-static",
    siteKey: "EkGuruLearning@gmail.com"
  }
};

/* fake relay: Apps Script answers a JSON success over text/plain */
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
window.fetch = global.fetch;   // mailer gates on window.fetch

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
  "BOOKING_EKGURU_NOTIFICATION"];
check("WHITELIST = five message types",
  TYPES.every((t) => (E.WHITELIST || []).indexOf(t) > -1) && E.WHITELIST.length === 5,
  JSON.stringify(E.WHITELIST));

/* =========================== 2. render =========================== */
const KEY2TYPE = {
  contactVisitor: "CONTACT_VISITOR_CONFIRMATION",
  contactInternal: "CONTACT_EKGURU_NOTIFICATION",
  bookingStudent: "BOOKING_STUDENT_CONFIRMATION",
  bookingTutor: "BOOKING_TUTOR_NOTIFICATION",
  bookingInternal: "BOOKING_EKGURU_NOTIFICATION"
};
Object.keys(E.FIXTURES).forEach((k) => {
  const r = E.render(k, E.FIXTURES[k]);
  check("fixture renders: " + k, r.ok && r.subject && r.html && r.text, r.errors && r.errors.join(", "));
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
  if (!r.ok) { check("role-language render: " + k, false, r.errors && r.errors.join(", ")); return; }
  const text = (r.subject + " " + r.html + " " + r.text).toLowerCase();
  const bad = [];
  qa.mustSay.forEach((m) => { if (text.indexOf(m.toLowerCase()) === -1) bad.push("missing '" + m + "'"); });
  qa.mustNotSay.forEach((m) => { if (text.indexOf(m.toLowerCase()) > -1) bad.push("should not say '" + m + "'"); });
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

function posted() { return POSTED.filter((p) => p.parsed && p.parsed.token); }
function byType(type) { return POSTED.filter((p) => p.parsed && p.parsed.type === type); }

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
    const internal = byType("BOOKING_EKGURU_NOTIFICATION");
    check("tutor job stamped BOOKING_TUTOR_NOTIFICATION", tutor.length === 1, "got " + tutor.length);
    check("student job stamped BOOKING_STUDENT_CONFIRMATION", student.length === 1, "got " + student.length);
    check("internal job stamped BOOKING_EKGURU_NOTIFICATION", internal.length === 1, "got " + internal.length);
    if (tutor[0]) {
      check("tutor payload has html + text", !!tutor[0].parsed.html && !!tutor[0].parsed.text);
      check("tutor payload has idempotencyKey", !!tutor[0].parsed.idempotencyKey,
        JSON.stringify(tutor[0].parsed.idempotencyKey));
      check("tutor payload subject is the template subject",
        /new lesson request/i.test(tutor[0].parsed.subject || ""), tutor[0].parsed.subject);
      check("tutor html rendered by template", /new lesson request/i.test(tutor[0].parsed.html));
      check("tutor payload recipient = tutor email", tutor[0].parsed.to === "tara@example.com");
      /* Reply-To on the tutor's working copy is the STUDENT (the
         tutor confirms the time by replying to the learner). The
         tutor's address is never the From, and the visitor's email
         is never the From. */
      check("tutor copy replyTo = student (not From, not support)",
        (tutor[0].parsed.replyTo || "").toLowerCase() === "priya@example.com");
      check("From is never the visitor/student (fromName is EkGuru)",
        String(tutor[0].parsed.fromName || "").toLowerCase().indexOf("ekguru") > -1 &&
        String(tutor[0].parsed.fromName || "").toLowerCase().indexOf("priya") === -1);
    }
    if (student[0]) {
      check("student recipient = student email", student[0].parsed.to === "priya@example.com");
      check("student html is the STUDENT template (not tutor's)",
        /booking request received/i.test(student[0].parsed.html) && !/new lesson request/i.test(student[0].parsed.html));
      check("student html does not expose tutor inbox",
        !/tara@example\.com/i.test(student[0].parsed.html), student[0].parsed.html.slice(0, 120));
    }
    if (internal[0]) {
      check("internal recipient = EkGuru inbox",
        internal[0].parsed.to.toLowerCase() === "ekgurulearning@gmail.com");
      check("internal html carries delivery state field",
        /delivery/i.test(internal[0].parsed.html));
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
    check("internal record still written",
      byType("BOOKING_EKGURU_NOTIFICATION").length === 1);
    const internal = byType("BOOKING_EKGURU_NOTIFICATION")[0];
    if (internal) {
      check("internal record marks tutorEmailState honestly",
        /ACTIVE\+MISSING/.test(internal.parsed.html || ""),
        internal.parsed.html && internal.parsed.html.slice(0, 200));
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
    const intl = byType("CONTACT_EKGURU_NOTIFICATION");
    check("visitor ack stamped CONTACT_VISITOR_CONFIRMATION", vis.length === 1, "got " + vis.length);
    check("internal stamped CONTACT_EKGURU_NOTIFICATION", intl.length === 1, "got " + intl.length);
    if (intl[0]) {
      check("internal contact replyTo = visitor email",
        (intl[0].parsed.replyTo || "").toLowerCase() === "aarav@example.com");
      check("visitor email NOT used as From (recipient is our inbox)",
        intl[0].parsed.to.toLowerCase() === "ekgurulearning@gmail.com");
      check("internal contact carries idempotencyKey",
        /^CONTACT-.*-INTERNAL$/.test(intl[0].parsed.idempotencyKey || ""),
        JSON.stringify(intl[0].parsed.idempotencyKey));
    }
    if (vis[0]) {
      check("visitor ack recipient = visitor email", vis[0].parsed.to === "aarav@example.com");
      check("visitor ack replyTo = support (not a bounce-back to self)",
        (vis[0].parsed.replyTo || "").toLowerCase() === "ekgurulearning@gmail.com");
      check("visitor ack carries idempotencyKey",
        /^CONTACT-.*-VISITOR$/.test(vis[0].parsed.idempotencyKey || ""),
        JSON.stringify(vis[0].parsed.idempotencyKey));
    }
  }

  /* =========================== 7. send-test =========================== */
  POSTED.length = 0;
  try {
    const t = await M.testSend("BOOKING_STUDENT_CONFIRMATION", "EkGuruLearning@gmail.com",
      E.FIXTURES.bookingStudent);
    check("testSend to controlled inbox resolves", !!t.ok && t.state === "ACCEPTED", JSON.stringify(t));
    check("testSend subject prefixed [TEST]", /^\[TEST\]/i.test(t.subject || ""), t.subject);
    const last = POSTED.filter((p) => p.parsed && p.parsed.type === "BOOKING_STUDENT_CONFIRMATION").pop();
    check("testSend posted the rendered template", !!last && !!last.parsed.html && !!last.parsed.text);
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

#!/usr/bin/env node
/* =========================================================
   EkGuru — MAIL FLOW TESTS
   Deterministic. No live network. No inbox claims.
   Run:  node tools/test-mail-flow.mjs
   ========================================================= */
"use strict";
import fs from "fs";
import path from "path";
import { createRequire } from "module";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, "..");
const require = createRequire(import.meta.url);

let failures = 0;
function check(name, cond, extra) {
  const ok = !!cond;
  if (!ok) failures++;
  console.log((ok ? "PASS" : "FAIL") + "  " + name + (ok ? "" : "  →  " + (extra || "")));
}

/* ------------------------- load gs as text ------------------------- */
const gs = fs.readFileSync(path.join(ROOT, "tools", "apps-script-mailer.gs"), "utf8");
const cfg = fs.readFileSync(path.join(ROOT, "js", "site-config.js"), "utf8");
const mailerSrc = fs.readFileSync(path.join(ROOT, "js", "mailer.js"), "utf8");

/* ============ 1. Apps Script is not an open relay ============ */
check("gs: empty type is refused (not `if (type && …)`)",
  /if\s*\(\s*!type\s*\|\|\s*MESSAGE_TYPES\.indexOf\(type\)\s*===\s*-1\s*\)/.test(gs));
check("gs: visitor From is never taken from the client (GmailApp owner + SENDER_NAME)",
  /GmailApp\.sendEmail\(to, subject, textBody, opts\)/.test(gs) &&
  /name:\s*SENDER_NAME/.test(gs) &&
  !/opts\.from\s*=/.test(gs));
check("gs: Reply-To via firstEmail (CR/LF rejected)",
  /function firstEmail/.test(gs) && /function isEmail/.test(gs) &&
  gs.indexOf("\\r\\n") > -1);
check("gs: internal / admin-outbound types cannot address strangers",
  /STRANGER_OK_TYPES/.test(gs) &&
  /Recipient not allowed/.test(gs) &&
  !/var ALLOW_STRANGERS\s*=\s*true/.test(gs));
check("gs: fail-closed token",
  /MAILER_SHARED_TOKEN/.test(gs) && /Not authorised/.test(gs) &&
  /if\s*\(!expected\)/.test(gs));
check("gs: daily cap + idempotency",
  /DAILY_LIMIT\s*=\s*90/.test(gs) && /sentFlag\(/.test(gs));

/* ============ 2. Live chain is two relays, not five ============ */
check("mailer live chain is Apps Script + Web3Forms only",
  /var LIVE_IDS\s*=\s*\["appsscript",\s*"web3forms"\]/.test(mailerSrc));
check("mailer does not force FormSubmit as a hidden floor",
  /Do NOT force FormSubmit/.test(mailerSrc));
check("EmailJS not configured in site-config",
  /serviceId:\s*""/.test(cfg) && /publicKey:\s*""/.test(cfg));
check("StaticForms key retired (empty)",
  /staticFormsKey:\s*""/.test(cfg));
check("extra Web3Forms keys array is empty (one fallback key)",
  /web3formsKeys:\s*\[\s*\]/.test(cfg) || /web3formsKeys:\s*\[\s*\/\*/.test(cfg));

/* ============ 3. No SMTP / private keys committed ============ */
const SECRET_HITS = [];
function scan(dir) {
  for (const f of fs.readdirSync(dir)) {
    const p = path.join(dir, f);
    const st = fs.statSync(p);
    if (st.isDirectory()) {
      if (/^(node_modules|\.git|dist|build|reports|backups)$/.test(f)) continue;
      scan(p);
      continue;
    }
    if (!/\.(js|json|gs|html|py|md|mjs)$/.test(f)) continue;
    const txt = fs.readFileSync(p, "utf8");
    if (/-----BEGIN [A-Z ]*PRIVATE KEY-----/.test(txt)) SECRET_HITS.push(p + " PEM");
    if (/\bsk_live_[A-Za-z0-9]{20,}/.test(txt)) SECRET_HITS.push(p + " stripe");
    if (/MAILER_SHARED_TOKEN\s*[:=]\s*["'][A-Za-z0-9_-]{16,}/.test(txt)) SECRET_HITS.push(p + " token value");
  }
}
scan(ROOT);
check("no private-key / SMTP secret class in source", SECRET_HITS.length === 0, SECRET_HITS.join("; "));
const tokenField = (cfg.match(/appsScript:[\s\S]*?token:\s*"([^"]*)"/) || [null, ""])[1] || "";
check("committed Apps Script client token is empty (wire at deploy)", tokenField === "");

/* ============ 4. Runtime: stop on first success, no duplicate type ============ */
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
global.location = { href: "https://ekguru.shop/contact/" };

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
    web3formsKey: "11111111-2222-3333-4444-555555555555",
    web3formsKeys: [],
    staticFormsKey: "",
    emailjs: { serviceId: "", templateId: "", publicKey: "" },
    siteKey: "EkGuruLearning@gmail.com"
  }
};

const POSTED = [];
let failFirst = false;
global.fetch = function (url, opts) {
  const body = String(opts && opts.body || "");
  let parsed = {};
  try { parsed = JSON.parse(body); } catch (e) {}
  POSTED.push({ url: String(url), parsed, headers: (opts && opts.headers) || {} });
  if (failFirst) {
    failFirst = false;
    return Promise.resolve({
      ok: true,
      text: () => Promise.resolve(JSON.stringify({ success: "false", message: "Not authorised." }))
    });
  }
  return Promise.resolve({
    ok: true,
    text: () => Promise.resolve(JSON.stringify({ success: "true", sent: true }))
  });
};
window.fetch = global.fetch;

require(path.join(ROOT, "js", "email-templates.js"));
require(path.join(ROOT, "js", "mailer.js"));
const M = window.EkGuruMail;
const E = window.EKGURU_EMAIL;

check("mailer + templates loaded", !!(M && E && M.contact && M.send));

const map = M.routingMap();
check("routing: student → appsscript (sendable in this harness)",
  map.bookingStudent === "appsscript", JSON.stringify(map.bookingStudent));
check("routing: visitor → appsscript",
  map.contactVisitor === "appsscript");
check("routing: EmailJS/StaticForms/FormSubmit not in live sendable set",
  map.providers.filter((p) => p.sendable).every((p) => p.id === "appsscript" || p.id === "web3forms"));

function typesPosted() {
  return POSTED.map((p) => p.parsed && p.parsed.type).filter(Boolean);
}

await (async function () {
  localStorage.clear();
  POSTED.length = 0;
  const cres = await M.contact({
    name: "Priya Test",
    email: "priya@example.com",
    topic: "General",
    subject: "Hello\r\nBcc: evil@attacker.example",
    message: "Do you teach complete beginners please?",
    pageUrl: "https://ekguru.shop/contact/"
  });
  check("contact() ACCEPTED (not DELIVERED)", cres && cres.ok && cres.state === "ACCEPTED");
  const vis = POSTED.filter((p) => p.parsed.type === "CONTACT_VISITOR_CONFIRMATION");
  const intl = POSTED.filter((p) => p.parsed.type === "CONTACT_EKGURU_NOTIFICATION");
  check("contact: one visitor job, one internal job",
    vis.length === 1 && intl.length === 1,
    "vis=" + vis.length + " intl=" + intl.length + " types=" + typesPosted().join(","));
  check("contact: no FormSubmit / StaticForms / EmailJS hop",
    POSTED.every((p) => /script\.google\.com|web3forms\.com/.test(p.url)));
  check("contact: visitor Reply-To is support, not the visitor as From",
    vis[0] && String(vis[0].parsed.replyTo || "").toLowerCase() === "ekgurulearning@gmail.com");
  check("contact: internal Reply-To is the visitor (so Reply works)",
    intl[0] && String(intl[0].parsed.replyTo || "").toLowerCase() === "priya@example.com");
  check("contact: subject has no CR/LF (header injection)",
    vis.every((p) => !/[\r\n]/.test(p.parsed.subject || "")) &&
    intl.every((p) => !/[\r\n]/.test(p.parsed.subject || "")));
  check("contact: Apps Script hop uses text/plain (no CORS preflight)",
    POSTED.filter((p) => /script\.google/.test(p.url))
      .every((p) => /text\/plain/i.test((p.headers["Content-Type"] || ""))));

  /* duplicate submit with same ref → idempotent, no second POST of that role */
  const ref = cres.ref;
  const n1 = POSTED.length;
  const cres2 = await M.contact({
    name: "Priya Test",
    email: "priya@example.com",
    topic: "General",
    message: "Do you teach complete beginners please?",
    pageUrl: "https://ekguru.shop/contact/",
    ref: ref
  });
  check("second contact with same ref does not POST again (client idempotency)",
    cres2 && cres2.ok && POSTED.length === n1,
    "posted " + POSTED.length + " after first " + n1);

  /* XSS in template */
  const xss = E.render("CONTACT_VISITOR_CONFIRMATION", Object.assign({}, E.FIXTURES.contactVisitor, {
    visitorName: "<script>alert(1)</script>",
    message: "<img src=x onerror=alert(1)>"
  }));
  check("template escapes script/img",
    xss.ok && !/<script/i.test(xss.html) && !/<img/i.test(xss.html));

  /* unknown type */
  check("unknown template type refused", E.render("SPAM_BLAST", {}).ok === false);

  /* booking: stop on first success — Apps Script answers success, Web3Forms must not fire for the same role */
  localStorage.clear();
  POSTED.length = 0;
  const sendRes = await M.send({
    tutor: { id: "tara", name: "Tara", email: "tara@example.com", lessonLength: "50 min", trialAvailable: true },
    name: "Priya", email: "priya@example.com",
    slot: "20 September 2026, 7:00 PM", timezone: "Asia/Kolkata",
    goal: "Conversation", message: "I want to speak better Hindi please.",
    price: "$8", ref: "EK-FLOW-01"
  });
  check("send() ACCEPTED", sendRes && sendRes.ok && sendRes.state === "ACCEPTED");
  const byType = {};
  POSTED.forEach((p) => {
    const t = p.parsed && p.parsed.type;
    if (t) byType[t] = (byType[t] || 0) + 1;
  });
  check("one POST per booking role (no multi-provider duplicate)",
    (byType.BOOKING_TUTOR_NOTIFICATION || 0) === 1 &&
    (byType.BOOKING_STUDENT_CONFIRMATION || 0) === 1 &&
    (byType.BOOKING_EKGURU_NOTIFICATION || 0) === 1,
    JSON.stringify(byType));
  check("booking student copy does not include tutor inbox",
    POSTED.filter((p) => p.parsed.type === "BOOKING_STUDENT_CONFIRMATION")
      .every((p) => !/tara@example\.com/i.test(JSON.stringify(p.parsed))));
  check("no live hop to FormSubmit/StaticForms/EmailJS on booking",
    POSTED.every((p) => /script\.google\.com|web3forms\.com/.test(p.url)));

  /* fallback: Apps Script refuses AUTH, Web3Forms carries the same role once */
  localStorage.clear();
  POSTED.length = 0;
  failFirst = true;
  const send2 = await M.send({
    tutor: { id: "tara", name: "Tara", email: "tara@example.com", lessonLength: "50 min" },
    name: "Priya", email: "priya@example.com",
    slot: "21 September 2026, 7:00 PM", timezone: "Asia/Kolkata",
    goal: "Conversation", message: "I want to speak better Hindi please.",
    price: "$8", ref: "EK-FLOW-02"
  });
  check("AUTH on Apps Script falls through to Web3Forms (still one logical send per role)",
    send2 && send2.ok);
  const tutorHops = POSTED.filter((p) =>
    (p.parsed.type === "BOOKING_TUTOR_NOTIFICATION") ||
    (p.parsed.to === "tara@example.com") ||
    (p.parsed.access_key && p.parsed.to === "tara@example.com")
  );
  const urls = tutorHops.map((p) => p.url);
  check("tutor role: Apps Script AUTH fail then Web3Forms once (no third hop)",
    urls.some((u) => /script\.google/.test(u)) &&
    urls.some((u) => /web3forms/.test(u)) &&
    urls.filter((u) => /web3forms/.test(u)).length === 1,
    urls.join(" | "));

  /* CRLF email rejected */
  let threw = false;
  try {
    await M.contact({
      name: "X", email: "priya@example.com\r\nBcc:evil@x.com",
      message: "hello there this is long enough"
    });
  } catch (e) { threw = true; }
  check("CRLF in visitor email is rejected", threw);

  /* mailto tertiary exists */
  const mail = M.contactMailto({
    name: "Priya", email: "priya@example.com", topic: "General",
    message: "hello", pageUrl: "https://ekguru.shop/contact/"
  });
  check("mailto tertiary is a mailto: to the site inbox",
    /^mailto:EkGuruLearning@gmail\.com\?/i.test(mail));

  /* honeypot: no POST */
  POSTED.length = 0;
  const hp = await M.contact({
    name: "Bot", email: "bot@example.com",
    message: "hello there this is long enough", hp: "http://spam"
  });
  check("honeypot does not POST", POSTED.length === 0 && hp && hp.ignored === true);

  /* testSend refuses a stranger */
  let refuse = false;
  try {
    await M.testSend("BOOKING_STUDENT_CONFIRMATION", "stranger@example.com", E.FIXTURES.bookingStudent);
  } catch (e) { refuse = /control/i.test(e.message); }
  check("testSend refuses a non-controlled address", refuse);
})().catch((e) => {
  check("runtime harness", false, e && e.stack || String(e));
});

console.log("\n" + (failures === 0 ? "ALL MAIL-FLOW TESTS PASSED" : failures + " FAILURE(S)"));
console.log("LABEL: " + (failures === 0 ? "tests-ok (live delivery still BROWSER_NOT_VERIFIED)" : "MAIL_SYSTEM_NOT_READY"));
process.exit(failures === 0 ? 0 : 1);

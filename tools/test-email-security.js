#!/usr/bin/env node
/* =========================================================
   EkGuru — EMAIL SECURITY TESTS  (v100)
   ---------------------------------------------------------
   Exercises the client + template layer against the §49
   security list, and statically verifies the Apps Script
   relay's defences:

     · header injection (newline in a name/date)
     · XSS (script/HTML in a user value)
     · unknown message type
     · replay / idempotency presence (server + client)
     · oversize payload limits (relay caps)
     · open-relay defence (whitelist + forced From + token)
     · PII / secret leakage (no token value in source; the
       student copy never carries the tutor's address)

   Run:  node tools/test-email-security.js
   ========================================================= */
"use strict";
const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");

let failures = 0;
function check(name, cond, extra) {
  const ok = !!cond;
  if (!ok) failures++;
  console.log((ok ? "PASS" : "FAIL") + "  " + name + (ok ? "" : "  →  " + (extra || "")));
}

/* ------------------------- load templates ------------------------- */
global.window = {};
require(path.join(ROOT, "js", "email-templates.js"));
const E = window.EKGURU_EMAIL;

/* ============ 1. header injection ============ */
const inject = Object.assign({}, E.FIXTURES.bookingTutor, {
  studentName: "Alice\r\nBcc: evil@attacker.example",
  date: "20 Sept 2026\r\nFrom: attacker@example.com"
});
const inj = E.render("bookingTutor", inject);
/* Header injection needs a CR/LF to terminate a header line. The
   subject must therefore be a single line — the injected value may
   still be visible as text, but it can never become a header. */
check("subject is a single line (no CR/LF)", inj.ok && !/[\r\n]/.test(inj.subject), JSON.stringify(inj.subject));
check("subject capped at 150 chars", inj.ok && inj.subject.length <= 150, String(inj.subject.length));
check("no <script>/<img> survives in html", inj.ok && !/<script/i.test(inj.html) && !/<img/i.test(inj.html));

/* ============ 2. XSS ============ */
const xss = Object.assign({}, E.FIXTURES.bookingStudent, {
  studentName: "<script>alert(document.cookie)</script>",
  studentRequirement: "<img src=x onerror=alert(1)>"
});
const xr = E.render("bookingStudent", xss);
check("script tag escaped in html", xr.ok && !/<script/i.test(xr.html) && /&lt;script/i.test(xr.html));
check("img onerror escaped", xr.ok && !/<img/i.test(xr.html) && /&lt;img/i.test(xr.html));

/* ============ 3. unknown type ============ */
check("unknown type refused", E.render("ADMIN_ANNOUNCE_BULK", {}).ok === false);
check("every whitelisted type renders", E.WHITELIST.every((t) => {
  const map = {
    "CONTACT_VISITOR_CONFIRMATION": "contactVisitor",
    "CONTACT_EKGURU_NOTIFICATION": "contactInternal",
    "BOOKING_STUDENT_CONFIRMATION": "bookingStudent",
    "BOOKING_TUTOR_NOTIFICATION": "bookingTutor",
    "BOOKING_EKGURU_NOTIFICATION": "bookingInternal",
    "ADMIN_CONTACT_OUTBOUND": "adminOutbound",
    "ADMIN_CONTACT_INTERNAL_COPY": "adminInternalCopy"
  };
  return E.render(t, E.FIXTURES[map[t]]).ok;
}));
check("seven message types, no more", E.WHITELIST.length === 7, E.WHITELIST.join(","));

/* ============ 4. student copy never leaks the tutor's address ============ */
const stu = E.render("bookingStudent", E.FIXTURES.bookingStudent);
const stuEmailVars = E.TEMPLATES.bookingStudent.allowedVars.filter((v) =>
  /email|inbox|address/i.test(v));
check("student template's only email var is the shared support address",
  stuEmailVars.length === 1 && stuEmailVars[0] === "supportEmail",
  stuEmailVars.join(","));
check("student html carries NO email address at all (simple copy — nothing to leak)",
  !/@/.test(stu.html), "leaks an address: " + stu.html.slice(0, 140));
check("student html has no 'provider' / internal wording",
  !/provider|delivery state|internal/i.test(stu.html), stu.html.slice(0, 160));

/* ============ 5. relay static defences ============ */
const gs = fs.readFileSync(path.join(ROOT, "tools", "apps-script-mailer.gs"), "utf8");
check("relay: message-type whitelist", /var MESSAGE_TYPES\s*=\s*\[/.test(gs));
check("relay: fail-closed token", /MAILER_SHARED_TOKEN/.test(gs) && /Not authorised/.test(gs));
check("relay: forced From = owner (never client)", /GmailApp\.sendEmail\(to, subject, textBody, opts\)/.test(gs) && /name:\s*SENDER_NAME/.test(gs));
check("relay: size caps", /MAX_HTML_BYTES\s*=\s*60000/.test(gs) && /MAX_TEXT_BYTES\s*=\s*20000/.test(gs));
check("relay: daily cap", /DAILY_LIMIT\s*=\s*90/.test(gs));
check("relay: server-side idempotency", /sentFlag\(/.test(gs) && /setSentFlag\(/.test(gs) && /idempotencyKey/.test(gs));
check("relay: reply-to via firstEmail (header injection safe)", /function firstEmail/.test(gs));
check("relay: subject single-line sanitised", gs.indexOf("[\\r\\n\\t]") > -1, "no sanitise in .gs");

/* ============ 6. secret / PII leakage scan ============ */
const SECRET_RE = /MAILER_SHARED_TOKEN\s*[:=]\s*["'][A-Za-z0-9_-]{16,}/;
const TOKEN_VALUE_RE = /appsScript:\s*\{[^}]*?token:\s*"[A-Za-z0-9_-]{8,}"/s;
let leaked = [];
function scan(dir) {
  fs.readdirSync(dir).forEach((f) => {
    const p = path.join(dir, f);
    const st = fs.statSync(p);
    if (st.isDirectory()) {
      if (/^(node_modules|\.git|dist|build|reports|backups)$/.test(f)) return;
      return scan(p);
    }
    if (!/\.(js|json|gs|html|py|md)$/.test(f)) return;
    /* test shims deliberately carry placeholder tokens ("test-client-token");
       they are not production code and never ship to the site. */
    if (/^test-/.test(f) && /\/tools\//.test(p)) return;
    const txt = fs.readFileSync(p, "utf8");
    if (SECRET_RE.test(txt)) leaked.push(p + " (token VALUE in source)");
    /* js/site-config.js's mail.appsScript.token is the sanctioned
       deploy-time field (checked separately against the gitignored
       secrets file); a token value anywhere ELSE is a leak. */
    if (!/site-config\.js$/.test(p) && TOKEN_VALUE_RE.test(txt)) {
      leaked.push(p + " (client token value in source)");
    }
  });
}
scan(ROOT);
check("no relay token value committed in source", leaked.length === 0, leaked.join("; "));

/* The client token's ONLY sanctioned home at deploy time is
   mail.appsScript.token in js/site-config.js, filled by wire-token.py
   from the gitignored deploy-secrets.local.json. If a value is present
   it must match that file, and that file must be gitignored. */
const cfg = fs.readFileSync(path.join(ROOT, "js", "site-config.js"), "utf8");
const tokenField = (cfg.match(/token:\s*"([^"]*)"/) || [null, ""])[1] || "";
const secretsPath = path.join(ROOT, "deploy-secrets.local.json");
let secretsToken = "";
if (fs.existsSync(secretsPath)) {
  try { secretsToken = JSON.parse(fs.readFileSync(secretsPath, "utf8")).mailerToken || ""; }
  catch (e) { secretsToken = ""; }
}
const gitignore = fs.existsSync(path.join(ROOT, ".gitignore"))
  ? fs.readFileSync(path.join(ROOT, ".gitignore"), "utf8") : "";
check("deploy-secrets.local.json is gitignored", /deploy-secrets\.local\.json/.test(gitignore));
if (tokenField) {
  check("wired client token matches the gitignored secrets file (deploy-time wiring)",
    tokenField === secretsToken, "site-config token != deploy-secrets.local.json");
} else {
  check("client token empty — not yet wired (wire-token.py pending)", true);
}

console.log("\n" + (failures === 0 ? "ALL EMAIL-SECURITY TESTS PASSED" : failures + " FAILURE(S)"));
process.exit(failures === 0 ? 0 : 1);

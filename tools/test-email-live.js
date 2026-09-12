#!/usr/bin/env node
/* =========================================================
   EkGuru — LIVE relay test against the REAL Apps Script
   deployment, using the SHIPPED mailer code path.

   Loads the real js/site-config.js (token wired from
   deploy-secrets.local.json by tools/wire-token.py), the real
   js/email-templates.js and js/mailer.js, and exercises:

     1. EkGuruMail.testSend() — a controlled [TEST] send to the
        owner inbox through the actual provider chain (Apps
        Script primary). ACCEPTED means the owner's Gmail
        dispatched the message.
     2. Server-side idempotency — the same idempotencyKey POSTed
        twice: first "sent", second "duplicate" (no re-send).

   Run:  node tools/test-email-live.js
   ========================================================= */
"use strict";
const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");

/* browser shim (same shape tools/test-email-system.js uses) */
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
global.location = { href: "https://ekguru.shop/admin.html" };

/* the real config */
require(path.join(ROOT, "js", "site-config.js"));
require(path.join(ROOT, "js", "email-templates.js"));
require(path.join(ROOT, "js", "mailer.js"));

const E = window.EKGURU_EMAIL;
const M = window.EkGuruMail;
const cfg = window.EKGURU_SITE.mail.appsScript || {};

/* REAL fetch with a browser UA (the relay's bot-gate rejects the
   bare Node UA on datacenter IPs). Node fetch follows the 302 to
   the googleusercontent echo endpoint automatically. */
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36";
const nativeFetch = global.fetch;
global.fetch = function (url, opts) {
  opts = opts || {};
  opts.headers = Object.assign({ "User-Agent": UA }, opts.headers || {});
  return nativeFetch(url, opts);
};
window.fetch = global.fetch;

let failures = 0;
function check(name, cond, extra) {
  const ok = !!cond;
  if (!ok) failures++;
  console.log((ok ? "PASS" : "FAIL") + "  " + name + (ok ? "" : "  →  " + (extra || "")));
}

function postRelay(body) {
  const url = cfg.url;
  return global.fetch(url, {
    method: "POST",
    headers: { "Content-Type": "text/plain;charset=utf-8" },
    body: JSON.stringify(body)
  }).then((r) => r.text()).then((t) => { try { return JSON.parse(t); } catch (e) { return { raw: t.slice(0, 120) }; } });
}

(async function () {
  console.log("relay URL:", (cfg.url || "").replace(/\/exec.*/, "/exec"));
  console.log("token wired:", !!cfg.token && String(cfg.token).trim().length > 0);

  /* ---- 1. shipped mailer path (testSend → controlled inbox) ---- */
  const vars = {};
  for (const k in E.FIXTURES.bookingInternal) vars[k] = E.FIXTURES.bookingInternal[k];
  vars.bookingId = "BOOK-TEST-001";
  try {
    const t = await M.testSend("BOOKING_EKGURU_NOTIFICATION", "EkGuruLearning@gmail.com", vars);
    check("mailer.testSend → relay ACCEPTED (real send)", t.ok && t.state === "ACCEPTED", JSON.stringify(t));
    check("testSend subject carries [TEST]", /^\[TEST\]/i.test(t.subject || ""), t.subject);
    check("testSend went via Apps Script", /Apps Script/i.test(t.via || ""), t.via);
  } catch (e) {
    check("mailer.testSend → relay ACCEPTED (real send)", false, e.message);
  }

  /* ---- 2. server-side idempotency (replay) ---- */
  const idem = "LIVE-TEST-" + Date.now().toString(36).toUpperCase();
  const payload = {
    token: cfg.token,
    type: "CONTACT_EKGURU_NOTIFICATION",
    to: "EkGuruLearning@gmail.com",
    subject: "[TEST] idempotency replay check",
    text: "controlled relay idempotency test — please ignore",
    html: "<p>controlled relay idempotency test — please ignore</p>",
    replyTo: "EkGuruLearning@gmail.com",
    fromName: "EkGuru",
    requestId: "live-req-1",
    idempotencyKey: idem
  };
  const first = await postRelay(payload);
  check("first POST with idem key → sent", first.success === "true" && first.message === "sent",
    JSON.stringify(first));
  const second = await postRelay(payload);
  check("replay of same key → duplicate (not re-sent)",
    second.success === "true" && second.dedup === true,
    JSON.stringify(second));

  console.log("\n" + (failures === 0 ? "ALL LIVE RELAY TESTS PASSED" : failures + " FAILURE(S)"));
  process.exit(failures === 0 ? 0 : 1);
})();

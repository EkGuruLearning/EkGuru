#!/usr/bin/env node
/* =========================================================
   EkGuru: INTAKE TEST (applications, reviews, sign-ups)
   ---------------------------------------------------------
   A. apps-script/Intake.gs in a sandbox with fake Google services:
      · refuses without consent, with a filled honeypot (silently
        succeeds, stores nothing), with an unknown kind, with bad
        email/url/number/enum, and with an oversize payload
      · writes ONLY to applications / reviews_pending / signups,
        always status=pending and approved blank
      · never writes to the public tabs (tutors, reviews, settings)
      · neutralises formula injection and HTML in text
      · enforces the hourly and daily caps
      · never echoes a field value back, only a short reference
      · health reports row counts only
   B. js/intake.js in a sandbox:
      · off (blank or malformed url): no request is made
      · on: POSTs text/plain JSON to the /exec address, shows the
        reference on success, the server's reason on refusal, and
        the email fallback when the request fails
   Run:  node tools/test-intake.js
   ========================================================= */
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const ROOT = path.join(__dirname, "..");

let failures = 0;
function check(name, cond, extra) {
  if (!cond) failures++;
  console.log((cond ? "PASS" : "FAIL") + "  " + name + (cond ? "" : "  ->  " + (extra || "")));
}

/* ---------- A. Intake.gs ---------- */
function makeSheets(names) {
  const tabs = {};
  names.forEach((n) => { tabs[n] = { rows: [] }; });
  return tabs;
}
function loadIntake(tabsSeed, opts) {
  opts = opts || {};
  const tabs = makeSheets(tabsSeed || []);
  const store = {};
  const sheetObj = (name) => ({
    appendRow: (row) => { tabs[name] = tabs[name] || { rows: [] }; tabs[name].rows.push(row); },
    getLastRow: () => (tabs[name] ? tabs[name].rows.length + 1 : 1),
    setFrozenRows: () => {}
  });
  const ctx = {
    console,
    SpreadsheetApp: {
      getActive: () => ({
        getSheetByName: (n) => (tabs[n] ? sheetObj(n) : null),
        insertSheet: (n) => { tabs[n] = { rows: [] }; return sheetObj(n); }
      })
    },
    CacheService: {
      getScriptCache: () => ({
        get: (k) => (Object.prototype.hasOwnProperty.call(store, k) ? store[k] : null),
        put: (k, v) => { store[k] = String(v); }
      })
    },
    ContentService: {
      MimeType: { JSON: "JSON" },
      createTextOutput: (t) => ({ text: t, setMimeType() { return this; }, getContent() { return this.text; } })
    },
    Utilities: { formatDate: (d, tz, f) => (f === "yyyyMMddHH" ? "2026110109" : "20261101") },
    Math
  };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(ROOT, "apps-script", "Intake.gs"), "utf8"), ctx);
  return { ctx, tabs, store };
}
/* data rows only: the script writes a header row when it creates a tab */
const dataRows = (tab) => (tab && tab.rows ? tab.rows.filter((r) => r[0] !== "timestamp") : []);
const post = (ctx, body) => JSON.parse(ctx.doPost({ postData: { contents: typeof body === "string" ? body : JSON.stringify(body) } }).getContent());

const APP = {
  kind: "application", consent: true, website: "",
  fields: { name: "Asha Verma", email: "asha@example.com", subject: "Hindi conversation", bio: "I teach Hindi to adults.", rate_usd: "7", city: "Jaipur" }
};
const REV = {
  kind: "review", consent: true, website: "",
  fields: { tutor_id: "sushila-g", reviewer_name: "Priya", stars: "5", text: "Patient and clear." }
};
const SIGN = {
  kind: "signup", consent: true, website: "",
  fields: { email: "learner@example.com", goal: "Travel", level: "Never studied" }
};

{
  const I = loadIntake(["tutors", "reviews", "settings"]);
  let r = post(I.ctx, APP);
  check("a complete application is accepted with a reference", r.ok === true && /^EG-[A-Z0-9]{6}$/.test(r.reference), JSON.stringify(r));
  check("it lands on the applications tab as one data row, under a header row",
    dataRows(I.tabs.applications).length === 1 && I.tabs.applications.rows[0][0] === "timestamp", JSON.stringify(I.tabs.applications));
  const hdr = I.ctx.INTAKE_KINDS.application.header;
  const row = dataRows(I.tabs.applications)[0];
  check("status is pending", row[hdr.indexOf("status")] === "pending");
  check("approved is blank (the owner sets it)", row[hdr.indexOf("approved")] === "");
  check("the reference on the row matches the one returned", row[hdr.indexOf("reference")] === r.reference);
  check("nothing from the form is echoed in the response",
    !/Asha|asha@example|Jaipur|conversation/.test(JSON.stringify(r)), JSON.stringify(r));
  check("the public tabs were not touched",
    I.tabs.tutors.rows.length === 0 && I.tabs.reviews.rows.length === 0 && I.tabs.settings.rows.length === 0);

  r = post(I.ctx, REV);
  check("a review goes to reviews_pending, never to the live reviews tab",
    r.ok && dataRows(I.tabs.reviews_pending).length === 1 && I.tabs.reviews.rows.length === 0);

  r = post(I.ctx, SIGN);
  check("a sign-up goes to signups, private", r.ok && dataRows(I.tabs.signups).length === 1);
  check("a missing tab is created with its header row first", I.tabs.signups.rows[0][0] === "timestamp");
}

{
  const I = loadIntake([]);
  let r = post(I.ctx, { ...APP, consent: false });
  check("no consent, no save", r.ok === false && /consent/.test(r.error) && !I.tabs.applications, JSON.stringify(r));
  r = post(I.ctx, { ...APP, website: "http://spam.example" });
  check("honeypot filled: says ok but stores nothing", r.ok === true && !I.tabs.applications, JSON.stringify(r));
  r = post(I.ctx, { ...APP, kind: "payments" });
  check("an unknown kind is refused", r.ok === false && /unknown kind/.test(r.error));
  r = post(I.ctx, "{not json");
  check("malformed JSON is refused without a stack trace", r.ok === false && r.error === "not JSON");
  r = post(I.ctx, "x".repeat(13000));
  check("an oversize payload is refused", r.ok === false && r.error === "too large");
  r = post(I.ctx, { ...APP, fields: { ...APP.fields, email: "not-an-email" } });
  check("a bad email is refused, in plain words", r.ok === false && /email/.test(r.error), JSON.stringify(r));
  r = post(I.ctx, { ...APP, fields: { ...APP.fields, photo_link: "http://insecure.example/a.jpg" } });
  check("a photo link must be https", r.ok === false && /https/.test(r.error));
  r = post(I.ctx, { ...APP, fields: { ...APP.fields, rate_usd: "500" } });
  check("a rate above the limit is refused", r.ok === false && /rate usd|rate_usd/.test(r.error), JSON.stringify(r));
  r = post(I.ctx, { ...APP, fields: { ...APP.fields, bio: "" } });
  check("a required field left empty is refused", r.ok === false && /bio/.test(r.error));
  r = post(I.ctx, { ...SIGN, fields: { ...SIGN.fields, goal: "Make money fast" } });
  check("an enum outside the menu is refused", r.ok === false && /options/.test(r.error));
  r = post(I.ctx, { ...APP, fields: { ...APP.fields, subject: "<script>x</script>" } });
  check("HTML is stripped from text", r.ok === true && !/[<>]/.test(dataRows(I.tabs.applications).slice(-1)[0].join("|")));
  r = post(I.ctx, { ...APP, fields: { ...APP.fields, name: "=HYPERLINK(\"http://x\")" } });
  check("a leading formula character is neutralised", r.ok === true && dataRows(I.tabs.applications).slice(-1)[0].some((c) => c === "'=HYPERLINK(\"http://x\")"));
  check("no refused submission left a row behind", dataRows(I.tabs.applications).length === 2, String(dataRows(I.tabs.applications).length));
}

{
  const I = loadIntake([]);
  let ok = 0, last = null;
  for (let i = 0; i < 40; i++) { last = post(I.ctx, { ...SIGN, fields: { ...SIGN.fields, email: "l" + i + "@example.com" } }); if (last.ok) ok++; }
  check("the hourly cap stops a flood (30 accepted of 40)", ok === 30, "accepted " + ok);
  check("the refusal says to try later, not why it is capped", last.ok === false && /try again later/.test(last.error), JSON.stringify(last));
}

{
  const I = loadIntake(["applications", "reviews_pending"]);
  const h = JSON.parse(I.ctx.doGet({ parameter: { action: "health" } }).getContent());
  check("health says ok and lists pending counts", h.ok === true && h.pendingRows.applications === 0 && h.pendingRows.reviews_pending === 0, JSON.stringify(h));
  check("health holds no field contents", !/@|Asha|Priya/.test(JSON.stringify(h)));
  const bad = JSON.parse(I.ctx.doGet({ parameter: { action: "dump" } }).getContent());
  check("any other GET action is refused", bad.ok === false);
}

{
  const src = fs.readFileSync(path.join(ROOT, "apps-script", "Intake.gs"), "utf8");
  check("Intake.gs never opens another workbook by id", !/openById|openByUrl/.test(src));
  check("Intake.gs never reads the public tabs", !/getSheetByName\("(tutors|reviews|settings|support)"\)/.test(src));
  check("Intake.gs holds no key, token or payments id", !/RAZORPAY|1u5Jkbe|secret|password/i.test(src));
  check("Intake.gs defines no doPost clash with the mailer (one doPost, one file)", (src.match(/function doPost\(/g) || []).length === 1);
}

/* ---------- C. the build never bakes an applicant ---------- */
{
  const st = fs.readFileSync(path.join(ROOT, "tools", "sheetsync.js"), "utf8");
  check("sheetsync reads the reviewed registry before it bakes anything",
    /window\\.EKGURU_TUTOR_ORDER/.test(st) && /registered\.has\(id\)/.test(st));
  check("sheetsync skips a row that is not in the registry, before any field is copied",
    st.indexOf("if (!registered.has(id)) { skippedUnregistered.push(id); continue; }") >
      st.indexOf("const registered = new Set(") &&
    st.indexOf("if (!registered.has(id))") < st.indexOf("const t = buildTutor(row);"));
  const ov = fs.readFileSync(path.join(ROOT, "js", "tutors", "_overrides.js"), "utf8");
  check("the committed overrides hold no applicant id, bio or photo link",
    !/"(hemlata|tara|sarshtee-baliyan)"\s*:\s*\{/.test(ov) && !/"photo_link"|"bio":\s*"I teach/.test(ov));
}

/* ---------- B. js/intake.js ---------- */
function loadClient(siteIntake, fetchPlan) {
  const calls = [];
  const fetch = (url, opts) => {
    calls.push({ url: String(url), opts });
    const rule = fetchPlan(String(url), opts);
    if (rule.throw) return Promise.reject(new Error("network down"));
    return Promise.resolve({ ok: rule.status ? rule.status < 400 : true, status: rule.status || 200, text: () => Promise.resolve(rule.body) });
  };
  const listeners = {};
  const forms = [];
  const sandbox = {
    console,
    setTimeout, clearTimeout,
    AbortController: typeof AbortController === "function" ? AbortController : undefined,
    EKGURU_SITE: { intake: siteIntake },
    fetch,
    document: {
      readyState: "complete",
      querySelectorAll: () => forms,
      addEventListener: () => {}
    }
  };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(fs.readFileSync(path.join(ROOT, "js", "intake.js"), "utf8"), sandbox);
  return { api: sandbox.EkGuruIntake, calls, forms };
}

const EXEC = "https://script.google.com/macros/s/AKfycbzINTAKE_123-abc/exec";
const fields = { name: "Asha", email: "asha@example.com", subject: "Hindi", bio: "Short bio." };

(async function () {
  let c = loadClient({ url: "" }, () => ({ body: "{}" }));
  check("off when the url is blank: not ready", c.api.ready() === false);
  let res = await c.api.submit("application", fields, true, "");
  check("off: no request is sent", c.calls.length === 0);
  check("off: the caller is told to use email", res.ok === false && res.fallback === true);

  c = loadClient({ url: "http://script.google.com/macros/s/AKfyc/exec" }, () => ({ body: "{}" }));
  check("a non-https url is ignored", c.api.ready() === false);
  c = loadClient({ url: "https://evil.example.com/macros/s/AKfyc/exec" }, () => ({ body: "{}" }));
  check("a foreign url is ignored", c.api.ready() === false);

  c = loadClient({ url: EXEC }, () => ({ body: JSON.stringify({ ok: true, reference: "EG-K3Q9AP" }) }));
  check("on: ready", c.api.ready() === true);
  res = await c.api.submit("application", fields, true, "");
  check("on: posts to the exec address", c.calls.length === 1 && c.calls[0].url === EXEC, c.calls[0] && c.calls[0].url);
  check("on: sends text/plain JSON (no CORS preflight)", c.calls[0].opts.method === "POST" &&
    c.calls[0].opts.headers["Content-Type"].indexOf("text/plain") === 0 && JSON.parse(c.calls[0].opts.body).kind === "application");
  check("on: the body carries consent and an empty honeypot", JSON.parse(c.calls[0].opts.body).consent === true && JSON.parse(c.calls[0].opts.body).website === "");
  check("on: success returns the reference", res.ok === true && res.reference === "EG-K3Q9AP", JSON.stringify(res));

  c = loadClient({ url: EXEC }, () => ({ body: JSON.stringify({ ok: false, error: "that email does not look right" }) }));
  res = await c.api.submit("application", fields, true, "");
  check("refusal: the server's reason is shown, not a generic one", res.ok === false && res.error === "that email does not look right" && !res.fallback);

  c = loadClient({ url: EXEC }, () => ({ throw: true }));
  res = await c.api.submit("application", fields, true, "");
  check("network failure: falls back to email, never rejects", res.ok === false && res.fallback === true);

  c = loadClient({ url: EXEC }, () => ({ status: 500, body: "" }));
  res = await c.api.submit("application", fields, true, "");
  check("HTTP 500: falls back to email", res.fallback === true);

  c = loadClient({ url: EXEC }, () => ({ body: "<html>Sign in</html>" }));
  res = await c.api.submit("application", fields, true, "");
  check("an HTML page instead of JSON: falls back, no crash", res.fallback === true);

  c = loadClient({ url: EXEC }, () => ({ body: "{}" }));
  res = await c.api.submit("application", { ...fields, email: "bad" }, true, "");
  check("client-side: a bad email is caught before any request", res.ok === false && c.calls.length === 0 && /email/.test(res.error));
  res = await c.api.submit("application", { ...fields, bio: "" }, true, "");
  check("client-side: an empty required field is caught", res.ok === false && /bio/.test(res.error) && c.calls.length === 0);
  res = await c.api.submit("application", fields, false, "");
  check("client-side: no consent, no request", res.ok === false && c.calls.length === 0 && /tick the box/.test(res.error));
  res = await c.api.submit("payments", fields, true, "");
  check("an unknown kind never sends", res.ok === false && c.calls.length === 0);
  res = await c.api.submit("review", { tutor_id: "x", reviewer_name: "R", stars: 5, text: "t".repeat(900) }, true, "");
  check("client-side: a review over 800 characters is caught", res.ok === false && /too long/.test(res.error));

  /* the join page form and the site config */
  const join = fs.readFileSync(path.join(ROOT, "join.html"), "utf8");
  const form = /<form class="intake-form" data-intake="application"[\s\S]*?<\/form>/.exec(join);
  check("join.html has the online application form", !!form);
  check("the form has a honeypot named website, hidden from people", !!form && /name="website"/.test(form[0]) && /left:-10000px/.test(form[0]) && /tabindex="-1"/.test(form[0]));
  check("the form has an explicit consent checkbox", !!form && /name="consent"[^>]*required/.test(form[0]));
  check("the form falls back to a mailto action", !!form && /action="mailto:EkGuruLearning@gmail\.com"/.test(form[0]));
  check("join.html loads js/intake.js", /src="js\/intake\.js"/.test(join));
  const cfg = fs.readFileSync(path.join(ROOT, "js", "site-config.js"), "utf8");
  const m = /intake:\s*\{\s*url:\s*"([^"]*)"/.exec(cfg);
  check("js/site-config.js has an intake block, blank or a valid /exec", !!m && (m[1] === "" || /^https:\/\/script\.google\.com\/macros\/s\/[A-Za-z0-9_-]+\/exec$/.test(m[1])), m && m[1]);

  console.log("\n" + (failures === 0 ? "ALL INTAKE TESTS PASSED" : failures + " FAILURE(S)"));
  process.exit(failures === 0 ? 0 : 1);
})();

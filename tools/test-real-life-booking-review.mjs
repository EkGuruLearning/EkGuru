#!/usr/bin/env node
/* =========================================================
   EkGuru — REAL-LIFE BOOKING → REVIEW JOURNEY  (16 Nov 2026)
   ---------------------------------------------------------
   One student, one tutor, the shipped pages, no network:

     1. find-tutors.html with sushila-g active=yes in the sheet
        -> her card is on the roster and links to the profile
     2. tutor.html?id=sushila-g: the student taps "Book", fills
        the form, sends
        · the booking row reaches the private sheet (intake POST,
          kind=booking, booking_ref EK-XXXXXX, tutor_id)
        · the receipt on screen shows the SAME reference
        · the browser ledger (EkGuruStore) records it as sent
     3. the student opens the tutor's profile and leaves a review,
        typing the reference the way people do ("ek-xxxxxx ")
        · the review POST carries kind=review + canonical EK- ref
     4. the server (Intake.gs, run in a vm) accepts that exact
        payload against the booking row from step 2 and files it
        under reviews_pending — never the live reviews tab.

   Run:  node tools/test-real-life-booking-review.mjs
   ========================================================= */
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const ROOT = path.resolve(import.meta.dirname, "..");

let pass = 0, fail = 0;
function ok(name, cond, extra) {
  if (cond) { pass++; console.log("PASS  " + name); }
  else { fail++; console.log("FAIL  " + name + (extra ? "  -- " + extra : "")); }
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const INTAKE = "https://script.google.com/macros/s/AKfyREALLIFE/exec";

/* ---------- the sheet ---------- */
const TUTORS_TSV = fs.readFileSync(path.join(ROOT, "tests/fixtures/tutors.tsv"), "utf8");
function tutorsTsv() {
  const lines = TUTORS_TSV.split("\n");
  const head = lines[0].split("\t");
  const ia = head.indexOf("active"), ii = head.indexOf("id"), ie = head.indexOf("notification_email");
  return lines.map((l, n) => {
    if (!n || !l) return l;
    const c = l.split("\t");
    if (c[ii] === "sushila-g") { c[ia] = "yes"; if (ie >= 0) c[ie] = "sushila.tutor@example.com"; }
    return c.join("\t");
  }).join("\n");
}
const csvOf = (tsv) => tsv.split("\n").map((l) => l.split("\t").map((c) => '"' + c.replace(/"/g, '""') + '"').join(",")).join("\n");
const REVIEWS_TSV = ["tutor", "name", "date", "stars", "text", "source", "status"].join("\t") + "\n";

/* ---------- a fake internet ---------- */
function makeNet() {
  const posts = [];   /* every POST body the browser sent, by host */
  const fetch = (u, o) => {
    u = String(u); o = o || {};
    const text = (body, status) => Promise.resolve({ ok: (status || 200) < 400, status: status || 200, text: () => Promise.resolve(body), json: () => Promise.resolve(JSON.parse(body)) });
    if (/gid=1631273256/.test(u)) return text(/output=tsv/.test(u) ? tutorsTsv() : csvOf(tutorsTsv()));
    if (/gid=293675115/.test(u)) return /output=csv/.test(u) ? text("", 500) : text(REVIEWS_TSV);
    if (u === INTAKE && o.method === "POST") {
      const body = JSON.parse(o.body);
      posts.push({ host: "intake", body });
      return text(JSON.stringify({ ok: true, reference: "EG-" + (body.kind === "booking" ? "BOOKED" : "REVIEW") }));
    }
    if (/web3forms\.com/.test(u) && o.method === "POST") {
      posts.push({ host: "web3forms", body: o.body });
      return text(JSON.stringify({ success: true, message: "ok" }));
    }
    if (/formsubmit\.co|emailjs\.com|staticforms/.test(u)) {
      posts.push({ host: "other-mail", body: o.body });
      return text(JSON.stringify({ success: "true" }));
    }
    return Promise.reject(new Error("offline: " + u.slice(0, 60)));
  };
  return { fetch, posts };
}

const STORAGE = new Map();
const storage = () => ({
  getItem: (k) => (STORAGE.has(k) ? STORAGE.get(k) : null),
  setItem: (k, v) => STORAGE.set(k, String(v)),
  removeItem: (k) => STORAGE.delete(k),
  clear: () => STORAGE.clear(),
  key: (i) => Array.from(STORAGE.keys())[i] || null,
  get length() { return STORAGE.size; }
});

function resolveScript(src, pageRel) {
  if (src.startsWith("/")) return src.slice(1);
  if (/^https?:/.test(src)) return null;
  return path.normalize(path.join(path.dirname(pageRel), src));
}
async function loadPage(rel, url, net, settle) {
  const html = fs.readFileSync(path.join(ROOT, rel), "utf8");
  const dom = new JSDOM(html, { url, runScripts: "outside-only", pretendToBeVisual: true });
  const win = dom.window;
  win.fetch = net.fetch;
  Object.defineProperty(win, "localStorage", { value: storage(), configurable: true });
  Object.defineProperty(win, "sessionStorage", { value: storage(), configurable: true });
  win.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
  win.matchMedia = win.matchMedia || ((q) => ({ matches: false, media: q, addEventListener() {}, removeEventListener() {}, addListener() {}, removeListener() {} }));
  win.scrollTo = () => {}; win.HTMLElement.prototype.scrollIntoView = function () {};
  win.requestAnimationFrame = (f) => setTimeout(f, 0);
  win.console = { log() {}, info() {}, warn() {}, error() {}, debug() {} };
  const errors = [];
  /* js/lazy.js injects mailer/calendar/etc. as <script src> at run time.
     jsdom (outside-only) would never run them, so a Book click would
     wait forever. Run the file when the tag lands, then fire load —
     which is what a browser does. */
  const realAppend = win.Node.prototype.appendChild, realInsert = win.Node.prototype.insertBefore;
  function runInjected(node) {
    if (!node || node.nodeName !== "SCRIPT" || !node.getAttribute("src")) return;
    const p = resolveScript(node.getAttribute("src").split("?")[0], rel);
    if (!p) return;
    const file = path.join(ROOT, p);
    setTimeout(() => {
      try {
        if (fs.existsSync(file)) { win.eval(fs.readFileSync(file, "utf8")); node.dispatchEvent(new win.Event("load")); }
        else node.dispatchEvent(new win.Event("error"));
      } catch (e) { errors.push(p + ": " + String(e && e.message).slice(0, 100)); node.dispatchEvent(new win.Event("error")); }
    }, 0);
  }
  win.Node.prototype.appendChild = function (n) { const r = realAppend.call(this, n); runInjected(n); return r; };
  win.Node.prototype.insertBefore = function (n, ref) { const r = realInsert.call(this, n, ref); runInjected(n); return r; };
  for (const s of [...win.document.querySelectorAll("script[src]")]) {
    const p = resolveScript(s.getAttribute("src"), rel);
    if (p === null) continue;
    const file = path.join(ROOT, p);
    if (!fs.existsSync(file)) continue;
    try { win.eval(fs.readFileSync(file, "utf8")); } catch (e) { errors.push(p + ": " + String(e && e.message).slice(0, 100)); }
    /* the live config has no intake url in the sandbox copy? — it does;
       point it at our fake endpoint right after site-config loads */
    if (/site-config\.js$/.test(p) && win.EKGURU_SITE) {
      win.EKGURU_SITE.intake = Object.assign({}, win.EKGURU_SITE.intake, { url: INTAKE });
    }
  }
  win.document.dispatchEvent(new win.Event("DOMContentLoaded", { bubbles: true }));
  win.dispatchEvent(new win.Event("load"));
  await sleep(settle || 900);
  return { win, errors, close: () => dom.window.close() };
}

/* ================= 1 + 2. book a lesson ================= */
console.log("\n== 1. find-tutors.html, sushila-g active=yes ==");
STORAGE.clear();
const net = makeNet();
let bookingRef = "";
{
  const { win, errors, close } = await loadPage("find-tutors.html", "https://ekguru.shop/find-tutors.html", net, 1200);
  const d = win.document;
  ok("roster loads without script errors", errors.length === 0, errors.join(" | "));
  const card = d.querySelector('.tcard[data-id="sushila-g"]');
  ok("sushila-g's card is on the roster", !!card);
  const link = card && card.querySelector('a[href*="sushila-g"]');
  ok("the card links to her profile", !!link, card && card.innerHTML.slice(0, 200));
  close();
}
{
  const { win, errors, close } = await loadPage("tutor.html", "https://ekguru.shop/tutor.html?id=sushila-g", net, 1200);
  const d = win.document;
  ok("interactive profile loads without script errors", errors.length === 0, errors.join(" | "));
  const bookBtn = d.querySelector('[data-book="sushila-g"]');
  ok("a Book button for sushila-g is on the page", !!bookBtn, [...d.querySelectorAll("button")].map((b) => b.textContent.trim().slice(0, 20)).join(","));

  console.log("\n== 2. The student books ==");
  bookBtn && bookBtn.click();
  await sleep(300);
  const modal = d.querySelector(".bk-modal, [class*=bk-]") && d.getElementById("bk-name") && d.getElementById("bk-name").closest("[class]");
  ok("booking modal opened with the form", !!d.getElementById("bk-name") && !!d.getElementById("bk-email"), "");
  ok("modal names the tutor", /Sushila/.test((d.getElementById("bk-title") || {}).textContent || ""), (d.getElementById("bk-title") || {}).textContent);

  const slot = d.querySelector(".sched-slot, .bk-slot");
  ok("at least one time slot is offered", !!slot);
  slot && slot.click();
  if (!d.getElementById("bk-name")) { console.log("\n" + pass + " passed, " + (fail + 1) + " failed (modal never opened)"); process.exit(1); }
  d.getElementById("bk-name").value = "Asha Verma";
  d.getElementById("bk-email").value = "Asha.Verma@example.com";
  const goal = d.getElementById("bk-goal"); if (goal) goal.value = "Speak with my in-laws in Jaipur";
  const wa = d.getElementById("bk-whatsapp"); if (wa) wa.value = "+91 98765 43210";
  ["bk-name", "bk-email", "bk-goal"].forEach((id) => { const el = d.getElementById(id); el && el.dispatchEvent(new win.Event("input", { bubbles: true })); });
  await sleep(1500);  /* refreshBookingLive timers (1200 ms) re-enable the button */

  const send = d.querySelector(".bk-send");
  ok("send button exists and is enabled", !!send && !send.disabled, send ? ("disabled=" + send.disabled + " text=" + send.textContent.trim()) : "no button");
  send && send.click();
  await sleep(1500);

  const intakePost = net.posts.find((p) => p.host === "intake" && p.body.kind === "booking");
  ok("exactly one booking row was sent to the private sheet", net.posts.filter((p) => p.host === "intake" && p.body.kind === "booking").length === 1, JSON.stringify(net.posts.map((p) => p.host + ":" + (p.body && p.body.kind))));
  const f = (intakePost && intakePost.body.fields) || {};
  bookingRef = f.booking_ref || "";
  ok("booking_ref is a fresh EK-XXXXXX code", /^EK-[A-HJ-NP-Z2-9]{6}$/.test(bookingRef), bookingRef);
  ok("row names the right tutor and student", f.tutor_id === "sushila-g" && f.student_name === "Asha Verma" && f.student_email === "Asha.Verma@example.com", JSON.stringify(f));
  ok("row carries the chosen slot and the WhatsApp number", /\S/.test(f.preferred_times_ist || "") && f.preferred_times_ist !== "Not chosen" && f.student_whatsapp === "+91 98765 43210", JSON.stringify({ t: f.preferred_times_ist, w: f.student_whatsapp }));
  ok("source_page is origin+path only (no ?id= / tracking params)", f.source_page === "https://ekguru.shop/tutor.html", f.source_page);
  ok("consent flag travels with the row", intakePost && intakePost.body.consent === true);

  const mailPosts = net.posts.filter((p) => p.host !== "intake");
  ok("booking email went out AFTER the sheet row (never before)", mailPosts.length >= 1 && net.posts.indexOf(intakePost) < net.posts.indexOf(mailPosts[0]), JSON.stringify(net.posts.map((p) => p.host)));
  const ownerLeak = mailPosts.some((p) => /EkGuruLearning@gmail\.com/i.test(String(p.body)) && !/Asha\.Verma@example\.com/i.test(String(p.body)));
  ok("no booking mail is addressed to the owner inbox", !ownerLeak);

  const body = d.querySelector(".bk-body");
  const txt = body ? body.textContent : "";
  ok("receipt replaced the form", !!d.querySelector(".bk-done") || /reference/i.test(txt), txt.slice(0, 120));
  ok("receipt shows the same EK- reference the sheet got", txt.indexOf(bookingRef) !== -1, "ref=" + bookingRef + " txt=" + txt.slice(0, 200));
  ok("receipt tells the student to keep the reference for a review", /review/i.test(txt), txt.slice(0, 300));
  ok("receipt never prints the tutor's private inbox", !/sushila\.tutor@example\.com/.test(txt));

  const led = (win.EkGuruStore && win.EkGuruStore.all ? win.EkGuruStore.all() : []).filter((r) => r.ref === bookingRef);
  ok("browser ledger holds the booking as sent", led.length === 1 && led[0].status === "sent", JSON.stringify(led[0] || null));
  close();
}

/* ================= 3. the review ================= */
console.log("\n== 3. Days later, the student reviews from the profile page ==");
let reviewBody = null;
{
  const { win, errors, close } = await loadPage("tutor/sushila-g/index.html", "https://ekguru.shop/tutor/sushila-g/", net, 900);
  const d = win.document;
  ok("profile loads without script errors", errors.length === 0, errors.join(" | "));
  const form = d.querySelector('form[data-intake="review"]');
  ok("the review form is on the profile", !!form);
  ok("the review form asks for the booking reference", !!(form && form.elements.namedItem("booking_id")));
  if (form) {
    form.elements.namedItem("reviewer_name").value = "Asha";
    form.elements.namedItem("stars").value = "5";
    form.elements.namedItem("booking_id").value = " " + bookingRef.toLowerCase().replace("-", " ") + " ";  /* "ek ab2cd3 " */
    form.elements.namedItem("text").value = "Three lessons in and I can greet my in-laws properly. Patient and clear.";
    form.elements.namedItem("consent").checked = true;
    const btn = form.querySelector('button[type="submit"]');
    form.dispatchEvent(new win.Event("submit", { bubbles: true, cancelable: true }));
    await sleep(600);
    const rp = net.posts.filter((p) => p.host === "intake" && p.body.kind === "review");
    ok("exactly one review was posted to the intake endpoint", rp.length === 1, String(rp.length));
    reviewBody = rp[0] && rp[0].body;
    const rf = (reviewBody && reviewBody.fields) || {};
    ok("the sloppy-typed reference was sent canonically", rf.booking_id === bookingRef, JSON.stringify(rf.booking_id) + " vs " + bookingRef);
    ok("review names the tutor id of the page", rf.tutor_id === "sushila-g");
    const msg = form.querySelector("[data-intake-msg]");
    ok("the student sees the thank-you with a reference", msg && /Thank you/.test(msg.textContent) && /EG-REVIEW/.test(msg.textContent), msg && msg.textContent);
    ok("the form was reset after sending", form.elements.namedItem("text").value === "");
    ok("submit button re-enabled", btn && !btn.disabled);
  }
  close();
}

/* ================= 4. the server side ================= */
console.log("\n== 4. Intake.gs accepts exactly those two payloads ==");
{
  const tabs = {};
  const sheet = (name) => ({
    appendRow: (row) => { tabs[name] = tabs[name] || { rows: [] }; tabs[name].rows.push(row.slice()); },
    getLastRow: () => (tabs[name] ? tabs[name].rows.length : 0),
    getRange: (row, col, numRows, numCols) => ({
      getValues: () => {
        const out = [];
        for (let r = 0; r < (numRows || 1); r++) {
          const vals = [];
          for (let c = 0; c < (numCols || 1); c++) {
            const src = (tabs[name] && tabs[name].rows[row - 1 + r]) || [];
            vals.push(src[col - 1 + c] !== undefined ? src[col - 1 + c] : "");
          }
          out.push(vals);
        }
        return out;
      },
      setValues: (vals) => {
        vals.forEach((line, r) => {
          const idx = row - 1 + r;
          tabs[name].rows[idx] = tabs[name].rows[idx] || [];
          line.forEach((v, c) => { tabs[name].rows[idx][col - 1 + c] = v; });
        });
      }
    }),
    setFrozenRows: () => {}
  });
  const ss = {
    getSheetByName: (n) => (tabs[n] ? sheet(n) : null),
    insertSheet: (n) => { tabs[n] = { rows: [] }; return sheet(n); }
  };
  const store = {};
  const ctx = {
    console,
    SpreadsheetApp: { getActive: () => ss, getActiveSpreadsheet: () => ss, openById: () => ss },
    PropertiesService: { getScriptProperties: () => ({ getProperty: () => null }) },
    LockService: { getScriptLock: () => ({ tryLock: () => true, waitLock() {}, releaseLock() {} }) },
    CacheService: { getScriptCache: () => ({ get: (k) => (k in store ? store[k] : null), put: (k, v) => { store[k] = String(v); } }) },
    ContentService: { MimeType: { JSON: "JSON" }, createTextOutput: (t) => ({ text: t, setMimeType() { return this; }, getContent() { return this.text; } }) },
    Utilities: { formatDate: (d, tz, f) => (f === "yyyyMMddHH" ? "2026111609" : "20261116") },
    Math, Date, JSON, String, Number, Object, Array, RegExp, isFinite
  };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(ROOT, "apps-script/Intake.gs"), "utf8"), ctx);
  const post = (b) => JSON.parse(ctx.doPost({ postData: { contents: JSON.stringify(b) } }).getContent());

  const bookingPost = net.posts.find((p) => p.host === "intake" && p.body.kind === "booking").body;
  const r1 = post(bookingPost);
  ok("server accepts the browser's booking payload verbatim", r1.ok === true && r1.reference === bookingRef, JSON.stringify(r1));
  ok("server stores the booking under the same EK- reference", (tabs.bookings.rows[1] || [])[0] === bookingRef, JSON.stringify(tabs.bookings.rows[1]));

  const r2 = post(reviewBody);
  ok("server accepts the browser's review payload against that booking", r2.ok === true && /^EG-/.test(r2.reference), JSON.stringify(r2));
  ok("review lands in reviews_pending, never the live reviews tab", !!tabs.reviews_pending && tabs.reviews_pending.rows.length === 2 && !tabs.reviews, JSON.stringify(Object.keys(tabs)));
  const hdr = ctx.INTAKE_KINDS.review.header;
  const row = tabs.reviews_pending.rows[1];
  ok("pending row is status=pending with the canonical booking id", row[hdr.indexOf("status")] === "pending" && row[hdr.indexOf("booking_id")] === bookingRef, JSON.stringify(row));

  /* a stranger with no booking */
  const r3 = post({ ...reviewBody, fields: { ...reviewBody.fields, booking_id: "EK-ZZZZZZ" } });
  ok("a stranger's review (no booking) is refused and not stored", r3.ok === false && tabs.reviews_pending.rows.length === 2, JSON.stringify(r3));
  /* the same booking, another tutor */
  const r4 = post({ ...reviewBody, fields: { ...reviewBody.fields, tutor_id: "shikha-dutta" } });
  ok("the booking cannot be reused to review a different tutor", r4.ok === false && /different tutor/.test(r4.error), JSON.stringify(r4));
}

console.log("\n" + pass + " passed, " + fail + " failed");
process.exit(fail ? 1 : 0);

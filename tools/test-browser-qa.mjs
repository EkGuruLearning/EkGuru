#!/usr/bin/env node
/** Release-mode browser-source QA for the public Support page.
 *
 * The current release intentionally has one ordinary link to Razorpay's hosted
 * page. Custom checkout, public-supporter feeds and third-party payment loaders
 * are not public release features and must not silently return.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const source = fs.readFileSync(path.join(ROOT, "support/index.html"), "utf8");
const dom = new JSDOM(source, { url: "https://ekguru.shop/support/" });
const { document } = dom.window;
let pass = 0, fail = 0;
function ok(label, condition, detail = "") {
  if (condition) { pass++; console.log("  PASS " + label + (detail ? " — " + detail : "")); }
  else { fail++; console.error("  FAIL " + label + (detail ? " — " + detail : "")); }
}

console.log("Support release-mode QA");
const links = [...document.querySelectorAll('a[href*="pages.razorpay.com"]')];
ok("exactly one hosted payment link", links.length === 1, String(links.length));
const payment = links[0];
ok("hosted link uses HTTPS", payment && new URL(payment.href).protocol === "https:");
ok("hosted link opens outside EkGuru", payment && payment.target === "_blank");
ok("new-tab link prevents opener access", payment && /\bnoopener\b/.test(payment.rel));
ok("support copy says contribution is optional", /contribution is optional/i.test(source));
ok("support copy says contribution buys no access or lesson", /does not purchase access, a lesson or a subscription/i.test(source));
ok("credentials are entered on provider page", /does not receive your card number, UPI PIN or online-banking credentials/i.test(source));
ok("no custom checkout form is public", !document.getElementById("support-payment-form"));
ok("no recent-supporter feed is public", !document.getElementById("recent-supporters-section"));
ok("no Razorpay script loader runs on EkGuru", !document.querySelector('script[src*="razorpay"]') && !/embed_btn|checkout\.razorpay/i.test(source));
ok("no release payment JavaScript is loaded", !document.querySelector('script[src*="support-razorpay.js"]'));
ok("page is excluded from ads", document.documentElement.getAttribute("data-ad-class") === "TRANSACTIONAL");
ok("privacy settings script remains present", !!document.querySelector('script[src*="cookie-consent.js"]'));
ok("viewport meta supports mobile", /width=device-width/.test(document.querySelector('meta[name="viewport"]')?.content || ""));
ok("single main landmark", document.querySelectorAll("main").length === 1);
ok("single h1", document.querySelectorAll("h1").length === 1);
ok("payment link has usable text", (payment?.textContent.trim().length || 0) >= 10);

for (const width of [320, 360, 390, 430, 768, 1024, 1280, 1440, 1920]) {
  // JSDOM has no layout engine. This is a deterministic DOM contract check at
  // every required width; real Chromium overflow checks run separately.
  dom.window.innerWidth = width;
  ok(`payment control remains a link at ${width}px`, payment?.tagName === "A");
}

console.log(`\n${fail ? "FAIL" : "PASS"}: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);

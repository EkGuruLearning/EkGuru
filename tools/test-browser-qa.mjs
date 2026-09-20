#!/usr/bin/env node
/** Release payment-surface QA.
 *
 * The current public flow is deliberately small: one ordinary link to
 * Razorpay's hosted page. The owner-only custom API and recent-supporters UI
 * are not mounted until their production configuration and privacy review are
 * complete. This test prevents either inactive surface leaking back in.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const html = fs.readFileSync(path.join(ROOT, "support/index.html"), "utf8");
const style = fs.readFileSync(path.join(ROOT, "css/style.min.css"), "utf8");
const viewports = [320, 360, 390, 430, 768, 1024, 1280, 1440, 1920];
let passed = 0;
let failed = 0;
function check(value, label) {
  if (value) { passed++; console.log("  PASS  " + label); }
  else { failed++; console.error("  FAIL  " + label); }
}

console.log("EkGuru hosted-payment release QA");
check(/<meta\b(?=[^>]*name="viewport")(?=[^>]*width=device-width)[^>]*>/.test(html), "responsive viewport declared");
check(!/checkout\.razorpay\.com|cdn\.razorpay\.com|embed_btn\/bundle/.test(html), "no payment SDK/third-party loader on EkGuru");
check(!/support-payment-form|support-submit-btn|recent-supporters-section/.test(html), "inactive custom checkout and supporter feed are absent");
check(!/support-razorpay\.js/.test(html), "inactive custom-payment client is not requested");
check(/contribution is optional/i.test(html) && /does not purchase access/i.test(html), "support is described as optional and not a purchase");
check(/not a registered charity/i.test(html) && /does not claim tax-deductible/i.test(html), "no charity or tax-deduction claim");
check(/@media/.test(style), "shared stylesheet includes responsive rules");

for (const width of viewports) {
  const dom = new JSDOM(html, { url: "https://ekguru.shop/support/", pretendToBeVisual: true });
  Object.defineProperty(dom.window, "innerWidth", { configurable: true, value: width });
  const doc = dom.window.document;
  const links = [...doc.querySelectorAll('a[href^="https://pages.razorpay.com/"]')];
  check(links.length === 1, `${width}px: exactly one hosted-payment link`);
  const link = links[0];
  check(!!link && link.protocol === "https:" && link.target === "_blank", `${width}px: HTTPS link opens a separate provider page`);
  const rel = (link && link.getAttribute("rel") || "").split(/\s+/);
  check(rel.includes("noopener") && rel.includes("noreferrer"), `${width}px: external-window isolation present`);
  check(!!doc.querySelector("#support-active-section") && !doc.querySelector("form"), `${width}px: active support state is link-only`);
  dom.window.close();
}

console.log(`\n${failed ? "FAIL" : "PASS"}: ${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);

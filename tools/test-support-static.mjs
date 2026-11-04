#!/usr/bin/env node
/* =========================================================
   EkGuru — SUPPORT STATIC-CARD DRIFT TEST  (no network)
   ---------------------------------------------------------
   PayPal + Razorpay are static HTML in support/index.html
   (force fix, 4 Nov 2026) AND baked values in
   js/site-config.js. Two copies of one truth WILL drift
   unless a test forbids it — this is that test.

   Proves:
   1. support/index.html carries exactly one #support-link-paypal
      and one #support-link-razorpay anchor, each with the
      support-option class, target=_blank and rel=noopener.
   2. Their hrefs (HTML-entity decoded) equal the baked
      supportPaypal / supportRazorpay values in js/site-config.js.
   3. js/support.js does NOT render those two keys itself
      (no duplicate cards when the sheet is up).
   4. The FAQ names both always-on methods.

   Run:  node tools/test-support-static.mjs
   ========================================================= */
"use strict";
import { readFileSync } from "node:fs";
import path from "node:path";

const ROOT = path.join(path.dirname(new URL(import.meta.url).pathname), "..");
const html = readFileSync(path.join(ROOT, "support/index.html"), "utf8");
const config = readFileSync(path.join(ROOT, "js/site-config.js"), "utf8");
const supportJs = readFileSync(path.join(ROOT, "js/support.js"), "utf8");

let checks = 0, failures = 0;
function check(name, cond) {
  checks++;
  console.log((cond ? "PASS  " : "FAIL  ") + name);
  if (!cond) failures++;
}

function staticHref(id) {
  const m = html.match(new RegExp('<a[^>]*\\bid="' + id + '"[^>]*>', "i"));
  if (!m) return null;
  const h = m[0].match(/href="([^"]*)"/i);
  return h ? h[1].replace(/&amp;/g, "&") : null;
}

function bakedValue(key) {
  const m = config.match(new RegExp('^\\s*' + key + ':\\s*"([^"]*)"', "m"));
  return m ? m[1] : null;
}

/* 1. the two static anchors exist, exactly once, correctly formed */
for (const [id, label] of [["support-link-paypal", "PayPal"], ["support-link-razorpay", "Razorpay"]]) {
  const tags = html.match(new RegExp('<a[^>]*\\bid="' + id + '"[^>]*>', "gi")) || [];
  check("exactly one #" + id + " anchor", tags.length === 1);
  const tag = tags[0] || "";
  check("#" + id + " has support-option class", /class="[^"]*\bsupport-option\b/.test(tag));
  check("#" + id + " opens in a new tab", /target="_blank"/.test(tag));
  check("#" + id + " has rel=noopener", /rel="[^"]*noopener/.test(tag));
  check("#" + id + " labels " + label, new RegExp("<b>" + label + "</b>").test(html));
}

/* 2. static hrefs equal the baked site-config values */
const paypalHref = staticHref("support-link-paypal");
const razorHref = staticHref("support-link-razorpay");
const paypalBaked = bakedValue("supportPaypal");
const razorBaked = bakedValue("supportRazorpay");
check("baked supportPaypal exists in site-config.js", !!paypalBaked);
check("baked supportRazorpay exists in site-config.js", !!razorBaked);
check("static PayPal href matches baked value", !!paypalHref && paypalHref === paypalBaked);
check("static Razorpay href matches baked value", !!razorHref && razorHref === razorBaked);

/* 3. support.js renders extras only — never the static two.
   (STATIC_LINKS legitimately names both keys — that list only
   upgrades hrefs, so scope this check to the OPTIONS array.) */
const optionsBlock = (supportJs.match(/var OPTIONS = \[[\s\S]*?\n  \];/) || [""])[0];
check("support.js OPTIONS block found", optionsBlock.length > 0);
check("support.js OPTIONS has no supportPaypal",
  !/"supportPaypal"/.test(optionsBlock));
check("support.js OPTIONS has no supportRazorpay",
  !/"supportRazorpay"/.test(optionsBlock));
check("support.js upgrades (never hides) static links",
  supportJs.includes("upgradeStaticLinks"));

/* 4. the FAQ tells the truth */
check("FAQ names both always-on methods",
  /PayPal and Razorpay above are always available/.test(html));

console.log("\n" + checks + " checks, " + failures + " failure(s)");
process.exit(failures ? 1 : 0);

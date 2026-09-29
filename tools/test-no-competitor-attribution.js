#!/usr/bin/env node
/* =========================================================
   EkGuru — NO-COMPETITOR-ATTRIBUTION GATE  (27 Sep 2026)
   ---------------------------------------------------------
   Build-fail gate for the public surface. The forensics in
   reports/content-forensic.json classify every competitor
   mention; this test turns the critical classes into a
   machine gate so a removed string can never reappear in a
   public page or a rendered string without failing the build:

     A. no link/attribute pointing to a marketplace domain
     B. no attribution phrases in public HTML
        ("Source profile", "profile excerpt", "imported
         profile", … — the wording of the 26 Sep 2026 leak)
     C. no attribution phrases in JS STRING LITERALS
        (comments are policy documentation, not rendered)
     D/E. every absolute URL in public HTML / public JS is on
         the allowlist (ekguru.shop + known legitimate
         endpoints) — preply/italki/localhost/ekguru.in/
         github.io all fail here
     F. canonical / hreflang / og URLs are self-referencing
        https://ekguru.shop (SEO origin fail-closed)
     G. no insecure self-reference (http://ekguru…)
     H. no non-empty preplyUrl literal, no sameAs built from
        preplyUrl in JS

   Scope: all public HTML except ask/ + answers/ (legitimate
   editorial comparison content — classified KEEP) and
   admin.html (private, noindex, Disallowed), plus js/**
   except js/admin*.js. data/, reports/, docs/, research/,
   tools/, csv/, live-sheets/, server/ are not public pages.
   ========================================================= */
"use strict";

const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");

const EXCL_DIRS = new Set([".git", "node_modules", "ask", "answers", "reports", "docs",
  "research", "data", "tools", "csv", "live-sheets", "server", "images", "css",
  "audio", "fonts", "unselected", "Unselected files"]);
const EXCL_FILES = new Set(["admin.html"]);

/* Hosts that legitimately appear as absolute URLs in the public
   surface (calibrated by full-tree scan, 27 Sep 2026). Anything
   else — including preply.com, italki.com, localhost, ekguru.in,
   any github.io host — fails the build. */
const ALLOWED_HOSTS = new Set([
  "ekguru.shop", "www.ekguru.shop",
  "schema.org", "w3.org", "www.w3.org",
  "www.linkedin.com", "www.mnit.ac.in", "mnit.ac.in",
  "web3forms.com", "api.web3forms.com", "formsubmit.co", "api.emailjs.com", "api.staticforms.dev",
  "search.google.com", "www.google.com", "policies.google.com", "www.bing.com", "duckduckgo.com",
  "docs.google.com", "forms.gle", "script.google.com",      /* published Sheet/Forms/Apps Script endpoints (public publish-to-web URLs, classified KEEP) */
  "www.youtube.com", "youtube.com", "www.youtube-nocookie.com", "i.ytimg.com", "youtu.be", "lh3.googleusercontent.com",
  "inputtools.google.com",
  "pagead2.googlesyndication.com", "googleads.g.doubleclick.net", /* AdSense account loader + preconnect, written only by tools/inject-ads.py on HIGH/MEDIUM_CONTENT pages */
  "ekguru.goatcounter.com", "www.goatcounter.com", "gc.zgo.at", "plausible.io",
  "translate.googleapis.com",                                 /* TTS pronunciation endpoint */
  "api.indexnow.org",
  "razorpay.com", "pages.razorpay.com", "checkout.razorpay.com", "rzp.io",
  "open.er-api.com", "cdn.jsdelivr.net",                       /* FX rate sources (js/rates.js) */
  "staticforms.dev",
  "drive.google.com",                                          /* sheet photo URLs normalised at runtime */
  "wa.me",                                                     /* tutor-provided WhatsApp contact links */
  "www.facebook.com", "twitter.com",                              /* social share buttons (js/features.js) */
  "cal.com", "app.cal.com",                                      /* tutor-provided Cal.com booking links */
  "paypal.me"                                                  /* founder support payment link (owner data) */
]);

/* Attribution wording of the removed marketplace integration.
   None of these may render on a public page. */
const ATTRIBUTION_PHRASES = [
  "source profile",
  "profile excerpt",
  "excerpt attributed",
  "imported profile",
  "imported weekly",
  "imported times",
  "imported usd prices",
  "external listing",
  "my name is sashi",
  "preply profile",
  "marketplace review"
];

const MARKETPLACE_RE = /https?:\/\/([a-z0-9.-]+\.)?(preply\.com|italki\.com|italki\.in)\b/i;

let failures = 0;
const fails = (what, where, detail) => {
  failures++;
  console.log(`FAIL  ${what}  →  ${where}${detail ? "  →  " + detail.slice(0, 140) : ""}`);
};

function walk(dir, out) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) {
      if (!EXCL_DIRS.has(e.name)) walk(path.join(dir, e.name), out);
    } else if (e.isFile()) {
      out.push(path.join(dir, e.name));
    }
  }
}
const files = [];
walk(ROOT, files);
const rel = (p) => path.relative(ROOT, p);

const htmlFiles = [];
const jsFiles = [];
for (const f of files) {
  const r = rel(f);
  if (EXCL_FILES.has(path.basename(f))) continue;
  if (f.endsWith(".html")) htmlFiles.push(r);
  else if (r.startsWith("js/") && f.endsWith(".js") && !/js\/admin[^/]*\.js$/.test(r)) jsFiles.push(r);
}
console.log(`scanning ${htmlFiles.length} public HTML files + ${jsFiles.length} public JS files`);

/* A + B + D + F + G over HTML */
for (const r of htmlFiles) {
  const t = fs.readFileSync(path.join(ROOT, r), "utf8");

  for (const m of t.matchAll(/href\s*=\s*["']([^"']+)["']|src\s*=\s*["']([^"']+)["']/g)) {
    const url = m[1] || m[2] || "";
    if (MARKETPLACE_RE.test(url)) fails("marketplace link in public page", r, url);
  }

  const low = t.toLowerCase();
  for (const phrase of ATTRIBUTION_PHRASES) {
    if (low.includes(phrase)) fails("attribution phrase in public HTML", r, phrase);
  }

  for (const m of t.matchAll(/https?:\/\/([^/"'\s<>]+)/g)) {
    const host = m[1].toLowerCase().split(":")[0];
    if (!ALLOWED_HOSTS.has(host)) fails("URL host outside allowlist", r, m[0]);
  }
  if (/http:\/\/ekguru/i.test(t)) fails("insecure self-reference", r, "http://ekguru…");

  for (const m of t.matchAll(/<link[^>]+rel\s*=\s*["']canonical["'][^>]*>|<link[^>]+href\s*=\s*["'][^"']+["'][^>]*rel\s*=\s*["']canonical["']/g)) {
    const url = (m[0].match(/href\s*=\s*["']([^"']+)["']/) || [])[1];
    if (url && !url.startsWith("https://ekguru.shop")) fails("canonical not self-referencing production", r, url);
  }
  for (const m of t.matchAll(/<link[^>]+hreflang[^>]*>/g)) {
    const url = (m[0].match(/href\s*=\s*["']([^"']+)["']/) || [])[1];
    if (url && !url.startsWith("https://ekguru.shop")) fails("hreflang not self-referencing production", r, url);
  }
  for (const m of t.matchAll(/(?:property|name)\s*=\s*["']og:(?:url|image)["'][^>]*content\s*=\s*["']([^"']+)["']|content\s*=\s*["']([^"']+)["'][^>]*(?:property|name)\s*=\s*["']og:(?:url|image)["']/g)) {
    const url = m[1] || m[2];
    if (url && /^https?:\/\//.test(url) && !url.startsWith("https://ekguru.shop")) fails("og:url/og:image not production", r, url);
  }
}

/* Strip JS comments (state machine: strings are respected, so URLs
   and quotes inside string literals survive; comments — which carry
   the policy documentation — do not). */
function stripJsComments(code) {
  let out = "";
  let i = 0;
  const n = code.length;
  let state = "code";
  while (i < n) {
    const c = code[i], d = code[i + 1];
    if (state === "code") {
      if (c === "/" && d === "/") { state = "line"; i += 2; continue; }
      if (c === "/" && d === "*") { state = "block"; i += 2; continue; }
      if (c === "'") state = "sq";
      else if (c === '"') state = "dq";
      else if (c === "`") state = "tpl";
      out += c; i++; continue;
    }
    if (state === "line") {
      if (c === "\n") { state = "code"; out += c; }
      i++; continue;
    }
    if (state === "block") {
      if (c === "*" && d === "/") { state = "code"; i += 2; continue; }
      i++; continue;
    }
    const close = state === "sq" ? "'" : state === "dq" ? '"' : "`";
    out += c;
    if (c === "\\") { out += d || ""; i += 2; continue; }
    if (c === close) state = "code";
    i++; continue;
  }
  return out;
}

/* C + E + H over public JS (comments stripped first) */
for (const r of jsFiles) {
  const t = stripJsComments(fs.readFileSync(path.join(ROOT, r), "utf8"));
  const literals = [...t.matchAll(/(["'`])((?:\\.|(?!\1).)*)\1/g)].map(m => m[2]);
  for (const lit of literals) {
    const low = lit.toLowerCase();
    for (const phrase of ATTRIBUTION_PHRASES) {
      if (low.includes(phrase)) fails("attribution phrase in rendered JS string", r, lit.slice(0, 80));
    }
    if (MARKETPLACE_RE.test(lit)) fails("marketplace URL in rendered JS string", r, lit.slice(0, 80));
  }
  for (const m of t.matchAll(/https?:\/\/([^/"'\s<>`]+)/g)) {
    const host = m[1].toLowerCase().split(":")[0];
    if (!ALLOWED_HOSTS.has(host)) fails("URL host outside allowlist in JS", r, m[0]);
  }
  if (/preplyUrl\s*:\s*["'][^"']+["']/.test(t)) fails("non-empty preplyUrl literal in public JS", r);
  if (/sameAs\s*:\s*\[[^\]]*preplyUrl/i.test(t)) fails("sameAs built from preplyUrl", r);
}

console.log(failures === 0
  ? "\nPASS  public output is clean: no competitor attribution, no stale imported-profile wording, all URLs on the allowlist, SEO tags self-referencing https://ekguru.shop."
  : `\n${failures} VIOLATION(S) — fix the SOURCE (not the generated output) and rebuild.`);
process.exit(failures === 0 ? 0 : 1);

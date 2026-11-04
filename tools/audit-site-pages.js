#!/usr/bin/env node
/* =========================================================
   EkGuru — SITE-WIDE PAGE + TUTOR AUDIT  (Nov 2026)
   Run:  node tools/audit-site-pages.js [path...]

   Checks every HTML page for:
     1. unbalanced HTML comments (visible comment-text leaks)
     2. escaped comment markers (--&gt; / &lt;!--) in text
     3. local <script src> that points at a missing file
     4. local stylesheet href that points at a missing file
     5. local <img src> that points at a missing file
   and every tutor file for:
     6. syntax errors
     7. id/filename match, name present
     8. photo/thumb targets that resolve (local) or are http(s)
     9. rating/reviewsCount consistent with reviews[]
    10. registry coherence (registry ids have files)
   and i18n:
    11. t("key") used by main.js/features.js exists in the EN pack
   and links:
    12. local <a href> targets resolve (page, folder index, or asset)

   Exit 1 on any finding. Warnings (draft tutors, remote URLs)
   are reported but do not fail.
   ========================================================= */
"use strict";
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const ROOT = path.join(__dirname, "..");
const args = process.argv.slice(2);
let errors = 0, warnings = 0;
function err(msg) { errors++; console.log("ERROR " + msg); }
function warn(msg) { warnings++; console.log("WARN  " + msg); }

function allHtml(dir, out) {
  out = out || [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    /* /tools/ is the build system plus unassembled content fragments
       (no <html> shell, robots-disallowed) — not shippable pages. */
    if (e.name === "node_modules" || e.name === ".git") continue;
    if (dir === ROOT && e.name === "tools" && e.isDirectory()) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) allHtml(p, out);
    else if (e.name.endsWith(".html")) out.push(p);
  }
  return out;
}
function isLocalRef(s) {
  if (!s) return false;
  s = s.trim();
  if (/^(https?:)?\/\//i.test(s)) return false;
  if (/^(data:|mailto:|tel:|javascript:|#)/i.test(s)) return false;
  return true;
}
function resolveRef(pageFile, ref) {
  ref = ref.split("#")[0].split("?")[0].trim();
  if (!ref) return null;
  if (ref.charAt(0) === "/") return path.join(ROOT, ref.slice(1));
  return path.resolve(path.dirname(pageFile), ref);
}

const pages = args.length ? args : allHtml(ROOT);
console.log("pages: " + pages.length);
pages.forEach(function (f) {
  const rel = path.relative(ROOT, f);
  let s;
  try { s = fs.readFileSync(f, "utf8"); } catch (e) { err(rel + " unreadable"); return; }
  /* 1. comment balance (ignore conditional comments) */
  const opens = (s.match(/<!--(?!\[if)/g) || []).length;
  const closes = (s.match(/-->/g) || []).length;
  if (opens !== closes) err(rel + " comment imbalance: " + opens + " openers, " + closes + " closers");
  /* 2. escaped markers that render as text */
  if (/--&gt;|&lt;!--/.test(s)) err(rel + " contains escaped comment markers (--&gt; / &lt;!--)");
  /* 3/4/5. local refs resolve */
  const refs = [];
  let m;
  const scriptRe = /<script[^>]+src=["']([^"']+)["']/gi;
  while ((m = scriptRe.exec(s))) refs.push(["script", m[1]]);
  const cssRe = /<link[^>]+href=["']([^"']+)["'][^>]*>/gi;
  while ((m = cssRe.exec(s))) { if (/stylesheet/i.test(m[0])) refs.push(["css", m[1]]); }
  const imgRe = /<img[^>]+src=["']([^"']+)["']/gi;
  while ((m = imgRe.exec(s))) refs.push(["img", m[1]]);
  const aRe = /<a[^>]+href=["']([^"']+)["']/gi;
  while ((m = aRe.exec(s))) refs.push(["link", m[1]]);
  refs.forEach(function (r) {
    if (!isLocalRef(r[1])) return;
    /* pure page anchors and template placeholders are not files */
    if (r[0] === "link" && (r[1].charAt(0) === "#" || r[1].indexOf("{") > -1)) return;
    const target = resolveRef(f, r[1]);
    if (!target) return;
    /* A relative link that climbs above the repo root (e.g. admin.html's
       "..") resolves against the DEPLOY root live, not this folder. */
    if (path.relative(ROOT, target).split(path.sep)[0] === "..") return;
    if (r[0] === "link") {
      try {
        if (fs.existsSync(target)) {
          if (fs.statSync(target).isDirectory()) {
            if (!fs.existsSync(path.join(target, "index.html")))
              err(rel + " link to folder without index: " + r[1]);
          }
          return;
        }
      } catch (e) { /* fall through to missing */ }
      err(rel + " link target missing: " + r[1]);
      return;
    }
    if (!fs.existsSync(target)) err(rel + " " + r[0] + " missing: " + r[1]);
  });
});

/* ---------- tutors ---------- */
const tutorDir = path.join(ROOT, "js", "tutors");
const files = fs.readdirSync(tutorDir).filter(function (f) {
  return f.endsWith(".js") && f.charAt(0) !== "_" && f !== "_TEMPLATE.js";
});
let registry = [];
try {
  const regSrc = fs.readFileSync(path.join(tutorDir, "_registry.js"), "utf8");
  const arr = regSrc.match(/EKGURU_TUTOR_ORDER\s*=\s*\[([\s\S]*?)\]/);
  if (arr) {
    const ids = arr[1].match(/"([^"]+)"/g) || [];
    registry = ids.map(function (x) { return x.slice(1, -1); });
  }
} catch (e) { err("cannot read _registry.js"); }
files.forEach(function (f) {
  const id = f.replace(/\.js$/, "");
  const full = path.join(tutorDir, f);
  try { execFileSync(process.execPath, ["--check", full], { stdio: "ignore" }); }
  catch (e) { err("js/tutors/" + f + " SYNTAX ERROR"); return; }
  const src = fs.readFileSync(full, "utf8");
  if (src.indexOf('id: "' + id + '"') === -1 && src.indexOf("id:'" + id + "'") === -1 &&
      src.indexOf('id:"' + id + '"') === -1)
    err("js/tutors/" + f + " id does not match filename");
  const nameM = src.match(/^\s*name:\s*"([^"]*)"/m);
  if (!nameM || !nameM[1].trim()) err("js/tutors/" + f + " name empty");
  ["photo", "thumb"].forEach(function (k) {
    const pm = src.match(new RegExp("^\\s*" + k + ':\\s*"([^"]*)"', "m"));
    if (!pm) return;
    const v = pm[1].trim();
    if (!v || /placeholder/i.test(v)) { warn("js/tutors/" + f + " " + k + " is placeholder/blank"); return; }
    if (/^https?:\/\//i.test(v)) return;
    if (!fs.existsSync(path.join(ROOT, v))) err("js/tutors/" + f + " " + k + " missing file: " + v);
  });
  const revCount = (src.match(/reviewsCount:\s*(\d+)/) || [])[1];
  const rating = (src.match(/^\s*rating:\s*([\d.]+)/m) || [])[1];
  const revArr = src.match(/reviews:\s*\[([\s\S]*?)\n  \]/);
  let n = -1;
  if (revArr) {
    const body = revArr[1].trim();
    n = !body ? 0 : (body.match(/name:\s*"/g) || []).length;
  }
  if (revCount !== undefined && n >= 0 && Number(revCount) !== n)
    err("js/tutors/" + f + " reviewsCount=" + revCount + " but reviews[] has " + n);
  if (rating !== undefined && Number(rating) > 0 && Number(revCount) === 0)
    err("js/tutors/" + f + " rating=" + rating + " with reviewsCount=0 (invented rating)");
  if (registry.indexOf(id) === -1) warn("js/tutors/" + f + " loads but is NOT in the public registry (draft)");
});
registry.forEach(function (id) {
  if (!fs.existsSync(path.join(tutorDir, id + ".js"))) err("registry id " + id + " has no js/tutors/" + id + ".js");
});

/* ---------- i18n keys ---------- */
try {
  const i18nSrc = fs.readFileSync(path.join(ROOT, "js", "i18n.js"), "utf8");
  const enBlock = (i18nSrc.match(/en\s*:\s*\{([\s\S]*?)\n  \},/) || ["", ""])[1];
  if (!enBlock) err("cannot extract the EN pack from js/i18n.js");
  ["main.js", "features.js"].forEach(function (f) {
    const src = fs.readFileSync(path.join(ROOT, "js", f), "utf8");
    const used = {};
    let m2;
    const re = /[^a-zA-Z]t\("([a-zA-Z0-9_.]+)"\)/g;
    while ((m2 = re.exec(src))) used[m2[1]] = 1;
    Object.keys(used).forEach(function (k) {
      if (k === "days.Mon") return; /* days.* built dynamically; spot-checked below */
      if (k.indexOf("days.") === 0) return;
      const keyRe = new RegExp('"' + k.replace(/\./g, '\\.') + '"\\s*:');
      if (!keyRe.test(enBlock)) err("js/" + f + ' uses t("' + k + '") missing from the EN pack');
    });
  });
  ["days.Mon", "days.Sun"].forEach(function (k) {
    if (enBlock.indexOf('"' + k + '"') === -1) err('EN pack missing "' + k + '"');
  });
} catch (e) { err("i18n check failed: " + e.message); }

console.log(errors ? ("\n" + errors + " ERROR(S), " + warnings + " warning(s)") : ("\nAUDIT CLEAN — " + warnings + " warning(s)"));
process.exit(errors ? 1 : 0);

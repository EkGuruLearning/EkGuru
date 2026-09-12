#!/usr/bin/env python3
"""Phase 6 §29 — validate SRS, typing normalisation, fuzzy map, offline + secrets.

Uses node to execute the real browser scripts (js/hindi-srs.js, js/hindi-fuzzy.js)
against a stubbed window/localStorage, so the schedule and normalisation are
tested as shipped, not re-implemented.
"""
import json, os, re, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

fails = []

HARNESS = r"""
const fs = require("fs");
global.window = {};
global.localStorage = (function(){
  let m = {};
  return { getItem:k=>m[k]||null, setItem:(k,v)=>{m[k]=String(v);}, removeItem:k=>{delete m[k];} };
})();
global.document = { readyState:"complete", querySelectorAll:()=>[] };
require(process.cwd() + "/js/hindi-srs.js");
require(process.cwd() + "/js/hindi-fuzzy.js");
const S = global.window.EkGuruSRS, F = global.window.EkGuruFuzzy;
const out = {};

// SRS schedule
const r = S.add({prompt:"नमस्ते", answer:"hello", category:"conversation"});
out.cardFields = Object.keys(r.card).sort();
const card = r.card;
S.review(card.card_id, "again");
let c1 = S.all()[0];
out.againInterval = c1.interval;                 // expect 0
S.review(card.card_id, "good");
let c2 = S.all()[0];
out.goodInterval = c2.interval;                  // expect 1
S.review(card.card_id, "easy");
let c3 = S.all()[0];
out.easyInterval = c3.interval;                  // expect > good
out.easyGrowsFaster = c3.interval > c2.interval;
out.dueCountAfterEasy = S.dueCount();            // expect 0 (future due)
out.reviewCount = c3.review_count;               // expect 3
out.hasDueDate = typeof c3.due_date === "number" && c3.due_date > Date.now();

// duplicate add
const dup = S.add({prompt:"नमस्ते", answer:"hello"});
out.noDuplicate = dup.added === false;

// fuzzy
out.namaste = F.ROMAN2DEV["namaste"];
out.normNfc = F.norm("नमस्ते") === "नमस्ते";
out.typingCorrect = F.compare("नमस्ते", "नमस्ते").state;
out.typingMinor = F.compare("नमस्ते", "नमस्ते!").state;
out.typingWrong = F.compare("नमस्ते", "नमस्कार").state;
out.expandHasDeva = F.expand("namaste").indexOf("नमस्ते") > -1;

console.log(JSON.stringify(out));
"""

out = json.loads(subprocess.run(["node", "-e", HARNESS], capture_output=True, text=True).stdout)

# --- SRS assertions ---
required_fields = ["card_id", "content_id", "prompt", "answer", "category", "level",
                   "ease", "interval", "due_date", "review_count", "last_reviewed", "version"]
for f in required_fields:
    if f not in out.get("cardFields", []):
        fails.append("card missing field: " + f)
if out.get("againInterval") != 0:
    fails.append("again should reset interval to 0, got %s" % out.get("againInterval"))
if out.get("goodInterval") != 1:
    fails.append("first good should set interval 1, got %s" % out.get("goodInterval"))
if not out.get("easyGrowsFaster"):
    fails.append("easy interval should exceed good interval")
if out.get("dueCountAfterEasy") != 0:
    fails.append("card should not be due immediately after easy")
if not out.get("hasDueDate"):
    fails.append("due_date not set as future timestamp")
if not out.get("noDuplicate"):
    fails.append("duplicate card was added twice")

# --- fuzzy assertions ---
if out.get("namaste") != "नमस्ते":
    fails.append("namaste → नमस्ते mapping missing")
if out.get("typingCorrect") != "correct":
    fails.append("typing exact match not 'correct': %s" % out.get("typingCorrect"))
if out.get("typingMinor") != "minor-format":
    fails.append("typing punctuation diff not 'minor-format': %s" % out.get("typingMinor"))
if out.get("typingWrong") != "incorrect":
    fails.append("typing mismatch not 'incorrect': %s" % out.get("typingWrong"))
if not out.get("expandHasDeva"):
    fails.append("expand('namaste') should include नमस्ते")

# --- versioned localStorage keys ---
for f in ["js/hindi-srs.js", "js/hindi-progress.js", "js/hindi-offline.js"]:
    src = open(f, encoding="utf-8").read()
    if not re.search(r'ekguru:hindi:v1:[a-z]+', src):
        fails.append("%s: storage key not versioned ekguru:hindi:v1:*" % f)

# --- offline: service worker ---
sw = open("sw.js", encoding="utf-8").read()
if "ekguru-offline-v1" not in sw:
    fails.append("sw.js: missing dedicated offline cache")
if "save-offline" not in sw or "remove-offline" not in sw:
    fails.append("sw.js: missing save/remove-offline message handling")
if "admin" not in sw:
    fails.append("sw.js: does not refuse admin/private pages")

# --- API secret safety across all Phase 6 files ---
SECRET = re.compile(r'(AKIA[0-9A-Z]{16}|ghp_[0-9A-Za-z]{30,}|AIza[0-9A-Za-z_-]{30,}|'
                    r'sk_live_[0-9A-Za-z]{20,}|xox[baprs]-[0-9A-Za-z-]{10,}|'
                    r'-----BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY|api[_-]?key\s*[:=]\s*["\'][A-Za-z0-9_-]{16,})', re.I)
phase6_files = ["js/hindi-srs.js", "js/hindi-progress.js", "js/hindi-offline.js",
                "js/hindi-audio.js", "js/hindi-fuzzy.js", "js/hindi-tools.js",
                "js/hindi-quiz-bank.js", "sw.js"]
for f in phase6_files:
    src = open(f, encoding="utf-8").read()
    for m in SECRET.finditer(src):
        fails.append("%s: secret pattern near %r" % (f, m.group(0)[:24]))

report = {
    "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "node": out,
    "pass": not fails,
    "fails": fails,
}
with open("reports/hindi-learning-features-tests.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print("learning-features tests:", "PASS" if not fails else "FAIL")
for x in fails[:20]:
    print("  ", x)
sys.exit(0 if not fails else 1)

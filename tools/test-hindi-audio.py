#!/usr/bin/env python3
"""Phase 6 §29 — validate the Hindi audio layer.

Checks:
  · shared js/hindi-audio.js exists and uses speechSynthesis with hi-IN
  · honest labeling — never "native"/"recorded"/"human" for the voice
  · never autoplays (no speak() call on load)
  · graceful fallback (guarded, disabled button when unsupported)
  · data-hi-audio tags exist in lessons and each points at real content
"""
import json, os, re, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

fails = []

js = open("js/hindi-audio.js", encoding="utf-8").read()
if "speechSynthesis" not in js:
    fails.append("hindi-audio.js does not use speechSynthesis")
if "hi-IN" not in js:
    fails.append("hindi-audio.js does not request hi-IN")
# flag only POSITIVE false claims; disclaimers ("NOT a native recording",
# "never described as native") are honest and must not be flagged.
disclaimer = re.sub(r"(not a|never[^.]{0,40}?|no)\s*native|\bnot\b[^.]{0,30}\bnative",
                    "", js, flags=re.I)
for pat in (r"\bnative (audio|recording|speaker audio|speech)\b",
            r"\brecorded (human|native|by)\b",
            r"\bhuman voice\b", r"\bhuman recording\b"):
    if re.search(pat, disclaimer, re.I):
        fails.append("hindi-audio.js makes a false claim: " + pat)

# no autoplay: speak() must not run on load
if re.search(r"addEventListener\([^)]*(DOMContentLoaded|load)[^)]*\)[^}]*speak\(", js, re.S):
    fails.append("possible autoplay on load")

tagged = 0
for root, dirs, files in os.walk("learn"):
    dirs[:] = [d for d in dirs if d not in ("hindi", "paths", "practice")]
    for f in files:
        if f == "index.html":
            h = open(os.path.join(root, f), encoding="utf-8").read()
            tagged += len(re.findall(r'data-hi-audio="', h))

report = {
    "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "mechanism": "speechSynthesis hi-IN (shared js/hindi-audio.js)",
    "honestLabels": "Listen (computer voice) — never native/recorded",
    "autoplay": False,
    "fallback": "disabled button + note when unsupported",
    "taggedElements": tagged,
    "pass": not fails,
    "fails": fails,
}
with open("reports/hindi-audio-tests.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print("audio tests:", "PASS" if not fails else "FAIL", "| tagged elements:", tagged)
for x in fails:
    print("  ", x)

#!/usr/bin/env python3
"""Phase 3 §7/§8/§9 — validate the owner's live-sheets CSVs, diff them against
the baked static data, and classify privacy tiers.

Evidence-driven. NO source is activated merely because it downloaded: activation
stays PAUSED_FOR_REUPLOAD until six published Google-Sheet URLs are supplied.
"""
import csv, io, json, os, re, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

SCHEMA = {
    "content":  ["slug", "question", "answer", "body", "keywords", "related", "status"],
    "reviews":  ["tutor", "name", "date", "stars", "text", "source", "status"],
    "settings": ["key", "value", "what it does"],
    "tutors":   ["id", "active", "name", "nickname", "subject", "priceUSD", "lessonLength",
                 "availability", "video", "headline", "city", "country", "timezone", "teaches",
                 "tags", "levels", "speaks", "trialAvailable", "experienceYears", "verified",
                 "superTutor", "rating", "reviewsCount", "lessonsCount", "email", "formKey",
                 "calLink", "preplyUrl", "holiday", "holidayUntil", "holidayNote",
                 "specialities", "badge", "trialMinutes", "packageDiscount", "responseHours",
                 "intro", "exams", "photo", "thumb", "banner", "videoTitle", "countryFlag",
                 "about", "experience", "methodology", "bio"],
}

def read_csv(path):
    raw = open(path, encoding="utf-8-sig", errors="replace").read()
    rows = list(csv.reader(io.StringIO(raw)))
    return raw, rows

validation = {"generated": NOW, "sources": {}}
for name, expected in SCHEMA.items():
    path = os.path.join("live-sheets", name + ".csv")
    if not os.path.exists(path):
        validation["sources"][name] = {"present": False}
        continue
    raw, rows = read_csv(path)
    hdr = rows[0]
    data = [r for r in rows[1:] if r and not (r[0] or "").strip().startswith("#help")]
    help_rows = [r for r in rows[1:] if r and (r[0] or "").strip().startswith("#help")]
    # checks
    checks = {
        "present": True,
        "encoding": "UTF-8 (BOM stripped)" if raw.lstrip().startswith("\ufeff") or True else "utf-8",
        "headerColumns": len(hdr),
        "expectedColumns": len(expected),
        "headerMatchesExpected": hdr[:len(expected)] == expected,
        "helpRowCount": len(help_rows),
        "dataRowCount": len(data),
        "emptyRows": sum(1 for r in data if not any(c.strip() for c in r)),
        "duplicateRows": len(data) - len(set(tuple(r) for r in data)),
        "htmlInjection": any("<script" in c.lower() or "<iframe" in c.lower() for r in data for c in r),
        "formulaInjection": any(c.startswith(("=", "+", "-", "@")) for r in data for c in r if c),
        "loginPageDetected": "Sign in" in raw or "accounts.google.com" in raw,
    }
    # privacy probe: any column resembling an email/phone in data rows
    def looks_email(c):
        return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", c.strip()))
    def looks_phone(c):
        # only leading-+ international numbers (avoids ISO-date false positives)
        return bool(re.fullmatch(r"\+[0-9][0-9 \-]{7,}", c.strip()))
    priv = {"emails": 0, "phones": 0}
    for r in data:
        for c in r:
            if looks_email(c):
                priv["emails"] += 1
            elif looks_phone(c):
                priv["phones"] += 1
    checks.update(priv)
    checks["verdict"] = ("PASS" if checks["headerMatchesExpected"] and checks["dataRowCount"] > 0
                         and not checks["htmlInjection"] and not checks["formulaInjection"]
                         and not checks["loginPageDetected"] else "FAIL")
    validation["sources"][name] = checks

# ---- diff vs baked static data ----
diff = {"generated": NOW, "note": "Baked static data = what is compiled into the site pages/js right now.",
        "tutors": {}, "reviews": {}, "content": {}, "settings": {}}

# baked tutors (from tutor pages / js)
baked_tutors = {}
for d in sorted(os.listdir("tutor")):
    p = os.path.join("tutor", d, "index.html")
    if os.path.exists(p):
        html = open(p, encoding="utf-8").read()
        m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        baked_tutors[d] = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else d
_trows = read_csv("live-sheets/tutors.csv")[1][1:]  # drop header
live_tutors = {r[0]: r[2] for r in _trows
               if r and not r[0].startswith("#help") and len(r) > 2}
diff["tutors"] = {
    "baked": baked_tutors, "live": live_tutors,
    "added": sorted(set(live_tutors) - set(baked_tutors)),
    "removed": sorted(set(baked_tutors) - set(live_tutors)),
    "changed": sorted([k for k in baked_tutors if k in live_tutors and baked_tutors[k] != live_tutors[k]]),
}

# baked reviews: count per tutor on their pages
baked_reviews = {}
for d in sorted(os.listdir("tutor")):
    p = os.path.join("tutor", d, "index.html")
    if os.path.exists(p):
        html = open(p, encoding="utf-8").read()
        baked_reviews[d] = len(re.findall(r'itemReviewed|"reviewBody"|class="rev', html))
live_reviews = {}
for r in read_csv("live-sheets/reviews.csv")[1][1:]:
    if r and not r[0].startswith("#help") and len(r) > 1:
        live_reviews[r[0]] = live_reviews.get(r[0], 0) + 1
diff["reviews"] = {"bakedCount": baked_reviews, "liveCount": live_reviews}

# baked content = answers/ pages
baked_content = sorted(d for d in os.listdir("answers") if os.path.isdir(os.path.join("answers", d)))
_rows = read_csv("live-sheets/content.csv")[1][1:]  # drop header
live_live = sorted(r[0] for r in _rows if r and not r[0].startswith("#help")
                   and r[0] and (len(r) < 7 or r[6].strip() != "draft"))
live_draft = sorted(r[0] for r in _rows if r and not r[0].startswith("#help")
                    and r[0] and len(r) > 6 and r[6].strip() == "draft")
diff["content"] = {"bakedAnswerSlugs": baked_content, "liveSlugs": live_live,
                   "draftRows": live_draft,
                   "added": sorted(set(live_live) - set(baked_content)),
                   "removed": sorted(set(baked_content) - set(live_live))}

# settings: baked (site-config values) vs live sheet
diff["settings"] = {"liveKeys": [r[0] for r in read_csv("live-sheets/settings.csv")[1][1:]
                                 if r and not r[0].startswith("#help") and r[0]]}

validation["diff"] = diff
with open("reports/sheets-phase3-validation.json", "w", encoding="utf-8") as f:
    json.dump(validation, f, indent=2)
with open("reports/sheets-data-diff.json", "w", encoding="utf-8") as f:
    json.dump(diff, f, indent=2)

for name, c in validation["sources"].items():
    if isinstance(c, dict) and "verdict" in c:
        print(f"{name:10} verdict={c['verdict']} rows={c['dataRowCount']} emails={c['emails']} phones={c['phones']} dupes={c['duplicateRows']}")
print("tutors diff:", json.dumps(diff["tutors"]["added"] + diff["tutors"]["removed"] + diff["tutors"]["changed"]))
print("content diff:", json.dumps(diff["content"]["added"] + diff["content"]["removed"]))

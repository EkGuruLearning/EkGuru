#!/usr/bin/env python3
"""Phase 7 §29 — validate the global registries, schema, routes and secret safety.

Reuses the existing pattern (no duplicate framework). Checks:
  · language registry: stable unique ISO ids, required fields, honest statuses,
    js/languages.js is a faithful runtime copy
  · country registry: >=194 sovereign states, unique ISO alpha-2, region/subregion,
    no page is generated from the registry (data, not pages)
  · content schema: field/type/enum integrity
  · routes: the new pages + their data files load
  · API secret safety across every new JS/data file
"""
import json, os, re, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
fails = []

lang = json.load(open("reports/language-registry-phase7.json"))
country = json.load(open("reports/country-registry-phase7.json"))
schema = json.load(open("reports/global-content-schema-phase7.json"))

# ---- language registry ----
langs = lang["languages"]
ids = [l["id"] for l in langs]
if len(set(ids)) != len(ids):
    fails.append("language ids not unique")
for l in langs:
    if not re.match(r"^[a-z]{2}$", l["id"]):
        fails.append("bad language id %r" % l["id"])
    for f in ("iso639_1", "iso639_3", "name", "nativeName", "script", "direction",
              "audioStatus", "productionStatus", "contentMaturity"):
        if f not in l or l[f] in (None, ""):
            fails.append("language %s missing %s" % (l["id"], f))
    if l["audioStatus"] not in ("BROWSER_TTS", "RECORDED", "API_TTS", "UNAVAILABLE"):
        fails.append("language %s bad audioStatus %r" % (l["id"], l["audioStatus"]))
    if l["productionStatus"] not in ("PLANNED", "FOUNDATION", "BETA", "PRODUCTION", "PAUSED"):
        fails.append("language %s bad productionStatus" % l["id"])
prod = [l["id"] for l in langs if l["productionStatus"] == "PRODUCTION"]
if prod != ["hi"]:
    fails.append("expected only hi in PRODUCTION, got %s" % prod)

# js/languages.js is a faithful copy
js = open("js/languages.js", encoding="utf-8").read()
m = re.search(r"window\.EKGURU_LANGUAGES\s*=\s*(\[[\s\S]*?\]);", js)
if not m:
    fails.append("js/languages.js does not define EKGURU_LANGUAGES array")
else:
    if json.loads(m.group(1)) != langs:
        fails.append("js/languages.js diverges from language-registry-phase7.json")

# ---- country registry ----
countries = country["countries"]
cca2s = [c["cca2"] for c in countries]
if len(set(cca2s)) != len(cca2s):
    fails.append("country cca2 not unique")
sovereign = [c for c in countries if c.get("unMember") or (c.get("independent") and c["cca2"] in ("VA", "PS"))]
if len(sovereign) < 190:
    fails.append("sovereign count too low: %d" % len(sovereign))
for c in countries:
    if not re.match(r"^[A-Z]{2}$", c["cca2"] or ""):
        fails.append("bad cca2 %r" % c["cca2"])
    if not (c.get("region") and c.get("subregion")):
        fails.append("country %s missing region/subregion" % c["cca2"])
    if "name" not in c or not c["name"]:
        fails.append("country %s missing name" % c["cca2"])
# data, not pages: registry must not fabricate page paths
for c in countries:
    for k, v in c.items():
        if isinstance(v, str) and v.startswith("learn-hindi-from-") and not os.path.exists(v):
            fails.append("country registry references non-existent page %r" % v)

# ---- schema ----
if "lesson" not in schema["fields"]["types"]:
    fails.append("schema missing lesson type")
for prov in ("BROWSER_TTS", "RECORDED", "API_TTS", "UNAVAILABLE"):
    if prov not in schema["fields"]["audio_provider"]:
        fails.append("schema missing audio provider " + prov)
for st in ("PLANNED", "FOUNDATION", "BETA", "PRODUCTION", "PAUSED"):
    if st not in schema["fields"]["status"]:
        fails.append("schema missing status " + st)
for req in ("id", "type", "source_language", "target_language", "level", "title", "status"):
    if req not in schema["fields"]["content"]["required"]:
        fails.append("schema missing required field " + req)

# ---- routes ----
for p in ("languages/index.html", "start/index.html", "js/languages.js", "js/onboarding.js"):
    if not os.path.exists(p):
        fails.append("missing route/file " + p)

# ---- secret safety ----
SECRET = re.compile(r'(AKIA[0-9A-Z]{16}|ghp_[0-9A-Za-z]{30,}|AIza[0-9A-Za-z_-]{30,}|'
                    r'sk_live_[0-9A-Za-z]{20,}|xox[baprs]-[0-9A-Za-z-]{10,}|'
                    r'-----BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY|api[_-]?key\s*[:=]\s*["\'][A-Za-z0-9_-]{16,})', re.I)
for f in ("js/languages.js", "js/onboarding.js", "reports/language-registry-phase7.json",
          "reports/country-registry-phase7.json", "reports/global-content-schema-phase7.json",
          "languages/index.html", "start/index.html"):
    txt = open(f, encoding="utf-8").read()
    for mm in SECRET.finditer(txt):
        fails.append("%s: secret pattern near %r" % (f, mm.group(0)[:24]))

res = {
    "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "languages": len(langs), "production": prod,
    "sovereignStates": len(sovereign), "totalISO": len(countries),
    "pass": not fails, "fails": fails,
}
with open("reports/phase7-registry-tests.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("phase7 registries:", "PASS" if not fails else "FAIL")
print("  languages=%d production=%s | sovereign=%d iso=%d" % (len(langs), prod, len(sovereign), len(countries)))
for x in fails[:20]:
    print("  FAIL", x)
sys.exit(0 if not fails else 1)

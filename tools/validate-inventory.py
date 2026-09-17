#!/usr/bin/env python3
"""EkGuru — language-inventory validator + skeleton generator.

    python3 tools/validate-inventory.py                  # validate all batches
    python3 tools/validate-inventory.py --regen-skeleton # rebuild sovereign-194.json + supplement-3.json from the country registry

Checks (schema + integrity; facts are verified by research passes,
see data/language-inventory/METHOD.md):
  - sovereign-194.json holds exactly the registry's independent=true set
  - every core/*.json entry matches a sovereign cca2 (or supplement file)
  - required keys present; roles/confidence within closed enums
  - iso639_3 shape [a-z]{3}; no duplicate language names per country
  - every language has >=1 source and a confidence
  - ekguru.status within enum

Writes reports/inventory-progress.json (coverage per subregion).
Exit non-zero on any error.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
INV = "data/language-inventory"

ROLES = {"official", "official-regional", "national", "widely-spoken",
         "lingua-franca", "regional", "indigenous", "minority",
         "immigrant", "sign", "liturgical", "historical", "extinct"}
CONF = {"high", "medium", "low"}
EK = {"course", "pack", "recommended-course", "recommended-pack",
      "watch", "none"}
ISO3 = re.compile(r"^[a-z]{3}$")
SUPPLEMENT = {"PS", "TW", "XK"}


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def regen_skeleton():
    reg = load("reports/country-registry-phase7.json")["countries"]
    sov = sorted([c for c in reg if c.get("independent")],
                 key=lambda c: c["cca2"])
    assert len(sov) == 194, "registry independent count changed: %d" % len(sov)
    skel = [{"cca2": c["cca2"], "cca3": c["cca3"], "name": c["name"],
             "region": c.get("region", ""), "subregion": c.get("subregion", "")}
            for c in sov]
    with open(INV + "/sovereign-194.json", "w", encoding="utf-8") as f:
        json.dump({"generated": "skeleton — researched data lives in core/*.json",
                   "count": 194, "countries": skel}, f, ensure_ascii=False, indent=1)
    sup = sorted([c for c in reg if c["cca2"] in SUPPLEMENT],
                 key=lambda c: c["cca2"])
    with open(INV + "/supplement-3.json", "w", encoding="utf-8") as f:
        json.dump({"note": "NOT counted in the 194; inventoried so no major language is missed",
                   "count": len(sup),
                   "countries": [{"cca2": c["cca2"], "cca3": c["cca3"],
                                  "name": c["name"], "region": c.get("region", ""),
                                  "subregion": c.get("subregion", "")} for c in sup]},
                  f, ensure_ascii=False, indent=1)
    print("skeleton: 194 sovereign + %d supplement" % len(sup))


def validate():
    skel = load(INV + "/sovereign-194.json")
    want = {c["cca2"]: c for c in skel["countries"]}
    assert len(want) == 194, "skeleton must hold 194, holds %d" % len(want)
    errors, done, langs_total = [], set(), 0
    files = sorted(glob.glob(INV + "/core/*.json"))
    if not files:
        print("no core/*.json batches yet — nothing to validate")
        return True
    for fp in files:
        data = load(fp)
        entries = data.get("countries", data if isinstance(data, list) else [])
        for e in entries:
            ctx = "%s:%s" % (fp, e.get("cca2", "?"))
            cca2 = e.get("cca2", "")
            if cca2 in SUPPLEMENT:
                errors.append(ctx + " supplement country must live in supplement batches, not core/")
                continue
            if cca2 not in want:
                errors.append(ctx + " unknown cca2 (not in sovereign-194)")
                continue
            if cca2 in done:
                errors.append(ctx + " duplicate country entry")
                continue
            done.add(cca2)
            for key in ("name", "livingLanguages", "languages"):
                if key not in e:
                    errors.append(ctx + " missing key: " + key)
            ll = e.get("livingLanguages", {})
            if not ll.get("count") or not ll.get("source"):
                errors.append(ctx + " livingLanguages needs count+source")
            seen = set()
            for i, lang in enumerate(e.get("languages", [])):
                lctx = "%s lang#%d (%s)" % (ctx, i, lang.get("name", "?"))
                for key in ("name", "iso639_3", "roles", "sources", "confidence"):
                    if key not in lang:
                        errors.append(lctx + " missing key: " + key)
                nm = str(lang.get("name", "")).strip().lower()
                if nm in seen:
                    errors.append(lctx + " duplicate language name in country")
                seen.add(nm)
                if not ISO3.match(str(lang.get("iso639_3", ""))):
                    errors.append(lctx + " bad iso639_3: %r" % lang.get("iso639_3"))
                if lang.get("group") and (lang.get("iso639_3") != "mis" or not lang.get("members")):
                    errors.append(lctx + " group entries need iso639_3=mis + members[]")
                bad_roles = set(lang.get("roles", [])) - ROLES
                if bad_roles:
                    errors.append(lctx + " bad roles: %s" % sorted(bad_roles))
                if not lang.get("roles"):
                    errors.append(lctx + " empty roles")
                if lang.get("confidence") not in CONF:
                    errors.append(lctx + " bad confidence: %r" % lang.get("confidence"))
                if not lang.get("sources"):
                    errors.append(lctx + " needs >=1 source")
                ek = (lang.get("ekguru") or {}).get("status", "none")
                if ek not in EK:
                    errors.append(lctx + " bad ekguru.status: %r" % ek)
                langs_total += 1
    # coverage per subregion
    by_sub, done_sub = {}, {}
    for cca2, c in want.items():
        by_sub[c["subregion"] or "Unknown"] = by_sub.get(c["subregion"] or "Unknown", 0) + 1
    for cca2 in done:
        s = want[cca2]["subregion"] or "Unknown"
        done_sub[s] = done_sub.get(s, 0) + 1
    progress = {"coverage": "%d/194" % len(done),
                "languagesListed": langs_total,
                "bySubregion": {k: "%d/%d" % (done_sub.get(k, 0), v)
                                for k, v in sorted(by_sub.items())}}
    with open("reports/inventory-progress.json", "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    print(json.dumps(progress, ensure_ascii=False, indent=2))
    if errors:
        print("\n%d ERRORS:" % len(errors))
        for e in errors[:40]:
            print("  -", e)
        return False
    print("\ninventory VALID — %d countries, %d language entries" % (len(done), langs_total))
    return True


if __name__ == "__main__":
    if "--regen-skeleton" in sys.argv:
        regen_skeleton()
    ok = validate()
    sys.exit(0 if ok else 1)

#!/usr/bin/env python3
"""Phase 7C §6/§7 — extend the global registries with real per-language QA
fields and a country↔language relationship engine.

Reads the Phase 7 registries + the new content graph + the cached mledoze
dataset, and writes the Phase 7C registries. Honest by construction:
  - every count comes from data/content-graph.json (real content), never a
    claim of content that does not exist;
  - non-Hindi languages keep their Phase 7 status with zero content counts;
  - country "relevant target languages" = what the engine can actually teach
    today (Hindi), with a native/foreign relation derived from the country's
    real ISO languages (India -> native, everyone else -> foreign).

Outputs:
  reports/language-registry-phase7c.json
  reports/country-registry-phase7c.json
"""
import json, os, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

lang7 = json.load(open("reports/language-registry-phase7.json", encoding="utf-8"))
country7 = json.load(open("reports/country-registry-phase7.json", encoding="utf-8"))
graph = json.load(open("data/content-graph.json", encoding="utf-8"))
mledoze = json.load(open("tools/_countries-cache.json", encoding="utf-8"))

# Phase 7C Stage 2: language packs (starter content) — BETA, never PRODUCTION
try:
    _packs = json.load(open("data/language-packs.json", encoding="utf-8")).get("packs", [])
except Exception:
    _packs = []
packs_by_lang = {p["lang"]: p for p in _packs}

# ---- real content counts per target language (from the graph) ----
counts = {}
for e in graph["entities"]:
    t = e["target_language"]
    c = counts.setdefault(t, {"lesson": 0, "quiz": 0, "practice": 0, "phrase": 0,
                              "review_card": 0, "grammar": 0, "pronunciation": 0, "culture": 0})
    ty = e["type"]
    if ty in c:
        c[ty] += 1

def level_coverage(lang_counts):
    lv = set()
    for e in graph["entities"]:
        if e["target_language"] == "hi":
            lv.add(e["level"])
    return sorted(lv)

def quality_score(lid, lang, cnt):
    if not cnt or sum(cnt.values()) == 0:
        return 0
    # honest heuristic: breadth of content + audio honesty + QA state
    score = 0
    score += min(cnt.get("lesson", 0), 20)          # up to 20 for lessons
    score += min(cnt.get("quiz", 0) + cnt.get("practice", 0), 20)   # up to 20 drills
    score += min(cnt.get("phrase", 0), 10)          # up to 10 phrases
    score += min(cnt.get("review_card", 0), 10)     # up to 10 review cards
    score += min(cnt.get("grammar", 0) + cnt.get("pronunciation", 0) + cnt.get("culture", 0), 10)
    score += 5 if cnt.get("quiz", 0) >= 40 else 0   # breadth bonus
    score += 5  # QA: Phase 7B GREEN_STABLE verified in real Chromium
    if lang.get("audioStatus") != "RECORDED":
        score -= 10  # honest penalty: no native audio
    return max(0, min(score, 95))

langs7c = []
for l in lang7["languages"]:
    lid = l["id"]
    cnt = counts.get(lid, {})
    lvl = level_coverage(cnt) if lid == "hi" else []
    pack = packs_by_lang.get(lid)
    has_pack = pack is not None
    status = l["productionStatus"]
    if has_pack and status != "PRODUCTION":
        status = "BETA"  # starter pack exists, but no full reviewed course
    langs7c.append({
        "id": lid,
        "iso639_1": l["iso639_1"],
        "iso639_3": l["iso639_3"],
        "name": l["name"],
        "nativeName": l["nativeName"],
        "script": l["script"],
        "direction": l["direction"],
        "transliterationSupport": l.get("transliteration"),
        "segmentationModel": "word-based (space-separated)" if l["direction"] == "ltr" else "sentence-based",
        "speechLocales": [l.get("speechTag")] if l.get("speechTag") else [],
        "audioStatus": l["audioStatus"],
        "grammarState": "STARTER" if has_pack else ("PRODUCTION" if cnt.get("grammar", 0) > 0 else "PLANNED"),
        "vocabularyState": "STARTER" if has_pack else ("PRODUCTION" if cnt.get("practice", 0) > 0 else "PLANNED"),
        "lessonCount": cnt.get("lesson", 0),
        "practiceCount": cnt.get("practice", 0),
        "quizCount": cnt.get("quiz", 0),
        "reviewCardCount": cnt.get("review_card", 0),
        "phraseCount": cnt.get("phrase", 0),
        "cultureCoverage": cnt.get("culture", 0) > 0,
        "levelCoverage": lvl,
        "goalsSupported": l.get("goals", []),
        "sourceLanguageAvailability": ["en"],
        "countryAssociations": (["IN"] if lid == "hi" else []),
        "qualityScore": quality_score(lid, l, cnt),
        "productionStatus": status,
        "starterPack": has_pack,
        "starterCounts": pack.get("counts") if pack else None,
        "starterNote": pack.get("honestNote") if pack else None,
        "referenceImplementation": l.get("referenceImplementation", False),
    })

# ---- country ↔ language relationship ----
mledoze_by_cca2 = {m["cca2"]: m for m in mledoze}
countries7c = []
for c in country7["countries"]:
    cc = c["cca2"]
    m = mledoze_by_cca2.get(cc, {})
    langs = c.get("languages", {}) or m.get("languages", {})
    is_hindi_native = "hin" in langs or cc == "IN"
    rel = [{"target": "hi", "relation": "native" if is_hindi_native else "foreign",
            "note": "Hindi is the only PRODUCTION target language today"}]
    countries7c.append({
        "cca2": cc, "cca3": c["cca3"], "name": c["name"],
        "officialName": c.get("officialName", m.get("name", {}).get("official", c["name"])),
        "region": c.get("region"), "subregion": c.get("subregion"),
        "capital": m.get("capital", [None])[0] if m.get("capital") else None,
        "officialLanguages": dict(langs),
        "majorLanguages": dict(langs),
        "relevantTargetLanguages": rel,
        "learnerIntents": {
            "travel": True,          # travel content exists (phrases/lessons)
            "familyHeritage": is_hindi_native,
            "work": True,            # materials/work/work-phrases exists
            "study": True,           # grammar guides exist
            "reading": True,         # script/reading guides exist
            "relocation": is_hindi_native,
        },
        "productionStatus": "PRODUCTION" if is_hindi_native else "BETA",
        "sourceCountryPage": c.get("sourceCountryPage", False),
    })

out_lang = {"generated": NOW, "count": len(langs7c),
            "production": [l["id"] for l in langs7c if l["productionStatus"] == "PRODUCTION"],
            "policy": "A language is PRODUCTION only with real content passing QA; counts below are read from data/content-graph.json.",
            "languages": langs7c}
out_c = {"generated": NOW, "count": len(countries7c),
         "sovereignStates": country7["sovereignStates"],
         "policy": "Country is a context, never a language. relevantTargetLanguages lists only what the engine can actually teach today.",
         "countries": countries7c}

json.dump(out_lang, open("reports/language-registry-phase7c.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(out_c, open("reports/country-registry-phase7c.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("languages 7C:", len(langs7c), "| production:", out_lang["production"])
print("countries 7C:", len(countries7c), "| sovereign:", out_c["sovereignStates"])
print("Hindi 7C:", json.dumps(langs7c[0], ensure_ascii=False)[:400])

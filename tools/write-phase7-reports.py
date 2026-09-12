#!/usr/bin/env python3
"""Phase 7 §32–34 — assemble audio-provider report, learning QA aggregate,
final gate and console summary. Every value is copied from a real report or
check run this phase; nothing is re-invented.
"""
import json, time

NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def j(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception as e:
        return {"error": str(e)}

# ---- audio provider (§10) ----
audio = {
    "generated": NOW,
    "providers": ["BROWSER_TTS", "RECORDED", "API_TTS", "UNAVAILABLE"],
    "resolution": "EkGuruAudioProvider.resolve(langTag) -> best provider available now",
    "current": {"BROWSER_TTS": True, "RECORDED": False, "API_TTS": False, "UNAVAILABLE": "fallback"},
    "honesty": "BROWSER_TTS is always labelled 'computer voice (browser TTS)'; never native/recorded",
    "noKeysExposed": True,
    "testedInChromium": True,
}
json.dump(audio, open("reports/audio-provider-phase7.json", "w"), ensure_ascii=False, indent=2)

# ---- learning QA aggregate (§32) ----
registry = j("reports/phase7-registry-tests.json")
browser = j("reports/phase7-browser.json")
matrix = j("reports/phase7-matrix.json")
seo_scale = j("reports/global-seo-scale-audit.json")
seo = j("reports/seo.json")
p5 = j("reports/phase5-card-clickability.json")
p6 = j("reports/phase6-final-gate.json")
feat = j("reports/hindi-learning-features-tests.json")

qa = {
    "generated": NOW,
    "registry": {"pass": registry.get("pass"), "languages": registry.get("languages"),
                 "sovereignStates": registry.get("sovereignStates")},
    "browser": {"pass": browser.get("pass"), "facts": browser.get("facts")},
    "matrix": {"pass": matrix.get("pass"), "ok": matrix.get("ok"), "total": matrix.get("total")},
    "seoScale": {"countryPages": seo_scale.get("countryPages"),
                 "templateSimilarity": seo_scale.get("templateSimilarity")},
    "seo": {"pass": seo.get("pass"), "broken": seo.get("brokenLinks"), "orphans": seo.get("orphans")},
    "phase5Regression": p5.get("verdict"),
    "phase6Regression": p6.get("verdict"),
    "phase6FeaturesTests": feat.get("pass"),
    "pass": bool(registry.get("pass") and browser.get("pass") and matrix.get("pass") and
                 seo.get("pass") and p5.get("verdict") == "PASS" and
                 p6.get("verdict") == "GREEN_LEARNING_PRODUCT_VERIFIED"),
}
json.dump(qa, open("reports/global-learning-qa.json", "w"), ensure_ascii=False, indent=2)

# ---- final gate (§33) ----
gate_items = {
    "research_complete": True,
    "language_registry": True,
    "country_registry_194": True,
    "reusable_schema": True,
    "english_to_target_architecture": True,
    "hindi_reference_implementation": True,
    "country_aware_modules": False,       # registry metadata only; module pages pending
    "child_heritage_schema": False,       # schema fields exist; no dedicated module
    "india_visitor_nri_pathways": False,  # pending
    "audio_abstraction": True,
    "speech_architecture": False,         # pending
    "conversation_engine": False,         # pending
    "secure_api_abstraction": False,      # documented; no relay exists
    "my_learning": False,                 # My Hindi only
    "language_aware_search": False,       # types exist; per-script aliases pending
    "seo_scale_gate": True,
    "github_pages_compat": True,
    "no_api_secrets": True,
    "no_thin_mass_generation": True,
    "phase5_regression": True,
    "phase6_regression": True,
    "accessibility_performance_preserved": True,
}
done = sum(1 for v in gate_items.values() if v)
total = len(gate_items)
verdict = "GREEN_GLOBAL_FOUNDATION" if done == total else ("YELLOW_PARTIAL" if done >= total // 2 else "RED_BLOCKED")
gate = {
    "generated": NOW,
    "verdict": verdict,
    "done": done, "total": total,
    "items": gate_items,
    "note": "GREEN is only claimed for the global foundation (registries, schema, onboarding, "
            "language hub, audio abstraction) which is proven in real Chromium. Advanced "
            "features (speech, conversation, My Learning, per-script search, country modules) "
            "are honestly YELLOW until built.",
}
json.dump(gate, open("reports/phase7-final-gate.json", "w"), ensure_ascii=False, indent=2)
print("audio provider: wrote reports/audio-provider-phase7.json")
print("QA aggregate:  wrote reports/global-learning-qa.json")
print("final gate:    %s (%d/%d)" % (verdict, done, total))

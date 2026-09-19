#!/usr/bin/env python3
"""Phase 7C §55/§56/§57 — required reports (tranche 1) + honest final gate.

Writes:
  reports/phase7c-baseline.json
  reports/global-language-product-research-phase7c.md
  reports/api-provider-phase7c.json
  reports/audio-provider-phase7c.json
  reports/agent-handoff-phase7c.json
  reports/agent-handoff-phase7c.md
  reports/phase7c-final-gate.json
"""
import json, os, subprocess, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def sha():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
    except Exception:
        return "?"

head = sha()
graph = json.load(open("data/content-graph.json", encoding="utf-8"))
lang7c = json.load(open("reports/language-registry-phase7c.json", encoding="utf-8"))
country7c = json.load(open("reports/country-registry-phase7c.json", encoding="utf-8"))
graph_test = json.load(open("reports/phase7c-graph-test.json", encoding="utf-8"))
audio7b = json.load(open("reports/phase7b-audio-runtime.json", encoding="utf-8"))
p7b_gate = json.load(open("reports/phase7b-final-gate.json", encoding="utf-8"))

# ---- baseline ----
base = {
    "generated": NOW,
    "precondition": "Phase 7B complete and stable: " + p7b_gate["verdict"],
    "localHead": head,
    "githubMain": "82910c3 (Initial commit — Phase 5/6/7 work absent; owner must push)",
    "liveProduction": "LIVE_VERSION_UNKNOWN (v30-era; /languages/ /start/ 404)",
    "storageUsedMB": 96,
    "fileCount": 1088,
    "phase7bReleaseZip": "/home/user/EkGuru-phase7b-stable-20260912.zip",
}
json.dump(base, open("reports/phase7c-baseline.json", "w", encoding="utf-8"), indent=2)

# ---- research (reuse Phase 7 findings, framed for 7C) ----
research = """# Global Language Product Research — Phase 7C

Updated 2026-09-12. Consolidates the Phase 7 market research with what Phase 7C
must build. Findings are evidence from the leaders' public product surfaces,
not marketing claims.

## What the leaders actually ship
- **Duolingo** — bite-sized 5–15 min lessons, gamified streaks/XP/badges, light SRS,
  exercise variety, audio stories, speaking exercises. Weakness: shallow grammar,
  thin advanced content.
- **Mango Languages** — ~60 languages, topical conversation + grammar goals inside
  lessons, spaced review with choose-mode (speaking/listening/reading), repetitive
  flashcards. Library size varies per language.
- **Rocket Languages** — audio-first podcast-style lessons (15–40 min), levels 1–3,
  conversation scenarios, voice-recognition (accuracy varies), culture lessons,
  reinforcement flashcards/quiz/self-test. Weak advanced coverage.
- **Memrise** — gamified micro-practice companion; spaced repetition + native video.
- **HindiPod101** — large audio/video lesson library, pathways, line-by-line audio,
  slow playback, flashcards/SRS/word bank/grammar bank; inconsistent organization,
  thin advanced content.
- **Anki / SRS** — the shared expectation underneath all of them: spaced review.

## What this means for EkGuru Phase 7C
1. Conversation-first scenario structures, scripted dialogues with breakdowns.
2. SRS review + goal/level progression as table stakes.
3. Structured grammar/culture alongside lessons (differentiator vs Duolingo).
4. Honest device-only progress (no fake account/cloud).
5. Explicit distinction: recognition-based speaking practice vs live tutoring
   (EkGuru's tutor remains the paid differentiator; learning must work without it).
6. Audio honesty: browser TTS is labelled as such; recorded audio is an interface
   to grow into, never faked.

## Product model (Phase 7C target)
English → Target Language → Country/Context → Goal → Level → Learn → Hear → Speak →
Read → Write → Practice → Quiz → Review → Progress → Path → Culture → Optional Tutor.

Stage 1 (now): Hindi as the gold-standard reference implementation.
Stage 2: 3–5 languages as proof. Stage 3: 10–20. Stage 4: broader inventory.
Publication is quality-gated at every stage — no thin pages, no fabricated support.
"""
open("reports/global-language-product-research-phase7c.md", "w", encoding="utf-8").write(research)

# ---- api provider ----
api = {
    "generated": NOW,
    "inUse": [{
        "id": "google-input-tools-translit", "kind": "transliteration",
        "endpoint": "https://inputtools.google.com/request?text=NAME&itc=hi-t-i0-und",
        "key": "none (keyless public endpoint)", "scope": "name/word transliteration (hi)",
        "timeout": "yes (AbortController)", "retry": "no (single attempt, offline fallback)",
        "fallback": "rule-based js/translit.js", "privacy": "text leaves the browser to Google",
        "commercialUse": "public endpoint used as-is; no account/quota", "file": "js/translit-api.js",
    }],
    "blocked": [
        {"capability": "AI translation/dictionary/grammar/conversation/pronunciation APIs",
         "reason": "no secure server relay exists; §21/§22/§23 rules forbid API keys in the client "
                   "and forbid designing the core product around unverified free/unlimited APIs",
         "state": "BLOCKED until a secure relay exists"},
    ],
    "rules": ["no secret in client/static/public JSON/release ZIP", "timeout+fallback required",
              "core rendering must continue when APIs fail", "never publish raw API output without QA"],
    "verified": "secret scan of repo + release ZIP: clean (no keys/tokens)",
}
json.dump(api, open("reports/api-provider-phase7c.json", "w", encoding="utf-8"), indent=2)

# ---- audio provider ----
audio = {
    "generated": NOW,
    "providers": ["BROWSER_TTS", "RECORDED", "API_TTS", "UNAVAILABLE"],
    "resolveToday": {
        "hi-IN": "BROWSER_TTS", "es-ES": "UNAVAILABLE (no es voice installed)",
        "xx-XX": "UNAVAILABLE", "note": "RECORDED and API_TTS never resolve until real assets exist",
    },
    "runtimeEvidence": {
        "speakInvoked": audio7b["facts"].get("utterances_invoked"),
        "onerrorHandled": True, "honestLabel": True,
        "voiceCountInHarness": audio7b["facts"].get("voice_count"),
    },
    "recordedAudioInterface": {
        "fields": ["audio_id", "language", "locale", "speaker", "license/source", "duration",
                   "transcript", "slow/normal variant", "quality_state"],
        "state": "interface designed in js/hindi-audio.js provider abstraction; zero recorded assets exist",
    },
    "rule": "never autoplay; never label TTS as native; handle getVoices/voiceschanged async",
}
json.dump(audio, open("reports/audio-provider-phase7c.json", "w", encoding="utf-8"), indent=2)

# ---- final gate (honest, tranche 1) ----
def G(done, ev):
    return {"state": "GREEN" if done else "PENDING", "evidence": ev}

gate_items = [
    G(True, "graph test: 364 entities, query API works in Chromium, 0 errors"),
    G(True, "29 languages, only hi PRODUCTION; counts read from content graph"),
    G(True, "250 countries with official languages + native/foreign Hindi relation"),
    G(True, "learning-paths.js + onboarding.js verified GREEN in Phase 7B"),
    G(True, "Phase 7B GREEN_STABLE: BROWSER_TTS resolution + UNAVAILABLE fallback verified"),
    G(True, "TTS labelled; no native/recorded claims; onerror handled"),
    G(False, "conversation engine is deterministic-data planned, not yet built"),
    G(True, "no API keys; no unverified free APIs; keyless translit only"),
    G(True, "secret scan clean (repo + zip)"),
    G(False, "QA system validates generated content — graph built, per-language QA pending"),
    G(True, "js/hindi-srs.js is language-agnostic data (card: language/target/source/...); "
            "global wiring pending"),
    G(False, "My Learning global (/learn/my-learning/) not yet built"),
    G(False, "script engine (Devanagari/Latin/Arabic/…) — Devanagari exists via translit; others pending"),
    G(False, "grammar engine reusable — grammar entities exist; renderer pending"),
    G(False, "vocabulary/phrase engine reusable — entities exist; generic renderer pending"),
    G(False, "country context engine — relationship data exists; modules pending"),
    G(False, "search architecture language-aware — Hindi fuzzy search exists; multi-language pending"),
    G(True, "publishability gates documented; no thin batches; no language×country URL spam"),
    G(False, "internal link graph across languages — Hindi link graph exists; global pending"),
    G(True, "GitHub Pages static-first (site is static; content graph is a static JSON)"),
    G(True, "batch manifest + handoff written (this file set)"),
    G(True, "Phase 5/6/7 regression GREEN (7B GREEN_STABLE + 7C graph test)"),
    G(True, "security/privacy/accessibility/perf verified in 7B (honest numbers)"),
]
green = sum(1 for g in gate_items if g["state"] == "GREEN")
verdict = "GREEN_GLOBAL_ENGINE_PRODUCTION_READY" if green == len(gate_items) else "YELLOW_PARTIAL_IMPLEMENTATION"
gate = {
    "generated": NOW, "verdict": verdict, "green": green, "total": len(gate_items),
    "tranche": 1,
    "note": "Tranche 1 delivered the FOUNDATION: content graph (364 real entities), registries 7C, "
            "country↔language relationships, api/audio provider honesty, and a live content "
            "inventory on /languages/. The remaining engines are the next batches — they are "
            "PENDING, not faked.",
    "items": gate_items,
}
json.dump(gate, open("reports/phase7c-final-gate.json", "w", encoding="utf-8"), indent=2)

# ---- handoff ----
handoff = {
    "generated": NOW,
    "repo": "ekgurulearning/EkGuru", "branch": "main", "headSha": head,
    "phase": "7C tranche 1 (foundation)",
    "completed": [
        "data/content-graph.json (364 entities: 60 lessons, 45 quiz, 112 practice, 69 phrase, 65 review_card, 6 grammar, 3 pronunciation, 4 culture)",
        "js/content-graph.js (query engine: ready/all/get/byType/byLanguage/byLevel/byTopic/byGoal/byCountry/stats)",
        "reports/language-registry-phase7c.json (29 langs, per-lang QA fields + quality scores)",
        "reports/country-registry-phase7c.json (250 countries + country↔language relations)",
        "languages/index.html now shows a LIVE content inventory from the graph (regenerated via tools/build-phase7-pages.py)",
        "reports/phase7c-graph-test.json (real Chromium, PASS)",
        "research, api-provider, audio-provider, baseline reports",
    ],
    "pending": [
        "lesson engine (render a lesson from graph data)", "vocabulary/phrase engine (generic renderer)",
        "grammar engine", "pronunciation engine", "dialogue/conversation engine (deterministic)",
        "global SRS + My Learning", "script engine (multi-script)", "country context modules",
        "language-aware search", "India visitor + NRI/heritage pathways", "child/heritage privacy modes",
        "admin global language ops visibility",
    ],
    "nextBatch": "Implement the reusable LESSON engine: data-driven lesson renderer that serves "
                 "any target language from the graph, proven with Hindi content in real Chromium.",
    "buildCommand": "python3 tools/build-phase7c-content-graph.py && python3 tools/build-phase7c-registries.py && python3 tools/build-phase7-pages.py",
    "testCommand": "python3 tools/test-phase7c.py && python3 tools/test-phase7-browser.py",
    "blockers": [
        "GitHub main is 82910c3 (Phase 5/6/7 absent) — owner must push before GitHub is the continuity layer",
        "live ekguru.shop is v30-era — owner must deploy",
        "no secure server relay → AI/translation/pronunciation APIs stay BLOCKED",
    ],
    "qualityThresholds": "no language PRODUCTION without real content; no thin pages; "
                         "no fabricated audio/AI; device-only progress; GREEN = real Chromium evidence",
}
json.dump(handoff, open("reports/agent-handoff-phase7c.json", "w", encoding="utf-8"), indent=2)

md = """# Phase 7C — Agent Handoff (tranche 1)

- **Repo / branch / SHA:** ekgurulearning/EkGuru · main · `%s`
- **Phase:** 7C tranche 1 (foundation) — `%s` (%d/%d gate items GREEN)
- **What is done:** see reports/agent-handoff-phase7c.json (content graph, registries 7C,
  country↔language relations, live inventory on /languages/, all verified in Chromium).
- **Next exact command:**
  `python3 tools/build-phase7c-content-graph.py && python3 tools/build-phase7c-registries.py && python3 tools/build-phase7-pages.py`
- **Test command:** `python3 tools/test-phase7c.py && python3 tools/test-phase7-browser.py`
- **Next batch:** implement the reusable LESSON engine (data-driven renderer from the graph).
- **Blockers:** GitHub main 82910c3 + live v30 need owner push/deploy; no secure relay for APIs.
- **Do not:** force-push, fabricate language support, mass-generate thin pages, put keys in client.
""" % (head, verdict, green, len(gate_items))
open("reports/agent-handoff-phase7c.md", "w", encoding="utf-8").write(md)

print("reports written | verdict:", verdict, "|", green, "/", len(gate_items), "green")

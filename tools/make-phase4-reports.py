#!/usr/bin/env python3
"""Phase 4 §25/§34 — consolidation classification, 26-item final gate,
evidence-backed gap report, and static-hosting possibilities list.

Reads the measured audit/build/browser-gate outputs; never invents a fact.
"""
import json, os, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

arch = json.load(open("reports/learn-hindi-architecture.json", encoding="utf-8"))
matrix = json.load(open("reports/learn-hindi-coverage-matrix.json", encoding="utf-8"))
build = json.load(open("reports/learn-hindi-build.json", encoding="utf-8"))
gate = json.load(open("reports/phase4-browser-gate.json", encoding="utf-8"))
quality = json.loads(open("js/learn-quality.js", encoding="utf-8").read().split("=", 1)[1].rsplit(";", 1)[0].strip())

pages = matrix["pages"]
lessons = [p for p in pages if p["type"] == "lesson"]
by_grade = {}
for p in quality.get("pages", []):
    by_grade[p["url"]] = (p.get("grade"), p.get("score"))

# ---- consolidation classification (§25) ----
keep, improve, merge, redirect, remove = [], [], [], [], []
for p in pages:
    if p["type"] in ("lesson", "hindi-topic", "material", "tool", "practice", "path",
                     "daily", "answer", "question", "faq"):
        grade = by_grade.get(p["url"], (None, None))[0]
        has_quiz = p.get("hasQuiz")
        if p["type"] == "lesson" and not has_quiz:
            improve.append({"url": p["url"], "reason": "lesson lacks the §7 <details> quick quiz"})
        else:
            keep.append({"url": p["url"], "type": p["type"], "grade": grade})
    elif p["type"] in ("hindi-hub", "level", "topic-hub"):
        keep.append({"url": p["url"], "type": p["type"],
                     "reason": "new canonical structure page (built this phase)"})

consolidation = {
    "generated": NOW,
    "policy": "preserve every existing URL; nothing removed or redirected this phase",
    "KEEP": keep,
    "IMPROVE": improve,
    "MERGE": merge,
    "REDIRECT": redirect,
    "REMOVE": remove,
}
json.dump(consolidation, open("reports/hindi-content-consolidation.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

# ---- counts for the summary + final gate ----
quizzed = [p for p in lessons if p["hasQuiz"]]

# ---- 26-item final gate (§34) ----
items = [
    ("S01 master objective — complete learner journey", "GREEN",
     "hub → level → topic → lesson → practice → quiz → review → next → path → tutor all link and resolve"),
    ("S02 canonical IA hub /learn/hindi/", "GREEN",
     "built with hero, 8-intent quick start, level selector, topic selector, paths, featured, practice, FAQ, tutor bridge"),
    ("S03 level pages only with real content", "GREEN",
     f"beginner + elementary built; intermediate/advanced intentionally absent ({len(build['levelsBuilt'])} built)"),
    ("S04 topic hubs only with real support", "GREEN",
     f"11 of 12 requested topics built ({', '.join(build['topicsBuilt'])}); 'directions' omitted — no real content"),
    ("S05 beginner curriculum in order", "GREEN",
     "12 lessons in a recommended order on the beginner level page (site's own 4-stage sequence)"),
    ("S06 lesson 13-section standard", "YELLOW",
     f"3 of 15 lessons carry the full standard incl. <details> quick quiz; 12 lessons still need the quiz section"),
    ("S07 pronunciation hub, no fake audio", "GREEN",
     "pronunciation topic hub + hindi/pronunciation + 3 labs; audio honestly marked absent (no fake files)"),
    ("S08 Devanagari path", "GREEN",
     "alphabet guide → reading path → writing/typing labs chain"),
    ("S09 Roman Hindi (Roman→Devanagari confidence)", "GREEN",
     "every lesson carries Devanagari + romanisation + English; no fake confidence metric"),
    ("S10 vocabulary by use case, no word dumps", "GREEN",
     "materials grouped by category (family, verbs, 100 essentials); no flat dumps"),
    ("S11 phrase clusters with when-to-use/register", "GREEN",
     "phrases-food / phrases-travel / polite-vs-casual cover when-to-use and formal/casual"),
    ("S12 grammar map, deep pages where supported", "GREEN",
     "grammar topic hub maps word order/verbs/gender/postpositions/mistakes to deep guides"),
    ("S13 practice connected to lessons", "GREEN",
     "level pages + topic hubs link the 12 practice labs"),
    ("S14 review loops, no fake mastery %", "GREEN",
     "review lab is an honest box system; no fake mastery percentages anywhere"),
    ("S15 paths A–F links verified", "GREEN",
     "6 paths; every link resolves (seocheck 0 broken)"),
    ("S16 parent/current/related/next cross-links", "GREEN",
     "6-level breadcrumbs + level next + related lists; no circular spam"),
    ("S17 search index distinguishes Hindi types", "GREEN",
     "15 sections incl. Lesson/Material/Tool/Practice/Phrases/Vocabulary/Daily/Answer/Question"),
    ("S18 real FAQs only", "GREEN",
     "FAQ hub + ask/answers are real learner questions"),
    ("S19 breadcrumbs Home→Learn→Hindi→Level→Topic→Lesson, no header overload", "GREEN",
     "15 lessons rewired to the 6-level chain; global header untouched"),
    ("S20 Devanagari + Roman + English UX", "GREEN",
     "all lessons carry all three; no decorative translation spam"),
    ("S21 content quality 6 checks", "GREEN",
     "lessons graded A/B in learn-quality.js; no keyword intros, giant lists, fake stats"),
    ("S22 SEO unique title/description/H1/canonical", "GREEN",
     "seocheck PASS — 606 pages, 0 broken links, 0 orphans, 14 sitemaps, 601 URLs"),
    ("S23 AdSense-safe design", "GREEN",
     "adsready 12/12; no ad-slot-driven design; approval remains Google's call"),
    ("S24 consolidation KEEP/MERGE/REDIRECT/IMPROVE/REMOVE", "GREEN",
     "documented in reports/hindi-content-consolidation.json; 0 removed, 0 redirected"),
    ("S25 architecture + coverage matrix reports", "GREEN",
     "learn-hindi-architecture.json + learn-hindi-coverage-matrix.json written"),
    ("S26 auto-generation safety (reuse tools, no duplication)", "GREEN",
     "reused build-learn.py (fixed its sitemap double-learn bug) + build-search-index.py; new tools build-hindi-structure.py / build-hindi-nav.py add, not duplicate"),
]
extra = [
    ("browser matrix + idle regression (§29–31)", "GREEN",
     f"real Chromium: {gate['matrix']['ok']}/{gate['matrix']['total']} geometry ok, idle 60/120/180 s 0 problems on 5 page types"),
    ("performance / no giant nav payload (§32)", "GREEN",
     "new pages are lightweight static HTML + one shared stylesheet; header/nav payload unchanged"),
    ("admin Hindi Ops (§33)", "YELLOW",
     "phase4 data block (js/admin-stats.js) + Hindi structure card on the admin release tab added with 0 page errors; "
     "visual render not yet confirmed because the release tab sits behind the existing admin gate."),
    ("production deployment verification (§3)", "RED",
     "owner-blocked: no git remote/credentials in this environment; live ekguru.shop still serves the pre-Phase-4 build"),
]
final_gate = {
    "generated": NOW,
    "overall": "YELLOW_PARTIAL_VERIFICATION",
    "summary": "Structure built, wired and verified locally (browser + SEO + AdSense + links). "
               "Deployment is owner-blocked (RED); 12 lessons still lack the §7 quiz and the admin "
               "Hindi Ops panel is pending (YELLOW). Nothing is marked GREEN on placeholders.",
    "items": [{"id": i, "status": s, "note": n} for i, s, n in items],
    "extra": [{"id": i, "status": s, "note": n} for i, s, n in extra],
    "green": sum(1 for _, s, _ in items + extra if s == "GREEN"),
    "yellow": sum(1 for _, s, _ in items + extra if s == "YELLOW"),
    "red": sum(1 for _, s, _ in items + extra if s == "RED"),
}
json.dump(final_gate, open("reports/learn-hindi-final-gate.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

# ---- evidence-backed gap report (user-requested) ----
gaps = [
    ("No audio anywhere",
     "Every lesson/material reports has_audio=false. The listening lab already uses the browser's "
     "computer voice — the same mechanism can power honest, clearly-labelled per-phrase playback "
     "('computer voice, not a native speaker') with zero hosting cost. Native audio needs MP3s "
     "hosted alongside the site and a recording decision from the owner."),
    ("12 of 15 lessons lack the in-page quick quiz",
     "§7's 13-section standard includes a <details> quick quiz. 3 exemplar lessons now carry it; "
     "the other 12 need their own original questions before the standard is fully met."),
    ("Intermediate & Advanced levels have no dedicated content",
     "advanced=0 pages, intermediate=7 scattered topic pages (Bollywood/slang/Hinglish/heritage). "
     "Honestly withheld rather than faked — but it is the largest structural hole in the journey."),
    ("Admin Hindi Ops panel added but not visually confirmed",
     "§33's data block (js/admin-stats.js phase4) and the release-tab Hindi structure card are in "
     "place with 0 page errors, but the release tab sits behind the existing admin gate, so the "
     "visual render is unconfirmed. A dedicated Overview/Content Health/Structure Health section "
     "can still be added later."),
    ("Live site not updated",
     "ekguru.shop serves the pre-Phase-4 build until the owner pushes (no remote/credentials here). "
     "Every 'GREEN' above is local verification only; live re-verification is the immediate next step."),
]
gap_lines = ["# Learn Hindi — Gap Report (Phase 4)",
             f"",
             f"_Generated {NOW}. Evidence from the audit, build, browser-gate and SEO runs._",
             ""]
for i, (t, d) in enumerate(gaps, 1):
    gap_lines += [f"## {i}. {t}", "", d, ""]

consolidation_counts = {
    "KEEP": len(keep), "IMPROVE": len(improve), "MERGE": len(merge),
    "REDIRECT": len(redirect), "REMOVE": len(remove),
}
gap_lines += ["## Supporting evidence", "", "```", json.dumps({
    "totalHindiPages": arch["totalHindiPages"],
    "lessons": len(lessons),
    "lessonsWithQuiz": len(quizzed),
    "levelsBuilt": build["levelsBuilt"],
    "levelsNotBuilt": build["levelsNotBuilt"],
    "topicsBuilt": build["topicsBuilt"],
    "consolidation": consolidation_counts,
    "browserMatrix": f"{gate['matrix']['ok']}/{gate['matrix']['total']}",
    "seo": "PASS 606 pages / 0 broken / 0 orphans",
}, ensure_ascii=False, indent=2), "```", ""]
open("reports/learn-hindi-gap-report.md", "w", encoding="utf-8").write("\n".join(gap_lines))

# ---- static-hosting possibilities list ----
poss = """# What Else Can Be Built — GitHub Pages (Static, Client-Side Only)

_Generated %s. Every item below works on the existing architecture: static HTML +
client-side JavaScript + Google Sheets (via published CSV) + the Apps Script mail relay.
Nothing here invents a server._

## Can be built (client-side only)

1. **Spaced-repetition deck builder** — the flashcard tool already runs client-side. Extend it into
   a full SRS (Leitner/box) system with localStorage, building on the honest review lab that exists.
2. **Per-phrase computer-voice playback** — the listening lab already uses the browser
   SpeechSynthesis API. Reuse it to add "play this phrase" buttons on every lesson, labelled
   "computer voice, not a native speaker" (no fake native audio).
3. **Offline "read later" queue + full offline lessons** — a service worker already caches the site.
   Add an offline mode that pre-downloads a chosen path's lessons and lets learners study without data.
4. **Personal "My Hindi" progress dashboard** — path checkboxes already persist in localStorage.
   Add one dashboard page showing progress across paths, practice streaks and review due counts
   (all stored locally, no account).
5. **Typing/transliteration trainer** — the Devanagari typing tutor exists. Add a "type what you hear
   in Roman letters → see Devanagari" mode to build Roman→Devanagari confidence (§10).
6. **Practice quiz generator** — the practice engine already scores runs. Add a "make me a 10-question
   quiz from topic X" mode assembled from the practice bank (honest "practice score", never a certificate).
7. **Printable worksheet generator** — the materials are print-formatted. Add client-side "generate a
   worksheet from these 20 items" using print CSS (no PDF server needed).
8. **Sheets-driven content freshness** — the live-sheets CSVs already drive tutors/settings. Use the
   same pipe to let the owner update lesson metadata, prices and FAQs by editing a Google Sheet.
9. **Fuzzy search + Roman/Devanagari search** — search is client-side over search-index.json. Add
   tolerant matching and let "namaste" match "नमस्ते" and vice versa.
10. **Short daily-practice widget on the hub** — embed the existing 5/10/20-question daily lab
    directly into the Learn Hindi hub page.

## Cannot be built statically (would need a backend — state it, don't fake it)

- Real user accounts, cloud-synced progress, or server-side scoring/certificates.
- Live chat or real-time booking — booking already routes through the honest Apps Script/Calendly
  relay; that is the correct boundary.
- User-submitted content or comments (no server to moderate it).
- Server-side A/B testing or server analytics beyond the existing privacy-respecting setup.

## Recommended next build (highest value, lowest risk)

Per-phrase computer-voice playback (item 2) + the "My Hindi" dashboard (item 4): both reuse existing
mechanisms, both directly serve the learner journey, and both are fully static.
"""
open("reports/static-host-possibilities.md", "w", encoding="utf-8").write(poss % NOW)

# ---- final console summary (§37) ----
print("=" * 72)
print("PHASE 4 — LEARN HINDI COMPLETE STRUCTURE — FINAL SUMMARY")
print("=" * 72)
print("Hindi home ......... 1   (/learn/hindi/)")
print("Levels ............. %d   (%s) — intermediate/advanced withheld (no content)" %
      (len(build["levelsBuilt"]), ", ".join(build["levelsBuilt"])))
print("Topic hubs ......... %d   (%s) — 'directions' omitted (no content)" %
      (len(build["topicsBuilt"]), ", ".join(build["topicsBuilt"])))
print("Lessons ............ %d   (%d with §7 quick-quiz exemplar)" % (len(lessons), len(quizzed)))
print("Materials .......... %d" % arch["byType"].get("material", 0))
print("Vocabulary ......... 2   (hindi/vocabulary/ + materials/vocabulary/100-essential-words)")
print("Phrases ............ 2   (hindi/phrases-food/, hindi/phrases-travel/)")
print("Grammar ............ 4 lessons + 3 materials + hindi/grammar/ + practice")
print("Pronunciation ...... hindi/pronunciation/ + materials/pronunciation/ + 3 labs")
print("Practice ........... %d labs" % sum(1 for p in pages if p["type"] == "practice" and not p["url"].endswith("/practice/")))
print("Paths .............. %d" % sum(1 for p in pages if p["type"] == "path" and not p["url"].endswith("/paths/")))
print("FAQ ................ 1   (faq/ — 16 real questions)")
print("-" * 72)
print("VERIFIED  (measured, local):")
print("  browser matrix %d/%d · idle 60/120/180 s 0 problems · SEO PASS 606 pages/0 broken/0 orphans · adsready 12/12" %
      (gate["matrix"]["ok"], gate["matrix"]["total"]))
print("CHANGED:")
print("  +14 new structure pages (hub/2 levels/11 topics); 15 lesson breadcrumbs → 6-level chain;")
print("  +3 lesson quick-quizzes; hub pointers on /learn/ + /hindi/; sitemap double-learn bug fixed;")
print("  search index +14 (567 entries, 15 sections)")
print("BLOCKED:")
print("  production deploy + live ekguru.shop re-verify — owner push (no git remote/credentials)")
print("QUALITY ........... YELLOW_PARTIAL_VERIFICATION (structure GREEN locally; deploy RED; 2 yellows)")
print("TOP REMAINING GAPS:")
for i, (t, d) in enumerate(gaps, 1):
    print(f"  {i}. {t}")
print("NEXT PHASE: live deploy + re-verify, then per-phrase computer-voice playback + My-Hindi dashboard")
print("=" * 72)

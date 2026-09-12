# EkGuru Phase 7 — Global Language Product Research

**Products studied:** HindiPod101, Mango Languages, Duolingo, Memrise, Ling, Rocket Languages,
Preply (tutor ecosystem), Anki/SRS. Research current to 2025–2026; patterns only — no content or
design is copied.

## What the leaders converge on

1. **Pathways / structured progression** — every serious product wraps a large content library in a
   *recommended path* (HindiPod101's 100+ "pathways", Rocket's Level 1→3 modules, Duolingo's tree).
   The library without the path is a known failure mode ("learners collect phrases while postponing
   the script"). → EkGuru already has this: `js/learning-paths.js` (6 goal paths).
2. **Conversation-first + audio-first** — Rocket and Mango lead with native-speaker dialogues, then
   break them down (vocabulary, grammar, culture). Transcripts + slow playback + line-by-line audio
   are the standard support layer. → EkGuru's honest gap: browser TTS only, no recorded audio.
3. **Spaced repetition is table stakes** — Duolingo, Mango, Memrise, Anki, HindiPod101 flashcards all
   use SRS. → EkGuru Phase 6 already shipped an SM-2-lite deck.
4. **Level ladder** — beginner→intermediate→advanced, roughly CEFR A1–B2; several products openly
   admit advanced content is thin. → EkGuru matches this honestly (no fabricated advanced).
5. **Progress dashboard + streaks/XP** — motivation layer; not a substitute for learning.
   → EkGuru has device-only progress; honest until a real account backend exists.
6. **Culture alongside language** — Rocket's "Language & Culture" lessons, Mango's chapter
   conversation/grammar goals. → a culture module is part of the Phase 7 content schema.
7. **Offline** — Mango and Rocket both advertise downloadable/offline lessons.
   → EkGuru Phase 6 shipped save-for-offline per lesson.
8. **Tutor bridge as the human layer** — Preply demonstrates the marketplace model; every app
   concedes speech needs a real human. → EkGuru already bridges to 1:1 tutors.

## Patterns explicitly rejected (and why)

| Pattern | Why rejected for EkGuru |
|---|---|
| HindiPod101's weak structure / English overload | Keep a clear path; keep target-language exposure central |
| Mango's uniform flashcard loop (boring, unvaried) | Vary exercise types (quiz/typing/worksheet/dialogue) |
| Duolingo-style gamification as the product | Motivation ≠ learning; no streak-pressured thin content |
| Rocket's small language set + paid lifetime | Stay free, static-first, breadth via *real* content only |
| Thin "level 3 advanced" promises | Never fabricate advanced content; ship when real material exists |
| Mass-generated country/language × country pages | Country data powers context modules, not a page-per-combo |

## Patterns adopted for Phase 7

1. `goal → level → learn → hear → speak → read → write → practice → quiz → review → progress → path → culture → tutor` journey.
2. Reusable engines, not language-specific copies — a new language is **data + content + audio + config**.
3. Deterministic goal-based onboarding (explicitly not "AI personalization").
4. Audio provider abstraction (`BROWSER_TTS | RECORDED | API_TTS | UNAVAILABLE`) so recorded audio can
   slot in later without rewriting lessons.
5. Structured scenario conversation engine, labelled `DETERMINISTIC` until a secure API exists.
6. Country context as metadata → contextual modules (travel / heritage / relocation / work / study),
   never a 194-page dump.

## Sources consulted

- Duolingo review (appstimes.in, 2026): gamified SRS, 40+ languages, speaking/listening exercises.
- Mango Languages (PCMag 2020; langoly.com 2025; App Store/Play listings 2025): conversation-goal +
  grammar-goal framing, choose speaking/listening/reading review, offline, ~60 languages.
- Rocket Languages (languagelearninglegend.com 2026; biopreneur.com.ng 2026; learnlanguagecenter.com
  2026): audio-first long-form dialogues, levels A1–B2, voice recognition, culture lessons, offline.
- HindiPod101 (lingomee.com 2024; fluentin3months.com 2026; alllanguageresources.com 2025):
  podcast lessons, 100+ pathways, word/grammar banks, SRS flashcards, slow playback; weak structure,
  English-heavy, thin advanced.
- Anki: the reference SRS; Memrise: native-speaker video + SRS; Ling: gamified mini-games, native audio.
- Preply: tutor marketplace as the human conversation layer.

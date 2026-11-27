# EkGuru Hindi A1–C2 Product Specification

## Product promise
A six-level Hindi pathway that integrates Devanagari, listening, speech, interaction, reading, writing, mediation, culture and durable memory. “Complete” means evidenced can-do performance by skill—not lesson count.

## Architecture and priorities
**P0 core:** CEFR objective graph; core lessons; Devanagari lab; native-dialogue player; practice engine; quizzes; level tests; SRS; worksheets/offline; mistake review; per-skill progress; accessibility.
**P1 depth:** branching roleplay, writing portfolio/versioning, source library, calibrated community/tutor review, regional audio packs, diagnostics and goal pathways.
**P2 after validation:** Hindi-specific phoneme diagnostics, adaptive AI conversation, teacher dashboard and externally moderated credential.

Each level: 8 thematic units × 4 core lessons. Each unit contains a scenario launch, two language/skill builds, one integrated performance, interleaved review and worksheet. A learner may choose 12–18 minute core, 25–35 minute deep lesson or hands-free audio, but all modes write to one objective graph.

## Ideal lesson sequence (evidence-led, not rigid)
1. **Can-do + retrieval (1–2 min):** reactivate two prerequisites; no untaught trap.
2. **Comprehensible encounter (2–3):** image/situation + normal-speed dialogue before analysis; gist question.
3. **Notice (3–5):** line audio, transcript, literal/natural gloss, sound and one grammar/function contrast.
4. **Guided discrimination (3–4):** listen/select, match, minimal contrast; explanatory feedback.
5. **Guided production (3–5):** build/type/say with scaffold fading.
6. **Interactive transfer (4–8):** new-context dialogue, roleplay, writing or mediation.
7. **Objective quiz (3–5):** mixed unseen items; no hints first attempt.
8. **Repair + SRS:** error-tagged correction, only eligible cards scheduled.
9. **Extension:** worksheet, culture card, authentic-style reading/listening or child/adult scenario swap.
Normal-speed audio returns at end so slow/line mode does not become the target.

## Future course data model (proposal; do not implement in this phase)
```json
{
  "course": {"language":"hi","script":"Devanagari","version":"semver","research_sources":[]},
  "level": {"cefr":"B2","can_do":[],"prerequisites":[],"promotion_policy":{}},
  "unit": {"id":"","theme":"","scenario":"","culture_refs":[],"review_plan":{}},
  "lesson": {
    "id":"","objectives":[],"skills":[],"difficulty":0,"estimated_minutes":0,
    "register":[],"learner_variants":["universal","child","adult"],
    "warmup":[],"input":[],"pronunciation":[],"vocabulary":[],"grammar":[],
    "dialogue":{"turns":[],"audio_assets":[],"transcript":[]},
    "practices":[],"quiz":[],"worksheet":{"tasks":[],"answer_key":[]},
    "srs_candidates":[],"culture":[],"common_mistakes":[],
    "teacher_notes":[],"learner_notes":[],"sources":[],"accessibility":{}
  },
  "asset": {"id":"","type":"audio","provenance":"native|community|tts","speaker":{},"license":"","transcript":""},
  "assessment": {"constructs":[],"items":[],"rubric":{},"parallel_form":"","moderation":{}}
}
```
Required invariants: stable IDs, source/license provenance, target/romanisation/English fields where pedagogically justified, answer alternatives, error taxonomy, register/relationship metadata, accessibility text, schema version and migration strategy. Romanisation defaults visible at early A1 and fades by competence; it remains optional accessibility/remediation, never a permanent script substitute.

## Personalization
Input signals: placement confidence, objective accuracy, response latency, lapses, skill performance, goal and preferred study window. Outputs: next lesson, prerequisite repair, SRS load, scenario skin and optional challenge. Guardrails: never infer age; never lower unseen productive threshold; show why an item is recommended; allow learner override; minimize voice data retention.

## Culture and country context
Culture appears where it changes interpretation: dialogue relationship, culture card, listening speaker note, practice decision and feedback. Longer articles cover language history/media/institutions; country pages handle practical evergreen orientation. Avoid a monolithic “Indian culture.” Label region and setting. Include family, school, work, travel, public service, media and business without assuming religion, caste, gender role or one urban norm. Teach Hinglish descriptively—who uses which switch, with whom and why.

## Accessibility and safeguarding
WCAG-oriented contrast, keyboard operation, screen-reader labels, captions/transcripts, reduced motion, adjustable type, no color-only grammar coding, offline/print equivalence and non-microphone alternative. Child profiles: no public voice/writing by default, guardian/educator controls, age-appropriate scenarios and rewards. Older learners: adjustable pacing, larger text, explicit navigation and printable support.

## Quality gates
| Gate | Objective pass rule |
|---|---|
| lesson | one measurable can-do; prerequisite check; ≥3 input exemplars; comprehension→production→transfer; answer/rationale; no placeholder |
| Hindi | two qualified checks for core grammar/register claims; Devanagari Unicode normalization; natural Hindi; gender/agreement/orthography review |
| translation | proposition, tense/aspect, modality, honorificity and register preserved; literal/natural distinction explicit; alternatives accepted |
| practice | objective coverage; ≥40% productive by B1, ≥60% by C1; no cue leakage; accessibility fallback |
| quiz | item map and plausible misconception distractors; unseen transfer; no duplicated prompt; reliability/item stats after launch |
| worksheet | standalone instructions, print/mobile usability, answer key/rationale, escalating difficulty, productive task |
| audio | provenance/license/speaker metadata; transcript alignment; loudness/clip/noise check; TTS labeled; native core target |
| CEFR | external descriptor mapping + unseen performance; separate skill threshold; completion alone insufficient |
| duplication | normalized exact/near-duplicate scan across titles, examples, dialogues, questions and long strings; intentional spiral tagged |
| culture | setting/region evidence, sensitivity review, no stereotype/generalization, current practical facts dated |
| SEO | unique useful title/summary, canonical URL, structured metadata, no doorway duplication; pedagogy controls page structure |
| accessibility | automated WCAG checks + keyboard/screen-reader/manual audio alternative audit |

### C1 quality gate
Must contain dense unseen audio/text, implicit stance, multi-source synthesis, professional/academic genres, register transformations, idiomatic inference, extended spontaneous interaction and revision. Pass requires C1 rubric in every skill, no skill compensation, rare errors that do not undermine precision, and human moderation of two open performances. Reject if tasks can be passed through explicit connectors, B2 vocabulary substitution or sentence-level recognition.

### C2 quality gate
Must require fine semantic distinctions, implicature/presupposition, rhetorical and stylistic analysis, culturally situated idiom/humour, high-stakes negotiation, expert presentation/Q&A, publishable revision and meaning-preserving recast across genres. Require multi-source critical synthesis, spontaneous interaction and justified translation choices. Reject “C2” based on text length, obscure nouns, grammatical complexity alone or memorized model reproduction.

## Measurement
North-star is verified retained can-do mastery. Report per skill: objectives evidenced, delayed retention, open-task rubric, ASR confidence (practice only), revision gain, SRS burden and transfer success. Audit fairness by age mode/device/input method without storing unnecessary protected attributes. A/B tests may optimize persistence only if mastery and wellbeing do not decline.

## Scale to 194 country contexts
Store global Hindi objective/content core separately from context modules. A context module supplies institution names, currencies/units, service workflows, location-aware scenarios, regional audio and cultural notes; it references core objective IDs but requires original dialogue/passage. Goal packs (travel/family/work/study/heritage) reorder or extend objectives, never falsely skip level evidence. Every local module has owner, sources, review date and fallback generic scenario.

## Build handoff
The next phase should prototype one A1 unit, one B2 unit and one C2 unit to validate data model/player/rubric breadth before full authoring. Freeze research IDs, not prose: linguistic claims remain source-linked and product claims must be rechecked. Production content must be original.

## Evidence register
- **CEFR-CV — CEFR Companion Volume** (framework): action-oriented descriptors, mediation, interaction, phonological control A1–C2. https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16809ea0d4
- **KOUL — Modern Hindi Grammar** (reference grammar): phonology, morphology, agreement, tense/aspect/modality, syntax. https://ikashmir.net/onkoul/pdf/ModernHindiGrammar.pdf
- **UT — Hindi Urdu Flagship grammar resources** (university): aspectual system and compound verb nuance. https://hindi.la.utexas.edu/resources/grammar/
- **CU — Hindi-Urdu Linguistics materials** (university): morphology, auxiliaries, tense/aspect/modality, causatives. https://verbs.colorado.edu/hindiurdu/tutorial_slides/2-hindi-urdu-linguistics-dipti.pptx.pdf
- **ACL — Hindi causatives research** (academic): -ā and -vā morphological causatives. https://www.aclweb.org/anthology/W10-3216.pdf
- **GLOT — Glottolog Hindi** (catalogue): language identity/classification. https://glottolog.org/resource/languoid/id/hind1269
- **UNICODE — Unicode Devanagari chart** (standard): script inventory and encoding. https://www.unicode.org/charts/PDF/U0900.pdf
- **HINDWI — Hindwi Dictionary** (dictionary): Hindi meanings, usage and literary vocabulary; verify entries in context. https://www.hindwidictionary.com/
- **SHABDKOSH — Shabdkosh Hindi-English Dictionary** (dictionary): lexical cross-checking, pronunciation and examples. https://www.shabdkosh.com/
- **CFILT — IIT Bombay Hindi WordNet** (lexical resource): synsets and semantic relations. https://www.cfilt.iitb.ac.in/wordnet/webhwn/
- **TDIL — Government of India TDIL** (government technology): Indian-language digital resources and tools. https://tdil-dc.in/
- **DUO — How Duolingo courses evolve** (official product): CEFR sections, section quizzes, skill integration. https://blog.duolingo.com/how-are-duolingo-courses-evolving/
- **DUO101 — Duolingo 101** (official product): progressive exercise difficulty, mistake-targeted personalized practice. https://blog.duolingo.com/duolingo-101-how-to-learn-a-language-on-duolingo/
- **DUOSCORE — Duolingo Score** (official product): granular progress and can-do communication. https://blog.duolingo.com/duolingo-score/
- **BUSUU — Busuu app listing** (official product listing): study plans, community feedback, vocabulary/grammar review, offline, certificates. https://play.google.com/store/apps/details?id=com.busuu.android&hl=en_GB
- **HP101 — HindiPod101 product features** (official product): native audio/video library, transcripts, PDFs, SRS, assessments, teacher feedback. https://www.hindipod101.com/about-us/business/
- **GLOSS — Glossika** (official product): native-recorded sentence audio and personalized sentence review. https://ai.glossika.com/
- **ANKI — Anki manual: deck options** (official documentation): retrievability-based scheduling and FSRS configuration. https://docs.ankiweb.net/deck-options.html
- **CLOZE — Clozemaster versus Anki** (product analysis): frequency-organized sentence cloze versus customizable cards. https://blog.clozemaster.com/clozemaster-vs-anki/
- **PIMS — Pimsleur method** (official product): graduated interval recall, anticipation, audio lessons. https://www.pimsleur.com/the-pimsleur-method/
- **MANGO — Mango methodology** (official product): conversation, semantic colour mapping, critical-thinking exercises. https://mangolanguages.com/our-methodology/
- **PREPLY — Preply Hindi tutors** (product): live individual tutoring and goal-oriented feedback. https://preply.com/en/online/hindi-tutors
- **ITALKI — italki language learning** (product): teacher marketplace and individualized conversation. https://www.italki.com/
- **DUO-HI-GAP — Post-Duolingo Hindi roadmap** (documented product analysis): observed Hindi A1–A2 ceiling, script-speed, colloquial and register gaps. https://www.clozemaster.com/blog/what-to-do-after-duolingo-hindi/
- **GLOSS-REV — Glossika review** (independent product analysis): sentence SRS strengths; repetition and uncorrected-recording limitations. https://www.fluentu.com/blog/reviews/glossika/
- **HP-REV — HindiPod101 review** (independent product analysis): Devanagari, aspiration/retroflexion, slowed audio; need for live interaction. https://www.fluentin3months.com/reviews/hindipod101-review/

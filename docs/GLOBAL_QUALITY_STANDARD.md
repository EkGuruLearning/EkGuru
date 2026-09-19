# EkGuru Global Quality and AdSense-Readiness Standard

**Status:** P0 publication policy. Applies to every language, country, course, level, lesson, guide, tool, and landing page.

## Primary-purpose rule

Every public URL must be useful to a learner without advertisements. URL count, word count, country-name substitution, machine translation, affiliate intent, or an interactive shell is not sufficient value. Learning content remains the primary purpose and must visually and structurally outweigh advertising.

## Publishability gate

A page may be published or retained as indexable only when all applicable gates pass:

1. **Content exists:** a clear introduction, objective or user intent, substantial original explanation/information, examples or practical context, and an actionable next step.
2. **Useful:** it solves the stated learning or informational need without relying on an advertisement, lead form, or JavaScript-only shell.
3. **Original:** examples, explanations, dialogue, exercises, metadata, and local context are authored for the page. Sources inform work but are not copied.
4. **Not thin:** depth is judged against intent, not an arbitrary word count. Short utility pages can pass when they fully solve a narrow task; broad guides require correspondingly deeper treatment.
5. **Not duplicative:** title, description, introduction, paragraphs, FAQs, examples, and intent are materially distinct. Pages produced by changing only country, language, level, or topic tokens fail.
6. **Language quality:** script, grammar, translation, pronunciation, register, pragmatics, and cultural claims pass language-specific review. C1/C2 pass independent advanced-reality gates.
7. **SEO:** unique title and meta description, one clear H1, canonical, meaningful internal links, appropriate index directive, structured data only when visible content supports it, sitemap consistency, and hreflang only for true alternates.
8. **Accessible and usable:** semantic headings/navigation, keyboard operation, text alternatives, captions/transcripts or equivalent, readable mobile layout, and no essential microphone-only or JavaScript-only path.
9. **Trust:** About, Contact, Privacy, Terms, and applicable cookie/consent information are visible and accurate. Ownership, editorial/source, and reviewed/updated information are present where relevant. No invented author, expert, review, credential, or recognition.
10. **Safe ad experience:** ads do not obscure content/navigation, imitate controls, encourage accidental clicks, create empty layout, or dominate mobile viewport. Synthetic audio and automated feedback are labeled honestly.

Any failed, uncertain, or unreviewed gate results in `REVIEW_REQUIRED`; it must not be mass-published automatically.

## Scalable page rule

For every country × language × level × topic × lesson combination, record its unique intent, unique facts, unique examples, local relevance, and learning outcome. Reusable language instruction belongs in the global language core. A country module may add verified language status, regional usage, locally relevant services, school/work/travel/family situations, communication conventions, and labeled variation. If only names, currency, timezone, or boilerplate change, the page is not a genuine localization and is `REVIEW_REQUIRED`.

## Course gate

Every A1–C2 level must contain substantial explanation, vocabulary, grammar, original dialogue/passage, mixed practice, quiz, worksheet with answers, assessment, reading, writing, and supported listening/speaking/review. Practice must be target-language-specific and span receptive and productive skills. SRS selects high-value items and actual mistakes rather than carding everything.

- **A1–A2:** script/sound where applicable, survival and daily interaction, foundational grammar, basic reading/listening/speaking/writing.
- **B1–B2:** connected narration, repair, source comprehension, argument, professional/social register, increasingly independent production.
- **C1:** implicit stance, advanced discourse, complex grammar, idiom, register transformation, academic/professional synthesis and extended interaction.
- **C2:** semantic precision, presupposition/implication, rhetoric, style, cultural pragmatics, high-stakes interaction, and sophisticated original production. Length or rare vocabulary cannot establish C2.

## Global practice-depth contract

The canonical machine-readable contract is `data/quality/global-practice-standard.json`. The practice **interaction types** are reusable infrastructure; prompts, answers, examples, audio, distractors, linguistic targets, and feedback must be authored for the target language and lesson. Copying the same exercise with language/country tokens replaced fails publication review.

Supported ecosystem:

- **Core:** multiple choice, fill in the blank, translation, reverse translation, matching, reorder, sentence building, word selection, error correction, dialogue completion.
- **Reading:** reading comprehension, paragraph comprehension, main idea, detail identification, inference.
- **Listening:** listening comprehension, dictation, listen and choose, listen and reorder, listen and fill.
- **Speaking:** repeat after audio, pronunciation, shadowing, guided speaking, free response, roleplay.
- **Writing:** sentence writing, short writing, paraphrase, summary, guided composition.
- **Advanced:** register transformation, tone identification, semantic distinction, contextual meaning, argument construction, discourse ordering, style rewriting, idiom interpretation, implied meaning.

No lesson must mechanically contain every format. Coverage is assessed at level scope: A1 prioritizes recognition and controlled production; A2 adds practical multi-step comprehension; B1 requires connected independent production; B2 adds argument and professional/social register; C1 requires inference, discourse, register, and academic/professional work; C2 requires semantic, rhetorical, stylistic, pragmatic, and sophisticated production.

A technically valid level remains `REVIEW_REQUIRED` when its practice ecosystem is narrow. The global audit uses minimum diversity signals of 12/16/20/24/28/32 distinct supported formats for A1/A2/B1/B2/C1/C2 respectively. These are triage floors, not permission to add token exercises: each item must test its lesson, contain a valid answer and options where needed, state a skill target, and render through the player.

Language adaptation is mandatory. Script, romanisation/transliteration, pronunciation, morphology, agreement, word order, register, pragmatics, regional variation, and audio tasks must reflect the language research profile. Examples include Devanagari and honorific agreement in Hindi; kana/kanji, particles, and politeness in Japanese; script and root-pattern awareness where pedagogically appropriate in Arabic; characters, pinyin, and tones in Chinese; liaison and formality in French; and Tamil script, agglutinative grammar, and formal/colloquial contrast in Tamil. These examples do not replace research for any language.

A course completion claim requires separate `CONTENT`, `PRACTICE`, `SKILL_COVERAGE`, `LEVEL_APPROPRIATENESS`, `LANGUAGE_SPECIFIC`, `VOICE_AUDIO` (where applicable), and `PLAYER` gates. `validator errors=0` establishes schema validity only.

## JS and indexability

Interactive practice can deepen a page but cannot be its only indexable value. Important course/guide outcomes need server-delivered headings, summaries, objectives, explanatory text, and internal links. A no-script or static route must still explain what the learner will learn and where to continue.

## Ads and consent

Ad inventory is never a reason to create a URL. Ad code and consent behavior must be audited by region, device, and viewport before approval/launch. Do not call the site “AdSense approved” unless Google has actually approved it. The readiness audit reports factual `PASS`, `PARTIAL`, `FAIL`, or `REVIEW_REQUIRED`, never a fabricated percentage.

## Required recurring audit

Run `python tools/audit-adsense-readiness.py`. Its machine-readable output is `data/quality/adsense-readiness.json`. Run it before substantial publishing batches and after changes to templates, navigation, ads, trust pages, course player, sitemap, or scalable content. The audit is a triage control, not a substitute for editorial, language, accessibility, mobile, policy, or AdSense review.

## Release ownership

A batch owner must repair failed source sections rather than delete valid courses or suppress audit findings. Course production and quality/AdSense readiness are parallel P0 priorities. Audit exceptions require a written reason, reviewer, scope, and expiration date; silent waivers are prohibited.

# -*- coding: utf-8 -*-
"""Hindi C5 — MASTER: translation craft, public oratory, teaching and the classics.

Final EkGuru extension level, authored 16 Nov 2026. All passages are
original EkGuru texts written in the manner of a tradition; no copyrighted
lines are reproduced. Classical forms (dohā, caupāī) are illustrated with
new verses composed for teaching.
"""

TITLE = "Master: Translation, Oratory and Teaching Hindi"
GOALS = [
    "Translate between Hindi and English with register, idiom and rhythm intact.",
    "Compress for subtitles and expand for voice-over without losing tone.",
    "Deliver a structured speech, host a stage and handle a hostile question.",
    "Read dohā and caupāī metre and the Braj/Awadhi grammar they carry.",
    "Explain Hindi grammar to a learner, diagnose errors and design a lesson.",
]

UNITS = [
    # ------------------------------------------------------------------ U1
    {
        "id": "hi-c5-u1",
        "title": "The Craft of Translation",
        "lessons": [
            {
                "id": "hi-c5-l1",
                "title": "Idiom for Idiom, Not Word for Word",
                "learn": "A master translator asks what a phrase does, not what it says. ‘Break a leg’ is not टाँग तोड़ो; it is ‘जाओ, कमाल कर दो’. ‘दाल में कुछ काला है’ is not ‘something black in the lentils’ but ‘something fishy’. When no idiom matches, translate the function in plain words and keep the tone; when the image itself matters, keep it and gloss lightly.",
                "vocab": [
                    ("अनुवाद", "anuvād", "translation", "noun"),
                    ("भावानुवाद", "bhāvānuvād", "sense-for-sense translation", "noun"),
                    ("शब्दानुवाद", "śabdānuvād", "word-for-word translation", "noun"),
                    ("समतुल्य", "samtulya", "equivalent", "adjective"),
                    ("स्रोत भाषा", "srot bhāṣā", "source language", "noun"),
                    ("लक्ष्य भाषा", "lakṣya bhāṣā", "target language", "noun"),
                    ("अर्थ-छाया", "arth-chāyā", "shade of meaning; nuance", "noun"),
                    ("टिप्पणी", "ṭippaṇī", "gloss; note", "noun"),
                ],
                "grammar": {
                    "title": "The three-way choice for every idiom",
                    "explain": "(1) समतुल्य मुहावरा — a target idiom with the same function and register: ‘the last straw’ → ‘ऊँट की पीठ पर आख़िरी तिनका’ (same image, happily) ; ‘once in a blue moon’ → ‘कभी-कभार / ईद का चाँद’. (2) सपाट भावानुवाद — plain sense when no idiom fits: ‘he's on the fence’ → ‘वह अभी तय नहीं कर पाया’. (3) बिम्ब रखकर टिप्पणी — keep the image when it carries culture: ‘उसने नमक-हलाली निभाई’ → ‘he kept faith with the salt he had eaten — stayed loyal’. Never choose (3) in dialogue subtitles; never choose (1) if the target idiom shifts register (a rustic proverb inside a courtroom speech).",
                    "pattern": "function + register → equivalent idiom / plain sense / image + gloss",
                    "examples": [
                        ("It's raining cats and dogs. → मूसलाधार बारिश हो रही है।", "mūslādhār bāriś ho rahī hai.", "(plain sense — Hindi has no animal idiom here; मूसलाधार keeps the force)"),
                        ("उसके पेट में चूहे कूद रहे हैं। → He's starving. / His stomach is growling.", "uske peṭ mẽ cūhe kūd rahe haĩ.", "(equivalent idiom; ‘mice jumping in his stomach’ would puzzle)"),
                        ("अब पछताए होत क्या, जब चिड़िया चुग गई खेत। → No use crying over spilt milk.", "ab pachtāe hot kyā, jab ciṛiyā cug gaī khet.", "(equivalent proverb; same function, same homely register)"),
                    ],
                    "mistakes": [
                        "Word-for-word idiom (‘आँखें चुराना’ → ‘to steal eyes’): translate the function (‘to avoid someone's gaze’).",
                        "Upgrading register: a village grandmother's proverb rendered as Latin-root English.",
                    ],
                },
                "dialogue": [
                    ("संपादक", "यहाँ लिखा है ‘he threw me under the bus’ — आपने ‘बस के नीचे फेंक दिया’ कर दिया?", "yahā̃ likhā hai ‘he threw me under the bus’ — āpne ‘bas ke nīce phẽk diyā’ kar diyā?", "It says ‘he threw me under the bus’ — you've made it ‘threw me under the bus’ literally?"),
                    ("अनुवादक", "हिंदी में कोई बस वाला मुहावरा नहीं है।", "hindī mẽ koī bas vālā muhāvrā nahī̃ hai.", "Hindi has no bus idiom."),
                    ("संपादक", "मुहावरा मत ढूँढिए, काम ढूँढिए। काम है — अपनी जान बचाने के लिए मुझे फँसा दिया।", "muhāvrā mat ḍhū̃ḍhie, kām ḍhū̃ḍhie. kām hai — apnī jān bacāne ke lie mujhe phãsā diyā.", "Don't look for the idiom, look for the job. The job is — he got me into trouble to save himself."),
                    ("अनुवादक", "‘उसने अपनी गर्दन बचाने के लिए मुझे बलि का बकरा बना दिया।’", "‘usne apnī gardan bacāne ke lie mujhe bali kā bakrā banā diyā.’", "‘He made me the scapegoat to save his own neck.’"),
                ],
                "practice": [
                    {"type": "transformation", "q": "Translate to Hindi, idiom for idiom: ‘She let the cat out of the bag.’", "answer": "उसने भेद खोल दिया। / उसने पोल खोल दी।", "skill_target": "idiom equivalence"},
                    {"type": "transformation", "q": "Translate to English: ‘वह अपने मुँह मियाँ मिट्ठू बन रहा है।’", "answer": "He's blowing his own trumpet.", "skill_target": "idiom equivalence"},
                    {"type": "multiple_choice", "q": "Best rendering of ‘नौ दो ग्यारह हो गया’ in a thriller subtitle:", "answer": "He bolted.", "skill_target": "register-matched idiom", "options": ["He became nine-two-eleven.", "He departed expeditiously.", "He bolted.", "He went to eleven."]},
                    {"type": "transformation", "q": "Choose plain sense: ‘He's sitting on the fence about the merger.’", "answer": "विलय पर वह अभी किसी पक्ष में नहीं है।", "skill_target": "plain-sense strategy"},
                    {"type": "transformation", "q": "Keep the image and gloss (literary prose): ‘उसने नमक का हक़ अदा किया।’", "answer": "He paid the debt of salt — stayed loyal to the house that had fed him.", "skill_target": "image + gloss"},
                    {"type": "error_correction", "q": "Fix the register mismatch: courtroom speech, ‘The evidence is conclusive.’ → ‘सबूत दूध का दूध पानी का पानी कर देते हैं।’", "answer": "साक्ष्य निर्णायक हैं।", "skill_target": "register control"},
                    {"type": "guided_composition", "q": "Translate this paragraph into natural Hindi (not word for word): ‘Look, I'm not going to sugar-coat it. The numbers are bad, the board is nervous, and if we don't turn this ship around by March, heads will roll — starting with mine.’", "answer": "देखिए, मैं लीपापोती नहीं करूँगा। आँकड़े ख़राब हैं, बोर्ड घबराया हुआ है, और अगर मार्च तक हमने हालात नहीं सँभाले तो गर्दनें कटेंगी — सबसे पहले मेरी।", "skill_target": "guided translation"},
                ],
                "quiz": [
                    {"q": "भावानुवाद means…", "options": ["word-for-word", "sense-for-sense", "machine translation", "back-translation"], "answer": 1, "why": "भाव = sense."},
                    {"q": "When no equivalent idiom exists, you should…", "options": ["translate literally", "render the plain sense in matching register", "skip the sentence", "add a footnote in subtitles"], "answer": 1, "why": "Function first."},
                    {"q": "Keeping the source image with a gloss suits…", "options": ["subtitles", "literary prose", "legal notices", "SMS"], "answer": 1, "why": "Only where the reader has time and the culture matters."},
                    {"q": "‘अब पछताए होत क्या…’ best matches…", "options": ["Better late than never", "No use crying over spilt milk", "Every cloud has a silver lining", "A stitch in time"], "answer": 1, "why": "Same function: regret after irreversible loss."},
                ],
                "worksheet": {
                    "title": "Idiom Exchange",
                    "tasks": [
                        {"instruction": "Give the best Hindi equivalent and name the strategy.", "items": ["to kill two birds with one stone", "to add fuel to the fire", "to bite the bullet"], "key": ["एक पंथ दो काज (equivalent)", "आग में घी डालना (equivalent)", "कड़वा घूँट पीना (equivalent)"]},
                        {"instruction": "Give the best English equivalent.", "items": ["ऊँट के मुँह में जीरा", "घर का भेदी लंका ढाए", "अपना उल्लू सीधा करना"], "key": ["a drop in the ocean", "the traitor within brings the house down / an inside job", "to feather one's own nest"]},
                        {"instruction": "Translate one page of any English novel's dialogue into Hindi; mark each idiom with strategy 1/2/3.", "items": ["open task"], "key": ["(open — check: no literal idioms, register preserved)"]},
                    ],
                },
                "srs": ["भावानुवाद", "समतुल्य", "अर्थ-छाया", "लक्ष्य भाषा"],
            },
            {
                "id": "hi-c5-l2",
                "title": "Register and Rhythm Across Languages",
                "learn": "English formality lives in Latin-root vocabulary and passive voice; Hindi formality lives in tatsam vocabulary, आप-forms and compound verbs like किया जाना. A legal clause, a tender love note and a street argument each need their own Hindi lexical layer. Beyond words, sentence length and stress must be re-tuned: Hindi carries emphasis by word order and particles (ही, तो, भी), English by stress and cleft sentences.",
                "vocab": [
                    ("प्रयुक्ति", "prayukti", "register (linguistics)", "noun"),
                    ("औपचारिक", "aupcārik", "formal", "adjective"),
                    ("अनौपचारिक", "anaupcārik", "informal", "adjective"),
                    ("लय", "lay", "rhythm", "noun"),
                    ("बलाघात", "balāghāt", "emphasis; stress", "noun"),
                    ("निपात", "nipāt", "emphatic particle (ही, तो, भी)", "noun"),
                    ("पदक्रम", "padkram", "word order", "noun"),
                    ("विधिक", "vidhik", "legal (register)", "adjective"),
                ],
                "grammar": {
                    "title": "Carrying emphasis without italics",
                    "explain": "English: ‘It was RAM who broke it’ / ‘It was Ram who broke it’. Hindi has no stress marking in print; it uses (a) particles — ‘राम ने ही तोड़ा’ (only/precisely Ram), ‘राम ने तो तोड़ा’ (as for Ram…), ‘राम ने भी तोड़ा’ (Ram too); (b) fronting — moving the emphasised word to the start or just before the verb; (c) cleft-like ‘तोड़ने वाला राम था’. Register: formal Hindi prefers tatsam nouns + light verb (निर्णय लिया गया), informal prefers Persian/tadbhav + simple verb (फ़ैसला कर लिया). Match sentence length to genre: legal Hindi tolerates long sentences; dialogue does not.",
                    "pattern": "English stress/cleft → Hindi ही/तो/भी + fronting ; Latin-root formality → tatsam + किया जाना",
                    "examples": [
                        ("It was the manager, not the clerk, who approved it. → स्वीकृति प्रबंधक ने दी थी, लिपिक ने नहीं।", "svīkṛti prabandhak ne dī thī, lipik ne nahī̃.", "(fronting of the object + contrast clause)"),
                        ("I DID call you. → मैंने फ़ोन किया तो था।", "maĩne fon kiyā to thā.", "(तो carries the ‘did’ emphasis)"),
                        ("The tenant shall vacate the premises within thirty days. → किरायेदार तीस दिवस के भीतर परिसर रिक्त करेगा।", "kirāyedār tīs divas ke bhītar parisar rikt karegā.", "(legal register: दिवस, परिसर, रिक्त)"),
                    ],
                    "mistakes": [
                        "Dropping emphasis particles so Hindi reads flat where English was pointed.",
                        "Translating a legal ‘shall’ as चाहिए (ought) instead of the binding future करेगा / किया जाएगा.",
                    ],
                },
                "dialogue": [
                    ("ग्राहक", "अनुबंध में ‘shall’ का अनुवाद आपने ‘चाहिए’ किया है।", "anubandh mẽ ‘shall’ kā anuvād āpne ‘cāhie’ kiyā hai.", "In the contract you've translated ‘shall’ as ‘should’."),
                    ("अनुवादक", "जी, वह सही नहीं है। विधिक ‘shall’ बाध्यकारी है — ‘करेगा’ या ‘किया जाएगा’।", "jī, vah sahī nahī̃ hai. vidhik ‘shall’ bādhyakārī hai — ‘karegā’ yā ‘kiyā jāegā’.", "Yes, that's wrong. Legal ‘shall’ is binding — ‘will do’ or ‘shall be done’."),
                    ("ग्राहक", "और ‘the Party of the First Part’?", "aur ‘the Party of the First Part’?", "And ‘the Party of the First Part’?"),
                    ("अनुवादक", "‘प्रथम पक्ष’। यहाँ तत्सम ही चलेगा; ‘पहली पार्टी’ हास्यास्पद लगेगा।", "‘pratham pakṣ’. yahā̃ tatsam hī calegā; ‘pahlī pārṭī’ hāsyāspad lagegā.", "‘प्रथम पक्ष’. Only tatsam works here; ‘pahli party’ would sound absurd."),
                ],
                "practice": [
                    {"type": "transformation", "q": "Translate with emphasis intact: ‘It was YOU who told them.’", "answer": "उन्हें तुमने ही बताया था।", "skill_target": "emphasis particles"},
                    {"type": "transformation", "q": "Translate with emphasis intact: ‘I did send the report, whatever he says.’", "answer": "वह जो भी कहे, रिपोर्ट मैंने भेजी तो थी।", "skill_target": "emphasis particles"},
                    {"type": "transformation", "q": "Render in legal register: ‘The buyer must pay within 15 days.’", "answer": "क्रेता पंद्रह दिवस के भीतर भुगतान करेगा।", "skill_target": "legal register"},
                    {"type": "transformation", "q": "Render the same sentence as a friend's text message.", "answer": "15 दिन में पैसे दे देना, ठीक?", "skill_target": "informal register"},
                    {"type": "multiple_choice", "q": "Which Hindi best matches ‘Ram, too, failed the exam’?", "answer": "राम भी परीक्षा में फ़ेल हो गया।", "skill_target": "particle choice", "options": ["राम ही परीक्षा में फ़ेल हो गया।", "राम भी परीक्षा में फ़ेल हो गया।", "राम तो परीक्षा में फ़ेल हो गया।", "राम परीक्षा में फ़ेल हो गया।"]},
                    {"type": "error_correction", "q": "Fix the register: wedding invitation, ‘आप लोग ज़रूर आ जाना।’", "answer": "आपकी गरिमामयी उपस्थिति प्रार्थनीय है।", "skill_target": "formal register"},
                    {"type": "guided_composition", "q": "Translate this into Hindi twice — once as a formal public notice, once as a WhatsApp message to neighbours: ‘Water supply will be interrupted on Sunday from 10 a.m. to 2 p.m. for maintenance. Please store water in advance.’", "answer": "सूचना: रविवार को प्रातः 10 बजे से अपराह्न 2 बजे तक रखरखाव कार्य हेतु जलापूर्ति बाधित रहेगी। कृपया पूर्व में जल संग्रह कर लें। / सब लोग — संडे को 10 से 2 पानी नहीं आएगा, मेंटेनेंस है। पहले से भर लेना।", "skill_target": "register switching"},
                ],
                "quiz": [
                    {"q": "Hindi marks ‘only/precisely X’ with…", "options": ["भी", "ही", "तो", "ने"], "answer": 1, "why": "ही = exclusive emphasis."},
                    {"q": "Legal ‘shall’ should become…", "options": ["चाहिए", "करेगा / किया जाएगा", "सकता है", "करता था"], "answer": 1, "why": "It is binding, not advisory."},
                    {"q": "Formal Hindi vocabulary draws mainly on…", "options": ["Portuguese", "tatsam Sanskrit", "English", "Bambaiya"], "answer": 1, "why": "Tatsam carries official/legal register."},
                    {"q": "निपात refers to…", "options": ["word order", "emphatic particles", "rhythm", "a legal clause"], "answer": 1, "why": "ही/तो/भी are निपात."},
                ],
                "worksheet": {
                    "title": "Same Sentence, Three Registers",
                    "tasks": [
                        {"instruction": "Translate into formal, neutral and informal Hindi.", "items": ["Please be seated; the session will begin shortly."], "key": ["कृपया आसन ग्रहण करें; सत्र शीघ्र आरंभ होगा। / बैठ जाइए, सत्र थोड़ी देर में शुरू होगा। / बैठो यार, अभी शुरू होता है।"]},
                        {"instruction": "Mark where the English stress falls and supply the Hindi particle.", "items": ["I never said THAT.", "Even SHE laughed."], "key": ["मैंने वह तो कभी नहीं कहा / ऐसा तो नहीं कहा (तो/ही)", "वह भी हँस पड़ी (भी)"]},
                        {"instruction": "Take one clause from any rental agreement and translate it; then explain each tatsam choice.", "items": ["open task"], "key": ["(open — check: binding future, tatsam nouns)"]},
                    ],
                },
                "srs": ["प्रयुक्ति", "निपात", "बलाघात", "विधिक"],
            },
            {
                "id": "hi-c5-l3",
                "title": "Subtitling and Voice-over: Compress, Expand, Sync",
                "learn": "A subtitle gets about 35 Devanagari characters per line, two lines, on screen for under six seconds; the translator must cut without losing the joke or the threat. A voice-over has the opposite problem: Hindi often runs longer than English, so the dub script must be timed to lip-flaps and breath. Masters cut function words and hedges first, names and numbers never.",
                "vocab": [
                    ("उपशीर्षक", "upśīrṣak", "subtitle", "noun"),
                    ("डबिंग", "ḍabiṅg", "dubbing", "noun"),
                    ("संक्षेपण", "saṅkṣepaṇ", "compression", "noun"),
                    ("पठन-गति", "paṭhan-gati", "reading speed", "noun"),
                    ("समकालन", "samkālan", "synchronisation", "noun"),
                    ("होंठ-मिलान", "hõṭh-milān", "lip-sync", "noun"),
                    ("संवाद-लेखक", "saṃvād-lekhak", "dialogue writer", "noun"),
                    ("अभिव्यक्ति", "abhivyakti", "expression", "noun"),
                ],
                "grammar": {
                    "title": "What to cut, what to keep",
                    "explain": "Cut order for subtitles: (1) fillers and hedges (देखिए, दरअसल, मेरा मतलब); (2) vocatives after the first (भाई, यार); (3) redundant auxiliaries where tense is clear (‘जा रहा हूँ’ → ‘जा रहा’) ; (4) one of two synonyms. Keep: proper names, numbers, negation, the punch-word of a joke, any threat or promise. For dubbing, expand or contract with light verbs (कर देना / कर लेना) and vocatives to hit syllable count; place the stressed Hindi word on the visible lip-closure (प/ब/म) where possible.",
                    "pattern": "subtitle: ≤2 lines × ~35 chars, cut fillers → keep names/numbers/negation ; dub: match syllables + stressed labials to lip-flaps",
                    "examples": [
                        ("EN: ‘Look, I'm not saying it was your fault, but someone left the gate open.’ → SUB: तुम्हारी ग़लती नहीं कह रहा — / पर गेट किसी ने खुला छोड़ा।", "tumhārī galtī nahī̃ kah rahā — / par geṭ kisī ne khulā choṛā.", "(filler ‘Look’ dropped, negation and ‘gate’ kept, 2 lines)"),
                        ("EN (1.2 s): ‘Not today.’ → DUB: ‘आज नहीं।’", "āj nahī̃.", "(syllable-matched; नहीं's closing lip works for ‘today’)"),
                        ("EN: ‘Seventeen people saw you.’ → SUB: सत्रह लोगों ने देखा तुम्हें।", "satrah logõ ne dekhā tumhẽ.", "(number kept exactly; object postposed for emphasis)"),
                    ],
                    "mistakes": [
                        "Cutting the number or the name to save space: those are what the viewer needs.",
                        "Dub lines that are grammatical but 40% longer than the mouth movement.",
                    ],
                },
                "dialogue": [
                    ("निर्देशक", "यह लाइन होंठों से डेढ़ सेकंड आगे निकल रही है।", "yah lāin hõṭhõ se ḍeṛh sekaṇḍ āge nikal rahī hai.", "This line runs a second and a half past the lips."),
                    ("संवाद-लेखक", "‘मैं तुम्हें यह बताना चाहता था कि मैं जा रहा हूँ’ — बहुत लंबा है।", "‘maĩ tumhẽ yah batānā cāhtā thā ki maĩ jā rahā hū̃’ — bahut lambā hai.", "‘I wanted to tell you that I am leaving’ — too long."),
                    ("निर्देशक", "अंग्रेज़ी में सिर्फ़ ‘I'm leaving’ है। चार सिलेबल।", "aṅgrezī mẽ sirf ‘I'm leaving’ hai. cār silebal.", "The English is just ‘I'm leaving’. Four syllables."),
                    ("संवाद-लेखक", "‘मैं चला।’ — और ‘म’ पर होंठ बंद भी होंगे।", "‘maĩ calā.’ — aur ‘ma’ par hõṭh band bhī hõge.", "‘I'm off.’ — and the lips close on ‘m’ too."),
                ],
                "practice": [
                    {"type": "transformation", "q": "Subtitle in ≤2 lines of ~35 chars: ‘Honestly, I think we should probably just call the whole thing off before anyone gets hurt.’", "answer": "किसी को चोट लगे उससे पहले / यह सब बंद कर देते हैं।", "skill_target": "compression"},
                    {"type": "transformation", "q": "Subtitle: ‘Twenty-two years, Vikram. Twenty-two years and not one phone call.’", "answer": "बाईस साल, विक्रम। / बाईस साल, और एक फ़ोन तक नहीं।", "skill_target": "compression (keep numbers/names)"},
                    {"type": "transformation", "q": "Dub line, 3 syllables, lip-closure at end: ‘Let him go.’", "answer": "जाने दो। / छोड़ो उसे।", "skill_target": "syllable matching"},
                    {"type": "multiple_choice", "q": "Which cut is wrong for a subtitle of ‘Look, Ravi, forty crore is not a small amount’?", "answer": "cutting ‘forty crore’", "skill_target": "cut priorities", "options": ["cutting ‘Look’", "cutting ‘Ravi’ if said earlier", "cutting ‘forty crore’", "none of these"]},
                    {"type": "transformation", "q": "Expand for dub to ~8 syllables keeping tone: EN ‘Fine. Whatever.’ (character sulking)", "answer": "ठीक है, जो मर्ज़ी करो।", "skill_target": "expansion"},
                    {"type": "error_correction", "q": "This subtitle lost the joke. Fix it: EN ‘I'm on a seafood diet — I see food and I eat it.’ → ‘मैं समुद्री भोजन की डाइट पर हूँ।’", "answer": "मेरी डाइट सीधी है — / जो दिखता है, खा लेता हूँ।", "skill_target": "preserving function"},
                    {"type": "guided_composition", "q": "Subtitle this 4-line exchange (each ≤2 lines): A: ‘You said you'd be here at nine.’ B: ‘Traffic.’ A: ‘For two hours?’ B: ‘It's Jaipur, what do you want from me?’", "answer": "A: नौ बजे आने को कहा था। / B: ट्रैफ़िक। / A: दो घंटे? / B: जयपुर है, क्या करूँ?", "skill_target": "guided subtitling"},
                ],
                "quiz": [
                    {"q": "First thing to cut in a long subtitle:", "options": ["numbers", "names", "fillers and hedges", "negation"], "answer": 2, "why": "Fillers carry least information."},
                    {"q": "Hindi dub scripts usually need to…", "options": ["expand", "compress relative to English", "stay identical", "add songs"], "answer": 1, "why": "Hindi tends to run longer than English."},
                    {"q": "होंठ-मिलान means…", "options": ["subtitle", "lip-sync", "reading speed", "dialogue writer"], "answer": 1, "why": "Matching speech to visible lip movement."},
                    {"q": "A subtitle should stay on screen…", "options": ["under one second", "under six seconds", "twenty seconds", "until the scene ends"], "answer": 1, "why": "Standard reading-speed limit."},
                ],
                "worksheet": {
                    "title": "Thirty-five Characters",
                    "tasks": [
                        {"instruction": "Compress to one line (~35 chars).", "items": ["मैं तो आपसे यही कहना चाह रहा था कि हमें अब निकल जाना चाहिए।", "दरअसल बात यह है कि पैसे अभी तक नहीं आए हैं।"], "key": ["अब निकलना चाहिए।", "पैसे अभी तक नहीं आए।"]},
                        {"instruction": "Write a dub line with the given syllable count and tone.", "items": ["4 syllables, angry: ‘Get out.’", "6 syllables, tender: ‘I missed you.’"], "key": ["निकल जाओ। / बाहर जाओ।", "बहुत याद आई।"]},
                        {"instruction": "Subtitle two minutes of any English scene into Hindi; check every line against the 2×35 rule.", "items": ["open task"], "key": ["(open — check: names/numbers/negation preserved)"]},
                    ],
                },
                "srs": ["उपशीर्षक", "संक्षेपण", "समकालन", "होंठ-मिलान"],
            },
        ],
    },
    # ------------------------------------------------------------------ U2
    {
        "id": "hi-c5-u2",
        "title": "Public Hindi: Stage, Speech and Debate",
        "lessons": [
            {
                "id": "hi-c5-l4",
                "title": "Anchoring a Stage: Mañc Sañcālan",
                "learn": "Indian stage anchoring has a liturgy: welcome, lamp-lighting, introduction of dignitaries in rank order, a couplet before each item, thanks at the end. The anchor's Hindi is slightly elevated, rhythmic, and never upstages the performer. Masters prepare transitions in advance and improvise only the filler when a performer is late.",
                "vocab": [
                    ("मंच संचालन", "mañc sañcālan", "stage anchoring", "noun"),
                    ("दीप प्रज्वलन", "dīp prajvalan", "lamp lighting", "noun"),
                    ("मुख्य अतिथि", "mukhya atithi", "chief guest", "noun"),
                    ("अध्यक्षता", "adhyakṣtā", "presiding; chairing", "noun"),
                    ("स्वागत भाषण", "svāgat bhāṣaṇ", "welcome address", "noun"),
                    ("धन्यवाद ज्ञापन", "dhanyavād gyāpan", "vote of thanks", "noun"),
                    ("करतल ध्वनि", "kartal dhvani", "applause", "noun"),
                    ("सादर आमंत्रित", "sādar āmantrit", "respectfully invited", "phrase"),
                ],
                "grammar": {
                    "title": "Formulae and the rank-order rule",
                    "explain": "Opening: ‘मंच पर विराजमान … , आदरणीय … , एवं उपस्थित सभी सुधीजनों को सादर नमस्कार।’ Rank order: chief guest → presiding officer → guests of honour → host institution head; mention names with designation first time, designation only after. Invitation formula: ‘मैं … जी से सादर अनुरोध करूँगा/करूँगी कि वे मंच पर पधारें।’ Item transition: one line of verse or a one-sentence bridge, then ‘प्रस्तुत है …’. Applause cue: ‘करतल ध्वनि से स्वागत कीजिए’. Closing: धन्यवाद ज्ञापन by someone else, anchor only announces it. Keep each anchor turn under 40 seconds.",
                    "pattern": "नमस्कार (rank order) → दीप प्रज्वलन → स्वागत → items with bridge + ‘प्रस्तुत है’ → धन्यवाद ज्ञापन",
                    "examples": [
                        ("मंच पर विराजमान मुख्य अतिथि श्रीमती … , कार्यक्रम की अध्यक्षता कर रहे प्रो. … , एवं उपस्थित सभी सुधीजनों को सादर नमस्कार।", "mañc par virājmān mukhya atithi śrīmatī …, kāryakram kī adhyakṣtā kar rahe pro. …, evaṃ upasthit sabhī sudhījanõ ko sādar namaskār.", "Respectful greetings to the chief guest seated on the dais, Mrs …, to Prof. … presiding, and to all the learned audience."),
                        ("अब मैं मुख्य अतिथि महोदया से सादर अनुरोध करूँगी कि वे दीप प्रज्वलित कर कार्यक्रम का शुभारंभ करें।", "ab maĩ mukhya atithi mahodayā se sādar anurodh karū̃gī ki ve dīp prajvalit kar kāryakram kā śubhārambh karẽ.", "I now respectfully request the chief guest to light the lamp and inaugurate the programme."),
                        ("सुरों की इस यात्रा में अगला पड़ाव — कक्षा नौ की छात्राओं द्वारा समूह-गान। करतल ध्वनि से स्वागत कीजिए।", "surõ kī is yātrā mẽ aglā paṛāv — kakṣā nau kī chātrāõ dvārā samūh-gān. kartal dhvani se svāgat kījie.", "The next stop on this journey of melody — a group song by the girls of class nine. Please welcome them with applause."),
                    ],
                    "mistakes": [
                        "Getting the rank order wrong (naming the principal before the chief guest) — the room notices.",
                        "Long anchor monologues between items: the audience came for the items.",
                    ],
                },
                "dialogue": [
                    ("आयोजक", "मुख्य अतिथि लेट हैं। मंच पर दो मिनट खींचने हैं।", "mukhya atithi leṭ haĩ. mañc par do minaṭ khī̃cne haĩ.", "The chief guest is late. Stretch two minutes on stage."),
                    ("संचालिका", "ठीक है — मैं संस्था का संक्षिप्त परिचय और आज के कार्यक्रम की रूपरेखा बता देती हूँ।", "ṭhīk hai — maĩ sansthā kā saṅkṣipt paricay aur āj ke kāryakram kī rūprekhā batā detī hū̃.", "Fine — I'll give a brief introduction to the institution and today's outline."),
                    ("आयोजक", "और नाम का क्रम?", "aur nām kā kram?", "And the order of names?"),
                    ("संचालिका", "पहले मुख्य अतिथि, फिर अध्यक्ष, फिर विशिष्ट अतिथि, अंत में प्राचार्य जी। लिखा हुआ है।", "pahle mukhya atithi, phir adhyakṣ, phir viśiṣṭ atithi, ant mẽ prācārya jī. likhā huā hai.", "Chief guest first, then the chair, then guests of honour, the principal last. It's written down."),
                ],
                "practice": [
                    {"type": "reorder", "q": "Order the greetings: प्राचार्य / मुख्य अतिथि / विशिष्ट अतिथि / अध्यक्ष", "answer": "मुख्य अतिथि, अध्यक्ष, विशिष्ट अतिथि, प्राचार्य", "skill_target": "rank order"},
                    {"type": "fill_in_the_blank", "q": "मैं डॉ. मीना जी से ____ ____ करूँगा कि वे मंच पर पधारें।", "answer": "सादर अनुरोध", "skill_target": "invitation formula"},
                    {"type": "transformation", "q": "Write a one-sentence bridge into a classical dance item.", "answer": "शब्द जहाँ थम जाते हैं, वहाँ से मुद्राएँ बोलती हैं — प्रस्तुत है भरतनाट्यम।", "skill_target": "bridge line"},
                    {"type": "multiple_choice", "q": "Who normally delivers the धन्यवाद ज्ञापन?", "answer": "a host-institution representative, announced by the anchor", "skill_target": "protocol", "options": ["the chief guest", "the anchor", "a host-institution representative, announced by the anchor", "the audience"]},
                    {"type": "transformation", "q": "Make it stage-appropriate: ‘अब मीना गाना गाएगी।’", "answer": "अब प्रस्तुत है एक सुमधुर गीत, स्वर हैं मीना शर्मा के। करतल ध्वनि से स्वागत कीजिए।", "skill_target": "register lift"},
                    {"type": "error_correction", "q": "Trim this anchor turn to under 40 seconds (remove upstaging): ‘…और मुझे याद है जब मैं छोटी थी तो मैंने भी यही गीत गाया था और सबने बहुत तारीफ़ की थी, तो आज जब मैं यह गीत सुनूँगी तो मुझे अपना बचपन याद आएगा, ख़ैर, अब प्रस्तुत है…’", "answer": "यह गीत कई पीढ़ियों का बचपन है। प्रस्तुत है — कक्षा छह की ओर से।", "skill_target": "brevity"},
                    {"type": "guided_composition", "q": "Write a full 90-second anchor script for a school annual day: greeting in rank order, lamp-lighting request, bridge into the first item.", "answer": "(Model) मंच पर विराजमान मुख्य अतिथि श्री अरुण वर्मा जी, कार्यक्रम की अध्यक्षता कर रहीं प्रबंध समिति की अध्यक्षा श्रीमती निशा जैन जी, विशिष्ट अतिथि डॉ. राकेश मीणा जी, प्राचार्य महोदय, अभिभावकगण एवं प्यारे विद्यार्थियों — सादर नमस्कार। आज का दिन इस विद्यालय के लिए वर्ष भर की साधना का उत्सव है। अब मैं मुख्य अतिथि महोदय से सादर अनुरोध करूँगी कि वे दीप प्रज्वलित कर कार्यक्रम का शुभारंभ करें। … ज्ञान का दीप जल चुका है; अब सुरों का। प्रस्तुत है सरस्वती वंदना — करतल ध्वनि से स्वागत कीजिए।", "skill_target": "guided composition"},
                ],
                "quiz": [
                    {"q": "करतल ध्वनि means…", "options": ["silence", "applause", "lamp", "song"], "answer": 1, "why": "Literally ‘palm-sound’."},
                    {"q": "Who is named first in the greeting?", "options": ["principal", "chief guest", "anchor", "students"], "answer": 1, "why": "Rank order starts with the chief guest."},
                    {"q": "The anchor's turn between items should be…", "options": ["5 minutes", "under 40 seconds", "a full speech", "silent"], "answer": 1, "why": "Bridges, not monologues."},
                    {"q": "‘पधारें’ is…", "options": ["a rude imperative", "an honorific ‘please come’", "a past tense", "a noun"], "answer": 1, "why": "Honorific subjunctive used in invitations."},
                ],
                "worksheet": {
                    "title": "Run of Show",
                    "tasks": [
                        {"instruction": "Write the invitation line for each.", "items": ["chief guest to light the lamp", "principal to give the welcome address"], "key": ["मुख्य अतिथि महोदय से सादर अनुरोध है कि वे दीप प्रज्वलित करें।", "प्राचार्य महोदय से अनुरोध है कि वे स्वागत भाषण प्रस्तुत करें।"]},
                        {"instruction": "Write one-line bridges into: a comedy skit; a tribute to a retiring teacher.", "items": ["skit", "tribute"], "key": ["अब थोड़ी हँसी — क्योंकि हँसी भी एक कला है। प्रस्तुत है…", "कुछ विदाइयाँ विदाई नहीं होतीं; वे कृतज्ञता होती हैं। आइए…"]},
                        {"instruction": "Prepare a two-minute filler on the host institution for a late-guest emergency.", "items": ["open task"], "key": ["(open — check: factual, warm, no upstaging)"]},
                    ],
                },
                "srs": ["मंच संचालन", "मुख्य अतिथि", "धन्यवाद ज्ञापन", "करतल ध्वनि"],
            },
            {
                "id": "hi-c5-l5",
                "title": "The Structured Speech: Hook, Three Points, Return",
                "learn": "A persuasive Hindi speech opens with a hook — a story, a question or a line of verse — states its one idea, develops three points with a concrete example each, and returns to the opening image in the last sentence. Rhetoric lives in तीन की लय (triads), अनुप्रास, deliberate repetition (पुनरावृत्ति) and the pause. Masters write for the ear: short clauses, spoken connectors, no sentence they cannot say in one breath.",
                "vocab": [
                    ("वक्तृत्व", "vaktṛtva", "oratory", "noun"),
                    ("वक्ता", "vaktā", "speaker", "noun"),
                    ("श्रोता", "śrotā", "listener; audience", "noun"),
                    ("प्रस्तावना", "prastāvnā", "introduction", "noun"),
                    ("पुनरावृत्ति", "punarāvṛtti", "repetition (rhetorical)", "noun"),
                    ("त्रिक", "trik", "triad; rule of three", "noun"),
                    ("विराम", "virām", "pause", "noun"),
                    ("उपसंहार", "upsaṃhār", "conclusion", "noun"),
                ],
                "grammar": {
                    "title": "Writing for the ear",
                    "explain": "Spoken syntax: subject + short predicate; put the key word last in the clause where Hindi naturally stresses it. Triads: ‘न सड़क थी, न स्कूल था, न उम्मीद थी।’ Anaphora: begin three consecutive sentences with the same phrase (‘हम वे लोग हैं जो…’). Rhetorical question followed by the answer. Contrast pair: ‘सवाल पैसे का नहीं, नीयत का है।’ Mark pauses in the script with ‘/’; a pause before the key word doubles its weight. Conclusion: do not summarise; return to the opening image, changed.",
                    "pattern": "hook → one idea → 3 points (each: claim + concrete example + line to remember) → return to the hook",
                    "examples": [
                        ("न सड़क थी, / न स्कूल था, / न उम्मीद थी। / आज तीनों हैं — / और तीनों इस गाँव ने ख़ुद बनाए।", "na saṛak thī, / na skūl thā, / na ummīd thī. / āj tīnõ haĩ — / aur tīnõ is gā̃v ne khud banāe.", "No road, no school, no hope. Today all three exist — and all three this village built itself."),
                        ("सवाल यह नहीं कि हम कर सकते हैं या नहीं। / सवाल यह है कि हम करेंगे या नहीं।", "savāl yah nahī̃ ki ham kar sakte haĩ yā nahī̃. / savāl yah hai ki ham karẽge yā nahī̃.", "The question is not whether we can. The question is whether we will."),
                        ("मैंने शुरुआत एक बच्ची की तस्वीर से की थी। / वह बच्ची आज इस मंच पर है — / और वह मैं हूँ।", "maĩne śuruāt ek baccī kī tasvīr se kī thī. / vah baccī āj is mañc par hai — / aur vah maĩ hū̃.", "I began with a photo of a girl. That girl is on this stage today — and she is me. (return to the hook)"),
                    ],
                    "mistakes": [
                        "Written-Hindi sentences (long तत्सम chains with यद्यपि…तथापि) that cannot be said in one breath.",
                        "Ending with ‘इन्हीं शब्दों के साथ मैं अपनी वाणी को विराम देता हूँ’ — a cliché that throws away the strongest slot.",
                    ],
                },
                "dialogue": [
                    ("प्रशिक्षक", "आपका भाषण पढ़ा। तीसरे पैराग्राफ़ का वाक्य इकतालीस शब्दों का है।", "āpkā bhāṣaṇ paṛhā. tīsre pairāgrāf kā vākya iktālīs śabdõ kā hai.", "I read your speech. The sentence in paragraph three is forty-one words long."),
                    ("वक्ता", "लिखने में ठीक लग रहा था।", "likhne mẽ ṭhīk lag rahā thā.", "It looked fine on paper."),
                    ("प्रशिक्षक", "बोलकर देखिए। जहाँ साँस टूटे, वहाँ वाक्य तोड़िए। और अंत में ‘वाणी को विराम’ मत दीजिए — पहली तस्वीर पर लौटिए।", "bolkar dekhie. jahā̃ sā̃s ṭūṭe, vahā̃ vākya toṛie. aur ant mẽ ‘vāṇī ko virām’ mat dījie — pahlī tasvīr par lauṭie.", "Say it aloud. Break the sentence where your breath breaks. And don't end with ‘I rest my voice’ — return to the first image."),
                    ("वक्ता", "तो आख़िरी पंक्ति वही बच्ची, वही सड़क।", "to ākhirī paṅkti vahī baccī, vahī saṛak.", "So the last line is the same girl, the same road."),
                ],
                "practice": [
                    {"type": "transformation", "q": "Rewrite for the ear (break into breath-length clauses): ‘यद्यपि हमारे विद्यालय में संसाधनों की कमी है तथापि हमारे शिक्षकों की निष्ठा के कारण परिणाम निरंतर सुधर रहे हैं।’", "answer": "संसाधन कम हैं। / शिक्षक नहीं। / इसलिए परिणाम हर साल बेहतर हैं।", "skill_target": "spoken syntax"},
                    {"type": "transformation", "q": "Build a triad on ‘water’ for a village speech.", "answer": "पानी खेत के लिए, / पानी घर के लिए, / पानी कल के लिए।", "skill_target": "rule of three"},
                    {"type": "transformation", "q": "Write a contrast pair: money vs intention.", "answer": "कमी पैसे की नहीं है, कमी नीयत की है।", "skill_target": "antithesis"},
                    {"type": "multiple_choice", "q": "The best way to end a speech is…", "answer": "return to the opening image, changed", "skill_target": "conclusion", "options": ["a summary of all points", "‘वाणी को विराम देता हूँ’", "return to the opening image, changed", "a new topic"]},
                    {"type": "fill_in_the_blank", "q": "Beginning three sentences with the same phrase is called ____ (Hindi term).", "answer": "पुनरावृत्ति", "skill_target": "terminology"},
                    {"type": "error_correction", "q": "Mark pauses (/) so the key word lands: ‘इस गाँव ने सरकार का इंतज़ार नहीं किया इसने ख़ुद सड़क बनाई।’", "answer": "इस गाँव ने / सरकार का इंतज़ार नहीं किया। / इसने ख़ुद / सड़क बनाई।", "skill_target": "pausing"},
                    {"type": "guided_composition", "q": "Write a three-minute speech (≈350 words) for a college debate on ‘क्या शहरों में निजी वाहनों पर रोक लगनी चाहिए?’ — hook, one idea, three points with examples, return.", "answer": "(Model opening & close) सुबह सात बजे, / टोंक रोड, / एक एम्बुलेंस / और उसके आगे खड़ी दो हज़ार कारें — / जिनमें से हर एक में / बैठा है एक आदमी। / एक। / मेरा विषय वही एक आदमी है। … / वही टोंक रोड, / वही सात बजे — / पर इस बार एम्बुलेंस निकल गई, / क्योंकि दो हज़ार कारें / बीस बसें बन गईं। / सवाल सुविधा का नहीं है; / सवाल उस एक एम्बुलेंस का है।", "skill_target": "guided composition"},
                ],
                "quiz": [
                    {"q": "A speech sentence should be…", "options": ["as long as possible", "sayable in one breath", "all tatsam", "a question"], "answer": 1, "why": "Write for the ear."},
                    {"q": "त्रिक refers to…", "options": ["a pause", "the rule of three", "a conclusion", "a hook"], "answer": 1, "why": "Three parallel items."},
                    {"q": "A pause before the key word…", "options": ["weakens it", "doubles its weight", "is a grammar error", "is only for poetry"], "answer": 1, "why": "Silence frames emphasis."},
                    {"q": "‘सवाल पैसे का नहीं, नीयत का है’ is…", "options": ["a triad", "a contrast pair", "a hook", "a filler"], "answer": 1, "why": "Antithesis in two halves."},
                ],
                "worksheet": {
                    "title": "Speech Skeleton",
                    "tasks": [
                        {"instruction": "Write a hook of ≤30 words for each topic.", "items": ["plastic waste", "reading habits"], "key": ["(open — story, question or verse; concrete image)"]},
                        {"instruction": "Write one triad and one anaphora set on ‘teachers’.", "items": ["त्रिक", "पुनरावृत्ति"], "key": ["जो पढ़ाते हैं, जो सँभालते हैं, जो याद रह जाते हैं। / हमने सीखा… हमने सीखा… हमने सीखा…"]},
                        {"instruction": "Record yourself delivering a one-minute speech; mark every place you ran out of breath and rewrite those sentences.", "items": ["open task"], "key": ["(open)"]},
                    ],
                },
                "srs": ["वक्तृत्व", "पुनरावृत्ति", "त्रिक", "उपसंहार"],
            },
            {
                "id": "hi-c5-l6",
                "title": "Debate and the Hostile Question",
                "learn": "In a Hindi debate or press Q&A the master does four things in order: acknowledge (‘अच्छा सवाल है’ only if it is), reframe the loaded premise, answer in one sentence, then bridge to the point they want to make. The tone stays warm; the grammar stays declarative. Never repeat a hostile phrase — repeat the correction instead.",
                "vocab": [
                    ("वाद-विवाद", "vād-vivād", "debate", "noun"),
                    ("पक्ष", "pakṣ", "side; the proposition", "noun"),
                    ("विपक्ष", "vipakṣ", "opposition", "noun"),
                    ("पूर्वग्रह", "pūrvgrah", "bias; loaded premise", "noun"),
                    ("पुनर्संरचना", "punarsaṃracnā", "reframing", "noun"),
                    ("सेतु", "setu", "bridge (to your message)", "noun"),
                    ("खंडन", "khaṇḍan", "rebuttal", "noun"),
                    ("संयम", "saṃyam", "composure; restraint", "noun"),
                ],
                "grammar": {
                    "title": "ABAB: acknowledge, reframe, answer, bridge",
                    "explain": "Acknowledge: ‘आपने ज़रूरी मुद्दा उठाया।’ Reframe the loaded premise without repeating it: Q ‘आपकी नाकाम योजना पर कितना पैसा बर्बाद हुआ?’ → ‘योजना का पहला चरण पूरा हुआ है; व्यय और परिणाम दोनों सार्वजनिक हैं।’ Answer in one declarative sentence with a number if you have one. Bridge: ‘और असल बात यह है कि …’ / ‘इससे भी ज़रूरी सवाल यह है कि …’. Rebuttal in debate: name the opponent's claim neutrally (‘विपक्ष का कहना है कि …’), give the missing fact, conclude with ‘इसलिए’. Composure devices: slow down, lower volume, use आप throughout.",
                    "pattern": "स्वीकार → पुनर्संरचना (don't echo the slur) → एक-वाक्य उत्तर (+ number) → सेतु",
                    "examples": [
                        ("प्रश्न: ‘आपकी नाकाम योजना पर कितना पैसा बर्बाद हुआ?’ उत्तर: ‘योजना का पहला चरण पूरा हुआ है — बारह करोड़ व्यय, चार सौ घर। असल सवाल यह है कि दूसरे चरण में गति कैसे बढ़े।’", "praśn: ‘āpkī nākām yojnā par kitnā paisā barbād huā?’ uttar: ‘yojnā kā pahlā caraṇ pūrā huā hai — bārah karoṛ vyay, cār sau ghar. asal savāl yah hai ki dūsre caraṇ mẽ gati kaise baṛhe.’", "Q: ‘How much money was wasted on your failed scheme?’ A: ‘The first phase is complete — twelve crore spent, four hundred homes. The real question is how to speed up phase two.’"),
                        ("विपक्ष का कहना है कि निजी वाहनों पर रोक से व्यापार प्रभावित होगा। आँकड़ा यह है कि पैदल-क्षेत्रों में दुकानों की बिक्री बढ़ी है। इसलिए रोक व्यापार के विरुद्ध नहीं, उसके पक्ष में है।", "vipakṣ kā kahnā hai ki nijī vāhanõ par rok se vyāpār prabhāvit hogā. ā̃kṛā yah hai ki paidal-kṣetrõ mẽ dukānõ kī bikrī baṛhī hai. islie rok vyāpār ke viruddh nahī̃, uske pakṣ mẽ hai.", "The opposition says a car ban will hurt trade. The figure is that shop sales rose in pedestrian zones. Therefore the ban is not against trade but for it."),
                        ("‘मैं आपकी बात समझता हूँ, और मैं असहमत हूँ — इसलिए कि …’", "‘maĩ āpkī bāt samajhtā hū̃, aur maĩ asahmat hū̃ — islie ki …’", "‘I understand your point, and I disagree — because …’ (composure formula)"),
                    ],
                    "mistakes": [
                        "Echoing the hostile word (‘नाकाम योजना नहीं है!’) — now you have said it too.",
                        "Answering a yes/no trap with a paragraph; give the one sentence first.",
                    ],
                },
                "dialogue": [
                    ("पत्रकार", "आप मानते हैं कि आपकी टीम ने जनता को गुमराह किया?", "āp mānte haĩ ki āpkī ṭīm ne jantā ko gumrāh kiyā?", "Do you admit your team misled the public?"),
                    ("प्रवक्ता", "हमने हर आँकड़ा उसी दिन वेबसाइट पर डाला था जिस दिन वह आया। तारीख़ें वहीं हैं।", "hamne har ā̃kṛā usī din vebsāiṭ par ḍālā thā jis din vah āyā. tārīkhẽ vahī̃ haĩ.", "We put every figure on the website the day it arrived. The dates are there."),
                    ("पत्रकार", "तो गुमराह नहीं किया?", "to gumrāh nahī̃ kiyā?", "So you didn't mislead?"),
                    ("प्रवक्ता", "जानकारी सार्वजनिक थी। और असल सवाल यह है कि अगली रिपोर्ट कब आएगी — पंद्रह तारीख़ को।", "jānkārī sārvajanik thī. aur asal savāl yah hai ki aglī riporṭ kab āegī — pandrah tārīkh ko.", "The information was public. And the real question is when the next report comes — on the fifteenth."),
                ],
                "practice": [
                    {"type": "transformation", "q": "Reframe without echoing: ‘आपकी बेकार ऐप पर बच्चे समय क्यों बर्बाद करें?’", "answer": "ऐप पर औसत सत्र बाईस मिनट का है और पठन-गति में सुधार दर्ज हुआ है। असल सवाल यह है कि इसे और स्कूलों तक कैसे पहुँचाएँ।", "skill_target": "reframing"},
                    {"type": "transformation", "q": "Answer the yes/no trap in one sentence first: ‘क्या आपने कभी नियम तोड़ा?’", "answer": "नहीं। और जहाँ नियम अस्पष्ट था, वहाँ हमने लिखित स्पष्टीकरण माँगा।", "skill_target": "one-sentence answer"},
                    {"type": "transformation", "q": "Write a rebuttal: opponent says ‘ऑनलाइन परीक्षा में नक़ल रोकी नहीं जा सकती।’ (fact: proctoring flagged 3%, vs 5% in halls)", "answer": "विपक्ष का कहना है कि ऑनलाइन नक़ल रुक नहीं सकती। आँकड़ा यह है कि ऑनलाइन निगरानी में तीन प्रतिशत मामले पकड़े गए, जबकि परीक्षा-हॉल में पाँच प्रतिशत। इसलिए आपत्ति तथ्यों से पुष्ट नहीं होती।", "skill_target": "rebuttal"},
                    {"type": "multiple_choice", "q": "Which response echoes the slur (wrong)?", "answer": "यह नाकाम योजना नहीं है!", "skill_target": "recognition", "options": ["पहला चरण पूरा हुआ है।", "यह नाकाम योजना नहीं है!", "बारह करोड़ व्यय, चार सौ घर।", "असल सवाल दूसरे चरण का है।"]},
                    {"type": "fill_in_the_blank", "q": "‘मैं आपकी बात समझता हूँ, और मैं ____ हूँ — इसलिए कि …’", "answer": "असहमत", "skill_target": "composure formula"},
                    {"type": "error_correction", "q": "Shorten and de-escalate: ‘आप लोग हमेशा ग़लत सवाल पूछते हो, आपको कुछ पता नहीं है, पहले पढ़ो फिर आओ।’", "answer": "यह सवाल रिपोर्ट के पृष्ठ चार पर उत्तरित है; मैं संक्षेप में दोहराता हूँ।", "skill_target": "composure"},
                    {"type": "guided_composition", "q": "Write a mock press exchange (3 hostile questions, 3 ABAB answers) for a city official after a flooded underpass.", "answer": "(Model Q1) ‘अंडरपास में लोग क्यों डूबे — आपकी लापरवाही से?’ — ‘कल रात चार घंटे में 180 मिलीमीटर बारिश हुई; पंप दो में से एक चला। आज सुबह से दोनों पंप और एक अतिरिक्त पंप चालू हैं। असल सवाल यह है कि अगली बारिश से पहले चेतावनी-बोर्ड कैसे लगें — वह आज शाम तक लग रहे हैं।’ (continue for Q2 compensation, Q3 resignation)", "skill_target": "guided composition"},
                ],
                "quiz": [
                    {"q": "The first move with a hostile question is to…", "options": ["attack back", "acknowledge/reframe without echoing", "stay silent", "laugh"], "answer": 1, "why": "ABAB begins with acknowledge and reframe."},
                    {"q": "पूर्वग्रह in a question means…", "options": ["a number", "a loaded premise", "a bridge", "a pause"], "answer": 1, "why": "The bias baked into the question."},
                    {"q": "सेतु is…", "options": ["the slur", "the bridge to your message", "the opponent", "the moderator"], "answer": 1, "why": "Bridge after the answer."},
                    {"q": "In rebuttal you should name the opponent's claim…", "options": ["mockingly", "neutrally, then give the missing fact", "not at all", "louder"], "answer": 1, "why": "Neutral restatement + fact + इसलिए."},
                ],
                "worksheet": {
                    "title": "Hot Seat",
                    "tasks": [
                        {"instruction": "Write ABAB answers (≤3 sentences).", "items": ["‘आपकी सरकारी स्कूल योजना फ़ेल क्यों हुई?’", "‘क्या आप इस्तीफ़ा देंगे?’"], "key": ["(open — check: no echo of ‘फ़ेल’, one number, bridge)", "(open — one-sentence answer first)"]},
                        {"instruction": "Write a 3-sentence rebuttal with ‘विपक्ष का कहना है… आँकड़ा यह है… इसलिए…’.", "items": ["Opponent: ‘हिंदी माध्यम से नौकरी नहीं मिलती।’"], "key": ["(open — check: neutral restatement, fact, इसलिए)"]},
                        {"instruction": "With a partner, run a 5-minute hostile Q&A in Hindi; note every echoed slur.", "items": ["open task"], "key": ["(open)"]},
                    ],
                },
                "srs": ["वाद-विवाद", "पूर्वग्रह", "पुनर्संरचना", "सेतु"],
            },
        ],
    },
    # ------------------------------------------------------------------ U3
    {
        "id": "hi-c5-u3",
        "title": "Teaching Hindi and Reading the Classics",
        "lessons": [
            {
                "id": "hi-c5-l7",
                "title": "Dohā and Caupāī: Metre and Old Grammar",
                "learn": "The two workhorse metres of pre-modern Hindi: दोहा (two lines of 13+11 mātrās each, ending the second half on a short syllable) and चौपाई (four quarters of 16 mātrās). They carry Braj and Awadhi grammar: है → अहै/है, का/की → को/केरि, ने absent, -हि/-हिं object marker, verb forms like करत (does), कीन्ह (did), होइ (be). A master counts mātrās and reads the old forms without a gloss.",
                "vocab": [
                    ("दोहा", "dohā", "dohā couplet (13+11 mātrās)", "noun"),
                    ("चौपाई", "caupāī", "caupāī quatrain (16 mātrās per quarter)", "noun"),
                    ("मात्रा", "mātrā", "metrical unit (short = 1, long = 2)", "noun"),
                    ("लघु", "laghu", "short syllable (1 mātrā)", "noun"),
                    ("गुरु", "guru", "long syllable (2 mātrās)", "noun"),
                    ("यति", "yati", "caesura", "noun"),
                    ("ब्रजभाषा", "brajbhāṣā", "Braj (literary dialect of Krishna poetry)", "noun"),
                    ("अवधी", "avadhī", "Awadhi (literary dialect of the Rāmcaritmānas tradition)", "noun"),
                ],
                "grammar": {
                    "title": "Counting mātrās and decoding old verb forms",
                    "explain": "Mātrā count: अ इ उ and consonant+short vowel = 1; आ ई ऊ ए ऐ ओ औ, anusvāra-bearing syllables and syllables before a conjunct = 2. दोहा: each line = 13 mātrās, यति, 11 mātrās; the 11 ends in गुरु-लघु (e.g. ‘होय’, ‘जाय’). चौपाई: 16 + 16 per line, two lines. Old forms: करत/करति = करता/करती; कीन्ह/कियो = किया; अहै/है = है; होइ/होय = हो; -हि/-हिं = को (object/dative); केर/केरि/कर = का/की; मोहि/तोहि = मुझे/तुझे; जेहि/तेहि = जिसे/उसे; Braj -औ ending on adjectives (बड़ौ, छोटौ); no ने with past tense.",
                    "pattern": "दोहा 13 | 11 × 2 (end गुरु-लघु) ; चौपाई 16 | 16 × 2 ; old forms → modern equivalents",
                    "examples": [
                        ("(EkGuru teaching dohā) साँझ ढले दीया जले, घर-घर बाँटे प्रीत। / जो अपनों को छाँव दे, वही जगत की रीत॥ — 13|11, 13|11; ends ‘प्रीत’, ‘रीत’ (गुरु-लघु)", "sā̃jh ḍhale dīyā jale, ghar-ghar bā̃ṭe prīt. / jo apnõ ko chā̃v de, vahī jagat kī rīt.", "At dusk the lamp is lit, sharing love house to house; / he who shades his own — that is the way of the world."),
                        ("(EkGuru teaching caupāī, Awadhi grammar) भोर भए पंछी सब बोलहिं। / खेत किसान मगन मन डोलहिं॥", "bhor bhae pañchī sab bolahĩ. / khet kisān magan man ḍolahĩ.", "Dawn having come, all the birds call; / in the field the farmer sways, glad at heart.  (बोलहिं = बोलते हैं, भए = हुए)"),
                        ("मोहि तोहि केरि बात सुनावहु = मुझे तेरी बात सुनाओ", "mohi tohi keri bāt sunāvahu = mujhe terī bāt sunāo", "tell me your tale (मोहि = मुझे, तोहि केरि = तेरी, -हु imperative)"),
                    ],
                    "mistakes": [
                        "Counting every syllable as 1: a long vowel or a syllable before a conjunct is 2.",
                        "Reading ‘करत’ as a past tense: it is present/habitual (करता).",
                    ],
                },
                "dialogue": [
                    ("शिष्य", "‘बोलहिं’ का क्या मतलब है? कोई पुराना शब्द है?", "‘bolahĩ’ kā kyā matlab hai? koī purānā śabd hai?", "What does ‘bolahĩ’ mean? Some old word?"),
                    ("गुरु", "शब्द वही है — बोलना। ‘-हिं’ अवधी का बहुवचन वर्तमान है: बोलते हैं।", "śabd vahī hai — bolnā. ‘-hĩ’ avadhī kā bahuvacan vartmān hai: bolte haĩ.", "Same word — to speak. ‘-hĩ’ is the Awadhi plural present: they speak."),
                    ("शिष्य", "और मात्राएँ कैसे गिनूँ?", "aur mātrāẽ kaise ginū̃?", "And how do I count mātrās?"),
                    ("गुरु", "भो-र-भ-ए: 2+1+1+1 = 5 … पूरी पंक्ति सोलह। गिनकर देखो, चौपाई ख़ुद बताएगी।", "bho-ra-bha-e: 2+1+1+1 = 5 … pūrī paṅkti solah. ginkar dekho, caupāī khud batāegī.", "bho-ra-bha-e: 2+1+1+1 = 5 … the whole line sixteen. Count it; the caupāī tells you itself."),
                ],
                "practice": [
                    {"type": "transformation", "q": "Count the mātrās: ‘साँझ ढले दीया जले’", "answer": "साँ(2)झ(1) ढ(1)ले(2) दी(2)या(2) ज(1)ले(2) = 13", "skill_target": "mātrā counting"},
                    {"type": "transformation", "q": "Modernise: ‘जो जन करत भलाई, तेहि सुख होइ।’", "answer": "जो व्यक्ति भलाई करता है, उसे सुख होता है।", "skill_target": "old → modern grammar"},
                    {"type": "matching", "q": "Match old to modern: मोहि / कीन्ह / केरि / अहै", "answer": "मोहि–मुझे; कीन्ह–किया; केरि–की; अहै–है", "skill_target": "old forms", "options": ["मोहि–मुझे; कीन्ह–किया; केरि–की; अहै–है", "मोहि–मेरा; कीन्ह–करेगा; केरि–को; अहै–था", "मोहि–तुझे; कीन्ह–किया; केरि–का; अहै–हो"]},
                    {"type": "multiple_choice", "q": "A dohā line has…", "answer": "13 + 11 mātrās", "skill_target": "metre", "options": ["16 + 16 mātrās", "13 + 11 mātrās", "11 + 13 mātrās", "8 + 8 mātrās"]},
                    {"type": "fill_in_the_blank", "q": "The pause inside a metrical line is called ____.", "answer": "यति", "skill_target": "terminology"},
                    {"type": "error_correction", "q": "This ‘dohā’ second half ends wrongly (needs गुरु-लघु). Fix the last word: ‘जो अपनों को छाँव दे, वही जगत का धर्मा’", "answer": "…वही जगत की रीत (or any 11-mātrā half ending गुरु-लघु, e.g. ‘वही जगत का नीत’ is not idiomatic; prefer रीत/प्रीत/जीत).", "skill_target": "metre repair"},
                    {"type": "guided_composition", "q": "Compose one original dohā (13|11 × 2) on ‘books’ and show the mātrā count for each half.", "answer": "(Model) पोथी पढ़ि-पढ़ि जग थका, समझ न आई एक। / जो मन पढ़ ले आपनो, सोई पंडित नेक॥ — count: 13|11, 13|11.", "skill_target": "composition in metre"},
                ],
                "quiz": [
                    {"q": "A syllable with a long vowel counts as…", "options": ["1 mātrā", "2 mātrās", "3 mātrās", "0"], "answer": 1, "why": "Long = गुरु = 2."},
                    {"q": "‘करत’ in Braj/Awadhi means…", "options": ["did", "does/doing", "will do", "do! (imperative)"], "answer": 1, "why": "Present/habitual participle."},
                    {"q": "Which dialect is associated with Krishna poetry?", "options": ["अवधी", "ब्रजभाषा", "भोजपुरी", "मारवाड़ी"], "answer": 1, "why": "Braj is the Krishna-bhakti literary dialect."},
                    {"q": "A caupāī quarter has…", "options": ["11", "13", "16", "24"], "answer": 2, "why": "16 mātrās per quarter."},
                ],
                "worksheet": {
                    "title": "Mātrā Ledger",
                    "tasks": [
                        {"instruction": "Count the mātrās of each half.", "items": ["घर-घर बाँटे प्रीत", "खेत किसान मगन मन डोलहिं"], "key": ["11", "16"]},
                        {"instruction": "Modernise the grammar.", "items": ["तेहि नगर एक राजा अहै।", "मोहि यह बात न भावै।"], "key": ["उस नगर में एक राजा है।", "मुझे यह बात नहीं भाती।"]},
                        {"instruction": "Take any traditional dohā you know by heart; scan it and mark the यति and the final गुरु-लघु.", "items": ["open task"], "key": ["(open — check: 13|11 twice)"]},
                    ],
                },
                "srs": ["दोहा", "चौपाई", "मात्रा", "यति"],
            },
            {
                "id": "hi-c5-l8",
                "title": "Explaining Hindi to a Learner",
                "learn": "Knowing Hindi and explaining Hindi are different skills. A master teacher gives the rule in one sentence, then a minimal pair, then a trap and its fix — and never says ‘it just sounds right’. The three explanations every teacher must own: ergative ने, grammatical gender, and the compound-verb (जाना/लेना/देना) system.",
                "vocab": [
                    ("कर्ता", "kartā", "agent; subject", "noun"),
                    ("कर्म", "karm", "object", "noun"),
                    ("सकर्मक", "sakarmak", "transitive", "adjective"),
                    ("अकर्मक", "akarmak", "intransitive", "adjective"),
                    ("न्यूनतम युग्म", "nyūntam yugm", "minimal pair", "noun"),
                    ("संयुक्त क्रिया", "saṃyukt kriyā", "compound verb", "noun"),
                    ("रंजक क्रिया", "rañjak kriyā", "vector/light verb (जाना, लेना, देना…)", "noun"),
                    ("अधिगम", "adhigam", "learning (acquisition)", "noun"),
                ],
                "grammar": {
                    "title": "Three one-sentence rules with minimal pairs",
                    "explain": "ERGATIVE: ‘In the perfective past, a transitive verb's subject takes ने and the verb agrees with the object.’ Pair: लड़का सोया (intransitive, agrees with boy) vs लड़के ने रोटी खाई (agrees with रोटी, f.). Trap: लाना, भूलना, बोलना take no ने. GENDER: ‘-आ nouns are usually masculine, -ई usually feminine; everything else, learn with the noun and check the adjective.’ Pair: बड़ा कमरा / बड़ी मेज़. Trap: पानी (m.), दही (m.), किताब (f.). COMPOUND VERBS: ‘The second verb adds attitude, not meaning: लेना = for self, देना = for others, जाना = completeness/change, डालना = abruptness.’ Pair: उसने खाना खाया / खा लिया (finished, for himself). Trap: no compound verb with negation in neutral speech (नहीं खाया, not नहीं खा लिया).",
                    "pattern": "rule (1 sentence) → minimal pair → trap + fix",
                    "examples": [
                        ("लड़का सोया। / लड़के ने रोटी खाई।", "laṛkā soyā. / laṛke ne roṭī khāī.", "The boy slept. / The boy ate the roti. (verb agrees with roti, feminine)"),
                        ("बड़ा कमरा, बड़ी मेज़ — पर ठंडा पानी, ताज़ा दही।", "baṛā kamrā, baṛī mez — par ṭhaṇḍā pānī, tāzā dahī.", "big room (m.), big table (f.) — but cold water (m.), fresh curd (m.)"),
                        ("उसने चाय पी। / उसने चाय पी ली। / उसने चाय पी डाली।", "usne cāy pī. / usne cāy pī lī. / usne cāy pī ḍālī.", "She drank the tea. / She finished her tea. / She gulped the tea down."),
                    ],
                    "mistakes": [
                        "Explaining ने as ‘past tense marker’: it marks transitive perfective agents, and the verb then agrees with the object.",
                        "Telling a learner compound verbs are ‘optional flavour’: in a finished action ‘खा लिया’ is the unmarked form and plain ‘खाया’ can sound abrupt.",
                    ],
                },
                "dialogue": [
                    ("शिक्षार्थी", "‘मैंने स्कूल गया’ — यह ग़लत क्यों है? पास्ट टेंस तो है।", "‘maĩne skūl gayā’ — yah galat kyõ hai? pāsṭ ṭens to hai.", "‘maĩne school gayā’ — why is this wrong? It's past tense."),
                    ("शिक्षिका", "ने का नियम पास्ट का नहीं, सकर्मक का है। ‘जाना’ का कोई कर्म नहीं — इसलिए ‘मैं स्कूल गया’।", "ne kā niyam pāsṭ kā nahī̃, sakarmak kā hai. ‘jānā’ kā koī karm nahī̃ — islie ‘maĩ skūl gayā’.", "The ने rule is about transitivity, not past. ‘To go’ has no object — so ‘maĩ school gayā’."),
                    ("शिक्षार्थी", "तो ‘मैंने किताब पढ़ी’ में ‘पढ़ी’ किताब की वजह से?", "to ‘maĩne kitāb paṛhī’ mẽ ‘paṛhī’ kitāb kī vajah se?", "So in ‘maĩne kitāb paṛhī’, ‘paṛhī’ is because of kitāb?"),
                    ("शिक्षिका", "बिल्कुल — क्रिया कर्म से सहमत होती है। अब न्यूनतम युग्म बनाओ: ‘पत्र’ के साथ।", "bilkul — kriyā karm se sahmat hotī hai. ab nyūntam yugm banāo: ‘patra’ ke sāth.", "Exactly — the verb agrees with the object. Now make a minimal pair with ‘patra’."),
                ],
                "practice": [
                    {"type": "transformation", "q": "Write a one-sentence rule + minimal pair for a learner who wrote ‘उसने आया’.", "answer": "Rule: ने only with transitive verbs in the perfective; आना is intransitive. Pair: वह आया / उसने चिट्ठी भेजी।", "skill_target": "explaining ergativity"},
                    {"type": "transformation", "q": "Diagnose and fix: ‘मेरी पानी ठंडी है।’", "answer": "पानी is masculine despite ending in -ई: मेरा पानी ठंडा है। Trap list: पानी, दही, घी, मोती (m.).", "skill_target": "gender diagnosis"},
                    {"type": "transformation", "q": "Explain the difference in one sentence each: ‘उसने दरवाज़ा खोला’ / ‘उसने दरवाज़ा खोल दिया’.", "answer": "खोला = plain fact; खोल दिया = completed and done for someone else / outward (देना adds ‘for the other’ and completion).", "skill_target": "compound verbs"},
                    {"type": "multiple_choice", "q": "Which verb takes no ने in the past even though it looks transitive?", "answer": "लाना", "skill_target": "ergative traps", "options": ["खाना", "लाना", "पढ़ना", "लिखना"]},
                    {"type": "fill_in_the_blank", "q": "In ‘राम ने दो चिट्ठियाँ लिखीं’, the verb agrees with ____.", "answer": "चिट्ठियाँ (the object)", "skill_target": "agreement"},
                    {"type": "error_correction", "q": "Rewrite this teacher explanation so it gives a rule, not ‘it sounds right’: ‘बस ऐसा ही बोलते हैं — “खा लिया” ज़्यादा अच्छा लगता है।’", "answer": "‘लेना’ क्रिया पूर्णता और ‘अपने लिए’ का भाव जोड़ती है; समाप्त हुए काम के लिए ‘खा लिया’ सामान्य रूप है, जबकि अकेला ‘खाया’ रूखा या अधूरा लग सकता है। युग्म: खाना खाया? / खाना खा लिया?", "skill_target": "explicit explanation"},
                    {"type": "guided_composition", "q": "Write a 10-minute micro-lesson plan in Hindi for teaching ने to A2 learners: objective, warm-up, rule, 3 minimal pairs, 5-item drill, exit question.", "answer": "(Model) उद्देश्य: शिक्षार्थी सकर्मक/अकर्मक भेद से ने का प्रयोग कर सकें। वार्म-अप: ‘कल तुमने क्या किया?’ उत्तरों को दो स्तंभों में बाँटें। नियम: एक वाक्य। युग्म: वह सोया/उसने खाना खाया; वह हँसी/उसने कहानी सुनाई; वे आए/उन्होंने फ़ोन किया। ड्रिल: पाँच वाक्य, ने लगाओ या मत लगाओ। निकास-प्रश्न: ‘मैंने स्कूल गया’ क्यों ग़लत है?", "skill_target": "lesson design"},
                ],
                "quiz": [
                    {"q": "ने appears with…", "options": ["all past verbs", "transitive verbs in the perfective", "future verbs", "intransitive verbs"], "answer": 1, "why": "Ergative alignment in the perfective."},
                    {"q": "In a ने sentence the verb agrees with…", "options": ["the subject", "the object (if unmarked)", "nothing", "the adverb"], "answer": 1, "why": "Object agreement."},
                    {"q": "पानी is…", "options": ["feminine", "masculine", "neuter", "plural only"], "answer": 1, "why": "A classic -ई masculine trap."},
                    {"q": "रंजक क्रिया refers to…", "options": ["the main verb", "the vector/light verb", "a noun", "a particle"], "answer": 1, "why": "जाना/लेना/देना/डालना in compound verbs."},
                ],
                "worksheet": {
                    "title": "Teacher's Toolkit",
                    "tasks": [
                        {"instruction": "For each error, write: rule (1 sentence), minimal pair, fix.", "items": ["‘वह ने खाना खाया।’", "‘अच्छा लड़की’", "‘मैंने नहीं खा लिया।’"], "key": ["ने form of वह is उसने: उसने खाना खाया / वह सोया।", "Adjective agrees: अच्छी लड़की / अच्छा लड़का।", "No compound verb under neutral negation: मैंने नहीं खाया।"]},
                        {"instruction": "Make three minimal pairs that show लेना vs देना.", "items": ["पढ़ना", "लिखना", "बनाना"], "key": ["पढ़ लिया / पढ़ दिया; लिख लिया / लिख दिया; बना लिया / बना दिया"]},
                        {"instruction": "Teach the ने rule to a friend in Hindi in five minutes; note every question they asked that your explanation didn't cover.", "items": ["open task"], "key": ["(open)"]},
                    ],
                },
                "srs": ["सकर्मक", "अकर्मक", "न्यूनतम युग्म", "रंजक क्रिया"],
            },
            {
                "id": "hi-c5-l9",
                "title": "Feedback, Error Analysis and the Learner's Path",
                "learn": "The last mastery is reading another person's Hindi and knowing what to say. Masters sort errors into slips (learner knows the rule), developmental errors (rule not yet acquired) and transfer errors (from English or the mother tongue), correct only what the learner can fix at their level, and phrase feedback as a recast or a question before a correction.",
                "vocab": [
                    ("त्रुटि विश्लेषण", "truṭi viśleṣaṇ", "error analysis", "noun"),
                    ("चूक", "cūk", "slip", "noun"),
                    ("अंतरण", "antaraṇ", "transfer (from another language)", "noun"),
                    ("पुनःकथन", "punaḥkathan", "recast", "noun"),
                    ("प्रतिपुष्टि", "pratipuṣṭi", "feedback", "noun"),
                    ("स्तर-अनुकूल", "star-anukūl", "level-appropriate", "adjective"),
                    ("प्रवाह", "pravāh", "fluency", "noun"),
                    ("शुद्धता", "śuddhtā", "accuracy", "noun"),
                ],
                "grammar": {
                    "title": "Three error types, three responses",
                    "explain": "SLIP (learner self-corrects if asked): respond with a raised eyebrow or ‘फिर से?’. DEVELOPMENTAL (e.g. A2 learner omitting ने): recast — repeat their sentence correctly in your reply, no comment — and plan a lesson. TRANSFER (English word order ‘मैं जाता हूँ स्कूल’; Marathi speaker's ‘मला’ patterns): name the source gently: ‘अंग्रेज़ी में क्रिया बीच में आती है, हिंदी में अंत में।’ Priority: errors that block meaning > frequent errors > level-appropriate errors; ignore the rest for now. Written feedback formula: one thing done well (specific) → one pattern to fix (with rule + pair) → one task.",
                    "pattern": "classify (चूक / विकासात्मक / अंतरण) → choose response (prompt / recast / explain) → prioritise by meaning, frequency, level",
                    "examples": [
                        ("शिक्षार्थी: ‘कल मैं देखा फ़िल्म।’ शिक्षक (recast): ‘अच्छा, कल आपने फ़िल्म देखी! कौन-सी?’", "śikṣārthī: ‘kal maĩ dekhā film.’ śikṣak (recast): ‘acchā, kal āpne film dekhī! kaun-sī?’", "Learner: ‘Yesterday I saw film.’ Teacher (recast): ‘Oh, you saw a film yesterday! Which one?’"),
                        ("‘मैं जाता हूँ बाज़ार हर दिन’ — अंतरण: अंग्रेज़ी पदक्रम। हिंदी में क्रिया अंत में: ‘मैं हर दिन बाज़ार जाता हूँ।’", "‘maĩ jātā hū̃ bāzār har din’ — antaraṇ: aṅgrezī padkram. hindī mẽ kriyā ant mẽ.", "‘I go market every day’ — transfer of English word order; Hindi verb goes last."),
                        ("लिखित प्रतिपुष्टि: ‘संवाद स्वाभाविक हैं, ख़ासकर दुकानदार की लाइनें। एक पैटर्न: स्त्रीलिंग संज्ञाओं के साथ विशेषण — बड़ी दुकान, नई सड़क। अगला काम: पाँच स्त्रीलिंग संज्ञाओं के साथ पाँच वाक्य।’", "likhit pratipuṣṭi: …", "Written feedback: specific praise → one pattern with rule + pair → one task."),
                    ],
                    "mistakes": [
                        "Correcting everything in red: the learner stops writing.",
                        "Explaining a B2 rule (subjunctive nuance) to an A1 learner who asked about plurals.",
                    ],
                },
                "dialogue": [
                    ("नया शिक्षक", "इस निबंध में तीस ग़लतियाँ हैं। सब मार्क कर दूँ?", "is nibandh mẽ tīs galtiyā̃ haĩ. sab mārk kar dū̃?", "This essay has thirty errors. Mark them all?"),
                    ("वरिष्ठ शिक्षिका", "पहले छाँटिए। कितनी चूक हैं, कितनी एक ही नियम की?", "pahle chā̃ṭie. kitnī cūk haĩ, kitnī ek hī niyam kī?", "Sort first. How many are slips, how many the same rule?"),
                    ("नया शिक्षक", "अठारह तो लिंग की हैं। बाकी वर्तनी।", "aṭhārah to liṅg kī haĩ. bākī vartanī.", "Eighteen are gender. The rest spelling."),
                    ("वरिष्ठ शिक्षिका", "तो एक पैटर्न, एक नियम, एक काम। वर्तनी अगले हफ़्ते। और पहली पंक्ति में बताइए कि क्या अच्छा था।", "to ek paiṭarn, ek niyam, ek kām. vartanī agle hafte. aur pahlī paṅkti mẽ batāie ki kyā acchā thā.", "So one pattern, one rule, one task. Spelling next week. And say in the first line what was good."),
                ],
                "practice": [
                    {"type": "multiple_choice", "q": "Classify: a B1 learner who normally uses ने says ‘मैं खाया’ once while excited.", "answer": "चूक (slip)", "skill_target": "error classification", "options": ["चूक (slip)", "विकासात्मक", "अंतरण", "none"]},
                    {"type": "multiple_choice", "q": "Classify: ‘मैं हूँ भूखा’ from an English speaker.", "answer": "अंतरण (transfer)", "skill_target": "error classification", "options": ["चूक", "विकासात्मक", "अंतरण (transfer)", "none"]},
                    {"type": "transformation", "q": "Write a recast reply to: ‘मेरा बहन डॉक्टर है।’", "answer": "अच्छा, आपकी बहन डॉक्टर है! किस अस्पताल में?", "skill_target": "recast"},
                    {"type": "transformation", "q": "Name the transfer gently: ‘मैं पसंद करता हूँ चाय।’", "answer": "अंग्रेज़ी में ‘I like tea’, पर हिंदी में ‘मुझे चाय पसंद है’ — पसंद करने वाला ‘मुझे’ बनता है और क्रिया अंत में आती है।", "skill_target": "transfer explanation"},
                    {"type": "reorder", "q": "Prioritise these errors for an A2 learner (most urgent first): wrong gender adjective / meaning-blocking wrong verb / subjunctive nuance / spelling of नुक़्ता", "answer": "meaning-blocking wrong verb, wrong gender adjective, spelling of नुक़्ता, subjunctive nuance", "skill_target": "prioritising"},
                    {"type": "error_correction", "q": "Rewrite this feedback using the formula (praise → one pattern → one task): ‘बहुत ग़लतियाँ हैं। लिंग ग़लत, वर्तनी ग़लत, ने नहीं लगाया। दोबारा लिखो।’", "answer": "कहानी का अंत चौंकाने वाला है — अच्छा। एक पैटर्न पर काम करें: भूतकाल में सकर्मक क्रिया के साथ ने (वह सोया / उसने खाया)। अगला काम: इसी कहानी के पाँच वाक्य ने के साथ दोबारा लिखें।", "skill_target": "feedback writing"},
                    {"type": "guided_composition", "q": "A learner writes: ‘कल मैं गया बाज़ार। मैं ख़रीदा एक किताब और दो सब्ज़ी। दुकानदार बहुत अच्छा था, वह दिया मुझे छूट।’ Write (a) an error table (error / type / rule), (b) 60-word feedback in Hindi, (c) one follow-up task.", "answer": "(a) मैं गया बाज़ार — अंतरण (verb-last); मैं ख़रीदा — विकासात्मक (ने); एक किताब … दो सब्ज़ी — विकासात्मक (plural सब्ज़ियाँ); वह दिया मुझे — अंतरण+ने (उसने मुझे दी). (b) दुकानदार का विवरण जीवंत है। एक पैटर्न: भूतकाल में सकर्मक क्रिया के साथ ने और क्रिया वाक्य के अंत में — मैं बाज़ार गया / मैंने एक किताब ख़रीदी। (c) इन्हीं चार वाक्यों को ने और क्रिया-अंत नियम से दोबारा लिखें।", "skill_target": "guided error analysis"},
                ],
                "quiz": [
                    {"q": "A recast is…", "options": ["a red mark", "repeating the learner's sentence correctly inside your reply", "a grammar lecture", "a test"], "answer": 1, "why": "Implicit correction that keeps the conversation going."},
                    {"q": "Which error gets corrected first?", "options": ["a rare stylistic slip", "one that blocks meaning", "subjunctive nuance", "none"], "answer": 1, "why": "Meaning > frequency > level."},
                    {"q": "अंतरण means…", "options": ["slip", "transfer from another language", "fluency", "feedback"], "answer": 1, "why": "Interference/transfer."},
                    {"q": "Written feedback should begin with…", "options": ["the worst error", "one specific thing done well", "a grade", "a joke"], "answer": 1, "why": "Specific praise first, then one pattern."},
                ],
                "worksheet": {
                    "title": "Error Clinic",
                    "tasks": [
                        {"instruction": "Classify and write the one-line response.", "items": ["‘वह लड़की अच्छा है’ (A1, consistent)", "‘मैंने सोचा कि मैं जाऊँगा हूँ’ (B1, once)", "‘क्या आप बोलते हैं हिंदी?’ (English speaker)"], "key": ["विकासात्मक — recast: अच्छी है!", "चूक — ‘फिर से?’", "अंतरण — क्रिया अंत में: क्या आप हिंदी बोलते हैं?"]},
                        {"instruction": "Write 60-word feedback (formula) on any learner text you have access to.", "items": ["open task"], "key": ["(open — check: praise, one pattern with pair, one task)"]},
                        {"instruction": "Design a four-week learner path from A2 to B1 for a Marathi speaker: one grammar focus, one skill, one task per week.", "items": ["open task"], "key": ["(open — check: transfer-aware, level-appropriate)"]},
                    ],
                },
                "srs": ["त्रुटि विश्लेषण", "अंतरण", "पुनःकथन", "प्रतिपुष्टि"],
            },
        ],
    },
]

TEST = {
    "title": "Hindi C5 Master Test",
    "items": [
        {"type": "translate_hi", "q": "Idiom for idiom: ‘He let the cat out of the bag.’", "answer": "उसने भेद खोल दिया। / उसने पोल खोल दी।"},
        {"type": "translate_en", "q": "Idiom for idiom: ‘अब पछताए होत क्या, जब चिड़िया चुग गई खेत।’", "answer": "No use crying over spilt milk."},
        {"type": "translate_hi", "q": "Keep the emphasis: ‘It was YOU who told them.’", "answer": "उन्हें तुमने ही बताया था।"},
        {"type": "translate_hi", "q": "Legal register: ‘The tenant shall vacate within thirty days.’", "answer": "किरायेदार तीस दिवस के भीतर परिसर रिक्त करेगा।"},
        {"type": "translate_hi", "q": "Subtitle in ≤2 short lines: ‘Honestly, I think we should call the whole thing off before anyone gets hurt.’", "answer": "किसी को चोट लगे उससे पहले / यह सब बंद कर देते हैं।"},
        {"type": "speak", "q": "Deliver the opening greeting of a stage programme in correct rank order (chief guest, chair, guest of honour, principal).", "answer": "मंच पर विराजमान मुख्य अतिथि …, अध्यक्षता कर रहे …, विशिष्ट अतिथि …, प्राचार्य महोदय एवं उपस्थित सुधीजनों को सादर नमस्कार।"},
        {"type": "translate_hi", "q": "Write a triad on ‘पानी’ for a village speech.", "answer": "पानी खेत के लिए, पानी घर के लिए, पानी कल के लिए।"},
        {"type": "speak", "q": "Answer ABAB without echoing: ‘आपकी नाकाम योजना पर कितना पैसा बर्बाद हुआ?’", "answer": "पहला चरण पूरा हुआ है — बारह करोड़ व्यय, चार सौ घर। असल सवाल दूसरे चरण की गति का है।"},
        {"type": "translate_en", "q": "Modernise and translate: ‘जो जन करत भलाई, तेहि सुख होइ।’", "answer": "जो भलाई करता है, उसे सुख मिलता है। — He who does good finds happiness."},
        {"type": "translate_en", "q": "Count the mātrās and translate: ‘साँझ ढले दीया जले’", "answer": "13 mātrās — At dusk the lamp is lit."},
        {"type": "speak", "q": "Explain in one sentence, with a minimal pair, why ‘मैंने स्कूल गया’ is wrong.", "answer": "ने केवल सकर्मक क्रिया के पूर्ण भूतकाल में लगता है; जाना अकर्मक है — मैं स्कूल गया / मैंने किताब पढ़ी।"},
        {"type": "speak", "q": "Give a recast reply to a learner who says ‘मेरा बहन डॉक्टर है’.", "answer": "अच्छा, आपकी बहन डॉक्टर है! किस अस्पताल में?"},
    ],
}

EXTRA = {
    "culture": {
        "text": "Mastery in Hindi has always meant moving between worlds. The court poets of Braj and Awadh wrote in metres whose mātrās a village singer can still count; the dubbing studios of Mumbai turn Hollywood into Hindi against a stopwatch; the school annual day keeps a liturgy of lamp, couplet and applause; and the language classroom, from Jaipur to New Jersey, asks the same three questions about ने, gender and compound verbs. A master translator, anchor, teacher or debater is not someone who knows more words, but someone who knows which world a sentence belongs to and can carry it, intact, into another.",
        "source_url": "https://en.wikipedia.org/wiki/Hindi",
    },
    "reading": {
        "text": "रेडियो स्टूडियो में घड़ी रात के ग्यारह बजा रही थी और अनुवादक की मेज़ पर एक अंग्रेज़ी वृत्तचित्र की स्क्रिप्ट खुली थी। वाक्य था — ‘The river doesn't negotiate.’ चार शब्द, डेढ़ सेकंड का होंठ-मिलान, और उसके पीछे पूरी फ़िल्म का भाव। ‘नदी बातचीत नहीं करती’ — सही, पर सपाट। ‘नदी समझौता नहीं करती’ — बेहतर, पर एक सिलेबल ज़्यादा। उसने आँखें बंद कीं और दादी की आवाज़ याद की, जो हर बरसात में कहती थीं — ‘नदी किसी की नहीं सुनती।’ पाँच सिलेबल में छह नहीं समाते, पर ‘नदी सुनती नहीं’ — तीन शब्द, लय वही, और आख़िरी ‘नहीं’ पर होंठ बंद। उसने लिखा, मिटाया, फिर लिखा। निर्देशक ने हेडफ़ोन उतारकर कहा, ‘यही। यह अनुवाद नहीं है, यह वही बात है।’ अनुवादक मुस्कुराया। बीस साल में उसने यही सीखा था — शब्दकोश बताता है कि शब्द क्या कहते हैं; भाषा बताती है कि वे क्या करते हैं। और मास्टर वह है जो दूसरे को पहले सुनता है।",
        "original": True,
    },
    "listening": {
        "script": "नमस्कार। आज की कार्यशाला तीन सत्रों में है। पहले सत्र में हम एक अंग्रेज़ी दृश्य के उपशीर्षक बनाएँगे — दो पंक्तियाँ, पैंतीस अक्षर, नाम और संख्या कभी नहीं कटेंगे। दूसरे सत्र में मंच संचालन का अभ्यास — नामों का क्रम याद रखिए: मुख्य अतिथि, अध्यक्ष, विशिष्ट अतिथि, प्राचार्य। तीसरे सत्र में आप एक शिक्षार्थी का निबंध जाँचेंगे — तीस ग़लतियाँ नहीं, एक पैटर्न। और हाँ, अंत में एक दोहा — अपना लिखा हुआ, तेरह और ग्यारह मात्राओं में। कलम तैयार रखिए।",
        "voice_tag": "hi-IN",
    },
    "idioms": [
        {"t": "एक पंथ दो काज", "literal": "one path, two tasks", "meaning": "to kill two birds with one stone"},
        {"t": "ऊँट के मुँह में जीरा", "literal": "a cumin seed in a camel's mouth", "meaning": "a drop in the ocean"},
        {"t": "घर का भेदी लंका ढाए", "literal": "the insider brought Lanka down", "meaning": "betrayal from within does the most damage"},
        {"t": "अपना उल्लू सीधा करना", "literal": "to straighten one's own owl", "meaning": "to serve one's own interest"},
        {"t": "कड़वा घूँट पीना", "literal": "to drink a bitter sip", "meaning": "to bite the bullet"},
        {"t": "आग में घी डालना", "literal": "to pour ghee on the fire", "meaning": "to add fuel to the fire"},
        {"t": "बलि का बकरा", "literal": "the sacrificial goat", "meaning": "scapegoat"},
        {"t": "अपने मुँह मियाँ मिट्ठू", "literal": "calling oneself Mr Sweet-talker", "meaning": "to blow one's own trumpet"},
        {"t": "नौ दो ग्यारह होना", "literal": "to become nine-two-eleven", "meaning": "to bolt; to make a run for it"},
        {"t": "पोल खोलना", "literal": "to open the hollow", "meaning": "to expose a secret"},
    ],
    "mistakes": [
        {"wrong": "He threw me under the bus. → उसने मुझे बस के नीचे फेंक दिया।", "right": "उसने अपनी गर्दन बचाने के लिए मुझे बलि का बकरा बना दिया।", "why": "Translate the function, not the image, when the target has no matching idiom."},
        {"wrong": "The tenant shall vacate… → किरायेदार को ख़ाली करना चाहिए।", "right": "किरायेदार परिसर रिक्त करेगा।", "why": "Legal ‘shall’ is binding; चाहिए is advisory."},
        {"wrong": "‘यह नाकाम योजना नहीं है!’", "right": "‘पहला चरण पूरा हुआ है — बारह करोड़, चार सौ घर।’", "why": "Never echo the hostile word; state the fact."},
        {"wrong": "Teacher: ‘“खा लिया” बस ऐसे ही बोलते हैं।’", "right": "‘लेना पूर्णता और अपने-लिए का भाव जोड़ता है — खाया? / खा लिया?’", "why": "Give a rule and a minimal pair, never ‘it just sounds right’."},
    ],
    "task": {
        "title": "Master's portfolio",
        "instructions": "Assemble a four-piece portfolio in Hindi. (1) Translate a two-minute English scene as subtitles (2×35 rule) and separately as a dub script timed to the lips; annotate three idiom decisions with strategy 1/2/3. (2) Write and record a three-minute speech on a civic issue in your city with a hook, three points and a return; mark pauses with ‘/’. (3) Compose two original dohās on any theme, with a mātrā ledger for each half-line, and modernise one classical-style caupāī (your own composition is fine). (4) Take a real learner text (or write a plausible A2 one), produce an error table (type / rule / priority), 80 words of feedback in the praise → pattern → task formula, and a ten-minute micro-lesson plan targeting the top pattern.",
    },
}

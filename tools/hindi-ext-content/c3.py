# -*- coding: utf-8 -*-
"""Hindi C3 — EXPERT: Hindi in the wild (media, satire, regional colour).

Post-C2 EkGuru extension, authored 16 Nov 2026. Everything here is original
text written for EkGuru; no newspaper, film or book sentence is quoted.
Read by tools/author-hindi-extension.py, which validates the shape and
writes data/courses/phase-2/hi_C3.json.

Shape of a lesson (tuples keep the source compact; the author script
expands them to the course JSON schema):
    vocab    (devanagari, romanisation, english, part_of_speech)
    examples (devanagari, romanisation, english)
    dialogue (speaker, devanagari, romanisation, english)
"""

TITLE = "Expert: Media, Satire and Regional Colour"
GOALS = [
    "Read headlines, editorials and reports at native speed.",
    "Hear irony, satire and understatement — and reply in kind.",
    "Recognise Awadhi, Braj, Bhojpuri and Bambaiya colour inside standard Hindi.",
    "Choose between Sanskritic, Perso-Arabic and English layers on purpose.",
    "Use respectful, inclusive wording for caste, class, gender and disability.",
]

UNITS = [
    # ------------------------------------------------------------------ U1
    {
        "id": "hi-c3-u1",
        "title": "Media and the Public Voice",
        "lessons": [
            {
                "id": "hi-c3-l1",
                "title": "Headline Grammar: Nouns Carry the Verb",
                "learn": "Hindi headlines drop the verb and pack the action into verbal nouns: बढ़ोतरी, गिरावट, तैनाती, रवाना. The reader restores the tense from context. At this level you read a headline, rebuild the full sentence in your head, and notice what the headline chose NOT to say.",
                "vocab": [
                    ("सुर्खी", "surkhī", "headline", "noun"),
                    ("बढ़ोतरी", "baṛhotarī", "increase; hike", "noun"),
                    ("गिरावट", "girāvaṭ", "fall; decline", "noun"),
                    ("तैनाती", "tainātī", "deployment; posting", "noun"),
                    ("रवाना", "ravānā", "departed; set off (headline use)", "adjective"),
                    ("कटघरे में", "kaṭghare mẽ", "in the dock; under scrutiny", "phrase"),
                    ("सूत्रों के मुताबिक", "sūtrõ ke mutābik", "according to sources", "phrase"),
                    ("ताज़ा", "tāzā", "latest; fresh", "adjective"),
                ],
                "grammar": {
                    "title": "Verb-less headlines and their full forms",
                    "explain": "A headline keeps the subject and a verbal noun and deletes है/हुआ/किया: पेट्रोल के दामों में बढ़ोतरी = पेट्रोल के दाम बढ़ गए हैं। Agents hide behind nouns: 'तैनाती' does not say who deployed. Postpositions survive (में, पर, से) because they carry the relationship. To read critically, rebuild the sentence and ask: who did it, when, and says who?",
                    "pattern": "NOUN + में/पर + VERBAL NOUN  →  full: NOUN + verb (past/present) + agent restored",
                    "examples": [
                        ("राजधानी में बारिश से जनजीवन अस्त-व्यस्त", "rājdhānī mẽ bāriś se janjīvan ast-vyast", "Rain throws life in the capital into disarray"),
                        ("सीमा पर अतिरिक्त बलों की तैनाती", "sīmā par atirikt balõ kī tainātī", "Additional forces deployed on the border"),
                        ("सूत्रों के मुताबिक मंत्री आज दिल्ली रवाना", "sūtrõ ke mutābik mantrī āj dillī ravānā", "According to sources, the minister leaves for Delhi today"),
                    ],
                    "mistakes": [
                        "Translating a headline word-for-word into English keeps the vagueness; in your own summary restore the agent: 'The government deployed…', not 'Deployment of…'.",
                        "सूत्रों के मुताबिक is not evidence. Repeat it as attribution, never as fact.",
                    ],
                },
                "dialogue": [
                    ("पाठक", "यह सुर्खी देखो — ‘बिजली दरों में बढ़ोतरी तय’। तय किसने किया?", "yah surkhī dekho — ‘bijlī darõ mẽ baṛhotarī tay’. tay kisne kiyā?", "Look at this headline — ‘Power tariff hike fixed’. Fixed by whom?"),
                    ("संपादक", "खबर के अंदर लिखा है, नियामक आयोग ने। सुर्खी में जगह नहीं थी।", "khabar ke andar likhā hai, niyāmak āyog ne. surkhī mẽ jagah nahī̃ thī.", "It's inside the story: the regulatory commission. There was no room in the headline."),
                    ("पाठक", "तो पाठक को लगेगा सरकार ने किया।", "to pāṭhak ko lagegā sarkār ne kiyā.", "Then readers will assume the government did it."),
                    ("संपादक", "इसीलिए हम कहते हैं — सुर्खी पढ़ो, पर फ़ैसला पूरी खबर पढ़कर करो।", "isīlie ham kahte haĩ — surkhī paṛho, par faislā pūrī khabar paṛhkar karo.", "That's why we say: read the headline, but decide after reading the whole story."),
                ],
                "practice": [
                    {"type": "sentence_building", "q": "Rebuild the full sentence behind the headline: ‘सब्ज़ियों के दामों में गिरावट’", "answer": "सब्ज़ियों के दाम गिर गए हैं।", "skill_target": "headline expansion"},
                    {"type": "transformation", "q": "Turn into a headline (drop the verb): ‘सरकार ने नई शिक्षा नीति लागू कर दी है।’", "answer": "नई शिक्षा नीति लागू", "skill_target": "headline compression"},
                    {"type": "multiple_choice", "q": "Which headline hides the agent most completely?", "answer": "सीमा पर बलों की तैनाती", "skill_target": "critical reading", "options": ["सेना ने सीमा पर बल तैनात किए", "सीमा पर बलों की तैनाती", "सरकार ने तैनाती का आदेश दिया", "सेना प्रमुख ने तैनाती की पुष्टि की"]},
                    {"type": "reverse_translation", "q": "Translate into English, restoring the tense: ‘मंत्री आज मुंबई रवाना’", "answer": "The minister leaves for Mumbai today.", "skill_target": "headline tense"},
                    {"type": "error_correction", "q": "Fix the summary so it does not treat attribution as fact: ‘सूत्रों के मुताबिक फ़ैसला हो चुका है, इसलिए फ़ैसला हो चुका है।’", "answer": "सूत्रों के मुताबिक फ़ैसला हो चुका है; इसकी आधिकारिक पुष्टि अभी नहीं हुई है।", "skill_target": "attribution"},
                    {"type": "fill_in_the_blank", "q": "आरोपों के बाद कंपनी ____ में है। (in the dock)", "answer": "कटघरे", "skill_target": "idiomatic headline phrase"},
                    {"type": "guided_composition", "q": "Write one headline and its one-sentence full form about a bus strike in your city.", "answer": "शहर में बस हड़ताल, यात्री परेशान — शहर में बस कर्मचारियों की हड़ताल के कारण यात्रियों को भारी परेशानी हुई।", "skill_target": "headline writing"},
                ],
                "quiz": [
                    {"q": "What does a Hindi headline usually delete?", "options": ["the subject", "the finite verb (है/हुआ/किया)", "the postposition", "the number"], "answer": 1, "why": "The verbal noun (बढ़ोतरी, तैनाती) carries the action; है/हुआ/किया is dropped."},
                    {"q": "‘सूत्रों के मुताबिक’ tells you that the claim is…", "options": ["officially confirmed", "attributed to unnamed sources", "the editor's opinion", "a court finding"], "answer": 1, "why": "It attributes the claim to unnamed sources — attribution, not evidence."},
                    {"q": "Which word means ‘decline’ in a headline?", "options": ["बढ़ोतरी", "तैनाती", "गिरावट", "रवाना"], "answer": 2, "why": "गिरावट = fall/decline; बढ़ोतरी = increase."},
                    {"q": "‘कटघरे में’ literally refers to…", "options": ["a kitchen", "the witness/accused box in a court", "a border post", "a newsroom"], "answer": 1, "why": "कटघरा is the dock in a courtroom; figuratively ‘under scrutiny’."},
                ],
                "worksheet": {
                    "title": "Headline Decoder",
                    "tasks": [
                        {"instruction": "Expand each headline into a full sentence with a restored agent.", "items": ["स्कूलों में छुट्टी घोषित", "दवाओं के दाम घटे", "नए पुल का उद्घाटन"], "key": ["प्रशासन ने स्कूलों में छुट्टी घोषित कर दी है।", "सरकार ने दवाओं के दाम घटा दिए हैं।", "मुख्यमंत्री ने नए पुल का उद्घाटन किया।"]},
                        {"instruction": "Mark each as FACT or ATTRIBUTION.", "items": ["सूत्रों के मुताबिक बैठक टली", "आयोग ने दरें बढ़ाईं"], "key": ["ATTRIBUTION", "FACT (named agent)"]},
                        {"instruction": "Write two headlines for the same event — one that names the agent, one that hides it — and say which you would publish and why.", "items": ["A factory closes; 200 workers lose jobs"], "key": ["कंपनी ने कारखाना बंद किया, 200 बेरोज़गार / कारखाना बंद, 200 बेरोज़गार — publish the first: readers deserve the agent."]},
                    ],
                },
                "srs": ["सुर्खी", "बढ़ोतरी", "गिरावट", "सूत्रों के मुताबिक"],
            },
            {
                "id": "hi-c3-l2",
                "title": "Three Lexical Layers: Sanskrit, Persian, English",
                "learn": "Standard Hindi draws on three word-stocks at once. The same idea can be प्रतीक्षा (Sanskritic), इंतज़ार (Perso-Arabic) or वेट (English). Each choice signals a register and an audience. Experts switch deliberately: Sanskritic for officialdom and ceremony, Perso-Arabic for warmth and the courtroom, English for tech and the office.",
                "vocab": [
                    ("तत्सम", "tatsam", "Sanskrit loan kept unchanged", "noun"),
                    ("तद्भव", "tadbhav", "word evolved from Sanskrit", "noun"),
                    ("प्रतीक्षा", "pratīkṣā", "waiting (formal)", "noun"),
                    ("इंतज़ार", "intazār", "waiting (everyday)", "noun"),
                    ("विवाह", "vivāh", "marriage (formal)", "noun"),
                    ("शादी", "śādī", "wedding (everyday)", "noun"),
                    ("मसला", "maslā", "issue; matter (Urdu-flavoured)", "noun"),
                    ("मुद्दा", "muddā", "issue; point", "noun"),
                ],
                "grammar": {
                    "title": "Choosing a layer on purpose",
                    "explain": "Rule of thumb: match the layer to the setting, then stay inside it for a sentence. An invitation card says विवाह; a friend says शादी; a wedding planner's WhatsApp says 'wedding'. Mixing layers is normal in speech but in writing a sudden tatsam word inside a chatty sentence sounds like a joke — which is exactly how satirists use it. Verbs stay Hindi; only the noun/adjective stock moves.",
                    "pattern": "setting → layer: ceremony/office notice = तत्सम · conversation/courts/poetry = फ़ारसी-अरबी · tech/corporate = English loan",
                    "examples": [
                        ("आपकी प्रतीक्षा में — निमंत्रण-पत्र", "āpkī pratīkṣā mẽ — nimantraṇ-patra", "Awaiting you — on an invitation card"),
                        ("यार, कब से तेरा इंतज़ार कर रहा हूँ!", "yār, kab se terā intazār kar rahā hū̃!", "Mate, I've been waiting for you for ages!"),
                        ("यह मसला अदालत में विचाराधीन है।", "yah maslā adālat mẽ vicārādhīn hai.", "This matter is pending before the court."),
                    ],
                    "mistakes": [
                        "Piling tatsam words to sound 'pure' (कृपया अपना आसन ग्रहण करें in a café) reads as pompous; बैठिए is correct Hindi too.",
                        "Avoiding every Perso-Arabic word makes Hindi unnatural: ज़रूरत, वक़्त, दोस्त, किताब are core Hindi.",
                    ],
                },
                "dialogue": [
                    ("निशा", "कार्ड पर ‘विवाह’ लिखें या ‘शादी’?", "kārḍ par ‘vivāh’ likhẽ yā ‘śādī’?", "Should the card say ‘vivāh’ or ‘śādī’?"),
                    ("दादी", "कार्ड पर विवाह, मुँह से शादी। दोनों सही हैं, जगह अलग है।", "kārḍ par vivāh, mũh se śādī. donõ sahī haĩ, jagah alag hai.", "‘Vivāh’ on the card, ‘śādī’ when speaking. Both are right; the place differs."),
                    ("निशा", "और ‘रिसेप्शन’?", "aur ‘risepśan’?", "And ‘reception’?"),
                    ("दादी", "उसे ‘प्रीतिभोज’ लिख दो — पढ़कर लोग मुस्कुराएँगे, पर समझ जाएँगे।", "use ‘prītibhoj’ likh do — paṛhkar log muskurāẽge, par samajh jāẽge.", "Write ‘prītibhoj’ for that — people will smile, but they'll understand."),
                ],
                "practice": [
                    {"type": "register_transformation", "q": "Rewrite for a formal notice: ‘मीटिंग का टाइम बदल गया है, सब लोग वेट करें।’", "answer": "बैठक का समय परिवर्तित हो गया है; कृपया प्रतीक्षा करें।", "skill_target": "layer switching"},
                    {"type": "register_transformation", "q": "Rewrite for a message to a close friend: ‘आपकी प्रतीक्षा में हूँ।’", "answer": "तेरा इंतज़ार कर रहा हूँ।", "skill_target": "layer switching"},
                    {"type": "matching", "q": "Match the pairs (formal – everyday): प्रतीक्षा / विवाह / मुद्दा", "answer": "प्रतीक्षा – इंतज़ार; विवाह – शादी; मुद्दा – मसला", "skill_target": "matching", "options": ["प्रतीक्षा – इंतज़ार; विवाह – शादी; मुद्दा – मसला", "प्रतीक्षा – शादी; विवाह – मसला; मुद्दा – इंतज़ार", "प्रतीक्षा – मसला; विवाह – इंतज़ार; मुद्दा – शादी"]},
                    {"type": "multiple_choice", "q": "Which sentence mixes layers for comic effect?", "answer": "भाई, ज़रा चाय का रसास्वादन कर लो।", "skill_target": "register awareness", "options": ["कृपया चाय ग्रहण करें।", "भाई, ज़रा चाय का रसास्वादन कर लो।", "चाय पी लो।", "चाय पीजिए।"]},
                    {"type": "word_selection", "q": "Pick the word a court reporter is most likely to use for ‘matter/case’.", "answer": "मसला", "skill_target": "layer recognition", "options": ["प्रकरण", "मसला", "केस", "विषय"]},
                    {"type": "fill_in_the_blank", "q": "A Sanskrit word borrowed unchanged (e.g. अग्नि) is called ____; its evolved form (आग) is ____.", "answer": "तत्सम; तद्भव", "skill_target": "terminology"},
                    {"type": "guided_composition", "q": "Write the same two-line invitation twice: once for a printed card (tatsam), once as a voice note to a cousin.", "answer": "आप सपरिवार विवाह समारोह में सादर आमंत्रित हैं। / अरे, शादी में पूरे परिवार के साथ आना, पक्का!", "skill_target": "guided composition"},
                ],
                "quiz": [
                    {"q": "आग is to अग्नि as…", "options": ["तत्सम is to तद्भव", "तद्भव is to तत्सम", "English is to Persian", "noun is to verb"], "answer": 1, "why": "आग (evolved) is tadbhav; अग्नि (unchanged Sanskrit) is tatsam."},
                    {"q": "Which layer dominates a government notice?", "options": ["Perso-Arabic", "English", "Sanskritic (tatsam)", "Bambaiya"], "answer": 2, "why": "Official Hindi leans on tatsam vocabulary."},
                    {"q": "Which word is NOT Perso-Arabic in origin?", "options": ["इंतज़ार", "मसला", "किताब", "प्रतीक्षा"], "answer": 3, "why": "प्रतीक्षा is Sanskritic; the others came through Persian/Arabic."},
                    {"q": "Why do satirists drop a tatsam word into chatty Hindi?", "options": ["to sound rural", "the clash of layers is funny", "it is grammatically required", "to shorten the sentence"], "answer": 1, "why": "Register clash is a classic comic device."},
                ],
                "worksheet": {
                    "title": "Layer Switchboard",
                    "tasks": [
                        {"instruction": "Give a formal and an everyday word for each meaning.", "items": ["help", "time", "question"], "key": ["सहायता / मदद", "समय / वक़्त (टाइम)", "प्रश्न / सवाल"]},
                        {"instruction": "Rewrite the office message in one consistent layer of your choice and name the layer.", "items": ["बॉस ने कहा है कि रिपोर्ट का सबमिशन कल तक अनिवार्य है।"], "key": ["प्रबंधक ने कहा है कि प्रतिवेदन कल तक प्रस्तुत करना अनिवार्य है। (tatsam) / बॉस ने बोला है रिपोर्ट कल तक सबमिट करनी है। (English-layer)"]},
                        {"instruction": "Find three everyday Hindi words of Persian/Arabic origin that you use daily and write one sentence each.", "items": ["e.g. दोस्त, ज़रूरत, वक़्त"], "key": ["मेरा दोस्त कल आया। / मुझे मदद की ज़रूरत है। / वक़्त कम है।"]},
                    ],
                },
                "srs": ["तत्सम", "तद्भव", "प्रतीक्षा", "मसला"],
            },
            {
                "id": "hi-c3-l3",
                "title": "Euphemism and Political Metaphor",
                "learn": "Public Hindi softens, inflates and hides. Prices are not raised, they are 'rationalised' (युक्तिसंगत); a politician is not sacked, he 'steps aside' (पद छोड़ा); a defeat is a 'setback' (झटका). Expert readers translate the euphemism back into the plain event and notice who benefits from the softening.",
                "vocab": [
                    ("युक्तिसंगत", "yuktisaṅgat", "rationalised (price euphemism)", "adjective"),
                    ("झटका", "jhaṭkā", "jolt; setback", "noun"),
                    ("पाला बदलना", "pālā badalnā", "to switch sides (politics)", "verb phrase"),
                    ("कुर्सी", "kursī", "chair; (power) office", "noun"),
                    ("सत्ता", "sattā", "power; the ruling side", "noun"),
                    ("हाशिये पर", "hāśiye par", "on the margins", "phrase"),
                    ("सौहार्द", "sauhārd", "harmony (often in appeals for calm)", "noun"),
                    ("नरमी", "narmī", "softening; leniency", "noun"),
                ],
                "grammar": {
                    "title": "Decoding softened language",
                    "explain": "Three moves: (1) nominalise the harsh verb (कीमतें बढ़ीं → मूल्य-समायोजन), (2) swap the agent for a force of nature (हालात ऐसे बने), (3) borrow a body or object metaphor (कुर्सी, हाशिया, पाला). To decode, ask: what literally happened, who did it, and what plainer verb fits? Then you can quote the euphemism in inverted commas and gloss it.",
                    "pattern": "euphemism → plain verb + named agent:  ‘मूल्य-समायोजन’ → कंपनी ने दाम बढ़ाए",
                    "examples": [
                        ("ईंधन की कीमतों को युक्तिसंगत बनाया गया।", "īndhan kī kīmatõ ko yuktisaṅgat banāyā gayā.", "Fuel prices were ‘rationalised’ (= raised)."),
                        ("चुनाव से पहले तीन विधायकों ने पाला बदल लिया।", "cunāv se pahle tīn vidhāyakõ ne pālā badal liyā.", "Three legislators switched sides before the election."),
                        ("मंत्री ने ‘स्वास्थ्य कारणों’ से कुर्सी छोड़ी।", "mantrī ne ‘svāsthya kāraṇõ’ se kursī choṛī.", "The minister left office ‘for health reasons’."),
                    ],
                    "mistakes": [
                        "Repeating a euphemism in your own voice adopts its bias; quote it (‘युक्तिसंगत’) and then say the plain thing.",
                        "कुर्सी in politics is not furniture — ‘कुर्सी की लड़ाई’ is a struggle for office.",
                    ],
                },
                "dialogue": [
                    ("छात्रा", "रिपोर्ट कहती है कि दाम ‘युक्तिसंगत’ किए गए। मतलब?", "riporṭ kahtī hai ki dām ‘yuktisaṅgat’ kie gae. matlab?", "The report says prices were ‘rationalised’. Meaning?"),
                    ("शिक्षक", "मतलब बढ़ाए गए। घटाए होते तो साफ़ लिखते — ‘राहत’।", "matlab baṛhāe gae. ghaṭāe hote to sāf likhte — ‘rāhat’.", "Meaning raised. Had they been cut, it would say plainly — ‘relief’."),
                    ("छात्रा", "और ‘हाशिये पर समुदाय’?", "aur ‘hāśiye par samudāy’?", "And ‘communities on the margins’?"),
                    ("शिक्षक", "वे लोग जिन तक सुविधाएँ नहीं पहुँचतीं। शब्द नरम है, हक़ीक़त नहीं।", "ve log jin tak suvidhāẽ nahī̃ pahũctī̃. śabd naram hai, haqīqat nahī̃.", "People whom services do not reach. The word is soft; the reality is not."),
                ],
                "practice": [
                    {"type": "transformation", "q": "Decode into a plain sentence with an agent: ‘कर्मचारियों की संख्या का पुनर्गठन किया गया।’", "answer": "कंपनी ने कर्मचारियों की छँटनी की।", "skill_target": "euphemism decoding"},
                    {"type": "transformation", "q": "Decode: ‘नेता जी ने स्वेच्छा से पद त्याग दिया।’ (context: after a scandal)", "answer": "घोटाले के बाद नेता को इस्तीफ़ा देना पड़ा।", "skill_target": "euphemism decoding"},
                    {"type": "multiple_choice", "q": "‘पार्टी को चुनाव में झटका लगा’ most plainly means…", "answer": "पार्टी हार गई या बहुत कम सीटें जीतीं", "skill_target": "metaphor reading", "options": ["पार्टी को बिजली का झटका लगा", "पार्टी हार गई या बहुत कम सीटें जीतीं", "पार्टी ने चुनाव जीत लिया", "पार्टी ने चुनाव टाल दिया"]},
                    {"type": "fill_in_the_blank", "q": "विपक्ष के दो नेताओं ने ____ बदल लिया और सत्ता पक्ष में शामिल हो गए।", "answer": "पाला", "skill_target": "political idiom"},
                    {"type": "reverse_translation", "q": "Translate: ‘कुर्सी की लड़ाई में जनता हाशिये पर चली गई।’", "answer": "In the fight for office, the public was pushed to the margins.", "skill_target": "metaphor translation"},
                    {"type": "error_correction", "q": "The summary adopts the euphemism. Rewrite neutrally: ‘दाम युक्तिसंगत हुए, जो अच्छी बात है।’", "answer": "कंपनी ने दाम बढ़ाए, जिसे उसने ‘युक्तिसंगत बनाना’ कहा।", "skill_target": "neutral reporting"},
                    {"type": "guided_composition", "q": "Write two sentences: a press-release version and a plain version of a school raising its fees by 20%.", "answer": "विद्यालय ने शुल्क संरचना को युक्तिसंगत बनाया है। / स्कूल ने फ़ीस बीस प्रतिशत बढ़ा दी है।", "skill_target": "guided composition"},
                ],
                "quiz": [
                    {"q": "In reports, ‘युक्तिसंगत बनाया गया’ about prices almost always means…", "options": ["cut", "raised", "frozen", "abolished"], "answer": 1, "why": "Cuts are announced as राहत; ‘rationalised’ softens a rise."},
                    {"q": "‘पाला बदलना’ comes from…", "options": ["cooking", "a playground game (kabaddi/kho-kho side)", "farming", "weaving"], "answer": 1, "why": "पाला is a side/court in games like kabaddi; switching it = defecting."},
                    {"q": "Which word names the ruling side?", "options": ["हाशिया", "सत्ता", "सौहार्द", "नरमी"], "answer": 1, "why": "सत्ता = power/the ruling side."},
                    {"q": "Best practice when you must mention a euphemism:", "options": ["repeat it as your own words", "quote it and give the plain meaning", "ignore the event", "translate it literally only"], "answer": 1, "why": "Quote, then gloss — the reader gets both the spin and the fact."},
                ],
                "worksheet": {
                    "title": "Spin Translator",
                    "tasks": [
                        {"instruction": "Decode each phrase into a plain event with a named agent.", "items": ["‘सेवा शुल्क में समायोजन’", "‘परियोजना को फिलहाल स्थगित रखा गया है’", "‘कुछ असामाजिक तत्वों ने शांति भंग की’"], "key": ["बैंक ने सेवा शुल्क बढ़ाया।", "सरकार ने परियोजना रोक दी।", "दंगाइयों ने हिंसा की — ‘असामाजिक तत्व’ नाम छिपाता है।"]},
                        {"instruction": "Pair each metaphor with its literal source.", "items": ["कुर्सी", "हाशिया", "पाला"], "key": ["chair → office", "page margin → exclusion", "game side → party"]},
                        {"instruction": "Collect three euphemisms from any Hindi news source this week and decode them in one line each.", "items": ["your own examples"], "key": ["(open task — check: plain verb + agent for each)"]},
                    ],
                },
                "srs": ["युक्तिसंगत", "झटका", "पाला बदलना", "हाशिये पर"],
            },
        ],
    },
    # ------------------------------------------------------------------ U2
    {
        "id": "hi-c3-u2",
        "title": "Humour, Satire and Wordplay",
        "lessons": [
            {
                "id": "hi-c3-l4",
                "title": "Vyangya: Saying the Opposite with a Straight Face",
                "learn": "व्यंग्य (satire) in Hindi rarely shouts. It praises what it attacks — ‘वाह, क्या व्यवस्था है!’ said about a broken system — and relies on particles (तो, ही, भी, ज़रूर), exaggerated respect, and a deadpan tone. You learn to hear the gap between the words and the voice, and to produce it without tipping into insult.",
                "vocab": [
                    ("व्यंग्य", "vyaṅgya", "satire; irony", "noun"),
                    ("तंज़", "tanz", "taunt; sarcastic remark", "noun"),
                    ("कटाक्ष", "kaṭākṣ", "sideways dig; sarcastic jibe", "noun"),
                    ("बेशक", "beśak", "of course (often ironic)", "adverb"),
                    ("ज़रूर", "zarūr", "certainly (ironic in context)", "adverb"),
                    ("महान", "mahān", "great (ironic when over-applied)", "adjective"),
                    ("व्यवस्था", "vyavasthā", "the system; arrangements", "noun"),
                    ("चुटकी लेना", "cuṭkī lenā", "to take a dig; tease", "verb phrase"),
                ],
                "grammar": {
                    "title": "Irony markers: particles and inflated praise",
                    "explain": "Three signals mark Hindi irony: (1) तो/ही/भी placed for contrast — ‘आप तो समय पर आ ही गए’ to someone two hours late; (2) over-formal praise in a trivial setting — ‘महान कार्य’ for fixing a bulb after a month; (3) agreement words used as disagreement — बेशक, ज़रूर, क्यों नहीं. The verb stays polite; the attack is in the mismatch. In writing, no exclamation mark is needed; the flatter, the sharper.",
                    "pattern": "polite/inflated statement + contrast particle (तो/ही/भी) + context that contradicts it",
                    "examples": [
                        ("वाह! सड़क क्या बनी है — हर मोड़ पर एक तालाब मुफ़्त।", "vāh! saṛak kyā banī hai — har moṛ par ek tālāb muft.", "Bravo! What a road — a free pond at every turn."),
                        ("आप तो ठीक समय पर आ ही गए, बस सभा खत्म हुई है।", "āp to ṭhīk samay par ā hī gae, bas sabhā khatm huī hai.", "You've arrived right on time — the meeting's only just ended."),
                        ("बेशक, फ़ाइल कल ज़रूर आगे बढ़ेगी — जैसे पिछले छह महीने बढ़ी।", "beśak, fāil kal zarūr āge baṛhegī — jaise pichhle chah mahīne baṛhī.", "Of course, the file will certainly move tomorrow — as it did these last six months."),
                    ],
                    "mistakes": [
                        "Irony aimed at a person's body, caste or religion is not satire; it is abuse. Aim at systems, habits and power.",
                        "Adding ‘(sarcasm)’ or many exclamation marks kills the effect; let the contrast do the work.",
                    ],
                },
                "dialogue": [
                    ("राहुल", "बिजली फिर गई। वाह, क्या व्यवस्था है!", "bijlī phir gaī. vāh, kyā vyavasthā hai!", "Power's gone again. Bravo, what a system!"),
                    ("मीना", "बेशक। महीने में सिर्फ़ बीस बार तो जाती है।", "beśak. mahīne mẽ sirf bīs bār to jātī hai.", "Of course. It only goes twenty times a month."),
                    ("राहुल", "शिकायत करें?", "śikāyat karẽ?", "Shall we complain?"),
                    ("मीना", "ज़रूर करो — पिछली तीन शिकायतों का जवाब बस आता ही होगा।", "zarūr karo — pichhlī tīn śikāyatõ kā javāb bas ātā hī hogā.", "Certainly — the reply to the last three complaints must be just arriving."),
                ],
                "practice": [
                    {"type": "transformation", "q": "Make it ironic using तो…ही: ‘आप देर से आए।’ (the person is very late)", "answer": "आप तो बिल्कुल समय पर आ ही गए।", "skill_target": "irony production"},
                    {"type": "multiple_choice", "q": "Which reply is ironic agreement?", "answer": "बेशक, जैसे पिछली बार हुआ था।", "skill_target": "irony recognition", "options": ["हाँ, ठीक है।", "बेशक, जैसे पिछली बार हुआ था।", "नहीं, मैं सहमत नहीं हूँ।", "मुझे नहीं पता।"]},
                    {"type": "reverse_translation", "q": "Translate, keeping the irony: ‘क्या बढ़िया सेवा है — बिल समय पर, पानी कभी नहीं।’", "answer": "What excellent service — the bill on time, the water never.", "skill_target": "irony translation"},
                    {"type": "error_correction", "q": "This ‘satire’ attacks a person's appearance. Redirect it at the system: ‘मोटे अफ़सर ने फ़ाइल दबा दी।’", "answer": "दफ़्तर ने फ़ाइल को छह महीने ‘विचाराधीन’ रखा — यानी दबा दी।", "skill_target": "ethical satire"},
                    {"type": "fill_in_the_blank", "q": "उसने मेरी देरी पर ____ ली: ‘आज सूरज पश्चिम से निकला क्या?’ (took a dig)", "answer": "चुटकी", "skill_target": "idiom"},
                    {"type": "word_selection", "q": "Which word is a sharp sideways jibe?", "answer": "कटाक्ष", "skill_target": "vocabulary", "options": ["व्यवस्था", "कटाक्ष", "महान", "बेशक"]},
                    {"type": "guided_composition", "q": "Write three deadpan ironic lines about a park that has a ‘No littering’ sign surrounded by litter.", "answer": "बोर्ड साफ़ लिखा है — ‘कूड़ा न फेंकें’। लोगों ने उसे पढ़ने लायक जगह भी साफ़ छोड़ी है। बाकी पार्क कूड़े ने अपनी ज़िम्मेदारी पर सँभाल लिया है।", "skill_target": "guided composition"},
                ],
                "quiz": [
                    {"q": "Which particle pattern commonly signals irony?", "options": ["ने … को", "तो … ही", "से … तक", "और … या"], "answer": 1, "why": "तो…ही sets up a contrast with reality: ‘आप तो समय पर आ ही गए’."},
                    {"q": "‘बेशक’ in an ironic reply means…", "options": ["I truly agree", "I disagree and am mocking the claim", "maybe", "I don't know"], "answer": 1, "why": "Agreement words flip to mockery when the context contradicts them."},
                    {"q": "Good satire targets…", "options": ["someone's body", "someone's caste", "systems, habits and power", "a child's mistake"], "answer": 2, "why": "Satire punches at power and systems, never at identity."},
                    {"q": "चुटकी लेना means…", "options": ["to pinch salt", "to take a teasing dig", "to clap", "to whisper"], "answer": 1, "why": "Figuratively: to tease with a quick remark."},
                ],
                "worksheet": {
                    "title": "Deadpan Workshop",
                    "tasks": [
                        {"instruction": "Rewrite each complaint as a one-line ironic remark.", "items": ["The lift has been broken for a year.", "The new app crashes on opening."], "key": ["लिफ़्ट एक साल से ‘अस्थायी रूप से’ बंद है — स्थायी रूप से।", "ऐप शानदार है — खुलते ही आराम करने चला जाता है।"]},
                        {"instruction": "Identify the irony marker in each line.", "items": ["आप तो बड़े समझदार निकले।", "ज़रूर, कल पक्का हो जाएगा।"], "key": ["तो…निकले (inflated praise + contrast)", "ज़रूर + पक्का (over-assurance)"]},
                        {"instruction": "Write a 120-word व्यंग्य about a committee formed to decide whether to form a committee.", "items": ["open task"], "key": ["Check: no personal attack; at least two particles (तो/ही/भी) and one inflated-praise phrase."]},
                    ],
                },
                "srs": ["व्यंग्य", "तंज़", "कटाक्ष", "चुटकी लेना"],
            },
            {
                "id": "hi-c3-l5",
                "title": "Proverbs and Puns in Argument",
                "learn": "A well-placed कहावत ends an argument in Hindi; a pun (श्लेष) wins the room. At expert level you must know the proverb, its literal image, when it is apt, and how speakers twist it. Half a proverb is enough among natives: ‘अब पछताए होत क्या…’ — everyone completes it.",
                "vocab": [
                    ("कहावत", "kahāvat", "proverb; saying", "noun"),
                    ("लोकोक्ति", "lokokti", "folk saying (literary term)", "noun"),
                    ("श्लेष", "śleṣ", "pun; double meaning", "noun"),
                    ("चिड़िया चुग गई खेत", "ciṛiyā cug gaī khet", "the birds have eaten the field (too late now)", "proverb"),
                    ("ऊँट के मुँह में जीरा", "ū̃ṭ ke mũh mẽ jīrā", "a cumin seed in a camel's mouth (far too little)", "proverb"),
                    ("जिसकी लाठी उसकी भैंस", "jiskī lāṭhī uskī bhaĩs", "whoever holds the stick owns the buffalo (might is right)", "proverb"),
                    ("घर की मुर्गी दाल बराबर", "ghar kī murgī dāl barābar", "home chicken counts as lentils (familiar things are undervalued)", "proverb"),
                    ("अधजल गगरी छलकत जाए", "adhjal gagrī chalkat jāe", "the half-full pot splashes (shallow people make noise)", "proverb"),
                ],
                "grammar": {
                    "title": "Deploying a proverb: full, half, twisted",
                    "explain": "Full form for writing: ‘अब पछताए होत क्या, जब चिड़िया चुग गई खेत’. Half form in speech: ‘अब क्या — चिड़िया चुग गई खेत’. Twisted form for humour: swap one noun to fit the situation — ‘जिसकी सत्ता उसकी भैंस’. Proverbs keep archaic verb forms (होत, छलकत = Awadhi/Braj present); do not modernise them. Introduce with कहावत है कि / कहते हैं न.",
                    "pattern": "कहावत है (कि) + proverb · कहते हैं न, + half proverb · twisted: keep rhythm, swap one noun",
                    "examples": [
                        ("कहते हैं न — अब पछताए होत क्या, जब चिड़िया चुग गई खेत।", "kahte haĩ na — ab pachhtāe hot kyā, jab ciṛiyā cug gaī khet.", "As they say — what use regretting now the birds have eaten the field."),
                        ("दस हज़ार की मदद? इतनी बड़ी बाढ़ में ऊँट के मुँह में जीरा।", "das hazār kī madad? itnī baṛī bāṛh mẽ ū̃ṭ ke mũh mẽ jīrā.", "Ten thousand in aid? In a flood this size, a cumin seed in a camel's mouth."),
                        ("हमारे इंजीनियर विदेश में हीरो, यहाँ घर की मुर्गी दाल बराबर।", "hamāre injīniyar videś mẽ hīro, yahā̃ ghar kī murgī dāl barābar.", "Our engineers are heroes abroad; here, home chicken counts as lentils."),
                    ],
                    "mistakes": [
                        "Explaining the proverb after using it (‘…यानी बहुत देर हो गई’) insults the listener; trust the image.",
                        "Changing the archaic verb (होत → होता है) breaks the metre and sounds like a learner.",
                    ],
                },
                "dialogue": [
                    ("अजय", "अब रिपोर्ट सुधारने का क्या फ़ायदा? नतीजे आ गए।", "ab riporṭ sudhārne kā kyā fāydā? natīje ā gae.", "What's the point of fixing the report now? The results are out."),
                    ("सीमा", "हाँ, चिड़िया चुग गई खेत। पर अगली बार के लिए सीख तो है।", "hā̃, ciṛiyā cug gaī khet. par aglī bār ke lie sīkh to hai.", "Yes, the birds have eaten the field. But there's a lesson for next time."),
                    ("अजय", "और जो सबसे ज़्यादा बोल रहा था, उसने सबसे कम काम किया।", "aur jo sabse zyādā bol rahā thā, usne sabse kam kām kiyā.", "And the one who talked most did the least."),
                    ("सीमा", "अधजल गगरी छलकत जाए — नाम लेने की ज़रूरत नहीं।", "adhjal gagrī chalkat jāe — nām lene kī zarūrat nahī̃.", "The half-full pot splashes — no need to name names."),
                ],
                "practice": [
                    {"type": "dialogue_completion", "q": "A: हमने बहुत देर कर दी, अब मुआवज़ा नहीं मिलेगा। B: (reply with the apt proverb, half form)", "answer": "हाँ, अब पछताए होत क्या…", "skill_target": "proverb use"},
                    {"type": "multiple_choice", "q": "Which proverb fits: a huge company fined a tiny amount?", "answer": "ऊँट के मुँह में जीरा", "skill_target": "proverb selection", "options": ["घर की मुर्गी दाल बराबर", "ऊँट के मुँह में जीरा", "अधजल गगरी छलकत जाए", "चिड़िया चुग गई खेत"]},
                    {"type": "transformation", "q": "Twist ‘जिसकी लाठी उसकी भैंस’ for an office where whoever has the boss's ear wins.", "answer": "जिसकी बॉस से नज़दीकी, उसकी भैंस।", "skill_target": "creative twist"},
                    {"type": "reverse_translation", "q": "Translate with an English equivalent: ‘घर की मुर्गी दाल बराबर’", "answer": "Familiarity breeds contempt / a prophet is not honoured in his own land.", "skill_target": "equivalence"},
                    {"type": "error_correction", "q": "Fix the modernised proverb: ‘अधजल गगरी छलकती जाती है।’", "answer": "अधजल गगरी छलकत जाए।", "skill_target": "archaic form"},
                    {"type": "fill_in_the_blank", "q": "The literary term for a folk proverb is ____; a pun is ____.", "answer": "लोकोक्ति; श्लेष", "skill_target": "terminology"},
                    {"type": "guided_composition", "q": "Write a four-line exchange where one speaker uses a half proverb and the other twists it back.", "answer": "— अब क्या, चिड़िया चुग गई खेत। — चुग गई तो क्या, अगली फ़सल के लिए बिजूका तो लगा लें!", "skill_target": "guided composition"},
                ],
                "quiz": [
                    {"q": "‘होत’ in ‘अब पछताए होत क्या’ is…", "options": ["a typo", "an archaic/Awadhi present form kept in the proverb", "a noun", "Urdu"], "answer": 1, "why": "Proverbs preserve older verb forms; keep them."},
                    {"q": "A half proverb is appropriate when…", "options": ["writing a legal notice", "speaking to natives who know the rest", "teaching beginners", "translating for foreigners"], "answer": 1, "why": "Natives complete it mentally; half form is natural in speech."},
                    {"q": "श्लेष means…", "options": ["proverb", "pun / double meaning", "rhyme", "insult"], "answer": 1, "why": "श्लेष is the figure of speech of double meaning."},
                    {"q": "‘जिसकी लाठी उसकी भैंस’ criticises…", "options": ["farmers", "might-is-right", "laziness", "greed for food"], "answer": 1, "why": "Whoever holds the stick owns the buffalo — power decides."},
                ],
                "worksheet": {
                    "title": "Proverb Toolkit",
                    "tasks": [
                        {"instruction": "Give the literal image and the meaning.", "items": ["ऊँट के मुँह में जीरा", "घर की मुर्गी दाल बराबर"], "key": ["cumin in a camel's mouth → far too little", "home chicken = lentils → the familiar is undervalued"]},
                        {"instruction": "Choose a proverb for each situation.", "items": ["A loud colleague who knows little", "A bully who wins because he is strong"], "key": ["अधजल गगरी छलकत जाए", "जिसकी लाठी उसकी भैंस"]},
                        {"instruction": "Collect five proverbs from an elder in your family or from a Hindi speaker; write each with its image and a modern situation.", "items": ["open task"], "key": ["(open — check image + situation for each)"]},
                    ],
                },
                "srs": ["कहावत", "श्लेष", "चिड़िया चुग गई खेत", "ऊँट के मुँह में जीरा"],
            },
            {
                "id": "hi-c3-l6",
                "title": "Film and Street Hindi: Hinglish and Bambaiya",
                "learn": "The Hindi of films, memes and metro cities is a mix: English verbs with Hindi endings (मैनेज करना, चिल मारना), Mumbai street forms (अपुन, क्या रे, बोले तो), and code-switching mid-sentence. Experts understand it instantly, can imitate it for effect, and know where it is out of place.",
                "vocab": [
                    ("अपुन", "apun", "I / we (Bambaiya)", "pronoun"),
                    ("बोले तो", "bole to", "that is to say; like (Bambaiya filler)", "phrase"),
                    ("क्या रे", "kyā re", "hey, what's up (Mumbai, familiar)", "interjection"),
                    ("झकास", "jhakās", "awesome (Bambaiya)", "adjective"),
                    ("टेंशन मत ले", "ṭenśan mat le", "don't stress (Hinglish)", "phrase"),
                    ("सीन क्या है", "sīn kyā hai", "what's the plan / situation", "phrase"),
                    ("मैनेज कर लेंगे", "mainej kar lẽge", "we'll manage", "phrase"),
                    ("कोड-मिश्रण", "koḍ-miśraṇ", "code-mixing", "noun"),
                ],
                "grammar": {
                    "title": "How English verbs enter Hindi",
                    "explain": "English verbs come in as noun + करना/होना/मारना: मैनेज करना, अपडेट होना, चिल मारना. Hindi grammar wins: tense, gender and ने belong to the Hindi light verb (उसने फ़ाइल सेव की — feminine agreeing with फ़ाइल). Bambaiya adds its own pronouns (अपुन, तेरेको, मेरेको) and a flat -ता/-ती for all persons (अपुन जाता है). Use it in dialogue, memes and jokes; never in a letter to a client.",
                    "pattern": "ENGLISH NOUN/VERB + करना/होना/मारना/लेना  (Hindi agreement on the light verb)",
                    "examples": [
                        ("अपुन बोले तो एकदम झकास फ़ीलिंग में है।", "apun bole to ekdam jhakās fīliṅg mẽ hai.", "Me — I'm in a totally awesome mood, like."),
                        ("टेंशन मत ले, डेडलाइन मैनेज कर लेंगे।", "ṭenśan mat le, ḍeḍlāin mainej kar lẽge.", "Don't stress, we'll manage the deadline."),
                        ("उसने प्रेज़ेंटेशन अपडेट कर दी है।", "usne prezenṭeśan apḍeṭ kar dī hai.", "She has updated the presentation."),
                    ],
                    "mistakes": [
                        "Agreement goes with the Hindi object, not the English word's ‘feel’: फ़ाइल सेव की (f.), डेटा सेव किया (m.).",
                        "Bambaiya अपुन/तेरेको in a formal email or to an elder sounds disrespectful, not cool.",
                    ],
                },
                "dialogue": [
                    ("विक्की", "क्या रे, शनिवार का सीन क्या है?", "kyā re, śanivār kā sīn kyā hai?", "Hey, what's the plan for Saturday?"),
                    ("सोनू", "अपुन फ़्री है। बोले तो, फ़िल्म चलें?", "apun frī hai. bole to, film calẽ?", "I'm free. Like, shall we catch a film?"),
                    ("विक्की", "टिकट मैनेज हो जाएँगे?", "ṭikaṭ mainej ho jāẽge?", "Can we manage tickets?"),
                    ("सोनू", "टेंशन मत ले, मेरेको ऐप पर ऑफ़र दिखा — एकदम झकास।", "ṭenśan mat le, mereko aip par ofar dikhā — ekdam jhakās.", "Don't stress, I saw an offer on the app — totally awesome."),
                ],
                "practice": [
                    {"type": "register_transformation", "q": "Turn into standard polite Hindi: ‘अपुन कल मीटिंग अटेंड नहीं कर पाएगा, मैनेज कर लेना।’", "answer": "मैं कल बैठक में शामिल नहीं हो पाऊँगा; कृपया व्यवस्था सँभाल लीजिए।", "skill_target": "register transformation"},
                    {"type": "register_transformation", "q": "Turn into Bambaiya for a film dialogue: ‘मैं ठीक हूँ, चिंता मत करो।’", "answer": "अपुन एकदम ठीक है, टेंशन मत ले।", "skill_target": "stylisation"},
                    {"type": "error_correction", "q": "Fix the agreement: ‘उसने रिपोर्ट सबमिट किया।’", "answer": "उसने रिपोर्ट सबमिट की।", "skill_target": "light-verb agreement"},
                    {"type": "multiple_choice", "q": "Where is ‘क्या रे, सीन क्या है?’ appropriate?", "answer": "a WhatsApp message to a close friend", "skill_target": "appropriateness", "options": ["an email to a client", "a WhatsApp message to a close friend", "a speech at a wedding", "a complaint to the municipality"]},
                    {"type": "fill_in_the_blank", "q": "Mumbai Hindi says ____ for ‘I/we’ and ____ for ‘that is to say’.", "answer": "अपुन; बोले तो", "skill_target": "dialect lexicon"},
                    {"type": "reverse_translation", "q": "Translate naturally: ‘डेटा तो सेव हो गया, पर फ़ाइल करप्ट हो गई।’", "answer": "The data got saved, but the file got corrupted.", "skill_target": "Hinglish comprehension"},
                    {"type": "guided_composition", "q": "Write a four-line meme caption exchange in Hinglish between two colleagues before a deadline, then its formal one-line summary.", "answer": "— डेडलाइन कल है। — पता है, टेंशन मत ले। — फ़ाइल कहाँ है? — मैनेज कर लेंगे… शायद। / सारांश: टीम समय-सीमा को लेकर अनिश्चित है।", "skill_target": "guided composition"},
                ],
                "quiz": [
                    {"q": "In ‘उसने फ़ाइल सेव की’, the verb agrees with…", "options": ["उसने", "फ़ाइल (feminine)", "सेव", "nothing"], "answer": 1, "why": "Hindi rules: with ने, the light verb agrees with the object फ़ाइल (f.)."},
                    {"q": "‘बोले तो’ in Bambaiya functions as…", "options": ["a past tense", "a filler meaning ‘that is / like’", "a question", "a plural marker"], "answer": 1, "why": "It introduces a gloss or just fills, like English ‘like’."},
                    {"q": "Which is NOT Bambaiya?", "options": ["अपुन", "मेरेको", "झकास", "कृपया"], "answer": 3, "why": "कृपया is formal standard Hindi."},
                    {"q": "Code-mixing is best described as…", "options": ["a grammar error", "switching languages within a sentence by fluent speakers", "a dialect of Marathi", "a spelling reform"], "answer": 1, "why": "Fluent bilinguals mix codes systematically; it is not an error."},
                ],
                "worksheet": {
                    "title": "Street to Standard",
                    "tasks": [
                        {"instruction": "Rewrite each line in standard polite Hindi.", "items": ["तेरेको क्या प्रॉब्लम है?", "अपुन को ये काम नहीं जमता।"], "key": ["आपको क्या समस्या है?", "मुझे यह काम पसंद नहीं आता।"]},
                        {"instruction": "Mark the gender agreement of the light verb.", "items": ["उसने ईमेल भेज (दिया/दी)।", "उसने मैसेज पढ़ (लिया/ली)।"], "key": ["दिया (ईमेल m.)", "लिया (मैसेज m.)"]},
                        {"instruction": "Watch any two-minute Hindi film clip and list five English-origin verbs with their Hindi light verbs.", "items": ["open task"], "key": ["e.g. मैनेज करना, ट्राई करना, एंजॉय करना, हैंडल करना, डील करना"]},
                    ],
                },
                "srs": ["अपुन", "बोले तो", "झकास", "कोड-मिश्रण"],
            },
        ],
    },
    # ------------------------------------------------------------------ U3
    {
        "id": "hi-c3-u3",
        "title": "Regional and Social Texture",
        "lessons": [
            {
                "id": "hi-c3-l7",
                "title": "Dialect Colour: Awadhi, Braj and Bhojpuri Traces",
                "learn": "Standard Hindi sits on a family of regional speeches. Film songs borrow Braj (मोहे, तोहे), village scenes use Awadhi (हमका, का हो), and Bhojpuri gives Hindi comedy its rhythm (का हो, बा, रउआ). You do not need to speak them, but an expert recognises them, knows the region, and never mocks the speaker.",
                "vocab": [
                    ("हमका", "hamkā", "to me/us (Awadhi)", "pronoun"),
                    ("का हो", "kā ho", "what's up / hey (Bhojpuri-Awadhi)", "interjection"),
                    ("रउआ", "rauā", "you, respectful (Bhojpuri)", "pronoun"),
                    ("बा", "bā", "is (Bhojpuri)", "verb"),
                    ("मोहे", "mohe", "to me (Braj, poetic)", "pronoun"),
                    ("तोहे", "tohe", "to you (Braj, poetic)", "pronoun"),
                    ("बोली", "bolī", "dialect; speech variety", "noun"),
                    ("खड़ी बोली", "khaṛī bolī", "Khari Boli, the base of standard Hindi", "noun"),
                ],
                "grammar": {
                    "title": "Recognising a dialect in three cues",
                    "explain": "Cue 1 — pronoun: हमका/हमें (Awadhi), मोहे/तोहे (Braj), रउआ/तोहरा (Bhojpuri). Cue 2 — the copula: बा/बाड़े (Bhojpuri) vs है. Cue 3 — the question word: का for क्या across the eastern belt. In standard prose these appear only in quoted speech, songs, or deliberate colour. When you quote them, keep the spelling the speaker would use and do not ‘correct’ it.",
                    "pattern": "standard: मुझे क्या चाहिए? · Awadhi: हमका का चाही? · Bhojpuri: हमरा का चाहीं? · Braj (poetic): मोहे का चहिए?",
                    "examples": [
                        ("का हो, कहाँ चलल बाड़ऽ? — भोजपुरी", "kā ho, kahā̃ calal bāṛa? — bhojpurī", "Hey, where are you off to? — Bhojpuri"),
                        ("हमका तनिक पानी दे दो, बिटिया। — अवधी रंग", "hamkā tanik pānī de do, biṭiyā. — avadhī raṅg", "Give me a little water, child. — Awadhi colour"),
                        ("मोहे रंग दे बसंती — ब्रज की गूँज", "mohe raṅg de basantī — braj kī gū̃j", "Colour me saffron — an echo of Braj"),
                    ],
                    "mistakes": [
                        "Calling a dialect ‘wrong Hindi’ is both rude and inaccurate; Awadhi and Braj have older literatures than Khari Boli.",
                        "Imitating a village dialect for laughs at a speaker's expense is mockery, not colour.",
                    ],
                },
                "dialogue": [
                    ("तनु", "गाने में ‘मोहे’ क्यों है, ‘मुझे’ क्यों नहीं?", "gāne mẽ ‘mohe’ kyõ hai, ‘mujhe’ kyõ nahī̃?", "Why does the song say ‘mohe’, not ‘mujhe’?"),
                    ("नानी", "वह ब्रज है, कृष्ण की भूमि की बोली। गीतों में वही मीठी लगती है।", "vah braj hai, kṛṣṇa kī bhūmi kī bolī. gītõ mẽ vahī mīṭhī lagtī hai.", "That's Braj, the speech of Krishna's land. In songs it sounds sweetest."),
                    ("तनु", "और गाँव वाले चाचा ‘हमका’ कहते हैं।", "aur gā̃v vāle cācā ‘hamkā’ kahte haĩ.", "And uncle from the village says ‘hamkā’."),
                    ("नानी", "वह अवधी है — तुलसीदास की भाषा। कोई भी ग़लत नहीं है।", "vah avadhī hai — tulsīdās kī bhāṣā. koī bhī galat nahī̃ hai.", "That's Awadhi — Tulsidas's language. None of them is wrong."),
                ],
                "practice": [
                    {"type": "multiple_choice", "q": "Which cue marks ‘का हो, ठीक बा?’ as Bhojpuri?", "answer": "the copula बा and का for क्या", "skill_target": "dialect recognition", "options": ["the word ठीक", "the copula बा and का for क्या", "the question mark", "the verb हो"]},
                    {"type": "matching", "q": "Match the pronoun with the variety: मोहे / हमका / रउआ", "answer": "मोहे – ब्रज; हमका – अवधी; रउआ – भोजपुरी", "skill_target": "matching", "options": ["मोहे – ब्रज; हमका – अवधी; रउआ – भोजपुरी", "मोहे – भोजपुरी; हमका – ब्रज; रउआ – अवधी", "मोहे – अवधी; हमका – भोजपुरी; रउआ – ब्रज"]},
                    {"type": "transformation", "q": "Give the standard Hindi for: ‘हमका का पता, तू कहाँ गइल?’", "answer": "मुझे क्या पता, तुम कहाँ गए?", "skill_target": "dialect to standard"},
                    {"type": "reverse_translation", "q": "Translate: ‘रउआ कइसन बानी?’ (Bhojpuri, respectful)", "answer": "How are you? (respectful)", "skill_target": "comprehension"},
                    {"type": "error_correction", "q": "Rewrite without disrespect: ‘गाँव वाले टूटी-फूटी हिंदी बोलते हैं।’", "answer": "गाँव के लोग अवधी या भोजपुरी बोलते हैं, जो अपनी पूरी भाषाएँ हैं।", "skill_target": "respectful framing"},
                    {"type": "fill_in_the_blank", "q": "Standard Hindi is based on the dialect of the Delhi–Meerut region called ____.", "answer": "खड़ी बोली", "skill_target": "terminology"},
                    {"type": "guided_composition", "q": "Write a short scene (four lines) where a city visitor and a village elder understand each other across standard Hindi and Awadhi colour.", "answer": "— नमस्ते बाबा, रास्ता यही है? — हाँ बिटिया, सीधे चली जाओ, हमका भी उधरै जाना है। — चलिए साथ चलते हैं। — चलो, बतियाते चलब।", "skill_target": "guided composition"},
                ],
                "quiz": [
                    {"q": "‘मोहे’ and ‘तोहे’ belong to…", "options": ["Braj", "Punjabi", "Marathi", "Bengali"], "answer": 0, "why": "They are Braj pronouns, common in devotional and film songs."},
                    {"q": "The copula ‘बा’ marks…", "options": ["Awadhi", "Bhojpuri", "Haryanvi", "Rajasthani"], "answer": 1, "why": "बा/बाड़े = ‘is/are’ in Bhojpuri."},
                    {"q": "Tulsidas wrote the Ramcharitmanas mainly in…", "options": ["Khari Boli", "Awadhi", "Bambaiya", "Urdu"], "answer": 1, "why": "The Ramcharitmanas is in Awadhi."},
                    {"q": "When quoting a dialect speaker in prose you should…", "options": ["correct it to standard", "keep their forms as spoken", "translate to English", "omit it"], "answer": 1, "why": "Quoted speech keeps the speaker's variety; that is respect and accuracy."},
                ],
                "worksheet": {
                    "title": "Dialect Ear",
                    "tasks": [
                        {"instruction": "Name the variety from the cue.", "items": ["हमका", "बाड़ऽ", "तोहे"], "key": ["अवधी", "भोजपुरी", "ब्रज"]},
                        {"instruction": "Convert to standard Hindi.", "items": ["का हो, खाना खइलऽ?", "हमका नाहीं मालूम।"], "key": ["क्या भाई, खाना खाया?", "मुझे नहीं मालूम।"]},
                        {"instruction": "Listen to one folk or film song with Braj or Bhojpuri words; list four words and their standard forms.", "items": ["open task"], "key": ["e.g. मोहे→मुझे, तोहे→तुझे, पिया→प्रिय/पति, सइयाँ→साजन"]},
                    ],
                },
                "srs": ["हमका", "का हो", "मोहे", "खड़ी बोली"],
            },
            {
                "id": "hi-c3-l8",
                "title": "Respectful and Inclusive Wording",
                "learn": "Hindi carries social hierarchy in its words. The expert chooses terms that name people as they wish to be named: दिव्यांग rather than विकलांग, दलित rather than older slurs, घरेलू सहायिका rather than नौकरानी, and gender-neutral frames where the gender is unknown. This is not politeness theatre; it is accuracy about people.",
                "vocab": [
                    ("दिव्यांग", "divyāṅg", "person with a disability (preferred term)", "noun"),
                    ("वरिष्ठ नागरिक", "variṣṭh nāgarik", "senior citizen", "noun"),
                    ("घरेलू सहायिका", "gharelū sahāyikā", "domestic help (woman), respectful", "noun"),
                    ("सफ़ाई कर्मचारी", "safāī karmcārī", "sanitation worker", "noun"),
                    ("समावेशी", "samāveśī", "inclusive", "adjective"),
                    ("पूर्वग्रह", "pūrvagrah", "prejudice", "noun"),
                    ("सम्बोधन", "sambodhan", "form of address", "noun"),
                    ("अन्य", "anya", "other (gender option on forms)", "adjective"),
                ],
                "grammar": {
                    "title": "Gender-neutral and person-first phrasing",
                    "explain": "When the person's gender is unknown, avoid forcing masculine: use plural (आवेदक अपना नाम लिखें), the noun व्यक्ति (कोई व्यक्ति), or recast as a noun phrase (आवेदन करने वाले). For groups, name the role not the body: सफ़ाई कर्मचारी, घरेलू सहायिका. For disability, lead with the person: दिव्यांग व्यक्ति / दृष्टिबाधित छात्र. Honorific plural (वे, हैं) applies to any adult whose status you respect, regardless of job.",
                    "pattern": "unknown gender → plural verb / व्यक्ति / -वाले ; role not body; person before condition",
                    "examples": [
                        ("हर आवेदक अपने दस्तावेज़ साथ लाएँ।", "har āvedak apne dastāvez sāth lāẽ.", "Every applicant should bring their documents (plural avoids he/she)."),
                        ("दृष्टिबाधित छात्रों के लिए अलग से समय दिया जाएगा।", "dṛṣṭibādhit chātrõ ke lie alag se samay diyā jāegā.", "Visually impaired students will be given extra time."),
                        ("हमारी घरेलू सहायिका सविता जी दस साल से हमारे साथ हैं।", "hamārī gharelū sahāyikā savitā jī das sāl se hamāre sāth haĩ.", "Our domestic help, Savita ji, has been with us for ten years."),
                    ],
                    "mistakes": [
                        "Using तू or bare name for workers but आप for guests encodes hierarchy; adults get आप.",
                        "‘बेचारा दिव्यांग’ — pity words (बेचारा) undo the respect of the term.",
                    ],
                },
                "dialogue": [
                    ("प्रिया", "फ़ॉर्म में लिखा है ‘वह अपना नाम लिखे’। महिला आवेदक के लिए?", "fôrm mẽ likhā hai ‘vah apnā nām likhe’. mahilā āvedak ke lie?", "The form says ‘he should write his name’. What about women applicants?"),
                    ("अधिकारी", "सही कहा। ‘आवेदक अपना नाम लिखें’ कर देते हैं — सब पर लागू।", "sahī kahā. ‘āvedak apnā nām likhẽ’ kar dete haĩ — sab par lāgū.", "Fair point. Let's make it ‘applicants should write their name’ — covers everyone."),
                    ("प्रिया", "और ‘विकलांग’ की जगह?", "aur ‘vikalāṅg’ kī jagah?", "And instead of ‘vikalāṅg’?"),
                    ("अधिकारी", "‘दिव्यांग व्यक्ति’। और नीचे ‘अन्य’ का विकल्प भी जोड़ देंगे।", "‘divyāṅg vyakti’. aur nīce ‘anya’ kā vikalp bhī joṛ dẽge.", "‘Divyāṅg vyakti’. And we'll add an ‘other’ option below too."),
                ],
                "practice": [
                    {"type": "error_correction", "q": "Make it gender-neutral: ‘हर छात्र अपनी किताब लाए।’", "answer": "सभी छात्र अपनी किताबें लाएँ।", "skill_target": "neutral phrasing"},
                    {"type": "register_transformation", "q": "Rewrite respectfully: ‘नौकरानी को बोलो चाय लाए।’", "answer": "सविता जी से कहिए कि चाय ले आएँ।", "skill_target": "respectful address"},
                    {"type": "multiple_choice", "q": "Preferred term for a person with a disability in official Hindi:", "answer": "दिव्यांग व्यक्ति", "skill_target": "terminology", "options": ["अपाहिज", "विकलांग", "दिव्यांग व्यक्ति", "लाचार"]},
                    {"type": "word_selection", "q": "Choose the role-based term for a cleaner.", "answer": "सफ़ाई कर्मचारी", "skill_target": "role naming", "options": ["सफ़ाई कर्मचारी", "झाड़ूवाला", "मेहतर", "नौकर"]},
                    {"type": "fill_in_the_blank", "q": "A bias formed before knowing the facts is called ____.", "answer": "पूर्वग्रह", "skill_target": "vocabulary"},
                    {"type": "reverse_translation", "q": "Translate: ‘वरिष्ठ नागरिकों के लिए अलग पंक्ति है।’", "answer": "There is a separate queue for senior citizens.", "skill_target": "comprehension"},
                    {"type": "guided_composition", "q": "Rewrite this notice inclusively (3 lines): ‘हर कर्मचारी अपनी पत्नी के साथ आए। विकलांग लोग पीछे बैठें।’", "answer": "सभी कर्मचारी अपने जीवनसाथी के साथ आमंत्रित हैं। दिव्यांग अतिथियों के लिए आगे की पंक्ति में सुगम बैठने की व्यवस्था है। सहायता के लिए स्वयंसेवक उपलब्ध रहेंगे।", "skill_target": "guided composition"},
                ],
                "quiz": [
                    {"q": "Which device avoids forcing masculine for an unknown person?", "options": ["use तू", "use the plural (आवेदक … लिखें)", "add जी", "use English"], "answer": 1, "why": "Plural verbs and nouns sidestep he/she in Hindi."},
                    {"q": "‘बेचारा’ before दिव्यांग…", "options": ["adds respect", "adds pity and undermines dignity", "is required", "is a plural marker"], "answer": 1, "why": "Pity words undo person-first respect."},
                    {"q": "Who should be addressed as आप?", "options": ["only guests", "only elders", "any adult, including workers", "only officials"], "answer": 2, "why": "आप for every adult removes hierarchy from the pronoun."},
                    {"q": "समावेशी means…", "options": ["exclusive", "inclusive", "expensive", "traditional"], "answer": 1, "why": "समावेशी = inclusive."},
                ],
                "worksheet": {
                    "title": "Inclusive Edit",
                    "tasks": [
                        {"instruction": "Replace each term with a respectful equivalent.", "items": ["नौकर", "अंधा", "बूढ़े लोग"], "key": ["सहायक / कर्मचारी", "दृष्टिबाधित व्यक्ति", "वरिष्ठ नागरिक"]},
                        {"instruction": "Rewrite with plural for unknown gender.", "items": ["ग्राहक अपना बिल दिखाए।"], "key": ["ग्राहक अपना बिल दिखाएँ।"]},
                        {"instruction": "Audit one real form or notice you have at home; list three lines you would change and why.", "items": ["open task"], "key": ["(open — check: neutral verb, role term, person-first)"]},
                    ],
                },
                "srs": ["दिव्यांग", "समावेशी", "पूर्वग्रह", "सम्बोधन"],
            },
            {
                "id": "hi-c3-l9",
                "title": "Reading Tone: Sarcasm, Understatement, Silence",
                "learn": "The last expert skill is hearing what is not said. ‘ठीक है’ can mean fine, furious or finished. ‘देखते हैं’ is often a polite no. A long ‘अच्छा…’ is doubt. Understatement (‘थोड़ी-सी दिक़्क़त है’ about a disaster) and strategic silence carry meaning. You learn the cues and how to respond without forcing the speaker to be blunt.",
                "vocab": [
                    ("देखते हैं", "dekhte haĩ", "we'll see (often a soft no)", "phrase"),
                    ("ठीक है", "ṭhīk hai", "okay (tone decides: fine / annoyed / closing)", "phrase"),
                    ("अच्छा…", "acchā…", "I see… (drawn out: doubt)", "interjection"),
                    ("थोड़ी-सी", "thoṛī-sī", "a little (understatement marker)", "adjective"),
                    ("कोई बात नहीं", "koī bāt nahī̃", "never mind (can be hurt)", "phrase"),
                    ("जैसी आपकी मर्ज़ी", "jaisī āpkī marzī", "as you wish (withdrawn consent)", "phrase"),
                    ("चुप्पी", "cuppī", "silence", "noun"),
                    ("लहज़ा", "lahzā", "tone; manner", "noun"),
                ],
                "grammar": {
                    "title": "Cues of indirect refusal and understatement",
                    "explain": "Indirect no: देखते हैं / कोशिश करूँगा / अभी थोड़ा मुश्किल है. Withdrawn consent: जैसी आपकी मर्ज़ी (I disagree but will not fight). Understatement: थोड़ा-सा, ज़रा-सा attached to serious nouns; the smaller the word, the bigger the problem. Closing: a flat ठीक है with no follow-up question. Respond to the meaning, not the words: offer an exit (‘अगर मुश्किल हो तो बाद में बात करते हैं’) rather than pressing.",
                    "pattern": "soft no = देखते हैं / कोशिश करूँगा · understatement = थोड़ा-सा + serious noun · closing = flat ठीक है + silence",
                    "examples": [
                        ("— शनिवार को आ पाओगे? — देखते हैं।  (= शायद नहीं)", "— śanivār ko ā pāoge? — dekhte haĩ.", "— Can you come Saturday? — We'll see. (= probably not)"),
                        ("बस थोड़ी-सी दिक़्क़त है — गोदाम में पानी भर गया है।", "bas thoṛī-sī diqqat hai — godām mẽ pānī bhar gayā hai.", "Just a small problem — the warehouse has flooded."),
                        ("ठीक है। जैसी आपकी मर्ज़ी।  (= मैं सहमत नहीं हूँ)", "ṭhīk hai. jaisī āpkī marzī.", "Fine. As you wish. (= I don't agree)"),
                    ],
                    "mistakes": [
                        "Taking देखते हैं as a yes and planning around it; confirm gently later or offer an easy out.",
                        "Answering understatement literally (‘थोड़ी दिक़्क़त ही तो है’) misses the alarm.",
                    ],
                },
                "dialogue": [
                    ("अनुज", "सर, रिपोर्ट कैसी लगी?", "sar, riporṭ kaisī lagī?", "Sir, how did you find the report?"),
                    ("सर", "अच्छा… ठीक है।", "acchā… ṭhīk hai.", "I see… it's fine."),
                    ("अनुज", "अगर कहीं थोड़ी-सी कमी हो तो बताइए, मैं सुधार लूँगा।", "agar kahī̃ thoṛī-sī kamī ho to batāie, maĩ sudhār lū̃gā.", "If there's any small shortfall, tell me and I'll fix it."),
                    ("सर", "हाँ, दूसरा हिस्सा फिर से देख लो। बाकी ठीक है।", "hā̃, dūsrā hissā phir se dekh lo. bākī ṭhīk hai.", "Yes, look at the second part again. The rest is fine."),
                ],
                "practice": [
                    {"type": "multiple_choice", "q": "‘कोशिश करूँगा’ in reply to an invitation most likely means…", "answer": "probably not, politely", "skill_target": "indirectness", "options": ["definitely yes", "probably not, politely", "I'm angry", "I didn't hear"]},
                    {"type": "dialogue_completion", "q": "A: आप शाम को आ रहे हैं न? B: देखते हैं… A: (respond to the soft no without pressing)", "answer": "कोई बात नहीं, अगर मुश्किल हो तो अगले हफ़्ते मिल लेते हैं।", "skill_target": "responding to indirectness"},
                    {"type": "transformation", "q": "Say it as understatement: ‘पूरा सर्वर क्रैश हो गया है।’", "answer": "सर्वर में थोड़ी-सी दिक़्क़त आ गई है।", "skill_target": "understatement"},
                    {"type": "transformation", "q": "Now decode the understatement into the plain fact: ‘बजट में ज़रा-सी कमी है।’ (context: half the money is missing)", "answer": "बजट का आधा हिस्सा नहीं है।", "skill_target": "decoding"},
                    {"type": "reverse_translation", "q": "Translate, adding the implied meaning in brackets: ‘ठीक है, जैसी आपकी मर्ज़ी।’", "answer": "Fine, as you wish. (I disagree but won't argue.)", "skill_target": "tone translation"},
                    {"type": "fill_in_the_blank", "q": "A drawn-out ‘____…’ before an answer usually signals doubt.", "answer": "अच्छा", "skill_target": "cue recognition"},
                    {"type": "guided_composition", "q": "Write a six-line office dialogue in which one person refuses twice without ever saying नहीं, and the other person understands and gives an exit.", "answer": "— कल की प्रस्तुति आप करेंगे? — देखते हैं, कल थोड़ा व्यस्त हूँ। — कोई बात नहीं, परसों? — कोशिश करूँगा… — समझ गया; मैं कर लेता हूँ, आप बाद में देख लीजिएगा। — धन्यवाद, यही ठीक रहेगा।", "skill_target": "guided composition"},
                ],
                "quiz": [
                    {"q": "A flat ‘ठीक है’ followed by silence usually means…", "options": ["enthusiastic agreement", "the topic is closed / mild displeasure", "a question", "a request for details"], "answer": 1, "why": "Tone and the missing follow-up signal closure."},
                    {"q": "‘थोड़ी-सी दिक़्क़त’ about a flood is…", "options": ["literal", "understatement", "sarcasm at a person", "a proverb"], "answer": 1, "why": "Small words on big problems = understatement."},
                    {"q": "Best response to देखते हैं:", "options": ["insist on a yes", "offer an easy alternative or exit", "get offended", "repeat the question louder"], "answer": 1, "why": "Respect the soft no; give an out."},
                    {"q": "‘जैसी आपकी मर्ज़ी’ signals…", "options": ["full agreement", "withdrawn consent / disagreement without a fight", "gratitude", "confusion"], "answer": 1, "why": "It yields the decision while marking disagreement."},
                ],
                "worksheet": {
                    "title": "Between the Lines",
                    "tasks": [
                        {"instruction": "Write the likely real meaning.", "items": ["कोशिश करूँगा।", "अच्छा… ठीक है।", "बस ज़रा-सी बात है।"], "key": ["शायद नहीं", "संदेह / असंतोष", "बड़ी समस्या (understatement)"]},
                        {"instruction": "Write a polite response that respects the indirect message.", "items": ["देखते हैं, शायद अगले महीने।"], "key": ["ज़रूर, जब सुविधा हो बता दीजिएगा।"]},
                        {"instruction": "Record (or recall) three real conversations this week where ठीक है meant three different things; note the cue each time.", "items": ["open task"], "key": ["(open — check: tone, follow-up, silence noted)"]},
                    ],
                },
                "srs": ["देखते हैं", "थोड़ी-सी", "जैसी आपकी मर्ज़ी", "लहज़ा"],
            },
        ],
    },
]

TEST = {
    "title": "Hindi C3 Expert Test",
    "items": [
        {"type": "translate_en", "q": "Expand the headline into a full English sentence: ‘दवाओं के दामों में बढ़ोतरी’", "answer": "Medicine prices have gone up."},
        {"type": "translate_hi", "q": "Rewrite for a formal notice: ‘मीटिंग का टाइम बदल गया है।’", "answer": "बैठक का समय परिवर्तित हो गया है।"},
        {"type": "translate_en", "q": "Decode plainly: ‘कर्मचारियों की संख्या को युक्तिसंगत बनाया गया।’", "answer": "The company laid off staff."},
        {"type": "translate_hi", "q": "Make it ironic with तो…ही (the person is very late): ‘आप देर से आए।’", "answer": "आप तो बिल्कुल समय पर आ ही गए।"},
        {"type": "translate_en", "q": "Give the meaning: ‘ऊँट के मुँह में जीरा’", "answer": "far too little for the need"},
        {"type": "translate_hi", "q": "Turn into standard polite Hindi: ‘अपुन कल नहीं आ पाएगा, मैनेज कर लेना।’", "answer": "मैं कल नहीं आ पाऊँगा; कृपया व्यवस्था सँभाल लीजिए।"},
        {"type": "translate_en", "q": "Translate: ‘रउआ कइसन बानी?’", "answer": "How are you? (respectful, Bhojpuri)"},
        {"type": "translate_hi", "q": "Make gender-neutral: ‘हर छात्र अपनी किताब लाए।’", "answer": "सभी छात्र अपनी किताबें लाएँ।"},
        {"type": "translate_en", "q": "Give the implied meaning: ‘देखते हैं।’ (reply to an invitation)", "answer": "probably not (a polite no)"},
        {"type": "translate_hi", "q": "Say as understatement: ‘पूरा सर्वर क्रैश हो गया है।’", "answer": "सर्वर में थोड़ी-सी दिक़्क़त आ गई है।"},
        {"type": "speak", "q": "Say one deadpan ironic line about a road full of potholes.", "answer": "वाह, क्या सड़क है — हर मोड़ पर तालाब मुफ़्त।"},
        {"type": "speak", "q": "Refuse an invitation twice without saying नहीं.", "answer": "देखते हैं… कल थोड़ा व्यस्त हूँ। कोशिश करूँगा, पक्का नहीं कह सकता।"},
    ],
}

EXTRA = {
    "culture": {
        "text": "Hindi public life runs on three registers at once: the Sanskritic Hindi of notices and ceremonies, the Hindustani of conversation, courts and poetry, and the English-mixed Hindi of offices and screens. Newspapers compress events into verb-less headlines; satirists in the tradition of Harishankar Parsai attack systems with deadpan praise; film songs reach for Braj and Awadhi because those dialects carry centuries of devotional song. An expert reader moves between these layers without judging any of them, hears the irony in a flat ‘ठीक है’, and names people — workers, elders, people with disabilities — in the words they would choose for themselves.",
        "source_url": "https://en.wikipedia.org/wiki/Hindi",
    },
    "reading": {
        "text": "नगर निगम ने इस बार बजट की सुर्खी बड़ी सँभालकर लिखी — ‘जल-आपूर्ति शुल्क का युक्तिसंगत पुनर्निर्धारण’। मोहल्ले के पुराने पत्रकार दीनानाथ जी ने अख़बार मेज़ पर रखा और हँसे, ‘बोले तो पानी महँगा।’ उनकी पोती ने पूछा कि अगर दाम बढ़ाने ही थे तो सीधा क्यों नहीं लिखा। उन्होंने कहा कि सीधा लिखने से सवाल उठते हैं, और घुमाकर लिखने से बस भौंहें। फिर उन्होंने अगले पन्ने पर व्यंग्य-स्तंभ दिखाया, जिसमें लेखक ने निगम को ‘महान जल-संरक्षक’ कहा था, क्योंकि जिस पानी के दाम बढ़े, वह आता ही कब है। पोती ने कहा कि यह तो ऊँट के मुँह में जीरा वाली शिकायत नहीं, सीधे ऊँट ग़ायब वाली बात है। दीनानाथ जी ने चाय की चुस्की ली और कहा, ‘देखते हैं, शायद अगले बजट में ऊँट भी लौट आए।’ पोती समझ गई कि दादा जी को उम्मीद कम है।",
        "original": True,
    },
    "listening": {
        "script": "नमस्कार, यह आज की सुर्खियाँ हैं। राजधानी में भारी बारिश से जनजीवन प्रभावित। बिजली दरों में बढ़ोतरी पर नियामक आयोग का फ़ैसला कल। सूत्रों के मुताबिक दो विधायक पाला बदल सकते हैं। और अंत में — शहर की नई सड़क का उद्घाटन हुआ; स्थानीय लोगों का कहना है कि पहली बारिश में ही उसकी ‘गुणवत्ता’ साफ़ दिखाई दे गई।",
        "voice_tag": "hi-IN",
    },
    "idioms": [
        {"t": "आँखों में धूल झोंकना", "literal": "to throw dust in someone's eyes", "meaning": "to deceive openly"},
        {"t": "ईद का चाँद होना", "literal": "to be the Eid moon", "meaning": "to be rarely seen"},
        {"t": "ऊँची दुकान फीका पकवान", "literal": "tall shop, bland dish", "meaning": "all show, no substance"},
        {"t": "खोदा पहाड़ निकली चुहिया", "literal": "dug a mountain, found a mouse", "meaning": "a huge effort for a trivial result"},
        {"t": "घड़ियाली आँसू", "literal": "crocodile tears", "meaning": "fake sympathy"},
        {"t": "चोर की दाढ़ी में तिनका", "literal": "a straw in the thief's beard", "meaning": "the guilty give themselves away"},
        {"t": "थाली का बैंगन", "literal": "the aubergine on the plate (rolls any way)", "meaning": "a person with no fixed loyalty"},
        {"t": "नाच न जाने आँगन टेढ़ा", "literal": "can't dance, blames the crooked courtyard", "meaning": "a bad workman blames his tools"},
        {"t": "बंदर क्या जाने अदरक का स्वाद", "literal": "what does a monkey know of ginger's taste", "meaning": "the ignorant cannot value quality"},
        {"t": "सौ सुनार की, एक लुहार की", "literal": "a hundred of the goldsmith's, one of the blacksmith's", "meaning": "one decisive blow beats many small ones"},
    ],
    "mistakes": [
        {"wrong": "सूत्रों के मुताबिक फ़ैसला हो गया है, इसलिए अब यह तय है।", "right": "सूत्रों के मुताबिक फ़ैसला हो गया है; आधिकारिक पुष्टि बाकी है।", "why": "Attribution is not confirmation. Repeat the source, not the certainty."},
        {"wrong": "कृपया अपना आसन ग्रहण करें और चाय का रसास्वादन करें। (to a friend at home)", "right": "बैठो, चाय पियो।", "why": "Stacking tatsam words in a casual setting is register clash — comic unless intended."},
        {"wrong": "मोटे अफ़सर ने फ़ाइल दबा दी। (as satire)", "right": "दफ़्तर ने फ़ाइल छह महीने ‘विचाराधीन’ रखी।", "why": "Satire targets systems and power, never a person's body or identity."},
        {"wrong": "वह विकलांग बेचारा पीछे बैठेगा।", "right": "दिव्यांग अतिथि के लिए आगे की पंक्ति में सुगम स्थान है।", "why": "Person-first, role-based, no pity word; accessibility is arranged, not assumed."},
    ],
    "task": {
        "title": "One week of public Hindi",
        "instructions": "For seven days collect one item a day from real Hindi media or conversation: a headline (expand it), a euphemism (decode it), an ironic line (name the marker), a proverb (give image and use), a Hinglish or Bambaiya line (standardise it), a dialect trace (name the variety), and one indirect refusal you heard (write what it really meant). Present the seven items as a two-page ‘field notebook’ with your decoding beside each; then write a 150-word व्यंग्य of your own about any one system you dealt with that week, with no personal attack in it.",
    },
}

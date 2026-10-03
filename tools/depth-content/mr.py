# -*- coding: utf-8 -*-
"""Marathi PHASE 1 depth — extras, third lessons, half-step rungs.

Written with the DSL in `tools/depth_kit.py`; rendered by
`tools/author-depth.py --lang mr`.

House style follows the shipped Marathi course: Devanagari in `t`, the course's
romanisation in `r` — sentence-case, no diacritics, hyphens inside compounds
(`Tumhala kay jhala?`, `rugnalay`, `khokala-sardi`) — and English in `en`, because
the course teaches in English. Unit ids keep the shipped scheme (`mr-a1-u1`,
`mr-a1-l1` …); the half-step rungs use `<rung>-U1`.

Register note: the shipped course addresses one person with तुम्ही and teaches
आहे / आहेत. A1-A2 stay there; B1 adds the future (येईन, जाईल) and the imperative
करा; B2 uses the impersonal and passives of negotiation (ठरवले जाईल); C1-C2 use
the written register of reports and papers (सदर, अन्वये, झाल्यानुसार, असे
निदर्शनास येते). आपण is the inclusive address, तू stays inside the family, and
the labels of the listening transcripts are native throughout.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # tools/ on the path
from depth_kit import D, EXTRA, G, L, T, V, WS, X   # noqa: E402

CODE = "mr"
NAME = "Marathi"
NATIVE = "मराठी"
PHASE = 2
SCRIPT = "Devanagari"
VOICE = "mr-IN"
SKILL = ("Marathi: Devanagari with ळ and the candra vowels, three-way address "
         "(तू / तुम्ही / आपण), three genders and agreement, postpositions, "
         "verb-final order, the -त आहे progressive and Marathi's compound verbs")

EXTRAS = {}
THIRD = {}
HALFSTEPS = {}

EXTRAS["A1"] = EXTRA(
    culture=("Marathi is written in Devanagari, with letters and habits Hindi does not have: ळ, "
             "the retroflex l of फळ (fruit) and शाळा (school); the candra signs ॅ and ॉ that carry "
             "English vowels into बँक and कॉलेज; and no capitals at all, so a sentence opens on the "
             "same letter it would use in the middle. The ळ is the quickest way to hear the "
             "difference: मराठी itself, and every Marathi speaker's name for the language, uses a "
             "sound that a Hindi speaker hears as a plain l."),
    source_url="https://en.wikipedia.org/wiki/Marathi_language",
    reading=("मी मीरा आहे. मी पुण्यात राहते. सकाळी सहा वाजता उठते आणि चहा करते. माझी आई "
             "शिक्षिका आहे आणि वडील दुकान चालवतात. मी रोज सकाळी अभ्यास करते, नंतर कॉलेजला "
             "जाते. संध्याकाळी मैदानावर फिरायला जाते. मला पुस्तके वाचायला आवडतात. रात्री "
             "जेवणानंतर मी दिवसभराची नोंद लिहिते. शनिवारी मी मैत्रिणींना भेटते आणि गप्पा "
             "मारते. रविवारी घरी सगळे एकत्र जेवतात."),
    reading_gloss=("I am Meera. I live in Pune. I get up at six in the morning and make tea. My "
                   "mother is a teacher and my father runs a shop. Every morning I study, then I go "
                   "to college. In the evening I go for a walk on the ground. I like reading "
                   "books. At night, after dinner, I write down my day. On Saturday I meet my "
                   "friends and we chat. On Sunday everyone at home eats together."),
    listening=("मीरा: नमस्कार, तुम्ही कसे आहात?<br>"
               "अर्णव: मी मजेत आहे, धन्यवाद. तुम्ही कशी आहात?<br>"
               "मीरा: मी सुद्धा छान आहे. हा तुमचा मुलगा आहे का?<br>"
               "अर्णव: हो, त्याचे नाव ओम आहे. तो आता शाळेत जातो.<br>"
               "मीरा: छान! माझी मुलगी पण शाळेत आहे."),
    listening_gloss=("Meera: Hello, how are you? Arnav: I am well, thank you. How are you? Meera: I "
                     "am fine too. Is this your son? Arnav: Yes, his name is Om. He goes to school "
                     "now. Meera: Nice! My daughter is at school too."),
    voice_tag=VOICE,
    idioms=[
        ("काय चाललंय?", "what is going on?", "how are things? (greeting a friend)"),
        ("मस्त", "excellent", "great, cool"),
        ("अरेरे", "oh dear", "oh no (mild dismay)"),
        ("गप्पा मारणे", "to hit gossip", "to chat, to pass the time talking"),
        ("पोटभर", "to the stomach", "as much as one wants, to the full"),
        ("थंडी वाजते", "the cold rings", "it is freezing"),
        ("छान", "fine", "nice, lovely"),
        ("चहा घेऊ या", "let us take tea", "let's have a cup of tea"),
        ("काळजी घ्या", "take the worry", "take care"),
        ("भेटू या", "let us meet", "see you (said on leaving)"),
    ],
    mistakes=[
        ("तू कुठे राहतो?", "तू कुठे राहतोस?",
         "तू takes its own ending: राहतोस for a male, राहतेस for a female. राहतो belongs to मी, तो."),
        ("हे माझा भाऊ आहे.", "हा माझा भाऊ आहे.",
         "The demonstrative agrees with the noun: हा भाऊ, ही बहीण, हे पुस्तक."),
        ("मला भूक आहे.", "मला भूक लागली आहे.",
         "Hunger has its own verb in Marathi: भूक लागते. भूक आहे just states that hunger exists."),
    ],
    task_title="Introduce yourself to a Marathi classmate",
    task_instructions=("Write five Marathi sentences: your name, the city you live in, what you do "
                       "in the morning, one thing you like, and one question back to the reader. "
                       "Use आहे / आहात / आहेत correctly, choose तुम्ही as your address, and read "
                       "the five sentences aloud twice."),
)

EXTRAS["A2"] = EXTRA(
    culture=("A Maharashtrian kitchen changes with the ground under it: bhakri of jowar or bajri "
             "with a chutney in the Deccan, rice and coconut along the Konkan coast, peanuts and "
             "dry coconut in Vidarbha. Bhaji mandai mornings, misal for breakfast and ukdiche "
             "modak at Ganesh Chaturthi are the parts everyone knows. Tea, चहा, is the great "
             "leveller — a cutting is sold on every corner, and the invitation चहा घेऊ या closes "
             "more deals than a contract does."),
    source_url="https://en.wikipedia.org/wiki/Maharashtrian_cuisine",
    reading=("आज सकाळी मी भाजी मंडईत गेली. भाजीवालीने टोमॅटो आणि वांगी दाखवली. दर महाग "
             "वाटले, म्हणून मी थोडा भाव केला आणि शेवटी दोन किलो घेतले. मी पाठीमागच्या "
             "दुकानातून गरम मिसळ आणली. शेजारच्या दुकानात चहा मिळाला. घरी येताना मी "
             "नारळ आणि हिरवी मिरची घेतली. संध्याकाळी आईने भाजी केली आणि सगळ्यांनी एकत्र "
             "जेवण केले. हिशोब पाहिला तर पंधरा रुपये वाचले."),
    reading_gloss=("This morning I went to the vegetable market. The vegetable seller showed me "
                   "tomatoes and brinjal. The price seemed high, so I bargained a little and in "
                   "the end took two kilos. From the shop behind I got hot misal. At the next shop "
                   "I found tea. On the way home I bought a coconut and green chillies. In the "
                   "evening my mother cooked the vegetables and we all ate together. When I looked "
                   "at the accounts, fifteen rupees were saved."),
    listening=("स्नेहा: काका, भाजी किती रुपये किलो आहे?<br>"
               "विक्रेता: तीस रुपये किलो, मॅडम. ताजी आहे.<br>"
               "स्नेहा: थोडे कमी करा. पंचवीसला द्या.<br>"
               "विक्रेता: ठीक आहे, दोन किलो घ्या म्हणजे बरोबर होईल.<br>"
               "स्नेहा: चला, द्या. आणि मिरचीचे काय दर आहेत?"),
    listening_gloss=("Sneha: Uncle, how much is the vegetable per kilo? Seller: Thirty rupees a "
                     "kilo, madam. It is fresh. Sneha: Make it a little less. Give it at "
                     "twenty-five. Seller: All right, take two kilos and it works out. Sneha: "
                     "Fine, give it. And what is the price of the chillies?"),
    voice_tag=VOICE,
    idioms=[
        ("भाव करणे", "to do the price", "to bargain"),
        ("भाजी मंडई", "vegetable market", "the morning market where produce is sold"),
        ("किलोभर", "about a kilo", "roughly a kilo, a kilo or so"),
        ("उधारी", "credit", "on account, to be paid later"),
        ("चिल्लर", "small change", "coins, change for a note"),
        ("हिशोब", "account", "the reckoning, the tally of what was spent"),
        ("फुकट", "free", "thrown in, at no cost"),
        ("गर्दी", "crowd", "the crush of people"),
        ("ताजे", "fresh", "fresh, just brought in"),
        ("जेवण करणे", "to do the eating", "to eat a proper meal"),
    ],
    mistakes=[
        ("काल मी मुंबईत गेलो.", "काल मी मुंबईला गेलो.",
         "Going to a city takes -ला; being in it takes -त. मुंबईला गेलो, मुंबईत राहिलो."),
        ("माझ्याजवळ पैसे आहे.", "माझ्याजवळ पैसे आहेत.",
         "पैसे is plural, so it takes आहेत; आहे would make it one single rupee."),
        ("शंभर रुपये लागतो.", "शंभर रुपये लागतात.",
         "रुपये counted as a sum takes a plural verb: रुपये लागतात, रुपये पडतात."),
    ],
    task_title="Shop for vegetables in Marathi",
    task_instructions=("Write a short market dialogue of six lines between a customer and a seller: "
                       "ask the price per kilo, bargain once with कमी करा, settle on two kilos, and "
                       "ask the price of one more thing. Then write down the account in one "
                       "sentence with रुपये लागतात."),
)

EXTRAS["B1"] = EXTRA(
    culture=("The first public Marathi play, Sita Swayamvar by Vishnudas Bhave, was staged at Sangli "
             "in 1843 and grew out of the travelling troupes of the time; by the 1950s the Marathi "
             "stage had musicals, farces and history plays, and after it the experimental theatre of "
             "Vijay Tendulkar and Satish Alekar. What marks it is that the rehearsal is a public "
             "institution: the नाट्यसंमेलन and the drama school culture around Pune and Mumbai keep "
             "an audience for a play that runs for years."),
    source_url="https://en.wikipedia.org/wiki/Marathi_theatre",
    reading=("गेल्या आठवड्यात आमच्या कार्यालयात महत्त्वाची बैठक होती. मी अहवाल तयार केला "
             "होता, पण सादरीकरणाची जबाबदारी माझ्या सहकाऱ्यावर होती. तिने आकडेवारी स्पष्ट "
             "मांडली आणि प्रश्नांना थेट उत्तर दिले. व्यवस्थापकांनी दोन मुद्द्यांवर आक्षेप "
             "घेतला — वेळ आणि खर्च. आम्ही दोन्ही आकड्यांची फेरतपासणी करून पुढील बैठकीत "
             "उत्तर देण्याचे ठरवले. बैठकीअंती सर्वांनी एकमताने निर्णय घेतला: काम दोन "
             "टप्प्यांत करायचे. वेळेवर तयारी आणि स्पष्ट उत्तर यांनीच विश्वास वाढतो, हे "
             "मला या बैठकीत शिकायला मिळाले."),
    reading_gloss=("Last week there was an important meeting at our office. I had prepared the "
                   "report, but the presentation was my colleague's responsibility. She set out the "
                   "figures clearly and answered the questions directly. The managers raised "
                   "objections on two points — time and cost. We decided to recheck both figures "
                   "and answer at the next meeting. At the end of the meeting everyone agreed on "
                   "one decision: the work would be done in two stages. In that meeting I learnt "
                   "that it is timely preparation and clear answers that build trust."),
    listening=("व्यवस्थापक: अहवाल उद्या संध्याकाळपर्यंत मिळेल का?<br>"
               "नवागंतुक: हो, पण दोन आकडे अजून तपासायचे आहेत.<br>"
               "व्यवस्थापक: ठीक, तपासून कळवा. आणि मुदतीचा उल्लेख नक्की करा.<br>"
               "नवागंतुक: नक्की. उद्या सकाळीच अहवाल पाठवतो.<br>"
               "व्यवस्थापक: कृपया ईमेलमध्ये वेळ आणि दिनांक दोन्ही लिहा."),
    listening_gloss=("Manager: Will the report reach me by tomorrow evening? Newcomer: Yes, but two "
                     "figures still have to be checked. Manager: All right, check them and let me "
                     "know. And do mention the deadline. Newcomer: Certainly. I will send the report "
                     "tomorrow morning itself. Manager: Please write both the time and the date in "
                     "the e-mail."),
    voice_tag=VOICE,
    idioms=[
        ("हातभार लावणे", "to add the weight of a hand", "to contribute to something"),
        ("डोळे दिपणे", "the eyes to dazzle", "to be dazzled, to be overwhelmed by what one sees"),
        ("डोकं खाणे", "to eat the head", "to pester, to nag somebody"),
        ("अंगावर काटा येणे", "a thorn to come on the body", "to get goosebumps, to be terrified"),
        ("गुडघे टेकणे", "to touch the knees", "to give in, to surrender"),
        ("नाकं मुरडणे", "to twist the noses", "to turn up one's nose, to sulk"),
        ("तोंडावर बोलणे", "to speak on the face", "to say it to somebody's face"),
        ("खांद्यावर घेणे", "to take it on the shoulder", "to take on a responsibility"),
        ("घाम गाळणे", "to pour out sweat", "to toil over something"),
        ("कानावर हात ठेवणे", "to put a hand on the ear", "to be stunned, to hear something unbelievable"),
    ],
    mistakes=[
        ("मी उद्या येतो.", "मी उद्या येईन.",
         "A promise about tomorrow takes the future: येईन, जाईल, कळवीन. येतो describes a habit."),
        ("कृपया अहवाल पाठव.", "कृपया अहवाल पाठवा.",
         "कृपया goes with the तुम्ही imperative in -ा: पाठवा, बसा, सांगा. पाठव belongs to तू."),
        ("माझं सहकारी आला.", "माझा सहकारी आला.",
         "The possessive agrees with the noun it owns: माझा सहकारी, माझी टीम, माझे काम."),
    ],
    task_title="Write a short office note in Marathi",
    task_instructions=("Write five Marathi sentences for a colleague: what has happened, who is "
                       "doing what by when, one polite request with कृपया … करा, one promise in the "
                       "future tense (कळवीन, पाठवीन), and one closing line. Keep the register "
                       "polite and the verbs in the तुम्ही form."),
)

EXTRAS["B2"] = EXTRA(
    culture=("Marathi is the official language of Maharashtra and one of India's 22 scheduled "
             "languages, with roughly 83 million speakers. The state was redrawn on language lines "
             "in 1960, and the Marathi-speaking belt runs past its border — Belagavi and the Goa "
             "coast included — which is why a Marathi speaker may be in Karnataka or Goa as "
             "naturally as in Pune. In the courts, the collector's office and the municipal "
             "corporation, Marathi and English share the page, and the negotiating vocabulary is "
             "mostly Marathi words doing English work."),
    source_url="https://en.wikipedia.org/wiki/Marathi_people",
    reading=("दोन्ही बाजूंनी कराराच्या अटी वाचल्या. पुरवठादाराने मुदत तीन महिन्यांची "
             "मागितली, पण आमच्या बाजूने खर्च वाढणार होता. बोलणी दोन तास चालली. शेवटी एक "
             "तडजोड झाली: पहिला टप्पा दोन महिन्यांत, दुसरा टप्पा चार महिन्यांत. दोन्ही "
             "बाजूंनी अटी लिखित स्वरूपात मान्य केल्या आणि करारावर स्वाक्षरी केली. कोंडी "
             "फुटली कारण दोन्ही बाजूंनी अंतिम मुदत वाढवायला तयारी दाखवली. पुढील बैठकीत "
             "दररोजच्या पुरवठ्याचा आढावा घ्यायचे ठरले."),
    reading_gloss=("Both sides read the terms of the contract. The supplier asked for a three-month "
                   "deadline, but on our side the cost was going to rise. The talks went on for two "
                   "hours. In the end there was a compromise: the first stage in two months, the "
                   "second in four. Both sides accepted the conditions in writing and signed the "
                   "contract. The deadlock broke because both sides showed readiness to extend the "
                   "final deadline. At the next meeting it was decided to review the daily supply."),
    listening=("वकील: मुदतीवर दोन्ही बाजूंनी ठरले आहे का?<br>"
               "सल्लागार: ठरले आहे, पण अट एक आहे — पहिला टप्पा दोन महिन्यांत.<br>"
               "वकील: ती अट कागदावर लिहिली पाहिजे, अन्यथा पुढे वाद होईल.<br>"
               "सल्लागार: तयार आहे. मी आज सायंकाळी मसुदा पाठवतो.<br>"
               "वकील: चांगले. मसुद्यात दोन्ही बाजूंची स्वाक्षरी आणि दिनांक ठेवा."),
    listening_gloss=("Lawyer: Have both sides settled on the deadline? Advisor: It is settled, but "
                     "there is one condition — the first stage within two months. Lawyer: That "
                     "condition must be written on paper, otherwise there will be a dispute later. "
                     "Advisor: Ready. I will send the draft this evening. Lawyer: Good. Put both "
                     "signatures and the date in the draft."),
    voice_tag=VOICE,
    idioms=[
        ("तडजोड", "a mutual giving", "compromise, settlement"),
        ("गुंता सोडवणे", "to untie the knot", "to resolve a tangle or a dispute"),
        ("कोंडी फुटणे", "the blockade to break", "a deadlock to give way"),
        ("अट पाळणे", "to keep the condition", "to honour a term"),
        ("बोलणी करणे", "to do the talking", "to hold negotiations"),
        ("स्वाक्षरी करणे", "to do the signature", "to sign a document"),
        ("अंतिम मुदत", "the last limit", "the final deadline"),
        ("जमीन तयार करणे", "to prepare the ground", "to pave the way for something"),
        ("दुहेरी फायदा", "double profit", "a win-win arrangement"),
        ("तह करणे", "to make a pact", "to strike a settlement"),
    ],
    mistakes=[
        ("आम्ही अट मान्य केला.", "आम्ही अट मान्य केली.",
         "अट is feminine, so the verb follows it: अट मान्य केली, अटी मान्य केल्या."),
        ("वाटाघाटी सुरू आहे.", "वाटाघाटी सुरू आहेत.",
         "वाटाघाटी is plural: वाटाघाटी सुरू आहेत, वाटाघाटी तडकल्या."),
        ("मी हा करार मान्य आहे.", "मी हा करार मान्य करतो.",
         "मान्य आहे describes the contract; accepting it needs the verb मान्य करतो / करते."),
    ],
    task_title="Draft the minutes of a negotiation",
    task_instructions=("Write five Marathi sentences of minutes: who met, what each side asked "
                       "for, the तडजोड that was reached, the अट that was written down, and the "
                       "signature line with a date. Use the impersonal once (ठरवले गेले) and keep "
                       "the verbs in the polite form."),
)

EXTRAS["C1"] = EXTRA(
    culture=("Marathi literature begins with Jnanadeva's ज्ञानेश्वरी (around 1290), a commentary on "
             "the Bhagavad Gita that put philosophy into the spoken Marathi of its day; Tukaram's "
             "abhangs and Ramdas's couplets followed, and the nineteenth century turned the same "
             "language to newspapers and the essay. Modern Marathi has a strong fictional line — "
             "the village novel, the Bombay novel, the short story — and an academic prose that "
             "keeps the Sanskrit-derived vocabulary on one side and the spoken verb on the other."),
    source_url="https://en.wikipedia.org/wiki/Marathi_literature",
    reading=("सदर अभ्यासात दोन नगरांची तुलना करण्यात आली. पूर्वीच्या संशोधनात प्रामुख्याने "
             "महानगरांचा विचार झाला होता, तर लहान शहरांविषयीची माहिती तुरळक आहे. आकडेवारी "
             "दाखवते की दोन्ही ठिकाणी रोजगाराची स्थिती वेगळी आहे, तथापि जमिनीच्या वापराचे "
             "नमुने सारखेच आहेत. उपलब्ध प्रमाण मर्यादित असल्याने निष्कर्ष सावधपणे मांडले "
             "आहेत. अभ्यासात दोन मर्यादा स्पष्टपणे नोंदवल्या आहेत: कालावधी लहान आहे आणि "
             "दुसऱ्या स्रोतांची पडताळणी झालेली नाही. पुढील संशोधनात दहा वर्षांची आकडेवारी "
             "घ्यावी, असे अभ्यासात सुचवण्यात आले आहे."),
    reading_gloss=("In the present study two cities were compared. Earlier research considered "
                   "mainly the metropolises, while information about smaller towns is sparse. The "
                   "data show that employment is different in the two places, yet the patterns of "
                   "land use are similar. Because the available evidence is limited, the "
                   "conclusions have been stated cautiously. Two limits are clearly recorded in "
                   "the study: the period is short and the second source has not been verified. "
                   "The study suggests that ten years of data should be used in further research."),
    listening=("संपादक: निष्कर्ष थोडा विस्तारलेला वाटतो.<br>"
               "लेखक: कोणता भाग आपल्याला जास्त वाटतो?<br>"
               "संपादक: राज्यभर लागू होतो, असे जिथे म्हटले आहे तिथे. ते दोन नगरांपुरते "
               "ठेवा.<br>"
               "लेखक: ठीक. मग सहसंबंधापर्यंत मर्यादा ठेवतो आणि कारण-परिणाम पुढील "
               "संशोधनासाठी सोडतो.<br>"
               "संपादक: आणि शेवटच्या परिच्छेदात उरलेला प्रश्न स्पष्ट लिहा."),
    listening_gloss=("Editor: The conclusion seems a little stretched. Writer: Which part reads "
                     "too wide to you? Editor: Where it says it applies across the whole state. "
                     "Keep it to the two cities. Writer: All right. Then I will limit it to a "
                     "correlation and leave cause and effect to further research. Editor: And write "
                     "the question that remains clearly in the last paragraph."),
    voice_tag=VOICE,
    idioms=[
        ("निदर्शनास येते", "it comes to view", "it is observed, we may note"),
        ("अन्वये", "in the following of", "in accordance with, in the light of"),
        ("सदर", "the present, the said", "the above-mentioned (documents, studies)"),
        ("तथापि", "even so", "nevertheless, however"),
        ("उपरोक्त", "spoken above", "the aforementioned"),
        ("लक्षात घेणे आवश्यक", "to take into mind is necessary", "it must be kept in view"),
        ("प्रमाणांचा आधार", "the support of proofs", "the evidential basis"),
        ("निष्कर्ष काढणे", "to draw the conclusion", "to arrive at a finding"),
        ("सावधपणे मांडणे", "to state with caution", "to put forward with due reservation"),
        ("पडताळणी करणे", "to make the verification", "to cross-check a source"),
    ],
    mistakes=[
        ("आकडेवारी दाखवतो की खर्च वाढला.", "आकडेवारी दाखवते की खर्च वाढला.",
         "आकडेवारी is feminine: दाखवते, सुचवते, दर्शवते."),
        ("निष्कर्ष स्पष्ट आहे.", "निष्कर्ष स्पष्ट आहेत.",
         "Several findings are plural: निष्कर्ष आहेत. एकच निष्कर्ष असेल तर आहे."),
        ("प्रमाण कमी आहेत.", "प्रमाण कमी आहे.",
         "प्रमाण is singular and neuter: प्रमाण आहे, पुरावे आहेत."),
    ],
    task_title="Write one paragraph of academic Marathi",
    task_instructions=("Write six Marathi sentences: the question, the method, one finding with "
                       "आकडेवारी दाखवते की …, one limitation, a conclusion that keeps to what the "
                       "data support, and a closing line that names the question still open. Use "
                       "सदर, तथापि and पडताळणी करणे once each."),
)

EXTRAS["C2"] = EXTRA(
    culture=("Marathi keeps two vocabularies on one shelf. The spoken layer — कर, दे, बघ, सांग — "
             "runs the street, the play and the friendly e-mail; a Sanskrit-derived layer — "
             "करणे, प्रदान करणे, अवलोकन, प्रस्ताव — runs the statute, the editorial and the "
             "examination answer. शुद्धलेखन, the standard orthography, decides where a word doubles "
             "its consonant or drops a vowel, and it is the layer a reader notices first: a "
             "misplaced letter in a formal word reads as a foreigner, while the same slip in a "
             "spoken word passes as dialect."),
    source_url="https://en.wikipedia.org/wiki/Maharashtra",
    reading=("मोठ्या शहरांबद्दल बोलताना आपण एक गोष्ट विसरतो: शहर आकड्यांनी वाढत नाही, "
             "माणसांनी वाढते. आकडेवारी वाढ दाखवते, पण त्या आकड्यांमागचा घाम दाखवत नाही. "
             "कागदावर सर्व काही सुरळीत दिसते — रस्ते, नळ, वीज; प्रत्यक्षात रांगा "
             "लांब असतात. हे लिहिणं म्हणजे शहरावर टीका करणं नव्हे, तर त्याची खरी "
             "चित्रं दाखवणं. जिथे विकास दिसतो तिथे अनेकदा एखादी गोष्ट मागे राहते. ती "
             "गोष्ट नावाने सांगितली तरच चर्चा पुढे जाते."),
    reading_gloss=("When we talk about big cities we forget one thing: a city does not grow by "
                   "figures, it grows by people. The data show growth, but they do not show the "
                   "sweat behind those figures. On paper everything looks smooth — roads, taps, "
                   "electricity; in practice the queues are long. Writing this is not criticism of "
                   "the city but showing its true picture. Where development is visible, something "
                   "is often left behind. Only when that something is named does the discussion "
                   "move forward."),
    listening=("तज्ज्ञ: या अहवालातील भाषा आता कागदी वाटते.<br>"
               "मध्यस्थ: म्हणजे शब्द वजनदार आहेत, पण वाचणारा थकतो?<br>"
               "तज्ज्ञ: नेमके तेच. करणे आणि प्रदान करणे नेहमी लागत नाही; कधी साधा "
               "कर पुरतो.<br>"
               "मध्यस्थ: मग दोन परिच्छेद साध्या भाषेत लिहितो आणि उर्वरित औपचारिक "
               "ठेवतो.<br>"
               "तज्ज्ञ: ते चांगले. उपरोध असला तर तो शेवटच्या वाक्यात ठेवा, मधे नको."),
    listening_gloss=("Specialist: The language in this report now reads papery. Mediator: You mean "
                     "the words are weighty, but the reader tires? Specialist: Exactly that. "
                     "करणे and प्रदान करणे are not always needed; sometimes the plain कर is enough. "
                     "Mediator: Then I will write two paragraphs in simple language and keep the "
                     "rest formal. Specialist: That is better. If there is irony, keep it for the "
                     "last sentence, not in the middle."),
    voice_tag=VOICE,
    idioms=[
        ("शब्दशः", "word by word", "literally, verbatim"),
        ("थोडक्यात", "in the short", "in short, to put it briefly"),
        ("अर्थाची छटा", "the shade of meaning", "a nuance of meaning"),
        ("उपरोध", "the under-throw", "irony, a meaning turned under the words"),
        ("वक्रोक्ती", "crooked speech", "oblique speech, saying the opposite to mean it"),
        ("भाषेचा खेळ", "the play of language", "wordplay"),
        ("रूढ अर्थ", "the settled meaning", "the conventional sense of a word"),
        ("मर्मग्राही", "taking the pith", "trenchant, striking at the point"),
        ("चपखल शब्द", "a fitting word", "the mot juste, the word that fits the slot"),
        ("दुहेरी अर्थ", "double meaning", "an ambiguity that carries two senses"),
    ],
    mistakes=[
        ("सर आला.", "सर आले.",
         "Marathi marks respect with the plural: सर आले, ते बोलले, मॅडम म्हणाल्या."),
        ("हे सर्व मुद्दे महत्त्वाचे आहे.", "हे सर्व मुद्दे महत्त्वाचे आहेत.",
         "मुद्दे is plural, so it takes आहेत."),
        ("सर म्हणाले की तो उद्या येईल.", "सर म्हणाले की ते उद्या येतील.",
         "Respect carries into reported speech: ते येतील stays plural even when it is one person."),
    ],
    task_title="Move a paragraph into the formal register",
    task_instructions=("Take five plain Marathi sentences about your work and rewrite them in the "
                       "written register: करणे forms instead of कर, सदर and प्रस्तुत where they fit, "
                       "one शब्दशः quotation, one उपरोध at the end, and the honorific plural kept "
                       "wherever a senior is mentioned."),
)

THIRD["A1"] = [
    ("mr-a1-u1", "mr-a1-l7", L("ओळख: नाव, गाव आणि काम",
        "An introduction is four slots — name, town, work, and a question back. Marathi puts the "
        "verb at the end and marks the town with -त when you live there (पुण्यात राहतो/राहते). "
        "माझे नाव … आहे is the neutral opencr; मी … आहे states a person or a profession.",
        [V("नाव", "naav", "name", "noun"),
         V("गाव", "gaav", "village, town", "noun"),
         V("काम", "kaam", "work", "noun"),
         V("राहणे", "raahne", "to live, to stay", "verb"),
         V("ओळख", "olakh", "acquaintance, recognition", "noun")],
        G("Giving your name",
          "माझे नाव … आहे · मी पुण्यात राहतो · तुमचे नाव काय?",
          "माझे नाव is neuter, so it takes आहे; a place you live in takes the locative -त "
          "(पुण्यात, नागपुरात), and a place you come from takes -चा/-ची (नागपूरचा, पुणेकर). The "
          "question back is तुमचे नाव काय? with तुम्ही.",
          [X("माझे नाव अर्णव आहे.", "Maze naav Arnav ahe.", "My name is Arnav."),
           X("मी पुण्यात राहतो.", "Mi Punyat raahto.", "I live in Pune."),
           X("तुमचे नाव काय आहे?", "Tumche naav kay ahe?", "What is your name?")],
          [("माझं नाव आहे अर्णव.", "माझे नाव अर्णव आहे.", "The name comes before the verb."),
           ("मी पुणे राहतो.", "मी पुण्यात राहतो.", "Living there takes -त: पुण्यात.")]),
        [D("मीरा", "तुमचे नाव काय आहे?", "Tumche naav kay ahe?", "What is your name?"),
         D("अर्णव", "माझे नाव अर्णव आहे. मी नागपूरचा आहे.", "Maze naav Arnav ahe. Mi Nagpurcha ahe.", "My name is Arnav. I am from Nagpur."),
         D("मीरा", "मी पुण्यात राहते. तुम्ही काय करता?", "Mi Punyat raahte. Tumhi kay karta?", "I live in Pune. What do you do?"),
         D("अर्णव", "मी शाळेत शिकवतो.", "Mi shalet shikavto.", "I teach in a school.")],
        WS("Introduction worksheet", [
            T("Introduce yourself.", ["my name is Meera", "I live in Pune"],
              ["माझे नाव मीरा आहे", "मी पुण्यात राहते"]),
            T("Ask the question back.", ["what is your name?", "what do you do?"],
              ["तुमचे नाव काय आहे?", "तुम्ही काय करता?"]),
        ]))),
    ("mr-a1-u2", "mr-a1-l8", L("दिवस आणि तारखा",
        "A day of the week takes -ई to mean on that day: सोमवारी, शुक्रवारी. A date is read day "
        "and month in that order (पंधरा मे), and आज, उद्या and काल stand beside the verb with no "
        "postposition at all.",
        [V("आठवडा", "aathvada", "week", "noun"),
         V("तारीख", "taarikh", "date", "noun"),
         V("महिना", "mahina", "month", "noun"),
         V("आज", "aaj", "today", "adverb"),
         V("उद्या", "udya", "tomorrow", "adverb")],
        G("On Monday, on the fifteenth",
          "सोमवारी बैठक आहे · पंधरा मे · उद्या शाळा बंद आहे",
          "The -वार days add -ई for on that day: सोमवारी, मंगळवारी, शुक्रवारी. A date puts the day "
          "before the month and takes no postposition: पंधरा मे, एक जानेवारी. आज, उद्या, काल and "
          "परवा never take -ला.",
          [X("सोमवारी बैठक आहे.", "Somvari baithak ahe.", "The meeting is on Monday."),
           X("माझा वाढदिवस पंधरा मे आहे.", "Majha vaadhdivas pandhra May ahe.", "My birthday is on the fifteenth of May."),
           X("उद्या शाळा बंद आहे.", "Udya shala band ahe.", "Tomorrow the school is closed.")],
          [("सोमवार बैठक आहे.", "सोमवारी बैठक आहे.", "-वार takes -ई for on that day."),
           ("मी उद्याला जाईन.", "मी उद्या जाईन.", "आज and उद्या take no postposition.")]),
        [D("अर्णव", "उद्या तुमची बैठक आहे का?", "Udya tumchi baithak ahe ka?", "Is your meeting tomorrow?"),
         D("मीरा", "हो, सोमवारी सकाळी दहा वाजता.", "Ho, somvari sakali daha vajta.", "Yes, on Monday at ten in the morning."),
         D("अर्णव", "कालची बैठक पुढे गेली का?", "Kaalchi baithak pudhe geli ka?", "Did yesterday's meeting get postponed?"),
         D("मीरा", "हो, गुरुवारपर्यंत पुढे ढकलली.", "Ho, guruvar-paryant pudhe dhakalli.", "Yes, it was pushed to Thursday.")],
        WS("Date worksheet", [
            T("Say when.", ["on Monday", "on the fifteenth of May"],
              ["सोमवारी", "पंधरा मे"]),
            T("Ask about it.", ["is the meeting tomorrow?", "when is your birthday?"],
              ["उद्या बैठक आहे का?", "तुमचा वाढदिवस कधी आहे?"]),
        ]))),
    ("mr-a1-u3", "mr-a1-l9", L("कपडे आणि रंग",
        "A colour copies the noun it describes: निळा शर्ट, निळी साडी, निळे स्वेटर. Colours in -ा "
        "inflect like that; लाल, गुलाबी and केशरी never change. घालणे is the verb for wearing.",
        [V("शर्ट", "shirt", "shirt", "noun"),
         V("साडी", "sadi", "sari", "noun"),
         V("स्वेटर", "sweater", "sweater", "noun"),
         V("रंग", "rang", "colour", "noun"),
         V("घालणे", "ghaalne", "to wear, to put on", "verb")],
        G("Agreement of colours",
          "निळा शर्ट · निळी साडी · निळे स्वेटर · लाल टोपी",
          "Marathi has three genders, and a colour adjective copies the gender of its noun: "
          "masculine -ा, feminine -ी, neuter -े. Colours borrowed as they are — लाल, गुलाबी, "
          "केशरी — stay the same with every noun.",
          [X("मला निळा शर्ट आवडतो.", "Mala nila shirt aavdto.", "I like the blue shirt."),
           X("ती हिरवी साडी घालते.", "Ti hirvi sadi ghalte.", "She wears a green sari."),
           X("हे लाल स्वेटर आहे.", "He laal sweater ahe.", "This is a red sweater.")],
          [("ती हिरवा साडी घालते.", "ती हिरवी साडी घालते.", "साडी is feminine: हिरवी."),
           ("मी काळा टोपी घालतो.", "मी काळी टोपी घालतो.", "टोपी is feminine: काळी टोपी.")]),
        [D("मीरा", "ही साडी कशी वाटते?", "Hi sadi kashi vaatte?", "How does this sari look?"),
         D("अर्णव", "छान! पण निळी जास्त शोभेल.", "Chaan! Pan nili jaast shobhel.", "Lovely! But blue will suit you more."),
         D("मीरा", "माझ्याकडे निळी आहे. तुमचा शर्ट कोणता?", "Majhyakade nili ahe. Tumcha shirt konta?", "I have a blue one. Which is your shirt?"),
         D("अर्णव", "हा पांढरा. उन्हात पांढरा चांगला वाटतो.", "Ha pandhra. Unhaat pandhra chaangla vaatto.", "This white one. White looks good in the sun.")],
        WS("Colour worksheet", [
            T("Agree the colour.", ["a blue shirt", "a green sari"],
              ["निळा शर्ट", "हिरवी साडी"]),
            T("Say what is worn.", ["I wear a white shirt.", "she wears a red sari."],
              ["मी पांढरा शर्ट घालतो.", "ती लाल साडी घालते."]),
        ]))),
]

THIRD["A2"] = [
    ("mr-a2-u1", "mr-a2-l7", L("प्रवास: तिकीट आणि फलक",
        "At a Marathi station the destination comes before the ticket and takes -चे: पुण्याचे "
        "तिकीट. The timetable runs on the simple present — गाडी सुटते, पोहोचते — and बदल करणे is "
        "the verb for changing trains.",
        [V("तिकीट", "tikit", "ticket", "noun"),
         V("फलक", "phalak", "platform, board", "noun"),
         V("गाडी", "gaadi", "train, vehicle", "noun"),
         V("उतरणे", "utarne", "to get down, to alight", "verb"),
         V("पोहोचणे", "pohochne", "to arrive, to reach", "verb")],
        G("Ticket, platform, change",
          "पुण्याचे दोन तिकीट द्या · गाडी किती वाजता सुटते? · कुठे बदल करायचा?",
          "The destination takes -चे/-ची before the ticket: पुण्याचे तिकीट, मुंबईची गाडी. A "
          "timetable states facts, so it uses the simple present: सुटते, पोहोचते, येते. बदल करणे "
          "is the standard phrase for a change of trains.",
          [X("पुण्याचे दोन तिकीट द्या.", "Punyache don tikit dya.", "Give me two tickets to Pune."),
           X("गाडी दहा वाजता सुटते.", "Gaadi daha vajta sutte.", "The train leaves at ten."),
           X("साताऱ्याला उतरायचे आहे का?", "Saataryala utrayche ahe ka?", "Do I get off at Satara?")],
          [("पुणे दोन तिकीट द्या.", "पुण्याचे दोन तिकीट द्या.", "The destination takes -चे: पुण्याचे तिकीट."),
           ("गाडी दहा वाजता सुटतील.", "गाडी दहा वाजता सुटते.", "गाडी is singular feminine: सुटते.")]),
        [D("मीरा", "मुंबईचे दोन तिकीट द्या.", "Mumbaiche don tikit dya.", "Give me two tickets to Mumbai."),
         D("विक्रेता", "मुंबईची गाडी फलक तीनवर येते.", "Mumbaichi gaadi phalak teen-var yete.", "The Mumbai train comes on platform three."),
         D("मीरा", "कुठे बदल करायचा?", "Kuthe badal karaycha?", "Where do I change?"),
         D("विक्रेता", "कल्याणला बदल करा, मग सरळ जाते.", "Kalyan-la badal kara, mag saral jate.", "Change at Kalyan, then it goes straight.")],
        WS("Travel worksheet", [
            T("Buy the ticket.", ["two tickets to Mumbai", "when does the train leave?"],
              ["मुंबईचे दोन तिकीट", "गाडी किती वाजता सुटते?"]),
            T("Ask about the journey.", ["where do I change?", "do I get off at Pune?"],
              ["कुठे बदल करायचा?", "पुण्याला उतरायचे आहे का?"]),
        ]))),
    ("mr-a2-u2", "mr-a2-l8", L("पुस्तकालय आणि अभ्यास",
        "A library runs on three words: सदस्यत्व, उधार and मुदत. The book borrowed stays the "
        "object of घेणे and is given back with परत करणे, and the deadline asks for the infinitive "
        "with -ायची: परत करायची मुदत.",
        [V("पुस्तकालय", "pustakalay", "library", "noun"),
         V("सदस्यत्व", "sadasyatva", "membership", "noun"),
         V("मुदत", "mudat", "deadline, period", "noun"),
         V("परत करणे", "parat karne", "to return, to give back", "verb"),
         V("शोधणे", "shodhne", "to search, to look up", "verb")],
        G("Borrowing and returning",
          "पुस्तक घेऊन जाऊ शकतो · परत करायची मुदत · शोधून काढणे",
          "शकतो / शकते says what one can do and needs no आहे after it. The infinitive with -ायची "
          "names what has to be done, so परत करायची मुदत is the date by which the book must come "
          "back. शोधून काढणे means to find something after looking for it.",
          [X("मी दोन पुस्तके घेऊन जाऊ शकतो का?", "Mi don pustake gheun jaau shakto ka?", "May I take two books home?"),
           X("परत करायची मुदत चौदा दिवस आहे.", "Parat karaychi mudat chauda divas ahe.", "The deadline to return is fourteen days."),
           X("हे पुस्तक शोधून काढा.", "He pustak shodhun kaadha.", "Find me this book.")],
          [("मी पुस्तकालयात जाऊ शकतो आहे.", "मी पुस्तकालयात जाऊ शकतो.", "शकतो already means can; आहे has no place after it."),
           ("मुदत चौदा दिवस आहेत.", "मुदत चौदा दिवस आहे.", "मुदत is singular feminine: आहे.")]),
        [D("विद्यार्थी", "नवीन सदस्यत्व कसे घ्यायचे?", "Navin sadasyatva kase ghyayche?", "How does one take a new membership?"),
         D("ग्रंथपाल", "ओळखपत्र आणि दोन फोटो आणा.", "Olakhpatra aani don photo aana.", "Bring an identity card and two photographs."),
         D("विद्यार्थी", "एकदा किती पुस्तके मिळतात?", "Ekda kiti pustake miltaat?", "How many books does one get at a time?"),
         D("ग्रंथपाल", "तीन. परत करायची मुदत चौदा दिवस आहे.", "Teen. Parat karaychi mudat chauda divas ahe.", "Three. The deadline to return is fourteen days.")],
        WS("Library worksheet", [
            T("Ask at the desk.", ["how do I take a membership?", "how many books at a time?"],
              ["सदस्यत्व कसे घ्यायचे?", "एकदा किती पुस्तके मिळतात?"]),
            T("Give the terms.", ["return within fourteen days", "two books at a time"],
              ["चौदा दिवसांत परत करा", "एकदा दोन पुस्तके"]),
        ]))),
    ("mr-a2-u3", "mr-a2-l9", L("सण आणि आमंत्रण",
        "An invitation is a polite imperative with an occasion attached: दिवाळीला आमच्या घरी "
        "या. With तुम्ही the imperative ends in -ा (या, बसा, घ्या), and the festival as a date "
        "takes -ला.",
        [V("सण", "san", "festival", "noun"),
         V("आमंत्रण", "aamantran", "invitation", "noun"),
         V("दिवाळी", "divali", "Diwali", "noun"),
         V("फराळ", "faral", "festival sweets and snacks", "noun"),
         V("भेट देणे", "bhet dene", "to visit, to pay a call", "verb")],
        G("Inviting somebody",
          "दिवाळीला आमच्या घरी या · फराळाला बसा · येणार का?",
          "The occasion takes -ला: दिवाळीला, गणपतीला, फराळाला. With तुम्ही the imperative ends "
          "in -ा, and an invitation is often framed as a question with -णार का? (येणार का?) so "
          "that the guest can refuse without refusing.",
          [X("दिवाळीला आमच्या घरी या.", "Divali-la aamchya ghari ya.", "Come to our house for Diwali."),
           X("फराळाला बसा.", "Faraal-la basaa.", "Sit down to the faral."),
           X("तुम्ही येणार का?", "Tumhi yenaar ka?", "Are you coming?")],
          [("आमच्या घरी ये.", "आमच्या घरी या.", "With तुम्ही the imperative ends in -ा; ये belongs to तू."),
           ("दिवाळीत आमच्या घरी या.", "दिवाळीला आमच्या घरी या.", "A festival as an occasion takes -ला.")]),
        [D("मीरा", "दिवाळीला तुम्ही येणार का?", "Divali-la tumhi yenaar ka?", "Are you coming for Diwali?"),
         D("स्नेहा", "हो, नक्की येईन. कधी?", "Ho, nakki yein. Kadhi?", "Yes, I will certainly come. When?"),
         D("मीरा", "लक्ष्मीपूजनाच्या दिवशी संध्याकाळी.", "Lakshmi-pujnchya divshi sandhyakali.", "On the evening of Lakshmi Puja."),
         D("स्नेहा", "मी फराळ घेऊन येईन.", "Mi faraal gheun yein.", "I will bring the faral.")],
        WS("Invitation worksheet", [
            T("Invite somebody.", ["come to our house for Diwali", "sit down to the faral"],
              ["दिवाळीला आमच्या घरी या", "फराळाला बसा"]),
            T("Answer an invitation.", ["yes, I will come", "what time?"],
              ["हो, मी येईन", "किती वाजता?"]),
        ]))),
]

THIRD["B1"] = [
    ("mr-b1-u1", "mr-b1-l7", L("बैठकीत मत मांडणे",
        "A meeting runs on मत मांडणे, सहमत होणे and आक्षेप घेणे. Marathi softens disagreement "
        "before it states it: मला वाटते की …, पण …. वाटणे takes the dative मला and stays neuter, "
        "and an objection is phrased as मला आक्षेप आहे, which is politer than a flat refusal. A "
        "counter-proposal opens with तरी or पण.",
        [V("मत", "mat", "opinion", "noun"),
         V("सहमत", "sahmat", "in agreement", "adjective"),
         V("आक्षेप", "aakshep", "objection", "noun"),
         V("मांडणे", "maandne", "to put forward, to state", "verb"),
         V("मुद्दा", "mudda", "point, item", "noun")],
        G("Putting an opinion",
          "मला वाटते की … · मी सहमत आहे · मला आक्षेप आहे",
          "मला वाटते is the standard softener and takes a की clause. सहमत आहे states agreement "
          "and stands after the thing agreed with (पहिल्या मुद्द्याशी सहमत आहे). An objection is "
          "मला आक्षेप आहे, and a proposal uses the -ावे form (करावे, ठेवावे).",
          [X("मला वाटते की ही योजना रद्द करावी.", "Mala vaatte ki hi yojna radd karavi.", "I think this plan should be dropped."),
           X("मी पहिल्या मुद्द्याशी सहमत आहे.", "Mi pahilya muddyashi sahmat ahe.", "I agree with the first point."),
           X("मला दुसऱ्या टप्प्यावर आक्षेप आहे.", "Mala dusrya tappyavar aakshep ahe.", "I have an objection to the second stage.")],
          [("मला वाटतो की हे बरोबर आहे.", "मला वाटते की हे बरोबर आहे.", "वाटणे stays neuter with मला: वाटते."),
           ("मी सहमत आहे तुमच्या मताशी.", "मी तुमच्या मताशी सहमत आहे.", "सहमत आहे comes after the thing agreed with.")]),
        [D("व्यवस्थापक", "या योजनेवर तुमचे मत काय आहे?", "Ya yojnevar tumche mat kay ahe?", "What is your opinion on this plan?"),
         D("सहकारी", "मला वाटते की पहिला टप्पा वेळेत पूर्ण होईल.", "Mala vaatte ki pahila tapp velt purn hoil.", "I think the first stage will finish in time."),
         D("व्यवस्थापक", "आणि खर्चाबद्दल?", "Aani kharchabaddal?", "And about the cost?"),
         D("सहकारी", "तेथे मला आक्षेप आहे. खर्च वाढल्यास मुदत बदलावी लागेल.", "Tethe mala aakshep ahe. Kharch vaadlyas mudat badlavi lagel.", "There I have an objection. If the cost rises, the deadline will have to change.")],
        WS("Meeting worksheet", [
            T("Put your opinion.", ["I think the first stage will finish in time", "I agree with the first point"],
              ["मला वाटते की पहिला टप्पा वेळेत पूर्ण होईल", "मी पहिल्या मुद्द्याशी सहमत आहे"]),
            T("Object politely.", ["I have an objection to the cost", "if the cost rises the deadline will change"],
              ["मला खर्चावर आक्षेप आहे", "खर्च वाढल्यास मुदत बदलेल"]),
        ]))),
    ("mr-b1-u2", "mr-b1-l8", L("अर्ज आणि मुलाखत",
        "An application and an interview move into the formal register: अनुभव, कौशल्य, अपेक्षा. "
        "Experience is counted in वर्षे and stated with the perfect केले आहे; जबाबदारी is feminine, "
        "so सांभाळली agrees with it. अपेक्षा is feminine too — अपेक्षा आहे, अपेक्षा नाही.",
        [V("अर्ज", "arj", "application", "noun"),
         V("मुलाखत", "mulakhat", "interview", "noun"),
         V("अनुभव", "anubhav", "experience", "noun"),
         V("कौशल्य", "kaushalya", "skill", "noun"),
         V("जबाबदारी", "jababdari", "responsibility", "noun")],
        G("Talking about experience",
          "मी चार वर्षे काम केले आहे · जबाबदारी सांभाळली · अपेक्षा एवढीच",
          "A counted period takes the plural वर्षे (चार वर्षे, दहा वर्षे). The perfect केले आहे "
          "presents the experience as still standing, and the object decides the ending of the "
          "verb: जबाबदारी सांभाळली, टीम सांभाळली, अहवाल सांभाळला.",
          [X("मी चार वर्षे विक्रीत काम केले आहे.", "Mi char varshe vikrit kaam kele ahe.", "I have worked four years in sales."),
           X("मी दहा जणांची टीम सांभाळली.", "Mi daha jnanchi team saambhalli.", "I handled a team of ten."),
           X("माझी अपेक्षा एवढीच आहे की काम शिकायला मिळावे.", "Majhi apeksha evdhich ahe ki kaam shikayla milave.", "My expectation is only that I get to learn on the job.")],
          [("मी दोन वर्ष काम केले आहे.", "मी दोन वर्षे काम केले आहे.", "A counted वर्ष takes the plural वर्षे."),
           ("मी जबाबदारी सांभाळला.", "मी जबाबदारी सांभाळली.", "जबाबदारी is feminine: सांभाळली.")]),
        [D("मुलाखतकार", "तुमचा अनुभव किती वर्षांचा आहे?", "Tumcha anubhav kiti varshacha ahe?", "How many years of experience do you have?"),
         D("उमेदवार", "चार वर्षे. मी विक्री विभागात काम केले आहे.", "Char varshe. Mi vikri vibhagat kaam kele ahe.", "Four years. I have worked in the sales department."),
         D("मुलाखतकार", "जबाबदारी कोणती होती?", "Jababdari konti hoti?", "What was your responsibility?"),
         D("उमेदवार", "दहा जणांची टीम आणि मासिक अहवाल.", "Daha jnanchi team aani masik ahaval.", "A team of ten and the monthly report.")],
        WS("Interview worksheet", [
            T("State your experience.", ["I have worked four years in sales", "I handled a team of ten"],
              ["मी चार वर्षे विक्रीत काम केले आहे", "मी दहा जणांची टीम सांभाळली"]),
            T("Answer the question.", ["what was your responsibility?", "what are your expectations?"],
              ["जबाबदारी कोणती होती?", "तुमच्या अपेक्षा काय आहेत?"]),
        ]))),
    ("mr-b1-u3", "mr-b1-l9", L("तक्रार आणि उपाय",
        "A complaint names the thing, the period and the remedy: हे मशीन सहा दिवसांपासून बंद आहे, "
        "तरी दुरुस्त झाले नाही. A stretch of time up to the present takes -पासून, the negative "
        "perfect reports what has not happened, and the polite demand uses करून द्या or बदलून द्या.",
        [V("तक्रार", "takrar", "complaint", "noun"),
         V("दुरुस्ती", "durusti", "repair", "noun"),
         V("बदलणे", "badalne", "to change, to replace", "verb"),
         V("वॉरंटी", "warranty", "warranty", "noun"),
         V("तपशील", "tapshil", "details", "noun")],
        G("Making a complaint",
          "सहा दिवसांपासून बंद आहे · दुरुस्त झाले नाही · बदलून द्या",
          "A duration up to the present takes -पासून (दोन आठवड्यांपासून). The negative perfect "
          "दुरुस्त झाले नाही says that the repair has not happened, which is stronger than a "
          "present negative. The demand keeps the polite imperative in -ा: बदलून द्या.",
          [X("हे मशीन सहा दिवसांपासून बंद आहे.", "He machine saha divsanpasun band ahe.", "This machine has been off for six days."),
           X("वॉरंटी आहे, पण दुरुस्ती झाली नाही.", "Warranty ahe, pan durusti jhali nahi.", "There is a warranty, but the repair was not done."),
           X("कृपया नवीन वस्तू बदलून द्या.", "Krupya navin vastu badlun dya.", "Please replace the item with a new one.")],
          [("हे मशीन सहा दिवस बंद आहे.", "हे मशीन सहा दिवसांपासून बंद आहे.", "A period up to now takes -पासून."),
           ("वॉरंटी आहेत.", "वॉरंटी आहे.", "वॉरंटी is singular feminine: आहे.")]),
        [D("ग्राहक", "हे मशीन सहा दिवसांपासून बंद आहे.", "He machine saha divsanpasun band ahe.", "This machine has been off for six days."),
         D("सेवा कर्मचारी", "वॉरंटी आहे का?", "Warranty ahe ka?", "Is there a warranty?"),
         D("ग्राहक", "हो, पण दुरुस्ती झाली नाही.", "Ho, pan durusti jhali nahi.", "Yes, but the repair was not done."),
         D("सेवा कर्मचारी", "तपशील द्या. आम्ही तपासतो आणि बदलून देतो.", "Tapshil dya. Aamhi tapasto aani badlun deto.", "Give me the details. We will check and replace it.")],
        WS("Complaint worksheet", [
            T("State the problem.", ["the machine has been off for six days", "there is a warranty"],
              ["मशीन सहा दिवसांपासून बंद आहे", "वॉरंटी आहे"]),
            T("Ask for the remedy.", ["please replace the item", "the repair was not done"],
              ["कृपया वस्तू बदलून द्या", "दुरुस्ती झाली नाही"]),
        ]))),
]

THIRD["B2"] = [
    ("mr-b2-u1", "mr-b2-l7", L("अंदाजपत्रक आणि मर्यादा",
        "Planning speaks in conditions and obligations: खर्च वाढल्यास …, प्रत्येक टप्प्याला मर्यादा "
        "ठरवावी लागेल. The formal conditional is -ल्यास, the spoken one is तर, and obligation uses "
        "the -ावी/-ावे form with लागेल, agreeing with its noun. Marathi keeps the obligation "
        "impersonal, so the person is named only when it matters.",
        [V("अंदाजपत्रक", "andaajpatrak", "budget", "noun"),
         V("खर्च", "kharch", "expenditure, cost", "noun"),
         V("मर्यादा", "maryada", "limit", "noun"),
         V("तरतूद", "tartud", "provision, arrangement", "noun"),
         V("ठरवणे", "tharvne", "to decide, to fix", "verb")],
        G("Condition and obligation",
          "खर्च वाढल्यास … · मर्यादा ठरवावी लागेल · तरतूद ठेवली आहे",
          "-ल्यास is the formal if (वाढल्यास, झाल्यास) and closes its own clause; तर is the spoken "
          "one and follows it. Obligation takes -ावी/-ावे with लागेल, and it agrees with its noun: "
          "मर्यादा ठरवावी लागेल, खर्च ठरवावा लागेल, काम करावे लागेल.",
          [X("खर्च वाढल्यास मुदत वाढवावी लागेल.", "Kharch vaadlyas mudat vaadhavi lagel.", "If the cost rises, the deadline will have to be extended."),
           X("प्रत्येक टप्प्याला मर्यादा ठरवावी लागेल.", "Pratyek tappyala maryada tharvavi lagel.", "A limit will have to be fixed for each stage."),
           X("यासाठी तरतूद ठेवली आहे.", "Yasathi tartud thevli ahe.", "A provision has been kept for this.")],
          [("टप्प्याला मर्यादा ठरवली लागेल.", "टप्प्याला मर्यादा ठरवावी लागेल.", "Obligation takes the -ावी form: ठरवावी लागेल."),
           ("खर्च वाढला तर मुदत वाढेल लागेल.", "खर्च वाढल्यास मुदत वाढवावी लागेल.", "One obligation frame, not two futures stacked.")]),
        [D("व्यवस्थापक", "या वर्षीचे अंदाजपत्रक तयार आहे का?", "Ya varshicha andaajpatrak tayar ahe ka?", "Is this year's budget ready?"),
         D("सल्लागार", "तयार आहे, पण दोन टप्प्यांना मर्यादा ठरवावी लागेल.", "Tayar ahe, pan don tappyanna maryada tharvavi lagel.", "It is ready, but a limit will have to be fixed for two stages."),
         D("व्यवस्थापक", "खर्च वाढल्यास काय करायचे?", "Kharch vaadlyas kay karayche?", "If the cost rises, what is to be done?"),
         D("सल्लागार", "तेव्हा मुदत वाढवावी लागेल किंवा कामकाज कमी करावे लागेल.", "Tevha mudat vaadhavi lagel kinva kamkaj kami karave lagel.", "Then the deadline will have to be extended or the work cut down.")],
        WS("Budget worksheet", [
            T("State the condition.", ["if the cost rises the deadline will change", "a limit for each stage"],
              ["खर्च वाढल्यास मुदत बदलेल", "प्रत्येक टप्प्याला मर्यादा"]),
            T("State the obligation.", ["a provision has been kept", "the work will have to be cut down"],
              ["तरतूद ठेवली आहे", "कामकाज कमी करावे लागेल"]),
        ]))),
    ("mr-b2-u2", "mr-b2-l8", L("वाटाघाटी आणि तडजोड",
        "A negotiation leaves room inside the sentence: या दरात पुरवठा करता येईल. The potential "
        "-ता येईल makes an offer without promising it, a refusal names what is impossible rather "
        "than the person, and तडजोडीची तयारी states readiness. A counter-offer usually opens with "
        "थोडे or पण, so that the door stays open.",
        [V("वाटाघाटी", "vaataghatai", "negotiation, talks", "noun"),
         V("अट", "at", "condition, term", "noun"),
         V("तडजोड", "tadjod", "compromise", "noun"),
         V("तयारी", "tayari", "readiness, preparation", "noun"),
         V("शक्य", "shakya", "possible", "adjective")],
        G("Softening and refusing",
          "करता येईल · इतक्यात शक्य नाही · तडजोडीची तयारी आहे",
          "The potential -ता येईल (करता, देता, घेता) offers without committing. A refusal names the "
          "impossible: इतक्यात शक्य नाही. Readiness takes the -ची possessive of what one is ready "
          "for — तडजोडीची तयारी, बोलणीची तयारी.",
          [X("या दरात पुरवठा करता येईल.", "Ya daarat purvatha karta yeil.", "Supply can be made at this rate."),
           X("इतक्यात शक्य नाही, पण विचार करता येईल.", "Itkyat shakya nahi, pan vichaar karta yeil.", "It is not possible at that rate, but it can be considered."),
           X("आमची तडजोडीची तयारी आहे.", "Aamchi tadjodichi tayari ahe.", "We are ready to compromise.")],
          [("देणे करता येईल.", "देणे देता येईल.", "The potential takes the -ता stem: देता येईल, करता येईल."),
           ("आमची तयारी आहे तडजोड.", "आमची तडजोडीची तयारी आहे.", "तयारी takes -ची of what one is ready for.")]),
        [D("खरेदी प्रमुख", "या दरात पुरवठा करता येईल का?", "Ya daarat purvatha karta yeil ka?", "Can supply be made at this rate?"),
         D("पुरवठादार", "इतक्यात शक्य नाही. वाहतूक खर्च वेगळा आहे.", "Itkyat shakya nahi. Vahatuk kharch vegla ahe.", "Not possible at that rate. The transport cost is separate."),
         D("खरेदी प्रमुख", "थोडी तडजोड करा. दोन्ही बाजूंना फायदा हवा.", "Thodi tadjod kara. Donhi bajunna fayda hava.", "Compromise a little. Both sides should gain."),
         D("पुरवठादार", "ठीक. मुदत दोन महिन्यांऐवजी तीन महिने हवी.", "Thik. Mudat don mahinyan-aivaji teen mahine havi.", "All right. Instead of two months, the deadline should be three.")],
        WS("Negotiation worksheet", [
            T("Make an offer.", ["supply can be made at this rate", "it can be considered"],
              ["या दरात पुरवठा करता येईल", "विचार करता येईल"]),
            T("Hold your ground politely.", ["not possible at that rate", "we are ready to compromise"],
              ["इतक्यात शक्य नाही", "आमची तडजोडीची तयारी आहे"]),
        ]))),
    ("mr-b2-u3", "mr-b2-l9", L("अहवाल आणि आढावा",
        "A report names its finding impersonally: अहवालात नमूद केले आहे की …, and it keeps what "
        "is pending visible with बाकी आहेत. आढावा घेणे is the verb for holding a review, and the "
        "passive जाईल announces the next step without naming who takes it. A reported clause always "
        "takes की.",
        [V("अहवाल", "ahaval", "report", "noun"),
         V("आढावा", "aadhava", "review", "noun"),
         V("पडताळणी", "padtaalni", "verification", "noun"),
         V("नमूद", "namud", "stated, recorded", "adjective"),
         V("बाकी", "baki", "pending, remaining", "noun")],
        G("Reporting a finding",
          "अहवालात नमूद केले आहे की … · पडताळणीच्या बाकी आहेत · आढावा घेतला जाईल",
          "A reported clause takes की. नमूद केले आहे and म्हटले आहे keep the writer out of the "
          "sentence, and बाकी agrees with what is pending (मुद्दे बाकी आहेत). The passive जाईल "
          "announces the next step, and तपासले आहे reports what is already done.",
          [X("अहवालात नमूद केले आहे की खर्च अंदाजापेक्षा जास्त आहे.", "Ahavalat namud kele ahe ki kharch andaajapeksha jaast ahe.", "The report states that the cost is higher than estimated."),
           X("दोन मुद्दे पडताळणीच्या बाकी आहेत.", "Don mudde padtalnicha baki aahet.", "Two points are still pending verification."),
           X("पुढील महिन्यात आढावा घेतला जाईल.", "Pudhil mahinyat aadhava ghetla jail.", "The review will be held next month.")],
          [("दोन मुद्दे बाकी आहे.", "दोन मुद्दे बाकी आहेत.", "मुद्दे is plural, so it takes आहेत."),
           ("अहवालात नमूद केले आहे खर्च वाढला.", "अहवालात नमूद केले आहे की खर्च वाढला.", "A reported clause takes की.")]),
        [D("संचालक", "आढाव्याचा अहवाल तयार आहे का?", "Aadhavyacha ahaval tayar ahe ka?", "Is the review report ready?"),
         D("विभाग प्रमुख", "हो, पण दोन मुद्दे पडताळणीच्या बाकी आहेत.", "Ho, pan don mudde padtalnicha baki aahet.", "Yes, but two points are still pending verification."),
         D("संचालक", "कोणते मुद्दे?", "Konte mudde?", "Which points?"),
         D("विभाग प्रमुख", "खर्च आणि मुदत. उर्वरित सर्व तपासले आहे.", "Kharch aani mudat. Urvarit sarva tapasle ahe.", "Cost and deadline. Everything else has been checked.")],
        WS("Report worksheet", [
            T("Report the finding.", ["the cost is higher than estimated", "two points are pending"],
              ["खर्च अंदाजापेक्षा जास्त आहे", "दोन मुद्दे बाकी आहेत"]),
            T("Announce the next step.", ["the review will be held next month", "everything else has been checked"],
              ["पुढील महिन्यात आढावा घेतला जाईल", "उर्वरित सर्व तपासले आहे"]),
        ]))),
]

THIRD["C1"] = [
    ("mr-c1-u1", "mr-c1-l7", L("संशोधन पद्धत आणि नमुना",
        "A method section is written in the passive and the impersonal: नमुना विभागला गेला, माहिती "
        "प्रश्नावलीद्वारे गोळा करण्यात आली. Marathi academic prose prefers करण्यात आले / जाहले over "
        "the first person, names the tool with -द्वारे or -तून, and keeps the sample size in words "
        "for small numbers.",
        [V("पद्धत", "paddhat", "method", "noun"),
         V("नमुना", "namuna", "sample", "noun"),
         V("प्रश्नावली", "prashnavali", "questionnaire", "noun"),
         V("विश्लेषण", "vishleshan", "analysis", "noun"),
         V("मर्यादा", "maryada", "limitation, limit", "noun")],
        G("Writing a method",
          "नमुना विभागला गेला · माहिती गोळा करण्यात आली · विश्लेषण करण्यात आले",
          "The passive -ला गेला / करण्यात आले keeps the researcher out of the sentence. People are "
          "counted with जणे (दोनशे जणांचा नमुना), the instrument takes -द्वारे (प्रश्नावलीद्वारे), "
          "and a limitation is नोंदवली गेली — feminine, because मर्यादा is feminine.",
          [X("दोनशे जणांचा नमुना यादृच्छिक पद्धतीने निवडला गेला.", "Donshe jnancha namuna yaadruchchhik paddhatine nivadla gela.", "A sample of two hundred was selected at random."),
           X("माहिती प्रश्नावलीद्वारे गोळा करण्यात आली.", "Mahiti prashnavalidvare gola karanyat aali.", "The information was collected through a questionnaire."),
           X("अभ्यासात दोन मर्यादा नोंदवल्या गेल्या.", "Abhyasat don maryada nondavlya gelya.", "Two limitations were recorded in the study.")],
          [("नमुना निवडला गेली.", "नमुना निवडला गेला.", "नमुना is masculine: निवडला गेला."),
           ("प्रश्नावली भरून घेतले.", "प्रश्नावली भरून घेतली.", "प्रश्नावली is feminine: घेतली.")]),
        [D("मार्गदर्शक", "नमुना कसा निवडला गेला?", "Namuna kasa nivadla gela?", "How was the sample selected?"),
         D("संशोधक", "दोन गटांतून प्रत्येकी पन्नास जण घेतले गेले.", "Don gantun pratyeki pannas jan ghetle gele.", "Fifty people were taken from each of two groups."),
         D("मार्गदर्शक", "माहिती कोणत्या साधनाने गोळा केली?", "Mahiti kontya sadhanane gola keli?", "With which instrument was the information collected?"),
         D("संशोधक", "प्रश्नावली आणि प्रत्यक्ष भेटी, अशा दोन साधनांद्वारे.", "Prashnavali aani pratyaksh bheti, asha don sadhanandvare.", "Through two instruments: a questionnaire and direct visits.")],
        WS("Method worksheet", [
            T("Write it impersonally.", ["the sample was selected at random", "the information was collected through a questionnaire"],
              ["नमुना यादृच्छिक पद्धतीने निवडला गेला", "माहिती प्रश्नावलीद्वारे गोळा करण्यात आली"]),
            T("Record the limits.", ["two limitations were recorded", "the period is short"],
              ["दोन मर्यादा नोंदवल्या गेल्या", "कालावधी लहान आहे"]),
        ]))),
    ("mr-c1-u2", "mr-c1-l8", L("पुरावा आणि युक्तिवाद",
        "Argument ties proof to claim with सूचक, दर्शवते and दुजोरा देणे. Marathi grades a claim "
        "instead of inflating it: आकडेवारी सूचक आहे, पण ती कारण सिद्ध करत नाही. सिद्ध करणे claims "
        "proof, पुरेसा नाही refuses it, and दुजोरा देणे brings a second source in.",
        [V("पुरावा", "purava", "evidence, proof", "noun"),
         V("युक्तिवाद", "yuktivad", "argument", "noun"),
         V("सूचक", "suchak", "indicative", "adjective"),
         V("दुजोरा", "dujora", "corroboration", "noun"),
         V("सिद्ध", "siddh", "proved", "adjective")],
        G("Grading a claim",
          "सूचक आहे · दुजोरा देणे · पुरेसा नाही",
          "सूचक describes evidence that points without proving; दुजोरा देणे is what a second source "
          "does; पुरेसा नाही refuses the strength of the evidence, agreeing with पुरावा. सिद्ध "
          "करणे is reserved for designs that can carry it, and सिद्ध होत नाही is the honest "
          "alternative when they cannot.",
          [X("ही आकडेवारी सूचक आहे, पुरावा नाही.", "Hi aakdevaari suchak ahe, purava nahi.", "These data are indicative, not proof."),
           X("दुसऱ्या संशोधनाने या निष्कर्षाला दुजोरा दिला.", "Dusrya sanshodhanane ya nishkarshala dujora dila.", "A second study corroborated this finding."),
           X("एका निरीक्षणावरून एवढा दावा सिद्ध होत नाही.", "Eka nirikshanavarun evdha dava siddh hot nahi.", "Such a claim is not proved by one observation.")],
          [("आकडेवारी हे सिद्ध करतो.", "आकडेवारी हे सिद्ध करते.", "आकडेवारी is feminine: करते."),
           ("पुरावा पुरेसे नाही.", "पुरावा पुरेसा नाही.", "पुरावा is masculine singular: पुरेसा.")]),
        [D("समीक्षक", "हा दावा कोणत्या पुराव्यावर उभा आहे?", "Ha dava kontya puravyavar ubha ahe?", "On what evidence does this claim stand?"),
         D("संशोधक", "दोन वर्षांची आकडेवारी आणि साक्षी.", "Don varshachi aakdevaari aani sakshi.", "Two years of data and interviews."),
         D("समीक्षक", "ती आकडेवारी कारण दाखवते का?", "Ti aakdevaari karan dakhvate ka?", "Do those data show causation?"),
         D("संशोधक", "नाही, ती सूचक आहे. कारणासाठी पुढील अभ्यास हवा.", "Nahi, ti suchak ahe. Karanasathi pudhil abhyas hava.", "No, they are indicative. Causation needs a further study.")],
        WS("Argument worksheet", [
            T("Grade the evidence.", ["the data are indicative", "the evidence is not sufficient"],
              ["आकडेवारी सूचक आहे", "पुरावा पुरेसा नाही"]),
            T("Bring in a second source.", ["a second study corroborated the finding", "the claim is not proved by one observation"],
              ["दुसऱ्या संशोधनाने निष्कर्षाला दुजोरा दिला", "एका निरीक्षणावरून दावा सिद्ध होत नाही"]),
        ]))),
    ("mr-c1-u3", "mr-c1-l9", L("समीक्षा आणि सुधारणा",
        "A review asks for changes without rewriting the author's paper: हा परिच्छेद दुसऱ्या "
        "क्रमाने ठेवावा, उदाहरण जोडावे, संदर्भ द्यावेत. The -ावा/-ावी/-ावे form states what should "
        "be done and agrees with its noun, and the operations are जोडणे, वगळणे and पुन्हा लिहिणे.",
        [V("समीक्षा", "samiksha", "review", "noun"),
         V("सुधारणा", "sudharna", "revision, improvement", "noun"),
         V("संदर्भ", "sandarbh", "reference", "noun"),
         V("वगळणे", "vagalne", "to omit, to leave out", "verb"),
         V("जोडणे", "jodne", "to add, to attach", "verb")],
        G("Recommendations in a review",
          "परिच्छेद ठेवावा · टीका वगळावी · उदाहरण जोडावे",
          "The -ावा/-ावी/-ावे form recommends without commanding and agrees with the noun it "
          "belongs to: परिच्छेद ठेवावा (m), टीका वगळावी (f), उदाहरण जोडावे (n). References in the "
          "plural take द्यावेत, and a passage that has to be rewritten is पुन्हा लिहावा.",
          [X("हा परिच्छेद चौथ्या क्रमांकावर ठेवावा.", "Ha parichchhed chouthya kramankavar thevava.", "This paragraph should be placed fourth."),
           X("उदाहरण जोडावे आणि संदर्भ द्यावेत.", "Udaharan jodave aani sandarbh dyavet.", "An example should be added and references given."),
           X("टीकेचा भाग वगळावा.", "Tikecha bhag vagalava.", "The critical part should be left out.")],
          [("उदाहरण जोडावा.", "उदाहरण जोडावे.", "उदाहरण is neuter: जोडावे."),
           ("संदर्भ द्यावा.", "संदर्भ द्यावेत.", "संदर्भ in the plural takes द्यावेत.")]),
        [D("संपादक", "पहिल्या परिच्छेदात काय बदलावे?", "Pahilya parichchhedat kay badlave?", "What should change in the first paragraph?"),
         D("लेखक", "उदाहरण जोडावे आणि संदर्भ द्यावेत, असे वाटते.", "Udaharan jodave aani sandarbh dyavet, ase vaatte.", "I think an example should be added and references given."),
         D("संपादक", "आणि शेवटचा भाग?", "Aani shevtacha bhag?", "And the last part?"),
         D("लेखक", "तो वगळतो आणि उरलेला प्रश्न तिथे ठेवतो.", "To vagalto aani urelela prashn tithe thevto.", "I will leave it out and keep the open question there.")],
        WS("Review worksheet", [
            T("Recommend a change.", ["this paragraph should be placed fourth", "the critical part should be left out"],
              ["हा परिच्छेद चौथ्या क्रमांकावर ठेवावा", "टीकेचा भाग वगळावा"]),
            T("Add what is missing.", ["an example should be added", "references should be given"],
              ["उदाहरण जोडावे", "संदर्भ द्यावेत"]),
        ]))),
]

THIRD["C2"] = [
    ("mr-c2-u1", "mr-c2-l7", L("शैली आणि उपरोध",
        "Irony in Marathi leans on उपरोध and वक्रोक्ती: the sentence says the opposite and trusts "
        "the reader to hear it. The markers are काय तर …, किती चांगले! and the rhetorical question; "
        "वक्रोक्ती is the older name for the same figure — the word with the meaning turned under "
        "it. A formal text keeps one ironical stroke, usually at the end.",
        [V("शैली", "shaili", "style", "noun"),
         V("उपरोध", "uparodh", "irony", "noun"),
         V("वक्रोक्ती", "vakrokti", "oblique speech", "noun"),
         V("छटा", "chhata", "nuance, shade", "noun"),
         V("उपरोधपूर्ण", "uparodhpurn", "ironical", "adjective")],
        G("Saying the opposite",
          "काय तर … · किती चांगले! · मग हे यश म्हणायचे का?",
          "उपरोध puts the praise where the criticism belongs and lets the next sentence carry the "
          "point; वक्रोक्ती names the same turn in poetics. The adjective is formed with -पूर्ण "
          "(उपरोधपूर्ण, अर्थपूर्ण), and a rhetorical question closes the paragraph without "
          "asserting anything.",
          [X("अरेरे, किती चांगली व्यवस्था!", "Areere, kiti chaangli vyavastha!", "Oh dear, what a fine arrangement!"),
           X("मग हे यश म्हणायचे का?", "Mag he yash mhanayache ka?", "Then is this to be called a success?"),
           X("शब्द तेच, अर्थ मात्र उलटा.", "Shabd tech, arth maatra ulta.", "The same words, the meaning turned around.")],
          [("हे वाक्य उपरोधिक आहे.", "हे वाक्य उपरोधपूर्ण आहे.", "The Marathi adjective is उपरोधपूर्ण."),
           ("शब्दांची छटा सूक्ष्म आहेत.", "शब्दांची छटा सूक्ष्म आहे.", "छटा is singular feminine: आहे.")]),
        [D("संपादक", "हा परिच्छेद थेट टीका वाटतो.", "Ha parichchhed thet tika vaatto.", "This paragraph reads as direct criticism."),
         D("लेखक", "म्हणून उपरोध वापरला आहे — वाचक स्वतः निष्कर्ष काढेल.", "Mhanun uparodh vaparla ahe — vaachak svatah nishkarsh kadhel.", "That is why irony is used — the reader will draw the conclusion."),
         D("संपादक", "शेवटच्या वाक्यात ठेवा, मधे नको.", "Shevtachya vakyat theva, madhe nako.", "Keep it in the last sentence, not in the middle."),
         D("लेखक", "ठीक, मग शेवटचे वाक्य उपरोधपूर्ण ठेवतो.", "Thik, mag shevtache vakya uparodhpurn thevto.", "All right, then I will keep the last sentence ironical.")],
        WS("Style worksheet", [
            T("Turn it into irony.", ["what a fine arrangement (ironical)", "then is this to be called a success?"],
              ["किती चांगली व्यवस्था!", "मग हे यश म्हणायचे का?"]),
            T("Name the figure.", ["the same words, the meaning turned around", "the adjective ironical"],
              ["शब्द तेच, अर्थ मात्र उलटा", "उपरोधपूर्ण"]),
        ]))),
    ("mr-c2-u2", "mr-c2-l8", L("भाषांतर आणि अर्थ",
        "Translation keeps three things honest: शब्दशः, भावार्थ and रूढ अर्थ. Marathi distinguishes "
        "शब्दशः भाषांतर from भावार्थाने उतरवणे, and a म्हण is carried over by what it does rather "
        "than by its words. रूढ अर्थ, the settled sense, is the first casualty of a literal "
        "translation.",
        [V("भाषांतर", "bhashantar", "translation", "noun"),
         V("भावार्थ", "bhavarth", "sense, meaning", "noun"),
         V("म्हण", "mhan", "proverb, saying", "noun"),
         V("रूढ अर्थ", "rudh arth", "settled meaning", "noun"),
         V("आशय", "aashay", "import, purport", "noun")],
        G("Carrying meaning across",
          "शब्दशः भाषांतर · भावार्थाने उतरवणे · रूढ अर्थ टिकवणे",
          "शब्दशः is the adverb for word-for-word; भावार्थाने उतरवणे works by sense. म्हण is "
          "feminine (म्हण उतरवली), अर्थ is masculine singular (अर्थ बदलला), and the settled usage "
          "is रूढ अर्थ — the sense a reader supplies without being told.",
          [X("ही म्हण शब्दशः उतरवता येत नाही.", "Hi mhan shabdashah utarvata yet nahi.", "This proverb cannot be translated word for word."),
           X("भावार्थाने उतरवले तर अर्थ टिकतो.", "Bhavarthane utarvale tar arth tiktto.", "Translated by sense, the meaning survives."),
           X("रूढ अर्थ बदलला की वाक्य चुकते.", "Rudh arth badalla ki vakya chukte.", "Change the settled sense and the sentence goes wrong.")],
          [("म्हण उतरवला.", "म्हण उतरवली.", "म्हण is feminine: उतरवली."),
           ("रूढ अर्थ बदलले.", "रूढ अर्थ बदलला.", "अर्थ is masculine singular: बदलला.")]),
        [D("अनुवादक", "ही म्हण शब्दशः उतरवता येत नाही.", "Hi mhan shabdashah utarvata yet nahi.", "This proverb cannot be translated word for word."),
         D("संपादक", "मग भावार्थाने उतरवा.", "Mag bhavarthane utarva.", "Then translate it by sense."),
         D("अनुवादक", "पण रूढ अर्थ टिकवावा लागेल.", "Pan rudh arth tikvava lagel.", "But the settled sense will have to be kept."),
         D("संपादक", "हो, अन्यथा वाक्य परक्या भाषेत हसू लागते.", "Ho, anyatha vakya parkya bhashet hasu lagte.", "Yes, otherwise the sentence starts to laugh in a foreign language.")],
        WS("Translation worksheet", [
            T("Choose the method.", ["translate it word for word", "translate it by sense"],
              ["शब्दशः उतरवा", "भावार्थाने उतरवा"]),
            T("Keep the usage.", ["the settled sense must be kept", "the proverb cannot be translated literally"],
              ["रूढ अर्थ टिकवावा लागेल", "म्हण शब्दशः उतरवता येत नाही"]),
        ]))),
    ("mr-c2-u3", "mr-c2-l9", L("वक्तृत्व आणि संवाद",
        "Mediating a dispute means giving each side its own sentence before any judgement: एकीकडे … "
        "दुसरीकडे …. The speaker then hedges with असे म्हणता येईल and turns the audience into the "
        "actor of the conclusion with आपण … ऊ या. विनय, the show of deference, keeps a formal "
        "speaker from sounding like a judge.",
        [V("वक्तृत्व", "vaktrutva", "oratory", "noun"),
         V("संवाद", "sanvad", "dialogue, conversation", "noun"),
         V("त्रयस्थ", "trayasth", "neutral third party", "noun"),
         V("विनय", "vinay", "deference, modesty", "noun"),
         V("सूत्र", "sutra", "thread, formula", "noun")],
        G("Holding both sides",
          "एकीकडे … दुसरीकडे … · असे म्हणता येईल · आपण हे ठरवू या",
          "एकीकडे … दुसरीकडे … gives each side a clause of its own, so the audience hears both "
          "before the speaker's own view. असे म्हणता येईल hedges that view, and आपण with the "
          "-ऊ या form turns the conclusion into a joint decision. त्रयस्थ keeps the mediator out "
          "of both camps.",
          [X("एकीकडे खर्च आहे, दुसरीकडे धोका आहे.", "Ekikade kharch ahe, dusrikade dhoka ahe.", "On one side there is cost, on the other there is risk."),
           X("असे म्हणता येईल की दोन्ही बाजूंना वेळ हवा.", "Ase mhanta yeil ki donhi bajunna vel hava.", "It could be said that both sides need time."),
           X("आपण हा प्रश्न मोकळा ठेवू या.", "Aapan ha prashn mokla thevu ya.", "Let us leave this question open.")],
          [("आपण हा प्रश्न ठेवेल.", "आपण हा प्रश्न ठेवू या.", "आपण takes the inclusive -ऊ या form."),
           ("आपण हे ठरवून घेऊ.", "आपण हे ठरवू या.", "The proposal form is -ऊ या, not the reflexive घेऊ.")]),
        [D("मध्यस्थ", "दोघांनी तक्रार मांडली आहे. आता प्रश्न कसा ठरवायचा?", "Doghanne takrar mandli ahe. Aata prashn kasa tharvayacha?", "Both sides have put their complaint. How is the question to be settled now?"),
         D("सल्लागार", "एकीकडे खर्च आहे, दुसरीकडे वेळ. दोन्ही खरे आहेत.", "Ekikade kharch ahe, dusrikade vel. Donhi khare aahet.", "On one side cost, on the other time. Both are true."),
         D("मध्यस्थ", "मग आपण क्रम ठरवू या: आधी वेळ, नंतर खर्च.", "Mag aapan kram thevu ya: aadhi vel, nantar kharch.", "Then let us settle the order: time first, cost after."),
         D("सल्लागार", "तेच योग्य. असे म्हणता येईल की तडजोडीची वाट मोकळी आहे.", "Tech yogya. Ase mhanta yeil ki tadjodichi vaat mokli ahe.", "That is right. It could be said that the way to a compromise is open.")],
        WS("Mediation worksheet", [
            T("Give each side its sentence.", ["on one side cost, on the other risk", "both are true"],
              ["एकीकडे खर्च आहे, दुसरीकडे धोका आहे", "दोन्ही खरे आहेत"]),
            T("Turn it into a joint decision.", ["let us settle the order", "let us leave the question open"],
              ["आपण क्रम ठरवू या", "आपण हा प्रश्न मोकळा ठेवू या"]),
        ]))),
]

HALFSTEPS["A1+"] = {
    "title": "Marathi A1+ — A day and a call",
    "native": NATIVE,
    "goals": [
        "Describe a whole day hour by hour and say how you travel",
        "Answer the phone, send a message and take down a number",
        "Invite somebody, accept, and decline without giving offence",
    ],
    "units": [
        {"id": "A1+-U1", "title": "दिवसाची सुरुवात", "lessons": [
            L("सकाळी काय करता?",
              "A day is a list of verbs on a clock: उठते, चहा करते, निघते. The hour takes वाजता and "
              "stands before the verb, and the habit takes the simple present rather than आहे.",
              [V("उठणे", "uthne", "to get up", "verb"),
               V("चहा", "chaha", "tea", "noun"),
               V("निघणे", "nighne", "to set out, to leave", "verb"),
               V("सकाळ", "sakal", "morning", "noun"),
               V("रोज", "roj", "every day", "adverb")],
              G("Telling the hour",
                "सहा वाजता उठते · साडेसात वाजता निघते · रोज चहा करते",
                "A clock time takes वाजता and stands before the verb: सहा वाजता, साडेसात वाजता, "
                "सव्वा नऊ वाजता. A routine takes the simple present, and रोज or रोज सकाळी makes the "
                "habit explicit without any auxiliary.",
                [X("मी रोज सहा वाजता उठते.", "Mi roj saha vajta uthate.", "I get up at six every day."),
                 X("साडेसात वाजता घरातून निघते.", "Saadesaat vajta gharatun nighate.", "I leave home at half past seven."),
                 X("आधी चहा करते, मग आंघोळ करते.", "Aadhi chaha karte, mag aanghol karte.", "First I make tea, then I bathe.")],
                [("मी सहा वाजता उठते आहे.", "मी सहा वाजता उठते.", "A daily routine takes the simple present, not आहे."),
                 ("मी सहा वाजेला उठते.", "मी सहा वाजता उठते.", "A clock time takes वाजता, not वाजेला.")]),
              [D("मीरा", "तुम्ही रोज किती वाजता उठता?", "Tumhi roj kiti vajta uthata?", "What time do you get up every day?"),
               D("स्नेहा", "सहा वाजता. मग चहा करते आणि साडेसात वाजता निघते.", "Saha vajta. Mag chaha karte aani saadesaat vajta nighate.", "At six. Then I make tea and leave at half past seven."),
               D("मीरा", "नाश्ता घरी करता का?", "Nashta ghari karta ka?", "Do you have breakfast at home?"),
               D("स्नेहा", "हो, पोहे किंवा उपमा. ते पटकन होते.", "Ho, pohe kinva upma. Te patkan hote.", "Yes, poha or upma. It is quick.")],
              WS("Routine worksheet", [
                  T("Say the hour.", ["I get up at six.", "I leave at half past seven."],
                    ["सहा वाजता उठते", "साडेसात वाजता निघते"]),
                  T("Ask the question.", ["what time do you get up?", "do you have breakfast at home?"],
                    ["किती वाजता उठता?", "नाश्ता घरी करता का?"]),
              ])),
            L("कामावर कसे जाता?",
              "Getting somewhere takes -ने for the vehicle (बसने, रिक्षाने, सायकलने) and चालत for "
              "walking. The time taken is वेळ लागतो, and the place you reach takes -पर्यंत.",
              [V("बसने", "basne", "by bus", "adverb"),
               V("रिक्षा", "riksha", "auto-rickshaw", "noun"),
               V("चालत", "chaalat", "on foot", "adverb"),
               V("वेळ", "vel", "time", "noun"),
               V("पोहोचणे", "pohochne", "to reach", "verb")],
              G("How you travel",
                "बसने जाते · चालत जाते · वीस मिनिटे लागतात",
                "A vehicle takes -ने (बसने, रिक्षाने, ट्रेनने) and walking takes चालत. The time "
                "spent is वेळ लागतो — the minutes are the subject, so the verb agrees with them: "
                "वीस मिनिटे लागतात, अर्धा तास लागतो.",
                [X("मी बसने कामावर जाते.", "Mi basne kamavar jate.", "I go to work by bus."),
                 X("पंधरा मिनिटे लागतात.", "Pandhra minute lagtaat.", "It takes fifteen minutes."),
                 X("चालत गेले तर अर्धा तास लागतो.", "Chaalat gele tar ardha taas laagto.", "On foot it takes half an hour.")],
                [("मी बस जाते.", "मी बसने जाते.", "The vehicle takes -ने: बसने जाते."),
                 ("वीस मिनिटे लागतो.", "वीस मिनिटे लागतात.", "मिनिटे is plural, so it takes लागतात.")]),
              [D("स्नेहा", "तुम्ही कामावर कसे जाता?", "Tumhi kamavar kase jata?", "How do you get to work?"),
               D("अर्णव", "रिक्षाने. सकाळी रिक्षा लवकर मिळते.", "Rikshane. Sakali riksha lavkar milte.", "By auto. In the morning an auto is easy to get."),
               D("स्नेहा", "किती वेळ लागतो?", "Kiti vel laagto?", "How long does it take?"),
               D("अर्णव", "वीस मिनिटे. पाऊस पडला तर पस्तीस.", "Vis minute. Paus padla tar pastis.", "Twenty minutes. If it rains, thirty-five.")],
              WS("Travel worksheet", [
                  T("Say how you go.", ["I go to work by bus", "I walk to the market"],
                    ["मी बसने कामावर जाते", "मी चालत बाजारात जाते"]),
                  T("Say how long.", ["it takes fifteen minutes", "it takes half an hour"],
                    ["पंधरा मिनिटे लागतात", "अर्धा तास लागतो"]),
              ])),
            L("संध्याकाळी घरी",
              "An evening is built with -नंतर (after) and the habitual present: जेवणानंतर अभ्यास "
              "करते. Liking takes मला … आवडते, and going to sleep is झोपणे with a time on it.",
              [V("संध्याकाळ", "sandhyakal", "evening", "noun"),
               V("जेवण", "jevan", "meal, dinner", "noun"),
               V("अभ्यास", "abhyas", "study", "noun"),
               V("आवडणे", "aavdne", "to like", "verb"),
               V("झोपणे", "jhopne", "to sleep", "verb")],
              G("After and before",
                "जेवणानंतर · जेवणाआधी · मला वाचायला आवडते",
                "-नंतर follows a noun in the oblique (जेवणानंतर, कामानंतर) and -आधी means before. "
                "आवडणे takes the dative मला and the thing liked in the -ायला form: मला वाचायला "
                "आवडते.",
                [X("जेवणानंतर मी अभ्यास करते.", "Jevnanantar mi abhyas karte.", "After dinner I study."),
                 X("मला गोष्टी वाचायला आवडतात.", "Mala goshti vaachayla aavdtaat.", "I like reading stories."),
                 X("अकरा वाजता झोपते.", "Akra vajta jhopte.", "I sleep at eleven.")],
                [("जेवण नंतर मी अभ्यास करते.", "जेवणानंतर मी अभ्यास करते.", "-नंतर attaches to the oblique: जेवणानंतर."),
                 ("मला गोष्टी वाचायला आवडते आहे.", "मला गोष्टी वाचायला आवडते.", "आवडणे needs no आहे for a general taste.")]),
              [D("अर्णव", "संध्याकाळी काय करता?", "Sandhyakali kay karta?", "What do you do in the evening?"),
               D("स्नेहा", "सहा वाजता घरी येते, मग जेवण करते.", "Saha vajta ghari yete, mag jevan karte.", "I come home at six, then eat."),
               D("अर्णव", "जेवणानंतर?", "Jevnanantar?", "After dinner?"),
               D("स्नेहा", "थोडा अभ्यास आणि गोष्टी वाचायला आवडते, मग अकरा वाजता झोपते.", "Thoda abhyas aani goshti vaachayla aavdte, mag akra vajta jhopte.", "A little study and I like reading stories, then I sleep at eleven.")],
              WS("Evening worksheet", [
                  T("Order the evening.", ["first dinner, then study", "I come home at six"],
                    ["आधी जेवण, मग अभ्यास", "मी सहा वाजता घरी येते"]),
                  T("Say what you like.", ["I like reading", "I sleep at eleven"],
                    ["मला वाचायला आवडते", "मी अकरा वाजता झोपते"]),
              ])),
        ]},
        {"id": "A1+-U2", "title": "फोन आणि संदेश", "lessons": [
            L("फोन उचला",
              "A Marathi phone call opens with हॅलो or नमस्कार, asks कोण बोलत आहे? and holds with "
              "थांबा. The polite form of बोलणे is बोलत आहे, and an unknown caller is asked rather "
              "than told.",
              [V("फोन", "phone", "phone", "noun"),
               V("उचलणे", "uchalne", "to pick up", "verb"),
               V("थांबणे", "thaambne", "to wait, to stop", "verb"),
               V("कोण", "kon", "who", "pronoun"),
               V("बोलणे", "bolne", "to speak", "verb")],
              G("On the phone",
                "फोन उचला · कोण बोलत आहे? · थोडे थांबा",
                "The polite imperative ends in -ा: उचला, थांबा, सांगा. कोण बोलत आहे? is the neutral "
                "way to ask who is calling, and the answer names the person with -तून: मी मीरा "
                "बोलत आहे.",
                [X("नमस्कार, कोण बोलत आहे?", "Namaskar, kon bolat ahe?", "Hello, who is speaking?"),
                 X("मी स्नेहा बोलत आहे.", "Mi Sneha bolat ahe.", "This is Sneha speaking."),
                 X("थोडे थांबा, मी त्यांना बोलावतो.", "Thode thaamba, mi tyanna bolavto.", "Wait a moment, I will call them.")],
                [("फोन घ्या.", "फोन उचला.", "For picking up a call Marathi says फोन उचला."),
                 ("तू कोण बोलत आहे?", "कोण बोलत आहे?", "The polite question needs no pronoun; तू would be rude to a stranger.")]),
              [D("मीरा", "नमस्कार, कोण बोलत आहे?", "Namaskar, kon bolat ahe?", "Hello, who is speaking?"),
               D("अर्णव", "नमस्कार, मी अर्णव बोलत आहे. स्नेहा घरी आहेत का?", "Namaskar, mi Arnav bolat ahe. Sneha ghari aahet ka?", "Hello, this is Arnav. Is Sneha at home?"),
               D("मीरा", "थोडे थांबा, मी त्यांना बोलावते.", "Thode thaamba, mi tyanna bolavte.", "Wait a moment, I will call her."),
               D("अर्णव", "धन्यवाद. मी नंतर पुन्हा फोन करतो.", "Dhanyavad. Mi nantar punha phone karto.", "Thank you. I will call again later.")],
              WS("Phone worksheet", [
                  T("Answer the call.", ["who is speaking?", "this is Meera speaking"],
                    ["कोण बोलत आहे?", "मी मीरा बोलत आहे"]),
                  T("Hold and promise.", ["wait a moment", "I will call again later"],
                    ["थोडे थांबा", "मी नंतर पुन्हा फोन करतो"]),
              ])),
            L("संदेश पाठवा",
              "A message is पाठवणे and it either मिळते or येते. Marathi marks the receiver with -ला "
              "(मला संदेश पाठवा) and the content with the plain clause, and short messages drop the "
              "pronoun altogether.",
              [V("संदेश", "sandesh", "message", "noun"),
               V("पाठवणे", "paathavne", "to send", "verb"),
               V("मिळणे", "milne", "to get, to receive", "verb"),
               V("उत्तर", "uttar", "reply, answer", "noun"),
               V("लगेच", "lagech", "immediately", "adverb")],
              G("Sending and getting",
                "मला संदेश पाठवा · संदेश मिळाला · लगेच उत्तर द्या",
                "पाठवणे sends, मिळणे receives, and उत्तर देणे replies. The receiver takes -ला "
                "(मला, त्यांना). In a short message the verb alone is enough: निघाले, पोहोचले, "
                "थांबा.",
                [X("मला संदेश पाठवा.", "Mala sandesh paathva.", "Send me a message."),
                 X("तुमचा संदेश मिळाला.", "Tumcha sandesh milala.", "Your message has reached me."),
                 X("लगेच उत्तर द्या.", "Lagech uttar dya.", "Reply at once.")],
                [("मी तुला संदेश पाठवतो.", "मी तुम्हाला संदेश पाठवतो.", "With the polite तुम्ही the object is तुम्हाला, not तुला."),
                 ("संदेश घेतला.", "संदेश मिळाला.", "A message that arrives मिळतो; घेतला would mean you took it deliberately.")]),
              [D("अर्णव", "मी निघालो, संदेश पाठवतो.", "Mi nighalo, sandesh paathavto.", "I have set out, I will send a message."),
               D("स्नेहा", "ठीक, पोहोचल्यावर कळवा.", "Thik, pohochlyavar kalva.", "All right, let me know when you reach."),
               D("अर्णव", "पोहोचलो. तुमचा संदेश मिळाला का?", "Pohochlo. Tumcha sandesh milala ka?", "I have reached. Did you get my message?"),
               D("स्नेहा", "मिळाला. मी लगेच उत्तर दिले होते.", "Milala. Mi lagech uttar dile hote.", "I got it. I had replied at once.")],
              WS("Message worksheet", [
                  T("Send the message.", ["send me a message", "let me know when you reach"],
                    ["मला संदेश पाठवा", "पोहोचल्यावर कळवा"]),
                  T("Confirm it arrived.", ["your message reached me", "reply at once"],
                    ["तुमचा संदेश मिळाला", "लगेच उत्तर द्या"]),
              ])),
            L("नंबर आणि वेळ",
              "Numbers are read digit by digit on the phone, and zero is झिरो or शून्य. Appointments "
              "are fixed with -ला (मला संध्याकाळी सहा वाजता जमेल) and changed with नंतर.",
              [V("नंबर", "number", "number", "noun"),
               V("झिरो", "zero", "zero", "noun"),
               V("जमणे", "jamne", "to work out, to suit", "verb"),
               V("नंतर", "nantar", "later, after", "adverb"),
               V("कळवणे", "kalavne", "to inform", "verb")],
              G("Numbers and appointments",
                "झिरो नऊ आठ · मला सहा वाजता जमेल · नंतर कळवते",
                "A phone number is read one digit at a time: झिरो नऊ आठ, चार पाच सहा. An "
                "appointment that suits takes जमणे with the dative मला, and a change is announced "
                "with नंतर कळवणे.",
                [X("माझा नंबर झिरो नऊ आठ चार आहे.", "Majha number zero nau aath char ahe.", "My number is zero nine eight four."),
                 X("मला संध्याकाळी सहा वाजता जमेल.", "Mala sandhyakali saha vajta jamel.", "Six in the evening will work for me."),
                 X("उद्या नंतर कळवते.", "Udya nantar kalavte.", "I will let you know tomorrow later.")],
                [("माझा नंबर झिरो नऊ आठ आहेत.", "माझा नंबर झिरो नऊ आठ आहे.", "नंबर is singular: आहे."),
                 ("मला सहा वाजता जमतो.", "मला सहा वाजता जमेल.", "An appointment for later takes जमेल.")]),
              [D("स्नेहा", "तुमचा नंबर पुन्हा सांगा.", "Tumcha number punha sanga.", "Tell me your number again."),
               D("अर्णव", "झिरो नऊ आठ, चार पाच सहा.", "Zero nau aath, char paach saha.", "Zero nine eight, four five six."),
               D("स्नेहा", "उद्या किती वाजता बोलू?", "Udya kiti vajta bolu?", "What time shall we talk tomorrow?"),
               D("अर्णव", "सात वाजता जमेल. नंतर बदल झाला तर कळवतो.", "Saat vajta jamel. Nantar badal jhala tar kalavto.", "Seven will work. If it changes later, I will let you know.")],
              WS("Number worksheet", [
                  T("Read the number.", ["zero nine eight", "my number is zero nine eight four"],
                    ["झिरो नऊ आठ", "माझा नंबर झिरो नऊ आठ चार आहे"]),
                  T("Fix a time.", ["seven will work", "I will let you know later"],
                    ["सात वाजता जमेल", "नंतर कळवतो"]),
              ])),
        ]},
        {"id": "A1+-U3", "title": "भेट आणि आमंत्रण", "lessons": [
            L("कधी भेटू या?",
              "भेटणे is to meet and वेळ काढणे is to make time. A suggestion uses -ऊ या (भेटू या, "
              "जाऊ या), and a fixed appointment takes वेळ ठरवणे.",
              [V("भेटणे", "bhetne", "to meet", "verb"),
               V("वेळ काढणे", "vel kaadhne", "to make time", "verb"),
               V("ठरवणे", "tharvne", "to fix, to decide", "verb"),
               V("जवळ", "javal", "near", "postposition"),
               V("मैदान", "maidan", "ground, field", "noun")],
              G("Suggesting a meeting",
                "भेटू या · वेळ ठरवू या · उद्या संध्याकाळी",
                "The suggestion form ends in -ऊ या and includes the person spoken to: भेटू या, "
                "जाऊ या, बोलू या. वेळ ठरवणे fixes it, and the place takes जवळ or -त: मैदानाजवळ, "
                "कॅफेत.",
                [X("उद्या संध्याकाळी भेटू या.", "Udya sandhyakali bhetu ya.", "Let us meet tomorrow evening."),
                 X("मैदानाजवळ वेळ ठरवू या.", "Maidanajaval vel tharvu ya.", "Let us fix a time near the ground."),
                 X("मी सहा वाजता वेळ काढतो.", "Mi saha vajta vel kaadhto.", "I will make time at six.")],
                [("उद्या भेटायचे आहे या.", "उद्या भेटू या.", "The suggestion is भेटू या."),
                 ("मैदान जवळ भेटू या.", "मैदानाजवळ भेटू या.", "जवळ attaches to the oblique: मैदानाजवळ.")]),
              [D("अर्णव", "कधी भेटू या?", "Kadhi bhetu ya?", "When shall we meet?"),
               D("मीरा", "उद्या संध्याकाळी जमेल का?", "Udya sandhyakali jamel ka?", "Will tomorrow evening work?"),
               D("अर्णव", "जमेल. कुठे?", "Jamel. Kuthe?", "It will. Where?"),
               D("मीरा", "मैदानाजवळ छान कॅफे आहे. तिथे सहा वाजता.", "Maidanajaval chaan cafe ahe. Tithe saha vajta.", "There is a nice cafe near the ground. There at six.")],
              WS("Meeting worksheet", [
                  T("Suggest.", ["let us meet tomorrow evening", "let us fix a time near the ground"],
                    ["उद्या संध्याकाळी भेटू या", "मैदानाजवळ वेळ ठरवू या"]),
                  T("Answer.", ["will tomorrow evening work?", "I will make time at six"],
                    ["उद्या संध्याकाळी जमेल का?", "मी सहा वाजता वेळ काढतो"]),
              ])),
            L("आज नको, उद्या",
              "A refusal in Marathi explains rather than refuses the person: आज जमत नाही, उद्या "
              "बघू. The -त नाही form states the impossibility, and पुढे ढकलणे moves it forward "
              "without closing the door.",
              [V("जमत नाही", "jamat nahi", "it does not work out", "phrase"),
               V("पुढे ढकलणे", "pudhe dhakalne", "to postpone", "verb"),
               V("दुसऱ्या दिवशी", "dusrya divshi", "on another day", "phrase"),
               V("कारण", "karan", "reason", "noun"),
               V("नक्की", "nakki", "certainly", "adverb")],
              G("Declining politely",
                "आज जमत नाही · उद्या बघू · नक्की येईन",
                "जमत नाही is the standard soft refusal and needs no pronoun. दुसऱ्या दिवशी or "
                "उद्या बघू keeps the invitation alive, and a firm acceptance is नक्की येईन or "
                "नक्की येतो.",
                [X("आज जमत नाही, काम आहे.", "Aaj jamat nahi, kaam ahe.", "Today does not work, there is work."),
                 X("उद्या बघू, चालेल का?", "Udya baghu, chalel ka?", "Let us see tomorrow, is that all right?"),
                 X("मी नक्की येईन.", "Mi nakki yein.", "I will certainly come.")],
                [("मी नाकारतो.", "आज जमत नाही.", "Marathi declines the date, not the person: जमत नाही."),
                 ("उद्या बघू नको.", "उद्या बघू.", "बघू is the inclusive suggestion; नको would refuse the person.")]),
              [D("स्नेहा", "आज संध्याकाळी भेटू या.", "Aaj sandhyakali bhetu ya.", "Let us meet this evening."),
               D("अर्णव", "आज जमत नाही, अहवालाची मुदत आहे.", "Aaj jamat nahi, ahavalachi mudat ahe.", "Today does not work, the report is due."),
               D("स्नेहा", "मग उद्या?", "Mag udya?", "Then tomorrow?"),
               D("अर्णव", "उद्या नक्की. सहा वाजता जमेल.", "Udya nakki. Saha vajta jamel.", "Tomorrow for sure. Six will work.")],
              WS("Declining worksheet", [
                  T("Decline and keep the door open.", ["today does not work", "let us see tomorrow"],
                    ["आज जमत नाही", "उद्या बघू"]),
                  T("Accept firmly.", ["I will certainly come", "will six work?"],
                    ["मी नक्की येईन", "सहा वाजता जमेल का?"]),
              ])),
            L("घरी या!",
              "Receiving a guest runs on three polite verbs: या, बसा, घ्या. The invitation is "
              "repeated once for warmth, and food is offered with स्वतःसाठी घ्या or अजून घ्या.",
              [V("स्वागत", "swagat", "welcome", "noun"),
               V("बसणे", "basne", "to sit", "verb"),
               V("घेणे", "ghene", "to take", "verb"),
               V("अजून", "ajun", "a little more, still", "adverb"),
               V("आनंद", "aanand", "joy, happiness", "noun")],
              G("Welcoming a guest",
                "या, बसा · चहा घ्या · अजून घ्या",
                "The polite imperatives are या, बसा, घ्या. Marathi offers food with घ्या rather "
                "than with want-words, and pressing for more is अजून घ्या. Pleasure is stated as "
                "मला आनंद झाला.",
                [X("या, बसा.", "Ya, basaa.", "Come in, sit down."),
                 X("चहा घ्या, थोडा गरम आहे.", "Chaha ghya, thoda garam ahe.", "Have some tea, it is a little hot."),
                 X("अजून एक घ्या.", "Ajun ek ghya.", "Take one more.")],
                [("तू ये आणि बस.", "या, बसा.", "Guests are addressed with the polite imperative in -ा."),
                 ("तुला चहा हवा आहे का?", "चहा घ्या.", "The host offers with घ्या; हवा आहे? asks the guest what they want.")]),
              [D("मीरा", "या, बसा. आज खूप गर्दी आहे.", "Ya, basaa. Aaj khup gardi ahe.", "Come, sit. There is a lot of rush today."),
               D("अर्णव", "आनंद झाला तुम्हाला भेटून.", "Aanand jhala tumhala bhetun.", "Pleased to meet you."),
               D("मीरा", "चहा घ्या, आणि थोडे पोहे आहेत.", "Chaha ghya, aani thode pohe aahet.", "Have tea, and there are some poha."),
               D("अर्णव", "आभारी आहे. अजून एक चहा घेतो.", "Aabhari ahe. Ajun ek chaha gheto.", "Thank you. I will take one more tea.")],
              WS("Guest worksheet", [
                  T("Welcome the guest.", ["come in, sit down", "have some tea"],
                    ["या, बसा", "चहा घ्या"]),
                  T("Press for more.", ["take one more", "pleased to meet you"],
                    ["अजून एक घ्या", "आनंद झाला तुम्हाला भेटून"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Pune is a Marathi city with a book in one hand and a factory in the other: the "
                 "Peshwa capital, the Deccan College, the university, and then the "
                 "automobile plants that turned it into a workshop town. The older part still runs "
                 "on पेठ and आळी — wada lanes, temple squares, and a shop for everything — while "
                 "the new city spreads out along the expressway. A Punekar will tell you, politely "
                 "and at length, why this is the best city in Maharashtra for a learner: people "
                 "still speak Marathi to strangers."),
        source_url="https://en.wikipedia.org/wiki/Pune",
        reading=("मी पुण्यात राहतो. सकाळी सात वाजता उठतो आणि आधी चहा करतो. आठ वाजता कामाला "
                 "निघतो; बसने वीस मिनिटे लागतात. दुपारी एक वाजता जेवण करतो. संध्याकाळी सहा "
                 "वाजता घरी परत येतो आणि थोडा अभ्यास करतो. रात्री मला गोष्टी वाचायला आवडते. "
                 "शनिवारी मी मैदानाजवळच्या कॅफेत मित्रांना भेटतो. आम्ही बराच वेळ बोलतो आणि "
                 "नंतर घरी जेवायला जातो. रविवारी मात्र मी उशिरा उठतो."),
        reading_gloss=("I live in Pune. I get up at seven in the morning and first make tea. At "
                       "eight I set out for work; by bus it takes twenty minutes. At one in the "
                       "afternoon I have lunch. In the evening at six I come back home and study a "
                       "little. At night I like reading stories. On Saturday I meet friends at a "
                       "cafe near the ground. We talk for a long time and then go home to eat. On "
                       "Sunday, however, I get up late."),
        listening=("मीरा: नमस्कार, काय चाललंय?<br>"
                   "अर्णव: मस्त! तू कुठे आहेस?<br>"
                   "मीरा: मैदानाजवळ. आज संध्याकाळी भेटू या.<br>"
                   "अर्णव: आज जमत नाही, अहवालाची मुदत आहे.<br>"
                   "मीरा: मग उद्या सहा वाजता, ठीक आहे.<br>"
                   "अर्णव: ठीक. मी नक्की येतो."),
        listening_gloss=("Meera: Hello, how are things? Arnav: Great! Where are you? Meera: Near the "
                         "ground. Let us meet this evening. Arnav: Today does not work, the report "
                         "is due. Meera: Then tomorrow at six, all right. Arnav: All right. I will "
                         "certainly come."),
        voice_tag=VOICE,
        idioms=[
            ("काय चाललंय?", "what is going on?", "how are things?"),
            ("मस्त", "excellent", "great, cool"),
            ("भेटू या", "let us meet", "see you, let us catch up"),
            ("वेळ काढणे", "to take out time", "to make time for somebody"),
            ("जमत नाही", "it does not join", "it does not work out"),
            ("नक्की येतो", "I come for certain", "I will be there"),
            ("थोडे थांबा", "wait a little", "hold on a moment"),
            ("लगेच कळवा", "inform at once", "let me know right away"),
            ("उशिरा उठणे", "to get up late", "to sleep in"),
            ("पोटभर", "to the stomach", "as much as one wants"),
        ],
        mistakes=[
            ("मी सहा वाजता उठते आहे.", "मी सहा वाजता उठते.", "A routine takes the simple present."),
            ("वीस मिनिटे लागतो.", "वीस मिनिटे लागतात.", "मिनिटे is plural, so लागतात."),
            ("आज भेटायचे नाही.", "आज जमत नाही.", "A polite refusal is जमत नाही, not an order."),
        ],
        task_title="Describe one working day of yours in Marathi",
        task_instructions=("Write seven Marathi sentences: the hour you get up, the tea or breakfast, "
                           "how you travel and how long it takes, what you do after dinner, what "
                           "you like doing at night, one phone call or message, and one sentence "
                           "declining something politely. Use वाजता five times and जमत नाही once."),
    ),
    "test": [
        ("translate_en", "Say: I get up at six every day.", "मी रोज सहा वाजता उठते."),
        ("translate_mr", "जेवणानंतर मी थोडा अभ्यास करतो.", "After dinner I study a little."),
        ("multiple_choice", "Which sentence offers tea to a guest?", "चहा घ्या."),
        ("fill_in_the_blank", "मला संध्याकाळी सहा वाजता ___.", "जमेल"),
        ("word_selection", "Select the Marathi for 'send me a message'.", "मला संदेश पाठवा"),
        ("error_correction", "वीस मिनिटे लागतो.", "वीस मिनिटे लागतात."),
        ("dialogue_completion", "Complete: कधी भेटू या? — ___ (tomorrow evening will work)", "उद्या संध्याकाळी जमेल"),
        ("matching", "Match नक्की to its meaning.", "certainly, for sure"),
        ("reading_comprehension", "मी बसने कामाला निघतो. — how does the speaker travel?", "by bus"),
        ("inference", "आज जमत नाही, अहवालाची मुदत आहे. — what is the speaker doing?", "declining politely and giving a reason"),
        ("main_idea", "या, बसा. चहा घ्या. — what is this?", "welcoming a guest"),
        ("detail_identification", "साडेसात वाजता काय होते?", "the speaker leaves home"),
    ],
}

HALFSTEPS["A2+"] = {
    "title": "Marathi A2+ — Bank, shop and repair",
    "native": NATIVE,
    "goals": [
        "Open an account, withdraw and deposit money, and read the slip",
        "Exchange something you bought and ask how long a repair takes",
        "Ask the way, ask for help, and follow a Marathi address",
    ],
    "units": [
        {"id": "A2+-U1", "title": "बँकेत", "lessons": [
            L("खाते उघडायचे आहे",
              "A bank form is भरायचा, a signature is सही and an identity card is ओळखपत्र. The "
              "purpose clause takes -ायचे आहे (खाते उघडायचे आहे) and the polite request ends in "
              "-ा.",
              [V("खाते", "khaate", "account", "noun"),
               V("ओळखपत्र", "olakhpatra", "identity card", "noun"),
               V("फॉर्म", "form", "form", "noun"),
               V("भरणे", "bharne", "to fill in", "verb"),
               V("सही", "sahi", "signature", "noun")],
              G("What you have come for",
                "खाते उघडायचे आहे · फॉर्म भरा · सही करा",
                "The -ायचे आहे form states what you have come to do, and it is the standard way to "
                "open a bank conversation: खाते उघडायचे आहे, पैसे काढायचे आहेत, चौकशी करायची आहे. "
                "The clerk's side uses the polite imperative in -ा.",
                [X("मला नवीन खाते उघडायचे आहे.", "Mala navin khaate ughadayche ahe.", "I want to open a new account."),
                 X("हा फॉर्म भरून द्या.", "Ha form bharun dya.", "Please fill in this form for me."),
                 X("इथे सही करा.", "Ithe sahi kara.", "Sign here.")],
                [("मी खाते उघडायचे आहे.", "मला खाते उघडायचे आहे.", "-ायचे आहे takes the dative मला, not the nominative मी."),
                 ("मला खाते उघडतो.", "मला खाते उघडायचे आहे.", "A purpose in a bank takes -ायचे आहे.")]),
              [D("ग्राहक", "मला नवीन खाते उघडायचे आहे.", "Mala navin khaate ughadayche ahe.", "I want to open a new account."),
               D("क्लर्क", "ओळखपत्र आहे का? मोबाइल नंबर द्या.", "Olakhpatra ahe ka? Mobile number dya.", "Is there an identity card? Give me a mobile number."),
               D("ग्राहक", "हा आहे. पत्ता पुरावा लागतो का?", "Ha ahe. Patta purava lagto ka?", "Here it is. Is proof of address needed?"),
               D("क्लर्क", "हो. हा फॉर्म भरा आणि दोन ठिकाणी सही करा.", "Ho. Ha form bhara aani don thikani sahi kara.", "Yes. Fill in this form and sign in two places.")],
              WS("Bank worksheet", [
                  T("State your purpose.", ["I want to open a new account", "I want to withdraw money"],
                    ["मला नवीन खाते उघडायचे आहे", "मला पैसे काढायचे आहेत"]),
                  T("Follow the instruction.", ["sign here", "fill in this form"],
                    ["इथे सही करा", "हा फॉर्म भरा"]),
              ])),
            L("पैसे काढायचे आहेत",
              "काढणे withdraws and जमा करणे deposits; the amount is रक्कम and the receipt पावती. "
              "The amount takes the plural verb (पैसे काढायचे आहेत), and शिल्लक is the balance.",
              [V("रक्कम", "rakkam", "amount", "noun"),
               V("जमा करणे", "jama karne", "to deposit", "verb"),
               V("पावती", "pavti", "receipt", "noun"),
               V("शिल्लक", "shillak", "balance", "noun"),
               V("रुपये", "rupaye", "rupees", "noun")],
              G("Amounts and slips",
                "दोन हजार रुपये काढायचे आहेत · शिल्लक सांगा · पावती घ्या",
                "The amount stands before rupees and the verb agrees with रुपये: दोन हजार रुपये "
                "काढायचे आहेत. The balance takes शिल्लक, and a receipt is घेतली rather than दिली "
                "from the customer's side.",
                [X("मला दोन हजार रुपये काढायचे आहेत.", "Mala don hajar rupaye kaadhayche aahet.", "I want to withdraw two thousand rupees."),
                 X("पाचशे रुपये जमा करायचे आहेत.", "Paanshe rupaye jama karayche aahet.", "Five hundred rupees are to be deposited."),
                 X("शिल्लक किती आहे?", "Shillak kiti ahe?", "What is the balance?")],
                [("मला दोन हजार रुपये काढायचा आहे.", "मला दोन हजार रुपये काढायचे आहेत.", "रुपये is plural: काढायचे आहेत."),
                 ("शिल्लक आहेत.", "शिल्लक आहे.", "शिल्लक is singular feminine: आहे.")]),
              [D("ग्राहक", "मला दोन हजार रुपये काढायचे आहेत.", "Mala don hajar rupaye kaadhayche aahet.", "I want to withdraw two thousand rupees."),
               D("क्लर्क", "पासबुक किंवा कार्ड आहे?", "Passbook kinva card ahe?", "Is there a passbook or a card?"),
               D("ग्राहक", "कार्ड आहे. शिल्लक सांगा.", "Card ahe. Shillak sanga.", "I have a card. Tell me the balance."),
               D("क्लर्क", "बारा हजार. पावती घ्या आणि मोजून घ्या.", "Bara hajar. Pavti ghya aani mojun ghya.", "Twelve thousand. Take the receipt and count it.")],
              WS("Money worksheet", [
                  T("Say the amount.", ["I want to withdraw two thousand rupees", "five hundred rupees are to be deposited"],
                    ["मला दोन हजार रुपये काढायचे आहेत", "पाचशे रुपये जमा करायचे आहेत"]),
                  T("Ask and check.", ["what is the balance?", "take the receipt"],
                    ["शिल्लक किती आहे?", "पावती घ्या"]),
              ])),
            L("रांग आणि क्रमांक",
              "A queue is रांग and a token is क्रमांक. Taking a turn is क्रमांक घेणे, and the "
              "counter is काउंटर with -वर for on it. Waiting politely uses थोडे.",
              [V("रांग", "raang", "queue", "noun"),
               V("क्रमांक", "kramank", "number, token", "noun"),
               V("काउंटर", "counter", "counter", "noun"),
               V("थोडे", "thode", "a little", "adverb"),
               V("बोलावणे", "bolavne", "to call", "verb")],
              G("Waiting your turn",
                "क्रमांक घ्या · काउंटर तीनवर जा · तुमचा क्रमांक आला",
                "The token takes घेणे and the counter takes -वर: काउंटर तीनवर जा. One's turn arrives "
                "with येणे (क्रमांक आला), and the staff call a person with बोलावणे.",
                [X("आधी क्रमांक घ्या.", "Aadhi kramank ghya.", "Take a number first."),
                 X("काउंटर चारवर जा.", "Counter charvar ja.", "Go to counter four."),
                 X("माझा क्रमांक कधी येईल?", "Majha kramank kadhi yeil?", "When will my number come?")],
                [("काउंटर चारला जा.", "काउंटर चारवर जा.", "A counter takes -वर: चारवर."),
                 ("रांग आहेत.", "रांग आहे.", "रांग is singular feminine: आहे.")]),
              [D("ग्राहक", "रांग खूप लांब आहे.", "Raang khup laamb ahe.", "The queue is very long."),
               D("क्लर्क", "आधी क्रमांक घ्या, मग काउंटर दोनवर या.", "Aadhi kramank ghya, mag counter don-var ya.", "Take a number first, then come to counter two."),
               D("ग्राहक", "किती वेळ लागेल?", "Kiti vel lagel?", "How long will it take?"),
               D("क्लर्क", "वीस मिनिटे. तुमचा क्रमांक आला की बोलावतो.", "Vis minute. Tumcha kramank ala ki bolavto.", "Twenty minutes. When your number comes up I will call you.")],
              WS("Queue worksheet", [
                  T("Take your turn.", ["take a number first", "go to counter four"],
                    ["आधी क्रमांक घ्या", "काउंटर चारवर जा"]),
                  T("Ask about the wait.", ["how long will it take?", "when will my number come?"],
                    ["किती वेळ लागेल?", "माझा क्रमांक कधी येईल?"]),
              ])),
        ]},
        {"id": "A2+-U2", "title": "दुकान आणि दुरुस्ती", "lessons": [
            L("ही वस्तू बदलायची आहे",
              "An exchange is बदलणे and it needs the bill: बिल दाखवा. A warranty is हमी, and a "
              "thing that does not work is चालत नाही.",
              [V("बिल", "bil", "bill", "noun"),
               V("हमी", "hami", "guarantee, warranty", "noun"),
               V("चालणे", "chaalne", "to work, to run", "verb"),
               V("दाखवणे", "dakhavne", "to show", "verb"),
               V("नवीन", "navin", "new", "adjective")],
              G("Exchanging a purchase",
                "हे चालत नाही · बिल दाखवा · बदलून द्या",
                "The defect is reported plainly (हे चालत नाही, आवाज येतो), the bill is asked for "
                "with दाखवा, and the remedy with बदलून द्या or दुरुस्त करून द्या. हमी covers the "
                "period, so हमी आहे का? is the first question to ask.",
                [X("हे चालत नाही, बदलायचे आहे.", "He chaalat nahi, badlayche ahe.", "This does not work, I want to exchange it."),
                 X("बिल दाखवू का?", "Bil dakhavu ka?", "Shall I show the bill?"),
                 X("हमी आहे का?", "Hami ahe ka?", "Is there a warranty?")],
                [("हे चालत नाहीत.", "हे चालत नाही.", "A single object takes नाही."),
                 ("बिल दाखवतो.", "बिल दाखवा.", "The polite imperative ends in -ा: दाखवा.")]),
              [D("ग्राहक", "हे मशीन चालत नाही.", "He machine chaalat nahi.", "This machine does not work."),
               D("विक्रेता", "बिल आहे का? आणि हमी कार्ड?", "Bil ahe ka? Aani hami card?", "Is there a bill? And the warranty card?"),
               D("ग्राहक", "दोन्ही आहेत. बदलायचे आहे.", "Donhi aahet. Badlayche ahe.", "Both are there. I want to exchange it."),
               D("विक्रेता", "बदलून देतो, पण तोच मॉडेल आहे का ते पाहा.", "Badlun deto, pan toch model ahe ka te paha.", "I will exchange it, but see whether that model is in stock.")],
              WS("Exchange worksheet", [
                  T("Report the defect.", ["this does not work", "is there a warranty?"],
                    ["हे चालत नाही", "हमी आहे का?"]),
                  T("Ask for the exchange.", ["I want to exchange it", "here is the bill"],
                    ["बदलायचे आहे", "हा बिल आहे"]),
              ])),
            L("दुरुस्ती किती दिवसांत?",
              "A repair takes the time phrase दोन दिवसांत or आठवड्यात, and तयार होणे is to be "
              "ready. Handing the item over is देणे, and collecting it is घेणे.",
              [V("दुरुस्त", "durust", "repaired, in order", "adjective"),
               V("तयार", "tayar", "ready", "adjective"),
               V("आठवडा", "aathvada", "week", "noun"),
               V("सोडणे", "sodne", "to leave behind", "verb"),
               V("तपासणी", "tapasni", "checking, inspection", "noun")],
              G("How long the repair takes",
                "दोन दिवसांत तयार होईल · इथे सोडा · तपासणी करा",
                "The time within which something is done takes -त: दोन दिवसांत, एका आठवड्यात. "
                "तयार होणे is the verb for being ready, and the shop's own step is तपासणी — a word "
                "worth knowing before you agree to anything.",
                [X("दोन दिवसांत तयार होईल का?", "Don divsant tayar hoil ka?", "Will it be ready in two days?"),
                 X("मी इथे सोडतो का?", "Mi ithe sodto ka?", "Shall I leave it here?"),
                 X("आधी तपासणी करा.", "Aadhi tapasni kara.", "Check it first.")],
                [("दोन दिवसात तयार होईल.", "दोन दिवसांत तयार होईल.", "A deadline in the future takes -ांत: दिवसांत."),
                 ("दोन दिवसांत तयार आहे.", "दोन दिवसांत तयार होईल.", "A future deadline takes होईल, not आहे.")]),
              [D("ग्राहक", "दुरुस्ती किती दिवसांत होईल?", "Durusti kiti divsant hoil?", "In how many days will the repair be done?"),
               D("तंत्रज्ञ", "आधी तपासणी करतो. बहुतेक तीन दिवस.", "Aadhi tapasni karto. Bahutek teen divas.", "I will check first. Probably three days."),
               D("ग्राहक", "मी इथे सोडतो का?", "Mi ithe sodto ka?", "Shall I leave it here?"),
               D("तंत्रज्ञ", "हो, पावती घ्या. तयार झाले की फोन करतो.", "Ho, pavti ghya. Tayar jhale ki phone karto.", "Yes, take the receipt. I will call when it is ready.")],
              WS("Repair worksheet", [
                  T("Ask about the time.", ["will it be ready in two days?", "in how many days will the repair be done?"],
                    ["दोन दिवसांत तयार होईल का?", "दुरुस्ती किती दिवसांत होईल?"]),
                  T("Leave it and collect it.", ["shall I leave it here?", "the checking comes first"],
                    ["मी इथे सोडतो का?", "आधी तपासणी करा"]),
              ])),
            L("घरातली दुरुस्ती",
              "A plumber is a प्लंबर or कारागीर, and the words are नळ, गळणे, बसवणे, बंद पडणे. The "
              "causal बसवणे (to have something fitted) is different from बसणे (to sit).",
              [V("नळ", "nal", "tap", "noun"),
               V("गळणे", "galne", "to leak", "verb"),
               V("बसवणे", "basavne", "to get something fitted", "verb"),
               V("बंद पडणे", "band padne", "to stop working", "verb"),
               V("कारागीर", "karagir", "craftsman, technician", "noun")],
              G("Getting something fitted",
                "नळ गळत आहे · दिवा बंद पडला · नवीन नळ बसवा",
                "गळणे and बंद पडणे describe the fault, and बसवणे is the causative: you have "
                "something fitted. The progressive गळत आहे or the perfect पडला places the fault in "
                "time, which a कारागीर will ask about first.",
                [X("स्वयंपाकघरातला नळ गळत आहे.", "Svayampakgharatla nal galat ahe.", "The kitchen tap is leaking."),
                 X("दिवा बंद पडला.", "Diva band padla.", "The lamp has stopped working."),
                 X("नवीन नळ बसवायचा आहे.", "Navin nal basvaycha ahe.", "A new tap is to be fitted.")],
                [("नळ गळतो आहे.", "नळ गळत आहे.", "The progressive takes the -त stem: गळत आहे, not गळतो आहे."),
                 ("मी नळ बसतो.", "मी नळ बसवतो.", "Getting it fitted is बसवणे, not बसणे.")]),
              [D("ग्राहक", "स्वयंपाकघरातला नळ गळत आहे. कारागीर पाठवा.", "Svayampakgharatla nal galat ahe. Karagir paathva.", "The kitchen tap is leaking. Send a technician."),
               D("कारागीर", "कधीपासून?", "Kadhipasun?", "Since when?"),
               D("ग्राहक", "दोन दिवसांपासून. आणि एक दिवा बंद पडला आहे.", "Don divsanpasun. Aani ek diva band padla ahe.", "Since two days. And one lamp has stopped working."),
               D("कारागीर", "नळ बदलावा लागेल. उद्या सकाळी येतो.", "Nal badlava lagel. Udya sakali yeto.", "The tap will have to be replaced. I will come tomorrow morning.")],
              WS("Household worksheet", [
                  T("Describe the fault.", ["the tap is leaking", "the lamp has stopped working"],
                    ["नळ गळत आहे", "दिवा बंद पडला"]),
                  T("Ask for the work.", ["a technician should be sent", "a new tap is to be fitted"],
                    ["कारागीर पाठवा", "नवीन नळ बसवायचा आहे"]),
              ])),
        ]},
        {"id": "A2+-U3", "title": "मदत आणि रस्ता", "lessons": [
            L("रस्ता विचारणे",
              "Directions run on सरळ, डावे, उजवे and the landmark: पुलापुढे, चौकात. The question "
              "is कसे जायचे? or कुठे आहे?, and the distance is जवळ or लांब.",
              [V("सरळ", "saral", "straight", "adverb"),
               V("डावे", "daave", "left", "adjective"),
               V("उजवे", "ujve", "right", "adjective"),
               V("चौक", "chauk", "crossing, square", "noun"),
               V("पूल", "pul", "bridge", "noun")],
              G("Asking the way",
                "सरळ जा · डावे वळा · पुलापुढे आहे",
                "Directions use the polite imperative: जा, वळा, उतरा. A landmark takes -पुढे, "
                "-मागे or -जवळ (पुलापुढे, चौकाजवळ), and the question is कुठे आहे? or कसे जायचे?",
                [X("स्टेशन कुठे आहे?", "Station kuthe ahe?", "Where is the station?"),
                 X("सरळ जा, मग डावे वळा.", "Saral ja, mag daave vala.", "Go straight, then turn left."),
                 X("पुलापुढे बस थांबा आहे.", "Pulapudhe bas thaamba ahe.", "There is a bus stop before the bridge.")],
                [("स्टेशन कुठे आहेत?", "स्टेशन कुठे आहे?", "स्टेशन is singular: आहे."),
                 ("डावा वळा.", "डावे वळा.", "वळा takes the neuter डावे in a direction.")]),
              [D("प्रवासी", "स्टेशन कसे जायचे?", "Station kase jaayche?", "How do I get to the station?"),
               D("स्थानिक", "सरळ जा, चौकात डावे वळा.", "Saral ja, chaukat daave vala.", "Go straight, turn left at the crossing."),
               D("प्रवासी", "लांब आहे का?", "Laamb ahe ka?", "Is it far?"),
               D("स्थानिक", "नाही, पुलापुढे दहा मिनिटांचा रस्ता आहे.", "Nahi, pulapudhe daha minutincha rasta ahe.", "No, it is a ten-minute walk before the bridge.")],
              WS("Directions worksheet", [
                  T("Ask the way.", ["where is the station?", "how do I get to the market?"],
                    ["स्टेशन कुठे आहे?", "बाजार कसे जायचे?"]),
                  T("Give the way.", ["go straight, then turn left", "it is before the bridge"],
                    ["सरळ जा, मग डावे वळा", "पुलापुढे आहे"]),
              ])),
            L("मदत मागणे",
              "Asking for help opens with त्रास दिल्याबद्दल माफ करा or एक मदत हवी आहे, and closes "
              "with धन्यवाद. The person helping answers हरकत नाही (no trouble).",
              [V("मदत", "madat", "help", "noun"),
               V("त्रास", "tras", "trouble", "noun"),
               V("हरकत नाही", "harkat nahi", "no problem", "phrase"),
               V("घेणे", "ghene", "to carry, to take", "verb"),
               V("उचलणे", "uchalne", "to lift", "verb")],
              G("Asking for help",
                "एक मदत हवी आहे · हे उचलायला मदत करा · हरकत नाही",
                "हवी आहे states what you need and is politer than an imperative. मदत करा asks for "
                "the action, and the answer हरकत नाही removes the apology. त्रास is the word for "
                "the trouble you fear you are causing.",
                [X("एक मदत हवी आहे.", "Ek madat havi ahe.", "I need a bit of help."),
                 X("हे उचलायला मदत करा.", "He uchlayla madat kara.", "Help me lift this."),
                 X("त्रास दिल्याबद्दल माफ करा.", "Traas dilyabaddal maaf kara.", "Sorry for the trouble.")],
                [("मला मदत कर.", "मला मदत करा.", "A stranger is addressed with the -ा imperative."),
                 ("त्रास झाला माफ करा.", "त्रास दिल्याबद्दल माफ करा.", "The apology takes दिल्याबद्दल: for the trouble given.")]),
              [D("प्रवासी", "एक मदत हवी आहे. हे बॅग उचलायला मदत करा.", "Ek madat havi ahe. He bag uchlayla madat kara.", "I need a bit of help. Help me lift this bag."),
               D("स्थानिक", "अगदी, हरकत नाही.", "Agadi, harkat nahi.", "Of course, no trouble."),
               D("प्रवासी", "खूप धन्यवाद. त्रास दिला.", "Khup dhanyavad. Traas dila.", "Many thanks. I gave you trouble."),
               D("स्थानिक", "काही नाही. स्टेशनकडे जायचे आहे का?", "Kahi nahi. Station-kade jaayche ahe ka?", "Not at all. Are you going towards the station?")],
              WS("Help worksheet", [
                  T("Ask for help.", ["I need a bit of help", "help me lift this"],
                    ["एक मदत हवी आहे", "हे उचलायला मदत करा"]),
                  T("Apologise and answer.", ["sorry for the trouble", "no trouble at all"],
                    ["त्रास दिल्याबद्दल माफ करा", "हरकत नाही"]),
              ])),
            L("पत्ता आणि खूण",
              "An address runs from the small unit to the large: घर क्रमांक, गल्ली, परिसर, शहर. A "
              "landmark is खूण, and the near-far pair is जवळ/लांब or इथून/तिथून.",
              [V("पत्ता", "patta", "address", "noun"),
               V("गल्ली", "galli", "lane", "noun"),
               V("खूण", "khun", "landmark, mark", "noun"),
               V("परिसर", "parisar", "locality", "noun"),
               V("इथून", "ithun", "from here", "adverb")],
              G("Giving an address",
                "घर क्रमांक सात · शिवाजी गल्ली · मंदिराजवळ",
                "A Marathi address climbs from the number to the locality: घर क्रमांक, गल्ली, "
                "परिसर, शहर. A landmark takes जवळ or समोर (मंदिराजवळ, दुकानासमोर), and a distance "
                "from a point takes -तून: इथून दोन गल्ल्या.",
                [X("घर क्रमांक सात, शिवाजी गल्ली.", "Ghar kramank saat, Shivaji galli.", "House number seven, Shivaji lane."),
                 X("मंदिराजवळ आहे.", "Mandirajaval ahe.", "It is near the temple."),
                 X("इथून दोन गल्ल्या पुढे.", "Ithun don gallya pudhe.", "Two lanes ahead of here.")],
                [("घर क्रमांक सात गल्ली शिवाजी.", "घर क्रमांक सात, शिवाजी गल्ली.", "The address climbs from the number to the lane."),
                 ("मंदिर जवळ आहे.", "मंदिराजवळ आहे.", "जवळ attaches to the oblique: मंदिराजवळ.")]),
              [D("पोस्टमन", "पत्ता सांगा.", "Patta sanga.", "Tell me the address."),
               D("रहिवासी", "घर क्रमांक सात, शिवाजी गल्ली, मंदिराजवळ.", "Ghar kramank saat, Shivaji galli, mandirajaval.", "House number seven, Shivaji lane, near the temple."),
               D("पोस्टमन", "खूण काय आहे?", "Khun kay ahe?", "What is the landmark?"),
               D("रहिवासी", "दुकानासमोरचा निळा दरवाजा. इथून दोन गल्ल्या पुढे.", "Dukanasamorcha nila darvaja. Ithun don gallya pudhe.", "The blue door opposite the shop. Two lanes ahead of here.")],
              WS("Address worksheet", [
                  T("Give the address.", ["house number seven, Shivaji lane", "near the temple"],
                    ["घर क्रमांक सात, शिवाजी गल्ली", "मंदिराजवळ"]),
                  T("Give the landmark.", ["opposite the shop", "two lanes from here"],
                    ["दुकानासमोर", "इथून दोन गल्ल्या"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Mumbai speaks Marathi in at least three accents before breakfast: the city "
                 "Marathi of Girgaon and Lalbaug, the Konkani-flavoured Marathi of the coastal "
                 "families, and the Marathi of the lakhs who came in from the Deccan and Vidarbha. "
                 "Local trains run the day — 7.5 million people a day on the suburban lines — and "
                 "the city's Marathi has taken aboard Hindi, English and every other language of "
                 "the street. A learner hears it most clearly in the market and on the platform, "
                 "not in the office."),
        source_url="https://en.wikipedia.org/wiki/Mumbai",
        reading=("आज सकाळी मला बँकेत जायचे होते. रांग खूप लांब होती, म्हणून आधी क्रमांक "
                 "घेतला. काउंटर दोनवर क्लर्कने फॉर्म दिला आणि दोन ठिकाणी सही करायला सांगितले. "
                 "मी दोन हजार रुपये काढले आणि पावती घेतली. नंतर बाजारात गेलो. एक "
                 "ग्राहक म्हणाला, 'हे मशीन चालत नाही, बदलून द्या.' बिल आणि हमी कार्ड "
                 "दोन्ही होते, म्हणून दुकानदाराने लगेच बदलून दिले. परतीच्या रस्त्यावर "
                 "एका माणसाने रस्ता विचारला आणि मी सरळ, चौकात डावे — असे सांगितले."),
        reading_gloss=("This morning I had to go to the bank. The queue was very long, so I took a "
                       "number first. At counter two the clerk gave me the form and told me to "
                       "sign in two places. I withdrew two thousand rupees and took the receipt. "
                       "Then I went to the market. A customer was saying, 'This machine does not "
                       "work, exchange it.' The bill and the warranty card were both there, so the "
                       "shopkeeper exchanged it at once. On the way back a man asked me the way, "
                       "and I said: straight, then left at the crossing."),
        listening=("क्लर्क: पुढचा. काय करायचे आहे?<br>"
                   "ग्राहक: पैसे काढायचे आहेत, दोन हजार.<br>"
                   "क्लर्क: कार्ड द्या. आणि हा फॉर्म भरा.<br>"
                   "ग्राहक: शिल्लक किती आहे?<br>"
                   "क्लर्क: बारा हजार रुपये. मोजून घ्या आणि पावती ठेवा."),
        listening_gloss=("Clerk: Next. What is to be done? Customer: I want to withdraw money, two "
                         "thousand. Clerk: Give me the card. And fill in this form. Customer: What "
                         "is the balance? Clerk: Twelve thousand rupees. Count it and keep the "
                         "receipt."),
        voice_tag=VOICE,
        idioms=[
            ("त्रास दिल्याबद्दल माफ करा", "forgive me for giving trouble", "sorry to trouble you"),
            ("हरकत नाही", "there is no objection", "no trouble at all"),
            ("आधी क्रमांक घ्या", "take the number first", "wait your turn"),
            ("बिल दाखवा", "show the bill", "the purchase is being checked"),
            ("दुरुस्त करून द्या", "get it repaired for me", "the shop must fix it"),
            ("सरळ जा", "go straight", "keep going without turning"),
            ("चौकात डावे वळा", "turn left at the crossing", "the turning point"),
            ("इथून जवळच", "close to here", "a short distance away"),
            ("मोजून घ्या", "count and take", "check the money before you leave"),
            ("काही नाही", "it is nothing", "don't mention it"),
        ],
        mistakes=[
            ("मला दोन हजार रुपये काढायचा आहे.", "मला दोन हजार रुपये काढायचे आहेत.", "रुपये is plural: काढायचे आहेत."),
            ("मी नळ बसतो.", "मी नळ बसवतो.", "Getting it fitted is बसवणे, not बसणे."),
            ("मंदिर जवळ आहे.", "मंदिराजवळ आहे.", "जवळ attaches to the oblique: मंदिराजवळ."),
        ],
        task_title="Do one errand in Marathi on paper",
        task_instructions=("Write a six-line Marathi dialogue for one errand of your choice: at the "
                           "bank, at a shop with a faulty purchase, or asking the way. State the "
                           "purpose with -ायचे आहे, ask one question, answer one question, and close "
                           "with धन्यवाद or हरकत नाही."),
    ),
    "test": [
        ("translate_en", "Say: I want to withdraw two thousand rupees.", "मला दोन हजार रुपये काढायचे आहेत."),
        ("translate_mr", "दोन दिवसांत तयार होईल का?", "Will it be ready in two days?"),
        ("multiple_choice", "Which sentence asks for the way?", "स्टेशन कुठे आहे?"),
        ("fill_in_the_blank", "इथे ___ करा.", "सही"),
        ("word_selection", "Select the Marathi for 'no trouble at all'.", "हरकत नाही"),
        ("error_correction", "दोन दिवसात तयार होईल.", "दोन दिवसांत तयार होईल."),
        ("dialogue_completion", "Complete: ___ (help me lift this bag) — अगदी, हरकत नाही.", "हे बॅग उचलायला मदत करा"),
        ("matching", "Match पावती to its meaning.", "receipt"),
        ("reading_comprehension", "शिल्लक किती आहे? — what does the clerk answer?", "twelve thousand rupees"),
        ("inference", "हे चालत नाही, बदलायचे आहे. — what does the speaker want?", "an exchange of the item"),
        ("main_idea", "बिल आणि हमी कार्ड दोन्ही होते. — why does the exchange succeed?", "the purchase was documented"),
        ("detail_identification", "कारागीर कधी येईल?", "in the morning tomorrow"),
    ],
}

HALFSTEPS["B1+"] = {
    "title": "Marathi B1+ — Meetings that decide something",
    "native": NATIVE,
    "goals": [
        "Put an item on the agenda and state your opinion without heat",
        "Take a responsibility, report progress, and name an obstacle",
        "Keep the minutes, announce the decision, and review the result",
    ],
    "units": [
        {"id": "B1+-U1", "title": "बैठकीत", "lessons": [
            L("कार्यसूची ठरवणे",
              "An agenda is कार्यसूची and the items on it are मुद्दे. A meeting opens with "
              "अध्यक्ष, moves item by item with हा मुद्दा, and closes with other matters — अन्य "
              "विषय. Pinning the agenda uses ठरवणे or मांडणे.",
              [V("कार्यसूची", "karyasuchi", "agenda", "noun"),
               V("मुद्दा", "mudda", "item, point", "noun"),
               V("अध्यक्ष", "adhyaksh", "chairperson", "noun"),
               V("मांडणे", "maandne", "to put forward", "verb"),
               V("अन्य", "anya", "other", "adjective")],
              G("Putting an item on the agenda",
                "कार्यसूचीत … मांडतो · हा मुद्दा तिसरा आहे · अन्य विषय",
                "An item goes on the agenda with मांडणे: कार्यसूचीत हा मुद्दा मांडतो. Items are "
                "counted with पहिला, दुसरा (मुद्दा is masculine), and other business is अन्य "
                "विषय. The chairperson's role is stated with अध्यक्षता: अध्यक्षता … करतात.",
                [X("कार्यसूचीत पहिला मुद्दा तुमचा आहे.", "Karyasuchit pahila mudda tumcha ahe.", "The first item on the agenda is yours."),
                 X("मी हा मुद्दा बैठकीत मांडतो.", "Mi ha mudda baithkit maandto.", "I am putting this item before the meeting."),
                 X("अन्य विषयासाठी शेवटी वेळ ठेवला आहे.", "Anya vishayasathi shevti vel thevla ahe.", "Time is kept at the end for other matters.")],
                [("कार्यसूचीत पहिला मुद्दा तुमची आहे.", "कार्यसूचीत पहिला मुद्दा तुमचा आहे.", "मुद्दा is masculine: तुमचा."),
                 ("मी मुद्दा मांडतो आहे.", "मी मुद्दा मांडतो.", "A statement of intent takes the simple present here.")]),
              [D("अध्यक्ष", "आजची कार्यसूची वाचा.", "Aajchi karyasuchi vaacha.", "Read today's agenda."),
               D("सचिव", "पहिला मुद्दा अंदाजपत्रक, दुसरा मुद्दा वेळापत्रक.", "Pahila mudda andajpatrak, dusra mudda velapatrak.", "The first item is the budget, the second the schedule."),
               D("अध्यक्ष", "वेळापत्रकाचा मुद्दा पुढे ढकलू या का?", "Velapatrakacha mudda pudhe dhakalu ya ka?", "Shall we move the schedule item later?"),
               D("सचिव", "ठीक, मग तो शेवटी अन्य विषयात घेऊ.", "Thik, mag to shevti anya vishayat gheu.", "All right, then we will take it at the end among other matters.")],
              WS("Agenda worksheet", [
                  T("Set the agenda.", ["the first item is yours", "I am putting this item before the meeting"],
                    ["पहिला मुद्दा तुमचा आहे", "मी हा मुद्दा बैठकीत मांडतो"]),
                  T("Move an item.", ["shall we move the schedule item later?", "we will take it at the end"],
                    ["वेळापत्रकाचा मुद्दा पुढे ढकलू या का?", "शेवटी घेऊ"]),
              ])),
            L("मत मांडणे आणि आक्षेप",
              "Opinions open with माझ्या मते or मला वाटते, agreement with सहमत आहे and objection "
              "with आक्षेप आहे or हरकत आहे. मत is neuter, हरकत is feminine, and मुद्दा is masculine "
              "— agreement follows the noun.",
              [V("मत", "mat", "opinion, vote", "noun"),
               V("सहमत", "sahmat", "agreeing", "adjective"),
               V("आक्षेप", "aakshep", "objection", "noun"),
               V("हरकत", "harkat", "objection, cavil", "noun"),
               V("सूचना", "suchana", "suggestion", "noun")],
              G("Opinions and objections",
                "माझ्या मते · मी सहमत आहे · मला आक्षेप आहे",
                "माझ्या मते is the neutral opener, मी सहमत आहे agrees, and आक्षेप आहे objects "
                "while staying impersonal: the objection is attached to the point, not the person. "
                "A suggestion is offered with सूचना देते/देतो, and दुसरे मत is the other view.",
                [X("माझ्या मते वेळापत्रक बदलावे.", "Majhya mate velapatrak badlave.", "In my opinion the schedule should be changed."),
                 X("या मुद्द्यावर मला आक्षेप आहे.", "Ya muddyavar mala aakshep ahe.", "I have an objection on this point."),
                 X("मी एक सूचना देतो.", "Mi ek suchana deto.", "I have a suggestion.")],
                [("माझ्या मताने वेळापत्रक बदलावे.", "माझ्या मते वेळापत्रक बदलावे.", "The fixed phrase is माझ्या मते."),
                 ("मी तुम्हाला सहमत आहे.", "मी तुमच्याशी सहमत आहे.", "Agreement takes -शी: तुमच्याशी सहमत आहे.")]),
              [D("अध्यक्ष", "वेळापत्रकाबद्दल प्रत्येकाचे मत सांगा.", "Velapatrakabaddal pratyekache mat sanga.", "Everyone state your opinion about the schedule."),
               D("सदस्य १", "माझ्या मते काम दोन टप्प्यांत व्हावे.", "Majhya mate kaam don tappyant vhave.", "In my opinion the work should be in two stages."),
               D("सदस्य २", "मला तत्त्व सहमत आहे, पण दुसऱ्या टप्प्यावर आक्षेप आहे.", "Mala tattva sahmat ahe, pan dusrya tappyavar aakshep ahe.", "I agree in principle, but I object to the second stage."),
               D("अध्यक्ष", "ठीक, दुसरा टप्पा आधी तपासून ठरवू.", "Thik, dusra tappa aadhi tapasun tharvu.", "All right, we will decide the second stage after checking.")],
              WS("Opinion worksheet", [
                  T("Give an opinion.", ["in my opinion the work should be in two stages", "I agree in principle"],
                    ["माझ्या मते काम दोन टप्प्यांत व्हावे", "तत्त्व सहमत आहे"]),
                  T("Object politely.", ["I have an objection on this point", "I have a suggestion"],
                    ["या मुद्द्यावर मला आक्षेप आहे", "मी एक सूचना देतो"]),
              ])),
            L("सारांश आणि ठराव",
              "A summary is सारांश and a resolution ठराव. समजले/ठरले states what was decided, "
              "and the minutes are नोंदी. The resolution takes होणे (ठराव झाला), not करणे.",
              [V("सारांश", "saraansh", "summary", "noun"),
               V("ठराव", "tharav", "resolution", "noun"),
               V("ठरले", "tharale", "it was decided", "verb"),
               V("नोंद", "nond", "note, record", "noun"),
               V("थोडक्यात", "thodakyat", "in short", "adverb")],
              G("Summing up",
                "थोडक्यात · ठराव झाला · नोंदी ठेवा",
                "थोडक्यात opens the summary and ठरले की … closes it. A resolution is झाला "
                "(ठराव झाला) and the record is ठेवली (नोंद ठेवली). सारांश is masculine, and the "
                "conclusion is stated before the thanks.",
                [X("थोडक्यात, दोन टप्पे ठरले.", "Thodakyat, don tappe tharale.", "In short, two stages were decided."),
                 X("ठराव सर्वांनी मान्य केला.", "Tharav sarvanni manya kela.", "Everyone accepted the resolution."),
                 X("सचिव नोंदी ठेवतात.", "Sachiv nondi thevtaat.", "The secretary keeps the minutes.")],
                [("ठराव झाले.", "ठराव झाला.", "ठराव is masculine singular: झाला."),
                 ("नोंद ठेवला.", "नोंद ठेवली.", "नोंद is feminine: ठेवली.")]),
              [D("अध्यक्ष", "बैठकीचा सारांश द्या.", "Baithkicha saraansh dya.", "Give the summary of the meeting."),
               D("सचिव", "थोडक्यात: दोन टप्पे ठरले, दुसऱ्याची तपासणी पुढे.", "Thodakyat: don tappe tharale, dusryachi tapasni pudhe.", "In short: two stages were decided, the second is to be checked later."),
               D("अध्यक्ष", "ठराव सर्वांनी मान्य केला का?", "Tharav sarvanni manya kela ka?", "Did everyone accept the resolution?"),
               D("सचिव", "हो, एक अनुपस्थित. नोंदी मी ठेवतो.", "Ho, ek anupasthit. Nondi mi thevto.", "Yes, one absent. I keep the minutes.")],
              WS("Summary worksheet", [
                  T("Summarise.", ["in short, two stages were decided", "everyone accepted the resolution"],
                    ["थोडक्यात, दोन टप्पे ठरले", "ठराव सर्वांनी मान्य केला"]),
                  T("Keep the record.", ["the secretary keeps the minutes", "the second stage is to be checked"],
                    ["सचिव नोंदी ठेवतात", "दुसऱ्याची तपासणी पुढे"]),
              ])),
        ]},
        {"id": "B1+-U2", "title": "कामाचे नियोजन", "lessons": [
            L("जबाबदारी आणि मुदत",
              "Work is divided with वाटणी, responsibility is जबाबदारी (feminine) and a deadline "
              "मुदत (feminine). The future takes -ईल/-ईन: ती जबाबदारी घेईल, मी घेईन. A deadline is dated with "
              "-पर्यंत and the part still to come is उरलेले काम.",
              [V("जबाबदारी", "jababdaari", "responsibility", "noun"),
               V("मुदत", "mudat", "deadline, term", "noun"),
               V("वाटणी", "vaatni", "division, sharing", "noun"),
               V("पूर्ण", "purn", "complete", "adjective"),
               V("उरलेले", "uralele", "that which remains", "adjective")],
              G("Who does what by when",
                "मी ही जबाबदारी घेईन · मुदत शुक्रवारपर्यंत · उरलेले काम",
                "जबाबदारी घेणे is to take on the work, and it takes the future: घेईन (I), घेईल "
                "(he/she), घेतील (they). A deadline ends in -पर्यंत (शुक्रवारपर्यंत), and the part "
                "still to come is उरलेले काम.",
                [X("मी ही जबाबदारी घेईन.", "Mi hi jababdaari ghein.", "I will take this responsibility."),
                 X("अहवाल शुक्रवारपर्यंत पूर्ण होईल.", "Ahaval shukravar-paryant purn hoil.", "The report will be complete by Friday."),
                 X("उरलेले काम दोन दिवसांत होईल.", "Uralele kaam don divsant hoil.", "The remaining work will be done in two days.")],
                [("मी जबाबदारी घेतला.", "मी जबाबदारी घेतली.", "जबाबदारी is feminine: घेतली."),
                 ("मुदत शुक्रवारपर्यंत होईल.", "मुदत शुक्रवारपर्यंत आहे.", "A deadline is dated with आहे: मुदत शुक्रवारपर्यंत आहे.")]),
              [D("अध्यक्ष", "अहवालाची जबाबदारी कोण घेईल?", "Ahavalachi jababdaari kon gheil?", "Who will take responsibility for the report?"),
               D("सदस्य", "मी घेईन. मुदत काय?", "Mi ghein. Mudat kay?", "I will. What is the deadline?"),
               D("अध्यक्ष", "पुढच्या सोमवारपर्यंत. मदत लागली तर सांगा.", "Pudchya somvar-paryant. Madat lagli tar sanga.", "By next Monday. Tell me if you need help."),
               D("सदस्य", "उरलेले आकडे मला द्या, म्हणजे पूर्ण करता येईल.", "Uralele aakde mala dya, mhanje purn karta yeil.", "Give me the remaining figures, then it can be finished.")],
              WS("Responsibility worksheet", [
                  T("Take the work.", ["I will take this responsibility", "the report will be complete by Friday"],
                    ["मी ही जबाबदारी घेईन", "अहवाल शुक्रवारपर्यंत पूर्ण होईल"]),
                  T("Ask for the deadline.", ["what is the deadline?", "the remaining figures"],
                    ["मुदत काय?", "उरलेले आकडे"]),
              ])),
            L("प्रगती कळवणे",
              "Progress is reported in three states: झाले आहे (done), सुरू आहे (going on) and उरले "
              "आहे (left). प्रगती is feminine, झाले/सुरू are participles, and the totals take the "
              "neuter.",
              [V("प्रगती", "pragati", "progress", "noun"),
               V("सुरू", "suru", "going on, begun", "adjective"),
               V("अर्धे", "ardhe", "half", "adjective"),
               V("आकडे", "aakde", "figures", "noun"),
               V("कळवणे", "kalavne", "to inform", "verb")],
              G("Reporting progress",
                "अर्धे काम झाले आहे · बाकी सुरू आहे · तीन दिवसांत कळवतो",
                "The three-way report is standard: झाले आहे, सुरू आहे, उरले आहे. काम and कामे are "
                "neuter, so they take झाले and उरले, not झाला. कळवणे carries the news back to the "
                "person waiting for it.",
                [X("अर्धे काम झाले आहे.", "Ardhe kaam jhale ahe.", "Half the work is done."),
                 X("बाकीचे काम सुरू आहे.", "Bakiche kaam suru ahe.", "The rest of the work is going on."),
                 X("तीन दिवसांत पूर्ण होईल असे वाटते.", "Teen divsant purn hoil ase vaatte.", "I think it will be finished in three days.")],
                [("अर्धे काम झाला आहे.", "अर्धे काम झाले आहे.", "काम is neuter: झाले."),
                 ("काम सुरू आहेत.", "काम सुरू आहे.", "काम is singular neuter: आहे.")]),
              [D("अध्यक्ष", "अहवालाची प्रगती कळवा.", "Ahavalachi pragati kalva.", "Report the progress of the report."),
               D("सदस्य", "अर्धे काम झाले आहे, आकडे तपासत आहे.", "Ardhe kaam jhale ahe, aakde tapasat ahe.", "Half the work is done, I am checking the figures."),
               D("अध्यक्ष", "उरलेले कधी पूर्ण होईल?", "Uralele kadhi purn hoil?", "When will the rest be finished?"),
               D("सदस्य", "तीन दिवसांत. झाले की लगेच कळवतो.", "Teen divsant. Jhale ki lagech kalavto.", "In three days. I will report as soon as it is done.")],
              WS("Progress worksheet", [
                  T("Report the state of the work.", ["half the work is done", "the rest is going on"],
                    ["अर्धे काम झाले आहे", "बाकीचे काम सुरू आहे"]),
                  T("Promise the date.", ["it will be finished in three days", "I will report as soon as it is done"],
                    ["तीन दिवसांत पूर्ण होईल", "झाले की लगेच कळवतो"]),
              ])),
            L("अडचण आणि मदत",
              "An obstacle is अडचण or अडथळा, and it आली (came) rather than झाली. Help is asked "
              "for with मदत लागेल, and extra hands are माणसे or सहकार्य.",
              [V("अडचण", "adchan", "difficulty", "noun"),
               V("अडथळा", "adthala", "obstacle", "noun"),
               V("सहकार्य", "sahakarya", "cooperation", "noun"),
               V("लागणे", "laagne", "to be needed", "verb"),
               V("तातडीचे", "taatdiche", "urgent", "adjective")],
              G("Naming the obstacle",
                "अडचण आली · मदत लागेल · माणसे लागतील",
                "अडचण and अडथळा arrive: आली, आला. What is needed takes लागणे — मदत लागेल, माणसे "
                "लागतील — and the request is softened with -ता तर: शक्य झाले तर दोन माणसे द्या.",
                [X("अहवालात अडचण आली आहे.", "Ahavalat adchan aali ahe.", "A difficulty has come up in the report."),
                 X("मला दोन माणसांचे सहकार्य लागेल.", "Mala don maansanche sahakarya lagel.", "I will need the cooperation of two people."),
                 X("शक्य झाले तर आज मदत करा.", "Shakya jhale tar aaj madat kara.", "If possible, help today.")],
                [("अडचण झाली आहे.", "अडचण आली आहे.", "An obstacle arrives: अडचण आली."),
                 ("मदत लागतील.", "मदत लागेल.", "मदत is singular feminine: लागेल.")]),
              [D("सदस्य", "अहवालात अडचण आली आहे.", "Ahavalat adchan aali ahe.", "A difficulty has come up in the report."),
               D("अध्यक्ष", "काय अडथळा आहे?", "Kay adthala ahe?", "What is the obstacle?"),
               D("सदस्य", "जुन्या आकड्यांची तपासणी राहिली आहे आणि मदत लागेल.", "Junya aakdyanchi tapasni rahili ahe aani madat lagel.", "Checking the old figures is left and I will need help."),
               D("अध्यक्ष", "उद्या दोन माणसे देतो. तातडीचे असेल तर आजच सांगा.", "Udya don maanse deto. Taatdiche asel tar aajach sanga.", "I will give two people tomorrow. If it is urgent, say so today.")],
              WS("Obstacle worksheet", [
                  T("Name the obstacle.", ["a difficulty has come up in the report", "what is the obstacle?"],
                    ["अहवालात अडचण आली आहे", "काय अडथळा आहे?"]),
                  T("Ask for the help.", ["I will need help", "two people will be needed"],
                    ["मदत लागेल", "दोन माणसे लागतील"]),
              ])),
        ]},
        {"id": "B1+-U3", "title": "बैठकीनंतर", "lessons": [
            L("नोंदी आणि पाठपुरावा",
              "The minutes are नोंदी and the follow-up पाठपुरावा (masculine). नोंद ठेवणे keeps a "
              "record and पाठपुरावा करणे chases it, but the work done goes with अमलात आणणे.",
              [V("नोंदी", "nondi", "minutes, notes", "noun"),
               V("पाठपुरावा", "paathpurava", "follow-up", "noun"),
               V("अमलात आणणे", "amlat aanne", "to put into effect", "verb"),
               V("वचन", "vachan", "promise, undertaking", "noun"),
               V("वेळेवर", "velevar", "on time", "adverb")],
              G("Following up",
                "नोंदी ठेवा · पाठपुरावा करा · वेळेवर अमलात आणा",
                "नोंदी ठेवणे keeps the record and पाठपुरावा करणे asks about it afterwards: "
                "पाठपुरावा करतो. A promise is वचन and keeping it is वचन पाळणे; putting a decision "
                "into effect is अमलात आणणे.",
                [X("बैठकीच्या नोंदी ठेवा.", "Baithkichya nondi theva.", "Keep the minutes of the meeting."),
                 X("पुढच्या आठवड्यात पाठपुरावा करतो.", "Pudchya aathvadyat paathpurava karto.", "I will follow up next week."),
                 X("निर्णय वेळेवर अमलात आणा.", "Nirnay velevar amlat aana.", "Put the decision into effect on time.")],
                [("नोंदी ठेवला.", "नोंदी ठेवल्या.", "नोंदी is plural feminine: ठेवल्या."),
                 ("पाठपुरावा केली.", "पाठपुरावा केला.", "पाठपुरावा is masculine: केला.")]),
              [D("अध्यक्ष", "नोंदी तयार आहेत का?", "Nondi tayar aahet ka?", "Are the minutes ready?"),
               D("सचिव", "तयार आहेत. सहा निर्णय आणि दोन वचने नोंदवली आहेत.", "Tayar aahet. Saha nirnay aani don vachne nondavli aahet.", "They are ready. Six decisions and two undertakings are recorded."),
               D("अध्यक्ष", "पाठपुरावा कोण करेल?", "Paathpurava kon karel?", "Who will follow up?"),
               D("सचिव", "मी. सोमवारी प्रत्येकाला विचारतो आणि अहवाल देतो.", "Mi. Somvari pratyekala vichaarto aani ahaval deto.", "I will. On Monday I will ask each one and give a report.")],
              WS("Minutes worksheet", [
                  T("Keep the record.", ["keep the minutes of the meeting", "six decisions are recorded"],
                    ["बैठकीच्या नोंदी ठेवा", "सहा निर्णय नोंदवली आहेत"]),
                  T("Follow up.", ["I will follow up next week", "who will follow up?"],
                    ["पुढच्या आठवड्यात पाठपुरावा करतो", "पाठपुरावा कोण करेल?"]),
              ])),
            L("निर्णय कळवणे",
              "A decision goes out in the impersonal passive: कळवले जाईल, ठरवले जाईल. जाईल takes "
              "the neuter participle, and the notice is सूचना, the board फलक.",
              [V("निर्णय", "nirnay", "decision", "noun"),
               V("कळवणे", "kalavne", "to inform", "verb"),
               V("फलक", "phalak", "notice board", "noun"),
               V("जाहीर", "jaahir", "public, announced", "adjective"),
               V("ठरवले जाईल", "tharvale jail", "it will be decided", "phrase")],
              G("Announcing a decision",
                "निर्णय कळवले जाईल · फलकावर लावा · सर्वांना जाहीर करा",
                "The impersonal -ले जाईल removes the person from the announcement: कळवले जाईल, "
                "ठरवले जाईल, लावले जाईल. The notice goes on the फलक (फलकावर लावा) and the "
                "announcement is जाहीर करणे.",
                [X("निर्णय उद्या कळवले जाईल.", "Nirnay udya kalavle jail.", "The decision will be announced tomorrow."),
                 X("पुढची बैठक पंधरा दिवसांनी ठरवली जाईल.", "Pudchi baithak pandhra divsanni tharvli jail.", "The next meeting will be fixed after fifteen days."),
                 X("सूचना फलकावर लावा.", "Suchana phalkavar lava.", "Put the notice on the board.")],
                [("निर्णय कळवला जाईल.", "निर्णय कळवले जाईल.", "The passive takes the neuter: कळवले जाईल."),
                 ("सूचना जाहीर केला.", "सूचना जाहीर केली.", "सूचना is feminine: केली.")]),
              [D("सदस्य", "निर्णय बाहेर कधी कळेल?", "Nirnay baher kadhi kalel?", "When will the decision be known outside?"),
               D("अध्यक्ष", "आज संध्याकाळी कळवले जाईल.", "Aaj sandhyakali kalavle jail.", "It will be announced this evening."),
               D("सदस्य", "सूचना फलकावर लावायची का?", "Suchana phalkavar lavaychi ka?", "Is the notice to be put on the board?"),
               D("अध्यक्ष", "हो, आणि सर्व खात्यांना जाहीर करा.", "Ho, aani sarv khatyanna jaahir kara.", "Yes, and announce it to all departments.")],
              WS("Announcement worksheet", [
                  T("Announce it.", ["the decision will be announced this evening", "the notice will be put on the board"],
                    ["निर्णय आज संध्याकाळी कळवले जाईल", "सूचना फलकावर लावली जाईल"]),
                  T("Order it.", ["put the notice on the board", "announce it to all departments"],
                    ["सूचना फलकावर लावा", "सर्व खात्यांना जाहीर करा"]),
              ])),
            L("आढावा बैठक",
              "A review is आढावा (masculine) and it is घेतला. Expectations are अपेक्षा (feminine) "
              "with अपेक्षेपेक्षा for more than expected, and a change for the better is सुधारणा.",
              [V("आढावा", "aadhava", "review", "noun"),
               V("अपेक्षा", "apeksha", "expectation", "noun"),
               V("सुधारणा", "sudharna", "improvement", "noun"),
               V("उशीर", "ushir", "delay", "noun"),
               V("निकष", "nikash", "standard, criterion", "noun")],
              G("Reviewing the result",
                "अपेक्षेपेक्षा जास्त · सुधारणा झाली · उशीर झाला",
                "अपेक्षेपेक्षा is more than expected and अपेक्षेइतके is as much as expected. "
                "सुधारणा and वाढ take झाली, while उशीर takes झाला. A review is घेतला (आढावा "
                "घेतला), never केला.",
                [X("या महिन्यात अपेक्षेपेक्षा जास्त काम झाले.", "Ya mahinyat apekshepeksha jaast kaam jhale.", "This month more work was done than expected."),
                 X("उशिराचे कारण सांगा.", "Ushirache karan sanga.", "Give the reason for the delay."),
                 X("पुढच्या महिन्यात सुधारणा होईल.", "Pudchya mahinyat sudharna hoil.", "There will be an improvement next month.")],
                [("आढावा केला.", "आढावा घेतला.", "A review is घेतला: आढावा घेतला."),
                 ("उशीर झाली.", "उशीर झाला.", "उशीर is masculine: झाला.")]),
              [D("अध्यक्ष", "मागच्या महिन्याचा आढावा घ्या.", "Maagchya mahinyacha aadhava ghya.", "Review last month's work."),
               D("सदस्य", "अपेक्षेपेक्षा जास्त काम झाले, पण दोन ठिकाणी उशीर झाला.", "Apekshepeksha jaast kaam jhale, pan don thikani ushir jhala.", "More work was done than expected, but there were delays in two places."),
               D("अध्यक्ष", "कारण काय?", "Karan kay?", "What is the reason?"),
               D("सदस्य", "आकडे उशिरा मिळाले. पुढच्या महिन्यात निकष बदलू.", "Aakde ushira milale. Pudchya mahinyat nikash badlu.", "The figures came late. Next month we will change the standard.")],
              WS("Review worksheet", [
                  T("Report the result.", ["more work was done than expected", "there were delays in two places"],
                    ["अपेक्षेपेक्षा जास्त काम झाले", "दोन ठिकाणी उशीर झाला"]),
                  T("Explain and improve.", ["the figures came late", "there will be an improvement next month"],
                    ["आकडे उशिरा मिळाले", "पुढच्या महिन्यात सुधारणा होईल"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Every year after the monsoon, lakhs of Warkaris walk to Pandharpur in the "
                 "वारी — some three weeks on the road, in palkhis that carry the padukas of "
                 "Dnyaneshwar and Tukaram. The walkers sing abhangas in Marathi, and the whole "
                 "road becomes a moving library of the language: चालवा, टाळ, मृदंग, and verse "
                 "after verse on Vitthal. For a learner this is Marathi at its oldest and most "
                 "public — heard in the fields, not in a classroom."),
        source_url="https://en.wikipedia.org/wiki/Pandharpur",
        reading=("बैठक आटोपल्यावर सचिवाने नोंदी लगेच लिहिल्या. सहा निर्णय आणि दोन वचने "
                 "नोंदवली गेली. पुढच्या आठवड्यात प्रत्येक जबाबदारीचा पाठपुरावा करायचा होता, "
                 "म्हणून त्याने कामाची वाटणी केली. दोन सदस्यांनी मुदत वेळेवर पाळली, पण एका "
                 "ठिकाणी आकडे उशिरा मिळाल्यामुळे अडचण आली. सचिवाने अध्यक्षांना कळवले आणि "
                 "मदत मागितली. अध्यक्षांनी दोन माणसे दिली. महिन्याच्या शेवटी आढावा "
                 "बैठकीत अपेक्षेपेक्षा जास्त काम झाल्याचे दिसले."),
        reading_gloss=("After the meeting ended, the secretary wrote the minutes at once. Six "
                       "decisions and two undertakings were recorded. The following week each "
                       "responsibility had to be followed up, so he divided the work. Two members "
                       "kept their deadlines on time, but at one place a difficulty came up "
                       "because the figures arrived late. The secretary informed the chairperson "
                       "and asked for help. The chairperson gave two people. At the end of the "
                       "month, the review meeting showed that more work had been done than "
                       "expected."),
        listening=("अध्यक्ष: सर्वांनी कार्यसूची पाहिली आहे का?<br>"
                   "सदस्य: हो. पहिल्या मुद्द्यावर मला आक्षेप आहे.<br>"
                   "अध्यक्ष: सांगा.<br>"
                   "सदस्य: वेळापत्रक तीन महिन्यांचे आहे, पण मुदत दोन महिन्यांची आहे.<br>"
                   "अध्यक्ष: ठीक, तर मुदत बदलून तीन महिन्यांची ठरवू. कळवले जाईल."),
        listening_gloss=("Chairperson: Has everyone seen the agenda? Member: Yes. I have an "
                         "objection to the first item. Chairperson: Go on. Member: The schedule is "
                         "for three months, but the deadline is two months. Chairperson: All "
                         "right, then let us change the deadline to three months. It will be "
                         "announced."),
        voice_tag=VOICE,
        idioms=[
            ("माझ्या मते", "in my opinion", "the polite way into an argument"),
            ("मुद्द्यावर येणे", "to come to the point", "stop wandering"),
            ("थोडक्यात सांगायचे तर", "to put it briefly", "cutting a long story short"),
            ("ठरले की कळवतो", "I will inform when it is decided", "no promises yet"),
            ("जबाबदारी घेणे", "to take responsibility", "to own the work"),
            ("पाठपुरावा करणे", "to follow up", "to chase a pending matter"),
            ("अमलात आणणे", "to bring into force", "to actually do what was decided"),
            ("अडचण आली", "a difficulty came", "something went wrong on the way"),
            ("वेळेवर", "on time", "before the deadline"),
            ("अपेक्षेपेक्षा जास्त", "more than expected", "better than the plan"),
        ],
        mistakes=[
            ("अर्धे काम झाला आहे.", "अर्धे काम झाले आहे.", "काम is neuter: झाले."),
            ("आढावा केला.", "आढावा घेतला.", "A review is घेतला: आढावा घेतला."),
            ("निर्णय कळवला जाईल.", "निर्णय कळवले जाईल.", "The impersonal passive takes the neuter: कळवले जाईल."),
        ],
        task_title="Run a meeting on paper, in Marathi",
        task_instructions=("Write a Marathi exchange of eight to ten turns: agree on an agenda with "
                           "three items, state one opinion with माझ्या मते, raise one objection, "
                           "summarise with थोडक्यात, fix one responsibility with a deadline, and "
                           "announce the decision in the impersonal passive (कळवले जाईल). Then "
                           "write three lines of minutes using नोंद ठेवली and ठरले."),
    ),
    "test": [
        ("translate_en", "Say: I will take this responsibility.", "मी ही जबाबदारी घेईन."),
        ("translate_mr", "अपेक्षेपेक्षा जास्त काम झाले.", "More work was done than expected."),
        ("multiple_choice", "Which sentence keeps the minutes?", "बैठकीच्या नोंदी ठेवा."),
        ("fill_in_the_blank", "निर्णय उद्या ___ जाईल.", "कळवले"),
        ("word_selection", "Select the Marathi for 'I will need help'.", "मदत लागेल"),
        ("error_correction", "अर्धे काम झाला आहे.", "अर्धे काम झाले आहे."),
        ("dialogue_completion", "Complete: अहवालाची जबाबदारी कोण घेईल? — ___ (I will take it)", "मी घेईन"),
        ("matching", "Match पाठपुरावा to its meaning.", "follow-up"),
        ("reading_comprehension", "आकडे उशिरा मिळाल्यामुळे काय झाले?", "a difficulty came up"),
        ("inference", "दोन सदस्यांनी मुदत वेळेवर पाळली, पण एका ठिकाणी अडचण आली. — how did the team do?", "mostly on time, with one problem"),
        ("main_idea", "थोडक्यात: दोन टप्पे ठरले. — what is this sentence?", "a summary of a decision"),
        ("detail_identification", "पुढची बैठक कधी ठरवली जाईल?", "after fifteen days"),
    ],
}

HALFSTEPS["C1+"] = {
    "title": "Marathi C1+ — Poetry, story, review",
    "native": NATIVE,
    "goals": [
        "Read a Marathi poem aloud and speak about its रस, अलंकार and ओळ",
        "Follow a story through its characters, structure and style",
        "Write a short review with a clearly named standpoint and no prejudice",
    ],
    "units": [
        {"id": "C1+-U1", "title": "कविता", "lessons": [
            L("कविता वाचणे",
              "A poem is कविता, its lines ओळी, its metre छंद and its aesthetic flavour रस. Marathi "
              "criticism names nine रस and speaks of अलंकार as the figures that carry them.",
              [V("कविता", "kavita", "poem", "noun"),
               V("ओळ", "ol", "line of verse", "noun"),
               V("छंद", "chhand", "metre", "noun"),
               V("रस", "ras", "aesthetic flavour", "noun"),
               V("अलंकार", "alankar", "figure of speech", "noun")],
              G("Speaking about a poem",
                "या कवितेत करुण रस आहे · ओळीचा छंद सुटत नाही · अलंकार ओळखा",
                "रस and अलंकार are masculine and take आहे; कविता and ओळ are feminine. A poem "
                "is read वाचली जाते or recited म्हटली जाते, and a line that carries a figure is "
                "described with -ने: उपमेने.",
                [X("या कवितेत करुण रस आहे.", "Ya kavitet karun ras ahe.", "There is the flavour of pathos in this poem."),
                 X("तीन ओळींत उपमा अलंकार आहे.", "Teen olinit upma alankar ahe.", "There is a simile in three lines."),
                 X("कविता मोठ्याने वाचली जाते.", "Kavita mothyanne vaachli jate.", "The poem is read aloud.")],
                [("या कवितेत करुण रस आहेत.", "या कवितेत करुण रस आहे.", "रस is singular masculine: आहे."),
                 ("कविता वाचला जातो.", "कविता वाचली जाते.", "कविता is feminine: वाचली जाते.")]),
              [D("वाचक", "ही कविता कशी वाटली?", "Hi kavita kashi vaatli?", "How did this poem seem to you?"),
               D("समीक्षक", "छंद घट्ट आहे आणि शेवटच्या ओळीत करुण रस आहे.", "Chhand ghatt ahe aani shevtachya olinit karun ras ahe.", "The metre is firm and there is pathos in the last line."),
               D("वाचक", "अलंकार कोणता आहे?", "Alankar konta ahe?", "Which figure is there?"),
               D("समीक्षक", "उपमा. ती ओळ मोठ्याने वाचली तर चांगली लागते.", "Upma. Ti ol mothyanne vaachli tar chaangli lagte.", "A simile. That line sounds good read aloud.")],
              WS("Poem worksheet", [
                  T("Describe the poem.", ["there is the flavour of pathos in this poem", "there is a simile in three lines"],
                    ["या कवितेत करुण रस आहे", "तीन ओळींत उपमा अलंकार आहे"]),
                  T("Say how it is read.", ["the poem is read aloud", "which figure is there?"],
                    ["कविता मोठ्याने वाचली जाते", "अलंकार कोणता आहे?"]),
              ])),
            L("रूपक आणि प्रतिमा",
              "उपमा compares with सारखा, रूपक identifies outright, and प्रतिमा is the image the "
              "line builds. A figure of sound is अनुप्रास, and the implicit suggestion is ध्वनि.",
              [V("उपमा", "upma", "simile", "noun"),
               V("रूपक", "rupak", "metaphor", "noun"),
               V("प्रतिमा", "pratima", "image", "noun"),
               V("अनुप्रास", "anupras", "alliteration", "noun"),
               V("ध्वनि", "dhvani", "suggestion, resonance", "noun")],
              G("Naming the figure",
                "… सारखा वाटतो (उपमा) · … च आहेच (रूपक) · अनुप्रास ओळीत ऐकू येतो",
                "उपमा keeps the two things apart with सारखा/प्रमाणे, while रूपक fuses them: चंद्र "
                "सारखा चेहरा is a simile and चेहराच चंद्र is a metaphor. ध्वनि is what the line "
                "suggests beyond what it says — the point Marathi criticism cares about most.",
                [X("चेहरा चंद्रासारखा आहे.", "Chehra chandrasarkha ahe.", "The face is like the moon."),
                 X("आईची माया सावलीसारखी असते.", "Aaichi maya saavlisarkhi aste.", "A mother's love is like shade."),
                 X("या ओळीत अनुप्रास आहे.", "Ya olit anupras ahe.", "There is alliteration in this line.")],
                [("आईची माया सावली आहे.", "आईची माया सावलीसारखी असते.", "With सारखी it stays a simile: सावलीसारखी."),
                 ("या ओळीत अनुप्रास आहेत.", "या ओळीत अनुप्रास आहे.", "अनुप्रास is singular here: आहे.")]),
              [D("विद्यार्थी", "ही ओळ रूपक आहे की उपमा?", "Hi ol rupak ahe ki upma?", "Is this line a metaphor or a simile?"),
               D("शिक्षक", "उपमा, कारण सारखी हा शब्द आहे.", "Upma, karan saarkhi ha shabd ahe.", "A simile, because the word 'like' is there."),
               D("विद्यार्थी", "मग रूपक कुठे?", "Mag rupak kuthe?", "Then where is the metaphor?"),
               D("शिक्षक", "पुढच्या ओळीत, जिथे प्रतिमाच माणूस होते.", "Pudchya olit, jithe pratimach maanus hote.", "In the next line, where the image itself becomes a person.")],
              WS("Figure worksheet", [
                  T("Name the figure.", ["the face is like the moon", "a mother's love is like shade"],
                    ["चेहरा चंद्रासारखा आहे", "आईची माया सावलीसारखी असते"]),
                  T("Find the sound.", ["there is alliteration in this line", "where is the metaphor?"],
                    ["या ओळीत अनुप्रास आहे", "रूपक कुठे आहे?"]),
              ])),
            L("कवितेचा अर्थ लावणे",
              "Interpretation runs on संदर्भ (context) and भावार्थ (sense); a hasty reading is "
              "अर्थ लावणे done गडबडीत. सूचित means suggested, and the settled reading is अर्थ "
              "स्पष्ट होतो.",
              [V("संदर्भ", "sandarbh", "context", "noun"),
               V("भावार्थ", "bhavarth", "sense, purport", "noun"),
               V("सूचित", "suchit", "suggested, implied", "adjective"),
               V("गडबड", "gadbad", "haste, muddle", "noun"),
               V("व्याख्या", "vyakhya", "interpretation, commentary", "noun")],
              G("Reading with context",
                "संदर्भाशिवाय अर्थ लागत नाही · यातून सूचित होते · व्याख्या करताना",
                "संदर्भाशिवाय (without context) and व्याख्या करताना (while interpreting) are the "
                "two fixed phrases of this lesson. सूचित होते states what the text implies, and "
                "भावार्थ is the sense you are entitled to claim — not the sense you invent.",
                [X("संदर्भाशिवाय या ओळीचा अर्थ लागत नाही.", "Sandarbhashivay ya olicha arth laagat nahi.", "Without context this line cannot be interpreted."),
                 X("या ओळीतून हताशा सूचित होते.", "Ya olitun hataasha suchit hote.", "Despair is suggested by this line."),
                 X("व्याख्या करताना संदर्भ द्यावा.", "Vyakhya karatana sandarbh dyava.", "While interpreting, give the context.")],
                [("संदर्भाशिवाय अर्थ लागतो.", "संदर्भाशिवाय अर्थ लागत नाही.", "The point is the negation: without context the sense does not come."),
                 ("या ओळीतून सूचित होतो.", "या ओळीतून सूचित होते.", "The impersonal सूचित होते is neuter.")]),
              [D("समीक्षक", "या ओळीचा अर्थ काय?", "Ya olicha arth kay?", "What does this line mean?"),
               D("वाचक", "संदर्भाशिवाय अर्थ लागत नाही.", "Sandarbhashivay arth laagat nahi.", "Without context it cannot be interpreted."),
               D("समीक्षक", "संदर्भ दिला तर?", "Sandarbh dila tar?", "And if the context is given?"),
               D("वाचक", "तर हताशा सूचित होते, पण असा व्याख्या केला तर गडबड होईल.", "Tar hataasha suchit hote, pan asa vyakhya kela tar gadbad hoil.", "Then despair is suggested, but to interpret it that way would be hasty.")],
              WS("Context worksheet", [
                  T("Ask and answer about the sense.", ["what does this line mean?", "without context it cannot be interpreted"],
                    ["या ओळीचा अर्थ काय?", "संदर्भाशिवाय अर्थ लागत नाही"]),
                  T("Interpret carefully.", ["despair is suggested by this line", "while interpreting, give the context"],
                    ["या ओळीतून हताशा सूचित होते", "व्याख्या करताना संदर्भ द्यावा"]),
              ])),
        ]},
        {"id": "C1+-U2", "title": "कथानक", "lessons": [
            L("पात्र आणि वाटचाल",
              "In a story the character is पात्र and the arc वाटचाल; the inner conflict is द्वंद्व "
              "and the turning point कलाटणी. पात्र is neuter, वाटचाल and कलाटणी are feminine.",
              [V("पात्र", "patra", "character", "noun"),
               V("वाटचाल", "vaatchal", "journey, arc", "noun"),
               V("द्वंद्व", "dvandva", "inner conflict", "noun"),
               V("कलाटणी", "kalatni", "turning point", "noun"),
               V("खात्री", "khatri", "certainty, assurance", "noun")],
              G("Following a character",
                "पात्राची वाटचाल विश्वासार्ह वाटते · द्वंद्व कमी होत नाही · कलाटणीत काय बदलते?",
                "The character's course is पात्राची वाटचाल and it वाटते विश्वासार्ह or ठोस, while "
                "the conflict कमी होते. The turning point is asked about with कलाटणीत काय बदलले? — "
                "the reliable test of a story's structure.",
                [X("पात्राची वाटचाल विश्वासार्ह वाटते.", "Patrachi vaatchal vishvasarha vaatte.", "The character's arc seems believable."),
                 X("कथेचा द्वंद्व कमी होत नाही.", "Kathecha dvandva kami hot nahi.", "The story's conflict does not ease."),
                 X("कलाटणीत पात्राचा निर्णय बदलतो.", "Kalatnit patracha nirnay badalto.", "At the turning point the character's decision changes.")],
                [("पात्राची वाटचाल विश्वासार्ह वाटतो.", "पात्राची वाटचाल विश्वासार्ह वाटते.", "वाटचाल is feminine: वाटते."),
                 ("कथेचे द्वंद्व आहे.", "कथेचा द्वंद्व आहे.", "द्वंद्व is masculine: कथेचा द्वंद्व.")]),
              [D("वाचक", "पात्र तुम्हाला पटले का?", "Patra tumhala patle ka?", "Did the character convince you?"),
               D("समीक्षक", "पटले, कारण वाटचाल विश्वासार्ह आहे.", "Patle, karan vaatchal vishvasarha ahe.", "Yes, because the arc is believable."),
               D("वाचक", "कलाटणी कुठे आहे?", "Kalatni kuthe ahe?", "Where is the turning point?"),
               D("समीक्षक", "तिसऱ्या प्रकरणात, जिथे पात्र परत जायचे ठरवते.", "Tisrya prakarnat, jithe patra parat jaayche tharvte.", "In the third chapter, where the character decides to go back.")],
              WS("Character worksheet", [
                  T("Describe the arc.", ["the character's arc seems believable", "the conflict does not ease"],
                    ["पात्राची वाटचाल विश्वासार्ह वाटते", "द्वंद्व कमी होत नाही"]),
                  T("Locate the turn.", ["where is the turning point?", "the character decides to go back"],
                    ["कलाटणी कुठे आहे?", "पात्र परत जायचे ठरवते"]),
              ])),
            L("कथानकाची रचना",
              "Plot is कथानक and structure रचना; an episode is प्रसंग and the thread सूत्र. "
              "उत्कटता is the intensity and कालानुक्रम the time order. A plot that moves back "
              "and forth has कालानुक्रम मोडला आहे, and उत्कटता वाढते where the turns are placed well.",
              [V("कथानक", "kathanak", "plot", "noun"),
               V("रचना", "rachana", "structure", "noun"),
               V("प्रसंग", "prasang", "episode, incident", "noun"),
               V("उत्कटता", "utkatta", "intensity", "noun"),
               V("कालानुक्रम", "kalanukram", "chronological order", "noun")],
              G("Describing structure",
                "कथानक घट्ट आहे · प्रसंग मागेपुढे केले आहेत · उत्कटता वाढते",
                "कथानक is neuter (कथानक घट्ट आहे) and रचना feminine (रचना घट्ट आहे). A story "
                "that moves back and forth is described with कालानुक्रम मोडला आहे; उत्कटता "
                "increases with वाढते.",
                [X("कथानकाची रचना घट्ट आहे.", "Kathanakachi rachana ghatt ahe.", "The structure of the plot is firm."),
                 X("लेखकाने कालानुक्रम मोडला आहे.", "Lekhane kalanukram modla ahe.", "The author has broken the chronological order."),
                 X("दुसऱ्या भागात उत्कटता वाढते.", "Dusrya bhaagat utkatta vaadhte.", "In the second part the intensity rises.")],
                [("कथानकाची रचना घट्ट आहेत.", "कथानकाची रचना घट्ट आहे.", "रचना is singular feminine: आहे."),
                 ("उत्कटता वाढतो.", "उत्कटता वाढते.", "उत्कटता is feminine: वाढते.")]),
              [D("विद्यार्थी", "कथानकाची रचना कशी आहे?", "Kathanakachi rachana kashi ahe?", "How is the plot's structure?"),
               D("शिक्षक", "घट्ट. पण कालानुक्रम मोडलेला आहे.", "Ghatt. Pan kalanukram modela ahe.", "Firm. But the chronological order is broken."),
               D("विद्यार्थी", "त्यामुळे त्रास होतो का?", "Tyamule traas hoto ka?", "Does that make it hard?"),
               D("शिक्षक", "नाही, उलट उत्कटता वाढते.", "Nahi, ulat utkatta vaadhte.", "No, on the contrary the intensity rises.")],
              WS("Structure worksheet", [
                  T("Describe the structure.", ["the structure of the plot is firm", "the author has broken the chronological order"],
                    ["कथानकाची रचना घट्ट आहे", "लेखकाने कालानुक्रम मोडला आहे"]),
                  T("Judge the effect.", ["in the second part the intensity rises", "does that make it hard?"],
                    ["दुसऱ्या भागात उत्कटता वाढते", "त्यामुळे त्रास होतो का?"]),
              ])),
            L("शैली आणि भाषा",
              "Style is शैली and the local speech a writer uses is बोली; sentence craft is "
              "वाक्यरचना and the idiom of a region म्हणी. Shorter sentences are described as "
              "कोरडी or तरल.",
              [V("शैली", "shaili", "style", "noun"),
               V("बोली", "boli", "dialect, spoken variety", "noun"),
               V("वाक्यरचना", "vakyarachana", "sentence craft", "noun"),
               V("म्हणी", "mhani", "proverbs", "noun"),
               V("तरल", "taral", "fluid, flowing", "adjective")],
              G("Talking about style",
                "लेखकाची शैली ओळखता येते · बोलीतले शब्द वापरले आहेत · वाक्यरचना तरल आहे",
                "शैली and वाक्यरचना are feminine, so they take आहे/ओळखली जाते and तरल आहे. A "
                "writer who uses local words is said to have बोली वापरली आहे, and proverbs are "
                "म्हणी वापरल्या आहेत.",
                [X("लेखकाची शैली पहिल्या परिच्छेदातच ओळखता येते.", "Lekhacha shaili pahilya parichchhedatach olakhta yete.", "The writer's style is recognisable in the first paragraph itself."),
                 X("त्याने बोलीतले शब्द वापरले आहेत.", "Tyane bolitale shabd vaparle aahet.", "He has used words from the dialect."),
                 X("वाक्यरचना तरल आहे.", "Vakyarachana taral ahe.", "The sentence craft is fluid.")],
                [("लेखकाची शैली ओळखता येतो.", "लेखकाची शैली ओळखता येते.", "शैली is feminine: ओळखता येते."),
                 ("म्हणी वापरला आहे.", "म्हणी वापरल्या आहेत.", "म्हणी is plural feminine: वापरल्या आहेत.")]),
              [D("वाचक", "लेखकाची शैली कशी आहे?", "Lekhacha shaili kashi ahe?", "How is the writer's style?"),
               D("समीक्षक", "तरल. आणि बोलीतले शब्द भरपूर आहेत.", "Taral. Aani bolitale shabd bharpur aahet.", "Fluid. And there are plenty of dialect words."),
               D("वाचक", "म्हणीही आहेत का?", "Mhanihi aahet ka?", "Are there proverbs too?"),
               D("समीक्षक", "हो, पण जास्त झाल्या तर शैली जड होते.", "Ho, pan jaast jhalya tar shaili jad hote.", "Yes, but if there are too many the style becomes heavy.")],
              WS("Style worksheet", [
                  T("Describe the style.", ["the writer's style is recognisable in the first paragraph", "the sentence craft is fluid"],
                    ["लेखकाची शैली पहिल्या परिच्छेदातच ओळखता येते", "वाक्यरचना तरल आहे"]),
                  T("Count the idiom.", ["he has used words from the dialect", "are there proverbs too?"],
                    ["त्याने बोलीतले शब्द वापरले आहेत", "म्हणीही आहेत का?"]),
              ])),
        ]},
        {"id": "C1+-U3", "title": "समीक्षा", "lessons": [
            L("मूल्यमापन",
              "To review is मूल्यमापन करणे; the judgement is न्याय and the standard मापदंड. "
              "निष्पक्ष means even-handed, and पक्षपात partiality. The reviewer states the yardstick first and then judges: मापदंड "
              "स्पष्ट असावा, अन्यथा न्याय होत नाही.",
              [V("मूल्यमापन", "mulyamapan", "evaluation", "noun"),
               V("न्याय", "nyay", "judgement, justice", "noun"),
               V("मापदंड", "mapdand", "standard, yardstick", "noun"),
               V("निष्पक्ष", "nishpaksh", "impartial", "adjective"),
               V("पक्षपात", "pakshpat", "partiality", "noun")],
              G("Judging a work",
                "मूल्यमापन करताना मापदंड स्पष्ट असावा · न्याय करणे सोपे नाही · पक्षपात टाळावा",
                "The review states its standard with मापदंड स्पष्ट असावा and its verdict with न्याय "
                "करताना …. पक्षपात टाळावा (one must avoid partiality) is the reviewer's own rule, "
                "and it uses the optative -ावा.",
                [X("मूल्यमापन करताना मापदंड स्पष्ट असावा.", "Mulyamapan karatana mapdand spasht asava.", "While evaluating, the standard should be clear."),
                 X("पक्षपात टाळावा, अन्यथा न्याय होत नाही.", "Pakshpat taalava, anyatha nyay hot nahi.", "Partiality must be avoided, otherwise there is no judgement."),
                 X("निष्पक्ष समीक्षा वाचकाला विश्वास देते.", "Nishpaksh samiksha vaachakala vishwas dete.", "An impartial review gives the reader confidence.")],
                [("मूल्यमापन करताना मापदंड स्पष्ट असावेत.", "मूल्यमापन करताना मापदंड स्पष्ट असावा.", "मापदंड here is singular masculine: असावा."),
                 ("पक्षपात टाळावी.", "पक्षपात टाळावा.", "पक्षपात is masculine: टाळावा.")]),
              [D("संपादक", "समीक्षा लिहायला तयार आहात?", "Samiksha lihayla tayar aahat?", "Are you ready to write the review?"),
               D("समीक्षक", "हो, पण मापदंड स्पष्ट असावा.", "Ho, pan mapdand spasht asava.", "Yes, but the standard should be clear."),
               D("संपादक", "कोणता मापदंड घेणार?", "Konta mapdand ghenaar?", "Which standard will you take?"),
               D("समीक्षक", "भाषेचा आणि रचनेचा — आणि पक्षपात टाळावा.", "Bhashecha aani rachanecha — aani pakshpat taalava.", "That of language and structure — and partiality must be avoided.")],
              WS("Evaluation worksheet", [
                  T("State the standard.", ["while evaluating, the standard should be clear", "which standard will you take?"],
                    ["मूल्यमापन करताना मापदंड स्पष्ट असावा", "कोणता मापदंड घेणार?"]),
                  T("Warn against partiality.", ["partiality must be avoided", "an impartial review gives the reader confidence"],
                    ["पक्षपात टाळावा", "निष्पक्ष समीक्षा वाचकाला विश्वास देते"]),
              ])),
            L("दृष्टिकोन आणि पूर्वग्रह",
              "A standpoint is दृष्टिकोन and a prejudice पूर्वग्रह. The obverse is आग्रह "
              "stubbornness, and the honest reviewer says मर्यादा आहे — this is where I stop.",
              [V("दृष्टिकोन", "drishtikon", "standpoint", "noun"),
               V("पूर्वग्रह", "purvagrah", "prejudice", "noun"),
               V("आग्रह", "aagrah", "insistence", "noun"),
               V("मर्यादा", "maryada", "limit, boundary", "noun"),
               V("स्पष्टवक्ते", "spashtavakte", "plain-spoken", "adjective")],
              G("Declaring your standpoint",
                "माझा दृष्टिकोन … आहे · पूर्वग्रह टाळला पाहिजे · माझी मर्यादा इथेच संपते",
                "The standpoint is declared with माझा दृष्टिकोन or या दृष्टिकोनातून. पूर्वग्रह takes "
                "टाळला पाहिजे, and the limit of one's reading is admitted with मर्यादा: माझी "
                "मर्यादा इथेच संपते.",
                [X("या दृष्टिकोनातून कादंबरी वाचली तर अर्थ बदलतो.", "Ya drishtikonatun kadambari vaachli tar arth badalto.", "Read from this standpoint, the novel's sense changes."),
                 X("पूर्वग्रह टाळला पाहिजे.", "Purvagrah taalala pahije.", "Prejudice ought to be avoided."),
                 X("मर्यादा सांगणे अप्रामाणिकपणा नाही.", "Maryada sangne apramanikpan naahi.", "Stating one's limit is not dishonesty.")],
                [("पूर्वग्रह टाळली पाहिजे.", "पूर्वग्रह टाळला पाहिजे.", "पूर्वग्रह is masculine: टाळला."),
                 ("या दृष्टिकोनातून अर्थ बदलते.", "या दृष्टिकोनातून अर्थ बदलतो.", "अर्थ is masculine singular: बदलतो.")]),
              [D("वाचक", "तुमचा दृष्टिकोन काय आहे?", "Tumcha drishtikon kay ahe?", "What is your standpoint?"),
               D("समीक्षक", "स्त्री-पात्रांच्या दृष्टिकोनातून कादंबरी वाचतो.", "Stri-patraancha drishtikonatun kadambari vaachto.", "I read the novel from the standpoint of the women characters."),
               D("वाचक", "पूर्वग्रह नको.", "Purvagrah nako.", "No prejudice, please."),
               D("समीक्षक", "टाळतो. आणि माझी मर्यादा सांगतो: कादंबरीच्या ऐतिहासिक संदर्भाची खोली माझ्याकडे कमी आहे.", "Taalto. Aani majhi maryada sangto: kadambarichya aitihasik sandarbhachi kholi majhyakade kami ahe.", "I avoid it. And I state my limit: my depth on the novel's historical context is small.")],
              WS("Standpoint worksheet", [
                  T("Declare the standpoint.", ["I read the novel from the standpoint of the women characters", "what is your standpoint?"],
                    ["स्त्री-पात्रांच्या दृष्टिकोनातून कादंबरी वाचतो", "तुमचा दृष्टिकोन काय आहे?"]),
                  T("Admit the limit.", ["prejudice ought to be avoided", "I state my limit"],
                    ["पूर्वग्रह टाळला पाहिजे", "माझी मर्यादा सांगतो"]),
              ])),
            L("समीक्षा लिहिणे",
              "A review moves in four steps: परिचय, मुद्दे, पुरावा, निष्कर्ष. समीक्षा is feminine "
              "and निष्कर्ष masculine, and a citation is संदर्भ द्यावा. The order matters: परिचय first, then the मुद्दे, an "
              "उद्धरण for each, and the निष्कर्ष last.",
              [V("समीक्षा", "samiksha", "review, criticism", "noun"),
               V("परिचय", "parichay", "introduction", "noun"),
               V("निष्कर्ष", "nishkarsh", "conclusion", "noun"),
               V("उद्धरण", "uddharan", "quotation", "noun"),
               V("तोटा", "tota", "shortcoming, loss", "noun")],
              G("Writing the review",
                "परिचय द्या · प्रत्येक मुद्द्याला उद्धरण द्या · शेवटी निष्कर्ष काढा",
                "The steps take the imperative: परिचय द्या, मुद्दे द्या, उद्धरण द्या, निष्कर्ष काढा. "
                "A shortcoming is noted with तोटा आहे, and the last line carries the निष्कर्ष — "
                "without the applause that belongs to a different genre.",
                [X("परिचयात लेखकाची पार्श्वभूमी द्यावी.", "Parichayat lekhachi parshvabhumi dyavi.", "In the introduction the writer's background should be given."),
                 X("प्रत्येक मुद्द्याला उद्धरण देऊन पुरावा द्यावा.", "Pratyek muddyala uddharan deun purava dyava.", "Each point should be backed with a quotation."),
                 X("शेवटी निष्कर्ष स्पष्ट लिहावा.", "Shevti nishkarsh spasht lihava.", "Finally the conclusion should be written clearly.")],
                [("परिचय द्यावी.", "परिचय द्यावा.", "परिचय is masculine: द्यावा."),
                 ("शेवटी निष्कर्ष लिहावी.", "शेवटी निष्कर्ष लिहावा.", "निष्कर्ष is masculine: लिहावा.")]),
              [D("संपादक", "समीक्षेची रचना कशी असावी?", "Samikshechi rachana kashi asavi?", "How should the review be structured?"),
               D("समीक्षक", "परिचय, तीन मुद्दे, प्रत्येकाला उद्धरण आणि शेवटी निष्कर्ष.", "Parichay, teen mudde, pratyekala uddharan aani shevti nishkarsh.", "Introduction, three points, a quotation for each, and a conclusion at the end."),
               D("संपादक", "तोटाही लिहा.", "Totahi liha.", "Write the shortcomings too."),
               D("समीक्षक", "लिहितो, पण पुराव्याशिवाय नाही.", "Lihito, pan puravyashivay nahi.", "I will, but not without evidence.")],
              WS("Review worksheet", [
                  T("Plan the review.", ["introduction, three points, a quotation for each", "finally the conclusion should be written clearly"],
                    ["परिचय, तीन मुद्दे, प्रत्येकाला उद्धरण", "शेवटी निष्कर्ष स्पष्ट लिहावा"]),
                  T("Balance it.", ["write the shortcomings too", "not without evidence"],
                    ["तोटाही लिहा", "पुराव्याशिवाय नाही"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Marathi has one of the oldest literatures among the modern Indian languages. "
                 "Dnyaneshwari (1290) — ज्ञानेश्वरी — put philosophy into the verse and images of "
                 "ordinary Marathi speech, Tukaram's abhangas turned it into song, and the Peshwa "
                 "centuries produced पोवाडे, the ballads of the battlefield. Then came the modern "
                 "turn: the novel, the short story, and the theatre of Vijay Tendulkar. A learner "
                 "who reads one abhanga and one page of modern prose has touched both ends of "
                 "seven hundred years."),
        source_url="https://en.wikipedia.org/wiki/Marathi_literature",
        reading=("समीक्षेत पहिला नियम असा: मापदंड आधी सांगावा. दुसरा नियम — प्रत्येक मुद्द्याला "
                 "उद्धरण द्यावे, कारण दावा पुराव्याशिवाय उभा राहत नाही. तिसरा नियम — "
                 "कादंबरीचा काळ आणि समाज समजून घ्यावा; संदर्भाशिवाय अर्थ लागत नाही. या "
                 "पुस्तकात शैली तरल आहे आणि स्त्री-पात्रांची वाटचाल विश्वासार्ह आहे. "
                 "दुसऱ्या भागाची उत्कटता वाढते, पण शेवटच्या प्रकरणात कालानुक्रम मोडल्याने "
                 "काही वाचक बुचकळ्यात पडतात. निष्कर्ष: चांगले पुस्तक, पण शेवट जास्त "
                 "स्पष्ट असावा."),
        reading_gloss=("In a review the first rule is: state the standard first. The second rule — "
                       "back every point with a quotation, because a claim cannot stand without "
                       "evidence. The third rule — understand the novel's period and society; "
                       "without context the sense does not come. In this book the style is fluid "
                       "and the arc of the women characters is believable. In the second part the "
                       "intensity rises, but because the chronological order is broken in the last "
                       "chapter some readers get bewildered. Conclusion: a good book, but the "
                       "ending should be clearer."),
        listening=("संपादक: पुस्तकाबद्दल तुमचा दृष्टिकोन काय?<br>"
                   "समीक्षक: पात्रांच्या दृष्टिकोनातून वाचले, पूर्वग्रह टाळला.<br>"
                   "संपादक: उणीव काय दिसली?<br>"
                   "समीक्षक: शेवटच्या प्रकरणात रचना ढिली वाटते.<br>"
                   "संपादक: पण स्त्री-पात्रांची वाटचाल बळकट आहे ना?<br>"
                   "समीक्षक: आहे, आणि तेच पुस्तकाचे बळ."),
        listening_gloss=("Editor: What is your standpoint on the book? Reviewer: I read it from the "
                         "characters' standpoint, avoiding prejudice. Editor: What shortcoming did "
                         "you see? Reviewer: In the last chapter the structure feels loose. "
                         "Editor: But the women characters' arc is strong, isn't it? Reviewer: It "
                         "is, and that is the book's strength."),
        voice_tag=VOICE,
        idioms=[
            ("डोळ्यांत तेल घालणे", "to pour oil into the eyes", "to hoodwink the reader"),
            ("दृष्ट लागणे", "to be touched by the evil eye", "a work that draws envy"),
            ("शब्दांची खान", "a mine of words", "a writer of inexhaustible vocabulary"),
            ("रस घेणे", "to take the flavour", "to read with relish"),
            ("पोटभर वाचन", "reading to the stomach", "reading to one's fill"),
            ("बुचकळ्यात पडणे", "to fall into perplexity", "to be bewildered"),
            ("कोरडा वाटणे", "to feel dry", "to feel lifeless, without play"),
            ("आठवणीत घर करणे", "to make a home in the memory", "a line that stays with you"),
            ("कानावर पडणे", "to fall on the ear", "to come to somebody's notice"),
            ("अंतरी रुजणे", "to take root within", "to settle deep in the mind"),
        ],
        mistakes=[
            ("या ओळीचा अर्थ लागतो.", "या ओळीचा अर्थ लागत नाही.", "Rule 3 is negative: संदर्भाशिवाय अर्थ लागत नाही."),
            ("शेवटी निष्कर्ष लिहावी.", "शेवटी निष्कर्ष लिहावा.", "निष्कर्ष is masculine: लिहावा."),
            ("पूर्वग्रह टाळली पाहिजे.", "पूर्वग्रह टाळला पाहिजे.", "पूर्वग्रह is masculine: टाळला."),
        ],
        task_title="Write a Marathi review of four short paragraphs",
        task_instructions=("Choose anything you have read or watched this month and write a Marathi "
                           "review in four paragraphs: परिचय with the period and the writer, two "
                           "मुद्दे each backed by an उद्धरण, one तोटा with evidence, and a निष्कर्ष. "
                           "Name your दृष्टिकोन in one sentence and keep पूर्वग्रह out of it."),
    ),
    "test": [
        ("translate_en", "Say: the poem is read aloud.", "कविता मोठ्याने वाचली जाते."),
        ("translate_mr", "संदर्भाशिवाय अर्थ लागत नाही.", "Without context it cannot be interpreted."),
        ("multiple_choice", "Which sentence names a simile?", "चेहरा चंद्रासारखा आहे."),
        ("fill_in_the_blank", "या कवितेत करुण ___ आहे.", "रस"),
        ("word_selection", "Select the Marathi for 'the plot's structure is firm'.", "कथानकाची रचना घट्ट आहे"),
        ("error_correction", "पूर्वग्रह टाळली पाहिजे.", "पूर्वग्रह टाळला पाहिजे."),
        ("dialogue_completion", "Complete: तुमचा दृष्टिकोन काय आहे? — ___ (I read from the characters' standpoint)", "पात्रांच्या दृष्टिकोनातून वाचतो"),
        ("matching", "Match उत्कटता to its meaning.", "intensity"),
        ("reading_comprehension", "कालानुक्रम मोडल्याने काय होते?", "some readers get bewildered"),
        ("inference", "पण शेवट जास्त स्पष्ट असावा. — what kind of sentence is this?", "a conclusion with a reservation"),
        ("main_idea", "दावा पुराव्याशिवाय उभा राहत नाही. — what does this rule ask for?", "evidence for every claim"),
        ("detail_identification", "समीक्षेत किती मुद्दे सुचवले आहेत?", "three"),
    ],
}

HALFSTEPS["B2+"] = {
    "title": "Marathi B2+ — Policy, contracts and figures",
    "native": NATIVE,
    "goals": [
        "Explain a policy and its conditions in the written register",
        "Read a contract clause, a figure and a trend out loud",
        "Present a proposal, answer an objection and promise a date",
    ],
    "units": [
        {"id": "B2+-U1", "title": "धोरण आणि नियम", "lessons": [
            L("धोरण समजावणे",
              "Formal Marathi runs on -ानुसार (धोरणानुसार, करारानुसार) and on लागू होणे for a rule "
              "that applies. अट is a condition and the exemptions are सवलती.",
              [V("धोरण", "dhoran", "policy", "noun"),
               V("अट", "at", "condition, clause", "noun"),
               V("लागू", "laagu", "applicable, in force", "adjective"),
               V("सवलत", "savlat", "concession, exemption", "noun"),
               V("अन्वये", "anvaye", "in accordance with", "postposition")],
              G("Saying how a rule applies",
                "धोरणानुसार लागू होते · अटी पूर्ण करा · अन्वये दिले जाईल",
                "The suffix -ानुसार attaches to the noun (धोरणानुसार, नियमानुसार) and अन्वये is "
                "the heavier written equivalent: अधिसूचनेच्या अन्वये. लागू होणे is for a rule that "
                "applies, and सवलत for a relaxation written into it.",
                [X("या धोरणानुसार अर्ज फेब्रुवारीपर्यंत द्यावा.", "Ya dhoran-anusar arj februvariparyant dyava.", "Under this policy the application must be given by February."),
                 X("अटी पूर्ण झाल्यास सवलत मिळेल.", "Ati purn jhalyas savlat milel.", "If the conditions are met, the concession will be given."),
                 X("अधिसूचनेच्या अन्वये हा नियम लागू होतो.", "Adhisuchanechya anvaye ha niyam laagu hoto.", "Under the notification this rule applies.")],
                [("धोरणानुसार नियम लागू आहेत.", "धोरणानुसार नियम लागू आहे.", "नियम is singular masculine: आहे."),
                 ("अट पूर्ण झाले.", "अट पूर्ण झाली.", "अट is feminine: झाली.")]),
              [D("अधिकारी", "अर्ज कसा द्यायचा?", "Arj kasa dyaycha?", "How is the application to be given?"),
               D("कर्मचारी", "धोरणानुसार अर्ज ऑनलाइन द्यावा लागतो.", "Dhoran-anusar arj online dyava lagto.", "Under the policy the application has to be given online."),
               D("अधिकारी", "आणि सवलत मिळते का?", "Aani savlat milte ka?", "And is a concession given?"),
               D("कर्मचारी", "फेब्रुवारीपर्यंत अटी पूर्ण झाल्यास मिळेल.", "Ferbhuvariparyant ati purn jhalyas milel.", "It will be given if the conditions are met by February.")],
              WS("Policy worksheet", [
                  T("Explain the rule.", ["under this policy the application must be given by February", "this rule applies under the notification"],
                    ["या धोरणानुसार अर्ज फेब्रुवारीपर्यंत द्यावा", "अधिसूचनेच्या अन्वये हा नियम लागू होतो"]),
                  T("State the condition.", ["if the conditions are met", "the concession will be given"],
                    ["अटी पूर्ण झाल्यास", "सवलत मिळेल"]),
              ])),
            L("तक्रार नोंदवणे",
              "A formal complaint is तक्रार (feminine) and it is नोंदवली. The remedy asked for is "
              "निवारण, the hearing सुनावणी, and the request is made with विनंती आहे.",
              [V("तक्रार", "takrar", "complaint", "noun"),
               V("निवारण", "nivaran", "remedy, redressal", "noun"),
               V("सुनावणी", "sunavni", "hearing", "noun"),
               V("विनंती", "vinanti", "request", "noun"),
               V("नोंदवणे", "nondavne", "to record, to register", "verb")],
              G("Recording a complaint",
                "तक्रार नोंदवली आहे · निवारणाची विनंती आहे · सुनावणी देण्यात यावी",
                "तक्रार takes नोंदवणे (नोंदवली). A request in the written register uses विनंती आहे "
                "with the noun in the genitive: निवारणाची विनंती आहे, सुनावणीची विनंती आहे. The "
                "optative -ावी is the formal way to ask for an action.",
                [X("मी लिखित तक्रार नोंदवली आहे.", "Mi likhit takrar nondavli ahe.", "I have registered a written complaint."),
                 X("निवारणाची विनंती आहे.", "Nivaranachi vinanti ahe.", "A remedy is requested."),
                 X("सुनावणी देण्यात यावी.", "Sunavni denyat yavi.", "A hearing may kindly be given.")],
                [("तक्रार नोंदवला आहे.", "तक्रार नोंदवली आहे.", "तक्रार is feminine: नोंदवली."),
                 ("निवारण विनंती आहे.", "निवारणाची विनंती आहे.", "The noun takes the genitive: निवारणाची विनंती.")]),
              [D("ग्राहक", "लिखित तक्रार नोंदवली आहे.", "Likhit takrar nondavli ahe.", "I have registered a written complaint."),
               D("अधिकारी", "तक्रार कशी आहे?", "Takrar kashi ahe?", "What is the complaint about?"),
               D("ग्राहक", "देयक दोनदा भरूनही सेवा बंद आहे. निवारणाची विनंती आहे.", "Deyak dondaa bharunhi seva band ahe. Nivaranachi vinanti ahe.", "The bill was paid twice and yet the service is off. A remedy is requested."),
               D("अधिकारी", "पंधरा दिवसांत सुनावणी देण्यात येईल.", "Pandhra divsant sunavni denyat yeil.", "A hearing will be given within fifteen days.")],
              WS("Complaint worksheet", [
                  T("Record the complaint.", ["I have registered a written complaint", "the bill was paid twice"],
                    ["लिखित तक्रार नोंदवली आहे", "देयक दोनदा भरले"]),
                  T("Ask formally.", ["a remedy is requested", "a hearing may kindly be given"],
                    ["निवारणाची विनंती आहे", "सुनावणी देण्यात यावी"]),
              ])),
            L("आकडेवारी वाचणे",
              "Figures are आकडेवारी, the trend is कल, growth वाढ (feminine) and decline घट "
              "(feminine). A comparison uses च्या तुलनेत, and a percentage टक्के. The figure stands before the noun "
              "(दहा टक्के वाढ) and the trend word carries the verb: वाढ झाली, घट झाली, प्रमाण वाढले.",
              [V("आकडेवारी", "aakdevari", "statistics", "noun"),
               V("वाढ", "vaadh", "growth, increase", "noun"),
               V("घट", "ghat", "decrease, decline", "noun"),
               V("तुलना", "tulna", "comparison", "noun"),
               V("प्रमाण", "praman", "proportion, rate", "noun")],
              G("Reading a trend",
                "गेल्या वर्षाच्या तुलनेत दहा टक्के वाढ · घट झाली · प्रमाण वाढले",
                "The comparison is च्या तुलनेत, and the figure is read before टक्के: दहा टक्के. "
                "वाढ and घट are feminine and take झाली, while प्रमाण is neuter: प्रमाण वाढले.",
                [X("गेल्या वर्षाच्या तुलनेत दहा टक्के वाढ झाली.", "Gelya varshachya tulnet daha tekke vaadh jhali.", "Compared with last year there was a ten per cent increase."),
                 X("दुसऱ्या तिमाहीत घट झाली.", "Dusrya timahit ghat jhali.", "There was a decline in the second quarter."),
                 X("निर्यातीचे प्रमाण वाढले आहे.", "Niryatichi praman vaadhle ahe.", "The share of exports has risen.")],
                [("दहा टक्के वाढ झाला.", "दहा टक्के वाढ झाली.", "वाढ is feminine: झाली."),
                 ("प्रमाण वाढली.", "प्रमाण वाढले.", "प्रमाण is neuter: वाढले.")]),
              [D("अधिकारी", "यंदाची आकडेवारी सांगा.", "Yandachi aakdevari sanga.", "Give this year's figures."),
               D("विश्लेषक", "गेल्या वर्षाच्या तुलनेत उत्पादनात आठ टक्के वाढ झाली.", "Gelya varshachya tulnet utpadanat aath tekke vaadh jhali.", "Compared with last year production rose by eight per cent."),
               D("अधिकारी", "आणि खर्च?", "Aani kharch?", "And the expenditure?"),
               D("विश्लेषक", "खर्चाचे प्रमाण वाढले, पण घट दिसत आहे.", "Kharchache praman vaadhle, pan ghat disto ahe.", "The expenditure rate has risen, but a decline is visible.")],
              WS("Figures worksheet", [
                  T("Read the trend.", ["there was a ten per cent increase", "there was a decline in the second quarter"],
                    ["दहा टक्के वाढ झाली", "दुसऱ्या तिमाहीत घट झाली"]),
                  T("Compare the years.", ["compared with last year production rose", "the share of exports has risen"],
                    ["गेल्या वर्षाच्या तुलनेत उत्पादन वाढले", "निर्यातीचे प्रमाण वाढले आहे"]),
              ])),
        ]},
        {"id": "B2+-U2", "title": "करार आणि जोखीम", "lessons": [
            L("कराराच्या अटी",
              "A contract is करार and its terms अटी; the period is कालावधी and the penalty दंड. "
              "Breach is भंग, and the obligation is stated with -ावे लागेल or करारबद्ध आहे.",
              [V("करार", "karar", "contract, agreement", "noun"),
               V("अटी", "ati", "terms, conditions", "noun"),
               V("कालावधी", "kalavdhi", "period, term", "noun"),
               V("दंड", "dand", "penalty", "noun"),
               V("भंग", "bhang", "breach", "noun")],
              G("Reading the clause",
                "करारानुसार · पंधरा दिवसांत पूर्तता करावी लागेल · अटींचा भंग झाल्यास दंड",
                "करारानुसार introduces the clause, and the obligation takes -ावी/-ावा लागेल "
                "according to the noun's gender: पूर्तता करावी लागेल, अहवाल द्यावा लागेल. Breach is "
                "भंग झाल्यास, and the penalty is लागू होईल.",
                [X("करारानुसार पंधरा दिवसांत पूर्तता करावी लागेल.", "Karar-anusar pandhra divsant purtata karavi lagel.", "Under the contract the delivery must be made in fifteen days."),
                 X("कालावधी संपल्यावर करार नूतनीकरण करता येईल.", "Kalavdhi samplyavar karar nutnikaran karta yeil.", "Once the period ends the contract can be renewed."),
                 X("अटींचा भंग झाल्यास दंड लागू होईल.", "Atincha bhang jhalyas dand laagu hoil.", "If the terms are breached a penalty will apply.")],
                [("करारानुसार अहवाल द्यावी लागेल.", "करारानुसार अहवाल द्यावा लागेल.", "अहवाल is masculine: द्यावा लागेल."),
                 ("कालावधी संपली आहे.", "कालावधी संपला आहे.", "कालावधी is masculine: संपला.")]),
              [D("व्यवस्थापक", "कराराचा कालावधी किती आहे?", "Kararacha kalavdhi kiti ahe?", "What is the term of the contract?"),
               D("वकील", "वर्षभर. पंधरा दिवसांत पूर्तता करावी लागेल.", "Varshabhar. Pandhra divsant purtata karavi lagel.", "One year. The delivery must be made in fifteen days."),
               D("व्यवस्थापक", "उशीर झाला तर?", "Ushir jhala tar?", "And if there is a delay?"),
               D("वकील", "अटींचा भंग झाल्यास दंड लागू होईल.", "Atincha bhang jhalyas dand laagu hoil.", "If the terms are breached a penalty will apply.")],
              WS("Contract worksheet", [
                  T("Read the clause.", ["the delivery must be made in fifteen days", "the contract can be renewed"],
                    ["पंधरा दिवसांत पूर्तता करावी लागेल", "करार नूतनीकरण करता येईल"]),
                  T("Name the consequence.", ["if the terms are breached", "a penalty will apply"],
                    ["अटींचा भंग झाल्यास", "दंड लागू होईल"]),
              ])),
            L("जोखीम आणि तयारी",
              "Risk is जोखीम (feminine) and it is कमी करण्यासाठी that provisions are made: "
              "आरक्षित निधी, विमा, पर्यायी व्यवस्था. Planning ahead is पूर्वतयारी, and the purpose clause "
              "always ends in -साठी: जोखीम कमी करण्यासाठी पर्यायी व्यवस्था ठेवली आहे.",
              [V("जोखीम", "jokhim", "risk", "noun"),
               V("विमा", "vima", "insurance", "noun"),
               V("पूर्वतयारी", "purvatayari", "advance preparation", "noun"),
               V("पर्यायी", "paryayi", "alternative", "adjective"),
               V("आरक्षित", "aarakshit", "reserved", "adjective")],
              G("Reducing a risk",
                "जोखीम कमी करण्यासाठी · पर्यायी व्यवस्था ठेवली आहे · पूर्वतयारी केली आहे",
                "जोखीम कमी करण्यासाठी is the purpose clause (करण्यासाठी), and हेतू takes -साठी "
                "throughout the written register. Preparations take केली आहे (feminine) or ठेवली "
                "आहे, and the fallback is पर्यायी व्यवस्था.",
                [X("जोखीम कमी करण्यासाठी पूर्वतयारी केली आहे.", "Jokhim kami karnyasathi purvatayari keli ahe.", "Advance preparation has been made to reduce the risk."),
                 X("पर्यायी व्यवस्था ठेवली आहे.", "Paryayi vyavastha thevli ahe.", "An alternative arrangement has been kept."),
                 X("विम्याचा खर्च आरक्षित निधीतून येईल.", "Vimyacha kharch aarakshit nidhitun yeil.", "The insurance cost will come from the reserve fund.")],
                [("जोखीम वाढला.", "जोखीम वाढली.", "जोखीम is feminine: वाढली."),
                 ("पर्यायी व्यवस्था ठेवला.", "पर्यायी व्यवस्था ठेवली.", "व्यवस्था is feminine: ठेवली.")]),
              [D("व्यवस्थापक", "या कामात जोखीम किती आहे?", "Ya kamat jokhim kiti ahe?", "How much risk is there in this work?"),
               D("अभियंता", "जास्त नाही, पण पूर्वतयारी केली आहे.", "Jaast nahi, pan purvatayari keli ahe.", "Not much, but advance preparation has been made."),
               D("व्यवस्थापक", "काय ठेवले आहे?", "Kay thevle ahe?", "What has been kept?"),
               D("अभियंता", "विमा, आरक्षित निधी आणि पर्यायी व्यवस्था — तीन्ही.", "Vima, aarakshit nidhi aani paryayi vyavastha — tinhi.", "Insurance, a reserve fund and an alternative arrangement — all three.")],
              WS("Risk worksheet", [
                  T("Explain the preparation.", ["advance preparation has been made", "an alternative arrangement has been kept"],
                    ["पूर्वतयारी केली आहे", "पर्यायी व्यवस्था ठेवली आहे"]),
                  T("Name the safeguards.", ["insurance and a reserve fund", "the risk is not much"],
                    ["विमा आणि आरक्षित निधी", "जोखीम जास्त नाही"]),
              ])),
            L("सूचना आणि अमलबजावणी",
              "A suggestion is सूचना and it is मान्य केली; implementation is अंमलबजावणी and it होते "
              "or केली जाते. Putting something into force is अमलात आणणे.",
              [V("मान्यता", "manyata", "approval", "noun"),
               V("अंमलबजावणी", "amalbajaavni", "implementation", "noun"),
               V("कार्यवाही", "karyavahi", "proceeding, action", "noun"),
               V("दुरुस्ती", "durusti", "amendment", "noun"),
               V("पूर्तता", "purtata", "fulfilment, delivery", "noun")],
              G("From suggestion to action",
                "सूचना मान्य केली · अंमलबजावणी सुरू होईल · दुरुस्ती सुचवली आहे",
                "A suggestion is मान्य केली (सूचना is feminine), implementation सुरू होते, and an "
                "amendment is सुचवली (दुरुस्ती सुचवली आहे). The formal passive अमलात आणले जाईल "
                "closes the chain.",
                [X("समितीने सूचना मान्य केली.", "Samitine suchana manya keli.", "The committee approved the suggestion."),
                 X("पुढच्या महिन्यात अंमलबजावणी सुरू होईल.", "Pudchya mahinyat amalbajaavni suru hoil.", "Implementation will begin next month."),
                 X("एका कलमात दुरुस्ती सुचवली आहे.", "Eka kalmat durusti suchavli ahe.", "An amendment has been suggested in one clause.")],
                [("सूचना मान्य केला.", "सूचना मान्य केली.", "सूचना is feminine: केली."),
                 ("अंमलबजावणी सुरू होतील.", "अंमलबजावणी सुरू होईल.", "अंमलबजावणी is singular feminine: होईल.")]),
              [D("सदस्य", "सूचनेचे काय झाले?", "Suchaneche kay jhale?", "What happened to the suggestion?"),
               D("सचिव", "समितीने सूचना मान्य केली आहे.", "Samitine suchana manya keli ahe.", "The committee has approved the suggestion."),
               D("सदस्य", "अंमलबजावणी कधी सुरू होईल?", "Amalbajaavni kadhi suru hoil?", "When will the implementation begin?"),
               D("सचिव", "पुढच्या महिन्यात, एका कलमात दुरुस्ती झाल्यावर.", "Pudchya mahinyat, eka kalmat durusti jhalyavar.", "Next month, after an amendment in one clause.")],
              WS("Implementation worksheet", [
                  T("Report the approval.", ["the committee approved the suggestion", "an amendment has been suggested in one clause"],
                    ["समितीने सूचना मान्य केली", "एका कलमात दुरुस्ती सुचवली आहे"]),
                  T("Fix the start.", ["implementation will begin next month", "when will the implementation begin?"],
                    ["पुढच्या महिन्यात अंमलबजावणी सुरू होईल", "अंमलबजावणी कधी सुरू होईल?"]),
              ])),
        ]},
        {"id": "B2+-U3", "title": "प्रस्ताव आणि उत्तर", "lessons": [
            L("प्रस्ताव मांडणे",
              "A proposal is प्रस्ताव or निवेदन and it is सादर केला जातो. मान्यता is approval, "
              "and the supporting documents are कागदपत्रे. The proposal is सादर केला जातो, its papers "
              "जोडली जातात, and approval मिळते.",
              [V("प्रस्ताव", "prastav", "proposal", "noun"),
               V("निवेदन", "nivedan", "representation, statement", "noun"),
               V("सादर", "saadar", "presented, submitted", "adjective"),
               V("कागदपत्रे", "kagadpatre", "documents", "noun"),
               V("मान्यता", "manyata", "approval", "noun")],
              G("Formal presentation",
                "प्रस्ताव सादर करत आहे · सोबत कागदपत्रे जोडली आहेत · मान्यता मिळाल्यास",
                "सादर करणे is the written verb for submitting: प्रस्ताव सादर करत आहे. Documents "
                "are जोडली जातात (कागदपत्रे जोडली आहेत), and approval is मिळणे: मान्यता मिळाल्यास "
                "काम सुरू होईल.",
                [X("मी पहिला प्रस्ताव सादर करत आहे.", "Mi pahila prastav saadar karat ahe.", "I am presenting the first proposal."),
                 X("सोबत सहा कागदपत्रे जोडली आहेत.", "Sobat saha kagadpatre jodli aahet.", "Six documents have been attached with it."),
                 X("मान्यता मिळाल्यास पुढचा टप्पा सुरू होईल.", "Manyata milalyas pudcha tappa suru hoil.", "If approval is received the next stage will begin.")],
                [("मी प्रस्ताव सादर करतो आहे.", "मी प्रस्ताव सादर करत आहे.", "The progressive takes सादर करत आहे."),
                 ("कागदपत्रे जोडली आहे.", "कागदपत्रे जोडली आहेत.", "कागदपत्रे is plural neuter: आहेत.")]),
              [D("सदस्य", "प्रस्ताव सादर करत आहे.", "Prastav saadar karat ahe.", "I am presenting the proposal."),
               D("अध्यक्ष", "कागदपत्रे जोडली आहेत का?", "Kagadpatre jodli aahet ka?", "Are the documents attached?"),
               D("सदस्य", "हो, सहा कागदपत्रे आणि खर्चाचा तपशील.", "Ho, saha kagadpatre aani kharchacha tapshil.", "Yes, six documents and the expenditure detail."),
               D("अध्यक्ष", "मान्यता मिळाल्यास काम कधी सुरू होईल?", "Manyata milalyas kaam kadhi suru hoil?", "If approval comes, when will the work begin?")],
              WS("Proposal worksheet", [
                  T("Present it.", ["I am presenting the proposal", "six documents have been attached"],
                    ["मी प्रस्ताव सादर करत आहे", "सहा कागदपत्रे जोडली आहेत"]),
                  T("Look ahead.", ["if approval is received the next stage will begin", "the expenditure detail"],
                    ["मान्यता मिळाल्यास पुढचा टप्पा सुरू होईल", "खर्चाचा तपशील"]),
              ])),
            L("आक्षेप आणि खुलासा",
              "An objection is आक्षेप (masculine) and the answer to it is खुलासा. Evidence is "
              "पुरावा, and a claim is दावा — खुलासा देताना the tone stays impersonal.",
              [V("खुलासा", "khulasa", "clarification, explanation", "noun"),
               V("पुरावा", "purava", "evidence, proof", "noun"),
               V("दावा", "dava", "claim", "noun"),
               V("स्पष्ट", "spasht", "clear, explicit", "adjective"),
               V("नोंद", "nond", "note, record", "noun")],
              G("Answering an objection",
                "आक्षेप नोंदवला आहे · खुलासा देतो · पुरावा सोबत आहे",
                "The objection arrives with नोंदवला (आक्षेप नोंदवला आहे), the answer is खुलासा "
                "देणे, and the backing is पुरावा. A claim that cannot be backed is stated with "
                "नोंदीवर आधारित आहे — grounded in the record.",
                [X("आपला आक्षेप नोंदवला आहे, खुलासा देतो.", "Aapla aakshep nondavla ahe, khulasa deto.", "Your objection is noted; I offer a clarification."),
                 X("पुरावा सोबत जोडलेला आहे.", "Purava sobat jodlela ahe.", "The evidence is attached."),
                 X("हा दावा नोंदींवर आधारित आहे.", "Ha dava nondinvar aadharit ahe.", "This claim is based on the record.")],
                [("पुरावा सोबत जोडलेली आहे.", "पुरावा सोबत जोडलेला आहे.", "पुरावा is masculine: जोडलेला."),
                 ("हा दावा नोंदींवर आधारित आहेत.", "हा दावा नोंदींवर आधारित आहे.", "दावा is masculine singular: आहे.")]),
              [D("सदस्य २", "खर्चाबद्दल मला आक्षेप आहे.", "Kharchabaddal mala aakshep ahe.", "I have an objection about the expenditure."),
               D("सदस्य १", "आपला आक्षेप नोंदवला आहे, खुलासा देतो.", "Aapla aakshep nondavla ahe, khulasa deto.", "Your objection is noted; I offer a clarification."),
               D("सदस्य २", "पुरावा काय आहे?", "Purava kay ahe?", "What is the evidence?"),
               D("सदस्य १", "गेल्या वर्षाची नोंद आणि कागदपत्रे, दोन्ही सोबत आहेत.", "Gelya varshachi nond aani kagadpatre, donhi sobat aahet.", "Last year's record and the documents, both are attached.")],
              WS("Objection worksheet", [
                  T("Note the objection.", ["your objection is noted", "I offer a clarification"],
                    ["आपला आक्षेप नोंदवला आहे", "खुलासा देतो"]),
                  T("Offer the evidence.", ["the evidence is attached", "this claim is based on the record"],
                    ["पुरावा सोबत जोडलेला आहे", "हा दावा नोंदींवर आधारित आहे"]),
              ])),
            L("कालमर्यादा आणि पूर्तता",
              "A deadline is कालमर्यादा and it संपते or पाळली जाते; पूर्तता होणे is to be fulfilled. "
              "The report of fulfilment is अहवाल and the periodical one is नियतकालिक अहवाल.",
              [V("कालमर्यादा", "kalamaryada", "deadline, time limit", "noun"),
               V("पूर्तता", "purtata", "fulfilment", "noun"),
               V("अहवाल", "ahaval", "report", "noun"),
               V("पाळणे", "paalne", "to keep, to observe", "verb"),
               V("तपशील", "tapshil", "detail", "noun")],
              G("Meeting the deadline",
                "कालमर्यादा पाळली जाईल · पूर्तता झाल्याचा अहवाल द्यावा · तपशील जोडा",
                "कालमर्यादा पाळली जाते (feminine passive) and पूर्तता होते. The report of what was "
                "done takes -ाचा अहवाल: पूर्तता झाल्याचा अहवाल. Instructions in the written "
                "register end in -ावा/-ावी.",
                [X("कालमर्यादा पाळली जाईल.", "Kalamaryada paalli jail.", "The deadline will be kept."),
                 X("पूर्तता झाल्याचा अहवाल पंधरा दिवसांत द्यावा.", "Purtata jhalyacha ahaval pandhra divsant dyava.", "The report of completion must be given in fifteen days."),
                 X("अहवालासोबत खर्चाचा तपशील जोडावा.", "Ahavalasobat kharchacha tapshil jodava.", "The expenditure detail must be attached with the report.")],
                [("कालमर्यादा पाळला जाईल.", "कालमर्यादा पाळली जाईल.", "कालमर्यादा is feminine: पाळली जाईल."),
                 ("अहवाल द्यावी.", "अहवाल द्यावा.", "अहवाल is masculine: द्यावा.")]),
              [D("व्यवस्थापक", "कालमर्यादा पाळली जाईल का?", "Kalamaryada paalli jail ka?", "Will the deadline be kept?"),
               D("प्रकल्प प्रमुख", "हो. पूर्तता झाल्याचा अहवाल देतो.", "Ho. Purtata jhalyacha ahaval deto.", "Yes. I will give the report of completion."),
               D("व्यवस्थापक", "सोबत काय जोडावे?", "Sobat kay jodave?", "What should be attached with it?"),
               D("प्रकल्प प्रमुख", "खर्चाचा तपशील आणि पुढच्या टप्प्याची नोंद.", "Kharchacha tapshil aani pudchya tappyachi nond.", "The expenditure detail and the note on the next stage.")],
              WS("Deadline worksheet", [
                  T("Promise the deadline.", ["the deadline will be kept", "the report must be given in fifteen days"],
                    ["कालमर्यादा पाळली जाईल", "अहवाल पंधरा दिवसांत द्यावा"]),
                  T("Attach the detail.", ["the expenditure detail must be attached", "the note on the next stage"],
                    ["खर्चाचा तपशील जोडावा", "पुढच्या टप्प्याची नोंद"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Maharashtra's economy is a workshop and a farm at once: the Mumbai–Pune–Nashik "
                 "belt carries a large share of India's engineering and pharmaceutical output, "
                 "the sugar cooperatives of the Deccan turned into a political school for the "
                 "rural Marathi elite, and Pune now writes software in between the automobile "
                 "plants. The state's economy is the largest of any Indian state, contributing about a "
                 "fifth of national industrial output. For a learner the useful part is the vocabulary of the world it "
                 "runs on: कारखाना, उत्पादन, सहकारी संस्था, निर्यात."),
        source_url="https://en.wikipedia.org/wiki/Economy_of_Maharashtra",
        reading=("राज्याची आकडेवारी मागच्या तिमाहीत मिश्र होती. गेल्या वर्षाच्या तुलनेत उत्पादनात "
                 "सहा टक्के वाढ झाली, पण खर्चाचे प्रमाणही वाढले. सहकारी संस्थांनी "
                 "शेतकऱ्यांना वेळेवर देयक दिले. निर्यातीत मात्र घट दिसली. प्रकल्पांची "
                 "कालमर्यादा पाळली गेली नाही, म्हणून निवारणाची सुनावणी ठरवली आहे. "
                 "जोखीम कमी करण्यासाठी आरक्षित निधी वाढवला जाईल आणि पुढच्या अहवालासोबत "
                 "खर्चाचा तपशील जोडला जाईल."),
        reading_gloss=("The state's figures were mixed in the last quarter. Compared with last "
                       "year production rose by six per cent, but the rate of expenditure also "
                       "rose. The cooperative institutions paid the farmers on time. In exports, "
                       "however, a decline was seen. Project deadlines were not kept, so a "
                       "redressal hearing has been fixed. To reduce the risk the reserve fund "
                       "will be increased, and the expenditure detail will be attached with the "
                       "next report."),
        listening=("अध्यक्ष: आकडेवारीचा तपशील सादर करा.<br>"
                   "विश्लेषक: उत्पादनात सहा टक्के वाढ, निर्यातीत घट.<br>"
                   "अध्यक्ष: घटीचे कारण?<br>"
                   "विश्लेषक: दोन प्रकल्पांची कालमर्यादा पाळली गेली नाही.<br>"
                   "अध्यक्ष: मग निवारणाची विनंती नोंदवा आणि पुढच्या अहवालासोबत तपशील जोडा."),
        listening_gloss=("Chairperson: Present the detail of the figures. Analyst: A six per cent "
                         "rise in production, a decline in exports. Chairperson: The reason for "
                         "the decline? Analyst: The deadlines of two projects were not kept. "
                         "Chairperson: Then record a request for redressal and attach the detail "
                         "with the next report."),
        voice_tag=VOICE,
        idioms=[
            ("कंबर कसणे", "to tighten the belt", "to brace for hard work"),
            ("अटीतटीचा प्रश्न", "a question of clauses and levels", "a knotty, unsettled question"),
            ("हातचे राखणे", "to keep what is in the hand", "to keep something in reserve"),
            ("पंचाईत होणे", "to be caught in the village council", "to be in a tight spot"),
            ("डोळ्यांत तेल घालणे", "to pour oil in the eyes", "to hoodwink somebody"),
            ("तोंडावर बोलणे", "to speak on the face", "to say it to somebody's face"),
            ("कानाडोळा करणे", "to make the ear an eye's path", "to turn a deaf ear"),
            ("डोळे उघडणे", "to open the eyes", "to see the reality at last"),
            ("तारेवरची कसरत", "a feat on the wire", "a tightrope act"),
            ("शब्द पाळणे", "to keep the word", "to keep one's promise"),
        ],
        mistakes=[
            ("दहा टक्के वाढ झाला.", "दहा टक्के वाढ झाली.", "वाढ is feminine: झाली."),
            ("कालमर्यादा पाळला जाईल.", "कालमर्यादा पाळली जाईल.", "कालमर्यादा is feminine: पाळली जाईल."),
            ("सूचना मान्य केला.", "सूचना मान्य केली.", "सूचना is feminine: केली."),
        ],
        task_title="Write one formal Marathi note of six to eight sentences",
        task_instructions=("Take a small decision anyone could make — a school trip, a shop rule, a "
                           "society repair — and write a formal note in Marathi: the policy line "
                           "with धोरणानुसार, the condition with झाल्यास, one figure with टक्के, the "
                           "risk and the preparation with करण्यासाठी, and the deadline with "
                           "कालमर्यादा पाळली जाईल. Close with an instruction in -ावे/-ावी."),
    ),
    "test": [
        ("translate_en", "Say: compared with last year there was a ten per cent increase.", "गेल्या वर्षाच्या तुलनेत दहा टक्के वाढ झाली."),
        ("translate_mr", "कालमर्यादा पाळली जाईल.", "The deadline will be kept."),
        ("multiple_choice", "Which sentence is a formal request for a remedy?", "निवारणाची विनंती आहे."),
        ("fill_in_the_blank", "अटींचा ___ झाल्यास दंड लागू होईल.", "भंग"),
        ("word_selection", "Select the Marathi for 'in accordance with the notification'.", "अधिसूचनेच्या अन्वये"),
        ("error_correction", "दहा टक्के वाढ झाला.", "दहा टक्के वाढ झाली."),
        ("dialogue_completion", "Complete: मान्यता मिळाल्यास काम कधी सुरू होईल? — ___ (the next stage will begin)", "पुढचा टप्पा सुरू होईल"),
        ("matching", "Match पूर्वतयारी to its meaning.", "advance preparation"),
        ("reading_comprehension", "निर्यातीत काय दिसले?", "a decline"),
        ("inference", "प्रकल्पांची कालमर्यादा पाळली गेली नाही. — what follows in the note?", "a redressal hearing is fixed"),
        ("main_idea", "जोखीम कमी करण्यासाठी आरक्षित निधी वाढवला जाईल. — what is this sentence?", "a measure against risk"),
        ("detail_identification", "अहवालासोबत काय जोडले जाईल?", "the expenditure detail"),
    ],
}

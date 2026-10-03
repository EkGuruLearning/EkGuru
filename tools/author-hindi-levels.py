# -*- coding: utf-8 -*-
"""Hindi PHASE 1 depth — the `level.extra` block for each CEFR rung.

PHASE 1 (content depth) needs every published level page to carry more than
drills: a culture note with a real source, an original reading text, a listening
script with the language's voice tag, ten idioms, the mistakes that level
actually makes, and a task. The schema has required this block all along
(`data/schemas/course-t1.schema.json` -> $defs/extra) but no course file carried
it and no tool rendered it, so it was invisible on both sides.

This file is the authored Hindi content. `tools/build-course-levels.py` renders
it (extra_block()) onto languages/hi/level/<rung>/.

Every text here is written for Hindi, not translated from another language's
block: the culture note cites a source, the reading text and the listening
script are EkGuru's own (reading.original = true), and the idioms and mistakes
are the ones a Hindi learner at that rung actually meets.

Run:  python3 tools/author-hindi-levels.py           write the blocks
      python3 tools/author-hindi-levels.py --check   report drift only
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOICE = "hi-IN"          # registry.json -> languages[code=hi].speech_tag

HI_EXTRA: dict[str, dict] = {
    # ── A1 ──────────────────────────────────────────────────────────────────
    "A1": {
        "culture": {
            "text": ("नमस्ते namaste is not one word but two: नमस् namas, ‘a bow’, plus ते te, ‘to you’ — "
                     "literally ‘a bow to you’. That is why it works at any hour: it never names a time of "
                     "day. Palms together at chest height, a small nod, and it is complete. Add जी jī to a "
                     "name or a word to raise the respect: प्रकाश जी, हाँ जी, नहीं जी. On the telephone जी "
                     "often means simply ‘yes, I am listening’."),
            "source_url": "https://en.wikipedia.org/wiki/Namaste",
        },
        "reading": {
            "text": ("मैं प्रकाश हूँ। यह मेरा घर है। यह मेरी बहन है। उसका नाम मीरा है। "
                     "यहाँ एक कुर्सी है और एक मेज़ है। मेरे पास एक किताब है। "
                     "क्या आप ठीक हैं? मैं ठीक हूँ, धन्यवाद। हम जयपुर में रहते हैं।"),
            "gloss": ("I am Prakash. This is my house. This is my sister. Her name is Meera. "
                      "Here is a chair and a table. I have a book. Are you well? I am well, thank you. "
                      "We live in Jaipur."),
            "original": True,
        },
        "listening": {
            "script": ("नमस्ते! मैं प्रकाश हूँ। यह मेरी बहन है। उसका नाम मीरा है। "
                       "हम जयपुर में रहते हैं। आप कहाँ रहते हैं?"),
            "gloss": "Hello! I am Prakash. This is my sister. Her name is Meera. We live in Jaipur. Where do you live?",
            "voice_tag": VOICE,
        },
        "idioms": [
            {"t": "नमस्ते", "literal": "a bow to you", "meaning": "hello — at any hour, to anyone; it never names a time of day"},
            {"t": "धन्यवाद", "literal": "thanks-giving", "meaning": "thank you — the formal one; शुक्रिया is what people actually say"},
            {"t": "शुक्रिया", "literal": "thanks (borrowed from Persian)", "meaning": "thanks — everyday, used by everybody, no register problem"},
            {"t": "कृपया", "literal": "with kindness", "meaning": "please — more often written on a notice than spoken aloud"},
            {"t": "माफ़ कीजिए", "literal": "forgive (me)", "meaning": "excuse me / sorry — for interrupting or squeezing past someone"},
            {"t": "कोई बात नहीं", "literal": "no matter at all", "meaning": "never mind, it is fine — the standard reply to an apology"},
            {"t": "ठीक है", "literal": "it is right", "meaning": "okay — also means ‘agreed’, and, with a flat voice, ‘that is enough’"},
            {"t": "क्या हाल है?", "literal": "what is the state?", "meaning": "how are you? — friends and family, never a stranger"},
            {"t": "बहुत अच्छा", "literal": "very good", "meaning": "very good — and also ‘how nice!’, when someone tells you their news"},
            {"t": "चलिए", "literal": "let us go", "meaning": "come on, let us go — the respectful form; चलो with friends your own age"},
        ],
        "mistakes": [
            {"wrong": "मैं ठीक हूँ है।", "right": "मैं ठीक हूँ।",
             "why": "हूँ already means ‘am’. है is the third-person partner of the same verb; a sentence never carries both."},
            {"wrong": "मेरा नाम प्रकाश हूँ।", "right": "मेरा नाम प्रकाश है।",
             "why": "a name is not ‘I’ — it is third person, so है. हूँ is only ever for मैं."},
            {"wrong": "आप कैसे हैं? (to a woman)", "right": "आप कैसी हैं? (to a woman) · आप कैसे हैं? (to a man)",
             "why": "in the respectful plural the adjective still agrees with the person’s gender: कैसी for a woman, कैसे for a man."},
        ],
        "task": {
            "title": "Introduce three people, out loud",
            "instructions": ("Write five sentences: your name, where you live, and one thing about three different "
                             "people — a friend, someone in your family, and someone older than you. Use तुम for the "
                             "friend, आप for the older person, and जी on one name. Then read it aloud twice: the second "
                             "time with the page face down."),
        },
    },

    # ── A2 ──────────────────────────────────────────────────────────────────
    "A2": {
        "culture": {
            "text": ("होली Holi is a spring festival, and it is also the most useful vocabulary lesson in the "
                     "calendar. The night before is होलिका दहन holikā dahan, a bonfire; the day itself is रंग rāng, "
                     "colour, thrown as dry गुलाल gulāl powder or shot from a पिचकारी pichkārī, a water syringe. "
                     "Strangers are fair game and the greeting is बुरा न मानो, होली है — ‘don’t take offence, it is Holi’."),
            "source_url": "https://en.wikipedia.org/wiki/Holi",
        },
        "reading": {
            "text": ("सुबह आठ बजे हैं। मैं बाज़ार जाता हूँ। बाज़ार में बहुत भीड़ है। "
                     "मैं दो किलो आलू और एक किलो टमाटर खरीदता हूँ। दुकानदार कहता है, “पचास रुपये।” "
                     "मैं कहता हूँ, “थोड़ा कम कर दीजिए।” वह हँसता है और कहता है, “ठीक है, पैंतालीस।” "
                     "मैं घर वापस आता हूँ और चाय बनाता हूँ।"),
            "gloss": ("It is eight in the morning. I go to the market. The market is very crowded. I buy two kilos of "
                      "potatoes and one kilo of tomatoes. The shopkeeper says, “Fifty rupees.” I say, “Make it a little "
                      "less.” He laughs and says, “Fine, forty-five.” I come back home and make tea."),
            "original": True,
        },
        "listening": {
            "script": ("— भैया, यह कुर्ता कितने का है?\n"
                       "— चार सौ रुपये, दीदी।\n"
                       "— चार सौ? बहुत ज़्यादा है। तीन सौ में दीजिए।\n"
                       "— नहीं दीदी, तीन सौ पचास का है। आप के लिए तीन सौ बीस।\n"
                       "— ठीक है, पैक कर दीजिए।"),
            "gloss": ("— Brother, how much is this kurta?\n— Four hundred rupees, sister.\n— Four hundred? That is "
                      "too much. Give it for three hundred.\n— No, sister, it costs me three hundred fifty. For you, "
                      "three hundred twenty.\n— Fine, pack it."),
            "voice_tag": VOICE,
        },
        "idioms": [
            {"t": "चलता है", "literal": "it goes", "meaning": "it will do, it is good enough — the shrug that ends an argument about quality"},
            {"t": "ऐसे ही", "literal": "just like that", "meaning": "for no reason, nothing special — the answer to क्यों?"},
            {"t": "क्या बात है!", "literal": "what a thing!", "meaning": "nice one! — genuine appreciation of something clever"},
            {"t": "फिर मिलेंगे", "literal": "we will meet again", "meaning": "see you — the normal goodbye, with no date attached"},
            {"t": "जल्दी क्या है?", "literal": "what is the hurry?", "meaning": "relax, there is no rush — also a polite way to stall a request"},
            {"t": "जैसा आप कहें", "literal": "as you say", "meaning": "whatever you prefer — the polite deferral when you disagree"},
            {"t": "एक मिनट", "literal": "one minute", "meaning": "hold on a moment — used on the phone and at counters, never literally a minute"},
            {"t": "मुझे नहीं पता", "literal": "it is not known to me", "meaning": "I don’t know — the honest answer; add माफ़ कीजिए to soften it"},
            {"t": "थोड़ा-थोड़ा", "literal": "little by little", "meaning": "a bit — the standard understatement for ‘I know some of that language’"},
            {"t": "कोई न कोई", "literal": "some one or another", "meaning": "one or another, somehow — when you cannot name who or how"},
        ],
        "mistakes": [
            {"wrong": "मैंने किताब है।", "right": "मेरे पास किताब है।",
             "why": "Hindi has no verb ‘to have’. Possession is the postposition पास plus होना: ‘a book is near me’."},
            {"wrong": "मैं घर पढ़ता हूँ।", "right": "मैं घर में पढ़ता हूँ।",
             "why": "a place needs its postposition. घर takes में inside; in a sentence like ‘I read at home’ in English the preposition comes first, in Hindi it comes after the noun."},
            {"wrong": "पचास रुपये का है? (asking the price of many items)", "right": "पचास रुपये का है? / पचास रुपये की हैं?",
             "why": "का-के-की agrees with the thing being priced, not with the money. One masculine item: का. A feminine or plural item: की."},
        ],
        "task": {
            "title": "One market conversation, both roles",
            "instructions": ("Copy the bargaining dialogue out by hand, then act both sides aloud. Change three things: "
                             "the item, the first price, and the final price. Keep the phrases पैक कर दीजिए, कितने का है "
                             "and थोड़ा कम कर दीजिए exactly as they are — those three carry most of the bargaining, and "
                             "the numbers are the easy part."),
        },
    },

    # ── B1 ──────────────────────────────────────────────────────────────────
    "B1": {
        "culture": {
            "text": ("देवनागरी Devanagari is a syllabic script written left to right under a continuous headline, the "
                     "शिरोरेखा śirorekhā. Each consonant already contains the vowel अ a, so क is ‘ka’, not a bare ‘k’; the "
                     "other vowels hang off it as matras — कि ki, की kī, कु ku, के ke, को ko. That is why a Hindi word typed "
                     "in Roman letters loses information English cannot give back, and why the alphabet repays a week of "
                     "drilling more than any vocabulary list does."),
            "source_url": "https://en.wikipedia.org/wiki/Devanagari",
        },
        "reading": {
            "text": ("मेरा नाम मीरा है और मैं दिल्ली में रहती हूँ। पिछले साल मैंने हिन्दी सीखनी शुरू की, क्योंकि "
                     "मेरे दफ़्तर में ज़्यादातर लोग हिन्दी बोलते हैं। शुरू में मुझे लगता था कि हिन्दी मुश्किल है, "
                     "लेकिन असल में दिक्कत सिर्फ़ लिपि की थी। जब मैंने देवनागरी पढ़ना सीख लिया, तो सब आसान हो गया। "
                     "अब मैं बैठकों में समझ लेती हूँ, हालाँकि बोलने में अभी झिझक होती है। मेरे साथी कहते हैं कि "
                     "छह महीने में बहुत फ़र्क़ है, और मुझे भी ऐसा लगता है।"),
            "gloss": ("My name is Meera and I live in Delhi. Last year I started learning Hindi, because most people in "
                      "my office speak Hindi. At first I thought Hindi was difficult, but in fact the problem was only "
                      "the script. When I learned to read Devanagari, everything became easier. Now I follow meetings, "
                      "although I still hesitate when speaking. My colleagues say there is a big difference in six "
                      "months, and I think so too."),
            "original": True,
        },
        "listening": {
            "script": ("मैं रोज़ सुबह सात बजे उठता हूँ। पहले चाय पीता हूँ, फिर आधा घंटा पढ़ता हूँ। "
                       "मेरा मानना है कि भाषा वही सीखता है जो रोज़ थोड़ा-थोड़ा करता रहे। "
                       "इसलिए मैंने एक छोटी कॉपी बनाई है — जो नया शब्द मिलता है, उसे लिख लेता हूँ। "
                       "हफ़्ते में एक बार वे सारे शब्द दोहराता हूँ।"),
            "gloss": ("I get up at seven every morning. First I drink tea, then I study for half an hour. My belief is "
                      "that whoever keeps doing a little every day is the one who learns a language. So I have made a "
                      "small notebook — whichever new word I meet, I write it down. Once a week I revise all of them."),
            "voice_tag": VOICE,
        },
        "idioms": [
            {"t": "अंधे की लाठी", "literal": "the blind man’s stick", "meaning": "the one support somebody has, and cannot lose"},
            {"t": "दाल में कुछ काला है", "literal": "there is something black in the lentils", "meaning": "something is fishy — the plan smells wrong"},
            {"t": "मुँह में पानी आना", "literal": "water comes to the mouth", "meaning": "to salivate — used for food, money and anything tempting"},
            {"t": "आँखों का तारा", "literal": "the star of the eyes", "meaning": "the apple of somebody’s eye"},
            {"t": "नौ दो ग्यारह होना", "literal": "to become nine, two, eleven", "meaning": "to vanish fast — to run for your life"},
            {"t": "आग बबूला होना", "literal": "to become fire and bubbles", "meaning": "to be furious — the cartoon kind of angry"},
            {"t": "हाथ मलना", "literal": "to rub the hands", "meaning": "to regret — the gesture matters more than the words"},
            {"t": "पानी-पानी होना", "literal": "to become water, water", "meaning": "to be deeply ashamed, to shrink into yourself"},
            {"t": "चार चाँद लगाना", "literal": "to add four moons", "meaning": "to make something four times finer — said of a good addition"},
            {"t": "घोड़े बेचकर सोना", "literal": "to sell the horse and sleep", "meaning": "to sleep completely untroubled, with nothing left to lose"},
        ],
        "mistakes": [
            {"wrong": "मैंने कल बाज़ार गया।", "right": "मैं कल बाज़ार गया।",
             "why": "the ergative ने appears with a perfective transitive verb, but जाना ‘to go’ is intransitive — no ने."},
            {"wrong": "मैं हिन्दी सीखता रहता हूँ (for ‘I keep learning for a while’).", "right": "मैं हिन्दी सीखता रहता हूँ (habit) · मैं हिन्दी सीख रहा हूँ (right now).",
             "why": "two forms look like the same thing and are not: रहा है is happening now, रहता है is what you do as a rule."},
            {"wrong": "मैं इसे पसंद करता हूँ।", "right": "मुझे यह पसंद है।",
             "why": "‘liking’ puts the person in the को form, not the nominative: the Hindi sentence says ‘to me, this is pleasing’."},
            {"wrong": "आप कल आईए।", "right": "आप कल आइए। / आप कल आइएगा।",
             "why": "the respectful imperative आइए is a fixed form; adding the future ending आइएगा is a common but different, regionally marked shape. Write आइए."},
        ],
        "task": {
            "title": "A page of your own Hindi, six weeks apart",
            "instructions": ("Write one page in Devanagari about why you are learning Hindi. Do not look anything up "
                             "while you write; mark the words you had to think about with a pencil dot. Keep the page. "
                             "In six weeks write the same page again without looking at the first one. The dot count "
                             "is your real progress report — not the number of lessons finished."),
        },
    },

    # ── B2 ──────────────────────────────────────────────────────────────────
    "B2": {
        "culture": {
            "text": ("हिन्दुस्तानी Hindustani is the ordinary spoken language of north India, and हिन्दी and उर्दू are its "
                     "two standards — same grammar, same everyday words, different script and different loan layers. A "
                     "shop conversation, a courtroom argument and a cricket commentary all run in the middle; what changes "
                     "is how far a speaker pulls the same sentence towards Sanskrit on one side (धन्यवाद, सूचना, आवश्यकता) "
                     "or Persian and Arabic on the other (शुक्रिया, ख़बर, ज़रूरत). A learner who can hear that pull is no "
                     "longer translating."),
            "source_url": "https://en.wikipedia.org/wiki/Hindustani_language",
        },
        "reading": {
            "text": ("शहर में एक पुरानी लाइब्रेरी है जो अब बंद होने वाली है। कारण वही है जो हर जगह है: जगह की कीमत। "
                     "कुछ लोग कहते हैं कि ऐसी जगहें शहर की याददाश्त होती हैं और उन्हें बचाना चाहिए। दूसरों का "
                     "ख़याल है कि भावना से किराया नहीं भरता। दोनों बातें सही हैं, और शायद इसीलिए फ़ैसला इतना "
                     "कठिन है। बैठक में जो प्रस्ताव आया, उसमें हॉल को पहली मंज़िल पर छोटा करके बाक़ी जगह किराए "
                     "पर देने की बात थी। किसी को भी सब कुछ मिलने वाला नहीं है।"),
            "gloss": ("There is an old library in the city that is now about to close. The reason is the one that is "
                      "everywhere: the price of space. Some people say such places are a city’s memory and should be "
                      "saved. Others think rent cannot be paid with sentiment. Both are true, and perhaps that is why "
                      "the decision is so hard. The proposal that came to the meeting was to shrink the hall onto the "
                      "first floor and rent out the rest. Nobody is going to get everything."),
            "original": True,
        },
        "listening": {
            "script": ("— सुनिए, बैठक कल दस बजे है या ग्यारह बजे?\n"
                       "— दस बजे तय हुई थी, लेकिन अध्यक्ष साढ़े दस ही पहुँच पाएँगे।\n"
                       "— तो फिर हमें दस बजे पहुँचने का कोई फ़ायदा नहीं।\n"
                       "— फ़ायदा है। जो लोग दस बजे आएँगे, वे पहले आपस में बात कर लेंगे। बहुत बार फ़ैसला "
                       "बैठक से पहले ही हो जाता है।\n"
                       "— यह तो आपने ठीक कहा। मैं सवा दस बजे पहुँच जाऊँगा।"),
            "gloss": ("— Listen, is the meeting tomorrow at ten or at eleven?\n— It was fixed for ten, but the chairman "
                      "can only arrive at half past ten.\n— Then there is no point in us reaching at ten.\n— There is a "
                      "point. The people who come at ten will talk among themselves first. Very often the decision is "
                      "already made before the meeting.\n— That is well said. I will arrive at quarter past ten."),
            "voice_tag": VOICE,
        },
        "idioms": [
            {"t": "बंदर क्या जाने अदरक का स्वाद", "literal": "what does a monkey know of the taste of ginger", "meaning": "someone incapable of appreciating the thing cannot judge it"},
            {"t": "नाच न जाने, आँगन टेढ़ा", "literal": "doesn’t know how to dance, and the courtyard is crooked", "meaning": "blaming the tools for your own failure"},
            {"t": "खोदा पहाड़, निकली चुहिया", "literal": "dug a mountain, out came a mouse", "meaning": "enormous effort, tiny result"},
            {"t": "एक और एक ग्यारह", "literal": "one and one makes eleven", "meaning": "together you are worth far more than your parts — unity is strength"},
            {"t": "जैसी करनी, वैसी भरनी", "literal": "as the doing, so the filling", "meaning": "you reap what you sow"},
            {"t": "घर का भेदी लंका ढाए", "literal": "the one who knows the house’s secrets destroys Lanka", "meaning": "the insider does the real damage"},
            {"t": "ऊँट के मुँह में ज़ीरा", "literal": "cumin in a camel’s mouth", "meaning": "far too little for the appetite — a token where a meal was needed"},
            {"t": "सिर पर कफ़न बाँधना", "literal": "to tie a shroud on the head", "meaning": "to set out ready to die — reckless commitment"},
            {"t": "हाथी के दाँत खाने के और, दिखाने के और", "literal": "the elephant’s teeth are for eating and for showing", "meaning": "one rule in private, another in public"},
            {"t": "आम के आम, गुठलियों के दाम", "literal": "mangoes at the mango price, and the stones’ price too", "meaning": "to profit twice over on one deal"},
        ],
        "mistakes": [
            {"wrong": "मुझे यह किताब पसंद करती है।", "right": "मुझे यह किताब पसंद है।",
             "why": "पसंद is a noun here, not a verb: the sentence is ‘to me this book is pleasing’, so no करती है and no agreement to chase."},
            {"wrong": "वह अध्यक्ष से मिलने गया। (meaning: the chairman went to meet him)", "right": "वह अध्यक्ष से मिलने गया। (he went to meet the chairman) · अध्यक्ष उससे मिलने गया। (the chairman went to meet him)",
             "why": "Hindi word order carries the roles. Move the ने/से phrase and the meaning moves with it — English can shuffle, Hindi mostly cannot."},
            {"wrong": "यह बहुत ज़्यादा महँगा है, थोड़ा सस्ता कीजिए।", "right": "यह बहुत महँगा है, थोड़ा कम कीजिए।",
             "why": "ज़्यादा plus महँगा doubles the intensity the wrong way, and सस्ता कीजिए asks the seller to make it cheap rather than to lower the price."},
            {"wrong": "मैंने उसे फ़ोन किया था, लेकिन उसने नहीं उठाया। (as a present-tense failure)", "right": "मैंने उसे फ़ोन किया, लेकिन उसने नहीं उठाया।",
             "why": "थी puts the attempt in a finished past that has nothing to do with now; a bare perfective is what a native speaker says about today."},
        ],
        "task": {
            "title": "The same sentence, pulled three ways",
            "instructions": ("Take one plain thought — for example ‘I need information about this’ — and write it three "
                             "times: the everyday way, the Sanskrit-side way, and the Persian side. (ज़रूरत/आवश्यकता, "
                             "ख़बर/सूचना are the pairs to start from.) Then read all three aloud and notice which one you "
                             "would use to a friend, to a clerk, and in a letter. That gap is what B2 is made of."),
        },
    },

    # ── C1 ──────────────────────────────────────────────────────────────────
    "C1": {
        "culture": {
            "text": ("हिन्दी सिनेमा has been the most influential register laboratory in the language since the talkies. "
                     "Dialogue writers work a middle register that has to be understood in every state at once, which is "
                     "why film Hindi avoids the deepest Sanskrit and the most Persian vocabulary and leans on "
                     "Hindi–Urdu–English code-mixing instead. Songs, by contrast, keep an older poetic grammar (मैंने "
                     "vs मैं, के बिना vs बग़ैर) that survives nowhere else in daily speech — which makes film dialogue a "
                     "genuine listening syllabus for a C1 learner, and film songs a grammar of their own."),
            "source_url": "https://en.wikipedia.org/wiki/Bollywood",
        },
        "reading": {
            "text": ("भाषा पर बात करते समय हम अक्सर उसकी शुद्धता पर उतर आते हैं, जबकि असली सवाल यह है कि भाषा "
                     "किस काम आती है। जो लेखक यह समझ लेता है, वह अपनी शब्दावली को दर्शक के हिसाब से ढालना सीख "
                     "जाता है। किसी सरकारी पत्र में ‘ज़रूरत’ लिखना कमज़ोरी नहीं, बल्कि अनुचित है; वहाँ ‘आवश्यकता’ "
                     "चाहिए। इसी तरह दोस्त के साथ ‘शुक्रिया’ ठीक लगता है, और मंच पर ‘धन्यवाद’। जो लेखक यह फ़र्क़ "
                     "नहीं कर पाता, उसकी बात सही होने पर भी अटपटी लगती है।"),
            "gloss": ("When we talk about language we usually end up on purity, whereas the real question is what the "
                      "language is useful for. A writer who understands this learns to shape vocabulary to the audience. "
                      "Writing ‘zarurat’ in an official letter is not weakness, it is simply inappropriate; there "
                      "‘āvashyaktā’ is needed. In the same way ‘shukriyā’ sits right with a friend, and ‘dhanyavād’ from "
                      "a stage. A writer who cannot tell the difference sounds awkward even when what they say is true."),
            "original": True,
        },
        "listening": {
            "script": ("इस शहर में दो तरह के लोग रहते हैं — वे जो कहते हैं कि पुरानी चीज़ें बचानी चाहिए, और वे जो "
                       "कहते हैं कि पुरानी चीज़ों से किराया नहीं भरता। दरअसल दोनों एक ही चीज़ की ओर इशारा कर "
                       "रहे हैं: वे कह रहे हैं कि हमें तय करना है कि हम कौन हैं। और यह फ़ैसला कोई भी नगरपालिका "
                       "नहीं कर सकती — यह फ़ैसला उन लोगों को करना है जो उस शहर में सुबह उठते हैं।"),
            "gloss": ("Two kinds of people live in this city — those who say old things must be saved, and those who say "
                      "rent cannot be paid with old things. In fact both are pointing at the same thing: they are saying "
                      "we have to decide who we are. And no municipality can make that decision — it has to be made by "
                      "the people who wake up in that city."),
            "voice_tag": VOICE,
        },
        "idioms": [
            {"t": "दामन में दाग़ लगना", "literal": "a stain on the hem", "meaning": "a blot on one’s honour that cannot be washed out"},
            {"t": "आँख का काजल बनना", "literal": "to become the kohl of the eye", "meaning": "to become the most precious thing somebody has"},
            {"t": "जान पर खेलना", "literal": "to play with one’s life", "meaning": "to risk everything on one throw"},
            {"t": "दिल में गाँठ पड़ना", "literal": "a knot forms in the heart", "meaning": "a misunderstanding that sets hard and colours everything after it"},
            {"t": "मुँह पर ताला लगना", "literal": "a lock on the mouth", "meaning": "to be unable to speak up, though you have plenty to say"},
            {"t": "हवा से बातें करना", "literal": "to talk with the wind", "meaning": "to build castles in the air — or, of a person, to be long gone"},
            {"t": "लोहे के चने चबाना", "literal": "to chew iron gram", "meaning": "to attempt something nobody manages easily"},
            {"t": "खरी-खरी सुनाना", "literal": "to make someone hear the salty ones", "meaning": "to tell somebody the blunt truth to their face"},
            {"t": "छक्के छुड़ाना", "literal": "to knock the sixes off somebody", "meaning": "to thrash someone — from cricket, now general"},
            {"t": "आँखें चार होना", "literal": "for the eyes to become four", "meaning": "for two people’s eyes to meet, usually unsought"},
        ],
        "mistakes": [
            {"wrong": "इस विषय पर मैं अपनी राय देता हूँ।", "right": "इस विषय पर मैं अपनी राय रखता हूँ।",
             "why": "राय takes रखना, not देना, and सलाह takes देना. Mixing them is the classic C1 slip: both are ‘advice’ in a dictionary."},
            {"wrong": "उसने मुझसे कहा कि वह कल आएगा (reported speech with wrong agreement).", "right": "उसने मुझसे कहा कि वह कल आएगा। (man) · उसने मुझसे कहा कि वह कल आएगी। (woman)",
             "why": "Hindi keeps the tense of reported speech unchanged, but the gender of वह has to follow the speaker — and वह never becomes ‘he’ or ‘she’ for you."},
            {"wrong": "यह एक बहुत ही महत्त्वपूर्ण विषय है जो बहुत ज़रूरी है।", "right": "यह एक महत्त्वपूर्ण विषय है।",
             "why": "stacking a Sanskrit adjective, a Hindi adjective and a boom of intensifiers is the commonest inflated style; C1 is judged on trimming, not on piling up."},
            {"wrong": "बग़ैर समय के कोई काम नहीं होता।", "right": "बग़ैर समय के कोई काम नहीं होता। / समय के बिना कोई काम नहीं होता।",
             "why": "बग़ैर stands before its noun (बग़ैर समय), बिना after it (समय के बिना). Both are correct; using बिना before the noun is the error."},
        ],
        "task": {
            "title": "Rewrite one paragraph at three registers",
            "instructions": ("Take the reading passage on this page and rewrite its first three sentences for three "
                             "audiences: a friend on WhatsApp, a newspaper column, and an official notice. Keep the "
                             "meaning identical — only the vocabulary and the sentence length may move. Then give the "
                             "three versions to someone who reads Hindi well and ask which sentence sounds like a "
                             "translation. That judgement is the skill."),
        },
    },

    # ── C2 ──────────────────────────────────────────────────────────────────
    "C2": {
        "culture": {
            "text": ("हिन्दी की शब्दावली तीन परतों में बनी है। सबसे नीचे तद्भव शब्द हैं — जो संस्कृत से बदलते-बदलते "
                     "आए: दूध, आँख, हाथ। उनके ऊपर तत्सम हैं, जो संस्कृत से ज्यों-के-त्यों आए और ज़्यादातर औपचारिक "
                     "लिखने में रहते हैं: दुग्ध, नेत्र, हस्त। सबसे ऊपर फ़ारसी, अरबी और अँग्रेज़ी की परत है: क़लम, "
                     "किताब, टिकट। किसी भी वाक्य की शैली यहीं तय होती है — कौन-सी परत किसके साथ बैठती है, और "
                     "कौन-सी परत एक-दूसरे को काट देती है।"),
            "gloss": ("Hindi’s vocabulary is built in three layers. At the bottom are tadbhava words, which drifted from "
                      "Sanskrit over centuries: dūdh (milk), āṅkh (eye), hāth (hand). Above them sit tatsama words, taken "
                      "from Sanskrit unchanged and mostly kept for formal writing: dugdh, netra, hast. On top is the "
                      "Persian, Arabic and English layer: qalam, kitāb, ṭikaṭ. The style of any sentence is decided right "
                      "here — which layer sits with which, and which layer cuts against another."),
            "source_url": "https://en.wikipedia.org/wiki/Hindi",
        },
        "reading": {
            "text": ("अनुवाद में सबसे बड़ी चूक शब्दों की नहीं, इरादे की होती है। एक ही वाक्य अँग्रेज़ी में विनम्र "
                     "लगता है और हिन्दी में रूखा, क्योंकि हिन्दी विनम्रता क्रिया के रूप में दिखाती है, शब्दों में "
                     "नहीं। जो अनुवादक यह समझ लेता है, वह ‘कृपया’ जोड़कर विनम्रता नहीं लाता; वह क्रिया बदल देता है। "
                     "इसीलिए अच्छा अनुवाद मूल से मिलता-जुलता नहीं, बल्कि मूल जैसा व्यवहार करता है — पाठक को वही "
                     "जगह देता है जो मूल पाठक को मिली थी।"),
            "gloss": ("The biggest failure in translation is not of words but of intent. The same sentence sounds polite "
                      "in English and blunt in Hindi, because Hindi shows politeness in the verb form, not in the words. "
                      "A translator who understands this does not bring politeness by adding ‘kripayā’; they change the "
                      "verb. That is why a good translation does not resemble the original, it behaves like it — it gives "
                      "the reader the same room the original reader had."),
            "original": True,
        },
        "listening": {
            "script": ("मैं मानता हूँ कि भाषा कभी शुद्ध नहीं होती, और जो इसे शुद्ध करने चलते हैं वे उसे मार डालते हैं। "
                       "पर इसका उल्टा भी उतना ही ग़लत है — यह कहना कि सब कुछ चलेगा। फ़र्क़ यह है कि भाषा नियम से "
                       "नहीं, आदत से चलती है; और आदत उसी को बदलती है जो उसे समझता है। इसलिए सवाल ‘सही क्या है’ "
                       "नहीं, ‘कौन समझेगा’ है।"),
            "gloss": ("I hold that a language is never pure, and that those who set out to purify it kill it. But the "
                      "opposite is just as wrong — saying that anything goes. The difference is that a language runs on "
                      "habit, not on rules; and habit changes only for someone who understands it. So the question is "
                      "not ‘what is correct’ but ‘who will understand’."),
            "voice_tag": VOICE,
        },
        "idioms": [
            {"t": "मुँह में राम, बगल में छुरी", "literal": "Ram on the tongue, a knife under the arm", "meaning": "sweet to your face, ready to cut you from the side"},
            {"t": "आँखों में धूल झोंकना", "literal": "to blow dust into somebody’s eyes", "meaning": "to deceive someone while they watch"},
            {"t": "हाथ-पाँव फूल जाना", "literal": "hands and feet to swell up", "meaning": "to be paralysed by fear — the body stops cooperating"},
            {"t": "नाक में दम करना", "literal": "to put your life into somebody’s nose", "meaning": "to plague a person until they cannot bear it"},
            {"t": "दाँत खट्टे करना", "literal": "to make somebody’s teeth sour", "meaning": "to defeat an opponent thoroughly"},
            {"t": "तलवार की धार पर चलना", "literal": "to walk on the edge of a sword", "meaning": "to tread a line where one slip ends everything"},
            {"t": "जुग-जुग जियो", "literal": "live age upon age", "meaning": "a blessing: may you live long — said to a child, or to anyone who has done you a kindness"},
            {"t": "दूध का दूध, पानी का पानी", "literal": "milk to the milk, water to the water", "meaning": "a verdict that separates the two sides exactly — used of a fair judge"},
            {"t": "सोने पे सुहागा", "literal": "borax on gold", "meaning": "a bonus on top of something already good"},
            {"t": "कान भरना", "literal": "to fill somebody’s ear", "meaning": "to poison a person’s mind against another by quiet talk"},
        ],
        "mistakes": [
            {"wrong": "वह मेरा मित्र है, वह बहुत अच्छा आदमी है, वह हमेशा मदद करता है।", "right": "वह मेरा मित्र है और हमेशा मदद करता है।",
             "why": "at C2 the failure is almost never grammar; it is a chain of clauses with no subordination. Hindi joins with और, लेकिन, जो and participles, not by stacking full sentences."},
            {"wrong": "यह पुस्तक मेरे द्वारा पढ़ी गई। (in ordinary speech)", "right": "यह किताब मैंने पढ़ी।",
             "why": "the Sanskrit passive द्वारा-construction exists but reads like a government circular. Choosing it in conversation is a register error, not a grammar error."},
            {"wrong": "मुझे हिन्दी बोलनी आती है। (meaning: I know how to speak Hindi — agreement on बोलनी)", "right": "मुझे हिन्दी बोलना आता है।",
             "why": "with आना as ‘to know how’, the verbal noun stays masculine singular whatever the object’s gender. Very common even among fluent speakers, so the error survives for years."},
            {"wrong": "वे लोग जो आए थे, उनका स्वागत किया गया और उन्होंने अपने विचार रखे और फिर चले गए।", "right": "जो लोग आए थे, उन्होंने अपने विचार रखे और चले गए।",
             "why": "over-correcting into formal vocabulary while leaving the sentence unstructured produces the para that reads like a form. Sentence architecture is the last thing to fix and the first thing a reader notices."},
        ],
        "task": {
            "title": "One idea, three layers, one honest note",
            "instructions": ("Choose one everyday idea — for example ‘the bus was late again’. Write it three times, once "
                             "with only तद्भव vocabulary, once with तत्सम vocabulary, once with the Persian–English layer. "
                             "Then write a short note underneath saying which version you would actually use, to whom, and "
                             "why. Do not translate between the three: write each one straight. That is the exercise — the "
                             "layers are registers, and registers are chosen, not translated."),
        },
    },
}


def main() -> int:
    check = "--check" in sys.argv
    changed = 0
    for rung, extra in sorted(HI_EXTRA.items()):
        path = ROOT / f"data/courses/phase-2/hi_{rung}.json"
        if not path.exists():
            raise SystemExit(f"missing course file: {path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        level = data.setdefault("level", {})
        if level.get("extra") == extra:
            print(f"  hi {rung:3s} extra already current")
            continue
        if check:
            print(f"  hi {rung:3s} extra STALE")
            changed += 1
            continue
        level["extra"] = extra
        # match the authored files' own formatting (indent 2, no trailing newline)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        idioms = len(extra["idioms"])
        print(f"  hi {rung:3s} extra written — {idioms} idioms, {len(extra['mistakes'])} mistakes, "
              f"reading {len(extra['reading']['text'])} chars, source {extra['culture']['source_url'].split('//')[-1]}")
        changed += 1
    print(f"{'STALE' if check else 'written'}: {changed} rung(s)")
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    raise SystemExit(main())

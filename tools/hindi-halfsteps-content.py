# -*- coding: utf-8 -*-
"""Authored content for the Hindi half-step rungs, as data.

`tools/author-hindi-halfsteps.py` holds the machinery (lesson building, practice
and quiz generation, file writing); this file holds the writing. Splitting them
keeps the Hindi text editable without touching code, and keeps the tool small
enough to read in one go.

Each level here is:

    {
      "title":  the half-step's name from data/levels.json,
      "goals":  three outcomes,
      "units":  [ {id, title, lessons: [lesson spec, ...]}, x3 ],
      "extra":  the schema's required extra block (culture, reading, listening,
                idioms, mistakes, task),
      "test":   [(type, question, answer), ...] — 10 to 20 items,
    }

A lesson spec is {title, learn, vocab, grammar, dialogue, worksheet}; the tool
turns it into a full lesson (practice ×12, quiz ×5, worksheet with the
integrated task appended).

The rungs follow data/levels.json: A2+ "Holding a chat" (keep a conversation
going, tell a short story), B1+ "Comfortable" (work in the language, argue a
point politely).
"""
from __future__ import annotations


def V(t, r, en, pos="phrase"):
    return {"t": t, "r": r, "en": en, "pos": pos}


def X(t, r, en):
    return {"t": t, "r": r, "en": en}


def unit(uid, title, lessons):
    return {"id": uid, "title": title, "lessons": lessons}


VOICE = "hi-IN"

# ════════════════════════════════════════════════════════════════════════════
# A2+ · Holding a chat  —  keep a conversation going, tell a short story
# ════════════════════════════════════════════════════════════════════════════
A2P_UNITS = [
    unit("A2P-U1", "Keeping a chat alive", [
        {
            "title": "Continuers and reactions",
            "learn": ("A conversation is held up by small words, not sentences: अच्छा (I see), सच? "
                      "(really?), वाक़ई? (truly?), ओह (oh), हाँ जी (yes — I am listening), तो? (and "
                      "then?). A learner who says only full sentences sounds like a textbook; the "
                      "reactions are what make the other person keep talking."),
            "vocab": [V("अच्छा", "achchhā", "I see / really?"), V("सच", "sac", "really?"),
                      V("वाक़ई", "vāqai", "truly?"), V("ओह", "oh", "oh"),
                      V("हाँ जी", "hāṅ jī", "yes — I am listening"), V("तो", "to", "and then?"),
                      V("समझ गया", "samajh gayā", "I have understood"),
                      V("मतलब", "matlab", "meaning / so what you mean is")],
            "grammar": {
                "title": "Reactions take no grammar",
                "explain": ("अच्छा, सच, वाक़ई and ओह stand alone — nothing agrees, nothing is added. "
                            "The length carries the meaning: a short अच्छा is 'noted', a long "
                            "आ-अ-अच्छा is surprise. समझ गया/समझ गई ('understood') is the other "
                            "one-word reaction that ends a set of instructions politely."),
                "pattern": "अच्छा · सच? · वाक़ई? · तो? · समझ गया/गई",
                "examples": [X("अच्छा, फिर क्या हुआ?", "achchhā, phir kyā huā?", "I see — then what happened?"),
                             X("सच? मुझे नहीं पता था।", "sac? mujhe nahīṅ patā thā.", "Really? I did not know."),
                             X("समझ गई, धन्यवाद।", "samajh gaī, dhanyavād.", "Understood, thank you.")],
                "mistakes": [{"wrong": "अच्छा हूँ। (as a reaction)",
                              "right": "अच्छा।",
                              "why": "अच्छा as a reaction is a whole turn on its own. Adding हूँ turns it into 'I am good', which answers a different question — आप कैसे हैं?"}],
            },
            "dialogue": [
                {"sp": "राहुल", "t": "कल मैं आगरा गया था।", "r": "kal main Āgrā gayā thā.", "en": "I went to Agra yesterday."},
                {"sp": "मीरा", "t": "अच्छा! वाक़ई? कैसा लगा?", "r": "achchhā! vāqai? kaisā lagā?", "en": "I see! Truly? How did you like it?"},
                {"sp": "राहुल", "t": "बहुत अच्छा लगा — ताज महल देखा।", "r": "bahut achchhā lagā — Tāj Mahal dekhā.", "en": "I liked it very much — I saw the Taj Mahal."},
                {"sp": "मीरा", "t": "सच? मैं वहाँ कभी नहीं गई।", "r": "sac? main vahāṅ kabhī nahīṅ gaī.", "en": "Really? I have never been there."},
            ],
            "worksheet": {"title": "Reactions worksheet", "tasks": [
                {"instruction": "React in Hindi.", "items": ["really?", "I see — and then?", "understood"], "key": ["सच?", "अच्छा, तो?", "समझ गया"]},
                {"instruction": "Fix the reaction.", "items": ["अच्छा हूँ।", "सच है? (as a reaction)"], "key": ["अच्छा।", "सच?"]},
            ]},
        },
        {
            "title": "Follow-up questions: फिर क्या हुआ?",
            "learn": ("Follow-ups keep the other person talking and they reuse the tense of the "
                      "answer: फिर क्या हुआ? (then what happened), क्यों? (why), कैसे? (how), और "
                      "कब? (and when). ज़रा और बताइए (tell me a little more) is the polite way to "
                      "ask for more, and it works with anyone."),
            "vocab": [V("फिर क्या हुआ", "phir kyā huā", "then what happened?"),
                      V("क्यों", "kyoṅ", "why?"), V("कैसे", "kaise", "how?"),
                      V("और कब", "aur kab", "and when?"), V("ज़रा और बताइए", "zarā aur batāie", "tell me a little more"),
                      V("आगे", "āge", "further / on"), V("पूरी बात", "pūrī bāt", "the whole story"),
                      V("दिलचस्प", "dilcasp", "interesting")],
            "grammar": {
                "title": "Follow-ups copy the tense",
                "explain": ("If the answer is in the past, फिर क्या हुआ stays in the past. If the "
                            "person is describing a habit, the follow-up is कैसे करते हैं? — same "
                            "habitual form. This is why a follow-up never sounds like a new topic: it "
                            "is the same sentence with the piece you want missing."),
                "pattern": "past answer → फिर क्या हुआ? · habit → कैसे करते हैं? · ज़रा और बताइए",
                "examples": [X("फिर क्या हुआ?", "phir kyā huā?", "Then what happened?"),
                             X("आप यह कैसे करते हैं?", "āp yah kaise karte haiṅ?", "How do you do this?"),
                             X("ज़रा और बताइए — पूरी बात सुनाइए।", "zarā aur batāie — pūrī bāt sunāie.", "Tell me more — tell me the whole story.")],
                "mistakes": [{"wrong": "फिर क्या होगा? (after a story that has already ended)",
                              "right": "फिर क्या हुआ?",
                              "why": "होगा looks forward; हुआ looks back. After a finished story the follow-up has to be in the past, or the speaker is asked about a future that does not exist."}],
            },
            "dialogue": [
                {"sp": "मीरा", "t": "मैंने नई नौकरी शुरू की।", "r": "mainne naī naukrī śurū kī.", "en": "I started a new job."},
                {"sp": "राहुल", "t": "अच्छा! फिर क्या हुआ?", "r": "achchhā! phir kyā huā?", "en": "Nice! Then what happened?"},
                {"sp": "मीरा", "t": "पहले डर लगा, फिर सब ठीक हो गया।", "r": "pahle ḍar lagā, phir sab ṭhīk ho gayā.", "en": "At first I was scared, then everything turned out fine."},
                {"sp": "राहुल", "t": "ज़रा और बताइए — काम कैसा है?", "r": "zarā aur batāie — kām kaisā hai?", "en": "Tell me more — how is the work?"},
            ],
            "worksheet": {"title": "Follow-up worksheet", "tasks": [
                {"instruction": "Ask a follow-up.", "items": ["then what happened?", "how do you do it?", "and when?"], "key": ["फिर क्या हुआ?", "आप यह कैसे करते हैं?", "और कब?"]},
                {"instruction": "Ask for more, politely.", "items": ["tell me the whole story"], "key": ["ज़रा और बताइए — पूरी बात सुनाइए।"]},
            ]},
        },
        {
            "title": "Likes of other people: आपको क्या पसंद है?",
            "learn": ("To keep a chat going you need the other person's likes, and Hindi puts the "
                      "person in the को-form: आपको क्या पसंद है? (what do you like?), मुझे संगीत "
                      "पसंद है. Ask about शौक़ (hobbies), फ़िल्में, खाना, यात्रा — and answer with "
                      "मुझे … पसंद है or मुझे … पसंद नहीं है."),
            "vocab": [V("शौक़", "śauq", "hobby", "noun"), V("संगीत", "saṅgīt", "music", "noun"),
                      V("फ़िल्म", "film", "film", "noun"), V("खाना बनाना", "khānā banānā", "to cook"),
                      V("यात्रा", "yātrā", "travel", "noun"), V("किताबें पढ़ना", "kitābeṅ paṛhnā", "to read books"),
                      V("खेल", "khel", "sport / game", "noun"), V("बिल्कुल नहीं", "bilkul nahīṅ", "not at all")],
            "grammar": {
                "title": "मुझे X पसंद है · आपको क्या पसंद है?",
                "explain": ("Liking puts the person in the को-form and the thing in the plain form: "
                            "मुझे संगीत पसंद है (I like music), आपको क्या पसंद है? To ask about doing "
                            "something, the verb becomes a verbal noun — मुझे खाना बनाना पसंद है (I like "
                            "cooking), and the verbal noun stays masculine singular."),
                "pattern": "मुझे/आपको + thing + पसंद है · मुझे + verb-ना + पसंद है",
                "examples": [X("आपको क्या पसंद है?", "āpko kyā pasand hai?", "What do you like?"),
                             X("मुझे पुरानी फ़िल्में पसंद हैं।", "mujhe purānī filmeṅ pasand haiṅ.", "I like old films."),
                             X("मुझे खाना बनाना पसंद है।", "mujhe khānā banānā pasand hai.", "I like cooking.")],
                "mistakes": [{"wrong": "मैं संगीत पसंद हूँ।",
                              "right": "मुझे संगीत पसंद है।",
                              "why": "the liker takes को; the liked thing is the subject and takes है/हैं. मैं पसंद हूँ makes you the thing being liked."}],
            },
            "dialogue": [
                {"sp": "राहुल", "t": "आपके शौक़ क्या हैं?", "r": "āpke śauq kyā haiṅ?", "en": "What are your hobbies?"},
                {"sp": "मीरा", "t": "मुझे किताबें पढ़ना और यात्रा करना पसंद है।", "r": "mujhe kitābeṅ paṛhnā aur yātrā karnā pasand hai.", "en": "I like reading books and travelling."},
                {"sp": "राहुल", "t": "और संगीत?", "r": "aur saṅgīt?", "en": "And music?"},
                {"sp": "मीरा", "t": "पुराना संगीत बिल्कुल पसंद नहीं — नया सुनती हूँ।", "r": "purānā saṅgīt bilkul pasand nahīṅ — nayā suntī hūṅ.", "en": "I do not like old music at all — I listen to new."},
            ],
            "worksheet": {"title": "Likes worksheet", "tasks": [
                {"instruction": "Ask about likes.", "items": ["What do you like?", "Do you like Hindi films?"], "key": ["आपको क्या पसंद है?", "आपको हिन्दी फ़िल्में पसंद हैं?"]},
                {"instruction": "Answer for yourself.", "items": ["I like music.", "I do not like cooking."], "key": ["मुझे संगीत पसंद है।", "मुझे खाना बनाना पसंद नहीं है।"]},
            ]},
        },
    ]),
    unit("A2P-U2", "Telling a short story", [
        {
            "title": "Sequencing: पहले, फिर, उसके बाद, आख़िर में",
            "learn": ("A story in Hindi is held together by four words: पहले (first), फिर (then), "
                      "उसके बाद (after that), आख़िर में (finally). They sit at the front of the "
                      "clause, and once they are in place the sentences themselves can stay short — "
                      "which is exactly what makes a beginner sound fluent."),
            "vocab": [V("पहले", "pahle", "first"), V("फिर", "phir", "then"),
                      V("उसके बाद", "uske bād", "after that"), V("आख़िर में", "ākhir meṅ", "finally"),
                      V("इसलिए", "islie", "therefore"), V("अचानक", "achānak", "suddenly"),
                      V("कहानी", "kahānī", "story", "noun"), V("शुरू", "śurū", "beginning", "noun")],
            "grammar": {
                "title": "Sequence words lead the clause",
                "explain": ("पहले … फिर … उसके बाद … आख़िर में is the standard frame. अचानक (suddenly) "
                            "is the interruption that makes a story worth listening to, and it also "
                            "leads: अचानक बारिश शुरू हो गई. Nothing else in the sentence changes."),
                "pattern": "पहले … फिर … उसके बाद … आख़िर में …",
                "examples": [X("पहले हम बाज़ार गए, फिर चाय पी।", "pahle ham bāzār gae, phir cāy pī.", "First we went to the market, then we drank tea."),
                             X("उसके बाद अचानक बारिश शुरू हो गई।", "uske bād achānak bāriś śurū ho gaī.", "After that it suddenly started raining."),
                             X("आख़िर में हम घर लौट आए।", "ākhir meṅ ham ghar lauṭ āe.", "Finally we came back home.")],
                "mistakes": [{"wrong": "पहले मैं गया, और फिर मैंने खाया, और फिर मैं सोया।",
                              "right": "पहले मैं गया, फिर खाया, आख़िर में सोया।",
                              "why": "the sequence words already do the joining, so और फिर repeated before every clause is the English 'and then' copied across. One word each is enough."}],
            },
            "dialogue": [
                {"sp": "मीरा", "t": "कल का दिन कैसा था?", "r": "kal kā din kaisā thā?", "en": "How was yesterday?"},
                {"sp": "राहुल", "t": "पहले हम दफ़्तर गए, फिर बाज़ार।", "r": "pahle ham daftar gae, phir bāzār.", "en": "First we went to the office, then the market."},
                {"sp": "मीरा", "t": "उसके बाद?", "r": "uske bād?", "en": "After that?"},
                {"sp": "राहुल", "t": "उसके बाद अचानक बारिश आई — आख़िर में टैक्सी से घर आए।", "r": "uske bād achānak bāriś āī — ākhir meṅ ṭaiksī se ghar āe.", "en": "After that it suddenly rained — finally we came home by taxi."},
            ],
            "worksheet": {"title": "Sequencing worksheet", "tasks": [
                {"instruction": "Put the story in order.", "items": ["फिर हम पहुँचे। / पहले गाड़ी छूटी। / आख़िर में मिल गए।"], "key": ["पहले गाड़ी छूटी। / फिर हम पहुँचे। / आख़िर में मिल गए।"]},
                {"instruction": "Tell it in Hindi.", "items": ["First we ate, then we left."], "key": ["पहले हमने खाया, फिर चले।"]},
            ]},
        },
        {
            "title": "Past continuous: जब… तब… खा रहा था",
            "learn": ("The past continuous था/थी/थे is what holds the background of a story: मैं खाना "
                      "खा रहा था (I was eating). जब sets the scene and तब delivers the event: जब मैं "
                      "सो रहा था, तब फ़ोन आया. था agrees with the person, so सो रही थी, सो रहे थे."),
            "vocab": [V("जब", "jab", "when"), V("तब", "tab", "then (at that moment)"),
                      V("सो रहा था", "so rahā thā", "was sleeping"), V("इंतज़ार कर रहा था", "intzār kar rahā thā", "was waiting"),
                      V("बीच में", "bīc meṅ", "in the middle / meanwhile"), V("तभी", "tabhī", "just then"),
                      V("पहुँचना", "pahuṅcnā", "to arrive"), V("छूट जाना", "chhūṭ jānā", "to get missed")],
            "grammar": {
                "title": "जब … रहा था, तब … आया",
                "explain": ("The continuous past draws the scene; the perfective delivers the event "
                            "that interrupts it. तभी ('just then') does the same job as तब but with the "
                            "timing tightened. था follows the subject's gender and number: मैं सो रहा "
                            "था, वह सो रही थी, हम सो रहे थे."),
                "pattern": "जब + subject + … रहा/रही/रहे था, तब + event (perfective)",
                "examples": [X("जब मैं सो रहा था, तब फ़ोन आया।", "jab main so rahā thā, tab fon āyā.", "While I was sleeping, the phone rang."),
                             X("तभी गाड़ी छूट गई।", "tabhī gāṛī chhūṭ gaī.", "Just then the train got missed."),
                             X("हम इंतज़ार कर रहे थे।", "ham intzār kar rahe the.", "We were waiting.")],
                "mistakes": [{"wrong": "जब मैं सो रहा था, तब फ़ोन आ रहा था।",
                              "right": "जब मैं सो रहा था, तब फ़ोन आया।",
                              "why": "the interruption is a single event, so it takes the perfective. Making both verbs continuous leaves the listener waiting for the thing that actually happened."}],
            },
            "dialogue": [
                {"sp": "राहुल", "t": "कल तुम कहाँ थे?", "r": "kal tum kahāṅ the?", "en": "Where were you yesterday?"},
                {"sp": "मीरा", "t": "मैं घर पर इंतज़ार कर रही थी।", "r": "main ghar par intzār kar rahī thī.", "en": "I was waiting at home."},
                {"sp": "राहुल", "t": "जब मैं पहुँचा, तब तुम सो रही थीं?", "r": "jab main pahuṅcā, tab tum so rahī thīṅ?", "en": "When I arrived, were you sleeping?"},
                {"sp": "मीरा", "t": "नहीं, तभी फ़ोन आया और मैं उठ गई।", "r": "nahīṅ, tabhī fon āyā aur main uṭh gaī.", "en": "No — just then the phone rang and I got up."},
            ],
            "worksheet": {"title": "Past continuous worksheet", "tasks": [
                {"instruction": "Build the scene and the event.", "items": ["While I was eating, the light went off.", "We were waiting, just then the bus came."], "key": ["जब मैं खा रहा था, तब बिजली चली गई।", "हम इंतज़ार कर रहे थे, तभी बस आई।"]},
                {"instruction": "Fix the tense.", "items": ["जब मैं पढ़ रहा था, तब वह आ रहा था।"], "key": ["जब मैं पढ़ रहा था, तब वह आया।"]},
            ]},
        },
        {
            "title": "Ending a story: क्या मज़ा आया!",
            "learn": ("A Hindi story ends with a reaction, not a summary: क्या मज़ा आया! (what fun it "
                      "was!), डर लगा (I was scared), हँसी आ गई (I burst out laughing), बहुत बढ़िया "
                      "था (it was great). The क्या …! frame turns any noun into an exclamation, and it "
                      "is the easiest expressive pattern in the language."),
            "vocab": [V("मज़ा", "mazā", "fun / enjoyment", "noun"), V("डर", "ḍar", "fear", "noun"),
                      V("हँसी", "haṅsī", "laughter", "noun"), V("बढ़िया", "baṛhiyā", "excellent"),
                      V("अफ़सोस", "afsos", "regret / a pity", "noun"), V("किस्मत", "kismat", "luck / fate", "noun"),
                      V("यादगार", "yādgār", "memorable"), V("सब ठीक हो गया", "sab ṭhīk ho gayā", "everything turned out fine")],
            "grammar": {
                "title": "क्या …! · … लगा · हँसी आ गई",
                "explain": ("क्या + noun + ! makes an exclamation: क्या मज़ा आया!, क्या बात है! Feelings "
                            "arrive rather than being had: डर लगा (fear came), हँसी आ गई (laughter "
                            "came), अफ़सोस हुआ (regret happened). The person takes को when named — "
                            "मुझे डर लगा."),
                "pattern": "क्या + noun + ! · मुझे + डर/हँसी/अफ़सोस + लगा/आया/हुआ",
                "examples": [X("क्या मज़ा आया!", "kyā mazā āyā!", "What fun it was!"),
                             X("मुझे डर लगा, पर सब ठीक हो गया।", "mujhe ḍar lagā, par sab ṭhīk ho gayā.", "I was scared, but everything turned out fine."),
                             X("हँसी आ गई — बहुत यादगार दिन था।", "haṅsī ā gaī — bahut yādgār din thā.", "I burst out laughing — it was a memorable day.")],
                "mistakes": [{"wrong": "मैंने बहुत मज़ा किया।",
                              "right": "मुझे बहुत मज़ा आया। / क्या मज़ा आया!",
                              "why": "मज़ा arrives at you, so it takes आया and the को-form. करना मज़ा is the English 'have fun' translated word for word and it is not what anyone says."}],
            },
            "dialogue": [
                {"sp": "मीरा", "t": "शादी कैसी थी?", "r": "śādī kaisī thī?", "en": "How was the wedding?"},
                {"sp": "राहुल", "t": "क्या मज़ा आया! बहुत यादगार थी।", "r": "kyā mazā āyā! bahut yādgār thī.", "en": "What fun it was! Very memorable."},
                {"sp": "मीरा", "t": "और भीड़?", "r": "aur bhīṛ?", "en": "And the crowd?"},
                {"sp": "राहुल", "t": "बहुत भीड़ थी — एक बार तो डर लगा, पर सब ठीक हो गया।", "r": "bahut bhīṛ thī — ek bār to ḍar lagā, par sab ṭhīk ho gayā.", "en": "Very crowded — at one point I was scared, but everything turned out fine."},
            ],
            "worksheet": {"title": "Story ending worksheet", "tasks": [
                {"instruction": "React in Hindi.", "items": ["what fun!", "what a thing!", "a pity"], "key": ["क्या मज़ा आया!", "क्या बात है!", "अफ़सोस"]},
                {"instruction": "Describe how it felt.", "items": ["I was scared.", "I burst out laughing."], "key": ["मुझे डर लगा।", "हँसी आ गई।"]},
            ]},
        },
    ]),
    unit("A2P-U3", "Inviting and arranging", [
        {
            "title": "Invitations: आइए, चलिए, क्या आप आएँगे?",
            "learn": ("An invitation is a polite imperative or a future question: ज़रा आइए (do come), "
                      "चलिए (let us go), क्या आप आएँगे? (will you come?). For an outing: चलिए, फ़िल्म "
                      "देखने चलें? (shall we go see a film?). Add ज़रूर आइएगा (do come, certainly) to "
                      "make it warm."),
            "vocab": [V("आइए", "āie", "please come"), V("चलिए", "calie", "let us go"),
                      V("आएँगे", "āeṅge", "will you come?"), V("न्योता", "nyotā", "invitation", "noun"),
                      V("मेहमान", "mehmān", "guest", "noun"), V("खाना खाइए", "khānā khāie", "do eat (please)"),
                      V("ज़रूर आइएगा", "zarūr āiega", "do come, certainly"),
                      V("इंतज़ार रहेगा", "intzār rahegā", "we will be waiting")],
            "grammar": {
                "title": "चलिए … चलें? — the joint suggestion",
                "explain": ("चलिए alone means 'come, let us go'; with a purpose it becomes a "
                            "suggestion: चलिए, चाय पीने चलें? The subjunctive चलें invites agreement "
                            "rather than ordering it. The invitation's closing line is ज़रूर आइएगा or "
                            "हमें इंतज़ार रहेगा."),
                "pattern": "ज़रा आइए · चलिए, … चलें? · ज़रूर आइएगा",
                "examples": [X("कल हमारे घर ज़रूर आइए।", "kal hamāre ghar zarūr āie.", "Do come to our home tomorrow."),
                             X("चलिए, फ़िल्म देखने चलें?", "calie, film dekhne caleṅ?", "Shall we go see a film?"),
                             X("हमें आपका इंतज़ार रहेगा।", "hameṅ āpkā intzār rahegā.", "We will be waiting for you.")],
                "mistakes": [{"wrong": "आप कल घर आओ। (inviting an elder or a colleague)",
                              "right": "आप कल घर ज़रूर आइए।",
                              "why": "invitations to anyone you would call आप take -इए; आओ turns the invitation into an instruction."}],
            },
            "dialogue": [
                {"sp": "मीरा", "t": "कल हमारे घर ज़रूर आइए।", "r": "kal hamāre ghar zarūr āie.", "en": "Do come to our home tomorrow."},
                {"sp": "राहुल", "t": "क्या बात है! कितने बजे?", "r": "kyā bāt hai! kitne baje?", "en": "Wonderful! At what time?"},
                {"sp": "मीरा", "t": "शाम छह बजे। और चलिए, रविवार को फ़िल्म देखने चलें?", "r": "śām chah baje. aur calie, ravivār ko film dekhne caleṅ?", "en": "Six in the evening. And shall we go see a film on Sunday?"},
                {"sp": "राहुल", "t": "बहुत अच्छा — हमें इंतज़ार रहेगा।", "r": "bahut achchhā — hameṅ intzār rahegā.", "en": "Lovely — we will be waiting."},
            ],
            "worksheet": {"title": "Invitation worksheet", "tasks": [
                {"instruction": "Invite politely.", "items": ["come to our home", "let us go for tea"], "key": ["हमारे घर आइए", "चलिए, चाय पीने चलें?"]},
                {"instruction": "Close the invitation warmly.", "items": ["do come (certainly)", "we will be waiting"], "key": ["ज़रूर आइएगा", "हमें इंतज़ार रहेगा"]},
            ]},
        },
        {
            "title": "Accepting, declining, changing the time",
            "learn": ("Accepting is short: ज़रूर, बहुत ख़ुशी से (with pleasure), ठीक है, मैं आऊँगा. "
                      "Declining needs a softener and an alternative: माफ़ कीजिए, उस दिन मैं व्यस्त "
                      "हूँ — क्या रविवार ठीक है? The alternative is what makes a refusal friendly; "
                      "declining without it closes the conversation."),
            "vocab": [V("बहुत ख़ुशी से", "bahut khuśī se", "with pleasure"),
                      V("उस दिन", "us din", "that day"), V("अगला रविवार", "aglā ravivār", "next Sunday"),
                      V("समय बदलना", "samay badalnā", "to change the time"),
                      V("क्या … ठीक है?", "kyā … ṭhīk hai?", "is … all right?"),
                      V("देर", "der", "lateness", "noun"), V("जल्दी", "jaldī", "early / hurry"),
                      V("भेज दीजिए", "bhej dījie", "please send it over")],
            "grammar": {
                "title": "Refuse, soften, offer another time",
                "explain": ("The three-part decline: माफ़ कीजिए, [reason], क्या [alternative] ठीक है? "
                            "The reason stays general (व्यस्त हूँ / काम है), the alternative is "
                            "specific (अगला रविवार). क्या … ठीक है? is the standard way to propose a "
                            "change without seeming to cancel."),
                "pattern": "माफ़ कीजिए, … — क्या … ठीक है?",
                "examples": [X("बहुत ख़ुशी से — मैं ज़रूर आऊँगा।", "bahut khuśī se — main zarūr āūṅgā.", "With pleasure — I will certainly come."),
                             X("माफ़ कीजिए, उस दिन काम है।", "māf kījie, us din kām hai.", "Sorry, I have work that day."),
                             X("क्या अगला रविवार ठीक है?", "kyā aglā ravivār ṭhīk hai?", "Is next Sunday all right?")],
                "mistakes": [{"wrong": "नहीं, मैं नहीं आऊँगा।",
                              "right": "माफ़ कीजिए, उस दिन मैं व्यस्त हूँ — क्या अगला रविवार ठीक है?",
                              "why": "a bare no ends the conversation. The apology, a general reason and a specific alternative together are what make the refusal acceptable."}],
            },
            "dialogue": [
                {"sp": "राहुल", "t": "शुक्रवार को चलें?", "r": "śukravār ko caleṅ?", "en": "Shall we go on Friday?"},
                {"sp": "मीरा", "t": "माफ़ कीजिए, शुक्रवार को काम है।", "r": "māf kījie, śukravār ko kām hai.", "en": "Sorry, I have work on Friday."},
                {"sp": "राहुल", "t": "कोई बात नहीं — तो कब?", "r": "koī bāt nahīṅ — to kab?", "en": "No matter — then when?"},
                {"sp": "मीरा", "t": "क्या अगला रविवार ठीक है? बहुत ख़ुशी से आऊँगी।", "r": "kyā aglā ravivār ṭhīk hai? bahut khuśī se āūṅgī.", "en": "Is next Sunday all right? I will come with pleasure."},
            ],
            "worksheet": {"title": "Accept/decline worksheet", "tasks": [
                {"instruction": "Accept warmly.", "items": ["with pleasure", "I will certainly come"], "key": ["बहुत ख़ुशी से", "मैं ज़रूर आऊँगा"]},
                {"instruction": "Decline and propose another day.", "items": ["Sorry, I am busy that day — is Sunday all right?"], "key": ["माफ़ कीजिए, उस दिन मैं व्यस्त हूँ — क्या रविवार ठीक है?"]},
            ]},
        },
        {
            "title": "On the phone: कौन? ज़रा रुकिए",
            "learn": ("Phone Hindi has its own fixed lines: नमस्ते (not hello), कौन बोल रहे हैं? (who "
                      "is speaking?), ज़रा रुकिए (hold on), मैं उन्हें बुला लाता हूँ (I will call him), "
                      "बाद में फ़ोन कीजिए (call later), ग़लत नंबर (wrong number). These are learned as "
                      "whole lines, not built."),
            "vocab": [V("कौन बोल रहे हैं", "kaun bol rahe haiṅ", "who is speaking?"),
                      V("ज़रा रुकिए", "zarā rukie", "hold on a moment"),
                      V("बुला लाता हूँ", "bulā lātā hūṅ", "I will call him/her"),
                      V("बाद में", "bād meṅ", "later"), V("ग़लत नंबर", "ġalat nambar", "wrong number"),
                      V("आवाज़", "āvāz", "voice", "noun"), V("संदेश", "sandesh", "message", "noun"),
                      V("काट दीजिए", "kāṭ dījie", "please hang up")],
            "grammar": {
                "title": "Fixed telephone lines",
                "explain": ("The phone script does not vary: नमस्ते … कौन बोल रहे हैं? … ज़रा रुकिए … "
                            "मैं उन्हें बुला लाता हूँ. To leave a message: संदेश दे दीजिए. If it is the "
                            "wrong number, ग़लत नंबर है, माफ़ कीजिए is complete — no explanation needed."),
                "pattern": "नमस्ते → कौन बोल रहे हैं? → ज़रा रुकिए → संदेश दे दीजिए",
                "examples": [X("नमस्ते, कौन बोल रहे हैं?", "namaste, kaun bol rahe haiṅ?", "Hello, who is speaking?"),
                             X("ज़रा रुकिए, मैं उन्हें बुला लाता हूँ।", "zarā rukie, main unheṅ bulā lātā hūṅ.", "Hold on, I will call him."),
                             X("माफ़ कीजिए, ग़लत नंबर है।", "māf kījie, ġalat nambar hai.", "Sorry, wrong number.")],
                "mistakes": [{"wrong": "हैलो, कौन है? (on a formal call)",
                              "right": "नमस्ते, कौन बोल रहे हैं?",
                              "why": "कौन है? is blunt on the phone; the respectful plural कौन बोल रहे हैं? is the polite standard, and नमस्ते opens a call where हैलो marks a stranger."}],
            },
            "dialogue": [
                {"sp": "राहुल", "t": "नमस्ते, क्या मीरा जी हैं?", "r": "namaste, kyā Mīrā jī haiṅ?", "en": "Hello, is that Meera?"},
                {"sp": "मीरा", "t": "जी, मैं मीरा बोल रही हूँ। कौन?", "r": "jī, main Mīrā bol rahī hūṅ. kaun?", "en": "Yes, Meera speaking. Who is this?"},
                {"sp": "राहुल", "t": "मैं राहुल। ज़रा रुकिए — प्रकाश जी से बात करनी है।", "r": "main Rāhul. zarā rukie — Prakāś jī se bāt karnī hai.", "en": "I am Rahul. One moment — I need to speak to Prakash."},
                {"sp": "मीरा", "t": "वे अभी नहीं हैं — संदेश दे दीजिए, मैं बता दूँगी।", "r": "ve abhī nahīṅ haiṅ — sandesh de dījie, main batā dūṅgī.", "en": "He is not here right now — give me the message, I will tell him."},
            ],
            "worksheet": {"title": "Phone worksheet", "tasks": [
                {"instruction": "Say it on the phone.", "items": ["who is speaking?", "hold on a moment", "wrong number"], "key": ["कौन बोल रहे हैं?", "ज़रा रुकिए", "ग़लत नंबर"]},
                {"instruction": "Leave a message.", "items": ["Tell him I called."], "key": ["बता दीजिए कि मैंने फ़ोन किया था।"]},
            ]},
        },
    ]),
]

A2P_EXTRA = {
    "culture": {
        "text": ("कहानी सुनाना — telling stories aloud — is a living habit, not a children's one. दीवाली "
                 "evenings are full of recited stories: the return of राम to अयोध्या in the Ramayana, "
                 "retold in Hindi from memory, with the teller pausing at the same places every year. "
                 "That pause is the craft: the teller stops just before the answer, and the listeners "
                 "fill it in. A learner telling a short story in Hindi is joining that habit, and the "
                 "sequence words (पहले, फिर, उसके बाद) are the whole of its scaffolding."),
        "source_url": "https://en.wikipedia.org/wiki/Diwali",
    },
    "reading": {
        "text": ("कल मेरा दिन बहुत अजीब था। पहले मैं दफ़्तर के लिए निकला, लेकिन गाड़ी छूट गई। "
                 "फिर मैंने ऑटो लिया और उसके बाद बस। जब मैं स्टेशन पहुँचा, तब तक दफ़्तर का समय "
                 "निकल गया था। अचानक फ़ोन आया — बॉस बोले, “आज घर से काम कर लीजिए।” आख़िर में मैं "
                 "घर लौटा और चाय बनाई। क्या दिन था! मुझे लगा कि सब बेकार हो गया, पर शाम को सब "
                 "ठीक निकला। कल फिर से जल्दी निकलूँगा।"),
        "gloss": ("Yesterday was a strange day. First I set out for the office, but the bus got "
                  "missed. Then I took an auto and after that a bus. When I reached the station, the "
                  "office time had already passed. Suddenly the phone rang — the boss said, “Work "
                  "from home today.” Finally I went back home and made tea. What a day! I felt "
                  "everything had been wasted, but by evening it all turned out fine. Tomorrow I "
                  "will set out early again."),
        "original": True,
    },
    "listening": {
        "script": ("— सुनो, कल शादी कैसी थी?\n"
                   "— क्या मज़ा आया! पहले हम देर से पहुँचे, फिर भीड़ में गुम हो गए।\n"
                   "— अच्छा! फिर क्या हुआ?\n"
                   "— उसके बाद अचानक मेरी बुआ मिल गईं — आख़िर में हम उनके साथ बैठ गए।\n"
                   "— और खाना?\n"
                   "— बहुत बढ़िया! मुझे तो हँसी आ गई जब सबने एक साथ नाच शुरू किया।"),
        "gloss": ("— Listen, how was the wedding yesterday?\n— What fun it was! First we arrived "
                  "late, then we got lost in the crowd.\n— Really! Then what happened?\n— After "
                  "that I suddenly met my bua — finally we sat down with her.\n— And the food?\n— "
                  "Excellent! I burst out laughing when everyone began to dance at once."),
        "voice_tag": VOICE,
    },
    "idioms": [
        {"t": "मुँह से निकलना", "literal": "to slip out of the mouth", "meaning": "to say something without meaning to"},
        {"t": "दिल लगना", "literal": "for the heart to attach", "meaning": "to feel at home, to enjoy being somewhere"},
        {"t": "बात बन जाना", "literal": "for the matter to be made", "meaning": "for something to work out, for a deal to come together"},
        {"t": "ग़लती से भी", "literal": "even by mistake", "meaning": "not even if you slipped — a strong never"},
        {"t": "जी भर कर", "literal": "having filled the heart", "meaning": "to one's heart's content, fully"},
        {"t": "छोटी-सी बात", "literal": "a small matter", "meaning": "it is nothing — the polite reply to thanks"},
        {"t": "टाइम निकल जाना", "literal": "for the time to leave", "meaning": "for the moment to have passed — too late now"},
        {"t": "माहौल बन जाना", "literal": "for the atmosphere to form", "meaning": "for a mood to settle over a group"},
        {"t": "हिम्मत करना", "literal": "to make courage", "meaning": "to pluck up the nerve"},
        {"t": "सुख-दुख", "literal": "happiness and pain", "meaning": "the whole of life's ups and downs, shared with someone"},
    ],
    "mistakes": [
        {"wrong": "कल हम फ़िल्म देखा।", "right": "कल हमने फ़िल्म देखी।",
         "why": "देखना is transitive, so the perfective needs ने and the verb agrees with फ़िल्म (feminine): देखी."},
        {"wrong": "जब मैं सोया, तब फ़ोन आया था।", "right": "जब मैं सो रहा था, तब फ़ोन आया।",
         "why": "the background takes the continuous था and the event takes the bare perfective. Swapping them makes both verbs sound like a summary."},
        {"wrong": "मैं आपको कल मिलूँगा। (arranging a meeting)", "right": "मैं आपसे कल मिलूँगा।",
         "why": "मिलना takes से — you meet *with* someone. आपको मिलूँगा means you will receive, which is a different sentence."},
    ],
    "task": {
        "title": "Tell the story of one day",
        "instructions": ("Write eight sentences about a single day you remember, in the past: where "
                         "you went, who you met, and one thing that went wrong. Use पहले, फिर, उसके "
                         "बाद and आख़िर में, at least one जब…तब sentence with रहा था, and finish with a "
                         "reaction (क्या मज़ा आया! / डर लगा / हँसी आ गई). Then record yourself telling "
                         "it aloud without reading. Do not correct yourself while speaking — the "
                         "fluency is the exercise, not the accuracy."),
    },
}

A2P_TEST = [
    ("multiple_choice", "Choose the reaction that means 'I see — and then?'.", "अच्छा, तो?"),
    ("fill_in_the_blank", "जब मैं सो ___ था, तब फ़ोन आया। (was sleeping)", "रहा"),
    ("translation", "क्या मज़ा आया!", "What fun it was!"),
    ("reverse_translation", "Tell me a little more.", "ज़रा और बताइए"),
    ("matching", "Match अचानक to its meaning.", "suddenly"),
    ("word_selection", "Select the Hindi for 'with pleasure'.", "बहुत ख़ुशी से"),
    ("error_correction", "मैं संगीत पसंद हूँ।", "मुझे संगीत पसंद है।"),
    ("dialogue_completion", "Complete: “कल हमारे घर ज़रूर आइए।” — “___?” (at what time)", "कितने बजे"),
    ("reading_comprehension", "कल मैं दफ़्तर के लिए निकला, लेकिन गाड़ी छूट गई। What went wrong?", "the bus was missed"),
    ("inference", "“ज़रा रुकिए, मैं उन्हें बुला लाता हूँ।” What is happening?", "the speaker is fetching someone"),
    ("main_idea", "पहले डर लगा, फिर सब ठीक हो गया। What is this sentence doing?", "ending a story on a relieved note"),
    ("detail_identification", "उसके बाद अचानक मेरी बुआ मिल गईं। Who was met?", "the speaker's father's sister"),
]

# ════════════════════════════════════════════════════════════════════════════
# B1+ · Comfortable  —  work in the language, argue a point politely
# ════════════════════════════════════════════════════════════════════════════
B1P_UNITS = [
    unit("B1P-U1", "Working in Hindi", [
        {
            "title": "Asking a colleague for something",
            "learn": ("Workplace requests are short and polite: ज़रा यह भेज दीजिए (please send this), "
                      "क्या आप मुझे फ़ाइल दे सकते हैं? (could you give me the file?), मुझे इसकी ज़रूरत "
                      "है (I need this). The compound भेज दीजिए is why the tone works: देना alone is "
                      "flat, देना with दीजिए hands the result over."),
            "vocab": [V("फ़ाइल", "fāil", "file", "noun"), V("भेज दीजिए", "bhej dījie", "please send it over"),
                      V("ज़रूरत", "zarūrat", "need", "noun"), V("काम", "kām", "work", "noun"),
                      V("समय", "samay", "time", "noun"), V("पूरा करना", "pūrā karnā", "to complete"),
                      V("बताइए", "batāie", "please tell"), V("मदद", "madad", "help", "noun")],
            "grammar": {
                "title": "क्या आप … सकते हैं? · ज़रा … दीजिए",
                "explain": ("क्या आप + verb stem + सकते हैं? is the standard 'could you': क्या आप यह "
                            "भेज सकते हैं? Its informal twin is ज़रा … दीजिए. मुझे इसकी ज़रूरत है states "
                            "the need without asking, which colleagues read as a request and learners "
                            "often miss."),
                "pattern": "क्या आप … सकते हैं? · ज़रा … दीजिए · मुझे इसकी ज़रूरत है",
                "examples": [X("क्या आप मुझे फ़ाइल भेज सकते हैं?", "kyā āp mujhe fāil bhej sakte haiṅ?", "Could you send me the file?"),
                             X("ज़रा यह ईमेल भेज दीजिए।", "zarā yah īmel bhej dījie.", "Please send this email over."),
                             X("मुझे इसकी ज़रूरत है — आज शाम तक।", "mujhe iskī zarūrat hai — āj śām tak.", "I need this — by this evening.")],
                "mistakes": [{"wrong": "आप यह भेजो। (to a colleague at work)",
                              "right": "क्या आप यह भेज दीजिए? / ज़रा यह भेज दीजिए।",
                              "why": "भेजो is तुम-form and behaves like an instruction. At work, even with a peer, the request shape is the norm — the difference is not hierarchy but register."}],
            },
            "dialogue": [
                {"sp": "राहुल", "t": "क्या आप मुझे पिछला फ़ाइल भेज सकते हैं?", "r": "kyā āp mujhe pichhlā fāil bhej sakte haiṅ?", "en": "Could you send me the previous file?"},
                {"sp": "मीरा", "t": "ज़रूर — अभी भेज देती हूँ।", "r": "zarūr — abhī bhej detī hūṅ.", "en": "Certainly — I am sending it now."},
                {"sp": "राहुल", "t": "धन्यवाद। इसकी ज़रूरत आज शाम तक है।", "r": "dhanyavād. iskī zarūrat āj śām tak hai.", "en": "Thank you. I need it by this evening."},
                {"sp": "मीरा", "t": "समझ गई। कुछ और चाहिए तो बताइए।", "r": "samajh gaī. kuchh aur cāhie to batāie.", "en": "Understood. If you need anything else, tell me."},
            ],
            "worksheet": {"title": "Workplace request worksheet", "tasks": [
                {"instruction": "Ask a colleague.", "items": ["send me the file", "help me with this"], "key": ["क्या आप मुझे फ़ाइल भेज सकते हैं?", "इसमें ज़रा मदद कीजिए।"]},
                {"instruction": "State a need and a deadline.", "items": ["I need this by tomorrow."], "key": ["मुझे इसकी ज़रूरत कल तक है।"]},
            ]},
        },
        {
            "title": "Explaining a delay",
            "learn": ("In a workplace, a delay is explained with देर हो गई (it got late) rather than a "
                      "blame sentence, plus a reason and a new deadline: देर हो गई क्योंकि फ़ाइल नहीं "
                      "मिली — कल शाम तक पूरा कर दूँगा. ठीक हो गया काम की वजह से (because of work) uses "
                      "की वजह से, the standard 'because of'."),
            "vocab": [V("देर हो गई", "der ho gaī", "it got late"), V("कारण", "kāraṇ", "reason", "noun"),
                      V("वजह से", "vajah se", "because of"), V("पूरा कर दूँगा", "pūrā kar dūṅgā", "I will finish it"),
                      V("अगली तारीख़", "aglī tārīkh", "the next date"), V("माफ़ी", "māfī", "apology", "noun"),
                      V("संभव नहीं", "sambhav nahīṅ", "not possible"), V("कोशिश करूँगा", "kośiś karūṅgā", "I will try")],
            "grammar": {
                "title": "देर हो गई, क्योंकि … — कल तक कर दूँगा",
                "explain": ("The delay is stated as an event with no agent (देर हो गई), the reason is "
                            "attached with क्योंकि or की वजह से, and the repair is a specific new "
                            "commitment (कल शाम तक कर दूँगा). Ending with माफ़ी in front — माफ़ी, देर हो "
                            "गई — is the normal opening of the whole move."),
                "pattern": "माफ़ी, देर हो गई क्योंकि … · … तक कर दूँगा",
                "examples": [X("माफ़ी, देर हो गई क्योंकि फ़ाइल नहीं मिली।", "māfī, der ho gaī kyoṅki fāil nahīṅ milī.", "Sorry, it got late because I could not find the file."),
                             X("ट्रैफ़िक की वजह से देर हो गई।", "ṭraifik kī vajah se der ho gaī.", "It got late because of the traffic."),
                             X("कोशिश करूँगा — कल शाम तक पूरा कर दूँगा।", "kośiś karūṅgā — kal śām tak pūrā kar dūṅgā.", "I will try — I will finish it by tomorrow evening.")],
                "mistakes": [{"wrong": "मैंने देर की।",
                              "right": "देर हो गई।",
                              "why": "मैंने देर की names you as the cause and sounds like a confession. देर हो गई reports the delay as something that happened — which is why it is the workplace form."}],
            },
            "dialogue": [
                {"sp": "प्रबंधक", "t": "रिपोर्ट कहाँ है? कल चाहिए थी।", "r": "riporṭ kahāṅ hai? kal cāhie thī.", "en": "Where is the report? It was needed yesterday."},
                {"sp": "राहुल", "t": "माफ़ी, देर हो गई क्योंकि आँकड़े अधूरे थे।", "r": "māfī, der ho gaī kyoṅki āṅkṛe adhūre the.", "en": "Sorry, it got late because the figures were incomplete."},
                {"sp": "प्रबंधक", "t": "तो अब कब तक?", "r": "to ab kab tak?", "en": "So by when now?"},
                {"sp": "राहुल", "t": "कल शाम तक पूरा कर दूँगा — कोशिश करूँगा, आज भी भेज दूँ।", "r": "kal śām tak pūrā kar dūṅgā — kośiś karūṅgā, āj bhī bhej dūṅ.", "en": "I will finish it by tomorrow evening — I will try to send it today as well."},
            ],
            "worksheet": {"title": "Delay worksheet", "tasks": [
                {"instruction": "Explain a delay and give a new date.", "items": ["Sorry, I got held up — I will finish by Monday."], "key": ["माफ़ी, देर हो गई — सोमवार तक पूरा कर दूँगा।"]},
                {"instruction": "Use की वजह से.", "items": ["because of traffic", "because of illness"], "key": ["ट्रैफ़िक की वजह से", "बीमारी की वजह से"]},
            ]},
        },
        {
            "title": "Email and message register",
            "learn": ("Written workplace Hindi opens with नमस्ते or प्रिय (dear) and closes with "
                      "धन्यवाद and सादर (respectfully). The body uses सूचित करना (to inform), कृपया "
                      "(please), and भेज रहा हूँ (I am sending). प्रिय is for letters and formal email; "
                      "नमस्ते works for both and is safer."),
            "vocab": [V("सूचित करना", "sūcit karnā", "to inform"), V("कृपया", "kṛpayā", "please (written)"),
                      V("भेज रहा हूँ", "bhej rahā hūṅ", "I am sending"), V("संलग्न", "saṅlagn", "attached"),
                      V("सादर", "sādar", "respectfully (closing)"), V("विषय", "viṣay", "subject", "noun"),
                      V("प्रतिक्रिया", "pratikriyā", "response / feedback", "noun"),
                      V("कृपया जाँच लीजिए", "kṛpayā jāṅc lījie", "please check it")],
            "grammar": {
                "title": "Opening, body verbs, closing",
                "explain": ("Hindi email has three fixed zones. Opening: नमस्ते / प्रिय. Body: सूचित "
                            "करना (inform), कृपया … (please), संलग्न है (is attached), प्रतिक्रिया दीजिए "
                            "(give feedback). Closing: धन्यवाद / सादर. The body prefers the passive-ish "
                            "impersonal: संलग्न फ़ाइल कृपया देख लीजिए."),
                "pattern": "नमस्ते → सूचित करता हूँ कि … → कृपया … → धन्यवाद/सादर",
                "examples": [X("नमस्ते, सूचित कर रहा हूँ कि फ़ाइल संलग्न है।", "namaste, sūcit kar rahā hūṅ ki fāil saṅlagn hai.", "Hello, I am informing you that the file is attached."),
                             X("कृपया इसे जाँच लीजिए।", "kṛpayā ise jāṅc lījie.", "Please check this."),
                             X("धन्यवाद। सादर।", "dhanyavād. sādar.", "Thank you. Respectfully.")],
                "mistakes": [{"wrong": "मैं आपको बताता हूँ कि फ़ाइल भेज दिया।",
                              "right": "सूचित करता हूँ कि फ़ाइल भेज दी गई है।",
                              "why": "बताना is conversational; written workplace Hindi uses सूचित करना. And a sent file is reported as भेज दी गई है — the thing, not the person, carries the verb."}],
            },
            "dialogue": [
                {"sp": "राहुल", "t": "ईमेल में विषय क्या लिखूँ?", "r": "īmel meṅ viṣay kyā likhūṅ?", "en": "What should I write as the email subject?"},
                {"sp": "मीरा", "t": "“रिपोर्ट — अंतिम प्रति” ठीक रहेगा।", "r": "“riporṭ — antim prati” ṭhīk rahegā.", "en": "“Report — final copy” will do."},
                {"sp": "राहुल", "t": "और अंदर?", "r": "aur andar?", "en": "And inside?"},
                {"sp": "मीरा", "t": "सूचित करता हूँ कि संलग्न फ़ाइल अंतिम है। कृपया जाँच लीजिए और प्रतिक्रिया दीजिए। धन्यवाद — सादर।", "r": "sūcit kartā hūṅ ki saṅlagn fāil antim hai. kṛpayā jāṅc lījie aur pratikriyā dījie. dhanyavād — sādar.", "en": "I am informing you that the attached file is final. Please check it and give feedback. Thank you — respectfully."},
            ],
            "worksheet": {"title": "Email worksheet", "tasks": [
                {"instruction": "Write the three zones.", "items": ["opening", "informing + attached", "closing"], "key": ["नमस्ते", "सूचित करता हूँ कि फ़ाइल संलग्न है।", "धन्यवाद — सादर"]},
                {"instruction": "Ask for feedback politely.", "items": ["please check and give feedback"], "key": ["कृपया जाँचकर प्रतिक्रिया दीजिए।"]},
            ]},
        },
    ]),
    unit("B1P-U2", "Arguing a point politely", [
        {
            "title": "Reasons: क्योंकि, इसलिए, इसका मतलब है कि",
            "learn": ("क्योंकि gives the reason after the fact, इसलिए gives the result after the "
                      "reason, and इसका मतलब है कि draws the inference. Only one of क्योंकि/इसलिए "
                      "belongs in a sentence pair — using both is the commonest B1 slip: क्योंकि बारिश "
                      "हुई, इसलिए हम रुके (not क्योंकि… इसलिए… in the same clause)."),
            "vocab": [V("क्योंकि", "kyoṅki", "because"), V("इसलिए", "islie", "therefore"),
                      V("इसका मतलब है", "iskā matlab hai", "this means"),
                      V("वजह", "vajah", "reason", "noun"), V("नतीजा", "natījā", "result", "noun"),
                      V("फ़ायदा", "fāydā", "benefit", "noun"), V("नुक़सान", "nuqsān", "loss / harm", "noun"),
                      V("साफ़ है", "sāf hai", "it is clear")],
            "grammar": {
                "title": "One reason, one result",
                "explain": ("क्योंकि … इसलिए never pair inside one bound sentence: either बारिश हुई, "
                            "इसलिए हम रुके, or हम रुके क्योंकि बारिश हुई. In writing they can meet only "
                            "across two full sentences. इसका मतलब है कि introduces what follows from "
                            "what was just said, and it is the workhorse of an argument."),
                "pattern": "… इसलिए … · … क्योंकि … · इसका मतलब है कि …",
                "examples": [X("बारिश हुई, इसलिए हम रुके।", "bāriś huī, islie ham ruke.", "It rained, so we stopped."),
                             X("हम रुके क्योंकि बारिश हो रही थी।", "ham ruke kyoṅki bāriś ho rahī thī.", "We stopped because it was raining."),
                             X("इसका मतलब है कि योजना बदलनी पड़ेगी।", "iskā matlab hai ki yojnā badalnī paṛegī.", "This means the plan will have to change.")],
                "mistakes": [{"wrong": "क्योंकि बारिश हुई, इसलिए हम रुके।",
                              "right": "बारिश हुई, इसलिए हम रुके। / हम रुके क्योंकि बारिश हुई।",
                              "why": "क्योंकि and इसलिए each carry the same link from opposite ends. Keeping both in one sentence is the English 'because … so' pattern, which Hindi does not use."}],
            },
            "dialogue": [
                {"sp": "साथी", "t": "हम आज क्यों नहीं शुरू कर रहे?", "r": "ham āj kyoṅ nahīṅ śurū kar rahe?", "en": "Why are we not starting today?"},
                {"sp": "मीरा", "t": "क्योंकि बजट अभी मंज़ूर नहीं हुआ।", "r": "kyoṅki bajat abhī manzūr nahīṅ huā.", "en": "Because the budget has not been approved yet."},
                {"sp": "साथी", "t": "तो?" , "r": "to?", "en": "So?"},
                {"sp": "मीरा", "t": "इसका मतलब है कि हमें एक हफ़्ते और रुकना पड़ेगा।", "r": "iskā matlab hai ki hameṅ ek hafte aur ruknā paṛegā.", "en": "This means we will have to wait another week."},
            ],
            "worksheet": {"title": "Reasons worksheet", "tasks": [
                {"instruction": "Link them — one direction only.", "items": ["It rained. We stopped. (result)", "We stopped. It was raining. (reason)"], "key": ["बारिश हुई, इसलिए हम रुके।", "हम रुके क्योंकि बारिश हो रही थी।"]},
                {"instruction": "Draw the inference.", "items": ["The file is late, so the meeting will move."], "key": ["फ़ाइल देर से आई — इसका मतलब है कि बैठक आगे बढ़ेगी।"]},
            ]},
        },
        {
            "title": "Adding and contrasting: इसके अलावा, हालाँकि",
            "learn": ("इसके अलावा (besides this) adds a point in the same direction; दूसरी ओर (on the "
                      "other hand) and हालाँकि (although) turn. The order matters: Hindi builds the "
                      "case first and turns late, and a turn that arrives in the first sentence reads "
                      "as a refusal to discuss."),
            "vocab": [V("इसके अलावा", "iske alāvā", "besides this"), V("दूसरी ओर", "dūsrī or", "on the other hand"),
                      V("हालाँकि", "hālāṅki", "although"), V("लेकिन", "lekin", "but"),
                      V("इसके विपरीत", "iske viprīt", "on the contrary"), V("और भी", "aur bhī", "even more"),
                      V("ज़रूरी", "zarūrī", "important / necessary"), V("मुख्य", "mukhya", "main / chief")],
            "grammar": {
                "title": "Add, then turn",
                "explain": ("इसके अलावा and और भी extend the argument; हालाँकि is a written 'although' "
                            "that opens a clause, and दूसरी ओर balances two sides. लेकिन joins inside a "
                            "sentence. The pattern in a paragraph: claim, इसके अलावा, लेकिन/हालाँकि — the "
                            "turn is last because the reader needs the case in hand before it turns."),
                "pattern": "… इसके अलावा … · हालाँकि …, फिर भी … · दूसरी ओर …",
                "examples": [X("यह योजना सस्ती है। इसके अलावा, यह जल्दी बन सकती है।", "yah yojnā sastī hai. iske alāvā, yah jaldī ban saktī hai.", "This plan is cheap. Besides, it can be built quickly."),
                             X("हालाँकि ख़र्च कम है, फिर भी जोखिम है।", "hālāṅki kharc kam hai, phir bhī jokhim hai.", "Although the cost is low, there is still a risk."),
                             X("दूसरी ओर, समय भी कम है।", "dūsrī or, samay bhī kam hai.", "On the other hand, time is short too.")],
                "mistakes": [{"wrong": "हालाँकि मैं सहमत नहीं हूँ, लेकिन बात अच्छी है।",
                              "right": "हालाँकि बात अच्छी है, फिर भी मैं पूरी तरह सहमत नहीं हूँ।",
                              "why": "हालाँकि leads with the concession and फिर भी carries the turn. Reversing them makes the sentence disagree before it has heard the point."}],
            },
            "dialogue": [
                {"sp": "राहुल", "t": "यह प्रस्ताव कैसा लगा?", "r": "yah prastāv kaisā lagā?", "en": "How did this proposal seem?"},
                {"sp": "मीरा", "t": "यह सस्ता है। इसके अलावा, जल्दी लागू हो सकता है।", "r": "yah sastā hai. iske alāvā, jaldī lāgū ho saktā hai.", "en": "It is cheap. Besides, it can be implemented quickly."},
                {"sp": "राहुल", "t": "तो आप सहमत हैं?", "r": "to āp sahmat haiṅ?", "en": "So you agree?"},
                {"sp": "मीरा", "t": "हालाँकि यह सस्ता है, फिर भी एक दिक्कत है — कर्मचारी नहीं हैं।", "r": "hālāṅki yah sastā hai, phir bhī ek dikkat hai — karmcārī nahīṅ haiṅ.", "en": "Although it is cheap, there is still one problem — there are no staff."},
            ],
            "worksheet": {"title": "Contrast worksheet", "tasks": [
                {"instruction": "Add a supporting point.", "items": ["It is fast. (also) it is cheap."], "key": ["यह तेज़ है। इसके अलावा, यह सस्ता भी है।"]},
                {"instruction": "Concede first, then turn.", "items": ["although the cost is low, the risk remains"], "key": ["हालाँकि ख़र्च कम है, फिर भी जोखिम है।"]},
            ]},
        },
        {
            "title": "Disagreeing without a fight",
            "learn": ("The polite disagreement concedes a piece, names the gap, and proposes: आपकी बात "
                      "सही है, पर एक बात रह गई (your point is right, but one thing was missed). मुझे लगता "
                      "है (it seems to me) softens everything after it, and थोड़ी आपत्ति है (I have a "
                      "small objection) is how a formal objection opens."),
            "vocab": [V("आपकी बात सही है", "āpkī bāt sahī hai", "your point is right"),
                      V("एक बात रह गई", "ek bāt rah gaī", "one thing was missed"),
                      V("मुझे लगता है", "mujhe lagtā hai", "it seems to me"),
                      V("थोड़ी आपत्ति", "thoṛī āpatti", "a small objection"),
                      V("सोचना पड़ेगा", "socnā paṛegā", "we will have to think"),
                      V("सुझाव", "sujhāv", "suggestion", "noun"), V("विकल्प", "vikalp", "alternative", "noun"),
                      V("फ़ैसला", "faislā", "decision", "noun")],
            "grammar": {
                "title": "Concede, name the gap, propose",
                "explain": ("Three beats: आपकी बात सही है (concede), पर एक बात रह गई / मुझे लगता है कि "
                            "(gap), तो हम … कर सकते हैं? (propose). मुझे लगता है takes the को-form and "
                            "can carry a whole objection politely — मुझे लगता है कि यह समय कम है."),
                "pattern": "आपकी बात सही है, पर … · मुझे लगता है कि … · तो हम … कर सकते हैं?",
                "examples": [X("आपकी बात सही है, पर एक बात रह गई।", "āpkī bāt sahī hai, par ek bāt rah gaī.", "Your point is right, but one thing was missed."),
                             X("मुझे लगता है कि समय कम है।", "mujhe lagtā hai ki samay kam hai.", "I feel the time is short."),
                             X("तो हम आधा काम पहले कर सकते हैं? — यह एक विकल्प है।", "to ham ādhā kām pahle kar sakte haiṅ? — yah ek vikalp hai.", "So could we do half the work first? — that is one alternative.")],
                "mistakes": [{"wrong": "नहीं, यह ग़लत है।",
                              "right": "मुझे लगता है कि इसमें एक दिक्कत है।",
                              "why": "a flat यह ग़लत है attacks the person's judgement; मुझे लगता है कि statement moves the disagreement onto the point itself, which is what lets the discussion continue."}],
            },
            "dialogue": [
                {"sp": "साथी", "t": "मेरा सुझाव है कि हम सब कुछ अगले हफ़्ते कर लें।", "r": "merā sujhāv hai ki ham sab kuchh agle hafte kar leṅ.", "en": "My suggestion is that we do everything next week."},
                {"sp": "मीरा", "t": "आपकी बात सही है, पर एक बात रह गई — टीम छोटी है।", "r": "āpkī bāt sahī hai, par ek bāt rah gaī — ṭīm chhoṭī hai.", "en": "Your point is right, but one thing was missed — the team is small."},
                {"sp": "साथी", "t": "तो आपका क्या सुझाव है?", "r": "to āpkā kyā sujhāv hai?", "en": "Then what do you suggest?"},
                {"sp": "मीरा", "t": "मुझे लगता है कि पहले आधा काम करें — यह एक विकल्प है, फ़ैसला आपका।", "r": "mujhe lagtā hai ki pahle ādhā kām kareṅ — yah ek vikalp hai, faislā āpkā.", "en": "I feel we should do half first — this is one alternative, the decision is yours."},
            ],
            "worksheet": {"title": "Disagreement worksheet", "tasks": [
                {"instruction": "Soften each disagreement.", "items": ["यह ग़लत है।", "नहीं, समय कम है।"], "key": ["मुझे लगता है कि इसमें एक दिक्कत है।", "आपकी बात सही है, पर मुझे लगता है कि समय कम है।"]},
                {"instruction": "Concede, gap, propose.", "items": ["The plan is good, but the cost is high — do half first."], "key": ["आपकी बात सही है, पर ख़र्च ज़्यादा है — पहले आधा करें।"]},
            ]},
        },
    ]),
    unit("B1P-U3", "Institutional Hindi", [
        {
            "title": "Forms and offices: आवेदन, प्रमाण, हस्ताक्षर",
            "learn": ("A form in Hindi asks for the same few things in a fixed order: नाम, पिता का नाम, "
                      "पता, तारीख़, हस्ताक्षर. What you submit is an आवेदन (application), what proves "
                      "something is a प्रमाण (certificate), and what you keep is a प्रतिलिपि (copy). "
                      "Learning these five words removes most of the fear of an Indian office."),
            "vocab": [V("आवेदन", "āvedan", "application", "noun"), V("प्रमाण", "pramāṇ", "certificate / proof", "noun"),
                      V("हस्ताक्षर", "hastākṣar", "signature", "noun"), V("तारीख़", "tārīkh", "date", "noun"),
                      V("प्रतिलिपि", "pratilipi", "copy", "noun"), V("फ़ॉर्म", "form", "form", "noun"),
                      V("जमा करना", "jamā karnā", "to submit"), V("कतार", "katār", "queue", "noun")],
            "grammar": {
                "title": "जमा करना · के लिए · कहाँ मिलेगा?",
                "explain": ("Applications are जमा करना (submitted) at a desk, and के लिए marks what they "
                            "are for: वीज़ा के लिए आवेदन. To find the right window: प्रमाण पत्र कहाँ "
                            "मिलेगा? and to check requirements: क्या चाहिए? — क्या मूल प्रमाण चाहिए या "
                            "प्रतिलिपि?"),
                "pattern": "… के लिए आवेदन · … जमा करना · कहाँ मिलेगा?",
                "examples": [X("मुझे प्रमाण पत्र कहाँ मिलेगा?", "mujhe pramāṇ patra kahāṅ milegā?", "Where can I get the certificate?"),
                             X("क्या मूल चाहिए या प्रतिलिपि?", "kyā mūl cāhie yā pratilipi?", "Is the original needed or a copy?"),
                             X("यह आवेदन यहाँ जमा कीजिए।", "yah āvedan yahāṅ jamā kījie.", "Submit this application here.")],
                "mistakes": [{"wrong": "मैं प्रमाण लेने आया। (at a government window)",
                              "right": "मुझे प्रमाण पत्र लेना है। / प्रमाण कहाँ मिलेगा?",
                              "why": "मैं … आया announces your purpose; the counter expects the requirement. The को-form marks you as the person the document is for, which is what the clerk is checking."}],
            },
            "dialogue": [
                {"sp": "नागरिक", "t": "माफ़ कीजिए, जन्म प्रमाण पत्र कहाँ मिलेगा?", "r": "māf kījie, janm pramāṇ patra kahāṅ milegā?", "en": "Excuse me, where can I get a birth certificate?"},
                {"sp": "क्लर्क", "t": "खिड़की चार पर। आवेदन भर दीजिए।", "r": "khiṛkī cār par. āvedan bhar dījie.", "en": "At window four. Fill in the application."},
                {"sp": "नागरिक", "t": "क्या मूल दस्तावेज़ चाहिए या प्रतिलिपि?", "r": "kyā mūl dastāvez cāhie yā pratilipi?", "en": "Is the original document needed or a copy?"},
                {"sp": "क्लर्क", "t": "प्रतिलिपि ठीक है — पर हस्ताक्षर और तारीख़ ज़रूरी है।", "r": "pratilipi ṭhīk hai — par hastākṣar aur tārīkh zarūrī hai.", "en": "A copy is fine — but the signature and date are essential."},
            ],
            "worksheet": {"title": "Office worksheet", "tasks": [
                {"instruction": "Ask at a counter.", "items": ["Where can I get the certificate?", "Is the original needed or a copy?"], "key": ["प्रमाण पत्र कहाँ मिलेगा?", "मूल चाहिए या प्रतिलिपि?"]},
                {"instruction": "Name the items.", "items": ["application", "signature", "date"], "key": ["आवेदन", "हस्ताक्षर", "तारीख़"]},
            ]},
        },
        {
            "title": "Official verbs: सूचित, निवेदन, अनुरोध",
            "learn": ("Three verbs run institutional Hindi: सूचित करना (to inform), निवेदन करना (to "
                      "request, formal and slightly supplicating), अनुरोध करना (to request, neutral). "
                      "They are used impersonally — सूचित किया जाता है (it is informed), निवेदन है कि … "
                      "(it is requested that …) — which is exactly why a letter looks unlike speech."),
            "vocab": [V("सूचित करना", "sūcit karnā", "to inform"), V("निवेदन करना", "nivedan karnā", "to request (formal)"),
                      V("अनुरोध करना", "anurodh karnā", "to request"), V("आदेश", "ādeś", "order / instruction", "noun"),
                      V("निर्देश", "nirdeś", "direction / instruction", "noun"), V("स्वीकार करना", "svīkār karnā", "to accept"),
                      V("अस्वीकार करना", "asvīkār karnā", "to reject"), V("प्रक्रिया", "prakriyā", "procedure", "noun")],
            "grammar": {
                "title": "Impersonal institutional verbs",
                "explain": ("Institutional writing prefers the impersonal: सूचित किया जाता है, निवेदन है "
                            "कि, आदेश दिया गया है. The passive जाना-form removes the person, which is "
                            "the point — a notice is not about who wrote it. In speech the same content "
                            "uses बताया and कहा; the switch is register, not grammar."),
                "pattern": "सूचित किया जाता है · निवेदन है कि … · आदेश दिया गया है",
                "examples": [X("सूचित किया जाता है कि दफ़्तर कल बंद रहेगा।", "sūcit kiyā jātā hai ki daftar kal band rahegā.", "It is notified that the office will remain closed tomorrow."),
                             X("निवेदन है कि समय पर पहुँचिए।", "nivedan hai ki samay par pahuṅcie.", "It is requested that you arrive on time."),
                             X("आदेश दिया गया है — प्रक्रिया बदल दी गई है।", "ādeś diyā gayā hai — prakriyā badal dī gaī hai.", "An order has been given — the procedure has been changed.")],
                "mistakes": [{"wrong": "मैं आपको सूचित करता हूँ। (in a formal notice)",
                              "right": "सूचित किया जाता है। / आपको सूचित किया जाता है।",
                              "why": "a notice speaks for the office, not for a person. The first-person verb makes it a private letter, and clerks read that as unofficial."}],
            },
            "dialogue": [
                {"sp": "क्लर्क", "t": "यह सूचना पढ़िए — दफ़्तर कल बंद रहेगा।", "r": "yah sūcnā paṛhie — daftar kal band rahegā.", "en": "Read this notice — the office will be closed tomorrow."},
                {"sp": "नागरिक", "t": "तो प्रक्रिया कब से?", "r": "to prakriyā kab se?", "en": "So from when does the procedure apply?"},
                {"sp": "क्लर्क", "t": "सूचित किया जाता है कि बदलाव अगले सोमवार से है।", "r": "sūcit kiyā jātā hai ki badlāv agle somvār se hai.", "en": "It is notified that the change is from next Monday."},
                {"sp": "नागरिक", "t": "निवेदन है कि लिखकर दे दीजिए।", "r": "nivedan hai ki likhkar de dījie.", "en": "It is requested that you give it to me in writing."},
            ],
            "worksheet": {"title": "Official verbs worksheet", "tasks": [
                {"instruction": "Turn it impersonal.", "items": ["मैं सूचित करता हूँ कि …", "मैं अनुरोध करता हूँ कि …"], "key": ["सूचित किया जाता है कि …", "अनुरोध किया जाता है कि … / निवेदन है कि …"]},
                {"instruction": "Read a notice aloud.", "items": ["The office will remain closed tomorrow."], "key": ["सूचित किया जाता है कि दफ़्तर कल बंद रहेगा।"]},
            ]},
        },
        {
            "title": "Asking for clarification",
            "learn": ("The most valuable institutional sentence is मैं समझा नहीं, ज़रा दोबारा बताइए (I did "
                      "not understand, please tell me again). Then: कृपया स्पष्ट कीजिए (please clarify), "
                      "इसका मतलब क्या है? (what does this mean?), लिखकर दे दीजिए (give it in writing). "
                      "Nobody minds being asked twice; everybody minds being misunderstood."),
            "vocab": [V("स्पष्ट", "spaṣṭ", "clear"), V("स्पष्ट कीजिए", "spaṣṭ kījie", "please clarify"),
                      V("समझा नहीं", "samjhā nahīṅ", "did not understand"),
                      V("दोबारा", "dobārā", "again"), V("मतलब", "matlab", "meaning", "noun"),
                      V("लिखकर दीजिए", "likhkar dījie", "please give it in writing"),
                      V("धीरे", "dhīre", "slowly"), V("ज़रूरी काग़ज़", "zarūrī kāġaz", "required papers")],
            "grammar": {
                "title": "मैं समझा नहीं · कृपया स्पष्ट कीजिए",
                "explain": ("समझा नहीं is the fixed shape of 'I did not get it' — masculine agreement for "
                            "a male speaker, समझी नहीं for a female speaker. कृपया स्पष्ट कीजिए is the "
                            "polite request for a clarification, and लिखकर दीजिए asks for it in writing, "
                            "which in a government office is a completely normal request."),
                "pattern": "मैं समझा/समझी नहीं · कृपया स्पष्ट कीजिए · लिखकर दे दीजिए",
                "examples": [X("माफ़ कीजिए, मैं समझा नहीं।", "māf kījie, main samjhā nahīṅ.", "Sorry, I did not understand."),
                             X("कृपया स्पष्ट कीजिए — कौन-से काग़ज़ चाहिए?", "kṛpayā spaṣṭ kījie — kaun-se kāġaz cāhie?", "Please clarify — which papers are needed?"),
                             X("ज़रा धीरे बताइए, और लिखकर दे दीजिए।", "zarā dhīre batāie, aur likhkar de dījie.", "Tell me slowly, and give it in writing.")],
                "mistakes": [{"wrong": "क्या? फिर से बोलो।",
                              "right": "माफ़ कीजिए, मैं समझा नहीं — ज़रा दोबारा बताइए।",
                              "why": "क्या? plus बोलो is the तुम-form and reads as irritation. The apology plus the polite repeat request is what keeps a counter conversation moving."}],
            },
            "dialogue": [
                {"sp": "क्लर्क", "t": "पहले फ़ॉर्म, फिर प्रतिलिपि, और अंत में शुल्क।", "r": "pahle fŏrm, phir pratilipi, aur ant meṅ śulk.", "en": "First the form, then a copy, and finally the fee."},
                {"sp": "नागरिक", "t": "माफ़ कीजिए, मैं समझा नहीं।", "r": "māf kījie, main samjhā nahīṅ.", "en": "Sorry, I did not understand."},
                {"sp": "क्लर्क", "t": "कोई बात नहीं — कृपया ध्यान से सुनिए।", "r": "koī bāt nahīṅ — kṛpayā dhyān se sunie.", "en": "No matter — please listen carefully."},
                {"sp": "नागरिक", "t": "ज़रा धीरे बताइए, और निवेदन है कि लिखकर दे दीजिए।", "r": "zarā dhīre batāie, aur nivedan hai ki likhkar de dījie.", "en": "Please tell me slowly, and I request that you give it in writing."},
            ],
            "worksheet": {"title": "Clarification worksheet", "tasks": [
                {"instruction": "Ask for a repeat, politely.", "items": ["I did not understand.", "please clarify"], "key": ["मैं समझा नहीं।", "कृपया स्पष्ट कीजिए।"]},
                {"instruction": "Ask for it in writing.", "items": ["Please give it in writing."], "key": ["निवेदन है कि लिखकर दे दीजिए।"]},
            ]},
        },
    ]),
]

B1P_EXTRA = {
    "culture": {
        "text": ("Hinglish — Hindi and English mixed inside a sentence — is the ordinary register of "
                 "Indian offices, and treating it as bad Hindi misunderstands how it works. The mixing "
                 "follows rules: English supplies nouns and technical terms (file, meeting, deadline, "
                 "report), Hindi supplies the grammar that carries them (भेज दीजिए, हो गया, कर लीजिए). "
                 "A learner who can say फ़ाइल भेज दीजिए sounds more fluent to a colleague than one who "
                 "builds a pure-Hindi sentence nobody in that office has ever spoken — and the same "
                 "learner still needs the formal register for anything written."),
        "source_url": "https://en.wikipedia.org/wiki/Hinglish",
    },
    "reading": {
        "text": ("पिछले हफ़्ते दफ़्तर में एक बैठक हुई। विषय था: नई प्रक्रिया। पहले प्रबंधक ने बताया कि "
                 "फ़ॉर्म बदल गया है। इसके अलावा, अब हस्ताक्षर के साथ तारीख़ भी ज़रूरी है। कुछ लोगों ने "
                 "आपत्ति की — पुरानी प्रक्रिया आसान थी। हालाँकि उनकी बात सही थी, फिर भी बदलाव ज़रूरी "
                 "था। आख़िर में तय हुआ कि नई प्रक्रिया अगले सोमवार से लागू होगी, और सबको लिखकर "
                 "सूचित किया जाएगा। मैंने भी एक सुझाव रखा: एक हफ़्ते का समय दिया जाए। मान लिया गया।"),
        "gloss": ("Last week there was a meeting at the office. The subject was: the new procedure. "
                  "First the manager said that the form has changed. Besides that, a date is now needed "
                  "along with the signature. Some people objected — the old procedure was easier. "
                  "Although their point was right, the change was still necessary. Finally it was "
                  "decided that the new procedure would apply from next Monday, and everyone would be "
                  "informed in writing. I also put forward a suggestion: that a week's time be given. "
                  "It was accepted."),
        "original": True,
    },
    "listening": {
        "script": ("— सुनिए, क्या फ़ाइल भेज दी आपने?\n"
                   "— माफ़ी, देर हो गई — आँकड़े अधूरे थे।\n"
                   "— तो अब कब तक?\n"
                   "— कोशिश करूँगा कि आज शाम तक भेज दूँ।\n"
                   "— ठीक है। और हाँ — अगली बार मुझे पहले बता दीजिए, ताकि बैठक में दिक्कत न हो।\n"
                   "— ज़रूर। इस बार मेरी ग़लती थी।"),
        "gloss": ("— Listen, did you send the file?\n— Sorry, it got late — the figures were "
                  "incomplete.\n— So by when now?\n— I will try to send it by this evening.\n— All "
                  "right. And yes — next time tell me in advance, so there is no trouble in the "
                  "meeting.\n— Certainly. This time it was my mistake."),
        "voice_tag": VOICE,
    },
    "idioms": [
        {"t": "काम चलाना", "literal": "to make the work go", "meaning": "to manage, to keep things ticking over"},
        {"t": "हाथ बटाना", "literal": "to fold in one's hand", "meaning": "to lend a hand, to help with work"},
        {"t": "सिर पर काम होना", "literal": "work on the head", "meaning": "to be buried in work"},
        {"t": "दो-टूक बात", "literal": "a two-piece statement", "meaning": "plain speaking, straight talk"},
        {"t": "बात टालना", "literal": "to postpone the matter", "meaning": "to put somebody off, to keep deferring"},
        {"t": "हिसाब बराबर", "literal": "the account is equal", "meaning": "we are even, settled"},
        {"t": "मिलकर चलना", "literal": "to walk together", "meaning": "to work together, to accommodate each other"},
        {"t": "हिम्मत बँधना", "literal": "for courage to be tied on", "meaning": "to take heart from someone's support"},
        {"t": "बात का पक्का", "literal": "firm in one's word", "meaning": "a person who keeps a commitment"},
        {"t": "ठंडे दिमाग़ से", "literal": "with a cool brain", "meaning": "calmly, without heat"},
    ],
    "mistakes": [
        {"wrong": "मैंने उसे मदद किया।", "right": "मैंने उसकी मदद की।",
         "why": "मदद is a noun, and helping someone is उसकी मदद करना — the helper is the owner. मदद किया treats it like a verb and is heard immediately."},
        {"wrong": "बैठक में मैंने कहा कि मुझे देर होगी। (reporting a past statement)", "right": "बैठक में मैंने कहा कि मुझे देर होगी। / … हो जाएगी।",
         "why": "Hindi keeps the tense of reported speech, so होगी stays futuristic inside a past sentence. Learners shift it to past because English would — and the sentence then claims a delay that has already been decided differently."},
        {"wrong": "कृपया आप इसको देख लीजिए।", "right": "कृपया इसे देख लीजिए।",
         "why": "कृपया plus आप doubles the politeness and reads as stiff, and thisको/उसको is conversational where इसे is the written form. Institutional Hindi trims rather than layers."},
    ],
    "task": {
        "title": "Write a workplace message twice",
        "instructions": ("Write the same message two ways: once as a WhatsApp note to a colleague, once "
                         "as an email to a manager. Same request, same deadline. Then underline every "
                         "place the two versions differ — the pronouns, the verbs, the closing. The "
                         "difference between the two versions is the register, and learning to see it is "
                         "the point of this rung."),
    },
}

B1P_TEST = [
    ("multiple_choice", "Choose the polite workplace request.", "क्या आप मुझे फ़ाइल भेज सकते हैं?"),
    ("fill_in_the_blank", "माफ़ी, देर हो ___ — आँकड़े अधूरे थे। (it got late)", "गई"),
    ("translation", "सूचित किया जाता है कि दफ़्तर कल बंद रहेगा।", "It is notified that the office will remain closed tomorrow."),
    ("reverse_translation", "Please clarify — which papers are needed?", "कृपया स्पष्ट कीजिए — कौन-से काग़ज़ चाहिए?"),
    ("matching", "Match हस्ताक्षर to its meaning.", "signature"),
    ("word_selection", "Select the Hindi for 'besides this'.", "इसके अलावा"),
    ("error_correction", "क्योंकि बारिश हुई, इसलिए हम रुके।", "बारिश हुई, इसलिए हम रुके।"),
    ("dialogue_completion", "Complete: “रिपोर्ट कहाँ है?” — “माफ़ी, ___।” (it got late)", "देर हो गई"),
    ("reading_comprehension", "हालाँकि उनकी बात सही थी, फिर भी बदलाव ज़रूरी था। What does this say?", "the objection was right but the change was still necessary"),
    ("inference", "“निवेदन है कि लिखकर दे दीजिए।” What is the speaker after?", "a written record of the instruction"),
    ("main_idea", "इसका मतलब है कि हमें एक हफ़्ते और रुकना पड़ेगा। What role does this sentence play?", "drawing the consequence of what was just said"),
    ("detail_identification", "प्रतिलिपि ठीक है — पर हस्ताक्षर और तारीख़ ज़रूरी है। What must be on the form?", "a signature and a date"),
]

# ════════════════════════════════════════════════════════════════════════════
# B2+ · Professional  —  run a meeting, read a contract, disagree well
# ════════════════════════════════════════════════════════════════════════════
B2P_UNITS = [
    unit("B2P-U1", "Running a meeting", [
        {
            "title": "Opening and agenda: कार्यसूची",
            "learn": ("A meeting opens in three sentences: बैठक शुरू कीजिए (let us begin), आज के तीन "
                      "विषय हैं (there are three items today), and the time limit — एक घंटा है. The "
                      "agenda is कार्यसूची in written Hindi and एजेंडा in speech, and naming the items "
                      "up front is what stops the meeting drifting."),
            "vocab": [V("बैठक", "baiṭhak", "meeting", "noun"), V("कार्यसूची", "kāryasūcī", "agenda", "noun"),
                      V("विषय", "viṣay", "item / topic", "noun"), V("समय-सीमा", "samay-sīmā", "time limit", "noun"),
                      V("शुरू कीजिए", "śurū kījie", "please begin"), V("उपस्थित", "upasthit", "present (attending)"),
                      V("अनुपस्थित", "anupasthit", "absent"), V("कार्यवृत्त", "kāryavṛtt", "minutes (of a meeting)", "noun")],
            "grammar": {
                "title": "आज के तीन विषय हैं",
                "explain": ("The opening states the count and the clock: आज के तीन विषय हैं, एक घंटा है, "
                            "इसलिए हर विषय पर बीस मिनट. Structure words do the work — पहला विषय (first "
                            "item), दूसरा (second), तीसरा (third), and आख़िर में (finally). Minutes are "
                            "कार्यवृत्त in writing, and the closing line is कार्यवृत्त भेज दीजिए."),
                "pattern": "बैठक शुरू कीजिए · आज के … विषय हैं · … मिनट प्रति विषय",
                "examples": [X("बैठक शुरू कीजिए — आज के तीन विषय हैं।", "baiṭhak śurū kījie — āj ke tīn viṣay haiṅ.", "Let us begin — there are three items today."),
                             X("पहला विषय: बजट। दूसरा: समय-सीमा।", "pahlā viṣay: bajat. dūsrā: samay-sīmā.", "First item: budget. Second: timeline."),
                             X("एक घंटा है, इसलिए हर विषय पर बीस मिनट।", "ek ghaṇṭā hai, islie har viṣay par bīs miniṭ.", "There is one hour, so twenty minutes per item.")],
                "mistakes": [{"wrong": "आज हम बहुत बातें करेंगे।",
                              "right": "आज के तीन विषय हैं — एक घंटा है।",
                              "why": "an open agenda is how meetings run over. Naming the count and the clock at the start is a B2+ skill, not politeness — it is what makes the rest enforceable."}],
            },
            "dialogue": [
                {"sp": "अध्यक्ष", "t": "बैठक शुरू कीजिए। आज के तीन विषय हैं।", "r": "baiṭhak śurū kījie. āj ke tīn viṣay haiṅ.", "en": "Let us begin. There are three items today."},
                {"sp": "अध्यक्ष", "t": "पहला विषय: बजट। एक घंटा है, हर विषय पर बीस मिनट।", "r": "pahlā viṣay: bajat. ek ghaṇṭā hai, har viṣay par bīs miniṭ.", "en": "First item: budget. One hour, twenty minutes per item."},
                {"sp": "सदस्य", "t": "क्या मैं एक बात जोड़ सकता हूँ?", "r": "kyā main ek bāt joṛ saktā hūṅ?", "en": "May I add one point?"},
                {"sp": "अध्यक्ष", "t": "ज़रूर — पर छोटी रखिए, समय कम है।", "r": "zarūr — par chhoṭī rakhiye, samay kam hai.", "en": "Certainly — but keep it short, time is short."},
            ],
            "worksheet": {"title": "Meeting opening worksheet", "tasks": [
                {"instruction": "Open a meeting in three sentences.", "items": ["begin", "three items", "time limit"], "key": ["बैठक शुरू कीजिए।", "आज के तीन विषय हैं।", "एक घंटा है।"]},
                {"instruction": "Ask to add a point.", "items": ["May I add one point?"], "key": ["क्या मैं एक बात जोड़ सकता हूँ?"]},
            ]},
        },
        {
            "title": "Moderating: turn-taking and time",
            "learn": ("Moderating is a set of interruptions that do not offend: ज़रा रुकिए (just a "
                      "moment), पहले उन्हें बोलने दीजिए (let them speak first), आपका विषय बाद में "
                      "(your item is later), एक-एक करके (one at a time). The moderator's job is to "
                      "protect the clock, and the phrases protect the speaker too."),
            "vocab": [V("ज़रा रुकिए", "zarā rukie", "just a moment"), V("बोलने दीजिए", "bolne dījie", "let (them) speak"),
                      V("एक-एक करके", "ek-ek karke", "one at a time"), V("बाद में", "bād meṅ", "later"),
                      V("समय कम है", "samay kam hai", "time is short"), V("संक्षेप में", "saṅkṣep meṅ", "in brief"),
                      V("बिंदु", "bindu", "point", "noun"), V("प्राथमिकता", "prāthamiktā", "priority", "noun")],
            "grammar": {
                "title": "Interrupting without offending",
                "explain": ("Every interruption carries an acknowledgement before the cut: बहुत सही "
                            "बात, पर ज़रा रुकिए — वक्त कम है. Letting others speak is बोलने दीजिए, and "
                            "deferring an item is politely explicit: आपका विषय तीसरा है, बाद में लेंगे. "
                            "संक्षेप में कहिए is the standard request to shorten a long speech."),
                "pattern": "बहुत सही बात, पर ज़रा रुकिए · पहले उन्हें बोलने दीजिए · संक्षेप में कहिए",
                "examples": [X("बहुत सही बात, पर ज़रा रुकिए — समय कम है।", "bahut sahī bāt, par zarā rukie — samay kam hai.", "A fair point, but just a moment — time is short."),
                             X("पहले उन्हें बोलने दीजिए।", "pahle unheṅ bolne dījie.", "Let them speak first."),
                             X("संक्षेप में कहिए — बिंदु पर आइए।", "saṅkṣep meṅ kahie — bindu par āie.", "Say it in brief — come to the point.")],
                "mistakes": [{"wrong": "चुप रहिए! आप बाद में बोलिए।",
                              "right": "अच्छी बात है — पर पहले उन्हें बोलने दीजिए, फिर आप।",
                              "why": "चुप रहिए silences a person; ordering the floor does not. The acknowledgement plus the turn order keeps the meeting working and the colleague intact."}],
            },
            "dialogue": [
                {"sp": "सदस्य", "t": "मैं कहना चाहता हूँ कि बजट से ज़्यादा ज़रूरी टीम है, क्योंकि पिछली बार…", "r": "main kahnā cāhtā hūṅ ki bajat se zyādā zarūrī ṭīm hai, kyoṅki pichhlī bār…", "en": "I want to say the team matters more than the budget, because last time…"},
                {"sp": "अध्यक्ष", "t": "बहुत सही बात, पर ज़रा रुकिए — बिंदु पर आइए।", "r": "bahut sahī bāt, par zarā rukie — bindu par āie.", "en": "A fair point, but just a moment — come to the point."},
                {"sp": "सदस्य", "t": "संक्षेप में: टीम नहीं तो काम नहीं।", "r": "saṅkṣep meṅ: ṭīm nahīṅ to kām nahīṅ.", "en": "In brief: no team, no work."},
                {"sp": "अध्यक्ष", "t": "ठीक। पहले उन्हें बोलने दीजिए, फिर आपका विषय।", "r": "ṭhīk. pahle unheṅ bolne dījie, phir āpkā viṣay.", "en": "Fine. Let them speak first, then your item."},
            ],
            "worksheet": {"title": "Moderation worksheet", "tasks": [
                {"instruction": "Interrupt politely.", "items": ["keep to the point", "say it in brief", "let them speak first"], "key": ["बिंदु पर आइए।", "संक्षेप में कहिए।", "पहले उन्हें बोलने दीजिए।"]},
                {"instruction": "Defer an item.", "items": ["Your item is third, we will take it later."], "key": ["आपका विषय तीसरा है, बाद में लेंगे।"]},
            ]},
        },
        {
            "title": "Decisions and action items",
            "learn": ("A meeting ends with decisions and owners: तय हुआ कि … (it was decided that …), "
                      "ज़िम्मेदारी किसकी है? (whose responsibility is it?), और समय? (and by when?). "
                      "The written record is कार्यवृत्त, and the closing line is कार्यवृत्त भेज दीजिए "
                      "— with names attached, or nothing will happen."),
            "vocab": [V("निर्णय", "nirṇay", "decision", "noun"), V("तय हुआ", "tay huā", "it was decided"),
                      V("ज़िम्मेदारी", "zimmdārī", "responsibility", "noun"), V("कार्य-विभाजन", "kārya-vibhājan", "division of work", "noun"),
                      V("समय-सीमा", "samay-sīmā", "deadline", "noun"), V("कार्यवृत्त", "kāryavṛtt", "minutes", "noun"),
                      V("अगली बैठक", "aglī baiṭhak", "next meeting", "noun"), V("लिखकर भेजिए", "likhkar bhejie", "send it in writing")],
            "grammar": {
                "title": "तय हुआ कि … · ज़िम्मेदारी किसकी? · … तक",
                "explain": ("Decisions are recorded impersonally — तय हुआ कि नई प्रक्रिया सोमवार से "
                            "लागू होगी — and then made concrete with a name and a date: ज़िम्मेदारी "
                            "राहुल की, सोमवार तक. Without the second half the first half is a wish. "
                            "कार्यवृत्त भेज दीजिए closes every meeting, and it is the sentence that "
                            "keeps the decisions alive."),
                "pattern": "तय हुआ कि … · ज़िम्मेदारी … की · … तक · कार्यवृत्त भेज दीजिए",
                "examples": [X("तय हुआ कि नई प्रक्रिया सोमवार से लागू होगी।", "tay huā ki naī prakriyā somvār se lāgū hogī.", "It was decided that the new procedure will apply from Monday."),
                             X("ज़िम्मेदारी राहुल की — सोमवार तक।", "zimmdārī Rāhul kī — somvār tak.", "Rahul is responsible — by Monday."),
                             X("कार्यवृत्त आज शाम तक भेज दीजिए।", "kāryavṛtt āj śām tak bhej dījie.", "Send the minutes by this evening.")],
                "mistakes": [{"wrong": "तय हुआ कि जल्दी करना चाहिए।",
                              "right": "तय हुआ कि प्रक्रिया सोमवार से लागू होगी; ज़िम्मेदारी राहुल की।",
                              "why": "a decision without an owner and a date is not a decision — जल्दी करना चाहिए commits nobody. The two-part form is what the record has to carry."}],
            },
            "dialogue": [
                {"sp": "अध्यक्ष", "t": "तो चलिए, निर्णय लिख लें।", "r": "to calie, nirṇay likh leṅ.", "en": "So let us write the decisions."},
                {"sp": "सदस्य", "t": "तय हुआ कि फ़ॉर्म सोमवार से बदलेगा।", "r": "tay huā ki fŏrm somvār se badlegā.", "en": "It was decided the form changes from Monday."},
                {"sp": "अध्यक्ष", "t": "ज़िम्मेदारी किसकी, और कब तक?", "r": "zimmdārī kiskī, aur kab tak?", "en": "Whose responsibility, and by when?"},
                {"sp": "सदस्य", "t": "मीरा की — बुधवार तक। और कार्यवृत्त आज भेज दीजिए।", "r": "Mīrā kī — budhvār tak. aur kāryavṛtt āj bhej dījie.", "en": "Meera's — by Wednesday. And send the minutes today."},
            ],
            "worksheet": {"title": "Decisions worksheet", "tasks": [
                {"instruction": "Record a decision properly.", "items": ["The form changes from Monday.", "Meera is responsible, by Wednesday."], "key": ["तय हुआ कि फ़ॉर्म सोमवार से बदलेगा।", "ज़िम्मेदारी मीरा की — बुधवार तक।"]},
                {"instruction": "Close the meeting.", "items": ["send the minutes today"], "key": ["कार्यवृत्त आज भेज दीजिए।"]},
            ]},
        },
    ]),
    unit("B2P-U2", "Contracts and conditions", [
        {
            "title": "Obligations: करना होगा, अनिवार्य है",
            "learn": ("A contract is made of obligations. In Hindi they are करना होगा (will have to do), "
                      "अनिवार्य है (is mandatory), and शर्त के अनुसार (according to the condition). "
                      "The party is named with को: कंपनी को भुगतान करना होगा. Nothing in a contract is "
                      "expressed as a desire."),
            "vocab": [V("करना होगा", "karnā hogā", "will have to do"), V("अनिवार्य", "anivārya", "mandatory"),
                      V("शर्त", "śart", "condition", "noun"), V("अनुसार", "anusār", "according to"),
                      V("पालन करना", "pālan karnā", "to comply"), V("भुगतान", "bhugtān", "payment", "noun"),
                      V("पक्षकार", "pakṣkār", "party (to an agreement)", "noun"), V("लागू होना", "lāgū honā", "to apply / come into force")],
            "grammar": {
                "title": "… को … करना होगा",
                "explain": ("Obligation puts the party in the को-form and the verb in the infinitive plus "
                            "होगा: कंपनी को भुगतान करना होगा. Conditions attach with शर्त के अनुसार or "
                            "के मुताबिक़. अनिवार्य है states it flatly, and पालन करना is what one does "
                            "with a rule — शर्तों का पालन करना होगा."),
                "pattern": "X को … करना होगा · शर्त के अनुसार … · … का पालन करना होगा",
                "examples": [X("कंपनी को हर महीने भुगतान करना होगा।", "kampnī ko har mahīne bhugtān karnā hogā.", "The company will have to pay every month."),
                             X("शर्त के अनुसार नोटिस देना अनिवार्य है।", "śart ke anusār noṭis denā anivārya hai.", "According to the condition, giving notice is mandatory."),
                             X("दोनों पक्षों को समय-सीमा का पालन करना होगा।", "donoṅ pakṣoṅ ko samay-sīmā kā pālan karnā hogā.", "Both parties will have to comply with the deadline.")],
                "mistakes": [{"wrong": "कंपनी भुगतान करेगी। (in a contract clause)",
                              "right": "कंपनी को भुगतान करना होगा।",
                              "why": "करेगी predicts what will happen; करना होगा states what is required. A contract records requirements, and the difference is exactly what a lawyer reads for."}],
            },
            "dialogue": [
                {"sp": "वकील", "t": "भुगतान की शर्त क्या है?", "r": "bhugtān kī śart kyā hai?", "en": "What is the payment condition?"},
                {"sp": "अधिकारी", "t": "शर्त के अनुसार कंपनी को हर महीने भुगतान करना होगा।", "r": "śart ke anusār kampnī ko har mahīne bhugtān karnā hogā.", "en": "According to the condition, the company must pay monthly."},
                {"sp": "वकील", "t": "और देर होने पर?", "r": "aur der hone par?", "en": "And if there is a delay?"},
                {"sp": "अधिकारी", "t": "देर होने पर नोटिस देना अनिवार्य है — दोनों पक्षों पर लागू।", "r": "der hone par noṭis denā anivārya hai — donoṅ pakṣoṅ par lāgū.", "en": "On delay, giving notice is mandatory — it applies to both parties."},
            ],
            "worksheet": {"title": "Obligation worksheet", "tasks": [
                {"instruction": "Write the obligation.", "items": ["The company must pay monthly.", "Both parties must give notice."], "key": ["कंपनी को हर महीने भुगतान करना होगा।", "दोनों पक्षों को नोटिस देना होगा।"]},
                {"instruction": "Use अनुसार.", "items": ["according to the condition"], "key": ["शर्त के अनुसार"]},
            ]},
        },
        {
            "title": "Rights, dates and exceptions",
            "learn": ("The other half of a contract is what is not required: के अलावा (besides/in "
                      "addition to), को छोड़कर (except for), और संशोधन (amendment). A right is अधिकार "
                      "and a fixed date is नियत तिथि. Reading a clause aloud means pausing exactly at "
                      "के अलावा and को छोड़कर, because everything after them changes the obligation."),
            "vocab": [V("अधिकार", "adhikār", "right", "noun"), V("नियत तिथि", "niyat tithi", "fixed date", "noun"),
                      V("के अलावा", "ke alāvā", "in addition to"), V("को छोड़कर", "ko chhoṛkar", "except for"),
                      V("संशोधन", "saṅśodhan", "amendment", "noun"), V("मान्य", "mānya", "valid"),
                      V("अमान्य", "amānya", "invalid"), V("समाप्ति", "samāpti", "termination / end", "noun")],
            "grammar": {
                "title": "छोड़कर and के अलावा move the whole clause",
                "explain": ("को छोड़कर cuts something out of what came before: सोमवार को छोड़कर (except "
                            "Monday). के अलावा adds: अधिकारों के अलावा कर्तव्य भी हैं. संशोधन लिखित रूप "
                            "में ज़रूरी है — an amendment must be in writing — is the standard clause, "
                            "and मान्य/अमान्य decide whether anything stands."),
                "pattern": "X को छोड़कर · X के अलावा · संशोधन लिखित रूप में मान्य है",
                "examples": [X("रविवार को छोड़कर हर दिन डिलीवरी होगी।", "ravivār ko chhoṛkar har din ḍilīvarī hogī.", "Delivery will be on every day except Sunday."),
                             X("अधिकारों के अलावा कर्तव्य भी हैं।", "adhikāroṅ ke alāvā kartavya bhī haiṅ.", "Besides the rights there are also duties."),
                             X("संशोधन लिखित रूप में ही मान्य होगा।", "saṅśodhan likhit rūp meṅ hī mānya hogā.", "An amendment is valid only in written form.")],
                "mistakes": [{"wrong": "रविवार को छोड़कर, डिलीवरी हर दिन नहीं होगी।",
                              "right": "रविवार को छोड़कर, डिलीवरी हर दिन होगी।",
                              "why": "को छोड़कर removes the exception, so the rest stands positive. Adding an extra negation flips the clause — the commonest reading error on a delivery term."}],
            },
            "dialogue": [
                {"sp": "वकील", "t": "डिलीवरी कब-कब होगी?", "r": "ḍilīvarī kab-kab hogī?", "en": "When will the deliveries be?"},
                {"sp": "अधिकारी", "t": "रविवार को छोड़कर हर दिन — नियत तिथि के अंदर।", "r": "ravivār ko chhoṛkar har din — niyat tithi ke andar.", "en": "Every day except Sunday — within the fixed date."},
                {"sp": "वकील", "t": "और संशोधन?", "r": "aur saṅśodhan?", "en": "And amendments?"},
                {"sp": "अधिकारी", "t": "अधिकारों के अलावा कर्तव्य भी हैं — संशोधन लिखित रूप में ही मान्य है।", "r": "adhikāroṅ ke alāvā kartavya bhī haiṅ — saṅśodhan likhit rūp meṅ hī mānya hai.", "en": "Besides the rights there are duties — an amendment is valid only in writing."},
            ],
            "worksheet": {"title": "Clauses worksheet", "tasks": [
                {"instruction": "Say the exception correctly.", "items": ["every day except Sunday", "all sections except the last"], "key": ["रविवार को छोड़कर हर दिन", "अंतिम भाग को छोड़कर सभी धाराएँ"]},
                {"instruction": "State the amendment rule.", "items": ["Amendments are valid only in writing."], "key": ["संशोधन लिखित रूप में ही मान्य होंगे।"]},
            ]},
        },
        {
            "title": "Reading a clause aloud and asking about scope",
            "learn": ("A clause is read out in pieces, and the listener checks the scope after each piece: "
                      "धारा (section), उपबंध (provision), दायरा (scope). The three questions that "
                      "prevent surprises are: यह किस पर लागू होता है? (to whom does it apply?), कब तक "
                      "मान्य है? (how long is it valid?), और अगर ऐसा हो तो? (and if that happens?)."),
            "vocab": [V("धारा", "dhārā", "section (of a text)", "noun"), V("उपबंध", "upabandh", "provision", "noun"),
                      V("दायरा", "dāyrā", "scope", "noun"), V("लागू होना", "lāgū honā", "to apply"),
                      V("कब तक", "kab tak", "until when"), V("ऐसा हो तो", "aisā ho to", "if that happens"),
                      V("स्पष्ट कीजिए", "spaṣṭ kījie", "please clarify"), V("समझौता", "samjhautā", "agreement", "noun")],
            "grammar": {
                "title": "किस पर लागू होता है? · कब तक मान्य है?",
                "explain": ("Scope questions use पर लागू होना (to apply to): यह उपबंध किन पर लागू होता है? "
                            "Validity uses कब तक मान्य है? and conditions use अगर … तो. Asking these three "
                            "after each clause is a technique, not a sign of weakness — it is how the "
                            "people who read contracts professionally do it."),
                "pattern": "यह … पर लागू होता है? · कब तक मान्य है? · अगर … तो क्या होगा?",
                "examples": [X("यह उपबंध किस पर लागू होता है?", "yah upabandh kis par lāgū hotā hai?", "To whom does this provision apply?"),
                             X("समझौता कब तक मान्य रहेगा?", "samjhautā kab tak mānya rahegā?", "Until when will the agreement be valid?"),
                             X("अगर भुगतान देर से हो, तो क्या होगा?", "agar bhugtān der se ho, to kyā hogā?", "If the payment is late, what happens?")],
                "mistakes": [{"wrong": "समझ गया, आगे पढ़िए। (after a clause you did not fully follow)",
                              "right": "ज़रा एक बात स्पष्ट कीजिए — यह किस पर लागू होता है?",
                              "why": "nodding on is how people agree to terms they later dispute. The clarification question is normal in every reading, and it is far cheaper than a disagreement later."}],
            },
            "dialogue": [
                {"sp": "वकील", "t": "अब धारा पाँच पढ़ता हूँ।", "r": "ab dhārā pāṅc paṛhtā hūṅ.", "en": "Now I will read section five."},
                {"sp": "अधिकारी", "t": "ज़रा रुकिए — यह उपबंध किस पर लागू होता है?", "r": "zarā rukie — yah upabandh kis par lāgū hotā hai?", "en": "Just a moment — to whom does this provision apply?"},
                {"sp": "वकील", "t": "दोनों पक्षों पर, पर समझौता कब तक मान्य रहेगा यह धारा आठ में है।", "r": "donoṅ pakṣoṅ par, par samjhautā kab tak mānya rahegā yah dhārā āṭh meṅ hai.", "en": "To both parties, but how long the agreement stays valid is in section eight."},
                {"sp": "अधिकारी", "t": "अच्छा। और अगर भुगतान देर से हो, तो क्या होगा?", "r": "achchhā. aur agar bhugtān der se ho, to kyā hogā?", "en": "Fine. And if the payment is late, what happens?"},
            ],
            "worksheet": {"title": "Scope worksheet", "tasks": [
                {"instruction": "Ask the three scope questions.", "items": ["to whom?", "until when?", "if that happens?"], "key": ["किस पर लागू होता है?", "कब तक मान्य है?", "अगर ऐसा हो तो क्या होगा?"]},
                {"instruction": "Name the parts.", "items": ["section", "provision", "scope"], "key": ["धारा", "उपबंध", "दायरा"]},
            ]},
        },
    ]),
    unit("B2P-U3", "Disagreeing well under pressure", [
        {
            "title": "Asserting with evidence",
            "learn": ("A claim under pressure needs its evidence attached: आँकड़े बताते हैं कि … (the "
                      "figures show that …), पिछले साल के मुक़ाबले … (compared with last year …), "
                      "इससे साफ़ है कि … (from this it is clear that …). Ungrounded assertions are what "
                      "make a discussion turn personal."),
            "vocab": [V("आँकड़े", "āṅkṛe", "figures / data", "noun"), V("बताते हैं कि", "batāte haiṅ ki", "they show that"),
                      V("के मुक़ाबले", "ke muqāble", "compared with"), V("साफ़ है कि", "sāf hai ki", "it is clear that"),
                      V("प्रमाण", "pramāṇ", "evidence", "noun"), V("दावा", "dāvā", "claim", "noun"),
                      V("आधार", "ādhār", "basis / foundation", "noun"), V("निष्कर्ष", "niṣkarṣ", "conclusion", "noun")],
            "grammar": {
                "title": "दावा + आधार + निष्कर्ष",
                "explain": ("The professional assertion has three parts: the claim (दावा), its basis "
                            "(आधार — आँकड़े, रिपोर्ट, अनुभव), and the conclusion (निष्कर्ष). Hindi "
                            "marks the basis with से: आँकड़ों से साफ़ है कि … and the comparison with के "
                            "मुक़ाबले. Saying आधार के बिना दावा कमज़ोर होता है is itself the standard "
                            "warning in a meeting."),
                "pattern": "आँकड़ों से साफ़ है कि … · पिछले साल के मुक़ाबले … · दावा किस आधार पर?",
                "examples": [X("आँकड़ों से साफ़ है कि माँग बढ़ रही है।", "āṅkṛoṅ se sāf hai ki māṅg baṛh rahī hai.", "From the figures it is clear that demand is growing."),
                             X("पिछले साल के मुक़ाबले अब ख़र्च कम है।", "pichhle sāl ke muqāble ab kharc kam hai.", "Compared with last year the cost is lower now."),
                             X("दावा किस आधार पर है?", "dāvā kis ādhār par hai?", "What is the claim based on?")],
                "mistakes": [{"wrong": "मुझे लगता है कि माँग बढ़ रही है। (as the only support)",
                              "right": "आँकड़ों से साफ़ है कि माँग बढ़ रही है — इसका आधार यह रिपोर्ट है।",
                              "why": "मुझे लगता है politely signals an ungrounded opinion; in a decision meeting that invites the counter-opinion and settles nothing. Attach the basis instead."}],
            },
            "dialogue": [
                {"sp": "सदस्य", "t": "मेरा दावा है कि माँग बढ़ रही है।", "r": "merā dāvā hai ki māṅg baṛh rahī hai.", "en": "My claim is that demand is growing."},
                {"sp": "अध्यक्ष", "t": "आधार क्या है?", "r": "ādhār kyā hai?", "en": "What is the basis?"},
                {"sp": "सदस्य", "t": "आँकड़ों से साफ़ है — पिछले साल के मुक़ाबले बीस प्रतिशत बढ़ोतरी।", "r": "āṅkṛoṅ se sāf hai — pichhle sāl ke muqāble bīs pratiśat baṛhotrī.", "en": "The figures make it clear — a twenty percent rise over last year."},
                {"sp": "अध्यक्ष", "t": "ठीक है, यह निष्कर्ष मान लेते हैं।", "r": "ṭhīk hai, yah niṣkarṣ mān lete haiṅ.", "en": "Good, let us accept this conclusion."},
            ],
            "worksheet": {"title": "Evidence worksheet", "tasks": [
                {"instruction": "Ground the claim.", "items": ["Demand is growing. (figures)", "Cost is lower. (compared with last year)"], "key": ["आँकड़ों से साफ़ है कि माँग बढ़ रही है।", "पिछले साल के मुक़ाबले ख़र्च कम है।"]},
                {"instruction": "Ask for the basis.", "items": ["What is the claim based on?"], "key": ["दावा किस आधार पर है?"]},
            ]},
        },
        {
            "title": "Conceding without collapsing",
            "learn": ("Conceding is a technique: मान लीजिए कि यह सही है (suppose that is right), फिर भी "
                      "(even so), सीमित सहमति (limited agreement). The skill is the size of the "
                      "concession — concede the specific and hold the general. और एक बात (and one more "
                      "thing) keeps your own case on the table while you concede."),
            "vocab": [V("मान लीजिए", "mān lījie", "suppose"), V("फिर भी", "phir bhī", "even so"),
                      V("सीमित सहमति", "sīmit sahmati", "limited agreement", "noun"),
                      V("एक बात", "ek bāt", "one point"), V("स्वीकार करना", "svīkār karnā", "to accept"),
                      V("अंतर", "antar", "difference", "noun"), V("जोर", "zor", "emphasis / force", "noun"),
                      V("टिकना", "ṭiknā", "to hold / to stand")],
            "grammar": {
                "title": "मान लीजिए …, फिर भी … · सीमित सहमति",
                "explain": ("मान लीजिए invites the other side's strongest version into the sentence; फिर "
                            "भी carries the turn; the concession is then named as limited — इस बिंदु पर "
                            "सीमित सहमति है. The general claim survives because it was never conceded: "
                            "the specific point was."),
                "pattern": "मान लीजिए … सही है, फिर भी … · इस बिंदु पर सहमति है, पर …",
                "examples": [X("मान लीजिए यह आँकड़ा सही है, फिर भी निष्कर्ष नहीं बदलता।", "mān lījie yah āṅkṛā sahī hai, phir bhī niṣkarṣ nahīṅ badaltā.", "Suppose this figure is right; even so the conclusion does not change."),
                             X("इस बिंदु पर सीमित सहमति है।", "is bindu par sīmit sahmati hai.", "There is limited agreement on this point."),
                             X("और एक बात — समय भी तो देखिए।", "aur ek bāt — samay bhī to dekhie.", "And one more thing — look at the time as well.")],
                "mistakes": [{"wrong": "आप सही हैं, सब कुछ ग़लत था।",
                              "right": "आपका यह बिंदु सही है, फिर भी बाक़ी निष्कर्ष टिकता है।",
                              "why": "conceding everything ends the argument and your case with it. A named, limited concession keeps the discussion alive and your position standing."}],
            },
            "dialogue": [
                {"sp": "सदस्य", "t": "आपका अनुमान ग़लत था।", "r": "āpkā anumān ġalat thā.", "en": "Your estimate was wrong."},
                {"sp": "अध्यक्ष", "t": "मान लीजिए वह आँकड़ा सही है, फिर भी निष्कर्ष नहीं बदलता।", "r": "mān lījie vah āṅkṛā sahī hai, phir bhī niṣkarṣ nahīṅ badaltā.", "en": "Suppose that figure is right; even so the conclusion does not change."},
                {"sp": "सदस्य", "t": "तो आप मानते हैं कि ग़लती हुई?", "r": "to āp mānte haiṅ ki ġalatī huī?", "en": "So you accept there was a mistake?"},
                {"sp": "अध्यक्ष", "t": "इस बिंदु पर सीमित सहमति है। और एक बात — पूरा निष्कर्ष इस पर नहीं टिकता।", "r": "is bindu par sīmit sahmati hai. aur ek bāt — pūrā niṣkarṣ is par nahīṅ ṭiktā.", "en": "There is limited agreement on this point. And one more thing — the whole conclusion does not rest on it."},
            ],
            "worksheet": {"title": "Concession worksheet", "tasks": [
                {"instruction": "Concede narrowly.", "items": ["Suppose the figure is right — the conclusion still holds."], "key": ["मान लीजिए आँकड़ा सही है, फिर भी निष्कर्ष टिकता है।"]},
                {"instruction": "State limited agreement.", "items": ["limited agreement on this point"], "key": ["इस बिंदु पर सीमित सहमति है।"]},
            ]},
        },
        {
            "title": "De-escalating and the written follow-up",
            "learn": ("When a discussion heats up, Hindi de-escalates by moving to process: इसे बाद में "
                      "लेंगे (we will take this later), ज़रा ठंडे दिमाग़ से सोचिए (think about it calmly), "
                      "लिखकर भेज दीजिए (send it in writing). The written follow-up is where the "
                      "agreement actually gets made — बातचीत के बाद लिखित सहमति."),
            "vocab": [V("ठंडे दिमाग़ से", "ṭhaṇḍe dimāġ se", "calmly"), V("बाद में लेंगे", "bād meṅ leṅge", "we will take it later"),
                      V("लिखित सहमति", "likhit sahmati", "written agreement", "noun"),
                      V("सारांश", "sārāṅś", "summary", "noun"), V("मुद्दा", "muddā", "issue / point", "noun"),
                      V("सुलझाना", "suljhānā", "to resolve"), V("बातचीत", "bātcīt", "discussion", "noun"),
                      V("आगे बढ़ना", "āge baṛhnā", "to move forward")],
            "grammar": {
                "title": "Move to process, then to paper",
                "explain": ("De-escalation has three moves: defer (इसे बाद में लेंगे), lower the "
                            "temperature (ज़रा ठंडे दिमाग़ से सोचिए), and shift to writing (लिखकर भेज दीजिए "
                            "— मुद्दे साफ़ हो जाएँगे). सारांश बनाकर भेजता हूँ ('I will send a summary') is "
                            "how a meeting ends without a fight and with a record."),
                "pattern": "इसे बाद में लेंगे · ठंडे दिमाग़ से सोचिए · सारांश बनाकर भेजिए",
                "examples": [X("इसे बाद में लेंगे — अभी नहीं।", "ise bād meṅ leṅge — abhī nahīṅ.", "We will take this later — not now."),
                             X("ज़रा ठंडे दिमाग़ से सोचिए।", "zarā ṭhaṇḍe dimāġ se socie.", "Think about it calmly."),
                             X("मैं सारांश बनाकर भेजता हूँ — लिखित सहमति से मुद्दे साफ़ होंगे।", "main sārāṅś banākar bhejtā hūṁ — likhit sahmati se mudde sāf hoṅge.", "I will send a summary — a written agreement will make the issues clear.")],
                "mistakes": [{"wrong": "आप नहीं समझ रहे! (in a professional discussion)",
                              "right": "ज़रा ठंडे दिमाग़ से सोचिए — मैं सारांश भेजता हूँ।",
                              "why": "आप नहीं समझ रहे makes it about the person; moving to a summary makes it about the record. The record is what survives the meeting."}],
            },
            "dialogue": [
                {"sp": "सदस्य", "t": "यह बात आगे नहीं बढ़ रही।", "r": "yah bāt āge nahīṅ baṛh rahī.", "en": "This is not moving forward."},
                {"sp": "अध्यक्ष", "t": "इसे बाद में लेंगे — अभी ज़रा ठंडे दिमाग़ से सोचिए।", "r": "ise bād meṅ leṅge — abhī zarā ṭhaṇḍe dimāġ se socie.", "en": "We will take this later — for now, think about it calmly."},
                {"sp": "सदस्य", "t": "तो क्या तय हुआ?", "r": "to kyā tay huā?", "en": "So what was decided?"},
                {"sp": "अध्यक्ष", "t": "मैं सारांश बनाकर भेजता हूँ। जो मुद्दे बाक़ी हैं, वे लिखित रूप में लेंगे।", "r": "main sārāṅś banākar bhejtā hūṁ. jo mudde bāqī haiṅ, ve likhit rūp meṅ leṅge.", "en": "I will send a summary. The open issues we will take up in writing."},
            ],
            "worksheet": {"title": "De-escalation worksheet", "tasks": [
                {"instruction": "De-escalate in three moves.", "items": ["defer", "cool down", "move to writing"], "key": ["इसे बाद में लेंगे।", "ज़रा ठंडे दिमाग़ से सोचिए।", "लिखकर भेज दीजिए।"]},
                {"instruction": "Close with a record.", "items": ["I will send a summary."], "key": ["मैं सारांश भेजता हूँ।"]},
            ]},
        },
    ]),
]

B2P_EXTRA = {
    "culture": {
        "text": ("In Indian professional life the document and the discussion live in different "
                 "registers. A contract is written in English and read in English; the meeting around it "
                 "runs in Hindi or Hinglish, and the terms are negotiated in Hindi before they are "
                 "redrafted in English. That gap is not a flaw — it is where the work happens, and it is "
                 "why a B2+ learner needs two things at once: the formal clause vocabulary (अनिवार्य, "
                 "उपबंध, लिखित रूप) for reading the paper, and the plain negotiation Hindi (शर्त, कब तक, "
                 "अगर ऐसा हो तो) for the table. The person who can move between the two is the one the "
                 "meeting waits for."),
        "source_url": "https://en.wikipedia.org/wiki/Contract",
    },
    "reading": {
        "text": ("आज की बैठक का विषय था: नया अनुबंध। पहले अध्यक्ष ने कार्यसूची पढ़ी — तीन विषय, एक घंटा। "
                 "शर्त के अनुसार कंपनी को हर महीने भुगतान करना होगा, और रविवार को छोड़कर डिलीवरी हर "
                 "दिन होगी। एक सदस्य ने आपत्ति की कि आँकड़े पुराने हैं। अध्यक्ष ने कहा, “मान लीजिए वे "
                 "सही हैं, फिर भी निष्कर्ष नहीं बदलता।” बात बढ़ती देखकर उन्होंने कहा कि इसे लिखित रूप "
                 "में लेंगे। अंत में तय हुआ कि संशोधन अगले सोमवार तक भेजा जाएगा, ज़िम्मेदारी मीरा की, "
                 "और कार्यवृत्त आज शाम तक सबको मिलेगा। बैठक पचास मिनट में ख़त्म हुई।"),
        "gloss": ("Today's meeting was about the new contract. First the chairman read the agenda — three "
                  "items, one hour. According to the condition, the company must pay monthly, and "
                  "deliveries will be every day except Sunday. One member objected that the figures "
                  "were old. The chairman said, “Suppose they are right; even so the conclusion does not "
                  "change.” Seeing the discussion heating up, he said they would take it up in writing. "
                  "Finally it was decided that the amendment would be sent by next Monday, the "
                  "responsibility was Meera's, and everyone would receive the minutes by this evening. "
                  "The meeting ended in fifty minutes."),
        "original": True,
    },
    "listening": {
        "script": ("— ज़रा रुकिए, यह बिंदु स्पष्ट कीजिए — उपबंध किस पर लागू होता है?\n"
                   "— दोनों पक्षों पर। पर संशोधन लिखित रूप में ही मान्य होगा।\n"
                   "— और अगर भुगतान देर से हो तो?\n"
                   "— तो नोटिस देना अनिवार्य है। यह शर्त के अनुसार है।\n"
                   "— अच्छा। और एक बात — यह सब कार्यवृत्त में लिखा जाएगा?\n"
                   "— जी, आज शाम तक भेज दिया जाएगा।"),
        "gloss": ("— Just a moment, clarify this point — to whom does the provision apply?\n— To both "
                  "parties. But an amendment will be valid only in writing.\n— And if the payment is "
                  "late?\n— Then giving notice is mandatory. That is according to the condition.\n— "
                  "Good. And one more thing — will all this be written in the minutes?\n— Yes, it will be "
                  "sent by this evening."),
        "voice_tag": VOICE,
    },
    "idioms": [
        {"t": "तारीख़ पर तारीख़", "literal": "date upon date", "meaning": "endless adjournments that never decide anything"},
        {"t": "काग़ज़ी कार्रवाई", "literal": "paperwork", "meaning": "procedure that produces files and no result"},
        {"t": "बात का बतंगड़", "literal": "a small matter made into a big dish", "meaning": "making a mountain out of a molehill"},
        {"t": "सिर झुकाकर", "literal": "with the head bowed", "meaning": "accepting humbly, without argument"},
        {"t": "मतलब निकलना", "literal": "for the purpose to come out", "meaning": "for somebody to get what they quietly wanted"},
        {"t": "हाथ-पैर मारना", "literal": "to flail hands and feet", "meaning": "to try every possible route to save something"},
        {"t": "एक ही राग अलापना", "literal": "to sing the same tune", "meaning": "to harp on one point regardless of the discussion"},
        {"t": "खुली बात", "literal": "an open matter", "meaning": "something said plainly and on the record"},
        {"t": "पानी की तरह बहना", "literal": "to flow like water", "meaning": "for money or time to drain away"},
        {"t": "रोब जमाना", "literal": "to settle one's authority down", "meaning": "to hold a room through presence rather than volume"},
    ],
    "mistakes": [
        {"wrong": "कंपनी भुगतान करेगी। (in a clause)", "right": "कंपनी को भुगतान करना होगा।",
         "why": "a contract records requirements, not predictions. करेगी is a forecast and gives a lawyer nothing to enforce."},
        {"wrong": "रविवार को छोड़कर, डिलीवरी हर दिन नहीं होगी।", "right": "रविवार को छोड़कर, डिलीवरी हर दिन होगी।",
         "why": "छोड़कर already removes the exception, so the clause stays positive. Adding a second negation flips the delivery term — the most common misreading of a schedule."},
        {"wrong": "मैंने उसको ग़लत कहा।", "right": "मैंने उसके निष्कर्ष को ग़लत कहा।",
         "why": "calling the person wrong ends the working relationship; naming the conclusion keeps the argument on the table. In Hindi the difference is just one word — निष्कर्ष."},
    ],
    "task": {
        "title": "Minute a real discussion",
        "instructions": ("Take a discussion you have had recently — at work or at home — and write its "
                         "minutes in Hindi, exactly as a professional meeting would: the agenda, two "
                         "decisions in the तय हुआ कि … form, an owner and a deadline for each, and the "
                         "one open issue recorded as लिखित रूप में लिया जाएगा. Then add a single "
                         "paragraph saying what you would have said differently in the room, and why."),
    },
}

B2P_TEST = [
    ("multiple_choice", "Choose the obligation clause.", "कंपनी को हर महीने भुगतान करना होगा।"),
    ("fill_in_the_blank", "रविवार ___ छोकर डिलीवरी हर दिन होगी। (except)", "को"),
    ("translation", "संशोधन लिखित रूप में ही मान्य होगा।", "An amendment will be valid only in writing."),
    ("reverse_translation", "Until when will the agreement be valid?", "समझौता कब तक मान्य रहेगा?"),
    ("matching", "Match उपबंध to its meaning.", "provision"),
    ("word_selection", "Select the Hindi for 'compared with last year'.", "पिछले साल के मुक़ाबले"),
    ("error_correction", "तय हुआ कि जल्दी करना चाहिए।", "तय हुआ कि प्रक्रिया सोमवार से लागू होगी; ज़िम्मेदारी राहुल की।"),
    ("dialogue_completion", "Complete: “ज़िम्मेदारी किसकी, और कब तक?” — “___”", "ज़िम्मेदारी मीरा की — बुधवार तक"),
    ("reading_comprehension", "मान लीजिए वे सही हैं, फिर भी निष्कर्ष नहीं बदलता। What is the chairman doing?", "conceding a point without giving up the conclusion"),
    ("inference", "“इसे लिखित रूप में लेंगे।” What does this prevent?", "a decision being remembered differently by each side"),
    ("main_idea", "बैठक पचास मिनट में ख़त्म हुई। What does the last sentence tell you?", "the moderation kept to the time limit"),
    ("detail_identification", "अंत में तय हुआ कि संशोधन अगले सोमवार तक भेजा जाएगा। Who is responsible?", "Meera"),
]

# ════════════════════════════════════════════════════════════════════════════
# C1+ · Almost native  —  write for work, translate, teach a beginner
# ════════════════════════════════════════════════════════════════════════════
C1P_UNITS = [
    unit("C1P-U1", "Writing for work", [
        {
            "title": "Report architecture: सारांश, निष्कर्ष, सिफ़ारिश",
            "learn": ("A Hindi report is read from the top and trusted from the bottom: सारांश (summary) "
                      "first, then विधि/आधार, निष्कर्ष (findings), सिफ़ारिश (recommendation), and "
                      "परिशिष्ट (annexure) for the evidence. The summary is written last and placed "
                      "first, and it must be readable on its own — that is the whole test of the form."),
            "vocab": [V("सारांश", "sārāṅś", "summary", "noun"), V("निष्कर्ष", "niṣkarṣ", "finding / conclusion", "noun"),
                      V("सिफ़ारिश", "sifāriś", "recommendation", "noun"), V("परिशिष्ट", "pariśiṣṭ", "annexure", "noun"),
                      V("विधि", "vidhi", "method", "noun"), V("आधार", "ādhār", "basis", "noun"),
                      V("प्रस्तुत करना", "prastut karnā", "to present"), V("संक्षिप्त", "saṅkṣipt", "concise")],
            "grammar": {
                "title": "Summary first, evidence last",
                "explain": ("The architecture is fixed: सारांश → आधार → निष्कर्ष → सिफ़ारिश → परिशिष्ट. "
                            "Each section opens with its own one-line statement — इस रिपोर्ट में … "
                            "(this report …), निष्कर्ष यह है कि … (the finding is that …), सिफ़ारिश है कि "
                            "… (the recommendation is that …). A report without सिफ़ारिश is a description, "
                            "not a report."),
                "pattern": "इस रिपोर्ट में … · निष्कर्ष यह है कि … · सिफ़ारिश है कि …",
                "examples": [X("इस रिपोर्ट में तीन निष्कर्ष हैं।", "is riporṭ meṅ tīn niṣkarṣ haiṅ.", "This report has three findings."),
                             X("निष्कर्ष यह है कि माँग बढ़ रही है।", "niṣkarṣ yah hai ki māṅg baṛh rahī hai.", "The finding is that demand is growing."),
                             X("सिफ़ारिश है कि पहले आधा काम शुरू किया जाए।", "sifāriś hai ki pahle ādhā kām śurū kiyā jāe.", "The recommendation is that half the work be started first.")],
                "mistakes": [{"wrong": "रिपोर्ट में सब कुछ लिखा है, आप पढ़ लीजिए।",
                              "right": "सारांश पहले पेज पर है; निष्कर्ष और सिफ़ारिश अलग-अलग दिए हैं।",
                              "why": "a report nobody can enter is a report nobody reads. The summary is a service to the reader, and at C1+ the architecture is the writing."}],
            },
            "dialogue": [
                {"sp": "प्रबंधक", "t": "रिपोर्ट कहाँ तक पहुँची?", "r": "riporṭ kahāṅ tak pahuṅcī?", "en": "How far has the report got?"},
                {"sp": "लेखक", "t": "सारांश और निष्कर्ष तैयार हैं। सिफ़ारिश बाक़ी है।", "r": "sārāṅś aur niṣkarṣ taiyār haiṅ. sifāriś bāqī hai.", "en": "The summary and findings are ready. The recommendation is left."},
                {"sp": "प्रबंधक", "t": "सिफ़ारिश के बिना रिपोर्ट अधूरी है।", "r": "sifāriś ke binā riporṭ adhūrī hai.", "en": "Without a recommendation the report is incomplete."},
                {"sp": "लेखक", "t": "सही बात है — कल तक दो सिफ़ारिशें जोड़ दूँगा।", "r": "sahī bāt hai — kal tak do sifāriśeṅ joṛ dūṅgā.", "en": "Fair point — I will add two recommendations by tomorrow."},
            ],
            "worksheet": {"title": "Report worksheet", "tasks": [
                {"instruction": "Name the five sections in order.", "items": ["summary", "basis", "findings", "recommendation", "annexure"], "key": ["सारांश, आधार, निष्कर्ष, सिफ़ारिश, परिशिष्ट"]},
                {"instruction": "Open each section with its line.", "items": ["The finding is that …", "The recommendation is that …"], "key": ["निष्कर्ष यह है कि …", "सिफ़ारिश है कि …"]},
            ]},
        },
        {
            "title": "Concise institutional prose",
            "learn": ("Institutional Hindi becomes unreadable by piling up nouns: समस्त प्रकार की "
                      "व्यवस्थाओं का यथाशीघ्र क्रियान्वयन किया जाएगा. The fix is a verb, a subject and "
                      "fewer words: जल्दी लागू किया जाएगा. C1+ writing is judged on what has been "
                      "removed — यथाशीघ्र, समस्त, प्रकार की, संबंधी are the usual four to cut."),
            "vocab": [V("यथाशीघ्र", "yathāśīghra", "as soon as possible (legalese)"), V("समस्त", "samast", "all / entire (legalese)"),
                      V("अनावश्यक", "anāvaśyak", "unnecessary"), V("क्रियान्वयन", "kriyānvayan", "implementation", "noun"),
                      V("संबंधी", "sambandhī", "relating to (overused)"), V("जल्दी", "jaldī", "soon / quickly"),
                      V("लागू करना", "lāgū karnā", "to implement / apply"), V("संक्षिप्त कीजिए", "saṅkṣipt kījie", "please shorten")],
            "grammar": {
                "title": "Cut the noun pile, restore the verb",
                "explain": ("Legalese stacks nouns and hides the verb at the end: व्यवस्थाओं का "
                            "क्रियान्वयन किया जाएगा. Concise institutional Hindi puts the verb in plain "
                            "sight and keeps the noun count low: जल्दी लागू किया जाएगा. The passive "
                            "किया जाएगा is still right for an impersonal order — what changes is the "
                            "weight in front of it, not the grammar."),
                "pattern": "… किया जाएगा · … जल्दी लागू होगा · संक्षिप्त कीजिए",
                "examples": [X("यह प्रक्रिया जल्दी लागू की जाएगी।", "yah prakriyā jaldī lāgū kī jāegī.", "This procedure will be implemented soon."),
                             X("अनावश्यक शब्द हटा दीजिए।", "anāvaśyak śabd haṭā dījie.", "Remove the unnecessary words."),
                             X("संक्षिप्त कीजिए — पाठक को समय चाहिए।", "saṅkṣipt kījie — pāṭhak ko samay cāhie.", "Shorten it — the reader needs time.")],
                "mistakes": [{"wrong": "समस्त प्रकार की व्यवस्थाओं का यथाशीघ्र क्रियान्वयन किया जाएगा।",
                              "right": "यह प्रक्रिया जल्दी लागू की जाएगी।",
                              "why": "समस्त, प्रकार की and यथाशीघ्र add no information and cost the reader a sentence. In institutional Hindi the shorter sentence is not less official — it is more enforceable."}],
            },
            "dialogue": [
                {"sp": "संपादक", "t": "यह वाक्य बहुत भारी है।", "r": "yah vākya bahut bhārī hai.", "en": "This sentence is very heavy."},
                {"sp": "लेखक", "t": "सही है — चार शब्द हटा दूँ?", "r": "sahī hai — cār śabd haṭā dūṅ?", "en": "True — shall I remove four words?"},
                {"sp": "संपादक", "t": "पूरा वाक्य फिर से लिखिए — क्रिया सामने रखिए।", "r": "pūrā vākya phir se likhie — kriyā sāmne rakhiye.", "en": "Rewrite the whole sentence — put the verb in front."},
                {"sp": "लेखक", "t": "“यह प्रक्रिया जल्दी लागू की जाएगी।” — अब ठीक है?", "r": "“yah prakriyā jaldī lāgū kī jāegī.” — ab ṭhīk hai?", "en": "“This procedure will be implemented soon.” — is that better?"},
            ],
            "worksheet": {"title": "Concision worksheet", "tasks": [
                {"instruction": "Rewrite without the noun pile.", "items": ["समस्त प्रकार की व्यवस्थाओं का यथाशीघ्र क्रियान्वयन किया जाएगा।"], "key": ["यह प्रक्रिया जल्दी लागू की जाएगी।"]},
                {"instruction": "Cut the four usual words.", "items": ["यथाशीघ्र", "समस्त", "प्रकार की", "संबंधी"], "key": ["जल्दी / सब / (delete) / (delete)"]},
            ]},
        },
        {
            "title": "Editing someone else's draft",
            "learn": ("Editing in Hindi is a protocol as much as a skill: पहले पढ़ लीजिए, फिर बदलिए "
                      "(read first, then change), सुझाव दीजिए, आदेश नहीं (suggest, do not order), and "
                      "मूल भाव बना रहे (the original sense must survive). Say what a change buys: बदलाव "
                      "से अर्थ साफ़ होगा."),
            "vocab": [V("संपादन", "sampādan", "editing", "noun"), V("सुझाव", "sujhāv", "suggestion", "noun"),
                      V("मूल भाव", "mūl bhāv", "the original sense", "noun"), V("संतुलन", "santulan", "balance", "noun"),
                      V("भाषा-शैली", "bhāṣā-śailī", "language and style", "noun"), V("बदलाव", "badlāv", "change", "noun"),
                      V("स्पष्टता", "spaṣṭatā", "clarity", "noun"), V("स्वर", "svar", "tone / voice", "noun")],
            "grammar": {
                "title": "सुझाव दीजिए, आदेश नहीं",
                "explain": ("Comment on a draft with suggestions, not corrections: यहाँ बदलाव से अर्थ "
                            "साफ़ होगा (a change here will make the meaning clear), शायद यह वाक्य छोटा "
                            "किया जा सके (this sentence could perhaps be shortened). मूल भाव बना रहे is "
                            "the constraint that governs every suggestion, and स्वर (tone) is what an "
                            "edit most easily damages."),
                "pattern": "यहाँ बदलाव से … होगा · शायद … किया जा सके · मूल भाव बना रहे",
                "examples": [X("यहाँ बदलाव से अर्थ साफ़ होगा।", "yahāṅ badlāv se arth sāf hogā.", "A change here will make the meaning clear."),
                             X("शायद यह वाक्य छोटा किया जा सके।", "śāyad yah vākya chhoṭā kiyā jā sake.", "Perhaps this sentence could be shortened."),
                             X("मूल भाव बना रहे — स्वर न बदले।", "mūl bhāv banā rahe — svar na badle.", "Let the original sense survive — do not change the tone.")],
                "mistakes": [{"wrong": "यह वाक्य ग़लत है, ऐसे लिखिए।",
                              "right": "यहाँ बदलाव से अर्थ साफ़ होगा — ऐसा लिखें तो?",
                              "why": "यह ग़लत है comments on the writer; the suggestion form comments on the sentence. In an editorial round the difference decides whether the writer can receive the note."}],
            },
            "dialogue": [
                {"sp": "लेखक", "t": "यह मेरा ड्राफ़्ट है। ज़रा देखिए।", "r": "yah merā ḍrāfṭ hai. zarā dekhie.", "en": "This is my draft. Have a look."},
                {"sp": "संपादक", "t": "पढ़ लिया। एक जगह बदलाव से अर्थ साफ़ होगा।", "r": "paṛh liyā. ek jagah badlāv se arth sāf hogā.", "en": "I have read it. In one place a change will make the meaning clear."},
                {"sp": "लेखक", "t": "कहाँ? और क्या बदले?", "r": "kahāṅ? aur kyā badle?", "en": "Where? And what should change?"},
                {"sp": "संपादक", "t": "दूसरा वाक्य छोटा कीजिए — मूल भाव बना रहे, बस स्वर हल्का हो जाए।", "r": "dūsrā vākya chhoṭā kījie — mūl bhāv banā rahe, bas svar halkā ho jāe.", "en": "Shorten the second sentence — let the sense survive, only let the tone lighten."},
            ],
            "worksheet": {"title": "Editing worksheet", "tasks": [
                {"instruction": "Turn a correction into a suggestion.", "items": ["यह वाक्य ग़लत है।", "यह बहुत लंबा है।"], "key": ["यहाँ बदलाव से अर्थ साफ़ होगा।", "शायद यह वाक्य छोटा किया जा सके।"]},
                {"instruction": "State the constraint.", "items": ["do not change the tone"], "key": ["मूल भाव बना रहे — स्वर न बदले।"]},
            ]},
        },
    ]),
    unit("C1P-U2", "Translating between Hindi and English", [
        {
            "title": "Register matching, not word matching",
            "learn": ("Translation chooses a register and keeps it. तत्सम words (आवश्यकता, सूचना, धन्यवाद) "
                      "sit in formal text; तद्भव words (ज़रूरत, ख़बर, शुक्रिया) sit in speech. Putting one "
                      "in the other's place is what makes a translation sound like a dictionary: the "
                      "English is right word by word and wrong in the room."),
            "vocab": [V("कार्यालयीन", "kāryālayīn", "official / office register"), V("बोलचाल", "bolcāl", "colloquial speech", "noun"),
                      V("तत्सम", "tatsam", "Sanskrit-derived (formal layer)"), V("तद्भव", "tadbhav", "Sanskrit-derived (evolved layer)"),
                      V("अनुवाद", "anuvād", "translation", "noun"), V("मूल", "mūl", "original / source", "noun"),
                      V("लक्ष्य भाषा", "lakṣya bhāṣā", "target language", "noun"), V("शैली", "śailī", "style", "noun")],
            "grammar": {
                "title": "One register, kept to the end",
                "explain": ("The translator reads the source for its register first, then picks the Hindi "
                            "layer and stays there — a नोटिस uses आवश्यकता and सूचित, a WhatsApp message "
                            "uses ज़रूरत and बता देना. Mixed registers inside one paragraph are what "
                            "reveal a translation; the grammar can be perfect and the text still reads "
                            "wrong."),
                "pattern": "formal source → तत्सम layer · conversational source → तद्भव layer",
                "examples": [X("Notice: “You are required to submit the form.” → फ़ॉर्म जमा करना आवश्यक है।", "fŏrm jamā karnā āvaśyak hai.", "the formal layer"),
                             X("Message: “You need to send it.” → यह भेज दीजिए, ज़रूरत है।", "yah bhej dījie, zarūrat hai.", "the conversational layer"),
                             X("दोनों सही हैं — पर एक ही अनुच्छेद में नहीं।", "donoṅ sahī haiṅ — par ek hī anucched meṅ nahīṅ.", "both are right — but not in the same paragraph")],
                "mistakes": [{"wrong": "फ़ॉर्म जमा करना ज़रूरत है। / यह भेज दीजिए, आवश्यकता है।",
                              "right": "फ़ॉर्म जमा करना आवश्यक है। / यह भेज दीजिए, ज़रूरत है।",
                              "why": "ज़रूरत is a noun people use with है in speech; आवश्यकता belongs to written formal Hindi. Both pairings above are grammatical and each is wrong for its register."}],
            },
            "dialogue": [
                {"sp": "संपादक", "t": "यह अनुवाद कैसा है?", "r": "yah anuvād kaisā hai?", "en": "How is this translation?"},
                {"sp": "अनुवादक", "t": "शब्द सही हैं, पर शैली मिली हुई है।", "r": "śabd sahī haiṅ, par śailī milī huī hai.", "en": "The words are right, but the register is mixed."},
                {"sp": "संपादक", "t": "मतलब?", "r": "matlab?", "en": "Meaning?"},
                {"sp": "अनुवादक", "t": "पहला वाक्य कार्यालयीन है, दूसरा बोलचाल का — दोनों को एक परत में लाना होगा।", "r": "pahlā vākya kāryālayīn hai, dūsrā bolcāl kā — donoṅ ko ek parat meṅ lānā hogā.", "en": "The first sentence is official, the second colloquial — both have to be brought to one layer."},
            ],
            "worksheet": {"title": "Register worksheet", "tasks": [
                {"instruction": "Choose the layer and stay there.", "items": ["Notice: I need the form.", "Message: I need the form."], "key": ["फ़ॉर्म आवश्यक है।", "फ़ॉर्म चाहिए।"]},
                {"instruction": "Name the layers.", "items": ["formal", "colloquial"], "key": ["कार्यालयीन (तत्सम)", "बोलचाल (तद्भव)"]},
            ]},
        },
        {
            "title": "Idioms, false friends and what not to translate",
            "learn": ("Idioms move by sense, not by word: मुँह में पानी आना is 'to make one's mouth "
                      "water', and word-for-word it is nonsense in English. False friends are quieter "
                      "and more dangerous: नुक़सान is loss, not nuisance; मतलब is meaning, not motive; "
                      "आराम is rest, not comfort as furniture."),
            "vocab": [V("मुहावरा", "muhāvarā", "idiom", "noun"), V("शब्दशः", "śabdaśaḥ", "literally / word for word"),
                      V("भाव", "bhāv", "sense / meaning", "noun"), V("झूठा मित्र", "jhūṭhā mitra", "false friend", "noun"),
                      V("नुक़सान", "nuqsān", "loss / damage", "noun"), V("मतलब", "matlab", "meaning", "noun"),
                      V("आराम", "ārām", "rest", "noun"), V("संदर्भ", "sandarbh", "context", "noun")],
            "grammar": {
                "title": "Translate the भाव, not the शब्द",
                "explain": ("An idiom is replaced by the target language's idiom, or by its plain sense "
                            "if there is none: मुँह में पानी आना → to make one's mouth water. शब्दशः "
                            "translation is kept only for glosses, never for the text itself. False "
                            "friends are checked in संदर्भ (context) rather than in a dictionary, because "
                            "a dictionary gives the commonest sense, not the sense in front of you."),
                "pattern": "idiom → target idiom · no target idiom → plain sense · check false friends in context",
                "examples": [X("उसका खाना देखकर मुँह में पानी आ गया।", "uskā khānā dekhkar muṅh meṅ pānī ā gayā.", "Seeing his food, my mouth watered."),
                             X("यहाँ “नुक़सान” का मतलब घाटा है, nuisance नहीं।", "yahāṅ “nuqsān” kā matlab ghāṭā hai, nuisance nahīṅ.", "Here नुक़सान means loss, not nuisance."),
                             X("मुहावरे को शब्दशः मत लीजिए।", "muhāvare ko śabdaśaḥ mat lījie.", "Do not translate an idiom word for word.")],
                "mistakes": [{"wrong": "“मेरा मतलब साफ़ है” → “My motive is clean.”",
                              "right": "“मेरा मतलब साफ़ है” → “What I mean is clear.”",
                              "why": "मतलब is meaning; motive is नीयत or इरादा. This is the classic false friend, and it is dangerous because both sentences are fluent English."}],
            },
            "dialogue": [
                {"sp": "अनुवादक", "t": "यह मुहावरा अँग्रेज़ी में नहीं है।", "r": "yah muhāvarā aṅgrezī meṅ nahīṅ hai.", "en": "This idiom does not exist in English."},
                {"sp": "संपादक", "t": "तो क्या करें?", "r": "to kyā kareṅ?", "en": "So what do we do?"},
                {"sp": "अनुवादक", "t": "भाव ले लें — शब्द नहीं। “मुँह में पानी आना” → “to make one's mouth water”।", "r": "bhāv le leṅ — śabd nahīṅ.", "en": "Take the sense, not the words."},
                {"sp": "संपादक", "t": "और दूसरी जगह?", "r": "aur dūsrī jagah?", "en": "And the other place?"},
                {"sp": "अनुवादक", "t": "वहाँ “मतलब” का अनुवाद “motive” नहीं होगा — संदर्भ में वह meaning है।", "r": "vahāṅ “matlab” kā anuvād “motive” nahīṅ hogā — sandarbh meṅ vah meaning hai.", "en": "There मतलब will not be “motive” — in context it means meaning."},
            ],
            "worksheet": {"title": "Idiom worksheet", "tasks": [
                {"instruction": "Translate the sense, not the words.", "items": ["मुँह में पानी आना", "आँखों का तारा"], "key": ["to make one's mouth water", "the apple of someone's eye"]},
                {"instruction": "Catch the false friend.", "items": ["मेरा मतलब साफ़ है", "इसमें नुक़सान हुआ"], "key": ["What I mean is clear. (not motive)", "There was a loss. (not nuisance)"]},
            ]},
        },
        {
            "title": "Back-translation as a check",
            "learn": ("The professional check is back-translation: पहले अनुवाद, फिर पुनःअनुवाद (translate, "
                      "then translate back), and compare the two Hindi texts. Where they diverge, the "
                      "first translation has either added or dropped something — यहाँ कुछ जुड़ गया (here "
                      "something has been added), यहाँ अर्थ घट गया (here the meaning has shrunk)."),
            "vocab": [V("पुनःअनुवाद", "punaḥ-anuvād", "back-translation", "noun"), V("बारीक़ी", "bārīqī", "fine detail", "noun"),
                      V("जुड़ना", "juṛnā", "to get added"), V("घटना", "ghaṭnā", "to decrease / shrink"),
                      V("तुलना", "tulnā", "comparison", "noun"), V("दोहराना", "dohrānā", "to repeat"),
                      V("सुधार", "sudhār", "correction / improvement", "noun"), V("जाँच", "jāṅc", "check", "noun")],
            "grammar": {
                "title": "अनुवाद → पुनःअनुवाद → तुलना",
                "explain": ("The method is mechanical, which is why it works: translate into Hindi, "
                            "translate that Hindi back into English without looking at the source, then "
                            "compare the two English texts. Extra information means the first pass "
                            "explained too much (बारीक़ी जुड़ गई); lost information means it smoothed "
                            "something over (अर्थ घट गया) — and smoothing is the commoner fault."),
                "pattern": "अनुवाद → पुनःअनुवाद → दोनों की तुलना",
                "examples": [X("यहाँ कुछ जुड़ गया — मूल में यह बात नहीं है।", "yahāṅ kuchh juṛ gayā — mūl meṅ yah bāt nahīṅ hai.", "Something has been added here — this is not in the original."),
                             X("यहाँ अर्थ घट गया — बारीक़ी छूट गई।", "yahāṅ arth ghaṭ gayā — bārīqī chhūṭ gaī.", "Here the meaning has shrunk — a fine detail was lost."),
                             X("पुनःअनुवाद से जाँच आसान हो जाती है।", "punaḥ-anuvād se jāṅc āsān ho jātī hai.", "Back-translation makes checking easier.")],
                "mistakes": [{"wrong": "अनुवाद अच्छा लग रहा है, इसलिए ठीक होगा।",
                              "right": "पुनःअनुवाद करके देखिए — जो जुड़ा या घटा, वह तुरंत दिखेगा।",
                              "why": "a translation that reads smoothly is exactly the one that has quietly smoothed something away. The mechanical check catches what fluent reading hides."}],
            },
            "dialogue": [
                {"sp": "संपादक", "t": "यह अनुवाद भरोसेमंद है?", "r": "yah anuvād bharosemand hai?", "en": "Is this translation reliable?"},
                {"sp": "अनुवादक", "t": "पुनःअनुवाद कर लिया है — दो जगह अंतर मिला।", "r": "punaḥ-anuvād kar liyā hai — do jagah antar milā.", "en": "I have done the back-translation — two differences were found."},
                {"sp": "संपादक", "t": "कहाँ?", "r": "kahāṅ?", "en": "Where?"},
                {"sp": "अनुवादक", "t": "एक जगह बारीक़ी जुड़ गई, दूसरी जगह अर्थ घट गया — दोनों सुधार दिए हैं।", "r": "ek jagah bārīqī juṛ gaī, dūsrī jagah arth ghaṭ gayā — donoṅ sudhār die haiṅ.", "en": "In one place a detail was added, in another the meaning shrank — I have made both corrections."},
            ],
            "worksheet": {"title": "Back-translation worksheet", "tasks": [
                {"instruction": "Name the three steps.", "items": ["translate", "back-translate", "compare"], "key": ["अनुवाद, पुनःअनुवाद, तुलना"]},
                {"instruction": "Diagnose the fault.", "items": ["Extra information appeared.", "A detail was lost."], "key": ["यहाँ कुछ जुड़ गया।", "यहाँ अर्थ घट गया।"]},
            ]},
        },
    ]),
    unit("C1P-U3", "Teaching a beginner", [
        {
            "title": "Explaining a rule simply",
            "learn": ("Teaching is the last test of understanding. A rule is explained with one example "
                      "first, then the rule, then a second example: देखिए — मैं जाता हूँ, वह जाता है. नियम "
                      "यह है कि क्रिया कर्ता के साथ बदलती है. The beginner's question is never 'why' but "
                      "'which one do I say', so the answer is an example, not a table."),
            "vocab": [V("नियम", "niyam", "rule", "noun"), V("उदाहरण", "udāharaṇ", "example", "noun"),
                      V("आसान भाषा", "āsān bhāṣā", "plain language", "noun"), V("कर्ता", "kartā", "subject / doer", "noun"),
                      V("क्रिया", "kriyā", "verb", "noun"), V("समझाना", "samjhānā", "to explain"),
                      V("दोहराइए", "dohrāie", "please repeat"), V("अभ्यास", "abhyās", "practice", "noun")],
            "grammar": {
                "title": "Example → rule → example",
                "explain": ("The teaching order is देखिए (look) → नियम यह है कि (the rule is) → अब आप "
                            "कहिए (now you say it). Every rule is stated in one sentence with no jargon, "
                            "and the learner's first attempt is answered with दोहराइए rather than a "
                            "correction. क्रिया, कर्ता and कारक are taught only after the learner can "
                            "use the thing."),
                "pattern": "देखिए … → नियम यह है कि … → अब आप कहिए …",
                "examples": [X("देखिए — मैं जाता हूँ, वह जाता है।", "dekhie — main jātā hūṅ, vah jātā hai.", "Look — I go, he goes."),
                             X("नियम यह है कि क्रिया कर्ता के साथ बदलती है।", "niyam yah hai ki kriyā kartā ke sāth badaltī hai.", "The rule is that the verb changes with the subject."),
                             X("अब आप कहिए — “आप जाते हैं।”", "ab āp kahie — “āp jāte haiṅ.”", "Now you say it — “you go” (respectful).")],
                "mistakes": [{"wrong": "सबसे पहले कारक और विभक्ति समझिए।",
                              "right": "देखिए — यह वाक्य। अब आप ऐसा ही बनाइए।",
                              "why": "grammar terminology before usage teaches the learner to talk about the language instead of using it. Terms come after the learner has said the sentence correctly three times."}],
            },
            "dialogue": [
                {"sp": "शिक्षक", "t": "देखिए — मैं जाता हूँ। वह जाता है।", "r": "dekhie — main jātā hūṅ. vah jātā hai.", "en": "Look — I go. He goes."},
                {"sp": "शिक्षार्थी", "t": "क्यों बदलता है?", "r": "kyoṅ badaltā hai?", "en": "Why does it change?"},
                {"sp": "शिक्षक", "t": "नियम यह है कि क्रिया कर्ता के साथ बदलती है। अब आप कहिए — “हम जाते हैं।”", "r": "niyam yah hai ki kriyā kartā ke sāth badaltī hai. ab āp kahie — “ham jāte haiṅ.”", "en": "The rule is that the verb changes with the subject. Now you say it — “we go”."},
                {"sp": "शिक्षार्थी", "t": "हम जाते हैं?", "r": "ham jāte haiṅ?", "en": "We go?"},
                {"sp": "शिक्षक", "t": "बिल्कुल सही! दोहराइए — और एक उदाहरण आप बनाइए।", "r": "bilkul sahī! dohrāie — aur ek udāharaṇ āp banāie.", "en": "Exactly right! Repeat it — and make one example yourself."},
            ],
            "worksheet": {"title": "Teaching worksheet", "tasks": [
                {"instruction": "Teach one rule in the three beats.", "items": ["verb agreement"], "key": ["देखिए — मैं जाता हूँ, वह जाता है। → नियम यह है कि क्रिया कर्ता के साथ बदलती है। → अब आप कहिए।"]},
                {"instruction": "Avoid the jargon.", "items": ["कर्ता, क्रिया, विभक्ति"], "key": ["(say “who does it” and “the doing word” instead)"]},
            ]},
        },
        {
            "title": "Correcting kindly",
            "learn": ("Correction is delivered inside encouragement: बहुत अच्छा! बस एक चीज़ बदलिए (very "
                      "good! just change one thing). Say the sentence back correctly rather than naming "
                      "the mistake — कर्ता ग़लत है means nothing to a beginner, while saying the right "
                      "sentence makes them hear it. ग़लती से सीखना (learning from the error) is the "
                      "frame to give the learner."),
            "vocab": [V("सुधार", "sudhār", "correction", "noun"), V("ग़लती", "ġalatī", "mistake", "noun"),
                      V("तारीफ़", "tārīf", "praise", "noun"), V("बस एक चीज़", "bas ek cīz", "just one thing"),
                      V("दोबारा कहिए", "dobārā kahie", "say it again"), V("शाबाश", "śābāś", "well done"),
                      V("हिम्मत", "himmat", "courage", "noun"), V("आत्मविश्वास", "ātmaviśvās", "confidence", "noun")],
            "grammar": {
                "title": "प्रशंसा → सुधार → प्रशंसा",
                "explain": ("The correction sandwich is not decoration: शाबाश! … बस एक चीज़ — “आप जाते "
                            "हैं” … हाँ, अब बिल्कुल सही! The middle part repeats the correct sentence "
                            "instead of labelling the error, and it is kept to one item per turn — a "
                            "learner given four corrections stops speaking altogether."),
                "pattern": "शाबाश! · बस एक चीज़ — (correct sentence) · अब बिल्कुल सही!",
                "examples": [X("बहुत अच्छा! बस एक चीज़ — “आप जाते हैं।”", "bahut achchhā! bas ek cīz — “āp jāte haiṅ.”", "Very good! Just one thing — “you go”."),
                             X("ग़लती से ही सीखते हैं — दोबारा कहिए।", "ġalatī se hī sīkhte haiṅ — dobārā kahie.", "We learn from mistakes — say it again."),
                             X("शाबाश! अब बिल्कुल सही।", "śābāś! ab bilkul sahī.", "Well done! Now it is exactly right.")],
                "mistakes": [{"wrong": "कर्ता और क्रिया का मेल नहीं है। फिर से।",
                              "right": "बहुत अच्छा! बस एक चीज़ — “आप जाते हैं।”",
                              "why": "naming the grammatical category tells the learner what is wrong without telling them what to say. Repeating the correct sentence gives them something to copy, which is what a beginner can act on."}],
            },
            "dialogue": [
                {"sp": "शिक्षार्थी", "t": "मैं जाता है।", "r": "main jātā hai.", "en": "I go. (wrong ending)"},
                {"sp": "शिक्षक", "t": "बहुत अच्छा! बस एक चीज़ — “मैं जाता हूँ।”", "r": "bahut achchhā! bas ek cīz — “main jātā hūṅ.”", "en": "Very good! Just one thing — “I go”."},
                {"sp": "शिक्षार्थी", "t": "मैं जाता हूँ।", "r": "main jātā hūṅ.", "en": "I go."},
                {"sp": "शिक्षक", "t": "शाबाश! अब बिल्कुल सही। ग़लती से ही सीखते हैं — एक बार और।", "r": "śābāś! ab bilkul sahī. ġalatī se hī sīkhte haiṅ — ek bār aur.", "en": "Well done! Exactly right. We learn from mistakes — once more."},
            ],
            "worksheet": {"title": "Correction worksheet", "tasks": [
                {"instruction": "Correct in the sandwich.", "items": ["शिक्षार्थी: “वह जाता हूँ।”"], "key": ["बहुत अच्छा! बस एक चीज़ — “वह जाता है।” शाबाश!"]},
                {"instruction": "Give the learner the frame.", "items": ["learning from errors"], "key": ["ग़लती से ही सीखते हैं।"]},
            ]},
        },
        {
            "title": "The first lesson, and the transliteration trap",
            "learn": ("A first Hindi lesson teaches three things and no more: नमस्ते, मेरा नाम … है, and "
                      "आप कैसे हैं?. The trap is transliteration — 'namaste' hides that there is no "
                      "'t' as in English, and 'main' is not 'mine'. लिप्यंतरण (transliteration) helps "
                      "for a week and then becomes a spelling habit; देवनागरी should arrive by week two."),
            "vocab": [V("लिप्यंतरण", "lipyantaran", "transliteration", "noun"), V("देवनागरी", "devnāgrī", "Devanagari", "noun"),
                      V("ध्वनि", "dhvani", "sound", "noun"), V("उच्चारण", "uccāraṇ", "pronunciation", "noun"),
                      V("पहला पाठ", "pahlā pāṭh", "first lesson", "noun"), V("आदत", "ādat", "habit", "noun"),
                      V("अभ्यास", "abhyās", "practice", "noun"), V("धीरे-धीरे", "dhīre-dhīre", "little by little")],
            "grammar": {
                "title": "Three sentences, then the script",
                "explain": ("The first lesson's content is fixed: नमस्ते, मेरा नाम … है, आप कैसे हैं? — plus "
                            "the answer मैं ठीक हूँ. Transliteration is a bridge with a date on it: it is "
                            "used for a week and then replaced by देवनागरी, because the Roman spelling "
                            "teaches the wrong vowels (main, namaste) and the wrong consonants (the "
                            "retroflex ट/ड written as 't'/'d')."),
                "pattern": "नमस्ते · मेरा नाम … है · आप कैसे हैं? → then देवनागरी",
                "examples": [X("पहले तीन वाक्य — और कुछ नहीं।", "pahle tīn vākya — aur kuchh nahīṅ.", "First three sentences — nothing more."),
                             X("लिप्यंतरण एक हफ़्ते के लिए है, आदत के लिए नहीं।", "lipyantaran ek hafte ke lie hai, ādat ke lie nahīṅ.", "Transliteration is for a week, not for a habit."),
                             X("धीरे-धीरे देवनागरी पर आइए।", "dhīre-dhīre devnāgrī par āie.", "Move to Devanagari little by little.")],
                "mistakes": [{"wrong": "शिक्षार्थी को सिर्फ़ रोमन में लिखकर देना।",
                              "right": "पहले हफ़्ते रोमन साथ रहे, दूसरे हफ़्ते से देवनागरी मुख्य हो।",
                              "why": "Roman-only notes feel kind and set a spelling habit that has to be unlearned. Keeping the Roman as a support beside Devanagari — never instead of it — is the difference."}],
            },
            "dialogue": [
                {"sp": "शिक्षार्थी", "t": "क्या मैं रोमन में लिखूँ?", "r": "kyā main roman meṅ likhūṅ?", "en": "Should I write in Roman?"},
                {"sp": "शिक्षक", "t": "पहले हफ़्ते ठीक है — साथ में देवनागरी भी देखिए।", "r": "pahle hafte ṭhīk hai — sāth meṅ devnāgrī bhī dekhie.", "en": "For the first week that is fine — but look at the Devanagari alongside it."},
                {"sp": "शिक्षार्थी", "t": "“नमस्ते” में ‘t’ अँग्रेज़ी जैसा नहीं है?", "r": "“namaste” meṅ ‘t’ aṅgrezī jaisā nahīṅ hai?", "en": "In “namaste”, the ‘t’ is not like English?"},
                {"sp": "शिक्षक", "t": "बिल्कुल — जीभ तालू पर लगाइए। इसीलिए धीरे-धीरे देवनागरी पर आइए।", "r": "bilkul — jībh tālū par lagāie. islie dhīre-dhīre devnāgrī par āie.", "en": "Exactly — put the tongue on the roof of the mouth. That is why we move to Devanagari slowly."},
            ],
            "worksheet": {"title": "First lesson worksheet", "tasks": [
                {"instruction": "Teach the three first sentences.", "items": ["hello", "my name is …", "how are you?"], "key": ["नमस्ते।", "मेरा नाम … है।", "आप कैसे हैं?"]},
                {"instruction": "Explain the transliteration trap.", "items": ["why 'namaste' misleads"], "key": ["‘t’ अँग्रेज़ी का नहीं, ट/त का है — इसलिए देवनागरी ज़रूरी है।"]},
            ]},
        },
    ]),
]

C1P_EXTRA = {
    "culture": {
        "text": ("Translation between Hindi and English has a direction problem. English into Hindi "
                 "needs a register decision the source does not make for you — the same English "
                 "sentence is आवश्यकता in a notice and ज़रूरत in a message. Hindi into English needs the "
                 "opposite: the translator has to un-colloquialise, because spoken Hindi carries warmth "
                 "(जी, अच्छा, ज़रा) that English flatly refuses to render, and losing it makes a warm "
                 "speaker sound curt. Both directions are judged by the same test — whether the reader "
                 "of the target text has the experience the reader of the source text had. That is why "
                 "back-translation is taught here as a habit rather than a proofreading step."),
        "source_url": "https://en.wikipedia.org/wiki/Translation",
    },
    "reading": {
        "text": ("पिछले महीने मुझे एक सरकारी सूचना का अनुवाद करना पड़ा। सूचना में लिखा था: “समस्त "
                 "आवेदकों को यथाशीघ्र आवश्यक दस्तावेज़ प्रस्तुत करने होंगे।” शब्दशः अनुवाद आसान था, पर "
                 "वह किसी काम का नहीं था — अँग्रेज़ी पढ़ने वाले को वह वाक्य भारी लगता। पहले मैंने शैली "
                 "चुनी: यह सूचना है, इसलिए कार्यालयीन परत। फिर मैंने लिखा: “All applicants must submit "
                 "the required documents as soon as possible.” इसके बाद पुनःअनुवाद किया, और दो जगह "
                 "अंतर मिला — एक जगह मैंने “ज़रूरी” जोड़ दिया था जो मूल में नहीं था। दूसरी जगह "
                 "“समस्त” छूट गया था, जिससे अर्थ घट गया। दोनों सुधारकर मैंने फिर से लिखा। अब वह "
                 "अनुवाद भरोसेमंद था, क्योंकि वह मूल जैसा व्यवहार करता था।"),
        "gloss": ("Last month I had to translate a government notice. The notice said: “All applicants "
                  "must submit the required documents as soon as possible.” A word-for-word translation "
                  "was easy, but it was of no use — the English reader would find that sentence heavy. "
                  "First I chose the register: this is a notice, so the official layer. Then I wrote: "
                  "“All applicants must submit the required documents as soon as possible.” After that "
                  "I back-translated, and found two differences — in one place I had added “necessary” "
                  "which was not in the source. In the other, “all” had been dropped, which shrank the "
                  "meaning. I corrected both and wrote it again. Now the translation was reliable, "
                  "because it behaved like the original."),
        "original": True,
    },
    "listening": {
        "script": ("— यह रिपोर्ट पढ़ने लायक है?\n"
                   "— सारांश ठीक है, पर सिफ़ारिश नहीं है।\n"
                   "— तो वह रिपोर्ट नहीं, विवरण है।\n"
                   "— सही कहा। और शुरू के दो पैराग्राफ़ बहुत भारी हैं — “समस्त प्रकार की व्यवस्थाओं "
                   "का यथाशीघ्र क्रियान्वयन” जैसी भाषा।\n"
                   "— उसे छोटा कीजिए: “यह प्रक्रिया जल्दी लागू की जाएगी।”\n"
                   "— मूल भाव बना रहेगा?\n"
                   "— बना रहेगा — और पाठक पहले पैराग्राफ़ से ही समझ जाएगा।"),
        "gloss": ("— Is this report worth reading?\n— The summary is fine, but there is no "
                  "recommendation.\n— Then it is not a report, it is a description.\n— Well said. And "
                  "the first two paragraphs are very heavy — language like “implementation of all "
                  "kinds of arrangements at the earliest”.\n— Shorten it: “This procedure will be "
                  "implemented soon.”\n— Will the original sense survive?\n— It will — and the reader "
                  "will understand from the first paragraph itself."),
        "voice_tag": VOICE,
    },
    "idioms": [
        {"t": "नौबत आना", "literal": "for the turn to come", "meaning": "for matters to reach that pass — usually said of a bad point"},
        {"t": "कान खड़े होना", "literal": "for the ears to stand up", "meaning": "to become alert, to prick up one's ears"},
        {"t": "बोलती बंद होना", "literal": "for one's speech to close", "meaning": "to be silenced completely"},
        {"t": "दो कौड़ी का", "literal": "worth two cowries", "meaning": "of almost no value — said of a cheap thing or a cheap person"},
        {"t": "दिल की बात", "literal": "the matter of the heart", "meaning": "what one really wanted to say"},
        {"t": "ठगा-सा रह जाना", "literal": "to be left as if robbed", "meaning": "to be stunned into stillness"},
        {"t": "मुँह न चुराना", "literal": "not to turn the face away", "meaning": "to face up to something rather than avoid it"},
        {"t": "दम न लेना", "literal": "not to take breath", "meaning": "to work without pause; relentless"},
        {"t": "हाथ लगाना", "literal": "to put a hand to", "meaning": "to touch — and, jokingly, to acquire"},
        {"t": "सिर उठाना", "literal": "to raise one's head", "meaning": "to emerge, or to push back against pressure"},
    ],
    "mistakes": [
        {"wrong": "“मेरा मतलब साफ़ है” → “My motive is clear.”", "right": "“मेरा मतलब साफ़ है” → “What I mean is clear.”",
         "why": "मतलब is meaning; नीयत or इरादा is motive. The false friend is dangerous because the wrong sentence is perfectly fluent English."},
        {"wrong": "फ़ॉर्म जमा करना ज़रूरत है।", "right": "फ़ॉर्म जमा करना आवश्यक है।",
         "why": "ज़रूरत belongs to speech, आवश्यकता/आवश्यक to written official Hindi. The sentence is grammatical and still wrong — a register error, which is what C1+ is examined on."},
        {"wrong": "रिपोर्ट में सब कुछ है। (no summary, no recommendation)", "right": "सारांश और सिफ़ारिश अलग से दीजिए।",
         "why": "a report that requires reading from the start to find anything is a description. The summary and the recommendation are the parts that make it usable."},
    ],
    "task": {
        "title": "Translate, back-translate, then teach it",
        "instructions": ("Take one paragraph of English — a notice, an email, a news paragraph — and do "
                         "three things with it in Hindi: translate it choosing one register and staying "
                         "in it; back-translate it without looking at the source and list every place "
                         "the two differ, saying whether something was added or lost; then write four "
                         "lines explaining to a beginner, in plain Hindi, the one rule your translation "
                         "had to get right. The third step is the real test — if you cannot explain it "
                         "simply, you made the choice by ear."),
    },
}

C1P_TEST = [
    ("multiple_choice", "Which opening belongs in a report's summary?", "इस रिपोर्ट में तीन निष्कर्ष हैं।"),
    ("fill_in_the_blank", "सिफ़ारिश है ___ पहले आधा काम शुरू किया जाए। (that)", "कि"),
    ("translation", "संशोधन लिखित रूप में ही मान्य होगा।", "An amendment will be valid only in writing."),
    ("reverse_translation", "This procedure will be implemented soon.", "यह प्रक्रिया जल्दी लागू की जाएगी।"),
    ("matching", "Match सारांश to its meaning.", "summary"),
    ("word_selection", "Select the Hindi for 'back-translation'.", "पुनःअनुवाद"),
    ("error_correction", "फ़ॉर्म जमा करना ज़रूरत है। (in an official notice)", "फ़ॉर्म जमा करना आवश्यक है।"),
    ("dialogue_completion", "Complete: “रिपोर्ट कहाँ तक पहुँची?” — “सारांश तैयार है, ___ बाक़ी है।”", "सिफ़ारिश"),
    ("reading_comprehension", "शब्दशः अनुवाद आसान था, पर वह किसी काम का नहीं था। Why not?", "it read heavily and did not behave like the original"),
    ("inference", "“पुनःअनुवाद करके देखिए।” What is the speaker guarding against?", "a translation that reads smoothly while dropping or adding meaning"),
    ("main_idea", "देखिए — मैं जाता हूँ। नियम यह है कि क्रिया कर्ता के साथ बदलती है। अब आप कहिए। What is this an example of?", "teaching a rule through examples before naming it"),
    ("detail_identification", "एक जगह बारीक़ी जुड़ गई, दूसरी जगह अर्थ घट गया। What were the two faults?", "an addition and a loss"),
]


LEVELS = {
    "A2+": {"title": "Holding a chat", "goals": [
        "Keep a conversation going with reactions and follow-up questions",
        "Tell a short story with sequence words and the past continuous",
        "Invite, accept, decline and handle the phone",
    ], "units": A2P_UNITS, "extra": A2P_EXTRA, "test": A2P_TEST},
    "B1+": {"title": "Comfortable", "goals": [
        "Ask for things and report progress at work",
        "Give reasons, add points and disagree politely",
        "Handle institutional Hindi: forms, official verbs, clarifications",
    ], "units": B1P_UNITS, "extra": B1P_EXTRA, "test": B1P_TEST},
    "B2+": {"title": "Professional", "goals": [
        "Open, moderate and minute a meeting, with decisions that carry owners and dates",
        "Read obligations, exceptions and scope out of a contract",
        "Assert with evidence, concede narrowly and de-escalate to writing",
    ], "units": B2P_UNITS, "extra": B2P_EXTRA, "test": B2P_TEST},
    "C1+": {"title": "Almost native", "goals": [
        "Architect a work report and cut institutional Hindi down to what it needs",
        "Translate with a register, handle idioms and false friends, and check by back-translation",
        "Teach a beginner a rule, correct kindly, and start from Devanagari rather than Roman",
    ], "units": C1P_UNITS, "extra": C1P_EXTRA, "test": C1P_TEST},
}

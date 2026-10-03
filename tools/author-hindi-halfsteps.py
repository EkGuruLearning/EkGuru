# -*- coding: utf-8 -*-
"""Hindi PHASE 1 — the half-step rungs (A1+ A2+ B1+ B2+ C1+).

`tools/language-gate.py` counts eleven rungs (RUNGS): the six CEFR levels plus
the half-step after each of the first five. `data/levels.json` names them the way
language schools do — A1+ is a recognised label — and each CEFR page already
describes its own half-step in the "After A1: the A1+ checkpoint" section.

What was missing was the data: every published course carried six files. This
tool authors Hindi's, starting with A1+ ("Getting around": ask for things, give
a phone number, name the days). A rung file is a real level, not a page stub —
the course player fetches `data/courses/<phase>/<code>_<level>.json` by name
(js/course-player.js: fetchLevel), so authoring the file makes A1+ playable at
/courses/#/hi/A1+ while the static level pages stay the six CEFR ones.

Each rung file carries the same shape the schema requires of a CEFR level:
three units of three lessons, a ten-item test, and the `extra` block.

Run:  python3 tools/author-hindi-halfsteps.py           write
      python3 tools/author-hindi-halfsteps.py --check   report drift
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VOICE = "hi-IN"
SRS_POLICY = ("Only these four high-value terms are preselected; lesson mistakes and productive "
              "patterns may enter personalized review after an actual error.")


def V(t, r, en, pos="phrase"):
    return {"t": t, "r": r, "en": en, "pos": pos}


def X(t, r, en):
    return {"t": t, "r": r, "en": en}


def practice_items(spec: dict) -> list:
    """The twelve exercise types, built from the lesson's own content — the same
    walk the existing lessons take (newest-first ordering of the same twelve)."""
    title, vocab, gram = spec["title"], spec["vocab"], spec["grammar"]
    ex, dlg = gram["examples"], spec["dialogue"]
    meanings = [v["en"] for v in vocab]
    opts4 = lambda m: [m] + [x for x in meanings if x != m][:3]
    opts3 = lambda m: [m] + [x for x in meanings if x != m][:2]
    items = [
        ("multiple_choice", "Practice 1: [multiple choice] %s — Choose the meaning of %s (%s) in this lesson."
         % (title, vocab[0]["t"], vocab[0]["r"]), vocab[0]["en"], opts4(vocab[0]["en"])),
        ("fill_in_the_blank", "Practice 2: [fill in the blank] %s — Type the Hindi expression meaning “%s”."
         % (title, vocab[1]["en"]), vocab[1]["t"], None),
        ("translation", "Practice 3: [translation] %s — Interpret the Devanagari in context: %s (%s)."
         % (title, ex[0]["t"], ex[0]["r"]), ex[0]["en"], None),
        ("reverse_translation", "Practice 4: [reverse translation] %s — Write in Devanagari: %s."
         % (title, ex[1]["en"]), ex[1]["t"], None),
        ("matching", "Practice 5: [matching] %s — Match %s to its lesson meaning." % (title, vocab[2]["t"]),
         vocab[2]["en"], opts3(vocab[2]["en"])),
        ("reorder", "Practice 6: [reorder] %s — Reconstruct the lesson model in coherent Hindi: %s."
         % (title, ex[2]["en"]), ex[2]["t"], None),
        ("sentence_building", "Practice 7: [sentence building] %s — Build the sentence with the lesson pattern (%s): %s."
         % (title, gram["pattern"], ex[0]["en"]), ex[0]["t"], None),
        ("word_selection", "Practice 8: [word selection] %s — Select the Hindi form for “%s”."
         % (title, vocab[3]["en"]), vocab[3]["t"], [vocab[3]["t"]] + [v["t"] for v in vocab[4:]][:2]),
        ("error_correction", "Practice 9: [error correction] %s — Correct the model the lesson warns about: %s"
         % (title, gram["mistakes"][0]["wrong"]), gram["mistakes"][0]["right"], None),
        ("dialogue_completion", "Practice 10: [dialogue completion] %s — Complete the exchange with the studied response to: %s"
         % (title, dlg[0]["en"]), dlg[1]["t"], None),
        ("reading_comprehension", "Practice 11: [reading comprehension] %s — Read “%s” (%s). What does it mean?"
         % (title, dlg[2]["t"], dlg[2]["r"]), dlg[2]["en"], None),
        ("paragraph_comprehension", "Practice 12: [paragraph comprehension] %s — Read the lesson dialogue as a whole and give its key move: %s"
         % (title, dlg[3]["en"]), dlg[3]["t"], None),
    ]
    out = []
    for kind, q, answer, options in items:
        item = {"type": kind, "q": q, "answer": answer, "skill_target": kind.replace("_", " ")}
        if options:
            item["options"] = options
        out.append(item)
    return out


def quiz_items(spec: dict) -> list:
    vocab = spec["vocab"]
    meanings = [v["en"] for v in vocab]
    out = []
    for v in vocab[:5]:
        out.append({"q": "Which meaning best fits %s?" % v["t"],
                    "options": [v["en"]] + [m for m in meanings if m != v["en"]][:3], "answer": 0,
                    "why": "%s (%s) means %s in this lesson." % (v["t"], v["r"], v["en"])})
    return out


def worksheet(spec: dict) -> dict:
    tasks = list(spec["worksheet"]["tasks"])
    tasks.append({"instruction": ("Integrated offline practice: read the first model, transform or extend it in "
                                  "Devanagari, then rehearse it as a dialogue. Self-check meaning, grammar, and register."),
                  "items": [spec["grammar"]["examples"][0]["t"], spec["dialogue"][0]["t"]],
                  "key": [spec["grammar"]["examples"][0]["en"], spec["dialogue"][0]["en"]]})
    return {"title": spec["worksheet"]["title"], "tasks": tasks}


def unit(uid, title, lessons):
    return {"id": uid, "title": title, "lessons": lessons}


def lesson(uid, n, spec):
    built = {
        "id": "%s-L%d" % (uid, n),
        "title": spec["title"],
        "learn": spec["learn"],
        "vocab": spec["vocab"],
        "grammar": spec["grammar"],
        "dialogue": spec["dialogue"],
        "practice": practice_items(spec),
        "quiz": quiz_items(spec),
        "flashcards": "auto:vocab",
        "worksheet": worksheet(spec),
        "srs_candidates": [v["t"] for v in spec["vocab"][:4]],
        "srs_policy": SRS_POLICY,
    }
    return built


# ── A1+ ─────────────────────────────────────────────────────────────────────
A1P_UNITS = [
    unit("A1P-U1", "Getting around town", [
        lesson("A1P-U1", 1, {
            "title": "Directions: सीधे, बाएँ, दाएँ",
            "learn": ("Directions are all polite imperatives, so they end in -इए: सीधे जाइए (go "
                      "straight), बाएँ मुड़िए (turn left), दाएँ मुड़िए (turn right). Landmarks carry "
                      "their own postpositions: सामने (in front), पीछे (behind), पास (near), दूर "
                      "(far) — and each one follows the noun it describes."),
            "vocab": [V("सीधे", "sīdhe", "straight"), V("बाएँ", "bāeṅ", "left"),
                      V("दाएँ", "dāeṅ", "right"), V("मुड़िए", "muṛie", "please turn"),
                      V("सामने", "sāmne", "in front of"), V("पीछे", "pīchhe", "behind"),
                      V("पास", "pās", "near"), V("दूर", "dūr", "far")],
            "grammar": {
                "title": "Route instructions in -इए",
                "explain": ("Every step of a route is a polite imperative: पहले सीधे जाइए, फिर बाएँ "
                            "मुड़िए, फिर दाएँ. The landmark comes before its postposition: बैंक के "
                            "सामने (in front of the bank), स्टेशन के पास (near the station)."),
                "pattern": "सीधे जाइए · बाएँ/दाएँ मुड़िए · X के सामने/पीछे/पास",
                "examples": [X("सीधे जाइए, फिर बाएँ मुड़िए।", "sīdhe jāie, phir bāeṅ muṛie.", "Go straight, then turn left."),
                             X("बैंक बाज़ार के सामने है।", "baiṅk bāzār ke sāmne hai.", "The bank is in front of the market."),
                             X("स्टेशन यहाँ से दूर नहीं है।", "sṭeśan yahāṅ se dūr nahīṅ hai.", "The station is not far from here.")],
                "mistakes": [{"wrong": "सीधे जाओ, बाएँ मुड़ो। (to a stranger)",
                              "right": "सीधे जाइए, बाएँ मुड़िए।",
                              "why": "directions to a stranger take the -इए form. जाओ/मुड़ो are for people you call तुम."}],
            },
            "dialogue": [
                {"sp": "यात्री", "t": "माफ़ कीजिए, बाज़ार कहाँ है?", "r": "māf kījie, bāzār kahāṅ hai?", "en": "Excuse me, where is the market?"},
                {"sp": "स्थानीय", "t": "सीधे जाइए, फिर बाएँ मुड़िए।", "r": "sīdhe jāie, phir bāeṅ muṛie.", "en": "Go straight, then turn left."},
                {"sp": "यात्री", "t": "कितनी दूर है?", "r": "kitnī dūr hai?", "en": "How far is it?"},
                {"sp": "स्थानीय", "t": "ज़्यादा दूर नहीं — बस के पास ही है।", "r": "zyādā dūr nahīṅ — bas ke pās hī hai.", "en": "Not far — it is right next to the bus stop."},
            ],
            "worksheet": {"title": "Directions worksheet", "tasks": [
                {"instruction": "Give the route politely.", "items": ["go straight", "turn right", "turn left"], "key": ["सीधे जाइए", "दाएँ मुड़िए", "बाएँ मुड़िए"]},
                {"instruction": "Where is it?", "items": ["in front of the bank", "behind the school", "near the station"], "key": ["बैंक के सामने", "स्कूल के पीछे", "स्टेशन के पास"]},
            ]},
        }),
        lesson("A1P-U1", 2, {
            "title": "Transport: बस, ऑटो, टिकट",
            "learn": ("Transport words and the two postpositions that run a journey: से (from) and तक "
                      "(up to). दिल्ली से जयपुर तक (from Delhi to Jaipur). To ask where someone is "
                      "going: आप कहाँ जा रहे हैं? For a ticket: एक टिकट चाहिए."),
            "vocab": [V("बस", "bas", "bus", "noun"), V("रेलगाड़ी", "relgāṛī", "train", "noun"),
                      V("ऑटो", "ŏṭo", "auto-rickshaw", "noun"), V("टिकट", "ṭikaṭ", "ticket", "noun"),
                      V("किराया", "kirāyā", "fare", "noun"), V("स्टेशन", "sṭeśan", "station", "noun"),
                      V("हवाई अड्डा", "havāī aḍḍā", "airport", "noun"), V("उतरना", "utarnā", "to get off")],
            "grammar": {
                "title": "X से Y तक",
                "explain": ("से marks the starting point and तक the end, and they wrap the journey: "
                            "जयपुर से दिल्ली तक. The verb agrees with the subject, not the route: "
                            "गाड़ी कितने बजे चलती है? (when does the train leave?)"),
                "pattern": "X से Y तक · … चाहिए · कहाँ जाना है?",
                "examples": [X("जयपुर से दिल्ली तक कितना किराया है?", "Jaipur se Dillī tak kitnā kirāyā hai?", "What is the fare from Jaipur to Delhi?"),
                             X("मुझे दो टिकट चाहिए।", "mujhe do ṭikaṭ cāhie.", "I need two tickets."),
                             X("गाड़ी कितने बजे चलती है?", "gāṛī kitne baje caltī hai?", "What time does the train leave?")],
                "mistakes": [{"wrong": "मुझे दो टिकट चाहता हूँ।",
                              "right": "मुझे दो टिकट चाहिए।",
                              "why": "चाहिए is invariable and the person takes the को-form: मुझे चाहिए. चाहता हूँ exists but means 'I want' with a different frame, and it is not what you say at a counter."}],
            },
            "dialogue": [
                {"sp": "यात्री", "t": "जयपुर से दिल्ली तक कितना किराया है?", "r": "Jaipur se Dillī tak kitnā kirāyā hai?", "en": "What is the fare from Jaipur to Delhi?"},
                {"sp": "क्लर्क", "t": "बस का चार सौ, गाड़ी का सात सौ।", "r": "bas kā cār sau, gāṛī kā sāt sau.", "en": "Four hundred by bus, seven hundred by train."},
                {"sp": "यात्री", "t": "मुझे दो बस टिकट चाहिए।", "r": "mujhe do bas ṭikaṭ cāhie.", "en": "I need two bus tickets."},
                {"sp": "क्लर्क", "t": "गाड़ी सुबह छह बजे चलती है — आपको जल्दी पहुँचना है।", "r": "gāṛī subah chah baje caltī hai — āpko jaldī pahuṅcnā hai.", "en": "The bus leaves at six in the morning — you need to arrive early."},
            ],
            "worksheet": {"title": "Transport worksheet", "tasks": [
                {"instruction": "Ask for tickets.", "items": ["one ticket", "two tickets to Delhi"], "key": ["मुझे एक टिकट चाहिए।", "मुझे दिल्ली के दो टिकट चाहिए।"]},
                {"instruction": "Say the route.", "items": ["from Jaipur to Delhi", "from home to the station"], "key": ["जयपुर से दिल्ली तक", "घर से स्टेशन तक"]},
            ]},
        }),
        lesson("A1P-U1", 3, {
            "title": "मुझे … चाहिए — asking for things",
            "learn": ("The single most useful A1+ sentence is मुझे … चाहिए: मुझे पानी चाहिए, मुझे मदद "
                      "चाहिए, मुझे एक कमरा चाहिए. The person takes को (मुझे/आपको/उसे), the thing is "
                      "plain, and चाहिए never changes. Add माफ़ कीजिए in front and it works at any counter."),
            "vocab": [V("चाहिए", "cāhie", "is needed / I want"), V("पानी", "pānī", "water", "noun"),
                      V("चाय", "cāy", "tea", "noun"), V("कमरा", "kamrā", "room", "noun"),
                      V("मदद", "madad", "help", "noun"), V("जानकारी", "jānkārī", "information", "noun"),
                      V("समय", "samay", "time", "noun"), V("थैला", "thailā", "bag", "noun")],
            "grammar": {
                "title": "मुझे X चाहिए",
                "explain": ("The frame is fixed: person in the को-form, thing in the plain form, चाहिए "
                            "unchanged. मुझे एक कमरा चाहिए (I want a room), आपको क्या चाहिए? (what do "
                            "you want?). Nothing about the thing changes चाहिए — not its gender, not "
                            "its number."),
                "pattern": "मुझे/आपको/उसे + thing + चाहिए",
                "examples": [X("मुझे एक कमरा चाहिए।", "mujhe ek kamrā cāhie.", "I need a room."),
                             X("आपको क्या चाहिए?", "āpko kyā cāhie?", "What would you like?"),
                             X("मुझे थोड़ी जानकारी चाहिए।", "mujhe thoṛī jānkārī cāhie.", "I need a little information.")],
                "mistakes": [{"wrong": "मैं एक कमरा चाहिए।",
                              "right": "मुझे एक कमरा चाहिए।",
                              "why": "चाहिए never takes मैं. The wanting happens *to* you in Hindi — the same को-form as मुझे पसंद है."}],
            },
            "dialogue": [
                {"sp": "अतिथि", "t": "माफ़ कीजिए, मुझे एक कमरा चाहिए।", "r": "māf kījie, mujhe ek kamrā cāhie.", "en": "Excuse me, I need a room."},
                {"sp": "मैनेजर", "t": "एक रात के लिए?", "r": "ek rāt ke lie?", "en": "For one night?"},
                {"sp": "अतिथि", "t": "हाँ — और पानी भी चाहिए।", "r": "hāṅ — aur pānī bhī cāhie.", "en": "Yes — and I need water as well."},
                {"sp": "मैनेजर", "t": "जी, कमरा नंबर तीन। कोई और चीज़ चाहिए?", "r": "jī, kamrā nambar tīn. koī aur cīz cāhie?", "en": "Yes, room three. Anything else?"},
            ],
            "worksheet": {"title": "चाहिए worksheet", "tasks": [
                {"instruction": "Ask for it.", "items": ["tea", "water", "help"], "key": ["मुझे चाय चाहिए।", "मुझे पानी चाहिए।", "मुझे मदद चाहिए।"]},
                {"instruction": "Fix the frame.", "items": ["मैं एक थैला चाहिए।", "उसको चाय चाहती है।"], "key": ["मुझे एक थैला चाहिए।", "उसे चाय चाहिए।"]},
            ]},
        }),
    ]),
    unit("A1P-U2", "Numbers, phone, money", [
        lesson("A1P-U2", 1, {
            "title": "Numbers 20–100",
            "learn": ("Hindi numbers up to twenty are irregular and have to be learned as sounds; from "
                      "twenty on they are built, but in a way English does not prepare you for: पचास is "
                      "literally 'half of a hundred', and इक्कीस is 'twenty-and-one' with the units "
                      "first. Practice them aloud in order — the rhythm is half the memory."),
            "vocab": [V("बीस", "bīs", "twenty", "number"), V("पचास", "pacās", "fifty", "number"),
                      V("साठ", "sāṭh", "sixty", "number"), V("सत्तर", "sattar", "seventy", "number"),
                      V("अस्सी", "assī", "eighty", "number"), V("सौ", "sau", "hundred", "number"),
                      V("इक्कीस", "ikkīs", "twenty-one", "number"), V("पचहत्तर", "pachattar", "seventy-five", "number")],
            "grammar": {
                "title": "Units before tens from 21 up",
                "explain": ("From twenty-one to ninety-nine the units come first and are joined with और: "
                            "इक्कीस is one-and-twenty. पचास (50) and सत्तर (70) are the two odd ones to "
                            "memorise. From fifty, the units sit inside the word: पचपन (55), पचहत्तर "
                            "(75), नब्बे (90)."),
                "pattern": "unit + और + tens · 21 = इक्कीस · 55 = पचपन",
                "examples": [X("मेरे पास बीस रुपये हैं।", "mere pās bīs rupae haiṅ.", "I have twenty rupees."),
                             X("गाड़ी पचास मिनट में पहुँचेगी।", "gāṛī pacās miniṭ meṅ pahuṅcegī.", "The train will arrive in fifty minutes."),
                             X("कमरे में पचहत्तर लोग हैं।", "kamre meṅ pachattar log haiṅ.", "There are seventy-five people in the room.")],
                "mistakes": [{"wrong": "पचास रुपये का एक: “पचास पाँच”।",
                              "right": "पचपन",
                              "why": "from fifty up the unit is inside the word. पचास पाँच is not a number anyone says — it will be heard as two numbers."}],
            },
            "dialogue": [
                {"sp": "विक्रेता", "t": "यह कुर्ता अस्सी का है।", "r": "yah kurtā assī kā hai.", "en": "This kurta is eighty."},
                {"sp": "ग्राहक", "t": "अस्सी बहुत है — सत्तर में दीजिए।", "r": "assī bahut hai — sattar meṅ dījie.", "en": "Eighty is a lot — give it for seventy."},
                {"sp": "विक्रेता", "t": "पचहत्तर — आख़िरी बात।", "r": "pachattar — ākhirī bāt.", "en": "Seventy-five — final word."},
                {"sp": "ग्राहक", "t": "ठीक है, सौ का नोट दीजिए ग़लत नहीं।", "r": "ṭhīk hai, sau kā noṭ dījie ġalat nahīṅ.", "en": "Fine — a hundred-rupee note, mind the change."},
            ],
            "worksheet": {"title": "Numbers worksheet", "tasks": [
                {"instruction": "Write the number in Hindi.", "items": ["21", "55", "90", "75"], "key": ["इक्कीस", "पचपन", "नब्बे", "पचहत्तर"]},
                {"instruction": "Say the price.", "items": ["80 rupees", "60 rupees", "100 rupees"], "key": ["अस्सी रुपये", "साठ रुपये", "सौ रुपये"]},
            ]},
        }),
        lesson("A1P-U2", 2, {
            "title": "Phone numbers and addresses",
            "learn": ("A phone number is read digit by digit, and Indians say zero as ज़ीरो or शून्य. To "
                      "ask for a repeat: ज़रा दोबारा बताइए. An address needs the noun chain पता (address), "
                      "सड़क (road), मोहल्ला (locality), मकान (house) — and the postposition at the end: "
                      "सड़क पर, मोहल्ले में."),
            "vocab": [V("फ़ोन", "fon", "phone", "noun"), V("नंबर", "nambar", "number", "noun"),
                      V("पता", "patā", "address", "noun"), V("सड़क", "saṛak", "road", "noun"),
                      V("मोहल्ला", "mohallā", "locality", "noun"), V("मकान", "makān", "house", "noun"),
                      V("दोबारा", "dobārā", "again"), V("बात करना", "bāt karnā", "to talk / to speak")],
            "grammar": {
                "title": "Digit by digit, and ज़रा … बताइए",
                "explain": ("Phone numbers are read as separate digits: नौ, आठ, दो… To ask for a repeat, "
                            "ज़रा दोबारा बताइए (could you tell me again). For an address the postposition "
                            "closes the phrase: मकान नंबर बारह, नई सड़क पर."),
                "pattern": "मेरा नंबर … है · ज़रा दोबारा बताइए · … सड़क पर",
                "examples": [X("मेरा नंबर नौ-आठ-दो-शून्य है।", "merā nambar nau-āṭh-do-śūnya hai.", "My number is nine-eight-two-zero."),
                             X("ज़रा दोबारा बताइए।", "zarā dobārā batāie.", "Could you say that again?"),
                             X("मेरा मकान नई सड़क पर है।", "merā makān naī saṛak par hai.", "My house is on Nai Road.")],
                "mistakes": [{"wrong": "मैं आपको फ़ोन करना चाहता हूँ। (asking for the number)",
                              "right": "आपका नंबर मिल सकता है? / मुझे आपका नंबर चाहिए।",
                              "why": "the English sentence states your intention; Hindi asks for the number. Saying your wish instead of your request sounds like a statement, not a question."}],
            },
            "dialogue": [
                {"sp": "मीरा", "t": "आपका फ़ोन नंबर क्या है?", "r": "āpkā fon nambar kyā hai?", "en": "What is your phone number?"},
                {"sp": "राहुल", "t": "नौ-आठ-दो-शून्य-चार…", "r": "nau-āṭh-do-śūnya-cār…", "en": "Nine-eight-two-zero-four…"},
                {"sp": "मीरा", "t": "माफ़ कीजिए, ज़रा दोबारा बताइए।", "r": "māf kījie, zarā dobārā batāie.", "en": "Sorry, could you say that again?"},
                {"sp": "राहुल", "t": "नौ-आठ-दो-शून्य-चार। और आपका पता?", "r": "nau-āṭh-do-śūnya-cār. aur āpkā patā?", "en": "Nine-eight-two-zero-four. And your address?"},
            ],
            "worksheet": {"title": "Phone worksheet", "tasks": [
                {"instruction": "Say it in Hindi.", "items": ["my phone number", "could you repeat", "my address"], "key": ["मेरा फ़ोन नंबर", "ज़रा दोबारा बताइए", "मेरा पता"]},
                {"instruction": "Read the digits aloud.", "items": ["9 8 2 0 4", "7 0 1 3"], "key": ["नौ आठ दो शून्य चार", "सात शून्य एक तीन"]},
            ]},
        }),
        lesson("A1P-U2", 3, {
            "title": "Prices and paying",
            "learn": ("Money words carry gender: रुपया is masculine, पैसा masculine, and रुपये is the "
                      "plural you actually use — पचास रुपये. To ask the total: कुल कितना हुआ? Card or "
                      "cash: कार्ड चलेगा या नक़द? छुट्टा means exact change, and every shop will ask you "
                      "for it."),
            "vocab": [V("रुपया", "rupyā", "rupee", "noun"), V("पैसा", "paisā", "money", "noun"),
                      V("महँगा", "mahṅgā", "expensive"), V("सस्ता", "sastā", "cheap"),
                      V("कुल", "kul", "total"), V("छुट्टा", "chhuṭṭā", "exact change"),
                      V("कार्ड", "kārḍ", "card", "noun"), V("नक़द", "naqad", "cash")],
            "grammar": {
                "title": "कुल कितना हुआ? · चलेगा?",
                "explain": ("कुल कितना हुआ? asks the total after the fact — हुआ, not है, because the "
                            "bill has already built up. चलेगा? is the everyday way to ask whether a "
                            "method of payment is accepted: कार्ड चलेगा? छुट्टा है? asks whether you have "
                            "small change, and the answer is usually नहीं."),
                "pattern": "कुल कितना हुआ? · कार्ड चलेगा? · छुट्टा नहीं है",
                "examples": [X("कुल कितना हुआ?", "kul kitnā huā?", "What is the total?"),
                             X("कार्ड चलेगा?", "kārḍ calegā?", "Do you take card?"),
                             X("यह बहुत महँगा है, थोड़ा सस्ता कीजिए।", "yah bahut mahṅgā hai, thoṛā sastā kījie.", "This is too expensive, make it a little cheaper.")],
                "mistakes": [{"wrong": "यह पचास रुपये महँगा है।",
                              "right": "यह बहुत महँगा है। / यह पचास रुपये का है।",
                              "why": "महँगा takes बहुत, not an amount. A price is stated with का/की: पचास रुपये का — putting the two together in one phrase mixes a price with an opinion."}],
            },
            "dialogue": [
                {"sp": "ग्राहक", "t": "कुल कितना हुआ?", "r": "kul kitnā huā?", "en": "What is the total?"},
                {"sp": "दुकानदार", "t": "दो सौ पचास।", "r": "do sau pacās.", "en": "Two hundred fifty."},
                {"sp": "ग्राहक", "t": "कार्ड चलेगा?", "r": "kārḍ calegā?", "en": "Do you take card?"},
                {"sp": "दुकानदार", "t": "कार्ड नहीं चलेगा — नक़द या छुट्टा हो तो बेहतर।", "r": "kārḍ nahīṅ calegā — naqad yā chhuṭṭā ho to behtar.", "en": "No card — cash, and exact change if possible."},
            ],
            "worksheet": {"title": "Money worksheet", "tasks": [
                {"instruction": "Ask in Hindi.", "items": ["What is the total?", "Do you take card?", "Do you have change?"], "key": ["कुल कितना हुआ?", "कार्ड चलेगा?", "छुट्टा है?"]},
                {"instruction": "Say the price.", "items": ["50-rupee", "250 rupees", "100 rupees"], "key": ["पचास रुपये का", "दो सौ पचास रुपये", "सौ रुपये"]},
            ]},
        }),
    ]),
    unit("A1P-U3", "Small talk and plans", [
        lesson("A1P-U3", 1, {
            "title": "Weather and small talk",
            "learn": ("Weather is the safest small talk in India and it runs on two nouns: गर्मी (heat) "
                      "and सर्दी (cold), used with है — आज बहुत गर्मी है. For the outdoors: धूप (sunshine), "
                      "बारिश (rain), हवा (wind), बादल (cloud). बारिश हो रही है for rain falling now."),
            "vocab": [V("मौसम", "mausam", "weather", "noun"), V("गर्मी", "garmī", "heat", "noun"),
                      V("सर्दी", "sardī", "cold", "noun"), V("बारिश", "bāriś", "rain", "noun"),
                      V("धूप", "dhūp", "sunshine", "noun"), V("हवा", "havā", "wind", "noun"),
                      V("बादल", "bādal", "cloud", "noun"), V("ठंडा", "ṭhaṇḍā", "cold (thing)")],
            "grammar": {
                "title": "गर्मी है · बारिश हो रही है",
                "explain": ("Heat and cold are nouns with है: आज बहुत गर्मी है. Rain, however, is an "
                            "event: बारिश हो रही है (it is raining), बारिश होगी (it will rain). ठंडा "
                            "agrees with the thing that is cold: पानी ठंडा है, चाय ठंडी है."),
                "pattern": "गर्मी/सर्दी है · बारिश हो रही है · X ठंडा/ठंडी है",
                "examples": [X("आज बहुत गर्मी है।", "āj bahut garmī hai.", "It is very hot today."),
                             X("बारिश हो रही है — छाता लीजिए।", "bāriś ho rahī hai — chhātā lījie.", "It is raining — take an umbrella."),
                             X("चाय ठंडी हो गई।", "cāy ṭhaṇḍī ho gaī.", "The tea has gone cold.")],
                "mistakes": [{"wrong": "आज बहुत गर्म है। (about the weather)",
                              "right": "आज बहुत गर्मी है।",
                              "why": "गर्म describes a thing (यह कमरा गर्म है); गर्मी is the noun for weather. The noun is what a conversation about the day uses."}],
            },
            "dialogue": [
                {"sp": "पड़ोसी", "t": "आज बहुत गर्मी है!", "r": "āj bahut garmī hai!", "en": "It is very hot today!"},
                {"sp": "मीरा", "t": "हाँ, और शाम को बारिश होगी।", "r": "hāṅ, aur śām ko bāriś hogī.", "en": "Yes, and it will rain in the evening."},
                {"sp": "पड़ोसी", "t": "तो छाता रखिए।", "r": "to chhātā rakhiye.", "en": "Then keep an umbrella."},
                {"sp": "मीरा", "t": "ज़रूर। सर्दी में यह मौसम बहुत अच्छा होता है।", "r": "zarūr. sardī meṅ yah mausam bahut achchhā hotā hai.", "en": "Certainly. In winter this weather is very good."},
            ],
            "worksheet": {"title": "Weather worksheet", "tasks": [
                {"instruction": "Say it in Hindi.", "items": ["It is hot today.", "It is raining.", "It will rain tomorrow."], "key": ["आज गर्मी है।", "बारिश हो रही है।", "कल बारिश होगी।"]},
                {"instruction": "Fix it.", "items": ["आज बहुत गर्म है।", "चाय ठंडा है।"], "key": ["आज बहुत गर्मी है।", "चाय ठंडी है।"]},
            ]},
        }),
        lesson("A1P-U3", 2, {
            "title": "Making a plan: कब मिलेंगे?",
            "learn": ("To arrange something: कब मिलेंगे? (when shall we meet?), मैं आज़ाद हूँ (I am "
                      "free), मैं व्यस्त हूँ (I am busy), और मुझे … बजे आना है (I have to come at …). "
                      "इंतज़ार करना is to wait, and माफ़ी for a small apology — the daily grammar of "
                      "keeping an appointment in India."),
            "vocab": [V("मिलना", "milnā", "to meet"), V("समय", "samay", "time", "noun"),
                      V("आज़ाद", "āzād", "free (not busy)"), V("व्यस्त", "vyast", "busy"),
                      V("इंतज़ार", "intzār", "a wait", "noun"), V("माफ़ी", "māfī", "apology", "noun"),
                      V("कितने बजे", "kitne baje", "at what time"), V("तय करना", "tay karnā", "to fix / decide")],
            "grammar": {
                "title": "कब मिलेंगे? · मुझे … बजे आना है",
                "explain": ("मिलेंगे is the future with the respectful plural ending, so it fits any "
                            "company: हम कब मिलेंगे? 'Have to' is the infinitive plus है: मुझे छह बजे "
                            "आना है (I have to come at six) — the person takes को again."),
                "pattern": "कब मिलेंगे? · मुझे + time + आना है · समय तय कीजिए",
                "examples": [X("हम कब मिलेंगे?", "ham kab milenge?", "When shall we meet?"),
                             X("मुझे छह बजे आना है।", "mujhe chah baje ānā hai.", "I have to come at six."),
                             X("कल शाम का समय तय कर लीजिए।", "kal śām kā samay tay kar lījie.", "Let us fix a time for tomorrow evening.")],
                "mistakes": [{"wrong": "मैं छह बजे आना है।",
                              "right": "मुझे छह बजे आना है।",
                              "why": "'have to' puts the person in the को-form. मैं आना है is two subjects in one sentence and is heard as a mistake."}],
            },
            "dialogue": [
                {"sp": "मीरा", "t": "हम कब मिलेंगे?", "r": "ham kab milenge?", "en": "When shall we meet?"},
                {"sp": "राहुल", "t": "आज शाम? मैं आज़ाद हूँ।", "r": "āj śām? main āzād hūṅ.", "en": "This evening? I am free."},
                {"sp": "मीरा", "t": "माफ़ कीजिए, आज मैं व्यस्त हूँ। कल?", "r": "māf kījie, āj main vyast hūṅ. kal?", "en": "Sorry, I am busy today. Tomorrow?"},
                {"sp": "राहुल", "t": "ठीक है — मुझे पाँच बजे आना है, छह बजे मिल लेंगे।", "r": "ṭhīk hai — mujhe pāṅc baje ānā hai, chah baje mil leṅge.", "en": "All right — I have to come at five, we will meet at six."},
            ],
            "worksheet": {"title": "Plans worksheet", "tasks": [
                {"instruction": "Arrange it in Hindi.", "items": ["When shall we meet?", "I am free tomorrow.", "I have to come at six."], "key": ["हम कब मिलेंगे?", "मैं कल आज़ाद हूँ।", "मुझे छह बजे आना है।"]},
                {"instruction": "Fix it.", "items": ["मैं पाँच बजे आना है।", "हम कब मिलूँगा?"], "key": ["मुझे पाँच बजे आना है।", "हम कब मिलेंगे?"]},
            ]},
        }),
        lesson("A1P-U3", 3, {
            "title": "Saying no politely",
            "learn": ("A refusal in Hindi arrives wrapped: माफ़ कीजिए, मैं नहीं आ पाऊँगा (sorry, I will "
                      "not be able to come). The compound नहीं … पाना is what makes it 'will not be "
                      "able' rather than 'will not', and it is much softer. Close with अगली बार ज़रूर "
                      "(next time, certainly) and the door stays open."),
            "vocab": [V("माफ़ कीजिए", "māf kījie", "sorry / excuse me"), V("नहीं हो पाएगा", "nahīṅ ho pāegā", "it will not be possible"),
                      V("अगली बार", "aglī bār", "next time"), V("ज़रूर", "zarūr", "certainly"),
                      V("कोशिश", "kośiś", "effort", "noun"), V("मजबूरी", "majbūrī", "compulsion / no choice", "noun"),
                      V("व्यस्त", "vyast", "busy"), V("आराम", "ārām", "rest", "noun")],
            "grammar": {
                "title": "नहीं + पाना = 'will not be able'",
                "explain": ("पाना as the second verb adds ability: आ पाना (to be able to come), कर "
                            "पाना (to manage to do). Made negative it becomes the polite refusal — "
                            "मैं नहीं आ पाऊँगा — where plain मैं नहीं आऊँगा sounds like a door closing. "
                            "मजबूरी है ('it is a compulsion') is the standard reason and needs no "
                            "details."),
                "pattern": "माफ़ कीजिए, मैं … नहीं … पाऊँगा · अगली बार ज़रूर",
                "examples": [X("माफ़ कीजिए, मैं नहीं आ पाऊँगा।", "māf kījie, main nahīṅ ā pāūṅgā.", "Sorry, I will not be able to come."),
                             X("कोशिश ज़रूर करूँगा।", "kośiś zarūr karūṅgā.", "I will certainly try."),
                             X("मजबूरी है — अगली बार ज़रूर।", "majbūrī hai — aglī bār zarūr.", "It is unavoidable — next time, certainly.")],
                "mistakes": [{"wrong": "नहीं, मैं नहीं आऊँगा। (to a colleague)",
                              "right": "माफ़ कीजिए, मैं नहीं आ पाऊँगा।",
                              "why": "the bare future refuses the event; नहीं … पाना refuses the possibility, which is what politeness needs. The apology in front is not optional."}],
            },
            "dialogue": [
                {"sp": "साथी", "t": "कल की बैठक में आइएगा?", "r": "kal kī baiṭhak meṅ āiega?", "en": "Will you come to tomorrow's meeting?"},
                {"sp": "मीरा", "t": "माफ़ कीजिए, मैं नहीं आ पाऊँगी।", "r": "māf kījie, main nahīṅ ā pāūṅgī.", "en": "Sorry, I will not be able to come."},
                {"sp": "साथी", "t": "कोई बात नहीं — कारण?", "r": "koī bāt nahīṅ — kāraṇ?", "en": "No matter — the reason?"},
                {"sp": "मीरा", "t": "मजबूरी है। कोशिश करूँगी — अगली बार ज़रूर।", "r": "majbūrī hai. kośiś karūṅgī — aglī bār zarūr.", "en": "It is unavoidable. I will try — next time, certainly."},
            ],
            "worksheet": {"title": "Polite no worksheet", "tasks": [
                {"instruction": "Refuse politely.", "items": ["I will not be able to come.", "I will not be able to do it today."], "key": ["माफ़ कीजिए, मैं नहीं आ पाऊँगा।", "माफ़ कीजिए, आज नहीं कर पाऊँगा।"]},
                {"instruction": "Keep the door open.", "items": ["next time, certainly", "I will certainly try"], "key": ["अगली बार ज़रूर", "कोशिश ज़रूर करूँगा"]},
            ]},
        }),
    ]),
]

A1P_EXTRA = {
    "culture": {
        "text": ("हाँ जी and अच्छा are the two words that hold up an Indian conversation. हाँ जी is not "
                 "‘yes sir’ — जी is a politeness particle that can follow almost anything (नहीं जी, ठीक "
                 "जी, प्रकाश जी), and it is what you say on the phone to mean 'yes, I am listening'. "
                 "अच्छा is 'I see' / 'really?', and the length of it tells you how surprised the "
                 "speaker is. A learner who can say हाँ जी and अच्छा at the right moments sounds "
                 "attentive long before their grammar is ready."),
        "source_url": "https://en.wikipedia.org/wiki/Hindi",
    },
    "reading": {
        "text": ("सुबह आठ बजे हैं। प्रकाश बस स्टैंड पर खड़ा है। उसे दिल्ली जाना है। "
                 "वह क्लर्क से पूछता है, “दिल्ली की बस कितने बजे आएगी?” क्लर्क कहता है, "
                 "“आधे घंटे में। टिकट लीजिए — चार सौ रुपये।” प्रकाश के पास सौ का नोट है। "
                 "वह कहता है, “माफ़ कीजिए, छुट्टा है?” क्लर्क हँसता है और कहता है, "
                 "“नहीं, पाँच सौ दीजिए।” प्रकाश पाँच सौ देता है और बस में बैठ जाता है।"),
        "gloss": ("It is eight in the morning. Prakash is standing at the bus stand. He has to go to "
                  "Delhi. He asks the clerk, “When will the Delhi bus come?” The clerk says, “In half "
                  "an hour. Take a ticket — four hundred rupees.” Prakash has a hundred-rupee note. He "
                  "says, “Excuse me, do you have change?” The clerk laughs and says, “No, give me five "
                  "hundred.” Prakash gives five hundred and sits down in the bus."),
        "original": True,
    },
    "listening": {
        "script": ("— माफ़ कीजिए, स्टेशन कहाँ है?\n"
                   "— सीधे जाइए, फिर बाएँ मुड़िए। ज़्यादा दूर नहीं है।\n"
                   "— धन्यवाद! और टिकट कहाँ मिलेगा?\n"
                   "— खिड़की नंबर दो पर। मुझे पाँच बजे की गाड़ी पकड़नी है, जल्दी कीजिए।\n"
                   "— जी, बहुत धन्यवाद।"),
        "gloss": ("— Excuse me, where is the station?\n— Go straight, then turn left. It is not far.\n"
                  "— Thank you! And where do I get a ticket?\n— At window two. I have to catch the "
                  "five o'clock train, hurry.\n— Yes, thank you very much."),
        "voice_tag": VOICE,
    },
    "idioms": [
        {"t": "हाँ जी", "literal": "yes, ji", "meaning": "yes — and also 'I am listening' on the phone"},
        {"t": "अच्छा", "literal": "good", "meaning": "I see / really? — the more drawn out, the more surprised"},
        {"t": "कोई बात नहीं", "literal": "no matter at all", "meaning": "never mind — the standard answer to an apology"},
        {"t": "ज़रा रुकिए", "literal": "wait just a little", "meaning": "hold on a moment — a polite pause, not a refusal"},
        {"t": "माफ़ कीजिए", "literal": "forgive (me)", "meaning": "excuse me — before asking a stranger anything"},
        {"t": "चलिए", "literal": "let us go", "meaning": "come on — the respectful invitation to move on"},
        {"t": "बहुत अच्छा", "literal": "very good", "meaning": "how nice! — on hearing somebody's news"},
        {"t": "फिर मिलेंगे", "literal": "we will meet again", "meaning": "see you — with no date attached"},
        {"t": "जल्दी क्या है?", "literal": "what is the hurry?", "meaning": "relax — also a polite way to stall"},
        {"t": "एक मिनट", "literal": "one minute", "meaning": "just a moment — never literally a minute"},
    ],
    "mistakes": [
        {"wrong": "मैं आपसे फ़ोन करता हूँ।", "right": "मैं आपको फ़ोन करता हूँ।",
         "why": "the person phoned takes को, not से — से would mean 'from'. फ़ोन करना is one of the first verbs where the postposition has to be learned with the verb."},
        {"wrong": "मुझे एक टिकट चाहता हूँ।", "right": "मुझे एक टिकट चाहिए।",
         "why": "चाहिए never agrees with anything. Dropping the को-form or agreeing the verb is the commonest A1+ slip."},
        {"wrong": "बस दो बजे आएगा।", "right": "बस दो बजे आएगी।",
         "why": "बस is feminine, so its verb is आएगी. Bus, train, car and plane are all feminine in Hindi — गाड़ी is the umbrella word, and it is feminine."},
    ],
    "task": {
        "title": "Plan a journey out loud",
        "instructions": ("Write and then say aloud a six-line journey plan: where you are going, how, "
                         "at what time, what it costs, and one thing you will ask a stranger. Use "
                         "से … तक for the route, मुझे … चाहिए at least once, and one polite refusal "
                         "or apology. Say it twice — the second time with the page face down and "
                         "without stopping to correct yourself."),
    },
}

A1P_TEST = [
    ("multiple_choice", "Choose the polite direction to a stranger: turn left.", "बाएँ मुड़िए"),
    ("fill_in_the_blank", "सीधे ___ , फिर बाएँ मुड़िए। (go straight)", "जाइए"),
    ("translation", "मुझे दो टिकट चाहिए।", "I need two tickets."),
    ("reverse_translation", "What is the fare from Jaipur to Delhi?", "जयपुर से दिल्ली तक कितना किराया है?"),
    ("matching", "Match सामने to its meaning.", "in front of"),
    ("word_selection", "Select the Hindi for seventy-five.", "पचहत्तर"),
    ("error_correction", "मैं एक कमरा चाहिए।", "मुझे एक कमरा चाहिए।"),
    ("dialogue_completion", "Complete: “कुल कितना हुआ?” — “दो सौ पचास” — “___?” (do you take card)", "कार्ड चलेगा?"),
    ("reading_comprehension", "बारिश हो रही है — छाता लीजिए। What should you take?", "an umbrella"),
    ("inference", "“मजबूरी है — अगली बार ज़रूर।” What is the speaker doing?", "refusing politely and leaving the door open"),
    ("main_idea", "आज बहुत गर्मी है, और शाम को बारिश होगी। What is this about?", "the day's weather"),
    ("detail_identification", "मेरा मकान नई सड़क पर है। Where is the house?", "on Nai Road"),
]


HALF_STEPS = {
    "A1+": {"title": "Getting around", "native": "हिन्दी", "goals": [
        "Ask for directions, tickets and things you need",
        "Give a phone number, an address and a price",
        "Make a plan and refuse one politely",
    ], "units": A1P_UNITS, "extra": A1P_EXTRA, "test": A1P_TEST},
}






# A2+ and B1+ live in their own module: the content is data, the machinery is
# here. A unit whose lessons already carry `practice` was built by this file's
# builders (A1+); a unit of raw lesson specs is built below.
_spec = importlib.util.spec_from_file_location("hhc", ROOT / "tools/hindi-halfsteps-content.py")
hhc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hhc)
for _level, _spec_dict in hhc.LEVELS.items():
    HALF_STEPS[_level] = _spec_dict


def main() -> int:
    check = "--check" in sys.argv
    written = stale = 0
    for level, spec in HALF_STEPS.items():
        path = ROOT / f"data/courses/phase-2/hi_{level}.json"
        units = []
        for u in spec["units"]:
            lessons = []
            for i, l in enumerate(u["lessons"], start=1):
                lessons.append(l if "practice" in l else lesson(u["id"], i, l))
            units.append({"id": u["id"], "title": u["title"], "lessons": lessons})
        doc = {
            "code": "hi", "name": "Hindi", "native": spec.get("native", "हिन्दी"), "phase": 2, "medium": "en",
            "file_level": level,
            "level": {
                "title": "Hindi %s — %s" % (level, spec["title"]),
                "goals": spec["goals"],
                "units": units,
                "test": {"title": "Hindi %s Checkpoint Test" % level,
                         "items": [{"type": t, "q": q, "answer": a} for t, q, a in spec["test"]]},
                "extra": spec["extra"],
            },
        }
        body = json.dumps(doc, ensure_ascii=False, indent=2)
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old == body:
            print("  hi %-4s already current" % level)
            continue
        if check:
            print("  hi %-4s STALE" % level)
            stale += 1
            continue
        path.write_text(body, encoding="utf-8")
        print("  hi %-4s written — %d units, %d lessons, %d idioms, %d test items"
              % (level, len(units), sum(len(u["lessons"]) for u in units),
                 len(spec["extra"]["idioms"]), len(spec["test"])))
        written += 1
    print("%s: %d written, %d stale" % ("CHECK" if check else "written", written, stale))
    return 1 if (check and (written or stale)) else 0


if __name__ == "__main__":
    raise SystemExit(main())

# -*- coding: utf-8 -*-
"""Hindi PHASE 1 depth — the third lesson in every A1 and A2 unit.

The language gate flags every published course with
`t1:units_or_lessons_out_of_range`: the schema wants 3-5 lessons per unit and
each unit carries 2. This file authors the missing third lesson for the six A1
and A2 units — the two rungs a beginner actually walks first — and appends it to
its unit as the next L3.

Every lesson here is written for Hindi: 8 vocabulary items with romanisation,
a grammar box with a pattern, three worked examples and the mistakes that rung
makes, a four-line dialogue, twelve practice items of mixed type (not the same
question twelve times), a five-item quiz with reasons, and a four-task
worksheet. Nothing is inherited from another language's lesson.

Run:  python3 tools/author-hindi-lessons.py           write
      python3 tools/author-hindi-lessons.py --check   report drift only
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (rung, unit id) -> lesson dict
HI_LESSONS: dict[tuple[str, str], dict] = {}


def lesson(rung: str, unit: str, data: dict) -> None:
    HI_LESSONS[(rung, unit)] = data


def v(t: str, r: str, en: str, pos: str = "phrase") -> dict:
    return {"t": t, "r": r, "en": en, "pos": pos}


def ex(t: str, r: str, en: str) -> dict:
    return {"t": t, "r": r, "en": en}


def line(sp: str, t: str, r: str, en: str) -> dict:
    return {"sp": sp, "t": t, "r": r, "en": en}


def p(kind: str, q: str, answer, **kw) -> dict:
    item = {"type": kind, "q": q, "answer": answer, "skill_target": kind.replace("_", " ")}
    item.update(kw)
    return item


def quiz(q: str, options: list, answer: int, why: str) -> dict:
    return {"q": q, "options": options, "answer": answer, "why": why}


def ws(title: str, tasks: list) -> dict:
    return {"title": title, "tasks": tasks}


def task(instruction: str, items: list, key: list) -> dict:
    return {"instruction": instruction, "items": items, "key": key}


# ── A1 · U1 · First words ───────────────────────────────────────────────────
lesson("A1", "A1-U1", {
    "id": "A1-U1-L3",
    "title": "कहाँ से — where you are from",
    "learn": ("से marks the place you start from: मैं जयपुर से हूँ = I am from Jaipur. Ask with "
              "आप कहाँ से हैं? Cities and countries behave the same — दिल्ली से, लंदन से, भारत से. "
              "Careful: जयपुर में हूँ means ‘I am IN Jaipur’, not ‘from’ it."),
    "vocab": [
        v("कहाँ", "kahā̃", "where", "question word"),
        v("यहाँ", "yahā̃", "here", "adverb"),
        v("वहाँ", "vahā̃", "there", "adverb"),
        v("से", "se", "from (also by, with)", "postposition"),
        v("शहर", "śahar", "city", "noun"),
        v("देश", "deś", "country", "noun"),
        v("आप कहाँ से हैं?", "āp kahā̃ se hain?", "where are you from?", "question"),
        v("मैं जयपुर से हूँ", "main Jaipur se hūṅ", "I am from Jaipur", "sentence"),
    ],
    "grammar": {
        "title": "कहाँ + से + होना",
        "explain": ("कहाँ asks the place; से marks the starting point; the BE-form still follows the person: "
                    "मैं … हूँ, आप … हैं, वह … है. So the whole question is just कहाँ से plus the BE-form "
                    "you already know."),
        "pattern": "आप कहाँ से हैं? · मैं + जगह + से + हूँ",
        "examples": [
            ex("मैं जयपुर से हूँ।", "main Jaipur se hūṅ.", "I am from Jaipur."),
            ex("आप कहाँ से हैं?", "āp kahā̃ se hain?", "Where are you from?"),
            ex("वह लंदन से है।", "vah London se hai.", "He is from London."),
        ],
        "mistakes": [
            "मैं जयपुर से हूँ है — one BE-form per sentence.",
            "Using में for origin: जयपुर में हूँ = I am in Jaipur, not I am from Jaipur.",
        ],
    },
    "dialogue": [
        line("अध्यापक", "आप कहाँ से हैं?", "āp kahā̃ se hain?", "Where are you from?"),
        line("मीरा", "मैं जयपुर से हूँ। और आप?", "main Jaipur se hūṅ. aur āp?", "I am from Jaipur. And you?"),
        line("अध्यापक", "मैं दिल्ली से हूँ, लेकिन अब यहाँ रहता हूँ।", "main Dillī se hūṅ, lekin ab yahā̃ rahtā hūṅ.",
             "I am from Delhi, but I live here now."),
        line("मीरा", "अच्छा! मेरा भाई भी दिल्ली में रहता है।", "acchā! merā bhāī bhī Dillī meṅ rahtā hai.",
             "I see! My brother lives in Delhi too."),
    ],
    "practice": [
        p("multiple_choice", "आप कहाँ से हैं? asks…", "Where are you from?",
          options=["Where are you from?", "Where are you going?", "What is your name?", "Are you well?"]),
        p("fill_in_the_blank", "मैं जयपुर ____ हूँ।", "से"),
        p("translation", "I am from Delhi.", "मैं दिल्ली से हूँ।"),
        p("reverse_translation", "वह लंदन से है।", "He is from London."),
        p("word_selection", "Choose the word that marks where you are from.", "से",
          options=["से", "है", "यहाँ", "यहाँ", "नाम"]),
        p("matching", "Match each word with its meaning.", "वहाँ = there",
          options=["वहाँ = there", "शहर = city", "कहाँ = where", "देश = country"]),
        p("reorder", "Put these in order: से · मैं · हूँ · जयपुर", "मैं जयपुर से हूँ।"),
        p("sentence_building", "Build the sentence: ‘We are from India.’", "हम भारत से हैं।"),
        p("error_correction", "Find the mistake: मैं जयपुर से हूँ है।", "मैं जयपुर से हूँ।"),
        p("dialogue_completion", "— आप कहाँ से हैं? — ____ (Answer as yourself.)", "मैं जयपुर से हूँ।"),
        p("pronunciation", "Say it clearly: कहाँ — the vowel is nasal, the mouth stays open.",
          "kahā̃", audio_source="कहाँ"),
        p("roleplay", "Introduce yourself to a stranger and ask where they are from.",
          "नमस्ते! मैं प्रकाश हूँ। मैं जयपुर से हूँ। आप कहाँ से हैं?"),
    ],
    "quiz": [
        quiz("Which sentence means ‘I am from Jaipur’?", ["मैं जयपुर में हूँ।", "मैं जयपुर से हूँ।",
             "मैं जयपुर हूँ।", "मैं जयपुर से हूँ है।"], 1,
             "से marks the origin; में would mean you are in the city right now."),
        quiz("कहाँ means…", ["here", "there", "where", "when"], 2, "कहाँ is the question word for place."),
        quiz("Choose the correct question.", ["आप कहाँ से हूँ?", "आप कहाँ से है?", "आप कहाँ से हैं?", "आप कहाँ से हूँ है?"],
             2, "आप is the respectful plural form, so the BE-form is हैं."),
        quiz("मैं दिल्ली ____ रहता हूँ means ‘I live in Delhi’. Fill the gap.", ["से", "में", "पर", "को"], 1,
             "Living somewhere is being inside the place: में."),
        quiz("Which reply fits आप कहाँ से हैं?", ["मैं ठीक हूँ।", "मेरा नाम मीरा है।",
             "मैं जयपुर से हूँ।", "नमस्ते!"], 2, "The question asks about origin, so the answer names a place."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["कहाँ", "से", "शहर", "मैं जयपुर से हूँ"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("Origin worksheet", [
        task("Write the Hindi for each place word.", ["where", "here", "there", "city"],
             ["कहाँ", "यहाँ", "वहाँ", "शहर"]),
        task("Answer as yourself — write the full sentence.", ["Where are you from?", "Where do you live now?"],
             ["मैं जयपुर से हूँ।", "मैं जयपुर में रहता हूँ।"]),
        task("से or में? Choose and write the sentence.", ["I am from Delhi.", "I live in Delhi."],
             ["मैं दिल्ली से हूँ।", "मैं दिल्ली में रहता हूँ।"]),
        task("Write the question, then answer it.", ["you (respectful) — where from",
             "he — where from"], ["आप कहाँ से हैं?", "वह कहाँ से है?"]),
    ]),
})

# ── A1 · U2 · है and plurals ────────────────────────────────────────────────
lesson("A1", "A1-U2", {
    "id": "A1-U2-L3",
    "title": "यह क्या है? — asking about things",
    "learn": ("यह क्या है? asks what a thing is; the answer is यह + thing + है. For more than one thing the "
              "demonstrative also changes: ये चाबियाँ हैं. To ask ‘is this a …?’, क्या leads: क्या यह बोतल है? "
              "Answer हाँ + the same sentence, or नहीं + what it really is."),
    "vocab": [
        v("क्या", "kyā", "what", "question word"),
        v("यह", "yah", "this (one thing)", "demonstrative"),
        v("ये", "ye", "these (more than one)", "demonstrative"),
        v("कौन", "kaun", "who", "question word"),
        v("हाँ", "hā̃", "yes", "particle"),
        v("नहीं", "nahī̃", "no, not", "particle"),
        v("बोतल", "botal", "bottle", "noun"),
        v("चाबी", "cābī", "key", "noun"),
    ],
    "grammar": {
        "title": "क्या यह … है? and ये … हैं",
        "explain": ("A yes/no question changes nothing but the order: क्या goes in front and the verb stays "
                    "where it is. A plural answer needs बoth changes — ये instead of यह, and हैं instead of है."),
        "pattern": "क्या + यह + चीज़ + है? · ये + चीज़ें + हैं",
        "examples": [
            ex("क्या यह बोतल है?", "kyā yah botal hai?", "Is this a bottle?"),
            ex("यह बोतल नहीं, चाय है।", "yah botal nahī̃, cāy hai.", "This is not a bottle, it is tea."),
            ex("ये चाबियाँ हैं।", "ye cābiyā̃ hain.", "These are keys."),
        ],
        "mistakes": [
            "Answering a bare नहीं when the real answer matters: नहीं, यह चाय है fixes the mistake instead of only refusing.",
            "यह चाबियाँ हैं — the demonstrative and the verb both have to go plural: ये चाबियाँ हैं.",
        ],
    },
    "dialogue": [
        line("अतिथि", "क्या यह आपकी चाबी है?", "kyā yah āpkī cābī hai?", "Is this your key?"),
        line("प्रिया", "नहीं, यह मेरी चाबी नहीं है। मेरी चाबी बैग में है।", "nahī̃, yah merī cābī nahī̃ hai. merī cābī baig meṅ hai.",
             "No, this is not my key. My key is in the bag."),
        line("अतिथि", "ये चाबियाँ किसकी हैं?", "ye cābiyā̃ kiskī hain?", "Whose keys are these?"),
        line("प्रिया", "वे राहुल की हैं। वह बाहर है।", "ve Rāhul kī hain. vah bāhar hai.", "They are Rahul’s. He is outside."),
    ],
    "practice": [
        p("multiple_choice", "Which question asks whether something is a book?", "क्या यह किताब है?",
          options=["क्या यह किताब है?", "यह क्या है?", "यह किताब कहाँ है?", "किताब कौन है?"]),
        p("fill_in_the_blank", "ये ____ हैं। (keys)", "चाबियाँ"),
        p("translation", "Is this water?", "क्या यह पानी है?"),
        p("reverse_translation", "ये चाबियाँ हैं।", "These are keys."),
        p("word_selection", "Which word asks about a thing, not a person?", "क्या",
          options=["क्या", "कौन", "हाँ", "ये"]),
        p("matching", "Match the question word with what it asks about.", "कौन = a person",
          options=["कौन = a person", "क्या = a thing", "कहाँ = a place", "कब = a time"]),
        p("reorder", "Put these in order: हैं · ये · चाबियाँ", "ये चाबियाँ हैं।"),
        p("sentence_building", "Build the question: ‘Is this tea?’", "क्या यह चाय है?"),
        p("error_correction", "Find the mistake: यह चाबियाँ हैं।", "ये चाबियाँ हैं।"),
        p("dialogue_completion", "— क्या यह आपकी किताब है? — ____ (It is not mine.)",
          "नहीं, यह मेरी किताब नहीं है।"),
        p("pronunciation", "Say it clearly: चाबियाँ — the final vowel is nasal.", "cābiyā̃", audio_source="चाबियाँ"),
        p("reading_comprehension", "मेज़ पर एक बोतल और दो किताबें हैं। What is on the table, and how many books?",
          "A bottle and two books."),
    ],
    "quiz": [
        quiz("ये राहुल की चाबियाँ हैं means…", ["This is Rahul’s key.", "These are Rahul’s keys.",
            "Are these Rahul’s keys?", "Rahul has no key."], 1, "ये + हैं marks a plural subject."),
        quiz("How do you ask ‘What is this?’", ["यह कौन है?", "यह क्या है?", "क्या यह है?", "यह कहाँ है?"], 1,
             "क्या asks about things; कौन asks about people."),
        quiz("Choose the correct plural sentence.", ["यह चाबियाँ हैं।", "ये चाबी है।", "ये चाबियाँ हैं।", "ये चाबियाँ है।"],
             2, "Both the demonstrative and the verb go plural."),
        quiz("क्या यह बोतल है? — the answer ‘no, it is a glass’ starts with…",
             ["हाँ,", "नहीं,", "ठीक,", "और,"], 1, "नहीं refuses, and the rest of the sentence corrects it."),
        quiz("Where does क्या go in a yes/no question?", ["At the end", "After the verb", "At the front", "It is not used"],
             2, "क्या leads the sentence; the rest of the word order is unchanged."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["क्या", "यह", "ये", "क्या यह चाय है?"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("Questions about things", [
        task("Write the Hindi for each word.", ["what", "this", "these", "yes", "no"],
             ["क्या", "यह", "ये", "हाँ", "नहीं"]),
        task("Turn each statement into a क्या question.", ["यह पानी है।", "ये किताबें हैं।"],
             ["क्या यह पानी है?", "क्या ये किताबें हैं?"]),
        task("Make each sentence plural.", ["यह चाबी है।", "यह बोतल है।"],
             ["ये चाबियाँ हैं।", "ये बोतलें हैं।"]),
        task("Write a two-line dialogue: ask what something is, then answer.",
             ["a bottle", "keys"], ["— यह क्या है? — यह बोतल है।", "— ये क्या हैं? — ये चाबियाँ हैं।"]),
    ]),
})

# ── A1 · U3 · First verbs ───────────────────────────────────────────────────
lesson("A1", "A1-U3", {
    "id": "A1-U3-L3",
    "title": "इए — asking people to do things",
    "learn": ("A request to someone you respect ends in इए: बोलिए, बैठिए, सुनिए, आइए. With a friend the same "
              "verb ends in ओ: बोलो, बैठो, सुनो, आओ. Two verbs change shape completely — करना becomes कीजिए, "
              "and देना becomes दीजिए."),
    "vocab": [
        v("बोलिए", "bolie", "please speak (respectful)", "imperative"),
        v("सुनिए", "sunie", "please listen (respectful)", "imperative"),
        v("बैठिए", "baithie", "please sit (respectful)", "imperative"),
        v("आइए", "āie", "please come (respectful)", "imperative"),
        v("कीजिए", "kījie", "please do (respectful)", "imperative"),
        v("दीजिए", "dījie", "please give (respectful)", "imperative"),
        v("ज़रा", "zarā", "just, a little — softens a request", "particle"),
        v("धीरे", "dhīre", "slowly", "adverb"),
    ],
    "grammar": {
        "title": "क्रिया-मूल + इए (आप) · + ओ (तुम)",
        "explain": ("The respectful imperative is built on the verb stem: सुन + इए = सुनिए. With तुम the ending "
                    "is ओ. Adding ज़रा in front makes any request softer, and धीरे politely sets the pace."),
        "pattern": "ज़रा + धीरे + बोलिए · बैठिए · सुनिए · कीजिए · दीजिए",
        "examples": [
            ex("ज़रा धीरे बोलिए।", "zarā dhīre bolie.", "Please speak a little slower."),
            ex("अंदर आइए, यहाँ बैठिए।", "andar āie, yahā̃ baithie.", "Come in, sit here."),
            ex("यह काम अभी कीजिए।", "yah kām abhī kījie.", "Please do this work now."),
        ],
        "mistakes": [
            "बोलो to an elder or a stranger — बोलिए. The ending carries the respect, not the tone of voice.",
            "करिए for करना: the respectful form is कीजिए, and देना follows the same pattern with दीजिए.",
        ],
    },
    "dialogue": [
        line("अध्यापक", "ज़रा धीरे बोलिए, और दोबारा पढ़िए।", "zarā dhīre bolie, aur dobārā paṛhie.",
             "Please speak a little slower, and read it again."),
        line("छात्र", "ठीक है। क्या मैं अब बैठ जाऊँ?", "ṭhīk hai. kyā main ab baith jāū̃?",
             "All right. May I sit down now?"),
        line("अध्यापक", "हाँ, बैठिए। और यह किताब अपने साथ ले जाइए।", "hā̃, baithie. aur yah kitāb apne sāth le jāie.",
             "Yes, sit down. And take this book with you."),
        line("छात्र", "धन्यवाद। मैं कल इसे वापस लाऊँगा।", "dhanyavād. main kal ise vāpas lāū̃gā.",
             "Thank you. I will bring it back tomorrow."),
    ],
    "practice": [
        p("multiple_choice", "Which form would you use to ask an elder to sit?", "बैठिए",
          options=["बैठिए", "बैठो", "बैठ", "बैठना"]),
        p("fill_in_the_blank", "ज़रा ____ बोलिए। (slowly)", "धीरे"),
        p("translation", "Please come in and sit here.", "अंदर आइए और यहाँ बैठिए।"),
        p("reverse_translation", "यह काम अभी कीजिए।", "Please do this work now."),
        p("word_selection", "Which word softens a request?", "ज़रा", options=["ज़रा", "अभी", "बहुत", "फिर"]),
        p("matching", "Match the respectful form with its verb.", "देना = दीजिए",
          options=["देना = दीजिए", "करना = कीजिए", "सुनना = सुनिए", "आना = आइए"]),
        p("reorder", "Put these in order: बोलिए · ज़रा · धीरे", "ज़रा धीरे बोलिए।"),
        p("sentence_building", "Build the request: ‘Please give me the key.’", "मुझे चाबी दीजिए।"),
        p("error_correction", "Find the mistake: ज़रा धीरे बोलो, अंकल जी।", "ज़रा धीरे बोलिए, अंकल जी।"),
        p("dialogue_completion", "— ____ (Please sit.) — धन्यवाद।", "बैठिए।"),
        p("pronunciation", "Say it clearly: दीजिए — three syllables, no swallowed vowel.", "dījie", audio_source="दीजिए"),
        p("speak", "Give a stranger three polite instructions using इए forms.", "आइए, बैठिए, और ज़रा धीरे बोलिए।"),
    ],
    "quiz": [
        quiz("The respectful form of करना is…", ["करिए", "कीजिए", "करो", "करता"], 1,
             "करना is irregular in the imperative: कीजिए."),
        quiz("आइए means…", ["I came", "please come", "he comes", "come (to a child)"], 1,
             "इए turns a stem into a respectful request."),
        quiz("Which sentence is correct for asking an elder to speak slowly?",
             ["धीरे बोल।", "धीरे बोलो।", "ज़रा धीरे बोलिए।", "धीरे बोलता है।"], 2,
             "बोलिए plus ज़रा is the polite form."),
        quiz("For a close friend, the imperative ending is…", ["इए", "ओ", "ता है", "आ"], 1,
             "तुम takes ओ: बोलो, बैठो, सुनो."),
        quiz("दीजिए comes from which verb?", ["देना", "दीना", "लेना", "दिलाना"], 0,
             "देना → दीजिए; लेना gives लीजिए, which means ‘take’, not ‘give’."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["बोलिए", "सुनिए", "दीजिए", "ज़रा धीरे बोलिए"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("Polite requests", [
        task("Write the respectful imperative of each verb.", ["सुनना", "करना", "देना", "आना"],
             ["सुनिए", "कीजिए", "दीजिए", "आइए"]),
        task("Turn each order into a polite request (तुम → आप).", ["बोलो।", "बैठो।"], ["बोलिए।", "बैठिए।"]),
        task("Translate into Hindi.", ["Please give me some water.", "Please speak slowly."],
             ["मुझे पानी दीजिए।", "ज़रा धीरे बोलिए।"]),
        task("Write two polite instructions for a guest arriving at your home.",
             ["come in", "sit here"], ["अंदर आइए।", "यहाँ बैठिए।"]),
    ]),
})

# ── A2 · U1 · Past and future ───────────────────────────────────────────────
lesson("A2", "A2-U1", {
    "id": "A2-U1-L3",
    "title": "कल — yesterday and tomorrow in one word",
    "learn": ("कल is both yesterday and tomorrow; the verb decides which one you mean. कल मैं बाज़ार गया था = "
              "yesterday I went; कल मैं बाज़ार जाऊँगा = tomorrow I will go. The same is true of परसों (the day "
              "before yesterday / the day after tomorrow), so a Hindi sentence about time is carried by its verb."),
    "vocab": [
        v("कल", "kal", "yesterday / tomorrow", "time word"),
        v("परसों", "parsõ", "day before yesterday / day after tomorrow", "time word"),
        v("आज", "āj", "today", "time word"),
        v("अभी", "abhī", "right now", "time word"),
        v("पिछले हफ़्ते", "pichle hafte", "last week", "time phrase"),
        v("अगले हफ़्ते", "agle hafte", "next week", "time phrase"),
        v("इस साल", "is sāl", "this year", "time phrase"),
        v("बार-बार", "bār-bār", "again and again", "adverb"),
    ],
    "grammar": {
        "title": "Time words carry no tense — the verb does",
        "explain": ("Hindi does not mark कल as past or future. A perfective verb (गया, खाया, आया) sends it "
                    "backwards; a future verb (जाऊँगा, खाऊँगा, आऊँगा) sends it forwards. Put the time word first "
                    "in the sentence and the listener hears the direction from the ending."),
        "pattern": "कल + गया/गई/गया था = yesterday · कल + जाऊँगा/जाएगी = tomorrow",
        "examples": [
            ex("कल मैं दिल्ली गया था।", "kal main Dillī gayā thā.", "I went to Delhi yesterday."),
            ex("कल मैं दिल्ली जाऊँगा।", "kal main Dillī jāū̃gā.", "I will go to Delhi tomorrow."),
            ex("परसों बारिश हुई थी, और परसों फिर होगी।", "parsõ bāriś huī thī, aur parsõ phir hogī.",
               "It rained the day before yesterday, and it will rain again the day after tomorrow."),
        ],
        "mistakes": [
            "कल मैं बाज़ार जाऊँगा था — a future form and a past marker cannot sit together; choose one direction.",
            "Putting कल at the end of the sentence: Hindi time words normally open it, and a late कल sounds like an afterthought.",
        ],
    },
    "dialogue": [
        line("राहुल", "कल आप बाज़ार गए थे?", "kal āp bāzār gae the?", "Did you go to the market yesterday?"),
        line("मीरा", "नहीं, कल मैं घर पर थी। बाज़ार मैं परसों गई थी।", "nahī̃, kal main ghar par thī. bāzār main parsõ gaī thī.",
             "No, yesterday I was at home. I went to the market the day before yesterday."),
        line("राहुल", "अच्छा। तो कल फिर जाना है?", "acchā. to kal phir jānā hai?", "I see. So we have to go again tomorrow?"),
        line("मीरा", "हाँ, कल सुबह जाऊँगी। आप भी चलिए।", "hā̃, kal subah jāū̃gī. āp bhī calie.",
             "Yes, I will go tomorrow morning. Come along."),
    ],
    "practice": [
        p("multiple_choice", "कल मैं स्कूल गया। — when did this happen?", "yesterday",
          options=["yesterday", "tomorrow", "today", "next week"]),
        p("fill_in_the_blank", "कल मैं बाज़ार ____। (I will go tomorrow)", "जाऊँगा"),
        p("translation", "I went to Delhi yesterday.", "कल मैं दिल्ली गया था।"),
        p("reverse_translation", "कल मैं दिल्ली जाऊँगा।", "I will go to Delhi tomorrow."),
        p("word_selection", "Which word can mean both yesterday and tomorrow?", "कल",
          options=["कल", "आज", "अभी", "परसों"]),
        p("matching", "Match the time word with the day it names.", "परसों = the day before yesterday or the day after tomorrow",
          options=["कल = yesterday or tomorrow", "आज = today", "अभी = right now",
                   "परसों = the day before yesterday or the day after tomorrow"]),
        p("reorder", "Put these in order: गया · कल · मैं · था", "कल मैं गया था।"),
        p("sentence_building", "Build the sentence: ‘We will meet next week.’", "हम अगले हफ़्ते मिलेंगे।"),
        p("error_correction", "Find the mistake: कल मैं बाज़ार जाऊँगा था।", "कल मैं बाज़ार जाऊँगा।"),
        p("dialogue_completion", "— आप कल कहाँ थे? — ____ (I was at home yesterday.)", "कल मैं घर पर था।"),
        p("semantic_distinction", "Explain the difference: कल मैं आया। / कल मैं आऊँगा।",
          "The first is yesterday and the second is tomorrow; कल itself carries no direction."),
        p("short_writing", "Write three sentences about yesterday, today and tomorrow using कल once only.",
          "कल मैं दफ़्तर गया था। आज मैं घर पर हूँ। कल मैं स्कूल जाऊँगा।"),
    ],
    "quiz": [
        quiz("कल मैं जाऊँगा — which day?", ["yesterday", "tomorrow", "today", "the day before yesterday"], 1,
             "जाऊँगा is future, so कल means tomorrow."),
        quiz("परसों can mean…", ["today or tonight", "the day before yesterday or the day after tomorrow",
             "last week or next week", "now or later"], 1, "परसों is two days away in either direction."),
        quiz("Which sentence is correct?", ["कल मैं गया था।", "कल मैं गया हूँ।", "कल मैं जाऊँगा था।", "कल मैं जाया।"], 0,
             "Past needs a perfective plus था; the others mix forms."),
        quiz("Where does a time word usually sit in a Hindi sentence?", ["At the end", "Before the verb, after the object",
             "At the start", "It cannot be used"], 2, "Hindi sentences normally open with place or time, then the subject."),
        quiz("आज means…", ["yesterday", "tomorrow", "today", "day after tomorrow"], 2, "आज is today."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["कल", "परसों", "आज", "पिछले हफ़्ते"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("कल in both directions", [
        task("Say which day each sentence is about.", ["कल मैं स्कूल गया।", "कल मैं स्कूल जाऊँगा।", "कल मैं स्कूल जाऊँगी।"],
             ["yesterday", "tomorrow (a boy or man speaking)", "tomorrow (a girl or woman speaking)"]),
        task("Write the Hindi for each time word.", ["today", "right now", "last week", "next week"],
             ["आज", "अभी", "पिछले हफ़्ते", "अगले हफ़्ते"]),
        task("Translate into Hindi.", ["What did you do yesterday?", "What will you do tomorrow?"],
             ["कल आपने क्या किया?", "कल आप क्या करेंगे?"]),
        task("Write two sentences with परसों, one pointing backwards and one forwards.",
             ["it rained", "we will meet"], ["परसों बारिश हुई थी।", "परसों हम मिलेंगे।"]),
    ]),
})

# ── A2 · U2 · Postpositions ─────────────────────────────────────────────────
lesson("A2", "A2-U2", {
    "id": "A2-U2-L3",
    "title": "ने — the marker of who did it",
    "learn": ("When a verb is transitive and finished, the doer takes ने: मैंने चाय पी, उसने खाना बनाया. The "
              "verb then agrees with the thing acted on, not with the doer — उसने दो किताबें पढ़ीं. Intransitive "
              "verbs never take it: मैं स्कूल गया, never मैंने स्कूल गया."),
    "vocab": [
        v("ने", "ne", "doer marker with finished transitive verbs", "particle"),
        v("मैंने", "mainne", "I (as doer of a finished action)", "pronoun form"),
        v("उसने", "usne", "he/she (as doer)", "pronoun form"),
        v("हमने", "hamne", "we (as doers)", "pronoun form"),
        v("आपने", "āpne", "you (respectful, as doer)", "pronoun form"),
        v("चिट्ठी", "ciṭṭhī", "letter", "noun"),
        v("बनाया", "banāyā", "made, cooked", "verb form"),
        v("बुलाया", "bulāyā", "called, invited", "verb form"),
    ],
    "grammar": {
        "title": "doer + ने + object + perfective verb",
        "explain": ("ने marks the doer only in the perfective, and only for transitive verbs. The verb drops its "
                    "agreement with the doer and follows the object instead: मैंने एक किताब पढ़ी (feminine object), "
                    "मैंने दो किताबें पढ़ीं (plural), मैंने पानी पिया (masculine object)."),
        "pattern": "मैंने + चीज़ + पी/पढ़ी/पढ़ीं/लिखी",
        "examples": [
            ex("मैंने सुबह चाय पी।", "mainne subah cāy pī.", "I drank tea in the morning."),
            ex("उसने दो किताबें पढ़ीं।", "usne do kitābẽ paṛhī̃.", "She read two books."),
            ex("हमने उन्हें कल बुलाया।", "hamne unhẽ kal bulāyā.", "We called them yesterday."),
        ],
        "mistakes": [
            "मैंने जयपुर गया — जाना is intransitive, so there is no ने: मैं जयपुर गया।",
            "मैंने किताब पढ़ा — the verb agrees with किताब, so it is पढ़ी: मैंने किताब पढ़ी।",
        ],
    },
    "dialogue": [
        line("मीरा", "आपने कल का अख़बार पढ़ा?", "āpne kal kā akhbār paṛhā?", "Did you read yesterday’s newspaper?"),
        line("राहुल", "नहीं, मैंने अख़बार नहीं पढ़ा। मैंने एक किताब पढ़ी।", "nahī̃, mainne akhbār nahī̃ paṛhā. mainne ek kitāb paṛhī.",
             "No, I did not read the newspaper. I read a book."),
        line("मीरा", "किसने लिखी है वह किताब?", "kisne likhī hai vah kitāb?", "Who wrote that book?"),
        line("राहुल", "यह किताब प्रेमचंद ने लिखी थी।", "yah kitāb Premcand ne likhī thī.", "Premchand wrote this book."),
    ],
    "practice": [
        p("multiple_choice", "Which sentence is correct?", "मैं स्कूल गया।",
          options=["मैं स्कूल गया।", "मैंने स्कूल गया।", "मैंने स्कूल गई।", "मैं स्कूल गई ने।"]),
        p("fill_in_the_blank", "मैंने एक किताब ____। (read — it agrees with किताब)", "पढ़ी"),
        p("translation", "I drank tea.", "मैंने चाय पी।"),
        p("reverse_translation", "उसने दो किताबें पढ़ीं।", "She read two books."),
        p("word_selection", "Which pronoun form is the doer of a finished action?", "मैंने",
          options=["मैंने", "मैं", "मेरा", "मुझे"]),
        p("matching", "Match the doer form with its meaning.", "आपने = you (respectful, as doer)",
          options=["मैंने = I (as doer)", "उसने = he/she (as doer)", "हमने = we (as doers)",
                   "आपने = you (respectful, as doer)"]),
        p("reorder", "Put these in order: चाय · मैंने · पी", "मैंने चाय पी।"),
        p("sentence_building", "Build the sentence: ‘We called them yesterday.’", "हमने उन्हें कल बुलाया।"),
        p("error_correction", "Find the mistake: मैंने किताब पढ़ा।", "मैंने किताब पढ़ी।"),
        p("dialogue_completion", "— आपने खाना बनाया? — ____ (No, mother made it.)",
          "नहीं, माँ ने बनाया।"),
        p("semantic_distinction", "Explain the difference: मैं गया। / मैंने खाया।",
          "The first verb is intransitive so there is no ने; the second is transitive and perfective, so ने is required."),
        p("short_writing", "Write three sentences about what you did yesterday, using ने at least twice.",
          "मैं स्कूल गया। मैंने होमवर्क किया और मैंने चाय पी।"),
    ],
    "quiz": [
        quiz("Which verb needs ने in the past?", ["जाना", "आना", "खाना", "सोना"], 2,
             "खाना is transitive, so the finished past takes ने: मैंने खाया."),
        quiz("Complete correctly: उसने एक किताब ____।", ["पढ़ा", "पढ़ी", "पढ़े", "पढ़ता"], 1,
             "The verb agrees with किताब, which is feminine singular."),
        quiz("मैंने सुबह चाय पी means…", ["I drink tea in the morning.", "I drank tea in the morning.",
             "I will drink tea in the morning.", "I am drinking tea."], 1, "Perfective plus ने puts it in the past."),
        quiz("Which sentence is wrong?", ["हमने उन्हें बुलाया।", "मैं स्कूल गया।", "उसने चिट्ठी लिखी।",
             "मैंने घर आया।"], 3, "आना is intransitive — मैं घर आया।"),
        quiz("ने appears only…", ["in questions", "with transitive verbs in the perfective", "with the future",
             "with every past verb"], 1, "It marks a transitive doer in a finished action."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["ने", "मैंने", "उसने", "मैंने चाय पी"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("The ने worksheet", [
        task("ने or no ने? Write the correct sentence.", ["I went home.", "I ate food.", "She read a book."],
             ["मैं घर गया।", "मैंने खाना खाया।", "उसने किताब पढ़ी।"]),
        task("Make the verb agree with the object.", ["मैंने चाय ____। (पीना)", "मैंने रोटी ____। (खाना)",
             "मैंने दो चिट्ठियाँ ____। (लिखना)"], ["मैंने चाय पी।", "मैंने रोटी खाई।", "मैंने दो चिट्ठियाँ लिखीं।"]),
        task("Translate into Hindi.", ["Who wrote this letter?", "We called them yesterday."],
             ["यह चिट्ठी किसने लिखी?", "हमने उन्हें कल बुलाया।"]),
        task("Put each sentence into the finished past.", ["मैं चाय पीता हूँ।", "वह किताब पढ़ती है।"],
             ["मैंने चाय पी।", "उसने किताब पढ़ी।"]),
    ]),
})

# ── A2 · U3 · Food and shopping ─────────────────────────────────────────────
lesson("A2", "A2-U3", {
    "id": "A2-U3-L3",
    "title": "रेस्टोरेंट में — ordering and the bill",
    "learn": ("Two verbs run a Hindi restaurant: दीजिए (please give) and लाइए (please bring). मुझे एक थाली "
              "दीजिए asks for a plate for yourself; उन्हें मेन्यू लाइए brings the menu to them. To close the meal "
              "you ask for the बिल or, more traditionally, the हिसाब."),
    "vocab": [
        v("मेन्यू", "menyū", "menu", "noun"),
        v("थाली", "thālī", "plate; a full meal", "noun"),
        v("बिल", "bil", "bill", "noun"),
        v("हिसाब", "hisāb", "the account, the bill", "noun"),
        v("दिखाइए", "dikhāie", "please show", "imperative"),
        v("लाइए", "lāie", "please bring", "imperative"),
        v("तीखा", "tīkhā", "spicy, hot", "adjective"),
        v("मीठा", "mīṭhā", "sweet", "adjective"),
    ],
    "grammar": {
        "title": "मुझे … दीजिए · उन्हें … लाइए",
        "explain": ("The person who receives takes को — मुझे, हमें, उन्हें — and the request verb comes last with "
                    "the respectful इए ending. देना → दीजिए (give), लाना → लाइए (bring), दिखाना → दिखाइए (show). "
                    "Degree words sit before the noun: थोड़ा कम तीखा, बहुत मीठा."),
        "pattern": "मुझे + चीज़ + दीजिए · थोड़ा कम/ज़्यादा + तीखा/मीठा",
        "examples": [
            ex("मुझे एक थाली दीजिए।", "mujhe ek thālī dījie.", "Please give me one plate."),
            ex("ज़रा मेन्यू दिखाइए।", "zarā menyū dikhāie.", "Please show me the menu."),
            ex("थोड़ा कम तीखा बनाइए, और अंत में बिल लाइए।", "thoṛā kam tīkhā banāie, aur ant meṅ bil lāie.",
               "Please make it a little less spicy, and bring the bill at the end."),
        ],
        "mistakes": [
            "मैं चाय चाहता हूँ दीजिए — two request patterns in one sentence. Choose मुझे चाय दीजिए or मुझे चाय चाहिए.",
            "लीजिए (please take) is not लाइए (please bring). The second is what you say in a restaurant.",
        ],
    },
    "dialogue": [
        line("वेटर", "आप क्या लेंगे?", "āp kyā leṅge?", "What will you have?"),
        line("ग्राहक", "ज़रा मेन्यू दिखाइए। और मुझे एक थाली दीजिए।", "zarā menyū dikhāie. aur mujhe ek thālī dījie.",
             "Please show me the menu. And give me one plate."),
        line("वेटर", "ठीक है। तीखा कम रखूँ?", "ṭhīk hai. tīkhā kam rakhū̃?", "All right. Shall I keep it less spicy?"),
        line("ग्राहक", "हाँ, थोड़ा कम तीखा। और खाने के बाद बिल लाइए।", "hā̃, thoṛā kam tīkhā. aur khāne ke bād bil lāie.",
             "Yes, a little less spicy. And bring the bill after the meal."),
    ],
    "practice": [
        p("multiple_choice", "You want the menu brought to you. Which do you say?", "ज़रा मेन्यू दिखाइए।",
          options=["ज़रा मेन्यू दिखाइए।", "मेन्यू लीजिए।", "मेन्यू कहाँ है?", "मैं मेन्यू हूँ।"]),
        p("fill_in_the_blank", "मुझे एक थाली ____। (please give)", "दीजिए"),
        p("translation", "Please bring the bill.", "बिल लाइए।"),
        p("reverse_translation", "मुझे एक थाली दीजिए।", "Please give me one plate."),
        p("word_selection", "Which word means ‘the account’ in a restaurant?", "हिसाब",
          options=["हिसाब", "मेन्यू", "थाली", "मीठा"]),
        p("matching", "Match the request verb with its meaning.", "दिखाइए = please show",
          options=["दीजिए = please give", "लाइए = please bring", "दिखाइए = please show", "बनाइए = please make"]),
        p("reorder", "Put these in order: लाइए · बिल · ज़रा", "ज़रा बिल लाइए।"),
        p("sentence_building", "Build the request: ‘Please make it a little less spicy.’", "थोड़ा कम तीखा बनाइए।"),
        p("error_correction", "Find the mistake: मुझे चाय दीजिए चाहिए।", "मुझे चाय दीजिए।"),
        p("dialogue_completion", "— खाना कैसा है? — ____ (It is very good, but it is a little too spicy.)",
          "बहुत अच्छा है, लेकिन थोड़ा ज़्यादा तीखा है।"),
        p("roleplay", "Order a meal for two and ask for the bill.", "हमें दो थाली दीजिए, और ज़रा मेन्यू दिखाइए। खाने के बाद बिल लाइए।"),
        p("reading_comprehension", "मीरा ने थाली ली, चाय पी और बिल माँगा। What did Meera do, in order?",
          "She took a plate, drank tea, and asked for the bill."),
    ],
    "quiz": [
        quiz("Which word means ‘please bring’?", ["दीजिए", "लाइए", "लीजिए", "दिखाइए"], 1,
             "लाना → लाइए. लीजिए would be ‘please take’."),
        quiz("मुझे एक थाली दीजिए — who receives the plate?", ["the waiter", "the speaker", "somebody else", "nobody"],
             1, "मुझे means ‘to me’."),
        quiz("To ask for the bill you say…", ["बिल दिखाइए।", "बिल लाइए।", "बिल लीजिए।", "बिल हूँ।"], 1,
             "The bill is brought to you, so लाइए."),
        quiz("‘A little less spicy’ is…", ["थोड़ा कम तीखा", "थोड़ा ज़्यादा तीखा", "बहुत तीखा", "कम थोड़ा तीखा"], 0,
             "The degree word comes before the adjective: थोड़ा कम + तीखा."),
        quiz("Which sentence mixes two patterns and is wrong?", ["मुझे चाय चाहिए।", "मुझे चाय दीजिए।",
             "मैं चाय चाहता हूँ दीजिए।", "मैं चाय लूँगा।"], 2,
             "चाहता हूँ and दीजिए are two different requests and cannot share a sentence."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["थाली", "बिल", "दिखाइए", "मुझे एक थाली दीजिए"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("At the restaurant", [
        task("Write the Hindi for each item.", ["menu", "plate/thali", "bill", "spicy", "sweet"],
             ["मेन्यू", "थाली", "बिल", "तीखा", "मीठा"]),
        task("Build each request with दीजिए or लाइए.", ["give me water", "bring the bill", "show the menu"],
             ["मुझे पानी दीजिए।", "बिल लाइए।", "मेन्यू दिखाइए।"]),
        task("Soften each request with ज़रा or थोड़ा कम.", ["make it spicy", "bring the menu"],
             ["ज़रा तीखा बनाइए।", "ज़रा मेन्यू लाइए।"]),
        task("Write a four-line restaurant dialogue: order, a question from the waiter, a change, and the bill.",
             ["order", "waiter asks", "change", "bill"],
             ["मुझे एक थाली दीजिए।", "तीखा कम रखूँ?", "हाँ, थोड़ा कम तीखा।", "खाने के बाद बिल लाइए।"]),
    ]),
})

# ── B1 · U1 · Ergative and compulsion ───────────────────────────────────────
lesson("B1", "B1-U1", {
    "id": "B1-U1-L3",
    "title": "किसने? — questions and negatives that need ने",
    "learn": ("Once a verb is transitive and finished, ने survives every change you make to the sentence: "
              "किसने बनाया? (who made it?), आपने खाना खाया या नहीं? (did you eat or not?), मैंने अभी तक "
              "किताब नहीं पढ़ी (I have not read the book yet). Question words take ने too — किसने, किस-किसने."),
    "vocab": [
        v("किसने", "kisne", "who (as the doer)", "question form"),
        v("किसको", "kisko", "whom (to whom)", "question form"),
        v("अभी तक", "abhī tak", "until now, yet", "time phrase"),
        v("पहले", "pahle", "before, first", "adverb"),
        v("कभी नहीं", "kabhī nahī̃", "never", "adverb"),
        v("साफ़", "sāf", "clean", "adjective"),
        v("ठीक किया", "ṭhīk kiyā", "did (it) right", "phrase"),
        v("याद", "yād", "memory; to remember (याद होना/करना)", "noun"),
    ],
    "grammar": {
        "title": "ने in questions and negatives",
        "explain": ("ने is not limited to statements. In a question the doer word simply becomes किसने; in a "
                    "negative the नहीं sits between the object and the verb, and ने stays where it was: "
                    "मैंने वह किताब नहीं पढ़ी. Do not drop ने just because the sentence is negative or a question."),
        "pattern": "किसने + object + verb? · doer + ने + object + नहीं + verb",
        "examples": [
            ex("यह खाना किसने बनाया?", "yah khānā kisne banāyā?", "Who made this food?"),
            ex("मैंने वह किताब अभी तक नहीं पढ़ी।", "mainne vah kitāb abhī tak nahī̃ paṛhī.",
               "I have not read that book yet."),
            ex("आपने मुझे पहले क्यों नहीं बताया?", "āpne mujhe pahle kyõ nahī̃ batāyā?",
               "Why did you not tell me before?"),
        ],
        "mistakes": [
            "कौन बनाया? for a thing that was made — for a transitive finished act the question word is किसने: किसने बनाया?",
            "Dropping ने in the negative: मैं वह किताब नहीं पढ़ी is heard, but in careful speech it is मैंने वह किताब नहीं पढ़ी।",
        ],
    },
    "dialogue": [
        line("मीरा", "यह साफ़ कमरा किसने किया?", "yah sāf kamrā kisne kiyā?", "Who cleaned this room?"),
        line("राहुल", "मैंने किया, लेकिन मैंने खिड़की नहीं खोली।", "mainne kiyā, lekin mainne khiṛkī nahī̃ kholī.",
             "I did, but I did not open the window."),
        line("मीरा", "आपने मुझे बताया ही नहीं था।", "āpne mujhe batāyā hī nahī̃ thā.", "You did not tell me at all."),
        line("राहुल", "सही कहा, मैंने याद ही नहीं रखा। अब बता दिया।", "sahī kahā, mainne yād hī nahī̃ rakhā. ab batā diyā.",
             "True, I did not remember. Now I have told you."),
    ],
    "practice": [
        p("multiple_choice", "Someone cleaned the room. The question ‘who did it?’ is…",
          "यह कमरा किसने साफ़ किया?", options=["यह कमरा किसने साफ़ किया?", "यह कमरा कौन साफ़ हुआ?",
          "कौन साफ़ कमरा है?", "किसने साफ़ है?"]),
        p("fill_in_the_blank", "मैंने वह किताब अभी तक ____ पढ़ी। (not)", "नहीं"),
        p("translation", "Who wrote this letter?", "यह चिट्ठी किसने लिखी?"),
        p("reverse_translation", "आपने मुझे पहले क्यों नहीं बताया?", "Why did you not tell me before?"),
        p("word_selection", "Which form asks ‘who’ as the doer of a finished action?", "किसने",
          options=["किसने", "कौन", "किसको", "किसका"]),
        p("matching", "Match each question word with what it asks.", "किसको = to whom",
          options=["किसने = who (doer)", "किसको = to whom", "कहाँ = where", "कब = when"]),
        p("reorder", "Put these in order: बनाया · किसने · खाना · यह", "यह खाना किसने बनाया?"),
        p("sentence_building", "Build the sentence: ‘I have not seen that film yet.’",
          "मैंने वह फ़िल्म अभी तक नहीं देखी।"),
        p("error_correction", "Find the mistake: यह काम कौन किया?", "यह काम किसने किया?"),
        p("dialogue_completion", "— यह किताब किसने लिखी? — ____ (I do not know, but I have read it.)",
          "मुझे नहीं पता, लेकिन मैंने इसे पढ़ी है।"),
        p("inference", "मैंने अभी तक नहीं देखा — what does this tell you about the speaker’s plan?",
          "The speaker has not watched it yet and implies it is still on the list; अभी तक leaves the action open."),
        p("short_writing", "Write three questions with किसने about things people do at home.",
          "खाना किसने बनाया? कमरा किसने साफ़ किया? बर्तन किसने धोए?"),
    ],
    "quiz": [
        quiz("Which is the correct question for ‘who made this?’", ["यह कौन बनाया?", "यह किसने बनाया?",
            "यह किस बनाया?", "यह कौन बना?"], 1, "किसने is the doer form with a transitive perfective."),
        quiz("Complete: मैंने वह किताब ____ पढ़ी।", ["नहीं", "न", "मत", "ना"], 0,
             "With a perfective verb the negative is नहीं, placed before the verb."),
        quiz("आपने मुझे क्यों नहीं बताया? asks…", ["Why did you not tell me?", "Why are you telling me?",
            "Will you tell me?", "Who told me?"], 0, "आपने is the respectful doer form in the past."),
        quiz("Which sentence keeps ने correctly?", ["मैं वह किताब नहीं पढ़ी।", "मैंने वह किताब नहीं पढ़ी।",
            "मैं वह किताब नहीं पढ़ा।", "मैंने वह किताब नहीं पढ़ा।"], 1,
             "Both the doer form and the feminine agreement matter: मैंने … नहीं पढ़ी।"),
        quiz("किसको asks…", ["who did it", "to whom", "whose", "which one"], 1, "किसको is the oblique ‘to whom’."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["किसने", "अभी तक", "कभी नहीं", "मैंने अभी तक नहीं पढ़ी"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("Questions and negatives with ने", [
        task("Ask with किसने.", ["this food — who made", "this letter — who wrote"],
             ["यह खाना किसने बनाया?", "यह चिट्ठी किसने लिखी?"]),
        task("Make each sentence negative.", ["मैंने फ़िल्म देखी।", "उसने मुझे बताया।"],
             ["मैंने फ़िल्म नहीं देखी।", "उसने मुझे नहीं बताया।"]),
        task("Translate into Hindi.", ["I have not eaten yet.", "Why did you not call?"],
             ["मैंने अभी तक खाना नहीं खाया।", "आपने फ़ोन क्यों नहीं किया?"]),
        task("Write a short dialogue: one person asks who did something, the other denies doing it.",
             ["ask who cleaned", "deny opening the window"],
             ["यह कमरा किसने साफ़ किया?", "मैंने खिड़की नहीं खोली।"]),
    ]),
})

# ── B1 · U2 · Commands and family ───────────────────────────────────────────
lesson("B1", "B1-U2", {
    "id": "B1-U2-L3",
    "title": "मत कीजिए — the kind way to say ‘don’t’",
    "learn": ("मत makes a command negative, and the polite इए ending keeps it friendly: चिंता मत कीजिए, "
              "जल्दी मत कीजिए, मेरी बात मत मानिए अगर आपको ठीक न लगे. In Hindi the softening comes from the "
              "verb form and from words like ज़रा and बिल्कुल, not from tone alone."),
    "vocab": [
        v("मत", "mat", "don’t (with a command)", "negative particle"),
        v("चिंता", "cintā", "worry, anxiety", "noun"),
        v("फ़िक्र", "fikr", "worry, concern", "noun"),
        v("जल्दी", "jaldī", "hurry; early", "noun/adverb"),
        v("बिल्कुल", "bilkul", "completely, at all", "adverb"),
        v("इतना", "itnā", "this much", "quantifier"),
        v("परेशान", "pareśān", "troubled, bothered", "adjective"),
        v("आराम", "ārām", "rest, comfort", "noun"),
    ],
    "grammar": {
        "title": "मत + इए (आप) · मत + ओ (तुम)",
        "explain": ("मत goes immediately before the verb, and the verb keeps the ending its respect level "
                    "demands: आप को — कीजिए / जाइए / बोलिए; तुम को — करो / जाओ / बोलो. The reassuring "
                    "phrases चिंता मत कीजिए and फ़िक्र मत कीजिए are fixed and are heard all day."),
        "pattern": "चिंता मत कीजिए · ज़रा भी मत सोचिए · आराम कीजिए",
        "examples": [
            ex("चिंता मत कीजिए, सब ठीक हो जाएगा।", "cintā mat kījie, sab ṭhīk ho jāegā.",
               "Do not worry, everything will be all right."),
            ex("इतनी जल्दी मत कीजिए, आराम से चलिए।", "itnī jaldī mat kījie, ārām se calie.",
               "Do not rush so much, walk comfortably."),
            ex("आप मेरी बात बुरा मत मानिए।", "āp merī bāt burā mat mānīe.", "Do not take my words badly."),
        ],
        "mistakes": [
            "मत with नहीं in the same command: चिंता नहीं कीजिए is not how the phrase runs — it is चिंता मत कीजिए।",
            "Forgetting the respect level: मत बोलो to an elder should be मत बोलिए।",
        ],
    },
    "dialogue": [
        line("मीरा", "माफ़ कीजिए, मुझे देर हो गई।", "māf kījie, mujhe der ho gaī.", "Sorry, I am late."),
        line("अध्यापक", "कोई बात नहीं। चिंता मत कीजिए, अभी शुरू ही हुआ है।", "koī bāt nahī̃. cintā mat kījie, abhī śurū hī huā hai.",
             "It is all right. Do not worry, it has only just started."),
        line("मीरा", "इतनी भीड़ क्यों है आज?", "itnī bhīṛ kyõ hai āj?", "Why is there such a crowd today?"),
        line("अध्यापक", "पता नहीं, पर जल्दी मत कीजिए — बैठिए, चाय पीजिए।", "patā nahī̃, par jaldī mat kījie — baithie, cāy pījie.",
             "No idea, but do not hurry — sit down, have some tea."),
    ],
    "practice": [
        p("multiple_choice", "Which is the polite way to say ‘don’t worry’ to an elder?",
          "चिंता मत कीजिए।", options=["चिंता मत कीजिए।", "चिंता मत करो।", "चिंता नहीं कर।", "चिंता मत नहीं कीजिए।"]),
        p("fill_in_the_blank", "चिंता ____ कीजिए, सब ठीक है। (don’t)", "मत"),
        p("translation", "Do not rush, please walk comfortably.", "जल्दी मत कीजिए, आराम से चलिए।"),
        p("reverse_translation", "आप मेरी बात बुरा मत मानिए।", "Do not take my words badly."),
        p("word_selection", "Which word makes a command negative without stopping its politeness?", "मत",
          options=["मत", "नहीं", "ना", "बिल्कुल"]),
        p("matching", "Match each phrase with its English.", "फ़िक्र मत कीजिए = do not worry",
          options=["चिंता मत कीजिए = do not worry", "जल्दी मत कीजिए = do not rush",
                   "आराम कीजिए = rest / take it easy", "बुरा मत मानिए = do not take it badly"]),
        p("reorder", "Put these in order: मत · चिंता · कीजिए", "चिंता मत कीजिए।"),
        p("sentence_building", "Build the sentence: ‘Do not take it badly, but I cannot come today.’",
          "बुरा मत मानिए, पर मैं आज नहीं आ सकता।"),
        p("error_correction", "Find the mistake: अंकल जी, चिंता मत करो।", "अंकल जी, चिंता मत कीजिए।"),
        p("dialogue_completion", "— मुझे देर हो गई, माफ़ कीजिए। — ____ (Do not worry, it is fine.)",
          "चिंता मत कीजिए, कोई बात नहीं।"),
        p("register_transformation", "Change this command from तुम to आप.", "जल्दी मत करो। → जल्दी मत कीजिए।"),
        p("roleplay", "Reassure a guest who has arrived late and is apologising.",
          "कोई बात नहीं, चिंता मत कीजिए। अंदर आइए, आराम कीजिए।"),
    ],
    "quiz": [
        quiz("Which word makes a Hindi command negative?", ["नहीं", "मत", "बिल्कुल", "ना"], 1,
             "नहीं negates statements; मत negates commands."),
        quiz("The respectful form of ‘do not go’ is…", ["मत जाओ", "मत जाइए", "मत जा", "नहीं जाना"], 1,
             "आप takes इए: मत जाइए।"),
        quiz("चिंता मत कीजिए means…", ["Do not worry.", "Do not go.", "Do not speak.", "Do not sit."], 0,
             "चिंता = worry; कीजिए = please do."),
        quiz("Which sentence mixes the two negatives wrongly?", ["चिंता मत कीजिए।", "जल्दी मत कीजिए।",
            "चिंता नहीं कीजिए।", "बुरा मत मानिए।"], 2,
             "A command takes मत, not नहीं."),
        quiz("आप मेरी बात बुरा मत मानिए is used when…",
             ["you are giving a gift", "you are saying something the listener may dislike",
              "you are thanking someone", "you are asking directions"], 1,
             "It softens a remark the listener might take badly."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["मत", "चिंता", "जल्दी", "चिंता मत कीजिए"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("Polite negatives", [
        task("Turn each order into a polite negative command.", ["जल्दी कीजिए।", "बोलिए।"],
             ["जल्दी मत कीजिए।", "मत बोलिए।"]),
        task("Write the Hindi for each reassuring phrase.", ["do not worry", "do not rush", "take it easy"],
             ["चिंता मत कीजिए।", "जल्दी मत कीजिए।", "आराम कीजिए।"]),
        task("Translate into Hindi.", ["Do not take my words badly.", "Do not be troubled, everything is fine."],
             ["आप मेरी बात बुरा मत मानिए।", "परेशान मत कीजिए, सब ठीक है।"]),
        task("Write three polite things you would say to a guest who arrives late.",
             ["apology accepted", "do not worry", "come in and sit"],
             ["कोई बात नहीं।", "चिंता मत कीजिए।", "अंदर आइए और बैठिए।"]),
    ]),
})

# ── B1 · U3 · Opinions and weather ──────────────────────────────────────────
lesson("B1", "B1-U3", {
    "id": "B1-U3-L3",
    "title": "सहमति और असहमति — agreeing without a fight",
    "learn": ("Hindi disagreement is usually built on agreement first: सही कहा आपने, लेकिन… Then the objection "
              "arrives. Softer than मैं असहमत हूँ are मुझे ऐसा नहीं लगता, मेरे ख़याल से यह ठीक नहीं, और "
              "एक बात कहूँ? — may I say one thing? To agree warmly: बिल्कुल सही, मैं आपसे पूरी तरह सहमत हूँ."),
    "vocab": [
        v("सहमत", "sahmat", "in agreement", "adjective"),
        v("असहमत", "asahmat", "in disagreement", "adjective"),
        v("ख़याल", "khayāl", "thought, opinion", "noun"),
        v("राय", "rāy", "opinion", "noun"),
        v("सही कहा", "sahī kahā", "you said it right", "phrase"),
        v("एक बात कहूँ?", "ek bāt kahū̃?", "may I say one thing?", "phrase"),
        v("दूसरी ओर", "dūsrī or", "on the other hand", "connector"),
        v("तो भी", "to bhī", "even then, still", "connector"),
    ],
    "grammar": {
        "title": "Agree, then turn: सही कहा, लेकिन…",
        "explain": ("A B1-level disagreement names what is right in the other view and then adds its own: "
                    "सही कहा आपने, लेकिन मेरे ख़याल से यह जल्दी हो जाएगा. The connectors हालाँकि, लेकिन और "
                    "दूसरी ओर do the turning, and मुझे लगता है keeps the claim personal rather than absolute."),
        "pattern": "सही कहा + लेकिन · मुझे ऐसा नहीं लगता कि · मेरे ख़याल से",
        "examples": [
            ex("सही कहा आपने, लेकिन मुझे ऐसा नहीं लगता कि यह ज़रूरी है।",
               "sahī kahā āpne, lekin mujhe aisā nahī̃ lagtā ki yah zarūrī hai.",
               "You are right, but I do not feel that it is necessary."),
            ex("मेरे ख़याल से हमें एक हफ़्ते और इंतज़ार करना चाहिए।",
               "mere khayāl se hamẽ ek hafte aur intzār karnā cāhie.",
               "In my opinion we should wait another week."),
            ex("दूसरी ओर यह भी सच है कि कीमत बढ़ रही है।",
               "dūsrī or yah bhī sac hai ki kīmat baṛh rahī hai.",
               "On the other hand it is also true that the price is rising."),
        ],
        "mistakes": [
            "Opening with आप ग़लत हैं — it is heard, but at B1 the polite shape is to name what is right first, then the difference.",
            "मुझे लगता है as a bare fact: मुझे लगता है कि… is a personal view, so quoting it later as proof reads oddly.",
        ],
    },
    "dialogue": [
        line("राहुल", "मेरे ख़याल से हमें मेट्रो से जाना चाहिए।", "mere khayāl se hamẽ meṭro se jānā cāhie.",
             "In my opinion we should go by metro."),
        line("मीरा", "सही कहा, लेकिन इस समय बहुत भीड़ होती है।", "sahī kahā, lekin is samay bahut bhīṛ hotī hai.",
             "True, but at this time it is very crowded."),
        line("राहुल", "दूसरी ओर टैक्सी में दुगना समय लगेगा।", "dūsrī or ṭāksī meṅ dugnā samay lagegā.",
             "On the other hand a taxi will take twice the time."),
        line("मीरा", "तो भी भीड़ में खड़े रहने से अच्छा है। चलिए, टैक्सी कर लें।",
             "to bhī bhīṛ meṅ khaṛe rahne se acchā hai. calie, ṭāksī kar lẽ.",
             "Even so, it is better than standing in the crowd. Come, let us take a taxi."),
    ],
    "practice": [
        p("multiple_choice", "Which opening disagrees politely?", "सही कहा आपने, लेकिन…",
          options=["सही कहा आपने, लेकिन…", "आप ग़लत हैं।", "नहीं, ऐसा नहीं है।", "यह बकवास है।"]),
        p("fill_in_the_blank", "मेरे ____ से हमें रुक जाना चाहिए। (opinion)", "ख़याल"),
        p("translation", "In my opinion we should wait another week.", "मेरे ख़याल से हमें एक हफ़्ते और इंतज़ार करना चाहिए।"),
        p("reverse_translation", "मुझे ऐसा नहीं लगता कि यह ज़रूरी है।", "I do not feel that it is necessary."),
        p("word_selection", "Which word means ‘agreement’?", "सहमत", options=["सहमत", "असहमत", "राय", "ख़याल"]),
        p("matching", "Match each connector with its function.", "दूसरी ओर = on the other hand",
          options=["लेकिन = but", "हालाँकि = although", "दूसरी ओर = on the other hand", "इसलिए = therefore"]),
        p("reorder", "Put these in order: लेकिन · कहा · सही · आपने", "सही कहा आपने, लेकिन…"),
        p("sentence_building", "Build the sentence: ‘You are right, but on the other hand it is expensive.’",
          "सही कहा आपने, लेकिन दूसरी ओर यह महँगा है।"),
        p("error_correction", "Find the mistake: मुझे लगता है कि यह ज़रूरी है, और आप ग़लत हैं।",
          "मुझे लगता है कि यह ज़रूरी है, लेकिन मैं आपकी बात समझता हूँ।"),
        p("dialogue_completion", "— मेरे ख़याल से आज ही काम ख़त्म करना चाहिए। — ____ (True, but it is very late.)",
          "सही कहा, लेकिन बहुत देर हो गई है।"),
        p("register_transformation", "Make this disagreement softer.", "मैं असहमत हूँ। → मुझे ऐसा नहीं लगता।"),
        p("guided_speaking", "Disagree with a friend’s plan in two sentences, starting with what is right about it.",
          "सही कहा, योजना अच्छी है, लेकिन समय कम है। मेरे ख़याल से हमें इसे अगले हफ़्ते करना चाहिए।"),
    ],
    "quiz": [
        quiz("Which phrase means ‘in my opinion’?", ["मेरे ख़याल से", "मुझे नहीं पता", "मेरे पास", "मेरे लिए"], 0,
             "मेरे ख़याल से introduces a personal view."),
        quiz("The polite way to disagree is…", ["आप ग़लत हैं।", "सही कहा आपने, लेकिन…", "ऐसा नहीं है।", "बिल्कुल नहीं।"], 1,
             "Name what is right first, then the difference."),
        quiz("दूसरी ओर means…", ["therefore", "although", "on the other hand", "in short"], 2,
             "It introduces the other side of an argument."),
        quiz("मुझे ऐसा नहीं लगता कि यह ज़रूरी है — the speaker is…",
             ["agreeing", "disagreeing", "asking a question", "thanking somebody"], 1,
             "ऐसा नहीं लगता states the speaker’s own different view."),
        quiz("Which connector means ‘although’?", ["इसलिए", "हालाँकि", "दूसरी ओर", "तो भी"], 1,
             "हालाँकि opens a concession."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["सहमत", "मेरे ख़याल से", "दूसरी ओर", "सही कहा आपने"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("Agreeing and disagreeing", [
        task("Write the Hindi for each phrase.", ["in my opinion", "you are right", "on the other hand", "even then"],
             ["मेरे ख़याल से", "सही कहा आपने", "दूसरी ओर", "तो भी"]),
        task("Soften each disagreement.", ["आप ग़लत हैं।", "यह बकवास है।"],
             ["मुझे ऐसा नहीं लगता।", "मेरे ख़याल से यह ठीक नहीं है।"]),
        task("Translate into Hindi.", ["In my opinion we should wait.", "You are right, but the price is rising."],
             ["मेरे ख़याल से हमें इंतज़ार करना चाहिए।", "सही कहा आपने, लेकिन कीमत बढ़ रही है।"]),
        task("Write four lines: agree, disagree, give a reason, and end with a way forward.",
             ["agree", "disagree", "reason", "way forward"],
             ["सही कहा आपने।", "लेकिन मुझे ऐसा नहीं लगता।", "क्योंकि समय कम है।", "चलिए, मिलकर तय करते हैं।"]),
    ]),
})

# ── B2 · U1 · Subjunctive and hypotheticals ─────────────────────────────────
lesson("B2", "B2-U1", {
    "id": "B2-U1-L3",
    "title": "शायद, हो सकता है, काश — the ladder of possibility",
    "learn": ("Hindi grades possibility rather than stating it flatly. At the top: ज़रूर होगा (it must be so). "
              "Below it: हो सकता है (it may be). Lower: शायद (maybe). And below the line, the regret that "
              "changes nothing: काश वह आता! — if only he came. Each rung takes a different verb form, and that "
              "is what makes the ladder worth learning."),
    "vocab": [
        v("शायद", "śāyad", "maybe, perhaps", "adverb"),
        v("हो सकता है", "ho saktā hai", "it is possible", "phrase"),
        v("ज़रूर", "zarūr", "certainly; must be", "adverb"),
        v("काश", "kāś", "if only (with regret)", "particle"),
        v("मुमकिन", "mumkin", "possible", "adjective"),
        v("उम्मीद", "ummed", "hope", "noun"),
        v("अंदाज़ा", "andāzā", "guess, estimate", "noun"),
        v("चांस", "cāns", "chance (colloquial, borrowed from English)", "noun"),
    ],
    "grammar": {
        "title": "एक ही बात, चार दर्जे की निश्चितता",
        "explain": ("Confidence runs through the form of होना and the subjunctive: ज़रूर होगा (future, "
                    "confident), हो सकता है (present, open), शायद … हो (subjunctive, doubtful), and काश + "
                    "subjunctive for a wish that is already lost. Note that शायद and हो सकता हैं are never "
                    "used together: one rung at a time."),
        "pattern": "ज़रूर होगा · हो सकता है · शायद जाए · काश जाता",
        "examples": [
            ex("वह अभी तक नहीं आया — शायद ट्रेन छूट गई।", "vah abhī tak nahī̃ āyā — śāyad ṭren chūṭ gaī.",
               "He has not arrived yet — perhaps he missed the train."),
            ex("हो सकता है कि कल बारिश हो।", "ho saktā hai ki kal bāriś ho.", "It may rain tomorrow."),
            ex("काश मैंने पहले पूछ लिया होता!", "kāś mainne pahle pūch liyā hotā!",
               "If only I had asked earlier!"),
        ],
        "mistakes": [
            "शायद हो सकता है — two hedges in one sentence; Hindi keeps one rung of certainty at a time.",
            "काश with the plain past: काश वह आया is heard in speech but the careful form is काश वह आता!, with the habitual form carrying the regret.",
        ],
    },
    "dialogue": [
        line("मीरा", "राहुल अभी तक नहीं पहुँचा।", "Rāhul abhī tak nahī̃ pahū̃cā.", "Rahul has not arrived yet."),
        line("अध्यापक", "शायद ट्रैफ़िक है। उसने कहा था कि वह नौ बजे निकलेगा।", "śāyad ṭraifik hai. usne kahā thā ki vah nau baje niklegā.",
             "Perhaps it is the traffic. He said he would leave at nine."),
        line("मीरा", "हो सकता है मीटिंग लंबी हो गई हो।", "ho saktā hai mīṭiṅg lambī ho gaī ho.",
             "It is possible the meeting ran long."),
        line("अध्यापक", "काश हमने उसे फ़ोन किया होता। चलिए, अब कर लेते हैं।",
             "kāś hamne use fon kiyā hotā. calie, ab kar lete hain.",
             "If only we had called him. Come, let us do it now."),
    ],
    "practice": [
        p("multiple_choice", "Which sentence expresses the strongest certainty?", "वह ज़रूर आएगा।",
          options=["वह ज़रूर आएगा।", "हो सकता है वह आए।", "शायद वह आए।", "काश वह आता!"]),
        p("fill_in_the_blank", "____ कल बारिश हो। (maybe)", "शायद"),
        p("translation", "It may rain tomorrow.", "हो सकता है कल बारिश हो।"),
        p("reverse_translation", "काश मैंने पहले पूछ लिया होता!", "If only I had asked earlier!"),
        p("word_selection", "Which word introduces a regret that cannot change?", "काश",
          options=["काश", "शायद", "ज़रूर", "मुमकिन"]),
        p("matching", "Match each expression with its level of certainty.", "हो सकता है = possible",
          options=["ज़रूर होगा = must be", "हो सकता है = possible", "शायद = maybe", "काश = if only"]),
        p("reorder", "Put these in order: हो · बारिश · सकता · कल · है", "हो सकता है कल बारिश हो।"),
        p("sentence_building", "Build the sentence: ‘Perhaps the train has left already.’",
          "शायद ट्रेन छूट गई है।"),
        p("error_correction", "Find the mistake: शायद हो सकता है वह आए।", "शायद वह आए।"),
        p("dialogue_completion", "— वह अभी तक नहीं आया। — ____ (Perhaps he missed the bus.)",
          "शायद उसकी बस छूट गई।"),
        p("inference", "काश हमने उसे फ़ोन किया होता — what does this tell you about the speaker’s view of the past?",
          "The speaker believes a call would have changed the outcome and regrets that it did not happen."),
        p("guided_composition", "Write one short paragraph about a plan that may or may not happen, using शायद, हो सकता है and ज़रूर once each.",
          "शायद हम कल जल्दी निकलेंगे। हो सकता है बारिश हो जाए। लेकिन अगर सब ठीक रहा, तो हम शाम तक ज़रूर पहुँच जाएँगे।"),
    ],
    "quiz": [
        quiz("Which pair expresses doubt BEFORE it expresses confidence?", ["ज़रूर होगा", "हो सकता है", "पक्का है", "निश्चित है"],
             1, "हो सकता है leaves the outcome open."),
        quiz("काश …! expresses…", ["a certainty", "a regret or wish", "a command", "a question"], 1,
             "काश introduces a wish, usually for something that did not happen."),
        quiz("Complete correctly: हो सकता है वह कल ____।", ["आया", "आए", "आता", "आएगा"], 1,
             "After हो सकता है the verb is subjunctive: आए।"),
        quiz("शायद does NOT combine with…", ["ट्रेन", "हो सकता है", "कल", "वह"], 1,
             "One hedge per sentence — शायद हो सकता है doubles the same doubt awkwardly."),
        quiz("‘It must be so’ is…", ["शायद हो", "हो सकता है", "ज़रूर होगा", "काश होता"], 2,
             "ज़रूर होगा states strong confidence."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["शायद", "हो सकता है", "ज़रूर", "काश"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("The possibility ladder", [
        task("Rank these from least to most certain.", ["ज़रूर होगा", "हो सकता है", "शायद"],
             ["शायद", "हो सकता है", "ज़रूर होगा"]),
        task("Write the Hindi for each.", ["maybe", "it is possible", "certainly", "if only"],
             ["शायद", "हो सकता है", "ज़रूर", "काश"]),
        task("Translate into Hindi.", ["Perhaps he missed the train.", "If only we had called earlier!"],
             ["शायद उसकी ट्रेन छूट गई।", "काश हमने पहले फ़ोन किया होता!"]),
        task("Write three sentences about tomorrow: one certain, one possible, one doubtful.",
             ["certain", "possible", "doubtful"],
             ["कल मैं ज़रूर जाऊँगा।", "हो सकता है बारिश हो।", "शायद समय नहीं मिले।"]),
    ]),
})

# ── B2 · U2 · Passive and debate ────────────────────────────────────────────
lesson("B2", "B2-U2", {
    "id": "B2-U2-L3",
    "title": "सच तो यह है कि — conceding, then holding your ground",
    "learn": ("A B2 argument concedes before it pushes: कोई शक नहीं कि… मगर (no doubt that… but); "
              "सच तो यह है कि (the truth is that); यह सही है, लेकिन सवाल यह है कि… (that is right, but the "
              "question is…). Conceding is not giving in — it moves the argument to the point you actually "
              "want to defend, and the passive keeps the claim impersonal."),
    "vocab": [
        v("कोई शक नहीं", "koī śak nahī̃", "there is no doubt", "phrase"),
        v("मगर", "magar", "but (a shade stronger than लेकिन)", "connector"),
        v("सच तो यह है", "sac to yah hai", "the truth is", "phrase"),
        v("सवाल यह है", "savāl yah hai", "the question is", "phrase"),
        v("दलील", "dalīl", "argument", "noun"),
        v("सबूत", "sabūt", "evidence, proof", "noun"),
        v("निष्कर्ष", "niṣkarṣ", "conclusion", "noun"),
        v("इनकार", "inkār", "refusal, denial", "noun"),
    ],
    "grammar": {
        "title": "रियायत + दलील: कोई शक नहीं कि… मगर…",
        "explain": ("The concession is a full clause with कि; the counter-claim follows मगर or लेकिन and is "
                    "often impersonal: यह माना जाता है कि… (it is accepted that…), कहा जाता है कि… (it is said "
                    "that…). Ending with इसलिए or निष्कर्ष में signals the conclusion the argument has earned."),
        "pattern": "कोई शक नहीं कि X, मगर Y · सच तो यह है कि Z · निष्कर्ष में…",
        "examples": [
            ex("कोई शक नहीं कि यह योजना अच्छी है, मगर इसका ख़र्च बहुत है।",
               "koī śak nahī̃ ki yah yojnā acchī hai, magar iskā kharc bahut hai.",
               "There is no doubt the plan is good, but it costs a great deal."),
            ex("सच तो यह है कि हमारे पास सबूत कम हैं।",
               "sac to yah hai ki hamāre pās sabūt kam hain.",
               "The truth is that we have little evidence."),
            ex("यह सही है, लेकिन सवाल यह है कि समय कितना बचा है।",
               "yah sahī hai, lekin savāl yah hai ki samay kitnā bacā hai.",
               "That is right, but the question is how much time is left."),
        ],
        "mistakes": [
            "मगर and लेकिन swapped at random: both are correct, but मगर lands harder and usually follows a concession.",
            "Using the passive to dodge the doer when the doer matters: सबूत नहीं दिए गए hides who failed to give them, and a debate partner will ask.",
        ],
    },
    "dialogue": [
        line("मीरा", "यह योजना महँगी है, मगर ज़रूरी है।", "yah yojnā mahãgī hai, magar zarūrī hai.",
             "This plan is expensive, but it is necessary."),
        line("राहुल", "कोई शक नहीं कि यह ज़रूरी है। सवाल यह है कि पैसा कहाँ से आएगा।",
             "koī śak nahī̃ ki yah zarūrī hai. savāl yah hai ki paisā kahā̃ se āegā.",
             "There is no doubt it is necessary. The question is where the money will come from."),
        line("मीरा", "सच तो यह है कि पिछले साल का बजट बचा हुआ है।", "sac to yah hai ki pichle sāl kā bajat bacā huā hai.",
             "The truth is that last year’s budget is unspent."),
        line("राहुल", "तो निष्कर्ष यह है कि नई मंज़ूरी की ज़रूरत नहीं है।", "to niṣkarṣ yah hai ki naī manzūrī kī zarūrat nahī̃ hai.",
             "Then the conclusion is that no new approval is needed."),
    ],
    "practice": [
        p("multiple_choice", "Which phrase concedes a point before arguing against it?",
          "कोई शक नहीं कि… मगर…", options=["कोई शक नहीं कि… मगर…", "यह बकवास है।", "मुझे नहीं पता।",
          "मुझे यह पसंद नहीं है।"]),
        p("fill_in_the_blank", "सच तो यह ____ कि हमारे पास समय कम है। (is)", "है"),
        p("translation", "There is no doubt that the plan is good, but it costs too much.",
          "कोई शक नहीं कि योजना अच्छी है, मगर ख़र्च बहुत है।"),
        p("reverse_translation", "सवाल यह है कि हम कब शुरू करेंगे।", "The question is when we will start."),
        p("word_selection", "Which word means ‘evidence’?", "सबूत", options=["सबूत", "दलील", "निष्कर्ष", "इनकार"]),
        p("matching", "Match each term with its role in an argument.", "निष्कर्ष = conclusion",
          options=["दलील = argument", "सबूत = evidence", "रियायत = concession", "निष्कर्ष = conclusion"]),
        p("reorder", "Put these in order: यह · लेकिन · है · सही · सवाल", "यह सही है, लेकिन सवाल…"),
        p("sentence_building", "Build the sentence: ‘The truth is that we have little evidence.’",
          "सच तो यह है कि हमारे पास सबूत कम हैं।"),
        p("error_correction", "Find the mistake: सच तो यह है कि हमारे पास सबूत कम है ना।",
          "सच तो यह है कि हमारे पास सबूत कम हैं।"),
        p("dialogue_completion", "— यह योजना बहुत महँगी है। — ____ (No doubt, but the question is where the money will come from.)",
          "कोई शक नहीं, मगर सवाल यह है कि पैसा कहाँ से आएगा।"),
        p("passive", "Rewrite impersonally: ‘People say the plan is ready.’ → …",
          "कहा जाता है कि योजना तैयार है।"),
        p("argument_construction", "Write four lines: concede a point, state the real question, give evidence, conclude.",
          "कोई शक नहीं कि योजना अच्छी है। सवाल यह है कि ख़र्च कौन उठाएगा। पिछले साल का बजट बचा हुआ है, इसलिए नई मंज़ूरी की ज़रूरत नहीं है। निष्कर्ष यह है कि काम अभी शुरू हो सकता है।"),
    ],
    "quiz": [
        quiz("Which phrase introduces a concession?", ["इसलिए", "कोई शक नहीं कि", "निष्कर्ष में", "इसके अलावा"], 1,
             "कोई शक नहीं कि grants the other side’s point before the counter-claim."),
        quiz("सवाल यह है कि means…", ["the answer is", "the question is", "the problem is solved", "in short"], 1,
             "It names the point still open."),
        quiz("Which is a passive construction?", ["यह कहा जाता है।", "यह कहता है।", "यह कह रहा है।", "यह कहेगा।"], 0,
             "कहा जाता है is impersonal: it is said."),
        quiz("मगर differs from लेकिन in that…", ["it is wrong", "it lands a little harder and follows a concession",
            "it means therefore", "it is only for questions"], 1, "Both are correct; मगर carries more contrast."),
        quiz("The strongest place for your conclusion in a Hindi argument is…",
             ["the first line", "the middle", "the end, after the concession and evidence", "it must be repeated twice"], 2,
             "Hindi argument writing builds to the conclusion rather than opening with it."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["मगर", "सबूत", "दलील", "कोई शक नहीं"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("Concede and argue", [
        task("Write the Hindi for each phrase.", ["no doubt", "but", "the truth is", "conclusion"],
             ["कोई शक नहीं", "मगर", "सच तो यह है", "निष्कर्ष"]),
        task("Turn each blunt claim into a concession plus objection.", ["यह योजना बेकार है।", "यह काम जल्दी हो जाएगा।"],
             ["कोई शक नहीं कि योजना में कमियाँ हैं, मगर यह ज़रूरी है।",
              "यह सही है, लेकिन सवाल यह है कि समय कितना है।"]),
        task("Write each sentence in the impersonal passive.", ["लोग कहते हैं कि योजना तैयार है।", "लोग मानते हैं कि यह ठीक है।"],
             ["कहा जाता है कि योजना तैयार है।", "माना जाता है कि यह ठीक है।"]),
        task("Write a five-line argument: concession, question, evidence, objection, conclusion.",
             ["concession", "question", "evidence", "objection", "conclusion"],
             ["कोई शक नहीं कि यह ज़रूरी है।", "सवाल यह है कि ख़र्च कौन उठाएगा।",
              "पिछले साल का बजट बचा हुआ है।", "मगर मंज़ूरी अभी नहीं मिली।",
              "निष्कर्ष यह है कि पहले मंज़ूरी लेनी होगी।"]),
    ]),
})

# ── B2 · U3 · Culture and mastery ───────────────────────────────────────────
lesson("B2", "B2-U3", {
    "id": "B2-U3-L3",
    "title": "मुहावरे बोलचाल में — idioms that sound earned",
    "learn": ("A Hindi idiom used correctly does the work of a whole sentence: उसकी बात सुनकर मेरे मुँह में पानी "
              "आ गया is warmer than मुझे बहुत अच्छा लगा. But an idiom used at the wrong moment sounds borrowed. "
              "The rule is register first: muhavare belong in conversation and informal writing, not in a "
              "report — and never two in one sentence."),
    "vocab": [
        v("मुहावरा", "muhāvarā", "idiom", "noun"),
        v("मुँह में पानी आना", "mū̃h meṅ pānī ānā", "to feel a craving (literally: water comes to the mouth)", "idiom"),
        v("हाथ मलना", "hāth malnā", "to regret (literally: to rub the hands)", "idiom"),
        v("आँखों का तारा", "āṅkhõ kā tārā", "the apple of one’s eye", "idiom"),
        v("दाल में कुछ काला है", "dāl meṅ kuch kālā hai", "something is fishy", "idiom"),
        v("चार चाँद लगाना", "cār cā̃d lagānā", "to make something much finer", "idiom"),
        v("अंधे की लाठी", "andhe kī lāṭhī", "someone’s only support", "idiom"),
        v("घोड़े बेचकर सोना", "ghoṛe beckar sonā", "to sleep untroubled", "idiom"),
    ],
    "grammar": {
        "title": "मुहावरा = स्थिति + रूप",
        "explain": ("An idiom carries its own grammar and its own situation. मुँह में पानी आना takes the "
                    "मुँह … में frame and the thing craved takes का: खाने का नाम सुनकर मुँह में पानी आ गया. "
                    "चार चाँद लगाना needs a thing and a addressee: आपके आने से समारोह को चार चाँद लग गए. "
                    "Learn the frame with the idiom, or it will sound translated."),
        "pattern": "स्थिति + मुहावरा (एक वाक्य में एक) · औपचारिक लेखन में नहीं",
        "examples": [
            ex("इस समारोह में आपके आने से चार चाँद लग गए।", "is samāroh meṅ āpke āne se cār cā̃d lag gae.",
               "Your coming added four moons to this function."),
            ex("मुझे उस दिन कुछ नहीं मिला और मैं हाथ मलता रह गया।",
               "mujhe us din kuch nahī̃ milā aur main hāth maltā rah gayā.",
               "That day I got nothing and was left regretting it."),
            ex("वह अपनी माँ की आँखों का तारा है।", "vah apnī mā̃ kī āṅkhõ kā tārā hai.",
               "He is the apple of his mother’s eye."),
        ],
        "mistakes": [
            "Two idioms in one sentence — मुँह में पानी आ गया और मैं हाथ मलता रह गया describes two opposite feelings and overloads the line.",
            "Using an idiom in a formal report: a school newsletter prints उल्लेखनीय सहयोग, not चार चाँद लग गए.",
        ],
    },
    "dialogue": [
        line("मीरा", "मिठाई का नाम सुना तो मेरे मुँह में पानी आ गया।", "miṭhāī kā nām sunā to mere mū̃h meṅ pānī ā gayā.",
             "The moment I heard ‘sweets’, I started craving them."),
        line("राहुल", "और मैंने सुना कि दुकान बंद हो गई — तब मैं हाथ मलता रह गया।",
             "aur mainne sunā ki dukān band ho gaī — tab main hāth maltā rah gayā.",
             "And I heard the shop had closed — then I was left regretting it."),
        line("मीरा", "कोई बात नहीं। माँ ने घर पर बनाई है।", "koī bāt nahī̃. mā̃ ne ghar par banāī hai.",
             "Never mind. Mother has made some at home."),
        line("राहुल", "तो चलिए! आपके आने से खाने को चार चाँद लग जाएँगे।",
             "to calie! āpke āne se khāne ko cār cā̃d lag jāẽge.",
             "Then let us go! Your coming will put four moons on the meal."),
    ],
    "practice": [
        p("multiple_choice", "Which idiom means ‘to regret’?", "हाथ मलना",
          options=["हाथ मलना", "मुँह में पानी आना", "चार चाँद लगाना", "आँखों का तारा"]),
        p("fill_in_the_blank", "मिठाई का नाम सुनकर मेरे ____ में पानी आ गया। (mouth)", "मुँह"),
        p("translation", "He is the apple of his mother’s eye.", "वह अपनी माँ की आँखों का तारा है।"),
        p("reverse_translation", "आपके आने से समारोह को चार चाँद लग गए।",
          "Your coming made the function much finer."),
        p("word_selection", "Which idiom says something is suspicious?", "दाल में कुछ काला है",
          options=["दाल में कुछ काला है", "अंधे की लाठी", "घोड़े बेचकर सोना", "हाथ मलना"]),
        p("matching", "Match each idiom with its meaning.", "अंधे की लाठी = somebody’s only support",
          options=["मुँह में पानी आना = to crave", "हाथ मलना = to regret",
                   "अंधे की लाठी = somebody’s only support", "घोड़े बेचकर सोना = to sleep untroubled"]),
        p("reorder", "Put these in order: आ गया · पानी · मुँह में · मेरे", "मेरे मुँह में पानी आ गया।"),
        p("sentence_building", "Build the sentence: ‘Something is fishy about this deal.’",
          "इस सौदे में दाल में कुछ काला है।"),
        p("error_correction", "Find the mistake: मेरे मुँह का पानी आ गया।", "मेरे मुँह में पानी आ गया।"),
        p("dialogue_completion", "— दुकान बंद हो गई, कुछ नहीं मिला। — ____ (I was left regretting it.)",
          "मैं हाथ मलता रह गया।"),
        p("register_transformation", "Rewrite formally, without the idiom: आपके आने से समारोह को चार चाँद लग गए।",
          "आपके आने से समारोह की शोभा बढ़ गई।"),
        p("idiom_interpretation", "Explain in your own words what घोड़े बेचकर सोना implies about someone’s state of mind.",
          "It means sleeping completely untroubled, as if nothing is left to lose or worry about."),
    ],
    "quiz": [
        quiz("मुँह में पानी आना describes…", ["anger", "craving", "regret", "fear"], 1,
             "It is the sensation of wanting something you can almost taste."),
        quiz("Which idiom fits somebody who is the only support of a family member?",
             ["चार चाँद लगाना", "अंधे की लाठी", "हाथ मलना", "दाल में कुछ काला है"], 1,
             "अंधे की लाठी is the support somebody cannot do without."),
        quiz("The correct frame is…", ["मुँह का पानी आना", "मुँह में पानी आना", "मुँह पर पानी आना", "मुँह से पानी आना"], 1,
             "The idiom is fixed: मुँह में पानी आना."),
        quiz("Idioms are usually misplaced in…", ["a conversation with friends", "a letter to a friend",
             "an official report", "a family story"], 2, "Formal writing prefers plain, unidiomatic wording."),
        quiz("घोड़े बेचकर सोना means…", ["to sleep badly", "to sell a horse", "to sleep untroubled",
             "to work all night"], 2, "It implies sleeping with nothing left to worry about."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["मुहावरा", "हाथ मलना", "आँखों का तारा", "चार चाँद लगाना"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("Idioms in your own sentences", [
        task("Write the meaning of each idiom in English.", ["मुँह में पानी आना", "हाथ मलना", "अंधे की लाठी"],
             ["to crave something", "to regret", "somebody’s only support"]),
        task("Use each idiom in a sentence of your own.", ["दाल में कुछ काला है", "चार चाँद लगाना"],
             ["इस प्रस्ताव में दाल में कुछ काला है।", "आपके आने से कार्यक्रम को चार चाँद लग गए।"]),
        task("Rewrite each idiom sentence in plain formal Hindi.",
             ["मैं हाथ मलता रह गया।", "वह अपनी माँ की आँखों का तारा है।"],
             ["मुझे बाद में पछतावा हुआ।", "वह अपनी माँ का सबसे प्रिय है।"]),
        task("Write a four-line conversation using exactly one idiom, correctly.",
             ["craving", "shop closed", "reassurance", "invitation"],
             ["मिठाई का नाम सुनकर मेरे मुँह में पानी आ गया।", "दुकान बंद हो गई।",
              "कोई बात नहीं, घर पर बनी है।", "तो चलिए!"]),
    ]),
})

# ── C1 · U1 · Discourse and Institutional Control ───────────────────────────
lesson("C1", "hi-c1-u1", {
    "id": "C1-U1-L3",
    "title": "सभा और प्रस्ताव — the language of deliberation",
    "learn": ("Institutional Hindi has a procedural register of its own: कोई बिंदु उठाना (to raise a point), "
              "चर्चा के लिए रखना (to place before discussion), प्रस्ताव रखा जाता है (a proposal is moved), "
              "सर्वसम्मति से (by consensus), मतदान द्वारा (by vote). Procedural Hindi prefers the impersonal "
              "passive and the nominal style, which is exactly why it is worth practising as a genre rather than "
              "picking up phrase by phrase."),
    "vocab": [
        v("सभा", "sabhā", "meeting, assembly", "noun"),
        v("बिंदु उठाना", "bindu uṭhānā", "to raise a point", "collocation"),
        v("कार्यसूची", "kāryasūcī", "agenda", "noun"),
        v("प्रस्ताव", "prastāv", "proposal, motion", "noun"),
        v("सर्वसम्मति", "sarvasammati", "unanimity, consensus", "noun"),
        v("मतदान", "matadān", "voting", "noun"),
        v("कार्यवृत्त", "kāryavṛtt", "minutes of a meeting", "noun"),
        v("स्थगित करना", "sthagit karnā", "to adjourn, to defer", "verb"),
    ],
    "grammar": {
        "title": "प्रक्रिया का निष्पersonal रूप",
        "explain": ("Procedural Hindi states the act, not the actor: प्रस्ताव रखा गया, निर्णय स्थगित कर दिया गया, "
                    "चर्चा के बाद सर्वसम्मति से स्वीकार किया गया. When a name must be recorded, the minute keeps "
                    "the doer but in the third person and with the full designation: अध्यक्ष महोदय ने सूचित किया कि… "
                    "The register lives in the verb form; changing it changes the genre."),
        "pattern": "… प्रस्ताव रखा गया · सर्वसम्मति से स्वीकार किया गया · कार्यवृत्त में दर्ज किया जाए",
        "examples": [
            ex("बैठक की शुरुआत में पिछले कार्यवृत्त को सर्वसम्मति से स्वीकृति दी गई।",
               "baiṭhak kī śurūāt meṅ pichle kāryavṛtt ko sarvasammati se svīkṛti dī gaī.",
               "At the start of the meeting the previous minutes were approved unanimously."),
            ex("सदस्य ने कार्यसूची में एक नया बिंदु जोड़ने का सुझाव दिया।",
               "sadasy ne kāryasūcī meṅ ek nayā bindu joṛne kā sujhāv diyā.",
               "A member suggested adding a new point to the agenda."),
            ex("धनराशि के अभाव में यह प्रस्ताव स्थगित कर दिया गया।",
               "dhanrāśi ke abhāv meṅ yah prastāv sthagit kar diyā gayā.",
               "For want of funds the proposal was deferred."),
        ],
        "mistakes": [
            "मैंने कहा कि… in minutes — the record prefers अध्यक्ष ने सूचित किया कि…; the first reads as personal, the second as a record.",
            "Mixing the register mid-page: सर्वसम्मति से स्वीकार किया गया followed by सब ने हाँ कह दी breaks the genre in one line.",
        ],
    },
    "dialogue": [
        line("अध्यक्ष", "कार्यसूची के तीसरे बिंदु पर चर्चा आरंभ की जाती है।", "kāryasūcī ke tīsre bindu par carcā ārambh kī jātī hai.",
             "Discussion on the third point on the agenda begins."),
        line("सदस्य", "मैं एक बिंदु उठाना चाहूँगा — इसका बजट अभी तय नहीं है।", "main ek bindu uṭhānā cāhū̃gā — iskā bajat abhī tay nahī̃ hai.",
             "I would like to raise a point — its budget is not settled yet."),
        line("अध्यक्ष", "उचित है। क्या यह प्रस्ताव अगली बैठक तक स्थगित किया जाए?", "ucit hai. kyā yah prastāv aglī baiṭhak tak sthagit kiyā jāe?",
             "Fair. Should the proposal be deferred to the next meeting?"),
        line("सदस्य", "जी, सर्वसम्मति से। कार्यवृत्त में यही दर्ज कीजिए।", "jī, sarvasammati se. kāryavṛtt meṅ yahī darj kījie.",
             "Yes, unanimously. Please record exactly that in the minutes."),
    ],
    "practice": [
        p("multiple_choice", "Which line belongs in the minutes, not in the conversation?",
          "यह प्रस्ताव सर्वसम्मति से स्वीकार किया गया।",
          options=["यह प्रस्ताव सर्वसम्मति से स्वीकार किया गया।", "सब ने हाँ कह दी।",
                   "सबको यह ठीक लगा।", "कोई नहीं बोला, तो मान लिया।"]),
        p("fill_in_the_blank", "धनराशि के अभाव में प्रस्ताव ____ कर दिया गया। (deferred)", "स्थगित"),
        p("translation", "A member raised a new point on the agenda.", "एक सदस्य ने कार्यसूची में नया बिंदु उठाया।"),
        p("reverse_translation", "पिछले कार्यवृत्त को सर्वसम्मति से स्वीकृति दी गई।",
          "The previous minutes were approved unanimously."),
        p("word_selection", "Which word means the written record of a meeting?", "कार्यवृत्त",
          options=["कार्यवृत्त", "कार्यसूची", "प्रस्ताव", "मतदान"]),
        p("matching", "Match each procedural term with its meaning.", "कार्यसूची = the agenda",
          options=["कार्यवृत्त = the minutes", "कार्यसूची = the agenda", "प्रस्ताव = a motion",
                   "मतदान = voting"]),
        p("reorder", "Put these in order: स्वीकार · सर्वसम्मति से · किया गया", "सर्वसम्मति से स्वीकार किया गया।"),
        p("sentence_building", "Build the minute line: ‘The proposal was deferred for want of funds.’",
          "धनराशि के अभाव में प्रस्ताव स्थगित कर दिया गया।"),
        p("error_correction", "Find the register error: पिछले कार्यवृत्त सब ने मंज़ूर कर दिए।",
          "पिछले कार्यवृत्त को सर्वसम्मति से स्वीकृति दी गई।"),
        p("dialogue_completion", "— इस बिंदु पर क्या निर्णय हुआ? — ____ (The discussion was adjourned to the next meeting.)",
          "चर्चा अगली बैठक तक स्थगित कर दी गई।"),
        p("register_transformation", "Recast this spoken line as a minute.",
          "सब ने कहा कि यह ठीक है, तो हमने मंज़ूर कर लिया। → यह प्रस्ताव सर्वसम्मति से स्वीकृत किया गया।"),
        p("guided_composition", "Write three minutes lines: an item opened, a suggestion made, a decision taken.",
          "कार्यसूची का दूसरा बिंदु खोला गया। एक सदस्य ने सुझाव दिया कि तिथि बदली जाए। अंत में यह सुझाव स्वीकृत किया गया।"),
    ],
    "quiz": [
        quiz("Which verb form is typical of minutes?", ["सब ने कहा", "निर्णय किया गया", "हमने सोचा", "मुझे लगा"], 1,
             "Minutes prefer the impersonal passive: निर्णय किया गया."),
        quiz("सर्वसम्मति से means…", ["by a majority", "unanimously", "after a vote", "by the chairman"], 1,
             "It records that no one dissented."),
        quiz("कार्यसूची is…", ["the minutes", "the agenda", "the motion", "the quorum"], 1,
             "The agenda lists the items; the minutes record what happened to them."),
        quiz("The correct formal recast of ‘I said the budget is not fixed’ in minutes is…",
             ["मैंने कहा कि बजट तय नहीं है।", "सदस्य ने सूचित किया कि बजट अभी तय नहीं है।",
              "बजट तय नहीं है ना।", "बजट का क्या हुआ?"], 1,
             "The record names the role, keeps the third person, and uses the neutral verb."),
        quiz("Which sentence breaks the procedural register?", ["प्रस्ताव रखा गया।", "चर्चा स्थगित की गई।",
            "सबने हाँ कह दी।", "कार्यवृत्त को स्वीकृति दी गई।"], 2,
             "It shifts to a conversational construction mid-record."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["कार्यवृत्त", "प्रस्ताव", "सर्वसम्मति", "स्थगित करना"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("Minutes and motions", [
        task("Write the Hindi for each term.", ["agenda", "minutes", "motion", "unanimously"],
             ["कार्यसूची", "कार्यवृत्त", "प्रस्ताव", "सर्वसम्मति से"]),
        task("Turn each spoken line into a minute.", ["सबने यह ठीक कहा।", "हमने अगली बैठक तक रोक दिया।"],
             ["यह उचित माना गया।", "यह बिंदु अगली बैठक तक स्थगित कर दिया गया।"]),
        task("Translate into formal Hindi.", ["A new point was raised on the agenda.",
             "The proposal was approved unanimously."],
             ["कार्यसूची में एक नया बिंदु उठाया गया।", "प्रस्ताव सर्वसम्मति से स्वीकृत किया गया।"]),
        task("Write a four-line minute: item opened, point raised, objection noted, decision taken.",
             ["opened", "point", "objection", "decision"],
             ["कार्यसूची का पहला बिंदु खोला गया।", "एक सदस्य ने बजट का बिंदु उठाया।",
              "आपत्ति दर्ज की गई कि धनराशि अपर्याप्त है।", "निर्णय अगली बैठक तक स्थगित किया गया।"]),
    ]),
})

# ── C1 · U2 · Academic and Figurative Control ───────────────────────────────
lesson("C1", "hi-c1-u2", {
    "id": "C1-U2-L3",
    "title": "निबंध की रूपरेखा — प्रस्तावना से उपसंहार तक",
    "learn": ("Academic Hindi writing has a visible shape: प्रस्तावना (the frame and the question), पक्ष (the "
              "case), प्रति-तर्क (the strongest objection, stated fairly), खंडन (the reply), उपसंहार (what "
              "follows from it). A reader who cannot find those five moves in your paragraph has to construct "
              "your argument for you — and will get it wrong."),
    "vocab": [
        v("प्रस्तावना", "prastāvanā", "introduction, preface", "noun"),
        v("पक्ष", "pakṣ", "the case for, a side", "noun"),
        v("प्रति-तर्क", "prati-tark", "counter-argument", "noun"),
        v("खंडन", "khaṇḍan", "rebuttal, refutation", "noun"),
        v("उपसंहार", "upsaṅhār", "conclusion, epilogue", "noun"),
        v("तर्कसंगत", "tarkasaṅgat", "logically consistent", "adjective"),
        v("सीमा", "sīmā", "limit, scope boundary", "noun"),
        v("अपवाद", "apavād", "exception", "noun"),
    ],
    "grammar": {
        "title": "रूपरेखा के पाँच चरण और उनकी भाषा",
        "explain": ("Each move has a signature construction: framing (यह लेख इस प्रश्न पर केंद्रित है कि…), "
                    "claiming (उपलब्ध साक्ष्य यह दर्शाते हैं कि…), conceding (यह सही है कि…, फिर भी…), replying "
                    "(परंतु इस तर्क की सीमा यह है कि…), concluding (इससे यह निष्कर्ष निकलता है कि…). The "
                    "constructions are conventional, and the control is in choosing which one carries which move."),
        "pattern": "यह लेख … पर केंद्रित है → साक्ष्य दर्शाते हैं → यह माना जाना चाहिए → परंतु सीमा यह है → निष्कर्ष",
        "examples": [
            ex("यह लेख इस प्रश्न पर केंद्रित है कि नीति का प्रभाव किन वर्गों पर पड़ा।",
               "yah lekh is praśn par kendrit hai ki nīti kā prabhāv kin vargõ par paṛā.",
               "This paper focuses on the question of which groups the policy affected."),
            ex("यह सही है कि आँकड़े सीमित हैं, फिर भी इनसे एक स्पष्ट प्रवृत्ति दिखती है।",
               "yah sahī hai ki ā̃kṛe sīmit hain, phir bhī inse ek spaṣṭ pravṛtti dikhtī hai.",
               "It is true that the data are limited, yet they show a clear trend."),
            ex("इससे यह निष्कर्ष निकलता है कि नीति का असर समान नहीं रहा।",
               "isse yah niṣkarṣ nikalta hai ki nīti kā asar samān nahī̃ rahā.",
               "From this it follows that the policy’s effect was not uniform."),
        ],
        "mistakes": [
            "An essay with a claim but no प्रति-तर्क: the strongest objection must be stated better than its opponents would, or the argument reads as advocacy.",
            "Concluding with a new claim — उपसंहार may only draw out what the argument already established.",
        ],
    },
    "dialogue": [
        line("समीक्षक", "आपके लेख का पक्ष स्पष्ट है, पर प्रति-तर्क कहाँ है?", "āpke lekh kā pakṣ spaṣṭ hai, par prati-tark kahā̃ hai?",
             "Your paper’s case is clear, but where is the counter-argument?"),
        line("लेखक", "दूसरे खंड में — वहाँ मैंने सबसे मज़बूत आपत्ति दर्ज की है।", "dūsre khaṇḍ meṅ — vahā̃ mainne sabse mazbūt āpatti darj kī hai.",
             "In the second section — I have recorded the strongest objection there."),
        line("समीक्षक", "और उपसंहार में?", "aur upsaṅhār meṅ?", "And in the conclusion?"),
        line("लेखक", "उपसंहार में केवल वही, जो तर्क से निकलता है — और एक सीमा स्पष्ट की है।",
             "upsaṅhār meṅ keval vahī, jo tark se nikalta hai — aur ek sīmā spaṣṭ kī hai.",
             "Only what follows from the argument — and I have stated one limitation."),
    ],
    "practice": [
        p("multiple_choice", "Which sentence states a limitation rather than a claim?",
          "इस अध्ययन की सीमा यह है कि आँकड़े एक ही वर्ष के हैं।",
          options=["इस अध्ययन की सीमा यह है कि आँकड़े एक ही वर्ष के हैं।",
                   "यह अध्ययन निर्णायक है।", "इससे यह सिद्ध होता है कि…", "सब जानते हैं कि…"]),
        p("fill_in_the_blank", "इससे यह ____ निकलता है कि नीति का असर समान नहीं रहा। (conclusion)", "निष्कर्ष"),
        p("translation", "It is true that the data are limited, yet they show a clear trend.",
          "यह सही है कि आँकड़े सीमित हैं, फिर भी इनसे एक स्पष्ट प्रवृत्ति दिखती है।"),
        p("reverse_translation", "परंतु इस तर्क की सीमा यह है कि यह अपवादों की उपेक्षा करता है।",
          "But the limit of this argument is that it ignores the exceptions."),
        p("word_selection", "Which term names the strongest objection stated fairly?", "प्रति-तर्क",
          options=["प्रति-तर्क", "खंडन", "उपसंहार", "प्रस्तावना"]),
        p("matching", "Match each move with its Hindi term.", "खंडन = the reply to the objection",
          options=["प्रस्तावना = the framing", "पक्ष = the case", "प्रति-तर्क = the objection",
                   "खंडन = the reply to the objection"]),
        p("reorder", "Put these in order: निकलता है · निष्कर्ष · यह · कि", "इससे यह निष्कर्ष निकलता है कि…"),
        p("sentence_building", "Build the concession: ‘It is true that the sample is small, yet the pattern holds.’",
          "यह सही है कि नमूना छोटा है, फिर भी प्रवृत्ति बनी रहती है।"),
        p("error_correction", "Find the error of argument, not grammar: इसलिए हमें यह नीति तुरंत बदल देनी चाहिए — लेखक ने कोई सीमा नहीं बताई।",
          "इसलिए इन आँकड़ों के आधार पर नीति की समीक्षा उचित होगी, हालाँकि नमूना छोटा है।"),
        p("dialogue_completion", "— आपके तर्क की सबसे कमज़ोर कड़ी कौन-सी है? — ____ (The sample is small.)",
          "इस तर्क की सीमा यह है कि नमूना छोटा है।"),
        p("argument_construction", "Write five sentences: frame, claim, concession, rebuttal, conclusion.",
          "यह लेख इस प्रश्न पर केंद्रित है कि नीति कितनी कारगर रही। उपलब्ध साक्ष्य यह दर्शाते हैं कि प्रभाव असमान रहा। यह सही है कि आँकड़े सीमित हैं। परंतु सीमित आँकड़ों में भी एक स्पष्ट प्रवृत्ति दिखती है। इससे यह निष्कर्ष निकलता है कि नीति की समीक्षा आवश्यक है।"),
        p("summary", "Summarise the shape of an academic Hindi essay in three lines.",
          "पहले प्रश्न तय होता है, फिर पक्ष रखा जाता है। इसके बाद सबसे मज़बूत प्रति-तर्क दर्ज किया जाता है। अंत में केवल वही निष्कर्ष निकाला जाता है जो तर्क से निकलता है।"),
    ],
    "quiz": [
        quiz("Which move states the strongest objection to your own case?", ["उपसंहार", "प्रति-तर्क", "खंडन", "प्रस्तावना"], 1,
             "The counter-argument is where you make the objection properly."),
        quiz("An उपसंहार may not…", ["restate the finding", "introduce a new claim", "name a limitation",
             "draw the consequence"], 1, "The conclusion may only draw out what the argument established."),
        quiz("‘It is true that … yet …’ is the shape of…", ["a claim", "a concession", "a definition", "a citation"], 1,
             "It grants a point before continuing."),
        quiz("इस अध्ययन की सीमा यह है कि… states…", ["a preference", "a limitation", "a citation", "a summary"], 1,
             "सीमा marks the boundary of what the work can support."),
        quiz("Which sentence is advocacy rather than argument?", ["उपलब्ध साक्ष्य सीमित हैं।",
            "यह नीति तुरंत बदलनी चाहिए क्योंकि मैं ऐसा मानता हूँ।", "फिर भी एक प्रवृत्ति दिखती है।",
            "इस तर्क की एक सीमा है।"], 1, "It gives no evidence and no concession — only conviction."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["प्रति-तर्क", "उपसंहार", "सीमा", "प्रस्तावना"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("The five moves", [
        task("Write the Hindi term for each move.", ["framing", "the case", "objection", "reply", "conclusion"],
             ["प्रस्तावना", "पक्ष", "प्रति-तर्क", "खंडन", "उपसंहार"]),
        task("Rewrite each as a concession plus continuation.", ["यह नीति असफल रही।", "यह योजना महँगी है।"],
             ["यह सही है कि नीति के परिणाम सीमित रहे, फिर भी इसका एक प्रभाव दिखता है।",
              "यह सही है कि योजना महँगी है, फिर भी इसे टाला नहीं जा सकता।"]),
        task("Write a limitation sentence for each claim.", ["आँकड़े यह दिखाते हैं कि…", "यह अध्ययन बताता है कि…"],
             ["इसकी सीमा यह है कि आँकड़े केवल एक वर्ष के हैं।",
              "इस अध्ययन की सीमा यह है कि नमूना छोटा है।"]),
        task("Write a five-sentence paragraph using all five moves once.",
             ["frame", "claim", "concession", "reply", "conclusion"],
             ["यह टिप्पणी इस प्रश्न पर केंद्रित है कि नीति कितनी कारगर रही।",
              "उपलब्ध साक्ष्य बताते हैं कि प्रभाव असमान रहा।", "यह सही है कि आँकड़े सीमित हैं।",
              "परंतु इनमें भी एक स्पष्ट प्रवृत्ति दिखती है।",
              "इससे यह निष्कर्ष निकलता है कि समीक्षा उचित है।"]),
    ]),
})

# ── C1 · U3 · Register and Integrated Mastery ───────────────────────────────
lesson("C1", "hi-c1-u3", {
    "id": "C1-U3-L3",
    "title": "मध्यस्थता — carrying a text across registers",
    "learn": ("Mediation is not translation of words but of purpose: explaining an official letter to a "
              "neighbour, summarising a report for a manager, or recasting a lecture as a WhatsApp message. The "
              "tools are सारांश (summary), आशय (intent), मूल भाव (the essential sense) and शब्दशः (word for "
              "word — which is usually what you must avoid)."),
    "vocab": [
        v("सारांश", "sārāṅś", "summary", "noun"),
        v("आशय", "āśay", "intent, purport", "noun"),
        v("मूल भाव", "mūl bhāv", "the essential sense", "collocation"),
        v("शब्दशः", "śabdaśaḥ", "word for word, literally", "adverb"),
        v("व्याख्या", "vyākhyā", "interpretation, explanation", "noun"),
        v("पुनर्कथन", "punarkathan", "retelling, reformulation", "noun"),
        v("सरल भाषा में", "saral bhāṣā meṅ", "in plain language", "phrase"),
        v("अर्थ-विस्तार", "arth-vistār", "expansion of meaning, over-reading", "noun"),
    ],
    "grammar": {
        "title": "मध्यस्थता का सूत्र: आशय बनाए रखें, रूप बदलें",
        "explain": ("A mediation names its own act and then delivers it: इस पत्र का आशय यह है कि… (the intent of "
                    "this letter is…), संक्षेप में (in short), सरल शब्दों में कहें तो… (put simply…). The risk "
                    "is अर्थ-विस्तार — adding certainty or detail the source did not have — so the mediation "
                    "keeps the source’s hedges: बताया गया है, संभव है, अपेक्षा है."),
        "pattern": "इसका आशय यह है कि… · सरल शब्दों में कहें तो… · संक्षेप में",
        "examples": [
            ex("इस पत्र का आशय यह है कि आवेदन अगले सोमवार तक जमा कर दिया जाए।",
               "is patra kā āśay yah hai ki āvedan agle somvār tak jamā kar diyā jāe.",
               "The intent of this letter is that the application be submitted by next Monday."),
            ex("सरल शब्दों में कहें तो योजना अभी लागू नहीं होगी, केवल प्रस्तावित है।",
               "saral śabdõ meṅ kahẽ to yojnā abhī lāgū nahī̃ hogī, keval prastāvit hai.",
               "Put simply, the plan will not take effect yet; it is only proposed."),
            ex("सारांश यह कि अगली बैठक में निर्णय होगा।", "sārāṅś yah ki aglī baiṭhak meṅ nirṇay hogā.",
               "In summary, the decision will come at the next meeting."),
        ],
        "mistakes": [
            "Turning संभव है into होगा — a hedge dropped in mediation becomes a promise the source never made.",
            "शब्दशः translation of officialese: the neighbour does not need निवेदन है कि; they need आशय.",
        ],
    },
    "dialogue": [
        line("पड़ोसी", "यह पत्र बहुत कठिन भाषा में है, क्या लिखा है?", "yah patra bahut kaṭhin bhāṣā meṅ hai, kyā likhā hai?",
             "This letter is in very difficult language — what does it say?"),
        line("मीरा", "संक्षेप में — आवेदन सोमवार तक जमा करना है, बस इतना।", "saṅkṣep meṅ — āvedan somvār tak jamā karnā hai, bas itnā.",
             "In short: the application has to be submitted by Monday, that is all."),
        line("पड़ोसी", "तो मंज़ूरी मिल गई?", "to manzūrī mil gaī?", "So it has been approved?"),
        line("मीरा", "नहीं, यह नहीं लिखा। पत्र कहता है कि निर्णय संभव है, पक्का नहीं।",
             "nahī̃, yah nahī̃ likhā. patra kahtā hai ki nirṇay sambhav hai, pakkā nahī̃.",
             "No, it does not say that. The letter says a decision is possible, not certain."),
    ],
    "practice": [
        p("multiple_choice", "Which sentence mediates rather than translates word for word?",
          "इसका आशय यह है कि आवेदन सोमवार तक जमा करें।",
          options=["इसका आशय यह है कि आवेदन सोमवार तक जमा करें।",
                   "निवेदन है कि आवेदन पत्र समय-सीमा के भीतर प्रस्तुत किया जाए।",
                   "आपको आवेदन करना होगा।", "आवेदन जमा कीजिए।"]),
        p("fill_in_the_blank", "____ शब्दों में कहें तो योजना अभी लागू नहीं होगी। (plain)", "सरल"),
        p("translation", "In summary, the decision will come at the next meeting.",
          "सारांश यह कि निर्णय अगली बैठक में होगा।"),
        p("reverse_translation", "इस पत्र का आशय यह है कि निर्णय संभव है, पक्का नहीं।",
          "The intent of the letter is that a decision is possible, not certain."),
        p("word_selection", "Which word means ‘word for word’?", "शब्दशः",
          options=["शब्दशः", "सारांश", "आशय", "व्याख्या"]),
        p("matching", "Match each term with its function in mediation.", "सारांश = the short form",
          options=["आशय = the intent", "सारांश = the short form", "व्याख्या = the explanation",
                   "पुनर्कथन = the retelling"]),
        p("reorder", "Put these in order: कहें तो · शब्दों में · सरल", "सरल शब्दों में कहें तो…"),
        p("sentence_building", "Build the mediation: ‘Put simply, it is only proposed.’",
          "सरल शब्दों में कहें तो यह केवल प्रस्तावित है।"),
        p("error_correction", "Find the over-reading: पत्र में लिखा है कि मंज़ूरी मिल जाएगी।",
          "पत्र में लिखा है कि निर्णय संभव है।"),
        p("dialogue_completion", "— तो अब क्या करना है? — ____ (In short: submit the application by Monday.)",
          "संक्षेप में, सोमवार तक आवेदन जमा कर दीजिए।"),
        p("paraphrase", "Recast this official line for a neighbour.",
          "निवेदन है कि आवेदन पत्र निर्धारित तिथि तक प्रस्तुत किया जाए। → सोमवार तक आवेदन जमा कर दीजिए, बस इतना।"),
        p("summary", "Summarise a letter’s three demands in two sentences, keeping its hedges.",
          "पत्र में तीन बातें हैं: आवेदन जमा करना, दस्तावेज़ संलग्न करना, और तिथि का पालन। इसमें कहा गया है कि निर्णय संभव है, परंतु अभी तय नहीं है।"),
    ],
    "quiz": [
        quiz("Mediation keeps…", ["every word of the source", "the source’s intent and degree of certainty",
            "the source’s register", "the source’s length"], 1,
             "The form changes; the claim and its hedges do not."),
        quiz("अर्थ-विस्तार is…", ["a good summary", "reading more into the text than it says",
            "a literal translation", "a formal register"], 1, "It is the mediation error to avoid."),
        quiz("सरल शब्दों में कहें तो… introduces…", ["a citation", "a plain-language restatement", "a concession",
            "a correction"], 1, "It signals the register switch."),
        quiz("A letter says निर्णय संभव है. A faithful mediation says…",
             ["मंज़ूरी मिल गई।", "निर्णय हो सकता है, पक्का नहीं।", "निर्णय नहीं होगा।", "मंज़ूरी मिलेगी।"], 1,
             "The hedge has to survive the retelling."),
        quiz("शब्दशः translation of officialese usually fails because…",
             ["it is too short", "the reader needed the intent, not the words", "it changes the meaning",
              "it is impolite"], 1, "Mediation serves the reader’s question, not the source’s phrasing."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["आशय", "सारांश", "शब्दशः", "सरल शब्दों में कहें तो"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("Mediating a text", [
        task("Write the Hindi for each mediation term.", ["intent", "summary", "word for word", "in plain language"],
             ["आशय", "सारांश", "शब्दशः", "सरल भाषा में"]),
        task("Recast each official line into plain speech.", ["निवेदन है कि आवेदन प्रस्तुत किया जाए।",
             "यह सूचित किया जाता है कि तिथि परिवर्तित कर दी गई है।"],
             ["आवेदन जमा कर दीजिए।", "तारीख़ बदल गई है।"]),
        task("Keep the hedge: rewrite each without adding certainty.",
             ["निर्णय संभव है।", "अपेक्षा है कि उत्तर मिलेगा।"],
             ["निर्णय हो सकता है, पक्का नहीं।", "उम्मीद है कि उत्तर मिल सकता है।"]),
        task("Write a four-line mediation: state the source, give the intent, keep one hedge, and say what to do.",
             ["source", "intent", "hedge", "action"],
             ["यह पत्र नगरपालिका से है।", "इसका आशय यह है कि आवेदन जमा किया जाए।",
              "इसमें लिखा है कि निर्णय संभव है, पक्का नहीं।", "सोमवार तक आवेदन जमा कर दीजिए।"]),
    ]),
})

# ── C2 · U1 · Meaning and Rhetorical Architecture ───────────────────────────
lesson("C2", "hi-c2-u1", {
    "id": "C2-U1-L3",
    "title": "निहितार्थ और पूर्वधारणा — what a sentence takes for granted",
    "learn": ("At C2 the work moves from what a sentence says to what it assumes. A पूर्वधारणा "
              "(presupposition) survives negation — ‘तुमने पढ़ना बंद क्यों किया?’ still assumes you were "
              "reading — while a निहितार्थ (implicature) can be cancelled without contradiction: ‘कुछ छात्र "
              "आए, वैसे सब नहीं आए।’ Learning to test which is which is how you stop being argued with "
              "sideways."),
    "vocab": [
        v("निहितार्थ", "nihitārth", "implicature, implied meaning", "noun"),
        v("पूर्वधारणा", "pūrvadhāraṇā", "presupposition", "noun"),
        v("अभिकथन", "abhikathan", "assertion, what is stated", "noun"),
        v("निषेध", "niṣedh", "negation", "noun"),
        v("संदेहास्पद", "saṅdehāspad", "dubious, questionable", "adjective"),
        v("बलाघात", "balāghāt", "emphasis, stress", "noun"),
        v("निगमन", "nigaman", "inference, deduction", "noun"),
        v("स्पष्टतः", "spaṣṭataḥ", "explicitly, clearly", "adverb"),
    ],
    "grammar": {
        "title": "परीक्षण: निषेध और रद्दीकरण",
        "explain": ("Two tests separate the layers. Presupposition test: negate the sentence and see what "
                    "survives — ‘वह पढ़ना बंद नहीं कर रहा’ still assumes he was reading, so ‘he was reading’ is a "
                    "presupposition, not an assertion. Implicature test: add a cancellation — ‘कुछ छात्र आए, "
                    "वैसे सब नहीं आए’ is not contradictory, so ‘not all came’ was only an implicature. In "
                    "argument, पूर्वधारणा is what you may challenge and निगमन is what you may only call valid "
                    "or invalid."),
        "pattern": "यह कहा गया कि… · यह मान लिया गया कि… (presupposition) · इससे यह निकलता है कि… (inference)",
        "examples": [
            ex("प्रश्न यह मान लेता है कि समय पर्याप्त था — यही उसकी पूर्वधारणा है।",
               "praśn yah mān letā hai ki samay paryāpt thā — yahī uskī pūrvadhāraṇā hai.",
               "The question assumes there was enough time — that is its presupposition."),
            ex("उसने कहा कि कुछ रिपोर्टें देर से आईं, पर यह नहीं कहा कि सब देर से आईं।",
               "usne kahā ki kuch riporṭeṅ der se āīṅ, par yah nahī̃ kahā ki sab der se āīṅ.",
               "He said some reports arrived late, but did not say all did."),
            ex("यदि आधार सही हैं, तो निगमन वैध है; यह अलग प्रश्न है कि निष्कर्ष सत्य है या नहीं।",
               "yadi ādhār sahī hain, to nigaman vaidh hai; yah alag praśn hai ki niṣkarṣ satya hai yā nahī̃.",
               "If the premises are correct the inference is valid; whether the conclusion is true is another question."),
        ],
        "mistakes": [
            "Treating a challengeable presupposition as an established fact: ‘आपने जो गलती की…’ presumes the fault before it is shown.",
            "Reading ‘कुछ’ as ‘सब’ — the classic implicature slip in both directions of an argument.",
        ],
    },
    "dialogue": [
        line("समीक्षक", "आपके प्रश्न में ही यह मान लिया गया है कि दोष किसी एक पक्ष का है।",
             "āpke praśn meṅ hī yah mān liyā gayā hai ki doṣ kisī ek pakṣ kā hai.",
             "Your very question assumes the fault lies with one side."),
        line("लेखक", "सही पकड़ा। तो पहले पूर्वधारणा को अलग करते हैं।",
             "sahī pakaṛā. to pahle pūrvadhāraṇā ko alag karte haiṅ.",
             "Well caught. Then let us separate the presupposition first."),
        line("समीक्षक", "और ‘कुछ’ से ‘सब’ निकालना भी उचित नहीं।", "aur ‘kuch’ se ‘sab’ nikālnā bhī ucit nahī̃.",
             "And drawing ‘all’ out of ‘some’ is not fair either."),
        line("लेखक", "मानता हूँ — निहितार्थ रद्द किया जा सकता है, पूर्वधारणा नहीं।",
             "māntā hū̃ — nihitārth radd kiyā jā saktā hai, pūrvadhāraṇā nahī̃.",
             "I accept — an implicature can be cancelled, a presupposition cannot."),
    ],
    "practice": [
        p("multiple_choice", "Which survives negation, and is therefore a presupposition?",
          "‘उसने पढ़ना बंद कर दिया’ → वह पहले पढ़ता था।",
          options=["‘उसने पढ़ना बंद कर दिया’ → वह पहले पढ़ता था।",
                   "‘कुछ आए’ → सब नहीं आए।", "‘वह थका है’ → उसे आराम चाहिए।",
                   "‘महँगा है’ → ख़रीदना कठिन है।"]),
        p("fill_in_the_blank", "प्रश्न यह ____ लेता है कि समय पर्याप्त था। (assumes)", "मान"),
        p("translation", "He said some reports arrived late, but did not say all did.",
          "उसने कहा कि कुछ रिपोर्टें देर से आईं, पर यह नहीं कहा कि सब देर से आईं।"),
        p("reverse_translation", "निहितार्थ रद्द किया जा सकता है, पूर्वधारणा नहीं।",
          "An implicature can be cancelled, a presupposition cannot."),
        p("word_selection", "Which term means a questionable assumption built into the wording?", "पूर्वधारणा",
          options=["पूर्वधारणा", "निहितार्थ", "अभिकथन", "निगमन"]),
        p("matching", "Match each layer with its test.", "पूर्वधारणा = survives negation",
          options=["अभिकथन = what is directly said", "निहितार्थ = can be cancelled",
                   "पूर्वधारणा = survives negation", "निगमन = valid or invalid"]),
        p("reorder", "Put these in order: मान लिया गया · यह · कि · है", "यह मान लिया गया है कि…"),
        p("sentence_building", "Build the challenge: ‘The question assumes the fault is already established.’",
          "यह प्रश्न मान लेता है कि दोष पहले से सिद्ध है।"),
        p("error_correction", "Find the over-reading: उसने कहा कि कुछ रिपोर्टें देर से आईं, इसलिए सब देर से आईं।",
          "उसने कहा कि कुछ रिपोर्टें देर से आईं, पर सबके बारे में कुछ नहीं कहा।"),
        p("dialogue_completion", "— तो पहले क्या अलग करें? — ____ (First separate the presupposition.)",
          "पहले पूर्वधारणा को अलग करते हैं।"),
        p("paraphrase", "Rewrite so that no presupposition remains.",
          "आपने जो गलती की, उसका कारण क्या था? → क्या आपको लगता है कि कोई गलती हुई? यदि हाँ, तो उसका कारण क्या था?"),
        p("argument_construction", "Write a four-sentence passage: assertion, presupposition, implicature, explicit qualification.",
          "रिपोर्ट देर से आई। यह मान लिया गया कि विभाग लापरवाह है। इसमें यह भी सुनाई देता है कि सब विभाग ऐसे हैं। परंतु यह स्पष्टतः नहीं कहा गया।"),
    ],
    "quiz": [
        quiz("A presupposition is what…", ["can be cancelled", "survives negation", "is stated directly",
            "follows necessarily"], 1, "Negation leaves it standing."),
        quiz("‘कुछ छात्र आए, वैसे सब नहीं आए’ is acceptable because…",
             ["it contradicts itself", "the implicature is cancelled", "it is a presupposition",
              "it is formal"], 1, "Cancellation shows ‘not all’ was never asserted."),
        quiz("निगमन is assessed as…", ["true or false", "valid or invalid", "polite or rude", "clear or vague"], 1,
             "Logic concerns the link between premises and conclusion."),
        quiz("‘आपने जो गलती की, उसका कारण क्या था?’ contains…",
             ["a presupposition", "a concessive", "a citation", "an imperative"], 0,
             "The fault is assumed before it is established."),
        quiz("Which sentence states the inference rather than the input?", ["आधार सही हैं।",
            "इससे यह निकलता है कि निष्कर्ष वैध है।", "रिपोर्ट देर से आई।", "यह मान लिया गया।"], 1,
             "It marks the movement from premises to conclusion."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["पूर्वधारणा", "निहितार्थ", "निगमन", "मान लिया गया"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("Testing the layers", [
        task("Write the Hindi term for each layer.", ["assertion", "implicature", "presupposition", "inference"],
             ["अभिकथन", "निहितार्थ", "पूर्वधारणा", "निगमन"]),
        task("Name the presupposition in each question.", ["तुमने पढ़ना बंद क्यों किया?",
             "आपने वह फ़ाइल क्यों मिटा दी?"],
             ["वह पहले पढ़ता था।", "फ़ाइल मौजूद थी और वही व्यक्ति उसे मिटाने वाला है।"]),
        task("Cancel the implicature in each line.", ["कुछ रिपोर्टें देर से आईं।", "कई लोग सहमत हैं।"],
             ["कुछ रिपोर्टें देर से आईं, पर सब नहीं।", "कई लोग सहमत हैं, पर सब नहीं।"]),
        task("Write a four-line correction: name the assumption, then restate the claim without it.",
             ["assumption", "restatement"],
             ["आपके प्रश्न में यह मान लिया गया है कि दोष किसी एक पक्ष का है।",
              "इसलिए पहले यह पूछना उचित होगा कि दोष सिद्ध हुआ है या नहीं।"]),
    ]),
})

# ── C2 · U2 · Scholarly and Figurative Mastery ──────────────────────────────
lesson("C2", "hi-c2-u2", {
    "id": "C2-U2-L3",
    "title": "उद्धरण और पुनर्कथन — keeping sources honest",
    "learn": ("When several sources disagree, the C2 skill is not choosing a winner but keeping each voice "
              "audible: आधार (the basis of a claim), दृष्टिकोण (standpoint), भिन्नता (the difference), समर्थन "
              "(support), उद्धरण (quotation). A faithful synthesis lets you say what each source claimed, on "
              "what basis, and how sure it was — without flattening them into one voice."),
    "vocab": [
        v("उद्धरण", "uddharaṇ", "quotation, citation", "noun"),
        v("संदर्भ", "sandarbh", "reference, context", "noun"),
        v("आधार", "ādhār", "basis, grounds", "noun"),
        v("दृष्टिकोण", "dṛṣṭikoṇ", "standpoint, perspective", "noun"),
        v("भिन्नता", "bhinnatā", "difference, divergence", "noun"),
        v("समर्थन", "samarthan", "support, endorsement", "noun"),
        v("असंगति", "asaṅgati", "inconsistency", "noun"),
        v("अप्रमाणित", "apramāṇit", "unverified, unattested", "adjective"),
    ],
    "grammar": {
        "title": "स्रोत-सूचना: किसने, किस आधार पर, कितने निश्चय से",
        "explain": ("Reported scholarship carries three pieces of information at once — the source, the basis "
                    "and the degree of certainty: मिश्रा के अनुसार (according to Mishra), आँकड़ों के आधार पर "
                    "(on the basis of data), सुझाव देते हैं (they suggest) versus सिद्ध करते हैं (they "
                    "demonstrate). असंगति between sources is named, not hidden: दोनों के निष्कर्ष भिन्न हैं "
                    "क्योंकि आधार भिन्न है."),
        "pattern": "… के अनुसार · आँकड़ों के आधार पर · सुझाव देते हैं / सिद्ध करते हैं · भिन्नता यह है कि…",
        "examples": [
            ex("मिश्रा के अनुसार नमूना छोटा था, इसलिए वे केवल सुझाव देते हैं।",
               "miśrā ke anusār namūnā choṭā thā, isliye ve keval sujhāv dete haiṅ.",
               "According to Mishra the sample was small, so they only suggest."),
            ex("आँकड़ों के आधार पर दोनों अध्ययन भिन्न निष्कर्ष निकालते हैं।",
               "ā̃kṛõ ke ādhār par donõ adhyayan bhinn niṣkarṣ nikālte haiṅ.",
               "On the basis of the data the two studies draw different conclusions."),
            ex("यह दावा अभी अप्रमाणित है और इसका आधार कोई उद्धरण नहीं देता।",
               "yah dāvā abhī apramāṇit hai aur iskā ādhār koī uddharaṇ nahī̃ detā.",
               "This claim is still unverified and no citation supports it."),
        ],
        "mistakes": [
            "Synthesis that reports only the agreement and silently drops भिन्नता — dissent is data too.",
            "Using सिद्ध करते हैं for what the source only suggested: the reported strength must match the source’s.",
        ],
    },
    "dialogue": [
        line("संपादक", "दोनों अध्ययनों में असंगति है — आपने कैसे निपटाया?",
             "donõ adhyayanõ meṅ asaṅgati hai — āpne kaise niptāyā?",
             "The two studies are inconsistent — how did you handle it?"),
        line("लेखक", "मैंने दोनों के आधार अलग-अलग रखे और भिन्नता स्पष्ट लिखी।",
             "mainne donõ ke ādhār alag-alag rakhe aur bhinnatā spaṣṭ likhī.",
             "I kept their bases separate and wrote the divergence out clearly."),
        line("संपादक", "और आपका निष्कर्ष?", "aur āpkā niṣkarṣ?", "And your conclusion?"),
        line("लेखक", "केवल इतना कि आधार भिन्न है; इसलिए दोनों में से किसी को सिद्ध नहीं कहा जा सकता।",
             "keval itnā ki ādhār bhinn hai; isliye donõ meṅ se kisī ko siddh nahī̃ kahā jā saktā.",
             "Only that the bases differ; so neither can be called proven."),
    ],
    "practice": [
        p("multiple_choice", "Which line reports the source’s certainty faithfully?",
          "मिश्रा के अनुसार संभावना है, निष्कर्ष नहीं।",
          options=["मिश्रा के अनुसार संभावना है, निष्कर्ष नहीं।",
                   "मिश्रा ने सिद्ध कर दिया है।", "मिश्रा का मत सर्वथा सत्य है।",
                   "मिश्रा और सब एक ही बात कहते हैं।"]),
        p("fill_in_the_blank", "आँकड़ों के ____ पर दोनों अध्ययन भिन्न निष्कर्ष निकालते हैं। (basis)", "आधार"),
        p("translation", "This claim is still unverified and no citation supports it.",
          "यह दावा अभी अप्रमाणित है और इसे कोई उद्धरण समर्थन नहीं देता।"),
        p("reverse_translation", "भिन्नता यह है कि एक अध्ययन की आबादी बड़ी थी।",
          "The difference is that one study had a large population."),
        p("word_selection", "Which term marks a claim as not yet verified?", "अप्रमाणित",
          options=["अप्रमाणित", "समर्थन", "संदर्भ", "दृष्टिकोण"]),
        p("matching", "Match each reporting verb with the strength it signals.",
          "सुझाव देते हैं = tentative",
          options=["सिद्ध करते हैं = demonstrated", "सुझाव देते हैं = tentative",
                   "बताते हैं = states", "मानते हैं = takes as a view"]),
        p("reorder", "Put these in order: अनुसार · मिश्रा · के · नमूना छोटा था", "मिश्रा के अनुसार नमूना छोटा था।"),
        p("sentence_building", "Build the synthesis line: ‘The bases differ, so the conclusions diverge.’",
          "आधार भिन्न हैं, इसलिए निष्कर्ष भी भिन्न हैं।"),
        p("error_correction", "Find the unfair report: राव ने सिद्ध किया है कि नीति असफल रही, हालाँकि उनका अध्ययन सुझाव देता है।",
          "राव का अध्ययन सुझाव देता है कि नीति के परिणाम सीमित हो सकते हैं।"),
        p("dialogue_completion", "— दोनों अध्ययन एक-दूसरे का खंडन करते हैं? — ____ (Not exactly; their bases differ.)",
          "निश्चित रूप से नहीं — दोनों के आधार भिन्न हैं।"),
        p("paraphrase", "Reformulate this dense citation without changing its certainty.",
          "यह संभव है कि नीति का प्रभाव सीमित रहा (रिपोर्ट, पृ. 14)। → रिपोर्ट के अनुसार नीति का प्रभाव सीमित हो सकता है।"),
        p("summary", "Write a three-line synthesis of two sources that disagree, naming the divergence.",
          "मिश्रा के अनुसार नमूना छोटा था। राव के अनुसार नमूना बड़ा था। इसलिए दोनों के निष्कर्ष भिन्न हैं और दोनों अनिश्चित दावे करते हैं।"),
    ],
    "quiz": [
        quiz("A faithful synthesis must keep…", ["only the agreement", "the differences too",
            "the sources anonymous", "only the strongest claim"], 1, "Dissent is evidence about the field."),
        quiz("अप्रमाणित means…", ["disproved", "unverified", "unpopular", "unnamed"], 1,
             "It is a claim without supporting evidence."),
        quiz("‘सुझाव देते हैं’ signals…", ["certainty", "tentativeness", "quotation", "refutation"], 1,
             "The source proposes, it does not prove."),
        quiz("आँकड़ों के आधार पर introduces…", ["an opinion", "the basis of a claim", "a citation style",
            "a concession"], 1, "It names the grounds."),
        quiz("Which sentence hides an inconsistency?", ["दोनों के निष्कर्ष भिन्न हैं।",
            "दोनों एक ही निष्कर्ष पर पहुँचते हैं (though their data differ).",
            "भिन्नता का कारण आधार है।", "एक अध्ययन अनिश्चित है।"], 1,
             "It asserts agreement that the data contradict."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["उद्धरण", "आधार", "भिन्नता", "अप्रमाणित"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("Sourcing and synthesis", [
        task("Write the Hindi for each reporting term.", ["citation", "basis", "divergence", "unverified"],
             ["उद्धरण", "आधार", "भिन्नता", "अप्रमाणित"]),
        task("Rewrite each claim at the strength the source allows.", ["मिश्रा ने सिद्ध किया है कि… (small sample)",
             "राव का निष्कर्ष अंतिम है। (one district)"],
             ["मिश्रा के अनुसार संभावना है कि…", "राव का निष्कर्ष एक ज़िले तक सीमित है।"]),
        task("Write a divergence sentence for each pair.", ["आबादी: बड़ी / छोटी", "अवधि: दो वर्ष / छह महीने"],
             ["भिन्नता यह है कि एक अध्ययन की आबादी बड़ी थी।",
              "भिन्नता यह है कि अवधि दो वर्ष और छह महीने की थी।"]),
        task("Write a four-line synthesis: source, basis, divergence, cautious conclusion.",
             ["source", "basis", "divergence", "conclusion"],
             ["मिश्रा और राव दोनों नीति के प्रभाव का अध्ययन करते हैं।",
              "मिश्रा आँकड़ों के आधार पर और राव साक्षात्कारों के आधार पर लिखते हैं।",
              "भिन्नता यह है कि उनके निष्कर्ष एक-दूसरे से अलग हैं।",
              "इसलिए अभी कहा जा सकता है कि प्रभाव की मात्रा अप्रमाणित है।"]),
    ]),
})

# ── C2 · U3 · Negotiation and Stylistic Mastery ─────────────────────────────
lesson("C2", "hi-c2-u3", {
    "id": "C2-U3-L3",
    "title": "रूपांतरण — recasting a text without losing it",
    "learn": ("Stylistic mastery is demonstrated by रूपांतरण: taking the same content through a report, an "
              "editorial, a formal notice and a spoken explanation, changing syntax, metaphor and information "
              "order while keeping every claim, hedge and relationship intact. The measure of success is not "
              "elegance but invariance — does the reader of version B know exactly what version A said?"),
    "vocab": [
        v("रूपांतरण", "rūpāntaraṇ", "transformation, recasting", "noun"),
        v("अपरिवर्तनीय", "aparivartanīya", "invariant, unchangeable", "adjective"),
        v("शैली", "śailī", "style", "noun"),
        v("लक्ष्य-पाठक", "lakṣya-pāṭhak", "target reader", "noun"),
        v("स्वर", "svar", "tone, voice", "noun"),
        v("संक्षिप्तीकरण", "saṅkṣiptīkaraṇ", "condensation", "noun"),
        v("विस्तार", "vistār", "expansion, elaboration", "noun"),
        v("भाव-निष्ठा", "bhāv-niṣṭhā", "fidelity of sense", "collocation"),
    ],
    "grammar": {
        "title": "शैली बदलती है, दावा नहीं",
        "explain": ("Recasting changes surface features and holds the claim constant: कर्ता-कर्म बदलने पर भी "
                    "तथ्य वही रहता है, and a hedge must follow the claim into every version. Practical moves: "
                    "condense (संक्षिप्त में), expand (विस्तार से), change voice (किया गया ↔ ने किया), change "
                    "order (cleft: यह तथ्य ही निर्णायक था), change metaphor (जब धारा बदलती है ↔ जब सोच बदलती "
                    "है). भाव-निष्ठा is the criterion."),
        "pattern": "विस्तार से कहें तो… · संक्षेप में… · कर्तृवाच्य ↔ कर्मवाच्य · यह तथ्य ही कि…",
        "examples": [
            ex("कार्यवृत्त की शैली में: यह सुझाव स्वीकृत किया गया।", "kāryavṛtt kī śailī meṅ: yah sujhāv svīkṛt kiyā gayā.",
               "In minutes style: this suggestion was approved."),
            ex("संपादकीय की शैली में: यही सुझाव दिशा बदल सकता है।", "sampādakīya kī śailī meṅ: yahī sujhāv diśā badal saktā hai.",
               "In editorial style: this very suggestion could change direction."),
            ex("बोलचाल में: देखिए, यह बात मान ली गई है, पक्का कुछ नहीं।",
               "bolcāl meṅ: dekhiye, yah bāt mān lī gaī hai, pakkā kuch nahī̃.",
               "In speech: look, the point has been accepted, but nothing is certain."),
        ],
        "mistakes": [
            "Condensation that drops a hedge: संभव है → होगा turns a possibility into a promise across versions.",
            "Changing the relationship while changing the register — a formal recast that removes politeness markers changes what the speaker did.",
        ],
    },
    "dialogue": [
        line("प्रशिक्षक", "एक ही निर्णय तीन शैलियों में लिखिए।", "ek hī nirṇay tīn śailiyõ meṅ likhie.",
             "Write the same decision in three styles."),
        line("शिक्षार्थी", "कार्यवृत्त में: निर्णय अगली बैठक तक स्थगित किया गया।",
             "kāryavṛtt meṅ: nirṇay aglī baiṭhak tak sthagit kiyā gayā.",
             "In minutes: the decision was deferred to the next meeting."),
        line("शिक्षार्थी", "संपादकीय में: निर्णय टल गया, पर प्रश्न खुला है।",
             "sampādakīya meṅ: nirṇay ṭal gayā, par praśn khulā hai.",
             "In editorial: the decision slipped, but the question remains open."),
        line("प्रशिक्षक", "और भाव-निष्ठा? क्या कहीं दावा बदला?", "aur bhāv-niṣṭhā? kyā kahī̃ dāvā badlā?",
             "And fidelity? Did the claim shift anywhere?"),
    ],
    "practice": [
        p("multiple_choice", "Which recast keeps both the claim and the hedge?",
          "यह संभव है कि योजना टल जाए।",
          options=["यह संभव है कि योजना टल जाए।", "योजना टल जाएगी।",
                   "योजना टालनी ही चाहिए।", "योजना का कोई भविष्य नहीं।"]),
        p("fill_in_the_blank", "कर्तृवाच्य से ____ में बदलने पर भी तथ्य वही रहता है। (passive)", "कर्मवाच्य"),
        p("translation", "The same claim, in editorial style: the decision slipped, but the question remains open.",
          "संपादकीय शैली में वही दावा: निर्णय टल गया, पर प्रश्न खुला है।"),
        p("reverse_translation", "संक्षेप में कहें तो योजना अभी प्रस्तावित है।",
          "In short, the plan is still only proposed."),
        p("word_selection", "Which term means fidelity to sense across versions?", "भाव-निष्ठा",
          options=["भाव-निष्ठा", "विस्तार", "शैली", "स्वर"]),
        p("matching", "Match each operation with its effect.", "संक्षिप्तीकरण = fewer words",
          options=["विस्तार = more detail", "संक्षिप्तीकरण = fewer words",
                   "कर्मवाच्य = actor backgrounded", "रूपांतरण = style changed"]),
        p("reorder", "Put these in order: तो · विस्तार से · कहें · यह", "विस्तार से कहें तो यह…"),
        p("sentence_building", "Build the cleft: ‘It was this fact that decided the matter.’",
          "यह तथ्य ही निर्णायक था।"),
        p("error_correction", "Find the version that changed the claim: कार्यवृत्त: निर्णय स्थगित। संपादकीय: निर्णय हो गया।",
          "संपादकीय: निर्णय अभी स्थगित है, पर प्रश्न खुला है।"),
        p("dialogue_completion", "— तीन शैलियों में दावा वही है? — ____ (Yes, only the style changed.)",
          "जी, दावा वही है — केवल शैली बदली है।"),
        p("register_transformation", "Recast this spoken line as a formal notice.",
          "देखिए, फ़ाइल अभी तैयार नहीं है, कल मिलेगी। → सूचित किया जाता है कि फ़ाइल एक कार्यदिवस में उपलब्ध होगी।"),
        p("guided_composition", "Write the same single claim in three styles: notice, editorial, spoken.",
          "सूचना: सूचित किया जाता है कि प्रस्ताव विचाराधीन है। संपादकीय: प्रस्ताव अभी विचाराधीन है, उत्तर नहीं। बोलचाल: देखिए, फ़ैसला अभी नहीं हुआ, सोच-विचार चल रहा है।"),
    ],
    "quiz": [
        quiz("The test of a good recast is…", ["more elegant language", "invariance of claim and hedging",
            "a different conclusion", "a longer text"], 1, "Version B must say what version A said."),
        quiz("संभव है → होगा across versions is…", ["a style change", "a changed claim", "a condensation",
            "a cleft"], 1, "Certainty was added."),
        quiz("Changing किया गया to ने किया changes…", ["the fact", "which participant is backgrounded",
            "the tense", "the politeness"], 1, "Voice shifts attention, not the event."),
        quiz("भाव-निष्ठा requires that…", ["the wording is identical", "the sense and relationships survive",
            "the register is identical", "the length is the same"], 1,
             "Form varies; content and stance do not."),
        quiz("Which condensation is faithful?", ["निर्णय संभव है → निर्णय होगा",
            "निर्णय संभव है, पक्का नहीं → निर्णय अभी अनिश्चित है",
            "संभव है → आवश्यक है", "संभव है → निश्चित है"], 1,
             "It keeps the uncertainty rather than removing it."),
    ],
    "flashcards": "auto:vocab",
    "srs_candidates": ["रूपांतरण", "भाव-निष्ठा", "संक्षिप्तीकरण", "यह तथ्य ही"],
    "srs_policy": ("Only these four high-value terms are preselected; lesson mistakes and productive patterns "
                   "may enter personalized review after an actual error."),
    "worksheet": ws("Recasting with fidelity", [
        task("Write the Hindi for each stylistic operation.", ["recasting", "condensation", "expansion",
             "fidelity of sense"], ["रूपांतरण", "संक्षिप्तीकरण", "विस्तार", "भाव-निष्ठा"]),
        task("Recast each in formal notice style.", ["फ़ाइल कल मिलेगी।", "बैठक अब नहीं होगी।"],
             ["सूचित किया जाता है कि फ़ाइल एक कार्यदिवस में उपलब्ध होगी।",
              "सूचित किया जाता है कि बैठक स्थगित कर दी गई है।"]),
        task("Condense each without dropping the hedge.", ["इसमें कहा गया है कि निर्णय संभव है, पक्का नहीं।",
             "अपेक्षा है कि उत्तर अगले सप्ताह मिल सकता है।"],
             ["निर्णय अभी अनिश्चित है।", "उत्तर अगले सप्ताह संभव है।"]),
        task("Take one claim through three styles and label each version.",
             ["notice", "editorial", "spoken"],
             ["सूचना: प्रस्ताव विचाराधीन है।", "संपादकीय: प्रस्ताव अभी विचाराधीन है — यह उत्तर नहीं है।",
              "बोलचाल: सोच-विचार चल रहा है, फ़ैसला बाकी है।"]),
    ]),
})


def sync_manifest(check: bool) -> int:
    """Keep the hi lesson counts in data/courses/index.json equal to the rung data.

    build-courses.py validates the legacy shape (2 lessons per unit) and can no
    longer compute counts for units that have grown, so the authoring source owns
    this one field. Idempotent; drift is reported by --check.
    """
    path = ROOT / "data/courses/index.json"
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    course = next((c for c in data["courses"] if c.get("code") == "hi"), None)
    if course is None:
        print("  index.json: no hi course entry")
        return 0 if check else 1
    stale = 0
    for rung in ("A1", "A2", "B1", "B2", "C1", "C2"):
        rung_path = ROOT / f"data/courses/phase-2/hi_{rung}.json"
        level = json.loads(rung_path.read_text(encoding="utf-8"))["level"]
        n = sum(len(u["lessons"]) for u in level["units"])
        entry = course.get("levels", {}).get(rung)
        if not isinstance(entry, dict) or entry.get("lessons") == n:
            continue
        if check:
            print(f"  index.json hi {rung}: {entry.get('lessons')} -> {n} STALE")
            stale += 1
            continue
        entry["lessons"] = n
        print(f"  index.json hi {rung}: lessons -> {n}")
        stale += 1
    if check or not stale:
        return stale
    out = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
    if out != raw:
        path.write_text(out, encoding="utf-8")
    return stale


def main() -> int:
    check = "--check" in sys.argv
    written = 0
    for (rung, unit_id), new in sorted(HI_LESSONS.items()):
        path = ROOT / f"data/courses/phase-2/hi_{rung}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        unit = next((u for u in data["level"]["units"] if u["id"] == unit_id), None)
        if unit is None:
            raise SystemExit(f"{path}: no unit {unit_id}")
        existing = next((l for l in unit["lessons"] if l["id"] == new["id"]), None)
        if existing == new:
            print(f"  {new['id']}  already current ({len(unit['lessons'])} lessons)")
            continue
        if check:
            print(f"  {new['id']}  STALE")
            written += 1
            continue
        if existing:
            unit["lessons"][unit["lessons"].index(existing)] = new
        else:
            unit["lessons"].append(new)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  {new['id']}  {new['title'][:34]:36s} vocab={len(new['vocab'])} "
              f"practice={len(new['practice'])} quiz={len(new['quiz'])} — unit now {len(unit['lessons'])} lessons")
        written += 1
    synced = sync_manifest(check)
    print(f"{'STALE' if check else 'written'}: {written} lesson(s)")
    return 1 if (check and (written or synced)) else 0


if __name__ == "__main__":
    raise SystemExit(main())

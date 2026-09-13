#!/usr/bin/env python3
"""Authored German course data. Language config + content.
Loaded by tools/build-world-course.py. Do not hand-edit the generated
output pages; edit THIS file and regenerate.
Content is authored by hand, not machine-translated.
"""

COURSE = {
 "lang": "de",
 "name": "German",
 "native": "Deutsch",
 "speechTag": "de-DE",
 "status": "Available",
 "note": "A real, authored German course: 6 lessons, a practice lab, a topic quiz and a review deck — all running on the same engines as Hindi. It is not yet as deep as the Hindi course, and all audio is your browser's computer voice, never a native recording."
}

LESSONS = [
 {
  "slug": "greetings-and-introductions",
  "title": "German Greetings and Introductions",
  "desc": "Every German greeting you actually need, when to use du and Sie, and how to introduce yourself — with pronunciation and examples.",
  "sections": [
   [
    "The greetings that cover most situations",
    [
     "German has one greeting for every hour of the day: <b>Hallo</b> (hello). It works with friends, shopkeepers and strangers alike. The time-based greetings are warmer and more standard in the south: <b>Guten Morgen</b> (good morning), <b>Guten Tag</b> (good day — used from late morning) and <b>Guten Abend</b> (good evening). Note that <b>Gute Nacht</b> means good night only as a farewell — you never greet someone arriving with it."
    ]
   ],
   [
    "Introducing yourself",
    [
     "To say your name, use <b>Ich heiße…</b> (I am called…) or <b>Ich bin…</b> (I am…). Both are natural: <b>Ich heiße Anna</b> and <b>Ich bin Anna</b> both introduce Anna. To ask someone's name, say <b>Wie heißt du?</b> (informal) or <b>Wie heißen Sie?</b> (formal). To say where you are from: <b>Ich komme aus Indien</b> (I come from India)."
    ]
   ],
   [
    "Du vs Sie — the register choice",
    [
     "German has two words for \"you\": <b>du</b> for friends, family, children, fellow students and increasingly colleagues, and <b>Sie</b> (always capitalised) for strangers, officials, and anyone you want to show distance to. The rule of thumb: wait for the older or higher-ranking person to offer <b>du</b>. Using <b>Sie</b> too long is merely stiff; using <b>du</b> too early can offend."
    ]
   ],
   [
    "Saying goodbye and thank you",
    [
     "The everyday goodbye is <b>Tschüss</b> (informal) or <b>Auf Wiedersehen</b> (formal, literally \"until seeing again\"). In the south you will hear <b>Servus</b> and in the north <b>Moin</b> — both can mean hello and goodbye. <b>Danke</b> is thanks; <b>Danke schön</b> adds warmth. The reply to thanks is <b>Bitte</b> — which also means \"please\" and \"here you are\"."
    ]
   ]
  ],
  "table": [
   [
    "Greeting",
    "When to use it"
   ],
   [
    [
     "Hallo",
     "hello — any time, any register"
    ],
    [
     "Guten Morgen",
     "good morning — until about 11"
    ],
    [
     "Guten Tag",
     "good day — late morning to afternoon"
    ],
    [
     "Guten Abend",
     "good evening — after about 6 pm"
    ],
    [
     "Tschüss",
     "bye — informal"
    ],
    [
     "Auf Wiedersehen",
     "goodbye — formal"
    ],
    [
     "Danke / Bitte",
     "thanks / please, you're welcome"
    ]
   ]
  ]
 },
 {
  "slug": "nouns-gender-and-articles",
  "title": "German Nouns, Gender and Articles",
  "desc": "Why every German noun is der, die or das, how to guess the gender, and the plural patterns that cover most words.",
  "sections": [
   [
    "Three genders, no escape",
    [
     "Every German noun has a gender — masculine (<b>der</b>), feminine (<b>die</b>) or neuter (<b>das</b>) — and the gender is a property of the word, not the thing. A girl is <b>das Mädchen</b> (neuter), a turnip is <b>die Rübe</b> (feminine). There is no way around memorising gender with each noun: learn <b>der Tisch</b> (the table), not just <b>Tisch</b>. Dictionaries always list it."
    ]
   ],
   [
    "Guessing rules that usually work",
    [
     "Some endings are reliable clues. Words ending in <b>-ung, -heit, -keit, -schaft, -ion, -tät</b> are almost always feminine (<b>die Zeitung</b>, the newspaper). Words ending in <b>-chen</b> and <b>-lein</b> (diminutives) are always neuter (<b>das Mädchen</b>, the girl). Most words ending in <b>-er</b> that describe people doing something are masculine (<b>der Lehrer</b>, the teacher). Days, months, seasons, compass directions and most car makes are masculine; most flowers, trees and numbers are feminine."
    ]
   ],
   [
    "Definite and indefinite articles",
    [
     "The definite article (the) is <b>der / die / das</b>; the indefinite article (a, an) is <b>ein</b> (masculine and neuter) and <b>eine</b> (feminine): <b>ein Mann</b> (a man), <b>eine Frau</b> (a woman), <b>ein Kind</b> (a child). German has no indefinite article in the plural — <b>Kinder</b> alone means \"children\" or \"some children\" depending on context. Professions and nationalities after <b>sein</b> (to be) also drop the article: <b>Ich bin Lehrer</b> (I am a teacher)."
    ]
   ],
   [
    "Plurals: five patterns",
    [
     "German plurals look chaotic but follow five main patterns: add <b>-e</b> (<b>der Tag → die Tage</b>, days), add <b>-er</b> often with an umlaut (<b>das Kind → die Kinder</b>), add <b>-(e)n</b> — the commonest feminine pattern (<b>die Frau → die Frauen</b>), add <b>-s</b> — mostly foreign words (<b>das Auto → die Autos</b>), or change nothing (<b>der Lehrer → die Lehrer</b>). All plurals take <b>die</b> as their definite article, whatever the singular gender."
    ]
   ]
  ],
  "table": [
   [
    "Article",
    "Use"
   ],
   [
    [
     "der",
     "the — masculine singular (der Mann)"
    ],
    [
     "die",
     "the — feminine singular AND all plurals"
    ],
    [
     "das",
     "the — neuter singular (das Kind)"
    ],
    [
     "ein",
     "a — masculine and neuter (ein Tag, ein Auto)"
    ],
    [
     "eine",
     "a — feminine (eine Frau)"
    ],
    [
     "kein / keine",
     "no, not a — the negative article"
    ]
   ]
  ]
 },
 {
  "slug": "sein-and-haben",
  "title": "Sein and Haben — To Be and To Have",
  "desc": "The two verbs every German sentence needs: full conjugations, the sentences they build, and negation with nicht and kein.",
  "sections": [
   [
    "Sein — to be, the irregular foundation",
    [
     "The verb <b>sein</b> (to be) is completely irregular and completely unavoidable: <b>ich bin</b> (I am), <b>du bist</b> (you are), <b>er/sie/es ist</b> (he/she/it is), <b>wir sind</b> (we are), <b>ihr seid</b> (you all are), <b>sie/Sie sind</b> (they/you-formal are). It identifies and describes: <b>Ich bin müde</b> (I am tired), <b>Das ist mein Bruder</b> (that is my brother). There is no continuous form — <b>Ich bin müde</b> covers both \"I am tired\" and \"I am being tired\"."
    ]
   ],
   [
    "Haben — to have, and more than having",
    [
     "<b>Haben</b> conjugates as <b>ich habe, du hast, er/sie/es hat, wir haben, ihr habt, sie/Sie haben</b>. It expresses possession (<b>Ich habe ein Auto</b> — I have a car) but also hunger, thirst, fear and cold, where English uses \"to be\": <b>Ich habe Hunger</b> (I am hungry, literally \"I have hunger\"), <b>Ich habe Angst</b> (I am afraid). Later it becomes the helper verb for the past tense, so learn it early and well."
    ]
   ],
   [
    "Negation: nicht vs kein",
    [
     "German negates in two ways. <b>Nicht</b> negates verbs, adjectives and whole sentences: <b>Ich bin nicht müde</b> (I am not tired), <b>Das ist nicht gut</b> (that is not good). <b>Kein</b> (declined like <b>ein</b>: kein/keine) negates nouns with indefinite articles or no article: <b>Ich habe kein Auto</b> (I have no car), <b>Das ist keine Frage</b> (that is no question). The shortcut: if English would use \"not a / no\" before a noun, German uses <b>kein</b>; otherwise <b>nicht</b>."
    ]
   ],
   [
    "The verb always comes second",
    [
     "In a German main clause the conjugated verb sits in second position — always. <b>Ich lerne Deutsch</b> (I learn German). Start with something else and the verb stays put while the subject moves after it: <b>Heute lerne ich Deutsch</b> (today learn I German). Yes-no questions invert: verb first, subject second — <b>Lernst du Deutsch?</b> (learn you German?). English word order will betray you here more than anywhere else."
    ]
   ]
  ],
  "table": [
   [
    "Person",
    "sein (to be) · haben (to have)"
   ],
   [
    [
     "ich (I)",
     "bin · habe"
    ],
    [
     "du (you, informal)",
     "bist · hast"
    ],
    [
     "er/sie/es (he/she/it)",
     "ist · hat"
    ],
    [
     "wir (we)",
     "sind · haben"
    ],
    [
     "ihr (you all)",
     "seid · habt"
    ],
    [
     "sie/Sie (they/you formal)",
     "sind · haben"
    ]
   ]
  ]
 },
 {
  "slug": "numbers-1-to-20",
  "title": "German Numbers 1 to 20",
  "desc": "Count to twenty, say your age, tell the time on the hour, and understand why German numbers run backwards after twelve.",
  "sections": [
   [
    "Eins to zwölf — learn them cold",
    [
     "The first twelve numbers are unique words: <b>eins, zwei, drei, vier, fünf, sechs, sieben, acht, neun, zehn, elf, zwölf</b>. Note the spellings that trip learners: <b>sechs</b> (six, pronounced \"zex\"), <b>sieben</b> (seven — the second syllable is short), and <b>zwölf</b> with its umlaut. Drill these until they are automatic; everything above twelve is built from them."
    ]
   ],
   [
    "Thirteen to nineteen — the -zehn pattern",
    [
     "Numbers 13–19 add <b>-zehn</b> (a worn-down form of <b>zehn</b>, ten): <b>dreizehn, vierzehn, fünfzehn, sechzehn, siebzehn, achtzehn, neunzehn</b>. Watch the two irregular stems: <b>sechzehn</b> (not \"sechszehn\") and <b>siebzehn</b> (not \"siebenzehn\") — the same shortened stems return in <b>sechzig</b> (60) and <b>siebzig</b> (70). Then <b>zwanzig</b> (20) closes the set."
    ]
   ],
   [
    "Backwards after twenty",
    [
     "From 21 on, German says the ones before the tens: 21 is <b>einundzwanzig</b> (one-and-twenty), 35 is <b>fünfunddreißig</b>. English did this too a thousand years ago (\"four-and-twenty blackbirds\") and then stopped; German kept it. Phone numbers and prices therefore demand full attention — <b>fünfundvierzig</b> (45) and <b>vierundfünfzig</b> (54) blur together at speed. Ask people to repeat: <b>Wie bitte?</b>"
    ]
   ],
   [
    "Age, time and quantities",
    [
     "Age uses <b>sein</b>, not <b>haben</b>: <b>Ich bin zwanzig Jahre alt</b> (I am twenty years old), asked as <b>Wie alt bist du?</b> (informal) or <b>Wie alt sind Sie?</b> (formal). Hours on the clock: <b>Es ist drei Uhr</b> (it is three o'clock). Counting objects needs no classifier — the number goes straight before the noun: <b>zwei Bücher</b> (two books), <b>drei Tassen Kaffee</b> (three cups of coffee)."
    ]
   ]
  ],
  "table": [
   [
    "Number",
    "German"
   ],
   [
    [
     "1–5",
     "eins, zwei, drei, vier, fünf"
    ],
    [
     "6–10",
     "sechs, sieben, acht, neun, zehn"
    ],
    [
     "11–15",
     "elf, zwölf, dreizehn, vierzehn, fünfzehn"
    ],
    [
     "16–20",
     "sechzehn, siebzehn, achtzehn, neunzehn, zwanzig"
    ],
    [
     "How old are you?",
     "Wie alt bist du? / Wie alt sind Sie?"
    ],
    [
     "I am 20 years old",
     "Ich bin zwanzig Jahre alt"
    ]
   ]
  ]
 },
 {
  "slug": "food-and-ordering",
  "title": "German Food and Ordering",
  "desc": "Order confidently in any German café or restaurant: the key phrases, table vocabulary, and how paying works.",
  "sections": [
   [
    "The magic phrase: Ich möchte…",
    [
     "Polite ordering in German runs on one phrase: <b>Ich möchte…</b> (I would like…). <b>Ich möchte einen Kaffee, bitte</b> (I would like a coffee, please) works everywhere — cafés, bakeries, restaurants. Add <b>bitte</b> (please) at the end and you sound gracious. Staff will ask <b>Was darf es sein?</b> (what may it be?) or <b>Was möchten Sie?</b> (what would you like?) — answer with your <b>Ich möchte…</b> and you are ordering like a local."
    ]
   ],
   [
    "At the table",
    [
     "Key table words: <b>die Speisekarte</b> (menu), <b>das Besteck</b> (cutlery), <b>das Glas</b> (glass), <b>die Tasse</b> (cup), <b>der Teller</b> (plate). To get attention, catch the server's eye and say <b>Entschuldigung!</b> (excuse me!). Germans say <b>Guten Appetit</b> before starting to eat — wait for it before touching your food. If something is delicious, say <b>Das schmeckt lecker!</b> (that tastes delicious!)."
    ]
   ],
   [
    "Paying the German way",
    [
     "Ask for the bill with <b>Die Rechnung, bitte</b> (the bill, please) — never <b>Zahlen, bitte</b> in writing, though you will hear it spoken. The server tells you the total; you state what you pay including tip, since card machines often lack a tip line: for a €18,50 bill say <b>Zwanzig, bitte</b> (twenty, please) and hand over €20. Five to ten percent is the normal tip — more looks showy, nothing looks rude."
    ]
   ],
   [
    "Hunger, thirst and taste",
    [
     "Hunger and thirst use <b>haben</b>: <b>Ich habe Hunger</b> (I am hungry), <b>Ich habe Durst</b> (I am thirsty). Core food words: <b>das Brot</b> (bread), <b>die Butter</b> (butter), <b>der Käse</b> (cheese), <b>das Wasser</b> (water), <b>die Milch</b> (milk), <b>der Apfel</b> (apple). Water must be specified: <b>stilles Wasser</b> (still) or <b>Sprudel / Wasser mit Kohlensäure</b> (sparkling) — unasked, you may get either."
    ]
   ]
  ],
  "table": [
   [
    "Phrase",
    "Meaning"
   ],
   [
    [
     "Ich möchte…, bitte",
     "I would like…, please — the ordering phrase"
    ],
    [
     "Die Speisekarte, bitte",
     "the menu, please"
    ],
    [
     "Die Rechnung, bitte",
     "the bill, please"
    ],
    [
     "Guten Appetit!",
     "enjoy your meal — said before eating"
    ],
    [
     "Das schmeckt lecker!",
     "that tastes delicious!"
    ],
    [
     "Ich habe Hunger / Durst",
     "I am hungry / thirsty"
    ]
   ]
  ]
 },
 {
  "slug": "present-tense-regular-verbs",
  "title": "German Present Tense — Regular Verbs",
  "desc": "One pattern that conjugates thousands of verbs: stems, endings, the e-insertion rule, and asking questions by inversion.",
  "sections": [
   [
    "Stem + ending — the whole system",
    [
     "Regular German verbs (the vast majority) conjugate by dropping <b>-en</b> from the infinitive and adding endings: <b>-e, -st, -t, -en, -t, -en</b>. So <b>lernen</b> (to learn) gives <b>ich lerne, du lernst, er lernt, wir lernen, ihr lernt, sie lernen</b>. Notice that <b>wir</b>, <b>sie</b> (they) and <b>Sie</b> (formal you) always match the infinitive — three persons for free. Learn one verb fully and you can conjugate thousands."
    ]
   ],
   [
    "The e-insertion rule",
    [
     "Stems ending in <b>-d, -t</b> or a consonant cluster like <b>-mn, -fn</b> insert an <b>e</b> before <b>-st</b> and <b>-t</b> so the word stays pronounceable: <b>arbeiten</b> (to work) gives <b>du arbeitest, er arbeitet</b> — never \"du arbeitst\". Similarly <b>finden</b> gives <b>du findest</b>. Stems ending in <b>-s, -ß, -x, -z</b> merge the ending: <b>du heißt</b> (not \"heißst\"), <b>du sitzt</b>."
    ]
   ],
   [
    "Questions by inversion",
    [
     "Yes-no questions invert verb and subject: <b>Lernst du Deutsch?</b> (do you learn German?), <b>Wohnt er in Berlin?</b> (does he live in Berlin?). There is no \"do\" helper verb — the main verb moves to the front and does the job. W-questions (question words) put the verb second: <b>Wo wohnst du?</b> (where do you live?), <b>Was lernst du?</b> (what are you learning?). Answer yes with <b>ja</b>, no with <b>nein</b>."
    ]
   ],
   [
    "Word order with two verbs",
    [
     "When a sentence has a modal verb (want, can, must) plus a main verb, the modal takes second position and the main verb goes to the very end in infinitive form: <b>Ich möchte Deutsch lernen</b> (I want to learn German), <b>Er kann gut kochen</b> (he can cook well). This \"verb bracket\" — conjugated verb second, infinitive last — is the single most important German sentence pattern after verb-second itself."
    ]
   ]
  ],
  "table": [
   [
    "Person",
    "lernen (to learn)"
   ],
   [
    [
     "ich",
     "lerne"
    ],
    [
     "du",
     "lernst"
    ],
    [
     "er / sie / es",
     "lernt"
    ],
    [
     "wir",
     "lernen"
    ],
    [
     "ihr",
     "lernt"
    ],
    [
     "sie / Sie",
     "lernen"
    ]
   ]
  ]
 }
]

PRACTICE = {
 "vocabulary": [
  {"q": "What does “Guten Tag” mean?", "a": "good day", "opts": ["good morning", "good day", "good evening", "good night"], "explain": "Guten Tag is good day — used from late morning through the afternoon."},
  {"q": "What does “Tschüss” mean?", "a": "bye (informal)", "opts": ["hello", "bye (informal)", "thanks", "please"], "explain": "Tschüss is the everyday informal goodbye."},
  {"q": "“Danke” means…", "a": "thanks", "opts": ["please", "thanks", "sorry", "yes"], "explain": "Danke is thanks; the reply is Bitte (you're welcome)."},
  {"q": "“Bitte” does NOT mean…", "a": "goodbye", "opts": ["please", "you're welcome", "here you are", "goodbye"], "explain": "Bitte covers please, you're welcome and here you are — but never goodbye."},
  {"q": "What does “die Rechnung” mean?", "a": "the bill", "opts": ["the menu", "the bill", "the table", "the tip"], "explain": "Die Rechnung, bitte — the bill, please."},
  {"q": "“Ich habe Hunger” means…", "a": "I am hungry", "opts": ["I am thirsty", "I am hungry", "I am tired", "I am cold"], "explain": "Hunger uses haben: Ich habe Hunger — literally I have hunger."},
  {"q": "What does “das Brot” mean?", "a": "bread", "opts": ["bread", "cheese", "water", "apple"], "explain": "Das Brot is bread — neuter, like most staple foods is not; just memorise it."},
  {"q": "“zwölf” is the number…", "a": "12", "opts": ["10", "11", "12", "20"], "explain": "Elf is 11, zwölf is 12 — then dreizehn (13)."},
  {"q": "What does “Guten Appetit” mean?", "a": "enjoy your meal", "opts": ["the bill please", "enjoy your meal", "table for two", "no sugar"], "explain": "Guten Appetit is said before starting to eat — wait for it."},
  {"q": "“Entschuldigung!” is used to…", "a": "get attention politely", "opts": ["order food", "get attention politely", "say goodbye", "ask the price"], "explain": "Entschuldigung means excuse me — to call a server or apologise."},
  {"q": "What does “das Mädchen” show about gender?", "a": "gender follows the word, not the thing", "opts": ["all girls are feminine", "gender follows the word, not the thing", "all people are masculine", "gender is random"], "explain": "Das Mädchen (the girl) is neuter because of the -chen ending."},
  {"q": "“Wie bitte?” means…", "a": "pardon? / say again?", "opts": ["how much?", "pardon? / say again?", "where?", "why?"], "explain": "Wie bitte? is the polite pardon? — use it when numbers blur past."}
 ],
 "grammar": [
  {"q": "The article for a masculine noun (the man) is…", "a": "der Mann", "opts": ["der Mann", "die Mann", "das Mann", "den Mann"], "explain": "Masculine takes der: der Mann."},
  {"q": "The article for a feminine noun (the woman) is…", "a": "die Frau", "opts": ["der Frau", "die Frau", "das Frau", "ein Frau"], "explain": "Feminine takes die: die Frau."},
  {"q": "The article for a neuter noun (the child) is…", "a": "das Kind", "opts": ["der Kind", "die Kind", "das Kind", "dem Kind"], "explain": "Neuter takes das: das Kind."},
  {"q": "“A woman” is…", "a": "eine Frau", "opts": ["ein Frau", "eine Frau", "einer Frau", "einen Frau"], "explain": "Feminine indefinite article is eine: eine Frau."},
  {"q": "The plural of “das Kind” is…", "a": "die Kinder", "opts": ["die Kindes", "die Kinder", "die Kinden", "die Kind"], "explain": "Das Kind → die Kinder — the -er plural with umlaut."},
  {"q": "“I am” is…", "a": "ich bin", "opts": ["ich bin", "ich bist", "ich ist", "ich sind"], "explain": "Sein: ich bin, du bist, er ist."},
  {"q": "“You (informal) have” is…", "a": "du hast", "opts": ["du habe", "du hast", "du hat", "du haben"], "explain": "Haben: ich habe, du hast, er hat."},
  {"q": "“I have no car” is…", "a": "Ich habe kein Auto", "opts": ["Ich habe nicht Auto", "Ich habe kein Auto", "Ich nicht habe Auto", "Ich habe keine Auto"], "explain": "Negating a noun with ein/no article uses kein (neuter: kein Auto)."},
  {"q": "“He learns German” is…", "a": "Er lernt Deutsch", "opts": ["Er lernen Deutsch", "Er lernt Deutsch", "Er lernst Deutsch", "Er lerne Deutsch"], "explain": "Regular verbs: er/sie/es take -t — er lernt."},
  {"q": "“Do you learn German?” is…", "a": "Lernst du Deutsch?", "opts": ["Du lernst Deutsch?", "Lernst du Deutsch?", "Lernen du Deutsch?", "Lernt du Deutsch?"], "explain": "Yes-no questions invert: verb first — Lernst du Deutsch?"},
  {"q": "“You (all) work” is…", "a": "ihr arbeitet", "opts": ["ihr arbeiten", "ihr arbeitet", "ihr arbeitst", "ihr arbeite"], "explain": "Arbeiten inserts e: ihr arbeitet — never arbeitst."},
  {"q": "In “Heute lerne ich Deutsch”, the verb position shows…", "a": "the verb always comes second", "opts": ["the verb comes first", "the verb always comes second", "the verb comes last", "free word order"], "explain": "German main clauses are verb-second, whatever starts the sentence."}
 ]
}

QUIZ = [
 {"id": "de-greet-1", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "What does “Guten Morgen” mean?", "a": "good morning", "opts": ["good morning", "good day", "good evening", "good night"], "explain": "Guten Morgen is good morning — used until about 11."},
 {"id": "de-greet-2", "lesson": "greetings-and-introductions", "type": "usage", "topic": "greetings", "level": "beginner", "q": "You meet a stranger at 3 pm. You say…", "a": "Guten Tag", "opts": ["Guten Morgen", "Guten Tag", "Gute Nacht", "Moin Moin"], "explain": "Afternoon calls for Guten Tag; Gute Nacht is a farewell only."},
 {"id": "de-greet-3", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "“Ich heiße Anna” means…", "a": "I am called Anna", "opts": ["I am called Anna", "I know Anna", "I see Anna", "I help Anna"], "explain": "Ich heiße… introduces your name — I am called…"},
 {"id": "de-greet-4", "lesson": "greetings-and-introductions", "type": "usage", "topic": "greetings", "level": "beginner", "q": "Ask a stranger's name (formal). You say…", "a": "Wie heißen Sie?", "opts": ["Wie heißt du?", "Wie heißen Sie?", "Wer bist du?", "Was bist du?"], "explain": "Strangers get Sie: Wie heißen Sie?"},
 {"id": "de-noun-1", "lesson": "nouns-gender-and-articles", "type": "vocab", "topic": "grammar", "level": "beginner", "q": "Which article goes with “Tisch” (table, masculine)?", "a": "der", "opts": ["der", "die", "das", "den"], "explain": "Der Tisch — masculine takes der."},
 {"id": "de-noun-2", "lesson": "nouns-gender-and-articles", "type": "vocab", "topic": "grammar", "level": "beginner", "q": "A word ending in -ung is almost always…", "a": "feminine", "opts": ["masculine", "feminine", "neuter", "plural"], "explain": "-ung, -heit, -keit are reliably feminine: die Zeitung."},
 {"id": "de-noun-3", "lesson": "nouns-gender-and-articles", "type": "meaning", "topic": "grammar", "level": "beginner", "q": "“Ich bin Lehrer” drops the article because…", "a": "professions after sein take no article", "opts": ["Lehrer is plural", "professions after sein take no article", "Lehrer is feminine", "articles are optional"], "explain": "Professions and nationalities after sein drop ein: Ich bin Lehrer."},
 {"id": "de-sein-1", "lesson": "sein-and-haben", "type": "vocab", "topic": "verbs", "level": "beginner", "q": "“We are” is…", "a": "wir sind", "opts": ["wir sind", "wir seid", "wir bin", "wir ist"], "explain": "Sein: wir sind — same as sie/Sie sind."},
 {"id": "de-sein-2", "lesson": "sein-and-haben", "type": "usage", "topic": "verbs", "level": "beginner", "q": "Say “I am not tired”. You say…", "a": "Ich bin nicht müde", "opts": ["Ich bin nicht müde", "Ich bin kein müde", "Ich nicht bin müde", "Ich bin müde nicht"], "explain": "Adjectives negate with nicht: Ich bin nicht müde."},
 {"id": "de-sein-3", "lesson": "sein-and-haben", "type": "meaning", "topic": "verbs", "level": "beginner", "q": "“Ich habe Angst” means…", "a": "I am afraid", "opts": ["I am afraid", "I am hungry", "I have fearfulness", "I fear having"], "explain": "Fear, hunger and cold use haben: Ich habe Angst."},
 {"id": "de-num-1", "lesson": "numbers-1-to-20", "type": "vocab", "topic": "numbers", "level": "beginner", "q": "“sieben” is the number…", "a": "7", "opts": ["6", "7", "9", "11"], "explain": "Sechs is 6, sieben is 7 — short second syllable."},
 {"id": "de-num-2", "lesson": "numbers-1-to-20", "type": "vocab", "topic": "numbers", "level": "beginner", "q": "“sechzehn” is…", "a": "16", "opts": ["6", "16", "60", "66"], "explain": "Sechzehn is 16 — note the shortened sech- stem."},
 {"id": "de-num-3", "lesson": "numbers-1-to-20", "type": "usage", "topic": "numbers", "level": "beginner", "q": "Say “I am 20 years old”. You say…", "a": "Ich bin zwanzig Jahre alt", "opts": ["Ich habe zwanzig Jahre", "Ich bin zwanzig Jahre alt", "Ich bin zwanzig alt Jahre", "Ich werde zwanzig"], "explain": "Age uses sein: Ich bin zwanzig Jahre alt."},
 {"id": "de-food-1", "lesson": "food-and-ordering", "type": "usage", "topic": "food", "level": "beginner", "q": "Order a coffee politely. You say…", "a": "Ich möchte einen Kaffee, bitte", "opts": ["Ich möchte einen Kaffee, bitte", "Ich will Kaffee jetzt", "Kaffee geben mir", "Ich habe Kaffee gern"], "explain": "Ich möchte… bitte is the polite ordering phrase."},
 {"id": "de-food-2", "lesson": "food-and-ordering", "type": "meaning", "topic": "food", "level": "beginner", "q": "“Die Rechnung, bitte” means…", "a": "the bill, please", "opts": ["the menu, please", "the bill, please", "table for two", "one more, please"], "explain": "Die Rechnung is the bill — never rush it."},
 {"id": "de-food-3", "lesson": "food-and-ordering", "type": "vocab", "topic": "food", "level": "beginner", "q": "“Still” water is…", "a": "stilles Wasser", "opts": ["stilles Wasser", "Sprudel", "Leitungswasser", "Mineralwasser kalt"], "explain": "Stilles Wasser is still water; Sprudel is sparkling."},
 {"id": "de-verb-1", "lesson": "present-tense-regular-verbs", "type": "vocab", "topic": "verbs", "level": "beginner", "q": "“Du lernst” — the ending -st marks…", "a": "du (you, informal)", "opts": ["ich", "du (you, informal)", "er", "wir"], "explain": "The -st ending always marks du."},
 {"id": "de-verb-2", "lesson": "present-tense-regular-verbs", "type": "usage", "topic": "verbs", "level": "beginner", "q": "Ask “where do you live?” (informal). You say…", "a": "Wo wohnst du?", "opts": ["Wo wohnst du?", "Wo wohnt du?", "Wo wohnen du?", "Wo wohne du?"], "explain": "W-questions keep the verb second: Wo wohnst du?"},
 {"id": "de-verb-3", "lesson": "present-tense-regular-verbs", "type": "meaning", "topic": "verbs", "level": "beginner", "q": "In “Ich möchte Deutsch lernen”, “lernen” sits last because…", "a": "the main verb goes last with a modal", "opts": ["German verbs always end sentences", "the main verb goes last with a modal", "lernen is irregular", "möchte is not a verb"], "explain": "Modal second, main verb last — the verb bracket."},
 {"id": "de-greet-5", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "“Auf Wiedersehen” literally means…", "a": "until seeing again", "opts": ["until seeing again", "go with God", "stay well", "good luck"], "explain": "Auf Wiedersehen — until seeing again — the formal goodbye."}
]

REVIEW = [
 {"p": "Hallo", "a": "hello"},
 {"p": "Guten Morgen", "a": "good morning"},
 {"p": "Guten Tag", "a": "good day"},
 {"p": "Guten Abend", "a": "good evening"},
 {"p": "Tschüss", "a": "bye (informal)"},
 {"p": "Danke", "a": "thanks"},
 {"p": "Bitte", "a": "please / you're welcome"},
 {"p": "Ich heiße…", "a": "I am called…"},
 {"p": "der / die / das", "a": "the (m / f / n)"},
 {"p": "ein / eine", "a": "a (m+n / f)"},
 {"p": "ich bin", "a": "I am"},
 {"p": "du bist", "a": "you are (informal)"},
 {"p": "er ist", "a": "he is"},
 {"p": "ich habe", "a": "I have"},
 {"p": "du hast", "a": "you have (informal)"},
 {"p": "nicht / kein", "a": "not / no, not a"},
 {"p": "eins, zwei, drei", "a": "one, two, three"},
 {"p": "zwölf", "a": "twelve"},
 {"p": "zwanzig", "a": "twenty"},
 {"p": "Ich möchte…", "a": "I would like…"},
 {"p": "Die Rechnung, bitte", "a": "the bill, please"},
 {"p": "Guten Appetit!", "a": "enjoy your meal!"},
 {"p": "ich lerne", "a": "I learn"},
 {"p": "Wo wohnst du?", "a": "where do you live?"}
]

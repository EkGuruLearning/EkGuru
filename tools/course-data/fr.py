#!/usr/bin/env python3
"""Authored French course data (Stage 8). Language config + content.
Loaded by tools/build-language-course.py. Do not hand-edit the generated
output pages; edit THIS file and regenerate.
Content is authored by hand, not machine-translated.
"""

COURSE = {
    "lang": "fr", "name": "French", "native": "français", "speechTag": "fr-FR",
    "status": "Available",
    "note": ("A real, authored French course: 6 lessons, a practice lab, a topic "
             "quiz and a review deck — all running on the same engines as Hindi. It is not "
             "yet as deep as the Hindi course, and all audio is your browser's computer "
             "voice, never a native recording."),
}

LESSONS = [
    {
        "slug": "greetings-and-introductions",
        "title": "French Greetings and Introductions",
        "desc": "Every French greeting you actually need, when to use tu and vous, and how to introduce yourself — with pronunciation notes.",
        "sections": [
            ("The greetings that cover most situations", [
                "French greetings are smaller in number than English ones. <b>Bonjour</b> (hello / good morning) works from dawn to dusk, in shops, offices and on the phone. After about 6pm people switch to <b>bonsoir</b> (good evening). <b>Salut</b> is the casual hi for friends, and <b>bonne nuit</b> (good night) is only said when someone is going to bed.",
            ]),
            ("Introducing yourself", [
                "To give your name, say <b>Je m'appelle</b> (literally \"I call myself\") or <b>Je suis</b> (I am): <b>Je m'appelle Marie</b> / <b>Je suis Marie</b>. To ask someone's name: <b>Comment tu t'appelles ?</b> (informal) or <b>Comment vous appelez-vous ?</b> (formal).",
            ]),
            ("Tu vs vous — the register choice", [
                "French has two words for \"you\": <b>tu</b> for friends, family, children and close peers, and <b>vous</b> for strangers, older people, and formal situations — <b>vous</b> is also the plural \"you all\". When unsure, <b>vous</b> is the safer, more respectful choice, and French speakers often wait to be invited to use <b>tu</b>.",
            ]),
            ("Ça va ? — asking how someone is", [
                "<b>Ça va ?</b> and <b>Comment ça va ?</b> mean \"how's it going?\" (informal); the formal version is <b>Comment allez-vous ?</b>. Everyday answers: <b>Ça va bien, merci</b> (fine, thanks), <b>Très bien</b> (very well), or <b>Pas mal</b> (not bad).",
            ]),
        ],
        "table": (("Greeting", "When to use it"), [
            ("bonjour", "hello / good morning — all day, any register"),
            ("salut", "hi — casual, friends only"),
            ("bonsoir", "good evening — after ~6pm"),
            ("bonne nuit", "good night — when leaving / going to sleep"),
            ("au revoir", "goodbye"),
            ("à bientôt", "see you soon"),
        ]),
    },
    {
        "slug": "etre-and-avoir",
        "title": "Être and Avoir — The Two Verbs You Can't Live Without",
        "desc": "The two most common French verbs, how to conjugate them, and why French says \"I have 20 years\" instead of \"I am 20\".",
        "sections": [
            ("Why start here", [
                "<b>Être</b> (to be) and <b>avoir</b> (to have) are the two most frequent verbs in French. You need them for descriptions, possession, and — surprisingly — for age, hunger and thirst, where French uses <b>avoir</b> where English uses \"to be\".",
            ]),
            ("Être — to be", [
                "<b>je suis, tu es, il/elle est, nous sommes, vous êtes, ils/elles sont</b>. Examples: <b>Je suis de l'Inde</b> (I am from India), <b>Je suis étudiant</b> (I am a student). Nationality, origin and profession all use <b>être</b>.",
            ]),
            ("Avoir — to have", [
                "<b>j'ai, tu as, il/elle a, nous avons, vous avez, ils/elles ont</b>. Notice <b>je ai</b> becomes <b>j'ai</b> — the vowel runs together. Examples: <b>J'ai un frère</b> (I have a brother), <b>Nous avons une voiture</b> (we have a car).",
            ]),
            ("Avoir for age and feelings", [
                "French literally \"has\" its age and feelings: <b>J'ai vingt ans</b> (I am 20 years old), <b>J'ai faim</b> (I am hungry), <b>J'ai soif</b> (I am thirsty), <b>J'ai chaud</b> (I am hot), <b>J'ai froid</b> (I am cold). Never say <i>je suis faim</i> — that is a classic learner error.",
            ]),
        ],
        "table": (("Meaning", "être", "avoir"), [
            ("I am / I have", "je suis", "j'ai"),
            ("you (informal) are / have", "tu es", "tu as"),
            ("he/she is / has", "il/elle est", "il/elle a"),
            ("we are / have", "nous sommes", "nous avons"),
            ("they are / have", "ils/elles sont", "ils/elles ont"),
        ]),
    },
    {
        "slug": "gender-and-articles",
        "title": "Gender and Articles in French",
        "desc": "Why every French noun is masculine or feminine, and the words for \"the\" and \"a\" — le, la, les, un, une.",
        "sections": [
            ("Every noun is masculine or feminine", [
                "Every French noun has a gender, and it shows in the article. <b>Le</b> is \"the\" for masculine singular, <b>la</b> for feminine singular, <b>les</b> for all plurals. <b>Un</b> and <b>une</b> mean \"a\" for masculine and feminine. Before a vowel, both le and la become <b>l'</b>: <b>l'ami</b>, <b>l'eau</b>, <b>l'école</b>.",
            ]),
            ("How to guess the gender", [
                "Most nouns ending in <b>-e</b> are feminine (<b>la table</b>, <b>la porte</b>) — but there are big exceptions like <b>le livre</b> (book) and <b>le fromage</b> (cheese). Some endings are reliable: <b>-tion, -sion, -té, -ette</b> are feminine (<b>la nation</b>, <b>la liberté</b>), while <b>-age, -ment, -eau</b> are masculine (<b>le voyage</b>, <b>le château</b>).",
            ]),
            ("Making plurals", [
                "Plurals usually add a silent <b>-s</b>: <b>les livres</b>, <b>les maisons</b>. Words ending in <b>-eau</b> or <b>-eu</b> take <b>-x</b> instead: <b>le château → les châteaux</b>. The article <b>les</b> is the only real clue in speech, because the -s is not pronounced.",
            ]),
            ("Agreement with adjectives", [
                "Adjectives agree with the noun. Most add <b>-e</b> for the feminine: <b>petit / petite</b>, <b>grand / grande</b> — <b>un petit livre</b> but <b>une petite maison</b>. Adjectives ending in <b>-e</b> already stay the same: <b>rouge</b>, <b>jeune</b>.",
            ]),
        ],
        "table": (("Article", "Meaning"), [
            ("le", "the — masculine singular"),
            ("la", "the — feminine singular"),
            ("les", "the — all plurals"),
            ("l'", "the — before a vowel (le/la elided)"),
            ("un / une", "a — masculine / feminine"),
        ]),
    },
    {
        "slug": "numbers-1-to-20",
        "title": "French Numbers 1 to 20",
        "desc": "The first twenty numbers, how to pronounce the tricky ones, and how to ask prices.",
        "sections": [
            ("1 to 10", [
                "<b>un, deux, trois, quatre, cinq, six, sept, huit, neuf, dix</b>. Watch the silent endings: <b>deux, trois, six, dix</b> all end in a silent consonant when alone.",
            ]),
            ("11 to 16", [
                "<b>onze, douze, treize, quatorze, quinze, seize</b>. These are single words with no pattern — memorise them. Note the <b>z</b> sound in <b>onze</b> and <b>quinze</b>.",
            ]),
            ("17 to 20", [
                "From 17 the pattern appears: <b>dix-sept</b> (17, \"ten-seven\"), <b>dix-huit</b> (18), <b>dix-neuf</b> (19), then <b>vingt</b> (20). The hyphen joins the parts, and <b>vingt</b> keeps its final -t silent.",
            ]),
            ("Asking and saying prices", [
                "<b>C'est combien ?</b> and <b>Ça coûte combien ?</b> both mean \"how much is it?\". The answer is just the number with <b>euros</b>: <b>C'est dix euros</b> (it's ten euros), <b>Vingt euros</b> (twenty euros).",
            ]),
        ],
        "table": (("Number", "French"), [
            ("1", "un"), ("2", "deux"), ("3", "trois"), ("4", "quatre"), ("5", "cinq"),
            ("6", "six"), ("7", "sept"), ("8", "huit"), ("9", "neuf"), ("10", "dix"),
            ("16", "seize"), ("20", "vingt"),
        ]),
    },
    {
        "slug": "food-and-ordering",
        "title": "Food and Ordering in French",
        "desc": "The phrases that get you fed: ordering politely, asking for the bill, and the words every menu uses.",
        "sections": [
            ("Ordering politely", [
                "The polite way to order is <b>Je voudrais…</b> (I would like): <b>Je voudrais un café, s'il vous plaît</b>. <b>Je prends…</b> (I'll take…) is also common and natural. Always add <b>s'il vous plaît</b> — French politeness depends on it.",
            ]),
            ("Water and drinks", [
                "<b>L'eau</b> is water. In France, tap water is free in restaurants — ask for <b>une carafe d'eau</b> (a jug of tap water). Sparkling water is <b>l'eau gazeuse</b>. For the rest: <b>un café</b> (an espresso), <b>un thé</b> (a tea), <b>un verre de vin</b> (a glass of wine).",
            ]),
            ("The bill", [
                "Ask for the bill with <b>L'addition, s'il vous plaît</b>. In France service is included (<b>service compris</b>) — a tip (<b>un pourboire</b>) is optional, usually just rounding up. In Québec you will hear <b>la facture</b> instead of <b>l'addition</b>.",
            ]),
            ("Useful menu words", [
                "<b>Entrée</b> (starter), <b>plat principal</b> (main course), <b>dessert</b> (dessert), <b>sans</b> (without) and <b>avec</b> (with): <b>sans oignons</b> (without onions), <b>avec glace</b> (with ice). <b>Végétarien</b> means vegetarian.",
            ]),
        ],
        "table": (("French", "English"), [
            ("Je voudrais…", "I would like…"),
            ("L'addition, s'il vous plaît", "The bill, please"),
            ("une carafe d'eau", "a jug of (tap) water"),
            ("Qu'est-ce que vous recommandez ?", "What do you recommend?"),
            ("sans / avec", "without / with"),
        ]),
    },
    {
        "slug": "present-tense-regular-verbs",
        "title": "French Present Tense — Regular Verbs",
        "desc": "The three verb groups (-er, -ir, -re) and the endings that let you conjugate any regular verb.",
        "sections": [
            ("Three groups, three sets of endings", [
                "Regular French verbs fall into three groups by their infinitive ending: <b>-er</b> (the biggest: <b>parler</b>, to speak), <b>-ir</b> (<b>finir</b>, to finish), and <b>-re</b> (<b>vendre</b>, to sell). Once you know each group's endings, you can conjugate any regular verb you meet.",
            ]),
            ("-er verbs: parler (to speak)", [
                "<b>je parle, tu parles, il/elle parle, nous parlons, vous parlez, ils/elles parlent</b>. Notice that <b>je parle</b>, <b>tu parles</b> and <b>il parle</b> all sound identical — the endings -e, -es and -ent are silent. Only <b>nous</b> and <b>vous</b> sound clearly different.",
            ]),
            ("-ir verbs: finir (to finish)", [
                "<b>je finis, tu finis, il/elle finit, nous finissons, vous finissez, ils/elles finissent</b>. The -ir group keeps an <b>-iss-</b> in the plural forms — that's the sign of a regular -ir verb.",
            ]),
            ("-re verbs: vendre (to sell)", [
                "<b>je vends, tu vends, il/elle vend, nous vendons, vous vendez, ils/elles vendent</b>. The -re group drops the final -re and adds -s, -s, (nothing), -ons, -ez, -ent.",
            ]),
        ],
        "table": (("Person", "-er (parler)", "-ir (finir)", "-re (vendre)"), [
            ("je (I)", "parle", "finis", "vends"),
            ("tu (you)", "parles", "finis", "vends"),
            ("il/elle (he/she)", "parle", "finit", "vend"),
            ("nous (we)", "parlons", "finissons", "vendons"),
            ("ils/elles (they)", "parlent", "finissent", "vendent"),
        ]),
    },
]

# practice banks (reuse practice-engine.js). `say` = the French text to speak.
PRACTICE = {
    "vocabulary": [
        {"q": "What does “bonjour” mean?", "a": "hello", "opts": ["goodbye", "hello", "please", "thanks"], "explain": "Bonjour is hello/good morning — used all day.", "say": "bonjour"},
        {"q": "What does “merci” mean?", "a": "thank you", "opts": ["please", "thank you", "sorry", "yes"], "explain": "Merci is thank you. The reply is de rien (you're welcome).", "say": "merci"},
        {"q": "What does “s'il vous plaît” mean?", "a": "please", "opts": ["please", "thank you", "excuse me", "goodbye"], "explain": "S'il vous plaît is please — the formal/polite form.", "say": "s'il vous plaît"},
        {"q": "What does “au revoir” mean?", "a": "goodbye", "opts": ["hello", "goodbye", "good night", "welcome"], "explain": "Au revoir is goodbye.", "say": "au revoir"},
        {"q": "What does “oui” mean?", "a": "yes", "opts": ["no", "yes", "maybe", "please"], "explain": "Oui is yes; non is no.", "say": "oui"},
        {"q": "What does “l'eau” mean?", "a": "water", "opts": ["bread", "water", "wine", "milk"], "explain": "L'eau is water (feminine: la eau → l'eau).", "say": "l'eau"},
        {"q": "What does “la maison” mean?", "a": "house", "opts": ["car", "house", "street", "room"], "explain": "La maison is the house or home.", "say": "la maison"},
        {"q": "What does “un ami” mean?", "a": "a friend", "opts": ["a brother", "a friend", "a teacher", "a neighbour"], "explain": "Un ami is a friend (masculine); une amie is the feminine form.", "say": "un ami"},
        {"q": "What does “le travail” mean?", "a": "work", "opts": ["work", "holiday", "money", "time"], "explain": "Le travail is work; travailler is to work.", "say": "le travail"},
        {"q": "What does “aujourd'hui” mean?", "a": "today", "opts": ["tomorrow", "today", "yesterday", "now"], "explain": "Aujourd'hui is today; demain is tomorrow; hier is yesterday.", "say": "aujourd'hui"},
        {"q": "What does “la nuit” mean?", "a": "night", "opts": ["day", "night", "morning", "week"], "explain": "La nuit is night — as in bonne nuit.", "say": "la nuit"},
        {"q": "What does “non” mean?", "a": "no", "opts": ["yes", "no", "maybe", "never"], "explain": "Non is no — the partner of oui.", "say": "non"},
    ],
    "grammar": [
        {"q": "“Je suis de l'Inde” uses être because…", "a": "origin uses être", "opts": ["origin uses être", "location uses être", "mood uses être", "it is a temporary state"], "explain": "Origin and identity are permanent — they use être.", "say": "je suis de l'Inde"},
        {"q": "“J'ai faim” (I am hungry) uses avoir because…", "a": "French uses avoir for hunger", "opts": ["French uses avoir for hunger", "it is about identity", "it is about origin", "faim is a verb"], "explain": "Age, hunger, thirst, heat and cold all use avoir in French.", "say": "j'ai faim"},
        {"q": "“J'ai vingt ans” literally means…", "a": "I have twenty years", "opts": ["I am twenty years old", "I have twenty years", "I want twenty years", "I like twenty years"], "explain": "French says \"I have 20 years\", not \"I am 20\".", "say": "j'ai vingt ans"},
        {"q": "“Le livre” vs “la table” — why different articles?", "a": "livre is masculine, table is feminine", "opts": ["livre is masculine, table is feminine", "table is plural", "livre is plural", "both are neutral"], "explain": "Livre is masculine (le), table is feminine (la) despite ending in -e.", "say": "le livre"},
        {"q": "Which is correct: “l'ami” or “le ami”?", "a": "l'ami", "opts": ["le ami", "l'ami", "la ami", "les ami"], "explain": "Le elides to l' before a vowel: l'ami.", "say": "l'ami"},
        {"q": "How do you make a sentence negative: “I don't speak English”?", "a": "Je ne parle pas anglais", "opts": ["Je ne parle pas anglais", "Je parle pas anglais jamais", "Je non parle anglais", "Je parle ne anglais pas"], "explain": "Negation wraps the verb with ne … pas.", "say": "je ne parle pas anglais"},
        {"q": "“Je parle” means…", "a": "I speak", "opts": ["I speak", "he speaks", "we speak", "they speak"], "explain": "The -e ending (silent) marks the je form of -er verbs.", "say": "je parle"},
        {"q": "“Nous parlons” means…", "a": "we speak", "opts": ["I speak", "we speak", "they speak", "he speaks"], "explain": "-ons is the nous (we) ending for -er verbs.", "say": "nous parlons"},
        {"q": "How do you ask a friend's name?", "a": "Comment tu t'appelles ?", "opts": ["Comment vous appelez-vous ?", "Comment tu t'appelles ?", "Qu'est-ce que c'est ?", "Où es-tu ?"], "explain": "Comment tu t'appelles ? is the informal (tu) form.", "say": "comment tu t'appelles ?"},
        {"q": "“Je m'appelle Marie” literally means…", "a": "I call myself Marie", "opts": ["My name is Marie", "I call myself Marie", "Call me Marie", "Marie is my name"], "explain": "S'appeler is reflexive: je m'appelle = I call myself.", "say": "je m'appelle Marie"},
        {"q": "Which means “the bill, please”?", "a": "L'addition, s'il vous plaît", "opts": ["L'addition, s'il vous plaît", "La nourriture, s'il vous plaît", "La maison, s'il vous plaît", "Le menu, s'il vous plaît"], "explain": "L'addition is the bill/check.", "say": "l'addition, s'il vous plaît"},
        {"q": "“Je voudrais un café” means…", "a": "I would like a coffee", "opts": ["I want a coffee now", "I would like a coffee", "I had a coffee", "The coffee is cold"], "explain": "Je voudrais is the polite conditional — “I would like”.", "say": "je voudrais un café"},
    ],
}

# topic quiz (daily rotation). topic + level + type like the Hindi quiz bank.
QUIZ = [
    {"id": "fr-greet-1", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner",
     "q": "What does “bonjour” mean?", "a": "hello / good morning", "opts": ["good night", "hello / good morning", "good evening", "goodbye"],
     "explain": "Bonjour is hello/good morning — used all day until evening."},
    {"id": "fr-greet-2", "lesson": "greetings-and-introductions", "type": "usage", "topic": "greetings", "level": "beginner",
     "q": "“Salut” is best used with…", "a": "friends and family", "opts": ["strangers", "friends and family", "a police officer", "your boss"],
     "explain": "Salut is the casual hi — for friends and family, not formal situations."},
    {"id": "fr-greet-3", "lesson": "greetings-and-introductions", "type": "usage", "topic": "greetings", "level": "beginner",
     "q": "After about 6pm, “bonjour” becomes…", "a": "bonsoir", "opts": ["bonne nuit", "bonsoir", "salut", "au revoir"],
     "explain": "Bonsoir (good evening) replaces bonjour in the evening."},
    {"id": "fr-greet-4", "lesson": "greetings-and-introductions", "type": "usage", "topic": "greetings", "level": "beginner",
     "q": "When should you use “vous” instead of “tu”?", "a": "With strangers and in formal situations", "opts": ["With friends", "With children", "With strangers and in formal situations", "Never"],
     "explain": "Vous is the formal “you” (and the plural) — safer with strangers."},
    {"id": "fr-etre-1", "lesson": "etre-and-avoir", "type": "usage", "topic": "grammar", "level": "beginner",
     "q": "“Je suis étudiant” uses être because…", "a": "profession uses être", "opts": ["profession uses être", "location uses être", "mood uses être", "it is temporary"],
     "explain": "Identity and profession are permanent — they use être."},
    {"id": "fr-etre-2", "lesson": "etre-and-avoir", "type": "usage", "topic": "grammar", "level": "beginner",
     "q": "How do you say “I am 20 years old” in French?", "a": "J'ai vingt ans", "opts": ["Je suis vingt ans", "J'ai vingt ans", "Je suis vingt années", "J'ai vingt années"],
     "explain": "French uses avoir for age: J'ai vingt ans (I have 20 years)."},
    {"id": "fr-etre-3", "lesson": "etre-and-avoir", "type": "meaning", "topic": "grammar", "level": "beginner",
     "q": "“J'ai soif” means…", "a": "I am thirsty", "opts": ["I am hungry", "I am thirsty", "I am tired", "I am cold"],
     "explain": "J'ai soif = I am thirsty (literally \"I have thirst\")."},
    {"id": "fr-etre-4", "lesson": "etre-and-avoir", "type": "usage", "topic": "grammar", "level": "beginner",
     "q": "Why is it “j'ai” and not “je ai”?", "a": "je + ai elides to j'ai", "opts": ["je + ai elides to j'ai", "ai is wrong", "it is the plural", "it is the formal form"],
     "explain": "Je elides to j' before a vowel sound: j'ai, j'habite."},
    {"id": "fr-gender-1", "lesson": "gender-and-articles", "type": "usage", "topic": "grammar", "level": "beginner",
     "q": "Which is the correct article for “maison”?", "a": "la", "opts": ["le", "la", "les", "un"],
     "explain": "Maison is feminine: la maison."},
    {"id": "fr-gender-2", "lesson": "gender-and-articles", "type": "usage", "topic": "grammar", "level": "beginner",
     "q": "Words ending in -tion (like nation) are usually…", "a": "feminine", "opts": ["feminine", "masculine", "neutral", "plural"],
     "explain": "-tion, -sion and -té nouns are almost always feminine: la nation."},
    {"id": "fr-gender-3", "lesson": "gender-and-articles", "type": "meaning", "topic": "grammar", "level": "beginner",
     "q": "Before a vowel, “le” and “la” both become…", "a": "l'", "opts": ["les", "l'", "un", "des"],
     "explain": "Le/la elide to l' before a vowel: l'ami, l'eau, l'école."},
    {"id": "fr-num-1", "lesson": "numbers-1-to-20", "type": "vocab", "topic": "numbers", "level": "beginner",
     "q": "How do you say 16 in French?", "a": "seize", "opts": ["seize", "dix-six", "six-dix", "quinze et un"],
     "explain": "16 is seize — a single word, no pattern."},
    {"id": "fr-num-2", "lesson": "numbers-1-to-20", "type": "vocab", "topic": "numbers", "level": "beginner",
     "q": "“Dix-sept” is which number?", "a": "17", "opts": ["16", "17", "18", "70"],
     "explain": "Dix-sept = ten-seven = 17; the pattern starts at 17."},
    {"id": "fr-num-3", "lesson": "numbers-1-to-20", "type": "meaning", "topic": "numbers", "level": "beginner",
     "q": "“C'est combien ?” means…", "a": "how much is it?", "opts": ["where is it?", "how much is it?", "what is it?", "how many are there?"],
     "explain": "C'est combien ? asks the price."},
    {"id": "fr-food-1", "lesson": "food-and-ordering", "type": "usage", "topic": "food", "level": "beginner",
     "q": "The polite way to order in a restaurant is…", "a": "Je voudrais…", "opts": ["Je voudrais…", "Donne-moi…", "Je veux maintenant…", "Peu importe"],
     "explain": "Je voudrais (I would like) is polite everywhere."},
    {"id": "fr-food-2", "lesson": "food-and-ordering", "type": "vocab", "topic": "food", "level": "beginner",
     "q": "In France, to ask for free tap water you say…", "a": "une carafe d'eau", "opts": ["une carafe d'eau", "l'eau gazeuse", "une bouteille d'eau", "de l'eau chaude"],
     "explain": "Une carafe d'eau is a jug of tap water — free in French restaurants."},
    {"id": "fr-food-3", "lesson": "food-and-ordering", "type": "usage", "topic": "food", "level": "beginner",
     "q": "How do you ask for the bill in France?", "a": "L'addition, s'il vous plaît", "opts": ["L'addition, s'il vous plaît", "Le menu, s'il vous plaît", "La nourriture, s'il vous plaît", "L'eau, s'il vous plaît"],
     "explain": "L'addition is the bill (la facture in Québec)."},
    {"id": "fr-verb-1", "lesson": "present-tense-regular-verbs", "type": "usage", "topic": "verbs", "level": "beginner",
     "q": "The “I” form of parler (to speak) is…", "a": "je parle", "opts": ["je parle", "je parles", "je parlons", "je parlent"],
     "explain": "The je form of -er verbs ends in silent -e: je parle."},
    {"id": "fr-verb-2", "lesson": "present-tense-regular-verbs", "type": "usage", "topic": "verbs", "level": "beginner",
     "q": "“Nous finissons” — which verb group is this?", "a": "-ir", "opts": ["-er", "-ir", "-re", "none"],
     "explain": "Finir is an -ir verb; the -iss- in the plural is the giveaway."},
    {"id": "fr-verb-3", "lesson": "present-tense-regular-verbs", "type": "meaning", "topic": "verbs", "level": "beginner",
     "q": "“Ils vendent” means…", "a": "they sell", "opts": ["they sell", "they speak", "they finish", "we sell"],
     "explain": "Vendre is -re; ils vendent = they sell."},
]

# review deck: French -> English (target = French for the Listen button)
REVIEW = [
    {"p": "bonjour", "a": "hello / good morning"}, {"p": "merci", "a": "thank you"},
    {"p": "s'il vous plaît", "a": "please"}, {"p": "au revoir", "a": "goodbye"},
    {"p": "salut", "a": "hi (informal)"}, {"p": "bonne nuit", "a": "good night"},
    {"p": "oui / non", "a": "yes / no"}, {"p": "Comment ça va ?", "a": "how's it going?"},
    {"p": "Je m'appelle Marie", "a": "my name is Marie"}, {"p": "Comment tu t'appelles ?", "a": "what is your name? (informal)"},
    {"p": "Je suis de l'Inde", "a": "I am from India"}, {"p": "J'ai faim", "a": "I am hungry"},
    {"p": "J'ai vingt ans", "a": "I am twenty years old"}, {"p": "le livre", "a": "the book"},
    {"p": "la maison", "a": "the house"}, {"p": "l'eau", "a": "the water"},
    {"p": "un, deux, trois", "a": "one, two, three"}, {"p": "seize", "a": "sixteen"},
    {"p": "C'est combien ?", "a": "how much is it?"}, {"p": "L'addition, s'il vous plaît", "a": "the bill, please"},
    {"p": "Je voudrais un café", "a": "I would like a coffee"}, {"p": "je parle français", "a": "I speak French"},
    {"p": "un ami", "a": "a friend"}, {"p": "à bientôt", "a": "see you soon"},
]

#!/usr/bin/env python3
"""Phase 7C Stage 7 — full courses, one language at a time, popular first.

First language: Spanish (es). A real, authored course — BETA, not PRODUCTION:
  6 lesson pages, a practice lab (reuses practice-engine.js), a topic quiz
  with daily rotation, and an SRS review deck (reuses EkGuruSRS) — all through
  the SAME engines Hindi uses. Every piece of content below is authored by
  hand, not machine-translated, and honest about being a beta course.

Hindi remains the only PRODUCTION language. A course makes a language
"BETA — full course" (still not Hindi-depth, still no recorded audio).

Outputs:
  js/course-es.js            — bank: practice / quiz / review (authored)
  data/courses.json          — course manifest (read by registries + pages)
  languages/es/course/index.html        course hub
  languages/es/lessons/{slug}/index.html 6 lessons
  languages/es/practice/index.html      practice lab
  languages/es/quiz/index.html          topic quiz
  languages/es/review/index.html        SRS review (noindex)

Run: python3 tools/build-language-course.py
"""
import importlib.util, json, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# build-hindi-pages.py has a hyphen in its filename, so import it by path.
_spec = importlib.util.spec_from_file_location("build_hindi_pages", os.path.join(ROOT, "tools", "build-hindi-pages.py"))
_bhp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bhp)
head, foot, write_page, CORE_STYLE = _bhp.head, _bhp.foot, _bhp.write_page, _bhp.CORE_STYLE

NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
BASE = "https://ekguru.shop"
UP = "../../../../"          # languages/es/lessons/X/ -> repo root


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# --------------------------------------------------------------------------
# AUTHORED SPANISH COURSE
# --------------------------------------------------------------------------
COURSE = {
    "lang": "es", "name": "Spanish", "native": "español", "speechTag": "es-ES",
    "status": "BETA",
    "note": ("A real, authored Spanish course in beta: 6 lessons, a practice lab, a topic "
             "quiz and a review deck — all running on the same engines as Hindi. It is not "
             "yet as deep as the Hindi course, and all audio is your browser's computer "
             "voice, never a native recording."),
}

LESSONS = [
    {
        "slug": "greetings-and-introductions",
        "title": "Spanish Greetings and Introductions",
        "desc": "Every Spanish greeting you actually need, when to use tú and usted, and how to introduce yourself — with pronunciation and examples.",
        "sections": [
            ("The greetings that cover most situations", [
                "Spanish has a small set of greetings that work almost everywhere. The two you will use most are <b>hola</b> (hello) and <b>buenos días</b> (good morning). After midday people switch to <b>buenas tardes</b> (good afternoon) and after dark to <b>buenas noches</b> (good night — also used as a greeting when arriving late).",
            ]),
            ("Introducing yourself", [
                "To say your name you use <b>me llamo</b> (literally \"I call myself\") or <b>soy</b> (I am). Both are correct: <b>Me llamo Ana</b> and <b>Soy Ana</b> both mean \"I am Ana\". To ask someone's name, say <b>¿Cómo te llamas?</b> (informal) or <b>¿Cómo se llama?</b> (formal).",
            ]),
            ("Tú vs usted — the register choice", [
                "Spanish has two words for \"you\": <b>tú</b> for friends, family, children and peers, and <b>usted</b> for strangers, older people and formal situations. Most of Latin America defaults to <b>usted</b> more than Spain does. When unsure, <b>usted</b> is the safer, more respectful choice.",
            ]),
            ("¿Cómo estás? — asking how someone is", [
                "<b>¿Cómo estás?</b> means \"how are you?\" (informal); <b>¿Cómo está?</b> is the formal version. The everyday answer is <b>Bien, gracias</b> (fine, thanks) or <b>Muy bien</b> (very well). To be polite you add <b>¿y tú?</b> (and you?) or <b>¿y usted?</b>.",
            ]),
        ],
        "table": (("Greeting", "When to use it"), [
            ("hola", "hello — any time, any register"),
            ("buenos días", "good morning — until midday"),
            ("buenas tardes", "good afternoon — midday to evening"),
            ("buenas noches", "good evening / good night"),
            ("adiós", "goodbye"),
            ("hasta luego", "see you later"),
        ]),
    },
    {
        "slug": "ser-and-estar",
        "title": "Ser and Estar — The Two Ways to Say \"To Be\"",
        "desc": "Why Spanish has two verbs for \"to be\", the rule that tells them apart, and the exceptions every learner hits.",
        "sections": [
            ("The core rule", [
                "Spanish has two verbs for \"to be\": <b>ser</b> and <b>estar</b>. The rule of thumb: <b>ser</b> is for what something <i>is</i> (permanent identity, origin, profession, characteristics), and <b>estar</b> is for how something <i>is right now</i> (location, mood, temporary states).",
            ]),
            ("Ser — identity and essence", [
                "<b>Soy de India</b> (I am from India), <b>Soy estudiante</b> (I am a student), <b>Ella es alta</b> (she is tall). These are stable facts. Origin, nationality, profession and personality all use <b>ser</b>.",
            ]),
            ("Estar — state and location", [
                "<b>Estoy cansado</b> (I am tired), <b>Estoy en casa</b> (I am at home), <b>El café está caliente</b> (the coffee is hot). Mood, position and location always use <b>estar</b> — even for places, which are locations, not identities.",
            ]),
            ("The one that trips everyone", [
                "Some adjectives change meaning with the verb. <b>Estoy listo</b> means \"I am ready\"; <b>Soy listo</b> means \"I am clever\". <b>Está aburrido</b> means \"he is bored\"; <b>Es aburrido</b> means \"he is boring\". Learn these as pairs, not rules.",
            ]),
        ],
        "table": (("Verb", "Used for"), [
            ("ser", "identity, origin, profession, time, permanent traits"),
            ("estar", "location, mood, condition, temporary states"),
            ("soy / estoy", "I am (ser / estar)"),
            ("eres / estás", "you are — informal (ser / estar)"),
            ("es / está", "he/she/it is (ser / estar)"),
        ]),
    },
    {
        "slug": "gender-and-articles",
        "title": "Gender and Articles in Spanish",
        "desc": "How to guess a noun's gender from its ending, and the four words for \"the\" — el, la, los, las.",
        "sections": [
            ("Every noun is masculine or feminine", [
                "Every Spanish noun has a gender, and it shows in the article. <b>El</b> is \"the\" for masculine singular, <b>la</b> for feminine singular, <b>los</b> and <b>las</b> for their plurals.",
            ]),
            ("The -o and -a rule (with exceptions)", [
                "Most nouns ending in <b>-o</b> are masculine (<b>el libro</b>, the book) and most ending in <b>-a</b> are feminine (<b>la casa</b>, the house). The famous exceptions are worth memorising: <b>el día</b> (the day), <b>el mapa</b> (the map), <b>la mano</b> (the hand), <b>la foto</b> (the photo).",
            ]),
            ("Other endings", [
                "Nouns ending in <b>-ción</b>, <b>-sión</b> and <b>-dad</b> are almost always feminine: <b>la canción</b>, <b>la televisión</b>, <b>la ciudad</b>. Nouns ending in <b>-ma</b> of Greek origin are masculine: <b>el problema</b>, <b>el tema</b>, <b>el sistema</b>.",
            ]),
            ("Agreement with adjectives", [
                "Adjectives agree with the noun: <b>el libro rojo</b> (the red book) but <b>la casa roja</b> (the red house). Adjectives ending in <b>-e</b> or a consonant are the same for both genders: <b>el libro grande</b>, <b>la casa grande</b>.",
            ]),
        ],
        "table": (("Article", "Meaning"), [
            ("el", "the — masculine singular"),
            ("la", "the — feminine singular"),
            ("los", "the — masculine plural"),
            ("las", "the — feminine plural"),
            ("un / una", "a — masculine / feminine"),
        ]),
    },
    {
        "slug": "numbers-1-to-20",
        "title": "Spanish Numbers 1 to 20",
        "desc": "The first twenty numbers with pronunciation, plus how to ask and say prices.",
        "sections": [
            ("1 to 10", [
                "The first ten numbers are the foundation: <b>uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve, diez</b>. Notice <b>uno</b> shortens to <b>un</b> before a masculine noun: <b>un libro</b> (one book).",
            ]),
            ("11 to 15", [
                "<b>once, doce, trece, catorce, quince</b>. These five are single words you simply memorise — there is no pattern to lean on.",
            ]),
            ("16 to 20", [
                "From 16 the pattern appears: <b>dieciséis</b> (16, literally \"ten and six\"), <b>diecisiete</b> (17), <b>dieciocho</b> (18), <b>diecinueve</b> (19), <b>veinte</b> (20).",
            ]),
            ("Asking and saying prices", [
                "<b>¿Cuánto cuesta?</b> means \"how much does it cost?\" (one thing); <b>¿Cuánto cuestan?</b> for several. The answer is just the number: <b>Diez euros</b> (ten euros). In most of Latin America you will also hear <b>¿Cuánto es?</b>.",
            ]),
        ],
        "table": (("Number", "Spanish"), [
            ("1", "uno"), ("2", "dos"), ("3", "tres"), ("4", "cuatro"), ("5", "cinco"),
            ("6", "seis"), ("7", "siete"), ("8", "ocho"), ("9", "nueve"), ("10", "diez"),
            ("15", "quince"), ("20", "veinte"),
        ]),
    },
    {
        "slug": "food-and-ordering",
        "title": "Food and Ordering in Spanish",
        "desc": "The phrases that get you fed: ordering, asking for the bill, and the words every menu uses.",
        "sections": [
            ("Ordering", [
                "To order, say <b>Quisiera</b> (I would like) — it is polite everywhere. <b>Quisiera un café, por favor</b> (I would like a coffee, please). The informal <b>Me das…</b> (can you give me…) works with friends but not in a formal restaurant.",
            ]),
            ("Water, please — still or sparkling", [
                "<b>Agua</b> is water; <b>agua sin gas</b> is still and <b>agua con gas</b> is sparkling. In Spain tap water is <b>agua del grifo</b>; asking for it is normal, though most restaurants still charge for bottled water.",
            ]),
            ("The bill", [
                "Ask for the bill with <b>La cuenta, por favor</b>. In Spain you may also hear <b>¿Me cobras?</b>. A tip (<b>propina</b>) is not expected in Spain — rounding up is enough — while in much of Latin America 10% is standard.",
            ]),
            ("Useful menu words", [
                "<b>Entrada</b> (starter), <b>plato principal</b> (main course), <b>postre</b> (dessert), <b>sin</b> (without) and <b>con</b> (with) are the ones you reach for most: <b>sin cebolla</b> (without onion), <b>con hielo</b> (with ice).",
            ]),
        ],
        "table": (("Spanish", "English"), [
            ("Quisiera…", "I would like…"),
            ("La cuenta, por favor", "The bill, please"),
            ("agua sin gas / con gas", "still / sparkling water"),
            ("¿Qué me recomienda?", "What do you recommend?"),
            ("sin / con", "without / with"),
        ]),
    },
    {
        "slug": "present-tense-regular-verbs",
        "title": "Spanish Present Tense — Regular Verbs",
        "desc": "The three verb families (-ar, -er, -ir) and the endings that let you conjugate any regular verb.",
        "sections": [
            ("Three families, three sets of endings", [
                "Regular Spanish verbs end in <b>-ar</b>, <b>-er</b> or <b>-ir</b>. Each family has its own set of endings. Once you know the endings, you can conjugate any regular verb you meet.",
            ]),
            ("-ar verbs: hablar (to speak)", [
                "<b>hablo, hablas, habla, hablamos, habláis, hablan</b> — I speak, you speak, he/she speaks, we speak, you all speak, they speak. The <b>-o</b> for \"I\" and <b>-a/-an</b> for he/she/they are the endings to notice first.",
            ]),
            ("-er and -ir verbs: comer (to eat), vivir (to live)", [
                "<b>como, comes, come, comemos, coméis, comen</b> and <b>vivo, vives, vive, vivimos, vivís, viven</b>. The only difference between -er and -ir shows in \"we\" and \"you all\": <b>comemos</b> vs <b>vivimos</b>, <b>coméis</b> vs <b>vivís</b>.",
            ]),
            ("Why this matters", [
                "The subject pronoun is optional in Spanish — <b>hablo</b> already means \"I speak\", so <b>yo hablo</b> is used only for emphasis. Learners over-use <b>yo</b>; native speakers drop it unless contrasting: <b>Yo hablo, tú escuchas</b> (I speak, you listen).",
            ]),
        ],
        "table": (("Person", "-ar (hablar)", "-er (comer)", "-ir (vivir)"), [
            ("yo (I)", "hablo", "como", "vivo"),
            ("tú (you)", "hablas", "comes", "vives"),
            ("él/ella (he/she)", "habla", "come", "vive"),
            ("nosotros (we)", "hablamos", "comemos", "vivimos"),
            ("ellos (they)", "hablan", "comen", "viven"),
        ]),
    },
]

# practice banks (reuse practice-engine.js). `say` = the Spanish text to speak.
PRACTICE = {
    "vocabulary": [
        {"q": "What does “hola” mean?", "a": "hello", "opts": ["goodbye", "hello", "please", "thanks"], "explain": "Hola is hello — the one word every Spanish speaker knows and uses.", "say": "hola"},
        {"q": "What does “adiós” mean?", "a": "goodbye", "opts": ["hello", "goodbye", "good night", "welcome"], "explain": "Adiós is goodbye.", "say": "adiós"},
        {"q": "What does “gracias” mean?", "a": "thank you", "opts": ["please", "thank you", "sorry", "yes"], "explain": "Gracias is thank you. The reply is de nada (you're welcome).", "say": "gracias"},
        {"q": "What does “por favor” mean?", "a": "please", "opts": ["please", "thank you", "excuse me", "goodbye"], "explain": "Por favor is please.", "say": "por favor"},
        {"q": "What does “agua” mean?", "a": "water", "opts": ["bread", "water", "wine", "milk"], "explain": "Agua is water. Note it is feminine but takes el: el agua.", "say": "agua"},
        {"q": "What does “comida” mean?", "a": "food", "opts": ["food", "drink", "table", "kitchen"], "explain": "Comida is food (and in Mexico, the midday meal).", "say": "comida"},
        {"q": "What does “casa” mean?", "a": "house", "opts": ["car", "house", "street", "room"], "explain": "Casa is house or home.", "say": "casa"},
        {"q": "What does “amigo” mean?", "a": "friend", "opts": ["brother", "friend", "teacher", "neighbour"], "explain": "Amigo is friend (masculine); amiga is the feminine form.", "say": "amigo"},
        {"q": "What does “trabajo” mean?", "a": "work", "opts": ["work", "holiday", "money", "time"], "explain": "Trabajo is work — also the verb trabajar (to work).", "say": "trabajo"},
        {"q": "What does “tiempo” mean?", "a": "time", "opts": ["weather", "time", "money", "place"], "explain": "Tiempo means both time and weather.", "say": "tiempo"},
        {"q": "What does “hoy” mean?", "a": "today", "opts": ["tomorrow", "today", "yesterday", "now"], "explain": "Hoy is today; mañana is tomorrow; ayer is yesterday.", "say": "hoy"},
        {"q": "What does “noche” mean?", "a": "night", "opts": ["day", "night", "morning", "week"], "explain": "Noche is night — as in buenas noches.", "say": "noche"},
    ],
    "grammar": [
        {"q": "Which verb means “to be” for identity: “Soy de India”?", "a": "ser", "opts": ["ser", "estar", "tener", "hacer"], "explain": "Origin and identity use ser: soy de India = I am from India.", "say": "soy de India"},
        {"q": "“Estoy en casa” — which verb is this, and why?", "a": "estar — location", "opts": ["ser — identity", "estar — location", "ser — time", "tener — possession"], "explain": "Location always uses estar.", "say": "estoy en casa"},
        {"q": "“El libro” vs “la casa” — why different articles?", "a": "libro is masculine, casa is feminine", "opts": ["libro is masculine, casa is feminine", "casa is plural", "libro is plural", "both are neutral"], "explain": "Libro ends in -o (masculine), casa ends in -a (feminine).", "say": "el libro"},
        {"q": "Which is correct: “el día” or “la día”?", "a": "el día", "opts": ["el día", "la día", "los día", "las día"], "explain": "Día is a famous exception: it is masculine despite ending in -a.", "say": "el día"},
        {"q": "“Hablamos” means…", "a": "we speak", "opts": ["I speak", "we speak", "they speak", "he speaks"], "explain": "-amos is the nosotros (we) ending for -ar verbs.", "say": "hablamos"},
        {"q": "“Como” (from comer) means…", "a": "I eat", "opts": ["I eat", "he eats", "we eat", "they eat"], "explain": "-o marks the yo (I) form in every family.", "say": "como"},
        {"q": "How do you say “how are you?” to a friend?", "a": "¿Cómo estás?", "opts": ["¿Cómo está?", "¿Cómo estás?", "¿Cómo se llama?", "¿Qué tal hoy?"], "explain": "¿Cómo estás? is the informal (tú) form.", "say": "¿cómo estás?"},
        {"q": "“Me llamo Ana” literally means…", "a": "I call myself Ana", "opts": ["My name is Ana", "I call myself Ana", "Call me Ana", "Ana is my name"], "explain": "Llamarse is reflexive: me llamo = I call myself.", "say": "me llamo Ana"},
        {"q": "Which means “the bill, please”?", "a": "La cuenta, por favor", "opts": ["La cuenta, por favor", "La comida, por favor", "La casa, por favor", "El menú, por favor"], "explain": "La cuenta is the bill/check.", "say": "la cuenta, por favor"},
        {"q": "“Quisiera un café” means…", "a": "I would like a coffee", "opts": ["I want a coffee now", "I would like a coffee", "I had a coffee", "The coffee is cold"], "explain": "Quisiera is the polite conditional — “I would like”.", "say": "quisiera un café"},
        {"q": "Choose the right verb: “Ella ___ alta” (she is tall).", "a": "es", "opts": ["es", "está", "tiene", "hay"], "explain": "Height is a characteristic, so ser: ella es alta.", "say": "ella es alta"},
        {"q": "Choose the right verb: “El café ___ caliente” (the coffee is hot).", "a": "está", "opts": ["está", "es", "tiene", "hay"], "explain": "Temperature is a temporary state, so estar.", "say": "el café está caliente"},
    ],
}

# topic quiz (daily rotation). topic + level + type like the Hindi quiz bank.
QUIZ = [
    {"id": "es-greet-1", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner",
     "q": "What does “buenos días” mean?", "a": "good morning", "opts": ["good night", "good morning", "good afternoon", "goodbye"],
     "explain": "Buenos días is good morning — used until midday."},
    {"id": "es-greet-2", "lesson": "greetings-and-introductions", "type": "usage", "topic": "greetings", "level": "beginner",
     "q": "When should you use “usted” instead of “tú”?", "a": "With strangers and in formal situations", "opts": ["With friends", "With children", "With strangers and in formal situations", "Never"],
     "explain": "Usted is the formal “you” for strangers, older people and formal settings."},
    {"id": "es-greet-3", "lesson": "greetings-and-introductions", "type": "vocab", "topic": "greetings", "level": "beginner",
     "q": "How do you ask a stranger's name politely?", "a": "¿Cómo se llama?", "opts": ["¿Cómo te llamas?", "¿Cómo se llama?", "¿Qué es esto?", "¿Dónde está?"],
     "explain": "¿Cómo se llama? is the formal (usted) form of “what is your name?”."},
    {"id": "es-greet-4", "lesson": "greetings-and-introductions", "type": "usage", "topic": "greetings", "level": "beginner",
     "q": "“Buenas noches” can mean…", "a": "both good evening and good night", "opts": ["only good night", "only good evening", "both good evening and good night", "good morning"],
     "explain": "Buenas noches works as a greeting when arriving late and as “good night” when leaving."},
    {"id": "es-ser-1", "lesson": "ser-and-estar", "type": "meaning", "topic": "grammar", "level": "beginner",
     "q": "“Soy de India” uses ser because…", "a": "origin uses ser", "opts": ["origin uses ser", "location uses ser", "mood uses ser", "it is a temporary state"],
     "explain": "Origin and identity are permanent — they use ser."},
    {"id": "es-ser-2", "lesson": "ser-and-estar", "type": "usage", "topic": "grammar", "level": "beginner",
     "q": "“Estoy cansado” (I am tired) uses estar because…", "a": "tiredness is a temporary state", "opts": ["tiredness is a temporary state", "it is about identity", "it is about origin", "it is about profession"],
     "explain": "Mood and condition are temporary states, so estar."},
    {"id": "es-ser-3", "lesson": "ser-and-estar", "type": "usage", "topic": "grammar", "level": "beginner",
     "q": "“Estoy listo” vs “Soy listo” — which means “I am ready”?", "a": "Estoy listo", "opts": ["Soy listo", "Estoy listo", "Both", "Neither"],
     "explain": "Estoy listo = I am ready; soy listo = I am clever. The verb changes the meaning."},
    {"id": "es-gender-1", "lesson": "gender-and-articles", "type": "usage", "topic": "grammar", "level": "beginner",
     "q": "Which is the correct article for “casa”?", "a": "la", "opts": ["el", "la", "los", "un"],
     "explain": "Casa ends in -a and is feminine: la casa."},
    {"id": "es-gender-2", "lesson": "gender-and-articles", "type": "usage", "topic": "grammar", "level": "beginner",
     "q": "Which of these is a famous exception to the -o/-a rule?", "a": "el día", "opts": ["el día", "la libro", "el casa", "la mano y el mapa"],
     "explain": "El día (day) is masculine despite -a; la mano and el mapa are the other classics."},
    {"id": "es-gender-3", "lesson": "gender-and-articles", "type": "meaning", "topic": "grammar", "level": "beginner",
     "q": "Words ending in -ción (like canción) are usually…", "a": "feminine", "opts": ["feminine", "masculine", "neutral", "plural"],
     "explain": "-ción, -sión and -dad nouns are almost always feminine: la canción."},
    {"id": "es-num-1", "lesson": "numbers-1-to-20", "type": "vocab", "topic": "numbers", "level": "beginner",
     "q": "How do you say 16 in Spanish?", "a": "dieciséis", "opts": ["dieciséis", "diez y seis", "seis y diez", "dieciocho"],
     "explain": "16 is dieciséis — literally “ten and six”."},
    {"id": "es-num-2", "lesson": "numbers-1-to-20", "type": "usage", "topic": "numbers", "level": "beginner",
     "q": "“Uno” shortens to “un” before…", "a": "a masculine noun", "opts": ["a feminine noun", "a masculine noun", "a plural noun", "a verb"],
     "explain": "Un libro (one book), but una casa (one house)."},
    {"id": "es-num-3", "lesson": "numbers-1-to-20", "type": "vocab", "topic": "numbers", "level": "beginner",
     "q": "“¿Cuánto cuesta?” means…", "a": "how much does it cost?", "opts": ["where is it?", "how much does it cost?", "what is it?", "how many are there?"],
     "explain": "¿Cuánto cuesta? asks the price of one thing."},
    {"id": "es-food-1", "lesson": "food-and-ordering", "type": "usage", "topic": "food", "level": "beginner",
     "q": "The polite way to order in a restaurant is…", "a": "Quisiera…", "opts": ["Quisiera…", "Dame…", "Quiero ahora…", "Me da igual"],
     "explain": "Quisiera (I would like) is polite everywhere."},
    {"id": "es-food-2", "lesson": "food-and-ordering", "type": "vocab", "topic": "food", "level": "beginner",
     "q": "“Agua con gas” is…", "a": "sparkling water", "opts": ["still water", "sparkling water", "tap water", "hot water"],
     "explain": "Con gas = with bubbles (sparkling); sin gas = still."},
    {"id": "es-food-3", "lesson": "food-and-ordering", "type": "usage", "topic": "food", "level": "beginner",
     "q": "How do you ask for the bill?", "a": "La cuenta, por favor", "opts": ["La cuenta, por favor", "El menú, por favor", "La comida, por favor", "El agua, por favor"],
     "explain": "La cuenta is the bill/check."},
    {"id": "es-verb-1", "lesson": "present-tense-regular-verbs", "type": "usage", "topic": "verbs", "level": "beginner",
     "q": "The “I” ending for regular -ar verbs is…", "a": "-o", "opts": ["-o", "-a", "-as", "-an"],
     "explain": "Hablo, como, vivo — the yo form always ends in -o."},
    {"id": "es-verb-2", "lesson": "present-tense-regular-verbs", "type": "meaning", "topic": "verbs", "level": "beginner",
     "q": "“Hablamos” means…", "a": "we speak", "opts": ["I speak", "we speak", "they speak", "he speaks"],
     "explain": "-amos is the nosotros ending for -ar verbs."},
    {"id": "es-verb-3", "lesson": "present-tense-regular-verbs", "type": "usage", "topic": "verbs", "level": "beginner",
     "q": "Why do native speakers often drop “yo”?", "a": "the verb ending already shows the subject", "opts": ["the verb ending already shows the subject", "yo is rude", "yo is only for formal speech", "yo does not exist"],
     "explain": "Hablo already means “I speak”, so yo is only added for emphasis."},
    {"id": "es-verb-4", "lesson": "present-tense-regular-verbs", "type": "vocab", "topic": "verbs", "level": "beginner",
     "q": "“Comemos” vs “vivimos” — which verb families?", "a": "-er and -ir", "opts": ["-ar and -er", "-er and -ir", "-ar and -ir", "both -ar"],
     "explain": "Comer is -er, vivir is -ir; the difference only shows in we/you-all forms."},
]

# review deck: Spanish -> English (target = Spanish for the Listen button)
REVIEW = [
    {"p": "hola", "a": "hello"}, {"p": "adiós", "a": "goodbye"},
    {"p": "gracias", "a": "thank you"}, {"p": "por favor", "a": "please"},
    {"p": "buenos días", "a": "good morning"}, {"p": "buenas noches", "a": "good evening / night"},
    {"p": "¿Cómo estás?", "a": "how are you? (informal)"}, {"p": "Me llamo Ana", "a": "my name is Ana"},
    {"p": "¿Cómo te llamas?", "a": "what is your name? (informal)"}, {"p": "soy de India", "a": "I am from India"},
    {"p": "estoy en casa", "a": "I am at home"}, {"p": "el libro", "a": "the book"},
    {"p": "la casa", "a": "the house"}, {"p": "el agua", "a": "the water"},
    {"p": "uno, dos, tres", "a": "one, two, three"}, {"p": "dieciséis", "a": "sixteen"},
    {"p": "¿Cuánto cuesta?", "a": "how much does it cost?"}, {"p": "La cuenta, por favor", "a": "the bill, please"},
    {"p": "Quisiera un café", "a": "I would like a coffee"}, {"p": "hablo español", "a": "I speak Spanish"},
    {"p": "amigo / amiga", "a": "friend (m / f)"}, {"p": "hoy", "a": "today"},
    {"p": "comida", "a": "food"}, {"p": "trabajo", "a": "work"},
]


# --------------------------------------------------------------------------
# GENERATORS
# --------------------------------------------------------------------------
def esc_html(s):
    return str(s)


def lesson_html(l):
    secs = "".join(
        '  <h2>%s</h2>\n' % esc_html(h) +
        "".join('  <p>%s</p>\n' % p for p in paras)
        for h, paras in l["sections"])
    tbl = ""
    if "table" in l:
        headers, rows = l["table"]
        head_cells = "".join('<th>%s</th>' % esc_html(c) for c in headers)
        body_rows = "".join(
            '<tr>' + "".join('<td>%s</td>' % esc_html(c) for c in r) + '</tr>\n'
            for r in rows)
        tbl = ('  <table>\n  <thead><tr>%s</tr></thead>\n  <tbody>\n%s  </tbody>\n  </table>\n'
               % (head_cells, body_rows))
    return ('  <h1>%s</h1>\n'
            '  <p class="lede">%s</p>\n'
            '  <div class="note"><b>Beta course.</b> Authored Spanish content, part of the free '
            'EkGuru Spanish course in beta. Audio is your browser’s computer voice, not a native recording.</div>\n'
            '%s%s'
            '  <p style="margin-top:26px"><a class="btn" href="/languages/es/course/">Spanish course</a> '
            '<a class="btn" href="/languages/es/practice/">Practice</a> '
            '<a class="btn" href="/languages/es/quiz/">Quiz</a> '
            '<a class="btn" href="/languages/es/review/">Review</a></p>\n'
            % (esc_html(l["title"]), esc_html(l["desc"]), secs, tbl))


def build_lessons():
    made = []
    for l in LESSONS:
        path = "languages/es/lessons/%s/index.html" % l["slug"]
        up = "../../../../"
        title = "%s — Spanish Course" % l["title"]
        crumb = ('<a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › '
                 '<a href="/languages/es/">Spanish</a> › <a href="/languages/es/course/">Course</a> › %s'
                 % esc_html(l["title"]))
        write_page(path, up, title, l["desc"], "languages/es/lessons/%s/" % l["slug"],
                   crumb, lesson_html(l), scripts=(), index=True,
                   extra_style=".art table{width:100%;border-collapse:collapse;margin:18px 0;font-size:.95rem}"
                               ".art th,.art td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line)}"
                               ".art th{font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}")
        made.append(path)
    return made


def build_course_hub():
    lessons = "".join(
        '  <li><a href="/languages/es/lessons/%s/">%s</a><span>%s</span></li>\n'
        % (l["slug"], esc_html(l["title"]), esc_html(l["desc"][:90] + "…"))
        for l in LESSONS)
    body = (
        '  <h1>Spanish Course <span class="tag beta" style="vertical-align:4px">BETA</span></h1>\n'
        '  <p class="lede">A real, free Spanish course: lessons, practice, a quiz and a review deck — '
        'all running on the same engines as the Hindi course.</p>\n'
        '  <div class="note"><b>Honest status.</b> %s</div>\n'
        '  <h2>Lessons</h2>\n'
        '  <ul class="linklist">\n%s  </ul>\n'
        '  <h2>Practice and review</h2>\n'
        '  <ul class="linklist">\n'
        '  <li><a href="/languages/es/practice/">Practice lab</a><span>Recognition drills on vocabulary and grammar, with the Spanish computer voice.</span></li>\n'
        '  <li><a href="/languages/es/quiz/">Topic quiz</a><span>20 multiple-choice questions with explanations; the set rotates daily.</span></li>\n'
        '  <li><a href="/languages/es/review/">Review deck</a><span>Spaced repetition of the words and phrases, saved on this device only.</span></li>\n'
        '  </ul>\n'
        '  <p><a class="btn" href="/languages/es/">Spanish starter pack</a> '
        '<a class="btn" href="/languages/">All languages</a></p>\n'
    ) % (esc_html(COURSE["note"]), lessons)
    write_page("languages/es/course/index.html", "../../../", "Learn Spanish — free course (beta)",
               "A free Spanish course in beta: six lessons, a practice lab, a topic quiz and a spaced-repetition review deck — all in your browser.",
               "languages/es/course/",
               '<a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › <a href="/languages/es/">Spanish</a> › Course',
               body, scripts=(), index=True)
    return "languages/es/course/index.html"


def build_practice():
    body = (
        '  <h1>Spanish Practice <span class="tag beta" style="vertical-align:4px">BETA</span></h1>\n'
        '  <p class="lede">Recognition drills on Spanish vocabulary and grammar. Pick a bank, '
        'then answer — the explanation follows each answer.</p>\n'
        '  <div class="row" style="gap:10px;flex-wrap:wrap;margin:14px 0">\n'
        '    <button type="button" class="btn" id="es-b-vocab">Vocabulary</button>\n'
        '    <button type="button" class="btn" id="es-b-grammar">Grammar</button>\n'
        '  </div>\n'
        '  <div class="px-wrap" id="es-practice"></div>\n'
        '  <script>\n'
        '  (function () {\n'
        '    function mount(bank) {\n'
        '      if (window.EKGURU_COURSE_ES && window.EKGURU_COURSE_ES.practice) {\n'
        '        window.EKGURU_PRACTICE_BANK = window.EKGURU_COURSE_ES.practice;\n'
        '      }\n'
        '      var el = document.getElementById("es-practice");\n'
        '      if (window.EkGuruPractice) window.EkGuruPractice.mount(el, {mode:"practice", bank:bank, count:10, speechLang:"es-ES"});\n'
        '    }\n'
        '    function on(id, bank) { var b = document.getElementById(id); if (b) b.addEventListener("click", function(){ mount(bank); }); }\n'
        '    on("es-b-vocab", "vocabulary"); on("es-b-grammar", "grammar");\n'
        '    var t = setInterval(function () {\n'
        '      if (window.EkGuruPractice && window.EKGURU_COURSE_ES) { clearInterval(t); mount("vocabulary"); }\n'
        '    }, 100);\n'
        '    setTimeout(function(){ clearInterval(t); }, 5000);\n'
        '  })();\n'
        '  </script>\n'
    )
    write_page("languages/es/practice/index.html", "../../../",
               "Spanish Practice — Vocabulary & Grammar Drills",
               "Free Spanish practice drills: see a Spanish word or rule, pick the meaning, get the explanation. Computer voice playback, saved in your browser.",
               "languages/es/practice/",
               '<a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › <a href="/languages/es/">Spanish</a> › Practice',
               body, scripts=["course-es.js", "practice-engine.js"], index=True)
    return "languages/es/practice/index.html"


def build_quiz():
    body = (
        '  <h1>Spanish Topic Quiz <span class="tag beta" style="vertical-align:4px">BETA</span></h1>\n'
        '  <p class="lede">20 multiple-choice questions with explanations, drawn from the Spanish lessons.</p>\n'
        '  <div class="row" style="gap:12px;flex-wrap:wrap;align-items:end">\n'
        '    <div><label for="es-q-topic">Topic</label><br><select id="es-q-topic"></select></div>\n'
        '    <div><label for="es-q-n">Questions</label><br><select id="es-q-n">\n'
        '      <option value="5">5</option><option value="10">10</option><option value="20">20</option></select></div>\n'
        '    <button type="button" class="btn" id="es-q-start">Start</button>\n'
        '  </div>\n'
        '  <p class="muted" style="font-size:.8rem;margin-top:8px">Questions rotate each day for the same topic '
        '(rule-based, not random) — come back tomorrow for a new set.</p>\n'
        '  <div id="es-q-body" style="margin-top:16px"></div>\n'
        '  <script>\n'
        '  (function () {\n'
        '    "use strict";\n'
        '    function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}\n'
        '    function shuffle(a){var o=a.slice();for(var i=o.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=o[i];o[i]=o[j];o[j]=t;}return o;}\n'
        '    function dayShuffle(a, salt, when){var d=when||new Date();var key=d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")+":"+(salt||"");var h=2166136261;for(var i=0;i<key.length;i++){h^=key.charCodeAt(i);h=Math.imul(h,16777619);}var s=h>>>0;var o=a.slice();var rnd=function(){s|=0;s=(s+0x6D2B79F5)|0;var t=Math.imul(s^(s>>>15),1|s);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};for(var i=o.length-1;i>0;i--){var j=Math.floor(rnd()*(i+1));var tmp=o[i];o[i]=o[j];o[j]=tmp;}return o;}\n'
        '    var state = null, sel = document.getElementById("es-q-topic");\n'
        '    function init() {\n'
        '      var Q = (window.EKGURU_COURSE_ES && window.EKGURU_COURSE_ES.quiz) || [];\n'
        '      var topics = {}; Q.forEach(function(q){ topics[q.topic]=1; });\n'
        '      sel.innerHTML = Object.keys(topics).map(function(t){ return \'<option value="\'+esc(t)+\'">\'+esc(t)+\'</option>\'; }).join("");\n'
        '      document.getElementById("es-q-start").addEventListener("click", function(){\n'
        '        var topic = sel.value; var n = parseInt(document.getElementById("es-q-n").value, 10);\n'
        '        var pool = Q.filter(function(q){ return q.topic === topic; });\n'
        '        var use = dayShuffle(pool, "quiz:" + topic).slice(0, n);\n'
        '        if (!use.length) { document.getElementById("es-q-body").innerHTML = "<p class=\\"muted\\">No questions for this topic yet.</p>"; return; }\n'
        '        state = { i:0, correct:0, use:use }; renderQuestion();\n'
        '      });\n'
        '    }\n'
        '    function renderQuestion() {\n'
        '      var b = document.getElementById("es-q-body");\n'
        '      if (!state || state.i >= state.use.length) { b.innerHTML = state ? "<p>Finished.</p>" : ""; return; }\n'
        '      var q = state.use[state.i];\n'
        '      var opts = shuffle(q.opts.slice());\n'
        '      b.innerHTML = \'<p class="muted">Question \' + (state.i+1) + \' of \' + state.use.length + \' — \' + esc(q.topic) + \'</p>\' +\n'
        '        \'<p style="font-weight:700;font-size:1.05rem">\' + esc(q.q) + \'</p>\' +\n'
        '        opts.map(function(o,idx){ return \'<button type="button" class="btn ghost" style="display:block;width:100%;text-align:left;margin:6px 0" data-opt="\'+idx+\'">\'+esc(o)+\'</button>\'; }).join("") +\n'
        '        \'<div id="es-q-fb" style="margin-top:10px"></div>\';\n'
        '      b.querySelectorAll("[data-opt]").forEach(function(btn){\n'
        '        btn.addEventListener("click", function(){\n'
        '          var chosen = opts[parseInt(btn.getAttribute("data-opt"),10)];\n'
        '          var ok = chosen === q.a; if (ok) state.correct++;\n'
        '          var fb = b.querySelector("#es-q-fb");\n'
        '          fb.innerHTML = \'<p style="font-weight:600;color:\' + (ok ? "var(--green,#1a7f37)" : "var(--red,#b3261e)") + \'">\' +\n'
        '            (ok ? "Correct." : "Not quite — the answer was “" + esc(q.a) + "”.") + \'</p>\' +\n'
        '            \'<p class="muted">\' + esc(q.explain) + \'</p>\' +\n'
        '            \'<button type="button" class="btn" id="es-q-next">Next</button>\';\n'
        '          b.querySelector("#es-q-next").addEventListener("click", function(){ state.i++; renderQuestion(); });\n'
        '        });\n'
        '      });\n'
        '    }\n'
        '    if (window.EKGURU_COURSE_ES) init();\n'
        '    else window.addEventListener("load", init);\n'
        '  })();\n'
        '  </script>\n'
    )
    write_page("languages/es/quiz/index.html", "../../../",
               "Spanish Quiz — Topic Questions with Explanations",
               "A free Spanish topic quiz: multiple-choice questions with explanations, drawn from the Spanish lessons. The set rotates daily.",
               "languages/es/quiz/",
               '<a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › <a href="/languages/es/">Spanish</a> › Quiz',
               body, scripts=["course-es.js"], index=True)
    return "languages/es/quiz/index.html"


def build_review():
    body = (
        '  <h1>Spanish Review <span class="tag beta" style="vertical-align:4px">BETA</span></h1>\n'
        '  <p class="lede">A simple spaced-repetition deck for the Spanish words and phrases, saved on this device only.</p>\n'
        '  <div id="es-srs-stats" style="margin:12px 0;font-weight:600"></div>\n'
        '  <div id="es-srs-card" style="border:1px solid var(--line);border-radius:14px;padding:20px;background:var(--card,#fff)"></div>\n'
        '  <div id="es-srs-empty" style="display:none" class="note">No Spanish cards due right now. Load the deck to start.</div>\n'
        '  <div style="margin-top:14px">\n'
        '    <button type="button" class="btn" id="es-srs-seed">Load Spanish deck</button>\n'
        '    <button type="button" class="btn ghost" id="es-srs-reset">Remove all Spanish cards</button>\n'
        '  </div>\n'
        '  <script>\n'
        '  (function () {\n'
        '    "use strict";\n'
        '    function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}\n'
        '    var queue = [], card = null;\n'
        '    function seed() {\n'
        '      var deck = (window.EKGURU_COURSE_ES && window.EKGURU_COURSE_ES.review) || [];\n'
        '      var added = 0;\n'
        '      deck.forEach(function (w) {\n'
        '        var r = window.EkGuruSRS.add({ prompt: w.p, answer: w.a, category: "spanish", level: "beginner", language: "es", target: w.p });\n'
        '        if (r.added) added++;\n'
        '      });\n'
        '      return added;\n'
        '    }\n'
        '    function paint() {\n'
        '      var st = document.getElementById("es-srs-stats");\n'
        '      var due = window.EkGuruSRS.due().filter(function (c) { return c.language === "es"; });\n'
        '      st.textContent = due.length + " Spanish cards due";\n'
        '      var box = document.getElementById("es-srs-card");\n'
        '      var empty = document.getElementById("es-srs-empty");\n'
        '      if (!queue.length) { queue = due; }\n'
        '      card = queue.shift() || null;\n'
        '      if (!card) { box.innerHTML = ""; empty.style.display = "block"; return; }\n'
        '      empty.style.display = "none";\n'
        '      var say = card.target || card.prompt;\n'
        '      box.innerHTML =\n'
        '        \'<p class="prompt">\' + esc(card.prompt) +\n'
        '        \'<button type="button" class="hi-listen" id="es-srs-say" aria-label="Listen (computer voice)" aria-pressed="false"><span aria-hidden="true">🔊</span> Listen</button></p>\' +\n'
        '        \'<div class="answer" id="es-srs-a" style="display:none;background:var(--bg-soft);border:1px solid #ddd8ff;border-radius:10px;padding:12px 14px;margin:0 0 14px;color:var(--ink-2)"><b>\' + esc(card.answer) + \'</b></div>\' +\n'
        '        \'<button type="button" class="btn ghost" id="es-srs-show">Show answer</button>\' +\n'
        '        \'<div class="rates" id="es-srs-rates" style="display:none;margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">\' +\n'
        '        \'<button type="button" class="btn ghost" data-r="again">Again</button>\' +\n'
        '        \'<button type="button" class="btn ghost" data-r="hard">Hard</button>\' +\n'
        '        \'<button type="button" class="btn" data-r="good">Good</button>\' +\n'
        '        \'<button type="button" class="btn" data-r="easy">Easy</button></div>\';\n'
        '      var sayBtn = box.querySelector("#es-srs-say");\n'
        '      if (sayBtn) sayBtn.addEventListener("click", function (e) {\n'
        '        e.preventDefault();\n'
        '        var A = window.EkGuruHindiAudio;\n'
        '        if (A && A.supported()) A.speak(String(card.target || card.prompt), sayBtn, "es-ES");\n'
        '      });\n'
        '      box.querySelector("#es-srs-show").addEventListener("click", function () {\n'
        '        box.querySelector("#es-srs-a").style.display = "block";\n'
        '        box.querySelector("#es-srs-rates").style.display = "flex";\n'
        '        this.style.display = "none";\n'
        '      });\n'
        '      box.querySelectorAll("[data-r]").forEach(function (b) {\n'
        '        b.addEventListener("click", function () { window.EkGuruSRS.review(card.card_id, b.getAttribute("data-r")); paint(); });\n'
        '      });\n'
        '    }\n'
        '    document.getElementById("es-srs-seed").addEventListener("click", function () { var n = seed(); queue = []; paint(); });\n'
        '    document.getElementById("es-srs-reset").addEventListener("click", function () {\n'
        '      window.EkGuruSRS.all().forEach(function (c) { if (c.language === "es") window.EkGuruSRS.remove(c.card_id); });\n'
        '      queue = []; paint();\n'
        '    });\n'
        '    if (window.EkGuruSRS) paint();\n'
        '    else window.addEventListener("load", paint);\n'
        '  })();\n'
        '  </script>\n'
    )
    write_page("languages/es/review/index.html", "../../../",
               "Spanish Review — spaced repetition",
               "Review the Spanish words and phrases you saved, on a simple spaced-repetition schedule that lives in your browser.",
               "languages/es/review/",
               '<a href="/">EkGuru</a> › <a href="/languages/">Languages</a> › <a href="/languages/es/">Spanish</a> › Review',
               body, scripts=["course-es.js", "hindi-srs.js", "hindi-audio.js"], index=False,
               extra_style=".hi-listen{display:inline-flex;align-items:center;gap:5px;margin:0 0 0 8px;padding:4px 10px;font-size:.82rem;line-height:1.4;border-radius:999px;border:1px solid var(--line);background:var(--bg-soft);color:var(--ink);cursor:pointer;vertical-align:middle}"
                            ".hi-listen.playing{background:var(--brand);border-color:var(--brand);color:#fff}"
                            "#es-srs-card .prompt{font-size:1.15rem;font-weight:700;margin-bottom:14px}")
    return "languages/es/review/index.html"


def build_bank_js():
    data = {"practice": PRACTICE, "quiz": QUIZ, "review": REVIEW}
    js = ("/* EkGuru — SPANISH COURSE BANK (authored, single source of truth).\n"
          "   Generated by tools/build-language-course.py — do not hand-edit. */\n"
          "window.EKGURU_COURSE_ES = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n")
    with open("js/course-es.js", "w", encoding="utf-8") as f:
        f.write(js)
    return "js/course-es.js"


def build_manifest():
    manifest = {
        "generated": NOW,
        "policy": ("A language gets a course object only when real authored lessons + practice + quiz + "
                   "review exist. A course keeps a language BETA (still not Hindi-depth, still no "
                   "recorded audio). PRODUCTION remains Hindi only."),
        "courses": [
            {"lang": "es", "name": "Spanish", "status": "BETA",
             "lessons": len(LESSONS), "practiceItems": sum(len(v) for v in PRACTICE.values()),
             "quizQuestions": len(QUIZ), "reviewCards": len(REVIEW),
             "url": "languages/es/course/", "note": COURSE["note"]},
        ],
    }
    with open("data/courses.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return "data/courses.json"


def main():
    made = []
    made.append(build_bank_js())
    made += build_lessons()
    made.append(build_course_hub())
    made.append(build_practice())
    made.append(build_quiz())
    made.append(build_review())
    made.append(build_manifest())
    print("Spanish course built:")
    for m in made:
        print("  ", m)


if __name__ == "__main__":
    main()

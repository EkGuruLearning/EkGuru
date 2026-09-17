#!/usr/bin/env python3
"""Authored Arabic course data. Language config + content.
Loaded by tools/build-world-course.py. Do not hand-edit the generated
output pages; edit THIS file and regenerate.
Content is authored by hand, not machine-translated.
Modern Standard Arabic; dialect notes where everyday speech differs.
"""

COURSE = {
 "lang": "ar",
 "name": "Arabic",
 "native": "العربية",
 "speechTag": "ar-SA",
 "status": "Available",
 "note": "A real, authored Arabic course: 6 lessons, a practice lab, a topic quiz and a review deck — all running on the same engines as Hindi. It is not yet as deep as the Hindi course, and all audio is your browser's computer voice, never a native recording."
}

LESSONS = [
 {
  "slug": "greetings-and-introductions",
  "title": "Arabic Greetings and Introductions",
  "desc": "Every Arabic greeting you actually need, the peace greeting and its answer, and how to introduce yourself — with pronunciation and examples.",
  "sections": [
   [
    "Peace upon you — and upon you peace",
    [
     "The universal Arabic greeting is <b>السلام عليكم</b> (as-salāmu ʿalaykum — peace upon you), used by Muslims and non-Muslims alike, any hour, any register. It demands its answer: <b>وعليكم السلام</b> (wa ʿalaykum as-salām — and upon you peace). Returning it is close to obligatory — silence reads as cold. The casual hello is <b>مرحبا</b> (marḥaban); time-based greetings are <b>صباح الخير</b> (morning of goodness) and <b>مساء الخير</b> (evening of goodness)."
    ]
   ],
   [
    "Introducing yourself",
    [
     "To give your name: <b>أنا اسمي…</b> (anā ismī… — I, my name is…). <b>أنا اسمي علي</b> introduces Ali. To ask: <b>ما اسمك؟</b> (mā ismuk? — to a man) or <b>ما اسمك؟</b> (mā ismuk? — to a woman; pronounced ismik). Same spelling, different ending — Arabic marks gender in speech constantly. Origin: <b>أنا من الهند</b> (anā min al-hind — I am from India)."
    ]
   ],
   [
    "You (man) vs you (woman)",
    [
     "Arabic has no formal/informal \"you\" like European languages — instead \"you\" splits by GENDER: <b>أنتَ</b> (anta — you, to a man) and <b>أنتِ</b> (anti — to a woman). Verbs and adjectives follow: <b>كيف حالك؟</b> (kīf ḥāluk? — how are you, to a man) vs <b>كيف حالك؟</b> (kīf ḥālik? — to a woman). Respect is shown through titles and plural verbs, not pronouns: address strangers as <b>أستاذ/أستاذة</b> (ustādh/ustādha — sir/madam)."
    ]
   ],
   [
    "Thanks, please and goodbye",
    [
     "<b>شكرا</b> (shukran) is thanks; <b>شكرا جزيلا</b> (shukran jazīlan) adds weight. There is no single word for \"please\" — requests use <b>من فضلك</b> (min faḍlik — to a man) / <b>من فضلك</b> (min faḍlik — to a woman), literally \"from your grace\". The reply to thanks is <b>عفوا</b> (ʿafwan — pardon/excuse). Goodbye: <b>مع السلامة</b> (maʿa as-salāma — go with safety) or <b>إلى اللقاء</b> (until the meeting)."
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
     "السلام عليكم",
     "peace upon you — the universal hello"
    ],
    [
     "وعليكم السلام",
     "and upon you peace — the required answer"
    ],
    [
     "صباح الخير / مساء الخير",
     "good morning / good evening"
    ],
    [
     "مرحبا",
     "hello — casual"
    ],
    [
     "مع السلامة",
     "goodbye — go with safety"
    ],
    [
     "شكرا / عفوا",
     "thanks / you're welcome"
    ],
    [
     "من فضلك",
     "please — from your grace"
    ]
   ]
  ]
 },
 {
  "slug": "alphabet-and-sounds",
  "title": "The Arabic Alphabet and Sounds",
  "desc": "Twenty-eight letters written right to left, the sounds English lacks, short vowels, and sun and moon letters.",
  "sections": [
   [
    "Twenty-eight letters, right to left",
    [
     "Arabic writes right to left in 28 letters, nearly all of which join their neighbours — each letter has up to four shapes (alone, starting, middle, ending). Six letters refuse to join leftward (<b>ا د ذ ر ز و</b>), which is why words break where they do. There are no capital letters. The good news: spelling is almost perfectly phonetic — learn the letters and you can sound out anything, including words you don't know."
    ]
   ],
   [
    "The sounds English lacks",
    [
     "Four sounds need new throat work: <b>ع</b> (ʿayn — a voiced squeeze deep in the throat), <b>ح</b> (ḥā — a breathy h from the same place), <b>ق</b> (qāf — a k from the far back) and <b>خ</b> (khā — like clearing your throat, as in Scottish loch). The \"emphatic\" consonants (<b>ص ض ط ظ</b>) are s/d/t/dh spoken with a dark, hollow resonance. Arabs will understand approximations — but the effort to learn ع and ح earns instant warmth."
    ]
   ],
   [
    "Short vowels are usually invisible",
    [
     "Arabic writes long vowels (<b>ا و ي</b>) but normally OMITS short ones: <b>كتب</b> could be kataba (he wrote), kutiba (it was written) or kutub (books) — context and grammar decide. Beginners' texts add <b>حركات</b> (ḥarakāt — vowel marks): <b>ـَ ـِ ـُ</b> for a/i/u. Don't fight this: read vowelled texts first, and your grammar will resolve the unvowelled ones sooner than you expect."
    ]
   ],
   [
    "Sun and moon letters",
    [
     "The definite article <b>الـ</b> (al- — the) behaves two ways. Before \"moon\" letters it keeps its ل: <b>القمر</b> (al-qamar — the moon). Before \"sun\" letters (ت ث د ذ ر ز س ش ص ض ط ظ ل ن) the ل vanishes and the sun letter doubles: <b>الشمس</b> is pronounced ash-shams (the sun), though still written with ل. The spelling never changes — only the pronunciation. Memorise the 14 sun letters once."
    ]
   ]
  ],
  "table": [
   [
    "Feature",
    "Example"
   ],
   [
    [
     "direction",
     "right to left — السلام عليكم"
    ],
    [
     "ع (ʿayn)",
     "deep voiced squeeze — عربي (Arab)"
    ],
    [
     "ح (ḥā)",
     "breathy h — حب (love)"
    ],
    [
     "short vowels",
     "usually unwritten — كتب = kataba/kutub"
    ],
    [
     "moon letter",
     "القمر = al-qamar (ل pronounced)"
    ],
    [
     "sun letter",
     "الشمس = ash-shams (ل assimilated)"
    ]
   ]
  ]
 },
 {
  "slug": "pronouns-and-to-be",
  "title": "Arabic Pronouns and To Be",
  "desc": "Twelve pronouns, a present tense with no \"is\", possession with عند, and the إضافة that builds Arabic phrases.",
  "sections": [
   [
    "Twelve pronouns",
    [
     "Arabic pronouns split by gender AND number — including a dual (two people): <b>أنا</b> (I), <b>أنتَ/أنتِ</b> (you m/f), <b>هو/هي</b> (he/she), <b>نحن</b> (we), <b>أنتم/أنتن</b> (you all m/f), <b>هم/هن</b> (they m/f), plus dual forms. In practice, verbs carry the endings so pronouns are dropped unless emphasised: <b>أنا طالب</b> stresses I (I am a student — and proud of it); <b>طالب</b> alone suffices."
    ]
   ],
   [
    "Present \"is\" doesn't exist",
    [
     "Like Russian, Arabic omits \"is\" in the present: <b>هو طالب</b> (he [is a] student), <b>القهوة لذيذة</b> (the coffee [is] delicious). Past and future use <b>كان</b> (kāna — was) and <b>سيكون/سوف</b>: <b>كان طالبا</b> (he was a student). Negating identity uses <b>ليس</b> (laysa — is not), which conjugates: <b>لست طالبا</b> (I am not a student), <b>ليس هنا</b> (he/it is not here)."
    ]
   ],
   [
    "\"I have\" = \"at me\"",
    [
     "Possession uses <b>عند</b> (ʿind — at): <b>عندي كتاب</b> (ʿindī kitāb — at-me a book — I have a book). The owner takes pronoun suffixes: <b>عندك/عندك</b> (you m/f have), <b>عنده/عندها</b> (he/she has), <b>عندنا</b> (we have). Dialects vary the preposition — Egypt says <b>معايا</b>, the Levant <b>عندي</b> too — but MSA عند works everywhere on paper."
    ]
   ],
   [
    "The إضافة — possession without \"of\"",
    [
     "Arabic joins possessed + possessor directly, with NO word for \"of\": <b>كتاب الطالب</b> (kitāb aṭ-ṭālib — book the-student — the student's book). This construction, the <b>إضافة</b> (iḍāfa), chains freely: <b>مفتاح باب البيت</b> (key door the-house — the house door's key). The first word never takes الـ; definiteness comes from the last word. Master إضافة and Arabic sentences unlock."
    ]
   ]
  ],
  "table": [
   [
    "Pattern",
    "Example"
   ],
   [
    [
     "zero copula (is)",
     "هو طالب — he is a student"
    ],
    [
     "ليس (is not)",
     "لست طالبا — I am not a student"
    ],
    [
     "عندي (I have)",
     "عندي كتاب — I have a book"
    ],
    [
     "إضافة (possession)",
     "كتاب الطالب — the student's book"
    ],
    [
     "كان (was)",
     "كان هنا — he was here"
    ],
    [
     "أنتَ / أنتِ",
     "you — to a man / to a woman"
    ]
   ]
  ]
 },
 {
  "slug": "numbers-1-to-20",
  "title": "Arabic Numbers 1 to 20",
  "desc": "Count to twenty, survive the gender polarity of 3–10, say your age, and tell the time.",
  "sections": [
   [
    "واحد to عشرة",
    [
     "The first ten: <b>واحد, اثنان, ثلاثة, أربعة, خمسة, ستة, سبعة, ثمانية, تسعة, عشرة</b>. One and two AGREE with the noun's gender: <b>كتاب واحد</b> (one book, m) but <b>سيارة واحدة</b> (one car, f); <b>كتابان</b> but <b>سيارتان</b>. Note that واحد follows the noun (<b>كتاب واحد</b>) while the rest precede it (<b>ثلاثة كتب</b>) — the first of several number quirks."
    ]
   ],
   [
    "The polarity of 3–10",
    [
     "Numbers 3–10 show <b>polarity</b>: they take the OPPOSITE gender to the noun. <b>ثلاثة كتب</b> (three books — masculine noun, feminine-looking number with ة) but <b>ثلاث طالبات</b> (three students — feminine noun, bare number). The ة marks feminine everywhere else in Arabic — except here, where it marks masculine nouns. Drill with real nouns until it stops feeling backwards."
    ]
   ],
   [
    "Eleven to twenty",
    [
     "Teens compound with <b>عشر</b>: <b>أحد عشر, اثنا عشر, ثلاثة عشر… تسعة عشر</b> (11–19), then <b>عشرون</b> (20). Eleven and twelve agree in gender (<b>أحد عشر كتابا / إحدى عشرة سيارة</b>); 13–19 keep polarity in the first digit (<b>ثلاثة عشر كتابا</b>). Counted nouns go singular after 11+: <b>أحد عشر كتابا</b> (eleven book — singular!). Twenty, thirty (<b>ثلاثون</b>) and beyond never change for gender."
    ]
   ],
   [
    "Age, time and money",
    [
     "Age: <b>عمري عشرون سنة</b> (ʿumrī ʿishrūn sana — my age twenty years — I am 20), asked as <b>كم عمرك؟</b> (to a man) / <b>كم عمرك؟</b> (to a woman). Time: <b>الساعة الثالثة</b> (the hour the-third — three o'clock). Money varies by country (riyal, dinar, dirham, pound) — prices are haggled in souqs with <b>بكم؟</b> (bikam? — for how much?)."
    ]
   ]
  ],
  "table": [
   [
    "Number",
    "Arabic"
   ],
   [
    [
     "1–2 (agree)",
     "واحد/واحدة، اثنان/اثنتان"
    ],
    [
     "3–10 (polarity!)",
     "ثلاثة كتب / ثلاث طالبات"
    ],
    [
     "11–12 (agree)",
     "أحد عشر / إحدى عشرة"
    ],
    [
     "13–20",
     "ثلاثة عشر… عشرون"
    ],
    [
     "How old are you?",
     "كم عمرك؟ (m) / كم عمرك؟ (f)"
    ],
    [
     "I am 20 years old",
     "عمري عشرون سنة"
    ]
   ]
  ]
 },
 {
  "slug": "food-and-ordering",
  "title": "Arabic Food and Ordering",
  "desc": "Order confidently in any Arab restaurant: the phrases, hospitality rules, and bread culture.",
  "sections": [
   [
    "Ordering politely",
    [
     "The ordering verbs are <b>أريد…</b> (urīdu… — I want…) or softer <b>ممكن…</b> (mumkin… — is it possible…): <b>أريد شايا، من فضلك</b> (I want tea, please). Staff ask <b>تفضل، ماذا تريد؟</b> (go ahead — what do you want?). To get attention: <b>لو سمحت!</b> (law samaḥt — if you permit!). Menus: <b>القائمة</b> (al-qā'ima). Pointing plus <b>هذا، من فضلك</b> (this one, please) works everywhere."
    ]
   ],
   [
    "Hospitality is sacred",
    [
     "Guests are a trust from God — hosts press food relentlessly, and refusing outright offends. Accept at least tea: <b>شاي</b> (shāy) comes sweet and endless in the Gulf; mint tea (<b>أتاي</b>) rules North Africa. Coffee (<b>قهوة</b>) is served in tiny cups — wiggle your cup to decline more. Never refuse with the left hand; eat, give and receive with the right."
    ]
   ],
   [
    "Bread, mains and paying",
    [
     "Bread (<b>خبز</b> — khubz) is the utensil — tear, scoop, never cut with a knife. Core words: <b>ماء</b> (water), <b>أرز</b> (rice), <b>لحم</b> (meat), <b>دجاج</b> (chicken), <b>سلطة</b> (salad). The bill: <b>الحساب لو سمحت</b> (al-ḥisāb law samaḥt). Tipping varies (10–15% in Levant/Egypt restaurants; service charges common in Gulf hotels). Delicious: <b>لذيذ!</b> (ladhīdh!)."
    ]
   ],
   [
    "Before and after eating",
    [
     "Before eating, say <b>بسم الله</b> (bismillāh — in God's name); after, <b>الحمد لله</b> (al-ḥamdu lillāh — praise God). Hosts urge <b>كل! كل!</b> (kul! — eat! eat!). Compliment the cook with <b>تسلم إيديك</b> (dialect — bless your hands). Hunger: <b>أنا جائع</b> (man) / <b>أنا جائعة</b> (woman); thirst: <b>أنا عطشان/عطشانة</b>."
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
     "أريد…، من فضلك",
     "I want… — the ordering phrase"
    ],
    [
     "القائمة، لو سمحت",
     "the menu, please"
    ],
    [
     "الحساب لو سمحت",
     "the bill, please"
    ],
    [
     "بسم الله",
     "in God's name — said before eating"
    ],
    [
     "أنا جائع / جائعة",
     "I am hungry — man / woman"
    ],
    [
     "لذيذ!",
     "delicious!"
    ]
   ]
  ]
 },
 {
  "slug": "present-tense-verbs",
  "title": "Arabic Present Tense — Verbs",
  "desc": "The root system in miniature: prefixes and suffixes that conjugate يكتب, negation with لا, and questions.",
  "sections": [
   [
    "Roots, not stems",
    [
     "Arabic verbs grow from three-consonant ROOTS: <b>ك-ت-ب</b> (k-t-b) carries \"writing\" — <b>كتاب</b> (book), <b>مكتبة</b> (library), <b>كاتب</b> (writer) and the verb <b>يكتب</b> (he writes) all share it. Learn roots and vocabulary multiplies: one root unlocks a family. The present tense wraps the root in prefixes (who) with occasional suffixes (gender/number)."
    ]
   ],
   [
    "The present-tense pattern",
    [
     "Take <b>يكتب</b> (to write): <b>أنا أكتب, أنتَ تكتب, أنتِ تكتبين, هو يكتب, هي تكتب, نحن نكتب, أنتم تكتبون, هم يكتبون</b>. The prefix shows the person (أ/ت/ي/ن) and feminine/plural add suffixes (<b>ـين/ـون</b>). Note أنتَ and هي share <b>تكتب</b> — context separates them. Drill one verb fully; every sound verb follows."
    ]
   ],
   [
    "Negation and questions",
    [
     "Present negation is <b>لا</b> before the verb: <b>لا أعرف</b> (I don't know), <b>لا يتكلم العربية</b> (he doesn't speak Arabic). (Past uses <b>ما/لم</b>, future <b>لن</b> — later lessons.) Questions need no inversion: <b>هل تتكلم العربية؟</b> (do you speak Arabic?) or pure intonation <b>تتكلم العربية؟</b> Question words: <b>أين تسكن؟</b> (where do you live?), <b>ماذا تعمل؟</b> (what do you do?)."
    ]
   ],
   [
    "The verbs you need first",
    [
     "Priority verbs: <b>يعرف</b> (know), <b>يفهم</b> (understand), <b>يسكن</b> (live), <b>يعمل</b> (work/do), <b>يقرأ</b> (read), <b>يكتب</b> (write), <b>يتكلم</b> (speak), <b>يدرس</b> (study). <b>لا أفهم</b> (I don't understand) is your shield; <b>ممكن تعيد؟</b> (can you repeat?) your sword. Arabic \"speak Arabic\" is <b>يتكلم العربية</b> — the language takes الـ, unlike most nouns you are used to."
    ]
   ]
  ],
  "table": [
   [
    "Person",
    "يكتب (to write)"
   ],
   [
    [
     "أنا",
     "أكتب"
    ],
    [
     "أنتَ / أنتِ",
     "تكتب / تكتبين"
    ],
    [
     "هو / هي",
     "يكتب / تكتب"
    ],
    [
     "نحن",
     "نكتب"
    ],
    [
     "أنتم / هم",
     "تكتبون / يكتبون"
    ]
   ]
  ]
 }
]

PRACTICE = {
 "vocabulary": [
  {"q": "What does “السلام عليكم” mean?", "a": "peace upon you", "opts": ["good morning", "peace upon you", "goodbye", "thank you"], "explain": "As-salāmu ʿalaykum — peace upon you — the universal hello."},
  {"q": "The required answer is…", "a": "وعليكم السلام", "opts": ["وعليكم السلام", "مع السلامة", "أهلا وسهلا", "مرحبا بك"], "explain": "Wa ʿalaykum as-salām — and upon you peace."},
  {"q": "“شكرا” means…", "a": "thanks", "opts": ["please", "thanks", "sorry", "hello"], "explain": "Shukran is thanks; عفوا answers it."},
  {"q": "The reply to thanks is…", "a": "عفوا", "opts": ["عفوا", "شكرا", "من فضلك", "لو سمحت"], "explain": "ʿAfwan — pardon — answers shukran."},
  {"q": "What does “الحساب” mean?", "a": "the bill", "opts": ["the menu", "the bill", "the table", "the tip"], "explain": "Al-ḥisāb law samaḥt — the bill, please."},
  {"q": "“أنا جائع” (man speaking) means…", "a": "I am hungry", "opts": ["I am thirsty", "I am hungry", "I am tired", "I am full"], "explain": "Anā jā'iʿ — I am hungry (man; woman: jā'iʿa)."},
  {"q": "“لذيذ!” means…", "a": "delicious!", "opts": ["big!", "delicious!", "hot!", "sweet!"], "explain": "Ladhīdh! praises the food."},
  {"q": "“الشمس” is pronounced…", "a": "ash-shams", "opts": ["al-shams", "ash-shams", "as-shams", "el-shams"], "explain": "ش is a sun letter: the ل assimilates — ash-shams."},
  {"q": "“بسم الله” is said…", "a": "before eating", "opts": ["after eating", "before eating", "when paying", "when leaving"], "explain": "Bismillāh opens the meal."},
  {"q": "“أنا اسمي علي” means…", "a": "my name is Ali", "opts": ["my name is Ali", "I know Ali", "call Ali", "Ali knows me"], "explain": "Anā ismī… — I, my name is…"},
  {"q": "“كتب” without vowels shows that…", "a": "short vowels are usually unwritten", "opts": ["Arabic has no vowels", "short vowels are usually unwritten", "all words look alike", "vowels don't matter"], "explain": "Kataba/kutub share كتب — context decides."},
  {"q": "“لا أفهم” means…", "a": "I don't understand", "opts": ["I don't know", "I don't understand", "I don't speak", "I don't hear"], "explain": "Lā afham — the beginner's shield."}
 ],
 "grammar": [
  {"q": "“You” to a woman is…", "a": "أنتِ", "opts": ["أنتَ", "أنتِ", "هو", "نحن"], "explain": "Anti — you to a woman; anta to a man."},
  {"q": "“He is a student” is…", "a": "هو طالب", "opts": ["هو طالب", "هو يكون طالب", "هو في طالب", "طالب هو يكون"], "explain": "Present \"is\" is omitted: هو طالب."},
  {"q": "“I am not a student” is…", "a": "لست طالبا", "opts": ["لا أنا طالب", "لست طالبا", "أنا مش طالب", "ما أنا طالب"], "explain": "Laysa negates identity: لست طالبا."},
  {"q": "“I have a book” is…", "a": "عندي كتاب", "opts": ["أنا عندي كتاب", "عندي كتاب", "لي كتاب عند", "أملك كتابا"], "explain": "ʿIndī kitāb — at-me a book."},
  {"q": "“The student's book” is…", "a": "كتاب الطالب", "opts": ["الكتاب الطالب", "كتاب الطالب", "كتاب لطالب", "الطالب كتاب"], "explain": "Iḍāfa: possessed + possessor, no \"of\"."},
  {"q": "“Three books” (masculine noun) is…", "a": "ثلاثة كتب", "opts": ["ثلاث كتب", "ثلاثة كتب", "ثلاثة كتاب", "ثلث كتب"], "explain": "Polarity: masculine noun takes ثلاثة."},
  {"q": "“Three (female) students” is…", "a": "ثلاث طالبات", "opts": ["ثلاثة طالبات", "ثلاث طالبات", "ثلاث طالبة", "ثالث طالبات"], "explain": "Polarity: feminine noun takes bare ثلاث."},
  {"q": "“I write” is…", "a": "أكتب", "opts": ["أكتب", "تكتب", "يكتب", "نكتب"], "explain": "أ prefix marks أنا: أكتب."},
  {"q": "“She writes” is…", "a": "تكتب", "opts": ["يكتب", "تكتب", "أكتب", "نكتب"], "explain": "هي takes ت: تكتب (same as أنتَ)."},
  {"q": "“I don't know” is…", "a": "لا أعرف", "opts": ["لا أعرف", "ما أعرف", "لم أعرف", "لن أعرف"], "explain": "Present negation: لا + verb."},
  {"q": "“Where do you (m) live?” is…", "a": "أين تسكن؟", "opts": ["أين تسكن؟", "أين أسكن؟", "أين يسكن؟", "أين نسكن؟"], "explain": "No inversion: أين تسكن؟"},
  {"q": "“My age is 20” is…", "a": "عمري عشرون سنة", "opts": ["عمري عشرون سنة", "أنا عشرون سنة", "عندي عشرون سنة", "سني عشرون عام"], "explain": "ʿUmrī ʿishrūn sana."}
 ]
}

QUIZ = [
 {"id": "ar-greet-1", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "What does “صباح الخير” mean?", "a": "good morning", "opts": ["good morning", "good evening", "good night", "goodbye"], "explain": "Ṣabāḥ al-khayr — morning of goodness."},
 {"id": "ar-greet-2", "lesson": "greetings-and-introductions", "type": "usage", "topic": "greetings", "level": "beginner", "q": "Someone says السلام عليكم. You answer…", "a": "وعليكم السلام", "opts": ["مع السلامة", "وعليكم السلام", "مرحبا", "أهلا"], "explain": "The greeting demands its answer."},
 {"id": "ar-greet-3", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "“مع السلامة” means…", "a": "goodbye (go with safety)", "opts": ["good morning", "goodbye (go with safety)", "welcome", "please sit"], "explain": "Maʿa as-salāma — go with safety."},
 {"id": "ar-greet-4", "lesson": "greetings-and-introductions", "type": "usage", "topic": "greetings", "level": "beginner", "q": "Ask a woman's name. You say…", "a": "ما اسمك؟ (ismik)", "opts": ["ما اسمك؟ (ismik)", "ما اسمك؟ (ismuk)", "ما هو اسمك؟", "كيف اسمك؟"], "explain": "To a woman: mā ismik?"},
 {"id": "ar-alpha-1", "lesson": "alphabet-and-sounds", "type": "vocab", "topic": "script", "level": "beginner", "q": "Arabic is written…", "a": "right to left", "opts": ["left to right", "right to left", "top to bottom", "in columns"], "explain": "Right to left, letters joining."},
 {"id": "ar-alpha-2", "lesson": "alphabet-and-sounds", "type": "vocab", "topic": "script", "level": "beginner", "q": "“القمر” (the moon) is pronounced…", "a": "al-qamar", "opts": ["al-qamar", "aq-qamar", "el-qamar", "ash-qamar"], "explain": "ق is a moon letter: the ل stays — al-qamar."},
 {"id": "ar-alpha-3", "lesson": "alphabet-and-sounds", "type": "meaning", "topic": "script", "level": "beginner", "q": "Short vowels are usually…", "a": "omitted in writing", "opts": ["written always", "omitted in writing", "written in red", "spoken only"], "explain": "Ḥarakāt appear in learners' texts, rarely elsewhere."},
 {"id": "ar-pro-1", "lesson": "pronouns-and-to-be", "type": "vocab", "topic": "grammar", "level": "beginner", "q": "“They (men)” is…", "a": "هم", "opts": ["هن", "هم", "أنتم", "نحن"], "explain": "Hum — they (masculine); hunna (هن) feminine."},
 {"id": "ar-pro-2", "lesson": "pronouns-and-to-be", "type": "usage", "topic": "grammar", "level": "beginner", "q": "Say “the house door's key” (chain). You say…", "a": "مفتاح باب البيت", "opts": ["مفتاح باب البيت", "المفتاح الباب البيت", "مفتاح لباب لبيت", "بيت باب مفتاح"], "explain": "Iḍāfa chains: مفتاح باب البيت."},
 {"id": "ar-pro-3", "lesson": "pronouns-and-to-be", "type": "meaning", "topic": "grammar", "level": "beginner", "q": "“هو طالب” has no “is” because…", "a": "present \"is\" is omitted", "opts": ["طالب means is", "present \"is\" is omitted", "هو means is", "Arabic has no verbs"], "explain": "Zero copula in the present."},
 {"id": "ar-num-1", "lesson": "numbers-1-to-20", "type": "vocab", "topic": "numbers", "level": "beginner", "q": "“سبعة” is the number…", "a": "7", "opts": ["6", "7", "9", "17"], "explain": "Sitta is 6, sabʿa is 7."},
 {"id": "ar-num-2", "lesson": "numbers-1-to-20", "type": "vocab", "topic": "numbers", "level": "beginner", "q": "“One car” (feminine) is…", "a": "سيارة واحدة", "opts": ["سيارة واحد", "سيارة واحدة", "واحدة سيارة", "واحد سيارة"], "explain": "Feminine one: واحدة, after the noun."},
 {"id": "ar-num-3", "lesson": "numbers-1-to-20", "type": "usage", "topic": "numbers", "level": "beginner", "q": "Ask a man's age. You say…", "a": "كم عمرك؟ (ʿumruk)", "opts": ["كم عمرك؟ (ʿumruk)", "كم عمرك؟ (ʿumrik)", "كم سنة لك؟", "ما عمرك أنت؟"], "explain": "To a man: kam ʿumruk?"},
 {"id": "ar-food-1", "lesson": "food-and-ordering", "type": "usage", "topic": "food", "level": "beginner", "q": "Order tea politely. You say…", "a": "أريد شايا، من فضلك", "opts": ["أريد شايا، من فضلك", "أعطني شاي الآن", "شاي بسرعة", "أبغى شاي حال"], "explain": "Urīdu shāyan, min faḍlik."},
 {"id": "ar-food-2", "lesson": "food-and-ordering", "type": "meaning", "topic": "food", "level": "beginner", "q": "“الحساب لو سمحت” means…", "a": "the bill, please", "opts": ["the menu, please", "the bill, please", "one more, please", "table for two"], "explain": "Al-ḥisāb — the bill."},
 {"id": "ar-food-3", "lesson": "food-and-ordering", "type": "vocab", "topic": "food", "level": "beginner", "q": "Bread (the utensil) is…", "a": "خبز", "opts": ["خبز", "أرز", "لحم", "ماء"], "explain": "Khubz — tear and scoop with it."},
 {"id": "ar-verb-1", "lesson": "present-tense-verbs", "type": "vocab", "topic": "verbs", "level": "beginner", "q": "“نكتب” — the prefix marks…", "a": "نحن (we)", "opts": ["أنا", "أنت", "نحن (we)", "هم"], "explain": "The ن prefix always marks نحن."},
 {"id": "ar-verb-2", "lesson": "present-tense-verbs", "type": "usage", "topic": "verbs", "level": "beginner", "q": "Ask “where do you (m) live?”. You say…", "a": "أين تسكن؟", "opts": ["أين تسكن؟", "أين أسكن؟", "أين يسكن؟", "أين سكنت؟"], "explain": "No inversion: أين تسكن؟"},
 {"id": "ar-verb-3", "lesson": "present-tense-verbs", "type": "meaning", "topic": "verbs", "level": "beginner", "q": "كتاب، مكتبة and كاتب share…", "a": "the root ك-ت-ب (writing)", "opts": ["the same vowels", "the root ك-ت-ب (writing)", "the same length", "nothing — coincidence"], "explain": "One root, one family: writing."},
 {"id": "ar-greet-5", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "“من فضلك” literally means…", "a": "from your grace", "opts": ["from your grace", "with sugar", "by order", "under God"], "explain": "Min faḍlik — from your grace."}
]

REVIEW = [
 {"p": "السلام عليكم", "a": "peace upon you (hello)"},
 {"p": "وعليكم السلام", "a": "and upon you peace (answer)"},
 {"p": "صباح الخير", "a": "good morning"},
 {"p": "مساء الخير", "a": "good evening"},
 {"p": "مع السلامة", "a": "goodbye"},
 {"p": "شكرا", "a": "thanks"},
 {"p": "عفوا", "a": "you're welcome"},
 {"p": "من فضلك", "a": "please"},
 {"p": "أنا اسمي…", "a": "my name is…"},
 {"p": "أنتَ / أنتِ", "a": "you (to man / woman)"},
 {"p": "هو طالب", "a": "he is a student"},
 {"p": "عندي…", "a": "I have…"},
 {"p": "كتاب الطالب", "a": "the student's book"},
 {"p": "واحد، اثنان، ثلاثة", "a": "one, two, three"},
 {"p": "عشرون", "a": "twenty"},
 {"p": "عمري عشرون سنة", "a": "I am 20 years old"},
 {"p": "أريد…", "a": "I want…"},
 {"p": "الحساب لو سمحت", "a": "the bill, please"},
 {"p": "بسم الله", "a": "in God's name (before eating)"},
 {"p": "لذيذ!", "a": "delicious!"},
 {"p": "أكتب", "a": "I write"},
 {"p": "لا أعرف", "a": "I don't know"},
 {"p": "لا أفهم", "a": "I don't understand"},
 {"p": "أين تسكن؟", "a": "where do you live?"}
]

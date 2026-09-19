#!/usr/bin/env python3
"""Authored Russian course data. Language config + content.
Loaded by tools/build-world-course.py. Do not hand-edit the generated
output pages; edit THIS file and regenerate.
Content is authored by hand, not machine-translated.
"""

COURSE = {
 "lang": "ru",
 "name": "Russian",
 "native": "русский",
 "speechTag": "ru-RU",
 "status": "Available",
 "note": "A real, authored Russian course: 6 lessons, a practice lab, a topic quiz and a review deck — all running on the same engines as Hindi. It is not yet as deep as the Hindi course, and all audio is your browser's computer voice, never a native recording."
}

LESSONS = [
 {
  "slug": "greetings-and-introductions",
  "title": "Russian Greetings and Introductions",
  "desc": "Every Russian greeting you actually need, when to use ты and вы, and how to introduce yourself — with pronunciation and examples.",
  "sections": [
   [
    "The greetings that cover most situations",
    [
     "Russian greets by time of day: <b>доброе утро</b> (good morning), <b>добрый день</b> (good day) and <b>добрый вечер</b> (good evening). The formal hello is <b>здравствуйте</b> (literally \"be healthy\" — the first в is silent: zdRA-stvooy-tye); the informal one is <b>привет</b>. Goodbye is <b>до свидания</b> (formal, \"until seeing\") or <b>пока</b> (informal). Russians shake hands on meeting AND parting — but never across a threshold."
    ]
   ],
   [
    "Introducing yourself",
    [
     "To give your name: <b>Меня зовут…</b> (me they-call… — \"I am called\") or <b>Я…</b> (I am…). <b>Меня зовут Анна</b> and <b>Я Анна</b> both introduce Anna. To ask: <b>Как тебя зовут?</b> (informal) or <b>Как вас зовут?</b> (formal). Origin: <b>Я из Индии</b> (I am from India). Russians also give their <b>отчество</b> (patronymic — father's name) in formal settings: Anna Petrovna."
    ]
   ],
   [
    "Ты vs вы — the register choice",
    [
     "For \"you\", <b>ты</b> is for friends, family, children and peers; <b>вы</b> is for strangers, older people, officials — and always for groups. Russia switches to <b>ты</b> slower than southern Europe: colleagues may use <b>вы</b> for years. The invitation <b>давай на ты</b> (let's switch to ты) is a small ceremony of friendship. Students and young people use <b>ты</b> with each other freely."
    ]
   ],
   [
    "Please, thanks and sorry",
    [
     "<b>Спасибо</b> is thanks; <b>большое спасибо</b> (big thanks) adds weight. <b>Пожалуйста</b> does triple duty: please, you're welcome, and here-you-are. <b>Извините</b> (formal) / <b>извини</b> (informal) apologises; <b>простите</b> begs pardon more deeply. To get attention: <b>Извините!</b> The reply to thanks is also <b>пожалуйста</b> — context tells you which meaning."
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
     "здравствуйте / привет",
     "hello — formal / informal"
    ],
    [
     "доброе утро",
     "good morning"
    ],
    [
     "добрый день",
     "good day — the default daytime greeting"
    ],
    [
     "добрый вечер",
     "good evening"
    ],
    [
     "до свидания / пока",
     "goodbye — formal / informal"
    ],
    [
     "спасибо / пожалуйста",
     "thanks / please, you're welcome"
    ],
    [
     "Меня зовут…",
     "I am called… — introducing yourself"
    ]
   ]
  ]
 },
 {
  "slug": "nouns-gender-and-cases",
  "title": "Russian Nouns, Gender and Cases",
  "desc": "Three genders you can see in the ending, and the case system that replaces English word order — starting with the nominative.",
  "sections": [
   [
    "Three genders, visible endings",
    [
     "Every Russian noun is masculine, feminine or neuter, and the ending usually shows it: consonant-ending nouns are masculine (<b>стол</b>, table), <b>-а/-я</b> nouns are feminine (<b>книга</b>, book), <b>-о/-е</b> nouns are neuter (<b>окно</b>, window). Nouns ending in <b>-ь</b> (soft sign) can be either — <b>ночь</b> (night) is feminine but <b>день</b> (day) is masculine — so learn those with their gender. Adjectives agree: <b>новый стол</b> but <b>новая книга</b>."
    ]
   ],
   [
    "Six cases — why word order is free",
    [
     "Russian nouns change endings by <b>case</b> — six of them — which marks each word's job in the sentence. Because the endings carry the grammar, word order is flexible: <b>Мама любит папу</b> and <b>Папу любит мама</b> both mean \"mum loves dad\" (папу's accusative ending proves who is loved). English relies on position; Russian relies on endings. This lesson uses only the <b>nominative</b> (dictionary form, the subject) — the other five come later."
    ]
   ],
   [
    "No articles at all",
    [
     "Russian has no words for \"the\" or \"a\" — <b>книга</b> means the book, a book, or just book depending on context. Beginners from English keep reaching for a missing article; stop reaching. <b>Это книга</b> (this is a/the book), <b>Книга на столе</b> (the book is on the table). Context does all the work articles do in English, and Russians never miss them."
    ]
   ],
   [
    "Plurals and spelling rules",
    [
     "Masculine nouns mostly add <b>-ы/-и</b> (<b>стол → столы</b>), feminines change <b>-а → -ы</b> (<b>книга → книги</b>), neuters change <b>-о → -а</b> (<b>окно → окна</b>). Two spelling rules override everything: after <b>ж, ш, ч, щ</b> write <b>-и</b> never <b>-ы</b> (<b>нож → ножи</b>), and after <b>к, г, х, ж, ш, ч, щ</b> write <b>-е</b> never unstressed <b>-о</b>. These rules have no exceptions — learn them once."
    ]
   ]
  ],
  "table": [
   [
    "Ending",
    "Gender and example"
   ],
   [
    [
     "consonant",
     "masculine — стол (table)"
    ],
    [
     "-а / -я",
     "feminine — книга (book), земля (land)"
    ],
    [
     "-о / -е",
     "neuter — окно (window), море (sea)"
    ],
    [
     "-ь",
     "either — ночь (f, night), день (m, day)"
    ],
    [
     "plural -ы/-и",
     "стол → столы, книга → книги"
    ],
    [
     "plural -а",
     "окно → окна (neuter pattern)"
    ]
   ]
  ]
 },
 {
  "slug": "byt-and-imet",
  "title": "Быть and У меня есть — Being and Having",
  "desc": "Russian drops \"is\" in the present, builds \"I have\" backwards, and says existence with есть — the three patterns behind half of all sentences.",
  "sections": [
   [
    "The present tense of \"to be\" is silence",
    [
     "In the present tense, Russian simply omits the verb \"to be\": <b>Он студент</b> (he [is a] student), <b>Книга интересная</b> (the book [is] interesting). A dash often marks the gap in writing: <b>Москва — столица</b> (Moscow — the capital). Past and future DO use forms of <b>быть</b> (<b>был/была/было/были</b> — was; <b>буду</b> — will be), but the present is zero. Saying <b>есть</b> (is) in these sentences is the classic beginner error."
    ]
   ],
   [
    "Есть — existence, not identity",
    [
     "<b>Есть</b> survives only for existence and possession: <b>В Москве есть метро</b> (in Moscow there is a metro), <b>Здесь есть вода?</b> (is there water here?). Its negative is <b>нет</b> — a whole word, not a prefix: <b>Времени нет</b> (there is no time). Never use <b>есть</b> for identity or description — <b>Он есть студент</b> is wrong; <b>Он студент</b> is right."
    ]
   ],
   [
    "\"I have\" works backwards",
    [
     "Possession uses <b>у меня есть</b> — literally \"at me there is\": <b>У меня есть книга</b> (I have a book), <b>У тебя есть время?</b> (do you have time?). The owner sits in the genitive case (<b>у меня, у тебя, у него/неё, у нас, у вас, у них</b>) and the THING is the grammatical subject. Negative: <b>У меня нет времени</b> (I have no time — note нет + genitive). This pattern feels alien for a week, then becomes automatic."
    ]
   ],
   [
    "Negation: не vs нет",
    [
     "<b>Не</b> negates verbs and adjectives: <b>Я не знаю</b> (I don't know), <b>Это не хорошо</b> (this is not good). <b>Нет</b> means \"no\" as an answer, \"there is no\" for existence, and partners <b>у меня</b> for having-nothing. The pair to drill: <b>У меня есть</b> (I have) vs <b>У меня нет</b> (I don't have); <b>Здесь есть</b> (there is) vs <b>Здесь нет</b> (there isn't)."
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
     "Он студент — he is a student"
    ],
    [
     "есть (there is)",
     "Здесь есть вода — there is water here"
    ],
    [
     "у меня есть (I have)",
     "У меня есть книга — I have a book"
    ],
    [
     "нет (there is no)",
     "Времени нет — there is no time"
    ],
    [
     "у меня нет (I don't have)",
     "У меня нет времени — I have no time"
    ],
    [
     "не + verb",
     "Я не знаю — I don't know"
    ]
   ]
  ]
 },
 {
  "slug": "numbers-1-to-20",
  "title": "Russian Numbers 1 to 20",
  "desc": "Count to twenty, handle the three genders of one and two, say your age the Russian way, and tell the time.",
  "sections": [
   [
    "Один to десять",
    [
     "The first ten: <b>один, два, три, четыре, пять, шесть, семь, восемь, девять, десять</b>. Stress matters: <b>одИн, два, три, четЫре, пять, шесть, семь, вОсемь, дЕвять, дЕсять</b>. <b>Один</b> has three genders — <b>один стол</b> (one table, m), <b>одна книга</b> (one book, f), <b>одно окно</b> (one window, n) — and <b>два</b> has two: <b>два стола</b> but <b>две книги</b> (feminine две). From три on, numbers never change for gender."
    ]
   ],
   [
    "Eleven to twenty",
    [
     "Teens fuse the digit with <b>-надцать</b> (on-ten): <b>одиннадцать, двенадцать, тринадцать, четырнадцать, пятнадцать, шестнадцать, семнадцать, восемнадцать, девятнадцать</b>, then <b>двадцать</b> (20). Stress the <b>-на-</b>: <b>пятнАдцать</b>. The tens continue the pattern outward: <b>тридцать</b> (30), <b>сорок</b> (40 — irregular!), <b>пятьдесят</b> (50). Compounds just join: 21 is <b>двадцать один</b>."
    ]
   ],
   [
    "Age: years decline",
    [
     "Age uses the dative + год family: <b>Мне двадцать лет</b> (to-me twenty years — I am 20). The word for \"years\" cycles: <b>1 год, 2–4 года, 5–20 лет</b>, then repeats (<b>21 год, 22 года, 25 лет</b>). Ask with <b>Сколько тебе лет?</b> (informal) or <b>Сколько вам лет?</b> (formal). Children under ten often answer with fingers plus <b>мне пять</b>."
    ]
   ],
   [
    "Time and quantities",
    [
     "Hours: <b>Сейчас три часа</b> (now three hours — it is three o'clock); one o'clock is <b>Сейчас час</b>. Half hours count FORWARD in Russian: 3:30 is <b>половина четвёртого</b> (half of the fourth [hour])! Counting objects needs case endings beyond this lesson — but one, two and the nominative plural cover daily survival: <b>два билета</b> (two tickets), <b>три чашки чая</b> (three cups of tea)."
    ]
   ]
  ],
  "table": [
   [
    "Number",
    "Russian"
   ],
   [
    [
     "1–5",
     "один, два, три, четыре, пять"
    ],
    [
     "6–10",
     "шесть, семь, восемь, девять, десять"
    ],
    [
     "11–15",
     "одиннадцать… пятнадцать"
    ],
    [
     "16–20",
     "шестнадцать… девятнадцать, двадцать"
    ],
    [
     "How old are you?",
     "Сколько тебе лет? / Сколько вам лет?"
    ],
    [
     "I am 20 years old",
     "Мне двадцать лет"
    ]
   ]
  ]
 },
 {
  "slug": "food-and-ordering",
  "title": "Russian Food and Ordering",
  "desc": "Order confidently in any Russian café or stolovaya: the phrases, table words, and tea culture.",
  "sections": [
   [
    "Ordering politely",
    [
     "The polite ordering verbs are <b>Я бы хотел…</b> (man speaking) / <b>Я бы хотела…</b> (woman speaking) — \"I would like\" — or the simpler <b>Можно мне…</b> (may I have…): <b>Можно мне чай, пожалуйста</b>. Staff ask <b>Что будете заказывать?</b> (what will you order?). To get attention: <b>Извините!</b> In a <b>столовая</b> (canteen) just point at the tray line and say <b>Мне, пожалуйста…</b> (for me…)."
    ]
   ],
   [
    "Tea is a ritual",
    [
     "Russia runs on <b>чай</b> (tea) — drunk black, strong, all day, from a <b>стакан</b> (glass) in a metal holder on trains. <b>Чай с лимоном</b> (tea with lemon) is standard; milk in tea reads as foreign. Coffee is <b>кофе</b> (masculine despite the -е ending — a famous exception). Offering tea is hospitality itself: refusing twice is polite ritual; the third offer, accept."
    ]
   ],
   [
    "At the table and paying",
    [
     "Table words: <b>меню</b> (menu), <b>стакан</b> (glass), <b>чашка</b> (cup), <b>тарелка</b> (plate), <b>ложка/вилка/нож</b> (spoon/fork/knife). The bill is <b>счёт</b>: <b>Счёт, пожалуйста</b>. Before eating, wish <b>Приятного аппетита!</b> Service charges are rare — 5–10% cash tip for good service is the norm. Splitting the bill: <b>Разделим счёт?</b> (shall we split?)."
    ]
   ],
   [
    "Hunger, bread and soup",
    [
     "Hunger uses <b>хотеть есть</b>: <b>Я хочу есть</b> (I want to eat — I am hungry). Core words: <b>хлеб</b> (bread — sacred; never waste it), <b>суп/борщ</b> (soup/borscht), <b>вода</b> (water — <b>с газом</b> sparkling, <b>без газа</b> still), <b>молоко</b> (milk). Delicious: <b>Очень вкусно!</b> (very tasty!). Bread and salt (<b>хлеб-соль</b>) remain the traditional welcome for honoured guests."
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
     "Можно мне…, пожалуйста",
     "may I have… — the ordering phrase"
    ],
    [
     "Меню, пожалуйста",
     "the menu, please"
    ],
    [
     "Счёт, пожалуйста",
     "the bill, please"
    ],
    [
     "Приятного аппетита!",
     "enjoy your meal — said before eating"
    ],
    [
     "Я хочу есть",
     "I am hungry (I want to eat)"
    ],
    [
     "Очень вкусно!",
     "very tasty!"
    ]
   ]
  ]
 },
 {
  "slug": "present-tense-verbs",
  "title": "Russian Present Tense — Verbs",
  "desc": "Two conjugations, one pattern each: first-conjugation читать and second-conjugation говорить, plus negation and questions.",
  "sections": [
   [
    "Two conjugations",
    [
     "Russian verbs fall into two conjugations. First conjugation (the bigger one): <b>читать</b> (to read) gives <b>я читаю, ты читаешь, он читает, мы читаем, вы читаете, они читают</b>. Second conjugation: <b>говорить</b> (to speak) gives <b>я говорю, ты говоришь, он говорит, мы говорим, вы говорите, они говорят</b>. The endings rhyme by person — learn the six slots once and every regular verb follows."
    ]
   ],
   [
    "Which conjugation?",
    [
     "The infinitive ending predicts it: verbs in <b>-ать/-ять/-еть</b> are usually first conjugation (<b>читать, делать</b>), verbs in <b>-ить</b> are usually second (<b>говорить, учить</b>) — with a famous gang of exceptions (<b>жить, плыть</b> and friends). Stress shifts in some verbs: <b>писать</b> gives <b>я пишу</b> (I write) with с→ш mutation. Dictionaries mark conjugation; textbooks drill the exceptions early."
    ]
   ],
   [
    "Negation and questions",
    [
     "Negation is <b>не</b> before the verb: <b>Я не знаю</b> (I don't know), <b>Он не говорит по-русски</b> (he doesn't speak Russian). Questions need no inversion — intonation (ИК-3, the rise-fall) turns <b>Ты говоришь по-русски?</b> into \"do you speak Russian?\". Question words lead: <b>Где ты живёшь?</b> (where do you live?), <b>Что ты делаешь?</b> (what are you doing?)."
    ]
   ],
   [
    "The verbs you need first",
    [
     "Priority verbs: <b>знать</b> (know a fact), <b>понимать</b> (understand), <b>жить</b> (live — <b>я живу</b>), <b>делать</b> (do), <b>читать</b> (read), <b>писать</b> (write), <b>говорить</b> (speak), <b>учить</b> (learn/teach). Note <b>по-русски</b> (in Russian — adverb, never changes) vs <b>русский язык</b> (the Russian language, noun). <b>Я не понимаю</b> (I don't understand) is your shield; <b>Повторите, пожалуйста</b> (repeat, please) is your sword."
    ]
   ]
  ],
  "table": [
   [
    "Person",
    "читать (to read)"
   ],
   [
    [
     "я",
     "читаю"
    ],
    [
     "ты",
     "читаешь"
    ],
    [
     "он / она",
     "читает"
    ],
    [
     "мы",
     "читаем"
    ],
    [
     "вы",
     "читаете"
    ],
    [
     "они",
     "читают"
    ]
   ]
  ]
 }
]

PRACTICE = {
 "vocabulary": [
  {"q": "What does “здравствуйте” mean?", "a": "hello (formal)", "opts": ["hello (formal)", "hello (informal)", "goodbye", "thanks"], "explain": "Здравствуйте is the formal hello — the first в is silent."},
  {"q": "“Добрый день” is used…", "a": "in the daytime", "opts": ["in the morning", "in the daytime", "in the evening", "at night"], "explain": "Добрый день is the default daytime greeting."},
  {"q": "“Пока” means…", "a": "bye (informal)", "opts": ["hello", "bye (informal)", "please", "sorry"], "explain": "Пока is informal bye; до свидания is formal."},
  {"q": "The reply to “спасибо” is…", "a": "пожалуйста", "opts": ["пожалуйста", "извините", "привет", "давай"], "explain": "Пожалуйста means please, you're welcome and here-you-are."},
  {"q": "What does “счёт” mean?", "a": "the bill", "opts": ["the menu", "the bill", "the table", "the tip"], "explain": "Счёт, пожалуйста — the bill, please."},
  {"q": "“Я хочу есть” means…", "a": "I am hungry", "opts": ["I am thirsty", "I am hungry", "I want to drink", "I am full"], "explain": "Я хочу есть — I want to eat — is how hunger is said."},
  {"q": "“Очень вкусно!” means…", "a": "very tasty!", "opts": ["very big!", "very tasty!", "very fast!", "very hot!"], "explain": "Очень вкусно! praises the food."},
  {"q": "“Двенадцать” is the number…", "a": "12", "opts": ["2", "12", "20", "22"], "explain": "Двенадцать is 12; двадцать is 20."},
  {"q": "What does “Приятного аппетита!” mean?", "a": "enjoy your meal!", "opts": ["the bill please", "enjoy your meal!", "one more!", "no sugar"], "explain": "Приятного аппетита opens the meal."},
  {"q": "“Меня зовут Анна” means…", "a": "I am called Anna", "opts": ["I am called Anna", "I know Anna", "call Anna", "Anna knows me"], "explain": "Меня зовут… — I am called…"},
  {"q": "“Кофе” is surprising because…", "a": "it is masculine despite -е", "opts": ["it is feminine", "it is masculine despite -е", "it is plural", "it is indeclinable"], "explain": "Кофе breaks the -е = neuter pattern: masculine."},
  {"q": "“Я не понимаю” means…", "a": "I don't understand", "opts": ["I don't know", "I don't understand", "I don't speak", "I don't remember"], "explain": "Я не понимаю — the beginner's shield."}
 ],
 "grammar": [
  {"q": "“Книга” (book) is…", "a": "feminine", "opts": ["masculine", "feminine", "neuter", "plural"], "explain": "-а ending → feminine: книга."},
  {"q": "“Окно” (window) is…", "a": "neuter", "opts": ["masculine", "feminine", "neuter", "plural"], "explain": "-о ending → neuter: окно."},
  {"q": "The plural of “стол” is…", "a": "столы", "opts": ["столы", "столи", "стола", "столыи"], "explain": "Masculine + -ы: стол → столы."},
  {"q": "“He is a student” is…", "a": "Он студент", "opts": ["Он студент", "Он есть студент", "Он ест студент", "Студент он есть"], "explain": "Present \"is\" is omitted: Он студент."},
  {"q": "“I have a book” is…", "a": "У меня есть книга", "opts": ["Я имею книгу", "У меня есть книга", "Мне есть книга", "Я есть с книгой"], "explain": "У меня есть — at me there is."},
  {"q": "“I have no time” is…", "a": "У меня нет времени", "opts": ["У меня не время", "У меня нет времени", "Я нет времени", "Мне не время"], "explain": "У меня нет + genitive: времени."},
  {"q": "“You (informal) read” is…", "a": "ты читаешь", "opts": ["ты читаю", "ты читаешь", "ты читает", "ты читаем"], "explain": "First conjugation: ты читаешь."},
  {"q": "“They speak” is…", "a": "они говорят", "opts": ["они говорю", "они говоришь", "они говорят", "они говорите"], "explain": "Second conjugation: они говорят."},
  {"q": "“I don't know” is…", "a": "Я не знаю", "opts": ["Я не знаю", "Я нет знаю", "Не я знаю", "Я знаю не"], "explain": "Не before the verb: Я не знаю."},
  {"q": "“Where do you live?” (informal) is…", "a": "Где ты живёшь?", "opts": ["Где ты живёшь?", "Где живёшь ты?", "Где ты живёт?", "Ты где живёшь есть?"], "explain": "No inversion: Где ты живёшь?"},
  {"q": "“Two books” (feminine) is…", "a": "две книги", "opts": ["два книги", "две книги", "две книга", "два книга"], "explain": "Feminine two: две книги."},
  {"q": "“I am 20” (age) is…", "a": "Мне двадцать лет", "opts": ["Я двадцать лет", "Мне двадцать лет", "Я имею двадцать", "Мне двадцать года"], "explain": "Dative + лет: Мне двадцать лет."}
 ]
}

QUIZ = [
 {"id": "ru-greet-1", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "What does “добрый вечер” mean?", "a": "good evening", "opts": ["good morning", "good day", "good evening", "good night"], "explain": "Добрый вечер is good evening."},
 {"id": "ru-greet-2", "lesson": "greetings-and-introductions", "type": "usage", "topic": "greetings", "level": "beginner", "q": "You greet an official at noon. You say…", "a": "здравствуйте", "opts": ["привет", "здравствуйте", "пока", "давай"], "explain": "Officials get здравствуйте, never привет."},
 {"id": "ru-greet-3", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "“До свидания” literally means…", "a": "until seeing (again)", "opts": ["until seeing (again)", "go with God", "stay well", "farewell forever"], "explain": "До свидания — until seeing — the formal goodbye."},
 {"id": "ru-greet-4", "lesson": "greetings-and-introductions", "type": "usage", "topic": "greetings", "level": "beginner", "q": "Ask a stranger's name (formal). You say…", "a": "Как вас зовут?", "opts": ["Как тебя зовут?", "Как вас зовут?", "Кто ты?", "Что ты?"], "explain": "Strangers get вы: Как вас зовут?"},
 {"id": "ru-noun-1", "lesson": "nouns-gender-and-cases", "type": "vocab", "topic": "grammar", "level": "beginner", "q": "“Стол” (table) is…", "a": "masculine", "opts": ["masculine", "feminine", "neuter", "plural"], "explain": "Consonant ending → masculine: стол."},
 {"id": "ru-noun-2", "lesson": "nouns-gender-and-cases", "type": "vocab", "topic": "grammar", "level": "beginner", "q": "The plural of “окно” is…", "a": "окна", "opts": ["окны", "окни", "окна", "окон"], "explain": "Neuter -о becomes -а: окно → окна."},
 {"id": "ru-noun-3", "lesson": "nouns-gender-and-cases", "type": "meaning", "topic": "grammar", "level": "beginner", "q": "Russian word order is free because…", "a": "case endings mark each word's job", "opts": ["verbs never move", "case endings mark each word's job", "there are no nouns", "adjectives fix positions"], "explain": "Cases carry the grammar, so position is flexible."},
 {"id": "ru-byt-1", "lesson": "byt-and-imet", "type": "vocab", "topic": "verbs", "level": "beginner", "q": "“There is water here” is…", "a": "Здесь есть вода", "opts": ["Здесь вода есть", "Здесь есть вода", "Вода здесь есть", "Есть здесь вода есть"], "explain": "Existence uses есть: Здесь есть вода."},
 {"id": "ru-byt-2", "lesson": "byt-and-imet", "type": "usage", "topic": "verbs", "level": "beginner", "q": "Say “I don't have time”. You say…", "a": "У меня нет времени", "opts": ["У меня нет времени", "Я не время", "Мне нет время", "У меня не времени"], "explain": "У меня нет + genitive."},
 {"id": "ru-byt-3", "lesson": "byt-and-imet", "type": "meaning", "topic": "verbs", "level": "beginner", "q": "“Он есть студент” is wrong because…", "a": "present \"is\" is omitted", "opts": ["есть means eats", "present \"is\" is omitted", "студент is feminine", "он needs вы"], "explain": "Он студент — no есть for identity."},
 {"id": "ru-num-1", "lesson": "numbers-1-to-20", "type": "vocab", "topic": "numbers", "level": "beginner", "q": "“Восемь” is the number…", "a": "8", "opts": ["7", "8", "9", "18"], "explain": "Семь is 7, восемь is 8."},
 {"id": "ru-num-2", "lesson": "numbers-1-to-20", "type": "vocab", "topic": "numbers", "level": "beginner", "q": "“Пятнадцать” is…", "a": "15", "opts": ["5", "15", "50", "55"], "explain": "Пятнадцать is 15 — stress on -на-."},
 {"id": "ru-num-3", "lesson": "numbers-1-to-20", "type": "usage", "topic": "numbers", "level": "beginner", "q": "Ask a friend's age (informal). You say…", "a": "Сколько тебе лет?", "opts": ["Сколько тебе лет?", "Сколько вам лет?", "Тебе сколько года?", "Сколько лет у тебя?"], "explain": "Friends get тебе: Сколько тебе лет?"},
 {"id": "ru-food-1", "lesson": "food-and-ordering", "type": "usage", "topic": "food", "level": "beginner", "q": "Order tea politely. You say…", "a": "Можно мне чай, пожалуйста", "opts": ["Можно мне чай, пожалуйста", "Дай мне чай", "Хочу чай сейчас", "Чай мне давай"], "explain": "Можно мне… пожалуйста is the polite phrase."},
 {"id": "ru-food-2", "lesson": "food-and-ordering", "type": "meaning", "topic": "food", "level": "beginner", "q": "“Счёт, пожалуйста” means…", "a": "the bill, please", "opts": ["the menu, please", "the bill, please", "one more, please", "table for two"], "explain": "Счёт is the bill."},
 {"id": "ru-food-3", "lesson": "food-and-ordering", "type": "vocab", "topic": "food", "level": "beginner", "q": "Still water is…", "a": "вода без газа", "opts": ["вода с газом", "вода без газа", "горячая вода", "холодная вода"], "explain": "Без газа is still; с газом is sparkling."},
 {"id": "ru-verb-1", "lesson": "present-tense-verbs", "type": "vocab", "topic": "verbs", "level": "beginner", "q": "“Читают” — the ending marks…", "a": "они (they)", "opts": ["я", "ты", "мы", "они (they)"], "explain": "The -ют/-ут ending always marks они."},
 {"id": "ru-verb-2", "lesson": "present-tense-verbs", "type": "usage", "topic": "verbs", "level": "beginner", "q": "Ask “do you speak Russian?” (informal). You say…", "a": "Ты говоришь по-русски?", "opts": ["Ты говоришь по-русски?", "Говоришь ты по-русски?", "Ты говорит по-русски?", "Ты говорю по-русски?"], "explain": "No inversion: Ты говоришь по-русски?"},
 {"id": "ru-verb-3", "lesson": "present-tense-verbs", "type": "meaning", "topic": "verbs", "level": "beginner", "q": "“Я пишу” shows…", "a": "a с→ш stem mutation", "opts": ["an irregular ending", "a с→ш stem mutation", "a borrowed verb", "past tense"], "explain": "Писать mutates: я пишу."},
 {"id": "ru-greet-5", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "“Давай на ты” means…", "a": "let's switch to ты", "opts": ["let's switch to ты", "goodbye, friend", "speak louder", "write it down"], "explain": "Давай на ты — the invitation to informality."}
]

REVIEW = [
 {"p": "здравствуйте", "a": "hello (formal)"},
 {"p": "привет", "a": "hello (informal)"},
 {"p": "добрый день", "a": "good day"},
 {"p": "до свидания", "a": "goodbye (formal)"},
 {"p": "пока", "a": "bye (informal)"},
 {"p": "спасибо", "a": "thanks"},
 {"p": "пожалуйста", "a": "please / you're welcome"},
 {"p": "Меня зовут…", "a": "I am called…"},
 {"p": "Он студент", "a": "he is a student (no \"is\")"},
 {"p": "У меня есть…", "a": "I have…"},
 {"p": "У меня нет…", "a": "I don't have…"},
 {"p": "есть / нет", "a": "there is / there isn't"},
 {"p": "один, два, три", "a": "one, two, three"},
 {"p": "двадцать", "a": "twenty"},
 {"p": "Мне двадцать лет", "a": "I am 20 years old"},
 {"p": "Можно мне…", "a": "may I have…"},
 {"p": "Счёт, пожалуйста", "a": "the bill, please"},
 {"p": "Приятного аппетита!", "a": "enjoy your meal!"},
 {"p": "Очень вкусно!", "a": "very tasty!"},
 {"p": "я читаю", "a": "I read"},
 {"p": "ты говоришь", "a": "you speak (informal)"},
 {"p": "Я не знаю", "a": "I don't know"},
 {"p": "Я не понимаю", "a": "I don't understand"},
 {"p": "Где ты живёшь?", "a": "where do you live?"}
]

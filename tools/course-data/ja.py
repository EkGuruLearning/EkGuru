#!/usr/bin/env python3
"""Authored Japanese course data. Language config + content.
Loaded by tools/build-world-course.py. Do not hand-edit the generated
output pages; edit THIS file and regenerate.
Content is authored by hand, not machine-translated.
Polite です/ます style throughout; romaji given alongside kana.
"""

COURSE = {
 "lang": "ja",
 "name": "Japanese",
 "native": "日本語",
 "speechTag": "ja-JP",
 "status": "Available",
 "note": "A real, authored Japanese course: 6 lessons, a practice lab, a topic quiz and a review deck — all running on the same engines as Hindi. It is not yet as deep as the Hindi course, and all audio is your browser's computer voice, never a native recording."
}

LESSONS = [
 {
  "slug": "greetings-and-introductions",
  "title": "Japanese Greetings and Introductions",
  "desc": "Greet through the day, introduce yourself with よろしく, and bow at the right depth — with particles は and も.",
  "sections": [
   [
    "Greetings through the day",
    [
     "Morning: <b>おはようございます</b> (ohayō gozaimasu). Daytime: <b>こんにちは</b> (konnichiwa — note the は pronounced \"wa\"). Evening: <b>こんばんは</b> (konbanwa). On the phone: <b>もしもし</b> (moshi moshi). Leaving before others: <b>お先に失礼します</b> (osaki ni shitsurei shimasu — excuse me for leaving first); those staying answer <b>お疲れ様でした</b> (otsukaresama deshita — thank you for your work)."
    ]
   ],
   [
    "Introducing yourself",
    [
     "The template: <b>はじめまして。私はラヴィです。インドから来ました。よろしくおねがいします。</b> (Hajimemashite. Watashi wa Ravi desu. Indo kara kimashita. Yoroshiku onegai shimasu.) — How do you do; I am Ravi; I came from India; please treat me well. <b>よろしく</b> has no English equivalent — it hands the relationship to the other person. Family name first: <b>田中さん</b> is Mr/Ms Tanaka."
    ]
   ],
   [
    "Bowing, at the right depth",
    [
     "Words ride on bows: a 15° nod (<b>eshaku</b>) for casual greetings, 30° for clients and thanks, 45°+ for deep apology. Hold eye contact until the bow starts, hands at sides (men) or folded front (women). Foreigners are not graded on angle — attempting the bow matters more than perfecting it. Business cards (<b>名刺</b> meishi) are exchanged with both hands and studied, never pocketed."
    ]
   ],
   [
    "Thanks and goodbye",
    [
     "<b>ありがとうございます</b> (arigatō gozaimasu) is full thanks; <b>どうも</b> is its casual shadow. \"You're welcome\" is <b>どういたしまして</b>. Apology doubles as thanks: <b>すみません</b> (sumimasen) covers excuse me, sorry, and thank you for the trouble. Goodbye varies by situation: <b>さようなら</b> is final; friends say <b>じゃあね / またね</b>; at home it's <b>いってきます</b> answered by <b>いってらっしゃい</b>."
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
     "おはようございます",
     "good morning — full polite form"
    ],
    [
     "こんにちは / こんばんは",
     "hello (day) / good evening"
    ],
    [
     "はじめまして",
     "how do you do — first meetings"
    ],
    [
     "よろしくおねがいします",
     "please treat me well — ends introductions"
    ],
    [
     "ありがとうございます",
     "thank you — full form"
    ],
    [
     "すみません",
     "excuse me / sorry / thanks for trouble"
    ]
   ]
  ]
 },
 {
  "slug": "scripts-and-particles",
  "title": "Three Scripts and Particles",
  "desc": "Hiragana, katakana and kanji in one lesson, the topic particle は vs subject が, and を・に・へ・で.",
  "sections": [
   [
    "Three scripts, one sentence",
    [
     "Japanese mixes three scripts: <b>ひらがな</b> (hiragana — native words and grammar), <b>カタカナ</b> (katakana — foreign words: <b>コーヒー</b> kōhī), and <b>漢字</b> (kanji — meaning-characters from China: <b>日本語</b> nihongo). A normal sentence uses all three: <b>私はコーヒーを飲みます</b> (I drink coffee). Learn hiragana first (46 characters, a weekend's work), katakana next, kanji gradually."
    ]
   ],
   [
    "は (wa) vs が (ga)",
    [
     "The most famous distinction in Japanese: <b>は</b> marks the TOPIC (what we're talking about), <b>が</b> marks the SUBJECT (who does it). <b>私は学生です</b> (as for me — student): neutral. <b>私が学生です</b> (I am the one who is a student): emphasis, answering \"who?\". Rule of thumb: new information takes が (<b>誰が来ますか</b> — who is coming?), established topics take は."
    ]
   ],
   [
    "を・に・へ・で in one pass",
    [
     "<b>を</b> (o) marks the object: <b>本を読みます</b> (read a book). <b>に</b> (ni) marks destination/time: <b>学校に行きます</b> (go to school), <b>八時に</b> (at 8). <b>へ</b> (e) marks direction with a nuance of journey: <b>日本へ行きます</b>. <b>で</b> (de) marks where an action happens: <b>図書館で勉強します</b> (study at the library) — versus <b>に</b> for where things ARE: <b>図書館にいます</b>."
    ]
   ],
   [
    "も and か — also and questions",
    [
     "<b>も</b> (mo) means also/too, replacing は: <b>私も学生です</b> (I too am a student). <b>か</b> (ka) ends questions: <b>学生ですか</b> (are you a student?) — answered <b>はい/いいえ</b> (hai/iie). Note: はい to a negative question confirms the NEGATIVE (\"aren't you?\" — \"はい\" = correct, I'm not). Question words: <b>何・誰・どこ・いつ・なぜ・どうやって</b> (what, who, where, when, why, how)."
    ]
   ]
  ],
  "table": [
   [
    "Particle",
    "Job and example"
   ],
   [
    [
     "は (wa)",
     "topic — 私は学生です"
    ],
    [
     "が (ga)",
     "subject/new info — 私が学生です"
    ],
    [
     "を (o)",
     "object — 本を読みます"
    ],
    [
     "に (ni)",
     "destination/time — 学校に行きます"
    ],
    [
     "で (de)",
     "place of action — 図書館で勉強します"
    ],
    [
     "か (ka)",
     "question — 学生ですか"
    ]
   ]
  ]
 },
 {
  "slug": "desu-aru-iru",
  "title": "です, ある and いる",
  "desc": "Identity with です, existence split by animacy with ある/いる, possession, and polite negation.",
  "sections": [
   [
    "です — identity and adjectives",
    [
     "<b>です</b> (desu) links identity: <b>私は先生です</b> (I am a teacher). Adjectives split into two tribes: <b>い-adjectives</b> conjugate themselves (<b>高いです</b> — is expensive; <b>高くないです</b> — isn't), while <b>な-adjectives</b> need です (<b>静かです</b> — is quiet; <b>静かじゃありません</b> — isn't). Past: <b>でした</b> (<b>学生でした</b> — was a student). Polite negative: <b>じゃありません / ではありません</b>."
    ]
   ],
   [
    "ある vs いる — alive or not?",
    [
     "Existence splits by animacy: <b>いる</b> (iru) for living things, <b>ある</b> (aru) for the rest. <b>猫がいます</b> (there is a cat), <b>本があります</b> (there is a book). Location first: <b>机の上に本があります</b> (on the desk there is a book). Negatives: <b>いません / ありません</b>. Robots and company departments take いる — if it moves with purpose, it's alive."
    ]
   ],
   [
    "\"I have\" through existence",
    [
     "Possession is expressed as existence-at-me: <b>私は車があります</b> (as for me, a car exists — I have a car). Siblings: <b>兄弟がいます</b> (I have siblings). Time and events use ある: <b>時間がありますか</b> (do you have time?), <b>会議があります</b> (there is a meeting). No verb \"to have\" exists — existence covers it."
    ]
   ],
   [
    "Politeness is grammar",
    [
     "です/ます is the polite baseline — plain forms (<b>だ・である</b>, dictionary verbs) wait for friends and writing. Above polite sits <b>keigo</b> (honorific language): humble verbs for your own acts (<b>参ります</b> for go), exalted verbs for others' (<b>いらっしゃいます</b>). Beginners: master です/ます everywhere — over-polite beats under-polite with every stranger."
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
     "です (identity)",
     "私は先生です — I am a teacher"
    ],
    [
     "い-adjective",
     "高いです / 高くないです"
    ],
    [
     "な-adjective",
     "静かです / 静かじゃありません"
    ],
    [
     "いる (animate)",
     "猫がいます — there is a cat"
    ],
    [
     "ある (inanimate)",
     "本があります — there is a book"
    ],
    [
     "possession",
     "私は車があります — I have a car"
    ]
   ]
  ]
 },
 {
  "slug": "numbers-and-counters",
  "title": "Japanese Numbers and Counters",
  "desc": "Count to 99, tell age and time, and survive the counter system — 人, つ, 本, 枚 and the sound changes.",
  "sections": [
   [
    "One to ten, two readings",
    [
     "Japanese numbers have native (<b>kun</b>) and Chinese-derived (<b>on</b>) readings: <b>ひとつ ふたつ みっつ よっつ いつつ むっつ ななつ やっつ ここのつ とお</b> (1–10 native) vs <b>いち に さん し/よん ご ろく しち/なな はち きゅう じゅう</b> (on). Modern counting mostly uses on-readings: <b>じゅういち</b> (11), <b>にじゅう</b> (20), <b>きゅうじゅうきゅう</b> (99). Note 4 avoids し (death) → <b>よん</b>; 7 prefers <b>なな</b>; 9 prefers <b>きゅう</b>."
    ]
   ],
   [
    "Counters: every shape counts differently",
    [
     "Like Chinese measure words, but shape-based: <b>人</b> (nin — people: <b>三人</b> sannin), <b>つ</b> (tsu — generic things: <b>みっつ</b>), <b>本</b> (hon — long things: <b>三本</b> sanbon), <b>枚</b> (mai — flat things: <b>三枚</b> sanmai), <b>匹</b> (hiki — small animals), <b>冊</b> (satsu — books). Default to <b>つ</b> when unsure — natives will supply the right one with a smile."
    ]
   ],
   [
    "Sound changes: 一本, 三本",
    [
     "一 (ichi) mutates before h/k/s/p sounds: <b>一本 = いっぽん</b> (ippon), <b>一匹 = いっぴき</b> (ippiki), <b>六本 = ろっぽん</b> (roppon), <b>三本 = さんぼん</b> (sanbon — no change). These <b>euphonic changes</b> are fixed per counter — learn them as chunks (ippon, nihon, sanbon) rather than rules. Dictionaries list each counter's readings."
    ]
   ],
   [
    "Age, time and money",
    [
     "Age: <b>二十歳</b> (hatachi — 20, special reading!) or <b>二十一歳</b> (nijūissai — 21). Asking age is sensitive — <b>おいくつですか</b> softens it. Time: <b>三時</b> (san-ji — 3 o'clock), <b>三時半</b> (half past). Money: <b>円</b> (en/yen): <b>いくらですか</b> (how much?). Bills over coins: even ¥10,000 notes are used daily."
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
     "1–10 (on)",
     "いち に さん よん ご ろく なな はち きゅう じゅう"
    ],
    [
     "11 / 20 / 99",
     "じゅういち / にじゅう / きゅうじゅうきゅう"
    ],
    [
     "people",
     "三人 (さんにん) — three people"
    ],
    [
     "sound change",
     "一本 = いっぽん (ippon)"
    ],
    [
     "I am 21",
     "二十一歳 (にじゅういっさい)"
    ],
    [
     "How much?",
     "いくらですか"
    ]
   ]
  ]
 },
 {
  "slug": "food-and-ordering",
  "title": "Japanese Food and Ordering",
  "desc": "Order with ください, say いただきます properly, handle ramen counters and izakaya, and pay at the register.",
  "sections": [
   [
    "Ordering with ください",
    [
     "The magic pattern: <b>〜をください</b> (…o kudasai — …please): <b>ラーメンをください</b>, <b>お水をください</b> (water, please). At counters: <b>これをください</b> (this one, please) with a point. Asking what's good: <b>おすすめは何ですか</b> (what do you recommend?). Allergic: <b>〜アレルギーがあります</b>. Vegetarian: <b>ベジタリアンです</b> — then specify, since dashi (fish stock) hides everywhere."
    ]
   ],
   [
    "いただきます and ごちそうさま",
    [
     "Before eating, hands together: <b>いただきます</b> (itadakimasu — I humbly receive). After: <b>ごちそうさまでした</b> (gochisōsama deshita — thank you for the feast). These are said to the cook, the ingredients, everyone — skipping them reads as rude. At someone's home add <b>おいしいです!</b> (it's delicious!) early and often."
    ]
   ],
   [
    "Ramen counters and izakaya",
    [
     "Ramen shops: buy a ticket from the machine (<b>食券</b> shokken), hand it to staff, state noodle firmness (<b>かため</b> — firm) and extras. Slurping is CORRECT — it cools noodles and signals enjoyment. Izakaya (pubs): first shout <b>とりあえずビール!</b> (for now, beer!), share everything, pour for others — never for yourself. <b>お通し</b> (otōshi) is the mandatory table-charge nibble."
    ]
   ],
   [
    "Chopsticks and paying",
    [
     "Never pass food chopstick-to-chopstick (<b>hiroibashi</b> — funeral bone ritual), never spear, never stand them in rice (<b>tatebashi</b>). Lay them on the <b>hashioki</b> rest. Paying: most restaurants are pay-at-the-register (<b>レジ</b>) — staff announce your total; some take trays for cash. Tipping is NOT done — it confuses and can offend. <b>お会計をおねがいします</b> (bill, please)."
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
     "〜をください",
     "…please — the ordering pattern"
    ],
    [
     "いただきます",
     "I humbly receive — before eating"
    ],
    [
     "ごちそうさまでした",
     "thanks for the feast — after eating"
    ],
    [
     "おすすめは何ですか",
     "what do you recommend?"
    ],
    [
     "お会計をおねがいします",
     "bill, please"
    ],
    [
     "おいしいです!",
     "it's delicious!"
    ]
   ]
  ]
 },
 {
  "slug": "masu-verbs",
  "title": "Japanese ます Verbs",
  "desc": "Conjugate the polite present, past and negative, make invitations with ましょう, and say must/have to.",
  "sections": [
   [
    "One stem, four endings",
    [
     "Every polite verb has a ます-stem: drop ます, add endings. <b>食べます</b> (tabemasu — eat): stem 食べ → <b>食べます</b> (eat/will eat), <b>食べました</b> (ate), <b>食べません</b> (don't eat), <b>食べませんでした</b> (didn't eat). <b>飲みます</b> (nomimasu — drink) works identically. Japanese verbs never change for person — 私/あなた/彼 all take the same form."
    ]
   ],
   [
    "The only two rebels",
    [
     "Two verbs conjugate irregularly — and they're the most common: <b>します</b> (shimasu — do) and <b>来ます</b> (kimasu — come). Past: <b>しました・来ました</b> (kimashita). Negative: <b>しません・来ません</b>. します also verbalises nouns: <b>勉強します</b> (study), <b>電話します</b> (phone), <b>結婚します</b> (marry) — learn it once, use it thousandfold."
    ]
   ],
   [
    "Invitations: ましょう",
    [
     "<b>ましょう</b> (mashō) proposes: <b>食べましょう</b> (let's eat), <b>行きましょう</b> (let's go). Question form <b>ましょうか</b> softens: <b>食べましょうか</b> (shall we eat?). Responding yes: <b>いいですね</b> (sounds good); hedging: <b>ちょっと…</b> (a little… — the famous soft no). Plans: <b>明日会いましょう</b> (let's meet tomorrow)."
    ]
   ],
   [
    "Want, like and must",
    [
     "Want (first person): stem + <b>たいです</b> — <b>食べたいです</b> (I want to eat). Like/dislike are な-adjectives: <b>猫が好きです / 嫌いです</b> (I like/dislike cats — note が). Must: plain-negative + <b>なければなりません</b> — <b>行かなければなりません</b> (must go). Casual speech clips it to <b>なきゃ</b>: <b>行かなきゃ</b>."
    ]
   ]
  ],
  "table": [
   [
    "Form",
    "食べます (to eat)"
   ],
   [
    [
     "present/future",
     "食べます"
    ],
    [
     "past",
     "食べました"
    ],
    [
     "negative",
     "食べません"
    ],
    [
     "past negative",
     "食べませんでした"
    ],
    [
     "let's",
     "食べましょう"
    ],
    [
     "want to",
     "食べたいです"
    ]
   ]
  ]
 }
]

PRACTICE = {
 "vocabulary": [
  {"q": "“こんにちは” is used…", "a": "in the daytime", "opts": ["in the morning", "in the daytime", "in the evening", "at night"], "explain": "Konnichiwa — daytime hello (は read wa)."},
  {"q": "“よろしくおねがいします” means…", "a": "please treat me well", "opts": ["thank you", "please treat me well", "goodbye", "excuse me"], "explain": "It closes introductions, handing over the relationship."},
  {"q": "“すみません” does NOT mean…", "a": "goodbye", "opts": ["excuse me", "sorry", "thanks for trouble", "goodbye"], "explain": "Sumimasen covers excuse/sorry/thanks-never goodbye."},
  {"q": "Foreign words are written in…", "a": "katakana", "opts": ["hiragana", "katakana", "kanji", "romaji"], "explain": "Katakana: コーヒー, コンピューター."},
  {"q": "“いただきます” is said…", "a": "before eating", "opts": ["after eating", "before eating", "when paying", "when cooking"], "explain": "Itadakimasu — I humbly receive."},
  {"q": "“ごちそうさまでした” is said…", "a": "after eating", "opts": ["before eating", "after eating", "at the door", "on the phone"], "explain": "Gochisōsama deshita — thanks for the feast."},
  {"q": "Slurping ramen is…", "a": "correct and appreciative", "opts": ["rude", "correct and appreciative", "illegal", "childish"], "explain": "Slurping cools noodles and signals enjoyment."},
  {"q": "“いくらですか” means…", "a": "how much?", "opts": ["what time?", "how much?", "how old?", "where?"], "explain": "Ikura desu ka — how much is it?"},
  {"q": "Tipping in Japan is…", "a": "not done", "opts": ["20% expected", "not done", "10% expected", "required"], "explain": "Tipping confuses and can offend."},
  {"q": "Passing food chopstick-to-chopstick is…", "a": "taboo (funeral-like)", "opts": ["polite", "taboo (funeral-like)", "fun", "normal"], "explain": "Hiroibashi mirrors a funeral bone ritual."},
  {"q": "“おはようございます” is…", "a": "good morning (polite)", "opts": ["good evening", "good morning (polite)", "good night", "welcome"], "explain": "Full polite morning greeting."},
  {"q": "A 45°+ bow signals…", "a": "deep apology", "opts": ["hello", "thanks", "deep apology", "goodbye"], "explain": "Deeper bow, deeper meaning."}
 ],
 "grammar": [
  {"q": "“I am a teacher” is…", "a": "私は先生です", "opts": ["私は先生です", "私が先生です", "私は先生が", "先生私はです"], "explain": "Neutral statement: topic は + です."},
  {"q": "“I am the one who is a student” stresses with…", "a": "私が学生です", "opts": ["私は学生です", "私が学生です", "私も学生です", "私は学生が"], "explain": "が marks the subject emphatically."},
  {"q": "“Read a book” (object) is…", "a": "本を読みます", "opts": ["本を読みます", "本が読みます", "本に読みます", "本で読みます"], "explain": "を marks the direct object."},
  {"q": "“Study at the library” is…", "a": "図書館で勉強します", "opts": ["図書館に勉強します", "図書館で勉強します", "図書館へ勉強します", "図書館を勉強します"], "explain": "で marks where an action happens."},
  {"q": "“There is a cat” is…", "a": "猫がいます", "opts": ["猫があります", "猫がいます", "猫はいます", "猫をいます"], "explain": "Living things take いる."},
  {"q": "“There is a book” is…", "a": "本があります", "opts": ["本がいます", "本があります", "本はあります", "本をあります"], "explain": "Inanimate things take ある."},
  {"q": "“(I) ate” is…", "a": "食べました", "opts": ["食べます", "食べました", "食べません", "食べましょう"], "explain": "ました is the polite past."},
  {"q": "“(I) don't drink” is…", "a": "飲みません", "opts": ["飲みます", "飲みました", "飲みません", "飲みましょう"], "explain": "ません is the polite negative."},
  {"q": "“Let's go” is…", "a": "行きましょう", "opts": ["行きます", "行きました", "行きましょう", "行きたいです"], "explain": "ましょう proposes: let's."},
  {"q": "“I want to eat” is…", "a": "食べたいです", "opts": ["食べます", "食べたいです", "食べましょう", "食べのです"], "explain": "Stem + たいです = want to."},
  {"q": "“Three people” is…", "a": "三人 (さんにん)", "opts": ["三人 (さんにん)", "三人 (みたり)", "三つ人", "人三"], "explain": "Sannin — the counter 人."},
  {"q": "“一本” is read…", "a": "いっぽん", "opts": ["いちほん", "いっぽん", "いちぼん", "いっほん"], "explain": "Euphonic change: ippon."}
 ]
}

QUIZ = [
 {"id": "ja-greet-1", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "“お疲れ様でした” is said…", "a": "to those leaving / after work", "opts": ["on arrival", "to those leaving / after work", "at meals", "on the phone"], "explain": "Otsukaresama — thank you for your work."},
 {"id": "ja-greet-2", "lesson": "greetings-and-introductions", "type": "usage", "topic": "greetings", "level": "beginner", "q": "Answer “いってきます” (I'm off). You say…", "a": "いってらっしゃい", "opts": ["いってらっしゃい", "いってきます", "ただいま", "おかえり again"], "explain": "Itterasshai answers ittekimasu."},
 {"id": "ja-greet-3", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "Business cards are exchanged…", "a": "with both hands, then studied", "opts": ["one-handed", "with both hands, then studied", "by throwing", "never in person"], "explain": "Meishi ritual: both hands, study it."},
 {"id": "ja-greet-4", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "“さようなら” vs “じゃあね”: pick…", "a": "sayōnara is final; jā ne is casual", "opts": ["both casual", "sayōnara is final; jā ne is casual", "both final", "same meaning"], "explain": "Sayōnara carries finality."},
 {"id": "ja-part-1", "lesson": "scripts-and-particles", "type": "vocab", "topic": "particles", "level": "beginner", "q": "In 私はコーヒーを飲みます, コーヒー is in…", "a": "katakana", "opts": ["hiragana", "katakana", "kanji", "romaji"], "explain": "Foreign loanword → katakana."},
 {"id": "ja-part-2", "lesson": "scripts-and-particles", "type": "usage", "topic": "particles", "level": "beginner", "q": "Ask “who is coming?”. You say…", "a": "誰が来ますか", "opts": ["誰が来ますか", "誰は来ますか", "誰を来ますか", "誰に来ますか"], "explain": "New information takes が."},
 {"id": "ja-part-3", "lesson": "scripts-and-particles", "type": "meaning", "topic": "particles", "level": "beginner", "q": "“私も学生です” means…", "a": "I too am a student", "opts": ["I am a student?", "I too am a student", "only I am a student", "I was a student"], "explain": "も = also, replacing は."},
 {"id": "ja-desu-1", "lesson": "desu-aru-iru", "type": "vocab", "topic": "grammar", "level": "beginner", "q": "“Is expensive” (い-adjective) is…", "a": "高いです", "opts": ["高いです", "高です", "高います", "高いだ"], "explain": "Takai desu — い-adjectives keep い."},
 {"id": "ja-desu-2", "lesson": "desu-aru-iru", "type": "usage", "topic": "grammar", "level": "beginner", "q": "Say “I have a car”. You say…", "a": "私は車があります", "opts": ["私は車があります", "私は車がいます", "私は車をです", "車が私あります"], "explain": "Cars are inanimate: ある."},
 {"id": "ja-desu-3", "lesson": "desu-aru-iru", "type": "meaning", "topic": "grammar", "level": "beginner", "q": "“学生でした” means…", "a": "was a student", "opts": ["is a student", "was a student", "will be a student", "is not a student"], "explain": "でした is the polite past."},
 {"id": "ja-num-1", "lesson": "numbers-and-counters", "type": "vocab", "topic": "numbers", "level": "beginner", "q": "4 is usually read よん because し also means…", "a": "death", "opts": ["four things", "death", "west", "dirt"], "explain": "し = death — avoided in counting."},
 {"id": "ja-num-2", "lesson": "numbers-and-counters", "type": "vocab", "topic": "numbers", "level": "beginner", "q": "Flat things (paper, shirts) count with…", "a": "枚 (まい)", "opts": ["本", "枚 (まい)", "匹", "冊"], "explain": "Mai — the flat-thing counter."},
 {"id": "ja-num-3", "lesson": "numbers-and-counters", "type": "usage", "topic": "numbers", "level": "beginner", "q": "20 years old is specially read…", "a": "二十歳 (はたち)", "opts": ["二十歳 (はたち)", "二十歳 (にじゅうさい)", "二十年", "二十才 (はたし)"], "explain": "Hatachi — the famous exception."},
 {"id": "ja-food-1", "lesson": "food-and-ordering", "type": "usage", "topic": "food", "level": "beginner", "q": "Order ramen politely. You say…", "a": "ラーメンをください", "opts": ["ラーメンをください", "ラーメンがください", "ラーメンくださいを", "くださいラーメンを"], "explain": "…o kudasai — the ordering pattern."},
 {"id": "ja-food-2", "lesson": "food-and-ordering", "type": "meaning", "topic": "food", "level": "beginner", "q": "“とりあえずビール!” means…", "a": "for now, beer!", "opts": ["no beer!", "for now, beer!", "beer forever!", "one beer only!"], "explain": "The izakaya opening shout."},
 {"id": "ja-food-3", "lesson": "food-and-ordering", "type": "vocab", "topic": "food", "level": "beginner", "q": "The bill, please — you say…", "a": "お会計をおねがいします", "opts": ["お会計をください", "お会計をおねがいします", "お金ください", "レジはいくら"], "explain": "Okaikei o onegai shimasu."},
 {"id": "ja-verb-1", "lesson": "masu-verbs", "type": "vocab", "topic": "verbs", "level": "beginner", "q": "“しました” is the past of…", "a": "します (do)", "opts": ["きます", "します (do)", "いきます", "みます"], "explain": "Shimashita — did."},
 {"id": "ja-verb-2", "lesson": "masu-verbs", "type": "usage", "topic": "verbs", "level": "beginner", "q": "Propose “shall we eat?”. You say…", "a": "食べましょうか", "opts": ["食べましょうか", "食べますか", "食べたいですか", "食べなさいか"], "explain": "Mashō ka softens the proposal."},
 {"id": "ja-verb-3", "lesson": "masu-verbs", "type": "meaning", "topic": "verbs", "level": "beginner", "q": "“猫が好きです” means…", "a": "I like cats", "opts": ["cats like me", "I like cats", "the cat is here", "cats exist"], "explain": "Suki (liked) with が — I like cats."},
 {"id": "ja-greet-5", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "“お先に失礼します” is said when…", "a": "leaving before others", "opts": ["arriving late", "leaving before others", "entering a shop", "answering mail"], "explain": "Excuse me for leaving first."}
]

REVIEW = [
 {"p": "おはようございます", "a": "good morning"},
 {"p": "こんにちは", "a": "hello (daytime)"},
 {"p": "はじめまして", "a": "how do you do"},
 {"p": "よろしくおねがいします", "a": "please treat me well"},
 {"p": "ありがとうございます", "a": "thank you"},
 {"p": "すみません", "a": "excuse me / sorry"},
 {"p": "私は…です", "a": "I am…"},
 {"p": "は / が", "a": "topic / subject"},
 {"p": "〜をください", "a": "…please (ordering)"},
 {"p": "いただきます", "a": "before eating"},
 {"p": "ごちそうさまでした", "a": "after eating"},
 {"p": "猫がいます", "a": "there is a cat"},
 {"p": "本があります", "a": "there is a book"},
 {"p": "三人 (さんにん)", "a": "three people"},
 {"p": "一本 (いっぽん)", "a": "one long thing"},
 {"p": "二十歳 (はたち)", "a": "20 years old"},
 {"p": "いくらですか", "a": "how much?"},
 {"p": "おすすめは何ですか", "a": "what do you recommend?"},
 {"p": "お会計をおねがいします", "a": "bill, please"},
 {"p": "食べました", "a": "(I) ate"},
 {"p": "飲みません", "a": "(I) don't drink"},
 {"p": "行きましょう", "a": "let's go"},
 {"p": "食べたいです", "a": "I want to eat"},
 {"p": "猫が好きです", "a": "I like cats"}
]

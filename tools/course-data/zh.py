#!/usr/bin/env python3
"""Authored Chinese (Mandarin) course data. Language config + content.
Loaded by tools/build-world-course.py. Do not hand-edit the generated
output pages; edit THIS file and regenerate.
Content is authored by hand, not machine-translated.
Simplified characters, Mainland usage, pinyin with tone marks throughout.
"""

COURSE = {
 "lang": "zh",
 "name": "Chinese",
 "native": "中文",
 "speechTag": "zh-CN",
 "status": "Available",
 "note": "A real, authored Mandarin course: 6 lessons, a practice lab, a topic quiz and a review deck — all running on the same engines as Hindi. It is not yet as deep as the Hindi course, and all audio is your browser's computer voice, never a native recording."
}

LESSONS = [
 {
  "slug": "greetings-and-introductions",
  "title": "Chinese Greetings and Introductions",
  "desc": "Say hello properly, introduce yourself by family name first, and handle thanks and goodbyes — with tones from day one.",
  "sections": [
   [
    "你好 is only the beginning",
    [
     "Everyone knows <b>你好</b> (nǐ hǎo — hello), and it works — but natives greet more concretely: <b>早上好</b> (zǎoshang hǎo — good morning), <b>晚上好</b> (good evening), and the wonderfully direct <b>你吃了吗?</b> (nǐ chī le ma — have you eaten?) — a \"how are you\" that expects no food report. Answer with <b>吃了</b> (chī le — eaten). The respectful \"you\" is <b>您</b> (nín) — use it with elders and clients."
    ]
   ],
   [
    "Names go family-first",
    [
     "Introduce yourself as <b>我叫…</b> (wǒ jiào… — I am called…): <b>我叫拉维</b> (I am called Ravi). Asking: <b>你叫什么名字?</b> (nǐ jiào shénme míngzi?). Crucial: the FAMILY name comes first — <b>王伟</b> is Mr Wáng, not Mr Wěi. Asking someone's surname: <b>您贵姓?</b> (nín guì xìng? — your honourable surname?) Answer: <b>我姓王</b> (wǒ xìng Wáng)."
    ]
   ],
   [
    "How are you, really",
    [
     "<b>你好吗?</b> (nǐ hǎo ma?) is textbook-correct but stiff; friends ask <b>最近怎么样?</b> (zuìjìn zěnmeyàng? — how have you been lately?). The polite reply ladder: <b>很好</b> (very good), <b>还不错</b> (not bad), <b>马马虎虎</b> (so-so — literally \"horse horse tiger tiger\"). Origin: <b>我是印度人</b> (wǒ shì Yìndù rén — I am an Indian), asked as <b>你是哪国人?</b>"
    ]
   ],
   [
    "Thanks and goodbye",
    [
     "<b>谢谢</b> (xièxie) is thanks — doubling is built in; <b>谢谢你</b> adds warmth. The reply is <b>不客气</b> (bú kèqi — don't be polite) or <b>没关系</b>. No direct word for \"please\" exists — <b>请</b> (qǐng) before a verb softens it: <b>请坐</b> (please sit). Goodbye: <b>再见</b> (zàijiàn — again see), or the casual <b>拜拜</b> (bàibai)."
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
     "你好 / 您好",
     "hello — casual / respectful"
    ],
    [
     "早上好 / 晚上好",
     "good morning / good evening"
    ],
    [
     "你吃了吗?",
     "have you eaten? — warm \"how are you\""
    ],
    [
     "我叫…",
     "I am called… — introducing yourself"
    ],
    [
     "谢谢 / 不客气",
     "thanks / you're welcome"
    ],
    [
     "再见",
     "goodbye — see you again"
    ]
   ]
  ]
 },
 {
  "slug": "pinyin-and-tones",
  "title": "Pinyin and the Four Tones",
  "desc": "Read romanised Chinese, nail the four tones plus neutral tone, and learn why mā and mà are different words.",
  "sections": [
   [
    "Pinyin is training wheels, not the bike",
    [
     "<b>拼音</b> (pīnyīn) spells Chinese sounds in the Latin alphabet: <b>hǎo</b> = h+ao+third tone. It is the standard input method and dictionary system — genuinely useful. But it is NOT the language: real text is characters, and pinyin omits them, so treat it as scaffolding you read fluently while characters catch up. Every lesson here pairs characters with pinyin."
    ]
   ],
   [
    "Four tones, one neutral",
    [
     "Mandarin has four main tones: <b>first</b> (mā — high flat), <b>second</b> (má — rising), <b>third</b> (mǎ — dipping), <b>fourth</b> (mà — falling), plus a light <b>neutral</b> tone (ma). Same syllable, different tone, different word: <b>mā (妈 mother), má (麻 hemp), mǎ (马 horse), mà (骂 scold)</b>. Tones are not decoration — māma vs màma is mother vs scolding."
    ]
   ],
   [
    "The sounds that trip learners",
    [
     "Three pinyin traps: <b>j/q/x</b> are NOT English j/ch/sh — smile wide, tongue forward: <b>xièxie</b> is closer to \"shyeh-shyeh\" with spread lips. <b>zh/ch/sh</b> curl the tongue back; <b>z/c/s</b> keep it behind the teeth: <b>zì</b> (character) vs <b>zhī</b> differ only in tongue curl. And <b>ü</b> (as in <b>绿 lǜ</b>) rounds lips for \"oo\" while saying \"ee\"."
    ]
   ],
   [
    "Tone change rules",
    [
     "Tones shift in company. The big two: <b>third-tone sandhi</b> — two third tones in a row turn the FIRST into a second: <b>你好</b> is written nǐ hǎo but said ní hǎo. And <b>不 (bù)</b> turns second tone before a fourth: <b>不对</b> is bú duì, not bù duì. Don't panic — internalise the written tones first; sandhi becomes automatic with listening."
    ]
   ]
  ],
  "table": [
   [
    "Tone",
    "Example"
   ],
   [
    [
     "1st — high flat",
     "mā 妈 — mother"
    ],
    [
     "2nd — rising",
     "má 麻 — hemp"
    ],
    [
     "3rd — dipping",
     "mǎ 马 — horse"
    ],
    [
     "4th — falling",
     "mà 骂 — to scold"
    ],
    [
     "neutral — light",
     "ma 吗 — question particle"
    ],
    [
     "sandhi",
     "你好 said ní hǎo"
    ]
   ]
  ]
 },
 {
  "slug": "shi-you-and-zai",
  "title": "是, 有 and 在 — The Three Workhorses",
  "desc": "Chinese has no single \"to be\": identity takes 是, existence takes 有, location takes 在. Learn the split once, use it forever.",
  "sections": [
   [
    "是 (shì) — identity only",
    [
     "<b>我是学生</b> (wǒ shì xuéshēng — I am a student): 是 links a subject to its identity — a noun. It does NOT link adjectives: \"I am tired\" is <b>我很累</b> (wǒ hěn lèi — I very tired) with NO 是 — adjectives act as verbs in Chinese. Negation: <b>我不是老师</b> (I am not a teacher). Rule: noun after? Use 是. Adjective after? Skip it."
    ]
   ],
   [
    "有 (yǒu) — existence and having",
    [
     "<b>我有一本书</b> (wǒ yǒu yì běn shū — I have a book) and <b>这里有人</b> (zhèlǐ yǒu rén — here there are people): 有 covers both \"have\" and \"there is\". It negates with <b>没</b>, never 不: <b>我没有钱</b> (I have no money), <b>没有人</b> (there is nobody). Note 没 also negates past actions — one particle, wide duties."
    ]
   ],
   [
    "在 (zài) — location",
    [
     "<b>我在家</b> (wǒ zài jiā — I am at home): location needs 在, never 是. It doubles as \"at/in\" before places: <b>他在学校</b> (he is at school). Yes/no question: just add <b>吗</b>: <b>你在家吗?</b> (are you at home?). Negation: <b>我不在家</b> (I am not at home)."
    ]
   ],
   [
    "Putting the three together",
    [
     "Test yourself: \"She is a doctor\" → <b>她是医生</b> (identity). \"There is a doctor here\" → <b>这里有医生</b> (existence). \"The doctor is here\" → <b>医生在这里</b> (location). Three sentences, three different \"is\"-words — and now you see why Chinese has no verb \"to be\". This one lesson prevents years of 是-everywhere errors."
    ]
   ]
  ],
  "table": [
   [
    "Word",
    "Use and example"
   ],
   [
    [
     "是 (shì)",
     "identity — 我是学生 (I am a student)"
    ],
    [
     "有 (yǒu)",
     "have / there is — 我有一本书"
    ],
    [
     "在 (zài)",
     "location — 我在家 (I am home)"
    ],
    [
     "不是",
     "is not (identity) — 我不是老师"
    ],
    [
     "没有",
     "don't have / there isn't — 没有人"
    ],
    [
     "adjectives",
     "need no 是 — 我很累 (I am tired)"
    ]
   ]
  ]
 },
 {
  "slug": "numbers-and-measure-words",
  "title": "Chinese Numbers and Measure Words",
  "desc": "Count to 99 with a beautifully logical system, say your age, tell the time — and meet 两 and the measure words.",
  "sections": [
   [
    "One to ten, then logic",
    [
     "<b>一 二 三 四 五 六 七 八 九 十</b> (yī èr sān sì wǔ liù qī bā jiǔ shí). Then pure logic: 11 is <b>十一</b> (ten-one), 12 <b>十二</b> (ten-two), 20 <b>二十</b> (two-ten), 21 <b>二十一</b> (two-ten-one), 99 <b>九十九</b>. No \"eleven/twelve/twenty\" irregularities — if you can say 1–10, you can say 1–99. Hundred is <b>百</b> (bǎi): 200 = <b>两百</b>."
    ]
   ],
   [
    "两 (liǎng) vs 二 (èr)",
    [
     "Counting abstract numbers: <b>一, 二, 三</b>. Counting THINGS: <b>两</b> replaces èr — <b>两个人</b> (two people), <b>两本书</b> (two books), never 二个人. 两 also means \"a couple of\" loosely. Phone numbers, floors and maths keep 二. One extra word — but natives notice instantly when it's wrong, so drill it early."
    ]
   ],
   [
    "Measure words: every noun needs one",
    [
     "You cannot say \"three book\" — Chinese needs a <b>量词</b> (measure word) between number and noun: <b>三本书</b> (three-volumes book), <b>两个人</b> (two-people person), <b>一杯茶</b> (one-cup tea). The universal fallback is <b>个</b> (ge): <b>三个苹果</b> (three apples). Wrong measure word? 个 saves you — natives may smile, but they'll understand."
    ]
   ],
   [
    "Age, time and money",
    [
     "Age: <b>我二十岁</b> (wǒ èrshí suì — I am 20), asked as <b>你多大了?</b> Time: <b>三点</b> (sān diǎn — 3 o'clock), <b>三点半</b> (half past three). Money: <b>块</b> (kuài — yuan, spoken) — <b>多少钱?</b> (duōshao qián? — how much?) is the market essential. Bargaining opens with <b>太贵了!</b> (tài guì le — too expensive!)."
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
     "1–10",
     "一二三四五六七八九十"
    ],
    [
     "11 / 20 / 99",
     "十一 / 二十 / 九十九"
    ],
    [
     "两 for things",
     "两个人 — two people"
    ],
    [
     "measure word",
     "三本书 — three books"
    ],
    [
     "I am 20",
     "我二十岁"
    ],
    [
     "How much?",
     "多少钱?"
    ]
   ]
  ]
 },
 {
  "slug": "food-and-ordering",
  "title": "Chinese Food and Ordering",
  "desc": "Survive and thrive at any Chinese table: ordering, chopstick rules, tea etiquette and paying the bill.",
  "sections": [
   [
    "Ordering like a local",
    [
     "Get attention: <b>服务员!</b> (fúwùyuán! — waiter!). Order with <b>我要…</b> (wǒ yào… — I want…): <b>我要一碗米饭</b> (one bowl of rice, please). Ask for the menu: <b>菜单, 谢谢</b>. \"Is it spicy?\" — <b>辣吗?</b> (là ma?) — matters in Sichuan. Vegetarian: <b>我是素食者</b> (wǒ shì sùshízhě). Pointing at a neighbour's dish plus <b>这个</b> (zhège — this one) never fails."
    ]
   ],
   [
    "At the table",
    [
     "Dishes land in the CENTRE for sharing — order one dish per person plus one extra. Rice (<b>米饭</b>) is individual; noodles (<b>面条</b>) are long life — never cut birthday noodles. Hosts serve you the best pieces; protesting lightly (<b>够了够了</b> — enough!) is polite ritual. Tea: tap two fingers on the table to thank the pourer silently."
    ]
   ],
   [
    "Chopstick rules",
    [
     "Three taboos: never stick chopsticks UPRIGHT in rice (funeral incense — deeply ominous); never point with them; never spear food. Rest them on the bowl edge or the stand. Struggling is fine — asking for a fork (<b>叉子</b>) is unremarkable in cities. But practise: competence with <b>筷子</b> (kuàizi) earns genuine respect."
    ]
   ],
   [
    "Paying and praising",
    [
     "The bill: <b>买单</b> (mǎidān). Expect a theatrical fight to pay — hosts nearly always win; guests contribute by inviting next time. Tipping is NOT customary on the Mainland (refuse politely if change is returned). Praise: <b>很好吃!</b> (hěn hǎochī — very delicious!). Full: <b>我吃饱了</b> (I have eaten to fullness)."
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
     "我要…",
     "I want… — the ordering phrase"
    ],
    [
     "这个",
     "this one — the pointer's friend"
    ],
    [
     "辣吗?",
     "is it spicy?"
    ],
    [
     "很好吃!",
     "very delicious!"
    ],
    [
     "我吃饱了",
     "I am full (eaten to fullness)"
    ],
    [
     "买单",
     "the bill, please"
    ]
   ]
  ]
 },
 {
  "slug": "basic-sentences",
  "title": "Chinese Basic Sentences",
  "desc": "Word order with time and place, the 把-free beginner patterns, 了 for completion, and saying no with 不 and 没.",
  "sections": [
   [
    "Time and place come first",
    [
     "English: \"I go to school at 8.\" Chinese: <b>我八点去学校</b> (I 8-o'clock go school) — TIME slots right after the subject, before the verb. Place words behave the same: <b>我在家吃饭</b> (I at-home eat). The frame is <b>subject + time + place + verb + object</b> — drill this order until it feels inevitable, because every sentence uses it."
    ]
   ],
   [
    "了 (le) — completion, not past tense",
    [
     "Chinese verbs never conjugate — <b>吃</b> is eat/eats/ate depending on context. Completion is marked with <b>了</b>: <b>我吃了</b> (I have eaten / I ate). New situations also take 了: <b>下雨了</b> (it's raining now — wasn't before). Don't equate 了 with English past tense — <b>我昨天去商店</b> (yesterday I go shop) needs no 了; the time word does the work."
    ]
   ],
   [
    "Saying no: 不 vs 没",
    [
     "Two negators split by time: <b>不</b> (bù) for present/future and habits — <b>我不吃肉</b> (I don't eat meat), <b>我明天不去</b> (I'm not going tomorrow). <b>没</b> (méi) for completed past — <b>我昨天没去</b> (I didn't go yesterday). The exception: 有 always negates with 没 (<b>没有</b>), even in the present. This single distinction fixes most beginner errors."
    ]
   ],
   [
    "Questions without rearranging",
    [
     "Yes/no: add <b>吗</b> — <b>你是中国人吗?</b> (are you Chinese?). Choice: <b>是不是 / 有没有</b> — <b>你是不是老师?</b>, <b>你有没有钱?</b> Wh-words stay IN PLACE: <b>你在哪儿工作?</b> (you where work? — where do you work?), never \"where do you work\" order. <b>什么</b> (what), <b>谁</b> (who), <b>哪儿</b> (where), <b>为什么</b> (why), <b>怎么</b> (how)."
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
     "word order",
     "我八点去学校 — I go at 8"
    ],
    [
     "了 (completion)",
     "我吃了 — I have eaten"
    ],
    [
     "不 (present no)",
     "我不吃肉 — I don't eat meat"
    ],
    [
     "没 (past no)",
     "我昨天没去 — I didn't go"
    ],
    [
     "吗 (yes/no ?)",
     "你是老师吗? — are you a teacher?"
    ],
    [
     "wh in place",
     "你在哪儿工作? — where do you work?"
    ]
   ]
  ]
 }
]

PRACTICE = {
 "vocabulary": [
  {"q": "What does “你好” mean?", "a": "hello", "opts": ["thanks", "hello", "goodbye", "sorry"], "explain": "Nǐ hǎo — hello (said ní hǎo by sandhi)."},
  {"q": "“谢谢” means…", "a": "thanks", "opts": ["please", "thanks", "sorry", "hello"], "explain": "Xièxie — thanks; answered with 不客气."},
  {"q": "The reply to 谢谢 is…", "a": "不客气", "opts": ["不客气", "没关系", "再见", "谢谢"], "explain": "Bú kèqi — don't be polite."},
  {"q": "In 王伟, the family name is…", "a": "王 (first)", "opts": ["伟", "王 (first)", "王伟 together", "neither"], "explain": "Family name comes first: Mr Wáng."},
  {"q": "“mǎ” (3rd tone) means…", "a": "horse", "opts": ["mother", "hemp", "horse", "scold"], "explain": "mā mother, má hemp, mǎ horse, mà scold."},
  {"q": "你好 is actually pronounced…", "a": "ní hǎo", "opts": ["nǐ hǎo", "ní hǎo", "nì hào", "nī hāo"], "explain": "Third-tone sandhi: first becomes 2nd."},
  {"q": "“多少钱?” means…", "a": "how much?", "opts": ["what time?", "how much?", "how old?", "how many?"], "explain": "Duōshao qián? — the market essential."},
  {"q": "“很好吃!” means…", "a": "very delicious!", "opts": ["very big!", "very hot!", "very delicious!", "very full!"], "explain": "Hěn hǎochī! praises the food."},
  {"q": "“买单” means…", "a": "the bill, please", "opts": ["the menu", "the bill, please", "one more", "takeaway"], "explain": "Mǎidān asks for the bill."},
  {"q": "“我吃饱了” means…", "a": "I am full", "opts": ["I am hungry", "I am full", "I am thirsty", "I am tired"], "explain": "Eaten to fullness."},
  {"q": "“不” before a 4th tone is said…", "a": "bú", "opts": ["bù", "bú", "bǔ", "bū"], "explain": "不对 is bú duì — tone change."},
  {"q": "Sticking chopsticks upright in rice is…", "a": "taboo (funeral-like)", "opts": ["lucky", "taboo (funeral-like)", "polite", "normal"], "explain": "It mirrors funeral incense — never do it."}
 ],
 "grammar": [
  {"q": "“I am a student” is…", "a": "我是学生", "opts": ["我在学生", "我是学生", "我有学生", "我学生"], "explain": "Identity uses 是: wǒ shì xuéshēng."},
  {"q": "“I am tired” is…", "a": "我很累", "opts": ["我是累", "我很累", "我在累", "我有累"], "explain": "Adjectives need no 是: wǒ hěn lèi."},
  {"q": "“I have a book” is…", "a": "我有一本书", "opts": ["我是书", "我有一本书", "我在书", "我书有"], "explain": "Having uses 有 + measure word: yì běn shū."},
  {"q": "“I am at home” is…", "a": "我在家", "opts": ["我是家", "我在家", "我有家", "家我"], "explain": "Location uses 在: wǒ zài jiā."},
  {"q": "“Two people” is…", "a": "两个人", "opts": ["二个人", "两个人", "两人们", "二人们"], "explain": "Things counted with 两: liǎng ge rén."},
  {"q": "“Three books” is…", "a": "三本书", "opts": ["三书", "三本书", "三本的书", "三个书"], "explain": "本 is the measure word for books."},
  {"q": "“I am 20” is…", "a": "我二十岁", "opts": ["我二十年", "我二十岁", "我是二十", "我有二十"], "explain": "Wǒ èrshí suì — 岁 for age."},
  {"q": "“I go to school at 8” is…", "a": "我八点去学校", "opts": ["我去学校八点", "我八点去学校", "八点我去学校去", "我去八点学校"], "explain": "Time slots after the subject."},
  {"q": "“I don't eat meat” is…", "a": "我不吃肉", "opts": ["我不吃肉", "我没吃肉", "我不是吃肉", "我没有吃肉"], "explain": "Habits negate with 不."},
  {"q": "“I didn't go yesterday” is…", "a": "我昨天没去", "opts": ["我昨天不去", "我昨天没去", "我没昨天去", "昨天我不去"], "explain": "Completed past negates with 没."},
  {"q": "“Where do you work?” is…", "a": "你在哪儿工作?", "opts": ["你在哪儿工作?", "在哪儿你工作?", "你工作在哪儿吗?", "哪儿工作你?"], "explain": "Wh-words stay in place."},
  {"q": "“Are you a teacher?” (choice) is…", "a": "你是不是老师?", "opts": ["你是老师吗?", "你是不是老师?", "你老师是不是?", "是不是你老师?"], "explain": "The 是不是 choice pattern; 吗 also works."}
 ]
}

QUIZ = [
 {"id": "zh-greet-1", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "“你吃了吗?” is used as…", "a": "a warm \"how are you\"", "opts": ["a dinner invitation", "a warm \"how are you\"", "a complaint", "a goodbye"], "explain": "Have-you-eaten = how are you."},
 {"id": "zh-greet-2", "lesson": "greetings-and-introductions", "type": "usage", "topic": "greetings", "level": "beginner", "q": "Introduce yourself as Ravi. You say…", "a": "我叫拉维", "opts": ["我叫拉维", "我是叫拉维", "我名字拉维", "叫我拉维是"], "explain": "Wǒ jiào… — I am called…"},
 {"id": "zh-greet-3", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "“您” (nín) is…", "a": "respectful \"you\"", "opts": ["plural you", "respectful \"you\"", "casual you", "\"they\""], "explain": "Nín honours elders and clients."},
 {"id": "zh-greet-4", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "“再见” literally means…", "a": "again see", "opts": ["go well", "again see", "stay safe", "long life"], "explain": "Zàijiàn — see you again."},
 {"id": "zh-pin-1", "lesson": "pinyin-and-tones", "type": "vocab", "topic": "tones", "level": "beginner", "q": "“mà” (4th tone) means…", "a": "to scold", "opts": ["mother", "horse", "hemp", "to scold"], "explain": "Mà — to scold; mā is mother."},
 {"id": "zh-pin-2", "lesson": "pinyin-and-tones", "type": "vocab", "topic": "tones", "level": "beginner", "q": "Pinyin is best described as…", "a": "romanisation scaffolding", "opts": ["the real script", "romanisation scaffolding", "a dialect", "handwriting"], "explain": "Training wheels; characters are the bike."},
 {"id": "zh-pin-3", "lesson": "pinyin-and-tones", "type": "meaning", "topic": "tones", "level": "beginner", "q": "“不对” is pronounced…", "a": "bú duì", "opts": ["bù duì", "bú duì", "bǔ duǐ", "bū duī"], "explain": "不 turns 2nd before a 4th tone."},
 {"id": "zh-shi-1", "lesson": "shi-you-and-zai", "type": "vocab", "topic": "grammar", "level": "beginner", "q": "“There is nobody” is…", "a": "没有人", "opts": ["沒有人", "没有人", "不有人", "没是人"], "explain": "Méiyǒu rén (simplified 没有人)."},
 {"id": "zh-shi-2", "lesson": "shi-you-and-zai", "type": "usage", "topic": "grammar", "level": "beginner", "q": "Say “the doctor is here” (location). You say…", "a": "医生在这里", "opts": ["医生在这里", "医生是有这里", "这里是医生在", "医生是有这里"], "explain": "Location → 在: 医生在这里."},
 {"id": "zh-shi-3", "lesson": "shi-you-and-zai", "type": "meaning", "topic": "grammar", "level": "beginner", "q": "“我不是老师” means…", "a": "I am not a teacher", "opts": ["I am a teacher", "I have no teacher", "I am not a teacher", "I was a teacher"], "explain": "Bú shì negates identity."},
 {"id": "zh-num-1", "lesson": "numbers-and-measure-words", "type": "vocab", "topic": "numbers", "level": "beginner", "q": "“九十九” is the number…", "a": "99", "opts": ["90", "99", "919", "999"], "explain": "Nine-ten-nine = 99."},
 {"id": "zh-num-2", "lesson": "numbers-and-measure-words", "type": "vocab", "topic": "numbers", "level": "beginner", "q": "The universal fallback measure word is…", "a": "个", "opts": ["本", "个", "杯", "只"], "explain": "个 (ge) rescues every noun."},
 {"id": "zh-num-3", "lesson": "numbers-and-measure-words", "type": "usage", "topic": "numbers", "level": "beginner", "q": "Phone numbers and maths use…", "a": "二 (èr)", "opts": ["两", "二 (èr)", "俩", "双"], "explain": "Abstract counting keeps èr."},
 {"id": "zh-food-1", "lesson": "food-and-ordering", "type": "usage", "topic": "food", "level": "beginner", "q": "Get the waiter's attention. You call…", "a": "服务员!", "opts": ["服务员!", "老板!", "朋友!", "师傅!"], "explain": "Fúwùyuán! — waiter!"},
 {"id": "zh-food-2", "lesson": "food-and-ordering", "type": "vocab", "topic": "food", "level": "beginner", "q": "Chopsticks are…", "a": "筷子", "opts": ["叉子", "筷子", "勺子", "刀子"], "explain": "Kuàizi; 叉子 is a fork."},
 {"id": "zh-food-3", "lesson": "food-and-ordering", "type": "meaning", "topic": "food", "level": "beginner", "q": "Tipping on the Mainland is…", "a": "not customary", "opts": ["20% expected", "not customary", "10% expected", "required"], "explain": "No tipping culture on the Mainland."},
 {"id": "zh-sen-1", "lesson": "basic-sentences", "type": "vocab", "topic": "grammar", "level": "beginner", "q": "了 (le) marks…", "a": "completion / new situation", "opts": ["past tense always", "completion / new situation", "future", "politeness"], "explain": "Completion, not past tense."},
 {"id": "zh-sen-2", "lesson": "basic-sentences", "type": "usage", "topic": "grammar", "level": "beginner", "q": "Say “I eat at home” (place first). You say…", "a": "我在家吃饭", "opts": ["我在家吃饭", "我吃饭在家", "在家我吃饭", "我吃在家饭"], "explain": "Place slots before the verb."},
 {"id": "zh-sen-3", "lesson": "basic-sentences", "type": "meaning", "topic": "grammar", "level": "beginner", "q": "有 always negates with…", "a": "没", "opts": ["不", "没", "别", "莫"], "explain": "没有 — even in the present."},
 {"id": "zh-greet-5", "lesson": "greetings-and-introductions", "type": "usage", "topic": "greetings", "level": "beginner", "q": "Ask someone's surname politely. You say…", "a": "您贵姓?", "opts": ["你叫什么?", "您贵姓?", "你姓什么名字?", "贵姓你什么?"], "explain": "Nín guì xìng? — your honourable surname?"}
]

REVIEW = [
 {"p": "你好", "a": "hello (nǐ hǎo → ní hǎo)"},
 {"p": "早上好", "a": "good morning"},
 {"p": "谢谢", "a": "thanks"},
 {"p": "不客气", "a": "you're welcome"},
 {"p": "再见", "a": "goodbye"},
 {"p": "我叫…", "a": "I am called…"},
 {"p": "我是印度人", "a": "I am an Indian"},
 {"p": "mā / má / mǎ / mà", "a": "mother / hemp / horse / scold"},
 {"p": "我是学生", "a": "I am a student"},
 {"p": "我很累", "a": "I am tired"},
 {"p": "我有一本书", "a": "I have a book"},
 {"p": "我在家", "a": "I am at home"},
 {"p": "一…十", "a": "1–10 (…shí)"},
 {"p": "二十一", "a": "21 (two-ten-one)"},
 {"p": "两个人", "a": "two people (liǎng!)"},
 {"p": "三本书", "a": "three books"},
 {"p": "我二十岁", "a": "I am 20 years old"},
 {"p": "多少钱?", "a": "how much?"},
 {"p": "我要…", "a": "I want… (ordering)"},
 {"p": "很好吃!", "a": "very delicious!"},
 {"p": "我吃饱了", "a": "I am full"},
 {"p": "买单", "a": "the bill, please"},
 {"p": "我不吃肉", "a": "I don't eat meat"},
 {"p": "你在哪儿工作?", "a": "where do you work?"}
]

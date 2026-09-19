#!/usr/bin/env python3
"""Authored Korean course data. Language config + content.
Loaded by tools/build-world-course.py. Do not hand-edit the generated
output pages; edit THIS file and regenerate.
Content is authored by hand, not machine-translated.
Polite 요 style throughout; romanisation alongside hangul.
"""

COURSE = {
 "lang": "ko",
 "name": "Korean",
 "native": "한국어",
 "speechTag": "ko-KR",
 "status": "Available",
 "note": "A real, authored Korean course: 6 lessons, a practice lab, a topic quiz and a review deck — all running on the same engines as Hindi. It is not yet as deep as the Hindi course, and all audio is your browser's computer voice, never a native recording."
}

LESSONS = [
 {
  "slug": "greetings-and-introductions",
  "title": "Korean Greetings and Introductions",
  "desc": "Say 안녕하세요 properly, introduce yourself, bow and exchange with two hands — with 입니다 from the first lesson.",
  "sections": [
   [
    "안녕하세요 — are you at peace?",
    [
     "<b>안녕하세요</b> (annyeonghaseyo) literally asks \"are you at peace?\" — it serves morning, noon and night. The casual <b>안녕</b> (annyeong) is for friends and juniors ONLY; using it to a stranger insults. On the phone: <b>여보세요</b> (yeoboseyo). Leaving: <b>안녕히 가세요</b> (go in peace — said by the stayer) vs <b>안녕히 계세요</b> (stay in peace — said by the leaver). Mix them and natives laugh kindly."
    ]
   ],
   [
    "Introducing yourself",
    [
     "The template: <b>안녕하세요. 저는 라비입니다. 인도에서 왔습니다. 만나서 반갑습니다.</b> (I am Ravi. I came from India. Pleased to meet you.) <b>저는…입니다</b> (jeoneun…imnida) is the humble-polite \"I am\" — 저 humbles the self, 입니다 elevates the sentence. Family name first: <b>김민준</b> is Mr Kim. Asking names: <b>성함이 어떻게 되세요?</b> (honorific — what is your name?)."
    ]
   ],
   [
    "Bowing and two hands",
    [
     "Greet with a short bow from the waist — nodding alone reads as curt. Give and receive EVERYTHING (cards, money, gifts) with two hands, or the right hand supported by the left. Business cards are received, studied aloud, and placed on the table — never written on or pocketed mid-meeting. Pouring drinks: two hands for elders, always; receive with two hands and turn aside to sip."
    ]
   ],
   [
    "Thanks, sorry and goodbye",
    [
     "<b>감사합니다</b> (gamsahamnida) is full thanks; <b>고마워요</b> is its warm younger sibling. Sorry: <b>죄송합니다</b> (formal) / <b>미안해요</b> (soft). Excuse me: <b>저기요 / 실례합니다</b>. Goodbye splits by who leaves: stayer says <b>안녕히 가세요</b>, leaver says <b>안녕히 계세요</b>. At night add <b>안녕히 주무세요</b> (sleep in peace)."
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
     "안녕하세요",
     "hello — any hour, any stranger"
    ],
    [
     "저는…입니다",
     "I am… — humble-polite self-intro"
    ],
    [
     "만나서 반갑습니다",
     "pleased to meet you"
    ],
    [
     "안녕히 가세요 / 계세요",
     "goodbye — said by stayer / leaver"
    ],
    [
     "감사합니다",
     "thank you — full form"
    ],
    [
     "죄송합니다",
     "I am sorry — formal"
    ]
   ]
  ]
 },
 {
  "slug": "hangul-and-particles",
  "title": "Hangul and Particles",
  "desc": "Read Korea's scientific alphabet in a weekend, then master 은/는 vs 이/가 and 을/를・에/에서.",
  "sections": [
   [
    "The world's most scientific alphabet",
    [
     "<b>한글</b> (hangeul) was DESIGNED in 1443 by King Sejong's scholars — consonant shapes mimic the mouth making them (ㄱ is the tongue blocking the throat). 14 consonants + 10 vowels stack into syllable blocks: <b>한</b> = ㅎ+ㅏ+ㄴ. It is fully phonetic — learn the 24 letters in a weekend and you can sound out every sign in Seoul. Literacy in Korea is near 100%, and hangul is why."
    ]
   ],
   [
    "Letters that change their sound",
    [
     "Four quirks to learn early: <b>ㅇ</b> is silent at a syllable's start (<b>아</b> = a) but \"ng\" at the end (<b>강</b> = gang). Plain stops voice between vowels: <b>가방</b> sounds like \"gabang\". Double consonants (<b>ㄲ ㄸ ㅃ ㅆ ㅉ</b>) are tense and clipped: <b>딸</b> (ttal — daughter) vs <b>탈</b> (tal — mask). And final consonants neutralise: <b>빛</b> (light) ends in an unreleased \"t\"."
    ]
   ],
   [
    "은/는 vs 이/가",
    [
     "Like Japanese: <b>은/는</b> (eun/neun) marks the TOPIC, <b>이/가</b> (i/ga) the SUBJECT. <b>저는 학생입니다</b> (as for me — student): neutral. <b>제가 학생입니다</b> (I am the one): emphasis. Vowel-ending nouns take 는/가 (<b>저는, 제가</b>), consonant-ending take 은/이 (<b>민준은, 민준이</b>). Question \"who?\" answers with 가: <b>누가 와요?</b> — <b>제가 와요</b>."
    ]
   ],
   [
    "을/를・에/에서・도",
    [
     "<b>을/를</b> marks the object: <b>책을 읽어요</b> (read a book). <b>에</b> marks destination/time: <b>학교에 가요</b> (go to school), <b>8시에</b> (at 8). <b>에서</b> marks where action happens: <b>도서관에서 공부해요</b> (study at the library). <b>도</b> means also: <b>저도 학생이에요</b> (I too am a student). Questions need no か — intonation rises: <b>학생이에요?</b>"
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
     "은/는",
     "topic — 저는 학생입니다"
    ],
    [
     "이/가",
     "subject — 제가 학생입니다"
    ],
    [
     "을/를",
     "object — 책을 읽어요"
    ],
    [
     "에",
     "destination/time — 학교에 가요"
    ],
    [
     "에서",
     "place of action — 도서관에서 공부해요"
    ],
    [
     "도",
     "also — 저도 학생이에요"
    ]
   ]
  ]
 },
 {
  "slug": "ida-and-isseoyo",
  "title": "이다 and 있어요 — To Be in Korean",
  "desc": "Identity with 입니다/이에요, existence with 있어요/없어요, possession, and negation with 안 and 못.",
  "sections": [
   [
    "입니다 vs 이에요",
    [
     "Identity has two polite gears: formal <b>입니다</b> (imnida — presentations, announcements) and everyday-polite <b>이에요/예요</b> (ieyo/yeyo — conversation). Consonant-ending nouns take 이에요 (<b>학생이에요</b>), vowel-ending take 예요 (<b>의사예요</b> — is a doctor). Negative: <b>이/가 아닙니다</b> (<b>학생이 아닙니다</b> — is not a student). Beginners: live in 이에요 — it fits nearly every conversation."
    ]
   ],
   [
    "있어요 / 없어요 — existence",
    [
     "<b>있어요</b> (isseoyo) means exists/have; <b>없어요</b> (eopseoyo) is its built-in negative: <b>고양이가 있어요</b> (there is a cat), <b>시간이 없어요</b> (there is no time). Possession: <b>저는 차가 있어요</b> (I have a car). Location: <b>책이 책상 위에 있어요</b> (the book is on the desk). Asking \"do you have?\": <b>…있어요?</b> — one word carries the whole question."
    ]
   ],
   [
    "Negation: 안 vs 못",
    [
     "Two short negators split by CAN'T vs WON'T: <b>안</b> (an) for won't/don't — <b>안 먹어요</b> (I don't eat / won't eat). <b>못</b> (mot) for can't — <b>못 먹어요</b> (I can't eat it — allergy, diet, fullness). Both slot before the verb. Long-form equivalents (<b>먹지 않아요/못해요</b>) sound more formal. Mixing them up changes won't into can't — a meaningful difference."
    ]
   ],
   [
    "Adjectives act like verbs",
    [
     "Korean adjectives conjugate like verbs: <b>좋아요</b> (is good), <b>좋았어요</b> (was good), <b>안 좋아요</b> (isn't good). <b>크다</b> (big) → <b>커요</b>; <b>작다</b> (small) → <b>작아요</b>. Attributive form adds ㄴ/는: <b>좋은 책</b> (a good book), <b>큰 집</b> (a big house). Past recollection: <b>맛있었어요!</b> (it WAS delicious — said after the meal)."
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
     "입니다 (formal)",
     "저는 학생입니다 — I am a student"
    ],
    [
     "이에요/예요 (daily)",
     "의사예요 — is a doctor"
    ],
    [
     "있어요 / 없어요",
     "고양이가 있어요 — there is a cat"
    ],
    [
     "possession",
     "저는 차가 있어요 — I have a car"
    ],
    [
     "안 (won't)",
     "안 먹어요 — I don't eat"
    ],
    [
     "못 (can't)",
     "못 먹어요 — I can't eat"
    ]
   ]
  ]
 },
 {
  "slug": "two-number-systems",
  "title": "Two Number Systems",
  "desc": "Sino-Korean for money and time, native Korean for people and things — plus counters and the 한・두・세 change.",
  "sections": [
   [
    "Sino-Korean: 일, 이, 삼…",
    [
     "For money, dates, minutes, phone numbers: <b>일 이 삼 사 오 육 칠 팔 구 십</b> (il i sam sa o yuk chil pal gu sip). Then logic like Chinese: <b>십일</b> (11), <b>이십</b> (20), <b>구십구</b> (99), <b>백</b> (100), <b>천</b> (1,000), <b>만</b> (10,000 — Korea counts in ten-thousands!). Prices: <b>오천 원</b> (5,000 won). Time-minutes: <b>3시 15분</b> (samsi sibobun)."
    ]
   ],
   [
    "Native Korean: 하나, 둘, 셋…",
    [
     "For people, things, hours, age: <b>하나 둘 셋 넷 다섯 여섯 일곱 여덟 아홉 열</b>. 11–19 compound: <b>열하나</b> (11), <b>열둘</b> (12); 20+ has special words (<b>스물, 서른, 마흔…</b>). Hours use native (<b>3시</b> = 세 시), minutes use Sino (<b>15분</b>) — \"3:15\" mixes BOTH systems in one breath. Age: <b>스무 살</b> (20 years old)."
    ]
   ],
   [
    "Counters and the 한・두・세 change",
    [
     "Before counters, native numbers shorten: <b>하나→한, 둘→두, 셋→세, 넷→네, 스물→스무</b>. <b>세 명</b> (three people), <b>두 개</b> (two things), <b>한 잔</b> (one glass). Counters: <b>명</b> (people), <b>개</b> (things), <b>잔</b> (cups), <b>병</b> (bottles), <b>마리</b> (animals), <b>권</b> (books). 개 is the universal rescue counter."
    ]
   ],
   [
    "Money, time and age",
    [
     "Money: <b>얼마예요?</b> (how much?) — answer in Sino + <b>원</b> (won). O'clock: native + <b>시</b> (<b>세 시</b> — 3 o'clock); half: <b>반</b> (<b>세 시 반</b>). Age: native + <b>살</b> (<b>스무 살</b>). Asking age is normal among new acquaintances (it sets speech levels!): <b>나이가 어떻게 되세요?</b> — answer proudly."
    ]
   ]
  ],
  "table": [
   [
    "System",
    "Used for"
   ],
   [
    [
     "Sino (일, 이, 삼…)",
     "money, minutes, dates — 오천 원"
    ],
    [
     "native (하나, 둘, 셋…)",
     "people, things, hours, age — 세 시"
    ],
    [
     "3:15",
     "세 시 십오 분 — mixed systems!"
    ],
    [
     "counters",
     "세 명 — three people"
    ],
    [
     "I am 20",
     "스무 살"
    ],
    [
     "How much?",
     "얼마예요?"
    ]
   ]
  ]
 },
 {
  "slug": "food-and-ordering",
  "title": "Korean Food and Ordering",
  "desc": "Order with 주세요, wrap your first 쌈, survive spicy levels, and split the bill the Korean way.",
  "sections": [
   [
    "Ordering with 주세요",
    [
     "The pattern: <b>〜주세요</b> (juseyo — please give me…): <b>불고기 주세요</b>, <b>물 주세요</b> (water, please). Summon staff: <b>저기요!</b> (jeogiyo!). The menu: <b>메뉴판</b>. \"What's tasty here?\" — <b>여기 뭐가 맛있어요?</b> Vegetarian: <b>저는 채식주의자예요</b> — then negotiate, since fish sauce and beef stock hide in kimchi and stews."
    ]
   ],
   [
    "잘 먹겠습니다 — and mean it",
    [
     "Before eating: <b>잘 먹겠습니다</b> (jal meokgesseumnida — I will eat well). After: <b>잘 먹었습니다</b> (I ate well). Say them to the cook or host — they're gratitude, not ritual noise. Delicious mid-meal: <b>맛있어요!</b> Full: <b>배불러요</b> (my stomach is full). Hosts panic at empty plates — <b>더 드세요!</b> (eat more!) is love."
    ]
   ],
   [
    "Banchan, ssam and spice",
    [
     "<b>반찬</b> (banchan) side dishes are free and refillable — flag down staff for more kimchi without shame. <b>쌈</b> (ssam): wrap rice + meat + ssamjang in lettuce, eat in ONE bite. Spice levels: <b>안 매운 거 있어요?</b> (is there anything not spicy?) saves the mild-palated; <b>매워요!</b> (spicy!) with joyful tears earns nods. Rice (<b>밥</b>) also means \"meal\" — <b>밥 먹었어요?</b> is \"how are you\"."
    ]
   ],
   [
    "Paying: the eldest wins",
    [
     "The bill: <b>계산서 주세요</b> (bill, please). The eldest or the inviter pays — expect theatrical card-blocking battles; juniors lose gracefully. Splitting (<b>더치페이</b> — Dutch pay) is spreading among friends. Tipping is NOT customary. After dinner comes <b>2차</b> (second round — Hof, karaoke/noraebang) — budget your evening accordingly."
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
     "〜주세요",
     "…please — the ordering pattern"
    ],
    [
     "잘 먹겠습니다",
     "I will eat well — before eating"
    ],
    [
     "잘 먹었습니다",
     "I ate well — after eating"
    ],
    [
     "맛있어요!",
     "it's delicious!"
    ],
    [
     "계산서 주세요",
     "bill, please"
    ],
    [
     "배불러요",
     "I am full"
    ]
   ]
  ]
 },
 {
  "slug": "present-tense-verbs",
  "title": "Korean Present Tense — Verbs",
  "desc": "Conjugate the 요 present with 아/어 harmony, talk past with ㅆ, and make plans with ㄹ 거예요.",
  "sections": [
   [
    "Vowel harmony: 아 vs 어",
    [
     "The polite present stem ends in <b>아요</b> if the stem's last vowel is ㅏ or ㅗ, else <b>어요</b>: <b>가다→가요</b> (go), <b>오다→와요</b> (come), <b>먹다→먹어요</b> (eat), <b>읽다→읽어요</b> (read), <b>하다→해요</b> (do — special!). 하다 verbs are everywhere: <b>공부해요</b> (study), <b>전화해요</b> (phone), <b>결혼해요</b> (marry). Verbs never change for person — 저/당신/그 all take 먹어요."
    ]
   ],
   [
    "Past with ㅆ",
    [
     "Add <b>ㅆ어(요)</b>: <b>먹었어요</b> (ate), <b>갔어요</b> (went), <b>왔어요</b> (came), <b>했어요</b> (did). The ㅆ (ss) is the past marker in every polite past form — hear it and you're in yesterday. \"Did you eat?\" — <b>밥 먹었어요?</b> — doubles as \"how are you\", just like Chinese 你吃了吗."
    ]
   ],
   [
    "Future: ㄹ 거예요",
    [
     "Plans and promises: stem + <b>ㄹ/을 거예요</b> — <b>갈 거예요</b> (will go), <b>먹을 거예요</b> (will eat). Vowel stems take ㄹ, consonant stems 을. Intentions: <b>내일 만날 거예요</b> (will meet tomorrow). Guesses about others use <b>겠</b>: <b>비가 오겠어요</b> (it will probably rain). Everyday speech often uses the present for near future: <b>내일 가요</b> (I go tomorrow)."
    ]
   ],
   [
    "Want, like and please",
    [
     "Want: <b>고 싶어요</b> — <b>먹고 싶어요</b> (I want to eat). Like: <b>좋아해요</b> (<b>김치를 좋아해요</b> — I like kimchi). \"Please do\": <b>주세요</b> after a connective — <b>앉아 주세요</b> (please sit), <b>기다려 주세요</b> (please wait). Inviting: <b>같이…요</b> — <b>같이 먹어요</b> (let's eat together). Shall we: <b>…ㄹ까요?</b> — <b>먹을까요?</b>"
    ]
   ]
  ],
  "table": [
   [
    "Form",
    "먹다 (to eat)"
   ],
   [
    [
     "present",
     "먹어요"
    ],
    [
     "past",
     "먹었어요"
    ],
    [
     "future",
     "먹을 거예요"
    ],
    [
     "don't",
     "안 먹어요"
    ],
    [
     "can't",
     "못 먹어요"
    ],
    [
     "want to",
     "먹고 싶어요"
    ]
   ]
  ]
 }
]

PRACTICE = {
 "vocabulary": [
  {"q": "“안녕하세요” literally asks…", "a": "are you at peace?", "opts": ["are you at peace?", "have you eaten?", "where are you?", "who are you?"], "explain": "Annyeonghaseyo — are you at peace?"},
  {"q": "On the phone, Koreans answer…", "a": "여보세요", "opts": ["안녕하세요", "여보세요", "감사합니다", "반갑습니다"], "explain": "Yeoboseyo — the phone greeting."},
  {"q": "The LEAVER says goodbye with…", "a": "안녕히 계세요", "opts": ["안녕히 가세요", "안녕히 계세요", "안녕히 주무세요", "안녕히 드세요"], "explain": "Leaver: stay in peace (계세요)."},
  {"q": "The STAYER says goodbye with…", "a": "안녕히 가세요", "opts": ["안녕히 가세요", "안녕히 계세요", "안녕히 주무세요", "안녕히 드세요"], "explain": "Stayer: go in peace (가세요)."},
  {"q": "“감사합니다” means…", "a": "thank you", "opts": ["sorry", "thank you", "hello", "goodbye"], "explain": "Gamsahamnida — full thanks."},
  {"q": "Hangul was created in…", "a": "1443, by scholars", "opts": ["1900, by missionaries", "1443, by scholars", "500 BC, by monks", "it evolved naturally"], "explain": "King Sejong's scholars designed it in 1443."},
  {"q": "“잘 먹겠습니다” is said…", "a": "before eating", "opts": ["after eating", "before eating", "when paying", "when cooking"], "explain": "I will eat well — before the meal."},
  {"q": "“계산서 주세요” means…", "a": "bill, please", "opts": ["menu, please", "bill, please", "water, please", "one more"], "explain": "Gyesanseo juseyo — the bill."},
  {"q": "Free refillable side dishes are…", "a": "반찬", "opts": ["반찬", "쌈", "밥", "국"], "explain": "Banchan — free and refillable."},
  {"q": "“얼마예요?” means…", "a": "how much?", "opts": ["what time?", "how much?", "how old?", "where?"], "explain": "Eolmayeyo — how much is it?"},
  {"q": "“배불러요” means…", "a": "I am full", "opts": ["I am hungry", "I am full", "I am thirsty", "I am tired"], "explain": "My stomach is full."},
  {"q": "Splitting the bill is called…", "a": "더치페이", "opts": ["반반페이", "더치페이", "나눔페이", "각자페이"], "explain": "Deochipei — Dutch pay."}
 ],
 "grammar": [
  {"q": "“I am a student” (everyday polite) is…", "a": "저는 학생이에요", "opts": ["저는 학생입니다", "저는 학생이에요", "제가 학생이에요", "저는 학생예요"], "explain": "Consonant stem → 이에요."},
  {"q": "“(She) is a doctor” is…", "a": "의사예요", "opts": ["의사이에요", "의사예요", "의사합니다", "의사가요"], "explain": "Vowel stem → 예요."},
  {"q": "“Read a book” (object) is…", "a": "책을 읽어요", "opts": ["책을 읽어요", "책이 읽어요", "책에 읽어요", "책도 읽어요"], "explain": "을 marks the object (consonant stem)."},
  {"q": "“Study at the library” is…", "a": "도서관에서 공부해요", "opts": ["도서관에 공부해요", "도서관에서 공부해요", "도서관을 공부해요", "도서관도 공부해요"], "explain": "에서 marks where action happens."},
  {"q": "“There is no time” is…", "a": "시간이 없어요", "opts": ["시간이 없어요", "시간이 있어요", "시간을 없어요", "시간에 없어요"], "explain": "없어요 — the built-in negative of 있어요."},
  {"q": "“(I) ate” is…", "a": "먹었어요", "opts": ["먹어요", "먹었어요", "먹을 거예요", "먹고 싶어요"], "explain": "ㅆ어요 is the polite past."},
  {"q": "“(I) will eat” is…", "a": "먹을 거예요", "opts": ["먹어요", "먹었어요", "먹을 거예요", "먹었거예요"], "explain": "을 거예요 — consonant stem future."},
  {"q": "“I want to eat” is…", "a": "먹고 싶어요", "opts": ["먹어요 싶다", "먹고 싶어요", "먹을 싶어요", "먹기 싶어요"], "explain": "고 싶어요 = want to."},
  {"q": "“Three people” is…", "a": "세 명", "opts": ["삼 명", "세 명", "셋 명", "세 사람"], "explain": "셋 shortens to 세 before counters."},
  {"q": "“3:15” is…", "a": "세 시 십오 분", "opts": ["삼 시 십오 분", "세 시 십오 분", "세 시 열다섯 분", "삼 시 삼십오 분"], "explain": "Native hours + Sino minutes."},
  {"q": "“I like kimchi” is…", "a": "김치를 좋아해요", "opts": ["김치가 좋아해요", "김치를 좋아해요", "김치에 좋아해요", "김치도 좋아해요"], "explain": "좋아해요 takes the object particle."},
  {"q": "“I can't eat it” (allergy) is…", "a": "못 먹어요", "opts": ["안 먹어요", "못 먹어요", "먹지요", "안 먹지요"], "explain": "못 = can't; 안 = won't."}
 ]
}

QUIZ = [
 {"id": "ko-greet-1", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "Using 안녕 to a stranger is…", "a": "insulting", "opts": ["polite", "insulting", "formal", "normal"], "explain": "안녕 is for friends/juniors only."},
 {"id": "ko-greet-2", "lesson": "greetings-and-introductions", "type": "usage", "topic": "greetings", "level": "beginner", "q": "You are LEAVING a friend's home. You say…", "a": "안녕히 계세요", "opts": ["안녕히 계세요", "안녕히 가세요", "안녕히 주무세요", "잘 가세요"], "explain": "Leaver says: stay in peace."},
 {"id": "ko-greet-3", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "Business cards are received…", "a": "with two hands, then studied", "opts": ["one-handed", "with two hands, then studied", "never touched", "by bowing only"], "explain": "Two hands, study aloud, table it."},
 {"id": "ko-greet-4", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "“성함이 어떻게 되세요?” is…", "a": "honorific \"what is your name?\"", "opts": ["casual hello", "honorific \"what is your name?\"", "goodbye", "thank you"], "explain": "Seongham — the honorific word for name."},
 {"id": "ko-han-1", "lesson": "hangul-and-particles", "type": "vocab", "topic": "script", "level": "beginner", "q": "ㅇ at a syllable's START is…", "a": "silent", "opts": ["ng", "silent", "n", "m"], "explain": "Silent initially (아 = a); ng finally (강 = gang)."},
 {"id": "ko-han-2", "lesson": "hangul-and-particles", "type": "usage", "topic": "particles", "level": "beginner", "q": "Answer “누가 와요?” (who's coming?). You say…", "a": "제가 와요", "opts": ["제는 와요", "제가 와요", "저를 와요", "저도 와요"], "explain": "Who-answers take 가."},
 {"id": "ko-han-3", "lesson": "hangul-and-particles", "type": "meaning", "topic": "particles", "level": "beginner", "q": "“저도 학생이에요” means…", "a": "I too am a student", "opts": ["am I a student?", "I too am a student", "only I study", "I was a student"], "explain": "도 = also."},
 {"id": "ko-ida-1", "lesson": "ida-and-isseoyo", "type": "vocab", "topic": "grammar", "level": "beginner", "q": "“Is not a student” is…", "a": "학생이 아닙니다", "opts": ["학생이 아닙니다", "학생 안이에요", "학생이 없어요", "안 학생이에요"], "explain": "이 아닙니다 negates identity."},
 {"id": "ko-ida-2", "lesson": "ida-and-isseoyo", "type": "usage", "topic": "grammar", "level": "beginner", "q": "Say “I have a car”. You say…", "a": "저는 차가 있어요", "opts": ["저는 차가 있어요", "저는 차를 있어요", "저는 차에 있어요", "제가 차를 해요"], "explain": "Possession via existence: 차가 있어요."},
 {"id": "ko-ida-3", "lesson": "ida-and-isseoyo", "type": "meaning", "topic": "grammar", "level": "beginner", "q": "“맛있었어요!” (after the meal) means…", "a": "it WAS delicious!", "opts": ["it is delicious!", "it WAS delicious!", "it will be tasty!", "I am hungry!"], "explain": "Past recollection after eating."},
 {"id": "ko-num-1", "lesson": "two-number-systems", "type": "vocab", "topic": "numbers", "level": "beginner", "q": "5,000 won is…", "a": "오천 원", "opts": ["다섯천 원", "오천 원", "오백 원", "만오천 원"], "explain": "Money uses Sino-Korean: 오천 원."},
 {"id": "ko-num-2", "lesson": "two-number-systems", "type": "vocab", "topic": "numbers", "level": "beginner", "q": "The universal rescue counter is…", "a": "개", "opts": ["명", "개", "잔", "마리"], "explain": "개 (gae) counts generic things."},
 {"id": "ko-num-3", "lesson": "two-number-systems", "type": "usage", "topic": "numbers", "level": "beginner", "q": "Say “two (things)” with a counter. You say…", "a": "두 개", "opts": ["둘 개", "두 개", "이 개", "둘의 개"], "explain": "둘 shortens to 두 before counters."},
 {"id": "ko-food-1", "lesson": "food-and-ordering", "type": "usage", "topic": "food", "level": "beginner", "q": "Order bulgogi politely. You say…", "a": "불고기 주세요", "opts": ["불고기 주세요", "불고기가 주세요", "불고기를 해요", "주세요 불고기를"], "explain": "…주세요 — please give me…"},
 {"id": "ko-food-2", "lesson": "food-and-ordering", "type": "meaning", "topic": "food", "level": "beginner", "q": "“밥 먹었어요?” doubles as…", "a": "\"how are you?\"", "opts": ["a dinner invite", "\"how are you?\"", "a complaint", "a bill request"], "explain": "밥 = rice/meal — have you eaten = how are you."},
 {"id": "ko-food-3", "lesson": "food-and-ordering", "type": "vocab", "topic": "food", "level": "beginner", "q": "Ssam (쌈) is eaten…", "a": "in one bite", "opts": ["with a fork", "in one bite", "in small nibbles", "with chopsticks only"], "explain": "Wrap it, eat it whole."},
 {"id": "ko-verb-1", "lesson": "present-tense-verbs", "type": "vocab", "topic": "verbs", "level": "beginner", "q": "하다 (do) becomes…", "a": "해요", "opts": ["하요", "해요", "하여요", "해어요"], "explain": "Hada is special: 해요."},
 {"id": "ko-verb-2", "lesson": "present-tense-verbs", "type": "usage", "topic": "verbs", "level": "beginner", "q": "Propose “let's eat together”. You say…", "a": "같이 먹어요", "opts": ["같이 먹어요", "먹고 싶어요", "먹을 거예요", "같이 먹었어요"], "explain": "같이…요 — let's together."},
 {"id": "ko-verb-3", "lesson": "present-tense-verbs", "type": "meaning", "topic": "verbs", "level": "beginner", "q": "“비가 오겠어요” means…", "a": "it will probably rain", "opts": ["it is raining", "it will probably rain", "it rained", "rain please"], "explain": "겠 guesses about others."},
 {"id": "ko-greet-5", "lesson": "greetings-and-introductions", "type": "meaning", "topic": "greetings", "level": "beginner", "q": "Receiving a drink from an elder: you…", "a": "use two hands, turn aside to sip", "opts": ["use one hand", "use two hands, turn aside to sip", "refuse first", "drink facing them"], "explain": "Two hands to receive, turn aside to sip."}
]

REVIEW = [
 {"p": "안녕하세요", "a": "hello (are you at peace?)"},
 {"p": "저는…입니다", "a": "I am…"},
 {"p": "만나서 반갑습니다", "a": "pleased to meet you"},
 {"p": "안녕히 가세요 / 계세요", "a": "goodbye (stayer / leaver)"},
 {"p": "감사합니다", "a": "thank you"},
 {"p": "죄송합니다", "a": "sorry (formal)"},
 {"p": "한글", "a": "the Korean alphabet"},
 {"p": "은/는 · 이/가", "a": "topic · subject"},
 {"p": "책을 읽어요", "a": "(I) read a book"},
 {"p": "…주세요", "a": "…please (give me)"},
 {"p": "잘 먹겠습니다", "a": "before eating"},
 {"p": "잘 먹었습니다", "a": "after eating"},
 {"p": "맛있어요!", "a": "it's delicious!"},
 {"p": "계산서 주세요", "a": "bill, please"},
 {"p": "고양이가 있어요", "a": "there is a cat"},
 {"p": "저는 차가 있어요", "a": "I have a car"},
 {"p": "세 명", "a": "three people"},
 {"p": "세 시 십오 분", "a": "3:15"},
 {"p": "얼마예요?", "a": "how much?"},
 {"p": "먹었어요", "a": "(I) ate"},
 {"p": "먹을 거예요", "a": "(I) will eat"},
 {"p": "먹고 싶어요", "a": "I want to eat"},
 {"p": "안 먹어요 / 못 먹어요", "a": "won't eat / can't eat"},
 {"p": "같이 먹어요", "a": "let's eat together"}
]

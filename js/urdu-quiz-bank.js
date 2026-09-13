/* =========================================================
   EkGuru — URDU QUIZ BANK  (single source of truth · v1)
   ---------------------------------------------------------
   Same contract as js/hindi-quiz-bank.js: the data object is
   deliberately valid JSON; js/hindi-tools.js renders quiz,
   typing and worksheets from the EKGURU_*_ACTIVE globals this
   file sets. Conservative, checked urdu — quiz answers test
   recognition, never fluency.
   ========================================================= */
window.EKGURU_URDU_QUIZ =
{
 "version": 1,
 "questions": [
  {
   "a": "hello! (peace greeting)",
   "explain": "السلام علیکم (Assalām Alaikum) — 'peace be upon you' — is the standard Urdu hello. Reply: وعلیکم السلام!",
   "id": "ur-01",
   "lesson": "basics",
   "level": "beginner",
   "opts": [
    "hello! (peace greeting)",
    "goodbye!",
    "thank you",
    "sorry"
   ],
   "q": "What does السلام علیکم mean?",
   "topic": "basics",
   "type": "meaning"
  },
  {
   "a": "thank you",
   "explain": "شکریہ (shukriyā) is thanks — same word Hindi borrowed.",
   "id": "ur-02",
   "lesson": "basics",
   "level": "beginner",
   "opts": [
    "thank you",
    "please",
    "sorry",
    "welcome"
   ],
   "q": "What does شکریہ mean?",
   "topic": "basics",
   "type": "meaning"
  },
  {
   "a": "میرا نام … ہے",
   "explain": "آپ کا نام کیا ہے؟ = what's your name — answer میرا نام … ہے (my name is …).",
   "id": "ur-03",
   "lesson": "basics",
   "level": "beginner",
   "opts": [
    "میرا نام … ہے",
    "مجھے بھوک لگی ہے",
    "پھر ملیں گے!",
    "رعایت دیں"
   ],
   "q": "Someone asks 'آپ کا نام کیا ہے؟' — you reply…",
   "topic": "basics",
   "type": "usage"
  },
  {
   "a": "sh as in shoe",
   "explain": "ش (shīn) is sh — س (sīn) is the plain s. Dots decide!",
   "id": "ur-04",
   "lesson": "pronunciation",
   "level": "beginner",
   "opts": [
    "sh as in shoe",
    "s as in sun",
    "h as in hat",
    "k as in kite"
   ],
   "q": "The letter ش sounds like…",
   "topic": "basics",
   "type": "vocab"
  },
  {
   "a": "3",
   "explain": "ایک دو تین — 1, 2, 3.",
   "id": "ur-05",
   "lesson": "numbers",
   "level": "beginner",
   "opts": [
    "2",
    "3",
    "4",
    "5"
   ],
   "q": "تین means…",
   "topic": "numbers",
   "type": "vocab"
  },
  {
   "a": "دس",
   "explain": "دس (das) = 10. پانچ = 5, بیس = 20, سو = 100.",
   "id": "ur-06",
   "lesson": "numbers",
   "level": "beginner",
   "opts": [
    "دس",
    "پانچ",
    "بیس",
    "سو"
   ],
   "q": "Which is 'ten'?",
   "topic": "numbers",
   "type": "vocab"
  },
  {
   "a": "20",
   "explain": "بیس (bīs) = 20, انیس = 19, اکیس = 21.",
   "id": "ur-07",
   "lesson": "numbers",
   "level": "beginner",
   "opts": [
    "12",
    "20",
    "22",
    "200"
   ],
   "q": "بیس means…",
   "topic": "numbers",
   "type": "meaning"
  },
  {
   "a": "50 rupees",
   "explain": "پچاس (pachās) = 50. پانچ = 5, پندرہ = 15, پانچ سو = 500.",
   "id": "ur-08",
   "lesson": "numbers",
   "level": "elementary",
   "opts": [
    "5 rupees",
    "15 rupees",
    "50 rupees",
    "500 rupees"
   ],
   "q": "'پچاس روپے' on a price tag means…",
   "topic": "numbers",
   "type": "usage"
  },
  {
   "a": "a slow-cooked meat stew",
   "explain": "نہاری — simmered overnight, eaten at dawn with naan — is Old Delhi's legendary breakfast.",
   "id": "ur-09",
   "lesson": "food",
   "level": "beginner",
   "opts": [
    "a slow-cooked meat stew",
    "a lentil curry",
    "a flatbread",
    "a dessert"
   ],
   "q": "نہاری is…",
   "topic": "food",
   "type": "vocab"
  },
  {
   "a": "this is very tasty",
   "explain": "مزیدار (mazedār) = tasty — say it and any cook will beam.",
   "id": "ur-10",
   "lesson": "food",
   "level": "beginner",
   "opts": [
    "this is very tasty",
    "this is too spicy",
    "the bill please",
    "I'm hungry"
   ],
   "q": "'یہ بہت مزیدار ہے' means…",
   "topic": "food",
   "type": "meaning"
  },
  {
   "a": "مجھے بھوک لگی ہے",
   "explain": "مجھے بھوک لگی ہے = I'm hungry. پیاس = thirst, بل = bill.",
   "id": "ur-11",
   "lesson": "food",
   "level": "elementary",
   "opts": [
    "مجھے بھوک لگی ہے",
    "مجھے پیاس لگی ہے",
    "بل دیں",
    "رعایت دیں"
   ],
   "q": "You're hungry in Lucknow. You say…",
   "topic": "food",
   "type": "usage"
  },
  {
   "a": "where is the station?",
   "explain": "کہاں (kahān) = where — the traveller's most useful word.",
   "id": "ur-12",
   "lesson": "travel",
   "level": "beginner",
   "opts": [
    "where is the station?",
    "how much is the fare?",
    "stop here",
    "one ticket please"
   ],
   "q": "'اسٹیشن کہاں ہے؟' means…",
   "topic": "travel",
   "type": "meaning"
  },
  {
   "a": "ticket",
   "explain": "ٹکٹ (ṭikaṭ) = ticket; کرایہ = fare; اسٹیشن = station.",
   "id": "ur-13",
   "lesson": "travel",
   "level": "beginner",
   "opts": [
    "ticket",
    "train",
    "fare",
    "station"
   ],
   "q": "ٹکٹ means…",
   "topic": "travel",
   "type": "vocab"
  },
  {
   "a": "یہاں رکیں",
   "explain": "یہاں رکیں (yahān ruken) = stop here. آہستہ چلیں = go slowly.",
   "id": "ur-14",
   "lesson": "travel",
   "level": "elementary",
   "opts": [
    "یہاں رکیں",
    "آہستہ چلیں",
    "سیدھا جائیں",
    "ٹکٹ دیں"
   ],
   "q": "To make the auto stop here, say…",
   "topic": "travel",
   "type": "usage"
  },
  {
   "a": "a man saying 'I eat'",
   "explain": "کھاتا (khātā, -تا) marks a male speaker; a woman says کھاتی ہوں.",
   "id": "ur-15",
   "lesson": "grammar",
   "level": "elementary",
   "opts": [
    "a man saying 'I eat'",
    "a woman saying 'I eat'",
    "a man saying 'I ate'",
    "many people saying 'we eat'"
   ],
   "q": "'میں کھاتا ہوں' is spoken by…",
   "topic": "grammar",
   "type": "meaning"
  },
  {
   "a": "کھاتی",
   "explain": "کھاتا/کھاتی (m/f), کھاتے (plural/respectful) — adjectives work the same way.",
   "id": "ur-16",
   "lesson": "grammar",
   "level": "elementary",
   "opts": [
    "کھاتی",
    "کھاتے",
    "کھایا",
    "کھاؤں گا"
   ],
   "q": "The feminine of کھاتا is…",
   "topic": "grammar",
   "type": "vocab"
  },
  {
   "a": "کھایا",
   "explain": "کھایا/کھائی (m/f) = ate; کھاؤں گا/کھاؤں گی = will eat.",
   "id": "ur-17",
   "lesson": "grammar",
   "level": "elementary",
   "opts": [
    "کھایا",
    "کھائی",
    "کھاؤں گا",
    "کھاتا"
   ],
   "q": "The past tense 'ate' (said by a man) is…",
   "topic": "grammar",
   "type": "vocab"
  },
  {
   "a": "it agrees with روٹی (feminine)",
   "explain": "Urdu past tenses are ergative: the verb agrees with the object — روٹی is feminine, so کھائی.",
   "id": "ur-18",
   "lesson": "grammar",
   "level": "elementary",
   "opts": [
    "it agrees with روٹی (feminine)",
    "the speaker is female",
    "it's the future tense",
    "it's a typo"
   ],
   "q": "In 'میں نے روٹی کھائی', why کھائی?",
   "topic": "grammar",
   "type": "usage"
  },
  {
   "a": "see you! (we'll meet again)",
   "explain": "پھر ملیں گے (phir milenge) — literally 'we'll meet again' — the warm goodbye.",
   "id": "ur-19",
   "lesson": "conversation",
   "level": "beginner",
   "opts": [
    "see you! (we'll meet again)",
    "good morning!",
    "welcome!",
    "congratulations!"
   ],
   "q": "'پھر ملیں گے!' means…",
   "topic": "conversation",
   "type": "meaning"
  },
  {
   "a": "welcome!",
   "explain": "خوش آمدید (khush āmdīd) — the warm Urdu welcome.",
   "id": "ur-20",
   "lesson": "conversation",
   "level": "beginner",
   "opts": [
    "welcome!",
    "sorry!",
    "good luck!",
    "bless you!"
   ],
   "q": "'خوش آمدید!' means…",
   "topic": "conversation",
   "type": "meaning"
  },
  {
   "a": "book",
   "explain": "کتاب (kitāb) = book — قلم = pen, خط = letter.",
   "id": "ur-21",
   "lesson": "vocabulary",
   "level": "beginner",
   "opts": [
    "book",
    "pen",
    "school",
    "letter"
   ],
   "q": "کتاب means…",
   "topic": "vocabulary",
   "type": "vocab"
  },
  {
   "a": "friend",
   "explain": "دوست (dost) = friend — دشمن is the opposite!",
   "id": "ur-22",
   "lesson": "vocabulary",
   "level": "beginner",
   "opts": [
    "friend",
    "brother",
    "guest",
    "neighbour"
   ],
   "q": "دوست means…",
   "topic": "vocabulary",
   "type": "vocab"
  },
  {
   "a": "asking the price",
   "explain": "یہ کتنے کا ہے؟ = how much is this — then counter with تھوڑا سستا کریں!",
   "id": "ur-23",
   "lesson": "shopping",
   "level": "elementary",
   "opts": [
    "asking the price",
    "ordering food",
    "asking directions",
    "saying goodbye"
   ],
   "q": "'یہ کتنے کا ہے؟' is asked when…",
   "topic": "vocabulary",
   "type": "usage"
  },
  {
   "a": "tomorrow — or yesterday!",
   "explain": "کل (kal) covers both — tense and context tell you which. پرسوں = the day beyond.",
   "id": "ur-24",
   "lesson": "time-dates",
   "level": "elementary",
   "opts": [
    "only tomorrow",
    "only yesterday",
    "tomorrow — or yesterday!",
    "every day"
   ],
   "q": "کل means…",
   "topic": "vocabulary",
   "type": "meaning"
  }
 ]
};
window.EKGURU_QUIZ_ACTIVE = window.EKGURU_URDU_QUIZ;
window.EKGURU_QUIZ_NAME = "urdu-quiz";
window.EKGURU_COURSE_LANG = { name: "Urdu", script: "Urdu (Nastaliq)" };
window.EKGURU_TYPING_ACTIVE =
[
 [
  "ماں",
  "maan"
 ],
 [
  "پانی",
  "paani"
 ],
 [
  "گھر",
  "ghar"
 ],
 [
  "روٹی",
  "roti"
 ],
 [
  "دال",
  "daal"
 ],
 [
  "چائے",
  "chaaye"
 ],
 [
  "لسی",
  "lassi"
 ],
 [
  "کتاب",
  "kitaab"
 ],
 [
  "اسکول",
  "school"
 ],
 [
  "بازار",
  "bazaar"
 ],
 [
  "دکان",
  "dukaan"
 ],
 [
  "ٹکٹ",
  "ticket"
 ],
 [
  "گاڑی",
  "gaadi"
 ],
 [
  "راستہ",
  "raasta"
 ],
 [
  "دن",
  "din"
 ],
 [
  "رات",
  "raat"
 ],
 [
  "صبح",
  "subah"
 ],
 [
  "شام",
  "shaam"
 ],
 [
  "لڑکا",
  "ladka"
 ],
 [
  "لڑکی",
  "ladki"
 ],
 [
  "دوست",
  "dost"
 ],
 [
  "پیار",
  "pyaar"
 ],
 [
  "خوش",
  "khush"
 ],
 [
  "شکریہ",
  "shukriya"
 ]
];

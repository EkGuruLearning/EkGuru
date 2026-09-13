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
  },
  {
   "a": "fever",
   "explain": "بخار (bukhar) = fever — مجھے بخار ہے (I have a fever).",
   "id": "ur-25",
   "lesson": "health",
   "level": "beginner",
   "opts": [
    "fever",
    "cough",
    "cold",
    "pain"
   ],
   "q": "بخار means…",
   "topic": "health",
   "type": "vocab"
  },
  {
   "a": "ڈاکٹر",
   "explain": "ڈاکٹر (doctor) = doctor.",
   "id": "ur-26",
   "lesson": "health",
   "level": "beginner",
   "opts": [
    "ڈاکٹر",
    "نرس",
    "مریض",
    "سرجن"
   ],
   "q": "Which is 'doctor'?",
   "topic": "health",
   "type": "vocab"
  },
  {
   "a": "I am not feeling well",
   "explain": "مجھے اچھا نہیں لگ رہا — اچھا = good.",
   "id": "ur-27",
   "lesson": "health",
   "level": "beginner",
   "opts": [
    "I am not feeling well",
    "I have a fever",
    "take rest",
    "get well soon"
   ],
   "q": "'مجھے اچھا نہیں لگ رہا' means…",
   "topic": "health",
   "type": "meaning"
  },
  {
   "a": "دوائی کی دکان کہاں ہے؟",
   "explain": "دوائی کی دکان کہاں ہے؟ — کہاں = where.",
   "id": "ur-28",
   "lesson": "health",
   "level": "elementary",
   "opts": [
    "دوائی کی دکان کہاں ہے؟",
    "ہسپتال کہاں ہے؟",
    "ڈاکٹر کہاں ہے؟",
    "گھر کہاں ہے؟"
   ],
   "q": "Ask where the pharmacy is. You say…",
   "topic": "health",
   "type": "usage"
  },
  {
   "a": "heart",
   "explain": "دل (dil) = heart.",
   "id": "ur-29",
   "lesson": "health",
   "level": "beginner",
   "opts": [
    "heart",
    "lung",
    "stomach",
    "liver"
   ],
   "q": "دل means…",
   "topic": "health",
   "type": "vocab"
  },
  {
   "a": "medical diet",
   "explain": "پرہیز (parhez) — the doctor's diet rules.",
   "id": "ur-30",
   "lesson": "health",
   "level": "elementary",
   "opts": [
    "medical diet",
    "home remedy",
    "herbal medicine",
    "first aid"
   ],
   "q": "پرہیز means…",
   "topic": "health",
   "type": "vocab"
  },
  {
   "a": "get well soon",
   "explain": "جلدی صحت یاب ہو جائیے — جلدی = soon.",
   "id": "ur-31",
   "lesson": "health",
   "level": "elementary",
   "opts": [
    "get well soon",
    "take rest",
    "drink hot water",
    "call a doctor"
   ],
   "q": "'جلدی صحت یاب ہو جائیے' means…",
   "topic": "health",
   "type": "meaning"
  },
  {
   "a": "منہ کھولیے",
   "explain": "منہ کھولیے = open your mouth — منہ = mouth.",
   "id": "ur-32",
   "lesson": "health",
   "level": "elementary",
   "opts": [
    "منہ کھولیے",
    "آنکھیں بند کیجیے",
    "ہاتھ بڑھائیے",
    "کھڑے ہو جائیے"
   ],
   "q": "The doctor says 'open your mouth'. She says…",
   "topic": "health",
   "type": "usage"
  },
  {
   "a": "injection",
   "explain": "ٹیکہ (tika) — injection; سوئی = needle.",
   "id": "ur-33",
   "lesson": "health",
   "level": "beginner",
   "opts": [
    "injection",
    "tablet",
    "syrup",
    "ointment"
   ],
   "q": "ٹیکہ means…",
   "topic": "health",
   "type": "vocab"
  },
  {
   "a": "take rest",
   "explain": "آرام کیجیے — آرام = rest.",
   "id": "ur-34",
   "lesson": "health",
   "level": "beginner",
   "opts": [
    "take rest",
    "wake up",
    "breathe deeply",
    "walk daily"
   ],
   "q": "'آرام کیجیے' means…",
   "topic": "health",
   "type": "meaning"
  },
  {
   "a": "salary",
   "explain": "تنخواہ (tankhvah) = salary.",
   "id": "ur-35",
   "lesson": "office",
   "level": "beginner",
   "opts": [
    "salary",
    "bonus",
    "loan",
    "bill"
   ],
   "q": "تنخواہ means…",
   "topic": "office",
   "type": "vocab"
  },
  {
   "a": "کمپیوٹر",
   "explain": "کمپیوٹر (computer) = computer.",
   "id": "ur-36",
   "lesson": "office",
   "level": "beginner",
   "opts": [
    "کمپیوٹر",
    "پرنٹر",
    "فائل",
    "میز"
   ],
   "q": "Which is 'computer'?",
   "topic": "office",
   "type": "vocab"
  },
  {
   "a": "come on time",
   "explain": "وقت پر آئیے — وقت = time.",
   "id": "ur-37",
   "lesson": "office",
   "level": "beginner",
   "opts": [
    "come on time",
    "go home early",
    "work fast",
    "take leave"
   ],
   "q": "'وقت پر آئیے' means…",
   "topic": "office",
   "type": "meaning"
  },
  {
   "a": "کل مجھے چھٹی چاہیے",
   "explain": "کل مجھے چھٹی چاہیے — چھٹی = leave.",
   "id": "ur-38",
   "lesson": "office",
   "level": "elementary",
   "opts": [
    "کل مجھے چھٹی چاہیے",
    "کل میٹنگ ہے",
    "کل تنخواہ ملے گی",
    "کل چھٹی نہیں"
   ],
   "q": "Ask for tomorrow's leave. You say…",
   "topic": "office",
   "type": "usage"
  },
  {
   "a": "signature",
   "explain": "دستخط (dastakhat) = signature.",
   "id": "ur-39",
   "lesson": "office",
   "level": "beginner",
   "opts": [
    "signature",
    "stamp",
    "file",
    "seal"
   ],
   "q": "دستخط means…",
   "topic": "office",
   "type": "vocab"
  },
  {
   "a": "photocopy",
   "explain": "زیروکس (zerox) — from Xerox! Urdu for photocopy.",
   "id": "ur-40",
   "lesson": "office",
   "level": "elementary",
   "opts": [
    "photocopy",
    "printout",
    "scanner",
    "file"
   ],
   "q": "زیروکس means…",
   "topic": "office",
   "type": "vocab"
  },
  {
   "a": "the work is finished",
   "explain": "کام ختم ہوا — ختم = finished.",
   "id": "ur-41",
   "lesson": "office",
   "level": "elementary",
   "opts": [
    "the work is finished",
    "the work begins",
    "the work is difficult",
    "the work can wait"
   ],
   "q": "'کام ختم ہوا' means…",
   "topic": "office",
   "type": "meaning"
  },
  {
   "a": "ای میل بھیجیے",
   "explain": "ای میل بھیجیے — بھیجیے = send.",
   "id": "ur-42",
   "lesson": "office",
   "level": "elementary",
   "opts": [
    "ای میل بھیجیے",
    "خط لکھیے",
    "فون کیجیے",
    "اجلاس میں آئیے"
   ],
   "q": "Tell someone to send the email. You say…",
   "topic": "office",
   "type": "usage"
  },
  {
   "a": "leave",
   "explain": "چھٹی (chhutti) = leave.",
   "id": "ur-43",
   "lesson": "office",
   "level": "beginner",
   "opts": [
    "leave",
    "holiday",
    "salary",
    "bonus"
   ],
   "q": "چھٹی means…",
   "topic": "office",
   "type": "vocab"
  },
  {
   "a": "good job!",
   "explain": "شاباش! — well done!",
   "id": "ur-44",
   "lesson": "office",
   "level": "beginner",
   "opts": [
    "good job!",
    "go home!",
    "sit down!",
    "wait here!"
   ],
   "q": "'شاباش!' means…",
   "topic": "office",
   "type": "meaning"
  },
  {
   "a": "teacher",
   "explain": "استاد (ustad) = teacher.",
   "id": "ur-45",
   "lesson": "education",
   "level": "beginner",
   "opts": [
    "teacher",
    "student",
    "professor",
    "examiner"
   ],
   "q": "استاد means…",
   "topic": "education",
   "type": "vocab"
  },
  {
   "a": "نئی کتاب",
   "explain": "نئی کتاب (nai kitab) = new book.",
   "id": "ur-46",
   "lesson": "education",
   "level": "beginner",
   "opts": [
    "نئی کتاب",
    "اخبار",
    "کاغذ",
    "حرف"
   ],
   "q": "Which is 'new book'?",
   "topic": "education",
   "type": "vocab"
  },
  {
   "a": "read aloud",
   "explain": "زور سے پڑھیے — زور = loudly.",
   "id": "ur-47",
   "lesson": "education",
   "level": "beginner",
   "opts": [
    "read aloud",
    "write neatly",
    "sit quietly",
    "stand up"
   ],
   "q": "'زور سے پڑھیے' means…",
   "topic": "education",
   "type": "meaning"
  },
  {
   "a": "مجھے نہیں معلوم",
   "explain": "مجھے نہیں معلوم — معلوم = known.",
   "id": "ur-48",
   "lesson": "education",
   "level": "elementary",
   "opts": [
    "مجھے نہیں معلوم",
    "مجھے یاد ہے",
    "مجھے سمجھ آیا",
    "مجھے آتا ہے"
   ],
   "q": "Say 'I don't know'. You say…",
   "topic": "education",
   "type": "usage"
  },
  {
   "a": "exam",
   "explain": "امتحان (imtihan) = exam.",
   "id": "ur-49",
   "lesson": "education",
   "level": "beginner",
   "opts": [
    "exam",
    "mark",
    "rank",
    "pass"
   ],
   "q": "امتحان means…",
   "topic": "education",
   "type": "vocab"
  },
  {
   "a": "slate",
   "explain": "تختی (takhti) — the child's first slate!",
   "id": "ur-50",
   "lesson": "education",
   "level": "elementary",
   "opts": [
    "slate",
    "notebook",
    "diary",
    "atlas"
   ],
   "q": "تختی means…",
   "topic": "education",
   "type": "vocab"
  },
  {
   "a": "study well",
   "explain": "اچھی طرح پڑھیے — پڑھنا = to study.",
   "id": "ur-51",
   "lesson": "education",
   "level": "elementary",
   "opts": [
    "study well",
    "write neatly",
    "read aloud",
    "come early"
   ],
   "q": "'اچھی طرح پڑھیے' means…",
   "topic": "education",
   "type": "meaning"
  },
  {
   "a": "اپنی کتابیں کھولیے",
   "explain": "اپنی کتابیں کھولیے — کھولیے = open.",
   "id": "ur-52",
   "lesson": "education",
   "level": "elementary",
   "opts": [
    "اپنی کتابیں کھولیے",
    "اپنی کاپیاں لائیے",
    "اپنی تختیاں رکھیے",
    "اپنا نام لکھیے"
   ],
   "q": "Tell students to open their books. You say…",
   "topic": "education",
   "type": "usage"
  },
  {
   "a": "student",
   "explain": "طالب علم (talib-e-ilm) = student.",
   "id": "ur-53",
   "lesson": "education",
   "level": "beginner",
   "opts": [
    "student",
    "teacher",
    "professor",
    "examiner"
   ],
   "q": "طالب علم means…",
   "topic": "education",
   "type": "vocab"
  },
  {
   "a": "passing marks",
   "explain": "پاس نمبر — پاس = pass.",
   "id": "ur-54",
   "lesson": "education",
   "level": "beginner",
   "opts": [
    "passing marks",
    "rank",
    "degree",
    "uniform"
   ],
   "q": "پاس نمبر means…",
   "topic": "education",
   "type": "vocab"
  },
  {
   "a": "weather",
   "explain": "موسم (mausam) = weather.",
   "id": "ur-55",
   "lesson": "weather",
   "level": "beginner",
   "opts": [
    "weather",
    "rain",
    "wind",
    "cloud"
   ],
   "q": "موسم means…",
   "topic": "weather",
   "type": "vocab"
  },
  {
   "a": "بارش",
   "explain": "بارش (barish) = rain.",
   "id": "ur-56",
   "lesson": "weather",
   "level": "beginner",
   "opts": [
    "بارش",
    "طوفان",
    "بادل",
    "بجلی"
   ],
   "q": "Which is 'rain'?",
   "topic": "weather",
   "type": "vocab"
  },
  {
   "a": "it is very hot",
   "explain": "بہت گرمی ہے — گرمی = heat.",
   "id": "ur-57",
   "lesson": "weather",
   "level": "beginner",
   "opts": [
    "it is very hot",
    "it is cold today",
    "it is raining",
    "night fell"
   ],
   "q": "'بہت گرمی ہے' means…",
   "topic": "weather",
   "type": "meaning"
  },
  {
   "a": "چھاتا لے لیجیے",
   "explain": "چھاتا لے لیجیے — چھاتا = umbrella.",
   "id": "ur-58",
   "lesson": "weather",
   "level": "elementary",
   "opts": [
    "چھاتا لے لیجیے",
    "ٹوپی پہنیے",
    "جوتی اتاریے",
    "سویٹر پہنیے"
   ],
   "q": "Tell someone to take an umbrella. You say…",
   "topic": "weather",
   "type": "usage"
  },
  {
   "a": "sun",
   "explain": "سورج (suraj) = sun.",
   "id": "ur-59",
   "lesson": "weather",
   "level": "beginner",
   "opts": [
    "sun",
    "moon",
    "star",
    "sky"
   ],
   "q": "سورج means…",
   "topic": "weather",
   "type": "vocab"
  },
  {
   "a": "monsoon",
   "explain": "ساون بھادوں — the monsoon months!",
   "id": "ur-60",
   "lesson": "weather",
   "level": "elementary",
   "opts": [
    "monsoon",
    "summer",
    "winter",
    "spring"
   ],
   "q": "ساون بھادوں means…",
   "topic": "weather",
   "type": "vocab"
  },
  {
   "a": "the sun rose",
   "explain": "سورج نکلا — نکلنا = to rise.",
   "id": "ur-61",
   "lesson": "weather",
   "level": "elementary",
   "opts": [
    "the sun rose",
    "the sun set",
    "night fell",
    "the moon rose"
   ],
   "q": "'سورج نکلا' means…",
   "topic": "weather",
   "type": "meaning"
  },
  {
   "a": "شام کو ملیں گے",
   "explain": "شام کو ملیں گے — شام = evening.",
   "id": "ur-62",
   "lesson": "weather",
   "level": "elementary",
   "opts": [
    "شام کو ملیں گے",
    "صبح ملیں گے",
    "کل ملیں گے",
    "پھر ملیں گے"
   ],
   "q": "Say 'see you in the evening'. You say…",
   "topic": "weather",
   "type": "usage"
  },
  {
   "a": "cold",
   "explain": "ٹھنڈ (thand) = cold.",
   "id": "ur-63",
   "lesson": "weather",
   "level": "beginner",
   "opts": [
    "cold",
    "heat",
    "wind",
    "fog"
   ],
   "q": "ٹھنڈ means…",
   "topic": "weather",
   "type": "vocab"
  },
  {
   "a": "rainbow",
   "explain": "قوس قزح (qaus-e-quzah) — the sky-bow!",
   "id": "ur-64",
   "lesson": "weather",
   "level": "beginner",
   "opts": [
    "rainbow",
    "lightning",
    "cloud",
    "dew"
   ],
   "q": "قوس قزح means…",
   "topic": "weather",
   "type": "vocab"
  },
  {
   "a": "biryani",
   "explain": "بریانی (biryani) — the beloved dish!",
   "id": "ur-65",
   "lesson": "home",
   "level": "beginner",
   "opts": [
    "biryani",
    "korma",
    "kebab",
    "nihari"
   ],
   "q": "بریانی means…",
   "topic": "home",
   "type": "vocab"
  },
  {
   "a": "اپنا گھر",
   "explain": "اپنا گھر (apna ghar) = own house.",
   "id": "ur-66",
   "lesson": "home",
   "level": "beginner",
   "opts": [
    "اپنا گھر",
    "صدر دروازہ",
    "کھڑکی",
    "کمرہ"
   ],
   "q": "Which is 'own house'?",
   "topic": "home",
   "type": "vocab"
  },
  {
   "a": "the food is ready",
   "explain": "کھانا تیار ہے — تیار = ready.",
   "id": "ur-67",
   "lesson": "home",
   "level": "beginner",
   "opts": [
    "the food is ready",
    "the food is tasty",
    "the food is hot",
    "the food is over"
   ],
   "q": "'کھانا تیار ہے' means…",
   "topic": "home",
   "type": "meaning"
  },
  {
   "a": "ہاتھ دھوئیے",
   "explain": "ہاتھ دھوئیے — ہاتھ = hand.",
   "id": "ur-68",
   "lesson": "home",
   "level": "elementary",
   "opts": [
    "ہاتھ دھوئیے",
    "منہ دھوئیے",
    "پیر دھوئیے",
    "بال دھوئیے"
   ],
   "q": "Tell a child to wash hands. You say…",
   "topic": "home",
   "type": "usage"
  },
  {
   "a": "main door",
   "explain": "صدر دروازہ (sadr darvaza) = main door.",
   "id": "ur-69",
   "lesson": "home",
   "level": "beginner",
   "opts": [
    "main door",
    "window",
    "wall",
    "roof"
   ],
   "q": "صدر دروازہ means…",
   "topic": "home",
   "type": "vocab"
  },
  {
   "a": "hot rice",
   "explain": "گرم چاول — hot rice; باسمتی = basmati.",
   "id": "ur-70",
   "lesson": "home",
   "level": "elementary",
   "opts": [
    "hot rice",
    "dal",
    "curry",
    "roti"
   ],
   "q": "گرم چاول means…",
   "topic": "home",
   "type": "vocab"
  },
  {
   "a": "it is very tasty!",
   "explain": "بہت مزیدار ہے! — مزیدار = tasty.",
   "id": "ur-71",
   "lesson": "home",
   "level": "elementary",
   "opts": [
    "it is very tasty!",
    "it is very hot!",
    "it is very sweet!",
    "it is enough!"
   ],
   "q": "'بہت مزیدار ہے!' means…",
   "topic": "home",
   "type": "meaning"
  },
  {
   "a": "صدر دروازہ بند کیجیے",
   "explain": "صدر دروازہ بند کیجیے — بند = closed.",
   "id": "ur-72",
   "lesson": "home",
   "level": "elementary",
   "opts": [
    "صدر دروازہ بند کیجیے",
    "کھڑکی کھولیے",
    "دیا جلائیے",
    "ٹی وی چلائیے"
   ],
   "q": "Say 'close the main door'. You say…",
   "topic": "home",
   "type": "usage"
  },
  {
   "a": "drinking water",
   "explain": "پینے کا پانی = drinking water.",
   "id": "ur-73",
   "lesson": "home",
   "level": "beginner",
   "opts": [
    "drinking water",
    "milk",
    "oil",
    "fire"
   ],
   "q": "پینے کا پانی means…",
   "topic": "home",
   "type": "vocab"
  },
  {
   "a": "go to sleep",
   "explain": "سونے جائیے — سونا = to sleep.",
   "id": "ur-74",
   "lesson": "home",
   "level": "beginner",
   "opts": [
    "go to sleep",
    "wake up",
    "sit down",
    "come here"
   ],
   "q": "'سونے جائیے' means…",
   "topic": "home",
   "type": "meaning"
  },
  {
   "a": "festival",
   "explain": "تیوہار (teohar) = festival.",
   "id": "ur-75",
   "lesson": "festivals",
   "level": "beginner",
   "opts": [
    "festival",
    "fast",
    "fair",
    "temple"
   ],
   "q": "تیوہار means…",
   "topic": "festivals",
   "type": "vocab"
  },
  {
   "a": "عید",
   "explain": "عید (eid) — the festival of joy!",
   "id": "ur-76",
   "lesson": "festivals",
   "level": "beginner",
   "opts": [
    "عید",
    "شب برات",
    "محرم",
    "دیوالی"
   ],
   "q": "Which is 'Eid'?",
   "topic": "festivals",
   "type": "vocab"
  },
  {
   "a": "happy festival!",
   "explain": "تیوہار مبارک! — مبارک = blessed.",
   "id": "ur-77",
   "lesson": "festivals",
   "level": "beginner",
   "opts": [
    "happy festival!",
    "happy journey!",
    "good morning!",
    "welcome home!"
   ],
   "q": "'تیوہار مبارک!' means…",
   "topic": "festivals",
   "type": "meaning"
  },
  {
   "a": "مٹھائی کھائیے",
   "explain": "مٹھائی کھائیے — مٹھائی = sweets.",
   "id": "ur-78",
   "lesson": "festivals",
   "level": "elementary",
   "opts": [
    "مٹھائی کھائیے",
    "کھانا کھائیے",
    "پانی پیجیے",
    "چائے پیجیے"
   ],
   "q": "Offer guests sweets. You say…",
   "topic": "festivals",
   "type": "usage"
  },
  {
   "a": "mosque",
   "explain": "مسجد (masjid) = mosque.",
   "id": "ur-79",
   "lesson": "festivals",
   "level": "beginner",
   "opts": [
    "mosque",
    "shrine",
    "temple",
    "church"
   ],
   "q": "مسجد means…",
   "topic": "festivals",
   "type": "vocab"
  },
  {
   "a": "holy night",
   "explain": "شب برات (shab-e-barat) — the night of blessings!",
   "id": "ur-80",
   "lesson": "festivals",
   "level": "elementary",
   "opts": [
    "holy night",
    "Diwali",
    "Holi",
    "Dussehra"
   ],
   "q": "شب برات is…",
   "topic": "festivals",
   "type": "vocab"
  },
  {
   "a": "light the lamp",
   "explain": "دیا جلائیے — دیا = lamp.",
   "id": "ur-81",
   "lesson": "festivals",
   "level": "elementary",
   "opts": [
    "light the lamp",
    "close the door",
    "cook the food",
    "ring the bell"
   ],
   "q": "'دیا جلائیے' means…",
   "topic": "festivals",
   "type": "meaning"
  },
  {
   "a": "مسجد جائیے",
   "explain": "مسجد جائیے — مسجد = mosque.",
   "id": "ur-82",
   "lesson": "festivals",
   "level": "elementary",
   "opts": [
    "مسجد جائیے",
    "گھر جائیے",
    "دکان جائیے",
    "اسکول جائیے"
   ],
   "q": "Say 'go to the mosque'. You say…",
   "topic": "festivals",
   "type": "usage"
  },
  {
   "a": "song of praise",
   "explain": "نعت (naat) — praise of the Prophet!",
   "id": "ur-83",
   "lesson": "festivals",
   "level": "beginner",
   "opts": [
    "song of praise",
    "fast",
    "fair",
    "song"
   ],
   "q": "نعت means…",
   "topic": "festivals",
   "type": "vocab"
  },
  {
   "a": "sweets",
   "explain": "مٹھائی (mithai) = sweets.",
   "id": "ur-84",
   "lesson": "festivals",
   "level": "beginner",
   "opts": [
    "sweets",
    "fruits",
    "flowers",
    "clothes"
   ],
   "q": "مٹھائی means…",
   "topic": "festivals",
   "type": "vocab"
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

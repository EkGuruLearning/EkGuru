/* =========================================================
   EkGuru — HINDI QUIZ BANK  (single source of truth · v1)
   ---------------------------------------------------------
   Canonical quiz data for the Hindi learning product:

     · Lesson quick quizzes (build-hindi-quizzes.py injects each
       lesson's questions into its page as <details> self-checks).
     · The topic quiz (/learn/hindi/practice/quiz/) filters this
       same bank by topic + level, so nothing can drift apart.

   Every question is derived from its own lesson and carries a
   short correct answer (`a`), four options (one equals `a`), and
   an explanation. Answers are conservative, checked Hindi — the
   same policy as the practice bank.

   The data object below is deliberately valid JSON so build
   tools and tests can parse it without executing JavaScript.
   ========================================================= */
window.EKGURU_HINDI_QUIZ =
{
  "version": 2,
  "questions": [
    {
      "id": "alpha-1",
      "lesson": "hindi-alphabet-for-beginners",
      "type": "meaning",
      "topic": "basics",
      "level": "beginner",
      "q": "How many letters are there in the Devanagari alphabet?",
      "a": "44",
      "opts": [
        "26",
        "33",
        "44",
        "52"
      ],
      "explain": "44 — each with one sound. That finite size is why the alphabet comes first: once you know the letters you can read anything."
    },
    {
      "id": "alpha-2",
      "lesson": "hindi-alphabet-for-beginners",
      "type": "usage",
      "topic": "basics",
      "level": "beginner",
      "q": "Why is the alphabet the right place to start, before vocabulary?",
      "a": "Hindi is phonetic and finite",
      "opts": [
        "Hindi words are short",
        "Hindi is phonetic and finite",
        "Hindi has no grammar",
        "Hindi is written in English letters"
      ],
      "explain": "Because Hindi is phonetic and finite. Two or three weeks on the letters and you can sound out any word, which makes vocabulary easier, not harder."
    },
    {
      "id": "alpha-3",
      "lesson": "hindi-alphabet-for-beginners",
      "type": "vocab",
      "topic": "basics",
      "level": "beginner",
      "q": "What does the guide give you to help the letters stick?",
      "a": "A printable chart and a learning order",
      "opts": [
        "A printable chart and a learning order",
        "A list of 500 words",
        "Recordings of a native speaker",
        "A monthly test"
      ],
      "explain": "A printable chart and the order to learn the letters in — pin the chart up and work through the letters in that order."
    },
    {
      "id": "hello-1",
      "lesson": "how-to-say-hello-in-hindi",
      "type": "usage",
      "topic": "conversation",
      "level": "beginner",
      "q": "Is namaste always the right greeting?",
      "a": "No — sometimes it is the wrong word",
      "opts": [
        "Yes, in every situation",
        "No — sometimes it is the wrong word",
        "Only after sunset",
        "Only with strangers"
      ],
      "explain": "No — it is sometimes the wrong word. Which greeting to use changes by time of day, age, religion and situation."
    },
    {
      "id": "hello-2",
      "lesson": "how-to-say-hello-in-hindi",
      "type": "translit",
      "topic": "conversation",
      "level": "beginner",
      "q": "Which of these is a time-of-day greeting?",
      "a": "सुप्रभात (suprabhat)",
      "opts": [
        "नमस्ते (namaste)",
        "सुप्रभात (suprabhat)",
        "धन्यवाद (dhanyavaad)",
        "फिर मिलेंगे (phir milenge)"
      ],
      "explain": "सुप्रभात (suprabhat) — good morning. Namaste is general; suprabhat is only for the morning."
    },
    {
      "id": "hello-3",
      "lesson": "how-to-say-hello-in-hindi",
      "type": "usage",
      "topic": "conversation",
      "level": "beginner",
      "q": "What matters more than the greeting itself?",
      "a": "The follow-up question",
      "opts": [
        "The follow-up question",
        "Your accent",
        "Shaking hands",
        "Speaking quickly"
      ],
      "explain": "The follow-up question — asking how the person is — which matters more than which greeting you opened with."
    },
    {
      "id": "sent-1",
      "lesson": "hindi-sentence-structure",
      "type": "grammar",
      "topic": "grammar",
      "level": "beginner",
      "q": "Where does the verb go in a Hindi sentence?",
      "a": "At the end",
      "opts": [
        "At the start",
        "At the end",
        "In the middle",
        "Wherever you like"
      ],
      "explain": "At the end — Hindi is subject-object-verb, so the action is the last thing you hear."
    },
    {
      "id": "sent-2",
      "lesson": "hindi-sentence-structure",
      "type": "grammar",
      "topic": "grammar",
      "level": "beginner",
      "q": "What does Hindi use instead of English prepositions like “in” and “on”?",
      "a": "Postpositions",
      "opts": [
        "Prepositions",
        "Postpositions",
        "Prefixes",
        "Suffixes"
      ],
      "explain": "Postpositions — small words that go AFTER the noun, not before it."
    },
    {
      "id": "sent-3",
      "lesson": "hindi-sentence-structure",
      "type": "grammar",
      "topic": "grammar",
      "level": "beginner",
      "q": "Why do Hindi sentences feel “backwards” at first?",
      "a": "Because the verb comes last",
      "opts": [
        "Because the verb comes last",
        "Because nouns come first",
        "Because it is written right to left",
        "Because of the script"
      ],
      "explain": "Because the verb comes last, so you wait for the whole sentence before you know the action."
    },
    {
      "id": "aap-1",
      "lesson": "aap-tum-tu-hindi",
      "type": "usage",
      "topic": "conversation",
      "level": "elementary",
      "q": "How many words for “you” does Hindi have?",
      "a": "Three",
      "opts": [
        "One",
        "Two",
        "Three",
        "Four"
      ],
      "explain": "Three — आप (aap, respectful), तुम (tum, familiar) and तू (tu, intimate)."
    },
    {
      "id": "aap-2",
      "lesson": "aap-tum-tu-hindi",
      "type": "usage",
      "topic": "conversation",
      "level": "elementary",
      "q": "Which word for “you” is the safe default with strangers?",
      "a": "आप (aap)",
      "opts": [
        "तू (tu)",
        "तुम (tum)",
        "आप (aap)",
        "None of them"
      ],
      "explain": "आप (aap) is the respectful default; तुम (tum) is for friends and तू (tu) for very close intimates."
    },
    {
      "id": "aap-3",
      "lesson": "aap-tum-tu-hindi",
      "type": "usage",
      "topic": "conversation",
      "level": "elementary",
      "q": "What can choosing the wrong “you” do?",
      "a": "Sound genuinely rude",
      "opts": [
        "Sound genuinely rude",
        "Cause a grammar error only",
        "Change the meaning to “we”",
        "Nothing in Hindi"
      ],
      "explain": "Choosing wrong can be genuinely rude — the three words carry real social weight."
    },
    {
      "id": "mis-1",
      "lesson": "common-hindi-mistakes",
      "type": "usage",
      "topic": "grammar",
      "level": "elementary",
      "q": "Where do the mistakes in this guide come from?",
      "a": "What actually goes wrong in lessons",
      "opts": [
        "What actually goes wrong in lessons",
        "Textbooks",
        "Old Sanskrit rules",
        "Native speakers"
      ],
      "explain": "The list is written from what actually goes wrong in lessons, not from a textbook."
    },
    {
      "id": "mis-2",
      "lesson": "common-hindi-mistakes",
      "type": "grammar",
      "topic": "grammar",
      "level": "elementary",
      "q": "Why do learners find Hindi gender hard?",
      "a": "English nouns have no gender",
      "opts": [
        "English nouns have no gender",
        "Hindi has no gender",
        "Gender is optional",
        "Only verbs have gender"
      ],
      "explain": "English nouns carry no gender, so remembering that every Hindi noun is masculine or feminine is a new habit."
    },
    {
      "id": "mis-3",
      "lesson": "common-hindi-mistakes",
      "type": "usage",
      "topic": "grammar",
      "level": "elementary",
      "q": "What marks a learner out fastest?",
      "a": "The small repeated errors",
      "opts": [
        "A slow vocabulary",
        "The small repeated errors",
        "An imperfect accent",
        "Short sentences"
      ],
      "explain": "The errors that mark you out as a learner are the small, repeated ones — and each has a fix."
    },
    {
      "id": "days-1",
      "lesson": "hindi-days-months-time",
      "type": "vocab",
      "topic": "time-dates",
      "level": "beginner",
      "q": "Which half-hour words confuse every learner?",
      "a": "Dhai and saadhe",
      "opts": [
        "Ek and do",
        "Dhai and saadhe",
        "Subah and shaam",
        "Aaj and kal"
      ],
      "explain": "ढाई (dhai, 2½) and साढ़े (saadhe, half past) — the half-hour words that confuse every learner."
    },
    {
      "id": "days-2",
      "lesson": "hindi-days-months-time",
      "type": "vocab",
      "topic": "time-dates",
      "level": "beginner",
      "q": "Which day is रविवार (ravivaar)?",
      "a": "Sunday",
      "opts": [
        "Monday",
        "Saturday",
        "Sunday",
        "Friday"
      ],
      "explain": "रविवार (ravivaar) is Sunday — named after Ravi, the sun."
    },
    {
      "id": "days-3",
      "lesson": "hindi-days-months-time",
      "type": "vocab",
      "topic": "time-dates",
      "level": "beginner",
      "q": "Which day is सोमवार (somvaar)?",
      "a": "Monday",
      "opts": [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday"
      ],
      "explain": "सोमवार (somvaar) is Monday — from som, the moon."
    },
    {
      "id": "fam-1",
      "lesson": "hindi-family-words",
      "type": "vocab",
      "topic": "vocabulary",
      "level": "beginner",
      "q": "What is your father's younger brother called?",
      "a": "चाचा (chaacha)",
      "opts": [
        "चाचा (chaacha)",
        "दादा (daada)",
        "नाना (naana)",
        "भाई (bhaai)"
      ],
      "explain": "चाचा (chaacha) is father's younger brother; ताऊ (taau) is father's older brother."
    },
    {
      "id": "fam-2",
      "lesson": "hindi-family-words",
      "type": "vocab",
      "topic": "vocabulary",
      "level": "beginner",
      "q": "What is your mother's brother called?",
      "a": "मामा (maama)",
      "opts": [
        "मामा (maama)",
        "चाचा (chaacha)",
        "ताऊ (taau)",
        "दादा (daada)"
      ],
      "explain": "मामा (maama) is mother's brother."
    },
    {
      "id": "fam-3",
      "lesson": "hindi-family-words",
      "type": "usage",
      "topic": "vocabulary",
      "level": "beginner",
      "q": "Why is family vocabulary harder in Hindi than English?",
      "a": "Hindi splits relations English lumps together",
      "opts": [
        "Hindi splits relations English lumps together",
        "Hindi has fewer words",
        "Hindi borrows from English",
        "Hindi uses numbers for relatives"
      ],
      "explain": "Hindi splits relations English lumps together — like the two kinds of uncle — which is why there are more words to learn."
    },
    {
      "id": "gen-1",
      "lesson": "hindi-gender-masculine-feminine",
      "type": "grammar",
      "topic": "grammar",
      "level": "beginner",
      "q": "What changes with the speaker's own gender?",
      "a": "The verb",
      "opts": [
        "The verb",
        "The noun",
        "The word order",
        "Nothing"
      ],
      "explain": "Every Hindi noun is masculine or feminine, and the verb changes with the speaker's own gender."
    },
    {
      "id": "gen-2",
      "lesson": "hindi-gender-masculine-feminine",
      "type": "grammar",
      "topic": "grammar",
      "level": "beginner",
      "q": "Are all Hindi nouns gendered?",
      "a": "Yes — every noun is masculine or feminine",
      "opts": [
        "Yes — every noun is masculine or feminine",
        "No, only people",
        "Only animals",
        "Only objects"
      ],
      "explain": "Every Hindi noun is masculine or feminine — there is no neuter."
    },
    {
      "id": "gen-3",
      "lesson": "hindi-gender-masculine-feminine",
      "type": "grammar",
      "topic": "grammar",
      "level": "beginner",
      "q": "What helps you guess a noun's gender?",
      "a": "The ending patterns",
      "opts": [
        "The ending patterns",
        "Its length",
        "Its first letter",
        "Whether it is written in Devanagari"
      ],
      "explain": "Ending patterns — like -आ (-aa) often masculine and -ई (-ii) often feminine — let you guess most nouns."
    },
    {
      "id": "num-1",
      "lesson": "hindi-numbers-1-to-100",
      "type": "vocab",
      "topic": "numbers",
      "level": "beginner",
      "q": "Why are Hindi numbers hard to learn?",
      "a": "They are genuinely irregular",
      "opts": [
        "They are genuinely irregular",
        "They are all the same",
        "They are written in English",
        "There are too many of them"
      ],
      "explain": "Hindi numbers are genuinely irregular, unlike most languages."
    },
    {
      "id": "num-2",
      "lesson": "hindi-numbers-1-to-100",
      "type": "vocab",
      "topic": "numbers",
      "level": "beginner",
      "q": "What is 11 in Hindi?",
      "a": "ग्यारह (gyaarah)",
      "opts": [
        "ग्यारह (gyaarah)",
        "इक्कीस (ikkees)",
        "दस (das)",
        "सौ (sau)"
      ],
      "explain": "ग्यारह (gyaarah) is 11; दस (das) is 10."
    },
    {
      "id": "num-3",
      "lesson": "hindi-numbers-1-to-100",
      "type": "vocab",
      "topic": "numbers",
      "level": "beginner",
      "q": "What is 100 in Hindi?",
      "a": "सौ (sau)",
      "opts": [
        "सौ (sau)",
        "दस (das)",
        "हज़ार (hazaar)",
        "बीस (bees)"
      ],
      "explain": "सौ (sau) is 100; हज़ार (hazaar) is 1,000."
    },
    {
      "id": "urdu-1",
      "lesson": "hindi-or-urdu-difference",
      "type": "meaning",
      "topic": "daily-life",
      "level": "elementary",
      "q": "Can Hindi and Urdu speakers understand each other?",
      "a": "Yes — completely in everyday speech",
      "opts": [
        "Yes — completely in everyday speech",
        "No, never",
        "Only in writing",
        "Only in formal settings"
      ],
      "explain": "Hindi and Urdu speakers understand each other completely in everyday speech, yet the languages are treated as separate."
    },
    {
      "id": "urdu-2",
      "lesson": "hindi-or-urdu-difference",
      "type": "meaning",
      "topic": "daily-life",
      "level": "elementary",
      "q": "What is the biggest visible difference between them?",
      "a": "The script",
      "opts": [
        "The script",
        "The grammar",
        "The word order",
        "The speakers"
      ],
      "explain": "Hindi is written in Devanagari and Urdu in a Perso-Arabic script; the spoken everyday language is very close."
    },
    {
      "id": "urdu-3",
      "lesson": "hindi-or-urdu-difference",
      "type": "vocab",
      "topic": "daily-life",
      "level": "elementary",
      "q": "Where do the two vocabularies differ most?",
      "a": "Formal and literary words",
      "opts": [
        "Formal and literary words",
        "Everyday words",
        "Numbers",
        "Family words"
      ],
      "explain": "Formal and literary Hindi draws on Sanskrit while formal Urdu draws on Persian and Arabic; everyday words overlap heavily."
    },
    {
      "id": "trav-1",
      "lesson": "hindi-phrases-for-travel",
      "type": "vocab",
      "topic": "travel",
      "level": "beginner",
      "q": "What situations do the 50 phrases cover?",
      "a": "Bargaining, autos, trains, food, being unwell",
      "opts": [
        "Bargaining, autos, trains, food, being unwell",
        "Office meetings",
        "Wedding ceremonies",
        "Court proceedings"
      ],
      "explain": "Bargaining, autos, trains, food and being unwell — the situations that genuinely matter when travelling in India."
    },
    {
      "id": "trav-2",
      "lesson": "hindi-phrases-for-travel",
      "type": "translit",
      "topic": "travel",
      "level": "beginner",
      "q": "Which phrase means “how much is this?”",
      "a": "यह कितने का है? (yah kitne ka hai?)",
      "opts": [
        "यह कितने का है? (yah kitne ka hai?)",
        "आप कैसे हैं? (aap kaise hain?)",
        "मुझे नहीं पता (mujhe nahin pata)",
        "फिर मिलेंगे (phir milenge)"
      ],
      "explain": "यह कितने का है? (yah kitne ka hai?) is “how much is this?” — the bargaining essential."
    },
    {
      "id": "trav-3",
      "lesson": "hindi-phrases-for-travel",
      "type": "usage",
      "topic": "travel",
      "level": "beginner",
      "q": "Why do numbers matter as much as phrases when you travel?",
      "a": "For bargaining prices",
      "opts": [
        "For bargaining prices",
        "For telling the date",
        "For reading signs",
        "For ordering coffee"
      ],
      "explain": "Prices are negotiated aloud, so numbers matter as much as phrases when you bargain."
    },
    {
      "id": "verb-1",
      "lesson": "hindi-verbs-present-past-future",
      "type": "grammar",
      "topic": "grammar",
      "level": "elementary",
      "q": "Which rule “catches everyone”?",
      "a": "The ne rule",
      "opts": [
        "The ne rule",
        "The ki rule",
        "The se rule",
        "The ka rule"
      ],
      "explain": "The ने (ne) rule — the ergative marker that appears with certain past-tense verbs — catches everyone."
    },
    {
      "id": "verb-2",
      "lesson": "hindi-verbs-present-past-future",
      "type": "grammar",
      "topic": "grammar",
      "level": "elementary",
      "q": "What do you need to conjugate a Hindi verb correctly?",
      "a": "Who is speaking, gender and tense",
      "opts": [
        "Who is speaking, gender and tense",
        "Only the tense",
        "Only the gender",
        "Only the subject's age"
      ],
      "explain": "The verb ending depends on who is speaking, their gender and the tense."
    },
    {
      "id": "verb-3",
      "lesson": "hindi-verbs-present-past-future",
      "type": "vocab",
      "topic": "grammar",
      "level": "elementary",
      "q": "What does करना (karnaa) mean?",
      "a": "To do",
      "opts": [
        "To do",
        "To be",
        "To go",
        "To eat"
      ],
      "explain": "करना (karnaa) means “to do” — the root verb used to build many others."
    },
    {
      "id": "bolly-1",
      "lesson": "learn-hindi-from-bollywood",
      "type": "usage",
      "topic": "daily-life",
      "level": "elementary",
      "q": "Is Bollywood a good way to learn Hindi?",
      "a": "Yes — with the right films and method",
      "opts": [
        "Yes — with the right films and method",
        "No, never",
        "Only for grammar",
        "Only for writing"
      ],
      "explain": "Films are a genuinely good way to learn Hindi, if you pick the right ones and use them properly."
    },
    {
      "id": "bolly-2",
      "lesson": "learn-hindi-from-bollywood",
      "type": "usage",
      "topic": "daily-life",
      "level": "elementary",
      "q": "What is the risk of learning from films alone?",
      "a": "Picking up unreal, dramatised speech",
      "opts": [
        "Picking up unreal, dramatised speech",
        "Learning perfect formal Hindi",
        "Learning only written Hindi",
        "Learning no vocabulary"
      ],
      "explain": "Film dialogue is written for drama — songs and dramatic lines are not everyday speech."
    },
    {
      "id": "bolly-3",
      "lesson": "learn-hindi-from-bollywood",
      "type": "usage",
      "topic": "daily-life",
      "level": "elementary",
      "q": "What should you pair films with?",
      "a": "Real conversation or structured study",
      "opts": [
        "Real conversation or structured study",
        "More films only",
        "Memorising songs",
        "Reading English subtitles only"
      ],
      "explain": "Films help most when paired with real conversation or structured study, so you learn which lines are actually used."
    },
    {
      "id": "guide-1",
      "lesson": "learn-hindi-online-guide",
      "type": "meaning",
      "topic": "basics",
      "level": "beginner",
      "q": "What does this guide honestly compare?",
      "a": "Apps, YouTube, textbooks and tutors",
      "opts": [
        "Apps, YouTube, textbooks and tutors",
        "Only apps",
        "Only tutors",
        "Only free resources"
      ],
      "explain": "A frank comparison of every way to learn Hindi online — apps, YouTube, textbooks and a tutor."
    },
    {
      "id": "guide-2",
      "lesson": "learn-hindi-online-guide",
      "type": "usage",
      "topic": "basics",
      "level": "beginner",
      "q": "What does the guide say about “learn Hindi in 30 days” promises?",
      "a": "They are unrealistic",
      "opts": [
        "They are unrealistic",
        "They are accurate",
        "They apply to grammar only",
        "They apply to children only"
      ],
      "explain": "The guide is frank that real fluency takes consistent months-to-years of work, not a month."
    },
    {
      "id": "guide-3",
      "lesson": "learn-hindi-online-guide",
      "type": "usage",
      "topic": "basics",
      "level": "beginner",
      "q": "Which real option does the guide compare?",
      "a": "One-to-one tutoring",
      "opts": [
        "One-to-one tutoring",
        "Hiring a translator",
        "A paid relocation to India",
        "Only free textbooks"
      ],
      "explain": "The guide compares one-to-one tutoring, apps, YouTube and textbooks for what each is genuinely good for."
    },
    {
      "id": "name-1",
      "lesson": "write-your-name-in-hindi",
      "type": "usage",
      "topic": "pronunciation",
      "level": "beginner",
      "q": "What does this guide help you do?",
      "a": "Write any English name in Devanagari",
      "opts": [
        "Write any English name in Devanagari",
        "Speak with a native accent",
        "Translate your name's meaning",
        "Learn calligraphy"
      ],
      "explain": "Write any English name in Devanagari, letter by letter."
    },
    {
      "id": "name-2",
      "lesson": "write-your-name-in-hindi",
      "type": "meaning",
      "topic": "pronunciation",
      "level": "beginner",
      "q": "What is Devanagari?",
      "a": "The script Hindi is written in",
      "opts": [
        "The script Hindi is written in",
        "A dialect",
        "A grammar rule",
        "A Hindi region"
      ],
      "explain": "Devanagari is the script Hindi is written in — an abugida where consonants carry an inherent “a”."
    },
    {
      "id": "name-3",
      "lesson": "write-your-name-in-hindi",
      "type": "usage",
      "topic": "pronunciation",
      "level": "beginner",
      "q": "Why can't English names always be written exactly?",
      "a": "Hindi writes sounds, not spellings",
      "opts": [
        "Hindi writes sounds, not spellings",
        "Hindi has too few letters",
        "Names are not allowed",
        "Hindi is only spoken"
      ],
      "explain": "Hindi letters represent sounds, so a name is written the way it sounds, not the way it is spelt in English."
    },
    {
      "a": "fever",
      "explain": "बुख़ार (bukhaar) = fever — मुझे बुख़ार है (I have a fever).",
      "id": "hi-25",
      "lesson": "hindi/advanced/health",
      "level": "beginner",
      "opts": [
        "fever",
        "cough",
        "cold",
        "pain"
      ],
      "q": "बुख़ार means…",
      "topic": "health",
      "type": "vocab"
    },
    {
      "a": "डॉक्टर",
      "explain": "डॉक्टर (doctor) = doctor.",
      "id": "hi-26",
      "lesson": "hindi/advanced/health",
      "level": "beginner",
      "opts": [
        "डॉक्टर",
        "नर्स",
        "मरीज़",
        "सर्जन"
      ],
      "q": "Which is 'doctor'?",
      "topic": "health",
      "type": "vocab"
    },
    {
      "a": "I am not feeling well",
      "explain": "मुझे अच्छा नहीं लग रहा — अच्छा = good.",
      "id": "hi-27",
      "lesson": "hindi/advanced/health",
      "level": "beginner",
      "opts": [
        "I am not feeling well",
        "I have a fever",
        "take rest",
        "get well soon"
      ],
      "q": "'मुझे अच्छा नहीं लग रहा' means…",
      "topic": "health",
      "type": "meaning"
    },
    {
      "a": "दवाखाना कहाँ है?",
      "explain": "दवाखाना कहाँ है? — कहाँ = where.",
      "id": "hi-28",
      "lesson": "hindi/advanced/health",
      "level": "elementary",
      "opts": [
        "दवाखाना कहाँ है?",
        "अस्पताल कहाँ है?",
        "डॉक्टर कहाँ है?",
        "घर कहाँ है?"
      ],
      "q": "Ask where the pharmacy is. You say…",
      "topic": "health",
      "type": "usage"
    },
    {
      "a": "heart",
      "explain": "दिल (dil) = heart.",
      "id": "hi-29",
      "lesson": "hindi/advanced/health",
      "level": "beginner",
      "opts": [
        "heart",
        "lung",
        "stomach",
        "liver"
      ],
      "q": "दिल means…",
      "topic": "health",
      "type": "vocab"
    },
    {
      "a": "medical diet",
      "explain": "परहेज़ (parhez) — the doctor's diet rules.",
      "id": "hi-30",
      "lesson": "hindi/advanced/health",
      "level": "elementary",
      "opts": [
        "medical diet",
        "home remedy",
        "herbal medicine",
        "first aid"
      ],
      "q": "परहेज़ means…",
      "topic": "health",
      "type": "vocab"
    },
    {
      "a": "get well soon",
      "explain": "जल्दी ठीक हो जाइए — जल्दी = soon.",
      "id": "hi-31",
      "lesson": "hindi/advanced/health",
      "level": "elementary",
      "opts": [
        "get well soon",
        "take rest",
        "drink hot water",
        "call a doctor"
      ],
      "q": "'जल्दी ठीक हो जाइए' means…",
      "topic": "health",
      "type": "meaning"
    },
    {
      "a": "मुँह खोलिए",
      "explain": "मुँह खोलिए = open your mouth — मुँह = mouth.",
      "id": "hi-32",
      "lesson": "hindi/advanced/health",
      "level": "elementary",
      "opts": [
        "मुँह खोलिए",
        "आँखें बंद कीजिए",
        "हाथ बढ़ाइए",
        "खड़े हो जाइए"
      ],
      "q": "The doctor says 'open your mouth'. She says…",
      "topic": "health",
      "type": "usage"
    },
    {
      "a": "injection",
      "explain": "टीका (teeka) — injection; सूई = needle.",
      "id": "hi-33",
      "lesson": "hindi/advanced/health",
      "level": "beginner",
      "opts": [
        "injection",
        "tablet",
        "syrup",
        "ointment"
      ],
      "q": "टीका means…",
      "topic": "health",
      "type": "vocab"
    },
    {
      "a": "take rest",
      "explain": "आराम कीजिए — आराम = rest.",
      "id": "hi-34",
      "lesson": "hindi/advanced/health",
      "level": "beginner",
      "opts": [
        "take rest",
        "wake up",
        "breathe deeply",
        "walk daily"
      ],
      "q": "'आराम कीजिए' means…",
      "topic": "health",
      "type": "meaning"
    },
    {
      "a": "salary",
      "explain": "वेतन (vetan) = salary; दिहाड़ी = daily wages.",
      "id": "hi-35",
      "lesson": "hindi/advanced/office",
      "level": "beginner",
      "opts": [
        "salary",
        "bonus",
        "loan",
        "bill"
      ],
      "q": "वेतन means…",
      "topic": "office",
      "type": "vocab"
    },
    {
      "a": "कंप्यूटर",
      "explain": "कंप्यूटर = computer.",
      "id": "hi-36",
      "lesson": "hindi/advanced/office",
      "level": "beginner",
      "opts": [
        "कंप्यूटर",
        "लैपटॉप",
        "टेलीफ़ोन",
        "प्रिंटर"
      ],
      "q": "Which is 'computer'?",
      "topic": "office",
      "type": "vocab"
    },
    {
      "a": "arrive on time",
      "explain": "समय पर आइए — समय = time.",
      "id": "hi-37",
      "lesson": "hindi/advanced/office",
      "level": "beginner",
      "opts": [
        "arrive on time",
        "come tomorrow",
        "wait a little",
        "work fast"
      ],
      "q": "'समय पर आइए' means…",
      "topic": "office",
      "type": "meaning"
    },
    {
      "a": "कल मुझे छुट्टी चाहिए",
      "explain": "कल मुझे छुट्टी चाहिए — चाहिए = need.",
      "id": "hi-38",
      "lesson": "hindi/advanced/office",
      "level": "elementary",
      "opts": [
        "कल मुझे छुट्टी चाहिए",
        "आज मुझे छुट्टी चाहिए",
        "कल मुझे काम चाहिए",
        "मुझे आज आना है"
      ],
      "q": "Say you need leave tomorrow. You say…",
      "topic": "office",
      "type": "usage"
    },
    {
      "a": "signature",
      "explain": "दस्तख़त (dastakhat) = signature.",
      "id": "hi-39",
      "lesson": "hindi/advanced/office",
      "level": "beginner",
      "opts": [
        "signature",
        "seal",
        "form",
        "report"
      ],
      "q": "दस्तख़त means…",
      "topic": "office",
      "type": "vocab"
    },
    {
      "a": "ज़ेरॉक्स",
      "explain": "ज़ेरॉक्स = photocopy.",
      "id": "hi-40",
      "lesson": "hindi/advanced/office",
      "level": "elementary",
      "opts": [
        "ज़ेरॉक्स",
        "प्रिंटर",
        "स्कैनर",
        "फ़ाइल"
      ],
      "q": "Which is 'photocopy'?",
      "topic": "office",
      "type": "vocab"
    },
    {
      "a": "the work is done",
      "explain": "काम ख़त्म हुआ — ख़त्म = finished.",
      "id": "hi-41",
      "lesson": "hindi/advanced/office",
      "level": "beginner",
      "opts": [
        "the work is done",
        "the work is left",
        "start the work",
        "leave the work"
      ],
      "q": "'काम ख़त्म हुआ' means…",
      "topic": "office",
      "type": "meaning"
    },
    {
      "a": "ईमेल भेजिए",
      "explain": "ईमेल भेजिए = send the email — भेजना = to send.",
      "id": "hi-42",
      "lesson": "hindi/advanced/office",
      "level": "elementary",
      "opts": [
        "ईमेल भेजिए",
        "ईमेल पढ़िए",
        "फ़ोन कीजिए",
        "चिट्ठी लिखिए"
      ],
      "q": "Say 'send the email'. You say…",
      "topic": "office",
      "type": "usage"
    },
    {
      "a": "leave",
      "explain": "छुट्टी (chhutti) — leave; कल मुझे छुट्टी चाहिए.",
      "id": "hi-43",
      "lesson": "hindi/advanced/office",
      "level": "beginner",
      "opts": [
        "leave",
        "overtime",
        "salary",
        "promotion"
      ],
      "q": "छुट्टी means…",
      "topic": "office",
      "type": "vocab"
    },
    {
      "a": "well done!",
      "explain": "शाबाश! — praise for good work.",
      "id": "hi-44",
      "lesson": "hindi/advanced/office",
      "level": "beginner",
      "opts": [
        "well done!",
        "sorry!",
        "wait!",
        "hurry!"
      ],
      "q": "'शाबाश!' means…",
      "topic": "office",
      "type": "meaning"
    },
    {
      "a": "teacher (male)",
      "explain": "शिक्षक (shikshak) — male teacher; शिक्षिका — female.",
      "id": "hi-45",
      "lesson": "hindi/advanced/education",
      "level": "beginner",
      "opts": [
        "teacher (male)",
        "teacher (female)",
        "student",
        "principal"
      ],
      "q": "शिक्षक means…",
      "topic": "education",
      "type": "vocab"
    },
    {
      "a": "नई किताब",
      "explain": "नई किताब = new book — नई = new (feminine).",
      "id": "hi-46",
      "lesson": "hindi/advanced/education",
      "level": "beginner",
      "opts": [
        "नई किताब",
        "पुरानी किताब",
        "नई कॉपी",
        "कहानी की किताब"
      ],
      "q": "Which is 'new book'?",
      "topic": "education",
      "type": "vocab"
    },
    {
      "a": "read aloud",
      "explain": "ज़ोर से पढ़िए — ज़ोर से = loudly.",
      "id": "hi-47",
      "lesson": "hindi/advanced/education",
      "level": "beginner",
      "opts": [
        "read aloud",
        "read silently",
        "write neatly",
        "listen carefully"
      ],
      "q": "'ज़ोर से पढ़िए' means…",
      "topic": "education",
      "type": "meaning"
    },
    {
      "a": "मुझे नहीं मालूम",
      "explain": "मुझे नहीं मालूम = I don't know.",
      "id": "hi-48",
      "lesson": "hindi/advanced/education",
      "level": "elementary",
      "opts": [
        "मुझे नहीं मालूम",
        "मुझे मालूम है",
        "मुझे पढ़ना है",
        "मुझे जाना है"
      ],
      "q": "Say 'I don't know'. You say…",
      "topic": "education",
      "type": "usage"
    },
    {
      "a": "exam",
      "explain": "परीक्षा (pariksha) = exam.",
      "id": "hi-49",
      "lesson": "hindi/advanced/education",
      "level": "beginner",
      "opts": [
        "exam",
        "result",
        "question paper",
        "answer sheet"
      ],
      "q": "परीक्षा means…",
      "topic": "education",
      "type": "vocab"
    },
    {
      "a": "स्लेट",
      "explain": "स्लेट = slate (writing board).",
      "id": "hi-50",
      "lesson": "hindi/advanced/education",
      "level": "elementary",
      "opts": [
        "स्लेट",
        "श्यामपट्ट",
        "डस्टर",
        "कॉपी"
      ],
      "q": "Which is 'slate'?",
      "topic": "education",
      "type": "vocab"
    },
    {
      "a": "study well",
      "explain": "अच्छी तरह पढ़िए — अच्छी तरह = well.",
      "id": "hi-51",
      "lesson": "hindi/advanced/education",
      "level": "beginner",
      "opts": [
        "study well",
        "play well",
        "eat well",
        "sleep well"
      ],
      "q": "'अच्छी तरह पढ़िए' means…",
      "topic": "education",
      "type": "meaning"
    },
    {
      "a": "अपनी किताबें खोलिए",
      "explain": "अपनी किताबें खोलिए = open your books.",
      "id": "hi-52",
      "lesson": "hindi/advanced/education",
      "level": "elementary",
      "opts": [
        "अपनी किताबें खोलिए",
        "अपनी किताबें बंद कीजिए",
        "अपनी कॉपी खोलिए",
        "अपना बस्ता खोलिए"
      ],
      "q": "Say 'open your books'. You say…",
      "topic": "education",
      "type": "usage"
    },
    {
      "a": "student",
      "explain": "छात्र (chhaatra) = student.",
      "id": "hi-53",
      "lesson": "hindi/advanced/education",
      "level": "beginner",
      "opts": [
        "student",
        "teacher",
        "class",
        "lesson"
      ],
      "q": "छात्र means…",
      "topic": "education",
      "type": "vocab"
    },
    {
      "a": "passing marks",
      "explain": "पास अंक — the minimum marks to pass.",
      "id": "hi-54",
      "lesson": "hindi/advanced/education",
      "level": "elementary",
      "opts": [
        "passing marks",
        "full marks",
        "first rank",
        "gold medal"
      ],
      "q": "पास अंक means…",
      "topic": "education",
      "type": "vocab"
    },
    {
      "a": "weather",
      "explain": "मौसम (mausam) = weather — आज मौसम कैसा है?",
      "id": "hi-55",
      "lesson": "hindi/advanced/weather",
      "level": "beginner",
      "opts": [
        "weather",
        "season",
        "climate",
        "forecast"
      ],
      "q": "मौसम means…",
      "topic": "weather",
      "type": "vocab"
    },
    {
      "a": "बारिश",
      "explain": "बारिश = rain; बूँदाबाँदी = drizzle.",
      "id": "hi-56",
      "lesson": "hindi/advanced/weather",
      "level": "beginner",
      "opts": [
        "बारिश",
        "बाढ़",
        "सूखा",
        "कोहरा"
      ],
      "q": "Which is 'rain'?",
      "topic": "weather",
      "type": "vocab"
    },
    {
      "a": "it is very hot",
      "explain": "बहुत गर्मी है — बहुत = very.",
      "id": "hi-57",
      "lesson": "hindi/advanced/weather",
      "level": "beginner",
      "opts": [
        "it is very hot",
        "it is very cold",
        "it is raining",
        "it is windy"
      ],
      "q": "'बहुत गर्मी है' means…",
      "topic": "weather",
      "type": "meaning"
    },
    {
      "a": "छाता ले लीजिए",
      "explain": "छाता ले लीजिए = take the umbrella.",
      "id": "hi-58",
      "lesson": "hindi/advanced/weather",
      "level": "elementary",
      "opts": [
        "छाता ले लीजिए",
        "छाता दे दीजिए",
        "कंबल ले लीजिए",
        "स्वेटर पहनिए"
      ],
      "q": "Say 'take the umbrella'. You say…",
      "topic": "weather",
      "type": "usage"
    },
    {
      "a": "sun",
      "explain": "सूरज (suraj) = sun.",
      "id": "hi-59",
      "lesson": "hindi/advanced/weather",
      "level": "beginner",
      "opts": [
        "sun",
        "moon",
        "star",
        "sky"
      ],
      "q": "सूरज means…",
      "topic": "weather",
      "type": "vocab"
    },
    {
      "a": "मानसून",
      "explain": "मानसून = monsoon (the rains).",
      "id": "hi-60",
      "lesson": "hindi/advanced/weather",
      "level": "elementary",
      "opts": [
        "मानसून",
        "बरसात",
        "बसंत",
        "पतझड़"
      ],
      "q": "Which is 'monsoon'?",
      "topic": "weather",
      "type": "vocab"
    },
    {
      "a": "the sun has risen",
      "explain": "सूरज निकला — निकलना = to come out.",
      "id": "hi-61",
      "lesson": "hindi/advanced/weather",
      "level": "elementary",
      "opts": [
        "the sun has risen",
        "the sun has set",
        "the moon is out",
        "it is noon"
      ],
      "q": "'सूरज निकला' means…",
      "topic": "weather",
      "type": "meaning"
    },
    {
      "a": "शाम को मिलेंगे",
      "explain": "शाम को मिलेंगे = we will meet in the evening.",
      "id": "hi-62",
      "lesson": "hindi/advanced/weather",
      "level": "elementary",
      "opts": [
        "शाम को मिलेंगे",
        "सुबह मिलेंगे",
        "कल मिलेंगे",
        "यहाँ मिलेंगे"
      ],
      "q": "Say 'we will meet in the evening'. You say…",
      "topic": "weather",
      "type": "usage"
    },
    {
      "a": "cold",
      "explain": "ठंड (thand) = cold.",
      "id": "hi-63",
      "lesson": "hindi/advanced/weather",
      "level": "beginner",
      "opts": [
        "cold",
        "heat",
        "wind",
        "fog"
      ],
      "q": "ठंड means…",
      "topic": "weather",
      "type": "vocab"
    },
    {
      "a": "इंद्रधनुष",
      "explain": "इंद्रधनुष = rainbow.",
      "id": "hi-64",
      "lesson": "hindi/advanced/weather",
      "level": "elementary",
      "opts": [
        "इंद्रधनुष",
        "बिजली",
        "गरज",
        "ओस"
      ],
      "q": "Which is 'rainbow'?",
      "topic": "weather",
      "type": "vocab"
    },
    {
      "a": "biryani",
      "explain": "बिरयानी (biryani) = biryani.",
      "id": "hi-65",
      "lesson": "hindi/advanced/home",
      "level": "beginner",
      "opts": [
        "biryani",
        "pulao",
        "khichdi",
        "curd rice"
      ],
      "q": "बिरयानी means…",
      "topic": "home",
      "type": "vocab"
    },
    {
      "a": "अपना घर",
      "explain": "अपना घर — अपना = one's own.",
      "id": "hi-66",
      "lesson": "hindi/advanced/home",
      "level": "beginner",
      "opts": [
        "अपना घर",
        "नया घर",
        "बड़ा घर",
        "पुराना घर"
      ],
      "q": "Which is 'one's own home'?",
      "topic": "home",
      "type": "vocab"
    },
    {
      "a": "the food is ready",
      "explain": "खाना तैयार है — तैयार = ready.",
      "id": "hi-67",
      "lesson": "hindi/advanced/home",
      "level": "beginner",
      "opts": [
        "the food is ready",
        "the food is hot",
        "the food is tasty",
        "the food is left"
      ],
      "q": "'खाना तैयार है' means…",
      "topic": "home",
      "type": "meaning"
    },
    {
      "a": "हाथ धोइए",
      "explain": "हाथ धोइए = wash your hands.",
      "id": "hi-68",
      "lesson": "hindi/advanced/home",
      "level": "elementary",
      "opts": [
        "हाथ धोइए",
        "मुँह धोइए",
        "बरतन धोइए",
        "कपड़े धोइए"
      ],
      "q": "Say 'wash your hands'. You say…",
      "topic": "home",
      "type": "usage"
    },
    {
      "a": "door",
      "explain": "दरवाज़ा (darvaaza) = door; खिड़की = window.",
      "id": "hi-69",
      "lesson": "hindi/advanced/home",
      "level": "beginner",
      "opts": [
        "door",
        "window",
        "wall",
        "roof"
      ],
      "q": "दरवाज़ा means…",
      "topic": "home",
      "type": "vocab"
    },
    {
      "a": "गरम चावल",
      "explain": "गरम चावल — गरम = hot; चावल = rice.",
      "id": "hi-70",
      "lesson": "hindi/advanced/home",
      "level": "elementary",
      "opts": [
        "गरम चावल",
        "गरम दाल",
        "ठंडा पानी",
        "गरम चाय"
      ],
      "q": "Which is 'hot rice'?",
      "topic": "home",
      "type": "vocab"
    },
    {
      "a": "it is very tasty!",
      "explain": "बहुत स्वादिष्ट है! — स्वादिष्ट = tasty.",
      "id": "hi-71",
      "lesson": "hindi/advanced/home",
      "level": "beginner",
      "opts": [
        "it is very tasty!",
        "it is very hot!",
        "it is very sweet!",
        "it is very little!"
      ],
      "q": "'बहुत स्वादिष्ट है!' means…",
      "topic": "home",
      "type": "meaning"
    },
    {
      "a": "दरवाज़ा बंद कीजिए",
      "explain": "दरवाज़ा बंद कीजिए = close the door.",
      "id": "hi-72",
      "lesson": "hindi/advanced/home",
      "level": "elementary",
      "opts": [
        "दरवाज़ा बंद कीजिए",
        "दरवाज़ा खोलिए",
        "खिड़की बंद कीजिए",
        "दरवाज़ा देखिए"
      ],
      "q": "Say 'close the door'. You say…",
      "topic": "home",
      "type": "usage"
    },
    {
      "a": "drinking water",
      "explain": "पीने का पानी = drinking water.",
      "id": "hi-73",
      "lesson": "hindi/advanced/home",
      "level": "beginner",
      "opts": [
        "drinking water",
        "cold water",
        "hot water",
        "coconut water"
      ],
      "q": "पीने का पानी means…",
      "topic": "home",
      "type": "vocab"
    },
    {
      "a": "सोने जाइए",
      "explain": "सोने जाइए = go to sleep.",
      "id": "hi-74",
      "lesson": "hindi/advanced/home",
      "level": "elementary",
      "opts": [
        "सोने जाइए",
        "खाने जाइए",
        "नहाने जाइए",
        "घूमने जाइए"
      ],
      "q": "Say 'go to sleep'. You say…",
      "topic": "home",
      "type": "usage"
    },
    {
      "a": "festival",
      "explain": "त्यौहार (tyauhaar) = festival.",
      "id": "hi-75",
      "lesson": "hindi/advanced/festivals",
      "level": "beginner",
      "opts": [
        "festival",
        "fast",
        "fair",
        "wedding"
      ],
      "q": "त्यौहार means…",
      "topic": "festivals",
      "type": "vocab"
    },
    {
      "a": "दीवाली",
      "explain": "दीवाली = Diwali, the festival of lamps.",
      "id": "hi-76",
      "lesson": "hindi/advanced/festivals",
      "level": "beginner",
      "opts": [
        "दीवाली",
        "दशहरा",
        "होली",
        "ईद"
      ],
      "q": "Which is 'Diwali'?",
      "topic": "festivals",
      "type": "vocab"
    },
    {
      "a": "happy festival!",
      "explain": "त्यौहार मुबारक! — मुबारक = blessed.",
      "id": "hi-77",
      "lesson": "hindi/advanced/festivals",
      "level": "beginner",
      "opts": [
        "happy festival!",
        "happy birthday!",
        "happy journey!",
        "good night!"
      ],
      "q": "'त्यौहार मुबारक!' means…",
      "topic": "festivals",
      "type": "meaning"
    },
    {
      "a": "मिठाई खाइए",
      "explain": "मिठाई खाइए = eat sweets.",
      "id": "hi-78",
      "lesson": "hindi/advanced/festivals",
      "level": "elementary",
      "opts": [
        "मिठाई खाइए",
        "मिठाई बाँटिए",
        "खाना खाइए",
        "प्रसाद लीजिए"
      ],
      "q": "Say 'eat sweets'. You say…",
      "topic": "festivals",
      "type": "usage"
    },
    {
      "a": "temple",
      "explain": "मंदिर (mandir) = temple; मस्जिद = mosque.",
      "id": "hi-79",
      "lesson": "hindi/advanced/festivals",
      "level": "beginner",
      "opts": [
        "temple",
        "mosque",
        "church",
        "fair"
      ],
      "q": "मंदिर means…",
      "topic": "festivals",
      "type": "vocab"
    },
    {
      "a": "नवरात्रि",
      "explain": "नवरात्रि — nine nights of the goddess.",
      "id": "hi-80",
      "lesson": "hindi/advanced/festivals",
      "level": "elementary",
      "opts": [
        "नवरात्रि",
        "शिवरात्रि",
        "जन्माष्टमी",
        "राम नवमी"
      ],
      "q": "Which is the nine-night festival?",
      "topic": "festivals",
      "type": "vocab"
    },
    {
      "a": "light the lamp",
      "explain": "दीया जलाइए — जलाना = to light.",
      "id": "hi-81",
      "lesson": "hindi/advanced/festivals",
      "level": "beginner",
      "opts": [
        "light the lamp",
        "burst crackers",
        "tie the rakhi",
        "offer flowers"
      ],
      "q": "'दीया जलाइए' means…",
      "topic": "festivals",
      "type": "meaning"
    },
    {
      "a": "मंदिर जाइए",
      "explain": "मंदिर जाइए = go to the temple.",
      "id": "hi-82",
      "lesson": "hindi/advanced/festivals",
      "level": "elementary",
      "opts": [
        "मंदिर जाइए",
        "मस्जिद जाइए",
        "मेले में जाइए",
        "घर जाइए"
      ],
      "q": "Say 'go to the temple'. You say…",
      "topic": "festivals",
      "type": "usage"
    },
    {
      "a": "devotional song",
      "explain": "भजन (bhajan) = devotional song.",
      "id": "hi-83",
      "lesson": "hindi/advanced/festivals",
      "level": "elementary",
      "opts": [
        "devotional song",
        "film song",
        "folk dance",
        "wedding march"
      ],
      "q": "भजन means…",
      "topic": "festivals",
      "type": "vocab"
    },
    {
      "a": "मिठाई",
      "explain": "मिठाई = sweets.",
      "id": "hi-84",
      "lesson": "hindi/advanced/festivals",
      "level": "beginner",
      "opts": [
        "मिठाई",
        "प्रसाद",
        "चढ़ावा",
        "भोग"
      ],
      "q": "Which is 'sweets'?",
      "topic": "festivals",
      "type": "vocab"
    }
  ]
};

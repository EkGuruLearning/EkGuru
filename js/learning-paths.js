/* =========================================================
   EkGuru — LEARNING PATHS  (single source of truth · v100)
   ---------------------------------------------------------
   Six goal-based paths built from EXISTING guides, tools,
   daily-hindi days and practice labs. Nothing here invents a
   page: every lesson URL must already exist or the admin gap
   engine flags it. Path pages (learn/paths/<slug>/) render
   their module list from this file; the progress tracker and
   the admin Learning Ops panel read the same data.

   A path is: goal → level → modules → lessons → practice →
   quiz → review → completion → next step. No dead ends: each
   path ends in `next` (or "done") and every module's lessons
   resolve to a real page.
   ========================================================= */
window.EKGURU_PATHS = [
  {
    slug: "hindi-from-zero",
    title: "Hindi From Zero",
    tagline: "The complete beginner track, in the order that actually works.",
    level: "Complete beginner",
    duration: "6–8 hours of focused study",
    goal: "Go from knowing nothing to reading Devanagari and holding a short scripted conversation.",
    intro: [
      "Most people quit Hindi because they start in the wrong place — memorising words before they can read the letters those words are made of. This path starts with the script, adds only the phrases you can use in week one, and brings in grammar after you have words to hang it on.",
      "Work through the modules top to bottom. Each lesson links to a guide you read once and a tool or practice lab you repeat. Mark lessons done as you go; your progress is saved in this browser and never leaves it."
    ],
    modules: [
      {
        title: "The script — read anything in Hindi",
        lessons: [
          { title: "The Hindi alphabet, explained", url: "/learn/hindi-alphabet-for-beginners/", kind: "guide", minutes: 20 },
          { title: "Practise the letters with the alphabet explorer", url: "/toolbox/hindi-alphabet/", kind: "tool", minutes: 15 },
          { title: "Write your own name in Devanagari", url: "/learn/write-your-name-in-hindi/", kind: "guide", minutes: 15 },
          { title: "Type it: your first Devanagari words", url: "/toolbox/hindi-typing/", kind: "tool", minutes: 10 }
        ]
      },
      {
        title: "First words — say something to a person",
        lessons: [
          { title: "How to say hello (and when namaste is wrong)", url: "/learn/how-to-say-hello-in-hindi/", kind: "guide", minutes: 10 },
          { title: "Numbers 1 to 100", url: "/learn/hindi-numbers-1-to-100/", kind: "guide", minutes: 20 },
          { title: "Days, months and telling the time", url: "/learn/hindi-days-months-time/", kind: "guide", minutes: 15 },
          { title: "Vocabulary drill: first 30 words", url: "/learn/practice/vocabulary/", kind: "practice", minutes: 10 }
        ]
      },
      {
        title: "How Hindi actually works",
        lessons: [
          { title: "Word order — why the verb goes last", url: "/learn/hindi-sentence-structure/", kind: "guide", minutes: 15 },
          { title: "Gender — why the verb changes with who is speaking", url: "/learn/hindi-gender-masculine-feminine/", kind: "guide", minutes: 15 },
          { title: "Verbs in the present, past and future", url: "/learn/hindi-verbs-present-past-future/", kind: "guide", minutes: 20 },
          { title: "Build your first sentences", url: "/learn/practice/sentence-builder/", kind: "practice", minutes: 10 }
        ]
      },
      {
        title: "Politeness and the mistakes that mark you out",
        lessons: [
          { title: "Aap, tum or tu — getting politeness right", url: "/learn/aap-tum-tu-hindi/", kind: "guide", minutes: 10 },
          { title: "The 10 mistakes every learner makes", url: "/learn/common-hindi-mistakes/", kind: "guide", minutes: 15 },
          { title: "Verb endings drill", url: "/learn/practice/verbs/", kind: "practice", minutes: 10 }
        ]
      }
    ],
    practice: [
      { title: "Flashcards — the words you keep forgetting", url: "/toolbox/hindi-flashcards/", kind: "tool" },
      { title: "Ten-question quiz", url: "/toolbox/hindi-quiz/", kind: "quiz" }
    ],
    quiz: { title: "Check where you are with the level test", url: "/toolbox/hindi-level-test/", note: "A rough self-check, not a certified placement." },
    review: { title: "Review what is getting wobbly", url: "/learn/practice/review/" },
    next: "speaking-starter",
    completion: "You can read Devanagari, introduce yourself, count, and build simple present-tense sentences."
  },
  {
    slug: "speaking-starter",
    title: "Speaking Starter",
    tagline: "Stop studying. Start saying things out loud.",
    level: "Beginner — knows some words",
    duration: "3–4 hours",
    goal: "Produce real spoken sentences from day one, however slowly.",
    intro: [
      "Reading teaches you the grammar; speaking teaches you the language. This path is deliberately light on new rules and heavy on producing sound: greetings, self-introductions, and the sentence frames that cover half of everyday talk.",
      "The speaking practice here is honest. A web page cannot judge your accent — it gives you phrases to shadow and a playback voice to compare against. The real check is a patient native speaker, which is what the tutors are for."
    ],
    modules: [
      {
        title: "Greet and introduce",
        lessons: [
          { title: "How to say hello in Hindi", url: "/learn/how-to-say-hello-in-hindi/", kind: "guide", minutes: 10 },
          { title: "Aap, tum or tu — the politeness that matters", url: "/learn/aap-tum-tu-hindi/", kind: "guide", minutes: 10 },
          { title: "Pronunciation: the sounds English doesn't have", url: "/toolbox/hindi-pronunciation/", kind: "tool", minutes: 15 },
          { title: "Shadowing drill (minimal pairs)", url: "/learn/practice/pronunciation/", kind: "practice", minutes: 10 }
        ]
      },
      {
        title: "Say something useful",
        lessons: [
          { title: "50 travel phrases people actually use", url: "/learn/hindi-phrases-for-travel/", kind: "guide", minutes: 20 },
          { title: "Phrasebook with search", url: "/toolbox/hindi-phrasebook/", kind: "tool", minutes: 10 },
          { title: "Family words — the twelve cousins", url: "/learn/hindi-family-words/", kind: "guide", minutes: 10 },
          { title: "Listening: hear it, choose it", url: "/learn/practice/listening/", kind: "practice", minutes: 10 }
        ]
      },
      {
        title: "Put words in the right order",
        lessons: [
          { title: "Word order — why the verb goes last", url: "/learn/hindi-sentence-structure/", kind: "guide", minutes: 15 },
          { title: "Sentence builder practice", url: "/learn/practice/sentence-builder/", kind: "practice", minutes: 10 }
        ]
      }
    ],
    practice: [
      { title: "Daily practice — five minutes a day", url: "/learn/practice/daily/", kind: "practice" },
      { title: "Flashcards", url: "/toolbox/hindi-flashcards/", kind: "tool" }
    ],
    quiz: { title: "Level test", url: "/toolbox/hindi-level-test/", note: "A rough self-check, not a certified placement." },
    review: { title: "Review", url: "/learn/practice/review/" },
    next: "everyday-hindi",
    completion: "You can introduce yourself, ask simple questions, and speak short sentences without translating every word first."
  },
  {
    slug: "reading-hindi",
    title: "Reading Hindi",
    tagline: "From first letters to reading signs and short texts.",
    level: "Beginner — no script knowledge needed",
    duration: "4–5 hours",
    goal: "Read Devanagari confidently enough to sound out any word and read short real-world texts.",
    intro: [
      "Devanagari is phonetic and finite: forty-four letters, each with one sound. Two or three focused weeks and you can read anything — this path compresses that into a few sessions.",
      "Reading is the one skill a page can genuinely help you build, because it is visual. Work the alphabet, then move from single words to sentences, and check yourself against the numbers and signs around you."
    ],
    modules: [
      {
        title: "The letters",
        lessons: [
          { title: "The Hindi alphabet, explained", url: "/learn/hindi-alphabet-for-beginners/", kind: "guide", minutes: 20 },
          { title: "Alphabet explorer — click every letter", url: "/toolbox/hindi-alphabet/", kind: "tool", minutes: 20 },
          { title: "The vowels and matras", url: "/daily-hindi/day-10/", kind: "daily", minutes: 10 }
        ]
      },
      {
        title: "Sound out real words",
        lessons: [
          { title: "Your first words — day 12 of Daily Hindi", url: "/daily-hindi/day-12/", kind: "daily", minutes: 10 },
          { title: "Reading drill in the listening lab (read the Devanagari)", url: "/learn/practice/listening/", kind: "practice", minutes: 10 },
          { title: "Type it yourself", url: "/toolbox/hindi-typing/", kind: "tool", minutes: 15 }
        ]
      },
      {
        title: "Numbers, time and the world around you",
        lessons: [
          { title: "Numbers 1 to 100", url: "/learn/hindi-numbers-1-to-100/", kind: "guide", minutes: 20 },
          { title: "Days, months and telling the time", url: "/learn/hindi-days-months-time/", kind: "guide", minutes: 15 },
          { title: "Numbers tool — sound out any number", url: "/toolbox/hindi-numbers/", kind: "tool", minutes: 10 }
        ]
      }
    ],
    practice: [
      { title: "Flashcards", url: "/toolbox/hindi-flashcards/", kind: "tool" },
      { title: "Vocabulary drill", url: "/learn/practice/vocabulary/", kind: "practice" }
    ],
    quiz: { title: "Level test", url: "/toolbox/hindi-level-test/", note: "A rough self-check, not a certified placement." },
    review: { title: "Review", url: "/learn/practice/review/" },
    next: "hindi-from-zero",
    completion: "You can read any Devanagari word aloud, slowly, and recognise common signs and numbers."
  },
  {
    slug: "travel-hindi",
    title: "Travel Hindi",
    tagline: "The phrases that get you fed, housed and pointed the right way.",
    level: "Beginner — useful with zero grammar",
    duration: "2–3 hours",
    goal: "Handle the situations a traveller actually meets: food, directions, shopping, prices, and emergencies.",
    intro: [
      "You do not need grammar to travel — you need the right phrases and the nerve to say them. This path is situational: each module covers one place a visitor ends up, with the exact words that work there.",
      "Bargaining, autos, trains, food and being unwell — these are the phrases written by people who use them, not copied from a phrasebook. Practise each set before you need it."
    ],
    modules: [
      {
        title: "Essentials",
        lessons: [
          { title: "How to say hello (and when namaste is wrong)", url: "/learn/how-to-say-hello-in-hindi/", kind: "guide", minutes: 10 },
          { title: "50 travel phrases people actually use", url: "/learn/hindi-phrases-for-travel/", kind: "guide", minutes: 20 },
          { title: "Phrasebook with search", url: "/toolbox/hindi-phrasebook/", kind: "tool", minutes: 10 }
        ]
      },
      {
        title: "Food, shopping and directions",
        lessons: [
          { title: "Food and restaurant phrases", url: "/learn/practice/listening/", kind: "practice", minutes: 10 },
          { title: "Topic vocabulary — food and travel", url: "/toolbox/hindi-vocabulary/", kind: "tool", minutes: 10 },
          { title: "Numbers 1 to 100 (prices)", url: "/learn/hindi-numbers-1-to-100/", kind: "guide", minutes: 15 }
        ]
      },
      {
        title: "Time and money",
        lessons: [
          { title: "Days, months and telling the time", url: "/learn/hindi-days-months-time/", kind: "guide", minutes: 15 },
          { title: "Numbers tool — sound out any price", url: "/toolbox/hindi-numbers/", kind: "tool", minutes: 10 }
        ]
      }
    ],
    practice: [
      { title: "Flashcards — the phrases you keep needing", url: "/toolbox/hindi-flashcards/", kind: "tool" },
      { title: "Daily practice", url: "/learn/practice/daily/", kind: "practice" }
    ],
    quiz: { title: "Ten-question quiz", url: "/toolbox/hindi-quiz/", note: "Recognition only — a quiz can't test a conversation." },
    review: { title: "Review", url: "/learn/practice/review/" },
    next: "everyday-hindi",
    completion: "You can order food, ask prices, take directions and handle common travel situations with phrases."
  },
  {
    slug: "everyday-hindi",
    title: "Everyday Hindi",
    tagline: "Small talk, plans, opinions — the language of normal days.",
    level: "High beginner",
    duration: "4–5 hours",
    goal: "Hold a short everyday conversation: how you are, what you did, what you want.",
    intro: [
      "Travel phrases get you through a trip; everyday Hindi gets you through a friendship. This path builds the conversational core: asking how someone is, talking about time and plans, and saying what you think.",
      "It assumes you can already read the script and form a basic sentence. If not, do Hindi From Zero or Reading Hindi first — this path leans on those."
    ],
    modules: [
      {
        title: "Small talk",
        lessons: [
          { title: "How are you — and the aap problem", url: "/daily-hindi/day-5/", kind: "daily", minutes: 10 },
          { title: "Family words — the twelve cousins", url: "/learn/hindi-family-words/", kind: "guide", minutes: 10 },
          { title: "Aap, tum or tu", url: "/learn/aap-tum-tu-hindi/", kind: "guide", minutes: 10 }
        ]
      },
      {
        title: "Time and plans",
        lessons: [
          { title: "Days, months and telling the time", url: "/learn/hindi-days-months-time/", kind: "guide", minutes: 15 },
          { title: "Verbs — present, past and future", url: "/learn/hindi-verbs-present-past-future/", kind: "guide", minutes: 20 },
          { title: "Verb endings drill", url: "/learn/practice/verbs/", kind: "practice", minutes: 10 }
        ]
      },
      {
        title: "Say what you think",
        lessons: [
          { title: "Word order — why the verb goes last", url: "/learn/hindi-sentence-structure/", kind: "guide", minutes: 15 },
          { title: "Sentence builder practice", url: "/learn/practice/sentence-builder/", kind: "practice", minutes: 10 },
          { title: "Grammar practice (gender and agreement)", url: "/learn/practice/grammar/", kind: "practice", minutes: 10 }
        ]
      }
    ],
    practice: [
      { title: "Daily practice", url: "/learn/practice/daily/", kind: "practice" },
      { title: "Flashcards", url: "/toolbox/hindi-flashcards/", kind: "tool" }
    ],
    quiz: { title: "Level test", url: "/toolbox/hindi-level-test/", note: "A rough self-check, not a certified placement." },
    review: { title: "Review", url: "/learn/practice/review/" },
    next: "grammar-foundations",
    completion: "You can talk about your day, your plans and your opinions in simple, correct sentences."
  },
  {
    slug: "grammar-foundations",
    title: "Grammar Foundations",
    tagline: "The rules that stop people guessing.",
    level: "High beginner to intermediate",
    duration: "4–6 hours",
    goal: "Understand and use Hindi word order, gender, agreement and tenses reliably.",
    intro: [
      "Grammar is not the enemy of speaking — it is what makes the sentences you produce actually mean what you think they mean. This path concentrates the rules that carry the most weight: word order, gender agreement, and verbs.",
      "Each rule is read once, then drilled. The drills are multiple-choice and fill-in — they test recognition and recall of forms, not conversation, and they say so."
    ],
    modules: [
      {
        title: "Structure",
        lessons: [
          { title: "Word order — why the verb goes last", url: "/learn/hindi-sentence-structure/", kind: "guide", minutes: 15 },
          { title: "Gender — why the verb changes with who is speaking", url: "/learn/hindi-gender-masculine-feminine/", kind: "guide", minutes: 15 },
          { title: "Grammar practice", url: "/learn/practice/grammar/", kind: "practice", minutes: 10 }
        ]
      },
      {
        title: "Verbs and tense",
        lessons: [
          { title: "Verbs — present, past and future", url: "/learn/hindi-verbs-present-past-future/", kind: "guide", minutes: 20 },
          { title: "Verb explorer — the first twenty", url: "/toolbox/hindi-verbs/", kind: "tool", minutes: 10 },
          { title: "Verb endings drill", url: "/learn/practice/verbs/", kind: "practice", minutes: 10 }
        ]
      },
      {
        title: "Precision",
        lessons: [
          { title: "Aap, tum or tu", url: "/learn/aap-tum-tu-hindi/", kind: "guide", minutes: 10 },
          { title: "The 10 mistakes every learner makes", url: "/learn/common-hindi-mistakes/", kind: "guide", minutes: 15 },
          { title: "Sentence builder practice", url: "/learn/practice/sentence-builder/", kind: "practice", minutes: 10 }
        ]
      }
    ],
    practice: [
      { title: "Daily practice", url: "/learn/practice/daily/", kind: "practice" },
      { title: "Flashcards", url: "/toolbox/hindi-flashcards/", kind: "tool" }
    ],
    quiz: { title: "Level test", url: "/toolbox/hindi-level-test/", note: "A rough self-check, not a certified placement." },
    review: { title: "Review", url: "/learn/practice/review/" },
    next: null,
    completion: "You can form correct sentences across tenses with the right gender and politeness level. There is no next path — this is the end of the core tracks. Keep the forms fresh with daily practice, or use a tutor to make them automatic in speech."
  }
];

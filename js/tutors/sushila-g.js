/* =========================================================
   EkGuru — TUTOR FILE
   ---------------------------------------------------------
   This file holds EVERYTHING for one tutor and nothing else.
   Editing it can never affect any other tutor.

   ⚠️  Do not rename the file without also updating:
         · the "id" below
         · js/tutors/_registry.js
         · the <script> tag in every HTML page

   QUICK MAP — what changes what
   ---------------------------------------------------------
     priceUSD     the number shown on the card, the profile,
                  the sidebar, the booking window and Google
     photo/thumb  square portrait  (500x500 or larger)
     banner       wide cover strip (1280x720), "" for none
     youtubeId    ONLY the id from the YouTube link
     email        where THIS tutor's enquiries go
     whatsapp     "+919876543210" turns their green buttons on,
                  "" hides them completely
     availability the clickable slots in their booking window
     reviews      keep rating + reviewsCount in sync with this
   ========================================================= */

ekguruTutor({
  /* ===== IDENTITY — SUSHILA ONLY =====================================
     id  : ⛔ NEVER CHANGE — this is her page address (tutor.html?id=sushila-g).
           Changing it breaks every existing link to her profile.
     Everything else here is safe to edit and affects only her.
     ================================================================ */
  id: "sushila-g",                    // unique, lowercase. URL: tutor.html?id=sushila-g
  name: "Sushila G.",
  nickname: "Sashi",
  headline: "Friendly Hindi Tutor — Speak, Read & Write with Confidence",
  subject: "Hindi",
  country: "India",
  countryFlag: "🇮🇳",
  city: "Rajasthan, India",
  timezone: "IST (GMT+5:30)",

  /* ===== IMAGES & VIDEO — SUSHILA ONLY ===============================
     photo  : square portrait, 500x500 or larger. Round picture on her profile.
     thumb  : the small picture on her card. Same file is fine.
     banner : wide 16:9 cover strip, 1280x720. "" = no banner.
     youtubeId : ONLY the ID. https://youtu.be/Ykic7gkyHjg -> "Ykic7gkyHjg"
     ================================================================ */
  photo: "images/sushila.jpg",
  thumb: "images/sushila.jpg",
  banner: "",                         // no banner yet — add a 1280x720 image here
  youtubeId: "Ykic7gkyHjg",           // https://youtu.be/Ykic7gkyHjg
  videoTitle: "Hindi Tutor Intro",

  /* ===== NUMBERS & PRICE — SUSHILA ONLY ==============================
     priceUSD : ← HER price. Number only, no "$". Updates her card, her
                profile, her sidebar, her booking window and Google.
     rating / reviewsCount : must match the reviews list at the bottom.
     verified   : true = blue tick on her photo
     superTutor : true = gold Super Tutor chip beside her name
     ================================================================ */
  rating: 5.0,
  reviewsCount: 3,
  lessonsCount: 40,
  priceUSD: 3,
  lessonLength: "50 min",
  experienceYears: 3,
  trialAvailable: true,
  verified: true,
  superTutor: true,

  /* ===== EXTERNAL LINK — SUSHILA ONLY ================================
     preplyUrl : her booking page elsewhere. "" hides the button.
     ================================================================ */
  preplyUrl: "https://preply.com/en/tutor/7717290",

  /* ===== CONTACT — SUSHILA ONLY =====================================
     These belong to THIS tutor. Changing them affects only Sushila's
     profile — Hemlata and Tara keep their own.

     email    : where HER enquiries and booking requests are sent.
                Put her personal address here to receive them directly,
                e.g. "sushila.hindi@gmail.com"
                Leave the shared EkGuru address and YOU receive them
                and forward them on.

     whatsapp : ""            -> her WhatsApp buttons stay hidden
                "+919876543210" -> green WhatsApp buttons appear on her
                card, her profile and inside her booking window, each
                opening a chat with the message already written.
                Country code required. No spaces or dashes.
     ================================================================ */
  email: "EkGuruLearning@gmail.com",   // ← SUSHILA's email
  whatsapp: "",                        // ← SUSHILA's WhatsApp

  /* ===== CONTENT — SUSHILA ONLY ===================================== */
  tags: ["Patient", "Engaging", "Approachable", "Adaptable"],
  teaches: [
    "Hindi for beginners",
    "Conversational Hindi",
    "Hindi grammar",
    "Devanagari reading & writing",
    "Hindi for kids",
    "Pronunciation training"
  ],
  levels: ["Beginner", "Intermediate", "Advanced"],
  speaks: [
    { lang: "Hindi", level: "Native" },
    { lang: "English", level: "Upper-Intermediate B2" }
  ],

  about: [
    "Hello! My name is Sashi, and I am a passionate Hindi tutor. I love teaching Hindi and helping students learn in an easy, fun and effective way. I have experience working with learners of every level, whether you are a complete beginner or looking to improve your fluency.",
    "In my classes I focus on speaking skills, grammar, vocabulary and correct pronunciation. I always adapt my teaching style to each student's needs, so that learning stays simple and genuinely enjoyable.",
    "My interests include reading, learning new languages, listening to music and exploring different cultures. I enjoy connecting with people and sharing knowledge. If you are interested in learning Hindi, I would be happy to guide you on your journey."
  ],

  experience: [
    "Helped complete beginners build a strong Hindi foundation, from the Devanagari alphabet to everyday conversation.",
    "Guided intermediate learners to noticeably improve their speaking, reading and writing.",
    "Taught students from many different countries and cultural backgrounds.",
    "Student-centred, interactive methodology: real-life conversation plus step-by-step grammar.",
    "Provides practice materials and regular feedback so progress is easy to track.",
    "Lessons tailored to each goal — conversational Hindi, academic study or general fluency."
  ],

  methodology: [
    { title: "Speak from day one", desc: "You start speaking in your very first lesson, so hesitation disappears early." },
    { title: "Step-by-step grammar", desc: "Grammar is broken into small pieces and taught with clear, practical examples." },
    { title: "Real-life practice", desc: "Dialogues built around markets, travel, family and work — language you will actually use." },
    { title: "Homework & feedback", desc: "Practice material after every class, plus personal feedback on your progress." }
  ],

  /* ===== WEEKLY SCHEDULE — SUSHILA ONLY ==============================
     These exact times appear as clickable slots in HER booking window,
     automatically converted into each student's own timezone.
     24-hour, two digits ("09:00" not "9:00"). [] = day off.
     ================================================================ */
  availability: {
    Mon: ["09:00", "10:00", "16:00", "18:00", "20:00"],
    Tue: ["09:00", "11:00", "17:00", "19:00"],
    Wed: ["09:00", "10:00", "16:00", "18:00", "20:00"],
    Thu: ["10:00", "12:00", "17:00", "19:00"],
    Fri: ["09:00", "11:00", "16:00", "18:00", "20:00"],
    Sat: ["10:00", "12:00", "15:00"],
    Sun: []
  },

  /* ===== REVIEWS — SUSHILA ONLY ======================================
     Add / edit / delete freely. After changing, update HER rating and
     reviewsCount above so Google's star rating stays honest.
     Format: { name: "...", date: "YYYY-MM-DD", stars: 5, text: "..." }
     ================================================================ */
  reviews: [
    {
      name: "Tomasz",
      date: "2026-07-12",
      stars: 5,
      text: "Sushila is a very patient teacher. She adjusts the tempo to the student's level and the content to his needs, is very calm and helpful. Her pronunciation is very clear and understandable. A lesson with Sushila is a highly enjoyable Hindi experience with lots of new knowledge. Thank you, Sushila!"
    },
    {
      name: "Jon",
      date: "2026-06-19",
      stars: 5,
      text: "Shashi is very patient and maintains a good pace during lessons. She plans the lessons according to my level, and we mostly converse in Hindi. She is a wonderful person with a calm and gentle nature — we even talk about Hindi culture. She is very professional and we share a great rapport. Shashi, you are amazing — thank you!"
    },
    {
      name: "Matthew",
      date: "2026-06-18",
      stars: 5,
      text: "Sushila is well organised, friendly, and most importantly she is patient. She is always fully present in class. She is helping me with my pronunciation, reading and speaking, and it is going well. Classes are fun — we read children's stories and other school material. I look forward to classes and I recommend her as a tutor."
    }
  ]
});

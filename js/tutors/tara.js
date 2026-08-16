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
  /* ===== IDENTITY — TARA ONLY ========================================
     id : ⛔ NEVER CHANGE — this is her page address (tutor.html?id=tara)
     ================================================================ */
  id: "tara",                         // ⛔ DO NOT CHANGE — this is her profile URL
  name: "Tara",                       // EDIT ME: full name, e.g. "Tara M."
  nickname: "",                       // EDIT ME: optional
  headline: "Native Hindi Tutor — Conversation, Grammar & Script for Every Level",
                                      // EDIT ME: her one-line tagline
  subject: "Hindi",
  country: "India",
  countryFlag: "🇮🇳",
  city: "India",                      // EDIT ME: e.g. "Delhi, India"
  timezone: "IST (GMT+5:30)",         // EDIT ME if different

  /* ===== IMAGES & VIDEO — TARA ONLY ==================================
     ⏳ All three are placeholders. When her files arrive:
        1. upload  images/tara.jpg         (square, 500x500+)
        2. upload  images/tara-banner.jpg  (wide, 1280x720)
        3. point the three lines below at them
     ================================================================ */
  photo: "images/placeholder-tutor.jpg",   // EDIT ME -> "images/tara.jpg"
  thumb: "images/placeholder-tutor.jpg",   // EDIT ME -> "images/tara.jpg"
  banner: "",                              // EDIT ME -> "images/tara-banner.jpg"
                                           //   leave "" and her profile simply has no cover strip
  youtubeId: "",                           // EDIT ME: only the ID from her YouTube link
  videoTitle: "Hindi Tutor Intro",         // EDIT ME

  /* ===== NUMBERS & PRICE — TARA ONLY =================================
     ⚠️ Every figure here is a placeholder. priceUSD is the important one.
     ================================================================ */
  rating: 5.0,                        // ← EDIT ME: HER real average
  reviewsCount: 0,                    // ← EDIT ME: must match HER reviews[] below
  lessonsCount: 0,                    // ← EDIT ME: HER total lessons taught
  priceUSD: 8,                        // ← EDIT ME: HER price. Number only, no "$".
  lessonLength: "50 min",             // EDIT ME
  experienceYears: 2,                 // EDIT ME
  trialAvailable: true,
  verified: false,                    // set to true once you have checked her documents
  superTutor: false,

  /* ===== EXTERNAL LINK — TARA ONLY =================================== */
  preplyUrl: "",                      // ← EDIT ME: HER Preply link. "" hides the button.

  /* ===== CONTACT — TARA ONLY ========================================
     ⚠️ EDIT ME. These two lines control TARA's contact only.

     email    : replace with HER personal address, e.g. "tara.hindi@gmail.com"
                All enquiries and booking requests from HER profile go there.

     whatsapp : add her number with the country code, e.g. "+919812345678"
                No spaces, brackets or dashes.
                Leave "" and her WhatsApp buttons stay hidden.
     ================================================================ */
  email: "EkGuruLearning@gmail.com",  // ← EDIT ME: TARA's personal email
  whatsapp: "",                       // ← EDIT ME: TARA's WhatsApp, e.g. "+919812345678"

  /* ---- content ---- */
  tags: ["Native speaker", "Friendly", "Structured", "Encouraging"],
                                      // EDIT ME: 4 style words

  teaches: [                          // EDIT ME
    "Conversational Hindi",
    "Hindi for beginners",
    "Hindi grammar",
    "Devanagari reading & writing"
  ],

  levels: ["Beginner", "Intermediate"],
                                      // EDIT ME: add "Advanced" if she teaches it

  speaks: [                           // EDIT ME
    { lang: "Hindi", level: "Native" },
    { lang: "English", level: "Intermediate B1" }
  ],

  /* EDIT ME — her bio. One string per paragraph. */
  about: [
    "Namaste! I am Tara, a native Hindi speaker and tutor. I enjoy helping students find their confidence in Hindi, whether they are starting from zero or polishing skills they already have.",
    "My lessons balance conversation with clear, structured grammar, so you understand why Hindi works the way it does rather than just repeating phrases.",
    "I keep the atmosphere relaxed and encouraging. Every student learns at a different speed, and my job is to match yours."
  ],

  /* EDIT ME — 3 to 6 bullet points. */
  experience: [
    "Teaches beginners and intermediate learners from a range of countries.",
    "Focuses on practical, everyday Hindi that students can use straight away.",
    "Teaches the Devanagari script step by step, at a comfortable pace.",
    "Sets short practice tasks between lessons to keep progress steady."
  ],

  /* EDIT ME — up to 4 method boxes. */
  methodology: [
    { title: "Conversation first", desc: "Speaking practice in every single lesson, from the very beginning." },
    { title: "Grammar that makes sense", desc: "Rules explained simply, with examples you will actually use." },
    { title: "Steady script practice", desc: "Reading and writing Devanagari built up gradually, never rushed." },
    { title: "Relaxed and encouraging", desc: "A patient space where asking questions is always welcome." }
  ],

  /* ===== WEEKLY SCHEDULE — TARA ONLY =================================
     ⚠️ EDIT ME — placeholder times. These become the clickable slots in
     HER booking window. 24-hour, two digits. [] = day off.
     ================================================================ */
  availability: {
    Mon: ["09:00", "15:00", "19:00"],
    Tue: ["09:00", "15:00"],
    Wed: ["09:00", "15:00", "19:00"],
    Thu: ["09:00", "15:00"],
    Fri: ["09:00", "15:00", "19:00"],
    Sat: ["10:00"],
    Sun: []
  },

  /* ===== REVIEWS — TARA ONLY =========================================
     Add them as they arrive, then update HER rating and reviewsCount.
     ================================================================ */
  reviews: []
});

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
  /* ===== IDENTITY — SARSHTEE ONLY ====================================
     id : ⛔ NEVER CHANGE — this is her page address
          (tutor.html?id=sarshtee-baliyan, /tutor/sarshtee-baliyan/)
     ================================================================ */
  id: "sarshtee-baliyan",             // ⛔ DO NOT CHANGE — this is her profile URL
  name: "Sarshtee Baliyan",           // her full name, as she wrote it
  nickname: "Sarshtee",               // what the booking form calls her
  headline: "Hindi for Children & Beginners — Speaking, Reading and Everyday Talk",
                                      // one line under her name
  subject: "Hindi",
  country: "India",
  countryFlag: "🇮🇳",
  city: "Greater Noida, India",
  timezone: "IST (GMT+5:30)",         // the sheet's format; Asia/Kolkata equivalent

  /* ===== IMAGES & VIDEO — SARSHTEE ONLY ==============================
     ⏳ She has not sent a photo yet, so her card and profile show the
        EkGuru placeholder. When the photo arrives:
          1. save it as  images/sarshtee-baliyan.jpg   (square, 500x500+)
          2. set photo and thumb below to "images/sarshtee-baliyan.jpg"
         The pre-rendered profile picks it up on the next
         `node tools/build-tutor-pages.js`.

     youtubeId: she has no intro video yet. Paste the 11-character id
     from a YouTube link to turn the video section on; "" keeps it off
     (an empty id renders nothing rather than an empty player).
     ================================================================ */
  photo: "images/placeholder-tutor.jpg",   // EDIT ME -> "images/sarshtee-baliyan.jpg"
  thumb: "images/placeholder-tutor.jpg",   // EDIT ME -> "images/sarshtee-baliyan.jpg"
  banner: "",                              // no cover strip until she sends one
  youtubeId: "",                           // no intro video yet
  videoTitle: "Hindi Tutor Intro",

  /* ===== NUMBERS & PRICE — SARSHTEE ONLY =============================
     She quoted "$8–10 to start". The site shows ONE number per tutor,
     so this is her starting price; when she settles on a single rate,
     change it here (and in her sheet row) and rebuild.
     ================================================================ */
  rating: 0,                          // no reviews yet — 0, never a guess
  reviewsCount: 0,
  lessonsCount: 0,
  priceUSD: 8,                        // her starting price per 50-minute lesson
  lessonLength: "50 min",
  experienceYears: 4,                 // ~4 years with children, as a school librarian
  trialAvailable: true,               // she offers a free trial
  verified: false,                    // stays false until her documents are checked
  superTutor: false,                  // set true only with a record that earns it

  /* ===== EXTERNAL LINK — SARSHTEE ONLY ===============================
     She has no Preply profile, so the button stays hidden. */
  preplyUrl: "",

  /* ===== CONTACT — SARSHTEE ONLY ====================================
     ⚠️ Her contact email is NOT written here.

     This repository is public. The site's rule (js/tutors-data.js,
     tools/sheetsync.js) is that a tutor's personal address lives in
     the spreadsheet's `notification_email` column — the private,
     canonical inbox every booking request is delivered to — and
     never in a committed file. Her address is in her sheet row, so
     booking mail reaches her directly while the page stays clean.

     whatsapp: her number is deliberately not published either.
     EkGuru does not print personal mobile numbers (see the note in
     js/tutors-data.js). If she wants WhatsApp buttons on her
     profile, she needs a *business* number and to say so in
     writing; only then does allowPhone:true below become honest.
     ================================================================ */
  email: "",                          // blank = enquiries route via the EkGuru inbox
  whatsapp: "",                       // personal numbers are never published
  // allowPhone: true,                // only with her written consent + a business number

  /* ===== BOOKING EMAIL — SARSHTEE ONLY ==============================
     Every booking request a student sends her is delivered to her
     `notification_email` from the sheet, with a copy to EkGuru and a
     copy back to the student. Nothing to switch on here.

     ⚠️ ONE-TIME: she must activate that address once with the mail
     relay or the first request bounces. Open tools/mail-activate.html,
     press the button on her row, then ask her to click "Activate
     Form" in the email that arrives. Once only, forever.
     ================================================================ */
  formKey: "",                        // optional public alias; "" keeps it simple

  /* ===== CONTENT — SARSHTEE ONLY ==================================== */
  tags: ["Patient", "Kid-friendly", "Friendly", "Interactive"],
                                      // four style words, shown as chips

  badge: "School Librarian",          // the short label on her card

  specialities: [                     // shown on her profile, max 6
    "Kids",
    "Beginners",
    "Conversation",
    "Reading",
    "Vocabulary",
    "Pronunciation"
  ],

  intro: "School librarian and Hindi tutor with four years' experience helping children learn through stories, pictures and everyday conversation.",
                                      // one line at the top of her profile (max 220)

  teaches: [                          // what a student can search her for
    "Hindi for kids",
    "Hindi for beginners",
    "Conversational Hindi",
    "Hindi reading & vocabulary",
    "Pronunciation training",
    "Everyday Hindi sentences"
  ],

  levels: ["Beginner", "Intermediate"],   // she teaches children and beginners
  speaks: [
    { lang: "Hindi", level: "Native" },
    { lang: "English", level: "Fluent" }
  ],

  exams: [],                          // no exam syllabus yet

  /* Her bio — one string per paragraph. Written from what she sent us. */
  about: [
    "Hello! My name is Sarshtee Baliyan, and I am from Greater Noida, India. I am a school librarian with around four years of experience working with children in a school environment.",
    "I enjoy working with children and helping them learn in a simple, friendly and interesting way. I would love to teach Hindi to children and beginners living outside India. My lessons focus on basic Hindi speaking, reading, vocabulary, everyday conversations, pronunciation and simple Hindi sentences.",
    "I believe children learn better when lessons are interactive and enjoyable, so I use stories, pictures, conversations, simple activities and age-appropriate books to make Hindi interesting. Whether your child is from an Indian family living abroad or is completely new to Hindi, I can help them build confidence step by step. My goal is to make Hindi easy, useful and enjoyable for every student."
  ],

  /* Teaching experience — one bullet per line, 3 to 6 of them. */
  experience: [
    "Around four years working with children in a school environment, as a school librarian.",
    "Focus on learning support, reading and educational activities with young learners.",
    "Helps complete beginners with the Hindi alphabet, first words and simple sentences.",
    "Builds vocabulary and pronunciation through picture books, stories and conversation.",
    "Patient, friendly approach designed for children and adults taking their first steps in Hindi."
  ],

  /* How she teaches — up to 4 method boxes. */
  methodology: [
    {
      title: "Stories and pictures",
      desc: "Age-appropriate books, pictures and simple activities, so a child is reading and speaking without noticing they are studying."
    },
    {
      title: "Step by step",
      desc: "Letters and sounds first, then words, then whole sentences — small steps that always feel achievable."
    },
    {
      title: "Speaking from the first lesson",
      desc: "Everyday conversation and correct pronunciation from day one, so confidence grows with the vocabulary."
    },
    {
      title: "Made for young learners",
      desc: "Short, friendly lessons at a calm pace, with plenty of encouragement and room to make mistakes."
    }
  ],

  /* ===== WEEKLY SCHEDULE — SARSHTEE ONLY =============================
     5:00 PM – 9:00 PM IST, Monday to Saturday. These are lesson START
     times, 24-hour, two digits; each lesson runs 50 minutes. [] = day off.
     ================================================================ */
  availability: {
    Mon: ["17:00", "18:00", "19:00", "20:00"],
    Tue: ["17:00", "18:00", "19:00", "20:00"],
    Wed: ["17:00", "18:00", "19:00", "20:00"],
    Thu: ["17:00", "18:00", "19:00", "20:00"],
    Fri: ["17:00", "18:00", "19:00", "20:00"],
    Sat: ["17:00", "18:00", "19:00", "20:00"],
    Sun: []                           // no Sunday lessons
  },

  /* ===== REVIEWS — SARSHTEE ONLY =====================================
     Her first review goes here, then update rating and reviewsCount
     above so the card, the profile and Google agree.
     ================================================================ */
  reviews: []
});

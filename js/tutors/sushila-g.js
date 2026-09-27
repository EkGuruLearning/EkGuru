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
  timezone: "IST (Asia/Kolkata)",

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
  /* ── Marketplace-imported numbers REMOVED (26 Sep 2026) ────────────
     The old values (rating 5.0 / 3 reviews / 40 lessons) described her
     record on an external marketplace, not on EkGuru, and the reviews
     themselves were excerpts copied from that marketplace's website.
     Policy: EkGuru shows only numbers it can verify from its own data.
     No EkGuru lessons have been delivered yet, and no site-native
     review exists — so nothing is claimed. Her external profile stays
     linked below so a student can check her track record there.
     priceUSD now matches the live sheet ($6); the sheet wins anyway,
     this file is only the fallback. ───────────────────────────────── */
  rating: 0,
  reviewsCount: 0,
  lessonsCount: 0,
  priceUSD: 6,
  lessonLength: "50 min",
  experienceYears: 3,
  trialAvailable: true,
  verified: true,
  /* superTutor: the gold chip is not rendered anywhere on the site today,
     and there is no EkGuru record that earns the label — ratings, reviews
     and lessons on EkGuru are all zero. Keep false until a real record
     exists. */
  superTutor: false,

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
  /* v97 — was "EkGuruLearning@gmail.com", the PLATFORM inbox, not
     Sushila's own address. Paste her real personal address (or a
     formKey alias) here; until then her bookings are marked
     TUTOR_EMAIL_UNAVAILABLE and routed via the EkGuru inbox for
     forwarding — honestly reported, never silently faked. */
  email: "",   // ← SUSHILA's email (empty = no direct address on file)
  whatsapp: "",                        // ← SUSHILA's WhatsApp

  /* ===== BOOKING EMAIL — SUSHILA ONLY ==============================
     Every booking request a student sends Sushila goes to the
     address above, with a copy to EkGuru and a copy back to the
     student. That happens automatically — nothing to switch on here.

     ⚠️ ONE-TIME: that address must be activated once with the mail
     relay or the first request will bounce. Open tools/mail-activate.html,
     press the button on Sushila's row, then ask Sushila to click
     "Activate Form" in the email that arrives. Once only, forever.

     formKey : optional. Leave "" and the address above is used, which
     means it appears in the page source where spam bots can read it.
     If Sushila would rather keep it private, get a FormSubmit alias
     (a random string, see tools/mail-activate.html) and paste it here
     instead — bookings still arrive, the address stays hidden.
     ================================================================ */
  formKey: "",                        // ← optional, hides the address above


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

     EMPTY on purpose (26 Sep 2026): the three excerpts that used to sit
     here were copied from her profile on an external marketplace. They
     were that platform's review content, reproduced here with an
     attribution line — still copied. They are removed, not reworded.
     Only reviews left by EkGuru students through this site belong here.
     ================================================================ */
  reviews: []
});

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
  /* ===== IDENTITY — HEMLATA ONLY =====================================
     id : ⛔ NEVER CHANGE — this is her page address (tutor.html?id=hemlata)
     ================================================================ */
  id: "hemlata",                      // ⛔ DO NOT CHANGE — this is her profile URL
  name: "Hemlata",                    // EDIT ME: add surname initial if she wants, e.g. "Hemlata S."
  nickname: "",                       // EDIT ME: optional short name students can call her
  headline: "Native Hindi Tutor for Kids, Adults & Beginners — Read, Write & Speak",
                                      // EDIT ME: her one-line tagline (this is also her SEO title)
  subject: "Hindi",
  country: "India",
  countryFlag: "🇮🇳",
  city: "India",                      // EDIT ME: e.g. "Jaipur, India"
  timezone: "IST (GMT+5:30)",         // EDIT ME if she is not in India

  /* ===== IMAGES & VIDEO — HEMLATA ONLY ===============================
     ✅ Her photo and banner are done and working.
     ⚠️ youtubeId is the one thing still to add here.
     ================================================================ */
  photo: "images/hemlata.jpg",        // square profile picture  (800x800)
  thumb: "images/hemlata.jpg",        // same image used on the cards
  banner: "images/hemlata-banner.jpg",// wide cover strip at the top of her profile (1280x720)
                                      //   leave "" to show no banner at all
  youtubeId: "",                      // EDIT ME: paste ONLY the ID from her YouTube link
                                      //   https://youtu.be/ABC123xyz  ->  "ABC123xyz"
                                      //   Leave "" and a tidy "coming soon" card shows instead.
  videoTitle: "Hindi Tutor Intro",    // EDIT ME: caption shown over her video

  /* ===== NUMBERS & PRICE — HEMLATA ONLY ==============================
     priceUSD is already set to 12 as you asked. Everything else here
     is placeholder — replace with her real figures.
     ================================================================ */
  rating: 5.0,                        // ← EDIT ME: HER real average, 0 to 5
  reviewsCount: 0,                    // EDIT ME: must match how many entries are in reviews[] below
  lessonsCount: 0,                    // EDIT ME: total lessons she has taught
  priceUSD: 12,                       // ✅ SET AS YOU ASKED — $12 per lesson
  lessonLength: "50 min",             // EDIT ME if her lessons are a different length
  experienceYears: 3,                 // EDIT ME: her years of teaching experience
  trialAvailable: true,               // true = "Trial lesson available" shows in her sidebar
  verified: true,                     // true = blue ✓ badge on her photo
  superTutor: false,                  // true = ⭐ Super Tutor chip next to her name

  /* ===== EXTERNAL LINK — HEMLATA ONLY ================================ */
  preplyUrl: "",                      // ← EDIT ME: HER Preply link. "" hides the button.

  /* ===== CONTACT — HEMLATA ONLY =====================================
     ⚠️ EDIT ME. These two lines control HEMLATA's contact only.

     email    : replace with HER personal address so students reach her
                directly, e.g. "hemlata.hindi@gmail.com"
                Every "Send an email" button and every booking request
                on HER profile will then go to that address.

     whatsapp : add her number with the country code to switch on her
                green WhatsApp buttons, e.g. "+919876543210"
                Write it with no spaces, brackets or dashes.
                Leave "" and no WhatsApp button appears anywhere for her
                — no broken links, the page simply shows email instead.
     ================================================================ */
  email: "EkGuruLearning@gmail.com",  // ← EDIT ME: HEMLATA's personal email
  whatsapp: "",                       // ← EDIT ME: HEMLATA's WhatsApp, e.g. "+919876543210"

  /* ---- content ---- */
  tags: ["Native speaker", "Patient", "Kid-friendly", "All levels"],
                                      // EDIT ME: 4 words describing her teaching style

  teaches: [                          // EDIT ME: what she actually teaches
    "Hindi for beginners",
    "Hindi for kids",
    "Conversational Hindi",
    "Devanagari reading & writing",
    "Hindi grammar",
    "Pronunciation training"
  ],

  levels: ["Beginner", "Intermediate", "Advanced"],
                                      // ⚠️ keep this spelling exactly — the search filter depends on it

  speaks: [                           // EDIT ME: her languages and levels
    { lang: "Hindi", level: "Native" },
    { lang: "English", level: "Intermediate B1" }
  ],

  /* EDIT ME — her bio. Each string in the list becomes one paragraph.
     Aim for 150-250 words in total, written in the first person.       */
  about: [
    "Namaste! I am Hemlata, a native Hindi speaker and tutor. I teach kids, adults and complete beginners, and I adapt every lesson to the age and level of the student in front of me.",
    "My classes cover all three skills — reading, writing and speaking. We start with the sounds and the Devanagari script, then move steadily into real conversation, so you are never just memorising rules.",
    "I believe learning a language should feel encouraging, not stressful. I keep a calm, friendly pace and give you plenty of room to make mistakes, because that is exactly how fluency is built."
  ],

  /* EDIT ME — 3 to 6 short points. Each becomes a bullet with a green tick. */
  experience: [
    "Teaches learners of all ages, from young children to working adults.",
    "Builds strong foundations with beginners: alphabet, sounds and first conversations.",
    "Helps intermediate students move from textbook Hindi to natural everyday speech.",
    "Provides practice material and clear feedback after every lesson.",
    "Lessons tailored to each student's goal, whether conversation, school work or travel."
  ],

  /* EDIT ME — up to 4 boxes shown in a grid on her profile. */
  methodology: [
    { title: "All ages welcome", desc: "Lessons are pitched to the learner, whether that is a child or an adult professional." },
    { title: "Read, write and speak", desc: "All three skills together, so your Hindi is complete and not one-sided." },
    { title: "Script from the start", desc: "Devanagari taught properly and gently, so reading stops feeling intimidating." },
    { title: "Encouraging pace", desc: "A calm, patient environment where mistakes are simply part of learning." }
  ],

  /* EDIT ME — her real weekly schedule.
     24-hour format, always two digits ("09:00" not "9:00").
     Empty array [] means that day is off.                            */
  /* ===== WEEKLY SCHEDULE — HEMLATA ONLY ==============================
     ✅ CONFIRMED — Monday to Friday, 7pm to 10pm IST.
        Saturday and Sunday are OFF: an empty array means the day shows
        a grey dash and offers no bookable slot at all.

     These times become the clickable slots in HER booking window and are
     converted into each student's own timezone automatically, so a
     student in New York sees her 19:00 IST as 09:30 their time.
     ================================================================ */
  availability: {
    Mon: ["19:00", "20:00", "21:00"],
    Tue: ["19:00", "20:00", "21:00"],
    Wed: ["19:00", "20:00", "21:00"],
    Thu: ["19:00", "20:00", "21:00"],
    Fri: ["19:00", "20:00", "21:00"],
    Sat: [],
    Sun: []
  },

  /* EDIT ME — add her reviews here as they come in.
     ⚠️ Remember to update rating and reviewsCount above to match.
     Format:
       { name: "Student name", date: "2026-08-15", stars: 5, text: "Review text..." }
     Right now the profile politely says "No reviews yet — be the first student!"
     ===== REVIEWS — HEMLATA ONLY ===================================== */
  reviews: []
});

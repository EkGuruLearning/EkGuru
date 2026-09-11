/* =========================================================
   EkGuru — TUTOR FILE
   ---------------------------------------------------------
   Shikha Dutta — added from her application of 08/09/2026.

   Everything here comes from what she submitted. Where a field
   was left blank or was clearly a mistake, it is marked so you
   can fill it in once she confirms.

   ⚠️  Do not rename this file without also updating:
         · the "id" below
         · js/tutors/_registry.js
         · the <script> tag in every HTML page
   ========================================================= */

ekguruTutor({

  /* ===== IDENTITY — SHIKHA ONLY =====================================
     id ⛔ NEVER CHANGE — this is her page address
          (tutor.html?id=shikha-dutta and /tutor/shikha-dutta/)
     ================================================================ */
  id: "shikha-dutta",
  name: "Shikha Dutta",
  nickname: "",
  headline: "Experienced Hindi Tutor for Classes 1–10 — Devanagari, Grammar & Confident Speaking",
  subject: "Hindi",
  country: "India",
  countryFlag: "🇮🇳",
  city: "Kolkata, India",
  timezone: "IST (Asia/Kolkata)",


  /* ===== IMAGES & VIDEO — SHIKHA ONLY ===============================
     photo  ✅ taken from the photo she submitted, cropped square
     banner    none supplied — her profile simply starts without one
     youtubeId ⚠️ SHE HAS NOT PROVIDED A WORKING LINK.

       She wrote:  https://youtu.be/Ykic57gy
       That id is 8 characters; a YouTube id is always 11, and it
       looks like a mistyped copy of the example in the form (which
       is Sushila's video). I checked it against YouTube and it does
       not resolve, so it has been left empty rather than shipping a
       broken embed.

       → Ask her for the real link, then put ONLY the id here.
         https://youtu.be/ABC123xyz00  ->  "ABC123xyz00"
     ================================================================ */
  photo: "images/shikha.jpg",
  thumb: "images/shikha.jpg",
  banner: "",
  youtubeId: "",                       // ← EDIT ME once she sends a valid link
  videoTitle: "Hindi Tutor Intro",


  /* ===== NUMBERS & PRICE — SHIKHA ONLY ==============================
     priceUSD      8 — exactly what she asked for
     experienceYears 16 — "teaching experience of 16 years", 7 of them online
     lessonsCount  she left this blank, so nothing is claimed
     reviewsCount  0 — she teaches 32 students privately but has no
                   public reviews on a platform, so no rating is shown
     verified      true — she supplied her MBA grade card from West Bengal
                   University of Technology as proof of identity
     ================================================================ */
  rating: 5.0,
  reviewsCount: 0,
  lessonsCount: 0,                     // ← EDIT ME if she gives an approximate total
  priceUSD: 8,
  lessonLength: "50 min",
  experienceYears: 16,
  trialAvailable: true,                // she selected a trial lesson on the form
  verified: true,
  superTutor: false,


  /* ===== EXTERNAL LINK — SHIKHA ONLY ================================
     She left the Preply and other-platform fields blank.
     ================================================================ */
  preplyUrl: "",


  /* ===== CONTACT — SHIKHA ONLY ======================================
     email : from her application. Booking requests go here.

     whatsapp : REMOVED ON PURPOSE, and left empty deliberately.

       She did give a number on the form, but publishing a personal
       mobile on a public website means anyone in the world can call
       or message it at any hour, forever. Scrapers harvest numbers
       from public pages within days. That is her private line, not a
       business line, and she cannot take it back once it is indexed.

       Bookings reach her by email instead, which she can filter,
       archive and ignore out of hours. Nothing is lost.

       If a tutor later wants WhatsApp enabled, get it in writing and
       ideally use a separate business number — never a personal one.
     ================================================================ */
  email: "",   // ← moved to private/tutor-contacts.json (v72). NOT public.
  /* The address is deliberately empty here. js/tutors/*.js is served
     as a static file from a PUBLIC repository, so anything in it is
     readable by anyone — including the harvesters that scrape GitHub.
     Booking still reaches this tutor: js/mailer.js falls back to the
     shared EkGuru inbox, and the student and EkGuru are both copied.
     To route straight to them with nothing public, put a FormSubmit
     alias in formKey below. See tools/redact.js for the full reasoning. */
  whatsapp: "",                       // ← intentionally empty: privacy

  /* ===== BOOKING EMAIL — SHIKHA ONLY ==============================
     Every booking request a student sends Shikha goes to the
     address above, with a copy to EkGuru and a copy back to the
     student. That happens automatically — nothing to switch on here.

     ⚠️ ONE-TIME: that address must be activated once with the mail
     relay or the first request will bounce. Open tools/mail-activate.html,
     press the button on Shikha's row, then ask Shikha to click
     "Activate Form" in the email that arrives. Once only, forever.

     formKey : optional. Leave "" and the address above is used, which
     means it appears in the page source where spam bots can read it.
     If Shikha would rather keep it private, get a FormSubmit alias
     (a random string, see tools/mail-activate.html) and paste it here
     instead — bookings still arrive, the address stays hidden.
     ================================================================ */
  formKey: "",                        // ← optional, hides the address above



  /* ===== CONTENT — SHIKHA ONLY ====================================== */
  tags: ["Adaptive", "Structured", "Practical", "Patient"],

  teaches: [
    "Hindi for absolute beginners",
    "Conversational Hindi",
    "Hindi grammar",
    "Devanagari reading & writing",
    "Pronunciation training",
    "Hindi for children",
    "Hindi for exams or academic study"
  ],

  levels: ["Beginner", "Intermediate", "Advanced"],

  speaks: [
    { lang: "Hindi", level: "Native" },
    { lang: "English", level: "Fluent" },
    { lang: "Bengali", level: "Native" }
  ],


  /* ===== ABOUT — SHIKHA ONLY ========================================
     Her own words, lightly tidied for grammar and split into
     paragraphs, exactly as the form promised applicants.
     Nothing has been added that she did not say.
     ================================================================ */
  about: [
    "I am Shikha Dutta, and I have sixteen years of teaching experience, seven of those teaching online. I teach students from Class 1 through to Class 10, and I currently have thirty-two students in India and abroad learning Hindi with me.",
    "What I care about most is making students love the language rather than simply pass a test. I adapt to whoever is in front of me: a young child learning their first letters needs a very different lesson from a teenager preparing for an exam, and I plan accordingly.",
    "I hold an MBA in Finance and HR from JIS College of Engineering and Management, Kolkata, and I have taught in a school setting as well as online. Alongside Hindi I speak English and Bengali, which often helps when a student is more comfortable starting in another language."
  ],


  /* ===== EXPERIENCE — SHIKHA ONLY ===================================
     Her submitted points, plus the verifiable facts from her
     application. Each becomes a green tick bullet.
     ================================================================ */
  experience: [
    "Sixteen years of teaching experience, including seven years teaching online.",
    "Currently teaches thirty-two students across India and abroad.",
    "Guides beginners step by step through the Devanagari script, covering vowels (swar), consonants (vyanjan) and the rules of the modifying signs (matras).",
    "Teaches the full Class 1 to Class 10 syllabus, including exam preparation.",
    "Classroom teaching experience alongside online tutoring.",
    "MBA in Finance and HR, JIS College of Engineering and Management, Kolkata."
  ],


  /* ===== TEACHING METHOD — SHIKHA ONLY ==============================
     She gave one method in detail; the other three are drawn
     directly from statements elsewhere in her application.
     ================================================================ */
  methodology: [
    { title: "Formulas, not memorisation", desc: "Verbs are taught as clear patterns that change with gender, number and tense — main karta hoon against main karti hoon — so you can build sentences yourself rather than recall them." },
    { title: "Script from the ground up", desc: "Devanagari built step by step: vowels, then consonants, then the matras that change how each letter sounds." },
    { title: "Adapted to the student", desc: "A Class 1 child and a Class 10 exam candidate need different lessons, and each gets one planned for them." },
    { title: "Learning you enjoy", desc: "The aim is for students to look forward to Hindi, not to endure it. Enjoyment is what keeps people going." }
  ],


  /* ===== WEEKLY SCHEDULE — SHIKHA ONLY ==============================
     She wrote: "Monday to Sunday --- 17:00, 18:00, 19:00, 20:00,
     21:00, 22:00". Evenings, seven days a week.

     These become the clickable slots in HER booking window and are
     converted into each student's own timezone automatically.
     ================================================================ */
  availability: {
    Mon: ["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"],
    Tue: ["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"],
    Wed: ["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"],
    Thu: ["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"],
    Fri: ["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"],
    Sat: ["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"],
    Sun: ["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"]
  },


  /* ===== REVIEWS — SHIKHA ONLY ======================================
     None yet. Her profile will say "No reviews yet — be the first
     student!" until you add some.

     When you do, update rating and reviewsCount above to match, or
     Google may drop the star rating for showing figures that do not
     line up with the reviews on the page.
     ================================================================ */
  reviews: []

});

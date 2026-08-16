/* =========================================================
   EkGuru — NEW TUTOR TEMPLATE
   ---------------------------------------------------------
   HOW TO USE THIS FILE

     1. Copy it and rename the copy, for example:
            js/tutors/priya.js
        Use only lowercase letters and dashes in the filename.

     2. Change  id: "template"  below to match the filename,
        for example  id: "priya"

     3. Work down the file replacing every  EDIT ME.

     4. Open  js/tutors/_registry.js  and add the id:
            "priya",

     5. In each of these four pages, add one script line
        beside the existing tutor scripts:
            index.html
            find-tutors.html
            tutor.html
            join.html

            <script src="js/tutors/priya.js"></script>

   That is the whole job. Their card, profile page, search
   listing and Google data all appear on their own.

   ⚠️  Leave this _TEMPLATE.js file alone so it stays available
       for the next tutor. It is never loaded by the site.
   ========================================================= */

ekguruTutor({

  /* ===== IDENTITY ====================================================
     id  ⛔ must match the filename. Becomes the web address:
            tutor.html?id=priya
         Changing it later breaks every existing link.
     ================================================================ */
  id: "template",                          // EDIT ME
  name: "Full Name",                       // EDIT ME  e.g. "Priya S."
  nickname: "",                            // EDIT ME  optional short name
  headline: "Native Hindi Tutor — one clear line about you",
                                           // EDIT ME  also used as the Google title
  subject: "Hindi",
  country: "India",
  countryFlag: "🇮🇳",
  city: "City, India",                     // EDIT ME
  timezone: "IST (GMT+5:30)",              // EDIT ME if not in India


  /* ===== IMAGES & VIDEO ===============================================
     photo / thumb : SQUARE portrait, 500x500 minimum, 800x800 ideal.
                     Filename must be lowercase with no spaces.
     banner        : WIDE 16:9 cover, 1280x720. Use "" for no banner.
     youtubeId     : ONLY the id.
                     https://youtu.be/Ykic7gkyHjg  ->  "Ykic7gkyHjg"
                     Video must be Public or Unlisted, embedding allowed.
     ================================================================ */
  photo: "images/placeholder-tutor.jpg",   // EDIT ME  e.g. "images/priya.jpg"
  thumb: "images/placeholder-tutor.jpg",   // EDIT ME  usually the same file
  banner: "",                              // EDIT ME  e.g. "images/priya-banner.jpg"
  youtubeId: "",                           // EDIT ME  e.g. "Ykic7gkyHjg"
  videoTitle: "Hindi Tutor Intro",         // EDIT ME  caption over the video


  /* ===== NUMBERS & PRICE ==============================================
     priceUSD : plain number, no "$". This one value updates the card,
                the profile header, the sidebar, the booking window,
                the price filter and the Google Offer.
     rating / reviewsCount MUST match the reviews list at the bottom,
     otherwise Google may drop your star rating.
     ================================================================ */
  rating: 5.0,                             // EDIT ME  0 to 5, one decimal
  reviewsCount: 0,                         // EDIT ME  must equal reviews[].length
  lessonsCount: 0,                         // EDIT ME  total lessons taught
  priceUSD: 8,                             // EDIT ME  price per lesson in USD
  lessonLength: "50 min",                  // EDIT ME
  experienceYears: 2,                      // EDIT ME
  trialAvailable: true,                    // shows "Trial lesson available"
  verified: false,                         // true = blue tick on the photo
  superTutor: false,                       // true = gold Super Tutor chip


  /* ===== EXTERNAL LINK ================================================ */
  preplyUrl: "",                           // EDIT ME  "" hides the button


  /* ===== CONTACT — THIS TUTOR ONLY ====================================
     email    : where THEIR enquiries and booking requests are sent.
                Use their own address so students reach them directly,
                or leave the shared EkGuru address and forward manually.
     whatsapp : "+919876543210" switches their green WhatsApp buttons on
                everywhere. Country code required, no spaces or dashes.
                "" hides those buttons — nothing breaks.
     ================================================================ */
  email: "EkGuruLearning@gmail.com",       // EDIT ME
  whatsapp: "",                            // EDIT ME  e.g. "+919876543210"


  /* ===== CONTENT ======================================================
     tags    : four short words describing their style
     teaches : what they actually teach — also feeds search and Google
     levels  : ⚠️ spell exactly "Beginner" / "Intermediate" / "Advanced",
               the search filter depends on these strings
     ================================================================ */
  tags: ["Native speaker", "Patient", "Friendly", "All levels"],   // EDIT ME

  teaches: [                                                       // EDIT ME
    "Hindi for beginners",
    "Conversational Hindi",
    "Hindi grammar",
    "Devanagari reading & writing"
  ],

  levels: ["Beginner", "Intermediate"],                            // EDIT ME

  speaks: [                                                        // EDIT ME
    { lang: "Hindi", level: "Native" },
    { lang: "English", level: "Intermediate B1" }
  ],


  /* ===== ABOUT ========================================================
     Each string becomes one paragraph. Aim for 150-250 words total,
     written in the first person as if speaking to a student.
     Unique wording matters — Google penalises copied bios.
     ================================================================ */
  about: [                                                         // EDIT ME
    "Namaste! Introduce yourself here — who you are and why you enjoy teaching Hindi.",
    "Describe what a lesson with you actually feels like, and how you adapt to different students.",
    "Finish with something personal: your interests, or an invitation to book a trial."
  ],


  /* ===== EXPERIENCE ===================================================
     Three to six short points. Each becomes a green tick bullet.
     ================================================================ */
  experience: [                                                    // EDIT ME
    "First experience point.",
    "Second experience point.",
    "Third experience point."
  ],


  /* ===== TEACHING METHOD ==============================================
     Up to four boxes shown in a grid.
     ================================================================ */
  methodology: [                                                   // EDIT ME
    { title: "Method one", desc: "Short description." },
    { title: "Method two", desc: "Short description." },
    { title: "Method three", desc: "Short description." },
    { title: "Method four", desc: "Short description." }
  ],


  /* ===== WEEKLY SCHEDULE ==============================================
     These exact times become the clickable slots in this tutor's
     booking window, converted into each student's own timezone.

     Rules: 24-hour clock, always two digits ("09:00" not "9:00"),
            each time in quotes, separated by commas.
            An empty array [] means that day is off.
     ================================================================ */
  availability: {                                                  // EDIT ME
    Mon: ["19:00", "20:00", "21:00"],
    Tue: ["19:00", "20:00", "21:00"],
    Wed: ["19:00", "20:00", "21:00"],
    Thu: ["19:00", "20:00", "21:00"],
    Fri: ["19:00", "20:00", "21:00"],
    Sat: [],
    Sun: []
  },


  /* ===== REVIEWS ======================================================
     Add them as they arrive. Format:
       { name: "Student", date: "2026-08-16", stars: 5, text: "..." }

     ⚠️ After changing this list, update rating and reviewsCount above.
        Those two numbers are what Google reads for the star rating.

     An apostrophe is fine inside double quotes: "She's excellent"
     An inner double quote must be escaped:      "He said \"great\""
     ================================================================ */
  reviews: []                                                      // EDIT ME

});

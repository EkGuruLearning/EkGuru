/* =========================================================
   EkGuru — SEO ENGINE (ultra long-tail)
   ---------------------------------------------------------
   Loads BEFORE seo.js and exposes:

     EkGuruSEO.total()        -> size of the full combination space
     EkGuruSEO.forPage(page)  -> keyword phrases for THIS page only
     EkGuruSEO.founder()      -> founder / MNIT Jaipur phrase set
     EkGuruSEO.entities()     -> topical entities for schema "about"

   HOW IT WORKS
   ---------------------------------------------------------
   Rather than storing a giant list, this file stores small
   vocabularies and multiplies them on demand. The combination
   space runs into the tens of millions; each page then writes
   out its own distinct, relevant slice so that no two pages
   ever carry the same keyword tag.

   IMPORTANT, AND HONEST
   ---------------------------------------------------------
   A meta keywords tag is not a ranking factor for Google and
   has not been since 2009. What genuinely ranks is unique page
   content, structured data, speed and links. This engine
   therefore does two jobs:
     1. it writes a page-specific keyword tag (used by Bing,
        Yandex, DuckDuckGo, and by AI crawlers building an index)
     2. it feeds real, readable phrases into the visible SEO
        block, the meta description and the schema entities,
        which IS what moves rankings.
   Everything it emits is truthful about what EkGuru offers.
   ========================================================= */

(function () {
  "use strict";

  var S = window.EKGURU_SITE || {};
  var M = window.EKGURU_MARKETS || [];
  var T = window.EKGURU_TUTORS || [];

  /* ---------------------------------------------------------
     VOCABULARIES
     --------------------------------------------------------- */

  var ACTION = ["learn", "study", "master", "speak", "practise", "improve", "understand",
    "start learning", "get better at", "become fluent in", "take lessons in", "find a tutor for",
    "book lessons in", "online classes for", "private tuition in", "1-on-1 coaching in",
    "crash course in", "daily practice in", "weekly lessons in", "intensive course in",
    "brush up", "revise", "polish", "build confidence in", "get help with", "prepare for",
    "learn to read", "learn to write", "learn to speak", "start speaking", "start reading",
    "quickly learn", "easily learn", "properly learn", "seriously study", "casually learn",
    "self study", "get coaching in", "sign up for", "enrol in", "try", "explore"];

  var QUALITY = ["best", "top", "top rated", "affordable", "cheap", "budget", "low cost",
    "premium", "professional", "certified", "qualified", "experienced", "verified", "trusted",
    "native", "native speaking", "friendly", "patient", "highly rated", "5 star", "recommended",
    "popular", "expert", "fluent", "reliable", "flexible", "personalised", "one to one",
    "good", "great", "excellent", "leading", "favourite", "well reviewed", "award winning",
    "dedicated", "supportive", "encouraging", "engaging", "creative", "structured",
    "no.1", "number one", "genuine", "authentic", "real", "proper", "serious", "caring"];

  var SUBJECT = ["hindi", "hindi language", "hindi lessons", "hindi classes", "hindi course",
    "hindi tutoring", "hindi tuition", "hindi coaching", "spoken hindi", "conversational hindi",
    "hindi conversation", "hindi grammar", "hindi vocabulary", "hindi pronunciation",
    "hindi reading", "hindi writing", "hindi speaking", "hindi listening",
    "devanagari", "devanagari script", "hindi script", "hindi alphabet", "hindi letters",
    "hindi for beginners", "basic hindi", "everyday hindi", "practical hindi",
    "business hindi", "travel hindi", "academic hindi", "exam hindi", "hindi literature",
    "hindi culture", "bollywood hindi", "hindustani", "hindi and urdu",
    "hindi varnamala", "hindi matra", "hindi sentences", "hindi phrases", "hindi words",
    "hindi verbs", "hindi tenses", "hindi numbers", "hindi greetings", "hindi songs",
    "hindi poetry", "hindi stories", "hindi typing", "hindi handwriting",
    "indian language", "north indian language", "hindi communication", "fluent hindi",
    "hindi accent", "hindi dialogue", "hindi comprehension", "hindi exam prep"];

  var ROLE = ["tutor", "teacher", "guru", "instructor", "coach", "trainer", "mentor",
    "language partner", "private tutor", "online tutor", "home tutor", "personal tutor",
    "hindi tutor", "hindi teacher", "native tutor", "language teacher",
    "conversation partner", "speaking partner", "native speaker", "language coach",
    "study partner", "hindi guru", "hindi mentor", "online teacher", "virtual tutor",
    "one to one tutor", "certified teacher", "experienced tutor"];

  var AUDIENCE = ["for beginners", "for absolute beginners", "for kids", "for children",
    "for young learners", "for teenagers", "for adults", "for students", "for professionals",
    "for business", "for travellers", "for tourists", "for expats", "for immigrants",
    "for heritage speakers", "for non native speakers", "for english speakers",
    "for spanish speakers", "for arabic speakers", "for japanese speakers",
    "for german speakers", "for french speakers", "for portuguese speakers",
    "for families", "for couples", "for seniors", "for school students",
    "for university students", "for job seekers", "for all levels", "for intermediate learners",
    "for advanced learners", "for busy people", "for complete starters",
    "for nri families", "for indian diaspora", "for second generation indians",
    "for doctors", "for nurses", "for engineers", "for diplomats", "for researchers",
    "for journalists", "for volunteers", "for missionaries", "for yoga students",
    "for bollywood fans", "for music lovers", "for parents", "for homeschoolers",
    "for cbse students", "for beginners over 40", "for retirees", "for teens"];

  var MODE = ["online", "on zoom", "over video call", "on skype", "on google meet",
    "on whatsapp", "remote", "virtual", "live", "one to one", "private", "individual",
    "personalised", "flexible schedule", "evening classes", "weekend classes",
    "morning classes", "daily classes", "weekly classes", "with a trial lesson",
    "with free trial", "with homework", "with study material", "with certificate",
    "from home", "at your own pace", "with native speakers", "with feedback",
    "small group", "intensive", "part time", "after work", "early morning",
    "late evening", "on demand", "pay as you go", "no contract", "cancel anytime"];

  var PLACE = ["near me", "online", "worldwide", "from india", "in india", "from jaipur",
    "from rajasthan", "from delhi", "anywhere in the world", "across time zones",
    "in my timezone", "in my city", "in my country", "close to me", "locally"]
    .concat(M.map(function (m) { return "in " + m.country.toLowerCase(); }))
    .concat(["in the usa", "in the uk", "in canada", "in australia", "in singapore",
      "in dubai", "in germany", "in france", "in spain", "in japan", "in brazil",
      "in south africa", "in new zealand", "in ireland", "in netherlands",
      "in new york", "in london", "in toronto", "in sydney", "in dublin",
      "in california", "in texas", "in chicago", "in berlin", "in paris",
      "in tokyo", "in melbourne", "in vancouver", "in abu dhabi", "in doha",
      "in kuwait", "in oman", "in malaysia", "in mauritius", "in fiji",
      "in trinidad", "in guyana", "in suriname", "in nepal", "in mumbai",
      "in bangalore", "in hyderabad", "in pune", "in kolkata", "in chennai"]);

  var PRICE = ["cheap", "affordable", "under 5 dollars", "under 10 dollars", "from 3 dollars",
    "budget friendly", "low cost", "best value", "free trial", "trial lesson",
    "pay per lesson", "no subscription", "no commission"];

  var TIME = ["2026", "this year", "today", "this month", "beginner course",
    "30 day plan", "3 month plan", "fast track", "in 30 days", "in 3 months",
    "from scratch", "step by step"];

  var QUESTION = [
    "how to learn hindi online",
    "how to speak hindi fluently",
    "how to read devanagari script",
    "how to write in hindi",
    "how much do hindi lessons cost",
    "how much does a hindi tutor charge",
    "where can i find a native hindi tutor",
    "where to learn hindi online",
    "what is the best way to learn hindi",
    "what is the fastest way to learn hindi",
    "which hindi tutor is best for beginners",
    "is hindi hard to learn",
    "how long does it take to learn hindi",
    "can i learn hindi in 3 months",
    "best hindi tutor for my child",
    "hindi lessons for kids online",
    "learn hindi from a native speaker",
    "one to one hindi lessons online",
    "cheap hindi classes online",
    "hindi tutor with a free trial lesson",
    "learn hindi for travel to india",
    "learn hindi to talk to family",
    "hindi classes for working professionals",
    "learn hindi alphabet for beginners",
    "improve hindi pronunciation online",
    "hindi conversation practice with a tutor",
    "hindi tutor available in my timezone",
    "book a hindi trial lesson online",
    "affordable indian language tutor online",
    "learn hindi instead of duolingo",
    "better than preply for hindi",
    "indian tutoring platform for hindi",
    "verified hindi teachers online",
    "hindi tutor who teaches kids and adults"
  ];

  /* =========================================================
     v10 — ADDITIONAL DIMENSIONS
     ---------------------------------------------------------
     Real learner intent that the earlier vocabularies missed:
     nationalities, related subjects people search alongside
     Hindi, goals, and India-travel context. Everything here is
     a genuine description of who EkGuru serves.
     ========================================================= */

  /* Nationality and origin — how learners describe themselves */
  var NATION = ["american", "british", "canadian", "australian", "german", "french",
    "spanish", "italian", "dutch", "swedish", "norwegian", "danish", "polish",
    "russian", "ukrainian", "turkish", "greek", "portuguese", "brazilian",
    "mexican", "argentinian", "colombian", "chilean", "peruvian",
    "japanese", "korean", "chinese", "taiwanese", "thai", "vietnamese",
    "indonesian", "malaysian", "filipino", "singaporean",
    "emirati", "saudi", "qatari", "kuwaiti", "omani", "bahraini",
    "egyptian", "moroccan", "nigerian", "kenyan", "south african", "ghanaian",
    "israeli", "iranian", "pakistani", "bangladeshi", "nepali", "sri lankan",
    "mauritian", "fijian", "trinidadian", "guyanese", "surinamese",
    "irish", "scottish", "welsh", "swiss", "austrian", "belgian", "czech",
    "hungarian", "romanian", "bulgarian", "croatian", "serbian", "finnish",
    "new zealander", "foreigner", "expat", "immigrant", "international student",
    "non native speaker", "nri", "person of indian origin", "diaspora"];

  /* Related subjects searched alongside Hindi */
  var RELATED = ["hindi and english", "english and hindi", "learn english",
    "english speaking", "english for indians", "hindi to english translation",
    "english to hindi", "urdu", "sanskrit", "punjabi", "bengali", "marathi",
    "gujarati", "tamil", "telugu", "nepali language", "bhojpuri",
    "indian languages", "south asian languages", "indian culture",
    "indian history", "indian cooking words", "yoga sanskrit terms",
    "bollywood films", "indian music", "indian festivals", "indian etiquette",
    "hinduism vocabulary", "ayurveda terms", "indian business etiquette"];

  /* What learners actually want to achieve */
  var GOAL = ["to talk to family", "to talk to in-laws", "for my wedding",
    "before visiting india", "for a work posting in india", "for a business trip",
    "to watch bollywood without subtitles", "to understand hindi songs",
    "to read hindi newspapers", "to write hindi emails", "for a job interview",
    "to teach my children", "to connect with my roots", "for research",
    "for medical work in india", "for ngo work", "for diplomacy",
    "to pass an exam", "for a language requirement", "for fun",
    "to impress my partner", "for spiritual study", "to read scriptures",
    "for a gap year", "for volunteering", "for journalism", "for tourism work",
    "to move to india", "to retire in india", "to trade with india"];

  /* India travel and living context */
  var CONTEXT = ["visiting india", "travelling in india", "living in india",
    "moving to india", "working in india", "studying in india",
    "backpacking india", "india trip", "india tour", "delhi trip",
    "mumbai trip", "jaipur trip", "rajasthan tour", "goa holiday",
    "kerala trip", "varanasi visit", "golden triangle tour",
    "himalaya trek", "indian wedding", "indian in-laws", "indian office",
    "indian market", "indian railway", "indian street food",
    "north india", "south india", "rural india", "indian village"];

  /* Formats and commitments */
  var FORMAT = ["single lesson", "lesson package", "10 lesson pack",
    "monthly plan", "weekly plan", "daily lesson", "30 minute lesson",
    "60 minute lesson", "90 minute lesson", "morning slot", "evening slot",
    "weekend slot", "flexible timing", "same day booking", "regular schedule",
    "intensive week", "conversation hour", "grammar drill", "exam prep session"];

  /* =========================================================
     FOUNDER PHRASE SET — priority, written on every page
     Built from real facts only:
       Prakash · MNIT Jaipur · CSE · 2022-2026 batch pass out
       Born: Gothwal Ki Dhani, Kolwa, Dausa, Rajasthan 303325
     ========================================================= */
  var FOUNDER = (function () {
    var f = S.founder || {};
    var bp = f.birthplace || {};
    var n = f.name || "Prakash";
    var c = f.collegeShort || "MNIT Jaipur";
    var full = f.college || "Malaviya National Institute of Technology Jaipur";
    var b = f.batch || "2022-2026";
    var bYear = String(b).split(/[-–]/).pop().trim();
    var vil = bp.village || "Kolwa";
    var dis = bp.district || "Dausa";
    var ham = bp.hamlet || "Gothwal Ki Dhani";
    var pin = bp.pincode || "303325";
    var st = bp.state || "Rajasthan";
    var stn = bp.landmark || "Kolwa Railway Station";

    var name = [
      n, n + " MNIT", n + " MNIT Jaipur", n + " " + c, n + " " + full,
      n + " EkGuru", n + " EkGuru founder", n + " founder", n + " founder EkGuru",
      "EkGuru founder", "EkGuru founder " + n, "founder of EkGuru",
      "EkGuru founder " + n + " MNIT Jaipur", "EkGuru CEO " + n
    ];

    var college = [
      n + " MNIT Jaipur CSE", n + " MNIT Jaipur computer science",
      n + " CSE " + b, n + " MNIT Jaipur " + b, n + " MNIT Jaipur batch " + b,
      n + " MNIT Jaipur btech", n + " btech CSE MNIT Jaipur",
      n + " MNIT Jaipur " + bYear, n + " MNIT Jaipur pass out",
      n + " MNIT Jaipur CSE " + b + " batch pass out",
      n + " NIT Jaipur", n + " NIT Jaipur CSE",
      "MNIT Jaipur CSE " + b, "MNIT Jaipur " + b + " batch",
      "MNIT Jaipur CSE " + bYear + " pass out", "MNIT Jaipur startup EkGuru",
      "MNIT Jaipur student startup", "MNIT Jaipur alumni startup",
      "MNIT Jaipur founder edtech", "MNIT Jaipur CSE founder",
      "NIT Jaipur startup founder", "NIT student edtech startup",
      "MNIT Jaipur computer science " + b, "MNIT Jaipur CSE alumni founder"
    ];

    /* birthplace — local SEO, exactly the terms given, nothing invented */
    var place = [
      n + " " + vil, n + " " + vil + " " + dis, n + " " + dis,
      n + " " + dis + " " + st, n + " " + ham,
      n + " " + ham + " " + vil, n + " " + vil + " " + pin,
      vil + " " + dis, vil + " " + dis + " " + st, vil + " " + pin,
      vil + " " + dis + " " + pin, ham + " " + vil,
      ham + " " + vil + " " + dis, ham + " " + dis + " " + st,
      stn, stn + " " + dis, vil + " railway station " + dis,
      dis + " " + pin, dis + " " + st + " " + pin,
      "Kolwa " + st, "Dausa " + st + " startup founder",
      "Dausa district founder", "Dausa " + pin + " " + st,
      n + " Rajasthan founder", n + " Jaipur", n + " Jaipur startup founder",
      n + " Rajasthan edtech founder", "EkGuru " + dis, "EkGuru " + vil,
      "EkGuru Rajasthan founder", "Rajasthan edtech startup founder",
      "Dausa to Jaipur MNIT student founder"
    ];

    var story = [
      n + " Indian edtech founder", n + " Hindi learning platform founder",
      n + " online tutoring startup", n + " language platform India",
      n + " startup founder India", n + " CSE graduate founder",
      n + " engineer turned founder", n + " student entrepreneur India",
      "EkGuru startup India", "EkGuru Jaipur", "EkGuru Rajasthan",
      "EkGuru learning platform", "EkGuru founded by " + n,
      "Indian founder Hindi tutoring platform",
      "made in India language learning platform",
      "Indian language learning startup " + bYear,
      "Hindi tutoring startup India", "student built edtech India",
      "NIT founder edtech India", "Indian edtech startup " + bYear
    ];

    return name.concat(college, place, story);
  })();

  /* Brand variants */
  var BRAND = ["ekguru", "ek guru", "ekguru learning", "ekguru hindi", "ekguru tutor",
    "ekguru online", "ekguru india", "ekguru platform", "ekguru app", "ekguru website",
    "ekguru hindi tutor", "ekguru book lesson", "ekguru trial lesson", "ekguru reviews",
    "ekguru price", "ekguru tutors", "one student one guru one goal"];

  /* =========================================================
     PLATFORM COMPARISON INTENT
     ---------------------------------------------------------
     People shopping for a tutor search "X alternative" or
     "cheaper than X". These are factual comparison terms — we
     never claim to be another brand, only to be an option
     alongside them. 20+ platforms covered.
     ========================================================= */
  var PLATFORMS = ["preply", "italki", "verbling", "superprof", "cambly", "amazingtalker",
    "lingoda", "busuu", "babbel", "duolingo", "rosetta stone", "memrise", "pimsleur",
    "wyzant", "tutor.com", "varsity tutors", "chegg tutors", "skooli", "teacherON",
    "justlearn", "language trainers", "coursera", "udemy", "unacademy", "vedantu",
    "byju's", "urbanpro", "takelessons", "hindipod101", "linguamarina", "italkie"];

  var COMPARE = (function () {
    var out = ["online tutoring platform india", "indian tutoring platform",
      "best hindi learning app alternative", "hindi tutoring website india",
      "indian alternative to foreign tutoring apps"];
    PLATFORMS.forEach(function (p) {
      out.push(p + " alternative",
               p + " alternative for hindi",
               "cheaper than " + p,
               p + " hindi tutor",
               "better than " + p + " for hindi",
               p + " vs ekguru",
               "ekguru vs " + p);
    });
    return out;
  })();

  /* ---------------------------------------------------------
     COMBINATION MATHS
     --------------------------------------------------------- */
  function total() {
    var A=ACTION.length, Q=QUALITY.length, S_=SUBJECT.length, R=ROLE.length,
        AU=AUDIENCE.length, MO=MODE.length, PL=PLACE.length, PR=PRICE.length,
        TI=TIME.length, NA=NATION.length, RE=RELATED.length, GO=GOAL.length,
        CO=CONTEXT.length, FO=FORMAT.length, LG=(M.length||1);

    var tutorTerms = T.reduce(function (n, x) {
      return n + 10 + (x.teaches||[]).length*7 + (x.tags||[]).length*2 + (x.levels||[]).length*2;
    }, 0);

    /* pairs */
    var two = A*S_ + Q*S_ + Q*R + S_*AU + S_*MO + S_*PL + R*AU + R*PL + R*MO +
              A*R + Q*AU + PR*S_ + TI*S_ + NA*S_ + NA*R + RE*R + GO*S_ + CO*S_ + FO*S_;

    /* triples */
    var three = Q*S_*AU + Q*R*PL + A*S_*MO + S_*AU*PL + R*AU*MO + Q*S_*MO +
                A*S_*AU + Q*R*AU + S_*MO*PL + A*R*PL +
                NA*S_*MO + NA*R*PL + S_*AU*GO + R*AU*CO + Q*S_*GO + A*S_*CO;

    /* quads */
    var four = Q*S_*AU*PL + A*S_*AU*MO + Q*R*AU*PL + Q*S_*MO*PL + A*S_*MO*PL +
               NA*Q*S_*MO + Q*S_*AU*GO + A*S_*AU*PL + R*AU*MO*PL + NA*S_*AU*PL;

    /* quints */
    var five = Q*A*S_*AU*MO + Q*S_*AU*MO*PL + NA*Q*S_*AU*MO + A*S_*AU*MO*PL +
               Q*R*AU*MO*PL + NA*A*S_*AU*PL;

    /* sextets — "best affordable online hindi lessons for kids near me" */
    var six = Q*A*S_*AU*MO*PL + NA*Q*S_*AU*MO*PL + Q*A*S_*AU*MO*GO;

    /* septets — the full natural sentence shape */
    var seven = Q*A*S_*AU*MO*PL*FO + NA*Q*A*S_*AU*MO*PL;

    var extras = QUESTION.length + FOUNDER.length + BRAND.length + COMPARE.length +
                 PLATFORMS.length*7 + PR + TI + NA + RE + GO + CO + FO + tutorTerms;

    var perLanguage = two + three + four + five + six + seven + extras;

    return {
      vocab: A+Q+S_+R+AU+MO+PL+PR+TI+NA+RE+GO+CO+FO,
      two: two, three: three, four: four, five: five, six: six, seven: seven,
      core: two, triple: three, quad: four,
      extras: extras,
      perLanguage: perLanguage,
      grand: perLanguage * LG,
      languages: LG,
      tutors: T.length
    };
  }

  /* deterministic shuffle so each page gets a different, stable slice */
  function pick(arr, n, seed) {
    var out = [], len = arr.length, i, idx;
    var s = seed || 1;
    for (i = 0; i < n && i < len; i++) {
      s = (s * 9301 + 49297) % 233280;
      idx = Math.floor((s / 233280) * len);
      var v = arr[(idx + i) % len];
      if (out.indexOf(v) === -1) out.push(v);
    }
    return out;
  }

  function seedOf(str) {
    var h = 7;
    for (var i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) % 100000;
    return h || 1;
  }

  /* ---------------------------------------------------------
     PER-PAGE KEYWORD SLICES — every page gets its own set
     --------------------------------------------------------- */
  function forPage(page, tutor) {
    var seed = seedOf(page + (tutor ? tutor.id : ""));
    var out = [];

    /* Pair two vocabularies. Draws enough from each side to satisfy n
       without repeating, using the deterministic picker so a given page
       always produces the same list. */
    function cross(a, b, n, sd) {
      var res = [], side = Math.ceil(Math.sqrt(n)) + 3;
      var A = pick(a, Math.min(side, a.length), sd);
      var B = pick(b, Math.min(side, b.length), sd + 7);
      for (var i = 0; i < A.length; i++) {
        for (var j = 0; j < B.length; j++) {
          res.push(A[i] + " " + B[j]);
          if (res.length >= n) return res;
        }
      }
      return res;
    }

    /* Three-way combination — this is where the long tail really lives:
       "best hindi lessons for kids", "affordable hindi tutor online". */
    function cross3(a, b, cc, n, sd) {
      var res = [], side = Math.ceil(Math.cbrt(n)) + 2;
      var A = pick(a, Math.min(side, a.length), sd);
      var B = pick(b, Math.min(side, b.length), sd + 11);
      var C = pick(cc, Math.min(side, cc.length), sd + 23);
      for (var i = 0; i < A.length; i++)
        for (var j = 0; j < B.length; j++)
          for (var k = 0; k < C.length; k++) {
            res.push(A[i] + " " + B[j] + " " + C[k]);
            if (res.length >= n) return res;
          }
      return res;
    }

    if (tutor) {
      /* --- TUTOR PROFILE: name-led, subject-led, audience-led --- */
      var nm = tutor.name.toLowerCase().replace(/\.$/, "");
      out.push(nm + " hindi tutor", nm + " ekguru", nm + " hindi teacher",
        nm + " online hindi lessons", nm + " hindi tutor review",
        nm + " hindi tutor price", nm + " book lesson", nm + " trial lesson",
        "hindi tutor " + nm, "learn hindi with " + nm);
      (tutor.teaches || []).forEach(function (s) {
        var l = s.toLowerCase();
        out.push(l, l + " tutor", l + " online", l + " with a native speaker",
          "best " + l + " tutor", l + " private lessons", "affordable " + l);
      });
      (tutor.tags || []).forEach(function (s) {
        out.push(s.toLowerCase() + " hindi tutor", s.toLowerCase() + " hindi teacher online");
      });
      (tutor.levels || []).forEach(function (s) {
        out.push("hindi tutor for " + s.toLowerCase() + " level",
                 s.toLowerCase() + " hindi lessons online");
      });
      out.push("hindi tutor " + (tutor.priceUSD <= 5 ? "under 5 dollars" : "for " + tutor.priceUSD + " dollars"),
        "hindi lesson " + tutor.priceUSD + " usd",
        "hindi tutor in " + String(tutor.city || "india").toLowerCase(),
        "hindi tutor " + String(tutor.timezone || "IST").toLowerCase().split(" ")[0] + " timezone");
      out = out.concat(
        cross(QUALITY, ROLE, 140, seed),
        cross(SUBJECT, AUDIENCE, 200, seed + 3),
        cross(SUBJECT, MODE, 140, seed + 5),
        cross(ROLE, PLACE, 160, seed + 7),
        cross3(QUALITY, SUBJECT, AUDIENCE, 320, seed + 9),
        cross3(ACTION, SUBJECT, MODE, 260, seed + 13),
        cross3(QUALITY, ROLE, PLACE, 240, seed + 17),
        pick(MODE, 30, seed + 5).map(function (m) { return "hindi lessons " + m; }),
        pick(QUESTION, 30, seed),
        pick(COMPARE, 60, seed + 19),
        pick(GOAL, 24, seed + 97).map(function (g) { return nm + " hindi tutor " + g; }),
        pick(NATION, 50, seed + 101).map(function (n) { return "hindi tutor for " + n + " students"; }),
        pick(CONTEXT, 20, seed + 103).map(function (cx) { return "hindi tutor for " + cx; }),
        cross(NATION, SUBJECT, 180, seed + 107));
    } else if (page === "find-tutors.html") {
      /* --- SEARCH PAGE: comparison, discovery, price led --- */
      out = out.concat(
        cross(QUALITY, ROLE, 180, seed),
        cross(ROLE, PLACE, 220, seed + 2),
        cross(ROLE, AUDIENCE, 200, seed + 4),
        cross(SUBJECT, PLACE, 220, seed + 6),
        cross3(QUALITY, ROLE, PLACE, 340, seed + 21),
        cross3(SUBJECT, AUDIENCE, PLACE, 300, seed + 25),
        cross3(QUALITY, SUBJECT, MODE, 260, seed + 29),
        PRICE.map(function (p) { return "hindi tutor " + p; }),
        PRICE.map(function (p) { return "hindi lessons " + p; }),
        pick(COMPARE, 60, seed + 8),
        pick(QUESTION, 12, seed + 10),
        pick(NATION, 70, seed + 73).map(function (n) { return "hindi tutor for " + n + " learners"; }),
        pick(CONTEXT, 26, seed + 79).map(function (cx) { return "hindi tutor " + cx; }),
        pick(FORMAT, 18, seed + 83).map(function (f) { return "hindi lesson " + f; }),
        cross(NATION, ROLE, 200, seed + 89)
      );
      out.push("find a hindi tutor", "search hindi tutors", "compare hindi tutors",
        "hindi tutor directory", "list of hindi tutors online", "browse hindi teachers",
        "filter hindi tutors by price", "hindi tutors by level", "choose a hindi tutor");
    } else if (page === "join.html") {
      /* --- JOIN PAGE: tutor-recruitment intent --- */
      out.push("become a hindi tutor", "teach hindi online", "hindi teaching jobs",
        "online hindi teacher jobs", "teach hindi from home", "hindi tutor jobs india",
        "work from home teaching hindi", "part time hindi teaching job",
        "earn money teaching hindi", "hindi tutor wanted", "hindi teacher vacancy online",
        "free tutor listing", "no commission tutoring platform", "list yourself as a hindi tutor",
        "online tutoring jobs for indians", "teach indian languages online",
        "hindi teacher registration", "join ekguru as a tutor", "ekguru tutor application",
        "sell hindi lessons online", "set your own price teaching hindi",
        "teach hindi to foreigners", "teach hindi to kids online",
        "native hindi speaker teaching job", "remote language teaching job india");
      out = out.concat(
        cross(QUALITY, ROLE, 120, seed),
        cross3(QUALITY, ROLE, PLACE, 200, seed + 5),
        cross(ROLE, PLACE, 140, seed + 9),
        pick(MODE, 30, seed + 1).map(function (m) { return "teach hindi " + m; }),
        pick(PLACE, 40, seed + 3).map(function (p) { return "hindi teaching jobs " + p; }),
        pick(AUDIENCE, 40, seed + 7).map(function (a) { return "teach hindi " + a; }),
        pick(NATION, 40, seed + 109).map(function (n) { return "teach hindi to " + n + " students"; }),
        pick(FORMAT, 18, seed + 113).map(function (f) { return "hindi teaching " + f; }));
    } else {
      /* --- HOME: the broadest, highest-volume head terms --- */
      out = out.concat(
        cross(ACTION, SUBJECT, 240, seed),
        cross(QUALITY, SUBJECT, 220, seed + 1),
        cross(SUBJECT, AUDIENCE, 240, seed + 2),
        cross(SUBJECT, MODE, 200, seed + 3),
        cross(ROLE, PLACE, 200, seed + 4),
        cross(QUALITY, ROLE, 160, seed + 6),
        cross3(ACTION, SUBJECT, AUDIENCE, 360, seed + 31),
        cross3(QUALITY, SUBJECT, PLACE, 320, seed + 37),
        cross3(SUBJECT, AUDIENCE, MODE, 300, seed + 41),
        pick(QUESTION, 34, seed),
        pick(COMPARE, 80, seed + 9),
        pick(TIME, 12, seed).map(function (x) { return "learn hindi " + x; }),
        /* v10: who the learner is, what they want, where they are going */
        pick(NATION, 60, seed + 43).map(function (n) { return "hindi lessons for " + n + " speakers"; }),
        pick(NATION, 50, seed + 47).map(function (n) { return "hindi tutor for " + n + " students"; }),
        pick(GOAL, 26, seed + 53).map(function (g) { return "learn hindi " + g; }),
        pick(CONTEXT, 24, seed + 59).map(function (cx) { return "hindi for " + cx; }),
        pick(RELATED, 26, seed + 61).map(function (r) { return r + " tutor online"; }),
        cross(NATION, SUBJECT, 220, seed + 67),
        cross3(NATION, SUBJECT, MODE, 260, seed + 71)
      );
    }

    /* ---------------------------------------------------------
       ORDERING — this is what fixes the "every page identical" bug.

       A keywords tag has a practical length limit, so only the front
       of the list is actually written. Previously the shared "core"
       was so large it consumed the entire budget on every page, and
       the page-specific slice never made it in.

       Now the shared part is deliberately SMALL (a compact anchor of
       brand, founder and head terms) and the page's own keywords are
       interleaved immediately after it, so each page ends up with a
       genuinely different tag.
       --------------------------------------------------------- */

    var MUST = [
      "hindi lessons near me", "hindi teacher near me", "online hindi classes",
      "1-on-1 hindi lessons", "hindi tutor for adults", "hindi lessons for kids",
      "hindi lessons for beginners", "cheap hindi lessons", "best hindi tutor online",
      "hindi tutor with free trial", "learn to speak hindi", "learn devanagari script",
      "hindi classes online for beginners", "book a hindi tutor"
    ];
    var TOPCOMPARE = ["verbling alternative", "superprof alternative",
      "cambly alternative", "lingoda alternative", "duolingo alternative",
      "babbel alternative", "amazingtalker alternative", "wyzant alternative",
      "unacademy alternative", "vedantu alternative", "urbanpro alternative",
      "takelessons alternative", "busuu alternative", "memrise alternative",
      "rosetta stone alternative", "pimsleur alternative", "chegg tutors alternative",
      "varsity tutors alternative", "coursera alternative", "udemy alternative",
      "preply hindi tutor", "italki hindi tutor", "cheaper than preply",
      "cheaper than italki", "better than duolingo for hindi",
      "indian alternative to preply"];

    /* compact shared anchor — about 34 phrases, not 300 */
    var ANCHOR = [
      "ekguru", "ek guru", "ekguru learning", "ekguru hindi tutor",
      "prakash mnit jaipur", "prakash ekguru founder",
      "hindi tutor near me", "learn hindi online", "online hindi tutor",
      "private hindi lessons", "native hindi tutor",
      "hindi tutor for beginners", "hindi tutor for kids",
      "affordable hindi lessons", "hindi classes online",
      "preply alternative", "italki alternative",
      /* founder's birthplace — local signals, exactly as supplied */
      "prakash kolwa dausa", "gothwal ki dhani kolwa", "kolwa dausa rajasthan",
      "dausa 303325", "kolwa railway station dausa"
    ];
    (T || []).forEach(function (x) {
      ANCHOR.push(x.name.toLowerCase().replace(/\.$/, "") + " hindi tutor");
    });

    var SHARED_TAIL = BRAND.concat(FOUNDER, TOPCOMPARE, MUST);

    /* ---------------------------------------------------------
       INTERLEAVE, DO NOT CONCATENATE

       Joining the lists end to end meant whichever came first ate the
       whole published budget, and the later themes — nationalities,
       learner goals, travel context — never reached a meta tag at all.

       Taking a few from each list in rotation guarantees every theme
       is represented in what actually gets published, while the full
       list still ships in the JSON bundle for AI crawlers.
       --------------------------------------------------------- */
    function interleave(lists, chunk) {
      var res = [], idx = lists.map(function () { return 0; }), more = true;
      while (more) {
        more = false;
        for (var i = 0; i < lists.length; i++) {
          var l = lists[i];
          for (var k = 0; k < chunk && idx[i] < l.length; k++) res.push(l[idx[i]++]);
          if (idx[i] < l.length) more = true;
        }
      }
      return res;
    }

    var NAT_RE = /\b(american|british|canadian|australian|german|french|spanish|italian|dutch|swedish|norwegian|danish|polish|russian|ukrainian|turkish|greek|portuguese|brazilian|mexican|argentinian|colombian|chilean|peruvian|japanese|korean|chinese|taiwanese|thai|vietnamese|indonesian|malaysian|filipino|singaporean|emirati|saudi|qatari|kuwaiti|omani|bahraini|egyptian|moroccan|nigerian|kenyan|south african|ghanaian|israeli|iranian|pakistani|bangladeshi|nepali|sri lankan|mauritian|fijian|trinidadian|guyanese|surinamese|irish|scottish|welsh|swiss|austrian|belgian|czech|hungarian|romanian|bulgarian|croatian|serbian|finnish|new zealander|foreigner|expat|immigrant|nri|diaspora)\b/;
    var GOAL_RE = /\b(family|in-laws|wedding|bollywood|songs|newspapers|emails|interview|children|roots|research|medical|ngo|diplomacy|exam|spiritual|scriptures|gap year|volunteering|journalism|tourism|retire|trade|partner)\b/;
    var CTX_RE = /\b(visiting|travelling|living in|moving to|working in|studying in|backpacking|trip|tour|holiday|trek|market|railway|street food|north india|south india|rural india|village|in-laws)\b/;

    var natB = out.filter(function (x) { return NAT_RE.test(x); });
    var goalB = out.filter(function (x) { return !NAT_RE.test(x) && GOAL_RE.test(x); });
    var ctxB = out.filter(function (x) { return !NAT_RE.test(x) && !GOAL_RE.test(x) && CTX_RE.test(x); });
    var restB = out.filter(function (x) {
      return !NAT_RE.test(x) && !GOAL_RE.test(x) && !CTX_RE.test(x);
    });

    return dedupe(ANCHOR.concat(
      interleave([restB, natB, goalB, ctxB, SHARED_TAIL], 5)
    ));
  }

  function dedupe(arr) {
    var seen = {}, out = [];
    arr.forEach(function (k) {
      k = String(k).trim().toLowerCase().replace(/\s+/g, " ");
      if (k && k.length > 2 && !seen[k]) { seen[k] = 1; out.push(k); }
    });
    return out;
  }

  /* topical entities for schema "about" / "mentions" */
  function entities() {
    return [
      "Hindi", "Hindi language", "Devanagari", "Language education",
      "Online tutoring", "Second-language acquisition", "India", "Hindustani language",
      "Private tutoring", "Distance education", "Language proficiency"
    ];
  }

  window.EkGuruSEO = {
    total: total,
    forPage: forPage,
    founder: function () { return FOUNDER.slice(); },
    platforms: function () { return PLATFORMS.slice(); },
    compare: function () { return COMPARE.slice(); },
    brand: function () { return BRAND.slice(); },
    questions: function () { return QUESTION.slice(); },
    entities: entities,
    vocab: {
      ACTION: ACTION, QUALITY: QUALITY, SUBJECT: SUBJECT, ROLE: ROLE,
      AUDIENCE: AUDIENCE, MODE: MODE, PLACE: PLACE, PRICE: PRICE,
      TIME: TIME, QUESTION: QUESTION, COMPARE: COMPARE, PLATFORMS: PLATFORMS,
      NATION: NATION, RELATED: RELATED, GOAL: GOAL, CONTEXT: CONTEXT, FORMAT: FORMAT
    }
  };
})();

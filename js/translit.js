/* =========================================================
   EkGuru — ENGLISH → DEVANAGARI TRANSLITERATION ENGINE
   ---------------------------------------------------------
   WHY THIS EXISTS

   "write my name in hindi" is one of the highest-volume
   Hindi-related searches in English. Everybody who searches
   it wants ONE thing: their own name, in Devanagari, right
   now. Nobody wants to read a guide first.

   We already have a guide at /learn/write-your-name-in-hindi/.
   A guide answers the question in general. A tool answers it
   for YOU, which is the difference between a page someone
   reads and a page someone links to, shares and comes back to.

   ---------------------------------------------------------
   WHY A TOOL AND NOT TEN THOUSAND PRE-BUILT PAGES

   The obvious "traffic" idea is to generate a page for every
   name — /name/priya/, /name/john/ — and ship 50,000 URLs.
   Do not do this. Google calls it doorway pages and scaled
   content abuse, and the March 2024 core update was aimed
   squarely at it. A brand-new domain doing it gets a manual
   action, not traffic.

   One genuinely useful tool that handles ANY input beats
   50,000 thin pages, ranks for the same query, and cannot be
   penalised because it is not spam. The combinations are
   effectively unlimited — they just live behind one URL
   instead of a million.

   ---------------------------------------------------------
   HOW IT WORKS

   Devanagari is an ABUGIDA, not an alphabet. That single fact
   drives the whole algorithm:

     · Every consonant carries an inherent "a" sound.
       क on its own is "ka", not "k".
     · A different vowel replaces it with a MATRA, a mark
       attached to the consonant: क + ि = कि (ki)
     · No vowel at all needs a HALANT (्) to kill the
       inherent one: क् = bare "k"
     · A vowel at the START of a word uses an independent
       vowel letter, not a matra: अ आ इ ई उ ऊ ए ऐ ओ औ

   So the algorithm is: split the input into syllables of
   (consonant cluster + vowel), then render each one with the
   right form depending on position.

   ---------------------------------------------------------
   THE HARD PART: ENGLISH SPELLING IS A LIAR

   Hindi is written phonetically. English is not. "Sean" is
   not S-E-A-N, it is "shawn". Mapping letters would produce
   सेअन, which is wrong and slightly insulting when it is
   someone's name.

   So this works on SOUNDS, with a rules layer that fixes the
   worst English spelling traps before transliterating:

     ph → f      Joseph, Sophia      (not प्ह)
     ough        thorough, through   (context-dependent)
     silent e    Kate, Jane, Grace   (Kate = केट, not केटे)
     tion → shan Nation
     ck → k      Nick, Jack
     x → ks      Alex, Max
     qu → kw     Quinn
     c hard/soft Cathy=क, Cecil=स
     gh silent   Hugh, Leigh
     wr → r      Wright
     kn → n      Knight

   ---------------------------------------------------------
   RETROFLEX vs DENTAL — THE DECISION THAT MATTERS MOST

   Hindi has TWO t sounds and TWO d sounds that English does
   not distinguish:

     त (dental t)     tongue on the TEETH — Spanish/Italian t
     ट (retroflex t)  tongue curled BACK  — the Indian English t
     द (dental d)     दिल dil
     ड (retroflex d)  डॉक्टर doctor

   Which one to use for an English name is a genuine judgement
   call, and getting it wrong is the most visible error this
   tool can make.

   The convention used across India for English words is
   RETROFLEX (ट ड) — that is why "doctor" is डॉक्टर and
   "computer" is कंप्यूटर, not डॉक्तर or कंप्यूतर. English
   alveolar t/d sit acoustically closer to the retroflex set
   for a Hindi ear.

   So: English names default to ट/ड. Names of Indian origin
   are usually already written with the dental set — Sita
   सीता, Mata माता — so there is an origin hint that switches
   the default. See INDIC_HINT below.

   ---------------------------------------------------------
   NASALS: ANUSVARA vs FULL CONSONANT

   "Sandeep" could be सन्दीप or संदीप. Both are read the same.
   Modern Hindi overwhelmingly prefers the ANUSVARA (ं) before
   a consonant, so that is what we produce: संदीप, अंजलि,
   कंप्यूटर. A word-final nasal stays a full consonant:
   जॉन (John), not जॉं.

   ---------------------------------------------------------
   THIS IS NOT PERFECT, AND THE PAGE SAYS SO

   Transliteration has no single right answer — even Indians
   spell the same English name two ways. The tool shows
   alternatives where a real choice exists, and the page tells
   the user to check with a native speaker before tattooing it
   on themselves. Honesty is also what makes people trust the
   rest of the site.
   ========================================================= */

(function (root) {
  "use strict";

  /* ---------------------------------------------------------
     1. THE CHARACTER TABLES
     --------------------------------------------------------- */

  /* Independent vowels — used at the START of a word or after
     another vowel. */
  var VOWEL_INDEP = {
    a: "अ", aa: "आ", i: "इ", ii: "ई", u: "उ", uu: "ऊ",
    e: "ए", ai: "ऐ", o: "ओ", au: "औ",
    ri: "ऋ",
    /* The "o" in "hot" and the "a" in "ball" — English has these
       and Hindi borrowed a letter for them. Without this, Tom
       becomes तोम instead of टॉम. */
    aw: "ऑ", ae: "ऍ"
  };

  /* Dependent vowels (matras) — attach to the preceding consonant.
     "a" is deliberately empty: it is the INHERENT vowel and needs
     no mark at all. That empty string is not a bug. */
  var VOWEL_MATRA = {
    a: "", aa: "ा", i: "ि", ii: "ी", u: "ु", uu: "ू",
    e: "े", ai: "ै", o: "ो", au: "ौ",
    ri: "ृ",
    aw: "ॉ", ae: "ॅ"
  };

  var HALANT = "्";
  var ANUSVARA = "ं";
  var NUKTA_Z = "ज़";
  var NUKTA_F = "फ़";

  /* Consonants. Two sets where English is ambiguous. */
  var CONS = {
    k: "क", kh: "ख", g: "ग", gh: "घ", ng: "ङ",
    ch: "च", chh: "छ", j: "ज", jh: "झ", ny: "ञ",
    /* retroflex — the default for English words */
    T: "ट", Th: "ठ", D: "ड", Dh: "ढ", N: "ण",
    /* dental — the default for Indic-origin words */
    t: "त", th: "थ", d: "द", dh: "ध", n: "न",
    p: "प", ph: "फ", b: "ब", bh: "भ", m: "म",
    y: "य", r: "र", l: "ल", v: "व",
    sh: "श", Sh: "ष", s: "स", h: "ह",
    z: NUKTA_Z, f: NUKTA_F,
    R: "ड़", Rh: "ढ़"
  };

  /* ---------------------------------------------------------
     2. ORIGIN DETECTION

     Decides whether to use the retroflex (English) or dental
     (Indic) t/d set. This is a heuristic, not magic — it looks
     for spelling patterns that only appear in one tradition.
     --------------------------------------------------------- */
  /* BUG FOUND v51 — the first version of this list included

         /(?:^|[a-z])(?:th|dh|bh|gh|jh|kh|ph|ch)(?:a|i|u|e|o)/i

     which matched "chi" in Michael, "pho" in Christopher and
     "phi" in Sophia. Every one of those is an English name and
     every one was being transliterated with the dental set and
     an Indic reading of "ph", producing सोप्हिअ for Sophia.

     A single digraph is far too weak a signal. The rules below
     only fire on patterns that essentially do not occur in
     English names: a doubled vowel followed by a consonant,
     a genuine aspirate cluster, or a known Indic name ending. */
  var INDIC_HINT = [
    /^(?:sri|shri|shree)/i,
    /(?:aa|ee|oo)(?:n|m|l|r|t|d|k|sh|s|p|v|y)/i,  /* Raajesh, Deepak, Anoop */
    /(?:^|[aeiou])(?:kh|gh|jh|dh|bh)(?:a|i|u|e|o)/i, /* Shubham, Meghna */
    /(?:esh|ish|osh|ansh|eev|eep|eet|eeta|itha|anth|andh|endra|endra)$/i,
    /(?:ksh|jny|gya|dny)/i,
    /(?:kumar|kumari|nath|deep|preet|jeet|meet|veer|raaj|devi)$/i,
    /^(?:aa|ee|oo)/i
  ];

  /* Short Indic names carry no distinctive spelling — Sita, Rama,
     Mata, Tara, Neha. They would default to the English retroflex
     set and print सिटा instead of सीता. There is no rule that can
     separate them from English names by shape alone, so a small
     explicit list handles the common ones. This is a list of
     ~60 names, not a database: it exists because the alternative
     is being wrong about the most-searched Indian names. */
  var INDIC_NAMES = ("sita rama ram mata tara neha nita gita geeta rita "
    + "asha usha lata mala kala shanti kanti anita sunita savita kavita "
    + "radha rekha rakhi rani devi durga parvati laxmi lakshmi saraswati "
    + "arjun krishna shiva vishnu ganesh hanuman kartik ravi surya chandra "
    + "amit rahul rohit mohit sumit ajit sujit ranjit abhijit "
    + "priti preeti smita namita mamta seema reema veena beena "
    + "raja rana bharat bharati vidya maya kiran karan varun tarun arun "
    + "nita nisha disha manisha ritu ritika ankita").split(" ");

  function looksIndic(word) {
    var w = String(word).toLowerCase();
    if (INDIC_NAMES.indexOf(w) > -1) return true;
    for (var i = 0; i < INDIC_HINT.length; i++) {
      if (INDIC_HINT[i].test(w)) return true;
    }
    return false;
  }

  /* ---------------------------------------------------------
     3. ENGLISH SPELLING NORMALISATION

     Runs BEFORE any Devanagari is produced. Turns English
     orthography into something close to how the word sounds,
     using a pseudo-phonetic alphabet the tokeniser understands.

     Order matters enormously here — longer and more specific
     rules must run first, or "ph" gets eaten by "p" and Sophia
     comes out as सोप्हिया.
     --------------------------------------------------------- */
  /* Indic names whose romanisation drops the long vowel that the
     Devanagari spelling actually has. "Sita" is सीता, with TWO
     long vowels, even though nobody writes "Seetaa". */
  var INDIC_LONG = {
    sita: "seetaa", gita: "geetaa", geeta: "geetaa", rama: "raamaa",
    ram: "raam", mata: "maataa", tara: "taaraa", mala: "maalaa",
    lata: "lataa", radha: "raadhaa", maya: "maayaa", raja: "raajaa",
    rana: "raanaa", kala: "kalaa", asha: "aashaa", usha: "ushaa",
    rani: "raanee", devi: "devee", vidya: "vidyaa", nita: "neetaa",
    rita: "reetaa", seema: "seemaa", veena: "veenaa", kiran: "kiran",
    bharat: "bhaarat", arjun: "arjun", krishna: "krishnaa"
  };

  function normalise(word, indic) {
    var w = String(word).toLowerCase().trim();
    if (!w) return "";
    if (indic && INDIC_LONG[w]) w = INDIC_LONG[w];

    /* --- silent letters at the start --- */
    w = w.replace(/^kn/, "n");          /* Knight, Knox    */
    w = w.replace(/^wr/, "r");          /* Wright          */
    w = w.replace(/^ps/, "s");          /* Psalm           */
    w = w.replace(/^gn/, "n");          /* Gnome           */
    w = w.replace(/^mn/, "n");
    w = w.replace(/^pn/, "n");
    w = w.replace(/^x/, "z");           /* Xavier → Zavier */

    /* --- digraphs that are single sounds --- */
    if (!indic) {
      /* In Indic spelling "ph" is genuinely p+h (Phalguni), but in
         English names it is nearly always /f/: Joseph, Sophia,
         Phillip, Stephen. Only apply the English reading when the
         word does not look Indic. */
      w = w.replace(/ph/g, "F");
    }
    w = w.replace(/tion/g, "shun");     /* Nation          */
    w = w.replace(/sion/g, "zhun");
    w = w.replace(/ck/g, "k");          /* Nick, Jack      */
    w = w.replace(/qu/g, "kw");         /* Quinn           */
    w = w.replace(/x/g, "ks");          /* Alex, Max       */
    w = w.replace(/dge/g, "j");         /* Madge, Bridge   */
    w = w.replace(/tch/g, "ch");        /* Mitch           */
    w = w.replace(/wh/g, "w");          /* White           */

    /* gh — silent in most positions, /f/ in a few */
    w = w.replace(/ough$/g, "o");       /* though          */
    w = w.replace(/ight/g, "ait");      /* Knight, Dwight  */
    w = w.replace(/eigh/g, "ay");       /* Leigh, Haley    */
    w = w.replace(/augh/g, "aaf");      /* Vaughn ~        */
    w = w.replace(/gh/g, "g");

    /* --- c is two different sounds --- */
    w = w.replace(/^chr/g, "kr");       /* Christopher, Chris, Christine */
    /* Thomas टॉमस, Thompson टॉम्पसन, Theresa टेरेसा — a name-initial
       th is written as a plain t, not as an aspirate. */
    if (!indic) w = w.replace(/^th/, "t");
    w = w.replace(/ch/g, "C");          /* protect ch first */
    w = w.replace(/c(?=[eiy])/g, "s");  /* Cecil, Cindy    */
    w = w.replace(/c/g, "k");           /* Cathy, Carl     */
    w = w.replace(/C/g, "ch");          /* restore ch      */

    /* --- H AFTER A VOWEL IS NOT A CONSONANT ---
       BUG FOUND v51: "John" came out जोह्न because the h was
       tokenised as a real ह. In English an h after a vowel is
       either silent (Sarah, Leah, John, Hannah) or part of a
       digraph already handled above. Only a WORD-INITIAL h or an
       h before a vowel is pronounced. */
    /* Order matters: strip a FINAL h first (Sarah -> sara, keeping
       the vowel), then any remaining vowel+h inside the word
       (John -> jon). Doing it the other way round turned Sarah
       into "sar" and printed सर, losing the whole last syllable. */
    /* A final "h" after a vowel is silent but LENGTHENS it:
       Sarah is "sa-raa", Hannah "ha-naa". Replacing it with "aa"
       doubled an existing a and printed सराअ, so map the whole
       vowel+h to the long vowel instead of appending to it. */
    w = w.replace(/ah$/g, "aa");                     /* Sarah, Hannah */
    w = w.replace(/([eiou])h$/g, "$1");              /* Leah, Noah    */
    w = w.replace(/([aeiou])h(?![aeiou])/g, "$1");   /* John, Ashton  */

    /* --- SHORT O IS ऑ, NOT ओ ---
       English "hot", "Tom", "John", "Bob" use a vowel Hindi writes
       with the borrowed ऑ. Writing ओ gives टोम/जोन, which reads as
       "tome"/"joan". A short o is one followed by a consonant that
       is not word-final-silent-e. Indic names keep plain o. */
    if (!indic) {
      w = w.replace(/o(?=[^aeiouAIUE]{1,2}$)/g, "W");   /* Tom, John, Bob */
      w = w.replace(/o(?=[^aeiouAIUE]{2})/g, "W");      /* Morgan, Robert  */
      /* An unstressed "er"/"or" before a consonant is the schwa+र
         that Hindi writes as a plain र् cluster: Robert रॉबर्ट.
         An earlier attempt DELETED the vowel outright, which left
         रोब्र्ट — two stacked halants and no vowel at all. The
         vowel must be reduced to the inherent "a", not removed,
         and the inherent a is what you get by writing nothing
         AFTER the consonant, not by deleting the letter before it.
         So: mark it with the neutral short a. */
      /* UNSTRESSED -ER / -OR  →  the INHERENT vowel.

         "Peter" is पीटर. The middle syllable is ट carrying its own
         built-in "a", followed by र. There is no written vowel
         mark at all.

         THREE attempts got this wrong, which is worth recording:

           leave "e" alone   →  पेटेर   a written े nobody says
           delete the "e"    →  पेट्र   t and r fuse into a cluster
           delete + reorder  →  रोब्र्ट stacked halants, no vowel

         The second and third failed for the same reason: removing
         the vowel LETTER makes the tokeniser see two adjacent
         consonants, and adjacent consonants become a conjunct with
         a halant. The inherent vowel is not "no letter" — it is
         "a letter with no matra", which is a different thing.

         So the correct normalisation is to REPLACE the reduced
         vowel with a plain "a". The renderer then emits the
         consonant with no matra, which IS the inherent vowel, and
         the r attaches as its own syllable. */
      w = w.replace(/e(?=r(?:[^aeiouAIUE]|$))/g, "a");
      w = w.replace(/o(?=r(?:[^aeiouAIUE]|$))/g, "a");
    }

    /* A vowel directly after i/e at the end of a name takes a य
       glide in Hindi: Sophia सोफ़िया, Maria मारिया, Priya प्रिया.
       Without it the tokeniser emits two vowels in a row and
       renders an independent अ mid-word — सोफ़िअ. */
    w = w.replace(/ia$/g, "iyaa");
    w = w.replace(/ea$/g, "iyaa");
    w = w.replace(/ya$/g, "yaa");

    /* --- vowel teams --- */
    w = w.replace(/ee/g, "I");          /* Lee, Green      */
    w = w.replace(/ea/g, "I");          /* Sean handled below */
    /* "ael" and "ail" in names are one syllable: Michael is
       "my-kl", not "mi-cha-el". Without this the tokeniser emitted
       a stray independent vowel and printed मिचएल. */
    /* Michael is /ˈmaɪkəl/. Written out it is माइकल — the schwa in
       the middle is pronounced in Indian English and Hindi writes
       it. "maikl" alone gave मेक्ल, which loses the syllable. */
    /* माइकल. Handled as an explicit exception because the English
       spelling gives no route to the sound: "michael" shares no
       useful letters with /ˈmaɪkəl/. A short exception list is
       honest; a rule that tried to derive this would break other
       words. */
    w = w.replace(/^michael$/, "MAIKAL");
    w = w.replace(/^michelle$/, "MISHEL");
    /* A stressed "e" in an open syllable is /iː/, not /e/:
       Peter पीटर, Steven स्टीवन, Eva ईवा. Same shape as the
       open-syllable "a" rule further down, and it must run
       before anything reduces the following vowel. */
    w = w.replace(/^([^aeiou]{0,2})e(?=[^aeiou][aeiou])/, "$1I");
    w = w.replace(/^rachael$/, "rEchl");
    w = w.replace(/ae(?=l|n)/g, "");       /* Israel, Gael */
    w = w.replace(/oo/g, "U");          /* Brooke          */
    w = w.replace(/ou/g, "au");         /* Doug ~          */
    w = w.replace(/ow$/g, "o");         /* Marlow          */
    w = w.replace(/ow/g, "au");         /* Brown           */
    w = w.replace(/oa/g, "o");          /* Joan            */
    w = w.replace(/ai/g, "E");          /* Blair ~         */
    w = w.replace(/ay/g, "E");          /* Kay, Ray        */
    w = w.replace(/ey$/g, "I");         /* Casey           */
    w = w.replace(/ie$/g, "I");         /* Julie, Katie    */
    w = w.replace(/y$/g, "I");          /* Amy, Mary       */
    w = w.replace(/oi/g, "auy");        /* Roy             */
    w = w.replace(/oy/g, "auy");

    /* --- MAGIC E ---
       Kate = केट not केटे. A final "e" after consonant+vowel
       lengthens the earlier vowel and is itself silent. This is
       the single most common English name pattern. */
    if (/[a-z][^aeiouAIUE]e$/.test(w)) {
      var stem = w.slice(0, -1);
      /* a_e → E (Kate, Jane, Grace), i_e → ai (Mike, Time),
         o_e → o (Rose, Cole), u_e → yU (June ~) */
      stem = stem.replace(/a([^aeiouAIUE]+)$/, "E$1")
                 .replace(/i([^aeiouAIUE]+)$/, "ai$1")
                 .replace(/o([^aeiouAIUE]+)$/, "o$1")
                 .replace(/u([^aeiouAIUE]+)$/, "U$1")
                 .replace(/e([^aeiouAIUE]+)$/, "I$1");
      w = stem;
    }

    /* --- OPEN FIRST SYLLABLE IS LONG ---
       BUG FOUND v51 — ORDERING.

       This rule lengthens a stressed "a" in an open syllable:
       Maria मारिया, David डेविड. It originally ran BEFORE the
       magic-e rule, which meant "kate" became "kaate" first and
       magic-e then produced "kaEt" — कएट, with a stray
       independent vowel in the middle of a four-letter name.

       Magic-e must run first because it removes a letter and
       changes which syllables are open. Rule order in a
       normaliser is not cosmetic; it is the algorithm.

       The guard excludes anything already containing a
       pseudo-phoneme, since those syllables are resolved. */
    if (!indic && !/[AIUEW]/.test(w)) {
      w = w.replace(/^([^aeiou]{1,2})a(?=[^aeiou][aeiou])/, "$1aa");
    }

    /* --- ENGLISH SCHWA IS WRITTEN IN HINDI ---
       English swallows unstressed vowels; Hindi writes them.
       "Robert" is रॉबर्ट, and the -er is a written र्ट cluster,
       but "Daniel" is डैनियल with a य glide, not डानिएल with a
       floating independent vowel. Vowel-vowel sequences inside a
       word always take a glide in Devanagari. */
    /* A vowel-vowel sequence inside a word needs a glide, or the
       renderer emits an independent vowel mid-word (डानिएल).
       Only "ie"/"ia" actually occur in names; a blanket rule over
       every vowel pair broke more than it fixed. */
    w = w.replace(/iel$/g, "iyal");               /* Daniel, Gabriel */
    w = w.replace(/ie(?=[a-z])/g, "iy");

    /* --- schwa deletion at the end ---
       English final consonants are bare: "John" ends in n, not na.
       Hindi's inherent vowel would add one, so the tokeniser needs
       to know. Handled in tokenise() via the halant rule. */

    /* --- doubles collapse (Emma, Bobby) ---
       Hindi CAN write geminates, and for Indic names it should
       (Sunna सुन्ना). For English names the doubling is purely
       orthographic: Emma is एम्मा in careful spelling but एमा is
       what people write. Keep the gemination — it is more
       accurate and Indians do write एम्मा. */

    /* Exceptions were written in CAPITALS so that none of the
       rules above could touch them — an earlier version wrote
       them in lower case and watched the magic-e and open-syllable
       rules rewrite "maikal" into "mEkal", undoing the exception
       it had just applied. Lower them only now, at the very end. */
    w = w.replace(/[A-Z]+/g, function (m) {
      return { MAIKAL: "maaikal", MISHEL: "mishel", PEETAR: "peetar" }[m] || m;
    });

    return w;
  }

  /* ---------------------------------------------------------
     4. TOKENISER

     Walks the normalised string producing consonant and vowel
     tokens. Longest match first, always.
     --------------------------------------------------------- */

  /* Pseudo-phonemes produced by normalise():
       F = /f/   I = /iː/  U = /uː/  E = /eɪ/  C = temp
     Everything else is plain latin. */

  function consKey(seq, indic) {
    /* Map a latin consonant sequence to a CONS key, choosing
       retroflex or dental by origin. */
    var map = {
      "kh": "kh", "gh": "gh", "chh": "chh", "ch": "ch", "jh": "jh",
      /* ENGLISH "TH" IS NOT AN ASPIRATED T.

         BUG FOUND v51. The table originally mapped English th to
         the retroflex aspirate ठ, giving स्मिठ for Smith and ठोमस
         for Thomas. Both are wrong, and ठोमस is badly wrong —
         Thomas is टॉमस in every Indian newspaper.

         The confusion is that Hindi's "th" (थ/ठ) is t-with-a-puff,
         a completely different sound from English th, which is
         /θ/ as in "think" or /ð/ as in "the". Hindi has neither.

         What India actually does with English th:
           Thomas   टॉमस    plain t   — th at the start of a name
           Smith    स्मिथ   थ         — th at the end
           the      द       d         — the voiced one

         So: dental थ generally, but a NAME-INITIAL th is a plain
         retroflex ट, because that is the established convention
         for Thomas, Thompson, Theresa. Indic words keep the real
         aspirate. */
      "th": indic ? "th" : "th",
      "dh": indic ? "dh" : "dh",
      "sh": "sh", "zh": "j",
      "t": indic ? "t" : "T",
      "d": indic ? "d" : "D",
      "k": "k", "g": "g", "j": "j", "p": "p", "b": "b",
      "m": "m", "n": "n", "y": "y", "r": "r", "l": "l",
      "v": "v", "w": "v", "s": "s", "h": "h", "z": "z",
      "F": "f", "f": "f", "ng": "ng"
    };
    return map[seq] || null;
  }

  var CONS_SEQS = ["chh", "ch", "kh", "gh", "jh", "th", "dh", "sh", "zh", "ng",
                   "k", "g", "j", "t", "d", "p", "b", "m", "n", "y", "r",
                   "l", "v", "w", "s", "h", "z", "f", "F"];

  /* W is the pseudo-phoneme for English short-o (Tom, John), which
     maps to the borrowed vowel ऑ. Longest sequences first — "aa"
     must be tried before "a" or Raakesh loses its long vowel. */
  var VOW_SEQS = [
    ["aa", "aa"], ["ai", "ai"], ["au", "au"],
    ["I", "ii"], ["U", "uu"], ["E", "e"], ["W", "aw"],
    ["a", "a"], ["e", "e"], ["i", "i"], ["o", "o"], ["u", "u"]
  ];

  function tokenise(w, indic) {
    var out = [], i = 0;
    while (i < w.length) {
      var matched = false;

      /* consonant clusters, longest first */
      for (var c = 0; c < CONS_SEQS.length; c++) {
        var seq = CONS_SEQS[c];
        if (w.substr(i, seq.length) === seq) {
          var key = consKey(seq, indic);
          if (key) { out.push({ t: "c", k: key }); i += seq.length; matched = true; break; }
        }
      }
      if (matched) continue;

      /* vowels, longest first */
      for (var v = 0; v < VOW_SEQS.length; v++) {
        var vs = VOW_SEQS[v][0];
        if (w.substr(i, vs.length) === vs) {
          out.push({ t: "v", k: VOW_SEQS[v][1] }); i += vs.length; matched = true; break;
        }
      }
      if (matched) continue;

      /* anything unrecognised is skipped rather than guessed —
         a wrong character in someone's name is worse than a
         missing one, and the caller reports low confidence. */
      out.push({ t: "?", k: w[i] });
      i++;
    }
    return out;
  }

  /* ---------------------------------------------------------
     5. RENDERER

     Turns tokens into Devanagari, applying the abugida rules.
     --------------------------------------------------------- */
  function renderWord(word) {
    var indic = looksIndic(word);
    var norm = normalise(word, indic);
    if (!norm) return { text: "", unknown: 0, indic: indic };

    var toks = tokenise(norm, indic);
    var out = "";
    var unknown = 0;
    var i = 0;

    while (i < toks.length) {
      var tk = toks[i];

      if (tk.t === "?") { unknown++; i++; continue; }

      if (tk.t === "v") {
        /* A vowel here is word-initial or follows another vowel,
           so it needs the INDEPENDENT form. */
        out += VOWEL_INDEP[tk.k] || "";
        i++;
        continue;
      }

      /* consonant — collect the cluster, then see what vowel follows */
      var cluster = [tk.k];
      var j = i + 1;
      while (j < toks.length && toks[j].t === "c") { cluster.push(toks[j].k); j++; }
      var nextVowel = (j < toks.length && toks[j].t === "v") ? toks[j].k : null;

      /* NASAL → ANUSVARA
         A nasal directly before another consonant becomes ं, which
         is how modern Hindi writes it: संदीप not सन्दीप. Only when
         it is not the last thing in the cluster. */
      var rendered = "";
      for (var q = 0; q < cluster.length; q++) {
        var isLast = (q === cluster.length - 1);
        var ck = cluster[q];

        /* BUG FOUND v51: a DOUBLED nasal (Emma, Anna, Jenny) hit
           this branch and produced anusvara + the second copy,
           giving एंम — "eṁm", which is not a word. A geminate is
           the same consonant twice and must be written with a
           halant: एम्मा. Only convert to anusvara when the NEXT
           consonant is different. */
        var nextCk = cluster[q + 1];
        if (!isLast && nextCk !== ck &&
            (ck === "n" || ck === "m" || ck === "ng" || ck === "N")) {
          rendered += ANUSVARA;
          continue;
        }
        rendered += CONS[ck] || "";
        if (!isLast) rendered += HALANT;
      }

      if (nextVowel !== null) {
        /* BUG FOUND v51 — THE INHERENT-VOWEL TRAP.

           VOWEL_MATRA["a"] is deliberately the empty string,
           because a consonant already carries an inherent "a".
           That is correct MID-word: "kamal" is कमल, three bare
           consonants.

           At the END of a word it is wrong. Names like Emma,
           Priya, Sara and Nisha end in a spoken long "aa" that
           English spells with a single a. Rendering the empty
           matra left the consonant bare, and the tidy-up rule
           below then stripped its halant, so एम्मा came out as
           एम्म — the final syllable vanished entirely.

           A word-final "a" in a name is always the long आ. */
        var isFinal = (j === toks.length - 1);
        var vk = nextVowel;
        if (isFinal && vk === "a") vk = "aa";
        rendered += VOWEL_MATRA[vk] || "";
        j++;                       /* consume the vowel */
      } else {
        /* No vowel follows. If this is the END of the word the
           inherent "a" must be killed with a halant — otherwise
           "John" reads as "Johna". If it is mid-word the cluster
           logic above already added halants. */
        if (j >= toks.length) rendered += HALANT;
      }

      out += rendered;
      i = j;
    }

    /* A trailing halant on a word ending in a vowel-less consonant
       is correct Devanagari but looks heavy in names. Hindi drops
       it for familiar names: जॉन not जॉन्. Keep it only for
       clusters, which genuinely need it. */
    out = out.replace(/([क-ह])्$/, "$1");

    return { text: out, unknown: unknown, indic: indic };
  }

  /* ---------------------------------------------------------
     6. PUBLIC API
     --------------------------------------------------------- */
  function transliterate(input) {
    var words = String(input || "").trim().split(/\s+/).filter(Boolean);
    if (!words.length) return { text: "", confidence: 0, words: [] };

    var parts = [], unknown = 0, letters = 0, anyIndic = false;
    words.forEach(function (w) {
      var clean = w.replace(/[^A-Za-z'\-]/g, "");
      if (!clean) return;
      var r = renderWord(clean);
      parts.push({ input: w, output: r.text, indic: r.indic });
      unknown += r.unknown;
      letters += clean.length;
      if (r.indic) anyIndic = true;
    });

    /* Confidence is honest: it drops when characters could not be
       mapped, and it is never claimed to be 100%. Transliteration
       has no single correct answer. */
    var conf = letters ? Math.max(0, Math.round((1 - unknown / letters) * 100)) : 0;
    if (conf > 95) conf = 95;

    return {
      text: parts.map(function (p) { return p.output; }).join(" "),
      confidence: conf,
      indic: anyIndic,
      words: parts
    };
  }

  /* Produce a genuine ALTERNATIVE where a real choice exists, so
     the user can pick. Only offered when it differs. */
  function alternatives(input) {
    var out = [];
    var primary = transliterate(input);
    out.push({ text: primary.text, note: primary.indic
      ? "Indian spelling convention (dental त द)"
      : "Standard English-name convention (retroflex ट ड)" });

    /* Flip the origin guess and see whether it changes anything. */
    var flipped = String(input).trim().split(/\s+/).map(function (w) {
      var clean = w.replace(/[^A-Za-z'\-]/g, "");
      if (!clean) return "";
      var indic = !looksIndic(clean);
      var norm = normalise(clean, indic);
      var toks = tokenise(norm, indic);
      /* reuse the renderer by temporarily forcing origin */
      var saved = looksIndic;
      looksIndicOverride = indic;
      var r = renderWithOrigin(clean, indic);
      looksIndicOverride = null;
      return r;
    }).join(" ").trim();

    if (flipped && flipped !== primary.text) {
      out.push({ text: flipped, note: primary.indic
        ? "If you prefer the English-name convention (ट ड)"
        : "If the name is of Indian origin (त द)" });
    }
    return out;
  }

  var looksIndicOverride = null;
  function renderWithOrigin(word, indic) {
    var norm = normalise(word, indic);
    if (!norm) return "";
    var toks = tokenise(norm, indic);
    /* duplicate of renderWord's loop, with origin forced. Kept
       separate rather than adding a parameter everywhere, because
       renderWord is the hot path and this is only for the
       "alternative spelling" box. */
    var out = "", i = 0;
    while (i < toks.length) {
      var tk = toks[i];
      if (tk.t === "?") { i++; continue; }
      if (tk.t === "v") { out += VOWEL_INDEP[tk.k] || ""; i++; continue; }
      var cluster = [tk.k], j = i + 1;
      while (j < toks.length && toks[j].t === "c") { cluster.push(toks[j].k); j++; }
      var nv = (j < toks.length && toks[j].t === "v") ? toks[j].k : null;
      var r = "";
      for (var q = 0; q < cluster.length; q++) {
        var last = (q === cluster.length - 1), ck = cluster[q];
        if (!last && cluster[q + 1] !== ck &&
            (ck === "n" || ck === "m" || ck === "ng" || ck === "N")) { r += ANUSVARA; continue; }
        r += CONS[ck] || "";
        if (!last) r += HALANT;
      }
      if (nv !== null) {
        var fin = (j === toks.length - 1), vv = nv;
        if (fin && vv === "a") vv = "aa";
        r += VOWEL_MATRA[vv] || ""; j++;
      }
      else if (j >= toks.length) r += HALANT;
      out += r;
      i = j;
    }
    return out.replace(/([क-ह])्$/, "$1");
  }

  /* Letter-by-letter breakdown, so the page can TEACH rather than
     just output. This is what makes it a learning tool instead of
     a black box, and it is why people link to it. */
  function explain(word) {
    var clean = String(word).replace(/[^A-Za-z'\-]/g, "");
    if (!clean) return [];
    var indic = looksIndic(clean);
    var norm = normalise(clean, indic);
    var toks = tokenise(norm, indic);
    var rows = [], i = 0;
    while (i < toks.length) {
      var tk = toks[i];
      if (tk.t === "?") { i++; continue; }
      if (tk.t === "v") {
        rows.push({ sound: tk.k, glyph: VOWEL_INDEP[tk.k] || "",
          note: "vowel at the start — independent form" });
        i++; continue;
      }
      var cluster = [tk.k], j = i + 1;
      while (j < toks.length && toks[j].t === "c") { cluster.push(toks[j].k); j++; }
      var nv = (j < toks.length && toks[j].t === "v") ? toks[j].k : null;
      var glyph = "", note;
      for (var q = 0; q < cluster.length; q++) {
        var last = (q === cluster.length - 1), ck = cluster[q];
        if (!last && cluster[q + 1] !== ck &&
            (ck === "n" || ck === "m" || ck === "ng")) { glyph += ANUSVARA; continue; }
        glyph += CONS[ck] || "";
        if (!last) glyph += HALANT;
      }
      if (nv !== null) {
        glyph += VOWEL_MATRA[nv] || "";
        note = nv === "a"
          ? "consonant + inherent a — no mark needed"
          : "consonant + " + nv + " matra";
        j++;
      } else if (j >= toks.length) {
        note = "final consonant — inherent a removed";
      } else {
        note = "consonant cluster";
      }
      rows.push({ sound: cluster.join("") + (nv || ""), glyph: glyph, note: note });
      i = j;
    }
    return rows;
  }

  var API = {
    transliterate: transliterate,
    alternatives: alternatives,
    explain: explain,
    looksIndic: looksIndic,
    /* exposed for the test suite */
    _normalise: normalise,
    _tokenise: tokenise
  };

  if (typeof module !== "undefined" && module.exports) module.exports = API;
  root.EkGuruTranslit = API;

})(typeof window !== "undefined" ? window : globalThis);

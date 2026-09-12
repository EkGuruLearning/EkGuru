/* =========================================================
   EkGuru — PRACTICE BANK  (single source of truth · v100)
   ---------------------------------------------------------
   Question banks for the practice labs. Every item is a
   multiple-choice, ordering or fill-in question with one clear
   answer and a short explanation. The content is basic, checked
   Hindi — deliberately conservative so the drills stay accurate.

   HONEST FRAMING (enforced by the engine, not just this comment):
   these are practice drills. A multiple-choice answer tests
   recognition and recall of forms, NOT the ability to speak or
   understand a native speaker at full speed. Nothing here is a
   certified test and no score is a fluency score.
   ========================================================= */
window.EKGURU_PRACTICE_BANK = {

  /* ---------- Vocabulary: word → meaning ---------- */
  vocabulary: [
    { q: "What does पानी mean?", a: "water", opts: ["water", "bread", "milk", "tea"], explain: "पानी (paani) is water — the word you will use most in India." },
    { q: "What does रोटी mean?", a: "bread", opts: ["rice", "bread", "vegetable", "water"], explain: "रोटी (roti) is the flat bread eaten with nearly every meal." },
    { q: "What does चाय mean?", a: "tea", opts: ["coffee", "milk", "tea", "sugar"], explain: "चाय (chaay) is tea — and 'chai' is one of the few Hindi words the world already knows." },
    { q: "What does घर mean?", a: "house", opts: ["door", "house", "car", "room"], explain: "घर (ghar) is house or home." },
    { q: "What does किताब mean?", a: "book", opts: ["pen", "paper", "book", "bag"], explain: "किताब (kitaab) is book — borrowed into Hindi from Arabic." },
    { q: "What does दोस्त mean?", a: "friend", opts: ["brother", "friend", "teacher", "neighbour"], explain: "दोस्त (dost) is friend." },
    { q: "What does खाना mean?", a: "food", opts: ["water", "food", "sleep", "work"], explain: "खाना (khaana) is food — also the verb 'to eat'." },
    { q: "What does नमस्ते mean?", a: "hello", opts: ["goodbye", "hello", "thank you", "sorry"], explain: "नमस्ते (namaste) is hello — and also goodbye." },
    { q: "What does धन्यवाद mean?", a: "thank you", opts: ["please", "thank you", "welcome", "excuse me"], explain: "धन्यवाद (dhanyavaad) is thank you. In speech people often say शुक्रिया (shukriya) instead." },
    { q: "What does हाँ mean?", a: "yes", opts: ["no", "yes", "maybe", "later"], explain: "हाँ (haan) is yes; नहीं (nahin) is no." },
    { q: "What does बड़ा mean?", a: "big", opts: ["small", "big", "tall", "short"], explain: "बड़ा (bada) is big; छोटा (chhota) is small." },
    { q: "What does अच्छा mean?", a: "good", opts: ["bad", "good", "new", "old"], explain: "अच्छा (achchha) is good. It also works as a filler word like 'okay'." },
    { q: "What does पैसा mean?", a: "money", opts: ["money", "time", "work", "food"], explain: "पैसा (paisa) is money — the word that gave English 'paisa'." },
    { q: "What does स्कूल mean?", a: "school", opts: ["hospital", "school", "shop", "station"], explain: "स्कूल (skool) is school — a borrowing from English written in Devanagari." },
    { q: "What does प्यार mean?", a: "love", opts: ["anger", "love", "fear", "joy"], explain: "प्यार (pyaar) is love." },
    { q: "What does दिन mean?", a: "day", opts: ["night", "day", "week", "month"], explain: "दिन (din) is day; रात (raat) is night." },
    { q: "What does नया mean?", a: "new", opts: ["old", "new", "young", "small"], explain: "नया (naya) is new." },
    { q: "What does आदमी mean?", a: "man", opts: ["woman", "man", "child", "boy"], explain: "आदमी (aadmi) is man; औरत (aurat) is woman." },
    { q: "What does बच्चा mean?", a: "child", opts: ["adult", "child", "teacher", "doctor"], explain: "बच्चा (bachcha) is child." },
    { q: "What does सुंदर mean?", a: "beautiful", opts: ["ugly", "beautiful", "tall", "clean"], explain: "सुंदर (sundar) is beautiful." }
  ],

  /* ---------- Grammar: gender / plural / agreement / tense ---------- */
  grammar: [
    { skill: "gender", q: "रोटी (bread) is which gender?", a: "feminine", opts: ["masculine", "feminine"], explain: "Words ending in -ī (ई) are almost always feminine, like रोटी." },
    { skill: "gender", q: "घर (house) is which gender?", a: "masculine", opts: ["masculine", "feminine"], explain: "घर ends in a consonant — the default is masculine." },
    { skill: "gender", q: "किताब (book) is which gender?", a: "feminine", opts: ["masculine", "feminine"], explain: "किताब is feminine even though it ends in a consonant — an exception worth memorising." },
    { skill: "gender", q: "लड़का (boy) is which gender?", a: "masculine", opts: ["masculine", "feminine"], explain: "Words ending in -ā (आ) like लड़का are masculine." },
    { skill: "plural", q: "The plural of लड़का (boy) is…", a: "लड़के (ladke)", opts: ["लड़के (ladke)", "लड़का (ladka)", "लड़की (ladki)", "लड़कों (ladkon)"], explain: "Masculine -ā nouns change to -e in the direct plural: लड़का → लड़के." },
    { skill: "plural", q: "The plural of लड़की (girl) is…", a: "लड़कियाँ (ladkiyaan)", opts: ["लड़कियाँ (ladkiyaan)", "लड़की (ladki)", "लड़के (ladke)", "लड़कियों (ladkiyon)"], explain: "Feminine -ī nouns change to -iyaan in the direct plural: लड़की → लड़कियाँ." },
    { skill: "agreement", q: "A man says: I go — मैं ____ हूँ", a: "जाता (jaata)", opts: ["जाता (jaata)", "जाती (jaati)", "जाते (jaate)", "गया (gaya)"], explain: "A male speaker uses the -aa ending: मैं जाता हूँ." },
    { skill: "agreement", q: "A woman says: I go — मैं ____ हूँ", a: "जाती (jaati)", opts: ["जाता (jaata)", "जाती (jaati)", "जाते (jaate)", "गई (gai)"], explain: "A female speaker uses the -ii ending: मैं जाती हूँ." },
    { skill: "tense", q: "Present: मैं खाता हूँ means…", a: "I eat", opts: ["I ate", "I eat", "I will eat", "I am eating right now"], explain: "मैं खाता हूँ is the habitual present: 'I eat'." },
    { skill: "tense", q: "Future: मैं खाऊँगा means…", a: "I will eat", opts: ["I ate", "I eat", "I will eat", "I should eat"], explain: "The -ūngā / -ūngī ending marks the future: मैं खाऊँगा, 'I will eat'." },
    { skill: "tense", q: "Past: मैंने खाया means…", a: "I ate", opts: ["I ate", "I eat", "I will eat", "I am eating"], explain: "With transitive verbs the past uses ने and the -ā form agrees with the object: मैंने खाया, 'I ate (it)'." },
    { skill: "agreement", q: "Which is correct for a woman: 'I am happy'?", a: "मैं खुश हूँ", opts: ["मैं खुश हूँ", "मैं खुश है", "मैं खुश हैं", "मैं खुश हो"], explain: "खुश doesn't change with gender; only the verb agrees: मैं … हूँ." }
  ],

  /* ---------- Sentence builder: put the words in order ---------- */
  sentences: [
    { q: "Build: I eat bread", words: ["खाता", "मैं", "रोटी", "हूँ"], answer: ["मैं", "रोटी", "खाता", "हूँ"], explain: "Hindi is Subject–Object–Verb: I bread eat am." },
    { q: "Build: She reads a book", words: ["पढ़ती", "वह", "है", "किताब"], answer: ["वह", "किताब", "पढ़ती", "है"], explain: "वह किताब पढ़ती है — subject, object, verb, auxiliary." },
    { q: "Build: We live in Delhi", words: ["में", "रहते", "हम", "दिल्ली", "हैं"], answer: ["हम", "दिल्ली", "में", "रहते", "हैं"], explain: "दिल्ली में — 'Delhi in'. Postpositions come after the noun." },
    { q: "Build: What is this?", words: ["क्या", "यह", "है"], answer: ["यह", "क्या", "है"], explain: "यह क्या है? — the question word sits just before the verb." },
    { q: "Build: My name is Sita", words: ["सीता", "नाम", "मेरा", "है"], answer: ["मेरा", "नाम", "सीता", "है"], explain: "मेरा नाम सीता है — 'my name Sita is'." },
    { q: "Build: I want tea", words: ["चाहिए", "मुझे", "चाय"], answer: ["मुझे", "चाय", "चाहिए"], explain: "मुझे चाय चाहिए — 'to me tea is wanted'." },
    { q: "Build: Where do you live?", words: ["रहते", "आप", "कहाँ", "हैं"], answer: ["आप", "कहाँ", "रहते", "हैं"], explain: "आप कहाँ रहते हैं? — question word before the verb." },
    { q: "Build: He goes to school", words: ["स्कूल", "वह", "जाता", "है"], answer: ["वह", "स्कूल", "जाता", "है"], explain: "वह स्कूल जाता है — subject, destination, verb." },
    { q: "Build: I don't understand", words: ["नहीं", "मैं", "समझता"], answer: ["मैं", "नहीं", "समझता"], explain: "नहीं goes right before the verb: मैं नहीं समझता." },
    { q: "Build: This is my house", words: ["घर", "मेरा", "यह", "है"], answer: ["यह", "मेरा", "घर", "है"], explain: "यह मेरा घर है — 'this my house is'." },
    { q: "Build: I will go tomorrow", words: ["जाऊँगा", "कल", "मैं"], answer: ["मैं", "कल", "जाऊँगा"], explain: "मैं कल जाऊँगा — the verb stays last even in the future." },
    { q: "Build: Give me water", words: ["पानी", "मुझे", "दीजिए"], answer: ["मुझे", "पानी", "दीजिए"], explain: "मुझे पानी दीजिए — the polite 'give' form." }
  ],

  /* ---------- Verb forms: fill in the correct form ---------- */
  verbs: [
    { q: "to go — a man says: मैं ____ हूँ", a: "जाता", opts: ["जाता", "जाती", "जाते", "जाऊँगा"], explain: "Male speaker, present: मैं जाता हूँ." },
    { q: "to go — a woman says: मैं ____ हूँ", a: "जाती", opts: ["जाता", "जाती", "जाते", "गई"], explain: "Female speaker, present: मैं जाती हूँ." },
    { q: "to eat — I will eat: मैं ____", a: "खाऊँगा", opts: ["खाता", "खाऊँगा", "खाया", "खाओ"], explain: "Future: मैं खाऊँगा." },
    { q: "to be — I am: मैं ____", a: "हूँ", opts: ["है", "हूँ", "हो", "हैं"], explain: "मैं हूँ — 'I am'. है is he/she/it, हैं is they/you-polite." },
    { q: "to be — he is: वह ____", a: "है", opts: ["है", "हूँ", "हो", "हैं"], explain: "वह है — 'he/she is'." },
    { q: "to do — a man: मैं काम ____ हूँ", a: "करता", opts: ["करता", "करती", "करते", "किया"], explain: "करना (to do) → मैं काम करता हूँ for a male speaker." },
    { q: "to drink — she drinks tea: वह चाय ____ है", a: "पीती", opts: ["पीता", "पीती", "पीते", "पिया"], explain: "पीना (to drink) → वह चाय पीती है (feminine)." },
    { q: "to come — you (polite) come: आप ____ हैं", a: "आते", opts: ["आता", "आती", "आते", "आया"], explain: "आप always takes the polite plural form: आप आते हैं." },
    { q: "to speak — I speak Hindi: मैं हिंदी ____ हूँ", a: "बोलता", opts: ["बोलता", "बोलती", "बोलते", "बोला"], explain: "बोलना (to speak) → मैं हिंदी बोलता हूँ (male)." },
    { q: "to see — I saw: मैंने ____", a: "देखा", opts: ["देखता", "देखी", "देखा", "देखूँगा"], explain: "Past of देखना: मैंने देखा." }
  ],

  /* ---------- Listening: hear a word (computer voice), choose it ---------- */
  listening: [
    { q: "You hear a greeting. What was it?", a: "नमस्ते", opts: ["नमस्ते", "धन्यवाद", "अलविदा", "क्षमा"], tts: "नमस्ते", explain: "नमस्ते is hello." },
    { q: "You hear: water. Which word?", a: "पानी", opts: ["पानी", "रोटी", "चाय", "दूध"], tts: "पानी", explain: "पानी is water." },
    { q: "You hear: thank you. Which word?", a: "धन्यवाद", opts: ["नमस्ते", "धन्यवाद", "शुभ रात्रि", "फिर मिलेंगे"], tts: "धन्यवाद", explain: "धन्यवाद is thank you." },
    { q: "You hear: how are you? Which phrase?", a: "आप कैसे हैं?", opts: ["आप कैसे हैं?", "आपका नाम क्या है?", "आप कहाँ रहते हैं?", "क्या हाल है?"], tts: "आप कैसे हैं?", explain: "आप कैसे हैं? — how are you (polite)." },
    { q: "You hear: my name is Ravi. Which phrase?", a: "मेरा नाम रवि है", opts: ["मेरा नाम रवि है", "मैं ठीक हूँ", "मैं भारत से हूँ", "मुझे चाय चाहिए"], tts: "मेरा नाम रवि है", explain: "मेरा नाम रवि है — my name is Ravi." },
    { q: "You hear: yes. Which word?", a: "हाँ", opts: ["हाँ", "नहीं", "क्या", "क्यों"], tts: "हाँ", explain: "हाँ is yes." },
    { q: "You hear: no. Which word?", a: "नहीं", opts: ["हाँ", "नहीं", "कभी", "शायद"], tts: "नहीं", explain: "नहीं is no." },
    { q: "You hear: I want tea. Which phrase?", a: "मुझे चाय चाहिए", opts: ["मुझे चाय चाहिए", "मुझे भूख लगी है", "मैं खा रहा हूँ", "मुझे नींद आ रही है"], tts: "मुझे चाय चाहिए", explain: "मुझे चाय चाहिए — I want tea." },
    { q: "You hear: goodbye. Which word?", a: "अलविदा", opts: ["नमस्ते", "अलविदा", "सुप्रभात", "शुभ रात्रि"], tts: "अलविदा", explain: "अलविदा is goodbye (from Arabic)." },
    { q: "You hear: good night. Which phrase?", a: "शुभ रात्रि", opts: ["सुप्रभात", "शुभ रात्रि", "नमस्कार", "फिर मिलेंगे"], tts: "शुभ रात्रि", explain: "शुभ रात्रि — good night." },
    { q: "You hear: food. Which word?", a: "खाना", opts: ["खाना", "पानी", "घर", "रास्ता"], tts: "खाना", explain: "खाना is food." },
    { q: "You hear: where are you from? Which phrase?", a: "आप कहाँ से हैं?", opts: ["आप कहाँ से हैं?", "आप कहाँ जा रहे हैं?", "आपका क्या नाम है?", "आप कैसे हैं?"], tts: "आप कहाँ से हैं?", explain: "आप कहाँ से हैं? — where are you from?" }
  ],

  /* ---------- Pronunciation: minimal pairs (playback, no auto-scoring) ---------- */
  minimalPairs: [
    { q: "क vs ख — which has a puff of air?", a: "ख (kha)", opts: ["क (ka)", "ख (kha)"], explain: "ख is aspirated — hold paper in front of your mouth and it moves." },
    { q: "ग vs घ — which has a puff of air?", a: "घ (gha)", opts: ["ग (ga)", "घ (gha)"], explain: "घ is the aspirated one." },
    { q: "ट vs ठ — which is aspirated?", a: "ठ (tha)", opts: ["ट (ta)", "ठ (tha)"], explain: "ठ is aspirated retroflex t." },
    { q: "द vs ध — which is aspirated?", a: "ध (dha)", opts: ["द (da)", "ध (dha)"], explain: "ध is aspirated d." },
    { q: "ब vs भ — which is aspirated?", a: "भ (bha)", opts: ["ब (ba)", "भ (bha)"], explain: "भ is aspirated b." },
    { q: "Which pair is: your tongue curls back (retroflex)?", a: "ट/ड (ta/da)", opts: ["ट/ड (ta/da)", "त/द (ta/da)", "क/ग (ka/ga)", "प/ब (pa/ba)"], explain: "ट and ड are retroflex — tongue tip curled back to the roof of the mouth." },
    { q: "Which pair is dental — tongue touching the teeth?", a: "त/द (ta/da)", opts: ["ट/ड (ta/da)", "त/द (ta/da)", "क/ग (ka/ga)", "फ/भ (pha/bha)"], explain: "त and द are dental — tongue against the back of the teeth." },
    { q: "श vs स — which sounds like English 'sh'?", a: "श (sha)", opts: ["श (sha)", "स (sa)"], explain: "श is like 'sh' in 'ship'; स is like 's' in 'sun'." }
  ],

  /* ---------- Placement: rough diagnostic (NOT certified) ---------- */
  placement: [
    { q: "Can you read this word: नमस्ते", a: "yes — namaste", opts: ["yes — namaste", "I can sound out some letters", "not yet"], explain: "If you read it instantly, the script is already yours. If you sounded it out, start with the alphabet guide anyway." },
    { q: "Which means 'thank you'?", a: "धन्यवाद", opts: ["धन्यवाद", "नमस्ते", "अलविदा", "सुप्रभात"], explain: "धन्यवाद is thank you." },
    { q: "Which word is 'water'?", a: "पानी", opts: ["पानी", "रोटी", "चाय", "दूध"], explain: "पानी is water." },
    { q: "What is the correct order: I eat bread", a: "मैं रोटी खाता हूँ", opts: ["मैं रोटी खाता हूँ", "मैं खाता रोटी हूँ", "रोटी मैं हूँ खाता", "खाता हूँ मैं रोटी"], explain: "Subject–Object–Verb: मैं रोटी खाता हूँ." },
    { q: "रोटी is which gender?", a: "feminine", opts: ["masculine", "feminine"], explain: "रोटी is feminine." },
    { q: "A woman says 'I go' — pick the right verb", a: "जाती", opts: ["जाता", "जाती", "जाते", "गया"], explain: "Female speaker: मैं जाती हूँ." },
    { q: "Which is the future: 'I will eat'?", a: "मैं खाऊँगा", opts: ["मैं खाता हूँ", "मैंने खाया", "मैं खाऊँगा", "मैं खा रहा हूँ"], explain: "मैं खाऊँगा is the future." },
    { q: "Which is the polite 'you'?", a: "आप", opts: ["आप", "तुम", "तू", "वह"], explain: "आप is the polite form, safe in almost every situation." },
    { q: "What does कहाँ mean?", a: "where", opts: ["what", "where", "when", "why"], explain: "कहाँ is where." },
    { q: "Which number is 5 in Hindi?", a: "पाँच", opts: ["पाँच", "चार", "छह", "सात"], explain: "पाँच is five." },
    { q: "I don't understand — which is right?", a: "मैं नहीं समझता", opts: ["मैं नहीं समझता", "मैं समझता नहीं नहीं", "नहीं मैं समझता", "मैं समझ नहीं"], explain: "नहीं goes right before the verb: मैं नहीं समझता." },
    { q: "Can you hold a short conversation with a patient native speaker?", a: "a little", opts: ["comfortably", "a little", "only set phrases", "not at all"], explain: "This is the one question a web page can't measure — be honest with yourself." }
  ],

  /* ---------- Reading: read a short sentence, pick the meaning ---------- */
  reading: [
    { q: "मैं चाय पीता हूँ।", a: "I drink tea.", opts: ["I drink tea.", "I eat bread.", "I like tea.", "I am making tea."], explain: "चाय is tea, पीता हूँ is 'I drink' (male speaker)." },
    { q: "यह मेरा घर है।", a: "This is my house.", opts: ["This is my house.", "This is my car.", "Where is my house?", "That is a big house."], explain: "यह = this, मेरा घर = my house, है = is." },
    { q: "वह बाज़ार जा रही है।", a: "She is going to the market.", opts: ["She is going to the market.", "He is going home.", "They are going to the market.", "She is at the market."], explain: "जा रही है = 'is going' (female subject); बाज़ार = market." },
    { q: "कल मौसम अच्छा था।", a: "Yesterday the weather was nice.", opts: ["Yesterday the weather was nice.", "Tomorrow the weather will be nice.", "Today the weather is bad.", "The weather is always nice."], explain: "कल = yesterday, मौसम = weather, अच्छा था = was nice." },
    { q: "मुझे हिन्दी सीखनी है।", a: "I want to learn Hindi.", opts: ["I want to learn Hindi.", "I already know Hindi.", "I teach Hindi.", "I don't like Hindi."], explain: "मुझे … है = 'I have to / I want to'; सीखनी = to learn." },
    { q: "आपका नाम क्या है?", a: "What is your name?", opts: ["What is your name?", "What is your address?", "How are you?", "Where do you live?"], explain: "आपका नाम = your name (polite), क्या है = what is." },
    { q: "वह कल दिल्ली जाएगा।", a: "He will go to Delhi tomorrow.", opts: ["He will go to Delhi tomorrow.", "He went to Delhi yesterday.", "She is in Delhi now.", "He never goes to Delhi."], explain: "जाएगा = 'will go' (male); कल here = tomorrow." },
    { q: "मुझे पानी चाहिए।", a: "I need water.", opts: ["I need water.", "I have water.", "Water is cold.", "I don't drink water."], explain: "चाहिए = need/want: मुझे पानी चाहिए." }
  ],

  /* ---------- Writing / Devanagari: recognise the letter ---------- */
  devanagari: [
    { q: "Which letter makes the sound 'ka' (as in car)?", a: "क", opts: ["क", "ग", "च", "ट"], explain: "क is ka — the unaspirated k." },
    { q: "Which letter is the vowel 'aa' (as in father)?", a: "आ", opts: ["आ", "अ", "इ", "ए"], explain: "आ is the long aa vowel." },
    { q: "Which letter makes 'na' (dental)?", a: "न", opts: ["न", "ण", "म", "त"], explain: "न is dental na; ण is the retroflex na." },
    { q: "Which letter is 'ma'?", a: "म", opts: ["म", "भ", "य", "स"], explain: "म is ma." },
    { q: "Which letter makes 'ta' with the tongue curled back?", a: "ट", opts: ["ट", "त", "द", "थ"], explain: "ट is the retroflex ta; त is dental ta." },
    { q: "Which letter is 'ha'?", a: "ह", opts: ["ह", "घ", "ख", "भ"], explain: "ह is ha." },
    { q: "Which letter is the vowel 'i' (short)?", a: "इ", opts: ["इ", "ई", "उ", "ऊ"], explain: "इ is short i; ई is long ee." },
    { q: "Which letter makes 'sa' (as in sun)?", a: "स", opts: ["स", "श", "ष", "छ"], explain: "स is sa; श is sha (like ship)." }
  ],

  /* ---------- Speaking: say it aloud, then check (self-graded, no auto-scoring) ---------- */
  speaking: [
    { q: "नमस्ते", a: "namaste — hello / goodbye", explain: "The universal greeting. The 't' is soft — nah-muh-stay, not nah-muh-STEE." },
    { q: "धन्यवाद", a: "dhanyavaad — thank you", explain: "'dh' is an aspirated d — a puff of air after the d." },
    { q: "मेरा नाम ___ है", a: "mera naam ___ hai — my name is ___", explain: "Fill in your own name and say the whole sentence." },
    { q: "आप कैसे हैं?", a: "aap kaise hain? — how are you? (polite)", explain: "The polite form — safe with anyone you don't know well." },
    { q: "मुझे पानी चाहिए", a: "mujhe paani chaahiye — I need water", explain: "'chaahiye' is the single most useful word for asking for things." },
    { q: "यह कितने का है?", a: "yah kitne ka hai? — how much is this?", explain: "The essential market question. Practice until it's instant." },
    { q: "मैं नहीं समझता हूँ", a: "main nahin samajhta hoon — I don't understand", explain: "A woman says 'samajhti'. Say the version that matches you." },
    { q: "क्या आप अंग्रेज़ी बोलते हैं?", a: "kya aap angrezi bolte hain? — do you speak English?", explain: "'kya' turns a statement into a yes/no question." },
    { q: "मुझे मदद चाहिए", a: "mujhe madad chaahiye — I need help", explain: "Same 'chaahiye' pattern — pair it with anything you need." },
    { q: "कल मिलेंगे", a: "kal milenge — see you tomorrow", explain: "'phir milenge' (see you again) works too — the friendly goodbye." }
  ]
};

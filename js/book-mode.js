/* EkGuru — BOOK MODE for lesson pages (17 Nov 2026)
   ---------------------------------------------------------------------
   Owner request: "Hindi lessons should feel like a book — one step at a
   time, next → next, with pictures and animation and far more practice."

   This file turns a long lesson article into a stepped reader WITHOUT
   changing the HTML the generators write: every h2 (and the heavy h3
   word groups) becomes a page, a progress rail and Back / Next buttons
   are added, and PRACTICE STEPS are generated from the lesson's own
   words and sentences (the .vcard and .fd-lines markup), so every lesson
   gains six exercise types for free:

     match      — pair the Hindi word with its meaning
     listen     — hear a word, pick the one you heard
     build      — assemble a word from its shuffled akshar
     picture    — pick the word for the pictogram
     roman      — pick the right romanisation
     order      — put a sentence's words back in order

   Visuals: an "ink reveal" animation on the lesson's key letter, the
   sign-joins-letter animation on .fd-sign, pictograms on word cards from
   a Hindi word → emoji dictionary, and a small confetti on a perfect
   round (via EkGuruUI.celebrate when present). Everything respects
   prefers-reduced-motion.

   Activation: a page with <div class="art" data-book-mode> or the
   foundation marker #fd-mark. "Whole lesson" toggle shows the plain
   article again; the DOM order is never altered, so printing, find-in-
   page after toggling, screen readers and crawlers get the same text.
   Progress per page is kept in localStorage (ekguru.book.*) only.
   --------------------------------------------------------------------- */
(function (root, doc) {
  "use strict";
  if (!doc || !doc.querySelector) return;

  var REDUCED = false;
  try { REDUCED = !!(root.matchMedia && root.matchMedia("(prefers-reduced-motion: reduce)").matches); } catch (e) {}

  /* ------------------------------------------------------------ helpers */
  function $(sel, el) { return (el || doc).querySelector(sel); }
  function $$(sel, el) { return Array.prototype.slice.call((el || doc).querySelectorAll(sel)); }
  function h(tag, attrs, children) {
    var el = doc.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === "class") el.className = attrs[k];
      else if (k === "text") el.textContent = attrs[k];
      else if (k === "html") el.innerHTML = attrs[k];
      else if (k.indexOf("on") === 0 && typeof attrs[k] === "function") el.addEventListener(k.slice(2), attrs[k]);
      else if (attrs[k] !== null && attrs[k] !== undefined) el.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c) el.appendChild(typeof c === "string" ? doc.createTextNode(c) : c); });
    return el;
  }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function sample(a, n, not) {
    var pool = a.filter(function (x) { return !not || not.indexOf(x) === -1; });
    return shuffle(pool).slice(0, n);
  }
  function store(k, v) {
    try { if (v === undefined) return JSON.parse(root.localStorage.getItem(k) || "null"); root.localStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; }
  }
  function clean(s) { return String(s || "").replace(/\s+/g, " ").replace(/[।॥.!?,]/g, "").trim(); }
  var LANG = (doc.documentElement.getAttribute("data-learning-language") || "hi").toLowerCase();
  function speak(text, onend) {
    if (root.EkGuruVoice && root.EkGuruVoice.speak) return root.EkGuruVoice.speak(String(text), LANG, undefined, onend);
    return false;
  }
  function celebrate(msg) {
    try {
      if (root.EkGuruUI && typeof root.EkGuruUI.celebrate === "function") return root.EkGuruUI.celebrate(msg);
      if (root.EkGuruUI && typeof root.EkGuruUI.toast === "function") return root.EkGuruUI.toast(msg);
    } catch (e) {}
  }

  /* Devanagari akshar (grapheme-cluster) splitter. Intl.Segmenter where
     the browser has it; otherwise a hand-rolled rule: a cluster is a base
     sign plus every combining mark after it, and a virama glues the next
     consonant on (so क्ष stays one akshar — the same unit a child writes). */
  function akshar(word) {
    word = String(word || "");
    try {
      if (root.Intl && root.Intl.Segmenter) {
        var seg = new root.Intl.Segmenter("hi", { granularity: "grapheme" });
        return Array.prototype.map.call(Array.from(seg.segment(word)), function (s) { return s.segment; }).filter(function (s) { return s.trim(); });
      }
    } catch (e) {}
    var out = [], cur = "", glue = false;
    for (var i = 0; i < word.length; i++) {
      var ch = word[i], code = ch.charCodeAt(0);
      var combining = (code >= 0x093A && code <= 0x094F) || (code >= 0x0951 && code <= 0x0957) || code === 0x093C || (code >= 0x0962 && code <= 0x0963) || (code >= 0x0900 && code <= 0x0903) || code === 0x200D || code === 0x200C;
      if (ch === " ") { if (cur) out.push(cur); cur = ""; glue = false; continue; }
      if (!cur || combining || glue) { cur += ch; }
      else { out.push(cur); cur = ch; }
      glue = (code === 0x094D);
    }
    if (cur) out.push(cur);
    return out;
  }

  /* ------------------------------------------------ pictogram dictionary
     Hindi word → emoji, for the word cards and the picture exercise. Only
     words whose meaning a picture can carry without ambiguity. */
  var PIC = {
    "आम": "🥭", "अनार": "🍎", "केला": "🍌", "सेब": "🍎", "अंगूर": "🍇", "नींबू": "🍋", "गाजर": "🥕", "आलू": "🥔", "टमाटर": "🍅", "प्याज": "🧅", "मटर": "🫛", "भुट्टा": "🌽", "मिर्च": "🌶️", "नारियल": "🥥", "तरबूज": "🍉", "पपीता": "🍈", "संतरा": "🍊", "अमरूद": "🍐",
    "घर": "🏠", "महल": "🏰", "बाजार": "🏪", "मकान": "🏠", "दुकान": "🏬", "स्कूल": "🏫", "मंदिर": "🛕", "गाँव": "🏡", "शहर": "🏙️", "सड़क": "🛣️", "पुल": "🌉", "कमरा": "🚪", "दरवाजा": "🚪", "खिड़की": "🪟", "छत": "🏠",
    "नाव": "⛵", "जहाज": "🚢", "रथ": "🛞", "बस": "🚌", "रेल": "🚆", "गाड़ी": "🚗", "साइकिल": "🚲", "हवाई जहाज": "✈️",
    "चाय": "🍵", "दूध": "🥛", "जल": "💧", "पानी": "💧", "दाल": "🍲", "चावल": "🍚", "रोटी": "🫓", "नमक": "🧂", "घी": "🧈", "दही": "🥣", "मक्खन": "🧈", "खाना": "🍽️", "फल": "🍎", "लड्डू": "🟠", "मिठाई": "🍬", "अंडा": "🥚", "शहद": "🍯", "चीनी": "🍬",
    "बादल": "☁️", "आसमान": "🌌", "सूरज": "☀️", "सूर्य": "☀️", "चाँद": "🌙", "चंद्र": "🌙", "तारा": "⭐", "बारिश": "🌧️", "हवा": "💨", "आग": "🔥", "नदी": "🏞️", "पहाड़": "⛰️", "समुद्र": "🌊", "पेड़": "🌳", "फूल": "🌸", "पत्ता": "🍃", "कमल": "🪷", "गुलाब": "🌹", "धूप": "☀️", "बर्फ": "❄️", "जंगल": "🌲", "झील": "🏞️", "खेत": "🌾", "बाग": "🌳",
    "राजा": "🤴", "रानी": "👸", "माता": "👩", "माँ": "👩", "पिता": "👨", "दादा": "👴", "दादी": "👵", "नाना": "👴", "नानी": "👵", "काका": "👨", "चाचा": "👨", "मामा": "👨", "बहन": "👧", "भाई": "👦", "बेटा": "👦", "बेटी": "👧", "बच्चा": "👶", "लड़का": "👦", "लड़की": "👧", "आदमी": "👨", "औरत": "👩", "दोस्त": "🧑‍🤝‍🧑", "डॉक्टर": "🧑‍⚕️", "किसान": "🧑‍🌾", "शिक्षक": "🧑‍🏫", "गुरु": "🧑‍🏫",
    "माला": "📿", "बाजा": "🥁", "ढोल": "🥁", "छाता": "☂️", "कलम": "🖊️", "किताब": "📖", "पुस्तक": "📖", "कागज": "📄", "थैला": "👜", "थाली": "🍽️", "कप": "☕", "गिलास": "🥛", "घड़ी": "⌚", "चश्मा": "👓", "टोपी": "🧢", "जूता": "👞", "कपड़ा": "👕", "कुर्सी": "🪑", "मेज": "🪑", "पलंग": "🛏️", "दीया": "🪔", "पतंग": "🪁", "गेंद": "⚽", "खिलौना": "🧸", "ताला": "🔒", "चाबी": "🔑", "घंटी": "🔔", "झंडा": "🚩", "तलवार": "🗡️", "धनुष": "🏹", "नल": "🚰", "बाल": "💇", "आँख": "👁️", "नाक": "👃", "कान": "👂", "हाथ": "✋", "पैर": "🦶", "दाँत": "🦷", "मुँह": "👄", "दिल": "❤️", "सिर": "🧑",
    "गाय": "🐄", "बकरी": "🐐", "कुत्ता": "🐕", "बिल्ली": "🐈", "हाथी": "🐘", "घोड़ा": "🐎", "शेर": "🦁", "बाघ": "🐅", "भालू": "🐻", "बंदर": "🐒", "हिरन": "🦌", "ऊँट": "🐪", "खरगोश": "🐇", "चूहा": "🐭", "मछली": "🐟", "कछुआ": "🐢", "साँप": "🐍", "मेंढक": "🐸", "मोर": "🦚", "कौआ": "🐦‍⬛", "कबूतर": "🕊️", "तोता": "🦜", "उल्लू": "🦉", "बतख": "🦆", "मुर्गा": "🐓", "चिड़िया": "🐦", "तितली": "🦋", "मधुमक्खी": "🐝", "चींटी": "🐜", "मकड़ी": "🕷️", "गधा": "🫏", "भैंस": "🐃", "सूअर": "🐖", "भेड़": "🐑", "गिलहरी": "🐿️",
    "एक": "1️⃣", "दो": "2️⃣", "तीन": "3️⃣", "चार": "4️⃣", "पाँच": "5️⃣", "छह": "6️⃣", "सात": "7️⃣", "आठ": "8️⃣", "नौ": "9️⃣", "दस": "🔟",
    "लाल": "🟥", "पीला": "🟨", "हरा": "🟩", "नीला": "🟦", "काला": "⬛", "सफेद": "⬜",
    "सोना": "😴", "खाना": "🍽️", "पीना": "🥤", "पढ़ना": "📖", "लिखना": "✍️", "गाना": "🎵", "नाचना": "💃", "दौड़ना": "🏃", "हँसना": "😄", "रोना": "😢", "बोलना": "🗣️", "सुनना": "👂", "देखना": "👀", "चलना": "🚶", "खेलना": "⚽", "तैरना": "🏊", "उड़ना": "🕊️",
    "सुबह": "🌅", "रात": "🌃", "शाम": "🌇", "दिन": "☀️", "आज": "📅", "कल": "📆", "समय": "⏰", "साल": "🗓️",
    "पैसा": "💰", "रुपया": "💵", "उपहार": "🎁", "दवा": "💊", "फोन": "📱", "दीवार": "🧱", "रस्सी": "🪢", "सुई": "🪡", "काम": "🛠️", "खुशी": "😊", "प्यार": "❤️", "शांति": "🕊️", "संगीत": "🎶", "खेल": "🏏", "नमस्ते": "🙏", "धन्यवाद": "🙏", "हाँ": "👍", "नहीं": "👎", "बड़ा": "🐘", "छोटा": "🐭", "गरम": "🔥", "ठंडा": "🧊", "नया": "✨", "पुराना": "🕰️"
  };

  /* English meaning → emoji, so word tables in any language get pictures. */
  var PIC_EN = {
    "mango": "🥭", "apple": "🍎", "banana": "🍌", "grapes": "🍇", "lemon": "🍋", "carrot": "🥕", "potato": "🥔", "tomato": "🍅", "onion": "🧅", "rice": "🍚", "bread": "🍞", "milk": "🥛", "water": "💧", "tea": "🍵", "coffee": "☕", "egg": "🥚", "salt": "🧂", "sugar": "🍬", "fruit": "🍎", "food": "🍽️", "fish": "🐟", "chicken": "🍗", "sweet": "🍬", "sweets": "🍬",
    "house": "🏠", "home": "🏠", "school": "🏫", "shop": "🏪", "market": "🏪", "temple": "🛕", "village": "🏡", "city": "🏙️", "road": "🛣️", "door": "🚪", "window": "🪟", "room": "🚪", "hospital": "🏥", "station": "🚉", "hotel": "🏨", "office": "🏢", "bank": "🏦",
    "boat": "⛵", "ship": "🚢", "bus": "🚌", "train": "🚆", "car": "🚗", "bicycle": "🚲", "aeroplane": "✈️", "airplane": "✈️", "plane": "✈️", "taxi": "🚕", "auto-rickshaw": "🛺", "rickshaw": "🛺",
    "cloud": "☁️", "sky": "🌌", "sun": "☀️", "moon": "🌙", "star": "⭐", "rain": "🌧️", "wind": "💨", "fire": "🔥", "river": "🏞️", "mountain": "⛰️", "sea": "🌊", "tree": "🌳", "flower": "🌸", "leaf": "🍃", "lotus": "🪷", "rose": "🌹", "snow": "❄️", "forest": "🌲", "lake": "🏞️", "field": "🌾", "garden": "🌳", "earth": "🌍", "stone": "🪨",
    "king": "🤴", "queen": "👸", "mother": "👩", "father": "👨", "grandfather": "👴", "grandmother": "👵", "sister": "👧", "brother": "👦", "son": "👦", "daughter": "👧", "child": "👶", "boy": "👦", "girl": "👧", "man": "👨", "woman": "👩", "friend": "🧑‍🤝‍🧑", "doctor": "🧑‍⚕️", "farmer": "🧑‍🌾", "teacher": "🧑‍🏫", "student": "🧑‍🎓", "family": "👨‍👩‍👧", "people": "👥", "baby": "👶", "uncle": "👨", "aunt": "👩", "husband": "👨", "wife": "👩",
    "garland": "📿", "drum": "🥁", "umbrella": "☂️", "pen": "🖊️", "book": "📖", "paper": "📄", "bag": "👜", "plate": "🍽️", "cup": "☕", "glass": "🥛", "clock": "⌚", "watch": "⌚", "glasses": "👓", "hat": "🧢", "cap": "🧢", "shoe": "👞", "shoes": "👞", "clothes": "👕", "shirt": "👕", "chair": "🪑", "table": "🪑", "bed": "🛏️", "lamp": "🪔", "kite": "🪁", "ball": "⚽", "toy": "🧸", "lock": "🔒", "key": "🔑", "bell": "🔔", "flag": "🚩", "sword": "🗡️", "bow": "🏹", "tap": "🚰", "phone": "📱", "money": "💰", "gift": "🎁", "medicine": "💊", "wall": "🧱", "rope": "🪢", "needle": "🪡", "knife": "🔪", "spoon": "🥄", "bottle": "🍶", "box": "📦", "letter": "✉️", "picture": "🖼️", "map": "🗺️", "ticket": "🎫", "computer": "💻", "television": "📺", "tv": "📺", "newspaper": "📰", "soap": "🧼", "mirror": "🪞", "comb": "🪮",
    "hair": "💇", "eye": "👁️", "eyes": "👀", "nose": "👃", "ear": "👂", "hand": "✋", "foot": "🦶", "leg": "🦵", "tooth": "🦷", "teeth": "🦷", "mouth": "👄", "heart": "❤️", "head": "🧑", "face": "🙂", "stomach": "🫃",
    "cow": "🐄", "goat": "🐐", "dog": "🐕", "cat": "🐈", "elephant": "🐘", "horse": "🐎", "lion": "🦁", "tiger": "🐅", "bear": "🐻", "monkey": "🐒", "deer": "🦌", "camel": "🐪", "rabbit": "🐇", "mouse": "🐭", "rat": "🐀", "tortoise": "🐢", "turtle": "🐢", "snake": "🐍", "frog": "🐸", "peacock": "🦚", "crow": "🐦‍⬛", "pigeon": "🕊️", "parrot": "🦜", "owl": "🦉", "duck": "🦆", "rooster": "🐓", "hen": "🐔", "bird": "🐦", "butterfly": "🦋", "bee": "🐝", "ant": "🐜", "spider": "🕷️", "donkey": "🫏", "buffalo": "🐃", "pig": "🐖", "sheep": "🐑", "squirrel": "🐿️",
    "one": "1️⃣", "two": "2️⃣", "three": "3️⃣", "four": "4️⃣", "five": "5️⃣", "six": "6️⃣", "seven": "7️⃣", "eight": "8️⃣", "nine": "9️⃣", "ten": "🔟", "hundred": "💯",
    "red": "🟥", "yellow": "🟨", "green": "🟩", "blue": "🟦", "black": "⬛", "white": "⬜", "orange": "🟧", "pink": "🩷", "brown": "🟫", "purple": "🟪",
    "to sleep": "😴", "sleep": "😴", "to eat": "🍽️", "eat": "🍽️", "to drink": "🥤", "drink": "🥤", "to read": "📖", "read": "📖", "to write": "✍️", "write": "✍️", "to sing": "🎵", "sing": "🎵", "to dance": "💃", "dance": "💃", "to run": "🏃", "run": "🏃", "to laugh": "😄", "laugh": "😄", "to cry": "😢", "cry": "😢", "to speak": "🗣️", "speak": "🗣️", "to listen": "👂", "listen": "👂", "to see": "👀", "see": "👀", "to walk": "🚶", "walk": "🚶", "to play": "⚽", "play": "⚽", "to swim": "🏊", "swim": "🏊", "to fly": "🕊️", "to cook": "🍳", "cook": "🍳", "to buy": "🛒", "buy": "🛒", "to go": "🚶", "go": "🚶", "to come": "🚶", "to sit": "🪑", "sit": "🪑", "to think": "🤔", "think": "🤔", "to work": "🛠️", "work": "🛠️", "to study": "📚", "study": "📚", "to wait": "⏳", "wait": "⏳", "to open": "🔓", "open": "🔓", "to close": "🔒", "close": "🔒", "to call": "📞", "call": "📞", "to give": "🎁", "give": "🎁", "to love": "❤️", "love": "❤️", "to ask": "❓", "ask": "❓",
    "morning": "🌅", "night": "🌃", "evening": "🌇", "day": "☀️", "today": "📅", "tomorrow": "📆", "yesterday": "📆", "time": "⏰", "year": "🗓️", "week": "📅", "month": "📆", "hour": "⏰", "minute": "⏱️", "summer": "☀️", "winter": "❄️", "monsoon": "🌧️", "spring": "🌸",
    "happiness": "😊", "happy": "😊", "sad": "😢", "angry": "😠", "tired": "😩", "hungry": "🍽️", "thirsty": "🥤", "sick": "🤒", "ill": "🤒", "hot": "🔥", "cold": "🧊", "new": "✨", "old": "🕰️", "big": "🐘", "small": "🐭", "good": "👍", "bad": "👎", "yes": "👍", "no": "👎", "hello": "🙏", "goodbye": "👋", "thank you": "🙏", "thanks": "🙏", "sorry": "🙇", "please": "🙏", "peace": "🕊️", "music": "🎶", "game": "🏏", "cricket": "🏏", "song": "🎵", "film": "🎬", "movie": "🎬", "festival": "🎉", "wedding": "💍", "birthday": "🎂", "question": "❓", "answer": "✅", "name": "🪪", "left": "⬅️", "right": "➡️", "up": "⬆️", "down": "⬇️", "straight": "⬆️", "near": "📍", "far": "🗺️", "fast": "🏎️", "slow": "🐢", "rupee": "💵", "rupees": "💵", "price": "🏷️", "cheap": "🏷️", "expensive": "💎"
  };
  function picFor(hi, en) {
    if (PIC[hi]) return PIC[hi];
    var k = String(en || "").toLowerCase().replace(/\(.*?\)/g, "").split(/[,;\/—–-]/)[0].replace(/^(a|an|the)\s+/, "").trim();
    return PIC_EN[k] || "";
  }

  /* ------------------------------------------------------------ harvest
     Pull the lesson's own words and sentences out of the markup. */
  function harvestWords(art) {
    var seen = {}, out = [];
    $$(".vcard", art).forEach(function (c) {
      var hi = clean(($(".lt", c) || {}).textContent);
      var rm = String((($(".sd", c) || {}).textContent) || "").replace(/·.*$/, "").trim();
      var en = String((($(".en", c) || {}).textContent) || "").trim();
      if (!hi || !en || seen[hi]) return;
      seen[hi] = 1; out.push({ hi: hi, rm: rm, en: en, pic: picFor(hi, en) });
    });
    /* level pages: Word | Say it | Meaning tables (vocabulary rows only) */
    $$('tr', art).forEach(function (tr) {
      var w = $('td[data-h="Word"]', tr); if (!w) return;
      var btn = $("button[data-voice-kind]", w);
      if (btn && btn.getAttribute("data-voice-kind") !== "vocabulary") return;
      var hi = clean((($("b", w) || w).textContent)), rm = String((($('td[data-h="Say it"]', tr) || {}).textContent) || "").trim();
      var en = String((($('td[data-h="Meaning"]', tr) || {}).textContent) || "").trim();
      if (!hi || !en || seen[hi] || hi.split(" ").length > 3) return;
      seen[hi] = 1; out.push({ hi: hi, rm: rm, en: en, pic: picFor(hi, en) });
    });
    $$(".fd-letter", art).forEach(function (c) {
      var hi = clean(($(".lt", c) || {}).textContent);
      var rm = String((($(".rm", c) || {}).textContent) || "").trim();
      var kw = $(".kw i", c), en = $(".en", c);
      if (!hi || seen[hi]) return;
      seen[hi] = 1;
      out.push({ hi: hi, rm: rm, en: (kw ? clean(kw.textContent) + " — " : "") + (en ? en.textContent.trim() : rm), letter: true, pic: kw ? (PIC[clean(kw.textContent)] || "") : "" });
    });
    return out;
  }
  function harvestLines(art) {
    var out = [], seen = {};
    $$(".fd-lines li", art).forEach(function (li) {
      var dv = $(".dv", li), rm = $(".rm", li), det = $("details", li);
      if (!dv) return;
      var hiRaw = String(dv.textContent || "").replace(/🔊/g, "").replace(/\s+/g, " ").trim();
      var en = det ? String(det.textContent || "").replace(/^\s*(English|Answer)\s*/i, "").trim() : "";
      var words = clean(hiRaw).split(" ").filter(Boolean);
      if (words.length < 2 || words.length > 9 || seen[hiRaw]) return;
      seen[hiRaw] = 1;
      out.push({ hi: hiRaw, words: words, rm: rm ? rm.textContent.trim() : "", en: en });
    });
    /* level pages: example rows */
    $$('tr', art).forEach(function (tr) {
      var w = $('td[data-h="Word"] button[data-voice-kind="example"]', tr); if (!w) return;
      var hiRaw = String(w.getAttribute("data-voice-text") || "").replace(/\s+/g, " ").trim();
      var words = clean(hiRaw).split(" ").filter(Boolean);
      var en = String((($('td[data-h="Meaning"]', tr) || {}).textContent) || "").trim();
      var rm = String((($('td[data-h="Say it"]', tr) || {}).textContent) || "").trim();
      if (words.length < 2 || words.length > 9 || seen[hiRaw]) return;
      seen[hiRaw] = 1; out.push({ hi: hiRaw, words: words, rm: rm, en: en });
    });
    return out;
  }

  /* ------------------------------------------------------------ practice
     Each builder returns an element with its own state; `report(score,
     total)` is called when the round is finished. */
  function practiceShell(title, hint) {
    var sec = h("section", { class: "bk-ex", "aria-label": title });
    sec.appendChild(h("h2", { class: "bk-ex-title", text: title }));
    if (hint) sec.appendChild(h("p", { class: "bk-ex-hint", text: hint }));
    sec.body = h("div", { class: "bk-ex-body" });
    sec.appendChild(sec.body);
    sec.foot = h("div", { class: "bk-ex-foot", "aria-live": "polite" });
    sec.appendChild(sec.foot);
    return sec;
  }
  function finishRound(sec, right, total, again) {
    var perfect = right === total;
    sec.foot.innerHTML = "";
    sec.foot.appendChild(h("p", { class: "bk-score " + (perfect ? "ok" : ""), text: (perfect ? "Perfect — " : "") + right + " / " + total + (perfect ? " 🎉" : "") }));
    var row = h("div", { class: "bk-row" });
    row.appendChild(h("button", { class: "btn btn-ghost", type: "button", text: "Try again", onclick: function () { sec.body.innerHTML = ""; sec.foot.innerHTML = ""; again(); } }));
    sec.foot.appendChild(row);
    if (perfect) celebrate("Perfect round!");
    sec.dispatchEvent(new CustomEvent("bk:done", { bubbles: true, detail: { right: right, total: total, kind: sec.getAttribute("data-kind") } }));
  }

  /* MATCH — tap a Hindi word, then its meaning. */
  function exMatch(words) {
    var sec = practiceShell("Practice · Match the pairs", "Tap a Hindi word, then tap its meaning. Pictures help; sound helps more.");
    sec.setAttribute("data-kind", "match");
    function round() {
      var set = sample(words, Math.min(5, words.length));
      var left = h("div", { class: "bk-col" }), rightCol = h("div", { class: "bk-col" });
      var pick = null, done = 0, wrong = 0;
      set.forEach(function (w) {
        left.appendChild(h("button", { class: "bk-chip hi", type: "button", lang: "hi", "data-k": w.hi, html: (w.pic ? '<span class="bk-pic" aria-hidden="true">' + w.pic + "</span>" : "") + w.hi,
          onclick: function () { if (this.classList.contains("hit")) return; speak(w.hi); $$(".bk-chip.hi.sel", left).forEach(function (b) { b.classList.remove("sel"); }); this.classList.add("sel"); pick = w.hi; } }));
      });
      shuffle(set).forEach(function (w) {
        rightCol.appendChild(h("button", { class: "bk-chip en", type: "button", "data-k": w.hi, text: w.en,
          onclick: function () {
            if (!pick || this.classList.contains("hit")) return;
            var l = $('.bk-chip.hi[data-k="' + pick.replace(/"/g, "") + '"]', left);
            if (this.getAttribute("data-k") === pick) {
              this.classList.add("hit"); if (l) { l.classList.add("hit"); l.classList.remove("sel"); }
              pick = null; done++;
              if (done === set.length) finishRound(sec, set.length - wrong, set.length, round);
            } else {
              wrong++; var me = this; me.classList.add("miss"); if (l) l.classList.add("miss");
              setTimeout(function () { me.classList.remove("miss"); if (l) l.classList.remove("miss"); }, 500);
            }
          } }));
      });
      var grid = h("div", { class: "bk-match" }, [left, rightCol]);
      sec.body.appendChild(grid);
    }
    round();
    return sec;
  }

  /* LISTEN — hear one, pick it from four. */
  function exListen(words, pool) {
    pool = pool && pool.length > words.length ? pool : words;
    var sec = practiceShell("Practice · Listen and pick", "Press play, then tap the word you heard. Replay as often as you like.");
    sec.setAttribute("data-kind", "listen");
    function round() {
      var qs = sample(words, Math.min(5, words.length)), i = 0, right = 0;
      function ask() {
        sec.body.innerHTML = "";
        if (i >= qs.length) return finishRound(sec, right, qs.length, round);
        var target = qs[i], opts = shuffle([target].concat(sample(pool, 3, [target])));
        var play = h("button", { class: "bk-play", type: "button", "aria-label": "Play the word", text: "🔊 Play", onclick: function () { speak(target.hi); } });
        sec.body.appendChild(h("div", { class: "bk-q" }, [h("span", { class: "bk-count", text: (i + 1) + " / " + qs.length }), play]));
        var grid = h("div", { class: "bk-grid" });
        var answered = false;
        opts.forEach(function (o) {
          grid.appendChild(h("button", { class: "bk-opt", type: "button", lang: "hi", text: o.hi, onclick: function () {
            if (answered) return; answered = true;
            var ok = o.hi === target.hi; if (ok) right++;
            this.classList.add(ok ? "hit" : "miss");
            if (!ok) $$(".bk-opt", grid).forEach(function (b) { if (b.textContent === target.hi) b.classList.add("hit"); });
            sec.foot.textContent = ok ? "✓ " + target.hi + " — " + target.en : "✗ It was " + target.hi + " (" + target.rm + ") — " + target.en;
            i++; setTimeout(function () { sec.foot.textContent = ""; ask(); }, ok ? 700 : 1600);
          } }));
        });
        sec.body.appendChild(grid);
        if (!REDUCED) setTimeout(function () { speak(target.hi); }, 250);
      }
      ask();
    }
    round();
    return sec;
  }

  /* BUILD — the word's akshar, shuffled; tap them back into order. */
  function exBuild(words) {
    var pool = words.filter(function (w) { return !w.letter && akshar(w.hi).length >= 2 && akshar(w.hi).length <= 6; });
    if (pool.length < 2) return null;
    var sec = practiceShell("Practice · Build the word", "The letters are mixed up. Tap them in the right order to spell the word for the meaning shown.");
    sec.setAttribute("data-kind", "build");
    function round() {
      var qs = sample(pool, Math.min(5, pool.length)), i = 0, right = 0;
      function ask() {
        sec.body.innerHTML = "";
        if (i >= qs.length) return finishRound(sec, right, qs.length, round);
        var w = qs[i], parts = akshar(w.hi), mixed = shuffle(parts), built = [], wrongHere = false;
        if (mixed.join("") === parts.join("") && parts.length > 1) mixed = parts.slice(1).concat(parts[0]);
        var prompt = h("div", { class: "bk-q" }, [h("span", { class: "bk-count", text: (i + 1) + " / " + qs.length }), h("b", { class: "bk-meaning", html: (w.pic ? '<span class="bk-pic" aria-hidden="true">' + w.pic + "</span> " : "") + w.en }), h("small", { text: w.rm })]);
        var slot = h("div", { class: "bk-slot", lang: "hi", "aria-live": "polite" });
        var tray = h("div", { class: "bk-tray" });
        mixed.forEach(function (p) {
          tray.appendChild(h("button", { class: "bk-akshar", type: "button", lang: "hi", text: p, onclick: function () {
            if (this.disabled) return;
            var expect = parts[built.length];
            if (p === expect) {
              built.push(p); this.disabled = true; this.classList.add("used");
              slot.appendChild(h("span", { class: "bk-akshar in", text: p }));
              if (built.length === parts.length) {
                if (!wrongHere) right++;
                slot.classList.add("ok"); speak(w.hi); i++;
                setTimeout(ask, 900);
              }
            } else { wrongHere = true; var me = this; me.classList.add("miss"); setTimeout(function () { me.classList.remove("miss"); }, 400); }
          } }));
        });
        sec.body.appendChild(prompt); sec.body.appendChild(slot); sec.body.appendChild(tray);
      }
      ask();
    }
    round();
    return sec;
  }

  /* PICTURE — the pictogram, four Hindi words. */
  function exPicture(words, all) {
    var pool = words.filter(function (w) { return w.pic; });
    if (pool.length < 3) return null;
    all = all && all.length > words.length ? all : words;
    var sec = practiceShell("Practice · Picture to word", "Which Hindi word is the picture? Tap it, then hear it.");
    sec.setAttribute("data-kind", "picture");
    function round() {
      var qs = sample(pool, Math.min(5, pool.length)), i = 0, right = 0;
      function ask() {
        sec.body.innerHTML = "";
        if (i >= qs.length) return finishRound(sec, right, qs.length, round);
        var t = qs[i], opts = shuffle([t].concat(sample(all, 3, [t])));
        sec.body.appendChild(h("div", { class: "bk-q" }, [h("span", { class: "bk-count", text: (i + 1) + " / " + qs.length }), h("span", { class: "bk-bigpic", role: "img", "aria-label": t.en, text: t.pic })]));
        var grid = h("div", { class: "bk-grid" }), answered = false;
        opts.forEach(function (o) {
          grid.appendChild(h("button", { class: "bk-opt", type: "button", lang: "hi", text: o.hi, onclick: function () {
            if (answered) return; answered = true;
            var ok = o.hi === t.hi; if (ok) right++;
            this.classList.add(ok ? "hit" : "miss"); speak(t.hi);
            if (!ok) $$(".bk-opt", grid).forEach(function (b) { if (b.textContent === t.hi) b.classList.add("hit"); });
            i++; setTimeout(ask, ok ? 800 : 1500);
          } }));
        });
        sec.body.appendChild(grid);
      }
      ask();
    }
    round();
    return sec;
  }

  /* ROMAN — the Hindi word, four romanisations. */
  function exRoman(words, all) {
    var pool = words.filter(function (w) { return w.rm; });
    if (pool.length < 4) return null;
    var dis = (all || []).filter(function (w) { return w.rm; }); if (dis.length < pool.length) dis = pool;
    var sec = practiceShell("Practice · Read it", "Read the Hindi, then pick how it sounds.");
    sec.setAttribute("data-kind", "roman");
    function round() {
      var qs = sample(pool, Math.min(6, pool.length)), i = 0, right = 0;
      function ask() {
        sec.body.innerHTML = "";
        if (i >= qs.length) return finishRound(sec, right, qs.length, round);
        var t = qs[i], opts = shuffle([t].concat(sample(dis, 3, [t])));
        sec.body.appendChild(h("div", { class: "bk-q" }, [h("span", { class: "bk-count", text: (i + 1) + " / " + qs.length }), h("b", { class: "bk-bigword", lang: "hi", text: t.hi })]));
        var grid = h("div", { class: "bk-grid" }), answered = false;
        opts.forEach(function (o) {
          grid.appendChild(h("button", { class: "bk-opt rm", type: "button", text: o.rm, onclick: function () {
            if (answered) return; answered = true;
            var ok = o.rm === t.rm; if (ok) right++;
            this.classList.add(ok ? "hit" : "miss"); speak(t.hi);
            if (!ok) $$(".bk-opt", grid).forEach(function (b) { if (b.textContent === t.rm) b.classList.add("hit"); });
            i++; setTimeout(ask, ok ? 700 : 1500);
          } }));
        });
        sec.body.appendChild(grid);
      }
      ask();
    }
    round();
    return sec;
  }

  /* ORDER — a sentence's words, shuffled. */
  function exOrder(lines) {
    if (lines.length < 2) return null;
    var sec = practiceShell("Practice · Order the sentence", "Tap the words in the order you would say them. The English is your clue.");
    sec.setAttribute("data-kind", "order");
    function round() {
      var qs = sample(lines, Math.min(4, lines.length)), i = 0, right = 0;
      function ask() {
        sec.body.innerHTML = "";
        if (i >= qs.length) return finishRound(sec, right, qs.length, round);
        var L = qs[i], mixed = shuffle(L.words), built = [], wrongHere = false;
        if (mixed.join(" ") === L.words.join(" ")) mixed = L.words.slice(1).concat(L.words[0]);
        sec.body.appendChild(h("div", { class: "bk-q" }, [h("span", { class: "bk-count", text: (i + 1) + " / " + qs.length }), h("b", { class: "bk-meaning", text: L.en || L.rm })]));
        var slot = h("div", { class: "bk-slot sentence", lang: "hi", "aria-live": "polite" }), tray = h("div", { class: "bk-tray" });
        mixed.forEach(function (wd, idx) {
          tray.appendChild(h("button", { class: "bk-akshar word", type: "button", lang: "hi", text: wd, "data-i": idx, onclick: function () {
            if (this.disabled) return;
            if (wd === L.words[built.length]) {
              built.push(wd); this.disabled = true; this.classList.add("used");
              slot.appendChild(h("span", { class: "bk-akshar in", text: wd }));
              if (built.length === L.words.length) { if (!wrongHere) right++; slot.classList.add("ok"); speak(L.hi); i++; setTimeout(ask, 1200); }
            } else { wrongHere = true; var me = this; me.classList.add("miss"); setTimeout(function () { me.classList.remove("miss"); }, 400); }
          } }));
        });
        sec.body.appendChild(slot); sec.body.appendChild(tray);
      }
      ask();
    }
    round();
    return sec;
  }

  /* ------------------------------------------------------------ visuals */
  function inkReveal(text) {
    var w = h("div", { class: "bk-ink" + (REDUCED ? " still" : ""), "aria-hidden": "true" });
    w.appendChild(h("span", { lang: "hi", text: text }));
    return w;
  }
  function decorateSign(art) {
    $$(".fd-sign", art).forEach(function (s) { s.classList.add("bk-sign"); });
  }
  function decorateCards(art) {
    $$(".vcard", art).forEach(function (c) {
      var hi = clean(($(".lt", c) || {}).textContent), pic = PIC[hi];
      var face = $(".vface", c);
      if (pic && face && !$(".bk-pic", face)) face.insertBefore(h("span", { class: "bk-pic card", "aria-hidden": "true", text: pic }), face.firstChild);
    });
  }

  /* ------------------------------------------------------------ slicing
     Foundation pages split at h2 (and heavy h3 word groups); the level pages
     (languages/xx/level/a1/) split at h2 / h3 unit / h4 lesson and give the
     question lists, quizzes, drills and the level test pages of their own. */
  function slice(art, level) {
    var kids = Array.prototype.slice.call(art.children);
    var steps = [], cur = { title: "Start", kind: "intro", nodes: [] };
    var heavy = 0, inTail = false, lesson = "";
    function push() { if (cur.nodes.length) steps.push(cur); }
    function titleOf(el) { return clean(el.textContent).replace(/🔊/g, "").slice(0, 60); }
    kids.forEach(function (el) {
      var tag = el.tagName;
      if (tag === "SCRIPT" || tag === "STYLE") return;
      var isH2 = tag === "H2", isH3 = tag === "H3", isH4 = tag === "H4";
      var isTail = level ? (isH2 && /keep going|device-only/i.test(el.textContent))
                         : (el.classList.contains("note") || el.classList.contains("cta") || el.classList.contains("chips") ||
                            (isH2 && /also useful|next steps?/i.test(el.textContent)) ||
                            (el.classList.contains("row") && $("a[href*='../']", el) && !$("button", el)));
      if (inTail) { cur.nodes.push(el); return; }
      if (isTail) { push(); cur = { title: "Finish", kind: "finish", nodes: [el] }; inTail = true; return; }
      if (el.classList.contains("quiz") && !level) {
        push(); cur = { title: "Quick check", kind: "quiz", nodes: [el] }; push(); cur = { title: "Finish", kind: "finish", nodes: [] }; return;
      }
      if (el.classList.contains("fd-passage")) {
        var ph = $("h3, h4, b, strong", el);
        push(); cur = { title: "Read · " + (ph ? clean(ph.textContent).replace(/🔊/g, "").slice(0, 40) : "कहानी"), kind: "section", nodes: [el] }; heavy = 1; return;
      }
      if (level) {
        var own = el.classList.contains("prac") ? "Questions" : el.classList.contains("quiz") ? "Quiz" : el.classList.contains("test") ? "Level test" :
                  el.classList.contains("lv-drills") ? "Recall drills" : el.classList.contains("lv-read") ? "Reading" : el.classList.contains("lv-listen") ? "Listening" : "";
        if (own) {
          /* the short intro paragraph just before a list belongs with it */
          var intro = null;
          if (cur.nodes.length > 1 && cur.nodes[cur.nodes.length - 1].tagName === "P") intro = cur.nodes.pop();
          push(); cur = { title: own + (lesson && own !== "Level test" ? " · " + lesson : ""), kind: own === "Level test" ? "quiz" : own === "Quiz" ? "quiz" : "section", nodes: intro ? [intro, el] : [el] };
          if (own === "Quiz" || own === "Level test" || own === "Recall drills") { push(); cur = { title: lesson || own, kind: "section", nodes: [] }; }
          return;
        }
        if (isH2 || isH3 || isH4) {
          push(); cur = { title: titleOf(el), kind: isH2 ? "section" : isH3 ? "unit" : "sub", nodes: [el] };
          if (isH4) lesson = titleOf(el).slice(0, 36); else if (isH2) lesson = "";
          return;
        }
        cur.nodes.push(el); return;
      }
      if (isH2 || (isH3 && heavy >= 1)) {
        push(); cur = { title: titleOf(el), kind: isH2 ? "section" : "sub", nodes: [] }; heavy = 0;
      }
      if (el.classList.contains("vcards") || el.classList.contains("fd-lines") || el.classList.contains("trace-grid") || el.classList.contains("fd-letters")) heavy++;
      cur.nodes.push(el);
    });
    push();
    /* a unit heading alone is a thin page: fold it into the lesson after it */
    for (var i = steps.length - 2; i >= 0; i--) {
      if (steps[i].kind === "unit" && steps[i].nodes.length === 1 && steps[i + 1].kind === "sub") {
        steps[i + 1].nodes = steps[i].nodes.concat(steps[i + 1].nodes); steps[i + 1].title = steps[i].title + " · " + steps[i + 1].title; steps.splice(i, 1);
      }
    }
    return steps;
  }

  /* --------------------------------------------------------------- mount */
  function mount(art, level) {
    if (art.getAttribute("data-bk-mounted")) return;
    art.setAttribute("data-bk-mounted", "1");

    var words = harvestWords(art), lines = harvestLines(art);
    decorateCards(art); decorateSign(art);

    var steps = slice(art, level);
    if (steps.length < 3) return;   /* a short page reads better as a page */

    /* wrap the step nodes in place (DOM order unchanged) */
    steps.forEach(function (s, i) {
      var wrap = h("section", { class: "bk-step", "data-step": i, "aria-label": s.title });
      art.insertBefore(wrap, s.nodes[0]);
      s.nodes.forEach(function (n) { wrap.appendChild(n); });
      s.el = wrap;
    });

    /* generated practice steps go after the step that holds the data */
    function addAfter(afterIdx, title, el) {
      if (!el) return;
      var wrap = h("section", { class: "bk-step bk-step-practice", "aria-label": title });
      wrap.appendChild(el);
      var ref = steps[afterIdx].el;
      ref.parentNode.insertBefore(wrap, ref.nextSibling);
      steps.splice(afterIdx + 1, 0, { title: title, kind: "practice", el: wrap, nodes: [el] });
    }
    var firstSection = -1;
    steps.forEach(function (s, i) { if (firstSection < 0 && s.kind === "section") firstSection = i; });

    if (level) {
      /* one worksheet page after every lesson that teaches words */
      for (var i = steps.length - 1; i >= 0; i--) {
        var sw = harvestWords(steps[i].el), sl = harvestLines(steps[i].el);
        if (sw.length < 4) continue;
        var sheet = h("div", { class: "bk-sheet" });
        [exMatch(sw), exListen(sw, words), exBuild(sw), exPicture(sw, words), exRoman(sw, words), exOrder(sl)].forEach(function (x) { if (x) sheet.appendChild(x); });
        if (!sheet.children.length) continue;
        var t = steps[i].title.replace(/^.*?·\s*/, "");
        sheet.insertBefore(h("p", { class: "bk-sheet-lede", text: "Worksheet · " + sw.length + " words from “" + t + "”. Finish each block; a perfect block turns its dot green." }), sheet.firstChild);
        addAfter(i, "Practice · " + t.slice(0, 40), sheet);
      }
    } else {
      var lastWords = -1, lastLines = -1;
      steps.forEach(function (s, i) {
        if ($(".vcards, .fd-letters", s.el)) lastWords = i;
        if ($(".fd-lines", s.el)) lastLines = i;
      });
      /* order matters: insert from the back so indices stay valid */
      if (lastLines >= 0 && lines.length >= 2) addAfter(lastLines, "Practice · Order the sentence", exOrder(lines));
      if (lastWords >= 0 && words.length >= 4) {
        [["Practice · Read it", exRoman(words)], ["Practice · Picture to word", exPicture(words)], ["Practice · Build the word", exBuild(words)], ["Practice · Listen and pick", exListen(words)], ["Practice · Match the pairs", exMatch(words)]]
          .forEach(function (p) { addAfter(lastWords, p[0], p[1]); });
      }
    }

    /* ink-reveal hero on the first content step: the key letter/form */
    var keyForm = "";
    var signResult = $(".fd-sign div:last-child b", art);
    if (signResult) keyForm = clean(signResult.textContent);
    if (!keyForm) { var firstLetter = $(".fd-letter .lt", art); if (firstLetter) keyForm = clean(firstLetter.textContent); }
    if (keyForm && keyForm.length <= 4 && firstSection >= 0) steps[firstSection].el.insertBefore(inkReveal(keyForm), steps[firstSection].el.firstChild);

    /* chrome: rail + nav */
    var key = "ekguru.book." + root.location.pathname.replace(/\/index\.html$/, "/");
    var saved = store(key) || {};
    var idx = Math.min(Number(saved.step) || 0, steps.length - 1);
    var mode = saved.mode === "all" ? "all" : "book";
    var seen = saved.seen || [];

    var rail = h("div", { class: "bk-rail", role: "group", "aria-label": "Lesson steps" });
    var bar = h("div", { class: "bk-bar" }, [h("i")]);
    var label = h("span", { class: "bk-label", "aria-live": "polite" });
    var dots = h("ol", { class: "bk-dots" });
    steps.forEach(function (s, i) {
      dots.appendChild(h("li", {}, [h("button", { type: "button", class: "bk-dot " + s.kind, "aria-label": "Step " + (i + 1) + ": " + s.title, title: s.title, onclick: function () { go(i); } })]));
    });
    var toggle = h("button", { class: "bk-toggle", type: "button", "aria-pressed": mode === "all" ? "true" : "false", text: mode === "all" ? "Step by step" : "Whole lesson", onclick: function () { setMode(mode === "all" ? "book" : "all"); } });
    rail.appendChild(h("div", { class: "bk-rail-top" }, [label, toggle]));
    rail.appendChild(bar); rail.appendChild(dots);

    var nav = h("div", { class: "bk-nav" });
    var back = h("button", { class: "btn btn-ghost bk-back", type: "button", text: "← Back", onclick: function () { go(idx - 1); } });
    var next = h("button", { class: "btn btn-primary bk-next", type: "button", text: "Next →", onclick: function () { go(idx + 1); } });
    var pos = h("span", { class: "bk-pos" });
    nav.appendChild(back); nav.appendChild(pos); nav.appendChild(next);

    var first = steps[0].el;
    art.insertBefore(rail, first);
    art.appendChild(nav);
    art.classList.add("bk-on");

    function paint() {
      steps.forEach(function (s, i) {
        var show = mode === "all" || i === idx;
        s.el.hidden = !show;
        s.el.classList.toggle("bk-current", i === idx && mode !== "all");
        var d = dots.children[i].firstChild;
        d.classList.toggle("now", i === idx);
        d.classList.toggle("seen", seen.indexOf(i) > -1);
      });
      var pct = Math.round(((idx + 1) / steps.length) * 100);
      bar.firstChild.style.width = pct + "%";
      label.textContent = "Step " + (idx + 1) + " of " + steps.length + " · " + steps[idx].title;
      pos.textContent = (idx + 1) + " / " + steps.length;
      back.disabled = idx === 0;
      var last = idx === steps.length - 1;
      next.textContent = last ? "Finish ✓" : "Next →";
      nav.hidden = mode === "all";
      art.classList.toggle("bk-all", mode === "all");
    }
    function go(n) {
      if (n < 0) return;
      if (n >= steps.length) {
        /* Finish: mark the lesson complete if the page offers it */
        var mark = $("#fd-mark"); if (mark && !/done|complete ✓/i.test(mark.textContent)) { try { mark.click(); } catch (e) {} }
        celebrate("Lesson finished. Well done!");
        var nextLink = $(".bk-step-finish a.btn-primary, .row a.btn-primary[href*='../']", art);
        if (nextLink) nextLink.focus();
        return;
      }
      idx = n;
      if (seen.indexOf(n) === -1) seen.push(n);
      store(key, { step: idx, mode: mode, seen: seen });
      paint();
      if (mode !== "all") {
        var top = rail.getBoundingClientRect().top + root.pageYOffset - 70;
        try { root.scrollTo({ top: Math.max(0, top), behavior: REDUCED ? "auto" : "smooth" }); } catch (e) { root.scrollTo(0, Math.max(0, top)); }
        var hd = $("h2, h3, .bk-ex-title", steps[idx].el); if (hd) { hd.setAttribute("tabindex", "-1"); try { hd.focus({ preventScroll: true }); } catch (e) {} }
        /* replay the sign animation each time its page opens */
        $$(".bk-sign", steps[idx].el).forEach(function (s) { s.classList.remove("play"); void s.offsetWidth; s.classList.add("play"); });
        $$(".bk-ink", steps[idx].el).forEach(function (s) { s.classList.remove("play"); void s.offsetWidth; s.classList.add("play"); });
      }
    }
    function setMode(m) {
      mode = m; toggle.setAttribute("aria-pressed", m === "all" ? "true" : "false"); toggle.textContent = m === "all" ? "Step by step" : "Whole lesson";
      store(key, { step: idx, mode: mode, seen: seen }); paint();
    }
    doc.addEventListener("keydown", function (e) {
      if (mode === "all" || e.altKey || e.ctrlKey || e.metaKey) return;
      var t = e.target; if (t && /INPUT|TEXTAREA|SELECT/.test(t.tagName)) return;
      if (e.key === "ArrowRight") { go(idx + 1); e.preventDefault(); }
      if (e.key === "ArrowLeft") { go(idx - 1); e.preventDefault(); }
    });
    /* practice results: remember the best score per exercise */
    art.addEventListener("bk:done", function (e) {
      var d = e.detail || {}; var k = key + ".scores"; var sc = store(k) || {};
      var prev = sc[d.kind] || 0; var now = d.total ? d.right / d.total : 0;
      if (now >= prev) sc[d.kind] = now; store(k, sc);
      var dot = e.target.closest(".bk-step"); if (dot) { var i = steps.map(function (s) { return s.el; }).indexOf(dot); if (i > -1) dots.children[i].firstChild.classList.add(now === 1 ? "perfect" : "tried"); }
    });

    if (seen.indexOf(idx) === -1) seen.push(idx);
    paint();
    if (mode !== "all") { $$(".bk-sign, .bk-ink", steps[idx].el).forEach(function (s) { s.classList.add("play"); }); }
    root.EkGuruBook = { go: go, level: !!level, steps: steps.length, mode: function () { return mode; }, words: words.length, lines: lines.length, akshar: akshar };
  }

  function init() {
    var lv = $(".lv-main");
    if (lv && $('td[data-h="Word"]', lv)) return mount(lv, true);   /* a level page, not the levels hub */
    if (lv) return;
    var art = $(".art[data-book-mode]") || ($("#fd-mark") ? $("#fd-mark").closest(".art") : null);
    if (!art) return;
    mount(art, false);
  }
  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", init); else init();
})(window, document);

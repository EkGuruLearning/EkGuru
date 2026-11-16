# -*- coding: utf-8 -*-
"""EkGuru — Hindi Foundation (हिंदी की नींव): the content.

The way Indian children learn to read in class 1: अक्षर → मात्रा → शब्द → वाक्य.
One sign at a time, and every word in a lesson uses ONLY the signs taught so far
(the builder enforces that — see validate() in build-hindi-foundation.py).

Word tuple:      (devanagari, roman, english)
Sentence tuple:  (devanagari, roman, english)
Letter tuple:    (letter, roman, sound hint, keyword devanagari, keyword roman, keyword english, emoji)

Romanisation follows the site convention (aa / ee / oo), a guide to the sound,
not a standard.
"""

# ---------------------------------------------------------------- signs
MATRA = {
    "aa": "\u093e", "i": "\u093f", "ee": "\u0940", "u": "\u0941", "oo": "\u0942",
    "ri": "\u0943", "e": "\u0947", "ai": "\u0948", "o": "\u094b", "au": "\u094c",
    "an": "\u0902", "ah": "\u0903", "chandra": "\u0901", "halant": "\u094d",
}

# Little words that appear in almost every Hindi sentence. Children learn their
# SHAPE first and their matras later; lesson 5 introduces them as sight words,
# and the validator lets sentences (never word lists) use them from then on.
SIGHT_WORDS = [
    ("है", "hai", "is"),
    ("हैं", "hain", "are"),
    ("में", "mein", "in"),
    ("और", "aur", "and"),
    ("का", "kaa", "of (m.)"), ("की", "kee", "of (f.)"), ("के", "ke", "of (pl.)"),
    ("को", "ko", "to"), ("से", "se", "from / with"), ("ने", "ne", "(past-tense marker)"),
    ("यह", "yah", "this"), ("वह", "vah", "that"),
]

# ---------------------------------------------------------------- lesson 1
VOWELS = [
    ("अ", "a", "the u in 'but'", "अनार", "anaar", "pomegranate", "🫐"),
    ("आ", "aa", "the a in 'father'", "आम", "aam", "mango", "🥭"),
    ("इ", "i", "the i in 'sit'", "इमली", "imlee", "tamarind", "🌰"),
    ("ई", "ee", "the ee in 'see'", "ईख", "eekh", "sugarcane", "🎋"),
    ("उ", "u", "the u in 'put'", "उल्लू", "ulloo", "owl", "🦉"),
    ("ऊ", "oo", "the oo in 'boot'", "ऊन", "oon", "wool", "🧶"),
    ("ऋ", "ri", "ri, as in 'rip' (a vowel in Hindi)", "ऋषि", "rishi", "sage", "🧘"),
    ("ए", "e", "the a in 'gate', no glide", "एड़ी", "eree", "heel", "🦶"),
    ("ऐ", "ai", "the a in 'cat', long", "ऐनक", "ainak", "spectacles", "👓"),
    ("ओ", "o", "the o in 'go', no glide", "ओखली", "okhlee", "mortar (for grinding)", "🪨"),
    ("औ", "au", "the o in 'hot', long", "औरत", "aurat", "woman", "👩"),
    ("अं", "an", "a + a nasal hum", "अंगूर", "angoor", "grapes", "🍇"),
    ("अः", "ah", "a + a soft breath", "नमः", "namah", "(as in 'namah', a bow)", "🙏"),
]

# ---------------------------------------------------------------- lessons 2–4
KA_CHA = [
    ("क", "ka", "k in 'skip' (no puff of air)", "कबूतर", "kabootar", "pigeon", "🕊️"),
    ("ख", "kha", "k with a strong puff of air", "खरगोश", "khargosh", "rabbit", "🐇"),
    ("ग", "ga", "g in 'go'", "गमला", "gamlaa", "flower pot", "🪴"),
    ("घ", "gha", "g with a breathy puff", "घर", "ghar", "house", "🏠"),
    ("ङ", "nga", "ng in 'sing' — never starts a word", "रंग", "rang", "colour (the ng inside it)", "🎨"),
    ("च", "cha", "ch in 'chip', no puff", "चम्मच", "chammach", "spoon", "🥄"),
    ("छ", "chha", "ch with a strong puff", "छाता", "chhaataa", "umbrella", "☂️"),
    ("ज", "ja", "j in 'jug'", "जहाज", "jahaaj", "ship", "🚢"),
    ("झ", "jha", "j with a breathy puff", "झंडा", "jhandaa", "flag", "🚩"),
    ("ञ", "nya", "ny in 'canyon' — lives inside ज्ञ", "ज्ञान", "gyaan", "knowledge (the ञ hides in ज्ञ)", "📚"),
]
TA_TA = [
    ("ट", "ṭa", "t with the tongue curled back", "टमाटर", "tamaatar", "tomato", "🍅"),
    ("ठ", "ṭha", "ट with a puff of air", "ठेला", "thelaa", "handcart", "🛒"),
    ("ड", "ḍa", "d with the tongue curled back", "डमरू", "damaroo", "hand drum", "🥁"),
    ("ढ", "ḍha", "ड with a breathy puff", "ढक्कन", "dhakkan", "lid", "🫙"),
    ("ण", "ṇa", "n with the tongue curled back", "बाण", "baan", "arrow (the ण at the end)", "🏹"),
    ("त", "ta", "soft t, tongue on the teeth", "तरबूज", "tarbooj", "watermelon", "🍉"),
    ("थ", "tha", "त with a puff of air", "थाली", "thaalee", "plate", "🍽️"),
    ("द", "da", "soft d, tongue on the teeth", "दरवाजा", "darvaajaa", "door", "🚪"),
    ("ध", "dha", "द with a breathy puff", "धनुष", "dhanush", "bow", "🏹"),
    ("न", "na", "n in 'no'", "नल", "nal", "tap", "🚰"),
]
PA_REST = [
    ("प", "pa", "p in 'spin', no puff", "पतंग", "patang", "kite", "🪁"),
    ("फ", "pha", "p with a strong puff", "फल", "phal", "fruit", "🍎"),
    ("ब", "ba", "b in 'bat'", "बतख", "batakh", "duck", "🦆"),
    ("भ", "bha", "b with a breathy puff", "भालू", "bhaaloo", "bear", "🐻"),
    ("म", "ma", "m in 'mat'", "मछली", "machhlee", "fish", "🐟"),
    ("य", "ya", "y in 'yes'", "योग", "yog", "yoga", "🧘"),
    ("र", "ra", "a light, tapped r", "रथ", "rath", "chariot", "🛞"),
    ("ल", "la", "l in 'lamp'", "लोमड़ी", "lomree", "fox", "🦊"),
    ("व", "va", "between v and w", "वन", "van", "forest", "🌳"),
    ("श", "sha", "sh in 'ship'", "शेर", "sher", "lion", "🦁"),
    ("ष", "sha", "sh, tongue curled back", "षट्कोण", "shatkon", "hexagon", "⬡"),
    ("स", "sa", "s in 'sun'", "सेब", "seb", "apple", "🍎"),
    ("ह", "ha", "h in 'hat'", "हाथी", "haathee", "elephant", "🐘"),
    ("क्ष", "ksha", "k + sh, said together", "क्षत्रिय", "kshatriya", "warrior", "⚔️"),
    ("त्र", "tra", "t + r, said together", "त्रिशूल", "trishool", "trident", "🔱"),
    ("ज्ञ", "gya", "said 'gya' in Hindi", "ज्ञानी", "gyaanee", "a wise person", "📚"),
]

# ---------------------------------------------------------------- word lessons
LESSONS = [
    # ------------------------------------------------------------ 1
    dict(
        n=1, slug="swar", kind="letters",
        hi="स्वर", en="The vowels", sub="13 letters that make a sound on their own",
        lede="A Hindi primer always opens with the स्वर (swar) — the vowels. Each one is a sound "
             "you can hold with your mouth open: say it, trace it, meet the word every Indian "
             "child learns it with.",
        letters=VOWELS,
        notes=[
            "There are eleven vowel letters plus two 'extras': <b>अं</b> adds a nasal hum and "
            "<b>अः</b> a soft breath. Children chant all thirteen as one song: "
            "<span class=\"spk\" lang=\"hi\">अ आ इ ई उ ऊ ऋ ए ऐ ओ औ अं अः</span>.",
            "Short and long come in pairs — <b>अ/आ, इ/ई, उ/ऊ</b>. The long one is simply held "
            "about twice as long. Getting the length wrong changes the word: "
            "<span class=\"spk\" lang=\"hi\">दिन</span> (day) vs <span class=\"spk\" lang=\"hi\">दीन</span> (poor).",
            "These full letters appear at the <b>start</b> of a word or after another vowel. "
            "Inside a word, after a consonant, the vowel shrinks to a sign — the मात्रा — "
            "which is lesson 6 onwards.",
        ],
        task="Say the thirteen vowels aloud in order, three times. Then write अ to अः once each, "
             "saying the sound as your pen moves. Hand and mouth learn together.",
        quiz=[
            ("Which vowel is long: इ or ई?", "ई. The long one is held about twice as long — like 'see' against 'sit'."),
            ("What do अं and अः add?", "अं adds a nasal hum (like the ng in 'sing'); अः adds a soft puff of breath."),
            ("Where do full vowel letters appear?", "At the start of a word, or after another vowel. After a consonant the vowel becomes a मात्रा sign."),
        ],
    ),
    # ------------------------------------------------------------ 2
    dict(
        n=2, slug="vyanjan-1", kind="letters",
        hi="व्यंजन — क वर्ग और च वर्ग", en="Consonants 1 — the throat and palate rows",
        sub="क ख ग घ ङ · च छ ज झ ञ",
        lede="Hindi consonants (व्यंजन, vyanjan) come in rows of five, arranged by where the "
             "tongue sits. Row one is made at the back of the throat, row two at the palate. "
             "Every letter already contains an 'a': क is 'ka', never a bare 'k'.",
        letters=KA_CHA,
        notes=[
            "Each row runs <b>plain · puffed · voiced · voiced-puffed · nasal</b>. Hold your palm "
            "in front of your mouth: <span class=\"spk\" lang=\"hi\">क</span> gives no air, "
            "<span class=\"spk\" lang=\"hi\">ख</span> gives a puff. That puff is the whole difference "
            "between <span class=\"spk\" lang=\"hi\">कल</span> (tomorrow) and <span class=\"spk\" lang=\"hi\">खल</span> (villain).",
            "<b>ङ</b> and <b>ञ</b> never start a word. Children learn their shape and move on; "
            "you will meet them inside words like रंग and ज्ञान.",
        ],
        task="Write the row क ख ग घ ङ five times, saying each letter. Then च छ ज झ ञ. Use the "
             "headline — the horizontal bar on top — like washing on a line: letters hang from it.",
        quiz=[
            ("How is ख different from क?", "A puff of air. Say both with your palm in front of your mouth — only ख moves it."),
            ("What sound is built into every consonant?", "A short 'a'. क is 'ka', म is 'ma'. Removing it needs a special sign (lesson 17)."),
            ("Which two letters here never begin a word?", "ङ and ञ. They live inside words — रंग, ज्ञान."),
        ],
    ),
    # ------------------------------------------------------------ 3
    dict(
        n=3, slug="vyanjan-2", kind="letters",
        hi="व्यंजन — ट वर्ग और त वर्ग", en="Consonants 2 — the two T rows",
        sub="ट ठ ड ढ ण · त थ द ध न",
        lede="English has one t and one d. Hindi has two of each, and the difference is where "
             "the tongue touches: curled back to the roof of the mouth for ट ड, or flat against "
             "the teeth for त द. This is the row English speakers find hardest — and the row "
             "every Indian child drills the most.",
        letters=TA_TA,
        notes=[
            "<b>ट ठ ड ढ ण</b> are the <i>retroflex</i> row: tongue tip curled up and back. "
            "English 't' in 'top' is close to ट. <b>त थ द ध न</b> are the <i>dental</i> row: "
            "tongue on the back of the top teeth, like a Spanish or French t.",
            "Two letters get a dot underneath to become new sounds: <span class=\"spk\" lang=\"hi\">ड़</span> "
            "(a flapped r, as in <span class=\"spk\" lang=\"hi\">सड़क</span>, road) and "
            "<span class=\"spk\" lang=\"hi\">ढ़</span> (<span class=\"spk\" lang=\"hi\">पढ़</span>, read). "
            "Treat them as letters in their own right.",
            "Minimal pair to drill: <span class=\"spk\" lang=\"hi\">टाल</span> (postpone) vs "
            "<span class=\"spk\" lang=\"hi\">ताल</span> (rhythm / pond).",
        ],
        task="Say ट ट ट with the tongue curled back, then त त त with the tongue on your teeth. "
             "Feel the difference before you write. Then copy both rows twice.",
        quiz=[
            ("Where is the tongue for ट?", "Curled up and back, touching the roof of the mouth (retroflex)."),
            ("Where is the tongue for त?", "Flat against the back of the top teeth (dental) — softer than an English t."),
            ("What does the dot under ड do?", "Makes ड़ — a flapped r sound, as in सड़क (road). Same for ढ़ in पढ़ (read)."),
        ],
    ),
    # ------------------------------------------------------------ 4
    dict(
        n=4, slug="vyanjan-3", kind="letters",
        hi="व्यंजन — प वर्ग, य र ल व, श ष स ह, क्ष त्र ज्ञ", en="Consonants 3 — lips, semivowels, sibilants and the three joined letters",
        sub="प फ ब भ म · य र ल व · श ष स ह · क्ष त्र ज्ञ",
        lede="The last row is made with the lips, then come the four 'in-between' letters, the "
             "three hissing sounds and ह. Indian primers finish the chart with क्ष, त्र and ज्ञ — "
             "three joined letters so common that children learn them as single shapes.",
        letters=PA_REST,
        notes=[
            "<b>फ</b> is p with a puff, not an English f. The f sound is written "
            "<span class=\"spk\" lang=\"hi\">फ़</span> with a dot, in borrowed words like फ़ोन.",
            "<b>व</b> sits between v and w; nobody will mind which you say. "
            "<b>श</b> and <b>ष</b> both sound like 'sh' in everyday Hindi.",
            "<b>क्ष त्र ज्ञ</b> are really two letters joined (क+ष, त+र, ज+ञ). They close every "
            "alphabet chart in India, so meet them now and learn how joining works in lesson 17.",
        ],
        task="Copy the full chart now — all 33 consonants plus क्ष त्र ज्ञ — row by row, saying "
             "each letter. Keep the page: it is your reference for the next fourteen lessons.",
        quiz=[
            ("Is फ an f sound?", "No — it is p with a strong puff of air. The f sound is फ़, with a dot, in words like फ़ोन."),
            ("What is ज्ञ made of?", "ज + ञ joined. In modern Hindi it is said 'gya', as in ज्ञान (knowledge)."),
            ("How many consonants in the chart?", "33 — five rows of five (25), plus य र ल व and श ष स ह — with क्ष त्र ज्ञ added at the end as joined letters."),
        ],
    ),
    # ------------------------------------------------------------ 5
    dict(
        n=5, slug="bina-matra", kind="words", allow=set(),
        hi="बिना मात्रा के शब्द", en="Words with no matra",
        sub="Two, three and four letters — just consonants and their built-in 'a'",
        lede="Before any vowel sign, a child reads words made of bare consonants: "
             "क-म-ल, कमल. Every letter says its own 'a'. Sound each letter out, then blend — "
             "slowly at first, and the speed arrives on its own.",
        sign=None,
        groups=[
            ("दो अक्षर · two letters", [
                ("घर", "ghar", "house"), ("जल", "jal", "water"), ("फल", "phal", "fruit"), ("नल", "nal", "tap"),
                ("कल", "kal", "yesterday / tomorrow"), ("बस", "bas", "bus; enough"), ("दस", "das", "ten"), ("मन", "man", "mind"),
                ("वन", "van", "forest"), ("धन", "dhan", "wealth"), ("हल", "hal", "plough"), ("पल", "pal", "moment"),
                ("रथ", "rath", "chariot"), ("पथ", "path", "path"), ("तन", "tan", "body"), ("गज", "gaj", "elephant"),
                ("छत", "chhat", "roof"), ("सच", "sach", "truth"), ("डर", "dar", "fear"), ("जग", "jag", "world"),
                ("मत", "mat", "don't"), ("अब", "ab", "now"), ("उठ", "uth", "get up"), ("चल", "chal", "walk, go"),
            ]),
            ("तीन अक्षर · three letters", [
                ("कमल", "kamal", "lotus"), ("नमक", "namak", "salt"), ("कलम", "kalam", "pen"), ("सड़क", "sarak", "road"),
                ("महल", "mahal", "palace"), ("गरम", "garam", "hot"), ("नरम", "naram", "soft"), ("सरल", "saral", "simple"),
                ("पवन", "pavan", "wind"), ("मटर", "matar", "peas"), ("शहद", "shahad", "honey"), ("भजन", "bhajan", "devotional song"),
                ("भवन", "bhavan", "building"), ("नगर", "nagar", "town"), ("गगन", "gagan", "sky"), ("रबड़", "rabar", "eraser"),
                ("पकड़", "pakar", "catch, hold"), ("समझ", "samajh", "understanding"), ("अजय", "Ajay", "a name"), ("सफल", "saphal", "successful"),
            ]),
            ("चार अक्षर · four letters", [
                ("अजगर", "ajgar", "python"), ("बरगद", "bargad", "banyan tree"), ("कसरत", "kasrat", "exercise"), ("मतलब", "matlab", "meaning"),
                ("शलजम", "shalgam", "turnip"), ("हरकत", "harkat", "movement"), ("बरतन", "bartan", "utensil"), ("पनघट", "panghat", "village well"),
                ("सरकस", "sarkas", "circus"), ("कटहल", "kathal", "jackfruit"), ("अदरक", "adrak", "ginger"), ("दशरथ", "Dashrath", "a name (Ram's father)"),
                ("हलचल", "halchal", "commotion"), ("नटखट", "natkhat", "naughty"), ("खटमल", "khatmal", "bedbug"), ("उपवन", "upvan", "garden"),
            ]),
        ],
        sentences=[
            ("घर चल।", "ghar chal.", "Go home."),
            ("नल पर चल।", "nal par chal.", "Go to the tap."),
            ("फल रख।", "phal rakh.", "Put the fruit down."),
            ("कलम पकड़।", "kalam pakar.", "Hold the pen."),
            ("सड़क पर मत चल।", "sarak par mat chal.", "Don't walk on the road."),
            ("नमक कम रख।", "namak kam rakh.", "Keep the salt low."),
            ("शहद चख।", "shahad chakh.", "Taste the honey."),
            ("दशरथ, रथ पर चढ़।", "Dashrath, rath par charh.", "Dashrath, climb onto the chariot."),
            ("अब उठ, कसरत कर।", "ab uth, kasrat kar.", "Now get up, do your exercise."),
        ],
        passage=("नटखट अजय", [
            ("अजय नटखट है।", "Ajay natkhat hai.", "Ajay is naughty."),
            ("वह घर पर है।", "vah ghar par hai.", "He is at home."),
            ("अजय, नमक मत चख।", "Ajay, namak mat chakh.", "Ajay, don't taste the salt."),
            ("अजय, शहद मत चख।", "Ajay, shahad mat chakh.", "Ajay, don't taste the honey."),
            ("अब बस। कलम पकड़।", "ab bas. kalam pakar.", "Enough now. Hold the pen."),
            ("क ख ग घ… अजय सफल है।", "ka kha ga gha… Ajay saphal hai.", "ka kha ga gha… Ajay has done it."),
        ]),
        sight=True,
        task="Copy all three ladders into a notebook, two letters first. Then close the book and "
             "write the words as someone reads them to you — dictation (श्रुतलेख) is how every "
             "Indian classroom checks this lesson.",
        quiz=[
            ("How do you read कमल?", "Letter by letter — क म ल, each with its own 'a' — then blend: kamal."),
            ("What is है?", "'Is'. It carries a sign you have not learnt yet, so learn its shape now as a sight word."),
            ("Why no है in 'घर चल'?", "It is a command — go home! Commands in Hindi need no 'is'."),
        ],
    ),
    # ------------------------------------------------------------ 6
    dict(
        n=6, slug="aa-ki-matra", kind="words", allow={"aa"},
        hi="आ की मात्रा (ा)", en="The aa matra — ा",
        sub="One straight stroke after the letter: क + ा = का",
        lede="The first matra every child learns is the easiest to see: a single vertical stroke "
             "to the right of the letter, hanging from the headline. It turns the short 'a' into "
             "the long 'aa' of 'father'. क becomes का; म becomes मा; put them together and you "
             "can already read माता and काका.",
        sign=("ा", "aa", "क", "का", "kaa"),
        groups=[
            ("दो अक्षर · two letters", [
                ("आम", "aam", "mango"), ("आज", "aaj", "today"), ("काका", "kaakaa", "uncle (father's younger brother)"), ("दादा", "daadaa", "grandfather"),
                ("नाना", "naanaa", "grandfather (mother's side)"), ("माता", "maataa", "mother"), ("माला", "maalaa", "garland"), ("राजा", "raajaa", "king"),
                ("बाजा", "baajaa", "musical instrument"), ("छाता", "chhaataa", "umbrella"), ("गाना", "gaanaa", "song"), ("खाना", "khaanaa", "food"),
                ("काला", "kaalaa", "black"), ("लाल", "laal", "red"), ("साल", "saal", "year"), ("बाल", "baal", "hair"),
                ("हाथ", "haath", "hand"), ("नाक", "naak", "nose"), ("कान", "kaan", "ear"), ("दाल", "daal", "lentils"),
                ("नाम", "naam", "name"), ("काम", "kaam", "work"), ("आग", "aag", "fire"), ("गाय", "gaay", "cow"),
                ("चाय", "chaay", "tea"), ("दाम", "daam", "price"), ("चाचा", "chaachaa", "uncle"), ("नाव", "naav", "boat"),
                ("सात", "saat", "seven"), ("आठ", "aath", "eight"), ("राम", "Raam", "Ram (a name)"), ("जाल", "jaal", "net"),
            ]),
            ("तीन अक्षर · three letters", [
                ("बाजार", "baajaar", "market"), ("आकाश", "aakaash", "sky"), ("कागज", "kaagaj", "paper"), ("तालाब", "taalaab", "pond"),
                ("अनार", "anaar", "pomegranate"), ("सलाद", "salaad", "salad"), ("पालक", "paalak", "spinach"), ("गाजर", "gaajar", "carrot"),
                ("सामान", "saamaan", "luggage, things"), ("आराम", "aaraam", "rest"), ("बादल", "baadal", "cloud"), ("नाराज", "naaraaj", "angry"),
                ("सवाल", "savaal", "question"), ("जवाब", "javaab", "answer"), ("मकान", "makaan", "house"), ("समाज", "samaaj", "society"),
                ("बालक", "baalak", "boy"), ("चावल", "chaaval", "rice"), ("नाटक", "naatak", "play, drama"), ("आदत", "aadat", "habit"),
            ]),
            ("चार अक्षर · four letters", [
                ("पाठशाला", "paathshaalaa", "school"), ("दरवाजा", "darvaajaa", "door"), ("कारखाना", "kaarkhaanaa", "factory"), ("जानवर", "jaanvar", "animal"),
                ("आसमान", "aasmaan", "sky"), ("रामायण", "Raamaayan", "the Ramayana"), ("अखबार", "akhbaar", "newspaper"), ("टमाटर", "tamaatar", "tomato"),
                ("बरसात", "barsaat", "rainy season"), ("कामकाज", "kaamkaaj", "work, chores"), ("आरामगाह", "aaraamgaah", "resting place"), ("हलवाई", "halvaaee", "sweet-maker"),
            ]),
        ],
        sentences=[
            ("आज आम खा।", "aaj aam khaa.", "Eat a mango today."),
            ("राम घर जा।", "Raam ghar jaa.", "Ram, go home."),
            ("माता जल ला।", "maataa jal laa.", "Mother, bring water."),
            ("काका बाजार जा।", "kaakaa baajaar jaa.", "Uncle, go to the market."),
            ("दादा चाय ला।", "daadaa chaay laa.", "Grandfather, bring tea."),
            ("नाव जल पर है।", "naav jal par hai.", "The boat is on the water."),
            ("राजा का महल बड़ा है।", "raajaa kaa mahal baraa hai.", "The king's palace is big."),
            ("काका का बाल काला है।", "kaakaa kaa baal kaalaa hai.", "Uncle's hair is black."),
            ("बादल आसमान में हैं।", "baadal aasmaan mein hain.", "The clouds are in the sky."),
        ],
        passage=("राम का घर", [
            ("राम का घर बड़ा है।", "Raam kaa ghar baraa hai.", "Ram's house is big."),
            ("घर में माता, काका और दादा हैं।", "ghar mein maataa, kaakaa aur daadaa hain.", "In the house are mother, uncle and grandfather."),
            ("आज बाजार जाना है।", "aaj baajaar jaanaa hai.", "Today we have to go to the market."),
            ("काका आम, अनार और गाजर लाया।", "kaakaa aam, anaar aur gaajar laayaa.", "Uncle brought mangoes, pomegranate and carrots."),
            ("माता दाल और चावल बना।", "maataa daal aur chaaval banaa.", "Mother, make dal and rice."),
            ("दादा चाय के साथ अखबार पढ़।", "daadaa chaay ke saath akhbaar parh.", "Grandfather, read the paper with your tea."),
            ("राम, हाथ साफ कर, खाना खा।", "Raam, haath saaph kar, khaanaa khaa.", "Ram, clean your hands, eat your food."),
        ]),
        task="Write का खा गा घा … for the whole consonant chart — every letter wearing ा. Then "
             "copy the two-letter words twice and take dictation of ten of them.",
        quiz=[
            ("Where does ा go?", "To the right of the consonant, as one vertical stroke hanging from the headline: क → का."),
            ("What is the difference between कम and काम?", "कम (kam, less) has the built-in short a; काम (kaam, work) wears ा and is held long."),
            ("Why does आम start with आ and not ा?", "A matra needs a consonant to sit on. At the start of a word, with no consonant before it, the full vowel letter आ is used."),
        ],
    ),
    # ------------------------------------------------------------ 7
    dict(
        n=7, slug="i-ki-matra", kind="words", allow={"aa", "i"},
        hi="इ की मात्रा (ि)", en="The i matra — ि",
        sub="The sign that is written BEFORE the letter but read after it: क + ि = कि",
        lede="This is the matra that surprises everyone. The short 'i' sign stands to the LEFT of "
             "its consonant — you write it first, but you say it second. कि is 'ki', not 'ik'. "
             "Children chant 'छोटी इ की मात्रा पहले' — the small i goes first — until it sticks.",
        sign=("ि", "i", "क", "कि", "ki"),
        groups=[
            ("दो अक्षर · two letters", [
                ("दिन", "din", "day"), ("गिन", "gin", "count"), ("तिल", "til", "sesame"), ("दिल", "dil", "heart"),
                ("मिल", "mil", "meet"), ("सिर", "sir", "head"), ("बिल", "bil", "bill; burrow"), ("कवि", "kavi", "poet"),
                ("रवि", "ravi", "sun; a name"), ("शिव", "Shiv", "Shiva"), ("पिता", "pitaa", "father"), ("किला", "kilaa", "fort"),
                ("दिया", "diyaa", "oil lamp"), ("जिला", "jilaa", "district"), ("चिता", "chitaa", "pyre"), ("हानि", "haani", "loss"),
            ]),
            ("तीन अक्षर · three letters", [
                ("किताब", "kitaab", "book"), ("हिरन", "hiran", "deer"), ("गिलास", "gilaas", "glass (tumbler)"), ("सितार", "sitaar", "sitar"),
                ("विमान", "vimaan", "aeroplane"), ("किसान", "kisaan", "farmer"), ("किरण", "kiran", "ray of light"), ("टिकट", "tikat", "ticket"),
                ("निकल", "nikal", "come out"), ("मालिक", "maalik", "owner"), ("नियम", "niyam", "rule"), ("विचार", "vichaar", "thought"),
                ("हिसाब", "hisaab", "account, sums"), ("बारिश", "baarish", "rain"), ("शिकार", "shikaar", "hunting"), ("अधिक", "adhik", "more"),
                ("डाकिया", "daakiyaa", "postman"), ("तकिया", "takiyaa", "pillow"), ("पहिया", "pahiyaa", "wheel"), ("गिटार", "gitaar", "guitar"),
            ]),
            ("चार अक्षर · four letters", [
                ("शनिवार", "shanivaar", "Saturday"), ("रविवार", "ravivaar", "Sunday"), ("नारियल", "naariyal", "coconut"), ("किनारा", "kinaaraa", "shore, edge"),
                ("शिकायत", "shikaayat", "complaint"), ("अमिताभ", "Amitaabh", "a name"), ("विशाल", "vishaal", "huge"), ("हिमालय", "Himaalay", "the Himalayas"),
                ("दिनभर", "dinbhar", "all day"), ("चिड़िया", "chiriyaa", "bird"), ("नदिया", "nadiyaa", "river (poetic)"), ("पिघल", "pighal", "melt"),
            ]),
        ],
        sentences=[
            ("रवि दिन भर किताब पढ़।", "Ravi din bhar kitaab parh.", "Ravi, read your book all day."),
            ("किसान हल चला।", "kisaan hal chalaa.", "The farmer drove the plough."),
            ("पिता घर पर हैं।", "pitaa ghar par hain.", "Father is at home."),
            ("हिरन वन में है।", "hiran van mein hai.", "The deer is in the forest."),
            ("गिलास में जल है।", "gilaas mein jal hai.", "There is water in the glass."),
            ("चिड़िया किला पर है।", "chiriyaa kilaa par hai.", "The bird is on the fort."),
            ("आज शनिवार है, कल रविवार।", "aaj shanivaar hai, kal ravivaar.", "Today is Saturday, tomorrow Sunday."),
            ("डाकिया टिकट लाया।", "daakiyaa tikat laayaa.", "The postman brought the stamp."),
            ("बारिश में विमान मत चला।", "baarish mein vimaan mat chalaa.", "Don't fly the plane in the rain."),
        ],
        passage=("किसान और बारिश", [
            ("किसान का नाम किशन है।", "kisaan kaa naam Kishan hai.", "The farmer's name is Kishan."),
            ("किशन दिन भर काम करता है।", "Kishan din bhar kaam kartaa hai.", "Kishan works all day."),
            ("आज बारिश है।", "aaj baarish hai.", "Today there is rain."),
            ("हिरन वन में भाग गया।", "hiran van mein bhaag gayaa.", "The deer ran into the forest."),
            ("चिड़िया नारियल पर आ गई।", "chiriyaa naariyal par aa gaee.", "The bird came onto the coconut tree."),
            ("किशन घर आया। पिता चाय लाया।", "Kishan ghar aayaa. pitaa chaay laayaa.", "Kishan came home. Father brought tea."),
            ("कल रविवार है — आराम का दिन।", "kal ravivaar hai — aaraam kaa din.", "Tomorrow is Sunday — a day of rest."),
        ]),
        task="Write कि खि गि घि … for the whole chart. Say 'first the sign, then the letter' each "
             "time you write, and 'letter, then i' each time you read. Dictation of ten words.",
        quiz=[
            ("Where is ि written?", "To the LEFT of the consonant — but it is read AFTER it. कि is 'ki'."),
            ("How is दिन read?", "द + ि = दि (di), then न: din — 'day'."),
            ("What is the trap in किला?", "Seeing ि first and reading 'ik'. The sign belongs to the letter on its right: कि-ला."),
        ],
    ),
    # ------------------------------------------------------------ 8
    dict(
        n=8, slug="ee-ki-matra", kind="words", allow={"aa", "i", "ee"},
        hi="ई की मात्रा (ी)", en="The ee matra — ी",
        sub="The same hook, but after the letter and held long: क + ी = की",
        lede="The long 'ee' sign looks like the short one flipped: it stands to the RIGHT of the "
             "letter and the sound is held, like 'see'. So ि before = short, ी after = long. "
             "Hindi loves this sound — most feminine words end in it: लड़की, बकरी, रोटी.",
        sign=("ी", "ee", "क", "की", "kee"),
        groups=[
            ("दो अक्षर · two letters", [
                ("नदी", "nadee", "river"), ("पानी", "paanee", "water"), ("रानी", "raanee", "queen"), ("पीला", "peelaa", "yellow"),
                ("नीला", "neelaa", "blue"), ("गली", "galee", "lane"), ("खीर", "kheer", "rice pudding"), ("चीनी", "cheenee", "sugar"),
                ("सीता", "Seetaa", "Sita"), ("गीता", "Geetaa", "Gita"), ("नीम", "neem", "neem tree"), ("तीन", "teen", "three"),
                ("बीस", "bees", "twenty"), ("सीख", "seekh", "learn"), ("दीदी", "deedee", "elder sister"), ("नानी", "naanee", "grandmother"),
                ("दादी", "daadee", "grandmother"), ("हीरा", "heeraa", "diamond"), ("वीर", "veer", "brave"), ("बीज", "beej", "seed"),
                ("जीत", "jeet", "victory"), ("मीठा", "meethaa", "sweet"), ("भीड़", "bheer", "crowd"), ("सीधा", "seedhaa", "straight"),
            ]),
            ("तीन अक्षर · three letters", [
                ("लड़की", "larkee", "girl"), ("बकरी", "bakree", "goat"), ("मछली", "machhlee", "fish"), ("तितली", "titlee", "butterfly"),
                ("हाथी", "haathee", "elephant"), ("दीवार", "deevaar", "wall"), ("मिठाई", "mithaaee", "sweets"), ("मशीन", "masheen", "machine"),
                ("कीमत", "keemat", "price"), ("जमीन", "jameen", "land"), ("शरीर", "shareer", "body"), ("पनीर", "paneer", "paneer"),
                ("कहानी", "kahaanee", "story"), ("साड़ी", "saaree", "saree"), ("पीपल", "peepal", "peepal tree"), ("सीढ़ी", "seerhee", "stairs"),
                ("ककड़ी", "kakree", "cucumber"), ("आदमी", "aadmee", "man"), ("नदी", "nadee", "river"), ("गरीब", "gareeb", "poor"),
            ]),
            ("चार अक्षर · four letters", [
                ("खिड़की", "khirkee", "window"), ("पहाड़ी", "pahaaree", "hill"), ("खिलाड़ी", "khilaaree", "player"), ("दीपावली", "Deepaavalee", "Diwali"),
                ("जानकारी", "jaankaaree", "information"), ("अलमारी", "almaaree", "cupboard"), ("तीसरा", "teesraa", "third"), ("नीलामी", "neelaamee", "auction"),
                ("बीमारी", "beemaaree", "illness"), ("गिलहरी", "gilahree", "squirrel"),
            ]),
        ],
        sentences=[
            ("नदी का पानी नीला है।", "nadee kaa paanee neelaa hai.", "The river's water is blue."),
            ("दीदी खीर बनाती है।", "deedee kheer banaatee hai.", "Elder sister makes kheer."),
            ("मछली पानी में रहती है।", "machhlee paanee mein rahtee hai.", "The fish lives in water."),
            ("सीता गली में खड़ी है।", "Seetaa galee mein kharee hai.", "Sita is standing in the lane."),
            ("हाथी बड़ा है।", "haathee baraa hai.", "The elephant is big."),
            ("नानी कहानी कहती है।", "naanee kahaanee kahtee hai.", "Grandmother tells a story."),
            ("बकरी घास खाती है।", "bakree ghaas khaatee hai.", "The goat eats grass."),
            ("लड़की साड़ी पहनती है।", "larkee saaree pahantee hai.", "The girl wears a saree."),
            ("खिड़की से तितली आई।", "khirkee se titlee aaee.", "A butterfly came in through the window."),
        ],
        passage=("नानी की कहानी", [
            ("रात है। दीदी और मीना नानी के पास हैं।", "raat hai. deedee aur Meenaa naanee ke paas hain.", "It is night. Elder sister and Meena are with grandmother."),
            ("नानी कहानी कहती है।", "naanee kahaanee kahtee hai.", "Grandmother tells a story."),
            ("एक नदी थी। नदी का पानी नीला था।", "ek nadee thee. nadee kaa paanee neelaa thaa.", "There was a river. The river's water was blue."),
            ("नदी में मछली रहती थी।", "nadee mein machhlee rahtee thee.", "A fish lived in the river."),
            ("पास ही पीपल था। पीपल पर तितली थी।", "paas hee peepal thaa. peepal par titlee thee.", "Nearby was a peepal tree. On the peepal was a butterfly."),
            ("मछली और तितली में यारी थी।", "machhlee aur titlee mein yaaree thee.", "The fish and the butterfly were friends."),
            ("मीना थक गई। कहानी कल।", "Meenaa thak gaee. kahaanee kal.", "Meena got tired. The story continues tomorrow."),
        ]),
        task="Write दिन / दीन, मिल / मील, सिल / सील — short and long side by side — and say them. "
             "Then copy the three-letter words and take dictation of ten.",
        quiz=[
            ("Which side of the letter does ी go on?", "The RIGHT side. ि (short) goes on the left, ी (long) on the right."),
            ("How long is the sound in नीला?", "Held long, like 'see'. नीला is neelaa — blue."),
            ("Why do so many words end in ी?", "It is the usual feminine ending — लड़की, बकरी, रोटी, साड़ी — and shows up in words for 'she does': खाती, कहती."),
        ],
    ),
    # ------------------------------------------------------------ 9
    dict(
        n=9, slug="u-ki-matra", kind="words", allow={"aa", "i", "ee", "u"},
        hi="उ की मात्रा (ु)", en="The u matra — ु",
        sub="A small hook under the letter: क + ु = कु",
        lede="Now the signs move underneath. The short 'u' of 'put' is a little hook that hangs "
             "below the consonant. One letter cheats: र + ु is written रु with the hook tucked "
             "into its side — you will see it in गुरु.",
        sign=("ु", "u", "क", "कु", "ku"),
        groups=[
            ("दो अक्षर · two letters", [
                ("गुड़", "gur", "jaggery"), ("पुल", "pul", "bridge"), ("सुन", "sun", "listen"), ("चुप", "chup", "quiet"),
                ("मधु", "madhu", "honey"), ("गुरु", "guru", "teacher"), ("पशु", "pashu", "animal"), ("दुम", "dum", "tail"),
                ("खुश", "khush", "happy"), ("सुख", "sukh", "happiness"), ("दुख", "dukh", "sorrow"), ("तुम", "tum", "you"),
                ("कुछ", "kuchh", "something"), ("युवा", "yuvaa", "young person"), ("गुफा", "guphaa", "cave"), ("सुई", "suee", "needle"),
                ("धुन", "dhun", "tune"), ("बुरा", "buraa", "bad"), ("खुला", "khulaa", "open"), ("सुमन", "suman", "flower; a name"),
            ]),
            ("तीन अक्षर · three letters", [
                ("सुबह", "subah", "morning"), ("गुलाब", "gulaab", "rose"), ("साबुन", "saabun", "soap"), ("बुखार", "bukhaar", "fever"),
                ("कछुआ", "kachhuaa", "tortoise"), ("मुरली", "muralee", "flute"), ("दुकान", "dukaan", "shop"), ("बहुत", "bahut", "very, many"),
                ("सुनार", "sunaar", "goldsmith"), ("चतुर", "chatur", "clever"), ("मधुर", "madhur", "sweet (sound)"), ("कुमार", "kumaar", "prince; a name"),
                ("पुकार", "pukaar", "a call"), ("रुमाल", "rumaal", "handkerchief"), ("पुराना", "puraanaa", "old (thing)"), ("धनुष", "dhanush", "bow"),
                ("झुमका", "jhumkaa", "earring"), ("घुटना", "ghutnaa", "knee"), ("सुराही", "suraahee", "clay water-pitcher"), ("बुलबुल", "bulbul", "nightingale"),
            ]),
            ("चार अक्षर · four letters", [
                ("हनुमान", "Hanumaan", "Hanuman"), ("पुजारी", "pujaaree", "priest"), ("बुढ़िया", "burhiyaa", "old woman"), ("सुनहरा", "sunahraa", "golden"),
                ("मुसाफिर", "musaaphir", "traveller"), ("गुलाबी", "gulaabee", "pink"), ("दुकानदार", "dukaandaar", "shopkeeper"), ("पुरानी", "puraanee", "old (f.)"),
            ]),
        ],
        sentences=[
            ("गुरु पाठशाला में हैं।", "guru paathshaalaa mein hain.", "The teacher is in the school."),
            ("सुमन गुलाब ला।", "Suman gulaab laa.", "Suman, bring a rose."),
            ("कछुआ पुल पर है।", "kachhuaa pul par hai.", "The tortoise is on the bridge."),
            ("बुलबुल गा रही है।", "bulbul gaa rahee hai.", "The nightingale is singing."),
            ("अनुज, गुड़ मत खा।", "Anuj, gur mat khaa.", "Anuj, don't eat the jaggery."),
            ("दुकान में साबुन है।", "dukaan mein saabun hai.", "There is soap in the shop."),
            ("सुबह सुबह बुलबुल गाती है।", "subah subah bulbul gaatee hai.", "Early in the morning the nightingale sings."),
            ("हनुमान बहुत बलवान हैं।", "Hanumaan bahut balvaan hain.", "Hanuman is very strong."),
            ("तुम चुप रहना।", "tum chup rahnaa.", "You stay quiet."),
        ],
        passage=("चतुर कछुआ", [
            ("एक पुराना पुल था।", "ek puraanaa pul thaa.", "There was an old bridge."),
            ("पुल के पास एक कछुआ रहता था।", "pul ke paas ek kachhuaa rahtaa thaa.", "Near the bridge lived a tortoise."),
            ("कछुआ बहुत चतुर था।", "kachhuaa bahut chatur thaa.", "The tortoise was very clever."),
            ("सुबह सुबह बुलबुल आती थी।", "subah subah bulbul aatee thee.", "Early every morning a nightingale came."),
            ("बुलबुल मधुर धुन गाती थी।", "bulbul madhur dhun gaatee thee.", "The nightingale sang a sweet tune."),
            ("कछुआ चुप रह कर सुनता था।", "kachhuaa chup rah kar suntaa thaa.", "The tortoise would listen quietly."),
            ("कछुआ खुश था। बुलबुल भी खुश थी।", "kachhuaa khush thaa. bulbul bhee khush thee.", "The tortoise was happy. The nightingale was happy too."),
        ]),
        task="Write कु खु गु … for the chart, and रु separately ten times — it is the odd one out. "
             "Copy the two-letter words; dictation of ten.",
        quiz=[
            ("Where does ु go?", "Underneath the consonant, as a small hook: क → कु."),
            ("How is र + ु written?", "रु — the hook sits in the side of र instead of underneath. As in गुरु."),
            ("Short or long: सुन?", "Short — the u of 'put'. The long oo (ू) is the next lesson."),
        ],
    ),
    # ------------------------------------------------------------ 10
    dict(
        n=10, slug="oo-ki-matra", kind="words", allow={"aa", "i", "ee", "u", "oo"},
        hi="ऊ की मात्रा (ू)", en="The oo matra — ू",
        sub="A bigger hook under the letter, held long: क + ू = कू",
        lede="The long 'oo' of 'boot' is also written underneath, with a fuller curl than the short "
             "one. Again र is the exception: रू with the sign on its side, as in रूप. Compare "
             "सुन (listen) and सूँघ (smell) — same place, different length.",
        sign=("ू", "oo", "क", "कू", "koo"),
        groups=[
            ("दो अक्षर · two letters", [
                ("फूल", "phool", "flower"), ("झूला", "jhoolaa", "swing"), ("चूहा", "choohaa", "mouse"), ("भालू", "bhaaloo", "bear"),
                ("आलू", "aaloo", "potato"), ("जादू", "jaadoo", "magic"), ("दूध", "doodh", "milk"), ("धूप", "dhoop", "sunshine"),
                ("रूई", "rooee", "cotton wool"), ("टूट", "toot", "break"), ("झाड़ू", "jhaaroo", "broom"), ("पूरा", "pooraa", "whole, complete"),
                ("दूर", "door", "far"), ("जूता", "jootaa", "shoe"), ("खून", "khoon", "blood"), ("मूली", "moolee", "radish"),
                ("काजू", "kaajoo", "cashew"), ("भूल", "bhool", "mistake"), ("पूजा", "poojaa", "worship"), ("रूप", "roop", "form, looks"),
                ("धूल", "dhool", "dust"), ("सूखा", "sookhaa", "dry"), ("बूढ़ा", "boorhaa", "old (person)"), ("कूड़ा", "kooraa", "rubbish"),
                ("चाकू", "chaakoo", "knife"), ("डाकू", "daakoo", "bandit"), ("जूस", "joos", "juice"), ("सूप", "soop", "soup"),
            ]),
            ("तीन अक्षर · three letters", [
                ("सूरज", "sooraj", "sun"), ("तरबूज", "tarbooj", "watermelon"), ("कबूतर", "kabootar", "pigeon"), ("नाखून", "naakhoon", "fingernail"),
                ("मजदूर", "majdoor", "labourer"), ("कपूर", "kapoor", "camphor"), ("तराजू", "taraajoo", "weighing scales"), ("समूह", "samooh", "group"),
                ("मयूर", "mayoor", "peacock"), ("तूफान", "toophaan", "storm"), ("खजूर", "khajoor", "date (fruit)"), ("सूअर", "sooar", "pig"),
                ("बबूल", "babool", "acacia tree"), ("पतलून", "patloon", "trousers"), ("कसूर", "kasoor", "fault"), ("जरूर", "jaroor", "certainly"),
            ]),
            ("चार अक्षर · four letters", [
                ("खरबूजा", "kharboojaa", "muskmelon"), ("मजबूत", "majboot", "strong, sturdy"), ("जादूगर", "jaadoogar", "magician"), ("दूरबीन", "doorbeen", "telescope"),
                ("मूलभूत", "moolbhoot", "basic"), ("सूरजमुखी", "soorajmukhee", "sunflower"), ("पूजापाठ", "poojaapaath", "prayers"), ("मूलधन", "mooldhan", "principal (money)"),
            ]),
        ],
        sentences=[
            ("सूरज दूर है।", "sooraj door hai.", "The sun is far away."),
            ("चूहा दूध पी रहा है।", "choohaa doodh pee rahaa hai.", "The mouse is drinking milk."),
            ("भालू झूला झूल रहा है।", "bhaaloo jhoolaa jhool rahaa hai.", "The bear is on the swing."),
            ("माली फूल ला रहा है।", "maalee phool laa rahaa hai.", "The gardener is bringing flowers."),
            ("दादी आलू और मूली ला।", "daadee aaloo aur moolee laa.", "Grandmother, bring potatoes and radish."),
            ("कबूतर दाना चुग रहा है।", "kabootar daanaa chug rahaa hai.", "The pigeon is pecking at grain."),
            ("जूता बाहर रख।", "jootaa baahar rakh.", "Leave the shoes outside."),
            ("पूजा का झाड़ू टूट गया।", "Poojaa kaa jhaaroo toot gayaa.", "Pooja's broom broke."),
            ("धूप में तरबूज मीठा लगता है।", "dhoop mein tarbooj meethaa lagtaa hai.", "Watermelon tastes sweet in the sunshine."),
        ],
        passage=("चूहा और भालू", [
            ("एक चूहा था। एक भालू था।", "ek choohaa thaa. ek bhaaloo thaa.", "There was a mouse. There was a bear."),
            ("भालू बड़ा था।", "bhaaloo baraa thaa.", "The bear was big."),
            ("भालू झूला झूलता था।", "bhaaloo jhoolaa jhoolataa thaa.", "The bear used to play on the swing."),
            ("चूहा दूध पीता था।", "choohaa doodh peetaa thaa.", "The mouse used to drink milk."),
            ("एक दिन झूला टूट गया।", "ek din jhoolaa toot gayaa.", "One day the swing broke."),
            ("चूहा दूर से भागा आया।", "choohaa door se bhaagaa aayaa.", "The mouse came running from far away."),
            ("चूहा आया, भालू उठा। भालू खुश हुआ।", "choohaa aayaa, bhaaloo uthaa. bhaaloo khush huaa.", "The mouse came, the bear got up. The bear was happy."),
            ("सूरज डूबा। सब घर गए।", "sooraj doobaa. sab ghar gaye.", "The sun set. Everyone went home."),
        ]),
        task="Write pairs: सुन / सून, कुल / कूल, पुल / फूल — and feel the length. Then copy the "
             "two-letter words and take dictation of ten.",
        quiz=[
            ("How do ु and ू differ on the page?", "Both hang under the letter; ू has the fuller, longer curl. Sound: short 'put' vs long 'boot'."),
            ("How is र + ू written?", "रू, with the sign at the side — as in रूप, रूई."),
            ("Read झाड़ू.", "झा-ड़ू — jhaaroo, broom. The ड़ has a dot: a flapped r."),
        ],
    ),
    # ------------------------------------------------------------ 11
    dict(
        n=11, slug="e-ki-matra", kind="words", allow={"aa", "i", "ee", "u", "oo", "e"},
        hi="ए की मात्रा (े)", en="The e matra — े",
        sub="A small stroke on top of the headline: क + े = के",
        lede="Now the signs climb on top. The 'e' of 'gate' (without the English glide) is one "
             "short slanted stroke above the headline, over the right side of the letter. It is "
             "everywhere in Hindi — के, से, ने, मेरे — so your reading speed jumps after this lesson.",
        sign=("े", "e", "क", "के", "ke"),
        groups=[
            ("दो अक्षर · two letters", [
                ("केला", "kelaa", "banana"), ("मेला", "melaa", "fair"), ("खेल", "khel", "game"), ("खेत", "khet", "field"),
                ("शेर", "sher", "lion"), ("मेज", "mej", "table"), ("बेटा", "betaa", "son"), ("बेटी", "betee", "daughter"),
                ("सेब", "seb", "apple"), ("रेल", "rel", "train"), ("पेड़", "per", "tree"), ("तेल", "tel", "oil"),
                ("देश", "desh", "country"), ("देर", "der", "delay"), ("रेत", "ret", "sand"), ("ढेर", "dher", "heap"),
                ("नेता", "netaa", "leader"), ("सेना", "senaa", "army"), ("भेड़", "bher", "sheep"), ("बेर", "ber", "berry"),
                ("जेब", "jeb", "pocket"), ("देखा", "dekhaa", "saw"), ("मेरा", "meraa", "my"), ("तेरा", "teraa", "your"),
            ]),
            ("तीन अक्षर · three letters", [
                ("सवेरा", "saveraa", "morning"), ("ठेला", "thelaa", "handcart"), ("सपेरा", "saperaa", "snake charmer"), ("केसर", "kesar", "saffron"),
                ("बेसन", "besan", "gram flour"), ("सहेली", "sahelee", "friend (girl)"), ("चमेली", "chamelee", "jasmine"), ("पहेली", "pahelee", "riddle"),
                ("लेखक", "lekhak", "writer"), ("केवल", "keval", "only"), ("हमेशा", "hameshaa", "always"), ("मेहनत", "mehnat", "hard work"),
                ("जलेबी", "jalebee", "jalebi"), ("अनेक", "anek", "many"), ("बसेरा", "baseraa", "nest, shelter"), ("विदेश", "videsh", "abroad"),
                ("पहले", "pahle", "first, before"), ("कपड़े", "kapre", "clothes"), ("सेवक", "sevak", "servant"), ("उधेड़", "udher", "unpick"),
            ]),
            ("चार अक्षर · four letters", [
                ("मेहमान", "mehmaan", "guest"), ("रेलगाड़ी", "relgaaree", "train"), ("बेचारा", "bechaaraa", "poor thing"), ("बेकार", "bekaar", "useless"),
                ("केदारनाथ", "Kedaarnaath", "Kedarnath"), ("मेहनती", "mehnatee", "hard-working"), ("देहरादून", "Dehraadoon", "Dehradun"), ("खेलकूद", "khelkood", "sports"),
            ]),
        ],
        sentences=[
            ("शेर खेत में है।", "sher khet mein hai.", "The lion is in the field."),
            ("बेटा मेले में खेल रहा है।", "betaa mele mein khel rahaa hai.", "The son is playing at the fair."),
            ("मेज पर सेब और केला है।", "mej par seb aur kelaa hai.", "On the table are an apple and a banana."),
            ("रेल देर से आई।", "rel der se aaee.", "The train came late."),
            ("पेड़ पर बेर हैं।", "per par ber hain.", "There are berries on the tree."),
            ("सहेली ने पहेली कही।", "sahelee ne pahelee kahee.", "The friend told a riddle."),
            ("देश की सेना मेहनत करती है।", "desh kee senaa mehnat kartee hai.", "The country's army works hard."),
            ("मेरा बेटा केवल जलेबी खाता है।", "meraa betaa keval jalebee khaataa hai.", "My son eats only jalebi."),
            ("सवेरे मेहमान आए।", "savere mehmaan aaye.", "Guests came in the morning."),
        ],
        passage=("मेले में", [
            ("आज मेले का दिन है।", "aaj mele kaa din hai.", "Today is the day of the fair."),
            ("बेटा और बेटी मेले में गए।", "betaa aur betee mele mein gaye.", "The son and daughter went to the fair."),
            ("एक ठेला था। ठेले पर केले और सेब थे।", "ek thelaa thaa. thele par kele aur seb the.", "There was a cart. On the cart were bananas and apples."),
            ("एक सपेरा बीन बजा रहा था।", "ek saperaa been bajaa rahaa thaa.", "A snake charmer was playing his pipe."),
            ("बेटी ने जलेबी खाई। बेटे ने बेर।", "betee ne jalebee khaaee. bete ne ber.", "The daughter ate jalebi. The son, berries."),
            ("देर हुई। रेल का समय था।", "der huee. rel kaa samay thaa.", "It got late. It was time for the train."),
            ("बेटा और बेटी पेड़ के पास से घर आए।", "betaa aur betee per ke paas se ghar aaye.", "The son and daughter came home past the tree."),
        ]),
        task="Write के खे गे … for the chart. Then write the little words के, से, ने, मेरे, तेरे "
             "ten times each — you have earned them now. Dictation of ten words.",
        quiz=[
            ("Where does े sit?", "On top, above the headline, as one slanted stroke over the right of the letter."),
            ("Is the e in केला like English 'kay'?", "Shorter and purer — no glide at the end. Hold your mouth still."),
            ("Read मेहनत.", "मे-ह-न-त — mehnat, hard work. Only the first letter wears a sign."),
        ],
    ),
    # ------------------------------------------------------------ 12
    dict(
        n=12, slug="ai-ki-matra", kind="words", allow={"aa", "i", "ee", "u", "oo", "e", "ai"},
        hi="ऐ की मात्रा (ै)", en="The ai matra — ै",
        sub="Two strokes on top: क + ै = कै",
        lede="Double the stroke, change the vowel. Two slanted marks above the headline give the "
             "'ai' sound — in most of north India it is the a of 'cat', held. You already know "
             "the most important ै word in Hindi: है.",
        sign=("ै", "ai", "क", "कै", "kai"),
        groups=[
            ("दो अक्षर · two letters", [
                ("पैसा", "paisaa", "money"), ("बैल", "bail", "ox"), ("कैसा", "kaisaa", "how (is it)"), ("मैना", "mainaa", "myna bird"),
                ("थैला", "thailaa", "bag"), ("जैसा", "jaisaa", "like, as"), ("वैसा", "vaisaa", "like that"), ("बैठ", "baith", "sit"),
                ("सैर", "sair", "a walk, outing"), ("नैया", "naiyaa", "boat"), ("गैस", "gais", "gas"), ("भैया", "bhaiyaa", "brother"),
                ("फैल", "phail", "spread"), ("मैला", "mailaa", "dirty"), ("चैन", "chain", "peace, calm"), ("पैर", "pair", "foot"),
                ("मैच", "maich", "match (sport)"), ("खैर", "khair", "well, anyway"), ("कैद", "kaid", "imprisonment"), ("तैर", "tair", "swim"),
            ]),
            ("तीन अक्षर · three letters", [
                ("मैदान", "maidaan", "ground, field"), ("तैयार", "taiyaar", "ready"), ("कैदी", "kaidee", "prisoner"), ("शैतान", "shaitaan", "devil; mischief"),
                ("हैरान", "hairaan", "surprised"), ("सैनिक", "sainik", "soldier"), ("पैदल", "paidal", "on foot"), ("जैतून", "jaitoon", "olive"),
                ("दैनिक", "dainik", "daily"), ("रैली", "railee", "rally"), ("बैसाखी", "Baisaakhee", "Baisakhi"), ("सैलाब", "sailaab", "flood"),
                ("तैराक", "tairaak", "swimmer"), ("वैशाली", "Vaishaalee", "a name"), ("पैमाना", "paimaanaa", "measure, scale"), ("बैठक", "baithak", "meeting; sitting room"),
            ]),
            ("चार अक्षर · four letters", [
                ("तैयारी", "taiyaaree", "preparation"), ("हैदराबाद", "Haidaraabaad", "Hyderabad"), ("मैदानी", "maidaanee", "of the plains"), ("पैदाइश", "paidaaish", "birth"),
                ("कैलाश", "Kailaash", "Kailash"), ("नैनीताल", "Naineetaal", "Nainital"), ("बैलगाड़ी", "bailgaaree", "bullock cart"), ("सैलानी", "sailaanee", "tourist"),
            ]),
        ],
        sentences=[
            ("बैल मैदान में बैठा है।", "bail maidaan mein baithaa hai.", "The ox is sitting in the field."),
            ("भैया पैदल सैर पर गए।", "bhaiyaa paidal sair par gaye.", "Brother went for a walk on foot."),
            ("मैना पेड़ पर है।", "mainaa per par hai.", "The myna is on the tree."),
            ("थैले में पैसे हैं।", "thaile mein paise hain.", "There is money in the bag."),
            ("सैनिक तैयार हैं।", "sainik taiyaar hain.", "The soldiers are ready."),
            ("कैसा है, भैया? — ठीक है।", "kaisaa hai, bhaiyaa? — theek hai.", "How are you, brother? — Fine."),
            ("मैदान में मैच है।", "maidaan mein maich hai.", "There is a match on the ground."),
            ("बैलगाड़ी धीरे चलती है।", "bailgaaree dheere chaltee hai.", "The bullock cart goes slowly."),
            ("पैर साफ कर के बैठ।", "pair saaph kar ke baith.", "Clean your feet and sit."),
        ],
        passage=("भैया की सैर", [
            ("सवेरा है। भैया सैर पर निकले।", "saveraa hai. bhaiyaa sair par nikle.", "It is morning. Brother went out for a walk."),
            ("वे पैदल मैदान तक गए।", "ve paidal maidaan tak gaye.", "He walked as far as the field."),
            ("मैदान में बैल बैठे थे।", "maidaan mein bail baithe the.", "Oxen were sitting in the field."),
            ("पेड़ पर मैना गा रही थी।", "per par mainaa gaa rahee thee.", "A myna was singing on the tree."),
            ("कुछ सैनिक कसरत कर रहे थे।", "kuchh sainik kasrat kar rahe the.", "Some soldiers were exercising."),
            ("भैया हैरान थे — कैसा सवेरा!", "bhaiyaa hairaan the — kaisaa saveraa!", "Brother was amazed — what a morning!"),
            ("थैले में पैसे थे। वे जलेबी ले आए।", "thaile mein paise the. ve jalebee le aaye.", "There was money in the bag. He brought back jalebi."),
        ]),
        task="Write के / कै, मे / मै, बे / बै side by side — one stroke, two strokes. Say them. Then "
             "write है twenty times, the most-used word in the language. Dictation of ten.",
        quiz=[
            ("How is ै different from े?", "Two slanted strokes on top instead of one. e → ai."),
            ("What does है sound like?", "'hai' — the a of 'cat', held. The commonest word in Hindi: 'is'."),
            ("Read तैयार.", "तै-या-र — taiyaar, ready."),
        ],
    ),
    # ------------------------------------------------------------ 13
    dict(
        n=13, slug="o-ki-matra", kind="words", allow={"aa", "i", "ee", "u", "oo", "e", "ai", "o"},
        hi="ओ की मात्रा (ो)", en="The o matra — ो",
        sub="The aa stroke plus one stroke on top: क + ो = को",
        lede="Look closely: ो is the ा stroke you already know, with the े stroke added on top of "
             "it. Two old friends make a new sound — the 'o' of 'go', with no glide. Hindi's "
             "little postposition को is written with it, and so are मोर, रोटी and होली.",
        sign=("ो", "o", "क", "को", "ko"),
        groups=[
            ("दो अक्षर · two letters", [
                ("मोर", "mor", "peacock"), ("ढोल", "dhol", "drum"), ("घोड़ा", "ghoraa", "horse"), ("लोटा", "lotaa", "small metal pot"),
                ("टोपी", "topee", "cap"), ("मोती", "motee", "pearl"), ("रोटी", "rotee", "flatbread"), ("बोल", "bol", "speak"),
                ("तोता", "totaa", "parrot"), ("गोभी", "gobhee", "cauliflower"), ("मोटा", "motaa", "fat"), ("छोटा", "chhotaa", "small"),
                ("कोना", "konaa", "corner"), ("सोना", "sonaa", "gold; to sleep"), ("धोबी", "dhobee", "washerman"), ("होली", "Holee", "Holi"),
                ("चोर", "chor", "thief"), ("शोर", "shor", "noise"), ("रोज", "roj", "every day"), ("खोल", "khol", "open"),
                ("दो", "do", "two"), ("सो", "so", "sleep"), ("रो", "ro", "cry"), ("धो", "dho", "wash"),
                ("लोग", "log", "people"), ("योग", "yog", "yoga"), ("भोर", "bhor", "dawn"), ("ओस", "os", "dew"),
            ]),
            ("तीन अक्षर · three letters", [
                ("कोयल", "koyal", "cuckoo"), ("खरगोश", "khargosh", "rabbit"), ("समोसा", "samosaa", "samosa"), ("लोमड़ी", "lomree", "fox"),
                ("भोजन", "bhojan", "meal"), ("कटोरी", "katoree", "small bowl"), ("बोतल", "botal", "bottle"), ("रसोई", "rasoee", "kitchen"),
                ("ढोलक", "dholak", "dholak drum"), ("कोयला", "koylaa", "coal"), ("सोमवार", "somvaar", "Monday"), ("मोहन", "Mohan", "a name"),
                ("गोपाल", "Gopaal", "a name"), ("टोकरी", "tokree", "basket"), ("अनमोल", "anmol", "priceless"), ("डोली", "dolee", "palanquin"),
                ("ओखली", "okhlee", "mortar"), ("बोली", "bolee", "speech, dialect"), ("गोदाम", "godaam", "warehouse"), ("खिलोना", "khilonaa", "toy (also खिलौना)"),
            ]),
            ("चार अक्षर · four letters", [
                ("सोमनाथ", "Somnaath", "Somnath"), ("कोलकाता", "Kolkaataa", "Kolkata"), ("मोटरगाड़ी", "motargaaree", "motor car"), ("दोपहर", "dopahar", "afternoon"),
                ("गोदावरी", "Godaavaree", "the Godavari river"), ("रोजगार", "rojgaar", "employment"), ("तोतापरी", "totaaparee", "a kind of mango"), ("मनोहर", "manohar", "charming; a name"),
            ]),
        ],
        sentences=[
            ("मोर नाच रहा है।", "mor naach rahaa hai.", "The peacock is dancing."),
            ("तोता रोटी खा रहा है।", "totaa rotee khaa rahaa hai.", "The parrot is eating roti."),
            ("घोड़ा सड़क पर भाग रहा है।", "ghoraa sarak par bhaag rahaa hai.", "The horse is running on the road."),
            ("कोयल मीठा बोलती है।", "koyal meethaa boltee hai.", "The cuckoo sings sweetly."),
            ("टोकरी में समोसे और गोभी हैं।", "tokree mein samose aur gobhee hain.", "In the basket are samosas and cauliflower."),
            ("सोमवार को होली है।", "somvaar ko Holee hai.", "Holi is on Monday."),
            ("मोहन सो रहा है।", "Mohan so rahaa hai.", "Mohan is sleeping."),
            ("धोबी कपड़े धो रहा है।", "dhobee kapre dho rahaa hai.", "The washerman is washing clothes."),
            ("रसोई में शोर मत करो।", "rasoee mein shor mat karo.", "Don't make noise in the kitchen."),
        ],
        passage=("होली का दिन", [
            ("आज होली है।", "aaj Holee hai.", "Today is Holi."),
            ("भोर से ही ढोल बज रहा है।", "bhor se hee dhol baj rahaa hai.", "Since dawn the drum has been beating."),
            ("मोहन और गोपाल गुलाल ले आए।", "Mohan aur Gopaal gulaal le aaye.", "Mohan and Gopal brought gulal (coloured powder)."),
            ("लोग गा रहे हैं, नाच रहे हैं।", "log gaa rahe hain, naach rahe hain.", "People are singing and dancing."),
            ("रसोई से समोसे की खुशबू आ रही है।", "rasoee se samose kee khushboo aa rahee hai.", "The smell of samosas is coming from the kitchen."),
            ("तोता भी बोल रहा है — होली है!", "totaa bhee bol rahaa hai — Holee hai!", "Even the parrot is saying — it's Holi!"),
            ("दोपहर को सब सो गए।", "dopahar ko sab so gaye.", "In the afternoon everyone slept."),
        ]),
        task="Write का / को, मा / मो, सा / सो — add the top stroke and hear the vowel change. Then "
             "write को, दो, सो, रो, धो, खो, बो — the one-letter words — and dictation of ten.",
        quiz=[
            ("What is ो made of?", "The ा stroke with a े stroke on top: two signs you already know, one new vowel."),
            ("Read रोटी.", "रो-टी — rotee, flatbread. One sign on top, one on the right."),
            ("What is the difference between दो and धो?", "दो (do) is 'two'; धो (dho) is 'wash' — the breathy ध, not the plain द."),
        ],
    ),
    # ------------------------------------------------------------ 14
    dict(
        n=14, slug="au-ki-matra", kind="words", allow={"aa", "i", "ee", "u", "oo", "e", "ai", "o", "au"},
        hi="औ की मात्रा (ौ)", en="The au matra — ौ",
        sub="The aa stroke plus two strokes on top: क + ौ = कौ",
        lede="The last of the vowel signs follows the same logic: ा plus two top strokes. The "
             "sound is the 'o' of 'hot', held long. It gives you the word you have been using "
             "since lesson 5 — और (and) — plus कौन, मौसम and खिलौना.",
        sign=("ौ", "au", "क", "कौ", "kau"),
        groups=[
            ("दो अक्षर · two letters", [
                ("कौआ", "kauaa", "crow"), ("नौका", "naukaa", "boat"), ("पौधा", "paudhaa", "plant"), ("चौक", "chauk", "town square"),
                ("लौकी", "laukee", "bottle gourd"), ("दौड़", "daur", "run"), ("मौसी", "mausee", "aunt (mother's sister)"), ("फौज", "phauj", "army"),
                ("बौना", "baunaa", "dwarf"), ("सौ", "sau", "hundred"), ("नौ", "nau", "nine"), ("मौका", "maukaa", "chance"),
                ("लौट", "laut", "return"), ("सौदा", "saudaa", "deal, purchase"), ("कौन", "kaun", "who"), ("और", "aur", "and"),
                ("चौड़ा", "chauraa", "wide"), ("मौन", "maun", "silence"), ("दौर", "daur", "era, round"), ("गौर", "gaur", "attention"),
            ]),
            ("तीन अक्षर · three letters", [
                ("औरत", "aurat", "woman"), ("मौसम", "mausam", "weather"), ("हथौड़ा", "hathauraa", "hammer"), ("कचौड़ी", "kachauree", "kachori"),
                ("खिलौना", "khilaunaa", "toy"), ("दौलत", "daulat", "wealth"), ("पकौड़ा", "pakauraa", "fritter"), ("गौरव", "gaurav", "pride"),
                ("औजार", "aujaar", "tool"), ("तौलिया", "tauliyaa", "towel"), ("नौकर", "naukar", "servant"), ("बिछौना", "bichhaunaa", "bedding"),
                ("चौकी", "chaukee", "low stool; police post"), ("भौजाई", "bhaujaaee", "brother's wife"), ("दौड़ना", "dauranaa", "to run"), ("सौरभ", "Saurabh", "a name"),
            ]),
            ("चार अक्षर · four letters", [
                ("चौकीदार", "chaukeedaar", "watchman"), ("चौराहा", "chauraahaa", "crossroads"), ("मौसमी", "mausamee", "sweet lime; seasonal"), ("नौकरानी", "naukaraanee", "maid"),
                ("औषधालय", "aushadhaalay", "dispensary"), ("कौशल", "kaushal", "skill"), ("सौतेला", "sautelaa", "step- (brother etc.)"), ("दौड़धूप", "daurdhoop", "running around"),
            ]),
        ],
        sentences=[
            ("कौआ पौधे पर बैठा है।", "kauaa paudhe par baithaa hai.", "The crow is sitting on the plant."),
            ("मौसी कचौड़ी और पकौड़े बना रही हैं।", "mausee kachauree aur pakaure banaa rahee hain.", "Aunt is making kachori and pakoras."),
            ("चौकीदार रात भर जागता है।", "chaukeedaar raat bhar jaagtaa hai.", "The watchman stays awake all night."),
            ("नौका पानी में दौड़ रही है।", "naukaa paanee mein daur rahee hai.", "The boat is racing on the water."),
            ("यह खिलौना कौन लाया?", "yah khilaunaa kaun laayaa?", "Who brought this toy?"),
            ("सौ में से नौ कम करो।", "sau mein se nau kam karo.", "Take nine away from a hundred."),
            ("मौसम सुहाना है।", "mausam suhaanaa hai.", "The weather is lovely."),
            ("चौराहे पर मत दौड़ो।", "chauraahe par mat dauro.", "Don't run at the crossroads."),
            ("औरत हथौड़ा और औजार लाई।", "aurat hathauraa aur aujaar laaee.", "The woman brought a hammer and tools."),
        ],
        passage=("कौआ और लौकी", [
            ("एक कौआ था। वह बहुत चतुर था।", "ek kauaa thaa. vah bahut chatur thaa.", "There was a crow. He was very clever."),
            ("चौक के पास एक पौधा था।", "chauk ke paas ek paudhaa thaa.", "Near the square there was a plant."),
            ("पौधे पर एक लौकी थी।", "paudhe par ek laukee thee.", "On the plant was a bottle gourd."),
            ("कौआ रोज लौकी को देखता था।", "kauaa roj laukee ko dekhtaa thaa.", "Every day the crow looked at the gourd."),
            ("एक दिन मौसी आई। उसने लौकी तोड़ी।", "ek din mausee aaee. usne laukee toree.", "One day aunt came. She picked the gourd."),
            ("कौआ दौड़ा, पर देर हो गई।", "kauaa dauraa, par der ho gaee.", "The crow ran, but it was too late."),
            ("मौसी ने कौए को पकौड़ा दिया। कौआ खुश।", "mausee ne kaue ko pakauraa diyaa. kauaa khush.", "Aunt gave the crow a pakora. Happy crow."),
        ]),
        task="Write को / कौ, मो / मौ, सो / सौ — one top stroke, then two. Now write the whole "
             "बारहखड़ी of क: क का कि की कु कू के कै को कौ कं कः — you own all twelve.",
        quiz=[
            ("What is ौ made of?", "The ा stroke with two strokes on top — like ो but doubled, as ै is to े."),
            ("Read खिलौना.", "खि-लौ-ना — khilaunaa, toy. Three signs in one word: ि, ौ, ा."),
            ("What does कौन mean?", "'Who'. कौन आया? — who came?"),
        ],
    ),
    # ------------------------------------------------------------ 15
    dict(
        n=15, slug="anusvar-visarg-chandrabindu", kind="words",
        allow={"aa", "i", "ee", "u", "oo", "e", "ai", "o", "au", "an", "ah", "chandra"},
        hi="अं, अः और चंद्रबिंदु (ं ः ँ)", en="The dot, the two dots and the moon-dot",
        sub="अनुस्वार ं · विसर्ग ः · चंद्रबिंदु ँ",
        lede="Three small marks finish the system. The dot on top (अनुस्वार) adds a nasal hum — "
             "रंग, अंगूर. The moon-with-a-dot (चंद्रबिंदु) makes the vowel itself nasal — माँ, "
             "चाँद, गाँव. The two dots after a letter (विसर्ग) add a breath and live mostly in "
             "words from Sanskrit — नमः, दुःख.",
        sign=("ं", "an", "क", "कं", "kan"),
        groups=[
            ("अनुस्वार ं · the dot", [
                ("अंगूर", "angoor", "grapes"), ("अंडा", "andaa", "egg"), ("कंघी", "kanghee", "comb"), ("पतंग", "patang", "kite"),
                ("रंग", "rang", "colour"), ("संतरा", "santaraa", "orange"), ("बंदर", "bandar", "monkey"), ("जंगल", "jangal", "jungle"),
                ("घंटा", "ghantaa", "bell; hour"), ("पंखा", "pankhaa", "fan"), ("लंबा", "lambaa", "tall, long"), ("ठंडा", "thandaa", "cold"),
                ("गंगा", "Gangaa", "the Ganga"), ("मंदिर", "mandir", "temple"), ("कंबल", "kambal", "blanket"), ("बंद", "band", "closed"),
                ("अंक", "ank", "number, digit"), ("इंजन", "injan", "engine"), ("पंख", "pankh", "wing"), ("सुंदर", "sundar", "beautiful"),
                ("हंस", "hans", "swan"), ("शंख", "shankh", "conch"), ("बसंत", "basant", "spring"), ("आनंद", "aanand", "joy"),
                ("पसंद", "pasand", "liking"), ("चंदन", "chandan", "sandalwood"), ("गेंद", "gend", "ball"), ("कैंची", "kainchee", "scissors"),
                ("भैंस", "bhains", "buffalo"), ("घोंसला", "ghonslaa", "nest"), ("भौंरा", "bhaunraa", "bumblebee"), ("मैं", "main", "I"),
            ]),
            ("चंद्रबिंदु ँ · the moon-dot", [
                ("माँ", "maan", "mother"), ("चाँद", "chaand", "moon"), ("गाँव", "gaanv", "village"), ("साँप", "saanp", "snake"),
                ("दाँत", "daant", "tooth"), ("हँस", "hans", "laugh"), ("ऊँट", "oont", "camel"), ("पाँच", "paanch", "five"),
                ("आँख", "aankh", "eye"), ("बाँसुरी", "baansuree", "flute"), ("कुआँ", "kuaan", "well"), ("धुआँ", "dhuaan", "smoke"),
                ("हाँ", "haan", "yes"), ("कहाँ", "kahaan", "where"), ("यहाँ", "yahaan", "here"), ("वहाँ", "vahaan", "there"),
                ("पूँछ", "poonchh", "tail"), ("मुँह", "munh", "mouth"), ("साँस", "saans", "breath"), ("काँच", "kaanch", "glass (material)"),
            ]),
            ("विसर्ग ः · the two dots", [
                ("नमः", "namah", "a bow, salutation"), ("दुःख", "duhkh", "sorrow"), ("अतः", "atah", "therefore"), ("छः", "chhah", "six"),
                ("पुनः", "punah", "again"), ("अंततः", "antatah", "finally"), ("शनैः", "shanaih", "slowly"),
            ]),
        ],
        sentences=[
            ("बंदर जंगल में है।", "bandar jangal mein hai.", "The monkey is in the jungle."),
            ("माँ ने संतरा और अंगूर दिए।", "maan ne santaraa aur angoor diye.", "Mother gave oranges and grapes."),
            ("पतंग का रंग लाल है।", "patang kaa rang laal hai.", "The kite's colour is red."),
            ("गाँव में एक मंदिर है।", "gaanv mein ek mandir hai.", "In the village there is a temple."),
            ("ऊँट लंबा होता है।", "oont lambaa hotaa hai.", "A camel is tall."),
            ("साँप को देख कर हंस उड़ गया।", "saanp ko dekh kar hans ur gayaa.", "Seeing the snake, the swan flew away."),
            ("पाँच और पाँच दस।", "paanch aur paanch das.", "Five and five, ten."),
            ("चाँद सुंदर है।", "chaand sundar hai.", "The moon is beautiful."),
            ("मैं यहाँ हूँ, तुम कहाँ हो?", "main yahaan hoon, tum kahaan ho?", "I am here, where are you?"),
        ],
        passage=("गाँव की रात", [
            ("यह मेरा गाँव है।", "yah meraa gaanv hai.", "This is my village."),
            ("गाँव में एक मंदिर है और एक कुआँ।", "gaanv mein ek mandir hai aur ek kuaan.", "In the village there is a temple and a well."),
            ("रात को चाँद निकला।", "raat ko chaand niklaa.", "At night the moon came out."),
            ("बंदर पेड़ पर सो गए।", "bandar per par so gaye.", "The monkeys slept in the tree."),
            ("माँ ने ठंडा कंबल दिया।", "maan ne thandaa kambal diyaa.", "Mother gave a cool blanket."),
            ("दूर से बाँसुरी की धुन आ रही थी।", "door se baansuree kee dhun aa rahee thee.", "From far away came the tune of a flute."),
            ("मैं हँस कर सो गया। आनंद ही आनंद।", "main hans kar so gayaa. aanand hee aanand.", "I laughed and fell asleep. Pure joy."),
        ]),
        task="Write अं, कं, खं … once across the chart, then माँ चाँद गाँव साँप दाँत हँस ten times. "
             "Finally the word मैं — I — twenty times. You will write it more than any other.",
        quiz=[
            ("What does the dot on रंग do?", "Adds a nasal hum before the next consonant — 'rang', like the ng in 'sing'."),
            ("When is ँ used instead of ं?", "When the vowel itself is nasal — माँ, चाँद, गाँव. If a top matra is already there (े ै ो ौ), the plain dot is written instead: मैं, हैं."),
            ("Where do you meet ः?", "Mostly in Sanskrit-derived words and set phrases: नमः, दुःख, अतः, छः."),
        ],
    ),
    # ------------------------------------------------------------ 16
    dict(
        n=16, slug="ri-ki-matra", kind="words",
        allow={"aa", "i", "ee", "u", "oo", "e", "ai", "o", "au", "an", "ah", "chandra", "ri"},
        hi="ऋ की मात्रा (ृ)", en="The ri matra — ृ",
        sub="A small curl under the letter: क + ृ = कृ",
        lede="The thirteenth sign belongs to the vowel ऋ — said 'ri' in modern Hindi. It is a "
             "small curl beneath the consonant and it lives in a particular set of words, most "
             "of them from Sanskrit: कृपा, ऋषि, मृग, अमृत. Few words, but you meet them often.",
        sign=("ृ", "ri", "क", "कृ", "kri"),
        groups=[
            ("शब्द · words", [
                ("ऋषि", "rishi", "sage"), ("ऋतु", "ritu", "season"), ("ऋण", "rin", "debt"), ("कृपा", "kripaa", "kindness, grace"),
                ("कृषक", "krishak", "farmer"), ("मृग", "mrig", "deer"), ("गृह", "grih", "house"), ("तृण", "trin", "blade of grass"),
                ("घृणा", "ghrinaa", "hatred"), ("अमृत", "amrit", "nectar"), ("हृदय", "hriday", "heart"), ("मृदु", "mridu", "soft, gentle"),
                ("कृति", "kriti", "a work (of art)"), ("सृजन", "srijan", "creation"), ("दृढ़", "drirh", "firm"), ("नृप", "nrip", "king"),
                ("ऋषभ", "Rishabh", "a name"), ("कृपया", "kripayaa", "please"), ("मृदंग", "mridang", "a drum"), ("गृहिणी", "grihinee", "housewife"),
                ("मातृभाषा", "maatribhaashaa", "mother tongue"), ("पितृ", "pitri", "father- (in compounds)"), ("वृषभ", "vrishabh", "bull"), ("भृकुटी", "bhrikutee", "eyebrow"),
            ]),
        ],
        sentences=[
            ("ऋषि वन में रहते हैं।", "rishi van mein rahte hain.", "The sage lives in the forest."),
            ("कृपया चुप रहो।", "kripayaa chup raho.", "Please be quiet."),
            ("मृग तृण खाता है।", "mrig trin khaataa hai.", "The deer eats grass."),
            ("ऋतु बदल गई।", "ritu badal gaee.", "The season changed."),
            ("कृषक खेत में हल चला रहा है।", "krishak khet mein hal chalaa rahaa hai.", "The farmer is ploughing the field."),
            ("माँ का हृदय कोमल है।", "maan kaa hriday komal hai.", "A mother's heart is tender."),
            ("अमृत मीठा होता है।", "amrit meethaa hotaa hai.", "Nectar is sweet."),
            ("हिंदी मेरी मातृभाषा है।", "Hindee meree maatribhaashaa hai.", "Hindi is my mother tongue."),
        ],
        passage=("ऋषि और मृग", [
            ("वन में एक ऋषि रहते थे।", "van mein ek rishi rahte the.", "In the forest lived a sage."),
            ("उनका गृह छोटा था, हृदय बड़ा।", "unkaa grih chhotaa thaa, hriday baraa.", "His house was small, his heart big."),
            ("एक दिन एक मृग आया।", "ek din ek mrig aayaa.", "One day a deer came."),
            ("ऋषि ने उसे तृण और जल दिया।", "rishi ne use trin aur jal diyaa.", "The sage gave it grass and water."),
            ("मृग रोज आने लगा।", "mrig roj aane lagaa.", "The deer began to come every day."),
            ("ऋतु बदली, पर मृग आता रहा।", "ritu badlee, par mrig aataa rahaa.", "The seasons changed, but the deer kept coming."),
            ("कृपा का फल अमृत जैसा मीठा होता है।", "kripaa kaa phal amrit jaisaa meethaa hotaa hai.", "The fruit of kindness is as sweet as nectar."),
        ]),
        task="Write कृ, गृ, तृ, मृ, हृ ten times each — the curl must sit under the letter, not "
             "beside it. Then write कृपया on a card and put it on your desk.",
        quiz=[
            ("How is ऋ pronounced in Hindi?", "'ri' — ऋषि is rishi, कृपा is kripaa. (Sanskrit scholars say it differently; Hindi does not.)"),
            ("Where does ृ go?", "Underneath the consonant, as a small curl — like ु but curling the other way."),
            ("Read मातृभाषा.", "मा-तृ-भा-षा — maatribhaashaa, mother tongue."),
        ],
    ),
    # ------------------------------------------------------------ 17
    dict(
        n=17, slug="sanyukt-akshar", kind="words",
        allow={"aa", "i", "ee", "u", "oo", "e", "ai", "o", "au", "an", "ah", "chandra", "ri", "halant"},
        hi="आधे अक्षर और संयुक्त अक्षर", en="Half letters and joined letters",
        sub="हलंत ् · क्ष त्र ज्ञ श्र · र के तीन रूप",
        lede="Every consonant carries an 'a'. To silence it you add a small slash underneath — the "
             "हलंत (्) — and the letter becomes 'half': it loses its vertical stem and leans on "
             "the next one. क + ् + ष = क्ष. Once you can see the half letter inside a cluster, "
             "the last locked door of Devanagari opens: बच्चा, स्कूल, प्रकाश, कर्म.",
        sign=("्", "halant", "क", "क्", "k"),
        groups=[
            ("एक ही अक्षर दो बार · doubled letters", [
                ("बच्चा", "bachchaa", "child"), ("सच्चा", "sachchaa", "true"), ("पत्ता", "pattaa", "leaf"), ("मक्का", "makkaa", "maize"),
                ("डिब्बा", "dibbaa", "box"), ("लट्टू", "lattoo", "spinning top"), ("अन्न", "ann", "grain"), ("चम्मच", "chammach", "spoon"),
                ("बिल्ली", "billee", "cat"), ("गुब्बारा", "gubbaaraa", "balloon"), ("कुत्ता", "kuttaa", "dog"), ("पक्का", "pakkaa", "firm, ripe"),
            ]),
            ("क्ष त्र ज्ञ श्र · the four classics", [
                ("कक्षा", "kakshaa", "class"), ("शिक्षा", "shikshaa", "education"), ("क्षमा", "kshamaa", "forgiveness"), ("पक्षी", "pakshee", "bird"),
                ("पत्र", "patra", "letter"), ("मित्र", "mitra", "friend"), ("पुत्र", "putra", "son"), ("चित्र", "chitra", "picture"),
                ("ज्ञान", "gyaan", "knowledge"), ("विज्ञान", "vigyaan", "science"), ("यज्ञ", "yagya", "fire ritual"), ("आज्ञा", "aagyaa", "permission"),
                ("श्रम", "shram", "labour"), ("श्रीमान", "shreemaan", "Mr"), ("विश्राम", "vishraam", "rest"), ("श्रीमती", "shreematee", "Mrs"),
            ]),
            ("स और अन्य आधे अक्षर · other half letters", [
                ("स्कूल", "skool", "school"), ("स्वर", "svar", "vowel"), ("व्यंजन", "vyanjan", "consonant"), ("शब्द", "shabd", "word"),
                ("वाक्य", "vaakya", "sentence"), ("विद्या", "vidyaa", "learning"), ("विद्यालय", "vidyaalay", "school"), ("बस्ता", "bastaa", "school bag"),
                ("हिम्मत", "himmat", "courage"), ("नन्हा", "nanhaa", "tiny"), ("कन्या", "kanyaa", "girl"), ("अच्छा", "achchhaa", "good"),
                ("सब्जी", "sabjee", "vegetable"), ("नृत्य", "nritya", "dance"), ("कृष्ण", "Krishna", "Krishna"), ("पृथ्वी", "prithvee", "earth"),
            ]),
            ("र के तीन रूप · the three shapes of र", [
                ("प्रकाश", "prakaash", "light — र tucked under: प्र"), ("क्रम", "kram", "order — क्र"), ("ब्राह्मण", "braahman", "brahmin — ब्र"), ("ट्रक", "trak", "truck — ट्र, the hat shape"),
                ("ट्रेन", "tren", "train — ट्रे"), ("ड्रम", "dram", "drum — ड्र"), ("कर्म", "karm", "deed — र on TOP of the next letter: र्म"), ("धर्म", "dharm", "religion — र्म"),
                ("सूर्य", "soorya", "sun — र्य"), ("कार्य", "kaarya", "work — र्य"), ("दर्द", "dard", "pain — र्द"), ("गर्म", "garm", "hot — र्म"),
                ("वृक्ष", "vriksh", "tree — ृ and क्ष together"), ("मूर्ति", "moorti", "statue — र्ति"), ("पर्व", "parv", "festival — र्व"), ("शर्म", "sharm", "shyness — र्म"),
            ]),
        ],
        sentences=[
            ("बच्चा स्कूल जा रहा है।", "bachchaa skool jaa rahaa hai.", "The child is going to school."),
            ("मित्र को पत्र लिख।", "mitra ko patra likh.", "Write a letter to your friend."),
            ("बिल्ली ने दूध पी लिया।", "billee ne doodh pee liyaa.", "The cat drank the milk."),
            ("पक्षी वृक्ष पर है।", "pakshee vriksh par hai.", "The bird is on the tree."),
            ("सूर्य पूर्व में उगता है।", "soorya poorv mein ugtaa hai.", "The sun rises in the east."),
            ("कृष्ण बाँसुरी बजाते हैं।", "Krishna baansuree bajaate hain.", "Krishna plays the flute."),
            ("ज्ञान से प्रकाश मिलता है।", "gyaan se prakaash miltaa hai.", "Knowledge brings light."),
            ("कक्षा में चित्र बनाओ।", "kakshaa mein chitra banaao.", "Draw a picture in class."),
            ("अच्छा बच्चा सच्चा होता है।", "achchhaa bachchaa sachchaa hotaa hai.", "A good child is truthful."),
        ],
        passage=("नन्हा मित्र", [
            ("मेरा नाम ऋषभ है। मैं कक्षा दो में हूँ।", "meraa naam Rishabh hai. main kakshaa do mein hoon.", "My name is Rishabh. I am in class two."),
            ("मेरा एक मित्र है — एक नन्हा कुत्ता।", "meraa ek mitra hai — ek nanhaa kuttaa.", "I have a friend — a tiny dog."),
            ("वह रोज मेरे साथ स्कूल तक आता है।", "vah roj mere saath skool tak aataa hai.", "Every day he comes with me as far as school."),
            ("वृक्ष के नीचे बैठ कर मेरा इंतजार करता है।", "vriksh ke neeche baith kar meraa intajaar kartaa hai.", "He sits under the tree and waits for me."),
            ("छुट्टी में हम गेंद से खेलते हैं।", "chhuttee mein ham gend se khelte hain.", "In the break we play with a ball."),
            ("माँ कहती हैं — मित्रता सबसे बड़ा धर्म है।", "maan kahtee hain — mitrataa sabse baraa dharm hai.", "Mother says — friendship is the greatest virtue."),
            ("मैं सच्चा मित्र बनना चाहता हूँ।", "main sachchaa mitra bannaa chaahtaa hoon.", "I want to be a true friend."),
        ]),
        task="Write क्ष त्र ज्ञ श्र ten times each as single shapes. Then take any page of Hindi — a "
             "newspaper, a shop sign — and circle every half letter you can find. Count them.",
        quiz=[
            ("What does ् do?", "Removes the built-in 'a' so the consonant becomes 'half' and joins the next letter: क + ् + ष = क्ष."),
            ("What are the three shapes of र?", "Tucked under (प्र, क्र), the 'hat' under ट ड (ट्र, ड्र), and the hook on TOP of the following letter when र comes first (कर्म, सूर्य)."),
            ("Read बच्चा.", "ब + च् + चा — bachchaa, child. The first च is half and leans on the second."),
        ],
    ),
    # ------------------------------------------------------------ 18
    dict(
        n=18, slug="pahli-kahani", kind="reader",
        allow={"aa", "i", "ee", "u", "oo", "e", "ai", "o", "au", "an", "ah", "chandra", "ri", "halant"},
        hi="पहली कहानी", en="Your first reader",
        sub="Two short stories using everything from lessons 1 to 17",
        lede="This is the last page of a class-1 primer: a real story, read start to finish. "
             "Everything in it has been taught. Read each line aloud, tap the speaker to check, "
             "and only then open the English. If you finish both stories without the English, "
             "you can read Hindi.",
        stories=[
            ("प्यासा कौआ", "pyaasaa kauaa", "The thirsty crow", [
                ("गरमी का दिन था।", "garmee kaa din thaa.", "It was a hot day."),
                ("एक कौआ बहुत प्यासा था।", "ek kauaa bahut pyaasaa thaa.", "A crow was very thirsty."),
                ("वह पानी की खोज में इधर-उधर उड़ा।", "vah paanee kee khoj mein idhar-udhar uraa.", "He flew here and there looking for water."),
                ("कहीं पानी नहीं मिला।", "kaheen paanee naheen milaa.", "He found water nowhere."),
                ("तभी उसे एक घड़ा दिखा।", "tabhee use ek gharaa dikhaa.", "Just then he saw a pot."),
                ("घड़े में थोड़ा पानी था — बहुत नीचे।", "ghare mein thoraa paanee thaa — bahut neeche.", "There was a little water in the pot — very low down."),
                ("कौए की चोंच पानी तक नहीं पहुँची।", "kaue kee chonch paanee tak naheen pahunchee.", "The crow's beak could not reach the water."),
                ("कौआ चतुर था। उसने पास में कंकड़ देखे।", "kauaa chatur thaa. usne paas mein kankar dekhe.", "The crow was clever. He saw pebbles nearby."),
                ("वह एक-एक कंकड़ लाया और घड़े में डाला।", "vah ek-ek kankar laayaa aur ghare mein daalaa.", "He brought the pebbles one by one and dropped them in the pot."),
                ("पानी ऊपर आ गया।", "paanee oopar aa gayaa.", "The water came up."),
                ("कौए ने पानी पिया और उड़ गया।", "kaue ne paanee piyaa aur ur gayaa.", "The crow drank the water and flew away."),
                ("सीख: मेहनत और समझ से हर काम बनता है।", "seekh: mehnat aur samajh se har kaam bantaa hai.", "Lesson: with effort and sense every job gets done."),
            ]),
            ("मीना का एक दिन", "Meenaa kaa ek din", "A day in Meena's life", [
                ("मीना सुबह पाँच बजे उठती है।", "Meenaa subah paanch baje uthtee hai.", "Meena gets up at five in the morning."),
                ("वह दाँत साफ करती है और नहाती है।", "vah daant saaph kartee hai aur nahaatee hai.", "She brushes her teeth and bathes."),
                ("माँ ने गरम दूध और रोटी दी।", "maan ne garam doodh aur rotee dee.", "Mother gave warm milk and roti."),
                ("मीना बस्ता उठा कर स्कूल गई।", "Meenaa bastaa uthaa kar skool gaee.", "Meena picked up her bag and went to school."),
                ("कक्षा में उसने हिंदी की किताब पढ़ी।", "kakshaa mein usne Hindee kee kitaab parhee.", "In class she read her Hindi book."),
                ("छुट्टी में सहेलियों के साथ खेली।", "chhuttee mein saheliyon ke saath khelee.", "In the break she played with her friends."),
                ("दोपहर को घर आई। भोजन किया।", "dopahar ko ghar aaee. bhojan kiyaa.", "In the afternoon she came home. She ate."),
                ("शाम को दादी ने कहानी सुनाई।", "shaam ko daadee ne kahaanee sunaaee.", "In the evening grandmother told a story."),
                ("रात को चाँद निकला। मीना सो गई।", "raat ko chaand niklaa. Meenaa so gaee.", "At night the moon came out. Meena fell asleep."),
                ("कल फिर एक नया दिन।", "kal phir ek nayaa din.", "Tomorrow, a new day again."),
            ]),
        ],
        questions=[
            ("कौआ क्यों उड़ रहा था?", "kauaa kyon ur rahaa thaa?", "Why was the crow flying about?", "वह प्यासा था और पानी खोज रहा था। — He was thirsty and looking for water."),
            ("कौए ने घड़े में क्या डाला?", "kaue ne ghare mein kyaa daalaa?", "What did the crow drop into the pot?", "कंकड़। — Pebbles."),
            ("मीना कितने बजे उठती है?", "Meenaa kitne baje uthtee hai?", "What time does Meena get up?", "सुबह पाँच बजे। — At five in the morning."),
            ("शाम को कहानी किसने सुनाई?", "shaam ko kahaanee kisne sunaaee?", "Who told the story in the evening?", "दादी ने। — Grandmother."),
        ],
        task="Read both stories aloud twice. Then write five sentences about YOUR day in the "
             "style of 'मीना का एक दिन' — simple present, one line each. That is the first Hindi "
             "you will have written on your own.",
        quiz=[
            ("What should you do before opening the English?", "Read the line aloud and tap the speaker. Meaning first from the Hindi, English only to check."),
            ("Which lesson taught चोंच?", "Lesson 13 (ो) and lesson 15 (ं) together — चों-च. Every word here is built from signs you already know."),
            ("What comes after this page?", "Reading real things: a menu, a sign, Daily Hindi day 12 onward, and the A1 course — see 'Keep going' below."),
        ],
    ),
]

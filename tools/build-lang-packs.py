#!/usr/bin/env python3
"""Phase 7C Stage 3 — author the multi-language starter packs (BETA proof of
engine reuse), and rebuild the pack manifest.

Each pack below is AUTHORED content (not machine translation): 24 words +
12 phrases + 4 grammar concepts per language, with romanisation and a simple
English gloss. A pack makes a language BETA (starter reference) — NEVER
PRODUCTION. Hindi stays the only PRODUCTION language.

Generates (never hand-edit; rerun this tool):
  data/lang-{en,bn,ta,te,mr,gu,pa,ur}.json   — one pack per new language
  data/language-packs.json                    — manifest of ALL packs (incl. es)

Run:  python3 tools/build-lang-packs.py
"""
import json, os, re, time, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

STD_SCOPE = ("Starter pack: beginner vocabulary + phrases + grammar reference, authored and "
             "checked. No lesson pages, no audio, no quizzes, no review course — this is NOT a "
             "full course and NOT PRODUCTION.")
STD_NOTE = ("BETA proof of engine reuse. Not PRODUCTION: Hindi is the only production language. "
            "This is starter reference content only — not a course.")


def slugify(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "x"


# ---------------------------------------------------------------- authored packs
# word  = (target, roman, meaning, pos, topic)
# phrase= (target, roman, meaning, topic, register)
PACKS = {
    "en": {
        "name": "English", "native": "English",
        "about": ("English basics for Hindi speakers — the most common words and phrases with "
                  "pronunciation and simple meanings. This starter pack is reference material, "
                  "not a full English course."),
        "words": [
            ("hello", "heh-LOH", "a greeting", "greeting", "greetings"),
            ("goodbye", "guhd-BYE", "a word said when leaving", "greeting", "greetings"),
            ("please", "pleez", "used to ask politely", "adverb", "essentials"),
            ("thanks", "thangks", "short for thank you", "noun", "essentials"),
            ("yes", "yes", "agreement", "particle", "essentials"),
            ("no", "noh", "refusal", "particle", "essentials"),
            ("water", "WAW-tuhr", "the clear drink we need every day", "noun", "essentials"),
            ("food", "food", "what we eat", "noun", "essentials"),
            ("house", "hows", "the place where someone lives", "noun", "home"),
            ("work", "wurk", "a job, or doing a task", "noun", "daily"),
            ("time", "tym", "what clocks measure", "noun", "time"),
            ("day", "day", "24 hours, morning to night", "noun", "time"),
            ("night", "nyt", "the dark hours for sleeping", "noun", "time"),
            ("friend", "frend", "someone you like and trust", "noun", "people"),
            ("family", "FAM-uh-lee", "parents, children and relatives", "noun", "people"),
            ("money", "MUH-nee", "what you use to buy things", "noun", "daily"),
            ("book", "buuk", "pages with words, for reading", "noun", "objects"),
            ("big", "big", "large in size", "adjective", "basics"),
            ("small", "smawl", "little in size", "adjective", "basics"),
            ("good", "guud", "pleasant, right, of quality", "adjective", "basics"),
            ("bad", "bad", "not good", "adjective", "basics"),
            ("help", "help", "to make something easier for someone", "verb", "actions"),
            ("come", "kum", "to move toward here", "verb", "actions"),
            ("go", "goh", "to move away from here", "verb", "actions"),
        ],
        "phrases": [
            ("How are you?", "how ahr YOO", "a polite question about someone", "greetings", "neutral"),
            ("What is your name?", "wuht iz yur NAYM", "asking someone's name", "greetings", "neutral"),
            ("My name is …", "my NAYM iz", "telling your name", "introductions", "neutral"),
            ("Nice to meet you.", "nys too MEET yoo", "said when you first meet someone", "introductions", "neutral"),
            ("Thank you very much.", "thangk yoo VER-ee much", "strong thanks", "essentials", "neutral"),
            ("Excuse me.", "eks-KYOOZ mee", "to get attention or pass by", "essentials", "polite"),
            ("I am sorry.", "eye am SAH-ree", "an apology", "essentials", "neutral"),
            ("I don't understand.", "eye dohnt un-der-STAND", "you did not catch the meaning", "problems", "neutral"),
            ("Please speak slowly.", "pleez speek SLOH-lee", "a request to talk slower", "problems", "polite"),
            ("Where is the toilet?", "wair iz thuh TOY-let", "asking for the bathroom", "travel", "neutral"),
            ("How much is this?", "how much iz THIS", "asking the price", "shopping", "neutral"),
            ("See you later.", "see yoo LAY-ter", "a farewell", "greetings", "casual"),
        ],
        "concepts": [
            {"concept": "Subject pronouns — who is acting",
             "pattern": "I · you · he · she · it · we · they",
             "examples": [{"target": "I am a student", "roman": "eye am uh STOO-duhnt", "gloss": "I study"},
                          {"target": "She is my friend", "roman": "shee iz my frend", "gloss": "she is my friend"},
                          {"target": "They are here", "roman": "thay ahr heer", "gloss": "they are here"}],
             "exceptions": ["'you' is both singular and plural."],
             "learnerNote": "English has one 'you' for friendly and formal use, unlike Hindi's tu/tum/aap.",
             "commonMistakes": ["Using 'he' for a woman", "Forgetting 'it' for things and animals"]},
            {"concept": "The verb 'to be' — am · is · are",
             "pattern": "I am · you/we/they are · he/she/it is",
             "examples": [{"target": "I am happy", "roman": "eye am HAP-ee", "gloss": "I am happy"},
                          {"target": "He is at home", "roman": "hee iz at hohm", "gloss": "he is at home"},
                          {"target": "They are busy", "roman": "thay ahr BIZ-ee", "gloss": "they are busy"}],
             "exceptions": ["am only after I; is only after a singular third person."],
             "learnerNote": "Match the be-verb to the subject. Hindi speakers often drop it — don't.",
             "commonMistakes": ["'I is' instead of 'I am'", "Dropping the verb: 'She happy'"]},
            {"concept": "Articles — a · an · the",
             "pattern": "a/an for one of many; the for the specific one",
             "examples": [{"target": "a book", "roman": "uh buuk", "gloss": "one book (any)"},
                          {"target": "an apple", "roman": "uhn AP-uhl", "gloss": "one apple"},
                          {"target": "the sun", "roman": "thuh sun", "gloss": "the one sun we know"}],
             "exceptions": ["an before vowel sounds (an hour, an honest man)."],
             "learnerNote": "Hindi has no exact articles; think of 'a/an' as 'ek' and 'the' as the specific one already known.",
             "commonMistakes": ["Using 'a' before a vowel sound", "Adding 'the' before every noun"]},
            {"concept": "Present simple vs present continuous",
             "pattern": "I eat (habit) vs I am eating (now)",
             "examples": [{"target": "I read every day", "roman": "eye reed EV-ree day", "gloss": "a habit"},
                          {"target": "I am reading now", "roman": "eye am REE-ding now", "gloss": "happening now"},
                          {"target": "She works in Jaipur", "roman": "shee wurks in JY-poor", "gloss": "a fact"}],
             "exceptions": ["state verbs (know, want, like) rarely take -ing."],
             "learnerNote": "Simple = habit or fact; continuous = happening right now.",
             "commonMistakes": ["'I am knowing' instead of 'I know'", "Using -ing for everyday habits"]},
        ],
    },
    "bn": {
        "name": "Bengali", "native": "বাংলা",
        "about": ("Bengali (বাংলা) is spoken by over 230 million people, mostly in Bangladesh and "
                  "West Bengal. This starter pack gives the most common words and phrases with "
                  "pronunciation — a first taste of the script and grammar, not a full course."),
        "words": [
            ("আমি", "AH-mee", "I", "pronoun", "people"),
            ("তুমি", "TOO-mee", "you (informal)", "pronoun", "people"),
            ("সে", "sheh", "he / she", "pronoun", "people"),
            ("আমরা", "AHM-rah", "we", "pronoun", "people"),
            ("নাম", "nahm", "name", "noun", "people"),
            ("পানি", "PAH-nee", "water", "noun", "essentials"),
            ("খাবার", "KHAH-bar", "food", "noun", "essentials"),
            ("বাড়ি", "BAH-ree", "house / home", "noun", "home"),
            ("কাজ", "kahj", "work", "noun", "daily"),
            ("দিন", "deen", "day", "noun", "time"),
            ("রাত", "raht", "night", "noun", "time"),
            ("বন্ধু", "BON-dhoo", "friend", "noun", "people"),
            ("পরিবার", "POH-ree-bar", "family", "noun", "people"),
            ("ভালো", "BHAH-lo", "good", "adjective", "basics"),
            ("খারাপ", "KHAH-rap", "bad", "adjective", "basics"),
            ("বড়", "BOH-ro", "big", "adjective", "basics"),
            ("ছোট", "CHOH-to", "small", "adjective", "basics"),
            ("হ্যাঁ", "hã", "yes", "particle", "essentials"),
            ("না", "nah", "no", "particle", "essentials"),
            ("সময়", "SHOH-moy", "time", "noun", "time"),
            ("টাকা", "TAH-kah", "money", "noun", "daily"),
            ("বই", "boi", "book", "noun", "objects"),
            ("মানুষ", "MAH-noosh", "person", "noun", "people"),
            ("রাস্তা", "RAHS-tah", "road", "noun", "travel"),
        ],
        "phrases": [
            ("নমস্কার", "NOH-mosh-kar", "hello (respectful)", "greetings", "formal"),
            ("ধন্যবাদ", "DHON-no-bad", "thank you", "essentials", "neutral"),
            ("কেমন আছেন?", "KEH-mon AH-chhen", "How are you? (formal)", "greetings", "formal"),
            ("আপনার নাম কী?", "AP-nar nahm kee", "What is your name?", "greetings", "formal"),
            ("আমার নাম …", "AH-mar nahm", "My name is …", "introductions", "neutral"),
            ("এটা কত?", "EH-ta KOH-to", "How much is this?", "shopping", "neutral"),
            ("আমি বুঝতে পারছি না", "AH-mee BOOJH-teh PAR-chhee nah", "I don't understand", "problems", "neutral"),
            ("আবার দেখা হবে", "AH-bar DEH-kha HOH-beh", "See you again", "greetings", "casual"),
            ("দয়া করে", "DOH-ya KOH-reh", "please", "essentials", "polite"),
            ("দুঃখিত", "DOOK-khee-to", "sorry", "essentials", "neutral"),
            ("আমাকে সাহায্য করুন", "AH-mah-keh SHAH-haj-jo KOH-run", "please help me", "problems", "formal"),
            ("এটা কী?", "EH-ta kee", "What is this?", "basics", "neutral"),
        ],
        "concepts": [
            {"concept": "Subject pronouns",
             "pattern": "আমি · তুমি/আপনি · সে · আমরা",
             "examples": [{"target": "আমি খাই", "roman": "AH-mee khai", "gloss": "I eat"},
                          {"target": "তুমি খাও", "roman": "TOO-mee khao", "gloss": "you eat (informal)"},
                          {"target": "সে খায়", "roman": "sheh khay", "gloss": "he/she eats"}],
             "exceptions": ["আপনি (apni) is the polite 'you' and takes a -n verb ending."],
             "learnerNote": "Bengali has three 'you' levels: তুই (tui, very informal), তুমি (tumi), আপনি (apni, formal).",
             "commonMistakes": ["Using তুমি with elders", "Keeping the pronoun when the verb already shows it"]},
            {"concept": "Postpositions (not prepositions)",
             "pattern": "'of/at/in' markers come AFTER the noun",
             "examples": [{"target": "বাড়িতে", "roman": "BAH-ree-teh", "gloss": "at home"},
                          {"target": "টেবিলে", "roman": "TEH-bee-leh", "gloss": "on the table"},
                          {"target": "আমার", "roman": "AH-mar", "gloss": "my / mine"}],
             "exceptions": ["The noun often takes a different (oblique) shape before a postposition."],
             "learnerNote": "Where English says 'in the house', Bengali says 'house-in': বাড়িতে.",
             "commonMistakes": ["Word-for-word English order", "Forgetting the oblique form"]},
            {"concept": "Present tense — verb root + ending",
             "pattern": "-i / -o / -e match the subject",
             "examples": [{"target": "আমি যাই", "roman": "AH-mee jai", "gloss": "I go"},
                          {"target": "তুমি যাও", "roman": "TOO-mee jao", "gloss": "you go"},
                          {"target": "সে যায়", "roman": "sheh jay", "gloss": "he/she goes"}],
             "exceptions": ["আপনি takes -ন: আপনি যান (apni jan)."],
             "learnerNote": "The verb ending shows who acts, so the subject is often dropped.",
             "commonMistakes": ["Wrong ending for the person", "Applying English -ing logic"]},
            {"concept": "Negation with না (na)",
             "pattern": "verb + না = negative",
             "examples": [{"target": "আমি জানি না", "roman": "AH-mee jah-nee nah", "gloss": "I don't know"},
                          {"target": "সে আসবে না", "roman": "sheh AH-sh-beh nah", "gloss": "he/she won't come"},
                          {"target": "তুমি যাও না", "roman": "TOO-mee jao nah", "gloss": "you don't go"}],
             "exceptions": ["In the future too, না stays last."],
             "learnerNote": "Negation is simple: verb + না.",
             "commonMistakes": ["Putting না before the verb", "Forgetting না in the future tense"]},
        ],
    },
    "ta": {
        "name": "Tamil", "native": "தமிழ்",
        "about": ("Tamil (தமிழ்) is one of the world's oldest living classical languages, spoken by "
                  "about 80 million people in Tamil Nadu, Sri Lanka and a large diaspora. This "
                  "starter pack introduces the script and core words — reference content, not a "
                  "full course."),
        "words": [
            ("நான்", "nahn", "I", "pronoun", "people"),
            ("நீ", "nee", "you", "pronoun", "people"),
            ("அவன்", "AH-vahn", "he", "pronoun", "people"),
            ("அவள்", "AH-vahl", "she", "pronoun", "people"),
            ("நாங்கள்", "NAHNG-gahl", "we", "pronoun", "people"),
            ("பெயர்", "PEH-yar", "name", "noun", "people"),
            ("தண்ணீர்", "TAHN-neer", "water", "noun", "essentials"),
            ("சாப்பாடு", "SAHP-pah-doo", "food / meal", "noun", "essentials"),
            ("வீடு", "VEE-doo", "house", "noun", "home"),
            ("வேலை", "VEH-lai", "work", "noun", "daily"),
            ("நாள்", "nahl", "day", "noun", "time"),
            ("இரவு", "EE-rah-voo", "night", "noun", "time"),
            ("நண்பன்", "NAHN-pahn", "friend", "noun", "people"),
            ("குடும்பம்", "koo-DOOM-bam", "family", "noun", "people"),
            ("நல்ல", "NAHL-lah", "good", "adjective", "basics"),
            ("கெட்ட", "KET-tah", "bad", "adjective", "basics"),
            ("பெரிய", "PEH-ree-yah", "big", "adjective", "basics"),
            ("சிறிய", "SEE-ree-yah", "small", "adjective", "basics"),
            ("ஆம்", "ahm", "yes", "particle", "essentials"),
            ("இல்லை", "IL-lai", "no / not", "particle", "essentials"),
            ("நேரம்", "NEH-ram", "time", "noun", "time"),
            ("பணம்", "PAH-nam", "money", "noun", "daily"),
            ("புத்தகம்", "POOT-tah-gam", "book", "noun", "objects"),
            ("மனிதன்", "MAH-nee-tahn", "person", "noun", "people"),
        ],
        "phrases": [
            ("வணக்கம்", "VAH-nak-kam", "hello / greetings", "greetings", "neutral"),
            ("நன்றி", "NAHN-ree", "thank you", "essentials", "neutral"),
            ("எப்படி இருக்கிறீர்கள்?", "EH-pah-dee ee-ROOK-kee-reer-gahl", "How are you? (formal)", "greetings", "formal"),
            ("உங்கள் பெயர் என்ன?", "OONG-gahl PEH-yar EN-nah", "What is your name?", "greetings", "formal"),
            ("என் பெயர் …", "en PEH-yar", "My name is …", "introductions", "neutral"),
            ("இது என்ன?", "EE-doo EN-nah", "What is this?", "basics", "neutral"),
            ("எனக்கு புரியவில்லை", "en-NAK-koo POO-ree-yah-VIL-lai", "I don't understand", "problems", "neutral"),
            ("மீண்டும் சந்திப்போம்", "MEEN-doom SAHN-dee-pohm", "See you again", "greetings", "casual"),
            ("தயவு செய்து", "TAH-yah-voo SEY-doo", "please", "essentials", "polite"),
            ("மன்னிக்கவும்", "MAHN-nee-kah-voom", "sorry / excuse me", "essentials", "neutral"),
            ("உதவி செய்யுங்கள்", "OO-dah-vee SEY-yoong-gahl", "please help", "problems", "formal"),
            ("எவ்வளவு?", "EV-vah-lah-voo", "How much?", "shopping", "neutral"),
        ],
        "concepts": [
            {"concept": "Subject pronouns",
             "pattern": "நான் · நீ · அவன்/அவள் · நாங்கள்",
             "examples": [{"target": "நான் படிக்கிறேன்", "roman": "nahn pah-dee-kee-REHN", "gloss": "I read"},
                          {"target": "நீ வா", "roman": "nee vah", "gloss": "you come"},
                          {"target": "அவன் போகிறான்", "roman": "AH-vahn POH-gee-rahn", "gloss": "he goes"}],
             "exceptions": ["அவன் = he, அவள் = she, அது = it."],
             "learnerNote": "Tamil has distinct pronouns for he, she and it.",
             "commonMistakes": ["Mixing அவன் and அவள்", "Using நீ for elders (use நீங்கள்)"]},
            {"concept": "Word order (SOV)",
             "pattern": "subject — object — verb",
             "examples": [{"target": "நான் புத்தகம் படிக்கிறேன்", "roman": "nahn POOT-tah-gam pah-dee-kee-REHN", "gloss": "I book read"},
                          {"target": "அவள் தண்ணீர் குடிக்கிறாள்", "roman": "AH-vahl TAHN-neer koo-dee-kee-RAHL", "gloss": "she water drinks"},
                          {"target": "நாங்கள் வீட்டுக்குப் போகிறோம்", "roman": "NAHNG-gahl VEE-too-koo POH-gee-rohm", "gloss": "we house-to go"}],
             "exceptions": ["The verb is almost always last."],
             "learnerNote": "English 'I read a book' becomes 'I book read' in Tamil.",
             "commonMistakes": ["English word order", "Putting the verb early"]},
            {"concept": "Present tense — கிற் (-kiṟ-) + person ending",
             "pattern": "verb + -kiṟ- + person/politeness ending",
             "examples": [{"target": "நான் செய்கிறேன்", "roman": "nahn SEY-gee-rehn", "gloss": "I do"},
                          {"target": "நீ செய்கிறாய்", "roman": "nee SEY-gee-rye", "gloss": "you do"},
                          {"target": "அவர் செய்கிறார்", "roman": "AH-var SEY-gee-rahr", "gloss": "he does (respectful)"}],
             "exceptions": ["The ending changes with politeness and person."],
             "learnerNote": "The ending already tells who acts, so the subject is often dropped.",
             "commonMistakes": ["Dropping the tense marker", "Wrong politeness ending"]},
            {"concept": "Politeness levels — நீ vs நீங்கள்",
             "pattern": "informal நீ · formal/plural நீங்கள்",
             "examples": [{"target": "நீ எப்படி இருக்கிறாய்?", "roman": "nee EH-pah-dee ee-ROOK-kee-rye", "gloss": "how are you? (informal)"},
                          {"target": "நீங்கள் எப்படி இருக்கிறீர்கள்?", "roman": "NEENG-gahl EH-pah-dee ee-ROOK-kee-reer-gahl", "gloss": "how are you? (formal)"},
                          {"target": "வாருங்கள்", "roman": "VAH-roong-gahl", "gloss": "please come"}],
             "exceptions": ["Use நீங்கள் for elders, strangers and groups."],
             "learnerNote": "Like Hindi's aap, Tamil நீங்கள் shows respect and is also the plural.",
             "commonMistakes": ["Using நீ with elders", "Forgetting -ங்கள் in formal requests"]},
        ],
    },
    "te": {
        "name": "Telugu", "native": "తెలుగు",
        "about": ("Telugu (తెలుగు) is spoken by over 90 million people, mainly in Andhra Pradesh and "
                  "Telangana. This starter pack covers the most useful words and phrases with "
                  "pronunciation — a first look at the script and grammar, not a full course."),
        "words": [
            ("నేను", "NEH-noo", "I", "pronoun", "people"),
            ("నువ్వు", "NOOV-voo", "you (informal)", "pronoun", "people"),
            ("అతను", "AH-tah-noo", "he", "pronoun", "people"),
            ("ఆమె", "AH-meh", "she", "pronoun", "people"),
            ("మేము", "MEH-moo", "we", "pronoun", "people"),
            ("పేరు", "PEH-roo", "name", "noun", "people"),
            ("నీళ్ళు", "NEE-ḷḷoo", "water", "noun", "essentials"),
            ("భోజనం", "BHOH-jah-nam", "food / meal", "noun", "essentials"),
            ("ఇల్లు", "IL-loo", "house", "noun", "home"),
            ("పని", "PAH-nee", "work", "noun", "daily"),
            ("రోజు", "ROH-joo", "day", "noun", "time"),
            ("రాత్రి", "RAH-tree", "night", "noun", "time"),
            ("స్నేహితుడు", "SNEH-hee-too-doo", "friend", "noun", "people"),
            ("కుటుంబం", "koo-TOOM-bam", "family", "noun", "people"),
            ("మంచి", "MAHN-chee", "good", "adjective", "basics"),
            ("చెడు", "CHEH-doo", "bad", "adjective", "basics"),
            ("పెద్ద", "PED-dah", "big", "adjective", "basics"),
            ("చిన్న", "CHIN-nah", "small", "adjective", "basics"),
            ("అవును", "AH-voo-noo", "yes", "particle", "essentials"),
            ("కాదు", "KAH-doo", "no / not", "particle", "essentials"),
            ("సమయం", "SAH-mah-yam", "time", "noun", "time"),
            ("డబ్బు", "DAB-boo", "money", "noun", "daily"),
            ("పుస్తకం", "POOS-tah-kam", "book", "noun", "objects"),
            ("మనిషి", "MAH-nee-shee", "person", "noun", "people"),
        ],
        "phrases": [
            ("నమస్తే", "NAH-mas-teh", "hello", "greetings", "neutral"),
            ("ధన్యవాదాలు", "DAHN-yah-vah-DAH-loo", "thank you", "essentials", "neutral"),
            ("ఎలా ఉన్నారు?", "EH-lah oon-NAH-roo", "How are you? (formal)", "greetings", "formal"),
            ("మీ పేరు ఏమిటి?", "mee PEH-roo EH-mee-tee", "What is your name?", "greetings", "formal"),
            ("నా పేరు …", "nah PEH-roo", "My name is …", "introductions", "neutral"),
            ("ఇది ఏమిటి?", "EE-dee EH-mee-tee", "What is this?", "basics", "neutral"),
            ("నాకు అర్థం కాలేదు", "NAH-koo AR-tham KAH-leh-doo", "I don't understand", "problems", "neutral"),
            ("మళ్ళీ కలుద్దాం", "MAL-lee kah-lood-DAHM", "See you again", "greetings", "casual"),
            ("దయచేసి", "DAH-yah-CHEH-see", "please", "essentials", "polite"),
            ("క్షమించండి", "kshah-MIN-chahn-dee", "sorry / excuse me", "essentials", "formal"),
            ("సహాయం చేయండి", "sah-HAH-yam CHEH-yahn-dee", "please help", "problems", "formal"),
            ("ఎంత?", "EN-tah", "How much?", "shopping", "neutral"),
        ],
        "concepts": [
            {"concept": "Subject pronouns",
             "pattern": "నేను · నువ్వు/మీరు · అతను/ఆమె · మేము",
             "examples": [{"target": "నేను వస్తున్నాను", "roman": "NEH-noo vas-toon-NAH-noo", "gloss": "I am coming"},
                          {"target": "నువ్వు వెళ్ళు", "roman": "NOOV-voo VEL-loo", "gloss": "you go"},
                          {"target": "ఆమె పాడుతుంది", "roman": "AH-meh PAH-doo-toon-dee", "gloss": "she sings"}],
             "exceptions": ["మీరు (mīru) is polite 'you' (also plural)."],
             "learnerNote": "Telugu నువ్వు is informal; మీరు shows respect.",
             "commonMistakes": ["Using నువ్వు with elders", "Mixing అతను (he) and ఆమె (she)"]},
            {"concept": "Word order (SOV)",
             "pattern": "subject — object — verb",
             "examples": [{"target": "నేను పుస్తకం చదువుతున్నాను", "roman": "NEH-noo POOS-tah-kam chah-doo-voo-toon-NAH-noo", "gloss": "I book am reading"},
                          {"target": "ఆమె నీళ్ళు తాగుతుంది", "roman": "AH-meh NEE-ḷḷoo TAH-goo-toon-dee", "gloss": "she water drinks"},
                          {"target": "మేము ఇంటికి వెళ్తున్నాము", "roman": "MEH-moo IN-tee-kee VEL-toon-NAH-moo", "gloss": "we house-to are going"}],
             "exceptions": ["The verb comes last in neutral sentences."],
             "learnerNote": "Like Hindi, Telugu is SOV: 'I water drink'.",
             "commonMistakes": ["English word order", "Verb placement"]},
            {"concept": "Present tense — -తున్నా- (-tunnā-) + ending",
             "pattern": "verb + -tunnā- + person/gender ending",
             "examples": [{"target": "నేను చేస్తున్నాను", "roman": "NEH-noo cheh-stoon-NAH-noo", "gloss": "I am doing"},
                          {"target": "నువ్వు చేస్తున్నావు", "roman": "NOOV-voo cheh-stoon-NAH-voo", "gloss": "you are doing"},
                          {"target": "అతను చేస్తున్నాడు", "roman": "AH-tah-noo cheh-stoon-NAH-doo", "gloss": "he is doing"}],
             "exceptions": ["The ending matches person and gender."],
             "learnerNote": "The -తున్నా- marks the ongoing action.",
             "commonMistakes": ["Dropping the -తున్నా- marker", "Wrong person ending"]},
            {"concept": "Case suffixes — కి/కు, లో, తో",
             "pattern": "noun + suffix = 'to / in / with'",
             "examples": [{"target": "ఇంటికి", "roman": "IN-tee-kee", "gloss": "to the house"},
                          {"target": "ఇంట్లో", "roman": "INT-loh", "gloss": "in the house"},
                          {"target": "నాతో", "roman": "NAH-toh", "gloss": "with me"}],
             "exceptions": ["The noun changes slightly before the suffix (sandhi)."],
             "learnerNote": "Telugu adds endings to nouns instead of prepositions.",
             "commonMistakes": ["Separate prepositions", "Forgetting the sandhi change"]},
        ],
    },
    "mr": {
        "name": "Marathi", "native": "मराठी",
        "about": ("Marathi (मराठी) is spoken by over 90 million people, mostly in Maharashtra and "
                  "around Mumbai. This starter pack gives the everyday words and phrases with "
                  "pronunciation — a first taste of the language, not a full course."),
        "words": [
            ("मी", "mee", "I", "pronoun", "people"),
            ("तू", "too", "you (informal)", "pronoun", "people"),
            ("तो", "toh", "he", "pronoun", "people"),
            ("ती", "tee", "she", "pronoun", "people"),
            ("आम्ही", "AHM-hee", "we", "pronoun", "people"),
            ("नाव", "nahv", "name", "noun", "people"),
            ("पाणी", "PAH-nee", "water", "noun", "essentials"),
            ("जेवण", "JEH-vahn", "food / meal", "noun", "essentials"),
            ("घर", "ghur", "house / home", "noun", "home"),
            ("काम", "kahm", "work", "noun", "daily"),
            ("दिवस", "DEE-vus", "day", "noun", "time"),
            ("रात्र", "RAH-truh", "night", "noun", "time"),
            ("मित्र", "MEE-truh", "friend", "noun", "people"),
            ("कुटुंब", "koo-TOOM-b", "family", "noun", "people"),
            ("चांगला", "CHAHNG-glah", "good", "adjective", "basics"),
            ("वाईट", "VAH-eeṭ", "bad", "adjective", "basics"),
            ("मोठा", "MOH-thah", "big", "adjective", "basics"),
            ("लहान", "lah-HAHN", "small", "adjective", "basics"),
            ("हो", "hoh", "yes", "particle", "essentials"),
            ("नाही", "NAH-hee", "no / not", "particle", "essentials"),
            ("वेळ", "vehl", "time", "noun", "time"),
            ("पैसे", "PAI-seh", "money", "noun", "daily"),
            ("पुस्तक", "POOS-tuk", "book", "noun", "objects"),
            ("माणूस", "MAH-noos", "person", "noun", "people"),
        ],
        "phrases": [
            ("नमस्कार", "nuh-mus-KAHR", "hello (respectful)", "greetings", "formal"),
            ("धन्यवाद", "DHUN-yah-vahd", "thank you", "essentials", "neutral"),
            ("तुम्ही कसे आहात?", "TOOM-hee kuh-SEH AH-haht", "How are you? (formal)", "greetings", "formal"),
            ("तुमचे नाव काय?", "TOOM-cheh nahv kahy", "What is your name?", "greetings", "formal"),
            ("माझे नाव …", "MAH-jheh nahv", "My name is …", "introductions", "neutral"),
            ("हे काय आहे?", "heh kahy AH-heh", "What is this?", "basics", "neutral"),
            ("मला समजले नाही", "muh-LAH suh-MUJ-leh NAH-hee", "I don't understand", "problems", "neutral"),
            ("पुन्हा भेटू", "POON-hah BHEH-too", "See you again", "greetings", "casual"),
            ("कृपया", "KRIH-puh-yah", "please", "essentials", "polite"),
            ("माफ करा", "mahf kuh-RAH", "sorry", "essentials", "neutral"),
            ("मदत करा", "muh-DUT kuh-RAH", "please help", "problems", "neutral"),
            ("किती?", "KEE-tee", "How much?", "shopping", "neutral"),
        ],
        "concepts": [
            {"concept": "Subject pronouns",
             "pattern": "मी · तू/तुम्ही · तो/ती · आम्ही",
             "examples": [{"target": "मी बोलतो", "roman": "mee BOHL-toh", "gloss": "I speak (masc.)"},
                          {"target": "ती बोलते", "roman": "tee BOHL-teh", "gloss": "she speaks"},
                          {"target": "तुम्ही बोलता", "roman": "TOOM-hee BOHL-tah", "gloss": "you speak (formal)"}],
             "exceptions": ["तुम्ही is polite/plural 'you'."],
             "learnerNote": "Marathi verbs change by the gender of the speaker: बोलतो (male) vs बोलते (female).",
             "commonMistakes": ["Using the wrong gender ending", "तू with elders"]},
            {"concept": "Noun gender",
             "pattern": "every noun is masculine, feminine or neuter",
             "examples": [{"target": "घर", "roman": "ghur", "gloss": "house (neuter)"},
                          {"target": "मुलगा", "roman": "mool-GAH", "gloss": "boy (masculine)"},
                          {"target": "मुलगी", "roman": "mool-GEE", "gloss": "girl (feminine)"}],
             "exceptions": ["Gender must be learned with each noun."],
             "learnerNote": "Neuter gender is common in Marathi — more than in Hindi.",
             "commonMistakes": ["Assuming Hindi gender", "Ignoring neuter"]},
            {"concept": "Present tense — -तो/-ते/-ता endings",
             "pattern": "verb + -to/-te/-tā matches gender & person",
             "examples": [{"target": "मी करतो", "roman": "mee kuh-TOH", "gloss": "I do (masc.)"},
                          {"target": "मी करते", "roman": "mee kuh-TEH", "gloss": "I do (fem.)"},
                          {"target": "तो करतो", "roman": "toh kuh-TOH", "gloss": "he does"}],
             "exceptions": ["The ending matches subject gender, number and person."],
             "learnerNote": "Same idea as Hindi's हूँ/है structure, but gendered for 'I'.",
             "commonMistakes": ["Wrong gender ending", "Dropping the -t-"]},
            {"concept": "Postpositions with oblique forms",
             "pattern": "माझे · तुझे · त्याचे — special forms before markers",
             "examples": [{"target": "माझे घर", "roman": "MAH-jheh ghur", "gloss": "my house"},
                          {"target": "त्याला पाणी", "roman": "TYAH-lah PAH-nee", "gloss": "to him water (he wants water)"},
                          {"target": "घरात", "roman": "ghuh-RAHT", "gloss": "in the house"}],
             "exceptions": ["Pronouns take special forms before postpositions."],
             "learnerNote": "Possession uses a form of the pronoun, not a separate word for 'my'.",
             "commonMistakes": ["Using मी for 'my' instead of माझे", "Wrong oblique form"]},
        ],
    },
    "gu": {
        "name": "Gujarati", "native": "ગુજરાતી",
        "about": ("Gujarati (ગુજરાતી) is spoken by over 55 million people, mainly in Gujarat and a "
                  "large diaspora worldwide. This starter pack introduces the script and the most "
                  "useful words and phrases — reference content, not a full course."),
        "words": [
            ("હું", "hoon", "I", "pronoun", "people"),
            ("તમે", "TAH-meh", "you (formal/neutral)", "pronoun", "people"),
            ("તે", "teh", "he / she", "pronoun", "people"),
            ("અમે", "AH-meh", "we", "pronoun", "people"),
            ("નામ", "nahm", "name", "noun", "people"),
            ("પાણી", "PAH-nee", "water", "noun", "essentials"),
            ("ખોરાક", "KHOH-rahk", "food", "noun", "essentials"),
            ("ઘર", "ghur", "house / home", "noun", "home"),
            ("કામ", "kahm", "work", "noun", "daily"),
            ("દિવસ", "DEE-vus", "day", "noun", "time"),
            ("રાત", "raht", "night", "noun", "time"),
            ("મિત્ર", "MEE-truh", "friend", "noun", "people"),
            ("કુટુંબ", "koo-TOOM-b", "family", "noun", "people"),
            ("સારું", "SAH-rooṁ", "good", "adjective", "basics"),
            ("ખરાબ", "khuh-RAHB", "bad", "adjective", "basics"),
            ("મોટું", "MOH-tooṁ", "big", "adjective", "basics"),
            ("નાનું", "NAH-nooṁ", "small", "adjective", "basics"),
            ("હા", "hah", "yes", "particle", "essentials"),
            ("ના", "nah", "no", "particle", "essentials"),
            ("સમય", "suh-MUY", "time", "noun", "time"),
            ("પૈસા", "PAI-sah", "money", "noun", "daily"),
            ("પુસ્તક", "POOS-tuk", "book", "noun", "objects"),
            ("માણસ", "MAH-nus", "person", "noun", "people"),
            ("બહેન", "buh-HEN", "sister", "noun", "people"),
        ],
        "phrases": [
            ("નમસ્તે", "nuh-MUS-teh", "hello", "greetings", "neutral"),
            ("આભાર", "AH-bhahr", "thank you", "essentials", "neutral"),
            ("તમે કેમ છો?", "TAH-meh kem chhoh", "How are you?", "greetings", "neutral"),
            ("તમારું નામ શું?", "tuh-MAH-rooṁ nahm shooṁ", "What is your name?", "greetings", "neutral"),
            ("મારું નામ …", "MAH-rooṁ nahm", "My name is …", "introductions", "neutral"),
            ("આ શું છે?", "ah shooṁ chheh", "What is this?", "basics", "neutral"),
            ("મને સમજાયું નહીં", "muh-NEH suh-muh-JAH-yooṁ nuh-HEEM", "I don't understand", "problems", "neutral"),
            ("ફરી મળીશું", "fuh-REE muh-LEE-shooṁ", "See you again", "greetings", "casual"),
            ("કૃપા કરીને", "KRIH-pah kuh-REE-neh", "please", "essentials", "polite"),
            ("માફ કરો", "mahf kuh-ROH", "sorry", "essentials", "neutral"),
            ("મદદ કરો", "muh-DUD kuh-ROH", "please help", "problems", "neutral"),
            ("કેટલું?", "KET-looṁ", "How much?", "shopping", "neutral"),
        ],
        "concepts": [
            {"concept": "Subject pronouns",
             "pattern": "હું · તમે · તે · અમે",
             "examples": [{"target": "હું બોલું છું", "roman": "hoon BOH-looṁ chhooṁ", "gloss": "I speak"},
                          {"target": "તમે બોલો છો", "roman": "TAH-meh BOH-loh chhoh", "gloss": "you speak"},
                          {"target": "તે બોલે છે", "roman": "teh BOH-leh chheh", "gloss": "he/she speaks"}],
             "exceptions": ["તમે is both singular-formal and plural."],
             "learnerNote": "Gujarati uses તમે (tame) far more than તું (tuṁ); it is the safe default.",
             "commonMistakes": ["Using informal તું with strangers", "Dropping the છું/છે helper"]},
            {"concept": "Word order (SOV)",
             "pattern": "subject — object — verb",
             "examples": [{"target": "હું પાણી પીઉં છું", "roman": "hoon PAH-nee PEE-yooṁ chhooṁ", "gloss": "I water drink"},
                          {"target": "તે પુસ્તક વાંચે છે", "roman": "teh POOS-tuk VAHN-cheh chheh", "gloss": "he book reads"},
                          {"target": "અમે ઘરે જઈએ છીએ", "roman": "AH-meh ghu-REH jah-EE-eh chhee-eh", "gloss": "we home-to go"}],
             "exceptions": ["The verb is last."],
             "learnerNote": "Like Hindi: 'I water drink'.",
             "commonMistakes": ["English word order", "Verb placement"]},
            {"concept": "Present tense — verb + છું/છો/છે helper",
             "pattern": "verb ending + છું (I) · છો (you) · છે (he/she)",
             "examples": [{"target": "હું કરું છું", "roman": "hoon kuh-ROOṁ chhooṁ", "gloss": "I do"},
                          {"target": "તમે કરો છો", "roman": "TAH-meh kuh-ROH chhoh", "gloss": "you do"},
                          {"target": "તે કરે છે", "roman": "teh kuh-REH chheh", "gloss": "he/she does"}],
             "exceptions": ["The helper છું/છો/છે is required."],
             "learnerNote": "Gujarati present needs two parts: main verb + છું/છો/છે.",
             "commonMistakes": ["Leaving out the helper", "Wrong helper for the person"]},
            {"concept": "Postpositions + oblique forms",
             "pattern": "'of/in/to' markers come after the noun",
             "examples": [{"target": "ઘરમાં", "roman": "ghur-MAHṀ", "gloss": "in the house"},
                          {"target": "મારું", "roman": "MAH-rooṁ", "gloss": "my / mine"},
                          {"target": "તેને", "roman": "TEH-neh", "gloss": "to him/her"}],
             "exceptions": ["Pronouns change before postpositions."],
             "learnerNote": "Where English uses prepositions, Gujarati sticks endings on the noun.",
             "commonMistakes": ["English preposition order", "Wrong oblique form"]},
        ],
    },
    "pa": {
        "name": "Punjabi", "native": "ਪੰਜਾਬੀ",
        "about": ("Punjabi (ਪੰਜਾਬੀ) is spoken by over 120 million people across Indian Punjab, "
                  "Pakistani Punjab and a worldwide diaspora. This starter pack introduces the "
                  "Gurmukhi script and everyday words and phrases — reference content, not a full "
                  "course."),
        "words": [
            ("ਮੈਂ", "maiṁ", "I", "pronoun", "people"),
            ("ਤੂੰ", "tooṁ", "you (informal)", "pronoun", "people"),
            ("ਤੁਸੀਂ", "tus-sīṁ", "you (formal)", "pronoun", "people"),
            ("ਉਹ", "uh", "he / she", "pronoun", "people"),
            ("ਅਸੀਂ", "as-sīṁ", "we", "pronoun", "people"),
            ("ਨਾਮ", "nahm", "name", "noun", "people"),
            ("ਪਾਣੀ", "PAH-nee", "water", "noun", "essentials"),
            ("ਖਾਣਾ", "KHAH-nah", "food", "noun", "essentials"),
            ("ਘਰ", "ghur", "house / home", "noun", "home"),
            ("ਕੰਮ", "kumm", "work", "noun", "daily"),
            ("ਦਿਨ", "din", "day", "noun", "time"),
            ("ਰਾਤ", "raht", "night", "noun", "time"),
            ("ਦੋਸਤ", "dost", "friend", "noun", "people"),
            ("ਪਰਿਵਾਰ", "puh-ree-VAHR", "family", "noun", "people"),
            ("ਚੰਗਾ", "CHUNG-gah", "good", "adjective", "basics"),
            ("ਮਾੜਾ", "MAH-ṛah", "bad", "adjective", "basics"),
            ("ਵੱਡਾ", "VUD-dah", "big", "adjective", "basics"),
            ("ਛੋਟਾ", "CHOH-tah", "small", "adjective", "basics"),
            ("ਹਾਂ", "hāṁ", "yes", "particle", "essentials"),
            ("ਨਹੀਂ", "nuh-HEEM", "no / not", "particle", "essentials"),
            ("ਸਮਾਂ", "suh-MAHṀ", "time", "noun", "time"),
            ("ਪੈਸੇ", "PAI-seh", "money", "noun", "daily"),
            ("ਕਿਤਾਬ", "kih-TAHB", "book", "noun", "objects"),
            ("ਬੰਦਾ", "BUN-dah", "person", "noun", "people"),
        ],
        "phrases": [
            ("ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "sut sree AH-kahl", "hello (Sikh greeting)", "greetings", "formal"),
            ("ਧੰਨਵਾਦ", "DHUN-nuh-vahd", "thank you", "essentials", "neutral"),
            ("ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?", "tus-sīṁ KIH-vehṁ hoh", "How are you?", "greetings", "neutral"),
            ("ਤੁਹਾਡਾ ਨਾਮ ਕੀ ਹੈ?", "tuh-HAH-dah nahm kee hai", "What is your name?", "greetings", "neutral"),
            ("ਮੇਰਾ ਨਾਮ …", "MEH-rah nahm", "My name is …", "introductions", "neutral"),
            ("ਇਹ ਕੀ ਹੈ?", "ih kee hai", "What is this?", "basics", "neutral"),
            ("ਮੈਨੂੰ ਸਮਝ ਨਹੀਂ ਆਇਆ", "mai-NOOM suh-MUJH nuh-HEEM AH-ee-ah", "I don't understand", "problems", "neutral"),
            ("ਫਿਰ ਮਿਲਾਂਗੇ", "fir mih-LAHN-geh", "See you again", "greetings", "casual"),
            ("ਕਿਰਪਾ ਕਰਕੇ", "KIR-pah KUR-keh", "please", "essentials", "polite"),
            ("ਮਾਫ਼ ਕਰਨਾ", "mahf KUR-nah", "sorry", "essentials", "neutral"),
            ("ਮਦਦ ਕਰੋ", "muh-DUD kuh-ROH", "please help", "problems", "neutral"),
            ("ਕਿੰਨਾ?", "KIN-nah", "How much?", "shopping", "neutral"),
        ],
        "concepts": [
            {"concept": "Subject pronouns + politeness",
             "pattern": "ਮੈਂ · ਤੂੰ/ਤੁਸੀਂ · ਉਹ · ਅਸੀਂ",
             "examples": [{"target": "ਮੈਂ ਬੋਲਦਾ ਹਾਂ", "roman": "maiṁ BOHL-dah hāṁ", "gloss": "I speak (masc.)"},
                          {"target": "ਤੂੰ ਬੋਲਦਾ ਹੈਂ", "roman": "tooṁ BOHL-dah haiṁ", "gloss": "you speak (informal)"},
                          {"target": "ਤੁਸੀਂ ਬੋਲਦੇ ਹੋ", "roman": "tus-sīṁ BOHL-deh hoh", "gloss": "you speak (formal)"}],
             "exceptions": ["ਤੁਸੀਂ = formal singular AND plural."],
             "learnerNote": "Default to ਤੁਸੀਂ; ਤੂੰ is for close friends and children.",
             "commonMistakes": ["ਤੂੰ with elders", "Wrong helper (ਹਾਂ/ਹੋ/ਹੈ)"]},
            {"concept": "Word order (SOV)",
             "pattern": "subject — object — verb",
             "examples": [{"target": "ਮੈਂ ਪਾਣੀ ਪੀਂਦਾ ਹਾਂ", "roman": "maiṁ PAH-nee PEEN-dah hāṁ", "gloss": "I water drink"},
                          {"target": "ਉਹ ਕਿਤਾਬ ਪੜ੍ਹਦਾ ਹੈ", "roman": "uh kih-TAHB PAHR-dah hai", "gloss": "he book reads"},
                          {"target": "ਅਸੀਂ ਘਰ ਜਾਂਦੇ ਹਾਂ", "roman": "as-sīṁ ghur JAHN-deh hāṁ", "gloss": "we home go"}],
             "exceptions": ["The verb is last."],
             "learnerNote": "'I water drink' — the verb sits at the end.",
             "commonMistakes": ["English word order", "Verb placement"]},
            {"concept": "Present tense — verb + -ਦਾ/-ਦੀ/-ਦੇ + helper",
             "pattern": "-dā (masc.) · -dī (fem.) · -de (pl.) + ਹਾਂ/ਹੋ/ਹੈ",
             "examples": [{"target": "ਮੈਂ ਕਰਦਾ ਹਾਂ", "roman": "maiṁ KUR-dah hāṁ", "gloss": "I do (masc.)"},
                          {"target": "ਮੈਂ ਕਰਦੀ ਹਾਂ", "roman": "maiṁ KUR-dee hāṁ", "gloss": "I do (fem.)"},
                          {"target": "ਉਹ ਕਰਦਾ ਹੈ", "roman": "uh KUR-dah hai", "gloss": "he does"}],
             "exceptions": ["The -ਦਾ/-ਦੀ ending matches gender."],
             "learnerNote": "The helper (ਹਾਂ/ਹੋ/ਹੈ) always comes last.",
             "commonMistakes": ["Wrong gender ending", "Dropping the helper"]},
            {"concept": "Oblique case with postpositions",
             "pattern": "ਕੋਲ (kol) · ਵਿੱਚ (vich) · ਨੂੰ (nūṁ) after the noun",
             "examples": [{"target": "ਮੇਰੇ ਕੋਲ", "roman": "MEH-reh kol", "gloss": "near me / I have"},
                          {"target": "ਘਰ ਵਿੱਚ", "roman": "ghur vich", "gloss": "in the house"},
                          {"target": "ਉਸਨੂੰ", "roman": "us-NOOṀ", "gloss": "to him/her"}],
             "exceptions": ["Nouns and pronouns change form before postpositions."],
             "learnerNote": "Punjabi marks 'in/at/to/with' by endings after an oblique noun form.",
             "commonMistakes": ["Preposition order", "Forgetting the oblique form"]},
        ],
    },
    "ur": {
        "name": "Urdu", "native": "اردو",
        "about": ("Urdu (اردو) is spoken by over 170 million people across Pakistan, India and a "
                  "large diaspora. It shares much of its grammar and everyday vocabulary with "
                  "Hindi, written in the Arabic script. This starter pack is a first taste, not a "
                  "full course."),
        "words": [
            ("میں", "maiṁ", "I", "pronoun", "people"),
            ("تم", "tum", "you (informal)", "pronoun", "people"),
            ("آپ", "ahp", "you (formal)", "pronoun", "people"),
            ("وہ", "vuh", "he / she", "pronoun", "people"),
            ("ہم", "hum", "we", "pronoun", "people"),
            ("نام", "nahm", "name", "noun", "people"),
            ("پانی", "PAH-nee", "water", "noun", "essentials"),
            ("کھانا", "KHAH-nah", "food", "noun", "essentials"),
            ("گھر", "ghur", "house / home", "noun", "home"),
            ("کام", "kahm", "work", "noun", "daily"),
            ("دن", "din", "day", "noun", "time"),
            ("رات", "raht", "night", "noun", "time"),
            ("دوست", "dost", "friend", "noun", "people"),
            ("خاندان", "khahn-DAHN", "family", "noun", "people"),
            ("اچھا", "ACH-chhah", "good", "adjective", "basics"),
            ("برا", "boo-RAH", "bad", "adjective", "basics"),
            ("بڑا", "buh-RAH", "big", "adjective", "basics"),
            ("چھوٹا", "CHHOH-tah", "small", "adjective", "basics"),
            ("ہاں", "hāṁ", "yes", "particle", "essentials"),
            ("نہیں", "nuh-HEEM", "no / not", "particle", "essentials"),
            ("وقت", "vukt", "time", "noun", "time"),
            ("پیسے", "PAI-seh", "money", "noun", "daily"),
            ("کتاب", "kih-TAHB", "book", "noun", "objects"),
            ("آدمی", "ahd-MEE", "person / man", "noun", "people"),
        ],
        "phrases": [
            ("السلام علیکم", "us-suh-LAH-moo AH-lai-koom", "hello (peace be upon you)", "greetings", "formal"),
            ("شکریہ", "SHUK-ree-yah", "thank you", "essentials", "neutral"),
            ("آپ کیسے ہیں؟", "ahp KAI-seh hāiṁ", "How are you?", "greetings", "formal"),
            ("آپ کا نام کیا ہے؟", "ahp kah nahm KYAH hai", "What is your name?", "greetings", "formal"),
            ("میرا نام …", "MEH-rah nahm", "My name is …", "introductions", "neutral"),
            ("یہ کیا ہے؟", "yah KYAH hai", "What is this?", "basics", "neutral"),
            ("میں نہیں سمجھا", "maiṁ nuh-HEEM SUM-jhah", "I don't understand", "problems", "neutral"),
            ("پھر ملیں گے", "fir mih-LEN-geh", "See you again", "greetings", "casual"),
            ("برائے مہربانی", "buh-RAH-eh mehr-BAH-nee", "please", "essentials", "polite"),
            ("معاف کیجیے", "moo-AHF KEE-jee-yeh", "sorry / excuse me", "essentials", "formal"),
            ("مدد کیجیے", "muh-DUD KEE-jee-yeh", "please help", "problems", "formal"),
            ("کتنا ہے؟", "KIT-nah hai", "How much?", "shopping", "neutral"),
        ],
        "concepts": [
            {"concept": "Subject pronouns + politeness",
             "pattern": "میں · تم/آپ · وہ · ہم",
             "examples": [{"target": "میں بولتا ہوں", "roman": "maiṁ BOHL-tah hooṁ", "gloss": "I speak (masc.)"},
                          {"target": "تم بولتے ہو", "roman": "tum BOHL-teh ho", "gloss": "you speak (informal)"},
                          {"target": "آپ بولتے ہیں", "roman": "ahp BOHL-teh haiṁ", "gloss": "you speak (formal)"}],
             "exceptions": ["آپ = formal singular AND plural."],
             "learnerNote": "Urdu's آپ mirrors Hindi's aap; use it for respect.",
             "commonMistakes": ["تم with elders", "Wrong helper (ہوں/ہو/ہیں)"]},
            {"concept": "Word order (SOV)",
             "pattern": "subject — object — verb",
             "examples": [{"target": "میں پانی پیتا ہوں", "roman": "maiṁ PAH-nee PEE-tah hooṁ", "gloss": "I water drink"},
                          {"target": "وہ کتاب پڑھتا ہے", "roman": "vuh kih-TAHB PAHR-tah hai", "gloss": "he book reads"},
                          {"target": "ہم گھر جاتے ہیں", "roman": "hum ghur JAH-teh haiṁ", "gloss": "we home go"}],
             "exceptions": ["The verb is last."],
             "learnerNote": "Urdu is nearly identical to Hindi in structure: 'I water drink'.",
             "commonMistakes": ["English word order", "Verb placement"]},
            {"concept": "Present tense — verb + -تا/-تی/-تے + helper",
             "pattern": "-tā (masc.) · -tī (fem.) · -te (pl.) + ہوں/ہو/ہیں",
             "examples": [{"target": "میں کرتا ہوں", "roman": "maiṁ KUR-tah hooṁ", "gloss": "I do (masc.)"},
                          {"target": "میں کرتی ہوں", "roman": "maiṁ KUR-tee hooṁ", "gloss": "I do (fem.)"},
                          {"target": "وہ کرتا ہے", "roman": "vuh KUR-tah hai", "gloss": "he does"}],
             "exceptions": ["The -تا/-تی ending matches gender."],
             "learnerNote": "Same helper-verb system as Hindi.",
             "commonMistakes": ["Wrong gender ending", "Dropping the helper"]},
            {"concept": "Oblique case with postpositions",
             "pattern": "کو (ko) · میں (meṁ) · سے (se) after the noun",
             "examples": [{"target": "گھر میں", "roman": "ghur mehṁ", "gloss": "in the house"},
                          {"target": "اس کو", "roman": "us koh", "gloss": "to him/her"},
                          {"target": "میرے ساتھ", "roman": "MEH-reh sahth", "gloss": "with me"}],
             "exceptions": ["Nouns/pronouns take the oblique form before a postposition."],
             "learnerNote": "Urdu sticks case-markers on nouns where English uses prepositions.",
             "commonMistakes": ["Preposition order", "Forgetting the oblique form"]},
        ],
    },
}


# Stage 5: the remaining 20 starter packs live in tools/langpacks_extra.py
# (authored the same way); merge them so this file stays the single entry point.
import sys
sys.path.insert(0, os.path.join(ROOT, "tools"))
import langpacks_extra
PACKS.update(langpacks_extra.EXTRA_PACKS)


# ---------------------------------------------------------------- build
def build_pack(code, spec):
    items = []
    seen = set()
    for i, (t, r, m, pos, topic) in enumerate(spec["words"]):
        sid = slugify(r) or ("w%02d" % i)
        n = 2
        while ("%s-w-%s" % (code, sid)) in seen:
            sid = slugify(r) + "-%d" % n
            n += 1
        seen.add("%s-w-%s" % (code, sid))
        items.append({"id": "%s-w-%s" % (code, sid), "type": "word", "language": code,
                      "target": t, "roman": r, "meaning": m, "pos": pos, "topic": topic,
                      "level": "beginner"})
    for i, (t, r, m, topic, reg) in enumerate(spec["phrases"]):
        sid = slugify(r) or ("p%02d" % i)
        n = 2
        while ("%s-p-%s" % (code, sid)) in seen:
            sid = slugify(r) + "-%d" % n
            n += 1
        seen.add("%s-p-%s" % (code, sid))
        items.append({"id": "%s-p-%s" % (code, sid), "type": "phrase", "language": code,
                      "target": t, "roman": r, "meaning": m, "topic": topic, "level": "beginner",
                      "register": reg})

    concepts = []
    for i, c in enumerate(spec["concepts"]):
        concepts.append({"id": "%s-%s" % (code, slugify(c["concept"][:28]) or ("c%d" % i)),
                         "concept": c["concept"], "pattern": c["pattern"], "examples": c["examples"],
                         "exceptions": c["exceptions"], "learnerNote": c["learnerNote"],
                         "commonMistakes": c["commonMistakes"], "level": "beginner",
                         "prerequisite": None, "sourceUrl": None, "sourceTitle": None})

    n_words = len(spec["words"])
    n_phr = len(spec["phrases"])
    assert n_words == 24 and n_phr == 12 and len(concepts) == 4, code
    return {
        "version": 1,
        "generated": NOW,
        "source_language": "en",
        "target_language": code,
        "status": "BETA",
        "scope": STD_SCOPE,
        "honestNote": STD_NOTE,
        "about": spec["about"],
        "items": items,
        "concepts": concepts,
    }


def build_manifest():
    # registry gives name/native/script/direction for every code
    reg = json.load(open("reports/language-registry-phase7.json", encoding="utf-8"))
    by_id = {l["id"]: l for l in reg["languages"]}

    pack_files = sorted([f for f in os.listdir("data") if f.startswith("lang-") and f.endswith(".json")])
    packs = []
    for f in pack_files:
        code = f[5:-5]  # lang-XX.json -> XX
        d = json.load(open(os.path.join("data", f), encoding="utf-8"))
        n_words = sum(1 for i in d["items"] if i["type"] == "word")
        n_phr = sum(1 for i in d["items"] if i["type"] == "phrase")
        meta = by_id.get(code, {})
        packs.append({
            "lang": code,
            "name": meta.get("name") or d.get("target_language"),
            "nativeName": meta.get("nativeName") or "",
            "script": meta.get("script") or "",
            "direction": meta.get("direction") or "ltr",
            "speechTag": meta.get("speechTag") or (code + "-" + code.upper()),
            "status": "BETA",
            "scope": d.get("scope", STD_SCOPE),
            "honestNote": STD_NOTE,
            "file": "data/lang-%s.json" % code,
            "counts": {"vocab": n_words, "phrase": n_phr, "grammar": len(d.get("concepts", []))},
        })
    packs.sort(key=lambda p: p["lang"])

    manifest = {
        "version": 1,
        "generated": NOW,
        "purpose": ("Manifest of language packs (§53 Stage 2 + Stage 3 — proof of engine reuse). "
                    "A pack makes a language BETA (starter reference content) — never PRODUCTION. "
                    "PRODUCTION requires a full reviewed course (lessons + practice + quiz + review) "
                    "passing QA in real Chromium; today only Hindi has that."),
        "policy": ("PRODUCTION = full course with browser QA. BETA = authored starter pack rendering "
                   "through the shared engines. PLANNED = registered language with no authored content yet."),
        "packs": packs,
    }
    return manifest


def main():
    for code, spec in PACKS.items():
        path = "data/lang-%s.json" % code
        with open(path, "w", encoding="utf-8") as f:
            json.dump(build_pack(code, spec), f, ensure_ascii=False, indent=2)
        print("  wrote", path)

    manifest = build_manifest()
    with open("data/language-packs.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print("  wrote data/language-packs.json (%d packs)" % len(manifest["packs"]))


if __name__ == "__main__":
    main()

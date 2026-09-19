#!/usr/bin/env python3
"""Fix the wrong-language A1 scaffolds. WHY THIS FILE EXISTS (2026-09-19)

The phase-3 A1 files for 19 languages were built on top of the SPANISH
template: their lesson vocabulary is in the correct language, but the
`alphabet` block says "The Spanish alphabet: 27 letters" and `counting`
runs cero, uno, dos, tres, … — Spanish words printed on, e.g., the Somali,
Ukrainian or Vietnamese pages. A learner on that page is told the wrong
alphabet and the wrong numbers for their own language, which is exactly the
"wrong target language" failure the course audit exists to catch.

This tool replaces ONLY the two scaffold blocks with real, hand-checked
data for each affected language. Lesson units, dialogues and practice in
those files are untouched.

Run:  python3 tools/fix-a1-scaffolds.py [--check]

It is idempotent: a file whose scaffold already matches its language is
reported as ok and not rewritten.
"""
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
REPORT = "data/audit/fix-a1-scaffolds.json"

SPANISH_TITLE = "The Spanish alphabet"
SPANISH_ZERO = {"cero", "0"}


def L(t, r, tip=""):
    return {"t": t, "r": r, "tip": tip}


def N(t, r, en):
    return {"t": t, "r": r, "en": en}


# ---------------------------------------------------------------------------
# Real alphabet + counting data, one entry per affected language.
# Letters carry the letter, its name/say-it and (where useful) a tip.
# Numbers are 0-15, the range the Spanish template used.
# ---------------------------------------------------------------------------
S = {}

S["af"] = {
    "alphabet": {
        "title": "The Afrikaans alphabet: 26 letters",
        "explain": ("Afrikaans writes in the ordinary Latin alphabet and, like "
                    "English, spells almost exactly what it says: short vowels, "
                    "one sound per letter, double consonants. The surprises are "
                    "few — the main one is J, which is pronounced like the H in "
                    "hello."),
        "letters": [
            L("a", "ah", "short, as in father"), L("b", "beh", ""),
            L("c", "seh", ""), L("d", "deh", ""), L("e", "eh", "short, as in met"),
            L("f", "ef", ""), L("g", "geh", "soft g, as in get"),
            L("h", "hah", ""), L("i", "ee", "long i"), L("j", "jah", "sounds like English H"),
            L("k", "kah", ""), L("l", "el", ""), L("m", "em", ""),
            L("n", "en", ""), L("o", "oh", "short o"), L("p", "peh", ""),
            L("q", "ku", "only in borrowed words"), L("r", "er", "lightly rolled"),
            L("s", "es", ""), L("t", "teh", ""), L("u", "oo", "long u"),
            L("v", "veh", ""), L("w", "weh", ""), L("x", "iks", "in borrowed words"),
            L("y", "wye", "vowel or y-sound"), L("z", "zet", "")
        ]
    },
    "counting": {
        "title": "Counting in Afrikaans: 0 to 15",
        "explain": "Learn 0-10 by heart, then build the rest: eleven and up is tien + the number (elf is the irregular one).",
        "numbers": [
            N("nul", "noo-l", "0"), N("een", "een", "1"), N("twee", "tweh", "2"),
            N("drie", "dree", "3"), N("vier", "fee-er", "4"), N("vyf", "veef", "5"),
            N("ses", "sehss", "6"), N("sewe", "sehwuh", "7"), N("agt", "aght", "8"),
            N("nege", "neguh", "9"), N("tien", "teen", "10"), N("elf", "elf", "11"),
            N("twaalf", "twaolf", "12"), N("dertien", "derteen", "13"),
            N("veertien", "foorteen", "14"), N("vyftien", "veefteen", "15")
        ],
        "rules": [
            "Vowels are single and short: a=ah, e=eh, i=ee, o=oh, u=oo.",
            "J is always the H sound: jaar is pronounced yah-er.",
            "Double consonants make the previous vowel short: bad (badd) vs baat (baht)."
        ]
    }
}

S["ca"] = {
    "alphabet": {
        "title": "The Catalan alphabet: 26 letters plus Ç",
        "explain": ("Catalan uses the Latin alphabet with one letter of its own: Ç "
                    "(c cedi), which is always pronounced S. Unlike Spanish or "
                    "Italian, final consonants are pronounced, so the t in "
                    "cattre (bed) is there."),
        "letters": [
            L("a", "ah", "pure, as in father"), L("b", "beh", "soft, lips touch"),
            L("c", "seh", "s before e/i, otherwise k"), L("ç", "s", "always s: plaça"),
            L("d", "deh", "soft, almost th"), L("e", "eh", "short e"),
            L("f", "ef", "silent at the end of a word"), L("g", "geh", "soft g"),
            L("h", "ah-tchah", "always silent"), L("i", "ee", "long i"),
            L("j", "yoh-tah", "gargled, as in loch"), L("k", "kah", "borrowed words"),
            L("l", "eh-lah", "ll = y-sound"), L("m", "ehm", ""), L("n", "eh-neh", ""),
            L("o", "oh", "pure o"), L("p", "pah", ""), L("q", "kuh", "with u: que"),
            L("r", "ehr", "tapped; rr rolled"), L("s", "ess", ""),
            L("t", "teh", "pronounced even at the end"), L("u", "oo", "long u"),
            L("v", "veh", "sounds like b"), L("w", "dobl-vi", "borrowed words"),
            L("x", "eeks", "ks in text; sh in words"), L("y", "ee-psee-lloh", "y = ee in yema"),
            L("z", "seh", "s or th, by region")
        ]
    },
    "counting": {
        "title": "Counting in Catalan: 0 to 15",
        "explain": "One is u (o). Eleven and twelve are their own words; thirteen and up is deu + the number.",
        "numbers": [
            N("zero", "seh-roh", "0"), N("u", "oh", "1"), N("dos", "dohss", "2"),
            N("tres", "trahss", "3"), N("quatre", "kwah-truh", "4"), N("cinc", "seenk", "5"),
            N("sis", "seess", "6"), N("set", "shtett", "7"), N("vuit", "booett", "8"),
            N("nou", "nooh", "9"), N("deu", "doh", "10"), N("onze", "ohn-tseh", "11"),
            N("dotze", "dohrtseh", "12"), N("tretze", "trertseh", "13"),
            N("catorze", "kah-tor-tseh", "14"), N("quinze", "keentseh", "15")
        ],
        "rules": [
            "Vowels never change: a e i o u, always the same sound.",
            "Final -t is pronounced: tres, catorze, dotze.",
            "J is the guttural H (loch); ll and i/y make the Y sound."
        ]
    }
}

S["el"] = {
    "alphabet": {
        "title": "The Greek alphabet: 24 letters",
        "explain": ("Greek uses its own 24-letter alphabet; you already met it "
                    "in π and Ω. Every letter has a name you will use when "
                    "spelling your name or a phone number out loud."),
        "letters": [
            L("α", "alfa", ""), L("β", "beta", "sounds like v"), L("γ", "gamma", "g or ng"),
            L("δ", "delta", "soft, like th in this"), L("ε", "epsilon", "short e"),
            L("ζ", "zeta", ""), L("η", "eta", "long e: eh"), L("θ", "theta", "th as in thin"),
            L("ι", "iota", "short i"), L("κ", "kappa", ""), L("λ", "lambda", "l"),
            L("μ", "mi", ""), L("ν", "ni", ""), L("ξ", "ksi", "x sound: ex-act"),
            L("ο", "omicron", "short o"), L("π", "pi", ""), L("ρ", "ro", "slight r"),
            L("σ/ς", "sigma", "at word end sigma is written ς, e.g. αθλητής ends in ς"),
            L("τ", "tau", "t"), L("υ", "ipsilon", "short u"),
            L("φ", "fi", "sounds like f"), L("χ", "chi", "kh, as in loch"),
            L("ψ", "psi", "ps"), L("ω", "omega", "long o")
        ]
    },
    "counting": {
        "title": "Counting in Greek: 0 to 15",
        "explain": "Learn 0-10 by heart. Eleven and twelve are their own words; thirteen and up is deka + the number.",
        "numbers": [
            N("μηδέν", "yee-theh-NEN", "0"), N("ένα", "EE-no", "1"), N("δύο", "DEE-o", "2"),
            N("τρία", "tree-A", "3"), N("τέσσερα", "TEH-seh-ro", "4"), N("πέντε", "PEHN-te", "5"),
            N("έξι", "EH-ksi", "6"), N("εφτά", "ef-TA", "7"), N("οκτώ", "ok-TO", "8"),
            N("εννιά", "en-YA", "9"), N("δέκα", "DEH-ka", "10"), N("έντεκα", "EN-teh-ka", "11"),
            N("δώδεκα", "DOD-eh-ka", "12"), N("δεκατρία", "deh-ka-REE-a", "13"),
            N("δεκατέσσερα", "deh-ka-TEH-seh-ro", "14"), N("δεκαπέντε", "deh-ka-PEHN-te", "15")
        ],
        "rules": [
            "Every syllable ends in a vowel or n; Greek has no silent letters.",
            "θ φ χ are the sounds English keeps only in th, f, loch.",
            "The stress mark is on one vowel of every word — it tells you where to push."
        ]
    }
}

S["en"] = {
    "alphabet": {
        "title": "The English alphabet: 26 letters",
        "explain": ("The alphabet you are reading now. Two notes for learners: "
                    "the same letter can carry several sounds (the a in cake vs "
                    "cat), and a few letters are silent in common words (the k in "
                    "knife). You already know it — the rest of this course is "
                    "about the sounds it makes."),
        "letters": [
            L("a", "ay", "cake vs cat"), L("b", "bee", ""), L("c", "see", "k in cat, s in city"),
            L("d", "dee", ""), L("e", "ee", "bed vs meet"), L("f", "eff", ""),
            L("g", "gee", "get vs guitar"), L("h", "aitch", ""), L("i", "eye", "sit vs site"),
            L("j", "jay", ""), L("k", "kay", ""), L("l", "el", ""), L("m", "em", ""),
            L("n", "en", ""), L("o", "oh", "hot vs goat"), L("p", "pee", ""),
            L("q", "cue", "always with u"), L("r", "ar", "varies by region"),
            L("s", "ess", "s in sun, sh in ship"), L("t", "tee", "t in time, ch in church"),
            L("u", "you", "cup vs cute"), L("v", "vee", ""), L("w", "double-u", "w vs wh"),
            L("x", "ex", "ex-act, box"), L("y", "why", "yes vs gym"), L("z", "zed/zee", "")
        ]
    },
    "counting": {
        "title": "Counting in English: 0 to 15",
        "explain": "Learn 0-12 by heart — eleven, twelve and thirteen keep their old shapes; from fourteen the pattern ten + number holds.",
        "numbers": [
            N("zero", "ZEH-roh", "0"), N("one", "wun", "1"), N("two", "too", "2"),
            N("three", "tree", "3"), N("four", "fawr", "4"), N("five", "fiv", "5"),
            N("six", "siks", "6"), N("seven", "SEV-uhn", "7"), N("eight", "eyt", "8"),
            N("nine", "nyn", "9"), N("ten", "ten", "10"), N("eleven", "EL-uh-ven", "11"),
            N("twelve", "twer-v", "12"), N("thirteen", "THIR-teen", "13"),
            N("fourteen", "FOR-teen", "14"), N("fifteen", "FIF-teen", "15")
        ],
        "rules": [
            "Stress falls on the first syllable of compound numbers: THIR-teen, not three-TEEN.",
            "Th has two sounds: thin (sharp) vs this (soft).",
            "R is optional in many accents — listen to British and American speakers and both are normal."
        ]
    }
}

S["fa"] = {
    "alphabet": {
        "title": "The Persian alphabet: 32 letters, right to left",
        "explain": ("Persian writes right to left in an alphabet descended from "
                    "Arabic's, with four extra letters for sounds Persian needs. "
                    "There are no capital letters, and letters change shape "
                    "depending on their neighbours."),
        "letters": [
            L("ا", "alef (ā)", "long a"), L("آ", "alef with madda", "long ā: آب"),
            L("ب", "be", "b"), L("پ", "pe", "p — Persian's own"), L("ت", "te", "t"),
            L("ث", "se", "th, in Arabic words"), L("ج", "jim", "j"), L("چ", "che", "ch — Persian's own"),
            L("ح", "he", "breathy h"), L("خ", "khe", "kh, as in loch"), L("د", "de", "d"),
            L("ذ", "ze", "dh, in Arabic words"), L("ر", "re", "r"), L("ز", "ze", "z"),
            L("ژ", "je", "zh — Persian's own"), L("س", "sin", "s"), L("ش", "shin", "sh"),
            L("ط", "to", "t"), L("ظ", "zo", "z"), L("ع", "aye", "deep throat sound"),
            L("غ", "ghayn", "dark g"), L("ف", "fe", "f"), L("ق", "ghaf", "deep k, not q"),
            L("ک", "kaf", "k"), L("گ", "gaf", "g — Persian's own"), L("ل", "lam", "l"),
            L("م", "mim", "m"), L("ن", "nun", "n"), L("و", "vav", "o / v / u"),
            L("ه", "he", "h or long e"), L("ی", "ye", "i / y")
        ]
    },
    "counting": {
        "title": "Counting in Persian: 0 to 15",
        "explain": "Eleven and up is dah (ten) + the number, fused: dah-yazda… — in practice yazda (11) and daazda (12) are their own words, then seзда, chaharda, panzada.",
        "numbers": [
            N("صفر", "sifr", "0"), N("یک", "yak", "1"), N("دو", "do", "2"),
            N("سه", "se", "3"), N("چهار", "chahar", "4"), N("پنج", "panj", "5"),
            N("شش", "shesh", "6"), N("هفت", "haft", "7"), N("هشت", "hesht", "8"),
            N("نه", "nah", "9"), N("ده", "dah", "10"), N("یازده", "yazdeh", "11"),
            N("دوازده", "daazdeh", "12"), N("سیزده", "sezdah", "13"),
            N("چهارده", "chahardah", "14"), N("پانزده", "panzdah", "15")
        ],
        "rules": [
            "ق is a deep k, not the English q; گ is a plain g.",
            "Persian has three e-vowels and two o-vowels — the difference is real, not a spelling quirk.",
            "There is no letter for the w sound; و (vav) does the work."
        ]
    }
}

S["fil"] = {
    "alphabet": {
        "title": "The Filipino alphabet: 26 letters plus the glottal stop",
        "explain": ("Filipino writes in the Latin alphabet, but the alphabet "
                    "officially taught in schools runs a to z without j, v, w, x "
                    "and y except in borrowed words — and it adds the glottal "
                    "stop (written ʼ) as a real letter of the language."),
        "letters": [
            L("a", "ah", ""), L("b", "be", ""), L("c", "se", "always k: bata, kumusta"),
            L("d", "de", ""), L("e", "eh", ""), L("g", "ge", "always g: gato"),
            L("h", "aitch", "silent; marks the glottal stop: taʼo"), L("i", "ee", ""),
            L("k", "ka", ""), L("l", "el", ""), L("m", "em", ""), L("n", "en", ""),
            L("o", "oh", ""), L("p", "pe", ""), L("r", "er", "tapped"),
            L("s", "es", ""), L("t", "te", ""), L("u", "oo", ""),
            L("w", "double-u", "borrowed words"), L("y", "ye", "y-sound: yelo")
        ]
    },
    "counting": {
        "title": "Counting in Filipino: 0 to 15",
        "explain": "Learn 0-10 by heart. Eleven and up is labing-/labin- + the number below ten.",
        "numbers": [
            N("cero", "seh-roh", "0"), N("isa", "ee-sah", "1"), N("dalawa", "dah-LAH-wah", "2"),
            N("tatlo", "TAHT-loh", "3"), N("apat", "ah-PAHT", "4"), N("lima", "LEE-mah", "5"),
            N("anim", "ah-NEEM", "6"), N("pitô", "PEE-toh", "7"), N("walo", "WAH-loh", "8"),
            N("siyam", "SEE-yam", "9"), N("disyete", "dee-SYE-teh", "10"),
            N("labing-siyam", "LAH-beeng SEE-yam", "11"), N("labing-walo", "LAH-beeng WAH-loh", "12"),
            N("labing-pitô", "LAH-beeng PEE-toh", "13"), N("labing-anim", "LAH-beeng ah-NEEM", "14"),
            N("labing-lima", "LAH-beeng LEE-mah", "15")
        ],
        "rules": [
            "All five vowels are pure: a e i o u, never diphthongs.",
            "Final consonants drop in casual speech: bata sounds like bah-tah.",
            "The glottal stop is real: taʼo (to be) is not tao (person)."
        ]
    }
}

S["ht"] = {
    "alphabet": {
        "title": "The Haitian Creole alphabet: 26 letters, three nasal vowels",
        "explain": ("Haitian Creole (Kreyòl) writes in the Latin alphabet with a "
                    "few spelling habits of its own: the apostrophe (wouf) is a "
                    "real sound, and an n before a vowel marks nasal vowels "
                    "(an, en, on, in, ou)."),
        "letters": [
            L("a", "ah", "short a"), L("b", "be", ""), L("ch", "sh", "one letter: chaj"),
            L("d", "de", ""), L("e", "eh", "short e"), L("f", "ef", ""),
            L("g", "je", "always the soft g"), L("h", "aitch", "silent"), L("i", "ee", ""),
            L("j", "zh", "zh sound: jou"), L("k", "ka", ""), L("l", "el", ""),
            L("m", "em", ""), L("n", "en", ""), L("o", "oh", "short o"),
            L("p", "pe", ""), L("r", "er", "slight r"), L("s", "es", ""),
            L("t", "te", ""), L("v", "ve", ""), L("w", "we", "the glottal stop: wouf"),
            L("y", "ye", "")
        ]
    },
    "counting": {
        "title": "Counting in Haitian Creole: 0 to 15",
        "explain": "Eleven and up are their own words: onz (11), douz (12), trèz (13), katòz (14), kinz (15) — once you know them, the pattern above does the rest.",
        "numbers": [
            N("zero", "zeh-ro", "0"), N("yon", "yon", "1"), N("de", "de", "2"),
            N("twa", "twah", "3"), N("kat", "katt", "4"), N("senk", "senk", "5"),
            N("sèt", "sett", "6"), N("uit", "weet", "7"), N("nen", "nen", "8"),
            N("dis", "deess", "9"), N("dis", "deess", "10 — same word, context decides"),
            N("onz", "ohnz", "11"), N("douz", "dooz", "12"), N("trèz", "trehz", "13"),
            N("katòz", "kah-tohz", "14"), N("kinz", "keenz", "15")
        ],
        "rules": [
            "Nasal vowels: an, en, in, on, ou — the air leaves through the nose.",
            "Stress almost always falls on the last syllable.",
            "The w is pronounced like the English h in hmm — a stop in the throat."
        ]
    }
}

S["id"] = {
    "alphabet": {
        "title": "The Indonesian alphabet: 26 letters, five pure vowels",
        "explain": ("Indonesian uses the Latin alphabet exactly as it appears in "
                    "English, with five vowels that are always pure (a e i o u) "
                    "and no letter that changes its mind. If you can read it, "
                    "you can say it."),
        "letters": [
            L("a", "ah", "pure a"), L("b", "be", ""), L("c", "se", "always k: coba"),
            L("d", "de", ""), L("e", "eh/é", "schwa in the middle: baca = ba-ca"),
            L("f", "ef", ""), L("g", "ge", "always a hard g"), L("h", "haitch", ""),
            L("i", "ee", ""), L("j", "zh", "zh sound: jari"), L("k", "ka", ""),
            L("l", "el", ""), L("m", "em", ""), L("n", "en", ""), L("o", "oh", "pure o"),
            L("p", "pe", ""), L("q", "ku", "borrowed words"), L("r", "er", "tapped"),
            L("s", "es", ""), L("t", "te", ""), L("u", "oo", ""), L("v", "ve", ""),
            L("w", "we", ""), L("x", "iks", "borrowed words"), L("y", "ye", "")
        ]
    },
    "counting": {
        "title": "Counting in Indonesian: 0 to 15",
        "explain": "Learn 0-12 by heart. Thirteen and up is the number + belas: tiga belas, empat belas, lima belas.",
        "numbers": [
            N("nol", "nohl", "0"), N("satu", "SAH-too", "1"), N("dua", "doo-AH", "2"),
            N("tiga", "TEE-gah", "3"), N("empat", "EHM-patt", "4"), N("lima", "LEE-mah", "5"),
            N("enam", "eh-NAHM", "6"), N("tujuh", "too-JOOH", "7"), N("delapan", "deh-LAH-pahn", "8"),
            N("sembilan", "sem-BEE-lahn", "9"), N("sepuluh", "seh-POO-luuh", "10"),
            N("sebelas", "seh-BEH-lahss", "11"), N("dua belas", "doo-AH BEH-lahss", "12"),
            N("tiga belas", "TEE-gah BEH-lahss", "13"), N("empat belas", "EHM-patt BEH-lahss", "14"),
            N("lima belas", "LEE-mah BEH-lahss", "15")
        ],
        "rules": [
            "Stress falls on the second-to-last syllable: se-PU-luh."
            "Every syllable is open (consonant + vowel), so words sound even and rhythmical.",
            "The middle e is a short schwa: rumah = roo-mah, not roo-meh."
        ]
    }
}

S["kk"] = {
    "alphabet": {
        "title": "The Kazakh alphabet: 42 letters in Cyrillic",
        "explain": ("Kazakh writes in Cyrillic with nine letters of its own "
                    "(Ә ә, Ғ ғ, Қ қ, Ң ң, Ө ө, Ұ ұ, Ү ү, Һ һ, І і). The new vowels "
                    "are the key: Kazakh vowels come in front and back pairs, "
                    "and the suffixes that follow must match."),
        "letters": [
            L("А а", "a", ""), L("Ә ә", "ä", "a as in about"), L("Б б", "b", ""),
            L("В в", "v", ""), L("Г г", "g", ""), L("Ғ ғ", "gh", "breathy g"),
            L("Д д", "d", ""), L("Е е", "e", ""), L("Ё ё", "yo", ""),
            L("Ж ж", "zh", ""), L("З з", "z", ""), L("И и", "i", ""),
            L("І і", "i (long)", "long i: іш"), L("Й й", "y", ""),
            L("К к", "k", ""), L("Қ қ", "q", "deep k from the back of the throat"),
            L("Л л", "l", ""), L("М м", "m", ""), L("Н н", "n", ""),
            L("Ң ң", "ng", "the nasal ng as in sing"), L("О о", "o", ""),
            L("Ө ө", "ö", "rounded ä"), L("П п", "p", ""), L("Р р", "r", "rolled"),
            L("С с", "s", ""), L("Т т", "t", ""), L("У у", "u", ""),
            L("Ұ ұ", "u (short)", "short u"), L("Ү ү", "ü", "rounded ee"),
            L("Ф ф", "f", ""), L("Х х", "h", "like loch"), L("Һ һ", "h (soft)", ""),
            L("Ц ц", "ts", ""), L("Ч ч", "ch", ""), L("Ш ш", "sh", ""),
            L("Щ щ", "shch", ""), L("Ъ ъ", "hard sign", ""), L("Ы ы", "y", "deep i"),
            L("Ь ь", "soft sign", ""), L("Э э", "e", ""), L("Ю ю", "yu", ""),
            L("Я я", "ya", "")
        ]
    },
    "counting": {
        "title": "Counting in Kazakh: 0 to 15",
        "explain": "Eleven and up is on (ten) + the number: on bir, on eki, on үsh.",
        "numbers": [
            N("нөл", "nöl", "0"), N("бір", "bır", "1"), N("екі", "egı", "2"),
            N("үш", "üş", "3"), N("төрт", "tört", "4"), N("бес", "bes", "5"),
            N("алты", "alty", "6"), N("жеті", "jetı", "7"), N("сегіз", "segız", "8"),
            N("тоғыз", "toğyz", "9"), N("он", "on", "10"), N("он бір", "on bır", "11"),
            N("он екі", "on egı", "12"), N("он үш", "on üsh", "13"),
            N("он төрт", "on tört", "14"), N("он бес", "on bes", "15")
        ],
        "rules": [
            "Vowel harmony: back vowels (a o u ı) take back suffixes; front vowels (ä e i ö ü) take front ones.",
            "Қ қ is a deep throat k — it has no English equivalent, but Arabic and Hebrew speakers know it.",
            "ң ң is the ng of sing; it sits after a vowel and before a consonant."
        ]
    }
}

S["nl"] = {
    "alphabet": {
        "title": "The Dutch alphabet: 26 letters",
        "explain": ("Dutch uses the Latin alphabet with two house rules: G and "
                    "CH are the same gargled sound, and the digraphs IJ and UI "
                    "behave like a single long vowel."),
        "letters": [
            L("a", "ah", "as in father"), L("b", "bh", "soft b"), L("c", "seh", "k in cat"),
            L("d", "dh", "soft, lips part"), L("e", "eh", "short e"), L("f", "ef", ""),
            L("g", "gh", "gargle: goed"), L("h", "hah", ""), L("i", "ee", "long i"),
            L("j", "ay", "y-sound: ja"), L("k", "kah", ""), L("l", "el", ""),
            L("m", "em", ""), L("n", "en", ""), L("o", "oh", "short o"),
            L("p", "ph", "soft p"), L("q", "ku", "with u: qualiteit"), L("r", "er", "uvular"),
            L("s", "es", ""), L("t", "th", "soft t"), L("u", "oo", "long u"),
            L("v", "vh", "soft, like f"), L("w", "weh", "w"), L("x", "iks", "borrowed words"),
            L("y", "wie", "borrowed words"), L("z", "eh-tseh", "")
        ]
    },
    "counting": {
        "title": "Counting in Dutch: 0 to 15",
        "explain": "Learn 0-12 by heart. Thirteen and up is the number + tien: dertien, veertien, vijftien.",
        "numbers": [
            N("nul", "noo-l", "0"), N("een", "een", "1"), N("twee", "tweh", "2"),
            N("drie", "dree", "3"), N("vier", "fee-er", "4"), N("vijf", "veef", "5"),
            N("zes", "zehss", "6"), N("zeven", "ZEH-ven", "7"), N("acht", "akht", "8"),
            N("negen", "NEH-gen", "9"), N("tien", "teen", "10"), N("elf", "elf", "11"),
            N("twaalf", "twaolf", "12"), N("dertien", "derteen", "13"),
            N("veertien", "foorteen", "14"), N("vijftien", "veefteen", "15")
        ],
        "rules": [
            "G and CH are the same gargled sound — the one tourists hear and locals love.",
            "IJ and UI are long vowels: wij (we) has the ee of machine, and huis (house) rhymes with it."
            "Final consonants are often voiced: niet (not) ends with a soft d-like sound."
        ]
    }
}

S["pl"] = {
    "alphabet": {
        "title": "The Polish alphabet: 24 letters, eight with diacritics",
        "explain": ("Polish uses the Latin alphabet plus eight letters with "
                    "marks: ą ć ę ł ń ó ś ź ż. The marks change the sound — "
                    "ś is s, ź is z with a soft tongue, and ł is the w of wine."),
        "letters": [
            L("a", "ah", ""), L("ą", "ong", "nasal a: łąka"), L("b", "bh", ""),
            L("c", "ts", "ts as in cats"), L("ć", "ts (soft)", "ts with a soft tongue: ćma"),
            L("d", "d", ""), L("e", "eh", "short e"), L("ę", "eng", "nasal e: ręka"),
            L("f", "ef", ""), L("g", "g", "always a hard g"), L("h", "h", "borrowed words"),
            L("i", "ee", ""), L("j", "y", "y-sound: ja"), L("k", "k", ""),
            L("l", "l", ""), L("ł", "w", "w-sound: łza"), L("m", "m", ""),
            L("n", "n", ""), L("ń", "n (soft)", "soft n: ńoc"), L("o", "oh", "short o"),
            L("p", "p", ""), L("r", "r", "rolled, with the tongue"), L("s", "s", ""),
            L("ś", "s (soft)", "s with a soft tongue: śnieg"), L("t", "t", ""),
            L("u", "oo", ""), L("w", "v", "v-sound: woda"), L("y", "ee", "after consonants: syn"),
            L("z", "z", ""), L("ź", "z (soft)", "soft z: źrebię"), L("ż", "zh", "zh: żaba")
        ]
    },
    "counting": {
        "title": "Counting in Polish: 0 to 15",
        "explain": "Learn 0-12 by heart. Thirteen and up is the number + -naście: trzynaście, czternaście, piętnaście.",
        "numbers": [
            N("zero", "zeh-ro", "0"), N("jeden", "YE-den", "1"), N("dwa", "dva", "2"),
            N("trzy", "tshi", "3"), N("cztery", "CHTih-rih", "4"), N("pięć", "pents", "5"),
            N("sześć", "shets", "6"), N("siedem", "SEE-dem", "7"), N("osiem", "OHS-yem", "8"),
            N("dziewięć", "dyev-ents", "9"), N("dziesięć", "dyeh-sets", "10"),
            N("jedenaście", "yeh-deh-NAHS-tsih", "11"), N("dwanaście", "dva-NAHS-tsih", "12"),
            N("trzynaście", "tshi-NAHS-tsih", "13"), N("czternaście", "CHter-NAHS-tsih", "14"),
            N("piętnaście", "pent-NAHS-tsih", "15")
        ],
        "rules": [
            "Consonant clusters are normal: wstrzymać (to stop) starts with five consonants in a row.",
            "ł is English w; ź ż ś c are soft variants of z s and ts.",
            "Stress falls on the second-to-last syllable: dwa-NA-scie, trze-NA-scie."
        ]
    }
}

S["ro"] = {
    "alphabet": {
        "title": "The Romanian alphabet: 24 letters, four with diacritics",
        "explain": ("Romanian uses the Latin alphabet with four marked letters: "
                    "ă (the schwa), î and â (long ă, depending on position), and "
                    "ș ț (the s and t of English measure, with the mark "
                    "historically under the letter)."),
        "letters": [
            L("a", "ah", ""), L("ă", "schwa", "uh: mamă"), L("b", "bh", ""),
            L("c", "ts", "ts before e/i: cer; otherwise k: cal"), L("d", "d", ""),
            L("e", "eh", "short e"), L("f", "ef", ""), L("g", "g", ""),
            L("h", "h", "always silent: har"), L("i", "ee", ""), L("î", "uh (long)", "start of words: înainte"),
            L("j", "zh", "zh: joc (game)"), L("k", "k", "borrowed words"),
            L("l", "l", ""), L("m", "m", ""), L("n", "n", ""), L("o", "oh", ""),
            L("p", "p", ""), L("r", "r", "rolled"), L("s", "s", ""),
            L("ș", "s", "s: șoarece (mouse)"), L("t", "t", ""),
            L("ț", "t", "t: țipăt (shriek)"), L("u", "oo", ""), L("v", "v", "")
        ]
    },
    "counting": {
        "title": "Counting in Romanian: 0 to 15",
        "explain": "Eleven and up is zece (ten) + the number below ten, fused: unsprezece, doisprezece, treisprezece, paisprezece, cincisprezece.",
        "numbers": [
            N("zero", "zeh-ro", "0"), N("un", "oon", "1"), N("doi", "doy", "2"),
            N("trei", "treh", "3"), N("patru", "pah-troo", "4"), N("cinci", "tcheen-tshee", "5"),
            N("șase", "shah-seh", "6"), N("șapte", "shahp-teh", "7"), N("opt", "ohpt", "8"),
            N("nouă", "noo-AH", "9"), N("zece", "zeh-tseh", "10"),
            N("unsprezece", "oon-spreh-ZEH-tseh", "11"), N("doisprezece", "doy-spreh-ZEH-tseh", "12"),
            N("treisprezece", "treh-spreh-ZEH-tseh", "13"), N("paisprezece", "pah-spreh-ZEH-tseh", "14"),
            N("cincisprezece", "tcheen-tshee-spreh-ZEH-tseh", "15")
        ],
        "rules": [
            "ă is the schwa (uh) — the most common vowel in Romanian.",
            "Final -e is very light: bine (well) ends with a nearly silent e."
            "ș and ț are just s and t with the historical mark; modern type often puts it above."
        ]
    }
}

S["so"] = {
    "alphabet": {
        "title": "The Somali alphabet: 26 letters, no silent letters",
        "explain": ("Somali's Latin alphabet is famously honest: every letter "
                    "is pronounced, no letter is silent, and the five vowels "
                    "come in short and long pairs (a/aa, e/ee, i/ii, o/oo, "
                    "u/uu) where the length changes the meaning."),
        "letters": [
            L("a", "ah", "long when doubled: aad"), L("b", "be", ""),
            L("d", "de", ""), L("dh", "d + h", "the dh of this: dhaqan"),
            L("e", "eh", ""), L("f", "ef", ""), L("g", "ge", ""),
            L("h", "h", ""), L("i", "ee", ""), L("j", "zh", "zh: jir (age)"),
            L("k", "ka", ""), L("kh", "k + h", "kh, as in loch: khayaal"),
            L("l", "el", ""), L("m", "em", ""), L("n", "en", ""),
            L("o", "oh", ""), L("p", "pe", ""), L("q", "qof", "the deep throat q: qof (person)"),
            L("r", "er", "slight r"), L("s", "es", ""),
            L("sh", "s + h", "sh: shan (five)"), L("t", "te", ""),
            L("u", "oo", ""), L("v", "ve", ""), L("w", "we", ""),
            L("y", "ye", "")
        ]
    },
    "counting": {
        "title": "Counting in Somali: 0 to 15",
        "explain": ("Somali builds numbers from its blocks: 6-9 is shan (5) + the "
                    "number below it, 10 is laba iyo toban, and 11-15 is that "
                    "same ten + the number. Once you see the pattern you can "
                    "count as far as you like."),
        "numbers": [
            N("jeerom", "yeer-o-m", "0"), N("hal", "hahl", "1"), N("labo", "lah-bo", "2"),
            N("saddex", "sah-deks", "3"), N("afar", "ah-fahr", "4"), N("shan", "shahn", "5"),
            N("shan iyo laba", "shahn ee-yo LAH-bo", "6"), N("shan iyo saddex", "shahn ee-yo SAH-deks", "7"),
            N("shan iyo afar", "shahn ee-yo AH-fahr", "8"), N("shan iyo shan", "shahn ee-yo SHAHN", "9"),
            N("laba iyo toban", "LAH-bo ee-yo TOH-bahn", "10"),
            N("laba iyo toban iyo hal", "… TOH-bahn ee-yo HAHHL", "11"),
            N("laba iyo toban iyo labo", "… TOH-bahn ee-yo LAH-bo", "12"),
            N("laba iyo toban iyo saddex", "… TOH-bahn ee-yo SAH-deks", "13"),
            N("laba iyo toban iyo afar", "… TOH-bahn ee-yo AH-fahr", "14"),
            N("laba iyo toban iyo shan", "… TOH-bahn ee-yo SHAHN", "15")
        ],
        "rules": [
            "There are no silent letters — the word is exactly what it looks like.",
            "Vowel length matters: hal (one) vs haal? the long vowel is real.",
            "The deep throat q (qof) is written with q: qof (person)."
        ]
    }
}

S["sw"] = {
    "alphabet": {
        "title": "The Swahili alphabet: 26 letters",
        "explain": ("Swahili (Kiswahili) uses the Latin alphabet and writes "
                    "almost exactly what it says: every syllable is a "
                    "consonant plus a vowel, and vowels come in pairs (a aa, "
                    "e ee, i ii, o oo, u uu) where the long vowel is "
                    "doubled."),
        "letters": [
            L("a", "ah", "long: aa — sana"), L("b", "be", ""), L("c", "ts", "the c of click languages; see the click drills"),
            L("d", "de", ""), L("e", "eh", "short e"), L("f", "ef", ""),
            L("g", "ge", ""), L("h", "haitch", ""), L("i", "ee", ""),
            L("j", "zh", "zh: jua (sun)"), L("k", "ka", ""), L("l", "el", ""),
            L("m", "em", ""), L("n", "en", ""), L("o", "oh", "short o"),
            L("p", "pe", ""), L("q", "click (q)", "the back click — in some dialects of the c family"),
            L("r", "er", "slight r"), L("s", "es", ""), L("t", "te", ""),
            L("u", "oo", ""), L("v", "ve", ""), L("w", "we", ""), L("x", "kh (x)", "kh — the x of click dialects"),
            L("y", "ye", "")
        ]
    },
    "counting": {
        "title": "Counting in Swahili: 0 to 15",
        "explain": "Eleven and up is kumi (ten) + na + the number: kumi na moja, kumi na mbili, kumi na tatu.",
        "numbers": [
            N("sifuri", "see-FOO-ree", "0"), N("moja", "MOH-jah", "1"), N("mbili", "M-EE-lee", "2"),
            N("tatu", "TAH-too", "3"), N("nne", "n-nuh", "4"), N("tano", "TAH-noh", "5"),
            N("sita", "SEE-tah", "6"), N("saba", "SAH-bah", "7"), N("nane", "NAH-nuh", "8"),
            N("tisa", "TEE-sah", "9"), N("kumi", "KOO-mee", "10"),
            N("kumi na moja", "KOO-mee nah MOH-jah", "11"), N("kumi na mbili", "KOO-mee nah M-EE-lee", "12"),
            N("kumi na tatu", "KOO-mee nah TAH-too", "13"), N("kumi na nne", "KOO-mee nah n-nuh", "14"),
            N("kumi na tano", "KOO-mee nah TAH-noh", "15")
        ],
        "rules": [
            "Every syllable is C+V, so the rhythm is perfectly even: MO-ha, KOO-mee.",
            "Long vowels are written doubled: saa (hour) is long; tano (five) is short."
            "The final -a on verbs is real: to speak is kusema, I speak is nina-sema."
        ]
    }
}

S["tr"] = {
    "alphabet": {
        "title": "The Turkish alphabet: 29 letters",
        "explain": ("Turkish uses the Latin alphabet with three letters of its "
                    "own: Ğ (soft g), İ (capital i with a dot) and Ş (sharp s) — "
                    "and one vowel most alphabets never meet: ı, the i without "
                    "a dot."),
        "letters": [
            L("a", "a", "short, open"), L("b", "be", ""), L("c", "che", "ch as in chair"),
            L("d", "de", ""), L("e", "e", "short e"), L("f", "fe", ""),
            L("g", "ge", ""), L("ğ", "yumuşak g", "soft g: köfte"), L("h", "ha", ""),
            L("i", "i", "the dotted i, like ee"), L("ı", "süz i", "the i without a dot: arı"),
            L("İ", "büyük i", "capital of dotted i"), L("j", "je", "j as in jam"),
            L("k", "ka", ""), L("l", "le", ""), L("m", "em", ""), L("n", "en", ""),
            L("o", "o", "short o"), L("ö", "ö", "rounded e: söz"), L("p", "pe", ""),
            L("r", "re", "slight r"), L("s", "se", ""), L("ş", "sert s", "sh: şu"),
            L("t", "te", ""), L("u", "u", "short u"), L("ü", "ü", "rounded ee: ütü"),
            L("v", "ve", ""), L("y", "yu", ""), L("z", "ze", "")
        ]
    },
    "counting": {
        "title": "Counting in Turkish: 0 to 15",
        "explain": "Eleven and up is on (ten) + the number: on bir, on iki, on üç.",
        "numbers": [
            N("sıfır", "sı-fır", "0"), N("bir", "bır", "1"), N("iki", "ee-kee", "2"),
            N("üç", "üch", "3"), N("dört", "dört", "4"), N("beş", "besh", "5"),
            N("altı", "ahl-tı", "6"), N("yedi", "ye-dee", "7"), N("sekiz", "se-keez", "8"),
            N("dokuz", "do-kuz", "9"), N("on", "ohn", "10"), N("on bir", "ohn bır", "11"),
            N("on iki", "ohn ee-kee", "12"), N("on üç", "ohn üch", "13"),
            N("on dört", "ohn dört", "14"), N("on beş", "ohn besh", "15")
        ],
        "rules": [
            "Vowel harmony: suffixes match the vowels of the word — a back-vowel word gets back-vowel endings.",
            "ı (no dot) and i (dotted) are different vowels: arı (bee) vs arı (carried).",
            "ğ lengthens the vowel before it: çok (very) has a long o."
        ]
    }
}

S["uk"] = {
    "alphabet": {
        "title": "The Ukrainian alphabet: 33 letters in Cyrillic",
        "explain": ("Ukrainian writes in Cyrillic with 33 letters, including Ґ "
                    "(the voiced g) and І/Ї for the i-sounds. Two habits stand "
                    "out: an apostrophe after і, ї or й before a vowel, and the "
                    "soft sign ь that makes a consonant soft."),
        "letters": [
            L("А а", "a", ""), L("Б б", "b", ""), L("В в", "v", ""),
            L("Г г", "h", "h-sound: га"), L("Ґ ґ", "g", "the voiced g"),
            L("Д д", "d", ""), L("Е е", "e", ""), L("Є є", "ye", "ye: єдиний"),
            L("Ж ж", "zh", ""), L("З з", "z", ""), L("И и", "y", "after a vowel: бий"),
            L("І і", "i", "i as in machine"), L("Ї ї", "yi", "yi: їжа"),
            L("Й й", "y", ""), L("К к", "k", ""), L("Л л", "l", ""),
            L("М м", "m", ""), L("Н н", "n", ""), L("О о", "o", ""),
            L("П п", "p", ""), L("Р р", "r", "rolled"), L("С с", "s", ""),
            L("Т т", "t", ""), L("У у", "u", ""), L("Ф ф", "f", ""),
            L("Х х", "kh", "kh, as in loch"), L("Ц ц", "ts", ""),
            L("Ч ч", "ch", ""), L("Ш ш", "sh", ""), L("Щ щ", "shch", ""),
            L("Ь ь", "soft sign", "softens the consonant"), L("Ю ю", "yu", ""),
            L("Я я", "ya", "")
        ]
    },
    "counting": {
        "title": "Counting in Ukrainian: 0 to 15",
        "explain": "Eleven and up: одинадцять, дванадцять, then тринадцять, чотирнадцять, п'ятнадцять — the number + настіє? the pattern is number + -наст(и)ть.",
        "numbers": [
            N("нуль", "noo-l", "0"), N("один", "o-DEEN", "1"), N("два", "dva", "2"),
            N("три", "try", "3"), N("чотири", "CHO-tih-ri", "4"), N("п'ять", "pyat", "5"),
            N("шість", "sheest", "6"), N("сім", "seem", "7"), N("вісім", "VEE-seem", "8"),
            N("дев'ять", "dev-yat", "9"), N("десять", "dyeh-SAT", "10"),
            N("одинадцять", "o-dee-NAHTS-yat", "11"), N("дванадцять", "dva-NAHTS-yat", "12"),
            N("тринадцять", "try-NAHTS-yat", "13"), N("чотирнадцять", "CHO-tir-NAHTS-yat", "14"),
            N("п'ятнадцять", "pyat-NAHTS-yat", "15")
        ],
        "rules": [
            "The apostrophe marks і/ї/й before a vowel: п'ять (five), сім'я (family).",
            "і is a real vowel (i as in machine) and it softens the consonant before it.",
            "Щ is shch: щира (sincere) starts with the sh of ship plus a ch."
        ]
    }
}

S["uzn"] = {
    "alphabet": {
        "title": "The Uzbek alphabet (Latin): 32 letters",
        "explain": ("Uzbek's official Latin alphabet has 32 letters. The apostrophe "
                    "does real work: it marks the deep throat sounds q and g "
                    "(to'rt, beg'ona). Every syllable is open — a consonant "
                    "plus a vowel — so words sound even and regular."),
        "letters": [
            L("a", "ah", ""), L("b", "be", ""), L("d", "de", "no c"), L("e", "eh", ""),
            L("f", "ef", ""), L("g", "ge", ""), L("gʼ", "g (deep)", "g with the apostrophe: gʻarb"),
            L("h", "haitch", ""), L("x", "h (deep)", "the h of loch: xam"), L("i", "ee", ""),
            L("j", "zh", "zh: jil"), L("k", "ka", ""), L("l", "el", ""), L("m", "em", ""),
            L("n", "en", ""), L("o", "oh", ""), L("p", "pe", ""), L("q", "k (deep)", "deep k: qalam"),
            L("qʼ", "k (deeper)", "with the apostrophe: qoʻsh (to add)"), L("r", "er", "slight r"),
            L("s", "es", ""), L("t", "te", ""), L("u", "oo", ""), L("v", "ve", "")
        ]
    },
    "counting": {
        "title": "Counting in Uzbek: 0 to 15",
        "explain": "Eleven and up is o'n (ten) + the number: o'n bir, o'n ikki, o'n uch.",
        "numbers": [
            N("nol", "nohl", "0"), N("bir", "bır", "1"), N("ikki", "ık-kee", "2"),
            N("uch", "oohch", "3"), N("to'rt", "to-urt", "4"), N("besh", "besh", "5"),
            N("olti", "ohl-tee", "6"), N("yetti", "yett-tee", "7"), N("sakkiz", "sah-keez", "8"),
            N("to'qqiz", "to-uk-keez", "9"), N("o'n", "ohn", "10"), N("o'n bir", "ohn bır", "11"),
            N("o'n ikki", "ohn ık-kee", "12"), N("o'n uch", "ohn oohch", "13"),
            N("o'n to'rt", "ohn to-urt", "14"), N("o'n besh", "ohn besh", "15")
        ],
        "rules": [
            "Vowel harmony: words built from back vowels (a o u) take back-vowel endings; front vowels (e i) take front ones.",
            "The apostrophe letters (q, g, x, h) are deep throat sounds — friends of Arabic qāf.",
            "There is no c, no w and no y: those letters simply do not exist in the Uzbek Latin alphabet."
        ]
    }
}

S["vi"] = {
    "alphabet": {
        "title": "The Vietnamese alphabet (quốc ngữ): 29 base letters",
        "explain": ("Vietnamese writes in Latin with diacritics that mark tone "
                    "and vowel quality — a letter can wear a hat, a comma, a "
                    "dot and a hook at the same time. The base alphabet has "
                    "29 letters; j and w are essentially unused, and q works "
                    "only before u."),
        "letters": [
            L("a", "ah", "short a"), L("ă", "uh", "as in about: cá"), L("b", "b", ""),
            L("c", "k", "k before a/o: cá, cô"), L("d", "y", "y-sound: đêm"), L("đ", "d", "the real d: đô"),
            L("e", "eh", ""), L("ê", "eh (long)", "day"), L("g", "g", ""),
            L("h", "h", ""), L("i", "ee", ""), L("k", "k", "only before a/o: kha"),
            L("l", "l", "slight l"), L("m", "m", ""), L("n", "n", ""),
            L("o", "oh", ""), L("ô", "oh (long)", ""), L("ơ", "uh (rounded)", ""),
            L("p", "p", "borrowed words"), L("q", "k", "always before u: quê"), L("r", "r", "varies by region"),
            L("s", "s", ""), L("t", "t", ""), L("u", "oo", ""), L("ư", "uh (rounded)", ""),
            L("v", "v", ""), L("x", "s", "s before i/e: xí"), L("y", "ee", "")
        ]
    },
    "counting": {
        "title": "Counting in Vietnamese: 0 to 15",
        "explain": ("Every number is a syllable with a tone: một, hai, ba, bốn. "
                    "Eleven and up is mười (ten) + the number: mười một, mười "
                    "hai, mười ba. Tone matters — the same syllable in a "
                    "different tone is a different word."),
        "numbers": [
            N("không", "khwng (falling)", "0"), N("một", "mwat (falling)", "1"),
            N("hai", "hy (falling)", "2"), N("ba", "baha (flat)", "3"), N("bốn", "bohn (falling)", "4"),
            N("năm", "nam (falling)", "5"), N("sáu", "sw (rising)", "6"), N("bảy", "bay (falling)", "7"),
            N("tám", "tam (falling)", "8"), N("chín", "chin (flat)", "9"),
            N("mười", "mwy (flat)", "10"), N("mười một", "mwy mwat", "11"),
            N("mười hai", "mwy hy", "12"), N("mười ba", "mwy baha", "13"),
            N("mười bốn", "mwy bohn", "14"), N("mười lăm", "mwy lam (rising)", "15")
        ],
        "rules": [
            "Six tones: flat, rising, falling, creaky (hỏi), question (ngã) and falling-rising (sắc).",
            "d and đ are different: d is English y, đ is the d of door.",
            "c before a/o is k; x before i/e is s."
        ]
    }
}

S["zsm"] = {
    "alphabet": {
        "title": "The Malay alphabet: 28 letters",
        "explain": ("Malay (Bahasa Melayu) uses the Latin alphabet with 28 "
                    "letters — the English set minus nothing, plus the rule "
                    "that the c of kata is a k, and that the e between two "
                    "consonants is a short schwa (baca sounds like ba-ca)."),
        "letters": [
            L("a", "ah", ""), L("b", "be", ""), L("c", "k", "always k: kata (word)"),
            L("d", "de", ""), L("e", "schwa/eh", "e in the middle is a schwa: baca"),
            L("f", "ef", ""), L("g", "ge", "always a hard g"), L("h", "haitch", ""),
            L("i", "ee", ""), L("j", "zh", "zh: jamu"), L("k", "ka", ""),
            L("l", "el", ""), L("m", "em", ""), L("n", "en", ""), L("o", "oh", ""),
            L("p", "pe", ""), L("q", "k", "borrowed words"), L("r", "er", "tapped"),
            L("s", "es", ""), L("t", "te", ""), L("u", "oo", ""), L("v", "v", ""),
            L("w", "we", ""), L("x", "ks", "borrowed words"), L("y", "ye", "")
        ]
    },
    "counting": {
        "title": "Counting in Malay: 0 to 15",
        "explain": "Learn 0-12 by heart. Thirteen and up is the number + belas: tiga belas, empat belas, lima belas.",
        "numbers": [
            N("sifar", "see-FAHR", "0"), N("satu", "SAH-too", "1"), N("dua", "doo-AH", "2"),
            N("tiga", "TEE-gah", "3"), N("empat", "EHM-patt", "4"), N("lima", "LEE-mah", "5"),
            N("enam", "eh-NAHM", "6"), N("tujuh", "too-JOOH", "7"), N("lapan", "LAH-pahn", "8"),
            N("sembilan", "sem-BEE-lahn", "9"), N("sepuluh", "seh-POO-luuh", "10"),
            N("sebelas", "seh-BEH-lahss", "11"), N("dua belas", "doo-AH BEH-lahss", "12"),
            N("tiga belas", "TEE-gah BEH-lahss", "13"), N("empat belas", "EHM-patt BEH-lahss", "14"),
            N("lima belas", "LEE-mah BEH-lahss", "15")
        ],
        "rules": [
            "Stress falls on the second-to-last syllable: seh-PU-luuh"
            "Every syllable is open (consonant + vowel), so the rhythm is even.",
            "The middle e is a short schwa: kata = kah-tah, not kah-teh."
        ]
    }
}


S["it"] = {
    "alphabet": {
        "title": "The Italian alphabet: 26 letters (21 are native)",
        "explain": ("Italian uses the Latin alphabet; of its 26 letters, five "
                    "(j, k, w, x, y) only appear in borrowed words. The main "
                    "spelling trick is C: it is hard (k) before a, o and u, "
                    "and soft (ch) before e and i."),
        "letters": [
            L("a", "ah", ""), L("b", "bee", ""), L("c", "chee", "k in cat, ch in city"),
            L("d", "dee", ""), L("e", "eh", "short e"), L("f", "effe", ""),
            L("g", "gee", "g in get; gh is always hard"), L("h", "hacca", "always silent"),
            L("i", "ee", ""), L("j", "ippi", "borrowed words"), L("k", "cappa", "borrowed words"),
            L("l", "elle", ""), L("m", "emme", ""), L("n", "enne", ""), L("o", "oh", ""),
            L("p", "pee", ""), L("q", "cu", "always with u: qua"), L("r", "erre", "rolled"),
            L("s", "esse", ""), L("t", "tee", ""), L("u", "oo", ""),
            L("v", "voppa", ""), L("w", "doppia-vu", "borrowed words"),
            L("x", "ics", "borrowed words"), L("y", "ipsilon", "borrowed words"),
            L("z", "zeta", "ts or dz, by region")
        ]
    },
    "counting": {
        "title": "Counting in Italian: 0 to 15",
        "explain": "Learn 0-12 by heart. Thirteen and up is the number + dici: tredici, quattordici, quindici.",
        "numbers": [
            N("zero", "ZEH-ro", "0"), N("uno", "OO-no", "1"), N("due", "dweh", "2"),
            N("tre", "treh", "3"), N("quattro", "KWAT-tro", "4"), N("cinque", "CHeen-kweh", "5"),
            N("sei", "say", "6"), N("sette", "SET-teh", "7"), N("otto", "OT-to", "8"),
            N("nove", "NOH-veh", "9"), N("dieci", "DYEH-chee", "10"), N("undici", "oon-DEE-chee", "11"),
            N("dodici", "doh-DEE-chee", "12"), N("tredici", "treh-DEE-chee", "13"),
            N("quattordici", "kwah-troh-DEE-chee", "14"), N("quindici", "keen-DEE-chee", "15")
        ],
        "rules": [
            "Double consonants shorten the vowel before them: palla (ball) is sharper than pallo.",
            "The h is always silent: chi (who) vs ci (us).",
            "Final -e and -o are pronounced, but a final -a, -i or -u after a consonant can fade in fast speech."
        ]
    }
}

S["ml"] = {
    "alphabet": {
        "title": "The Malayalam script: vowels and the basic consonants",
        "explain": ("Malayalam writes in its own rounded script. Every consonant "
                    "carries a built-in a-sound, and the vowels around it are "
                    "small marks. Here are the twelve vowel letters and the "
                    "common consonants of the basic rows; the full script has "
                    "34 consonant letters, which the later levels cover."),
        "letters": [
            L("അ", "a", ""), L("ആ", "aa", "long a"), L("ഇ", "i", ""), L("ഊ", "ii", "long i"),
            L("ഉ", "u", ""), L("ഋ", "uu", "long u"), L("ഌ", "ri", "rare"), L("഍", "rii", "rare"),
            L("എ", "li", "rare"), L("ഏ", "e", "like e in met"), L("ഐ", "ai", "like ai in air"),
            L("ഓ", "o", ""), L("ഔ", "au", "like au in audio"),
            L("ക", "ka", ""), L("ഗ", "ga", ""), L("ങ", "nga", "the ng of sing"),
            L("ച", "cha", "t + sh: chat"), L("ജ", "ja", ""), L("ഞ", "nya", "n + ya"),
            L("ട", "ta (retroflex)", "t with the tongue curled back"), L("ഡ", "da (retroflex)", "d with the tongue curled back"),
            L("ണ", "na (retroflex)", "n with the tongue curled back"),
            L("ത", "ta", "the plain t"), L("ധ", "dha", "th as in this"), L("ന", "na", ""),
            L("പ", "pa", ""), L("ബ", "ba", ""), L("മ", "ma", ""),
            L("യ", "ya", "y as in yes"), L("ര", "ra", "light r"), L("ല", "la", ""),
            L("വ", "va", "v as in very"), L("സ", "sa", ""), L("ഹ", "ha", "")
        ]
    },
    "counting": {
        "title": "Counting in Malayalam: 0 to 15",
        "explain": ("Learn 0-10 by heart. Eleven and up is pattu (ten) + the "
                    "number below it: pattu onnu, pattu randu, pattu moonn."),
        "numbers": [
            N("പൂജ്യം", "pooryam", "0"), N("ഒന്ന്", "onnu", "1"), N("രണ്ട്", "randu", "2"),
            N("മൂന്ന്", "moonnu", "3"), N("നാല്", "naal", "4"), N("അഞ്ച്", "anj", "5"),
            N("ആറ്", "aar", "6"), N("ഏഴ്", "eeraa", "7"), N("പത്തൊൻപത്", "patontu", "8"),
            N("ഒൻപത്", "ontu", "9"), N("പത്ത്", "patt", "10"), N("പതിനോന്ന്", "patinnonnu", "11"),
            N("പതിനരണ്ട്", "patinarandu", "12"), N("പതിമൂന്ന്", "patimoonn", "13"),
            N("പതിനാല്", "patinaal", "14"), N("പതിനഞ്ച്", "patinj", "15")
        ],
        "rules": [
            "Every consonant has a hidden short a: ക is pronounced ka; the other vowels attach to it as marks.",
            "Double vowels are written with the long vowel letter: ആ (aa), ഊ (ii), ഋ (uu).",
            "The retroflex row (ട ഡ ണ) is made with the tongue curled back — it has no English equivalent."
        ]
    }
}


def is_spanish_scaffold(data, code):
    if code == "es":
        return False
    al = (data.get("alphabet") or {})
    co = (data.get("counting") or {})
    nums = {n.get("t", "") for n in (co.get("numbers") or [])}
    return (SPANISH_TITLE in (al.get("title") or "") or
            (len(nums) >= 5 and any(w in nums for w in ("cero", "uno", "dos", "tres", "cuatro"))))


def main():
    check = "--check" in sys.argv
    fixed, ok, skipped = [], [], []
    for code in sorted(S):
        found = None
        for phase in sorted(os.listdir("data/courses")):
            p = os.path.join("data/courses", phase, "%s_A1.json" % code)
            if os.path.exists(p):
                found = p
                break
        if not found:
            skipped.append("%s (no A1 file)" % code)
            continue
        data = json.load(open(found, encoding="utf-8"))
        if not is_spanish_scaffold(data, code):
            ok.append("%s %s" % (code, found))
            continue
        patch = S[code]
        data["alphabet"] = patch["alphabet"]
        data["counting"] = patch["counting"]
        if check:
            fixed.append("%s %s (would fix)" % (code, found))
        else:
            with open(found, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            fixed.append("%s %s" % (code, found))

    print("fixed:  %d" % len(fixed))
    for f in fixed:
        print("  ", f)
    print("already ok: %d" % len(ok))
    print("skipped:  %d" % len(skipped))
    for s in skipped:
        print("  ", s)

    if not check:
        os.makedirs("data/audit", exist_ok=True)
        with open(REPORT, "w", encoding="utf-8") as f:
            json.dump({
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "tool": "tools/fix-a1-scaffolds.py",
                "fixed": fixed,
                "already_ok": ok,
                "skipped": skipped,
                "status": "PASS" if fixed or ok else "REVIEW_REQUIRED",
            }, f, ensure_ascii=False, indent=1)
        print("\nreport: %s" % REPORT)
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Punjabi PHASE 1 depth — extras, third lessons, half-step rungs.

Written with the DSL in `tools/depth_kit.py`; rendered by
`tools/author-depth.py --lang pa`.

House style follows the shipped Punjabi course: Gurmukhi in `t`, the course's
romanisation in `r` — lowercase, ASCII, no diacritics (`pahilan main naksha
vekhia`, `ikk aurat ne meri madad kiti`) — and English in `en`, because the
course teaches in English. Unit ids keep each rung's own shipped scheme (A1 uses
`A1-U1` / `A1-U1-L1`, A2–C2 use `pa-a2-u1` / `pa-a2-l1`); the half-step rungs use
`<RUNG>P-U1` (A1P-U1 … C1P-U1). The shipped `pa_A1` lessons and the number table
used diacritics (`sati srī akāl`, `chār`) where the rest of the course was plain
ASCII; they were normalised to this convention in the pa pass, and the two blocks
that *define* marks — `alphabet` (`ṭa (retroflex)`) and `pronunciation` (`low
tone`) — keep them.

Register note: Punjabi is tonal, and the shipped course teaches the three-way
address ਤੂੰ / ਤੁਸੀਂ / ਤੁਸੀਂ ਜੀ. A1–A2 stay with ਤੁਸੀਂ and the present; B1 adds the
perfective with ergative ਨੇ (never after ਮੈਂ/ਅਸੀਂ) and the future (-ਆਂਗਾ/-ੇਗਾ);
B2 uses reported speech (ਕਿਹਾ ਗਿਆ ਕਿ …) and the impersonal passive; C1–C2 use the
written register of criticism and mediation (ਦ੍ਰਿਸ਼ਟੀਕੋਣ, ਸਬੂਤ, ਅੰਕੜੇ, ਮਤਲਬ).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # tools/ on the path
from depth_kit import D, EXTRA, G, L, T, V, WS, X   # noqa: E402

CODE = "pa"
NAME = "Punjabi"
NATIVE = "ਪੰਜਾਬੀ"
PHASE = 2
SCRIPT = "Gurmukhi"
VOICE = "pa-IN"
SKILL = ("Punjabi: Gurmukhi, three tones written by ਘ ਝ ਢ ਧ ਭ and the ਹ series, "
         "three-way address (ਤੂੰ / ਤੁਸੀਂ / ਤੁਸੀਂ ਜੀ), the ergative ਨੇ in the "
         "perfective, verb-final order, and the analytical future (-ਆਂਗਾ/-ੇਗਾ)")

EXTRAS = {}
THIRD = {}
HALFSTEPS = {}


EXTRAS["A1"] = EXTRA(
    culture=("Punjabi is written in Gurmukhi, and it is a tonal language: the same letters with "
             "a different pitch are different words, which is why ਘੋੜਾ (a horse) and ਕੋਰਾ "
             "(blank) are not the same word said two ways. Two letters carry sounds English "
             "does not use, and the ੜ of ਪੜ੍ਹਨਾ (to read) is the one every learner hears first. "
             "Shahmukhi, the Perso-Arabic script, writes the same language across the border."),
    source_url="https://en.wikipedia.org/wiki/Punjabi_language",
    reading=("ਮੈਂ ਸਿਮਰਨ ਹਾਂ। ਮੈਂ ਅੰਮ੍ਰਿਤਸਰ ਵਿੱਚ ਰਹਿੰਦੀ ਹਾਂ। ਸਵੇਰੇ ਛੇ ਵਜੇ ਉੱਠਦੀ ਹਾਂ ਅਤੇ ਚਾਹ "
             "ਬਣਾਉਂਦੀ ਹਾਂ। ਮੇਰੀ ਮਾਂ ਅਧਿਆਪਕਾ ਹੈ ਅਤੇ ਪਿਤਾ ਜੀ ਦੁਕਾਨ ਚਲਾਉਂਦੇ ਹਨ। ਮੈਂ ਰੋਜ਼ ਸਵੇਰੇ "
             "ਪੜ੍ਹਦੀ ਹਾਂ, ਫਿਰ ਕਾਲਜ ਜਾਂਦੀ ਹਾਂ। ਸ਼ਾਮ ਨੂੰ ਪਾਰਕ ਵਿੱਚ ਸੈਰ ਕਰਦੀ ਹਾਂ। ਮੈਨੂੰ ਕਿਤਾਬਾਂ "
             "ਪੜ੍ਹਨਾ ਪਸੰਦ ਹੈ। ਐਤਵਾਰ ਨੂੰ ਸਾਰੇ ਘਰ ਇਕੱਠੇ ਖਾਂਦੇ ਹਾਂ।"),
    reading_gloss=("I am Simran. I live in Amritsar. I get up at six in the morning and make "
                   "tea. My mother is a teacher and my father runs a shop. Every morning I "
                   "study, then I go to college. In the evening I walk in the park. I like "
                   "reading books. On Sunday everyone at home eats together."),
    listening=("ਸਿਮਰਨ: ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਜੀ, ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?<br>"
               "ਅਰਜੁਨ: ਮੈਂ ਠੀਕ ਹਾਂ, ਧੰਨਵਾਦ। ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?<br>"
               "ਸਿਮਰਨ: ਮੈਂ ਵੀ ਠੀਕ ਹਾਂ। ਇਹ ਤੁਹਾਡਾ ਪੁੱਤਰ ਹੈ?<br>"
               "ਅਰਜੁਨ: ਹਾਂ, ਉਸ ਦਾ ਨਾਮ ਮਨਵੀਰ ਹੈ। ਉਹ ਹੁਣ ਸਕੂਲ ਜਾਂਦਾ ਹੈ।<br>"
               "ਸਿਮਰਨ: ਬਹੁਤ ਚੰਗਾ! ਮੇਰੀ ਧੀ ਵੀ ਸਕੂਲ ਜਾਂਦੀ ਹੈ।"),
    listening_gloss=("Simran: Hello, how are you? Arjun: I am fine, thank you. How are you? "
                     "Simran: I am fine too. Is this your son? Arjun: Yes, his name is Manveer. "
                     "He goes to school now. Simran: Very good! My daughter goes to school too."),
    voice_tag=VOICE,
    idioms=[
        ("ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ", "God is truth", "the everyday greeting, and the reply to it"),
        ("ਜੀ ਆਇਆਂ ਨੂੰ", "may you come and be seated", "welcome"),
        ("ਕੀ ਹਾਲ ਹੈ?", "what is the state?", "how are you? how are things?"),
        ("ਵਾਹ ਵਾਹ", "wow wow", "bravo, very well done"),
        ("ਰੱਬ ਰਾਖਾ", "God is the keeper", "goodbye, God protect you"),
        ("ਚੰਗਾ ਚੰਗਾ", "good good", "all right, agreed"),
        ("ਹੁਣੇ ਹੁਣੇ", "just now just now", "a moment ago"),
        ("ਕੋਈ ਗੱਲ ਨਹੀਂ", "there is no matter", "never mind, it is nothing"),
        ("ਮਿਹਰਬਾਨੀ", "kindness", "please / thank you, said to be polite"),
        ("ਖੁਸ਼ੀ ਨਾਲ", "with happiness", "gladly, with pleasure"),
    ],
    mistakes=[
        ("ਤੂੰ ਕਿੱਥੇ ਰਹਿੰਦਾ ਹੈ?", "ਤੂੰ ਕਿੱਥੇ ਰਹਿੰਦਾ ਹੈਂ?",
         "The intimate ਤੂੰ takes ਹੈਂ; ਹੈ belongs to ਉਹ and ਇਹ."),
        ("ਮੈਂ ਨੂੰ ਚਾਹ ਚਾਹੀਦੀ ਹੈ।", "ਮੈਨੂੰ ਚਾਹ ਚਾਹੀਦੀ ਹੈ।",
         "The dative is one word: ਮੈਨੂੰ, not ਮੈਂ ਨੂੰ."),
        ("ਇਹ ਮੇਰਾ ਭੈਣ ਹੈ।", "ਇਹ ਮੇਰੀ ਭੈਣ ਹੈ।",
         "ਭੈਣ is feminine, so the possessive agrees: ਮੇਰੀ ਭੈਣ."),
    ],
    task_title="Write six sentences introducing yourself in Punjabi",
    task_instructions=("Cover name, city, what you do in the morning, one thing you like, one "
                       "thing about your family, and a goodbye. Use ਤੁਸੀਂ when you address "
                       "somebody and ਮੈਂ about yourself, and colour the whole set with three "
                       "phrases from the idiom list."),
)

EXTRAS["A2"] = EXTRA(
    culture=("Punjabi cooking runs on the tandoor and the griddle: ਸਰਸੋਂ ਦਾ ਸਾਗ with ਮੱਕੀ ਦੀ ਰੋਟੀ "
             "in winter, ਛੋਲੇ and ਕੁਲਚੇ in the market, and ਲੱਸੀ to cool the afternoon. The "
             "region's cooking is known for its many local ways rather than one recipe, and a "
             "Punjabi kitchen measures by hand and ear — a fist of flour, a fist of ghee, salt "
             "till it tastes right."),
    source_url="https://en.wikipedia.org/wiki/Punjabi_cuisine",
    reading=("ਅੱਜ ਸਵੇਰੇ ਮੈਂ ਸਬਜ਼ੀ ਮੰਡੀ ਗਿਆ। ਟਮਾਟਰ ਅੱਠ ਰੁਪਏ ਕਿੱਲੋ ਸਨ ਅਤੇ ਆਲੂ ਪੰਜ ਰੁਪਏ। ਮੈਂ ਦੋ "
             "ਕਿੱਲੋ ਟਮਾਟਰ ਅਤੇ ਇੱਕ ਕਿੱਲੋ ਆਲੂ ਲਏ। ਦੁਕਾਨਦਾਰ ਨੇ ਬੋਰੀ ਵਿੱਚ ਪਾ ਦਿੱਤਾ। ਫਿਰ ਮੈਂ ਦੁੱਧ "
             "ਅਤੇ ਦਹੀਂ ਲਿਆ। ਘਰ ਆ ਕੇ ਮਾਂ ਨੇ ਕਿਹਾ ਕਿ ਭਾਅ ਮੁੱਲ ਚੰਗਾ ਹੋਇਆ। ਸ਼ਾਮ ਨੂੰ ਅਸੀਂ ਸਾਰੇ "
             "ਰਲ ਕੇ ਖਾਣਾ ਖਾਧਾ।"),
    reading_gloss=("This morning I went to the vegetable market. Tomatoes were eight rupees a "
                   "kilo and potatoes five. I took two kilos of tomatoes and one kilo of "
                   "potatoes. The shopkeeper put them in a sack. Then I bought milk and curd. "
                   "At home my mother said the bargaining had gone well. In the evening we all "
                   "ate together."),
    listening=("ਗਾਹਕ: ਇਹ ਕੁੜਤੀ ਕਿੰਨੇ ਦੀ ਹੈ?<br>"
               "ਦੁਕਾਨਦਾਰ: ਅੱਠ ਸੌ ਰੁਪਏ ਦੀ। ਖੱਦਰ ਦੀ ਹੈ।<br>"
               "ਗਾਹਕ: ਬਹੁਤ ਮਹਿੰਗੀ ਹੈ। ਛੇ ਸੌ ਵਿੱਚ ਦਿਓ।<br>"
               "ਦੁਕਾਨਦਾਰ: ਸੱਤ ਸੌ ਪੰਜਾਹ, ਇਸ ਤੋਂ ਘੱਟ ਨਹੀਂ।<br>"
               "ਗਾਹਕ: ਠੀਕ ਹੈ, ਇਹੀ ਲੈ ਲਵਾਂਗਾ।"),
    listening_gloss=("Customer: How much is this kurta? Shopkeeper: Eight hundred rupees. It is "
                     "khaddar. Customer: That is very expensive. Give it for six hundred. "
                     "Shopkeeper: Seven hundred and fifty, not less. Customer: All right, I "
                     "will take this one."),
    voice_tag=VOICE,
    idioms=[
        ("ਗਰਮਾ-ਗਰਮ", "hot-hot", "piping hot, straight off the griddle"),
        ("ਦਿਲ ਖੋਲ੍ਹ ਕੇ", "having opened the heart", "heartily, generously"),
        ("ਘਰ ਦਾ ਬਣਿਆ", "made at home", "home-made"),
        ("ਪੇਟ ਭਰ ਕੇ", "having filled the stomach", "to the full, as much as one wants"),
        ("ਭਾਅ ਮੁੱਲ ਕਰਨਾ", "to do rate and price", "to bargain"),
        ("ਘੱਟ ਤੋਂ ਘੱਟ", "less than less", "at least"),
        ("ਸ਼ੌਕ ਨਾਲ", "with fondness", "with relish, gladly"),
        ("ਮੂੰਹ ਮਿੱਠਾ ਕਰਨਾ", "to sweeten the mouth", "to celebrate good news with sweets"),
        ("ਲੰਗਰ ਛਕਣਾ", "to share the langar", "to eat the community meal"),
        ("ਰੋਟੀ-ਪਾਣੀ", "bread and water", "daily sustenance, a living"),
    ],
    mistakes=[
        ("ਇਹ ਕਿੰਨਾ ਦੀ ਹੈ?", "ਇਹ ਕਿੰਨੇ ਦੀ ਹੈ?",
         "A price is asked with the oblique masculine: ਕਿੰਨੇ ਦੀ."),
        ("ਮੈਂ ਦੋ ਕਿੱਲੋ ਆਲੂ ਲਈ।", "ਮੈਂ ਦੋ ਕਿੱਲੋ ਆਲੂ ਲਏ।",
         "ਆਲੂ counts as masculine plural here: ਲਏ, not ਲਈ."),
        ("ਇਹ ਕੁੜਤੀ ਖੱਦਰ ਦਾ ਹੈ।", "ਇਹ ਕੁੜਤੀ ਖੱਦਰ ਦੀ ਹੈ।",
         "ਕੁੜਤੀ is feminine, so the material takes ਦੀ: ਖੱਦਰ ਦੀ."),
    ],
    task_title="Bargain for three things in Punjabi on paper",
    task_instructions=("Write a market dialogue of six turns: ask the price with ਕਿੰਨੇ ਦੀ, "
                       "call it ਮਹਿੰਗਾ, offer your own price, hear the seller refuse with "
                       "ਇਸ ਤੋਂ ਘੱਟ ਨਹੀਂ, agree, and close with ਧੰਨਵਾਦ. Add one sentence "
                       "comparing two prices with ਤੋਂ ਸਸਤਾ."),
)

EXTRAS["B1"] = EXTRA(
    culture=("Bhangra is the harvest dance of Punjab, tied to Vaisakhi in April and the first "
             "quarter of May, when the wheat comes in. The ਢੋਲ sets the beat, the dancers "
             "answer it with the shoulder and the knee, and the women's ਗਿੱਧਾ answers back "
             "with ਬੋਲੀਆਂ — couplets tossed one at a time across the circle. In the villages "
             "the dance is a work party with a drum in it, not a performance with an audience."),
    source_url="https://en.wikipedia.org/wiki/Bhangra_(dance)",
    reading=("ਪਿੰਡ ਵਿੱਚ ਵਿਸਾਖੀ ਦਾ ਮੇਲਾ ਲੱਗਾ ਹੋਇਆ ਸੀ। ਢੋਲ ਵੱਜ ਰਿਹਾ ਸੀ ਅਤੇ ਮੁੰਡੇ ਭੰਗੜਾ ਪਾ ਰਹੇ "
             "ਸਨ। ਕੁੜੀਆਂ ਨੇ ਗਿੱਧਾ ਕੀਤਾ ਅਤੇ ਬੋਲੀਆਂ ਪਾਈਆਂ। ਬਜ਼ੁਰਗ ਛਾਂ ਵਿੱਚ ਬੈਠੇ ਸਨ ਅਤੇ ਕਣਕ ਦੀ "
             "ਫ਼ਸਲ ਬਾਰੇ ਗੱਲਾਂ ਕਰ ਰਹੇ ਸਨ। ਮੈਂ ਵੀ ਨੱਚਣ ਲੱਗਾ ਪਰ ਜਲਦੀ ਥੱਕ ਗਿਆ। ਸ਼ਾਮ ਨੂੰ ਅਸੀਂ ਲੰਗਰ "
             "ਛਕਿਆ ਅਤੇ ਖੁਸ਼ੀ ਨਾਲ ਘਰ ਆਏ।"),
    reading_gloss=("A Vaisakhi fair was on in the village. The dhol was being played and the boys "
                   "were dancing bhangra. The girls danced giddha and threw boliyan. The elders "
                   "sat in the shade and talked about the wheat crop. I started dancing too but "
                   "tired quickly. In the evening we shared the langar and went home happy."),
    listening=("ਰਾਜ: ਵਿਸਾਖੀ ਦੇ ਪ੍ਰੋਗਰਾਮ ਦੀ ਤਿਆਰੀ ਕਿੱਥੇ ਪਹੁੰਚੀ?<br>"
               "ਸੀਮਾ: ਢੋਲ ਵਾਲੇ ਨਾਲ ਗੱਲ ਹੋ ਗਈ ਹੈ, ਪਰ ਛਾਂ ਲਈ ਤੰਬੂ ਦੀ ਲੋੜ ਹੈ।<br>"
               "ਰਾਜ: ਤੰਬੂ ਦਾ ਖਰਚਾ ਕਿੰਨਾ ਪਵੇਗਾ?<br>"
               "ਸੀਮਾ: ਲਗਭਗ ਦਸ ਹਜ਼ਾਰ। ਮੈਂ ਕਮੇਟੀ ਨੂੰ ਬੇਨਤੀ ਭੇਜ ਦਿੱਤੀ ਹੈ।<br>"
               "ਰਾਜ: ਠੀਕ ਹੈ, ਜਵਾਬ ਆਉਣ ਤੱਕ ਬੋਲੀ ਦਾ ਕੰਮ ਰੋਕ ਦਿਓ।"),
    listening_gloss=("Raj: Where has the preparation for the Vaisakhi programme reached? Seema: "
                     "It is settled with the dhol player, but we need a tent for the shade. Raj: "
                     "How much will the tent cost? Seema: About ten thousand. I have sent a "
                     "request to the committee. Raj: All right, stop the bidding work until the "
                     "reply comes."),
    voice_tag=VOICE,
    idioms=[
        ("ਮਿਹਨਤ ਦਾ ਫਲ", "the fruit of labour", "what hard work finally gives"),
        ("ਕੰਮ ਸਿਰੇ ਚੜ੍ਹਨਾ", "the work to climb to its head", "the job to be finished"),
        ("ਉੱਠ ਕੇ ਪੈਣਾ", "to rise and lie down", "to be up and about, busy all day"),
        ("ਅੱਖ ਮਿਲਾਉਣਾ", "to meet the eye", "to face somebody honestly"),
        ("ਦਿਲ ਦੀ ਗੱਲ", "a matter of the heart", "a frank word, what one really thinks"),
        ("ਵਾਅਦਾ ਪੂਰਾ ਕਰਨਾ", "to fulfil the promise", "to keep one's word"),
        ("ਢੋਲ ਵੱਜਣਾ", "for the dhol to be beaten", "for a celebration to be under way"),
        ("ਦੋ ਗੱਲਾਂ ਕਰਨਾ", "to do two talks", "to have a word with somebody"),
        ("ਪੱਕੀ ਗੱਲ", "a ripe matter", "a settled, certain thing"),
        ("ਸਿਰ ਉੱਤੇ ਬੋਝ", "a load on the head", "a heavy responsibility"),
    ],
    mistakes=[
        ("ਮੈਂ ਨੇ ਨਕਸ਼ਾ ਵੇਖਿਆ।", "ਮੈਂ ਨਕਸ਼ਾ ਵੇਖਿਆ।",
         "The ergative ਨੇ is not used after ਮੈਂ and ਅਸੀਂ in the standard perfective."),
        ("ਕੱਲ੍ਹ ਮੈਂ ਜਾਵਾਂਗਾ ਸੀ।", "ਕੱਲ੍ਹ ਮੈਂ ਗਿਆ ਸੀ।",
         "A finished past takes the perfective ਗਿਆ ਸੀ, not the future ਜਾਵਾਂਗਾ."),
        ("ਉਹ ਮੇਰੀ ਮਦਦ ਕੀਤੀ।", "ਉਸ ਨੇ ਮੇਰੀ ਮਦਦ ਕੀਤੀ।",
         "A third-person subject of a transitive perfective takes ਨੇ: ਉਸ ਨੇ."),
    ],
    task_title="Plan a village event in Punjabi, and report it after",
    task_instructions=("Write eight lines: three lines of planning between two people (who does "
                       "what by when, with ਲੋੜ and ਪਵੇਗਾ), then five lines reporting the event in "
                       "the past, using one perfective with ਨੇ, one future from the planning, "
                       "and one idiom from the list."),
)

EXTRAS["B2"] = EXTRA(
    culture=("The Sikh Empire held Punjab from 1799, when Maharaja Ranjit Singh took Lahore, "
             "until 1849, when the British annexed it after the Second Anglo-Sikh War. At its "
             "height it ran from Gilgit and Tibet to the Sindh desert and from the Khyber Pass "
             "to the Sutlej, in eight provinces, with roughly twelve million people in 1800 and "
             "an army trained in the European manner. A formal note in Punjabi about a state "
             "inherits that vocabulary of ਦਫ਼ਤਰ, ਸੂਬਾ, ਸੰਧੀ and ਸ਼ਰਤ."),
    source_url="https://en.wikipedia.org/wiki/Sikh_Empire",
    reading=("ਇੱਕ ਰਸਮੀ ਨੋਟ ਵਿੱਚ ਲਿਖਿਆ ਗਿਆ ਹੈ ਕਿ ਮਹਾਰਾਜਾ ਰਣਜੀਤ ਸਿੰਘ ਨੇ 1799 ਵਿੱਚ ਲਾਹੌਰ ਉੱਤੇ "
             "ਕਬਜ਼ਾ ਕੀਤਾ ਅਤੇ ਖਾਲਸਾ ਰਾਜ ਦੀ ਨੀਂਹ ਰੱਖੀ। ਇਹ ਰਾਜ 1849 ਵਿੱਚ ਦੂਜੀ ਅੰਗਰੇਜ਼-ਸਿੱਖ ਜੰਗ "
             "ਤੋਂ ਬਾਅਦ ਖ਼ਤਮ ਹੋ ਗਿਆ। ਇਤਿਹਾਸਕਾਰਾਂ ਅਨੁਸਾਰ ਇਸ ਵਿੱਚ ਅੱਠ ਸੂਬੇ ਸਨ ਅਤੇ 1800 ਵਿੱਚ "
             "ਲਗਭਗ ਇੱਕ ਕਰੋੜ ਵੀਹ ਲੱਖ ਲੋਕ ਵੱਸਦੇ ਸਨ। ਇਹ ਉੱਤਰ-ਪੱਛਮ ਦਾ ਆਖ਼ਰੀ ਵੱਡਾ ਰਾਜ ਸੀ ਜੋ "
             "ਅੰਗਰੇਜ਼ਾਂ ਦੇ ਹੱਥ ਆਇਆ।"),
    reading_gloss=("A formal note states that Maharaja Ranjit Singh took Lahore in 1799 and laid "
                   "the foundation of the Khalsa state. That state ended in 1849 after the "
                   "Second Anglo-Sikh War. According to historians it had eight provinces and "
                   "about twelve million people lived in it in 1800. It was the last major "
                   "north-western power to fall to the British."),
    listening=("ਅਧਿਕਾਰੀ: ਰਿਪੋਰਟ ਵਿੱਚ ਕੀ ਕਿਹਾ ਗਿਆ ਹੈ?<br>"
               "ਕਰਮਚਾਰੀ: ਕਿਹਾ ਗਿਆ ਹੈ ਕਿ ਦੋ ਵਿਭਾਗਾਂ ਨੇ ਅੰਕੜੇ ਨਹੀਂ ਭੇਜੇ।<br>"
               "ਅਧਿਕਾਰੀ: ਕੀ ਇਹ ਗੱਲ ਪੱਕੀ ਹੈ?<br>"
               "ਕਰਮਚਾਰੀ: ਜੀ, ਲਿਖਤੀ ਤੌਰ ਤੇ ਪੁਸ਼ਟੀ ਕੀਤੀ ਗਈ ਹੈ।<br>"
               "ਅਧਿਕਾਰੀ: ਤਾਂ ਫਿਰ ਅਗਲੀ ਮੀਟਿੰਗ ਵਿੱਚ ਮਨਜ਼ੂਰੀ ਲਈ ਪੇਸ਼ ਕੀਤਾ ਜਾਵੇਗਾ।"),
    listening_gloss=("Officer: What is said in the report? Clerk: It is stated that two "
                     "departments have not sent their figures. Officer: Is the matter certain? "
                     "Clerk: Yes, it has been confirmed in writing. Officer: Then it will be "
                     "placed for approval in the next meeting."),
    voice_tag=VOICE,
    idioms=[
        ("ਕਾਗਜ਼ੀ ਕਾਰਵਾਈ", "paper proceedings", "paperwork, formal process"),
        ("ਦਾਅਵਾ ਸਿੱਧ ਕਰਨਾ", "to prove the claim", "to make a claim stand up"),
        ("ਸਬੂਤ ਦੇਣਾ", "to give proof", "to produce evidence"),
        ("ਅੰਕੜੇ ਬੋਲਦੇ ਹਨ", "the figures speak", "the numbers settle the argument"),
        ("ਦੋ ਧਿਰਾਂ", "two sides", "the two parties in a dispute"),
        ("ਗੋਲ-ਮੋਲ ਜਵਾਬ", "a round-about answer", "an evasive reply"),
        ("ਜਵਾਬਦੇਹੀ ਬਣਦੀ ਹੈ", "accountability is due", "somebody must answer for it"),
        ("ਸਮੇਂ ਦੀ ਪਾਬੰਦੀ", "a restriction of time", "a time limit"),
        ("ਸ਼ਰਤਾਂ ਪੂਰੀਆਂ ਕਰਨਾ", "to complete the conditions", "to meet the terms"),
        ("ਫੈਸਲੇ ਤੋਂ ਪਹਿਲਾਂ", "before the decision", "while the matter is still open"),
    ],
    mistakes=[
        ("ਉਸ ਨੇ ਕਿਹਾ ਕਿ ਮੈਂ ਆਵਾਂਗਾ।", "ਉਸ ਨੇ ਕਿਹਾ ਕਿ ਉਹ ਆਵੇਗਾ।",
         "Reported speech shifts the pronoun: the speaker's ਮੈਂ becomes ਉਹ in the report."),
        ("ਤਿੰਨ ਰਿਪੋਰਟਾਂ ਭੇਜਿਆ ਗਿਆ।", "ਤਿੰਨ ਰਿਪੋਰਟਾਂ ਭੇਜੀਆਂ ਗਈਆਂ।",
         "The passive participle agrees with its plural object: ਭੇਜੀਆਂ ਗਈਆਂ."),
        ("ਸ਼ਰਤਾਂ ਪੂਰੀਆਂ ਹੋਈ।", "ਸ਼ਰਤਾਂ ਪੂਰੀਆਂ ਹੋਈਆਂ।",
         "Plural feminine subject takes ਹੋਈਆਂ."),
    ],
    task_title="Write a formal Punjabi note of six sentences",
    task_instructions=("Take one small decision — a society rule, a shop licence, a school "
                       "timing — and write it formally: one sentence of reported speech with "
                       "ਕਿਹਾ ਗਿਆ ਹੈ ਕਿ, one impersonal passive, one condition with ਸ਼ਰਤ, one "
                       "figure, and one line naming who is ਜਵਾਬਦੇਹ. Keep the pronouns shifted "
                       "as a formal note requires."),
)

EXTRAS["C1"] = EXTRA(
    culture=("Punjabi literature runs from Baba Farid's verses in the Guru Granth Sahib through "
             "Bulleh Shah's kafis and Waris Shah's ਲੋਕ ਕਥਾ of Heer, to the twentieth century, "
             "where Amrita Pritam's poem on the partition of 1947 became the language's most "
             "quoted modern text. The literary language is written in two scripts — Gurmukhi "
             "in the east, Shahmukhi in the west — so the same poem often exists in two "
             "alphabets, and a reader in Amritsar and a reader in Lahore can share one line "
             "without sharing a page."),
    source_url="https://en.wikipedia.org/wiki/Punjabi_literature",
    reading=("ਪੰਜਾਬੀ ਸਾਹਿਤ ਦੀ ਪਰੰਪਰਾ ਵਿੱਚ ਬੁੱਲ੍ਹੇ ਸ਼ਾਹ ਦੀ ਕਾਫ਼ੀ ਅਤੇ ਵਾਰਿਸ ਸ਼ਾਹ ਦੀ ਹੀਰ ਦੋ ਵੱਡੇ "
             "ਥੰਮ੍ਹ ਹਨ। ਬੁੱਲ੍ਹੇ ਸ਼ਾਹ ਨੇ ਰੂਹਾਨੀ ਸਵਾਲ ਸਧਾਰਨ ਬੋਲੀ ਵਿੱਚ ਪੁੱਛੇ, ਅਤੇ ਵਾਰਿਸ ਸ਼ਾਹ ਨੇ "
             "ਪਿਆਰ ਦੀ ਕਥਾ ਨੂੰ ਉਸ ਵੇਲੇ ਦੇ ਸਮਾਜ ਦਾ ਸ਼ੀਸ਼ਾ ਬਣਾ ਦਿੱਤਾ। ਵੀਹਵੀਂ ਸਦੀ ਵਿੱਚ ਅੰਮ੍ਰਿਤਾ "
             "ਪ੍ਰੀਤਮ ਦੀ ਕਵਿਤਾ ਨੇ ਇਸੇ ਰਵਾਇਤ ਨੂੰ ਵੰਡ ਦੇ ਦਰਦ ਨਾਲ ਜੋੜਿਆ। ਸਮੀਖਿਅਕ ਮੰਨਦੇ ਹਨ ਕਿ "
             "ਇਹਨਾਂ ਰਚਨਾਵਾਂ ਦੀ ਤਾਕਤ ਉਹਨਾਂ ਦੀ ਬੋਲੀ ਵਿੱਚ ਹੈ, ਸਿਰਫ਼ ਵਿਸ਼ੇ ਵਿੱਚ ਨਹੀਂ।"),
    reading_gloss=("In the tradition of Punjabi literature, Bulleh Shah's kafi and Waris Shah's "
                   "Heer are two great pillars. Bulleh Shah asked spiritual questions in plain "
                   "speech, and Waris Shah turned a love story into a mirror of the society of "
                   "his time. In the twentieth century Amrita Pritam's poetry joined that same "
                   "tradition to the pain of partition. Critics hold that the strength of these "
                   "works lies in their language, not only in their subject."),
    listening=("ਸੰਪਾਦਕ: ਹੀਰ ਬਾਰੇ ਤੁਹਾਡਾ ਦ੍ਰਿਸ਼ਟੀਕੋਣ ਕੀ ਹੈ?<br>"
               "ਸਮੀਖਿਅਕ: ਮੇਰੇ ਖਿਆਲ ਵਿੱਚ ਇਹ ਪਿਆਰ ਦੀ ਕਹਾਣੀ ਨਹੀਂ, ਸਮਾਜ ਦਾ ਸ਼ੀਸ਼ਾ ਹੈ।<br>"
               "ਸੰਪਾਦਕ: ਕੀ ਕੋਈ ਕਮੀ ਵੀ ਦਿਸਦੀ ਹੈ?<br>"
               "ਸਮੀਖਿਅਕ: ਹਾਂ, ਕੁਝ ਹਿੱਸਿਆਂ ਵਿੱਚ ਬਿਰਤਾਂਤ ਢਿੱਲਾ ਪੈ ਜਾਂਦਾ ਹੈ।<br>"
               "ਸੰਪਾਦਕ: ਇਹ ਗੱਲ ਲਿਖਤ ਵਿੱਚ ਵੀ ਆਉਣੀ ਚਾਹੀਦੀ ਹੈ, ਪਰ ਸਬੂਤ ਨਾਲ।"),
    listening_gloss=("Editor: What is your standpoint on Heer? Critic: In my view it is not a "
                     "love story, it is a mirror of society. Editor: Do you see any weakness "
                     "too? Critic: Yes, in some parts the narrative slackens. Editor: That "
                     "point should come into the writing as well, but with evidence."),
    voice_tag=VOICE,
    idioms=[
        ("ਬੋਲੀ ਵਿੱਚ ਗੱਲ ਕਰਨੀ", "to put it in the language", "to say it plainly"),
        ("ਲਿਖਤ ਦਾ ਸਬੂਤ", "proof from the writing", "evidence from the text itself"),
        ("ਪਰਤਾਂ ਪਰਤਾਂ", "layer on layer", "a text with depths to open"),
        ("ਦ੍ਰਿਸ਼ਟੀਕੋਣ ਅਪਣਾਉਣਾ", "to adopt a standpoint", "to read from a stated position"),
        ("ਸਿਰਫ਼ ਇੱਕ ਪੱਖ", "only one side", "a one-sided reading"),
        ("ਸ਼ਬਦਾਂ ਦਾ ਜਾਦੂ", "the magic of words", "writing that holds the reader"),
        ("ਸਮੇਂ ਦੀ ਧਾਰਾ", "the current of time", "the drift of an age"),
        ("ਸੱਚ ਦੀ ਭਾਲ", "the search for truth", "an honest inquiry"),
        ("ਮੂਲ ਪਾਠ", "the root text", "the original text"),
        ("ਦਿਲ ਦੀ ਡੂੰਘਾਈ", "the depth of the heart", "inner feeling"),
    ],
    mistakes=[
        ("ਮੇਰੇ ਖਿਆਲ ਵਿੱਚ ਕਿ ਇਹ ਠੀਕ ਹੈ।", "ਮੇਰੇ ਖਿਆਲ ਵਿੱਚ ਇਹ ਠੀਕ ਹੈ।",
         "ਵਿੱਚ already carries the opinion — the complementiser ਕਿ is not added after it."),
        ("ਉਹ ਕਹਿੰਦਾ ਕਿ ਇਹ ਸੱਚ ਹੈ।", "ਉਹ ਕਹਿੰਦਾ ਹੈ ਕਿ ਇਹ ਸੱਚ ਹੈ।",
         "The reporting verb needs its ਹੈ before ਕਿ introduces the clause."),
        ("ਲੇਖਕ ਨੇ ਲਿਖਿਆ ਕਿ ਹਰ ਇਨਸਾਨ ਦੀ ਆਪਣੀ ਰਾਏ ਹੋਣੀ ਚਾਹੀਦੀ।",
         "ਲੇਖਕ ਨੇ ਲਿਖਿਆ ਕਿ ਹਰ ਇਨਸਾਨ ਦੀ ਆਪਣੀ ਰਾਏ ਹੋਣੀ ਚਾਹੀਦੀ ਹੈ।",
         "ਚਾਹੀਦੀ/ਚਾਹੀਦਾ keeps its ਹੈ at the end of the clause."),
    ],
    task_title="Write a Punjabi review of one poem in four short paragraphs",
    task_instructions=("Choose one kafi, one folk narrative or one modern poem. In four "
                       "paragraphs: name the poet and the period, state your ਦ੍ਰਿਸ਼ਟੀਕੋਣ in one "
                       "sentence, quote two lines with the page or the section you took them "
                       "from, and finish with one ਕਮੀ and one strength. No claim without ਲਿਖਤ ਦਾ "
                       "ਸਬੂਤ."),
)

EXTRAS["C2"] = EXTRA(
    culture=("The Punjabi diaspora numbers between three and five million, concentrated in "
             "Britain, Canada, the United States, Western Europe, the Gulf and Australia. Its "
             "language tells two stories at once: Punjabi survives as the language of the house "
             "and the gurdwara, while the office, the form and the school notice arrive in "
             "English. A conversation in a diaspora family moves between the two without "
             "noticing — the same speaker negotiates a wedding in Punjabi and a mortgage in "
             "English, and the third generation has to decide what to keep."),
    source_url="https://en.wikipedia.org/wiki/Punjabi_diaspora",
    reading=("ਪੰਜਾਬੀ ਡਾਇਸਪੋਰਾ ਤਿੰਨ ਤੋਂ ਪੰਜ ਮਿਲੀਅਨ ਲੋਕਾਂ ਦਾ ਹੈ ਅਤੇ ਬ੍ਰਿਟੇਨ, ਕੈਨੇਡਾ, ਅਮਰੀਕਾ ਤੇ "
             "ਖਾੜੀ ਦੇਸ਼ਾਂ ਵਿੱਚ ਵੱਸਦਾ ਹੈ। ਪਰਵਾਸ ਵਿੱਚ ਪੰਜਾਬੀ ਘਰ ਦੀ ਭਾਸ਼ਾ ਰਹਿੰਦੀ ਹੈ, ਪਰ ਦਫ਼ਤਰ "
             "ਵਿੱਚ ਅੰਗਰੇਜ਼ੀ। ਇਸੇ ਲਈ ਗੱਲਬਾਤ ਵਿੱਚ ਦੋ ਜਹਾਨ ਇੱਕੋ ਵਾਕ ਵਿੱਚ ਆ ਜਾਂਦੇ ਹਨ: ਵੱਡੇ ਸ਼ਹਿਰ "
             "ਦੀ ਨੌਕਰੀ ਅਤੇ ਪਿੰਡ ਦਾ ਵਿਆਹ। ਤੀਜੀ ਪੀੜ੍ਹੀ ਲਈ ਇਹ ਚੋਣ ਸੌਖੀ ਨਹੀਂ ਰਹਿੰਦੀ, ਅਤੇ ਉਹੀ "
             "ਸਵਾਲ ਇਸ ਭਾਸ਼ਾ ਦਾ ਸਭ ਤੋਂ ਦਿਲਚਸਪ ਹਿੱਸਾ ਹੈ।"),
    reading_gloss=("The Punjabi diaspora is three to five million people and lives in Britain, "
                   "Canada, the United States and the Gulf countries. Abroad, Punjabi remains "
                   "the language of the home, but the office speaks English. That is why two "
                   "worlds arrive in one sentence: a job in a big city and a wedding in the "
                   "village. For the third generation the choice is not simple, and that "
                   "question is the most interesting part of this language."),
    listening=("ਸਲਾਹਕਾਰ: ਮਾਪੇ ਚਾਹੁੰਦੇ ਹਨ ਕਿ ਮੁੰਡਾ ਵਿਆਹ ਪਿੰਡ ਵਿੱਚ ਕਰੇ।<br>"
               "ਵਿਚੋਲਾ: ਅਤੇ ਮੁੰਡਾ ਕੀ ਕਹਿੰਦਾ ਹੈ?<br>"
               "ਸਲਾਹਕਾਰ: ਉਹ ਕਹਿੰਦਾ ਹੈ ਕਿ ਨੌਕਰੀ ਕਾਰਨ ਉਹ ਦੋ ਹਫ਼ਤੇ ਤੋਂ ਵੱਧ ਨਹੀਂ ਰੁਕ ਸਕਦਾ।<br>"
               "ਵਿਚੋਲਾ: ਤਾਂ ਫਿਰ ਦੋਵਾਂ ਧਿਰਾਂ ਨੂੰ ਸਮਾਂ ਅਤੇ ਖ਼ਰਚ ਦੀ ਸੂਚੀ ਦੇਣੀ ਚਾਹੀਦੀ ਹੈ।<br>"
               "ਸਲਾਹਕਾਰ: ਸਹਿਮਤ ਹਾਂ, ਪਰ ਫੈਸਲਾ ਪਰਿਵਾਰ ਹੀ ਕਰੇਗਾ।"),
    listening_gloss=("Adviser: The parents want the son to marry in the village. Mediator: And "
                     "what does the son say? Adviser: He says that because of his job he cannot "
                     "stay more than two weeks. Mediator: Then both sides should be given a list "
                     "of the time and the expense. Adviser: I agree, but the family will make "
                     "the decision."),
    voice_tag=VOICE,
    idioms=[
        ("ਸੱਚ ਕਹਾਂ ਤਾਂ", "if I tell the truth", "frankly, between us"),
        ("ਗੱਲ ਦਾ ਮਤਲਬ", "the meaning of the matter", "what the point really is"),
        ("ਮਿੱਠੇ-ਕੌੜੇ ਬੋਲ", "sweet-and-bitter words", "plain speaking, both ways"),
        ("ਤੀਜੀ ਧਿਰ", "a third party", "a neutral outsider"),
        ("ਦੋਵਾਂ ਧਿਰਾਂ ਦੀ ਗੱਲ", "the case of both sides", "hearing both parties"),
        ("ਚੁੱਪ ਦਾ ਅਰਥ", "the meaning of the silence", "what is not said"),
        ("ਅੱਧੀ ਗੱਲ", "half a matter", "an unfinished point"),
        ("ਕੌੜੀ ਸੱਚਾਈ", "a bitter truth", "a truth nobody enjoys"),
        ("ਸੋਨੇ ਉੱਤੇ ਸੁਹਾਗਾ", "the extra on gold", "icing on the cake"),
        ("ਪਾਣੀ ਵਾਂਗ ਸਾਫ਼", "clear as water", "plain and above board"),
    ],
    mistakes=[
        ("ਉਹ ਬਹੁਤ ਪੜ੍ਹਿਆ ਲਿਖਿਆ ਆਦਮੀ ਹੈ।", "ਉਹ ਬਹੁਤ ਪੜ੍ਹਿਆ-ਲਿਖਿਆ ਆਦਮੀ ਹੈ।",
         "The reduplicated pair is written with a hyphen: ਪੜ੍ਹਿਆ-ਲਿਖਿਆ."),
        ("ਇਹ ਗੱਲ ਦਿਲ ਤੇ ਲੱਗੀ।", "ਇਹ ਗੱਲ ਦਿਲ ਨੂੰ ਲੱਗੀ।",
         "The idiom is ਦਿਲ ਨੂੰ ਲੱਗਣਾ, with ਨੂੰ."),
        ("ਉਸ ਦੀ ਬੋਲੀ ਵਿੱਚ ਮਿਠਾਸ ਹੈ ਅਤੇ ਸੱਚ।", "ਉਸ ਦੀ ਬੋਲੀ ਵਿੱਚ ਮਿਠਾਸ ਵੀ ਹੈ ਅਤੇ ਸੱਚ ਵੀ।",
         "The paired emphasis needs ਵੀ on both sides."),
    ],
    task_title="Mediate one family decision in Punjabi",
    task_instructions=("Write eight turns: two sides state their position, a third party "
                       "restates both fairly with ਇੱਕ ਧਿਰ … ਦੂਜੀ ਧਿਰ …, one speaker hedges with "
                       "ਅੱਧੀ ਗੱਲ or ਕੌੜੀ ਸੱਚਾਈ, and the exchange closes without a forced "
                       "verdict. Then add three lines saying what was agreed and what was left "
                       "open."),
)

THIRD["A1"] = [
    ("A1-U1", "A1-U1-L3", L("ਦਿਨ ਅਤੇ ਤਾਰੀਖ਼",
        "Days and dates are the first thing a beginner needs after greetings. A day of the week "
        "is a noun that takes ਹੈ, and ਅੱਜ / ਕੱਲ੍ਹ place it in time — ਕੱਲ੍ਹ is the same word for "
        "yesterday and tomorrow, so the verb decides which one you mean.",
        [V("ਸੋਮਵਾਰ", "somvar", "Monday", "noun"),
         V("ਅੱਜ", "ajj", "today", "adverb"),
         V("ਕੱਲ੍ਹ", "kallh", "yesterday, tomorrow", "adverb"),
         V("ਹਫ਼ਤਾ", "hafta", "week", "noun"),
         V("ਮਹੀਨਾ", "mahina", "month", "noun")],
        G("Saying the day",
          "ਅੱਜ ਸੋਮਵਾਰ ਹੈ · ਕੱਲ੍ਹ ਮੰਗਲਵਾਰ ਸੀ · ਅਗਲੇ ਹਫ਼ਤੇ",
          "The day of the week is a masculine noun, so it takes ਹੈ for today and ਸੀ for "
          "yesterday: ਅੱਜ ਸੋਮਵਾਰ ਹੈ, ਕੱਲ੍ਹ ਐਤਵਾਰ ਸੀ. ਅਗਲੇ ਹਫ਼ਤੇ and ਇਸ ਮਹੀਨੇ put the day in a "
          "week or a month, and the verb stays at the end.",
          [X("ਅੱਜ ਸੋਮਵਾਰ ਹੈ।", "ajj somvar hai.", "Today is Monday."),
           X("ਕੱਲ੍ਹ ਐਤਵਾਰ ਸੀ।", "kallh aitvar si.", "Yesterday was Sunday."),
           X("ਅਗਲੇ ਹਫ਼ਤੇ ਮੈਂ ਘਰ ਜਾਵਾਂਗਾ।", "agle hafte main ghar javanga.", "Next week I will go home.")],
          [("ਅੱਜ ਸੋਮਵਾਰ ਹਨ।", "ਅੱਜ ਸੋਮਵਾਰ ਹੈ।", "One day is singular: ਹੈ, not ਹਨ."),
           ("ਕੱਲ੍ਹ ਐਤਵਾਰ ਸਨ।", "ਕੱਲ੍ਹ ਐਤਵਾਰ ਸੀ।", "Singular past is ਸੀ.")]),
        [D("ਸਿਮਰਨ", "ਅੱਜ ਕੀ ਦਿਨ ਹੈ?", "ajj ki din hai?", "What day is it today?"),
         D("ਮਨਵੀਰ", "ਅੱਜ ਵੀਰਵਾਰ ਹੈ।", "ajj virvar hai.", "Today is Thursday."),
         D("ਸਿਮਰਨ", "ਕੱਲ੍ਹ ਕੀ ਸੀ?", "kallh ki si?", "What was yesterday?"),
         D("ਮਨਵੀਰ", "ਕੱਲ੍ਹ ਬੁੱਧਵਾਰ ਸੀ, ਅਤੇ ਅਗਲੇ ਹਫ਼ਤੇ ਛੁੱਟੀ ਹੈ।", "kallh budhvar si, ate agle hafte chhutti hai.", "Yesterday was Wednesday, and next week there is a holiday.")],
        WS("Days worksheet", [
            T("Say the day.", ["today is Monday", "yesterday was Sunday"],
              ["ਅੱਜ ਸੋਮਵਾਰ ਹੈ", "ਕੱਲ੍ਹ ਐਤਵਾਰ ਸੀ"]),
            T("Place it in time.", ["next week I will go home", "this month"],
              ["ਅਗਲੇ ਹਫ਼ਤੇ ਮੈਂ ਘਰ ਜਾਵਾਂਗਾ", "ਇਸ ਮਹੀਨੇ"]),
        ]))),
    ("A1-U2", "A1-U2-L3", L("ਰੰਗ ਅਤੇ ਚੀਜ਼ਾਂ",
        "A colour is an adjective and it agrees with the thing it describes: ਲਾਲ ਕਿਤਾਬ, ਲਾਲ "
        "ਫੁੱਲ, ਲਾਲ ਗੱਡੀ. The short form stays the same for masculine and feminine; what "
        "changes is the verb — ਹੈ for one thing, ਹਨ for many.",
        [V("ਲਾਲ", "lal", "red", "adjective"),
         V("ਹਰਾ", "hara", "green", "adjective"),
         V("ਨੀਲਾ", "nila", "blue", "adjective"),
         V("ਸਫ਼ੈਦ", "safaid", "white", "adjective"),
         V("ਛੋਟਾ", "chhota", "small", "adjective")],
        G("Colour and thing",
          "ਇਹ ਕਿਤਾਬ ਲਾਲ ਹੈ · ਇਹ ਫੁੱਲ ਲਾਲ ਹਨ · ਲਾਲ ਗੱਡੀ",
          "The colour stands before the noun and does not change: ਲਾਲ ਕਿਤਾਬ (a red book), ਲਾਲ "
          "ਫੁੱਲ (a red flower). In a sentence the noun decides the verb: ਇਹ ਲਾਲ ਹੈ against ਇਹ "
          "ਲਾਲ ਹਨ. ਸਫ਼ੈਦ and ਛੋਟਾ behave the same way.",
          [X("ਇਹ ਕਿਤਾਬ ਲਾਲ ਹੈ।", "ih kitab lal hai.", "This book is red."),
           X("ਇਹ ਫੁੱਲ ਹਰੇ ਹਨ।", "ih phull hare han.", "These flowers are green."),
           X("ਮੈਨੂੰ ਨੀਲੀ ਗੱਡੀ ਪਸੰਦ ਹੈ।", "mainun nili gaddi pasand hai.", "I like the blue car.")],
          [("ਇਹ ਫੁੱਲ ਲਾਲ ਹੈ।", "ਇਹ ਫੁੱਲ ਲਾਲ ਹਨ।", "A plural subject takes ਹਨ."),
           ("ਇਹ ਗੱਡੀ ਛੋਟਾ ਹੈ।", "ਇਹ ਗੱਡੀ ਛੋਟੀ ਹੈ।", "ਗੱਡੀ is feminine: ਛੋਟੀ.")]),
        [D("ਮਨਵੀਰ", "ਇਹ ਕੀ ਹੈ?", "ih ki hai?", "What is this?"),
         D("ਸਿਮਰਨ", "ਇਹ ਲਾਲ ਕਿਤਾਬ ਹੈ।", "ih lal kitab hai.", "This is a red book."),
         D("ਮਨਵੀਰ", "ਅਤੇ ਇਹ ਫੁੱਲ?", "ate ih phull?", "And these flowers?"),
         D("ਸਿਮਰਨ", "ਇਹ ਪੀਲੇ ਹਨ। ਮੈਨੂੰ ਪੀਲਾ ਰੰਗ ਪਸੰਦ ਹੈ।", "ih pile han. mainun pila rang pasand hai.", "These are yellow. I like the colour yellow.")],
        WS("Colour worksheet", [
            T("Describe the thing.", ["this book is red", "these flowers are green"],
              ["ਇਹ ਕਿਤਾਬ ਲਾਲ ਹੈ", "ਇਹ ਫੁੱਲ ਹਰੇ ਹਨ"]),
            T("Say what you like.", ["I like the blue car", "I like the colour yellow"],
              ["ਮੈਨੂੰ ਨੀਲੀ ਗੱਡੀ ਪਸੰਦ ਹੈ", "ਮੈਨੂੰ ਪੀਲਾ ਰੰਗ ਪਸੰਦ ਹੈ"]),
        ]))),
    ("A1-U3", "A1-U3-L3", L("ਰੋਜ਼ ਦਾ ਕੰਮ",
        "Habits are said with the present tense and the word ਰੋਜ਼. The verb agrees with the "
        "speaker: ਉੱਠਦਾ ਹਾਂ for a man, ਉੱਠਦੀ ਹਾਂ for a woman, ਉੱਠਦੇ ਹਾਂ for a group — and the "
        "time of day stands before the verb.",
        [V("ਉੱਠਣਾ", "uthna", "to get up", "verb"),
         V("ਨਹਾਉਣਾ", "nahuna", "to bathe", "verb"),
         V("ਪੜ੍ਹਨਾ", "parhna", "to study, to read", "verb"),
         V("ਖਾਣਾ", "khana", "to eat", "verb"),
         V("ਸੌਣਾ", "sauna", "to sleep", "verb")],
        G("A daily routine",
          "ਮੈਂ ਰੋਜ਼ ਛੇ ਵਜੇ ਉੱਠਦਾ ਹਾਂ · ਪੜ੍ਹਨ ਤੋਂ ਬਾਅਦ ਖਾਂਦਾ ਹਾਂ · ਰਾਤ ਨੂੰ ਸੌਂਦਾ ਹਾਂ",
          "The habitual present takes the -ਦਾ/-ਦੀ ending plus ਹਾਂ: ਉੱਠਦਾ ਹਾਂ, ਉੱਠਦੀ ਹਾਂ. ਜਦੋਂ "
          "(when) and ਤੋਂ ਬਾਅਦ (after) order the day, and the whole routine keeps the verb last.",
          [X("ਮੈਂ ਰੋਜ਼ ਛੇ ਵਜੇ ਉੱਠਦਾ ਹਾਂ।", "main roj chhe vaje uthda han.", "I get up at six every day."),
           X("ਪੜ੍ਹਨ ਤੋਂ ਬਾਅਦ ਮੈਂ ਖਾਂਦਾ ਹਾਂ।", "parhan to baad main khanda han.", "After studying I eat."),
           X("ਰਾਤ ਨੂੰ ਦਸ ਵਜੇ ਸੌਂਦੀ ਹਾਂ।", "raat nun das vaje saundi han.", "I sleep at ten at night.")],
          [("ਮੈਂ ਰੋਜ਼ ਛੇ ਵਜੇ ਉੱਠਦਾ ਹਾਂ ਹਾਂ।", "ਮੈਂ ਰੋਜ਼ ਛੇ ਵਜੇ ਉੱਠਦਾ ਹਾਂ।",
            "One ਹਾਂ is the whole verb; it is not doubled."),
           ("ਮੈਂ ਰੋਜ਼ ਛੇ ਵਜੇ ਉੱਠਦਾ।", "ਮੈਂ ਰੋਜ਼ ਛੇ ਵਜੇ ਉੱਠਦਾ ਹਾਂ।",
            "The first and second person keep ਹਾਂ: ਉੱਠਦਾ ਹਾਂ.")]),
        [D("ਸਿਮਰਨ", "ਤੁਸੀਂ ਰੋਜ਼ ਕੀ ਕਰਦੇ ਹੋ?", "tusin roj ki karde ho?", "What do you do every day?"),
         D("ਮਨਵੀਰ", "ਮੈਂ ਰੋਜ਼ ਛੇ ਵਜੇ ਉੱਠਦਾ ਹਾਂ ਅਤੇ ਨਹਾਉਂਦਾ ਹਾਂ।", "main roj chhe vaje uthda han ate nahunda han.", "I get up at six every day and bathe."),
         D("ਸਿਮਰਨ", "ਫਿਰ?", "phir?", "Then?"),
         D("ਮਨਵੀਰ", "ਪੜ੍ਹਨ ਤੋਂ ਬਾਅਦ ਖਾਂਦਾ ਹਾਂ, ਅਤੇ ਰਾਤ ਨੂੰ ਦਸ ਵਜੇ ਸੌਂਦਾ ਹਾਂ।", "parhan to baad khanda han, ate raat nun das vaje saunda han.", "After studying I eat, and at night I sleep at ten.")],
        WS("Routine worksheet", [
            T("Say the routine.", ["I get up at six every day", "after studying I eat"],
              ["ਮੈਂ ਰੋਜ਼ ਛੇ ਵਜੇ ਉੱਠਦਾ ਹਾਂ", "ਪੜ੍ਹਨ ਤੋਂ ਬਾਅਦ ਮੈਂ ਖਾਂਦਾ ਹਾਂ"]),
            T("Say when.", ["I sleep at ten at night", "in the morning I bathe"],
              ["ਰਾਤ ਨੂੰ ਦਸ ਵਜੇ ਸੌਂਦੀ ਹਾਂ", "ਸਵੇਰੇ ਮੈਂ ਨਹਾਉਂਦਾ ਹਾਂ"]),
        ]))),
]

THIRD["A2"] = [
    ("pa-a2-u1", "pa-a2-l7", L("ਹੋਟਲ ਅਤੇ ਕਮਰਾ",
        "Booking a room is the first thing a traveller does in Punjabi. The request uses ਚਾਹੀਦਾ "
        "ਹੈ or ਮਿਲ ਸਕਦਾ ਹੈ, the price is asked with ਕਿੰਨਾ ਹੈ, and everything the desk gives you "
        "— ਚਾਬੀ, ਰਸੀਦ, ਪਾਣੀ — is offered with ਲਓ or ਦਿਓ.",
        [V("ਹੋਟਲ", "hotel", "hotel", "noun"),
         V("ਕਮਰਾ", "kamra", "room", "noun"),
         V("ਚਾਬੀ", "chabi", "key", "noun"),
         V("ਕਿਰਾਇਆ", "kiraia", "rent, charge", "noun"),
         V("ਬੁਕਿੰਗ", "buking", "booking", "noun")],
        G("Asking for a room",
          "ਕੀ ਇੱਕ ਕਮਰਾ ਖ਼ਾਲੀ ਹੈ? · ਕਿਰਾਇਆ ਕਿੰਨਾ ਹੈ? · ਇੱਕ ਰਾਤ ਲਈ",
          "The polite question opens with ਕੀ … ਹੈ or ਮਿਲ ਸਕਦਾ ਹੈ: ਕਮਰਾ ਮਿਲ ਸਕਦਾ ਹੈ? The price "
          "takes ਕਿੰਨਾ ਹੈ (masculine, agreeing with ਕਿਰਾਇਆ), the period takes ਲਈ, and a request "
          "for something is ਦਿਓ while an offer is ਲਓ.",
          [X("ਕੀ ਇੱਕ ਕਮਰਾ ਖ਼ਾਲੀ ਹੈ?", "ki ikk kamra khali hai?", "Is a room free?"),
           X("ਇੱਕ ਰਾਤ ਦਾ ਕਿਰਾਇਆ ਕਿੰਨਾ ਹੈ?", "ikk raat da kiraia kinna hai?", "How much is the charge for one night?"),
           X("ਚਾਬੀ ਦਿਓ, ਅਤੇ ਗਰਮ ਪਾਣੀ ਦਾ ਪਤਾ ਦੱਸੋ।", "chabi dio, ate garam pani da pata dasso.", "Give me the key, and tell me about the hot water.")],
          [("ਕਿਰਾਇਆ ਕਿੰਨੀ ਹੈ?", "ਕਿਰਾਇਆ ਕਿੰਨਾ ਹੈ?", "ਕਿਰਾਇਆ is masculine: ਕਿੰਨਾ."),
           ("ਕੀ ਕਮਰਾ ਖ਼ਾਲੀ ਹੋ?", "ਕੀ ਕਮਰਾ ਖ਼ਾਲੀ ਹੈ?", "A question keeps ਹੈ, not ਹੋ.")]),
        [D("ਗਾਹਕ", "ਕੀ ਤੁਹਾਡੇ ਹੋਟਲ ਵਿੱਚ ਕਮਰਾ ਖ਼ਾਲੀ ਹੈ?", "ki tuhade hotel vich kamra khali hai?", "Is a room free in your hotel?"),
         D("ਮੈਨੇਜਰ", "ਹਾਂ, ਇੱਕ ਕਮਰਾ ਹੈ। ਕਿੰਨੀ ਰਾਤ ਲਈ?", "han, ikk kamra hai. kinni raat lai?", "Yes, there is one room. For how many nights?"),
         D("ਗਾਹਕ", "ਦੋ ਰਾਤਾਂ ਲਈ। ਕਿਰਾਇਆ ਕਿੰਨਾ ਹੈ?", "do raatan lai. kiraia kinna hai?", "For two nights. How much is the charge?"),
         D("ਮੈਨੇਜਰ", "ਇੱਕ ਹਜ਼ਾਰ ਰੁਪਏ ਰਾਤ ਦਾ। ਇਹ ਚਾਬੀ ਲਓ।", "ikk hazar rupae raat da. ih chabi lo.", "A thousand rupees a night. Take this key.")],
        WS("Hotel worksheet", [
            T("Ask for the room.", ["is a room free?", "how much is the charge for one night?"],
              ["ਕੀ ਇੱਕ ਕਮਰਾ ਖ਼ਾਲੀ ਹੈ?", "ਇੱਕ ਰਾਤ ਦਾ ਕਿਰਾਇਆ ਕਿੰਨਾ ਹੈ?"]),
            T("Ask and answer.", ["for two nights", "take this key"],
              ["ਦੋ ਰਾਤਾਂ ਲਈ", "ਇਹ ਚਾਬੀ ਲਓ"]),
        ]))),
    ("pa-a2-u2", "pa-a2-l8", L("ਕਪੜੇ ਅਤੇ ਨਾਪ",
        "Clothes shopping needs three words: ਨਾਪ (size), ਰੰਗ (colour) and ਬਦਲਣਾ (to exchange). "
        "The complaint is stated plainly — ਇਹ ਛੋਟਾ ਹੈ — and the request follows with ਦਿਓ or ਬਦਲ "
        "ਦਿਓ, which is how a shop turns a fault into a purchase.",
        [V("ਕੁੜਤਾ", "kurta", "kurta", "noun"),
         V("ਪਜਾਮਾ", "pajama", "pyjama, trousers", "noun"),
         V("ਨਾਪ", "nap", "size, measure", "noun"),
         V("ਵੱਡਾ", "vadda", "big, large", "adjective"),
         V("ਬਦਲਣਾ", "badalna", "to change, to exchange", "verb")],
        G("Sizes and exchange",
          "ਇਹ ਛੋਟਾ ਹੈ · ਵੱਡਾ ਦਿਓ · ਬਦਲ ਸਕਦੇ ਹੋ?",
          "The size word agrees with the garment: ਕੁੜਤਾ ਛੋਟਾ ਹੈ, ਕੁੜਤੀ ਛੋਟੀ ਹੈ. A wish is "
          "stated with ਦਿਓ (ਵੱਡਾ ਦਿਓ), and the question ਬਦਲ ਸਕਦੇ ਹੋ? asks whether the shop will "
          "exchange — the modal ਸਕਣਾ stays in the middle of the verb.",
          [X("ਇਹ ਕੁੜਤਾ ਛੋਟਾ ਹੈ, ਵੱਡਾ ਦਿਓ।", "ih kurta chhota hai, vadda dio.", "This kurta is small, give me a larger one."),
           X("ਕੀ ਇਸ ਨੂੰ ਬਦਲ ਸਕਦੇ ਹੋ?", "ki is nun badal sakde ho?", "Can you exchange this?"),
           X("ਇਸ ਦਾ ਨਾਪ ਬਾਰਾਂ ਹੈ।", "is da nap baran hai.", "Its size is twelve.")],
          [("ਇਹ ਕੁੜਤੀ ਛੋਟਾ ਹੈ।", "ਇਹ ਕੁੜਤੀ ਛੋਟੀ ਹੈ।", "ਕੁੜਤੀ is feminine: ਛੋਟੀ."),
           ("ਮੈਂ ਇਸ ਨੂੰ ਬਦਲ ਕਰਾਂਗਾ।", "ਮੈਂ ਇਸ ਨੂੰ ਬਦਲਾਂਗਾ।", "ਬਦਲਣਾ is one verb: ਬਦਲਾਂਗਾ, not ਬਦਲ ਕਰਾਂਗਾ.")]),
        [D("ਗਾਹਕ", "ਇਹ ਕੁੜਤਾ ਛੋਟਾ ਹੈ। ਵੱਡਾ ਹੈ?", "ih kurta chhota hai. vadda hai?", "This kurta is small. Is there a bigger one?"),
         D("ਦੁਕਾਨਦਾਰ", "ਹਾਂ, ਇਹ ਲਓ। ਨਾਪ ਚੌਦਾਂ ਹੈ।", "han, ih lo. nap chaudan hai.", "Yes, take this one. The size is fourteen."),
         D("ਗਾਹਕ", "ਰੰਗ ਦੂਜਾ ਹੈ, ਬਦਲ ਸਕਦੇ ਹੋ?", "rang duja hai, badal sakde ho?", "The colour is different, can you exchange it?"),
         D("ਦੁਕਾਨਦਾਰ", "ਨੀਲਾ ਵੀ ਹੈ। ਉਹੀ ਨਾਪ ਵਿੱਚ।", "nila vi hai. uhi nap vich.", "There is a blue one too. In the same size.")],
        WS("Clothes worksheet", [
            T("Report the size.", ["this kurta is small", "its size is twelve"],
              ["ਇਹ ਕੁੜਤਾ ਛੋਟਾ ਹੈ", "ਇਸ ਦਾ ਨਾਪ ਬਾਰਾਂ ਹੈ"]),
            T("Ask for the change.", ["give me a larger one", "can you exchange this?"],
              ["ਵੱਡਾ ਦਿਓ", "ਕੀ ਇਸ ਨੂੰ ਬਦਲ ਸਕਦੇ ਹੋ?"]),
        ]))),
    ("pa-a2-u3", "pa-a2-l9", L("ਮੌਸਮ ਅਤੇ ਰੁੱਤਾਂ",
        "Weather in Punjabi is built from a noun and a verb of motion: ਬਾਰਿਸ਼ ਪੈਣੀ (rain to "
        "fall), ਗਰਮੀ ਲੱਗਣੀ (heat to strike), ਬੱਦਲ ਛਾਉਣਾ (clouds to spread). The noun decides "
        "the gender, so the verb has to follow it.",
        [V("ਮੌਸਮ", "mausam", "weather", "noun"),
         V("ਬਾਰਿਸ਼", "barish", "rain", "noun"),
         V("ਗਰਮੀ", "garmi", "heat", "noun"),
         V("ਸਰਦੀ", "sardi", "cold, winter", "noun"),
         V("ਬੱਦਲ", "baddal", "cloud", "noun")],
        G("Talking about the weather",
          "ਬਾਰਿਸ਼ ਪੈ ਰਹੀ ਹੈ · ਗਰਮੀ ਲੱਗ ਰਹੀ ਹੈ · ਬੱਦਲ ਛਾਏ ਹੋਏ ਹਨ",
          "The noun carries the gender: ਬਾਰਿਸ਼ is feminine (ਪੈ ਰਹੀ ਹੈ), ਗਰਮੀ and ਸਰਦੀ are "
          "feminine too (ਲੱਗ ਰਹੀ ਹੈ), while ਬੱਦਲ is masculine and plural (ਛਾਏ ਹੋਏ ਹਨ). ਰੁੱਤ "
          "(season) is feminine: ਰੁੱਤ ਬਦਲ ਗਈ.",
          [X("ਅੱਜ ਬਾਰਿਸ਼ ਪੈ ਰਹੀ ਹੈ।", "ajj barish pai rahi hai.", "It is raining today."),
           X("ਗਰਮੀ ਬਹੁਤ ਲੱਗ ਰਹੀ ਹੈ।", "garmi bahut lag rahi hai.", "The heat is striking hard."),
           X("ਸਰਦੀ ਵਿੱਚ ਬੱਦਲ ਛਾਏ ਹੋਏ ਹਨ।", "sardi vich baddal chhae hoe han.", "In the cold the clouds are spread out.")],
          [("ਬਾਰਿਸ਼ ਪੈ ਰਿਹਾ ਹੈ।", "ਬਾਰਿਸ਼ ਪੈ ਰਹੀ ਹੈ।", "ਬਾਰਿਸ਼ is feminine: ਰਹੀ."),
           ("ਗਰਮੀ ਲੱਗ ਰਿਹਾ ਹੈ।", "ਗਰਮੀ ਲੱਗ ਰਹੀ ਹੈ।", "ਗਰਮੀ is feminine: ਰਹੀ.")]),
        [D("ਮਨਵੀਰ", "ਅੱਜ ਮੌਸਮ ਕਿਹੋ ਜਿਹਾ ਹੈ?", "ajj mausam kiho jiha hai?", "What is the weather like today?"),
         D("ਸਿਮਰਨ", "ਬੱਦਲ ਛਾਏ ਹੋਏ ਹਨ, ਅਤੇ ਬਾਰਿਸ਼ ਪੈ ਰਹੀ ਹੈ।", "baddal chhae hoe han, ate barish pai rahi hai.", "The clouds are spread out, and it is raining."),
         D("ਮਨਵੀਰ", "ਕੱਲ੍ਹ ਵੀ ਪਵੇਗੀ?", "kallh vi pavegi?", "Will it rain tomorrow too?"),
         D("ਸਿਮਰਨ", "ਉਮੀਦ ਹੈ ਨਹੀਂ, ਪਰ ਰੁੱਤ ਬਦਲ ਗਈ ਹੈ।", "umid hai nahin, par rutt badal gai hai.", "I hope not, but the season has changed.")],
        WS("Weather worksheet", [
            T("Describe the weather.", ["it is raining today", "the clouds are spread out"],
              ["ਅੱਜ ਬਾਰਿਸ਼ ਪੈ ਰਹੀ ਹੈ", "ਬੱਦਲ ਛਾਏ ਹੋਏ ਹਨ"]),
            T("Talk about the season.", ["the season has changed", "the heat is striking hard"],
              ["ਰੁੱਤ ਬਦਲ ਗਈ ਹੈ", "ਗਰਮੀ ਬਹੁਤ ਲੱਗ ਰਹੀ ਹੈ"]),
        ]))),
]

THIRD["B1"] = [
    ("pa-b1-u1", "pa-b1-l7", L("ਯਾਦਾਂ ਅਤੇ ਬਚਪਨ",
        "Telling a memory needs ਜਦੋਂ … ਤਦੋਂ (when … then) and the habitual past in ਸਾਂ: ਅਸੀਂ "
        "ਰਹਿੰਦੇ ਸਾਂ (we used to live). The scene is set first, then the event, and the verbs of "
        "the memory agree with their own subjects.",
        [V("ਯਾਦ", "yad", "memory", "noun"),
         V("ਬਚਪਨ", "bachpan", "childhood", "noun"),
         V("ਰਹਿੰਦੇ ਸਾਂ", "rahinde san", "we used to live", "phrase"),
         V("ਪੁਰਾਣਾ", "purana", "old, former", "adjective"),
         V("ਸੰਭਾਲਣਾ", "sambhalna", "to keep, to look after", "verb")],
        G("Setting the scene of a memory",
          "ਜਦੋਂ ਮੈਂ ਛੋਟਾ ਸੀ, ਤਦੋਂ … · ਅਸੀਂ ਰਹਿੰਦੇ ਸਾਂ · ਉਹ ਦਿਨ ਯਾਦ ਆਉਂਦੇ ਹਨ",
          "ਜਦੋਂ opens the scene and ਤਦੋਂ answers it. The habitual past takes ਸਾਂ for we/I "
          "(ਰਹਿੰਦੇ ਸਾਂ), ਸੀ for one person, and ਸਨ for they. ਯਾਦ ਆਉਣਾ is the fixed phrase for a "
          "memory coming back: ਉਹ ਦਿਨ ਯਾਦ ਆਉਂਦੇ ਹਨ.",
          [X("ਜਦੋਂ ਮੈਂ ਛੋਟਾ ਸੀ, ਅਸੀਂ ਪਿੰਡ ਵਿੱਚ ਰਹਿੰਦੇ ਸਾਂ।", "jadon main chhota si, asin pind vich rahinde san.", "When I was small, we used to live in the village."),
           X("ਬਚਪਨ ਵਿੱਚ ਅਸੀਂ ਨਦੀ ਵਿੱਚ ਨਹਾਉਂਦੇ ਸਾਂ।", "bachpan vich asin nadi vich nahunde san.", "In childhood we used to bathe in the river."),
           X("ਉਹ ਦਿਨ ਅੱਜ ਵੀ ਯਾਦ ਆਉਂਦੇ ਹਨ।", "uh din ajj vi yad aunde han.", "Those days come back to memory even today.")],
          [("ਜਦੋਂ ਮੈਂ ਛੋਟਾ ਸੀ, ਅਸੀਂ ਰਹਿੰਦੇ ਸੀ।", "ਜਦੋਂ ਮੈਂ ਛੋਟਾ ਸੀ, ਅਸੀਂ ਰਹਿੰਦੇ ਸਾਂ।", "For ਅਸੀਂ the habitual past is ਸਾਂ."),
           ("ਉਹ ਦਿਨ ਯਾਦ ਆਉਂਦਾ ਹਨ।", "ਉਹ ਦਿਨ ਯਾਦ ਆਉਂਦੇ ਹਨ।", "ਦਿਨ is plural masculine: ਆਉਂਦੇ.")]),
        [D("ਸੀਮਾ", "ਤੁਸੀਂ ਬਚਪਨ ਵਿੱਚ ਕਿੱਥੇ ਰਹਿੰਦੇ ਸੀ?", "tusin bachpan vich kithe rahinde si?", "Where did you live in childhood?"),
         D("ਰਾਜ", "ਜਦੋਂ ਮੈਂ ਛੋਟਾ ਸੀ, ਅਸੀਂ ਮੋਗੇ ਰਹਿੰਦੇ ਸਾਂ।", "jadon main chhota si, asin moge rahinde san.", "When I was small, we used to live in Moga."),
         D("ਸੀਮਾ", "ਉਹ ਘਰ ਅੱਜ ਵੀ ਹੈ?", "uh ghar ajj vi hai?", "Is that house still there?"),
         D("ਰਾਜ", "ਹੈ, ਪਰ ਪੁਰਾਣਾ ਹੋ ਗਿਆ। ਦਾਦੀ ਨੇ ਸੰਭਾਲਿਆ ਹੋਇਆ ਹੈ।", "hai, par purana ho gia. dadi ne sambhalia hoia hai.", "It is, but it has grown old. Grandmother has kept it up.")],
        WS("Memory worksheet", [
            T("Set the scene.", ["when I was small, we used to live in the village", "in childhood we used to bathe in the river"],
              ["ਜਦੋਂ ਮੈਂ ਛੋਟਾ ਸੀ, ਅਸੀਂ ਪਿੰਡ ਵਿੱਚ ਰਹਿੰਦੇ ਸਾਂ", "ਬਚਪਨ ਵਿੱਚ ਅਸੀਂ ਨਦੀ ਵਿੱਚ ਨਹਾਉਂਦੇ ਸਾਂ"]),
            T("Close the memory.", ["those days come back to memory", "the house has grown old"],
              ["ਉਹ ਦਿਨ ਯਾਦ ਆਉਂਦੇ ਹਨ", "ਘਰ ਪੁਰਾਣਾ ਹੋ ਗਿਆ ਹੈ"]),
        ]))),
    ("pa-b1-u2", "pa-b1-l8", L("ਸਹਿਮਤੀ ਅਤੇ ਨਰਮ ਅਸਹਿਮਤੀ",
        "Agreeing is ਸਹਿਮਤ ਹੋਣਾ and disagreeing politely is done in three moves: accept the "
        "person, name the doubt, offer an alternative. ਸਹਿਮਤ takes ਨਾਲ (ਸਹਿਮਤ ਹਾਂ), and the "
        "softer refusal uses ਇੱਕ ਗੱਲ ਹੈ or ਸੋਚਣਾ ਪਵੇਗਾ.",
        [V("ਸਹਿਮਤ", "sahmat", "agreeing", "adjective"),
         V("ਰਾਏ", "rae", "opinion", "noun"),
         V("ਨਰਮੀ", "narmi", "gentleness", "noun"),
         V("ਸੋਚਣਾ", "sochna", "to think, to consider", "verb"),
         V("ਵੱਖਰਾ", "vakhra", "separate, different", "adjective")],
        G("Agreeing and disagreeing",
          "ਮੈਂ ਸਹਿਮਤ ਹਾਂ · ਪਰ ਇੱਕ ਗੱਲ ਹੈ · ਸੋਚਣਾ ਪਵੇਗਾ",
          "Agreement is ਮੈਂ ਸਹਿਮਤ ਹਾਂ (or ਸਹਿਮਤ ਨਹੀਂ ਹਾਂ). The polite objection introduces one "
          "doubt with ਪਰ ਇੱਕ ਗੱਲ ਹੈ, and a refusal to decide yet is ਸੋਚਣਾ ਪਵੇਗਾ — the "
          "obligation form with ਪਵੇਗਾ. ਤੁਹਾਡੀ ਰਾਏ ਵੱਖਰੀ ਹੋ ਸਕਦੀ ਹੈ leaves the other person "
          "their view.",
          [X("ਮੈਂ ਤੁਹਾਡੀ ਗੱਲ ਨਾਲ ਸਹਿਮਤ ਹਾਂ।", "main tuhadi gal nal sahmat han.", "I agree with your point."),
           X("ਪਰ ਇੱਕ ਗੱਲ ਹੈ: ਖ਼ਰਚਾ ਵੱਧ ਹੋਵੇਗਾ।", "par ikk gal hai: kharcha vaddh hovega.", "But there is one thing: the cost will rise."),
           X("ਮੈਨੂੰ ਸੋਚਣਾ ਪਵੇਗਾ।", "mainun sochna pavega.", "I will have to think it over.")],
          [("ਮੈਂ ਤੁਹਾਡੀ ਗੱਲ ਨੂੰ ਸਹਿਮਤ ਹਾਂ।", "ਮੈਂ ਤੁਹਾਡੀ ਗੱਲ ਨਾਲ ਸਹਿਮਤ ਹਾਂ।", "ਸਹਿਮਤ takes ਨਾਲ, not ਨੂੰ."),
           ("ਮੈਂ ਸੋਚਣਾ ਪਵੇਗਾ।", "ਮੈਨੂੰ ਸੋਚਣਾ ਪਵੇਗਾ।", "The obligation is dative: ਮੈਨੂੰ … ਪਵੇਗਾ.")]),
        [D("ਸੀਮਾ", "ਮੇਰੀ ਰਾਏ ਹੈ ਕਿ ਅਸੀਂ ਯੋਜਨਾ ਬਦਲੀਏ।", "meri rae hai ki asin yojna badalie.", "My opinion is that we change the plan."),
         D("ਰਾਜ", "ਮੈਂ ਤੁਹਾਡੀ ਗੱਲ ਨਾਲ ਸਹਿਮਤ ਹਾਂ, ਪਰ ਇੱਕ ਗੱਲ ਹੈ।", "main tuhadi gal nal sahmat han, par ikk gal hai.", "I agree with your point, but there is one thing."),
         D("ਸੀਮਾ", "ਦੱਸੋ।", "dasso.", "Tell me."),
         D("ਰਾਜ", "ਖ਼ਰਚਾ ਵੱਧ ਹੋਵੇਗਾ। ਮੈਨੂੰ ਸੋਚਣਾ ਪਵੇਗਾ।", "kharcha vaddh hovega. mainun sochna pavega.", "The cost will be higher. I will have to think it over.")],
        WS("Agreement worksheet", [
            T("Agree and qualify.", ["I agree with your point", "but there is one thing"],
              ["ਮੈਂ ਤੁਹਾਡੀ ਗੱਲ ਨਾਲ ਸਹਿਮਤ ਹਾਂ", "ਪਰ ਇੱਕ ਗੱਲ ਹੈ"]),
            T("Hold your decision.", ["I will have to think it over", "your opinion may be different"],
              ["ਮੈਨੂੰ ਸੋਚਣਾ ਪਵੇਗਾ", "ਤੁਹਾਡੀ ਰਾਏ ਵੱਖਰੀ ਹੋ ਸਕਦੀ ਹੈ"]),
        ]))),
    ("pa-b1-u3", "pa-b1-l9", L("ਜੇ ਯੋਜਨਾ ਬਦਲੇ",
        "A plan that depends on something uses ਜੇ … ਤਾਂ with the subjunctive (ਪਵੇ) and the "
        "future (ਜਾਵਾਂਗੇ). When the reason is outside your control, Punjabi says ਮਜਬੂਰੀ ਕਾਰਨ, "
        "and the work of changing the plan is ਬਦਲਣੀ ਪਵੇਗੀ.",
        [V("ਯੋਜਨਾ", "yojna", "plan", "noun"),
         V("ਤਬਦੀਲੀ", "tabdili", "change", "noun"),
         V("ਮਜਬੂਰੀ", "majburi", "compulsion, constraint", "noun"),
         V("ਪਵੇ", "pave", "may fall (subjunctive)", "verb"),
         V("ਰੱਦ", "radd", "cancelled", "adjective")],
        G("If the plan changes",
          "ਜੇ ਮੀਂਹ ਪਵੇ ਤਾਂ ਅਸੀਂ ਨਹੀਂ ਜਾਵਾਂਗੇ · ਮਜਬੂਰੀ ਕਾਰਨ · ਯੋਜਨਾ ਬਦਲਣੀ ਪਵੇਗੀ",
          "ਜੇ takes the subjunctive (ਪਵੇ, ਹੋਵੇ, ਆਵੇ) and ਤਾਂ takes the future (ਜਾਵਾਂਗੇ, ਹੋਵੇਗਾ). "
          "ਮਜਬੂਰੀ ਕਾਰਨ gives the reason without blaming anybody, and ਤਬਦੀਲੀ ਕਰਨੀ ਪਵੇਗੀ states "
          "what has to be done.",
          [X("ਜੇ ਮੀਂਹ ਪਵੇ ਤਾਂ ਅਸੀਂ ਨਹੀਂ ਜਾਵਾਂਗੇ।", "je minh pave tan asin nahin javange.", "If it rains we will not go."),
           X("ਮਜਬੂਰੀ ਕਾਰਨ ਮੈਂ ਨਹੀਂ ਆ ਸਕਾਂਗਾ।", "majburi karan main nahin a sakanga.", "Because of a compulsion I will not be able to come."),
           X("ਯੋਜਨਾ ਵਿੱਚ ਤਬਦੀਲੀ ਕਰਨੀ ਪਵੇਗੀ।", "yojna vich tabdili karni pavegi.", "A change will have to be made in the plan.")],
          [("ਜੇ ਮੀਂਹ ਪਵੇਗਾ ਤਾਂ ਅਸੀਂ ਨਹੀਂ ਜਾਵਾਂਗੇ।", "ਜੇ ਮੀਂਹ ਪਵੇ ਤਾਂ ਅਸੀਂ ਨਹੀਂ ਜਾਵਾਂਗੇ।", "After ਜੇ the verb is subjunctive: ਪਵੇ, not ਪਵੇਗਾ."),
           ("ਯੋਜਨਾ ਬਦਲਣਾ ਪਵੇਗੀ।", "ਯੋਜਨਾ ਬਦਲਣੀ ਪਵੇਗੀ।", "ਯੋਜਨਾ is feminine: ਬਦਲਣੀ ਪਵੇਗੀ.")]),
        [D("ਰਾਜ", "ਕੱਲ੍ਹ ਦਾ ਪ੍ਰੋਗਰਾਮ ਪੱਕਾ ਹੈ?", "kallh da program pakka hai?", "Is tomorrow's programme fixed?"),
         D("ਸੀਮਾ", "ਜੇ ਮੀਂਹ ਪਵੇ ਤਾਂ ਨਹੀਂ।", "je minh pave tan nahin.", "If it rains, no."),
         D("ਰਾਜ", "ਤਾਂ ਫਿਰ ਕੀ ਕਰੀਏ?", "tan phir ki karie?", "Then what shall we do?"),
         D("ਸੀਮਾ", "ਮਜਬੂਰੀ ਕਾਰਨ ਯੋਜਨਾ ਬਦਲਣੀ ਪਵੇਗੀ। ਅੰਦਰ ਦਾ ਹਾਲ ਲੈ ਲਵਾਂਗੇ।", "majburi karan yojna badalni pavegi. andar da hal lai lavange.", "Because of the constraint we will have to change the plan. We will take the indoor hall.")],
        WS("Plans worksheet", [
            T("State the condition.", ["if it rains we will not go", "if tomorrow's programme is fixed"],
              ["ਜੇ ਮੀਂਹ ਪਵੇ ਤਾਂ ਅਸੀਂ ਨਹੀਂ ਜਾਵਾਂਗੇ", "ਜੇ ਕੱਲ੍ਹ ਦਾ ਪ੍ਰੋਗਰਾਮ ਪੱਕਾ ਹੋਵੇ"]),
            T("Change the plan.", ["a change will have to be made in the plan", "because of a compulsion I will not be able to come"],
              ["ਯੋਜਨਾ ਵਿੱਚ ਤਬਦੀਲੀ ਕਰਨੀ ਪਵੇਗੀ", "ਮਜਬੂਰੀ ਕਾਰਨ ਮੈਂ ਨਹੀਂ ਆ ਸਕਾਂਗਾ"]),
        ]))),
]

THIRD["B2"] = [
    ("pa-b2-u1", "pa-b2-l7", L("ਰਿਪੋਰਟ ਅਤੇ ਬਿਆਨ",
        "Reporting what somebody said puts the whole sentence after ਕਿ, and the pronouns shift: "
        "the speaker's ਮੈਂ becomes ਉਹ, my becomes his. The tense moves back one step, and the "
        "word ਹਵਾਲਾ names the source, which is what makes a report checkable.",
        [V("ਬਿਆਨ", "bian", "statement", "noun"),
         V("ਹਵਾਲਾ", "havala", "reference, citation", "noun"),
         V("ਅਧਿਕਾਰੀ", "adhikari", "officer, official", "noun"),
         V("ਸਬੰਧਤ", "sabdhat", "concerned, related", "adjective"),
         V("ਸਪਸ਼ਟ", "spasht", "clear, explicit", "adjective")],
        G("Reported speech and sources",
          "ਅਧਿਕਾਰੀ ਨੇ ਕਿਹਾ ਕਿ ਉਹ ਜਾਂਚ ਕਰੇਗਾ · ਹਵਾਲੇ ਅਨੁਸਾਰ · ਸਪਸ਼ਟ ਕੀਤਾ ਗਿਆ",
          "The reporting verb comes first and everything said follows ਕਿ: ਉਸ ਨੇ ਕਿਹਾ ਕਿ ਸਬੰਧਤ "
          "ਦਫ਼ਤਰ ਜਾਂਚ ਕਰੇਗਾ. Inside the report the speaker's ਮੈਂ turns into ਉਹ and ਮੇਰਾ into "
          "ਉਸ ਦਾ. The passive ਹਵਾਲੇ ਅਨੁਸਾਰ ਦੱਸਿਆ ਗਿਆ keeps the source unnamed but present.",
          [X("ਅਧਿਕਾਰੀ ਨੇ ਕਿਹਾ ਕਿ ਉਹ ਸਬੰਧਤ ਦਫ਼ਤਰ ਵਿੱਚ ਜਾਂਚ ਕਰੇਗਾ।", "adhikari ne kiha ki uh sabdhat daftar vich janch karega.", "The officer said that he would investigate in the concerned office."),
           X("ਹਵਾਲੇ ਅਨੁਸਾਰ ਰਿਪੋਰਟ ਸਪਸ਼ਟ ਹੈ।", "havale anusar report spasht hai.", "According to the reference the report is clear."),
           X("ਇਹ ਗੱਲ ਸਪਸ਼ਟ ਕੀਤੀ ਗਈ ਕਿ ਮੀਟਿੰਗ ਅਗਲੇ ਹਫ਼ਤੇ ਹੋਵੇਗੀ।", "ih gal spasht kiti gai ki meeting agle hafte hovegi.", "It was made clear that the meeting would be next week.")],
          [("ਅਧਿਕਾਰੀ ਨੇ ਕਿਹਾ ਕਿ ਮੈਂ ਜਾਂਚ ਕਰੇਗਾ।", "ਅਧਿਕਾਰੀ ਨੇ ਕਿਹਾ ਕਿ ਉਹ ਜਾਂਚ ਕਰੇਗਾ।", "In a report the speaker's ਮੈਂ changes to ਉਹ."),
           ("ਅਧਿਕਾਰੀ ਨੇ ਕਿਹਾ ਕਿ ਉਹ ਜਾਂਚ ਕਰਦਾ ਹੈ।", "ਅਧਿਕਾਰੀ ਨੇ ਕਿਹਾ ਕਿ ਉਹ ਜਾਂਚ ਕਰੇਗਾ।", "The tense of the report moves back: ਹੈ becomes ਹੋਵੇਗਾ.")]),
        [D("ਰਿਪੋਰਟਰ", "ਅਧਿਕਾਰੀ ਨੇ ਕੀ ਕਿਹਾ?", "adhikari ne ki kiha?", "What did the officer say?"),
         D("ਕਲਰਕ", "ਉਨ੍ਹਾਂ ਨੇ ਕਿਹਾ ਕਿ ਉਹ ਕੱਲ੍ਹ ਜਾਂਚ ਕਰਨਗੇ।", "unhan ne kiha ki uh kallh janch karange.", "They said that they would investigate tomorrow."),
         D("ਰਿਪੋਰਟਰ", "ਕੀ ਇਹ ਲਿਖਤੀ ਹੈ?", "ki ih likhti hai?", "Is this in writing?"),
         D("ਕਲਰਕ", "ਹਵਾਲੇ ਅਨੁਸਾਰ ਪੱਤਰ ਵਿੱਚ ਸਪਸ਼ਟ ਲਿਖਿਆ ਹੋਇਆ ਹੈ।", "havale anusar pattar vich spasht likhia hoia hai.", "According to the reference it is clearly written in the letter.")],
        WS("Report worksheet", [
            T("Report the words.", ["the officer said that he would investigate", "it was made clear that the meeting would be next week"],
              ["ਅਧਿਕਾਰੀ ਨੇ ਕਿਹਾ ਕਿ ਉਹ ਜਾਂਚ ਕਰੇਗਾ", "ਇਹ ਸਪਸ਼ਟ ਕੀਤਾ ਗਿਆ ਕਿ ਮੀਟਿੰਗ ਅਗਲੇ ਹਫ਼ਤੇ ਹੋਵੇਗੀ"]),
            T("Name the source.", ["according to the reference", "the concerned office"],
              ["ਹਵਾਲੇ ਅਨੁਸਾਰ", "ਸਬੰਧਤ ਦਫ਼ਤਰ"]),
        ]))),
    ("pa-b2-u2", "pa-b2-l8", L("ਅੰਕੜੇ ਅਤੇ ਫ਼ੀਸਦੀ",
        "Figures in Punjabi take the postposition that matches their role: ਵਿੱਚੋਂ for a part of "
        "a total, ਤੱਕ for a limit, ਨਾਲੋਂ for a comparison. ਫ਼ੀਸਦੀ, ਲੱਖ and ਕਰੋੜ are nouns, so "
        "the verb agreeing with them stays singular.",
        [V("ਫ਼ੀਸਦੀ", "fisadi", "percent", "noun"),
         V("ਲੱਖ", "lakkh", "hundred thousand", "noun"),
         V("ਆਬਾਦੀ", "abadi", "population", "noun"),
         V("ਵਾਧਾ", "vadha", "increase", "noun"),
         V("ਕਮੀ", "kami", "shortage, decrease", "noun")],
        G("Numbers and comparison",
          "ਆਬਾਦੀ ਸੋਲਾਂ ਲੱਖ ਹੈ · ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਦੋ ਫ਼ੀਸਦੀ ਵੱਧ · ਵਿੱਚੋਂ ਚਾਰ ਫ਼ੀਸਦੀ",
          "ਵੱਧ and ਘੱਟ take ਨਾਲੋਂ for the thing compared (ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਵੱਧ), ਵਿੱਚੋਂ takes a "
          "part out of the whole (ਹਰ ਸੌ ਵਿੱਚੋਂ), and ਤੱਕ gives the limit (ਦਸ ਹਜ਼ਾਰ ਤੱਕ). "
          "Figures stay singular: ਵੀਹ ਲੱਖ ਹੈ.",
          [X("ਇਸ ਸਾਲ ਆਬਾਦੀ ਵਿੱਚ ਦੋ ਫ਼ੀਸਦੀ ਵਾਧਾ ਹੋਇਆ।", "is sal abadi vich do fisadi vadha hoia.", "This year there was a two percent increase in population."),
           X("ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਪੈਦਾਵਾਰ ਵੱਧ ਹੈ।", "pichhle sal nalon paidavar vaddh hai.", "Production is higher than last year."),
           X("ਹਰ ਸੌ ਵਿੱਚੋਂ ਚਾਰ ਪਰਿਵਾਰ ਲਾਭ ਲੈਂਦੇ ਹਨ।", "har sau vichon char parivar labh lainde han.", "Out of every hundred, four families benefit.")],
          [("ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਪੈਦਾਵਾਰ ਵੱਧ ਕਰਦੀ ਹੈ।", "ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਪੈਦਾਵਾਰ ਵੱਧ ਹੈ।", "A comparison needs ਵੱਧ ਹੈ, not ਵੱਧ ਕਰਦੀ ਹੈ."),
           ("ਹਰ ਸੌ ਵਿੱਚ ਚਾਰ ਪਰਿਵਾਰ।", "ਹਰ ਸੌ ਵਿੱਚੋਂ ਚਾਰ ਪਰਿਵਾਰ।", "A part of a total takes ਵਿੱਚੋਂ.")]),
        [D("ਅਧਿਕਾਰੀ", "ਇਸ ਵਾਰ ਦਾ ਵਾਧਾ ਕੀ ਹੈ?", "is var da vadha ki hai?", "What is the increase this time?"),
         D("ਕਲਰਕ", "ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਤਿੰਨ ਫ਼ੀਸਦੀ ਵੱਧ।", "pichhle sal nalon tinn fisadi vaddh.", "Three percent more than last year."),
         D("ਅਧਿਕਾਰੀ", "ਆਬਾਦੀ ਦਾ ਅੰਕੜਾ?", "abadi da ankra?", "The population figure?"),
         D("ਕਲਰਕ", "ਲਗਭਗ ਤੀਹ ਲੱਖ, ਅਤੇ ਹਰ ਸੌ ਵਿੱਚੋਂ ਸੱਠ ਪਿੰਡਾਂ ਵਿੱਚ ਪਾਣੀ ਪਹੁੰਚਿਆ।", "lagbhag tih lakkh, ate har sau vichon satth pindan vich pani pahunchia.", "About three million, and in sixty out of every hundred villages water has reached.")],
        WS("Figures worksheet", [
            T("State the comparison.", ["three percent more than last year", "production is higher than last year"],
              ["ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਤਿੰਨ ਫ਼ੀਸਦੀ ਵੱਧ", "ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਪੈਦਾਵਾਰ ਵੱਧ ਹੈ"]),
            T("Give the figure.", ["the population is about three million", "four out of every hundred families"],
              ["ਆਬਾਦੀ ਲਗਭਗ ਤੀਹ ਲੱਖ ਹੈ", "ਹਰ ਸੌ ਵਿੱਚੋਂ ਚਾਰ ਪਰਿਵਾਰ"]),
        ]))),
    ("pa-b2-u3", "pa-b2-l9", L("ਬੇਨਤੀ ਅਤੇ ਪੱਤਰ",
        "A formal letter has four moves: ਸੰਬੋਧਨ (the address), the reason with ਦੇ ਸਬੰਧ ਵਿੱਚ, the "
        "request with ਬੇਨਤੀ ਹੈ ਕਿ, and the closing with ਹਸਤਾਖ਼ਰ. The verb of a request goes into "
        "the subjunctive — ਕਿ ਕੰਮ ਜਲਦੀ ਹੋਵੇ — which keeps the tone respectful.",
        [V("ਬੇਨਤੀ", "benti", "request, petition", "noun"),
         V("ਪੱਤਰ", "pattar", "letter", "noun"),
         V("ਸੰਬੋਧਨ", "sambodhan", "address, salutation", "noun"),
         V("ਹਸਤਾਖ਼ਰ", "hastakhar", "signature", "noun"),
         V("ਸਬੰਧ", "sabandh", "relation, matter", "noun")],
        G("Writing a formal request",
          "ਸਬੰਧ ਵਿੱਚ ਬੇਨਤੀ ਹੈ ਕਿ … · ਕਿ ਕੰਮ ਜਲਦੀ ਹੋਵੇ · ਭਰੋਸਾ ਦਿਵਾਉਂਦੇ ਹਾਂ",
          "The opening names the matter: ਇਸ ਪੱਤਰ ਦੇ ਸਬੰਧ ਵਿੱਚ. The request follows ਬੇਨਤੀ ਹੈ ਕਿ "
          "with a subjunctive verb (ਹੋਵੇ, ਕਰਨ, ਦਿੱਤੀ ਜਾਵੇ), and the close gives assurance with "
          "ਭਰੋਸਾ ਦਿਵਾਉਂਦੇ ਹਾਂ before the signature.",
          [X("ਇਸ ਪੱਤਰ ਦੇ ਸਬੰਧ ਵਿੱਚ ਬੇਨਤੀ ਹੈ ਕਿ ਸੜਕ ਦਾ ਕੰਮ ਜਲਦੀ ਹੋਵੇ।", "is pattar de sabandh vich benti hai ki sarak da kam jaldi hove.", "With reference to this letter, the request is that the road work be done soon."),
           X("ਸੰਬੋਧਨ: ਪ੍ਰਧਾਨ ਜੀ, ਪਿੰਡ ਸੁਧਾਰ ਸਭਾ।", "sambodhan: pradhan ji, pind sudhar sabha.", "Salutation: President, Village Improvement Committee."),
           X("ਭਰੋਸਾ ਦਿਵਾਉਂਦੇ ਹਾਂ ਕਿ ਮਸਲਾ ਹੱਲ ਹੋਵੇਗਾ।", "bharosa divaunde han ki masla hal hovega.", "We assure you that the matter will be resolved.")],
          [("ਬੇਨਤੀ ਹੈ ਕਿ ਕੰਮ ਜਲਦੀ ਹੋਵੇਗਾ।", "ਬੇਨਤੀ ਹੈ ਕਿ ਕੰਮ ਜਲਦੀ ਹੋਵੇ।", "A request after ਕਿ takes the subjunctive ਹੋਵੇ."),
           ("ਇਸ ਪੱਤਰ ਵਿੱਚ ਸਬੰਧ ਬੇਨਤੀ ਹੈ ਕਿ।", "ਇਸ ਪੱਤਰ ਦੇ ਸਬੰਧ ਵਿੱਚ ਬੇਨਤੀ ਹੈ ਕਿ।", "The matter is named with ਦੇ ਸਬੰਧ ਵਿੱਚ.")]),
        [D("ਸਕੱਤਰ", "ਪੱਤਰ ਤਿਆਰ ਹੈ?", "pattar tayar hai?", "Is the letter ready?"),
         D("ਸਦੱਸ", "ਸੰਬੋਧਨ ਲਿਖਿਆ ਹੈ, ਪਰ ਬੇਨਤੀ ਬਾਕੀ ਹੈ।", "sambodhan likhia hai, par benti baki hai.", "The salutation is written, but the request is left."),
         D("ਸਕੱਤਰ", "ਲਿਖੋ: ਬੇਨਤੀ ਹੈ ਕਿ ਪਾਣੀ ਦਾ ਕੰਮ ਜਲਦੀ ਹੋਵੇ।", "likho: benti hai ki pani da kam jaldi hove.", "Write: the request is that the water work be done soon."),
         D("ਸਦੱਸ", "ਅਤੇ ਅਖ਼ੀਰ ਵਿੱਚ ਹਸਤਾਖ਼ਰ?", "ate akhir vich hastakhar?", "And the signature at the end?"),
         D("ਸਕੱਤਰ", "ਹਾਂ, ਭਰੋਸਾ ਦਿਵਾਉਂਦੇ ਹਾਂ ਲਿਖ ਕੇ ਹਸਤਾਖ਼ਰ ਕਰ ਦਿਓ।", "han, bharosa divaunde han likh ke hastakhar kar dio.", "Yes, write 'we assure you' and then sign.")],
        WS("Letter worksheet", [
            T("Open the letter.", ["salutation: President, Village Improvement Committee", "with reference to this letter"],
              ["ਸੰਬੋਧਨ: ਪ੍ਰਧਾਨ ਜੀ, ਪਿੰਡ ਸੁਧਾਰ ਸਭਾ", "ਇਸ ਪੱਤਰ ਦੇ ਸਬੰਧ ਵਿੱਚ"]),
            T("Make the request.", ["the request is that the water work be done soon", "we assure you that the matter will be resolved"],
              ["ਬੇਨਤੀ ਹੈ ਕਿ ਪਾਣੀ ਦਾ ਕੰਮ ਜਲਦੀ ਹੋਵੇ", "ਭਰੋਸਾ ਦਿਵਾਉਂਦੇ ਹਾਂ ਕਿ ਮਸਲਾ ਹੱਲ ਹੋਵੇਗਾ"]),
        ]))),
]

THIRD["C1"] = [
    ("pa-c1-u1", "pa-c1-l7", L("ਸਮੀਖਿਆ ਦੀ ਭਾਸ਼ਾ",
        "A review weighs a work instead of describing it. The scale is stated openly — ਵਧੀਆ ਪੱਖ "
        "… ਕਮਜ਼ੋਰੀ … — and the judgement is carried by ਪ੍ਰਭਾਵ ਪਾਉਣਾ and ਛਾਪ ਛੱਡਣਾ, so the "
        "reader can disagree with the reasoning rather than the verdict.",
        [V("ਸਮੀਖਿਆ", "samikhia", "review, criticism", "noun"),
         V("ਟਿੱਪਣੀ", "tippni", "comment", "noun"),
         V("ਪ੍ਰਭਾਵ", "prabhav", "impression, effect", "noun"),
         V("ਬਣਾਵਟ", "banavat", "structure, construction", "noun"),
         V("ਪੱਖ", "pakhh", "side, aspect", "noun")],
        G("Weighing a work",
          "ਵਧੀਆ ਪੱਖ ਇਹ ਹੈ ਕਿ · ਕਮਜ਼ੋਰੀ ਇਹ ਹੈ ਕਿ · ਪ੍ਰਭਾਵ ਛੱਡਦੀ ਹੈ",
          "The two sides of a review are introduced with ਵਧੀਆ ਪੱਖ ਇਹ ਹੈ ਕਿ and ਕਮਜ਼ੋਰੀ ਇਹ ਹੈ ਕਿ, "
          "each followed by ਕਿ and a full clause. ਬਣਾਵਟ and ਭਾਸ਼ਾ are judged with ਕਸਵੱਟੀ ਲੱਗਣੀ "
          "(to stand the test), and ਛਾਪ ਛੱਡਣਾ says the work leaves a mark on the reader.",
          [X("ਇਸ ਕਹਾਣੀ ਦਾ ਵਧੀਆ ਪੱਖ ਇਹ ਹੈ ਕਿ ਭਾਸ਼ਾ ਤਿੱਖੀ ਹੈ।", "is kahani da vadhia pakhh ih hai ki bhasha tikkhi hai.", "The strong side of this story is that the language is sharp."),
           X("ਕਮਜ਼ੋਰੀ ਇਹ ਹੈ ਕਿ ਬਣਾਵਟ ਢਿੱਲੀ ਹੋ ਜਾਂਦੀ ਹੈ।", "kamzori ih hai ki banavat dhilli ho jandi hai.", "The weakness is that the structure grows loose."),
           X("ਕਿਤਾਬ ਪਾਠਕ ਉੱਤੇ ਛਾਪ ਛੱਡਦੀ ਹੈ।", "kitab pathak utte chhap chhadddi hai.", "The book leaves a mark on the reader.")],
          [("ਵਧੀਆ ਪੱਖ ਇਹ ਹੈ ਕਿ ਭਾਸ਼ਾ ਤਿੱਖੀ ਹੈ ਕਿ।", "ਵਧੀਆ ਪੱਖ ਇਹ ਹੈ ਕਿ ਭਾਸ਼ਾ ਤਿੱਖੀ ਹੈ।", "One ਕਿ opens the clause; a second one closes nothing."),
           ("ਕਮਜ਼ੋਰੀ ਇਹ ਹੈ ਕਿ ਬਣਾਵਟ ਢਿੱਲੀ ਹੋ ਜਾਂਦੀ।", "ਕਮਜ਼ੋਰੀ ਇਹ ਹੈ ਕਿ ਬਣਾਵਟ ਢਿੱਲੀ ਹੋ ਜਾਂਦੀ ਹੈ।", "The clause needs its verb ਹੈ.")]),
        [D("ਸੰਪਾਦਕ", "ਤੁਹਾਡੀ ਸਮੀਖਿਆ ਕੀ ਕਹਿੰਦੀ ਹੈ?", "tuhadi samikhia ki kahindi hai?", "What does your review say?"),
         D("ਸਮੀਖਿਆਕਾਰ", "ਵਧੀਆ ਪੱਖ ਇਹ ਹੈ ਕਿ ਕਥਾ ਸਿੱਧੀ ਚੱਲਦੀ ਹੈ।", "vadhia pakhh ih hai ki katha siddhi challdi hai.", "The strong side is that the story moves straight."),
         D("ਸੰਪਾਦਕ", "ਅਤੇ ਕਮਜ਼ੋਰੀ?", "ate kamzori?", "And the weakness?"),
         D("ਸਮੀਖਿਆਕਾਰ", "ਅਖ਼ੀਰ ਵਿੱਚ ਬਣਾਵਟ ਢਿੱਲੀ ਹੋ ਜਾਂਦੀ ਹੈ, ਪਰ ਪ੍ਰਭਾਵ ਰਹਿ ਜਾਂਦਾ ਹੈ।", "akhir vich banavat dhilli ho jandi hai, par prabhav rahi janda hai.", "At the end the structure grows loose, but the impression stays.")],
        WS("Review worksheet", [
            T("Open the weighing.", ["the strong side is that the language is sharp", "the weakness is that the structure grows loose"],
              ["ਵਧੀਆ ਪੱਖ ਇਹ ਹੈ ਕਿ ਭਾਸ਼ਾ ਤਿੱਖੀ ਹੈ", "ਕਮਜ਼ੋਰੀ ਇਹ ਹੈ ਕਿ ਬਣਾਵਟ ਢਿੱਲੀ ਹੋ ਜਾਂਦੀ ਹੈ"]),
            T("Judge the effect.", ["the book leaves a mark on the reader", "the impression stays"],
              ["ਕਿਤਾਬ ਪਾਠਕ ਉੱਤੇ ਛਾਪ ਛੱਡਦੀ ਹੈ", "ਪ੍ਰਭਾਵ ਰਹਿ ਜਾਂਦਾ ਹੈ"]),
        ]))),
    ("pa-c1-u2", "pa-c1-l8", L("ਦ੍ਰਿਸ਼ਟੀਕੋਣ ਅਤੇ ਸਬੂਤ",
        "An argument stays honest when the claim and the evidence are named separately. ਦਾਅਵਾ "
        "introduces what is being asserted, ਸਬੂਤ what supports it, and the hedge ਇਹ ਕਿਹਾ ਜਾ "
        "ਸਕਦਾ ਹੈ ਕਿ keeps the writer's voice out of the middle of the sentence.",
        [V("ਦ੍ਰਿਸ਼ਟੀਕੋਣ", "darishtikon", "point of view", "noun"),
         V("ਦਾਅਵਾ", "daava", "claim", "noun"),
         V("ਸਬੂਤ", "sabut", "evidence, proof", "noun"),
         V("ਤਰਕ", "tarak", "argument, reasoning", "noun"),
         V("ਆਧਾਰ", "aadhar", "basis", "noun")],
        G("Claim and evidence",
          "ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ · ਸਬੂਤ ਵਜੋਂ · ਇਹ ਕਿਹਾ ਜਾ ਸਕਦਾ ਹੈ ਕਿ",
          "ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ names the claim, ਸਬੂਤ ਵਜੋਂ brings in the evidence, and ਆਧਾਰ ਉੱਤੇ "
          "gives the ground on which the claim rests. The impersonal ਇਹ ਕਿਹਾ ਜਾ ਸਕਦਾ ਹੈ ਕਿ "
          "lets the evidence speak first and the writer second.",
          [X("ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ ਖ਼ਰਚ ਵਧਿਆ ਹੈ।", "daava ih hai ki kharch vadhia hai.", "The claim is that the cost has risen."),
           X("ਸਬੂਤ ਵਜੋਂ ਤਿੰਨ ਅੰਕੜੇ ਪੇਸ਼ ਕੀਤੇ ਜਾ ਸਕਦੇ ਹਨ।", "sabut vajo tinn ankde pesh kite ja sakde han.", "As evidence three figures can be presented."),
           X("ਇਹ ਕਿਹਾ ਜਾ ਸਕਦਾ ਹੈ ਕਿ ਤਰਕ ਪੂਰਾ ਨਹੀਂ ਹੈ।", "ih kiha ja sakda hai ki tarak pura nahin hai.", "It can be said that the argument is not complete.")],
          [("ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ ਖ਼ਰਚ ਵਧਿਆ।", "ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ ਖ਼ਰਚ ਵਧਿਆ ਹੈ।", "The claim's clause keeps its verb."),
           ("ਸਬੂਤ ਵਜੋਂ ਇਹ ਕਿਹਾ ਜਾ ਸਕਦਾ ਹੈ।", "ਸਬੂਤ ਵਜੋਂ ਤਿੰਨ ਅੰਕੜੇ ਹਨ।", "ਸਬੂਤ ਵਜੋਂ brings evidence, not an announcement.")]),
        [D("ਪ੍ਰੋਫ਼ੈਸਰ", "ਤੁਹਾਡਾ ਦਾਅਵਾ ਕੀ ਹੈ?", "tuhada daava ki hai?", "What is your claim?"),
         D("ਵਿਦਿਆਰਥੀ", "ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ ਲਾਗਤ ਵੱਧ ਗਈ ਹੈ।", "daava ih hai ki lagat vaddh gai hai.", "The claim is that the cost has risen."),
         D("ਪ੍ਰੋਫ਼ੈਸਰ", "ਅਤੇ ਸਬੂਤ?", "ate sabut?", "And the evidence?"),
         D("ਵਿਦਿਆਰਥੀ", "ਇਹ ਕਿਹਾ ਜਾ ਸਕਦਾ ਹੈ ਕਿ ਦੋ ਰਿਪੋਰਟਾਂ ਇੱਕੋ ਤਰਕ ਦਿੰਦੀਆਂ ਹਨ।", "ih kiha ja sakda hai ki do reportan ikko tarak dindian han.", "It can be said that two reports give the same reasoning.")],
        WS("Argument worksheet", [
            T("Name the claim.", ["the claim is that the cost has risen", "as evidence, three figures"],
              ["ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ ਲਾਗਤ ਵੱਧ ਗਈ ਹੈ", "ਸਬੂਤ ਵਜੋਂ ਤਿੰਨ ਅੰਕੜੇ"]),
            T("Hold back the writer.", ["it can be said that the argument is not complete", "on this basis"],
              ["ਇਹ ਕਿਹਾ ਜਾ ਸਕਦਾ ਹੈ ਕਿ ਤਰਕ ਪੂਰਾ ਨਹੀਂ ਹੈ", "ਇਸ ਆਧਾਰ ਉੱਤੇ"]),
        ]))),
    ("pa-c1-u3", "pa-c1-l9", L("ਸੰਪਾਦਕੀ ਸੁਰ",
        "An editorial speaks for a paper, so it uses ਅਸੀਂ rather than ਮੈਂ and asks institutions to "
        "act: ਸਰਕਾਰ ਨੂੰ ਚਾਹੀਦਾ ਹੈ ਕਿ, ਪ੍ਰਸ਼ਾਸਨ ਤੋਂ ਮੰਗ ਹੈ ਕਿ. The demand stays firm and the "
        "tone stays impersonal — the argument, not the writer, is doing the talking.",
        [V("ਸੰਪਾਦਕੀ", "sampadki", "editorial", "noun"),
         V("ਮੰਗ", "mang", "demand", "noun"),
         V("ਜ਼ਿੰਮੇਵਾਰੀ", "zimmevari", "responsibility", "noun"),
         V("ਹੱਕ", "hakk", "right", "noun"),
         V("ਪ੍ਰਸ਼ਾਸਨ", "prashasan", "administration", "noun")],
        G("The editorial voice",
          "ਸਰਕਾਰ ਨੂੰ ਚਾਹੀਦਾ ਹੈ ਕਿ · ਪ੍ਰਸ਼ਾਸਨ ਤੋਂ ਮੰਗ ਹੈ ਕਿ · ਜ਼ਿੰਮੇਵਾਰੀ ਬਣਦੀ ਹੈ",
          "The editorial voice uses ਅਸੀਂ and addresses institutions, not persons: ਸਰਕਾਰ ਨੂੰ "
          "ਚਾਹੀਦਾ ਹੈ ਕਿ ਮਸਲਾ ਹੱਲ ਕਰੇ. ਮੰਗ ਹੈ ਕਿ takes the subjunctive, ਜ਼ਿੰਮੇਵਾਰੀ ਬਣਦੀ ਹੈ states "
          "the obligation, and ਹੱਕ ਬਣਦਾ ਹੈ claims the right without shouting.",
          [X("ਸਰਕਾਰ ਨੂੰ ਚਾਹੀਦਾ ਹੈ ਕਿ ਸੜਕ ਦਾ ਕੰਮ ਜਲਦੀ ਕਰੇ।", "sarkar nun chahida hai ki sarak da kam jaldi kare.", "The government ought to do the road work soon."),
           X("ਪ੍ਰਸ਼ਾਸਨ ਤੋਂ ਮੰਗ ਹੈ ਕਿ ਹਿਸਾਬ ਸਾਹਮਣੇ ਰੱਖਿਆ ਜਾਵੇ।", "prashasan ton mang hai ki hisab sahmane rakhia jave.", "Our demand from the administration is that the accounts be placed in the open."),
           X("ਨਾਗਰਿਕਾਂ ਦਾ ਹੱਕ ਬਣਦਾ ਹੈ ਕਿ ਜਵਾਬ ਮਿਲੇ।", "nagrikan da hakk bandda hai ki javab mile.", "Citizens have a right to get an answer.")],
          [("ਸਰਕਾਰ ਨੂੰ ਚਾਹੀਦਾ ਹੈ ਕਿ ਕੰਮ ਜਲਦੀ ਕਰੇਗੀ।", "ਸਰਕਾਰ ਨੂੰ ਚਾਹੀਦਾ ਹੈ ਕਿ ਕੰਮ ਜਲਦੀ ਕਰੇ।", "What ought to be done takes the subjunctive ਕਰੇ."),
           ("ਮੈਨੂੰ ਲੱਗਦਾ ਹੈ ਕਿ ਸਰਕਾਰ ਨੂੰ ਚਾਹੀਦਾ ਹੈ।", "ਸੰਪਾਦਕੀ ਵਿੱਚ ਅਸੀਂ ਲਿਖਦੇ ਹਾਂ।", "An editorial speaks as ਅਸੀਂ, not as ਮੈਂ.")]),
        [D("ਸੰਪਾਦਕ", "ਅੱਜ ਦੀ ਸੰਪਾਦਕੀ ਦਾ ਮੁੱਖ ਤਰਕ?", "ajj di sampadki da mukkh tarak?", "The main argument of today's editorial?"),
         D("ਲੇਖਕ", "ਸਰਕਾਰ ਨੂੰ ਚਾਹੀਦਾ ਹੈ ਕਿ ਹਿਸਾਬ ਸਾਹਮਣੇ ਰੱਖੇ।", "sarkar nun chahida hai ki hisab sahmane rakhe.", "The government ought to place the accounts in the open."),
         D("ਸੰਪਾਦਕ", "ਸੁਰ ਕਿਵੇਂ ਹੋਵੇ?", "sur kiven hove?", "How should the tone be?"),
         D("ਲੇਖਕ", "ਅਸੀਂ ਮੰਗ ਕਰਦੇ ਹਾਂ, ਪਰ ਜ਼ਿੰਮੇਵਾਰੀ ਦੀ ਗੱਲ ਕਰੀਏ।", "asin mang karde han, par zimmevari di gal karie.", "We make the demand, but we speak of responsibility.")],
        WS("Editorial worksheet", [
            T("Ask the institution.", ["the government ought to do the road work soon", "our demand is that the accounts be placed in the open"],
              ["ਸਰਕਾਰ ਨੂੰ ਚਾਹੀਦਾ ਹੈ ਕਿ ਸੜਕ ਦਾ ਕੰਮ ਜਲਦੀ ਕਰੇ", "ਪ੍ਰਸ਼ਾਸਨ ਤੋਂ ਮੰਗ ਹੈ ਕਿ ਹਿਸਾਬ ਸਾਹਮਣੇ ਰੱਖਿਆ ਜਾਵੇ"]),
            T("State the right.", ["citizens have a right to get an answer", "responsibility"],
              ["ਨਾਗਰਿਕਾਂ ਦਾ ਹੱਕ ਬਣਦਾ ਹੈ ਕਿ ਜਵਾਬ ਮਿਲੇ", "ਜ਼ਿੰਮੇਵਾਰੀ"]),
        ]))),
]

THIRD["C2"] = [
    ("pa-c2-u1", "pa-c2-l7", L("ਗੱਲਬਾਤ ਦਾ ਮੋੜ",
        "When two sides are stuck, the mediator reframes instead of repeating: ਪਹਿਲਾਂ ਖ਼ਰਚਾ … ਹੁਣ "
        "ਸਮਾਂ, ਜੇ ਇੱਕ ਪਾਸੇ … ਤਾਂ ਦੂਜੇ ਪਾਸੇ. ਸ਼ਰਤ (condition) and ਵਿਕਲਪ (option) move the talk "
        "from positions to interests.",
        [V("ਮੋੜ", "mor", "turn, twist", "noun"),
         V("ਸ਼ਰਤ", "sharat", "condition", "noun"),
         V("ਵਿਕਲਪ", "vikalp", "option, alternative", "noun"),
         V("ਸਮਝੌਤਾ", "samjhauta", "compromise, agreement", "noun"),
         V("ਪਾਸਾ", "pasa", "side (of a question)", "noun")],
        G("Reframing a stuck talk",
          "ਜੇ ਇੱਕ ਪਾਸੇ … ਤਾਂ ਦੂਜੇ ਪਾਸੇ · ਸ਼ਰਤ ਇਹ ਹੈ ਕਿ · ਵਿਕਲਪ ਵੀ ਹੈ",
          "The reframe sets two sides in one sentence with ਜੇ ਇੱਕ ਪਾਸੇ … ਤਾਂ ਦੂਜੇ ਪਾਸੇ, and every "
          "condition is stated openly with ਸ਼ਰਤ ਇਹ ਹੈ ਕਿ. ਵਿਕਲਪ ਵੀ ਹੈ announces that the door is "
          "still open, which is what keeps a mediation alive.",
          [X("ਜੇ ਇੱਕ ਪਾਸੇ ਖ਼ਰਚਾ ਵੱਧ ਹੈ, ਤਾਂ ਦੂਜੇ ਪਾਸੇ ਸਮਾਂ ਵੀ ਵੱਧ ਲੱਗੇਗਾ।", "je ikk pase kharcha vaddh hai, tan duje pase saman vi vaddh lagega.", "If on one side the cost is higher, on the other the time will also take longer."),
           X("ਸ਼ਰਤ ਇਹ ਹੈ ਕਿ ਅਗਲੀ ਮੀਟਿੰਗ ਸਮੇਂ ਸਿਰ ਹੋਵੇ।", "sharat ih hai ki agli meeting samen sir hove.", "The condition is that the next meeting be on time."),
           X("ਇੱਕ ਵਿਕਲਪ ਵੀ ਹੈ: ਕੰਮ ਦੋ ਹਿੱਸਿਆਂ ਵਿੱਚ ਹੋਵੇ।", "ikk vikalp vi hai: kam do hissian vich hove.", "There is also an option: the work be done in two parts.")],
          [("ਜੇ ਇੱਕ ਪਾਸੇ ਖ਼ਰਚਾ ਵੱਧ ਹੈ। ਤਾਂ ਦੂਜੇ ਪਾਸੇ ਸਮਾਂ।", "ਜੇ ਇੱਕ ਪਾਸੇ ਖ਼ਰਚਾ ਵੱਧ ਹੈ, ਤਾਂ ਦੂਜੇ ਪਾਸੇ ਸਮਾਂ ਵੀ ਵੱਧ ਲੱਗੇਗਾ।", "The two sides belong to one sentence with its verb."),
           ("ਸ਼ਰਤ ਇਹ ਹੈ ਕਿ ਮੀਟਿੰਗ ਸਮੇਂ ਸਿਰ ਹੋਵੇਗੀ।", "ਸ਼ਰਤ ਇਹ ਹੈ ਕਿ ਮੀਟਿੰਗ ਸਮੇਂ ਸਿਰ ਹੋਵੇ।", "A condition takes the subjunctive ਹੋਵੇ.")]),
        [D("ਵਿਚੋਲਾ", "ਦੋਵੇਂ ਪਾਸੇ ਆਪਣੀ ਗੱਲ ਕਹਿ ਲੈਣ।", "doven pase apni gal kahi lain.", "Let both sides say their piece."),
         D("ਪਹਿਲੀ ਧਿਰ", "ਸਾਡਾ ਖ਼ਰਚਾ ਵੱਧ ਹੈ।", "sada kharcha vaddh hai.", "Our cost is higher."),
         D("ਵਿਚੋਲਾ", "ਜੇ ਇੱਕ ਪਾਸੇ ਖ਼ਰਚਾ ਵੱਧ ਹੈ, ਤਾਂ ਸਮਾਂ ਵੀ ਵੱਧ ਲੱਗੇਗਾ।", "je ikk pase kharcha vaddh hai, tan samam vi vaddh lagega.", "If on one side the cost is higher, the time will also be longer."),
         D("ਦੂਜੀ ਧਿਰ", "ਸ਼ਰਤ ਇਹ ਹੈ ਕਿ ਕੰਮ ਦੋ ਹਿੱਸਿਆਂ ਵਿੱਚ ਹੋਵੇ।", "sharat ih hai ki kam do hissian vich hove.", "The condition is that the work be done in two parts.")],
        WS("Mediation worksheet", [
            T("Reframe both sides.", ["if on one side the cost is higher, the time will also be longer", "there is also an option"],
              ["ਜੇ ਇੱਕ ਪਾਸੇ ਖ਼ਰਚਾ ਵੱਧ ਹੈ, ਤਾਂ ਸਮਾਂ ਵੀ ਵੱਧ ਲੱਗੇਗਾ", "ਇੱਕ ਵਿਕਲਪ ਵੀ ਹੈ"]),
            T("State the condition.", ["the condition is that the next meeting be on time", "the work be done in two parts"],
              ["ਸ਼ਰਤ ਇਹ ਹੈ ਕਿ ਅਗਲੀ ਮੀਟਿੰਗ ਸਮੇਂ ਸਿਰ ਹੋਵੇ", "ਕੰਮ ਦੋ ਹਿੱਸਿਆਂ ਵਿੱਚ ਹੋਵੇ"]),
        ]))),
    ("pa-c2-u2", "pa-c2-l8", L("ਲਹਿਜਾ ਅਤੇ ਪੱਧਰ",
        "The same sentence changes meaning with its ਲਹਿਜਾ. Punjabi marks respect with ਤੁਸੀਂ, "
        "warmth with ਤੂੰ among equals, and formality with ਜੀ. Choosing the level is part of the "
        "message; mixing levels inside one turn sounds careless.",
        [V("ਲਹਿਜਾ", "lahija", "tone, register", "noun"),
         V("ਪੱਧਰ", "paddhar", "level, standard", "noun"),
         V("ਆਦਰ", "aadar", "respect", "noun"),
         V("ਰਸਮ", "rasam", "custom, formality", "noun"),
         V("ਦੋਸਤੀ", "dosti", "friendship", "noun")],
        G("Choosing the level",
          "ਤੁਸੀਂ ਬੈਠੋ ਜੀ · ਤੂੰ ਆ ਜਾ · ਆਦਰ ਵਾਲਾ ਲਹਿਜਾ",
          "ਤੁਸੀਂ carries respect and takes plural verbs (ਤੁਸੀਂ ਬੈਠੋ), ਤੂੰ carries closeness and "
          "takes singular verbs (ਤੂੰ ਆ ਜਾ), and ਜੀ softens a plain request (ਦੱਸੋ ਜੀ). The formal "
          "level also prefers ਰਸਮ ਵਾਲੇ ਸ਼ਬਦ such as ਸੰਬੋਧਨ over ਸੱਦਾ.",
          [X("ਤੁਸੀਂ ਬੈਠੋ ਜੀ, ਮੈਂ ਹੁਣੇ ਆਇਆ।", "tusin baitho ji, main hune aia.", "Please sit, I have just come."),
           X("ਤੂੰ ਆ ਜਾ, ਦੇਰ ਹੋ ਗਈ।", "tun a ja, der ho gai.", "Come on, it has got late."),
           X("ਆਦਰ ਵਾਲਾ ਲਹਿਜਾ ਸੁਣ ਕੇ ਗੱਲ ਸੌਖੀ ਹੋ ਜਾਂਦੀ ਹੈ।", "aadar vala lahija sun ke gal saukhi ho jandi hai.", "Hearing a respectful tone makes the matter easier.")],
          [("ਤੁਸੀਂ ਬੈਠ।", "ਤੁਸੀਂ ਬੈਠੋ।", "ਤੁਸੀਂ takes the plural verb ਬੈਠੋ."),
           ("ਤੂੰ ਬੈਠੋ ਜੀ।", "ਤੂੰ ਬੈਠ।", "ਤੂੰ and ਜੀ belong to different levels; keep them apart.")]),
        [D("ਮੇਜ਼ਬਾਨ", "ਤੁਸੀਂ ਬੈਠੋ ਜੀ, ਚਾਹ ਲਓ।", "tusin baitho ji, chah lo.", "Please sit, have some tea."),
         D("ਮਹਿਮਾਨ", "ਸ਼ੁਕਰੀਆ ਜੀ।", "shukria ji.", "Thank you."),
         D("ਮੇਜ਼ਬਾਨ", "ਪੁਰਾਣੇ ਸਮੇਂ ਵਿੱਚ ਅਸੀਂ ਰਸਮ ਵੱਧ ਨਿਭਾਉਂਦੇ ਸਾਂ।", "purane samen vich asin rasam vaddh nibhaunde san.", "In older times we observed formality more."),
         D("ਮਹਿਮਾਨ", "ਹੁਣ ਲਹਿਜਾ ਉਹੀ ਹੈ, ਪੱਧਰ ਬਦਲ ਗਿਆ।", "hun lahija uhi hai, paddhar badal gia.", "The tone is the same now, the level has changed.")],
        WS("Register worksheet", [
            T("Choose the level.", ["please sit, I have just come", "come on, it has got late"],
              ["ਤੁਸੀਂ ਬੈਠੋ ਜੀ, ਮੈਂ ਹੁਣੇ ਆਇਆ", "ਤੂੰ ਆ ਜਾ, ਦੇਰ ਹੋ ਗਈ"]),
            T("Talk about tone.", ["a respectful tone makes the matter easier", "the level has changed"],
              ["ਆਦਰ ਵਾਲਾ ਲਹਿਜਾ ਗੱਲ ਸੌਖੀ ਕਰ ਦਿੰਦਾ ਹੈ", "ਪੱਧਰ ਬਦਲ ਗਿਆ"]),
        ]))),
    ("pa-c2-u3", "pa-c2-l9", L("ਬਾਰੀਕ ਫ਼ਰਕ",
        "Near synonyms sit side by side in Punjabi and the difference is in the shade: ਲੱਗਦਾ ਹੈ "
        "says how something seems, ਦਿਸਦਾ ਹੈ what is seen, ਸੁਣੀਦਾ ਹੈ what is heard. Naming the "
        "shade is the last skill of the register ladder.",
        [V("ਫ਼ਰਕ", "farak", "difference", "noun"),
         V("ਛਾਂ", "chhan", "shade", "noun"),
         V("ਭਾਵ", "bhav", "sense, meaning", "noun"),
         V("ਦਿਸਦਾ ਹੈ", "disda hai", "is visible", "phrase"),
         V("ਸੁਣੀਦਾ ਹੈ", "sunida hai", "is heard", "phrase")],
        G("The shade between near words",
          "ਲੱਗਦਾ ਹੈ · ਦਿਸਦਾ ਹੈ · ਸੁਣੀਦਾ ਹੈ · ਸ਼ਾਇਦ",
          "ਲੱਗਦਾ ਹੈ reports a guess (ਸ਼ਾਇਦ ਸਹੀ ਹੈ), ਦਿਸਦਾ ਹੈ reports what the eye gives, ਸੁਣੀਦਾ "
          "ਹੈ reports what reaches the ear. Punjabi also uses ਸ਼ਾਇਦ and ਹੋ ਸਕਦਾ ਹੈ to hold a "
          "meaning open, so the ear hears doubt and not a claim.",
          [X("ਇਹ ਸ਼ਾਇਦ ਸਹੀ ਲੱਗਦਾ ਹੈ, ਪਰ ਸਬੂਤ ਨਹੀਂ ਹੈ।", "ih shaid sahi lagda hai, par sabut nahin hai.", "This seems perhaps right, but there is no evidence."),
           X("ਦੂਰੋਂ ਪਹਾੜ ਦਿਸਦਾ ਹੈ।", "durron pahar disda hai.", "The mountain is visible from far away."),
           X("ਗਲੀ ਵਿੱਚੋਂ ਆਵਾਜ਼ ਸੁਣੀਦੀ ਹੈ।", "gali vichon avaz sunidi hai.", "A voice is heard from the lane.")],
          [("ਇਹ ਸਹੀ ਦਿਸਦਾ ਹੈ, ਪਰ ਸਬੂਤ ਨਹੀਂ।", "ਇਹ ਸਹੀ ਲੱਗਦਾ ਹੈ, ਪਰ ਸਬੂਤ ਨਹੀਂ।", "For a guess Punjabi says ਲੱਗਦਾ ਹੈ, not ਦਿਸਦਾ ਹੈ."),
           ("ਆਵਾਜ਼ ਸੁਣਦਾ ਹੈ।", "ਆਵਾਜ਼ ਸੁਣੀਦੀ ਹੈ।", "ਆਵਾਜ਼ is feminine and hears itself: ਸੁਣੀਦੀ ਹੈ.")]),
        [D("ਵਿਦਿਆਰਥੀ", "ਇਹ ਵਾਕ ਸਹੀ ਹੈ?", "ih vaak sahi hai?", "Is this sentence correct?"),
         D("ਅਧਿਆਪਕ", "ਸ਼ਾਇਦ ਸਹੀ ਲੱਗਦਾ ਹੈ, ਪਰ ਨਿਯਮ ਦੇਖੋ।", "shaid sahi lagda hai, par niyam dekho.", "It seems maybe right, but look at the rule."),
         D("ਵਿਦਿਆਰਥੀ", "ਦੋਵੇਂ ਸ਼ਬਦ ਇੱਕੋ ਜਿਹੇ ਸੁਣੀਦੇ ਹਨ।", "doven shabad ikko jihe sunide han.", "The two words sound the same."),
         D("ਅਧਿਆਪਕ", "ਸੁਣੀਦੇ ਹਾਂ, ਪਰ ਫ਼ਰਕ ਛਾਂ ਵਾਂਗ ਹੁੰਦਾ ਹੈ।", "sunide han, par farak chhan vang hunda hai.", "They are heard alike, but the difference is like a shade.")],
        WS("Nuance worksheet", [
            T("Report the impression.", ["the mountain is visible from far away", "a voice is heard from the lane"],
              ["ਦੂਰੋਂ ਪਹਾੜ ਦਿਸਦਾ ਹੈ", "ਗਲੀ ਵਿੱਚੋਂ ਆਵਾਜ਼ ਸੁਣੀਦੀ ਹੈ"]),
            T("Hold the meaning open.", ["this seems maybe right, but there is no evidence", "the difference is like a shade"],
              ["ਇਹ ਸ਼ਾਇਦ ਸਹੀ ਲੱਗਦਾ ਹੈ, ਪਰ ਸਬੂਤ ਨਹੀਂ ਹੈ", "ਫ਼ਰਕ ਛਾਂ ਵਾਂਗ ਹੁੰਦਾ ਹੈ"]),
        ]))),
]

HALFSTEPS["A1+"] = {
    "native": NATIVE,
    "title": "%s A1+ — Greetings, a phone call and a visit" % NAME,
    "goals": [
        "Greet a neighbour, ask after the family, and answer about yourself",
        "Run a short phone call: who is speaking, what for, and when to call back",
        "Receive a guest, offer chai, and take leave without hurry",
    ],
    "units": [
        {"id": "A1+-U1", "title": "ਸਵੇਰ ਦੀ ਗੱਲਬਾਤ", "lessons": [
            L("ਨਮਸਤੇ ਅਤੇ ਹਾਲ-ਚਾਲ",
              "A Punjabi greeting is not a formula you finish quickly. ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ is the "
              "respectful Sikh greeting and ਜੀ ਆਇਆਂ ਨੂੰ welcomes a guest, while ਕੀ ਹਾਲ ਹੈ? opens "
              "the family news. The answer usually starts with ਠੀਕ ਹਾਂ and then adds one line.",
              [V("ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ", "sati sri akal", "respectful greeting", "phrase"),
               V("ਕੀ ਹਾਲ ਹੈ?", "ki hal hai?", "how are you?", "phrase"),
               V("ਠੀਕ", "thik", "all right, fine", "adjective"),
               V("ਮਿਹਰਬਾਨੀ", "miharbani", "kindness, thanks", "noun"),
               V("ਘਰ ਵਾਲੇ", "ghar vale", "family, people at home", "phrase")],
              G("Greeting and answering",
                "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ · ਕੀ ਹਾਲ ਹੈ? · ਘਰ ਵਾਲੇ ਠੀਕ ਹਨ",
                "The greeting comes first and the question follows. ਕੀ ਹਾਲ ਹੈ? asks about the "
                "person; ਘਰ ਵਾਲੇ ਕਿਵੇਂ ਹਨ? asks about the family. The polite answer is ਠੀਕ ਹਾਂ, "
                "ਧੰਨਵਾਦ, and the question is returned with ਤੁਸੀਂ ਦੱਸੋ.",
                [X("ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ, ਸਰਦਾਰ ਜੀ।", "sati sri akal, sardar ji.", "Respectful greetings, sir."),
                 X("ਕੀ ਹਾਲ ਹੈ? ਕੀ ਘਰ ਵਾਲੇ ਠੀਕ ਹਨ?", "ki hal hai? ki ghar vale thik han?", "How are you? Is the family all right?"),
                 X("ਮੈਂ ਠੀਕ ਹਾਂ, ਧੰਨਵਾਦ। ਤੁਸੀਂ ਦੱਸੋ।", "main thik han, dhannavad. tusin dasso.", "I am fine, thank you. You tell me.")],
                [("ਮੈਂ ਠੀਕ ਹੋ।", "ਮੈਂ ਠੀਕ ਹਾਂ।", "ਹਾਂ is the first person singular of ਹੋਣਾ."),
                 ("ਕੀ ਘਰ ਵਾਲੇ ਠੀਕ ਹੈ?", "ਕੀ ਘਰ ਵਾਲੇ ਠੀਕ ਹਨ?", "ਘਰ ਵਾਲੇ is plural: ਹਨ.")]),
              [D("ਸਰਦਾਰ ਜੀ", "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ, ਬੀਬੀ ਜੀ।", "sati sri akal, bibi ji.", "Respectful greetings, madam."),
               D("ਬੀਬੀ ਜੀ", "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ। ਕੀ ਹਾਲ ਹੈ?", "sati sri akal. ki hal hai?", "Greetings. How are you?"),
               D("ਸਰਦਾਰ ਜੀ", "ਮੈਂ ਠੀਕ ਹਾਂ। ਘਰ ਵਾਲੇ ਵੀ ਠੀਕ ਹਨ।", "main thik han. ghar vale vi thik han.", "I am fine. The family is well too."),
               D("ਬੀਬੀ ਜੀ", "ਬਹੁਤ ਚੰਗਾ। ਫਿਰ ਮਿਲਾਂਗੇ।", "bahut changa. phir milange.", "Very good. We will meet again.")],
              WS("Greetings worksheet", [
                  T("Greet and ask.", ["respectful greetings, sir", "how are you? is the family all right?"],
                    ["ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ, ਸਰਦਾਰ ਜੀ", "ਕੀ ਹਾਲ ਹੈ? ਕੀ ਘਰ ਵਾਲੇ ਠੀਕ ਹਨ?"]),
                  T("Answer.", ["I am fine, thank you", "the family is well too"],
                    ["ਮੈਂ ਠੀਕ ਹਾਂ, ਧੰਨਵਾਦ", "ਘਰ ਵਾਲੇ ਵੀ ਠੀਕ ਹਨ"]),
              ])),
            L("ਸਵੇਰ ਦਾ ਕੰਮ",
              "The morning is described in order: ਉੱਠਣਾ, ਮੂੰਹ ਧੋਣਾ, ਚਾਹ ਪੀਣਾ, ਅਖ਼ਬਾਰ ਪੜ੍ਹਨਾ. "
              "Each verb is a noun-like infinitive when you list it, and turns into -ਦਾ/-ਦੀ ਹਾਂ "
              "when you say what you do. ਵਜੇ tells the clock time.",
              [V("ਉੱਠਣਾ", "uthna", "to get up", "verb"),
               V("ਮੂੰਹ ਧੋਣਾ", "munh dhona", "to wash the face", "verb"),
               V("ਚਾਹ ਪੀਣਾ", "chah pina", "to drink tea", "verb"),
               V("ਅਖ਼ਬਾਰ", "akhbar", "newspaper", "noun"),
               V("ਛੇ ਵਜੇ", "chhe vaje", "at six o'clock", "phrase")],
              G("Saying the morning",
                "ਮੈਂ ਛੇ ਵਜੇ ਉੱਠਦਾ ਹਾਂ · ਮੂੰਹ ਧੋਂਦਾ ਹਾਂ · ਚਾਹ ਪੀਂਦਾ ਹਾਂ",
                "The time comes before the verb with ਵਜੇ: ਛੇ ਵਜੇ ਉੱਠਦਾ ਹਾਂ. The habitual present "
                "ends in -ਦਾ ਹਾਂ for a man and -ਦੀ ਹਾਂ for a woman. ਪਹਿਲਾਂ (first) and ਫਿਰ (then) "
                "keep the order clear.",
                [X("ਮੈਂ ਰੋਜ਼ ਛੇ ਵਜੇ ਉੱਠਦਾ ਹਾਂ।", "main roj chhe vaje uthda han.", "I get up at six every day."),
                 X("ਪਹਿਲਾਂ ਮੂੰਹ ਧੋਂਦਾ ਹਾਂ, ਫਿਰ ਚਾਹ ਪੀਂਦਾ ਹਾਂ।", "pahilan munh dhonda han, phir chah pinda han.", "First I wash my face, then I drink tea."),
                 X("ਅਖ਼ਬਾਰ ਪੜ੍ਹਨ ਤੋਂ ਬਾਅਦ ਕੰਮ ਸ਼ੁਰੂ ਹੁੰਦਾ ਹੈ।", "akhbar parhan to baad kam shuru hunda hai.", "The work starts after reading the newspaper.")],
                [("ਮੈਂ ਛੇ ਵਜੇ ਉੱਠਦਾ ਹੋ।", "ਮੈਂ ਛੇ ਵਜੇ ਉੱਠਦਾ ਹਾਂ।", "The first person takes ਹਾਂ, not ਹੋ."),
                 ("ਮੈਂ ਚਾਹ ਪੀਂਦੀ ਹਾਂ। (man speaking)", "ਮੈਂ ਚਾਹ ਪੀਂਦਾ ਹਾਂ।", "A male speaker uses ਪੀਂਦਾ ਹਾਂ.")]),
              [D("ਮਨਵੀਰ", "ਤੁਸੀਂ ਕਿੰਨੇ ਵਜੇ ਉੱਠਦੇ ਹੋ?", "tusin kinne vaje uthde ho?", "What time do you get up?"),
               D("ਸਿਮਰਨ", "ਛੇ ਵਜੇ। ਪਹਿਲਾਂ ਮੂੰਹ ਧੋਂਦੀ ਹਾਂ।", "chhe vaje. pahilan munh dhondi han.", "At six. First I wash my face."),
               D("ਮਨਵੀਰ", "ਫਿਰ?", "phir?", "Then?"),
               D("ਸਿਮਰਨ", "ਚਾਹ ਪੀਂਦੀ ਹਾਂ ਅਤੇ ਅਖ਼ਬਾਰ ਪੜ੍ਹਦੀ ਹਾਂ।", "chah pindi han ate akhbar parhdi han.", "I drink tea and read the newspaper.")],
              WS("Morning worksheet", [
                  T("Give the time.", ["I get up at six every day", "at eight o'clock"],
                    ["ਮੈਂ ਰੋਜ਼ ਛੇ ਵਜੇ ਉੱਠਦਾ ਹਾਂ", "ਅੱਠ ਵਜੇ"]),
                  T("Put it in order.", ["first I wash my face, then I drink tea", "the work starts after reading the newspaper"],
                    ["ਪਹਿਲਾਂ ਮੂੰਹ ਧੋਂਦਾ ਹਾਂ, ਫਿਰ ਚਾਹ ਪੀਂਦਾ ਹਾਂ", "ਅਖ਼ਬਾਰ ਪੜ੍ਹਨ ਤੋਂ ਬਾਅਦ ਕੰਮ ਸ਼ੁਰੂ ਹੁੰਦਾ ਹੈ"]),
              ])),
            L("ਫ਼ੋਨ ਉੱਤੇ ਗੱਲ",
              "A phone call has its own opening: ਹੈਲੋ, ਕੌਣ ਬੋਲ ਰਹੇ ਹੋ? ਇੱਕ ਮਿੰਟ (one minute), ਫ਼ੋਨ "
              "ਕਰਾਂਗਾ (I will call). The future with -ਾਂਗਾ promises a call back, and ਬਿਜ਼ੀ (busy) "
              "or ਬਾਅਦ ਵਿੱਚ (later) buys the time politely.",
              [V("ਹੈਲੋ", "hello", "hello", "phrase"),
               V("ਕੌਣ", "kaun", "who", "pronoun"),
               V("ਇੱਕ ਮਿੰਟ", "ikk mint", "one minute", "phrase"),
               V("ਬਿਜ਼ੀ", "bizi", "busy", "adjective"),
               V("ਫ਼ੋਨ ਕਰਨਾ", "fon karna", "to phone", "verb")],
              G("A short phone call",
                "ਹੈਲੋ, ਕੌਣ ਬੋਲ ਰਹੇ ਹੋ? · ਮੈਂ ਬਾਅਦ ਵਿੱਚ ਫ਼ੋਨ ਕਰਾਂਗਾ · ਇੱਕ ਮਿੰਟ",
                "The call opens with ਹੈਲੋ and the question ਕੌਣ ਬੋਲ ਰਹੇ ਹੋ? — plural, to be "
                "respectful. A promise to call back takes the future: ਫ਼ੋਨ ਕਰਾਂਗਾ (I, male) or "
                "ਕਰਾਂਗੀ (I, female). ਬਿਜ਼ੀ ਹਾਂ says you cannot talk now.",
                [X("ਹੈਲੋ, ਕੌਣ ਬੋਲ ਰਹੇ ਹੋ?", "hello, kaun bol rahe ho?", "Hello, who is speaking?"),
                 X("ਮੈਂ ਹੁਣ ਬਿਜ਼ੀ ਹਾਂ, ਬਾਅਦ ਵਿੱਚ ਫ਼ੋਨ ਕਰਾਂਗਾ।", "main hun bizi han, baad vich fon karanga.", "I am busy now, I will phone later."),
                 X("ਇੱਕ ਮਿੰਟ ਰੁਕੋ, ਮੈਂ ਆਇਆ।", "ikk mint ruko, main aia.", "Wait a minute, I am coming.")],
                [("ਮੈਂ ਬਾਅਦ ਵਿੱਚ ਫ਼ੋਨ ਕਰਦਾ ਹਾਂ।", "ਮੈਂ ਬਾਅਦ ਵਿੱਚ ਫ਼ੋਨ ਕਰਾਂਗਾ।", "A promise about the future takes -ਾਂਗਾ."),
                 ("ਕੌਣ ਬੋਲ ਰਿਹਾ ਹੋ?", "ਕੌਣ ਬੋਲ ਰਹੇ ਹੋ?", "The polite question is plural: ਰਹੇ ਹੋ.")]),
              [D("ਸਿਮਰਨ", "ਹੈਲੋ, ਕੌਣ ਬੋਲ ਰਹੇ ਹੋ?", "hello, kaun bol rahe ho?", "Hello, who is speaking?"),
               D("ਮਨਵੀਰ", "ਮੈਂ ਮਨਵੀਰ। ਤੁਸੀਂ ਹੁਣ ਗੱਲ ਕਰ ਸਕਦੇ ਹੋ?", "main manvir. tusin hun gal kar sakde ho?", "I am Manveer. Can you talk now?"),
               D("ਸਿਮਰਨ", "ਮੈਂ ਹੁਣ ਬਿਜ਼ੀ ਹਾਂ।", "main hun bizi han.", "I am busy now."),
               D("ਮਨਵੀਰ", "ਠੀਕ ਹੈ, ਮੈਂ ਸ਼ਾਮ ਨੂੰ ਫ਼ੋਨ ਕਰਾਂਗਾ।", "thik hai, main sham nun fon karanga.", "All right, I will phone in the evening.")],
              WS("Phone worksheet", [
                  T("Open the call.", ["hello, who is speaking?", "can you talk now?"],
                    ["ਹੈਲੋ, ਕੌਣ ਬੋਲ ਰਹੇ ਹੋ?", "ਕੀ ਤੁਸੀਂ ਹੁਣ ਗੱਲ ਕਰ ਸਕਦੇ ਹੋ?"]),
                  T("Close the call.", ["I am busy now, I will phone later", "all right, I will phone in the evening"],
                    ["ਮੈਂ ਹੁਣ ਬਿਜ਼ੀ ਹਾਂ, ਬਾਅਦ ਵਿੱਚ ਫ਼ੋਨ ਕਰਾਂਗਾ", "ਠੀਕ ਹੈ, ਮੈਂ ਸ਼ਾਮ ਨੂੰ ਫ਼ੋਨ ਕਰਾਂਗਾ"]),
              ])),
        ]},
        {"id": "A1+-U2", "title": "ਘਰ ਅਤੇ ਬਾਜ਼ਾਰ", "lessons": [
            L("ਰਸੋਈ ਵਿੱਚ",
              "The kitchen gives you concrete nouns: ਤਵਾ, ਕੜਾਹੀ, ਥਾਲੀ, ਗਲਾਸ. Counting is done with "
              "the thing itself — ਇੱਕ ਥਾਲੀ, ਦੋ ਗਲਾਸ — and ਥੋੜ੍ਹਾ (a little) softens any quantity.",
              [V("ਤਵਾ", "tava", "griddle", "noun"),
               V("ਥਾਲੀ", "thali", "plate", "noun"),
               V("ਗਲਾਸ", "gilas", "glass", "noun"),
               V("ਥੋੜ੍ਹਾ", "thorha", "a little", "adjective"),
               V("ਪਾਣੀ", "pani", "water", "noun")],
              G("In the kitchen",
                "ਇੱਕ ਥਾਲੀ · ਦੋ ਗਲਾਸ ਪਾਣੀ · ਥੋੜ੍ਹਾ ਲੂਣ",
                "A number stands before the noun without a plural ending: ਦੋ ਗਲਾਸ (two glasses), "
                "ਤਿੰਨ ਥਾਲੀਆਂ (three plates, feminine). ਥੋੜ੍ਹਾ means a little and ਥੋੜ੍ਹੀ a few for "
                "feminine nouns: ਥੋੜ੍ਹੀ ਚੀਨੀ.",
                [X("ਇੱਕ ਥਾਲੀ ਵਿੱਚ ਦੋ ਰੋਟੀਆਂ ਹਨ।", "ikk thali vich do rotian han.", "There are two rotis on one plate."),
                 X("ਗਲਾਸ ਵਿੱਚ ਥੋੜ੍ਹਾ ਪਾਣੀ ਹੈ।", "gilas vich thorha pani hai.", "There is a little water in the glass."),
                 X("ਤਵੇ ਉੱਤੇ ਤਿੰਨ ਰੋਟੀਆਂ ਪਕਾਈਆਂ।", "tave utte tinn rotian pakaiyan.", "I cooked three rotis on the griddle.")],
                [("ਦੋ ਗਲਾਸਾਂ ਪਾਣੀ ਦਿਓ।", "ਦੋ ਗਲਾਸ ਪਾਣੀ ਦਿਓ।", "After a number the noun stays plain: ਦੋ ਗਲਾਸ."),
                 ("ਥੋੜ੍ਹਾ ਚੀਨੀ ਦਿਓ।", "ਥੋੜ੍ਹੀ ਚੀਨੀ ਦਿਓ।", "ਚੀਨੀ is feminine: ਥੋੜ੍ਹੀ.")]),
              [D("ਮਾਂ", "ਥਾਲੀ ਵਿੱਚ ਕੀ ਰੱਖਾਂ?", "thali vich ki rakkhan?", "What shall I put on the plate?"),
               D("ਪੁੱਤ", "ਦੋ ਰੋਟੀਆਂ ਅਤੇ ਥੋੜ੍ਹੀ ਦਾਲ।", "do rotian ate thorhi dal.", "Two rotis and a little dal."),
               D("ਮਾਂ", "ਅਤੇ ਪਾਣੀ?", "ate pani?", "And water?"),
               D("ਪੁੱਤ", "ਇੱਕ ਗਲਾਸ ਪਾਣੀ ਕਾਫ਼ੀ ਹੈ।", "ikk gilas pani kafi hai.", "One glass of water is enough.")],
              WS("Kitchen worksheet", [
                  T("Say the quantity.", ["two glasses of water", "a little sugar"],
                    ["ਦੋ ਗਲਾਸ ਪਾਣੀ", "ਥੋੜ੍ਹੀ ਚੀਨੀ"]),
                  T("Say what is there.", ["there are two rotis on one plate", "there is a little water in the glass"],
                    ["ਇੱਕ ਥਾਲੀ ਵਿੱਚ ਦੋ ਰੋਟੀਆਂ ਹਨ", "ਗਲਾਸ ਵਿੱਚ ਥੋੜ੍ਹਾ ਪਾਣੀ ਹੈ"]),
              ])),
            L("ਦੁਕਾਨ ਉੱਤੇ",
              "At a shop you ask for a thing and then for its price: ਭਾਅ ਕੀ ਹੈ? ਇੱਕ ਕਿੱਲੋ ਦਿਓ. "
              "Weights are ਕਿੱਲੋ and ਗ੍ਰਾਮ, and the total is ਕੁੱਲ. ਕਿੰਨੇ ਦਾ? asks about the "
              "whole purchase rather than one item.",
              [V("ਦੁਕਾਨਦਾਰ", "dukandar", "shopkeeper", "noun"),
               V("ਭਾਅ", "bhaa", "price, rate", "noun"),
               V("ਕਿੱਲੋ", "killo", "kilogram", "noun"),
               V("ਕੁੱਲ", "kull", "total", "adjective"),
               V("ਕਿੰਨੇ ਦਾ?", "kinne da?", "for how much?", "phrase")],
              G("Asking the price",
                "ਭਾਅ ਕੀ ਹੈ? · ਇੱਕ ਕਿੱਲੋ ਦਿਓ · ਕੁੱਲ ਕਿੰਨੇ ਦਾ?",
                "ਭਾਅ ਕੀ ਹੈ? asks the rate of one thing, ਕਿੰਨੇ ਦਾ? the price of the lot, and ਕੁੱਲ "
                "adds the total. ਦਿਓ asks for something politely; ਲਓ hands it over. Quantities "
                "take the noun plain after numbers.",
                [X("ਭਾਅ ਕੀ ਹੈ ਭਾਜੀ ਦਾ?", "bhaa ki hai bhaji da?", "What is the rate of the greens?"),
                 X("ਇੱਕ ਕਿੱਲੋ ਟਮਾਟਰ ਦਿਓ।", "ikk killo tamatar dio.", "Give me one kilogram of tomatoes."),
                 X("ਕੁੱਲ ਕਿੰਨੇ ਦਾ ਹੋਇਆ?", "kull kinne da hoia?", "How much is the total?")],
                [("ਭਾਅ ਕਿੰਨੇ ਹੈ?", "ਭਾਅ ਕੀ ਹੈ?", "For a rate Punjabi asks ਭਾਅ ਕੀ ਹੈ."),
                 ("ਇੱਕ ਕਿੱਲੋ ਟਮਾਟਰਾਂ ਦਿਓ।", "ਇੱਕ ਕਿੱਲੋ ਟਮਾਟਰ ਦਿਓ।", "After a weight the noun stays plain.")]),
              [D("ਗਾਹਕ", "ਭਾਜੀ ਦਾ ਭਾਅ ਕੀ ਹੈ?", "bhaji da bhaa ki hai?", "What is the rate of the greens?"),
               D("ਦੁਕਾਨਦਾਰ", "ਚਾਲੀ ਰੁਪਏ ਕਿੱਲੋ।", "chali rupae killo.", "Forty rupees a kilogram."),
               D("ਗਾਹਕ", "ਇੱਕ ਕਿੱਲੋ ਦਿਓ, ਅਤੇ ਦੋ ਕਿੱਲੋ ਆਲੂ।", "ikk killo dio, ate do killo alu.", "Give me one kilogram, and two kilograms of potatoes."),
               D("ਦੁਕਾਨਦਾਰ", "ਕੁੱਲ ਇੱਕ ਸੌ ਚਾਲੀ ਰੁਪਏ।", "kull ikk sau chali rupae.", "The total is one hundred and forty rupees.")],
              WS("Shop worksheet", [
                  T("Ask the rate.", ["what is the rate of the greens?", "one kilogram of tomatoes"],
                    ["ਭਾਜੀ ਦਾ ਭਾਅ ਕੀ ਹੈ?", "ਇੱਕ ਕਿੱਲੋ ਟਮਾਟਰ"]),
                  T("Ask the total.", ["how much is the total?", "the total is one hundred and forty rupees"],
                    ["ਕੁੱਲ ਕਿੰਨੇ ਦਾ ਹੋਇਆ?", "ਕੁੱਲ ਇੱਕ ਸੌ ਚਾਲੀ ਰੁਪਏ ਹੈ"]),
              ])),
            L("ਥੋੜ੍ਹਾ ਘੱਟ ਕਰੋ",
              "Bargaining is polite firmness. The opening is ਥੋੜ੍ਹਾ ਘੱਟ ਕਰੋ ਜੀ (please make it a "
              "little less), the counter is ਇਸ ਤੋਂ ਘੱਟ ਨਹੀਂ (not less than this), and the final "
              "agreement is ਠੀਕ ਹੈ, ਲੈ ਲਓ or ਲੈ ਲਓ, ਦੇ ਦਿਓ.",
              [V("ਘੱਟ", "ghatt", "less", "adverb"),
               V("ਵੱਧ", "vaddh", "more", "adverb"),
               V("ਮਹਿੰਗਾ", "mahinga", "expensive", "adjective"),
               V("ਸਸਤਾ", "sasta", "cheap", "adjective"),
               V("ਲੈ ਲਓ", "lai lo", "take it", "phrase")],
              G("Bargaining politely",
                "ਥੋੜ੍ਹਾ ਘੱਟ ਕਰੋ ਜੀ · ਇਸ ਤੋਂ ਘੱਟ ਨਹੀਂ · ਠੀਕ ਹੈ, ਲੈ ਲਓ",
                "ਕਰੋ ਜੀ softens a request, ਇਸ ਤੋਂ ਘੱਟ ਨਹੀਂ sets the floor, and ਠੀਕ ਹੈ closes the "
                "deal. ਮਹਿੰਗਾ and ਸਸਤਾ describe the shop: ਇਹ ਬਹੁਤ ਮਹਿੰਗਾ ਹੈ. The comparison takes "
                "ਤੋਂ: ਇਸ ਤੋਂ ਘੱਟ.",
                [X("ਥੋੜ੍ਹਾ ਘੱਟ ਕਰੋ ਜੀ।", "thorha ghatt karo ji.", "Please make it a little less."),
                 X("ਇਹ ਬਹੁਤ ਮਹਿੰਗਾ ਹੈ।", "ih bahut mahinga hai.", "This is very expensive."),
                 X("ਇਸ ਤੋਂ ਘੱਟ ਨਹੀਂ ਹੋ ਸਕਦਾ।", "is ton ghatt nahin ho sakda.", "It cannot be less than this.")],
                [("ਇਸ ਨਾਲੋਂ ਘੱਟ ਨਹੀਂ।", "ਇਸ ਤੋਂ ਘੱਟ ਨਹੀਂ।", "Comparison takes ਤੋਂ."),
                 ("ਥੋੜ੍ਹਾ ਘੱਟ ਕਰਦੇ ਹੋ।", "ਥੋੜ੍ਹਾ ਘੱਟ ਕਰੋ ਜੀ।", "A request is ਕਰੋ ਜੀ, not a question about habit.")]),
              [D("ਗਾਹਕ", "ਅੱਠ ਸੌ ਮਹਿੰਗਾ ਲੱਗਦਾ ਹੈ।", "atth sau mahinga lagda hai.", "Eight hundred seems expensive."),
               D("ਦੁਕਾਨਦਾਰ", "ਸੱਤ ਸੌ ਪੰਜਾਹ, ਇਸ ਤੋਂ ਘੱਟ ਨਹੀਂ।", "satt sau pachas, is ton ghatt nahin.", "Seven hundred and fifty, not a rupee less."),
               D("ਗਾਹਕ", "ਥੋੜ੍ਹਾ ਘੱਟ ਕਰੋ ਜੀ।", "thorha ghatt karo ji.", "Please make it a little less."),
               D("ਦੁਕਾਨਦਾਰ", "ਠੀਕ ਹੈ, ਲੈ ਲਓ।", "thik hai, lai lo.", "All right, take it.")],
              WS("Bargain worksheet", [
                  T("Ask for less.", ["please make it a little less", "this is very expensive"],
                    ["ਥੋੜ੍ਹਾ ਘੱਟ ਕਰੋ ਜੀ", "ਇਹ ਬਹੁਤ ਮਹਿੰਗਾ ਹੈ"]),
                  T("Hold the price.", ["it cannot be less than this", "all right, take it"],
                    ["ਇਸ ਤੋਂ ਘੱਟ ਨਹੀਂ ਹੋ ਸਕਦਾ", "ਠੀਕ ਹੈ, ਲੈ ਲਓ"]),
              ])),
        ]},
        {"id": "A1+-U3", "title": "ਮਿਲਣੀ ਅਤੇ ਵਿਦਾਇਗੀ", "lessons": [
            L("ਮਹਿਮਾਨ ਆਉਣਾ",
              "A guest is welcomed with ਜੀ ਆਇਆਂ ਨੂੰ and seats are offered with ਬੈਠੋ ਜੀ. The house "
              "answers with ਪਾਣੀ ਲਓ ਜੀ and the guest answers the news with a question of their own. "
              "None of it is rushed.",
              [V("ਮਹਿਮਾਨ", "mahiman", "guest", "noun"),
               V("ਜੀ ਆਇਆਂ ਨੂੰ", "ji aian nun", "welcome", "phrase"),
               V("ਬੈਠੋ ਜੀ", "baitho ji", "please sit", "phrase"),
               V("ਪਾਣੀ ਲਓ ਜੀ", "pani lo ji", "please have water", "phrase"),
               V("ਦੇਰ", "der", "delay", "noun")],
              G("Receiving a guest",
                "ਜੀ ਆਇਆਂ ਨੂੰ · ਬੈਠੋ ਜੀ · ਕੀ ਖ਼ਬਰ?",
                "The welcome ਜੀ ਆਇਆਂ ਨੂੰ stands alone as a sentence. ਬੈਠੋ ਜੀ offers a seat with "
                "the respectful ਜੀ, ਪਾਣੀ ਲਓ ਜੀ offers water, and ਕੀ ਖ਼ਬਰ? asks for news. ਦੇਰ ਹੋ "
                "ਗਈ (you are late) is said with a smile, never as a complaint.",
                [X("ਜੀ ਆਇਆਂ ਨੂੰ! ਬੈਠੋ ਜੀ।", "ji aian nun! baitho ji.", "Welcome! Please sit."),
                 X("ਪਾਣੀ ਲਓ ਜੀ, ਫਿਰ ਗੱਲ ਕਰੀਏ।", "pani lo ji, phir gal karie.", "Please have water, then we will talk."),
                 X("ਕੀ ਖ਼ਬਰ ਹੈ? ਦੇਰ ਹੋ ਗਈ।", "ki khabar hai? der ho gai.", "What news? You are late.")],
                [("ਜੀ ਆਇਆਂ ਨੂੰ ਆਇਆ।", "ਜੀ ਆਇਆਂ ਨੂੰ।", "The welcome is complete on its own."),
                 ("ਬੈਠੋ ਜੀ ਕਰੋ।", "ਬੈਠੋ ਜੀ।", "ਬੈਠੋ is already the verb: ਬੈਠੋ ਜੀ.")]),
              [D("ਮੇਜ਼ਬਾਨ", "ਜੀ ਆਇਆਂ ਨੂੰ! ਬੈਠੋ ਜੀ।", "ji aian nun! baitho ji.", "Welcome! Please sit."),
               D("ਮਹਿਮਾਨ", "ਸ਼ੁਕਰੀਆ, ਬੈਠ ਗਿਆ।", "shukria, baith gia.", "Thank you, I have sat down."),
               D("ਮੇਜ਼ਬਾਨ", "ਪਾਣੀ ਲਓ ਜੀ, ਕੀ ਖ਼ਬਰ ਹੈ?", "pani lo ji, ki khabar hai?", "Please have water, what news?"),
               D("ਮਹਿਮਾਨ", "ਸਭ ਠੀਕ ਹੈ, ਬਸ ਦੇਰ ਹੋ ਗਈ।", "sabh thik hai, bas der ho gai.", "All is well, only it got late.")],
              WS("Guest worksheet", [
                  T("Welcome the guest.", ["welcome! please sit", "please have water"],
                    ["ਜੀ ਆਇਆਂ ਨੂੰ! ਬੈਠੋ ਜੀ", "ਪਾਣੀ ਲਓ ਜੀ"]),
                  T("Ask for news.", ["what news? you are late", "all is well"],
                    ["ਕੀ ਖ਼ਬਰ ਹੈ? ਦੇਰ ਹੋ ਗਈ", "ਸਭ ਠੀਕ ਹੈ"]),
              ])),
            L("ਚਾਹ ਪਾਣੀ",
              "Offering chai is a small negotiation: ਚਾਹ ਪੀਓਗੇ? (will you have tea), ਇੱਕ ਕੱਪ, ਖੰਡ "
              "ਘੱਟ. The guest can refuse with ਨਾ, ਧੰਨਵਾਦ or accept with ਹਾਂ, ਇੱਕ ਕੱਪ ਠੀਕ ਹੈ.",
              [V("ਚਾਹ", "chah", "tea", "noun"),
               V("ਕੱਪ", "kapp", "cup", "noun"),
               V("ਖੰਡ", "khand", "sugar", "noun"),
               V("ਦੁੱਧ", "duddh", "milk", "noun"),
               V("ਪੀਓਗੇ?", "pioge?", "will you drink?", "phrase")],
              G("Offering and accepting",
                "ਚਾਹ ਪੀਓਗੇ? · ਇੱਕ ਕੱਪ ਠੀਕ ਹੈ · ਖੰਡ ਘੱਟ",
                "The offer is a future question: ਚਾਹ ਪੀਓਗੇ? The answer can be ਹਾਂ, ਇੱਕ ਕੱਪ or ਨਾ, "
                "ਧੰਨਵਾਦ. Preferences are stated with ਘੱਟ and ਵੱਧ: ਖੰਡ ਘੱਟ, ਦੁੱਧ ਵੱਧ. ਲਓ ਜੀ hands "
                "the cup over.",
                [X("ਚਾਹ ਪੀਓਗੇ ਜੀ?", "chah pioge ji?", "Will you have tea?"),
                 X("ਹਾਂ, ਇੱਕ ਕੱਪ, ਖੰਡ ਘੱਟ।", "han, ikk kapp, khand ghatt.", "Yes, one cup, less sugar."),
                 X("ਨਾ, ਧੰਨਵਾਦ, ਮੈਂ ਹੁਣੇ ਪੀਤੀ ਹੈ।", "na, dhannavad, main hune piti hai.", "No, thank you, I have just had some.")],
                [("ਚਾਹ ਪੀਵੋਗੇ?", "ਚਾਹ ਪੀਓਗੇ?", "The future of ਪੀਣਾ is ਪੀਓਗੇ."),
                 ("ਮੈਂ ਚਾਹ ਪੀਤੀ ਹਾਂ ਹੈ।", "ਮੈਂ ਚਾਹ ਪੀਤੀ ਹੈ।", "The present perfect ends with ਹੈ once.")]),
              [D("ਮੇਜ਼ਬਾਨ", "ਚਾਹ ਪੀਓਗੇ ਜੀ?", "chah pioge ji?", "Will you have tea?"),
               D("ਮਹਿਮਾਨ", "ਹਾਂ, ਇੱਕ ਕੱਪ। ਖੰਡ ਘੱਟ ਰੱਖੋ।", "han, ikk kapp. khand ghatt rakho.", "Yes, one cup. Keep the sugar low."),
               D("ਮੇਜ਼ਬਾਨ", "ਦੁੱਧ ਵੱਧ ਰੱਖਾਂ?", "duddh vaddh rakkhan?", "Shall I keep more milk?"),
               D("ਮਹਿਮਾਨ", "ਨਾ, ਇਹੀ ਠੀਕ ਹੈ। ਸ਼ੁਕਰੀਆ।", "na, ihi thik hai. shukria.", "No, this is fine. Thank you.")],
              WS("Chai worksheet", [
                  T("Offer.", ["will you have tea?", "shall I keep more milk?"],
                    ["ਚਾਹ ਪੀਓਗੇ ਜੀ?", "ਦੁੱਧ ਵੱਧ ਰੱਖਾਂ?"]),
                  T("Answer.", ["yes, one cup, less sugar", "no, thank you, I have just had some"],
                    ["ਹਾਂ, ਇੱਕ ਕੱਪ, ਖੰਡ ਘੱਟ", "ਨਾ, ਧੰਨਵਾਦ, ਮੈਂ ਹੁਣੇ ਪੀਤੀ ਹੈ"]),
              ])),
            L("ਵਿਦਾਇਗੀ",
              "Leaving takes three steps: ਫਿਰ ਆਉਣਾ (come again), ਹੁਣ ਚੱਲਦੇ ਹਾਂ (we are leaving "
              "now), ਫਿਰ ਮਿਲਾਂਗੇ (we will meet again). The host's line is ਰੁਕੋ ਜੀ and the "
              "guest's line is ਦੇਰ ਹੋ ਗਈ, ਘਰ ਜਾਣਾ ਹੈ.",
              [V("ਚੱਲਦੇ ਹਾਂ", "challde han", "we are leaving", "phrase"),
               V("ਫਿਰ ਮਿਲਾਂਗੇ", "phir milange", "we will meet again", "phrase"),
               V("ਰੁਕੋ ਜੀ", "ruko ji", "please wait, stay a while", "phrase"),
               V("ਘਰ ਜਾਣਾ", "ghar jana", "to go home", "verb"),
               V("ਫਿਰ ਆਉਣਾ", "phir auna", "do come again", "phrase")],
              G("Taking leave",
                "ਹੁਣ ਚੱਲਦੇ ਹਾਂ · ਫਿਰ ਮਿਲਾਂਗੇ · ਫਿਰ ਆਉਣਾ",
                "The leave-taking starts with ਹੁਣ ਚੱਲਦੇ ਹਾਂ and the reason ਘਰ ਜਾਣਾ ਹੈ. The host "
                "says ਰੁਕੋ ਜੀ or ਫਿਰ ਆਉਣਾ, the guest answers with the promise ਫਿਰ ਮਿਲਾਂਗੇ, and the "
                "door closes on ਤੁਸੀਂ ਆਉਂਦੇ ਰਹਿਣਾ.",
                [X("ਹੁਣ ਚੱਲਦੇ ਹਾਂ, ਦੇਰ ਹੋ ਗਈ।", "hun challde han, der ho gai.", "We are leaving now, it has got late."),
                 X("ਫਿਰ ਆਉਣਾ ਜੀ।", "phir auna ji.", "Do come again."),
                 X("ਫਿਰ ਮਿਲਾਂਗੇ। ਰੱਬ ਰਾਖਾ।", "phir milange. rabb rakha.", "We will meet again. God protect you.")],
                [("ਹੁਣ ਚੱਲਦਾ ਹਾਂ (two people).", "ਹੁਣ ਚੱਲਦੇ ਹਾਂ।", "Two speakers take ਚੱਲਦੇ ਹਾਂ."),
                 ("ਫਿਰ ਮਿਲਦੇ ਹਾਂ।", "ਫਿਰ ਮਿਲਾਂਗੇ।", "A future promise is ਮਿਲਾਂਗੇ.")]),
              [D("ਮੇਜ਼ਬਾਨ", "ਰੁਕੋ ਜੀ, ਹੋਰ ਚਾਹ?", "ruko ji, hor chah?", "Stay a while, more tea?"),
               D("ਮਹਿਮਾਨ", "ਨਾ ਜੀ, ਹੁਣ ਚੱਲਦੇ ਹਾਂ। ਦੇਰ ਹੋ ਗਈ।", "na ji, hun challde han. der ho gai.", "No, we are leaving now. It has got late."),
               D("ਮੇਜ਼ਬਾਨ", "ਠੀਕ ਹੈ, ਫਿਰ ਆਉਣਾ ਜੀ।", "thik hai, phir auna ji.", "All right, do come again."),
               D("ਮਹਿਮਾਨ", "ਫਿਰ ਮਿਲਾਂਗੇ। ਰੱਬ ਰਾਖਾ।", "phir milange. rabb rakha.", "We will meet again. God protect you.")],
              WS("Farewell worksheet", [
                  T("Say you are going.", ["we are leaving now, it has got late", "please stay a while"],
                    ["ਹੁਣ ਚੱਲਦੇ ਹਾਂ, ਦੇਰ ਹੋ ਗਈ", "ਰੁਕੋ ਜੀ"]),
                  T("Say you will return.", ["do come again", "we will meet again"],
                    ["ਫਿਰ ਆਉਣਾ ਜੀ", "ਫਿਰ ਮਿਲਾਂਗੇ"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Punjabi culture grew out of the settlements along five rivers, and agriculture "
                 "has stayed at its centre: land is still the measure of standing, and izzat — the "
                 "family's honour — is what a household protects in everything it says and does. "
                 "The Green Revolution of the 1960s and 70s turned the region into what writers "
                 "call the breadbasket of India and Pakistan, and the same villages that watched "
                 "wheat rise also carried Bhangra and giddha to the world outside. A learner "
                 "hears all of this in the greeting: respect first, family second, work third."),
        source_url="https://en.wikipedia.org/wiki/Punjabi_culture",
        reading=("ਸਾਡੇ ਪਿੰਡ ਵਿੱਚ ਸਵੇਰ ਚਾਰ ਵਜੇ ਸ਼ੁਰੂ ਹੁੰਦੀ ਹੈ। ਪਹਿਲਾਂ ਮੋਟਰ ਚੱਲਦੀ ਹੈ, ਫਿਰ ਖੇਤਾਂ ਨੂੰ "
                 "ਪਾਣੀ ਜਾਂਦਾ ਹੈ। ਦਾਦੀ ਚੁੱਲ੍ਹੇ ਉੱਤੇ ਚਾਹ ਬਣਾਉਂਦੀ ਹੈ ਅਤੇ ਮੈਨੂੰ ਉੱਠਣ ਲਈ ਆਵਾਜ਼ ਮਾਰਦੀ "
                 "ਹੈ। ਮੈਂ ਛੇ ਵਜੇ ਉੱਠਦਾ ਹਾਂ, ਮੂੰਹ ਧੋਂਦਾ ਹਾਂ, ਅਤੇ ਚਾਹ ਪੀਂਦਾ ਹਾਂ। ਸੱਤ ਵਜੇ ਅਖ਼ਬਾਰ ਆ "
                 "ਜਾਂਦਾ ਹੈ। ਉਹੀ ਸਵੇਰ ਦੀ ਸਭ ਤੋਂ ਵੱਡੀ ਗੱਲ ਹੁੰਦੀ ਹੈ: ਨਾਨਕੇ-ਦਾਦਕੇ ਦੀਆਂ ਖ਼ਬਰਾਂ ਅਖ਼ਬਾਰ "
                 "ਵਿੱਚ ਨਹੀਂ, ਮਾਂ ਦੇ ਫ਼ੋਨ ਵਿੱਚ ਹੁੰਦੀਆਂ ਹਨ।"),
        reading_gloss=("In our village the morning starts at four. First the motor starts, then "
                       "water goes to the fields. Grandmother makes tea on the clay stove and "
                       "calls me to get up. I get up at six, wash my face, and drink tea. At "
                       "seven the newspaper arrives. That is the biggest thing of the morning "
                       "itself: news of the mother's side and the father's side comes not in the "
                       "newspaper but in the mother's phone call."),
        listening=("ਫ਼ੋਨ ਵੱਜਦਾ ਹੈ। ਮਾਂ: ਹੈਲੋ, ਕੌਣ ਬੋਲ ਰਿਹਾ ਹੈ? ਪੁੱਤ: ਮੈਂ ਮਨਵੀਰ। ਮਾਂ: ਠੀਕ ਹੈ, ਖੇਤ "
                   "ਦਾ ਕੰਮ ਕਿਵੇਂ ਚੱਲ ਰਿਹਾ ਹੈ? ਪੁੱਤ: ਠੀਕ ਹੈ। ਪਾਣੀ ਸਮੇਂ ਸਿਰ ਆ ਗਿਆ। ਮਾਂ: ਚੰਗਾ, ਅਤੇ "
                   "ਮਾਸੀ ਨੂੰ ਫ਼ੋਨ ਕਰ ਲੈ। ਪੁੱਤ: ਠੀਕ ਹੈ, ਮੈਂ ਸ਼ਾਮ ਨੂੰ ਕਰਾਂਗਾ।"),
        listening_gloss=("The phone rings. Mother: Hello, who is speaking? Son: I am Manveer. "
                         "Mother: All right, how is the work in the fields going? Son: It is "
                         "fine. The water came on time. Mother: Good, and give aunt a call. "
                         "Son: All right, I will call in the evening."),
        voice_tag=VOICE,
        idioms=[
            ("ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ", "the timeless One is immortal", "the everyday respectful greeting"),
            ("ਜੀ ਆਇਆਂ ਨੂੰ", "may your coming be with honour", "welcome to a guest"),
            ("ਰੱਬ ਰਾਖਾ", "may God protect you", "said on parting, blessing the other person"),
            ("ਵਾਹ ਵਾਹ", "wonder, wonder", "praise for something well done"),
            ("ਕੋਈ ਗੱਲ ਨਹੀਂ", "it is no matter", "it is nothing, do not worry"),
            ("ਚੰਗਾ ਚੰਗਾ", "good, good", "relaxed agreement, a job agreed to"),
            ("ਹੁਣੇ ਹੁਣੇ", "just now", "a very short time ago"),
            ("ਥੋੜ੍ਹਾ ਘੱਟ", "a little less", "the opening line of a bargain"),
            ("ਦੇਰ ਹੋ ਗਈ", "the delay has happened", "sorry, I am late"),
            ("ਫਿਰ ਮਿਲਾਂਗੇ", "we will meet again", "the ordinary goodbye"),
        ],
        mistakes=[
            ("ਮੈਂ ਠੀਕ ਹੋ।", "ਮੈਂ ਠੀਕ ਹਾਂ।", "First person singular takes ਹਾਂ."),
            ("ਕੀ ਘਰ ਵਾਲੇ ਠੀਕ ਹੈ?", "ਕੀ ਘਰ ਵਾਲੇ ਠੀਕ ਹਨ?", "ਘਰ ਵਾਲੇ is plural: ਹਨ."),
            ("ਦੋ ਗਲਾਸਾਂ ਪਾਣੀ ਦਿਓ।", "ਦੋ ਗਲਾਸ ਪਾਣੀ ਦਿਓ।", "After a number the noun stays plain."),
        ],
        task_title="Introduce three people and take one leave, in Punjabi",
        task_instructions=("Write a Punjabi exchange of eight to ten turns. Greet a neighbour and "
                           "ask after the family, give your own morning routine with three verbs "
                           "in the -ਦਾ ਹਾਂ form, ask the rate of one vegetable and bargain it "
                           "down by fifty rupees with ਥੋੜ੍ਹਾ ਘੱਟ ਕਰੋ ਜੀ, then take leave with "
                           "ਦੇਰ ਹੋ ਗਈ and ਫਿਰ ਮਿਲਾਂਗੇ."),
    ),
    "test": [
        ("translate_en", "Say: I am fine, thank you.", "ਮੈਂ ਠੀਕ ਹਾਂ, ਧੰਨਵਾਦ।"),
        ("translate_pa", "ਮੈਂ ਰੋਜ਼ ਛੇ ਵਜੇ ਉੱਠਦਾ ਹਾਂ।", "I get up at six every day."),
        ("multiple_choice", "Which sentence asks for a lower price?", "ਥੋੜ੍ਹਾ ਘੱਟ ਕਰੋ ਜੀ।"),
        ("fill_in_the_blank", "ਇੱਕ ਕਿੱਲੋ ਟਮਾਟਰ ___।", "ਦਿਓ"),
        ("word_selection", "Select the Punjabi for 'welcome'.", "ਜੀ ਆਇਆਂ ਨੂੰ"),
        ("error_correction", "ਮੈਂ ਬਾਅਦ ਵਿੱਚ ਫ਼ੋਨ ਕਰਦਾ ਹਾਂ।", "ਮੈਂ ਬਾਅਦ ਵਿੱਚ ਫ਼ੋਨ ਕਰਾਂਗਾ।"),
        ("dialogue_completion", "Complete: ਚਾਹ ਪੀਓਗੇ ਜੀ? — ___ (Yes, one cup)", "ਹਾਂ, ਇੱਕ ਕੱਪ"),
        ("matching", "Match ਕੁੱਲ to its meaning.", "total"),
        ("reading_comprehension", "ਪਿੰਡ ਵਿੱਚ ਸਵੇਰ ਕਦੋਂ ਸ਼ੁਰੂ ਹੁੰਦੀ ਹੈ?", "at four"),
        ("inference", "ਮਾਂ ਫ਼ੋਨ ਉੱਤੇ ਖੇਤਾਂ ਬਾਰੇ ਪੁੱਛਦੀ ਹੈ। — what does this tell us about her?", "she keeps track of the family's work"),
        ("main_idea", "ਸਵੇਰ ਦੀ ਸਭ ਤੋਂ ਵੱਡੀ ਗੱਲ ਮਾਂ ਦਾ ਫ਼ੋਨ ਹੁੰਦਾ ਹੈ। — what is this sentence?", "the main point of the reading"),
        ("detail_identification", "ਪੁੱਤ ਮਾਸੀ ਨੂੰ ਕਦੋਂ ਫ਼ੋਨ ਕਰੇਗਾ?", "in the evening"),
    ],
}

HALFSTEPS["A2+"] = {
    "native": NATIVE,
    "title": "%s A2+ — Bus stand, bazaar and repair shop" % NAME,
    "goals": [
        "Buy a ticket, ask when the bus leaves, and understand a delay announcement",
        "Ask the way, give a landmark, and check that you have understood",
        "Deal with a repair shop: say what broke, agree a time, and ask about the bill",
    ],
    "units": [
        {"id": "A2+-U1", "title": "ਬੱਸ ਅੱਡਾ", "lessons": [
            L("ਟਿਕਟ ਅਤੇ ਸਮਾਂ",
              "At a bus stand it helps to know three sentences: ਦੋ ਟਿਕਟਾਂ ਦਿਓ, ਬੱਸ ਕਿੰਨੇ ਵਜੇ ਚੱਲਦੀ "
              "ਹੈ? and ਕਿੱਥੋਂ ਚੜ੍ਹਨਾ ਹੈ? The time is said with ਵਜੇ, the destination with ਤੱਕ or ਨੂੰ, "
              "and ਜਾਣਾ ਹੈ states where you must go.",
              [V("ਟਿਕਟ", "tikat", "ticket", "noun"),
               V("ਬੱਸ", "bass", "bus", "noun"),
               V("ਚੱਲਦੀ ਹੈ", "challdi hai", "leaves, runs", "phrase"),
               V("ਤੱਕ", "takk", "up to", "postposition"),
               V("ਜਾਣਾ ਹੈ", "jana hai", "have to go", "phrase")],
              G("Tickets and timings",
                "ਦੋ ਟਿਕਟਾਂ ਦਿਓ · ਬੱਸ ਕਿੰਨੇ ਵਜੇ ਚੱਲਦੀ ਹੈ? · ਕਿੱਥੋਂ ਚੜ੍ਹਨਾ ਹੈ?",
                "The ticket is counted with the noun, and the destination takes ਤੱਕ or ਨੂੰ: "
                "ਅੰਮ੍ਰਿਤਸਰ ਤੱਕ. Timings take ਵਜੇ: ਸਵਾ ਨੌਂ ਵਜੇ. The plan is stated with ਜਾਣਾ ਹੈ "
                "(I have to go), and the question ਕਿੱਥੋਂ? asks from where the bus leaves.",
                [X("ਦੋ ਟਿਕਟਾਂ ਅੰਮ੍ਰਿਤਸਰ ਤੱਕ ਦਿਓ।", "do tiktan Amritsar takk dio.", "Give me two tickets to Amritsar."),
                 X("ਬੱਸ ਕਿੰਨੇ ਵਜੇ ਚੱਲਦੀ ਹੈ?", "bass kinne vaje challdi hai?", "What time does the bus leave?"),
                 X("ਮੈਨੂੰ ਲੁਧਿਆਣਾ ਜਾਣਾ ਹੈ।", "mainun Ludhiana jana hai.", "I have to go to Ludhiana.")],
                [("ਬੱਸ ਕਿੰਨੇ ਵਜੇ ਚੱਲਦਾ ਹੈ?", "ਬੱਸ ਕਿੰਨੇ ਵਜੇ ਚੱਲਦੀ ਹੈ?", "ਬੱਸ is feminine: ਚੱਲਦੀ ਹੈ."),
                 ("ਦੋ ਟਿਕਟਾ ਦਿਓ।", "ਦੋ ਟਿਕਟਾਂ ਦਿਓ।", "Feminine plurals end in -ਾਂ: ਟਿਕਟਾਂ.")]),
              [D("ਯਾਤਰੀ", "ਦੋ ਟਿਕਟਾਂ ਅੰਮ੍ਰਿਤਸਰ ਤੱਕ ਦਿਓ।", "do tiktan Amritsar takk dio.", "Give me two tickets to Amritsar."),
               D("ਕਲਰਕ", "ਅੰਮ੍ਰਿਤਸਰ ਵਾਲੀ ਬੱਸ ਸਵਾ ਨੌਂ ਵਜੇ ਚੱਲਦੀ ਹੈ।", "Amritsar vali bass sava nau vaje challdi hai.", "The Amritsar bus leaves at quarter past nine."),
               D("ਯਾਤਰੀ", "ਕਿੱਥੋਂ ਚੜ੍ਹਨਾ ਹੈ?", "kitthon charhna hai?", "Where do I board?"),
               D("ਕਲਰਕ", "ਪਲੇਟਫ਼ਾਰਮ ਦੋ ਤੋਂ, ਉਹੀ ਬੱਸ ਹੈ।", "platform do ton, uhi bass hai.", "From platform two, that is the bus.")],
              WS("Ticket worksheet", [
                  T("Buy the ticket.", ["two tickets to Amritsar", "what time does the bus leave?"],
                    ["ਦੋ ਟਿਕਟਾਂ ਅੰਮ੍ਰਿਤਸਰ ਤੱਕ", "ਬੱਸ ਕਿੰਨੇ ਵਜੇ ਚੱਲਦੀ ਹੈ?"]),
                  T("Say the plan.", ["I have to go to Ludhiana", "from platform two"],
                    ["ਮੈਨੂੰ ਲੁਧਿਆਣਾ ਜਾਣਾ ਹੈ", "ਪਲੇਟਫ਼ਾਰਮ ਦੋ ਤੋਂ"]),
              ])),
            L("ਰਾਹ ਪੁੱਛਣਾ",
              "Asking the way gives you a landmark, a distance and a direction: ਇੱਥੋਂ ਨੇੜੇ, ਸਿੱਧਾ "
              "ਜਾਓ, ਪਹਿਲੇ ਮੋੜ ਤੋਂ ਸੱਜੇ. Repeat the answer back with ਠੀਕ ਹੈ, ਸਿੱਧਾ? — that is how "
              "you check that you have understood.",
              [V("ਰਾਹ", "rah", "way, road", "noun"),
               V("ਨੇੜੇ", "nere", "near", "adverb"),
               V("ਸਿੱਧਾ", "siddha", "straight", "adverb"),
               V("ਮੋੜ", "mor", "turn", "noun"),
               V("ਸੱਜੇ", "sajje", "to the right", "adverb")],
              G("Asking and repeating the way",
                "ਇੱਥੋਂ ਨੇੜੇ ਹੈ? · ਸਿੱਧਾ ਜਾਓ · ਪਹਿਲੇ ਮੋੜ ਤੋਂ ਸੱਜੇ",
                "Directions use ਜਾਓ and turn with ਤੋਂ: ਪਹਿਲੇ ਮੋੜ ਤੋਂ ਸੱਜੇ. Distance is ਨੇੜੇ or ਦੂਰ, "
                "and the shop is spotted with ਵਾਲਾ: ਬੱਸ ਅੱਡੇ ਵਾਲਾ ਬਾਜ਼ਾਰ. Repeating the answer "
                "with ਠੀਕ ਹੈ confirms it without repeating the whole sentence.",
                [X("ਬੱਸ ਅੱਡਾ ਇੱਥੋਂ ਨੇੜੇ ਹੈ?", "bass adda itthon nere hai?", "Is the bus stand near here?"),
                 X("ਸਿੱਧਾ ਜਾਓ, ਫਿਰ ਪਹਿਲੇ ਮੋੜ ਤੋਂ ਸੱਜੇ।", "siddha jao, phir pahile mor ton sajje.", "Go straight, then right at the first turn."),
                 X("ਠੀਕ ਹੈ, ਸਿੱਧਾ ਅਤੇ ਫਿਰ ਸੱਜੇ?", "thik hai, siddha ate phir sajje?", "All right, straight and then right?")],
                [("ਸਿੱਧਾ ਜਾਂਦੇ ਹੋ।", "ਸਿੱਧਾ ਜਾਓ।", "A direction is ਜਾਓ, not a statement about habit."),
                 ("ਪਹਿਲਾ ਮੋੜ ਸੱਜੇ।", "ਪਹਿਲੇ ਮੋੜ ਤੋਂ ਸੱਜੇ।", "The turn takes ਤੋਂ: ਮੋੜ ਤੋਂ ਸੱਜੇ.")]),
              [D("ਯਾਤਰੀ", "ਬਾਜ਼ਾਰ ਇੱਥੋਂ ਨੇੜੇ ਹੈ?", "bazar itthon nere hai?", "Is the market near here?"),
               D("ਰਾਹਗੀਰ", "ਹਾਂ, ਸਿੱਧਾ ਜਾਓ, ਪਹਿਲੇ ਮੋੜ ਤੋਂ ਸੱਜੇ।", "han, siddha jao, pahile mor ton sajje.", "Yes, go straight, right at the first turn."),
               D("ਯਾਤਰੀ", "ਠੀਕ ਹੈ, ਸਿੱਧਾ ਅਤੇ ਫਿਰ ਸੱਜੇ?", "thik hai, siddha ate phir sajje?", "All right, straight and then right?"),
               D("ਰਾਹਗੀਰ", "ਹਾਂ, ਉੱਥੇ ਹੀ ਬੱਸ ਅੱਡੇ ਵਾਲਾ ਬਾਜ਼ਾਰ ਹੈ।", "han, utthe hi bass adde vala bazar hai.", "Yes, the bus-stand market is right there.")],
              WS("Directions worksheet", [
                  T("Ask the way.", ["is the bus stand near here?", "go straight, then right at the first turn"],
                    ["ਬੱਸ ਅੱਡਾ ਇੱਥੋਂ ਨੇੜੇ ਹੈ?", "ਸਿੱਧਾ ਜਾਓ, ਫਿਰ ਪਹਿਲੇ ਮੋੜ ਤੋਂ ਸੱਜੇ"]),
                  T("Check the answer.", ["all right, straight and then right?", "the bus-stand market is right there"],
                    ["ਠੀਕ ਹੈ, ਸਿੱਧਾ ਅਤੇ ਫਿਰ ਸੱਜੇ?", "ਉੱਥੇ ਹੀ ਬੱਸ ਅੱਡੇ ਵਾਲਾ ਬਾਜ਼ਾਰ ਹੈ"]),
              ])),
            L("ਦੇਰੀ ਦਾ ਐਲਾਨ",
              "Announcements come fast, so the learner listens for three words: ਦੇਰੀ (delay), "
              "ਅੱਧਾ ਘੰਟਾ (half an hour), ਟਾਈਮ ਬਦਲ ਗਿਆ (the time has changed). The compound "
              "verb ਬਦਲ ਗਿਆ shows a change that has already happened.",
              [V("ਦੇਰੀ", "deri", "delay", "noun"),
               V("ਅੱਧਾ ਘੰਟਾ", "addha ghanta", "half an hour", "noun"),
               V("ਐਲਾਨ", "ailan", "announcement", "noun"),
               V("ਬਦਲ ਗਿਆ", "badal gia", "has changed", "phrase"),
               V("ਉਡੀਕ", "udik", "wait", "noun")],
              G("Hearing a delay",
                "ਬੱਸ ਵਿੱਚ ਦੇਰੀ ਹੈ · ਟਾਈਮ ਬਦਲ ਗਿਆ · ਅੱਧਾ ਘੰਟਾ ਉਡੀਕ ਕਰੋ",
                "A delay is reported as ਦੇਰੀ ਹੈ, a change as ਬਦਲ ਗਿਆ, and the wait as ਉਡੀਕ ਕਰੋ. "
                "The past ਬਦਲ ਗਿਆ is about what has already happened, so it takes no ਹੈ: ਟਾਈਮ ਬਦਲ "
                "ਗਿਆ, not ਟਾਈਮ ਬਦਲ ਗਿਆ ਹੈ.",
                [X("ਐਲਾਨ ਅਨੁਸਾਰ ਬੱਸ ਵਿੱਚ ਦੇਰੀ ਹੈ।", "ailan anusar bass vich deri hai.", "According to the announcement the bus is delayed."),
                 X("ਟਾਈਮ ਬਦਲ ਗਿਆ ਹੈ, ਅੱਧਾ ਘੰਟਾ ਉਡੀਕ ਕਰੋ।", "taim badal gia hai, addha ghanta udik karo.", "The time has changed, wait half an hour."),
                 X("ਅਸੀਂ ਇੱਥੇ ਉਡੀਕ ਕਰਦੇ ਹਾਂ।", "asin itthe udik karde han.", "We wait here.")],
                [("ਬੱਸ ਦੀ ਦੇਰੀ ਕਰਦੀ ਹੈ।", "ਬੱਸ ਵਿੱਚ ਦੇਰੀ ਹੈ।", "A delay is ਦੇਰੀ ਹੈ, not a verb of doing."),
                 ("ਟਾਈਮ ਬਦਲ ਕੀਤਾ।", "ਟਾਈਮ ਬਦਲ ਗਿਆ।", "A change that happens by itself takes ਗਿਆ.")]),
              [D("ਕੰਡਕਟਰ", "ਇੱਕ ਐਲਾਨ ਹੈ: ਬੱਸ ਵਿੱਚ ਅੱਧਾ ਘੰਟਾ ਦੇਰੀ ਹੈ।", "ikk ailan hai: bass vich addha ghanta deri hai.", "There is an announcement: the bus is delayed by half an hour."),
               D("ਯਾਤਰੀ", "ਟਾਈਮ ਬਦਲ ਗਿਆ?", "taim badal gia?", "Has the time changed?"),
               D("ਕੰਡਕਟਰ", "ਹਾਂ, ਸਵਾ ਨੌਂ ਦੀ ਥਾਂ ਦਸ ਵਜੇ।", "han, sava nau di than das vaje.", "Yes, ten o'clock instead of quarter past nine."),
               D("ਯਾਤਰੀ", "ਠੀਕ ਹੈ, ਅਸੀਂ ਇੱਥੇ ਉਡੀਕ ਕਰਦੇ ਹਾਂ।", "thik hai, asin itthe udik karde han.", "All right, we will wait here.")],
              WS("Delay worksheet", [
                  T("Report the delay.", ["the bus is delayed by half an hour", "the time has changed"],
                    ["ਬੱਸ ਵਿੱਚ ਅੱਧਾ ਘੰਟਾ ਦੇਰੀ ਹੈ", "ਟਾਈਮ ਬਦਲ ਗਿਆ"]),
                  T("Say what you will do.", ["we will wait here", "ten o'clock instead of quarter past nine"],
                    ["ਅਸੀਂ ਇੱਥੇ ਉਡੀਕ ਕਰਾਂਗੇ", "ਸਵਾ ਨੌਂ ਦੀ ਥਾਂ ਦਸ ਵਜੇ"]),
              ])),
        ]},
        {"id": "A2+-U2", "title": "ਬਾਜ਼ਾਰ ਦਾ ਕੰਮ", "lessons": [
            L("ਪੈਸੇ ਅਤੇ ਰਸੀਦ",
              "Money matters need exact nouns: ਰਸੀਦ (receipt), ਬਾਕੀ (balance), ਉਧਾਰ (credit), "
              "ਖੁੱਲ੍ਹੇ (change). ਬਾਕੀ ਕਿੰਨੀ ਬਚਦੀ ਹੈ? asks what is left to pay, and ਰਸੀਦ ਦੇ ਦਿਓ "
              "asks for the paper without argument.",
              [V("ਰਸੀਦ", "rasid", "receipt", "noun"),
               V("ਬਾਕੀ", "baki", "balance, remaining", "noun"),
               V("ਉਧਾਰ", "udhar", "credit, loan", "noun"),
               V("ਖੁੱਲ੍ਹੇ", "khulle", "small change", "noun"),
               V("ਗਿਣਤੀ", "ginti", "counting, total", "noun")],
              G("Paying and getting a receipt",
                "ਬਾਕੀ ਕਿੰਨੀ ਬਚਦੀ ਹੈ? · ਰਸੀਦ ਦੇ ਦਿਓ · ਖੁੱਲ੍ਹੇ ਨਹੀਂ ਹਨ",
                "ਬਾਕੀ and ਗਿਣਤੀ are feminine, so they take ਬਚਦੀ ਹੈ and ਠੀਕ ਹੈ. ਦੇ ਦਿਓ asks for "
                "something to be handed over at once, ਉਧਾਰ ਲੈਣਾ takes credit, and ਖੁੱਲ੍ਹੇ ਨਹੀਂ ਹਨ "
                "explains why the note cannot be changed.",
                [X("ਬਾਕੀ ਪੰਜਾਹ ਰੁਪਏ ਬਚਦੇ ਹਨ।", "baki pachas rupae bachde han.", "Fifty rupees remain to be paid."),
                 X("ਰਸੀਦ ਦੇ ਦਿਓ, ਗਿਣਤੀ ਮਿਲਾ ਲਵਾਂ।", "rasid de dio, ginti mila lavan.", "Give me the receipt, let me check the total."),
                 X("ਮੇਰੇ ਕੋਲ ਖੁੱਲ੍ਹੇ ਨਹੀਂ ਹਨ।", "mere kol khulle nahin han.", "I do not have small change.")],
                [("ਬਾਕੀ ਕਿੰਨਾ ਬਚਦੀ ਹੈ?", "ਬਾਕੀ ਕਿੰਨੀ ਬਚਦੀ ਹੈ?", "ਬਾਕੀ is feminine: ਕਿੰਨੀ ਬਚਦੀ ਹੈ."),
                 ("ਰਸੀਦ ਦਿਓ।", "ਰਸੀਦ ਦੇ ਦਿਓ।", "ਦੇ ਦਿਓ asks for it to be handed over now.")]),
              [D("ਗਾਹਕ", "ਕੁੱਲ ਕਿੰਨੀ ਗਿਣਤੀ ਹੋਈ?", "kull kinni ginti hoi?", "What is the total?"),
               D("ਦੁਕਾਨਦਾਰ", "ਇੱਕ ਹਜ਼ਾਰ ਦੋ ਸੌ। ਤੁਸੀਂ ਅੱਠ ਸੌ ਦਿੱਤੇ ਸਨ।", "ikk hazar do sau. tusin atth sau ditte san.", "One thousand two hundred. You had given eight hundred."),
               D("ਗਾਹਕ", "ਬਾਕੀ ਚਾਰ ਸੌ ਬਚਦੇ ਹਨ। ਰਸੀਦ ਦੇ ਦਿਓ।", "baki char sau bachde han. rasid de dio.", "Four hundred remain. Give me the receipt."),
               D("ਦੁਕਾਨਦਾਰ", "ਇਹ ਰਸੀਦ, ਅਤੇ ਖੁੱਲ੍ਹੇ ਵੀ ਲੈ ਲਓ।", "ih rasid, ate khulle vi lai lo.", "Here is the receipt, and take the change too.")],
              WS("Money worksheet", [
                  T("Ask about the money.", ["what is the total?", "fifty rupees remain to be paid"],
                    ["ਕੁੱਲ ਕਿੰਨੀ ਗਿਣਤੀ ਹੋਈ?", "ਬਾਕੀ ਪੰਜਾਹ ਰੁਪਏ ਬਚਦੇ ਹਨ"]),
                  T("Ask for the paper.", ["give me the receipt", "I do not have small change"],
                    ["ਰਸੀਦ ਦੇ ਦਿਓ", "ਮੇਰੇ ਕੋਲ ਖੁੱਲ੍ਹੇ ਨਹੀਂ ਹਨ"]),
              ])),
            L("ਬੈਂਕ ਦੀ ਲਾਈਨ",
              "In a bank you fill in a form and show identity: ਫਾਰਮ ਭਰਨਾ, ਪਛਾਣ ਪੱਤਰ, ਖਾਤਾ ਨੰਬਰ. "
              "The queue moves with ਹੁਣ ਕਿਸ ਦੀ ਵਾਰੀ ਹੈ? and the clerk asks ਤੁਹਾਡਾ ਖਾਤਾ ਨੰਬਰ ਕੀ ਹੈ?",
              [V("ਫਾਰਮ", "faram", "form", "noun"),
               V("ਭਰਨਾ", "bharna", "to fill in", "verb"),
               V("ਪਛਾਣ ਪੱਤਰ", "pachhan pattar", "identity document", "noun"),
               V("ਖਾਤਾ", "khata", "account", "noun"),
               V("ਲਾਈਨ", "lain", "queue, line", "noun")],
              G("At the counter",
                "ਫਾਰਮ ਭਰਨਾ ਹੈ · ਪਛਾਣ ਪੱਤਰ ਦਿਖਾਓ · ਖਾਤਾ ਨੰਬਰ ਕੀ ਹੈ?",
                "The obligation is ਮੈਨੂੰ ਫਾਰਮ ਭਰਨਾ ਹੈ (I have to fill in the form). ਦਿਖਾਓ asks "
                "for a document to be shown, ਦੱਸੋ for information to be given, and ਲਾਈਨ ਵਿੱਚ ਖੜ੍ਹੋ "
                "keeps the queue in order.",
                [X("ਮੈਨੂੰ ਇਹ ਫਾਰਮ ਭਰਨਾ ਹੈ।", "mainun ih faram bharna hai.", "I have to fill in this form."),
                 X("ਪਛਾਣ ਪੱਤਰ ਦਿਖਾਓ।", "pachhan pattar dikhao.", "Show the identity document."),
                 X("ਤੁਹਾਡਾ ਖਾਤਾ ਨੰਬਰ ਕੀ ਹੈ?", "tuhada khata nambar ki hai?", "What is your account number?")],
                [("ਮੈਨੂੰ ਫਾਰਮ ਭਰਦਾ ਹੈ।", "ਮੈਨੂੰ ਫਾਰਮ ਭਰਨਾ ਹੈ।", "The obligation is ਭਰਨਾ ਹੈ."),
                 ("ਲਾਈਨ ਵਿੱਚ ਖੜ੍ਹਦੇ ਹੋ।", "ਲਾਈਨ ਵਿੱਚ ਖੜ੍ਹੋ।", "An instruction takes ਖੜ੍ਹੋ.")]),
              [D("ਕਲਰਕ", "ਤੁਹਾਡਾ ਖਾਤਾ ਨੰਬਰ ਕੀ ਹੈ?", "tuhada khata nambar ki hai?", "What is your account number?"),
               D("ਗਾਹਕ", "ਨੰਬਰ ਇਸ ਕਾਗਜ਼ ਉੱਤੇ ਹੈ।", "nambar is kagaz utte hai.", "The number is on this paper."),
               D("ਕਲਰਕ", "ਠੀਕ ਹੈ। ਇਹ ਫਾਰਮ ਭਰੋ ਅਤੇ ਪਛਾਣ ਪੱਤਰ ਦਿਖਾਓ।", "thik hai. ih faram bharo ate pachhan pattar dikhao.", "All right. Fill in this form and show the identity document."),
               D("ਗਾਹਕ", "ਮੈਨੂੰ ਫਾਰਮ ਭਰਨਾ ਹੈ? ਮੈਂ ਹੁਣੇ ਭਰ ਦਿੰਦਾ ਹਾਂ।", "mainun faram bharna hai? main hune bhar dinda han.", "I have to fill in the form? I will fill it in just now.")],
              WS("Bank worksheet", [
                  T("State the task.", ["I have to fill in this form", "what is your account number?"],
                    ["ਮੈਨੂੰ ਇਹ ਫਾਰਮ ਭਰਨਾ ਹੈ", "ਤੁਹਾਡਾ ਖਾਤਾ ਨੰਬਰ ਕੀ ਹੈ?"]),
                  T("Give the instruction.", ["show the identity document", "stand in the queue"],
                    ["ਪਛਾਣ ਪੱਤਰ ਦਿਖਾਓ", "ਲਾਈਨ ਵਿੱਚ ਖੜ੍ਹੋ"]),
              ])),
            L("ਘੱਟ ਤੋਲੇ ਦੀ ਸ਼ਿਕਾਇਤ",
              "If the weight is short, the complaint stays factual: ਤੋਲ ਘੱਟ ਹੈ (the weight is "
              "short), ਦੁਬਾਰਾ ਤੋਲੋ (weigh it again), ਮਸ਼ੀਨ ਦੇਖੋ. The compound ਤੋਲ ਦੇਖਣਾ means to "
              "check the weight, and ਮਿਲਾ ਲੈਣਾ to match it against the bill.",
              [V("ਤੋਲ", "tol", "weight", "noun"),
               V("ਘੱਟ", "ghatt", "short, less", "adverb"),
               V("ਦੁਬਾਰਾ", "dubara", "again", "adverb"),
               V("ਮਸ਼ੀਨ", "mashin", "machine, scale", "noun"),
               V("ਸ਼ਿਕਾਇਤ", "shikait", "complaint", "noun")],
              G("Complaining about weight",
                "ਤੋਲ ਘੱਟ ਹੈ · ਦੁਬਾਰਾ ਤੋਲੋ · ਮਸ਼ੀਨ ਦੇਖੋ",
                "The sentence is a plain statement: ਤੋਲ ਘੱਟ ਹੈ. ਦੁਬਾਰਾ ਤੋਲੋ asks for a second "
                "weighing, ਮਿਲਾ ਲਵਾਂ checks the total, and ਸ਼ਿਕਾਇਤ ਕਰਨਾ is the last step, kept for "
                "when the shop does not respond.",
                [X("ਇਹ ਤੋਲ ਘੱਟ ਹੈ, ਦੁਬਾਰਾ ਤੋਲੋ।", "ih tol ghatt hai, dubara tolo.", "This weight is short, weigh it again."),
                 X("ਮਸ਼ੀਨ ਦੇਖੋ, ਸ਼ਾਇਦ ਨੁਕਸ ਹੈ।", "mashin dekho, shaid nukas hai.", "Look at the scale, maybe there is a fault."),
                 X("ਮੈਂ ਗਿਣਤੀ ਮਿਲਾ ਲਵਾਂਗਾ।", "main ginti mila lavanga.", "I will check the total.")],
                [("ਤੋਲ ਘੱਟ ਹੋ।", "ਤੋਲ ਘੱਟ ਹੈ।", "A statement takes ਹੈ."),
                 ("ਦੁਬਾਰਾ ਤੋਲਦੇ ਹੋ।", "ਦੁਬਾਰਾ ਤੋਲੋ।", "A request takes ਤੋਲੋ.")]),
              [D("ਗਾਹਕ", "ਇਹ ਤੋਲ ਘੱਟ ਹੈ।", "ih tol ghatt hai.", "This weight is short."),
               D("ਦੁਕਾਨਦਾਰ", "ਮਸ਼ੀਨ ਠੀਕ ਹੈ ਜੀ।", "mashin thik hai ji.", "The scale is fine."),
               D("ਗਾਹਕ", "ਫਿਰ ਦੁਬਾਰਾ ਤੋਲੋ।", "phir dubara tolo.", "Then weigh it again."),
               D("ਦੁਕਾਨਦਾਰ", "ਠੀਕ ਹੈ, ਦੇਖੋ — ਇੱਕ ਕਿੱਲੋ ਪੂਰਾ ਹੈ।", "thik hai, dekho — ikk killo pura hai.", "All right, look — one kilogram exactly.")],
              WS("Weight worksheet", [
                  T("State the problem.", ["this weight is short", "look at the scale, maybe there is a fault"],
                    ["ਇਹ ਤੋਲ ਘੱਟ ਹੈ", "ਮਸ਼ੀਨ ਦੇਖੋ, ਸ਼ਾਇਦ ਨੁਕਸ ਹੈ"]),
                  T("Ask again.", ["weigh it again", "I will check the total"],
                    ["ਦੁਬਾਰਾ ਤੋਲੋ", "ਮੈਂ ਗਿਣਤੀ ਮਿਲਾ ਲਵਾਂਗਾ"]),
              ])),
        ]},
        {"id": "A2+-U3", "title": "ਮੁਰੰਮਤ ਦਾ ਕੰਮ", "lessons": [
            L("ਮਿਸਤਰੀ ਨੂੰ ਬੁਲਾਉਣਾ",
              "Calling a mechanic needs the fault, the address and a time: ਪੱਖਾ ਖ਼ਰਾਬ ਹੋ ਗਿਆ ਹੈ, "
              "ਗਲੀ ਨੰਬਰ ਚਾਰ, ਸ਼ਾਮ ਨੂੰ ਆ ਜਾਓ. The compound ਖ਼ਰਾਬ ਹੋ ਗਿਆ reports the fault, and "
              "ਆ ਜਾਓ makes the visit sound easy.",
              [V("ਮਿਸਤਰੀ", "mistari", "mechanic, artisan", "noun"),
               V("ਖ਼ਰਾਬ", "kharab", "spoiled, out of order", "adjective"),
               V("ਪੱਖਾ", "pakhha", "fan", "noun"),
               V("ਗਲੀ", "gali", "lane, street", "noun"),
               V("ਆ ਜਾਓ", "a jao", "come over", "phrase")],
              G("Describing a fault on the phone",
                "ਪੱਖਾ ਖ਼ਰਾਬ ਹੋ ਗਿਆ ਹੈ · ਗਲੀ ਨੰਬਰ ਚਾਰ · ਸ਼ਾਮ ਨੂੰ ਆ ਜਾਓ",
                "The fault is reported with ਹੋ ਗਿਆ: ਪੱਖਾ ਖ਼ਰਾਬ ਹੋ ਗਿਆ ਹੈ. The address is given "
                "with ਨੰਬਰ and the time with ਨੂੰ (ਸ਼ਾਮ ਨੂੰ). ਆ ਜਾਓ asks for a visit and ਹੁਣੇ "
                "ਆਉਂਦਾ ਹਾਂ answers it.",
                [X("ਪੱਖਾ ਖ਼ਰਾਬ ਹੋ ਗਿਆ ਹੈ।", "pakhha kharab ho gia hai.", "The fan has gone out of order."),
                 X("ਅਸੀਂ ਗਲੀ ਨੰਬਰ ਚਾਰ ਵਿੱਚ ਰਹਿੰਦੇ ਹਾਂ।", "asin gali nambar char vich rahinde han.", "We live in lane number four."),
                 X("ਸ਼ਾਮ ਨੂੰ ਆ ਜਾਓ।", "sham nun a jao.", "Come over in the evening.")],
                [("ਪੱਖਾ ਖ਼ਰਾਬ ਹੈ ਗਿਆ।", "ਪੱਖਾ ਖ਼ਰਾਬ ਹੋ ਗਿਆ ਹੈ।", "The compound is ਹੋ ਗਿਆ ਹੈ."),
                 ("ਸ਼ਾਮ ਵਿੱਚ ਆ ਜਾਓ।", "ਸ਼ਾਮ ਨੂੰ ਆ ਜਾਓ।", "A time of day takes ਨੂੰ: ਸ਼ਾਮ ਨੂੰ.")]),
              [D("ਗਾਹਕ", "ਮਿਸਤਰੀ ਜੀ, ਪੱਖਾ ਖ਼ਰਾਬ ਹੋ ਗਿਆ ਹੈ।", "mistari ji, pakhha kharab ho gia hai.", "Mechanic, the fan has gone out of order."),
               D("ਮਿਸਤਰੀ", "ਪਤਾ ਦੱਸੋ।", "pata dasso.", "Tell me the address."),
               D("ਗਾਹਕ", "ਗਲੀ ਨੰਬਰ ਚਾਰ, ਸ਼ਾਮ ਨੂੰ ਆ ਜਾਓ।", "gali nambar char, sham nun a jao.", "Lane number four, come over in the evening."),
               D("ਮਿਸਤਰੀ", "ਠੀਕ ਹੈ, ਹੁਣੇ ਆਉਂਦਾ ਹਾਂ।", "thik hai, hune aunda han.", "All right, I am coming just now.")],
              WS("Call worksheet", [
                  T("Report the fault.", ["the fan has gone out of order", "come over in the evening"],
                    ["ਪੱਖਾ ਖ਼ਰਾਬ ਹੋ ਗਿਆ ਹੈ", "ਸ਼ਾਮ ਨੂੰ ਆ ਜਾਓ"]),
                  T("Give the address.", ["we live in lane number four", "tell me the address"],
                    ["ਅਸੀਂ ਗਲੀ ਨੰਬਰ ਚਾਰ ਵਿੱਚ ਰਹਿੰਦੇ ਹਾਂ", "ਪਤਾ ਦੱਸੋ"]),
              ])),
            L("ਕੀ ਖ਼ਰਾਬ ਹੋਇਆ",
              "The mechanic diagnoses in order: ਕੀ ਹੋਇਆ? (what happened), ਤਾਰ ਕੱਟ ਗਈ (the wire "
              "snapped), ਬਦਲਣਾ ਪਵੇਗਾ (it will have to be replaced). ਪਵੇਗਾ states what has to be "
              "done, which is how a cost is announced before the bill.",
              [V("ਤਾਰ", "tar", "wire", "noun"),
               V("ਕੱਟ ਗਈ", "katt gai", "has snapped", "phrase"),
               V("ਬਦਲਣਾ", "badalna", "to replace", "verb"),
               V("ਪਵੇਗਾ", "pavega", "will have to", "verb"),
               V("ਪੁਰਜ਼ਾ", "purza", "part, spare", "noun")],
              G("What has to be replaced",
                "ਤਾਰ ਕੱਟ ਗਈ ਹੈ · ਪੁਰਜ਼ਾ ਬਦਲਣਾ ਪਵੇਗਾ · ਖ਼ਰਚਾ ਕਿੰਨਾ ਹੋਵੇਗਾ?",
                "ਕੱਟ ਗਈ is the compound that says the wire snapped on its own, and ਬਦਲਣਾ ਪਵੇਗਾ "
                "says a part must be replaced. The estimate is asked with ਖ਼ਰਚਾ ਕਿੰਨਾ ਹੋਵੇਗਾ?, and "
                "the answer comes in rupees.",
                [X("ਤਾਰ ਕੱਟ ਗਈ ਹੈ।", "tar katt gai hai.", "The wire has snapped."),
                 X("ਇੱਕ ਪੁਰਜ਼ਾ ਬਦਲਣਾ ਪਵੇਗਾ।", "ikk purza badalna pavega.", "One part will have to be replaced."),
                 X("ਖ਼ਰਚਾ ਕਿੰਨਾ ਹੋਵੇਗਾ?", "kharcha kinna hovega?", "How much will the cost be?")],
                [("ਪੁਰਜ਼ਾ ਬਦਲਣਾ ਕਰੇਗਾ।", "ਪੁਰਜ਼ਾ ਬਦਲਣਾ ਪਵੇਗਾ।", "Obligation takes ਪਵੇਗਾ, not ਕਰੇਗਾ."),
                 ("ਤਾਰ ਕੱਟ ਹੋਈ।", "ਤਾਰ ਕੱਟ ਗਈ।", "The accident on its own takes ਗਈ.")]),
              [D("ਮਿਸਤਰੀ", "ਕੀ ਹੋਇਆ?", "ki hoia?", "What happened?"),
               D("ਗਾਹਕ", "ਪਤਾ ਨਹੀਂ, ਅਚਾਨਕ ਬੰਦ ਹੋ ਗਿਆ।", "pata nahin, achanak band ho gia.", "I do not know, it suddenly turned off."),
               D("ਮਿਸਤਰੀ", "ਤਾਰ ਕੱਟ ਗਈ ਹੈ। ਇੱਕ ਪੁਰਜ਼ਾ ਬਦਲਣਾ ਪਵੇਗਾ।", "tar katt gai hai. ikk purza badalna pavega.", "The wire has snapped. One part will have to be replaced."),
               D("ਗਾਹਕ", "ਖ਼ਰਚਾ ਕਿੰਨਾ ਹੋਵੇਗਾ?", "kharcha kinna hovega?", "How much will the cost be?")],
              WS("Fault worksheet", [
                  T("Name the fault.", ["the wire has snapped", "one part will have to be replaced"],
                    ["ਤਾਰ ਕੱਟ ਗਈ ਹੈ", "ਇੱਕ ਪੁਰਜ਼ਾ ਬਦਲਣਾ ਪਵੇਗਾ"]),
                  T("Ask the cost.", ["how much will the cost be?", "it suddenly turned off"],
                    ["ਖ਼ਰਚਾ ਕਿੰਨਾ ਹੋਵੇਗਾ?", "ਅਚਾਨਕ ਬੰਦ ਹੋ ਗਿਆ"]),
              ])),
            L("ਬਿੱਲ ਅਤੇ ਗਾਰੰਟੀ",
              "Before paying, three questions protect you: ਬਿੱਲ ਦਿਓ (give the bill), ਗਾਰੰਟੀ ਕਿੰਨੀ "
              "ਹੈ? (how long is the guarantee), ਅਤੇ ਲਿਖ ਕੇ ਦਿਓ (give it in writing). ਲਿਖ ਕੇ ਦੇਣਾ is "
              "how a promise becomes a document.",
              [V("ਬਿੱਲ", "bill", "bill", "noun"),
               V("ਗਾਰੰਟੀ", "garanti", "guarantee, warranty", "noun"),
               V("ਲਿਖ ਕੇ", "likh ke", "in writing", "phrase"),
               V("ਤਾਰੀਖ਼", "tarikh", "date", "noun"),
               V("ਬਦਲਣ ਦੀ ਸ਼ਰਤ", "badlan di sharat", "condition for replacement", "phrase")],
              G("Bill, date and guarantee",
                "ਬਿੱਲ ਦਿਓ · ਗਾਰੰਟੀ ਕਿੰਨੀ ਹੈ? · ਤਾਰੀਖ਼ ਲਿਖ ਦਿਓ",
                "The bill is asked with ਬਿੱਲ ਦਿਓ, the guarantee with ਗਾਰੰਟੀ ਕਿੰਨੀ ਹੈ?, and the "
                "date with ਤਾਰੀਖ਼ ਲਿਖ ਦਿਓ. The condition is stated with ਦੀ ਸ਼ਰਤ: ਬਦਲਣ ਦੀ ਸ਼ਰਤ "
                "ਇਹ ਹੈ ਕਿ ਬਿੱਲ ਹੋਵੇ.",
                [X("ਬਿੱਲ ਦਿਓ, ਤਾਰੀਖ਼ ਵੀ ਲਿਖ ਦਿਓ।", "bill dio, tarikh vi likh dio.", "Give the bill, write the date too."),
                 X("ਗਾਰੰਟੀ ਕਿੰਨੀ ਹੈ?", "garanti kinni hai?", "How long is the guarantee?"),
                 X("ਬਦਲਣ ਦੀ ਸ਼ਰਤ ਇਹ ਹੈ ਕਿ ਬਿੱਲ ਹੋਵੇ।", "badlan di sharat ih hai ki bill hove.", "The condition for replacement is that there be a bill.")],
                [("ਗਾਰੰਟੀ ਕਿੰਨੀ ਹੈ ਹੈ?", "ਗਾਰੰਟੀ ਕਿੰਨੀ ਹੈ?", "One ਹੈ completes the question."),
                 ("ਬਿੱਲ ਦੋ।", "ਬਿੱਲ ਦਿਓ।", "The request is ਦਿਓ.")]),
              [D("ਗਾਹਕ", "ਕੰਮ ਹੋ ਗਿਆ?", "kam ho gia?", "Is the work done?"),
               D("ਮਿਸਤਰੀ", "ਹੋ ਗਿਆ। ਬਿੱਲ ਦੇਖੋ।", "ho gia. bill dekho.", "It is done. Look at the bill."),
               D("ਗਾਹਕ", "ਗਾਰੰਟੀ ਕਿੰਨੀ ਹੈ? ਤਾਰੀਖ਼ ਲਿਖ ਦਿਓ।", "garanti kinni hai? tarikh likh dio.", "How long is the guarantee? Write the date."),
               D("ਮਿਸਤਰੀ", "ਛੇ ਮਹੀਨੇ, ਅਤੇ ਤਾਰੀਖ਼ ਬਿੱਲ ਉੱਤੇ ਲਿਖੀ ਹੈ।", "chhe mahine, ate tarikh bill utte likhi hai.", "Six months, and the date is written on the bill.")],
              WS("Guarantee worksheet", [
                  T("Ask for the paper.", ["give the bill, write the date too", "how long is the guarantee?"],
                    ["ਬਿੱਲ ਦਿਓ, ਤਾਰੀਖ਼ ਵੀ ਲਿਖ ਦਿਓ", "ਗਾਰੰਟੀ ਕਿੰਨੀ ਹੈ?"]),
                  T("State the condition.", ["the condition for replacement is that there be a bill", "the date is written on the bill"],
                    ["ਬਦਲਣ ਦੀ ਸ਼ਰਤ ਇਹ ਹੈ ਕਿ ਬਿੱਲ ਹੋਵੇ", "ਤਾਰੀਖ਼ ਬਿੱਲ ਉੱਤੇ ਲਿਖੀ ਹੈ"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Ludhiana is the most populous city in Punjab — about 1.6 million people at the "
                 "2011 census, packed into some 310 square kilometres, which makes it the state's "
                 "most densely populated urban centre. Industry is what the city is known for: "
                 "hosiery, bicycles, machine parts, and a trade that pulls workers in from "
                 "districts all around. The BBC once called it India's Manchester, and the "
                 "nickname stuck. For a learner the city is a good market for practice: a bus "
                 "stand, a wholesale bazaar and a repair lane, all within a few kilometres."),
        source_url="https://en.wikipedia.org/wiki/Ludhiana",
        reading=("ਲੁਧਿਆਣੇ ਵਿੱਚ ਸਵੇਰ ਸੱਤ ਵਜੇ ਬਾਜ਼ਾਰ ਖੁੱਲ੍ਹਦਾ ਹੈ। ਅਸੀਂ ਪਹਿਲਾਂ ਬੱਸ ਅੱਡੇ ਗਏ: ਦੋ ਟਿਕਟਾਂ "
                 "ਅੰਮ੍ਰਿਤਸਰ ਤੱਕ ਲਈਆਂ, ਪਰ ਬੱਸ ਵਿੱਚ ਅੱਧਾ ਘੰਟਾ ਦੇਰੀ ਸੀ, ਇਸ ਲਈ ਅਸੀਂ ਉੱਥੇ ਉਡੀਕ ਕੀਤੀ। ਫਿਰ "
                 "ਅਸੀਂ ਸਿੱਧਾ ਬਾਜ਼ਾਰ ਗਏ ਅਤੇ ਪਹਿਲੇ ਮੋੜ ਤੋਂ ਸੱਜੇ ਮੁੜੇ। ਦੁਕਾਨ ਉੱਤੇ ਇੱਕ ਕਿੱਲੋ ਟਮਾਟਰ ਲਏ "
                 "ਅਤੇ ਰਸੀਦ ਲਈ। ਸ਼ਾਮ ਨੂੰ ਮਿਸਤਰੀ ਨੂੰ ਫ਼ੋਨ ਕੀਤਾ: ਪੱਖਾ ਖ਼ਰਾਬ ਹੋ ਗਿਆ ਸੀ, ਤਾਰ ਕੱਟ ਗਈ ਸੀ, "
                 "ਅਤੇ ਇੱਕ ਪੁਰਜ਼ਾ ਬਦਲਣਾ ਪਿਆ। ਬਿੱਲ ਉੱਤੇ ਤਾਰੀਖ਼ ਅਤੇ ਛੇ ਮਹੀਨੇ ਦੀ ਗਾਰੰਟੀ ਲਿਖੀ ਹੋਈ ਹੈ।"),
        reading_gloss=("In Ludhiana the bazaar opens at seven in the morning. We went first to the "
                       "bus stand: we took two tickets to Amritsar, but the bus was delayed by "
                       "half an hour, so we waited there. Then we went straight to the market and "
                       "turned right at the first turn. At the shop we took a kilogram of "
                       "tomatoes and asked for a receipt. In the evening we phoned the mechanic: "
                       "the fan had gone out of order, the wire had snapped, and one part had to "
                       "be replaced. On the bill the date and a six-month guarantee are written."),
        listening=("ਗਾਹਕ: ਹੈਲੋ, ਮਿਸਤਰੀ ਜੀ? ਪੱਖਾ ਖ਼ਰਾਬ ਹੋ ਗਿਆ ਹੈ। ਮਿਸਤਰੀ: ਕੀ ਹੋਇਆ? ਗਾਹਕ: ਅਚਾਨਕ ਬੰਦ "
                   "ਹੋ ਗਿਆ। ਮਿਸਤਰੀ: ਤਾਰ ਕੱਟ ਗਈ ਹੋਵੇਗੀ। ਪਤਾ ਦੱਸੋ। ਗਾਹਕ: ਗਲੀ ਨੰਬਰ ਚਾਰ। ਮਿਸਤਰੀ: ਠੀਕ "
                   "ਹੈ, ਸ਼ਾਮ ਨੂੰ ਆਉਂਦਾ ਹਾਂ। ਬਿੱਲ ਅਤੇ ਤਾਰੀਖ਼ ਦੇਵਾਂਗਾ।"),
        listening_gloss=("Customer: Hello, mechanic? The fan has gone out of order. Mechanic: What "
                         "happened? Customer: It suddenly turned off. Mechanic: The wire must have "
                         "snapped. Tell me the address. Customer: Lane number four. Mechanic: All "
                         "right, I will come in the evening. I will give the bill and the date."),
        voice_tag=VOICE,
        idioms=[
            ("ਟਾਈਮ ਬਦਲ ਗਿਆ", "the time has changed", "the schedule has moved"),
            ("ਚੱਕਰ ਲਾਉਣਾ", "to make circles", "to go round and round looking for something"),
            ("ਰਸੀਦ ਦੇ ਦਿਓ", "give the receipt", "make it official, keep a record"),
            ("ਘੱਟ ਤੋਲੇ", "short in the weighing", "cheated on the weight of a purchase"),
            ("ਹੁਣੇ ਆਉਂਦਾ ਹਾਂ", "I am coming just now", "I will be there in a moment"),
            ("ਕੰਮ ਹੋ ਗਿਆ", "the work is done", "the job is finished"),
            ("ਪਤਾ ਦੱਸੋ", "tell the address", "give me the details, where to come"),
            ("ਲਿਖ ਕੇ ਦਿਓ", "give it in writing", "put the promise on paper"),
            ("ਮਿਲਾ ਲਵਾਂ", "let me match it up", "let me check the total"),
            ("ਦੁਬਾਰਾ ਤੋਲੋ", "weigh it again", "I want a second weighing"),
        ],
        mistakes=[
            ("ਬੱਸ ਕਿੰਨੇ ਵਜੇ ਚੱਲਦਾ ਹੈ?", "ਬੱਸ ਕਿੰਨੇ ਵਜੇ ਚੱਲਦੀ ਹੈ?", "ਬੱਸ is feminine."),
            ("ਮੈਨੂੰ ਫਾਰਮ ਭਰਦਾ ਹੈ।", "ਮੈਨੂੰ ਫਾਰਮ ਭਰਨਾ ਹੈ।", "The obligation is ਭਰਨਾ ਹੈ."),
            ("ਸਿੱਧਾ ਜਾਂਦੇ ਹੋ, ਫਿਰ ਸੱਜੇ।", "ਸਿੱਧਾ ਜਾਓ, ਫਿਰ ਸੱਜੇ।", "A direction takes ਜਾਓ."),
        ],
        task_title="Run three errands in Punjabi, on paper",
        task_instructions=("Write a Punjabi exchange of ten to twelve turns for three errands: "
                           "buy two tickets and ask the departure time, ask the way and repeat it "
                           "back to check, and report a fault to a mechanic. Use ਦੇਰੀ ਹੈ, ਰਸੀਦ ਦੇ "
                           "ਦਿਓ, ਪੁਰਜ਼ਾ ਬਦਲਣਾ ਪਵੇਗਾ and ਗਾਰੰਟੀ ਕਿੰਨੀ ਹੈ?, and finish with ਲਿਖ ਕੇ "
                           "ਦਿਓ."),
    ),
    "test": [
        ("translate_en", "Say: I have to go to Ludhiana.", "ਮੈਨੂੰ ਲੁਧਿਆਣਾ ਜਾਣਾ ਹੈ।"),
        ("translate_pa", "ਇਹ ਤੋਲ ਘੱਟ ਹੈ।", "This weight is short."),
        ("multiple_choice", "Which sentence asks the departure time of the bus?", "ਬੱਸ ਕਿੰਨੇ ਵਜੇ ਚੱਲਦੀ ਹੈ?"),
        ("fill_in_the_blank", "ਮੈਨੂੰ ਇਹ ਫਾਰਮ ___ ਹੈ।", "ਭਰਨਾ"),
        ("word_selection", "Select the Punjabi for 'receipt'.", "ਰਸੀਦ"),
        ("error_correction", "ਪੁਰਜ਼ਾ ਬਦਲਣਾ ਕਰੇਗਾ।", "ਪੁਰਜ਼ਾ ਬਦਲਣਾ ਪਵੇਗਾ।"),
        ("dialogue_completion", "Complete: ਖ਼ਰਚਾ ਕਿੰਨਾ ___? (How much will the cost be?)", "ਹੋਵੇਗਾ"),
        ("matching", "Match ਪਛਾਣ ਪੱਤਰ to its meaning.", "identity document"),
        ("reading_comprehension", "ਬਾਜ਼ਾਰ ਕਦੋਂ ਖੁੱਲ੍ਹਦਾ ਹੈ?", "at seven in the morning"),
        ("inference", "ਅਸੀਂ ਰਸੀਦ ਲਈ। — why does this matter later?", "it is the proof of purchase for the guarantee"),
        ("main_idea", "ਇੱਕ ਸਵੇਰ ਵਿੱਚ ਅੱਡਾ, ਬਾਜ਼ਾਰ ਅਤੇ ਮਿਸਤਰੀ। — what is this sentence?", "the order of the day's errands"),
        ("detail_identification", "ਗਾਰੰਟੀ ਕਿੰਨੇ ਮਹੀਨੇ ਦੀ ਹੈ?", "six months"),
    ],
}

HALFSTEPS["B1+"] = {
    "native": NATIVE,
    "title": "%s B1+ — A community programme and the report" % NAME,
    "goals": [
        "Divide work for a programme and fix who does what by when",
        "Invite people, hear a complaint without heat, and ask for help clearly",
        "Write a short report: what was decided, who answered for it, and what it produced",
    ],
    "units": [
        {"id": "B1+-U1", "title": "ਪ੍ਰੋਗਰਾਮ ਦੀ ਤਿਆਰੀ", "lessons": [
            L("ਕੰਮ ਵੰਡਣਾ",
              "Dividing work uses the ergative ਨੇ when the verb is transitive and past: ਅਸੀਂ ਕੰਮ "
              "ਵੰਡਿਆ, ਮੈਂ ਸੂਚੀ ਬਣਾਈ. The future promise takes -ਾਂਗੇ: ਅਸੀਂ ਸੰਭਾਲਾਂਗੇ. ਜ਼ਿੰਮੇਵਾਰੀ "
              "names the responsibility and ਮੁਕੰਮਲ ਹੋਣਾ says the task is complete.",
              [V("ਵੰਡਣਾ", "vandna", "to divide, to share out", "verb"),
               V("ਜ਼ਿੰਮੇਵਾਰੀ", "zimmevari", "responsibility", "noun"),
               V("ਸੂਚੀ", "suchi", "list", "noun"),
               V("ਮੁਕੰਮਲ", "mukammal", "complete", "adjective"),
               V("ਅੰਦਾਜ਼ਾ", "andaza", "estimate", "noun")],
              G("Who takes what",
                "ਅਸੀਂ ਕੰਮ ਵੰਡਿਆ · ਮੈਂ ਜ਼ਿੰਮੇਵਾਰੀ ਲਈ · ਅਸੀਂ ਸੰਭਾਲਾਂਗੇ",
                "In the past tense a transitive verb takes ਨੇ with its subject: ਮੈਂ ਸੂਚੀ ਬਣਾਈ, "
                "ਅਸੀਂ ਕੰਮ ਵੰਡਿਆ — the verb then agrees with the object. The future keeps the "
                "plain subject: ਮੈਂ ਸੰਭਾਲਾਂਗਾ, ਅਸੀਂ ਸੰਭਾਲਾਂਗੇ.",
                [X("ਅਸੀਂ ਪ੍ਰੋਗਰਾਮ ਦਾ ਕੰਮ ਵੰਡਿਆ।", "asin program da kam vandia.", "We divided the work of the programme."),
                 X("ਮੈਂ ਸੂਚੀ ਬਣਾਈ ਅਤੇ ਜ਼ਿੰਮੇਵਾਰੀ ਲਈ।", "main suchi banai ate zimmevari lai.", "I made the list and took the responsibility."),
                 X("ਅਸੀਂ ਸਟੇਜ ਸੰਭਾਲਾਂਗੇ।", "asin stage sambhalange.", "We will look after the stage.")],
                [("ਮੈਂ ਸੂਚੀ ਬਣਾਇਆ।", "ਮੈਂ ਸੂਚੀ ਬਣਾਈ।", "ਸੂਚੀ is feminine: ਬਣਾਈ."),
                 ("ਮੈਂ ਨੇ ਕੰਮ ਵੰਡਿਆ।", "ਮੈਂ ਕੰਮ ਵੰਡਿਆ।", "ਮੈਂ does not take ਨੇ; only third-person subjects do.")]),
              [D("ਪ੍ਰਧਾਨ", "ਪ੍ਰੋਗਰਾਮ ਦਾ ਕੰਮ ਕਿਵੇਂ ਵੰਡੀਏ?", "program da kam kiven vandie?", "How shall we divide the programme work?"),
               D("ਸਕੱਤਰ", "ਅਸੀਂ ਕੰਮ ਤਿੰਨ ਹਿੱਸਿਆਂ ਵਿੱਚ ਵੰਡਿਆ।", "asin kam tinn hissian vich vandia.", "We divided the work into three parts."),
               D("ਪ੍ਰਧਾਨ", "ਸਟੇਜ ਦੀ ਜ਼ਿੰਮੇਵਾਰੀ ਕਿਸ ਨੇ ਲਈ?", "stage di zimmevari kis ne lai?", "Who took the responsibility for the stage?"),
               D("ਸਕੱਤਰ", "ਰਾਜ ਨੇ ਲਈ। ਬਾਕੀ ਦੋ ਹਿੱਸੇ ਅਸੀਂ ਸੰਭਾਲਾਂਗੇ।", "raj ne lai. baki do hisse asin sambhalange.", "Raj took it. We will manage the other two parts.")],
              WS("Dividing work worksheet", [
                  T("Report the past.", ["we divided the work into three parts", "I made the list"],
                    ["ਅਸੀਂ ਕੰਮ ਤਿੰਨ ਹਿੱਸਿਆਂ ਵਿੱਚ ਵੰਡਿਆ", "ਮੈਂ ਸੂਚੀ ਬਣਾਈ"]),
                  T("Promise the future.", ["we will look after the stage", "who took the responsibility?"],
                    ["ਅਸੀਂ ਸਟੇਜ ਸੰਭਾਲਾਂਗੇ", "ਜ਼ਿੰਮੇਵਾਰੀ ਕਿਸ ਨੇ ਲਈ?"]),
              ])),
            L("ਫ਼ੈਸਲਾ ਕਰਨਾ",
              "A decision in a meeting is reported in the impersonal: ਫ਼ੈਸਲਾ ਹੋਇਆ ਕਿ … (it was "
              "decided that), ਅਤੇ ਇਹ ਤੈਅ ਹੋਇਆ ਕਿ … . The people who decided stay in the "
              "background, which is what makes a decision sound settled.",
              [V("ਫ਼ੈਸਲਾ", "faisla", "decision", "noun"),
               V("ਤੈਅ", "tai", "fixed, settled", "adjective"),
               V("ਪਾਸ", "pass", "passed (a proposal)", "adjective"),
               V("ਬਹੁਮਤ", "bahumat", "majority", "noun"),
               V("ਪ੍ਰਸਤਾਵ", "prastav", "proposal", "noun")],
              G("Reporting a decision",
                "ਫ਼ੈਸਲਾ ਹੋਇਆ ਕਿ · ਤੈਅ ਹੋਇਆ ਕਿ · ਬਹੁਮਤ ਨਾਲ ਪਾਸ",
                "The impersonal ਹੋਇਆ removes the person: ਫ਼ੈਸਲਾ ਹੋਇਆ ਕਿ ਸਮਾਂ ਬਦਲਿਆ ਜਾਵੇ. ਤੈਅ ਹੋਇਆ "
                "says the matter is settled, and ਬਹੁਮਤ ਨਾਲ ਪਾਸ says how the vote went. The clause "
                "after ਕਿ takes the subjunctive ਜਾਵੇ.",
                [X("ਫ਼ੈਸਲਾ ਹੋਇਆ ਕਿ ਸਮਾਂ ਬਦਲਿਆ ਜਾਵੇ।", "faisla hoia ki saman badalia jave.", "It was decided that the time be changed."),
                 X("ਇਹ ਤੈਅ ਹੋਇਆ ਕਿ ਪ੍ਰਸਤਾਵ ਬਹੁਮਤ ਨਾਲ ਪਾਸ ਹੋਵੇ।", "ih tai hoia ki prastav bahumat nal pass hove.", "It was settled that the proposal pass by majority."),
                 X("ਦੋ ਸੁਝਾਅ ਆਏ, ਪਰ ਇੱਕ ਪਾਸ ਹੋਇਆ।", "do sujhaa aae, par ikk pass hoia.", "Two suggestions came, but one passed.")],
                [("ਫ਼ੈਸਲਾ ਕੀਤਾ ਕਿ ਜਾਵੇ।", "ਫ਼ੈਸਲਾ ਹੋਇਆ ਕਿ ਜਾਵੇ।", "A decision is reported as ਹੋਇਆ."),
                 ("ਤੈਅ ਹੋਇਆ ਕਿ ਸਮਾਂ ਬਦਲਿਆ ਜਾਵੇਗਾ।", "ਤੈਅ ਹੋਇਆ ਕਿ ਸਮਾਂ ਬਦਲਿਆ ਜਾਵੇ।", "After ਕਿ the verb is subjunctive: ਜਾਵੇ.")]),
              [D("ਸਕੱਤਰ", "ਮੀਟਿੰਗ ਵਿੱਚ ਕੀ ਤੈਅ ਹੋਇਆ?", "meeting vich ki tai hoia?", "What was settled in the meeting?"),
               D("ਪ੍ਰਧਾਨ", "ਤੈਅ ਹੋਇਆ ਕਿ ਪ੍ਰੋਗਰਾਮ ਅਗਲੇ ਹਫ਼ਤੇ ਹੋਵੇ।", "tai hoia ki program agle hafte hove.", "It was settled that the programme be next week."),
               D("ਸਕੱਤਰ", "ਅਤੇ ਪ੍ਰਸਤਾਵ?", "ate prastav?", "And the proposal?"),
               D("ਪ੍ਰਧਾਨ", "ਬਹੁਮਤ ਨਾਲ ਪਾਸ ਹੋਇਆ। ਫ਼ੈਸਲਾ ਲਿਖ ਲਓ।", "bahumat nal pass hoia. faisla likh lo.", "It passed by majority. Write the decision down.")],
              WS("Decision worksheet", [
                  T("Report the decision.", ["it was decided that the time be changed", "it was settled that the programme be next week"],
                    ["ਫ਼ੈਸਲਾ ਹੋਇਆ ਕਿ ਸਮਾਂ ਬਦਲਿਆ ਜਾਵੇ", "ਤੈਅ ਹੋਇਆ ਕਿ ਪ੍ਰੋਗਰਾਮ ਅਗਲੇ ਹਫ਼ਤੇ ਹੋਵੇ"]),
                  T("Say how it went.", ["it passed by majority", "two suggestions came"],
                    ["ਬਹੁਮਤ ਨਾਲ ਪਾਸ ਹੋਇਆ", "ਦੋ ਸੁਝਾਅ ਆਏ"]),
              ])),
            L("ਸਮਾਂ ਪੱਕਾ ਕਰਨਾ",
              "Fixing a time means agreeing on a date, an hour and a place: ਤਾਰੀਖ਼ ਪੱਕੀ ਕਰਨੀ ਹੈ, "
              "ਸ਼ਾਮ ਪੰਜ ਵਜੇ, ਗੁਰਦੁਆਰੇ ਵਾਲੇ ਹਾਲ ਵਿੱਚ. The infinitive with ਹੈ states what still has "
              "to be done, and ਪੱਕਾ ਹੋ ਗਿਆ says it is settled.",
              [V("ਤਾਰੀਖ਼", "tarikh", "date", "noun"),
               V("ਪੱਕਾ", "pakka", "firm, fixed", "adjective"),
               V("ਹਾਲ", "hal", "hall", "noun"),
               V("ਵਜੇ", "vaje", "o'clock", "phrase"),
               V("ਤਿਆਰੀ", "taiari", "preparation", "noun")],
              G("Fixing date, hour and place",
                "ਤਾਰੀਖ਼ ਪੱਕੀ ਕਰਨੀ ਹੈ · ਸ਼ਾਮ ਪੰਜ ਵਜੇ · ਹਾਲ ਵਿੱਚ",
                "The thing still to be done takes the infinitive with ਹੈ: ਤਾਰੀਖ਼ ਪੱਕੀ ਕਰਨੀ ਹੈ "
                "(the date has to be fixed). The hour takes ਵਜੇ, the place takes ਵਿੱਚ, and "
                "ਪੱਕਾ ਹੋ ਗਿਆ closes the matter.",
                [X("ਅਸੀਂ ਤਾਰੀਖ਼ ਪੱਕੀ ਕਰਨੀ ਹੈ।", "asin tarikh pakki karni hai.", "We have to fix the date."),
                 X("ਸ਼ਾਮ ਪੰਜ ਵਜੇ, ਗੁਰਦੁਆਰੇ ਵਾਲੇ ਹਾਲ ਵਿੱਚ।", "sham panj vaje, gurduare vale hal vich.", "At five in the evening, in the hall at the gurdwara."),
                 X("ਸਮਾਂ ਪੱਕਾ ਹੋ ਗਿਆ ਹੈ।", "saman pakka ho gia hai.", "The time has been fixed.")],
                [("ਤਾਰੀਖ਼ ਪੱਕਾ ਕਰਨਾ ਹੈ।", "ਤਾਰੀਖ਼ ਪੱਕੀ ਕਰਨੀ ਹੈ।", "ਤਾਰੀਖ਼ is feminine: ਪੱਕੀ ਕਰਨੀ ਹੈ."),
                 ("ਸ਼ਾਮ ਪੰਜ ਵਜ।", "ਸ਼ਾਮ ਪੰਜ ਵਜੇ।", "The hour takes ਵਜੇ.")]),
              [D("ਪ੍ਰਧਾਨ", "ਤਾਰੀਖ਼ ਪੱਕੀ ਹੋ ਗਈ?", "tarikh pakki ho gai?", "Is the date fixed?"),
               D("ਸਕੱਤਰ", "ਹਾਂ, ਅਗਲੇ ਸ਼ਨੀਵਾਰ, ਸ਼ਾਮ ਪੰਜ ਵਜੇ।", "han, agle shanivar, sham panj vaje.", "Yes, next Saturday, at five in the evening."),
               D("ਪ੍ਰਧਾਨ", "ਥਾਂ?", "thaan?", "The place?"),
               D("ਸਕੱਤਰ", "ਗੁਰਦੁਆਰੇ ਵਾਲਾ ਹਾਲ। ਤਿਆਰੀ ਸ਼ੁੱਕਰਵਾਰ ਸ਼ਾਮ ਤੋਂ ਸ਼ੁਰੂ ਕਰਾਂਗੇ।", "gurduare vala hal. taiari shukarvar sham ton shuru karange.", "The hall at the gurdwara. We will start the preparation from Friday evening.")],
              WS("Fixing the time worksheet", [
                  T("State what is needed.", ["we have to fix the date", "the time has been fixed"],
                    ["ਅਸੀਂ ਤਾਰੀਖ਼ ਪੱਕੀ ਕਰਨੀ ਹੈ", "ਸਮਾਂ ਪੱਕਾ ਹੋ ਗਿਆ ਹੈ"]),
                  T("Give place and hour.", ["at five in the evening, in the hall", "next Saturday"],
                    ["ਸ਼ਾਮ ਪੰਜ ਵਜੇ, ਹਾਲ ਵਿੱਚ", "ਅਗਲਾ ਸ਼ਨੀਵਾਰ"]),
              ])),
        ]},
        {"id": "B1+-U2", "title": "ਲੋਕਾਂ ਨਾਲ ਗੱਲ", "lessons": [
            L("ਸੱਦਾ ਦੇਣਾ",
              "An invitation is given with ਸੱਦਾ ਦੇਣਾ, and the guest is told the date, the hour and "
              "the reason: ਸੱਦਾ ਦੇ ਰਹੇ ਹਾਂ, ਸ਼ਨੀਵਾਰ ਸ਼ਾਮ, ਪ੍ਰੋਗਰਾਮ ਵਿੱਚ. ਜ਼ਰੂਰ ਆਉਣਾ (do come) "
              "closes it, and the guest answers ਹਾਂ, ਜ਼ਰੂਰ or ਕੋਸ਼ਿਸ਼ ਕਰਾਂਗੇ.",
              [V("ਸੱਦਾ", "sadda", "invitation", "noun"),
               V("ਜ਼ਰੂਰ", "zarur", "certainly", "adverb"),
               V("ਮੌਕਾ", "mauka", "occasion, chance", "noun"),
               V("ਕੋਸ਼ਿਸ਼", "koshish", "effort, attempt", "noun"),
               V("ਸ਼ਨੀਵਾਰ", "shanivar", "Saturday", "noun")],
              G("Giving and answering an invitation",
                "ਸੱਦਾ ਦੇ ਰਹੇ ਹਾਂ · ਜ਼ਰੂਰ ਆਉਣਾ · ਕੋਸ਼ਿਸ਼ ਕਰਾਂਗੇ",
                "The invitation is in the progressive: ਸੱਦਾ ਦੇ ਰਹੇ ਹਾਂ. ਜ਼ਰੂਰ ਆਉਣਾ puts a soft "
                "obligation on the guest, and the polite answer is ਜ਼ਰੂਰ ਆਵਾਂਗੇ or ਕੋਸ਼ਿਸ਼ ਕਰਾਂਗੇ. "
                "An excuse is given with ਕੰਮ ਕਾਰਨ (because of work).",
                [X("ਅਸੀਂ ਤੁਹਾਨੂੰ ਸੱਦਾ ਦੇ ਰਹੇ ਹਾਂ।", "asin tuhanun sadda de rahe han.", "We are giving you an invitation."),
                 X("ਸ਼ਨੀਵਾਰ ਸ਼ਾਮ ਪੰਜ ਵਜੇ, ਜ਼ਰੂਰ ਆਉਣਾ।", "shanivar sham panj vaje, zarur auna.", "Saturday evening at five, do come."),
                 X("ਸ਼ੁਕਰੀਆ, ਅਸੀਂ ਕੋਸ਼ਿਸ਼ ਕਰਾਂਗੇ।", "shukria, asin koshish karange.", "Thank you, we will try.")],
                [("ਤੁਹਾਨੂੰ ਸੱਦਾ ਦਿੱਤਾ ਜਾ ਰਿਹਾ।", "ਤੁਹਾਨੂੰ ਸੱਦਾ ਦੇ ਰਹੇ ਹਾਂ।", "ਅਸੀਂ speaks as ਦੇ ਰਹੇ ਹਾਂ."),
                 ("ਜ਼ਰੂਰ ਆਉਣਾ ਹੈ।", "ਜ਼ਰੂਰ ਆਉਣਾ।", "The warm invitation is ਜ਼ਰੂਰ ਆਉਣਾ, without ਹੈ.")]),
              [D("ਸਕੱਤਰ", "ਅਸੀਂ ਤੁਹਾਨੂੰ ਸੱਦਾ ਦੇ ਰਹੇ ਹਾਂ।", "asin tuhanun sadda de rahe han.", "We are giving you an invitation."),
               D("ਪਿੰਡ ਵਾਲਾ", "ਕਦੋਂ ਹੈ ਮੌਕਾ?", "kadon hai mauka?", "When is the occasion?"),
               D("ਸਕੱਤਰ", "ਸ਼ਨੀਵਾਰ ਸ਼ਾਮ ਪੰਜ ਵਜੇ, ਗੁਰਦੁਆਰੇ ਵਾਲੇ ਹਾਲ ਵਿੱਚ।", "shanivar sham panj vaje, gurduare vale hal vich.", "Saturday evening at five, in the hall at the gurdwara."),
               D("ਪਿੰਡ ਵਾਲਾ", "ਜ਼ਰੂਰ ਆਵਾਂਗੇ। ਸੱਦੇ ਲਈ ਸ਼ੁਕਰੀਆ।", "zarur avange. sadde lai shukria.", "We will certainly come. Thank you for the invitation.")],
              WS("Invitation worksheet", [
                  T("Invite.", ["we are giving you an invitation", "Saturday evening at five, do come"],
                    ["ਅਸੀਂ ਤੁਹਾਨੂੰ ਸੱਦਾ ਦੇ ਰਹੇ ਹਾਂ", "ਸ਼ਨੀਵਾਰ ਸ਼ਾਮ ਪੰਜ ਵਜੇ, ਜ਼ਰੂਰ ਆਉਣਾ"]),
                  T("Answer.", ["we will certainly come", "we will try"],
                    ["ਜ਼ਰੂਰ ਆਵਾਂਗੇ", "ਅਸੀਂ ਕੋਸ਼ਿਸ਼ ਕਰਾਂਗੇ"]),
              ])),
            L("ਸ਼ਿਕਾਇਤ ਸੁਣਨਾ",
              "Listening to a complaint means letting it finish and then answering the point, not "
              "the tone: ਗੱਲ ਸਮਝ ਗਏ, ਅਸੀਂ ਵੇਖਦੇ ਹਾਂ. ਨਾਰਾਜ਼ਗੀ (displeasure) is named without "
              "blame, ਅਤੇ ਜੇ ਲੋੜ ਪਵੇ (if needed) leaves room for a second step.",
              [V("ਸ਼ਿਕਾਇਤ", "shikait", "complaint", "noun"),
               V("ਨਾਰਾਜ਼ਗੀ", "narazgi", "displeasure", "noun"),
               V("ਲੋੜ", "lor", "need", "noun"),
               V("ਵੇਖਣਾ", "vekhna", "to look into", "verb"),
               V("ਜਵਾਬ", "javab", "answer", "noun")],
              G("Hearing a complaint",
                "ਤੁਹਾਡੀ ਨਾਰਾਜ਼ਗੀ ਠੀਕ ਹੈ · ਅਸੀਂ ਵੇਖਦੇ ਹਾਂ · ਜੇ ਲੋੜ ਪਵੇ",
                "The listener first accepts the feeling: ਨਾਰਾਜ਼ਗੀ ਠੀਕ ਹੈ. Then the answer is "
                "promised in the present: ਅਸੀਂ ਵੇਖਦੇ ਹਾਂ, ਜਵਾਬ ਦਿੰਦੇ ਹਾਂ. The condition ਜੇ ਲੋੜ ਪਵੇ "
                "takes the subjunctive ਪਵੇ and keeps the promise honest.",
                [X("ਤੁਹਾਡੀ ਨਾਰਾਜ਼ਗੀ ਠੀਕ ਹੈ।", "tuhadi narazgi thik hai.", "Your displeasure is justified."),
                 X("ਅਸੀਂ ਗੱਲ ਵੇਖਦੇ ਹਾਂ ਅਤੇ ਜਵਾਬ ਦਿੰਦੇ ਹਾਂ।", "asin gal vekhde han ate javab dinde han.", "We will look into the matter and answer."),
                 X("ਜੇ ਲੋੜ ਪਵੇ ਤਾਂ ਮੀਟਿੰਗ ਸੱਦਾਂਗੇ।", "je lor pave tan meeting saddange.", "If needed we will call a meeting.")],
                [("ਤੁਹਾਡੀ ਨਾਰਾਜ਼ਗੀ ਠੀਕ ਹੋ।", "ਤੁਹਾਡੀ ਨਾਰਾਜ਼ਗੀ ਠੀਕ ਹੈ।", "The statement takes ਹੈ."),
                 ("ਜੇ ਲੋੜ ਪਵੇਗੀ ਤਾਂ ਮੀਟਿੰਗ ਸੱਦਾਂਗੇ।", "ਜੇ ਲੋੜ ਪਵੇ ਤਾਂ ਮੀਟਿੰਗ ਸੱਦਾਂਗੇ।", "After ਜੇ the verb is subjunctive: ਪਵੇ.")]),
              [D("ਔਰਤ", "ਪਾਣੀ ਦਾ ਕੰਮ ਤਿੰਨ ਹਫ਼ਤੇ ਤੋਂ ਰੁਕਿਆ ਹੋਇਆ ਹੈ।", "pani da kam tinn hafte ton rukia hoia hai.", "The water work has been stopped for three weeks."),
               D("ਸਕੱਤਰ", "ਤੁਹਾਡੀ ਨਾਰਾਜ਼ਗੀ ਠੀਕ ਹੈ।", "tuhadi narazgi thik hai.", "Your displeasure is justified."),
               D("ਔਰਤ", "ਫਿਰ ਕਦੋਂ ਸ਼ੁਰੂ ਹੋਵੇਗਾ?", "phir kadon shuru hovega?", "Then when will it start?"),
               D("ਸਕੱਤਰ", "ਅਸੀਂ ਵੇਖਦੇ ਹਾਂ ਅਤੇ ਜਵਾਬ ਦਿੰਦੇ ਹਾਂ। ਜੇ ਲੋੜ ਪਵੇ ਤਾਂ ਮੀਟਿੰਗ ਸੱਦਾਂਗੇ।", "asin vekhde han ate javab dinde han. je lor pave tan meeting saddange.", "We will look into it and answer. If needed we will call a meeting.")],
              WS("Complaint worksheet", [
                  T("Accept the feeling.", ["your displeasure is justified", "we will look into the matter and answer"],
                    ["ਤੁਹਾਡੀ ਨਾਰਾਜ਼ਗੀ ਠੀਕ ਹੈ", "ਅਸੀਂ ਗੱਲ ਵੇਖਦੇ ਹਾਂ ਅਤੇ ਜਵਾਬ ਦਿੰਦੇ ਹਾਂ"]),
                  T("Leave room.", ["if needed we will call a meeting", "when will it start?"],
                    ["ਜੇ ਲੋੜ ਪਵੇ ਤਾਂ ਮੀਟਿੰਗ ਸੱਦਾਂਗੇ", "ਕਦੋਂ ਸ਼ੁਰੂ ਹੋਵੇਗਾ?"]),
              ])),
            L("ਮਦਦ ਮੰਗਣਾ",
              "Asking for help is direct in Punjabi: ਮਦਦ ਕਰ ਦਿਓ (please help), ਥੋੜ੍ਹਾ ਹੱਥ ਵਟਾਓ "
              "(lend a hand), ਸਮਾਂ ਮਿਲੇ ਤਾਂ ਆ ਜਾਓ. The conditional ਸਮਾਂ ਮਿਲੇ ਤਾਂ keeps the request "
              "polite, and ਸ਼ੁਕਰੀਆ closes it.",
              [V("ਮਦਦ", "madad", "help", "noun"),
               V("ਹੱਥ ਵਟਾਉਣਾ", "hatth vatauna", "to lend a hand", "phrase"),
               V("ਸਮਾਂ", "saman", "time", "noun"),
               V("ਮਿਲੇ", "mile", "if (it) is available", "verb"),
               V("ਸ਼ੁਕਰੀਆ", "shukria", "thank you", "noun")],
              G("Asking for help",
                "ਮਦਦ ਕਰ ਦਿਓ · ਥੋੜ੍ਹਾ ਹੱਥ ਵਟਾਓ · ਸਮਾਂ ਮਿਲੇ ਤਾਂ ਆ ਜਾਓ",
                "ਕਰ ਦਿਓ asks for help now, ਹੱਥ ਵਟਾਓ for a hand with physical work, and ਸਮਾਂ ਮਿਲੇ "
                "ਤਾਂ ਆ ਜਾਓ makes the request conditional so the other person can refuse lightly. "
                "The answer ਹੁਣੇ ਆਇਆ ਜਾਂਦਾ ਹੈ promises quick help.",
                [X("ਭਾਈ, ਥੋੜ੍ਹੀ ਮਦਦ ਕਰ ਦਿਓ।", "bhai, thorhi madad kar dio.", "Brother, please help a little."),
                 X("ਸਟੇਜ ਲਗਾਉਣ ਵਿੱਚ ਹੱਥ ਵਟਾਓ।", "stage laaun vich hatth vatao.", "Lend a hand in setting up the stage."),
                 X("ਸਮਾਂ ਮਿਲੇ ਤਾਂ ਸ਼ਾਮ ਨੂੰ ਆ ਜਾਓ।", "saman mile tan sham nun a jao.", "If you have time, come in the evening.")],
                [("ਮਦਦ ਕਰੋ ਦਿਓ।", "ਮਦਦ ਕਰ ਦਿਓ।", "The request is ਕਰ ਦਿਓ."),
                 ("ਸਮਾਂ ਮਿਲੇਗਾ ਤਾਂ ਆ ਜਾਓ।", "ਸਮਾਂ ਮਿਲੇ ਤਾਂ ਆ ਜਾਓ।", "The condition takes the subjunctive ਮਿਲੇ.")]),
              [D("ਸਕੱਤਰ", "ਰਾਜ ਭਾਈ, ਥੋੜ੍ਹੀ ਮਦਦ ਕਰ ਦਿਓ।", "raj bhai, thorhi madad kar dio.", "Raj, please help a little."),
               D("ਰਾਜ", "ਦੱਸੋ, ਕੀ ਕਰਨਾ ਹੈ?", "dasso, ki karna hai?", "Tell me, what has to be done?"),
               D("ਸਕੱਤਰ", "ਸਟੇਜ ਲਗਾਉਣ ਵਿੱਚ ਹੱਥ ਵਟਾਓ।", "stage laaun vich hatth vatao.", "Lend a hand in setting up the stage."),
               D("ਰਾਜ", "ਠੀਕ ਹੈ, ਹੁਣੇ ਆਇਆ ਜਾਂਦਾ ਹੈ। ਸ਼ੁਕਰੀਆ ਕਹਿਣ ਦੀ ਲੋੜ ਨਹੀਂ।", "thik hai, hune aia janda hai. shukria kahin di lor nahin.", "All right, I am coming just now. No need to say thanks.")],
              WS("Help worksheet", [
                  T("Ask for help.", ["please help a little", "if you have time, come in the evening"],
                    ["ਥੋੜ੍ਹੀ ਮਦਦ ਕਰ ਦਿਓ", "ਸਮਾਂ ਮਿਲੇ ਤਾਂ ਸ਼ਾਮ ਨੂੰ ਆ ਜਾਓ"]),
                  T("Answer the request.", ["tell me, what has to be done?", "lend a hand in setting up the stage"],
                    ["ਦੱਸੋ, ਕੀ ਕਰਨਾ ਹੈ?", "ਸਟੇਜ ਲਗਾਉਣ ਵਿੱਚ ਹੱਥ ਵਟਾਓ"]),
              ])),
        ]},
        {"id": "B1+-U3", "title": "ਰਿਪੋਰਟ ਅਤੇ ਸਿੱਖਿਆ", "lessons": [
            L("ਰਿਪੋਰਟ ਲਿਖਣਾ",
              "A report is written in the impersonal past: ਕੰਮ ਹੋਇਆ, ਅੰਕੜੇ ਇਕੱਠੇ ਕੀਤੇ ਗਏ, ਨਤੀਜਾ "
              "ਮਿਲਿਆ. The passive with ਗਏ keeps the writer out, and ਹਵਾਲਾ names where the figures "
              "came from.",
              [V("ਰਿਪੋਰਟ", "report", "report", "noun"),
               V("ਨਤੀਜਾ", "natija", "result", "noun"),
               V("ਇਕੱਠਾ", "ikattha", "collected, together", "adjective"),
               V("ਸਫ਼ਾ", "safa", "page", "noun"),
               V("ਖ਼ੁਲਾਸਾ", "khulasa", "summary", "noun")],
              G("Writing in the impersonal",
                "ਕੰਮ ਹੋਇਆ · ਅੰਕੜੇ ਇਕੱਠੇ ਕੀਤੇ ਗਏ · ਨਤੀਜਾ ਮਿਲਿਆ",
                "The report avoids ਅਸੀਂ and ਮੈਂ: ਕੰਮ ਹੋਇਆ (the work was done), ਅੰਕੜੇ ਇਕੱਠੇ ਕੀਤੇ "
                "ਗਏ (the figures were collected), ਨਤੀਜਾ ਮਿਲਿਆ (a result was obtained). The source "
                "is given with ਹਵਾਲੇ ਅਨੁਸਾਰ or ਰਿਪੋਰਟ ਦੇ ਅਨੁਸਾਰ.",
                [X("ਪ੍ਰੋਗਰਾਮ ਦਾ ਕੰਮ ਸਮੇਂ ਸਿਰ ਹੋਇਆ।", "program da kam samen sir hoia.", "The programme work was done on time."),
                 X("ਅੰਕੜੇ ਹਵਾਲਿਆਂ ਸਮੇਤ ਇਕੱਠੇ ਕੀਤੇ ਗਏ।", "ankde havalean samet ikatthe kite gae.", "The figures were collected along with references."),
                 X("ਰਿਪੋਰਟ ਦੇ ਖ਼ੁਲਾਸੇ ਵਿੱਚ ਨਤੀਜਾ ਸਪਸ਼ਟ ਹੈ।", "report de khulase vich natija spasht hai.", "The result is clear in the summary of the report.")],
                [("ਮੈਂ ਰਿਪੋਰਟ ਵਿੱਚ ਅੰਕੜੇ ਇਕੱਠੇ ਕੀਤੇ ਗਏ।", "ਰਿਪੋਰਟ ਵਿੱਚ ਅੰਕੜੇ ਇਕੱਠੇ ਕੀਤੇ ਗਏ।", "The impersonal report leaves ਮੈਂ out."),
                 ("ਨਤੀਜਾ ਮਿਲੀ।", "ਨਤੀਜਾ ਮਿਲਿਆ।", "ਨਤੀਜਾ is masculine: ਮਿਲਿਆ.")]),
              [D("ਪ੍ਰਧਾਨ", "ਰਿਪੋਰਟ ਤਿਆਰ ਹੈ?", "report taiar hai?", "Is the report ready?"),
               D("ਸਕੱਤਰ", "ਖ਼ੁਲਾਸਾ ਲਿਖਿਆ ਹੈ। ਕੰਮ ਸਮੇਂ ਸਿਰ ਹੋਇਆ।", "khulasa likhia hai. kam samen sir hoia.", "The summary is written. The work was done on time."),
               D("ਪ੍ਰਧਾਨ", "ਅੰਕੜੇ ਕਿੱਥੋਂ ਲਏ?", "ankde kitthon lae?", "Where did the figures come from?"),
               D("ਸਕੱਤਰ", "ਹਵਾਲਿਆਂ ਸਮੇਤ ਇਕੱਠੇ ਕੀਤੇ ਗਏ, ਅਤੇ ਨਤੀਜਾ ਇੱਕ ਸਫ਼ੇ ਉੱਤੇ ਹੈ।", "havalean samet ikatthe kite gae, ate natija ikk safe utte hai.", "They were collected with references, and the result is on one page.")],
              WS("Report worksheet", [
                  T("Write impersonally.", ["the work was done on time", "the figures were collected"],
                    ["ਕੰਮ ਸਮੇਂ ਸਿਰ ਹੋਇਆ", "ਅੰਕੜੇ ਇਕੱਠੇ ਕੀਤੇ ਗਏ"]),
                  T("Name the source.", ["the result is clear in the summary", "along with references"],
                    ["ਖ਼ੁਲਾਸੇ ਵਿੱਚ ਨਤੀਜਾ ਸਪਸ਼ਟ ਹੈ", "ਹਵਾਲਿਆਂ ਸਮੇਤ"]),
              ])),
            L("ਜਵਾਬਦੇਹੀ",
              "Answering for work needs the passive and the person: ਕੰਮ ਦੀ ਜਵਾਬਦੇਹੀ ਸਕੱਤਰ ਦੀ ਸੀ, "
              "ਦੇਰੀ ਲਈ ਜ਼ਿੰਮੇਵਾਰੀ ਲਈ ਗਈ. The question ਕਿਸ ਦੀ ਜਵਾਬਦੇਹੀ ਸੀ? asks who was answerable, "
              "and ਜ਼ਿੰਮੇਵਾਰੀ ਲੈਣਾ takes the responsibility.",
              [V("ਜਵਾਬਦੇਹੀ", "javabdehi", "accountability", "noun"),
               V("ਦੇਰੀ", "deri", "delay", "noun"),
               V("ਸਬੱਬ", "sababb", "reason, cause", "noun"),
               V("ਲੈਣਾ", "laina", "to take", "verb"),
               V("ਸੁਧਾਰ", "sudhar", "improvement", "noun")],
              G("Naming who answers for what",
                "ਕੰਮ ਦੀ ਜਵਾਬਦੇਹੀ ਸਕੱਤਰ ਦੀ ਸੀ · ਦੇਰੀ ਲਈ ਜ਼ਿੰਮੇਵਾਰੀ ਲਈ ਗਈ · ਸੁਧਾਰ ਦੀ ਗੁੰਜਾਇਸ਼ ਹੈ",
                "The responsibility is stated with ਦੀ ਜਵਾਬਦੇਹੀ: ਕੰਮ ਦੀ ਜਵਾਬਦੇਹੀ ਸਕੱਤਰ ਦੀ ਸੀ. The "
                "reason takes ਲਈ (ਦੇਰੀ ਲਈ), the passive ਲਈ ਗਈ keeps it impersonal, and ਗੁੰਜਾਇਸ਼ ਹੈ "
                "says there is still room to improve.",
                [X("ਸਟੇਜ ਦੇ ਕੰਮ ਦੀ ਜਵਾਬਦੇਹੀ ਰਾਜ ਦੀ ਸੀ।", "stage de kam di javabdehi raj di si.", "Raj was answerable for the stage work."),
                 X("ਦੇਰੀ ਲਈ ਦੋ ਸਬੱਬ ਸਨ।", "deri lai do sababb san.", "There were two reasons for the delay."),
                 X("ਸੁਧਾਰ ਦੀ ਗੁੰਜਾਇਸ਼ ਹੈ।", "sudhar di gunjaish hai.", "There is room for improvement.")],
                [("ਜਵਾਬਦੇਹੀ ਰਾਜ ਸੀ।", "ਜਵਾਬਦੇਹੀ ਰਾਜ ਦੀ ਸੀ।", "The answerable person takes ਦੀ: ਰਾਜ ਦੀ ਸੀ."),
                 ("ਦੇਰੀ ਵਾਸਤੇ ਦੋ ਸਬੱਬ ਸਨ।", "ਦੇਰੀ ਲਈ ਦੋ ਸਬੱਬ ਸਨ।", "Punjabi uses ਲਈ for a reason: ਦੇਰੀ ਲਈ.")]),
              [D("ਪ੍ਰਧਾਨ", "ਦੇਰੀ ਕਿਉਂ ਹੋਈ?", "deri kiun hoi?", "Why was there a delay?"),
               D("ਸਕੱਤਰ", "ਦੋ ਸਬੱਬ ਸਨ: ਪਾਣੀ ਅਤੇ ਬਿਜਲੀ।", "do sababb san: pani ate bijli.", "There were two reasons: water and electricity."),
               D("ਪ੍ਰਧਾਨ", "ਜਵਾਬਦੇਹੀ ਕਿਸ ਦੀ ਸੀ?", "javabdehi kis di si?", "Who was answerable?"),
               D("ਸਕੱਤਰ", "ਸਟੇਜ ਦੀ ਰਾਜ ਦੀ, ਅਤੇ ਬਾਕੀ ਕੰਮ ਦੀ ਸਾਡੀ। ਸੁਧਾਰ ਦੀ ਗੁੰਜਾਇਸ਼ ਹੈ।", "stage di raj di, ate baki kam di sadi. sudhar di gunjaish hai.", "The stage's was Raj's, and the rest of the work ours. There is room for improvement.")],
              WS("Accountability worksheet", [
                  T("Name who answers.", ["Raj was answerable for the stage work", "who was answerable?"],
                    ["ਸਟੇਜ ਦੇ ਕੰਮ ਦੀ ਜਵਾਬਦੇਹੀ ਰਾਜ ਦੀ ਸੀ", "ਜਵਾਬਦੇਹੀ ਕਿਸ ਦੀ ਸੀ?"]),
                  T("Give the reasons.", ["there were two reasons for the delay", "there is room for improvement"],
                    ["ਦੇਰੀ ਲਈ ਦੋ ਸਬੱਬ ਸਨ", "ਸੁਧਾਰ ਦੀ ਗੁੰਜਾਇਸ਼ ਹੈ"]),
              ])),
            L("ਅਗਲੀ ਵਾਰ ਲਈ ਸਿੱਖਿਆ",
              "The last page of a report says what to do differently: ਅਸੀਂ ਇਹ ਸਿੱਖਿਆ ਕਿ, ਅਗਲੀ ਵਾਰ "
              "ਪਹਿਲਾਂ ਸੂਚੀ ਬਣੇਗੀ, ਤਿਆਰੀ ਦੋ ਦਿਨ ਪਹਿਲਾਂ ਸ਼ੁਰੂ ਹੋਵੇਗੀ. ਸਿੱਖਿਆ (lesson) and ਅਗਲੀ ਵਾਰ "
              "(next time) turn a difficulty into a plan.",
              [V("ਸਿੱਖਿਆ", "sikhia", "lesson, learning", "noun"),
               V("ਅਗਲੀ ਵਾਰ", "agli var", "next time", "phrase"),
               V("ਪਹਿਲਾਂ", "pahilan", "before, in advance", "adverb"),
               V("ਤਜਵੀਜ਼", "tajviz", "proposal, suggestion", "noun"),
               V("ਸੁਝਾਅ", "sujhaa", "suggestion", "noun")],
              G("Turning a difficulty into a plan",
                "ਅਸੀਂ ਇਹ ਸਿੱਖਿਆ ਕਿ · ਅਗਲੀ ਵਾਰ ਪਹਿਲਾਂ · ਤਜਵੀਜ਼ ਹੈ ਕਿ",
                "The lesson is introduced with ਅਸੀਂ ਇਹ ਸਿੱਖਿਆ ਕਿ, the plan with ਤਜਵੀਜ਼ ਹੈ ਕਿ (both "
                "take a clause after ਕਿ), and the time with ਅਗਲੀ ਵਾਰ ਪਹਿਲਾਂ. The suggestion can "
                "also be plural: ਦੋ ਸੁਝਾਅ ਸਨ.",
                [X("ਅਸੀਂ ਇਹ ਸਿੱਖਿਆ ਕਿ ਸੂਚੀ ਪਹਿਲਾਂ ਬਣਾਉਣੀ ਚਾਹੀਦੀ ਹੈ।", "asin ih sikhia ki suchi pahilan banauni chahidi hai.", "We learned that the list should be made in advance."),
                 X("ਤਜਵੀਜ਼ ਹੈ ਕਿ ਤਿਆਰੀ ਦੋ ਦਿਨ ਪਹਿਲਾਂ ਸ਼ੁਰੂ ਹੋਵੇ।", "tajviz hai ki taiari do din pahilan shuru hove.", "The proposal is that the preparation start two days earlier."),
                 X("ਅਗਲੀ ਵਾਰ ਦੋ ਸੁਝਾਅ ਅਮਲ ਵਿੱਚ ਲਿਆਂਦੇ ਜਾਣਗੇ।", "agli var do sujhaa amal vich liaande jange.", "Next time two suggestions will be put into practice.")],
                [("ਅਸੀਂ ਇਹ ਸਿੱਖਿਆ ਸਿੱਖਿਆ।", "ਅਸੀਂ ਇਹ ਸਿੱਖਿਆ।", "One ਸਿੱਖਿਆ is the whole object."),
                 ("ਤਜਵੀਜ਼ ਹੈ ਕਿ ਤਿਆਰੀ ਸ਼ੁਰੂ ਹੋਵੇਗੀ।", "ਤਜਵੀਜ਼ ਹੈ ਕਿ ਤਿਆਰੀ ਸ਼ੁਰੂ ਹੋਵੇ।", "After ਕਿ the verb is subjunctive: ਹੋਵੇ.")]),
              [D("ਪ੍ਰਧਾਨ", "ਰਿਪੋਰਟ ਦਾ ਆਖ਼ਰੀ ਸਫ਼ਾ?", "report da akhri safa?", "The last page of the report?"),
               D("ਸਕੱਤਰ", "ਅਸੀਂ ਇਹ ਸਿੱਖਿਆ ਕਿ ਸੂਚੀ ਪਹਿਲਾਂ ਬਣੇ।", "asin ih sikhia ki suchi pahilan bane.", "We learned that the list should be made in advance."),
               D("ਪ੍ਰਧਾਨ", "ਕੋਈ ਤਜਵੀਜ਼?", "koi tajviz?", "Any proposal?"),
               D("ਸਕੱਤਰ", "ਹਾਂ, ਅਗਲੀ ਵਾਰ ਤਿਆਰੀ ਦੋ ਦਿਨ ਪਹਿਲਾਂ ਸ਼ੁਰੂ ਹੋਵੇ।", "han, agli var taiari do din pahilan shuru hove.", "Yes, next time the preparation should start two days earlier.")],
              WS("Lessons worksheet", [
                  T("State the lesson.", ["we learned that the list should be made in advance", "the proposal is that the preparation start earlier"],
                    ["ਅਸੀਂ ਇਹ ਸਿੱਖਿਆ ਕਿ ਸੂਚੀ ਪਹਿਲਾਂ ਬਣਾਉਣੀ ਚਾਹੀਦੀ ਹੈ", "ਤਜਵੀਜ਼ ਹੈ ਕਿ ਤਿਆਰੀ ਪਹਿਲਾਂ ਸ਼ੁਰੂ ਹੋਵੇ"]),
                  T("Look ahead.", ["next time the preparation should start two days earlier", "next time two suggestions will be put into practice"],
                    ["ਅਗਲੀ ਵਾਰ ਤਿਆਰੀ ਦੋ ਦਿਨ ਪਹਿਲਾਂ ਸ਼ੁਰੂ ਹੋਵੇ", "ਅਗਲੀ ਵਾਰ ਦੋ ਸੁਝਾਅ ਅਮਲ ਵਿੱਚ ਲਿਆਂਦੇ ਜਾਣਗੇ"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Amritsar is the second city of Punjab after Ludhiana and the centre of the Majha "
                 "region, standing about 28 kilometres from the India–Pakistan border and 47 "
                 "kilometres from Lahore. Its name means the pool of nectar, and the Harmandir "
                 "Sahib, the Golden Temple, sits in the middle of that pool. Anything a learner "
                 "needs in Punjabi is on show here: kirtan heard across the courtyard, langar "
                 "served to everyone who comes, and announcements in Punjabi read out over the "
                 "loudspeakers. Community programmes — gurpurabs, nagar kirtans, school functions "
                 "— are planned by committees, which is exactly the language of this level."),
        source_url="https://en.wikipedia.org/wiki/Amritsar",
        reading=("ਅੰਮ੍ਰਿਤਸਰ ਵਿੱਚ ਸਾਡੀ ਕਮੇਟੀ ਨੇ ਨਗਰ ਕੀਰਤਨ ਦੀ ਤਿਆਰੀ ਲਈ ਮੀਟਿੰਗ ਕੀਤੀ। ਪਹਿਲਾਂ ਕੰਮ ਤਿੰਨ "
                 "ਹਿੱਸਿਆਂ ਵਿੱਚ ਵੰਡਿਆ ਗਿਆ: ਲੰਗਰ, ਸਟੇਜ ਅਤੇ ਲੰਗਰ ਲਈ ਪਾਣੀ। ਸਟੇਜ ਦੀ ਜ਼ਿੰਮੇਵਾਰੀ ਰਾਜ ਨੇ "
                 "ਲਈ, ਅਤੇ ਬਾਕੀ ਕੰਮ ਸਕੱਤਰ ਨੇ। ਫਿਰ ਫ਼ੈਸਲਾ ਹੋਇਆ ਕਿ ਤਾਰੀਖ਼ ਅਗਲੇ ਸ਼ਨੀਵਾਰ ਪੱਕੀ ਕੀਤੀ ਜਾਵੇ "
                 "ਅਤੇ ਸਮਾਂ ਸ਼ਾਮ ਪੰਜ ਵਜੇ ਰੱਖਿਆ ਜਾਵੇ। ਸੱਦੇ ਲਈ ਸੂਚੀ ਬਣੀ, ਅਤੇ ਪਿੰਡਾਂ ਵਿੱਚ ਫ਼ੋਨ ਕੀਤੇ ਗਏ। "
                 "ਪ੍ਰੋਗਰਾਮ ਵਾਲੇ ਦਿਨ ਬਿਜਲੀ ਗਈ, ਇਸ ਲਈ ਅੱਧਾ ਘੰਟਾ ਦੇਰੀ ਹੋਈ। ਰਿਪੋਰਟ ਵਿੱਚ ਅਸੀਂ ਇਹ ਸਿੱਖਿਆ "
                 "ਲਿਖੀ ਕਿ ਅਗਲੀ ਵਾਰ ਜਨਰੇਟਰ ਦਾ ਪਹਿਲਾਂ ਪ੍ਰਬੰਧ ਕਰਨਾ ਚਾਹੀਦਾ ਹੈ।"),
        reading_gloss=("In Amritsar our committee held a meeting to prepare for a nagar kirtan. "
                       "First the work was divided into three parts: langar, the stage, and water "
                       "for the langar. Raj took responsibility for the stage, and the secretary "
                       "took the rest of the work. Then it was decided that the date be fixed for "
                       "next Saturday and the time kept at five in the evening. A list was made "
                       "for the invitations, and calls were made to the villages. On the day of "
                       "the programme the electricity went, so there was a delay of half an hour. "
                       "In the report we wrote the lesson that next time the generator should be "
                       "arranged in advance."),
        listening=("ਸਕੱਤਰ: ਪ੍ਰਧਾਨ ਜੀ, ਰਿਪੋਰਟ ਤਿਆਰ ਹੈ। ਪ੍ਰਧਾਨ: ਕੰਮ ਸਮੇਂ ਸਿਰ ਹੋਇਆ? ਸਕੱਤਰ: ਲੰਗਰ ਅਤੇ ਸਟੇਜ "
                   "ਦਾ ਕੰਮ ਸਮੇਂ ਸਿਰ ਹੋਇਆ, ਪਰ ਬਿਜਲੀ ਕਾਰਨ ਅੱਧਾ ਘੰਟਾ ਦੇਰੀ ਹੋਈ। ਪ੍ਰਧਾਨ: ਜਵਾਬਦੇਹੀ ਕਿਸ ਦੀ "
                   "ਸੀ? ਸਕੱਤਰ: ਬਿਜਲੀ ਦੀ ਜਵਾਬਦੇਹੀ ਕਿਸੇ ਦੀ ਨਹੀਂ ਸੀ, ਇਸ ਲਈ ਅਗਲੀ ਵਾਰ ਜਨਰੇਟਰ ਦਾ ਪ੍ਰਬੰਧ "
                   "ਪਹਿਲਾਂ ਹੋਵੇ।"),

        listening_gloss=("Secretary: President, the report is ready. President: Was the work done on "
                         "time? Secretary: The langar and stage work was done on time, but there "
                         "was a half-hour delay because of the electricity. President: Whose "
                         "responsibility was it? Secretary: The electricity was nobody's "
                         "responsibility, so next time the generator should be arranged in "
                         "advance."),
        voice_tag=VOICE,
        idioms=[
            ("ਕੰਮ ਵੰਡਿਆ", "the work was divided", "tasks handed out, everyone has a share"),
            ("ਫ਼ੈਸਲਾ ਹੋਇਆ", "the decision happened", "it was decided, the matter is settled"),
            ("ਜ਼ਰੂਰ ਆਉਣਾ", "do come for certain", "a warm, firm invitation"),
            ("ਹੱਥ ਵਟਾਉਣਾ", "to exchange hands", "to lend a hand with the work"),
            ("ਜਵਾਬਦੇਹੀ ਲੈਣੀ", "to take accountability", "to answer for a piece of work"),
            ("ਗੁੰਜਾਇਸ਼ ਹੈ", "there is room", "there is still scope to improve"),
            ("ਅਗਲੀ ਵਾਰ", "next time", "let us do it differently next time"),
            ("ਅਮਲ ਵਿੱਚ ਲਿਆਉਣਾ", "to bring into practice", "to carry a suggestion out"),
            ("ਤੈਅ ਹੋਇਆ", "it was settled", "the point is agreed and closed"),
            ("ਸਿੱਖਿਆ ਲੈਣੀ", "to take a lesson", "to learn from what went wrong"),
        ],
        mistakes=[
            ("ਮੈਂ ਨੇ ਕੰਮ ਵੰਡਿਆ।", "ਮੈਂ ਕੰਮ ਵੰਡਿਆ।", "ਮੈਂ never takes ਨੇ; only third-person subjects do."),
            ("ਤਾਰੀਖ਼ ਪੱਕਾ ਕਰਨੀ ਹੈ।", "ਤਾਰੀਖ਼ ਪੱਕੀ ਕਰਨੀ ਹੈ।", "ਤਾਰੀਖ਼ is feminine: ਪੱਕੀ."),
            ("ਜੇ ਲੋੜ ਪਵੇਗੀ ਤਾਂ ਮੀਟਿੰਗ ਸੱਦਾਂਗੇ।", "ਜੇ ਲੋੜ ਪਵੇ ਤਾਂ ਮੀਟਿੰਗ ਸੱਦਾਂਗੇ।", "After ਜੇ the verb is subjunctive: ਪਵੇ."),
        ],
        task_title="Plan a programme and write its report, in Punjabi",
        task_instructions=("Write a Punjabi meeting of ten to twelve turns. Divide three tasks and "
                           "name who takes each with ਨੇ, report one decision with ਫ਼ੈਸਲਾ ਹੋਇਆ ਕਿ, fix "
                           "a date and hour, invite one person, answer one complaint without "
                           "heat, and close with a three-sentence report: what was done, who was "
                           "answerable, and one lesson beginning ਅਸੀਂ ਇਹ ਸਿੱਖਿਆ ਕਿ."),
    ),
    "test": [
        ("translate_en", "Say: it was settled that the programme be next week.", "ਤੈਅ ਹੋਇਆ ਕਿ ਪ੍ਰੋਗਰਾਮ ਅਗਲੇ ਹਫ਼ਤੇ ਹੋਵੇ।"),
        ("translate_pa", "ਅਸੀਂ ਕੰਮ ਤਿੰਨ ਹਿੱਸਿਆਂ ਵਿੱਚ ਵੰਡਿਆ।", "We divided the work into three parts."),
        ("multiple_choice", "Which sentence reports a decision impersonally?", "ਫ਼ੈਸਲਾ ਹੋਇਆ ਕਿ ਸਮਾਂ ਬਦਲਿਆ ਜਾਵੇ।"),
        ("fill_in_the_blank", "ਸਟੇਜ ਦੀ ਜ਼ਿੰਮੇਵਾਰੀ ਰਾਜ ___ ਲਈ।", "ਨੇ"),
        ("word_selection", "Select the Punjabi for 'accountability'.", "ਜਵਾਬਦੇਹੀ"),
        ("error_correction", "ਮੈਂ ਨੇ ਸੂਚੀ ਬਣਾਈ।", "ਮੈਂ ਸੂਚੀ ਬਣਾਈ।"),
        ("dialogue_completion", "Complete: ਸੱਦਾ ਦੇ ਰਹੇ ਹਾਂ, ਸ਼ਨੀਵਾਰ ਸ਼ਾਮ ਪੰਜ ਵਜੇ, ___ (do come)", "ਜ਼ਰੂਰ ਆਉਣਾ"),
        ("matching", "Match ਹੱਥ ਵਟਾਉਣਾ to its meaning.", "to lend a hand"),
        ("reading_comprehension", "ਦੇਰੀ ਕਿਉਂ ਹੋਈ?", "the electricity went off"),
        ("inference", "ਰਿਪੋਰਟ ਵਿੱਚ ਜਨਰੇਟਰ ਦਾ ਜ਼ਿਕਰ ਹੈ। — what does this show about the committee?", "it plans ahead from what went wrong"),
        ("main_idea", "ਕੰਮ ਸਮੇਂ ਸਿਰ ਹੋਇਆ, ਪਰ ਬਿਜਲੀ ਕਾਰਨ ਦੇਰੀ ਹੋਈ। — what is this sentence?", "a balanced report of success and delay"),
        ("detail_identification", "ਅਗਲੀ ਵਾਰ ਕੀ ਪਹਿਲਾਂ ਹੋਵੇ?", "the generator's arrangement"),
    ],
}

HALFSTEPS["B2+"] = {
    "native": NATIVE,
    "title": "%s B2+ — Farm, figures and the department" % NAME,
    "goals": [
        "Read and quote a figure: yield per hectare, comparisons, percentage growth",
        "Write an official application and report what an officer said, without shifting the blame",
        "Read a contract for its conditions: tenure, clause, penalty, approval",
    ],
    "units": [
        {"id": "B2+-U1", "title": "ਖੇਤ ਅਤੇ ਅੰਕੜੇ", "lessons": [
            L("ਫ਼ਸਲ ਦਾ ਹਿਸਾਬ",
              "Farm figures are read in units: ਹੈਕਟੇਅਰ (hectare), ਕੁਇੰਟਲ (quintal), ਝਾੜੀ (yield). "
              "The verb stays impersonal — ਹਿਸਾਬ ਰੱਖਿਆ ਜਾਂਦਾ ਹੈ — and a comparison takes ਨਾਲੋਂ: "
              "ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਵੱਧ ਝਾੜੀ.",
              [V("ਹੈਕਟੇਅਰ", "hectare", "hectare", "noun"),
               V("ਕੁਇੰਟਲ", "quintal", "quintal", "noun"),
               V("ਝਾੜੀ", "jharhi", "yield", "noun"),
               V("ਹਿਸਾਬ", "hisab", "account, reckoning", "noun"),
               V("ਔਸਤ", "ausat", "average", "noun")],
              G("Reporting farm figures",
                "ਹਿੱਸਾਬ ਰੱਖਿਆ ਜਾਂਦਾ ਹੈ · ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਵੱਧ · ਔਸਤ ਕੱਢਣਾ",
                "The impersonal passive ਰੱਖਿਆ ਜਾਂਦਾ ਹੈ keeps the record-keeping out of anybody's "
                "hands. ਔਸਤ (average) is feminine, ਝਾੜੀ (yield) feminine, and both take the "
                "feminine verb: ਔਸਤ ਕੱਢੀ ਗਈ. Comparison uses ਨਾਲੋਂ, a part of the total takes ਵਿੱਚੋਂ.",
                [X("ਹਰ ਹੈਕਟੇਅਰ ਦਾ ਹਿਸਾਬ ਰੱਖਿਆ ਜਾਂਦਾ ਹੈ।", "har hectare da hisab rakhia janda hai.", "The account is kept for every hectare."),
                 X("ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਝਾੜੀ ਵੱਧ ਹੈ।", "pichhle sal nalon jharhi vaddh hai.", "The yield is higher than last year."),
                 X("ਪੰਜਾਹ ਹੈਕਟੇਅਰਾਂ ਦੀ ਔਸਤ ਕੱਢੀ ਗਈ।", "pachas hectarean di ausat kaddhi gai.", "The average of fifty hectares was worked out.")],
                [("ਔਸਤ ਕੱਢਿਆ ਗਿਆ।", "ਔਸਤ ਕੱਢੀ ਗਈ।", "ਔਸਤ is feminine: ਕੱਢੀ ਗਈ."),
                 ("ਪਿਛਲੇ ਸਾਲ ਤੋਂ ਝਾੜੀ ਵੱਧ ਹੈ।", "ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਝਾੜੀ ਵੱਧ ਹੈ।", "Comparison takes ਨਾਲੋਂ.")]),
              [D("ਅਧਿਕਾਰੀ", "ਝਾੜੀ ਦਾ ਹਿਸਾਬ ਤਿਆਰ ਹੈ?", "jharhi da hisab taiar hai?", "Is the yield account ready?"),
               D("ਕਿਸਾਨ", "ਹਾਂ, ਪੰਜਾਹ ਹੈਕਟੇਅਰਾਂ ਦਾ ਹਿਸਾਬ ਰੱਖਿਆ ਗਿਆ।", "han, pachas hectarean da hisab rakhia gia.", "Yes, the account of fifty hectares was kept."),
               D("ਅਧਿਕਾਰੀ", "ਔਸਤ ਕੀ ਬਣੀ?", "ausat ki bani?", "What did the average come to?"),
               D("ਕਿਸਾਨ", "ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਚਾਰ ਕੁਇੰਟਲ ਵੱਧ ਝਾੜੀ ਹੈ।", "pichhle sal nalon char quintal vaddh jharhi hai.", "The yield is four quintals more than last year.")],
              WS("Figures worksheet", [
                  T("State the record.", ["the account is kept for every hectare", "the average of fifty hectares was worked out"],
                    ["ਹਰ ਹੈਕਟੇਅਰ ਦਾ ਹਿਸਾਬ ਰੱਖਿਆ ਜਾਂਦਾ ਹੈ", "ਪੰਜਾਹ ਹੈਕਟੇਅਰਾਂ ਦੀ ਔਸਤ ਕੱਢੀ ਗਈ"]),
                  T("Compare.", ["the yield is higher than last year", "four quintals more than last year"],
                    ["ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਝਾੜੀ ਵੱਧ ਹੈ", "ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਚਾਰ ਕੁਇੰਟਲ ਵੱਧ"]),
              ])),
            L("ਪੈਦਾਵਾਰ ਦੀ ਤੁਲਨਾ",
              "Comparisons are made with ਨਾਲੋਂ, ਵਿੱਚੋਂ and ਦੇ ਮੁਕਾਬਲੇ: ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਵੱਧ, ਹਰ ਸੌ "
              "ਵਿੱਚੋਂ ਸੱਠ, ਮੰਡੀ ਦੇ ਮੁਕਾਬਲੇ। The comparative sentence keeps ਹੈ at the end, and the "
              "figures stay singular.",
              [V("ਪੈਦਾਵਾਰ", "paidavar", "production", "noun"),
               V("ਮੁਕਾਬਲਾ", "mukabla", "comparison, competition", "noun"),
               V("ਵਾਧਾ", "vadha", "growth", "noun"),
               V("ਕਮੀ", "kami", "shortfall", "noun"),
               V("ਜ਼ਮੀਨ", "zamin", "land", "noun")],
              G("Comparing two years",
                "ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਵੱਧ · ਮੰਡੀ ਦੇ ਮੁਕਾਬਲੇ ਘੱਟ · ਹਰ ਸੌ ਵਿੱਚੋਂ ਸੱਠ",
                "ਨਾਲੋਂ compares like with like, ਦੇ ਮੁਕਾਬਲੇ sets one against another, and ਵਿੱਚੋਂ "
                "takes a part out of the whole. ਵਾਧਾ (growth) and ਕਮੀ (shortfall) are both "
                "masculine and feminine respectively: ਵਾਧਾ ਹੋਇਆ, ਕਮੀ ਰਹੀ.",
                [X("ਇਸ ਸਾਲ ਪੈਦਾਵਾਰ ਵਿੱਚ ਵਾਧਾ ਹੋਇਆ।", "is sal paidavar vich vadha hoia.", "This year there was growth in production."),
                 X("ਮੰਡੀ ਦੇ ਮੁਕਾਬਲੇ ਇੱਥੇ ਭਾਅ ਘੱਟ ਹੈ।", "mandi de mukable itthe bhaa ghatt hai.", "The price here is lower compared with the market."),
                 X("ਹਰ ਸੌ ਵਿੱਚੋਂ ਸੱਠ ਕਿਸਾਨਾਂ ਕੋਲ ਸਿੰਚਾਈ ਹੈ।", "har sau vichon satth kisanan kol sinchai hai.", "Sixty out of every hundred farmers have irrigation.")],
                [("ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਪੈਦਾਵਾਰ ਵਾਧਾ ਹੋਇਆ ਵੱਧ।", "ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਪੈਦਾਵਾਰ ਵੱਧ ਹੋਈ।", "The comparison needs one verb: ਵੱਧ ਹੋਈ."),
                 ("ਮੰਡੀ ਨਾਲੋਂ ਮੁਕਾਬਲੇ ਘੱਟ।", "ਮੰਡੀ ਦੇ ਮੁਕਾਬਲੇ ਘੱਟ।", "ਦੇ ਮੁਕਾਬਲੇ already carries the comparison.")]),
              [D("ਅਧਿਕਾਰੀ", "ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਕੀ ਫ਼ਰਕ ਹੈ?", "pichhle sal nalon ki farak hai?", "What is the difference from last year?"),
               D("ਕਿਸਾਨ", "ਕਮੀ ਘੱਟ ਹੋਈ, ਪਰ ਵਾਧਾ ਵੀ ਥੋੜ੍ਹਾ ਹੈ।", "kami ghatt hoi, par vadha vi thorha hai.", "The shortfall came down, but the growth is also small."),
               D("ਅਧਿਕਾਰੀ", "ਅਤੇ ਮੰਡੀ ਦੇ ਮੁਕਾਬਲੇ?", "ate mandi de mukable?", "And compared with the market?"),
               D("ਕਿਸਾਨ", "ਮੰਡੀ ਦੇ ਮੁਕਾਬਲੇ ਸਾਡਾ ਭਾਅ ਘੱਟ ਹੈ, ਇਹੀ ਗੱਲ ਰਿਪੋਰਟ ਵਿੱਚ ਲਿਖੀ ਜਾਵੇ।", "mandi de mukable sada bhaa ghatt hai, ihi gal report vich likhi jave.", "Our price is lower than the market's; let this be written in the report.")],
              WS("Comparison worksheet", [
                  T("Compare the years.", ["this year there was growth in production", "the yield is higher than last year"],
                    ["ਇਸ ਸਾਲ ਪੈਦਾਵਾਰ ਵਿੱਚ ਵਾਧਾ ਹੋਇਆ", "ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਝਾੜੀ ਵੱਧ ਹੈ"]),
                  T("Compare the market.", ["the price here is lower compared with the market", "sixty out of every hundred farmers"],
                    ["ਮੰਡੀ ਦੇ ਮੁਕਾਬਲੇ ਇੱਥੇ ਭਾਅ ਘੱਟ ਹੈ", "ਹਰ ਸੌ ਵਿੱਚੋਂ ਸੱਠ ਕਿਸਾਨ"]),
              ])),
            L("ਮੰਡੀ ਅਤੇ ਭਾਅ",
              "The market has its own words: ਮੰਡੀ (market), ਆੜ੍ਹਤੀ (commission agent), ਤੁਲਾਈ "
              "(weighing), ਬਾਰਦਾਨਾ (packaging). A price agreement is reported in the passive: "
              "ਭਾਅ ਤੈਅ ਕੀਤਾ ਗਿਆ, ਅਤੇ ਭੁਗਤਾਨ ਦੀ ਮਿਆਦ ਤਿੰਨ ਦਿਨ ਰੱਖੀ ਗਈ.",
              [V("ਮੰਡੀ", "mandi", "market", "noun"),
               V("ਆੜ੍ਹਤੀ", "aarhti", "commission agent", "noun"),
               V("ਤੁਲਾਈ", "tulai", "weighbridge", "noun"),
               V("ਭੁਗਤਾਨ", "bhugtan", "payment", "noun"),
               V("ਮਿਆਦ", "miad", "term, tenure", "noun")],
              G("Agreeing a price in the market",
                "ਭਾਅ ਤੈਅ ਕੀਤਾ ਗਿਆ · ਭੁਗਤਾਨ ਦੀ ਮਿਆਦ · ਤੁਲਾਈ ਉੱਤੇ ਤੋਲਿਆ ਜਾਵੇ",
                "Agreements in the market are reported impersonally: ਭਾਅ ਤੈਅ ਕੀਤਾ ਗਿਆ, ਮਿਆਦ ਤਿੰਨ "
                "ਦਿਨ ਰੱਖੀ ਗਈ. A condition takes the subjunctive: ਤੁਲਾਈ ਉੱਤੇ ਤੋਲਿਆ ਜਾਵੇ (let it be "
                "weighed at the weighbridge).",
                [X("ਭਾਅ ਤੈਅ ਕੀਤਾ ਗਿਆ।", "bhaa tai kita gia.", "The price was settled."),
                 X("ਭੁਗਤਾਨ ਦੀ ਮਿਆਦ ਤਿੰਨ ਦਿਨ ਰੱਖੀ ਗਈ।", "bhugtan di miad tinn din rakhhi gai.", "The payment term was kept at three days."),
                 X("ਸ਼ਰਤ ਹੈ ਕਿ ਸਮਾਨ ਤੁਲਾਈ ਉੱਤੇ ਤੋਲਿਆ ਜਾਵੇ।", "sharat hai ki saman tulai utte tolia jave.", "The condition is that the goods be weighed at the weighbridge.")],
                [("ਭਾਅ ਤੈਅ ਕੀਤਾ।", "ਭਾਅ ਤੈਅ ਕੀਤਾ ਗਿਆ।", "An impersonal agreement takes ਗਿਆ."),
                 ("ਸ਼ਰਤ ਹੈ ਕਿ ਸਮਾਨ ਤੋਲਿਆ ਜਾਵੇਗਾ।", "ਸ਼ਰਤ ਹੈ ਕਿ ਸਮਾਨ ਤੋਲਿਆ ਜਾਵੇ।", "A condition takes the subjunctive ਜਾਵੇ.")]),
              [D("ਕਿਸਾਨ", "ਭਾਅ ਤੈਅ ਹੋਇਆ?", "bhaa tai hoia?", "Is the price settled?"),
               D("ਆੜ੍ਹਤੀ", "ਹਾਂ, ਭਾਅ ਤੈਅ ਕੀਤਾ ਗਿਆ ਅਤੇ ਮਿਆਦ ਤਿੰਨ ਦਿਨ ਰੱਖੀ ਗਈ।", "han, bhaa tai kita gia ate miad tinn din rakhhi gai.", "Yes, the price was settled and the term kept at three days."),
               D("ਕਿਸਾਨ", "ਤੋਲ ਕਿੱਥੇ ਹੋਵੇਗਾ?", "tol kithe hovega?", "Where will the weighing be?"),
               D("ਆੜ੍ਹਤੀ", "ਸ਼ਰਤ ਹੈ ਕਿ ਸਮਾਨ ਤੁਲਾਈ ਉੱਤੇ ਤੋਲਿਆ ਜਾਵੇ।", "sharat hai ki saman tulai utte tolia jave.", "The condition is that the goods be weighed at the weighbridge.")],
              WS("Market worksheet", [
                  T("Report the agreement.", ["the price was settled", "the payment term was kept at three days"],
                    ["ਭਾਅ ਤੈਅ ਕੀਤਾ ਗਿਆ", "ਭੁਗਤਾਨ ਦੀ ਮਿਆਦ ਤਿੰਨ ਦਿਨ ਰੱਖੀ ਗਈ"]),
                  T("State the condition.", ["the condition is that the goods be weighed at the weighbridge", "where will the weighing be?"],
                    ["ਸ਼ਰਤ ਹੈ ਕਿ ਸਮਾਨ ਤੁਲਾਈ ਉੱਤੇ ਤੋਲਿਆ ਜਾਵੇ", "ਤੋਲ ਕਿੱਥੇ ਹੋਵੇਗਾ?"]),
              ])),
        ]},
        {"id": "B2+-U2", "title": "ਸਰਕਾਰੀ ਦਫ਼ਤਰ", "lessons": [
            L("ਅਰਜ਼ੀ ਦੇਣਾ",
              "An official application has a fixed shape: ਸੰਬੋਧਨ, ਵਿਸ਼ਾ, ਬੇਨਤੀ, ਹਸਤਾਖ਼ਰ. ਵਿਸ਼ਾ "
              "(subject) names the matter in one line, and ਬੇਨਤੀ ਹੈ ਕਿ opens the request with a "
              "subjunctive verb.",
              [V("ਅਰਜ਼ੀ", "arzi", "application", "noun"),
               V("ਵਿਸ਼ਾ", "visha", "subject, topic", "noun"),
               V("ਮਨਜ਼ੂਰੀ", "manzuri", "approval", "noun"),
               V("ਅਨੁਸਾਰ", "anusar", "according to", "postposition"),
               V("ਨੋਟਿਸ", "notis", "notice", "noun")],
              G("Writing an application",
                "ਵਿਸ਼ਾ: ਪਾਣੀ ਦੀ ਸਮੱਸਿਆ · ਬੇਨਤੀ ਹੈ ਕਿ · ਨਿਯਮਾਂ ਅਨੁਸਾਰ",
                "The subject line is a noun phrase, not a sentence: ਵਿਸ਼ਾ: ਪਾਣੀ ਦੀ ਸਮੱਸਿਆ. The "
                "request follows ਬੇਨਤੀ ਹੈ ਕਿ with ਜਾਵੇ or ਹੋਵੇ, and any reference to rules takes "
                "ਅਨੁਸਾਰ: ਨਿਯਮਾਂ ਅਨੁਸਾਰ ਮਨਜ਼ੂਰੀ ਦਿੱਤੀ ਜਾਵੇ.",
                [X("ਵਿਸ਼ਾ: ਪਿੰਡ ਵਿੱਚ ਪਾਣੀ ਦੀ ਸਮੱਸਿਆ।", "visha: pind vich pani di sammasia.", "Subject: the water problem in the village."),
                 X("ਬੇਨਤੀ ਹੈ ਕਿ ਪਾਈਪ ਦੀ ਮੁਰੰਮਤ ਕਰਵਾਈ ਜਾਵੇ।", "benti hai ki paip di murmmat karvaai jave.", "The request is that the pipe be repaired."),
                 X("ਨਿਯਮਾਂ ਅਨੁਸਾਰ ਮਨਜ਼ੂਰੀ ਬਣਦੀ ਹੈ।", "niyaman anusar manzuri bandi hai.", "As per the rules, approval is due.")],
                [("ਵਿਸ਼ਾ: ਪਾਣੀ ਦੀ ਸਮੱਸਿਆ ਹੈ।", "ਵਿਸ਼ਾ: ਪਾਣੀ ਦੀ ਸਮੱਸਿਆ।", "A subject line is a phrase, not a sentence."),
                 ("ਬੇਨਤੀ ਹੈ ਕਿ ਮੁਰੰਮਤ ਕਰਵਾਈ ਜਾਵੇਗੀ।", "ਬੇਨਤੀ ਹੈ ਕਿ ਮੁਰੰਮਤ ਕਰਵਾਈ ਜਾਵੇ।", "After ਕਿ the request takes the subjunctive ਜਾਵੇ.")]),
              [D("ਪਿੰਡ ਵਾਲਾ", "ਅਰਜ਼ੀ ਕਿਵੇਂ ਲਿਖੀਏ?", "arzi kiven likhie?", "How shall we write the application?"),
               D("ਸਕੱਤਰ", "ਪਹਿਲਾਂ ਵਿਸ਼ਾ ਲਿਖੋ: ਪਿੰਡ ਵਿੱਚ ਪਾਣੀ ਦੀ ਸਮੱਸਿਆ।", "pahilan visha likho: pind vich pani di sammasia.", "First write the subject: the water problem in the village."),
               D("ਪਿੰਡ ਵਾਲਾ", "ਫਿਰ ਬੇਨਤੀ?", "phir benti?", "Then the request?"),
               D("ਸਕੱਤਰ", "ਬੇਨਤੀ ਹੈ ਕਿ ਪਾਈਪ ਦੀ ਮੁਰੰਮਤ ਕਰਵਾਈ ਜਾਵੇ, ਨਿਯਮਾਂ ਅਨੁਸਾਰ।", "benti hai ki paip di murmmat karvaai jave, niyaman anusar.", "The request is that the pipe be repaired, according to the rules.")],
              WS("Application worksheet", [
                  T("Write the subject line.", ["the water problem in the village", "application according to the rules"],
                    ["ਵਿਸ਼ਾ: ਪਿੰਡ ਵਿੱਚ ਪਾਣੀ ਦੀ ਸਮੱਸਿਆ", "ਨਿਯਮਾਂ ਅਨੁਸਾਰ ਅਰਜ਼ੀ"]),
                  T("Write the request.", ["the request is that the pipe be repaired", "approval is due"],
                    ["ਬੇਨਤੀ ਹੈ ਕਿ ਪਾਈਪ ਦੀ ਮੁਰੰਮਤ ਕਰਵਾਈ ਜਾਵੇ", "ਮਨਜ਼ੂਰੀ ਬਣਦੀ ਹੈ"]),
              ])),
            L("ਰਿਪੋਰਟ ਦਾ ਹਵਾਲਾ",
              "A report is quoted with ਹਵਾਲਾ ਦੇਣਾ: ਰਿਪੋਰਟ ਵਿੱਚ ਦੱਸਿਆ ਗਿਆ ਹੈ ਕਿ …, ਅੰਕੜਿਆਂ "
              "ਅਨੁਸਾਰ …, ਅਧਿਕਾਰੀ ਨੇ ਦੱਸਿਆ ਕਿ ਉਹ …. Reported words shift the pronoun: ਮੈਂ becomes "
              "ਉਹ, and the tense moves back.",
              [V("ਹਵਾਲਾ", "havala", "citation, reference", "noun"),
               V("ਰਿਪੋਰਟ", "report", "report", "noun"),
               V("ਅੰਕੜਾ", "ankra", "figure, statistic", "noun"),
               V("ਦੱਸਿਆ", "dassia", "s/he told", "verb"),
               V("ਸੋਧ", "sodh", "correction, revision", "noun")],
              G("Quoting a report",
                "ਰਿਪੋਰਟ ਵਿੱਚ ਦੱਸਿਆ ਗਿਆ ਹੈ ਕਿ · ਅੰਕੜਿਆਂ ਅਨੁਸਾਰ · ਅਧਿਕਾਰੀ ਨੇ ਦੱਸਿਆ ਕਿ",
                "A quoted report uses the impersonal ਦੱਸਿਆ ਗਿਆ ਹੈ ਕਿ, the figures take ਅਨੁਸਾਰ, and "
                "the official's words take the reporting verb with ਕਿ: ਅਧਿਕਾਰੀ ਨੇ ਦੱਸਿਆ ਕਿ ਉਹ "
                "ਜਾਂਚ ਕਰੇਗਾ. Inside the quote ਮੈਂ shifts to ਉਹ.",
                [X("ਰਿਪੋਰਟ ਵਿੱਚ ਦੱਸਿਆ ਗਿਆ ਹੈ ਕਿ ਕੰਮ ਪੂਰਾ ਹੋਇਆ।", "report vich dassia gia hai ki kam pura hoia.", "In the report it is stated that the work was completed."),
                 X("ਅੰਕੜਿਆਂ ਅਨੁਸਾਰ ਝਾੜੀ ਵੱਧੀ ਹੈ।", "ankdian anusar jharhi vaddhi hai.", "According to the figures the yield has risen."),
                 X("ਅਧਿਕਾਰੀ ਨੇ ਦੱਸਿਆ ਕਿ ਉਹ ਜਾਂਚ ਕਰੇਗਾ।", "adhikari ne dassia ki uh janch karega.", "The officer said that he would investigate.")],
                [("ਅਧਿਕਾਰੀ ਨੇ ਦੱਸਿਆ ਕਿ ਮੈਂ ਜਾਂਚ ਕਰਾਂਗਾ।", "ਅਧਿਕਾਰੀ ਨੇ ਦੱਸਿਆ ਕਿ ਉਹ ਜਾਂਚ ਕਰੇਗਾ।", "In a quotation the speaker's ਮੈਂ becomes ਉਹ."),
                 ("ਅੰਕੜੇ ਅਨੁਸਾਰ ਝਾੜੀ ਵੱਧੀ ਹੈ।", "ਅੰਕੜਿਆਂ ਅਨੁਸਾਰ ਝਾੜੀ ਵੱਧੀ ਹੈ।", "ਅੰਕੜਿਆਂ is the plural oblique.")]),
              [D("ਪੱਤਰਕਾਰ", "ਰਿਪੋਰਟ ਵਿੱਚ ਕੀ ਲਿਖਿਆ ਹੈ?", "report vich ki likhia hai?", "What does the report say?"),
               D("ਅਧਿਕਾਰੀ", "ਰਿਪੋਰਟ ਵਿੱਚ ਦੱਸਿਆ ਗਿਆ ਹੈ ਕਿ ਕੰਮ ਪੂਰਾ ਹੋਇਆ।", "report vich dassia gia hai ki kam pura hoia.", "In the report it is stated that the work was completed."),
               D("ਪੱਤਰਕਾਰ", "ਅੰਕੜੇ?", "ankde?", "The figures?"),
               D("ਅਧਿਕਾਰੀ", "ਅੰਕੜਿਆਂ ਅਨੁਸਾਰ ਝਾੜੀ ਵੱਧੀ ਹੈ, ਅਤੇ ਸੋਧ ਵੀ ਹੋਈ ਹੈ।", "ankdian anusar jharhi vaddhi hai, ate sodh vi hoi hai.", "According to the figures the yield has risen, and there has also been a revision.")],
              WS("Citation worksheet", [
                  T("Quote the report.", ["in the report it is stated that the work was completed", "according to the figures the yield has risen"],
                    ["ਰਿਪੋਰਟ ਵਿੱਚ ਦੱਸਿਆ ਗਿਆ ਹੈ ਕਿ ਕੰਮ ਪੂਰਾ ਹੋਇਆ", "ਅੰਕੜਿਆਂ ਅਨੁਸਾਰ ਝਾੜੀ ਵੱਧੀ ਹੈ"]),
                  T("Report the officer.", ["the officer said that he would investigate", "then the figures?"],
                    ["ਅਧਿਕਾਰੀ ਨੇ ਦੱਸਿਆ ਕਿ ਉਹ ਜਾਂਚ ਕਰੇਗਾ", "ਅਤੇ ਅੰਕੜੇ?"]),
              ])),
            L("ਮੀਟਿੰਗ ਦੀ ਕਾਰਵਾਈ",
              "The record of a meeting is called ਕਾਰਵਾਈ: ਕਾਰਵਾਈ ਲਿਖੀ ਗਈ, ਤਜਵੀਜ਼ਾਂ ਰੱਖੀਆਂ ਗਈਆਂ, "
              "ਫ਼ੈਸਲਾ ਲਿਆ ਗਿਆ. Passives dominate because the record is about what was done, not who "
              "did it.",
              [V("ਕਾਰਵਾਈ", "karvaai", "proceedings, action", "noun"),
               V("ਨਿਮਾਣਾ", "nimana", "humble (the undersigned)", "adjective"),
               V("ਸੰਖੇਪ", "sankhep", "brief, summary", "noun"),
               V("ਤਾਰੀਖ਼", "tarikh", "date", "noun"),
               V("ਦਸਤਖ਼ਤ", "dastakhat", "signature", "noun")],
              G("Keeping the minutes",
                "ਕਾਰਵਾਈ ਲਿਖੀ ਗਈ · ਫ਼ੈਸਲਾ ਲਿਆ ਗਿਆ · ਨਿਮਾਣਾ ਸਕੱਤਰ",
                "The minutes are written in the passive: ਕਾਰਵਾਈ ਲਿਖੀ ਗਈ, ਫ਼ੈਸਲਾ ਲਿਆ ਗਿਆ, "
                "ਤਜਵੀਜ਼ਾਂ ਰੱਖੀਆਂ ਗਈਆਂ. The writer signs as ਨਿਮਾਣਾ (the undersigned), and the "
                "brief note at the end is ਸੰਖੇਪ.",
                [X("ਬੈਠਕ ਦੀ ਕਾਰਵਾਈ ਸੰਖੇਪ ਵਿੱਚ ਲਿਖੀ ਗਈ।", "baithak di karvaai sankhep vich likhi gai.", "The proceedings of the meeting were written in brief."),
                 X("ਦੋ ਤਜਵੀਜ਼ਾਂ ਰੱਖੀਆਂ ਗਈਆਂ।", "do tajvizan rakhian gaian.", "Two proposals were placed."),
                 X("ਨਿਮਾਣਾ ਸਕੱਤਰ, ਪਿੰਡ ਸੁਧਾਰ ਸਭਾ।", "nimana saktar, pind sudhar sabha.", "The undersigned secretary, Village Improvement Committee.")],
                [("ਦੋ ਤਜਵੀਜ਼ਾਂ ਰੱਖੇ ਗਏ।", "ਦੋ ਤਜਵੀਜ਼ਾਂ ਰੱਖੀਆਂ ਗਈਆਂ।", "ਤਜਵੀਜ਼ਾਂ is feminine plural: ਰੱਖੀਆਂ ਗਈਆਂ."),
                 ("ਕਾਰਵਾਈ ਲਿਖਿਆ ਗਿਆ।", "ਕਾਰਵਾਈ ਲਿਖੀ ਗਈ।", "ਕਾਰਵਾਈ is feminine: ਲਿਖੀ ਗਈ.")]),
              [D("ਪ੍ਰਧਾਨ", "ਕਾਰਵਾਈ ਲਿਖੀ ਗਈ?", "karvaai likhi gai?", "Were the proceedings written?"),
               D("ਸਕੱਤਰ", "ਹਾਂ, ਸੰਖੇਪ ਵਿੱਚ, ਅਤੇ ਦੋ ਤਜਵੀਜ਼ਾਂ ਵੀ ਰੱਖੀਆਂ ਗਈਆਂ।", "han, sankhep vich, ate do tajvizan vi rakhian gaian.", "Yes, in brief, and two proposals were also placed."),
               D("ਪ੍ਰਧਾਨ", "ਫ਼ੈਸਲਾ?", "faisla?", "The decision?"),
               D("ਸਕੱਤਰ", "ਫ਼ੈਸਲਾ ਲਿਆ ਗਿਆ। ਅਖ਼ੀਰ ਵਿੱਚ ਨਿਮਾਣਾ ਸਕੱਤਰ ਲਿਖਿਆ ਹੈ।", "faisla lia gia. akhir vich nimana saktar likhia hai.", "The decision was taken. At the end it says 'the undersigned secretary'.")],
              WS("Minutes worksheet", [
                  T("Write impersonally.", ["the proceedings were written in brief", "two proposals were placed"],
                    ["ਕਾਰਵਾਈ ਸੰਖੇਪ ਵਿੱਚ ਲਿਖੀ ਗਈ", "ਦੋ ਤਜਵੀਜ਼ਾਂ ਰੱਖੀਆਂ ਗਈਆਂ"]),
                  T("Close the record.", ["the decision was taken", "the undersigned secretary"],
                    ["ਫ਼ੈਸਲਾ ਲਿਆ ਗਿਆ", "ਨਿਮਾਣਾ ਸਕੱਤਰ"]),
              ])),
        ]},
        {"id": "B2+-U3", "title": "ਸਮਝੌਤਾ ਅਤੇ ਸ਼ਰਤਾਂ", "lessons": [
            L("ਇਕਰਾਰਨਾਮਾ",
              "A contract is ਇਕਰਾਰਨਾਮਾ, made of ਸ਼ਰਤਾਂ (conditions) and ਧਾਰਾਵਾਂ (clauses). It is "
              "signed, witnessed and dated: ਇਕਰਾਰਨਾਮੇ ਉੱਤੇ ਦਸਤਖ਼ਤ ਹੋਏ, ਗਵਾਹ ਵੀ ਲੱਗੇ, ਤਾਰੀਖ਼ ਲਿਖੀ "
              "ਗਈ.",
              [V("ਇਕਰਾਰਨਾਮਾ", "ikrarnama", "contract, agreement", "noun"),
               V("ਧਾਰਾ", "dhara", "clause", "noun"),
               V("ਗਵਾਹ", "gavah", "witness", "noun"),
               V("ਮਿਆਦ", "miad", "term, period", "noun"),
               V("ਨਵੀਨੀਕਰਨ", "navinikaran", "renewal", "noun")],
              G("Reading a contract",
                "ਇਕਰਾਰਨਾਮੇ ਦੀ ਧਾਰਾ ਚਾਰ · ਮਿਆਦ ਇੱਕ ਸਾਲ · ਨਵੀਨੀਕਰਨ ਹੋਵੇਗਾ",
                "The clause is named with ਦੀ ਧਾਰਾ: ਇਕਰਾਰਨਾਮੇ ਦੀ ਧਾਰਾ ਚਾਰ ਕਹਿੰਦੀ ਹੈ ਕਿ. The term "
                "takes ਮਿਆਦ, the renewal ਨਵੀਨੀਕਰਨ, and the promise is stated with the future: "
                "ਨਵੀਨੀਕਰਨ ਆਪਣੇ ਆਪ ਹੋਵੇਗਾ.",
                [X("ਇਕਰਾਰਨਾਮੇ ਦੀ ਧਾਰਾ ਚਾਰ ਕਹਿੰਦੀ ਹੈ ਕਿ ਮਿਆਦ ਇੱਕ ਸਾਲ ਹੈ।", "ikrarname di dhara char kahindi hai ki miad ikk sal hai.", "Clause four of the contract says that the term is one year."),
                 X("ਦੋ ਗਵਾਹਾਂ ਦੇ ਦਸਤਖ਼ਤ ਲੱਗੇ।", "do gavahan de dastakhat lagge.", "The signatures of two witnesses were affixed."),
                 X("ਨਵੀਨੀਕਰਨ ਆਪਣੇ ਆਪ ਨਹੀਂ ਹੋਵੇਗਾ।", "navinikaran apne aap nahin hovega.", "The renewal will not happen by itself.")],
                [("ਇਕਰਾਰਨਾਮੇ ਦੀ ਧਾਰਾ ਚਾਰ ਕਹਿੰਦੇ ਹਨ।", "ਇਕਰਾਰਨਾਮੇ ਦੀ ਧਾਰਾ ਚਾਰ ਕਹਿੰਦੀ ਹੈ।", "ਧਾਰਾ is feminine: ਕਹਿੰਦੀ ਹੈ."),
                 ("ਮਿਆਦ ਇੱਕ ਸਾਲ ਹਨ।", "ਮਿਆਦ ਇੱਕ ਸਾਲ ਹੈ।", "ਮਿਆਦ is singular: ਹੈ.")]),
              [D("ਠੇਕੇਦਾਰ", "ਇਕਰਾਰਨਾਮਾ ਪੜ੍ਹ ਲਿਆ?", "ikrarnama parh lia?", "Have you read the contract?"),
               D("ਕਿਸਾਨ", "ਧਾਰਾ ਚਾਰ ਪੜ੍ਹੀ: ਮਿਆਦ ਇੱਕ ਸਾਲ ਹੈ।", "dhara char parhi: miad ikk sal hai.", "I read clause four: the term is one year."),
               D("ਠੇਕੇਦਾਰ", "ਅਤੇ ਨਵੀਨੀਕਰਨ?", "ate navinikaran?", "And the renewal?"),
               D("ਕਿਸਾਨ", "ਨਵੀਨੀਕਰਨ ਲਿਖਤੀ ਹੋਵੇਗਾ, ਇਸ ਲਈ ਦੋ ਗਵਾਹ ਲੋੜੀਂਦੇ ਹਨ।", "navinikaran likhti hovega, is lai do gavah lorinde han.", "The renewal will be in writing, so two witnesses are needed.")],
              WS("Contract worksheet", [
                  T("Read the clause.", ["clause four says that the term is one year", "the signatures of two witnesses were affixed"],
                    ["ਧਾਰਾ ਚਾਰ ਕਹਿੰਦੀ ਹੈ ਕਿ ਮਿਆਦ ਇੱਕ ਸਾਲ ਹੈ", "ਦੋ ਗਵਾਹਾਂ ਦੇ ਦਸਤਖ਼ਤ ਲੱਗੇ"]),
                  T("Speak about renewal.", ["the renewal will not happen by itself", "two witnesses are needed"],
                    ["ਨਵੀਨੀਕਰਨ ਆਪਣੇ ਆਪ ਨਹੀਂ ਹੋਵੇਗਾ", "ਦੋ ਗਵਾਹ ਲੋੜੀਂਦੇ ਹਨ"]),
              ])),
            L("ਸ਼ਰਤਾਂ ਦੀ ਪਾਲਣਾ",
              "Conditions are kept or broken: ਸ਼ਰਤਾਂ ਦੀ ਪਾਲਣਾ ਹੋਈ (the conditions were kept), ਜੇ "
              "ਦੇਰੀ ਹੋਈ ਤਾਂ ਜੁਰਮਾਨਾ ਲੱਗੇਗਾ (if there is a delay, a penalty will apply). ਲਾਗੂ ਹੋਣਾ "
              "says a rule comes into force.",
              [V("ਪਾਲਣਾ", "palna", "compliance, keeping", "noun"),
               V("ਜੁਰਮਾਨਾ", "jurmana", "penalty, fine", "noun"),
               V("ਲਾਗੂ", "lagu", "in force, applicable", "adjective"),
               V("ਛੋਟ", "chhott", "exemption, concession", "noun"),
               V("ਸੂਚਨਾ", "suchna", "information, notice", "noun")],
              G("Conditions and penalties",
                "ਸ਼ਰਤਾਂ ਦੀ ਪਾਲਣਾ ਹੋਈ · ਜੇ ਦੇਰੀ ਹੋਈ ਤਾਂ ਜੁਰਮਾਨਾ ਲੱਗੇਗਾ · ਨੋਟਿਸ ਲਾਗੂ ਹੋਵੇਗਾ",
                "ਪਾਲਣਾ (compliance) is feminine: ਪਾਲਣਾ ਹੋਈ. The penalty is announced with the "
                "conditional ਜੇ … ਤਾਂ, the rule with ਲਾਗੂ ਹੋਣਾ, and any concession with ਛੋਟ ਦੇਣੀ. "
                "ਸੂਚਨਾ ਦੇਣੀ means to give notice.",
                [X("ਸਾਰੀਆਂ ਸ਼ਰਤਾਂ ਦੀ ਪਾਲਣਾ ਹੋਈ।", "sarian shartaan di palna hoi.", "All the conditions were kept."),
                 X("ਜੇ ਦੇਰੀ ਹੋਈ ਤਾਂ ਜੁਰਮਾਨਾ ਲੱਗੇਗਾ।", "je deri hoi tan jurmana lagega.", "If there is a delay, a penalty will apply."),
                 X("ਦਸ ਦਿਨਾਂ ਦੀ ਸੂਚਨਾ ਦਿੱਤੀ ਜਾਵੇ।", "das dinan di suchna ditti jave.", "Ten days' notice should be given.")],
                [("ਸਾਰੀਆਂ ਸ਼ਰਤਾਂ ਦੀ ਪਾਲਣਾ ਹੋਇਆ।", "ਸਾਰੀਆਂ ਸ਼ਰਤਾਂ ਦੀ ਪਾਲਣਾ ਹੋਈ।", "ਪਾਲਣਾ is feminine: ਹੋਈ."),
                 ("ਜੇ ਦੇਰੀ ਹੋਵੇਗੀ ਤਾਂ ਜੁਰਮਾਨਾ ਲੱਗੇਗਾ।", "ਜੇ ਦੇਰੀ ਹੋਈ ਤਾਂ ਜੁਰਮਾਨਾ ਲੱਗੇਗਾ।", "The conditional uses the past form ਹੋਈ.")]),
              [D("ਅਧਿਕਾਰੀ", "ਸ਼ਰਤਾਂ ਦੀ ਪਾਲਣਾ ਹੋਈ?", "shartaan di palna hoi?", "Were the conditions kept?"),
               D("ਠੇਕੇਦਾਰ", "ਪਾਲਣਾ ਹੋਈ, ਪਰ ਤਿੰਨ ਦਿਨ ਦੇਰੀ ਹੋਈ।", "palna hoi, par tinn din deri hoi.", "They were kept, but there was a delay of three days."),
               D("ਅਧਿਕਾਰੀ", "ਫਿਰ ਜੁਰਮਾਨਾ?", "phir jurmana?", "Then the penalty?"),
               D("ਠੇਕੇਦਾਰ", "ਜੁਰਮਾਨਾ ਲੱਗੇਗਾ, ਪਰ ਮੈਂ ਛੋਟ ਲਈ ਅਰਜ਼ੀ ਦਿੰਦਾ ਹਾਂ।", "jurmana lagega, par main chhott lai arzi dinda han.", "The penalty will apply, but I am applying for a concession.")],
              WS("Conditions worksheet", [
                  T("Report compliance.", ["all the conditions were kept", "there was a delay of three days"],
                    ["ਸਾਰੀਆਂ ਸ਼ਰਤਾਂ ਦੀ ਪਾਲਣਾ ਹੋਈ", "ਤਿੰਨ ਦਿਨ ਦੇਰੀ ਹੋਈ"]),
                  T("State the penalty.", ["if there is a delay, a penalty will apply", "ten days' notice should be given"],
                    ["ਜੇ ਦੇਰੀ ਹੋਈ ਤਾਂ ਜੁਰਮਾਨਾ ਲੱਗੇਗਾ", "ਦਸ ਦਿਨਾਂ ਦੀ ਸੂਚਨਾ ਦਿੱਤੀ ਜਾਵੇ"]),
              ])),
            L("ਭੁਗਤਾਨ ਅਤੇ ਬਕਾਇਆ",
              "Money at the end of work needs exact words: ਭੁਗਤਾਨ (payment), ਬਕਾਇਆ (arrears), "
              "ਕਿਸ਼ਤਾਂ (instalments), ਵਿਆਜ (interest). The polite chase is ਬਕਾਇਆ ਦੀ ਯਾਦ ਦਿਵਾਉਂਦੇ "
              "ਹਾਂ, and the deadline is ਇਸ ਮਹੀਨੇ ਦੇ ਅੰਦਰ.",
              [V("ਬਕਾਇਆ", "bakaaia", "arrears, outstanding", "noun"),
               V("ਕਿਸ਼ਤ", "kisht", "instalment", "noun"),
               V("ਵਿਆਜ", "viaj", "interest", "noun"),
               V("ਯਾਦ", "yad", "reminder, memory", "noun"),
               V("ਅੰਦਰ", "andar", "within", "postposition")],
              G("Asking for payment",
                "ਬਕਾਇਆ ਦੀ ਯਾਦ ਦਿਵਾਉਂਦੇ ਹਾਂ · ਇਸ ਮਹੀਨੇ ਦੇ ਅੰਦਰ · ਤਿੰਨ ਕਿਸ਼ਤਾਂ ਵਿੱਚ",
                "The reminder is framed softly: ਯਾਦ ਦਿਵਾਉਂਦੇ ਹਾਂ (we remind you). The deadline "
                "takes ਅੰਦਰ or ਤੱਕ, the instalments take ਵਿੱਚ: ਤਿੰਨ ਕਿਸ਼ਤਾਂ ਵਿੱਚ ਭੁਗਤਾਨ ਹੋਵੇ, and "
                "the last step is stated plainly: ਬਕਾਇਆ ਬਾਕੀ ਹੈ.",
                [X("ਬਕਾਇਆ ਦੀ ਯਾਦ ਦਿਵਾਉਂਦੇ ਹਾਂ।", "bakaaia di yad divaunde han.", "We remind you of the arrears."),
                 X("ਭੁਗਤਾਨ ਇਸ ਮਹੀਨੇ ਦੇ ਅੰਦਰ ਹੋਵੇ।", "bhugtan is mahine de andar hove.", "The payment should be within this month."),
                 X("ਰਕਮ ਤਿੰਨ ਕਿਸ਼ਤਾਂ ਵਿੱਚ ਦਿੱਤੀ ਜਾਵੇ।", "rakam tinn kishtan vich ditti jave.", "The amount should be paid in three instalments.")],
                [("ਭੁਗਤਾਨ ਅੰਦਰ ਇਸ ਮਹੀਨੇ ਹੋਵੇ।", "ਭੁਗਤਾਨ ਇਸ ਮਹੀਨੇ ਦੇ ਅੰਦਰ ਹੋਵੇ।", "The postposition follows the phrase: ਦੇ ਅੰਦਰ."),
                 ("ਤਿੰਨ ਕਿਸ਼ਤਾਂ ਵਿੱਚ ਦਿੱਤਾ ਜਾਵੇਗਾ।", "ਤਿੰਨ ਕਿਸ਼ਤਾਂ ਵਿੱਚ ਦਿੱਤੀ ਜਾਵੇ।", "A request keeps the subjunctive ਜਾਵੇ.")]),
              [D("ਠੇਕੇਦਾਰ", "ਬਕਾਇਆ ਕਦੋਂ ਤੱਕ ਮਿਲੇਗਾ?", "bakaaia kadon takk milega?", "By when will the arrears come?"),
               D("ਅਧਿਕਾਰੀ", "ਭੁਗਤਾਨ ਇਸ ਮਹੀਨੇ ਦੇ ਅੰਦਰ ਹੋਵੇ।", "bhugtan is mahine de andar hove.", "The payment should be within this month."),
               D("ਠੇਕੇਦਾਰ", "ਪੂਰੀ ਰਕਮ ਇੱਕ ਵਾਰ?", "puri rakam ikk var?", "The whole amount at once?"),
               D("ਅਧਿਕਾਰੀ", "ਨਹੀਂ, ਤਿੰਨ ਕਿਸ਼ਤਾਂ ਵਿੱਚ, ਅਤੇ ਵਿਆਜ ਦੀ ਗੱਲ ਵੱਖਰੀ ਹੈ।", "nahin, tinn kishtan vich, ate viaj di gal vakhri hai.", "No, in three instalments, and the question of interest is separate.")],
              WS("Payment worksheet", [
                  T("Remind the office.", ["we remind you of the arrears", "the payment should be within this month"],
                    ["ਬਕਾਇਆ ਦੀ ਯਾਦ ਦਿਵਾਉਂਦੇ ਹਾਂ", "ਭੁਗਤਾਨ ਇਸ ਮਹੀਨੇ ਦੇ ਅੰਦਰ ਹੋਵੇ"]),
                  T("Arrange the amount.", ["in three instalments", "the question of interest is separate"],
                    ["ਤਿੰਨ ਕਿਸ਼ਤਾਂ ਵਿੱਚ", "ਵਿਆਜ ਦੀ ਗੱਲ ਵੱਖਰੀ ਹੈ"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("The Green Revolution in India began in the 1960s, when high-yielding varieties of "
                 "wheat arrived together with chemical fertiliser, irrigation and a new price "
                 "policy. The work is associated above all with M. S. Swaminathan, who brought "
                 "Norman Borlaug's varieties into Indian fields and built the research and seed "
                 "systems around them. Punjab, with canal water and tube wells, took to the new "
                 "seed faster than any other state and became the country's granary. The language "
                 "of that change is still spoken in Punjabi: ਝਾੜੀ, ਕੁਇੰਟਲ, ਮੰਡੀ, ਆੜ੍ਹਤੀ, and a "
                 "farmer's account book that compares one year with the next."),
        source_url="https://en.wikipedia.org/wiki/Green_Revolution_in_India",
        reading=("ਸਾਠ ਦੇ ਦਹਾਕੇ ਵਿੱਚ ਪੰਜਾਬ ਦੇ ਖੇਤਾਂ ਵਿੱਚ ਨਵੀਂ ਕਿਸਮ ਆਈ। ਪਹਿਲਾਂ ਕਣਕ ਦੀ ਝਾੜੀ ਘੱਟ ਸੀ "
                 "ਅਤੇ ਖਾਦ ਦਾ ਖ਼ਰਚ ਵੀ ਘੱਟ। ਫਿਰ ਬੀਜ, ਪਾਣੀ ਅਤੇ ਖਾਦ ਦਾ ਹਿਸਾਬ ਬਦਲ ਗਿਆ: ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ "
                 "ਝਾੜੀ ਦੁੱਗਣੀ ਹੋ ਗਈ, ਪਰ ਖ਼ਰਚ ਵੀ ਵੱਧ ਗਿਆ। ਮੰਡੀ ਵਿੱਚ ਭਾਅ ਤੈਅ ਕੀਤਾ ਗਿਆ ਅਤੇ ਭੁਗਤਾਨ ਦੀ "
                 "ਮਿਆਦ ਸੱਤ ਦਿਨ ਰੱਖੀ ਗਈ। ਅੱਜ ਹਰ ਹੈਕਟੇਅਰ ਦਾ ਹਿਸਾਬ ਰੱਖਿਆ ਜਾਂਦਾ ਹੈ: ਬੀਜ ਕਿੰਨਾ, ਪਾਣੀ "
                 "ਕਿੰਨਾ, ਝਾੜੀ ਕਿੰਨੀ। ਅੰਕੜਿਆਂ ਅਨੁਸਾਰ ਇਹ ਕ੍ਰਾਂਤੀ ਜ਼ਮੀਨ ਦੀ ਨਹੀਂ, ਹਿਸਾਬ ਦੀ ਸੀ।"),
        reading_gloss=("In the sixties a new variety came into the fields of Punjab. Earlier the "
                       "wheat yield was low and the spending on fertiliser was low too. Then the "
                       "arithmetic of seed, water and fertiliser changed: the yield doubled "
                       "compared with the previous year, but the cost rose as well. In the market "
                       "the price was settled and the payment term was kept at seven days. Today "
                       "the account is kept for every hectare: how much seed, how much water, how "
                       "much yield. Going by the figures, this revolution was not of land but of "
                       "arithmetic."),
        listening=("ਅਧਿਕਾਰੀ: ਇਸ ਸਾਲ ਦੀ ਝਾੜੀ ਦੱਸੋ। ਕਿਸਾਨ: ਔਸਤ ਚਾਲੀ ਕੁਇੰਟਲ ਪ੍ਰਤੀ ਹੈਕਟੇਅਰ ਹੈ। ਅਧਿਕਾਰੀ: "
                   "ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ? ਕਿਸਾਨ: ਛੇ ਕੁਇੰਟਲ ਵੱਧ। ਅਧਿਕਾਰੀ: ਖ਼ਰਚਾ? ਕਿਸਾਨ: ਖਾਦ ਦਾ ਖ਼ਰਚ ਵੀ ਵੱਧ "
                   "ਹੈ, ਪਰ ਮੰਡੀ ਦੇ ਮੁਕਾਬਲੇ ਭਾਅ ਘੱਟ ਹੈ। ਅਧਿਕਾਰੀ: ਅੰਕੜੇ ਰਿਪੋਰਟ ਵਿੱਚ ਲਿਖੋ, ਅਤੇ ਬਕਾਇਆ "
                   "ਦੀ ਯਾਦ ਵੀ ਦਿਵਾਓ।"),
        listening_gloss=("Officer: Tell me this year's yield. Farmer: The average is forty quintals "
                         "per hectare. Officer: Compared with last year? Farmer: Six quintals "
                         "more. Officer: The cost? Farmer: The fertiliser cost is higher too, but "
                         "the price is lower than the market's. Officer: Write the figures in the "
                         "report, and remind them about the arrears as well."),
        voice_tag=VOICE,
        idioms=[
            ("ਹਰ ਹੈਕਟੇਅਰ", "for every hectare", "per hectare, the standard farm measure"),
            ("ਝਾੜੀ ਵੱਧ", "the yield is more", "the crop has done well"),
            ("ਮੰਡੀ ਦੇ ਮੁਕਾਬਲੇ", "compared with the market", "measured against the going rate"),
            ("ਕਾਰਵਾਈ ਹੋਈ", "the proceedings took place", "the matter was formally handled"),
            ("ਧਾਰਾ ਅਨੁਸਾਰ", "according to the clause", "as the contract says"),
            ("ਯਾਦ ਦਿਵਾਉਂਦੇ ਹਾਂ", "we give a reminder", "the polite opening of a payment chase"),
            ("ਮਿਆਦ ਲੰਘ ਗਈ", "the term has passed", "the deadline is over"),
            ("ਅੰਕੜੇ ਬੋਲਦੇ ਹਨ", "the figures speak", "the numbers settle the argument"),
            ("ਹਵਾਲਾ ਦੇਣਾ", "to give a reference", "to cite a source or a report"),
            ("ਮਨਜ਼ੂਰੀ ਬਣਦੀ ਹੈ", "the approval is due", "the rules entitle this to be approved"),
        ],
        mistakes=[
            ("ਬੇਨਤੀ ਹੈ ਕਿ ਮੁਰੰਮਤ ਕਰਵਾਈ ਜਾਵੇਗੀ।", "ਬੇਨਤੀ ਹੈ ਕਿ ਮੁਰੰਮਤ ਕਰਵਾਈ ਜਾਵੇ।", "A request after ਕਿ takes the subjunctive ਜਾਵੇ."),
            ("ਸਾਰੀਆਂ ਸ਼ਰਤਾਂ ਦੀ ਪਾਲਣਾ ਹੋਇਆ।", "ਸਾਰੀਆਂ ਸ਼ਰਤਾਂ ਦੀ ਪਾਲਣਾ ਹੋਈ।", "ਪਾਲਣਾ is feminine: ਹੋਈ."),
            ("ਪਿਛਲੇ ਸਾਲ ਤੋਂ ਝਾੜੀ ਵੱਧ ਹੈ।", "ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਝਾੜੀ ਵੱਧ ਹੈ।", "Comparison takes ਨਾਲੋਂ."),
        ],
        task_title="Write a one-page official note, in Punjabi",
        task_instructions=("Write a Punjabi note of ten to twelve sentences for a department: state "
                           "the yield per hectare and compare it with last year, quote one line "
                           "from a report with ਦੱਸਿਆ ਗਿਆ ਹੈ ਕਿ, report what an officer said with the "
                           "pronoun shifted to ਉਹ, list two conditions of a contract with ਧਾਰਾ, and "
                           "close by reminding the office of the arrears with ਯਾਦ ਦਿਵਾਉਂਦੇ ਹਾਂ."),
    ),
    "test": [
        ("translate_en", "Say: the account is kept for every hectare.", "ਹਰ ਹੈਕਟੇਅਰ ਦਾ ਹਿਸਾਬ ਰੱਖਿਆ ਜਾਂਦਾ ਹੈ।"),
        ("translate_pa", "ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ ਝਾੜੀ ਵੱਧ ਹੈ।", "The yield is higher than last year."),
        ("multiple_choice", "Which sentence reports an official's words?", "ਅਧਿਕਾਰੀ ਨੇ ਦੱਸਿਆ ਕਿ ਉਹ ਜਾਂਚ ਕਰੇਗਾ।"),
        ("fill_in_the_blank", "ਬੇਨਤੀ ਹੈ ਕਿ ਪਾਈਪ ਦੀ ਮੁਰੰਮਤ ਕਰਵਾਈ ___।", "ਜਾਵੇ"),
        ("word_selection", "Select the Punjabi for 'arrears'.", "ਬਕਾਇਆ"),
        ("error_correction", "ਸਾਰੀਆਂ ਸ਼ਰਤਾਂ ਦੀ ਪਾਲਣਾ ਹੋਇਆ।", "ਸਾਰੀਆਂ ਸ਼ਰਤਾਂ ਦੀ ਪਾਲਣਾ ਹੋਈ।"),
        ("dialogue_completion", "Complete: ਭੁਗਤਾਨ ___ ਮਹੀਨੇ ਦੇ ਅੰਦਰ ਹੋਵੇ। (within this month)", "ਇਸ"),
        ("matching", "Match ਧਾਰਾ to its meaning.", "clause"),
        ("reading_comprehension", "ਅੰਕੜਿਆਂ ਅਨੁਸਾਰ ਕ੍ਰਾਂਤੀ ਕਿਸ ਦੀ ਸੀ?", "of arithmetic, the way the account was kept"),
        ("inference", "ਮੰਡੀ ਦੇ ਮੁਕਾਬਲੇ ਭਾਅ ਘੱਟ ਹੈ। — what is the farmer really saying?", "the price he gets is below the market rate"),
        ("main_idea", "ਝਾੜੀ ਦੁੱਗਣੀ ਹੋਈ, ਪਰ ਖ਼ਰਚ ਵੀ ਵੱਧ ਗਿਆ। — what is this sentence?", "the gain and its cost together"),
        ("detail_identification", "ਭੁਗਤਾਨ ਦੀ ਮਿਆਦ ਕਿੰਨੀ ਰੱਖੀ ਗਈ?", "seven days"),
    ],
}

HALFSTEPS["C1+"] = {
    "native": NATIVE,
    "title": "%s C1+ — Heer, the epic and the review" % NAME,
    "goals": [
        "Describe the shape of a long poem: episode, turn, ending, and the idiom it is carried in",
        "Compare two tellings of one story and say what each version gains or loses",
        "Write a review that holds a claim to its evidence, and answer a reader who disagrees",
    ],
    "units": [
        {"id": "C1+-U1", "title": "ਕਥਾ ਅਤੇ ਪਾਤਰ", "lessons": [
            L("ਕਥਾ ਦਾ ਢਾਂਚਾ",
              "A folk narrative is described by its stages: ਭੂਮਿਕਾ (opening), ਮੋੜ (turn), ਵਿਛੋੜਾ "
              "(separation), ਅੰਤ (ending). ਦਾਰੂ (the mover of the plot) is what keeps the story "
              "walking, and it is described with ਕਰਨ ਵਾਲੀ ਸ਼ਕਤੀ or ਦਾਰੂ ਹੁੰਦਾ ਹੈ.",
              [V("ਕਥਾ", "katha", "tale, narrative", "noun"),
               V("ਢਾਂਚਾ", "dhancha", "structure", "noun"),
               V("ਵਿਛੋੜਾ", "vichhorha", "separation", "noun"),
               V("ਦਾਰੂ", "daru", "the moving force of a plot", "noun"),
               V("ਮੋੜ", "mor", "turn", "noun")],
              G("Describing the shape of a story",
                "ਕਥਾ ਦੇ ਚਾਰ ਹਿੱਸੇ ਹਨ · ਦਾਰੂ ਇਹ ਹੈ ਕਿ · ਵਿਛੋੜੇ ਤੋਂ ਬਾਅਦ",
                "The stages are listed with ਦੇ ਹਿੱਸੇ ਹਨ, the moving force is introduced with ਦਾਰੂ "
                "ਇਹ ਹੈ ਕਿ, and the sequence takes ਤੋਂ ਬਾਅਦ: ਵਿਛੋੜੇ ਤੋਂ ਬਾਅਦ ਕਥਾ ਹਨੇਰੀ ਪਾਸੇ ਜਾਂਦੀ "
                "ਹੈ. The essayistic present (ਜਾਂਦੀ ਹੈ) keeps the story alive in the review.",
                [X("ਕਥਾ ਦਾ ਢਾਂਚਾ ਤਿੰਨ ਹਿੱਸਿਆਂ ਵਿੱਚ ਬਣਦਾ ਹੈ।", "katha da dhancha tinn hissian vich bandda hai.", "The structure of the tale is built in three parts."),
                 X("ਦਾਰੂ ਇਹ ਹੈ ਕਿ ਹੀਰ ਨੂੰ ਉਹਦੀ ਮਰਜ਼ੀ ਨਾਲ ਨਹੀਂ ਵਿਆਹਿਆ ਜਾਂਦਾ।", "daru ih hai ki Hir nun uhdi marzi nal nahin viahia janda.", "The moving force is that Heer is not married off by her own wish."),
                 X("ਵਿਛੋੜੇ ਤੋਂ ਬਾਅਦ ਕਥਾ ਦੀ ਰਫ਼ਤਾਰ ਬਦਲ ਜਾਂਦੀ ਹੈ।", "vichhorhe to baad katha di raftar badal jandi hai.", "After the separation the pace of the tale changes.")],
                [("ਕਥਾ ਦਾ ਢਾਂਚਾ ਤਿੰਨ ਹਿੱਸੇ ਬਣਦਾ ਹੈ।", "ਕਥਾ ਦਾ ਢਾਂਚਾ ਤਿੰਨ ਹਿੱਸਿਆਂ ਵਿੱਚ ਬਣਦਾ ਹੈ।", "Structure is described with ਵਿੱਚ."),
                 ("ਵਿਛੋੜਾ ਤੋਂ ਬਾਅਦ ਕਥਾ ਬਦਲਦੀ ਹੈ।", "ਵਿਛੋੜੇ ਤੋਂ ਬਾਅਦ ਕਥਾ ਬਦਲਦੀ ਹੈ।", "The oblique form is ਵਿਛੋੜੇ before ਤੋਂ ਬਾਅਦ.")]),
              [D("ਸੰਪਾਦਕ", "ਕਥਾ ਦਾ ਢਾਂਚਾ ਕੀ ਹੈ?", "katha da dhancha ki hai?", "What is the structure of the tale?"),
               D("ਸਮੀਖਿਆਕਾਰ", "ਤਿੰਨ ਹਿੱਸੇ: ਭੂਮਿਕਾ, ਵਿਛੋੜਾ, ਅੰਤ।", "tinn hisse: bhumika, vichhorha, ant.", "Three parts: opening, separation, ending."),
               D("ਸੰਪਾਦਕ", "ਦਾਰੂ ਕੀ ਹੈ?", "daru ki hai?", "What is the moving force?"),
               D("ਸਮੀਖਿਆਕਾਰ", "ਦਾਰੂ ਇਹ ਹੈ ਕਿ ਮਰਜ਼ੀ ਕਿਸੇ ਦੀ ਨਹੀਂ ਪੁੱਛੀ ਜਾਂਦੀ।", "daru ih hai ki marzi kise di nahin puchhi jandi.", "The force is that nobody asks anybody's wish.")],
              WS("Structure worksheet", [
                  T("Name the parts.", ["opening, separation, ending", "the structure of the tale is built in three parts"],
                    ["ਭੂਮਿਕਾ, ਵਿਛੋੜਾ, ਅੰਤ", "ਕਥਾ ਦਾ ਢਾਂਚਾ ਤਿੰਨ ਹਿੱਸਿਆਂ ਵਿੱਚ ਬਣਦਾ ਹੈ"]),
                  T("State the force.", ["the moving force is that Heer is not married off by her own wish", "after the separation the pace changes"],
                    ["ਦਾਰੂ ਇਹ ਹੈ ਕਿ ਹੀਰ ਨੂੰ ਉਹਦੀ ਮਰਜ਼ੀ ਨਾਲ ਨਹੀਂ ਵਿਆਹਿਆ ਜਾਂਦਾ", "ਵਿਛੋੜੇ ਤੋਂ ਬਾਅਦ ਰਫ਼ਤਾਰ ਬਦਲ ਜਾਂਦੀ ਹੈ"]),
              ])),
            L("ਪਾਤਰ ਦੀ ਬਣਾਵਟ",
              "A character is built out of speech, decision and silence: ਹੀਰ ਬੋਲਦੀ ਹੈ, ਰਾਂਝਾ ਸਹਿੰਦਾ "
              "ਹੈ, ਕਾਹਨੂੰਵਾਨ ਦਖ਼ਲ ਦਿੰਦਾ ਹੈ. The review describes this with ਰਾਹੀਂ (through): ਬੋਲੀ "
              "ਰਾਹੀਂ ਪਾਤਰ ਬਣਦੀ ਹੈ.",
              [V("ਪਾਤਰ", "pattar", "character", "noun"),
               V("ਬੋਲੀ", "boli", "speech, idiom", "noun"),
               V("ਦਖ਼ਲ", "dakhhal", "intervention, interference", "noun"),
               V("ਰਾਹੀਂ", "rahin", "through, by means of", "postposition"),
               V("ਸੰਜਮ", "sanjam", "restraint", "noun")],
              G("Building a character in a review",
                "ਬੋਲੀ ਰਾਹੀਂ ਬਣਦੀ ਹੈ · ਦਖ਼ਲ ਦਿੰਦਾ ਹੈ · ਸੰਜਮ ਨਾਲ ਬੋਲਦੀ ਹੈ",
                "The means takes ਰਾਹੀਂ: ਬੋਲੀ ਰਾਹੀਂ. The interference takes ਦਖ਼ਲ ਦੇਣਾ, restraint "
                "takes ਸੰਜਮ ਨਾਲ, and the claim about a character is hedged with ਲੱਗਦਾ ਹੈ: ਹੀਰ "
                "ਸੰਜਮ ਵਾਲੀ ਲੱਗਦੀ ਹੈ.",
                [X("ਹੀਰ ਦੀ ਬਣਾਵਟ ਬੋਲੀ ਰਾਹੀਂ ਬਣਦੀ ਹੈ।", "Hir di banavat boli rahin banddi hai.", "Heer's character is built through speech."),
                 X("ਕਾਹਨੂੰਵਾਨ ਵਾਰ-ਵਾਰ ਦਖ਼ਲ ਦਿੰਦਾ ਹੈ।", "Kahnuwan var-var dakhhal dinda hai.", "Kahnuwan intervenes again and again."),
                 X("ਰਾਂਝਾ ਸੰਜਮ ਨਾਲ ਸਹਿੰਦਾ ਲੱਗਦਾ ਹੈ।", "Ranjha sanjam nal sahinda lagda hai.", "Ranjha seems to bear it with restraint.")],
                [("ਹੀਰ ਦੀ ਬਣਾਵਟ ਬੋਲੀ ਨਾਲ ਬਣਦੀ ਹੈ ਰਾਹੀਂ।", "ਹੀਰ ਦੀ ਬਣਾਵਟ ਬੋਲੀ ਰਾਹੀਂ ਬਣਦੀ ਹੈ।", "The means is ਰਾਹੀਂ, placed after the noun."),
                 ("ਕਾਹਨੂੰਵਾਨ ਦਖ਼ਲ ਕਰਦਾ ਦਿੰਦਾ ਹੈ।", "ਕਾਹਨੂੰਵਾਨ ਦਖ਼ਲ ਦਿੰਦਾ ਹੈ।", "The phrase is ਦਖ਼ਲ ਦੇਣਾ, one verb.")]),
              [D("ਸੰਪਾਦਕ", "ਹੀਰ ਦੀ ਬਣਾਵਟ ਕਿਵੇਂ ਬਣਦੀ ਹੈ?", "Hir di banavat kiven banddi hai?", "How is Heer's character built?"),
               D("ਸਮੀਖਿਆਕਾਰ", "ਬੋਲੀ ਰਾਹੀਂ। ਉਹ ਸੰਜਮ ਨਾਲ ਬੋਲਦੀ ਹੈ ਅਤੇ ਫੈਸਲਾ ਵੀ ਦਿੰਦੀ ਹੈ।", "boli rahin. uh sanjam nal boldi hai ate faisla vi dindi hai.", "Through speech. She speaks with restraint and also takes a decision."),
               D("ਸੰਪਾਦਕ", "ਅਤੇ ਬਾਕੀ ਪਾਤਰ?", "ate baki pattar?", "And the other characters?"),
               D("ਸਮੀਖਿਆਕਾਰ", "ਕਾਹਨੂੰਵਾਨ ਦਖ਼ਲ ਦਿੰਦਾ ਹੈ, ਰਾਂਝਾ ਸਹਿੰਦਾ ਹੈ।", "Kahnuwan dakhhal dinda hai, Ranjha sahinda hai.", "Kahnuwan intervenes, Ranjha endures.")],
              WS("Character worksheet", [
                  T("Say how it is built.", ["Heer's character is built through speech", "she speaks with restraint"],
                    ["ਹੀਰ ਦੀ ਬਣਾਵਟ ਬੋਲੀ ਰਾਹੀਂ ਬਣਦੀ ਹੈ", "ਉਹ ਸੰਜਮ ਨਾਲ ਬੋਲਦੀ ਹੈ"]),
                  T("Describe the others.", ["Kahnuwan intervenes again and again", "Ranjha seems to bear it with restraint"],
                    ["ਕਾਹਨੂੰਵਾਨ ਵਾਰ-ਵਾਰ ਦਖ਼ਲ ਦਿੰਦਾ ਹੈ", "ਰਾਂਝਾ ਸੰਜਮ ਨਾਲ ਸਹਿੰਦਾ ਲੱਗਦਾ ਹੈ"]),
              ])),
            L("ਲੋਕ-ਕਥਾ ਦੀ ਬੋਲੀ",
              "The folk idiom lives in fixed phrases: ਮੇਲਾ ਹੋ ਗਿਆ, ਹਾਲ ਵੀ ਪੁੱਛਿਆ, ਦਿਲ ਦੀ ਗੱਲ, ਰੰਗ "
              "ਬਦਲ ਗਿਆ. A review quotes one such line and explains what it carries: ਇੱਕ ਸਤਰ ਵਿੱਚ ਪੂਰਾ "
              "ਰਿਸ਼ਤਾ ਆ ਜਾਂਦਾ ਹੈ.",
              [V("ਲੋਕ-ਕਥਾ", "lok-katha", "folk tale", "noun"),
               V("ਸਤਰ", "satar", "line of verse", "noun"),
               V("ਰਿਸ਼ਤਾ", "rishta", "relation, connection", "noun"),
               V("ਛੰਦ", "chhand", "metre", "noun"),
               V("ਮੁਹਾਵਰਾ", "muhavra", "idiom", "noun")],
              G("Quoting the folk line",
                "ਇੱਕ ਸਤਰ ਵਿੱਚ ਪੂਰਾ ਰਿਸ਼ਤਾ ਆ ਜਾਂਦਾ ਹੈ · ਮੁਹਾਵਰਾ ਕੰਮ ਕਰਦਾ ਹੈ · ਛੰਦ ਬਦਲ ਜਾਂਦਾ ਹੈ",
                "A quoted line is introduced with ਸਤਰ (line) or ਮੁਹਾਵਰਾ (idiom), and its work is "
                "described with ਕੰਮ ਕਰਨਾ or ਆ ਜਾਣਾ: ਇੱਕ ਸਤਰ ਵਿੱਚ ਪੂਰਾ ਰਿਸ਼ਤਾ ਆ ਜਾਂਦਾ ਹੈ. Metre is "
                "ਛੰਦ, which ਬਦਲ ਜਾਂਦਾ ਹੈ as the episode moves.",
                [X("ਇੱਕ ਸਤਰ ਵਿੱਚ ਪੂਰਾ ਰਿਸ਼ਤਾ ਆ ਜਾਂਦਾ ਹੈ।", "ikk satar vich pura rishta a janda hai.", "In one line the whole relationship arrives."),
                 X("ਮੁਹਾਵਰਾ ਇੱਥੇ ਕੰਮ ਕਰਦਾ ਹੈ।", "muhavra itthe kam karda hai.", "The idiom does its work here."),
                 X("ਵਿਛੋੜੇ ਵਿੱਚ ਛੰਦ ਬਦਲ ਜਾਂਦਾ ਹੈ।", "vichhorhe vich chhand badal janda hai.", "In the separation the metre changes.")],
                [("ਇੱਕ ਸਤਰ ਵਿੱਚ ਪੂਰਾ ਰਿਸ਼ਤਾ ਆਉਂਦਾ ਕਰਦਾ ਹੈ।", "ਇੱਕ ਸਤਰ ਵਿੱਚ ਪੂਰਾ ਰਿਸ਼ਤਾ ਆ ਜਾਂਦਾ ਹੈ।", "The phrase is ਆ ਜਾਣਾ."),
                 ("ਛੰਦ ਬਦਲ ਕੀਤਾ।", "ਛੰਦ ਬਦਲ ਜਾਂਦਾ ਹੈ।", "A change on its own takes ਜਾਂਦਾ ਹੈ.")]),
              [D("ਸੰਪਾਦਕ", "ਕੀ ਸਤਰ ਪੇਸ਼ ਕਰੀਏ?", "ki satar pesh karie?", "Which line shall we present?"),
               D("ਸਮੀਖਿਆਕਾਰ", "ਇੱਕ ਸਤਰ ਕਾਫ਼ੀ ਹੈ: ਉਸ ਵਿੱਚ ਪੂਰਾ ਰਿਸ਼ਤਾ ਆ ਜਾਂਦਾ ਹੈ।", "ikk satar kafi hai: us vich pura rishta a janda hai.", "One line is enough: in it the whole relationship arrives."),
               D("ਸੰਪਾਦਕ", "ਮੁਹਾਵਰੇ ਬਾਰੇ ਕੀ ਲਿਖੀਏ?", "muhavare bare ki likhie?", "What shall we write about the idiom?"),
               D("ਸਮੀਖਿਆਕਾਰ", "ਕਿ ਮੁਹਾਵਰਾ ਕੰਮ ਕਰਦਾ ਹੈ, ਅਤੇ ਛੰਦ ਵਿਛੋੜੇ ਵਿੱਚ ਬਦਲ ਜਾਂਦਾ ਹੈ।", "ki muhavra kam karda hai, ate chhand vichhorhe vich badal janda hai.", "That the idiom does its work, and the metre changes in the separation.")],
              WS("Idiom worksheet", [
                  T("Quote the line.", ["in one line the whole relationship arrives", "the idiom does its work here"],
                    ["ਇੱਕ ਸਤਰ ਵਿੱਚ ਪੂਰਾ ਰਿਸ਼ਤਾ ਆ ਜਾਂਦਾ ਹੈ", "ਮੁਹਾਵਰਾ ਇੱਥੇ ਕੰਮ ਕਰਦਾ ਹੈ"]),
                  T("Speak about form.", ["in the separation the metre changes", "which line shall we present?"],
                    ["ਵਿਛੋੜੇ ਵਿੱਚ ਛੰਦ ਬਦਲ ਜਾਂਦਾ ਹੈ", "ਕੀ ਸਤਰ ਪੇਸ਼ ਕਰੀਏ?"]),
              ])),
        ]},
        {"id": "C1+-U2", "title": "ਸਮੀਖਿਆ ਦਾ ਤਰਕ", "lessons": [
            L("ਦਾਅਵਾ ਅਤੇ ਸਬੂਤ",
              "A review stands on two legs: ਦਾਅਵਾ (claim) and ਸਬੂਤ (evidence). The claim is "
              "introduced with ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ, the evidence with ਸਬੂਤ ਵਜੋਂ or ਇਸ ਦਾ ਸਬੂਤ ਇਹ ਹੈ ਕਿ, "
              "and the hedge with ਇਹ ਨਹੀਂ ਕਿਹਾ ਜਾ ਸਕਦਾ ਕਿ.",
              [V("ਦਾਅਵਾ", "daava", "claim", "noun"),
               V("ਸਬੂਤ", "sabut", "evidence", "noun"),
               V("ਪਾਠ", "path", "text, reading", "noun"),
               V("ਸੰਦਰਭ", "sandarbh", "context", "noun"),
               V("ਨਿਆਂ", "nian", "judgement, justice", "noun")],
              G("Holding a claim to its evidence",
                "ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ · ਇਸ ਦਾ ਸਬੂਤ ਇਹ ਹੈ ਕਿ · ਇਹ ਨਹੀਂ ਕਿਹਾ ਜਾ ਸਕਦਾ ਕਿ",
                "ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ states what is being argued, ਇਸ ਦਾ ਸਬੂਤ ਇਹ ਹੈ ਕਿ brings the text "
                "in, and ਇਹ ਨਹੀਂ ਕਿਹਾ ਜਾ ਸਕਦਾ ਕਿ sets the limit of the claim. ਸੰਦਰਭ gives the "
                "context in which the line is read.",
                [X("ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ ਮਰਜ਼ੀ ਦਾ ਸਵਾਲ ਕਥਾ ਦਾ ਕੇਂਦਰ ਹੈ।", "daava ih hai ki marzi da saval katha da kendar hai.", "The claim is that the question of wish is the centre of the tale."),
                 X("ਇਸ ਦਾ ਸਬੂਤ ਇਹ ਹੈ ਕਿ ਵਿਆਹ ਦੀ ਗੱਲ ਹੀ ਪੁੱਛੀ ਨਹੀਂ ਜਾਂਦੀ।", "is da sabut ih hai ki viah di gal hi puchhi nahin jandi.", "Its evidence is that the matter of the marriage is not even asked."),
                 X("ਪਰ ਇਹ ਨਹੀਂ ਕਿਹਾ ਜਾ ਸਕਦਾ ਕਿ ਕੋਈ ਵੀ ਪਾਤਰ ਪੂਰਾ ਨਿਰਦੋਸ਼ ਹੈ।", "par ih nahin kiha ja sakda ki koi vi pattar pura nirdosh hai.", "But it cannot be said that any character is entirely blameless.")],
                [("ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ ਮਰਜ਼ੀ ਦਾ ਸਵਾਲ ਕੇਂਦਰ ਹੈ ਕਿ।", "ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ ਮਰਜ਼ੀ ਦਾ ਸਵਾਲ ਕੇਂਦਰ ਹੈ।", "One ਕਿ opens the clause."),
                 ("ਇਸ ਦਾ ਸਬੂਤ ਇਹ ਹੈ।", "ਇਸ ਦਾ ਸਬੂਤ ਇਹ ਹੈ ਕਿ ਵਿਆਹ ਦੀ ਗੱਲ ਪੁੱਛੀ ਨਹੀਂ ਜਾਂਦੀ।", "ਸਬੂਤ needs the clause that carries it.")]),
              [D("ਸੰਪਾਦਕ", "ਤੁਹਾਡਾ ਦਾਅਵਾ?", "tuhada daava?", "Your claim?"),
               D("ਸਮੀਖਿਆਕਾਰ", "ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ ਮਰਜ਼ੀ ਦਾ ਸਵਾਲ ਕੇਂਦਰ ਵਿੱਚ ਹੈ।", "daava ih hai ki marzi da saval kendar vich hai.", "The claim is that the question of wish is at the centre."),
               D("ਸੰਪਾਦਕ", "ਸਬੂਤ?", "sabut?", "The evidence?"),
               D("ਸਮੀਖਿਆਕਾਰ", "ਸਬੂਤ ਵਜੋਂ ਦੋ ਸਤਰਾਂ ਕਾਫ਼ੀ ਹਨ; ਪਰ ਇਹ ਨਹੀਂ ਕਿਹਾ ਜਾ ਸਕਦਾ ਕਿ ਪਾਠ ਪੂਰਾ ਨਿਰਦੋਸ਼ ਹੈ।", "sabut vajo do sataran kafi han; par ih nahin kiha ja sakda ki path pura nirdosh hai.", "As evidence two lines are enough; but it cannot be said that the text is entirely innocent.")],
              WS("Claim worksheet", [
                  T("State the claim.", ["the claim is that the question of wish is the centre", "its evidence is that the matter is not even asked"],
                    ["ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ ਮਰਜ਼ੀ ਦਾ ਸਵਾਲ ਕੇਂਦਰ ਹੈ", "ਇਸ ਦਾ ਸਬੂਤ ਇਹ ਹੈ ਕਿ ਗੱਲ ਹੀ ਪੁੱਛੀ ਨਹੀਂ ਜਾਂਦੀ"]),
                  T("Set the limit.", ["it cannot be said that any character is entirely blameless", "as evidence two lines are enough"],
                    ["ਇਹ ਨਹੀਂ ਕਿਹਾ ਜਾ ਸਕਦਾ ਕਿ ਕੋਈ ਪਾਤਰ ਪੂਰਾ ਨਿਰਦੋਸ਼ ਹੈ", "ਸਬੂਤ ਵਜੋਂ ਦੋ ਸਤਰਾਂ ਕਾਫ਼ੀ ਹਨ"]),
              ])),
            L("ਪਾਠ ਦੀ ਤੁਲਨਾ",
              "Comparing two tellings uses ਸੰਸਕਰਨ (version) and ਦੋਹਾਂ ਵਿੱਚ ਫ਼ਰਕ: ਦਾਮੋਦਰ ਦਾ ਸੰਸਕਰਨ, "
              "ਵਾਰਿਸ ਦਾ ਸੰਸਕਰਨ, ਅਤੇ ਦੋਹਾਂ ਵਿੱਚ ਫ਼ਰਕ ਇਹ ਹੈ ਕਿ. The comparison sentence keeps both "
              "sides alive and avoids calling one wrong.",
              [V("ਸੰਸਕਰਨ", "sansakaran", "version, edition", "noun"),
               V("ਤੁਲਨਾ", "tulna", "comparison", "noun"),
               V("ਅੰਸ਼", "ansh", "element, part", "noun"),
               V("ਭਾਵ", "bhav", "sense, meaning", "noun"),
               V("ਲੈਣ-ਦੇਣ", "lain-den", "give and take", "noun")],
              G("Comparing two versions",
                "ਦਾਮੋਦਰ ਦਾ ਸੰਸਕਰਨ · ਦੋਹਾਂ ਵਿੱਚ ਫ਼ਰਕ ਇਹ ਹੈ ਕਿ · ਭਾਵ ਨਹੀਂ ਬਦਲਦਾ",
                "The version is named with ਦਾ ਸੰਸਕਰਨ, the comparison is made with ਦੋਹਾਂ ਵਿੱਚ ਫ਼ਰਕ, "
                "and the conclusion says what survives translation into another telling: ਭਾਵ "
                "ਨਹੀਂ ਬਦਲਦਾ, ਸਿਰਫ਼ ਲਹਿਜਾ ਬਦਲਦਾ ਹੈ.",
                [X("ਦਾਮੋਦਰ ਦਾ ਸੰਸਕਰਨ ਸੋਲ੍ਹਵੀਂ ਸਦੀ ਦਾ ਹੈ।", "Damodar da sansakaran solhvin sadi da hai.", "Damodar's version belongs to the sixteenth century."),
                 X("ਦੋਹਾਂ ਵਿੱਚ ਫ਼ਰਕ ਇਹ ਹੈ ਕਿ ਵਾਰਿਸ ਦਾ ਲਹਿਜਾ ਤਿੱਖਾ ਹੈ।", "dovan vich farak ih hai ki Waris da lahija tikkha hai.", "The difference between the two is that Waris's tone is sharper."),
                 X("ਤੁਲਨਾ ਵਿੱਚ ਭਾਵ ਨਹੀਂ ਬਦਲਦਾ, ਲਹਿਜਾ ਬਦਲਦਾ ਹੈ।", "tulna vich bhav nahin badalda, lahija badalda hai.", "In the comparison the meaning does not change, the tone changes.")],
                [("ਦੋਹਾਂ ਵਿੱਚ ਫ਼ਰਕ ਇਹ ਹੈ ਕਿ।", "ਦੋਹਾਂ ਵਿੱਚ ਫ਼ਰਕ ਇਹ ਹੈ ਕਿ ਵਾਰਿਸ ਦਾ ਲਹਿਜਾ ਤਿੱਖਾ ਹੈ।", "The clause after ਕਿ has to be written out."),
                 ("ਦਾਮੋਦਰ ਦਾ ਸੰਸਕਰਨ ਸੋਲ੍ਹਵੀਂ ਸਦੀ ਹੈ।", "ਦਾਮੋਦਰ ਦਾ ਸੰਸਕਰਨ ਸੋਲ੍ਹਵੀਂ ਸਦੀ ਦਾ ਹੈ।", "A century belongs: ਸਦੀ ਦਾ ਹੈ.")]),
              [D("ਸੰਪਾਦਕ", "ਕਿਹੜਾ ਸੰਸਕਰਨ ਪਹਿਲਾਂ ਹੈ?", "kihrha sansakaran pahilan hai?", "Which version is earlier?"),
               D("ਸਮੀਖਿਆਕਾਰ", "ਦਾਮੋਦਰ ਦਾ, ਸੋਲ੍ਹਵੀਂ ਸਦੀ ਦਾ। ਵਾਰਿਸ ਦਾ 1766 ਦਾ ਹੈ।", "Damodar da, solhvin sadi da. Waris da 1766 da hai.", "Damodar's, of the sixteenth century. Waris's is of 1766."),
               D("ਸੰਪਾਦਕ", "ਤੁਲਨਾ ਵਿੱਚ ਕੀ ਨਿਕਲਦਾ ਹੈ?", "tulna vich ki nikalda hai?", "What comes out of the comparison?"),
               D("ਸਮੀਖਿਆਕਾਰ", "ਭਾਵ ਇੱਕੋ ਰਹਿੰਦਾ ਹੈ, ਪਰ ਲਹਿਜਾ ਅਤੇ ਰਫ਼ਤਾਰ ਬਦਲ ਜਾਂਦੀ ਹੈ।", "bhav ikko rahinda hai, par lahija ate raftar badal jandi hai.", "The meaning stays the same, but the tone and the pace change.")],
              WS("Comparison worksheet", [
                  T("Name the versions.", ["Damodar's version is of the sixteenth century", "the difference between the two is that the tone is sharper"],
                    ["ਦਾਮੋਦਰ ਦਾ ਸੰਸਕਰਨ ਸੋਲ੍ਹਵੀਂ ਸਦੀ ਦਾ ਹੈ", "ਦੋਹਾਂ ਵਿੱਚ ਫ਼ਰਕ ਇਹ ਹੈ ਕਿ ਲਹਿਜਾ ਤਿੱਖਾ ਹੈ"]),
                  T("Say what survives.", ["the meaning does not change, the tone changes", "what comes out of the comparison?"],
                    ["ਭਾਵ ਨਹੀਂ ਬਦਲਦਾ, ਲਹਿਜਾ ਬਦਲਦਾ ਹੈ", "ਤੁਲਨਾ ਵਿੱਚ ਕੀ ਨਿਕਲਦਾ ਹੈ?"]),
              ])),
            L("ਵਿਆਖਿਆ ਦੀਆਂ ਹੱਦਾਂ",
              "The strongest sentence in a review names its own limit: ਹੱਦ ਇੱਥੇ ਖ਼ਤਮ ਹੁੰਦੀ ਹੈ (the "
              "limit ends here), ਇਸ ਤੋਂ ਅੱਗੇ ਪਾਠ ਚੁੱਪ ਕਰ ਜਾਂਦਾ ਹੈ, ਸੰਭਵ ਹੈ ਕਿ … ਪਰ ਸਿੱਧ ਨਹੀਂ. It "
              "keeps the argument honest without weakening it.",
              [V("ਵਿਆਖਿਆ", "viakhia", "interpretation", "noun"),
               V("ਹੱਦ", "hadd", "limit, boundary", "noun"),
               V("ਸੰਭਵ", "sambhav", "possible", "adjective"),
               V("ਸਿੱਧ", "siddh", "proved", "adjective"),
               V("ਚੁੱਪ", "chupp", "silence", "noun")],
              G("Naming the limit of an interpretation",
                "ਹੱਦ ਇੱਥੇ ਖ਼ਤਮ ਹੁੰਦੀ ਹੈ · ਸੰਭਵ ਹੈ ਕਿ … ਪਰ ਸਿੱਧ ਨਹੀਂ · ਪਾਠ ਚੁੱਪ ਕਰ ਜਾਂਦਾ ਹੈ",
                "The limit is stated plainly: ਹੱਦ ਇੱਥੇ ਖ਼ਤਮ ਹੁੰਦੀ ਹੈ. A possibility is offered "
                "with ਸੰਭਵ ਹੈ ਕਿ, and immediately qualified with ਪਰ ਸਿੱਧ ਨਹੀਂ. When the text says "
                "nothing, the review says ਪਾਠ ਚੁੱਪ ਕਰ ਜਾਂਦਾ ਹੈ.",
                [X("ਵਿਆਖਿਆ ਦੀ ਹੱਦ ਇੱਥੇ ਖ਼ਤਮ ਹੁੰਦੀ ਹੈ।", "viakhia di hadd itthe khatam hundi hai.", "The limit of the interpretation ends here."),
                 X("ਸੰਭਵ ਹੈ ਕਿ ਕਵੀ ਨੇ ਇਹ ਜਾਣ-ਬੁੱਝ ਕੇ ਲਿਖਿਆ, ਪਰ ਸਿੱਧ ਨਹੀਂ।", "sambhav hai ki kavi ne ih jaan-bujh ke likhia, par siddh nahin.", "It is possible that the poet wrote this deliberately, but it is not proved."),
                 X("ਇਸ ਮੁੱਦੇ ਉੱਤੇ ਪਾਠ ਚੁੱਪ ਕਰ ਜਾਂਦਾ ਹੈ।", "is mudde utte path chupp kar janda hai.", "On this point the text falls silent.")],
                [("ਸੰਭਵ ਹੈ ਕਿ ਕਵੀ ਨੇ ਲਿਖਿਆ ਹੋਵੇਗਾ ਸਿੱਧ ਨਹੀਂ।", "ਸੰਭਵ ਹੈ ਕਿ ਕਵੀ ਨੇ ਲਿਖਿਆ, ਪਰ ਸਿੱਧ ਨਹੀਂ।", "The qualification needs ਪਰ to stand."),
                 ("ਹੱਦ ਖ਼ਤਮ ਹੁੰਦੀ।", "ਹੱਦ ਖ਼ਤਮ ਹੁੰਦੀ ਹੈ।", "The statement keeps ਹੈ.")]),
              [D("ਸੰਪਾਦਕ", "ਕੀ ਇਹ ਜਾਣ-ਬੁੱਝ ਕੇ ਲਿਖਿਆ ਗਿਆ?", "ki ih jaan-bujh ke likhia gia?", "Was this written deliberately?"),
               D("ਸਮੀਖਿਆਕਾਰ", "ਸੰਭਵ ਹੈ, ਪਰ ਸਿੱਧ ਨਹੀਂ।", "sambhav hai, par siddh nahin.", "It is possible, but not proved."),
               D("ਸੰਪਾਦਕ", "ਤਾਂ ਫਿਰ ਕੀ ਲਿਖੀਏ?", "tan phir ki likhie?", "Then what shall we write?"),
               D("ਸਮੀਖਿਆਕਾਰ", "ਕਿ ਇੱਥੇ ਵਿਆਖਿਆ ਦੀ ਹੱਦ ਖ਼ਤਮ ਹੁੰਦੀ ਹੈ ਅਤੇ ਪਾਠ ਚੁੱਪ ਕਰ ਜਾਂਦਾ ਹੈ।", "ki itthe viakhia di hadd khatam hundi hai ate path chupp kar janda hai.", "That here the limit of the interpretation ends and the text falls silent.")],
              WS("Limits worksheet", [
                  T("State the limit.", ["the limit of the interpretation ends here", "on this point the text falls silent"],
                    ["ਵਿਆਖਿਆ ਦੀ ਹੱਦ ਇੱਥੇ ਖ਼ਤਮ ਹੁੰਦੀ ਹੈ", "ਇਸ ਮੁੱਦੇ ਉੱਤੇ ਪਾਠ ਚੁੱਪ ਕਰ ਜਾਂਦਾ ਹੈ"]),
                  T("Hedge honestly.", ["it is possible that the poet wrote this deliberately, but it is not proved", "then what shall we write?"],
                    ["ਸੰਭਵ ਹੈ ਕਿ ਕਵੀ ਨੇ ਇਹ ਜਾਣ-ਬੁੱਝ ਕੇ ਲਿਖਿਆ, ਪਰ ਸਿੱਧ ਨਹੀਂ", "ਤਾਂ ਫਿਰ ਕੀ ਲਿਖੀਏ?"]),
              ])),
        ]},
        {"id": "C1+-U3", "title": "ਸੰਪਾਦਕੀ ਅਤੇ ਸੰਵਾਦ", "lessons": [
            L("ਸੰਪਾਦਕੀ ਲਿਖਣੀ",
              "An editorial speaks as ਅਸੀਂ and puts the argument in the first paragraph: ਪਹਿਲਾ "
              "ਤਰਕ ਇਹ ਹੈ ਕਿ, ਦੂਜਾ ਤਰਕ, ਅਤੇ ਅਖ਼ੀਰ ਵਿੱਚ ਮੰਗ. The tone stays impersonal even when "
              "the demand is sharp.",
              [V("ਸੰਪਾਦਕੀ", "sampadki", "editorial", "noun"),
               V("ਤਰਕ", "tarak", "argument", "noun"),
               V("ਮੰਗ", "mang", "demand", "noun"),
               V("ਪਾਠਕ", "pathak", "reader", "noun"),
               V("ਸੰਵਾਦ", "sanvad", "dialogue", "noun")],
              G("The editorial paragraph",
                "ਪਹਿਲਾ ਤਰਕ ਇਹ ਹੈ ਕਿ · ਦੂਜਾ ਤਰਕ · ਅਸੀਂ ਮੰਗ ਕਰਦੇ ਹਾਂ ਕਿ",
                "The editorial orders its reasons with ਪਹਿਲਾ ਤਰਕ and ਦੂਜਾ ਤਰਕ, and its demand with "
                "ਅਸੀਂ ਮੰਗ ਕਰਦੇ ਹਾਂ ਕਿ. The verb stays respectful: ਧਿਆਨ ਦਿੱਤਾ ਜਾਵੇ (let attention "
                "be given), not a command.",
                [X("ਪਹਿਲਾ ਤਰਕ ਇਹ ਹੈ ਕਿ ਪਾਠ ਨੂੰ ਸਕੂਲਾਂ ਵਿੱਚ ਪੜ੍ਹਾਇਆ ਜਾਵੇ।", "pahila tarak ih hai ki path nun skulan vich parhaia jave.", "The first argument is that the text be taught in schools."),
                 X("ਦੂਜਾ ਤਰਕ ਇਹ ਹੈ ਕਿ ਅਨੁਵਾਦ ਨਾਲ ਭਾਵ ਨਹੀਂ ਖੁੱਸਦਾ।", "duja tarak ih hai ki anuvad nal bhav nahin khussda.", "The second argument is that the sense is not lost in translation."),
                 X("ਅਸੀਂ ਮੰਗ ਕਰਦੇ ਹਾਂ ਕਿ ਪਾਠਕਾਂ ਦੀ ਰਾਏ ਛਾਪੀ ਜਾਵੇ।", "asin mang karde han ki pathakan di rae chhapi jave.", "We demand that readers' opinions be printed.")],
                [("ਪਹਿਲਾ ਤਰਕ ਇਹ ਹੈ ਕਿ ਪਾਠ ਪੜ੍ਹਾਇਆ ਜਾਵੇਗਾ।", "ਪਹਿਲਾ ਤਰਕ ਇਹ ਹੈ ਕਿ ਪਾਠ ਪੜ੍ਹਾਇਆ ਜਾਵੇ।", "An argument of this kind takes the subjunctive ਜਾਵੇ."),
                 ("ਅਸੀਂ ਮੰਗ ਕਰਦੇ ਹਾਂ ਕਿ ਰਾਏ ਛਾਪੀ ਜਾਵੇਗੀ।", "ਅਸੀਂ ਮੰਗ ਕਰਦੇ ਹਾਂ ਕਿ ਰਾਏ ਛਾਪੀ ਜਾਵੇ।", "A demand takes the subjunctive ਜਾਵੇ.")]),
              [D("ਸੰਪਾਦਕ", "ਸੰਪਾਦਕੀ ਦਾ ਪਹਿਲਾ ਤਰਕ?", "sampadki da pahila tarak?", "The editorial's first argument?"),
               D("ਲੇਖਕ", "ਪਹਿਲਾ ਤਰਕ ਇਹ ਹੈ ਕਿ ਪਾਠ ਸਕੂਲਾਂ ਵਿੱਚ ਪੜ੍ਹਾਇਆ ਜਾਵੇ।", "pahila tarak ih hai ki path skulan vich parhaia jave.", "The first argument is that the text be taught in schools."),
               D("ਸੰਪਾਦਕ", "ਮੰਗ ਕਿਵੇਂ ਲਿਖੀਏ?", "mang kiven likhie?", "How shall we write the demand?"),
               D("ਲੇਖਕ", "ਅਸੀਂ ਮੰਗ ਕਰਦੇ ਹਾਂ ਕਿ ਪਾਠਕਾਂ ਦੀ ਰਾਏ ਛਾਪੀ ਜਾਵੇ, ਅਤੇ ਧਿਆਨ ਦਿੱਤਾ ਜਾਵੇ।", "asin mang karde han ki pathakan di rae chhapi jave, ate dhian ditta jave.", "We demand that readers' opinions be printed, and that attention be paid.")],
              WS("Editorial worksheet", [
                  T("Order the arguments.", ["the first argument is that the text be taught in schools", "the second argument is that the sense is not lost"],
                    ["ਪਹਿਲਾ ਤਰਕ ਇਹ ਹੈ ਕਿ ਪਾਠ ਸਕੂਲਾਂ ਵਿੱਚ ਪੜ੍ਹਾਇਆ ਜਾਵੇ", "ਦੂਜਾ ਤਰਕ ਇਹ ਹੈ ਕਿ ਭਾਵ ਨਹੀਂ ਖੁੱਸਦਾ"]),
                  T("Write the demand.", ["we demand that readers' opinions be printed", "attention should be paid"],
                    ["ਅਸੀਂ ਮੰਗ ਕਰਦੇ ਹਾਂ ਕਿ ਪਾਠਕਾਂ ਦੀ ਰਾਏ ਛਾਪੀ ਜਾਵੇ", "ਧਿਆਨ ਦਿੱਤਾ ਜਾਵੇ"]),
              ])),
            L("ਪਾਠਕ ਦਾ ਪੱਤਰ",
              "A reader's letter argues with the review: ਪੱਤਰ ਰਾਹੀਂ, ਸਹਿਮਤ ਨਹੀਂ ਹਾਂ, ਪਰ ਇਹ ਵੀ ਸੱਚ "
              "ਹੈ ਕਿ. The words ਰਾਏ (opinion), ਸੁਝਾਅ (suggestion) and ਸੋਧ (correction) keep the "
              "exchange civil.",
              [V("ਰਾਏ", "rae", "opinion", "noun"),
               V("ਸਹਿਮਤ", "sahmat", "agreeing", "adjective"),
               V("ਸੋਧ", "sodh", "correction", "noun"),
               V("ਸੁਝਾਅ", "sujhaa", "suggestion", "noun"),
               V("ਸੰਪਰਕ", "sampark", "contact, connection", "noun")],
              G("Writing to the editor",
                "ਪੱਤਰ ਰਾਹੀਂ · ਸਹਿਮਤ ਨਹੀਂ ਹਾਂ · ਪਰ ਇਹ ਵੀ ਸੱਚ ਹੈ ਕਿ",
                "The channel takes ਰਾਹੀਂ, disagreement is stated with ਸਹਿਮਤ ਨਹੀਂ ਹਾਂ, and the "
                "counterpoint is added with ਪਰ ਇਹ ਵੀ ਸੱਚ ਹੈ ਕਿ. The suggestion is offered with "
                "ਸੁਝਾਅ ਦੇਣਾ, and the correction with ਸੋਧ ਕਰਨੀ (feminine).",
                [X("ਪੱਤਰ ਰਾਹੀਂ ਆਪਣੀ ਰਾਏ ਦੇ ਰਿਹਾ ਹਾਂ।", "pattar rahin apni rae de rahia han.", "Through this letter I am giving my opinion."),
                 X("ਮੈਂ ਸਹਿਮਤ ਨਹੀਂ ਹਾਂ, ਪਰ ਇਹ ਵੀ ਸੱਚ ਹੈ ਕਿ ਲੇਖਕ ਨੇ ਪਾਠ ਪੜ੍ਹਿਆ ਹੈ।", "main sahmat nahin han, par ih vi sach hai ki lekhak ne path parhia hai.", "I do not agree, but it is also true that the writer has read the text."),
                 X("ਇੱਕ ਸੁਝਾਅ ਦੇਣਾ ਚਾਹੁੰਦਾ ਹਾਂ, ਅਤੇ ਇੱਕ ਸੋਧ ਵੀ।", "ikk sujhaa dena chahunda han, ate ikk sodh vi.", "I want to give a suggestion, and a correction too.")],
                [("ਮੈਂ ਸਹਿਮਤ ਨਹੀਂ ਹਾਂ ਨਾਂ।", "ਮੈਂ ਸਹਿਮਤ ਨਹੀਂ ਹਾਂ।", "One negation is enough."),
                 ("ਸੋਧ ਕੀਤੀ ਜਾਵੇ।", "ਸੋਧ ਕਰਨੀ ਚਾਹੀਦੀ ਹੈ।", "ਸੋਧ is feminine: ਸੋਧ ਕਰਨੀ.")]),
              [D("ਸੰਪਾਦਕ", "ਪਾਠਕ ਦਾ ਪੱਤਰ ਆਇਆ ਹੈ?", "pathak da pattar aia hai?", "Has the reader's letter come?"),
               D("ਸਹਾਇਕ", "ਹਾਂ, ਪੱਤਰ ਰਾਹੀਂ ਇੱਕ ਰਾਏ ਆਈ ਹੈ।", "han, pattar rahin ikk rae aai hai.", "Yes, an opinion has come through a letter."),
               D("ਸੰਪਾਦਕ", "ਸਹਿਮਤ ਹੈ?", "sahmat hai?", "Does he agree?"),
               D("ਸਹਾਇਕ", "ਨਹੀਂ, ਸਹਿਮਤ ਨਹੀਂ, ਪਰ ਇੱਕ ਸੁਝਾਅ ਅਤੇ ਇੱਕ ਸੋਧ ਵੀ ਦਿੱਤੀ ਹੈ।", "nahin, sahmat nahin, par ikk sujhaa ate ikk sodh vi ditti hai.", "No, he does not agree, but he has also given a suggestion and a correction.")],
              WS("Reader's letter worksheet", [
                  T("Open the letter.", ["through this letter I am giving my opinion", "I do not agree"],
                    ["ਪੱਤਰ ਰਾਹੀਂ ਆਪਣੀ ਰਾਏ ਦੇ ਰਿਹਾ ਹਾਂ", "ਮੈਂ ਸਹਿਮਤ ਨਹੀਂ ਹਾਂ"]),
                  T("Add the counterpoint.", ["but it is also true that the writer has read the text", "I want to give a suggestion and a correction"],
                    ["ਪਰ ਇਹ ਵੀ ਸੱਚ ਹੈ ਕਿ ਲੇਖਕ ਨੇ ਪਾਠ ਪੜ੍ਹਿਆ ਹੈ", "ਇੱਕ ਸੁਝਾਅ ਅਤੇ ਇੱਕ ਸੋਧ ਦੇਣਾ ਚਾਹੁੰਦਾ ਹਾਂ"]),
              ])),
            L("ਸੰਵਾਦ ਅਤੇ ਸੋਧ",
              "The last step is public correction: ਜਵਾਬ ਵਿੱਚ, ਸੋਧ ਛਾਪੀ ਗਈ, ਧੰਨਵਾਦ ਸਹਿਤ. ਸੋਧ ਛਾਪਣੀ "
              "(to print a correction) keeps the record straight, and ਧੰਨਵਾਦ ਸਹਿਤ closes it with "
              "grace.",
              [V("ਜਵਾਬ", "javab", "reply", "noun"),
               V("ਸੋਧ", "sodh", "correction", "noun"),
               V("ਧੰਨਵਾਦ ਸਹਿਤ", "dhannavad sahit", "with thanks", "phrase"),
               V("ਰਿਕਾਰਡ", "rikard", "record", "noun"),
               V("ਇਨਸਾਫ਼", "insaf", "fairness, justice", "noun")],
              G("Correcting in public",
                "ਜਵਾਬ ਵਿੱਚ ਲਿਖਿਆ ਗਿਆ · ਸੋਧ ਛਾਪੀ ਗਈ · ਧੰਨਵਾਦ ਸਹਿਤ",
                "The reply is reported in the passive: ਜਵਾਬ ਵਿੱਚ ਲਿਖਿਆ ਗਿਆ ਕਿ …, ਸੋਧ ਛਾਪੀ ਗਈ. "
                "ਧੰਨਵਾਦ ਸਹਿਤ closes a correction with good manners, and ਰਿਕਾਰਡ ਸਾਫ਼ ਰਹਿੰਦਾ ਹੈ "
                "gives the reason: the record stays clean.",
                [X("ਜਵਾਬ ਵਿੱਚ ਲਿਖਿਆ ਗਿਆ ਕਿ ਸੋਧ ਸਹੀ ਹੈ।", "javab vich likhia gia ki sodh sahi hai.", "In the reply it was written that the correction is right."),
                 X("ਸੋਧ ਅਗਲੇ ਅੰਕ ਵਿੱਚ ਛਾਪੀ ਗਈ।", "sodh agle ank vich chhapi gai.", "The correction was printed in the next issue."),
                 X("ਧੰਨਵਾਦ ਸਹਿਤ, ਇਸ ਲਈ ਕਿ ਰਿਕਾਰਡ ਸਾਫ਼ ਰਹਿੰਦਾ ਹੈ।", "dhannavad sahit, is lai ki rikard saf rahinda hai.", "With thanks, because the record stays clean.")],
                [("ਸੋਧ ਛਾਪਿਆ ਗਿਆ।", "ਸੋਧ ਛਾਪੀ ਗਈ।", "ਸੋਧ is feminine: ਛਾਪੀ ਗਈ."),
                 ("ਜਵਾਬ ਵਿੱਚ ਲਿਖਿਆ ਕਿ ਸੋਧ ਸਹੀ ਹੈ।", "ਜਵਾਬ ਵਿੱਚ ਲਿਖਿਆ ਗਿਆ ਕਿ ਸੋਧ ਸਹੀ ਹੈ।", "The impersonal needs ਗਿਆ.")]),
              [D("ਸੰਪਾਦਕ", "ਸੋਧ ਛਾਪੀਏ?", "sodh chhapie?", "Shall we print the correction?"),
               D("ਸਹਾਇਕ", "ਹਾਂ, ਜਵਾਬ ਵਿੱਚ ਲਿਖਿਆ ਗਿਆ ਹੈ ਕਿ ਸੋਧ ਸਹੀ ਹੈ।", "han, javab vich likhia gia hai ki sodh sahi hai.", "Yes, in the reply it has been written that the correction is right."),
               D("ਸੰਪਾਦਕ", "ਲਹਿਜਾ?", "lahija?", "The tone?"),
               D("ਸਹਾਇਕ", "ਧੰਨਵਾਦ ਸਹਿਤ, ਅਤੇ ਇਹ ਵੀ ਲਿਖੀਏ ਕਿ ਰਿਕਾਰਡ ਸਾਫ਼ ਰਹਿੰਦਾ ਹੈ।", "dhannavad sahit, ate ih vi likhie ki rikard saf rahinda hai.", "With thanks, and let us also write that the record stays clean.")],
              WS("Correction worksheet", [
                  T("Report the reply.", ["in the reply it was written that the correction is right", "the correction was printed in the next issue"],
                    ["ਜਵਾਬ ਵਿੱਚ ਲਿਖਿਆ ਗਿਆ ਕਿ ਸੋਧ ਸਹੀ ਹੈ", "ਸੋਧ ਅਗਲੇ ਅੰਕ ਵਿੱਚ ਛਾਪੀ ਗਈ"]),
                  T("Close with grace.", ["with thanks", "because the record stays clean"],
                    ["ਧੰਨਵਾਦ ਸਹਿਤ", "ਕਿਉਂਕਿ ਰਿਕਾਰਡ ਸਾਫ਼ ਰਹਿੰਦਾ ਹੈ"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Heer Ranjha is the classical tragedy of Punjabi literature. The story of love, "
                 "forced separation and the simultaneous death of the two young people in the "
                 "Punjabi countryside reached writing through Damodar Gulati in the 1600s, working "
                 "from an oral legend already in circulation; the telling everyone knows is Waris "
                 "Shah's Heer, an epic written in 1766. Waris Shah's version is quoted in rural "
                 "Punjab the way proverbs are quoted, and it gave the language phrases that are "
                 "still used as ordinary idiom. For a learner it is the best long text in the "
                 "language: a story carried in dialogue, and a diction that has not gone out of "
                 "use in two hundred and fifty years."),
        source_url="https://en.wikipedia.org/wiki/Heer_Ranjha",
        reading=("ਹੀਰ ਰਾਂਝਾ ਦੀ ਕਥਾ ਲੋਕ-ਕਥਾ ਤੋਂ ਲਿਖਤ ਤੱਕ ਪਹੁੰਚੀ। ਸੋਲ੍ਹਵੀਂ ਸਦੀ ਵਿੱਚ ਦਾਮੋਦਰ ਨੇ ਪਹਿਲੀ "
                 "ਪੇਸ਼ਕਾਰੀ ਲਿਖੀ, ਅਤੇ 1766 ਵਿੱਚ ਵਾਰਿਸ ਸ਼ਾਹ ਨੇ ‘ਹੀਰ’ ਨੂੰ ਇੱਕ ਲੰਮੀ ਨਜ਼ਮ ਦਾ ਰੂਪ ਦਿੱਤਾ। "
                 "ਦੋਹਾਂ ਸੰਸਕਰਨਾਂ ਵਿੱਚ ਫ਼ਰਕ ਲਹਿਜੇ ਦਾ ਹੈ: ਦਾਮੋਦਰ ਦਾ ਵਹਾਅ ਸਾਧਾਰਨ ਹੈ, ਵਾਰਿਸ ਦਾ ਤਿੱਖਾ। "
                 "ਕਥਾ ਦਾ ਢਾਂਚਾ ਤਿੰਨ ਹਿੱਸਿਆਂ ਵਿੱਚ ਬਣਦਾ ਹੈ — ਭੂਮਿਕਾ, ਵਿਛੋੜਾ ਅਤੇ ਅੰਤ — ਅਤੇ ਦਾਰੂ ਇਹ "
                 "ਹੈ ਕਿ ਮਰਜ਼ੀ ਕਿਸੇ ਦੀ ਨਹੀਂ ਪੁੱਛੀ ਜਾਂਦੀ। ਸੰਭਵ ਹੈ ਕਿ ਕਵੀ ਨੇ ਇਹ ਜਾਣ-ਬੁੱਝ ਕੇ ਲਿਖਿਆ, ਪਰ "
                 "ਇਹ ਸਿੱਧ ਨਹੀਂ; ਇੱਥੇ ਵਿਆਖਿਆ ਦੀ ਹੱਦ ਖ਼ਤਮ ਹੁੰਦੀ ਹੈ ਅਤੇ ਪਾਠ ਚੁੱਪ ਕਰ ਜਾਂਦਾ ਹੈ।"),
        reading_gloss=("The story of Heer and Ranjha travelled from folk tale to writing. In the "
                       "sixteenth century Damodar wrote the first presentation, and in 1766 Waris "
                       "Shah gave 'Heer' the form of a long poem. The difference between the two "
                       "versions is one of tone: Damodar's flow is plain, Waris's is sharp. The "
                       "structure of the tale is built in three parts — opening, separation and "
                       "ending — and the moving force is that nobody asks anybody's wish. It is "
                       "possible that the poet wrote this deliberately, but it is not proved; here "
                       "the limit of the interpretation ends and the text falls silent."),
        listening=("ਸੰਪਾਦਕ: ਸਮੀਖਿਆ ਦਾ ਦਾਅਵਾ ਕੀ ਹੈ? ਸਮੀਖਿਆਕਾਰ: ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ ਕਥਾ ਮਰਜ਼ੀ ਦੇ ਸਵਾਲ ਉੱਤੇ "
                   "ਖੜ੍ਹੀ ਹੈ। ਸੰਪਾਦਕ: ਸਬੂਤ? ਸਮੀਖਿਆਕਾਰ: ਸਬੂਤ ਵਜੋਂ ਤਿੰਨ ਸਤਰਾਂ ਹਨ, ਅਤੇ ਦੋਹਾਂ ਸੰਸਕਰਨਾਂ ਵਿੱਚ "
                   "ਭਾਵ ਨਹੀਂ ਬਦਲਦਾ। ਸੰਪਾਦਕ: ਕੋਈ ਹੱਦ ਵੀ ਦੱਸੋ। ਸਮੀਖਿਆਕਾਰ: ਹੱਦ ਇੱਥੇ ਖ਼ਤਮ ਹੁੰਦੀ ਹੈ; "
                   "ਸੰਭਵ ਹੈ ਕਿ ਕਵੀ ਨੇ ਜਾਣ-ਬੁੱਝ ਕੇ ਲਿਖਿਆ, ਪਰ ਸਿੱਧ ਨਹੀਂ।"),
        listening_gloss=("Editor: What is the claim of the review? Reviewer: The claim is that the "
                         "tale stands on the question of wish. Editor: The evidence? Reviewer: As "
                         "evidence there are three lines, and the meaning does not change between "
                         "the two versions. Editor: State a limit as well. Reviewer: The limit "
                         "ends here; it is possible that the poet wrote it deliberately, but it is "
                         "not proved."),
        voice_tag=VOICE,
        idioms=[
            ("ਇੱਕ ਸਤਰ ਵਿੱਚ", "in a single line", "said of a line that does a whole passage's work"),
            ("ਕੱਸਵੱਟੀ ਲੱਗਣੀ", "to stand the touchstone", "to hold up under a test"),
            ("ਹੱਦ ਖ਼ਤਮ ਹੋਣੀ", "for the limit to end", "here the argument can go no further"),
            ("ਪਾਠ ਚੁੱਪ ਕਰ ਜਾਂਦਾ ਹੈ", "the text falls silent", "the source says nothing about this"),
            ("ਜਾਣ-ਬੁੱਝ ਕੇ", "knowingly, on purpose", "done deliberately rather than by accident"),
            ("ਦੋਹਾਂ ਵਿੱਚ ਫ਼ਰਕ", "the difference between the two", "what separates two versions"),
            ("ਸਹਿਮਤ ਨਹੀਂ", "not in agreement", "the polite beginning of a disagreement"),
            ("ਰਿਕਾਰਡ ਸਾਫ਼", "the record is clean", "the correction has been made public"),
            ("ਧੰਨਵਾਦ ਸਹਿਤ", "along with thanks", "the polite close of a correction"),
            ("ਲਹਿਜਾ ਬਦਲਣਾ", "for the tone to change", "the same matter sounded differently"),
        ],
        mistakes=[
            ("ਕਥਾ ਦਾ ਢਾਂਚਾ ਤਿੰਨ ਹਿੱਸੇ ਬਣਦਾ ਹੈ।", "ਕਥਾ ਦਾ ਢਾਂਚਾ ਤਿੰਨ ਹਿੱਸਿਆਂ ਵਿੱਚ ਬਣਦਾ ਹੈ।", "A structure is described with ਵਿੱਚ."),
            ("ਸੋਧ ਛਾਪਿਆ ਗਿਆ।", "ਸੋਧ ਛਾਪੀ ਗਈ।", "ਸੋਧ is feminine: ਛਾਪੀ ਗਈ."),
            ("ਦੋਹਾਂ ਵਿੱਚ ਫ਼ਰਕ ਇਹ ਹੈ ਕਿ ਲਹਿਜਾ ਤਿੱਖਾ ਹੈ ਕਿ।", "ਦੋਹਾਂ ਵਿੱਚ ਫ਼ਰਕ ਇਹ ਹੈ ਕਿ ਲਹਿਜਾ ਤਿੱਖਾ ਹੈ।", "One ਕਿ opens the clause."),
        ],
        task_title="Write a 300-word review of a Punjabi classic, in Punjabi",
        task_instructions=("Write a Punjabi review of one folk telling in three short paragraphs. "
                           "Open with the shape: ਭੂਮਿਕਾ, ਵਿਛੋੜਾ, ਅੰਤ. In the middle state one claim "
                           "with ਦਾਅਵਾ ਇਹ ਹੈ ਕਿ and hold it to two lines of evidence with ਸਬੂਤ ਵਜੋਂ. "
                           "Compare it with one other version (ਦੋਹਾਂ ਵਿੱਚ ਫ਼ਰਕ ਇਹ ਹੈ ਕਿ), then close "
                           "by naming the limit with ਹੱਦ ਇੱਥੇ ਖ਼ਤਮ ਹੁੰਦੀ ਹੈ and adding one line of "
                           "ਸੁਝਾਅ for the reader."),
    ),
    "test": [
        ("translate_en", "Say: the limit of the interpretation ends here.", "ਵਿਆਖਿਆ ਦੀ ਹੱਦ ਇੱਥੇ ਖ਼ਤਮ ਹੁੰਦੀ ਹੈ।"),
        ("translate_pa", "ਦੋਹਾਂ ਵਿੱਚ ਫ਼ਰਕ ਇਹ ਹੈ ਕਿ ਲਹਿਜਾ ਤਿੱਖਾ ਹੈ।", "The difference between the two is that the tone is sharper."),
        ("multiple_choice", "Which sentence brings in the evidence?", "ਇਸ ਦਾ ਸਬੂਤ ਇਹ ਹੈ ਕਿ ਵਿਆਹ ਦੀ ਗੱਲ ਪੁੱਛੀ ਨਹੀਂ ਜਾਂਦੀ।"),
        ("fill_in_the_blank", "ਹੀਰ ਦੀ ਬਣਾਵਟ ਬੋਲੀ ___ ਬਣਦੀ ਹੈ।", "ਰਾਹੀਂ"),
        ("word_selection", "Select the Punjabi for 'version'.", "ਸੰਸਕਰਨ"),
        ("error_correction", "ਸੋਧ ਛਾਪਿਆ ਗਿਆ।", "ਸੋਧ ਛਾਪੀ ਗਈ।"),
        ("dialogue_completion", "Complete: ਸੰਭਵ ਹੈ ਕਿ ਕਵੀ ਨੇ ਜਾਣ-ਬੁੱਝ ਕੇ ਲਿਖਿਆ, ___ ਸਿੱਧ ਨਹੀਂ। (but not proved)", "ਪਰ"),
        ("matching", "Match ਕੱਸਵੱਟੀ ਲੱਗਣੀ to its meaning.", "to stand up under a test"),
        ("reading_comprehension", "ਵਾਰਿਸ ਸ਼ਾਹ ਨੇ ‘ਹੀਰ’ ਕਦੋਂ ਲਿਖੀ?", "in 1766"),
        ("inference", "ਲੇਖਕ ਆਪਣੀ ਵਿਆਖਿਆ ਦੀ ਹੱਦ ਦੱਸਦਾ ਹੈ। — what does this show about the review?", "it is honest about what the text cannot prove"),
        ("main_idea", "ਦੋਹਾਂ ਸੰਸਕਰਨਾਂ ਵਿੱਚ ਭਾਵ ਨਹੀਂ ਬਦਲਦਾ, ਲਹਿਜਾ ਬਦਲਦਾ ਹੈ। — what is this sentence?", "a comparison of tone between two versions"),
        ("detail_identification", "ਕਥਾ ਦਾ ਦਾਰੂ ਕੀ ਹੈ?", "that nobody asks anybody's wish"),
    ],
}

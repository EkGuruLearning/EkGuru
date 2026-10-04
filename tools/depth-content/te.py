# -*- coding: utf-8 -*-
"""Telugu PHASE 1 depth — six CEFR extras, third lessons, and five half-steps.

The existing Telugu course is in `data/courses/phase-1/te_*.json`; this module
adds the authored PHASE 1 surfaces with `tools/author-depth.py --lang te`.

House style follows the course's marked Telugu romanisation: lowercase for
vocabulary, sentence case for examples and dialogue; ā/ī/ū/ē/ō, ṭ/ḍ/ṇ/ḷ/ṟ,
ś/ṣ and ṁ stay visible. The small transliterator below is deliberately limited
to ordinary Telugu orthography and is self-checked against shipped examples.
Telugu remains awaiting native-speaker review; this is not a pronunciation
certificate.

The course teaches a careful written register, not a claim that regional or
spoken Telugu is less correct. At beginner level the module uses మీరు and the
respectful plural verb; later lessons practise case suffixes, quotative అని,
converb/participial clauses, focus, evidential stance and register choices.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # tools/ on the path
from depth_kit import D, EXTRA, G, L, T, V, WS, X   # noqa: E402

CODE = "te"
NAME = "Telugu"
NATIVE = "తెలుగు"
PHASE = 1
SCRIPT = "Telugu script"
VOICE = "te-IN"
SKILL = ("Telugu: the Telugu abugida, vowel signs and virama, case suffixes, "
         "verb-final clauses, మీరు with respectful agreement, quotative అని, "
         "and the difference between a written standard and regional speech")

# The scheme is the marked scheme already printed in the shipped Telugu A1/A2
# vocabulary lane. Consonants carry inherent a unless a vowel sign or virama
# says otherwise; this is a reading aid, not a claim of a single official Latin
# spelling for every Telugu word.
_VOWELS = {
    "అ": "a", "ఆ": "ā", "ఇ": "i", "ఈ": "ī", "ఉ": "u", "ఊ": "ū",
    "ఋ": "ṛ", "ౠ": "ṝ", "ఌ": "ḷ", "ౡ": "ḹ", "ఎ": "e", "ఏ": "ē",
    "ఐ": "ai", "ఒ": "o", "ఓ": "ō", "ఔ": "au",
}
_SIGNS = {
    "ా": "ā", "ి": "i", "ీ": "ī", "ు": "u", "ూ": "ū", "ృ": "ṛ",
    "ౄ": "ṝ", "ౢ": "ḷ", "ౣ": "ḹ", "ె": "e", "ే": "ē", "ై": "ai",
    "ొ": "o", "ో": "ō", "ౌ": "au",
}
_CONSONANTS = {
    "క": "k", "ఖ": "kh", "గ": "g", "ఘ": "gh", "ఙ": "ṅ",
    "చ": "ch", "ఛ": "chh", "జ": "j", "ఝ": "jh", "ఞ": "ñ",
    "ట": "ṭ", "ఠ": "ṭh", "డ": "ḍ", "ఢ": "ḍh", "ణ": "ṇ",
    "త": "t", "థ": "th", "ద": "d", "ధ": "dh", "న": "n",
    "ప": "p", "ఫ": "ph", "బ": "b", "భ": "bh", "మ": "m",
    "య": "y", "ర": "r", "ఱ": "ṟ", "ల": "l", "ళ": "ḷ", "ఴ": "ḻ",
    "వ": "v", "శ": "ś", "ష": "ṣ", "స": "s", "హ": "h",
}
_VIRAMA = "్"
_JOINERS = {"\u200c", "\u200d"}


def romanise(text: str, sentence: bool = False) -> str:
    """Transliterate standard Telugu letters/signs to the course's marked scheme."""
    out: list[str] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch in _CONSONANTS:
            out.append(_CONSONANTS[ch])
            i += 1
            if i < len(text) and text[i] == _VIRAMA:
                i += 1
                if i < len(text) and text[i] in _JOINERS:
                    i += 1
                continue
            if i < len(text) and text[i] in _SIGNS:
                out.append(_SIGNS[text[i]])
                i += 1
                continue
            out.append("a")
            continue
        if ch in _VOWELS:
            out.append(_VOWELS[ch])
        elif ch == "ం":
            # The course romanisation writes a nasal homorganic with the next
            # stop (e.g. తెరవండి → teravaṇḍi); retain ṁ when no stop follows.
            following = text[i + 1] if i + 1 < len(text) else ""
            if following and following in "కఖగఘఙ":
                out.append("ṅ")
            elif following and following in "చఛజఝఞ":
                out.append("ñ")
            elif following and following in "టఠడఢణ":
                out.append("ṇ")
            elif following and following in "తథదధన":
                out.append("n")
            elif following and following in "పఫబభమ":
                out.append("m")
            else:
                out.append("ṁ")
        elif ch == "ః":
            out.append("ḥ")
        elif ch == "ఁ":
            out.append("m̃")
        elif ch in _JOINERS or ch == _VIRAMA:
            pass
        elif ch == "఼":
            # Nukta is rare in ordinary Telugu; retain a visible marker rather
            # than silently pretending the modified sound is the base letter.
            out.append("̇")
        else:
            out.append(ch)
        i += 1
    result = "".join(out)
    if sentence:
        for index, char in enumerate(result):
            if char.isalpha() and char.lower() != char.upper():
                result = result[:index] + char.upper() + result[index + 1:]
                break
    return result


# Sanity-check the transliteration against forms already present in te_A1.
assert romanise("డాక్టర్") == "ḍākṭar"
assert romanise("చదవండి", sentence=True) == "Chadavaṇḍi"
assert romanise("ఒంట్లో బాగాలేదు", sentence=True) == "Oṇṭlō bāgālēdu"
assert romanise("పుస్తకం") == "pustakaṁ"
assert romanise("అందరూ") == "andarū"


def _vocab(rows):
    return [V(t, romanise(t), en, pos) for t, en, pos in rows]


def _examples(rows):
    return [X(t, romanise(t, sentence=True), en) for t, en in rows]


def _turns(rows):
    return [D(sp, t, romanise(t, sentence=True), en) for sp, t, en in rows]


def _lesson(title, aim, vocab, grammar, examples, mistakes, dialogue, worksheet):
    """A compact authoring surface; all target text and glosses stay explicit."""
    gtitle, pattern, explanation = grammar
    wtitle, tasks = worksheet
    return L(
        title, aim, _vocab(vocab),
        G(gtitle, pattern, explanation, _examples(examples), mistakes),
        _turns(dialogue),
        WS(wtitle, [T(instruction, items, key) for instruction, items, key in tasks]),
    )


def _extra(culture, source, reading, gloss, listening, listening_gloss,
           idioms, mistakes, task_title, task_instructions):
    return EXTRA(culture, source, reading, gloss, listening, listening_gloss,
                 VOICE, idioms, mistakes, task_title, task_instructions)


EXTRAS = {}
THIRD = {}
HALFSTEPS = {}

# ── the six CEFR rungs: culture, reading, listening, ten expressions, task ──
EXTRAS["A1"] = _extra(
    culture=("Telugu is written in its own left-to-right script. A consonant normally carries "
             "an inherent short a; a vowel sign changes that sound, and the virama (్) removes "
             "it or helps write a consonant cluster. A learner can therefore read a syllable by "
             "looking at the consonant and the mark attached to it, rather than treating every "
             "printed shape as an unrelated letter. Telugu and Kannada scripts also share a "
             "historical stage, though each is a distinct script and language."),
    source="https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-12/",
    reading=("నా పేరు అనన్య. నేను విజయవాడలో ఉంటాను. మా ఇంట్లో తెలుగు పుస్తకాలు ఉన్నాయి. "
             "ఈ రోజు నేను అచ్చులు, హల్లులు చదువుతున్నాను. మా ఉపాధ్యాయుడు ఒక అక్షరాన్ని "
             "బోర్డుపై రాశారు. నేను దాన్ని పలికి, నా పుస్తకంలో మళ్లీ రాశాను. ఇప్పుడు "
             "చిన్న పదాలను నెమ్మదిగా చదవగలను."),
    gloss=("My name is Ananya. I live in Vijayawada. There are Telugu books in our home. "
           "Today I am reading vowels and consonants. Our teacher wrote one letter on the "
           "board. I pronounced it and wrote it again in my book. Now I can read short words "
           "slowly."),
    listening=("అనన్య: నమస్కారం, ఇది తెలుగు తరగతి ఎక్కడ?<br>"
               "ఉపాధ్యాయుడు: ఈ గది చివర ఉంది. నెమ్మదిగా రండి.<br>"
               "అనన్య: ధన్యవాదాలు. నేను కొత్త విద్యార్థిని.<br>"
               "ఉపాధ్యాయుడు: స్వాగతం. మీ పుస్తకం తెరవండి."),
    listening_gloss=("Ananya: Hello, where is the Telugu class? Teacher: It is at the end of "
                     "this corridor. Please come slowly. Ananya: Thank you. I am a new student. "
                     "Teacher: Welcome. Open your book."),
    idioms=[
        ("అక్షరాలా", "letter by letter", "exactly as written; literally"),
        ("కంటికి రెప్పలా కాపాడటం", "to guard like an eyelid guards an eye", "to protect very carefully"),
        ("తలపట్టుకోవడం", "to hold one's head", "to feel puzzled or overwhelmed"),
        ("నోరు జారడం", "for the mouth to slip", "to say something unintentionally"),
        ("కళ్లకు కట్టినట్టు", "as if tied before the eyes", "vividly and clearly"),
        ("నోటికి తాళం వేయడం", "to put a lock on the mouth", "to keep quiet"),
        ("మాట నిలబెట్టుకోవడం", "to keep one's word standing", "to honour a promise"),
        ("కాళ్ల మీద నిలబడటం", "to stand on one's feet", "to become self-reliant"),
        ("చెవిలో పెట్టుకోవడం", "to place something in the ear", "to listen to and remember advice"),
        ("ఒక్క మాటలో", "in one word", "in a nutshell"),
    ],
    mistakes=[
        ("నా పేరు నాకు అనన్య.", "నా పేరు అనన్య.", "A name is introduced directly; the dative నాకు does not belong in this pattern."),
        ("నేను పాఠశాల వెళ్తాను.", "నేను పాఠశాలకు వెళ్తాను.", "A destination takes the dative suffix -కు: పాఠశాలకు."),
        ("మీరు రా.", "మీరు రండి.", "Respectful మీరు takes the respectful imperative రండి, not the familiar రా."),
    ],
    task_title="తెలుగు అక్షరాలతో స్వపరిచయం",
    task_instructions=("Write six short Telugu sentences: your name, town, one person at home, a "
                       "book you read, a letter you are practising, and a polite question to a "
                       "classmate. Underline two vowel signs and one virama. Read the sentences "
                       "slowly, then copy one of them without looking at the model."),
)

EXTRAS["A2"] = _extra(
    culture=("Ugadi marks a new year for many Telugu-speaking families. The Government of "
             "India's festival description notes the custom of preparing Ugadi pachadi, a "
             "mixture associated with six tastes: sweet, salty, sour, bitter, tangy and spicy. "
             "Households may vary the ingredients and proportions; the useful language lesson "
             "is to name a taste, describe a recipe and ask what someone prefers without "
             "assuming every family celebrates in exactly the same way."),
    source="https://utsav.gov.in/view-event/ugadi-telugu-new-year",
    reading=("ఉగాది ముందు రోజు మా ఇంట్లో పనులు మొదలయ్యాయి. అమ్మ చింతపండు నానబెట్టింది; "
             "నేను మామిడికాయను చిన్న ముక్కలుగా కోశాను. నాన్న బెల్లం, ఉప్పు, మిరపకాయ "
             "తీసుకొచ్చారు. అమ్మమ్మ ఒక్కొక్క పదార్థం కలిపి రుచి చూసింది. ఎవరికీ ఒకే రుచి "
             "నచ్చలేదు, కాబట్టి చివరికి అందరం కొద్దిగా చేర్చుకున్నాం. భోజనానికి ముందు "
             "పచ్చడిని పంచుకున్నాం."),
    gloss=("The work began at our home on the day before Ugadi. Mother soaked the tamarind; "
           "I cut the raw mango into small pieces. Father brought jaggery, salt and chilli. "
           "Grandmother mixed each ingredient and tasted it. Nobody liked exactly the same "
           "taste, so in the end we each added a little. We shared the pachadi before the meal."),
    listening=("రేఖ: పచ్చడిలో ఇంకా ఏమి కలపాలి?<br>"
               "కిరణ్: కొద్దిగా బెల్లం కలపండి; నాకు తీపి ఎక్కువగా నచ్చుతుంది.<br>"
               "రేఖ: నాకు పులుపు ఇష్టం. చింతపండు సరిపోతుందా?<br>"
               "కిరణ్: అవును, ముందు కొద్దిగా వేసి రుచి చూడండి."),
    listening_gloss=("Rekha: What else should we add to the pachadi? Kiran: Add a little "
                     "jaggery; I like it sweeter. Rekha: I like sourness. Is the tamarind "
                     "enough? Kiran: Yes, add a little first and taste it."),
    idioms=[
        ("తీపి కబురు", "sweet news", "good news"),
        ("చేతులు కలపడం", "to join hands", "to cooperate"),
        ("ముఖం వెలిగిపోవడం", "for the face to light up", "to look delighted"),
        ("ఇంటి దారి పట్టడం", "to take the road home", "to head home"),
        ("కడుపు నిండా", "with the stomach full", "to one's fill"),
        ("మాట మీద నిలబడటం", "to stand by one's word", "to keep a promise"),
        ("హడావుడి చేయడం", "to make a commotion", "to rush about in a hurry"),
        ("ఒక అడుగు ముందుకు వేయడం", "to take one step forward", "to make progress"),
        ("చేతికి అందడం", "to reach the hand", "to become available or manageable"),
        ("పండగ చేసుకోవడం", "to celebrate a festival", "to enjoy or celebrate something fully"),
    ],
    mistakes=[
        ("నేను పచ్చడి కావాలి.", "నాకు పచ్చడి కావాలి.", "కావాలి normally frames the person who wants something with the dative నాకు."),
        ("అమ్మ మామిడికాయ కోశారు.", "అమ్మ మామిడికాయను కోశారు.", "The definite object is marked with -ను here: మామిడికాయను."),
        ("మీరు కలుపు.", "మీరు కలపండి.", "A respectful request to మీరు uses the plural imperative కలపండి."),
    ],
    task_title="ఉగాది వంటకు చిన్న ప్రణాళిక",
    task_instructions=("Write a short recipe plan for a family meal: name four ingredients, say "
                       "who will prepare each one, give two quantity instructions, and ask one "
                       "person about a preferred taste. Use ముందు, తరువాత and చివరికి to make "
                       "the order clear. Add one sentence that acknowledges that tastes differ."),
)

EXTRAS["B1"] = _extra(
    culture=("Bathukamma is a floral festival strongly associated with Telangana. The state's "
             "official culture page describes flower stacks, group songs and gatherings, with "
             "the celebration culminating in immersion of the floral arrangements in nearby "
             "tanks or lakes. Seasonal flowers and local practice matter, so the lesson treats "
             "Bathukamma as a living regional tradition rather than a single recipe or a "
             "performance that every Telugu-speaking household observes in the same way."),
    source="https://www.telangana.gov.in/about/language-culture/",
    reading=("మా వీధిలో బతుకమ్మ వేడుకకు అందరూ కలిసి ఏర్పాట్లు చేశారు. కొందరు పూలు "
             "తీసుకొచ్చారు; మరికొందరు వలయంగా కూర్చోవడానికి చోటు సిద్ధం చేశారు. పెద్దవారు "
             "పాట మొదలుపెట్టినప్పుడు పిల్లలు కూడా స్వరంతో కలిశారు. కార్యక్రమం తర్వాత "
             "పూలను చెరువు దగ్గరకు తీసుకెళ్లారు. నిర్వాహకులు నీటి ప్రదేశాన్ని శుభ్రంగా "
             "ఉంచాలని అందరికీ గుర్తు చేశారు."),
    gloss=("Everyone on our street prepared together for the Bathukamma gathering. Some "
           "brought flowers; others prepared a place to sit in a circle. When the elders "
           "started a song, children joined in too. After the programme, they took the flowers "
           "to the tank. The organisers reminded everyone to keep the waterside clean."),
    listening=("లత: పూల బుట్టలు వచ్చాయా?<br>"
               "సుధ: వచ్చాయి, కానీ పాటల జాబితా ఇంకా సిద్ధం కాలేదు.<br>"
               "లత: నేను పెద్దవారితో మాట్లాడి క్రమం రాసుకుంటాను.<br>"
               "సుధ: బాగుంది. నీటి దగ్గర చెత్త వేయకూడదని కూడా చెప్పాలి."),
    listening_gloss=("Latha: Have the flower baskets arrived? Sudha: They have, but the song "
                     "list is not ready yet. Latha: I will speak with the elders and write down "
                     "the order. Sudha: Good. We should also say that rubbish must not be left "
                     "near the water."),
    idioms=[
        ("ఊపిరి పీల్చుకోవడం", "to draw a breath", "to feel relief after worry"),
        ("ఒకే తాటిపైకి రావడం", "to come onto one plank", "to reach agreement"),
        ("విషయం వెలుగులోకి రావడం", "for a matter to come into the light", "for something to become known"),
        ("కంటిమీద కునుకు లేకుండా", "without a wink on the eye", "without sleeping at all"),
        ("చేతులు ముడుచుకొని కూర్చోవడం", "to sit with folded hands", "to stay idle instead of helping"),
        ("దారిచూపడం", "to show the way", "to guide someone"),
        ("మనసు విప్పి మాట్లాడడం", "to speak with the heart opened", "to speak frankly"),
        ("కలిసి కట్టుగా", "tied together", "as a united group"),
        ("కన్నుల పండుగ", "a feast for the eyes", "a beautiful sight"),
        ("వేరు వేయడం", "to put down a root", "to become firmly established"),
    ],
    mistakes=[
        ("వాళ్లు పూలు నీటిలో వేసారు.", "వాళ్లు పూలను నీటిలో వేశారు.", "Mark the definite object with -ను, and use the written past form వేశారు."),
        ("పాట మొదలైనప్పుడు పిల్లలు కూడా పాడారు.", "పాట మొదలుపెట్టినప్పుడు పిల్లలు కూడా పాడారు.", "మొదలైనప్పుడు means when it began; this sentence needs the agentive 'when they started' form."),
        ("అందరూ కలిసి ఏర్పాట్లు చేసింది.", "అందరూ కలిసి ఏర్పాట్లు చేశారు.", "The human plural subject అందరూ takes plural agreement చేశారు."),
    ],
    task_title="సమాజ వేడుకకు బాధ్యతల పంచకం",
    task_instructions=("Write a short note for a neighbourhood group: describe two tasks already "
                       "completed, assign two tasks still to do, and give a reason to protect the "
                       "waterfront. Use కలిసి, తరువాత, ఎందుకంటే and ఒకవేళ at least once. Finish "
                       "with one sentence that invites people to help without assuming everyone "
                       "celebrates in the same way."),
)

EXTRAS["B2"] = _extra(
    culture=("Kuchipudi is a Telugu dance-drama tradition associated with the village of "
             "Kuchipudi in Andhra Pradesh's Krishna district. The district's cultural-tourism "
             "description presents it as a performance art with dance and dramatic elements. "
             "For a learner, that means the language of a rehearsal includes directions, "
             "characters, entrances and expressive lines; a stage version is not simply a "
             "sequence of steps without story."),
    source="https://krishna.ap.gov.in/cultural-tourism/",
    reading=("కూచిపూడి బృందం కొత్త ప్రదర్శనకు సాధన చేసింది. నర్తకి ఒక పాత్ర భావాన్ని "
             "ముఖాభినయంతో చూపించింది; సంగీతకారుడు తాళాన్ని నెమ్మదిగా ఉంచాడు. గురువు "
             "మధ్య భాగంలో అడుగుల క్రమం మార్చమన్నారు. బృందం మళ్లీ సాధన చేసిన తర్వాత "
             "కథ ప్రేక్షకులకు స్పష్టంగా కనిపించింది. ముగింపులో అందరూ సమయానికి వేదిక "
             "వెనుకకు వెళ్లారు."),
    gloss=("The Kuchipudi group rehearsed for a new performance. The dancer showed a "
           "character's feeling through facial expression; the musician kept the rhythm slow. "
           "The teacher asked them to change the order of steps in the middle section. After "
           "the group rehearsed again, the story became clear to the audience. At the end, "
           "everyone went backstage on time."),
    listening=("గురువు: రెండో దృశ్యంలో పాత్ర ఎందుకు ఆగుతుంది?<br>"
               "నర్తకి: ఆమెకు వార్త విన్న తర్వాత సందేహం కలుగుతుంది.<br>"
               "సంగీతకారుడు: ఆ క్షణంలో తాళం తగ్గించనా?<br>"
               "గురువు: అవును, అప్పుడు భావం ప్రేక్షకులకు చేరుతుంది."),
    listening_gloss=("Teacher: Why does the character pause in the second scene? Dancer: "
                     "After hearing the news, she becomes uncertain. Musician: Should I slow "
                     "the rhythm at that moment? Teacher: Yes; then the feeling will reach the "
                     "audience."),
    idioms=[
        ("రంగంలోకి దిగడం", "to step into the arena", "to begin taking action"),
        ("కథకు ప్రాణం పోయడం", "to breathe life into a story", "to make a story vivid"),
        ("మాటకు మారు మాట", "a reply to each word", "a continuing back-and-forth exchange"),
        ("తాళం తప్పకుండా", "without losing the beat", "steadily and in rhythm"),
        ("అరంగేట్రం చేయడం", "to make an entry onto the stage", "to make a debut"),
        ("భావం పలకడం", "for a feeling to speak", "for an emotion to come across"),
        ("చూపు తిప్పుకోలేకపోవడం", "to be unable to turn one's gaze away", "to be absorbed by a performance"),
        ("చేతికి పని ఇవ్వడం", "to give work to the hand", "to keep oneself usefully occupied"),
        ("స్వరానికి తాళం కలపడం", "to join rhythm to a melody", "to coordinate music and movement"),
        ("చప్పట్లు మారుమోగడం", "for applause to echo", "for the audience to applaud loudly"),
    ],
    mistakes=[
        ("నర్తకి భావాన్ని ముఖం చూపించింది.", "నర్తకి భావాన్ని ముఖాభినయంతో చూపించింది.", "Use ముఖాభినయం for expressive facial acting; ముఖం alone names the face."),
        ("గురువు అడుగులు మార్చమని చెప్పింది.", "గురువు అడుగులు మార్చమని చెప్పారు.", "This respectful reference to a teacher uses plural honorific agreement చెప్పారు."),
        ("ప్రేక్షకులకు కథ స్పష్టంగా కనిపించింది తరువాత.", "తర్వాత ప్రేక్షకులకు కథ స్పష్టంగా కనిపించింది.", "Place the time connector before the clause it introduces."),
    ],
    task_title="సాధనకు దర్శకుని గమనిక",
    task_instructions=("Write a rehearsal note with three parts: describe what the dancer "
                       "changes, explain what the musician should do at that moment, and say "
                       "how the audience will understand the story. Use అయినప్పుడు, కాబట్టి "
                       "and ప్రేక్షకులకు. End with one respectful request to a performer."),
)

EXTRAS["C1"] = _extra(
    culture=("Telugu literary history includes translation as creative work. Encyclopaedia "
             "Britannica describes Nannaya Bhatta's eleventh-century poetic rendering of part "
             "of the Mahabharata and notes that Tikkana and Errana later continued the Telugu "
             "version. A regional-language retelling need not be a word-for-word copy: choices "
             "of metre, vocabulary, emphasis and audience shape how an inherited story is "
             "heard. This is a useful setting for practising attribution and qualified claims."),
    source="https://www.britannica.com/biography/Nannaya-Bhatta",
    reading=("నన్నయ రచనను చదివేటప్పుడు అనువాదం అంటే పదానికి పదం మార్చడం మాత్రమే కాదని "
             "గుర్తుంచుకోవాలి. కవితా ఛందస్సు, పాఠకుల పరిచయం, కథలోని ప్రాధాన్యం కలిసి "
             "రూపాన్ని నిర్ణయిస్తాయి. తరువాతి కవులు అదే మహాకావ్య సంప్రదాయాన్ని కొనసాగించినా, "
             "ప్రతి రచనకు తన కాలపు భాష, శైలి, అవసరం ఉంటాయి. అందువల్ల పరిశోధకుడు మూలాన్ని "
             "చూడటంతో పాటు, రచయిత ఎంచుకున్న మార్గాన్ని కూడా వివరించాలి."),
    gloss=("When reading Nannaya's work, remember that translation is not only replacing one "
           "word with another. Poetic metre, readers' familiarity and the story's emphasis "
           "together shape the form. Later poets continued the same epic tradition, but each "
           "work has the language, style and needs of its own time. A researcher should therefore "
           "look at the source and also explain the path chosen by the writer."),
    listening=("సంపాదకుడు: ఈ భాగాన్ని నేరుగా అనువదించాలా?<br>"
               "పరిశోధకుడు: మూల భావం నిలవాలి, కానీ ఛందస్సును కూడా గమనించాలి.<br>"
               "సంపాదకుడు: ఒక పదానికి రెండు అర్థాలు కనిపిస్తున్నాయి.<br>"
               "పరిశోధకుడు: సందర్భాన్ని చూపించి, మన ఎంపికకు కారణం చెప్పండి."),
    listening_gloss=("Editor: Should we translate this passage literally? Researcher: The core "
                     "meaning should remain, but we should also notice the metre. Editor: One "
                     "word seems to have two meanings. Researcher: Show the context and explain "
                     "the reason for our choice."),
    idioms=[
        ("సారం పిండుకోవడం", "to press out the essence", "to extract the central point"),
        ("తూకం వేసి మాట్లాడడం", "to weigh words before speaking", "to speak with care"),
        ("ఆలోచనకు పదును పెట్టడం", "to sharpen a thought", "to refine an argument"),
        ("అర్థం తేటతెల్లం కావడం", "for meaning to become crystal clear", "for the meaning to become explicit"),
        ("మాటలో ముల్లు", "a thorn in the words", "a pointed or hurtful remark"),
        ("ఒక అడుగు వెనక్కి వేయడం", "to take one step back", "to reconsider before proceeding"),
        ("సందేహం నివృత్తి చేయడం", "to remove a doubt", "to clarify an uncertainty"),
        ("పలుకుబడి చూపించడం", "to show one's influence", "to use one's standing to affect a decision"),
        ("గీత దాటకపోవడం", "not to cross the line", "to stay within an agreed limit"),
        ("మూలం వెతకడం", "to search for the source", "to trace where an idea or text began"),
    ],
    mistakes=[
        ("కవి ఈ భావాన్ని పదానికి పదం మార్చాడు.", "కవి ఈ భావాన్ని తన శైలిలో మలిచాడు.", "The first sentence claims literal replacement; use మలిచాడు when discussing an interpretive rendering."),
        ("మూలంలో ఉన్న భావం మారినప్పటికీ అదే అర్థం.", "మూలంలోని భావం నిలిచినా, పదప్రయోగం మారింది.", "Use the concessive/result relation that matches the intended claim; మారినప్పటికీ says the meaning changed."),
        ("రచయిత ఎంచుకున్న పదం గురించి వివరించాలి అని పరిశోధకుడు అన్నారు.", "రచయిత ఎంచుకున్న పదం గురించి వివరించాలని పరిశోధకుడు అన్నారు.", "The reported request takes the purposive complement -అని is not needed after the infinitive-like -అని structure here."),
    ],
    task_title="అనువాద ఎంపికపై సంపాదకీయ గమనిక",
    task_instructions=("Write a short editorial note about one translation choice. Name the source "
                       "idea, state what the Telugu wording preserves, identify one nuance that "
                       "does not transfer directly, and explain the choice without calling it "
                       "the only possible version. Attribute the claim and use అయినప్పటికీ and "
                       "అందువల్ల to connect the reasoning."),
)

EXTRAS["C2"] = _extra(
    culture=("Telugu is a Dravidian language with regional speech varieties and a long literary "
             "history. Britannica notes both regional variation and a historical Telugu–Kannada "
             "script stage; it also describes lexical interaction between the languages. These "
             "facts are a reminder that language boundaries, scripts and standards are related "
             "but not interchangeable. In advanced writing, it is more accurate to name the "
             "variety or register being discussed than to treat one speaker's form as the only "
             "Telugu."),
    source="https://www.britannica.com/topic/Dravidian-languages/Literary-languages",
    reading=("ఒక ప్రజా ప్రకటనలో ప్రామాణిక పదరూపం ఉపయోగించారు; ఇంటి సంభాషణలో అదే భావాన్ని "
             "ప్రాంతీయ పలుకుబడితో చెప్పారు. రెండింటి పని వేరు: ప్రకటన అందరికీ ఒకే విధంగా "
             "అర్థమయ్యేలా ఉండాలి, సంభాషణ మాత్రం పరిచయాన్ని చూపవచ్చు. ఒక రూపాన్ని "
             "మరొకదానికంటే 'మంచిది' అని తేల్చే ముందు సందర్భం, పాఠకుడు, ఉద్దేశం ఏమిటో "
             "తెలుసుకోవాలి. సవరించిన పాఠ్యంలో రెండు రూపాలనూ అవసరమైన చోట వివరించడం "
             "స్పష్టతను పెంచుతుంది."),
    gloss=("A public notice used a standard written form; in a home conversation the same idea "
           "was expressed with regional pronunciation. Their jobs differ: the notice should be "
           "understood consistently by a broad audience, while conversation can signal familiarity. "
           "Before deciding that one form is 'better' than another, identify the context, reader "
           "and purpose. Explaining both forms where needed can make an edited text clearer."),
    listening=("మధ్యవర్తి: ఈ పదాన్ని ప్రకటనలో మార్చాలా?<br>"
               "సమీక్షకుడు: లక్ష్య పాఠకులు ఎవరో ముందుగా నిర్ణయిద్దాం.<br>"
               "మధ్యవర్తి: ప్రాంతీయ రూపాన్ని ఉదాహరణగా ఉంచితే ఎలా ఉంటుంది?<br>"
               "సమీక్షకుడు: ఉంచవచ్చు; దాని పరిధిని స్పష్టంగా చెప్పాలి."),
    listening_gloss=("Mediator: Should we change this word in the notice? Reviewer: Let us first "
                     "decide who the intended readers are. Mediator: What if we keep the regional "
                     "form as an example? Reviewer: We can; we should state its scope clearly."),
    idioms=[
        ("తాడును పామనుకోవడం", "to mistake a rope for a snake", "to misread a situation through fear"),
        ("రెండు వైపులా చూడడం", "to look at both sides", "to consider competing perspectives"),
        ("మాట మింగేయడం", "to swallow one's words", "to hold back what one was about to say"),
        ("అసలు విషయానికి రావడం", "to come to the actual matter", "to get to the point"),
        ("గొంతు కలపడం", "to add one's voice", "to join a discussion or cause"),
        ("పరిధి దాటడం", "to cross the boundary", "to go beyond the agreed scope"),
        ("ముఖం నిలబెట్టడం", "to keep someone's face standing", "to help someone save face"),
        ("మాట మార్చడం", "to change one's words", "to change one's position or story"),
        ("వెనుకడుగు వేయడం", "to take a step back", "to retreat or reconsider"),
        ("చిత్రం స్పష్టంగా కనిపించడం", "for the picture to appear clearly", "for the overall situation to become clear"),
    ],
    mistakes=[
        ("ఈ ప్రాంతీయ రూపం తప్పు; దాన్ని తొలగించాలి.", "ఈ పాఠకుల కోసం ప్రామాణిక రూపం అవసరం; ప్రాంతీయ రూపాన్ని ఉదాహరణగా ఉంచవచ్చు.", "A register choice is not proof that another regional form is wrong; state the audience and purpose."),
        ("రెండు రూపాలు ఒకటే అని నిర్ణయించాలి.", "రెండు రూపాల మధ్య తేడా ఏ సందర్భంలో ముఖ్యమో వివరించాలి.", "Do not erase a distinction before checking its context and use."),
        ("పాఠకుడు అర్థం చేసుకోకపోవచ్చు అయినప్పటికీ వివరణ ఇవ్వాలి.", "పాఠకుడు అర్థం చేసుకోకపోవచ్చు కాబట్టి వివరణ ఇవ్వాలి.", "Use కారణం కోసం కాబట్టి; అయినప్పటికీ marks a concession, not a cause."),
    ],
    task_title="ప్రాంతీయ రూపంపై సంపాదకీయ నిర్ణయం",
    task_instructions=("Write a two-paragraph editorial decision about a regional Telugu form. "
                       "Name the audience, explain what the form signals in that context, state "
                       "whether the main text or a note should carry it, and give one limitation "
                       "of your choice. Distinguish evidence from opinion and avoid ranking "
                       "speakers as correct or incorrect."),
)


def _third(rung, unit, spec):
    low = rung.lower()
    n = 6 + unit
    return (f"te-{low}-u{unit}", f"te-{low}-l{n}", spec)


# ── eighteen third lessons: one new situation in every shipped unit ──
THIRD["A1"] = [
    _third("A1", 1, _lesson(
        "At the pharmacy: a simple request",
        "Ask for a familiar medicine and explain one basic symptom without turning the exchange into a diagnosis.",
        [("మందుల దుకాణం", "pharmacy", "noun"), ("మాత్ర", "tablet", "noun"), ("జ్వరం", "fever", "noun"), ("రోజుకు", "per day", "adverb"), ("సూచన", "instruction", "noun")],
        ("దాతువు కావాలి and dative need", "నాకు + వస్తువు + కావాలి", "Use నాకు for the person who needs something. Keep the object before కావాలి, then ask politely with కావాలా? A symptom can be stated separately; the phrase does not diagnose its cause."),
        [("నాకు జ్వరానికి మాత్ర కావాలి.", "I need a tablet for fever."), ("ఈ మందు రోజుకు రెండుసార్లు తీసుకోండి.", "Take this medicine twice a day."), ("సూచనను మళ్లీ చెప్పగలరా?", "Could you repeat the instruction?")],
        [("నాకు ఈ మందు కావాలా?", "నాకు ఈ మందు కావాలి.", "The question particle changes the meaning; use కావాలి for a statement of need.")],
        [("కొనుగోలుదారు", "నాకు జ్వరానికి మాత్ర కావాలి.", "I need a tablet for fever."), ("ఔషధ విక్రేత", "వైద్యుడు ఇచ్చిన సూచన ఉందా?", "Do you have an instruction from a doctor?"), ("కొనుగోలుదారు", "అవును, రోజుకు రెండుసార్లు అన్నారు.", "Yes, they said twice a day."), ("ఔషధ విక్రేత", "సరే, లేబుల్ కూడా చదవండి.", "All right, please read the label too.")],
        ("Check the pharmacy exchange", [("Write the symptom and the item you need.", ["జ్వరం", "మాత్ర"], ["fever", "tablet"]), ("Ask for the instructions again politely.", ["సూచనను మళ్లీ చెప్పగలరా?"], ["Could you repeat the instruction?"])])
    )),
    _third("A1", 2, _lesson(
        "A short meeting invitation",
        "Invite a colleague to a brief meeting and make the time and place easy to confirm.",
        [("సమావేశం", "meeting", "noun"), ("గంట", "hour; o'clock", "noun"), ("గది", "room", "noun"), ("ఖాళీ", "free; available", "adjective"), ("రేపు", "tomorrow", "adverb")],
        ("time phrases before the verb", "సమయం + స్థలం + finite verb", "Telugu usually places time and place information before the final verb. Use రేపు with a clock time marked by గంటలకు; an invitation can end with వస్తారా? to ask respectfully."),
        [("రేపు పది గంటలకు సమావేశం ఉంది.", "There is a meeting tomorrow at ten."), ("మీకు ఈ గది ఖాళీగా ఉందా?", "Is this room free for you?"), ("మీరు సమావేశానికి వస్తారా?", "Will you come to the meeting?")],
        [("మీరు సమావేశానికి వస్తావా?", "మీరు సమావేశానికి వస్తారా?", "మీరు takes respectful plural agreement వస్తారా, not familiar వస్తావా.")],
        [("మేనేజర్", "రేపు పది గంటలకు చిన్న సమావేశం ఉంది.", "There is a short meeting tomorrow at ten."), ("కొత్త సహోద్యోగి", "ఏ గదిలో కలవాలి?", "Which room should we meet in?"), ("మేనేజర్", "రెండో అంతస్తులోని గది ఖాళీగా ఉంది.", "The room on the second floor is free."), ("కొత్త సహోద్యోగి", "సరే, నేను సమయానికి వస్తాను.", "All right, I will come on time.")],
        ("Send a clear invitation", [("Write the time and room in one sentence.", ["రేపు పది గంటలకు", "గది"], ["tomorrow at ten", "room"]), ("Write one respectful yes-or-no question.", ["మీరు సమావేశానికి వస్తారా?"], ["Will you come to the meeting?"])])
    )),
    _third("A1", 3, _lesson(
        "Setting a place for dinner",
        "Accept a family invitation and say where the meal will happen.",
        [("విందు", "meal; feast", "noun"), ("పక్కింటి", "next door", "adjective"), ("సమయం", "time", "noun"), ("వంటకం", "dish", "noun"), ("కలిసి", "together", "adverb")],
        ("locative -లో and dative -కి", "స్థలం-లో + వ్యక్తి-కి + కావాలి/ఉంది", "Use -లో for the place where something happens and -కి for the person to whom something is offered or needed. Keep both suffixes attached to their nouns."),
        [("విందు మా ఇంట్లో ఉంది.", "The meal is at our home."), ("మీకు ఏ సమయం సరిపోతుంది?", "What time suits you?"), ("మనం కలిసి కొత్త వంటకం చేస్తాం.", "We will make a new dish together.")],
        [("మా ఇల్లు విందు ఉంది.", "మా ఇంట్లో విందు ఉంది.", "Mark the location with -లో: ఇంట్లో means at the house.")],
        [("అమ్మ", "ఆదివారం మా ఇంట్లో చిన్న విందు ఉంది.", "There is a small meal at our home on Sunday."), ("పక్కింటి వారు", "మీకు ఏ సమయం సరిపోతుంది?", "What time suits you?"), ("అమ్మ", "సాయంత్రం ఆరు గంటలకు రండి.", "Please come at six in the evening."), ("పక్కింటి వారు", "ధన్యవాదాలు, ఒక వంటకం తీసుకొస్తాను.", "Thank you; I will bring one dish.")],
        ("Reply to the invitation", [("Say where and when the meal is.", ["మా ఇంట్లో", "ఆదివారం"], ["at our home", "Sunday"]), ("Offer one dish you can bring.", ["ఒక వంటకం తీసుకొస్తాను"], ["I will bring one dish"])])
    )),
]

THIRD["A2"] = [
    _third("A2", 1, _lesson(
        "Confirming a follow-up appointment",
        "Confirm a follow-up visit, give a time, and describe a symptom that has changed.",
        [("తిరిగి కలవడం", "to meet again", "verb"), ("తగ్గడం", "to lessen", "verb"), ("పరీక్ష", "check-up; test", "noun"), ("ముందస్తు", "advance; prior", "adjective"), ("అపాయింట్‌మెంట్", "appointment", "noun")],
        ("past change and next appointment", "మార్పు + అయింది; తేదీకి + కలవండి", "Use a past form for a change already observed and a date or time phrase for the next step. This is a language model, not medical advice; describe what happened and follow the clinician's instructions."),
        [("నిన్నటి నుంచి జ్వరం తగ్గింది.", "The fever has lessened since yesterday."), ("మళ్లీ పరీక్ష కోసం శుక్రవారం రండి.", "Come Friday for another check-up."), ("నాకు పది గంటల అపాయింట్‌మెంట్ ఉంది.", "I have a ten o'clock appointment.")],
        [("నిన్నటి నుంచి జ్వరం తగ్గుతాను.", "నిన్నటి నుంచి జ్వరం తగ్గింది.", "The sentence reports an observed change, so use past తగ్గింది, not first-person future తగ్గుతాను.")],
        [("వైద్యుడు", "మందు తీసుకున్న తర్వాత ఎలా ఉంది?", "How has it been after taking the medicine?"), ("రోగి", "నిన్నటి నుంచి జ్వరం తగ్గింది.", "The fever has lessened since yesterday."), ("వైద్యుడు", "శుక్రవారం మళ్లీ పరీక్ష చేద్దాం.", "Let us check again on Friday."), ("రోగి", "ఉదయం పది గంటలకు రావచ్చా?", "May I come at ten in the morning?")],
        ("Record the follow-up", [("Write the change since yesterday.", ["నిన్నటి నుంచి", "తగ్గింది"], ["since yesterday", "has lessened"]), ("Confirm the next visit time.", ["శుక్రవారం", "పది గంటలకు"], ["Friday", "at ten o'clock"])])
    )),
    _third("A2", 2, _lesson(
        "A school project on rainwater",
        "Explain how a class will collect and measure rainwater for a simple school project.",
        [("వాననీరు", "rainwater", "noun"), ("సేకరించడం", "to collect", "verb"), ("కొలత", "measurement", "noun"), ("పాత్ర", "container", "noun"), ("ఫలితం", "result", "noun")],
        ("future plan with -తాము", "సమయం/స్థలం + object-ను + verb-తాము", "Use the first-person plural ending -తాము for a plan the group will carry out. Mark a definite object with -ను and describe the result after the action."),
        [("రేపు మేము వాననీటిని సేకరిస్తాము.", "Tomorrow we will collect rainwater."), ("ప్రతి గంటకు కొలత రాస్తాము.", "We will write the measurement every hour."), ("వాన ఆగిన తర్వాత ఫలితాన్ని పోలుస్తాము.", "After the rain stops, we will compare the result.")],
        [("మేము వాననీరు సేకరిస్తాం.", "మేము వాననీటిని సేకరిస్తాము.", "In this definite-object sentence, mark వాననీరు with -ని/-ను: వాననీటిని.")],
        [("ఉపాధ్యాయుడు", "పాత్రను ఎక్కడ పెట్టాలి?", "Where should we place the container?"), ("విద్యార్థిని", "కప్పు కింద ఉంచితే నీరు అందులో పడుతుంది.", "If we put it under the roof edge, water will fall into it."), ("ఉపాధ్యాయుడు", "ప్రతి గంటకు కొలత రాయండి.", "Write the measurement every hour."), ("విద్యార్థిని", "వాన ఆగిన తర్వాత ఫలితాన్ని పోలుస్తాము.", "After the rain stops, we will compare the result.")],
        ("Write the project steps", [("List the collection step and the measuring step.", ["వాననీటిని సేకరిస్తాము", "కొలత రాస్తాము"], ["we will collect rainwater", "we will write the measurement"]), ("Add the time for comparing results.", ["వాన ఆగిన తర్వాత"], ["after the rain stops"])])
    )),
    _third("A2", 3, _lesson(
        "Accepting a family invitation",
        "Accept an invitation, ask what to bring, and make one polite suggestion about the time.",
        [("ఆహ్వానం", "invitation", "noun"), ("తీసుకురావడం", "to bring", "verb"), ("సౌకర్యం", "convenience", "noun"), ("సాయంత్రం", "evening", "noun"), ("బంధువు", "relative", "noun")],
        ("suggestions with -లామా", "verb stem + -లామా?", "The ending -లామా? asks whether an action would be suitable: కలుద్దామా? (shall we meet?). Combine it with a time or place phrase, and answer with a courteous acceptance or a reason for changing the plan."),
        [("సాయంత్రం ఆరు గంటలకు కలుద్దామా?", "Shall we meet at six in the evening?"), ("మీకు సౌకర్యంగా ఉంటే పండ్లు తీసుకొస్తాను.", "If it is convenient for you, I will bring fruit."), ("ఆహ్వానానికి ధన్యవాదాలు; తప్పకుండా వస్తాను.", "Thank you for the invitation; I will certainly come.")],
        [("కలుద్దాము?", "కలుద్దామా?", "The suggestion question uses the final vowel sign in -లామా?; keep it in the written form." )],
        [("అక్క", "ఆదివారం సాయంత్రం మా ఇంటికి రండి.", "Please come to our home on Sunday evening."), ("చెల్లెలు", "ధన్యవాదాలు. ఏదైనా తీసుకురావాలా?", "Thank you. Should I bring anything?"), ("అక్క", "మీకు సౌకర్యంగా ఉంటే పండ్లు తీసుకురండి.", "If convenient, please bring fruit."), ("చెల్లెలు", "సరే, ఆరు గంటలకు కలుద్దాం.", "All right, let us meet at six." )],
        ("Write a polite reply", [("Accept the invitation and thank the host.", ["ఆహ్వానానికి ధన్యవాదాలు", "వస్తాను"], ["thank you for the invitation", "I will come"]), ("Ask what would be useful to bring.", ["ఏదైనా తీసుకురావాలా?"], ["Should I bring anything?"])])
    )),
]

THIRD["B1"] = [
    _third("B1", 1, _lesson(
        "Discussing a recovery plan",
        "Report a symptom change and agree on a follow-up without presenting a learner dialogue as medical advice.",
        [("కోలుకోవడం", "to recover", "verb"), ("విశ్రాంతి", "rest", "noun"), ("లక్షణం", "symptom", "noun"), ("నియమం", "instruction; rule", "noun"), ("మళ్లీ", "again", "adverb")],
        ("since-clauses and reported instruction", "కాలం నుంచి + మార్పు; X చేయాలని చెప్పారు", "Use నుంచి to mark the point when a change began. A clinician's instruction can be reported with చేయాలని చెప్పారు; keep the reported advice attributed to its speaker."),
        [("రెండు రోజుల నుంచి దగ్గు తగ్గుతోంది.", "The cough has been easing for two days."), ("వైద్యుడు విశ్రాంతి తీసుకోవాలని చెప్పారు.", "The doctor said to rest."), ("లక్షణం మారితే మళ్లీ సంప్రదించండి.", "Contact them again if the symptom changes.")],
        [("వైద్యుడు విశ్రాంతి తీసుకోవాలి చెప్పారు.", "వైద్యుడు విశ్రాంతి తీసుకోవాలని చెప్పారు.", "Reported advice uses the complement -అని/-అని contracted as -ాలని: తీసుకోవాలని చెప్పారు.")],
        [("వైద్యుడు", "రెండు రోజుల నుంచి దగ్గు ఎలా ఉంది?", "How has the cough been for the last two days?"), ("రోగి", "కొంచెం తగ్గుతోంది, కానీ రాత్రి ఇంకా ఇబ్బంది ఉంది.", "It is easing a little, but there is still difficulty at night."), ("వైద్యుడు", "విశ్రాంతి తీసుకోవాలని, నీరు తాగాలని చెప్పాను.", "I said to rest and drink water."), ("రోగి", "లక్షణం మారితే మళ్లీ సంప్రదిస్తాను.", "If the symptom changes, I will contact you again.")],
        ("Summarise the plan", [("Report the symptom change and its time span.", ["రెండు రోజుల నుంచి", "తగ్గుతోంది"], ["for two days", "has been easing"]), ("Attribute the advice to the clinician.", ["వైద్యుడు", "చెప్పారు"], ["doctor", "said"])])
    )),
    _third("B1", 2, _lesson(
        "Explaining a local water change",
        "Describe a change in a local water source, separate an observation from a possible cause, and propose one action.",
        [("నీటి మట్టం", "water level", "noun"), ("బావి", "well", "noun"), ("గమనించడం", "to observe", "verb"), ("కారణం", "cause", "noun"), ("సంరక్షణ", "conservation", "noun")],
        ("cause with కాబట్టి and cautious possibility", "గమనింపు + ఉంది; కారణం + కావచ్చు", "Use కాబట్టి to state a result that follows from a reason. Use కావచ్చు when the cause is a possibility rather than a proved fact; keep the observation and inference distinct."),
        [("ఈ నెల బావిలో నీటి మట్టం తగ్గింది.", "The water level in this well fell this month."), ("వాన తక్కువగా పడింది కాబట్టి నీరు తగ్గి ఉండవచ్చు.", "The water may have fallen because there was little rain."), ("మొదట కొలతలను నమోదు చేద్దాం.", "First, let us record the measurements.")],
        [("వాన తక్కువగా పడింది కాబట్టి నీరు తగ్గుతుంది.", "వాన తక్కువగా పడింది కాబట్టి నీరు తగ్గి ఉండవచ్చు.", "When evidence is incomplete, use the possibility form ఉండవచ్చు rather than stating the result as certain.")],
        [("మీనాక్షి", "ఈ నెల బావిలో నీటి మట్టం తగ్గింది.", "The water level in this well fell this month."), ("రవి", "వాన తక్కువగా పడింది కాబట్టి అదే కారణం కావచ్చు.", "It may be the cause because there was little rain."), ("మీనాక్షి", "ఇంకా కొలతలు చూడకుండా తేల్చలేం.", "We cannot conclude before checking more measurements."), ("రవి", "సరే, ప్రతి వారం నమోదు చేద్దాం.", "All right, let us record it every week.")],
        ("Separate evidence from inference", [("Write the observed change as a fact.", ["నీటి మట్టం తగ్గింది"], ["the water level fell"]), ("Write the possible cause cautiously.", ["కారణం కావచ్చు"], ["may be the cause"])])
    )),
    _third("B1", 3, _lesson(
        "Planning a community exhibition",
        "Coordinate a small cultural exhibition, assign responsibilities, and explain why the display needs a clear caption.",
        [("ప్రదర్శన", "exhibition", "noun"), ("వివరణ", "caption; explanation", "noun"), ("నిర్వాహకుడు", "organiser", "noun"), ("స్వచ్ఛందం", "voluntary", "adjective"), ("ప్రేక్షకుడు", "viewer; audience member", "noun")],
        ("purpose with కోసం and reason with ఎందుకంటే", "కార్యం + కోసం; కారణం + ఎందుకంటే", "Use కోసం to name the purpose of an action. Use ఎందుకంటే to introduce a reason; the explanatory clause follows the point it supports."),
        [("ప్రదర్శన కోసం పూల చిత్రాలు సేకరిస్తున్నాం.", "We are collecting flower pictures for the exhibition."), ("ప్రతి చిత్రానికి చిన్న వివరణ రాస్తాం.", "We will write a short caption for each picture."), ("ప్రేక్షకులు సందర్భం తెలుసుకోవాలి ఎందుకంటే ఇది స్థానిక సంప్రదాయం.", "Viewers should know the context because this is a local tradition.")],
        [("ప్రదర్శన కోసం మేము చిత్రాలు సేకరిస్తున్నారు.", "ప్రదర్శన కోసం మేము చిత్రాలు సేకరిస్తున్నాం.", "The subject మేము requires first-person plural agreement సేకరిస్తున్నాం.")],
        [("నిర్వాహకురాలు", "ప్రతి చిత్రానికి వివరణ ఎవరు రాస్తారు?", "Who will write the caption for each picture?"), ("స్వచ్ఛంద కార్యకర్త", "నేను రాస్తాను; కళాకారుల పేర్లు మీ దగ్గర ఉన్నాయా?", "I will write them; do you have the artists' names?"), ("నిర్వాహకురాలు", "ఉన్నాయి. తేదీని కూడా చేర్చండి.", "Yes. Please include the date too."), ("స్వచ్ఛంద కార్యకర్త", "సరే, ప్రేక్షకులకు సందర్భం స్పష్టంగా ఉంటుంది.", "All right; the context will be clear to the audience.")],
        ("Assign an exhibition task", [("Name the task and who will do it.", ["వివరణ", "నేను రాస్తాను"], ["caption", "I will write it"]), ("Give one reason the audience needs context.", ["సందర్భం", "ఎందుకంటే"], ["context", "because"])])
    )),
]

THIRD["B2"] = [
    _third("B2", 1, _lesson(
        "Explaining a referral and privacy",
        "Explain what a referral note is for and ask that personal details remain private.",
        [("రిఫరల్", "referral", "noun"), ("వైద్య చరిత్ర", "medical history", "noun"), ("గోప్యత", "privacy", "noun"), ("పంపించడం", "to have sent", "verb"), ("అనుమతి", "permission", "noun")],
        ("purpose and condition in a formal request", "X కోసం; Y ఉంటే మాత్రమే + చేయండి", "Use కోసం for the purpose of sharing a document. Add మాత్రమే to limit the action, and use ఉంటే to state the condition; a polite request can end with చేయండి."),
        [("ఈ రిఫరల్ తదుపరి పరీక్ష కోసం.", "This referral is for the next examination."), ("మీ అనుమతి ఉంటే మాత్రమే వివరాలు పంపండి.", "Send the details only if you have permission."), ("వ్యక్తిగత చరిత్ర గోప్యంగా ఉంచాలి.", "Personal history should be kept private.")],
        [("అనుమతి ఉంటే వివరాలు మాత్రమే పంపండి.", "అనుమతి ఉంటే మాత్రమే వివరాలు పంపండి.", "మాత్రమే belongs with the condition here: permission is the limit on sending details.")],
        [("సలహాదారు", "ఈ నోట్‌ను ఎవరికి పంపిస్తారు?", "To whom will you send this note?"), ("వైద్య సహాయకుడు", "తదుపరి పరీక్ష చేసే వైద్యుడికి మాత్రమే.", "Only to the doctor who will do the next examination."), ("సలహాదారు", "రోగి అనుమతి నమోదు చేశారా?", "Have you recorded the patient's permission?"), ("వైద్య సహాయకుడు", "అవును; వ్యక్తిగత వివరాలు గోప్యంగా ఉంటాయి.", "Yes; personal details will remain private.")],
        ("Write a privacy reminder", [("State the purpose of the referral.", ["తదుపరి పరీక్ష కోసం"], ["for the next examination"]), ("State the condition for sharing details.", ["అనుమతి ఉంటే మాత్రమే"], ["only if there is permission"])])
    )),
    _third("B2", 2, _lesson(
        "Reading a report on urban trees",
        "Compare two observations in a short environmental report and qualify a recommendation.",
        [("నీడ", "shade", "noun"), ("ఉష్ణోగ్రత", "temperature", "noun"), ("నమూనా", "sample", "noun"), ("పరిశీలన", "observation", "noun"), ("సిఫార్సు", "recommendation", "noun")],
        ("comparison with కంటే and cautious inference", "A కంటే B ఎక్కువ; అందువల్ల + qualified claim", "Use కంటే to compare two places or measurements. A report can use సూచిస్తుంది or కావచ్చు to distinguish what the data suggests from what it proves."),
        [("చెట్లు ఉన్న వీధి కంటే ఖాళీ వీధి వేడిగా ఉంది.", "The treeless street is hotter than the street with trees."), ("ఈ నమూనా మధ్యాహ్నపు మార్పును సూచిస్తుంది.", "This sample suggests a midday change."), ("మరిన్ని రోజులు కొలిస్తే సిఫార్సు బలపడవచ్చు.", "If we measure for more days, the recommendation may become stronger.")],
        [("చెట్లు ఉన్న వీధి ఖాళీ వీధి కంటే చల్లగా.", "చెట్లు ఉన్న వీధి ఖాళీ వీధి కంటే చల్లగా ఉంది.", "A complete comparison clause needs the finite verb ఉంది.")],
        [("విశ్లేషకుడు", "చెట్లు ఉన్న వీధిలో నీడ ఎక్కువగా ఉంది.", "There is more shade on the street with trees."), ("సంపాదకురాలు", "అయితే ఉష్ణోగ్రతలో తేడాను ఎలా కొలిచారు?", "But how did you measure the temperature difference?"), ("విశ్లేషకుడు", "మూడు మధ్యాహ్నాల నమూనాలను పోల్చాం.", "We compared samples from three afternoons."), ("సంపాదకురాలు", "అప్పుడు సిఫార్సును తాత్కాలికంగా పేర్కొందాం.", "Then let us describe the recommendation as provisional.")],
        ("Draft a qualified recommendation", [("Compare the two streets.", ["కంటే", "ఉష్ణోగ్రత"], ["than", "temperature"]), ("Qualify what the small sample can show.", ["నమూనా", "సూచిస్తుంది"], ["sample", "suggests"])])
    )),
    _third("B2", 3, _lesson(
        "Describing a Kuchipudi rehearsal",
        "Describe how a rehearsal changes a scene and distinguish movement from expressive storytelling.",
        [("సాధన", "rehearsal", "noun"), ("అభినయం", "expressive acting", "noun"), ("దృశ్యం", "scene", "noun"), ("సూచన", "direction", "noun"), ("ప్రవేశం", "entrance", "noun")],
        ("relative participles for a scene description", "verb-stem + -న + noun", "A past relative participle such as చూపించిన modifies the noun that follows: చూపించిన భావం, the feeling that was shown. Keep the modifier close to its noun so the reader can see which scene detail it describes."),
        [("నర్తకి చూపించిన భావం ప్రేక్షకులకు చేరింది.", "The feeling shown by the dancer reached the audience."), ("గురువు మార్చిన క్రమం కథను స్పష్టం చేసింది.", "The order changed by the teacher clarified the story."), ("తాళం తగ్గించినప్పుడు దృశ్యం నెమ్మదించింది.", "When the rhythm was slowed, the scene became slower.")],
        [("గురువు క్రమం మార్చింది కథను స్పష్టం చేసింది.", "గురువు మార్చిన క్రమం కథను స్పష్టం చేసింది.", "Use the relative participle మార్చిన to attach 'changed' to the noun క్రమం.")],
        [("నర్తకి", "ఈ దృశ్యంలో నా ప్రవేశం ఆలస్యంగా ఉండాలా?", "Should my entrance in this scene be delayed?"), ("గురువు", "అవును, ముందున్న మాట ముగిసిన తర్వాత రండి.", "Yes, come after the previous line ends."), ("నర్తకి", "అప్పుడు అభినయం స్పష్టంగా కనిపిస్తుంది.", "Then the expressive acting will be clear."), ("గురువు", "సరే, తాళం తగ్గించినప్పుడు ప్రవేశించండి.", "All right, enter when the rhythm slows.")],
        ("Annotate a rehearsal change", [("Name the change and the scene detail it affects.", ["మార్చిన క్రమం", "దృశ్యం"], ["the changed order", "scene"]), ("Explain when the performer enters.", ["తాళం తగ్గించినప్పుడు"], ["when the rhythm slows"])])
    )),
]

THIRD["C1"] = [
    _third("C1", 1, _lesson(
        "Citing a handloom source",
        "Summarise a public source about Mangalagiri weaving while separating the source's description from your own inference.",
        [("చేనేత", "handloom weaving", "noun"), ("వస్త్రం", "textile", "noun"), ("వివరణ", "description", "noun"), ("ఆధారం", "evidence; source", "noun"), ("వాదన", "argument", "noun")],
        ("source attribution and inference", "X ప్రకారం + reported claim; ఇది + inference కావచ్చు", "Attribute a factual description with ప్రకారం and an explicit source. Mark your own inference separately with కావచ్చు; do not make a source appear to prove more than it actually says."),
        [("ప్రభుత్వ వెబ్‌సైట్ ప్రకారం, మంగళగిరి చేనేతకు ప్రత్యేక గుర్తింపు ఉంది.", "According to the government website, Mangalagiri handloom has a distinct recognition."), ("ఈ వివరణ స్థానిక ఉత్పత్తిపై దృష్టి పెడుతుంది.", "This description focuses on the local product."), ("దీనివల్ల ప్రతి వస్త్రం ఒకే విధంగా తయారవుతుందని తేల్చలేం.", "We cannot conclude from this that every textile is made in the same way.")],
        [("వెబ్‌సైట్ ఈ వస్త్రం ప్రపంచంలోనే ఉత్తమమని నిరూపిస్తుంది.", "వెబ్‌సైట్ ఈ వస్త్రాన్ని స్థానిక ఉత్పత్తిగా వివరిస్తుంది.", "Do not turn a descriptive source into an unsupported superlative; report only what it states.")],
        [("విద్యార్థి", "ఈ పేజీ ఏ విషయాన్ని నిర్ధారిస్తుంది?", "What does this page establish?"), ("మార్గదర్శి", "ఇది మంగళగిరి చేనేత ఉత్పత్తిని వివరిస్తుంది.", "It describes the Mangalagiri handloom product."), ("విద్యార్థి", "అయితే నాణ్యతపై నా వాదనకు మరో ఆధారం కావాలి.", "Then I need another source for my argument about quality."), ("మార్గదర్శి", "అవును, వివరణను వాదనతో కలపకండి.", "Yes; do not confuse a description with an argument.")],
        ("Write a source note", [("Attribute one statement to the named source.", ["ప్రకారం", "చేనేత"], ["according to", "handloom"]), ("Add a limit on what can be inferred.", ["తేల్చలేం"], ["cannot conclude"])])
    )),
    _third("C1", 2, _lesson(
        "Reading an archaeological description",
        "Summarise an archaeological source about Amaravati and distinguish visible remains from a historical interpretation.",
        [("స్తూపం", "stupa", "noun"), ("శిల్పం", "sculpture", "noun"), ("అవశేషం", "remains", "noun"), ("కాలనిర్ణయం", "dating", "noun"), ("వివరణాత్మకం", "descriptive", "adjective")],
        ("evidence with ప్రకారం and contrast with అయితే", "ఆధారం ప్రకారం + claim; అయితే + limit", "Use ప్రకారం to attribute a description to the source and అయితే to introduce a qualification. State what can be seen separately from what scholars infer about date or use."),
        [("అమరావతి అవశేషాల గురించి పురావస్తు శాఖ వివరణ ఇస్తుంది.", "The archaeology department provides a description of the Amaravati remains."), ("చిత్రంలో శిల్ప వివరాలు కనిపిస్తున్నాయి.", "Sculptural details are visible in the image."), ("అయితే, ఒక్క చిత్రంతో కాలాన్ని నిర్ణయించలేం.", "However, one image is not enough to determine the date.")],
        [("ఈ చిత్రం అన్ని వివరాలు నిర్ధారిస్తుంది.", "ఈ చిత్రం కొన్ని శిల్ప వివరాలను చూపిస్తుంది.", "Describe what the image shows; it does not by itself establish every historical claim.")],
        [("సంపాదకుడు", "మూల వివరణలో ఏది స్పష్టంగా ఉంది?", "What is explicit in the source description?"), ("చరిత్రకారిణి", "శిల్పాల స్థానం, కొన్ని రూపాలు వివరించబడ్డాయి.", "The placement of sculptures and some forms are described."), ("సంపాదకుడు", "వాటి తేదీ గురించి ఏమి చెప్పవచ్చు?", "What can we say about their date?"), ("చరిత్రకారిణి", "మరిన్ని ఆధారాలు కావాలి; చిత్రమే సరిపోదు.", "We need more evidence; the image alone is not enough.")],
        ("Separate observation from interpretation", [("Write one visible detail.", ["చిత్రంలో", "కనిపిస్తున్నాయి"], ["in the image", "are visible"]), ("State one limit on dating from a single image.", ["ఒక్క చిత్రంతో", "నిర్ణయించలేం"], ["with one image", "cannot determine"])])
    )),
    _third("C1", 3, _lesson(
        "Editing a public-language notice",
        "Revise an event notice for clarity while preserving the organiser's intended information and a respectful public tone.",
        [("ప్రకటన", "notice", "noun"), ("లక్ష్య పాఠకుడు", "intended reader", "noun"), ("సంక్షిప్తం", "concise", "adjective"), ("స్పష్టత", "clarity", "noun"), ("సవరణ", "revision", "noun")],
        ("nominalised purpose and balanced contrast", "X కోసం; Y అయినప్పటికీ + main clause", "Use కోసం to state the purpose of an edit. Use అయినప్పటికీ for a concession, then keep the main clause explicit so that concision does not erase essential information."),
        [("ప్రకటనను కొత్త పాఠకుల కోసం సవరించాం.", "We revised the notice for new readers."), ("వాక్యం సంక్షిప్తమైనప్పటికీ సమయం స్పష్టంగా ఉంది.", "Although the sentence is concise, the time is clear."), ("ప్రవేశ నియమాన్ని తొలగించకుండా పదాలను సరళం చేయాలి.", "We should simplify the wording without removing the entry rule.")],
        [("వాక్యం సంక్షిప్తమైనప్పటికీ సమయం స్పష్టంగా లేవు.", "వాక్యం సంక్షిప్తమైనప్పటికీ సమయం స్పష్టంగా ఉంది.", "The singular subject సమయం requires singular agreement ఉంది.")],
        [("సంపాదకురాలు", "ఈ వాక్యం చిన్నదే, కానీ ప్రవేశ సమయం కనిపించడం లేదు.", "This sentence is short, but the entry time is missing."), ("నిర్వాహకుడు", "సమయం చేరిస్తే ప్రకటన పొడవవుతుంది.", "If we add the time, the notice will become longer."), ("సంపాదకురాలు", "అయినా పాఠకుడికి అవసరమైన వివరాన్ని ఉంచాలి.", "Even so, we should keep the detail the reader needs."), ("నిర్వాహకుడు", "సరే, పునరుక్తిని మాత్రమే తొలగిద్దాం.", "All right; let us remove only the repetition.")],
        ("Make a careful revision", [("Name the audience and purpose of the revision.", ["పాఠకుల కోసం", "సవరించాం"], ["for readers", "revised"]), ("Preserve one essential detail while shortening the sentence.", ["సమయం", "ఉంచాలి"], ["time", "should keep"])])
    )),
]

THIRD["C2"] = [
    _third("C2", 1, _lesson(
        "Explaining Telugu text encoding",
        "Explain why a Telugu character sequence may need normalization before search or comparison, without equating encoded data with pronunciation.",
        [("ఎన్‌కోడింగ్", "encoding", "noun"), ("సంకేత బిందువు", "code point", "noun"), ("సాధారణీకరణ", "normalization", "noun"), ("వ్యంజన సమూహం", "consonant cluster", "noun"), ("శోధన", "search", "noun")],
        ("technical condition and consequence", "ఒకవేళ + condition, అయితే + consequence", "Use ఒకవేళ ... అయితే to state a condition and its consequence. Keep the distinction between a Unicode sequence, a displayed glyph and a spoken form explicit; encoding alone does not decide how a word is pronounced."),
        [("ఒకవేళ రెండు పాఠ్యాలు వేర్వేరు క్రమాల్లో నిల్వైతే, శోధన విఫలమవచ్చు.", "If two texts are stored in different sequences, search may fail."), ("సాధారణీకరణ చేసిన తర్వాత అక్షర క్రమాన్ని పోల్చవచ్చు.", "After normalization, the character sequence can be compared."), ("సంకేత బిందువు ఉచ్చారణకు సమానం కాదు.", "A code point is not the same thing as pronunciation.")],
        [("సంకేత బిందువు మాటను పలుకుతుంది.", "సంకేత బిందువు అక్షరాన్ని సూచిస్తుంది.", "A code point represents a character value; it does not itself speak a word." )],
        [("ఇంజినీర్", "శోధనలో ఒకే పదం ఎందుకు కనిపించదు?", "Why does the same word not appear in search?"), ("భాషావేత్త", "రెండు అక్షర క్రమాలు వేర్వేరుగా నిల్వై ఉండవచ్చు.", "Two character sequences may have been stored differently."), ("ఇంజినీర్", "సాధారణీకరణ చేస్తే సమస్య పూర్తిగా పోతుందా?", "Will normalization remove the problem completely?"), ("భాషావేత్త", "అన్ని సమస్యలు కాదు; పరీక్షించి పరిమితిని చెప్పాలి.", "Not every problem; we should test and state the limitation." )],
        ("Write a technical explanation", [("State the condition that can affect search.", ["వేర్వేరు క్రమాల్లో", "శోధన"], ["in different sequences", "search"]), ("State one limit of normalization.", ["అన్ని సమస్యలు కాదు", "పరిమితి"], ["not every problem", "limitation"])])
    )),
    _third("C2", 2, _lesson(
        "Comparing a transcript with a recording",
        "Edit a Telugu transcript against an audio recording while recording uncertainty instead of silently replacing a regional form.",
        [("లిప్యంతరీకరణ", "transcription", "noun"), ("ధ్వనిముద్రణ", "audio recording", "noun"), ("ప్రాంతీయ రూపం", "regional form", "noun"), ("సందిగ్ధం", "ambiguous", "adjective"), ("సంపాదకీయ", "editorial", "adjective")],
        ("reported speech and editorial uncertainty", "X అన్నట్లు వినిపించింది; Y అని నిర్ధారించలేం", "Use అన్నట్లు వినిపించింది to report what seems audible, and explicitly mark what cannot be confirmed. Preserve a regional form when the evidence supports it; use an editorial note for an unresolved reading."),
        [("రికార్డింగ్‌లో చివరి పదం స్పష్టంగా వినిపించలేదు.", "The final word was not clearly audible in the recording."), ("వక్త ప్రాంతీయ రూపం ఉపయోగించినట్లు వినిపించింది.", "It sounded as though the speaker used a regional form."), ("మరొకసారి విన్నా దాన్ని నిర్ధారించలేం.", "Even after listening again, we cannot confirm it.")],
        [("వక్త తప్పు పదం ఉపయోగించాడని తేల్చాలి.", "వక్త ఏ రూపం ఉపయోగించారో రికార్డింగ్ ఆధారంగా మాత్రమే చెప్పాలి.", "A transcript should not label an unfamiliar regional form an error without evidence; attribute only what the recording supports.")],
        [("సంపాదకుడు", "ఈ పదాన్ని ప్రామాణిక రూపంతో మార్చనా?", "Should I replace this word with the standard form?"), ("లిప్యంతరీకర్త", "ముందు రికార్డింగ్‌లోని ధ్వనిని నిర్ధారిద్దాం.", "First let us confirm the sound in the recording."), ("సంపాదకుడు", "ఇంకా సందిగ్ధంగా ఉంటే?", "What if it remains ambiguous?"), ("లిప్యంతరీకర్త", "మార్చకుండా గమనికలో అనిశ్చితిని నమోదు చేద్దాం.", "Let us record the uncertainty in a note without changing it.")],
        ("Prepare an editorial note", [("State what is audible and what remains uncertain.", ["స్పష్టంగా వినిపించలేదు", "నిర్ధారించలేం"], ["was not clearly audible", "cannot confirm"]), ("Describe your conservative editing choice.", ["మార్చకుండా", "గమనికలో"], ["without changing", "in a note"])])
    )),
    _third("C2", 3, _lesson(
        "Presenting a language-policy proposal",
        "Present a balanced proposal for public Telugu text that accounts for accessibility, regional representation and technical searchability.",
        [("భాషా విధానం", "language policy", "noun"), ("ప్రాతినిధ్యం", "representation", "noun"), ("అందుబాటు", "accessibility", "noun"), ("సాంకేతికత", "technology", "noun"), ("పరిమితి", "limitation", "noun")],
        ("concession and qualified recommendation", "X ఉన్నప్పటికీ, Y కోసం + recommendation", "Use ఉన్నప్పటికీ to acknowledge a real constraint before the recommendation. Name the audience and the trade-off; do not present a technical convenience as proof that a regional form lacks value."),
        [("శోధన సౌలభ్యం ముఖ్యం అయినప్పటికీ, ప్రాంతీయ రూపాలకు ఉదాహరణల్లో చోటు ఇవ్వాలి.", "Although search convenience matters, regional forms should have a place in examples."), ("ప్రజా పాఠ్యం అందరికీ అందుబాటులో ఉండేలా చూడాలి.", "Public text should be made accessible to everyone."), ("ఈ విధానం పాఠకుల అభిప్రాయంతో సవరించవచ్చు.", "This policy can be revised with readers' feedback.")],
        [("సాంకేతికత సులభం కాబట్టి ప్రాంతీయ రూపాలు అవసరం లేదు.", "శోధన సులభం కావాలి; అయినప్పటికీ ప్రాంతీయ రూపాలను సందర్భంతో నమోదు చేయాలి.", "A search constraint does not establish that regional forms are unnecessary; state both the technical need and the representation choice.")],
        [("సభ్యురాలు", "మనం ఒకే ప్రామాణిక రూపం పెట్టాలా?", "Should we set just one standard form?"), ("సంపాదకుడు", "ప్రజా సూచనల్లో అది స్పష్టతకు తోడ్పడవచ్చు.", "That may support clarity in public notices."), ("సభ్యురాలు", "అయితే ప్రాంతీయ పలుకుబడి ఎక్కడ కనిపిస్తుంది?", "But where will regional usage appear?"), ("సంపాదకుడు", "ఉదాహరణల్లో నమోదు చేసి, పాఠకులతో విధానాన్ని సమీక్షిద్దాం.", "Let us document it in examples and review the policy with readers.")],
        ("Draft a balanced recommendation", [("Acknowledge one technical or public-text constraint.", ["శోధన సౌలభ్యం", "స్పష్టత"], ["search convenience", "clarity"]), ("Add a measure that preserves regional representation.", ["ప్రాంతీయ రూపాలు", "ఉదాహరణల్లో"], ["regional forms", "in examples"])])
    )),
]

# ── five playable plus-rungs: bridge routines, not placeholder ranks ──

HALF_EXTRAS = {}

HALF_EXTRAS["A1+"] = _extra(
    culture=("Kondapalli Toys are a wooden craft associated with Kondapalli in Andhra Pradesh's "
             "NTR district. The district administration describes a process in which artisans "
             "carve softwood, smooth the figure with a sawdust-and-tamarind-seed-paste coating, "
             "then paint it. The subjects include village scenes and animals. Naming the stages "
             "of a craft is useful beginner language: మొదట (first), తరువాత (then), చివరికి "
             "(finally). The description belongs to this craft tradition, not to every wooden toy."),
    source="https://ntr.ap.gov.in/one-district-one-product/",
    reading=("కొండపల్లి బొమ్మల పనిని చూడటానికి నిఖిల్ తన స్నేహితురాలితో వెళ్లాడు. "
             "కార్మికుడు ఒక చెక్క ముక్కను తీసుకొని, చిన్న పక్షి ఆకారంలో చెక్కాడు. తరువాత "
             "ఉపరితలాన్ని మృదువుగా చేసి రంగు వేశాడు. నిఖిల్ ఒక చిన్న బొమ్మను చూపించి, "
             "దాని ధర అడిగాడు. అతని స్నేహితురాలు బొమ్మను జాగ్రత్తగా కాగితంలో చుట్టింది."),
    gloss=("Nikhil went with his friend to see Kondapalli toy-making. The craftsperson took a "
           "piece of wood and carved it into the shape of a small bird. Then the surface was "
           "smoothed and painted. Nikhil pointed to a small toy and asked its price. His friend "
           "carefully wrapped the toy in paper."),
    listening=("నిఖిల్: ఈ పక్షి బొమ్మ చెక్కతో చేశారా?<br>"
               "కార్మికుడు: అవును, ముందు ఆకారం చెక్కుతాం.<br>"
               "నిఖిల్: తరువాత రంగు వేస్తారా?<br>"
               "కార్మికుడు: అవును, ఆరిన తర్వాత రంగు వేస్తాం."),
    listening_gloss=("Nikhil: Is this bird toy made of wood? Craftsperson: Yes, first we carve "
                     "the shape. Nikhil: Do you paint it next? Craftsperson: Yes, after it dries, "
                     "we paint it."),
    idioms=[
        ("రూపం దాల్చడం", "to take on a shape", "to begin to take form"),
        ("చేతి పని", "work of the hand", "handcraft or handiwork"),
        ("రంగులు అద్దడం", "to apply colours", "to add colour or character"),
        ("కథకు రూపం ఇవ్వడం", "to give a story a form", "to shape an idea into a story"),
        ("ఒక చూపు చూడడం", "to have one look", "to glance at something"),
        ("జాగ్రత్తగా చూడడం", "to look carefully", "to take care with something"),
        ("చేతిలో పెట్టడం", "to place in the hand", "to hand something over"),
        ("చిన్నచూపు చూడడం", "to look with a small gaze", "to look down on someone"),
        ("మొదటి అడుగు వేయడం", "to take the first step", "to begin a task"),
        ("ఒక్కొక్కటిగా", "one by one", "in sequence, one at a time"),
    ],
    mistakes=[
        ("కార్మికుడు చెక్క బొమ్మ చెక్కుతారు.", "కార్మికుడు చెక్క బొమ్మను చెక్కుతారు.", "Mark this definite object with -ను: బొమ్మను."),
        ("మొదట రంగు వేసి, తరువాత ఆకారం చెక్కుతారు.", "మొదట ఆకారం చెక్కి, తరువాత రంగు వేస్తారు.", "Put the making stages in their intended order; the converb చెక్కి links the first action to the next."),
        ("ఈ బొమ్మ ఎంత ధర ఉంది?", "ఈ బొమ్మ ధర ఎంత?", "Ask the price with the natural frame ధర ఎంత? rather than combining ఎంత with an extra ఉంది."),
    ],
    task_title="బొమ్మల దుకాణంలో చిన్న సంభాషణ",
    task_instructions=("Write a six-turn shop conversation: greet the craftsperson, name one toy, ask "
                       "what it is made from, ask its price, accept or decline politely, and thank "
                       "the craftsperson. Use మొదట, తరువాత and ఒక బొమ్మను at least once."),
)

HALF_EXTRAS["A2+"] = _extra(
    culture=("The Telangana State Portal names Oggu Kathalu and Golla Suddulu among local "
             "storytelling traditions that developed alongside everyday community life. A "
             "learner can practise retelling a story by separating the event from a speaker's "
             "comment on it: ఎవరు? (who?), ఏమి జరిగింది? (what happened?), and కథకుడు ఏమి "
             "చెప్పాడు? (what did the storyteller say?). This exercise does not claim that all "
             "performances follow one fixed script."),
    source="https://www.telangana.gov.in/about/language-culture/",
    reading=("సాంస్కృతిక కేంద్రంలో కథా కార్యక్రమం మొదలైంది. కథకుడు ముందుగా ఒక గ్రామం "
             "గురించి పరిచయం ఇచ్చాడు; తరువాత ప్రధాన పాత్రకు ఎదురైన సమస్యను వివరించాడు. "
             "ప్రేక్షకులు ఒక ప్రశ్న అడిగినప్పుడు, కథకుడు కథను ఆపి దానికి సమాధానం చెప్పాడు. "
             "తర్వాత కథ మళ్లీ కొనసాగింది. కార్యక్రమం ముగిసినప్పుడు నిర్వాహకురాలు కథలోని "
             "సందేశం గురించి అందరినీ మాట్లాడమని ఆహ్వానించింది."),
    gloss=("A storytelling programme began at the cultural centre. The storyteller first "
           "introduced a village; then he described the problem faced by the main character. "
           "When an audience member asked a question, the storyteller paused the story and "
           "answered it. Then the story continued. At the end of the programme, the organiser "
           "invited everyone to talk about the message in the story."),
    listening=("నిర్వాహకురాలు: కథ ఎక్కడ మొదలైంది?<br>"
               "కథకుడు: నది పక్కన ఉన్న గ్రామంలో మొదలైంది.<br>"
               "నిర్వాహకురాలు: పాత్రకు సమస్య ఎప్పుడు వచ్చింది?<br>"
               "కథకుడు: ప్రయాణం మొదలైన తర్వాత వచ్చింది."),
    listening_gloss=("Organiser: Where did the story begin? Storyteller: It began in a village "
                     "beside a river. Organiser: When did the character face the problem? "
                     "Storyteller: It came after the journey began."),
    idioms=[
        ("కథలో మునిగిపోవడం", "to sink into a story", "to become absorbed in a story"),
        ("మాటలో మాట", "a word within a word", "one topic leading into another"),
        ("కథను మలుపు తిప్పడం", "to turn the story at a bend", "to change the direction of a story"),
        ("విషయానికి రావడం", "to come to the subject", "to get to the point"),
        ("విన్నది వినిపించడం", "to make heard what one heard", "to repeat or report what was heard"),
        ("ఒక్కసారి వెనక్కి చూడడం", "to look back once", "to review what happened"),
        ("దృష్టి ఆకర్షించడం", "to attract attention", "to draw someone's attention"),
        ("మనసులో నిలవడం", "to remain in the mind", "to be memorable"),
        ("సమయం గడవడం", "for time to pass", "for time to go by"),
        ("ప్రశ్నకు సమాధానం ఇవ్వడం", "to give an answer to a question", "to respond directly"),
    ],
    mistakes=[
        ("కథకుడు కథను చెప్పినప్పుడు ప్రేక్షకులు ప్రశ్న అడిగారు.", "కథకుడు కథ చెబుతున్నప్పుడు ప్రేక్షకులు ప్రశ్న అడిగారు.", "Use the progressive participle చెబుతున్నప్పుడు for an action that was in progress when the question came."),
        ("కథలో ప్రధాన పాత్రకు సమస్య ఎదురైంది, అందుకే కథను ఆపాడు.", "ప్రేక్షకులు ప్రశ్న అడిగినప్పుడు కథకుడు కథను ఆపాడు.", "Make the subject of the action explicit: the storyteller, not the character, paused the telling."),
        ("నిర్వాహకురాలు అందరిని మాట్లాడమని ఆహ్వానించారు.", "నిర్వాహకురాలు అందరినీ మాట్లాడమని ఆహ్వానించారు.", "Use the object form అందరినీ with the postposition-like request construction."),
    ],
    task_title="విన్న కథను తిరిగి చెప్పడం",
    task_instructions=("Retell a short story in three parts: where it began, what problem arose, and "
                       "how it ended. Add one interruption or question from an audience member. "
                       "Use మొదట, ఒకప్పుడు, ఆ తరువాత and చివరికి to signal sequence, and attribute "
                       "one statement to the storyteller with అని."),
)

HALF_EXTRAS["B1+"] = _extra(
    culture=("Cheriyal scroll painting is a Telangana narrative-art tradition. The Telangana "
             "State Handicrafts Development Corporation describes scrolls that unfold like a "
             "film roll, carrying stories from epic, Puranic and local traditions; it also "
             "notes a canvas made from khadi cotton, starch, white mud and tamarind-seed paste. "
             "A scroll can be read as a sequence of pictured episodes. The source describes a "
             "specific craft and its history, not every painted narrative in the region."),
    source="https://tsht.telangana.gov.in/GolkoCrafts/07-10-2021.html",
    reading=("చెరియాల్ చిత్రకారిణి కొత్త కథా చుట్టను తయారు చేసింది. ముందుగా వస్త్రంపై "
             "పొర వేసి ఆరనిచ్చింది. తరువాత ప్రధాన పాత్రల రూపురేఖలు గీసి, ఒక్కో దృశ్యానికి "
             "వేర్వేరు రంగులు నింపింది. సహాయకుడు చిత్రాల క్రమాన్ని చూసి చిన్న శీర్షికలు "
             "రాశాడు. సందర్శకులు చుట్టను ఎడమ నుంచి కుడికి తెరిచి, కథలో మార్పు ఎక్కడ "
             "వచ్చిందో గమనించారు."),
    gloss=("A Cheriyal artist made a new story scroll. First she coated the cloth and let it "
           "dry. Then she drew the outlines of the main characters and filled each scene with "
           "different colours. An assistant checked the order of the pictures and wrote short "
           "captions. Visitors opened the scroll from left to right and noticed where the story "
           "changed."),
    listening=("సహాయకుడు: ఈ దృశ్యానికి ఏ శీర్షిక రాయాలి?<br>"
               "చిత్రకారిణి: పాత్ర ప్రయాణం మొదలుపెట్టే ఘట్టం అని రాయండి.<br>"
               "సహాయకుడు: తదుపరి చిత్రంలో అతను తిరిగి వస్తాడా?<br>"
               "చిత్రకారిణి: అవును, కానీ మధ్యలోని సంఘటనను కూడా చూపాలి."),
    listening_gloss=("Assistant: What caption should I write for this scene? Artist: Write 'the "
                     "episode in which the character begins the journey.' Assistant: Does he "
                     "return in the next picture? Artist: Yes, but we should also show the event "
                     "in between."),
    idioms=[
        ("చిత్రం కళ్లకు కట్టినట్టు ఉండడం", "for a picture to be tied before the eyes", "for a scene to be vivid"),
        ("ఘట్టం మారడం", "for an episode to change", "for the story to move to a new scene"),
        ("రేఖలు గీయడం", "to draw lines", "to outline a plan or picture"),
        ("రంగు నింపడం", "to fill with colour", "to add detail or life"),
        ("కథను విప్పడం", "to unfold the story", "to reveal a story gradually"),
        ("క్రమం తప్పడం", "for the order to slip", "to lose the sequence"),
        ("ఒక చూపులో", "in one glance", "at first sight"),
        ("బొమ్మ మాటాడినట్టు", "as if the picture spoke", "as if an image conveyed a story by itself"),
        ("సందర్భం కుదరడం", "for the context to fit", "for details to make sense together"),
        ("చివరి మలుపు", "the final turn", "the last unexpected development"),
    ],
    mistakes=[
        ("చిత్రకారిణి దృశ్యాలను క్రమంగా గీసింది.", "చిత్రకారిణి దృశ్యాలను క్రమంలో గీసింది.", "Use క్రమంలో for 'in sequence'; క్రమంగా more often means gradually."),
        ("అతను తిరిగి వస్తాడా తరువాత చిత్రంలో?", "తదుపరి చిత్రంలో అతను తిరిగి వస్తాడా?", "Place the time phrase before the clause in this neutral written question."),
        ("శీర్షికలు కథను చూపించింది.", "శీర్షికలు కథను చూపించాయి.", "Plural subject శీర్షికలు takes plural agreement చూపించాయి."),
    ],
    task_title="చిత్రకథకు శీర్షికలు",
    task_instructions=("Choose four linked episodes for a short scroll story. Write one clear caption "
                       "per panel, keep the character names consistent, and explain where the "
                       "turning point occurs. Use ముందుగా, ఆ తరువాత, మధ్యలో and చివరికి; do not "
                       "claim that the imagined story is a traditional Cheriyal subject."),
)

HALF_EXTRAS["B2+"] = _extra(
    culture=("The Andhra Pradesh Department of Handlooms and Textiles describes Mangalagiri "
             "as a weaving centre and notes pit-loom production, cotton yarn and Nizam-border "
             "designs among features of its sarees. A product description should identify "
             "which details come from a particular source and avoid turning them into a claim "
             "about every textile or every weaver. This unit uses that distinction to practise "
             "asking for a sample, checking dimensions and writing a precise order."),
    source="https://handlooms.ap.gov.in/odopdistrict.html",
    reading=("మంగళగిరి చేనేత వస్త్రానికి ఆర్డర్ ఇవ్వడానికి కొనుగోలుదారు ముందుగా నమూనా "
             "చూశాడు. అంచు వెడల్పు, రంగుల కలయిక, నూలు వివరాలు పత్రంలో నమోదు చేశాడు. "
             "నేతకారుడు తయారీకి కావలసిన సమయం చెప్పి, రంగు నమూనా ఆమోదించిన తర్వాతే "
             "పని మొదలుపెడతానన్నాడు. కొనుగోలుదారు ధరతో పాటు సంరక్షణ సూచనలను కూడా "
             "లిఖితపూర్వకంగా పంపమని కోరాడు."),
    gloss=("The buyer first looked at a sample before ordering a Mangalagiri handloom textile. "
           "He recorded the border width, colour combination and yarn details in a document. "
           "The weaver stated the time needed and said that work would begin only after the "
           "colour sample was approved. The buyer also asked for the price and care instructions "
           "in writing."),
    listening=("కొనుగోలుదారు: నమూనాలోని అంచు వెడల్పే తయారీలో ఉంటుందా?<br>"
               "నేతకారుడు: మీరు ఆమోదించిన కొలతనే ఉపయోగిస్తాను.<br>"
               "కొనుగోలుదారు: రంగు మారితే ముందుగా తెలియజేయండి.<br>"
               "నేతకారుడు: మార్పు ఉంటే పని మొదలుపెట్టే ముందు మీ అనుమతి తీసుకుంటాను."),
    listening_gloss=("Buyer: Will the finished border have the same width as the sample? Weaver: "
                     "I will use the measurement you approve. Buyer: If the colour changes, tell "
                     "me first. Weaver: If there is a change, I will get your approval before I "
                     "begin work."),
    idioms=[
        ("కొలతకు తగ్గట్టు", "according to the measurement", "to match a stated requirement"),
        ("మాట మీద ఉండడం", "to remain on one's word", "to keep an agreement"),
        ("అంచనా వేయడం", "to make an estimate", "to assess before deciding"),
        ("నూలుపోగు విడవకుండా", "without letting a thread slip", "with close attention to detail"),
        ("విషయాన్ని లిఖితంలో పెట్టడం", "to put a matter in writing", "to document an agreement"),
        ("ధర పలకడం", "to state a price", "to quote a price"),
        ("పని మొదలుపెట్టడం", "to begin the work", "to start a project"),
        ("తేడా గుర్తించడం", "to notice a difference", "to identify a variation"),
        ("సరిహద్దు దాటకపోవడం", "not to cross the boundary", "to stay within the agreed scope"),
        ("రెండు కొలతలు కలపడం", "to combine two measures", "to compare two specifications"),
    ],
    mistakes=[
        ("నమూనా చూసిన పని మొదలుపెడతాను.", "నమూనా చూసిన తర్వాత పని మొదలుపెడతాను.", "Use చూసిన తర్వాత as a complete time phrase before the next action."),
        ("కొలతలు పత్రంలో నమోదు చేశాడు తర్వాత రంగు ఆమోదించాడు.", "కొలతలు పత్రంలో నమోదు చేసి, తర్వాత రంగును ఆమోదించాడు.", "Use the converb నమోదు చేసి to link the first action to the next, and mark రంగు as the object."),
        ("మీరు ఆమోదించిన కొలతలు ఉపయోగిస్తాను.", "మీరు ఆమోదించిన కొలతనే ఉపయోగిస్తాను.", "When referring to the single approved measurement, keep the singular focus marker కొలతనే."),
    ],
    task_title="నేతకారునికి స్పష్టమైన ఆర్డర్",
    task_instructions=("Write an order note with five checkable details: textile, dimensions, border, "
                       "colour and delivery date. Add a condition for approval before production, "
                       "then request the care instructions in writing. Mark source-reported facts "
                       "separately from the specifications you are inventing for your order."),
)

HALF_EXTRAS["C1+"] = _extra(
    culture=("The Archaeological Survey of India describes the Amaravati Mahachaitya as a "
             "Buddhist stupa whose sculptured slabs included scenes from the Buddha's life, "
             "Jataka stories and other motifs. Its page also records that archaeological "
             "research and conservation are part of ASI's work. A careful heritage report "
             "separates a visible feature, an interpretation of its significance and a claim "
             "that still needs evidence. The passage here uses the official description as a "
             "source to practise that distinction."),
    source="https://asi.nic.in/ruined-buddhist-stupa-remains-amaravati/",
    reading=("అమరావతి మహాస్తూపం గురించి నివేదిక సిద్ధం చేస్తూ పరిశోధకురాలు మూడు స్థాయిలను "
             "వేరు చేసింది. మొదట, స్థలంలో కనిపించే నిర్మాణ అవశేషాలను నమోదు చేసింది. "
             "తరువాత, పురావస్తు శాఖ వివరణలో శిల్ప పలకలపై బౌద్ధ కథలు, జాతక దృశ్యాలు "
             "ఉన్నాయని గుర్తించింది. చివరగా, వాటి కాలం లేదా ఉద్దేశం గురించి చేసే ప్రతి "
             "వ్యాఖ్యకు ఏ ఆధారం ఉందో సూచించింది. ఆధారం లేని వివరాన్ని ఖచ్చితమైన "
             "చరిత్రగా రాయకూడదని ఆమె సంపాదకుడికి తెలిపింది."),
    gloss=("While preparing a report on the Amaravati Mahastupa, the researcher separated "
           "three levels. First, she recorded the structural remains visible at the site. Then "
           "she noted that the Archaeological Survey description mentions Buddhist stories and "
           "Jataka scenes on sculptured slabs. Finally, she indicated what evidence supported "
           "each statement about their date or purpose. She told the editor that a detail "
           "without evidence should not be written as certain history."),
    listening=("సంపాదకుడు: ఈ శిల్పం ఏ కాలానికి చెందిందని రాయవచ్చు?<br>"
               "పరిశోధకురాలు: మూల వివరణలో ఉన్న తేదీని ఆపాదించి చెప్పవచ్చు.<br>"
               "సంపాదకుడు: దాని ఉద్దేశం కూడా నిర్ధారితమేనా?<br>"
               "పరిశోధకురాలు: ఆ అంశానికి వేరే ఆధారం లేకపోతే, దాన్ని అనుమానంగా మాత్రమే పేర్కొందాం."),
    listening_gloss=("Editor: What date can we assign to this sculpture? Researcher: We can "
                     "attribute the date stated in the source description. Editor: Is its purpose "
                     "also established? Researcher: If we have no separate evidence for that, "
                     "let us state it only as a possibility."),
    idioms=[
        ("కాలానికి సాక్ష్యంగా నిలవడం", "to stand as a witness to time", "to survive as evidence of a period"),
        ("చరిత్ర పుటల్లో నిలవడం", "to remain on the pages of history", "to become part of recorded history"),
        ("ఆధారం చూపించడం", "to show the evidence", "to substantiate a claim"),
        ("ఒక కోణంలో చూడడం", "to look from one angle", "to consider one perspective"),
        ("వివరాన్ని విడదీయడం", "to separate a detail", "to analyse a claim into parts"),
        ("అనుమానానికి తావివ్వడం", "to leave room for doubt", "to acknowledge uncertainty"),
        ("పరిశీలనకు పెట్టడం", "to put up for examination", "to make a claim open to review"),
        ("సందర్భం కోల్పోవడం", "to lose the context", "to remove a detail from its setting"),
        ("పరిమితిని గుర్తించడం", "to recognise a limit", "to acknowledge what the evidence cannot show"),
        ("తీర్మానానికి రావడం", "to arrive at a conclusion", "to reach a reasoned finding"),
    ],
    mistakes=[
        ("మూలం ఈ నిర్మాణం తప్పకుండా ఈ తేదీన నిర్మించిందని చెబుతుంది.", "మూలం ఈ నిర్మాణానికి ఒక అంచనా కాలాన్ని సూచిస్తుంది.", "Do not strengthen an approximate or attributed date into certainty; report the source's actual level of confidence."),
        ("ఈ శిల్పం కథను చూపించడం అని నిరూపిస్తుంది.", "ఈ శిల్పం కథా దృశ్యాన్ని చూపుతుందని మూల వివరణ పేర్కొంటుంది.", "Attribute the interpretation to the source; an image alone does not prove every narrative detail."),
        ("ఆధారం లేకపోయినా ఖచ్చితంగా రాయాలి.", "ఆధారం లేకపోతే అనిశ్చితిని స్పష్టంగా పేర్కొనాలి.", "A report should mark an unresolved claim as uncertain rather than state it as fact."),
    ],
    task_title="పురావస్తు నివేదికలో ఆధారాల శ్రేణి",
    task_instructions=("Draft a concise report paragraph with three labelled moves: direct observation, "
                       "source-attributed interpretation, and a remaining question. Use ప్రకారం, "
                       "అయితే and ఇంకా నిర్ధారించాలి. Avoid giving a precise date or motive unless "
                       "your stated source supports it."),
)

# A separate Unicode chapter is the single source for the orthographic bridge.

HALFSTEPS["A1+"] = {
    "title": "Telugu A1+ — Toys, materials and a visit",
    "native": NATIVE,
    "goals": [
        "Name an object, its material and its shape",
        "Describe a simple making process in order",
        "Ask a craftsperson a clear, respectful question",
    ],
    "units": [
        {"id": "A1+-U1", "title": "కొండపల్లి బొమ్మలు", "lessons": [
            _lesson(
                "A toy made of wood",
                "Identify a toy, say what it is made from, and ask who made it.",
                [("చెక్క", "wood", "noun"), ("బొమ్మ", "toy; figure", "noun"), ("పక్షి", "bird", "noun"), ("కార్మికుడు", "craftsperson", "noun"), ("చెక్కడం", "to carve", "verb")],
                ("material with -తో", "వస్తువు + material-తో + చేసిన", "Attach -తో to a material to say what something is made with. Place చేసిన before the noun it describes, and ask who made a particular object with ఎవరు?"),
                [("ఇది చెక్కతో చేసిన బొమ్మ.", "This is a toy made of wood."), ("కార్మికుడు పక్షి ఆకారాన్ని చెక్కాడు.", "The craftsperson carved the shape of a bird."), ("ఈ బొమ్మను ఎవరు చేశారు?", "Who made this toy?")],
                [("ఇది చెక్క చేసిన బొమ్మ.", "ఇది చెక్కతో చేసిన బొమ్మ.", "Mark the material with -తో: చెక్కతో." )],
                [("సందర్శకుడు", "ఈ పక్షి బొమ్మను ఎవరు చేశారు?", "Who made this bird toy?"), ("కార్మికుడు", "మా పనివాళ్లు చెక్కతో తయారు చేశారు.", "Our artisans made it from wood."), ("సందర్శకుడు", "ఈ ఆకారం మీరే చెక్కారా?", "Did you carve this shape yourself?"), ("కార్మికుడు", "అవును, ముందుగా రూపురేఖలు గీసాను.", "Yes, I first drew the outline." )],
                ("Ask about a craft object", [("Name the material and object.", ["చెక్కతో", "బొమ్మ"], ["made of wood", "toy"]), ("Ask who made it.", ["ఈ బొమ్మను ఎవరు చేశారు?"], ["Who made this toy?"])])
            ),
            _lesson(
                "From carving to colour",
                "Retell three simple stages of making a toy using a clear sequence.",
                [("మొదట", "first", "adverb"), ("ఉపరితలం", "surface", "noun"), ("మృదువుగా", "smoothly", "adverb"), ("ఆరడం", "to dry", "verb"), ("రంగు వేయడం", "to paint; apply colour", "verb")],
                ("converbs for linked actions", "verb stem + -ి, then the next verb", "When the same person performs a sequence of actions, Telugu can link the earlier action with a converb such as చెక్కి or చేసి. Put మొదట and తరువాత near the step they organise."),
                [("మొదట ఆకారాన్ని చెక్కి, తరువాత ఉపరితలాన్ని మృదువుగా చేస్తారు.", "First they carve the shape, then smooth the surface."), ("పూత ఆరిన తర్వాత రంగు వేస్తారు.", "They paint it after the coating dries."), ("చివరికి బొమ్మను పరిశీలిస్తారు.", "Finally, they inspect the toy.")],
                [("మొదట ఆకారాన్ని చెక్కాడు, తరువాత రంగు వేశాడు.", "మొదట ఆకారాన్ని చెక్కి, తరువాత రంగు వేశాడు.", "Use the converb చెక్కి to link two actions by the same subject in this sequence." )],
                [("విద్యార్థిని", "రంగు వేయడానికి ముందు ఏమి చేస్తారు?", "What do they do before painting?"), ("కార్మికురాలు", "మొదట ఉపరితలాన్ని మృదువుగా చేస్తాం.", "First we smooth the surface."), ("విద్యార్థిని", "తర్వాత రంగు వేస్తారా?", "Do you paint it next?"), ("కార్మికురాలు", "అవును, పూత పూర్తిగా ఆరిన తర్వాత.", "Yes, after the coating has dried completely." )],
                ("Put the stages in order", [("Write the carving and smoothing steps.", ["మొదట", "చెక్కి", "మృదువుగా"], ["first", "carve", "smooth"]), ("Say when the painting begins.", ["ఆరిన తర్వాత", "రంగు వేస్తారు"], ["after it dries", "they paint"])])
            ),
            _lesson(
                "Ask a craftsperson about a toy",
                "Ask a respectful question about a toy's size and price and respond to the answer.",
                [("ధర", "price", "noun"), ("పరిమాణం", "size", "noun"), ("ఎత్తు", "height", "noun"), ("తక్కువ", "less; lower", "adjective"), ("చూపించడం", "to show", "verb")],
                ("question words and respectful request", "ఎంత? / ఎంత ఎత్తు? · చూపించగలరా?", "Ask for a price with ధర ఎంత? and for height with ఎంత ఎత్తు? A respectful request can use చూపించగలరా?; keep the question word with the information being requested."),
                [("ఈ బొమ్మ ధర ఎంత?", "What is the price of this toy?"), ("ఏనుగు బొమ్మ ఎంత ఎత్తు ఉంది?", "How tall is the elephant toy?"), ("కొంచెం దగ్గరగా చూపించగలరా?", "Could you show it a little closer?")],
                [("ఈ బొమ్మ ఎంత ధర ఉంది?", "ఈ బొమ్మ ధర ఎంత?", "Ask directly with the natural price frame ధర ఎంత?" )],
                [("కొనుగోలుదారు", "ఈ ఏనుగు బొమ్మ ధర ఎంత?", "What is the price of this elephant toy?"), ("అమ్మకందారు", "చిన్నది ఐదు వందల రూపాయలు.", "The small one is five hundred rupees."), ("కొనుగోలుదారు", "పెద్ద బొమ్మను చూపించగలరా?", "Could you show me the larger toy?"), ("అమ్మకందారు", "తప్పకుండా, ఇదిగో చూడండి.", "Certainly, here it is." )],
                ("Complete the purchase exchange", [("Ask the price of the small toy.", ["చిన్న బొమ్మ", "ధర ఎంత?"], ["small toy", "what is the price?"]), ("Ask to see the larger toy respectfully.", ["పెద్ద బొమ్మ", "చూపించగలరా?"], ["larger toy", "could you show?"])])
            ),
        ]},
        {"id": "A1+-U2", "title": "రూపం, రంగు, ప్రదర్శన", "lessons": [
            _lesson(
                "Describe a toy's shape and colour",
                "Give two visible details about a toy so another visitor can identify it.",
                [("ఆకారం", "shape", "noun"), ("నీలం", "blue", "adjective"), ("ఎరుపు", "red", "adjective"), ("ఏనుగు", "elephant", "noun"), ("ఎడమవైపు", "on the left", "adverb")],
                ("adjectives before nouns and location", "colour + noun; ఎడమవైపు / కుడివైపు", "Place a colour adjective before the noun. Use ఎడమవైపు and కుడివైపు to locate an item in a display, and keep the main predicate at the end."),
                [("నీలం రంగు పక్షి బొమ్మ ఎడమవైపు ఉంది.", "The blue bird toy is on the left."), ("ఎరుపు ఏనుగు మధ్యలో ఉంది.", "The red elephant is in the middle."), ("ఆ రెండు బొమ్మల ఆకారం వేరు.", "The shapes of those two toys are different.")],
                [("ఎడమవైపు నీలం బొమ్మ ఉంది రంగు.", "ఎడమవైపు నీలం రంగు బొమ్మ ఉంది.", "Keep the colour phrase together before the noun: నీలం రంగు బొమ్మ." )],
                [("చిన్నారి", "పక్షి బొమ్మ ఎక్కడ ఉంది?", "Where is the bird toy?"), ("తల్లి", "నీలం రంగు పక్షి ఎడమవైపు ఉంది.", "The blue bird is on the left."), ("చిన్నారి", "ఎరుపు ఏనుగు కూడా ఉందా?", "Is there a red elephant too?"), ("తల్లి", "ఉంది, అది మధ్యలో ఉంది.", "Yes, it is in the middle." )],
                ("Describe a display position", [("Name the colour and object.", ["నీలం రంగు", "పక్షి బొమ్మ"], ["blue", "bird toy"]), ("Say where the elephant is.", ["ఎరుపు ఏనుగు", "మధ్యలో"], ["red elephant", "in the middle"])])
            ),
            _lesson(
                "Compare two figures",
                "Compare the size or colour of two objects without claiming that one is universally better.",
                [("కంటే", "than", "postposition"), ("పెద్దది", "larger one", "adjective"), ("చిన్నది", "smaller one", "adjective"), ("రెండూ", "both", "pronoun"), ("ఎంచుకోవడం", "to choose", "verb")],
                ("comparison with కంటే", "A, B కంటే + adjective", "Attach -కంటే to the item used as the comparison point. Use పెద్దది or చిన్నది for size; use రెండూ when you mean both items share a feature."),
                [("ఈ బొమ్మ ఆ బొమ్మ కంటే పెద్దది.", "This toy is larger than that toy."), ("రెండూ చేతితో చేసిన బొమ్మలే.", "Both are handmade toys."), ("మీకు ఏది నచ్చింది?", "Which one did you like?")],
                [("ఈ బొమ్మ ఆ బొమ్మ కంటే పెద్దగా ఉంది.", "ఈ బొమ్మ ఆ బొమ్మ కంటే పెద్దది.", "Compare two toys with the adjective పెద్దది; avoid an unnecessary adverb ending here." )],
                [("స్నేహితుడు", "ఈ పక్షి బొమ్మ ఆ ఏనుగు కంటే చిన్నదా?", "Is this bird toy smaller than that elephant?"), ("స్నేహితురాలు", "అవును, కానీ రెండూ అందంగా ఉన్నాయి.", "Yes, but both are beautiful."), ("స్నేహితుడు", "మీకు ఏది నచ్చింది?", "Which one did you like?"), ("స్నేహితురాలు", "నాకు చిన్న పక్షి బొమ్మ నచ్చింది.", "I liked the small bird toy." )],
                ("Compare and choose", [("Compare a bird with an elephant toy.", ["పక్షి బొమ్మ", "ఏనుగు బొమ్మ కంటే"], ["bird toy", "than the elephant toy"]), ("Say which one you prefer.", ["నాకు", "నచ్చింది"], ["I", "liked it"])])
            ),
            _lesson(
                "Invite someone to a toy display",
                "Invite a friend to a household display and explain when it is open.",
                [("ప్రదర్శన", "display; exhibition", "noun"), ("ఆహ్వానించడం", "to invite", "verb"), ("సాయంత్రం", "evening", "noun"), ("వచ్చే", "upcoming; next", "adjective"), ("చూడటం", "to see", "verb")],
                ("future time and polite invitation", "వచ్చే + day/time; రండి / వస్తారా?", "Use వచ్చే with a coming day or event. A respectful imperative రండి is a warm invitation; వస్తారా? asks whether the person can come."),
                [("వచ్చే ఆదివారం మా ఇంట్లో బొమ్మల ప్రదర్శన ఉంది.", "There is a toy display at our home next Sunday."), ("సాయంత్రం ఆరు గంటలకు రండి.", "Please come at six in the evening."), ("మీరు కూడా చూస్తారా?", "Will you come and see it too?")],
                [("వచ్చే ఆదివారం ప్రదర్శన ఉండింది.", "వచ్చే ఆదివారం ప్రదర్శన ఉంటుంది.", "A future event takes the future form ఉంటుంది, not past ఉండింది." )],
                [("అనన్య", "వచ్చే ఆదివారం మా ఇంట్లో బొమ్మల ప్రదర్శన ఉంది.", "There is a toy display at our home next Sunday."), ("సుమ", "ఎప్పుడు రావాలి?", "When should I come?"), ("అనన్య", "సాయంత్రం ఆరు గంటలకు రండి.", "Please come at six in the evening."), ("సుమ", "ధన్యవాదాలు, తప్పకుండా వస్తాను.", "Thank you; I will certainly come." )],
                ("Write an invitation", [("Give the day and place.", ["వచ్చే ఆదివారం", "మా ఇంట్లో"], ["next Sunday", "at our home"]), ("Add a polite invitation.", ["సాయంత్రం ఆరు గంటలకు", "రండి"], ["at six in the evening", "please come"])])
            ),
        ]},
        {"id": "A1+-U3", "title": "కథ, కొనుగోలు, కృతజ్ఞత", "lessons": [
            _lesson(
                "Choose a toy as a gift",
                "Choose a toy for a child and explain one reason for the choice.",
                [("బహుమతి", "gift", "noun"), ("పిల్లవాడు", "child", "noun"), ("తేలిక", "lightweight", "adjective"), ("ఎందుకంటే", "because", "conjunction"), ("ప్యాక్ చేయడం", "to pack", "verb")],
                ("give a reason with ఎందుకంటే", "choice + ఎందుకంటే + reason", "Name the choice first, then give its reason with ఎందుకంటే. Keep the reason concrete, such as size or the recipient's interest; avoid promising that every toy suits every child."),
                [("చిన్న పక్షి బొమ్మ తీసుకుంటాను, ఎందుకంటే అది తేలికగా ఉంది.", "I will take the small bird toy because it is light."), ("పిల్లవాడికి జంతువుల కథలు ఇష్టం.", "The child likes stories about animals."), ("దయచేసి దీన్ని కాగితంలో ప్యాక్ చేయండి.", "Please wrap this in paper." )],
                [("చిన్న బొమ్మ తీసుకుంటాను ఎందుకంటే తేలికగా.", "చిన్న బొమ్మ తీసుకుంటాను, ఎందుకంటే అది తేలికగా ఉంది.", "Give the reason as a complete clause with its subject and predicate." )],
                [("కొనుగోలుదారు", "ఈ బొమ్మ బహుమతిగా సరిపోతుందా?", "Would this toy be suitable as a gift?"), ("అమ్మకందారు", "పిల్లవాడికి జంతువులంటే ఇష్టమైతే సరిపోతుంది.", "It suits if the child likes animals."), ("కొనుగోలుదారు", "అయితే చిన్న పక్షి బొమ్మ తీసుకుంటాను.", "Then I will take the small bird toy."), ("అమ్మకందారు", "సరే, కాగితంలో చుట్టి ఇస్తాను.", "All right, I will wrap it in paper." )],
                ("Explain a gift choice", [("Name the gift and give one reason.", ["చిన్న పక్షి బొమ్మ", "ఎందుకంటే"], ["small bird toy", "because"]), ("Ask for it to be wrapped.", ["కాగితంలో", "ప్యాక్ చేయండి"], ["in paper", "please wrap"])])
            ),
            _lesson(
                "Tell a toy's small story",
                "Describe a toy figure and connect it to a simple imagined story.",
                [("గ్రామం", "village", "noun"), ("రైతు", "farmer", "noun"), ("జంతువు", "animal", "noun"), ("కథ", "story", "noun"), ("చెప్పడం", "to tell", "verb")],
                ("noun + story role", "ఇది ...; కథలో ...", "Use ఇది to identify the object, then కథలో to place its character in an imagined story. Signal that it is a story rather than a factual description when needed."),
                [("ఇది ఒక రైతు బొమ్మ.", "This is a farmer figure."), ("కథలో రైతు గ్రామానికి వెళ్తాడు.", "In the story, the farmer goes to a village."), ("పక్కన ఉన్న జంతువు అతనికి దారి చూపిస్తుంది.", "The animal beside him shows him the way." )],
                [("ఇది రైతు కథ బొమ్మ.", "ఇది రైతు బొమ్మ.", "Identify the figure with రైతు బొమ్మ; కథలో introduces the imagined story separately." )],
                [("కథకుడు", "ఈ బొమ్మ ఎవరి పాత్ర?", "Whose character is this figure?"), ("చిన్నారి", "ఇది గ్రామానికి వెళ్లే రైతు పాత్ర.", "It is the character of a farmer going to a village."), ("కథకుడు", "అతనికి ఎవరు దారి చూపిస్తారు?", "Who shows him the way?"), ("చిన్నారి", "పక్కన ఉన్న జంతువు దారి చూపిస్తుంది.", "The animal beside him shows the way." )],
                ("Describe an imagined scene", [("Name the figure.", ["రైతు బొమ్మ"], ["farmer figure"]), ("Add one sentence beginning with కథలో.", ["కథలో", "గ్రామానికి"], ["in the story", "to the village"])])
            ),
            _lesson(
                "Thank a craftsperson",
                "Thank a craftsperson for explaining the work and ask permission before taking a photograph.",
                [("వివరించడం", "to explain", "verb"), ("అనుమతి", "permission", "noun"), ("ఫోటో", "photo", "noun"), ("తీసుకోవడం", "to take", "verb"), ("ధన్యవాదాలు", "thank you", "phrase")],
                ("permission with -వచ్చా?", "చేయ + వచ్చా?", "Ask permission with a verb ending in -వచ్చా? such as ఫోటో తీసుకోవచ్చా? Answer respectfully, and thank the person for the explanation."),
                [("మీరు వివరించినందుకు ధన్యవాదాలు.", "Thank you for explaining."), ("ఫోటో తీసుకోవచ్చా?", "May I take a photo?"), ("అనుమతి ఉంటే మాత్రమే తీసుకోండి.", "Please take one only if permission is given." )],
                [("ఫోటో తీసుకుంటారా?", "ఫోటో తీసుకోవచ్చా?", "Use -వచ్చా? to ask for permission, rather than asking what the other person will do." )],
                [("సందర్శకురాలు", "బొమ్మల తయారీ వివరించినందుకు ధన్యవాదాలు.", "Thank you for explaining how the toys are made."), ("కార్మికుడు", "మీకు ఉపయోగపడిందని సంతోషం.", "I am glad it was useful to you."), ("సందర్శకురాలు", "ఫోటో తీసుకోవచ్చా?", "May I take a photo?"), ("కార్మికుడు", "అవును, ఈ బొమ్మల వరుసను మాత్రమే తీసుకోండి.", "Yes, please photograph only this row of toys." )],
                ("Close the visit respectfully", [("Thank the craftsperson.", ["వివరించినందుకు", "ధన్యవాదాలు"], ["for explaining", "thank you"]), ("Ask permission to take a photo.", ["ఫోటో", "తీసుకోవచ్చా?"], ["photo", "may I take?"])])
            ),
        ]},
    ],
    "test": [
        ("translation", "Say: This toy is made of wood.", "ఇది చెక్కతో చేసిన బొమ్మ."),
        ("translation", "Ask respectfully: Could you show the larger toy?", "పెద్ద బొమ్మను చూపించగలరా?"),
        ("translation", "Say: First carve the shape, then paint it.", "మొదట ఆకారాన్ని చెక్కి, తరువాత రంగు వేస్తారు."),
        ("short_answer", "Which suffix marks the material in చెక్కతో?", "-తో"),
        ("translation", "Ask: Who made this bird toy?", "ఈ పక్షి బొమ్మను ఎవరు చేశారు?"),
        ("short_answer", "What does చూపించగలరా? make the request?", "polite / respectful"),
        ("translation", "They smooth the surface before painting it.", "రంగు వేయడానికి ముందు ఉపరితలాన్ని మృదువుగా చేస్తారు."),
        ("translation", "Both are handmade toys.", "రెండూ చేతితో చేసిన బొమ్మలే."),
        ("translation", "Please wrap the bird toy in paper.", "పక్షి బొమ్మను కాగితంలో చుట్టి ఇవ్వండి."),
        ("short_answer", "Which question asks for a toy's price?", "ధర ఎంత?"),
    ],
    "extra": HALF_EXTRAS["A1+"],
}

HALFSTEPS["A2+"] = {
    "title": "Telugu A2+ — Story order, quotation and retelling",
    "native": NATIVE,
    "goals": [
        "Retell a short narrative in a clear sequence",
        "Report what a speaker said with అని",
        "Respond to an audience question and distinguish event from comment",
    ],
    "units": [
        {"id": "A2+-U1", "title": "కథకు పరిచయం", "lessons": [
            _lesson(
                "Introduce a village story",
                "Introduce the place and main character of a short imagined village story.",
                [("కథకుడు", "storyteller", "noun"), ("ప్రధాన పాత్ర", "main character", "noun"), ("గ్రామం", "village", "noun"), ("ప్రారంభం", "beginning", "noun"), ("ఒకప్పుడు", "once upon a time", "adverb")],
                ("setting before the main event", "ఒకప్పుడు + place; తరువాత + character", "Begin with a time marker such as ఒకప్పుడు, then introduce the setting and character. Keep this narrative opening distinct from a factual claim about a real community or performance."),
                [("ఒకప్పుడు నది పక్కన ఒక చిన్న గ్రామం ఉండేది.", "Once there was a small village beside a river."), ("ఆ గ్రామంలో మాలతి అనే యువతి నివసించేది.", "A young woman named Malathi lived in that village."), ("కథ ప్రారంభంలో ఆమె ఒక ప్రయాణానికి సిద్ధమవుతుంది.", "At the beginning of the story, she prepares for a journey.")],
                [("ఒకప్పుడు గ్రామం నది పక్కన ఉండేది.", "ఒకప్పుడు నది పక్కన ఒక చిన్న గ్రామం ఉండేది.", "Put the setting phrase near the beginning and include the verb ఉండేది for the past narrative setting." )],
                [("నిర్వాహకురాలు", "కథ ఎక్కడ మొదలవుతుంది?", "Where does the story begin?"), ("కథకుడు", "నది పక్కన ఉన్న ఒక చిన్న గ్రామంలో.", "In a small village beside a river."), ("నిర్వాహకురాలు", "ప్రధాన పాత్ర ఎవరు?", "Who is the main character?"), ("కథకుడు", "మాలతి అనే యువతి ప్రయాణానికి సిద్ధమవుతుంది.", "A young woman named Malathi prepares for a journey." )],
                ("Write a story opening", [("Name the setting and character.", ["నది పక్కన", "మాలతి అనే యువతి"], ["beside the river", "a young woman named Malathi"]), ("Add what happens at the beginning.", ["కథ ప్రారంభంలో", "ప్రయాణానికి సిద్ధమవుతుంది"], ["at the beginning of the story", "prepares for a journey"])])
            ),
            _lesson(
                "Link story events in order",
                "Connect three events in a short story without losing who performs each action.",
                [("తర్వాత", "after that", "adverb"), ("సహాయం", "help", "noun"), ("కనిపించడం", "to appear; be seen", "verb"), ("చేరడం", "to arrive", "verb"), ("చివరికి", "finally", "adverb")],
                ("converbs and sequence words", "verb + -ి; మొదట · తరువాత · చివరికి", "Link actions performed by one subject with a converb such as చూసి or అడిగి. Use sequence words to guide the listener, and change the subject explicitly when another character takes over."),
                [("మొదట మాలతి దారి తప్పి, తరువాత ఒక ప్రయాణికుడిని అడిగింది.", "First Malathi lost her way, then she asked a traveller."), ("అతను దారి చూపి, ఆమెను వంతెన దగ్గరకు తీసుకెళ్లాడు.", "He showed the way and took her near the bridge."), ("చివరికి ఆమె గ్రామానికి చేరింది.", "Finally she reached the village." )],
                [("అతను దారి చూపాడు ఆమె గ్రామానికి చేరింది.", "అతను దారి చూపి, ఆమె గ్రామానికి చేరింది.", "Use a converb to link the first action to what followed; keep the subject change clear if the actions have different subjects." )],
                [("కథకుడు", "మాలతి దారి తప్పిన తర్వాత ఏమి చేసింది?", "What did Malathi do after she lost her way?"), ("శ్రోత", "ఒక ప్రయాణికుడిని అడిగింది.", "She asked a traveller."), ("కథకుడు", "అతను ఎలా సహాయం చేశాడు?", "How did he help?"), ("శ్రోత", "దారి చూపి వంతెన దగ్గరకు తీసుకెళ్లాడు.", "He showed her the way and took her near the bridge." )],
                ("Arrange the events", [("Put the traveller's action before the arrival.", ["దారి చూపి", "గ్రామానికి చేరింది"], ["showed the way", "reached the village"]), ("Add the final sequence marker.", ["చివరికి"], ["finally"])])
            ),
            _lesson(
                "Describe a character's choice",
                "Explain why a character makes a choice and what changes because of it.",
                [("ఎంపిక", "choice", "noun"), ("నమ్మకం", "trust", "noun"), ("భయం", "fear", "noun"), ("నిర్ణయం", "decision", "noun"), ("ఫలితం", "result", "noun")],
                ("reason with ఎందుకంటే and result with అందువల్ల", "choice + ఎందుకంటే + reason; అందువల్ల + result", "Use ఎందుకంటే to give the character's reason and అందువల్ల to signal a consequence. These explain the imagined plot; do not state them as facts about a real person's motives."),
                [("ఆమె ఒంటరిగా వెళ్లలేదు, ఎందుకంటే దారి తెలియదు.", "She did not go alone because she did not know the way."), ("ఆమె సహాయం అడిగింది; అందువల్ల సురక్షితంగా చేరింది.", "She asked for help; as a result, she arrived safely."), ("ఆ నిర్ణయం కథను మరో దిశకు తీసుకెళ్లింది.", "That decision took the story in another direction." )],
                [("ఆమె సహాయం అడిగింది, అందువల్ల దారి తెలియదు.", "ఆమె దారి తెలియదు కాబట్టి సహాయం అడిగింది.", "Use కాబట్టి for the reason before the action; the original sentence reverses the cause and result." )],
                [("శ్రోత", "మాలతి ఒంటరిగా ఎందుకు వెళ్లలేదు?", "Why did Malathi not go alone?"), ("కథకుడు", "ఆమెకు దారి తెలియదు కాబట్టి సహాయం అడిగింది.", "She asked for help because she did not know the way."), ("శ్రోత", "ఆ నిర్ణయం వల్ల ఏమైంది?", "What happened because of that decision?"), ("కథకుడు", "ఆమె సురక్షితంగా గ్రామానికి చేరింది.", "She reached the village safely." )],
                ("Explain a character's decision", [("Give the reason for asking for help.", ["దారి తెలియదు", "సహాయం అడిగింది"], ["did not know the way", "asked for help"]), ("State the result.", ["అందువల్ల", "సురక్షితంగా చేరింది"], ["as a result", "arrived safely"])])
            ),
        ]},
        {"id": "A2+-U2", "title": "కథ, మాట, ప్రశ్న", "lessons": [
            _lesson(
                "Report a storyteller's words",
                "Report a short line from a storyteller using the Telugu quotative marker అని.",
                [("అని", "that; quotation marker", "particle"), ("చెప్పడం", "to say", "verb"), ("జవాబు", "answer", "noun"), ("నిజం", "truth", "noun"), ("సందేశం", "message", "noun")],
                ("quotative అని with చెప్పాడు/చెప్పింది", "quoted words + అని + verb of saying", "Place అని after the quoted words and before a verb such as చెప్పాడు, చెప్పింది or అడిగాడు. The quote reports what someone said; it does not by itself verify that statement."),
                [("కథకుడు ప్రయాణం కష్టంగా ఉందని చెప్పాడు.", "The storyteller said that the journey was difficult."), ("ఆమె దారి కనుగొంటానని చెప్పింది.", "She said that she would find the way."), ("ఆ మాటే కథలోని సందేశమని శ్రోత భావించాడు.", "The listener thought that those words were the story's message." )],
                [("కథకుడు ప్రయాణం కష్టంగా ఉంది చెప్పాడు.", "కథకుడు ప్రయాణం కష్టంగా ఉందని చెప్పాడు.", "Use అని to connect the reported words to చెప్పాడు." )],
                [("శ్రోత", "మాలతి ఏమని చెప్పింది?", "What did Malathi say?"), ("కథకుడు", "నేను దారి కనుగొంటానని చెప్పింది.", "She said, 'I will find the way.'"), ("శ్రోత", "ఆమె నిజంగా దారి కనుగొన్నదా?", "Did she actually find the way?"), ("కథకుడు", "అవును, తరువాతి ఘట్టంలో కనుగొంటుంది.", "Yes, she finds it in the next episode." )],
                ("Report the line", [("Connect the statement to the reporting verb.", ["ప్రయాణం కష్టంగా ఉంది", "అని"], ["the journey is difficult", "that"]), ("Write the report with చెప్పాడు.", ["కథకుడు", "చెప్పాడు"], ["storyteller", "said"])])
            ),
            _lesson(
                "Respond to a listener's question",
                "Answer a listener's question about the story and make clear which character an answer concerns.",
                [("శ్రోత", "listener", "noun"), ("ప్రశ్న", "question", "noun"), ("ఎందుకు", "why", "question word"), ("సమాధానం", "answer", "noun"), ("అయితే", "however; then", "connector")],
                ("question word and answer focus", "ఎవరు? ఎప్పుడు? ఎందుకు? · answer + subject", "Use the question word that matches the information requested. Start the answer with the relevant character or event when two people are present, so pronouns do not become ambiguous."),
                [("మాలతి ఎవరిని కలిసింది?", "Whom did Malathi meet?"), ("ఆమె ఒక వృద్ధ ప్రయాణికుడిని కలిసింది.", "She met an elderly traveller."), ("అయితే అతను అక్కడికి ఎందుకు వచ్చాడు?", "Then why had he come there?" )],
                [("ఆమె అతన్ని కలిసింది. అతను ఎందుకు?", "మాలతి ఒక ప్రయాణికుడిని కలిసింది. అతను దారి చూపడానికి అక్కడికి వచ్చాడు.", "Name the people and complete the answer so the pronouns have clear referents." )],
                [("శ్రోత", "వృద్ధ ప్రయాణికుడు అక్కడికి ఎందుకు వచ్చాడు?", "Why had the elderly traveller come there?"), ("కథకురాలు", "అతను సమీప గ్రామానికి వెళ్తున్నాడు.", "He was going to a nearby village."), ("శ్రోత", "అయితే మాలతికి దారి ఎలా చూపించాడు?", "Then how did he show Malathi the way?"), ("కథకురాలు", "మ్యాప్ చూసి వంతెన వరకు తీసుకెళ్లాడు.", "He checked a map and took her as far as the bridge." )],
                ("Answer with a clear referent", [("Answer why the traveller was there.", ["సమీప గ్రామానికి", "వెళ్తున్నాడు"], ["to a nearby village", "was going"]), ("Name how he helped Malathi.", ["మ్యాప్ చూసి", "వంతెన వరకు"], ["after checking a map", "as far as the bridge"])])
            ),
            _lesson(
                "Separate an event from a comment",
                "Distinguish an event in the narrative from a storyteller's comment about it.",
                [("ఘటన", "event", "noun"), ("వ్యాఖ్య", "comment", "noun"), ("వివరించడం", "to describe", "verb"), ("నిజానికి", "in fact", "adverb"), ("కథనం", "narration", "noun")],
                ("contrast with కానీ and అయితే", "event; కానీ + comment", "Use కానీ or అయితే to contrast the event with a comment or interpretation. Keep the event in a past clause and attribute an opinion to the speaker rather than presenting it as a verified fact."),
                [("మాలతి వంతెన దాటింది, కానీ కథకుడు ఆ నిర్ణయాన్ని ప్రమాదకరమని అన్నాడు.", "Malathi crossed the bridge, but the storyteller called that decision risky."), ("ఘటన కథలో ఉంది; వ్యాఖ్య కథకుడిది.", "The event is in the story; the comment belongs to the storyteller."), ("నిజానికి, మరో పాత్ర వేరే కారణం చెప్పింది.", "In fact, another character gave a different reason." )],
                [("కథకుడు నిర్ణయం ప్రమాదకరం అని అనుకున్నది.", "కథకుడు ఆ నిర్ణయాన్ని ప్రమాదకరమని అన్నాడు.", "Use the natural report pattern నిర్ణయాన్ని ... అని అన్నాడు, and keep the reporting subject clear." )],
                [("సంపాదకుడు", "ఆ ప్రమాదం కథలో జరిగిన సంఘటనా, లేక వ్యాఖ్యనా?", "Is that danger an event in the story or a comment?"), ("కథకురాలు", "వంతెన దాటడం సంఘటన; ప్రమాదకరమని చెప్పడం నా వ్యాఖ్య.", "Crossing the bridge is the event; calling it risky is my comment."), ("సంపాదకుడు", "మరో పాత్ర ఏమంటుంది?", "What does the other character say?"), ("కథకురాలు", "ఆమె దారిని సురక్షితమని భావిస్తుంది.", "She considers the path safe." )],
                ("Label fact and comment", [("Write the event and the storyteller's comment separately.", ["వంతెన దాటడం", "ప్రమాదకరమని"], ["crossing the bridge", "that it was risky"]), ("Add a contrasting viewpoint.", ["మరో పాత్ర", "సురక్షితమని"], ["another character", "that it was safe"])])
            ),
        ]},
        {"id": "A2+-U3", "title": "కథను తిరిగి చెప్పడం", "lessons": [
            _lesson(
                "Give a three-sentence retelling",
                "Retell a short narrative in three sentences: setting, turning point and outcome.",
                [("సారాంశం", "summary", "noun"), ("మలుపు", "turning point", "noun"), ("పరిణామం", "outcome", "noun"), ("సంక్షిప్తంగా", "briefly", "adverb"), ("ముగింపు", "ending", "noun")],
                ("parallel sequence in a summary", "setting; turning point; outcome", "Keep one main event in each sentence and use తరువాత or చివరికి to make the order explicit. A summary selects events; it does not need to repeat every detail."),
                [("కథ నది పక్కన ఉన్న గ్రామంలో మొదలవుతుంది.", "The story begins in a village beside a river."), ("మాలతి దారి తప్పినప్పుడు ప్రయాణికుడు సహాయం చేస్తాడు.", "When Malathi loses her way, a traveller helps."), ("చివరికి ఆమె సురక్షితంగా ఇంటికి చేరుతుంది.", "Finally she reaches home safely." )],
                [("కథ ముగింపు మొదలవుతుంది గ్రామంలో.", "కథ గ్రామంలో మొదలై, చివరికి మాలతి ఇంటికి చేరుతుంది.", "Put the setting at the start and the outcome at the end of the summary." )],
                [("ఉపాధ్యాయురాలు", "మూడు వాక్యాల్లో కథ చెప్పగలరా?", "Can you tell the story in three sentences?"), ("విద్యార్థి", "కథ గ్రామంలో మొదలవుతుంది.", "The story begins in a village."), ("విద్యార్థి", "మాలతి దారి తప్పినప్పుడు ఒక ప్రయాణికుడు సహాయం చేస్తాడు.", "When Malathi loses her way, a traveller helps."), ("విద్యార్థి", "చివరికి ఆమె ఇంటికి చేరుతుంది.", "Finally she reaches home." )],
                ("Build a compact retelling", [("Write the setting in the first sentence.", ["గ్రామంలో", "మొదలవుతుంది"], ["in a village", "begins"]), ("Add the outcome with చివరికి.", ["చివరికి", "ఇంటికి చేరుతుంది"], ["finally", "reaches home"])])
            ),
            _lesson(
                "Compare two tellings of a story",
                "Compare two retellings and state one detail that differs without declaring either speaker unreliable.",
                [("వెర్షన్", "version", "noun"), ("వివరం", "detail", "noun"), ("తేడా", "difference", "noun"), ("సమానంగా", "similarly", "adverb"), ("మారడం", "to change", "verb")],
                ("comparison with ఒకటిలో / మరొకటిలో", "ఒక కథనంలో ...; మరొక కథనంలో ...", "Use one frame for each retelling. Compare the detail stated, then describe what is shared; a difference by itself is not evidence that either speaker is dishonest."),
                [("ఒక కథనంలో మాలతి ఒంటరిగా ప్రయాణిస్తుంది.", "In one telling, Malathi travels alone."), ("మరొక కథనంలో ఆమె స్నేహితురాలితో వెళ్తుంది.", "In another telling, she goes with a friend."), ("రెండింటిలోనూ ఆమె దారి తప్పుతుంది.", "In both, she loses her way." )],
                [("ఒక కథనం, మరొక కథనం స్నేహితురాలు.", "ఒక కథనంలో ఆమె ఒంటరిగా వెళ్తుంది; మరొక కథనంలో స్నేహితురాలితో వెళ్తుంది.", "Use complete clauses to state what differs in each version." )],
                [("విద్యార్థిని", "రెండు కథనాల్లో ఏ తేడా ఉంది?", "What difference is there between the two tellings?"), ("ఉపాధ్యాయుడు", "ఒకదానిలో మాలతి ఒంటరిగా వెళ్తుంది.", "In one, Malathi goes alone."), ("విద్యార్థిని", "మరొకదానిలో స్నేహితురాలు ఉంది.", "In the other, a friend is there."), ("ఉపాధ్యాయుడు", "అయినా రెండింటిలోనూ ఆమె దారి తప్పుతుంది.", "Even so, she loses her way in both." )],
                ("Compare without judging", [("State one difference between the tellings.", ["ఒక కథనంలో", "మరొక కథనంలో"], ["in one telling", "in the other telling"]), ("State a shared event.", ["రెండింటిలోనూ", "దారి తప్పుతుంది"], ["in both", "loses her way"])])
            ),
            _lesson(
                "Invite a group to discuss a story",
                "Invite classmates to discuss a story's choices and moderate disagreement respectfully.",
                [("చర్చ", "discussion", "noun"), ("అభిప్రాయం", "opinion", "noun"), ("గౌరవించడం", "to respect", "verb"), ("అంగీకరించడం", "to agree", "verb"), ("భిన్నం", "different", "adjective")],
                ("softening an opinion", "నా అభిప్రాయం ప్రకారం ...; మీకు ఎలా అనిపించింది?", "Use నా అభిప్రాయం ప్రకారం to mark a personal view rather than a fact. Invite another person's response with మీకు ఎలా అనిపించింది? and acknowledge a different reading without forcing agreement."),
                [("నా అభిప్రాయం ప్రకారం, మాలతి సహాయం అడగడం సరైన నిర్ణయం.", "In my opinion, asking for help was the right decision."), ("మీకు ఆ ముగింపు ఎలా అనిపించింది?", "How did that ending seem to you?"), ("భిన్నమైన అభిప్రాయాన్ని కూడా గౌరవించాలి.", "A different opinion should also be respected." )],
                [("నా అభిప్రాయం నిజం ప్రకారం ఇదే.", "నా అభిప్రాయం ప్రకారం ఇదే సరైన ముగింపు.", "Mark an interpretation as an opinion with నా అభిప్రాయం ప్రకారం, not as an objective truth." )],
                [("సమావేశ నిర్వాహకుడు", "మాలతి నిర్ణయం గురించి మీ అభిప్రాయం ఏమిటి?", "What is your opinion about Malathi's decision?"), ("విద్యార్థిని", "నా అభిప్రాయం ప్రకారం ఆమె సహాయం అడగడం సరైంది.", "In my opinion, it was right for her to ask for help."), ("సమావేశ నిర్వాహకుడు", "ఇంకెవరైనా భిన్నంగా భావిస్తున్నారా?", "Does anyone else feel differently?"), ("విద్యార్థి", "అవును, కానీ ఆ అభిప్రాయాన్ని గౌరవిస్తాను.", "Yes, but I respect that opinion." )],
                ("Moderate a short discussion", [("State a view as an opinion.", ["నా అభిప్రాయం ప్రకారం", "సరైన నిర్ణయం"], ["in my opinion", "right decision"]), ("Invite another perspective.", ["భిన్నంగా", "మీకు ఎలా అనిపించింది?"], ["differently", "how did it seem to you?"])])
            ),
        ]},
    ],
    "test": [
        ("translation", "Report: The storyteller said that the journey was difficult.", "కథకుడు ప్రయాణం కష్టంగా ఉందని చెప్పాడు."),
        ("translation", "Finally she reached the village.", "చివరికి ఆమె గ్రామానికి చేరింది."),
        ("short_answer", "Which particle marks reported words?", "అని"),
        ("short_answer", "Give one phrase that marks a personal opinion.", "నా అభిప్రాయం ప్రకారం"),
        ("translation", "At first Malathi waited near the old bridge.", "మొదట మాలతి పాత వంతెన దగ్గర వేచి ఉంది."),
        ("short_answer", "Which word can introduce a result after an event?", "దాంతో"),
        ("translation", "Although the path was long, they continued.", "దారి పొడవుగా ఉన్నప్పటికీ, వారు కొనసాగారు."),
        ("short_answer", "Which word means 'finally' in the retelling?", "చివరికి"),
        ("translation", "The storyteller said that a helper arrived.", "సహాయకుడు వచ్చాడని కథకుడు చెప్పాడు."),
        ("argument_construction", "Retell a short event in order and attribute one detail to its speaker.", "An acceptable answer uses a clear sequence and marks the reported words with అని."),
    ],
    "extra": HALF_EXTRAS["A2+"],
}

HALFSTEPS["B1+"] = {
    "title": "Telugu B1+ — Cheriyal scrolls, sequence and captions",
    "native": NATIVE,
    "goals": [
        "Describe how a scroll presents a story through linked scenes",
        "Write captions that connect a picture to its narrative context",
        "Discuss a source-backed craft detail without overgeneralising",
    ],
    "units": [
        {"id": "B1+-U1", "title": "చిత్రంలో కథా క్రమం", "lessons": [
            _lesson(
                "Read a story across scroll panels",
                "Describe how a viewer follows a story through a sequence of pictured episodes.",
                [("చుట్ట", "scroll", "noun"), ("దృశ్యం", "scene", "noun"), ("ప్యానెల్", "panel", "noun"), ("సన్నివేశం", "episode; scene", "noun"), ("క్రమం", "sequence", "noun")],
                ("relative participle for a pictured action", "verb + -న + noun", "Use a relative participle such as చూపించిన to describe the picture or action that follows. When comparing panels, name the earlier and later scene so the story order remains clear."),
                [("మొదటి దృశ్యంలో ప్రయాణం మొదలుపెట్టిన పాత్ర కనిపిస్తుంది.", "The character who began the journey appears in the first scene."), ("తదుపరి ప్యానెల్‌లో దారి చూపించిన వ్యక్తి కనిపిస్తాడు.", "The person who showed the way appears in the next panel."), ("చివరి సన్నివేశం కథకు ముగింపు ఇస్తుంది.", "The final episode gives the story its ending." )],
                [("ప్రయాణం మొదలుపెట్టిన మొదటి దృశ్యం పాత్ర కనిపిస్తుంది.", "మొదటి దృశ్యంలో ప్రయాణం మొదలుపెట్టిన పాత్ర కనిపిస్తుంది.", "Keep the location phrase దృశ్యంలో before the character description; place the relative clause directly before పాత్ర." )],
                [("సంపాదకురాలు", "మొదటి ప్యానెల్‌లో ఏమి కనిపిస్తోంది?", "What appears in the first panel?"), ("చిత్రకారుడు", "ప్రయాణం మొదలుపెట్టిన పాత్ర కనిపిస్తోంది.", "The character who began the journey appears."), ("సంపాదకురాలు", "తరువాతి దృశ్యంలో ఎవరు వస్తారు?", "Who comes in the next scene?"), ("చిత్రకారుడు", "దారి చూపించిన వ్యక్తి కనిపిస్తాడు.", "The person who showed the way appears." )],
                ("Caption the scene order", [("Describe the first pictured action.", ["మొదటి దృశ్యంలో", "ప్రయాణం మొదలుపెట్టిన పాత్ర"], ["in the first scene", "the character who began the journey"]), ("Name who appears next.", ["తదుపరి ప్యానెల్‌లో", "దారి చూపించిన వ్యక్తి"], ["in the next panel", "the person who showed the way"])])
            ),
            _lesson(
                "Describe a painting surface",
                "Explain, in sequence, how a scroll surface is prepared and why the artist waits before drawing.",
                [("వస్త్రం", "cloth", "noun"), ("పొర", "layer; coating", "noun"), ("పూత", "coating", "noun"), ("ఆరబెట్టడం", "to let dry", "verb"), ("రూపురేఖ", "outline", "noun")],
                ("purpose clause with ముందు", "చర్యకు ముందు + material/action", "Use ముందు to say what happens before another action. Link the steps with an explicit subject or a converb when the same person performs them; report the described material as a source detail, not as a rule for every painting."),
                [("చిత్రం గీయడానికి ముందు వస్త్రంపై పూత వేస్తారు.", "Before drawing, they apply a coating to the cloth."), ("పూత పూర్తిగా ఆరిన తర్వాత రూపురేఖలు గీస్తారు.", "After the coating dries completely, they draw the outlines."), ("ఈ పద్ధతి గురించి సంస్థ ఇచ్చిన వివరణలో ఉంది.", "This method appears in the organisation's description." )],
                [("పూత ఆరిన ముందు రూపురేఖలు గీస్తారు.", "పూత ఆరిన తర్వాత రూపురేఖలు గీస్తారు.", "Use తర్వాత to mean after the coating dries; ముందు would reverse the intended order." )],
                [("విద్యార్థి", "రూపురేఖలు ఎప్పుడు గీస్తారు?", "When are the outlines drawn?"), ("కళాకారిణి", "పూత పూర్తిగా ఆరిన తర్వాత గీస్తాం.", "We draw them after the coating has dried completely."), ("విద్యార్థి", "అందుకు ముందు వస్త్రాన్ని సిద్ధం చేస్తారా?", "Do you prepare the cloth before that?"), ("కళాకారిణి", "అవును, ముందు ఉపరితలాన్ని సమంగా చేస్తాం.", "Yes, first we make the surface even." )],
                ("Explain a making step", [("State what happens before drawing.", ["చిత్రం గీయడానికి ముందు", "పూత వేస్తారు"], ["before drawing", "they apply a coating"]), ("State when the outline is added.", ["పూత ఆరిన తర్వాత", "రూపురేఖలు గీస్తారు"], ["after the coating dries", "they draw the outlines"])])
            ),
            _lesson(
                "Track a character through the story",
                "Follow one character across several panels and explain how the character's situation changes.",
                [("పాత్ర", "character", "noun"), ("సహాయకుడు", "helper", "noun"), ("తిరిగి", "back; again", "adverb"), ("మార్పు", "change", "noun"), ("గుర్తించడం", "to identify", "verb")],
                ("the same referent across clauses", "పాత్ర మొదట ...; తరువాత అదే పాత్ర ...", "Repeat the character's name or use అదే పాత్ర when a pronoun could be unclear. Use మొదట and తరువాత to make a change across panels easy to follow."),
                [("మొదట పాత్ర ఒంటరిగా ప్రయాణిస్తుంది.", "At first the character travels alone."), ("తరువాత అదే పాత్ర ఒక సహాయకుడిని కలుస్తుంది.", "Later the same character meets a helper."), ("చివరి దృశ్యంలో ఇద్దరూ కలిసి తిరిగి వస్తారు.", "In the last scene, the two return together." )],
                [("తరువాత అతను సహాయకుడిని కలుస్తాడు. అతను ఒంటరిగా ఉన్నాడు.", "తరువాత పాత్ర ఒక సహాయకుడిని కలుస్తుంది; ఆ సమయంలో పాత్ర ఒంటరిగా ప్రయాణిస్తోంది.", "Avoid an ambiguous pronoun when two characters appear; name the referent and the time of the change." )],
                [("మార్గదర్శి", "మొదటి దృశ్యంలో పాత్ర ఒంటరిగా ఉందా?", "Is the character alone in the first scene?"), ("చిత్రకారుడు", "అవును, కానీ తరువాత సహాయకుడిని కలుస్తుంది.", "Yes, but later the character meets a helper."), ("మార్గదర్శి", "చివరికి ఎవరు కలిసి వస్తారు?", "Who returns together at the end?"), ("చిత్రకారుడు", "ప్రధాన పాత్ర, సహాయకుడు ఇద్దరూ.", "The main character and the helper, both." )],
                ("Write a character path", [("Describe the character at the start and later.", ["మొదట", "తరువాత"], ["at first", "later"]), ("Name who returns together.", ["ఇద్దరూ", "కలిసి తిరిగి వస్తారు"], ["both", "return together"])])
            ),
        ]},
        {"id": "B1+-U2", "title": "శీర్షిక, శైలి, సందర్భం", "lessons": [
            _lesson(
                "Write a useful panel caption",
                "Write a short caption that tells the reader who is pictured and what is happening.",
                [("శీర్షిక", "caption; heading", "noun"), ("సందర్భం", "context", "noun"), ("చర్య", "action", "noun"), ("సంక్షిప్తం", "concise", "adjective"), ("స్పష్టంగా", "clearly", "adverb")],
                ("who + action + context", "పాత్ర + action + time/place", "Put the character and action before background information. A caption should identify the scene without inventing details that are not visible or provided by the source."),
                [("నది దగ్గర దారి అడుగుతున్న మాలతి.", "Malathi asking for directions near the river."), ("సాయంత్రం గ్రామానికి చేరిన ప్రయాణికులు.", "The travellers who arrived at the village in the evening."), ("ఈ శీర్షిక దృశ్యానికి సందర్భం ఇస్తుంది.", "This caption gives context to the scene." )],
                [("నది దగ్గర మాలతి దారి అడుగు.", "నది దగ్గర మాలతి దారి అడుగుతోంది.", "Use a finite verb or a clear participial caption; the singular imperative అడుగు does not describe this scene." )],
                [("సంపాదకుడు", "శీర్షికలో ఏ సమాచారం తప్పనిసరిగా ఉండాలి?", "What information must be in the caption?"), ("చిత్రకారిణి", "పాత్ర, చర్య, అవసరమైతే స్థలం.", "The character, action and, if needed, the place."), ("సంపాదకుడు", "కనిపించని వివరాన్ని చేర్చాలా?", "Should we add a detail that is not visible?"), ("చిత్రకారిణి", "ఆధారం లేకపోతే చేర్చకూడదు.", "We should not add it without evidence." )],
                ("Draft a caption", [("Name who is pictured and what they are doing.", ["మాలతి", "దారి అడుగుతోంది"], ["Malathi", "is asking for directions"]), ("Add a place only if supported.", ["నది దగ్గర"], ["near the river"])])
            ),
            _lesson(
                "Interview an artist about a story choice",
                "Ask an artist why a character or episode was placed in a particular panel.",
                [("ఎంచుకోవడం", "to choose", "verb"), ("స్థానం", "placement; position", "noun"), ("ఎందుకు", "why", "question word"), ("ముఖ్యం", "important", "adjective"), ("ప్రేరణ", "inspiration", "noun")],
                ("ask why and report a reason", "ఎందుకు + verb?; ... కాబట్టి ఎంచుకున్నాను", "Ask an open question with ఎందుకు and answer with a reason that belongs to the artist. Use కాబట్టి to connect that reason to the panel choice."),
                [("ఈ దృశ్యాన్ని ఇక్కడ ఎందుకు ఉంచారు?", "Why did you place this scene here?"), ("కథలో మలుపు ఇక్కడ వస్తుంది కాబట్టి ఎంచుకున్నాను.", "I chose it because the turning point comes here in the story."), ("ఆ నిర్ణయం తరువాతి ప్యానెల్‌ను స్పష్టం చేస్తుంది.", "That decision clarifies the next panel." )],
                [("దృశ్యాన్ని ఇక్కడ ఎందుకు ఉంచారు మీరు?", "ఈ దృశ్యాన్ని ఇక్కడ ఎందుకు ఉంచారు?", "Keep the object and question word before the respectful verb in this neutral question." )],
                [("విద్యార్థిని", "ప్రధాన పాత్రను పెద్దగా ఎందుకు చిత్రించారు?", "Why did you paint the main character larger?"), ("చిత్రకారిణి", "ఆమె కథలో ముఖ్యమైన పాత్ర కాబట్టి.", "Because she is an important character in the story."), ("విద్యార్థిని", "అది పాఠకుడికి ఎలా సహాయపడుతుంది?", "How does that help the reader?"), ("చిత్రకారిణి", "ఎవరి చర్యపై దృష్టి పెట్టాలో తెలుస్తుంది.", "It shows whose action to focus on." )],
                ("Write an interview question", [("Ask why a scene is in this position.", ["ఈ దృశ్యాన్ని", "ఎందుకు ఉంచారు?"], ["this scene", "why did you place?"]), ("Record the artist's reason.", ["ముఖ్యమైన పాత్ర", "కాబట్టి"], ["important character", "because"])])
            ),
            _lesson(
                "Clarify a source detail",
                "Check whether a description comes from a source or is an interpretation added by a visitor.",
                [("వివరణ", "description", "noun"), ("మూలం", "source", "noun"), ("ప్రకారం", "according to", "postposition"), ("అనిపించడం", "to seem", "verb"), ("నిర్ధారించడం", "to confirm", "verb")],
                ("attribution with ప్రకారం", "source + ప్రకారం + stated detail", "Place ప్రకారం after the named source or speaker. Use అనిపిస్తోంది to mark an interpretation, and do not turn it into a source-confirmed fact without checking."),
                [("సంస్థ వివరణ ప్రకారం, ఈ చుట్టలో అనేక దృశ్యాలు ఉన్నాయి.", "According to the organisation's description, this scroll has several scenes."), ("నాకు చివరి దృశ్యం ముగింపులా అనిపిస్తోంది.", "The last scene seems like an ending to me."), ("ఆ భావాన్ని మరో మూలంతో నిర్ధారించాలి.", "That interpretation should be checked against another source." )],
                [("సంస్థ ప్రకారం నాకు చివరి దృశ్యం ముగింపు.", "సంస్థ వివరణ ప్రకారం, ఈ చుట్టలో అనేక దృశ్యాలు ఉన్నాయి.", "Keep source attribution separate from a personal interpretation; do not make the source the speaker of your opinion." )],
                [("సంపాదకురాలు", "ఈ వివరాన్ని ఎవరు నిర్ధారించారు?", "Who confirmed this detail?"), ("పరిశోధకుడు", "సంస్థ వివరణలో ఉంది; నా వ్యాఖ్య వేరుగా ఉంది.", "It is in the organisation's description; my comment is separate."), ("సంపాదకురాలు", "అయితే వ్యాఖ్యను ఎలా గుర్తించాలి?", "Then how should we mark the comment?"), ("పరిశోధకుడు", "నాకు అనిపిస్తోంది అని స్పష్టంగా రాస్తాను.", "I will clearly write 'it seems to me'." )],
                ("Mark source and opinion", [("Attribute a detail to the organisation.", ["సంస్థ వివరణ ప్రకారం"], ["according to the organisation's description"]), ("Mark the personal interpretation.", ["నాకు", "అనిపిస్తోంది"], ["to me", "it seems"])])
            ),
        ]},
        {"id": "B1+-U3", "title": "కథను ప్రేక్షకులకు అందించడం", "lessons": [
            _lesson(
                "Explain how a story changes",
                "Describe a turning point and explain how it changes the next scene.",
                [("మలుపు", "turning point", "noun"), ("దిశ", "direction", "noun"), ("ప్రతిస్పందన", "response", "noun"), ("దాంతో", "as a result", "connector"), ("తదుపరి", "next", "adjective")],
                ("result and transition", "event; దాంతో + changed direction", "Use దాంతో to connect the turning point to its result. Identify the event first, then state what changes in the next scene."),
                [("ప్రయాణికుడు దారి చూపిస్తాడు; దాంతో కథ కొత్త దిశలో సాగుతుంది.", "The traveller shows the way; as a result, the story moves in a new direction."), ("తదుపరి దృశ్యంలో మాలతి తిరిగి గ్రామానికి వెళ్తుంది.", "In the next scene, Malathi returns to the village."), ("ఆమె ప్రతిస్పందన కథ మలుపును స్పష్టం చేస్తుంది.", "Her response clarifies the story's turning point." )],
                [("దాంతో ముందు దారి చూపించాడు కథ కొత్త దిశ.", "ప్రయాణికుడు దారి చూపించాడు; దాంతో కథ కొత్త దిశలో సాగింది.", "Put the action before the result connector and complete the result clause with its verb." )],
                [("మార్గదర్శి", "కథలో మలుపు ఎక్కడ వస్తుంది?", "Where does the turning point occur?"), ("చిత్రకారుడు", "ప్రయాణికుడు సహాయం చేసినప్పుడు.", "When the traveller offers help."), ("మార్గదర్శి", "దాంతో తరువాత ఏమి మారుతుంది?", "As a result, what changes next?"), ("చిత్రకారుడు", "మాలతి తిరిగి వెళ్లాలని నిర్ణయిస్తుంది.", "Malathi decides to return." )],
                ("Describe a turning point", [("Name the event that changes the story.", ["ప్రయాణికుడు", "సహాయం చేసినప్పుడు"], ["the traveller", "when he helps"]), ("State what changes next.", ["దాంతో", "తిరిగి వెళ్లాలని నిర్ణయిస్తుంది"], ["as a result", "decides to return"])])
            ),
            _lesson(
                "Prepare a two-minute gallery introduction",
                "Introduce a narrative-art display to visitors and guide them through one sequence of scenes.",
                [("సందర్శకుడు", "visitor", "noun"), ("ప్రవేశం", "entrance", "noun"), ("వివరణకర్త", "guide; explainer", "noun"), ("క్రమంగా", "in order", "adverb"), ("గమనించండి", "please notice", "verb")],
                ("polite imperative and guided sequence", "ముందుగా చూడండి · తరువాత గమనించండి", "Use respectful plural imperatives to guide a group. Name the first detail to look at, then lead attention to the next panel; keep directions short enough to follow while viewing."),
                [("ముందుగా ఎడమవైపు ఉన్న మొదటి దృశ్యాన్ని చూడండి.", "First, look at the opening scene on the left."), ("తరువాత పాత్రల క్రమాన్ని గమనించండి.", "Then notice the sequence of characters."), ("చివరగా కథ ముగింపును చదవండి.", "Finally, read the story's ending." )],
                [("ముందుగా దృశ్యాన్ని చూడు.", "ముందుగా దృశ్యాన్ని చూడండి.", "Address a group of visitors respectfully with చూడండి." )],
                [("వివరణకర్త", "ముందుగా ప్రవేశద్వారం దగ్గర ఆగండి.", "First, pause near the entrance."), ("సందర్శకురాలు", "తరువాత ఏ ప్యానెల్ చూడాలి?", "Which panel should we see next?"), ("వివరణకర్త", "ఎడమ నుంచి కుడికి క్రమంగా చూడండి.", "Please view them in order from left to right."), ("సందర్శకురాలు", "చివరి దృశ్యమే ముగింపు అని అర్థమైంది.", "I understand that the last scene is the ending." )],
                ("Guide a visitor", [("Give one first instruction politely.", ["ముందుగా", "చూడండి"], ["first", "please look"]), ("Direct attention to the sequence.", ["ఎడమ నుంచి కుడికి", "క్రమంగా"], ["from left to right", "in order"])])
            ),
            _lesson(
                "Reflect on a visitor's interpretation",
                "Respond to a visitor's interpretation by acknowledging it and adding a source-supported detail.",
                [("వ్యాఖ్యానం", "interpretation", "noun"), ("అంగీకరించడం", "to agree", "verb"), ("భిన్నంగా", "differently", "adverb"), ("ఆధారంగా", "based on", "postposition"), ("సంభాషణ", "conversation", "noun")],
                ("concession with అయినా", "మీ వ్యాఖ్యను అంగీకరిస్తాను; అయినా + detail", "Acknowledge a visitor's interpretation before adding a different detail with అయినా. Use ఆధారంగా to identify what supports the additional point, and keep the conversation respectful."),
                [("మీ వ్యాఖ్యను అర్థం చేసుకున్నాను; అయినా మరో దృశ్యాన్ని కూడా చూడాలి.", "I understand your interpretation; still, we should also look at another scene."), ("మూల వివరణ ఆధారంగా కథా క్రమాన్ని గుర్తించవచ్చు.", "The story sequence can be identified based on the source description."), ("భిన్నమైన వ్యాఖ్యానం చర్చను విస్తరిస్తుంది.", "A different interpretation broadens the discussion." )],
                [("మీ వ్యాఖ్యను అర్థం చేసుకున్నాను అయినా మరో దృశ్యాన్ని కూడా చూడాలి.", "మీ వ్యాఖ్యను అర్థం చేసుకున్నాను; అయినా మరో దృశ్యాన్ని కూడా చూడాలి.", "Use punctuation to separate the acknowledgement from the concessive continuation." )],
                [("సందర్శకుడు", "ఈ పాత్ర కథకుడికి కోపంగా కనిపిస్తోంది.", "This character seems angry to the storyteller."), ("వివరణకర్త", "ఆ వ్యాఖ్యను అర్థం చేసుకున్నాను; అయినా ముఖభావం వేరేలా కూడా చదవవచ్చు.", "I understand that interpretation; still, the facial expression could also be read differently."), ("సందర్శకుడు", "మూల వివరణలో ఏముంది?", "What is in the source description?"), ("వివరణకర్త", "అది దృశ్య క్రమాన్ని చెబుతుంది, భావాన్ని ఖచ్చితంగా నిర్ణయించదు.", "It gives the sequence of scenes; it does not determine the emotion with certainty." )],
                ("Respond with care", [("Acknowledge the visitor's reading.", ["మీ వ్యాఖ్యను", "అర్థం చేసుకున్నాను"], ["your interpretation", "I understand"]), ("Add what the source does and does not establish.", ["మూల వివరణ", "ఖచ్చితంగా నిర్ణయించదు"], ["source description", "does not determine with certainty"])])
            ),
        ]},
    ],
    "test": [
        ("translation", "The character who began the journey appears in the first scene.", "మొదటి దృశ్యంలో ప్రయాణం మొదలుపెట్టిన పాత్ర కనిపిస్తుంది."),
        ("translation", "According to the organisation's description, this scroll has several scenes.", "సంస్థ వివరణ ప్రకారం, ఈ చుట్టలో అనేక దృశ్యాలు ఉన్నాయి."),
        ("short_answer", "Which connector can introduce the result of a turning point?", "దాంతో"),
        ("short_answer", "What should a caption avoid inventing?", "కనిపించని వివరాలు / ఆధారం లేని వివరాలు"),
        ("translation", "The next scene shows a gathering in the village.", "తదుపరి దృశ్యం గ్రామంలో ఒక సమావేశాన్ని చూపిస్తుంది."),
        ("short_answer", "Which phrase attributes a detail to its source?", "మూలం ప్రకారం / సంస్థ వివరణ ప్రకారం"),
        ("translation", "The caption links the image to the next part of the story.", "శీర్షిక చిత్రాన్ని కథలోని తదుపరి భాగంతో అనుసంధానిస్తుంది."),
        ("short_answer", "Should a caption state an uncertain emotion as a fact?", "No; mark it as an interpretation or leave it open."),
        ("translation", "The source gives the scene order but does not determine the character's emotion.", "మూలం దృశ్యాల క్రమాన్ని చెబుతుంది, కానీ పాత్ర భావాన్ని నిర్ధారించదు."),
        ("argument_construction", "Write a caption that describes what is visible and marks one uncertain inference.", "An acceptable caption separates visible detail from interpretation and does not invent missing context."),
    ],
    "extra": HALF_EXTRAS["B1+"],
}

HALFSTEPS["B2+"] = {
    "title": "Telugu B2+ — Weaving specifications and responsible product writing",
    "native": NATIVE,
    "goals": [
        "Record a textile order with measurable specifications",
        "Negotiate a delivery change and document quality concerns",
        "Attribute product claims to a source and qualify recommendations",
    ],
    "units": [
        {"id": "B2+-U1", "title": "నమూనా, అంచు, కొలత", "lessons": [
            _lesson(
                "Read a Mangalagiri product description",
                "Extract product details from a government description and distinguish description from evaluation.",
                [("మగ్గం", "loom", "noun"), ("అంచు", "border", "noun"), ("నూలు", "yarn", "noun"), ("వివరణ", "description", "noun"), ("లక్షణం", "feature", "noun")],
                ("source attribution with a relative clause", "వివరణ ప్రకారం + detail; ... ఉన్న వస్త్రం", "Attribute a feature to the named description with ప్రకారం. Use a relative clause such as ఉన్న వస్త్రం to group details, and keep an evaluative statement separate from what the source reports."),
                [("శాఖ వివరణ ప్రకారం, మంగళగిరి వస్త్రాలు గుంటూరు ప్రాంతంతో సంబంధం కలిగి ఉన్నాయి.", "According to the department description, Mangalagiri textiles are associated with the Guntur region."), ("పిట్ మగ్గంపై నేసిన వస్త్రం నమూనాలో చూపించారు.", "The textile woven on a pit loom was shown in the sample."), ("నిజాం అంచు ఆ వివరణలో పేర్కొన్న ఒక లక్షణం.", "The Nizam border is one feature mentioned in that description." )],
                [("వివరణ ప్రకారం ఇది అత్యుత్తమ వస్త్రం.", "వివరణ ప్రకారం ఇందులో నిజాం అంచు ఉంది.", "Do not add an unsupported superlative; attribute the feature that the source actually describes." )],
                [("కొనుగోలుదారు", "ఈ నమూనాలో ఏ వివరాలు మూల వివరణతో సరిపోతాయి?", "Which details in this sample match the source description?"), ("సంపాదకురాలు", "మగ్గం, అంచు గురించి వివరాలు ఉన్నాయి.", "There are details about the loom and border."), ("కొనుగోలుదారు", "నాణ్యతపై అభిప్రాయాన్ని కూడా జోడించాలా?", "Should we also add an opinion about quality?"), ("సంపాదకురాలు", "జోడించవచ్చు, కానీ అది మన అంచనా అని గుర్తించాలి.", "We can, but we should mark it as our assessment." )],
                ("Separate a sourced feature", [("Attribute one concrete feature to the department.", ["వివరణ ప్రకారం", "అంచు"], ["according to the description", "border"]), ("Mark an evaluation as your own.", ["మన అంచనా", "నాణ్యత"], ["our assessment", "quality"])])
            ),
            _lesson(
                "Specify a sample's dimensions",
                "Record border width, textile length and colour in a clear order form.",
                [("వెడల్పు", "width", "noun"), ("పొడవు", "length", "noun"), ("కొలత", "measurement", "noun"), ("నమూనా", "sample", "noun"), ("నమోదు", "record", "noun")],
                ("measurement clauses and object marking", "item-ను + measure-తో నమోదు చేయండి", "Mark the item being recorded with -ను. State the unit with the number and put each specification on its own line when precision matters."),
                [("అంచు వెడల్పును సెంటీమీటర్లలో నమోదు చేయండి.", "Record the border width in centimetres."), ("వస్త్రం పొడవు ఐదు మీటర్లు.", "The textile length is five metres."), ("నమూనాలోని రంగును ఆమోదించిన తర్వాతే ఆర్డర్ ఖాయం.", "The order is confirmed only after the sample colour is approved." )],
                [("అంచు వెడల్పు సెంటీమీటర్ నమోదు చేయండి.", "అంచు వెడల్పును సెంటీమీటర్లలో నమోదు చేయండి.", "Mark the width as the object and state the unit with -లలో." )],
                [("నేతకారుడు", "అంచు వెడల్పు ఎంత కావాలి?", "What border width would you like?"), ("కొనుగోలుదారు", "నమూనాలో ఉన్న కొలతనే నమోదు చేయండి.", "Please record the measurement shown in the sample."), ("నేతకారుడు", "రంగును కూడా ఇప్పుడు ఖరారు చేద్దామా?", "Shall we confirm the colour now too?"), ("కొనుగోలుదారు", "ముందుగా రంగు నమూనాను ఆమోదిస్తాను.", "I will approve the colour sample first." )],
                ("Complete an order form", [("Record a width from the sample.", ["అంచు వెడల్పును", "నమూనాలో ఉన్న కొలత"], ["border width", "the measurement in the sample"]), ("State when the order is confirmed.", ["రంగు నమూనాను", "ఆమోదించిన తర్వాతే"], ["colour sample", "only after approval"])])
            ),
            _lesson(
                "Approve a colour sample",
                "Approve or request a change to a sample while making the next step conditional on confirmation.",
                [("ఆమోదించడం", "to approve", "verb"), ("మార్పు", "change", "noun"), ("నిర్ధారించడం", "to confirm", "verb"), ("ఒప్పందం", "agreement", "noun"), ("అప్పుడే", "only then", "adverb")],
                ("conditional with అయితే and అప్పుడే", "X అయితే, Y; X తర్వాతే Y", "Use అయితే to state a condition and అప్పుడే to emphasise that the next action follows only after approval. Put the requirement in writing if the order depends on it."),
                [("రంగు నమూనా సరిపోతే, ఆర్డర్‌ను ఖాయం చేస్తాను.", "If the colour sample is suitable, I will confirm the order."), ("మీరు నిర్ధారించిన తర్వాతే నూలు కొనండి.", "Buy the yarn only after you have confirmed."), ("మార్పు ఉంటే కొత్త నమూనా పంపండి.", "If there is a change, send a new sample." )],
                [("రంగు నమూనా సరిపోతుంది అయితే ఆర్డర్ ఖాయం.", "రంగు నమూనా సరిపోతే, ఆర్డర్‌ను ఖాయం చేస్తాను.", "Use the conditional form సరిపోతే and include the intended subject and action in the result clause." )],
                [("నేతకారుడు", "నీలి రంగు నమూనా సిద్ధంగా ఉంది.", "The blue colour sample is ready."), ("కొనుగోలుదారు", "అంచు రంగు కొద్దిగా మార్చగలరా?", "Could you change the border colour a little?"), ("నేతకారుడు", "మార్చిన నమూనా పంపిన తర్వాతే నేయడం మొదలుపెడతాను.", "I will begin weaving only after sending the revised sample."), ("కొనుగోలుదారు", "సరే, దాన్ని చూసి లిఖితంగా నిర్ధారిస్తాను.", "All right; I will review it and confirm in writing." )],
                ("Write an approval condition", [("State the condition for confirming the order.", ["రంగు నమూనా సరిపోతే", "ఆర్డర్‌ను ఖాయం చేస్తాను"], ["if the colour sample is suitable", "I will confirm the order"]), ("State what happens only after the sample is approved.", ["నిర్ధారించిన తర్వాతే", "నేయడం మొదలుపెడతాను"], ["only after confirmation", "I will begin weaving"])])
            ),
        ]},
        {"id": "B2+-U2", "title": "సమయపట్టిక, ఆలస్యం, పరిష్కారం", "lessons": [
            _lesson(
                "Agree on a delivery schedule",
                "Agree on a delivery date and identify which step needs to finish first.",
                [("సమయపట్టిక", "schedule", "noun"), ("గడువు", "deadline", "noun"), ("పూర్తి", "complete", "adjective"), ("పంపిణీ", "delivery", "noun"), ("ముందుగా", "first; beforehand", "adverb")],
                ("before-and-after clauses", "X పూర్తయ్యాక + Y; గడువులోపు + action", "Use అయ్యాక to place one completed step before the next. Mark a deadline with లోపు and name the action that must be completed by it."),
                [("రంగు ఆమోదం పూర్తయ్యాక నేయడం మొదలవుతుంది.", "Weaving begins after colour approval is complete."), ("వస్త్రాన్ని నెల చివరిలోపు పంపాలి.", "The textile must be sent by the end of the month."), ("ప్యాకింగ్‌కు ముందు తుది కొలతను తనిఖీ చేద్దాం.", "Let us check the final measurement before packing." )],
                [("ఆమోదం పూర్తవుతుంది తర్వాత నేయడం మొదలవుతుంది.", "ఆమోదం పూర్తయ్యాక నేయడం మొదలవుతుంది.", "Use the completed-action connector పూర్తయ్యాక before the next step." )],
                [("కొనుగోలుదారు", "ఏ తేదీలోపు పంపిణీ చేయగలరు?", "By what date can you deliver?"), ("నేతకారుడు", "రంగు ఆమోదం త్వరగా వస్తే, నెల చివరిలోపు పంపుతాను.", "If colour approval comes soon, I will send it by the end of the month."), ("కొనుగోలుదారు", "ముందుగా తుది కొలతను తనిఖీ చేద్దాం.", "Let us check the final measurement first."), ("నేతకారుడు", "సరే, సమయపట్టికను రాతపూర్వకంగా పంపుతాను.", "All right; I will send the schedule in writing." )],
                ("Set a delivery deadline", [("Name the step that must happen first.", ["రంగు ఆమోదం", "పూర్తయ్యాక"], ["colour approval", "after completion"]), ("State the delivery deadline.", ["నెల చివరిలోపు", "పంపాలి"], ["by the end of the month", "must send"])])
            ),
            _lesson(
                "Renegotiate a delayed order",
                "Explain a delay, offer a revised date and respond to the buyer's concern without hiding the cause.",
                [("ఆలస్యం", "delay", "noun"), ("కారణం", "reason", "noun"), ("మార్చడం", "to change", "verb"), ("వీలైతే", "if possible", "phrase"), ("వికల్పం", "alternative", "noun")],
                ("concession and revised plan", "ఆలస్యమైనప్పటికీ + plan; వీలైతే + alternative", "Acknowledge the delay before proposing a new date. Use అయినప్పటికీ for a concession and వీలైతే to offer an alternative, not to guarantee an uncertain delivery."),
                [("నూలు ఆలస్యంగా వచ్చినప్పటికీ పని కొనసాగుతోంది.", "Although the yarn arrived late, the work is continuing."), ("వీలైతే శుక్రవారం నమూనా పంపిస్తాను.", "If possible, I will send the sample on Friday."), ("కొత్త తేదీని ఒప్పందంలో నమోదు చేద్దాం.", "Let us record the new date in the agreement." )],
                [("నూలు ఆలస్యంగా వచ్చింది అయినా పని కొనసాగుతోంది.", "నూలు ఆలస్యంగా వచ్చినప్పటికీ పని కొనసాగుతోంది.", "Use the concessive participle వచ్చినప్పటికీ to connect the delay to the continuing work." )],
                [("కొనుగోలుదారు", "ఆర్డర్ రెండు రోజులు ఆలస్యమైంది; కొత్త తేదీ ఏది?", "The order is two days late; what is the new date?"), ("నేతకారుడు", "నూలు ఆలస్యంగా వచ్చింది, అందుకే శుక్రవారం పంపుతాను.", "The yarn arrived late, so I will send it on Friday."), ("కొనుగోలుదారు", "అది సాధ్యం కాకపోతే ముందుగా తెలియజేయండి.", "If that is not possible, please let me know first."), ("నేతకారుడు", "సరే, మార్పు ఉంటే వెంటనే రాతపూర్వకంగా చెబుతాను.", "All right; if anything changes, I will tell you in writing immediately." )],
                ("Write a revised schedule", [("Acknowledge the cause of delay.", ["నూలు", "ఆలస్యంగా వచ్చింది"], ["yarn", "arrived late"]), ("Offer the revised date and a fallback.", ["శుక్రవారం", "సాధ్యం కాకపోతే"], ["Friday", "if it is not possible"])])
            ),
            _lesson(
                "Document a quality concern",
                "Describe a difference between a sample and a delivered textile and request a practical remedy.",
                [("నాణ్యత", "quality", "noun"), ("లోపం", "defect", "noun"), ("పోల్చడం", "to compare", "verb"), ("సరిచేయడం", "to correct", "verb"), ("పరిహారం", "remedy", "noun")],
                ("contrast with కంటే and remedy request", "sample కంటే + difference; దయచేసి + remedy", "Use కంటే to compare the delivered item with the approved sample. Describe the observable difference, attach evidence if available and request a specific remedy rather than using an unsupported accusation."),
                [("పంపిన వస్త్రం నమూనా కంటే కొద్దిగా ముదురు రంగులో ఉంది.", "The delivered textile is slightly darker than the sample."), ("రెండు చిత్రాలను జతచేసి పంపుతున్నాను.", "I am sending two pictures attached."), ("దయచేసి మార్పు చేయగలరా?", "Could you please correct it?" )],
                [("పంపిన వస్త్రం నమూనా ముదురు రంగు కంటే ఉంది.", "పంపిన వస్త్రం నమూనా కంటే ముదురు రంగులో ఉంది.", "Use the comparative phrase నమూనా కంటే before the property being compared." )],
                [("కొనుగోలుదారు", "వస్త్రం నమూనా కంటే ముదురు రంగులో ఉంది.", "The textile is darker than the sample."), ("నేతకారుడు", "మీరు పంపిన చిత్రాలు చూశాను.", "I have seen the pictures you sent."), ("కొనుగోలుదారు", "తదుపరి దశగా అంచు రంగును సరిచేయగలరా?", "As the next step, could you correct the border colour?"), ("నేతకారుడు", "నమూనాతో పోల్చి, సాధ్యమైన పరిష్కారాన్ని రేపు చెబుతాను.", "I will compare it with the sample and tell you a possible solution tomorrow." )],
                ("Draft a quality note", [("Describe the measurable difference.", ["నమూనా కంటే", "ముదురు రంగులో"], ["than the sample", "darker in colour"]), ("Request one specific remedy.", ["అంచు రంగును", "సరిచేయగలరా?"], ["border colour", "could you correct?"])])
            ),
        ]},
        {"id": "B2+-U3", "title": "వివరణను సమీక్షించడం", "lessons": [
            _lesson(
                "Write a balanced textile label",
                "Write a concise label that names a source-reported feature and a limitation of the description.",
                [("లేబుల్", "label", "noun"), ("ప్రత్యేకత", "feature; distinction", "noun"), ("వివరంగా", "in detail", "adverb"), ("ఆపాదించడం", "to attribute", "verb"), ("పరిధి", "scope", "noun")],
                ("attribution and scope", "source ప్రకారం + feature; ఈ వివరణ + scope", "Name the source and the exact feature it reports. Use ఈ వివరణ to define the scope of the label and avoid implying that one page describes every Mangalagiri textile or every maker."),
                [("శాఖ పేజీ ప్రకారం, ఈ వస్త్రంలో నిజాం అంచు ఉంది.", "According to the department page, this textile has a Nizam border."), ("ఈ లేబుల్ నమూనాలోని వివరాలకే పరిమితం.", "This label is limited to the details in the sample."), ("నూలు వివరాలను వేరుగా నిర్ధారించాలి.", "The yarn details should be verified separately." )],
                [("ఈ పేజీ అన్ని వస్త్రాలు ఒకేలా అని చెబుతుంది.", "ఈ పేజీ కొన్ని వస్త్ర లక్షణాలను వివరిస్తుంది.", "Do not generalise from one description to all textiles; state the page's limited scope." )],
                [("సంపాదకుడు", "లేబుల్‌లో ఏ వివరాన్ని మూలానికి ఆపాదించాలి?", "Which detail in the label should be attributed to the source?"), ("విక్రేత", "నిజాం అంచు గురించి ఉన్న వాక్యాన్ని.", "The sentence about the Nizam border."), ("సంపాదకుడు", "అన్ని వస్త్రాలకు వర్తిస్తుందా?", "Does it apply to all textiles?"), ("విక్రేత", "కాదు, ఈ వివరణ పరిధి అంతవరకే.", "No; that is the scope of this description." )],
                ("Edit the product label", [("Attribute one source-reported feature.", ["శాఖ పేజీ ప్రకారం", "నిజాం అంచు"], ["according to the department page", "Nizam border"]), ("State a limitation of the description.", ["అన్ని వస్త్రాలకు కాదు", "పరిధి"], ["not all textiles", "scope"])])
            ),
            _lesson(
                "Explain care instructions to a buyer",
                "Explain textile-care instructions, ask the buyer to confirm understanding and report the source of the advice.",
                [("సంరక్షణ", "care", "noun"), ("సూచన", "instruction", "noun"), ("ఉతకడం", "to wash", "verb"), ("నేరుగా", "directly", "adverb"), ("తెలియజేయడం", "to inform", "verb")],
                ("reported instruction with -అని", "verb + -అని సూచించారు", "Use -అని with a reporting verb such as సూచించారు to attribute a care instruction. Do not invent a care requirement; use the product maker's confirmed guidance."),
                [("విక్రేత చేతితో ఉతకాలని సూచించారు.", "The seller advised washing it by hand."), ("నేరుగా ఎండలో ఉంచవద్దని కూడా చెప్పారు.", "They also said not to leave it in direct sunlight."), ("సూచన అర్థమైందో లేదో తెలియజేయండి.", "Please let me know whether the instruction is clear." )],
                [("విక్రేత చేతితో ఉతకాలి సూచించారు.", "విక్రేత చేతితో ఉతకాలని సూచించారు.", "Reported advice takes -అని/-అని contracted with -అని: ఉతకాలని సూచించారు." )],
                [("విక్రేత", "లేబుల్‌లోని సంరక్షణ సూచన చదివారా?", "Have you read the care instruction on the label?"), ("కొనుగోలుదారు", "చదివాను. చేతితో ఉతకాలని ఉంది.", "I have. It says to wash it by hand."), ("విక్రేత", "ఆ సూచన తయారీదారు ఇచ్చిందే.", "That instruction was provided by the maker."), ("కొనుగోలుదారు", "అర్థమైంది; సందేహం ఉంటే అడుగుతాను.", "Understood; I will ask if I have a question." )],
                ("Attribute a care instruction", [("Report what the label says.", ["చేతితో", "ఉతకాలని ఉంది"], ["by hand", "says to wash"]), ("Identify the source of the advice.", ["తయారీదారు", "సూచన"], ["maker", "instruction"])])
            ),
            _lesson(
                "Recommend a product with qualifications",
                "Recommend a textile for a stated use while naming the buyer's priorities and limits of your recommendation.",
                [("సిఫార్సు", "recommendation", "noun"), ("ప్రాధాన్యం", "priority", "noun"), ("వాడుక", "use", "noun"), ("తగిన", "suitable", "adjective"), ("అయితే", "if; however", "connector")],
                ("conditional recommendation", "మీ ప్రాధాన్యం X అయితే, Y తగినదై ఉండవచ్చు", "Base a recommendation on a stated priority. Use ఉండవచ్చు to qualify it when the buyer's full needs are not known, and invite a follow-up question instead of treating the recommendation as universal."),
                [("తేలికైన వస్త్రం మీ ప్రాధాన్యం అయితే, ఈ నమూనా తగినదై ఉండవచ్చు.", "If a light textile is your priority, this sample may be suitable."), ("రోజువారీ వాడుక కోసం అయితే, సంరక్షణ సూచనను కూడా చూడండి.", "If it is for everyday use, also check the care instruction."), ("మీ బడ్జెట్ చెబితే మరొక ఎంపిక చూపగలను.", "If you tell me your budget, I can show another option." )],
                [("మీకు ఏది కావాలో తెలియకపోయినా ఈ వస్త్రమే ఉత్తమం.", "మీ ప్రాధాన్యం తేలికైన వస్త్రమైతే, ఈ నమూనా సరిపోవచ్చు.", "Tie the recommendation to an explicit priority and avoid claiming it is best without knowing the buyer's needs." )],
                [("విక్రేత", "మీకు వస్త్రంలో ఏ లక్షణం ముఖ్యం?", "Which feature matters to you in a textile?"), ("కొనుగోలుదారు", "తేలికగా ఉండాలి, రోజువారీగా వాడాలి.", "It should be light and for everyday use."), ("విక్రేత", "ఈ నమూనా సరిపోవచ్చు; సంరక్షణ సూచన కూడా చూడండి.", "This sample may suit you; please also check its care instructions."), ("కొనుగోలుదారు", "ధన్యవాదాలు, బడ్జెట్‌లో మరో ఎంపిక ఉందా?", "Thank you; is there another option within my budget?" )],
                ("Write a qualified recommendation", [("State the buyer's priority.", ["తేలికగా", "రోజువారీగా"], ["light", "for everyday use"]), ("Offer a qualified option and invite a follow-up.", ["సరిపోవచ్చు", "మరో ఎంపిక"], ["may suit", "another option"])])
            ),
        ]},
    ],
    "test": [
        ("translation", "The textile is slightly darker than the sample.", "పంపిన వస్త్రం నమూనా కంటే కొద్దిగా ముదురు రంగులో ఉంది."),
        ("translation", "If the colour sample is suitable, I will confirm the order.", "రంగు నమూనా సరిపోతే, ఆర్డర్‌ను ఖాయం చేస్తాను."),
        ("short_answer", "Which word marks the comparison point in నమూనా కంటే?", "కంటే"),
        ("short_answer", "What must a product claim include when it comes from a source?", "source attribution / ప్రకారం"),
        ("short_answer", "Which word means 'slightly' in the first sentence?", "కొద్దిగా"),
        ("translation", "Please record the width before confirming the order.", "ఆర్డర్‌ను ఖాయం చేసే ముందు వెడల్పును నమోదు చేయండి."),
        ("short_answer", "Which phrase makes a recommendation less absolute?", "ఉండవచ్చు / సరిపోవచ్చు"),
        ("translation", "The colour differs from the sample, so we should review it.", "రంగు నమూనా కంటే భిన్నంగా ఉంది, కాబట్టి దాన్ని మళ్లీ పరిశీలించాలి."),
        ("short_answer", "Name two details to verify before recommending a textile.", "intended use and care instructions / వాడుక, సంరక్షణ సూచనలు"),
        ("argument_construction", "Recommend a textile for a stated use and name one limit to your recommendation.", "An acceptable answer states the buyer's priority, qualifies the recommendation, and invites clarification when needed."),
    ],
    "extra": HALF_EXTRAS["B2+"],
}

HALFSTEPS["C1+"] = {
    "title": "Telugu C1+ — Evidence, interpretation and public heritage writing",
    "native": NATIVE,
    "goals": [
        "Separate direct observation, source report and historical inference",
        "Write a qualified interpretation of an archaeological description",
        "Respond to an editorial challenge without overstating evidence",
    ],
    "units": [
        {"id": "C1+-U1", "title": "ఆధారం ఏ స్థాయిలో?", "lessons": [
            _lesson(
                "Separate three layers of a site report",
                "Classify a sentence as observation, source-attributed detail or inference.",
                [("ప్రత్యక్షం", "direct; immediate", "adjective"), ("ఆపాదన", "attribution", "noun"), ("నిర్ధారణ", "establishment; confirmation", "noun"), ("అనుమానం", "inference; doubt", "noun"), ("పరిశీలన", "observation", "noun")],
                ("three evidence frames", "నేను గమనించినది ...; మూలం ప్రకారం ...; ఇది ... కావచ్చు", "Use separate sentence frames for what you observed, what a named source states and what you infer. An interpretation can be useful while remaining explicitly provisional."),
                [("స్థలంలో రాతి పలకల అవశేషాలు కనిపించాయి.", "Remains of stone slabs were visible at the site."), ("పురావస్తు శాఖ వివరణ ప్రకారం, వాటిపై శిల్పాలు ఉన్నాయి.", "According to the archaeology department description, sculptures were on them."), ("ఇవి ఒక నిర్దిష్ట కాలానికి చెందినవని మరిన్ని ఆధారాలు అవసరం.", "More evidence is needed to establish that these belong to a particular period." )],
                [("స్థలంలో చూసినదే వాటి కాలాన్ని నిర్ధారిస్తుంది.", "స్థలంలో రాతి పలకల అవశేషాలు కనిపించాయి; వాటి కాలాన్ని వేరే ఆధారాలతో నిర్ధారించాలి.", "A visible feature does not by itself establish its date; separate observation from dating evidence." )],
                [("సమీక్షకుడు", "మొదటి వాక్యం ఏ ఆధార స్థాయిని చూపుతుంది?", "What evidence level does the first sentence show?"), ("రచయిత", "అది స్థలంలో చేసిన ప్రత్యక్ష పరిశీలన.", "It is a direct observation made at the site."), ("సమీక్షకుడు", "రెండో వాక్యం?", "And the second sentence?"), ("రచయిత", "అది శాఖ వివరణకు ఆపాదించిన సమాచారం.", "That is information attributed to the department description." )],
                ("Label each evidence layer", [("Write one direct observation.", ["స్థలంలో", "కనిపించాయి"], ["at the site", "were visible"]), ("Attribute a separate source statement.", ["వివరణ ప్రకారం", "శిల్పాలు"], ["according to the description", "sculptures"])])
            ),
            _lesson(
                "Quote an archaeological source precisely",
                "Paraphrase an official site description and keep the source's confidence and scope intact.",
                [("ఉటంకించడం", "to quote", "verb"), ("పారాయణం", "recitation", "noun"), ("పరిధి", "scope", "noun"), ("అంచనా", "estimate", "noun"), ("సూచించడం", "to indicate", "verb")],
                ("reported clause with అని and an estimate", "మూలం ... అని పేర్కొంటుంది; సుమారు + measure", "Use అని with a reporting verb such as పేర్కొంటుంది. Preserve qualifiers like సుమారు when the source gives an estimate, and do not broaden the claim beyond the described feature."),
                [("మూల వివరణ స్తూపం వ్యాసం సుమారు యాభై మీటర్లు అని పేర్కొంటుంది.", "The source description states that the stupa's diameter is about fifty metres."), ("సుమారు అనే పదం అంచనాను సూచిస్తుంది.", "The word about signals an estimate."), ("ఈ కొలతను మొత్తం స్థలానికి వర్తింపజేయరాదు.", "This measurement should not be applied to the entire site." )],
                [("మూలం స్తూపం వ్యాసం ఖచ్చితంగా యాభై మీటర్లు అని నిర్ధారిస్తుంది.", "మూల వివరణ స్తూపం వ్యాసం సుమారు యాభై మీటర్లు అని పేర్కొంటుంది.", "Preserve the source's qualifier సుమారు and reporting verb; an estimate is not an exact measurement." )],
                [("సంపాదకురాలు", "ఇక్కడ యాభై మీటర్లు ఖచ్చితమైన కొలతనా?", "Is fifty metres an exact measurement here?"), ("రచయిత", "కాదు, మూలం సుమారు అని చెబుతుంది.", "No; the source says approximately."), ("సంపాదకురాలు", "అయితే శీర్షికలో ఎలా రాయాలి?", "Then how should we write it in the heading?"), ("రచయిత", "అంచనా అని స్పష్టంగా ఉంచాలి.", "We should make clear that it is an estimate." )],
                ("Preserve a qualifier", [("Paraphrase the source's approximate figure.", ["సుమారు", "యాభై మీటర్లు"], ["about", "fifty metres"]), ("State what the figure measures.", ["స్తూపం", "వ్యాసం"], ["stupa", "diameter"])])
            ),
            _lesson(
                "Distinguish remains from reconstruction",
                "Describe what remains at a site and label a proposed reconstruction as a scholarly interpretation.",
                [("అవశేషం", "remains", "noun"), ("పునర్నిర్మాణం", "reconstruction", "noun"), ("ఆధారం", "evidence", "noun"), ("రూపకల్పన", "design", "noun"), ("ఊహాత్మకం", "hypothetical", "adjective")],
                ("contrast with కాగా and qualification", "అవశేషం ... కాగా, పునర్నిర్మాణం ...", "Use కాగా to contrast a surviving feature with a reconstruction. Add కావచ్చు or ఆధారంగా రూపొందింది when a proposed shape relies on interpretation rather than a complete surviving structure."),
                [("పునాది అవశేషాలు కనిపిస్తున్నాయి, కాగా పైభాగపు రూపం ఊహాత్మకం.", "The foundation remains are visible, whereas the upper form is hypothetical."), ("ఈ రూపకల్పన లభించిన ఆధారాలపై రూపొందింది.", "This design is based on the evidence found."), ("మరొక ఆధారం లభిస్తే పునర్నిర్మాణం మారవచ్చు.", "The reconstruction may change if further evidence is found." )],
                [("పైభాగం పూర్తిగా కనిపిస్తోంది కాగా అది ఊహాత్మకం.", "పునాది అవశేషాలు కనిపిస్తున్నాయి, కాగా పైభాగపు రూపం ఊహాత్మకం.", "State what is visible and what is reconstructed as separate, contrasting claims." )],
                [("పరిశోధకుడు", "చిత్రంలో పైభాగం కూడా అసలు నిర్మాణమేనా?", "Is the upper part in the image also the original structure?"), ("సంరక్షకురాలు", "కాదు, అది ఆధారాలపై రూపొందించిన ప్రతిపాదిత రూపం.", "No; it is a proposed form designed from evidence."), ("పరిశోధకుడు", "దాన్ని ఎలా గుర్తించాలి?", "How should we identify it?"), ("సంరక్షకురాలు", "పునర్నిర్మాణం అని స్పష్టంగా పేర్కొనాలి.", "We should clearly label it as a reconstruction." )],
                ("Label surviving and proposed elements", [("Name the visible remains.", ["పునాది", "అవశేషాలు"], ["foundation", "remains"]), ("Label the proposed upper form.", ["పైభాగపు రూపం", "ఊహాత్మకం"], ["upper form", "hypothetical"])])
            ),
        ]},
        {"id": "C1+-U2", "title": "సంరక్షణ, అర్థం, పాఠకుడు", "lessons": [
            _lesson(
                "Explain a conservation decision",
                "Explain why a display choice protects an original object while acknowledging trade-offs for visitors.",
                [("సంరక్షణ", "conservation", "noun"), ("ప్రతిరూపం", "replica", "noun"), ("ప్రాప్యత", "access", "noun"), ("ప్రమాదం", "risk", "noun"), ("సమతుల్యం", "balance", "noun")],
                ("concessive framing with అయినప్పటికీ", "X అయినప్పటికీ, Y అవసరం", "Use అయినప్పటికీ to acknowledge a real trade-off before stating the decision. Name who benefits and what is limited; avoid presenting a conservation choice as cost-free."),
                [("ప్రతిరూపం ద్వారా ప్రాప్యత పెరిగినప్పటికీ, అసలు వస్తువును చూడలేరు.", "Although access increases through a replica, visitors cannot see the original object."), ("అసలును కాపాడటానికి దూరం ఉంచడం అవసరం.", "Keeping a distance is necessary to protect the original."), ("సమతుల్య వివరణ సందర్శకుడికి కారణాన్ని చెబుతుంది.", "A balanced explanation tells visitors the reason." )],
                [("ప్రతిరూపం పెట్టడం వల్ల ప్రతి సందర్శకుడు అసలు వస్తువును చూశాడు.", "ప్రతిరూపం పెట్టడం వల్ల ప్రతి సందర్శకుడికి రూపం కనిపిస్తుంది; అసలు వస్తువును కాపాడవచ్చు.", "Do not confuse access to a replica with viewing the original; state both the benefit and limitation." )],
                [("సంరక్షకుడు", "ప్రతిరూపం ఎందుకు ప్రదర్శిస్తున్నారు?", "Why are you displaying a replica?"), ("వివరణకర్త", "అసలుకు హాని కలగకుండా రూపాన్ని చూపించడానికి.", "To show the form without harming the original."), ("సంరక్షకుడు", "సందర్శకుడికి ఏ పరిమితి చెప్పాలి?", "What limitation should we tell visitors?"), ("వివరణకర్త", "ఇది ప్రతిరూపం, అసలు వస్తువు కాదు అని చెప్పాలి.", "We should say that this is a replica, not the original." )],
                ("Draft a balanced display note", [("State the conservation reason.", ["అసలు", "హాని కలగకుండా"], ["original", "without causing harm"]), ("Label the replica honestly.", ["ప్రతిరూపం", "అసలు వస్తువు కాదు"], ["replica", "not the original"])])
            ),
            _lesson(
                "Write for two kinds of readers",
                "Adapt a heritage explanation for a local visitor and an international reader without changing its evidence.",
                [("లక్ష్య పాఠకుడు", "intended reader", "noun"), ("సంక్షిప్తీకరించడం", "to condense", "verb"), ("పదజాలం", "terminology", "noun"), ("పాదటిప్పణి", "footnote", "noun"), ("అనువాదం", "translation", "noun")],
                ("audience adaptation with while preserving", "పాఠకుడికి సరిపోయేలా + simplify; ఆధారాన్ని అలాగే ఉంచి", "Change the explanation or define a technical term for the intended reader, while retaining the source and evidence. Simpler language is not a licence to omit a necessary qualification."),
                [("స్థానిక పాఠకుడికి తెలిసిన పదాన్ని విదేశీ పాఠకుడికి వివరించాలి.", "A term familiar to a local reader should be explained to an international reader."), ("వాక్యాన్ని సంక్షిప్తం చేసినా, అంచనా అనే పదాన్ని ఉంచాలి.", "Even when shortening the sentence, keep the word estimate."), ("పాదటిప్పణిలో మూలాన్ని సూచించవచ్చు.", "The source can be indicated in a footnote." )],
                [("వాక్యం చిన్నదిగా చేయడానికి మూలాన్ని తొలగించాలి.", "వాక్యాన్ని సంక్షిప్తం చేసినా, మూలాన్ని సూచించాలి.", "Condense the wording without deleting the source attribution." )],
                [("అనువాదకురాలు", "ఈ పదానికి చిన్న వివరణ అవసరమా?", "Does this term need a short explanation?"), ("సంపాదకుడు", "అంతర్జాతీయ పాఠకుడికి అవసరం; స్థానిక పాఠకుడికి కాదు.", "It is needed for an international reader, but not for a local reader."), ("అనువాదకురాలు", "అయితే పాదటిప్పణి చేర్చుదామా?", "Then shall we add a footnote?"), ("సంపాదకుడు", "అవును, మూలాన్ని కూడా అక్కడ సూచించండి.", "Yes, indicate the source there too." )],
                ("Adapt without losing evidence", [("Name a term that needs explanation for one audience.", ["పదజాలం", "వివరించాలి"], ["terminology", "should explain"]), ("Keep the source when condensing.", ["సంక్షిప్తం", "మూలాన్ని సూచించాలి"], ["shorter", "should indicate the source"])])
            ),
            _lesson(
                "Respond to a conservation concern",
                "Respond to a visitor's concern by explaining the evidence behind a conservation measure and inviting questions.",
                [("ఆందోళన", "concern", "noun"), ("ప్రక్రియ", "process", "noun"), ("పారదర్శకత", "transparency", "noun"), ("సందేహం", "question; doubt", "noun"), ("వివరణ ఇవ్వడం", "to explain", "verb")],
                ("cause, evidence and invitation", "మీ సందేహం అర్థమైంది; ఎందుకంటే ...; ప్రశ్న ఉంటే ...", "Acknowledge the concern first, explain the reason with because, and invite a follow-up question. Attribute technical claims to the responsible team or report."),
                [("మీ ఆందోళన అర్థమైంది; ఈ కొలత నివేదిక ఆధారంగా తీసుకున్నారు.", "I understand your concern; this measure was taken based on the report."), ("ప్రక్రియను బహిరంగంగా వివరించడం పారదర్శకతకు తోడ్పడుతుంది.", "Explaining the process openly supports transparency."), ("ఇంకా సందేహం ఉంటే, సంరక్షణ బృందాన్ని అడగండి.", "If you still have a question, please ask the conservation team." )],
                [("మీ ఆందోళన అర్థమైంది ఎందుకంటే ఈ కొలత నివేదిక ఆధారంగా తీసుకున్నారు.", "మీ ఆందోళన అర్థమైంది; ఈ కొలత నివేదిక ఆధారంగా తీసుకున్నారు.", "The concern is acknowledged first; the report-based explanation is a separate supporting clause." )],
                [("సందర్శకుడు", "ఈ ప్రాంతానికి ప్రవేశం ఎందుకు పరిమితం చేశారు?", "Why is access to this area limited?"), ("సంరక్షణ అధికారి", "నిర్మాణానికి ప్రమాదం తగ్గించడానికి ఈ చర్య తీసుకున్నారు.", "This measure was taken to reduce risk to the structure."), ("సందర్శకుడు", "దానికి ఏ ఆధారం ఉంది?", "What evidence supports that?"), ("సంరక్షణ అధికారి", "సంబంధిత నివేదికను చూడవచ్చు; ఇంకా ప్రశ్నలు ఉంటే అడగండి.", "You can see the relevant report; please ask if you have further questions." )],
                ("Answer a visitor carefully", [("Acknowledge the visitor's concern.", ["మీ ఆందోళన", "అర్థమైంది"], ["your concern", "I understand"]), ("Invite a source-based follow-up.", ["నివేదికను", "చూడవచ్చు"], ["the report", "can see"])])
            ),
        ]},
        {"id": "C1+-U3", "title": "వాదనను పరిమితిలో ఉంచడం", "lessons": [
            _lesson(
                "Answer an editorial challenge",
                "Defend a cautious interpretation when an editor asks whether the available evidence supports a stronger claim.",
                [("ప్రతివాదం", "counterargument", "noun"), ("బలమైన", "stronger", "adjective"), ("సమర్థించడం", "to support", "verb"), ("పునఃపరిశీలన", "review", "noun"), ("మినహాయింపు", "exception", "noun")],
                ("counterpoint with అయినా and unless", "బలమైన వాదన చేయవచ్చు; అయినా + limit", "Acknowledge the strongest reasonable counterpoint, then state what the current evidence does not establish. A stronger conclusion needs a new source or an explicit exception."),
                [("శిల్ప శైలి ఒక నిర్దిష్ట కాలాన్ని సూచించవచ్చు; అయినా అది ఒక్కటే సరిపోదు.", "The sculptural style may suggest a period; even so, it is not enough by itself."), ("కొత్త ఆధారం లభించకపోతే తేదీని ఖచ్చితంగా చెప్పలేం.", "Unless new evidence appears, we cannot state the date with certainty."), ("ఈ మినహాయింపును పునఃపరిశీలనలో చేర్చాలి.", "This exception should be included in the review." )],
                [("శైలి ఒక్కటే తేదీని నిర్ధారిస్తుంది.", "శైలి ఒక కాలాన్ని సూచించవచ్చు; తేదీని నిర్ధారించడానికి మరిన్ని ఆధారాలు అవసరం.", "A stylistic feature may suggest a period but does not by itself establish an exact date." )],
                [("సంపాదకుడు", "శిల్ప శైలిని బట్టి తేదీని ఖచ్చితంగా చెప్పలేమా?", "Can we state the date exactly from the sculptural style?"), ("రచయిత", "శైలి ఒక కాలాన్ని సూచిస్తుంది, కానీ ఒక్క ఆధారం సరిపోదు.", "The style suggests a period, but one piece of evidence is not enough."), ("సంపాదకుడు", "మరి బలమైన వాదన ఎప్పుడు సాధ్యం?", "When would a stronger claim be possible?"), ("రచయిత", "కొత్త ఆధారాలు దాన్ని స్వతంత్రంగా సమర్థించినప్పుడు.", "When new evidence independently supports it." )],
                ("State the limit of a claim", [("Say what the style may suggest.", ["శైలి", "సూచించవచ్చు"], ["style", "may suggest"]), ("Name what would be needed for certainty.", ["కొత్త ఆధారాలు", "సమర్థించినప్పుడు"], ["new evidence", "when it supports"])])
            ),
            _lesson(
                "Write a source-led synthesis",
                "Synthesize a source description, a direct observation and a remaining research question in one paragraph.",
                [("సంశ్లేషణ", "synthesis", "noun"), ("సమగ్రం", "integrated", "adjective"), ("లింక్", "link", "noun"), ("మిగిలిన", "remaining", "adjective"), ("ప్రశ్నార్థకం", "open question", "noun")],
                ("layered paragraph structure", "source claim + observed detail + అయినప్పటికీ + open question", "Order the paragraph from source to observation to limitation. Use అయినప్పటికీ to keep the interpretation connected while naming what remains unresolved."),
                [("మూల వివరణ శిల్ప పలకలను ప్రస్తావిస్తుంది.", "The source description mentions sculptured slabs."), ("స్థలంలోని పునాది అవశేషాలు ఆ వివరణకు సందర్భం ఇస్తాయి.", "The foundation remains at the site provide context for that description."), ("అయినప్పటికీ, ప్రతి పలక యొక్క స్థానం ఇంకా పరిశీలించాలి.", "Even so, the position of each slab still needs to be examined." )],
                [("మూలం పలకలను చెబుతుంది, అందువల్ల ప్రతి పలక ఎక్కడ ఉంది తెలుసు.", "మూల వివరణ పలకలను ప్రస్తావిస్తుంది; అయినప్పటికీ, ప్రతి పలక స్థానం ఇంకా పరిశీలించాలి.", "A general source statement does not settle the position of each item; preserve the unresolved question." )],
                [("పరిశోధకురాలు", "మూల వివరణ, స్థల పరిశీలనను ఎలా కలుపుతారు?", "How do you connect the source description and the site observation?"), ("రచయిత", "మూలంలో ఉన్న శిల్ప పలకలను అవశేషాలతో పోలుస్తాను.", "I compare the sculptured slabs mentioned in the source with the remains."), ("పరిశోధకురాలు", "ఏ ప్రశ్న ఇంకా తెరిచి ఉంది?", "Which question remains open?"), ("రచయిత", "ప్రతి పలక అసలు స్థానం ఏమిటో ఇంకా పరిశీలించాలి.", "We still need to examine the original position of each slab." )],
                ("Draft a layered synthesis", [("Include one source claim and one observation.", ["మూల వివరణ", "అవశేషాలు"], ["source description", "remains"]), ("Name the unresolved question.", ["స్థానం", "ఇంకా పరిశీలించాలి"], ["position", "still needs to be examined"])])
            ),
            _lesson(
                "Present a public summary with limits",
                "Give visitors a short, balanced summary that preserves a source attribution and a visible uncertainty.",
                [("ప్రజా సారాంశం", "public summary", "noun"), ("ఆపాదిత", "attributed", "adjective"), ("నిర్ధారితం", "established", "adjective"), ("సూచన", "indication", "noun"), ("వినయంగా", "with modesty", "adverb")],
                ("qualified closing with మేరకు", "అందుబాటులో ఉన్న ఆధారాల మేరకు ...", "Use మేరకు to bound the conclusion by the evidence available. Attribute the source, say what is established and leave open what is not; concise public writing still needs those distinctions."),
                [("అందుబాటులో ఉన్న ఆధారాల మేరకు, ఈ స్థలం బౌద్ధ సంప్రదాయంతో సంబంధం కలిగి ఉంది.", "As far as the available evidence indicates, this site is associated with Buddhist tradition."), ("మూల వివరణ శిల్పాల అంశాలను పేర్కొంటుంది.", "The source description names the subjects of the sculptures."), ("కొన్ని వివరాల తేదీ ఇంకా నిర్ధారితం కాలేదు.", "The date of some details has not yet been established." )],
                [("అన్ని వివరాలు నిర్ధారితం.", "కొన్ని వివరాల తేదీ ఇంకా నిర్ధారితం కాలేదు.", "State which details remain unconfirmed instead of claiming that all details are settled." )],
                [("వివరణకర్త", "సందర్శకులకు ఏ మూడు విషయాలు చెప్పాలి?", "What three things should we tell visitors?"), ("పరిశోధకుడు", "మూలం ఏమి చెబుతుంది, స్థలంలో ఏమి కనిపిస్తుంది, ఏది ఇంకా తెలియదు.", "What the source says, what is visible at the site and what is still unknown."), ("వివరణకర్త", "ఈ పరిమితిని చిన్న వాక్యంలో చెప్పవచ్చా?", "Can this limitation be stated in one short sentence?"), ("పరిశోధకుడు", "అవును, అందుబాటులో ఉన్న ఆధారాల మేరకు అని మొదలుపెట్టండి.", "Yes; begin with 'as far as the available evidence indicates'." )],
                ("Write a public-facing summary", [("Bound the conclusion by the evidence.", ["ఆధారాల మేరకు"], ["as far as the evidence indicates"]), ("State one detail that remains uncertain.", ["తేదీ", "నిర్ధారితం కాలేదు"], ["date", "has not been established"])])
            ),
        ]},
    ],
    "test": [
        ("translation", "The source description states that the diameter is about fifty metres.", "మూల వివరణ వ్యాసం సుమారు యాభై మీటర్లు అని పేర్కొంటుంది."),
        ("translation", "The foundation remains are visible, whereas the upper form is hypothetical.", "పునాది అవశేషాలు కనిపిస్తున్నాయి, కాగా పైభాగపు రూపం ఊహాత్మకం."),
        ("short_answer", "Which word preserves an approximate source measurement?", "సుమారు"),
        ("short_answer", "Name the three evidence layers.", "direct observation, attributed source detail, inference"),
        ("translation", "According to the description, this sculpture contains a Jataka scene.", "వివరణ ప్రకారం, ఈ శిల్పంలో జాతక కథా దృశ్యం ఉంది."),
        ("short_answer", "Which phrase limits a conclusion to the evidence available?", "ఆధారాల మేరకు / అందుబాటులో ఉన్న ఆధారాల మేరకు"),
        ("translation", "The source names the subject but does not establish its date.", "మూలం అంశాన్ని పేర్కొంటుంది, కానీ తేదీని నిర్ధారించదు."),
        ("short_answer", "Should an inferred purpose be stated as certain without separate evidence?", "No; state it as a possibility or leave it unresolved."),
        ("translation", "The exact purpose remains uncertain because no separate evidence is cited.", "ప్రత్యేక ఆధారం చూపించనందున, ఖచ్చితమైన ఉద్దేశం ఇంకా అనిశ్చితంగానే ఉంది."),
        ("argument_construction", "Write three sentences: observation, attributed interpretation, and an open question.", "An acceptable answer separates what is visible, what the source says, and what remains unverified."),
    ],
    "extra": HALF_EXTRAS["C1+"],
}


# Existing C1/C2 JSON also carried a repeated phase-3 gloss template. These
# source specs replace the affected original lessons (not just the new third
# lessons), so the source, examples, romanisation, review items and test remain
# reproducible together.
BASE_REWRITES = {
    "C1": [
        ("te-c1-u1", "te-c1-l1", _lesson(
            "Attribute a finding with ప్రకారం and తెలుస్తోంది",
            "Report a measured result while distinguishing what a report states from what the writer infers.",
            [("నివేదిక", "report", "noun"), ("ప్రకారం", "according to", "postposition"), ("అమలు", "implementation", "noun"), ("మెరుగుపడడం", "to improve", "verb"), ("స్పందన సమయం", "response time", "noun phrase"), ("పరిశీలన", "review", "noun"), ("తగ్గుదల", "decrease", "noun"), ("నమోదు", "record", "noun")],
            ("evidential stance and quotative అని", "source + ప్రకారం; proposition + అని + తెలుస్తోంది", "Place ప్రకారం after the named source. Use అని to package the proposition and తెలుస్తోంది to mark an inference from evidence, rather than presenting a qualified finding as certainty."),
            [("సర్వే నివేదిక ప్రకారం, స్పందన సమయం తగ్గిందని తెలుస్తోంది.", "According to the survey report, response time appears to have decreased."), ("మూడు జిల్లాల్లో మాత్రమే మార్పు నమోదైందని నివేదిక చెబుతోంది.", "The report says a change was recorded in only three districts."), ("ఈ సమాచారం మార్పును సూచిస్తుంది; దాని కారణాన్ని మాత్రం నిర్ధారించదు.", "This information indicates a change, but does not establish its cause." )],
            [("సర్వే నివేదిక ప్రకారం స్పందన సమయం ఖచ్చితంగా తగ్గింది.", "సర్వే నివేదిక ప్రకారం, స్పందన సమయం తగ్గిందని తెలుస్తోంది.", "Do not strengthen a reported indication into certainty; retain the source and the qualified ending తెలుస్తోంది." )],
            [("పరిశోధకుడు", "నివేదిక ఫలితాన్ని ఎంత నిశ్చయంగా చెబుతోంది?", "How confidently does the report state the finding?"), ("సంపాదకురాలు", "సమయం తగ్గిందని చెబుతోంది, కానీ కారణాన్ని నిర్ధారించదు.", "It says the time decreased, but it does not establish the cause."), ("పరిశోధకుడు", "అయితే శీర్షికలో ఎలా రాయాలి?", "Then how should we write it in the heading?"), ("సంపాదకురాలు", "నివేదిక ప్రకారం తగ్గుదల కనిపించిందని పరిమితితో రాయండి.", "Write with the qualification that a decrease appears according to the report." )],
            ("Preserve evidential scope", [("Attribute the result to its source.", ["సర్వే నివేదిక ప్రకారం", "స్పందన సమయం"], ["according to the survey report", "response time"]), ("Avoid claiming a cause the report did not establish.", ["కారణాన్ని", "నిర్ధారించదు"], ["the cause", "does not establish"])])
        )),
        ("te-c1-u1", "te-c1-l2", _lesson(
            "Concede a limitation without abandoning a proposal",
            "Acknowledge a pilot's limitation and retain a recommendation with a condition for responsible expansion.",
            [("పరిమితి", "limitation", "noun"), ("అయినప్పటికీ", "although; even so", "conjunction"), ("ప్రతిపాదన", "proposal", "noun"), ("పర్యవేక్షణ", "monitoring", "noun"), ("విస్తరణ", "expansion", "noun"), ("పైలట్", "pilot", "noun"), ("అదనపు సిబ్బంది", "additional staff", "noun phrase"), ("గడువు", "deadline", "noun")],
            ("concession with అయినప్పటికీ", "concession + అయినప్పటికీ, recommendation + condition", "Use అయినప్పటికీ to grant a limitation before stating what can still be done. Keep the condition for a larger rollout explicit; a concession is not a reason to hide risk."),
            [("పర్యవేక్షణ పరిమితంగా ఉన్నప్పటికీ, పైలట్‌ను కొనసాగించవచ్చు.", "Although monitoring is limited, the pilot can continue."), ("అయితే, విస్తరణకు ముందు అదనపు సిబ్బందిని కేటాయించాలి.", "However, additional staff should be assigned before expansion."), ("ఈ పరిమితి తొలగిన తర్వాతే తదుపరి దశను ప్రారంభిద్దాం.", "Let us begin the next stage only after this limitation is addressed." )],
            [("పర్యవేక్షణ పరిమితంగా అయినప్పటికీ, పైలట్ కొనసాగించాలి.", "పర్యవేక్షణ పరిమితంగా ఉన్నప్పటికీ, పైలట్‌ను కొనసాగించవచ్చు.", "Use the concessive form ఉన్నప్పటికీ and mark the pilot as the object with -ను." )],
            [("సమీక్షకుడు", "పైలట్‌లో సిబ్బంది తక్కువగా ఉన్నారు.", "There are too few staff in the pilot."), ("విధాన నిపుణురాలు", "అది నిజమే; అయినప్పటికీ, ప్రస్తుత దశను పర్యవేక్షణతో కొనసాగించవచ్చు.", "That is true; even so, the current stage can continue with monitoring."), ("సమీక్షకుడు", "విస్తరణకు ముందు ఏం అవసరం?", "What is needed before expansion?"), ("విధాన నిపుణురాలు", "అదనపు సిబ్బంది, స్పష్టమైన సమీక్షా గడువు అవసరం.", "Additional staff and a clear review deadline are needed." )],
            ("Write a conditional recommendation", [("Acknowledge the limitation.", ["సిబ్బంది తక్కువగా", "పరిమితి"], ["too few staff", "limitation"]), ("Name two safeguards before expansion.", ["అదనపు సిబ్బంది", "సమీక్షా గడువు"], ["additional staff", "review deadline"])])
        )),
        ("te-c1-u2", "te-c1-l3", _lesson(
            "Compress a description with a participial clause",
            "Use a relative participle to describe a group or trend without losing the relationship between the action and noun.",
            [("ప్రభావం చూపడం", "to have an effect", "verb"), ("సేకరించిన", "collected", "participle"), ("నివసిస్తున్న", "living; residing", "participle"), ("మార్పు", "change", "noun"), ("విశ్లేషించడం", "to analyse", "verb"), ("గణాంకాలు", "statistics", "noun"), ("కుటుంబం", "family", "noun"), ("పేర్కొన్న", "mentioned", "participle")],
            ("relative participles before nouns", "verb stem + participle + noun", "A participle such as సేకరించిన or నివసిస్తున్న modifies the noun that follows. Keep that noun close to the participle, then place the main instruction or conclusion at the end."),
            [("గత ఏడాది సేకరించిన గణాంకాలు మూడు ప్రాంతాల్లో మార్పును చూపిస్తున్నాయి.", "Statistics collected last year show a change in three regions."), ("నది పక్కన నివసిస్తున్న కుటుంబాలపై ప్రభావాన్ని విడిగా విశ్లేషించాలి.", "The effect on families living beside the river should be analysed separately."), ("నివేదికలో పేర్కొన్న పరిమితులను సమీక్షలో చేర్చాలి.", "The limitations mentioned in the report should be included in the review." )],
            [("నివేదికలో పేర్కొన్నది పరిమితులను సమీక్షలో చేర్చాలి.", "నివేదికలో పేర్కొన్న పరిమితులను సమీక్షలో చేర్చాలి.", "Place the participial phrase directly before the noun it describes: పేర్కొన్న పరిమితులను." )],
            [("విశ్లేషకుడు", "ఏ కుటుంబాలపై ప్రభావాన్ని విడిగా చూపాలి?", "Which families' impact should be shown separately?"), ("సంపాదకురాలు", "నది పక్కన నివసిస్తున్న కుటుంబాలపై.", "The families living beside the river."), ("విశ్లేషకుడు", "ఆ వాక్యాన్ని సంక్షిప్తం చేయవచ్చా?", "Can that sentence be made more concise?"), ("సంపాదకురాలు", "అవును, కానీ నివసిస్తున్న అనే సంబంధాన్ని ఉంచండి.", "Yes, but keep the relationship marked by నివసిస్తున్న." )],
            ("Build a precise noun phrase", [("Describe which statistics are meant.", ["గత ఏడాది", "సేకరించిన గణాంకాలు"], ["last year", "statistics that were collected"]), ("Name the group affected.", ["నది పక్కన", "నివసిస్తున్న కుటుంబాలు"], ["beside the river", "families who live"])])
        )),
        ("te-c1-u2", "te-c1-l4", _lesson(
            "Separate incomplete evidence from inference",
            "Explain why a small sample limits a conclusion and identify what further evidence is needed.",
            [("అసంపూర్ణం", "incomplete", "adjective"), ("నమూనా", "sample", "noun"), ("కారణ సంబంధం", "causal relationship", "noun phrase"), ("వాయిదా", "postponement", "noun"), ("స్వతంత్ర ఆధారం", "independent evidence", "noun phrase"), ("కొలత", "measurement", "noun"), ("వర్తింపజేయడం", "to apply", "verb"), ("జాగ్రత్తగా", "cautiously", "adverb")],
            ("cause, inference and limit", "X కాబట్టి + cautious consequence; కావచ్చు", "Use కాబట్టి to state a reason, then qualify an inference with కావచ్చు or state what cannot yet be concluded. A correlation or small sample does not by itself establish a causal relationship."),
            [("నమూనా చిన్నదిగా ఉన్నందున, ఫలితాన్ని అన్ని ప్రాంతాలకు వర్తింపజేయలేం.", "Because the sample is small, we cannot apply the result to every region."), ("రెండు సూచికలు కలిసి మారడం కారణ సంబంధం కావచ్చు, కానీ అది నిరూపణ కాదు.", "Two indicators changing together may suggest a causal link, but that is not proof."), ("అదనపు కొలతలు వచ్చిన తర్వాత తీర్మానాన్ని పునఃపరిశీలిద్దాం.", "Let us revisit the conclusion after additional measurements arrive." )],
            [("నమూనా చిన్నది కాబట్టి ఫలితం తప్పు.", "నమూనా చిన్నది కాబట్టి ఫలితాన్ని జాగ్రత్తగా అర్థం చేసుకోవాలి.", "A small sample limits the strength of a conclusion; it does not prove that the result is false." )],
            [("సమీక్షకురాలు", "రెండు సూచికలు కలిసి మారాయి; అది కారణాన్ని నిరూపిస్తుందా?", "Two indicators changed together; does that prove a cause?"), ("విశ్లేషకుడు", "లేదు, అది ఒక సంభావ్య సంబంధాన్ని మాత్రమే సూచించవచ్చు.", "No, it may only indicate a possible relationship."), ("సమీక్షకురాలు", "తదుపరి దశ ఏమిటి?", "What is the next step?"), ("విశ్లేషకుడు", "స్వతంత్ర ఆధారాలు సేకరించి నమూనాను విస్తరించాలి.", "We should collect independent evidence and expand the sample." )],
            ("Qualify the conclusion", [("Name why the result cannot cover every region.", ["నమూనా చిన్నదిగా", "వర్తింపజేయలేం"], ["because the sample is small", "cannot apply"]), ("Propose the next evidence step.", ["స్వతంత్ర ఆధారాలు", "సేకరించాలి"], ["independent evidence", "should collect"])])
        )),
        ("te-c1-u3", "te-c1-l5", _lesson(
            "Propose an alternative without dismissing a colleague",
            "Acknowledge the purpose of a colleague's suggestion, then propose a staged alternative in a professional register.",
            [("సూచన", "suggestion", "noun"), ("ప్రత్యామ్నాయం", "alternative", "noun"), ("ప్రతిపాదించడం", "to propose", "verb"), ("పునఃపరిశీలన", "review", "noun"), ("సాధ్యమైతే", "if possible", "phrase"), ("మండలం", "mandal", "noun"), ("లక్ష్యం", "goal", "noun"), ("సమావేశం", "meeting", "noun")],
            ("mitigation and a respectful proposal", "మీ సూచనను అంగీకరిస్తూనే, ... ప్రతిపాదిస్తున్నాను", "Use the object marker -ను in సూచనను. Acknowledge the other person's goal before naming the alternative; a respectful frame softens disagreement without hiding the substance."),
            [("మీ సూచనలోని ఉద్దేశాన్ని అంగీకరిస్తూనే, అమలు క్రమాన్ని మార్చాలని ప్రతిపాదిస్తున్నాను.", "While accepting the purpose of your suggestion, I propose changing the order of implementation."), ("ప్రత్యామ్నాయంగా, ముందుగా రెండు మండలాల్లో ప్రయోగాత్మకంగా అమలు చేయవచ్చు.", "Alternatively, it can first be implemented as a pilot in two mandals."), ("ఈ మార్పును సమీక్షా సమావేశంలో మళ్లీ పరిశీలించవచ్చా?", "Could we review this change again at the review meeting?" )],
            [("మీ సూచన గౌరవిస్తూ, వేరే క్రమం ప్రతిపాదిస్తున్నాను.", "మీ సూచనను గౌరవిస్తూ, వేరే క్రమాన్ని ప్రతిపాదిస్తున్నాను.", "Mark సూచన and క్రమం as objects with -ను in this formal proposal." )],
            [("సహోద్యోగి", "మొదట అన్ని ప్రాంతాల్లో ప్రారంభిద్దాం.", "Let us begin in all regions first."), ("మధ్యవర్తి", "మీ సూచనలోని లక్ష్యాన్ని అర్థం చేసుకున్నాను.", "I understand the goal in your suggestion."), ("సహోద్యోగి", "అయితే మీరు ఏ మార్పు కోరుతున్నారు?", "Then what change are you asking for?"), ("మధ్యవర్తి", "సాధ్యమైతే, రెండు మండలాల్లో ప్రయోగాత్మక దశతో మొదలుపెడదాం.", "If possible, let us begin with a pilot in two mandals." )],
            ("Draft a diplomatic alternative", [("Acknowledge the colleague's goal.", ["మీ సూచనలోని లక్ష్యం", "అర్థం చేసుకున్నాను"], ["the goal in your suggestion", "I understand"]), ("Propose a staged first step.", ["రెండు మండలాల్లో", "ప్రయోగాత్మక దశ"], ["in two mandals", "pilot stage"])])
        )),
        ("te-c1-u3", "te-c1-l6", _lesson(
            "Synthesize two sources without flattening them",
            "Combine two studies while preserving what each measured and limiting the conclusion to their shared evidence.",
            [("అధ్యయనం", "study", "noun"), ("సమన్వయించడం", "to synthesise", "verb"), ("సందర్భం", "context", "noun"), ("సూచిక", "indicator", "noun"), ("సంక్షిప్తంగా", "briefly", "adverb"), ("మూలం", "source", "noun"), ("పోల్చడం", "to compare", "verb"), ("విభిన్నం", "different", "adjective")],
            ("synthesis with condition and consequence", "రెండు మూలాలను సమన్వయిస్తే, ...; అయితే ...", "State what each source contributes before giving a shared conclusion. Use అయితే to mark a limitation; synthesis should connect findings without pretending their methods or populations were identical."),
            [("మొదటి అధ్యయనం ఖర్చును కొలిచింది; రెండోది వినియోగదారుల అనుభవాన్ని నమోదు చేసింది.", "The first study measured cost; the second recorded user experience."), ("రెండింటిని సమన్వయిస్తే, స్థానిక సందర్భం ఫలితంపై ప్రభావం చూపిందని తెలుస్తోంది.", "Synthesising both suggests that local context affected the result."), ("అయితే, ఒకే సూచికతో మొత్తం విజయాన్ని నిర్ణయించలేం.", "However, overall success cannot be determined from a single indicator." )],
            [("రెండు అధ్యయనాలు ఒకే విధంగా కొలిచాయి అని చెప్పాలి.", "రెండు అధ్యయనాలు వేర్వేరు అంశాలను కొలిచాయి; వాటి ఫలితాలను పరిమితితో సమన్వయించాలి.", "Do not claim identical methods when the studies measured different things; preserve that distinction in the synthesis." )],
            [("పరిశోధకురాలు", "రెండు అధ్యయనాల ఫలితాలను ఎలా కలిపారు?", "How did you combine the findings of the two studies?"), ("రచయిత", "ఒకటి ఖర్చును, మరొకటి వినియోగదారుల అనుభవాన్ని కొలిచింది.", "One measured cost, the other user experience."), ("పరిశోధకురాలు", "అయితే ఒకే విజయ సూచిక ఉందని చెప్పవచ్చా?", "Then can we say there is one success indicator?"), ("రచయిత", "కాదు; సందర్భాన్ని చూపిస్తూ పరిమితితో మాత్రమే తీర్మానించాలి.", "No; we should conclude only with a qualification that shows the context." )],
            ("Write a source-led synthesis", [("Name what each study measured.", ["మొదటి అధ్యయనం", "రెండోది"], ["the first study", "the second"]), ("Add the limit on a shared conclusion.", ["అయితే", "ఒకే సూచికతో"], ["however", "with one indicator"])])
        )),
    ],
    "C2": [
        ("te-c2-u1", "te-c2-l1", _lesson(
            "Put focus on the part that changes the outcome",
            "Use focus and contrast to distinguish announcing a policy from carrying it out.",
            [("నిర్ణయం", "decision", "noun"), ("మాత్రమే", "only; alone", "focus particle"), ("అమలు", "implementation", "noun"), ("కీలకం", "crucial", "adjective"), ("బాధ్యత", "responsibility", "noun"), ("ప్రకటన", "announcement", "noun"), ("పంపిణీ", "allocation", "noun"), ("ఫలితం", "outcome", "noun")],
            ("focus with -ఏ and మాత్రమే", "X మాత్రమే కాదు; Y-ఏ కీలకం", "మాత్రమే limits the first item; the emphatic suffix -ఏ highlights the contrastive item. Keep the contrast explicit so a sentence cannot be read as saying that the decision itself was ineffective."),
            [("ఈ నిర్ణయం మాత్రమే సమస్యను పరిష్కరించలేదు; దాని అమలే కీలకమైంది.", "The decision alone did not solve the problem; its implementation was crucial."), ("ప్రకటన మాత్రమే కాదు, బాధ్యతల పంపిణీ కూడా స్పష్టంగా ఉండాలి.", "Not only the announcement; the allocation of responsibilities must also be clear."), ("అమలే ఫలితాన్ని మార్చిందని ఆధారాలు సూచిస్తున్నాయి.", "Evidence suggests that implementation is what changed the outcome." )],
            [("ఈ నిర్ణయమే సమస్యను పరిష్కరించలేదు; దాని అమలే కీలకం.", "ఈ నిర్ణయం మాత్రమే సమస్యను పరిష్కరించలేదు; దాని అమలే కీలకమైంది.", "Use మాత్రమే to express 'the decision alone'; -ఏ on అమలు marks the contrasting focus." )],
            [("సంపాదకుడు", "ఈ వాక్యంలో మార్పు తెచ్చింది ఏది?", "What brought about the change in this sentence?"), ("విశ్లేషకురాలు", "నిర్ణయం ప్రకటించడం మాత్రమే కాదు, దాని అమలు.", "Not just announcing the decision, but its implementation."), ("సంపాదకుడు", "అయితే శీర్షికలో దేనిపై దృష్టి పెట్టాలి?", "Then what should the heading focus on?"), ("విశ్లేషకురాలు", "అమలుపై; అదే ఫలితాన్ని మార్చింది.", "On implementation; that is what changed the outcome." )],
            ("Clarify the focus", [("State what the decision alone did not do.", ["నిర్ణయం మాత్రమే", "పరిష్కరించలేదు"], ["the decision alone", "did not solve"]), ("Highlight the crucial factor.", ["అమలే", "కీలకమైంది"], ["implementation is what", "was crucial"])])
        )),
        ("te-c2-u1", "te-c2-l2", _lesson(
            "Interpret a reserved response cautiously",
            "Discuss an implied meaning without treating silence or a short reply as proof of a person's intention.",
            [("మౌనం", "silence", "noun"), ("సమ్మతి", "agreement", "noun"), ("దూరం పాటించడం", "to keep distance", "phrase"), ("సూచించడం", "to indicate", "verb"), ("సందర్భం", "context", "noun"), ("అసమ్మతి", "disagreement", "noun"), ("సమాధానం", "response", "noun"), ("అర్థం చేసుకోవడం", "to interpret", "verb")],
            ("inference with కావచ్చు and cannot conclude", "X సూచించవచ్చు; అయితే + intention cannot be confirmed", "Use సూచించవచ్చు or కావచ్చు for a plausible reading. Follow it with a limit when a speaker's intention is not explicit; consider the surrounding exchange before inferring agreement or criticism."),
            [("ఆయన మౌనం సమ్మతిని కాక, జాగ్రత్తగా దూరం పాటించడాన్ని సూచించి ఉండవచ్చు.", "His silence may have indicated not agreement, but careful distance."), ("అయితే, సందర్భం తెలియకుండా ఉద్దేశాన్ని ఖచ్చితంగా నిర్ణయించలేం.", "However, without context we cannot determine the intention with certainty."), ("తదుపరి ప్రశ్న అడగడం అర్థాన్ని స్పష్టం చేయవచ్చు.", "Asking a follow-up question may clarify the meaning." )],
            [("ఆయన మౌనం తప్పకుండా అసమ్మతిని నిరూపిస్తుంది.", "ఆయన మౌనం అసమ్మతిని సూచించి ఉండవచ్చు; అయితే మరింత సందర్భం అవసరం.", "Silence may suggest disagreement, but it does not prove it; qualify the inference and seek context." )],
            [("మధ్యవర్తి", "ఆ సమాధానం సమ్మతిగా వినిపించిందా?", "Did that response sound like agreement?"), ("సమీక్షకుడు", "అలా అనిపించవచ్చు, కానీ అతను ఉద్దేశాన్ని స్పష్టంగా చెప్పలేదు.", "It might seem so, but he did not state his intention clearly."), ("మధ్యవర్తి", "తదుపరి సమావేశంలో ఎలా అడగాలి?", "How should we ask in the next meeting?"), ("సమీక్షకుడు", "మీరు ఈ ప్రతిపాదనకు అంగీకరిస్తున్నారా అని నేరుగా, గౌరవంగా అడగండి.", "Ask directly and respectfully whether he agrees with the proposal." )],
            ("Separate implication from proof", [("Offer a cautious interpretation.", ["సూచించి ఉండవచ్చు"], ["may have indicated"]), ("Name what is still unknown.", ["ఉద్దేశాన్ని", "స్పష్టంగా చెప్పలేదు"], ["the intention", "did not state clearly"])])
        )),
        ("te-c2-u2", "te-c2-l3", _lesson(
            "Balance speed with accountability",
            "Make a public argument for timely action while retaining review, transparency and responsibility.",
            [("వేగం", "speed", "noun"), ("జవాబుదారీతనం", "accountability", "noun"), ("పారదర్శకత", "transparency", "noun"), ("పురోగతి", "progress", "noun"), ("పర్యవేక్షణ", "oversight", "noun"), ("కాలపరిమితి", "deadline", "noun"), ("కారణం", "reason", "noun"), ("నమోదు చేయడం", "to record", "verb")],
            ("contrast with కానీ and emphatic -ఏ", "X అవసరమే; కానీ Y లేకుండా + claim", "The emphatic అవసరమే grants that speed matters; కానీ introduces the limit. State the accountability process as a condition of progress, not as an optional afterthought."),
            [("వేగం అవసరమే; కానీ జవాబుదారీతనం లేని వేగాన్ని పురోగతిగా పరిగణించలేం.", "Speed is necessary, but speed without accountability cannot be considered progress."), ("కాలపరిమితి ఉన్నప్పటికీ, నిర్ణయానికి కారణాలను నమోదు చేయాలి.", "Even with a deadline, the reasons for the decision should be recorded."), ("ఫలితంతో పాటు ప్రక్రియను ప్రకటించడం విశ్వాసాన్ని పెంచుతుంది.", "Announcing the process along with the result increases trust." )],
            [("వేగం అవసరం; అందువల్ల జవాబుదారీతనం అవసరం లేదు.", "వేగం అవసరమే; కానీ జవాబుదారీతనం కూడా అవసరం.", "The consequence does not cancel accountability; use కానీ to present the necessary balance." )],
            [("నిర్వాహకుడు", "ప్రాజెక్టును వేగంగా పూర్తి చేయాలా?", "Should we complete the project quickly?"), ("సమీక్షకురాలు", "వేగం అవసరమే, కానీ నిర్ణయాలకు కారణాలు నమోదు చేయాలి.", "Speed is necessary, but the reasons for decisions must be recorded."), ("నిర్వాహకుడు", "అది పురోగతిని ఆలస్యం చేయదా?", "Will that not delay progress?"), ("సమీక్షకురాలు", "స్పష్టమైన ప్రక్రియ తర్వాతి సవరణలను తగ్గించవచ్చు.", "A clear process may reduce later corrections." )],
            ("Draft a balanced public statement", [("Acknowledge the need for speed.", ["వేగం", "అవసరమే"], ["speed", "is necessary"]), ("Add one accountability safeguard.", ["కారణాలను", "నమోదు చేయాలి"], ["the reasons", "should record"])])
        )),
        ("te-c2-u2", "te-c2-l4", _lesson(
            "Adapt a written statement for a public meeting",
            "Shorten a formal written statement for oral delivery while preserving its qualification and key exception.",
            [("లిఖిత రూపం", "written form", "noun phrase"), ("మౌఖిక వివరణ", "oral explanation", "noun phrase"), ("శ్రోత", "listener", "noun"), ("సంక్షిప్తీకరించడం", "to condense", "verb"), ("మినహాయింపు", "exception", "noun"), ("లిఖిత ప్రకటన", "written notice", "noun phrase"), ("సరళీకరించడం", "to simplify", "verb"), ("ప్రామాణికం", "formal; standard", "adjective")],
            ("register adaptation with అయితే", "formal detail; oral summary + అయితే + exception", "A spoken summary may be shorter and more direct than a written notice. Keep a qualifier or exception that changes the meaning; do not confuse accessible wording with removing the condition."),
            [("లిఖిత ప్రకటనలో పూర్తి వివరాలు ఉండాలి; మౌఖిక వివరణలో ప్రధాన దశలను సంక్షిప్తంగా చెప్పవచ్చు.", "A written notice should contain full details; an oral explanation can summarise the main steps."), ("శ్రోతలకు తెలియని సాంకేతిక పదాన్ని ముందుగా వివరించాలి.", "A technical term unfamiliar to listeners should be explained first."), ("వాక్యాన్ని సరళీకరించినా, మినహాయింపును తొలగించకూడదు.", "Even when simplifying the sentence, the exception should not be removed." )],
            [("వాక్యం చిన్నదిగా చేయడం కోసం మినహాయింపును తొలగించండి.", "వాక్యాన్ని సంక్షిప్తం చేసినా, అర్థాన్ని మార్చే మినహాయింపును ఉంచండి.", "Condense the sentence without deleting an exception that changes its meaning." )],
            [("వక్త", "ఈ వాక్యాన్ని సమావేశంలో చదవడం కష్టంగా ఉంది.", "This sentence is difficult to read aloud at the meeting."), ("సంపాదకురాలు", "ప్రధాన చర్యను ముందుకు తెచ్చి, మినహాయింపును తరువాత స్పష్టంగా చెబుదాం.", "Let us put the main action first and state the exception clearly afterward."), ("వక్త", "అప్పుడు లిఖిత అర్థం మారుతుందా?", "Will the written meaning change then?"), ("సంపాదకురాలు", "లేదు, అవసరమైన పరిమితిని అలాగే ఉంచితే మారదు.", "No, not if we preserve the necessary limitation." )],
            ("Adapt without losing the qualification", [("Name the intended audience.", ["సమావేశంలో", "శ్రోతలకు"], ["at the meeting", "for listeners"]), ("Keep the exception in the oral version.", ["మినహాయింపును", "ఉంచండి"], ["the exception", "keep"])])
        )),
        ("te-c2-u3", "te-c2-l5", _lesson(
            "Clarify a disagreement without dismissing a colleague",
            "State that you are clarifying a claim's scope rather than rejecting the colleague's view.",
            [("అభిప్రాయం", "view; opinion", "noun"), ("పరిధి", "scope", "noun"), ("స్పష్టీకరణ", "clarification", "noun"), ("ఖండించడం", "to refute; dismiss", "verb"), ("నిర్వచించడం", "to define", "verb"), ("అంగీకారం", "agreement", "noun"), ("మినహాయింపు", "exception", "noun"), ("వర్తించడం", "to apply", "verb")],
            ("contrastive clarification and respectful disagreement", "X ను ఖండించడం కాదు; Y ను స్పష్టం చేయడం", "Use కాదు to distinguish the purpose of the response, then name the clarification you are making. Mark the view as the object with -ను and separate the claim's scope from the person who expressed it."),
            [("మీ అభిప్రాయాన్ని ఖండించడం కాదు; దాని పరిధిని స్పష్టీకరించాలనుకుంటున్నాను.", "I am not dismissing your view; I want to clarify its scope."), ("ఈ నిర్ణయం ఏ సందర్భాలకు వర్తిస్తుందో ముందుగా నిర్వచిద్దాం.", "Let us first define the situations to which this decision applies."), ("అంగీకరించని అంశాన్ని గౌరవంగా, స్పష్టంగా చెప్పవచ్చు.", "A point of disagreement can be stated respectfully and clearly." )],
            [("మీ అభిప్రాయం ఖండించడం కాదు; దాని పరిధిని స్పష్టం చేయాలి.", "మీ అభిప్రాయాన్ని ఖండించడం కాదు; దాని పరిధిని స్పష్టీకరించాలనుకుంటున్నాను.", "Mark అభిప్రాయం as the object with -ని, then state whose intention the clarification expresses." )],
            [("సంపాదకుడు", "మీరు నా అభిప్రాయాన్ని తిరస్కరిస్తున్నారా?", "Are you rejecting my view?"), ("మధ్యవర్తి", "లేదు, దాన్ని ఖండించడం కాదు; వర్తించే పరిధిని స్పష్టం చేస్తున్నాను.", "No, I am not dismissing it; I am clarifying the scope in which it applies."), ("సంపాదకుడు", "అయితే ఏ సందర్భం బయట ఉంటుంది?", "Then which situation is outside it?"), ("మధ్యవర్తి", "ఆ మినహాయింపును వేరుగా నిర్వచిద్దాం.", "Let us define that exception separately." )],
            ("Clarify the scope respectfully", [("State what you are not doing.", ["అభిప్రాయాన్ని", "ఖండించడం కాదు"], ["the view", "not dismissing"]), ("Name what needs definition.", ["ఏ సందర్భాలకు", "వర్తిస్తుందో"], ["to which situations", "applies"])])
        )),
        ("te-c2-u3", "te-c2-l6", _lesson(
            "Calibrate certainty in expert mediation",
            "Present a plausible explanation, identify its evidence limit and explain what new finding would change the assessment.",
            [("లభ్యమైన ఆధారాలు", "available evidence", "noun phrase"), ("సంభావ్య", "plausible", "adjective"), ("తుది నిర్ధారణ", "final conclusion", "noun phrase"), ("అనిశ్చితి", "uncertainty", "noun"), ("సవరించడం", "to revise", "verb"), ("అంచనా", "assessment", "noun"), ("నిర్ధారించడం", "to establish", "verb"), ("సమాచారం", "information", "noun")],
            ("qualified conclusion with మేరకు", "ఆధారాల మేరకు + plausible claim; అయితే + limit", "Use మేరకు to bound a conclusion by the evidence available. Label a claim as సంభావ్య when it is plausible but not settled, and state what could revise the assessment."),
            [("లభ్యమైన ఆధారాల మేరకు ఇది సంభావ్య వివరణ; తుది నిర్ధారణ కాదు.", "As far as the available evidence shows, this is a plausible explanation, not a final conclusion."), ("కొత్త సమాచారం లభిస్తే ఈ అంచనాను సవరించాలి.", "If new information becomes available, this assessment should be revised."), ("అనిశ్చితిని స్పష్టంగా గుర్తించడం నివేదిక విశ్వసనీయతను పెంచుతుంది.", "Clearly identifying uncertainty increases a report's credibility." )],
            [("ఈ వివరణ ఖచ్చితంగా నిజమని ఆధారాలు చెబుతున్నాయి.", "ఈ వివరణ లభ్యమైన ఆధారాలకు అనుగుణంగా కనిపిస్తోంది; తుది నిర్ధారణకు ఇంకా ఆధారం కావాలి.", "Do not present a plausible interpretation as proven; state the supporting evidence and what remains unresolved." )],
            [("నిపుణురాలు", "ఈ వివరణను ఎంత నిశ్చయంగా చెప్పవచ్చు?", "How confidently can we state this explanation?"), ("మధ్యవర్తి", "లభ్యమైన ఆధారాల మేరకు సంభావ్యంగా చెప్పవచ్చు.", "We can describe it as plausible given the available evidence."), ("నిపుణురాలు", "ఏ సమాచారం దాన్ని మార్చవచ్చు?", "What information could change it?"), ("మధ్యవర్తి", "కొత్త కొలతలు వస్తే అంచనాను సవరించాలి.", "If new measurements arrive, the assessment should be revised." )],
            ("Write a calibrated conclusion", [("Bound the claim by available evidence.", ["లభ్యమైన ఆధారాల మేరకు", "సంభావ్య"], ["as far as the available evidence", "plausible"]), ("State what could change the assessment.", ["కొత్త సమాచారం", "సవరించాలి"], ["new information", "should revise"])])
        )),
    ],
}

LEVEL_GOALS = {
    "C1": [
        "Attribute findings and control the certainty of a reported claim",
        "Build concessive, participial and evidence-based arguments in Telugu",
        "Synthesize sources and mediate a proposal without losing scope or register",
    ],
    "C2": [
        "Use focus, implication and contrast to manage subtle differences in meaning",
        "Adapt formal Telugu for public speech without erasing conditions or exceptions",
        "Mediate disagreement and calibrate conclusions against the evidence available",
    ],
}

LEVEL_TESTS = {
    "C1": [
        ("translation", "According to the survey report, response time appears to have decreased.", "సర్వే నివేదిక ప్రకారం, స్పందన సమయం తగ్గిందని తెలుస్తోంది."),
        ("short_answer", "Which phrase attributes a finding to its source?", "నివేదిక ప్రకారం / మూలం ప్రకారం"),
        ("translation", "Although monitoring is limited, the pilot can continue.", "పర్యవేక్షణ పరిమితంగా ఉన్నప్పటికీ, పైలట్‌ను కొనసాగించవచ్చు."),
        ("short_answer", "Which connector marks the concession in that sentence?", "అయినప్పటికీ"),
        ("translation", "The families living beside the river should be analysed separately.", "నది పక్కన నివసిస్తున్న కుటుంబాలపై ప్రభావాన్ని విడిగా విశ్లేషించాలి."),
        ("short_answer", "What does a small sample limit: truth or the strength of a conclusion?", "the strength of a conclusion / తీర్మాన బలం"),
        ("translation", "If possible, let us begin with a pilot in two mandals.", "సాధ్యమైతే, రెండు మండలాల్లో ప్రయోగాత్మక దశతో మొదలుపెడదాం."),
        ("short_answer", "Name the connector that introduces a result or consequence.", "అందువల్ల / కాబట్టి"),
        ("argument_construction", "Give one source-attributed finding and one limitation on its interpretation.", "An acceptable answer attributes the finding, preserves its qualifier, and states what the source does not establish."),
        ("argument_construction", "Synthesize two different measures without claiming that they used the same method.", "An acceptable answer names what each study measured, then gives a qualified shared conclusion."),
    ],
    "C2": [
        ("translation", "The decision alone did not solve the problem; its implementation was crucial.", "ఈ నిర్ణయం మాత్రమే సమస్యను పరిష్కరించలేదు; దాని అమలే కీలకమైంది."),
        ("short_answer", "Which word means 'only/alone' in the focus contrast?", "మాత్రమే"),
        ("short_answer", "Does silence by itself prove agreement?", "No; context and follow-up are needed."),
        ("translation", "Speed is necessary, but speed without accountability cannot be considered progress.", "వేగం అవసరమే; కానీ జవాబుదారీతనం లేని వేగాన్ని పురోగతిగా పరిగణించలేం."),
        ("short_answer", "Name one detail a public oral summary must preserve.", "a condition or exception / షరతు లేదా మినహాయింపు"),
        ("translation", "I am not dismissing your view; I want to clarify its scope.", "మీ అభిప్రాయాన్ని ఖండించడం కాదు; దాని పరిధిని స్పష్టీకరించాలనుకుంటున్నాను."),
        ("translation", "This is a plausible explanation, not a final conclusion.", "ఇది సంభావ్య వివరణ; తుది నిర్ధారణ కాదు."),
        ("short_answer", "Which suffix highlights అమలు as the focus?", "-ఏ"),
        ("argument_construction", "Adapt a formal written condition for a public meeting without deleting the exception.", "An acceptable answer is concise, audience-aware, and retains the exception that changes the meaning."),
        ("argument_construction", "State what evidence could change a plausible expert assessment.", "An acceptable answer names new evidence or measurements and says the conclusion should be revised."),
    ],
}

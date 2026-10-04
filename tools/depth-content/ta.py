# -*- coding: utf-8 -*-
"""Tamil PHASE 1 depth — extras, third lessons, half-step rungs.

Written with the DSL in `tools/depth_kit.py`; rendered by
`tools/author-depth.py --lang ta`.

House style follows the shipped Tamil course: Tamil script in `t`, the course's
own romanisation in `r` — lowercase for vocabulary, sentence case for examples
and dialogue, with the marks the course already teaches (ā ī ū ē ō, retroflex
ṇ ḷ ṟ, ṅ ñ: `vaṇakkam`, `nīṅkaḷ eppaḍi irukkiṟīrkaḷ?`, `naṉṟi`) — and English
in `en`, because the course teaches in English. Unit ids keep the shipped
scheme: A1–C2 use `ta-a1-u1` … `ta-c2-u3` with sequential lesson ids
(`ta-a1-l1` … `ta-a1-l6`), so a third lesson in a unit takes the next free
number in that rung's sequence (`ta-a1-l7`, `ta-a1-l8`, `ta-a1-l9` — the same
arrangement Punjabi and Gujarati use); the half-step rungs use `<RUNG>-U1`
(`A1+-U1` … `C1+-U1`).

`tools/normalise-romanisation.py` deliberately skips this course: Tamil's
romanisation already carries marks, and that column is the one the learner
reads. The scheme is therefore hand-consistent — no ASCII folding of ā/ī/ū/ṇ/ḷ,
and no diacritics smuggled into the plain-English columns.

Register note: Tamil is head-final and agglutinative, and the course teaches the
written register with its own politeness ladder. A1 uses நீங்கள் with the
plural verb (வாருங்கள்), A2 adds the familiar நீ and the -க்கு/-இல் case
suffixes, B1 moves into relative participles (நான் செய்த வேலை) and purpose
clauses (-க்காக), B2 into echo/reported speech (என்று கூறப்படுகிறது) and
conditionals (-ஆல் / என்றால்), C1–C2 into the impersonal scholarly register
(குறிப்பிடப்படுகிறது, எனக் கருதப்படுகிறது) and translation strategy. Spoken
Tamil differs from the written forms taught here; the course says so in A1 and
keeps the written form consistent across all rungs.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # tools/ on the path
from depth_kit import D, EXTRA, G, L, T, V, WS, X   # noqa: E402

CODE = "ta"
NAME = "Tamil"
NATIVE = "தமிழ்"
PHASE = 2
SCRIPT = "Tamil script"
VOICE = "ta-IN"
SKILL = ("Tamil: Tamil script, agglutinative case suffixes, head-final word order, "
         "diglossia between the written and spoken registers, and the respectful "
         "நீங்கள் / familiar நீ address")

EXTRAS = {}
THIRD = {}
HALFSTEPS = {}

# ── the six CEFR rungs: culture, reading, listening, idioms, mistakes, task ──

EXTRAS["A1"] = EXTRA(
    culture=("Tamil is one of the longest continuously written languages in the "
             "world, and its script is an abugida: every consonant carries an "
             "inherent அ unless a vowel sign changes it, and a pulli (்) removes "
             "the vowel altogether. The script the course teaches is the written "
             "register — செந்தமிழ், 'correct Tamil' — while everyday speech "
             "shortens the same words (வருகிறேன் → வர்றேன்). Both are Tamil, and "
             "the course says which one it is teaching at every step; Thirukkural "
             "couplets and film songs are quoted from memory in the same "
             "households that speak the shortened forms."),
    source_url="https://en.wikipedia.org/wiki/Tamil_language",
    reading=("தமிழ் என் தாய்மொழி. நான் சென்னையில் பிறந்தேன், இப்போது பெங்களூரில் "
             "வேலை செய்கிறேன். வீட்டில் தமிழ் பேசுகிறோம், கடையில் ஆங்கிலம். "
             "வாரம் ஒருமுறை அம்மாவுக்குத் தொலைபேசி செய்கிறேன். என் மகள் இப்போது "
             "தமிழ் எழுதப் பழகுகிறாள்; முதலில் உயிர் எழுத்துகள், பிறகு மெய் "
             "எழுத்துகள். அவளுக்குப் பிடித்த எழுத்து ழ."),
    reading_gloss=("Tamil is my mother tongue. I was born in Chennai and now work "
                   "in Bengaluru. At home we speak Tamil, at the shop English. Once "
                   "a week I telephone my mother. My daughter is now learning to "
                   "write Tamil; first the vowels, then the consonants. Her "
                   "favourite letter is ழ."),
    listening=("வணக்கம், நான் ரவி. நீங்கள் எந்த ஊர்? — நான் மதுரை. தமிழ் "
               "கற்றுக்கொண்டிருக்கிறேன். — நல்லது, மெதுவாகப் பேசுகிறேன்."),
    listening_gloss=("Hello, I am Ravi. Which town are you from? — I am from "
                     "Madurai. I am learning Tamil. — Good, I will speak slowly."),
    voice_tag=VOICE,
    idioms=[
        ("தலைக்கு மேல்", "above the head", "beyond what one can manage"),
        ("கை வரிசை", "the line of the hand", "a person's flair or practised skill"),
        ("மனம் திறந்து", "opening the mind", "frankly, without holding back"),
        ("வயிறு எரிகிறது", "the stomach is burning", "to be eaten up with envy"),
        ("கண் கலங்கியது", "the eye blurred", "to be moved to tears"),
        ("பல் கடித்து", "biting the teeth", "bearing something silently"),
        ("காது கொடுத்துக் கேள்", "listen giving your ear", "listen attentively"),
        ("வெறுங்கையுடன்", "with an empty hand", "empty-handed, with nothing to give"),
        ("சுடுசொல்", "a hot word", "a cutting remark"),
        ("நெஞ்சு பொறுக்கவில்லை", "the chest did not tolerate it", "I could not bear it"),
    ],
    mistakes=[
        ("எனக்கு பெயர் ரவி.", "என் பெயர் ரவி.", "A name takes the genitive என், not the dative எனக்கு."),
        ("நான் போகிறேன் வீட்டிற்கு.", "நான் வீட்டிற்குப் போகிறேன்.", "Tamil is head-final: the verb comes last."),
        ("நீங்கள் வா.", "நீங்கள் வாருங்கள்.", "The respectful நீங்கள் takes the plural imperative."),
    ],
    task_title="என்னை அறிமுகம் செய்யுங்கள்",
    task_instructions=("Write six sentences introducing yourself in Tamil: your "
                       "name, your town, your work or study, one language you "
                       "speak, what you do at home, and one thing you are learning. "
                       "Use நான் with the -கிறேன் present, and the respectful "
                       "நீங்கள் once in a question. Read it aloud twice: once "
                       "slowly for the letters, once at speaking speed. Then write "
                       "the same six sentences with a different subject (அவர், "
                       "அவள், அவர்கள்) and check that the verb ending changes."),
)

EXTRAS["A2"] = EXTRA(
    culture=("Pongal is the four-day harvest festival that opens the Tamil month "
             "of தை (mid-January), and the word itself means 'to boil over'. "
             "Families boil the first rice of the harvest with jaggery in a new "
             "clay pot and let it overflow — an overflow that is welcomed, not "
             "cleaned up — while the doorway carries a fresh கோலம் drawn in rice "
             "flour the night before. The second day belongs to the cattle "
             "(மாட்டுப் பொங்கல்), and the fourth to visiting (காணும் பொங்கல்). "
             "The vocabulary of the festival is also the everyday vocabulary of "
             "the kitchen, which is why Tamil courses meet it so early."),
    source_url="https://en.wikipedia.org/wiki/Pongal_(festival)",
    reading=("நாளை தைப்பொங்கல். அம்மா விடியற்காலையில் எழுந்து அரிசியைக் "
             "கழுவுகிறார். அப்பா கரும்பு வாங்க வந்தார். நான் வாசலில் கோலம் "
             "போட்டேன். பாட்டி சொன்னார்: «பொங்கல் பொங்கட்டும், வீட்டில் "
             "நிறைவு இருக்கும்». மதியம் உறவினர்கள் வருகிறார்கள்; எல்லோரும் "
             "ஒன்றாகச் சாப்பிடுகிறோம். இரவில் நான் நண்பர்களுக்குத் தொலைபேசி "
             "செய்தேன்."),
    reading_gloss=("Tomorrow is Thai Pongal. Mother gets up at dawn and washes the "
                   "rice. Father came to buy sugarcane. I drew a kolam at the "
                   "doorstep. Grandmother said: 'Let the pongal boil over, and "
                   "there will be plenty in the house.' At noon the relatives come; "
                   "we all eat together. In the evening I telephoned my friends."),
    listening=("நாளைக்கு நீங்கள் வருகிறீர்களா? — வருகிறேன், பத்து மணிக்கு. "
               "— கரும்பு வாங்கலாமா? — வாங்கலாம், சந்தையில் கிடைக்கும்."),
    listening_gloss=("Are you coming tomorrow? — I am coming, at ten o'clock. — "
                     "Shall we buy sugarcane? — We can, it is available in the market."),
    voice_tag=VOICE,
    idioms=[
        ("பொங்கல் பொங்குகிறது", "the pongal is boiling over", "good fortune is overflowing"),
        ("கோலம் போடு", "draw a kolam", "to decorate the threshold, to start the day well"),
        ("வீடு திரும்பு", "turn back to the house", "to return home"),
        ("விருந்து வைத்தான்", "he set a feast", "he hosted everyone generously"),
        ("புது நெல்லின் சோறு", "rice of the new paddy", "the first taste of a new season"),
        ("கூடி வாழ்தல்", "living joined together", "living in harmony"),
        ("ஊருக்கு உபதேசம்", "a sermon for the whole town", "advice one does not follow oneself"),
        ("முகம் மலர்ந்தது", "the face blossomed", "the face lit up"),
        ("களைத்துப் போனேன்", "I went tired", "I am worn out"),
        ("நிறைந்த மனசு", "a heart that is full", "a contented, generous mood"),
    ],
    mistakes=[
        ("நான் நாளைக்கு வருவேன்.", "நான் நாளை வருவேன்.", "The written register drops the spoken -க்கு on நாளை."),
        ("நான் தண்ணீர் வேண்டும்.", "எனக்குத் தண்ணீர் வேண்டும்.", "வேண்டும் takes the dative: எனக்கு."),
        ("நான் சென்னை போகிறேன்.", "நான் சென்னைக்குப் போகிறேன்.", "The destination takes -க்கு: சென்னைக்கு."),
    ],
    task_title="ஒரு நாளின் திட்டம்",
    task_instructions=("Write your plans for tomorrow in eight sentences, using the "
                       "present for the plan (நான் ... கிறேன்) and a time expression "
                       "in every sentence (காலையில், பத்து மணிக்கு, மதியம், "
                       "மாலையில், நாளை). Include one invitation with -லாமா? "
                       "(வருகிறீர்களா? / சாப்பிடலாமா?) and one sentence about someone "
                       "else (அம்மா ... கிறார்). Then swap the sentences with a "
                       "partner and answer each one aloud."),
)

EXTRAS["B1"] = EXTRA(
    culture=("A Tamil meal is built around rice, and the banana leaf is its plate: "
             "rice in the middle, sambar and rasam poured over it in that order, "
             "poriyal and kootu along the side, and a piece of appalam to finish. "
             "Filter coffee — காபி, frothed between two tumblers until it foams — "
             "ends the meal and the argument that came with it. The kitchens differ "
             "by district: Chettinad cooks with pepper and fennel, Madurai with "
             "more chilli, Chennai's streets with idli and dosa at every hour. "
             "Food vocabulary is also the vocabulary of hospitality: சாப்பிட்டீர்களா? "
             "is a question about wellbeing, not only about lunch."),
    source_url="https://en.wikipedia.org/wiki/Tamil_cuisine",
    reading=("வார இறுதியில் நண்பர்கள் வீட்டிற்கு வந்தார்கள். அம்மா வாழை இலையில் "
             "சோறு பரிமாறினார்; முதலில் சாம்பார், பிறகு ரசம். என் நண்பன் கார்த்திக் "
             "செட்டிநாடு பாணியில் காரம் அதிகம் சாப்பிடுகிறான். «இங்கே ருசி "
             "வேறு» என்றான். முடிவில் காபி வந்தது; அப்பா கேட்டார்: «இன்னொரு "
             "தம்ளர்?» நாங்கள் அரை மணி நேரம் பேசிக்கொண்டிருந்தோம். "
             "விருந்துக்குப் பிறகு அம்மா சொன்னார்: «வீட்டில் சாப்பிடுவது "
             "வெறும் சோறு அல்ல, நினைவு.»"),
    reading_gloss=("At the weekend friends came home. Mother served rice on a banana "
                   "leaf; first sambar, then rasam. My friend Karthik eats very "
                   "spicy Chettinad style. 'The taste is different here,' he said. "
                   "At the end the coffee came; father asked: 'Another tumbler?' We "
                   "went on talking for half an hour. After the meal mother said: "
                   "'Eating at home is not just rice, it is memory.'"),
    listening=("சாப்பிட்டீர்களா? — ஆமா, சாப்பிட்டேன், நன்றி. — இன்னும் கொஞ்சம் "
               "சோறு? — போதும், வயிறு நிறைந்தது. காபி மட்டும் குடிப்பேன்."),
    listening_gloss=("Have you eaten? — Yes, I have eaten, thank you. — A little "
                     "more rice? — That is enough, my stomach is full. I will only "
                     "drink coffee."),
    voice_tag=VOICE,
    idioms=[
        ("வயிறு நிறைந்தது", "the stomach was filled", "I have had plenty"),
        ("கை மணக்கும்", "the hand smells of it", "the cooking is fragrant, well made"),
        ("சோறு போட்டவள்", "the one who has served rice", "the person who has fed you, a benefactor"),
        ("காரம் தாங்கவில்லை", "the heat cannot be borne", "it is too spicy for me"),
        ("ருசி பார்க்க", "to look at the taste", "to taste a dish"),
        ("இலை போட்டான்", "he laid the leaf", "he served a meal, usually a generous one"),
        ("தம்ளர் கொடு", "give a tumbler", "pour the coffee"),
        ("பட்டினி கிட", "to stay starving", "to go without eating"),
        ("உப்பு குறைவு", "the salt is short", "the dish is undersalted, a mild complaint"),
        ("கடைசி வாய்", "the last mouthful", "the final item, the closing part"),
    ],
    mistakes=[
        ("அம்மா சோறு பரிமாறினார் ஒரு இலையில்.", "அம்மா ஒரு இலையில் சோறு பரிமாறினார்.", "The finite verb closes the clause; the adverbial phrase stays before it."),
        ("நான் ஒரு தம்ளர் காபி குடித்தேன் விரைவாக.", "நான் ஒரு தம்ளர் காபியை விரைவாகக் குடித்தேன்.", "The object marked by -ஐ stays next to the verb it belongs to."),
        ("சாப்பிட்டீர்களா? — ஆமா, சாப்பிட்டேன்.", "சாப்பிட்டீர்களா? — ஆமாம், சாப்பிட்டேன்.", "ஆமாம் is the written form; ஆமா belongs to speech."),
    ],
    task_title="விருந்துக்கு நன்றி",
    task_instructions=("Write a short account of a meal you remember: who cooked, "
                       "what was served, one comparison between two kitchens or two "
                       "cooks, and a closing sentence with a proverb-like comment. "
                       "Use two relative participles (நான் சாப்பிட்ட பிரியாணி), one "
                       "comparative with -ஐ விட (சாம்பார் ரசத்தை விட காரம்) and one "
                       "reported speech with என்று. Read it aloud and mark every "
                       "place where you would shorten the word in speech."),
)

EXTRAS["B2"] = EXTRA(
    culture=("Tamil cinema is not a single genre: the studios and theatres of Chennai "
             "support commercial drama, political satire, intimate independent films "
             "and adaptations of short fiction. Kodambakkam — a Chennai neighbourhood "
             "with many studios — is so closely associated with Tamil-language film "
             "that it is nicknamed its 'Hollywood'. Songs are not an intermission: "
             "lyrics can carry the scene's argument, a melody can return as a character "
             "changes, and the playback singer may be a different artist from the actor "
             "whose mouth moves on screen. Listening closely is a way to hear register "
             "and metaphor as well as plot."),
    source_url="https://www.britannica.com/topic/Tamil",
    reading=("புதிய படத்தின் பாடலைக் கேட்ட பிறகு மீனா அதன் வரிகளைத் தேடினாள். "
             "«இந்தப் பாடல் கதையைச் சுருக்கவில்லை; கதாநாயகியின் முடிவை "
             "மாற்றுகிறது» என்றாள். இயக்குநர் அந்த வரியைப் பின்னர் வரும் "
             "காட்சியிலும் ஒலிக்கச் செய்திருந்தார். முதல் முறை அது காதல் பாடலாகத் "
             "தெரிந்தது; இரண்டாவது முறை அது எதிர்ப்பாகக் கேட்டது. பாடிய குரலும் "
             "நடிகையின் குரலும் ஒன்றல்ல என்பதை வரவுகளில் பார்த்தோம். இசை "
             "மாறியதும் காட்சியின் பொருளும் மாறியது."),
    reading_gloss=("After hearing the new film's song, Meena looked up its lyrics. 'This "
                   "song does not summarise the story; it changes the heroine's "
                   "decision,' she said. The director had made that line sound again "
                   "in a later scene. The first time it seemed a love song; the second "
                   "time it sounded like resistance. We saw in the credits that the "
                   "singing voice and the actress's voice were not the same. When the "
                   "music changed, the scene's meaning changed too."),
    listening=("படத்தின் முடிவு உங்களுக்குப் பிடித்ததா? — பிடித்தது; ஆனால் பாடல் "
               "மீண்டும் வரும் விதம் கதையின் கருத்தை மாற்றியது. — எந்த வரி? — "
               "«நான் காத்திருக்க மாட்டேன்» என்ற வரி. முதலில் அது காதலாக இருந்தது; "
               "பிறகு எதிர்ப்பாக மாறியது."),
    listening_gloss=("Did you like the film's ending? — I did, but the way the song "
                     "returns changed the story's idea. — Which line? — The line, 'I "
                     "will not wait.' At first it was love; later it became resistance."),
    voice_tag=VOICE,
    idioms=[
        ("காட்சியைத் திருடு", "steal the scene", "draw all the attention in a scene"),
        ("திரைக்குப் பின்னால்", "behind the screen", "behind the scenes, out of public view"),
        ("கதை கட்டு", "build a story", "to make up an explanation or a plot"),
        ("குரல் கொடு", "give a voice", "to speak up for a cause or person"),
        ("வசனம் பேசு", "speak the dialogue", "to deliver a line; also to state one's case"),
        ("முகம் காட்டுதல்", "show one's face", "to appear in public or make an appearance"),
        ("கை தட்டு", "clap a hand", "to applaud, or to approve openly"),
        ("திருப்புமுனை", "a turning point", "a decisive change in a story or situation"),
        ("படம் ஓடுகிறது", "the film is running", "the film is playing or succeeding"),
        ("கதை வேறு, காட்சி வேறு", "the story is one thing, the scene another", "the same facts can be framed differently"),
    ],
    mistakes=[
        ("பாடல் காட்சியைப் பொருள் மாறியது.", "பாடல் காட்சியின் பொருளை மாற்றியது.", "பொருள் is the object of மாற்றியது, so it takes -ஐ; காட்சியின் marks possession."),
        ("நடிகை பாடலைப் பாடப்பட்டாள்.", "பாடல் பாடப்பட்டது.", "The impersonal passive uses the thing as subject: பாடல் பாடப்பட்டது."),
        ("படம் நன்றாக இருந்தாலும், ஆனால் நீளம் அதிகம்.", "படம் நன்றாக இருந்தாலும், நீளம் அதிகம்.", "The concessive இருந்தாலும் already means 'although'; do not add ஆனால்."),
    ],
    task_title="ஒரு காட்சியின் இரு வாசிப்புகள்",
    task_instructions=("Choose a film scene or song whose meaning changes when you hear it "
                       "again. Write a short review with a neutral summary, your "
                       "interpretation, and one alternative reading. Use a concessive "
                       "clause with இருந்தாலும், report one line with என்று, and explain "
                       "how the sound or image changes the audience's inference. Do not "
                       "retell the whole plot; identify the precise turning point."),
)

EXTRAS["C1"] = EXTRA(
    culture=("Sangam poetry organises interior experience through landscape. In the "
             "Ainkurunuru, five sets of one hundred short poems are associated with "
             "five thinai: kurinji (mountain), mullai (pasture and forest), marutham "
             "(cultivated land), neithal (shore), and palai (wasteland). A landscape is "
             "not a decorative backdrop: plants, time of day, occupation, and weather "
             "help the poem imply a relationship's situation without spelling it out. "
             "The Tamil Virtual Academy's lesson describes each thinai as joining a "
             "geography to a 'mindscape'. Reading such a poem means asking what the "
             "image lets the speaker leave unsaid."),
    source_url="https://www.tamilvu.org/courses/degree/d011/d0112/html/d01121ad.htm",
    reading=("நெய்தல் திணையில் கடல் வெறும் பின்னணி அல்ல. காத்திருக்கும் "
             "தலைவியின் கவலை, அலை திரும்பி வருவதைப் போலத் திரும்பத் திரும்ப "
             "எழுகிறது. தோழி நேரடியாக «அவள் வருந்துகிறாள்» என்று சொல்லவில்லை; "
             "கரையில் நின்று தொலைவில் செல்லும் படகைப் பார்க்கிறாள். அந்தக் "
             "காட்சி பிரிவை உணர்த்துகிறது. நிலமும் மனநிலையும் ஒன்றாகப் "
             "செயல்படும்போது, குறைந்த சொற்களிலேயே கவிதை முழு உறவையும் "
             "உருவாக்குகிறது."),
    reading_gloss=("In the neithal thinai the sea is not merely a background. The "
                   "waiting heroine's worry rises again and again, like a wave that "
                   "returns. The friend does not directly say 'she is grieving'; she "
                   "stands on the shore and watches a boat recede into the distance. "
                   "That image suggests separation. When land and state of mind work "
                   "together, the poem creates a whole relationship in very few words."),
    listening=("இந்தக் கவிதையில் பாலை நிலம் ஏன் வருகிறது? — பயணம் கடினமானது "
               "என்பதை மட்டும் சொல்ல அல்ல. பிரிவின் நீளத்தையும் ஆபத்தையும் "
               "ஒரே உருவகத்தில் சேர்க்கிறது. — அப்படியானால், நிலக்காட்சி "
               "உணர்ச்சிக்கான சான்றா? — சான்று மட்டும் அல்ல; அது கவிதையின் "
               "அமைப்பே."),
    listening_gloss=("Why does the palai landscape appear in this poem? — Not only to "
                     "say that the journey is difficult. It brings the length and the "
                     "danger of separation into one image. — Then is the landscape "
                     "evidence for the emotion? — Not only evidence; it is the poem's "
                     "structure itself."),
    voice_tag=VOICE,
    idioms=[
        ("உள்ளங்கை நெல்லிக்கனி", "an amla fruit in the palm", "something plain to see, requiring no proof"),
        ("அகமும் புறமும்", "the interior and the exterior", "private feeling and public life"),
        ("சொல்லாமல் சொல்", "say without saying", "let an image or implication carry the meaning"),
        ("நுண்ணிய வேறுபாடு", "a fine distinction", "a subtle but meaningful difference"),
        ("மறைபொருள்", "the hidden meaning", "an implication beneath the literal reading"),
        ("பொருள் பொதிந்த சொல்", "a word filled with meaning", "a compact word with several resonances"),
        ("காலத்தைக் கடந்து", "crossing beyond time", "enduring across generations"),
        ("கண்ணுக்குப் புலப்படாதது", "what is not visible to the eye", "an unseen force or idea"),
        ("சொல்லின் செறிவு", "the density of the word", "meaning packed into a few words"),
        ("ஒரு பக்கம் பார்த்தால்", "if seen from one side", "one perspective among several"),
    ],
    mistakes=[
        ("இக்காட்சி உணர்ச்சியை விளக்கமாகிறது.", "இக்காட்சி உணர்ச்சியை விளக்குகிறது.", "விளக்குகிறது is the finite verb; விளக்கமாகிறது means 'becomes explanatory' and is not the intended form."),
        ("நிலமும் மனநிலையும் ஒன்று அல்ல; ஆனால் கவிதையில் இரண்டும் தொடர்புடையது.", "நிலமும் மனநிலையும் வேறானவை; இருந்தாலும் கவிதையில் இரண்டும் தொடர்புடையவை.", "Use plural agreement and a clear concessive relation for two related things."),
        ("கவிஞர் சொல்லாமல், காட்சியை உருவாக்குகிறார்.", "கவிஞர் நேரடியாகச் சொல்லாமல், காட்சியின் வழியாக உணர்த்துகிறார்.", "The first version leaves the action incomplete; state what the image implies."),
    ],
    task_title="திணையும் மனநிலையும்",
    task_instructions=("Select a short poem, film scene, or landscape description. Write an "
                       "interpretive paragraph that separates (1) the literal setting, "
                       "(2) the emotional situation it implies, and (3) the evidence "
                       "that supports your reading. Include one alternative interpretation "
                       "and say what the text does not establish. Use a concessive clause, "
                       "one reported claim, and the distinction between அகப்பொருள் and "
                       "புறப்பொருள் without treating it as a rigid formula."),
)

EXTRAS["C2"] = EXTRA(
    culture=("The Tirukkural is a compact work of 1,330 couplets arranged in 133 "
             "chapters. The Tamil Virtual Academy presents its three divisions as "
             "அறம் (aram, virtue), பொருள் (porul, public and material life), and "
             "இன்பம் (inbam, love and human relationship). The form is small enough "
             "to memorise and dense enough to invite commentary: translators must "
             "decide what to do with a word that carries an ethical idea, a social "
             "relationship, and a rhythm at once. The point of comparing translations "
             "is not to crown one as final, but to notice what each version preserves, "
             "makes explicit, or lets remain open. The age and historical context of "
             "the text are matters of scholarly debate; its three-part structure is "
             "not."),
    source_url="https://www.tamilvu.org/courses/diploma/c031/c0313/html/c0313107.htm",
    reading=("ஒரு குறளின் ஆங்கில மொழிபெயர்ப்பில் «அறம்» என்பதற்கு virtue என்று "
             "கொடுக்கப்பட்டுள்ளது. மற்றொரு மொழிபெயர்ப்பாளர் அதை ethical conduct "
             "என்று விரிக்கிறார். முதல் சொல் சுருக்கமானது; இரண்டாவது அதன் "
             "செயல்முறையை வெளிப்படுத்துகிறது. எது சரி என்று மட்டும் கேட்பதைவிட, "
             "எந்த வாசகருக்காக எந்தத் தேர்வு செய்யப்பட்டது என்று கேட்பது பயனுள்ளது. "
             "மொழிபெயர்ப்பு ஒரு கதவைத் திறக்கிறது; அதே நேரத்தில் மூலச் சொல்லின் "
             "எல்லா எதிரொலிகளையும் தன்னுடன் கொண்டு செல்ல முடியாது."),
    reading_gloss=("In one English translation of a Kural, அறம் is rendered as 'virtue'. "
                   "Another translator expands it as 'ethical conduct'. The first word is "
                   "compact; the second makes its practice explicit. Rather than asking "
                   "only which is correct, it is useful to ask which choice was made for "
                   "which reader. A translation opens a door; at the same time it cannot "
                   "carry every resonance of the source word with it."),
    listening=("இரண்டு மொழிபெயர்ப்புகளும் ஒரே குறளை வேறுவிதமாகத் தருகின்றன. "
               "ஒன்று ஓசையையும் சுருக்கத்தையும் காக்கிறது; மற்றொன்று கருத்தை "
               "விளக்குகிறது. எது மூலத்துக்கு நெருக்கம்? — ஒரு அளவுகோலால் "
               "முடிவெடுக்க முடியாது. முதலில் எதை ஒப்பிடுகிறோம் என்று தெளிவுபடுத்த "
               "வேண்டும்."),
    listening_gloss=("The two translations render the same Kural differently. One "
                     "preserves sound and brevity; the other explains the idea. Which "
                     "is closer to the original? — We cannot decide with one measure. "
                     "First we must clarify what we are comparing."),
    voice_tag=VOICE,
    idioms=[
        ("அளவுக்கு மிஞ்சினால் அமிர்தமும் நஞ்சு", "beyond the measure, even nectar is poison", "excess can spoil what is good"),
        ("கற்றது கைம்மண்ணளவு, கல்லாதது உலகளவு", "what is learned is a handful of sand; what is unknown is the world", "learning reveals how much remains to learn"),
        ("காக்கைக்கும் தன் குஞ்சு பொன் குஞ்சு", "to a crow its chick is a golden chick", "everyone sees their own as precious"),
        ("சிறு துளி பெரு வெள்ளம்", "small drops make a great flood", "small contributions accumulate"),
        ("ஆற்றில் போட்டாலும் அளந்து போடு", "measure it even if you put it in a river", "use resources carefully"),
        ("தீயினால் சுட்ட புண் உள்ளாறும்", "a fire-burned wound may heal", "physical hurt can heal"),
        ("நாவினால் சுட்ட வடு ஆறாது", "a wound made by the tongue does not heal", "hurtful words leave a lasting mark"),
        ("பொறுத்தார் பூமி ஆள்வார்", "the patient will rule the earth", "patience can outlast force"),
        ("வினை விதைத்தவன் வினை அறுப்பான்", "the one who sows an act will reap its act", "actions bring their consequences"),
        ("ஒன்றுபட்டால் உண்டு வாழ்வு", "if united, there is life", "cooperation sustains a community"),
    ],
    mistakes=[
        ("இந்த மொழிபெயர்ப்பு மட்டுமே சரியானது என்று நிரூபிக்கிறது.", "இந்த மொழிபெயர்ப்பு ஒரு பொருள்வாசிப்பை முன்வைக்கிறது.", "A translation advances an interpretation; without argument it cannot prove exclusivity."),
        ("இரு உரைகளிலும் சொல்லின் ஓசை காக்கப்படுகிறது.", "ஒரு உரை ஓசையைக் காக்கிறது; மற்றொன்று கருத்தை விரிக்கிறது.", "Do not claim both versions preserve a feature when the comparison shows a trade-off."),
        ("குறள் பழமையானதால், அதன் பொருள் எல்லாக் காலத்திலும் ஒன்றே.", "குறள் பழமையானது; அதன் வாசிப்பு காலத்தோடு மாறலாம்.", "A text's age does not make its interpretation historically fixed."),
    ],
    task_title="மொழிபெயர்ப்பின் தேர்வுகள்",
    task_instructions=("Compare two translations of the same short Tamil passage. Quote no more "
                       "than one phrase from each version. Identify one choice about register, "
                       "rhythm, or an ambiguous word; describe what each version gains and "
                       "loses; and state which readers each version serves. Finish with a "
                       "qualified conclusion rather than a winner. Distinguish evidence from "
                       "your preference, and do not claim the English can reproduce every "
                       "feature of the Tamil original."),
)

# Small authoring helper: all content still flows through depth_kit's V/X/G/D/T/WS/L.
def _spec_lesson(title, learn, vocab, grammar_title, pattern, explain, examples,
                  mistakes, dialogue, worksheet_title, tasks):
    return L(title, learn,
             [V(*row) for row in vocab],
             G(grammar_title, pattern, explain, [X(*row) for row in examples], mistakes),
             [D(*row) for row in dialogue],
             WS(worksheet_title, [T(*row) for row in tasks]))


# ── third lessons for the 18 existing units ─────────────────────────────────

THIRD["A1"] = [
    ("ta-a1-u1", "ta-a1-l7", _spec_lesson(
        "குடும்பமும் உறவுகளும்",
        "Name the people in a family and say who someone is to you. என் introduces "
        "one person's relation; எங்கள் introduces the family as a group. In Tamil, "
        "the familiar kin term can also be a warm form of address, but this lesson "
        "keeps the respectful நீங்கள் for a new adult.",
        [("குடும்பம்", "kuṭumpam", "family", "noun"),
         ("அம்மா", "ammā", "mother", "noun"),
         ("அப்பா", "appā", "father", "noun"),
         ("அண்ணன்", "aṇṇaṉ", "elder brother", "noun"),
         ("தங்கை", "taṅkai", "younger sister", "noun")],
        "My family", "என் + kin term · அவர் என் ... · எங்கள் குடும்பம்",
        "Possession comes before the noun: என் அண்ணன். For a person's role, say "
        "அவர் என் அப்பா. The pronoun அவர் is respectful and takes the plural-like "
        "அவர் இருக்கிறார் form, even when referring to one person.",
        [("இவர் என் அம்மா.", "ivar eṉ ammā.", "This is my mother."),
         ("அவர் என் அண்ணன்.", "avar eṉ aṇṇaṉ.", "He is my elder brother."),
         ("எங்கள் குடும்பத்தில் நான்கு பேர் இருக்கிறார்கள்.", "eṅkaḷ kuṭumpattil nāṉku pēr irukkiṟārkaḷ.", "There are four people in our family.")],
        [("என் அண்ணன் இவர்.", "இவர் என் அண்ணன்.", "The simple introduction places இவர் first."),
         ("அவர் என் அப்பா இருக்கிறான்.", "அவர் என் அப்பா இருக்கிறார்.", "Respectful அவர் takes இருக்கிறார், not the familiar இருக்கிறான்.")],
        [("Divya", "இவர் யார்?", "ivar yār?", "Who is this?"),
         ("Karthik", "இவர் என் அம்மா.", "ivar eṉ ammā.", "This is my mother."),
         ("Divya", "உங்கள் குடும்பத்தில் எத்தனை பேர் இருக்கிறார்கள்?", "uṅkaḷ kuṭumpattil ettaṉai pēr irukkiṟārkaḷ?", "How many people are there in your family?"),
         ("Karthik", "நான்கு பேர். என் அப்பா, அம்மா, தங்கை, நான்.", "nāṉku pēr. eṉ appā, ammā, taṅkai, nāṉ.", "Four people: my father, mother, younger sister, and me.")],
        "Family worksheet", [
            ("Introduce the person.", ["this is my mother", "he is my elder brother"], ["இவர் என் அம்மா", "அவர் என் அண்ணன்"]),
            ("Say who is in the family.", ["four people in our family", "my father, mother, younger sister, and me"], ["எங்கள் குடும்பத்தில் நான்கு பேர்", "என் அப்பா, அம்மா, தங்கை, நான்"]),
        ])),
    ("ta-a1-u2", "ta-a1-l8", _spec_lesson(
        "கடையில் வாங்குதல்",
        "Ask a shopkeeper for a quantity and the price. ஒரு கிலோ, அரை கிலோ and இரண்டு "
        "பழம் name amounts; வேண்டும் states what you need, while எவ்வளவு? asks the "
        "price. Put the item and quantity before the verb வேண்டும்.",
        [("கடை", "kaṭai", "shop", "noun"),
         ("விலை", "vilai", "price", "noun"),
         ("கிலோ", "kilō", "kilogram", "measure"),
         ("அரை", "arai", "half", "quantity"),
         ("தக்காளி", "takkāḷi", "tomato", "noun")],
        "Amounts and requests", "item + quantity + வேண்டும் · இது எவ்வளவு?",
        "வேண்டும் follows the thing requested: இரண்டு கிலோ தக்காளி வேண்டும். To ask "
        "about a price, use எவ்வளவு?; the answer is a number followed by ரூபாய். "
        "The measure word follows the number.",
        [("எனக்கு ஒரு கிலோ தக்காளி வேண்டும்.", "eṉakku oru kilō takkāḷi vēṇṭum.", "I need one kilogram of tomatoes."),
         ("இந்தப் பழம் எவ்வளவு?", "intap paḻam evvaḷavu?", "How much is this fruit?"),
         ("அரை கிலோ இருபது ரூபாய்.", "arai kilō irupatu rūpāy.", "Half a kilo is twenty rupees.")],
        [("தக்காளி ஒரு கிலோ வேண்டும்.", "ஒரு கிலோ தக்காளி வேண்டும்.", "Keep the quantity next to the item, before வேண்டும்."),
         ("எனக்கு வேண்டும் தக்காளி.", "எனக்கு தக்காளி வேண்டும்.", "வேண்டும் closes the request." )],
        [("வாடிக்கையாளர்", "வணக்கம். ஒரு கிலோ தக்காளி வேண்டும்.", "vaṇakkam. oru kilō takkāḷi vēṇṭum.", "Hello. I need one kilogram of tomatoes."),
         ("விற்பனையாளர்", "சரி. இன்னும் ஏதாவது வேண்டுமா?", "sari. iṉṉum ētāvatu vēṇṭumā?", "Certainly. Do you need anything else?"),
         ("வாடிக்கையாளர்", "அரை கிலோ வெங்காயமும் வேண்டும். விலை எவ்வளவு?", "arai kilō veṅkāyamum vēṇṭum. vilai evvaḷavu?", "I also need half a kilo of onions. What is the price?"),
         ("விற்பனையாளர்", "மொத்தம் அறுபது ரூபாய்.", "mottam aṟupatu rūpāy.", "Sixty rupees in total.")],
        "At the shop worksheet", [
            ("Ask for the amount.", ["I need one kilogram of tomatoes", "I also need half a kilo of onions"], ["எனக்கு ஒரு கிலோ தக்காளி வேண்டும்", "அரை கிலோ வெங்காயமும் வேண்டும்"]),
            ("Ask and answer the price.", ["how much is this fruit?", "half a kilo is twenty rupees"], ["இந்தப் பழம் எவ்வளவு?", "அரை கிலோ இருபது ரூபாய்"]),
        ])),
    ("ta-a1-u3", "ta-a1-l9", _spec_lesson(
        "பேருந்து நிலையத்தில்",
        "Ask which bus goes to a place and understand a simple direction. The destination "
        "takes -க்கு; எங்கே? asks where, and நேராக / வலப்பக்கம் / இடப்பக்கம் give a "
        "short route. In a respectful request, say சொல்லுங்கள் rather than சொல்.",
        [("பேருந்து", "pēruntu", "bus", "noun"),
         ("நிலையம்", "nilaiyam", "station", "noun"),
         ("வலப்பக்கம்", "valappakkam", "on the right", "direction"),
         ("இடப்பக்கம்", "iṭappakkam", "on the left", "direction"),
         ("நேராக", "nērāka", "straight ahead", "adverb")],
        "Destinations and directions", "place + -க்கு · எப்படிப் போவது? · நேராகச் செல்லுங்கள்",
        "The destination marker -க்கு joins to the place: மதுரைக்கு. Ask எப்படிப் "
        "போவது? (how to go?) and listen for a sequence: முதலில் (first), பிறகு "
        "(then). The respectful instruction ends with -ுங்கள்.",
        [("நிலையத்திற்கு எப்படிப் போவது?", "nilaiyattiṟku eppaṭip pōvatu?", "How do I get to the station?"),
         ("நேராகச் சென்று வலப்பக்கம் திரும்புங்கள்.", "nērākac cenṟu valappakkam tirumpuṅkaḷ.", "Go straight and turn right."),
         ("பேருந்து நிலையம் அருகில்தான் இருக்கிறது.", "pēruntu nilaiyam arukil-tāṉ irukkiṟatu.", "The bus station is quite nearby.")],
        [("நான் நிலையம் போகிறேன்.", "நான் நிலையத்திற்குப் போகிறேன்.", "The destination takes -க்கு."),
         ("வலப்பக்கம் திரும்பு.", "வலப்பக்கம் திரும்புங்கள்.", "Use the respectful imperative with a new person.")],
        [("பயணி", "மன்னிக்கவும், பேருந்து நிலையம் எங்கே?", "maṉṉikkavum, pēruntu nilaiyam eṅkē?", "Excuse me, where is the bus station?"),
         ("உள்ளூர்வாசி", "நேராகச் செல்லுங்கள்; பிறகு இடப்பக்கம்.", "nērākac celluṅkaḷ; piṟaku iṭappakkam.", "Go straight; then to the left."),
         ("பயணி", "அங்கு எவ்வளவு தூரம்?", "aṅku evvaḷavu tūram?", "How far is it?"),
         ("உள்ளூர்வாசி", "ஐந்து நிமிடம். நிலையம் சாலையின் முடிவில்.", "aintu nimiṭam. nilaiyam cālaiyiṉ muṭivil.", "Five minutes. The station is at the end of the road.")],
        "Directions worksheet", [
            ("Ask for the station.", ["excuse me, where is the bus station?", "how do I get to the station?"], ["மன்னிக்கவும், பேருந்து நிலையம் எங்கே?", "நிலையத்திற்கு எப்படிப் போவது?"]),
            ("Give the route.", ["go straight and turn right", "the station is at the end of the road"], ["நேராகச் சென்று வலப்பக்கம் திரும்புங்கள்", "நிலையம் சாலையின் முடிவில்"]),
        ])),
]

THIRD["A2"] = [
    ("ta-a2-u1", "ta-a2-l7", _spec_lesson(
        "மருத்துவரிடம் நேரம் கேட்பது",
        "Make an appointment and describe a simple symptom. The body part comes before "
        "வலி (pain); எனக்கு marks the person experiencing it, and வேண்டும் expresses "
        "the need for an appointment. Ask for a date with எந்த நாள்?",
        [("தலைவலி", "talaivali", "headache", "noun"),
         ("காய்ச்சல்", "kāyccal", "fever", "noun"),
         ("மருத்துவர்", "marutt uvar", "doctor", "noun"),
         ("நேரம்", "nēram", "time, appointment slot", "noun"),
         ("ஓய்வு", "ōyvu", "rest", "noun")],
        "Symptoms and appointments", "எனக்கு + symptom + இருக்கிறது · ... வேண்டும்",
        "For a symptom, say எனக்கு தலைவலி இருக்கிறது. The singular symptom takes "
        "இருக்கிறது. To request an appointment, say மருத்துவரைப் பார்க்க நேரம் "
        "வேண்டும்; the object மருத்துவரை takes -ஐ.",
        [("எனக்கு இரண்டு நாட்களாகக் காய்ச்சல் இருக்கிறது.", "eṉakku iraṇṭu nāṭkaḷākak kāyccal irukkiṟatu.", "I have had a fever for two days."),
         ("நாளை மருத்துவரைப் பார்க்க நேரம் வேண்டும்.", "nāḷai maruttuvaraip pārkka nēram vēṇṭum.", "I need an appointment to see the doctor tomorrow."),
         ("மருந்து சாப்பிட்ட பிறகு ஓய்வு எடுங்கள்.", "maruntu cāppiṭṭa piṟaku ōyvu eṭuṅkaḷ.", "Rest after taking the medicine.")],
        [("எனக்கு காய்ச்சல் இருக்கின்றன.", "எனக்கு காய்ச்சல் இருக்கிறது.", "காய்ச்சல் is singular here, so use இருக்கிறது."),
         ("நான் மருத்துவர் பார்க்க நேரம் வேண்டும்.", "நான் மருத்துவரைப் பார்க்க நேரம் வேண்டும்.", "The person seen is the object: மருத்துவரை.")],
        [("வரவேற்பாளர்", "வணக்கம். என்ன உதவி வேண்டும்?", "vaṇakkam. eṉṉa utavi vēṇṭum?", "Hello. How can I help?"),
         ("நோயாளி", "எனக்கு இரண்டு நாட்களாகக் காய்ச்சல் இருக்கிறது.", "eṉakku iraṇṭu nāṭkaḷākak kāyccal irukkiṟatu.", "I have had a fever for two days."),
         ("வரவேற்பாளர்", "நாளை காலை பத்து மணிக்கு நேரம் இருக்கிறது.", "nāḷai kālai pattu maṇikku nēram irukkiṟatu.", "There is an appointment tomorrow at ten in the morning."),
         ("நோயாளி", "சரி, அந்த நேரம் எனக்கு வசதி.", "sari, anta nēram eṉakku vacati.", "All right, that time works for me.")],
        "Clinic worksheet", [
            ("Describe the symptom.", ["I have had a fever for two days", "I have a headache"], ["எனக்கு இரண்டு நாட்களாகக் காய்ச்சல் இருக்கிறது", "எனக்குத் தலைவலி இருக்கிறது"]),
            ("Arrange the visit.", ["I need an appointment to see the doctor tomorrow", "that time works for me"], ["நாளை மருத்துவரைப் பார்க்க நேரம் வேண்டும்", "அந்த நேரம் எனக்கு வசதி"]),
        ])),
    ("ta-a2-u2", "ta-a2-l8", _spec_lesson(
        "பள்ளித் திட்டமும் வானிலையும்",
        "Talk about a school activity affected by the weather. Use இன்று / நாளை with "
        "the correct verb time, and because with -ஆல் or அதனால் to connect weather "
        "and a plan. Tamil keeps the finite verb at the end of each clause.",
        [("வானிலை", "vāṉilai", "weather", "noun"),
         ("மழை", "maḻai", "rain", "noun"),
         ("வகுப்பு", "vakuppu", "class", "noun"),
         ("திட்டம்", "tiṭṭam", "plan", "noun"),
         ("மாற்று", "māṟṟu", "to change", "verb")],
        "Reason and changed plans", "மழை பெய்வதால் ... · அதனால் ... · நாளை ... செய்வோம்",
        "Attach -ஆல் to a reason noun or verb: மழையால் (because of rain), மழை "
        "பெய்வதால் (because it is raining). அதனால் begins the result. நாளை is a "
        "future-time word, so the plan uses a future verb such as செய்வோம்.",
        [("மழை பெய்வதால் விளையாட்டு வகுப்பு உள்ளே நடக்கும்.", "maḻai peyvatāl viḷaiyāṭṭu vakuppu uḷḷē naṭakkum.", "Because it is raining, the sports class will be indoors."),
         ("வானிலை நன்றாக இருந்தால், வெளியே படிப்போம்.", "vāṉilai naṉṟāka iruntāl, veḷiyē paṭippōm.", "If the weather is good, we will study outside."),
         ("அதனால் ஆசிரியர் திட்டத்தை மாற்றினார்.", "ataṉāl āciriyar tiṭṭattai māṟṟiṉār.", "Therefore the teacher changed the plan.")],
        [("மழை பெய்கிறது அதனால் வகுப்பு உள்ளே நடக்கும்.", "மழை பெய்வதால் வகுப்பு உள்ளே நடக்கும்.", "Join the reason with -வதால், or separate it with அதனால்."),
         ("நாளை நாங்கள் படித்தோம்.", "நாளை நாங்கள் படிப்போம்.", "A future time word takes a future verb.")],
        [("மாணவர்", "நாளைய வெளிப்புற வகுப்பு நடக்குமா?", "nāḷaiya veḷippuṟa vakuppu naṭakkumā?", "Will tomorrow's outdoor class take place?"),
         ("ஆசிரியர்", "மழை பெய்வதால் வகுப்பு உள்ளே நடக்கும்.", "maḻai peyvatāl vakuppu uḷḷē naṭakkum.", "Because it is raining, the class will be indoors."),
         ("மாணவர்", "வானிலை மாறினால் வெளியே செல்லலாமா?", "vāṉilai māṟiṉāl veḷiyē cellalāmā?", "If the weather changes, may we go outside?"),
         ("ஆசிரியர்", "ஆம், மதியத்துக்குப் பிறகு முடிவு செய்வோம்.", "ām, matiyattukku-p piṟaku muṭivu ceyvōm.", "Yes, we will decide after noon.")],
        "Weather and school worksheet", [
            ("Give the reason.", ["because it is raining, the class will be indoors", "therefore the teacher changed the plan"], ["மழை பெய்வதால் வகுப்பு உள்ளே நடக்கும்", "அதனால் ஆசிரியர் திட்டத்தை மாற்றினார்"]),
            ("Make the plan conditional.", ["if the weather is good, we will study outside", "we will decide after noon"], ["வானிலை நன்றாக இருந்தால் வெளியே படிப்போம்", "மதியத்துக்குப் பிறகு முடிவு செய்வோம்"]),
        ])),
    ("ta-a2-u3", "ta-a2-l9", _spec_lesson(
        "உறவினர்களை அழைத்தல்",
        "Invite relatives and agree on a time. -லாமா? makes a polite suggestion; "
        "வருகிறீர்களா? asks whether someone can come, while வந்த பிறகு sequences "
        "what happens after arrival. Keep the respectful plural ending when inviting "
        "an elder or a new guest.",
        [("அழைப்பு", "aḻaippu", "invitation", "noun"),
         ("உறவினர்", "uṟaviṉar", "relative", "noun"),
         ("நாளை", "nāḷai", "tomorrow", "adverb"),
         ("வந்த பிறகு", "vanta piṟaku", "after arriving", "phrase"),
         ("சேர்ந்து", "cērntu", "together", "adverb")],
        "Inviting and sequencing", "...லாமா? · ...வருகிறீர்களா? · வந்த பிறகு ...",
        "The suggestion suffix -லாமா? attaches to the verb: சாப்பிடலாமா? (shall we "
        "eat?). For a respectful invitation, use வருகிறீர்களா? After an action, "
        "வந்த பிறகு means 'after coming'; the next clause gives the plan.",
        [("நாளை எங்கள் வீட்டுக்கு வருகிறீர்களா?", "nāḷai eṅkaḷ vīṭṭukku varukiṟīrkaḷā?", "Will you come to our home tomorrow?"),
         ("வந்த பிறகு சேர்ந்து சாப்பிடலாம்.", "vanta piṟaku cērntu cāppiṭalām.", "After you arrive, we can eat together."),
         ("மாலை ஆறு மணிக்கு வருவது வசதியா?", "mālai āṟu maṇikku varuvatu vacatiyā?", "Is coming at six in the evening convenient?")],
        [("நாளை வீட்டுக்கு வருகிறாயா? (respectful)", "நாளை வீட்டுக்கு வருகிறீர்களா?", "Use the respectful plural ending for a guest."),
         ("வந்த பிறகு நாங்கள் சாப்பிட்டோம். (future plan)", "வந்த பிறகு நாங்கள் சாப்பிடலாம்.", "A suggestion about the future takes -லாம்.")],
        [("Meena", "ஞாயிற்றுக்கிழமை எங்கள் வீட்டுக்கு வருகிறீர்களா?", "ñāyiṟṟukkiḻamai eṅkaḷ vīṭṭukku varukiṟīrkaḷā?", "Will you come to our home on Sunday?"),
         ("Ravi", "மகிழ்ச்சியாக வருகிறேன். மாலை எத்தனை மணிக்கு?", "makiḻcciyāka varukiṟēṉ. mālai ettaṉai maṇikku?", "Gladly. What time in the evening?"),
         ("Meena", "ஆறு மணிக்கு. வந்த பிறகு காபி குடிக்கலாம்.", "āṟu maṇikku. vanta piṟaku kāpi kuṭikkalām.", "At six. After you arrive, we can have coffee."),
         ("Ravi", "சரி, குடும்பத்துடன் வருகிறேன்.", "sari, kuṭumpattuṭaṉ varukiṟēṉ.", "All right, I will come with my family.")],
        "Invitation worksheet", [
            ("Invite and accept.", ["will you come to our home tomorrow?", "gladly, what time in the evening?"], ["நாளை எங்கள் வீட்டுக்கு வருகிறீர்களா?", "மகிழ்ச்சியாக வருகிறேன், மாலை எத்தனை மணிக்கு?"]),
            ("Sequence the visit.", ["after you arrive, we can eat together", "I will come with my family"], ["வந்த பிறகு சேர்ந்து சாப்பிடலாம்", "குடும்பத்துடன் வருகிறேன்"]),
        ])),
]

THIRD["B1"] = [
    ("ta-b1-u1", "ta-b1-l7", _spec_lesson(
        "அறிகுறி மாறிய விதம்",
        "Describe how a symptom changed over several days and explain what you tried. "
        "முதலில் / அதன் பிறகு / இப்போது orders the account; குறைந்தது and அதிகரித்தது "
        "report change, while ...தால் gives the reason for seeking care.",
        [("அறிகுறி", "aṟikuṟi", "symptom", "noun"),
         ("முதலில்", "mutalil", "at first", "adverb"),
         ("குறைதல்", "kuṟaital", "to decrease", "verb"),
         ("அதிகரித்தல்", "atikarittal", "to increase", "verb"),
         ("தொடர்ந்து", "toṭarntu", "continuously, in succession", "adverb")],
        "A symptom timeline", "முதலில் ... · அதன் பிறகு ... · இப்போது ... · ...தால் மருத்துவரைச் சந்தித்தேன்",
        "Use முதலில், அதன் பிறகு, and இப்போது to make a timeline. For a change, "
        "காய்ச்சல் குறைந்தது; வலி அதிகரித்தது. A reason can be attached with -தால்: "
        "வலி அதிகரித்ததால் மருத்துவரைச் சந்தித்தேன்.",
        [("முதலில் இருமல் இருந்தது; அதன் பிறகு காய்ச்சல் குறைந்தது.", "mutalil irumal iruntatu; ataṉ piṟaku kāyccal kuṟaintatu.", "At first I had a cough; after that the fever decreased."),
         ("வலி தொடர்ந்து இருந்ததால் நான் மீண்டும் வந்தேன்.", "vali toṭarntu iruntatāl nāṉ mīṇṭum vantēṉ.", "Because the pain continued, I came back."),
         ("இப்போது சுவாசம் சீராக இருக்கிறது.", "ippōtu cuvāsam cīrāka irukkiṟatu.", "Now my breathing is steady.")],
        [("வலி அதிகரித்தது நான் மீண்டும் வந்தேன்.", "வலி அதிகரித்ததால் நான் மீண்டும் வந்தேன்.", "Join the cause to the result with -தால்."),
         ("முதலில் காய்ச்சல் குறைந்தது, இப்போது இருந்தது.", "முதலில் காய்ச்சல் அதிகமாக இருந்தது; இப்போது குறைந்தது.", "Use a clear contrast between the earlier and current state.")],
        [("மருத்துவர்", "மருந்துக்குப் பிறகு என்ன மாற்றம்?", "maruntukkup piṟaku eṉṉa māṟṟam?", "What changed after the medicine?"),
         ("நோயாளி", "முதலில் காய்ச்சல் குறைந்தது; இருமல் தொடர்ந்து இருந்தது.", "mutalil kāyccal kuṟaintatu; irumal toṭarntu iruntatu.", "At first the fever decreased; the cough continued."),
         ("மருத்துவர்", "இப்போது சுவாசம் எப்படி இருக்கிறது?", "ippōtu cuvāsam eppaṭi irukkiṟatu?", "How is your breathing now?"),
         ("நோயாளி", "சீராக இருக்கிறது, ஆனால் வலி அதிகரித்ததால் மீண்டும் வந்தேன்.", "cīrāka irukkiṟatu, āṉāl vali atikarittatāl mīṇṭum vantēṉ.", "It is steady, but I came back because the pain increased.")],
        "Health timeline worksheet", [
            ("Report the change.", ["at first the fever decreased", "the cough continued"], ["முதலில் காய்ச்சல் குறைந்தது", "இருமல் தொடர்ந்து இருந்தது"]),
            ("Explain the visit.", ["because the pain increased, I came back", "now my breathing is steady"], ["வலி அதிகரித்ததால் நான் மீண்டும் வந்தேன்", "இப்போது சுவாசம் சீராக இருக்கிறது"]),
        ])),
    ("ta-b1-u2", "ta-b1-l8", _spec_lesson(
        "ஆய்வும் சுற்றுச்சூழலும்",
        "Present a small observation from a school or neighbourhood project without "
        "turning one measurement into a universal claim. Compare two days with -ஐ "
        "விட; அதே நேரத்தில் introduces a balancing point, and எனவே marks a reasoned "
        "conclusion.",
        [("அளவீடு", "aḷavīṭu", "measurement", "noun"),
         ("மாதிரி", "mātiri", "sample", "noun"),
         ("ஒப்பிடுதல்", "oppiṭutal", "to compare", "verb"),
         ("முடிவு", "muṭivu", "conclusion", "noun"),
         ("அதே நேரத்தில்", "atē nērattil", "at the same time, however", "connector")],
        "Comparing observations", "செவ்வாயை விட ... · அதே நேரத்தில் ... · எனவே ...",
        "Use -ஐ விட after the comparison point: செவ்வாயை விட புதன்கிழமை வெப்பம் "
        "குறைந்தது. அதே நேரத்தில் signals a balancing observation. End with a "
        "proportionate claim: எனவே இந்த மாதிரியில் ...; it is not yet a claim about "
        "every neighbourhood.",
        [("இந்த மாதிரியில் நீரின் அளவு கடந்த வாரத்தை விடக் குறைந்தது.", "inta mātiriyil nīriṉ aḷavu kaṭanta vārattaiviṭak kuṟaintatu.", "In this sample, the water level was lower than last week."),
         ("அதே நேரத்தில், மழை அளவும் குறைந்திருந்தது.", "atē nērattil, maḻai aḷavum kuṟaintiruntatu.", "At the same time, the rainfall measurement had also fallen."),
         ("எனவே இன்னொரு இடத்திலும் அளவிட வேண்டும்.", "eṉavē iṉṉoru iṭattilum aḷaviṭa vēṇṭum.", "Therefore we need to measure at another location too.")],
        [("ஒரு மாதிரி எல்லா ஊருக்கும் பொருந்தும்.", "இந்த ஒரு மாதிரி எல்லா ஊருக்கும் பொருந்தாது.", "One sample cannot support a universal conclusion."),
         ("செவ்வாயை விட புதன் குறைந்தது.", "செவ்வாயை விட புதன்கிழமை அளவு குறைந்தது.", "Name what decreased so the comparison is complete.")],
        [("மாணவர்", "எங்கள் குழு இரண்டு இடங்களில் நீரை அளந்தது.", "eṅkaḷ kuḻu iraṇṭu iṭaṅkaḷil nīrai aḷantatu.", "Our group measured water in two locations."),
         ("ஆசிரியர்", "என்ன வேறுபாடு தெரிந்தது?", "eṉṉa vēṟupāṭu terintatu?", "What difference did you find?"),
         ("மாணவர்", "ஒரு இடத்தில் அளவு குறைந்தது; அதே நேரத்தில் அங்கு மழையும் குறைவு.", "oru iṭattil aḷavu kuṟaintatu; atē nērattil aṅku maḻaiyum kuṟaivu.", "At one location the level fell; at the same time, rainfall there was lower too."),
         ("ஆசிரியர்", "எனவே முடிவை எல்லா இடங்களுக்கும் பொதுவாக்காதீர்கள்.", "eṉavē muṭivai ellā iṭaṅkaḷukkum potuvākkātīrkaḷ.", "Therefore do not generalise the conclusion to every location.")],
        "Observation worksheet", [
            ("Compare the observations.", ["in this sample, the water level was lower than last week", "rainfall had also fallen"], ["இந்த மாதிரியில் நீரின் அளவு கடந்த வாரத்தை விடக் குறைந்தது", "மழை அளவும் குறைந்திருந்தது"]),
            ("Limit the conclusion.", ["therefore we need to measure another location too", "do not generalise it to every location"], ["எனவே இன்னொரு இடத்திலும் அளவிட வேண்டும்", "எல்லா இடங்களுக்கும் பொதுவாக்காதீர்கள்"]),
        ])),
    ("ta-b1-u3", "ta-b1-l9", _spec_lesson(
        "ஊர் விழாவுக்கான ஏற்பாடு",
        "Coordinate a community event when people have different schedules. முன்மொழிவு "
        "names a proposal; யாருக்கு வசதி? checks access, and ... என்றால் conditions "
        "the plan. Offer two alternatives before asking the group to decide.",
        [("ஏற்பாடு", "ēṟpāṭu", "arrangement", "noun"),
         ("முன்மொழிவு", "muṉmoḻivu", "proposal", "noun"),
         ("பங்கேற்பாளர்", "paṅkēṟpāḷar", "participant", "noun"),
         ("மாற்று நாள்", "māṟṟu nāḷ", "alternative date", "phrase"),
         ("வசதி", "vacati", "convenience, suitability", "noun")],
        "Making a shared plan", "நாள் ... என்றால் ... · யாருக்கு வசதி? · இல்லையெனில் ...",
        "A condition with -என்றால் lets a group test a date: சனிக்கிழமை என்றால் "
        "யாருக்கு வசதி? இல்லையெனில் introduces the fallback. A suggestion with "
        "...லாமா? invites agreement rather than issuing an order.",
        [("சனிக்கிழமை என்றால் பலருக்கு வசதியாக இருக்கும்.", "caṉikkiḻamai eṉṟāl palarukku vacatiyāka irukkum.", "If it is Saturday, it will be convenient for many people."),
         ("இல்லையெனில் ஞாயிற்றுக்கிழமை மாற்று நாளாக இருக்கலாம்.", "illaiyeṉil ñāyiṟṟukkiḻamai māṟṟu nāḷāka irukkalām.", "Otherwise, Sunday could be an alternative date."),
         ("மாலை நேரம் குழந்தைகளுக்கும் வசதியாக இருக்கும்.", "mālai nēram kuḻantaikaḷukkum vacatiyāka irukkum.", "An evening time will be convenient for the children too.")],
        [("சனிக்கிழமை என்றால் யாருக்கு வசதியாக?", "சனிக்கிழமை என்றால் யாருக்கு வசதியாக இருக்கும்?", "Complete the condition with a finite verb."),
         ("இல்லை என்றால் ஞாயிற்றுக்கிழமை.", "இல்லையெனில் ஞாயிற்றுக்கிழமை மாற்று நாளாக இருக்கலாம்.", "Use இல்லையெனில் to introduce the fallback clearly.")],
        [("Meena", "விழாவை எந்த நாளில் நடத்தலாம்?", "viḻāvai enta nāḷil naṭattalām?", "On which day can we hold the festival?"),
         ("Ravi", "சனிக்கிழமை என்றால் பலருக்கு வசதி.", "caṉikkiḻamai eṉṟāl palarukku vacati.", "Saturday would suit many people."),
         ("Meena", "வேலை செய்பவர்களுக்கு மாலை நேரம் நல்லதா?", "vēlai ceypavarkaḷukku mālai nēram nallatā?", "Would evening suit the people who work?"),
         ("Ravi", "ஆம். இல்லையெனில் ஞாயிற்றுக்கிழமை காலை பார்க்கலாம்.", "ām. illaiyeṉil ñāyiṟṟukkiḻamai kālai pārkkalām.", "Yes. Otherwise, we can consider Sunday morning.")],
        "Community event worksheet", [
            ("Propose a date.", ["if it is Saturday, it will suit many people", "would evening suit the people who work?"], ["சனிக்கிழமை என்றால் பலருக்கு வசதியாக இருக்கும்", "வேலை செய்பவர்களுக்கு மாலை நேரம் நல்லதா?"]),
            ("Offer a fallback.", ["otherwise, Sunday could be an alternative date", "we can consider Sunday morning"], ["இல்லையெனில் ஞாயிற்றுக்கிழமை மாற்று நாளாக இருக்கலாம்", "ஞாயிற்றுக்கிழமை காலை பார்க்கலாம்"]),
        ])),
]

THIRD["B2"] = [
    ("ta-b2-u1", "ta-b2-l7", _spec_lesson(
        "மருத்துவ நடைமுறையை விளக்குதல்",
        "Explain a clinic procedure and its reason without sounding abrupt. Passive "
        "forms in -ப்படுகிறது focus on the procedure, while ஏனெனில் gives an explicit "
        "reason. Use முதலில் / அதன் பின்னர் to make the sequence auditable.",
        [("நடைமுறை", "naṭaimuṟai", "procedure", "noun"),
         ("ஒப்புதல்", "opp utal", "consent, approval", "noun"),
         ("மாதிரி", "mātiri", "specimen, sample", "noun"),
         ("பரிசோதனை", "paricōtaṉai", "test, examination", "noun"),
         ("விளக்கம்", "viḷakkam", "explanation", "noun")],
        "Procedural passive", "முதலில் ... செய்யப்படுகிறது · அதன் பின்னர் ... · ஏனெனில் ...",
        "In the procedural passive, the action is foregrounded: மாதிரி பரிசோதிக்கப்படுகிறது. "
        "The staff member can be named with -ஆல் if relevant, but the order should "
        "remain clear. ஏனெனில் introduces the reason for collecting consent first.",
        [("முதலில் உங்கள் ஒப்புதல் பதிவு செய்யப்படுகிறது.", "mutalil uṅkaḷ opputal pativu ceyyappaṭukiṟatu.", "First, your consent is recorded."),
         ("அதன் பின்னர் மாதிரி ஆய்வகத்திற்கு அனுப்பப்படுகிறது.", "ataṉ piṉṉar mātiri āyvakattiṟku aṉuppappaṭukiṟatu.", "After that, the sample is sent to the laboratory."),
         ("முடிவை மருத்துவர் விளக்குவார், ஏனெனில் ஒவ்வொரு முடிவும் தனித்தனியாகப் பார்க்கப்பட வேண்டும்.", "muṭivai maruttuvar viḷakkuvār, ēṉeṉil ovvoru muṭivum taṉittaṉiyākap pārkkappaṭa vēṇṭum.", "The doctor will explain the result, because each result must be considered individually.")],
        [("மாதிரி ஆய்வகத்திற்கு அனுப்புகிறது.", "மாதிரி ஆய்வகத்திற்கு அனுப்பப்படுகிறது.", "Use the passive ending when the actor is not the focus."),
         ("முதலில் மாதிரி அனுப்பப்படுகிறது, பின்னர் ஒப்புதல் பெறப்படுகிறது.", "முதலில் ஒப்புதல் பெறப்படுகிறது; பின்னர் மாதிரி அனுப்பப்படுகிறது.", "The order must reflect consent before the procedure.")],
        [("செவிலியர்", "முதலில் என்ன செய்யப்படும்?", "mutalil eṉṉa ceyyappaṭum?", "What will be done first?"),
         ("நோயாளி", "என் ஒப்புதல் பதிவு செய்யப்படும் என்று சொன்னார்கள்.", "eṉ opputal pativu ceyyappaṭum eṉṟu coṉṉārkaḷ.", "They said that my consent would be recorded."),
         ("செவிலியர்", "ஆம். அதன் பின்னர் மாதிரி எடுக்கப்படும்; முடிவை மருத்துவர் விளக்குவார்.", "ām. ataṉ piṉṉar mātiri eṭukkappaṭum; muṭivai maruttuvar viḷakkuvār.", "Yes. After that a sample will be taken; the doctor will explain the result."),
         ("நோயாளி", "சரி. எந்தக் கேள்வியையும் கேட்கலாமா?", "sari. entak kēḷviyaiyum kēṭkalāmā?", "All right. May I ask any question?")],
        "Procedure worksheet", [
            ("Put the steps in order.", ["first, your consent is recorded", "after that, the sample is sent to the laboratory"], ["முதலில் உங்கள் ஒப்புதல் பதிவு செய்யப்படுகிறது", "அதன் பின்னர் மாதிரி ஆய்வகத்திற்கு அனுப்பப்படுகிறது"]),
            ("Explain the safeguard.", ["each result must be considered individually", "the doctor will explain the result"], ["ஒவ்வொரு முடிவும் தனித்தனியாகப் பார்க்கப்பட வேண்டும்", "முடிவை மருத்துவர் விளக்குவார்"]),
        ])),
    ("ta-b2-u2", "ta-b2-l8", _spec_lesson(
        "தரவின் எல்லையும் முடிவும்",
        "Evaluate a claim about weather or water using a small dataset. Distinguish "
        "what the figures show from what they do not establish. மட்டும் limits a "
        "claim; இருப்பினும் introduces a counterpoint, and இதனால் must have a "
        "traceable antecedent.",
        [("தரவு", "taravu", "data", "noun"),
         ("போக்கு", "pōkku", "trend", "noun"),
         ("வரம்பு", "varampu", "limit", "noun"),
         ("உறுதி", "uṟuti", "certainty", "noun"),
         ("இருப்பினும்", "iruppiṉum", "nevertheless", "connector")],
        "Claim and evidence", "தரவு ... காட்டுகிறது · இருப்பினும் ... · இதனால் ... நிரூபிக்கப்படவில்லை",
        "State the measured observation first. A count from one station மட்டும் shows "
        "that station's reading, not the whole region. இருப்பினும் can introduce a "
        "qualified comparison; இதனால் refers to the evidence already named, and "
        "cannot carry a stronger conclusion than that evidence supports.",
        [("இந்தத் தரவு ஒரு நிலையத்தில் மழை குறைந்ததைக் காட்டுகிறது.", "intat taravu oru nilaiyattil maḻai kuṟaintataik kāṭṭukiṟatu.", "These data show that rain fell at one station."),
         ("இருப்பினும், மற்ற நிலையங்களிலும் அதே போக்கு இருந்தது.", "iruppiṉum, maṟṟa nilaiyaṅkaḷilum atē pōkku iruntatu.", "Nevertheless, the same trend was present at the other stations too."),
         ("இதனால் வறட்சி உறுதியாகிவிட்டது என்று கூற முடியாது.", "itaṉāl vaṟaṭci uṟutiyāki viṭṭatu eṉṟu kūṟa muṭiyātu.", "This does not let us say that drought has been established with certainty.")],
        [("ஒரு நிலையத் தரவு முழுப் பகுதியை நிரூபிக்கிறது.", "ஒரு நிலையத்தின் தரவு அந்த நிலையத்தைப் பற்றிய முடிவையே ஆதரிக்கிறது.", "One station's data cannot by itself establish a region-wide claim."),
         ("இதனால் என்று சொல்லி புதிய ஆதாரமில்லாத முடிவைச் சேர்த்தார்.", "இதனால் என்று சொல்லும் முடிவு முன் கூறிய ஆதாரத்திலிருந்து வர வேண்டும்.", "A causal connector needs evidence that supports its conclusion.")],
        [("ஆய்வாளர்", "முதன்மை முடிவு என்ன?", "mut aṉmai muṭivu eṉṉa?", "What is the main result?"),
         ("பகுப்பாய்வாளர்", "ஒரு நிலையத்தில் மழை குறைந்தது; மூன்றில் அது அதிகரித்தது.", "oru nilaiyattil maḻai kuṟaintatu; mūṉṟil atu atikarittatu.", "Rain fell at one station; it increased at three."),
         ("ஆய்வாளர்", "அப்படியானால், ஒரே பிராந்தியப் போக்கைச் சொல்ல முடியாது.", "appaṭiyāṉāl, orē pirāntiyap pōkkaic colla muṭiyātu.", "Then we cannot claim one regional trend."),
         ("பகுப்பாய்வாளர்", "சரி. நிலையங்களின் வேறுபாட்டை அறிக்கையில் குறிப்பிடுகிறேன்.", "sari. nilaiyaṅkaḷiṉ vēṟupāṭṭai aṟikkaiyil kuṟippiṭukiṟēṉ.", "Right. I will note the differences between stations in the report.")],
        "Evidence worksheet", [
            ("Report the evidence.", ["the data show less rain at one station", "at three stations it increased"], ["ஒரு நிலையத்தில் மழை குறைந்ததைத் தரவு காட்டுகிறது", "மூன்று நிலையங்களில் அது அதிகரித்தது"]),
            ("Limit the claim.", ["we cannot claim one regional trend", "the report will note differences between stations"], ["ஒரே பிராந்தியப் போக்கைச் சொல்ல முடியாது", "நிலையங்களின் வேறுபாட்டை அறிக்கையில் குறிப்பிடுவேன்"]),
        ])),
    ("ta-b2-u3", "ta-b2-l9", _spec_lesson(
        "குழுக் கூட்டத்தில் சமரசம்",
        "Mediate a disagreement about a shared space. Paraphrase each proposal before "
        "responding, and distinguish an objection to the plan from a judgement about "
        "the people. ... என்று கூறினார் attributes a position; அதற்குப் பதிலாக "
        "offers an alternative without erasing the concern.",
        [("கருத்து வேறுபாடு", "karuttu vēṟupāṭu", "disagreement", "noun"),
         ("சமரசம்", "camaracam", "compromise", "noun"),
         ("முன்னுரிமை", "muṉṉurimai", "priority", "noun"),
         ("பரிந்துரை", "parinturai", "recommendation", "noun"),
         ("அதற்குப் பதிலாக", "ataṟkup patilāka", "instead, in its place", "connector")],
        "Attributing and mediating", "A ... வேண்டும் என்று கூறினார் · அதற்குப் பதிலாக ... · இரு தரப்பும் ...",
        "Attribute a request with என்று கூறினார், then restate its reason fairly. A "
        "counterproposal can begin அதற்குப் பதிலாக. End by naming the shared criterion "
        "— access, quiet, or cost — rather than labelling one group unreasonable.",
        [("ஒரு தரப்பு மாலை நேரத்தை முன்னுரிமை என்றது; மற்றொரு தரப்பு அமைதியை விரும்பியது.", "oru tarappu mālai nērat tai muṉṉurimai eṉṟatu; maṟṟoru tarappu amaitiyai virumpiyatu.", "One group prioritised evening access; the other wanted quiet."),
         ("அதற்குப் பதிலாக, இடத்தை இரு நேரங்களாகப் பகிரலாம்.", "ataṟkup patilāka, iṭattai iru nēraṅkaḷākap pakiralām.", "Instead, we can share the space across two time slots."),
         ("இரு தரப்புக்கும் ஏற்ற அட்டவணையை முதலில் சோதிப்போம்.", "iru tarappukkum ēṟṟa aṭṭavaṇaiyai mutalil cōtip pōm.", "Let us first test a schedule that works for both groups.")],
        [("அவர்கள் அமைதியை விரும்பினார்.", "அவர்கள் அமைதியை விரும்பினர்.", "Plural அவர்கள் takes plural agreement in this sentence."),
         ("அதற்குப் பதிலாக, அவர்கள் கோரிக்கை தவறு.", "அதற்குப் பதிலாக, மாற்று நேரத்தை முன்மொழியலாம்.", "A mediator offers an alternative, not a dismissal of the people.")],
        [("தலைவர்", "இரு குழுக்களின் கோரிக்கைகளையும் முதலில் கேட்போம்.", "iru kuḻukkaḷiṉ kōrikkaikaḷaiyum mutalil kēṭpōm.", "Let us first hear both groups' requests."),
         ("அயலவர்", "மாலை நேரம் எங்களுக்கு வேண்டும் என்று கூறினோம்.", "mālai nēram eṅkaḷukku vēṇṭum eṉṟu kūṟiṉōm.", "We said that we need the evening slot."),
         ("தலைவர்", "மற்றவர்கள் அமைதியை விரும்புகிறார்கள்; அதற்குப் பதிலாக அட்டவணை அமைக்கலாமா?", "maṟṟavarkaḷ amaitiyai virumpukiṟārkaḷ; ataṟkup patilāka aṭṭavaṇai amaikkalāmā?", "The others want quiet; could we make a schedule instead?"),
         ("அயலவர்", "இரு தரப்புக்கும் ஏற்ற நேரம் என்றால் முயற்சி செய்யலாம்.", "iru tarappukkum ēṟṟa nēram eṉṟāl muyaṟci ceyyalām.", "If there is a time that works for both groups, we can try it.")],
        "Mediation worksheet", [
            ("Attribute each view.", ["we said that we need the evening slot", "the others want quiet"], ["மாலை நேரம் எங்களுக்கு வேண்டும் என்று கூறினோம்", "மற்றவர்கள் அமைதியை விரும்புகிறார்கள்"]),
            ("Offer a shared test.", ["instead, we can share the space across two time slots", "let us first test a schedule"], ["அதற்குப் பதிலாக, இடத்தை இரு நேரங்களாகப் பகிரலாம்", "அட்டவணையை முதலில் சோதிப்போம்"]),
        ])),
]

THIRD["C1"] = [
    ("ta-c1-u1", "ta-c1-l7", _spec_lesson(
        "பொது சுகாதார அறிவிப்பு",
        "Draft an advisory that separates established guidance from local uncertainty. "
        "பரிந்துரைக்கப்படுகிறது gives an impersonal recommendation; இருப்பினும் "
        "marks a limit, and ... என்றால் என்ற நிபந்தனை makes the audience and "
        "circumstances explicit.",
        [("அறிவிப்பு", "aṟivippu", "advisory, notice", "noun"),
         ("பரிந்துரை", "parinturai", "recommendation", "noun"),
         ("வெளிப்பாடு", "veḷippāṭu", "exposure", "noun"),
         ("ஆதார நிலை", "ātāra nilai", "state of the evidence", "phrase"),
         ("தனிநபர்", "taṉiṉapar", "individual", "noun")],
        "Advice with a stated scope", "... பரிந்துரைக்கப்படுகிறது · இருப்பினும் ... · ... என்றால் ...",
        "The passive recommendation keeps focus on the guidance, not an unnamed "
        "authority. Name the scope before the caveat: வெளிப்புறப் பணியாளர்களுக்கு "
        "முகக்கவசம் பரிந்துரைக்கப்படுகிறது. இருப்பினும் introduces what the guidance "
        "does not settle; ... என்றால் makes an individual exception visible.",
        [("அதிகத் தூசி உள்ள பணியிடங்களில் பாதுகாப்பு முகக்கவசம் பரிந்துரைக்கப்படுகிறது.", "atika-t tūci uḷḷa paṇiyiṭaṅkaḷil pāṭukāppu mukakkavasam parinturaikkappaṭukiṟatu.", "A protective mask is recommended in workplaces with high dust."),
         ("இருப்பினும், தனிநபரின் உடல்நிலையைப் பொறுத்து ஆலோசனை மாறலாம்.", "iruppiṉum, taṉiṉapariṉ uṭalnilaiyaip poṟuttu ālōcaṉai māṟalām.", "Nevertheless, advice may vary depending on an individual's health."),
         ("அறிகுறிகள் நீடித்தால், மருத்துவரை நேரில் அணுகுவது பரிந்துரைக்கப்படுகிறது.", "aṟikuṟikaḷ nīṭittāl, maruttuvarai nēril aṇukuvatu parinturaikkappaṭukiṟatu.", "If symptoms persist, it is recommended to consult a doctor in person.")],
        [("எல்லோருக்கும் ஒரே ஆலோசனை கட்டாயம் பொருந்தும்.", "பொதுவான ஆலோசனை இருந்தாலும், தனிநபரின் உடல்நிலை மாறுபடலாம்.", "A general advisory should not erase relevant individual differences."),
         ("அறிகுறிகள் நீடித்தால் மருத்துவர் சந்திக்கவும்.", "அறிகுறிகள் நீடித்தால் மருத்துவரை நேரில் அணுகுவது பரிந்துரைக்கப்படுகிறது.", "Use the respectful construction and mark the doctor as the object." )],
        [("தொகுப்பாளர்", "இந்த அறிவிப்பு யாருக்காக எழுதப்படுகிறது?", "inta aṟivippu yārukkāka eḻutappaṭukiṟatu?", "Who is this advisory written for?"),
         ("நிபுணர்", "தூசி அதிகமுள்ள இடங்களில் பணிபுரிபவர்களுக்காக.", "tūci atikam uḷḷa iṭaṅkaḷil paṇipuripavarkaḷukkāka.", "For people working in places with heavy dust."),
         ("தொகுப்பாளர்", "அப்படியானால், எல்லோருக்கும் பொருந்தும் என்று எழுத வேண்டாம்.", "appaṭiyāṉāl, ellōrukkum poruntum eṉṟu eḻuta vēṇṭām.", "Then do not write that it applies to everyone."),
         ("நிபுணர்", "சரி. அறிகுறிகள் நீடித்தால் மருத்துவரை அணுகுமாறு சேர்க்கிறேன்.", "sari. aṟikuṟikaḷ nīṭittāl maruttuvarai aṇukumāṟu cērkkiṟēṉ.", "Right. I will add that people should consult a doctor if symptoms persist.")],
        "Advisory worksheet", [
            ("State the scoped recommendation.", ["a protective mask is recommended in dusty workplaces", "advice may vary with an individual's health"], ["தூசி உள்ள பணியிடங்களில் பாதுகாப்பு முகக்கவசம் பரிந்துரைக்கப்படுகிறது", "தனிநபரின் உடல்நிலையைப் பொறுத்து ஆலோசனை மாறலாம்"]),
            ("Add the condition.", ["if symptoms persist, consult a doctor in person", "do not write that it applies to everyone"], ["அறிகுறிகள் நீடித்தால் மருத்துவரை நேரில் அணுகுவது பரிந்துரைக்கப்படுகிறது", "எல்லோருக்கும் பொருந்தும் என்று எழுத வேண்டாம்"]),
        ])),
    ("ta-c1-u2", "ta-c1-l8", _spec_lesson(
        "நீர்வள அறிக்கையை ஒருங்கிணைத்தல்",
        "Synthesize observations from a local tank and a rainfall record. ஒப்பீட்டளவில் "
        "signals a relative comparison; அதேவேளை holds two findings together, and "
        "முடிவாக gives a conclusion that does not outrun the stated sample.",
        [("நீர்வளம்", "nīrvaḷam", "water resource", "noun"),
         ("நிலத்தடி நீர்", "nilattaṭi nīr", "groundwater", "phrase"),
         ("பருவமழை", "paruvamaḻai", "seasonal monsoon", "noun"),
         ("ஒப்பீட்டளவில்", "oppīṭṭaḷavil", "comparatively", "adverb"),
         ("முடிவாக", "muṭivāka", "in conclusion", "connector")],
        "Synthesis without overclaim", "ஒருபுறம் ... · அதேவேளை ... · ஒப்பீட்டளவில் ... · முடிவாக ...",
        "Use ஒருபுறம் and மறுபுறம் to keep evidence streams distinct. அதேவேளை "
        "notes a concurrent factor rather than a causal link. ஒப்பீட்டளவில் is "
        "comparative, not absolute; முடிவாக should name the spatial and temporal "
        "scope of the recommendation.",
        [("ஒருபுறம், நீர்த்தேக்கத்தின் அளவு உயர்ந்தது; மறுபுறம், நிலத்தடி நீர் மாறவில்லை.", "orupuṟam, nīrttēkkattiṉ aḷavu uyarntatu; maṟupuṟam, nilattaṭi nīr māṟavillai.", "On one hand, the reservoir level rose; on the other, groundwater did not change."),
         ("அதேவேளை, பருவமழை வழக்கத்தை விடக் குறைவாகப் பதிவானது.", "atēvēḷai, paruvamaḻai vaḻakkattai viṭak kuṟaivākap pativāṉatu.", "At the same time, seasonal rainfall was recorded below its usual level."),
         ("முடிவாக, இந்தப் பகுதியின் தரவை அடுத்த பருவத்திலும் சேகரிக்க வேண்டும்.", "muṭivāka, intap pakutiyiṉ taravai aṭutta paruvattilum cēkarikka vēṇṭum.", "In conclusion, data from this area should also be collected in the next season.")],
        [("மழை குறைந்ததால் நிலத்தடி நீர் உயர்ந்தது என்று தரவு நிரூபிக்கிறது.", "மழையும் நிலத்தடி நீரும் இம்மாதிரியில் வேறுபட்ட போக்கைக் காட்டுகின்றன.", "Do not infer a causal relationship from two measurements alone."),
         ("இந்தப் பகுதி எல்லா மாவட்டங்களையும் பிரதிநிதித்துவப்படுத்துகிறது.", "இந்தப் பகுதியின் முடிவை மற்ற மாவட்டங்களில் தனியாகச் சரிபார்க்க வேண்டும்.", "Limit a local sample to its actual geographic scope.")],
        [("ஆய்வாளர்", "நீர்த்தேக்கமும் கிணறுகளும் ஒரே போக்கைக் காட்டினவா?", "nīrttēkkamum kiṇaṟukaḷum orē pōkkaik kāṭṭiṉavā?", "Did the reservoir and the wells show the same trend?"),
         ("பகுப்பாய்வாளர்", "இல்லை. நீர்த்தேக்கம் உயர்ந்தது; கிணறுகளில் மாற்றம் இல்லை.", "illai. nīrttēkkam uyarntatu; kiṇaṟukaḷil māṟṟam illai.", "No. The reservoir rose; there was no change in the wells."),
         ("ஆய்வாளர்", "அதேவேளை, மழைப் பதிவு வழக்கத்தைவிடக் குறைவு.", "atēvēḷai, maḻaip pativu vaḻakkattai viṭak kuṟaivu.", "At the same time, the rainfall record is below normal."),
         ("பகுப்பாய்வாளர்", "அப்படியானால், காரணத்தை உறுதிப்படுத்த அடுத்த பருவமும் தேவை.", "appaṭiyāṉāl, kāraṇattai uṟutippaṭutta aṭutta paruvamum tēvai.", "Then we need the next season too to establish the cause.")],
        "Water evidence worksheet", [
            ("Keep findings distinct.", ["the reservoir level rose", "groundwater did not change"], ["நீர்த்தேக்கத்தின் அளவு உயர்ந்தது", "நிலத்தடி நீர் மாறவில்லை"]),
            ("Write a scoped conclusion.", ["data from this area should be collected next season too", "the cause needs more evidence"], ["இந்தப் பகுதியின் தரவை அடுத்த பருவத்திலும் சேகரிக்க வேண்டும்", "காரணத்திற்கு மேலும் ஆதாரம் தேவை"]),
        ])),
    ("ta-c1-u3", "ta-c1-l9", _spec_lesson(
        "வாய்மொழி வரலாற்றைப் பதிவு செய்தல்",
        "Record an oral-history interview without turning memory into an unqualified "
        "archive fact. The narrator's own claim takes என்று நினைவுகூர்கிறார்; the "
        "editor distinguishes memory, corroboration, and editorial framing. "
        "அவருடைய சொற்களில் preserves attribution.",
        [("வாய்மொழி வரலாறு", "vāymoḻi varalāṟu", "oral history", "phrase"),
         ("நினைவுகூர்தல்", "niṉaivukūṟtal", "to recall", "verb"),
         ("சான்று", "cāṉṟu", "evidence", "noun"),
         ("பதிப்பாசிரியர்", "patipp āciriyar", "editor", "noun"),
         ("அவருடைய சொற்களில்", "avaruṭaiya coṟkaḷil", "in their own words", "phrase")],
        "Attributing remembered events", "... என்று நினைவுகூர்கிறார் · அவருடைய சொற்களில் · தனி ஆதாரம் தேவை",
        "The reporting verb marks the source: அவர் ... என்று நினைவுகூர்கிறார். "
        "அவருடைய சொற்களில் introduces a quotation or paraphrase; it does not "
        "independently verify the event. A careful note says where corroboration "
        "exists and where memory remains the source.",
        [("அவர் அந்தச் சந்திப்பை 1978-ஆம் ஆண்டு நடந்ததாக நினைவுகூர்கிறார்.", "avar antac cantippai 1978-ām āṇṭu naṭantatāka niṉaivukūrkiṟār.", "They recall that the meeting took place in 1978."),
         ("அவருடைய சொற்களில், அந்த முடிவு ஒரே நாளில் எடுக்கப்படவில்லை.", "avaruṭaiya coṟkaḷil, anta muṭivu orē nāḷil eṭukkappaṭavillai.", "In their words, that decision was not made in a single day."),
         ("தேதியை உறுதிப்படுத்த தனி ஆவணச் சான்று தேவை.", "tētiyai uṟutippaṭutta taṉi āvaṇac cāṉṟu tēvai.", "A separate documentary source is needed to confirm the date.")],
        [("அவர் சொன்னதால் அந்தத் தேதி உறுதி.", "அவர் அந்தத் தேதியை நினைவுகூர்கிறார்; அதைத் தனி ஆவணத்தால் சரிபார்க்க வேண்டும்.", "A remembered date should remain attributed until corroborated."),
         ("பதிப்பாசிரியர் கூறினார், அவர் நினைவுகூர்கிறார்.", "பதிப்பாசிரியர், அவர் அந்த நிகழ்வை நினைவுகூர்கிறார் என்று பதிவு செய்தார்.", "Use என்று to mark the reported clause and keep speaker roles clear.")],
        [("தொகுப்பாளர்", "இந்தச் சந்திப்பின் தேதிக்கு ஆவணம் இருக்கிறதா?", "intac cantippiṉ tētikku āvaṇam irukkiṟatā?", "Is there a document for the date of this meeting?"),
         ("ஆய்வாளர்", "இல்லை. அவர் 1978 என்று நினைவுகூர்கிறார்; பதிவேட்டில் தேதி இல்லை.", "illai. avar 1978 eṉṟu niṉaivukūrkiṟār; pativēṭṭil tēti illai.", "No. They recall 1978; there is no date in the register."),
         ("தொகுப்பாளர்", "அப்படியானால், அந்தக் கூற்றை அவருடைய நினைவாகக் குறிக்கிறோம்.", "appaṭiyāṉāl, antak kūṟṟai avaruṭaiya niṉaivākak kuṟikkiṟōm.", "Then we will mark the claim as their recollection."),
         ("ஆய்வாளர்", "சரி; உறுதிப்படுத்தப்படாததை உறுதியான உண்மையாக எழுதமாட்டோம்.", "sari; uṟutippaṭuttappaṭātatai uṟutiyāṉa uṇmaiyāka eḻutamāṭṭōm.", "Right; we will not write what is unverified as established fact.")],
        "Oral history worksheet", [
            ("Attribute the memory.", ["they recall that the meeting took place in 1978", "in their words, the decision was not made in one day"], ["அந்தச் சந்திப்பு 1978-ஆம் ஆண்டு நடந்ததாக அவர் நினைவுகூர்கிறார்", "அவருடைய சொற்களில், அந்த முடிவு ஒரே நாளில் எடுக்கப்படவில்லை"]),
            ("State the evidence limit.", ["a separate document is needed to confirm the date", "we will not present an unverified claim as fact"], ["தேதியை உறுதிப்படுத்த தனி ஆவணச் சான்று தேவை", "உறுதிப்படுத்தப்படாததை உண்மையாக எழுதமாட்டோம்"]),
        ])),
]

THIRD["C2"] = [
    ("ta-c2-u1", "ta-c2-l7", _spec_lesson(
        "ஆய்வுப் பரிந்துரையின் நிபந்தனைகள்",
        "Write a specialist recommendation that makes its evidence and decision rule "
        "visible. ஏற்கெனவே and இதுவரை distinguish prior work from the current record; "
        "unless a condition is met, state what action should wait. A conditional "
        "recommendation is not a refusal to decide.",
        [("பரிந்துரைக் குழு", "parinturaik kuḻu", "recommendation panel", "phrase"),
         ("முன்நிபந்தனை", "muṉnipant aṉai", "precondition", "noun"),
         ("மறுஆய்வு", "maṟu āyvu", "review, re-examination", "noun"),
         ("போதுமான", "pōtumāṉa", "sufficient", "adjective"),
         ("தற்காலிகமாக", "taṟkālikamāka", "provisionally", "adverb")],
        "Conditional recommendations", "... உறுதிப்படுத்தப்பட்டால் ... · உறுதிப்படுத்தப்படும்வரை ... கூடாது",
        "A recommendation can be stated with a clear threshold: தரவு மறுஆய்வில் "
        "உறுதிப்படுத்தப்பட்டால் ... . Until then, ... உறுதிப்படுத்தப்படும்வரை "
        "முடிவை மாற்றக்கூடாது. Distinguish a temporary pause from a permanent "
        "rejection, and identify who owns the next review.",
        [("மறுஆய்வில் முடிவு உறுதிப்படுத்தப்பட்டால், நடைமுறையைத் தொடரலாம்.", "maṟuāyvil muṭivu uṟutippaṭuttappaṭṭāl, naṭaimuṟaiyait toṭaralām.", "If the result is confirmed in review, the procedure may continue."),
         ("தனி மாதிரி கிடைக்கும் வரை இறுதி பரிந்துரை வெளியிடப்படாது.", "taṉi mātiri kiṭaikkum varai iṟuti parinturai veḷiyiṭappaṭātu.", "A final recommendation will not be issued until an independent sample is available."),
         ("இடைநிலை முடிவை தற்காலிகமாகப் பதிவு செய்து, அடுத்தக் கூட்டத்தில் மீண்டும் மதிப்பிட வேண்டும்.", "iṭainilai muṭivai taṟkālikamākap pativu ceytu, aṭuttak kūṭṭattil mīṇṭum matippiṭa vēṇṭum.", "The interim result should be recorded provisionally and reassessed at the next meeting.")],
        [("மீளாய்வு இல்லாமல் முடிவு உறுதியானது.", "மீளாய்வில் முடிவு உறுதிப்படுத்தப்பட்டால் மட்டுமே அதை இறுதியாகக் கருதலாம்.", "State the review threshold before treating a result as final."),
         ("தற்காலிக இடைநிறுத்தம் நிரந்தர மறுப்பு.", "தற்காலிக இடைநிறுத்தம் அடுத்த ஆய்வு வரை மட்டுமே.", "A provisional pause is time-bounded, not a permanent rejection.")],
        [("தலைவர்", "பரிந்துரையை இன்றே வெளியிடலாமா?", "parinturaiyai iṉṟē veḷiyiṭalāmā?", "Can we issue the recommendation today?"),
         ("நிபுணர்", "தனி மாதிரி கிடைக்கும் வரை இறுதி முடிவு வேண்டாம்.", "taṉi mātiri kiṭaikkum varai iṟuti muṭivu vēṇṭām.", "Not a final decision until the independent sample is available."),
         ("தலைவர்", "அப்படியானால், இடைநிலை முடிவைத் தெளிவாகக் குறிக்கிறோம்.", "appaṭiyāṉāl, iṭainilai muṭivait teḷivākak kuṟikkiṟōm.", "Then we will clearly mark it as an interim result."),
         ("நிபுணர்", "ஆம்; அடுத்த கூட்டத்தில் மறுஆய்வு பொறுப்பாளரையும் நியமிக்க வேண்டும்.", "ām; aṭutta kūṭṭattil maṟu āyvu poṟuppāḷaraiyum niyamikka vēṇṭum.", "Yes; at the next meeting we should also appoint who is responsible for the review.")],
        "Recommendation worksheet", [
            ("Set the condition.", ["if the result is confirmed in review, the procedure may continue", "a final recommendation waits for an independent sample"], ["மறுஆய்வில் முடிவு உறுதிப்படுத்தப்பட்டால் நடைமுறையைத் தொடரலாம்", "தனி மாதிரி கிடைக்கும் வரை இறுதி பரிந்துரை வெளியிடப்படாது"]),
            ("Name the status.", ["record the interim result provisionally", "reassess it at the next meeting"], ["இடைநிலை முடிவைத் தற்காலிகமாகப் பதிவு செய்யுங்கள்", "அடுத்தக் கூட்டத்தில் மீண்டும் மதிப்பிடுங்கள்"]),
        ])),
    ("ta-c2-u2", "ta-c2-l8", _spec_lesson(
        "காலநிலை மாதிரியின் கருதுகோள்கள்",
        "Explain what a climate model assumes and why a projection is not a "
        "prediction with a fixed date. Modelled outcomes depend on scenarios and "
        "inputs; ஆகவே marks an inference, not a direct observation, and என்றாலும் "
        "introduces uncertainty without dismissing the result.",
        [("கருதுகோள்", "karutukōḷ", "assumption", "noun"),
         ("சூழ்நிலை", "cūḻnilai", "scenario, context", "noun"),
         ("கணிப்பு", "kaṇippu", "projection, estimate", "noun"),
         ("நிச்சயமின்மை", "niccayamiṉmai", "uncertainty", "noun"),
         ("உள்ளீடு", "uḷḷīṭu", "input", "noun")],
        "Projection and uncertainty", "உள்ளீடு மாறினால் ... · ஆகவே ... எனப் பொருள் கொள்ளக் கூடாது · என்றாலும் ...",
        "Name the scenario and the input before interpreting the output. ஆகவே "
        "introduces a conclusion; the phrase கணிப்பு எனப் பொருள் கொள்ளக் கூடாது "
        "prevents a projection from being reported as an exact forecast. என்றாலும் "
        "allows uncertainty to be stated without denying the model's useful range.",
        [("உமிழ்வு உள்ளீடு மாறினால் மாதிரியின் கணிப்பும் மாறும்.", "umiḻvu uḷḷīṭu māṟiṉāl mātiriyiṉ kaṇippum māṟum.", "If the emissions input changes, the model's projection changes too."),
         ("ஆகவே 2050-ஆம் ஆண்டின் ஒரு எண்ணை உறுதியான கணிப்பாகப் பொருள் கொள்ளக் கூடாது.", "ākavē 2050-ām āṇṭiṉ oru eṇṇai uṟutiyāṉa kaṇippākap poruḷ koḷḷak kūṭātu.", "Therefore a single figure for 2050 should not be read as a certain prediction."),
         ("நிச்சயமின்மை இருந்தாலும், பல சூழ்நிலைகளை ஒப்பிடுவது பயனுள்ளது.", "niccayamiṉmai iruntālum, pala cūḻnilaikaḷai oppiṭuvatu payaṉuḷḷatu.", "Even with uncertainty, comparing several scenarios is useful.")],
        [("இந்த மாதிரி 2050-ஆம் ஆண்டின் வெப்பநிலையைத் துல்லியமாகச் சொல்கிறது.", "இந்த மாதிரி சில கருதுகோள்களின் கீழ் சாத்தியமான வெப்பநிலை வரம்பைக் காட்டுகிறது.", "A scenario model gives conditional ranges, not a fixed exact value."),
         ("நிச்சயமின்மை இருப்பதால் எந்த முடிவும் பயனற்றது.", "நிச்சயமின்மை இருந்தாலும், ஒப்பிடப்பட்ட சூழ்நிலைகள் முடிவெடுக்க உதவுகின்றன.", "Uncertainty limits precision but does not erase all decision value.")],
        [("ஆய்வாளர்", "இந்த எண்ணை நாளைய வெப்பநிலையாகச் சொல்லலாமா?", "inta eṇṇai nāḷaiya veppanilaiyākac collalāmā?", "Can we state this figure as tomorrow's temperature?"),
         ("பகுப்பாய்வாளர்", "இல்லை; இது ஒரு நீண்டகாலச் சூழ்நிலைக் கணிப்பு.", "illai; itu oru nīṇṭakālac cūḻnilaik kaṇippu.", "No; it is a long-term scenario projection."),
         ("ஆய்வாளர்", "உள்ளீடுகள் மாறினால் வரம்பும் மாறுமா?", "uḷḷīṭukaḷ māṟiṉāl varampum māṟumā?", "If the inputs change, will the range change too?"),
         ("பகுப்பாய்வாளர்", "ஆம். அதனால் கருதுகோள்களை முடிவுடன் சேர்த்து வெளியிடுகிறோம்.", "ām. ataṉāl karutukōḷkaḷai muṭivuṭaṉ cērttu veḷiyiṭukiṟōm.", "Yes. That is why we publish the assumptions with the result.")],
        "Model worksheet", [
            ("State the dependency.", ["if the emissions input changes, the projection changes", "the assumptions must be published with the result"], ["உமிழ்வு உள்ளீடு மாறினால் கணிப்பும் மாறும்", "கருதுகோள்களை முடிவுடன் சேர்த்து வெளியிட வேண்டும்"]),
            ("Keep the claim conditional.", ["this is a long-term scenario projection", "compare several scenarios despite uncertainty"], ["இது நீண்டகாலச் சூழ்நிலைக் கணிப்பு", "நிச்சயமின்மை இருந்தாலும் பல சூழ்நிலைகளை ஒப்பிடுவது பயனுள்ளது"]),
        ])),
    ("ta-c2-u3", "ta-c2-l9", _spec_lesson(
        "மொழிநடையும் அடையாளமும்",
        "Edit a public essay about Tamil without treating one register as the only "
        "authentic voice. Distinguish the writer's chosen voice from a reader's "
        "expectation, and explain why changing register also changes audience and "
        "power. ... என்று மட்டும் கூறுவது reduces a claim; இல்லை என்பதைக் காட்டிலும் "
        "... என்பதை வலியுறுத்துகிறது frames a contrast.",
        [("மொழிநடை", "moḻinaṭai", "register, style", "noun"),
         ("வாசகர் வட்டம்", "vācakar vaṭṭam", "readership", "phrase"),
         ("அடையாளம்", "aṭaiyāḷam", "identity", "noun"),
         ("எதிர்பார்ப்பு", "etirpārppu", "expectation", "noun"),
         ("வலியுறுத்துதல்", "valiyuṟuttutal", "to emphasise", "verb")],
        "Contrast without essentialising", "... என்று மட்டும் கூறுவது ... · இல்லை என்பதைக் காட்டிலும் ... என்பதை வலியுறுத்துகிறது",
        "A precise editorial does not reduce a writer to a register. State the narrow "
        "claim first; then contrast it with the wider issue: இது சொல் தேர்வு மட்டும் "
        "அல்ல; வாசகர் வட்டத்தையும் தீர்மானிக்கிறது. Use என்று மட்டும் to identify "
        "what a claim omits, and ... என்பதை வலியுறுத்துகிறது to name the alternative "
        "that the evidence actually supports.",
        [("இது பேச்சுத் தமிழை மட்டும் பற்றிய விவாதம் அல்ல; யாருடைய குரல் அச்சில் இடம் பெறுகிறது என்பதையும் பற்றியது.", "itu pēccut tamiḻai maṭṭum paṟṟiya vivātam alla; yāruṭaiya kural accil iṭam peṟukiṟatu eṉpataiyum paṟṟiyatu.", "This is not only a debate about spoken Tamil; it is also about whose voice appears in print."),
         ("எழுத்தாளர் ஒரு நடையைத் தேர்ந்தெடுக்கிறார்; வாசகர் அதில் அடையாளத்தை வாசிக்கிறார்.", "eḻuttāḷar oru naṭaiyait tērnteṭukkiṟār; vācakar atil aṭaiyāḷattai vācikkiṟār.", "The writer chooses a register; the reader reads identity into it."),
         ("ஆகவே திருத்தம் என்பது பிழை நீக்கம் மட்டுமல்ல, குரலைப் பற்றிய முடிவும் ஆகும்.", "ākavē tiruttam eṉpatu piḻai nīkkam maṭṭumalla, kuralaip paṟṟiya muṭivum ākum.", "Therefore editing is not only the removal of errors; it is also a decision about voice.")],
        [("ஒரே நடையே உண்மையான தமிழ்.", "ஒரு குறிப்பிட்ட நடையை மட்டுமே உண்மையான தமிழ் என்று கூற முடியாது.", "Do not turn a register preference into an absolute claim about authenticity."),
         ("திருத்தம் பிழையை மட்டும் நீக்குகிறது; குரலை மாற்றாது.", "திருத்தம் பிழையை நீக்குவதோடு, குரலையும் மாற்றக்கூடும்.", "Editing can alter voice as well as correct errors; acknowledge both." )],
        [("தொகுப்பாளர்", "இந்தக் கட்டுரை எந்தக் கேள்வியை முன்வைக்கிறது?", "intak kaṭṭurai entak kēḷviyai muṉvaikkiṟatu?", "What question does this essay raise?"),
         ("எழுத்தாளர்", "ஒரு குறிப்பிட்ட நடையை மட்டுமே ஏன் சரியானது எனக் கருதுகிறோம்?", "oru kuṟippiṭṭa naṭaiyai maṭṭumē ēṉ cariyāṉatu eṉak karutukiṟōm?", "Why do we treat only one register as correct?"),
         ("தொகுப்பாளர்", "சரி; மொழிநடை வாசகர் வட்டத்தையும் மாற்றுகிறது என்பதைச் சேர்க்கவும்.", "sari; moḻinaṭai vācakar vaṭṭattaiyum māṟṟukiṟatu eṉpataic cērkkavum.", "Good; add that register also changes the readership."),
         ("எழுத்தாளர்", "அப்படியானால், முடிவில் குரலின் தேர்வை விளக்குகிறேன்.", "appaṭiyāṉāl, muṭivil kuraliṉ tērvai viḷakkukiṟēṉ.", "Then I will explain the choice of voice in the conclusion.")],
        "Editing worksheet", [
            ("Refine the claim.", ["one register is not the only authentic Tamil", "editing can change voice as well as remove errors"], ["ஒரு நடையை மட்டுமே உண்மையான தமிழ் என்று கூற முடியாது", "திருத்தம் பிழையை நீக்குவதோடு குரலையும் மாற்றக்கூடும்"]),
            ("Name the consequence.", ["register also changes the readership", "explain the choice of voice in the conclusion"], ["மொழிநடை வாசகர் வட்டத்தையும் மாற்றுகிறது", "முடிவில் குரலின் தேர்வை விளக்குகிறேன்"]),
        ])),
]

HALFSTEPS["A1+"] = {
    "native": NATIVE,
    "title": "Tamil A1+ — Kiosk, home and time",
    "goals": [
        "Buy a small amount at a street stall and ask the price politely",
        "Give a simple address, show a room, and welcome a visitor",
        "Ask the time and agree on a day and hour to meet",
    ],
    "units": [
        {"id": "A1+-U1", "title": "கடைத்தெரு", "lessons": [
            _spec_lesson(
                "பழக்கடையில்",
                "Point to fruit, ask for a small quantity, and ask the price. இந்தப் பழம் "
                "names the item in front of you; கொஞ்சம் softens the amount, and "
                "கொடுங்கள் makes the request respectful.",
                [("பழக்கடை", "paḻakkaṭai", "fruit stall", "noun"), ("வாழைப்பழம்", "vāḻaippaḻam", "banana", "noun"), ("கொஞ்சம்", "koñcam", "a little", "quantity"), ("புதியது", "putiyatu", "fresh", "adjective"), ("கொடுங்கள்", "koṭuṅkaḷ", "please give", "verb")],
                "Pointing and asking", "இந்தப் பழம் · கொஞ்சம் ... கொடுங்கள் · எவ்வளவு?",
                "இந்தப் பழம் points to the item. கொஞ்சம் or அரை கிலோ gives the amount, "
                "and கொடுங்கள் is a respectful plural imperative. Put the price question "
                "after the request: இது எவ்வளவு?",
                [("கொஞ்சம் பழம் கொடுங்கள்.", "koñcam paḻam koṭuṅkaḷ.", "Please give me some fruit."), ("இரண்டு வாழைப்பழங்கள் வேண்டும்.", "iraṇṭu vāḻaippaḻaṅkaḷ vēṇṭum.", "I need two bananas."), ("இது புதியதா? விலை எவ்வளவு?", "itu putiyatā? vilai evvaḷavu?", "Is this fresh? What is the price?")],
                [("இந்தப் பழம் கொடு.", "இந்தப் பழம் கொடுங்கள்.", "Use the respectful request with a shopkeeper."), ("இரண்டு வாழைப்பழம் வேண்டும்.", "இரண்டு வாழைப்பழங்கள் வேண்டும்.", "Use the plural noun form with a counted plural in written Tamil.")],
                [("கவி", "இந்த வாழைப்பழம் புதியதா?", "inta vāḻaippaḻam putiyatā?", "Are these bananas fresh?"), ("கடைக்காரர்", "ஆம், இன்று காலையில் வந்தது.", "ām, iṉṟu kālaiyil vantatu.", "Yes, they arrived this morning."), ("கவி", "இரண்டு கொடுங்கள். விலை எவ்வளவு?", "iraṇṭu koṭuṅkaḷ. vilai evvaḷavu?", "Please give me two. What is the price?"), ("கடைக்காரர்", "முப்பது ரூபாய்.", "muppatu rūpāy.", "Thirty rupees.")],
                "Fruit stall worksheet", [("Point and ask.", ["are these bananas fresh?", "please give me two"], ["இந்த வாழைப்பழம் புதியதா?", "இரண்டு கொடுங்கள்"]), ("Ask the price.", ["what is the price?", "thirty rupees"], ["விலை எவ்வளவு?", "முப்பது ரூபாய்"])]),
            _spec_lesson(
                "எடை மற்றும் விலை",
                "Ask for a measured amount and check the total before paying. எடை is the "
                "weight; அரை கிலோ is half a kilo; மொத்தம் introduces the total. The "
                "number and measure come before the item being bought.",
                [("எடை", "eṭai", "weight", "noun"), ("அரை கிலோ", "arai kilō", "half a kilo", "measure"), ("மொத்தம்", "mottam", "total", "noun"), ("காசு", "kācu", "money", "noun"), ("மீதி", "mīti", "change remaining", "noun")],
                "Asking for a measure", "அரை கிலோ + item · மொத்தம் எவ்வளவு? · ... ரூபாய் கொடுங்கள்",
                "Put the amount first: அரை கிலோ வெங்காயம். Ask the total with மொத்தம் "
                "எவ்வளவு? When handing over money, say ... ரூபாய் கொடுங்கள்; the shopkeeper "
                "can answer with the change, மீதி.",
                [("அரை கிலோ வெங்காயம் வேண்டும்.", "arai kilō veṅkāyam vēṇṭum.", "I need half a kilo of onions."), ("மொத்தம் எண்பது ரூபாய்.", "mottam eṇpatu rūpāy.", "The total is eighty rupees."), ("நூறு ரூபாய் கொடுத்தால், இருபது ரூபாய் மீதி.", "nūṟu rūpāy koṭuttāl, irupatu rūpāy mīti.", "If you give one hundred rupees, the change is twenty rupees.")],
                [("வெங்காயம் அரை கிலோ வேண்டும்.", "அரை கிலோ வெங்காயம் வேண்டும்.", "The measure comes before the item."), ("மொத்தம் எண்பது ரூபாய்கள்.", "மொத்தம் எண்பது ரூபாய்.", "In this price expression ரூபாய் stays uninflected.")],
                [("அருண்", "மாம்பழம் அரை கிலோ வேண்டும்.", "māmpaḻam arai kilō vēṇṭum.", "I need half a kilo of mangoes."), ("விற்பனையாளர்", "சரி. இன்னும் ஏதாவது?", "sari. iṉṉum ētāvatu?", "All right. Anything else?"), ("அருண்", "இல்லை. மொத்தம் எவ்வளவு?", "illai. mottam evvaḷavu?", "No. What is the total?"), ("விற்பனையாளர்", "எண்பது ரூபாய். நூறு கொடுத்தால் இருபது மீதி.", "eṇpatu rūpāy. nūṟu koṭuttāl irupatu mīti.", "Eighty rupees. If you give one hundred, twenty is the change.")],
                "Price worksheet", [("Order the measure.", ["I need half a kilo of onions", "I need half a kilo of mangoes"], ["அரை கிலோ வெங்காயம் வேண்டும்", "அரை கிலோ மாம்பழம் வேண்டும்"]), ("Calculate the change.", ["the total is eighty rupees", "if you give one hundred, twenty is the change"], ["மொத்தம் எண்பது ரூபாய்", "நூறு கொடுத்தால் இருபது ரூபாய் மீதி"])]),
            _spec_lesson(
                "பையைப் பற்றி கேட்பது",
                "Finish a shop visit by asking for a bag, refusing one politely, and checking "
                "whether an item is available. வேண்டாம் declines an offer; இருந்தால் "
                "conditionals are useful when a specific size or colour is needed.",
                [("பை", "pai", "bag", "noun"), ("தேவை", "tēvai", "need", "noun"), ("வேண்டாம்", "vēṇṭām", "no need, do not want", "phrase"), ("இருக்கிறதா", "irukkiṟatā", "is there?", "question"), ("நிறம்", "niṟam", "colour", "noun")],
                "Accepting and declining", "பை வேண்டுமா? · வேண்டாம் · ... இருந்தால் ...",
                "A question ending in -ஆ? invites a simple answer. Say பை வேண்டாம் to "
                "decline one, or ஆம், வேண்டும் to accept. For a condition, நிறம் இருந்தால் "
                "கொடுங்கள் means 'if that colour is available, please give it'.",
                [("பை வேண்டுமா?", "pai vēṇṭumā?", "Would you like a bag?"), ("வேண்டாம், நன்றி. என் பை இருக்கிறது.", "vēṇṭām, naṉṟi. eṉ pai irukkiṟatu.", "No, thank you. I have my bag."), ("சிவப்பு நிறம் இருந்தால் கொடுங்கள்.", "civappu niṟam iruntāl koṭuṅkaḷ.", "If red is available, please give it.")],
                [("வேண்டும் இல்லை.", "வேண்டாம்.", "Use வேண்டாம் to decline an offer."), ("சிவப்பு நிறம் இருந்தால் கொடு.", "சிவப்பு நிறம் இருந்தால் கொடுங்கள்.", "Keep the polite imperative in a shop exchange.")],
                [("மீனா", "பை வேண்டுமா?", "pai vēṇṭumā?", "Would you like a bag?"), ("கடைக்காரர்", "வேண்டாம், நன்றி. என் பை இருக்கிறது.", "vēṇṭām, naṉṟi. eṉ pai irukkiṟatu.", "No, thank you. I have my bag."), ("மீனா", "இந்தப் பழம் வேறு நிறத்தில் இருக்கிறதா?", "intap paḻam vēṟu niṟattil irukkiṟatā?", "Is this fruit available in another colour?"), ("கடைக்காரர்", "சிவப்பு நிறம் இருந்தால் கொடுக்கிறேன்.", "civappu niṟam iruntāl koṭukkiṟēṉ.", "If the red ones are available, I will give them to you.")],
                "Closing the purchase worksheet", [("Decline the bag.", ["no, thank you", "I have my bag"], ["வேண்டாம், நன்றி", "என் பை இருக்கிறது"]), ("Ask about availability.", ["is this available in another colour?", "if red is available, please give it"], ["இது வேறு நிறத்தில் இருக்கிறதா?", "சிவப்பு நிறம் இருந்தால் கொடுங்கள்"])]),
        ]},
        {"id": "A1+-U2", "title": "வீடும் முகவரியும்", "lessons": [
            _spec_lesson(
                "வீட்டு முகவரி",
                "Give a simple address and ask how to find a house. தெரு and எண் identify "
                "the street and number; அருகில் locates a landmark. Tamil places the "
                "location phrase before the verb இருக்கிறது.",
                [("முகவரி", "mukavari", "address", "noun"), ("தெரு", "teru", "street", "noun"), ("எண்", "eṇ", "number", "noun"), ("அருகில்", "arukil", "near", "postposition"), ("கட்டிடம்", "kaṭṭiṭam", "building", "noun")],
                "Locating a home", "எண் + தெரு · ... அருகில் · எங்கே இருக்கிறது?",
                "The house number comes before the street: எண் 12, பூங்கா தெரு. "
                "அருகில் follows the landmark: பள்ளிக்கு அருகில். Ask எங்கே இருக்கிறது? "
                "and answer with the location before the verb.",
                [("என் வீட்டு முகவரி எண் 12, பூங்கா தெரு.", "eṉ vīṭṭu mukavari eṇ 12, pūṅkā teru.", "My home address is number 12, Poonga Street."), ("அது பள்ளிக்கு அருகில் இருக்கிறது.", "atu paḷḷikku arukil irukkiṟatu.", "It is near the school."), ("பேருந்து நிறுத்தம் எங்கே இருக்கிறது?", "pēruntu niṟuttam eṅkē irukkiṟatu?", "Where is the bus stop?")],
                [("என் முகவரி தெரு 12.", "என் முகவரி எண் 12, பூங்கா தெரு.", "Give the house number before the street name."), ("பள்ளி அருகில் அது இருக்கிறது.", "அது பள்ளிக்கு அருகில் இருக்கிறது.", "Use -க்கு with the landmark before அருகில்.")],
                [("கவி", "உங்கள் வீட்டு முகவரி என்ன?", "uṅkaḷ vīṭṭu mukavari eṉṉa?", "What is your home address?"), ("அருண்", "எண் 12, பூங்கா தெரு.", "eṇ 12, pūṅkā teru.", "Number 12, Poonga Street."), ("கவி", "பேருந்து நிறுத்தம் எங்கே இருக்கிறது?", "pēruntu niṟuttam eṅkē irukkiṟatu?", "Where is the bus stop?"), ("அருண்", "பள்ளிக்கு அருகில் இருக்கிறது.", "paḷḷikku arukil irukkiṟatu.", "It is near the school.")],
                "Address worksheet", [("Give the address.", ["my home address is number 12, Poonga Street", "it is near the school"], ["என் வீட்டு முகவரி எண் 12, பூங்கா தெரு", "அது பள்ளிக்கு அருகில் இருக்கிறது"]), ("Ask for a landmark.", ["where is the bus stop?", "where is the school?"], ["பேருந்து நிறுத்தம் எங்கே இருக்கிறது?", "பள்ளி எங்கே இருக்கிறது?"])]),
            _spec_lesson(
                "வீட்டின் அறைகள்",
                "Show a guest where things are in a home. அறை is a room; சமையலறை is the "
                "kitchen. இங்கே / அங்கே point to near and far, while உள்ளே and வெளியே "
                "describe inside and outside.",
                [("அறை", "aṟai", "room", "noun"), ("சமையலறை", "camaiyalaṟai", "kitchen", "noun"), ("வாசல்", "vāc al", "entrance, doorway", "noun"), ("உள்ளே", "uḷḷē", "inside", "adverb"), ("வெளியே", "veḷiyē", "outside", "adverb")],
                "Showing a room", "இங்கே ... இருக்கிறது · ... உள்ளே · ... வெளியே",
                "Put the thing before இருக்கிறது: சமையலறை உள்ளே இருக்கிறது. இங்கே points "
                "to a nearby place; அங்கே points farther away. Add -இல் to a room for "
                "'in the room': அறையில்.",
                [("இங்கே உட்காரும் அறை இருக்கிறது.", "iṅkē uṭkārum aṟai irukkiṟatu.", "Here is the sitting room."), ("சமையலறையில் தண்ணீர் இருக்கிறது.", "camaiyalaṟaiyil taṇṇīr irukkiṟatu.", "There is water in the kitchen."), ("செருப்பை வெளியே வையுங்கள்.", "ceruppai veḷiyē vaiyuṅkaḷ.", "Please leave the shoes outside.")],
                [("சமையலறை உள்ளே தண்ணீர் இருக்கிறது.", "சமையலறையில் தண்ணீர் இருக்கிறது.", "Use -இல் to mark 'in the kitchen'."), ("செருப்பை வெளியே வை.", "செருப்பை வெளியே வையுங்கள்.", "Mark the object and use a respectful request.")],
                [("மீனா", "வீட்டுக்குள் வாருங்கள்.", "vīṭṭukkuḷ vāruṅkaḷ.", "Please come inside."), ("கவி", "நன்றி. உட்காரும் அறை எங்கே?", "naṉṟi. uṭkārum aṟai eṅkē?", "Thank you. Where is the sitting room?"), ("மீனா", "இங்கே இருக்கிறது. தண்ணீர் சமையலறையில் இருக்கிறது.", "iṅkē irukkiṟatu. taṇṇīr camaiyalaṟaiyil irukkiṟatu.", "It is here. The water is in the kitchen."), ("கவி", "செருப்பை வெளியே வைக்கிறேன்.", "ceruppai veḷiyē vaik kiṟēṉ.", "I will leave my shoes outside.")],
                "Rooms worksheet", [("Show the guest.", ["here is the sitting room", "the water is in the kitchen"], ["இங்கே உட்காரும் அறை இருக்கிறது", "தண்ணீர் சமையலறையில் இருக்கிறது"]), ("Ask and answer.", ["where is the kitchen?", "please come inside"], ["சமையலறை எங்கே?", "வீட்டுக்குள் வாருங்கள்"])]),
            _spec_lesson(
                "விருந்தினரை வரவேற்பது",
                "Welcome a visitor, offer a seat, and ask whether they would like water or tea. "
                "வாருங்கள் and உட்காருங்கள் are respectful invitations; வேண்டுமா? asks "
                "about preference, and நன்றி closes the offer naturally.",
                [("விருந்தினர்", "viruntiṉar", "guest", "noun"), ("வரவேற்பு", "varavēṟpu", "welcome", "noun"), ("உட்காருதல்", "uṭkāṟutal", "to sit", "verb"), ("தண்ணீர்", "taṇṇīr", "water", "noun"), ("தேநீர்", "tēnīr", "tea", "noun")],
                "Welcoming a guest", "... வாருங்கள் · ... உட்காருங்கள் · தேநீர் வேண்டுமா?",
                "Use the respectful plural imperative for a guest: வாருங்கள், உட்காருங்கள். "
                "An offer ends with வேண்டுமா?; the answer can be வேண்டும் or வேண்டாம், "
                "நன்றி. The guest may say கொஞ்சம், please, to accept a small amount.",
                [("வீட்டிற்கு வாருங்கள்.", "vīṭṭiṟku vāruṅkaḷ.", "Please come home."), ("இங்கே உட்காருங்கள்.", "iṅkē uṭkāruṅkaḷ.", "Please sit here."), ("தேநீர் வேண்டுமா? — வேண்டும், நன்றி.", "tēnīr vēṇṭumā? — vēṇṭum, naṉṟi.", "Would you like tea? — Yes, thank you.")],
                [("உட்கார் இங்கே.", "இங்கே உட்காருங்கள்.", "Use the respectful invitation for a guest."), ("தேநீர் வேண்டுமா? — வேண்டும் இல்லை.", "தேநீர் வேண்டுமா? — வேண்டாம், நன்றி.", "Decline with வேண்டாம்.")],
                [("மீனா", "வணக்கம், உள்ளே வாருங்கள்.", "vaṇakkam, uḷḷē vāruṅkaḷ.", "Hello, please come in."), ("அருண்", "நன்றி. இங்கே உட்காரலாமா?", "naṉṟi. iṅkē uṭkāralāmā?", "Thank you. May I sit here?"), ("மீனா", "நிச்சயமாக. தண்ணீர் வேண்டுமா, தேநீர் வேண்டுமா?", "niccayamāka. taṇṇīr vēṇṭumā, tēnīr vēṇṭumā?", "Certainly. Would you like water or tea?"), ("அருண்", "தண்ணீர் மட்டும், நன்றி.", "taṇṇīr maṭṭum, naṉṟi.", "Just water, thank you.")],
                "Welcome worksheet", [("Welcome the visitor.", ["hello, please come in", "please sit here"], ["வணக்கம், உள்ளே வாருங்கள்", "இங்கே உட்காருங்கள்"]), ("Offer and respond.", ["would you like tea?", "just water, thank you"], ["தேநீர் வேண்டுமா?", "தண்ணீர் மட்டும், நன்றி"])]),
        ]},
        {"id": "A1+-U3", "title": "நேரமும் நாளும்", "lessons": [
            _spec_lesson(
                "எத்தனை மணி?",
                "Ask the time and say when an activity begins. மணி is the hour, and மணிக்கு "
                "marks 'at' a clock time. Half past uses ...ரை; say the time first, then "
                "the event.",
                [("மணி", "maṇi", "hour, o'clock", "noun"), ("காலையில்", "kālaiyil", "in the morning", "time"), ("மாலையில்", "mālaiyil", "in the evening", "time"), ("அரை", "arai", "half", "quantity"), ("தொடங்குதல்", "toṭaṅkutal", "to begin", "verb")],
                "Clock time", "மூன்று மணிக்கு · மூன்றரை மணி · ... மணிக்கு தொடங்கும்",
                "Attach -க்கு to the hour for 'at': மூன்று மணிக்கு. Half past three is "
                "மூன்றரை மணி. Put the time before the event, and use தொடங்கும் for a "
                "scheduled start.",
                [("இப்போது மணி மூன்று.", "ippōtu maṇi mūṉṟu.", "It is three o'clock now."), ("வகுப்பு மூன்றரை மணிக்கு தொடங்கும்.", "vakuppu mūṉṟarai maṇikku toṭaṅkum.", "The class starts at half past three."), ("காலை எட்டு மணிக்கு சந்திப்போம்.", "kālai eṭṭu maṇikku cantippōm.", "We will meet at eight in the morning.")],
                [("வகுப்பு மூன்று மணியில் தொடங்கும்.", "வகுப்பு மூன்று மணிக்குத் தொடங்கும்.", "Use -க்கு for an exact clock time."), ("மூன்று மணி அரை.", "மூன்றரை மணி.", "Use the combined form for half past.")],
                [("கவி", "இப்போது மணி என்ன?", "ippōtu maṇi eṉṉa?", "What time is it now?"), ("அருண்", "மூன்று மணி. வகுப்பு எப்போது?", "mūṉṟu maṇi. vakuppu eppōtu?", "Three o'clock. When is the class?"), ("கவி", "மூன்றரை மணிக்கு தொடங்கும்.", "mūṉṟarai maṇikku toṭaṅkum.", "It starts at half past three."), ("அருண்", "சரி, பத்து நிமிடம் இருக்கிறது.", "sari, patt u nimiṭam irukkiṟatu.", "All right, there are ten minutes left.")],
                "Clock worksheet", [("Say the time.", ["it is three o'clock now", "at half past three"], ["இப்போது மணி மூன்று", "மூன்றரை மணிக்கு"]), ("State the schedule.", ["the class starts at half past three", "we will meet at eight in the morning"], ["வகுப்பு மூன்றரை மணிக்கு தொடங்கும்", "காலை எட்டு மணிக்கு சந்திப்போம்"])]),
            _spec_lesson(
                "வார அட்டவணை",
                "Describe a weekly routine and ask when a person is free. வாரத்தில் இரண்டு "
                "முறை says twice a week; செவ்வாய்க்கிழமை அன்று places an event on Tuesday. "
                "Use இருக்கிறேன் / இருக்கிறீர்களா? to talk about availability.",
                [("வாரம்", "vāram", "week", "noun"), ("அட்டவணை", "aṭṭavaṇai", "schedule", "noun"), ("செவ்வாய்க்கிழமை", "cevvāy-kkiḻamai", "Tuesday", "noun"), ("முறை", "muṟai", "time, occasion", "counter"), ("காலி", "kāli", "free, unoccupied", "adjective")],
                "Weekly routine", "வாரத்தில் இரண்டு முறை · ... அன்று · உங்களுக்கு நேரம் இருக்கிறதா?",
                "Use வாரத்தில் for frequency and அன்று after a named day. To ask a polite "
                "person about availability, say உங்களுக்கு நேரம் இருக்கிறதா? The answer "
                "can be இருக்கிறது (yes) or இல்லை (no).",
                [("நான் வாரத்தில் இரண்டு முறை நூலகத்திற்குச் செல்கிறேன்.", "nāṉ vārattil iraṇṭu muṟai nūlakat tiṟkuc celkiṟēṉ.", "I go to the library twice a week."), ("செவ்வாய்க்கிழமை அன்று எனக்கு நேரம் இருக்கிறது.", "cevvāy-kkiḻamai aṉṟu eṉakku nēram irukkiṟatu.", "I am free on Tuesday."), ("உங்களுக்கு மாலை நேரம் இருக்கிறதா?", "uṅkaḷukku mālai nēram irukkiṟatā?", "Are you free in the evening?")],
                [("நான் வாரம் இரண்டு முறை செல்கிறேன்.", "நான் வாரத்தில் இரண்டு முறை செல்கிறேன்.", "Use வாரத்தில் to state a weekly frequency."), ("செவ்வாய்க்கிழமை எனக்கு நேரம் இருக்கிறார்.", "செவ்வாய்க்கிழமை எனக்கு நேரம் இருக்கிறது.", "நேரம் is singular and takes இருக்கிறது.")],
                [("மீனா", "இந்த வாரம் எப்போது சந்திக்கலாம்?", "inta vāram eppōtu cantikkalām?", "When can we meet this week?"), ("கவி", "செவ்வாய்க்கிழமை மாலை எனக்கு நேரம் இருக்கிறது.", "cevvāy-kkiḻamai mālai eṉakku nēram irukkiṟatu.", "I am free Tuesday evening."), ("மீனா", "நூலகத்தில் சந்திக்கலாமா?", "nūlakattil cantikkalāmā?", "Shall we meet at the library?"), ("கவி", "சரி. ஆறு மணிக்கு வருகிறேன்.", "sari. āṟu maṇikku varukiṟēṉ.", "All right. I will come at six.")],
                "Weekly schedule worksheet", [("State the frequency.", ["I go to the library twice a week", "I am free on Tuesday"], ["நான் வாரத்தில் இரண்டு முறை நூலகத்திற்குச் செல்கிறேன்", "செவ்வாய்க்கிழமை அன்று எனக்கு நேரம் இருக்கிறது"]), ("Arrange a meeting.", ["shall we meet at the library?", "I will come at six"], ["நூலகத்தில் சந்திக்கலாமா?", "ஆறு மணிக்கு வருகிறேன்"])]),
            _spec_lesson(
                "சந்திக்கும் நேரம்",
                "Make an appointment, confirm a place, and say what to do if you are late. "
                "முடியுமா? asks whether a time is possible; தாமதம் means a delay, and "
                "தொலைபேசியில் சொல்கிறேன் promises a call.",
                [("சந்திப்பு", "cantippu", "meeting", "noun"), ("முடியுமா", "muṭiyumā", "is it possible?", "question"), ("தாமதம்", "tāmatam", "delay", "noun"), ("இடம்", "iṭam", "place", "noun"), ("தொலைபேசியில்", "tol aipēciyil", "by phone", "adverb")],
                "Confirming an appointment", "... மணிக்கு வர முடியுமா? · ... இடத்தில் · தாமதமானால் ...",
                "Put the time before வர முடியுமா? to ask whether it works. Name the meeting "
                "place with -இல், and use தாமதமானால் (if delayed) before the plan: "
                "தொலைபேசியில் சொல்கிறேன்.",
                [("நாளை ஐந்து மணிக்கு வர முடியுமா?", "nāḷai aintu maṇikku vara muṭiyumā?", "Can you come at five tomorrow?"), ("நிலையத்தின் முன்புறத்தில் சந்திப்போம்.", "nilaiyattiṉ muṉpuṟattil cantippōm.", "We will meet in front of the station."), ("தாமதமானால் தொலைபேசியில் சொல்கிறேன்.", "tāmatamāṉāl tol aipēciyil colkiṟēṉ.", "If I am delayed, I will call.")],
                [("நாளை ஐந்து மணியில் வர முடியுமா?", "நாளை ஐந்து மணிக்கு வர முடியுமா?", "Mark the clock time with -க்கு."), ("தாமதம் என்றால் சொல்கிறேன்.", "தாமதமானால் சொல்கிறேன்.", "Use the conditional form தாமதமானால்.")],
                [("அருண்", "நாளை ஐந்து மணிக்கு வர முடியுமா?", "nāḷai aintu maṇikku vara muṭiyumā?", "Can you come at five tomorrow?"), ("மீனா", "முடியும். எங்கே சந்திப்போம்?", "muṭiyum. eṅkē cantippōm?", "Yes. Where shall we meet?"), ("அருண்", "நிலையத்தின் முன்புறத்தில்.", "nilaiyattiṉ muṉpuṟattil.", "In front of the station."), ("மீனா", "சரி. தாமதமானால் தொலைபேசியில் சொல்கிறேன்.", "sari. tāmatamāṉāl tol aipēciyil colkiṟēṉ.", "All right. If I am delayed, I will call.")],
                "Appointment worksheet", [("Confirm the time.", ["can you come at five tomorrow?", "yes, I can"], ["நாளை ஐந்து மணிக்கு வர முடியுமா?", "முடியும்"]), ("Confirm the plan.", ["we will meet in front of the station", "if I am delayed, I will call"], ["நிலையத்தின் முன்புறத்தில் சந்திப்போம்", "தாமதமானால் தொலைபேசியில் சொல்கிறேன்"])]),
        ]},
    ],
    "extra": EXTRA(
        culture=("Chennai's Metropolitan Transport Corporation publishes bus route and "
                 "stage information for everyday journeys. A first-time passenger "
                 "often needs more than a destination: which stop to board at, where "
                 "to change, and which landmark to name to the conductor. Asking "
                 "«இந்தப் பேருந்து ... போகுமா?» and confirming the stop are practical "
                 "language acts, not textbook extras. The examples here use generic "
                 "routes rather than promising a current timetable; passengers should "
                 "check the operator's live information before travelling."),
        source_url="https://mtcbus.tn.gov.in/",
        reading=("கவி முதல் முறையாகப் பேருந்தில் அலுவலகத்திற்குச் செல்கிறாள். "
                 "நிறுத்தத்தில் வழித்தடப் பலகையைப் பார்த்தாள்; அவளுக்குத் தேவையான "
                 "நிலையம் கடைசி நிறுத்தம் அல்ல. நடத்துநரிடம் «இந்தப் பேருந்து "
                 "மருத்துவமனைக்குப் போகுமா?» என்று கேட்டாள். அவர் «போகும்; "
                 "நூலகம் வந்ததும் சொல்லுங்கள்» என்றார். கவி ஏறும் இடத்தையும் "
                 "இறங்கும் இடத்தையும் கைப்பேசியில் எழுதிக்கொண்டாள். பயணம் "
                 "தொடங்கிய பிறகு, சரியான நிறுத்தத்தைத் தவறவிடுவோமோ என்ற "
                 "கவலை குறைந்தது."),
        reading_gloss=("Kavi is taking a bus to the office for the first time. At the "
                       "stop she looked at the route board; the stop she needed was "
                       "not the final one. She asked the conductor, 'Does this bus go "
                       "to the hospital?' He said, 'It does; tell me when we reach the "
                       "library.' Kavi wrote down the boarding and getting-off points "
                       "on her phone. After the journey began, her worry about missing "
                       "the right stop eased."),
        listening=("இந்தப் பேருந்து சந்தைக்குப் போகுமா? — ஆம். அடுத்த நிறுத்தத்தில் "
                   "ஏறுங்கள். — மருத்துவமனை வந்ததும் சொல்ல முடியுமா? — நிச்சயமாக, "
                   "நீங்கள் இறங்க வேண்டிய இடத்தைச் சொல்கிறேன்."),
        listening_gloss=("Does this bus go to the market? — Yes. Board at the next stop. "
                         "— Can you tell me when we reach the hospital? — Certainly, "
                         "I will tell you where you should get off."),
        voice_tag=VOICE,
        idioms=[
            ("காலில் சக்கரம் கட்டிக்கொண்டு", "with wheels tied to one's feet", "to be rushing from place to place"),
            ("வழி தெரியாமல் விழித்தல்", "to stare without knowing the way", "to be at a loss"),
            ("கண் மூடித் திறப்பதற்குள்", "before the eye closes and opens", "in the blink of an eye"),
            ("கை கொடுத்தல்", "to give a hand", "to help someone"),
            ("காதில் வாங்குதல்", "to take it in the ear", "to listen and take note"),
            ("கண்ணில் படுதல்", "to fall into the eye", "to come into view or notice"),
            ("கைக்கு எட்டுதல்", "to reach the hand", "to be within reach"),
            ("கை நிறைய", "with a hand full", "in abundance, or with one's hands full"),
            ("வாய்விட்டு அழைத்தல்", "to call out aloud", "to call openly for help"),
            ("வந்த வழியே திரும்புதல்", "to return by the way one came", "to retrace one's steps"),
        ],
        mistakes=[
            ("இந்தப் பேருந்து மருத்துவமனைக்கு போகுமா?", "இந்தப் பேருந்து மருத்துவமனைக்குப் போகுமா?", "The destination takes -க்கு; the linking sound appears before போகுமா."),
            ("நான் இறங்கு வேண்டிய இடம் எது?", "நான் இறங்க வேண்டிய இடம் எது?", "The verbal participle வேண்டிய modifies இடம்."),
            ("அடுத்த நிறுத்தத்தில் இறங்குங்கள் இல்லையா?", "அடுத்த நிறுத்தத்தில் இறங்குங்கள்.", "Do not add an unnecessary negative tag to a direct instruction."),
        ],
        task_title="பேருந்துப் பயணத் திட்டம்",
        task_instructions=("Plan a short bus journey using a current operator route map. Write "
                           "where you board, where you change if needed, one landmark to "
                           "watch for, and the stop where you get off. Ask the conductor "
                           "one respectful question and explain what you will do if you "
                           "miss the stop. Do not copy old route numbers or timetables "
                           "from this exercise: verify them before travel."),
    ),
    "test": [
        ("translate_en", "Say: I need half a kilo of onions.", "அரை கிலோ வெங்காயம் வேண்டும்."),
        ("translate_ta", "நாளை ஐந்து மணிக்கு வர முடியுமா?", "Can you come at five tomorrow?"),
        ("multiple_choice", "Which phrase politely declines a bag?", "வேண்டாம், நன்றி."),
        ("fill_in_the_blank", "என் வீட்டு முகவரி எண் 12, பூங்கா ___.", "தெரு"),
        ("word_selection", "Select the Tamil phrase for 'in the evening'.", "மாலையில்"),
        ("error_correction", "வகுப்பு மூன்று மணியில் தொடங்கும்.", "வகுப்பு மூன்று மணிக்குத் தொடங்கும்."),
        ("dialogue_completion", "பை வேண்டுமா? — ___, என் பை இருக்கிறது. (No, thank you)", "வேண்டாம், நன்றி"),
        ("matching", "Match அருகில் to its meaning.", "near"),
        ("reading_comprehension", "The bus passenger asks the conductor whether the bus goes where?", "to the hospital"),
        ("inference", "Why does Kavi record both the boarding and getting-off points?", "to avoid missing the correct stop"),
        ("main_idea", "What is the passage mainly about?", "asking for and confirming bus-stop information"),
        ("detail_identification", "Which landmark does the conductor name?", "the library"),
    ],
}

HALFSTEPS["A2+"] = {
    "native": NATIVE,
    "title": "Tamil A2+ — Metro, tickets and a hotel",
    "goals": [
        "Ask which metro line to take and where to change",
        "Buy a ticket and confirm a departure time and seat",
        "Check in at a hotel and make a polite request about the room",
    ],
    "units": [
        {"id": "A2+-U1", "title": "மெட்ரோ பயணம்", "lessons": [
            _spec_lesson(
                "மெட்ரோ நிலையத்தில்",
                "Read a station sign, identify a line, and ask which direction to travel. "
                "வழித்தடம் is a route; எந்தப் பக்கம் asks which direction, while "
                "மாற்றம் requires changing trains at a named station.",
                [("மெட்ரோ", "mēṭrō", "metro", "noun"), ("வழித்தடம்", "vaḻittaṭam", "route, line", "noun"), ("நுழைவாயில்", "nuḻaivāyil", "entrance", "noun"), ("திசை", "ticai", "direction", "noun"), ("நிலையம்", "nilaiyam", "station", "noun")],
                "Finding a line", "... செல்ல எந்த வழித்தடம்? · ... திசையில் · ... நிலையத்தில் மாற்றம்",
                "Ask for a route with எந்த வழித்தடம்? A direction can be named with "
                "... திசையில். To change trains, say ... நிலையத்தில் மாற்றம் செய்ய வேண்டும்; "
                "the place comes before the action.",
                [("விமான நிலையத்திற்குச் செல்ல எந்த வழித்தடம்?", "vimāṉa nilaiyattiṟkuc cella enta vaḻittaṭam?", "Which line goes to the airport?"), ("நீல வழித்தடத்தில் செல்லுங்கள்.", "nīla vaḻittaṭattil celluṅkaḷ.", "Take the blue line."), ("மத்திய நிலையத்தில் மாற்றம் செய்ய வேண்டும்.", "mattiya nilaiyattil māṟṟam ceyya vēṇṭum.", "You need to change at Central station.")],
                [("விமான நிலையம் செல்ல எந்த வழித்தடம்?", "விமான நிலையத்திற்குச் செல்ல எந்த வழித்தடம்?", "Mark the destination with -க்கு."), ("மத்திய நிலையம் மாற்றம் செய்ய வேண்டும்.", "மத்திய நிலையத்தில் மாற்றம் செய்ய வேண்டும்.", "Use -இல் for the station where the change takes place.")],
                [("பயணி", "விமான நிலையத்திற்குச் செல்ல எந்த வழித்தடம்?", "vimāṉa nilaiyattiṟkuc cella enta vaḻittaṭam?", "Which line goes to the airport?"), ("ஊழியர்", "நீல வழித்தடத்தில் செல்லுங்கள்.", "nīla vaḻittaṭattil celluṅkaḷ.", "Take the blue line."), ("பயணி", "மாற்றம் எங்கே செய்ய வேண்டும்?", "māṟṟam eṅkē ceyya vēṇṭum?", "Where should I change?"), ("ஊழியர்", "மத்திய நிலையத்தில். அங்கே பலகையைப் பாருங்கள்.", "mattiya nilaiyattil. aṅkē palakaiyaip pāruṅkaḷ.", "At Central. Look at the sign there.")],
                "Metro worksheet", [("Ask for the line.", ["which line goes to the airport?", "take the blue line"], ["விமான நிலையத்திற்குச் செல்ல எந்த வழித்தடம்?", "நீல வழித்தடத்தில் செல்லுங்கள்"]), ("Ask where to change.", ["where should I change?", "at Central station"], ["மாற்றம் எங்கே செய்ய வேண்டும்?", "மத்திய நிலையத்தில்"])]),
            _spec_lesson(
                "வழிமாற்றம் மற்றும் வெளியேறும் வழி",
                "Change lines, follow the signs, and choose the right exit for a landmark. "
                "வெளியேறும் வழி is the exit; அடுத்ததாக sequences the next step, and "
                "அங்கிருந்து means 'from there'. Give directions as a short sequence.",
                [("வெளியேறும் வழி", "veḷiyēṟum vaḻi", "exit", "phrase"), ("அடுத்தது", "aṭuttatu", "next", "adverb"), ("மாற்றம்", "māṟṟam", "transfer", "noun"), ("அங்கிருந்து", "aṅkiruntu", "from there", "adverb"), ("பலகை", "palakai", "signboard", "noun")],
                "Following the route", "முதலில் ... · அடுத்ததாக ... · அங்கிருந்து ...",
                "Sequence the route with முதலில் and அடுத்தது. அங்கிருந்து begins a "
                "direction from the transfer point; the destination marker -க்கு joins "
                "the place, as in அருங்காட்சியகத்திற்கு.",
                [("முதலில் பச்சை வழித்தடத்திற்கு மாற்றம் செய்யுங்கள்.", "mutalil paccai vaḻittaṭattiṟku māṟṟam ceyyuṅkaḷ.", "First transfer to the green line."), ("அடுத்ததாக இரண்டு நிலையங்கள் செல்லுங்கள்.", "aṭuttatāka iraṇṭu nilaiyaṅkaḷ celluṅkaḷ.", "Next, travel two stations."), ("அங்கிருந்து அருங்காட்சியகத்திற்கு நடந்து செல்லலாம்.", "aṅkiruntu aruṅkāṭciyakat tiṟku naṭantu cellalām.", "From there, you can walk to the museum.")],
                [("பச்சை வழித்தடம் முதலில் மாற்றம் செய்யுங்கள்.", "முதலில் பச்சை வழித்தடத்திற்கு மாற்றம் செய்யுங்கள்.", "Use -க்கு for the line you are transferring to."), ("அங்கிருந்து அருங்காட்சியகம் நடந்து செல்லலாம்.", "அங்கிருந்து அருங்காட்சியகத்திற்கு நடந்து செல்லலாம்.", "Mark the destination with -க்கு.")],
                [("பயணி", "அருங்காட்சியகத்திற்கான வெளியேறும் வழி எது?", "aruṅkāṭciyakat tiṟkāṉa veḷiyēṟum vaḻi etu?", "Which exit is for the museum?"), ("ஊழியர்", "இரண்டாவது வெளியேறும் வழி.", "iraṇṭāvatu veḷiyēṟum vaḻi.", "The second exit."), ("பயணி", "அங்கிருந்து எவ்வளவு தூரம்?", "aṅkiruntu evvaḷavu tūram?", "How far is it from there?"), ("ஊழியர்", "ஐந்து நிமிடம் நடக்க வேண்டும்.", "aintu nimiṭam naṭakka vēṇṭum.", "You need to walk for five minutes.")],
                "Transfer worksheet", [("Give the sequence.", ["first transfer to the green line", "next, travel two stations"], ["முதலில் பச்சை வழித்தடத்திற்கு மாற்றம் செய்யுங்கள்", "அடுத்ததாக இரண்டு நிலையங்கள் செல்லுங்கள்"]), ("Find the exit.", ["which exit is for the museum?", "the second exit"], ["அருங்காட்சியகத்திற்கான வெளியேறும் வழி எது?", "இரண்டாவது வெளியேறும் வழி"])]),
            _spec_lesson(
                "நிலையத்தில் காத்திருத்தல்",
                "Ask how long a train will take and explain that you are waiting for someone. "
                "இன்னும் எவ்வளவு நேரம்? asks about remaining time; வரும்வரை marks 'until "
                "someone arrives', and காத்திருக்கிறேன் names the ongoing wait.",
                [("காத்திருத்தல்", "kāttiruttal", "to wait", "verb"), ("வரை", "varai", "until", "postposition"), ("தாமதம்", "tāmatam", "delay", "noun"), ("சந்திப்பு", "cantippu", "meeting", "noun"), ("இன்னும்", "iṉṉum", "still, yet, more", "adverb")],
                "Waiting and duration", "இன்னும் எவ்வளவு நேரம்? · ... வரும்வரை காத்திருக்கிறேன்",
                "Use இன்னும் எவ்வளவு நேரம்? for the remaining duration. A verb with -வரை "
                "means 'until': ரயில் வரும்வரை. The ongoing action takes -க்கிறேன்: "
                "காத்திருக்கிறேன்.",
                [("ரயில் வரும்வரை இங்கே காத்திருக்கிறேன்.", "rayil varumvarai iṅkē kāttirukkiṟēṉ.", "I will wait here until the train comes."), ("ரயில் இன்னும் பத்து நிமிடத்தில் வரும்.", "rayil iṉṉum patt u nimiṭattil varum.", "The train will come in ten more minutes."), ("நண்பர் வரத் தாமதமாகிறது.", "naṇpar varat tāmatamākiṟatu.", "My friend is late arriving.")],
                [("ரயில் வரும் வரை இங்கே காத்திருக்கிறேன்.", "ரயில் வரும்வரை இங்கே காத்திருக்கிறேன்.", "Join the verb and -வரை in this written compound."), ("ரயில் இன்னும் பத்து நிமிடம் வரும்.", "ரயில் இன்னும் பத்து நிமிடத்தில் வரும்.", "Use -இல் to say the train will arrive in ten minutes.")],
                [("மீனா", "ரயில் எப்போது வரும்?", "rayil eppōtu varum?", "When will the train come?"), ("கவி", "இன்னும் பத்து நிமிடத்தில் வரும்.", "iṉṉum patt u nimiṭattil varum.", "It will come in ten more minutes."), ("மீனா", "நான் நண்பருக்காகக் காத்திருக்கிறேன்.", "nāṉ naṇparukkākak kāttirukkiṟēṉ.", "I am waiting for a friend."), ("கவி", "அவர் வரும்வரை இங்கே இருப்போம்.", "avar varumvarai iṅkē iruppōm.", "We will stay here until they arrive.")],
                "Waiting worksheet", [("Ask about the wait.", ["when will the train come?", "it will come in ten more minutes"], ["ரயில் எப்போது வரும்?", "இன்னும் பத்து நிமிடத்தில் வரும்"]), ("Say what you are doing.", ["I am waiting for a friend", "we will stay here until they arrive"], ["நான் நண்பருக்காகக் காத்திருக்கிறேன்", "அவர் வரும்வரை இங்கே இருப்போம்"])]),
        ]},
        {"id": "A2+-U2", "title": "சீட்டு மற்றும் பயணத் திட்டம்", "lessons": [
            _spec_lesson(
                "சீட்டு வாங்குதல்",
                "Buy a single or return ticket and confirm the destination. ஒருவழிச் சீட்டு "
                "is one way; திரும்பும் சீட்டு is return. இலிருந்து marks the starting "
                "place, and வரை the destination or endpoint.",
                [("ஒருவழிச் சீட்டு", "oruvaḻic cīṭṭu", "one-way ticket", "phrase"), ("திரும்பும் சீட்டு", "tirumpum cīṭṭu", "return ticket", "phrase"), ("இலிருந்து", "iliruntu", "from", "postposition"), ("வரை", "varai", "to, until", "postposition"), ("கட்டணம்", "kaṭṭaṇam", "fare", "noun")],
                "Ticket types", "... இலிருந்து ... வரை · ஒரு வழியா, திரும்புமா?",
                "State the start and endpoint with இலிருந்து ... வரை. The clerk may ask "
                "ஒரு வழியா, திரும்புமா?; answer ஒருவழி or திரும்பும் சீட்டு. Use "
                "எத்தனை? to ask how many tickets.",
                [("சென்னையிலிருந்து மதுரை வரை ஒரு வழிச் சீட்டு வேண்டும்.", "ceṉṉaiyiliruntu maturai varai oru vaḻic cīṭṭu vēṇṭum.", "I need a one-way ticket from Chennai to Madurai."), ("இரண்டு திரும்பும் சீட்டுகள் வேண்டும்.", "iraṇṭu tirumpum cīṭṭukaḷ vēṇṭum.", "I need two return tickets."), ("கட்டணம் எவ்வளவு?", "kaṭṭaṇam evvaḷavu?", "What is the fare?")],
                [("சென்னை முதல் மதுரை வரை ஒரு சீட்டு.", "சென்னையிலிருந்து மதுரை வரை ஒரு வழிச் சீட்டு.", "Use இலிருந்து to mark the starting station and name the ticket type."), ("இரண்டு திரும்பும் சீட்டு வேண்டும்.", "இரண்டு திரும்பும் சீட்டுகள் வேண்டும்.", "Pluralise சீட்டு for two tickets.")],
                [("பயணி", "மதுரைக்கு ஒரு வழிச் சீட்டு வேண்டும்.", "maturaikku oru vaḻic cīṭṭu vēṇṭum.", "I need a one-way ticket to Madurai."), ("ஊழியர்", "எத்தனை சீட்டுகள்?", "ettaṉai cīṭṭukaḷ?", "How many tickets?"), ("பயணி", "இரண்டு. கட்டணம் எவ்வளவு?", "iraṇṭu. kaṭṭaṇam evvaḷavu?", "Two. What is the fare?"), ("ஊழியர்", "ஒவ்வொரு சீட்டும் ஐந்நூறு ரூபாய்.", "ovvoru cīṭṭum ainnūṟu rūpāy.", "Each ticket is five hundred rupees.")],
                "Ticket worksheet", [("State the route.", ["a one-way ticket from Chennai to Madurai", "two return tickets"], ["சென்னையிலிருந்து மதுரை வரை ஒரு வழிச் சீட்டு", "இரண்டு திரும்பும் சீட்டுகள்"]), ("Ask about the cost.", ["what is the fare?", "each ticket is five hundred rupees"], ["கட்டணம் எவ்வளவு?", "ஒவ்வொரு சீட்டும் ஐந்நூறு ரூபாய்"])]),
            _spec_lesson(
                "புறப்படும் நேரமும் இருக்கையும்",
                "Check the departure time and ask whether seats are available together. "
                "புறப்படும் நேரம் is departure time; அருகருகே means side by side, and "
                "கிடைக்குமா? asks if something is available.",
                [("புறப்படும்", "puṟappaṭum", "departing", "participle"), ("நேரம்", "nēram", "time", "noun"), ("இருக்கை", "irukkai", "seat", "noun"), ("அருகருகே", "arukarukē", "side by side", "adverb"), ("கிடைக்கும்", "kiṭaikkum", "will be available", "verb")],
                "Checking seats", "ரயில் எப்போது புறப்படும்? · ... இருக்கைகள் கிடைக்குமா?",
                "Use புறப்படும் before the noun நேரம்: புறப்படும் நேரம். Ask the departure "
                "time with எப்போது? For availability, say இருக்கைகள் கிடைக்குமா? "
                "அருகருகே describes seats placed beside each other.",
                [("ரயில் மாலை ஏழு மணிக்குப் புறப்படும்.", "rayil mālai ēḻu maṇikkup puṟappaṭum.", "The train departs at seven in the evening."), ("இரண்டு இருக்கைகள் அருகருகே கிடைக்குமா?", "iraṇṭu irukkaikaḷ arukarukē kiṭaikkumā?", "Are two seats available side by side?"), ("புறப்படும் நேரத்திற்கு முன் நிலையத்திற்கு வருங்கள்.", "puṟappaṭum nērat tiṟku muṉ nilaiyattiṟku varuṅkaḷ.", "Come to the station before the departure time.")],
                [("ரயில் ஏழு மணியில் புறப்படும்.", "ரயில் ஏழு மணிக்குப் புறப்படும்.", "Use -க்கு for an exact clock time."), ("இரண்டு அருகருகே இருக்கை கிடைக்குமா?", "இரண்டு இருக்கைகள் அருகருகே கிடைக்குமா?", "Place the noun before its description and use plural agreement.")],
                [("பயணி", "ரயில் எப்போது புறப்படும்?", "rayil eppōtu puṟappaṭum?", "When does the train depart?"), ("ஊழியர்", "மாலை ஏழு மணிக்கு.", "mālai ēḻu maṇikku.", "At seven in the evening."), ("பயணி", "இரண்டு இருக்கைகள் அருகருகே கிடைக்குமா?", "iraṇṭu irukkaikaḷ arukarukē kiṭaikkumā?", "Are two seats available side by side?"), ("ஊழியர்", "ஆம், நடுப்பகுதியில் கிடைக்கின்றன.", "ām, naṭuppakutiyil kiṭaikkiṉṟaṉa.", "Yes, they are available in the middle section.")],
                "Departure worksheet", [("Ask and answer.", ["when does the train depart?", "at seven in the evening"], ["ரயில் எப்போது புறப்படும்?", "மாலை ஏழு மணிக்கு"]), ("Check the seats.", ["are two seats available side by side?", "they are available in the middle section"], ["இரண்டு இருக்கைகள் அருகருகே கிடைக்குமா?", "நடுப்பகுதியில் கிடைக்கின்றன"])]),
            _spec_lesson(
                "பயணப் பையைத் தயாரித்தல்",
                "Prepare for a journey and ask what may be carried. எடுத்துச் செல்லுதல் "
                "means take along; தேவையான பொருட்கள் is the things needed, and "
                "மறந்துவிடாதீர்கள் is a respectful reminder.",
                [("பயணப்பை", "payaṇappai", "travel bag", "noun"), ("தேவையான", "tēvaiyāṉa", "necessary", "adjective"), ("ஆவணம்", "āvaṇam", "document", "noun"), ("மருந்து", "maruntu", "medicine", "noun"), ("மறந்துவிடாதீர்கள்", "maṟant uviṭātīrkaḷ", "please do not forget", "phrase")],
                "Packing and reminders", "... எடுத்துச் செல்லுங்கள் · ... மறந்துவிடாதீர்கள்",
                "Use எடுத்துச் செல்லுங்கள் to say 'take along'. The items can be listed before "
                "the verb: அடையாள அட்டை, மருந்து, தண்ணீர். The negative reminder "
                "மறந்துவிடாதீர்கள் is respectful and addresses the listener directly.",
                [("அடையாள அட்டையையும் மருந்தையும் எடுத்துச் செல்லுங்கள்.", "aṭaiyāḷa aṭṭaiyaiyum maruntaiyum eṭuttuc celluṅkaḷ.", "Take your identity card and medicine with you."), ("தண்ணீர் பாட்டிலை மறந்துவிடாதீர்கள்.", "taṇṇīr pāṭṭilai maṟant uviṭātīrkaḷ.", "Please do not forget the water bottle."), ("பயணத்திற்கு முன் சீட்டைச் சரிபாருங்கள்.", "payaṇattiṟku muṉ cīṭṭaic caripāruṅkaḷ.", "Check the ticket before the journey.")],
                [("அடையாள அட்டை மருந்தையும் எடுத்துச் செல்லுங்கள்.", "அடையாள அட்டையையும் மருந்தையும் எடுத்துச் செல்லுங்கள்.", "Repeat the object marker and -உம் on both items in a formal list."), ("தண்ணீர் பாட்டில் மறந்துவிடாதீர்கள்.", "தண்ணீர் பாட்டிலை மறந்துவிடாதீர்கள்.", "Mark the object with -ஐ.")],
                [("கவி", "பயணத்திற்கு முன் என்னென்ன எடுத்துச் செல்ல வேண்டும்?", "payaṇattiṟku muṉ eṉṉeṉṉa eṭuttuc cella vēṇṭum?", "What should we take before the journey?"), ("மீனா", "அடையாள அட்டையையும் மருந்தையும் எடுத்துச் செல்லுங்கள்.", "aṭaiyāḷa aṭṭaiyaiyum maruntaiyum eṭuttuc celluṅkaḷ.", "Take your identity card and medicine."), ("கவி", "தண்ணீர் பாட்டிலை மறக்கமாட்டேன்.", "taṇṇīr pāṭṭilai maṟakkamāṭṭēṉ.", "I will not forget the water bottle."), ("மீனா", "சீட்டையும் முன்பே சரிபாருங்கள்.", "cīṭṭaiyum muṉpē caripāruṅkaḷ.", "Check the ticket in advance too.")],
                "Packing worksheet", [("List the essentials.", ["take your identity card and medicine", "do not forget the water bottle"], ["அடையாள அட்டையையும் மருந்தையும் எடுத்துச் செல்லுங்கள்", "தண்ணீர் பாட்டிலை மறந்துவிடாதீர்கள்"]), ("Check before travel.", ["check the ticket before the journey", "check the ticket in advance too"], ["பயணத்திற்கு முன் சீட்டைச் சரிபாருங்கள்", "சீட்டையும் முன்பே சரிபாருங்கள்"])]),
        ]},
        {"id": "A2+-U3", "title": "விடுதியில் தங்குதல்", "lessons": [
            _spec_lesson(
                "விடுதியில் பதிவு செய்தல்",
                "Check in, give the booking name, and confirm the room and number of nights. "
                "முன்பதிவு is a booking; பெயரில் says under the name, and எத்தனை இரவுகள் "
                "asks for the length of the stay.",
                [("விடுதி", "viṭuti", "hotel, lodging", "noun"), ("முன்பதிவு", "muṉpativu", "booking", "noun"), ("பெயர்", "peyar", "name", "noun"), ("அறை", "aṟai", "room", "noun"), ("இரவு", "iravu", "night", "noun")],
                "Checking in", "... பெயரில் முன்பதிவு · எத்தனை இரவுகள்? · அறை எண் ...",
                "Use -இல் to identify the booking name: கவி என்ற பெயரில். Ask for the stay "
                "with எத்தனை இரவுகள்? The room number follows அறை எண்.",
                [("கவி என்ற பெயரில் இரண்டு இரவுகளுக்கு முன்பதிவு செய்துள்ளேன்.", "kavi eṉṟa peyaril iraṇṭu iravukaḷukku muṉpativu ceytuḷḷēṉ.", "I have a booking for two nights under the name Kavi."), ("அறை எண் 204.", "aṟai eṇ 204.", "Room number 204."), ("காலை உணவு எத்தனை மணிக்கு?", "kālai uṇavu ettaṉai maṇikku?", "What time is breakfast?")],
                [("கவி பெயரில் முன்பதிவு செய்தேன்.", "கவி என்ற பெயரில் முன்பதிவு செய்துள்ளேன்.", "Use என்ற பெயரில் for a booking under a name."), ("இரண்டு இரவு தங்குகிறேன்.", "இரண்டு இரவுகள் தங்குகிறேன்.", "Use the plural duration for two nights.")],
                [("வரவேற்பாளர்", "வணக்கம். முன்பதிவு செய்துள்ளீர்களா?", "vaṇakkam. muṉpativu ceytuḷḷīrkaḷā?", "Hello. Do you have a booking?"), ("பயணி", "ஆம், கவி என்ற பெயரில் இரண்டு இரவுகளுக்கு.", "ām, kavi eṉṟa peyaril iraṇṭu iravukaḷukku.", "Yes, for two nights under the name Kavi."), ("வரவேற்பாளர்", "அறை எண் 204. காலை உணவு ஏழு மணிக்கு.", "aṟai eṇ 204. kālai uṇavu ēḻu maṇikku.", "Room 204. Breakfast is at seven."), ("பயணி", "நன்றி. அறை எங்கே இருக்கிறது?", "naṉṟi. aṟai eṅkē irukkiṟatu?", "Thank you. Where is the room?")],
                "Check-in worksheet", [("Give the booking.", ["I booked two nights under the name Kavi", "room number 204"], ["கவி என்ற பெயரில் இரண்டு இரவுகளுக்கு முன்பதிவு செய்துள்ளேன்", "அறை எண் 204"]), ("Ask about breakfast.", ["what time is breakfast?", "breakfast is at seven"], ["காலை உணவு எத்தனை மணிக்கு?", "காலை உணவு ஏழு மணிக்கு"])]),
            _spec_lesson(
                "அறைக்கான வேண்டுகோள்",
                "Request a towel, a second key, or help with a room problem. தேவைப்படுகிறது "
                "states a need; வேலை செய்யவில்லை reports that something is not working, "
                "and முடியுமா? makes the request polite.",
                [("துண்டு", "tuṇṭu", "towel", "noun"), ("சாவி", "cāvi", "key", "noun"), ("வேலை செய்யவில்லை", "vēlai ceyyavillai", "is not working", "phrase"), ("உதவி", "utavi", "help", "noun"), ("கொண்டு வருதல்", "koṇṭu varutal", "to bring", "verb")],
                "A polite request", "... கொண்டு வர முடியுமா? · ... வேலை செய்யவில்லை · உதவி தேவைப்படுகிறது",
                "Ask whether staff can bring something with கொண்டு வர முடியுமா? State a "
                "problem with ... வேலை செய்யவில்லை. Adding தயவுசெய்து keeps the request "
                "courteous without making it unclear.",
                [("தயவுசெய்து இன்னொரு துண்டு கொண்டு வர முடியுமா?", "tayavuceytu iṉṉoru tuṇṭu koṇṭu vara muṭiyumā?", "Could you please bring another towel?"), ("அறையின் விளக்கு வேலை செய்யவில்லை.", "aṟaiyiṉ viḷakku vēlai ceyyavillai.", "The room light is not working."), ("சாவியை மாற்ற உதவி தேவைப்படுகிறது.", "cāviyai māṟṟa utavi tēvaippaṭukiṟatu.", "I need help changing the key.")],
                [("இன்னொரு துண்டு கொண்டு வா.", "இன்னொரு துண்டு கொண்டு வர முடியுமா?", "Use a question to make the request polite."), ("அறையின் விளக்கு வேலை செய்யவில்லை இருக்கிறது.", "அறையின் விளக்கு வேலை செய்யவில்லை.", "வேலை செய்யவில்லை is already a complete negative verb.")],
                [("பயணி", "அறையின் விளக்கு வேலை செய்யவில்லை.", "aṟaiyiṉ viḷakku vēlai ceyyavillai.", "The room light is not working."), ("வரவேற்பாளர்", "மன்னிக்கவும். உடனே சரிபார்க்கிறோம்.", "maṉṉikkavum. uṭaṉē caripārkkiṟōm.", "I am sorry. We will check it immediately."), ("பயணி", "இன்னொரு துண்டும் கொண்டு வர முடியுமா?", "iṉṉoru tuṇṭum koṇṭu vara muṭiyumā?", "Could you bring another towel too?"), ("வரவேற்பாளர்", "நிச்சயமாக. அறைக்கு அனுப்புகிறேன்.", "niccayamāka. aṟaikku aṉuppukiṟēṉ.", "Certainly. I will send it to the room.")],
                "Room request worksheet", [("Report the problem.", ["the room light is not working", "I need help changing the key"], ["அறையின் விளக்கு வேலை செய்யவில்லை", "சாவியை மாற்ற உதவி தேவைப்படுகிறது"]), ("Make the request.", ["could you please bring another towel?", "I will send it to the room"], ["தயவுசெய்து இன்னொரு துண்டு கொண்டு வர முடியுமா?", "அறைக்கு அனுப்புகிறேன்"])]),
            _spec_lesson(
                "விடுதியிலிருந்து புறப்படுதல்",
                "Check the bill, return the key, and ask whether luggage can be kept after checkout. "
                "கணக்கு is the bill; சரிபார்த்தல் is checking; ... வரை இங்கே வைக்கலாமா? "
                "asks permission to leave something until a time.",
                [("கணக்கு", "kaṇakku", "bill, account", "noun"), ("புறப்படுதல்", "puṟappaṭutal", "to depart", "verb"), ("சாமான்கள்", "cāmaṉkaḷ", "luggage, belongings", "noun"), ("வைக்க", "vaikka", "to leave, put", "verb"), ("பிற்பகல்", "piṟpakal", "afternoon", "noun")],
                "Checking out", "கணக்கைச் சரிபாருங்கள் · ... வரை வைக்கலாமா? · சாவியைத் திருப்பிக் கொடுங்கள்",
                "Mark the bill as an object with -ஐ: கணக்கைச் சரிபாருங்கள். For a time limit, "
                "use வரை: பிற்பகல் மூன்று மணி வரை. A respectful request ends in -லாமா?",
                [("கணக்கைச் சரிபார்க்க முடியுமா?", "kaṇakkaic caripārkka muṭiyumā?", "Could I check the bill?"), ("சாமான்களை பிற்பகல் மூன்று மணி வரை இங்கே வைக்கலாமா?", "cāmaṉkaḷai piṟpakal mūṉṟu maṇi varai iṅkē vaikkalāmā?", "May I leave my luggage here until three in the afternoon?"), ("சாவியை வரவேற்பில் திருப்பிக் கொடுங்கள்.", "cāviyai varavēṟpil tiruppik koṭuṅkaḷ.", "Please return the key at reception.")],
                [("கணக்கு சரிபார்க்க முடியுமா?", "கணக்கைச் சரிபார்க்க முடியுமா?", "Mark the bill as the object with -ஐ."), ("மூன்று மணி வரை சாமான்கள் வைக்கலாமா?", "சாமான்களை மூன்று மணி வரை வைக்கலாமா?", "Mark luggage as the object and keep the time limit clear.")],
                [("பயணி", "கணக்கைச் சரிபார்க்க முடியுமா?", "kaṇakkaic caripārkka muṭiyumā?", "Could I check the bill?"), ("வரவேற்பாளர்", "நிச்சயமாக. இதோ கணக்கு.", "niccayamāka. itō kaṇakku.", "Certainly. Here is the bill."), ("பயணி", "சாமான்களை மூன்று மணி வரை இங்கே வைக்கலாமா?", "cāmaṉkaḷai mūṉṟu maṇi varai iṅkē vaikkalāmā?", "May I leave my luggage here until three?"), ("வரவேற்பாளர்", "ஆம். புறப்படும்போது சாவியைத் திருப்பிக் கொடுங்கள்.", "ām. puṟappaṭumpōtu cāviyait tiruppik koṭuṅkaḷ.", "Yes. Please return the key when you leave.")],
                "Check-out worksheet", [("Check the bill.", ["could I check the bill?", "here is the bill"], ["கணக்கைச் சரிபார்க்க முடியுமா?", "இதோ கணக்கு"]), ("Ask about luggage.", ["may I leave my luggage here until three?", "please return the key when you leave"], ["சாமான்களை மூன்று மணி வரை இங்கே வைக்கலாமா?", "புறப்படும்போது சாவியைத் திருப்பிக் கொடுங்கள்"])]),
        ]},
    ],
    "extra": EXTRA(
        culture=("Kancheepuram silk is a living handloom craft, not a single fixed pattern. "
                 "Tamil Nadu Tourism notes that motifs draw on local architecture, "
                 "animals, birds and religious imagery, and that a sari's weaving time "
                 "depends on its design. In a weaving household, warp, weft, colour "
                 "and border are practical vocabulary as well as craft knowledge. "
                 "The examples describe the work without claiming that every sari or "
                 "weaver follows one design tradition; Tamil Nadu has other silk "
                 "weaving clusters too."),
        source_url="https://www.tamilnadutourism.tn.gov.in/experiences/silk-sarees",
        reading=("காஞ்சிபுரத்தில் ஒரு நெசவாளர் சேலையின் வடிவத்தை முதலில் "
                 "காகிதத்தில் வரைந்தார். பின்னர் நிறத்தையும் கரையின் அகலத்தையும் "
                 "தேர்ந்தெடுத்தார். «இந்த மயில் வடிவம் கோயில் சிற்பத்தை நினைவூட்டும்; "
                 "ஆனால் ஒவ்வொரு வடிவத்துக்கும் ஒரு கதையைச் சேர்க்க வேண்டியதில்லை» "
                 "என்றார். நெசவு முடிந்ததும் துணி சோதிக்கப்பட்டு, குறை இருந்தால் "
                 "திருத்தப்பட்டது. ஒரு சேலையை உருவாக்கும் நேரம் அதன் வடிவத்தைப் "
                 "பொறுத்து மாறும்."),
        reading_gloss=("In Kancheepuram a weaver first drew the sari's design on paper. "
                       "Then the weaver chose the colour and the border's width. 'This "
                       "peacock motif recalls a temple sculpture; but not every motif "
                       "needs to be given a story,' the weaver said. After weaving, the "
                       "cloth was inspected and, if there was a flaw, corrected. The time "
                       "needed to make a sari varies with its design."),
        listening=("இந்த வடிவத்தை நெய்ய எவ்வளவு நேரம் ஆகும்? — வடிவத்தைப் "
                   "பொறுத்து மாறும். — கரையை வேறு நிறத்தில் செய்யலாமா? — "
                   "செய்யலாம்; முதலில் மாதிரியைப் பார்த்து உறுதிப்படுத்துங்கள்."),
        listening_gloss=("How long will it take to weave this design? — It varies with "
                         "the design. — Can the border be made in another colour? — "
                         "Yes; first look at and confirm the sample."),
        voice_tag=VOICE,
        idioms=[
            ("கண்ணைக் கவரும்", "to catch the eye", "visually striking"),
            ("நூலிழையில் தப்புதல்", "to escape by a thread's width", "to escape narrowly"),
            ("வாயில் வெண்ணெய் வைத்தது போல", "as if butter were in the mouth", "to remain silent"),
            ("மூக்கில் வியர்வை சிந்துதல்", "to sweat from the nose", "to work very hard"),
            ("கைதேர்ந்த கலைஞர்", "an artist trained by the hand", "a highly skilled craftsperson"),
            ("பட்டுப்போல் மென்மை", "soft as silk", "exceptionally soft or gentle"),
            ("கண்ணுக்கு குளிர்ச்சி", "coolness to the eye", "a pleasing sight"),
            ("கண்ணில் மண் தூவுதல்", "to throw dust in the eye", "to deceive someone"),
            ("கைமீறிப் போதல்", "to go beyond the hand", "to get out of control"),
            ("கண்ணை மூடிக்கொண்டு நம்புதல்", "to trust with the eyes closed", "to trust without checking"),
        ],
        mistakes=[
            ("ஒவ்வொரு சேலையும் ஒரே வடிவத்தில் நெய்யப்படுகிறது.", "சேலையின் வடிவம் நெசவாளரின் தேர்வைப் பொறுத்து மாறலாம்.", "Do not turn one regional craft into a claim of uniformity."),
            ("இந்த நிறம் கண்ணுக்கு குளிர்.", "இந்த நிறம் கண்ணுக்கு குளிர்ச்சியாக இருக்கிறது.", "Use the adverbial adjective form குளிர்ச்சியாக with இருக்கிறது."),
            ("வடிவத்தைப் பொறுத்து நேரம் மாறுகிறது அது.", "வடிவத்தைப் பொறுத்து நேரம் மாறுகிறது.", "Tamil does not need an extra subject pronoun after the clause."),
        ],
        task_title="நெசவின் விவரிப்பு",
        task_instructions=("Describe a handwoven object you have seen or studied. Name its "
                           "material, one design choice, and how the maker's work is "
                           "checked. Distinguish what your source says from what you "
                           "observed yourself, and avoid treating one workshop as "
                           "representative of every weaving community."),
    ),
    "test": [
        ("translate_en", "Say: I need a one-way ticket from Chennai to Madurai.", "சென்னையிலிருந்து மதுரை வரை ஒரு வழிச் சீட்டு வேண்டும்."),
        ("translate_ta", "சாமான்களை மூன்று மணி வரை இங்கே வைக்கலாமா?", "May I leave my luggage here until three?"),
        ("multiple_choice", "Which phrase asks for an exit?", "வெளியேறும் வழி எது?"),
        ("fill_in_the_blank", "இரண்டு இருக்கைகள் அருகருகே ___.", "கிடைக்குமா"),
        ("word_selection", "Select the Tamil for 'booking'.", "முன்பதிவு"),
        ("error_correction", "ரயில் ஏழு மணியில் புறப்படும்.", "ரயில் ஏழு மணிக்குப் புறப்படும்."),
        ("dialogue_completion", "முன்பதிவு செய்துள்ளீர்களா? — ஆம், ___ பெயரில்.", "கவி என்ற"),
        ("matching", "Match திரும்பும் சீட்டு to its meaning.", "return ticket"),
        ("reading_comprehension", "What did the weaver inspect after weaving?", "the cloth"),
        ("inference", "Why does the passage say not every motif needs a story?", "to avoid assuming one fixed meaning for every design"),
        ("main_idea", "What is the reading mainly about?", "a weaver choosing and checking a sari design"),
        ("detail_identification", "What can the time needed to weave a sari depend on?", "its design"),
    ],
}

HALFSTEPS["B1+"] = {
    "native": NATIVE,
    "title": "Tamil B1+ — Neighbourhood, work and opinion",
    "goals": [
        "Describe an apartment and compare nearby services without exaggerating",
        "Give a work or study update, explaining sequence and cause",
        "State a view, respond to disagreement, and suggest a fair next step",
    ],
    "units": [
        {"id": "B1+-U1", "title": "பகுதியும் குடியிருப்பும்", "lessons": [
            _spec_lesson(
                "அருகிலுள்ள வசதிகள்",
                "Describe what is available in a neighbourhood and what remains far away. "
                "அருகிலுள்ள modifies a nearby place; இருந்தாலும் adds a contrast, and "
                "சேவை is a service. Keep the comparison attached to a named location.",
                [("குடியிருப்பு", "kuṭiyiruppu", "residential area", "noun"), ("வசதி", "vacati", "facility, convenience", "noun"), ("அருகிலுள்ள", "arukil uḷḷa", "nearby", "adjective"), ("மருத்துவமனை", "maruttuvamaṉai", "hospital", "noun"), ("சேவை", "cēvai", "service", "noun")],
                "Neighbourhood description", "... அருகிலுள்ளது · இருந்தாலும் ... · ...க்கு ... தூரம்",
                "Describe a service relative to a named place: பள்ளிக்கு அருகிலுள்ள மருத்துவமனை. "
                "Use இருந்தாலும் to balance a benefit with a limitation. For distance, put "
                "the place first and use -க்கு தூரம்: பேருந்து நிறுத்தத்திற்கு ஐந்து நிமிடம் தூரம்.",
                [("எங்கள் குடியிருப்புக்கு அருகிலுள்ள சந்தை காலை திறக்கும்.", "eṅkaḷ kuṭiyiruppukku arukiluḷḷa cantai kālai tiṟakkum.", "The market near our residential area opens in the morning."), ("மருத்துவமனை அருகில் இருந்தாலும், பேருந்து சேவை குறைவு.", "maruttuvamaṉai arukil iruntālum, pēruntu cēvai kuṟaivu.", "Although the hospital is nearby, bus service is limited."), ("பேருந்து நிறுத்தத்திற்கு ஐந்து நிமிடம் நடக்க வேண்டும்.", "pēruntu niṟuttattiṟku aintu nimiṭam naṭakka vēṇṭum.", "You need to walk five minutes to the bus stop.")],
                [("மருத்துவமனை அருகில், ஆனால் பேருந்து சேவை குறைவு.", "மருத்துவமனை அருகில் இருந்தாலும், பேருந்து சேவை குறைவு.", "Join the contrast with இருந்தாலும் instead of a fragment."), ("சந்தை அருகிலுள்ள எங்கள் குடியிருப்பு காலை திறக்கும்.", "எங்கள் குடியிருப்புக்கு அருகிலுள்ள சந்தை காலை திறக்கும்.", "Attach the location to the market, not to the residential area as an adjective.")],
                [("மீனா", "இந்தப் பகுதியில் என்ன வசதிகள் உள்ளன?", "intap pakutiyil eṉṉa vacatikaḷ uḷḷaṉa?", "What facilities are there in this area?"), ("கவி", "சந்தையும் மருத்துவமனையும் அருகில் உள்ளன.", "cantaiyum maruttuvamaṉaiyum arukil uḷḷaṉa.", "The market and hospital are nearby."), ("மீனா", "பேருந்து சேவை எப்படி?", "pēruntu cēvai eppaṭi?", "How is the bus service?"), ("கவி", "நிறுத்தம் அருகில் இருந்தாலும், பேருந்துகள் அடிக்கடி வருவதில்லை.", "niṟuttam arukil iruntālum, pēruntukaḷ aṭikkaṭi varuvatillai.", "Although the stop is nearby, buses do not come often.")],
                "Neighbourhood worksheet", [("Describe the facilities.", ["the market and hospital are nearby", "the market near our area opens in the morning"], ["சந்தையும் மருத்துவமனையும் அருகில் உள்ளன", "எங்கள் குடியிருப்புக்கு அருகிலுள்ள சந்தை காலை திறக்கும்"]), ("Add the limitation.", ["although the stop is close, buses do not come often", "bus service is limited"], ["நிறுத்தம் அருகில் இருந்தாலும் பேருந்துகள் அடிக்கடி வருவதில்லை", "பேருந்து சேவை குறைவு"])]),
            _spec_lesson(
                "குடியிருப்பு பராமரிப்பு",
                "Report a maintenance problem and ask when it will be fixed. பழுதடைந்த "
                "describes something that has broken; புகார் அளித்தேன் says a complaint "
                "was made, and சரிசெய்யப்படும் is a future passive.",
                [("பராமரிப்பு", "paramarippu", "maintenance", "noun"), ("பழுதடைந்த", "paḻutaṭainta", "broken, damaged", "adjective"), ("குழாய்", "kuḻāy", "pipe, tap", "noun"), ("புகார்", "pukār", "complaint", "noun"), ("சரிசெய்தல்", "cariceytal", "to repair", "verb")],
                "Reporting a repair", "... பழுதடைந்துள்ளது · புகார் அளித்தேன் · ... சரிசெய்யப்படும்",
                "Describe the fault with a participle: பழுதடைந்த குழாய். The repair is "
                "foregrounded in the passive சரிசெய்யப்படும். Ask for a time with "
                "எப்போது? and state the report number if you have it.",
                [("சமையலறைக் குழாய் பழுதடைந்துள்ளது.", "camaiyalaṟaik kuḻāy paḻutaṭaintuḷḷatu.", "The kitchen tap is broken."), ("நேற்று பராமரிப்பு அலுவலகத்தில் புகார் அளித்தேன்.", "nēṟṟu paramarippu aluv alakattil pukār aḷittēṉ.", "Yesterday I filed a complaint with the maintenance office."), ("பழுது நாளைக்குள் சரிசெய்யப்படும் என்று தெரிவித்தார்கள்.", "paḻutu nāḷaikkuḷ cariceyyappaṭum eṉṟu terivittārkaḷ.", "They said the fault would be repaired by tomorrow.")],
                [("சமையலறைக் குழாய் பழுது உள்ளது.", "சமையலறைக் குழாய் பழுதடைந்துள்ளது.", "Use the participle பழுதடைந்த to describe the broken tap."), ("பராமரிப்பு அலுவலகம் பழுது சரிசெய்யும் என்று கூறப்பட்டது.", "பழுது சரிசெய்யப்படும் என்று கூறப்பட்டது.", "Use a passive when the repairing team is not identified.")],
                [("கவி", "குழாய் இன்னும் சரிசெய்யப்படவில்லையா?", "kuḻāy iṉṉum cariceyyappaṭavillaiyā?", "Has the tap still not been repaired?"), ("மீனா", "இல்லை. நேற்று புகார் அளித்தேன்.", "illai. nēṟṟu pukār aḷittēṉ.", "No. I filed a complaint yesterday."), ("கவி", "எப்போது சரிசெய்யப்படும் என்று சொன்னார்கள்?", "eppōtu cariceyyappaṭum eṉṟu coṉṉārkaḷ?", "When did they say it would be repaired?"), ("மீனா", "நாளைக்குள் என்று தெரிவித்தார்கள்.", "nāḷaikkuḷ eṉṟu terivittārkaḷ.", "They said by tomorrow.")],
                "Repair worksheet", [("Report the fault.", ["the kitchen tap is broken", "I filed a complaint yesterday"], ["சமையலறைக் குழாய் பழுதடைந்துள்ளது", "நேற்று புகார் அளித்தேன்"]), ("Ask for the timeline.", ["when will it be repaired?", "they said by tomorrow"], ["எப்போது சரிசெய்யப்படும்?", "நாளைக்குள் என்று தெரிவித்தார்கள்"])]),
            _spec_lesson(
                "இரு பகுதிகளை ஒப்பிடுதல்",
                "Compare two neighbourhoods by access, noise, and cost rather than calling one "
                "simply better. ...ஐ விட gives the comparison point; அதே சமயம் balances "
                "the advantage with a drawback.",
                [("அமைதியான", "amaitiyāṉa", "quiet", "adjective"), ("போக்குவரத்து", "pōkkuvarattu", "transport", "noun"), ("செலவு", "celavu", "cost", "noun"), ("ஒப்பீடு", "oppīṭu", "comparison", "noun"), ("சுற்றுப்புறம்", "cuṟṟuppuṟam", "surroundings", "noun")],
                "Balanced comparisons", "A-ஐ விட B ... · அதே சமயம் ... · எனக்கு ... ஏற்றது",
                "Use -ஐ விட after the comparison point, and name the feature being compared: "
                "முதல் பகுதியை விட இரண்டாவது பகுதி அமைதியானது. அதே சமயம் introduces a "
                "balancing cost or limitation. End with a personal criterion, not a "
                "universal ranking.",
                [("முதல் பகுதியை விட இரண்டாவது பகுதி அமைதியானது.", "mutal pakutiyai viṭa iraṇṭāvatu pakuti amaitiyāṉatu.", "The second area is quieter than the first."), ("அதே சமயம், அங்கு போக்குவரத்து வசதி குறைவு.", "atē camayam, aṅku pōkkuvarattu vacati kuṟaivu.", "At the same time, transport is less convenient there."), ("பள்ளிக்கு அருகில் இருப்பது எங்கள் குடும்பத்திற்கு முக்கியம்.", "paḷḷikku arukil iruppatu eṅkaḷ kuṭumpattiṟku mukkiyam.", "Being near the school is important for our family.")],
                [("முதல் பகுதியை விட இரண்டாவது பகுதி அமைதி.", "முதல் பகுதியை விட இரண்டாவது பகுதி அமைதியானது.", "Use the adjective அமைதியானது to complete the comparison."), ("அதே சமயம் அங்கு போக்குவரத்து வசதி நல்லது குறைவு.", "அதே சமயம் அங்கு போக்குவரத்து வசதி குறைவு.", "Do not include contradictory evaluations in the same clause.")],
                [("அருண்", "எந்தப் பகுதி உங்களுக்கு ஏற்றது?", "entap pakuti uṅkaḷukku ēṟṟatu?", "Which area suits you?"), ("கவி", "முதல் பகுதியை விட இரண்டாவது பகுதி அமைதியானது.", "mutal pakutiyai viṭa iraṇṭāvatu pakuti amaitiyāṉatu.", "The second area is quieter than the first."), ("அருண்", "ஆனால் போக்குவரத்து வசதி?", "āṉāl pōkkuvarattu vacati?", "But what about transport?"), ("கவி", "அதே சமயம் அது குறைவு; பள்ளிக்கு அருகில் இருப்பதே எங்களுக்கு முக்கியம்.", "atē camayam atu kuṟaivu; paḷḷikku arukil iruppatē eṅkaḷukku mukkiyam.", "At the same time, it is limited; being near the school matters most to us.")],
                "Compare areas worksheet", [("Compare the areas.", ["the second area is quieter than the first", "transport is less convenient there"], ["முதல் பகுதியை விட இரண்டாவது பகுதி அமைதியானது", "அங்கு போக்குவரத்து வசதி குறைவு"]), ("State your criterion.", ["being near the school is important for our family", "the second area suits us"], ["பள்ளிக்கு அருகில் இருப்பது எங்கள் குடும்பத்திற்கு முக்கியம்", "இரண்டாவது பகுதி எங்களுக்கு ஏற்றது"])]),
        ]},
        {"id": "B1+-U2", "title": "வேலையும் படிப்பும்", "lessons": [
            _spec_lesson(
                "குழுப் பணியின் முன்னேற்றம்",
                "Give a project update with completed tasks, work in progress, and the next "
                "step. முடித்த பணி names finished work; செய்து கொண்டிருக்கிறோம் is "
                "ongoing, and அடுத்ததாக sequences the plan.",
                [("முன்னேற்றம்", "muṉṉēṟṟam", "progress", "noun"), ("குழுப்பணி", "kuḻuppaṇi", "teamwork", "noun"), ("முடித்த", "muṭitta", "completed", "participle"), ("செயல்பாடு", "ceyalpāṭu", "activity", "noun"), ("அடுத்ததாக", "aṭuttatāka", "next, afterward", "adverb")],
                "A progress update", "முடித்த பணி ... · செய்து கொண்டிருக்கிறோம் · அடுத்ததாக ... செய்வோம்",
                "A participle modifies the noun: முடித்த பணி. For work still under way, "
                "use செய்து கொண்டிருக்கிறோம்; then announce the next step with "
                "அடுத்ததாக and a future verb.",
                [("முடித்த பணிகளை அறிக்கையில் சேர்த்தோம்.", "muṭitta paṇikaḷai aṟikkaiyil cērttōm.", "We added the completed tasks to the report."), ("தரவைச் சரிபார்த்து கொண்டிருக்கிறோம்.", "taravaic caripārttu koṇṭirukkiṟōm.", "We are checking the data."), ("அடுத்ததாக வரைபடத்தைத் தயாரிப்போம்.", "aṭuttatāka varaipaṭattait tayārippōm.", "Next we will prepare the chart.")],
                [("முடித்த பணி அறிக்கையில் சேர்க்கிறோம்.", "முடித்த பணிகளை அறிக்கையில் சேர்த்தோம்.", "Use plural object marking and past tense for completed work."), ("தரவைச் சரிபார்த்து கொண்டிருக்கிறார். (our team)", "தரவைச் சரிபார்த்துக் கொண்டிருக்கிறோம்.", "Use the first-person plural for the team and join the aspect marker.")],
                [("மேலாளர்", "இந்த வாரம் என்ன முன்னேற்றம்?", "inta vāram eṉṉa muṉṉēṟṟam?", "What progress did you make this week?"), ("கவி", "முடித்த பணிகளை அறிக்கையில் சேர்த்தோம்.", "muṭitta paṇikaḷai aṟikkaiyil cērttōm.", "We added the completed tasks to the report."), ("மேலாளர்", "தரவு சரிபார்க்கப்பட்டுவிட்டதா?", "taravu caripārkkappaṭṭuviṭṭatā?", "Has the data been checked?"), ("கவி", "இப்போது சரிபார்த்து கொண்டிருக்கிறோம்; அடுத்ததாக வரைபடம் தயாராகும்.", "ippōtu caripārttu koṇṭirukkiṟōm; aṭuttatāka varaipaṭam tayārākum.", "We are checking it now; next the chart will be ready.")],
                "Project update worksheet", [("Report completed work.", ["we added the completed tasks to the report", "we are checking the data"], ["முடித்த பணிகளை அறிக்கையில் சேர்த்தோம்", "தரவைச் சரிபார்த்துக் கொண்டிருக்கிறோம்"]), ("Name the next step.", ["next we will prepare the chart", "the chart will be ready"], ["அடுத்ததாக வரைபடத்தைத் தயாரிப்போம்", "வரைபடம் தயாராகும்"])]),
            _spec_lesson(
                "படிப்பு இலக்கை விளக்குதல்",
                "Explain a study goal and a reason for choosing it. நோக்கம் states a goal; "
                "...க்காக gives purpose, and ... என்பதால் links a reason to a decision.",
                [("இலக்கு", "ilakku", "goal", "noun"), ("நோக்கம்", "nōkkam", "purpose", "noun"), ("தேர்வு", "tērvu", "choice, selection", "noun"), ("வளர்த்தல்", "vaḷarttal", "to develop", "verb"), ("தன்னம்பிக்கை", "taṉṉampikkai", "confidence", "noun")],
                "Purpose and reason", "...க்காக ... தேர்ந்தெடுத்தேன் · ... என்பதால் ...",
                "Attach -க்காக to the purpose: மொழித் திறனை வளர்ப்பதற்காக. Use என்பதால் "
                "to give the reason behind a choice. Keep the goal and the reason in "
                "separate clauses so both remain clear.",
                [("பேச்சுத் திறனை வளர்ப்பதற்காக இந்தப் பாடத்தைத் தேர்ந்தெடுத்தேன்.", "pēccut tiṟaṉai vaḷarppataṟkāka intap pāṭattait tēṟnteṭuttēṉ.", "I chose this course to develop my speaking skill."), ("தேர்வில் வாய்மொழிப் பகுதி இருப்பதால் பயிற்சி தேவை.", "tērvil vāymoḻip pakuti iruppatāl payiṟci tēvai.", "Because the exam has an oral section, practice is needed."), ("சிறிய இலக்குகளை அமைத்தால் தன்னம்பிக்கை வளரும்.", "ciṟiya ilakkukaḷai amaittāl taṉṉampikkai vaḷarum.", "If we set small goals, confidence grows.")],
                [("பேச்சுத் திறனை வளர்க்க இந்தப் பாடம் தேர்ந்தெடுத்தேன்.", "பேச்சுத் திறனை வளர்ப்பதற்காக இந்தப் பாடத்தைத் தேர்ந்தெடுத்தேன்.", "Use the purpose form -தற்காக and mark the course as the object."), ("தேர்வில் வாய்மொழிப் பகுதி இருக்கிறதா பயிற்சி தேவை.", "தேர்வில் வாய்மொழிப் பகுதி இருப்பதால் பயிற்சி தேவை.", "Connect the reason with -தால்.")],
                [("ஆசிரியர்", "இந்தப் பாடத்தை ஏன் தேர்ந்தெடுத்தீர்கள்?", "intap pāṭattai ēṉ tēṟnteṭuttīrkaḷ?", "Why did you choose this course?"), ("மாணவர்", "பேச்சுத் திறனை வளர்ப்பதற்காக.", "pēccut tiṟaṉai vaḷarppataṟkāka.", "To develop my speaking skill."), ("ஆசிரியர்", "உங்கள் அடுத்த இலக்கு என்ன?", "uṅkaḷ aṭutta ilakku eṉṉa?", "What is your next goal?"), ("மாணவர்", "வாய்மொழிப் பகுதி இருப்பதால், வாரம் இருமுறை பேசிப் பயிற்சி செய்வேன்.", "vāymoḻip pakuti iruppatāl, vāram irumuṟai pēc ip payiṟci ceyvēṉ.", "Because there is an oral section, I will practise speaking twice a week.")],
                "Study goal worksheet", [("Give the purpose.", ["I chose this course to develop my speaking skill", "my next goal is to practise twice a week"], ["பேச்சுத் திறனை வளர்ப்பதற்காக இந்தப் பாடத்தைத் தேர்ந்தெடுத்தேன்", "வாரம் இருமுறை பேசிப் பயிற்சி செய்வது என் அடுத்த இலக்கு"]), ("Explain why.", ["because there is an oral section, practice is needed", "small goals build confidence"], ["வாய்மொழிப் பகுதி இருப்பதால் பயிற்சி தேவை", "சிறிய இலக்குகள் தன்னம்பிக்கையை வளர்க்கும்"])]),
            _spec_lesson(
                "வேலை நேர மாற்றம்",
                "Explain a schedule conflict and suggest another time. பணி நேரம் marks "
                "work hours; மாற்று நேரம் is an alternative slot, and ... முடியாவிட்டால் "
                "sets a polite condition.",
                [("பணி நேரம்", "paṇi nēram", "work hours", "phrase"), ("மாற்று", "māṟṟu", "alternative", "noun"), ("கூட்டம்", "kūṭṭam", "meeting", "noun"), ("முடியாவிட்டால்", "muṭiyāviṭṭāl", "if it is not possible", "conditional"), ("முன்கூட்டியே", "muṉkūṭṭiyē", "in advance", "adverb")],
                "Negotiating a time", "... நேரத்தில் முடியாது · ... முடியாவிட்டால் ... · முன்கூட்டியே தெரிவிக்கிறேன்",
                "State the conflict without blame: அந்த நேரத்தில் கூட்டத்தில் பங்கேற்க "
                "முடியாது. Use முடியாவிட்டால் to offer a fallback, then promise to notify "
                "in advance with முன்கூட்டியே தெரிவிக்கிறேன்.",
                [("திங்கள் மாலை பணி நேரம் என்பதால் கூட்டத்தில் பங்கேற்க முடியாது.", "tiṅkaḷ mālai paṇi nēram eṉpatāl kūṭṭattil paṅkēṟka muṭiyātu.", "I cannot attend the Monday evening meeting because it is work time."), ("அந்த நேரம் முடியாவிட்டால் புதன்கிழமை முயற்சிக்கலாம்.", "anta nēram muṭiyāviṭṭāl put aṉkiḻamai muyaṟcikkalām.", "If that time does not work, we can try Wednesday."), ("மாற்றம் இருந்தால் முன்கூட்டியே தெரிவிக்கிறேன்.", "māṟṟam iruntāl muṉkūṭṭiyē terivikkiṟēṉ.", "If there is a change, I will let you know in advance.")],
                [("திங்கள் மாலை கூட்டம் பங்கேற்க முடியாது.", "திங்கள் மாலை கூட்டத்தில் பங்கேற்க முடியாது.", "Mark the meeting with -இல் after கூட்டம்."), ("முடியாது என்றால் புதன்கிழமை.", "அந்த நேரம் முடியாவிட்டால் புதன்கிழமை முயற்சிக்கலாம்.", "Offer a full, courteous alternative rather than a fragment.")],
                [("மேலாளர்", "திங்கள் மாலை கூட்டத்தில் பங்கேற்க முடியுமா?", "tiṅkaḷ mālai kūṭṭattil paṅkēṟka muṭiyumā?", "Can you attend the Monday evening meeting?"), ("கவி", "அந்த நேரம் பணி நேரம் என்பதால் முடியாது.", "anta nēram paṇi nēram eṉpatāl muṭiyātu.", "I cannot, because that time is work hours."), ("மேலாளர்", "மாற்று நேரம் எது?", "māṟṟu nēram etu?", "What is an alternative time?"), ("கவி", "புதன்கிழமை முயற்சிக்கலாம்; மாற்றம் இருந்தால் முன்கூட்டியே தெரிவிக்கிறேன்.", "put aṉkiḻamai muyaṟcikkalām; māṟṟam iruntāl muṉkūṭṭiyē terivikkiṟēṉ.", "We can try Wednesday; if anything changes, I will let you know in advance.")],
                "Schedule worksheet", [("Explain the conflict.", ["I cannot attend because that time is work hours", "if the time does not work, we can try Wednesday"], ["அந்த நேரம் பணி நேரம் என்பதால் பங்கேற்க முடியாது", "அந்த நேரம் முடியாவிட்டால் புதன்கிழமை முயற்சிக்கலாம்"]), ("Promise an update.", ["I will let you know in advance", "we can try another time"], ["முன்கூட்டியே தெரிவிக்கிறேன்", "மாற்று நேரத்தில் முயற்சிக்கலாம்"])]),
        ]},
        {"id": "B1+-U3", "title": "கருத்தும் விவாதமும்", "lessons": [
            _spec_lesson(
                "கருத்தை ஆதாரத்துடன் கூறுதல்",
                "State an opinion and support it with one reason and one example. எனக்குத் "
                "தோன்றுகிறது softens a claim; காரணம் is the reason, and உதாரணமாக "
                "introduces a concrete example.",
                [("கருத்து", "karuttu", "opinion", "noun"), ("காரணம்", "kāraṇam", "reason", "noun"), ("ஆதாரம்", "ātāram", "evidence", "noun"), ("உதாரணம்", "utāraṇam", "example", "noun"), ("முடிவு", "muṭivu", "conclusion", "noun")],
                "Opinion and evidence", "எனக்குத் தோன்றுகிறது ... · காரணம் ... · உதாரணமாக ...",
                "Begin a personal view with எனக்குத் தோன்றுகிறது. Follow it with காரணம் "
                "and one observable example. A preference is not the same as evidence, "
                "so label the example rather than presenting it as a universal fact.",
                [("இந்தப் பகுதியில் நடந்து செல்லும் வசதியை மேம்படுத்த வேண்டும் என்று எனக்குத் தோன்றுகிறது.", "intap pakutiyil naṭantu cellum vacatiyai mēmpaṭutta vēṇṭum eṉṟu eṉakkut tōṉṟukiṟatu.", "I think pedestrian access in this area should improve."), ("காரணம், பள்ளிக்குச் செல்லும் குழந்தைகள் சாலையைப் பகிர்கிறார்கள்.", "kāraṇam, paḷḷikkuc cellum kuḻantaikaḷ cālaiyaip pakirkiṟārkaḷ.", "The reason is that children going to school share the road."), ("உதாரணமாக, காலை நேரத்தில் நடைபாதை வாகனங்களால் மறைக்கப்படுகிறது.", "utāraṇamāka, kālai nērattil naṭaipātai vākaṉaṅkaḷāl maṟaikkappaṭukiṟatu.", "For example, in the morning the footpath is blocked by vehicles.")],
                [("இந்தப் பகுதி மேம்படுத்த வேண்டும் எனக்குத் தோன்றுகிறது.", "இந்தப் பகுதியில் நடந்து செல்லும் வசதியை மேம்படுத்த வேண்டும் என்று எனக்குத் தோன்றுகிறது.", "Name the object being improved and place the opinion marker at the clause end."), ("உதாரணம் காலை நேரத்தில் நடைபாதை வாகனங்கள் மறைக்கிறது.", "உதாரணமாக, காலை நேரத்தில் நடைபாதை வாகனங்களால் மறைக்கப்படுகிறது.", "Use உதாரணமாக and mark the agent in the passive with -ஆல்.")],
                [("மீனா", "உங்கள் கருத்து என்ன?", "uṅkaḷ karuttu eṉṉa?", "What is your opinion?"), ("கவி", "நடைபாதையை மேம்படுத்த வேண்டும் என்று எனக்குத் தோன்றுகிறது.", "naṭaipātaiyai mēmpaṭutta vēṇṭum eṉṟu eṉakkut tōṉṟukiṟatu.", "I think the footpath should be improved."), ("மீனா", "காரணம் என்ன?", "kāraṇam eṉṉa?", "What is the reason?"), ("கவி", "காலை நேரத்தில் குழந்தைகள் சாலையைப் பகிர்கிறார்கள்; அதுதான் ஒரு உதாரணம்.", "kālai nērattil kuḻantaikaḷ cālaiyaip pakirkiṟārkaḷ; atutāṉ oru utāraṇam.", "In the morning children share the road; that is one example.")],
                "Supported opinion worksheet", [("State the view.", ["I think pedestrian access should improve", "the footpath should be improved"], ["நடந்து செல்லும் வசதி மேம்பட வேண்டும் என்று எனக்குத் தோன்றுகிறது", "நடைபாதையை மேம்படுத்த வேண்டும்"]), ("Add evidence.", ["children share the road in the morning", "the footpath is blocked by vehicles"], ["காலை நேரத்தில் குழந்தைகள் சாலையைப் பகிர்கிறார்கள்", "நடைபாதை வாகனங்களால் மறைக்கப்படுகிறது"])]),
            _spec_lesson(
                "மரியாதையுடன் மறுப்பது",
                "Disagree with a proposal while showing that you understood its aim. ஒரு "
                "அளவுக்கு acknowledges part of the view; இருப்பினும் introduces the "
                "objection, and அதற்குப் பதிலாக offers a workable alternative.",
                [("மறுப்பு", "maṟuppu", "disagreement, refusal", "noun"), ("ஒரு அளவுக்கு", "oru aḷavukku", "to some extent", "phrase"), ("இருப்பினும்", "iruppiṉum", "nevertheless", "connector"), ("மாற்று வழி", "māṟṟu vaḻi", "alternative", "phrase"), ("ஏற்றுக்கொள்ளுதல்", "ēṟṟukkoḷḷutal", "to accept", "verb")],
                "Partial agreement", "ஒரு அளவுக்கு ஒத்துக்கொள்கிறேன் · இருப்பினும் ... · அதற்குப் பதிலாக ...",
                "Acknowledge the useful part first: உங்கள் கருத்தை ஒரு அளவுக்கு ஒத்துக்கொள்கிறேன். "
                "Then state the constraint with இருப்பினும். Offer an alternative with "
                "அதற்குப் பதிலாக, keeping the shared goal visible.",
                [("செலவைக் குறைக்க வேண்டும் என்ற கருத்தை ஒரு அளவுக்கு ஒத்துக்கொள்கிறேன்.", "celavaik kuṟaikka vēṇṭum eṉṟa karuttai oru aḷavukku ottukkoḷkiṟēṉ.", "I agree to some extent with the idea of reducing cost."), ("இருப்பினும், பாதுகாப்பைக் குறைக்க முடியாது.", "iruppiṉum, pāṭukāppaik kuṟaikka muṭiyātu.", "Nevertheless, we cannot reduce safety."), ("அதற்குப் பதிலாக, முதலில் தேவையற்ற செலவை ஆய்வு செய்யலாம்.", "ataṟkup patilāka, mutalil tēvaiyaṟṟa celavai āyvu ceyyalām.", "Instead, we can first review unnecessary costs.")],
                [("உங்கள் கருத்தை ஒரு அளவுக்கு ஒத்துக்கொள்கிறேன், இருப்பினும் அது தவறு.", "உங்கள் கருத்தை ஒரு அளவுக்கு ஒத்துக்கொள்கிறேன்; இருப்பினும் பாதுகாப்பைக் குறைக்க முடியாது.", "State the actual constraint rather than dismissing the whole proposal."), ("அதற்குப் பதிலாக செலவு குறைக்கலாம்.", "அதற்குப் பதிலாக, தேவையற்ற செலவை முதலில் ஆய்வு செய்யலாம்.", "Give a specific, feasible alternative.")],
                [("அருண்", "புதிய உபகரணம் செலவைக் குறைக்கும்.", "putiya upakaraṇam celavaik kuṟaikkum.", "The new equipment will reduce cost."), ("மீனா", "செலவைக் குறைக்க வேண்டும் என்ற கருத்தை ஒரு அளவுக்கு ஒத்துக்கொள்கிறேன்.", "celavaik kuṟaikka vēṇṭum eṉṟa karuttai oru aḷavukku ottukkoḷkiṟēṉ.", "I agree to some extent with reducing cost."), ("அருண்", "அப்படியானால் வாங்கலாமா?", "appaṭiyāṉāl vāṅkalāmā?", "Then shall we buy it?"), ("மீனா", "இருப்பினும் பாதுகாப்பை உறுதிப்படுத்த வேண்டும்; முதலில் தேவையற்ற செலவை ஆய்வு செய்வோம்.", "iruppiṉum pāṭukāppai uṟutippaṭutta vēṇṭum; mutalil tēvaiyaṟṟa celavai āyvu ceyvōm.", "Still, safety must be ensured; let us first review unnecessary costs.")],
                "Disagreement worksheet", [("Acknowledge and qualify.", ["I agree to some extent with reducing cost", "nevertheless, we cannot reduce safety"], ["செலவைக் குறைக்க வேண்டும் என்ற கருத்தை ஒரு அளவுக்கு ஒத்துக்கொள்கிறேன்", "இருப்பினும் பாதுகாப்பைக் குறைக்க முடியாது"]), ("Offer an alternative.", ["instead, we can review unnecessary costs first", "let us ensure safety"], ["அதற்குப் பதிலாக தேவையற்ற செலவை முதலில் ஆய்வு செய்யலாம்", "பாதுகாப்பை உறுதிப்படுத்துவோம்"])]),
            _spec_lesson(
                "கூட்டத்தில் முடிவெடுத்தல்",
                "Summarise a discussion and propose a next step that different people can "
                "accept. இதுவரை shows what has been done so far; இரு தரப்பும் keeps "
                "participants visible, and ... என்று முடிவு செய்தோம் reports the agreed "
                "decision.",
                [("கூட்டம்", "kūṭṭam", "meeting", "noun"), ("பங்கேற்பு", "paṅkēṟpu", "participation", "noun"), ("இரு தரப்பும்", "iru tarappum", "both sides", "phrase"), ("இதுவரை", "ituvarai", "so far", "adverb"), ("முடிவெடுத்தல்", "muṭiveṭuttal", "to decide", "verb")],
                "Summarising agreement", "இதுவரை ... · இரு தரப்பும் ... · ... என்று முடிவு செய்தோம்",
                "Start the summary with இதுவரை to refer to the discussion so far. "
                "இரு தரப்பும் makes both groups explicit. Report an agreed next step "
                "with என்று முடிவு செய்தோம்; do not claim agreement beyond what was settled.",
                [("இதுவரை இரு தரப்பும் தங்கள் கருத்துகளைப் பகிர்ந்தனர்.", "ituvarai iru tarappum taṅkaḷ karuttukaḷaip pakirnt aṉar.", "So far both sides have shared their views."), ("முதலில் சிறிய அளவில் திட்டத்தைச் சோதிக்கலாம் என்று முடிவு செய்தோம்.", "mutalil ciṟiya aḷavil tiṭṭattaic cōtikkalām eṉṟu muṭivu ceytōm.", "We decided to test the plan on a small scale first."), ("மாத முடிவில் முடிவுகளை மீண்டும் பார்ப்போம்.", "māta muṭivil muṭivukaḷai mīṇṭum pārppōm.", "We will review the results again at the end of the month.")],
                [("இரு தரப்பும் கருத்து பகிர்ந்தது.", "இரு தரப்பும் தங்கள் கருத்துகளைப் பகிர்ந்தனர்.", "Use plural agreement for both groups and mark the plural object."), ("திட்டம் சோதிக்கலாமென்று முடிவெடுத்தோம்.", "திட்டத்தைச் சிறிய அளவில் சோதிக்கலாம் என்று முடிவு செய்தோம்.", "State what will be tested and report the decision clearly.")],
                [("தலைவர்", "இதுவரை என்ன முடிவு?", "ituvarai eṉṉa muṭivu?", "What have we decided so far?"), ("மீனா", "இரு தரப்பும் தங்கள் கருத்துகளைப் பகிர்ந்தனர்.", "iru tarappum taṅkaḷ karuttukaḷaip pakirnt aṉar.", "Both sides shared their views."), ("தலைவர்", "அடுத்த படி என்ன?", "aṭutta paṭi eṉṉa?", "What is the next step?"), ("மீனா", "முதலில் சிறிய அளவில் திட்டத்தைச் சோதிக்கலாம் என்று முடிவு செய்தோம்.", "mutalil ciṟiya aḷavil tiṭṭattaic cōtikkalām eṉṟu muṭivu ceytōm.", "We decided to test the plan on a small scale first.")],
                "Meeting summary worksheet", [("Summarise the discussion.", ["both sides shared their views", "we have decided to test the plan on a small scale"], ["இரு தரப்பும் தங்கள் கருத்துகளைப் பகிர்ந்தனர்", "திட்டத்தைச் சிறிய அளவில் சோதிக்கலாம் என்று முடிவு செய்தோம்"]), ("Set the review.", ["we will review the results at the end of the month", "what is the next step?"], ["மாத முடிவில் முடிவுகளை மீண்டும் பார்ப்போம்", "அடுத்த படி என்ன?"])]),
        ]},
    ],
    "extra": EXTRA(
        culture=("In Tamil Nadu, eri or kanmai tanks store seasonal water and connect "
                 "agriculture with local decisions about access and upkeep. Research "
                 "on tank cascades describes water bodies linked through channels, "
                 "rather than as isolated ponds. Their operation can involve several "
                 "institutions and local users; therefore a report about one tank "
                 "should name its location and management arrangement. The vocabulary "
                 "of water-sharing — inflow, release, turn, downstream — belongs in "
                 "public discussion as much as in engineering."),
        source_url="https://www.frontiersin.org/journals/water/articles/10.3389/frwa.2025.1597293/full",
        reading=("ஏரியில் சேமித்த நீர் வயல்களுக்குச் செல்லும் கால்வாயில் "
                 "விடப்பட்டது. மேல்பகுதி விவசாயிகள் முதலில் நீர் பெற்றனர்; "
                 "கீழ்ப்பகுதி விவசாயிகளும் தங்கள் பங்கை கேட்டனர். கூட்டத்தில் "
                 "அட்டவணையைப் புதுப்பித்து, ஒவ்வொரு பகுதியின் தேவையையும் "
                 "பதிவு செய்ய முடிவு செய்தார்கள். ஆனால் மழை குறைந்தால் பழைய "
                 "அளவு போதாது. எனவே, நீர் திறக்கும் நேரத்தை மட்டும் அல்ல, "
                 "நீர்வரத்தையும் கண்காணிக்க வேண்டும் என்று பொறியாளர் கூறினார்."),
        reading_gloss=("Water stored in the tank was released into the channel leading "
                       "to the fields. Farmers in the upstream area received water "
                       "first; those downstream asked for their share too. At a meeting "
                       "they decided to update the schedule and record each area's "
                       "needs. But if rainfall falls, the old allocation will not be "
                       "enough. Therefore, the engineer said, we must monitor not only "
                       "the release time but also the inflow."),
        listening=("நீர் பகிர்வு அட்டவணையை மாற்ற வேண்டுமா? — மழை அளவைப் "
                   "பார்த்த பிறகு முடிவு செய்வோம். — கீழ்ப்பகுதிக்கு எப்போது "
                   "நீர் செல்லும்? — மேல்பகுதி பயன்பாடு முடிந்ததும், ஒப்புக்கொண்ட "
                   "நேரத்தில் திறக்கப்படும்."),
        listening_gloss=("Should we change the water-sharing schedule? — We will decide "
                         "after looking at the rainfall. — When will water reach the "
                         "downstream area? — After upstream use is complete, it will be "
                         "released at the agreed time."),
        voice_tag=VOICE,
        idioms=[
            ("கிணற்றுத் தவளை", "a frog in a well", "someone with a narrow view of the world"),
            ("ஆழம் தெரியாமல் காலை விடாதே", "do not step in without knowing the depth", "do not act before assessing the risk"),
            ("மண் குதிரையை நம்பி ஆற்றில் இறங்காதே", "do not enter the river trusting a clay horse", "do not rely on an unreliable support"),
            ("ஆற்றில் ஒரு கால், சேற்றில் ஒரு கால்", "one foot in the river, one in the mud", "to be committed to neither side"),
            ("தண்ணீரில் எழுதிய எழுத்து", "writing written on water", "something that will not last"),
            ("கையும் களவுமாகப் பிடித்தல்", "to catch with the hand and the theft", "to catch someone red-handed"),
            ("கையைப் பிசைதல்", "to wring one's hands", "to feel helpless or anxious"),
            ("கரை சேர்தல்", "to reach the shore", "to reach safety or complete a difficult task"),
            ("வேரோடு பிடுங்குதல்", "to pull up by the root", "to remove a problem completely"),
            ("நீர் இன்றி அமையாது உலகு", "the world cannot exist without water", "water is indispensable to life"),
        ],
        mistakes=[
            ("ஏரி நீர் விவசாயிகளுக்குச் செல்கிறது; கீழ்ப்பகுதியினர் இல்லை.", "ஏரி நீர் பகிர்வில் மேல்பகுதியும் கீழ்ப்பகுதியும் சேர்த்துக் கருதப்பட வேண்டும்.", "Do not omit the downstream users from a water-sharing account."),
            ("மழை குறைந்தால் பழைய அளவு போதும்.", "மழை குறைந்தால் பழைய அளவு போதாது.", "The negative suffix changes the conclusion: போதாது means is not enough."),
            ("நீர் அட்டவணை மாறும் என்று முடிவு செய்தார்கள் மழை.", "மழை அளவைப் பார்த்த பிறகு நீர் அட்டவணையை மாற்ற முடிவு செய்தார்கள்.", "Keep the evidence and the decision in their logical order."),
        ],
        task_title="நீர்ப் பகிர்வுக் கூட்டக் குறிப்பு",
        task_instructions=("Write a short meeting note about a water-sharing decision. Name the "
                           "tank or area, distinguish upstream from downstream users, state "
                           "the evidence the group considered, and list the agreed next "
                           "step. Include one uncertainty and say what should be monitored "
                           "before changing the allocation."),
    ),
    "test": [
        ("translate_en", "Say: We decided to test the plan on a small scale first.", "முதலில் சிறிய அளவில் திட்டத்தைச் சோதிக்கலாம் என்று முடிவு செய்தோம்."),
        ("translate_ta", "மழை அளவைப் பார்த்த பிறகு முடிவு செய்வோம்.", "We will decide after looking at the rainfall."),
        ("multiple_choice", "Which expression means 'to some extent'?", "ஒரு அளவுக்கு"),
        ("fill_in_the_blank", "மருத்துவமனை அருகில் ___, பேருந்து சேவை குறைவு.", "இருந்தாலும்"),
        ("word_selection", "Select the Tamil word for 'progress'.", "முன்னேற்றம்"),
        ("error_correction", "இந்தப் பகுதியில் பேருந்து சேவை மேம்படுத்த வேண்டும்.", "இந்தப் பகுதியில் பேருந்து சேவையை மேம்படுத்த வேண்டும்."),
        ("dialogue_completion", "ஒரு அளவுக்கு ஒத்துக்கொள்கிறேன்; ___, பாதுகாப்பைக் குறைக்க முடியாது.", "இருப்பினும்"),
        ("matching", "Match புகார் to its meaning.", "complaint"),
        ("reading_comprehension", "What did the meeting decide to update?", "the water-sharing schedule"),
        ("inference", "Why should the group monitor inflow as well as release time?", "because reduced rainfall may make the old allocation insufficient"),
        ("main_idea", "What is the reading mainly about?", "sharing tank water fairly using an updated schedule and evidence"),
        ("detail_identification", "Who asked for their share of the water?", "the downstream farmers"),
    ],
}

HALFSTEPS["B2+"] = {
    "native": NATIVE,
    "title": "Tamil B2+ — Official life, economy and research",
    "goals": [
        "Complete a formal request and ask how an application is being processed",
        "Discuss household costs using comparisons and a stated time period",
        "Explain a technical result, its assumptions, and a responsible next step",
    ],
    "units": [
        {"id": "B2+-U1", "title": "அலுவல் மற்றும் ஆவணங்கள்", "lessons": [
            _spec_lesson(
                "சான்றிதழுக்கான விண்ணப்பம்",
                "Request a certificate, attach the required documents, and ask when it will "
                "be issued. விண்ணப்பம் is an application; இணைக்கப்பட்டுள்ளன describes "
                "attached documents, and வழங்கப்படும் is a formal passive future.",
                [("சான்றிதழ்", "cāṉṟitaḻ", "certificate", "noun"), ("விண்ணப்பம்", "viṇṇappam", "application", "noun"), ("இணைப்பு", "iṇaippu", "attachment", "noun"), ("வழங்குதல்", "vaḻaṅkutal", "to issue, provide", "verb"), ("காலக்கெடு", "kālakkeṭu", "deadline", "noun")],
                "Formal application", "... விண்ணப்பிக்கிறேன் · ஆவணங்கள் இணைக்கப்பட்டுள்ளன · ... வழங்கப்படும்",
                "A formal request can use விண்ணப்பிக்கிறேன். List the attached documents "
                "with -உம் or a comma; இணைக்கப்பட்டுள்ளன agrees with plural ஆவணங்கள். "
                "Ask for the issue date using எப்போது வழங்கப்படும்?",
                [("பிறப்புச் சான்றிதழின் நகலுக்காக விண்ணப்பிக்கிறேன்.", "piṟappuc cāṉṟitaḻiṉ nakaluk kāka viṇṇappikkiṟēṉ.", "I am applying for a copy of the birth certificate."), ("அடையாள அட்டையும் முகவரிச் சான்றும் இணைக்கப்பட்டுள்ளன.", "aṭaiyāḷa aṭṭaiyum mukavaric cāṉṟum iṇaikkappaṭṭuḷḷaṉa.", "The identity card and proof of address are attached."), ("சான்றிதழ் பத்து வேலை நாட்களுக்குள் வழங்கப்படும்.", "cāṉṟitaḻ pattu vēlai nāṭkaḷukkuḷ vaḻaṅkappaṭum.", "The certificate will be issued within ten working days.")],
                [("சான்றிதழ் விண்ணப்பம் செய்கிறேன்.", "சான்றிதழுக்காக விண்ணப்பிக்கிறேன்.", "Use the verb விண்ணப்பிக்கிறேன் and mark what you apply for."), ("ஆவணங்கள் இணைக்கப்பட்டுள்ளது.", "ஆவணங்கள் இணைக்கப்பட்டுள்ளன.", "The plural subject ஆவணங்கள் takes plural agreement.")],
                [("விண்ணப்பதாரர்", "விண்ணப்பத்துடன் எந்த ஆவணங்கள் தேவை?", "viṇṇappattuṭaṉ enta āvaṇaṅkaḷ tēvai?", "Which documents are needed with the application?"), ("அலுவலர்", "அடையாள அட்டையும் முகவரிச் சான்றும் இணைக்கப்பட வேண்டும்.", "aṭaiyāḷa aṭṭaiyum mukavaric cāṉṟum iṇaikkappaṭa vēṇṭum.", "The identity card and proof of address must be attached."), ("விண்ணப்பதாரர்", "சான்றிதழ் எப்போது வழங்கப்படும்?", "cāṉṟitaḻ eppōtu vaḻaṅkappaṭum?", "When will the certificate be issued?"), ("அலுவலர்", "முழுமையான விண்ணப்பம் கிடைத்த பத்து வேலை நாட்களுக்குள்.", "muḻumaiyāṉa viṇṇappam kiṭaitta pattu vēlai nāṭkaḷukkuḷ.", "Within ten working days after we receive the complete application.")],
                "Certificate worksheet", [("State the request.", ["I am applying for a copy of the birth certificate", "the certificate will be issued within ten working days"], ["பிறப்புச் சான்றிதழின் நகலுக்காக விண்ணப்பிக்கிறேன்", "சான்றிதழ் பத்து வேலை நாட்களுக்குள் வழங்கப்படும்"]), ("List the attachments.", ["the identity card and proof of address are attached", "which documents are needed?"], ["அடையாள அட்டையும் முகவரிச் சான்றும் இணைக்கப்பட்டுள்ளன", "எந்த ஆவணங்கள் தேவை?"])]),
            _spec_lesson(
                "விண்ணப்ப நிலையை விசாரித்தல்",
                "Ask about the status of an application and respond to a request for "
                "additional information. பரிசீலனையில் means under review; கூடுதல் "
                "ஆவணம் is an additional document, and சமர்ப்பித்தவுடன் means once it "
                "is submitted.",
                [("நிலை", "nilai", "status", "noun"), ("பரிசீலனை", "paricīlaṉai", "review", "noun"), ("கூடுதல்", "kūṭutal", "additional", "adjective"), ("சமர்ப்பித்தல்", "camarppittal", "to submit", "verb"), ("விவரம்", "vivaram", "detail", "noun")],
                "Application status", "... பரிசீலனையில் உள்ளது · ... சமர்ப்பித்தவுடன் · நிலை என்ன?",
                "Use பரிசீலனையில் உள்ளது to report a file under review. A completed action "
                "with -வுடன் means 'once it is done': ஆவணம் சமர்ப்பித்தவுடன். Ask the "
                "status politely with விண்ணப்பத்தின் நிலை என்ன?",
                [("என் விண்ணப்பம் தற்போது பரிசீலனையில் உள்ளது.", "eṉ viṇṇappam taṟpōtu paricīlaṉaiyil uḷḷatu.", "My application is currently under review."), ("கூடுதல் விவரம் தேவைப்பட்டால் எனக்குத் தெரிவிக்கவும்.", "kūṭutal vivaram tēvaippaṭṭāl eṉakkut terivikkavum.", "Please let me know if further information is needed."), ("ஆவணம் சமர்ப்பித்தவுடன் செயல்முறை தொடரும்.", "āvaṇam camarppittavuṭaṉ ceyalmuṟai toṭarum.", "The process will continue once the document is submitted.")],
                [("என் விண்ணப்பம் பரிசீலனையில் இருக்கிறார்கள்.", "என் விண்ணப்பம் பரிசீலனையில் உள்ளது.", "விண்ணப்பம் is singular and takes உள்ளது."), ("ஆவணம் சமர்ப்பித்த பிறகு உடனே செயல்முறை தொடர்ந்தது. (future)", "ஆவணம் சமர்ப்பித்தவுடன் செயல்முறை தொடரும்.", "Use -வுடன் for 'once submitted' and future tense for the next step.")],
                [("விண்ணப்பதாரர்", "என் விண்ணப்பத்தின் நிலை என்ன?", "eṉ viṇṇappattiṉ nilai eṉṉa?", "What is the status of my application?"), ("அலுவலர்", "அது தற்போது பரிசீலனையில் உள்ளது.", "atu taṟpōtu paricīlaṉaiyil uḷḷatu.", "It is currently under review."), ("விண்ணப்பதாரர்", "கூடுதல் ஆவணம் தேவையா?", "kūṭutal āvaṇam tēvaiyā?", "Is an additional document needed?"), ("அலுவலர்", "ஆம். அதைச் சமர்ப்பித்தவுடன் செயல்முறை தொடரும்.", "ām. ataic camarppittavuṭaṉ ceyalmuṟai toṭarum.", "Yes. Once you submit it, the process will continue.")],
                "Status worksheet", [("Ask for status.", ["what is the status of my application?", "it is currently under review"], ["என் விண்ணப்பத்தின் நிலை என்ன?", "அது தற்போது பரிசீலனையில் உள்ளது"]), ("Ask for the next step.", ["is another document needed?", "once you submit it, the process will continue"], ["கூடுதல் ஆவணம் தேவையா?", "அதைச் சமர்ப்பித்தவுடன் செயல்முறை தொடரும்"])]),
            _spec_lesson(
                "படிவத்தில் திருத்தம் கோருதல்",
                "Ask to correct a spelling or date on a form, and confirm the correction in "
                "writing. தவறுதலாக means by mistake; திருத்தம் கோருகிறேன் is a formal "
                "request, and சரிபார்த்த பின் marks the next check.",
                [("படிவம்", "paṭivam", "form", "noun"), ("எழுத்துப்பிழை", "eḻuttuppiḻai", "spelling error", "noun"), ("திருத்தம்", "tiruttam", "correction", "noun"), ("தவறுதலாக", "tavaṟutalāka", "by mistake", "adverb"), ("சரிபார்த்தல்", "caripārttal", "to verify", "verb")],
                "Requesting a correction", "... தவறுதலாக ... · திருத்தம் கோருகிறேன் · சரிபார்த்த பின் ...",
                "State the field and the correct value: பெயரில் எழுத்துப்பிழை உள்ளது. Use "
                "திருத்தம் கோருகிறேன் for a formal request. சரிபார்த்த பின் means after "
                "checking, and lets both sides confirm the change.",
                [("படிவத்தில் என் பெயர் தவறுதலாக மாறியுள்ளது.", "paṭivattil eṉ peyar tavaṟutalāka māṟiyuḷḷatu.", "My name has been changed by mistake on the form."), ("எழுத்துப்பிழையைச் சரிசெய்யத் திருத்தம் கோருகிறேன்.", "eḻuttuppiḻaiyaic cariceyyat tiruttam kōrukiṟēṉ.", "I request a correction to fix the spelling error."), ("திருத்தப்பட்ட விவரத்தைச் சரிபார்த்த பின் கையொப்பமிடுவேன்.", "tiruttappaṭṭa vivarattaic caripārtta piṉ kaiyoppamiṭuvēṉ.", "I will sign after checking the corrected details.")],
                [("என் பெயர் தவறாக மாறுகிறது.", "படிவத்தில் என் பெயர் தவறுதலாக மாறியுள்ளது.", "Use the present perfect to report an existing error on the form."), ("திருத்தம் கோரி.", "திருத்தம் கோருகிறேன்.", "Complete the formal request with a finite verb.")],
                [("விண்ணப்பதாரர்", "படிவத்தில் பெயர் தவறுதலாக மாறியுள்ளது.", "paṭivattil peyar tavaṟutalāka māṟiyuḷḷatu.", "The name has been changed by mistake on the form."), ("அலுவலர்", "திருத்தத்திற்கான ஆதாரம் உள்ளதா?", "tiruttattiṟkāṉa ātāram uḷḷatā?", "Do you have evidence for the correction?"), ("விண்ணப்பதாரர்", "ஆம், அடையாள அட்டையை இணைத்துள்ளேன்.", "ām, aṭaiyāḷa aṭṭaiyai iṇaittuḷḷēṉ.", "Yes, I have attached my identity card."), ("அலுவலர்", "சரிபார்த்த பின் புதுப்பிக்கப்பட்ட படிவத்தை வழங்குகிறேன்.", "caripārtta piṉ putuppikkappaṭṭa paṭivattai vaḻaṅkukiṟēṉ.", "After verifying it, I will provide the updated form.")],
                "Form correction worksheet", [("Explain the error.", ["my name has been changed by mistake on the form", "I request a correction to the spelling"], ["படிவத்தில் என் பெயர் தவறுதலாக மாறியுள்ளது", "எழுத்துப்பிழைக்கு திருத்தம் கோருகிறேன்"]), ("Confirm the follow-up.", ["I attached my identity card", "I will sign after checking the corrected details"], ["அடையாள அட்டையை இணைத்துள்ளேன்", "திருத்தப்பட்ட விவரத்தைச் சரிபார்த்த பின் கையொப்பமிடுவேன்"])]),
        ]},
        {"id": "B2+-U2", "title": "பொருளாதாரமும் அன்றாட வாழ்வும்", "lessons": [
            _spec_lesson(
                "மாதச் செலவுத் திட்டம்",
                "Describe a monthly household budget and explain why one category increased. "
                "மாதாந்திரம் marks a monthly period; ஒதுக்கீடு is an allocation, and "
                "ஒப்பிடும்போது introduces a comparison.",
                [("மாதாந்திரம்", "mātāntiram", "monthly", "adverb"), ("ஒதுக்கீடு", "otukkīṭu", "allocation", "noun"), ("வாடகை", "vāṭakai", "rent", "noun"), ("மின்சாரம்", "miṉcāram", "electricity", "noun"), ("உயர்வு", "uyarvu", "increase", "noun")],
                "Budget categories", "...க்கான ஒதுக்கீடு · கடந்த மாதத்துடன் ஒப்பிடும்போது ...",
                "Use -க்கான to say what an allocation is for: உணவுக்கான ஒதுக்கீடு. "
                "ஒப்பிடும்போது introduces the earlier period; explain what changed and "
                "why, without treating one household's budget as a national average.",
                [("இந்த மாதம் மின்சாரத்திற்கான ஒதுக்கீடு உயர்ந்துள்ளது.", "inta mātam miṉcārattiṟkāṉa otukkīṭu uyarntuḷḷatu.", "This month's electricity allocation has increased."), ("கடந்த மாதத்துடன் ஒப்பிடும்போது வாடகை மாறவில்லை.", "kaṭanta mātattuṭaṉ oppiṭumpōtu vāṭakai māṟavillai.", "Compared with last month, the rent has not changed."), ("மின்சாரப் பயன்பாடு அதிகரித்ததால் செலவு உயர்ந்தது.", "miṉcārap payaṉpāṭu atikarittatāl celavu uyarntatu.", "The cost rose because electricity use increased.")],
                [("கடந்த மாதம் ஒப்பிடும்போது வாடகை மாறவில்லை.", "கடந்த மாதத்துடன் ஒப்பிடும்போது வாடகை மாறவில்லை.", "Use -உடன் to mark the comparison point."), ("மின்சாரப் பயன்பாடு அதிகரித்ததால் செலவு உயர்கிறது. (last month)", "மின்சாரப் பயன்பாடு அதிகரித்ததால் செலவு உயர்ந்தது.", "Use past tense for a change that occurred last month.")],
                [("மீனா", "இந்த மாதம் எந்தச் செலவு உயர்ந்தது?", "inta mātam entac celavu uyarntatu?", "Which expense increased this month?"), ("கவி", "மின்சாரத்திற்கான ஒதுக்கீடு உயர்ந்துள்ளது.", "miṉcārattiṟkāṉa otukkīṭu uyarntuḷḷatu.", "The electricity allocation has increased."), ("மீனா", "வாடகையும் உயர்ந்ததா?", "vāṭakaiyum uyarntatā?", "Did the rent also increase?"), ("கவி", "இல்லை; மின்சாரப் பயன்பாடு அதிகரித்ததால் மட்டும் செலவு உயர்ந்தது.", "illai; miṉcārap payaṉpāṭu atikarittatāl maṭṭum celavu uyarntatu.", "No; only the cost rose because electricity use increased.")],
                "Budget worksheet", [("Compare the months.", ["compared with last month, the rent has not changed", "the electricity allocation has increased"], ["கடந்த மாதத்துடன் ஒப்பிடும்போது வாடகை மாறவில்லை", "மின்சாரத்திற்கான ஒதுக்கீடு உயர்ந்துள்ளது"]), ("Explain the cost.", ["the cost rose because electricity use increased", "only the electricity cost increased"], ["மின்சாரப் பயன்பாடு அதிகரித்ததால் செலவு உயர்ந்தது", "மின்சாரச் செலவு மட்டும் உயர்ந்தது"])]),
            _spec_lesson(
                "விலை மற்றும் வருமானத்தை ஒப்பிடுதல்",
                "Compare prices over a stated period and distinguish a percentage change "
                "from a rupee amount. விலை உயர்வு is a price increase; வருமானம் is "
                "income, and அதற்கேற்ப asks whether a budget changed accordingly.",
                [("விலை உயர்வு", "vilai uyarvu", "price increase", "phrase"), ("வருமானம்", "varumāṉam", "income", "noun"), ("சதவீதம்", "catavītam", "percent", "noun"), ("குடும்பச் செலவு", "kuṭumpac celavu", "household expense", "phrase"), ("அதற்கேற்ப", "ataṟkēṟpa", "accordingly", "adverb")],
                "Prices and household impact", "... சதவீதம் உயர்ந்தது · வருமானம் அதே அளவில் ... இல்லை",
                "State the period and unit for a price change: மூன்று மாதங்களில் ஐந்து "
                "சதவீதம். Do not confuse the percentage with the rupee amount. Compare "
                "the household's income with the increase using அதற்கேற்ப.",
                [("மூன்று மாதங்களில் அரிசி விலை ஐந்து சதவீதம் உயர்ந்தது.", "mūṉṟu mātaṅkaḷil arici vilai aintu catavītam uyarntatu.", "The price of rice rose by five percent in three months."), ("குடும்ப வருமானம் அதற்கேற்ப உயரவில்லை.", "kuṭumpa varumāṉam ataṟkēṟpa uyaravillai.", "Household income did not rise accordingly."), ("எனவே உணவுச் செலவுக்கான திட்டத்தை மறுபரிசீலனை செய்கிறோம்.", "eṉavē uṇavuc celavukkāṉa tiṭṭattai maṟuparicīlaṉai ceykiṟōm.", "Therefore we are reviewing the food budget.")],
                [("ஐந்து ரூபாய் சதவீதம் விலை உயர்ந்தது.", "விலை ஐந்து சதவீதம் உயர்ந்தது.", "Keep the unit 'percent' attached to the measured change, not the currency."), ("வருமானம் அதற்கேற்ப உயர்ந்தது இல்லை.", "வருமானம் அதற்கேற்ப உயரவில்லை.", "Use the negative verb form உயரவில்லை.")],
                [("அருண்", "அரிசி விலை எவ்வளவு மாறியது?", "arici vilai evvaḷavu māṟiyatu?", "How much did the price of rice change?"), ("கவி", "மூன்று மாதங்களில் ஐந்து சதவீதம் உயர்ந்தது.", "mūṉṟu mātaṅkaḷil aintu catavītam uyarntatu.", "It rose by five percent in three months."), ("அருண்", "வருமானமும் உயர்ந்ததா?", "varumāṉamum uyarntatā?", "Did income rise too?"), ("கவி", "இல்லை. அதனால் உணவுச் செலவுத் திட்டத்தை மறுபரிசீலனை செய்கிறோம்.", "illai. ataṉāl uṇavuc celavuttiṭṭattai maṟuparicīlaṉai ceykiṟōm.", "No. Therefore we are reviewing the food budget.")],
                "Price worksheet", [("Report the percentage.", ["the price rose by five percent in three months", "household income did not rise accordingly"], ["மூன்று மாதங்களில் விலை ஐந்து சதவீதம் உயர்ந்தது", "குடும்ப வருமானம் அதற்கேற்ப உயரவில்லை"]), ("State the response.", ["we are reviewing the food budget", "income did not increase"], ["உணவுச் செலவுத் திட்டத்தை மறுபரிசீலனை செய்கிறோம்", "வருமானம் உயரவில்லை"])]),
            _spec_lesson(
                "வாடகை ஒப்பந்தத்தைப் புரிந்துகொள்ளுதல்",
                "Ask about a rent increase, notice period, and which costs are included. "
                "ஒப்பந்தம் is a contract; முன் அறிவிப்பு is prior notice, and சேர்க்கப்படவில்லை "
                "says that a cost is not included.",
                [("ஒப்பந்தம்", "oppantam", "contract", "noun"), ("முன் அறிவிப்பு", "muṉaṟivippu", "prior notice", "phrase"), ("சேர்க்கை", "cērkkai", "inclusion", "noun"), ("பராமரிப்புக் கட்டணம்", "paramarippuk kaṭṭaṇam", "maintenance fee", "phrase"), ("புதுப்பித்தல்", "putuppittal", "renewal", "noun")],
                "Clarifying a contract", "... ஒப்பந்தத்தில் · முன் அறிவிப்பு இல்லாமல் ... முடியாது · ... சேர்க்கப்படவில்லை",
                "Ask which clause governs a change: ஒப்பந்தத்தில் எந்த விதி? A rent change "
                "may require முன் அறிவிப்பு; distinguish the rent from a separate "
                "maintenance fee using சேர்க்கப்படவில்லை.",
                [("ஒப்பந்தத்தில் வாடகை உயர்வுக்கான விதி எது?", "oppantattil vāṭakai uyarvukkāṉa viti etu?", "Which clause in the contract covers a rent increase?"), ("முன் அறிவிப்பு இல்லாமல் வாடகை உயர்த்த முடியாது.", "muṉaṟivippu illāmal vāṭakai uyar tta muṭiyātu.", "The rent cannot be raised without prior notice."), ("பராமரிப்புக் கட்டணம் வாடகையில் சேர்க்கப்படவில்லை.", "paramarippuk kaṭṭaṇam vāṭakaiyil cērkkappaṭavillai.", "The maintenance fee is not included in the rent.")],
                [("வாடகை உயர்த்த முடியாது முன் அறிவிப்பு.", "முன் அறிவிப்பு இல்லாமல் வாடகை உயர்த்த முடியாது.", "Use இல்லாமல் to state a condition that must be met."), ("பராமரிப்புக் கட்டணம் வாடகையில் சேர்க்கவில்லை.", "பராமரிப்புக் கட்டணம் வாடகையில் சேர்க்கப்படவில்லை.", "Use the passive negative when the fee is not included in the contract.")],
                [("குடியிருப்பவர்", "ஒப்பந்தத்தில் வாடகை உயர்வுக்கான விதி எது?", "oppantattil vāṭakai uyarvukkāṉa viti etu?", "Which clause covers a rent increase?"), ("நிர்வாகி", "மூன்று மாத முன் அறிவிப்பு தேவை.", "mūṉṟu māta muṉaṟivippu tēvai.", "Three months' notice is required."), ("குடியிருப்பவர்", "பராமரிப்புக் கட்டணம் வாடகையில் சேர்க்கப்பட்டுள்ளதா?", "paramarippuk kaṭṭaṇam vāṭakaiyil cērkkappaṭṭuḷḷatā?", "Is the maintenance fee included in the rent?"), ("நிர்வாகி", "இல்லை; ஒப்பந்தத்தில் அது தனியாகக் குறிப்பிடப்பட்டுள்ளது.", "illai; oppantattil atu taṉiyākak kuṟippiṭappaṭṭuḷḷatu.", "No; it is stated separately in the contract.")],
                "Rent contract worksheet", [("Ask about the clause.", ["which clause covers a rent increase?", "three months' notice is required"], ["வாடகை உயர்வுக்கான விதி எது?", "மூன்று மாத முன் அறிவிப்பு தேவை"]), ("Clarify included costs.", ["is the maintenance fee included in the rent?", "it is stated separately"], ["பராமரிப்புக் கட்டணம் வாடகையில் சேர்க்கப்பட்டுள்ளதா?", "அது தனியாகக் குறிப்பிடப்பட்டுள்ளது"])]),
        ]},
        {"id": "B2+-U3", "title": "அறிவியலும் தொழில்நுட்பமும்", "lessons": [
            _spec_lesson(
                "தொழில்நுட்பக் கோளாறைத் தெரிவிப்பது",
                "Describe when a technical problem began, what works, and what does not. "
                "கோளாறு is a fault; பதிவேற்றம் is an upload, and மீண்டும் முயன்றும் "
                "introduces an unsuccessful attempt.",
                [("தொழில்நுட்பம்", "toḻilnuṭpam", "technology", "noun"), ("கோளாறு", "kōḷāṟu", "fault, issue", "noun"), ("பதிவேற்றம்", "pativēṟṟam", "upload", "noun"), ("மீண்டும்", "mīṇṭum", "again", "adverb"), ("செய்திப் பதிவு", "ceytip pativu", "error log", "phrase")],
                "Troubleshooting", "... முதல் கோளாறு · மீண்டும் முயன்றும் ...வில்லை · பதிவு இணைத்துள்ளேன்",
                "State when the fault began with ... முதல். Use முயன்றும் plus a negative "
                "verb to say an attempt failed. Attach an error log with இணைத்துள்ளேன் "
                "so support can reproduce the problem.",
                [("நேற்று முதல் பதிவேற்றக் கோளாறு உள்ளது.", "nēṟṟu mutal pativēṟṟak kōḷāṟu uḷḷatu.", "There has been an upload issue since yesterday."), ("மீண்டும் முயன்றும் கோப்பு அனுப்பப்படவில்லை.", "mīṇṭum muyaṉṟum kōppu aṉuppappaṭavillai.", "Even after trying again, the file was not sent."), ("பிழைச் செய்திப் பதிவை இணைத்துள்ளேன்.", "piḻaic ceytip pativai iṇaittuḷḷēṉ.", "I have attached the error log.")],
                [("மீண்டும் முயன்றேன் கோப்பு அனுப்பப்படவில்லை.", "மீண்டும் முயன்றும் கோப்பு அனுப்பப்படவில்லை.", "Use -உம் after the participle to mean 'even after trying'."), ("பிழை பதிவை இணைத்தேன் உள்ளது.", "பிழைச் செய்திப் பதிவை இணைத்துள்ளேன்.", "Use one completed-action form, not two competing tense markers.")],
                [("பயனர்", "பதிவேற்றம் எப்போது நின்றது?", "pativēṟṟam eppōtu niṉṟatu?", "When did the upload stop?"), ("தொழில்நுட்ப உதவி", "நேற்று முதல் கோளாறு உள்ளதா?", "nēṟṟu mutal kōḷāṟu uḷḷatā?", "Has there been an issue since yesterday?"), ("பயனர்", "ஆம். மீண்டும் முயன்றும் கோப்பு அனுப்பப்படவில்லை.", "ām. mīṇṭum muyaṉṟum kōppu aṉuppappaṭavillai.", "Yes. Even after trying again, the file was not sent."), ("தொழில்நுட்ப உதவி", "செய்திப் பதிவை அனுப்புங்கள்; காரணத்தைச் சரிபார்க்கிறோம்.", "ceytip pativai aṉuppuṅkaḷ; kāraṇattaic caripārkkiṟōm.", "Send the error log; we will check the cause.")],
                "Technical support worksheet", [("Report the fault.", ["there has been an upload issue since yesterday", "the file was not sent even after trying again"], ["நேற்று முதல் பதிவேற்றக் கோளாறு உள்ளது", "மீண்டும் முயன்றும் கோப்பு அனுப்பப்படவில்லை"]), ("Give support the evidence.", ["I have attached the error log", "we will check the cause"], ["பிழைச் செய்திப் பதிவை இணைத்துள்ளேன்", "காரணத்தைச் சரிபார்க்கிறோம்"])]),
            _spec_lesson(
                "தரவு பகிர்வும் தனியுரிமையும்",
                "Ask what data an application collects and how long it is retained. "
                "தனியுரிமை is privacy; சேகரிக்கப்படும் is passive, and எதற்காக asks "
                "for the purpose. Distinguish required data from optional fields.",
                [("தனியுரிமை", "taṉiyurimai", "privacy", "noun"), ("தரவு", "taravu", "data", "noun"), ("சேகரித்தல்", "cēkarittal", "to collect", "verb"), ("நோக்கம்", "nōkkam", "purpose", "noun"), ("விருப்பத் தேர்வு", "viruppat tērvu", "optional choice", "phrase")],
                "Purpose and retention", "எந்தத் தரவு சேகரிக்கப்படுகிறது? · எதற்காக? · எவ்வளவு காலம்?",
                "Ask what is collected, why, and how long it is stored. The passive "
                "சேகரிக்கப்படுகிறது focuses on the data; எதற்காக identifies the purpose. "
                "Use கட்டாயம் and விருப்பம் to separate required and optional information.",
                [("மின்னஞ்சல் முகவரி கணக்கு பாதுகாப்பிற்காக சேகரிக்கப்படுகிறது.", "miṉṉañcal mukavari kaṇakku pāṭukāppirkāka cēkarikkappaṭukiṟatu.", "The email address is collected for account security."), ("விளம்பர விருப்பங்கள் தனியாகத் தேர்ந்தெடுக்கப்படுகின்றன.", "viḷampara viruppaṅkaḷ taṉiyākat tēṟnteṭukkappaṭukiṉṟaṉa.", "Advertising preferences are selected separately."), ("பயனர் கணக்கை நீக்கிய பின் தரவு எவ்வளவு காலம் வைக்கப்படும்?", "payaṉar kaṇakkai nīkkiya piṉ taravu evvaḷavu kālam vaikkappaṭum?", "How long is data kept after a user deletes an account?")],
                [("எந்தத் தரவு சேகரிக்கிறார்கள்?", "எந்தத் தரவு சேகரிக்கப்படுகிறது?", "Use the passive when the collector is not specified."), ("மின்னஞ்சல் முகவரி விளம்பரத்திற்காக மட்டும் சேகரிக்கப்படுகிறது. (security)", "மின்னஞ்சல் முகவரி கணக்கு பாதுகாப்பிற்காக சேகரிக்கப்படுகிறது.", "State the actual purpose rather than substituting an unrelated one.")],
                [("பயனர்", "என் மின்னஞ்சல் முகவரி எதற்காகச் சேகரிக்கப்படுகிறது?", "eṉ miṉṉañcal mukavari etaṟkākac cēkarikkappaṭukiṟatu?", "Why is my email address collected?"), ("ஆதரவு", "கணக்கு பாதுகாப்பிற்காக; விளம்பரத் தேர்வு விருப்பமானது.", "kaṇakku pāṭukāppirkāka; viḷamparat tērvu viruppamāṉatu.", "For account security; advertising choices are optional."), ("பயனர்", "கணக்கை நீக்கிய பின் தரவு எவ்வளவு காலம் இருக்கும்?", "kaṇakkai nīkkiya piṉ taravu evvaḷavu kālam irukkum?", "How long will the data remain after I delete my account?"), ("ஆதரவு", "கொள்கையில் காலவரம்பு குறிப்பிடப்பட்டுள்ளது; இணைப்பை அனுப்புகிறேன்.", "koḷkaiyil kāl avarampu kuṟippiṭappaṭṭuḷḷatu; iṇaippai aṉuppukiṟēṉ.", "The policy states a retention period; I will send the link.")],
                "Privacy worksheet", [("Ask about collection.", ["why is my email address collected?", "advertising choice is optional"], ["என் மின்னஞ்சல் முகவரி எதற்காகச் சேகரிக்கப்படுகிறது?", "விளம்பரத் தேர்வு விருப்பமானது"]), ("Ask about retention.", ["how long will the data remain after deletion?", "the policy states a retention period"], ["நீக்கிய பின் தரவு எவ்வளவு காலம் இருக்கும்?", "கொள்கையில் காலவரம்பு குறிப்பிடப்பட்டுள்ளது"])]),
            _spec_lesson(
                "ஆய்வு முடிவை விளக்குதல்",
                "Present a technical finding with its sample size and limitation. கண்டறிதல் "
                "is a finding; பங்கேற்பாளர் is a participant, and ... மட்டுமே "
                "limits a result to what the study actually tested.",
                [("கண்டறிதல்", "kaṇṭaṟital", "finding", "noun"), ("பங்கேற்பாளர்", "paṅkēṟpāḷar", "participant", "noun"), ("மாதிரி அளவு", "mātiri aḷavu", "sample size", "phrase"), ("வரம்பு", "varampu", "limitation", "noun"), ("பொதுமைப்படுத்துதல்", "potumaippaṭuttutal", "to generalise", "verb")],
                "Sample and limitation", "... பேரில் ஆய்வு · ... மட்டுமே காட்டுகிறது · இதை எல்லோருக்கும் பொதுமைப்படுத்த முடியாது",
                "Report the sample first: 120 பங்கேற்பாளர்களிடம். State what the result "
                "shows, then name its limitation. A sample finding should not be "
                "generalised to an untested population.",
                [("120 பங்கேற்பாளர்களிடம் நடத்தப்பட்ட ஆய்வு இந்தப் போக்கை மட்டும் காட்டுகிறது.", "120 paṅkēṟpāḷarkaḷiṭam naṭattappaṭṭa āyvu intap pōkkai maṭṭum kāṭṭukiṟatu.", "The study of 120 participants shows only this trend."), ("மாதிரி அளவு சிறியதால், முடிவை எல்லோருக்கும் பொதுமைப்படுத்த முடியாது.", "mātiri aḷavu ciṟiyatāl, muṭivai ellōrukkum potumaippaṭutta muṭiyātu.", "Because the sample is small, the result cannot be generalised to everyone."), ("அடுத்த ஆய்வில் வேறு வயதுக் குழுவையும் சேர்க்க வேண்டும்.", "aṭutta āyv il vēṟu vay atuk kuḻuvaiyum cērkka vēṇṭum.", "The next study should include another age group too.")],
                [("120 பேர் ஆய்வு எல்லோருக்கும் பொருந்துகிறது.", "120 பங்கேற்பாளர்களின் ஆய்வு இந்த மாதிரியில் ஒரு போக்கைக் காட்டுகிறது.", "State the sample and its limited result rather than generalising."), ("மாதிரி அளவு சிறியது முடிவு பொதுமைப்படுத்த முடியாது.", "மாதிரி அளவு சிறியதால் முடிவைப் பொதுமைப்படுத்த முடியாது.", "Connect the cause with -தால்.")],
                [("ஆய்வாளர்", "முக்கியக் கண்டறிதல் என்ன?", "mukkiyak kaṇṭaṟital eṉṉa?", "What is the main finding?"), ("ஆய்வு உதவியாளர்", "120 பங்கேற்பாளர்களிடம் இந்தப் போக்கு தெரிந்தது.", "120 paṅkēṟpāḷarkaḷiṭam intap pōkku terintatu.", "This trend appeared among 120 participants."), ("ஆய்வாளர்", "அதை எல்லா வயதினருக்கும் பொருந்தும் என்று கூறலாமா?", "atai ellā vayatiṉarukkum poruntum eṉṟu kūṟalāmā?", "Can we say it applies to all age groups?"), ("ஆய்வு உதவியாளர்", "இல்லை. அடுத்த ஆய்வில் வேறு வயதுக் குழுவையும் சேர்க்க வேண்டும்.", "illai. aṭutta āyvil vēṟu vay atuk kuḻuvaiyum cērkka vēṇṭum.", "No. The next study should include another age group.")],
                "Research finding worksheet", [("State the result.", ["the study included 120 participants", "the result cannot be generalised to everyone"], ["ஆய்வில் 120 பங்கேற்பாளர்கள் இருந்தனர்", "முடிவை எல்லோருக்கும் பொதுமைப்படுத்த முடியாது"]), ("Name the next step.", ["include another age group in the next study", "state the sample size"], ["அடுத்த ஆய்வில் வேறு வயதுக் குழுவையும் சேர்க்க வேண்டும்", "மாதிரி அளவைத் தெரிவிக்கவும்"])]),
        ]},
    ],
    "extra": EXTRA(
        culture=("Bharatanatyam uses rhythm and gesture as parts of a performed language. "
                 "Britannica describes its footwork as marking complex counter-rhythms "
                 "and its expressive sections as using conventional hand gestures and "
                 "facial expression to tell a story. That is why a short programme note "
                 "should not translate every gesture as a fixed one-word code: the "
                 "meaning depends on sequence, character, music, and the performance "
                 "context. A viewer can describe what is visible before interpreting "
                 "what it signifies."),
        source_url="https://www.britannica.com/art/bharata-natyam",
        reading=("நடனத்தில் கை அசைவும் முகபாவமும் கதையைச் சொல்கின்றன. ஆனால் "
                 "ஒரு முத்திரைக்கு எல்லா நிகழ்ச்சிகளிலும் ஒரே பொருள் என்று "
                 "கூற முடியாது. பாடலின் வரி, தாளம், கதாபாத்திரம் ஆகியவற்றுடன் "
                 "அந்த அசைவு சேர்ந்து பொருள் பெறுகிறது. விமர்சகர் முதலில் "
                 "நடனக் கலைஞர் என்ன செய்கிறார் என்பதை விவரிக்கிறார்; பின்னர் "
                 "அது எந்த உணர்வை உருவாக்குகிறது என்று விளக்குகிறார். இதனால் "
                 "பார்வையும் விளக்கமும் ஒன்றாகக் கலக்காமல் தெளிவாக இருக்கும்."),
        reading_gloss=("In dance, hand movement and facial expression tell the story. "
                       "But we cannot say that one mudra has the same meaning in every "
                       "performance. The gesture gets meaning together with the song's "
                       "line, rhythm, and character. The critic first describes what the "
                       "dancer does; then the critic explains what feeling it creates. "
                       "This keeps observation and interpretation distinct."),
        listening=("இந்த முத்திரை எதை உணர்த்துகிறது? — அது எந்தச் சூழலில் "
                   "வருகிறது என்பதைப் பார்க்க வேண்டும். — முகபாவம் மட்டும் போதுமா? "
                   "— இல்லை; தாளமும் கதாபாத்திரமும் சேர்ந்து பொருள் உருவாக்குகின்றன."),
        listening_gloss=("What does this hand gesture express? — We need to see the "
                         "context in which it appears. — Is facial expression alone "
                         "enough? — No; rhythm and character together create the meaning."),
        voice_tag=VOICE,
        idioms=[
            ("கை வண்ணம்", "the colour of the hand", "a person's skill in making or performing"),
            ("தாளம் தவறுதல்", "to miss the rhythm", "to lose the rhythm or go out of step"),
            ("கண் பேசுதல்", "the eyes speak", "to communicate a feeling without words"),
            ("முகம் சுளித்தல்", "to wrinkle the face", "to show displeasure"),
            ("நெஞ்சை உருக்குதல்", "to melt the heart", "to move someone deeply"),
            ("கால் பதித்தல்", "to set foot", "to enter or establish oneself in a place"),
            ("முகமூடி அணிதல்", "to wear a mask", "to conceal one's real intention"),
            ("கண் கவர்தல்", "to attract the eye", "to be visually striking"),
            ("அடி மேல் அடி", "step upon step", "one event or difficulty after another"),
            ("ஆட்டம் காணுதல்", "to see the dance", "to watch a situation unfold, often with uncertainty"),
        ],
        mistakes=[
            ("இந்த முத்திரை எப்போதும் ஒரே பொருள்.", "இந்த முத்திரையின் பொருள் நிகழ்ச்சிச் சூழலைப் பொறுத்து மாறலாம்.", "Gesture meanings are contextual, not a universal one-to-one code."),
            ("நடனக் கலைஞர் தாளத்தை தவறினார்.", "நடனக் கலைஞர் தாளத்தைத் தவறவிட்டார்.", "Use the idiomatic verb தவறவிடு for missing a rhythm."),
            ("முகபாவம் மட்டும் கதையை முழுமையாகச் சொல்கிறது.", "முகபாவம், கை அசைவு, தாளம் ஆகியவை இணைந்து கதையை உருவாக்குகின்றன.", "Do not isolate one expressive element from the performance sequence."),
        ],
        task_title="நிகழ்ச்சிக் குறிப்பை எழுதுதல்",
        task_instructions=("Write a short programme note for a dance excerpt. First describe two "
                           "observable actions (foot rhythm, hand gesture, or facial expression); "
                           "then offer one interpretation and name the context that supports it. "
                           "Mark uncertainty where the gesture could have more than one meaning, "
                           "and avoid presenting an interpretation as a universal code."),
    ),
    "test": [
        ("translate_en", "Say: The certificate will be issued within ten working days.", "சான்றிதழ் பத்து வேலை நாட்களுக்குள் வழங்கப்படும்."),
        ("translate_ta", "மாதிரி அளவு சிறியதால், முடிவைப் பொதுமைப்படுத்த முடியாது.", "Because the sample is small, the result cannot be generalised."),
        ("multiple_choice", "Which phrase asks for an application status?", "விண்ணப்பத்தின் நிலை என்ன?"),
        ("fill_in_the_blank", "கடந்த மாதத்துடன் ___ வாடகை மாறவில்லை.", "ஒப்பிடும்போது"),
        ("word_selection", "Select the Tamil word for 'privacy'.", "தனியுரிமை"),
        ("error_correction", "ஆவணங்கள் இணைக்கப்பட்டுள்ளது.", "ஆவணங்கள் இணைக்கப்பட்டுள்ளன."),
        ("dialogue_completion", "விண்ணப்பத்தின் நிலை என்ன? — அது தற்போது ___ உள்ளது.", "பரிசீலனையில்"),
        ("matching", "Match முன் அறிவிப்பு to its meaning.", "prior notice"),
        ("reading_comprehension", "What does the dance note say works with gesture to create meaning?", "rhythm and character"),
        ("inference", "Why should a critic describe an action before interpreting it?", "to keep observation distinct from interpretation"),
        ("main_idea", "What is the dance passage mainly about?", "gesture and expression gain meaning in performance context"),
        ("detail_identification", "Which expressive feature besides hand gestures is mentioned?", "facial expression"),
    ],
}

HALFSTEPS["C1+"] = {
    "native": NATIVE,
    "title": "Tamil C1+ — Academic argument, public policy and editing",
    "goals": [
        "Frame a research question and distinguish evidence from interpretation",
        "Compare policy options while naming who benefits and what remains uncertain",
        "Edit a translation for register, terminology, and a clearly stated audience",
    ],
    "units": [
        {"id": "C1+-U1", "title": "கல்வியியல் தமிழ்", "lessons": [
            _spec_lesson(
                "ஆய்வுக் கேள்வியை வரையறுத்தல்",
                "Turn a broad topic into a researchable question. ஆய்வுக் கேள்வி names "
                "the question; வரையறை is a definition or boundary, and எந்தச் சூழலில் "
                "limits a claim to its context.",
                [("ஆய்வுக் கேள்வி", "āyvuk kēḷvi", "research question", "phrase"), ("வரையறை", "varaiyaṟai", "definition, scope", "noun"), ("சூழல்", "cūḻal", "context", "noun"), ("கருதுகோள்", "karutukōḷ", "hypothesis", "noun"), ("விளக்கம்", "viḷakkam", "interpretation", "noun")],
                "Question and scope", "... எந்தச் சூழலில்? · இதை ... என வரையறுக்கிறோம் · கேள்வி ... அல்ல",
                "A workable question names a population, time, or context. Define the "
                "term before arguing about it. Use அல்ல to distinguish the research "
                "question from a wider topic that the study does not answer.",
                [("இந்த ஆய்வு, நகர்ப்புறப் பள்ளிகளில் வீட்டுப்பாடப் பயன்பாட்டை ஆராய்கிறது.", "inta āyvu, nakarppuṟap paḷḷikaḷil vīṭṭuppāṭap payaṉpāṭṭai ārāykiṟatu.", "This study examines homework use in urban schools."), ("இங்கு 'பயன்பாடு' என்பது மாணவர் பணியைத் தொடங்கும் நேரத்தைக் குறிக்கிறது.", "iṅku payaṉpāṭu eṉpatu māṇavar paṇiyait toṭaṅkum nērattaik kuṟikkiṟatu.", "Here, 'use' refers to the time when students begin the task."), ("ஆய்வின் கேள்வி வீட்டுப்பாடத்தின் தரத்தைப் பற்றியது அல்ல; மாணவர்கள் எப்போது தொடங்குகிறார்கள் என்பதுடனான தொடர்பைப் பற்றியது.", "āyviṉ kēḷvi vīṭṭuppāṭattiṉ tarattaip paṟṟiyatu alla; māṇavarkaḷ eppōtu toṭaṅkukiṟārkaḷ eṉpatuṭaṉāṉa toṭarpaip paṟṟiyatu.", "The research question is not homework quality; it is the relation to when students begin.")],
                [("இந்த ஆய்வு எல்லாப் பள்ளிகளையும் ஆராய்கிறது. (urban sample)", "இந்த ஆய்வு நகர்ப்புறப் பள்ளிகளில் வீட்டுப்பாடப் பயன்பாட்டை ஆராய்கிறது.", "State the study's actual scope, not all schools."), ("பயன்பாடு என்ற சொல்லை விளக்குகிறது. (we define)", "இங்கு 'பயன்பாடு' என்பது பணியைத் தொடங்கும் நேரத்தைக் குறிக்கிறது.", "Define the term's meaning within the study.")],
                [("ஆய்வாளர்", "உங்கள் ஆய்வுக் கேள்வி என்ன?", "uṅkaḷ āyvuk kēḷvi eṉṉa?", "What is your research question?"), ("மாணவர்", "வீட்டுப்பாடத்தை மாணவர்கள் எப்போது தொடங்குகிறார்கள் என்பதே.", "vīṭṭuppāṭattai māṇavarkaḷ eppōtu toṭaṅkukiṟārkaḷ eṉpatē.", "It is when students begin their homework."), ("ஆய்வாளர்", "எந்த மாணவர்கள், எந்தச் சூழலில்?", "enta māṇavarkaḷ, entac cūḻalil?", "Which students, and in what context?"), ("மாணவர்", "நகர்ப்புறப் பள்ளிகளின் ஏழாம் வகுப்பு மாணவர்களிடம் ஆய்வு செய்கிறோம்; முடிவை எல்லா வயதினருக்கும் நீட்டிக்கமாட்டோம்.", "nakarppuṟap paḷḷikaḷiṉ ēḻām vakuppu māṇavarkaḷiṭam āyvu ceykiṟōm; muṭivai ellā vayatiṉarukkum nīṭṭikkamāṭṭōm.", "We are studying grade-seven students in urban schools; we will not extend the result to all ages.")],
                "Research framing worksheet", [("Narrow the question.", ["this study examines homework use in urban schools", "we will not extend the result to all ages"], ["இந்த ஆய்வு நகர்ப்புறப் பள்ளிகளில் வீட்டுப்பாடப் பயன்பாட்டை ஆராய்கிறது", "முடிவை எல்லா வயதினருக்கும் நீட்டிக்கமாட்டோம்"]), ("Define the term.", ["use refers to when a student begins the task", "the question is not homework quality"], ["பயன்பாடு என்பது மாணவர் பணியைத் தொடங்கும் நேரத்தைக் குறிக்கிறது", "கேள்வி வீட்டுப்பாடத்தின் தரம் அல்ல"])]),
            _spec_lesson(
                "ஆதாரங்களை ஒருங்கிணைத்தல்",
                "Summarise two studies without making their findings sound identical. "
                "முந்தைய ஆய்வு attributes earlier work; இதற்கு மாறாக signals a contrast, "
                "and இரண்டிலும் identifies common ground.",
                [("முந்தைய ஆய்வு", "muntaiya āyvu", "previous study", "phrase"), ("ஒருங்கிணைத்தல்", "oruṅkiṇa itt al", "to synthesise", "verb"), ("மாறாக", "māṟāka", "in contrast", "connector"), ("ஒற்றுமை", "oṟṟumai", "similarity", "noun"), ("வேறுபாடு", "vēṟupāṭu", "difference", "noun")],
                "Synthesis and contrast", "ஒரு ஆய்வு ... · இதற்கு மாறாக ... · இரண்டிலும் ...",
                "Attribute each finding to its study before comparing. இதற்கு மாறாக marks "
                "a genuine contrast, while இரண்டிலும் identifies a shared result. Do not "
                "erase different methods just because the conclusions overlap.",
                [("முந்தைய ஆய்வு வருகை எண்ணிக்கையை அளந்தது.", "muntaiya āyvu varukai eṇṇikkaiyai aḷantatu.", "The previous study measured attendance."), ("இதற்கு மாறாக, இரண்டாவது ஆய்வு மாணவர்களின் அனுபவத்தை நேர்காணலில் பதிவு செய்தது.", "itaṟku māṟāka, iraṇṭāvatu āyvu māṇavarkaḷiṉ aṉupavattai nērkāṇalil pativu ceytatu.", "In contrast, the second study recorded students' experiences in interviews."), ("இரண்டிலும் பள்ளி நேரம் பங்கேற்பை பாதிக்கிறது என்று தெரிந்தது.", "iraṇṭilum paḷḷi nēram paṅkēṟpai pāti kkiṟatu eṉṟu terintatu.", "Both found that school timing affects participation.")],
                [("இரண்டு ஆய்வுகளும் ஒரே முறையைப் பயன்படுத்தின. (one survey, one interview)", "இரண்டு ஆய்வுகளும் வெவ்வேறு முறைகளைப் பயன்படுத்தின.", "Do not claim methodological identity when their methods differ."), ("இரண்டிலும் முடிவு வேறுபட்டது. (shared finding)", "இரண்டிலும் பள்ளி நேரம் பங்கேற்பை பாதிக்கிறது என்று தெரிந்தது.", "State the common finding accurately.")],
                [("மாணவர்", "முந்தைய ஆய்வு என்ன அளந்தது?", "muntaiya āyvu eṉṉa aḷantatu?", "What did the previous study measure?"), ("ஆய்வாளர்", "வருகை எண்ணிக்கையை; மற்ற ஆய்வு நேர்காணலைப் பயன்படுத்தியது.", "varukai eṇṇikkaiyai; maṟṟa āyvu nērkāṇalaip payaṉpaṭuttiyatu.", "Attendance numbers; the other study used interviews."), ("மாணவர்", "அவற்றில் என்ன ஒற்றுமை?", "avaṟṟil eṉṉa oṟṟumai?", "What is similar between them?"), ("ஆய்வாளர்", "இரண்டிலும் பள்ளி நேரம் பங்கேற்பை பாதிக்கிறது.", "iraṇṭilum paḷḷi nēram paṅkēṟpai pātikkiṟatu.", "Both find that school timing affects participation.")],
                "Synthesis worksheet", [("Attribute the studies.", ["the previous study measured attendance", "the second study used interviews"], ["முந்தைய ஆய்வு வருகை எண்ணிக்கையை அளந்தது", "இரண்டாவது ஆய்வு நேர்காணலைப் பயன்படுத்தியது"]), ("State the common ground.", ["both found that school timing affects participation", "their methods differ"], ["இரண்டிலும் பள்ளி நேரம் பங்கேற்பை பாதிக்கிறது", "அவற்றின் முறைகள் வேறுபட்டவை"])]),
            _spec_lesson(
                "ஆய்வுச் சுருக்கம் எழுதுதல்",
                "Write a compact abstract that states the question, method, finding, and "
                "limitation in that order. ஆய்வின் நோக்கம் frames the purpose; முறையில் "
                "names the method, and இருப்பினும் prevents a finding from sounding "
                "more conclusive than it is.",
                [("சுருக்கம்", "curukkam", "abstract, summary", "noun"), ("நோக்கம்", "nōkkam", "purpose", "noun"), ("முறை", "muṟai", "method", "noun"), ("கண்டறிதல்", "kaṇṭaṟital", "finding", "noun"), ("வரம்பு", "varampu", "limitation", "noun")],
                "Abstract structure", "நோக்கம் ... · முறையில் ... · முடிவு ... · இருப்பினும் ...",
                "Order the abstract from purpose to method to finding to limitation. Use "
                "இருப்பினும் for the limitation, and include only what the method supports. "
                "A compact summary should be short because it is structured, not because "
                "it leaves out essential scope.",
                [("இந்த ஆய்வின் நோக்கம் மாணவர் பங்கேற்பைப் புரிந்துகொள்வது.", "inta āyviṉ nōkkam māṇavar paṅkēṟpaip purintukoḷvatu.", "The purpose of this study is to understand student participation."), ("இரண்டு பள்ளிகளில் நேர்காணல் முறையில் தரவு சேகரிக்கப்பட்டது.", "iraṇṭu paḷḷikaḷil nērkāṇal muṟaiyil taravu cēkarikkappaṭṭatu.", "Data were collected through interviews at two schools."), ("இருப்பினும், இந்த முடிவை வேறு மாவட்டங்களுக்கு நேரடியாகப் பொதுமைப்படுத்த முடியாது.", "iruppiṉum, inta muṭivai vēṟu māvaṭṭaṅkaḷukku nēraṭiyākap potumaippaṭutta muṭiyātu.", "Nevertheless, this result cannot be directly generalised to other districts.")],
                [("நோக்கம், முறை, முடிவு, வரம்பு எல்லாம் விடப்பட்டன.", "சுருக்கத்தில் நோக்கம், முறை, முடிவு, வரம்பு ஆகியவை இடம்பெற வேண்டும்.", "A complete abstract includes all four elements."), ("இரண்டு பள்ளிகளின் முடிவு எல்லா மாவட்டங்களையும் நிரூபிக்கிறது.", "இரண்டு பள்ளிகளின் முடிவு அந்த ஆய்வுச் சூழலுக்குள் மட்டுமே பொருந்தும்.", "Keep the claim within the sample's scope.")],
                [("வழிகாட்டி", "சுருக்கத்தில் முதலில் என்ன வர வேண்டும்?", "curukk attil mutalil eṉṉa vara vēṇṭum?", "What should come first in the abstract?"), ("ஆய்வாளர்", "ஆய்வின் நோக்கம்; அதன் பிறகு முறை மற்றும் முடிவு.", "āyviṉ nōkkam; ataṉ piṟaku muṟai maṟṟum muṭivu.", "The study's purpose; then its method and finding."), ("வழிகாட்டி", "வரம்பை எங்கே குறிப்பிடுவீர்கள்?", "varampai eṅkē kuṟippiṭuvīrkaḷ?", "Where will you state the limitation?"), ("ஆய்வாளர்", "முடிவுக்குப் பிறகு இருப்பினும் என்று தொடங்கி எழுதுவேன்.", "muṭivukkup piṟaku iruppiṉum eṉṟu toṭaṅki eḻutuvēṉ.", "After the finding, I will begin with 'nevertheless'.")],
                "Abstract worksheet", [("Order the abstract.", ["the purpose is to understand student participation", "data were collected through interviews at two schools"], ["ஆய்வின் நோக்கம் மாணவர் பங்கேற்பைப் புரிந்துகொள்வது", "இரண்டு பள்ளிகளில் நேர்காணல் முறையில் தரவு சேகரிக்கப்பட்டது"]), ("State result and limit.", ["include the finding", "do not generalise directly to other districts"], ["கண்டறிதலைச் சேர்க்கவும்", "வேறு மாவட்டங்களுக்கு நேரடியாகப் பொதுமைப்படுத்த முடியாது"])]),
        ]},
        {"id": "C1+-U2", "title": "பொதுக் கொள்கை", "lessons": [
            _spec_lesson(
                "பொது விசாரணையில் கருத்து கேட்பது",
                "Summarise residents' views at a public hearing without reducing disagreement "
                "to a simple for-or-against vote. பங்கேற்பாளர் கூறியதாவது attributes a "
                "view; பலரின் கருத்தில் marks a shared concern, and அதேவேளை preserves "
                "a counterpoint.",
                [("பொது விசாரணை", "potu vicāraṇai", "public hearing", "phrase"), ("பங்கேற்பாளர்", "paṅkēṟpāḷar", "participant", "noun"), ("கவலை", "kavalai", "concern", "noun"), ("எதிர்ப்பு", "etirppu", "objection", "noun"), ("கருத்துச் சுருக்கம்", "karuttuc curukkam", "summary of views", "phrase")],
                "Reporting a public hearing", "பங்கேற்பாளர் கூறியதாவது ... · பலரின் கருத்தில் ... · அதேவேளை ...",
                "Attribute each view rather than turning it into a general public opinion. "
                "Use பலரின் கருத்தில் for a recurring concern and அதேவேளை for a distinct "
                "counterpoint. A hearing summary reports views; it does not by itself "
                "settle the policy choice.",
                [("ஒரு பங்கேற்பாளர் கூறியதாவது, புதிய வழித்தடம் பயண நேரத்தைக் குறைக்கும்.", "oru paṅkēṟpāḷar kūṟiyatāvatu, putiya vaḻittaṭam payaṇa nērattaik kuṟaikkum.", "One participant said the new route would reduce travel time."), ("பலரின் கருத்தில், இரவு சேவையின் பாதுகாப்பு முக்கியமான கவலை.", "palar iṉ karuttil, iravu cēvaiyiṉ pāṭukāppu mukkiyamāṉa kavalai.", "For many, the safety of evening service is an important concern."), ("அதேவேளை, வணிகர்கள் நிறுத்தம் மாறினால் வாடிக்கையாளர் வருகை குறையும் என்றனர்.", "atēvēḷai, vaṇikarkaḷ niṟuttam māṟiṉāl vāṭikkaiyāḷar varukai kuṟaiyum eṉṟaṉar.", "At the same time, shopkeepers said changing the stop would reduce customer visits.")],
                [("எல்லோரும் புதிய வழித்தடத்தை ஆதரித்தனர்.", "சிலர் புதிய வழித்தடத்தை ஆதரித்தனர்; சிலர் அணுகல் குறித்து கவலை தெரிவித்தனர்.", "Do not turn a mixed hearing into unanimous support."), ("கேட்பில் கருத்து தெரிவிக்கப்பட்டது.", "பொது விசாரணையில் பங்கேற்பாளர்கள் கருத்துத் தெரிவித்தனர்.", "Name the hearing and the people who offered their views.")],
                [("தலைவர்", "இன்றைய கருத்துச் சுருக்கம் என்ன?", "iṉṟaiya karuttuc curukkam eṉṉa?", "What is today's summary of views?"), ("ஆய்வாளர்", "பலர் இரவு சேவையின் பாதுகாப்பு குறித்து கவலை தெரிவித்தனர்.", "palar iravu cēvaiyiṉ pāṭukāppu kuṟittu kavalai terivitt aṉar.", "Many expressed concern about the safety of evening service."), ("தலைவர்", "வழித்தட மாற்றம் குறித்த கருத்து?", "vaḻittaṭa māṟṟam kuṟitta karuttu?", "What about the route change?"), ("ஆய்வாளர்", "வணிகர்கள் வருகை குறையலாம் என்றனர்; இது தனி மதிப்பீடு தேவைப்படுத்துகிறது.", "vaṇikarkaḷ varukai kuṟaiyalām eṉṟaṉar; itu taṉi matippīṭu tēvaippaṭuttukiṟatu.", "Shopkeepers said visits may fall; this requires a separate assessment.")],
                "Public hearing worksheet", [("Attribute the views.", ["many raised safety concerns", "shopkeepers said visits may fall"], ["பலர் பாதுகாப்பு குறித்து கவலை தெரிவித்தனர்", "வாடிக்கையாளர் வருகை குறையலாம் என்று வணிகர்கள் கூறினர்"]), ("Keep the summary balanced.", ["one participant supported the new route", "a separate assessment is needed"], ["ஒரு பங்கேற்பாளர் புதிய வழித்தடத்தை ஆதரித்தார்", "தனி மதிப்பீடு தேவைப்படுகிறது"])]),
            _spec_lesson(
                "கொள்கைத் தேர்வுகளை ஒப்பிடுதல்",
                "Compare two policy options by cost, access, and implementation time. "
                "முதலாவது ... இரண்டாவது ... structures the options; செலவு மட்டுமல்ல "
                "adds a second criterion, and நடைமுறைப்படுத்தும் காலம் marks the "
                "implementation period.",
                [("கொள்கைத் தேர்வு", "koḷkait tērvu", "policy option", "phrase"), ("அணுகல்", "aṇukal", "access", "noun"), ("செயலாக்கம்", "ceyalākkam", "implementation", "noun"), ("செலவுத்திட்டம்", "celavuttiṭṭam", "budget", "noun"), ("நடைமுறை", "naṭaimuṟai", "practical implementation", "noun")],
                "Comparing policy options", "முதலாவது ... · இரண்டாவது ... · செலவு மட்டுமல்ல, அணுகலும் ...",
                "Describe both options using the same criteria. செலவு மட்டுமல்ல, அணுகலும் "
                "signals that cost is not the only measure. State who gains access and "
                "how long implementation takes before recommending an option.",
                [("முதலாவது தேர்வு செலவைக் குறைக்கும், ஆனால் செயலாக்கம் நீளும்.", "mutalāvatu tērvu celavaik kuṟaikkum, āṉāl ceyalākkam nīḷum.", "The first option reduces cost, but implementation will take longer."), ("இரண்டாவது தேர்வு அணுகலை விரைவாக மேம்படுத்தும்.", "iraṇṭāvatu tērvu aṇukalai viraivāka mēmpaṭuttum.", "The second option will improve access quickly."), ("செலவு மட்டுமல்ல, பயனாளர்களின் பகிர்வும் மதிப்பிடப்பட வேண்டும்.", "celavu maṭṭumalla, payaṉāḷarkaḷiṉ pakirvum matippiṭappaṭa vēṇṭum.", "Not only cost but also the distribution of beneficiaries should be assessed.")],
                [("முதலாவது தேர்வு மலிவு, ஆகவே அதுவே சிறந்தது.", "முதலாவது தேர்வு செலவைக் குறைக்கும்; அணுகல் மற்றும் செயலாக்க நேரத்தையும் ஒப்பிட வேண்டும்.", "Cost alone does not establish which option is best."), ("இரண்டாவது தேர்வு விரைவாகும்.", "இரண்டாவது தேர்வு அணுகலை விரைவாக மேம்படுத்தும்.", "Name what improves quickly; the option itself is not 'fast'.")],
                [("அதிகாரி", "எந்தத் தேர்வு செலவைக் குறைக்கும்?", "entat tērvu celavaik kuṟaikkum?", "Which option reduces cost?"), ("ஆய்வாளர்", "முதலாவது; ஆனால் செயலாக்கம் அதிக நேரம் எடுக்கும்.", "mutalāvatu; āṉāl ceyalākkam atika nēram eṭukkum.", "The first; but implementation takes longer."), ("அதிகாரி", "இரண்டாவது தேர்வின் பலன் என்ன?", "iraṇṭāvatu tēṟviṉ palaṉ eṉṉa?", "What is the benefit of the second option?"), ("ஆய்வாளர்", "அணுகலை விரைவாக மேம்படுத்தும்; பயனாளர்களின் பகிர்வையும் மதிப்பிட வேண்டும்.", "aṇukalai viraivāka mēmpaṭuttum; payaṉāḷarkaḷiṉ pakirvaiyum matippiṭa vēṇṭum.", "It improves access quickly; we should also assess how benefits are distributed.")],
                "Policy options worksheet", [("Compare the options.", ["the first option reduces cost but takes longer", "the second improves access quickly"], ["முதலாவது தேர்வு செலவைக் குறைக்கும், ஆனால் அதிக நேரம் எடுக்கும்", "இரண்டாவது தேர்வு அணுகலை விரைவாக மேம்படுத்தும்"]), ("Add the equity check.", ["cost is not the only criterion", "assess how benefits are distributed"], ["செலவு மட்டுமே ஒரே அளவுகோல் அல்ல", "பயனாளர்களின் பகிர்வை மதிப்பிட வேண்டும்"])]),
            _spec_lesson(
                "தீர்மானத்தையும் நிபந்தனையையும் அறிவித்தல்",
                "Announce a decision, its condition, and when it will be reviewed. "
                "தீர்மானிக்கப்பட்டது reports an impersonal decision; நடைமுறைக்கு வரும் "
                "தேதி names the effective date, and ... வரை conditions the decision.",
                [("தீர்மானம்", "tīrmāṉam", "decision", "noun"), ("நிபந்தனை", "nipant aṉai", "condition", "noun"), ("நடைமுறை", "naṭaimuṟai", "implementation", "noun"), ("மதிப்பாய்வு", "matippāyvu", "review", "noun"), ("தேதி", "tēti", "date", "noun")],
                "Decision with a review condition", "... தீர்மானிக்கப்பட்டது · ... வரை · ... அன்று மீண்டும் மதிப்பாய்வு செய்யப்படும்",
                "State the decision in passive form, then its start date and condition. "
                "முடிவுகள் மதிப்பாய்வு செய்யப்படும் வரை keeps the measure provisional; "
                "the review date should be explicit so a temporary policy does not look "
                "permanent.",
                [("புதிய சேவை ஜூன் முதல் நடைமுறைக்கு வரும் என்று தீர்மானிக்கப்பட்டது.", "putiya cēvai jūṉ mutal naṭaimuṟaikku varum eṉṟu tīrmāṉikkappaṭṭatu.", "It was decided that the new service will take effect from June."), ("முதல் ஆறு மாத முடிவுகள் மதிப்பாய்வு செய்யப்படும்.", "mutal āṟu māta muṭivukaḷ matippāyvu ceyyappaṭum.", "The first six months' results will be reviewed."), ("மதிப்பாய்வு முடியும் வரை அட்டவணை தற்காலிகமாக இருக்கும்.", "matippāyvu muṭiyum varai aṭṭavaṇai taṟkālikamāka irukkum.", "The schedule will remain provisional until the review is complete.")],
                [("ஜூன் முதல் புதிய சேவை வரும் என்று தீர்மானித்தது.", "புதிய சேவை ஜூன் முதல் நடைமுறைக்கு வரும் என்று தீர்மானிக்கப்பட்டது.", "Use the passive to report an institutional decision."), ("அட்டவணை தற்காலிகம் இருக்கும் முடியும் வரை.", "மதிப்பாய்வு முடியும் வரை அட்டவணை தற்காலிகமாக இருக்கும்.", "Place the until-clause before the main clause and use the adverbial form.")],
                [("தலைவர்", "புதிய சேவை எப்போது தொடங்கும்?", "putiya cēvai eppōtu toṭaṅkum?", "When will the new service begin?"), ("அலுவலர்", "ஜூன் முதல் நடைமுறைக்கு வரும் என்று தீர்மானிக்கப்பட்டது.", "jūṉ mutal naṭaimuṟaikku varum eṉṟu tīrmāṉikkappaṭṭatu.", "It was decided that it will take effect from June."), ("தலைவர்", "அட்டவணை நிரந்தரமானதா?", "aṭṭavaṇai nirantaramāṉatā?", "Is the schedule permanent?"), ("அலுவலர்", "இல்லை. ஆறு மாத முடிவுகள் மதிப்பாய்வு செய்யப்படும் வரை தற்காலிகம்.", "illai. āṟu māta muṭivukaḷ matippāyvu ceyyappaṭum varai taṟkālikam.", "No. It is provisional until the six-month results are reviewed.")],
                "Decision worksheet", [("Announce the decision.", ["the service will take effect from June", "the first six months' results will be reviewed"], ["சேவை ஜூன் முதல் நடைமுறைக்கு வரும்", "முதல் ஆறு மாத முடிவுகள் மதிப்பாய்வு செய்யப்படும்"]), ("State the condition.", ["the schedule is provisional until review", "when will the service begin?"], ["மதிப்பாய்வு முடியும் வரை அட்டவணை தற்காலிகமாக இருக்கும்", "சேவை எப்போது தொடங்கும்?"])]),
        ]},
        {"id": "C1+-U3", "title": "மொழிபெயர்ப்பும் தொகுப்பும்", "lessons": [
            _spec_lesson(
                "சொற்களஞ்சியத்தை ஒருமைப்படுத்துதல்",
                "Edit a long document so a technical term is used consistently without "
                "flattening its meaning. சொற்களஞ்சியம் is a glossary; ஒருமைப்படுத்துதல் "
                "is standardising, and முதன்முதலில் வரும் இடத்தில் signals the first "
                "occurrence.",
                [("சொற்களஞ்சியம்", "coṟkaḷañciyam", "glossary", "noun"), ("ஒருமைப்படுத்துதல்", "orum aippaṭuttutal", "to standardise", "verb"), ("தொழில்நுட்பச் சொல்", "toḻilnuṭpac col", "technical term", "phrase"), ("முதன்முதலில்", "mutaṉmutalil", "at first occurrence", "adverb"), ("மாறுபாடு", "māṟupāṭu", "variation", "noun")],
                "Term consistency", "முதன்முதலில் ... என்று வரையறுக்கவும் · பின்னர் ... பயன்படுத்தவும்",
                "Define a technical term at first use, then keep one form through the "
                "document. If a context-specific meaning is needed, explain the variation "
                "rather than silently replacing the term. A glossary should document the "
                "choice and its scope.",
                [("முதன்முதலில் வரும் இடத்தில் சொல்லை வரையறுக்கிறோம்.", "mutaṉmutalil varum iṭattil collai varaiyaṟukkiṟōm.", "We define the term at its first occurrence."), ("பின்னர் அதே தொழில்நுட்பச் சொல்லைப் பயன்படுத்துகிறோம்.", "piṉṉar atē toḻilnuṭpac coll aip payaṉpaṭuttukiṟōm.", "After that we use the same technical term."), ("சூழலைப் பொறுத்து பொருள் மாறினால், சொற்களஞ்சியத்தில் வேறுபாட்டைக் குறிப்பிடுகிறோம்.", "cūḻalaip poṟuttu poruḷ māṟiṉāl, coṟkaḷañciyattil vēṟupāṭṭaik kuṟippiṭukiṟōm.", "If meaning varies by context, we note the distinction in the glossary.")],
                [("ஒவ்வொரு பக்கத்திலும் வேறு சொல்லைப் பயன்படுத்தவும்.", "முதன்முதலில் சொல்லை வரையறுத்து, பின்னர் ஒரே வடிவத்தைப் பயன்படுத்தவும்.", "Consistency helps the reader follow a technical term."), ("சூழல் மாறினால் வேறுபாடு குறிப்பிட வேண்டாம்.", "சூழலைப் பொறுத்து பொருள் மாறினால் வேறுபாட்டைக் குறிப்பிடுங்கள்.", "Document a context-dependent meaning rather than hiding it.")],
                [("தொகுப்பாளர்", "இந்தச் சொல்லுக்கு இரண்டு மொழிபெயர்ப்புகள் உள்ளன.", "intac collukku iraṇṭu moḻipeyarppukaḷ uḷḷaṉa.", "There are two translations for this term."), ("மொழிபெயர்ப்பாளர்", "முதன்முதலில் ஒன்றை வரையறுத்து, மற்றொன்றின் பயன்பாட்டை விளக்கலாம்.", "mutaṉmutalil oṉṟai varaiyaṟuttu, maṟṟoṉṟiṉ payaṉpāṭṭai viḷakkalām.", "We can define one at first use and explain when the other is used."), ("தொகுப்பாளர்", "சொற்களஞ்சியத்தில் அந்த வேறுபாட்டைச் சேர்க்கிறேன்.", "coṟkaḷañciyattil anta vēṟupāṭṭaic cērkkiṟēṉ.", "I will add that distinction to the glossary."), ("மொழிபெயர்ப்பாளர்", "அப்படியானால், உரை முழுவதும் தேர்ந்தெடுத்த வடிவத்தைப் பயன்படுத்துகிறேன்.", "appaṭiyāṉāl, urai muḻuvatum tēṟnteṭutta vaṭivattaip payaṉpaṭuttukiṟēṉ.", "Then I will use the chosen form throughout the text.")],
                "Glossary worksheet", [("Define the term.", ["define the term at first use", "use the same technical term afterward"], ["முதன்முதலில் சொல்லை வரையறுக்கவும்", "பின்னர் அதே தொழில்நுட்பச் சொல்லைப் பயன்படுத்தவும்"]), ("Record the nuance.", ["note the difference in the glossary", "explain context-dependent meaning"], ["சொற்களஞ்சியத்தில் வேறுபாட்டைக் குறிப்பிடவும்", "சூழலைப் பொறுத்து பொருளை விளக்கவும்"])]),
            _spec_lesson(
                "இருபொருள் கொண்ட சொற்றொடரை மொழிபெயர்த்தல்",
                "Translate an ambiguous phrase only after reading the surrounding scene. "
                "இருபொருள் கொண்ட identifies ambiguity; முன்னும் பின்னும் is the "
                "context around it, and தேர்வை நியாயப்படுத்துதல் means explaining the "
                "translation choice.",
                [("இருபொருள்", "iruporuḷ", "ambiguity, two meanings", "noun"), ("சொற்றொடர்", "coṟṟoṭar", "phrase", "noun"), ("முன்னும் பின்னும்", "muṉṉum piṉṉum", "surrounding context", "phrase"), ("நியாயப்படுத்துதல்", "niyāyappaṭuttutal", "to justify", "verb"), ("தேர்வு", "tērvu", "choice", "noun")],
                "Context and ambiguity", "சூழலைப் பொறுத்து ... · முன்னும் பின்னும் வாசித்த பின் · தேர்வை விளக்குகிறேன்",
                "Do not choose a dictionary equivalent before checking the speaker and "
                "scene. Read the sentence before and after; then record which sense is "
                "supported. The translator can explain a choice without pretending the "
                "other possible meaning never existed.",
                [("இந்தச் சொற்றொடர் சூழலைப் பொறுத்து இரண்டு பொருள் தருகிறது.", "intac coṟṟoṭar cūḻalaip poṟuttu iraṇṭu poruḷ tarukiṟatu.", "This phrase has two meanings depending on context."), ("முன்னும் பின்னும் வாசித்த பின், இங்கே நகைச்சுவைத் தொனி தெளிவாகிறது.", "muṉṉum piṉṉum vācitta piṉ, iṅkē nakaiccuvait toṉi teḷivākiṟatu.", "After reading the surrounding lines, the humorous tone becomes clear here."), ("அந்தத் தேர்வை மொழிபெயர்ப்புக் குறிப்பில் விளக்குகிறேன்.", "antat tērvai moḻipeyarppuk kuṟippil viḷakkukiṟēṉ.", "I explain that choice in the translator's note.")],
                [("அகராதியில் முதல் பொருள் இருக்கிறது, அதையே தேர்ந்தெடுக்க வேண்டும்.", "சூழல் ஆதரிக்கும் பொருளைத் தேர்ந்தெடுத்து காரணத்தை விளக்க வேண்டும்.", "A dictionary's first sense does not determine a context-specific translation."), ("முன்னும் பின்னும் பார்க்காமல் தொனி தெளிவாகிறது.", "முன்னும் பின்னும் வாசித்த பின் தொனி தெளிவாகிறது.", "The interpretation follows the contextual reading.")],
                [("தொகுப்பாளர்", "இங்கே இந்தச் சொற்றொடர் எந்தப் பொருளில் வருகிறது?", "iṅkē intac coṟṟoṭar entap poruḷil varukiṟatu?", "Which sense of the phrase is used here?"), ("மொழிபெயர்ப்பாளர்", "முன்னும் பின்னும் வாசித்தால் நகைச்சுவைத் தொனி தெரிகிறது.", "muṉṉum piṉṉum vācittāl nakaiccuvait toṉi terikiṟatu.", "Reading the context shows a humorous tone."), ("தொகுப்பாளர்", "மற்ற பொருளை முற்றிலும் நீக்கலாமா?", "maṟṟa poruḷai muṟṟilum nīkkalāmā?", "Can we remove the other meaning entirely?"), ("மொழிபெயர்ப்பாளர்", "இல்லை; குறிப்பில் சாத்தியமான இரண்டாவது வாசிப்பையும் சொல்கிறேன்.", "illai; kuṟippil cāttiyamāṉa iraṇṭāvatu vācippaiyum colkiṟēṉ.", "No; I will also mention the possible second reading in a note.")],
                "Ambiguity worksheet", [("Read for context.", ["this phrase has two meanings depending on context", "the surrounding lines show a humorous tone"], ["இந்தச் சொற்றொடர் சூழலைப் பொறுத்து இரண்டு பொருள் தருகிறது", "முன்னும் பின்னும் வாசித்தால் நகைச்சுவைத் தொனி தெரிகிறது"]), ("Justify the choice.", ["explain the choice in a translator's note", "mention the possible second reading"], ["மொழிபெயர்ப்புக் குறிப்பில் தேர்வை விளக்குங்கள்", "சாத்தியமான இரண்டாவது வாசிப்பையும் குறிப்பிடுங்கள்"])]),
            _spec_lesson(
                "இறுதித் திருத்தக் குறிப்பை எழுதுதல்",
                "Prepare a final editorial note that states what changed and what remains "
                "unresolved. இறுதிப் பதிப்பு is the final version; மாற்றங்கள் is changes, "
                "and நிலுவையில் உள்ளது names an open question without hiding it.",
                [("இறுதிப் பதிப்பு", "iṟutipp atippu", "final version", "phrase"), ("திருத்தக் குறிப்பு", "tiruttak kuṟippu", "editorial note", "phrase"), ("மாற்றம்", "māṟṟam", "change", "noun"), ("நிலுவை", "niluvai", "pending matter", "noun"), ("வெளிப்படைத் தன்மை", "veḷippaṭait taṉmai", "transparency", "noun")],
                "A transparent editorial note", "... மாற்றங்கள் செய்யப்பட்டன · ... நிலுவையில் உள்ளது · வாசகர் கவனிக்க வேண்டும்",
                "Name substantive changes and distinguish them from unresolved choices. "
                "நிலுவையில் உள்ளது is more honest than silently smoothing an uncertainty. "
                "A final note should let readers see what the editor decided and what "
                "remains open.",
                [("சொற்களஞ்சியம் ஒருமைப்படுத்தப்பட்டது; இரண்டு தேதிகள் சரிபார்க்கப்பட்டன.", "coṟkaḷañciyam orumaippaṭuttappaṭṭatu; iraṇṭu tētikaḷ caripārkkappaṭṭaṉa.", "The glossary was standardised; two dates were verified."), ("ஒரு மேற்கோளின் மூலப் பதிப்பு இன்னும் நிலுவையில் உள்ளது.", "oru mēṟkōḷiṉ mūlap patippu iṉṉum niluvaiyil uḷḷatu.", "The source edition of one quotation is still pending."), ("அந்த வரம்பை வாசகர் கவனிக்குமாறு திருத்தக் குறிப்பு தெரிவிக்கிறது.", "anta varampai vācakar kavaṉikkumāṟu tiruttak kuṟippu terivikkiṟatu.", "The editorial note asks readers to notice that limitation.")],
                [("எல்லா மேற்கோள்களும் சரிபார்க்கப்பட்டன. (one is pending)", "ஒரு மேற்கோளின் மூலப் பதிப்பு இன்னும் நிலுவையில் உள்ளது.", "Do not say all sources were checked when one remains pending."), ("சொற்களஞ்சியம் ஒன்றாக்கப்பட்டது.", "சொற்களஞ்சியம் ஒருமைப்படுத்தப்பட்டது.", "Use the editorial term ஒருமைப்படுத்தப்பட்டது for standardising terminology.")],
                [("தொகுப்பாளர்", "இறுதிப் பதிப்பில் என்ன மாற்றங்கள் செய்யப்பட்டன?", "iṟutipp atippil eṉṉa māṟṟaṅkaḷ ceyyappaṭṭaṉa?", "What changes were made in the final version?"), ("ஆசிரியர்", "சொற்களஞ்சியம் ஒருமைப்படுத்தப்பட்டது; இரண்டு தேதிகள் சரிபார்க்கப்பட்டன.", "coṟkaḷañciyam orumaippaṭuttappaṭṭatu; iraṇṭu tētikaḷ caripārkkappaṭṭaṉa.", "The glossary was standardised; two dates were verified."), ("தொகுப்பாளர்", "நிலுவையில் உள்ள மேற்கோளை எப்படிக் குறிப்பிடுவோம்?", "niluvaiyil uḷḷa mēṟkōḷai eppaṭik kuṟippiṭuvōm?", "How will we note the pending quotation?"), ("ஆசிரியர்", "திருத்தக் குறிப்பில் அதன் மூலப் பதிப்பு இன்னும் நிலுவையில் உள்ளது என்று எழுதுவோம்.", "tiruttak kuṟippil ataṉ mūlap patippu iṉṉum niluvaiyil uḷḷatu eṉṟu eḻutuvōm.", "We will write in the note that its source edition is still pending.")],
                "Editorial note worksheet", [("State the completed edits.", ["the glossary was standardised", "two dates were verified"], ["சொற்களஞ்சியம் ஒருமைப்படுத்தப்பட்டது", "இரண்டு தேதிகள் சரிபார்க்கப்பட்டன"]), ("Be transparent about what remains.", ["one source edition is still pending", "the note asks readers to notice the limitation"], ["ஒரு மூலப் பதிப்பு இன்னும் நிலுவையில் உள்ளது", "வரம்பை வாசகர் கவனிக்குமாறு குறிப்பு தெரிவிக்கிறது"])]),
        ]},
    ],
    "extra": EXTRA(
        culture=("Subrahmanya Bharati is described by Britannica as a poet who blended "
                 "popular and scholastic styles and modified traditional Tamil poetry. "
                 "That combination matters to an editor: a line may be accessible "
                 "without being casual, and a classical echo may sit beside a direct "
                 "public address. Rather than label one voice 'pure' and another "
                 "'modern', a close reading asks what the diction, rhythm, and intended "
                 "audience are doing together. His example belongs to a broader change "
                 "in Tamil writing, not a single break with the past."),
        source_url="https://www.britannica.com/topic/Tamil",
        reading=("பாரதி கவிதையை வாசிக்கும் போது, எளிய சொல் தேர்வும் பழைய "
                 "இலக்கிய நினைவுகளும் ஒன்றாக இருக்க முடியும். ஒரு வரி நேரடியாகப் "
                 "பேசுகிறது; அடுத்த வரி பழைய செய்யுள் மரபை நினைவூட்டுகிறது. "
                 "இரண்டையும் ஒன்றுக்கொன்று எதிராக வைக்காமல், கவிஞர் எதை "
                 "புதிய வாசகரிடம் கொண்டு செல்ல முயல்கிறார் என்று பார்க்கலாம். "
                 "அவருடைய மொழிநடை மக்களிடம் பேசுவதற்கும் இலக்கிய மரபுடன் "
                 "உரையாடுவதற்கும் இடம் செய்கிறது."),
        reading_gloss=("When reading Bharati's poetry, a simple choice of words and "
                       "memories of older literature can coexist. One line speaks "
                       "directly; the next recalls an older poetic tradition. Rather "
                       "than set the two against each other, we can ask what the poet "
                       "is trying to bring to a new reader. His register makes room "
                       "both to address the public and to converse with literary tradition."),
        listening=("இந்த வரி பழைய மரபைத் தொடர்கிறதா, மாற்றுகிறதா? — இரண்டுமே "
                   "இருக்கலாம். சொற்களின் எளிமை வாசகரை நெருங்குகிறது; பழைய "
                   "உருவகம் வேறு அடுக்கைத் திறக்கிறது. — அப்படியானால் "
                   "மொழிநடையை ஒரே பெயரில் முடிக்க வேண்டாமா? — ஆம்; "
                   "சூழலையும் நோக்கத்தையும் விளக்க வேண்டும்."),
        listening_gloss=("Does this line continue or change an older tradition? — It "
                         "may do both. Simple words bring the reader closer; an older "
                         "image opens another layer. — Then should we avoid reducing "
                         "the register to one label? — Yes; explain the context and aim."),
        voice_tag=VOICE,
        idioms=[
            ("எண்ணித் துணிக கருமம்", "think, then undertake the deed", "consider carefully before acting"),
            ("நாவில் தேன்", "honey on the tongue", "to speak sweetly or flatter"),
            ("சொல் ஒன்று செயல் ஒன்று", "one word, another action", "to say one thing and do another"),
            ("வார்த்தையை அளந்து பேசுதல்", "to measure words before speaking", "to speak with care"),
            ("சொல்லாமல் உணர்த்துதல்", "to make understood without saying", "to imply through image or context"),
            ("அடிக்கோடிட்டு காட்டுதல்", "to show by underlining", "to emphasise a point"),
            ("வாதத்தைத் திசைதிருப்புதல்", "to turn an argument aside", "to divert a discussion from its issue"),
            ("கேட்டும் கேளாதது போல", "as if not hearing after hearing", "to ignore something deliberately"),
            ("சொல்லின் செல்வம்", "the wealth of words", "the richness of expression"),
            ("நாவன்மை", "strength of the tongue", "eloquence, the power to speak well"),
        ],
        mistakes=[
            ("ஒரு நடை மட்டுமே தூயது; மற்றவை தவறு.", "ஒவ்வொரு நடையும் அதன் சூழல், வாசகர், நோக்கம் ஆகியவற்றோடு மதிப்பிடப்பட வேண்டும்.", "Do not treat a single register as inherently authentic or the only correct one."),
            ("எளிய சொல் தேர்வு இலக்கிய ஆழத்தை நீக்குகிறது.", "எளிய சொல் தேர்வும் இலக்கிய ஆழமும் ஒன்றாக இருக்கலாம்.", "Accessible language does not automatically remove literary complexity."),
            ("இந்த வரி பழைய மரபை முற்றிலும் மறுக்கிறது. (it adapts it)", "இந்த வரி பழைய மரபை மாற்றி உரையாடுகிறது.", "Describe adaptation rather than claiming a total break without evidence."),
        ],
        task_title="மொழிநடையைப் பற்றிய தொகுப்புக் குறிப்பு",
        task_instructions=("Write an editorial note on a short modern Tamil poem that contains both "
                           "direct public language and a literary echo. Identify the audience, "
                           "one register shift, and one tradition the poem adapts. Quote only a "
                           "brief phrase, distinguish your interpretation from the source's "
                           "documented facts, and avoid ranking registers as pure or impure."),
    ),
    "test": [
        ("translate_en", "Say: The study's result cannot be directly generalised to other districts.", "இந்த ஆய்வின் முடிவை வேறு மாவட்டங்களுக்கு நேரடியாகப் பொதுமைப்படுத்த முடியாது."),
        ("translate_ta", "முதன்முதலில் சொல்லை வரையறுத்து, பின்னர் ஒரே வடிவத்தைப் பயன்படுத்தவும்.", "Define the term at first use, then use one form consistently."),
        ("multiple_choice", "Which phrase means 'in contrast'?", "இதற்கு மாறாக"),
        ("fill_in_the_blank", "முடிவுக்குப் பிறகு ___ வரம்பைச் சொல்கிறோம்.", "இருப்பினும்"),
        ("word_selection", "Select the Tamil for 'glossary'.", "சொற்களஞ்சியம்"),
        ("error_correction", "இரண்டு ஆய்வுகளும் ஒரே முறையைப் பயன்படுத்தின. (one survey, one interview)", "இரண்டு ஆய்வுகளும் வெவ்வேறு முறைகளைப் பயன்படுத்தின."),
        ("dialogue_completion", "என் முடிவை எல்லா வயதினருக்கும் நீட்டிக்கலாமா? — இல்லை; ___ குறிப்பிட வேண்டும்.", "ஆய்வின் வரம்பை"),
        ("matching", "Match நிலுவையில் உள்ளது to its meaning.", "is pending"),
        ("reading_comprehension", "What two styles does the culture note say Bharati brought together?", "popular and scholastic styles"),
        ("inference", "Why should an editor avoid calling one voice 'pure' and another 'modern'?", "because a poem can combine registers and traditions"),
        ("main_idea", "What is the reading mainly about?", "simple diction and older literary echoes can coexist"),
        ("detail_identification", "What does the reading say the register makes room for?", "public address and conversation with literary tradition"),
    ],
}

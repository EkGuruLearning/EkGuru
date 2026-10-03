# -*- coding: utf-8 -*-
"""German PHASE 1 depth — extras, third lessons, half-step rungs.

Written with the DSL in `tools/depth_kit.py`; rendered by
`tools/author-depth.py --lang de`.

House style follows the shipped German course: standard German (Hochdeutsch)
with the course's own romanisation (stressed syllable in CAPITALS, syllables
hyphenated), speakers Lena and Max, and unit ids in the course's own shape
(`A1-U1` for the CEFR rungs, `de-c1-u1` for C1/C2). Half-step rungs use
`<rung>-U1`, e.g. `A1+-U1`, so a lesson id is unique across all sixteen files.

Register note: the dialogues between Lena and Max use `du`; every exchange
where one speaker is older, a stranger or a colleague at first meeting uses
`Sie`, and the difference is taught explicitly rather than dodged, because it
is the first decision every German sentence forces on the speaker.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # tools/ on the path
from depth_kit import D, EXTRA, G, L, T, V, WS, X   # noqa: E402

CODE = "de"
NAME = "German"
NATIVE = "Deutsch"
PHASE = 1
SCRIPT = "German"
VOICE = "de-DE"
SKILL = ("German: verb-second word order, four cases with article agreement, separable prefixes, "
         "Perfekt vs Präteritum, modal particles, and Konjunktiv register — measured by clause "
         "architecture and by choosing du or Sie before the first verb.")

EXTRAS = {}
THIRD = {}
HALFSTEPS = {}


# ── the six CEFR rungs ──────────────────────────────────────────────────────

EXTRAS["A1"] = EXTRA(
    culture=("The first decision in every German sentence is not the verb but the pronoun: du or "
             "Sie. Du is for family, friends, students and anyone who has offered it; Sie is for "
             "strangers, officials, most colleagues until someone proposes the switch — and the "
             "proposal always comes from the older or senior person, usually with «Wollen wir uns "
             "duzen?». Getting this wrong is heard as either coldness or presumption, not as bad "
             "grammar, which is why A1 spends a whole lesson on it."),
    source_url="https://en.wikipedia.org/wiki/German_language",
    reading=("Lena kommt neu in die Klasse. Sie sagt: «Guten Morgen, ich heiße Lena. Wie heißt du?» "
             "Max antwortet: «Ich bin Max. Woher kommst du?» — «Aus Hamburg. Und du?» — «Aus Köln.» "
             "Der Lehrer kommt herein und sagt: «Guten Morgen! Ich bin Herr Wolf.» Alle sagen: "
             "«Guten Morgen, Herr Wolf!»"),
    reading_gloss=("Lena comes into the class for the first time. She says: 'Good morning, my name "
                   "is Lena. What is your name?' Max answers: 'I am Max. Where are you from?' — "
                   "'From Hamburg. And you?' — 'From Cologne.' The teacher comes in and says: 'Good "
                   "morning! I am Mr Wolf.' Everyone says: 'Good morning, Mr Wolf!'"),
    listening=("Lena: Hallo! Ich heiße Lena. Wie heißt du?<br>Max: Ich bin Max. Wie geht es dir?<br>"
               "Lena: Gut, danke. Und dir?<br>Max: Auch gut. Woher kommst du?"),
    listening_gloss=("Lena: Hello! My name is Lena. What is your name? Max: I am Max. How are you? "
                     "Lena: Good, thanks. And you? Max: Also good. Where are you from?"),
    voice_tag=VOICE,
    idioms=[
        ("Daumen drücken", "pressing thumbs", "to keep one's fingers crossed"),
        ("Alles Gute", "all good", "all the best"),
        ("Es geht", "it goes", "I'm all right / so-so"),
        ("Mach's gut", "do it well", "take care (leave-taking)"),
        ("Bis bald", "until soon", "see you soon"),
        ("Guten Appetit", "good appetite", "enjoy your meal"),
        ("Herzlich willkommen", "heartily welcome", "a warm welcome"),
        ("Viel Spaß", "much fun", "have fun"),
        ("Gute Reise", "good journey", "have a good trip"),
        ("Wie geht's?", "how goes it?", "how are you? (du)"),
    ],
    mistakes=[
        ("Ich bin gut.", "Mir geht es gut.", "«Bist du gut?» asks about quality or skill; the state is «mir geht es gut»."),
        ("Ich heiße bin Max.", "Ich heiße Max. / Ich bin Max.", "heißen and sein are two different verbs; one sentence uses one."),
        ("Guten Morgen, wie geht's Ihnen, Max?", "Guten Morgen, wie geht's dir, Max?", "First names take du; «wie geht's Ihnen» belongs with Herr/Frau + surname."),
    ],
    task_title="Introduce yourself twice",
    task_instructions=("Write the same introduction twice in German: once to a classmate (du), once "
                       "to a professor's secretary at a first meeting (Sie, surname, no first name). "
                       "Read both aloud. Then swap one word and check that the whole sentence still "
                       "agrees — verb form, possessive and greeting all follow the pronoun you "
                       "chose, and a mixed pair is what a listener hears first."),
)

EXTRAS["A2"] = EXTRA(
    culture=("German eating has two speeds. The Abendbrot — bread, cheese, cold cuts, eaten at "
             "six — is not a snack but the evening meal, and it is eaten cold on purpose. The other "
             "speed is the Imbiss: currywurst, döner and fries eaten standing, in paper, at eleven "
             "at night after a concert. A2 covers ordering because the phrases are short, real and "
             "forgiving; the cultural note is that «Abendbrot» as an invitation is a home meal, "
             "never a restaurant."),
    source_url="https://en.wikipedia.org/wiki/German_cuisine",
    reading=("Um sechs Uhr gibt es Abendbrot. Auf dem Tisch stehen Brot, Käse, Wurst und Tee. Meine "
             "Mutter fragt: «Möchtest du noch ein Brot?» Ich sage: «Nein, danke, ich bin satt.» "
             "Später gehen wir zum Imbiss an der Ecke: eine Currywurst mit Pommes, vier Euro "
             "fünfzig. Der Verkäufer sagt: «Guten Appetit!»"),
    reading_gloss=("At six o'clock there is Abendbrot. On the table stand bread, cheese, sausage "
                   "and tea. My mother asks: 'Would you like another sandwich?' I say: 'No thanks, "
                   "I'm full.' Later we go to the snack stand on the corner: a currywurst with "
                   "fries, four euros fifty. The seller says: 'Enjoy your meal!'"),
    listening=("Max: Was möchtest du trinken?<br>Lena: Einen Kaffee, bitte.<br>"
               "Max: Und zu essen?<br>Lena: Ein Brot mit Käse. — Zahlen, bitte!"),
    listening_gloss=("Max: What would you like to drink? Lena: A coffee, please. Max: And to eat? "
                     "Lena: A sandwich with cheese. — The bill, please!"),
    voice_tag=VOICE,
    idioms=[
        ("Ich habe Hunger", "I have hunger", "I am hungry"),
        ("Es tut mir leid", "it does me sorrow", "I am sorry"),
        ("Kein Problem", "no problem", "no problem"),
        ("Ich freue mich", "I rejoice myself", "I am looking forward to it"),
        ("Auf jeden Fall", "in every case", "definitely"),
        ("Es lohnt sich", "it rewards itself", "it is worth it"),
        ("Wie viel kostet das?", "how much costs that?", "how much is this?"),
        ("Zusammen oder getrennt?", "together or separate?", "one bill or two?"),
        ("Das stimmt", "that agrees", "that's right"),
        ("Bis später", "until later", "see you later"),
    ],
    mistakes=[
        ("Ich habe Kaffee möchten.", "Ich möchte einen Kaffee.", "möchten is the verb; put it second and the drink in the accusative."),
        ("Ich bin Hunger.", "Ich habe Hunger.", "Hunger is had, not been; sein here means «I am hunger» to a German ear."),
        ("Zahlen bitte, ich will bezahlen die Rechnung.", "Zahlen, bitte! / Ich möchte die Rechnung bezahlen.", "The restaurant phrase is fixed and short; the full sentence keeps the infinitive last."),
    ],
    task_title="Order at the Imbiss",
    task_instructions=("Write an eight-line Imbiss dialogue in German: greet, order food, order a "
                       "drink, ask the price, pay, say goodbye. Use «ich möchte» once, «bitte» "
                       "twice and no English. Then read it with a partner and change the order to "
                       "two people — «zusammen oder getrennt?» — which forces the plural verb forms "
                       "and is where most learners slip from du to ihr."),
)

EXTRAS["B1"] = EXTRA(
    culture=("The German route into working life runs through the Ausbildung: a two- to "
             "three-and-a-half-year apprenticeship, half at a company half at a state vocational "
             "school, ending in a chamber exam. It is not a fallback — bank clerks, nurses "
             "and IT specialists all qualify that way, and the word «Azubi» is said with no "
             "apology. B1 needs the vocabulary because work is the first place learners are asked "
             "to talk about their own plans in a register that is neither school nor home."),
    source_url="https://en.wikipedia.org/wiki/Ausbildung",
    reading=("Lena macht eine Ausbildung als Krankenschwester. Drei Tage arbeitet sie im "
             "Krankenhaus, zwei Tage geht sie zur Berufsschule. «Am Anfang war es schwer», sagt "
             "sie. «Ich hatte Angst vor dem ersten Frühdienst.» Nach zwei Jahren sagt sie: «Die "
             "Ausbildung passt zu mir. Nächstes Jahr habe ich Prüfung, danach möchte ich auf der "
             "Intensivstation arbeiten.»"),
    reading_gloss=("Lena is doing an apprenticeship as a nurse. Three days she works in the "
                   "hospital, two days she goes to the vocational school. 'At the beginning it was "
                   "hard,' she says. 'I was afraid of the first early shift.' After two years she "
                   "says: 'The apprenticeship suits me. Next year I have my exam; after that I want "
                   "to work in intensive care.'"),
    listening=("Chef: Was machen Sie beruflich?<br>Max: Ich lerne noch — ich bin im dritten Jahr<br>"
               "Chef: Und danach?<br>Max: Danach bleibe ich gern hier. Ich möchte mehr Verantwortung übernehmen."),
    listening_gloss=("Boss: What do you do for a living? Max: I am still training — I'm in my "
                     "third year. Boss: And afterwards? Max: Afterwards I'd gladly stay here. I'd "
                     "like to take on more responsibility."),
    voice_tag=VOICE,
    idioms=[
        ("Feierabend machen", "to make evening-off", "to clock off for the day"),
        ("Blaumachen", "to make blue", "to skip work or school"),
        ("Schwein haben", "to have pig", "to be lucky"),
        ("Die Nase voll haben", "to have the nose full", "to be fed up"),
        ("Ins Fettnäpfchen treten", "to step in the grease pot", "to put one's foot in it"),
        ("Tomaten auf den Augen haben", "to have tomatoes on the eyes", "to miss something obvious"),
        ("Alles in Butter", "everything in butter", "all is well"),
        ("Auf dem Schlauch stehen", "to stand on the hose", "to be completely lost"),
        ("Da steppt der Bär", "the bear tap-dances there", "it's buzzing / great fun"),
        ("Kohle verdienen", "to earn coal", "to earn money"),
    ],
    mistakes=[
        ("Ich habe 25 Jahre.", "Ich bin 25 Jahre alt.", "Age takes sein, not haben, and the phrase needs alt."),
        ("Ich arbeite hier seit drei Jahre.", "Ich arbeite hier seit drei Jahren.", "seit takes the dative plural: drei Jahren."),
        ("Ich will nach Hause gehen, weil ich bin müde.", "…, weil ich müde bin.", "In a weil-clause the verb moves to the end."),
    ],
    task_title="Describe your working life in ninety seconds",
    task_instructions=("Record ninety seconds in German about what you do and what comes next: "
                       "present job or study, one thing that was hard at the start, one plan for "
                       "next year. Use a weil-clause with the verb last, one separable verb, and "
                       "«möchte» for the plan. Listen back and count the sentences where the verb "
                       "is in the wrong position — those are the ones to rewrite, not the ones to "
                       "memorise."),
)

EXTRAS["B2"] = EXTRA(
    culture=("German small talk is short; German argument is long. A Verein — the registered club "
             "for football, choirs, carnival or pigeon breeding — is where both happen: sixty "
             "million memberships, and the place a new arrival meets the town without a job "
             "attached. At work the same people who answer «Wie geht's?» with one word will argue "
             "a technical point for an hour with sources, and neither is rudeness. B2 teaches the "
             "argument register: state, support, concede, close."),
    source_url="https://en.wikipedia.org/wiki/German_culture",
    reading=("In der Sitzung sagt Herr Wolf: «Die neue Regel hat einen Vorteil: sie ist klar. Sie "
             "hat aber auch einen Nachteil: sie kostet Zeit.» Frau Berger antwortet: «Da haben Sie "
             "recht. Trotzdem möchte ich den Aufwand messen, bevor wir sie beschließen.» Am Ende "
             "sagt der Chef: «Wir testen die Regel drei Monate und entscheiden dann.» So läuft "
             "eine deutsche Besprechung: erst der Punkt, dann der Einwand, dann der Test."),
    reading_gloss=("In the meeting Mr Wolf says: 'The new rule has one advantage: it is clear. But "
                   "it also has a disadvantage: it costs time.' Ms Berger answers: 'You're right "
                   "about that. Even so, I'd like to measure the effort before we decide.' At the "
                   "end the boss says: 'We'll test the rule for three months and then decide.' That "
                   "is how a German meeting runs: first the point, then the objection, then the test."),
    listening=("Moderator: Finden Sie die Regel gut?<br>Frau Berger: Im Prinzip ja, aber ich sehe ein Problem.<br>"
               "Moderator: Welches?<br>Frau Berger: Sie ist nicht messbar. Deshalb schlage ich einen Test vor."),
    listening_gloss=("Moderator: Do you think the rule is good? Ms Berger: In principle yes, but I "
                     "see a problem. Moderator: Which? Ms Berger: It is not measurable. That is why "
                     "I suggest a test."),
    voice_tag=VOICE,
    idioms=[
        ("Den Nagel auf den Kopf treffen", "to hit the nail on the head", "to say exactly the right thing"),
        ("Zwei Fliegen mit einer Klappe schlagen", "to hit two flies with one flap", "to kill two birds with one stone"),
        ("Das ist nicht mein Bier", "that is not my beer", "that's not my business"),
        ("Da haben wir den Salat", "there we have the salad", "now we're in a mess"),
        ("Den Wald vor lauter Bäumen nicht sehen", "not to see the forest for the trees", "to miss the big picture"),
        ("Mit Kanonen auf Spatzen schießen", "to shoot sparrows with cannons", "to use a sledgehammer to crack a nut"),
        ("Kein Blatt vor den Mund nehmen", "to take no leaf before the mouth", "to speak bluntly"),
        ("Perlen vor die Säue werfen", "to throw pearls before swine", "to waste something good on the wrong audience"),
        ("Da liegt der Hund begraben", "the dog is buried there", "that's the crux of the matter"),
        ("Das ist der springende Punkt", "the jumping point", "that's the decisive point"),
    ],
    mistakes=[
        ("Ich bin einverstanden mit dir, trotzdem ich habe Zweifel.", "…, trotzdem habe ich Zweifel.", "trotzdem is an adverb: it takes position 1 or 3, and then the verb comes second."),
        ("Ich habe mit dem Projekt angefangen seit zwei Wochen.", "Ich habe vor zwei Wochen mit dem Projekt angefangen.", "Duration is «seit», a point in the past is «vor»."),
        ("Deshalb ich schlage vor…", "Deshalb schlage ich vor…", "After deshalb the verb comes before the subject."),
    ],
    task_title="Argue one point through four moves",
    task_instructions=("Pick a rule in your workplace or study programme and write four German "
                       "paragraphs: the point, the advantage, the objection («da haben Sie recht, "
                       "trotzdem …»), and the test or compromise you propose. Then say it aloud in "
                       "two minutes without notes. If a sentence starts with deshalb, trotzdem or "
                       "außerdem, check that the verb has not stayed in the English position."),
)

EXTRAS["C1"] = EXTRA(
    culture=("German institutional prose runs on the Nominalstil: verbs become nouns, nouns stack "
             "into compounds, and one sentence can carry a whole paragraph — «die Gewährung der "
             "Fristverlängerung erfolgt nach Prüfung der Voraussetzungen». It is not decoration; it "
             "is how law, administration and science compress a condition into a thing that can be "
             "referenced later. C1 is the level where you learn both to read it without parsing "
             "twice and to rewrite it as a verb sentence when a human has to act on it."),
    source_url="https://en.wikipedia.org/wiki/German_grammar",
    reading=("«Die Verlängerung der Frist setzt die Vorlage eines Nachweises voraus», heißt es im "
             "Bescheid. Der Satz enthält zwei Handlungen in zwei Substantiven. Wer ihn in "
             "Verantwortung übersetzen will, schreibt: «Wenn Sie den Nachweis vorlegen, können wir "
             "die Frist verlängern.» Derselbe Inhalt, ein Drittel der Wörter, ein Akteur. Genau "
             "diese Übersetzung ist die Arbeit von C1."),
    reading_gloss=("'The extension of the deadline presupposes the submission of a proof,' says the "
                   "official notice. The sentence contains two actions inside two nouns. Anyone who "
                   "wants to translate it into responsibility writes: 'If you submit the proof, we "
                   "can extend the deadline.' The same content, a third of the words, one actor. "
                   "Exactly that translation is the work of C1."),
    listening=("Referent: Der Antrag wurde abgelehnt, weil die Frist nicht eingehalten wurde.<br>"
               "Kollegin: Kann man das genauer sagen?<br>Referent: Ja: Sie haben zu spät eingereicht.<br>"
               "Kollegin: Danke — so versteht es jeder."),
    listening_gloss=("Officer: The application was rejected because the deadline was not met. "
                     "Colleague: Can that be said more precisely? Officer: Yes: you submitted too "
                     "late. Colleague: Thanks — that way everybody understands it."),
    voice_tag=VOICE,
    idioms=[
        ("Etwas in Kauf nehmen", "to take something in purchase", "to accept a drawback"),
        ("Auf Messers Schneide stehen", "to stand on the knife's edge", "to hang in the balance"),
        ("Das Heft in der Hand haben", "to hold the notebook in hand", "to be in control"),
        ("Den Finger in die Wunde legen", "to lay a finger in the wound", "to name the sore point"),
        ("Das Ruder herumreißen", "to yank the rudder around", "to turn things around"),
        ("Einen Schlussstrich ziehen", "to draw a closing line", "to draw a line under it"),
        ("Zug um Zug", "move by move", "step by step, tit for tat"),
        ("Auf der Kippe stehen", "to stand on the tipping edge", "to be touch-and-go"),
        ("Sich die Finger verbrennen", "to burn one's fingers", "to get one's fingers burnt"),
        ("Etwas auf die lange Bank schieben", "to push something onto the long bench", "to shelve something"),
    ],
    mistakes=[
        ("Die Frist wurde verlängert, weil der Nachweis wurde vorgelegt.", "…, weil der Nachweis vorgelegt wurde.", "Subordinate clause: the finite verb goes last, the participle before it."),
        ("Man muss die Voraussetzungen prüfen, die für die Verlängerung.", "…prüfen, die für die Verlängerung gelten.", "The relative clause needs its own verb."),
        ("Der Antrag ist abgelehnt geworden.", "Der Antrag wurde abgelehnt.", "Passiv with werden; «ist abgelehnt worden» is the perfect form, not «geworden»."),
    ],
    task_title="Un-nominalise one paragraph",
    task_instructions=("Find one paragraph of German administrative or academic prose — a form "
                       "letter, a handbook page, an abstract — and rewrite it twice: once with the "
                       "verbs restored and one actor per sentence, once for a reader who has ninety "
                       "seconds. Then write the original and both versions side by side and mark "
                       "the nouns that turned back into verbs. That list is the C1 vocabulary."),
)

EXTRAS["C2"] = EXTRA(
    culture=("German has a literature of ideas read aloud: Lessing's arguments, Brecht's "
             "interruptions, Kafka's paragraphs that never quite resolve. The practical effect on "
             "C2 is that quotation is normal — an essay quotes a phrase and then reverses it, and "
             "the reversal is the argument. Readers are expected to hear the borrowed phrase, which "
             "is why C2 drills allusion, parallelism and irony rather than more vocabulary lists."),
    source_url="https://en.wikipedia.org/wiki/German_literature",
    reading=("Ein Essay beginnt: «Es ist nicht alles Gold, was glänzt — dieser Satz ist wahr und "
             "wird trotzdem falsch, sobald man ihn als Urteil über Menschen benutzt.» Der Autor "
             "zitiert also, um zu widersprechen. Wer die Anspielung nicht hört, liest nur eine "
             "Behauptung. Wer sie hört, liest eine Bewegung: erst die übernommene Formel, dann ihre "
             "Umkehrung, dann die Begründung."),
    reading_gloss=("An essay begins: 'All that glitters is not gold — that sentence is true and "
                   "becomes false the moment you use it as a verdict on people.' So the author "
                   "quotes in order to contradict. Whoever does not hear the allusion reads only a "
                   "claim. Whoever hears it reads a movement: first the borrowed formula, then its "
                   "reversal, then the reasoning."),
    listening=("Autorin: Ihr Text zitiert Goethe und widerspricht ihm.<br>Interviewer: Ist das nicht riskant?<br>"
               "Autorin: Nein — nur wenn man den Satz nur noch als Zitat liest.<br>Interviewer: Also rechnen Sie mit Lesern, die ihn kennen."),
    listening_gloss=("Author: Your text quotes Goethe and contradicts him. Interviewer: Isn't that "
                     "risky? Author: No — only if one still reads the sentence merely as a "
                     "quotation. Interviewer: So you count on readers who know it."),
    voice_tag=VOICE,
    idioms=[
        ("Das Kind mit dem Bade ausschütten", "to throw the child out with the bathwater", "to throw out the good with the bad"),
        ("Eulen nach Athen tragen", "to carry owls to Athens", "to carry coals to Newcastle"),
        ("Den Rubikon überschreiten", "to cross the Rubicon", "to pass the point of no return"),
        ("Wie ein Damoklesschwert", "like a sword of Damocles", "a threat hanging overhead"),
        ("Sisyphusarbeit", "Sisyphus work", "endless, futile labour"),
        ("Mit zweierlei Maß messen", "to measure with two different measures", "to apply double standards"),
        ("Eine Lanze brechen für", "to break a lance for", "to champion someone or something"),
        ("Den Teufel an die Wand malen", "to paint the devil on the wall", "to be a doomsayer"),
        ("Etwas auf den Punkt bringen", "to bring something to the point", "to state it precisely"),
        ("Zwischen den Zeilen lesen", "to read between the lines", "to read between the lines"),
    ],
    mistakes=[
        ("Der Konjunktiv I zeigt, dass er glaubt es.", "Der Konjunktiv I zeigt, dass er es glaubt / er glaube es.", "Embedded clauses need one finite verb each; the evidential form replaces, not doubles it."),
        ("Es ist nicht alles Gold was glänzt.", "Es ist nicht alles Gold, was glänzt.", "The comma marks the relative clause — and quoting the proverb ironically does not make it a proof: C2 reads the stance, not only the words."),
        ("Ich bin davon überzeugt, dass das stimmt, oder?", "…, dass das stimmt.", "Modal particles push a claim toward the listener; in argument they can undercut the very certainty they mark."),
    ],
    task_title="Quote, reverse, justify",
    task_instructions=("Write one German paragraph of C2 argument in three moves: quote a proverb "
                       "or a famous line, reverse it, and justify the reversal with a case the "
                       "original misses. Then cut every adjective that only adds emphasis and check "
                       "whether the reversal still stands. If it does, the paragraph was an "
                       "argument; if it does not, it was decoration."),
)

# ── the third lesson of every CEFR unit ─────────────────────────────────────

THIRD["A1"] = [
    ("A1-U1", "A1-U1-L3", L(
        "Woher kommst du? Countries, languages, origins",
        "Origin takes aus + country: ICH KOMME AUS INDIEN. With countries that carry an article "
        "(die Schweiz, die Türkei, der Iran) it becomes AUS DER SCHWEIZ. Languages are their own "
        "words: ICH SPRECHE ENGLISCH UND EIN BISSCHEN DEUTSCH.",
        [V("aus", "aus", "from (a country or city)", "preposition"),
         V("das Land", "das LANT", "country", "noun"),
         V("die Sprache", "dee SHPRAH-khuh", "language", "noun"),
         V("sprechen", "SHPREH-khen", "to speak", "verb"),
         V("ein bisschen", "ine BISS-khen", "a little", "adverb")],
        G("Origin and language",
          "ich komme aus + country · ich spreche + language",
          "Ich komme aus Indien. Ich wohne in Berlin, aber ich komme aus Japan. «Woher …?» asks "
          "origin, «wo …?» asks where you are now — the answers use aus and in.",
          [X("Ich komme aus Indien.", "ikh KOM-muh ows IN-dee-en.", "I come from India."),
           X("Sie wohnt in Berlin, aber sie kommt aus der Schweiz.", "zee VOHNT in ber-LEEN, AH-ber zee KOMT ows dair SHVYTS.", "She lives in Berlin but comes from Switzerland."),
           X("Sprechen Sie Englisch?", "SHPREH-khen zee ENG-lish?", "Do you speak English?")],
          [("Ich komme von Indien.", "Ich komme aus Indien.", "Countries take aus; von is for people and places you pass through."),
           ("Ich bin aus die Schweiz.", "Ich bin aus der Schweiz.", "Countries with an article take the dative after aus.")]),
        [D("Max", "Woher kommst du, Lena?", "voh-HAIR komst doo, LAY-nah?", "Where are you from, Lena?"),
         D("Lena", "Aus Hamburg. Und du?", "ows HAHM-boork. unt doo?", "From Hamburg. And you?"),
         D("Max", "Ich komme aus der Schweiz, aber ich wohne in Köln.", "ikh KOM-muh ows dair SHVYTS, AH-ber ikh VOH-nuh in kurln.", "I come from Switzerland, but I live in Cologne."),
         D("Lena", "Und welche Sprachen sprichst du?", "unt VEL-kheh SHPRAH-khen shprikhst doo?", "And which languages do you speak?")],
        WS("Origin worksheet", [
            T("Answer with aus.", ["Where are you from? (India)", "Where does she come from? (Switzerland)"],
              ["Ich komme aus Indien.", "Sie kommt aus der Schweiz."]),
            T("Add the language.", ["German and a little English", "only Hindi"],
              ["Deutsch und ein bisschen Englisch", "nur Hindi"]),
        ]))),
    ("A1-U2", "A1-U2-L3", L(
        "Living: rooms, furniture and es gibt",
        "A home is described with ES GIBT + accusative: ES GIBT EINEN TISCH (there is a table) — "
        "einen shows the case. Rooms: DAS WOHNZIMMER, DIE KÜCHE, DAS SCHLAFZIMMER, DAS BAD.",
        [V("es gibt", "es geept", "there is / there are", "phrase"),
         V("das Wohnzimmer", "das VOHN-tsim-mer", "living room", "noun"),
         V("die Küche", "dee KEW-khuh", "kitchen", "noun"),
         V("das Schlafzimmer", "das SHLAHF-tsim-mer", "bedroom", "noun"),
         V("der Tisch", "dair tish", "table", "noun")],
        G("es gibt + accusative",
          "es gibt einen/ein/eine + noun",
          "Es gibt einen Tisch, ein Sofa und eine Lampe. Masculine nouns change to einen, feminine "
          "and neuter stay — the one visible change is the marker of the case.",
          [X("Es gibt einen Tisch in der Küche.", "es geept EYE-nen tish in dair KEW-khuh.", "There is a table in the kitchen."),
           X("Die Wohnung hat drei Zimmer.", "dee VOH-noong hat dry TSIM-mer.", "The flat has three rooms."),
           X("Mein Zimmer ist klein, aber hell.", "mine TSIM-mer ist kline, AH-ber hel.", "My room is small but bright.")],
          [("Es gibt ein Tisch.", "Es gibt einen Tisch.", "es gibt always takes the accusative; masculine shows it."),
           ("Ich habe ein Bruder.", "Ich habe einen Bruder.", "haben also takes the accusative: einen Bruder.")]),
        [D("Lena", "Wie wohnst du, Max?", "vee VOHNST doo, maks?", "How do you live, Max?"),
         D("Max", "In einer kleinen Wohnung. Es gibt zwei Zimmer.", "in EYE-ner KLY-nen VOH-noong. es geept tsvy TSIM-mer.", "In a small flat. There are two rooms."),
         D("Lena", "Und eine Küche?", "unt EYE-nuh KEW-khuh?", "And a kitchen?"),
         D("Max", "Ja, und es gibt einen großen Tisch im Wohnzimmer.", "yah, unt es geept EYE-nen GROH-sen tish im VOHN-tsim-mer.", "Yes, and there is a big table in the living room.")],
        WS("Living worksheet", [
            T("Say what there is.", ["a table", "a bed", "a lamp"],
              ["Es gibt einen Tisch.", "Es gibt ein Bett.", "Es gibt eine Lampe."]),
            T("Describe your home.", ["two rooms and a kitchen", "a small bedroom"],
              ["zwei Zimmer und eine Küche", "ein kleines Schlafzimmer"]),
        ]))),
    ("A1-U3", "A1-U3-L3", L(
        "Weather and seasons: es ist kalt, es regnet",
        "Weather is spoken with es: ES REGNET, ES SCHNEIT, ES IST WARM. With zu + adjective it "
        "needs no noun: ES IST ZU KALT. Seasons take im: IM WINTER, IM SOMMER.",
        [V("es regnet", "es RAYG-net", "it is raining", "phrase"),
         V("es schneit", "es SHNYTE", "it is snowing", "phrase"),
         V("der Winter", "dair VIN-ter", "winter", "noun"),
         V("warm", "varm", "warm", "adjective"),
         V("zu", "tsoo", "too (before an adjective)", "adverb")],
        G("Weather with es",
          "es ist + adjective · es + verb (regnet/schneit)",
          "Es ist heute kalt, aber die Sonne scheint. Im Sommer ist es sehr warm, im Winter "
          "schneit es oft. Compare English «it is» — German keeps the same impersonal es.",
          [X("Es ist heute kalt.", "es ist HOY-tuh kalt.", "It is cold today."),
           X("Im Winter schneit es oft.", "im VIN-ter SHNYTE es oft.", "In winter it often snows."),
           X("Es ist zu warm für eine Jacke.", "es ist tsoo varm fewr EYE-nuh YAH-kuh.", "It is too warm for a jacket.")],
          [("Es ist kalt heute?", "Ist es heute kalt?", "In a statement and a yes/no question the verb keeps position 2."),
           ("Ich bin kalt.", "Mir ist kalt.", "A person feels cold with mir ist kalt; «ich bin kalt» describes a cold character.")]),
        [D("Max", "Wie ist das Wetter heute?", "vee ist das VET-ter HOY-tuh?", "How is the weather today?"),
         D("Lena", "Es ist kalt und es regnet.", "es ist kalt unt es RAYG-net.", "It is cold and it is raining."),
         D("Max", "Im Winter regnet es hier nie — es schneit.", "im VIN-ter RAYG-net es heer nee — es SHNYTE.", "In winter it never rains here — it snows."),
         D("Lena", "Dann brauchen wir eine warme Jacke.", "dan BROW-khen veer EYE-nuh VAR-muh YAH-kuh.", "Then we need a warm jacket.")],
        WS("Weather worksheet", [
            T("Say the weather.", ["it rains", "it is snowing", "it is too warm"],
              ["Es regnet.", "Es schneit.", "Es ist zu warm."]),
            T("Answer with the season.", ["When is it warm? (summer)", "When does it snow? (winter)"],
              ["Im Sommer ist es warm.", "Im Winter schneit es."]),
        ]))),
]

THIRD["A2"] = [
    ("A2-U1", "A2-U1-L3", L(
        "By train: tickets, platforms, delays",
        "Station German is compact: EINE FAHRKARTE NACH BERLIN, BITTE. With changing trains: "
        "MÜSSEN SIE UMSTEIGEN? Delays are announced with the number first: «Der Zug nach Bonn "
        "fährt heute von Gleis sieben».",
        [V("die Fahrkarte", "dee FAHR-kar-tuh", "ticket (for a trip)", "noun"),
         V("das Gleis", "das glice", "platform, track", "noun"),
         V("umsteigen", "OOM-shty-gen", "to change trains", "verb"),
         V("die Verspätung", "dee fair-SHPHAY-toong", "delay", "noun"),
         V("der Anschluss", "dair AHN-shloos", "connection", "noun")],
        G("Tickets and connections",
          "Fahrkarte nach + city · von Gleis + number · Anschluss nach + city",
          "Eine Fahrkarte nach München, bitte — hin und zurück. Der Anschluss nach Hamburg ist "
          "auf Gleis zwölf. hin und zurück (return) is the phrase that halves the price of a "
          "mistake.",
          [X("Ich brauche eine Fahrkarte nach Berlin.", "ikh BROW-khuh EYE-nuh FAHR-kar-tuh nakh ber-LEEN.", "I need a ticket to Berlin."),
           X("Muss ich in Köln umsteigen?", "moos ikh in kurln OOM-shty-gen?", "Do I have to change in Cologne?"),
           X("Der Zug hat zwanzig Minuten Verspätung.", "dair tsook hat TSVAHN-tsikh mi-NOO-ten fair-SHPHAY-toong.", "The train is twenty minutes late.")],
          [("Ich brauche ein Ticket zu Berlin.", "Ich brauche eine Fahrkarte nach Berlin.", "German uses Fahrkarte and nach, not a borrowed ticket and zu."),
           ("Ich steige um in Köln um.", "Ich steige in Köln um.", "One um is the prefix, one the preposition: «umsteigen in».")]),
        [D("Lena", "Eine Fahrkarte nach Bonn, bitte.", "EYE-nuh FAHR-kar-tuh nakh bon, BIT-tuh.", "A ticket to Bonn, please."),
         D("Beamter", "Einfach oder hin und zurück?", "INE-fakh o-der hin unt tsoo-REWK?", "Single or return?"),
         D("Lena", "Hin und zurück. Muss ich umsteigen?", "hin unt tsoo-REWK. moos ikh OOM-shty-gen?", "Return. Do I have to change?"),
         D("Beamter", "Nein, direkt. Gleis fünf, Abfahrt in zehn Minuten.", "nine, di-REKT. glice fewnf, AP-fahrt in tsehn mi-NOO-ten.", "No, direct. Platform five, departure in ten minutes.")],
        WS("Train worksheet", [
            T("Buy a ticket.", ["to Munich, return", "a single to Hamburg"],
              ["Eine Fahrkarte nach München, hin und zurück, bitte.", "Eine einfache Fahrkarte nach Hamburg."]),
            T("Ask about the connection.", ["must I change?", "from which platform?", "is it late?"],
              ["Muss ich umsteigen?", "Von welchem Gleis?", "Hat der Zug Verspätung?"]),
        ]))),
    ("A2-U2", "A2-U2-L3", L(
        "At the doctor: symptoms and advice",
        "Illness is said with haben and weh tun: ICH HABE HALSSCHMERZEN · MEIN KOPF TUT WEH. The "
        "doctor answers with sollen: SIE SOLLEN VIEL TRINKEN — advice, not an order.",
        [V("der Termin", "dair ter-MEEN", "appointment", "noun"),
         V("die Schmerzen", "dee SHMAIR-tsen", "pain (plural)", "noun"),
         V("weh tun", "vay toon", "to hurt", "phrase"),
         V("das Rezept", "das ray-TSEPT", "prescription", "noun"),
         V("sollen", "ZOL-len", "should, to be advised to", "verb")],
        G("Symptoms and advice",
          "ich habe …schmerzen · es tut weh · Sie sollen …",
          "Ich habe Halsschmerzen und mein Kopf tut weh. Der Arzt sagt: «Sie sollen viel trinken "
          "und drei Tage zu Hause bleiben.» sollen is what a doctor, a teacher or a rota says — "
          "the advisor is named by the form itself.",
          [X("Ich habe Halsschmerzen.", "ikh HAH-buh HALS-shmair-tsen.", "I have a sore throat."),
           X("Mein Rücken tut weh.", "mine REW-ken toot vay.", "My back hurts."),
           X("Sie sollen im Bett bleiben.", "zee ZOL-len im bet BLY-ben.", "You should stay in bed.")],
          [("Ich habe Schmerz.", "Ich habe Schmerzen.", "The plural is the usual form; the singular is bookish and rare."),
           ("Ich bin krank mit Kopf.", "Ich habe Kopfschmerzen.", "German compounds the pain: Kopfschmerzen, Zahnschmerzen.")]),
        [D("Max", "Guten Tag, ich habe einen Termin.", "GOO-ten tahk, ikh HAH-buh EYE-nen ter-MEEN.", "Good day, I have an appointment."),
         D("Ärztin", "Was fehlt Ihnen?", "vas filet EEN-en?", "What is wrong with you?"),
         D("Max", "Ich habe Halsschmerzen und mein Kopf tut weh.", "ikh HAH-buh HALS-shmair-tsen unt mine kof toot vay.", "I have a sore throat and my head hurts."),
         D("Ärztin", "Sie sollen viel trinken und drei Tage zu Hause bleiben.", "zee ZOL-len feel TRIN-ken unt dry TAH-guh tsoo HOW-zuh BLY-ben.", "You should drink a lot and stay home for three days.")],
        WS("Doctor worksheet", [
            T("Say the symptom.", ["sore throat", "my back hurts", "a headache"],
              ["Ich habe Halsschmerzen.", "Mein Rücken tut weh.", "Ich habe Kopfschmerzen."]),
            T("Give the advice.", ["drink a lot", "stay home for three days"],
              ["Sie sollen viel trinken.", "Sie sollen zu Hause bleiben."]),
        ]))),
    ("A2-U3", "A2-U3-L3", L(
        "Exchanging and comparing: zu groß, günstiger",
        "Shopping problems need two tools: the comparative (GRÖSSER, BILLIGER, GÜNSTIGER) and "
        "UMTAUSCHEN. The shop answers with a condition: WENN SIE DEN KASSENZETTEL HABEN, "
        "TAUSCHEN WIR UM.",
        [V("umtauschen", "OOM-tow-shen", "to exchange", "verb"),
         V("der Kassenzettel", "dair KAS-sen-tset-tel", "receipt", "noun"),
         V("günstiger", "GEWN-sti-ger", "cheaper", "adjective"),
         V("die Größe", "dee GRUR-suh", "size", "noun"),
         V("passen", "PAS-sen", "to fit", "verb")],
        G("Comparing and exchanging",
          "X ist größer/günstiger als Y · können wir … umtauschen?",
          "Diese Jacke ist günstiger als die andere. Sie ist zu klein — können wir sie "
          "umtauschen? The comparative adds -er and takes als for «than»; zu + adjective says "
          "«too».",
          [X("Diese Hose ist zu groß.", "DEE-zuh HOH-zuh ist tsoo grohs.", "These trousers are too big."),
           X("Das Hemd ist günstiger als die Jacke.", "das hemt ist GEWN-sti-ger als dee YAH-kuh.", "The shirt is cheaper than the jacket."),
           X("Können wir das umtauschen?", "KUR-nen veer das OOM-tow-shen?", "Can we exchange this?")],
          [("Das ist größer wie das andere.", "Das ist größer als das andere.", "Comparative + als; «wie» belongs to equality (so groß wie)."),
           ("Ich will umtauschen das Hemd.", "Ich möchte das Hemd umtauschen.", "Separable verb: the prefix goes to the end.")]),
        [D("Lena", "Entschuldigung, diese Hose ist zu klein.", "ent-SHOOL-di-goong, DEE-zuh HOH-zuh ist tsoo kline.", "Excuse me, these trousers are too small."),
         D("Verkäuferin", "Haben Sie den Kassenzettel?", "HAH-ben zee dayn KAS-sen-tset-tel?", "Do you have the receipt?"),
         D("Lena", "Ja. Gibt es eine Nummer größer?", "yah. geept es EYE-nuh NUM-mer GRUR-ser?", "Yes. Is there a bigger size?"),
         D("Verkäuferin", "Ja, und diese ist auch günstiger.", "yah, unt DEE-zuh ist owkh GEWN-sti-ger.", "Yes, and this one is cheaper too.")],
        WS("Shopping worksheet", [
            T("Say the problem.", ["too big", "too small", "cheaper than the other one"],
              ["zu groß", "zu klein", "günstiger als die andere"]),
            T("Ask to exchange it.", ["can we exchange this?", "do you have a bigger size?"],
              ["Können wir das umtauschen?", "Haben Sie eine Nummer größer?"]),
        ]))),
]

THIRD["B1"] = [
    ("B1-U1", "B1-U1-L3", L(
        "Telling a story: erst, dann, plötzlich",
        "A German anecdote is built with time adverbs and the Präteritum for the frame: ZUERST "
        "WAR ES RUHIG, DANN KAM DER REGEN, PLÖTZLICH FIEL DER STROM AUS. The punchline takes "
        "Perfekt.",
        [V("zuerst", "tsoo-AIRST", "at first", "adverb"),
         V("dann", "dan", "then", "adverb"),
         V("plötzlich", "PLURTS-likh", "suddenly", "adverb"),
         V("auf einmal", "owf eye-NMAHL", "all at once", "phrase"),
         V("zum Schluss", "tsoom shloos", "in the end", "phrase")],
        G("Narrative frame",
          "Präteritum for the setting · Perfekt for the event · time adverb first",
          "Es war Samstag, wir waren müde. Plötzlich hat es an der Tür geklingelt. When a time "
          "adverb opens the sentence, the verb still comes second — «plötzlich hat es geklingelt».",
          [X("Zuerst war es ruhig.", "tsoo-AIRST vahr es ROO-ikh.", "At first it was quiet."),
           X("Dann ist der Strom ausgefallen.", "dan ist dair shtrohm OWS-ge-fal-len.", "Then the power went out."),
           X("Zum Schluss haben wir gelacht.", "tsoom shloos HAH-ben veer ge-LAKHT.", "In the end we laughed.")],
          [("Plötzlich es hat geklingelt.", "Plötzlich hat es geklingelt.", "The adverb occupies position 1, the verb position 2."),
           ("Ich habe gewesen müde.", "Ich war müde.", "States use the Präteritum form war, not the Perfekt of sein.")]),
        [D("Max", "Was ist gestern passiert?", "vas ist GES-tern pas-SEERT?", "What happened yesterday?"),
         D("Lena", "Zuerst war alles ruhig. Dann ist der Strom ausgefallen.", "tsoo-AIRST vahr AL-les ROO-ikh. dan ist dair shtrohm OWS-ge-fal-len.", "At first everything was quiet. Then the power went out."),
         D("Max", "Und dann?", "unt dan?", "And then?"),
         D("Lena", "Plötzlich hat es an der Tür geklingelt — der Nachbar hatte Kerzen.", "PLURTS-likh hat es an dair tewr ge-KLIN-gelt — dair NAKH-bar HAT-tuh KAIR-tsen.", "Suddenly someone rang the doorbell — the neighbour had candles.")],
        WS("Story worksheet", [
            T("Order the story.", ["then the rain came", "at first it was quiet", "in the end we laughed"],
              ["dann kam der Regen", "zuerst war es ruhig", "zum Schluss haben wir gelacht"]),
            T("Open with an adverb.", ["suddenly someone knocked", "all at once it rang"],
              ["Plötzlich hat jemand geklopft.", "Auf einmal hat es geklingelt."]),
        ]))),
    ("B1-U2", "B1-U2-L3", L(
        "Applying: Bewerbung, Lebenslauf, interview",
        "An application is a genre with fixed words: DIE STELLE, DIE BEWERBUNG, DER LEBENSLAUF, "
        "DAS VORSTELLUNGSGESPRÄCH. In the interview the polite register holds: WARUM HABEN SIE "
        "SICH BEI UNS BEWORBEN?",
        [V("die Stelle", "dee SHTEL-luh", "position, job", "noun"),
         V("sich bewerben", "zikh beh-VAIR-ben", "to apply", "verb"),
         V("der Lebenslauf", "dair LAY-bens-lowf", "CV", "noun"),
         V("die Erfahrung", "dee air-FAH-roong", "experience", "noun"),
         V("die Stärke", "dee SHTAIR-kuh", "strength (of a person)", "noun")],
        G("Application talk",
          "ich habe mich bei … beworben · ich bringe … mit · meine Stärke ist …",
          "Ich habe mich bei Ihrer Firma beworben, weil ich Erfahrung im Kundendienst mitbringe. "
          "Meine Stärke ist, dass ich ruhig bleibe. sich bewerben is reflexive: the mich travels "
          "with it.",
          [X("Ich habe mich bei Ihrer Firma beworben.", "ikh HAH-buh mikh by EER-er FEER-mah beh-VAIR-ben.", "I applied at your company."),
           X("Ich bringe drei Jahre Erfahrung mit.", "ikh BRIN-guh dry YAH-ruh air-FAH-roong mit.", "I bring three years of experience."),
           X("Meine Stärke ist, dass ich ruhig bleibe.", "MY-nuh SHTAIR-kuh ist, das ikh ROO-ikh BLY-buh.", "My strength is that I stay calm.")],
          [("Ich habe beworben bei Ihnen.", "Ich habe mich bei Ihnen beworben.", "bewerben needs the reflexive pronoun."),
           ("Ich bin Erfahrung in Verkauf.", "Ich habe Erfahrung im Verkauf.", "Experience is had, and the field takes im.")]),
        [D("Frau Wolf", "Guten Tag. Warum haben Sie sich bei uns beworben?", "GOO-ten tahk. var-OOM HAH-ben zee zikh by oons beh-VAIR-ben?", "Good day. Why did you apply to us?"),
         D("Max", "Ich habe mich beworben, weil ich Erfahrung im Verkauf mitbringe.", "ikh HAH-buh mikh beh-VAIR-ben, vile ikh air-FAH-roong im fair-KOWF MIT-brin-guh.", "I applied because I bring sales experience."),
         D("Frau Wolf", "Und was ist Ihre Stärke?", "unt vas ist EE-ruh SHTAIR-kuh?", "And what is your strength?"),
         D("Max", "Ich bleibe ruhig, auch wenn es schnell geht.", "ikh BLY-buh ROO-ikh, owkh ven es shnel gayt.", "I stay calm even when things move fast.")],
        WS("Application worksheet", [
            T("Say it in German.", ["I applied at your company", "three years of experience", "my strength"],
              ["Ich habe mich bei Ihrer Firma beworben.", "drei Jahre Erfahrung", "meine Stärke"]),
            T("Answer the question.", ["Why this company?", "What do you bring?"],
              ["Weil mich die Aufgabe interessiert.", "Ich bringe Erfahrung mit."]),
        ]))),
    ("B1-U3", "B1-U3-L3", L(
        "Arrangements: Termine, verschieben, sich treffen",
        "Fixing a time uses sich treffen and passen: WANN TREFFEN WIR UNS? — MIR PASST ES AM "
        "DONNERSTAG. Moving it uses verschieben; cancelling, absagen.",
        [V("sich treffen", "zikh TREF-fen", "to meet", "verb"),
         V("der Termin", "dair ter-MEEN", "appointment, slot", "noun"),
         V("verschieben", "fair-SHEE-ben", "to postpone", "verb"),
         V("passen", "PAS-sen", "to suit", "verb"),
         V("absagen", "AP-zah-gen", "to cancel", "verb")],
        G("Making and moving an appointment",
          "wann treffen wir uns? · mir passt es am … · können wir … verschieben?",
          "Mir passt es am Dienstag um vier. Können wir den Termin auf Freitag verschieben? "
          "Mir passt … is the natural form; «ich passe» means something else entirely (a person "
          "fits a role).",
          [X("Wann treffen wir uns?", "van TREF-fen veer oons?", "When shall we meet?"),
           X("Mir passt es am Dienstag.", "meer PASST es am DEENS-tahk.", "Tuesday suits me."),
           X("Können wir den Termin verschieben?", "KUR-nen veer dayn ter-MEEN fair-SHEE-ben?", "Can we postpone the appointment?")],
          [("Ich passe am Montag.", "Mir passt es am Montag.", "The dative mir is the person the time suits."),
           ("Wir treffen am Montag.", "Wir treffen uns am Montag.", "sich treffen needs uns / uns.")]),
        [D("Lena", "Wann treffen wir uns?", "van TREF-fen veer oons?", "When shall we meet?"),
         D("Max", "Mir passt es am Donnerstag um sechs.", "meer PASST es am DON-ners-tahk oom zeks.", "Thursday at six suits me."),
         D("Lena", "Donnerstag ist schwierig — können wir verschieben?", "DON-ners-tahk ist SHVEE-rikh — KUR-nen veer fair-SHEE-ben?", "Thursday is difficult — can we postpone?"),
         D("Max", "Klar. Dann Freitag, gleiche Zeit?", "klar. dan FRY-tahk, GLY-khuh tsite?", "Sure. Friday then, same time?")],
        WS("Arrangement worksheet", [
            T("Fix the time.", ["when do we meet?", "Thursday suits me", "same time?"],
              ["Wann treffen wir uns?", "Mir passt es am Donnerstag.", "Gleiche Zeit?"]),
            T("Move or cancel it.", ["can we postpone it?", "I must cancel"],
              ["Können wir den Termin verschieben?", "Ich muss leider absagen."]),
        ]))),
]

THIRD["B2"] = [
    ("B2-U1", "B2-U1-L3", L(
        "Conceding and rebutting: zwar … aber, einerseits … andererseits",
        "The German rebuttal gives ground in a marked first clause: ZWAR IST DIE REGEL KLAR, ABER "
        "DER AUFWAND IST HOCH. The concession is a grammatical slot, not an apology.",
        [V("zwar", "tsvar", "admittedly (opens the concession)", "adverb"),
         V("aber", "AH-ber", "but", "conjunction"),
         V("einerseits", "EYE-ner-zites", "on the one hand", "adverb"),
         V("andererseits", "AN-der-er-zites", "on the other hand", "adverb"),
         V("der Einwand", "dair INE-vant", "objection", "noun")],
        G("Two-part concession",
          "zwar … aber · einerseits … andererseits",
          "Zwar ist die Regel klar, aber der Aufwand ist hoch — verb after zwar, verb after aber. "
          "The pair holds the sentence together; dropping aber after zwar leaves the listener "
          "waiting.",
          [X("Zwar ist die Regel klar, aber der Aufwand ist hoch.", "tsvar ist dee RAY-gel klar, AH-ber dair OWF-vant ist hokh.", "Admittedly the rule is clear, but the effort is high."),
           X("Einerseits spart es Zeit, andererseits kostet es Personal.", "EYE-ner-zites shpart es tsite, AN-der-er-zites KOS-tet es pair-zo-NAHL.", "On the one hand it saves time; on the other it costs staff."),
           X("Ich verstehe den Einwand, sehe aber ein Risiko.", "ikh fair-SHTAY-uh dayn INE-vant, ZAY-uh AH-ber ine ri-ZEE-ko.", "I understand the objection but see a risk.")],
          [("Zwar ist die Regel klar, der Aufwand ist hoch.", "Zwar ist die Regel klar, aber der Aufwand ist hoch.", "zwar requires aber in the second clause."),
           ("Einerseits spart es Zeit, andererseits kostet Personal.", "…, andererseits kostet es Personal.", "The second clause needs its own subject.")]),
        [D("Frau Berger", "Was halten Sie von der Regel?", "vas HAL-ten zee fon dair RAY-gel?", "What do you think of the rule?"),
         D("Herr Wolf", "Zwar ist die Regel klar, aber der Aufwand ist hoch.", "tsvar ist dee RAY-gel klar, AH-ber dair OWF-vant ist hokh.", "Admittedly the rule is clear, but the effort is high."),
         D("Frau Berger", "Und Ihr Vorschlag?", "unt eer FOR-shlahk?", "And your proposal?"),
         D("Herr Wolf", "Einerseits testen, andererseits dokumentieren.", "EYE-ner-zites TES-ten, AN-der-er-zites do-koo-men-TEE-ren.", "On the one hand test it; on the other document it.")],
        WS("Rebuttal worksheet", [
            T("Build the concession.", ["the rule is clear (but the effort is high)", "it saves time (but costs staff)"],
              ["Zwar ist die Regel klar, aber der Aufwand ist hoch.", "Zwar spart es Zeit, aber es kostet Personal."]),
            T("Use the pair.", ["one hand saves money / other costs time"],
              ["Einerseits spart es Geld, andererseits kostet es Zeit."]),
        ]))),
    ("B2-U2", "B2-U2-L3", L(
        "The formal email: Betreff, Anrede, Grußformel",
        "A German business email is short and framed: BETREFF with the subject and no verb, "
        "ANREDE with SEHR GEEHRTE FRAU / GUTEN TAG HERR, body, and «Mit freundlichen Grüßen».",
        [V("der Betreff", "dair beh-TREF", "subject line", "noun"),
         V("die Anrede", "dee AN-ray-duh", "salutation", "noun"),
         V("die Grußformel", "dee GROOS-for-mel", "closing formula", "noun"),
         V("beiliegend", "BY-lee-gent", "attached, enclosed", "adjective"),
         V("um Rückmeldung bitten", "oom REWK-mel-doong BIT-ten", "to ask for a reply", "phrase")],
        G("Email frame",
          "Betreff: … · Sehr geehrte Frau …, · Mit freundlichen Grüßen",
          "Betreff: Termin am 12. Mai. Sehr geehrte Frau Berger, anbei die Unterlagen. Ich bitte "
          "um Rückmeldung bis Freitag. Mit freundlichen Grüßen. The exclamation mark after a "
          "salutation («Guten Tag Herr Wolf!») marks a private email; business keeps the comma.",
          [X("Betreff: Unterlagen für den Termin", "beh-TREF: OON-ter-lah-gen fewr dayn ter-MEEN", "Subject: documents for the appointment"),
           X("Sehr geehrte Frau Berger,", "zair ge-AIR-tuh frow BAIR-ger", "Dear Ms Berger,"),
           X("Mit freundlichen Grüßen", "mit FROYNT-li-khen GREW-sen", "Kind regards")],
          [("Hallo Frau Berger!", "Sehr geehrte Frau Berger,", "A business first contact takes the formal address and a comma."),
           ("Ich bitte um Rückmeldung bis Freitag!", "Ich bitte um Rückmeldung bis Freitag.", "Business bodies end with a full stop, not an exclamation mark.")]),
        [D("Herr Wolf", "Haben Sie die Mail geschrieben?", "HAH-ben zee dee mail ge-SHREE-ben?", "Have you written the email?"),
         D("Lena", "Ja. Betreff: Termin am 12. Mai.", "yah. beh-TREF: ter-MEEN am TSVURLF-ten my.", "Yes. Subject: appointment on 12 May."),
         D("Herr Wolf", "Und die Anrede?", "unt dee AN-ray-duh?", "And the salutation?"),
         D("Lena", "«Sehr geehrte Frau Berger,» — und zum Schluss «Mit freundlichen Grüßen».", "zair ge-AIR-tuh frow BAIR-ger — unt tsoom shloos mit FROYNT-li-khen GREW-sen.", "'Dear Ms Berger,' — and at the end 'Kind regards'.")],
        WS("Email worksheet", [
            T("Frame the email.", ["subject: deadline 12 May", "salutation to Ms Berger", "closing"],
              ["Betreff: Frist am 12. Mai", "Sehr geehrte Frau Berger,", "Mit freundlichen Grüßen"]),
            T("Write the body line.", ["ask for a reply by Friday", "the documents are attached"],
              ["Ich bitte um Rückmeldung bis Freitag.", "Die Unterlagen sind beiliegend."]),
        ]))),
    ("B2-U3", "B2-U3-L3", L(
        "Reading the news: headline, source, claim",
        "A German news item answers three questions fast: WHO says it (LAUT …, … ZUFOLGE), what is "
        "claimed, and what is still open. Headlines drop the verb: «Bahn streikt ab Montag».",
        [V("laut", "lowt", "according to", "preposition"),
         V("zufolge", "tsoo-FOL-guh", "according to (postposed)", "postposition"),
         V("die Quelle", "dee KVEL-luh", "source", "noun"),
         V("die Schlagzeile", "dee SHLAHK-tsy-luh", "headline", "noun"),
         V("unbestätigt", "OON-beh-shtay-tikht", "unconfirmed", "adjective")],
        G("Attribution",
          "laut + dative (laut Bericht) · noun + zufolge · das ist unbestätigt",
          "Laut Bericht steigen die Preise. Dem Bericht zufolge steigen die Preise. The frame is "
          "the honest part of the sentence: it says who is speaking, and the claim stays with them.",
          [X("Laut Bericht steigen die Preise.", "lowt beh-REEKHT SHTY-gen dee PRY-zuh.", "According to the report, prices are rising."),
           X("Dem Ministerium zufolge ist die Zahl unbestätigt.", "daym mi-nis-TAY-ree-oom tsoo-FOL-guh ist dee tsahl OON-beh-shtay-tikht.", "According to the ministry, the figure is unconfirmed."),
           X("Die Schlagzeile nennt keine Quelle.", "dee SHLAHK-tsy-luh NENT KY-nuh KVEL-luh.", "The headline names no source.")],
          [("Laut Bericht ist es sicher.", "Laut Bericht ist es wahrscheinlich.", "A reported claim stays a claim until the source's own certainty is quoted."),
           ("Dem Bericht laut steigen die Preise.", "Dem Bericht zufolge steigen die Preise.", "zufolge follows its noun; laut precedes.")]),
        [D("Lena", "Was steht in der Schlagzeile?", "vas shtayt in dair SHLAHK-tsy-luh?", "What does the headline say?"),
         D("Max", "«Bahn streikt ab Montag» — laut Gewerkschaft.", "bahn shtrykt ap MON-tahk — lowt ge-VAIRK-shaft.", "'Railway to strike from Monday' — according to the union."),
         D("Lena", "Und die Quelle?", "unt dee KVEL-luh?", "And the source?"),
         D("Max", "Nur die Gewerkschaft. Vom Unternehmen gibt es noch keine Aussage.", "noor dee ge-VAIRK-shaft. fom OON-ter-nay-men geept es nokh KY-nuh OWS-zah-guh.", "Only the union. The company has made no statement yet.")],
        WS("News worksheet", [
            T("Attribute the claim.", ["according to the report", "according to the ministry"],
              ["laut Bericht", "dem Ministerium zufolge"]),
            T("Separate the states.", ["it is claimed", "it is unconfirmed"],
              ["es wird berichtet", "es ist unbestätigt"]),
        ]))),
]

THIRD["C1"] = [
    ("de-c1-u1", "de-c1-l7", L(
        "Unnamed sources: Konjunktiv I and «soll»",
        "German keeps a claim at arm's length with Konjunktiv I: ER SEI KRANK (he is said to be "
        "ill), SIE HABE ABGELEHNT. Without a Konjunktiv I form the language falls back on soll: ER "
        "SOLL KRANK SEIN — the same distance, one word.",
        [V("Konjunktiv I", "KON-yoonk-tif ine", "reported-speech mood", "noun"),
         V("er sei", "air zy", "he is (reported)", "verb"),
         V("sie habe", "zee HAH-buh", "she has (reported)", "verb"),
         V("er solle", "air ZOL-luh", "he is said to (be to)", "verb"),
         V("die Wiedergabe", "dee VEE-der-gah-buh", "reproduction, reporting", "noun")],
        G("Evidential distance",
          "er sei · sie habe · er solle · laut Angaben",
          "Der Minister sagte, die Lage sei ruhig. Er solle nächste Woche zurücktreten, heißt es. "
          "The form marks that the speaker is not vouching — dropping it turns the sentence into "
          "assertion.",
          [X("Er sei krank, heißt es.", "air zy krank, HYST es.", "He is said to be ill."),
           X("Sie habe den Antrag abgelehnt.", "zee HAH-buh dayn AN-trahk AP-ge-laynt.", "She is said to have rejected the application."),
           X("Der Minister solle zurücktreten.", "dair mi-NIS-ter ZOL-luh tsoo-REWK-tray-ten.", "The minister is reportedly to step down.")],
          [("Er ist krank, heißt es.", "Er sei krank, heißt es.", "«heißt es» expects Konjunktiv I; with «ist» the sentence asserts what it disclaims."),
           ("Sie hat abgelehnt laut Quelle.", "Sie habe laut Quelle abgelehnt.", "The distancing sits in the verb, not in a trailing tag.")]),
        [D("Redakteurin", "Woher wissen wir das?", "voh-HAIR VIS-sen veer das?", "How do we know that?"),
         D("Reporter", "Zwei Quellen sagen, der Minister sei zurückgetreten.", "tsvy KVEL-len ZAH-gen, dair mi-NIS-ter zy tsoo-REWK-ge-tray-ten.", "Two sources say the minister has stepped down."),
         D("Redakteurin", "Bestätigt?", "beh-SHTAY-tikht?", "Confirmed?"),
         D("Reporter", "Nein — offiziell heißt es nur, er solle nächste Woche sprechen.", "nine — o-fi-TSYEL HYST es noor, air ZOL-luh NAYS-tuh VOKHuh SHPREH-khen.", "No — officially it is only said that he is to speak next week.")],
        WS("Evidential worksheet", [
            T("Put it at arm's length.", ["he is ill (reported)", "she has resigned (reported)", "they are said to travel"],
              ["Er sei krank.", "Sie habe gekündigt.", "Sie sollen reisen."]),
            T("Say what the source is.", ["two sources say", "officially it is said"],
              ["Zwei Quellen sagen", "offiziell heißt es"]),
        ]))),
    ("de-c1-u2", "de-c1-l8", L(
        "Graded causality: trägt bei, dürfte, spricht dafür",
        "Careful German causal prose grades the link: X TRÄGT ZU Y BEI (contributes), X DÜRFTE Y "
        "ERKLÄREN (may well explain), VIELES SPRICHT DAFÜR (much suggests). Each verb states how "
        "strong the link is.",
        [V("beitragen zu", "BY-trah-gen tsoo", "to contribute to", "verb"),
         V("dürfte", "DEWRF-tuh", "may well, is likely to", "verb"),
         V("sprechen für", "SHPREH-khen fewr", "to argue for, suggest", "phrase"),
         V("der Zusammenhang", "dair tsoo-ZAH-men-hank", "connection, correlation", "noun"),
         V("hinreichend", "HIN-ry-khent", "sufficient", "adjective")],
        G("Calibrated cause",
          "trägt bei zu · dürfte erklären · spricht dafür, dass · ist nicht hinreichend",
          "Die Nachfrage dürfte den Preisanstieg erklären, doch allein ist sie nicht "
          "hinreichend. The sentence holds a mechanism and its limit in one clause pair — the "
          "signature of German academic prose.",
          [X("Der Ausfall dürfte den Rückgang erklären.", "dair OWS-fal DEWRF-tuh dayn REWK-gang air-KLAY-ren.", "The outage may well explain the decline."),
           X("Vieles spricht dafür, dass sich der Markt erholt.", "FEE-les shprikht dah-FEWR, das zikh dair markt air-HOLT.", "Much suggests the market is recovering."),
           X("Das allein ist nicht hinreichend.", "das ah-LINE ist nikht HIN-ry-khent.", "That alone is not sufficient.")],
          [("Der Ausfall erklärt den Rückgang.", "Der Ausfall dürfte den Rückgang erklären.", "A correlation is not a cause: dürfte marks the inference."),
           ("Vieles spricht, dass es stimmt.", "Vieles spricht dafür, dass es stimmt.", "sprechen dafür is a fixed pair.")]),
        [D("Kollegin", "Warum steigen die Preise?", "var-OOM SHTY-gen dee PRY-zuh?", "Why are prices rising?"),
         D("Referent", "Die Nachfrage dürfte eine Rolle spielen.", "dee NAHKH-frah-guh DEWRF-tuh EYE-nuh ROL-luh SHPEE-len.", "Demand is likely to play a role."),
         D("Kollegin", "Und die Energiepreise?", "unt dee air-nair-GEE-pry-zuh?", "And energy prices?"),
         D("Referent", "Sie tragen dazu bei — hinreichend ist das aber nicht.", "zee TRAH-gen dah-tsoo by — HIN-ry-khent ist das AH-ber nikht.", "They contribute to it — but that is not sufficient.")],
        WS("Causality worksheet", [
            T("Grade the link.", ["may well explain", "contributes to", "much suggests"],
              ["dürfte erklären", "trägt dazu bei", "vieles spricht dafür"]),
            T("State the limit.", ["this alone is not enough", "correlation is not cause"],
              ["Das allein ist nicht hinreichend.", "Ein Zusammenhang ist keine Ursache."]),
        ]))),
    ("de-c1-u3", "de-c1-l9", L(
        "Synthesis: two sources, one paragraph",
        "Synthesis names the sources and then speaks with one voice: LAUT BUNDESAMT …, DER VERBAND "
        "NENNT DAGEGEN … — GEMEINSAM IST BEIDEN, DASS … The third sentence is the synthesis, and it "
        "is where the writing earns its place.",
        [V("laut", "lowt", "according to", "preposition"),
         V("dagegen", "dah-GAY-gen", "by contrast", "adverb"),
         V("gemeinsam", "ge-MYNE-zahm", "in common", "adjective"),
         V("das Amt", "das amt", "office, authority", "noun"),
         V("der Verband", "dair fair-PANT", "association, federation", "noun")],
        G("Source sandwich",
          "laut A … · B nennt dagegen … · gemeinsam ist beiden, dass …",
          "Laut Bundesamt ist die Zahl stabil. Der Verband nennt dagegen Risiken. Gemeinsam ist "
          "beiden, dass die Datenlage dünn ist. Three sentences, two positions, one honest "
          "conclusion.",
          [X("Laut Amt ist die Zahl stabil.", "lowt amt ist dee tsahl shta-BEEL.", "According to the authority the figure is stable."),
           X("Der Verband nennt dagegen ein Risiko.", "dair fair-PANT nent dah-GAY-gen ine ri-ZEE-ko.", "The association, by contrast, names a risk."),
           X("Gemeinsam ist beiden, dass die Daten dünn sind.", "ge-MYNE-zahm ist BY-den, das dee DAH-ten dewn zint.", "What both have in common is that the data is thin.")],
          [("Beide sagen dasselbe Gegenteil.", "Beide betonen Unterschiedliches.", "A synthesis states the difference and the shared ground; it cannot merge them."),
           ("Gemeinsam ist beiden die Daten.", "Gemeinsam ist beiden, dass die Daten dünn sind.", "The shared point is a clause, not a noun phrase.")]),
        [D("Chefin", "Wie ist die Lage bei den Zahlen?", "vee ist dee LAH-guh by daynTSAH-len?", "What is the picture on the figures?"),
         D("Referent", "Laut Bundesamt ist die Zahl stabil; der Verband nennt dagegen Risiken.", "lowt BOON-des-amt ist dee tsahl shta-BEEL; dair fair-PANT nent dah-GAY-gen ri-ZEE-ken.", "According to the federal office the figure is stable; the association, by contrast, names risks."),
         D("Chefin", "Und Ihr Fazit?", "unt eer fah-TSEET?", "And your conclusion?"),
         D("Referent", "Gemeinsam ist beiden, dass die Datenlage dünn ist.", "ge-MYNE-zahm ist BY-den, das dee DAH-ten-lah-guh dewn ist.", "What is common to both is that the data is thin.")],
        WS("Synthesis worksheet", [
            T("Line the sources up.", ["according to the office", "the association, by contrast"],
              ["laut Amt", "der Verband nennt dagegen"]),
            T("Write the synthesis.", ["what both have in common"],
              ["Gemeinsam ist beiden, dass …"]),
        ]))),
]

THIRD["C2"] = [
    ("de-c2-u1", "de-c2-l7", L(
        "Presupposition: what the sentence assumes",
        "A sentence smuggles in assumptions: WARUM HABEN SIE DAS VERBOT IGNORIERT? presupposes the "
        "ban and the ignoring. C2 names the presupposition instead of arguing inside it: DIESE "
        "FRAGE UNTERSTELLT, DASS …",
        [V("unterstellen", "OON-ter-shtel-len", "to impute, presuppose", "verb"),
         V("die Voraussetzung", "dee fohr-OWS-zeh-tsoong", "precondition", "noun"),
         V("die Implikatur", "dee im-plee-kah-TOOR", "implicature", "noun"),
         V("nahelegen", "NAH-huh-lay-gen", "to suggest, imply", "verb"),
         V("zurückweisen", "tsoo-REWK-vy-zen", "to reject", "verb")],
        G("Naming the presupposition",
          "die Frage unterstellt, dass … · das legt nahe, dass …",
          "Die Frage unterstellt, dass das Verbot bekannt war. Der Satz legt nahe, es habe einen "
          "Verstoß gegeben — das ist nicht belegt. Konjunktiv II (hätte, wäre) often marks the "
          "assumption as unverified.",
          [X("Die Frage unterstellt, dass alle davon wussten.", "dee FRAH-guh OON-ter-shtelt, das AL-luh dah-FON VOOS-ten.", "The question presupposes that everyone knew."),
           X("Der Satz legt nahe, es habe einen Verstoß gegeben.", "dair zats laykt NAH-huh, es HAH-buh EYE-nen fair-SHTOS ge-GAY-ben.", "The sentence implies that there was a breach."),
           X("Diese Voraussetzung weise ich zurück.", "DEE-zuh fohr-OWS-zeh-tsoong VY-zuh ikh tsoo-REWK.", "I reject that presupposition.")],
          [("Warum haben Sie das ignoriert?", "Warum sollten Sie das ignorieren? — or name the presupposition first.", "The question smuggles in the answer; in argument one must break the frame before answering."),
           ("Der Satz impliziert, dass es so war.", "Der Satz legt nahe, dass es so war.", "legen nahe states an implication without asserting it — implizieren claims a logical link that must then be defended.")]),
        [D("Interviewer", "Warum haben Sie die Regel ignoriert?", "var-OOM HAH-ben zee dee RAY-gel i-gno-REERT?", "Why did you ignore the rule?"),
         D("Sprecherin", "Diese Frage unterstellt, dass ich sie ignoriert habe.", "DEE-zuh FRAH-guh OON-ter-shtelt, das ikh zee i-gno-REERT HAH-buh.", "That question presupposes that I ignored it."),
         D("Interviewer", "Haben Sie denn nicht?", "HAH-ben zee den nikht?", "Didn't you?"),
         D("Sprecherin", "Der Vorgang ist ungeklärt. Bevor ich antworte, klären wir das.", "dair FOHR-gang ist OON-ge-klairt. beh-FOHR ikh ANT-vor-tuh, KLAY-ren veer das.", "The matter is unresolved. Before I answer, we settle that.")],
        WS("Presupposition worksheet", [
            T("Name what is assumed.", ["the question presupposes that everyone knew", "the sentence implies a breach"],
              ["Die Frage unterstellt, dass alle wussten.", "Der Satz legt nahe, dass es einen Verstoß gab."]),
            T("Break the frame.", ["reject the presupposition", "unresolved before answering"],
              ["Diese Voraussetzung weise ich zurück.", "Das ist nicht geklärt."]),
        ]))),
    ("de-c2-u2", "de-c2-l8", L(
        "Deliberate register break: Amtsdeutsch, Werbung, Motto",
        "A C2 text can fold in a register on purpose — a Verwaltungssatz quoted to be mocked, a "
        "slogan dropped into an essay. The effect is signalled by the surrounding sentence: «Es "
        "klingt wie Amtsdeutsch, wenn es heißt: …»",
        [V("das Amtsdeutsch", "das AMTS-doych", "officialese", "noun"),
         V("die Werbesprache", "dee VAIR-buh-shprah-khuh", "advertising language", "noun"),
         V("das Motto", "das MOT-toh", "motto, slogan", "noun"),
         V("zitieren", "tsi-TEE-ren", "to quote", "verb"),
         V("der Registerbruch", "dair re-GIS-ter-brookh", "register break", "noun")],
        G("Quoting a register, and marking it",
          "es klingt wie Amtsdeutsch, wenn es heißt: … · mit einem Motto gesagt: …",
          "Es klingt wie Amtsdeutsch, wenn es heißt: «Die Gewährung erfolgt nach Prüfung.» Mit "
          "einem Motto gesagt: «Erst prüfen, dann gewähren.» The frame keeps the borrowed register "
          "bounded and the irony legible.",
          [X("Es klingt wie Amtsdeutsch: «Die Gewährung erfolgt nach Prüfung.»", "es klingt vee AMTS-doych: dee ge-VAY-roong air-FOLKT nakh PREW-foong.", "It sounds like officialese: 'Granting follows review.'"),
           X("Mit einem Motto gesagt: erst prüfen, dann vertrauen.", "mit EYE-nem MOT-toh ge-ZAHKT: airst PREW-fen, dan fair-TROW-en.", "Put as a motto: first check, then trust."),
           X("Der Registerbruch ist Absicht, kein Fehler.", "dair re-GIS-ter-brookh ist AP-zikht, kine FAY-ler.", "The register break is intentional, not a mistake.")],
          [("Die Gewährung erfolgt nach Prüfung. (in an essay, unmarked)", "Es klingt wie Amtsdeutsch, wenn es heißt: «…»", "An unmarked quotation reads as the author's own register."),
           ("Motto: wir sind gut.", "Motto: «Erst prüfen, dann vertrauen.»", "A motto earns its place by compressing the argument, not by praising it.")]),
        [D("Autor", "Klingt dieser Satz gut?", "klingt DEE-zer zats goot?", "Does this sentence sound good?"),
         D("Lektorin", "Er klingt wie Amtsdeutsch: «Die Gewährung erfolgt nach Prüfung.»", "air klingt vee AMTS-doych: dee ge-VAY-roong air-FOLKT nakh PREW-foong.", "It sounds like officialese: 'Granting follows review.'"),
         D("Autor", "Also kürzen?", "AL-zo KEWR-tsen?", "So shorten it?"),
         D("Lektorin", "Oder bewusst zitieren — aber dann mit Rahmen.", "OH-der beh-VOOST tsi-TEE-ren — AH-ber dan mit RAH-men.", "Or quote it deliberately — but then with a frame.")],
        WS("Register worksheet", [
            T("Frame the borrowed register.", ["officialese", "advertising language"],
              ["Es klingt wie Amtsdeutsch: …", "Es klingt wie Werbesprache: …"]),
            T("Compress the argument into a motto.", ["check first, then trust"],
              ["Motto: «Erst prüfen, dann vertrauen.»"]),
        ]))),
    ("de-c2-u3", "de-c2-l9", L(
        "Calibrated forecasts: naming uncertainty in numbers",
        "Expert German states its own uncertainty with a scale: GESICHERT, WAHRSCHEINLICH, MÖGLICH, "
        "NICHT AUSZUSCHLIESSEN, UNWAHRSCHEINLICH — and with the time it applies to: KURZFRISTIG, "
        "BIS 2030. The forecast is only as good as the words around it.",
        [V("gesichert", "ge-ZEE-khert", "established, secure", "adjective"),
         V("wahrscheinlich", "var-SHYNE-likh", "probable", "adjective"),
         V("nicht auszuschließen", "nikht OWS-tsoo-sklee-sen", "cannot be ruled out", "phrase"),
         V("kurzfristig", "KOORTS-frish-tikh", "in the short term", "adverb"),
         V("die Prognose", "dee pro-GNO-zuh", "forecast", "noun")],
        G("Uncertainty scale",
          "gesichert > wahrscheinlich > möglich > nicht auszuschließen > unwahrscheinlich",
          "Kurzfristig ist ein Anstieg wahrscheinlich, langfristig möglich; ein Rückgang ist nicht "
          "auszuschließen. Stating the horizon and the band is what makes a forecast falsifiable "
          "instead of rhetorical.",
          [X("Kurzfristig ist ein Anstieg wahrscheinlich.", "KOORTS-frish-tikh ist ine AN-shtayk var-SHYNE-likh.", "In the short term a rise is probable."),
           X("Ein Rückgang ist nicht auszuschließen.", "ine REWK-gang ist nikht OWS-tsoo-sklee-sen.", "A decline cannot be ruled out."),
           X("Diese Prognose gilt bis 2030.", "DEE-zuh pro-GNO-zuh gilt bis TSVY-tow-zent-DRY-sikh.", "This forecast holds until 2030.")],
          [("Es wird steigen.", "Kurzfristig ist ein Anstieg wahrscheinlich.", "A bare future assertion hides both the horizon and the band."),
           ("Vielleicht möglich.", "Möglich, aber unwahrscheinlich.", "Two hedges in a row cancel; the scale needs one position.")]),
        [D("Chef", "Wie ist Ihre Prognose?", "vee ist EE-ruh pro-GNO-zuh?", "What is your forecast?"),
         D("Analystin", "Kurzfristig ist ein Anstieg wahrscheinlich.", "KOORTS-frish-tikh ist ine AN-shtayk var-SHYNE-likh.", "In the short term a rise is probable."),
         D("Chef", "Und langfristig?", "unt LANG-frish-tikh?", "And in the long term?"),
         D("Analystin", "Möglich. Ein Rückgang ist jedenfalls nicht auszuschließen.", "MURK-likh. ine REWK-gang ist YAY-den-fals nikht OWS-tsoo-sklee-sen.", "Possible. In any case a decline cannot be ruled out.")],
        WS("Forecast worksheet", [
            T("Place it on the scale.", ["probable in the short term", "cannot be ruled out", "held until 2030"],
              ["kurzfristig wahrscheinlich", "nicht auszuschließen", "gilt bis 2030"]),
            T("Name the horizon.", ["in the short term", "in the long term"],
              ["kurzfristig", "langfristig"]),
        ]))),
]

# ── the five half-step rungs ────────────────────────────────────────────────

HALFSTEPS["A1+"] = {
    "title": "German A1+ — Getting around",
    "native": NATIVE,
    "goals": [
        "Ask the way, buy a ticket and name a landmark",
        "Say a phone number, an address and a price out loud",
        "Name the days, tell the time and make a plan — or refuse one politely",
    ],
    "units": [
        {"id": "A1+-U1", "title": "In der Stadt", "lessons": [
            L("Rechts, links, geradeaus: asking the way",
              "Directions are imperative and short: GEHEN SIE GERADEAUS, DANN RECHTS. Add «bitte» "
              "and the request is polite: WO IST DER BAHNHOF, BITTE?",
              [V("geradeaus", "ge-RAH-duh-ows", "straight ahead", "adverb"),
               V("rechts", "rekhts", "right", "adverb"),
               V("links", "links", "left", "adverb"),
               V("die Ecke", "dee EK-kuh", "corner", "noun"),
               V("in der Nähe", "in dair NAY-uh", "nearby", "phrase")],
              G("Directions and location",
                "gehen Sie geradeaus · an der Ecke · in der Nähe",
                "Gehen Sie geradeaus, dann die zweite Straße links. Der Bahnhof ist an der Ecke, "
                "in der Nähe vom Markt. «in der Nähe von» names the landmark — the German "
                "equivalent of «near the …».",
                [X("Gehen Sie geradeaus, dann rechts.", "GAY-en zee ge-RAH-duh-ows, dan rekhts.", "Go straight ahead, then right."),
                 X("Der Bahnhof ist an der Ecke.", "dair BAHN-hof ist an dair EK-kuh.", "The station is on the corner."),
                 X("Ist der Markt in der Nähe?", "ist dair markt in dair NAY-uh?", "Is the market nearby?")],
                [("Gehen geradeaus.", "Gehen Sie geradeaus.", "The imperative needs the pronoun in the polite form."),
                 ("Der Bahnhof ist in der Ecke.", "Der Bahnhof ist an der Ecke.", "A building stands an der Ecke; something inside a room is in der Ecke.")]),
              [D("Max", "Entschuldigung, wo ist der Bahnhof, bitte?", "ent-SHOOL-di-goong, voh ist dair BAHN-hof, BIT-tuh?", "Excuse me, where is the station, please?"),
               D("Frau Wolf", "Gehen Sie geradeaus, dann die zweite Straße links.", "GAY-en zee ge-RAH-duh-ows, dan dee TSVY-tuh SHTRAH-suh links.", "Go straight ahead, then take the second street on the left."),
               D("Max", "Ist es weit?", "ist es vite?", "Is it far?"),
               D("Frau Wolf", "Nein, fünf Minuten zu Fuß, an der Ecke links.", "nine, fewnf mi-NOO-ten tsoo foos, an dair EK-kuh links.", "No, five minutes on foot, on the left corner.")],
              WS("Directions worksheet", [
                  T("Give the direction.", ["go straight ahead", "then left", "on the corner"],
                    ["Gehen Sie geradeaus.", "dann links", "an der Ecke"]),
                  T("Ask and answer.", ["Where is the market? (nearby)", "Is it far? (no, five minutes on foot)"],
                    ["Wo ist der Markt? — In der Nähe.", "Ist es weit? — Nein, fünf Minuten zu Fuß."]),
              ])),
            L("Tickets, fare and the rickshaw question",
              "Rides are bought with fixed lines: EINE FAHRKARTE NACH …, BITTE · WAS KOSTET ES? · "
              "HALTEN SIE BITTE HIER. Prices answer with the amount first and the currency after.",
              [V("kosten", "KOS-ten", "to cost", "verb"),
               V("halten", "HAL-ten", "to stop", "verb"),
               V("die Haltestelle", "dee HAL-tuh-shtel-luh", "stop (bus/tram)", "noun"),
               V("der Fahrer", "dair FAH-rer", "driver", "noun"),
               V("einfach", "INE-fakh", "single (ticket)", "adjective")],
              G("Fares and stops",
                "was kostet …? · eine Fahrkarte nach … · halten Sie hier, bitte",
                "Was kostet eine Fahrkarte nach Bonn? Sie kostet neun Euro. Halten Sie hier, "
                "bitte. The question about price takes was (thing), not wie viel — both are "
                "correct, but was kostet is the faster one.",
                [X("Was kostet die Fahrt zum Flughafen?", "vas KOS-tet dee fahrt tsoom FLOOK-hah-fen?", "What does the ride to the airport cost?"),
                 X("Eine Fahrkarte nach Bonn, bitte.", "EYE-nuh FAHR-kar-tuh nakh bon, BIT-tuh.", "A ticket to Bonn, please."),
                 X("Halten Sie hier, bitte.", "HAL-ten zee heer, BIT-tuh.", "Stop here, please.")],
                [("Was kostet das Ticket für Bonn?", "Was kostet eine Fahrkarte nach Bonn?", "nach + city, not für."),
                 ("Halten hier bitte.", "Halten Sie hier, bitte.", "Imperative with Sie needs the pronoun.")]),
              [D("Lena", "Was kostet eine Fahrkarte zum Hauptbahnhof?", "vas KOS-tet EYE-nuh FAHR-kar-tuh tsoom HOWPT-bahn-hof?", "What does a ticket to the main station cost?"),
               D("Fahrer", "Drei Euro zwanzig.", "dry OY-roh TSVAHN-tsikh.", "Three euros twenty."),
               D("Lena", "Einfach, bitte. Halten Sie an der Haltestelle?", "INE-fakh, BIT-tuh. HAL-ten zee an dair HAL-tuh-shtel-luh?", "Single, please. Do you stop at the stop?"),
               D("Fahrer", "Ja, gleich die nächste.", "yah, glike dee NAYS-tuh.", "Yes, the very next one.")],
              WS("Fare worksheet", [
                  T("Say it in German.", ["a ticket to Bonn", "what does it cost?", "stop here, please"],
                    ["eine Fahrkarte nach Bonn", "Was kostet das?", "Halten Sie hier, bitte."]),
                  T("Answer as the driver.", ["nine euros", "the next stop"],
                    ["neun Euro", "die nächste Haltestelle"]),
              ])),
            L("Landmarks: gegenüber, neben, hinter",
              "Two-place prepositions take the dative for position: NEBEN DEM MARKT, GEGENÜBER DER "
              "POST. gegenüber can stand before or after its noun.",
              [V("gegenüber", "GAY-gen-ew-ber", "opposite", "preposition"),
               V("neben", "NAY-ben", "next to", "preposition"),
               V("hinter", "HIN-ter", "behind", "preposition"),
               V("die Post", "dee post", "post office", "noun"),
               V("die Apotheke", "dee ah-po-TAY-kuh", "pharmacy", "noun")],
              G("Position with dative",
                "neben dem Markt · gegenüber der Post · hinter dem Bahnhof",
                "Die Apotheke ist neben dem Markt, gegenüber der Post. Dative forms: dem (m/n), "
                "der (f). Position answers «wo?»; direction would take the accusative.",
                [X("Die Apotheke ist neben dem Markt.", "dee ah-po-TAY-kuh ist NAY-ben daym markt.", "The pharmacy is next to the market."),
                 X("Die Bank ist gegenüber der Post.", "dee bank ist GAY-gen-ew-ber dair post.", "The bank is opposite the post office."),
                 X("Der Park liegt hinter dem Bahnhof.", "dair park leekt HIN-ter daym BAHN-hof.", "The park lies behind the station.")],
                [("Die Apotheke ist neben der Markt.", "Die Apotheke ist neben dem Markt.", "der Markt is masculine; the dative is dem."),
                 ("Gegenüber von der Post.", "Gegenüber der Post.", "gegenüber takes the dative directly, without von.")]),
              [D("Max", "Wo ist die Apotheke?", "voh ist dee ah-po-TAY-kuh?", "Where is the pharmacy?"),
               D("Lena", "Neben dem Markt, gegenüber der Post.", "NAY-ben daym markt, GAY-gen-ew-ber dair post.", "Next to the market, opposite the post office."),
               D("Max", "Und die Bank?", "unt dee bank?", "And the bank?"),
               D("Lena", "Die ist hinter dem Bahnhof — etwas weiter.", "dee ist HIN-ter daym BAHN-hof — ET-vas VY-ter.", "That one is behind the station — a bit further.")],
              WS("Landmark worksheet", [
                  T("Complete with the relation.", ["next to the market", "opposite the post office", "behind the station"],
                    ["neben dem Markt", "gegenüber der Post", "hinter dem Bahnhof"]),
                  T("Describe your street.", ["what is next to the pharmacy?", "what is opposite the bank?"],
                    ["Neben der Apotheke ist …", "Gegenüber der Bank ist …"]),
              ])),
        ]},
        {"id": "A1+-U2", "title": "Zahlen, die nach Hause bringen", "lessons": [
            L("From eleven to a hundred",
              "From 21 German counts backwards: EINUNDZWANZIG, ZWEIUNDDREISSIG — one-and-twenty, "
              "two-and-thirty. Learn the tens and the flip, and every price becomes audible.",
              [V("elf", "elf", "eleven", "numeral"),
               V("zwanzig", "TSVAHN-tsikh", "twenty", "numeral"),
               V("einundzwanzig", "INE-oont-tsvahn-tsikh", "twenty-one", "numeral"),
               V("hundert", "HOON-dert", "hundred", "numeral"),
               V("die Zahl", "dee tsahl", "number", "noun")],
              G("Numbers above twenty",
                "unit + und + ten: einundzwanzig (21) · zweiundfünfzig (52)",
                "21 = einundzwanzig, 52 = zweiundfünfzig, 100 = hundert. The unit comes first, "
                "the ten second — German says «one-and-twenty», and phone numbers are read in "
                "pairs: sieben-und-dreißig, neunzehn.",
                [X("Ich bin einundzwanzig Jahre alt.", "ikh bin INE-oont-tsvahn-tsikh YAH-ruh alt.", "I am twenty-one years old."),
                 X("Das kostet zweiundfünfzig Euro.", "das KOS-tet TSVY-oont-fewnf-tsikh OY-roh.", "That costs fifty-two euros."),
                 X("Meine Nummer ist sieben-und-dreißig.", "MY-nuh NUM-mer ist ZEEP-en-oont-DRY-sikh.", "My number is thirty-seven.")],
                [("Zwanzig-ein.", "einundzwanzig", "German flips the order: unit before ten."),
                 ("Einhundert und zwanzig.", "einhundertzwanzig", "Above a hundred the parts join into one word.")]),
              [D("Lena", "Wie alt ist dein Bruder?", "vee alt ist dine BROO-der?", "How old is your brother?"),
               D("Max", "Er ist einundzwanzig.", "air ist INE-oont-tsvahn-tsikh.", "He is twenty-one."),
               D("Lena", "Und deine Schwester?", "unt DY-nuh SHVES-ter?", "And your sister?"),
               D("Max", "Zweiunddreißig — sie hat heute Geburtstag.", "TSVY-oont-dry-sikh — zee hat HOY-tuh ge-BOORTS-tahk.", "Thirty-two — it's her birthday today.")],
              WS("Numbers worksheet", [
                  T("Write the number in German words.", ["21", "32", "52", "99"],
                    ["einundzwanzig", "zweiunddreißig", "zweiundfünfzig", "neunundneunzig"]),
                  T("Say the price in full.", ["ticket: €9.20", "two books: €120"],
                    ["neun Euro zwanzig", "einhundertzwanzig Euro"]),
              ])),
            L("Phone numbers and addresses",
              "Numbers are read in pairs and addresses run Straße, Hausnummer, Ort: WOLFGANGSTRASSE "
              "SIEBZEHN. Asking for details: WIE IST DEINE NUMMER? · KANNST DU DAS BUCHSTABIEREN?",
              [V("buchstabieren", "BOOKH-shtah-BEE-ren", "to spell", "verb"),
               V("die Straße", "dee SHTRAH-suh", "street", "noun"),
               V("die Hausnummer", "dee HOWS-noom-mer", "house number", "noun"),
               V("die Postleitzahl", "dee POST-lits-tsahl", "postcode", "noun"),
               V("die Nummer", "dee NOOM-mer", "number", "noun")],
              G("Address and phone frame",
                "Straße + Hausnummer · PLZ + Ort · wie ist deine Nummer?",
                "Ich wohne in der Gartenstraße siebzehn, Postleitzahl 50667. Kannst du das "
                "buchstabieren? The street takes «in der», the number follows without a "
                "preposition.",
                [X("Ich wohne in der Gartenstraße siebzehn.", "ikh VOH-nuh in dair GAR-ten-shtrah-suh ZEEP-tsen.", "I live at 17 Gartenstrasse."),
                 X("Wie ist deine Handynummer?", "vee ist DY-nuh HAN-dee-noom-mer?", "What is your mobile number?"),
                 X("Kannst du das buchstabieren?", "KANST doo das BOOKH-shtah-BEE-ren?", "Can you spell that?")],
                [("Ich wohne in Gartenstraße 17.", "Ich wohne in der Gartenstraße siebzehn.", "Street names take the article: in der Gartenstraße."),
                 ("Meine Nummer ist null-eins-sieben.", "…null, eins, sieben.", "Digits are read separately or in pairs, never as a single number.")]),
              [D("Max", "Wie ist deine Adresse?", "vee ist DY-nuh ah-DRES-suh?", "What is your address?"),
               D("Lena", "Gartenstraße siebzehn, 50667 Köln.", "GAR-ten-shtrah-suh ZEEP-tsen, fewnf-nool-zeks-zeks-zeeps.", "17 Gartenstrasse, 50667 Cologne."),
               D("Max", "Und deine Nummer?", "unt DY-nuh NOOM-mer?", "And your number?"),
               D("Lena", "Null-eins-sieben-drei, zwei-vier-null-acht.", "nool-ines-ZEEP-en-dry, TSVY-feer-nool-ahkht.", "Zero-one-seven-three, two-four-zero-eight.")],
              WS("Address worksheet", [
                  T("Say it in German.", ["my address", "house number seventeen", "can you spell that?"],
                    ["meine Adresse", "Hausnummer siebzehn", "Kannst du das buchstabieren?"]),
                  T("Ask for the details.", ["your phone number?", "your postcode?"],
                    ["Wie ist deine Nummer?", "Wie ist deine Postleitzahl?"]),
              ])),
            L("Prices: teuer, günstig, ein bisschen weniger",
              "Bargaining is rare in German shops but normal at the flea market: WAS LETZTEN "
              "PREIS? · KANNST DU ETWAS NACHGEBEN? · DAS IST ZU TEUER.",
              [V("teuer", "TOY-er", "expensive", "adjective"),
               V("günstig", "GEWN-stikh", "inexpensive, good value", "adjective"),
               V("nachgeben", "NAHKH-gah-ben", "to come down (in price)", "verb"),
               V("der Preis", "dair price", "price", "noun"),
               V("das Angebot", "das AN-ge-boht", "offer, special deal", "noun")],
              G("Price talk",
                "das ist zu teuer · kannst du etwas nachgeben? · was ist der letzte Preis?",
                "Das ist mir zu teuer — kannst du etwas nachgeben? Zwanzig Euro, dann nehme ich "
                "es. «mir zu teuer» puts the speaker in the dative, which is what makes the "
                "complaint about the object and not the seller.",
                [X("Das ist mir zu teuer.", "das ist meer tsoo TOY-er.", "That is too expensive for me."),
                 X("Kannst du etwas nachgeben?", "KANST doo ET-vas NAHKH-gah-ben?", "Can you come down a little?"),
                 X("Zwanzig Euro, dann nehme ich es.", "TSVAHN-tsikh OY-roh, dan NAY-muh ikh es.", "Twenty euros, then I'll take it.")],
                [("Ich bin zu teuer.", "Das ist mir zu teuer.", "The price is expensive, not the person."),
                 ("Gib mir Rabatt, ja?", "Kannst du etwas nachgeben?", "A direct demand sounds rude; the question keeps the market friendly.")]),
              [D("Lena", "Was soll die Lampe kosten?", "vas zol dee LAM-puh KOS-ten?", "What is the lamp supposed to cost?"),
               D("Verkäufer", "Dreißig Euro.", "DRY-sikh OY-roh.", "Thirty euros."),
               D("Lena", "Das ist mir zu teuer. Kannst du etwas nachgeben?", "das ist meer tsoo TOY-er. KANST doo ET-vas NAHKH-gah-ben?", "That's too expensive for me. Can you come down a bit?"),
               D("Verkäufer", "Fünfundzwanzig, dann ist es gut.", "FEWNF-oont-tsvahn-tsikh, dan ist es goot.", "Twenty-five, then it's a deal.")],
              WS("Price worksheet", [
                  T("Bargain politely.", ["that's too expensive for me", "can you come down?", "twenty-five, then it's a deal"],
                    ["Das ist mir zu teuer.", "Kannst du etwas nachgeben?", "Fünfundzwanzig, dann ist es gut."]),
                  T("Answer as the seller.", ["the price is thirty euros", "a special offer"],
                    ["Der Preis ist dreißig Euro.", "Das ist ein Angebot."]),
              ])),
        ]},
        {"id": "A1+-U3", "title": "Tage, Zeiten, Pläne", "lessons": [
            L("The week: Montag bis Sonntag",
              "Days are masculine and take am: AM MONTAG. «Von … bis» covers a range: VON MONTAG BIS "
              "FREITAG. Weekend is DAS WOCHENENDE.",
              [V("der Montag", "dair MOHN-tahk", "Monday", "noun"),
               V("der Freitag", "dair FRY-tahk", "Friday", "noun"),
               V("das Wochenende", "das VOKH-en-en-duh", "weekend", "noun"),
               V("die Woche", "dee VOKH-uh", "week", "noun"),
               V("von … bis", "fon … bis", "from … to", "phrase")],
              G("Days with am",
                "am Montag · von … bis … · am Wochenende",
                "Am Montag arbeite ich. Am Wochenende habe ich frei. Which day is today: WELCHER TAG "
                "IST HEUTE? — HEUTE IST DIENSTAG.",
                [X("Am Montag habe ich keine Zeit.", "am MOHN-tahk HAH-buh ikh KY-nuh tsite.", "On Monday I have no time."),
                 X("Von Montag bis Freitag arbeite ich.", "fon MOHN-tahk bis FRY-tahk AR-by-tuh ikh.", "From Monday to Friday I work."),
                 X("Am Wochenende bin ich zu Hause.", "am VOKH-en-en-duh bin ikh tsoo HOW-zuh.", "At the weekend I am at home.")],
                [("In Montag arbeite ich.", "Am Montag arbeite ich.", "Days take am (an + dem), not in."),
                 ("Von Montag zu Freitag.", "Von Montag bis Freitag.", "The range is von … bis.")]),
              [D("Lena", "Welcher Tag ist heute?", "VEL-kher tahk ist HOY-tuh?", "What day is today?"),
               D("Max", "Heute ist Donnerstag.", "HOY-tuh ist DON-ners-tahk.", "Today is Thursday."),
               D("Lena", "Und wann hast du Zeit?", "unt van hast doo tsite?", "And when do you have time?"),
               D("Max", "Von Freitag bis Sonntag habe ich frei.", "fon FRY-tahk bis ZON-tahk HAH-buh ikh fry.", "From Friday to Sunday I'm off.")],
              WS("Days worksheet", [
                  T("Answer in German.", ["what day is today? (Tuesday)", "when do you work? (Monday to Friday)", "the weekend"],
                    ["Heute ist Dienstag.", "Von Montag bis Freitag arbeite ich.", "am Wochenende"]),
                  T("Plan your week.", ["a working day", "a free day"],
                    ["Am … arbeite ich.", "Am … habe ich frei."]),
              ])),
            L("Telling the time: Viertel nach, halb, Viertel vor",
              "German counts to the next hour at the half: HALB DREI = 2:30. Quarter: VIERTEL NACH "
              "ZWEI (2:15), VIERTEL VOR DREI (2:45). Formal time is digital: 14:30 = VIERZEHN UHR "
              "DREISSIG.",
              [V("halb", "halp", "half (to the next hour)", "adjective"),
               V("das Viertel", "das FEER-tel", "quarter", "noun"),
               V("die Uhr", "dee oor", "o'clock, clock", "noun"),
               V("nach", "nahkh", "past", "preposition"),
               V("vor", "fohr", "to (before the hour)", "preposition")],
              G("Clock German",
                "halb drei = 2:30 · Viertel nach zwei = 2:15 · Viertel vor drei = 2:45",
                "Es ist halb drei. Der Zug fährt um Viertel nach sieben. Two systems live side by "
                "side: the spoken halb/viertel one and the timetable one (sieben Uhr fünfzehn).",
                [X("Es ist halb drei.", "es ist halp dry.", "It is half past two."),
                 X("Der Zug fährt um Viertel vor acht.", "dair tsook fairt oom FEER-tel fohr ahkht.", "The train leaves at a quarter to eight."),
                 X("Wir treffen uns um sieben Uhr.", "veer TREF-fen oons oom ZEEP-en oor.", "We meet at seven o'clock.")],
                [("Halb drei heißt 3:30.", "halb drei heißt 2:30.", "halb counts forward to the next hour: halb drei is half to three."),
                 ("Es ist drei und halb.", "Es ist halb drei.", "German puts halb first.")]),
              [D("Max", "Es ist schon halb fünf!", "es ist shohn halp fewnf!", "It is already half past four!"),
               D("Lena", "Wann treffen wir die anderen?", "van TREF-fen veer dee AN-de-ren?", "When do we meet the others?"),
               D("Max", "Um Viertel nach fünf, am Bahnhof.", "oom FEER-tel nahkh fewnf, am BAHN-hof.", "At a quarter past five, at the station."),
               D("Lena", "Gut, dann habe ich noch zehn Minuten.", "goot, dan HAH-buh ikh nokh tsehn mi-NOO-ten.", "Good, then I still have ten minutes.")],
              WS("Clock worksheet", [
                  T("Say the time in German.", ["2:30", "2:15", "7:45", "7:00"],
                    ["halb drei", "Viertel nach zwei", "Viertel vor acht", "sieben Uhr"]),
                  T("Answer the question.", ["When do we meet? (at 6:30)", "When does the train leave? (at 9:15)"],
                    ["Um halb sieben.", "Um Viertel nach neun."]),
              ])),
            L("Making a plan, refusing one kindly",
              "Plans open with WIR KÖNNTEN … or HAST DU LUST? Refusals come with a reason and an "
              "alternative: DAS PASST MIR LEIDER NICHT — ABER NÄCHSTE WOCHE GERNE.",
              [V("die Lust", "dee loost", "desire, inclination", "noun"),
               V("leider", "LY-der", "unfortunately", "adverb"),
               V("vielleicht", "fee-LIKHT", "maybe", "adverb"),
               V("nächste Woche", "NAYS-tuh VOKH-uh", "next week", "phrase"),
               V("sich freuen", "zikh FROY-en", "to be glad", "verb")],
              G("Invite, refuse, re-offer",
                "hast du Lust? · das passt mir leider nicht · aber nächste Woche gerne",
                "Hast du Lust auf einen Kaffee? — Heute passt es mir leider nicht, aber nächste "
                "Woche gerne. The refusal names the time, not the person, and offers another one in "
                "the same breath.",
                [X("Hast du Lust auf einen Kaffee?", "hast doo loost owf EYE-nen KAF-fee?", "Do you feel like a coffee?"),
                 X("Heute passt es mir leider nicht.", "HOY-tuh PASST es meer LY-der nikht.", "Today unfortunately doesn't suit me."),
                 X("Aber nächste Woche gerne!", "AH-ber NAYS-tuh VOKH-uh GAIR-nuh!", "But next week gladly!")],
                [("Ich habe keine Lust nicht.", "Ich habe keine Lust.", "One negation is enough."),
                 ("Das passt nicht mir.", "Das passt mir nicht.", "The dative pronoun comes before nicht.")]),
              [D("Max", "Hast du am Samstag Zeit?", "hast doo am ZAMS-tahk tsite?", "Do you have time on Saturday?"),
               D("Lena", "Samstag passt mir leider nicht — ich arbeite.", "ZAMS-tahk passt meer LY-der nikht — ikh AR-by-tuh.", "Saturday unfortunately doesn't suit me — I'm working."),
               D("Max", "Und Sonntag?", "unt ZON-tahk?", "And Sunday?"),
               D("Lena", "Sonntag gerne! Treffen wir uns um elf?", "ZON-tahk GAIR-nuh! TREF-fen veer oons oom elf?", "Sunday gladly! Shall we meet at eleven?")],
              WS("Plan worksheet", [
                  T("Make the plan.", ["feel like a coffee?", "meet at eleven", "next week"],
                    ["Lust auf einen Kaffee?", "Treffen wir uns um elf?", "nächste Woche"]),
                  T("Refuse and offer another day.", ["refuse Saturday, offer Sunday", "refuse today, offer next week"],
                    ["Samstag passt mir nicht — Sonntag gerne.", "Heute leider nicht — nächste Woche gerne."]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Getting around Germany means trusting the timetable: buses and trams run to the "
                 "minute, the platform is announced twice, and a missed connection is a real "
                 "problem because the next train may be an hour away. The vocabulary of the "
                 "half-step is therefore mostly nouns that appear on signs — Gleis, Anschluss, "
                 "Haltestelle, Umstieg — because reading the board is the skill that actually gets "
                 "a learner home."),
        source_url="https://en.wikipedia.org/wiki/Deutsche_Bahn",
        reading=("Am Samstag fahre ich nach Köln. Der Zug fährt um Viertel nach neun von Gleis "
                 "sieben. Die Fahrkarte kostet neunzehn Euro einfach. Ich muss in Düsseldorf "
                 "umsteigen, aber der Anschluss hat zwanzig Minuten Zeit. Am Bahnhof kaufe ich "
                 "einen Kaffee und schaue auf die Tafel: alles pünktlich."),
        reading_gloss=("On Saturday I'm going to Cologne. The train leaves at a quarter past nine "
                       "from platform seven. The ticket costs nineteen euros single. I have to "
                       "change in Düsseldorf, but the connection allows twenty minutes. At the "
                       "station I buy a coffee and look at the board: everything on time."),
        listening=("Lena: Wo ist Gleis sieben?<br>Max: Geradeaus, dann links, neben der Apotheke.<br>"
                   "Lena: Danke! Und wann fährt der Zug?<br>Max: Um Viertel nach neun — fünf Minuten."),
        listening_gloss=("Lena: Where is platform seven? Max: Straight ahead, then left, next to the "
                         "pharmacy. Lena: Thanks! And when does the train leave? Max: At a quarter "
                         "past nine — five minutes."),
        voice_tag=VOICE,
        idioms=[
            ("Zu Fuß gehen", "to go on foot", "to walk"),
            ("Um die Ecke", "around the corner", "just around the corner"),
            ("Gute Fahrt", "good journey", "have a good trip"),
            ("Letzter Aufruf", "last call", "final boarding call"),
            ("Hin und zurück", "there and back", "a return ticket"),
            ("Auf die Minute", "to the minute", "punctually"),
            ("Am Bahnhof", "at the station", "at the station"),
            ("Weit und breit", "far and wide", "far and wide, nowhere in sight"),
            ("Nach dem Weg fragen", "to ask for the way", "to ask for directions"),
            ("Sich verfahren", "to drive oneself wrong", "to take the wrong route"),
        ],
        mistakes=[
            ("Ich fahre mit dem Zug nach Köln morgen.", "Ich fahre morgen mit dem Zug nach Köln.", "Time expressions go in the middle field before the manner, not at the end."),
            ("Wir treffen uns in der Bahnhof.", "Wir treffen uns am Bahnhof.", "Public places take an + dem = am."),
            ("Halb drei heißt 3:30.", "Halb drei heißt 2:30.", "halb counts to the next hour."),
        ],
        task_title="Direct someone across your city",
        task_instructions=("Write six German steps from your home to a place you go often: two "
                           "landmarks (neben, gegenüber), one ticket or fare question, and one time "
                           "(halb/viertel). Give it to someone who must follow it without asking "
                           "you anything. Where they hesitate, the missing word is almost always a "
                           "two-way preposition — an der Ecke, neben dem Markt, gegenüber der Post."),
    ),
    "test": [
        ("translate_en", "Say: Where is the station, please?", "Wo ist der Bahnhof, bitte?"),
        ("translate_de", "Gehen Sie geradeaus, dann die zweite Straße links.", "Go straight ahead, then take the second street on the left."),
        ("multiple_choice", "Which is the polite request?", "Kannst du etwas nachgeben?"),
        ("fill_in_the_blank", "Was ___ eine Fahrkarte nach Bonn?", "kostet"),
        ("word_selection", "Select the German for twenty-one.", "einundzwanzig"),
        ("error_correction", "Die Apotheke ist neben der Markt.", "Die Apotheke ist neben dem Markt."),
        ("dialogue_completion", "Complete: Was kostet das? — ___ (nine euros)", "neun Euro"),
        ("matching", "Match gegenüber to its meaning.", "opposite"),
        ("reading_comprehension", "Der Zug fährt von Gleis sieben. Which platform?", "seven"),
        ("inference", "«Das ist mir zu teuer» — what is the speaker doing?", "bargaining politely"),
        ("main_idea", "Von Montag bis Freitag arbeite ich. What is this about?", "the working week"),
        ("detail_identification", "Es ist halb drei. What time is it?", "2:30"),
    ],
}

HALFSTEPS["A2+"] = {
    "title": "German A2+ — Holding a chat",
    "native": NATIVE,
    "goals": [
        "React, follow up and keep a conversation alive",
        "Tell a short story in order, with a scene and a turn",
        "Invite, accept, decline — in person and on the phone",
    ],
    "units": [
        {"id": "A2+-U1", "title": "Das Gespräch am Laufen halten", "lessons": [
            L("Reactions that mean something",
              "German feedback is short and often a single word: ECHT? WIRKLICH? TOLL! UND DANN? "
              "These hand the floor straight back to the speaker.",
              [V("echt?", "ekht?", "really?", "interrogative"),
               V("wirklich?", "VEERK-likh?", "truly?", "interrogative"),
               V("toll!", "tol!", "great!", "interjection"),
               V("schade", "SHAH-duh", "a pity", "adjective"),
               V("erzähl weiter", "air-TSAIL VY-ter", "keep telling me", "phrase")],
              G("React, then ask",
                "reaction + und + follow-up question",
                "Echt? Und dann? A reaction alone can close a turn; und + question keeps it open. "
                "«Schade» sympathises, «toll» celebrates — picking the wrong one is felt "
                "immediately.",
                [X("Wirklich? Das wusste ich nicht.", "VEERK-likh? das VOOS-tuh ikh nikht.", "Really? I did not know that."),
                 X("Toll! Ich möchte auch mitkommen.", "tol! ikh MURKH-tuh owkh MIT-kom-men.", "Great! I'd like to come too."),
                 X("Schade, dass es nicht geklappt hat.", "SHAH-duh, das es nikht ge-KLAPT hat.", "A pity it didn't work out.")],
                [("Echt? Ich wusste das nicht nicht.", "Echt? Ich wusste das nicht.", "One negation per clause."),
                 ("Schade! Und dann war alles gut.", "Schade! Wie ist es weitergegangen?", "A sympathising reaction and a cheerful question cancel each other out.")]),
              [D("Max", "Ich habe die Prüfung bestanden!", "ikh HAH-buh dee PREW-foong beh-SHTAN-den!", "I passed the exam!"),
               D("Lena", "Echt? Glückwunsch! Und wie war es?", "ekht? GLEWK-voonsh! unt vee vahr es?", "Really? Congratulations! And how was it?"),
               D("Max", "Schwer, aber machbar.", "shvair, AH-ber MAKH-bar.", "Hard, but doable."),
               D("Lena", "Toll! Erzähl weiter — was kam dran?", "tol! air-TSAIL VY-ter — vas kahm dran?", "Great! Keep going — what came up?")],
              WS("Reaction worksheet", [
                  T("React in German.", ["good news", "something unbelievable", "bad news"],
                    ["Toll! Glückwunsch!", "Echt? Wirklich?", "Schade."]),
                  T("React and follow up.", ["'I moved to Berlin'", "'I changed jobs'"],
                    ["Echt? Und wie gefällt es dir?", "Wirklich? Warum denn?"]),
              ])),
            L("Following up: und dann? warum? wie war es?",
              "Three questions carry a conversation: UND DANN? (next event), WARUM? (reason), WIE WAR "
              "ES? (evaluation). The third one asks for feeling, which is what turns a report into "
              "a chat.",
              [V("und dann?", "unt dan?", "and then?", "interrogative"),
               V("warum?", "var-OOM?", "why?", "interrogative"),
               V("wie war es?", "vee vahr es?", "how was it?", "phrase"),
               V("noch etwas?", "nokh ET-vas?", "anything else?", "phrase"),
               V("interessant", "in-te-re-SANT", "interesting", "adjective")],
              G("Follow-up ladder",
                "was ist passiert? → und dann? → wie war es?",
                "Each question goes one step deeper: the event, the next event, the evaluation. "
                "«erzähl weiter» is the shortest way to say «I am listening».",
                [X("Was ist dann passiert?", "vas ist dan pas-SEERT?", "What happened then?"),
                 X("Wie war es für dich?", "vee vahr es fewr dikh?", "How was it for you?"),
                 X("Noch etwas? Ich höre zu.", "nokh ET-vas? ikh HUR-uh tsoo.", "Anything else? I'm listening.")],
                [("Und? Warum? Wie? Noch?", "(one follow-up at a time)", "A chain of questions turns interest into an interrogation."),
                 ("Wie war es für dich dir?", "Wie war es für dich?", "One pronoun per slot.")]),
              [D("Lena", "Gestern war ich beim Bewerbungsgespräch.", "GES-tern vahr ikh bym beh-VAIR-boongs-ge-SHPREKH.", "Yesterday I had the job interview."),
               D("Max", "Und wie war es?", "unt vee vahr es?", "And how was it?"),
               D("Lena", "Zuerst war ich nervös, dann ging es besser.", "tsoo-AIRST vahr ikh nair-VURS, dan geeng es BES-ser.", "At first I was nervous, then it got better."),
               D("Max", "Interessant! Und dann — hast du ein Angebot?", "in-te-re-SANT! unt dan — hast doo ine AN-ge-boht?", "Interesting! And then — did you get an offer?")],
              WS("Follow-up worksheet", [
                  T("Ask the next question.", ["'I met the director'", "'I moved to a new city'"],
                    ["Und was hat er gesagt?", "Und wie gefällt dir die Stadt?"]),
                  T("Show interest.", ["(it was hard)", "(tell me more)"],
                    ["Interessant! Wie war es für dich?", "Erzähl weiter."]),
              ])),
            L("Praise in German: Das hast du gut gemacht",
              "Praise is concrete in German: DAS HAST DU GUT GEMACHT, TOLL GEMACHT, ICH FINDE DAS "
              "STARK. «Super!» alone is heard as filler; naming what was good makes it real.",
              [V("stark", "shtark", "strong, impressive", "adjective"),
               V("gut gemacht", "goot ge-MAKHT", "well done", "phrase"),
               V("der Glückwunsch", "dair GLEWK-voonsh", "congratulation", "noun"),
               V("ich finde", "ikh FIN-duh", "I find, I think", "phrase"),
               V("weiter so", "VY-ter zoh", "keep it up", "phrase")],
              G("Praise frames",
                "das hast du gut gemacht · ich finde das stark · weiter so",
                "Das hast du gut gemacht — besonders die Einleitung. The addition after the dash "
                "is what makes German praise audible: it names the part that was good.",
                [X("Das hast du gut gemacht.", "das hast doo goot ge-MAKHT.", "You did that well."),
                 X("Ich finde deinen Text stark.", "ikh FIN-duh DY-nen tekst shtark.", "I find your text strong."),
                 X("Weiter so!", "VY-ter zoh!", "Keep it up!")],
                [("Super, war aber nichts.", "Super — besonders der Schluss.", "Praise followed by a cancellation is worse than silence."),
                 ("Du bist ein gut.", "Das hast du gut gemacht.", "Praise names the deed, not a mangled adjective.")]),
              [D("Max", "Hier ist mein Bericht.", "heer ist mine beh-REEKHT.", "Here is my report."),
               D("Lena", "Das hast du gut gemacht — besonders die Übersicht.", "das hast doo goot ge-MAKHT — beh-ZON-ders dee EW-ber-zikht.", "You did that well — especially the overview."),
               D("Max", "Wirklich? Ich war unsicher.", "VEERK-likh? ikh vahr OON-zee-kher.", "Really? I was unsure."),
               D("Lena", "Wirklich stark. Weiter so!", "VEERK-likh shtark. VY-ter zoh!", "Really strong. Keep it up!")],
              WS("Praise worksheet", [
                  T("Praise warmly.", ["a report", "an exam result", "someone's cooking"],
                    ["Das hast du gut gemacht.", "Glückwunsch, stark!", "Das schmeckt wirklich gut."]),
                  T("Name what was good.", ["the overview", "the introduction"],
                    ["besonders die Übersicht", "besonders die Einleitung"]),
              ])),
        ]},
        {"id": "A2+-U2", "title": "Eine kurze Geschichte", "lessons": [
            L("In order: zuerst, dann, danach, zum Schluss",
              "Four connectors turn four sentences into a story: ZUERST, DANN, DANACH, ZUM SCHLUSS. "
              "German also uses «und plötzlich» to keep the beat.",
              [V("zuerst", "tsoo-AIRST", "at first", "adverb"),
               V("danach", "dah-NAHKH", "after that", "adverb"),
               V("zum Schluss", "tsoom shloos", "finally", "phrase"),
               V("danach ging es los", "dah-NAHKH geeng es lohs", "then it got going", "phrase"),
               V("die Reihenfolge", "dee RY-en-fol-guh", "order, sequence", "noun")],
              G("Story order",
                "zuerst … · dann … · danach … · zum Schluss …",
                "Zuerst haben wir gepackt, dann sind wir losgefahren, danach kam der Regen, zum "
                "Schluss haben wir gelacht. One connector per sentence; stacking them sounds like "
                "a school exercise.",
                [X("Zuerst habe ich nichts verstanden.", "tsoo-AIRST HAH-buh ikh nikhts fair-SHTAN-den.", "At first I understood nothing."),
                 X("Danach war alles klar.", "dah-NAHKH vahr AL-les klar.", "After that everything was clear."),
                 X("Zum Schluss haben wir gelacht.", "tsoom shloos HAH-ben veer ge-LAKHT.", "In the end we laughed.")],
                [("Zuerst, dann, danach, zum Schluss alles zusammen.", "(one connector per sentence)", "All four in one sentence is a list, not a story."),
                 ("Dann und dann und dann.", "(each connector brings a new event)", "Repeating one connector flattens the story.")]),
              [D("Lena", "Was ist gestern passiert?", "vas ist GES-tern pas-SEERT?", "What happened yesterday?"),
               D("Max", "Zuerst habe ich den Bus verpasst.", "tsoo-AIRST HAH-buh ikh dayn boos fair-PAST.", "First I missed the bus."),
               D("Lena", "Und dann?", "unt dan?", "And then?"),
               D("Max", "Danach bin ich gelaufen, zum Schluss war ich früher da als der Chef.", "dah-NAHKH bin ikh ge-LOW-fen, tsoom shloos vahr ikh FREW-er dah als dair shef.", "After that I walked, and in the end I was there earlier than the boss.")],
              WS("Order worksheet", [
                  T("Put the story in order.", ["we packed", "we set off", "it rained", "we laughed"],
                    ["Zuerst haben wir gepackt.", "dann sind wir losgefahren.", "danach kam der Regen.", "zum Schluss haben wir gelacht."]),
                  T("Tell your own morning.", ["first", "then", "finally"],
                    ["Zuerst …", "dann …", "zum Schluss …"]),
              ])),
            L("Scene and turn: es war … plötzlich",
              "A scene is set with the Präteritum (ES WAR, WIR SASSEN) and turned with PLÖTZLICH. "
              "The background sits in the first clause, the event steps out of the second.",
              [V("es war", "es vahr", "it was", "verb"),
               V("wir saßen", "veer ZAH-sen", "we were sitting", "verb"),
               V("plötzlich", "PLURTS-likh", "suddenly", "adverb"),
               V("auf einmal", "owf eye-NMAHL", "all at once", "phrase"),
               V("der Augenblick", "dair OW-gen-blik", "moment", "noun")],
              G("Scene then event",
                "präteritum scene + plötzlich + präteritum event",
                "Es war schon dunkel, wir saßen im Café; plötzlich ging das Licht aus. The "
                "background stays unfinished until the event hits it.",
                [X("Es war zehn Uhr, alle schliefen.", "es vahr tsehn oor, AL-luh SHLEE-fen.", "It was ten o'clock; everyone was asleep."),
                 X("Wir haben geredet, plötzlich klingelte das Telefon.", "veer HAH-ben ge-RAY-det, PLURTS-likh KLING-el-tuh das te-le-FOHN.", "We were talking; suddenly the phone rang."),
                 X("Auf einmal wurde es still.", "owf eye-NMAHL VOOR-duh es shtil.", "All at once it went quiet.")],
                [("Plötzlich das Licht.", "Plötzlich ging das Licht aus.", "plötzlich needs the event after it."),
                 ("Wir saßen und dann saßen wir.", "Wir saßen im Café, plötzlich ging das Licht aus.", "The scene runs until the turn; do not repeat it afterwards.")]),
              [D("Max", "Wie war der Abend?", "vee vahr dair AH-bent?", "How was the evening?"),
               D("Lena", "Es war ruhig, wir saßen draußen.", "es vahr ROO-ikh, veer ZAH-sen DROWS-sen.", "It was quiet; we were sitting outside."),
               D("Max", "Und dann?", "unt dan?", "And then?"),
               D("Lena", "Plötzlich kam ein Gewitter — wir mussten rennen.", "PLURTS-likh kahm ine ge-VIT-ter — veer MOOS-ten REN-nen.", "Suddenly a thunderstorm came — we had to run.")],
              WS("Scene worksheet", [
                  T("Set the scene.", ["it was raining", "we were waiting", "everyone was quiet"],
                    ["Es regnete.", "Wir warteten.", "Alle waren still."]),
                  T("Add the turn with plötzlich.", ["(someone knocked)", "(the train left)", "(the lights went out)"],
                    ["Plötzlich klopfte jemand.", "Plötzlich fuhr der Zug ab.", "Plötzlich ging das Licht aus."]),
              ])),
            L("The close: am Ende stellte sich heraus",
              "An anecdote closes with a finding: AM ENDE STELLTE SICH HERAUS, DASS … · ICH HABE "
              "GELERNT, DASS … · UND DAS WAR DAS BESTE.",
              [V("sich herausstellen", "zikh hair-OWS-shtel-len", "to turn out", "verb"),
               V("am Ende", "am EN-duh", "in the end", "phrase"),
               V("gelernt", "ge-LAIRNT", "learned", "verb"),
               V("eigentlich", "EY-gent-likh", "actually", "adverb"),
               V("das Beste", "das BES-tuh", "the best part", "phrase")],
              G("Closing moves",
                "am Ende stellte sich heraus, dass … · ich habe gelernt, dass …",
                "Am Ende stellte sich heraus, dass der Fehler bei mir lag. Ich habe gelernt, dass "
                "man vorher fragen sollte. German anecdotes end on a small admission more often "
                "than on a boast.",
                [X("Am Ende stellte sich heraus, dass ich zu spät war.", "am EN-duh SHTEL-tuh zikh hair-OWS, das ikh tsoo shpayt vahr.", "In the end it turned out I was late."),
                 X("Ich habe gelernt, dass man die Zeit prüfen muss.", "ikh HAH-buh ge-LAIRNT, das man dee tsite PREW-fen moos.", "I learned that one must check the time."),
                 X("Und das war eigentlich das Beste.", "unt das vahr EY-gent-likh das BES-tuh.", "And that was actually the best part.")],
                [("Am Ende stellte sich heraus, dass ich alles wusste.", "Am Ende stellte sich heraus, dass ich nichts wusste.", "A close that reveals nothing is not a close."),
                 ("Ich habe gelernt, dass ich gelernt habe.", "Ich habe gelernt, dass Planen Zeit spart.", "The lesson has to be a sentence with content.")]),
              [D("Lena", "Und dann?", "unt dan?", "And then?"),
               D("Max", "Am Ende stellte sich heraus, dass ich am falschen Bahnhof war.", "am EN-duh SHTEL-tuh zikh hair-OWS, das ikh am FAL-shen BAHN-hof vahr.", "In the end it turned out I was at the wrong station."),
               D("Lena", "Oh nein. Und?", "oh nine. unt?", "Oh no. And?"),
               D("Max", "Ich habe gelernt, dass man den Namen lesen soll, bevor man aussteigt.", "ikh HAH-buh ge-LAIRNT, das man dayn NAH-men LAY-zen zol, beh-FOHR man OWS-shtykt.", "I learned that you should read the name before getting off.")],
              WS("Ending worksheet", [
                  T("Close the story.", ["I was tired but it worked out", "I lost the key and found it"],
                    ["Am Ende stellte sich heraus, dass es geklappt hat.", "Am Ende fand ich den Schlüssel in der Jacke."]),
                  T("Turn it into a lesson.", ["check before you go", "time is worth watching"],
                    ["Ich habe gelernt, dass man vorher prüfen muss.", "Ich habe gelernt, dass Zeit wichtig ist."]),
              ])),
        ]},
        {"id": "A2+-U3", "title": "Einladungen und Telefon", "lessons": [
            L("Inviting: hast du Lust? komm vorbei",
              "Invitations are questions: HAST DU LUST AUF …? · KOMMST DU MIT? · WIR KÖNNTEN … "
              "Answering yes is GERNE! — one word that carries the whole acceptance.",
              [V("Lust haben", "loost HAH-ben", "to feel like", "phrase"),
               V("mitkommen", "MIT-kom-men", "to come along", "verb"),
               V("vorbeikommen", "FOHR-by-kom-men", "to drop by", "verb"),
               V("gerne", "GAIR-nuh", "gladly", "adverb"),
               V("die Einladung", "dee INE-lah-doong", "invitation", "noun")],
              G("Invitation frames",
                "hast du Lust auf …? · wir könnten … · kommst du mit?",
                "Wir könnten am Freitag grillen — hast du Lust? Kommst du mit ins Kino? The "
                "subjunctive könnten softens the plan into a suggestion.",
                [X("Hast du Lust auf einen Film?", "hast doo loost owf EYE-nen film?", "Do you feel like a film?"),
                 X("Wir könnten am Freitag grillen.", "veer KURN-ten am FRY-tahk GRIL-len.", "We could have a barbecue on Friday."),
                 X("Kommst du mit ins Kino?", "komst doo mit ins KEE-noh?", "Are you coming along to the cinema?")],
                [("Hast du Lust einen Film?", "Hast du Lust auf einen Film?", "Lust auf + accusative."),
                 ("Ich will du kommst.", "Kommst du mit?", "Invitations are questions, not embedded demands.")]),
              [D("Max", "Wir grillen am Samstag. Hast du Lust?", "veer GRIL-len am ZAMS-tahk. hast doo loost?", "We're having a barbecue on Saturday. Do you feel like it?"),
               D("Lena", "Gerne! Soll ich etwas mitbringen?", "GAIR-nuh! zol ikh ET-vas MIT-brin-gen?", "Gladly! Shall I bring something?"),
               D("Max", "Einen Salat, wenn du möchtest.", "EYE-nen zah-LAHT, ven doo MURKH-test.", "A salad, if you'd like."),
               D("Lena", "Mache ich. Bis Samstag!", "MAH-khuh ikh. bis ZAMS-tahk!", "I'll do that. See you Saturday!")],
              WS("Invitation worksheet", [
                  T("Invite in German.", ["a barbecue on Saturday", "a film", "come along?"],
                    ["Wir grillen am Samstag.", "Lust auf einen Film?", "Kommst du mit?"]),
                  T("Extend the invitation.", ["bring a salad", "come with your family"],
                    ["Bring einen Salat mit.", "Komm mit deiner Familie."]),
              ])),
            L("Accepting and declining",
              "Yes is GERNE or SEHR GERNE. No is TUT MIR LEID, DA KANN ICH NICHT — with a reason "
              "and usually an alternative, because German refusals keep the date open.",
              [V("es tut mir leid", "es toot meer lite", "I am sorry", "phrase"),
               V("leider", "LY-der", "unfortunately", "adverb"),
               V("der Termin", "dair ter-MEEN", "appointment", "noun"),
               V("nächstes Mal", "NAYS-tes mahl", "next time", "phrase"),
               V("absagen", "AP-zah-gen", "to cancel", "verb")],
              G("Accept / decline + keep the door open",
                "gerne! · tut mir leid, da kann ich nicht + reason · nächstes Mal",
                "Gerne, ich komme! Tut mir leid, am Samstag kann ich nicht — ich habe einen "
                "Termin. Nächstes Mal bestimmt. The third clause is what keeps the invitation "
                "alive.",
                [X("Gerne, ich komme!", "GAIR-nuh, ikh KOM-muh!", "Gladly, I'll come!"),
                 X("Tut mir leid, da kann ich nicht.", "toot meer lite, dah kan ikh nikht.", "I'm sorry, I can't then."),
                 X("Nächstes Mal bestimmt.", "NAYS-tes mahl beh-SHTIMT.", "Definitely next time.")],
                [("Nein.", "Tut mir leid, da kann ich nicht — nächstes Mal gerne.", "A bare no ends the invitation."),
                 ("Ich kann nicht können.", "Ich kann nicht.", "One modal per clause.")]),
              [D("Lena", "Kommst du am Samstag zum Grillen?", "komst doo am ZAMS-tahk tsoom GRIL-len?", "Are you coming to the barbecue on Saturday?"),
               D("Max", "Tut mir leid, da kann ich nicht — ich arbeite.", "toot meer lite, dah kan ikh nikht — ikh AR-by-tuh.", "I'm sorry, I can't then — I'm working."),
               D("Lena", "Schade. Und am Sonntag?", "SHAH-duh. unt am ZON-tahk?", "A pity. And on Sunday?"),
               D("Max", "Sonntag gerne! Nächstes Mal bin ich dabei.", "ZON-tahk GAIR-nuh! NAYS-tes mahl bin ikh dah-BY.", "Sunday gladly! Next time I'm in.")],
              WS("Answer worksheet", [
                  T("Accept and decline.", ["invitation to dinner (accept)", "invitation to travel (decline, reason)"],
                    ["Gerne, ich komme!", "Tut mir leid, da kann ich nicht — ich habe einen Termin."]),
                  T("Keep the door open.", ["decline and promise next time"],
                    ["Nächstes Mal bestimmt."]),
              ])),
            L("On the phone: Wer ist am Apparat?",
              "Phone German has its own openers: NAME, BITTE? · WER IST AM APPARAT? · KANN ICH "
              "ETWAS AUSRICHTEN? · BLEIBEN SIE DRAN.",
              [V("der Apparat", "dair ah-pah-RAHT", "device, phone", "noun"),
               V("dranbleiben", "DRAN-bly-ben", "to hold on", "verb"),
               V("ausrichten", "OWS-rikh-ten", "to pass on (a message)", "verb"),
               V("zurückrufen", "tsoo-REWK-roo-fen", "to call back", "verb"),
               V("die Nachricht", "dee NAHKH-rikht", "message", "noun")],
              G("Phone frames",
                "Name, bitte? · wer ist am Apparat? · bleiben Sie dran · kann ich etwas ausrichten?",
                "Firma Wolf, guten Tag. Wer ist am Apparat? Bleiben Sie dran, ich verbinde. If "
                "the line breaks: Die Verbindung war weg, ich rufe zurück.",
                [X("Guten Tag, hier ist Lena Berger.", "GOO-ten tahk, heer ist LAY-nuh BAIR-ger.", "Good day, this is Lena Berger."),
                 X("Bleiben Sie dran, bitte.", "BLY-ben zee dran, BIT-tuh.", "Hold on, please."),
                 X("Kann ich etwas ausrichten?", "kan ikh ET-vas OWS-rikh-ten?", "Can I pass on a message?")],
                [("Wer sind Sie am Telefon?", "Wer ist am Apparat?", "The fixed phrase asks about the device, not the person's identity."),
                 ("Ich rufe zurück dir.", "Ich rufe dich zurück.", "zurückrufen splits: rufen + dich + zurück.")]),
              [D("Max", "Guten Tag, hier ist Max.", "GOO-ten tahk, heer ist maks.", "Good day, this is Max."),
               D("Sekretärin", "Wer ist am Apparat?", "vair ist am ah-pah-RAHT?", "Who is speaking?"),
               D("Max", "Max Weber. Kann ich Frau Wolf sprechen?", "maks VAY-ber. kan ikh frow volf SHPREH-khen?", "Max Weber. Can I speak to Ms Wolf?"),
               D("Sekretärin", "Bleiben Sie dran, ich verbinde.", "BLY-ben zee dran, ikh fair-BIN-duh.", "Hold on, I'll connect you.")],
              WS("Phone worksheet", [
                  T("Open the call in German.", ["say who you are", "ask who is speaking", "ask them to hold"],
                    ["Hier ist …", "Wer ist am Apparat?", "Bleiben Sie dran, bitte."]),
                  T("Handle a bad line.", ["the line cut", "call back", "leave a message"],
                    ["Die Verbindung war weg.", "Ich rufe zurück.", "Kann ich etwas ausrichten?"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("German conversation is carried by short reactions and honest follow-up questions; "
                 "long enthusiastic monologues from a listener are read as performance. The "
                 "half-step therefore drills the small moves — echt?, und dann?, erzähl weiter — "
                 "because at A2+ the risk is not grammar but a learner who answers with full "
                 "sentences and never hands the floor back."),
        source_url="https://en.wikipedia.org/wiki/Small_talk",
        reading=("Am Freitag haben wir bei Max gegrillt. Zuerst war es kühl, dann kam die Sonne. "
                 "Lena hat einen Salat mitgebracht, ich habe die Getränke besorgt. Plötzlich hat es "
                 "geregnet, aber niemand wollte nach Hause. Am Ende stellte sich heraus, dass wir "
                 "bis Mitternacht draußen gesessen haben. Ich habe gelernt, dass ein guter Abend "
                 "keinen Plan braucht."),
        reading_gloss=("On Friday we had a barbecue at Max's. At first it was cool, then the sun "
                       "came out. Lena brought a salad; I got the drinks. Suddenly it rained, but "
                       "nobody wanted to go home. In the end it turned out we sat outside until "
                       "midnight. I learned that a good evening needs no plan."),
        listening=("Max: Hast du am Samstag Zeit?<br>Lena: Samstag passt leider nicht — ich arbeite.<br>"
                   "Max: Und Sonntag?<br>Lena: Sonntag gerne! Um elf?"),
        listening_gloss=("Max: Do you have time on Saturday? Lena: Saturday unfortunately doesn't "
                         "work — I'm working. Max: And Sunday? Lena: Sunday gladly! At eleven?"),
        voice_tag=VOICE,
        idioms=[
            ("Hast du Lust?", "do you have desire?", "do you feel like it?"),
            ("Erzähl weiter", "tell further", "keep telling me"),
            ("Weiter so", "further so", "keep it up"),
            ("Das war's", "that was it", "that's all"),
            ("Bis dann", "until then", "see you then"),
            ("Alles klar", "everything clear", "all right / understood"),
            ("Nächstes Mal", "next time", "next time"),
            ("Sich melden", "to announce oneself", "to get in touch"),
            ("Am Apparat", "on the device", "speaking (on the phone)"),
            ("Aus dem Nichts", "out of nothing", "out of nowhere"),
        ],
        mistakes=[
            ("Ich habe keine Lust nicht.", "Ich habe keine Lust.", "One negation is enough."),
            ("Wer sind Sie am Apparat?", "Wer ist am Apparat?", "The fixed telephone phrase uses the third person."),
            ("Plötzlich das Telefon.", "Plötzlich klingelte das Telefon.", "plötzlich needs the event after it."),
        ],
        task_title="Tell me a two-minute story",
        task_instructions=("Record yourself telling a real story in German for two minutes: zuerst "
                           "for the scene, a Präteritum clause for the background, plötzlich for the "
                           "turn, and a close with «am Ende stellte sich heraus, dass …». Then "
                           "listen back and count the reactions you never gave — every «echt?» "
                           "your listener needed is a place the story ran without them."),
    ),
    "test": [
        ("translate_en", "Say: Really? And how was it?", "Echt? Und wie war es?"),
        ("translate_de", "Am Ende stellte sich heraus, dass ich zu spät war.", "In the end it turned out I was late."),
        ("multiple_choice", "Which invitation is the softest?", "Wir könnten am Freitag grillen."),
        ("fill_in_the_blank", "Hast du ___ auf einen Film?", "Lust"),
        ("word_selection", "Select the German for 'keep it up'.", "Weiter so"),
        ("error_correction", "Plötzlich das Licht.", "Plötzlich ging das Licht aus."),
        ("dialogue_completion", "Complete: Tut mir leid, da kann ich nicht — ___ (next time for sure)", "nächstes Mal bestimmt"),
        ("matching", "Match «am Apparat» to its meaning.", "speaking (on the phone)"),
        ("reading_comprehension", "Zuerst war es kühl, dann kam die Sonne. What changed?", "the weather"),
        ("inference", "«Niemand wollte nach Hause» — what does it tell us?", "the evening was good despite the rain"),
        ("main_idea", "Wir haben bis Mitternacht draußen gesessen. What is this about?", "how long they stayed"),
        ("detail_identification", "Wann hat es geregnet? (plötzlich, beim Grillen)", "during the barbecue"),
    ],
}

HALFSTEPS["B1+"] = {
    "title": "German B1+ — Comfortable",
    "native": NATIVE,
    "goals": [
        "Say what you want, need and intend — with the right strength",
        "Give an opinion and disagree without losing the room",
        "Move between du, Sie and ihr, and know which one the situation asks for",
    ],
    "units": [
        {"id": "B1+-U1", "title": "Wollen, brauchen, vorhaben", "lessons": [
            L("Three strengths: möchten, wollen, brauchen",
              "MOCHTEN is the polite wish (ICH MÖCHTE EINEN KAFFEE), WOLLEN the decided intention "
              "(ICH WILL DAS LERNEN), BRAUCHEN the requirement (ICH BRAUCHE HILFE). Choosing the "
              "wrong one sounds either weak or blunt.",
              [V("möchten", "MURKH-ten", "would like", "verb"),
               V("wollen", "VOL-len", "to want (decidedly)", "verb"),
               V("brauchen", "BROW-khen", "to need", "verb"),
               V("die Absicht", "dee AP-zikht", "intention", "noun"),
               V("unbedingt", "OON-beh-dinkt", "absolutely, at all costs", "adverb")],
              G("Strength of want",
                "ich möchte … · ich will … · ich brauche …",
                "Ich möchte einen Termin. Ich will das Projekt noch dieses Jahr abschließen. Ich "
                "brauche zwei Tage mehr. möchten is a wish, wollen is a decision — «ich will» from "
                "a stranger can sound like a demand.",
                [X("Ich möchte einen Termin vereinbaren.", "ikh MURKH-tuh EYE-nen ter-MEEN fair-EYE-nuh-bah-ren.", "I would like to arrange an appointment."),
                 X("Ich brauche noch zwei Tage.", "ikh BROW-khuh nokh tsvy TAH-guh.", "I still need two days."),
                 X("Ich will das unbedingt schaffen.", "ikh vil das OON-beh-dinkt SHAF-fen.", "I absolutely want to manage it.")],
                [("Ich will einen Kaffee, bitte. (to a waiter)", "Ich möchte einen Kaffee, bitte.", "Ordering takes möchten; wollen sounds like a child."),
                 ("Ich brauche das nicht müssen.", "Ich muss das nicht.", "Modal verbs do not stack; use muss or brauche.")]),
              [D("Lena", "Was brauchst du für das Projekt?", "vas BROOKHST doo fewr das pro-YEKT?", "What do you need for the project?"),
               D("Max", "Ich brauche zwei Tage mehr und eine Kollegin.", "ikh BROW-khuh tsvy TAH-guh mair unt EYE-nuh kol-LAY-gin.", "I need two more days and a colleague."),
               D("Lena", "Und was möchtest du danach machen?", "unt vas MURKH-test doo dah-NAHKH MAH-khen?", "And what would you like to do afterwards?"),
               D("Max", "Ich will das Team behalten — wir arbeiten gut zusammen.", "ikh vil das teem beh-HAL-ten — veer AR-by-ten goot tsoo-ZAH-men.", "I want to keep the team — we work well together.")],
              WS("Wants worksheet", [
                  T("Choose the right strength.", ["I need help", "I would like a coffee", "I want to finish this year"],
                    ["Ich brauche Hilfe.", "Ich möchte einen Kaffee.", "Ich will dieses Jahr abschließen."]),
                  T("Ask a colleague.", ["what do you need?", "what would you like to do?", "is it urgent?"],
                    ["Was brauchst du?", "Was möchtest du machen?", "Ist es dringend?"]),
              ])),
            L("Intentions: ich habe vor, ich plane",
              "Intention is stated with HABEN VOR (plan), PLANEN and WERDEN: ICH HABE VOR, DIE "
              "PRÜFUNG ZU MACHEN. The infinitive goes to the end with zu.",
              [V("vorhaben", "FOHR-hah-ben", "to intend, to plan", "verb"),
               V("planen", "PLAH-nen", "to plan", "verb"),
               V("werden", "VAIR-den", "will (future)", "verb"),
               V("die Ausbildung", "dee OWS-bil-doong", "training, apprenticeship", "noun"),
               V("später", "SHPAY-ter", "later", "adverb")],
              G("Intention frames",
                "ich habe vor, … zu + infinitive · ich plane, … zu … · ich werde …",
                "Ich habe vor, nächstes Jahr die Prüfung zu machen. Ich werde im Sommer umziehen. "
                "With vorhaben the zu-infinitive is obligatory; with werden the bare infinitive "
                "sits at the end.",
                [X("Ich habe vor, im Herbst zu wechseln.", "ikh HAH-buh fohr, im haist TSEK-seln.", "I intend to change in the autumn."),
                 X("Ich werde mehr lernen.", "ikh VAIR-duh mair LAIR-nen.", "I will study more."),
                 X("Wir planen, im Sommer umzuziehen.", "veer PLAH-nen, im ZOM-mer OOM-tsoo-tsoo-en.", "We plan to move in the summer.")],
                [("Ich habe vor die Prüfung machen.", "Ich habe vor, die Prüfung zu machen.", "vorhaben needs zu + infinitive and a comma."),
                 ("Ich werde zu lernen.", "Ich werde lernen.", "werden takes the bare infinitive.")]),
              [D("Max", "Was hast du im Herbst vor?", "vas hast doo im haist fohr?", "What are your plans for the autumn?"),
               D("Lena", "Ich habe vor, die Prüfung zu machen.", "ikh HAH-buh fohr, dee PREW-foong tsoo MAH-khen.", "I intend to take the exam."),
               D("Max", "Und danach?", "unt dah-NAHKH?", "And after that?"),
               D("Lena", "Dann werde ich mich bei zwei Firmen bewerben.", "dan VAIR-duh ikh mikh by tsvy FEER-men beh-VAIR-ben.", "Then I'll apply to two companies.")],
              WS("Intention worksheet", [
                  T("State your intention.", ["take the exam", "change jobs", "move house"],
                    ["Ich habe vor, die Prüfung zu machen.", "Ich habe vor, die Stelle zu wechseln.", "Ich habe vor, umzuziehen."]),
                  T("Say it in the future.", ["more study", "an application"],
                    ["Ich werde mehr lernen.", "Ich werde mich bewerben."]),
              ])),
            L("Persuading without pushing",
              "Persuasion leans on shared gain: WENN WIR DAS GEMEINSAM MACHEN, … · WAS HÄLTST DU "
              "DAVON? · DENK EINMAL DARÜBER NACH. The question is the softest push.",
              [V("gemeinsam", "ge-MYNE-zahm", "together", "adjective"),
               V("vorschlagen", "FOHR-shlah-gen", "to suggest", "verb"),
               V("überlegen", "ew-ber-LAY-gen", "to consider", "verb"),
               V("der Vorteil", "dair FOHR-tyle", "advantage", "noun"),
               V("sich einigen", "zikh EYE-ni-gen", "to reach agreement", "verb")],
              G("Soft persuasion",
                "was hältst du davon? · wenn …, dann … · denk einmal darüber nach",
                "Was hältst du davon, wenn wir es zusammen machen? Wenn zwei es machen, spart es "
                "Zeit. The conditional lets the listener reach the conclusion; the question hands "
                "the decision over.",
                [X("Was hältst du davon, wenn wir es teilen?", "vas HELTST doo dah-FON, ven veer es TY-len?", "What do you think of sharing it?"),
                 X("Wenn wir zusammenarbeiten, sparen wir Zeit.", "ven veer tsoo-ZAH-men-ar-by-ten, SPAH-ren veer tsite.", "If we work together, we save time."),
                 X("Denk einmal darüber nach.", "denk EYE-nemahl dah-REW-ber nahkh.", "Think it over.")],
                [("Du musst das machen.", "Was hältst du davon?", "A bare müssen closes the conversation."),
                 ("Wenn du machst, ich helfe.", "Wenn du es machst, helfe ich.", "In the wenn-clause the verb goes to the end.")]),
              [D("Max", "Willst du den Kurs allein machen?", "vilst doo dayn koors ah-LINE MAH-khen?", "Do you want to do the course alone?"),
               D("Lena", "Was hältst du davon, wenn wir uns zusammentun?", "vas HELTST doo dah-FON, ven veer oons tsoo-ZAH-men-toon?", "What do you think of teaming up?"),
               D("Max", "Vielleicht. Warum?", "fee-LIKHT. var-OOM?", "Maybe. Why?"),
               D("Lena", "Wenn wir gemeinsam lernen, halten wir länger durch.", "ven veer ge-MYNE-zahm LAIR-nen, HAL-ten veer LAYN-ger doorkh.", "If we study together, we last longer.")],
              WS("Persuasion worksheet", [
                  T("Build the conditional.", ["we share → we save time", "you come → we finish today"],
                    ["Wenn wir es teilen, sparen wir Zeit.", "Wenn du kommst, sind wir heute fertig."]),
                  T("Soften the request.", ["do it (direct)", "think about it"],
                    ["Wie wäre es, wenn …?", "Denk einmal darüber nach."]),
              ])),
        ]},
        {"id": "B1+-U2", "title": "Meinungen und Widerspruch", "lessons": [
            L("Stating an opinion with a hedge",
              "Opinions come with a frame: ICH FINDE … · MEINER MEINUNG NACH … · ICH GLAUBE, DASS "
              "… · SOVIEL ICH WEISS … The frame tells the listener how much weight to give it.",
              [V("meiner Meinung nach", "MY-ner MY-noong nahkh", "in my opinion", "phrase"),
               V("ich glaube", "ikh GLOW-buh", "I believe", "phrase"),
               V("soviel ich weiß", "zoh-FEEL ikh vìce", "as far as I know", "phrase"),
               V("die Ansicht", "dee AN-zikht", "view", "noun"),
               V("begründen", "beh-GREWN-den", "to give reasons for", "verb")],
              G("Opinion frames",
                "ich finde, dass … · meiner Meinung nach … · soviel ich weiß …",
                "Ich finde, dass der Plan funktioniert. Meiner Meinung nach ist der Preis zu "
                "hoch. With «ich finde» a dass-clause is normal; «meiner Meinung nach» inverts — "
                "the phrase occupies position 1 and the verb follows.",
                [X("Ich finde, dass wir mehr Zeit brauchen.", "ikh FIN-duh, das veer mair tsite BROW-khen.", "I think we need more time."),
                 X("Meiner Meinung nach ist der Preis zu hoch.", "MY-ner MY-noong nahkh ist dair price tsoo hokh.", "In my opinion the price is too high."),
                 X("Soviel ich weiß, ist es noch offen.", "zoh-FEEL ikh vice, ist es nokh OF-fen.", "As far as I know it is still open.")],
                [("Meiner Meinung nach der Preis ist zu hoch.", "Meiner Meinung nach ist der Preis zu hoch.", "The fronted phrase takes position 1: verb second."),
                 ("Ich finde dass wir brauchen mehr Zeit.", "Ich finde, dass wir mehr Zeit brauchen.", "In the dass-clause the verb goes last.")]),
              [D("Frau Wolf", "Was halten Sie von dem Vorschlag?", "vas HAL-ten zee fon daym FOHR-shlahk?", "What do you think of the proposal?"),
               D("Max", "Meiner Meinung nach ist der Zeitplan zu knapp.", "MY-ner MY-noong nahkh ist dair TSITE-plahn tsoo knap.", "In my opinion the schedule is too tight."),
               D("Frau Wolf", "Und warum?", "unt var-OOM?", "And why?"),
               D("Max", "Ich finde, dass zwei Wochen nicht reichen.", "ikh FIN-duh, das tsvy VOKH-en nikht RY-khen.", "I think two weeks are not enough.")],
              WS("Opinion worksheet", [
                  T("Give an opinion with a frame.", ["the plan will work", "the price is too high", "we need more time"],
                    ["Ich finde, dass der Plan funktioniert.", "Meiner Meinung nach ist der Preis zu hoch.", "Ich finde, dass wir mehr Zeit brauchen."]),
                  T("Hedge it.", ["as far as I know", "I believe"],
                    ["soviel ich weiß", "ich glaube"]),
              ])),
            L("Disagreeing with the person intact",
              "The German ladder: DA HABEN SIE RECHT, ABER … · ICH SEHE DAS ANDERS · DAS SEHE ICH "
              "NICHT SO. Start where you agree — that is how the sentence is built, not a "
              "politeness trick.",
              [V("da haben Sie recht", "dah HAH-ben zee rekht", "you're right about that", "phrase"),
               V("anders sehen", "AN-ders ZAY-en", "to see differently", "phrase"),
               V("der Einwand", "dair INE-vant", "objection", "noun"),
               V("überzeugen", "ew-ber-TSOY-gen", "to convince", "verb"),
               V("der Kompromiss", "dair kom-pro-MIS", "compromise", "noun")],
              G("Disagreement ladder",
                "da haben Sie recht, aber … · ich sehe das anders · das sehe ich nicht so",
                "Da haben Sie recht, aber die Zahlen sagen etwas anderes. Ich sehe das anders: "
                "der Aufwand ist höher. «Ich sehe das anders» disagrees with the view; «Sie irren "
                "sich» disagrees with the person.",
                [X("Da haben Sie recht, aber der Aufwand ist höher.", "dah HAH-ben zee rekht, AH-ber dair OWF-vant ist HUR-er.", "You're right about that, but the effort is higher."),
                 X("Ich sehe das anders.", "ikh ZAY-uh das AN-ders.", "I see it differently."),
                 X("Das sehe ich nicht so.", "das ZAY-uh ikh nikht zoh.", "I don't see it that way.")],
                [("Sie irren sich.", "Da haben Sie recht, aber ich sehe das anders.", "Naming the person makes the room defensive."),
                 ("Ich sehe anders das.", "Ich sehe das anders.", "The adverb closes the sentence.")]),
              [D("Herr Wolf", "Wir sollten sofort starten.", "veer ZOL-ten zoh-FOHRT SHTAR-ten.", "We should start immediately."),
               D("Lena", "Da haben Sie recht, aber die Vorbereitung fehlt noch.", "dah HAH-ben zee rekht, AH-ber dee fohr-beh-RY-toong faylt nokh.", "You're right about that, but the preparation is still missing."),
               D("Herr Wolf", "Und Ihr Vorschlag?", "unt eer FOHR-shlahk?", "And your suggestion?"),
               D("Lena", "Ich sehe das anders: erst zwei Tage vorbereiten, dann starten.", "ikh ZAY-uh das AN-ders: airst tsvy TAH-guh fohr-beh-RY-ten, dan SHTAR-ten.", "I see it differently: prepare for two days first, then start.")],
              WS("Disagreement worksheet", [
                  T("Disagree, keeping respect.", ["the deadline is realistic", "the plan is cheap"],
                    ["Da haben Sie recht, aber die Frist ist knapp.", "Ich sehe das anders: der Plan ist teuer."]),
                  T("Concede then differ.", ["the report is good (but late)", "the idea is right (but costly)"],
                    ["Der Bericht ist gut, aber spät.", "Die Idee ist richtig, aber teuer."]),
              ])),
            L("Modal particles: ja, doch, wohl, eigentlich",
              "German particles tune a sentence: DAS IST JA KLAR (as you know), KOMM DOCH MIT "
              "(come on), DAS IST WOHL RICHTIG (probably), EIGENTLICH WOLLTE ICH … (actually I "
              "wanted). They carry stance, not content.",
              [V("ja", "yah", "indeed, as you know", "particle"),
               V("doch", "dokh", "after all, do (urging)", "particle"),
               V("wohl", "vohl", "probably", "particle"),
               V("eigentlich", "EY-gent-likh", "actually", "particle"),
               V("halt", "halt", "simply, just (regional)", "particle")],
              G("Particles in position",
                "ja / doch / wohl / eigentlich sit in the middle field, after the verb",
                "Das ist ja interessant. Komm doch mit! Er hat wohl recht. Eigentlich wollte ich "
                "früher gehen. Removing a particle does not change the facts — it changes the "
                "speaker's relation to the listener, which is why learners are understood without "
                "them and sound foreign with none.",
                [X("Das ist ja praktisch.", "das ist yah prak-TISH.", "That's practical, as you know."),
                 X("Komm doch mit!", "kom dokh mit!", "Do come along!"),
                 X("Das ist wohl ein Missverständnis.", "das ist vohl ine MIS-fair-shtent-nis.", "That's probably a misunderstanding.")],
                [("Das ja ist praktisch.", "Das ist ja praktisch.", "Particles sit after the verb, not before it."),
                 ("Komm doch du mit!", "Komm doch mit!", "doch already does the urging; the pronoun is not needed.")]),
              [D("Max", "Kommst du mit ins Konzert?", "KOMST doo mit ins kon-TSAIRT?", "Are you coming to the concert?"),
               D("Lena", "Eigentlich wollte ich lernen.", "EY-gent-likh VOL-tuh ikh LAIR-nen.", "Actually I wanted to study."),
               D("Max", "Komm doch mit — das ist ja nur einmal.", "kom dokh mit — das ist yah noor INE-mahl.", "Do come along — it's only this once."),
               D("Lena", "Na gut, dann wohl doch.", "nah goot, dan vohl dokh.", "All right, then I probably will.")],
              WS("Particle worksheet", [
                  T("Add the particle.", ["that's interesting (as you know)", "come along (urging)", "probably true"],
                    ["Das ist ja interessant.", "Komm doch mit!", "Das ist wohl richtig."]),
                  T("Soften a statement.", ["actually I wanted to leave earlier"],
                    ["Eigentlich wollte ich früher gehen."]),
              ])),
        ]},
        {"id": "B1+-U3", "title": "Register: du, Sie, ihr", "lessons": [
            L("Choosing the pronoun",
              "German has three: SIE (distance, respect), DU (familiar singular), IHR (familiar "
              "plural). The verb form follows: SPRECHEN SIE / SPRICHST DU / SPRECHT IHR. Getting "
              "this wrong is heard before any grammar error.",
              [V("Sie", "zee", "you (formal)", "pronoun"),
               V("du", "doo", "you (familiar)", "pronoun"),
               V("ihr", "eer", "you (familiar plural)", "pronoun"),
               V("das Du", "das doo", "the familiar address", "noun"),
               V("das Sie", "das zee", "the formal address", "noun")],
              G("Pronoun governs the verb",
                "Sie sprechen · du sprichst · ihr sprecht",
                "Können Sie mir helfen? Kannst du mir helfen? Könnt ihr mir helfen? The polite "
                "form is the third-person plural shape with a capital S — that is why «Sie sind» "
                "and «sie sind» sound alike and are told apart by context and capitalisation.",
                [X("Können Sie das bitte wiederholen?", "KUR-nen zee das BIT-tuh vee-der-HOH-len?", "Could you repeat that, please?"),
                 X("Kannst du das bitte wiederholen?", "kanst doo das BIT-tuh vee-der-HOH-len?", "Can you repeat that, please?"),
                 X("Könnt ihr morgen kommen?", "kurt eer MOR-gen KOM-men?", "Can you (all) come tomorrow?")],
                [("Kannst du das bitte wiederholen, Herr Wolf?", "Können Sie das bitte wiederholen, Herr Wolf?", "A surname takes Sie."),
                 ("Ihr kannst kommen.", "Ihr könnt kommen.", "ihr takes the second-person plural form: könnt.")]),
              [D("Lena", "Können Sie mir helfen, Herr Wolf?", "KUR-nen zee meer HEL-fen, hair volf?", "Could you help me, Mr Wolf?"),
               D("Herr Wolf", "Natürlich. Wo ist das Problem?", "nah-TEWR-likh. voh ist das pro-BLEEM?", "Of course. Where is the problem?"),
               D("Lena", "Können Sie den Satz noch einmal sagen?", "KUR-nen zee dayn zats nokh INE-mahl ZAH-gen?", "Could you say the sentence once more?"),
               D("Herr Wolf", "Gerne. Und du kannst mich fragen, wann du willst.", "GAIR-nuh. unt doo kanst mikh FRAH-gen, van doo vilst.", "Gladly. And you can ask me whenever you like.")],
              WS("Register worksheet", [
                  T("Choose the right form.", ["to your professor", "to your friend", "to a group of friends"],
                    ["Können Sie …", "Kannst du …", "Könnt ihr …"]),
                  T("Answer respectfully.", ["can you help me?", "can you repeat that?", "when can you come?"],
                    ["Können Sie mir helfen?", "Können Sie das wiederholen?", "Wann können Sie kommen?"]),
              ])),
            L("From Sie to du: the switch",
              "The switch is proposed, never assumed: WIR KÖNNEN UNS GERNE DUZEN · SOLLEN WIR UNS "
              "DUZEN? The older or senior person offers; the other accepts.",
              [V("duzen", "DOO-tsen", "to address with du", "verb"),
               V("siezen", "ZEE-tsen", "to address with Sie", "verb"),
               V("vorschlagen", "FOHR-shlah-gen", "to suggest", "verb"),
               V("der Kollege", "dair kol-LAY-guh", "colleague (m)", "noun"),
               V("die Runde", "dee ROON-duh", "round (of people)", "noun")],
              G("Offering the switch",
                "sollen wir uns duzen? · wir können uns gerne duzen · bleiben wir beim Sie?",
                "Sollen wir uns duzen? — Ja, gerne, ich bin der Max. If declined: Bleiben wir "
                "lieber beim Sie. Both answers are complete; the offer itself is the polite act.",
                [X("Sollen wir uns duzen?", "ZOL-len veer oons DOO-tsen?", "Shall we use du?"),
                 X("Wir können uns gerne duzen.", "veer KUR-nen oons GAIR-nuh DOO-tsen.", "We're welcome to switch to du."),
                 X("Bleiben wir lieber beim Sie.", "BLY-ben veer LEE-ber bym zee.", "Let's rather stay with Sie.")],
                [("Wir duzen jetzt.", "Sollen wir uns duzen?", "The switch is offered, not decreed."),
                 ("Ich bin Max, Sie sind Frau Wolf, oder?", "Sollen wir uns duzen, Frau Wolf?", "The offer comes as a question with the name.")]),
              [D("Herr Wolf", "Wir arbeiten jetzt oft zusammen. Sollen wir uns duzen?", "veer AR-by-ten yetst oft tsoo-ZAH-men. ZOL-len veer oons DOO-tsen?", "We work together often now. Shall we use du?"),
               D("Lena", "Gerne! Ich bin die Lena.", "GAIR-nuh! ikh bin dee LAY-nuh.", "Gladly! I'm Lena."),
               D("Herr Wolf", "Und ich der Thomas. Willkommen im Team.", "unt ikh dair TOH-mahs. vil-KOM-men im teem.", "And I'm Thomas. Welcome to the team."),
               D("Lena", "Danke, Thomas. Dann duze ich Sie — dich — ab heute.", "DAN-kuh, TOH-mahs. dan DOO-tsuh ikh zee — dikh — ap HOY-tuh.", "Thanks, Thomas. Then I'll use du — you — from today.")],
              WS("Switch worksheet", [
                  T("Offer the switch.", ["shall we use du?", "welcome to switch", "let's stay with Sie"],
                    ["Sollen wir uns duzen?", "Wir können uns gerne duzen.", "Bleiben wir beim Sie."]),
                  T("Accept and introduce yourself.", ["gladly, I'm Lena"],
                    ["Gerne! Ich bin die Lena."]),
              ])),
            L("Greetings that match the person",
              "Greetings follow region and relationship: GUTEN TAG everywhere, HALLO with friends, "
              "GRÜSS GOTT in the south, MOIN in the north, SERVUS in Bavaria. Leaving: "
              "AUF WIEDERSEHEN (formal), TSCHÜSS (familiar), WIRS SEHEN UNS (casual).",
              [V("Guten Tag", "GOO-ten tahk", "good day", "greeting"),
               V("Hallo", "hah-LOH", "hello (casual)", "greeting"),
               V("Grüß Gott", "grews got", "greeting (southern)", "greeting"),
               V("Moin", "moyn", "hello (northern)", "greeting"),
               V("Auf Wiederhören", "owf vee-der-HUR-ren", "goodbye (on the phone)", "phrase")],
              G("Greeting by region and relation",
                "Guten Tag / Hallo / Grüß Gott / Moin · Auf Wiedersehen / Tschüss",
                "In Hamburg hört man «Moin», in München «Grüß Gott» — both are correct, both are "
                "regional, and a learner is usually advised to start with «Guten Tag» and let the "
                "other person set the tone.",
                [X("Guten Tag, wie geht es Ihnen?", "GOO-ten tahk, vee gayt es EEN-en?", "Good day, how are you?"),
                 X("Hallo, wie geht's?", "hah-LOH, vee gayts?", "Hi, how are you?"),
                 X("Auf Wiedersehen — und auf Wiederhören am Telefon!", "owf VEE-der-zay-en — unt owf vee-der-HUR-ren am te-le-FOHN!", "Goodbye — and 'goodbye' on the phone!")],
                [("Guten Tag, wie geht's dir, Frau Wolf?", "Guten Tag, wie geht es Ihnen, Frau Wolf?", "The surname takes Sie and the matching verb."),
                 ("Tschüss, Herr Professor.", "Auf Wiedersehen, Herr Professor.", "Tschüss is for people you call du.")]),
              [D("Lena", "Guten Tag, Herr Wolf!", "GOO-ten tahk, hair volf!", "Good day, Mr Wolf!"),
               D("Herr Wolf", "Guten Tag, Frau Berger. Wie geht es Ihnen?", "GOO-ten tahk, frow BAIR-ger. vee gayt es EEN-en?", "Good day, Ms Berger. How are you?"),
               D("Lena", "Danke, gut. Und Ihnen?", "DAN-kuh, goot. unt EEN-en?", "Fine, thanks. And you?"),
               D("Herr Wolf", "Auch gut. Auf Wiedersehen!", "owkh goot. owf VEE-der-zay-en!", "Well too. Goodbye!")],
              WS("Greeting worksheet", [
                  T("Greet the right way.", ["a professor", "a friend in the north", "an elder in Bavaria"],
                    ["Guten Tag, Herr …", "Moin!", "Grüß Gott!"]),
                  T("Leave the right way.", ["to a colleague you call Sie", "on the phone", "to a friend"],
                    ["Auf Wiedersehen!", "Auf Wiederhören!", "Tschüss!"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Register in Germany is negotiated, not fixed: a team can work years in Sie and "
                 "switch over lunch, and the offer («sollen wir uns duzen?») always comes from the "
                 "person with more standing. A learner who waits for the offer is never wrong, "
                 "and a learner who offers it to a stranger is remembered. The half-step teaches "
                 "the offer, the acceptance and the polite refusal as three complete moves."),
        source_url="https://en.wikipedia.org/wiki/Formality",
        reading=("Meine neue Kollegin hat mich drei Wochen gesiezt, ich sie auch. Am Freitag hat "
                 "sie gefragt: «Sollen wir uns duzen?» Ich habe ja gesagt, und plötzlich waren die "
                 "E-Mails kürzer. Ein Kollege hat abgelehnt: «Bleiben wir lieber beim Sie.» Das war "
                 "nicht unfreundlich — nur eine Entscheidung. Ich habe gelernt, dass die Anrede "
                 "kein Zufall ist, sondern eine Verhandlung."),
        reading_gloss=("My new colleague used Sie with me for three weeks; I did with her too. On "
                       "Friday she asked: 'Shall we use du?' I said yes, and suddenly the emails "
                       "were shorter. One colleague declined: 'Let's rather stay with Sie.' That "
                       "was not unfriendly — just a decision. I learned that the form of address "
                       "is not an accident but a negotiation."),
        listening=("Max: Sollen wir uns duzen?<br>Lena: Gerne! Ich bin die Lena.<br>"
                   "Max: Und ich der Max. Willkommen im Team.<br>Lena: Danke — dann sage ich ab heute du."),
        listening_gloss=("Max: Shall we use du? Lena: Gladly! I'm Lena. Max: And I'm Max. Welcome to "
                         "the team. Lena: Thanks — then from today I'll say du."),
        voice_tag=VOICE,
        idioms=[
            ("Auf Wiedersehen", "until seeing again", "goodbye (formal)"),
            ("Grüß Gott", "greet God", "hello (southern)"),
            ("Moin", "morning", "hello (northern)"),
            ("Sich duzen", "to du each other", "to be on familiar terms"),
            ("Beim Sie bleiben", "to stay with Sie", "to keep the formal address"),
            ("Unter uns", "among us", "between ourselves"),
            ("Mit Vornamen", "by first name", "on first-name terms"),
            ("Auf Augenhöhe", "at eye level", "as equals"),
            ("Guten Ton", "good tone", "good form, etiquette"),
            ("Das Du anbieten", "to offer the du", "to propose informality"),
        ],
        mistakes=[
            ("Kannst du mir helfen, Herr Wolf?", "Können Sie mir helfen, Herr Wolf?", "A surname takes Sie."),
            ("Ihr bist willkommen.", "Ihr seid willkommen.", "ihr takes seid."),
            ("Wir duzen jetzt.", "Sollen wir uns duzen?", "The switch is offered, not decreed."),
        ],
        task_title="Map your German register",
        task_instructions=("Write four short dialogues in German: with a professor, a colleague your "
                           "age, a group of friends, and a neighbour you have known for a year. "
                           "Use Sie, du and ihr in the right places, and propose the du-to-Sie "
                           "switch once. Read them aloud — if a sentence mixes the pronouns and "
                           "the verb endings, that is the pair to fix, not the vocabulary."),
    ),
    "test": [
        ("translate_en", "Say: I need two more days, and I would like to keep the team.", "Ich brauche zwei Tage mehr, und ich möchte das Team behalten."),
        ("translate_de", "Meiner Meinung nach ist der Preis zu hoch.", "In my opinion the price is too high."),
        ("multiple_choice", "Which reply fits «Sollen wir uns duzen?»", "Gerne! Ich bin die Lena."),
        ("fill_in_the_blank", "Können ___ mir helfen, Herr Wolf?", "Sie"),
        ("word_selection", "Select the German for 'to consider'.", "überlegen"),
        ("error_correction", "Ich finde dass wir brauchen mehr Zeit.", "Ich finde, dass wir mehr Zeit brauchen."),
        ("dialogue_completion", "Complete: Da haben Sie recht, ___ (but the effort is higher)", "aber der Aufwand ist höher"),
        ("matching", "Match «das Du» to its meaning.", "the familiar address"),
        ("reading_comprehension", "Die Kollegin hat nach drei Wochen gefragt. What did she want?", "to switch from Sie to du"),
        ("inference", "«Die Anrede ist eine Verhandlung» — what does the writer mean?", "forms of address are negotiated between people"),
        ("main_idea", "Ein Kollege hat abgelehnt, und das war nicht unfreundlich. What is the point?", "a refusal is a decision, not a rejection"),
        ("detail_identification", "Wie lange hat sie gesiezt? (three weeks)", "drei Wochen"),
    ],
}

HALFSTEPS["B2+"] = {
    "title": "German B2+ — Professional",
    "native": NATIVE,
    "goals": [
        "Run the moves of a German meeting: open, qualify, decide, minute",
        "Write an email, a summary and minutes that get acted on",
        "Negotiate a deadline with the plan attached",
    ],
    "units": [
        {"id": "B2+-U1", "title": "In der Besprechung", "lessons": [
            L("Opening, framing, closing down",
              "A German meeting has named moves: die Tagesordnung (agenda), der Punkt (item), "
              "die Entscheidung. Saying which move you are in is what makes you audible.",
              [V("die Tagesordnung", "dee TAH-guhs-or-noong", "agenda", "noun"),
               V("der Punkt", "dair poonkt", "item, point", "noun"),
               V("die Entscheidung", "dee ent-SHY-dung", "decision", "noun"),
               V("beschließen", "beh-SHLEE-sen", "to resolve, decide", "verb"),
               V("die Sitzung", "dee ZIT-soong", "meeting, session", "noun")],
              G("Meeting moves",
                "wir haben drei Punkte · kommen wir zum zweiten Punkt · dann beschließen wir",
                "Wir haben drei Punkte: Kosten, Zeit, Verantwortung. Kommen wir zum zweiten "
                "Punkt. Dann beschließen wir. The move is announced, then performed — that is "
                "the difference between chairing and talking.",
                [X("Wir haben drei Punkte auf der Tagesordnung.", "veer HAH-ben dry poonk-tuh owf dair TAH-guhs-or-noong.", "We have three items on the agenda."),
                 X("Kommen wir zum zweiten Punkt.", "KOM-men veer tsoom TSVY-ten poonkt.", "Let's come to the second item."),
                 X("Dann beschließen wir das heute.", "dan beh-SHLEE-sen veer das HOY-tuh.", "Then we'll decide it today.")],
                [("Wir haben Tagesordnung drei.", "Wir haben drei Punkte auf der Tagesordnung.", "The agenda carries items: Punkte auf der Tagesordnung."),
                 ("Kommen wir zum Punkt zweiten.", "Kommen wir zum zweiten Punkt.", "Ordinals before the noun here.")]),
              [D("Herr Wolf", "Wir haben zwei Punkte: Zeit und Kosten.", "veer HAH-ben tsvy poonk-tuh: tsite unt KOS-ten.", "We have two items: time and costs."),
               D("Lena", "Kommen wir zuerst zu den Kosten?", "KOM-men veer tsoo-AIRST tsoo dayn KOS-ten?", "Shall we take costs first?"),
               D("Herr Wolf", "Gut. Dann die Zeit. Und am Ende beschließen wir.", "goot. dan dee tsite. unt am EN-duh beh-SHLEE-sen veer.", "Good. Then time. And at the end we decide."),
               D("Lena", "Einverstanden — ich notiere.", "IN-fair-shtan-den — ikh no-TEE-ruh.", "Agreed — I'll take notes.")],
              WS("Meeting worksheet", [
                  T("Open the meeting.", ["two items", "let's start", "the agenda"],
                    ["Wir haben zwei Punkte.", "Fangen wir an.", "die Tagesordnung"]),
                  T("Close it down.", ["come to the decision", "we decide today", "who takes notes?"],
                    ["Kommen wir zur Entscheidung.", "Wir beschließen das heute.", "Wer notiert?"]),
              ])),
            L("Qualifying a claim in a meeting",
              "German meetings qualify with conditions and scope: UNTER DER VORAUSSETZUNG, DASS … · "
              "VORAUSGESETZT, … · NUR WENN … · IM RAHMEN DES BUDGETS.",
              [V("die Voraussetzung", "dee fohr-OWS-zeh-tsoong", "precondition", "noun"),
               V("vorausgesetzt", "fohr-OWS-ge-zehzt", "provided that", "conjunction"),
               V("der Rahmen", "dair RAH-men", "frame, scope", "noun"),
               V("verbindlich", "fair-BINT-likh", "binding", "adjective"),
               V("die Zusage", "dee TSOO-zah-guh", "commitment, promise", "noun")],
              G("Qualified commitment",
                "unter der Voraussetzung, dass … · vorausgesetzt, das Budget … · nur wenn …",
                "Wir sagen zu — unter der Voraussetzung, dass das Budget bleibt. Nur wenn zwei "
                "Stellen frei bleiben, ist der Termin zu halten. The condition travels with the "
                "promise in the same sentence.",
                [X("Wir sagen unter Voraussetzung zu.", "veer ZAH-gen OON-ter fohr-OWS-zeh-tsoong tsoo.", "We agree on one condition."),
                 X("Nur wenn das Budget bleibt, ist es machbar.", "noor ven das bew-ZHAY BLYPT, ist es MAKH-bar.", "Only if the budget stays is it doable."),
                 X("Im Rahmen des Budgets ja.", "im RAH-men des bew-ZHAYS yah.", "Within the budget, yes.")],
                [("Wir sagen zu, aber vielleicht nicht.", "Wir sagen unter Voraussetzung zu.", "State the condition instead of cancelling the promise."),
                 ("Vorausgesetzt dass das klappt.", "Vorausgesetzt, das klappt.", "vorausgesetzt takes a comma, then a main clause.")]),
              [D("Herr Wolf", "Können Sie den Termin zusagen?", "KUR-nen zee dayn ter-MEEN TSOO-zah-gen?", "Can you commit to the date?"),
               D("Lena", "Unter einer Voraussetzung: das Budget bleibt.", "OON-ter EYE-ner fohr-OWS-zeh-tsoong: das bew-ZHAY blypt.", "On one condition: the budget stays."),
               D("Herr Wolf", "Und wenn nicht?", "unt ven nikht?", "And if not?"),
               D("Lena", "Dann nur die Hälfte — das sage ich lieber jetzt.", "dan noor dee HELF-tuh — das ZAH-guh ikh LEE-ber yetst.", "Then only half — I'd rather say that now.")],
              WS("Qualification worksheet", [
                  T("Qualify the commitment.", ["we agree (if the budget stays)", "only if two posts stay free"],
                    ["Wir sagen unter Voraussetzung zu — wenn das Budget bleibt.", "Nur wenn zwei Stellen frei bleiben."]),
                  T("Use the frame.", ["within the budget", "provided that it works"],
                    ["im Rahmen des Budgets", "vorausgesetzt, es klappt"]),
              ])),
            L("Reporting what someone said",
              "Reported speech keeps the facts and shifts the frame: ER HAT GESAGT, DASS … · SIE "
              "MEINTE, … · LAUT PROTOKOLL … The Konjunktiv I marks the distance in formal German.",
              [V("das Protokoll", "das pro-to-KOL", "minutes", "noun"),
               V("mitteilen", "MIT-ty-len", "to inform, to communicate", "verb"),
               V("die Aussage", "dee OWS-zah-guh", "statement", "noun"),
               V("bestätigen", "beh-SHTAY-ti-gen", "to confirm", "verb"),
               V("dementieren", "day-men-TEE-ren", "to deny", "verb")],
              G("Reporting",
                "er hat gesagt, dass … · laut Protokoll … · sie habe … (Konjunktiv I)",
                "Laut Protokoll hat sie zugesagt. Sie habe die Zahlen geprüft — schreibt die "
                "Zeitung. In informal speech the indicative is normal; the Konjunktiv I appears "
                "where the report must not become an assertion.",
                [X("Laut Protokoll hat sie zugesagt.", "lowt pro-to-KOL hat zee TSOO-ge-zahkt.", "According to the minutes, she agreed."),
                 X("Er hat gesagt, dass er morgen kommt.", "air hat ge-ZAHKT, das air MOR-gen komt.", "He said he is coming tomorrow."),
                 X("Die Firma bestätigt den Termin.", "dee FEER-mah beh-SHTAY-tikt dayn ter-MEEN.", "The company confirms the date.")],
                [("Er hat gesagt, dass ich morgen komme.", "Er hat gesagt, dass er morgen kommt.", "The report shifts the pronoun, not only the verb."),
                 ("Laut Protokoll sie hat zugesagt.", "Laut Protokoll hat sie zugesagt.", "After the fronted phrase the verb stays in position 2.")]),
              [D("Lena", "Was hat Herr Wolf gesagt?", "vas hat hair volf ge-ZAHKT?", "What did Mr Wolf say?"),
               D("Max", "Er hat gesagt, dass die Zahlen stimmen.", "air hat ge-ZAHKT, das dee TSAH-len SHTIM-men.", "He said the figures are right."),
               D("Lena", "Steht das im Protokoll?", "shtayt das im pro-to-KOL?", "Is that in the minutes?"),
               D("Max", "Ja, wörtlich. Und die Firma bestätigt es schriftlich.", "yah, VURT-likh. unt dee FEER-mah beh-SHTAY-tikt es SHRIFT-likh.", "Yes, word for word. And the company confirms it in writing.")],
              WS("Report worksheet", [
                  T("Report the sentence.", ["'I will call tomorrow' (he)", "'the figures are right' (she)"],
                    ["Er hat gesagt, dass er morgen anruft.", "Sie hat gesagt, dass die Zahlen stimmen."]),
                  T("Use the formal frame.", ["according to the minutes", "in writing"],
                    ["laut Protokoll", "schriftlich"]),
              ])),
        ]},
        {"id": "B2+-U2", "title": "Schreiben, das wirkt", "lessons": [
            L("A message that gets an answer",
              "Professional German messages are three-part: BEZUG (context), ANLIEGEN (request), "
              "DANK. The request is nominal and polite: ICH BITTE UM … · WÄRE ES MÖGLICH, …?",
              [V("der Bezug", "dair beh-TSOOK", "reference, context", "noun"),
               V("das Anliegen", "das AN-lee-gen", "concern, request", "noun"),
               V("ich bitte um", "ikh BIT-tuh oom", "I request", "phrase"),
               V("wäre es möglich", "VAIR-uh es MURKH-likh", "would it be possible", "phrase"),
               V("die Rückmeldung", "dee REWK-mel-doong", "reply, feedback", "noun")],
              G("Message frame",
                "Bezug: … · ich bitte um … · ich freue mich auf Ihre Rückmeldung",
                "Bezug: Termin am 12. Mai. Ich bitte um die Unterlagen bis Freitag. Für eine kurze "
                "Rückmeldung wäre ich dankbar. The request is a noun phrase with um — that is the "
                "register.",
                [X("Ich bitte um kurze Rückmeldung.", "ikh BIT-tuh oom KOOR-tsuh REWK-mel-doong.", "I would ask for a short reply."),
                 X("Wäre es möglich, die Unterlagen zu senden?", "VAIR-uh es MURKH-likh, dee OON-ter-lah-gen tsoo ZEN-den?", "Would it be possible to send the documents?"),
                 X("Vielen Dank im Voraus.", "FEE-len dank im fohr-OWS.", "Many thanks in advance.")],
                [("Ich will die Unterlagen.", "Ich bitte um die Unterlagen.", "The nominal request keeps the register."),
                 ("Bitte senden mir die Unterlagen.", "Bitte senden Sie mir die Unterlagen.", "The polite imperative needs Sie.")]),
              [D("Lena", "Ist die Mail so in Ordnung?", "ist dee mail zoh in OR-noong?", "Is the email all right like this?"),
               D("Max", "Der Bezug fehlt. Schreib: Bezug: Termin am 12. Mai.", "dair beh-TSOOK faylt. shryp: beh-TSOOK: ter-MEEN am TSVURLF-ten my.", "The reference is missing. Write: re: appointment on 12 May."),
               D("Lena", "Und die Bitte?", "unt dee BIT-tuh?", "And the request?"),
               D("Max", "«Ich bitte um die Unterlagen bis Freitag.» — höflich und klar.", "ikh BIT-tuh oom dee OON-ter-lah-gen bis FRY-tahk — HURF-likh unt klar.", "'I would ask for the documents by Friday.' — polite and clear.")],
              WS("Message worksheet", [
                  T("Build the three parts.", ["reference: the report", "request: by Friday", "thanks"],
                    ["Bezug: der Bericht", "Ich bitte um die Unterlagen bis Freitag.", "Vielen Dank im Voraus."]),
                  T("Ask a favour in the register.", ["send the file", "a short reply"],
                    ["Wäre es möglich, die Datei zu senden?", "Ich bitte um kurze Rückmeldung."]),
              ])),
            L("The summary: drei Zeilen",
              "A German summary states decision, reason, next step: BESCHLUSS: … · GRUND: … · "
              "NÄCHSTER SCHRITT: …. Three lines, no adjectives.",
              [V("der Beschluss", "dair beh-SHLUS", "resolution", "noun"),
               V("der Grund", "dair groont", "reason", "noun"),
               V("der nächste Schritt", "dair NAYS-tuh shrit", "next step", "noun"),
               V("die Zusammenfassung", "dee tsoo-ZAH-men-fah-soong", "summary", "noun"),
               V("das Ergebnis", "das air-GAYP-nis", "result", "noun")],
              G("Decision → reason → next step",
                "Beschluss: … · Grund: … · Nächster Schritt: …",
                "Beschluss: Die Frist wird um zwei Wochen verlängert. Grund: Daten fehlen. "
                "Nächster Schritt: neuer Termin am Montag. Nothing else belongs in a summary.",
                [X("Beschluss: Die Frist wird verlängert.", "beh-SHLUS: dee frist vairt fair-LAYN-gert.", "Resolution: the deadline is extended."),
                 X("Grund: Die Daten fehlen noch.", "groont: dee DAH-ten FAY-len nokh.", "Reason: the data is still missing."),
                 X("Nächster Schritt: Termin am Montag.", "NAYS-ter shrit: ter-MEEN am MOHN-tahk.", "Next step: appointment on Monday.")],
                [("Zusammenfassung: Es war ein langes Gespräch.", "Beschluss: … · Grund: …", "A summary is decision-shaped, not narrative."),
                 ("Grund und Ergebnis sind dasselbe.", "Grund: … · Ergebnis: …", "Keep the cause and the outcome in separate slots.")]),
              [D("Herr Wolf", "Lesen Sie die Zusammenfassung vor.", "LAY-zen zee dee tsoo-ZAH-men-fah-soong fohr.", "Read the summary aloud."),
               D("Lena", "Beschluss: Design genehmigt. Grund: Test war gut. Nächster Schritt: Montag.", "beh-SHLUS: di-ZINE ge-NY-mikt. groont: test vahr goot. NAYS-ter shrit: MOHN-tahk.", "Resolution: design approved. Reason: the test was good. Next step: Monday."),
               D("Herr Wolf", "Gut — drei Zeilen, alles drin.", "goot — dry TSY-len, AL-les drin.", "Good — three lines, everything in."),
               D("Lena", "Soll ich sie ins Protokoll setzen?", "zol ikh zee ins pro-to-KOL ZET-sen?", "Shall I put it into the minutes?")],
              WS("Summary worksheet", [
                  T("Summarize in three lines.", ["the decision", "the reason", "the next step"],
                    ["Beschluss: Die Frist wird verlängert.", "Grund: Die Daten fehlen.", "Nächster Schritt: Montag, neuer Termin."]),
                  T("Cut the filler.", ["a long polite paragraph with one decision"],
                    ["Beschluss: … — der Rest ist Kontext."]),
              ])),
            L("Notes into minutes",
              "Minutes are terse and dated: DATUM, ANWESENDE, BESCHLÜSSE, VERANTWORTLICH, NÄCHSTER "
              "TERMIN. Four headings and any meeting can be written up.",
              [V("das Datum", "das DAH-toom", "date", "noun"),
               V("die Anwesenden", "dee AN-veh-zen-den", "those present", "noun"),
               V("verantwortlich", "fair-ANT-vort-likh", "responsible", "adjective"),
               V("der Beschluss", "dair beh-SHLUS", "resolution", "noun"),
               V("die Frist", "dee frist", "deadline", "noun")],
              G("Minutes headings",
                "Datum · Anwesende · Beschlüsse · Verantwortlich · Nächster Termin",
                "Datum: 12. Oktober. Anwesende: acht. Beschluss: Frist plus zwei Wochen. "
                "Verantwortlich: Lena Berger. Nächster Termin: Montag. Headings make the page "
                "usable a month later.",
                [X("Anwesende: acht Personen.", "AN-veh-zen-duh: ahkht pair-ZOH-nen.", "Present: eight people."),
                 X("Verantwortlich: Lena Berger.", "fair-ANT-vort-likh: LAY-nuh BAIR-ger.", "Responsible: Lena Berger."),
                 X("Nächster Termin: Montag, 10 Uhr.", "NAYS-ter ter-MEEN: MOHN-tahk, tsehn oor.", "Next appointment: Monday, 10 o'clock.")],
                [("Anwesende sind viele.", "Anwesende: acht.", "Minutes take counts and names, not evaluations."),
                 ("Beschluss: vielleicht.", "Beschluss: Frist plus zwei Wochen.", "A minute records the decision, not the mood.")]),
              [D("Max", "Wer schreibt das Protokoll?", "vair SHRYPE das pro-to-KOL?", "Who writes the minutes?"),
               D("Lena", "Ich: Datum, Anwesende, Beschlüsse, Verantwortlich.", "ikh: DAH-toom, AN-veh-zen-duh, beh-SHLEW-suh, fair-ANT-vort-likh.", "Me: date, attendance, resolutions, responsibility."),
               D("Max", "Und der nächste Termin?", "unt dair NAYS-tuh ter-MEEN?", "And the next appointment?"),
               D("Lena", "Montag, zehn Uhr — steht schon drin.", "MOHN-tahk, tsehn oor — shtayt shohn drin.", "Monday, ten o'clock — it's in already.")],
              WS("Minutes worksheet", [
                  T("Write the headings.", ["who was present", "what was decided", "whose duty", "next meeting"],
                    ["Anwesende: acht", "Beschluss: Frist verlängert", "Verantwortlich: Lena", "Nächster Termin: Montag"]),
                  T("Correct a vague note.", ["it was maybe decided"],
                    ["Beschluss: Die Frist wird um zwei Wochen verlängert."]),
              ])),
        ]},
        {"id": "B2+-U3", "title": "Fristen verhandeln", "lessons": [
            L("Bearing bad news early",
              "German offices prefer the early warning: ICH MELDE MICH FRÜHZEITIG · ES KANN ZU "
              "EINER VERZÖGERUNG KOMMEN · DER RISIKO IST … Bad news that arrives early is project "
              "management; the same news on the deadline is a character problem.",
              [V("frühzeitig", "FREW-tsy-tikh", "early, in good time", "adverb"),
               V("die Verzögerung", "dee fair-TSUR-guh-roong", "delay", "noun"),
               V("das Risiko", "das REE-zee-koh", "risk", "noun"),
               V("rechtzeitig", "REKHT-tsy-tikh", "on time", "adverb"),
               V("melden", "MEL-den", "to report", "verb")],
              G("Early-warning frames",
                "ich melde mich frühzeitig · es kann zu … kommen · das Risiko liegt bei …",
                "Ich melde frühzeitig: Es kann zu einer Verzögerung von zwei Tagen kommen. The "
                "warning is a first-person statement of fact, with the number attached.",
                [X("Es kann zu einer Verzögerung kommen.", "es kan tsoo EYE-ner fair-TSUR-guh-roong KOM-men.", "There may be a delay."),
                 X("Ich melde mich bewusst frühzeitig.", "ikh MEL-duh mikh beh-VOOST FREW-tsy-tikh.", "I am reporting deliberately early."),
                 X("Das Risiko liegt bei uns, nicht beim Kunden.", "das REE-zee-koh leekt by oons, nikht bym KOON-den.", "The risk is with us, not the client.")],
                [("Es ist zwei Tage zu spät.", "Es kann zu zwei Tagen Verzögerung kommen.", "A warning names the possible delay, not the failure."),
                 ("Ich melde, dass alles gut ist.", "Ich melde frühzeitig: es kann zu einer Verzögerung kommen.", "An early warning carries the number.")]),
              [D("Herr Wolf", "Wie weit ist das Projekt?", "vee vite ist das pro-YEKT?", "How far along is the project?"),
               D("Max", "Ich melde frühzeitig: zwei Tage Verzögerung sind möglich.", "ikh MEL-duh FREW-tsy-tikh: tsvy TAH-guh fair-TSUR-guh-roong zint MURKH-likh.", "I'm reporting early: two days' delay are possible."),
               D("Herr Wolf", "Warum?", "var-OOM?", "Why?"),
               D("Max", "Die Daten vom Amt fehlen; das Risiko liegt nicht bei uns.", "dee DAH-ten fom amt FAY-len; das REE-zee-koh leekt nikht by oons.", "The data from the office is missing; the risk is not ours.")],
              WS("Warning worksheet", [
                  T("Give early warning.", ["two days' delay", "the data has not arrived", "the risk is not ours"],
                    ["zwei Tage Verzögerung sind möglich", "die Daten fehlen noch", "das Risiko liegt nicht bei uns"]),
                  T("Say when you will report again.", ["if it is more than two days"],
                    ["Wenn es mehr als zwei Tage sind, melde ich mich sofort."]),
              ])),
            L("Asking for more time, with a plan",
              "A German extension request arrives as a package: WENN SIE MIR DREI TAGE GEBEN, … · "
              "ALTERNATIV KANN ICH … · SO KANN ICH … The alternative is offered, not requested.",
              [V("die Frist", "dee frist", "deadline", "noun"),
               V("verlängern", "fair-LAYN-gern", "to extend", "verb"),
               V("alternativ", "al-ter-nah-TEEF", "alternatively", "adverb"),
               V("der Teil", "dair tile", "part, portion", "noun"),
               V("zusagen", "TSOO-zah-gen", "to commit", "verb")],
              G("Request + plan",
                "wenn Sie mir … geben, kann ich … · alternativ … · dann sage ich zu",
                "Wenn Sie mir drei Tage geben, ist alles fertig. Alternativ liefere ich heute die "
                "Hälfte. The request arrives with its price and its fallback in the same breath.",
                [X("Wenn Sie mir zwei Tage geben, ist es fertig.", "ven zee meer tsvy TAH-guh GAY-ben, ist es FAIR-tikh.", "If you give me two days, it will be done."),
                 X("Alternativ liefere ich heute die Hälfte.", "al-ter-nah-TEEF LEE-fuh-ruh ikh HOY-tuh dee HELF-tuh.", "Alternatively I deliver half today."),
                 X("Dann sage ich verbindlich zu.", "dan ZAH-guh ikh fair-BINT-likh tsoo.", "Then I commit bindingly.")],
                [("Geben Sie mir mehr Zeit.", "Wenn Sie mir zwei Tage geben, ist es fertig.", "The bare demand carries no plan."),
                 ("Ich kann nicht alles, aber nichts.", "Heute die Hälfte, in zwei Tagen der Rest.", "Alternatives need quantities.")]),
              [D("Lena", "Können Sie bis Mittwoch liefern?", "KUR-nen zee bis MIT-vokh LEE-fairn?", "Can you deliver by Wednesday?"),
               D("Max", "Wenn Sie mir drei Tage geben, ja. Alternativ: heute die Hälfte.", "ven zee meer dry TAH-guh GAY-ben, yah. al-ter-nah-TEEF: HOY-tuh dee HELF-tuh.", "If you give me three days, yes. Alternatively: half today."),
               D("Lena", "Was ist besser?", "vas ist BES-ser?", "Which is better?"),
               D("Max", "Heute die Hälfte — dann sehen Sie sofort etwas.", "HOY-tuh dee HELF-tuh — dan ZAY-en zee zoh-FOHRT ET-vas.", "Half today — then you see something immediately.")],
              WS("Negotiation worksheet", [
                  T("Ask for time with a plan.", ["three days → all of it", "two days → the rest"],
                    ["Wenn Sie mir drei Tage geben, ist alles fertig.", "Wenn Sie mir zwei Tage geben, kommt der Rest."]),
                  T("Offer an alternative.", ["half today", "the first part tonight"],
                    ["Alternativ liefere ich heute die Hälfte.", "Den ersten Teil heute Abend."]),
              ])),
            L("Closing the loop",
              "The last move confirms and hands over: DAS PROJEKT IST ABGESCHLOSSEN · DER BERICHT "
              "IST UNTERWEGS · BEI FRAGEN BIN ICH ERREICHBAR. Thanks, status, availability — three "
              "short sentences.",
              [V("abgeschlossen", "AP-ge-shlos-sen", "completed", "adjective"),
               V("unterwegs", "oon-ter-VAYKS", "on its way", "adverb"),
               V("erreichbar", "air-RYKH-bar", "reachable", "adjective"),
               V("die Übergabe", "dee EW-ber-gah-buh", "handover", "noun"),
               V("die Rückfrage", "dee REWK-frah-guh", "follow-up question", "noun")],
              G("Closing frames",
                "ist abgeschlossen · ist unterwegs · bei Fragen bin ich erreichbar",
                "Das Projekt ist abgeschlossen, der Bericht ist unterwegs. Bei Fragen bin ich "
                "erreichbar. The close offers availability and stops; it does not open a new "
                "queue.",
                [X("Das Projekt ist abgeschlossen.", "das pro-YEKT ist AP-ge-shlos-sen.", "The project is complete."),
                 X("Der Bericht ist unterwegs.", "dair beh-REEKHT ist OON-ter-vayks.", "The report is on its way."),
                 X("Bei Fragen bin ich erreichbar.", "by FRAH-gen bin ikh air-RYKH-bar.", "I'm available for questions.")],
                [("Das Projekt ist fast fertig, oder?", "Das Projekt ist abgeschlossen.", "A close is definite; «fast» belongs in the risk line."),
                 ("Ich habe noch eine Frage, und noch eine.", "Bei Fragen bin ich erreichbar.", "The close offers availability; it does not open the queue.")]),
              [D("Max", "Das Projekt ist abgeschlossen.", "das pro-YEKT ist AP-ge-shlos-sen.", "The project is complete."),
               D("Herr Wolf", "Und der Bericht?", "unt dair beh-REEKHT?", "And the report?"),
               D("Max", "Ist unterwegs. Die Übergabe machen wir Montag.", "ist OON-ter-vayks. dee EW-ber-gah-buh MAH-khen veer MOHN-tahk.", "Is on its way. We'll do the handover on Monday."),
               D("Herr Wolf", "Gut. Bei Fragen melde ich mich.", "goot. by FRAH-gen MEL-duh ikh mikh.", "Good. I'll get in touch with questions.")],
              WS("Closing worksheet", [
                  T("Close the loop.", ["it is done", "the report is on its way", "handover on Monday"],
                    ["Das Projekt ist abgeschlossen.", "Der Bericht ist unterwegs.", "Die Übergabe ist am Montag."]),
                  T("Offer availability and stop.", ["for questions"],
                    ["Bei Fragen bin ich erreichbar."]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("German professional life runs on the early, factual warning and the written "
                 "minute. A delay reported on day one with its number is ordinary management; the "
                 "same delay discovered at the deadline is a character fault. Small teams also "
                 "expect the closing loop — the short message that says «done, handed over, "
                 "available» — because without it the next person cannot start."),
        source_url="https://en.wikipedia.org/wiki/Business_etiquette",
        reading=("In der Sitzung am Mittwoch hat Max frühzeitig gemeldet: zwei Tage Verzögerung "
                 "seien möglich, weil die Daten vom Amt fehlen. Statt Kritik gab es eine "
                 "Entscheidung: heute die Hälfte, in drei Tagen der Rest. Das Protokoll hat drei "
                 "Zeilen: Beschluss, Grund, nächster Schritt. Ich habe gelernt, dass eine Frist "
                 "nicht durch Schweigen länger wird."),
        reading_gloss=("In Wednesday's meeting Max reported early that a two-day delay was possible "
                       "because the data from the office is missing. Instead of criticism there was "
                       "a decision: half today, the rest in three days. The minutes have three "
                       "lines: resolution, reason, next step. I learned that a deadline does not "
                       "get longer through silence."),
        listening=("Herr Wolf: Wie ist der Stand?<br>Max: Zwei Tage Verzögerung, ich melde es frühzeitig.<br>"
                   "Herr Wolf: Der Grund?<br>Max: Die Daten fehlen — das Risiko liegt nicht bei uns."),
        listening_gloss=("Mr Wolf: What is the status? Max: Two days' delay; I'm reporting it early. "
                         "Mr Wolf: The reason? Max: The data is missing — the risk is not ours."),
        voice_tag=VOICE,
        idioms=[
            ("Stand der Dinge", "state of things", "the current status"),
            ("Auf dem Laufenden", "on the running (track)", "up to date"),
            ("Ins Rollen bringen", "to set it rolling", "to get something going"),
            ("Über den Tisch", "across the table", "negotiated face to face"),
            ("Auf die lange Bank", "on the long bench", "shelved"),
            ("Am Ball bleiben", "to stay on the ball", "to stay on top of it"),
            ("Klare Kante", "clear edge", "a clear position"),
            ("Im Rahmen bleiben", "to stay within the frame", "to stay within limits"),
            ("Zugesagt ist zugesagt", "promised is promised", "a commitment is a commitment"),
            ("Ein Wort ein Mann", "a word, a man", "one's word is one's bond"),
        ],
        mistakes=[
            ("Es ist zwei Tage zu spät.", "Es kann zu zwei Tagen Verzögerung kommen.", "A warning names the possible delay, not the failure."),
            ("Geben Sie mir mehr Zeit.", "Wenn Sie mir zwei Tage geben, ist es fertig.", "A request for time travels with a plan."),
            ("Beschluss: vielleicht.", "Beschluss: Frist plus zwei Wochen.", "Minutes record decisions."),
        ],
        task_title="Run one meeting in German",
        task_instructions=("Take a real meeting — three people, twenty minutes — and run it entirely "
                           "in German: announce the agenda, qualify one commitment with a "
                           "condition, report one thing someone said, and close with the decision. "
                           "Then write minutes with four headings and send a three-line summary. If "
                           "the room switched to English, note which move it was — that is the "
                           "German you prepare next."),
    ),
    "test": [
        ("translate_en", "Say: We agree on one condition — the budget stays.", "Wir sagen unter einer Voraussetzung zu — das Budget bleibt."),
        ("translate_de", "Beschluss: Die Frist wird um zwei Wochen verlängert.", "Resolution: the deadline is extended by two weeks."),
        ("multiple_choice", "Which line sounds like early warning?", "Ich melde frühzeitig: zwei Tage Verzögerung sind möglich."),
        ("fill_in_the_blank", "Wir sagen unter der ___ zu, dass das Budget bleibt.", "Voraussetzung"),
        ("word_selection", "Select the German for 'alternatively'.", "alternativ"),
        ("error_correction", "Er hat gesagt, dass ich morgen komme.", "Er hat gesagt, dass er morgen kommt."),
        ("dialogue_completion", "Complete: Wenn Sie mir drei Tage geben, ___ (everything will be done)", "ist alles fertig"),
        ("matching", "Match Übergabe to its meaning.", "handover"),
        ("reading_comprehension", "Warum gab es keine Kritik?", "weil Max frühzeitig gemeldet hat"),
        ("inference", "«Eine Frist wird nicht durch Schweigen länger» — what does it mean?", "reporting delays early is the professional move"),
        ("main_idea", "Heute die Hälfte, in drei Tagen der Rest. What is this?", "a negotiated alternative"),
        ("detail_identification", "Wie viele Zeilen hat das Protokoll?", "drei"),
    ],
}

HALFSTEPS["C1+"] = {
    "title": "German C1+ — Almost native",
    "native": NATIVE,
    "goals": [
        "Use and recognise idioms, proverbs and images at the right moment",
        "Move between formal and colloquial registers inside one text",
        "Revise a paragraph for rhythm, precision and length",
    ],
    "units": [
        {"id": "C1+-U1", "title": "Idiom und Bild", "lessons": [
            L("Idioms that carry judgement",
              "German idioms judge in one image: DAS SAGT SCHON ALLES (that says it all), DAS GEHT "
              "AUF KEINE KUHHAUT (that won't fit on any cowhide — it is outrageous), WER'S GLAUBT "
              "(whoever believes it). One idiom replaces a paragraph of evaluation.",
              [V("das sagt schon alles", "das zahkt shohn AL-les", "that says it all", "phrase"),
               V("auf keine Kuhhaut gehen", "owf KY-nuh KOO-howt GAY-en", "to be outrageous", "idiom"),
               V("das ist bezeichnend", "das ist beh-TSYSH-nent", "that is telling", "phrase"),
               V("kennzeichnen", "KEN-tsysh-nen", "to characterise", "verb"),
               V("die Bewertung", "dee beh-VAIR-toong", "evaluation", "noun")],
              G("Idioms sit where an evaluator would sit",
                "subject + idiom + verb, and the tense follows the event",
                "Die Antwort sagt schon alles. Was da passiert ist, geht auf keine Kuhhaut. The "
                "idiom takes the place of a sentence about reaction or quality — and it stays in "
                "the register of the surrounding text.",
                [X("Diese Antwort sagt schon alles.", "DEE-zuh ANT-vort zahkt shohn AL-les.", "That answer says it all."),
                 X("Was da passiert ist, geht auf keine Kuhhaut.", "vas dah pas-SEERT ist, gayt owf KY-nuh KOO-howt.", "What happened there is outrageous."),
                 X("Das ist bezeichnend für den Stil.", "das ist beh-TSYSH-nent fewr dayn shteel.", "That is telling about the style.")],
                [("Das sagt alles schon, aber nichts.", "Das sagt schon alles.", "One idiom per judgement; stacking cancels the image."),
                 ("Auf keine Kuhhaut ist es.", "Es geht auf keine Kuhhaut.", "The idiom is a verb phrase: gehen auf.")]),
              [D("Lena", "Hast du seine Antwort gelesen?", "hast doo ZY-nuh ANT-vort ge-LAY-zen?", "Did you read his answer?"),
               D("Max", "Ja. Diese Antwort sagt schon alles.", "yah. DEE-zuh ANT-vort zahkt shohn AL-les.", "Yes. That answer says it all."),
               D("Lena", "Und die Zahlen darin?", "unt dee TSAH-len dah-RIN?", "And the figures in it?"),
               D("Max", "Was er da behauptet, geht auf keine Kuhhaut.", "vas air dah beh-HOWP-tet, gayt owf KY-nuh KOO-howt.", "What he claims there is outrageous.")],
              WS("Idiom worksheet", [
                  T("Choose the right idiom.", ["that says it all", "that is outrageous", "that is telling"],
                    ["Das sagt schon alles.", "Das geht auf keine Kuhhaut.", "Das ist bezeichnend."]),
                  T("Use it in a sentence.", ["the answer astonished everyone", "the claim is outrageous"],
                    ["Die Antwort sagt schon alles.", "Die Behauptung geht auf keine Kuhhaut."]),
              ])),
            L("Proverbs as arguments — and as decoration",
              "Proverbs are quoted in German and also reversed: DER APFEL FÄLLT NICHT WEIT VOM "
              "STAMM · ÜBUNG MACHT DEN MEISTER · WER ZU SPÄT KOMMT, DEN BESTRAFT DAS LEBEN. Quoting "
              "one is an argument by analogy, not a proof.",
              [V("der Apfel", "dair AP-fel", "apple", "noun"),
               V("der Stamm", "dair shtam", "trunk, stem", "noun"),
               V("die Übung", "dee EW-boong", "practice, exercise", "noun"),
               V("der Meister", "dair MY-ster", "master", "noun"),
               V("bestrafen", "beh-SHTRAH-fen", "to punish", "verb")],
              G("Proverb + frame",
                "proverb + denn / aber / und das heißt …",
                "Der Apfel fällt nicht weit vom Stamm — die Tochter führt die Firma genauso. Übung "
                "macht den Meister, aber nur die richtige Übung. The frame after the proverb is "
                "where the argument lives.",
                [X("Der Apfel fällt nicht weit vom Stamm.", "dair AP-fel felt nikht vite fom shtam.", "The apple does not fall far from the trunk."),
                 X("Übung macht den Meister, aber nur die richtige.", "EW-boong makht dayn MY-ster, AH-ber noor dee RIKH-ti-guh.", "Practice makes the master — but only the right practice."),
                 X("Wer zu spät kommt, den bestraft das Leben.", "vair tsoo shpayt komt, dayn beh-SHTRAHFT das LAY-ben.", "Life punishes those who come too late.")],
                [("Übung macht den Meister, also ist Üben bewiesen.", "Übung macht den Meister — die Daten zeigen es aber erst bei richtiger Übung.", "A proverb argues by analogy; evidence is still required."),
                 ("Wer zu spät kommt, deshalb kommen alle zu spät.", "Wer zu spät kommt, den bestraft das Leben — deshalb fährt der Zug pünktlich.", "The proverb should lead to a consequence, not to a slogan.")]),
              [D("Max", "Soll ich das Zitat streichen?", "zol ikh das tsi-TAHT SHRY-khen?", "Shall I cut the quotation?"),
               D("Lena", "Nicht das Zitat — die Behauptung danach.", "nikht das tsi-TAHT — dee beh-HOWP-toong dah-NAHKH.", "Not the quotation — the claim after it."),
               D("Max", "Also: «Übung macht den Meister» und dann?", "AL-zo: EW-boong makht dayn MY-ster unt dan?", "So: 'practice makes the master' and then?"),
               D("Lena", "Und dann ein Fall, wo es nicht stimmt.", "unt dan ine fal, voh es nikht shtimt.", "And then a case where it isn't true.")],
              WS("Proverb worksheet", [
                  T("Use the proverb that fits.", ["talent runs in the family", "practice is what gets you there"],
                    ["Der Apfel fällt nicht weit vom Stamm.", "Übung macht den Meister."]),
                  T("Add the argument.", ["a case where it does not hold"],
                    ["Aber nur, wenn die Übung richtig ist."]),
              ])),
            L("Metaphors that are alive in German",
              "Some images still work: DER MOTOR (drive), DAS FUNDAMENT (foundation), DER "
              "SEISMOGRAF (seismograph), DAS SCHARNIER (hinge), DER ANKER (anchor). A metaphor "
              "carries one claim and then steps aside.",
              [V("der Motor", "dair MOH-tor", "engine, motor", "noun"),
               V("das Fundament", "das foon-dah-MENT", "foundation", "noun"),
               V("das Scharnier", "das shar-NEER", "hinge", "noun"),
               V("der Anker", "dair AN-ker", "anchor", "noun"),
               V("das Gefüge", "das ge-FEW-guh", "structure, fabric", "noun")],
              G("Living image + concrete claim",
                "image + clause that states the claim",
                "Bildung ist der Motor der Wirtschaft — sie trägt, was die Zahlen messen. One "
                "image, one claim; three images in a paragraph compete and none lands.",
                [X("Bildung ist der Motor der Wirtschaft.", "BIL-doong ist dair MOH-tor dair VEER-shaft.", "Education is the engine of the economy."),
                 X("Vertrauen ist das Fundament jeder Zahl.", "fair-TROW-en ist das foon-dah-MENT YAY-der tsahl.", "Trust is the foundation of every figure."),
                 X("Diese Regel ist das Scharnier der Reform.", "DEE-zuh RAY-gel ist das shar-NEER dair re-FORM.", "This rule is the hinge of the reform.")],
                [("Bildung ist der Motor, das Fundament und der Anker.", "(one image, one claim)", "Three images in one sentence fight each other."),
                 ("Bildung ist like a motor.", "Bildung ist der Motor der Wirtschaft.", "Clear the English particle out; German uses the bare metaphor.")]),
              [D("Lena", "Der Absatz hat drei Bilder.", "dair AP-zats hat dry BIL-der.", "The paragraph has three images."),
               D("Max", "Zu viel?", "tsoo feel?", "Too much?"),
               D("Lena", "Ja — eins trägt, die anderen schmücken.", "yah — ines tairkt, dee AN-de-ren SHMEW-ken.", "Yes — one carries it, the others decorate."),
               D("Max", "Also streiche ich den Anker und den Seismografen.", "AL-zo SHRY-khuh ikh dayn AN-ker unt dayn zice-mo-GRAH-fen.", "So I cut the anchor and the seismograph.")],
              WS("Image worksheet", [
                  T("Use one living image.", ["education drives the economy", "trust underlies the figures"],
                    ["Bildung ist der Motor der Wirtschaft.", "Vertrauen ist das Fundament der Zahlen."]),
                  T("Trim competing images.", ["three metaphors in one paragraph"],
                    ["Eins trägt, der Rest fällt weg."]),
              ])),
        ]},
        {"id": "C1+-U2", "title": "Register rauf und runter", "lessons": [
            L("Formal prose: Amtsdeutsch without imitating it",
              "Formal German uses the passive and the Nominalstil: DIE PRÜFUNG ERFOLGT DURCH … · "
              "ES WIRD DARAUS HINGEWIESEN, DASS … The skill is to read it, and to choose "
              "deliberately when to write it.",
              [V("erfolgen", "air-FOL-gen", "to take place (formal)", "verb"),
               V("der Hinweis", "dair HIN-vice", "reference, hint", "noun"),
               V("die Prüfung", "dee PREW-foong", "examination, check", "noun"),
               V("die Gewährung", "dee ge-VAY-roong", "granting", "noun"),
               V("die Vorschrift", "dee FOHR-shrift", "regulation", "noun")],
              G("Formal register",
                "erfolgt durch … · wird darauf hingewiesen, dass … · gemäß Vorschrift",
                "Die Prüfung erfolgt durch das Amt. Es wird darauf hingewiesen, dass die Frist "
                "gemäß Vorschrift gilt. Nobody is named because the procedure is the subject.",
                [X("Die Prüfung erfolgt durch das Amt.", "dee PREW-foong air-FOLKT doorkh das amt.", "The check is carried out by the office."),
                 X("Es wird darauf hingewiesen, dass die Frist gilt.", "es vairt dah-ROWF HIN-ge-vee-zen, das dee frist gilt.", "Attention is drawn to the fact that the deadline applies."),
                 X("Gemäß Vorschrift gilt die Frist.", "ge-MAYS FOHR-shrift gilt dee frist.", "According to regulation the deadline applies.")],
                [("Sie werden prüfen das.", "Die Prüfung erfolgt durch Sie.", "Formal prose prefers the nominal passive over the addressed future."),
                 ("Es wird hingewiesen darauf, dass…", "Es wird darauf hingewiesen, dass …", "The preposition belongs before the verb particle.")]),
              [D("Autor", "Klingt der Satz zu amtlich?", "klingt dair zats tsoo AMT-likh?", "Does the sentence sound too official?"),
               D("Lektor", "Die Prüfung erfolgt durch die Kommission — ja, sehr amtlich.", "dee PREW-foong air-FOLKT doorkh dee kom-mis-YOHN — yah, zair AMT-likh.", "The check is carried out by the commission — yes, very official."),
               D("Autor", "Also aktiver?", "AL-zo ak-TEE-ver?", "So more active?"),
               D("Lektor", "Die Kommission prüft — ein Drittel der Wörter, ein Akteur.", "dee kom-mis-YOHN prewft — ine DRIT-tel dair VUR-ter, ine ak-TUR.", "The commission checks — a third of the words, one actor.")],
              WS("Formal worksheet", [
                  T("Make it formal.", ["we check it", "attention is drawn to the deadline", "as per regulation"],
                    ["Die Prüfung erfolgt durch uns.", "Es wird auf die Frist hingewiesen.", "gemäß Vorschrift"]),
                  T("Make it active again.", ["(rewrite without the passive)"],
                    ["Die Kommission prüft die Unterlagen."]),
              ])),
            L("Colloquial prose: short, direct, warm",
              "Colloquial German drops the middle field and the particles multiply: ECHT JETZT? · "
              "DAS IST DOCH BLÖDSINN · KRIEGST DU DAS HIN? Nothing here is wrong — it is a "
              "different room.",
              [V("echt jetzt?", "ekht yetst?", "seriously?", "phrase"),
               V("doch", "dokh", "surely, after all", "particle"),
               V("der Blödsinn", "dair BLURT-zin", "nonsense", "noun"),
               V("hinkriegen", "HIN-kree-gen", "to manage, pull off", "verb"),
               V("krass", "kras", "extreme, wild (colloquial)", "adjective")],
              G("Colloquial register",
                "particles (doch, ja, mal, halt) + short clauses + contractions",
                "Kriegst du das bis morgen hin? — Klar, das ist doch kein Problem. The "
                "contractions (kriegen + hin, 'n Kaffee) and the particles are what make speech "
                "sound native; the register is carried by rhythm as much as by words.",
                [X("Kriegst du das hin?", "KREEKST doo das hin?", "Can you pull that off?"),
                 X("Das ist doch kein Problem.", "das ist dokh kine pro-BLEEM.", "That's no problem at all."),
                 X("Echt jetzt? Das ist krass.", "ekht yetst? das ist kras.", "Seriously? That's wild.")],
                [("Das ist kein Problem doch.", "Das ist doch kein Problem.", "Particles sit before the negation, not after it."),
                 ("Kriegst du hin das?", "Kriegst du das hin?", "Separable prefix to the end, object in the middle.")]),
              [D("Max", "Kriegst du das bis morgen hin?", "KREEKST doo das bis MOR-gen hin?", "Can you get that done by tomorrow?"),
               D("Lena", "Klar, das ist doch kein Problem.", "klar, das ist dokh kine pro-BLEEM.", "Sure, that's no problem at all."),
               D("Max", "Echt? Du bist krass, danke!", "ekht? doo bist kras, DAN-kuh!", "Really? You're amazing, thanks!"),
               D("Lena", "Übertreib mal nicht. Bis morgen.", "ew-ber-TRYP mahl nikht. bis MOR-gen.", "Don't exaggerate. See you tomorrow.")],
              WS("Colloquial worksheet", [
                  T("Make it colloquial.", ["can you pull that off?", "that's no problem", "seriously?"],
                    ["Kriegst du das hin?", "Das ist doch kein Problem.", "Echt jetzt?"]),
                  T("Use a particle.", ["don't exaggerate", "that's surely clear"],
                    ["Übertreib mal nicht.", "Das ist ja klar."]),
              ])),
            L("Switching register inside one text",
              "A good German text can move registers: formal in the argument, colloquial in the "
              "example, formal again at the close. The switch is marked by the verb form and by a "
              "boundary — a new paragraph, a dash, or «mit anderen Worten».",
              [V("die Wendung", "dee VEN-doong", "turn of phrase", "noun"),
               V("der Wechsel", "dair VEK-sel", "switch, change", "noun"),
               V("mit anderen Worten", "mit AN-de-ren VUR-ten", "in other words", "phrase"),
               V("die Ebene", "dee AY-beh-nuh", "level, plane", "noun"),
               V("bewusst", "beh-VOOST", "deliberate", "adjective")],
              G("Register switch = marked boundary",
                "formal → «mit anderen Worten» → colloquial → new paragraph → formal",
                "Die Prüfung erfolgt durch die Kommission. Mit anderen Worten: Daumen drücken. "
                "Im nächsten Absatz kehrt der Text zum Verfahren zurück. The switch is signalled, "
                "never accidental.",
                [X("Mit anderen Worten: Daumen drücken.", "mit AN-de-ren VUR-ten: DOW-men DREW-ken.", "In other words: fingers crossed."),
                 X("Der Wechsel ist bewusst gesetzt.", "dair VEK-sel ist beh-VOOST ge-ZETST.", "The switch is placed deliberately."),
                 X("Auf der nächsten Ebene wird es wieder förmlich.", "owf dair NAYS-ten AY-beh-nuh vairt es vee-der FURM-likh.", "At the next level it becomes formal again.")],
                [("Alles ist amtlich, auch der Witz. (accidental)", "Der Witz ist markiert, der Rahmen bleibt amtlich.", "An unmarked switch reads as a mistake, not style."),
                 ("Mit anderen Worten, und trotzdem dasselbe.", "Mit anderen Worten: …", "The phrase announces a shift; it must actually shift.")]),
              [D("Lektor", "Der Text springt.", "dair tekst shpringt.", "The text jumps."),
               D("Autorin", "Bewusst — erst Verfahren, dann Alltag, dann Fazit.", "beh-VOOST — airst fair-FAH-ren, dan AL-tahk, dan fah-TSEET.", "Deliberately — procedure first, then everyday, then the conclusion."),
               D("Lektor", "Und der Übergang?", "unt dair EW-ber-gang?", "And the transition?"),
               D("Autorin", "«Mit anderen Worten» — dann ist der Sprung ein Schritt.", "mit AN-de-ren VUR-ten — dan ist dair shproong ine shrit.", "'In other words' — then the jump becomes a step.")],
              WS("Switch worksheet", [
                  T("Plan the registers.", ["argument → example → close"],
                    ["amtlich → alltäglich → amtlich"]),
                  T("Mark the boundary.", ["return to the argument"],
                    ["Neuer Absatz, dann wieder förmlich."]),
              ])),
        ]},
        {"id": "C1+-U3", "title": "Besser sagen", "lessons": [
            L("Rhythm: long line, short line",
              "German prose breathes with alternating length. A long qualification followed by a "
              "three-word sentence is a native rhythm: DIE FRIST IST KNAPP, ABER MACHBAR. — ZWEI "
              "WOCHEN REICHEN.",
              [V("der Rhythmus", "dair REWT-moos", "rhythm", "noun"),
               V("knapp", "knap", "tight, scarce", "adjective"),
               V("machbar", "MAKH-bar", "doable", "adjective"),
               V("die Pointe", "dee pwan-tuh", "punchline", "noun"),
               V("der Einschnitt", "dair INE-shnit", "break, caesura", "noun")],
              G("Alternate length deliberately",
                "long clause + short clause, emphasis last",
                "Wer die Zahlen liest, sieht ein Muster: es wird knapper. German lands the point "
                "in the shortest sentence, after the longest one. The colon and the full stop are "
                "rhythmic instruments.",
                [X("Die Frist ist knapp, aber machbar.", "dee frist ist knap, AH-ber MAKH-bar.", "The deadline is tight but doable."),
                 X("Zwei Wochen reichen.", "tsvy VOKH-en RY-khen.", "Two weeks are enough."),
                 X("Ein Muster: es wird knapper.", "ine MOOS-ter: es vairt KNAP-per.", "A pattern: it is getting tighter.")],
                [("Die Frist ist knapp, und zwei Wochen reichen nicht, aber eigentlich reichen sie.", "(one rhythm per paragraph)", "Repeating the same beat makes prose mechanical."),
                 ("Alles ist knapp, eng, kurz, schwierig.", "Die Frist ist knapp.", "Lists flatten the emphasis the rhythm was carrying.")]),
              [D("Lektor", "Lesen Sie den Absatz einmal laut.", "LAY-zen zee dayn AP-zats INE-mahl lowt.", "Read the paragraph aloud once."),
               D("Autorin", "Wer die Zahlen liest, sieht ein Muster, und das Muster ist, dass es immer knapper wird.", "vair dee TSAH-len leest, zeet ine MOOS-ter, unt das MOOS-ter ist, das es IM-mer KNAP-per vairt.", "Whoever reads the figures sees a pattern, and the pattern is that it keeps getting tighter."),
               D("Lektor", "Und kurz?", "unt koorts?", "And short?"),
               D("Autorin", "Ein Muster: es wird knapper.", "ine MOOS-ter: es vairt KNAP-per.", "A pattern: it is getting tighter.")],
              WS("Rhythm worksheet", [
                  T("Make the sentence land.", ["long clause: the deadline is tight but doable", "(three-word close): two weeks are enough"],
                    ["Die Frist ist knapp, aber machbar.", "Zwei Wochen reichen."]),
                  T("Trim the connectives.", ["the deadline is tight, and two weeks are enough, but it is hard"],
                    ["Die Frist ist knapp. Zwei Wochen reichen."]),
              ])),
            L("Precision: replace the vague verb",
              "Vague verbs hide weak thinking: machen, haben, sein, geben. German alternatives are "
              "concrete: FESTLEGEN (fix), ZUSICHERN (assure), ÜBERGEBEN (hand over), VORANTREIBEN "
              "(drive forward), ZURÜCKFÜHREN (trace back).",
              [V("festlegen", "FEST-lay-gen", "to fix, determine", "verb"),
               V("zusichern", "TSOO-zi-khern", "to assure, promise", "verb"),
               V("übergeben", "ew-ber-GAY-ben", "to hand over", "verb"),
               V("vorantreiben", "fohr-AN-try-ben", "to drive forward", "verb"),
               V("zurückführen auf", "tsoo-REWK-few-ren owf", "to trace back to", "phrase")],
              G("Concrete verb beats machen",
                "machen → festlegen · geben → zusichern / übergeben · sein → beruhen auf",
                "Der Termin wurde festgelegt (not: mit dem Termin wurde etwas gemacht). Die "
                "Zahlen beruhen auf einer Stichprobe (not: die Zahlen sind von einer Stichprobe). "
                "The concrete verb names the action and saves the reader a question.",
                [X("Der Termin wurde festgelegt.", "dair ter-MEEN VOOR-duh FEST-ge-laykt.", "The date was fixed."),
                 X("Die Wirkung lässt sich auf zwei Ursachen zurückführen.", "dee VEER-koong lest zikh owf tsvy OOR-zah-khen tsoo-REWK-few-ren.", "The effect can be traced back to two causes."),
                 X("Wir sichern die Lieferung zu.", "veer ZEE-khern dee LEE-fuh-roong tsoo.", "We assure the delivery.")],
                [("Mit dem Termin wurde etwas gemacht.", "Der Termin wurde festgelegt.", "«etwas gemacht» names nothing."),
                 ("Die Zahlen sind von einer Stichprobe.", "Die Zahlen beruhen auf einer Stichprobe.", "The relation needs its own verb.")]),
              [D("Lektor", "«Es wurde etwas gemacht» — was heißt das?", "es VOOR-duh ET-vas ge-MAKHT — vas hyst das?", "'Something was done' — what does that mean?"),
               D("Autor", "Zu wenig. Ich schreibe: Der Termin wurde festgelegt.", "tsoo VAY-nikh. ikh SHRY-buh: dair ter-MEEN VOOR-duh FEST-ge-laykt.", "Too little. I'll write: the date was fixed."),
               D("Lektor", "Und «die Zahlen»?", "unt dee TSAH-len?", "And 'the figures'?"),
               D("Autor", "Sie beruhen auf einer Stichprobe von zweitausend Fällen.", "zee beh-ROO-en owf EYE-ner SHTIKH-proh-buh fon TSVY-tow-zent FEL-len.", "They rest on a sample of two thousand cases.")],
              WS("Precision worksheet", [
                  T("Replace the vague verb.", ["something was done about the date", "the figures were given", "the plan was moved forward"],
                    ["Der Termin wurde festgelegt.", "Die Zahlen wurden vorgelegt.", "Der Plan wurde vorangetrieben."]),
                  T("Make it concrete.", ["the effect comes from two causes"],
                    ["Die Wirkung lässt sich auf zwei Ursachen zurückführen."]),
              ])),
            L("Revising your own paragraph",
              "German revision has four cuts: nominalise where a term is needed, verbalise where a "
              "human must act, order decision first, and read it aloud. A revised paragraph is "
              "usually a third shorter.",
              [V("die Überarbeitung", "dee ew-ber-AR-by-toong", "revision", "noun"),
               V("kürzen", "KEWR-tsen", "to shorten", "verb"),
               V("die Reihenfolge", "dee RY-en-fol-guh", "order", "noun"),
               V("vorlesen", "FOHR-lay-zen", "to read aloud", "verb"),
               V("streichen", "SHRY-khen", "to cut, strike out", "verb")],
              G("Four cuts",
                "nominalise · verbalise · decision first · read aloud",
                "Aus «Wir haben nach langer Diskussion entschieden, dass die Frist verlängert "
                "wird» wird «Beschluss: Die Frist wird um zwei Wochen verlängert.» — a third of "
                "the words, all of the meaning.",
                [X("Beschluss: Die Frist wird verlängert.", "beh-SHLUS: dee frist vairt fair-LAYN-gert.", "Resolution: the deadline is extended."),
                 X("Grund: Zwei Zulieferer fehlen.", "groont: tsvy TSOO-lee-fuh-rer FAY-len.", "Reason: two suppliers are missing."),
                 X("Nächster Schritt: Montag, zehn Uhr.", "NAYS-ter shrit: MOHN-tahk, tsehn oor.", "Next step: Monday, ten o'clock.")],
                [("Nach langer Diskussion wurde entschieden, dass…", "Beschluss: …", "The frame belongs to the draft, not to the text."),
                 ("Die Überarbeitung wurde länger.", "Die Überarbeitung wurde kürzer.", "A revision shortens; if it grew, it was a rewrite.")]),
              [D("Lektor", "Dritte Fassung?", "DRIT-tuh FAS-soong?", "Third version?"),
               D("Autorin", "Ja — ein Drittel kürzer, und der Beschluss steht vorn.", "yah — ine DRIT-tel KEWR-tser, unt dair beh-SHLUS shtayt forn.", "Yes — a third shorter, and the decision stands first."),
               D("Lektor", "Und vorgelesen?", "unt FOHR-ge-lay-zen?", "And read aloud?"),
               D("Autorin", "Zweimal. Wo ich Luft holen musste, habe ich gestrichen.", "TSVY-mahl. voh ikh looft HOH-len MOOS-tuh, HAH-buh ikh ge-SHRI-khen.", "Twice. Where I had to take a breath, I cut.")],
              WS("Revision worksheet", [
                  T("Cut the frame.", ["after long discussion we decided that the deadline will change"],
                    ["Beschluss: Die Frist wird verlängert."]),
                  T("Order it.", ["reason, decision, next step"],
                    ["Beschluss, Grund, nächster Schritt"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("German idiom lives in quotation and reversal: an essay borrows a proverb or a "
                 "classical phrase, turns it, and the turn is the argument. C1 learners are "
                 "expected both to catch the borrowed register and to refuse it where it replaces "
                 "evidence — «Der Apfel fällt nicht weit vom Stamm» is a nice sentence and a poor "
                 "proof. The same reflex applies to Amtsdeutsch: reading it without imitating it "
                 "is the mark of the level."),
        source_url="https://en.wikipedia.org/wiki/Register_(sociolinguistics)",
        reading=("Der Lektor sagte: «Der Text springt.» Ich habe zwei Absätze gestrichen und einen "
                 "Satz wiederholt: «Übung macht den Meister — aber nur die richtige Übung.» Plötzlich "
                 "war der Absatz ein Drittel kürzer, und der Widerspruch trug den Gedanken. Früher "
                 "hätte ich das Zitat gelassen und die Behauptung danach geschrieben; jetzt drehe "
                 "ich es um. Ich habe gelernt, dass eine Überarbeitung nicht mehr Wörter braucht, "
                 "sondern weniger."),
        reading_gloss=("The editor said: 'The text jumps.' I cut two paragraphs and repeated one "
                       "sentence: 'Practice makes the master — but only the right practice.' "
                       "Suddenly the paragraph was a third shorter, and the contradiction carried "
                       "the thought. Earlier I would have left the quotation and written the claim "
                       "after it; now I reverse it. I learned that a revision does not need more "
                       "words but fewer."),
        listening=("Autorin: Klingt der Absatz zu amtlich?<br>Lektor: Die Prüfung erfolgt durch die Kommission — ja.<br>"
                   "Autorin: Dann aktiver: die Kommission prüft.<br>Lektor: Besser — ein Drittel der Wörter, ein Akteur."),
        listening_gloss=("Author: Does the paragraph sound too official? Editor: 'The check is "
                         "carried out by the commission' — yes. Author: Then more active: the "
                         "commission checks. Editor: Better — a third of the words, one actor."),
        voice_tag=VOICE,
        idioms=[
            ("Auf den Punkt bringen", "to bring to the point", "to state it precisely"),
            ("Den Kern treffen", "to hit the core", "to get to the heart of it"),
            ("Um den heißen Brei", "around the hot porridge", "beating about the bush"),
            ("Das Ruder herumreißen", "to yank the rudder", "to turn things around"),
            ("Einen Schlussstrich ziehen", "to draw a closing line", "to draw a line under it"),
            ("Im Kern", "in the core", "at bottom, essentially"),
            ("Wort für Wort", "word for word", "verbatim"),
            ("Zwischen den Zeilen", "between the lines", "between the lines"),
            ("Sich verrennen", "to run oneself wrong", "to get stuck on a wrong track"),
            ("Bild für Bild", "image for image", "image by image"),
        ],
        mistakes=[
            ("Übung macht den Meister, also ist Üben bewiesen.", "Übung macht den Meister — bewiesen ist damit nichts.", "A proverb argues by analogy; evidence is still required."),
            ("Mit dem Termin wurde etwas gemacht.", "Der Termin wurde festgelegt.", "«etwas gemacht» names nothing."),
            ("Die Überarbeitung wurde länger.", "Die Überarbeitung wurde kürzer.", "Revision shortens; length was the draft's problem."),
        ],
        task_title="Revise one paragraph three times",
        task_instructions=("Take any paragraph you have written in German and revise it three "
                           "times: cut the frames («nach langer Diskussion …»), replace every vague "
                           "machen/haben/sein with a concrete verb, and put the decision first. "
                           "Compare the lengths. Then read the final version aloud — where your "
                           "voice runs out of breath the sentence is too long, and where you "
                           "stumble the register changed without a boundary."),
    ),
    "test": [
        ("translate_en", "Say: The deadline is tight, but doable. Two weeks are enough.", "Die Frist ist knapp, aber machbar. Zwei Wochen reichen."),
        ("translate_de", "Diese Antwort sagt schon alles.", "That answer says it all."),
        ("multiple_choice", "Which is the formal close?", "Beschluss: Die Frist wird verlängert."),
        ("fill_in_the_blank", "Übung macht den ___.", "Meister"),
        ("word_selection", "Select the German for 'to hand over'.", "übergeben"),
        ("error_correction", "Mit dem Termin wurde etwas gemacht.", "Der Termin wurde festgelegt."),
        ("dialogue_completion", "Complete: Übertreib mal nicht, ___ (see you tomorrow)", "bis morgen"),
        ("matching", "Match Rhythmus to its meaning.", "rhythm"),
        ("reading_comprehension", "Warum wurde der Absatz kürzer?", "weil zwei Absätze gestrichen wurden"),
        ("inference", "«Eine Überarbeitung braucht weniger, nicht mehr Wörter» — what does the editor mean?", "cutting improves the text more than adding"),
        ("main_idea", "Die Prüfung erfolgt durch die Kommission → die Kommission prüft. What changed?", "the register, not the content"),
        ("detail_identification", "Wie viel kürzer ist der Absatz geworden?", "ein Drittel"),
    ],
}

# -*- coding: utf-8 -*-
"""Spanish PHASE 1 depth — extras, third lessons, half-step rungs.

Written with the DSL in `tools/depth_kit.py`; rendered by
`tools/author-depth.py --lang es`.

House style follows the shipped Spanish course: standard peninsular Spanish
with the course's own romanisation (stressed syllable in CAPITALS, syllables
hyphenated), speakers Ana and Ben, and unit ids in the course's own shape
(`A1-U1` for the CEFR rungs, `es-c1-u1` for C1/C2). Half-step rungs use
`<rung>-U1`, e.g. `A1+-U1`, so a lesson id is unique across all sixteen files.

Register note: the dialogues between Ana and Ben use `tú`; every exchange with
an older speaker, a stranger or an official uses `usted`, and the half-step B1+
teaches the switch (`¿nos tuteamos?`). Peninsular `vosotros` is taught as the
plural of `tú`; Latin-American `ustedes` is named where it differs, because the
course is read on both sides of the Atlantic.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # tools/ on the path
from depth_kit import D, EXTRA, G, L, T, V, WS, X   # noqa: E402

CODE = "es"
NAME = "Spanish"
NATIVE = "Español"
PHASE = 1
SCRIPT = "Spanish"
VOICE = "es-ES"
SKILL = ("Spanish: verb conjugation across three moods, ser/estar and por/para splits, "
         "object-pronoun placement, subjunctive in subordinate clauses, and the tú/usted "
         "register decision — measured by choosing the right form before producing the sentence.")

EXTRAS = {}
THIRD = {}
HALFSTEPS = {}


# ── the six CEFR rungs ──────────────────────────────────────────────────────

EXTRAS["A1"] = EXTRA(
    culture=("Spanish carries two second persons and a whole social grammar with them: tú for "
             "friends, family, students and anyone who has offered it; usted for strangers, "
             "officials, older people and most first meetings. Unlike German, the verb form makes "
             "the choice audible in every sentence (hablas / habla), so a learner who guesses is "
             "heard immediately — which is why A1 drills both from the first lesson."),
    source_url="https://en.wikipedia.org/wiki/Spanish_language",
    reading=("Ana llega nueva a la clase. Dice: «Hola, me llamo Ana. ¿Y tú?» Ben contesta: «Yo soy "
             "Ben. ¿De dónde eres?» — «De Sevilla. ¿Y tú?» — «De México.» Entra el profesor y "
             "dice: «Buenos días. Yo soy el señor García.» Todos dicen: «Buenos días, señor "
             "García.»"),
    reading_gloss=("Ana arrives new to the class. She says: 'Hello, my name is Ana. And you?' Ben "
                   "answers: 'I am Ben. Where are you from?' — 'From Seville. And you?' — 'From "
                   "Mexico.' The teacher comes in and says: 'Good morning. I am Mr García.' "
                   "Everyone says: 'Good morning, Mr García.'"),
    listening=("Ana: ¡Hola! Me llamo Ana. ¿Y tú?<br>Ben: Yo soy Ben. ¿Cómo estás?<br>"
               "Ana: Bien, gracias. ¿Y tú?<br>Ben: Bien también. ¿De dónde eres?"),
    listening_gloss=("Ana: Hello! My name is Ana. And you? Ben: I am Ben. How are you? Ana: Fine, "
                     "thanks. And you? Ben: Fine too. Where are you from?"),
    voice_tag=VOICE,
    idioms=[
        ("Buenos días", "good days", "good morning"),
        ("Buenas tardes", "good afternoons", "good afternoon"),
        ("Por favor", "by favour", "please"),
        ("Mucho gusto", "much pleasure", "pleased to meet you"),
        ("¿Qué tal?", "what such?", "how's it going?"),
        ("Hasta luego", "until later", "see you later"),
        ("Lo siento", "I feel it", "I'm sorry"),
        ("Con permiso", "with permission", "excuse me (passing through)"),
        ("Bienvenido", "well-come", "welcome"),
        ("Que te vaya bien", "may it go well for you", "take care"),
    ],
    mistakes=[
        ("Yo soy bien.", "Yo estoy bien.", "Feelings and states take estar; ser would describe a permanent quality."),
        ("Me llamo es Ana.", "Me llamo Ana. / Soy Ana.", "llamarse already carries the verb; two verbs in one sentence."),
        ("¿Cómo estás? (to a professor you have just met)", "¿Cómo está usted?", "First meetings take usted; tú is offered, not assumed."),
    ],
    task_title="Introduce yourself twice",
    task_instructions=("Write the same introduction twice in Spanish: once to a classmate (tú) and "
                       "once to a professor's secretary at a first meeting (usted, surname). Read "
                       "both aloud. Then change one word and check that the whole sentence still "
                       "agrees — the verb ending, the possessive and the greeting all follow the "
                       "person you chose, and a mixed pair is what a listener hears first."),
)

EXTRAS["A2"] = EXTRA(
    culture=("Spanish eating has a rhythm of its own: the mid-morning almuerzo, the late comida "
             "around two, and the sobremesa — the time after eating when nobody moves and the talk "
             "continues. Tapas are not a starter but a way of eating: small plates shared, ordered "
             "in rounds. A2 covers ordering because the phrases are short and real, and the "
             "cultural note is that «quedarse de sobremesa» is a compliment to the table, never a "
             "delay."),
    source_url="https://en.wikipedia.org/wiki/Spanish_cuisine",
    reading=("A las dos comemos. En la mesa hay pan, tortilla y ensalada. Mi madre pregunta: "
             "«¿Quieres más?» Yo digo: «No, gracias, estoy lleno.» Luego nos quedamos de "
             "sobremesa: café, charla y ninguna prisa. Por la noche vamos de tapas: dos raciones, "
             "una caña y la cuenta, que son nueve euros."),
    reading_gloss=("At two o'clock we eat. On the table there is bread, tortilla and salad. My "
                   "mother asks: 'Do you want more?' I say: 'No thanks, I'm full.' Then we stay "
                   "over the sobremesa: coffee, talk and no hurry. At night we go for tapas: two "
                   "portions, a small beer and the bill, which is nine euros."),
    listening=("Ben: ¿Qué quieres tomar?<br>Ana: Una caña, por favor.<br>"
               "Ben: ¿Y para comer?<br>Ana: Una ración de tortilla. Y la cuenta, cuando puedas."),
    listening_gloss=("Ben: What would you like to drink? Ana: A small beer, please. Ben: And to "
                     "eat? Ana: A portion of tortilla. And the bill, when you can."),
    voice_tag=VOICE,
    idioms=[
        ("Tengo hambre", "I have hunger", "I am hungry"),
        ("Está para chuparse los dedos", "it is to lick one's fingers", "it's delicious"),
        ("Ponerse las botas", "to put on the boots", "to eat one's fill"),
        ("Tomar algo", "to take something", "to have a drink"),
        ("La cuenta, por favor", "the bill, please", "the bill, please"),
        ("Para llevar", "to take away", "takeaway"),
        ("¿Me trae…?", "will you bring me…?", "could you bring me…?"),
        ("De primero y de segundo", "as first and second", "first and main course"),
        ("Estar lleno", "to be full", "to be full"),
        ("Invito yo", "I invite", "it's on me"),
    ],
    mistakes=[
        ("Quiero un café, por favor. (to a waiter, first contact)", "Quisiera un café, por favor.", "Quisiera is the polite request; quiero sounds blunt to a stranger."),
        ("Soy hambre.", "Tengo hambre.", "Hunger is had: tener, not ser."),
        ("La cuenta, cuando puedes. (to a waiter)", "La cuenta, cuando pueda.", "The polite frame takes usted: cuando pueda."),
    ],
    task_title="Order at a bar",
    task_instructions=("Write an eight-line bar dialogue in Spanish: greet, order a drink, order "
                       "food, ask for the bill, pay, say goodbye. Use «quisiera» once, «por favor» "
                       "twice, and no English. Then change the order to two people — «¿algo para "
                       "picar?» — which forces the plural forms and is where learners slip from "
                       "tú to vosotros (or ustedes, on the American side)."),
)

EXTRAS["B1"] = EXTRA(
    culture=("The Spanish working day still bends around the middle of the day: a long lunch, "
             "often at home, and business that runs into the evening. The siesta is not laziness "
             "but the shape of a climate and a timetable; in the cities it has shrunk to a short "
             "pause, while the evening meeting and the late dinner remain. B1 needs the vocabulary "
             "because work is the first place a learner is asked about plans in a register that is "
             "neither home nor classroom."),
    source_url="https://en.wikipedia.org/wiki/Siesta",
    reading=("Ana trabaja en una oficina en Sevilla. «Entro a las ocho y salgo a las tres», dice. "
             "«Luego como en casa y duermo veinte minutos.» Por la tarde vuelve al trabajo si hay "
             "una reunión con clientes de América: «A las siete hablamos con México, así que la "
             "tarde es larga.» Después cursa una formación: «Quiero cambiar de departamento el año "
             "que viene.»"),
    reading_gloss=("Ana works in an office in Seville. 'I start at eight and leave at three,' she "
                   "says. 'Then I eat at home and sleep twenty minutes.' In the afternoon she goes "
                   "back to work if there is a meeting with clients from America: 'At seven we talk "
                   "to Mexico, so the afternoon is long.' Afterwards she takes a training course: "
                   "'I want to change department next year.'"),
    listening=("Jefe: ¿Qué tal va el proyecto?<br>Ben: Bien, pero necesito dos días más.<br>"
               "Jefe: ¿Y eso?<br>Ben: Los datos del cliente llegan tarde. Se lo digo ahora para que no haya sorpresas."),
    listening_gloss=("Boss: How is the project going? Ben: Well, but I need two more days. Boss: "
                     "Why? Ben: The client's data arrives late. I'm telling you now so there are "
                     "no surprises."),
    voice_tag=VOICE,
    idioms=[
        ("Estar hecho polvo", "to be made dust", "to be exhausted"),
        ("Echar una mano", "to throw a hand", "to lend a hand"),
        ("Meter la pata", "to put the paw in", "to put one's foot in it"),
        ("Quedarse de sobremesa", "to stay for the sobremesa", "to linger at the table"),
        ("No dar abasto", "not to give enough", "to be swamped"),
        ("Ir al grano", "to go to the grain", "to get to the point"),
        ("Ponerse las pilas", "to put in the batteries", "to get a move on"),
        ("Tener prisa", "to have haste", "to be in a hurry"),
        ("Salir del paso", "to get out of the step", "to get by, to muddle through"),
        ("Dormir la siesta", "to sleep the siesta", "to take a midday nap"),
    ],
    mistakes=[
        ("Tengo 25 años y trabajo aquí desde tres años.", "Tengo 25 años y trabajo aquí desde hace tres años.", "Duration takes desde hace; desde alone marks a point in time."),
        ("Estoy de acuerdo contigo, pero pienso que no es posible el plan.", "… pero creo que el plan no es posible.", "Spanish prefers the negative before the verb and the subject after it."),
        ("Mañana yo iré a trabajar y después yo comeré.", "Mañana iré a trabajar y después comeré.", "Pronouns are dropped when the verb ending already carries the person."),
    ],
    task_title="Describe your working life in ninety seconds",
    task_instructions=("Record ninety seconds in Spanish about what you do and what comes next: "
                       "current job or study, one thing that was hard at the start, one plan for "
                       "next year. Use one «desde hace», one «para que + subjunctive» and one "
                       "reflexive verb. Listen back and count the sentences where the verb ending "
                       "and the subject disagree — those are the ones to rewrite."),
)

EXTRAS["B2"] = EXTRA(
    culture=("Spanish argument lives in the tertulia — the regular gathering where talk is the "
             "point, and disagreement is expected to be lively and personal without being rude. "
             "In writing the tone drops: an opinion piece can concede in the first paragraph "
             "(«es cierto que…») and then rebut at length, because the concession is read as "
             "seriousness rather than weakness. B2 teaches that register: concede, qualify, "
             "rebut, propose."),
    source_url="https://en.wikipedia.org/wiki/Tertulia",
    reading=("«Es cierto que la medida es popular», escribe la columnista, «pero también es "
             "cierta una cosa: nadie ha medido su coste.» En la tertulia de la radio la "
             "discusión sigue el mismo patrón: primero se concede, después se matiza y solo al "
             "final se propone. Alguien dice: «A mí me da la impresión de que el problema no es "
             "la norma, sino cómo se aplica.» Y todos están de acuerdo."),
    reading_gloss=("'It is true that the measure is popular,' writes the columnist, 'but one "
                   "thing is also true: nobody has measured its cost.' On the radio tertulia the "
                   "discussion follows the same pattern: first concede, then qualify, and only at "
                   "the end propose. Someone says: 'It seems to me that the problem is not the "
                   "rule but how it is applied.' And everyone agrees."),
    listening=("Moderador: ¿Le parece bien la medida?<br>Ana: En principio sí, aunque tengo dudas.<br>"
               "Moderador: ¿Cuáles?<br>Ana: No está claro cómo se va a financiar. Por eso propongo medirlo antes."),
    listening_gloss=("Moderator: Do you think the measure is a good idea? Ana: In principle yes, "
                     "although I have doubts. Moderator: Which ones? Ana: It is not clear how it "
                     "will be financed. That is why I propose measuring it first."),
    voice_tag=VOICE,
    idioms=[
        ("Ir al grano", "to go to the grain", "to get to the point"),
        ("Ponerse el mundo por montera", "to put the world as a hat", "to throw caution to the wind"),
        ("Ser pan comido", "to be eaten bread", "to be a piece of cake"),
        ("Estar en el ajo", "to be in the garlic", "to be in the know"),
        ("Hacer la vista gorda", "to make the fat view", "to turn a blind eye"),
        ("Tirar la casa por la ventana", "to throw the house out of the window", "to spare no expense"),
        ("Quedarse en agua de borrajas", "to end up in borage water", "to fizzle out"),
        ("Dar en el clavo", "to hit the nail", "to hit the nail on the head"),
        ("Estar entre la espada y la pared", "to be between sword and wall", "to be between a rock and a hard place"),
        ("No tener pelos en la lengua", "to have no hairs on the tongue", "to speak one's mind"),
    ],
    mistakes=[
        ("Creo que es bueno, aunque que tiene problemas.", "Creo que es bueno, aunque tiene problemas.", "aunque takes the indicative when the fact is real, the subjunctive when it is not."),
        ("Estoy de acuerdo con que el plan es malo.", "No estoy de acuerdo con que el plan sea malo.", "Negated opinion takes the subjunctive: sea."),
        ("Aunque es tarde, vamos. / prob.", "Aunque sea tarde, vamos.", "For a concession about a hypothetical condition the subjunctive is the natural form."),
    ],
    task_title="Argue one point through four moves",
    task_instructions=("Pick a rule in your workplace or study programme and write four Spanish "
                       "paragraphs: the point, the concession («es cierto que…»), the objection "
                       "with a qualifier («aunque», «sin embargo»), and the test or compromise you "
                       "propose. Then say it aloud in two minutes without notes. Every sentence "
                       "that starts with a concession should have its verb in the right mood — "
                       "indicative for a fact, subjunctive for a hypothesis."),
)

EXTRAS["C1"] = EXTRA(
    culture=("Spanish bureaucratic prose runs on the passive-reflexive and on nominalisation: "
             "«se procederá a la revisión de las solicitudes presentadas en plazo». It is not "
             "decoration; it is how the administration compresses a procedure into something that "
             "can be referenced later. C1 is the level where you learn to read it without parsing "
             "twice — and to rewrite it as a sentence with a subject when a human has to act on "
             "it."),
    source_url="https://en.wikipedia.org/wiki/Spanish_grammar",
    reading=("«Se procederá a la revisión de las solicitudes presentadas en plazo», dice la "
             "resolución. La frase contiene dos acciones dentro de dos sustantivos y ningún "
             "responsable. Quien la traduce a lenguaje claro escribe: «Vamos a revisar las "
             "solicitudes que llegaron a tiempo.» El mismo contenido, un tercio de las palabras y "
             "un sujeto. Esa traducción es el trabajo de C1."),
    reading_gloss=("'The review of applications submitted on time will be proceeded with,' says "
                   "the resolution. The sentence contains two actions inside two nouns and no one "
                   "responsible. Anyone who translates it into plain language writes: 'We are going "
                   "to review the applications that arrived on time.' The same content, a third of "
                   "the words and a subject. That translation is the work of C1."),
    listening=("Funcionario: Se denegó la solicitud porque no se aportó la documentación.<br>"
               "Ciudadana: ¿Puede decirlo de otra manera?<br>Funcionario: Sí: faltaba un papel y por eso no la aceptamos.<br>"
               "Ciudadana: Gracias — así se entiende."),
    listening_gloss=("Officer: The application was refused because the documentation was not "
                     "provided. Citizen: Can you say it another way? Officer: Yes: a paper was "
                     "missing and that is why we did not accept it. Citizen: Thanks — that way it "
                     "is understandable."),
    voice_tag=VOICE,
    idioms=[
        ("A grandes rasgos", "at large strokes", "broadly speaking"),
        ("En aras de", "in the interests of", "for the sake of"),
        ("Sentar precedente", "to set precedent", "to set a precedent"),
        ("A la vista de", "in view of", "in view of"),
        ("No obstante", "not obstructing", "nevertheless"),
        ("En su caso", "in its case", "where applicable"),
        ("De cara a", "facing", "with a view to"),
        ("De ahí que", "from there that", "hence"),
        ("Cabe señalar", "it fits to point out", "it should be noted"),
        ("A efectos de", "to the effects of", "for the purposes of"),
    ],
    mistakes=[
        ("Se procederá a revisar las solicitudes, y se procederá a decidir después.", "Se revisarán las solicitudes y se decidirá después.", "Two nominalisations of the same verb are a draft problem, not a register."),
        ("El informe fue redactado por mí mismo ayer por la tarde.", "El informe lo redacté yo ayer por la tarde.", "Spanish turns a stiff passive into an active sentence with a pronoun."),
        ("Cabe señalar que es necesario que se debe de revisar.", "Cabe señalar que conviene revisarlo.", "Stacked periphrases; one modal is enough."),
    ],
    task_title="Un-nominalise one paragraph",
    task_instructions=("Find one paragraph of Spanish administrative or academic prose — a form "
                       "letter, a handbook page, an abstract — and rewrite it twice: once with the "
                       "verbs restored and one subject per sentence, once for a reader who has "
                       "ninety seconds. Then put the original and both versions side by side and "
                       "mark the nouns that turned back into verbs. That list is the C1 "
                       "vocabulary."),
)

EXTRAS["C2"] = EXTRA(
    culture=("Spanish has a literature of quotation and reversal: Cervantes parodied the books of "
             "chivalry, Lorca borrowed the romance and changed its voice, and the press quotes a "
             "phrase in order to turn it. The practical effect at C2 is that allusion is normal: "
             "readers are expected to hear the borrowed line, which is why this level drills irony, "
             "parallelism and the deliberate clash of registers rather than more word lists."),
    source_url="https://en.wikipedia.org/wiki/Spanish_literature",
    reading=("Un artículo empieza: «En un lugar de la Mancha no pasa nada — y eso es la noticia.» "
             "El autor cita a Cervantes para contradecirlo. Quien no oye la alusión lee solo una "
             "afirmación; quien la oye lee un movimiento: primero la fórmula prestada, luego su "
             "vuelta, luego la razón. Ese movimiento es el argumento, y sin él la cita solo "
             "adorna."),
    reading_gloss=("An article begins: 'In a place in La Mancha nothing happens — and that is the "
                   "news.' The author quotes Cervantes in order to contradict him. Whoever does not "
                   "hear the allusion reads only a claim; whoever hears it reads a movement: first "
                   "the borrowed formula, then its turn, then the reason. That movement is the "
                   "argument, and without it the quotation merely decorates."),
    listening=("Entrevistadora: Su texto cita el Quijote y lo contradice.<br>Autor: Sí, y no es un riesgo si el lector lo conoce.<br>"
               "Entrevistadora: ¿Y si no lo conoce?<br>Autor: Entonces le queda la idea, que también funciona sola."),
    listening_gloss=("Interviewer: Your text quotes Don Quixote and contradicts it. Author: Yes, "
                     "and it is not a risk if the reader knows it. Interviewer: And if they don't? "
                     "Author: Then the idea remains, which also works on its own."),
    voice_tag=VOICE,
    idioms=[
        ("Luchar contra molinos de viento", "to fight against windmills", "to tilt at windmills"),
        ("Ser el quinto pino", "to be the fifth pine", "to be miles away"),
        ("No hay mal que por bien no venga", "there is no bad from which good does not come", "every cloud has a silver lining"),
        ("A quien madruga, Dios le ayuda", "God helps the early riser", "the early bird catches the worm"),
        ("Estar en babia", "to be in Babia", "to be daydreaming"),
        ("Tomar el pelo", "to take the hair", "to pull someone's leg"),
        ("Morderse la lengua", "to bite one's tongue", "to hold one's tongue"),
        ("Ir de punta en blanco", "to go from point in white", "to be dressed to the nines"),
        ("Con pelos y señales", "with hairs and signs", "in full detail"),
        ("Leer entre líneas", "to read between lines", "to read between the lines"),
    ],
    mistakes=[
        ("En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no pasa nada.", "«En un lugar de la Mancha no pasa nada», parafraseando a Cervantes.", "An unmarked quotation reads as the author's own prose; a marked one is an allusion."),
        ("Es un riesgo si el lector conoce o no lo conoce.", "No es un riesgo si el lector lo conoce.", "One condition per clause; the doubled alternative muddies the claim."),
        ("La cita adorna y también prueba.", "La cita adorna; la prueba es otra cosa.", "A quotation illustrates; it never proves."),
    ],
    task_title="Quote, reverse, justify",
    task_instructions=("Write one Spanish paragraph of C2 argument in three moves: quote a "
                       "proverb or a literary line, reverse it, and justify the reversal with a "
                       "case the original misses. Then cut every adjective that only adds "
                       "emphasis and check whether the reversal still stands. If it does, the "
                       "paragraph was an argument; if not, it was decoration."),
)

# ── the third lesson of every CEFR unit ─────────────────────────────────────

THIRD["A1"] = [
    ("A1-U1", "A1-U1-L3", L(
        "¿De dónde eres? Países, nacionalidades, idiomas",
        "Origin takes ser + de: SOY DE MÉXICO. Nationalities agree like adjectives (mexicano / "
        "mexicana) and are not capitalised. Languages: HABLO ESPAÑOL Y UN POCO DE INGLÉS.",
        [V("de", "deh", "from (origin)", "preposition"),
         V("el país", "el pah-EES", "country", "noun"),
         V("la nacionalidad", "lah nah-see-oh-nah-lee-DAD", "nationality", "noun"),
         V("hablar", "ah-BLAR", "to speak", "verb"),
         V("un poco", "oon POH-koh", "a little", "adverb")],
        G("Origin and nationality",
          "soy de + country · soy + nationality · hablo + language",
          "Soy de México, pero vivo en Sevilla. Soy mexicana. Hablo español y un poco de inglés. "
          "«¿De dónde eres?» asks origin; «¿Dónde vives?» asks where you are now.",
          [X("Soy de México.", "soy deh MEH-hee-koh.", "I am from Mexico."),
           X("Ella es de Argentina y vive en Madrid.", "EH-yah es deh ar-hen-TEE-nah ee BEE-veh en mah-DREED.", "She is from Argentina and lives in Madrid."),
           X("¿Hablas inglés?", "AH-blahs een-GLAYS?", "Do you speak English?")],
          [("Soy de mexicano.", "Soy mexicano. / Soy de México.", "Origin and nationality are different slots: de + place, bare adjective."),
           ("Soy de la México.", "Soy de México.", "Most country names take no article after de.")]),
        [D("Ben", "¿De dónde eres, Ana?", "deh DON-deh EH-rehs, AH-nah?", "Where are you from, Ana?"),
         D("Ana", "Soy de Sevilla. ¿Y tú?", "soy deh seh-BEE-yah. ee too?", "I'm from Seville. And you?"),
         D("Ben", "Soy de México, pero vivo en Madrid.", "soy deh MEH-hee-koh, PEH-roh BEE-voh en mah-DREED.", "I'm from Mexico, but I live in Madrid."),
         D("Ana", "¿Y hablas inglés?", "ee AH-blahs een-GLAYS?", "And do you speak English?")],
        WS("Origin worksheet", [
            T("Answer with ser de.", ["Where are you from? (Peru)", "Where is she from? (Argentina)"],
              ["Soy del Perú.", "Ella es de Argentina."]),
            T("Add the language.", ["Spanish and a little English", "only Portuguese"],
              ["Hablo español y un poco de inglés.", "Solo hablo portugués."]),
        ]))),
    ("A1-U2", "A1-U2-L3", L(
        "Mi casa: habitaciones, muebles y «hay»",
        "Rooms and furniture are described with HAY (there is / there are): EN MI CASA HAY DOS "
        "HABITACIONES. HAY never changes for number — one form serves both.",
        [V("hay", "eye", "there is / there are", "verb"),
         V("el salón", "el sah-LOHN", "living room", "noun"),
         V("la cocina", "lah koh-SEE-nah", "kitchen", "noun"),
         V("el dormitorio", "el dor-mee-TOH-ree-oh", "bedroom", "noun"),
         V("la mesa", "lah MEH-sah", "table", "noun")],
        G("hay and possession",
          "hay + noun · mi / tu / su + noun",
          "En el salón hay una mesa grande. Mi dormitorio es pequeño pero tiene mucha luz. hay "
          "states existence; tener states what a room has.",
          [X("En la cocina hay una mesa.", "en lah koh-SEE-nah eye OO-nah MEH-sah.", "In the kitchen there is a table."),
           X("Mi casa tiene tres habitaciones.", "mee KAH-sah TEE-eh-neh tres ah-bee-tah-SYOH-nehs.", "My house has three rooms."),
           X("Hay un balcón pequeño.", "eye oon bahl-KOHN peh-KEH-nyoh.", "There is a small balcony.")],
          [("Hay son dos camas.", "Hay dos camas.", "hay is invariable; no plural form."),
           ("Mi casa hay tres habitaciones.", "En mi casa hay tres habitaciones. / Mi casa tiene tres habitaciones.", "hay states existence in a place; tener states what something has.")]),
        [D("Ana", "¿Cómo es tu casa?", "KOH-moh es too KAH-sah?", "What is your house like?"),
         D("Ben", "No es grande. En el salón hay una mesa y un sofá.", "noh es GRAHN-deh. en el sah-LOHN eye OO-nah MEH-sah ee oon soh-FAH.", "It isn't big. In the living room there is a table and a sofa."),
         D("Ana", "¿Cuántas habitaciones?", "KWAHN-tahs ah-bee-tah-SYOH-nehs?", "How many rooms?"),
         D("Ben", "Dos: un dormitorio y un despacho pequeño.", "dohs: oon dor-mee-TOH-ree-oh ee oon des-PAH-choh peh-KEH-nyoh.", "Two: a bedroom and a small study.")],
        WS("Home worksheet", [
            T("Say what there is.", ["a table", "two bedrooms", "a small balcony"],
              ["Hay una mesa.", "Hay dos dormitorios.", "Hay un balcón pequeño."]),
            T("Describe your home.", ["three rooms and a kitchen", "a bright living room"],
              ["Tiene tres habitaciones y una cocina.", "El salón tiene mucha luz."]),
        ]))),
    ("A1-U3", "A1-U3-L3", L(
        "El tiempo y las estaciones: hace frío, llueve",
        "Weather uses HACER for most states: HACE FRÍO, HACE SOL — and dedicated verbs for rain "
        "and snow: LLUEVE, NIEVA. Seasons take en: EN INVIERNO.",
        [V("hace frío", "AH-seh FREE-oh", "it is cold", "phrase"),
         V("hace sol", "AH-seh sol", "it is sunny", "phrase"),
         V("llueve", "YWEH-veh", "it is raining", "verb"),
         V("el verano", "el beh-RAH-noh", "summer", "noun"),
         V("el invierno", "el een-BYEHR-noh", "winter", "noun")],
        G("Weather with hacer",
          "hace + frío/calor/sol/viento · llueve / nieva · en + season",
          "Hoy hace frío y llueve. En verano hace mucho calor, en invierno nieva en la sierra. "
          "«hace» is the third person of hacer and never takes a subject pronoun.",
          [X("Hoy hace mucho calor.", "oy AH-seh MOO-choh kah-LOR.", "Today it is very hot."),
           X("En invierno nieva en la montaña.", "en een-BYEHR-noh NYEH-vah en lah mohn-TAH-nyah.", "In winter it snows in the mountains."),
           X("Llueve y hace viento.", "YWEH-veh ee AH-seh BYEHN-toh.", "It is raining and windy.")],
          [("Es frío hoy.", "Hace frío hoy.", "Temperature states take hacer, not ser."),
           ("Yo tengo frío. (about the weather)", "Hace frío. Tengo frío (about me).", "Weather is hace frío; a person's sensation is tengo frío.")]),
        [D("Ben", "¿Qué tiempo hace hoy?", "keh TYEHM-poh AH-seh oy?", "What is the weather like today?"),
         D("Ana", "Hace frío y llueve.", "AH-seh FREE-oh ee YWEH-veh.", "It is cold and raining."),
         D("Ben", "En invierno aquí llueve mucho, ¿verdad?", "en een-BYEHR-noh ah-KEE YWEH-veh MOO-choh, behr-DAD?", "In winter it rains a lot here, right?"),
         D("Ana", "Sí, pero en verano hace mucho calor.", "see, PEH-roh en beh-RAH-noh AH-seh MOO-choh kah-LOR.", "Yes, but in summer it is very hot.")],
        WS("Weather worksheet", [
            T("Say the weather.", ["it is cold", "it is raining", "it is very hot"],
              ["Hace frío.", "Llueve.", "Hace mucho calor."]),
            T("Answer with the season.", ["When is it hot? (summer)", "When does it snow? (winter)"],
              ["En verano hace calor.", "En invierno nieva."]),
        ]))),
]

THIRD["A2"] = [
    ("A2-U1", "A2-U1-L3", L(
        "En el tren: billetes, andenes, retrasos",
        "Station Spanish is compact: UN BILLETE PARA SEVILLA, POR FAVOR · ¿DE QUÉ ANDÉN SALE? · "
        "LLEVO VEINTE MINUTOS DE RETRASO. «para» marks the destination of a ticket.",
        [V("el billete", "el bee-YEH-teh", "ticket", "noun"),
         V("el andén", "el ahn-DEN", "platform", "noun"),
         V("el retraso", "el reh-TRAH-soh", "delay", "noun"),
         V("el transbordo", "el trahns-BOR-doh", "change (of train)", "noun"),
         V("la llegada", "lah yeh-GAH-dah", "arrival", "noun")],
        G("Tickets and connections",
          "un billete para + city · ¿de qué andén sale? · hay que hacer transbordo",
          "Un billete de ida y vuelta para Sevilla, por favor. ¿Hay que hacer transbordo en "
          "Córdoba? «para» marks the destination; «a» marks the movement of the train.",
          [X("Quiero un billete para Sevilla.", "KYEH-roh oon bee-YEH-teh PAH-rah seh-BEE-yah.", "I want a ticket to Seville."),
           X("¿De qué andén sale el tren?", "deh keh ahn-DEN SAH-leh el tren?", "Which platform does the train leave from?"),
           X("El tren lleva veinte minutos de retraso.", "el tren YEH-vah BAYN-teh mee-NOO-tohs deh reh-TRAH-soh.", "The train is twenty minutes late.")],
          [("Un billete a por Sevilla.", "Un billete para Sevilla.", "The ticket's destination takes para."),
           ("El tren sale de andén cinco.", "El tren sale del andén cinco.", "de + el = del.")]),
        [D("Ana", "Un billete para Sevilla, por favor.", "oon bee-YEH-teh PAH-rah seh-BEE-yah, por fah-BOR.", "A ticket to Seville, please."),
         D("Taquillero", "¿Ida o ida y vuelta?", "EE-dah oh EE-dah ee BWEHL-tah?", "Single or return?"),
         D("Ana", "Ida y vuelta. ¿Hay que hacer transbordo?", "EE-dah ee BWEHL-tah. eye keh ah-SEHR trahns-BOR-doh?", "Return. Do I have to change?"),
         D("Taquillero", "No, directo. Sale del andén siete en diez minutos.", "noh, dee-REK-toh. SAH-leh del ahn-DEN SYEH-teh en DYEHZ mee-NOO-tohs.", "No, direct. It leaves from platform seven in ten minutes.")],
        WS("Train worksheet", [
            T("Buy a ticket.", ["to Valencia, return", "a single to Cádiz"],
              ["Un billete de ida y vuelta para Valencia.", "Un billete de ida para Cádiz."]),
            T("Ask about the connection.", ["which platform?", "must I change?", "is it late?"],
              ["¿De qué andén sale?", "¿Hay que hacer transbordo?", "¿Lleva retraso?"]),
        ]))),
    ("A2-U2", "A2-U2-L3", L(
        "En el médico: síntomas y consejos",
        "Illness is said with tener and doler: TENGO DOLOR DE CABEZA · ME DUELE LA GARGANTA. The "
        "doctor answers with debería: DEBERÍA DESCANSAR — advice, not an order.",
        [V("el dolor", "el doh-LOR", "pain", "noun"),
         V("me duele", "meh DWEH-leh", "it hurts (me)", "phrase"),
         V("la garganta", "lah gar-GAHN-tah", "throat", "noun"),
         V("la receta", "lah reh-SEH-tah", "prescription", "noun"),
         V("descansar", "des-kahn-SAR", "to rest", "verb")],
        G("Symptoms and advice",
          "tengo dolor de … · me duele / me duelen … · debería + infinitive",
          "Me duele la cabeza y tengo fiebre. El médico dice: «Debería descansar y beber agua.» "
          "doler agrees with the thing that hurts: me duele la cabeza, me duelen los pies.",
          [X("Me duele la garganta.", "meh DWEH-leh lah gar-GAHN-tah.", "My throat hurts."),
           X("Me duelen los pies.", "meh DWEH-lehn lohs pyehs.", "My feet hurt."),
           X("Debería descansar dos días.", "deh-beh-REE-ah des-kahn-SAR dohs DEE-ahs.", "You should rest for two days.")],
          [("Tengo dolor de la garganta.", "Tengo dolor de garganta.", "The pain's location takes bare de: dolor de garganta."),
           ("Yo duele la cabeza.", "Me duele la cabeza.", "doler takes the person as indirect object: me duele.")]),
        [D("Ben", "Buenos días, tengo cita con la doctora.", "BWEH-nohs DEE-ahs, TEN-goh SEE-tah kohn lah dok-TOH-rah.", "Good morning, I have an appointment with the doctor."),
         D("Doctora", "¿Qué le pasa?", "keh leh PAH-sah?", "What is wrong with you?"),
         D("Ben", "Me duele la garganta y tengo fiebre.", "meh DWEH-leh lah gar-GAHN-tah ee TEN-goh FYEH-breh.", "My throat hurts and I have a fever."),
         D("Doctora", "Debería descansar y beber mucha agua. Le doy una receta.", "deh-beh-REE-ah des-kahn-SAR ee beh-BEHR MOO-chah AH-gwah. leh doy OO-nah reh-SEH-tah.", "You should rest and drink a lot of water. I'll give you a prescription.")],
        WS("Doctor worksheet", [
            T("Say the symptom.", ["sore throat", "my head hurts", "my feet hurt"],
              ["Me duele la garganta.", "Me duele la cabeza.", "Me duelen los pies."]),
            T("Give the advice.", ["rest two days", "drink a lot of water"],
              ["Debería descansar dos días.", "Debería beber mucha agua."]),
        ]))),
    ("A2-U3", "A2-U3-L3", L(
        "Cambiar y comparar: demasiado grande, más barato",
        "Shopping problems need the comparative (MÁS BARATO, MÁS GRANDE, MEJOR) and CAMBIAR. The "
        "shop answers with a condition: SI TIENE EL TICKET, LO CAMBIAMOS.",
        [V("cambiar", "kahm-BYAR", "to exchange, to change", "verb"),
         V("el ticket", "el TEE-keht", "receipt", "noun"),
         V("demasiado", "deh-mah-SYAH-doh", "too, too much", "adverb"),
         V("la talla", "lah TAH-yah", "size (clothing)", "noun"),
         V("probarse", "proh-BAR-seh", "to try on", "verb")],
        G("Comparing and exchanging",
          "más / menos + adjective + que · demasiado + adjective · ¿puedo cambiarlo?",
          "Esta camisa es más barata que la otra, pero es demasiado pequeña. ¿Puedo cambiarla? "
          "The comparative uses más … que; «tan … como» states equality.",
          [X("Estos pantalones son demasiado grandes.", "EHS-tohs pahn-tah-LOH-nehs sohn deh-mah-SYAH-doh GRAHN-dehs.", "These trousers are too big."),
           X("Esta camisa es más barata que esa.", "EHS-tah kah-MEE-sah es más bah-RAH-tah keh EH-sah.", "This shirt is cheaper than that one."),
           X("¿Puedo cambiarlo por una talla más?", "PWEH-doh kahm-BYAR-loh por OO-nah TAH-yah más?", "Can I exchange it for a larger size?")],
          [("Es más grande que lo otro más.", "Es más grande que el otro.", "One comparative per phrase."),
           ("Puedo cambiar lo?", "¿Puedo cambiarlo?", "The object pronoun attaches to the infinitive.")]),
        [D("Ana", "Perdón, estos pantalones son demasiado grandes.", "per-DOHN, EHS-tohs pahn-tah-LOH-nehs sohn deh-mah-SYAH-doh GRAHN-dehs.", "Excuse me, these trousers are too big."),
         D("Dependienta", "¿Tiene el ticket?", "TYEH-neh el TEE-keht?", "Do you have the receipt?"),
         D("Ana", "Sí. ¿Puedo probarme una talla menos?", "see. PWEH-doh proh-BAR-meh OO-nah TAH-yah MEH-nohs?", "Yes. Can I try a size smaller?"),
         D("Dependienta", "Claro, el probador está al fondo.", "KLAH-roh, el proh-bah-DOR es-TAH al FOHN-doh.", "Of course, the fitting room is at the back.")],
        WS("Shopping worksheet", [
            T("Say the problem.", ["too big", "too small", "cheaper than the other one"],
              ["demasiado grande", "demasiado pequeño", "más barato que el otro"]),
            T("Ask to exchange it.", ["can I exchange it?", "do you have a bigger size?"],
              ["¿Puedo cambiarlo?", "¿Tiene una talla más?"]),
        ]))),
]

THIRD["B1"] = [
    ("B1-U1", "B1-U1-L3", L(
        "Contar una anécdota: primero, luego, de repente",
        "Spanish anecdotes mix the pretérito for events and the imperfecto for the scene: PRIMERO "
        "LLEGAMOS, LUEGO EMPEZÓ A LLOVER, DE REPENTE SE FUE LA LUZ. The imperfect describes; the "
        "preterite acts.",
        [V("primero", "pree-MEH-roh", "first", "adverb"),
         V("luego", "LWEH-goh", "then", "adverb"),
         V("de repente", "deh reh-PEN-teh", "suddenly", "adverb"),
         V("al final", "al fee-NAL", "in the end", "phrase"),
         V("la escena", "lah EHS-seh-nah", "scene", "noun")],
        G("Scene and event",
          "imperfecto for the background · pretérito for the event · time adverbs fronted",
          "Estábamos en casa, llovía y de repente se fue la luz. The scene is imperfect, the turn "
          "is preterite — that pairing is what makes a Spanish story sound native.",
          [X("Primero llegamos al hotel.", "pree-MEH-roh yeh-GAH-mohs al oh-TEL.", "First we arrived at the hotel."),
           X("Llovía y de repente se fue la luz.", "yoh-VEE-ah ee deh reh-PEN-teh seh fweh lah looz.", "It was raining and suddenly the power went out."),
           X("Al final todo salió bien.", "al fee-NAL TOH-doh sah-LYOH byehn.", "In the end everything turned out well.")],
          [("De repente llovía.", "De repente empezó a llover.", "de repente introduces an event: preterite."),
           ("Estuvimos en casa y llovió toda la tarde. (scene)", "Estábamos en casa y llovía.", "Background states take the imperfect.")]),
        [D("Ana", "¿Qué pasó ayer?", "keh pah-SOH ah-YEHR?", "What happened yesterday?"),
         D("Ben", "Estábamos en el bar, hablábamos tranquilamente y de repente se fue la luz.", "es-TAH-bah-mohs en el bar, ah-BLAH-bah-mohs trahn-kee-lah-MEN-teh ee deh reh-PEN-teh seh fweh lah looz.", "We were in the bar, talking quietly, and suddenly the power went out."),
         D("Ana", "¿Y luego?", "ee LWEH-goh?", "And then?"),
         D("Ben", "Luego todos sacamos el móvil y seguimos hablando igual.", "LWEH-goh TOH-dohs sah-KAH-mohs el MOH-veel ee seh-GEE-mohs ah-BLAN-doh ee-GWAL.", "Then we all took out our phones and kept talking anyway.")],
        WS("Story worksheet", [
            T("Order the story.", ["it was raining", "then the power went out", "in the end we laughed"],
              ["llovía", "luego se fue la luz", "al final nos reímos"]),
            T("Set the scene, then turn it.", ["we were talking → suddenly someone knocked"],
              ["Hablábamos y de repente alguien llamó a la puerta."]),
        ]))),
    ("B1-U2", "B1-U2-L3", L(
        "Buscar trabajo: currículum, entrevista, usted",
        "Applications and interviews keep the usted register: ¿POR QUÉ SE INTERESA POR ESTE "
        "PUESTO? · TENGO EXPERIENCIA EN … The polite forms are usted forms, not third-person "
        "accidents.",
        [V("el puesto", "el PWES-toh", "position, post", "noun"),
         V("el currículum", "el koo-RREE-koo-loom", "CV", "noun"),
         V("la experiencia", "lah eks-peh-RYEN-syah", "experience", "noun"),
         V("solicitar", "soh-lee-see-TAR", "to apply for", "verb"),
         V("la entrevista", "lah en-treh-VEES-tah", "interview", "noun")],
        G("Interview register",
          "¿por qué se interesa por…? · tengo experiencia en … · me gustaría …",
          "Tengo experiencia en atención al cliente y me gustaría aprender más. Note the usted "
          "forms (se interesa, tiene) and the conditional for wishes (me gustaría).",
          [X("¿Por qué se interesa por este puesto?", "por keh seh een-teh-REH-sah por EHS-teh PWES-toh?", "Why are you interested in this position?"),
           X("Tengo tres años de experiencia.", "TEN-goh tres AH-nyohs deh eks-peh-RYEN-syah.", "I have three years of experience."),
           X("Me gustaría trabajar en su equipo.", "meh goos-tah-REE-ah trah-bah-HAR en soo eh-KEE-poh.", "I would like to work in your team.")],
          [("Yo tengo experiencia en trabajar.", "Tengo experiencia en atención al cliente.", "Experience is in a field, not in a verb."),
           ("Quiero el trabajo, dámelo.", "Me interesa el puesto y me gustaría aportar mi experiencia.", "The interview register is mitigated, not direct.")]),
        [D("Sra. Ruiz", "Buenos días. ¿Por qué se interesa por este puesto?", "BWEH-nohs DEE-ahs. por keh seh een-teh-REH-sah por EHS-teh PWES-toh?", "Good morning. Why are you interested in this position?"),
         D("Ana", "Tengo experiencia en atención al cliente y me gustaría crecer aquí.", "TEN-goh eks-peh-RYEN-syah en ah-ten-SYOHN al KLYEN-teh ee meh goos-tah-REE-ah kreh-SEHR ah-KEE.", "I have experience in customer service and I would like to grow here."),
         D("Sra. Ruiz", "¿Y su punto fuerte?", "ee soo POON-toh FWEHR-teh?", "And your strong point?"),
         D("Ana", "Mantengo la calma cuando hay prisa.", "mahn-TEN-goh lah KAHL-mah KWAHN-doh eye PREE-sah.", "I keep calm when there is pressure.")],
        WS("Interview worksheet", [
            T("Say it in Spanish.", ["I have three years of experience", "I would like to work in your team"],
              ["Tengo tres años de experiencia.", "Me gustaría trabajar en su equipo."]),
            T("Answer the question.", ["Why this post?", "What do you bring?"],
              ["Me interesa el puesto porque quiero crecer.", "Aporto experiencia y calma."]),
        ]))),
    ("B1-U3", "B1-U3-L3", L(
        "Quedar: citas, cambios, cancelar",
        "Making an appointment uses QUEDAR and venir bien: ¿QUEDAMOS EL JUEVES? · ME VIENE BIEN A "
        "LAS SEIS. Moving it: ¿LO PODEMOS CAMBIAR? Cancelling: me ha surgido algo.",
        [V("quedar", "keh-DAR", "to arrange to meet", "verb"),
         V("la cita", "lah SEE-tah", "appointment", "noun"),
         V("cambiar", "kahm-BYAR", "to change, move", "verb"),
         V("surgir", "soor-HEER", "to come up", "verb"),
         V("avisar", "ah-bee-SAR", "to let know", "verb")],
        G("Arranging and moving",
          "¿quedamos el …? · me viene bien / me viene mal · ¿lo podemos cambiar?",
          "¿Quedamos el jueves a las seis? Me viene bien. Si surge algo, aviso con tiempo. "
          "«quedar» is for the plan; «quedarse» means to stay.",
          [X("¿Quedamos el jueves?", "keh-DAH-mohs el HWEH-vehs?", "Shall we meet on Thursday?"),
           X("Me viene bien a las seis.", "meh BYEH-neh byehn ah lahs says.", "Six o'clock works for me."),
           X("Me ha surgido algo y no puedo ir.", "meh ah soor-HEE-doh AL-goh ee noh PWEH-doh eer.", "Something has come up and I can't go.")],
          [("Me quedo bien a las seis.", "Me viene bien a las seis.", "The time suits: venir bien."),
           ("Quedamos a las seis y quedé en casa.", "Quedamos a las seis y me quedé en casa.", "quedar plans; quedarse stays.")]),
        [D("Ben", "¿Quedamos el jueves para repasar?", "keh-DAH-mohs el HWEH-vehs PAH-rah reh-pah-SAR?", "Shall we meet on Thursday to revise?"),
         D("Ana", "El jueves me viene mal. ¿Lo podemos cambiar al viernes?", "el HWEH-vehs meh BYEH-neh mahl. loh poh-DEH-mohs kahm-BYAR al BYEHR-nehs?", "Thursday doesn't work for me. Can we move it to Friday?"),
         D("Ben", "Viernes a las seis, ¿te viene bien?", "BYEHR-nehs ah lahs says, teh BYEH-neh byehn?", "Friday at six, does that suit you?"),
         D("Ana", "Perfecto. Si surge algo, te aviso.", "per-FEK-toh. see SOOR-heh AL-goh, teh ah-BEE-soh.", "Perfect. If something comes up, I'll let you know.")],
        WS("Arrangement worksheet", [
            T("Fix the time.", ["shall we meet on Thursday?", "six o'clock works for me", "does Friday suit you?"],
              ["¿Quedamos el jueves?", "Me viene bien a las seis.", "¿Te viene bien el viernes?"]),
            T("Move or cancel it.", ["can we move it?", "something has come up"],
              ["¿Lo podemos cambiar?", "Me ha surgido algo."]),
        ]))),
]

THIRD["B2"] = [
    ("B2-U1", "B2-U1-L3", L(
        "Conceder y rebatir: es cierto que…, aunque, sin embargo",
        "The Spanish rebuttal concedes first: ES CIERTO QUE … PERO … · AUNQUE …, SIN EMBARGO … "
        "The concession is a grammatical slot, not a decoration — and it decides the mood of the "
        "clause that follows.",
        [V("es cierto que", "es SYEHR-toh keh", "it is true that", "phrase"),
         V("aunque", "AWN-keh", "although", "conjunction"),
         V("sin embargo", "seen em-BAR-goh", "however", "adverb"),
         V("matizar", "mah-tee-SAR", "to qualify", "verb"),
         V("el matiz", "el mah-TEES", "nuance", "noun")],
        G("Concession",
          "es cierto que + indicative · aunque + indicative (fact) / subjunctive (hypothesis)",
          "Es cierto que la medida es popular, pero nadie ha medido su coste. Aunque llueva, "
          "saldremos (hypothesis → subjunctive). The mood of aunque is the argument: fact or "
          "supposition.",
          [X("Es cierto que es popular, pero tiene un coste.", "es SYEHR-toh keh es poh-poo-LAR, PEH-roh TYEH-neh oon KOS-teh.", "It is true that it is popular, but it has a cost."),
           X("Aunque llueva, iremos.", "AWN-keh YWEH-vah, ee-REH-mohs.", "Even if it rains, we will go."),
           X("Sin embargo, falta un dato.", "seen em-BAR-goh, FAHL-tah oon DAH-toh.", "However, one piece of data is missing.")],
          [("Aunque llueve, iremos. (as hypothesis)", "Aunque llueva, iremos.", "Hypothetical concession takes the subjunctive."),
           ("Es cierto que, pero sin embargo…", "Es cierto que …, pero …", "One concessive per sentence; stacking cancels it.")]),
        [D("Sra. Ruiz", "¿Qué le parece la propuesta?", "keh leh pah-REH-seh lah proh-poo-EHS-tah?", "What do you think of the proposal?"),
         D("Ben", "Es cierto que ahorra tiempo, pero el coste es alto.", "es SYEHR-toh keh ah-OH-rrah TYEHM-poh, PEH-roh el KOS-teh es AL-toh.", "It is true that it saves time, but the cost is high."),
         D("Sra. Ruiz", "¿Y su propuesta?", "ee soo proh-poo-EHS-tah?", "And your proposal?"),
         D("Ben", "Sin embargo, creo que podemos probarlo un mes.", "seen em-BAR-goh, KREH-oh keh poh-DEH-mohs proh-BAR-loh oon mes.", "However, I think we can test it for a month.")],
        WS("Rebuttal worksheet", [
            T("Build the concession.", ["it is popular (but it costs)", "it saves time (but it costs staff)"],
              ["Es cierto que es popular, pero tiene un coste.", "Es cierto que ahorra tiempo, pero cuesta personal."]),
            T("Choose the mood.", ["although it rains (hypothesis)", "although it is raining (fact)"],
              ["Aunque llueva …", "Aunque llueve …"]),
        ]))),
    ("B2-U2", "B2-U2-L3", L(
        "El correo formal: asunto, saludo, despedida",
        "A Spanish business email is framed: ASUNTO with the matter, ESTIMADO/A + surname, body, "
        "and ATENTAMENTE or UN SALUDO. «Estimados señores» opens to a company.",
        [V("el asunto", "el ah-SOON-toh", "subject line", "noun"),
         V("estimado", "es-tee-MAH-doh", "dear (formal)", "adjective"),
         V("adjuntar", "ah-hoon-TAR", "to attach", "verb"),
         V("agradecer", "ah-grah-deh-SEHR", "to thank", "verb"),
         V("atentamente", "ah-ten-tah-MEN-teh", "yours faithfully", "adverb")],
        G("Email frame",
          "Asunto: … · Estimada Sra. Ruiz: · Adjunto … · Quedo a la espera de su respuesta. · Atentamente",
          "Asunto: Reunión del 12 de mayo. Estimada Sra. Ruiz: Adjunto los documentos. Quedo a la "
          "espera de su respuesta antes del viernes. Atentamente. The colon after the greeting is "
          "the peninsular convention.",
          [X("Asunto: Documentos para la reunión", "ah-SOON-toh: doh-koo-MEN-tohs PAH-rah lah reh-YOHN.", "Subject: documents for the meeting"),
           X("Estimada Sra. Ruiz:", "es-tee-MAH-dah SEH-nyoh-rah RWEES:", "Dear Ms Ruiz:"),
           X("Atentamente, Ana López", "ah-ten-tah-MEN-teh, AH-nah LOH-pehs.", "Yours faithfully, Ana López")],
          [("Hola Sra. Ruiz!", "Estimada Sra. Ruiz:", "A first business contact takes the formal greeting and a colon."),
           ("Te adjunto los documentos, saludos!", "Adjunto los documentos. Un saludo,", "The formal register keeps usted and no exclamation marks.")]),
        [D("Ana", "¿Está bien el correo?", "es-TAH byehn el koh-RREH-oh?", "Is the email all right?"),
         D("Ben", "Falta el asunto, y el saludo es muy informal.", "FAHL-tah el ah-SOON-toh, ee el sah-LOO-doh es mooy een-for-MAL.", "The subject is missing, and the greeting is too informal."),
         D("Ana", "¿«Estimado Sr. García»?", "es-tee-MAH-doh SEH-nyor gar-SEE-ah?", "'Dear Mr García'?"),
         D("Ben", "Mejor «Estimado Sr. García:», y al final «Atentamente».", "meh-HOR es-tee-MAH-doh SEH-nyor gar-SEE-ah:, ee al fee-NAL ah-ten-tah-MEN-teh.", "Better 'Dear Mr García:' and at the end 'Yours faithfully'.")],
        WS("Email worksheet", [
            T("Frame the email.", ["subject: meeting on 12 May", "greeting to Ms Ruiz", "closing"],
              ["Asunto: Reunión del 12 de mayo", "Estimada Sra. Ruiz:", "Atentamente"]),
            T("Write the body line.", ["the documents are attached", "I await your reply"],
              ["Adjunto los documentos.", "Quedo a la espera de su respuesta."]),
        ]))),
    ("B2-U3", "B2-U3-L3", L(
        "Leer las noticias: titular, fuente, afirmación",
        "Spanish news answers three questions fast: SEGÚN …, FUENTES … , and what is still open. "
        "Headlines drop articles and verbs: «El Gobierno niega la subida».",
        [V("según", "seh-GOON", "according to", "preposition"),
         V("la fuente", "lah FWEHN-teh", "source", "noun"),
         V("el titular", "el tee-too-LAR", "headline", "noun"),
         V("confirmar", "kohn-feer-MAR", "to confirm", "verb"),
         V("sin confirmar", "seen kohn-feer-MAR", "unconfirmed", "phrase")],
        G("Attribution",
          "según + source · fuentes cercanas a … · está sin confirmar",
          "Según el ministerio, los precios suben. Fuentes cercanas a la empresa lo niegan. «según» "
          "keeps the claim with the source and is the honest part of the sentence.",
          [X("Según el informe, los precios suben.", "seh-GOON el een-FOR-meh, lohs PREH-syohs SOO-behn.", "According to the report, prices are rising."),
           X("Fuentes cercanas al ministerio lo niegan.", "FWEHN-tehs sehr-KAH-nahs al mee-nees-TEH-ryoh loh NYEH-gahn.", "Sources close to the ministry deny it."),
           X("La cifra está sin confirmar.", "lah SEE-frah es-TAH seen kohn-feer-MAR.", "The figure is unconfirmed.")],
          [("Según de fuentes, suben.", "Según las fuentes, suben.", "según takes the source directly."),
           ("El informe dice que es seguro. (a claim)", "El informe apunta a que podría subir.", "A reported claim keeps its own certainty.")]),
        [D("Ana", "¿Qué dice el titular?", "keh DEE-seh el tee-too-LAR?", "What does the headline say?"),
         D("Ben", "«El Gobierno niega la subida», según fuentes del ministerio.", "el goh-BYEHR-noh NYEH-gah lah soo-BEE-dah, seh-GOON FWEHN-tehs del mee-nees-TEH-ryoh.", "'The government denies the rise', according to ministry sources."),
         D("Ana", "¿Y la empresa?", "ee lah em-PREH-sah?", "And the company?"),
         D("Ben", "No ha dicho nada todavía. La cifra sigue sin confirmar.", "noh ah DEE-choh NAH-dah toh-dah-VEE-ah. lah SEE-frah SEE-geh seen kohn-feer-MAR.", "It has said nothing yet. The figure remains unconfirmed.")],
        WS("News worksheet", [
            T("Attribute the claim.", ["according to the report", "sources close to the ministry"],
              ["según el informe", "fuentes cercanas al ministerio"]),
            T("Separate the states.", ["it is claimed", "it is unconfirmed"],
              ["se afirma que …", "está sin confirmar"]),
        ]))),
]

THIRD["C1"] = [
    ("es-c1-u1", "es-c1-l7", L(
        "Atribución sin aval: al parecer, presuntamente, según fuentes",
        "Spanish distances a claim with adverbs and frames: AL PARECER, PRESUNTAMENTE, AL PARECER "
        "QUE, SEGÚN FUENTES, AL PARECER HABRÍA. The frame says who owns the claim — and the "
        "conditional keeps it a report.",
        [V("al parecer", "al pah-reh-SEHR", "apparently", "phrase"),
         V("presuntamente", "preh-soon-tah-MEN-teh", "allegedly", "adverb"),
         V("según fuentes", "seh-GOON FWEHN-tehs", "according to sources", "phrase"),
         V("supuestamente", "soo-pwehs-tah-MEN-teh", "supposedly", "adverb"),
         V("la atribución", "lah ah-tree-boo-SYOHN", "attribution", "noun")],
        G("Evidential frames",
          "al parecer + indicative · al parecer, habría + participle · presuntamente + fact",
          "Al parecer, el ministro habría dimitido. Presuntamente se pagaron comisiones. The "
          "conditional (habría dimitido) labels the news as unconfirmed — dropping it turns the "
          "sentence into an assertion.",
          [X("Al parecer, el ministro habría dimitido.", "al pah-reh-SEHR, el mee-NEES-troh ah-BREE-ah dee-mee-TEE-doh.", "Apparently the minister has stepped down."),
           X("Presuntamente se pagaron comisiones.", "preh-soon-tah-MEN-teh seh pah-GAH-rohn koh-mee-SYOH-nehs.", "Commissions were allegedly paid."),
           X("Según fuentes del partido, habrá elecciones.", "seh-GOON FWEHN-tehs del par-TEE-doh, ah-BRAH eh-lek-SYOH-nehs.", "According to party sources, there will be elections.")],
          [("Al parecer, el ministro dimitió. (unconfirmed)", "Al parecer, el ministro habría dimitido.", "The conditional carries the distance."),
           ("Presuntamente, seguro que fue él.", "Presuntamente fue él.", "One evidential per claim; certainty cancels the hedge.")]),
        [D("Redactor", "¿Publicamos que dimitió?", "pool-lee-KAH-mohs keh dee-mee-TYOH?", "Do we publish that he resigned?"),
         D("Editora", "No. Al parecer habría dimitido — dos fuentes, ninguna oficial.", "noh. al pah-reh-SEHR ah-BREE-ah dee-mee-TEE-doh — dohs FWEHN-tehs, neen-GOO-nah oh-fee-SYAL.", "No. Apparently he has resigned — two sources, none official."),
         D("Redactor", "¿Y el titular?", "ee el tee-too-LAR?", "And the headline?"),
         D("Editora", "«Al parecer, el ministro habría dimitido» — con la atribución dentro.", "al pah-reh-SEHR, el mee-NEES-troh ah-BREE-ah dee-mee-TEE-doh — kohn lah ah-tree-boo-SYOHN DEN-troh.", "'Apparently the minister has stepped down' — with the attribution inside it.")],
        WS("Evidential worksheet", [
            T("Put it at arm's length.", ["he resigned (unconfirmed)", "commissions were paid (alleged)", "there will be elections (sources)"],
              ["Al parecer, habría dimitido.", "Presuntamente se pagaron comisiones.", "Según fuentes, habrá elecciones."]),
            T("Say what the source is.", ["two sources, none official", "party sources"],
              ["dos fuentes, ninguna oficial", "fuentes del partido"]),
        ]))),
    ("es-c1-u2", "es-c1-l8", L(
        "Causalidad graduada: contribuye a, podría explicar, apunta a que",
        "Careful Spanish causal prose grades the link: CONTRIBUYE A (contributes), PODRÍA EXPLICAR "
        "(may explain), APUNTA A QUE (points to), NO BASTA PARA (is not enough to). Each verb "
        "states how strong the link is.",
        [V("contribuir a", "kohn-tree-BWEER ah", "to contribute to", "verb"),
         V("podría explicar", "poh-DREE-ah eks-plee-KAR", "could explain", "phrase"),
         V("apuntar a que", "ah-poon-TAR ah keh", "to point to", "verb"),
         V("bastar para", "bahs-TAR PAH-rah", "to be enough to", "verb"),
         V("la correlación", "lah koh-rreh-lah-SYOHN", "correlation", "noun")],
        G("Calibrated cause",
          "contribuye a · podría explicar · apunta a que · no basta para",
          "La demanda contribuye al aumento, pero no basta para explicarlo. The sentence holds a "
          "mechanism and its limit in one clause pair — the signature of Spanish academic prose.",
          [X("La sequía podría explicar la subida.", "lah seh-KEE-ah poh-DREE-ah eks-plee-KAR lah soo-BEE-dah.", "The drought could explain the rise."),
           X("Los datos apuntan a que el mercado se recupera.", "lohs DAH-tohs ah-POON-tahn ah keh el mer-KAH-doh seh reh-koo-peh-RAH.", "The data points to the market recovering."),
           X("Una correlación no basta para afirmar una causa.", "OO-nah koh-rreh-lah-SYOHN noh BAHS-tah PAH-rah ah-feer-MAR OO-nah KOW-sah.", "A correlation is not enough to assert a cause.")],
          [("La sequía explica la subida. (correlation)", "La sequía podría explicar la subida.", "podría marks the inference."),
           ("Los datos apuntan que sube.", "Los datos apuntan a que sube.", "apuntar a que needs the preposition.")]),
        [D("Ana", "¿Por qué suben los precios?", "por keh SOO-behn lohs PREH-syohs?", "Why are prices rising?"),
         D("Analista", "La demanda contribuye, pero no basta para explicarlo.", "lah deh-MAHN-dah kohn-tree-BWEH-yeh, PEH-roh noh BAHS-tah PAH-rah eks-plee-KAR-loh.", "Demand contributes, but it is not enough to explain it."),
         D("Ana", "¿Y la energía?", "ee lah eh-ner-HEE-ah?", "And energy?"),
         D("Analista", "También apunta a que hay presión — pero es una correlación.", "tahm-BYEHN ah-POON-tah ah keh eye preh-SYOHN — PEH-roh es OO-nah koh-rreh-lah-SYOHN.", "It also points to pressure — but it is a correlation.")],
        WS("Causality worksheet", [
            T("Grade the link.", ["could explain", "contributes to", "points to"],
              ["podría explicar", "contribuye a", "apunta a que"]),
            T("State the limit.", ["this alone is not enough", "correlation is not cause"],
              ["Esto solo no basta.", "Una correlación no es una causa."]),
        ]))),
    ("es-c1-u3", "es-c1-l9", L(
        "Síntesis: dos fuentes en un párrafo",
        "Synthesis names the sources and then speaks with one voice: SEGÚN EL INSTITUTO …, LA "
        "PATRONAL SEÑALA POR SU LADO … — EN LO QUE AMBAS COINCIDEN ES EN QUE … The third sentence "
        "is the synthesis.",
        [V("señalar", "seh-nyah-LAR", "to point out", "verb"),
         V("por su lado", "por soo LAH-doh", "on its side", "phrase"),
         V("coincidir en", "koh-een-see-DEER en", "to agree on", "verb"),
         V("el instituto", "el een-stee-TOO-toh", "institute", "noun"),
         V("la patronal", "lah pah-troh-NAL", "employers' association", "noun")],
        G("Source sandwich",
          "según A … · B señala por su lado … · en lo que ambos coinciden es en que …",
          "Según el instituto, la cifra es estable. La patronal señala por su lado riesgos. En "
          "lo que ambos coinciden es en que faltan datos. Three sentences, two positions, one "
          "honest conclusion.",
          [X("Según el instituto, la cifra es estable.", "seh-GOON el een-stee-TOO-toh, lah SEE-frah es es-TAH-bleh.", "According to the institute the figure is stable."),
           X("La patronal señala riesgos por su lado.", "lah pah-troh-NAL seh-NYAH-lah RYEH-sgohs por soo LAH-doh.", "The employers' association points to risks on its side."),
           X("En lo que ambos coinciden es en que faltan datos.", "en loh keh AHM-bohs koh-een-SEE-dehn es en keh FAHL-tahn DAH-tohs.", "What both agree on is that data is missing.")],
          [("Ambos dicen lo mismo, pero lo contrario.", "Ambos ven cosas distintas y coinciden en el diagnóstico.", "A synthesis states difference and shared ground; it cannot merge them."),
           ("Coinciden en que los datos.", "Coinciden en que faltan datos.", "The shared point is a clause, not a noun phrase.")]),
        [D("Ana", "¿Cómo resumo las dos fuentes?", "KOH-moh reh-SOO-moh lah dohs FWEHN-tehs?", "How do I summarise the two sources?"),
         D("Ben", "Primero cada una, después el punto común.", "pree-MEH-roh KAH-dah OO-nah, des-PWEHS el POON-toh koh-MOON.", "First each one, then the common point."),
         D("Ana", "«Según el instituto es estable; la patronal señala riesgos…»", "seh-GOON el een-stee-TOO-toh es es-TAH-bleh; lah pah-troh-NAL seh-NYAH-lah RYEH-sgohs…", "'According to the institute it is stable; the employers point to risks…'"),
         D("Ben", "…y «en lo que coinciden es en que faltan datos». Perfecto.", "ee en loh keh koh-een-SEE-dehn es en keh FAHL-tahn DAH-tohs. per-FEK-toh.", "…and 'what they agree on is that data is missing'. Perfect.")],
        WS("Synthesis worksheet", [
            T("Line the sources up.", ["according to the institute", "the association, on its side"],
              ["según el instituto", "la patronal, por su lado"]),
            T("Write the synthesis.", ["what both agree on"],
              ["En lo que ambos coinciden es en que …"]),
        ]))),
]

THIRD["C2"] = [
    ("es-c2-u1", "es-c2-l7", L(
        "Lo que el texto presupone: presuposición e implicatura",
        "A sentence smuggles in assumptions: ¿POR QUÉ IGNORÓ LA NORMA? presupposes the norm and the "
        "ignoring. C2 names the presupposition instead of arguing inside it: ESA PREGUNTA PARTE DE "
        "QUE …",
        [V("presuponer", "preh-soo-poh-NEHR", "to presuppose", "verb"),
         V("la presuposición", "lah preh-soo-poh-see-SYOHN", "presupposition", "noun"),
         V("la implicatura", "lah eem-plee-kah-TOO-rah", "implicature", "noun"),
         V("dar por hecho", "dar por EH-choh", "to take for granted", "phrase"),
         V("rechazar", "reh-chah-SAR", "to reject", "verb")],
        G("Naming the presupposition",
          "esa pregunta parte de que … · el texto da por hecho que … · eso no está probado",
          "Esa pregunta parte de que yo lo sabía. El párrafo da por hecho que hubo un incumplimiento "
          "— y eso no está probado. Naming the frame is how a Spanish speaker refuses the question "
          "without refusing to answer.",
          [X("Esa pregunta parte de que todos lo sabían.", "EH-sah preh-GOON-tah PAR-teh deh keh TOH-dohs loh sah-BEE-ahn.", "That question presupposes that everyone knew."),
           X("El texto da por hecho que hubo un incumplimiento.", "el TEKS-toh dah por EH-choh keh OO-boh oon een-koom-plee-MYEN-toh.", "The text takes a breach for granted."),
           X("Esa presuposición la rechazo.", "EH-sah preh-soo-poh-see-SYOHN lah reh-CHAH-soh.", "I reject that presupposition.")],
          [("¿Por qué ignoró la norma? (as a first question)", "Antes de responder: ¿de dónde parte la pregunta?", "The question smuggles in the answer; break the frame first."),
           ("El texto implica que fue así y lo prueba.", "El texto lo da por hecho; probarlo es otra cosa.", "Presupposing is not proving.")]),
        [D("Periodista", "¿Por qué ignoró la norma?", "por keh ee-gnoh-ROH lah NOR-mah?", "Why did you ignore the rule?"),
         D("Entrevistada", "Esa pregunta parte de que la ignoré.", "EH-sah preh-GOON-tah PAR-teh deh keh lah ee-gnoh-REH.", "That question presupposes that I ignored it."),
         D("Periodista", "¿Y no fue así?", "ee noh fweh ah-SEE?", "And was it not so?"),
         D("Entrevistada", "El asunto está sin resolver. Antes de responder, aclaremos eso.", "el ah-SOON-toh es-TAH seen reh-sol-VEHR. AHN-tehs deh res-pohn-DEHR, ah-klah-REH-mohs EH-soh.", "The matter is unresolved. Before I answer, let's settle that.")],
        WS("Presupposition worksheet", [
            T("Name what is assumed.", ["the question presupposes that everyone knew", "the text takes a breach for granted"],
              ["Esa pregunta parte de que todos lo sabían.", "El texto da por hecho que hubo un incumplimiento."]),
            T("Break the frame.", ["reject the presupposition", "unresolved before answering"],
              ["Esa presuposición la rechazo.", "El asunto está sin resolver."]),
        ]))),
    ("es-c2-u2", "es-c2-l8", L(
        "Cambio de registro deliberado: administrativo, publicitario, lema",
        "A C2 text can fold in a register on purpose — a legal sentence quoted to be mocked, a "
        "slogan dropped into an essay. The frame signals it: «Suena a lenguaje administrativo "
        "cuando dice: …»",
        [V("el lenguaje administrativo", "el len-GWAH-heh ahd-mee-nees-trah-TEE-boh", "administrative language", "noun"),
         V("el eslogan", "el es-LOH-gahn", "slogan", "noun"),
         V("el lema", "el LEH-mah", "motto", "noun"),
         V("citar", "see-TAR", "to quote", "verb"),
         V("el contraste", "el kohn-TRAHS-teh", "contrast", "noun")],
        G("Quoting a register, and marking it",
          "suena a … cuando dice: … · cito: … · con un lema: …",
          "Suena a lenguaje administrativo: «se procederá a la revisión». Con un lema: «primero "
          "revisar, después prometer». The frame bounds the borrowed register and keeps the irony "
          "legible.",
          [X("Suena a lenguaje administrativo: «se procederá a la revisión».", "SWEH-nah ah len-GWAH-heh ahd-mee-nees-trah-TEE-boh: seh proh-seh-deh-RAH ah lah reh-bee-SYOHN.", "It sounds like officialese: 'the review will be proceeded with'."),
           X("Con un lema: «primero revisar, después prometer».", "kohn oon LEH-mah: pree-MEH-roh reh-bee-SAR, des-PWEHS proh-meh-TEHR.", "As a motto: 'first review, then promise'."),
           X("El contraste es intencionado.", "el kohn-TRAHS-teh es een-ten-syoh-NAH-doh.", "The contrast is intentional.")],
          [("Se procederá a la revisión. (in an essay, unmarked)", "Suena a lenguaje administrativo: «…»", "An unmarked quotation reads as the author's own register."),
           ("Lema: somos los mejores.", "Lema: «primero revisar, después prometer».", "A motto compresses the argument rather than praising.")]),
        [D("Autor", "¿Suena bien este párrafo?", "SWEH-nah byehn EHS-teh PAR-rah-foh?", "Does this paragraph sound good?"),
         D("Editora", "Suena a lenguaje administrativo: «se procederá a la revisión».", "SWEH-nah ah len-GWAH-heh ahd-mee-nees-trah-TEE-boh: seh proh-seh-deh-RAH ah lah reh-bee-SYOHN.", "It sounds like officialese: 'the review will be proceeded with'."),
         D("Autor", "¿Lo acorto?", "loh ah-KOR-toh?", "Shall I shorten it?"),
         D("Editora", "O cítalo con marco — entonces el contraste trabaja para ti.", "oh SEE-tah-loh kohn MAR-koh — en-TOHN-sehs el kohn-TRAHS-teh trah-BAH-hah PAH-rah tee.", "Or quote it with a frame — then the contrast works for you.")],
        WS("Register worksheet", [
            T("Frame the borrowed register.", ["administrative language", "advertising language"],
              ["Suena a lenguaje administrativo: …", "Suena a publicidad: …"]),
            T("Compress the argument into a motto.", ["first review, then promise"],
              ["Lema: «primero revisar, después prometer»."]),
        ]))),
    ("es-c2-u3", "es-c2-l9", L(
        "El pronóstico calibrado: la incertidumbre con números",
        "Expert Spanish states its uncertainty on a scale: CONFIRMADO, PROBABLE, POSIBLE, NO "
        "DESCARTABLE, POCO PROBABLE — and names the horizon: A CORTO PLAZO, HASTA 2030. The "
        "forecast is only as good as the words around it.",
        [V("confirmado", "kohn-feer-MAH-doh", "confirmed", "adjective"),
         V("probable", "proh-BAH-bleh", "probable", "adjective"),
         V("no descartable", "noh des-kar-TAH-bleh", "cannot be ruled out", "phrase"),
         V("a corto plazo", "ah KOR-toh PLAH-soh", "in the short term", "phrase"),
         V("el pronóstico", "el proh-NOS-tee-koh", "forecast", "noun")],
        G("Uncertainty scale",
          "confirmado > probable > posible > no descartable > poco probable",
          "A corto plazo, una subida es probable; a largo plazo es posible, y una bajada no es "
          "descartable. Stating the horizon and the band makes a forecast falsifiable instead of "
          "rhetorical.",
          [X("A corto plazo, una subida es probable.", "ah KOR-toh PLAH-soh, OO-nah soo-BEE-dah es proh-BAH-bleh.", "In the short term a rise is probable."),
           X("Una bajada no es descartable.", "OO-nah bah-HAH-dah noh es des-kar-TAH-bleh.", "A decline cannot be ruled out."),
           X("El pronóstico vale hasta 2030.", "el proh-NOS-tee-koh BAH-leh AHS-tah dohs MEE-l treh-een-tah.", "The forecast holds until 2030.")],
          [("Va a subir.", "A corto plazo es probable que suba.", "A bare future assertion hides the horizon and the band."),
           ("Quizá posible.", "Posible, pero poco probable.", "Two hedges cancel; the scale takes one position.")]),
        [D("Jefe", "¿Cuál es su pronóstico?", "KWAHL es soo proh-NOS-tee-koh?", "What is your forecast?"),
         D("Analista", "A corto plazo, una subida es probable.", "ah KOR-toh PLAH-soh, OO-nah soo-BEE-dah es proh-BAH-bleh.", "In the short term a rise is probable."),
         D("Jefe", "¿Y a largo plazo?", "ee ah LAR-goh PLAH-soh?", "And in the long term?"),
         D("Analista", "Posible. Una bajada no es descartable.", "poh-SEE-bleh. OO-nah bah-HAH-dah noh es des-kar-TAH-bleh.", "Possible. A decline cannot be ruled out.")],
        WS("Forecast worksheet", [
            T("Place it on the scale.", ["probable in the short term", "cannot be ruled out", "held until 2030"],
              ["a corto plazo, probable", "no descartable", "válido hasta 2030"]),
            T("Name the horizon.", ["in the short term", "in the long term"],
              ["a corto plazo", "a largo plazo"]),
        ]))),
]

# ── the five half-step rungs ────────────────────────────────────────────────

HALFSTEPS["A1+"] = {
    "title": "Spanish A1+ — Getting around",
    "native": NATIVE,
    "goals": [
        "Ask the way, buy a ticket and name a landmark",
        "Say a phone number, an address and a price out loud",
        "Name the days, tell the time and make a plan — or refuse one politely",
    ],
    "units": [
        {"id": "A1+-U1", "title": "Por la ciudad", "lessons": [
            L("Derecha, izquierda, todo recto",
              "Directions are imperative and short: siga todo recto, luego gire a la derecha. Add "
              "«por favor» and the request is polite: ¿DÓNDE ESTÁ LA ESTACIÓN, POR FAVOR?",
              [V("todo recto", "TOH-doh REK-toh", "straight ahead", "adverb"),
               V("a la derecha", "ah lah deh-REH-chah", "to the right", "phrase"),
               V("a la izquierda", "ah lah ees-KYEHR-dah", "to the left", "phrase"),
               V("la esquina", "lah es-KEE-nah", "corner", "noun"),
               V("cerca", "SEHR-kah", "near", "adverb")],
              G("Directions and location",
                "siga todo recto · gire a la derecha · está en la esquina · está cerca",
                "Siga todo recto y gire a la izquierda en la esquina. La estación está cerca, a "
                "cinco minutos. The polite imperative of usted is the default with strangers.",
                [X("Siga todo recto, luego gire a la derecha.", "SEE-gah TOH-doh REK-toh, LWEH-goh HEE-reh ah lah deh-REH-chah.", "Go straight ahead, then turn right."),
                 X("La estación está en la esquina.", "lah es-tah-SYOHN es-TAH en lah es-KEE-nah.", "The station is on the corner."),
                 X("¿Está lejos de aquí?", "es-TAH LEH-hohs deh ah-KEE?", "Is it far from here?")],
                [("Vas todo recto y gira.", "Siga todo recto y gire.", "With a stranger the usted imperative is the polite default."),
                 ("Está a la esquina.", "Está en la esquina.", "Position takes en: en la esquina.")]),
              [D("Ben", "Perdón, ¿dónde está la estación, por favor?", "per-DOHN, DON-deh es-TAH lah es-tah-SYOHN, por fah-BOR?", "Excuse me, where is the station, please?"),
               D("Sra. Ruiz", "Siga todo recto y gire a la izquierda en la esquina.", "SEE-gah TOH-doh REK-toh ee HEE-reh ah lah ees-KYEHR-dah en lah es-KEE-nah.", "Go straight ahead and turn left at the corner."),
               D("Ben", "¿Está lejos?", "es-TAH LEH-hohs?", "Is it far?"),
               D("Sra. Ruiz", "No, cinco minutos andando.", "noh, SEEN-koh mee-NOO-tohs ahn-DAHN-doh.", "No, five minutes on foot.")],
              WS("Directions worksheet", [
                  T("Give the direction.", ["go straight ahead", "then left", "on the corner"],
                    ["Siga todo recto.", "luego a la izquierda", "en la esquina"]),
                  T("Ask and answer.", ["Where is the market? (nearby)", "Is it far? (no, five minutes on foot)"],
                    ["¿Dónde está el mercado? — Está cerca.", "¿Está lejos? — No, cinco minutos andando."]),
              ])),
            L("Billetes, paradas y tarifas",
              "Rides are bought with fixed lines: UN BILLETE PARA EL CENTRO, POR FAVOR · ¿CUÁNTO "
              "CUESTA? · PARE AQUÍ, POR FAVOR. Prices answer with the amount first.",
              [V("costar", "kos-TAR", "to cost", "verb"),
               V("la parada", "lah pah-RAH-dah", "stop (bus)", "noun"),
               V("parar", "pah-RAR", "to stop", "verb"),
               V("el autobús", "el ow-toh-BOOS", "bus", "noun"),
               V("sencillo", "sen-SEE-yoh", "single (ticket)", "adjective")],
              G("Fares and stops",
                "¿cuánto cuesta …? · un billete para … · pare aquí, por favor",
                "¿Cuánto cuesta un billete para el centro? Cuesta un euro cincuenta. Pare aquí, "
                "por favor. «¿Cuánto cuesta?» is the fast question; «¿cuánto es?» asks for the "
                "total.",
                [X("¿Cuánto cuesta el billete?", "KWAHN-toh KWEHS-tah el bee-YEH-teh?", "How much does the ticket cost?"),
                 X("Un billete sencillo, por favor.", "oon bee-YEH-teh sen-SEE-yoh, por fah-BOR.", "A single ticket, please."),
                 X("Pare en la próxima parada.", "PAH-reh en lah PROK-see-mah pah-RAH-dah.", "Stop at the next stop.")],
                [("¿Cuánto es cuesta?", "¿Cuánto cuesta?", "One question word per sentence."),
                 ("Pare a la parada.", "Pare en la parada.", "A stop is a place: en la parada.")]),
              [D("Ana", "¿Cuánto cuesta un billete para el centro?", "KWAHN-toh KWEHS-tah oon bee-YEH-teh PAH-rah el SEN-troh?", "How much is a ticket to the centre?"),
               D("Conductor", "Un euro cincuenta.", "oon EH-roh seen-KWEHN-tah.", "One euro fifty."),
               D("Ana", "Sencillo, por favor. ¿Me avisa en la plaza?", "sen-SEE-yoh, por fah-BOR. meh ah-BEE-sah en lah PLAH-sah?", "Single, please. Will you tell me at the square?"),
               D("Conductor", "Claro, la próxima parada es la plaza.", "KLAH-roh, lah PROK-see-mah pah-RAH-dah es lah PLAH-sah.", "Of course, the next stop is the square.")],
              WS("Fare worksheet", [
                  T("Say it in Spanish.", ["a ticket to the centre", "how much does it cost?", "stop here, please"],
                    ["un billete para el centro", "¿Cuánto cuesta?", "Pare aquí, por favor."]),
                  T("Answer as the driver.", ["one euro fifty", "the next stop"],
                    ["un euro cincuenta", "la próxima parada"]),
              ])),
            L("Puntos de referencia: enfrente, al lado, detrás",
              "Landmark relations: ENFRENTE DE (opposite), AL LADO DE (next to), DETRÁS DE, DELANTE "
              "DE. All three take de + noun.",
              [V("enfrente de", "en-FREHN-teh deh", "opposite, in front of", "phrase"),
               V("al lado de", "al LAH-doh deh", "next to", "phrase"),
               V("detrás de", "deh-TRAHS deh", "behind", "phrase"),
               V("el mercado", "el mer-KAH-doh", "market", "noun"),
               V("la farmacia", "lah far-MAH-syah", "pharmacy", "noun")],
              G("Position with de",
                "enfrente de la plaza · al lado del mercado · detrás del banco",
                "La farmacia está al lado del mercado, enfrente de la plaza. de + el = del; the "
                "relation word carries the position and the noun carries the landmark.",
                [X("La farmacia está al lado del mercado.", "lah far-MAH-syah es-TAH al LAH-doh del mer-KAH-doh.", "The pharmacy is next to the market."),
                 X("El banco está enfrente de la plaza.", "el BAHN-koh es-TAH en-FREHN-teh deh lah PLAH-sah.", "The bank is opposite the square."),
                 X("Hay un parque detrás del museo.", "eye oon PAR-keh deh-TRAHS del moo-SEH-oh.", "There is a park behind the museum.")],
                [("La farmacia está al lado el mercado.", "La farmacia está al lado del mercado.", "The relation takes de: al lado de + el = del."),
                 ("Está enfrente la plaza.", "Está enfrente de la plaza.", "The relation is a phrase: enfrente de.")]),
              [D("Ana", "¿Dónde está la farmacia?", "DON-deh es-TAH lah far-MAH-syah?", "Where is the pharmacy?"),
               D("Ben", "Al lado del mercado, enfrente de la plaza.", "al LAH-doh del mer-KAH-doh, en-FREHN-teh deh lah PLAH-sah.", "Next to the market, opposite the square."),
               D("Ana", "¿Y hay un banco cerca?", "ee eye oon BAHN-koh SEHR-kah?", "And is there a bank nearby?"),
               D("Ben", "Sí, detrás del museo.", "see, deh-TRAHS del moo-SEH-oh.", "Yes, behind the museum.")],
              WS("Landmark worksheet", [
                  T("Complete with the relation.", ["next to the market", "opposite the square", "behind the museum"],
                    ["al lado del mercado", "enfrente de la plaza", "detrás del museo"]),
                  T("Describe your street.", ["what is next to the pharmacy?", "what is opposite the bank?"],
                    ["Al lado de la farmacia hay …", "Enfrente del banco está …"]),
              ])),
        ]},
        {"id": "A1+-U2", "title": "Números que te llevan a casa", "lessons": [
            L("De once a cien",
              "Spanish numbers run in one word to thirty, then join with y: DIECISÉIS, VEINTIUNO, "
              "TREINTA Y CUATRO. Hundreds are DOSCIENTOS, TRESCIENTOS.",
              [V("once", "OHN-seh", "eleven", "numeral"),
               V("veinte", "BAYN-teh", "twenty", "numeral"),
               V("veintiuno", "bayn-tee-OO-noh", "twenty-one", "numeral"),
               V("treinta y cuatro", "TRAYN-tah ee KWAH-troh", "thirty-four", "numeral"),
               V("cien", "syen", "one hundred", "numeral")],
              G("Numbers to a hundred",
                "16–29 in one word · 31+ with y · 100 cien / 101 ciento uno",
                "Veintiuno, veintidós, veintitrés; treinta y uno, treinta y dos. The numbers with "
                "an accent (dieciséis, veintidós) are written with one — that accent is the only "
                "spelling risk in this lesson.",
                [X("Tengo veintiún años.", "TEN-goh bayn-tee-OON AH-nyohs.", "I am twenty-one years old."),
                 X("Cuesta treinta y cuatro euros.", "KWEHS-tah TRAYN-tah ee KWAH-troh EH-rohs.", "It costs thirty-four euros."),
                 X("Somos cien personas.", "SOH-mohs syen per-SOH-nahs.", "We are a hundred people.")],
                [("Treinticuatro.", "treinta y cuatro", "From thirty-one the numbers are written separately with y."),
                 ("Veintiuno años.", "veintiún años", "Before a masculine noun veintiuno shortens to veintiún.")]),
              [D("Ana", "¿Cuántos años tiene tu hermano?", "KWAHN-tohs AH-nyohs TYEH-neh too ehr-MAH-noh?", "How old is your brother?"),
               D("Ben", "Veintiún años. Mi hermana tiene treinta y cuatro.", "bayn-tee-OON AH-nyohs. mee ehr-MAH-nah TYEH-neh TRAYN-tah ee KWAH-troh.", "Twenty-one. My sister is thirty-four."),
               D("Ana", "¿Y cuántos primos tienes?", "ee KWAHN-tohs PREE-mohs TYEH-nehs?", "And how many cousins do you have?"),
               D("Ben", "Muchos: veintiocho, creo.", "MOO-chohs: bayn-tee-OH-choh, KREH-oh.", "Many: twenty-eight, I think.")],
              WS("Numbers worksheet", [
                  T("Write the number in Spanish words.", ["16", "21", "34", "99"],
                    ["dieciséis", "veintiuno", "treinta y cuatro", "noventa y nueve"]),
                  T("Say the price in full.", ["ticket: €9.50", "two books: €120"],
                    ["nueve euros cincuenta", "ciento veinte euros"]),
              ])),
            L("Teléfonos y direcciones",
              "Phone numbers are read in pairs, and addresses run CALLE, NÚMERO, PISO: CALLE MAYOR, "
              "QUINCE, TERCERO. Asking: ¿ME DAS TU NÚMERO? · ¿PUEDES DELETREARLO?",
              [V("deletrear", "deh-leh-treh-AR", "to spell out", "verb"),
               V("la calle", "lah KAH-yeh", "street", "noun"),
               V("el número", "el NOO-meh-roh", "number", "noun"),
               V("el piso", "el PEE-soh", "floor, flat", "noun"),
               V("el código postal", "el KOH-dee-goh pos-TAL", "postcode", "noun")],
              G("Address and phone frame",
                "calle + nombre, número · ¿me das tu número? · ¿puedes deletrearlo?",
                "Vivo en la calle Mayor, número quince, tercero. Mi número es seis-siete-cuatro, "
                "dos-uno-cero. The street takes «en la calle»; the number follows without a "
                "preposition.",
                [X("Vivo en la calle Mayor, quince.", "BEE-voh en lah KAH-yeh mah-YOR, KEEN-seh.", "I live at 15 Calle Mayor."),
                 X("¿Me das tu número de teléfono?", "meh dahs too NOO-meh-roh deh teh-LEH-foh-noh?", "Will you give me your phone number?"),
                 X("¿Puedes deletrear tu apellido?", "PWEH-dehs deh-leh-treh-AR too ah-peh-YEE-doh?", "Can you spell your surname?")],
                [("Vivo en calle Mayor 15.", "Vivo en la calle Mayor, quince.", "Street names take the article: la calle Mayor."),
                 ("Mi número es seiscientos setenta y cuatro.", "Mi número es seis-siete-cuatro…", "Phone numbers are read in digits or pairs, never as one big number.")]),
              [D("Ben", "¿Me das tu dirección?", "meh dahs too dee-rek-SYOHN?", "Will you give me your address?"),
               D("Ana", "Calle Mayor, quince, tercero.", "KAH-yeh mah-YOR, KEEN-seh, ter-SEH-roh.", "15 Calle Mayor, third floor."),
               D("Ben", "¿Y el código postal?", "ee el KOH-dee-goh pos-TAL?", "And the postcode?"),
               D("Ana", "Cuatro-uno-cero, cero-dos.", "KWAH-troh-OO-noh-SEH-roh, SEH-roh-dohs.", "Four-one-zero, zero-two.")],
              WS("Address worksheet", [
                  T("Say it in Spanish.", ["my address", "number fifteen", "can you spell it?"],
                    ["mi dirección", "número quince", "¿Puedes deletrearlo?"]),
                  T("Ask for the details.", ["your phone number?", "your postcode?"],
                    ["¿Me das tu número?", "¿Cuál es tu código postal?"]),
              ])),
            L("Precios: caro, barato, un poco menos",
              "Bargaining is normal in markets: ¿ME HACE UN PRECIO? · ES MUY CARO · ¿Y SI ME LO "
              "DEJA EN VEINTE? The question keeps it friendly and the conditional softens it.",
              [V("caro", "KAH-roh", "expensive", "adjective"),
               V("barato", "bah-RAH-toh", "cheap", "adjective"),
               V("el precio", "el PREH-syoh", "price", "noun"),
               V("rebajar", "reh-bah-HAR", "to lower the price", "verb"),
               V("la oferta", "lah oh-FEHR-tah", "offer, deal", "noun")],
              G("Price talk",
                "es muy caro · ¿me hace un precio? · ¿y si … ?",
                "Es un poco caro — ¿me hace un precio? ¿Y si me lo deja en veinte? «me lo deja en "
                "veinte» is the market formula: leave it to me at twenty.",
                [X("Es un poco caro.", "es oon POH-koh KAH-roh.", "It is a little expensive."),
                 X("¿Me hace un precio?", "meh AH-seh oon PREH-syoh?", "Can you make me a price?"),
                 X("¿Y si me lo deja en veinte?", "ee see meh loh DEH-hah en BAYN-teh?", "What if you leave it to me at twenty?")],
                [("Yo soy caro.", "Es caro.", "The price is expensive, not the person."),
                 ("Rebaja, ¿sí?", "¿Me hace un precio?", "The question keeps the market friendly.")]),
              [D("Ana", "¿Cuánto cuesta la bolsa?", "KWAHN-toh KWEHS-tah lah BOL-sah?", "How much is the bag?"),
               D("Vendedor", "Treinta euros.", "TRAYN-tah EH-rohs.", "Thirty euros."),
               D("Ana", "Es un poco caro. ¿Me hace un precio?", "es oon POH-koh KAH-roh. meh AH-seh oon PREH-syoh?", "It's a little expensive. Can you make me a price?"),
               D("Vendedor", "Veinticinco, y no menos.", "bayn-tee-SEEN-koh, ee noh MEH-nohs.", "Twenty-five, and no less.")],
              WS("Price worksheet", [
                  T("Bargain politely.", ["that's a bit expensive", "can you make me a price?", "twenty-five and no less"],
                    ["Es un poco caro.", "¿Me hace un precio?", "Veinticinco y no menos."]),
                  T("Answer as the seller.", ["the price is thirty euros", "a special offer"],
                    ["El precio es treinta euros.", "Es una oferta."]),
              ])),
        ]},
        {"id": "A1+-U3", "title": "Días, horas, planes", "lessons": [
            L("La semana: de lunes a domingo",
              "Days are lowercase and take el: EL LUNES. A range uses DE … A …: DE LUNES A VIERNES. "
              "The weekend is EL FIN DE SEMANA.",
              [V("el lunes", "el LOO-nehs", "Monday", "noun"),
               V("el viernes", "el BYEHR-nehs", "Friday", "noun"),
               V("el fin de semana", "el feen deh seh-MAH-nah", "weekend", "noun"),
               V("la semana", "lah seh-MAH-nah", "week", "noun"),
               V("de … a …", "deh … ah", "from … to", "phrase")],
              G("Days with el",
                "el lunes · de lunes a viernes · el fin de semana",
                "El lunes trabajo. El fin de semana descanso. Which day: ¿QUÉ DÍA ES HOY? — HOY ES "
                "MARTES. Days are not capitalised in Spanish.",
                [X("El lunes no tengo tiempo.", "el LOO-nehs noh TEN-goh TYEHM-poh.", "On Monday I have no time."),
                 X("De lunes a viernes trabajo.", "deh LOO-nehs ah BYEHR-nehs trah-BAH-hoh.", "From Monday to Friday I work."),
                 X("El fin de semana descanso.", "el feen deh seh-MAH-nah des-KAHN-soh.", "At the weekend I rest.")],
                [("En lunes trabajo.", "El lunes trabajo.", "Days take el, not en, for a single occurrence."),
                 ("De lunes a el viernes.", "De lunes a viernes.", "The second day drops the article.")]),
              [D("Ben", "¿Qué día es hoy?", "keh DEE-ah es oy?", "What day is today?"),
               D("Ana", "Hoy es jueves.", "oy es HWEH-vehs.", "Today is Thursday."),
               D("Ben", "¿Y cuándo tienes tiempo?", "ee KWAHN-doh TYEH-nehs TYEHM-poh?", "And when do you have time?"),
               D("Ana", "El viernes por la tarde estoy libre.", "el BYEHR-nehs por lah TAR-deh es-TOY LEE-breh.", "On Friday afternoon I'm free.")],
              WS("Days worksheet", [
                  T("Answer in Spanish.", ["what day is today? (Tuesday)", "when do you work? (Monday to Friday)", "the weekend"],
                    ["Hoy es martes.", "De lunes a viernes trabajo.", "el fin de semana"]),
                  T("Plan your week.", ["a working day", "a free day"],
                    ["El … trabajo.", "El … estoy libre."]),
              ])),
            L("La hora: y media, y cuarto, menos cuarto",
              "Clock time uses SON LAS + number: SON LAS TRES Y MEDIA (3:30), SON LAS CUATRO MENOS "
              "CUARTO (3:45). One o'clock is ES LA UNA because it is singular.",
              [V("y media", "ee MEH-dyah", "half past", "phrase"),
               V("y cuarto", "ee KWAHR-toh", "quarter past", "phrase"),
               V("menos cuarto", "MEH-nohs KWAHR-toh", "quarter to", "phrase"),
               V("la hora", "lah OH-rah", "hour, time", "noun"),
               V("en punto", "en POON-toh", "on the dot", "phrase")],
              G("Clock Spanish",
                "es la una · son las + hour + y/menos …",
                "Es la una en punto. Son las tres y media. Son las cuatro menos cuarto. Spanish "
                "counts minutes forward to the half and backwards after it — «cuatro menos cuarto» "
                "is 3:45.",
                [X("Es la una en punto.", "es lah OO-nah en POON-toh.", "It is one o'clock exactly."),
                 X("Son las siete y cuarto.", "sohn lahs SYEH-teh ee KWAHR-toh.", "It is a quarter past seven."),
                 X("La reunión es a las cuatro menos cuarto.", "lah reh-YOHN es ah lahs KWAH-troh MEH-nohs KWAHR-toh.", "The meeting is at a quarter to four.")],
                [("Son la una.", "Es la una.", "One o'clock is singular: es la una."),
                 ("Son las cinco y cuarenta y cinco.", "Son las seis menos cuarto.", "Standard speech prefers menos cuarto to the exact minute.")]),
              [D("Ana", "¿Qué hora es?", "keh OH-rah es?", "What time is it?"),
               D("Ben", "Son las tres y media.", "sohn lahs trehs ee MEH-dyah.", "It is half past three."),
               D("Ana", "¿A qué hora es la película?", "ah keh OH-rah es lah peh-LEE-koo-lah?", "What time is the film?"),
               D("Ben", "A las cuatro menos cuarto, en el centro.", "ah lahs KWAH-troh MEH-nohs KWAHR-toh, en el SEN-troh.", "At a quarter to four, in the centre.")],
              WS("Clock worksheet", [
                  T("Say the time in Spanish.", ["3:00", "3:30", "3:45", "1:00"],
                    ["son las tres", "son las tres y media", "son las cuatro menos cuarto", "es la una"]),
                  T("Answer the question.", ["When is the film? (at 6:30)", "When shall we meet? (at 9:15)"],
                    ["A las seis y media.", "A las nueve y cuarto."]),
              ])),
            L("Hacer planes y decir que no con educación",
              "Plans open with ¿TE APETECE …? or PODEMOS …; refusals come with a reason and an "
              "alternative: HOY NO PUEDO, PERO MAÑANA SÍ.",
              [V("apetecer", "ah-peh-teh-SEHR", "to feel like", "verb"),
               V("quedar", "keh-DAR", "to arrange to meet", "verb"),
               V("lo siento", "loh SYEHN-toh", "I'm sorry", "phrase"),
               V("mañana", "mah-NYAH-nah", "tomorrow", "adverb"),
               V("otro día", "OH-troh DEE-ah", "another day", "phrase")],
              G("Invite, refuse, re-offer",
                "¿te apetece …? · hoy no puedo · pero mañana sí",
                "¿Te apetece un café? — Hoy no puedo, lo siento; mañana sí. The refusal names the "
                "time, not the person, and offers another one in the same breath.",
                [X("¿Te apetece un café?", "teh ah-peh-TEH-seh oon kah-FEH?", "Do you feel like a coffee?"),
                 X("Hoy no puedo, lo siento.", "oy noh PWEH-doh, loh SYEHN-toh.", "I can't today, sorry."),
                 X("Pero mañana sí.", "PEH-roh mah-NYAH-nah see.", "But tomorrow yes.")],
                [("No puedo no.", "No puedo.", "One negation per clause."),
                 ("¿Te apeteces un café?", "¿Te apetece un café?", "apetecer agrees with the thing: apetece.")]),
              [D("Ana", "¿Te apetece ir al cine el sábado?", "teh ah-peh-TEH-seh eer al SEE-neh el SAH-bah-doh?", "Do you feel like going to the cinema on Saturday?"),
               D("Ben", "El sábado no puedo, lo siento — trabajo.", "el SAH-bah-doh noh PWEH-doh, loh SYEHN-toh — trah-BAH-hoh.", "Saturday I can't, sorry — I'm working."),
               D("Ana", "¿Y el domingo?", "ee el doh-MEEN-goh?", "And Sunday?"),
               D("Ben", "El domingo sí. ¿A las seis?", "el doh-MEEN-goh see. ah lahs says?", "Sunday yes. At six?")],
              WS("Plan worksheet", [
                  T("Make the plan.", ["feel like a coffee?", "the cinema on Sunday", "at six"],
                    ["¿Te apetece un café?", "el cine el domingo", "a las seis"]),
                  T("Refuse and offer another day.", ["refuse Saturday, offer Sunday", "refuse today, offer tomorrow"],
                    ["El sábado no puedo — el domingo sí.", "Hoy no puedo — mañana sí."]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Getting around a Spanish city means trusting the walk more than the timetable: "
                 "most historic centres are compact, the metro runs late, and the taxi from the "
                 "station is short and fixed. The vocabulary of the half-step is therefore mostly "
                 "signs and relations — parada, andén, esquina, al lado de — because reading the "
                 "street is what actually gets a learner home."),
        source_url="https://en.wikipedia.org/wiki/Renfe",
        reading=("El sábado voy a Sevilla. El tren sale a las nueve y cuarto del andén cuatro. El "
                 "billete cuesta diecinueve euros y no hay que hacer transbordo. En la estación "
                 "tomo un café y miro el panel: el tren lleva cinco minutos de retraso. Llego al "
                 "centro andando, porque la estación está cerca."),
        reading_gloss=("On Saturday I'm going to Seville. The train leaves at a quarter past nine "
                       "from platform four. The ticket costs nineteen euros and there is no change "
                       "to make. At the station I have a coffee and look at the board: the train is "
                       "five minutes late. I reach the centre on foot, because the station is "
                       "close."),
        listening=("Ben: ¿Dónde está el andén cuatro?<br>Ana: Todo recto y a la izquierda, al lado de la farmacia.<br>"
                   "Ben: Gracias. ¿A qué hora sale?<br>Ana: A las nueve y cuarto — quedan cinco minutos."),
        listening_gloss=("Ben: Where is platform four? Ana: Straight ahead and to the left, next to "
                         "the pharmacy. Ben: Thanks. What time does it leave? Ana: At a quarter "
                         "past nine — five minutes left."),
        voice_tag=VOICE,
        idioms=[
            ("A pie", "on foot", "walking"),
            ("A la vuelta de la esquina", "at the turn of the corner", "just around the corner"),
            ("Buen viaje", "good trip", "have a good trip"),
            ("Ida y vuelta", "going and return", "a return ticket"),
            ("En punto", "on the dot", "exactly on time"),
            ("Ir al grano", "to go to the grain", "to get to the point"),
            ("Perderse", "to lose oneself", "to get lost"),
            ("Estar a dos pasos", "to be two steps away", "to be a stone's throw away"),
            ("Preguntar por el camino", "to ask for the way", "to ask for directions"),
            ("Ir andando", "to go walking", "to walk there"),
        ],
        mistakes=[
            ("Son la una.", "Es la una.", "One o'clock is singular."),
            ("El tren sale a las nueve y cuarto en el andén cuatro.", "El tren sale a las nueve y cuarto del andén cuatro.", "Trains leave from a platform: del andén."),
            ("Voy a pie a la estación andando.", "Voy a pie a la estación. / Voy andando a la estación.", "One expression of walking is enough."),
        ],
        task_title="Direct someone across your city",
        task_instructions=("Write six Spanish steps from your home to a place you go often: two "
                           "landmarks (al lado de, enfrente de), one ticket or fare question, and "
                           "one time (y media, menos cuarto). Give it to someone who must follow it "
                           "without asking you anything. Where they hesitate, the missing word is "
                           "almost always a relation — al lado de, enfrente de, detrás de."),
    ),
    "test": [
        ("translate_en", "Say: Where is the station, please?", "¿Dónde está la estación, por favor?"),
        ("translate_es", "Siga todo recto y gire a la izquierda en la esquina.", "Go straight ahead and turn left at the corner."),
        ("multiple_choice", "Which is the polite request?", "¿Me hace un precio?"),
        ("fill_in_the_blank", "¿Cuánto ___ un billete para el centro?", "cuesta"),
        ("word_selection", "Select the Spanish for twenty-one.", "veintiuno"),
        ("error_correction", "La farmacia está al lado el mercado.", "La farmacia está al lado del mercado."),
        ("dialogue_completion", "Complete: ¿Cuánto cuesta? — ___ (one euro fifty)", "un euro cincuenta"),
        ("matching", "Match «enfrente de» to its meaning.", "opposite"),
        ("reading_comprehension", "El tren sale del andén cuatro. Which platform?", "cuatro"),
        ("inference", "«Es un poco caro» — what is the speaker doing?", "bargaining politely"),
        ("main_idea", "De lunes a viernes trabajo. What is this about?", "the working week"),
        ("detail_identification", "Son las tres y media. What time is it?", "3:30"),
    ],
}

HALFSTEPS["A2+"] = {
    "title": "Spanish A2+ — Day-to-day business",
    "native": NATIVE,
    "goals": [
        "Return, exchange and complain about a purchase without losing your temper or your grammar",
        "Run a phone call: answer, take a message, arrange a time and apologise for being late",
        "Talk about how the neighbourhood used to be, and say what happened yesterday",
    ],
    "units": [
        {"id": "A2+-U1", "title": "Compras, cambios y reclamaciones", "lessons": [
            L("Cambiar y devolver: la talla, el recibo",
              "Returns run on four words: LA TALLA (size), EL RECIBO (receipt), CAMBIAR (exchange) "
              "and DEVOLVER (refund). ¿ME LO PUEDE CAMBIAR POR UNA TALLA MÁS?",
              [V("la talla", "lah TAH-yah", "size (clothes)", "noun"),
               V("el recibo", "el reh-SEE-boh", "receipt", "noun"),
               V("cambiar", "kahm-BYAR", "to exchange", "verb"),
               V("devolver", "deh-bol-VEHR", "to return, to refund", "verb"),
               V("probarse", "proh-BAR-seh", "to try on", "verb")],
              G("Return frame",
                "¿me lo puede cambiar? · quiero devolver … · con el recibo",
                "Compré esta camisa ayer y me queda pequeña. ¿Me la puede cambiar por una talla "
                "más? — Con el recibo, claro. «Me queda» is how clothes judge you in Spanish.",
                [X("Me queda pequeña.", "meh KEH-dah peh-KEH-nyah.", "It is too small for me."),
                 X("¿Me lo puede cambiar por una talla más?", "meh loh PWEH-deh kahm-BYAR por OO-nah TAH-yah mahs?", "Can you exchange it for a bigger size?"),
                 X("Quiero devolver esto, tengo el recibo.", "KYEH-roh deh-bol-VEHR EHS-toh, TEN-goh el reh-SEE-boh.", "I want to return this, I have the receipt.")],
                [("Quiero devolver esto sin el recibo.", "Quiero devolver esto; tengo el recibo.", "The receipt is the whole negotiation."),
                 ("Me queda pequeño la camisa.", "La camisa me queda pequeña.", "The thing is the subject; the adjective agrees with it.")]),
              [D("Ben", "Buenas, compré esta camisa ayer y me queda pequeña.", "BWEH-nahs, kohm-PREH EHS-tah kah-MEE-sah ah-YEHR ee meh KEH-dah peh-KEH-nyah.", "Hi, I bought this shirt yesterday and it is too small for me."),
               D("Dependienta", "¿Tiene el recibo?", "TYEH-neh el reh-SEE-boh?", "Do you have the receipt?"),
               D("Ben", "Sí, aquí está.", "see, ah-KEE es-TAH.", "Yes, here it is."),
               D("Dependienta", "Perfecto. ¿Se la cambio por una talla más?", "per-FEK-toh. seh lah KAHM-byoh por OO-nah TAH-yah mahs?", "Perfect. Shall I exchange it for a bigger size?")],
              WS("Returns worksheet", [
                  T("Say what is wrong.", ["the shirt is too small", "the trousers are too long"],
                    ["La camisa me queda pequeña.", "Los pantalones me quedan largos."]),
                  T("Make the request.", ["exchange it for a bigger size", "return it, I have the receipt"],
                    ["¿Me lo puede cambiar por una talla más?", "Quiero devolverlo, tengo el recibo."]),
              ])),
            L("En el probador: tallas, colores, precios",
              "Trying clothes on: ¿PUEDO PASAR AL PROBADOR? · ¿LO TIENE EN AZUL? · ME LO LLEVO. The "
              "shops are small, so «¿lo tiene?» is the question that saves a trip.",
              [V("el probador", "el proh-bah-DOR", "fitting room", "noun"),
               V("quedar bien", "keh-DAR byehn", "to suit, to fit well", "phrase"),
               V("llevarse", "yeh-VAR-seh", "to take (buy)", "verb"),
               V("el escaparate", "el es-kah-pah-RAH-teh", "shop window", "noun"),
               V("la rebaja", "lah reh-BAH-hah", "sale, discount", "noun")],
              G("Shopping phrases",
                "¿puedo pasar al probador? · ¿lo tiene en azul? · me lo llevo",
                "¿Puedo pasar al probador? ¿Lo tiene en azul, en la cuarenta? Me lo llevo. In "
                "Spain the size is often spoken as a number — la cuarenta — with no word for "
                "size at all.",
                [X("¿Puedo pasar al probador?", "PWEH-doh pah-SAR al proh-bah-DOR?", "May I go to the fitting room?"),
                 X("¿Lo tiene en azul?", "loh TYEH-neh en ah-SOOL?", "Do you have it in blue?"),
                 X("Me lo llevo.", "meh loh YEH-voh.", "I'll take it.")],
                [("Quiero probármelo la camisa.", "Quiero probarme la camisa.", "The reflexive pronoun goes with the verb: probarme."),
                 ("¿Lo tiene azul?", "¿Lo tiene en azul?", "Colours take en when you buy them.")]),
              [D("Ana", "¿Puedo pasar al probador con estos dos?", "PWEH-doh pah-SAR al proh-bah-DOR kohn EHS-tohs dohs?", "May I go to the fitting room with these two?"),
               D("Dependiente", "Claro, al fondo a la derecha.", "KLAH-roh, al FON-doh ah lah deh-REH-chah.", "Of course, at the back on the right."),
               D("Ana", "Este me queda bien. ¿Lo tiene en azul?", "EHS-teh meh KEH-dah byehn. loh TYEH-neh en ah-SOOL?", "This one fits well. Do you have it in blue?"),
               D("Dependiente", "En azul solo queda la cuarenta.", "en ah-SOOL SOH-loh KEH-dah lah kwah-REN-tah.", "In blue there is only the forty left.")],
              WS("Fitting-room worksheet", [
                  T("Ask in the shop.", ["May I try it on?", "Do you have it in blue?", "I'll take it."],
                    ["¿Puedo probármelo?", "¿Lo tiene en azul?", "Me lo llevo."]),
                  T("Say how it fits.", ["it fits well", "it is too big"],
                    ["Me queda bien.", "Me queda grande."]),
              ])),
            L("Reclamar con educación: no funciona, falta…",
              "A complaint is a fact plus a request: NO FUNCIONA (it does not work), LE FALTA UN "
              "BOTÓN (a button is missing), ¿PUEDE MIRARLO? Keep the tone flat and the request "
              "explicit.",
              [V("funcionar", "foon-syoh-NAR", "to work (device)", "verb"),
               V("faltar", "fahl-TAR", "to be missing", "verb"),
               V("la garantía", "lah gah-rahn-TEE-ah", "warranty", "noun"),
               V("arreglar", "ah-rreh-GLAR", "to repair", "verb"),
               V("reclamar", "reh-klah-MAR", "to complain, to claim", "verb")],
              G("Complaint frame",
                "no funciona · le falta … · está en garantía · ¿puede mirarlo?",
                "Compré este reloj la semana pasada y no funciona. Le falta una pieza. Está en "
                "garantía — ¿puede mirarlo? The polite request is the complaint's engine.",
                [X("Compré este reloj y no funciona.", "kohm-PREH EHS-teh reh-LOH ee noh foon-SYOH-nah.", "I bought this watch and it does not work."),
                 X("Le falta una pieza.", "leh FAHL-tah OO-nah PYEH-sah.", "A part is missing."),
                 X("Está en garantía, ¿puede mirarlo?", "es-TAH en gah-rahn-TEE-ah, PWEH-deh mee-RAR-loh?", "It is under warranty — can you look at it?")],
                [("No funciona nada nunca.", "No funciona.", "One fact per complaint; hyperbole weakens it."),
                 ("¿Puede mirar? (no object)", "¿Puede mirarlo?", "The request needs its object pronoun.")]),
              [D("Ana", "Buenas tardes. Compré este reloj aquí y no funciona.", "BWEH-nahs TAR-dehs. kohm-PREH EHS-teh reh-LOH ah-KEE ee noh foon-SYOH-nah.", "Good afternoon. I bought this watch here and it does not work."),
               D("Encargado", "¿Trae la garantía?", "TRAH-eh lah gah-rahn-TEE-ah?", "Do you have the warranty with you?"),
               D("Ana", "Sí, y le falta una pieza.", "see, ee leh FAHL-tah OO-nah PYEH-sah.", "Yes, and a part is missing."),
               D("Encargado", "Lo miramos y, si no se arregla, se lo cambiamos.", "loh mee-RAH-mohs ee, see noh seh ah-RREH-glah, seh loh kahm-BYAH-mohs.", "We'll look at it and, if it can't be repaired, we'll exchange it.")],
              WS("Complaint worksheet", [
                  T("State the problem and the request.", ["it doesn't work — can you look at it?", "a part is missing — it's under warranty"],
                    ["No funciona, ¿puede mirarlo?", "Le falta una pieza, está en garantía."]),
                  T("Ask what happens next.", ["can it be repaired?", "can it be exchanged?"],
                    ["¿Se puede arreglar?", "¿Se puede cambiar?"]),
              ])),
        ]},
        {"id": "A2+-U2", "title": "Por teléfono y de quedada", "lessons": [
            L("Llamar y contestar: ¿dígame?",
              "Spanish phones answer with DÍGAME (tell me). Messages run: ¿ESTÁ …? · SOY … · ¿DE "
              "PARTE DE QUIÉN? · LE DEJO UN RECADO.",
              [V("dígame", "DEE-gah-meh", "hello (on the phone)", "verb"),
               V("el recado", "el reh-KAH-doh", "message", "noun"),
               V("de parte de", "deh PAR-teh deh", "on behalf of", "phrase"),
               V("la llamada", "lah yah-MAH-dah", "call", "noun"),
               V("colgar", "kol-GAR", "to hang up", "verb")],
              G("Phone frame",
                "¿dígame? · soy … · ¿de parte de quién? · le dejo un recado",
                "¿Dígame? — Hola, soy Ana. ¿Está Ben? — No está ahora. ¿De parte de quién? — De "
                "parte de la agencia. «Soy», not «estoy»: on the phone you are your name.",
                [X("¿Dígame?", "DEE-gah-meh?", "Hello? (on the phone)"),
                 X("Soy Ana, de parte de la agencia.", "soy AH-nah, deh PAR-teh deh lah ah-HEN-syah.", "It's Ana, from the agency."),
                 X("¿Puedo dejarle un recado?", "PWEH-doh deh-HAR-leh oon reh-KAH-doh?", "Can I leave a message?")],
                [("Estoy Ana.", "Soy Ana.", "On the phone you use ser: soy."),
                 ("¿Dígame quién es?", "¿De parte de quién?", "The fixed phrase is de parte de quién.")]),
              [D("Recepcionista", "Despacho de Ruiz, ¿dígame?", "des-PAH-choh deh RWEES, DEE-gah-meh?", "Ruiz's office, hello?"),
               D("Ana", "Buenos días, soy Ana. ¿Está la señora Ruiz?", "BWEH-nohs DEE-ahs, soy AH-nah. es-TAH lah seh-NYOH-rah RWEES?", "Good morning, it's Ana. Is Mrs Ruiz in?"),
               D("Recepcionista", "Está en una reunión. ¿De parte de quién?", "es-TAH en OO-nah reh-YOHN. deh PAR-teh deh KYEN?", "She is in a meeting. Who is calling?"),
               D("Ana", "De parte de la agencia. ¿Puedo dejarle un recado?", "deh PAR-teh deh lah ah-HEN-syah. PWEH-doh deh-HAR-leh oon reh-KAH-doh?", "From the agency. Can I leave a message?")],
              WS("Phone worksheet", [
                  T("Run the call.", ["hello? (answering)", "it's Ben", "can I leave a message?"],
                    ["¿Dígame?", "Soy Ben.", "¿Puedo dejar un recado?"]),
                  T("Ask who is calling.", ["who is it from?", "is Ana in?"],
                    ["¿De parte de quién?", "¿Está Ana?"]),
              ])),
            L("Citas y retrasos: disculparse por llegar tarde",
              "Arranging the time is one line — ¿QUEDAMOS A LAS SIETE? — and apologising is another: "
              "PERDONA EL RETRASO, SE ME HA HECHO TARDE.",
              [V("quedar", "keh-DAR", "to arrange to meet", "verb"),
               V("el retraso", "el reh-TRAH-soh", "delay", "noun"),
               V("perdona", "per-DOH-nah", "sorry, forgive me (tú)", "verb"),
               V("el atasco", "el ah-TAHS-koh", "traffic jam", "noun"),
               V("llegar", "yeh-GAR", "to arrive", "verb")],
              G("Meeting and lateness",
                "¿quedamos a las …? · perdona el retraso · se me ha hecho tarde",
                "¿Quedamos a las siete en el bar? — Vale. — Perdona el retraso, había un atasco. "
                "«Se me ha hecho tarde» blames the clock, which is the polite Spanish way.",
                [X("¿Quedamos a las siete?", "keh-DAH-mohs ah lahs SYEH-teh?", "Shall we meet at seven?"),
                 X("Perdona el retraso, había un atasco.", "per-DOH-nah el reh-TRAH-soh, ah-BEE-ah oon ah-TAHS-koh.", "Sorry I'm late, there was a traffic jam."),
                 X("Se me ha hecho tarde.", "seh meh ah EH-choh TAR-deh.", "It got late on me.")],
                [("Perdóname por el retraso.", "Perdona el retraso.", "Blunt the apology: perdona + noun, no clause."),
                 ("Llegué tarde porque yo quiero.", "Se me ha hecho tarde.", "The accidental se me frame removes the blame.")]),
              [D("Ben", "¿Quedamos a las siete en el bar?", "keh-DAH-mohs ah lahs SYEH-teh en el bar?", "Shall we meet at seven in the bar?"),
               D("Ana", "Vale. Pero voy justa — perdona el retraso por adelantado.", "BAH-leh. PEH-roh boy HOOS-tah — per-DOH-nah el reh-TRAH-soh por ah-deh-lahn-TAH-doh.", "OK. But I'm cutting it fine — sorry in advance for being late."),
               D("Ben", "Tranquila. A las siete y cuarto también me vale.", "trahn-KEE-lah. ah lahs SYEH-teh ee KWAHR-toh tahm-BYEHN meh BAH-leh.", "No problem. A quarter past seven works for me too."),
               D("Ana", "Pues a las siete y cuarto. ¡Hasta luego!", "pwehs ah lahs SYEH-teh ee KWAHR-toh. AHS-tah LWEH-goh!", "Quarter past seven then. See you!")],
              WS("Appointments worksheet", [
                  T("Fix the time and apologise.", ["shall we meet at seven?", "sorry I'm late, there was a traffic jam"],
                    ["¿Quedamos a las siete?", "Perdona el retraso, había un atasco."]),
                  T("Answer as the other person.", ["quarter past seven works for me", "no problem, see you"],
                    ["A las siete y cuarto me vale.", "Tranquila, hasta luego."]),
              ])),
            L("Invitar y agradecer: quedar en casa",
              "Guests are invited with TE INVITO A …; thanks are answered with DE NADA, NADA, or "
              "the more generous A MANDAR.",
              [V("invitar", "een-bee-TAR", "to invite, to treat", "verb"),
               V("agradecer", "ah-grah-deh-SEHR", "to thank", "verb"),
               V("de nada", "deh NAH-dah", "you're welcome", "phrase"),
               V("la quedada", "lah keh-DAH-dah", "meet-up", "noun"),
               V("traer", "trah-EHR", "to bring", "verb")],
              G("Inviting and thanking",
                "te invito a cenar · gracias por todo · de nada · a mandar",
                "Te invito a cenar el viernes en casa. Trae algo de postre, si quieres. — Gracias "
                "por todo. — De nada, a mandar. «A mandar» is the warm southern answer to thanks.",
                [X("Te invito a cenar en casa.", "teh een-BEE-toh ah seh-NAR en KAH-sah.", "I'm inviting you to dinner at home."),
                 X("Gracias por todo.", "GRAH-syahs por TOH-doh.", "Thanks for everything."),
                 X("De nada, a mandar.", "deh NAH-dah, ah mahn-DAR.", "You're welcome, at your service.")],
                [("Gracias para todo.", "Gracias por todo.", "Thanks take por: gracias por."),
                 ("Te invito a que cenas.", "Te invito a cenar.", "The invitation takes the infinitive.")]),
              [D("Ana", "Te invito a cenar el viernes en casa.", "teh een-BEE-toh ah seh-NAR el BYEHR-nehs en KAH-sah.", "I'm inviting you to dinner at home on Friday."),
               D("Ben", "Gracias, ¿traigo algo?", "GRAH-syahs, TRAH-ee-goh AHL-goh?", "Thanks, shall I bring something?"),
               D("Ana", "Si quieres, un postre.", "see KYEH-rehs, oon POHS-treh.", "A dessert, if you like."),
               D("Ben", "Perfecto. Muchas gracias por la invitación.", "per-FEK-toh. MOO-chahs GRAH-syahs por lah een-bee-tah-SYOHN.", "Perfect. Many thanks for the invitation.")],
              WS("Invitation worksheet", [
                  T("Invite and answer.", ["I'm inviting you to dinner", "shall I bring something?", "a dessert"],
                    ["Te invito a cenar.", "¿Traigo algo?", "un postre"]),
                  T("Thank and reply.", ["thanks for everything", "you're welcome"],
                    ["Gracias por todo.", "De nada."]),
              ])),
        ]},
        {"id": "A2+-U3", "title": "El barrio, antes y ahora", "lessons": [
            L("Antes y ahora: imperfecto y presente",
              "The imperfect draws the old landscape: ANTES AQUÍ HABÍA …; the present draws the new "
              "one. HABÍA (there was) is the imperfect of HAY, and it never changes.",
              [V("antes", "AHN-tehs", "before, formerly", "adverb"),
               V("ahora", "ah-OH-rah", "now", "adverb"),
               V("había", "ah-BEE-ah", "there was / were", "verb"),
               V("el barrio", "el BAH-rryoh", "neighbourhood", "noun"),
               V("la tienda", "lah TYEHN-dah", "shop", "noun")],
              G("Before and now",
                "antes había … · ahora hay … · ya no queda …",
                "Antes había tres panaderías; ahora solo queda una. The imperfect sets the scene, "
                "the present reports the change, and «ya no» finishes the old one off.",
                [X("Antes había una panadería en la esquina.", "AHN-tehs ah-BEE-ah OO-nah pah-nah-deh-REE-ah en lah es-KEE-nah.", "There used to be a bakery on the corner."),
                 X("Ahora hay un banco.", "ah-OH-rah eye oon BAHN-koh.", "Now there is a bank."),
                 X("Ya no queda ninguna tienda pequeña.", "yah noh KEH-dah neen-GOO-nah TYEHN-dah peh-KEH-nyah.", "There is no small shop left any more.")],
                [("Antes hubo tres panaderías (habitual).", "Antes había tres panaderías.", "Habitual past takes the imperfect, not the preterite."),
                 ("Habían muchas tiendas.", "Había muchas tiendas.", "había is invariable, even before a plural.")]),
              [D("Ben", "¿Cómo era el barrio antes?", "KOH-moh eh-RAH el BAH-rryoh AHN-tehs?", "What was the neighbourhood like before?"),
               D("Vecina", "Antes había dos panaderías y un mercado pequeño.", "AHN-tehs ah-BEE-ah dohs pah-nah-deh-REE-ahs ee oon mer-KAH-doh peh-KEH-nyoh.", "There used to be two bakeries and a small market."),
               D("Ben", "¿Y ahora?", "ee ah-OH-rah?", "And now?"),
               D("Vecina", "Ahora hay supermercados y ya no queda panadería.", "ah-OH-rah eye soo-per-mer-KAH-dohs ee yah noh KEH-dah pah-nah-deh-REE-ah.", "Now there are supermarkets and no bakery left.")],
              WS("Before-and-now worksheet", [
                  T("Draw the two pictures.", ["there used to be a bakery", "now there is a supermarket", "there is nothing left"],
                    ["Antes había una panadería.", "Ahora hay un supermercado.", "Ya no queda nada."]),
                  T("Describe your street.", ["what was there before?", "what is there now?"],
                    ["Antes había …", "Ahora hay …"]),
              ])),
            L("Preguntar por un piso: alquiler y gastos",
              "Renting asks three things: ¿ESTÁ LIBRE? (is it free), ¿CUÁNTO ES EL ALQUILER? (how "
              "much is the rent), ¿ESTÁN INCLUIDOS LOS GASTOS? (are bills included).",
              [V("el alquiler", "el al-kee-LEHR", "rent", "noun"),
               V("los gastos", "lohs GAHS-tohs", "bills, costs", "noun"),
               V("incluido", "een-kloo-EE-doh", "included", "adjective"),
               V("amueblado", "ah-mweh-BLAH-doh", "furnished", "adjective"),
               V("el contrato", "el kohn-TRAH-toh", "contract", "noun")],
              G("Renting frame",
                "¿está libre? · ¿cuánto es el alquiler? · ¿están incluidos los gastos?",
                "¿Está libre el piso de la calle Mayor? ¿Cuánto es el alquiler? ¿Están incluidos "
                "los gastos? — Sí, pero sin muebles: no está amueblado.",
                [X("¿Está libre el piso?", "es-TAH LEE-breh el PEE-soh?", "Is the flat free?"),
                 X("¿Cuánto es el alquiler?", "KWAHN-toh es el al-kee-LEHR?", "How much is the rent?"),
                 X("¿Están incluidos los gastos?", "es-TAHN een-kloo-EE-dohs lohs GAHS-tohs?", "Are the bills included?")],
                [("¿Cuánto cuesta el alquiler al mes? ✓", "¿Cuánto es el alquiler al mes?", "Both work; «cuánto es» is the fast spoken form."),
                 ("Los gastos están incluidas.", "Los gastos están incluidos.", "gastos is masculine plural.")]),
              [D("Ana", "Hola, llamo por el piso de la calle Mayor.", "OH-lah, YAH-moh por el PEE-soh deh lah KAH-yeh mah-YOR.", "Hello, I'm calling about the flat on Calle Mayor."),
               D("Casero", "Sí, está libre desde julio.", "see, es-TAH LEE-breh des-deh HOO-lyoh.", "Yes, it is free from July."),
               D("Ana", "¿Cuánto es el alquiler y están incluidos los gastos?", "KWAHN-toh es el al-kee-LEHR ee es-TAHN een-kloo-EE-dohs lohs GAHS-tohs?", "How much is the rent and are the bills included?"),
               D("Casero", "Seiscientos, gastos aparte. Está amueblado.", "seys-SYEHN-tohs, GAHS-tohs ah-PAR-teh. es-TAH ah-mweh-BLAH-doh.", "Six hundred, bills separate. It is furnished.")],
              WS("Renting worksheet", [
                  T("Ask about the flat.", ["is it free?", "how much is the rent?", "are the bills included?"],
                    ["¿Está libre?", "¿Cuánto es el alquiler?", "¿Están incluidos los gastos?"]),
                  T("Answer as the landlord.", ["free from July", "six hundred, bills separate, furnished"],
                    ["Está libre desde julio.", "Seiscientos, gastos aparte, amueblado."]),
              ])),
            L("Contar lo que pasó ayer: el pretérito repaso",
              "A story in the preterite is a chain of finished events: AYER FUI … , DESAYUNÉ … , "
              "LUEGO LLAMÉ … , y AL FINAL ME ACORDÉ.",
              [V("ayer", "ah-YEHR", "yesterday", "adverb"),
               V("luego", "LWEH-goh", "then", "adverb"),
               V("al final", "al fee-NAL", "in the end", "phrase"),
               V("acordarse de", "ah-kor-DAR-seh deh", "to remember", "verb"),
               V("olvidarse de", "ol-bee-DAR-seh deh", "to forget", "verb")],
              G("Story chain",
                "ayer fui … · desayuné … · luego llamé … · al final me acordé",
                "Ayer fui al centro, desayuné en el bar de siempre y luego llamé a mi madre. Al "
                "final me acordé de la cita. Chain the verbs and the story moves by itself.",
                [X("Ayer fui al centro y desayuné en un bar.", "ah-YEHR fwee al SEN-troh ee deh-sah-oo-NEH en oon bar.", "Yesterday I went to the centre and had breakfast in a bar."),
                 X("Luego llamé a mi madre.", "LWEH-goh yah-MEH ah mee MAH-dreh.", "Then I called my mother."),
                 X("Al final me acordé de la cita.", "al fee-NAL meh ah-kor-DEH deh lah SEE-tah.", "In the end I remembered the appointment.")],
                [("Ayer iba al centro y desayunaba.", "Ayer fui al centro y desayuné.", "A finished chain takes the preterite; the imperfect would make it a habit."),
                 ("Me olvidé a llamar.", "Me olvidé de llamar.", "olvidarse takes de before the infinitive.")]),
              [D("Ana", "¿Qué hiciste ayer?", "keh ee-SEES-teh ah-YEHR?", "What did you do yesterday?"),
               D("Ben", "Fui al centro, desayuné en un bar y luego llamé a mi madre.", "fwee al SEN-troh, deh-sah-oo-NEH en oon bar ee LWEH-goh yah-MEH ah mee MAH-dreh.", "I went to the centre, had breakfast in a bar and then called my mother."),
               D("Ana", "¿Y por la tarde?", "ee por lah TAR-deh?", "And in the afternoon?"),
               D("Ben", "Al final me acordé de la cita y llegué corriendo.", "al fee-NAL meh ah-kor-DEH deh lah SEE-tah ee yeh-GEH koh-RRYEN-doh.", "In the end I remembered the appointment and arrived running.")],
              WS("Story worksheet", [
                  T("Chain yesterday.", ["I went to the centre", "then I called my mother", "in the end I remembered the appointment"],
                    ["Fui al centro.", "Luego llamé a mi madre.", "Al final me acordé de la cita."]),
                  T("Finish the story.", ["I forgot my keys", "I arrived running"],
                    ["Me olvidé de las llaves.", "Llegué corriendo."]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Spanish daily life runs on small verbal rituals: the return with the receipt, the "
                 "phone that answers «dígame», the apology that blames the traffic rather than "
                 "yourself, and the landlord who quotes the rent and adds «gastos aparte». This "
                 "half-step collects those rituals because they are the language a learner "
                 "actually needs in the second month: a transaction, a call, a complaint, and an "
                 "apology that keeps everyone friends."),
        source_url="https://en.wikipedia.org/wiki/Small_talk",
        reading=("Ayer fui al centro porque quería cambiar una camisa. En la tienda había mucha "
                 "gente: era sábado por la mañana. La dependienta miró el recibo, buscó mi talla y "
                 "me la cambió sin problema. Luego llamé a Ana para quedar, pero no contestó: "
                 "estaba en una reunión. Me dejó un mensaje por la tarde y cenamos juntos."),
        reading_gloss=("Yesterday I went to the centre because I wanted to exchange a shirt. In the "
                       "shop there were a lot of people: it was Saturday morning. The assistant "
                       "looked at the receipt, found my size and exchanged it without a problem. "
                       "Then I called Ana to arrange to meet, but she did not answer: she was in a "
                       "meeting. She left me a message in the afternoon and we had dinner together."),
        listening=("Ana: ¿Dígame?<br>Ben: Hola, soy Ben. ¿Puedo dejarle un recado a Marta?<br>"
                   "Ana: Claro, dime.<br>Ben: Decirle que el piso de la calle Mayor está libre desde julio."),
        listening_gloss=("Ana: Hello? Ben: Hi, it's Ben. Can I leave a message for Marta? Ana: Of "
                         "course, go ahead. Ben: Tell her the flat on Calle Mayor is free from July."),
        voice_tag=VOICE,
        idioms=[
            ("Quedarse con alguien", "to stay with someone", "to keep someone waiting, to have one over on someone"),
            ("Perdona el retraso", "forgive the delay", "sorry I'm late"),
            ("Se me ha hecho tarde", "it has got late on me", "I lost track of time"),
            ("Gastos aparte", "costs apart", "bills not included"),
            ("De parte de", "on the part of", "on behalf of"),
            ("Dar plantón", "to give a bench", "to stand someone up"),
            ("Hacer la compra", "to do the shopping", "to do the grocery shopping"),
            ("Ir a medias", "to go halves", "to split the cost"),
            ("Ponerse de acuerdo", "to put oneself in agreement", "to come to an agreement"),
            ("Sin compromiso", "without commitment", "no strings attached"),
        ],
        mistakes=[
            ("Estoy Ana, de la agencia.", "Soy Ana, de la agencia.", "On the phone you use ser, not estar."),
            ("Antes hubo tres panaderías en el barrio.", "Antes había tres panaderías en el barrio.", "Habitual past takes the imperfect: había."),
            ("Los gastos están incluidas.", "Los gastos están incluidos.", "gastos is masculine plural."),
        ],
        task_title="Run a whole errand in Spanish",
        task_instructions=("Write the six Spanish lines of a real errand you have run this month — "
                           "opening the call, stating the problem, making the request, answering "
                           "the question that comes back, agreeing the time, and saying goodbye. "
                           "Use the phone frame (soy …, ¿de parte de quién?), one complaint frame "
                           "(no funciona, le falta) and one before-and-now pair (antes había … / "
                           "ahora hay …). The aim is one page an assistant in a shop would "
                           "understand on the first hearing."),
    ),
    "test": [
        ("translate_en", "Say: Can you exchange it for a bigger size?", "¿Me lo puede cambiar por una talla más?"),
        ("translate_es", "Perdona el retraso, había un atasco.", "Sorry I'm late, there was a traffic jam."),
        ("multiple_choice", "Which is correct on the phone?", "Soy Ana."),
        ("fill_in_the_blank", "¿Están ___ los gastos?", "incluidos"),
        ("word_selection", "Select the Spanish for receipt.", "el recibo"),
        ("error_correction", "Me queda pequeño la camisa.", "La camisa me queda pequeña."),
        ("dialogue_completion", "Complete: ¿Puedo dejar un ___? — Claro.", "recado"),
        ("matching", "Match «gastos aparte» to its meaning.", "bills not included"),
        ("reading_comprehension", "En la tienda había mucha gente. Why?", "it was Saturday morning"),
        ("inference", "«Se me ha hecho tarde» — who is blamed?", "nobody; the clock"),
        ("main_idea", "Antes había dos panaderías; ahora hay un supermercado. What is described?", "a change in the neighbourhood"),
        ("detail_identification", "¿Cuánto es el alquiler?", "six hundred, bills separate"),
    ],
}

HALFSTEPS["B1+"] = {
    "title": "Spanish B1+ — Work and opinions",
    "native": NATIVE,
    "goals": [
        "Take part in a meeting, take the floor, and write the minutes afterwards",
        "Disagree in a way the other person can accept, and concede what is true",
        "Talk about your job, your experience and a project with deadlines",
    ],
    "units": [
        {"id": "B1+-U1", "title": "Reuniones y correo", "lessons": [
            L("La reunión: el orden del día y los turnos de palabra",
              "Meetings move by formula: EL ORDEN DEL DÍA, TIENES LA PALABRA, VAMOS AL GRANO, "
              "LO DEJAMOS PENDIENTE.",
              [V("el orden del día", "el OR-dehn del DEE-ah", "the agenda", "noun"),
               V("la palabra", "lah pah-LAH-brah", "the floor (to speak)", "noun"),
               V("pendiente", "pen-DYEHN-teh", "pending, outstanding", "adjective"),
               V("el acuerdo", "el ah-KWEHR-doh", "agreement", "noun"),
               V("plantear", "plahn-teh-AR", "to raise, to put forward", "verb")],
              G("Meeting language",
                "tienes la palabra · vamos al grano · lo dejamos pendiente",
                "Antes de empezar, el orden del día. Ana, tienes la palabra. ¿Alguna objeción? "
                "Bien, lo dejamos pendiente para la próxima. The formulas do the work; you only "
                "supply the content.",
                [X("Ana, tienes la palabra.", "AH-nah, TYEH-nehs lah pah-LAH-brah.", "Ana, you have the floor."),
                 X("Vamos al grano.", "BAH-mohs al GRAH-noh.", "Let's get to the point."),
                 X("Lo dejamos pendiente para el martes.", "loh deh-HAH-mohs pen-DYEHN-teh PAH-rah el MAR-tehs.", "We'll leave it pending until Tuesday.")],
                [("Pues yo hablo ahora.", "Tienes la palabra si quieres.", "The floor is given, not taken."),
                 ("Está pendiente de hacer.", "Está pendiente.", "pendiente stands alone in meeting Spanish.")]),
              [D("Jefa", "Empezamos. Ana, tienes la palabra.", "em-peh-SAH-mohs. AH-nah, TYEH-nehs lah pah-LAH-brah.", "Let's start. Ana, you have the floor."),
               D("Ana", "Propongo retrasar el lanzamiento dos semanas.", "proh-POHN-goh reh-trah-SAR el lahn-sah-MYEN-toh dohs seh-MAH-nahs.", "I propose postponing the launch by two weeks."),
               D("Jefa", "¿Alguna objeción?", "ahl-GOO-nah ob-heh-SYOHN?", "Any objection?"),
               D("Ben", "Ninguna de fondo, pero lo dejo pendiente hasta ver el presupuesto.", "neen-GOO-nah deh FON-doh, PEH-roh loh DEH-hoh pen-DYEHN-teh AHS-tah behr el preh-soo-PWEHS-toh.", "No fundamental one, but I'll leave it pending until we see the budget.")],
              WS("Meeting worksheet", [
                  T("Use the formulas.", ["you have the floor", "let's get to the point", "left pending"],
                    ["Tienes la palabra.", "Vamos al grano.", "Queda pendiente."]),
                  T("Raise and park.", ["propose postponing it", "any objection?"],
                    ["Propongo retrasarlo.", "¿Alguna objeción?"]),
              ])),
            L("El correo profesional: asunto, saludo, cierre",
              "Business email has fixed shelves: ASUNTO (subject), ESTIMADO/A …, LE ESCRIBO PARA …, "
              "ADJUNTO …, UN SALUDO CORDIAL.",
              [V("el asunto", "el ah-SOON-toh", "subject line", "noun"),
               V("adjunto", "ahd-HOON-toh", "attached", "adjective"),
               V("cordial", "kor-DYAL", "cordial, kind regards", "adjective"),
               V("agradecer", "ah-grah-deh-SEHR", "to thank", "verb"),
               V("quedar a la espera", "keh-DAR ah lah es-PEH-rah", "to await", "phrase")],
              G("Email frame",
                "asunto: … · le escribo para … · adjunto … · un saludo cordial",
                "Asunto: presupuesto del proyecto. Estimada señora Ruiz: le escribo para pedirle el "
                "presupuesto actualizado. Adjunto el pliego. Quedo a la espera de su respuesta. Un "
                "saludo cordial. Not one sentence is creative — that is the point.",
                [X("Le escribo para pedirle el presupuesto.", "leh es-KREE-boh PAH-rah peh-DEER-leh el preh-soo-PWEHS-toh.", "I am writing to ask you for the budget."),
                 X("Adjunto el pliego actualizado.", "ahd-HOON-toh el PYEH-goh ahk-too-ah-lee-SAH-doh.", "I attach the updated specification."),
                 X("Quedo a la espera de su respuesta.", "KEH-doh ah lah es-PEH-rah deh soo res-PWEHS-tah.", "I await your reply.")],
                [("Hola guapa, te mando esto.", "Estimada señora Ruiz: le escribo para …", "Business email has its own register; the chat register stays in the chat."),
                 ("Adjunto le mando el archivo.", "Adjunto el archivo.", "adjunto already means «I attach».")]),
              [D("Ana", "¿Cómo empiezo el correo a la señora Ruiz?", "KOH-moh em-PYEH-soh el koh-RREH-oh ah lah seh-NYOH-rah RWEES?", "How do I start the email to Mrs Ruiz?"),
               D("Ben", "«Estimada señora Ruiz: le escribo para …».", "es-tee-MAH-dah seh-NYOH-rah RWEES: leh es-KREE-boh PAH-rah …", "'Dear Mrs Ruiz: I am writing to …'."),
               D("Ana", "¿Y para cerrar?", "ee PAH-rah seh-RRAR?", "And to close?"),
               D("Ben", "«Quedo a la espera de su respuesta. Un saludo cordial.»", "KEH-doh ah lah es-PEH-rah deh soo res-PWEHS-tah. oon sah-LOO-doh kor-DYAL.", "'I await your reply. Kind regards.'")],
              WS("Email worksheet", [
                  T("Open the email.", ["you are writing to ask for the budget", "you attach the file"],
                    ["Le escribo para pedirle el presupuesto.", "Adjunto el archivo."]),
                  T("Close the email.", ["awaiting your reply", "kind regards"],
                    ["Quedo a la espera de su respuesta.", "Un saludo cordial."]),
              ])),
            L("Resumir una reunión por escrito: acordamos, se decidió",
              "Minutes speak in the first person plural and the impersonal: ACORDAMOS … , SE DECIDIÓ "
              "… , QUEDA PENDIENTE …",
              [V("acordar", "ah-kor-DAR", "to agree", "verb"),
               V("decidir", "deh-see-DEER", "to decide", "verb"),
               V("el acta", "el AHK-tah", "the minutes", "noun"),
               V("el plazo", "el PLAH-soh", "deadline", "noun"),
               V("asumir", "ah-soo-MEER", "to take on", "verb")],
              G("Minutes frame",
                "acordamos … · se decidió … · queda pendiente … · el plazo es …",
                "Se acordó retrasar el lanzamiento dos semanas. Ana asume la coordinación. El plazo "
                "es el 30 de junio. Queda pendiente el presupuesto. Four sentences, no adjectives.",
                [X("Se acordó retrasar el lanzamiento.", "seh ah-kor-DOH reh-trah-SAR el lahn-sah-MYEN-toh.", "It was agreed to postpone the launch."),
                 X("Ana asume la coordinación.", "AH-nah ah-SOO-meh lah koh-or-dee-nah-SYOHN.", "Ana takes on the coordination."),
                 X("El plazo es el treinta de junio.", "el PLAH-soh es el TREYN-tah deh HOO-nyoh.", "The deadline is 30 June.")],
                [("Acordamos que sí, todo bien.", "Se acordó retrasar el lanzamiento dos semanas.", "Minutes state decisions, not moods."),
                 ("Yo asumo que Ana hace la coordinación.", "Ana asume la coordinación.", "Name the owner of the task directly.")]),
              [D("Ben", "¿Cómo resumo la reunión?", "KOH-moh reh-SOO-moh lah reh-YOHN?", "How do I summarise the meeting?"),
               D("Ana", "Con verbos, no con adjetivos: se acordó, se decidió, queda pendiente.", "kohn BEHR-bohs, noh kohn ahd-heh-TEE-bohs: seh ah-kor-DOH, seh deh-see-DYOH, KEH-dah pen-DYEHN-teh.", "With verbs, not adjectives: it was agreed, it was decided, it remains pending."),
               D("Ben", "«Se acordó retrasar el lanzamiento. El plazo es el treinta de junio.»", "seh ah-kor-DOH reh-trah-SAR el lahn-sah-MYEN-toh. el PLAH-soh es el TREYN-tah deh HOO-nyoh.", "'It was agreed to postpone the launch. The deadline is 30 June.'"),
               D("Ana", "Eso es. Y «queda pendiente el presupuesto».", "EH-soh es. ee KEH-dah pen-DYEHN-teh el preh-soo-PWEHS-toh.", "That's it. And 'the budget remains pending'.")],
              WS("Minutes worksheet", [
                  T("Write the decisions.", ["it was agreed to postpone the launch", "Ana takes on the coordination", "the deadline is 30 June"],
                    ["Se acordó retrasar el lanzamiento.", "Ana asume la coordinación.", "El plazo es el 30 de junio."]),
                  T("Note what is open.", ["the budget remains pending", "we'll decide on Tuesday"],
                    ["Queda pendiente el presupuesto.", "Se decide el martes."]),
              ])),
        ]},
        {"id": "B1+-U2", "title": "Opiniones que se pueden escuchar", "lessons": [
            L("Estoy de acuerdo, pero…",
              "A disagreement that lands starts with the part that is true: ENTIENDO TU POSTURA, Y "
              "HASTA CIERTO PUNTO ESTOY DE ACUERDO; AHORA BIEN, …",
              [V("la postura", "lah pohs-TOO-rah", "position, stance", "noun"),
               V("hasta cierto punto", "AHS-tah SYEHR-toh POON-toh", "up to a point", "phrase"),
               V("ahora bien", "ah-OH-rah byehn", "however", "phrase"),
               V("matizar", "mah-tee-SAR", "to qualify, to nuance", "verb"),
               V("el matiz", "el mah-TEES", "nuance", "noun")],
              G("Concede, then qualify",
                "entiendo tu postura · hasta cierto punto · ahora bien · el matiz es …",
                "Entiendo tu postura y hasta cierto punto estoy de acuerdo. Ahora bien, el coste "
                "cambia el matiz. Spanish argument prefers a concession before a contradiction.",
                [X("Entiendo tu postura.", "en-TYEHN-doh too pohs-TOO-rah.", "I understand your position."),
                 X("Hasta cierto punto estoy de acuerdo.", "AHS-tah SYEHR-toh POON-toh es-TOY deh ah-KWEHR-doh.", "Up to a point I agree."),
                 X("Ahora bien, el coste cambia el matiz.", "ah-OH-rah byehn, el KOHS-teh KAHM-byah el mah-TEES.", "However, the cost changes the nuance.")],
                [("Estás equivocado, y punto.", "Entiendo tu postura, pero hay un matiz.", "A concession keeps the argument alive."),
                 ("Estoy de acuerdo en todo, aunque no.", "Hasta cierto punto estoy de acuerdo.", "One position per sentence.")]),
              [D("Ana", "Creo que deberíamos lanzarlo ya.", "KREH-oh keh deh-beh-REE-ah-mohs lahn-SAR-loh yah.", "I think we should launch it now."),
               D("Ben", "Entiendo tu postura y hasta cierto punto estoy de acuerdo.", "en-TYEHN-doh too pohs-TOO-rah ee AHS-tah SYEHR-toh POON-toh es-TOY deh ah-KWEHR-doh.", "I understand your position and up to a point I agree."),
               D("Ana", "¿Pero?", "PEH-roh?", "But?"),
               D("Ben", "Ahora bien, el presupuesto no está aprobado. Ese es el matiz.", "ah-OH-rah byehn, el preh-soo-PWEHS-toh noh es-TAH ah-proh-BAH-doh. EH-seh es el mah-TEES.", "However, the budget is not approved. That's the nuance.")],
              WS("Agreement worksheet", [
                  T("Concede, then qualify.", ["I understand your position", "up to a point I agree", "however, there is a nuance"],
                    ["Entiendo tu postura.", "Hasta cierto punto estoy de acuerdo.", "Ahora bien, hay un matiz."]),
                  T("Name the real obstacle.", ["the budget is not approved", "we need more data"],
                    ["El presupuesto no está aprobado.", "Necesitamos más datos."]),
              ])),
            L("Convencer: si hacemos esto, pasa aquello",
              "Persuasion uses a real condition plus a consequence: SI SUBIMOS EL PRECIO, PERDEMOS "
              "CLIENTES. And a recommendation: SERÍA MEJOR QUE ESPERÁRAMOS.",
              [V("convencer", "kohn-behn-SEHR", "to convince", "verb"),
               V("a corto plazo", "ah KOR-toh PLAH-soh", "in the short term", "phrase"),
               V("perder", "per-DEHR", "to lose", "verb"),
               V("el riesgo", "el RYEH-sgoh", "risk", "noun"),
               V("sería mejor que", "seh-REE-ah meh-HOR keh", "it would be better if", "phrase")],
              G("Real condition and recommendation",
                "si + presente, + presente/futuro · sería mejor que + subjuntivo",
                "Si subimos el precio ahora, perdemos clientes. Sería mejor que esperáramos al "
                "otoño. The condition states the mechanism, the recommendation offers the way out.",
                [X("Si subimos el precio, perdemos clientes.", "see soo-BEE-mohs el PREH-syoh, per-DEH-mohs KLYEHN-tehs.", "If we raise the price, we lose customers."),
                 X("Sería mejor que esperáramos al otoño.", "seh-REE-ah meh-HOR keh es-peh-RAH-rah-mohs al oh-TOH-nyoh.", "It would be better to wait until autumn."),
                 X("El riesgo es real a corto plazo.", "el RYEH-sgoh es reh-AL ah KOR-toh PLAH-soh.", "The risk is real in the short term.")],
                [("Si subiéramos el precio, perdemos clientes.", "Si subimos el precio, perdemos clientes.", "A real condition takes the present indicative, not the imperfect subjunctive."),
                 ("Sería mejor esperar que esperáramos.", "Sería mejor que esperáramos.", "sería mejor que takes the subjunctive.")]),
              [D("Ben", "Si subimos el precio ahora, perdemos clientes.", "see soo-BEE-mohs el PREH-syoh ah-OH-rah, per-DEH-mohs KLYEHN-tehs.", "If we raise the price now, we lose customers."),
               D("Ana", "¿Y qué propones?", "ee keh proh-poh-NEHS?", "And what do you propose?"),
               D("Ben", "Sería mejor que esperáramos al otoño.", "seh-REE-ah meh-HOR keh es-peh-RAH-rah-mohs al oh-TOH-nyoh.", "It would be better for us to wait until autumn."),
               D("Ana", "Vale, pero pongamos una fecha límite.", "BAH-leh, PEH-roh pohn-GAH-mohs OO-nah FEH-chah LEE-mee-teh.", "OK, but let's set a deadline.")],
              WS("Persuasion worksheet", [
                  T("State the mechanism.", ["if we raise the price, we lose customers", "if we wait, we lose the season"],
                    ["Si subimos el precio, perdemos clientes.", "Si esperamos, perdemos la temporada."]),
                  T("Recommend.", ["it would be better to wait until autumn", "the risk is real in the short term"],
                    ["Sería mejor que esperáramos al otoño.", "El riesgo es real a corto plazo."]),
              ])),
            L("Desacuerdo sin pelea: entiendo, pero no puedo aceptarlo",
              "The soft refusal names the disagreement and the shared goal in one breath: NO PUEDO "
              "ACEPTARLO ASÍ, AUNQUE COMPARTO EL OBJETIVO.",
              [V("aceptar", "ah-sep-TAR", "to accept", "verb"),
               V("compartir", "kohm-par-TEER", "to share", "verb"),
               V("el objetivo", "el ob-heh-TEE-boh", "objective", "noun"),
               V("la postura", "lah pohs-TOO-rah", "stance", "noun"),
               V("replantear", "reh-plahn-teh-AR", "to rethink", "verb")],
              G("Soft refusal",
                "no puedo aceptarlo así · comparto el objetivo · ¿lo replanteamos?",
                "No puedo aceptarlo así, aunque comparto el objetivo. ¿Lo replanteamos con los "
                "datos delante? The refusal is about the proposal; the shared goal keeps the "
                "relationship intact.",
                [X("No puedo aceptarlo así.", "noh PWEH-doh ah-sep-TAR-loh ah-SEE.", "I can't accept it like that."),
                 X("Comparto el objetivo, no el método.", "kohm-PAR-toh el ob-heh-TEE-boh, noh el MEH-toh-doh.", "I share the objective, not the method."),
                 X("¿Lo replanteamos con los datos delante?", "loh reh-plahn-teh-AH-mohs kohn lohs DAH-tohs deh-LAHN-teh?", "Shall we rethink it with the data in front of us?")],
                [("No, eso es una tontería.", "No puedo aceptarlo así; replanteémoslo.", "Attack the proposal, never the person."),
                 ("Comparto el objetivo y el método siempre.", "Comparto el objetivo, no el método.", "Precision is the politeness.")]),
              [D("Ana", "Firmemos el contrato esta semana.", "feer-MEH-mohs el kohn-TRAH-toh EHS-tah seh-MAH-nah.", "Let's sign the contract this week."),
               D("Ben", "No puedo aceptarlo así, aunque comparto el objetivo.", "noh PWEH-doh ah-sep-TAR-loh ah-SEE, awn-KEH kohm-PAR-toh el ob-heh-TEE-boh.", "I can't accept it like that, although I share the objective."),
               D("Ana", "¿Qué te falta?", "keh teh FAHL-tah?", "What do you need?"),
               D("Ben", "Los datos del trimestre. ¿Lo replanteamos el lunes?", "lohs DAH-tohs del tree-MEHS-treh. loh reh-plahn-teh-AH-mohs el LOO-nehs?", "The quarter's figures. Shall we rethink it on Monday?")],
              WS("Disagreement worksheet", [
                  T("Refuse the proposal, keep the goal.", ["I can't accept it like that", "I share the objective, not the method"],
                    ["No puedo aceptarlo así.", "Comparto el objetivo, no el método."]),
                  T("Offer the next step.", ["shall we rethink it with the data?", "what the other side needs"],
                    ["¿Lo replanteamos con los datos?", "¿Qué te falta?"]),
              ])),
        ]},
        {"id": "B1+-U3", "title": "Trabajo, experiencia y proyectos", "lessons": [
            L("La oferta y el currículum: requisitos y experiencia",
              "Job adverts are a list of requirements: SE VALORA (is valued), IMPRESCINDIBLE "
              "(essential), EXPERIENCIA DEMOSTRABLE, INCORPORACIÓN INMEDIATA.",
              [V("el requisito", "el reh-kee-SEE-toh", "requirement", "noun"),
               V("imprescindible", "eem-pres-seen-DEE-bleh", "essential", "adjective"),
               V("la experiencia", "lah eks-peh-RYEN-syah", "experience", "noun"),
               V("valorar", "bah-loh-RAR", "to value, to assess", "verb"),
               V("la incorporación", "lah een-kor-poh-rah-SYOHN", "start date, joining", "noun")],
              G("Requirements frame",
                "se valora … · imprescindible … · experiencia demostrable · incorporación …",
                "Se valora el inglés; imprescindible experiencia demostrable en atención al "
                "cliente; incorporación inmediata. The advert's grammar is impersonal and blunt — "
                "the answer should be too.",
                [X("Se valora el inglés.", "seh bah-LOH-rah el een-GLEHS.", "English is valued."),
                 X("Imprescindible experiencia demostrable.", "eem-pres-seen-DEE-bleh eks-peh-RYEN-syah deh-mohs-TRAH-bleh.", "Demonstrable experience essential."),
                 X("Incorporación inmediata.", "een-kor-poh-rah-SYOHN een-meh-DYAH-tah.", "Immediate start.")],
                [("Es imprescindible que inglés.", "Es imprescindible el inglés.", "The advert style is a noun phrase, not a que-clause."),
                 ("Se valoran trabajar en equipo.", "Se valora trabajar en equipo.", "se valora + infinitive is singular.")]),
              [D("Ana", "¿Qué piden exactamente?", "keh PEE-dehn ek-sahk-tah-MEN-teh?", "What exactly are they asking for?"),
               D("Ben", "Se valora el inglés y es imprescindible experiencia demostrable.", "seh bah-LOH-rah el een-GLEHS ee es eem-pres-seen-DEE-bleh eks-peh-RYEN-syah deh-mohs-TRAH-bleh.", "English is valued and demonstrable experience is essential."),
               D("Ana", "Yo llevo cinco años en atención al cliente.", "yoh YEH-boh SEEN-koh AH-nyohs en ah-ten-SYOHN al KLYEHN-teh.", "I have five years in customer service."),
               D("Ben", "Pues ponlo en la primera línea: eso es lo que buscan.", "pwehs POHN-loh en lah pree-MEH-rah LEE-neh-ah: EH-soh es loh keh BOOS-kahn.", "Then put it in the first line: that's what they are looking for.")],
              WS("Job-advert worksheet", [
                  T("Read the advert.", ["English is valued", "experience essential", "immediate start"],
                    ["Se valora el inglés.", "Imprescindible experiencia.", "Incorporación inmediata."]),
                  T("Answer with your record.", ["I have five years in customer service", "I can start in July"],
                    ["Llevo cinco años en atención al cliente.", "Puedo incorporarme en julio."]),
              ])),
            L("La entrevista: llevo tres años + gerundio",
              "Experience is spoken with LLEVO + time + GERUND: LLEVO TRES AÑOS TRABAJANDO EN "
              "LOGÍSTICA. Then the strength: MI PUNTO FUERTE ES …",
              [V("llevar + tiempo", "yeh-BAR TYEHM-poh", "to have been (for a time)", "verb"),
               V("trabajando", "trah-bah-HAHN-doh", "working (gerund)", "verb"),
               V("el punto fuerte", "el POON-toh FWEHR-teh", "strength", "noun"),
               V("el reto", "el REH-toh", "challenge", "noun"),
               V("encargarse de", "en-kar-GAR-seh deh", "to be in charge of", "verb")],
              G("Experience frame",
                "llevo + tiempo + gerundio · mi punto fuerte es … · mi reto fue …",
                "Llevo tres años trabajando en logística y me encargo de las rutas. Mi punto fuerte "
                "es el detalle; mi reto fue aprender a delegar. Spanish interview answers are "
                "concrete, because the frame forces the gerund.",
                [X("Llevo tres años trabajando en logística.", "YEH-boh trehs AH-nyohs trah-bah-HAHN-doh en loh-HEES-tee-kah.", "I have been working in logistics for three years."),
                 X("Mi punto fuerte es la atención al detalle.", "mee POON-toh FWEHR-teh es lah ah-ten-SYOHN al deh-TAH-yeh.", "My strength is attention to detail."),
                 X("Mi reto fue aprender a delegar.", "mee REH-toh fweh ah-pren-DEHR ah deh-leh-GAR.", "My challenge was learning to delegate.")],
                [("Trabajo aquí desde tres años.", "Llevo tres años trabajando aquí.", "Duration up to now takes llevar + time, not desde."),
                 ("Mi punto fuerte soy el detalle.", "Mi punto fuerte es el detalle.", "The strength is the thing, not you.")]),
              [D("Entrevistadora", "¿Cuál es su experiencia?", "KWAHL es soo eks-peh-RYEN-syah?", "What is your experience?"),
               D("Ana", "Llevo tres años trabajando en logística y me encargo de las rutas.", "YEH-boh trehs AH-nyohs trah-bah-HAHN-doh en loh-HEES-tee-kah ee meh en-KAR-goh deh lahs ROO-tahs.", "I have been working in logistics for three years and I am in charge of the routes."),
               D("Entrevistadora", "¿Y su punto fuerte?", "ee soo POON-toh FWEHR-teh?", "And your strength?"),
               D("Ana", "El detalle. Mi reto fue aprender a delegar.", "el deh-TAH-yeh. mee REH-toh fweh ah-pren-DEHR ah deh-leh-GAR.", "Detail. My challenge was learning to delegate.")],
              WS("Interview worksheet", [
                  T("State your experience.", ["three years in logistics", "in charge of the routes"],
                    ["Llevo tres años trabajando en logística.", "Me encargo de las rutas."]),
                  T("Name strength and challenge.", ["attention to detail", "learning to delegate"],
                    ["Mi punto fuerte es el detalle.", "Mi reto fue aprender a delegar."]),
              ])),
            L("Hablar de un proyecto: objetivos y plazos",
              "Projects are described as a goal plus a deadline plus a risk: EL OBJETIVO ES … , LA "
              "FECHA LÍMITE ES … , EL RIESGO ES …",
              [V("el objetivo", "el ob-heh-TEE-boh", "goal", "noun"),
               V("la fecha límite", "lah FEH-chah LEE-mee-teh", "deadline", "noun"),
               V("el hito", "el EE-toh", "milestone", "noun"),
               V("asumir", "ah-soo-MEER", "to take on", "verb"),
               V("el riesgo", "el RYEH-sgoh", "risk", "noun")],
              G("Project frame",
                "el objetivo es … · la fecha límite es … · el riesgo es …",
                "El objetivo es digitalizar los pedidos; la fecha límite, el 30 de noviembre; el "
                "riesgo, la integración con el sistema antiguo. Goal, date, risk — in that order.",
                [X("El objetivo es digitalizar los pedidos.", "el ob-heh-TEE-boh es dee-hee-tah-lee-SAR lohs peh-DEE-dohs.", "The goal is to digitalise orders."),
                 X("La fecha límite es el treinta de noviembre.", "lah FEH-chah LEE-mee-teh es el TREYN-tah deh noh-BYEHN-breh.", "The deadline is 30 November."),
                 X("El riesgo es la integración con el sistema antiguo.", "el RYEH-sgoh es lah een-teh-grah-SYOHN kohn el sees-TEH-mah ahn-TEE-gwoh.", "The risk is the integration with the old system.")],
                [("El objetivo es que digitalizamos.", "El objetivo es digitalizar los pedidos.", "A goal takes the infinitive, not a conjugated verb."),
                 ("La fecha límite hay el 30.", "La fecha límite es el 30.", "Dates take ser.")]),
              [D("Ben", "¿Cuál es el objetivo del proyecto?", "KWAHL es el ob-heh-TEE-boh del proh-YEK-toh?", "What is the project goal?"),
               D("Ana", "Digitalizar los pedidos antes de noviembre.", "dee-hee-tah-lee-SAR lohs peh-DEE-dohs AHN-tehs deh noh-BYEHN-breh.", "To digitalise orders before November."),
               D("Ben", "¿Y el mayor riesgo?", "ee el mah-YOR RYEH-sgoh?", "And the biggest risk?"),
               D("Ana", "La integración con el sistema antiguo. Por eso el primer hito es una prueba.", "lah een-teh-grah-SYOHN kohn el sees-TEH-mah ahn-TEE-gwoh. por EH-soh el pree-MEHR EE-toh es OO-nah PRWEH-bah.", "The integration with the old system. That is why the first milestone is a test.")],
              WS("Project worksheet", [
                  T("Describe the project.", ["the goal is to digitalise the orders", "the deadline is 30 November", "the biggest risk"],
                    ["El objetivo es digitalizar los pedidos.", "La fecha límite es el 30 de noviembre.", "El mayor riesgo es …"]),
                  T("Name the milestone.", ["the first milestone is a test", "we take on the integration"],
                    ["El primer hito es una prueba.", "Asumimos la integración."]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Spanish working life leans on fixed verbal machinery — «tienes la palabra», «vamos "
                 "al grano», «queda pendiente», «un saludo cordial» — and a learner who owns the "
                 "machinery sounds senior long before the grammar is perfect. This half-step "
                 "drills the machinery of meetings, email, negotiation and the interview, because "
                 "in Spanish offices the formulas are not empty: they are how a disagreement stays "
                 "professional."),
        source_url="https://en.wikipedia.org/wiki/Formality",
        reading=("En la reunión del martes se acordó retrasar el lanzamiento dos semanas. Ana "
                 "planteó el riesgo del presupuesto y el equipo decidió esperar al otoño. Quedó "
                 "pendiente la fecha del primer hito. Después, Ana escribió el acta en veinte "
                 "minutos: acordamos, se decidió, queda pendiente — con verbos, sin adjetivos."),
        reading_gloss=("At Tuesday's meeting it was agreed to postpone the launch by two weeks. Ana "
                       "raised the budget risk and the team decided to wait until autumn. The date "
                       "of the first milestone was left pending. Afterwards Ana wrote the minutes "
                       "in twenty minutes: we agreed, it was decided, it remains pending — with "
                       "verbs, no adjectives."),
        listening=("Ben: Entiendo tu postura, pero no puedo aceptarlo así.<br>Ana: ¿Qué te falta?<br>"
                   "Ben: Los datos del trimestre. ¿Lo replanteamos el lunes?<br>Ana: Vale, pero pongamos una fecha límite."),
        listening_gloss=("Ben: I understand your position, but I can't accept it like that. Ana: What "
                         "do you need? Ben: The quarter's figures. Shall we rethink it on Monday? "
                         "Ana: OK, but let's set a deadline."),
        voice_tag=VOICE,
        idioms=[
            ("Vamos al grano", "let's go to the grain", "let's get to the point"),
            ("Tienes la palabra", "you have the word", "the floor is yours"),
            ("Queda pendiente", "it remains pending", "still outstanding"),
            ("Estar de acuerdo", "to be in agreement", "to agree"),
            ("Ponerse las pilas", "to put one's batteries in", "to get a move on"),
            ("Llevar el peso", "to carry the weight", "to carry the load"),
            ("Tirar del carro", "to pull the cart", "to drive things forward"),
            ("Un saludo cordial", "a cordial greeting", "kind regards"),
            ("A la mayor brevedad", "at the greatest brevity", "as soon as possible"),
            ("Manos a la obra", "hands to the work", "let's get to work"),
        ],
        mistakes=[
            ("Trabajo en esto desde tres años.", "Llevo tres años trabajando en esto.", "Duration up to now takes llevar, not desde."),
            ("Si subiéramos el precio, perdemos clientes.", "Si subimos el precio, perdemos clientes.", "A real condition takes the present indicative."),
            ("El objetivo es que digitalizamos.", "El objetivo es digitalizar los pedidos.", "Goals take the infinitive."),
        ],
        task_title="Hold a five-line negotiation in Spanish",
        task_instructions=("Write the five moves of a disagreement you might actually have at work: "
                           "open with the part you accept, give the qualification (hasta cierto "
                           "punto … ahora bien), state the real obstacle with a verb, make a "
                           "recommendation with sería mejor que + subjunctive, and close by fixing "
                           "the next step and its date. Then rewrite the same five lines as the "
                           "minutes of the meeting — acordamos, se decidió, queda pendiente."),
    ),
    "test": [
        ("translate_en", "Say: You have the floor.", "Tienes la palabra."),
        ("translate_es", "Entiendo tu postura, pero hay un matiz.", "I understand your position, but there is a nuance."),
        ("multiple_choice", "Which closes a business email?", "Un saludo cordial."),
        ("fill_in_the_blank", "Sería mejor que ___ al otoño.", "esperáramos"),
        ("word_selection", "Select the Spanish for the minutes.", "el acta"),
        ("error_correction", "Si subiéramos el precio, perdemos clientes.", "Si subimos el precio, perdemos clientes."),
        ("dialogue_completion", "Complete: ¿Alguna ___? — Ninguna de fondo.", "objeción"),
        ("matching", "Match «quedar pendiente» to its meaning.", "still outstanding"),
        ("reading_comprehension", "What did the team decide about the launch?", "to postpone it two weeks"),
        ("inference", "«Comparto el objetivo, no el método» — what is the speaker refusing?", "the proposal, not the person"),
        ("main_idea", "El objetivo es digitalizar los pedidos. What is stated?", "the project goal"),
        ("detail_identification", "What is the deadline?", "30 November"),
    ],
}

HALFSTEPS["B2+"] = {
    "title": "Spanish B2+ — Argument and formal register",
    "native": NATIVE,
    "goals": [
        "Argue with figures: proportions, rises and falls, and the frame that reads them",
        "Write a formal letter and a formal complaint: facts, grounds, request",
        "Cite, reformulate and close a text without repeating yourself",
    ],
    "units": [
        {"id": "B2+-U1", "title": "Argumentar con cifras", "lessons": [
            L("Cifras y tendencias: un tercio, el doble, en torno a",
              "Statistics are spoken with proportions and verbs of change: UN TERCIO DE (a third "
              "of), EL DOBLE DE (twice as many), EN TORNO A (around), CRECIÓ UN 4 %.",
              [V("un tercio", "oon TEHR-syoh", "a third", "numeral"),
               V("el doble de", "el DOH-bleh deh", "twice as much as", "phrase"),
               V("en torno a", "en TOR-noh ah", "around, roughly", "phrase"),
               V("crecer", "kreh-SEHR", "to grow", "verb"),
               V("descender", "des-sen-DEHR", "to fall", "verb")],
              G("Figures frame",
                "un tercio de … · el doble de … · en torno a … · creció un 4 %",
                "Un tercio de los hogares tiene un perro. El gasto creció un cuatro por ciento y "
                "el consumo descendió ligeramente. The figure carries the sentence; the verb says "
                "the direction.",
                [X("Un tercio de los hogares tiene un perro.", "oon TEHR-syoh deh lohs oh-GAH-rehs TYEH-neh oon PEH-rroh.", "A third of households have a dog."),
                 X("El gasto creció un cuatro por ciento.", "el GAHS-toh kreh-SYOH oon KWAH-troh por syen-TOH.", "Spending grew by four per cent."),
                 X("El consumo descendió ligeramente.", "el kohn-SOO-moh des-sen-DYOH lee-heh-rah-MEN-teh.", "Consumption fell slightly.")],
                [("Creció el cuatro por ciento.", "Creció un cuatro por ciento.", "A change names an amount with un."),
                 ("El doble que de hogares.", "El doble de hogares.", "The proportion takes de twice: el doble de.")]),
              [D("Ana", "¿Cuánta gente usa el bus?", "KWAHN-tah HEN-teh OO-sah el boos?", "How many people use the bus?"),
               D("Analista", "En torno a un tercio de la ciudad.", "en TOR-noh ah oon TEHR-syoh deh lah syoo-DAD.", "Around a third of the city."),
               D("Ana", "¿Y ha cambiado?", "ee ah kahm-BYAH-doh?", "And has it changed?"),
               D("Analista", "El uso creció un cuatro por ciento; el coche descendió ligeramente.", "el OO-soh kreh-SYOH oon KWAH-troh por syen-TOH; el KOH-choh des-sen-DYOH lee-heh-rah-MEN-teh.", "Use grew by four per cent; car use fell slightly.")],
              WS("Figures worksheet", [
                  T("Say it with figures.", ["a third of households", "twice as many", "around thirty people"],
                    ["un tercio de los hogares", "el doble de", "en torno a treinta personas"]),
                  T("Report the change.", ["spending grew by 4%", "consumption fell slightly"],
                    ["El gasto creció un 4 %.", "El consumo descendió ligeramente."]),
              ])),
            L("Encadenar argumentos: no solo …, sino que además",
              "Good Spanish argument stacks evidence with NO SOLO … SINO QUE ADEMÁS (not only … but "
              "also) and tops it with POR SI FUERA POCO (as if that were not enough).",
              [V("no solo … sino que además", "noh SOH-loh … SEE-noh keh ah-deh-MAHS", "not only … but also", "phrase"),
               V("por si fuera poco", "por see FWEH-rah POH-koh", "as if that were not enough", "phrase"),
               V("añadir", "ah-nyah-DEER", "to add", "verb"),
               V("es más", "es MAHS", "what is more", "phrase"),
               V("en la misma línea", "en lah MEES-mah LEE-neh-ah", "along the same lines", "phrase")],
              G("Stacking evidence",
                "no solo … , sino que además … · por si fuera poco · es más",
                "No solo subió el precio, sino que además bajó la calidad. Es más, el plazo se "
                "duplicó. Por si fuera poco, nadie avisó. Three escalations, one argument.",
                [X("No solo subió el precio, sino que además bajó la calidad.", "noh SOH-loh soo-BYOH el PREH-syoh, SEE-noh keh ah-deh-MAHS bah-HOH lah kah-lee-DAD.", "Not only did the price rise, but the quality also fell."),
                 X("Es más, el plazo se duplicó.", "es MAHS, el PLAH-soh seh doo-plee-KOH.", "What is more, the deadline doubled."),
                 X("Por si fuera poco, nadie avisó.", "por see FWEH-rah POH-koh, NAH-dee ah-bee-SOH.", "As if that were not enough, nobody informed us.")],
                [("No solo subió el precio, sino bajó también.", "No solo subió el precio, sino que además bajó la calidad.", "The second clause needs sino que + además."),
                 ("Por si es poco.", "Por si fuera poco.", "The phrase is fixed: por si fuera poco.")]),
              [D("Ben", "¿Cómo lo digo sin sonar exagerado?", "KOH-moh loh DEE-goh seen soh-NAR eks-ah-heh-RAH-doh?", "How do I say it without sounding exaggerated?"),
               D("Ana", "Encadena: no solo … , sino que además …", "en-kah-DEH-nah: noh SOH-loh …, SEE-noh keh ah-deh-MAHS …", "Chain it: not only …, but also …"),
               D("Ben", "«No solo subió el precio, sino que además bajó la calidad.»", "noh SOH-loh soo-BYOH el PREH-syoh, SEE-noh keh ah-deh-MAHS bah-HOH lah kah-lee-DAD.", "'Not only did the price rise, but the quality also fell.'"),
               D("Ana", "Y si quieres rematar: «por si fuera poco, nadie avisó».", "ee see KYEH-rehs reh-mah-TAR: por see FWEH-rah POH-koh, NAH-dee ah-bee-SOH.", "And if you want to finish it: 'as if that were not enough, nobody informed us'.")],
              WS("Argument-chain worksheet", [
                  T("Stack the evidence.", ["not only did the price rise, but the quality also fell", "what is more, the deadline doubled", "as if that were not enough, nobody informed us"],
                    ["No solo subió el precio, sino que además bajó la calidad.", "Es más, el plazo se duplicó.", "Por si fuera poco, nadie avisó."]),
                  T("Add along the same lines.", ["along the same lines", "I would add one more fact"],
                    ["En la misma línea, …", "Añadiría un dato más."]),
              ])),
            L("Conceder para ganar: si bien …, no es menos cierto que …",
              "The C1-level concession is a two-storey sentence: SI BIEN … (although), NO ES MENOS "
              "CIERTO QUE … (it is no less true that). It concedes the fact and keeps the "
              "conclusion.",
              [V("si bien", "see byehn", "although, while", "conjunction"),
               V("no es menos cierto que", "noh es MEH-nohs SYEHR-toh keh", "it is no less true that", "phrase"),
               V("cierto", "SYEHR-toh", "true", "adjective"),
               V("sin embargo", "seen ehm-BAR-goh", "however", "adverb"),
               V("en cambio", "en KAHM-byoh", "by contrast", "phrase")],
              G("Two-storey concession",
                "si bien … , no es menos cierto que … · sin embargo · en cambio",
                "Si bien la medida redujo el gasto, no es menos cierto que aumentó el riesgo. The "
                "first clause pays; the second collects.",
                [X("Si bien la medida redujo el gasto, no es menos cierto que aumentó el riesgo.", "see byehn lah meh-DEE-dah reh-doo-HOH el GAHS-toh, noh es MEH-nohs SYEHR-toh keh ow-men-TOH el RYEH-sgoh.", "Although the measure reduced spending, it is no less true that it increased the risk."),
                 X("Los datos mejoran; sin embargo, la tendencia es frágil.", "lohs DAH-tohs meh-HOH-rahn; seen ehm-BAR-goh, lah tehn-DEN-syah es FRAH-heel.", "The data improves; however, the trend is fragile."),
                 X("En cambio, el empleo no se recuperó.", "en KAHM-byoh, el ehm-PLEH-oh noh seh reh-koo-peh-ROH.", "By contrast, employment did not recover.")],
                [("Si bien la medida redujo el gasto, pero subió el riesgo.", "Si bien la medida redujo el gasto, no es menos cierto que subió el riesgo.", "si bien already carries the contrast; pero doubles it."),
                 ("No es menos cierto que subió el riesgo, y claro.", "No es menos cierto que subió el riesgo.", "The frame ends the sentence; it does not invite agreement.")]),
              [D("Jefa", "¿Recomienda usted la medida?", "reh-koh-MYEHN-dah oos-TEHD lah meh-DEE-dah?", "Do you recommend the measure?"),
               D("Analista", "Si bien redujo el gasto, no es menos cierto que aumentó el riesgo.", "see byehn reh-doo-HOH el GAHS-toh, noh es MEH-nohs SYEHR-toh keh ow-men-TOH el RYEH-sgoh.", "While it reduced spending, it is no less true that it increased the risk."),
               D("Jefa", "¿Y eso qué significa en la práctica?", "ee EH-soh keh seen-GEE-fee-kah en lah PRAHK-tee-kah?", "And what does that mean in practice?"),
               D("Analista", "Significa que la recomiendo con condiciones, no tal cual.", "seen-GEE-fee-kah keh lah reh-koh-MYEHN-doh kohn kohn-dee-SYOH-nehs, noh tal KWAHL.", "It means I recommend it with conditions, not as it stands.")],
              WS("Concession worksheet", [
                  T("Build the two-storey sentence.", ["although it reduced spending, the risk increased", "the data improves, however the trend is fragile"],
                    ["Si bien redujo el gasto, no es menos cierto que aumentó el riesgo.", "Los datos mejoran; sin embargo, la tendencia es frágil."]),
                  T("Qualify the recommendation.", ["with conditions, not as it stands", "by contrast, employment did not recover"],
                    ["La recomiendo con condiciones.", "En cambio, el empleo no se recuperó."]),
              ])),
        ]},
        {"id": "B2+-U2", "title": "Cartas y reclamaciones formales", "lessons": [
            L("La carta formal: expongo, solicito, le agradecería",
              "Administrative Spanish runs on verbs in the first person: EXPONGO (I set out), "
              "SOLICITO (I request), LE AGRADECERÍA (I would be grateful).",
              [V("exponer", "eks-poh-NEHR", "to set out, to state", "verb"),
               V("solicitar", "soh-lee-see-TAR", "to request", "verb"),
               V("agradecería", "ah-grah-deh-seh-REE-ah", "I would be grateful", "verb"),
               V("el escrito", "el es-KREE-toh", "formal letter, document", "noun"),
               V("la instancia", "lah eens-TAHN-syah", "formal application", "noun")],
              G("Formal letter verbs",
                "expongo … · solicito … · le agradecería que …",
                "Expongo los hechos y solicito una revisión. Le agradecería que me confirmara la "
                "fecha. The letter names its own acts — expongo, solicito — and then asks.",
                [X("Expongo los hechos a continuación.", "eks-POHN-goh lohs EH-chohs ah kohn-tee-noo-ah-SYOHN.", "I set out the facts below."),
                 X("Solicito una revisión del expediente.", "soh-LEE-see-toh OO-nah reh-bee-SYOHN del eks-peh-DYEN-teh.", "I request a review of the file."),
                 X("Le agradecería que me confirmara la fecha.", "leh ah-grah-deh-seh-REE-ah keh meh kohn-feer-MAH-rah lah FEH-chah.", "I would be grateful if you would confirm the date.")],
                [("Quiero que me revises esto.", "Solicito una revisión del expediente.", "The formal letter uses the same request, in the third person."),
                 ("Le agradecería que me confirma.", "Le agradecería que me confirmara.", "agradecería que takes the imperfect subjunctive.")]),
              [D("Ana", "¿Cómo pido una revisión sin sonar agresiva?", "KOH-moh PEE-doh OO-nah reh-bee-SYOHN seen soh-NAR ah-greh-SEE-bah?", "How do I ask for a review without sounding aggressive?"),
               D("Ben", "«Expongo los hechos y solicito una revisión. Le agradecería que me confirmara la fecha.»", "eks-POHN-goh lohs EH-chohs ee soh-LEE-see-toh OO-nah reh-bee-SYOHN. leh ah-grah-deh-seh-REE-ah keh meh kohn-feer-MAH-rah lah FEH-chah.", "'I set out the facts and request a review. I would be grateful if you would confirm the date.'"),
               D("Ana", "Suena firme, no agresivo.", "SWEH-nah FEER-meh, noh ah-greh-SEE-boh.", "It sounds firm, not aggressive."),
               D("Ben", "Ese es el registro: firme y cortés a la vez.", "EH-seh es el reh-HEES-troh: FEER-meh ee kor-TEHS ah lah BEHS.", "That is the register: firm and polite at once.")],
              WS("Formal-letter worksheet", [
                  T("Write the moves.", ["I set out the facts", "I request a review", "I would be grateful if you would confirm the date"],
                    ["Expongo los hechos.", "Solicito una revisión.", "Le agradecería que me confirmara la fecha."]),
                  T("Choose the register.", ["formal firm request", "neutral alternative"],
                    ["Solicito que se revise el expediente.", "Quisiera pedir una revisión."]),
              ])),
            L("Reclamar por escrito: hechos, fundamentos, solicitud",
              "A written claim has three numbered parts: LOS HECHOS (facts), LOS FUNDAMENTOS "
              "(grounds), LA SOLICITUD (the request).",
              [V("los hechos", "lohs EH-chohs", "the facts", "noun"),
               V("los fundamentos", "lohs foon-dah-MEN-tohs", "the grounds", "noun"),
               V("la solicitud", "lah soh-lee-see-TOOD", "the request", "noun"),
               V("adjuntar", "ahd-hoon-TAR", "to attach", "verb"),
               V("el expediente", "el eks-peh-DYEN-teh", "the file, the case", "noun")],
              G("Claim structure",
                "primero, los hechos · segundo, los fundamentos · por último, la solicitud",
                "Primero: los hechos, con fecha y número de contrato. Segundo: los fundamentos, "
                "con la cláusula aplicable. Por último: la solicitud, en una frase. The numbering "
                "is the argument.",
                [X("Primero, los hechos: el servicio se interrumpió el 3 de mayo.", "pree-MEH-roh, lohs EH-chohs: el sehr-BEE-syoh seh een-teh-rroom-PYOH el trehs deh MAH-yoh.", "First, the facts: the service was interrupted on 3 May."),
                 X("Segundo, los fundamentos: la cláusula séptima del contrato.", "seh-GOON-doh, lohs foon-dah-MEN-tohs: lah KLAH-soo-lah sep-TEE-mah del kohn-TRAH-toh.", "Second, the grounds: clause seven of the contract."),
                 X("Por último, solicito una compensación.", "por OOL-tee-moh, soh-LEE-see-toh OO-nah kohm-pen-sah-SYOHN.", "Lastly, I request compensation.")],
                [("Fundamentos: pues porque no funcionó.", "Fundamentos: la cláusula séptima del contrato.", "Grounds are the rule that was broken, not the annoyance."),
                 ("Solicito que me dais dinero.", "Solicito una compensación.", "The request is a noun phrase in the formal register.")]),
              [D("Ben", "¿Cómo ordeno la reclamación?", "KOH-moh or-DEH-noh lah reh-klah-mah-SYOHN?", "How do I order the claim?"),
               D("Ana", "Hechos con fecha, fundamentos con cláusula, solicitud en una frase.", "EH-chohs kohn FEH-chah, foon-dah-MEN-tohs kohn KLAH-soo-lah, soh-lee-see-TOOD en OO-nah FRAH-seh.", "Facts with a date, grounds with a clause, the request in one sentence."),
               D("Ben", "«Primero, los hechos: el servicio se interrumpió el 3 de mayo.»", "pree-MEH-roh, lohs EH-chohs: el sehr-BEE-syoh seh een-teh-rroom-PYOH el trehs deh MAH-yoh.", "'First, the facts: the service was interrupted on 3 May.'"),
               D("Ana", "Exacto. Y adjunta la factura: sin prueba, no hay expediente.", "ek-SAHK-toh. ee ahd-HOON-tah lah fak-TOO-rah: seen PRWEH-bah, noh eye eks-peh-DYEN-teh.", "Exactly. And attach the invoice: without proof, there is no file.")],
              WS("Claim worksheet", [
                  T("Order the claim.", ["first, the facts with the date", "second, the grounds with the clause", "lastly, the request in one sentence"],
                    ["Primero, los hechos: …", "Segundo, los fundamentos: la cláusula …", "Por último, solicito …"]),
                  T("Attach the proof.", ["attach the invoice", "the file number"],
                    ["Adjunto la factura.", "el número de expediente"]),
              ])),
            L("Disculparse formalmente: lamentamos informarle",
              "Formal apologies are impersonal and specific: LAMENTAMOS INFORMARLE DE QUE … , LE "
              "PEDIMOS DISCULPAS POR LAS MOLESTIAS, y TOMAMOS NOTA PARA EVITARLO.",
              [V("lamentar", "lah-men-TAR", "to regret", "verb"),
               V("las molestias", "lahs moh-LES-tyahs", "the inconvenience", "noun"),
               V("tomar nota", "toh-MAR NOH-tah", "to take note", "phrase"),
               V("subsanar", "soob-sah-NAR", "to remedy", "verb"),
               V("a la mayor brevedad", "ah lah mah-YOR breh-VEH-dahd", "as soon as possible", "phrase")],
              G("Formal apology",
                "lamentamos informarle de que … · le pedimos disculpas por las molestias · lo subsanaremos a la mayor brevedad",
                "Lamentamos informarle de que su pedido se ha retrasado. Le pedimos disculpas por "
                "las molestias; lo subsanaremos a la mayor brevedad. No excuses, no drama — a "
                "fact, an apology, a remedy, a date.",
                [X("Lamentamos informarle de que su pedido se ha retrasado.", "lah-men-TAH-mohs een-for-MAR-leh deh keh soo peh-DEE-doh seh ah reh-trah-SAH-doh.", "We regret to inform you that your order has been delayed."),
                 X("Le pedimos disculpas por las molestias.", "leh peh-DEE-mohs dees-KOOL-pahs por lahs moh-LES-tyahs.", "We apologise for the inconvenience."),
                 X("Lo subsanaremos a la mayor brevedad.", "loh soob-sah-nah-REH-mohs ah lah mah-YOR breh-VEH-dahd.", "We will remedy it as soon as possible.")],
                [("Perdón, es que somos un desastre.", "Lamentamos las molestias; lo subsanaremos.", "Formal apology removes the person and keeps the commitment."),
                 ("Le pedimos disculpas por las molestia.", "Le pedimos disculpas por las molestias.", "molestias is plural.")]),
              [D("Ana", "El cliente está enfadado. ¿Qué le escribo?", "el KLYEHN-teh es-TAH en-fah-DAH-doh. keh leh es-KREE-boh?", "The client is angry. What do I write?"),
               D("Ben", "«Lamentamos informarle de que su pedido se ha retrasado.»", "lah-men-TAH-mohs een-for-MAR-leh deh keh soo peh-DEE-doh seh ah reh-trah-SAH-doh.", "'We regret to inform you that your order has been delayed.'"),
               D("Ana", "¿Y la disculpa?", "ee lah dees-KOOL-pah?", "And the apology?"),
               D("Ben", "«Le pedimos disculpas por las molestias; lo subsanaremos a la mayor brevedad.»", "leh peh-DEE-mohs dees-KOOL-pahs por lahs moh-LES-tyahs; loh soob-sah-nah-REH-mohs ah lah mah-YOR breh-VEH-dahd.", "'We apologise for the inconvenience; we will remedy it as soon as possible.'")],
              WS("Apology worksheet", [
                  T("Write the apology.", ["we regret to inform you that the order is delayed", "we apologise for the inconvenience", "we will remedy it as soon as possible"],
                    ["Lamentamos informarle de que el pedido se ha retrasado.", "Le pedimos disculpas por las molestias.", "Lo subsanaremos a la mayor brevedad."]),
                  T("Add the commitment.", ["we take note to avoid it", "the new date is 12 May"],
                    ["Tomamos nota para evitarlo.", "La nueva fecha es el 12 de mayo."]),
              ])),
        ]},
        {"id": "B2+-U3", "title": "Citar, resumir, cerrar", "lessons": [
            L("Citar y reformular: en palabras de …, dicho de otro modo",
              "Quotation in Spanish marks its own voice: EN PALABRAS DE X … , SEGÚN X … , COMO "
              "SEÑALA X … Then the reformulation: ES DECIR, O SEA, DICHO DE OTRO MODO.",
              [V("en palabras de", "en pah-LAH-brahs deh", "in the words of", "phrase"),
               V("señalar", "seh-nyah-LAR", "to point out", "verb"),
               V("es decir", "es deh-SEER", "that is to say", "phrase"),
               V("dicho de otro modo", "DEE-choh deh OH-troh MOH-doh", "put another way", "phrase"),
               V("la cita", "lah SEE-tah", "quotation", "noun")],
              G("Citation and reformulation",
                "en palabras de … · como señala … · es decir · dicho de otro modo",
                "En palabras de la autora, el problema es de diseño. Es decir, no es de dinero. "
                "Dicho de otro modo: el diseño decide el coste. Quotation, reformulation, "
                "consequence.",
                [X("En palabras de la autora, el problema es de diseño.", "en pah-LAH-brahs deh lah ow-TOH-rah, el proh-BLEH-mah es deh dee-SEH-nyoh.", "In the author's words, the problem is one of design."),
                 X("Como señala el informe, faltan datos.", "KOH-moh seh-NYAH-lah el een-FOR-meh, FAHL-tahn DAH-tohs.", "As the report points out, data is missing."),
                 X("Dicho de otro modo: el diseño decide el coste.", "DEE-choh deh OH-troh MOH-doh: el dee-SEH-nyoh deh-SEE-deh el KOHS-teh.", "Put another way: design decides the cost.")],
                [("La autora dice que el problema es de diseño y yo también.", "En palabras de la autora, el problema es de diseño.", "Citation separates the quoted voice from yours."),
                 ("Es decir o sea, en otras palabras distintas.", "Es decir, en otras palabras …", "One reformulation marker per sentence.")]),
              [D("Ana", "¿Cómo meto la cita sin perder mi voz?", "KOH-moh MEH-toh lah SEE-tah seen per-DEHR mee bohs?", "How do I insert the quotation without losing my voice?"),
               D("Ben", "Cita y luego reformula: en palabras de la autora … es decir …", "SEE-tah ee LWEH-goh reh-for-MOO-lah: en pah-LAH-brahs deh lah ow-TOH-rah … es deh-SEER …", "Quote and then reformulate: in the author's words … that is to say …"),
               D("Ana", "«En palabras de la autora, el problema es de diseño. Es decir, no es de dinero.»", "en pah-LAH-brahs deh lah ow-TOH-rah, el proh-BLEH-mah es deh dee-SEH-nyoh. es deh-SEER, noh es deh dee-NEH-roh.", "'In the author's words, the problem is one of design. That is to say, it is not one of money.'"),
               D("Ben", "Ahora la cita trabaja para tu argumento.", "ah-OH-rah lah SEE-tah trah-BAH-hah PAH-rah too ar-goo-MEN-toh.", "Now the quotation works for your argument.")],
              WS("Citation worksheet", [
                  T("Cite and reformulate.", ["in the author's words", "as the report points out", "put another way"],
                    ["En palabras de la autora, …", "Como señala el informe, …", "Dicho de otro modo, …"]),
                  T("Draw the consequence.", ["that is to say, it is not about money", "the design decides the cost"],
                    ["Es decir, no es de dinero.", "El diseño decide el coste."]),
              ])),
            L("Resumir una discusión: en síntesis, a grandes rasgos",
              "A summary names the positions and the shared ground: EN SÍNTESIS, DOS POSTURAS … ; A "
              "GRANDES RASGOS … ; EN SUMA …",
              [V("en síntesis", "en SEEN-teh-sees", "in short, to sum up", "phrase"),
               V("a grandes rasgos", "ah GRAHN-dehs RAHS-gohs", "broadly speaking", "phrase"),
               V("en suma", "en SOO-mah", "in sum", "phrase"),
               V("la postura", "lah pohs-TOO-rah", "position", "noun"),
               V("coincidir en", "koh-een-see-DEER en", "to agree on", "verb")],
              G("Summary frame",
                "en síntesis, dos posturas … · a grandes rasgos … · coinciden en que …",
                "En síntesis, dos posturas: una pide rapidez, otra pide pruebas. A grandes rasgos, "
                "ambas coinciden en que falta información. The summary counts the positions before "
                "it judges them.",
                [X("En síntesis, hay dos posturas.", "en SEEN-teh-sees, eye dohs pohs-TOO-rahs.", "In short, there are two positions."),
                 X("A grandes rasgos, ambas coinciden en que falta información.", "ah GRAHN-dehs RAHS-gohs, AHM-bahs koh-een-SEE-dehn en keh FAHL-tah een-for-mah-SYOHN.", "Broadly speaking, both agree that information is missing."),
                 X("En suma, el acuerdo es posible.", "en SOO-mah, el ah-KWEHR-doh es poh-SEE-bleh.", "In sum, agreement is possible.")],
                [("En síntesis, yo creo que ellos están mal.", "En síntesis, hay dos posturas; el acuerdo es posible.", "A summary reports, it does not rule."),
                 ("A grandes rasgos, en la línea de, más o menos.", "A grandes rasgos, ambas posturas coinciden en lo esencial.", "One hedge is enough.")]),
              [D("Ben", "¿Cómo cierro la discusión del equipo?", "KOH-moh SYEH-rroh lah dees-koo-SYOHN del eh-KEE-poh?", "How do I close the team discussion?"),
               D("Ana", "Cuenta las posturas antes de juzgarlas: en síntesis, dos posturas …", "KWEEN-tah lahs pohs-TOO-rahs AHN-tehs deh hoos-GAR-lahs: en SEEN-teh-sees, dohs pohs-TOO-rahs …", "Count the positions before judging them: in short, two positions …"),
               D("Ben", "«En síntesis: una pide rapidez; otra, pruebas. Ambas coinciden en que falta información.»", "en SEEN-teh-sees: OO-nah PEE-deh rah-PEE-dehs; OH-trah, PRWEH-bahs. AHM-bahs koh-een-SEE-dehn en keh FAHL-tah een-for-mah-SYOHN.", "'In short: one asks for speed; the other, for evidence. Both agree that information is missing.'"),
               D("Ana", "Y así nadie se siente resumido a la fuerza.", "ee ah-SEE NAH-dee seh SYEHN-teh reh-soo-MEE-doh ah lah FWEHR-sah.", "And that way nobody feels summarised against their will.")],
              WS("Summary worksheet", [
                  T("Summarise the discussion.", ["in short, there are two positions", "broadly speaking, both agree", "in sum, agreement is possible"],
                    ["En síntesis, hay dos posturas.", "A grandes rasgos, ambas coinciden.", "En suma, el acuerdo es posible."]),
                  T("Name the shared ground.", ["both agree that information is missing", "one asks for speed, the other for evidence"],
                    ["Ambas coinciden en que falta información.", "Una pide rapidez; otra, pruebas."]),
              ])),
            L("Cerrar un texto: en definitiva, por todo lo anterior",
              "The final paragraph gathers and decides: por todo lo anterior, … ; EN DEFINITIVA, … ; "
              "CABE CONCLUIR QUE …",
              [V("en definitiva", "en deh-fee-nee-TEE-bah", "in the end, ultimately", "phrase"),
               V("por todo lo anterior", "por TOH-doh loh ahn-teh-RYOR", "for all the above", "phrase"),
               V("cabe concluir que", "KAH-beh kohn-kloo-EER keh", "one may conclude that", "phrase"),
               V("la conclusión", "lah kohn-kloo-SYOHN", "conclusion", "noun"),
               V("la recomendación", "lah reh-koh-men-dah-SYOHN", "recommendation", "noun")],
              G("Closing frame",
                "por todo lo anterior, … · en definitiva, … · cabe concluir que …",
                "Por todo lo anterior, cabe concluir que el retraso es evitable. En definitiva, la "
                "recomendación es simple: probar antes de prometer. A close decides and then "
                "recommends.",
                [X("Por todo lo anterior, cabe concluir que el retraso es evitable.", "por TOH-doh loh ahn-teh-RYOR, KAH-beh kohn-kloo-EER keh el reh-TRAH-soh es eh-ee-TAH-bleh.", "For all the above, one may conclude that the delay is avoidable."),
                 X("En definitiva, la recomendación es simple.", "en deh-fee-nee-TEE-bah, lah reh-koh-men-dah-SYOHN es SEEM-pleh.", "In the end, the recommendation is simple."),
                 X("Conclusión: probar antes de prometer.", "kohn-kloo-SYOHN: proh-BAR AHN-tehs deh proh-meh-TEHR.", "Conclusion: test before promising.")],
                [("En definitiva, gracias por leer.", "En definitiva, la recomendación es simple: probar antes de prometer.", "A close states a conclusion and a next step."),
                 ("Por todo lo anterior y también por otras cosas.", "Por todo lo anterior, cabe concluir que …", "The frame is fixed; the content carries the weight.")]),
              [D("Ana", "¿Cómo termino el informe?", "KOH-moh tehr-MEE-noh el een-FOR-meh?", "How do I end the report?"),
               D("Ben", "Concluye y recomienda: por todo lo anterior, cabe concluir que …", "kohn-kloo-EH-ee ee reh-koh-MYEHN-dah: por TOH-doh loh ahn-teh-RYOR, KAH-beh kohn-kloo-EER keh …", "Conclude and recommend: for all the above, one may conclude that …"),
               D("Ana", "«Por todo lo anterior, cabe concluir que el retraso es evitable.»", "por TOH-doh loh ahn-teh-RYOR, KAH-beh kohn-kloo-EER keh el reh-TRAH-soh es eh-ee-TAH-bleh.", "'For all the above, one may conclude that the delay is avoidable.'"),
               D("Ben", "Y una recomendación en la última línea: siempre la última línea.", "ee OO-nah reh-koh-men-dah-SYOHN en lah OOL-tee-mah LEE-neh-ah: SYEHM-preh lah OOL-tee-mah LEE-neh-ah.", "And a recommendation in the last line: always the last line.")],
              WS("Closing worksheet", [
                  T("Close the text.", ["for all the above, one may conclude that the delay is avoidable", "in the end, the recommendation is simple", "conclusion: test before promising"],
                    ["Por todo lo anterior, cabe concluir que el retraso es evitable.", "En definitiva, la recomendación es simple.", "Conclusión: probar antes de prometer."]),
                  T("Write the last line.", ["a recommendation", "the next step"],
                    ["La recomendación es …", "El siguiente paso es …"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Spanish formal writing is a register with its own verbs — expongo, solicito, "
                 "lamentamos, cabe concluir — and its own music: numbered facts, a clause as "
                 "grounds, and a request in one clean sentence. This half-step teaches the "
                 "register and the argument at the same time, because in Spanish public life they "
                 "arrive together: the moment a text becomes formal, it also becomes structured."),
        source_url="https://en.wikipedia.org/wiki/Business_etiquette",
        reading=("Por todo lo anterior, cabe concluir que el servicio no cumplió lo pactado. "
                 "Primero, los hechos: la interrupción duró cuatro días. Segundo, los fundamentos: "
                 "la cláusula séptima del contrato. Por último, la solicitud: una compensación "
                 "proporcional. Lamentamos las molestias; lo subsanaremos a la mayor brevedad."),
        reading_gloss=("For all the above, one may conclude that the service did not meet what was "
                       "agreed. First, the facts: the interruption lasted four days. Second, the "
                       "grounds: clause seven of the contract. Lastly, the request: proportional "
                       "compensation. We regret the inconvenience; we will remedy it as soon as "
                       "possible."),
        listening=("Ana: Si bien la medida redujo el gasto, subió el riesgo.<br>Ben: No es menos cierto, sí. ¿Y qué recomiendas?<br>"
                   "Ana: Aplicarla con condiciones y revisar en tres meses.<br>Ben: Anotado: condiciones y revisión."),
        listening_gloss=("Ana: While the measure reduced spending, it increased risk. Ben: It is no "
                         "less true. And what do you recommend? Ana: Apply it with conditions and "
                         "review in three months. Ben: Noted: conditions and a review."),
        voice_tag=VOICE,
        idioms=[
            ("Dar fe", "to give faith", "to attest, to confirm"),
            ("Dejar constancia", "to leave record", "to put on record"),
            ("Salvo error u omisión", "save error or omission", "errors and omissions excepted"),
            ("Con carácter urgente", "with urgent character", "as a matter of urgency"),
            ("Tomar nota", "to take note", "to note it down"),
            ("Al pie de la letra", "at the foot of the letter", "to the letter"),
            ("Poner en conocimiento", "to put in knowledge", "to inform officially"),
            ("Sin ánimo de lucro", "without profit motive", "non-profit"),
            ("A los efectos oportunos", "for the opportune effects", "for whatever purpose may be required"),
            ("Quedar constancia", "for record to remain", "for the record"),
        ],
        mistakes=[
            ("Si bien subió el precio, pero bajó la calidad.", "Si bien subió el precio, no es menos cierto que bajó la calidad.", "si bien already contrasts; do not add pero."),
            ("No solo subió el precio, sino bajó la calidad.", "No solo subió el precio, sino que además bajó la calidad.", "The second clause takes sino que además."),
            ("Quiero que me revises el expediente (in a formal letter).", "Solicito una revisión del expediente.", "Formal letters use solicitar, in the first person of the act."),
        ],
        task_title="Write a one-page formal claim",
        task_instructions=("Write a real complaint you could send: a heading, one sentence of "
                           "context, then the three numbered moves — hechos with dates, "
                           "fundamentos with the rule or clause, solicitud in a single sentence. "
                           "Close with lamentamos … / le agradecería que me confirmara … and attach "
                           "the proof by name. Finally, rewrite your opening line at B1 level "
                           "(quiero que me …) and compare the two registers."),
    ),
    "test": [
        ("translate_en", "Say: Not only did the price rise, but the quality also fell.", "No solo subió el precio, sino que además bajó la calidad."),
        ("translate_es", "Si bien redujo el gasto, no es menos cierto que aumentó el riesgo.", "While it reduced spending, it is no less true that it increased the risk."),
        ("multiple_choice", "Which opens a formal request?", "Solicito una revisión del expediente."),
        ("fill_in_the_blank", "Le agradecería que me ___ la fecha.", "confirmara"),
        ("word_selection", "Select the Spanish for the grounds (of a claim).", "los fundamentos"),
        ("error_correction", "No solo subió el precio, sino bajó la calidad.", "No solo subió el precio, sino que además bajó la calidad."),
        ("dialogue_completion", "Complete: Lamentamos informarle de que su pedido se ha ___.", "retrasado"),
        ("matching", "Match «tomar nota» to its meaning.", "to note it down"),
        ("reading_comprehension", "How long did the interruption last?", "four days"),
        ("inference", "«no es menos cierto» — what does the speaker accept?", "the opposing fact, while keeping the conclusion"),
        ("main_idea", "Por todo lo anterior, cabe concluir que el retraso es evitable. What is this?", "a conclusion of a report"),
        ("detail_identification", "Which clause is cited as grounds?", "clause seven of the contract"),
    ],
}

HALFSTEPS["C1+"] = {
    "title": "Spanish C1+ — Register, strategy and the spoken formal",
    "native": NATIVE,
    "goals": [
        "Rewrite one content in three registers without changing a single fact",
        "Grade commitment precisely: me consta, no me consta, me consta que …",
        "Handle a hostile question and chair the round-table summary",
    ],
    "units": [
        {"id": "C1+-U1", "title": "Precisión y compromiso", "lessons": [
            L("El mismo contenido en tres registros",
              "Register is a dial: LO QUE PASA ES QUE … (chat), EL PROBLEMA ES QUE … (standard), "
              "CABE SEÑALAR QUE … (formal). Same fact, three rooms.",
              [V("el registro", "el reh-HEES-troh", "register", "noun"),
               V("coloquial", "koh-loh-KYAL", "colloquial", "adjective"),
               V("culto", "KOOL-toh", "learned, formal", "adjective"),
               V("cabe señalar que", "KAH-beh seh-nyah-LAR keh", "it should be noted that", "phrase"),
               V("lo que pasa es que", "loh keh PAH-sah es keh", "the thing is that", "phrase")],
              G("Register dial",
                "lo que pasa es que … · el problema es que … · cabe señalar que …",
                "Lo que pasa es que faltan datos. El problema es que faltan datos. Cabe señalar "
                "que la información disponible es incompleta. One fact, three registers — and the "
                "formal one never gets longer than the fact.",
                [X("Lo que pasa es que faltan datos.", "loh keh PAH-sah es keh FAHL-tahn DAH-tohs.", "The thing is that data is missing."),
                 X("El problema es que faltan datos.", "el proh-BLEH-mah es keh FAHL-tahn DAH-tohs.", "The problem is that data is missing."),
                 X("Cabe señalar que la información disponible es incompleta.", "KAH-beh seh-nyah-LAR keh lah een-for-mah-SYOHN dees-poh-NEE-bleh es een-kohm-PLEH-tah.", "It should be noted that the available information is incomplete.")],
                [("En el registro formal hay que decir muchas más palabras.", "Cabe señalar que la información disponible es incompleta.", "Formality changes the frame, not the length."),
                 ("Lo que pasa es que, cabe señalar que, faltan datos.", "El problema es que faltan datos.", "One register marker per sentence.")]),
              [D("Ana", "El cliente pregunta lo mismo otra vez.", "el KLYEHN-teh pre-GOON-tah loh MEES-moh OH-trah behs.", "The client is asking the same thing again."),
               D("Ben", "Depende del registro: al cliente, «el problema es que faltan datos».", "deh-PEHN-deh del reh-HEES-troh: al KLYEHN-teh, el proh-BLEH-mah es keh FAHL-tahn DAH-tohs.", "It depends on the register: to the client, 'the problem is that data is missing'."),
               D("Ana", "¿Y en el informe?", "ee en el een-FOR-meh?", "And in the report?"),
               D("Ben", "«Cabe señalar que la información disponible es incompleta.»", "KAH-beh seh-nyah-LAR keh lah een-for-mah-SYOHN dees-poh-NEE-bleh es een-kohm-PLEH-tah.", "'It should be noted that the available information is incomplete.'")],
              WS("Register worksheet", [
                  T("Say the same fact three ways.", ["data is missing (chat)", "the problem is that data is missing (standard)", "it should be noted that information is incomplete (formal)"],
                    ["Lo que pasa es que faltan datos.", "El problema es que faltan datos.", "Cabe señalar que la información es incompleta."]),
                  T("Pick the register.", ["to a client", "in a report"],
                    ["El problema es que …", "Cabe señalar que …"]),
              ])),
            L("El compromiso graduado: me consta, no me consta",
              "Institutions speak with ME CONSTA (I can attest), NO ME CONSTA (I have no record), ME "
              "CONSTA QUE … — a scale from certainty to ignorance that keeps the speaker safe.",
              [V("me consta", "meh KOHNS-tah", "I can attest", "phrase"),
               V("no me consta", "noh meh KOHNS-tah", "I have no record of it", "phrase"),
               V("constar por escrito", "kohns-TAR por es-KREE-toh", "to be on record", "phrase"),
               V("según mi información", "seh-GOON mee een-for-mah-SYOHN", "according to my information", "phrase"),
               V("hasta donde sé", "AHS-tah DON-deh seh", "as far as I know", "phrase")],
              G("Commitment scale",
                "me consta · no me consta · hasta donde sé · según mi información",
                "Me consta que la solicitud se presentó en plazo. No me consta ninguna reclamación "
                "posterior. Hasta donde sé, el expediente sigue abierto. The scale protects the "
                "speaker better than any adjective.",
                [X("Me consta que la solicitud se presentó en plazo.", "meh KOHNS-tah keh lah soh-lee-see-TOOD seh preh-sen-TOH en PLAH-soh.", "I can attest that the application was submitted on time."),
                 X("No me consta ninguna reclamación posterior.", "noh meh KOHNS-tah neen-GOO-nah reh-klah-mah-SYOHN pos-teh-RYOR.", "I have no record of any later complaint."),
                 X("Hasta donde sé, el expediente sigue abierto.", "AHS-tah DON-deh seh, el eks-peh-DYEN-teh SEE-geh ah-BYEHR-toh.", "As far as I know, the file is still open.")],
                [("Es verdad, seguro, yo lo vi.", "Me consta que …", "The institutional scale replaces the assertion."),
                 ("No sé nada de eso.", "No me consta.", "The neutral institutional form is not me consta.")]),
              [D("Funcionaria", "¿Le consta que hubo una reclamación?", "leh KOHNS-tah keh OO-boh OO-nah reh-klah-mah-SYOHN?", "Do you have a record of a complaint?"),
               D("Gestor", "No me consta ninguna posterior a marzo.", "noh meh KOHNS-tah neen-GOO-nah pos-teh-RYOR ah MAR-soh.", "I have no record of any after March."),
               D("Funcionaria", "¿Y la solicitud inicial?", "ee lah soh-lee-see-TOOD ee-nee-SYAL?", "And the initial application?"),
               D("Gestor", "Me consta que se presentó en plazo, según mi información.", "meh KOHNS-tah keh seh preh-sen-TOH en PLAH-soh, seh-GOON mee een-for-mah-SYOHN.", "I can attest it was submitted on time, according to my information.")],
              WS("Commitment worksheet", [
                  T("Grade the commitment.", ["I can attest that it was submitted on time", "I have no record of a later complaint", "as far as I know"],
                    ["Me consta que se presentó en plazo.", "No me consta ninguna reclamación posterior.", "Hasta donde sé …"]),
                  T("Sources of information.", ["according to my information", "it is on record"],
                    ["Según mi información, …", "Consta por escrito."]),
              ])),
            L("El matiz que cambia la frase: en todo caso, cuando menos",
              "Three hedges do surgical work: en todo caso (in any case), CUANDO MENOS (at least), "
              "SI ACASO (if anything).",
              [V("en todo caso", "en TOH-doh KAH-soh", "in any case", "phrase"),
               V("cuando menos", "KWAHN-doh MEH-nohs", "at least", "phrase"),
               V("si acaso", "see ah-KAH-soh", "if anything", "phrase"),
               V("en principio", "en preen-SEE-pyoh", "in principle", "phrase"),
               V("a lo sumo", "ah loh SOO-moh", "at most", "phrase")],
              G("Surgical hedges",
                "en todo caso · cuando menos · si acaso · a lo sumo",
                "Quizá llegue tarde; en todo caso, avisaré. Cuando menos, el aviso llega. Si "
                "acaso, retrasamos una semana. Each hedge adjusts one part of the sentence — time, "
                "degree, condition — and leaves the rest untouched.",
                [X("En todo caso, avisaré.", "en TOH-doh KAH-soh, ah-bee-sah-REH.", "In any case, I will let you know."),
                 X("Cuando menos, el aviso llega.", "KWAHN-doh MEH-nohs, el ah-BEE-soh YEH-gah.", "At least the notice arrives."),
                 X("Si acaso, retrasamos una semana.", "see ah-KAH-soh, reh-trah-SAH-mohs OO-nah seh-MAH-nah.", "If anything, we postpone it by a week.")],
                [("En todo caso, quizá, puede, no sé.", "En todo caso, retrasamos una semana.", "One hedge; the rest of the sentence stays decisive."),
                 ("Cuando menos no.", "Cuando menos, el aviso llega.", "The hedge needs a proposition under it.")]),
              [D("Jefa", "¿Retrasamos el lanzamiento?", "reh-trah-SAH-mohs el lahn-sah-MYEN-toh?", "Do we postpone the launch?"),
               D("Ben", "Si acaso, una semana. En todo caso, avisaré a los clientes.", "see ah-KAH-soh, OO-nah seh-MAH-nah. en TOH-doh KAH-soh, ah-bee-sah-REH ah lohs KLYEHN-tehs.", "If anything, a week. In any case, I'll let the clients know."),
               D("Jefa", "¿Y el presupuesto?", "ee el preh-soo-PWEHS-toh?", "And the budget?"),
               D("Ben", "Cuando menos, lo revisamos antes de firmar.", "KWAHN-doh MEH-nohs, loh reh-bee-SAH-mohs AHN-tehs deh feer-MAR.", "At least we review it before signing.")],
              WS("Hedge worksheet", [
                  T("Adjust one part.", ["in any case, I will let you know", "at least, the notice arrives", "if anything, a week"],
                    ["En todo caso, avisaré.", "Cuando menos, el aviso llega.", "Si acaso, una semana."]),
                  T("Set the limits.", ["in principle yes", "at most two weeks"],
                    ["En principio, sí.", "A lo sumo, dos semanas."]),
              ])),
        ]},
        {"id": "C1+-U2", "title": "Estrategia: decir y desmontar", "lessons": [
            L("El eufemismo y su desmontaje",
              "Official Spanish hides facts behind soft nouns: AJUSTE DE PLANTILLA (job cuts), "
              "DAÑOS COLATERALES (civilian deaths), INCIDENCIA TÉCNICA (an outage).",
              [V("el eufemismo", "el eh-oo-feh-MEES-moh", "euphemism", "noun"),
               V("el ajuste", "el ah-HOOS-teh", "adjustment (cuts)", "noun"),
               V("la incidencia", "lah een-see-DEN-syah", "incident, outage", "noun"),
               V("traducir", "trah-doo-SEER", "to translate", "verb"),
               V("llamar a las cosas por su nombre", "yah-MAR ah lahs KOH-sahs por soo NOHM-breh", "to call things by their name", "phrase")],
              G("Undoing a euphemism",
                "esto es lo que se llama … · traducido: … · en lenguaje llano, …",
                "«Ajuste de plantilla»: traducido, cuarenta despidos. «Incidencia técnica»: en "
                "lenguaje llano, el servicio estuvo caído nueve horas. Naming the euphemism is "
                "itself the argument.",
                [X("«Ajuste de plantilla»: traducido, cuarenta despidos.", "ah-HOOS-teh deh plahn-TEE-yah: trah-doo-SEE-doh, kwah-REN-tah des-PEE-dohs.", "'Workforce adjustment': translated, forty lay-offs."),
                 X("En lenguaje llano, el servicio estuvo caído nueve horas.", "en len-GWAH-heh YAH-noh, el sehr-BEE-syoh es-TOO KAH-ee-doh NWEH-beh OH-rahs.", "In plain language, the service was down for nine hours."),
                 X("Llamemos a las cosas por su nombre.", "yah-MEH-mohs ah lahs KOH-sahs por soo NOHM-breh.", "Let's call things by their name.")],
                [("Hay un ajuste de plantilla, o sea, nada importante.", "«Ajuste de plantilla»: traducido, cuarenta despidos.", "The dismantling names the number."),
                 ("Eso es propaganda y mentira.", "Esto se llama «incidencia técnica»: en llano, nueve horas caído.", "Name the mechanism instead of denouncing it.")]),
              [D("Ana", "El comunicado dice «ajuste de plantilla».", "el koh-moo-nee-KAH-doh DEE-seh ah-HOOS-teh deh plahn-TEE-yah.", "The statement says 'workforce adjustment'."),
               D("Ben", "Traducido: cuarenta despidos.", "trah-doo-SEE-doh: kwah-REN-tah des-PEE-dohs.", "Translated: forty lay-offs."),
               D("Ana", "Y «incidencia técnica».", "ee een-see-DEN-syah TEK-nee-kah.", "And 'technical incident'."),
               D("Ben", "En lenguaje llano: nueve horas sin servicio.", "en len-GWAH-heh YAH-noh: NWEH-beh OH-rahs seen sehr-BEE-syoh.", "In plain language: nine hours with no service.")],
              WS("Euphemism worksheet", [
                  T("Translate the euphemism.", ["workforce adjustment", "technical incident", "collateral damage"],
                    ["cuarenta despidos", "nueve horas sin servicio", "víctimas civiles"]),
                  T("Name the mechanism.", ["this is what is called …", "in plain language"],
                    ["Esto es lo que se llama …", "En lenguaje llano, …"]),
              ])),
            L("El discurso oral formal: anunciar, ordenar, cerrar",
              "A formal talk is signposted: VOY A ESTRUCTURAR MI INTERVENCIÓN EN TRES PUNTOS · ME "
              "DETENGO EN EL SEGUNDO · PARA TERMINAR · QUEDO A SU DISPOSICIÓN.",
              [V("la intervención", "lah een-tehr-ben-SYOHN", "speech, intervention", "noun"),
               V("detenerse en", "deh-teh-NEHR-seh en", "to dwell on", "verb"),
               V("para terminar", "PAH-rah tehr-mee-NAR", "to finish", "phrase"),
               V("quedar a disposición", "keh-DAR ah dees-poh-see-SYOHN", "to be at your disposal", "phrase"),
               V("el punto", "el POON-toh", "point (of an argument)", "noun")],
              G("Talk signposts",
                "voy a estructurar mi intervención en tres puntos · me detengo en … · para terminar · quedo a su disposición",
                "Voy a estructurar mi intervención en tres puntos. En el primero, el contexto. Me "
                "detengo en el segundo: los datos. Para terminar, una recomendación. The signposts "
                "are the talk; the sentences fill them.",
                [X("Voy a estructurar mi intervención en tres puntos.", "boy ah es-trook-too-RAR mee een-tehr-ben-SYOHN en trehs POON-tohs.", "I will structure my talk in three points."),
                 X("Me detengo en el segundo punto.", "meh deh-TEHN-goh en el seh-GOON-doh POON-toh.", "I will dwell on the second point."),
                 X("Para terminar, quedo a su disposición.", "PAH-rah tehr-mee-NAR, KEH-doh ah soo dees-poh-see-SYOHN.", "To finish, I remain at your disposal.")],
                [("Bueno, pues voy a hablar de cosas.", "Voy a estructurar mi intervención en tres puntos.", "The formal talk announces its own shape."),
                 ("Para terminar, gracias, adiós.", "Para terminar, una recomendación: probar antes de prometer.", "The close delivers the last point, then steps back.")]),
              [D("Moderadora", "Tiene cinco minutos.", "TYEH-neh SEEN-koh mee-NOO-tohs.", "You have five minutes."),
               D("Ponente", "Voy a estructurar mi intervención en tres puntos.", "boy ah es-trook-too-RAR mee een-tehr-ben-SYOHN en trehs POON-tohs.", "I will structure my talk in three points."),
               D("Moderadora", "Adelante.", "ah-deh-LAHN-teh.", "Go ahead."),
               D("Ponente", "Me detengo en el segundo —los datos— y, para terminar, una recomendación.", "meh deh-TEHN-goh en el seh-GOON-doh —lohs DAH-tohs— ee, PAH-rah tehr-mee-NAR, OO-nah reh-koh-men-dah-SYOHN.", "I will dwell on the second — the data — and, to finish, one recommendation.")],
              WS("Talk worksheet", [
                  T("Signpost the talk.", ["I will structure it in three points", "I dwell on the second", "to finish, one recommendation"],
                    ["Voy a estructurar mi intervención en tres puntos.", "Me detengo en el segundo punto.", "Para terminar, una recomendación."]),
                  T("Close with the formal offer.", ["I remain at your disposal", "thank you for your attention"],
                    ["Quedo a su disposición.", "Gracias por su atención."]),
              ])),
            L("Traducir registro: del titular al informe y vuelta",
              "A headline and a report say the same thing in two grammars: PARO AL ALZA (headline "
              "noun pile) versus LA TASA DE PARO AUMENTÓ UN 2 % (report).",
              [V("el titular", "el tee-too-LAR", "headline", "noun"),
               V("la tasa", "lah TAH-sah", "rate", "noun"),
               V("el paro", "el PAH-roh", "unemployment", "noun"),
               V("el informe", "el een-FOR-meh", "report", "noun"),
               V("la cifra", "lah SEE-frah", "figure, number", "noun")],
              G("Headline ↔ report",
                "paro al alza (titular) · la tasa de paro aumentó un 2 % (informe)",
                "El titular: paro al alza. El informe: la tasa de paro aumentó un dos por ciento en "
                "el trimestre. The headline piles nouns; the report builds a sentence. A translator "
                "moves between the two on purpose.",
                [X("Titular: paro al alza.", "tee-too-LAR: PAH-roh al AHL-sah.", "Headline: unemployment up."),
                 X("En el informe: la tasa de paro aumentó un dos por ciento.", "en el een-FOR-meh: lah TAH-sah deh PAH-roh ow-men-TOH oon dohs por syen-TOH.", "In the report: the unemployment rate rose by two per cent."),
                 X("La cifra no se explica sola.", "lah SEE-frah noh seh eks-PLEE-kah SOH-lah.", "The figure does not explain itself.")],
                [("Titular: el paro subió porque hubo una crisis y mucha gente.", "Titular: paro al alza.", "Headlines pile the fact; the sentence is the report's job."),
                 ("Informe: paro al alza, más o menos.", "Informe: la tasa de paro aumentó un 2 %.", "The report states the figure and its horizon.")]),
              [D("Ana", "¿Cómo paso el titular al informe?", "KOH-moh PAH-soh el tee-too-LAR al een-FOR-meh?", "How do I turn the headline into the report?"),
               D("Ben", "Pon verbo y cifra: la tasa de paro aumentó un dos por ciento.", "pohn BEHR-boh ee SEE-frah: lah TAH-sah deh PAH-roh ow-men-TOH oon dohs por syen-TOH.", "Add a verb and a figure: the unemployment rate rose by two per cent."),
               D("Ana", "¿Y al revés, del informe al titular?", "ee al reh-BEHS, del een-FOR-meh al tee-too-LAR?", "And the other way, from report to headline?"),
               D("Ben", "Quita el verbo y apila: paro al alza.", "KEE-tah el BEHR-boh ee ah-PEE-lah: PAH-roh al AHL-sah.", "Drop the verb and pile: unemployment up.")],
              WS("Register-swap worksheet", [
                  T("Turn the headline into a report sentence.", ["paro al alza", "precios en descenso"],
                    ["La tasa de paro aumentó un 2 %.", "Los precios descendieron ligeramente."]),
                  T("Turn the report sentence into a headline.", ["the price rose by four per cent", "consumption fell"],
                    ["Precios al alza.", "Consumo en descenso."]),
              ])),
        ]},
        {"id": "C1+-U3", "title": "Réplica, preguntas y mesa redonda", "lessons": [
            L("La réplica elegante: me permito discrepar",
              "A formal disagreement opens with respect and states the disagreement plainly: CON EL "
              "DEBIDO RESPETO, ME PERMITO DISCREPAR; DONDE USTED VE UN COSTE, YO VEO UNA INVERSIÓN.",
              [V("me permito", "meh per-MEE-toh", "may I venture to", "phrase"),
               V("discrepar", "dees-kreh-PAR", "to disagree", "verb"),
               V("con el debido respeto", "kohn el deh-BEE-doh res-PEH-toh", "with due respect", "phrase"),
               V("donde usted ve …", "DON-deh oos-TEHD beh", "where you see …", "phrase"),
               V("el enfoque", "el en-FOH-keh", "approach, angle", "noun")],
              G("Formal rebuttal",
                "con el debido respeto, me permito discrepar · donde usted ve …, yo veo …",
                "Con el debido respeto, me permito discrepar. Donde usted ve un coste, yo veo una "
                "inversión a tres años. The formula keeps the person and disputes the frame.",
                [X("Con el debido respeto, me permito discrepar.", "kohn el deh-BEE-doh res-PEH-toh, meh per-MEE-toh dees-kreh-PAR.", "With due respect, I venture to disagree."),
                 X("Donde usted ve un coste, yo veo una inversión.", "DON-deh oos-TEHD beh oon KOHS-teh, yoh BEH-oh OO-nah een-behr-SYOHN.", "Where you see a cost, I see an investment."),
                 X("Discrepo del enfoque, no del objetivo.", "dees-KREH-poh del en-FOH-keh, noh del ob-heh-TEE-boh.", "I disagree with the approach, not the objective.")],
                [("Está usted equivocado del todo.", "Con el debido respeto, me permito discrepar.", "The formula states the disagreement without the verdict."),
                 ("Me permito discrepar y usted no sabe nada.", "Discrepo del enfoque, no del objetivo.", "Dispute the frame, not the person's competence.")]),
              [D("Ponente", "El coste es insostenible.", "el KOHS-teh es een-sohs-teh-NEE-bleh.", "The cost is unsustainable."),
               D("Ana", "Con el debido respeto, me permito discrepar.", "kohn el deh-BEE-doh res-PEH-toh, meh per-MEE-toh dees-kreh-PAR.", "With due respect, I venture to disagree."),
               D("Ponente", "Le escucho.", "leh es-KOO-choh.", "I'm listening."),
               D("Ana", "Donde usted ve un coste, yo veo una inversión a tres años.", "DON-deh oos-TEHD beh oon KOHS-teh, yoh BEH-oh OO-nah een-behr-SYOHN ah trehs AH-nyohs.", "Where you see a cost, I see a three-year investment.")],
              WS("Rebuttal worksheet", [
                  T("Open the formal rebuttal.", ["with due respect, I venture to disagree", "I disagree with the approach, not the objective"],
                    ["Con el debido respeto, me permito discrepar.", "Discrepo del enfoque, no del objetivo."]),
                  T("Reframe the fact.", ["where you see a cost, I see a three-year investment", "where you see a risk, I see a market"],
                    ["Donde usted ve un coste, yo veo una inversión a tres años.", "Donde usted ve un riesgo, yo veo un mercado."]),
              ])),
            L("Responder a una pregunta hostil",
              "A hostile question is answered by reframing it: ANTES DE RESPONDER, ACLAREMOS LA "
              "PREMISA · SI ENTENDÍ BIEN, ME PREGUNTA …",
              [V("la premisa", "lah preh-MEE-sah", "premise", "noun"),
               V("reformular", "reh-for-moo-LAR", "to reformulate", "verb"),
               V("si entendí bien", "see en-ten-DEE byehn", "if I understood correctly", "phrase"),
               V("la pregunta", "lah preh-GOON-tah", "question", "noun"),
               V("responder", "res-pohn-DEHR", "to answer", "verb")],
              G("Answering a hostile question",
                "antes de responder, aclaremos la premisa · si entendí bien, me pregunta …",
                "Antes de responder, aclaremos la premisa: la decisión se tomó en marzo. Si entendí "
                "bien, me pregunta por qué. Respondo: por prudencia. Three moves: premise, "
                "reformulation, answer.",
                [X("Antes de responder, aclaremos la premisa.", "AHN-tehs deh res-pohn-DEHR, ah-klah-REH-mohs lah preh-MEE-sah.", "Before answering, let us clarify the premise."),
                 X("Si entendí bien, me pregunta por qué.", "see en-ten-DEE byehn, meh pre-GOON-tah por KEH.", "If I understood correctly, you are asking me why."),
                 X("Respondo con una palabra: prudencia.", "res-POHN-doh kohn OO-nah pah-LAH-brah: proo-DEN-syah.", "I answer with one word: prudence.")],
                [("Esa pregunta es injusta.", "Antes de responder, aclaremos la premisa.", "Reframe the question instead of judging it."),
                 ("No voy a responder a eso.", "Si entendí bien, me pregunta por qué: respondo …", "Answer the reframed question, not the trap.")]),
              [D("Periodista", "¿Por qué ocultaron la información?", "por keh oh-kool-TAH-rohn lah een-for-mah-SYOHN?", "Why did you hide the information?"),
               D("Portavoz", "Antes de responder, aclaremos la premisa: no se ocultó, se publicó el día 4.", "AHN-tehs deh res-pohn-DEHR, ah-klah-REH-mohs lah preh-MEE-sah: noh seh oh-kool-TOH, seh poo-blee-KOH el DEE-ah KWAH-troh.", "Before answering, let us clarify the premise: nothing was hidden; it was published on the 4th."),
               D("Periodista", "¿Y el retraso?", "ee el reh-TRAH-soh?", "And the delay?"),
               D("Portavoz", "Si entendí bien, me pregunta por qué el día 4: por verificar los datos.", "see en-ten-DEE byehn, meh pre-GOON-tah por keh el DEE-ah KWAH-troh: por beh-ree-fee-KAR lohs DAH-tohs.", "If I understood correctly, you are asking why the 4th: to verify the data.")],
              WS("Hostile-question worksheet", [
                  T("Reframe before answering.", ["let us clarify the premise", "if I understood correctly, you are asking why"],
                    ["Aclaremos la premisa.", "Si entendí bien, me pregunta por qué."]),
                  T("Answer in the reframed frame.", ["to verify the data", "the decision was taken in March"],
                    ["Por verificar los datos.", "La decisión se tomó en marzo."]),
              ])),
            L("La mesa redonda: quién dijo qué y qué queda abierto",
              "Chairing means attributing precisely and closing what is still open: ANA SEÑALÓ QUE … "
              "· BEN OBJETÓ QUE … · QUEDA ABIERTO …",
              [V("señalar", "seh-nyah-LAR", "to point out", "verb"),
               V("objetar", "ob-heh-TAR", "to object", "verb"),
               V("quedar abierto", "keh-DAR ah-BYEHR-toh", "to remain open", "phrase"),
               V("la mesa redonda", "lah MEH-sah reh-DOHN-dah", "round table", "noun"),
               V("atribuir", "ah-tree-BWEER", "to attribute", "verb")],
              G("Chairing frame",
                "Ana señaló que … · Ben objetó que … · queda abierto …",
                "Ana señaló que faltan datos. Ben objetó que los datos llegan en mayo. Queda "
                "abierto el calendario. Attribution, objection, open question — the three-line "
                "close of every round table.",
                [X("Ana señaló que faltan datos.", "AH-nah seh-nyah-LOH keh FAHL-tahn DAH-tohs.", "Ana pointed out that data is missing."),
                 X("Ben objetó que los datos llegan en mayo.", "ben ob-heh-TOH keh lohs DAH-tohs YEH-gahn en MAH-yoh.", "Ben objected that the data arrives in May."),
                 X("Queda abierto el calendario.", "KEH-dah ah-BYEHR-toh el kah-lehn-DAH-ryoh.", "The calendar remains open.")],
                [("Ana dijo cosas y Ben también.", "Ana señaló que faltan datos; Ben objetó que llegan en mayo.", "Attribution names the claim, not the fact of speaking."),
                 ("Queda abierto y ya está.", "Queda abierto el calendario.", "The open question must be named.")]),
              [D("Moderadora", "Cerramos con una síntesis.", "seh-RRAH-mohs kohn OO-nah SEEN-teh-sees.", "Let's close with a summary."),
               D("Ana", "Ana señaló que faltan datos; Ben objetó que llegan en mayo.", "AH-nah seh-nyah-LOH keh FAHL-tahn DAH-tohs; ben ob-heh-TOH keh YEH-gahn en MAH-yoh.", "Ana pointed out that data is missing; Ben objected that it arrives in May."),
               D("Moderadora", "¿Qué queda abierto?", "keh KEH-dah ah-BYEHR-toh?", "What remains open?"),
               D("Ana", "El calendario: si los datos no llegan en mayo, no hay decisión.", "el kah-lehn-DAH-ryoh: see lohs DAH-tohs noh YEH-gahn en MAH-yoh, noh eye deh-see-SYOHN.", "The calendar: if the data does not arrive in May, there is no decision.")],
              WS("Round-table worksheet", [
                  T("Attribute precisely.", ["Ana pointed out that data is missing", "Ben objected that it arrives in May"],
                    ["Ana señaló que faltan datos.", "Ben objetó que los datos llegan en mayo."]),
                  T("Name what is open.", ["the calendar remains open", "if the data does not arrive, there is no decision"],
                    ["Queda abierto el calendario.", "Si los datos no llegan, no hay decisión."]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("At C1 the Spanish learner's problem is no longer grammar but strategy: which "
                 "register to wear, how firm a commitment to make, when to name a euphemism out "
                 "loud, and how to disagree in public without losing the room. The verbs of "
                 "institutional Spanish — me consta, cabe señalar, me permito discrepar — are the "
                 "tools of that strategy, and they are learnable, formula by formula, like "
                 "anything else in the language."),
        source_url="https://en.wikipedia.org/wiki/Register_(sociolinguistics)",
        reading=("Cabe señalar que la información disponible es incompleta. Me consta que la "
                 "solicitud se presentó en plazo; no me consta ninguna reclamación posterior. En "
                 "todo caso, el expediente sigue abierto y queda pendiente el calendario. Con el "
                 "debido respeto, discrepo del enfoque: donde se ve un coste, yo veo una inversión."),
        reading_gloss=("It should be noted that the available information is incomplete. I can "
                       "attest that the application was submitted on time; I have no record of any "
                       "later complaint. In any case, the file remains open and the calendar is "
                       "still pending. With due respect, I disagree with the approach: where a "
                       "cost is seen, I see an investment."),
        listening=("Periodista: ¿Por qué ocultaron la información?<br>Portavoz: Antes de responder, aclaremos la premisa.<br>"
                   "Periodista: Adelante.<br>Portavoz: No se ocultó; se publicó el día 4, al verificar los datos."),
        listening_gloss=("Journalist: Why did you hide the information? Spokesperson: Before "
                         "answering, let us clarify the premise. Journalist: Go ahead. "
                         "Spokesperson: Nothing was hidden; it was published on the 4th, when the "
                         "data was verified."),
        voice_tag=VOICE,
        idioms=[
            ("Quedar abierto", "to remain open", "to still be undecided"),
            ("Poner el foco", "to put the focus", "to focus attention"),
            ("Dar por zanjado", "to consider settled", "to consider the matter closed"),
            ("Dejar en el aire", "to leave in the air", "to leave hanging"),
            ("Marca el tono", "it sets the tone", "it sets the tone"),
            ("Perder el hilo", "to lose the thread", "to lose the thread of the argument"),
            ("Con el debido respeto", "with due respect", "with all due respect"),
            ("Poner en cuestión", "to put in question", "to call into question"),
            ("Ir al fondo", "to go to the bottom", "to get to the substance"),
            ("Sin salir del guion", "without leaving the script", "sticking to the script"),
        ],
        mistakes=[
            ("Me permito discrepar pero usted está equivocado.", "Me permito discrepar: donde usted ve un coste, yo veo una inversión.", "Dispute the frame, not the person."),
            ("Es verdad, yo lo he visto, seguro.", "Me consta.", "The institutional scale replaces the personal assertion."),
            ("No voy a responder a esa pregunta.", "Antes de responder, aclaremos la premisa.", "Reframe rather than refuse."),
        ],
        task_title="Chair a five-minute round table in Spanish",
        task_instructions=("Write the chair's nine lines for a round table you could actually hold: "
                           "state that the information is incomplete (cabe señalar), give two "
                           "commitments at different strengths (me consta, no me consta), reframe "
                           "one hostile question (antes de responder …), attribute two positions "
                           "(X señaló, Y objetó), and close by naming what remains open and what is "
                           "pending. Read it aloud: if a line needs a comma to survive, rewrite "
                           "the line."),
    ),
    "test": [
        ("translate_en", "Say: With due respect, I venture to disagree.", "Con el debido respeto, me permito discrepar."),
        ("translate_es", "Cabe señalar que la información disponible es incompleta.", "It should be noted that the available information is incomplete."),
        ("multiple_choice", "Which reframes a hostile question?", "Antes de responder, aclaremos la premisa."),
        ("fill_in_the_blank", "Me ___ que la solicitud se presentó en plazo.", "consta"),
        ("word_selection", "Select the formal register of «the thing is that».", "cabe señalar que"),
        ("error_correction", "No me sé nada de eso.", "No me consta."),
        ("dialogue_completion", "Complete: Si entendí bien, me ___ por qué.", "pregunta"),
        ("matching", "Match «quedar abierto» to its meaning.", "to still be undecided"),
        ("reading_comprehension", "What remains pending?", "the calendar"),
        ("inference", "«Donde usted ve un coste, yo veo una inversión» — what is being disputed?", "the frame, not the person"),
        ("main_idea", "«Ajuste de plantilla»: traducido, cuarenta despidos. What is the speaker doing?", "undoing a euphemism"),
        ("detail_identification", "When was the information published?", "on the 4th"),
    ],
}

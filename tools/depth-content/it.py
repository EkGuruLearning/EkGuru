# -*- coding: utf-8 -*-
"""PHASE 1 depth for Italian (`it`).

Authored as specs for `tools/author-depth.py` through the helpers in
`tools/depth_kit.py`. Everything here is language-specific content: six CEFR
`extra` blocks, the eighteen third lessons that lift every A1-C2 unit to the
schema minimum of three lessons, and the five half-step rungs A1+ .. C1+.

House style follows the shipped Italian course: standard Italian with the
course's own romanisation (stressed syllable in CAPITALS, syllables
hyphenated), speakers Marco and Sofia for A1-B2, role names higher up, and the
course's unit ids (`A1-U1` for the CEFR rungs, `it-c1-u1` for C1/C2).
Half-step rungs use `<rung>-U1`, e.g. `A1+-U1`, so a lesson id stays unique
across the sixteen files.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # tools/ on the path
from depth_kit import D, EXTRA, G, L, T, V, WS, X   # noqa: E402

CODE = "it"
NAME = "Italian"
NATIVE = "Italiano"
PHASE = 1
SCRIPT = "Latin with Italian diacritics (à è é ì ò ù « »)"
VOICE = "it-IT"
SKILL = ("Italian: grammatical gender and agreement, the passato prossimo/imperfetto split, "
         "the polite Lei beside the familiar tu, and the doubled consonants that decide meaning")

EXTRAS = {}
THIRD = {}
HALFSTEPS = {}


EXTRAS["A1"] = EXTRA(
    culture=("Ciao is for friends and family; with a stranger, a shopkeeper or anyone older, "
             "Italian opens with buongiorno and closes with arrivederci. The tu/Lei decision is "
             "made in the first sentence — tu for people you would call by first name, Lei for "
             "everyone else, including anyone whose surname you know."),
    source_url="https://en.wikipedia.org/wiki/Italian_language",
    reading=("Sofia arriva al bar la mattina. « Buongiorno, un caffè, per favore. » Il barista "
             "risponde: « Buongiorno! Desidera altro? » Lei prende un cornetto e chiede l'ora. "
             "« Sono le otto e un quarto. » Dice grazie e arrivederci, poi va al lavoro a piedi, "
             "perché l'ufficio è qui vicino."),
    reading_gloss=("Sofia arrives at the bar in the morning. 'Good morning, a coffee, please.' "
                   "The barista answers: 'Good morning! Would you like anything else?' She takes "
                   "a croissant and asks the time. 'It is a quarter past eight.' She says thank "
                   "you and goodbye, then walks to work, because the office is nearby."),
    listening=("Sofia: Buongiorno, come sta?<br>Marco: Bene, grazie. E Lei?<br>"
               "Sofia: Bene. Come si chiama, scusi?<br>Marco: Marco. Piacere!"),
    listening_gloss=("Sofia: Good morning, how are you? Marco: Fine, thanks. And you? Sofia: "
                     "Fine. What is your name, excuse me? Marco: Marco. Pleased to meet you!"),
    voice_tag=VOICE,
    idioms=[
        ("Ciao", "hi/bye (familiar)", "hi, bye — friends only"),
        ("Buongiorno", "good day", "good morning (polite default)"),
        ("Per favore", "for favour", "please"),
        ("Grazie mille", "a thousand thanks", "thanks a lot"),
        ("Prego", "I beg", "you're welcome / go ahead"),
        ("Come va?", "how does it go?", "how's it going?"),
        ("Piacere", "pleasure", "pleased to meet you"),
        ("Scusi", "excuse (you, polite)", "excuse me (polite)"),
        ("Arrivederci", "until we see each other again", "goodbye (polite)"),
        ("A presto", "to soon", "see you soon"),
    ],
    mistakes=[
        ("Ciao, come sta?", "Buongiorno, come sta? / Ciao, come stai?", "Ciao and the polite Lei form cannot share a sentence."),
        ("Grazie Lei.", "Grazie.", "Grazie takes no object; to insist, say grazie mille."),
        ("Mi chiamo sono Sofia.", "Mi chiamo Sofia. / Sono Sofia.", "One introduction; choose one."),
    ],
    task_title="Meet someone twice",
    task_instructions=("Write the same introduction twice: once at a party to someone your age (tu, "
                       "first name) and once at a doctor's reception (Lei, surname). Keep both to "
                       "four lines and read them aloud — the politeness lives in the pronoun and "
                       "the verb ending, not in the adjectives."),
)

EXTRAS["A2"] = EXTRA(
    culture=("Italian meals keep a timetable: colazione standing at the bar, pranzo at one, "
             "aperitivo around seven and cena at nine. The bar is cheaper standing than seated, "
             "« un caffè » is an espresso, and the receipt (lo scontrino) is asked for on the way "
             "out, not on the way in."),
    source_url="https://en.wikipedia.org/wiki/Italian_cuisine",
    reading=("Al ristorante, il cameriere porta il menù. Sofia prende un primo e un secondo, "
             "Marco solo un primo e un dolce. « Da bere? — Una bottiglia d'acqua, per favore. » Il "
             "coperto è a pagamento, il pane no. Alla fine Marco chiede il conto, divide e lascia "
             "un piccolo resto, perché il servizio è incluso."),
    reading_gloss=("At the restaurant the waiter brings the menu. Sofia takes a first course and a "
                   "main, Marco only a first course and a dessert. 'To drink? — A bottle of water, "
                   "please.' The cover charge is paid, the bread is not. In the end Marco asks for "
                   "the bill, splits it and leaves a small remainder, because service is included."),
    listening=("Marco: Che cosa prendi?<br>Sofia: Vorrei il menù del giorno.<br>"
               "Marco: E da bere?<br>Sofia: Una bottiglia d'acqua. Il coperto è incluso?"),
    listening_gloss=("Marco: What are you having? Sofia: I would like the menu of the day. Marco: "
                     "And to drink? Sofia: A bottle of water. Is the cover charge included?"),
    voice_tag=VOICE,
    idioms=[
        ("Vorrei", "I would want", "I would like (polite ordering)"),
        ("Il menù del giorno", "the menu of the day", "the set menu"),
        ("Il conto", "the account", "the bill"),
        ("Lo scontrino", "the receipt", "the receipt, asked for"),
        ("Il resto", "the remainder", "the change, or a small tip"),
        ("Il coperto", "the cover", "cover charge"),
        ("Da bere", "to drink", "drinks"),
        ("Quanto viene?", "how much does it come to?", "how much is it in total?"),
        ("Da portare via", "to carry away", "takeaway"),
        ("Buon appetito", "good appetite", "enjoy your meal"),
    ],
    mistakes=[
        ("Voglio un caffè.", "Vorrei un caffè.", "Voglio is blunt; vorrei is the standard polite order."),
        ("Il menù è a pagamento.", "Il coperto è a pagamento.", "menu in Italian is the list of dishes; the charge is the coperto."),
        ("Prendo il conto.", "Chiedo il conto.", "You ask for the bill: chiedere il conto."),
    ],
    task_title="Order a two-course meal out loud",
    task_instructions=("Write a nine-line restaurant scene: greet, ask for the menù, order a primo "
                       "and a secondo with vorrei, order drinks, ask what the coperto is, ask for "
                       "the bill, ask whether service is included, and leave. Then rewrite the same "
                       "scene as you would say it to a friend at home (tu, prendo) and compare the "
                       "two registers."),
)

EXTRAS["B1"] = EXTRA(
    culture=("The Italian working day runs late and breaks long: offices open around nine, pranzo "
             "takes a real hour, and August empties the cities. The vocabulary of work is therefore "
             "as much about time as about tasks — la pausa pranzo, gli orari, le ferie — and asking "
             "a colleague for help starts with the clock, not the request."),
    source_url="https://en.wikipedia.org/wiki/Working_time",
    reading=("In ufficio la giornata comincia con un caffè e la domanda sugli orari. Sofia lavora "
             "dalle nove alle diciotto, con una vera pausa pranzo. Ha tre settimane di ferie ad "
             "agosto. Marco, invece, il venerdì lavora da casa: finisce prima e risponde alle "
             "email la sera, cosa che non piace a tutti."),
    reading_gloss=("At the office the day starts with a coffee and the question of hours. Sofia "
                   "works from nine to six, with a real lunch break. She has three weeks of holiday "
                   "in August. Marco, on the other hand, works from home on Fridays: he finishes "
                   "earlier and answers emails in the evening, which does not please everyone."),
    listening=("Sofia: Mi dai una mano con la pratica?<br>Marco: Sì, ma non prima delle due.<br>"
               "Sofia: Dopo la pausa pranzo, allora.<br>Marco: Perfetto. Ti rispondo nel pomeriggio."),
    listening_gloss=("Sofia: Can you give me a hand with the file? Marco: Yes, but not before two. "
                     "Sofia: After the lunch break, then. Marco: Perfect. I'll answer you in the "
                     "afternoon."),
    voice_tag=VOICE,
    idioms=[
        ("La pausa pranzo", "the lunch break", "the lunch break"),
        ("Gli orari", "the hours", "the working hours"),
        ("Le ferie", "the holidays", "annual leave"),
        ("Lavorare da casa", "to work from home", "to work from home"),
        ("La pratica", "the file", "the case, the paperwork"),
        ("Va bene", "it goes well", "OK, all right"),
        ("Me ne occupo io", "I occupy myself of it", "I'll take care of it"),
        ("Dare una mano", "to give a hand", "to lend a hand"),
        ("In ritardo", "in delay", "late"),
        ("Fare gli straordinari", "to do the extra-ordinary hours", "to work overtime"),
    ],
    mistakes=[
        ("Lavoro qui da tre anni (in speech).", "Sono tre anni che lavoro qui.", "Spoken Italian prefers the sono … che frame for duration up to now."),
        ("Sono d'accordo con te, ma non sono d'accordo sul budget.", "Sono d'accordo con te, ma non sul budget.", "Do not repeat the verb when the subject has not changed."),
        ("Prendo le ferie in agosto da dieci anni.", "Sono dieci anni che prendo le ferie in agosto.", "Duration up to now: sono + time + che."),
    ],
    task_title="Plan a week of work in Italian",
    task_instructions=("Write seven Italian lines that plan your week the way a colleague would "
                       "hear it: the hours you work, one day of ferie, one day working from home, "
                       "one request for a hand with a file and its reply, and one thing you will "
                       "take care of yourself. Then say the same plan to a friend in tu form and "
                       "note which words change."),
)

EXTRAS["B2"] = EXTRA(
    culture=("Italian argument likes the counter-move: a claim is granted with «è vero che», then "
             "turned with «però», «d'altra parte» or «tuttavia». A debate can sound heated and end "
             "with a coffee, because conceding the true part first is what makes the objection "
             "listenable."),
    source_url="https://en.wikipedia.org/wiki/Italian_culture",
    reading=("«È vero che la misura ha ridotto i costi», dice la sindacalista. «Tuttavia ha "
             "aumentato il carico di lavoro, e nessuno ha misurato questo effetto.» Il direttore "
             "risponde che i dati sono provvisori. D'altra parte accetta una valutazione "
             "indipendente a settembre: due posizioni, un accordo parziale e una data per "
             "verificare."),
    reading_gloss=("'It is true that the measure reduced costs,' says the union representative. "
                   "'However, it increased the workload, and nobody has measured that effect.' The "
                   "director replies that the figures are provisional. On the other hand he accepts "
                   "an independent evaluation in September: two positions, a partial agreement and "
                   "a date to check it."),
    listening=("Marco: È vero che costa molto.<br>Sofia: Tuttavia non possiamo aspettare un altro anno.<br>"
               "Marco: D'accordo sul principio. Però serve un calendario.<br>"
               "Sofia: Un controllo al mese, ti va?"),
    listening_gloss=("Marco: It is true that it costs a lot. Sofia: However, we cannot wait "
                     "another year. Marco: Agreed in principle. But we need a timetable. Sofia: One "
                     "check a month, does that suit you?"),
    voice_tag=VOICE,
    idioms=[
        ("Tuttavia", "however", "however, nevertheless"),
        ("D'altra parte", "on the other hand", "on the other hand"),
        ("È vero che", "it is true that", "granted that"),
        ("D'accordo sul principio", "agreed on the principle", "agreed in principle"),
        ("Mettere i puntini sulle i", "to put the little dots on the i's", "to spell things out"),
        ("Un punto d'accordo", "a point of agreement", "a point of agreement"),
        ("Trovare un'intesa", "to find an understanding", "to come to an agreement"),
        ("Prendere le distanze", "to take distances", "to distance oneself"),
        ("A settembre", "in September", "in September, when work resumes"),
        ("Mettere in discussione", "to put in discussion", "to call into question"),
    ],
    mistakes=[
        ("Tuttavia però serve un calendario.", "Tuttavia serve un calendario.", "One contrast marker per sentence."),
        ("Non sono d'accordo per niente ma ti rispetto.", "Non sono d'accordo, anche se rispetto la tua posizione.", "State the limit of the disagreement; empty courtesy sounds dismissive."),
        ("È vero che costa molto, quindi lasciamo perdere.", "È vero che costa molto; d'altra parte, aspettare costa di più.", "Concede to keep the argument, not to abandon it."),
    ],
    task_title="Disagree in writing, twice",
    task_instructions=("Write a six-line Italian note about a decision you find partly wrong: "
                       "concede with è vero che …, turn with tuttavia / d'altra parte, offer a "
                       "counter-measure, and close with one point of agreement and a date. Then "
                       "rewrite the same note with every concession removed and compare which "
                       "version a real reader would act on."),
)

EXTRAS["C1"] = EXTRA(
    culture=("Bureaucratic Italian loves the noun: «la messa in atto della riforma» hides an actor, "
             "a verb and a responsibility. C1 work is learning to un-nominalise — to read "
             "«procedere all'aggiornamento» and hear «aggiornare» — and to write in a register that "
             "stays impersonal without disappearing entirely."),
    source_url="https://en.wikipedia.org/wiki/Italian_grammar",
    reading=("La relazione indica che «la messa in atto del dispositivo sarà oggetto di "
             "valutazione». Tradotto in italiano corrente: qualcuno dovrà verificare se la misura "
             "funziona, e la relazione non dice chi. È esattamente questa vaghezza che la nota di "
             "sintesi attacca: per ogni frase passiva si scrivono il verbo, il soggetto e la data."),
    reading_gloss=("The report states that 'the implementation of the scheme will be the subject of "
                   "an evaluation'. Translated into ordinary Italian: somebody will have to check "
                   "whether the measure works, and the report does not say who. It is exactly that "
                   "vagueness that the summary note attacks: for every passive sentence, write the "
                   "verb, the subject and the date."),
    listening=("Analyst: Sarebbe opportuno procedere a una verifica.<br>Reviewer: Concretamente?<br>"
               "Analyst: Concretamente: due persone, quindici giorni, una nota di tre pagine.<br>"
               "Reviewer: Questo è più chiaro."),
    listening_gloss=("Analyst: It would be appropriate to proceed to a check. Reviewer: "
                     "Concretely? Analyst: Concretely: two people, fifteen days, a three-page note. "
                     "Reviewer: That is clearer."),
    voice_tag=VOICE,
    idioms=[
        ("La messa in atto", "the putting into act", "implementation"),
        ("Essere oggetto di", "to be the object of", "to be subject to"),
        ("Procedere a", "to proceed to", "to carry out"),
        ("Sarebbe opportuno", "it would be opportune", "it would be advisable"),
        ("Allo stato attuale", "in the current state", "as things stand"),
        ("A titolo di", "by way of", "as, by way of"),
        ("Salvo conguaglio", "save adjustment", "subject to adjustment"),
        ("Ove necessario", "where necessary", "if applicable"),
        ("Ai fini di", "to the ends of", "for the purposes of"),
        ("Ne prendiamo atto", "we take act of it", "noted accordingly"),
    ],
    mistakes=[
        ("Si è proceduto da parte degli uffici a una verifica (subject hidden).", "Gli uffici hanno verificato i conti.", "Un-nominalise: name the actor and the verb."),
        ("Sarebbe opportuno procedere a una verifica rapida ed efficace e utile.", "Sarebbe opportuno verificare il dispositivo entro quindici giorni.", "One adjective per claim; the date does the work."),
        ("Essere oggetto di una valutazione da parte di chiunque.", "Essere oggetto di una valutazione indipendente.", "Replace the vague agent with a named one."),
    ],
    task_title="Un-nominalise one administrative paragraph",
    task_instructions=("Take a real Italian administrative sentence you have received — a letter, a "
                       "notice, a form — and rewrite it three times: as it was written, in plain "
                       "Italian with a subject and a verb, and as a three-line memo that names who "
                       "does what by when. List every noun phrase you had to unpack; that list is "
                       "your C1 vocabulary."),
)

EXTRAS["C2"] = EXTRA(
    culture=("Italian literary argument plays with understatement and borrowed register: a legal "
             "phrase dropped into an essay, a slogan quoted to be mocked, a litote («non è poco») "
             "that says more by saying less. Reading at C2 means hearing the borrowed voice and "
             "knowing who is being quoted, and mocked."),
    source_url="https://en.wikipedia.org/wiki/Italian_literature",
    reading=("«Non era inconsapevole che la cosa fosse delicata»: tre negazioni per una sola "
             "informazione, e l'informazione resta sul bordo della frase. Il commento che segue "
             "cita un comunicato — «un esito favorevole è ipotizzabile» — e lo lascia lì, senza "
             "virgolette aggiunte, perché il lettore senta il vuoto."),
    reading_gloss=("'He was not unaware that the matter was delicate': three negations for one "
                   "piece of information, and the information itself stays at the edge of the "
                   "sentence. The commentary that follows quotes a press release — 'a favourable "
                   "outcome is conceivable' — and leaves it there, with no added quotation marks, "
                   "so that the reader hears the emptiness."),
    listening=("Editor: Il suo testo cita il comunicato senza commentarlo.<br>Author: Lo lascio parlare.<br>"
               "Editor: E il lettore sente?<br>Author: Sente la litote, se vuole."),
    listening_gloss=("Editor: Your text quotes the press release without commenting on it. Author: "
                     "I let it speak. Editor: And the reader hears? Author: They hear the "
                     "understatement, if they care to."),
    voice_tag=VOICE,
    idioms=[
        ("La litote", "the litotes", "understatement"),
        ("Non essere inconsapevole", "not to be unaware", "to be well aware"),
        ("A mezza voce", "at half voice", "without spelling it out"),
        ("Sottintendere", "to under-intend", "to imply"),
        ("Il non detto", "the unsaid", "what is left unsaid"),
        ("Mettere tra virgolette", "to put between little commas", "to quote, to hedge"),
        ("Il tono impassibile", "the impassive tone", "deadpan"),
        ("Fare centro", "to hit the centre", "to hit the mark"),
        ("Senza toccarla", "without touching it", "without appearing to try"),
        ("Un ammicco", "a wink", "a nod, a knowing allusion"),
    ],
    mistakes=[
        ("Non è poco, cioè è moltissimo.", "Non è poco.", "A litote explains itself into nothing; leave it standing."),
        ("Ha detto: « » tra virgolette, ironicamente.", "Ha detto «un esito favorevole è ipotizzabile» — e si è taciuto.", "Show the irony by silence, not by labelling it."),
        ("L'autore è ironico qui (tre volte nel paragrafo).", "L'autore cita il comunicato senza commento.", "Describe the device once; the reader will hear the rest."),
    ],
    task_title="Write a litote and dismantle one",
    task_instructions=("Write a six-line Italian paragraph in which a plan is described only by what "
                       "it is not («non è poco», «non è escluso che»), then rewrite the same "
                       "paragraph in flat official Italian and in one blunt line. Finally, take a "
                       "real Italian slogan or press release and write the sentence that names what "
                       "it leaves unsaid without using the word ironia."),
)


THIRD["A1"] = [
    ("A1-U1", "A1-U1-L3", L(
        "Tu o Lei: scegliere alla prima frase",
        "Italian decides before it says anything else: tu for friends and family, Lei for "
        "strangers, shops and anyone older. Buongiorno opens both doors; the pronoun picks the "
        "room.",
        [V("Lei", "lay", "you (polite)", "pronoun"),
         V("tu", "too", "you (familiar)", "pronoun"),
         V("signora", "see-NYOH-rah", "madam", "noun"),
         V("signore", "see-NYOH-reh", "sir", "noun"),
         V("scusi", "SKOO-zee", "excuse me (polite)", "verb")],
        G("The two yous",
          "tu + 2nd person singular · Lei + 3rd person singular · scusi (Lei) / scusa (tu)",
          "Buongiorno signora, come sta? Buongiorno Marco, come stai? Lei takes the verb of lui — "
          "sta, not stai — which is the whole trick of polite Italian.",
          [X("Buongiorno signora, come sta?", "bwohn-JOR-noh see-NYOH-rah, KOH-meh stah?", "Good morning madam, how are you?"),
           X("Ciao Marco, come stai?", "CHOW MAR-koh, KOH-meh STAHY?", "Hi Marco, how are you?"),
           X("Scusi, Lei è il professore?", "SKOO-zee, lay eh eel proh-fes-SOH-reh?", "Excuse me, are you the teacher?")],
          [("Buongiorno signora, come stai?", "Buongiorno signora, come sta?", "Lei takes the third-person verb form: sta."),
           ("Scusa, Lei è il professore?", "Scusi, Lei è il professore?", "With Lei the excuse is scusi, not scusa.")]),
        [D("Sofia", "Buongiorno, scusi, Lei è il professor Bianchi?", "bwohn-JOR-noh, SKOO-zee, lay eh eel proh-fes-SOR BYAHN-kee?", "Good morning, excuse me, are you Professor Bianchi?"),
         D("Prof. Bianchi", "Sì, sono io. E Lei?", "see, SOH-noh ee-oh. eh lay?", "Yes, that's me. And you?"),
         D("Sofia", "Mi chiamo Sofia. Sono nuova.", "mee KYAH-moh SOH-fyah. SOH-noh NWOH-vah.", "My name is Sofia. I'm new."),
         D("Prof. Bianchi", "Benvenuta. Cominciamo alle nove.", "ben-veh-NOO-tah. koh-mnch-YAH-moh AHL-leh NOH-veh.", "Welcome. We start at nine.")],
        WS("Tu/Lei worksheet", [
            T("Choose the pronoun.", ["to your friend Marco", "to a shopkeeper", "to your little sister"],
              ["tu", "Lei", "tu"]),
            T("Say it politely.", ["Good morning madam, how are you?", "Excuse me, are you the teacher?", "Shall we go?"],
              ["Buongiorno signora, come sta?", "Scusi, Lei è il professore?", "Andiamo?"]),
        ]))),
    ("A1-U2", "A1-U2-L3", L(
        "Dove abito: c'è, ci sono",
        "Home is described with C'È (there is) and CI SONO (there are) plus a room list: un "
        "appartamento, una camera, la cucina, il soggiorno.",
        [V("c'è", "cheh", "there is", "phrase"),
         V("ci sono", "chee SOH-noh", "there are", "phrase"),
         V("la camera", "lah KAH-meh-rah", "bedroom", "noun"),
         V("la cucina", "lah koo-CHEE-nah", "kitchen", "noun"),
         V("abitare", "ah-bee-TAH-reh", "to live", "verb")],
        G("There is / there are",
          "c'è + singular · ci sono + plural · abito + place",
          "C'è una cucina e ci sono due camere. In camera non c'è il balcone. The negative swaps "
          "the article for nothing: non c'è balcone.",
          [X("C'è una cucina grande.", "cheh OO-nah koo-CHEE-nah GRAHN-deh.", "There is a big kitchen."),
           X("Ci sono due camere.", "chee SOH-noh DOO-eh KAH-meh-reh.", "There are two bedrooms."),
           X("Non c'è il balcone.", "nohn cheh eel bahl-KOH-neh.", "There is no balcony.")],
          [("È una cucina grande.", "C'è una cucina grande.", "Existence takes c'è, not è."),
           ("Ci sono una camera.", "C'è una camera.", "One room takes c'è; ci sono is plural.")]),
        [D("Marco", "Dove abiti?", "DOH-veh AH-bee-tee?", "Where do you live?"),
         D("Sofia", "Vicino al centro, in un appartamento piccolo.", "vee-CHEE-noh ahl CHEN-troh, een oon ah-pahr-tah-MEN-toh PEEK-koh-loh.", "Near the centre, in a small flat."),
         D("Marco", "Quante stanze ci sono?", "KWAHN-teh STAHN-tseh chee SOH-noh?", "How many rooms are there?"),
         D("Sofia", "Due camere, una cucina e un soggiorno. Niente balcone, purtroppo.", "DOO-eh KAH-meh-reh, OO-nah koo-CHEE-nah eh oon sohj-JOR-noh. NYEN-teh bahl-KOH-neh, poor-TROHP-poh.", "Two bedrooms, a kitchen and a living room. No balcony, unfortunately.")],
        WS("Home worksheet", [
            T("Say what there is.", ["two bedrooms", "a small kitchen", "no balcony"],
              ["Ci sono due camere.", "C'è una cucina piccola.", "Non c'è il balcone."]),
            T("Place your home.", ["near the centre", "where do you live?"],
              ["Abito vicino al centro.", "Dove abiti?"]),
        ]))),
    ("A1-U3", "A1-U3-L3", L(
        "Il tempo e le stagioni",
        "Weather is impersonal and short: FA BEL TEMPO, PIOVE, FA FREDDO. Seasons take IN for the "
        "ones you live through: in estate, in inverno.",
        [V("fa bel tempo", "fah bel TEM-poh", "the weather is nice", "phrase"),
         V("piove", "PYOH-veh", "it is raining", "phrase"),
         V("fa freddo", "fah FRED-doh", "it is cold", "phrase"),
         V("l'estate", "les-TAH-teh", "summer", "noun"),
         V("l'inverno", "leen-VEHR-noh", "winter", "noun")],
        G("Weather frame",
          "fa + adjective · piove / nevica · in estate / in inverno",
          "In estate fa bel tempo e la gente esce. In inverno fa freddo e a volte nevica. Notice "
          "that weather uses fare: fa caldo, fa freddo, fa bel tempo.",
          [X("In estate fa bel tempo.", "een es-TAH-teh fah bel TEM-poh.", "In summer the weather is nice."),
           X("In autunno piove spesso.", "een ow-TOON-noh PYOH-veh SPES-soh.", "In autumn it often rains."),
           X("In inverno fa freddo e nevica.", "een een-VEHR-noh fah FRED-doh eh NEH-vee-kah.", "In winter it is cold and it snows.")],
          [("È freddo oggi.", "Fa freddo oggi.", "Weather uses fare: fa freddo."),
           ("A estate piove.", "In estate piove.", "Seasons take in.")]),
        [D("Sofia", "Che tempo fa a Roma?", "keh TEM-poh fah ah ROH-mah?", "What is the weather like in Rome?"),
         D("Marco", "Piove e fa freddo. È inverno, che vuoi.", "PYOH-veh eh fah FRED-doh. eh een-VEHR-noh, keh VWOH-ee.", "It is raining and cold. It's winter, what do you expect."),
         D("Sofia", "E in estate?", "eh een es-TAH-teh?", "And in summer?"),
         D("Marco", "Fa bel tempo e tutti escono. È la stagione migliore.", "fah bel TEM-poh eh TOOT-tee EH-sko-noh. eh lah stah-JOH-neh mee-LYOH-reh.", "The weather is nice and everyone goes out. It's the best season.")],
        WS("Weather worksheet", [
            T("Describe the weather.", ["it is nice (summer)", "it is raining (autumn)", "it is cold (winter)"],
              ["In estate fa bel tempo.", "In autunno piove.", "In inverno fa freddo."]),
            T("Answer the question.", ["What is the weather like today?", "Do you like summer?"],
              ["Che tempo fa oggi?", "Ti piace l'estate?"]),
        ]))),
]

THIRD["A2"] = [
    ("A2-U1", "A2-U1-L3", L(
        "In treno: biglietti, binari, ritardi",
        "Station Italian is compact: UN BIGLIETTO PER ROMA, PER FAVORE · DA QUALE BINARIO PARTE? · "
        "IL TRENO È IN RITARDO DI DIECI MINUTI.",
        [V("il biglietto", "eel beel-YET-toh", "ticket", "noun"),
         V("il binario", "eel bee-NAH-ryoh", "platform", "noun"),
         V("il ritardo", "eel ree-TAR-doh", "delay", "noun"),
         V("il cambio", "eel KAHM-byoh", "change (of trains)", "noun"),
         V("la coincidenza", "lah koh-een-chee-DEN-tsah", "connection", "noun")],
        G("Tickets and platforms",
          "un biglietto per + city · da quale binario? · in ritardo di …",
          "Un biglietto per Firenze, per favore. Da quale binario parte? Il treno è in ritardo di "
          "dieci minuti. The destination takes per; the delay takes di.",
          [X("Un biglietto per Firenze, per favore.", "oon beel-YET-toh per fee-REN-tseh, per fah-VOH-reh.", "A ticket to Florence, please."),
           X("Da quale binario parte il treno?", "dah KWAH-leh bee-NAH-ryoh PAR-teh eel TREH-noh?", "Which platform does the train leave from?"),
           X("Il treno è in ritardo di dieci minuti.", "eel TREH-noh eh een ree-TAR-doh dee DYEH-chee mee-NOO-tee.", "The train is ten minutes late.")],
          [("Un biglietto a Firenze.", "Un biglietto per Firenze.", "A destination takes per."),
           ("Il treno è in ritardo dieci minuti.", "Il treno è in ritardo di dieci minuti.", "The delay takes di.")]),
        [D("Marco", "Un biglietto per Firenze, per favore.", "oon beel-YET-toh per fee-REN-tseh, per fah-VOH-reh.", "A ticket to Florence, please."),
         D("Bigliettaia", "Andata e ritorno?", "ahn-DAH-tah eh ree-TOR-noh?", "Return?"),
         D("Marco", "Solo andata. Da quale binario parte?", "SOH-loh ahn-DAH-tah. dah KWAH-leh bee-NAH-ryoh PAR-teh?", "One way. Which platform does it leave from?"),
         D("Bigliettaia", "Binario quattro, ma è in ritardo di dieci minuti.", "bee-NAH-ryoh KWAH-troh, mah eh een ree-TAR-doh dee DYEH-chee mee-NOO-tee.", "Platform four, but it is ten minutes late.")],
        WS("Train worksheet", [
            T("Buy the ticket.", ["a return to Florence", "a single to Milan", "departure at ten"],
              ["Un andata e ritorno per Firenze.", "Un solo andata per Milano.", "Partenza alle dieci."]),
            T("Ask at the station.", ["which platform?", "is there a change?", "is it late?"],
              ["Da quale binario?", "C'è un cambio?", "È in ritardo?"]),
        ]))),
    ("A2-U2", "A2-U2-L3", L(
        "Dal medico: mi fa male, dovresti",
        "Pain uses FARE MALE: mi fa male la gola, mi fanno male i piedi. Advice uses the "
        "conditional: DOVRESTI riposare.",
        [V("mi fa male", "mee fah MAH-leh", "it hurts me", "phrase"),
         V("la gola", "lah GOH-lah", "throat", "noun"),
         V("riposare", "ree-poh-ZAH-reh", "to rest", "verb"),
         V("la ricetta", "lah ree-CHET-tah", "prescription", "noun"),
         V("dovresti", "doh-VRES-tee", "you should", "phrase")],
        G("Pain and advice",
          "mi fa male + singular · mi fanno male + plural · dovresti + infinitive",
          "Mi fa male la gola e mi fanno male le gambe. Dovresti bere molto e riposare. The body "
          "part is the subject: it agrees with fa / fanno.",
          [X("Mi fa male la gola.", "mee fah MAH-leh lah GOH-lah.", "I have a sore throat."),
           X("Mi fanno male i piedi.", "mee FAHN-noh MAH-leh ee PYEH-dee.", "My feet hurt."),
           X("Dovresti riposare due giorni.", "doh-VRES-tee ree-poh-ZAH-reh DOO-eh JOR-nee.", "You should rest for two days.")],
          [("Mi fa male i piedi.", "Mi fanno male i piedi.", "Plural body parts take fanno."),
           ("Devi riposare (advice to a friend).", "Dovresti riposare.", "devi orders; the conditional advises.")]),
        [D("Sofia", "Buongiorno dottore, mi fa male la gola.", "bwohn-JOR-noh dot-TOH-reh, mee fah MAH-leh lah GOH-lah.", "Good morning doctor, I have a sore throat."),
         D("Medico", "Da quando?", "dah KWAHN-doh?", "Since when?"),
         D("Sofia", "Da tre giorni, e mi fa male anche la testa.", "dah treh JOR-nee, eh mee fah MAH-leh AHN-keh lah TES-tah.", "For three days, and my head hurts too."),
         D("Medico", "Dovresti riposare e bere molta acqua.", "doh-VRES-tee ree-poh-ZAH-reh eh BEH-reh MOHL-tah AHK-kwah.", "You should rest and drink a lot of water.")],
        WS("Doctor worksheet", [
            T("Say where it hurts.", ["sore throat", "my head hurts", "my feet hurt"],
              ["Mi fa male la gola.", "Mi fa male la testa.", "Mi fanno male i piedi."]),
            T("Give advice.", ["you should rest", "you should drink water"],
              ["Dovresti riposare.", "Dovresti bere acqua."]),
        ]))),
    ("A2-U3", "A2-U3-L3", L(
        "I vestiti: taglia, colore, cambio",
        "Clothes shopping turns on four words: LA TAGLIA (size), IL COLORE, PROVARE (to try on) and "
        "CAMBIARE. «Mi sta bene» judges the fit.",
        [V("la taglia", "lah TAH-lyah", "size", "noun"),
         V("provare", "proh-VAH-reh", "to try on", "verb"),
         V("cambiare", "kahm-BYAH-reh", "to exchange", "verb"),
         V("la cassa", "lah KAHS-sah", "checkout", "noun"),
         V("mi sta bene", "mee stah BEH-neh", "it fits me well", "phrase")],
        G("Shopping frame",
          "posso provare? · mi sta bene / non mi sta bene · vorrei cambiarlo con …",
          "Posso provare questa camicia? È troppo piccola: vorrei cambiarla con una taglia in più. "
          "The fit takes stare: mi sta bene, ti sta bene.",
          [X("Posso provare questa camicia?", "POHS-soh proh-VAH-reh KWES-tah kah-MEE-chah?", "Can I try this shirt on?"),
           X("È troppo piccola.", "eh TROHP-poh PEEK-koh-lah.", "It is too small."),
           X("Vorrei cambiarla con una taglia in più.", "vor-RAY kahm-BYAR-lah kon OO-nah TAH-lyah een pyoo.", "I would like to exchange it for one size bigger.")],
          [("Posso provare di questa camicia?", "Posso provare questa camicia?", "provare takes a direct object; no di."),
           ("Mi sta bene i pantaloni (plural).", "Mi stanno bene i pantaloni.", "Plural clothes take stanno.")]),
        [D("Sofia", "Buongiorno, posso provare questo vestito?", "bwohn-JOR-noh, POHS-soh proh-VAH-reh KWES-toh ves-TEE-toh?", "Good morning, can I try this dress on?"),
         D("Commessa", "Certo, il camerino è in fondo.", "CHER-toh, eel kah-meh-REE-noh eh een FOHN-doh.", "Of course, the fitting room is at the back."),
         D("Sofia", "È troppo piccolo. Avete una taglia in più?", "eh TROHP-poh PEEK-koh-loh. ah-VEH-teh OO-nah TAH-lyah een pyoo?", "It is too small. Do you have one size bigger?"),
         D("Commessa", "Sì, in blu. Le sta molto bene.", "see, een bloo. leh stah MOHL-toh BEH-neh.", "Yes, in blue. It suits you very well.")],
        WS("Clothes worksheet", [
            T("Shop in Italian.", ["can I try it on?", "it is too small", "one size bigger"],
              ["Posso provarlo?", "È troppo piccolo.", "una taglia in più"]),
            T("Finish the purchase.", ["I'll take it", "where is the checkout?"],
              ["Lo prendo.", "Dov'è la cassa?"]),
        ]))),
]

THIRD["B1"] = [
    ("B1-U1", "B1-U1-L3", L(
        "Raccontare un aneddoto: prima, poi, alla fine",
        "A story in Italian is signposted: PRIMA … , POI … , ALL'IMPROVVISO … , ALLA FINE … The "
        "frame keeps the tense honest — passato prossimo for the events, imperfetto for the scene "
        "behind them.",
        [V("prima", "PREE-mah", "first", "adverb"),
         V("poi", "pohy", "then", "adverb"),
         V("all'improvviso", "ahl-leem-proh-VEE-zoh", "suddenly", "adverb"),
         V("alla fine", "AHL-lah FEE-neh", "in the end", "phrase"),
         V("raccontare", "rahk-kohn-TAH-reh", "to tell", "verb")],
        G("Story signposts",
          "prima … · poi … · all'improvviso … · alla fine …",
          "Prima sono arrivato alla stazione. Poi, all'improvviso, il treno si è fermato. Alla "
          "fine sono tornato a casa a piedi. Signposts carry the listener; the tenses carry the "
          "time.",
          [X("Prima sono arrivato alla stazione.", "PREE-mah SOH-noh ahr-ree-VAH-toh AHL-lah stah-TSYOH-neh.", "First I arrived at the station."),
           X("All'improvviso il treno si è fermato.", "ahl-leem-proh-VEE-zoh eel TREH-noh see eh fer-MAH-toh.", "Suddenly the train stopped."),
           X("Alla fine sono tornato a piedi.", "AHL-lah FEE-neh SOH-noh tor-NAH-toh ah PYEH-dee.", "In the end I walked home.")],
          [("Alla fine, poi, prima, ripetizione.", "Alla fine sono tornato a piedi.", "One signpost per move."),
           ("Ero arrivato alla stazione alle otto.", "Sono arrivato alla stazione alle otto.", "A single finished arrival takes the passato prossimo.")]),
        [D("Marco", "Raccontami la giornata.", "rahk-KOHN-tah-mee lah jor-NAH-tah.", "Tell me about your day."),
         D("Sofia", "Prima il treno aveva un'ora di ritardo.", "PREE-mah eel TREH-noh ah-VEH-vah oo-NOH-rah dee ree-TAR-doh.", "First the train was an hour late."),
         D("Marco", "E poi?", "eh pohy?", "And then?"),
         D("Sofia", "Poi, all'improvviso, è arrivato: alla fine sono tornata tardi.", "pohy, ahl-leem-proh-VEE-zoh, eh ahr-ree-VAH-toh: AHL-lah FEE-neh SOH-noh tor-NAH-tah TAR-dee.", "Then, all of a sudden, it arrived: in the end I got home late.")],
        WS("Story worksheet", [
            T("Chain the anecdote.", ["first the train was late", "then it arrived suddenly", "finally I got home late"],
              ["Prima il treno era in ritardo.", "Poi, all'improvviso, è arrivato.", "Alla fine sono tornato tardi."]),
            T("Order the moves.", ["first", "then", "finally"],
              ["prima", "poi", "alla fine"]),
        ]))),
    ("B1-U2", "B1-U2-L3", L(
        "Cercare lavoro: curriculum, colloquio, esperienza",
        "Job talk names experience with SONO … CHE + present, and the wish with MI INTERESSA. The "
        "interview frame: MI PARLI DEL SUO PERCORSO.",
        [V("il percorso", "eel per-KOR-soh", "career path", "noun"),
         V("l'esperienza", "les-peh-RYEN-tsah", "experience", "noun"),
         V("il colloquio", "eel kohl-LOH-kwyoh", "interview", "noun"),
         V("il curriculum", "eel koo-REE-koo-loom", "CV, résumé", "noun"),
         V("mi interessa", "mee een-teh-RES-sah", "I am interested", "phrase")],
        G("Experience frame",
          "sono + durata + che + presente · mi interessa + noun · mi occupo di …",
          "Sono tre anni che lavoro nella logistica. Mi occupo delle consegne e mi interessa "
          "questo ruolo. The sono … che frame is the spoken way to state a duration that is still "
          "running.",
          [X("Sono tre anni che lavoro nella logistica.", "SOH-noh treh AHN-nee keh lah-VOH-roh NEHL-lah loh-JEES-tee-kah.", "I have been working in logistics for three years."),
           X("Mi occupo delle consegne.", "mee OH-koo-poh DEL-leh kohn-SEH-nyeh.", "I handle deliveries."),
           X("Mi interessa questo ruolo.", "mee een-teh-RES-sah KWES-toh RWOH-loh.", "I am interested in this role.")],
          [("Lavoro qui da tre anni (in speech).", "Sono tre anni che lavoro qui.", "Spoken Italian prefers the sono … che frame."),
           ("Sono interessato per questo ruolo.", "Mi interessa questo ruolo.", "Italian prefers mi interessa + noun here.")]),
        [D("Selezionatrice", "Mi parli del suo percorso.", "mee PAR-lee del SOO-oh per-KOR-soh.", "Tell me about your career path."),
         D("Sofia", "Sono tre anni che lavoro nella logistica.", "SOH-noh treh AHN-nee keh lah-VOH-roh NEHL-lah loh-JEES-tee-kah.", "I have been working in logistics for three years."),
         D("Selezionatrice", "E perché questo ruolo?", "eh per-KEH KWES-toh RWOH-loh?", "And why this role?"),
         D("Sofia", "Mi occupo già delle consegne e mi interessa l'organizzazione del servizio.", "mee OH-koo-poh jah DEL-leh kohn-SEH-nyeh eh mee een-teh-RES-sah lor-gah-nee-tsah-TSYOH-neh del ser-VEE-tsyoh.", "I already handle deliveries and I am interested in how the department is organised.")],
        WS("Interview worksheet", [
            T("State your experience.", ["three years in logistics", "I handle deliveries"],
              ["Sono tre anni che lavoro nella logistica.", "Mi occupo delle consegne."]),
            T("Answer the questions.", ["why this role?", "what is your goal?"],
              ["Mi interessa questo ruolo.", "Il mio obiettivo è …"]),
        ]))),
    ("B1-U3", "B1-U3-L3", L(
        "Fissare un appuntamento: spostare, annullare",
        "Appointments move with three verbs: SPOSTARE (move), ANNULLARE (cancel), CONFERMARE. "
        "«Ti va bene?» checks the time without imposing it.",
        [V("spostare", "spoh-STAH-reh", "to move (an appointment)", "verb"),
         V("annullare", "ahn-nool-LAH-reh", "to cancel", "verb"),
         V("confermare", "kohn-fer-MAH-reh", "to confirm", "verb"),
         V("l'appuntamento", "lahp-poon-tah-MEN-toh", "appointment", "noun"),
         V("ti va bene", "tee vah BEH-neh", "does it suit you", "phrase")],
        G("Appointment frame",
          "ci vediamo … ? · ti va bene? · devo spostare / annullare l'appuntamento",
          "Ci vediamo martedì alle dieci? Ti va bene? Altrimenti devo spostare l'appuntamento a "
          "giovedì. The question at the end leaves the other person a way out.",
          [X("Ci vediamo martedì alle dieci?", "chee veh-DYAH-moh mar-teh-DEE AHL-leh DYEH-chee?", "Shall we meet Tuesday at ten?"),
           X("Ti va bene?", "tee vah BEH-neh?", "Does that suit you?"),
           X("Devo spostare l'appuntamento a giovedì.", "DEH-voh spoh-STAH-reh lahp-poon-tah-MEN-toh ah JOH-veh-dee.", "I have to move the appointment to Thursday.")],
          [("Devo annullare l'appuntamento a giovedì.", "Devo spostare l'appuntamento a giovedì.", "Annullare cancels; spostare moves."),
           ("Ci vediamo al martedì.", "Ci vediamo martedì.", "Days take no preposition: martedì.")]),
        [D("Marco", "Ci vediamo martedì alle dieci?", "chee veh-DYAH-moh mar-teh-DEE AHL-leh DYEH-chee?", "Shall we meet on Tuesday at ten?"),
         D("Sofia", "Martedì non mi va — devo spostare.", "mar-teh-DEE nohn mee vah — DEH-voh spoh-STAH-reh.", "Tuesday doesn't work for me — I have to move it."),
         D("Marco", "Giovedì, allora?", "JOH-veh-dee, ahl-LOH-rah?", "Thursday, then?"),
         D("Sofia", "Giovedì, perfetto. Confermo con un messaggio.", "JOH-veh-dee, per-FET-toh. kohn-FER-moh kon oon mes-SAJ-joh.", "Thursday, perfect. I'll confirm by message.")],
        WS("Appointment worksheet", [
            T("Fix the time.", ["shall we meet Tuesday?", "does that suit you?", "I have to move it to Thursday"],
              ["Ci vediamo martedì?", "Ti va bene?", "Devo spostarlo a giovedì."]),
            T("Close the loop.", ["I'll confirm by message", "I have to cancel"],
              ["Confermo con un messaggio.", "Devo annullare."]),
        ]))),
]

THIRD["B2"] = [
    ("B2-U1", "B2-U1-L3", L(
        "Concedere e ribattere: è vero che…, tuttavia",
        "An Italian rebuttal gives the other side its due first: È VERO CHE … , TUTTAVIA … ; "
        "D'ACCORDO, MA … The concession is what makes the refutation audible.",
        [V("è vero che", "eh VEH-roh keh", "it is true that", "phrase"),
         V("tuttavia", "toot-tah-VEE-ah", "nevertheless", "adverb"),
         V("d'accordo, ma", "dahk-KOR-doh, mah", "agreed, but", "phrase"),
         V("la sfumatura", "lah sfoo-mah-TOO-rah", "nuance", "noun"),
         V("a condizione che", "ah kohn-dee-TSYOH-neh keh", "provided that", "phrase")],
        G("Two-storey concession",
          "è vero che … , tuttavia … · d'accordo, ma … · a condizione che + congiuntivo",
          "È vero che la misura costa; tuttavia evita un rischio più grande. D'accordo, ma il "
          "tempo è poco, a condizione che due persone ci lavorino. One concession, one counter, "
          "one condition.",
          [X("È vero che la misura costa.", "eh VEH-roh keh lah mee-ZOO-rah KOHS-tah.", "It is true that the measure costs."),
           X("Tuttavia evita un rischio più grande.", "toot-tah-VEE-ah EH-vee-tah oon ree-SKEE-oh pyoo GRAHN-deh.", "Nevertheless it avoids a bigger risk."),
           X("A condizione che due persone ci lavorino.", "ah kohn-dee-TSYOH-neh keh DOO-eh per-SOH-neh chee lah-VOH-ree-noh.", "Provided two people work on it.")],
          [("È vero che costa, ma però serve tempo.", "È vero che costa; tuttavia serve tempo.", "One contrast marker; però and tuttavia do not stack."),
           ("A condizione che due persone ci lavorano.", "A condizione che due persone ci lavorino.", "a condizione che takes the congiuntivo.")]),
        [D("Collega", "La riforma costa troppo.", "lah ree-FOR-mah KOHS-tah TROHP-poh.", "The reform costs too much."),
         D("Sofia", "È vero che costa; tuttavia evita un rischio più grande.", "eh VEH-roh keh KOHS-tah; toot-tah-VEE-ah EH-vee-tah oon ree-SKEE-oh pyoo GRAHN-deh.", "It is true that it costs; nevertheless it avoids a bigger risk."),
         D("Collega", "E i tempi?", "eh ee TEM-pee?", "And the timing?"),
         D("Sofia", "Sono sostenibili, a condizione che due persone ci lavorino.", "SOH-noh sohs-teh-NEE-bee-lee, ah kohn-dee-TSYOH-neh keh DOO-eh per-SOH-neh chee lah-VOH-ree-noh.", "They are sustainable, provided two people work on it.")],
        WS("Rebuttal worksheet", [
            T("Concede, then counter.", ["admittedly it costs", "nevertheless it avoids a bigger risk", "provided two people work on it"],
              ["È vero che costa.", "Tuttavia evita un rischio più grande.", "a condizione che due persone ci lavorino"]),
            T("Name the nuance.", ["there is a nuance", "agreed, but the timing is tight"],
              ["C'è una sfumatura.", "D'accordo, ma i tempi sono stretti."]),
        ]))),
    ("B2-U2", "B2-U2-L3", L(
        "L'email formale: oggetto, apertura, formula",
        "A formal Italian email has three shelves: OGGETTO, GENTILE DOTTORE, (no name after the "
        "comma) and a closing formula — CORDIALI SALUTI or LA RINGRAZIO E LE PORGO I MIEI SALUTI.",
        [V("l'oggetto", "loh-JET-toh", "subject", "noun"),
         V("l'allegato", "lahl-leh-GAH-toh", "attachment", "noun"),
         V("la ringrazio", "lah reen-GRAH-tsyoh", "I thank you", "phrase"),
         V("cordiali saluti", "kor-DYAH-lee sah-LOO-tee", "kind regards", "phrase"),
         V("in attesa di", "een aht-TEH-zah dee", "awaiting", "phrase")],
        G("Email frame",
          "Oggetto: … · Gentile Dottore, · Le scrivo per … · In attesa di un Suo riscontro, cordiali saluti",
          "Oggetto: Richiesta di preventivo. Gentile Dottore, Le scrivo per chiedere il "
          "preventivo aggiornato. In allegato trova il capitolato. In attesa di un Suo riscontro, "
          "cordiali saluti. Not one sentence is creative — that is the point.",
          [X("Le scrivo per chiedere il preventivo.", "leh SKREE-voh per kyeh-DEH-reh eel preh-ven-TEE-voh.", "I am writing to ask for the quote."),
           X("In allegato trova il capitolato.", "een ahl-leh-GAH-toh TROH-vah eel kah-pee-toh-LAH-toh.", "Attached you will find the specification."),
           X("In attesa di un Suo riscontro, cordiali saluti.", "een aht-TEH-zah dee oon SOO-oh ree-SKOHN-troh, kor-DYAH-lee sah-LOO-tee.", "Awaiting your reply, kind regards.")],
          [("Ciao Dottoressa Maria,", "Gentile Dottoressa,", "Formal Italian uses the title alone; the first name stays out."),
           ("Cordiali saluti, Sofia.", "In attesa di un Suo riscontro, cordiali saluti.", "The formula closes the request and sits above the signature.")]),
        [D("Marco", "Come comincio l'email?", "KOH-meh koh-MEEN-choh lee-MAYL?", "How do I start the email?"),
         D("Sofia", "«Oggetto: …», poi «Gentile Dottoressa,».", "oh-JET-toh, …, pohy jen-TEE-leh dot-toh-RES-sah,", "'Subject: …', then 'Dear Doctor'."),
         D("Marco", "E per chiudere?", "eh per KYOO-deh-reh?", "And to close?"),
         D("Sofia", "«In attesa di un Suo riscontro, cordiali saluti.»", "een aht-TEH-zah dee oon SOO-oh ree-SKOHN-troh, kor-DYAH-lee sah-LOO-tee.", "'Awaiting your reply, kind regards.'")],
        WS("Email worksheet", [
            T("Open the email.", ["subject: quote request", "I am writing to ask for the quote", "attached you find the file"],
              ["Oggetto: Richiesta di preventivo.", "Le scrivo per chiedere il preventivo.", "In allegato trova il file."]),
            T("Close the email.", ["awaiting your reply", "kind regards"],
              ["In attesa di un Suo riscontro,", "cordiali saluti"]),
        ]))),
    ("B2-U3", "B2-U3-L3", L(
        "Leggere le notizie: dal titolo al rapporto",
        "A headline and a report say the same thing in two grammars: «Disoccupazione in calo» piles "
        "nouns, while «il tasso di disoccupazione è sceso del 2%» builds a sentence with a verb and "
        "a figure.",
        [V("il titolo", "eel TEE-toh-loh", "headline", "noun"),
         V("il tasso", "eel TAHS-soh", "rate", "noun"),
         V("il calo", "eel KAH-loh", "fall", "noun"),
         V("la fonte", "lah FOHN-teh", "source", "noun"),
         V("secondo", "seh-KOHN-doh", "according to", "preposition")],
        G("Headline ↔ report",
          "disoccupazione in calo (titolo) · il tasso è sceso del 2% (rapporto) · secondo + fonte",
          "Il titolo annuncia: «Disoccupazione in calo». Il rapporto precisa: il tasso di "
          "disoccupazione è sceso di due punti nel primo trimestre, secondo l'ISTAT. A translator "
          "moves between the pile and the sentence on purpose.",
          [X("Titolo: Disoccupazione in calo.", "TEE-toh-loh: dee-zoh-koo-pah-TSYOH-neh een KAH-loh.", "Headline: unemployment falling."),
           X("Il tasso è sceso del due per cento.", "eel TAHS-soh eh SHEH-zoh del DOO-eh per CHEN-toh.", "The rate fell by two per cent."),
           X("Secondo l'ISTAT il calo rallenta.", "seh-KOHN-doh lees-TAHT eel KAH-loh rahl-LEN-tah.", "According to ISTAT the fall is slowing.")],
          [("Il tasso è sceso del 2%, perché c'è la crisi.", "Il tasso è sceso del 2% nel primo trimestre.", "The report states the figure and its period; the cause is a different sentence."),
           ("Secondo l'ISTAT ha detto che …", "Secondo l'ISTAT, …", "secondo takes a source, not a clause with a verb.")]),
        [D("Sofia", "Il titolo dice «Disoccupazione in calo».", "eel TEE-toh-loh DEE-cheh dee-zoh-koo-pah-TSYOH-neh een KAH-loh.", "The headline says 'unemployment falling'."),
         D("Marco", "Il rapporto invece dà il periodo e la fonte.", "eel rahp-POR-toh een-VEH-cheh dah eel peh-RYOH-doh eh lah FOHN-teh.", "The report gives the period and the source instead."),
         D("Sofia", "«Il tasso è sceso del due per cento nel primo trimestre, secondo l'ISTAT.»", "eel TAHS-soh eh SHEH-zoh del DOO-eh per CHEN-toh nel PREE-moh tree-MES-treh, seh-KOHN-doh lees-TAHT.", "'The rate fell by two per cent in the first quarter, according to ISTAT.'"),
         D("Marco", "Ecco: il titolo vende, il rapporto verifica.", "EK-koh: eel TEE-toh-loh VEN-deh, eel rahp-POR-toh veh-REE-fee-kah.", "There you go: the headline sells, the report verifies.")],
        WS("News worksheet", [
            T("Turn the headline into a report sentence.", ["unemployment falling", "prices rising"],
              ["Il tasso di disoccupazione è sceso del 2%.", "I prezzi sono aumentati leggermente."]),
            T("Turn the report sentence into a headline.", ["the rate fell by two per cent", "consumption fell"],
              ["Disoccupazione in calo.", "Consumi in calo."]),
        ]))),
]

THIRD["C1"] = [
    ("it-c1-u1", "it-c1-l7", L(
        "Il discorso indiretto libero: la voce senza virgolette",
        "Free indirect discourse lets a character's words into the narration with no quotation marks: "
        "the tense and the pronouns stay with the narrator, while the questions, the exclamations and "
        "the evaluations belong to the character. Italian novels run on it, and so does a report that "
        "wants to name a view without adopting it.",
        [V("il discorso indiretto libero", "eel dees-KOR-soh een-dee-RET-toh LEE-beh-roh", "free indirect discourse", "noun"),
         V("la voce narrante", "lah VOH-cheh nar-RAHN-teh", "the narrating voice", "noun"),
         V("l'esclamazione", "les-klah-mah-TSYOH-neh", "exclamation", "noun"),
         V("la domanda indiretta", "lah doh-MAHN-dah een-dee-RET-tah", "indirect question", "noun"),
         V("il pensiero", "eel pen-SYEH-roh", "thought", "noun")],
        G("Free indirect frame",
          "sarebbe arrivato tardi, lo sapeva · perché non aveva chiamato? · che sciocco era stato",
          "Sarebbe arrivato tardi, lo sapeva. Perché non aveva chiamato prima? Che sciocco era stato. "
          "No reporting verb, no colon: the modality (sarebbe, the exclamation) marks the voice as the "
          "character's, while the tenses stay inside the narration.",
          [X("Sarebbe arrivato tardi, lo sapeva.", "sah-REB-beh ahr-ree-VAH-toh TAR-dee, loh sah-PEH-vah.", "He would arrive late, he knew it."),
           X("Perché non aveva chiamato prima?", "per-KEH nohn ah-VEH-vah kyah-MAH-toh PREE-mah?", "Why had he not called earlier?"),
           X("Che sciocco era stato.", "keh SHOHK-koh EH-rah STAH-toh.", "What a fool he had been.")],
          [("Disse: sarebbe arrivato tardi.", "Sarebbe arrivato tardi, lo sapeva.", "Free indirect discourse drops the reporting verb and the colon; the viewpoint carries them."),
           ("Perché non ha chiamato prima? (inside a past narration)", "Perché non aveva chiamato prima?", "The character's question keeps the narration's tense.")]),
        [D("Editor", "Come fai entrare il punto di vista senza virgolette?", "KOH-meh fehy ahn-TRAH-reh eel POON-toh dee VEES-tah SEN-tsah veer-GOHT-tseh?", "How do you let the viewpoint in without quotation marks?"),
         D("Mediator", "Con il modo e il tempo: «sarebbe arrivato tardi, lo sapeva».", "kohn eel MOH-doh eh eel TEM-poh: sah-REB-beh ahr-ree-VAH-toh TAR-dee, loh sah-PEH-vah.", "With mood and tense: 'he would arrive late, he knew it'."),
         D("Editor", "E la domanda?", "eh lah doh-MAHN-dah?", "And the question?"),
         D("Reviewer", "Resta del personaggio, ma nel tempo del racconto: «perché non aveva chiamato?».", "RES-tah del per-soh-NAJ-joh, mah nel TEM-poh del rahk-KOHN-toh: per-KEH nohn ah-VEH-vah kyah-MAH-toh?", "It stays the character's, but in the narration's tense: 'why had he not called?'.")],
        WS("Voice worksheet", [
            T("Move the view inside.", ["he would arrive late, he knew it", "what a fool he had been"],
              ["Sarebbe arrivato tardi, lo sapeva.", "Che sciocco era stato."]),
            T("Keep the narration's tense.", ["why had he not called?", "where would he sleep?"],
              ["Perché non aveva chiamato?", "Dove avrebbe dormito?"]),
        ]))),
    ("it-c1-u2", "it-c1-l8", L(
        "La precisione giuridica: ai sensi di, fatto salvo",
        "Legal Italian names its own machinery: AI SENSI DELL'ARTICOLO 5, FATTO SALVO IL DIRITTO DI "
        "RECESSO, È FATTO OBBLIGO DI … Each formula either points to a source of authority or "
        "preserves a right — none of them is decoration, and swapping one for another changes the "
        "obligation.",
        [V("ai sensi di", "ahy SEN-see dee", "under the terms of", "phrase"),
         V("fatto salvo", "FAHT-toh SAHL-voh", "without prejudice to", "phrase"),
         V("la clausola", "lah KLOW-zoh-lah", "clause", "noun"),
         V("il dispositivo", "eel dee-spoh-zee-TEE-voh", "operative part (of a ruling)", "noun"),
         V("l'obbligo", "loh-BLEE-goh", "obligation", "noun")],
        G("Normative frame",
          "ai sensi dell'articolo 5 · fatto salvo il diritto di recesso · è fatto obbligo di …",
          "Ai sensi dell'articolo 5, il termine è di trenta giorni. Fatto salvo il diritto di recesso, "
          "è fatto obbligo di comunicare la variazione. Each formula either cites the norm or protects "
          "a right; that is why it cannot be replaced by a synonym.",
          [X("Ai sensi dell'articolo 5, il termine è di trenta giorni.", "ahy SEN-see del-lar-TEE-koh-loh CHEEN-kweh, eel TER-mee-neh eh dee TREHN-tah JOR-nee.", "Under article 5, the deadline is thirty days."),
           X("Fatto salvo il diritto di recesso.", "FAHT-toh SAHL-voh eel dee-REET-toh dee reh-CHES-soh.", "Without prejudice to the right of withdrawal."),
           X("È fatto obbligo di comunicare la variazione.", "eh FAHT-toh oh-BLEE-goh dee koh-moo-nee-KAH-reh lah vah-ryah-TSYOH-neh.", "It is mandatory to notify the change.")],
          [("Secondo l'articolo 5, il termine è di trenta giorni.", "Ai sensi dell'articolo 5, il termine è di trenta giorni.", "ai sensi di cites the norm itself; secondo reports what someone says about it."),
           ("Fatto salvo di recedere dal contratto.", "Fatto salvo il diritto di recesso.", "fatto salvo takes a noun, not an infinitive.")]),
        [D("Analyst", "Questo comma che cosa salva?", "KWES-toh KOH-mah keh KOH-zah SAHL-vah?", "What does this clause preserve?"),
         D("Reviewer", "Il diritto di recesso: «fatto salvo il diritto di recesso».", "eel dee-REET-toh dee reh-CHES-soh: FAHT-toh SAHL-voh eel dee-REET-toh dee reh-CHES-soh.", "The right of withdrawal: 'without prejudice to the right of withdrawal'."),
         D("Analyst", "E il termine?", "eh eel TER-mee-neh?", "And the deadline?"),
         D("Reviewer", "«Ai sensi dell'articolo 5, trenta giorni»: la norma, non l'opinione.", "ahy SEN-see del-lar-TEE-koh-loh CHEEN-kweh, TREHN-tah JOR-nee: lah NOR-mah, nohn loh-pee-NYOH-neh.", "'Under article 5, thirty days': the norm, not an opinion.")],
        WS("Normative worksheet", [
            T("Cite the norm.", ["under article 5", "without prejudice to the right of withdrawal"],
              ["Ai sensi dell'articolo 5,", "Fatto salvo il diritto di recesso,"]),
            T("State the duty.", ["it is mandatory to notify the change", "within thirty days"],
              ["È fatto obbligo di comunicare la variazione.", "entro trenta giorni."]),
        ]))),
    ("it-c1-u3", "it-c1-l9", L(
        "La mediazione: rendere accessibile senza tradire",
        "A mediator does two jobs at once: make the text usable — «in parole semplici: la misura entra "
        "in vigore a gennaio» — and record the loss. «Il testo dice dispositivo: qui vale misura» is a "
        "note, not a failure. Accessibility with no trace of the compromise is not mediation; it is "
        "rewriting.",
        [V("la mediazione", "lah meh-dyah-TSYOH-neh", "mediation", "noun"),
         V("rendere accessibile", "REN-deh-reh ah-ches-SEE-bee-leh", "to make accessible", "phrase"),
         V("il registro", "eel reh-JEES-troh", "register", "noun"),
         V("il pubblico di riferimento", "eel POOB-blee-koh dee ree-feh-ree-MEN-toh", "target audience", "noun"),
         V("la nota del mediatore", "lah NOH-tah del meh-dyah-TOH-reh", "mediator's note", "noun")],
        G("Mediation frame",
          "in parole semplici, … · il testo dice …, qui vale … · la nota del mediatore segnala …",
          "In parole semplici, la misura entra in vigore a gennaio. Il testo dice «dispositivo»: qui "
          "vale «misura». La nota del mediatore segnala ciò che si perde. The plain version and the "
          "record of the loss travel together.",
          [X("In parole semplici, la misura entra in vigore a gennaio.", "een pah-ROH-leh SEM-plee-chee, lah mee-ZOO-rah EN-trah een vee-GOH-reh ah jen-NAH-yoh.", "In plain words, the measure comes into force in January."),
           X("Il testo dice «dispositivo»: qui vale «misura».", "eel TES-toh DEE-cheh dee-spoh-zee-TEE-voh: kwee VAH-leh mee-ZOO-rah.", "The text says 'dispositivo': here it means 'measure'."),
           X("La nota segnala ciò che si perde.", "lah NOH-tah seh-NYAH-lah choh keh see PER-deh.", "The note flags what is lost.")],
          [("In parole semplici, il dispositivo de quo entra in vigore.", "In parole semplici, la misura entra in vigore a gennaio.", "Plain language means plain: no residual jargon in the same sentence."),
           ("Ho reso tutto: non manca niente.", "Ho reso il testo accessibile e ho segnalato in nota ciò che resta intraducibile.", "A mediator records the loss instead of denying it.")]),
        [D("Mediator", "Il committente vuole il testo in parole semplici.", "eel koh-MEET-ten-teh VWOH-leh eel TES-toh een pah-ROH-leh SEM-plee-chee.", "The client wants the text in plain words."),
         D("Editor", "Allora togliamo «dispositivo» e mettiamo «misura».", "ahl-LOH-rah toh-LYAH-moh dee-spoh-zee-TEE-voh eh met-TYAH-moh mee-ZOO-rah.", "Then let us drop 'dispositivo' and put 'misura'."),
         D("Mediator", "Sì, e in nota segnaliamo che il testo giuridico usa un'altra parola.", "see, eh een NOH-tah seh-NYAH-lyah-moh keh eel TES-toh joo-REE-dee-koh OO-zah oo-NAL-trah pah-ROH-lah.", "Yes, and in a note we flag that the legal text uses a different word."),
         D("Reviewer", "Accessibile, ma con la traccia del compromesso.", "ah-ches-SEE-bee-leh, mah kohn lah TRAHT-chah del kohm-proh-MES-soh.", "Accessible, but with a trace of the compromise.")],
        WS("Mediation worksheet", [
            T("Make it usable.", ["in plain words", "the measure comes into force in January"],
              ["In parole semplici,", "la misura entra in vigore a gennaio."]),
            T("Record the loss.", ["the mediator's note flags what is lost", "the text says 'dispositivo'"],
              ["La nota del mediatore segnala ciò che si perde.", "Il testo dice «dispositivo»."]),
        ]))),
]

THIRD["C2"] = [
    ("it-c2-u1", "it-c2-l7", L(
        "Leggere tra le righe: il rifiuto cortese",
        "Italian refuses without the word no: «Ci pensiamo», «Vediamo», «Le faremo sapere». C2 reading "
        "means hearing the refusal inside the hedge — and, when writing one, leaving the door ajar on "
        "purpose rather than by accident.",
        [V("il rifiuto", "eel ree-FYOO-toh", "refusal", "noun"),
         V("il margine di manovra", "eel MAR-jee-neh dee mah-NOH-vrah", "room for manoeuvre", "noun"),
         V("prendere tempo", "PREN-deh-reh TEM-poh", "to stall", "phrase"),
         V("la disponibilità", "lah dee-spoh-nee-bee-lee-TAH", "willingness", "noun"),
         V("l'apertura", "lah-pehr-TOO-rah", "opening", "noun")],
        G("Graded refusal",
          "ci pensiamo · vediamo cosa si può fare · al momento non è possibile, ma … · Le faremo sapere",
          "«Ci pensiamo» means no. «Vediamo cosa si può fare» means probably not, and asks for a reason "
          "to change. «Al momento non è possibile, ma ci risentiamo a settembre» is a real no with a "
          "date attached. The hedge is a graded scale, and the reader knows which step they are on.",
          [X("Ci pensiamo e Le facciamo sapere.", "chee pen-SYAH-moh eh leh fah-CHA-moh sah-PEH-reh.", "We will think about it and let you know."),
           X("Al momento non è possibile, ma ci risentiamo a settembre.", "ahl moh-MEN-toh nohn eh pohs-SEE-bee-leh, mah chee ree-sen-TYAH-moh ah set-TEM-breh.", "At the moment it is not possible, but we will speak again in September."),
           X("Vediamo cosa si può fare, senza promettere nulla.", "veh-DYAH-moh KOH-zah see pwoh FAH-reh, SEN-tsah proh-MET-teh-reh NOOL-lah.", "Let us see what can be done, without promising anything.")],
          [("No, non ci interessa. (formal first reply)", "Al momento non rientra nelle nostre priorità, ma La ringrazio.", "A bare no closes the exchange; the graded refusal keeps the relationship."),
           ("Ci pensiamo, ci risentiamo.", "Ci pensiamo e Le facciamo sapere entro venerdì.", "A hedge with a date is a deferral; without one it is a refusal.")]),
        [D("Reviewer", "Hanno risposto «ci pensiamo».", "AHN-noh ree-SPOHS-toh chee pen-SYAH-moh.", "They replied 'we will think about it'."),
         D("Analyst", "Senza data? Allora è un no.", "SEN-tsah DAH-tah? ahl-LOH-rah eh oon noh.", "With no date? Then it is a no."),
         D("Reviewer", "Però hanno aggiunto «vediamo cosa si può fare».", "peh-ROH AHN-noh aj-JOON-toh veh-DYAH-moh KOH-zah see pwoh FAH-reh.", "But they added 'let us see what can be done'."),
         D("Analyst", "Allora c'è un margine: mandiamo i numeri.", "ahl-LOH-rah cheh oon MAR-jee-neh: mahn-DYAH-moh ee NOO-meh-ree.", "Then there is room: let us send the figures.")],
        WS("Hedge worksheet", [
            T("Read the hedge.", ["we will think about it (no date)", "we will see what can be done"],
              ["Ci pensiamo: è un no.", "Vediamo cosa si può fare: c'è un margine."]),
            T("Write a graded refusal.", ["not possible at the moment, but in touch in September", "thank you for the proposal"],
              ["Al momento non è possibile, ma ci risentiamo a settembre.", "La ringrazio per la proposta."]),
        ]))),
    ("it-c2-u2", "it-c2-l8", L(
        "Il periodare: ritmo, incisi, parentesi",
        "Italian lets a sentence run, and the main clause can wait while an inciso does its work. What "
        "it cannot do is lose the thread: «La misura, annunciata a gennaio, è entrata in vigore» holds; "
        "a second parenthesis before the verb does not.",
        [V("il periodare", "eel peh-ryoh-DAH-reh", "sentence rhythm, period structure", "noun"),
         V("l'inciso", "leen-CHEE-zoh", "parenthetical phrase", "noun"),
         V("la parentesi", "lah pah-REN-teh-zee", "parenthesis", "noun"),
         V("la virgola", "lah VEER-goh-lah", "comma", "noun"),
         V("il ritmo", "eel REET-moh", "rhythm", "noun")],
        G("Long-period frame",
          "la frase regge · un inciso per frase · il verbo al posto che gli spetta",
          "La misura, annunciata a gennaio, è entrata in vigore lunedì. One inciso, then the verb, then "
          "the rest. Add a second parenthesis and the reader loses the clause they were holding; put "
          "the verb inside the inciso and there is no sentence left.",
          [X("La misura, annunciata a gennaio, è entrata in vigore.", "lah mee-ZOO-rah, ahn-noon-CHAH-tah ah jen-NAH-yoh, eh en-TRAH-tah een vee-GOH-reh.", "The measure, announced in January, came into force."),
           X("Tutti aspettavano una data (e nessuno la conosceva).", "TOOT-tee ah-spet-TAH-vah-noh OO-nah DAH-tah (eh nes-SOO-noh lah koh-noh-SHEH-vah).", "Everyone was waiting for a date (and nobody knew it)."),
           X("Il verbo regge la frase; l'inciso la interrompe una volta sola.", "eel VER-boh REJ-jeh lah FRAH-zeh; leen-CHEE-zoh lah een-ter-ROHM-peh OO-nah VOHL-tah SOH-lah.", "The verb carries the sentence; the parenthesis interrupts it once.")],
          [("La misura, annunciata a gennaio, che tutti aspettavano, è entrata in vigore, dopo tante discussioni, in ritardo.", "La misura, annunciata a gennaio, è entrata in vigore lunedì.", "One inciso per sentence; the second breaks the reader's hold."),
           ("Il periodo lungo è elegante, quindi va usato.", "Il periodo lungo va usato quando la gerarchia delle idee lo richiede.", "Rhythm serves the meaning, not the other way round.")]),
        [D("Editor", "Questa frase ha tre incisi.", "KWES-tah FRAH-zeh ah treh een-CHEE-zee.", "This sentence has three parentheses."),
         D("Reviewer", "Allora ne togliamo due: il lettore deve respirare.", "ahl-LOH-rah neh toh-LYAH-moh DOO-eh: eel let-TOH-reh DEH-veh reh-spee-RAH-reh.", "Then we drop two: the reader has to breathe."),
         D("Editor", "E il verbo dove lo mettiamo?", "eh eel VER-boh DOH-veh loh met-TYAH-moh?", "And where do we put the verb?"),
         D("Reviewer", "Al posto che gli spetta: dopo l'inciso, non dentro.", "ahl POHS-toh keh ly SPEHT-tah: DOH-poh leen-CHEE-zoh, nohn DEN-troh.", "Where it belongs: after the parenthesis, not inside it.")],
        WS("Rhythm worksheet", [
            T("Keep the thread.", ["the measure, announced in January, came into force on Monday", "everyone was waiting for a date"],
              ["La misura, annunciata a gennaio, è entrata in vigore lunedì.", "Tutti aspettavano una data."]),
            T("Move the inciso.", ["one parenthesis per sentence", "the verb carries the sentence"],
              ["Un inciso per frase.", "Il verbo regge la frase."]),
        ]))),
    ("it-c2-u3", "it-c2-l9", L(
        "Quando il testo resiste: intraducibilità e nota del mediatore",
        "Some words resist. «Municipio» is not «town hall» when the office also keeps the registers. "
        "C2 mediation does not pretend the gap away: it chooses a rendering, says so, and puts what is "
        "left into a note.",
        [V("l'intraducibilità", "leen-trah-doo-chee-bee-lee-TAH", "untranslatability", "noun"),
         V("la perdita", "lah PER-dee-tah", "loss", "noun"),
         V("la resa", "lah REH-zah", "rendering", "noun"),
         V("il compromesso", "eel kohm-proh-MES-soh", "compromise", "noun"),
         V("la nota del mediatore", "lah NOH-tah del meh-dyah-TOH-reh", "mediator's note", "noun")],
        G("Limits frame",
          "il testo resiste · si sceglie una resa e la si dichiara · la perdita si annota",
          "Qui «municipio» vale l'ente che tiene i registri, non solo l'edificio. Si sceglie una resa, "
          "la si dichiara in nota e la perdita resta scritta. A gap that is not flagged reads as if it "
          "did not exist.",
          [X("Qui «municipio» vale l'ente che tiene i registri.", "kwee moo-NEE-chee-poh VAH-leh LEN-teh keh TYEH-neh ee reh-JEES-tree.", "Here 'municipio' means the body that keeps the registers."),
           X("La scelta è dichiarata in nota.", "lah SHEL-tah eh dee-kyah-RAH-tah een NOH-tah.", "The choice is declared in a note."),
           X("La perdita si annota invece di nasconderla.", "lah PER-dee-tah see ahn-NOH-tah een-VEH-cheh dee nah-SKOHN-der-lah.", "The loss is annotated instead of hidden.")],
          [("Ho reso «municipio» con «town hall» e non ho segnalato nulla.", "Ho reso «municipio» con «town hall» e in nota ho chiarito la differenza.", "A cross-cultural gap that is not flagged reads as if it did not exist."),
           ("La nota del mediatore è un'ammissione di debolezza.", "La nota del mediatore è parte della resa.", "Mediation documents the compromise; it does not apologise for it.")]),
        [D("Mediator", "«Municipio» non è soltanto l'edificio.", "moo-NEE-chee-poh nohn eh sohl-TAHN-toh leh-dee-FEE-choh.", "'Municipio' is not only the building."),
         D("Analyst", "Allora in nota: l'ente che tiene i registri.", "ahl-LOH-rah een NOH-tah: LEN-teh keh TYEH-neh ee reh-JEES-tree.", "Then in a note: the body that keeps the registers."),
         D("Mediator", "E il resto della frase?", "eh eel RES-toh DEL-lah FRAH-zeh?", "And the rest of the sentence?"),
         D("Reviewer", "Regge: la perdita è dichiarata dove serve, non nascosta.", "REJ-jeh: lah PER-dee-tah eh dee-kyah-RAH-tah DOH-veh SER-veh, nohn nah-SKOH-stah.", "It holds: the loss is declared where it matters, not hidden.")],
        WS("Resistance worksheet", [
            T("Declare the choice.", ["here 'municipio' means the body that keeps the registers", "the choice is declared in a note"],
              ["Qui «municipio» vale l'ente che tiene i registri.", "La scelta è dichiarata in nota."]),
            T("Annotate the loss.", ["the loss is annotated", "mediation documents the compromise"],
              ["La perdita si annota.", "La mediazione documenta il compromesso."]),
        ]))),
]

HALFSTEPS["A1+"] = {
    "title": "Italian A1+ — Getting around",
    "native": NATIVE,
    "goals": [
        "Ask the way, buy a ticket and name a landmark",
        "Say a time, a phone number and an address out loud",
        "Make a plan for the week — or turn one down politely",
    ],
    "units": [
        {"id": "A1+-U1", "title": "In città", "lessons": [
            L("Sempre dritto, poi a destra: chiedere la strada",
              "Directions are an imperative and a landmark: VADA SEMPRE DRITTO, POI A DESTRA. Add "
              "«scusi» at the front and «per favore» at the end and it works with anyone.",
              [V("sempre dritto", "SEM-preh DREET-toh", "straight ahead", "phrase"),
               V("a destra", "ah DES-trah", "to the right", "phrase"),
               V("l'angolo", "LAN-goh-loh", "corner", "noun"),
               V("vicino a", "vee-CHEE-noh ah", "near", "phrase"),
               V("attraversare", "aht-trah-ver-SAH-reh", "to cross", "verb")],
              G("Directions",
                "vada sempre dritto · poi a destra · all'angolo · vicino alla piazza",
                "Vada sempre dritto, poi la seconda strada a sinistra. La stazione è all'angolo, "
                "vicino alla piazza. The polite imperative vada carries the whole instruction — the "
                "landmark at the end is what the listener actually walks towards.",
                [X("Vada sempre dritto, poi a destra.", "VAH-dah SEM-preh DREET-toh, pohy ah DES-trah.", "Go straight ahead, then right."),
                 X("La stazione è all'angolo.", "lah stah-TSYOH-neh eh ahl-LAN-goh-loh.", "The station is on the corner."),
                 X("È vicino alla piazza?", "eh vee-CHEE-noh AHL-lah PYAHT-tsah?", "Is it near the square?")],
                [("Va sempre dritto, poi a destra. (to a stranger)", "Vada sempre dritto, poi a destra.", "With a stranger the polite imperative is vada, not va."),
                 ("È vicino la piazza.", "È vicino alla piazza.", "vicino a keeps its article: vicino alla piazza.")]),
              [D("Marco", "Scusi, dov'è la stazione?", "SKOO-zee, doh-VEH lah stah-TSYOH-neh?", "Excuse me, where is the station?"),
               D("Sofia", "Vada sempre dritto, poi a destra.", "VAH-dah SEM-preh DREET-toh, pohy ah DES-trah.", "Go straight ahead, then right."),
               D("Marco", "È lontano?", "eh lohn-TAH-noh?", "Is it far?"),
               D("Sofia", "No, cinque minuti a piedi.", "noh, CHEEN-kweh mee-NOO-tee ah PYEH-dee.", "No, five minutes on foot.")],
              WS("Directions worksheet", [
                  T("Give the direction.", ["go straight ahead", "then right", "at the corner"],
                    ["Vada sempre dritto.", "poi a destra", "all'angolo"]),
                  T("Ask and answer.", ["Where is the station? (nearby)", "Is it far? (no, five minutes on foot)"],
                    ["Dov'è la stazione? — È vicina.", "È lontano? — No, cinque minuti a piedi."]),
              ])),
            L("Il biglietto e la fermata: quanto costa, dove scendo",
              "Ticket talk has three moves: ask for the ticket, ask the price, name the stop. UN "
              "BIGLIETTO PER IL CENTRO, PER FAVORE · QUANTO COSTA? · SCENDO ALLA TERZA FERMATA.",
              [V("il biglietto", "eel beel-YET-toh", "ticket", "noun"),
               V("la corsa semplice", "lah KOR-sah SEM-plee-cheh", "single ride", "noun"),
               V("la fermata", "lah fer-MAH-tah", "stop", "noun"),
               V("convalidare", "kohn-vah-lee-DAH-reh", "to validate (a ticket)", "verb"),
               V("l'autobus", "LOW-toh-boos", "bus", "noun")],
              G("Tickets and stops",
                "un biglietto per il centro · quanto costa la corsa semplice? · scendo alla terza fermata",
                "Un biglietto per il centro, per favore. Quanto costa? Novanta centesimi. Scendo alla "
                "terza fermata. The destination arrives with per; the price question is quanto costa, "
                "unchanged whether the thing is singular or plural in speech.",
                [X("Un biglietto per il centro, per favore.", "oon beel-YET-toh per eel CHEN-troh, per fah-VOH-reh.", "A ticket to the centre, please."),
                 X("Quanto costa la corsa semplice?", "KWAHN-toh KOHS-tah lah KOR-sah SEM-plee-cheh?", "How much is a single ride?"),
                 X("Scendo alla terza fermata.", "SHEN-doh AHL-lah TER-tsah fer-MAH-tah.", "I get off at the third stop.")],
                [("Un biglietto al centro.", "Un biglietto per il centro.", "A destination takes per, not al."),
                 ("Io scendo alla terza fermata.", "Scendo alla terza fermata.", "Subject pronouns drop unless they carry a contrast.")]),
              [D("Sofia", "Un biglietto per il centro, per favore.", "oon beel-YET-toh per eel CHEN-troh, per fah-VOH-reh.", "A ticket to the centre, please."),
               D("Marco", "Novanta centesimi.", "noh-VAHN-tah chen-TEH-zee-mee.", "Ninety cents."),
               D("Sofia", "Devo convalidarlo?", "DEH-voh kohn-vah-lee-DAR-loh?", "Do I have to validate it?"),
               D("Marco", "Sì, sulla macchinetta gialla.", "see, SOOL-lah mahk-kee-NET-tah JAL-lah.", "Yes, on the yellow machine.")],
              WS("Ticket worksheet", [
                  T("Buy the ticket.", ["a ticket to the centre, please", "how much is a single?"],
                    ["Un biglietto per il centro, per favore.", "Quanto costa la corsa semplice?"]),
                  T("Name the stop.", ["I get off at the third stop", "do I have to validate it?"],
                    ["Scendo alla terza fermata.", "Devo convalidarlo?"]),
              ])),
            L("L'indirizzo: via, piazza, numero civico",
              "An address gives the street, the number, the floor and one landmark: ABITO IN VIA ROMA "
              "12, AL SECONDO PIANO, DI FRONTE ALLA POSTA. The landmark is what makes it findable.",
              [V("l'indirizzo", "leen-dee-REET-tsoh", "address", "noun"),
               V("la via", "lah VEE-ah", "street", "noun"),
               V("la piazza", "lah PYAHT-tsah", "square", "noun"),
               V("il numero civico", "eel NOO-meh-roh CHEE-vee-koh", "street number", "noun"),
               V("di fronte a", "dee FRON-teh ah", "opposite", "phrase")],
              G("Addresses",
                "abito in via Roma 12 · al secondo piano · di fronte alla posta",
                "Abito in via Roma 12, al secondo piano. È di fronte alla posta, non lontano dalla "
                "piazza. Addresses take in + via; the floor takes a + article; the landmark arrives "
                "with di fronte a.",
                [X("Abito in via Roma 12.", "AH-bee-toh een VEE-ah ROH-mah DOH-dee-chee.", "I live at 12 Via Roma."),
                 X("È al secondo piano.", "eh ahl seh-KOHN-doh PYAH-noh.", "It is on the second floor."),
                 X("È di fronte alla posta.", "eh dee FRON-teh AHL-lah POHS-tah.", "It is opposite the post office.")],
                [("Abito a via Roma 12.", "Abito in via Roma 12.", "An address takes in + via."),
                 ("È fronte alla posta.", "È di fronte alla posta.", "di fronte a is fixed: the di never drops.")]),
              [D("Marco", "Qual è il tuo indirizzo?", "kwahl eh eel TOO-oh een-dee-REET-tsoh?", "What is your address?"),
               D("Sofia", "Via Roma 12, al secondo piano.", "VEE-ah ROH-mah DOH-dee-chee, ahl seh-KOHN-doh PYAH-noh.", "12 Via Roma, second floor."),
               D("Marco", "Di fronte alla posta?", "dee FRON-teh AHL-lah POHS-tah?", "Opposite the post office?"),
               D("Sofia", "Sì, proprio lì.", "see, PROH-pryoh lee.", "Yes, right there.")],
              WS("Address worksheet", [
                  T("Give the address.", ["I live at 12 Via Roma", "on the second floor"],
                    ["Abito in via Roma 12.", "al secondo piano"]),
                  T("Point at the landmark.", ["opposite the post office", "near the square"],
                    ["di fronte alla posta", "vicino alla piazza"]),
              ])),
        ]},
        {"id": "A1+-U2", "title": "Ore e appuntamenti", "lessons": [
            L("Che ore sono? Le otto e mezza",
              "The hour is plural and short: SONO LE OTTO E MEZZA, LE NOVE IN PUNTO. Only l'una is "
              "singular, and halves are said as mezza, never as thirty minutes.",
              [V("l'ora", "LOH-rah", "hour, time", "noun"),
               V("mezzogiorno", "med-dzoh-JOR-noh", "noon", "noun"),
               V("la mezzanotte", "lah med-dzah-NOT-teh", "midnight", "noun"),
               V("in punto", "een POON-toh", "exactly, on the dot", "phrase"),
               V("un quarto d'ora", "oon KWAR-toh DOH-rah", "a quarter of an hour", "phrase")],
              G("Telling the time",
                "che ore sono? · sono le otto e mezza · alle nove in punto",
                "Che ore sono? Sono le otto e mezza. Il treno parte alle nove in punto. The time of "
                "day takes essere with the plural article; a scheduled time takes a + le.",
                [X("Sono le otto e mezza.", "SOH-noh leh OT-toh eh MED-dzah.", "It is half past eight."),
                 X("Alle nove in punto.", "AHL-leh NOH-veh een POON-toh.", "At nine exactly."),
                 X("Manca un quarto d'ora.", "MAHN-kah oon KWAR-toh DOH-rah.", "There is a quarter of an hour to go.")],
                [("È le otto e mezza.", "Sono le otto e mezza.", "Hours take the plural: sono le otto; only l'una is singular."),
                 ("Sono le otto e trenta minuti.", "Sono le otto e mezza.", "Italian says e mezza, not trenta minuti.")]),
              [D("Sofia", "Che ore sono?", "keh OH-reh SOH-noh?", "What time is it?"),
               D("Marco", "Sono le otto e mezza.", "SOH-noh leh OT-toh eh MED-dzah.", "It is half past eight."),
               D("Sofia", "Il treno è alle nove in punto.", "eel TREH-noh eh AHL-leh NOH-veh een POON-toh.", "The train is at nine exactly."),
               D("Marco", "Allora abbiamo mezz'ora.", "ahl-LOH-rah ahb-BYAH-moh med-DZOH-rah.", "Then we have half an hour.")],
              WS("Clock worksheet", [
                  T("Say the time.", ["eight thirty", "nine o'clock exactly"],
                    ["Sono le otto e mezza.", "alle nove in punto"]),
                  T("Count the wait.", ["in a quarter of an hour", "we have half an hour"],
                    ["fra un quarto d'ora", "abbiamo mezz'ora"]),
              ])),
            L("I giorni e la settimana: lunedì, il fine settimana",
              "A single day takes nothing: LUNEDÌ HO LEZIONE. Repeated days take the article: IL LUNEDÌ "
              "NON LAVORO. The weekend is one phrase: IL FINE SETTIMANA.",
              [V("lunedì", "loo-neh-DEE", "Monday", "noun"),
               V("il fine settimana", "eel FEE-neh set-tee-MAH-nah", "the weekend", "noun"),
               V("la settimana prossima", "lah set-tee-MAH-nah PROHS-see-mah", "next week", "phrase"),
               V("feriale", "feh-RYAH-leh", "weekday (working day)", "adjective"),
               V("il giorno festivo", "eel JOR-noh fes-TEE-voh", "public holiday", "noun")],
              G("Days and the week",
                "lunedì · il fine settimana · la settimana prossima · nei giorni feriali",
                "Lunedì ho lezione, mercoledì lavoro fino a tardi e il fine settimana sono libero. "
                "Bare day names point at one day; il + day means every one of them.",
                [X("Lunedì ho lezione.", "loo-neh-DEE oh leh-TSYOH-neh.", "On Monday I have class."),
                 X("Il fine settimana sono libero.", "eel FEE-neh set-tee-MAH-nah SOH-noh LEE-beh-roh.", "At the weekend I am free."),
                 X("Nei giorni feriali gli uffici sono aperti.", "nay JOR-nee feh-RYAH-lee ly oof-FEE-chee SOH-noh ah-PER-tee.", "On weekdays the offices are open.")],
                [("Al lunedì ho lezione.", "Lunedì ho lezione.", "One Monday takes no preposition; il lunedì means every Monday."),
                 ("Sabato e la domenica sono il fine settimana.", "Sabato e domenica sono il fine settimana.", "Naming the two days needs no article when you mean the coming ones.")]),
              [D("Marco", "Cosa fai lunedì?", "KOH-zah fehy loo-neh-DEE?", "What are you doing on Monday?"),
               D("Sofia", "Lunedì lavoro; martedì sono libera.", "loo-neh-DEE lah-VOH-roh; mar-teh-DEE SOH-noh LEE-beh-rah.", "Monday I work; Tuesday I am free."),
               D("Marco", "E il fine settimana?", "eh eel FEE-neh set-tee-MAH-nah?", "And the weekend?"),
               D("Sofia", "Sabato vado al mare.", "SAH-bah-toh VAH-doh ahl MAH-reh.", "On Saturday I am going to the sea.")],
              WS("Week worksheet", [
                  T("Place the days.", ["on Monday I have class", "at the weekend I am free"],
                    ["Lunedì ho lezione.", "Il fine settimana sono libero."]),
                  T("Ask about the week.", ["what are you doing on Tuesday?", "are you free on Saturday?"],
                    ["Cosa fai martedì?", "Sei libera sabato?"]),
              ])),
            L("Fare un programma: ci vediamo alle sette",
              "A plan is one question that already contains a time and a place: CI VEDIAMO ALLE SETTE "
              "DAVANTI ALLA STAZIONE? TI VA BENE? Everything else — messages, delays — hangs on that.",
              [V("ci vediamo", "chee veh-DYAH-moh", "see you", "phrase"),
               V("ti va bene", "tee vah BEH-neh", "does that suit you", "phrase"),
               V("davanti a", "dah-VAHN-tee ah", "in front of", "phrase"),
               V("in ritardo", "een ree-TAR-doh", "late", "phrase"),
               V("l'appuntamento", "lahp-poon-tah-MEN-toh", "appointment", "noun")],
              G("Making a plan",
                "ci vediamo alle sette · ti va bene davanti alla stazione? · se sono in ritardo, mando un messaggio",
                "Ci vediamo alle sette davanti alla stazione? Ti va bene? Se sono in ritardo, mando "
                "un messaggio. Time with alle, place with davanti a, and the check-question at the "
                "end that leaves room for no.",
                [X("Ci vediamo alle sette.", "chee veh-DYAH-moh AHL-leh SET-teh.", "See you at seven."),
                 X("Ti va bene davanti alla stazione?", "tee vah BEH-neh dah-VAHN-tee AHL-lah stah-TSYOH-neh?", "Does the station front suit you?"),
                 X("Se sono in ritardo, mando un messaggio.", "seh SOH-noh een ree-TAR-doh, MAHN-doh oon mes-SAJ-joh.", "If I am late, I will send a message.")],
                [("Ci vediamo a sette ore.", "Ci vediamo alle sette.", "A clock time takes alle; ore is not said."),
                 ("Ti va bene alla stazione?", "Ti va bene davanti alla stazione?", "A meeting point needs a preposition that places people: davanti a.")]),
              [D("Sofia", "Ci vediamo alle sette?", "chee veh-DYAH-moh AHL-leh SET-teh?", "See you at seven?"),
               D("Marco", "Ti va bene davanti alla stazione?", "tee vah BEH-neh dah-VAHN-tee AHL-lah stah-TSYOH-neh?", "Does in front of the station suit you?"),
               D("Sofia", "Sì, ma non fare tardi.", "see, mah nohn FAH-reh TAR-dee.", "Yes, but do not be late."),
               D("Marco", "Tranquilla, arrivo in anticipo.", "trahn-KWEEL-lah, ahr-REE-voh een ahn-TEE-chee-poh.", "Relax, I arrive early.")],
              WS("Plan worksheet", [
                  T("Make the plan.", ["see you at seven", "in front of the station"],
                    ["Ci vediamo alle sette.", "davanti alla stazione"]),
                  T("Handle the delay.", ["I am late, I am sending a message", "is eight o'clock fine by you?"],
                    ["Sono in ritardo, mando un messaggio.", "Ti va bene alle otto?"]),
              ])),
        ]},
        {"id": "A1+-U3", "title": "Capire e farsi capire", "lessons": [
            L("Non ho capito: può ripetere?",
              "Three repair phrases keep a conversation alive: NON HO CAPITO · PUÒ RIPETERE, PER FAVORE? "
              "· PIÙ PIANO. They are not an admission of failure; they are turn-taking tools.",
              [V("ripetere", "ree-PEH-teh-reh", "to repeat", "verb"),
               V("più piano", "pyoo PYAH-noh", "more slowly, more quietly", "phrase"),
               V("come si scrive", "KOH-meh see SKREE-veh", "how is it written", "phrase"),
               V("non capisco", "nohn kah-PEES-koh", "I do not understand", "phrase"),
               V("scusi", "SKOO-zee", "excuse me (polite)", "interjection")],
              G("Repair phrases",
                "non ho capito · può ripetere, per favore? · più piano · come si scrive?",
                "Non ho capito: può ripetere, per favore? Più piano. Come si scrive? Each phrase hands "
                "the turn back to the other person with a precise instruction inside it.",
                [X("Non ho capito, può ripetere?", "nohn oh kah-PEE-toh, pwoh ree-PEH-teh-reh?", "I did not understand, can you repeat?"),
                 X("Può parlare più piano?", "pwoh par-LAH-reh pyoo PYAH-noh?", "Can you speak more slowly?"),
                 X("Come si scrive?", "KOH-meh see SKREE-veh?", "How is it written?")],
                [("Non capisco niente. (to the person helping you)", "Non ho capito, può ripetere?", "Ho capito names the one moment; niente sounds like a verdict on the speaker."),
                 ("Ripeti più piano. (to a stranger)", "Può ripetere più piano?", "With a stranger use the Lei form: può ripetere.")]),
              [D("Marco", "La fermata si chiama Corso Vittorio.", "lah fer-MAH-tah see KYAH-mah KOR-soh veet-TOH-ryoh.", "The stop is called Corso Vittorio."),
               D("Sofia", "Scusi, non ho capito: può ripetere più piano?", "SKOO-zee, nohn oh kah-PEE-toh: pwoh ree-PEH-teh-reh pyoo PYAH-noh?", "Sorry, I did not understand: can you repeat more slowly?"),
               D("Marco", "Corso Vittorio.", "KOR-soh veet-TOH-ryoh.", "Corso Vittorio."),
               D("Sofia", "Grazie. E come si scrive?", "GRAH-tsyeh. eh KOH-meh see SKREE-veh?", "Thanks. And how is it written?")],
              WS("Repair worksheet", [
                  T("Ask for the repair.", ["I did not understand, can you repeat?", "more slowly, please"],
                    ["Non ho capito, può ripetere?", "Più piano, per favore."]),
                  T("Ask how it is written.", ["how do you spell it?", "I do not know this word"],
                    ["Come si scrive?", "Non conosco questa parola."]),
              ])),
            L("Chiedere un favore: mi dai una mano?",
              "A favour opens with a question and closes with one word: MI DAI UNA MANO CON LA VALIGIA? "
              "VOLENTIERI. Between friends the tu form is right; with anyone else, mi può.",
              [V("dare una mano", "DAH-reh OO-nah MAH-noh", "to give a hand", "phrase"),
               V("prestare", "preh-STAH-reh", "to lend", "verb"),
               V("volentieri", "voh-len-TYEH-ree", "gladly", "adverb"),
               V("con piacere", "kohn pyah-CHEH-reh", "with pleasure", "phrase"),
               V("se possibile", "seh pohs-SEE-bee-leh", "if possible", "phrase")],
              G("Asking a favour",
                "mi dai una mano? · mi presti …? · volentieri · ci mancherebbe",
                "Mi dai una mano con la valigia? Volentieri. Mi presti la penna un secondo? Con "
                "piacere. The request is a question in the present, and the answer is one word — "
                "long answers sound reluctant.",
                [X("Mi dai una mano con la valigia?", "mee dahy OO-nah MAH-noh kohn lah vah-LEEJ-jah?", "Can you give me a hand with the suitcase?"),
                 X("Mi presti la penna?", "mee PRES-tee lah PEN-nah?", "Can you lend me the pen?"),
                 X("Volentieri, ci mancherebbe.", "voh-len-TYEH-ree, chee mahn-keh-REB-beh.", "Gladly, of course.")],
                [("Dammi una mano. (to a stranger)", "Mi può dare una mano?", "The bare imperative dammi is for friends; a stranger gets mi può."),
                 ("Grazie, sì, va bene, certo. (accepting a favour)", "Volentieri, grazie.", "One word accepts a favour; a piling-up sounds like hesitation.")]),
              [D("Sofia", "Marco, mi dai una mano con la valigia?", "MAR-koh, mee dahy OO-nah MAH-noh kohn lah vah-LEEJ-jah?", "Marco, can you give me a hand with the suitcase?"),
               D("Marco", "Volentieri.", "voh-len-TYEH-ree.", "Gladly."),
               D("Sofia", "Grazie mille.", "GRAH-tsyeh MEEL-leh.", "Thanks a lot."),
               D("Marco", "Ci mancherebbe.", "chee mahn-keh-REB-beh.", "Of course, no need to thank me.")],
              WS("Favour worksheet", [
                  T("Ask a favour.", ["can you give me a hand with the suitcase?", "can you lend me a pen?"],
                    ["Mi dai una mano con la valigia?", "Mi presti una penna?"]),
                  T("Answer well.", ["gladly", "of course, no need"],
                    ["Volentieri.", "Ci mancherebbe."]),
              ])),
            L("Quanto costa? Prezzi e pagamenti",
              "Every counter asks three things: QUANTO COSTA? · POSSO PAGARE CON LA CARTA? · MI DÀ LO "
              "SCONTRINO? Price, method, receipt — in that order, and the purchase is closed.",
              [V("quanto costa", "KWAHN-toh KOHS-tah", "how much does it cost", "phrase"),
               V("in contanti", "een kohn-TAHN-tee", "in cash", "phrase"),
               V("la carta", "lah KAR-tah", "card (bank card)", "noun"),
               V("lo sconto", "loh SKOHN-toh", "discount", "noun"),
               V("lo scontrino", "loh skohn-TREE-noh", "receipt", "noun")],
              G("Prices and payment",
                "quanto costa? · posso pagare con la carta? · mi dà lo scontrino?",
                "Quanto costa questa borsa? Trentacinque euro. Posso pagare con la carta? Certo. Mi "
                "dà lo scontrino, per favore? Means of payment keeps its article, and the receipt "
                "question is the last thing you say.",
                [X("Quanto costa questa borsa?", "KWAHN-toh KOHS-tah KWES-tah BOR-sah?", "How much does this bag cost?"),
                 X("Posso pagare con la carta?", "POHS-soh pah-GAH-reh kohn lah KAR-tah?", "Can I pay by card?"),
                 X("Mi dà lo scontrino, per favore?", "mee dah loh skohn-TREE-noh, per fah-VOH-reh?", "Can you give me the receipt, please?")],
                [("Quanto costa questi biglietti?", "Quanto costano questi biglietti?", "The verb agrees with the plural subject."),
                 ("Posso pagare con carta.", "Posso pagare con la carta.", "A means of payment keeps the article: con la carta, in contanti.")]),
              [D("Marco", "Quanto costa questa borsa?", "KWAHN-toh KOHS-tah KWES-tah BOR-sah?", "How much does this bag cost?"),
               D("Sofia", "Trentacinque euro.", "trehn-tah-CHEEN-kweh EH-oo-roh.", "Thirty-five euros."),
               D("Marco", "Posso pagare con la carta?", "POHS-soh pah-GAH-reh kohn lah KAR-tah?", "Can I pay by card?"),
               D("Sofia", "Certo. Ecco lo scontrino.", "CHER-toh. EK-koh loh skohn-TREE-noh.", "Of course. Here is the receipt.")],
              WS("Counter worksheet", [
                  T("Ask the price.", ["how much does this bag cost?", "can I pay by card?"],
                    ["Quanto costa questa borsa?", "Posso pagare con la carta?"]),
                  T("Close the purchase.", ["the receipt, please", "is it on offer?"],
                    ["Lo scontrino, per favore.", "È in offerta?"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Getting around Italy means validating your ticket before you get on: a ticket bought "
                 "at the tabaccheria and never stamped at the machine counts as no ticket at all, and "
                 "the fine is collected on the spot. The vocabulary of the half-step is therefore the "
                 "vocabulary of the platform — obliterare, convalidare, la corsa semplice, il capolinea "
                 "— because reading the machine is what keeps the day cheap."),
        source_url="https://en.wikipedia.org/wiki/Trenitalia",
        reading=("Un biglietto per il centro, per favore. Novanta centesimi. Devo convalidarlo? Sì, c'è "
                 "la macchinetta gialla all'ingresso. Grazie. Scendo alla terza fermata, vicino alla "
                 "piazza; poi vado a piedi fino in via Roma, sono cinque minuti. Il treno per casa è "
                 "alle otto e mezza in punto, quindi ho ancora mezz'ora."),
        reading_gloss=("A ticket to the centre, please. Ninety cents. Do I have to validate it? Yes, "
                       "there is the yellow machine at the entrance. Thanks. I get off at the third "
                       "stop, near the square; then I walk as far as Via Roma, it is five minutes. The "
                       "train home is at half past eight exactly, so I still have half an hour."),
        listening=("Marco: Scusi, dov'è la fermata dell'autobus?<br>Sofia: Sempre dritto, poi a destra, "
                   "davanti alla posta.<br>Marco: Grazie. Sa quando passa?<br>Sofia: Ogni dieci minuti."),
        listening_gloss=("Marco: Excuse me, where is the bus stop? Sofia: Straight ahead, then right, "
                         "opposite the post office. Marco: Thank you. Do you know when it comes? "
                         "Sofia: Every ten minutes."),
        voice_tag=VOICE,
        idioms=[
            ("A piedi", "on foot", "on foot, walking"),
            ("All'angolo", "at the corner", "on the corner"),
            ("In ritardo", "in delay", "late"),
            ("In anticipo", "in advance", "early"),
            ("Quanto costa?", "how much does it cost?", "how much is it?"),
            ("Dare una mano", "to give a hand", "to lend a hand"),
            ("Ci mancherebbe", "it would be missing", "of course, don't mention it"),
            ("Non ho capito", "I have not understood", "I did not catch that"),
            ("Più piano", "more slow", "more slowly, please"),
            ("Buona giornata", "good day", "have a good day"),
        ],
        mistakes=[
            ("Vado alla stazione a piedi per venti minuti.", "Vado alla stazione a piedi: venti minuti.", "A duration is stated with a colon or con, not with a second a."),
            ("Il biglietto costa novanta centesimi per il centro andata e ritorno.", "Un biglietto andata e ritorno per il centro costa novanta centesimi.", "Price sentences start with the thing priced."),
            ("Scendo alla fermata terza.", "Scendo alla terza fermata.", "Ordinals go before the noun: la terza fermata."),
        ],
        task_title="Direct a visitor from the station to your home",
        task_instructions=("Write eight Italian lines a visitor can follow from the station to your "
                           "front door: two directions (sempre dritto, a destra), one ticket or stop "
                           "question, one time (alle … in punto), and one landmark at the end (di "
                           "fronte a …). Hand it to someone who cannot ask you anything; the place "
                           "where they hesitate is the sentence that is missing a preposition."),
    ),
    "test": [
        ("translate_en", "Say: Where is the station, please?", "Dov'è la stazione, per favore?"),
        ("translate_it", "Vada sempre dritto, poi la seconda strada a sinistra.", "Go straight ahead, then the second street on the left."),
        ("multiple_choice", "Which is the polite request to a stranger?", "Può ripetere più piano?"),
        ("fill_in_the_blank", "Quanto ___ la corsa semplice?", "costa"),
        ("word_selection", "Select the Italian for 'half past eight'.", "le otto e mezza"),
        ("error_correction", "Abito a via Roma 12.", "Abito in via Roma 12."),
        ("dialogue_completion", "Complete: Devo convalidarlo? — ___ (yes, on the yellow machine)", "Sì, sulla macchinetta gialla"),
        ("matching", "Match davanti a to its meaning.", "in front of"),
        ("reading_comprehension", "Il treno parte alle nove in punto. What time does it leave?", "nine exactly"),
        ("inference", "«Ci mancherebbe» — what is the speaker doing?", "accepting a thank-you"),
        ("main_idea", "Lunedì lavoro, martedì sono libera, il fine settimana vado al mare. What is this about?", "the week's plans"),
        ("detail_identification", "Scendo alla terza fermata. Which stop?", "the third"),
    ],
}

HALFSTEPS["A2+"] = {
    "title": "Italian A2+ — Day-to-day business",
    "native": NATIVE,
    "goals": [
        "State your working hours, ask for a permission and offer the repair",
        "Answer the phone in an office and pass a call on",
        "Handle a counter visit: the queue, the bank, the pharmacy",
        "Keep small talk going on weather, weekends and coffee",
    ],
    "units": [
        {"id": "A2+-U1", "title": "In ufficio: orari e piccoli favori", "lessons": [
            L("L'orario di lavoro: entro alle nove, esco alle sei",
              "Two words keep a timetable honest: ENTO marks the latest moment, VERSO the "
              "approximate one. Entro alle nove e faccio la pausa verso l'una.",
              [V("l'orario", "loh-RAH-ryoh", "timetable, working hours", "noun"),
               V("la pausa", "lah POW-zah", "break", "noun"),
               V("il turno", "eel TOOR-noh", "shift", "noun"),
               V("uscire", "oo-SHEE-reh", "to go out, to leave", "verb"),
               V("entro", "EN-troh", "by, not later than", "preposition")],
              G("Working hours",
                "entro le nove · faccio la pausa verso l'una · il martedì esco alle sei",
                "Entro alle nove e faccio la pausa pranzo verso l'una; il martedì esco alle sei. "
                "Clock times take alle; entro and verso say how exact the hour is.",
                [X("Entro alle nove.", "EN-troh AHL-leh NOH-veh.", "I get in by nine."),
                 X("Faccio la pausa verso l'una.", "FAHT-choh lah POW-zah VER-soh LOO-nah.", "I take my break around one."),
                 X("Il martedì esco alle sei.", "eel mar-teh-DEE ES-koh AHL-leh SAY.", "On Tuesdays I leave at six.")],
                [("Devo essere a lavoro per le nove.", "Devo essere al lavoro entro le nove.", "The phrase is al lavoro, and the deadline is entro."),
                 ("Faccio pausa alle una.", "Faccio la pausa all'una.", "pausa takes the article; one o'clock is all'una.")]),
              [D("Sofia", "A che ora entri?", "ah keh OH-rah EN-tree?", "What time do you get in?"),
               D("Marco", "Entro alle nove, ma il lunedì c'è traffico.", "EN-troh AHL-leh NOH-veh, mah eel loo-neh-DEE cheh TRAHF-fee-koh.", "I get in by nine, but on Mondays there is traffic."),
               D("Sofia", "E la pausa?", "eh lah POW-zah?", "And the break?"),
               D("Marco", "Verso l'una, mezz'ora.", "VER-soh LOO-nah, med-DZOH-rah.", "Around one, half an hour.")],
              WS("Hours worksheet", [
                  T("State the timetable.", ["I get in by nine", "I take my break around one"],
                    ["Entro alle nove.", "Faccio la pausa verso l'una."]),
                  T("Talk about Tuesday.", ["on Tuesday I leave at six", "we start at eight"],
                    ["Il martedì esco alle sei.", "Cominciamo alle otto."]),
              ])),
            L("Chiedere un permesso: posso uscire prima?",
              "A permission request names the reason and the repair: POSSO USCIRE PRIMA? HO UN "
              "APPUNTAMENTO DAL MEDICO. RECUPERO DOMANI. That second sentence is what gets the yes.",
              [V("il permesso", "eel per-MES-soh", "permission, leave", "noun"),
               V("uscire prima", "oo-SHEE-reh PREE-mah", "to leave early", "phrase"),
               V("le ferie", "leh FEH-ryeh", "annual leave", "noun"),
               V("avvisare", "ahv-vee-ZAH-reh", "to let know, to notify", "verb"),
               V("recuperare", "reh-koo-peh-RAH-reh", "to make up (hours)", "verb")],
              G("Asking for leave",
                "posso uscire prima? · ho un appuntamento dal medico · recupero domani · avviso il capo",
                "Posso uscire prima oggi? Ho un appuntamento dal medico e recupero domani. The reason "
                "makes the request legitimate, the repair makes it easy to grant.",
                [X("Posso uscire prima oggi?", "POHS-soh oo-SHEE-reh PREE-mah OJ-jee?", "Can I leave early today?"),
                 X("Ho un appuntamento dal medico.", "oh oon ahp-poon-tah-MEN-toh dahl MEH-dee-koh.", "I have a doctor's appointment."),
                 X("Recupero domani e avviso il capo.", "reh-KOO-peh-roh doh-MAH-nee eh ahv-VEE-zoh eel KAH-poh.", "I will make it up tomorrow and let the boss know.")],
                [("Vado al medico, non vengo.", "Devo andare dal medico: posso uscire prima?", "A request, not an announcement, is what gets a yes."),
                 ("Prendo un giorno di vacanza per il medico.", "Prendo un giorno di permesso per andare dal medico.", "Short absences from work are permesso or ferie, not vacanza.")]),
              [D("Marco", "Posso uscire prima oggi?", "POHS-soh oo-SHEE-reh PREE-mah OJ-jee?", "Can I leave early today?"),
               D("Sofia", "Cosa succede?", "KOH-zah soot-CHEH-deh?", "What is going on?"),
               D("Marco", "Ho un appuntamento dal medico; recupero domani.", "oh oon ahp-poon-tah-MEN-toh dahl MEH-dee-koh; reh-KOO-peh-roh doh-MAH-nee.", "I have a doctor's appointment; I will make it up tomorrow."),
               D("Sofia", "Va bene, avvisa il capo.", "vah BEH-neh, ahv-VEE-zah eel KAH-poh.", "Fine, let the boss know.")],
              WS("Permission worksheet", [
                  T("Ask for permission.", ["can I leave early today?", "I have a doctor's appointment"],
                    ["Posso uscire prima oggi?", "Ho un appuntamento dal medico."]),
                  T("Offer the repair.", ["I will make up the hours tomorrow", "I will let the boss know"],
                    ["Recupero domani.", "Avviso il capo."]),
              ])),
            L("Al telefono in ufficio: pronto, chi parla?",
              "Office phone Italian is three formulas and a promise: PRONTO, UFFICIO VENDITE · CHI "
              "PARLA? · UN ATTIMO, GLIELO PASSO · LA RICHIAMO IO.",
              [V("pronto", "PROHN-toh", "hello (on the phone)", "interjection"),
               V("chi parla?", "kee PAR-lah?", "who is speaking?", "phrase"),
               V("un attimo", "oon AHT-tee-moh", "one moment", "phrase"),
               V("richiamare", "ree-kyah-MAH-reh", "to call back", "verb"),
               V("il messaggio", "eel mes-SAJ-joh", "message", "noun")],
              G("Phone frames",
                "pronto, ufficio vendite · chi parla? · un attimo, glielo passo · la richiamo io",
                "Pronto, ufficio vendite. Chi parla? Un attimo, glielo passo. Non c'è: la richiamo io "
                "nel pomeriggio. The office names itself first, then asks, then handles the absence.",
                [X("Pronto, ufficio vendite.", "PROHN-toh, oof-FEE-choh VEN-dee-teh.", "Hello, sales office."),
                 X("Un attimo, glielo passo.", "oon AHT-tee-moh, LYEH-loh PAHS-soh.", "One moment, I will put you through."),
                 X("Non c'è: la richiamo io nel pomeriggio.", "nohn cheh: lah ree-KYAH-moh EE-oh nel poh-meh-REEJ-joh.", "She is not in: I will call you back this afternoon.")],
                [("Sono io, Maria. (answering a business call)", "Sono Maria, dell'ufficio vendite.", "Business calls name the office, not only the person."),
                 ("Aspetta un attimo. (to a client)", "Un attimo, per favore.", "With a client there is no aspetta: the Lei form drops the imperative.")]),
              [D("Sofia", "Pronto, ufficio vendite.", "PROHN-toh, oof-FEE-choh VEN-dee-teh.", "Hello, sales office."),
               D("Marco", "Buongiorno, sono Marco Bianchi. Posso parlare con la dottoressa Rossi?", "bwohn-JOR-noh, SOH-noh MAR-koh BYAHN-kee. POHS-soh par-LAH-reh kohn lah dot-toh-RES-sah ROS-see?", "Good morning, I am Marco Bianchi. Can I speak to Doctor Rossi?"),
               D("Sofia", "Un attimo, gliela passo.", "oon AHT-tee-moh, LYEH-lah PAHS-soh.", "One moment, I will put you through."),
               D("Marco", "Grazie mille.", "GRAH-tsyeh MEEL-leh.", "Thank you very much.")],
              WS("Phone worksheet", [
                  T("Answer the phone.", ["sales office, hello", "who is speaking?"],
                    ["Pronto, ufficio vendite.", "Chi parla?"]),
                  T("Handle the absence.", ["she is not in, I will call you back", "one moment, I will put you through"],
                    ["Non c'è, la richiamo io.", "Un attimo, glielo passo."]),
              ])),
        ]},
        {"id": "A2+-U2", "title": "Piccole conversazioni", "lessons": [
            L("Come va? Risposte brevi e vere",
              "Small talk answers are graded and short: NON C'È MALE · COSÌ COSÌ · TUTTO BENE. The "
              "honest middle answer is the one that invites the next question.",
              [V("come va?", "KOH-meh vah?", "how is it going?", "phrase"),
               V("così così", "koh-ZEE koh-ZEE", "so-so", "phrase"),
               V("alla grande", "AHL-lah GRAHN-deh", "great", "phrase"),
               V("d'accordo", "dahk-KOR-doh", "agreed, all right", "phrase"),
               V("la settimana pesante", "lah set-tee-MAH-nah peh-ZAHN-teh", "a heavy week", "phrase")],
              G("Greeting frames",
                "come va? · non c'è male · così così · tutto bene, e tu?",
                "Come va? Non c'è male, e tu? Così così: settimana pesante. One answer, one question "
                "back — that is the whole machinery of Italian small talk.",
                [X("Come va? — Non c'è male.", "KOH-meh vah? — nohn cheh MAH-leh.", "How is it going? — Not bad."),
                 X("Così così: settimana pesante.", "koh-ZEE koh-ZEE: set-tee-MAH-nah peh-ZAHN-teh.", "So-so: a heavy week."),
                 X("Tutto bene, grazie, e tu?", "TOOT-toh BEH-neh, GRAH-tsyeh, eh too?", "All good, thanks, and you?")],
                [("Come stai? — Bene, grazie, e Lei? (to a colleague in your own office)", "Come va? — Bene, e tu?", "Colleagues in the same office use tu; a Lei would build a wall."),
                 ("Come va? — Sì.", "Come va? — Non c'è male.", "come va asks for a state, not a yes.")]),
              [D("Marco", "Ciao Sofia, come va?", "CHAH-oh SOH-fyah, KOH-meh vah?", "Hi Sofia, how is it going?"),
               D("Sofia", "Così così, settimana pesante.", "koh-ZEE koh-ZEE, set-tee-MAH-nah peh-ZAHN-teh.", "So-so, a heavy week."),
               D("Marco", "Mi dispiace. Caffè?", "mee dee-SPYAH-cheh. kahf-FEH?", "Sorry to hear it. Coffee?"),
               D("Sofia", "Volentieri, così respiriamo.", "voh-len-TYEH-ree, koh-ZEE reh-spee-RYAH-moh.", "Gladly, we can breathe for a minute.")],
              WS("Greeting worksheet", [
                  T("Answer the greeting.", ["not bad", "so-so, heavy week"],
                    ["Non c'è male.", "Così così: settimana pesante."]),
                  T("Invite for coffee.", ["coffee? my treat", "let us take five minutes"],
                    ["Caffè? Offro io.", "Ci prendiamo cinque minuti."]),
              ])),
            L("Che tempo fa? Parlare del tempo senza imbarazzo",
              "Weather is the safest small talk in Italian because it takes impersonal verbs and asks "
              "for no opinion: PIOVE DA TRE GIORNI · FA CALDO · SECONDO LA PREVISIONE, DOMANI C'È IL SOLE.",
              [V("che tempo fa?", "keh TEM-poh fah?", "what is the weather like?", "phrase"),
               V("piove", "PYOH-veh", "it is raining", "verb"),
               V("c'è il sole", "cheh eel SOH-leh", "the sun is out", "phrase"),
               V("fa caldo", "fah KAHL-doh", "it is hot", "phrase"),
               V("la previsione", "lah preh-vee-ZYOH-neh", "forecast", "noun")],
              G("Weather frames",
                "che tempo fa? · piove da tre giorni · fa caldo · secondo la previsione",
                "Che tempo fa da voi? Piove da tre giorni e fa freddo. Secondo la previsione, domani "
                "c'è il sole. Impersonal verbs take no subject, which is why the topic never runs dry.",
                [X("Che tempo fa?", "keh TEM-poh fah?", "What is the weather like?"),
                 X("Piove da tre giorni.", "PYOH-veh dah treh JOR-nee.", "It has been raining for three days."),
                 X("Fa caldo per essere ottobre.", "fah KAHL-doh per ES-seh-reh ot-TOH-breh.", "It is hot for October.")],
                [("È piovendo.", "Sta piovendo.", "Italian uses stare + gerundio for what is happening right now."),
                 ("Fa sole.", "C'è il sole.", "Sunshine is c'è il sole; fa belongs to caldo, freddo, bel tempo.")]),
              [D("Sofia", "Che tempo fa a Milano?", "keh TEM-poh fah ah mee-LAH-noh?", "What is the weather like in Milan?"),
               D("Marco", "Piove da tre giorni.", "PYOH-veh dah treh JOR-nee.", "It has been raining for three days."),
               D("Sofia", "Qui invece c'è il sole.", "kwee een-VEH-cheh cheh eel SOH-leh.", "Here, on the other hand, the sun is out."),
               D("Marco", "Secondo la previsione, domani cambia.", "seh-KOHN-doh lah preh-vee-ZYOH-neh, doh-MAH-nee KAHM-byah.", "According to the forecast, tomorrow it changes.")],
              WS("Weather worksheet", [
                  T("Describe the weather.", ["it is raining", "it is hot for October"],
                    ["Piove.", "Fa caldo per essere ottobre."]),
                  T("Use the forecast.", ["according to the forecast, tomorrow it improves", "the sun is out"],
                    ["Secondo la previsione, domani migliora.", "C'è il sole."]),
              ])),
            L("Il fine settimana: cosa hai fatto?",
              "One past-tense answer carries two auxiliaries and one agreement: SONO ANDATA IN "
              "PALESTRA, POI HO VISTO LA PARTITA. Movement takes essere; everything you watch takes avere.",
              [V("il tempo libero", "eel TEM-poh LEE-beh-roh", "free time", "noun"),
               V("fare una passeggiata", "FAH-reh OO-nah pahs-seh-JAH-tah", "to take a walk", "phrase"),
               V("la palestra", "lah pah-LES-trah", "gym", "noun"),
               V("la partita", "lah par-TEE-tah", "match, game", "noun"),
               V("riposare", "ree-poh-ZAH-reh", "to rest", "verb")],
              G("Weekend frames",
                "cosa hai fatto? · sono andata in palestra · ho visto la partita · ho riposato",
                "Cosa hai fatto nel fine settimana? Sono andata in palestra, poi ho visto la partita "
                "e ho riposato. andare takes essere and agrees; vedere and riposare take avere.",
                [X("Cosa hai fatto nel fine settimana?", "KOH-zah ahy FAHT-toh nel FEE-neh set-tee-MAH-nah?", "What did you do at the weekend?"),
                 X("Sono andata in palestra.", "SOH-noh ahn-DAH-tah een pah-LES-trah.", "I went to the gym."),
                 X("Ho visto la partita con mio fratello.", "oh VEES-toh lah par-TEE-tah kohn MEE-oh frah-TEL-loh.", "I watched the match with my brother.")],
                [("Ho andato in palestra.", "Sono andata in palestra.", "Movement verbs like andare take essere and agree with the subject."),
                 ("Ho visitato la partita.", "Ho visto la partita.", "Matches and films are visti, not visitati.")]),
              [D("Marco", "Cosa hai fatto nel fine settimana?", "KOH-zah ahy FAHT-toh nel FEE-neh set-tee-MAH-nah?", "What did you do at the weekend?"),
               D("Sofia", "Sono andata in palestra sabato, poi ho riposato.", "SOH-noh ahn-DAH-tah een pah-LES-trah SAH-bah-toh, pohy oh ree-poh-ZAH-toh.", "I went to the gym on Saturday, then I rested."),
               D("Marco", "Io ho visto la partita.", "EE-oh oh VEES-toh lah par-TEE-tah.", "I watched the match."),
               D("Sofia", "Chi ha vinto?", "kee ah VEEN-toh?", "Who won?")],
              WS("Weekend worksheet", [
                  T("Report the weekend.", ["I went to the gym", "I watched the match"],
                    ["Sono andata in palestra.", "Ho visto la partita."]),
                  T("Ask back.", ["what did you do?", "who won?"],
                    ["Cosa hai fatto?", "Chi ha vinto?"]),
              ])),
        ]},
        {"id": "A2+-U3", "title": "Servizi: posta, banca, farmacia", "lessons": [
            L("Allo sportello: fare la fila, prendere il numero",
              "Service Italian is queue Italian: PRENDO IL NUMERO, ASPETTO IL MIO TURNO, ALLO "
              "SPORTELLO TRE C'È MENO FILA. Number, turn, counter — in that order.",
              [V("lo sportello", "loh spor-TEL-loh", "counter, window", "noun"),
               V("la fila", "lah FEE-lah", "queue", "noun"),
               V("il turno", "eel TOOR-noh", "turn (in a queue)", "noun"),
               V("attendere", "aht-TEN-deh-reh", "to wait", "verb"),
               V("spedire", "speh-DEE-reh", "to send", "verb")],
              G("Counter frames",
                "prendo il numero · aspetto il mio turno · allo sportello tre c'è meno fila",
                "Prendo il numero e aspetto il mio turno: allo sportello tre c'è meno fila. The "
                "counter takes allo, and aspettare takes its object directly.",
                [X("Prendo il numero.", "PREN-doh eel NOO-meh-roh.", "I take a number."),
                 X("Aspetto il mio turno.", "ahs-PET-toh eel MEE-oh TOOR-noh.", "I wait my turn."),
                 X("Allo sportello tre c'è meno fila.", "AHL-loh spor-TEL-loh treh cheh MEH-noh FEE-lah.", "There is less queue at counter three.")],
                [("Faccio la fila al sportello.", "Faccio la fila allo sportello.", "sportello takes allo (a + lo)."),
                 ("Aspetto per il mio turno.", "Aspetto il mio turno.", "aspettare is transitive: no preposition.")]),
              [D("Sofia", "Devo spedire un pacco.", "DEH-voh speh-DEE-reh oon PAHK-koh.", "I have to send a parcel."),
               D("Marco", "Prendi il numero e aspetta il turno.", "PREN-dee eel NOO-meh-roh eh ahs-PET-tah eel TOOR-noh.", "Take a number and wait your turn."),
               D("Sofia", "Quanta fila c'è?", "KWAHN-tah FEE-lah cheh?", "How long is the queue?"),
               D("Marco", "Allo sportello tre, pochissima.", "AHL-loh spor-TEL-loh treh, poh-KEES-see-mah.", "At counter three, hardly any.")],
              WS("Counter worksheet", [
                  T("Handle the queue.", ["I take a number", "there is less queue at counter three"],
                    ["Prendo il numero.", "Allo sportello tre c'è meno fila."]),
                  T("State the errand.", ["I have to send a parcel", "I have to pay in cash"],
                    ["Devo spedire un pacco.", "Devo pagare in contanti."]),
              ])),
            L("In banca: aprire un conto e il bancomat",
              "Bank Italian starts in the conditional and turns factual afterwards: VORREI APRIRE UN "
              "CONTO · SERVE UN DOCUMENTO · FACCIO UN PRELIEVO · IL BONIFICO ARRIVA DOMANI.",
              [V("il conto", "eel KOHN-toh", "account", "noun"),
               V("il bancomat", "eel BAHN-koh-maht", "ATM, debit card", "noun"),
               V("il prelievo", "eel preh-LYEH-voh", "withdrawal", "noun"),
               V("il bonifico", "eel boh-NEE-fee-koh", "bank transfer", "noun"),
               V("la carta d'identità", "lah KAR-tah dee-den-tee-TAH", "ID card", "noun")],
              G("Bank frames",
                "vorrei aprire un conto · serve un documento e il codice fiscale · faccio un prelievo · il bonifico arriva domani",
                "Vorrei aprire un conto. Serve un documento e il codice fiscale. Faccio un prelievo "
                "al bancomat e il bonifico arriva domani. vorrei opens; the rest is plain present.",
                [X("Vorrei aprire un conto.", "vor-RAY ah-PREE-reh oon KOHN-toh.", "I would like to open an account."),
                 X("Faccio un prelievo al bancomat.", "FAHT-choh oon preh-LYEH-voh ahl BAHN-koh-maht.", "I make a withdrawal at the ATM."),
                 X("Il bonifico arriva domani.", "eel boh-NEE-fee-koh ahr-REE-vah doh-MAH-nee.", "The transfer arrives tomorrow.")],
                [("Voglio aprire un conto. (at the counter)", "Vorrei aprire un conto.", "vorrei is the polite form; voglio states a demand."),
                 ("Il bonifico si arriva domani.", "Il bonifico arriva domani.", "arrivare is not reflexive.")]),
              [D("Marco", "Vorrei aprire un conto.", "vor-RAY ah-PREE-reh oon KOHN-toh.", "I would like to open an account."),
               D("Sofia", "Serve un documento e il codice fiscale.", "SER-veh oon doh-koo-MEN-toh eh eel KOH-dee-cheh fees-KAH-leh.", "An ID document and the tax code are needed."),
               D("Marco", "Ho la carta d'identità.", "oh lah KAR-tah dee-den-tee-TAH.", "I have my ID card."),
               D("Sofia", "Perfetto, si accomodi allo sportello due.", "per-FET-toh, see ahk-KOH-moh-dee AHL-loh spor-TEL-loh DOO-eh.", "Perfect, please go to counter two.")],
              WS("Bank worksheet", [
                  T("Ask at the bank.", ["I would like to open an account", "I have to make a transfer"],
                    ["Vorrei aprire un conto.", "Devo fare un bonifico."]),
                  T("Say what you need.", ["an ID document and the tax code", "a withdrawal at the ATM"],
                    ["un documento e il codice fiscale", "un prelievo al bancomat"]),
              ])),
            L("In farmacia: un sintomo, un rimedio",
              "A pharmacy visit names the symptom first and asks about the prescription second: HO MAL "
              "DI TESTA DA IERI · SERVE LA RICETTA? · DUE COMPRESSE AL GIORNO, DOPO I PASTI.",
              [V("la ricetta", "lah ree-CHET-tah", "prescription", "noun"),
               V("il sintomo", "eel SEEN-toh-moh", "symptom", "noun"),
               V("il mal di testa", "eel mahl dee TES-tah", "headache", "noun"),
               V("la compressa", "lah kohm-PRES-sah", "tablet", "noun"),
               V("la posologia", "lah poh-zoh-loh-JEE-ah", "dosage", "noun")],
              G("Pharmacy frames",
                "ho mal di testa da ieri · serve la ricetta? · due compresse al giorno, dopo i pasti",
                "Ho mal di testa da ieri. Ha qualcosa senza ricetta? Sì: due compresse al giorno, dopo "
                "i pasti. The symptom arrives with da + time; the dose with al giorno.",
                [X("Ho mal di testa da ieri.", "oh mahl dee TES-tah dah YEH-ree.", "I have had a headache since yesterday."),
                 X("Serve la ricetta?", "SER-veh lah ree-CHET-tah?", "Is a prescription needed?"),
                 X("Due compresse al giorno, dopo i pasti.", "DOO-eh kohm-PRES-seh ahl JOR-noh, DOH-poh ee PAHS-tee.", "Two tablets a day, after meals.")],
                [("Ho dolore di testa.", "Ho mal di testa.", "The fixed phrase is mal di testa."),
                 ("Prendo una compressa per due volte al giorno.", "Prendo una compressa due volte al giorno.", "Frequency takes no per: due volte al giorno.")]),
              [D("Sofia", "Buongiorno, ho mal di testa da ieri.", "bwohn-JOR-noh, oh mahl dee TES-tah dah YEH-ree.", "Good morning, I have had a headache since yesterday."),
               D("Marco", "Ha allergie?", "ah ahl-ler-JEE-eh?", "Do you have allergies?"),
               D("Sofia", "No. Serve la ricetta?", "noh. SER-veh lah ree-CHET-tah?", "No. Is a prescription needed?"),
               D("Marco", "No, è senza ricetta: due compresse al giorno.", "noh, eh SEN-tsah ree-CHET-tah: DOO-eh kohm-PRES-seh ahl JOR-noh.", "No, it is over the counter: two tablets a day.")],
              WS("Pharmacy worksheet", [
                  T("Name the symptom.", ["I have had a headache since yesterday", "does it need a prescription?"],
                    ["Ho mal di testa da ieri.", "Serve la ricetta?"]),
                  T("Repeat the dose.", ["two tablets a day", "after meals"],
                    ["due compresse al giorno", "dopo i pasti"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Italian working life runs on two institutions the half-step has to teach: the caffè "
                 "al bar, taken standing at the counter in three minutes and paid for after drinking, "
                 "and the pausa pranzo, which is a real break rather than a sandwich at the desk. "
                 "Small talk is not optional here — it is how a colleague becomes someone who will "
                 "cover your shift, and the phrases are short, graded and exchanged every morning."),
        source_url="https://en.wikipedia.org/wiki/Small_talk",
        reading=("Ciao Sofia, come va? Così così: settimana pesante, entro alle otto e il martedì esco "
                 "alle sei. Faccio la pausa verso l'una e prendiamo un caffè al bar. Poi devo passare "
                 "in banca: vorrei aprire un conto e fare un bonifico. In farmacia, invece, ho preso "
                 "due compresse per il mal di testa: niente ricetta, per fortuna. Sabato sono andata "
                 "in palestra e domenica ho riposato."),
        reading_gloss=("Hi Sofia, how is it going? So-so: a heavy week, I get in by eight and on "
                       "Tuesdays I leave at six. I take my break around one and we have a coffee at "
                       "the bar. Then I have to stop at the bank: I would like to open an account and "
                       "make a transfer. At the pharmacy, on the other hand, I got two tablets for the "
                       "headache: no prescription, luckily. On Saturday I went to the gym and on "
                       "Sunday I rested."),
        listening=("Sofia: Pronto, ufficio vendite.<br>Marco: Buongiorno, sono Marco Bianchi. Posso "
                   "parlare con la dottoressa Rossi?<br>Sofia: Non c'è: la richiamo io nel "
                   "pomeriggio.<br>Marco: Grazie, arrivederci."),
        listening_gloss=("Sofia: Hello, sales office. Marco: Good morning, I am Marco Bianchi. Can I "
                         "speak to Doctor Rossi? Sofia: She is not in: I will call you back this "
                         "afternoon. Marco: Thank you, goodbye."),
        voice_tag=VOICE,
        idioms=[
            ("Non c'è male", "there is no bad", "not bad at all"),
            ("Così così", "so so", "so-so"),
            ("Alla grande", "at the big", "great, brilliantly"),
            ("Fare la fila", "to make the queue", "to queue up"),
            ("Prendere il numero", "to take the number", "to take a ticket"),
            ("Caffè al bar", "coffee at the bar", "a quick espresso standing up"),
            ("Pausa pranzo", "lunch break", "lunch break"),
            ("Mal di testa", "headache", "headache"),
            ("Senza ricetta", "without prescription", "over the counter"),
            ("Due volte al giorno", "twice a day", "twice daily"),
        ],
        mistakes=[
            ("Sono andato a la palestra.", "Sono andato in palestra.", "Sports venues take in: in palestra, never a la palestra."),
            ("Ho mal di testa da tre ore fa.", "Ho mal di testa da tre ore.", "da takes a plain duration; fa is not added."),
            ("Faccio un prelievo dal bancomat alla banca.", "Faccio un prelievo al bancomat.", "One location is enough: al bancomat."),
        ],
        task_title="Script a working day in Italian",
        task_instructions=("Write ten lines of your own working day: what time you get in (entro), one "
                           "small favour you ask for and how you repair it (recupero …), one office "
                           "phone exchange (chi parla?), one counter visit (prendo il numero) and one "
                           "small-talk exchange (come va?). Read it out loud twice: the first time "
                           "for the phrases, the second for the tone, because the graded answer is "
                           "what an Italian colleague is listening for."),
    ),
    "test": [
        ("translate_en", "Say: Can I leave early today?", "Posso uscire prima oggi?"),
        ("translate_it", "Entro alle nove e faccio la pausa verso l'una.", "I get in by nine and take my break around one."),
        ("multiple_choice", "Which is the polite bank opening?", "Vorrei aprire un conto."),
        ("fill_in_the_blank", "Aspetto ___ mio turno allo sportello tre.", "il"),
        ("word_selection", "Select the Italian for 'it has been raining for three days'.", "piove da tre giorni"),
        ("error_correction", "Ho andato in palestra sabato.", "Sono andata in palestra sabato."),
        ("dialogue_completion", "Complete: Pronto, ufficio vendite. — ___ (who is speaking?)", "Chi parla?"),
        ("matching", "Match senza ricetta to its meaning.", "over the counter"),
        ("reading_comprehension", "Il bonifico arriva domani. When does the transfer arrive?", "tomorrow"),
        ("inference", "«Così così, settimana pesante» — what is the speaker doing?", "answering small talk honestly"),
        ("main_idea", "Prendi il numero e aspetta il turno. What is this about?", "queueing at a counter"),
        ("detail_identification", "Due compresse al giorno. How many tablets per day?", "two"),
    ],
}

HALFSTEPS["B1+"] = {
    "title": "Italian B1+ — Work and opinions",
    "native": NATIVE,
    "goals": [
        "Run through an agenda, take the floor and summarise what was decided",
        "Give an opinion, agree with a reservation and disagree without a scene",
        "Describe a project: goal, deadline and the risk that keeps it honest",
    ],
    "units": [
        {"id": "B1+-U1", "title": "Riunioni e parole", "lessons": [
            L("L'ordine del giorno e la parola",
              "A meeting has a script: L'ORDINE DEL GIORNO · POSSO INTERVENIRE? · METTIAMO AI VOTI. "
              "Naming the step you are on is what keeps five people in one conversation.",
              [V("l'ordine del giorno", "LOR-dee-neh del JOR-noh", "the agenda", "noun"),
               V("cedere la parola", "CHEH-deh-reh lah pah-ROH-lah", "to give the floor", "phrase"),
               V("intervenire", "een-ter-veh-NEE-reh", "to step in, to speak", "verb"),
               V("mettere ai voti", "met-TEH-reh ahy VOH-tee", "to put to the vote", "phrase"),
               V("il verbale", "eel ver-BAH-leh", "the minutes", "noun")],
              G("Meeting frames",
                "l'ordine del giorno · posso intervenire? · passiamo al punto due · mettiamo ai voti",
                "Prima di tutto l'ordine del giorno: tre punti. Posso intervenire sul secondo? "
                "Passiamo al punto due e poi mettiamo ai voti. Each phrase names the step, which is "
                "why the meeting does not need a chair to shout.",
                [X("Prima di tutto, l'ordine del giorno.", "PREE-mah dee TOOT-toh, LOR-dee-neh del JOR-noh.", "First of all, the agenda."),
                 X("Posso intervenire sul secondo punto?", "POHS-soh een-ter-veh-NEE-reh sool seh-KOHN-doh POON-toh?", "May I speak on the second point?"),
                 X("Mettiamo ai voti.", "met-TYAH-moh ahy VOH-tee.", "Let us put it to the vote.")],
                [("Ho un intervento per il secondo punto.", "Posso intervenire sul secondo punto?", "A request for the floor is a question, not a declaration."),
                 ("Facciamo i voti.", "Mettiamo ai voti.", "The fixed phrase is mettere ai voti.")]),
              [D("Sofia", "Prima di tutto, l'ordine del giorno: tre punti.", "PREE-mah dee TOOT-toh, LOR-dee-neh del JOR-noh: treh POON-tee.", "First of all, the agenda: three points."),
               D("Marco", "Posso intervenire sul secondo?", "POHS-soh een-ter-veh-NEE-reh sool seh-KOHN-doh?", "May I speak on the second one?"),
               D("Sofia", "Certo. Poi passiamo al terzo.", "CHER-toh. pohy pahs-SYAH-moh ahl TER-tsoh.", "Of course. Then we move to the third."),
               D("Marco", "Sul terzo direi di mettere ai voti.", "sool TER-tsoh dee-RAY dee met-TEH-reh ahy VOH-tee.", "On the third I would say we put it to the vote.")],
              WS("Meeting worksheet", [
                  T("Run the meeting.", ["the agenda has three points", "may I speak on the second?"],
                    ["L'ordine del giorno ha tre punti.", "Posso intervenire sul secondo?"]),
                  T("Close the point.", ["let us put it to the vote", "let us move to the third point"],
                    ["Mettiamo ai voti.", "Passiamo al terzo punto."]),
              ])),
            L("Scrivere il verbale: noi abbiamo deciso",
              "Minutes speak in the plural and in the passive: ABBIAMO DECISO · È STATO CONVENUTO · "
              "RESTA IN SOSPESO · LA SCADENZA È FISSATA AL … Each line is a decision with a date.",
              [V("decidere", "deh-CHEE-deh-reh", "to decide", "verb"),
               V("convenire", "kohn-veh-NEE-reh", "to be agreed", "verb"),
               V("restare in sospeso", "res-TAH-reh een sohs-PEH-zoh", "to remain open", "phrase"),
               V("la scadenza", "lah skah-DEN-tsah", "deadline", "noun"),
               V("il punto aperto", "eel POON-toh ah-PER-toh", "open item", "noun")],
              G("Minutes frames",
                "abbiamo deciso di … · è stato convenuto che … · resta in sospeso … · la scadenza è fissata al …",
                "Abbiamo deciso di rinviare il lancio. È stato convenuto che Sofia coordina il "
                "progetto. La scadenza è fissata al 30 giugno; il budget resta in sospeso. If a line "
                "has no decision and no date, it belongs in the open items.",
                [X("Abbiamo deciso di rinviare il lancio.", "ahb-BYAH-moh deh-CHEE-zoh dee reen-VYAH-reh eel LAHN-choh.", "We decided to postpone the launch."),
                 X("La scadenza è fissata al 30 giugno.", "lah skah-DEN-tsah eh fees-SAH-tah ahl TREHN-tah JOO-nyoh.", "The deadline is set for 30 June."),
                 X("Il budget resta in sospeso.", "eel BOOJ-jet RES-tah een sohs-PEH-zoh.", "The budget remains open.")],
                [("Si è deciso che forse rinviamo il lancio.", "Abbiamo deciso di rinviare il lancio.", "Minutes record decisions, not hesitations; forse never reaches the page."),
                 ("La scadenza è fissata a 30 giugno.", "La scadenza è fissata al 30 giugno.", "A date takes al (a + il): al 30 giugno.")]),
              [D("Marco", "Hai scritto il verbale?", "ahy SKREET-toh eel ver-BAH-leh?", "Did you write the minutes?"),
               D("Sofia", "Sì: «abbiamo deciso», «è stato convenuto», «resta in sospeso».", "see: ahb-BYAH-moh deh-CHEE-zoh, eh STAH-toh kohn-veh-NOO-toh, RES-tah een sohs-PEH-zoh.", "Yes: 'we decided', 'it was agreed', 'remains open'."),
               D("Marco", "E la scadenza?", "eh lah skah-DEN-tsah?", "And the deadline?"),
               D("Sofia", "«È fissata al 30 giugno.»", "eh fees-SAH-tah ahl TREHN-tah JOO-nyoh.", "'It is set for 30 June.'")],
              WS("Minutes worksheet", [
                  T("Write the decisions.", ["we decided to postpone the launch", "the deadline is set for 30 June"],
                    ["Abbiamo deciso di rinviare il lancio.", "La scadenza è fissata al 30 giugno."]),
                  T("List what is open.", ["the budget remains open", "we decide on Tuesday"],
                    ["Il budget resta in sospeso.", "Decidiamo martedì."]),
              ])),
            L("Parlare del proprio lavoro: mi occupo di",
              "Describing your job takes mi occupo di + noun and lavoro su + project: MI OCCUPO DELLE "
              "CONSEGNE, LAVORO SU UN PROGETTO NUOVO. The verb is reflexive; the field takes di.",
              [V("occuparsi di", "oh-koo-PAR-see dee", "to deal with", "verb"),
               V("lavorare su", "lah-voh-RAH-reh soo", "to work on", "phrase"),
               V("il settore", "eel set-TOH-reh", "sector", "noun"),
               V("il ruolo", "eel RWOH-loh", "role", "noun"),
               V("il reparto", "eel reh-PAR-toh", "department", "noun")],
              G("Job description",
                "mi occupo di … · lavoro su … · nel reparto … · il mio ruolo è …",
                "Mi occupo delle consegne e lavoro su un progetto di digitalizzazione nel reparto "
                "logistica. occuparsi takes di; lavorare su names the project, not the company.",
                [X("Mi occupo delle consegne.", "mee OH-koo-poh DEL-leh kohn-SEH-nyeh.", "I deal with deliveries."),
                 X("Lavoro su un progetto nuovo.", "lah-VOH-roh soo oon proh-JET-toh NWOH-voh.", "I am working on a new project."),
                 X("Il mio ruolo è coordinare il reparto.", "eel MEE-oh RWOH-loh eh koh-or-dee-NAH-reh eel reh-PAR-toh.", "My role is to coordinate the department.")],
                [("Mi occupo le consegne.", "Mi occupo delle consegne.", "occuparsi takes di + article: delle consegne."),
                 ("Lavoro per un progetto nuovo.", "Lavoro su un progetto nuovo.", "Projects take su: lavorare su.")]),
              [D("Marco", "Di cosa ti occupi?", "dee KOH-zah tee oh-KOO-pee?", "What do you deal with?"),
               D("Sofia", "Mi occupo delle consegne e lavoro su un progetto nuovo.", "mee OH-koo-poh DEL-leh kohn-SEH-nyeh eh lah-VOH-roh soo oon proh-JET-toh NWOH-voh.", "I deal with deliveries and I am working on a new project."),
               D("Marco", "In quale reparto?", "een KWAH-leh reh-PAR-toh?", "In which department?"),
               D("Sofia", "Nel reparto logistica, con due colleghi.", "nel reh-PAR-toh loh-JEES-tee-kah, kohn DOO-eh kohl-LEH-ghee.", "In the logistics department, with two colleagues.")],
              WS("Role worksheet", [
                  T("Describe the job.", ["I deal with deliveries", "I am working on a new project"],
                    ["Mi occupo delle consegne.", "Lavoro su un progetto nuovo."]),
                  T("Name the place.", ["in the logistics department", "my role is to coordinate"],
                    ["nel reparto logistica", "il mio ruolo è coordinare"]),
              ])),
        ]},
        {"id": "B1+-U2", "title": "Pareri e disaccordi", "lessons": [
            L("Esprimere un parere: secondo me",
              "An opinion arrives with a frame: SECONDO ME · DAL MIO PUNTO DI VISTA · MI SEMBRA CHE + "
              "congiuntivo. The frame is what turns a claim into something a colleague can answer.",
              [V("secondo me", "seh-KOHN-doh meh", "in my opinion", "phrase"),
               V("dal mio punto di vista", "dahl MEE-oh POON-toh dee VEES-tah", "from my point of view", "phrase"),
               V("mi sembra che", "mee SEM-brah keh", "it seems to me that", "phrase"),
               V("la proposta", "lah proh-POHS-tah", "proposal", "noun"),
               V("il dubbio", "eel DOOB-byoh", "doubt", "noun")],
              G("Opinion frames",
                "secondo me · dal mio punto di vista · mi sembra che sia … · ho un dubbio su …",
                "Secondo me la proposta regge. Dal mio punto di vista manca un dato. Mi sembra che "
                "il piano sia ambizioso. The frame takes the sting out: the claim becomes one view "
                "among several, which is exactly what invites an answer.",
                [X("Secondo me la proposta regge.", "seh-KOHN-doh meh lah proh-POHS-tah RED-jeh.", "In my opinion the proposal holds."),
                 X("Dal mio punto di vista manca un dato.", "dahl MEE-oh POON-toh dee VEES-tah MAHN-kah oon DAH-toh.", "From my point of view a figure is missing."),
                 X("Mi sembra che il piano sia ambizioso.", "mee SEM-brah keh eel PYAH-noh SEE-ah ahm-beets-YOH-zoh.", "It seems to me that the plan is ambitious.")],
                [("Secondo me che la proposta regge.", "Secondo me la proposta regge.", "secondo me is already a frame: no che after it."),
                 ("Mi sembra che il piano è ambizioso.", "Mi sembra che il piano sia ambizioso.", "mi sembra che takes the congiuntivo.")]),
              [D("Sofia", "Secondo me la proposta regge.", "seh-KOHN-doh meh lah proh-POHS-tah RED-jeh.", "In my opinion the proposal holds."),
               D("Marco", "Dal mio punto di vista manca un dato.", "dahl MEE-oh POON-toh dee VEES-tah MAHN-kah oon DAH-toh.", "From my point of view a figure is missing."),
               D("Sofia", "Quale dato?", "KWAH-leh DAH-toh?", "Which figure?"),
               D("Marco", "I costi: mi sembra che il piano sia ambizioso.", "ee KOHS-tee: mee SEM-brah keh eel PYAH-noh SEE-ah ahm-beets-YOH-zoh.", "The costs: it seems to me the plan is ambitious.")],
              WS("Opinion worksheet", [
                  T("Give an opinion.", ["in my opinion the proposal holds", "a figure is missing"],
                    ["Secondo me la proposta regge.", "Manca un dato."]),
                  T("Frame the doubt.", ["from my point of view", "it seems to me that the plan is ambitious"],
                    ["Dal mio punto di vista,", "Mi sembra che il piano sia ambizioso."]),
              ])),
            L("Essere d'accordo — e non esserlo",
              "Agreement and disagreement are both graded: SONO D'ACCORDO · D'ACCORDO, MA … · NON "
              "SONO CONVINTO · SU QUESTO NON POSSO ESSERE D'ACCORDO. The middle forms keep the room open.",
              [V("sono d'accordo", "SOH-noh dahk-KOR-doh", "I agree", "phrase"),
               V("non sono convinto", "nohn SOH-noh kohn-VEEN-toh", "I am not convinced", "phrase"),
               V("il compromesso", "eel kohm-proh-MES-soh", "compromise", "noun"),
               V("la riserva", "lah ree-ZER-vah", "reservation, caveat", "noun"),
               V("su questo punto", "soo KWES-toh POON-toh", "on this point", "phrase")],
              G("Agreement frame",
                "sono d'accordo · d'accordo, ma … · non sono convinto · su questo punto, no",
                "Sono d'accordo sulla prima parte. D'accordo, ma il tempo è poco. Su questo punto "
                "non sono convinto: preferisco una prova. Disagreement in Italian likes a named point "
                "and a proposal attached to it.",
                [X("Sono d'accordo sulla prima parte.", "SOH-noh dahk-KOR-doh SOOL-lah PREE-mah PAR-teh.", "I agree on the first part."),
                 X("D'accordo, ma il tempo è poco.", "dahk-KOR-doh, mah eel TEM-poh eh POH-koh.", "Agreed, but there is little time."),
                 X("Su questo punto non sono convinto.", "soo KWES-toh POON-toh nohn SOH-noh kohn-VEEN-toh.", "On this point I am not convinced.")],
                [("Sono d'accordo con la prima parte.", "Sono d'accordo sulla prima parte.", "Agreement on a topic takes su: d'accordo su."),
                 ("Non sono d'accordo, punto.", "Su questo punto non sono convinto.", "A named point plus a proposal keeps the disagreement workable.")]),
              [D("Marco", "Allora, approviamo il piano?", "ahl-LOH-rah, ahp-proh-VYAH-moh eel PYAH-noh?", "So, do we approve the plan?"),
               D("Sofia", "Sono d'accordo sulla prima parte.", "SOH-noh dahk-KOR-doh SOOL-lah PREE-mah PAR-teh.", "I agree on the first part."),
               D("Marco", "E sulla seconda?", "eh SOOL-lah seh-KOHN-dah?", "And on the second?"),
               D("Sofia", "Su questo punto non sono convinta: preferisco una prova.", "soo KWES-toh POON-toh nohn SOH-noh kohn-VEEN-tah: preh-feh-REES-koh OO-nah PROH-vah.", "On this point I am not convinced: I prefer a trial.")],
              WS("Agreement worksheet", [
                  T("Agree with a reservation.", ["I agree on the first part", "agreed, but there is little time"],
                    ["Sono d'accordo sulla prima parte.", "D'accordo, ma il tempo è poco."]),
                  T("Disagree politely.", ["on this point I am not convinced", "I prefer a trial"],
                    ["Su questo punto non sono convinto.", "Preferisco una prova."]),
              ])),
            L("Convincere: se facciamo così, succede questo",
              "Persuasion in Italian is a real conditional: SE RIDUCIAMO I TEMPI, IL RISCHIO CRESCE. "
              "State the consequence, then let the other person draw the conclusion.",
              [V("se", "seh", "if", "conjunction"),
               V("il rischio", "eel REES-kyoh", "risk", "noun"),
               V("ridurre", "ree-DOOR-reh", "to reduce", "verb"),
               V("conviene", "kohn-VYEH-neh", "it is worth it, it makes sense", "verb"),
               V("il margine", "eel MAR-jee-neh", "margin", "noun")],
              G("Conditional frame",
                "se facciamo così, … · conviene + infinito · altrimenti il rischio cresce",
                "Se riduciamo i tempi, il rischio cresce. Conviene provare con due persone per "
                "quindici giorni; altrimenti il margine sparisce. One condition, one consequence, one "
                "proposal — the listener can check all three.",
                [X("Se riduciamo i tempi, il rischio cresce.", "seh ree-DOO-chah-moh ee TEM-pee, eel REES-kyoh KREH-sheh.", "If we cut the time, the risk grows."),
                 X("Conviene provare con due persone.", "kohn-VYEH-neh proh-VAH-reh kohn DOO-eh per-SOH-neh.", "It makes sense to try with two people."),
                 X("Altrimenti il margine sparisce.", "ahl-ter-MEN-tee eel MAR-jee-neh spah-REES-sheh.", "Otherwise the margin disappears.")],
                [("Se ridurremo i tempi, il rischio cresce.", "Se riduciamo i tempi, il rischio cresce.", "A real condition takes the presente, not the futuro."),
                 ("Conviene di provare.", "Conviene provare.", "conviene takes the bare infinitive.")]),
              [D("Sofia", "Se riduciamo i tempi, il rischio cresce.", "seh ree-DOO-chah-moh ee TEM-pee, eel REES-kyoh KREH-sheh.", "If we cut the time, the risk grows."),
               D("Marco", "Allora cosa conviene fare?", "ahl-LOH-rah KOH-zah kohn-VYEH-neh FAH-reh?", "So what makes sense to do?"),
               D("Sofia", "Conviene provare con due persone per quindici giorni.", "kohn-VYEH-neh proh-VAH-reh kohn DOO-eh per-SOH-neh per kween-DEE-chee JOR-nee.", "It makes sense to try with two people for fifteen days."),
               D("Marco", "E se non funziona?", "eh seh nohn foon-TSYOH-nah?", "And if it does not work?"),
               D("Sofia", "Altrimenti teniamo i tempi lunghi.", "ahl-ter-MEN-tee teh-NYAH-moh ee TEM-pee LOON-ghee.", "Otherwise we keep the longer timeline.")],
              WS("Persuasion worksheet", [
                  T("State the condition.", ["if we cut the time, the risk grows", "otherwise the margin disappears"],
                    ["Se riduciamo i tempi, il rischio cresce.", "Altrimenti il margine sparisce."]),
                  T("Propose the trial.", ["it makes sense to try with two people", "for fifteen days"],
                    ["Conviene provare con due persone.", "per quindici giorni"]),
              ])),
        ]},
        {"id": "B1+-U3", "title": "Progetti e scadenze", "lessons": [
            L("Obiettivi e tempi: l'obiettivo è, entro giugno",
              "A goal takes the bare infinitive; a deadline takes entro: L'OBIETTIVO È RIDURRE I COSTI "
              "ENTRO GIUGNO. entro names the outside limit, non oltre the hard one.",
              [V("l'obiettivo", "loh-byet-TEE-voh", "goal, objective", "noun"),
               V("entro", "EN-troh", "by, within", "preposition"),
               V("il traguardo", "eel trah-GWAR-doh", "milestone", "noun"),
               V("la tappa", "lah TAHP-pah", "stage", "noun"),
               V("non oltre", "nohn OHL-treh", "no later than", "phrase")],
              G("Project frames",
                "l'obiettivo è + infinito · entro giugno · il primo traguardo è … · non oltre il 30",
                "L'obiettivo è ridurre i costi entro giugno; il primo traguardo è un test a marzo, non "
                "oltre il 15. Goal, month, milestone — three sentences, and the project has a shape.",
                [X("L'obiettivo è ridurre i costi entro giugno.", "loh-byet-TEE-voh eh ree-DOOR-reh ee KOHS-tee EN-troh JOO-nyoh.", "The goal is to cut costs by June."),
                 X("Il primo traguardo è un test a marzo.", "eel PREE-moh trah-GWAR-doh eh oon test ah MAR-tsoh.", "The first milestone is a test in March."),
                 X("Non oltre il 15.", "nohn OHL-treh eel KWEEN-dee-chee.", "No later than the 15th.")],
                [("L'obiettivo è che riduciamo i costi.", "L'obiettivo è ridurre i costi.", "A goal takes the bare infinitive, not a che-clause."),
                 ("Consegniamo entro al 30 giugno.", "Consegniamo entro il 30 giugno.", "entro takes a plain date: entro il 30 giugno.")]),
              [D("Marco", "Qual è l'obiettivo del progetto?", "kwahl eh loh-byet-TEE-voh del proh-JET-toh?", "What is the project goal?"),
               D("Sofia", "Ridurre i costi entro giugno.", "ree-DOOR-reh ee KOHS-tee EN-troh JOO-nyoh.", "To cut costs by June."),
               D("Marco", "E il primo traguardo?", "eh eel PREE-moh trah-GWAR-doh?", "And the first milestone?"),
               D("Sofia", "Un test a marzo, non oltre il 15.", "oon test ah MAR-tsoh, nohn OHL-treh eel KWEEN-dee-chee.", "A test in March, no later than the 15th.")],
              WS("Goal worksheet", [
                  T("State the goal.", ["the goal is to cut the costs", "by June"],
                    ["L'obiettivo è ridurre i costi.", "entro giugno"]),
                  T("Set the milestone.", ["the first milestone is a test in March", "no later than the 15th"],
                    ["Il primo traguardo è un test a marzo.", "non oltre il 15"]),
              ])),
            L("Il colloquio: sono tre anni che lavoro qui",
              "Duration in speech takes the sono … che frame: SONO TRE ANNI CHE LAVORO QUI. Then the "
              "wish: MI INTERESSA QUESTO RUOLO.",
              [V("il colloquio", "eel kohl-LOH-kwyoh", "interview", "noun"),
               V("il percorso", "eel per-KOR-soh", "career path", "noun"),
               V("l'esperienza", "les-peh-RYEN-tsah", "experience", "noun"),
               V("mi interessa", "mee een-teh-RES-sah", "I am interested", "phrase"),
               V("la referenza", "lah reh-feh-REN-tsah", "reference", "noun")],
              G("Interview frames",
                "sono tre anni che lavoro … · mi interessa questo ruolo · ho lavorato su …",
                "Sono tre anni che lavoro nella logistica e mi interessa questo ruolo perché seguo "
                "già le consegne. Duration with the sono … che frame, then the reason the role is the "
                "next step.",
                [X("Sono tre anni che lavoro nella logistica.", "SOH-noh treh AHN-nee keh lah-VOH-roh NEL-lah loh-JEES-tee-kah.", "I have been working in logistics for three years."),
                 X("Mi interessa questo ruolo.", "mee een-teh-RES-sah KWES-toh RWOH-loh.", "I am interested in this role."),
                 X("Ho lavorato su due progetti simili.", "oh lah-voh-RAH-toh soo DOO-eh proh-JET-tee SEE-mee-lee.", "I have worked on two similar projects.")],
                [("Lavoro qui da tre anni, per tre anni.", "Sono tre anni che lavoro qui.", "Speech prefers the sono … che frame for a duration still running."),
                 ("Sono interessato per questo ruolo.", "Mi interessa questo ruolo.", "Italian says mi interessa + noun.")]),
              [D("Marco", "Da quanto tempo lavori nella logistica?", "dah KWAHN-toh TEM-poh lah-VOH-ree NEL-lah loh-JEES-tee-kah?", "How long have you worked in logistics?"),
               D("Sofia", "Sono tre anni che lavoro nella logistica.", "SOH-noh treh AHN-nee keh lah-VOH-roh NEL-lah loh-JEES-tee-kah.", "I have been working in logistics for three years."),
               D("Marco", "Perché questo ruolo?", "per-KEH KWES-toh RWOH-loh?", "Why this role?"),
               D("Sofia", "Seguo già le consegne e mi interessa coordinare il reparto.", "SEH-gwoh jah leh kohn-SEH-nyeh eh mee een-teh-RES-sah koh-or-dee-NAH-reh eel reh-PAR-toh.", "I already follow deliveries and I am interested in coordinating the department.")],
              WS("Interview worksheet", [
                  T("State the experience.", ["I have been working in logistics for three years", "I have worked on two similar projects"],
                    ["Sono tre anni che lavoro nella logistica.", "Ho lavorato su due progetti simili."]),
                  T("Answer the motivation.", ["I am interested in this role", "I already follow the deliveries"],
                    ["Mi interessa questo ruolo.", "Seguo già le consegne."]),
              ])),
            L("Rischi e imprevisti: se salta la scadenza",
              "Contingency talk names the risk and the fallback: SE SALTA LA SCADENZA, AVVISIAMO IL "
              "CLIENTE SUBITO. Prima il rischio, poi la mossa, infine chi la fa.",
              [V("l'imprevisto", "leem-preh-VEES-toh", "unforeseen event", "noun"),
               V("saltare", "sahl-TAH-reh", "to be missed, to blow (a deadline)", "verb"),
               V("il piano B", "eel PYAH-noh BEE", "plan B", "noun"),
               V("avvisare subito", "ahv-vee-ZAH-reh SOO-bee-toh", "to notify immediately", "phrase"),
               V("recuperare il ritardo", "reh-koo-peh-RAH-reh eel ree-TAR-doh", "to make up the delay", "phrase")],
              G("Contingency frame",
                "se salta la scadenza, … · avvisiamo il cliente subito · il piano B è … · recuperiamo il ritardo",
                "Se salta la scadenza, avvisiamo il cliente subito e passiamo al piano B: due "
                "settimane in più. The risk is stated plainly, the fallback is named, and no one has "
                "to guess in the moment.",
                [X("Se salta la scadenza, avvisiamo il cliente.", "seh SAHL-tah lah skah-DEN-tsah, ahv-vee-ZYAH-moh eel kly-EN-teh.", "If the deadline slips, we notify the client."),
                 X("Il piano B è due settimane in più.", "eel PYAH-noh BEE eh DOO-eh set-tee-MAH-neh een pyoo.", "Plan B is two more weeks."),
                 X("Recuperiamo il ritardo a luglio.", "reh-koo-peh-RYAH-moh eel ree-TAR-doh ah LOO-lyoh.", "We make up the delay in July.")],
                [("Se salta la scadenza, avvisiamo il cliente magari.", "Se salta la scadenza, avvisiamo il cliente subito.", "A contingency names a timing, not a maybe."),
                 ("Il piano B è di due settimane.", "Il piano B è due settimane in più.", "A fallback is described with its content, not with di.")]),
              [D("Sofia", "E se salta la scadenza?", "eh seh SAHL-tah lah skah-DEN-tsah?", "And if the deadline slips?"),
               D("Marco", "Avvisiamo il cliente subito.", "ahv-vee-ZYAH-moh eel kly-EN-teh SOO-bee-toh.", "We notify the client immediately."),
               D("Sofia", "E poi?", "eh pohy?", "And then?"),
               D("Marco", "Piano B: due settimane in più, recuperiamo il ritardo a luglio.", "PYAH-noh BEE: DOO-eh set-tee-MAH-neh een pyoo, reh-koo-peh-RYAH-moh eel ree-TAR-doh ah LOO-lyoh.", "Plan B: two more weeks, we make up the delay in July.")],
              WS("Risk worksheet", [
                  T("Name the risk and the move.", ["if the deadline slips, we notify the client", "we switch to plan B"],
                    ["Se salta la scadenza, avvisiamo il cliente.", "Passiamo al piano B."]),
                  T("Describe the fallback.", ["two more weeks", "we make up the delay in July"],
                    ["due settimane in più", "recuperiamo il ritardo a luglio"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Italian office life is more oral than its paperwork suggests: the riunione is where "
                 "decisions are actually taken, the verbale is written afterwards by whoever holds the "
                 "pen, and the email that follows exists to confirm what was said out loud. The "
                 "half-step therefore teaches three registers at once — the spoken meeting, the "
                 "written minutes, and the opinion that has to survive both."),
        source_url="https://en.wikipedia.org/wiki/Meeting",
        reading=("Prima di tutto l'ordine del giorno: tre punti. Sul secondo intervengo io: secondo me "
                 "la proposta regge, ma dal mio punto di vista manca un dato sui costi. Se riduciamo i "
                 "tempi, il rischio cresce. Alla fine abbiamo deciso di provare con due persone per "
                 "quindici giorni; la scadenza è fissata al 30 giugno e il budget resta in sospeso. "
                 "Scrivo il verbale nel pomeriggio e lo mando a tutti."),
        reading_gloss=("First of all the agenda: three points. On the second I take the floor: in my "
                       "opinion the proposal holds, but from my point of view a cost figure is missing. "
                       "If we cut the time, the risk grows. In the end we decided to try with two "
                       "people for fifteen days; the deadline is set for 30 June and the budget "
                       "remains open. I will write the minutes in the afternoon and send them to "
                       "everyone."),
        listening=("Marco: Allora, approviamo il piano?<br>Sofia: Sono d'accordo sulla prima parte. Su "
                   "questo punto non sono convinta: preferisco una prova.<br>Marco: Se facciamo una "
                   "prova, chi la segue?<br>Sofia: Due persone, quindici giorni, e il verbale lo "
                   "scrivo io."),
        listening_gloss=("Marco: So, do we approve the plan? Sofia: I agree on the first part. On this "
                         "point I am not convinced: I prefer a trial. Marco: If we run a trial, who "
                         "follows it? Sofia: Two people, fifteen days, and I will write the minutes."),
        voice_tag=VOICE,
        idioms=[
            ("Ordine del giorno", "order of the day", "the agenda"),
            ("Prendere la parola", "to take the word", "to take the floor"),
            ("Mettere ai voti", "to put to the votes", "to put to the vote"),
            ("Restare in sospeso", "to remain in suspense", "to stay open"),
            ("Punto di vista", "point of view", "point of view"),
            ("Essere d'accordo", "to be of accord", "to agree"),
            ("Dare una mano", "to give a hand", "to help out"),
            ("Saltare la scadenza", "to jump the deadline", "to blow the deadline"),
            ("Piano B", "plan B", "fallback plan"),
            ("Fare il punto", "to make the point", "to take stock"),
        ],
        mistakes=[
            ("Sono d'accordo con tutto, però no.", "Sono d'accordo sulla prima parte; sul resto ho una riserva.", "Agreement names the part it covers."),
            ("La scadenza è al 30 giugno, forse.", "La scadenza è fissata al 30 giugno.", "A deadline that is real has no forse."),
            ("Mi sembra che il piano è pronto.", "Mi sembra che il piano sia pronto.", "mi sembra che takes the congiuntivo."),
        ],
        task_title="Run a fifteen-minute meeting and write its minutes",
        task_instructions=("Take a real decision you have to make this week — at work, at home, in a "
                           "club. Write the Italian agenda (three points), then the two lines you "
                           "will actually say to open the discussion (posso intervenire, secondo "
                           "me), then the minutes: one decision with a date, one open item, one "
                           "owner. If a line has no owner, you have found the part of the plan that "
                           "is not yet a plan."),
    ),
    "test": [
        ("translate_en", "Say: May I speak on the second point?", "Posso intervenire sul secondo punto?"),
        ("translate_it", "Abbiamo deciso di rinviare il lancio; la scadenza è fissata al 30 giugno.", "We decided to postpone the launch; the deadline is set for 30 June."),
        ("multiple_choice", "Which sentence takes the congiuntivo?", "Mi sembra che il piano sia pronto."),
        ("fill_in_the_blank", "Mi occupo ___ consegne nel reparto logistica.", "delle"),
        ("word_selection", "Select the Italian for 'no later than the 15th'.", "non oltre il 15"),
        ("error_correction", "Se ridurremo i tempi, il rischio cresce.", "Se riduciamo i tempi, il rischio cresce."),
        ("dialogue_completion", "Complete: Su questo punto ___ convinta. (I am not)", "non sono"),
        ("matching", "Match restare in sospeso to its meaning.", "to stay open"),
        ("reading_comprehension", "La scadenza è fissata al 30 giugno. What is set for 30 June?", "the deadline"),
        ("inference", "«D'accordo, ma il tempo è poco» — what is the speaker doing?", "agreeing with a reservation"),
        ("main_idea", "Piano B: due settimane in più, recuperiamo il ritardo a luglio. What is this about?", "a fallback plan"),
        ("detail_identification", "Sono tre anni che lavoro nella logistica. How long?", "three years"),
    ],
}

HALFSTEPS["B2+"] = {
    "title": "Italian B2+ — Argument and formal register",
    "native": NATIVE,
    "goals": [
        "Read a figure, a trend and a source without being misled",
        "Chain an argument and interrogate the data behind it",
        "Write a formal letter, a complaint and a written apology",
        "Summarise a document and close it with one decision",
    ],
    "units": [
        {"id": "B2+-U1", "title": "Dati e argomenti", "lessons": [
            L("Le cifre che convincono: il doppio, un terzo, in calo del 2%",
              "Italian puts the figure first and the comparison after: LE VENDITE SONO IL DOPPIO "
              "DELL'ANNO SCORSO · UN TERZO DEI CLIENTI · IN CALO DEL 2%. Fractions take a singular verb.",
              [V("la cifra", "lah CHEE-frah", "figure, number", "noun"),
               V("il doppio", "eel DOHP-pyoh", "double", "noun"),
               V("un terzo", "oon TER-tsoh", "a third", "noun"),
               V("il calo", "eel KAH-loh", "fall, decrease", "noun"),
               V("l'aumento", "low-MEN-toh", "increase", "noun")],
              G("Figures and trends",
                "il doppio di · un terzo dei clienti · in calo del 2% · pari al 15%",
                "Le vendite sono il doppio dell'anno scorso; un terzo dei clienti arriva dal web e il "
                "prezzo medio è in calo del 2%. The figure comes first, and di or del carries the "
                "comparison.",
                [X("Le vendite sono il doppio dell'anno scorso.", "leh VEN-dee-teh SOH-noh eel DOHP-pyoh del-LAHN-noh SKOR-soh.", "Sales are double last year's."),
                 X("Un terzo dei clienti arriva dal web.", "oon TER-tsoh day kly-EN-tee ahr-REE-vah dahl web.", "A third of the customers come from the web."),
                 X("Il prezzo è in calo del 2%.", "eel PRET-tsoh eh een KAH-loh del DOO-eh per CHEN-toh.", "The price is down by 2%.")],
                [("Le vendite sono due volte più dell'anno scorso.", "Le vendite sono il doppio dell'anno scorso.", "Doubling is il doppio di, not due volte più di."),
                 ("Un terzo dei clienti arrivano dal web.", "Un terzo dei clienti arriva dal web.", "A fraction takes the singular verb in Italian.")]),
              [D("Capo", "Come vanno le vendite?", "KOH-meh VAHN-noh leh VEN-dee-teh?", "How are the sales going?"),
               D("Sofia", "Sono il doppio dell'anno scorso.", "SOH-noh eel DOHP-pyoh del-LAHN-noh SKOR-soh.", "They are double last year's."),
               D("Capo", "E il prezzo medio?", "eh eel PRET-tsoh MEH-dyoh?", "And the average price?"),
               D("Sofia", "È in calo del due per cento.", "eh een KAH-loh del DOO-eh per CHEN-toh.", "It is down by two per cent.")],
              WS("Figures worksheet", [
                  T("Read the figures.", ["sales are double last year's", "a third of the customers"],
                    ["Le vendite sono il doppio dell'anno scorso.", "un terzo dei clienti"]),
                  T("State the trend.", ["the price is down by 2%", "the costs are rising slightly"],
                    ["Il prezzo è in calo del 2%.", "I costi sono in leggero aumento."]),
              ])),
            L("Incatenare gli argomenti: non solo … ma anche",
              "A chain needs direction words: NON SOLO … MA ANCHE … · INOLTRE · DI CONSEGUENZA. They "
              "carry the argument forward so that perché does not have to do all the work.",
              [V("non solo", "nohn SOH-loh", "not only", "phrase"),
               V("ma anche", "mah AHN-keh", "but also", "phrase"),
               V("inoltre", "ee-NOL-treh", "moreover", "adverb"),
               V("di conseguenza", "dee kohn-seh-GWEN-tsah", "consequently", "phrase"),
               V("quindi", "KWEEN-dee", "therefore", "conjunction")],
              G("Argument chain",
                "non solo … ma anche … · inoltre · di conseguenza · quindi",
                "Non solo i costi calano, ma anche i tempi si accorciano; di conseguenza il margine "
                "cresce. Moreover extends, therefore concludes — and the second clause changes verb "
                "instead of repeating it.",
                [X("Non solo i costi calano, ma anche i tempi si accorciano.", "nohn SOH-loh ee KOHS-tee KAH-lah-noh, mah AHN-keh ee TEM-pee see ahk-kor-CHAH-noh.", "Not only do the costs fall, but the times also shorten."),
                 X("Inoltre il margine cresce.", "ee-NOL-treh eel MAR-jee-neh KREH-sheh.", "Moreover the margin grows."),
                 X("Di conseguenza, conviene partire a marzo.", "dee kohn-seh-GWEN-tsah, kohn-VYEH-neh par-TEE-reh ah MAR-tsoh.", "Consequently, it makes sense to start in March.")],
                [("Non solo i costi calano, ma anche calano i tempi.", "Non solo i costi calano, ma anche i tempi si accorciano.", "The second clause varies the verb instead of repeating it."),
                 ("Quindi di conseguenza partiamo.", "Di conseguenza partiamo.", "One connector at a time: quindi and di conseguenza do not stack.")]),
              [D("Marco", "Non solo i costi calano, ma anche i tempi si accorciano.", "nohn SOH-loh ee KOHS-tee KAH-lah-noh, mah AHN-keh ee TEM-pee see ahk-kor-CHAH-noh.", "Not only do costs fall, but the times also shorten."),
               D("Sofia", "E di conseguenza?", "eh dee kohn-seh-GWEN-tsah?", "And consequently?"),
               D("Marco", "Il margine cresce, quindi conviene partire a marzo.", "eel MAR-jee-neh KREH-sheh, KWEEN-dee kohn-VYEH-neh par-TEE-reh ah MAR-tsoh.", "The margin grows, so it makes sense to start in March."),
               D("Sofia", "Allora porto i numeri in riunione.", "ahl-LOH-rah POR-toh ee NOO-meh-ree een ree-oo-NYOH-neh.", "Then I will bring the figures to the meeting.")],
              WS("Chain worksheet", [
                  T("Chain the argument.", ["not only do the costs fall, but the times also shorten", "consequently the margin grows"],
                    ["Non solo i costi calano, ma anche i tempi si accorciano.", "Di conseguenza il margine cresce."]),
                  T("Add a second reason.", ["moreover, the client asked for it", "so it makes sense to start in March"],
                    ["Inoltre il cliente l'ha chiesto.", "Quindi conviene partire a marzo."]),
              ])),
            L("Interrogare i dati: la fonte, il metodo, il campione",
              "Three questions turn a percentage into evidence: SECOND O LA FONTE? SU QUALE CAMPIONE? "
              "CON QUALE METODO? A figure without all three is a rumour with a decimal point.",
              [V("la fonte", "lah FOHN-teh", "source", "noun"),
               V("il campione", "eel kahm-PYOH-neh", "sample", "noun"),
               V("il metodo", "eel MEH-toh-doh", "method", "noun"),
               V("la media", "lah MEH-dyah", "average", "noun"),
               V("l'indagine", "leen-DAH-jee-neh", "survey", "noun")],
              G("Interrogating a figure",
                "secondo la fonte · su un campione di … · la media è … · il metodo non è dichiarato",
                "Il dato è del 12%: su quale campione, con quale metodo? Secondo la fonte, la media è "
                "del 12% su mille interviste; il metodo non è dichiarato. Ask the three questions "
                "before the number enters your argument.",
                [X("Secondo la fonte, la media è del 12%.", "seh-KOHN-doh lah FOHN-teh, lah MEH-dyah eh del DOH-dee-chee per CHEN-toh.", "According to the source, the average is 12%."),
                 X("Su un campione di mille interviste.", "soo oon kahm-PYOH-neh dee MEEL-leh een-ter-VEES-teh.", "On a sample of a thousand interviews."),
                 X("Il metodo non è dichiarato.", "eel MEH-toh-doh nohn eh dee-kyah-RAH-toh.", "The method is not declared.")],
                [("Il 70% delle persone pensa che …", "Secondo l'indagine, il 70% degli intervistati pensa che …", "A percentage needs its source and its population."),
                 ("Il 70% degli intervistati pensano che …", "Il 70% degli intervistati pensa che …", "The percentage, not the population, is the subject.")]),
              [D("Sofia", "Il dato è del dodici per cento.", "eel DAH-toh eh del DOH-dee-chee per CHEN-toh.", "The figure is twelve per cent."),
               D("Capo", "Su quale campione?", "soo KWAH-leh kahm-PYOH-neh?", "On which sample?"),
               D("Sofia", "Mille interviste, secondo l'indagine.", "MEEL-leh een-ter-VEES-teh, seh-KOHN-doh leen-DAH-jee-neh.", "A thousand interviews, according to the survey."),
               D("Capo", "E il metodo?", "eh eel MEH-toh-doh?", "And the method?"),
               D("Sofia", "Non è dichiarato: lo chiedo io.", "nohn eh dee-kyah-RAH-toh: loh KYEH-doh EE-oh.", "It is not declared: I will ask.")],
              WS("Evidence worksheet", [
                  T("Interrogate the figure.", ["according to the source, the average is 12%", "on a sample of a thousand interviews"],
                    ["Secondo la fonte, la media è del 12%.", "su un campione di mille interviste"]),
                  T("Flag the gap.", ["the method is not declared", "I will ask for it"],
                    ["Il metodo non è dichiarato.", "Lo chiedo io."]),
              ])),
        ]},
        {"id": "B2+-U2", "title": "Registro formale: scrivere per ottenere", "lessons": [
            L("La lettera formale: in riferimento a, distinti saluti",
              "A formal letter is a reference, a request and a closing: EGREGIO DOT TORE, IN "
              "RIFERIMENTO ALLA SUA DEL 3 MAGGIO · IL SOTTOSCRITTO CHIEDE · DISTINTI SALUTI.",
              [V("egregio", "eh-GREH-joh", "dear (formal, to a man)", "adjective"),
               V("in riferimento a", "een ree-feh-ree-MEN-toh ah", "with reference to", "phrase"),
               V("il sottoscritto", "eel sot-toh-SKREET-toh", "the undersigned", "noun"),
               V("il cortese riscontro", "eel kor-TEH-zeh ree-SKOHN-troh", "kind reply", "phrase"),
               V("distinti saluti", "dee-STEEN-tee sah-LOO-tee", "distinct regards", "phrase")],
              G("Formal letter frame",
                "Egregio Dottore, · in riferimento alla Sua del … · il sottoscritto chiede … · distinti saluti",
                "Egregio Dottore, in riferimento alla Sua del 3 maggio, il sottoscritto chiede un "
                "chiarimento. In attesa di un cortese riscontro, distinti saluti. Three shelves and "
                "not one word more.",
                [X("Egregio Dottore, in riferimento alla Sua del 3 maggio,", "eh-GREH-joh dot-TOH-reh, een ree-feh-ree-MEN-toh AHL-lah SOO-ah del TREH MAJ-joh,", "Dear Doctor, with reference to your letter of 3 May,"),
                 X("Il sottoscritto chiede un chiarimento.", "eel sot-toh-SKREET-toh KYEH-deh oon kyah-ree-MEN-toh.", "The undersigned asks for a clarification."),
                 X("In attesa di un cortese riscontro, distinti saluti.", "een ah-TEH-zah dee oon kor-TEH-zeh ree-SKOHN-troh, dee-STEEN-tee sah-LOO-tee.", "Awaiting your kind reply, distinct regards.")],
                [("Caro Dottore, come stai?", "Egregio Dottore, come sta?", "A formal letter keeps the Lei form and the title alone."),
                 ("In attesa di un riscontro, ciao.", "In attesa di un cortese riscontro, distinti saluti.", "The closing formula matches the register of the opening.")]),
              [D("Sofia", "Come comincio la lettera?", "KOH-meh koh-MEEN-choh lah LET-teh-rah?", "How do I start the letter?"),
               D("Marco", "«Egregio Dottore, in riferimento alla Sua del 3 maggio».", "eh-GREH-joh dot-TOH-reh, een ree-feh-ree-MEN-toh AHL-lah SOO-ah del TREH MAJ-joh.", "'Dear Doctor, with reference to your letter of 3 May'."),
               D("Sofia", "E chiudo?", "eh KYOO-doh?", "And how do I close?"),
               D("Marco", "«In attesa di un cortese riscontro, distinti saluti.»", "een ah-TEH-zah dee oon kor-TEH-zeh ree-SKOHN-troh, dee-STEEN-tee sah-LOO-tee.", "'Awaiting your kind reply, distinct regards.'")],
              WS("Letter worksheet", [
                  T("Open the letter.", ["Dear Doctor, with reference to your letter of 3 May", "the undersigned asks for a clarification"],
                    ["Egregio Dottore, in riferimento alla Sua del 3 maggio,", "Il sottoscritto chiede un chiarimento."]),
                  T("Close it.", ["awaiting your kind reply", "distinct regards"],
                    ["In attesa di un cortese riscontro,", "distinti saluti"]),
              ])),
            L("Il reclamo formale: fatti, motivi, richiesta",
              "A complaint is three paragraphs with no adjectives: ESPONGO I FATTI · PER QUESTI MOTIVI "
              "· CHIEDO … ENTRO DIECI GIORNI. Facts, grounds, request — and a date.",
              [V("il reclamo", "eel reh-KLAH-moh", "complaint", "noun"),
               V("i fatti", "ee FAHT-tee", "the facts", "noun"),
               V("la richiesta", "lah ree-KYES-tah", "request", "noun"),
               V("il risarcimento", "eel ree-sar-chee-MEN-toh", "compensation", "noun"),
               V("entro", "EN-troh", "within", "preposition")],
              G("Complaint frame",
                "espongo i fatti · per questi motivi · chiedo la restituzione … entro …",
                "Espongo i fatti: il pacco doveva arrivare il 3 maggio ed è arrivato il 12. Per questi "
                "motivi chiedo la restituzione delle spese entro dieci giorni. The date is what turns "
                "a complaint into a claim someone can answer.",
                [X("Espongo i fatti: il pacco è arrivato con nove giorni di ritardo.", "es-POHN-goh ee FAHT-tee: eel PAHK-koh eh ahr-ree-VAH-toh kohn NOH-veh JOR-nee dee ree-TAR-doh.", "I set out the facts: the parcel arrived nine days late."),
                 X("Per questi motivi chiedo la restituzione delle spese.", "per KWES-tee moh-TEE-vee KYEH-doh lah ree-stee-too-TSYOH-neh DEL-leh SPEH-zeh.", "For these reasons I ask for the refund of the costs."),
                 X("Entro dieci giorni.", "EN-troh DYEH-chee JOR-nee.", "Within ten days.")],
                [("Siete dei disonesti, voglio i soldi.", "Per questi motivi chiedo la restituzione delle spese entro dieci giorni.", "A complaint that names facts and a request gets answered; an insult gets filed."),
                 ("Chiedo di essere rimborsato i soldi.", "Chiedo la restituzione delle spese.", "The refund is la restituzione delle spese, with a single object.")]),
              [D("Marco", "Come scrivo il reclamo?", "KOH-meh SKREE-voh eel reh-KLAH-moh?", "How do I write the complaint?"),
               D("Sofia", "Prima i fatti, poi i motivi, poi la richiesta.", "PREE-mah ee FAHT-tee, pohy ee moh-TEE-vee, pohy lah ree-KYES-tah.", "First the facts, then the grounds, then the request."),
               D("Marco", "Fatti: nove giorni di ritardo.", "FAHT-tee: NOH-veh JOR-nee dee ree-TAR-doh.", "Facts: nine days late."),
               D("Sofia", "E chiudi con «chiedo la restituzione delle spese entro dieci giorni».", "eh KYOO-dee kohn KYEH-doh lah ree-stee-too-TSYOH-neh DEL-leh SPEH-zeh EN-troh DYEH-chee JOR-nee.", "And close with 'I ask for the refund within ten days'.")],
              WS("Complaint worksheet", [
                  T("State facts and grounds.", ["the parcel arrived nine days late", "for these reasons"],
                    ["Il pacco è arrivato con nove giorni di ritardo.", "Per questi motivi"]),
                  T("Make the request.", ["I ask for the refund of the costs", "within ten days"],
                    ["Chiedo la restituzione delle spese.", "entro dieci giorni"]),
              ])),
            L("Scusarsi per iscritto: ci rammarichiamo",
              "A written apology names the inconvenience, the repair and the date: CI RAMMARICHIAMO PER "
              "IL DISAGIO · PROVVEDEREMO ALLA SOSTITUZIONE ENTRO TRE GIORNI LAVORATIVI.",
              [V("rammaricarsi", "rahm-mah-ree-KAR-see", "to regret", "verb"),
               V("il disagio", "eel dee-ZAH-joh", "inconvenience", "noun"),
               V("provvedere a", "prohv-veh-DEH-reh ah", "to arrange, to see to", "verb"),
               V("il sollecito", "eel sohl-LEH-chee-toh", "reminder, follow-up", "noun"),
               V("la cortese attenzione", "lah kor-TEH-zeh aht-ten-TSYOH-neh", "kind attention", "phrase")],
              G("Written apology",
                "ci rammarichiamo per … · provvederemo a … entro … · grazie per la cortese attenzione",
                "Ci rammarichiamo per il disagio. Provvederemo alla sostituzione entro tre giorni "
                "lavorativi. Grazie per la cortese attenzione. An apology with no repair and no date "
                "is a second inconvenience.",
                [X("Ci rammarichiamo per il disagio.", "chee rahm-mah-ree-KYAH-moh per eel dee-ZAH-joh.", "We regret the inconvenience."),
                 X("Provvederemo alla sostituzione entro tre giorni lavorativi.", "prohv-veh-deh-REH-moh AHL-lah sohs-tee-too-TSYOH-neh EN-troh treh JOR-nee lah-voh-rah-TEE-vee.", "We will arrange the replacement within three working days."),
                 X("La ringraziamo per la cortese attenzione.", "lah reen-GRAH-tsyah-moh per lah kor-TEH-zeh aht-ten-TSYOH-neh.", "We thank you for your kind attention.")],
                [("Scusa per il ritardo.", "Ci rammarichiamo per il disagio.", "Between companies the apology speaks in the first person plural."),
                 ("Provvediamo subito, forse domani.", "Provvederemo entro tre giorni lavorativi.", "A repair carries a date, not a hope.")]),
              [D("Sofia", "Hanno scritto per il ritardo.", "AHN-noh SKREET-toh per eel ree-TAR-doh.", "They wrote about the delay."),
               D("Marco", "Rispondiamo: «ci rammarichiamo per il disagio».", "rees-POHN-dyah-moh: chee rahm-mah-ree-KYAH-moh per eel dee-ZAH-joh.", "Let us answer: 'we regret the inconvenience'."),
               D("Sofia", "E la sostituzione?", "eh lah sohs-tee-too-TSYOH-neh?", "And the replacement?"),
               D("Marco", "«Provvederemo entro tre giorni lavorativi.»", "prohv-veh-deh-REH-moh EN-troh treh JOR-nee lah-voh-rah-TEE-vee.", "'We will see to it within three working days.'")],
              WS("Apology worksheet", [
                  T("Apologise formally.", ["we regret the inconvenience", "we will arrange the replacement"],
                    ["Ci rammarichiamo per il disagio.", "Provvederemo alla sostituzione."]),
                  T("Give the date.", ["within three working days", "thank you for your kind attention"],
                    ["entro tre giorni lavorativi", "La ringraziamo per la cortese attenzione."]),
              ])),
        ]},
        {"id": "B2+-U3", "title": "Sintesi e chiusura", "lessons": [
            L("Riformulare: in altre parole, vale a dire",
              "Reformulation opens a second door into the same sentence: IN ALTRE PAROLE · VALE A DIRE "
              "· IN PRATICA. One marker per sentence, and the reader gets a second chance.",
              [V("riformulare", "ree-for-moo-LAH-reh", "to reformulate", "verb"),
               V("in altre parole", "een AHL-treh pah-ROH-leh", "in other words", "phrase"),
               V("vale a dire", "VAH-leh ah DEE-reh", "that is to say", "phrase"),
               V("il concetto", "eel kohn-CHET-toh", "concept", "noun"),
               V("in pratica", "een PRAH-tee-kah", "in practice", "phrase")],
              G("Reformulation frame",
                "in altre parole · vale a dire · in pratica, …",
                "Il margine resta sotto il 5%: in altre parole, non c'è spazio per un errore. Vale a "
                "dire: due settimane di margine. In pratica, il piano regge solo con i tempi lunghi.",
                [X("In altre parole, non c'è spazio per un errore.", "een AHL-treh pah-ROH-leh, nohn cheh SPAH-tsyoh per oon er-ROH-reh.", "In other words, there is no room for an error."),
                 X("Vale a dire: due settimane di margine.", "VAH-leh ah DEE-reh: DOO-eh set-tee-MAH-neh dee MAR-jee-neh.", "That is to say: two weeks of margin."),
                 X("In pratica, il piano regge solo con i tempi lunghi.", "een PRAH-tee-kah, eel PYAH-noh RED-jeh SOH-loh kohn ee TEM-pee LOON-ghee.", "In practice, the plan holds only with the long timeline.")],
                [("In altre parole, cioè, in pratica, non c'è margine.", "In altre parole, non c'è margine.", "One reformulation marker per sentence."),
                 ("Vale a dire che due settimane.", "Vale a dire: due settimane di margine.", "vale a dire introduces a noun phrase with a colon, not a fragment with che.")]),
              [D("Capo", "Cosa significa «margine sotto il 5%»?", "KOH-zah see-NYEE-fee-kah MAR-jee-neh SOHT-toh eel CHEN-kweh per CHEN-toh?", "What does 'margin below 5%' mean?"),
               D("Sofia", "In altre parole: non c'è spazio per un errore.", "een AHL-treh pah-ROH-leh: nohn cheh SPAH-tsyoh per oon er-ROH-reh.", "In other words: there is no room for an error."),
               D("Capo", "Traduci in pratica.", "trah-DOO-chee een PRAH-tee-kah.", "Put it into practice."),
               D("Sofia", "Vale a dire due settimane di margine, non di più.", "VAH-leh ah DEE-reh DOO-eh set-tee-MAH-neh dee MAR-jee-neh, nohn dee pyoo.", "That is to say two weeks of margin, no more.")],
              WS("Reformulation worksheet", [
                  T("Reformulate.", ["in other words, there is no room for error", "that is to say: two weeks of margin"],
                    ["In altre parole, non c'è spazio per un errore.", "Vale a dire: due settimane di margine."]),
                  T("Bring it to practice.", ["in practice, the plan holds only with the long timeline", "how do you put it better?"],
                    ["In pratica, il piano regge solo con i tempi lunghi.", "Come si dice meglio?"]),
              ])),
            L("Riassumere un documento: in sintesi",
              "A summary counts and selects: IN SINTESI: TRE RICHIESTE, UNA APPROVATA · IN SOSTANZA, IL "
              "PUNTO CHIAVE È … · A GRANDI LINEE. How many points, and which one decides the rest.",
              [V("in sintesi", "een SEEN-teh-zee", "in summary", "phrase"),
               V("in sostanza", "een sohs-TAHN-tsah", "in essence", "phrase"),
               V("a grandi linee", "ah GRAHN-dee LEE-neh", "broadly speaking", "phrase"),
               V("il punto chiave", "eel POON-toh KYAH-veh", "the key point", "noun"),
               V("la raccomandazione", "lah rahk-koh-mahn-dah-TSYOH-neh", "recommendation", "noun")],
              G("Summary frame",
                "in sintesi: … · in sostanza, il punto chiave è … · a grandi linee · la raccomandazione è …",
                "In sintesi: il documento chiede tre cose, ne ottiene una e rinvia le altre due. In "
                "sostanza, il punto chiave è chi paga; a grandi linee, il piano regge. A summary "
                "states the count and the pivot.",
                [X("In sintesi: tre richieste, una sola approvata.", "een SEEN-teh-zee: treh ree-KYES-teh, OO-nah SOH-lah ahp-proh-VAH-tah.", "In summary: three requests, only one approved."),
                 X("In sostanza, il punto chiave è chi paga.", "een sohs-TAHN-tsah, eel POON-toh KYAH-veh eh kee PAH-gah.", "In essence, the key point is who pays."),
                 X("A grandi linee, il piano regge.", "ah GRAHN-dee LEE-neh, eel PYAH-noh RED-jeh.", "Broadly speaking, the plan holds.")],
                [("In sintesi, il documento parla di tante cose interessanti.", "In sintesi: tre richieste, una approvata.", "A summary counts and selects; interesting things are not a summary."),
                 ("A grandi linee, il punto chiave è chi paga, in sostanza.", "In sostanza, il punto chiave è chi paga.", "Summary markers do not double inside one sentence.")]),
              [D("Marco", "Riassumi il documento.", "ree-AHS-soo-mee eel doh-koo-MEN-toh.", "Summarise the document."),
               D("Sofia", "In sintesi: tre richieste, una approvata.", "een SEEN-teh-zee: treh ree-KYES-teh, OO-nah ahp-proh-VAH-tah.", "In summary: three requests, one approved."),
               D("Marco", "E il punto chiave?", "eh eel POON-toh KYAH-veh?", "And the key point?"),
               D("Sofia", "In sostanza: chi paga.", "een sohs-TAHN-tsah: kee PAH-gah.", "In essence: who pays.")],
              WS("Summary worksheet", [
                  T("Summarise.", ["in summary: three requests, one approved", "in essence, the key point is who pays"],
                    ["In sintesi: tre richieste, una approvata.", "In sostanza, il punto chiave è chi paga."]),
                  T("Give the outline.", ["broadly speaking, the plan holds", "the recommendation is two more weeks"],
                    ["A grandi linee, il piano regge.", "La raccomandazione è due settimane in più."]),
              ])),
            L("Chiudere: in conclusione, per questi motivi",
              "A closing converts the argument into one decision with an owner: IN CONCLUSIONE, PER "
              "QUESTI MOTIVI CHIEDIAMO DI APPROVARE LA PROVA. IL PROSSIMO PASSO È FISSARE LA DATA.",
              [V("in conclusione", "een kohn-kloo-ZYOH-neh", "in conclusion", "phrase"),
               V("per questi motivi", "per KWES-tee moh-TEE-vee", "for these reasons", "phrase"),
               V("la proposta finale", "lah proh-POHS-tah fee-NAH-leh", "the final proposal", "noun"),
               V("il prossimo passo", "eel PROHS-see-moh PAHS-soh", "the next step", "noun"),
               V("approvare", "ahp-proh-VAH-reh", "to approve", "verb")],
              G("Closing frame",
                "in conclusione · per questi motivi · chiediamo di approvare … · il prossimo passo è …",
                "In conclusione, per questi motivi chiediamo di approvare la prova. Il prossimo passo è "
                "fissare la data. The closing does not repeat the reasoning; it names the decision "
                "and who takes it.",
                [X("In conclusione, chiediamo di approvare la prova.", "een kohn-kloo-ZYOH-neh, kyah-DYAH-moh dee ahp-proh-VAH-reh lah PROH-vah.", "In conclusion, we ask you to approve the trial."),
                 X("Per questi motivi, la proposta finale è la più prudente.", "per KWES-tee moh-TEE-vee, lah proh-POHS-tah fee-NAH-leh eh lah pyoo proo-DEN-teh.", "For these reasons, the final proposal is the most prudent."),
                 X("Il prossimo passo è fissare la data.", "eel PROHS-see-moh PAHS-soh eh fees-SAH-reh lah DAH-tah.", "The next step is to set the date.")],
                [("In conclusione, come ho detto, ribadisco quanto sopra.", "In conclusione, chiediamo di approvare la prova.", "A closing asks for a decision; it does not repeat itself."),
                 ("Il prossimo passo è di fissare la data.", "Il prossimo passo è fissare la data.", "A step takes the bare infinitive.")]),
              [D("Sofia", "Come chiudo il documento?", "KOH-meh KYOO-doh eel doh-koo-MEN-toh?", "How do I close the document?"),
               D("Marco", "«In conclusione, per questi motivi chiediamo di approvare la prova.»", "een kohn-kloo-ZYOH-neh, per KWES-tee moh-TEE-vee kyah-DYAH-moh dee ahp-proh-VAH-reh lah PROH-vah.", "'In conclusion, for these reasons we ask you to approve the trial.'"),
               D("Sofia", "E l'ultima riga?", "eh LOOL-tee-mah REE-gah?", "And the last line?"),
               D("Marco", "«Il prossimo passo è fissare la data.»", "eel PROHS-see-moh PAHS-soh eh fees-SAH-reh lah DAH-tah.", "'The next step is to set the date.'")],
              WS("Closing worksheet", [
                  T("Close the text.", ["in conclusion, we ask you to approve the trial", "for these reasons"],
                    ["In conclusione, chiediamo di approvare la prova.", "Per questi motivi"]),
                  T("Name the next step.", ["the next step is to set the date", "the final proposal is the most prudent"],
                    ["Il prossimo passo è fissare la data.", "La proposta finale è la più prudente."]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Formal Italian is a register with fixed furniture: the Lei form, the title without a "
                 "first name (Egregio Dottore, Gentile Dottoressa), the passive for institutions and "
                 "the closing formula that has to match the opening. Nothing here is improvised, and "
                 "that is the point — a letter that uses the right hinges is read as competent before "
                 "its first argument is even weighed."),
        source_url="https://en.wikipedia.org/wiki/Business_etiquette",
        reading=("Egregio Dottore, in riferimento alla Sua del 3 maggio, il sottoscritto espone i "
                 "fatti: il pacco doveva arrivare il 3 maggio ed è arrivato il 12. Per questi motivi "
                 "chiedo la restituzione delle spese entro dieci giorni. In sintesi: nove giorni di "
                 "ritardo, nessuna comunicazione, una richiesta. In attesa di un cortese riscontro, "
                 "distinti saluti."),
        reading_gloss=("Dear Doctor, with reference to your letter of 3 May, the undersigned sets out "
                       "the facts: the parcel was to arrive on 3 May and arrived on the 12th. For "
                       "these reasons I ask for the refund of the costs within ten days. In summary: "
                       "nine days of delay, no communication, one request. Awaiting your kind reply, "
                       "distinct regards."),
        listening=("Capo: Come vanno le vendite?<br>Sofia: Sono il doppio dell'anno scorso, ma il "
                   "prezzo è in calo del due per cento: in altre parole, il margine resta sotto il "
                   "cinque per cento.<br>Capo: Su quale campione è quel dato?<br>Sofia: Mille "
                   "interviste, secondo l'indagine; il metodo non è dichiarato."),
        listening_gloss=("Boss: How are the sales going? Sofia: They are double last year's, but the "
                         "price is down by two per cent: in other words, the margin stays below five "
                         "per cent. Boss: On which sample is that figure? Sofia: A thousand "
                         "interviews, according to the survey; the method is not declared."),
        voice_tag=VOICE,
        idioms=[
            ("Il doppio", "the double", "twice as much"),
            ("In calo", "in fall", "falling"),
            ("Di conseguenza", "by consequence", "consequently"),
            ("Su un campione di", "on a sample of", "based on a sample of"),
            ("In riferimento a", "in reference to", "with reference to"),
            ("Il sottoscritto", "the undersigned", "the undersigned"),
            ("Per questi motivi", "for these reasons", "for these reasons"),
            ("In altre parole", "in other words", "in other words"),
            ("In sintesi", "in synthesis", "in summary"),
            ("Il prossimo passo", "the next step", "the next step"),
        ],
        mistakes=[
            ("Il 70% degli intervistati pensano che il prezzo sia giusto.", "Il 70% degli intervistati pensa che il prezzo sia giusto.", "The percentage is the subject and stays singular."),
            ("In sintesi, come ho già detto, in pratica è così.", "In sintesi: una richiesta, una data.", "A summary states the count; the markers do not stack."),
            ("Chiedo di essere rimborsato i soldi entro dieci giorni.", "Chiedo la restituzione delle spese entro dieci giorni.", "The claim is la restituzione delle spese, with one object."),
        ],
        task_title="Turn a complaint into a formal letter",
        task_instructions=("Take a real annoyance — a late delivery, a cancelled appointment, a bill "
                           "that does not add up — and write the Italian formal letter in three "
                           "paragraphs: the reference and the facts (espongo i fatti), the grounds (per "
                           "questi motivi) and the request with a date. Then rewrite the same content "
                           "as a five-line summary for your own file (in sintesi) and as one sentence "
                           "you would say out loud. If the spoken sentence is longer than the letter, "
                           "the letter is not finished."),
    ),
    "test": [
        ("translate_en", "Say: A third of the customers come from the web.", "Un terzo dei clienti arriva dal web."),
        ("translate_it", "Non solo i costi calano, ma anche i tempi si accorciano.", "Not only do the costs fall, but the times also shorten."),
        ("multiple_choice", "Which sentence is the correct formal opening?", "Egregio Dottore, in riferimento alla Sua del 3 maggio,"),
        ("fill_in_the_blank", "Per questi motivi chiedo la restituzione delle spese ___ dieci giorni.", "entro"),
        ("word_selection", "Select the Italian for 'on a sample of a thousand interviews'.", "su un campione di mille interviste"),
        ("error_correction", "Il 70% degli intervistati pensano che sia giusto.", "Il 70% degli intervistati pensa che sia giusto."),
        ("dialogue_completion", "Complete: In sintesi: tre richieste, ___ approvata. (only one)", "una sola"),
        ("matching", "Match ci rammarichiamo to its meaning.", "we regret"),
        ("reading_comprehension", "Il prezzo medio è in calo del 2%. Which direction is the price moving?", "down"),
        ("inference", "«Su quale campione?» — what is the speaker doing?", "challenging a figure's evidence"),
        ("main_idea", "In altre parole, non c'è spazio per un errore. What is this about?", "reformulating a margin warning"),
        ("detail_identification", "Provvederemo entro tre giorni lavorativi. How long does the repair take?", "three working days"),
    ],
}

HALFSTEPS["C1+"] = {
    "title": "Italian C1+ — Register, strategy and mediation",
    "native": NATIVE,
    "goals": [
        "Grade your commitment: what you know, what you are told, what you cannot confirm",
        "Use the diplomatic conditional and attenuation without disappearing behind them",
        "Recognise euphemism, keep the formal spoken register and translate between registers",
        "Mediate, dissent elegantly and write the note that closes a discussion",
    ],
    "units": [
        {"id": "C1+-U1", "title": "Precisione e impegno", "lessons": [
            L("Gradazione dell'impegno: mi risulta, mi consta",
              "Italian marks how strongly you own a claim: MI RISULTA · MI CONSTA · NON MI CONSTA · "
              "PER QUANTO NE SO. The same fact can be held at three distances, and the distance is "
              "the message.",
              [V("mi risulta", "mee ree-ZOOL-tah", "it appears to me, I understand", "phrase"),
               V("mi consta", "mee KOHN-stah", "I have it on record, I know", "phrase"),
               V("non mi consta", "nohn mee KOHN-stah", "I have no record of it", "phrase"),
               V("per quanto ne so", "per KWAHN-toh neh SOH", "as far as I know", "phrase"),
               V("la verifica", "lah veh-REE-fee-kah", "check, verification", "noun")],
              G("Commitment scale",
                "mi risulta che … · mi consta che … · non mi consta · per quanto ne so",
                "Mi risulta che la pratica sia chiusa; mi consta che il pagamento è partito; non mi "
                "consta nulla di diverso. risulta distances you from the source, consta puts your own "
                "record behind it, and non mi consta refuses to answer without calling anyone a liar.",
                [X("Mi risulta che la pratica sia chiusa.", "mee ree-ZOOL-tah keh lah PRAH-tee-kah SEE-ah KYOO-zah.", "I understand that the file is closed."),
                 X("Mi consta che il pagamento è partito.", "mee KOHN-stah keh eel pah-gah-MEN-toh eh par-TEE-toh.", "I have it on record that the payment went out."),
                 X("Non mi consta nulla di diverso.", "nohn mee KOHN-stah NOOL-lah dee dee-VER-soh.", "I have no record of anything different.")],
                [("Mi consta che forse la pratica è chiusa.", "Mi risulta che la pratica sia chiusa.", "consta claims a record; if there is a forse, the claim is risulta."),
                 ("Non mi consta, quindi è falso.", "Non mi consta.", "non mi consta states an absence of record, not a verdict.")]),
              [D("Analyst", "La pratica è chiusa?", "lah PRAH-tee-kah eh KYOO-zah?", "Is the file closed?"),
               D("Reviewer", "Mi risulta di sì, ma non mi consta per iscritto.", "mee ree-ZOOL-tah dee see, mah nohn mee KOHN-stah per ee-SKREET-toh.", "I understand so, but I have no written record of it."),
               D("Analyst", "Allora chiediamo la verifica.", "ahl-LOH-rah kyah-DYAH-moh lah veh-REE-fee-kah.", "Then let us ask for the verification."),
               D("Reviewer", "Per quanto ne so, arriva domani.", "per KWAHN-toh neh SOH, ahr-REE-vah doh-MAH-nee.", "As far as I know, it arrives tomorrow.")],
              WS("Commitment worksheet", [
                  T("Grade the claim.", ["I understand that the file is closed", "I have it on record that the payment went out"],
                    ["Mi risulta che la pratica sia chiusa.", "Mi consta che il pagamento è partito."]),
                  T("Refuse without accusing.", ["I have no record of anything different", "as far as I know"],
                    ["Non mi consta nulla di diverso.", "Per quanto ne so"]),
              ])),
            L("Il condizionale diplomatico: sarebbe opportuno",
              "The polite conditional moves a demand one step away from the speaker: SAREBBE "
              "OPPORTUNO · POTREMMO VALUTARE · CONVIENE FORSE. The request stays, the pressure drops.",
              [V("sarebbe opportuno", "sah-REB-beh ohp-por-TOO-noh", "it would be advisable", "phrase"),
               V("potremmo valutare", "poh-TREM-moh vah-loo-TAH-reh", "we could consider", "phrase"),
               V("conviene forse", "kohn-VYEH-neh FOR-seh", "perhaps it is worth", "phrase"),
               V("la proposta", "lah proh-POHS-tah", "proposal", "noun"),
               V("il margine", "eel MAR-jee-neh", "margin", "noun")],
              G("Diplomatic conditional",
                "sarebbe opportuno + infinito · potremmo valutare … · conviene forse …",
                "Sarebbe opportuno verificare i dati prima di decidere. Potremmo valutare due "
                "alternative e conviene forse sentire il cliente. Each sentence is a request wearing "
                "an observation, which is exactly what lets the other person agree without losing face.",
                [X("Sarebbe opportuno verificare i dati.", "sah-REB-beh ohp-por-TOO-noh veh-ree-fee-KAH-reh ee DAH-tee.", "It would be advisable to check the figures."),
                 X("Potremmo valutare due alternative.", "poh-TREM-moh vah-loo-TAH-reh DOO-eh ahl-ter-nah-TEE-veh.", "We could consider two alternatives."),
                 X("Conviene forse sentire il cliente.", "kohn-VYEH-neh FOR-seh sen-TEE-reh eel kly-EN-teh.", "It is perhaps worth hearing the client.")],
                [("Devi verificare i dati.", "Sarebbe opportuno verificare i dati.", "The diplomatic conditional removes the personal obligation."),
                 ("Potremmo valutare, dovete farlo subito.", "Potremmo valutare due alternative.", "Mixing a soft modal with a hard imperative undoes the register.")]),
              [D("Editor", "Il testo è pronto?", "eel TES-toh eh PROHN-toh?", "Is the text ready?"),
               D("Mediator", "Sarebbe opportuno verificare i dati prima di decidere.", "sah-REB-beh ohp-por-TOO-noh veh-ree-fee-KAH-reh ee DAH-tee PREE-mah dee deh-CHEE-deh-reh.", "It would be advisable to check the figures before deciding."),
               D("Editor", "Quanto tempo serve?", "KWAHN-toh TEM-poh SER-veh?", "How much time is needed?"),
               D("Mediator", "Potremmo valutare due alternative in una settimana.", "poh-TREM-moh vah-loo-TAH-reh DOO-eh ahl-ter-nah-TEE-veh een OO-nah set-tee-MAH-nah.", "We could consider two alternatives within a week.")],
              WS("Diplomacy worksheet", [
                  T("Soften the request.", ["it would be advisable to check the figures", "we could consider two alternatives"],
                    ["Sarebbe opportuno verificare i dati.", "Potremmo valutare due alternative."]),
                  T("Add the opening.", ["perhaps it is worth hearing the client", "the margin stays thin"],
                    ["Conviene forse sentire il cliente.", "Il margine resta sottile."]),
              ])),
            L("Attenuare senza sparire: un po', piuttosto, semmai",
              "Attenuation is not vagueness: E UN PO' CARO · PIUTTOSTO DIREI · SE MAI, NE PARLIAMO "
              "DOPO. Each word lowers the volume while keeping the claim findable.",
              [V("un po'", "oon poh", "a little, rather", "adverb"),
               V("piuttosto", "pyoot-TOHS-toh", "rather", "adverb"),
               V("semmai", "sem-MAHY", "if anything, possibly later", "adverb"),
               V("francamente", "frahn-kah-MEN-teh", "frankly", "adverb"),
               V("il tono", "eel TOH-noh", "tone", "noun")],
              G("Attenuation frame",
                "è un po' caro · direi piuttosto che … · semmai, ne parliamo dopo · francamente",
                "Il prezzo è un po' caro rispetto al mercato. Direi piuttosto che il problema è il "
                "tempo. Semmai, ne parliamo dopo la prova. Attenuation keeps the criticism on the table "
                "and gives the other person a chair at it.",
                [X("Il prezzo è un po' caro.", "eel PRET-tsoh eh oon poh KAH-roh.", "The price is a little high."),
                 X("Direi piuttosto che il problema è il tempo.", "dee-RAY pyoot-TOHS-toh keh eel proh-BLEH-mah eh eel TEM-poh.", "I would rather say the problem is the time."),
                 X("Semmai, ne parliamo dopo la prova.", "sem-MAHY, neh par-LYAH-moh DOH-poh lah PROH-vah.", "If anything, we discuss it after the trial.")],
                [("Il prezzo è caro, quindi è una truffa.", "Il prezzo è un po' caro rispetto al mercato.", "Attenuation keeps the comparison instead of the accusation."),
                 ("Semmai forse probabilmente potremmo…", "Semmai, ne parliamo dopo la prova.", "Three hedges in one sentence cancel each other.")]),
              [D("Reviewer", "Il prezzo è un po' caro.", "eel PRET-tsoh eh oon poh KAH-roh.", "The price is a little high."),
               D("Analyst", "Rispetto a cosa?", "rees-PET-toh ah KOH-zah?", "Relative to what?"),
               D("Reviewer", "Al mercato. Direi piuttosto che il problema è il tempo.", "ahl mer-KAH-toh. dee-RAY pyoot-TOHS-toh keh eel proh-BLEH-mah eh eel TEM-poh.", "To the market. I would rather say the problem is the time."),
               D("Analyst", "Semmai, ne parliamo dopo la prova.", "sem-MAHY, neh par-LYAH-moh DOH-poh lah PROH-vah.", "If anything, we discuss it after the trial.")],
              WS("Attenuation worksheet", [
                  T("Lower the volume.", ["the price is a little high", "I would rather say the problem is the time"],
                    ["Il prezzo è un po' caro.", "Direi piuttosto che il problema è il tempo."]),
                  T("Defer, do not dismiss.", ["if anything, we discuss it after the trial", "frankly, the margin is thin"],
                    ["Semmai, ne parliamo dopo la prova.", "Francamente, il margine è sottile."]),
              ])),
        ]},
        {"id": "C1+-U2", "title": "Registro e strategia", "lessons": [
            L("L'eufemismo e come smontarlo: esuberi, mobilità",
              "Institutional Italian softens what it means: ESUBERI · MOBILITÀ · RIORGANIZZAZIONE · "
              "RIDUZIONE DEL PERIMETRO. C1 reading translates the euphemism back into verbs, people "
              "and dates.",
              [V("l'esubero", "leh-ZOO-beh-roh", "redundancy, surplus staff", "noun"),
               V("la mobilità", "lah moh-bee-lee-TAH", "redeployment (formally: mobility)", "noun"),
               V("la riorganizzazione", "lah ree-or-gah-nee-tsah-TSYOH-neh", "reorganisation", "noun"),
               V("il perimetro", "eel peh-REE-meh-troh", "scope, perimeter", "noun"),
               V("smontare", "smon-TAH-reh", "to take apart, to dismantle", "verb")],
              G("Euphemism frame",
                "esuberi · mobilità · riorganizzazione · riduzione del perimetro",
                "«Riorganizzazione con ricorso alla mobilità» significa: alcune persone cambiano "
                "mansione, altre escono, e il perimetro si riduce. Smontare l'eufemismo significa "
                "riscrivere la frase con soggetti, verbi e date.",
                [X("«Riorganizzazione con ricorso alla mobilità».", "ree-or-gah-nee-tsah-TSYOH-neh kohn ree-KOR-soh AHL-lah moh-bee-lee-TAH.", "'Reorganisation with recourse to redeployment'."),
                 X("Tradotto: alcune persone cambiano mansione, altre escono.", "trah-DOT-toh: ahl-KOO-neh per-SOH-neh KAHM-byah-noh mahn-SYOH-neh, AHL-treh EH-skoh-noh.", "Translated: some people change role, others leave."),
                 X("Il perimetro si riduce di due reparti.", "eel peh-REE-meh-troh see ree-DOO-cheh dee DOO-eh reh-PAR-tee.", "The scope shrinks by two departments.")],
                [("L'azienda ha annunciato una riorganizzazione per crescere.", "L'azienda chiude due reparti; quaranta persone cambiano mansione.", "An announcement about growth names no verb, no number and no date."),
                 ("Esuberi volontari.", "Escono quaranta persone: venti volontarie, venti no.", "The adjective hides the count; the count is the fact.")]),
              [D("Analyst", "Come lo scrive l'azienda?", "KOH-meh loh SKREE-veh lahz-YEN-dah?", "How does the company write it?"),
               D("Editor", "«Riorganizzazione con ricorso alla mobilità».", "ree-or-gah-nee-tsah-TSYOH-neh kohn ree-KOR-soh AHL-lah moh-bee-lee-TAH.", "'Reorganisation with recourse to redeployment'."),
               D("Analyst", "E come lo diciamo noi?", "eh KOH-meh loh dee-CHAH-moh nohy?", "And how do we say it?"),
               D("Editor", "Alcune persone cambiano mansione, altre escono; il perimetro si riduce di due reparti.", "ahl-KOO-neh per-SOH-neh KAHM-byah-noh mahn-SYOH-neh, AHL-treh EH-skoh-noh; eel peh-REE-meh-troh see ree-DOO-cheh dee DOO-eh reh-PAR-tee.", "Some people change role, others leave; the scope shrinks by two departments.")],
              WS("Euphemism worksheet", [
                  T("Take the euphemism apart.", ["some people change role, others leave", "the scope shrinks by two departments"],
                    ["Alcune persone cambiano mansione, altre escono.", "Il perimetro si riduce di due reparti."]),
                  T("Name the fact.", ["forty people leave: twenty voluntarily", "the announcement names no verb and no date"],
                    ["Escono quaranta persone: venti volontarie.", "L'annuncio non nomina verbi né date."]),
              ])),
            L("Il discorso formale parlato: aprire, annunciare, chiudere",
              "Formal spoken Italian has a shape: SIGNORE E SIGNORI, VI RINGRAZIO · IL TEMA DI OGGI È "
              "· MI AVVIO A CONCLUDERE · GRAZIE PER L'ATTENZIONE. Naming the move keeps the room with you.",
              [V("mi avvio a concludere", "mee ahv-VEE-oh ah kohn-kloo-DEH-reh", "I am coming to a close", "phrase"),
               V("il tema", "eel TEH-mah", "theme, topic", "noun"),
               V("il filo", "eel FEE-loh", "thread (of an argument)", "noun"),
               V("la transizione", "lah trahn-zee-TSYOH-neh", "transition", "noun"),
               V("l'attenzione", "laht-ten-TSYOH-neh", "attention", "noun")],
              G("Formal spoken frame",
                "signore e signori, vi ringrazio · il tema di oggi è · come dicevo · mi avvio a concludere",
                "Signore e signori, vi ringrazio. Il tema di oggi è il margine. Come dicevo, tre dati "
                "reggono il filo del discorso; mi avvio a concludere. The listener always knows which "
                "move they are in.",
                [X("Il tema di oggi è il margine.", "eel TEH-mah dee OJ-jee eh eel MAR-jee-neh.", "Today's theme is the margin."),
                 X("Come dicevo, tre dati reggono il filo.", "KOH-meh dee-CHEH-voh, treh DAH-tee RED-joh-noh eel FEE-loh.", "As I was saying, three figures hold the thread."),
                 X("Mi avvio a concludere.", "mee ahv-VEE-oh ah kohn-kloo-DEH-reh.", "I am coming to a close.")],
                [("Allora, insomma, boh, cominciamo.", "Signore e signori, vi ringrazio.", "The formal opening thanks the room before the first content sentence."),
                 ("Ho finito.", "Mi avvio a concludere.", "A close is announced before it arrives.")]),
              [D("Editor", "Come apro l'intervento?", "KOH-meh AH-proh leen-ter-VEN-toh?", "How do I open the talk?"),
               D("Mediator", "«Signore e signori, vi ringrazio. Il tema di oggi è il margine.»", "see-NYOH-reh eh see-NYOH-ree, vee reen-GRAH-tsyoh. eel TEH-mah dee OJ-jee eh eel MAR-jee-neh.", "'Ladies and gentlemen, thank you. Today's theme is the margin.'"),
               D("Editor", "E per chiudere?", "eh per KYOO-deh-reh?", "And to close?"),
               D("Mediator", "«Mi avvio a concludere: tre dati, una raccomandazione.»", "mee ahv-VEE-oh ah kohn-kloo-DEH-reh: treh DAH-tee, OO-nah rahk-koh-mahn-dah-TSYOH-neh.", "'I am coming to a close: three figures, one recommendation.'")],
              WS("Talk worksheet", [
                  T("Open the talk.", ["thank you, ladies and gentlemen", "today's theme is the margin"],
                    ["Vi ringrazio, signore e signori.", "Il tema di oggi è il margine."]),
                  T("Close the talk.", ["I am coming to a close", "three figures, one recommendation"],
                    ["Mi avvio a concludere.", "tre dati, una raccomandazione"]),
              ])),
            L("Tradurre il registro: dal titolo al rapporto",
              "A headline piles nouns; a report builds sentences: «DISOCUPAZIONE IN CALO» becomes IL "
              "TASSO DI DISOCUPAZIONE È SCESO DELLO 0,4% NEL SECONDO TRIMESTRE, SECONDO L'ISTAT.",
              [V("il titolo", "eel TEE-toh-loh", "headline", "noun"),
               V("il rapporto", "eel rahp-POR-toh", "report", "noun"),
               V("il trimestre", "eel tree-MES-treh", "quarter", "noun"),
               V("la variazione", "lah vah-ryah-TSYOH-neh", "change", "noun"),
               V("l'ordine di grandezza", "LOR-dee-neh dee grahn-DET-tsah", "order of magnitude", "noun")],
              G("Register translation",
                "titolo: «disoccupazione in calo» · rapporto: «il tasso è sceso dello 0,4% nel secondo trimestre»",
                "Il titolo annuncia, il rapporto precisa: variazione, periodo, fonte. Tradurre il "
                "registro significa restituire al lettore l'ordine di grandezza che il titolo aveva "
                "compresso.",
                [X("Titolo: «Disoccupazione in calo».", "TEE-toh-loh: dee-zoh-koo-pah-TSYOH-neh een KAH-loh.", "Headline: 'unemployment falling'."),
                 X("Rapporto: «Il tasso è sceso dello 0,4% nel secondo trimestre».", "rahp-POR-toh: eel TAHS-soh eh SHEH-zoh DEL-loh ZEH-roh VIR-goh-lah KWAT-tro per CHEN-toh nel seh-KOHN-doh tree-MES-treh.", "Report: 'the rate fell by 0.4% in the second quarter'."),
                 X("Secondo l'ISTAT.", "seh-KOHN-doh lees-TAHT.", "According to ISTAT.")],
                [("Il titolo dice tutto: disoccupazione in calo, quindi è tutto risolto.", "Titolo e rapporto dicono due cose diverse: il titolo annuncia, il rapporto misura.", "A headline is a direction; the report is a number, a period and a source."),
                 ("Il tasso è sceso del 0,4% nel secondo trimestre, perché c'è la ripresa.", "Il tasso è sceso dello 0,4% nel secondo trimestre.", "The report states the variation; the cause is a separate sentence.")]),
              [D("Analyst", "Il titolo dice «disoccupazione in calo».", "eel TEE-toh-loh DEE-cheh dee-zoh-koo-pah-TSYOH-neh een KAH-loh.", "The headline says 'unemployment falling'."),
               D("Reviewer", "Il rapporto invece dà variazione, periodo e fonte.", "eel rahp-POR-toh een-VEH-cheh dah vah-ryah-TSYOH-neh, peh-RYOH-doh eh FOHN-teh.", "The report gives the change, the period and the source."),
               D("Analyst", "Quindi riscriviamo: «il tasso è sceso dello 0,4% nel secondo trimestre».", "KWEEN-dee ree-skree-VYAH-moh: eel TAHS-soh eh SHEH-zoh DEL-loh ZEH-roh VIR-goh-lah KWAT-tro per CHEN-toh nel seh-KOHN-doh tree-MES-treh.", "So we rewrite it: 'the rate fell by 0.4% in the second quarter'."),
               D("Reviewer", "Secondo l'ISTAT: senza fonte, il numero non entra.", "seh-KOHN-doh lees-TAHT: SEN-tsah FOHN-teh, eel NOO-meh-roh nohn EN-trah.", "According to ISTAT: without a source the number does not go in.")],
              WS("Register worksheet", [
                  T("Turn the headline into a report sentence.", ["unemployment falling", "prices rising"],
                    ["Il tasso di disoccupazione è sceso dello 0,4% nel secondo trimestre.", "I prezzi sono aumentati dell'1,2% nel trimestre."]),
                  T("Turn the report sentence into a headline.", ["the rate fell by 0.4%", "consumption fell"],
                    ["Disoccupazione in calo.", "Consumi in calo."]),
              ])),
        ]},
        {"id": "C1+-U3", "title": "Mediare e chiudere", "lessons": [
            L("La replica elegante: mi permetto di dissentire",
              "Elegant dissent names the respect first and the disagreement second: CON TUTTO IL "
              "RISPETTO · MI PERMETTO DI DISSENTIRE · SE MI È CONSENTITO. Then the reason, in one sentence.",
              [V("con tutto il rispetto", "kohn TOOT-toh eel ree-SPET-toh", "with all due respect", "phrase"),
               V("mi permetto di", "mee per-MET-toh dee", "I take the liberty of", "phrase"),
               V("dissentire", "dees-sen-TEE-reh", "to dissent", "verb"),
               V("se mi è consentito", "seh mee eh kohn-SEN-tee-toh", "if I may", "phrase"),
               V("il rilievo", "eel ree-LYEH-voh", "objection, remark", "noun")],
              G("Elegant dissent",
                "con tutto il rispetto · mi permetto di dissentire · se mi è consentito, un rilievo",
                "Con tutto il rispetto, mi permetto di dissentire su un punto. Se mi è consentito, il "
                "rilievo non è sul merito ma sui tempi. The formula and the point arrive in that "
                "order, and the argument is never the person.",
                [X("Con tutto il rispetto, mi permetto di dissentire.", "kohn TOOT-toh eel ree-SPET-toh, mee per-MET-toh dee dees-sen-TEE-reh.", "With all due respect, I take the liberty of dissenting."),
                 X("Se mi è consentito, un rilievo sui tempi.", "seh mee eh kohn-SEN-tee-toh, oon ree-LYEH-voh soo ee TEM-pee.", "If I may, an objection on the timing."),
                 X("Il rilievo non è sul merito.", "eel ree-LYEH-voh nohn eh sool MEH-ree-toh.", "The objection is not on the substance.")],
                [("Con tutto il rispetto, lei non capisce niente.", "Con tutto il rispetto, mi permetto di dissentire su un punto.", "The formula opens a disagreement; it does not license an insult."),
                 ("Mi permetto dissentire.", "Mi permetto di dissentire.", "The phrase is permettersi di + infinitive.")]),
              [D("Reviewer", "Con tutto il rispetto, mi permetto di dissentire.", "kohn TOOT-toh eel ree-SPET-toh, mee per-MET-toh dee dees-sen-TEE-reh.", "With all due respect, I take the liberty of dissenting."),
               D("Editor", "Su quale punto?", "soo KWAH-leh POON-toh?", "On which point?"),
               D("Reviewer", "Se mi è consentito, il rilievo non è sul merito ma sui tempi.", "seh mee eh kohn-SEN-tee-toh, eel ree-LYEH-voh nohn eh sool MEH-ree-toh mah soo ee TEM-pee.", "If I may, the objection is not on the substance but on the timing."),
               D("Editor", "Allora rivediamo il calendario.", "ahl-LOH-rah ree-veh-DYAH-moh eel kah-len-DAH-ryoh.", "Then let us revise the schedule.")],
              WS("Dissent worksheet", [
                  T("Dissent elegantly.", ["with all due respect, I take the liberty of dissenting", "if I may, an objection on the timing"],
                    ["Con tutto il rispetto, mi permetto di dissentire.", "Se mi è consentito, un rilievo sui tempi."]),
                  T("Place the objection.", ["the objection is not on the substance", "let us revise the schedule"],
                    ["Il rilievo non è sul merito.", "Rivediamo il calendario."]),
              ])),
            L("La nota di sintesi: conclusioni e raccomandazioni",
              "A note closes in two headed paragraphs: CONCLUSIONI (what the evidence supports) and "
              "RACCOMANDAZIONI (what someone should do, by when). Nothing else belongs at the end.",
              [V("la conclusione", "lah kohn-kloo-ZYOH-neh", "conclusion", "noun"),
               V("la raccomandazione", "lah rahk-koh-mahn-dah-TSYOH-neh", "recommendation", "noun"),
               V("l'evidenza", "leh-vee-DEN-tsah", "evidence", "noun"),
               V("il destinatario", "eel des-tee-nah-TAH-ryoh", "addressee", "noun"),
               V("la scadenza", "lah skah-DEN-tsah", "deadline", "noun")],
              G("Note frame",
                "Conclusioni: … · Raccomandazioni: 1) … entro … · Il destinatario è …",
                "Conclusioni: l'evidenza sostiene la prova su due reparti. Raccomandazioni: 1) partire "
                "con due persone entro marzo; 2) verificare i costi a giugno. A note that ends without "
                "a name and a date has not ended.",
                [X("Conclusioni: l'evidenza sostiene la prova.", "kohn-kloo-ZYOH-nee: leh-vee-DEN-tsah sohs-TYEH-neh lah PROH-vah.", "Conclusions: the evidence supports the trial."),
                 X("Raccomandazioni: partire con due persone entro marzo.", "rahk-koh-mahn-dah-TSYOH-nee: par-TEE-reh kohn DOO-eh per-SOH-neh EN-troh MAR-tsoh.", "Recommendations: start with two people by March."),
                 X("Il destinatario è la direzione.", "eel des-tee-nah-TAH-ryoh eh lah dee-reh-TSYOH-neh.", "The addressee is the management.")],
                [("Conclusioni: tutto sembra positivo e interessante.", "Conclusioni: l'evidenza sostiene la prova su due reparti.", "A conclusion states what the evidence supports, not an impression."),
                 ("Raccomandazioni: valutare possibili azioni future.", "Raccomandazioni: partire con due persone entro marzo.", "A recommendation names an action and a date.")]),
              [D("Mediator", "Come chiudo la nota?", "KOH-meh KYOO-doh lah NOH-tah?", "How do I close the note?"),
               D("Analyst", "Con due paragrafi: conclusioni e raccomandazioni.", "kohn DOO-eh pah-RAH-grah-fee: kohn-kloo-ZYOH-nee eh rahk-koh-mahn-dah-TSYOH-nee.", "With two paragraphs: conclusions and recommendations."),
               D("Mediator", "E il destinatario?", "eh eel des-tee-nah-TAH-ryoh?", "And the addressee?"),
               D("Analyst", "La direzione, con una data: entro marzo.", "lah dee-reh-TSYOH-neh, kohn OO-nah DAH-tah: EN-troh MAR-tsoh.", "Management, with a date: by March.")],
              WS("Note worksheet", [
                  T("Write the conclusions.", ["the evidence supports the trial", "on two departments"],
                    ["L'evidenza sostiene la prova.", "su due reparti"]),
                  T("Write the recommendations.", ["start with two people by March", "check the costs in June"],
                    ["Partire con due persone entro marzo.", "Verificare i costi a giugno."]),
              ])),
            L("La sintesi di una tavola rotonda: chi ha detto cosa",
              "A round-table summary attributes, not repeats: L'ANALISTA HA RILEVATO CHE … · L'EDITOR "
              "HA OBIETTATO CHE … · È EMERSO UN PUNTO COMUNE. Report who said what, not what you think.",
              [V("la tavola rotonda", "lah TAH-voh-lah roh-TOHN-dah", "round table", "noun"),
               V("rilevare", "ree-leh-VAH-reh", "to note, to observe", "verb"),
               V("obiettare", "oh-byet-TAH-reh", "to object", "verb"),
               V("emergere", "eh-MER-jeh-reh", "to emerge", "verb"),
               V("il punto comune", "eel POON-toh koh-MOO-neh", "common ground", "noun")],
              G("Round-table frame",
                "l'analista ha rilevato che … · l'editor ha obiettato che … · è emerso un punto comune",
                "L'analista ha rilevato che il margine è sottile; l'editor ha obiettato che i tempi "
                "sono lunghi. È emerso un punto comune: partire con una prova. Attribution keeps the "
                "summary honest and the readers able to check the room.",
                [X("L'analista ha rilevato che il margine è sottile.", "lah-NAH-lees-tah ah ree-leh-VAH-toh keh eel MAR-jee-neh eh sot-TEE-leh.", "The analyst noted that the margin is thin."),
                 X("L'editor ha obiettato che i tempi sono lunghi.", "leh-dee-tohr ah oh-byet-TAH-toh keh ee TEM-pee SOH-noh LOON-ghee.", "The editor objected that the timelines are long."),
                 X("È emerso un punto comune.", "eh eh-MER-soh oon POON-toh koh-MOO-neh.", "A common ground emerged.")],
                [("Tutti hanno detto che va bene.", "L'analista ha rilevato che il margine è sottile; l'editor ha obiettato che i tempi sono lunghi.", "A summary attributes; «everyone agreed» is not a summary."),
                 ("È emerso un punto comune: secondo me bisogna partire.", "È emerso un punto comune: partire con una prova.", "The summary reports the room, not the writer's opinion.")]),
              [D("Mediator", "Come riassumo la tavola rotonda?", "KOH-meh ree-AHS-soo-moh lah TAH-voh-lah roh-TOHN-dah?", "How do I summarise the round table?"),
               D("Reviewer", "Attribuisci: «l'analista ha rilevato che …».", "aht-tree-BWEES-shee: lah-NAH-lees-tah ah ree-leh-VAH-toh keh.", "Attribute: 'the analyst noted that …'."),
               D("Mediator", "E se non sono d'accordo?", "eh seh nohn SOH-noh dahk-KOR-doh?", "And if I disagree?"),
               D("Reviewer", "Lo scrivi in una nota tua, non nella sintesi.", "loh SKREE-vee een OO-nah NOH-tah TOO-ah, nohn NEL-lah SEEN-teh-zee.", "You write that in your own note, not in the summary.")],
              WS("Round-table worksheet", [
                  T("Attribute the points.", ["the analyst noted that the margin is thin", "the editor objected that the timelines are long"],
                    ["L'analista ha rilevato che il margine è sottile.", "L'editor ha obiettato che i tempi sono lunghi."]),
                  T("State the common ground.", ["a common ground emerged: start with a trial", "your own opinion goes in a separate note"],
                    ["È emerso un punto comune: partire con una prova.", "La tua opinione va in una nota separata."]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Italian institutional prose and Italian speech run at different temperatures, and C1+ "
                 "work lives in the gap: the same decision is «una riorganizzazione con ricorso alla "
                 "mobilità» on paper and «due reparti chiudono» in the corridor. Reading the register "
                 "means being able to move the same content between the two — and knowing which one "
                 "the person in front of you is entitled to hear."),
        source_url="https://en.wikipedia.org/wiki/Register_(sociolinguistics)",
        reading=("Mi risulta che la nota sia pronta; mi consta però che i dati non sono verificati. "
                 "Sarebbe opportuno chiudere la verifica prima della riunione. Il titolo annuncia "
                 "«margine sotto pressione», mentre il rapporto dice che il margine è sceso di un "
                 "punto; in sintesi, il rilievo non è sul merito ma sui tempi. Mi avvio a concludere: "
                 "conclusioni e raccomandazioni sono due paragrafi separati, con una data e un "
                 "destinatario."),
        reading_gloss=("I understand that the note is ready; I have it on record, though, that the "
                       "figures are not verified. It would be advisable to close the check before the "
                       "meeting. The headline announces 'margin under pressure', while the report says "
                       "the margin fell by one point; in summary, the objection is not on the substance "
                       "but on the timing. I am coming to a close: conclusions and recommendations are "
                       "two separate paragraphs, with a date and an addressee."),
        listening=("Editor: Con tutto il rispetto, mi permetto di dissentire.<br>Reviewer: Su quale "
                   "punto?<br>Editor: Se mi è consentito, il rilievo non è sul merito ma sui tempi: "
                   "sarebbe opportuno verificare i dati prima della riunione.<br>Reviewer: D'accordo; "
                   "allora mi avvio a concludere con due raccomandazioni."),
        listening_gloss=("Editor: With all due respect, I take the liberty of dissenting. Reviewer: On "
                         "which point? Editor: If I may, the objection is not on the substance but on "
                         "the timing: it would be advisable to check the figures before the meeting. "
                         "Reviewer: Agreed; then I am coming to a close with two recommendations."),
        voice_tag=VOICE,
        idioms=[
            ("Mi risulta", "it results to me", "I understand, as far as I know"),
            ("Mi consta", "it is established to me", "I have it on record"),
            ("Sarebbe opportuno", "it would be advisable", "it would be advisable"),
            ("Un po' caro", "a bit dear", "a little expensive"),
            ("Semmai", "if ever", "if anything, possibly later"),
            ("Con tutto il rispetto", "with all respect", "with all due respect"),
            ("Mi permetto di", "I allow myself to", "I take the liberty of"),
            ("In sintesi", "in synthesis", "in summary"),
            ("Mi avvio a concludere", "I set off to conclude", "I am coming to a close"),
            ("Punto comune", "common point", "common ground"),
        ],
        mistakes=[
            ("Mi consta che forse la pratica è chiusa.", "Mi risulta che la pratica sia chiusa.", "consta claims a record; with a forse the claim drops to risulta."),
            ("Sarebbe opportuno che tu verifichi subito i dati.", "Sarebbe opportuno verificare i dati prima della riunione.", "The impersonal conditional does not turn into a personal order."),
            ("Raccomandazioni: valutare possibili azioni future.", "Raccomandazioni: partire con due persone entro marzo.", "A recommendation names an action and a date."),
        ],
        task_title="Mediate one decision between two registers",
        task_instructions=("Take a decision that has been described to you in institutional language — a "
                           "notice, a memo, a press line — and produce three texts in Italian: (1) the "
                           "same content in plain verbs, subjects and dates, (2) a formal note with "
                           "Conclusioni and Raccomandazioni, each recommendation carrying an owner and "
                           "a deadline, and (3) the ten lines you would say out loud in the meeting, "
                           "including one elegant dissent (con tutto il rispetto, mi permetto di "
                           "dissentire) and one attribution (l'analista ha rilevato che …). If the "
                           "spoken version contains a word that only exists on paper, mediation is "
                           "not finished."),
    ),
    "test": [
        ("translate_en", "Say: I have it on record that the payment went out.", "Mi consta che il pagamento è partito."),
        ("translate_it", "Sarebbe opportuno verificare i dati prima della riunione.", "It would be advisable to check the figures before the meeting."),
        ("multiple_choice", "Which line is the elegant dissent?", "Con tutto il rispetto, mi permetto di dissentire."),
        ("fill_in_the_blank", "Semmai, ne parliamo ___ la prova.", "dopo"),
        ("word_selection", "Select the plain-language version of «riorganizzazione con ricorso alla mobilità».", "alcune persone cambiano mansione, altre escono"),
        ("error_correction", "Mi consta che forse la pratica è chiusa.", "Mi risulta che la pratica sia chiusa."),
        ("dialogue_completion", "Complete: Raccomandazioni: partire con due persone ___ marzo.", "entro"),
        ("matching", "Match punto comune to its meaning.", "common ground"),
        ("reading_comprehension", "Il tasso è sceso dello 0,4% nel secondo trimestre. Which quarter?", "the second"),
        ("inference", "«Mi risulta di sì, ma non mi consta per iscritto» — what is the speaker doing?", "grading their commitment to a claim"),
        ("main_idea", "L'analista ha rilevato che il margine è sottile; l'editor ha obiettato che i tempi sono lunghi. What is this?", "attributed round-table summary"),
        ("detail_identification", "Mi avvio a concludere: tre dati, una raccomandazione. How many recommendations?", "one"),
    ],
}

# -*- coding: utf-8 -*-
"""PHASE 1 depth for French (`fr`).

Authored as specs for `tools/author-depth.py` through the helpers in
`tools/depth_kit.py`. Everything here is language-specific content: six CEFR
`extra` blocks, the eighteen third lessons that bring every A1-C2 unit to the
schema minimum, and the five half-step rungs A1+ .. C1+.

Voice: fr-FR. Speakers: Léa and Théo for A1-B2; role names are used higher up.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # tools/ on the path
from depth_kit import D, EXTRA, G, L, T, V, WS, X   # noqa: E402

CODE = "fr"
NAME = "French"
NATIVE = "Français"
PHASE = 1
SCRIPT = "Latin with French diacritics (é è ê à ç ù î ô û œ « »)"
VOICE = "fr-FR"
SKILL = ("French: grammatical gender and agreement, the passé composé/imparfait split, "
         "the two registers of tu and vous, and the nasal vowels that make liaison audible")

EXTRAS = {}
THIRD = {}
HALFSTEPS = {}


EXTRAS["A1"] = EXTRA(
    culture=("Bonjour is not a word, it is a door: French opens every exchange with it and "
             "closes with au revoir. The tu/vous choice is made on the first sentence — vous for "
             "a stranger, a shopkeeper or anyone older, tu for family, friends and classmates who "
             "have offered it."),
    source_url="https://en.wikipedia.org/wiki/French_language",
    reading=("Léa arrive au café le matin. « Bonjour, un café, s'il vous plaît. » Le serveur "
             "répond : « Bonjour ! Et avec ça ? » Elle prend un croissant et demande l'heure. "
             "« Il est huit heures et quart. » Elle dit merci, au revoir, et va au travail à "
             "pied, parce que le bureau est tout près."),
    reading_gloss=("Léa arrives at the café in the morning. 'Hello, a coffee, please.' The "
                   "waiter answers: 'Hello! And with that?' She takes a croissant and asks the "
                   "time. 'It is a quarter past eight.' She says thank you, goodbye, and walks to "
                   "work, because the office is very close."),
    listening=("Léa: Bonjour, comment ça va ?<br>Théo: Ça va bien, merci. Et toi ?<br>"
               "Léa: Ça va. Tu t'appelles comment, déjà ?<br>Théo: Théo. Enchanté !"),
    listening_gloss=("Léa: Hello, how are you? Théo: I'm fine, thanks. And you? Léa: Fine. What "
                     "is your name again? Théo: Théo. Nice to meet you!"),
    voice_tag=VOICE,
    idioms=[
        ("Bonjour", "good day", "hello (the default greeting)"),
        ("Au revoir", "to the seeing-again", "goodbye"),
        ("S'il vous plaît", "if it pleases you", "please (formal)"),
        ("Merci beaucoup", "thanks a lot", "thank you very much"),
        ("De rien", "of nothing", "you're welcome"),
        ("Comment ça va ?", "how does it go", "how are you?"),
        ("Ça va", "it goes", "fine / it's OK"),
        ("Enchanté", "enchanted", "pleased to meet you"),
        ("Excusez-moi", "excuse me", "excuse me (formal)"),
        ("À bientôt", "to soon", "see you soon"),
    ],
    mistakes=[
        ("Bonjour, comment allez-tu ?", "Bonjour, comment allez-vous ? / Bonjour, comment vas-tu ?",
         "The vous form and the tu form cannot mix inside one question."),
        ("Merci vous.", "Merci.", "Merci takes no object; to insist, use merci beaucoup."),
        ("Je m'appelle je suis Léa.", "Je m'appelle Léa. / Je suis Léa.", "Two introductions; use one."),
    ],
    task_title="Meet someone twice",
    task_instructions=("Write the same introduction twice: once at a party to someone your age "
                       "(tu, first name) and once at a doctor's reception desk (vous, surname). "
                       "Keep both to four lines, read them aloud, and notice that the politeness "
                       "lives in the pronoun, not in the adjectives."),
)

EXTRAS["A2"] = EXTRA(
    culture=("The French meal is a timetable: déjeuner sits at noon, dîner arrives at eight or "
             "later, and the café between them is a place to stand, not to linger over dessert. "
             "« Je prends un café » orders; « je voudrais » softens; « l'addition, s'il vous "
             "plaît » ends the meal and, in a Parisian café, also ends your right to the table."),
    source_url="https://en.wikipedia.org/wiki/French_cuisine",
    reading=("Au restaurant, le serveur apporte la carte. Léa prend une entrée et un plat, Théo "
             "un plat et un dessert. « Et comme boisson ? — Une carafe d'eau, s'il vous plaît. » "
             "Le pain est gratuit, la carafe aussi. À la fin, Théo demande l'addition, partage "
             "et laisse un petit pourboire, car le service est déjà compris."),
    reading_gloss=("At the restaurant, the waiter brings the menu. Léa takes a starter and a main, "
                   "Théo a main and a dessert. 'And to drink? — A jug of water, please.' The "
                   "bread is free, and so is the jug. At the end Théo asks for the bill, splits "
                   "it and leaves a small tip, since service is already included."),
    listening=("Théo: Qu'est-ce que tu prends ?<br>Léa: Je voudrais le menu du jour.<br>"
               "Théo: Et comme boisson ?<br>Léa: Une carafe d'eau. Et l'addition est comprise ?"),
    listening_gloss=("Théo: What are you having? Léa: I would like the menu of the day. Théo: And "
                     "to drink? Léa: A jug of water. And is the bill included?"),
    voice_tag=VOICE,
    idioms=[
        ("Je voudrais", "I would want", "I would like (polite ordering)"),
        ("Le menu du jour", "the menu of the day", "the set menu"),
        ("La carte", "the card", "the menu (full list)"),
        ("L'addition", "the addition", "the bill"),
        ("Le pourboire", "the for-drink", "a tip"),
        ("Gratuit", "free of charge", "free"),
        ("Ça fait combien ?", "that makes how much?", "how much is it in total?"),
        ("Je prends", "I take", "I'll have"),
        ("À emporter", "to take away", "takeaway"),
        ("Bon appétit", "good appetite", "enjoy your meal"),
    ],
    mistakes=[
        ("Je veux un café.", "Je voudrais un café.", "Je veux is blunt; je voudrais is the standard polite order."),
        ("Je vais prendre le addition.", "Je vais payer l'addition. / L'addition, s'il vous plaît.", "In an order, prendre takes the dish; the bill is asked for."),
        ("Le menu est chez moi.", "Le menu, s'il vous plaît. (the set menu)", "menu in French is the fixed-price meal, not the list of dishes."),
    ],
    task_title="Order a two-course meal out loud",
    task_instructions=("Write a nine-line restaurant scene: greet, ask for la carte, order a "
                       "starter and a main with je voudrais, order drinks, ask what comes with the "
                       "dish, ask for the bill, ask whether service is included, and leave. Then "
                       "rewrite the same scene as you would say it to a friend at home (tu, je "
                       "prends) and compare the two registers."),
)

EXTRAS["B1"] = EXTRA(
    culture=("The French working day is legally 35 hours, and the calendar compensates: RTT days, "
             "a long lunch, and August, when half of Paris changes address. The vocabulary of the "
             "office is therefore as much about time as about tasks — la pause déjeuner, les "
             "horaires, les congés — and asking a colleague for a favour starts with a look at "
             "the clock, not with the request."),
    source_url="https://en.wikipedia.org/wiki/35-hour_workweek",
    reading=("Au bureau, la journée commence par un café et la question des horaires. Léa "
             "travaille de neuf heures à dix-sept heures, avec une vraie pause déjeuner. Elle a "
             "des RTT et prend trois semaines de congés en août. Théo, lui, est en télétravail le "
             "vendredi : il finit plus tôt et répond aux courriels le soir, ce qui ne plaît pas à "
             "tout le monde."),
    reading_gloss=("At the office the day starts with a coffee and the question of hours. Léa "
                   "works from nine to five, with a real lunch break. She has RTT days and takes "
                   "three weeks of leave in August. Théo works from home on Fridays: he finishes "
                   "earlier and answers emails in the evening, which does not please everyone."),
    listening=("Léa: Tu peux m'aider sur le dossier ?<br>Théo: Oui, mais pas avant deux heures.<br>"
               "Léa: Après la pause déjeuner, alors.<br>Théo: Parfait. Je t'envoie ma réponse cet après-midi."),
    listening_gloss=("Léa: Can you help me with the file? Théo: Yes, but not before two. Léa: "
                     "After the lunch break, then. Théo: Perfect. I'll send you my answer this "
                     "afternoon."),
    voice_tag=VOICE,
    idioms=[
        ("La pause déjeuner", "the lunch break", "the lunch break"),
        ("Les horaires", "the hours", "the working hours"),
        ("Prendre des congés", "to take leaves", "to take holiday"),
        ("Être en télétravail", "to be in remote work", "to work from home"),
        ("Un dossier", "a file", "a case, a project file"),
        ("Ça marche", "it walks", "that works, OK"),
        ("Je m'en occupe", "I occupy myself with it", "I'll take care of it"),
        ("Coup de main", "a hand blow", "a helping hand"),
        ("À la bourre", "at the slack", "running late (familiar)"),
        ("Mettre les bouchées doubles", "to put double mouthfuls", "to put in double effort"),
    ],
    mistakes=[
        ("Je travaille ici depuis trois ans (for a job you still hold) — acceptable, but the spoken norm is « ça fait trois ans que je travaille ici ».", "Ça fait trois ans que je travaille ici.", "Spoken French prefers the ça fait … que frame for duration up to now."),
        ("Je prends mes congés en août depuis dix ans.", "Ça fait dix ans que je prends mes congés en août.", "Duration up to now: ça fait + time + que."),
        ("Je suis d'accord avec toi, mais je suis pas d'accord sur le budget (double 'je suis').", "Je suis d'accord avec toi, mais pas sur le budget.", "Do not repeat the verb when the subject has not changed."),
    ],
    task_title="Plan a week of work in French",
    task_instructions=("Write seven French lines that plan your week the way a colleague would "
                       "hear it: the hours you work, one RTT or holiday day, a remote day, one "
                       "request for a hand with a file and its reply, and one thing you will take "
                       "care of yourself. Then say the same plan to a friend in tu form and note "
                       "which words change."),
)

EXTRAS["B2"] = EXTRA(
    culture=("French argument has a taste for the counter-example: a claim is offered with « il "
             "est vrai que », then turned with « cela dit » or « en revanche ». The politeness of "
             "disagreeing lies in conceding the true part first, which is why a French debate can "
             "sound heated and still end in a handshake over a coffee."),
    source_url="https://en.wikipedia.org/wiki/French_culture",
    reading=("« Il est vrai que la mesure a réduit les coûts », dit la syndicaliste. « Cela dit, "
             "elle a augmenté la charge de travail, et personne n'a mesuré cet effet. » Le "
             "directeur répond que les chiffres sont provisoires. En revanche, il accepte une "
             "évaluation indépendante à la rentrée : deux positions, un accord partiel, et une "
             "date pour vérifier."),
    reading_gloss=("'It is true that the measure reduced costs,' says the union representative. "
                   "'That said, it increased the workload, and nobody has measured that effect.' "
                   "The director replies that the figures are provisional. However, he accepts an "
                   "independent evaluation in September: two positions, a partial agreement, and "
                   "a date to check it."),
    listening=("Théo: Il est vrai que ça coûte cher.<br>Léa: Cela dit, on ne peut pas attendre encore un an.<br>"
               "Théo: D'accord sur le principe. En revanche, il faut un calendrier.<br>"
               "Léa: Un point par mois, ça te va ?"),
    listening_gloss=("Théo: It is true that it costs a lot. Léa: That said, we cannot wait "
                     "another year. Théo: Agreed in principle. However, we need a timetable. Léa: "
                     "One checkpoint a month, does that suit you?"),
    voice_tag=VOICE,
    idioms=[
        ("Cela dit", "that said", "that said"),
        ("En revanche", "in return", "on the other hand"),
        ("Il est vrai que", "it is true that", "granted that"),
        ("D'accord sur le principe", "agreed on the principle", "agreed in principle"),
        ("Mettre les points sur les i", "to put the dots on the i's", "to spell things out"),
        ("Un point d'accord", "a point of agreement", "a point of agreement"),
        ("Tomber d'accord", "to fall in agreement", "to come to an agreement"),
        ("Prendre du recul", "to take some distance", "to step back"),
        ("À la rentrée", "at the return", "in September, when work resumes"),
        ("Remettre en question", "to put back into question", "to call into question"),
    ],
    mistakes=[
        ("Cela dit, mais en revanche, il faut un calendrier.", "Cela dit, il faut un calendrier.", "One contrast marker per sentence."),
        ("Je suis pas d'accord du tout mais je respecte.", "Je ne suis pas d'accord, même si je respecte votre position.", "State the limit of the disagreement; empty courtesy sounds dismissive."),
        ("Il est vrai que c'est cher, donc on laisse tomber.", "Il est vrai que c'est cher ; en revanche, le risque est plus grand si on attend.", "Concede to keep the argument, not to abandon it."),
    ],
    task_title="Disagree in writing, twice",
    task_instructions=("Write a six-line French note about a decision you find partly wrong: "
                       "concede with il est vrai que … , turn with cela dit / en revanche, offer a "
                       "counter-measure, and close with one point of agreement and a date. Then "
                       "rewrite the same note with every concession removed and compare which "
                       "version a real reader would act on."),
)

EXTRAS["C1"] = EXTRA(
    culture=("Administrative French loves the noun: « la mise en œuvre de la réforme » hides an "
             "actor, a verb and a responsibility. C1 work is learning to un-nominalise — to read "
             "« procéder à l'actualisation » and hear « mettre à jour » — and to write in a "
             "register that stays impersonal without disappearing entirely."),
    source_url="https://en.wikipedia.org/wiki/French_grammar",
    reading=("Le rapport indique que « la mise en œuvre du dispositif fera l'objet d'une "
             "évaluation ». Traduit en français courant : quelqu'un devra vérifier si la mesure "
             "fonctionne, et le rapport ne dit pas qui. C'est précisément ce flou que la note de "
             "synthèse attaque : pour chaque phrase au passif, on écrit le verbe, le sujet et la "
             "date."),
    reading_gloss=("The report states that 'the implementation of the scheme will be the subject "
                   "of an evaluation'. Translated into ordinary French: somebody will have to "
                   "check whether the measure works, and the report does not say who. It is "
                   "exactly that vagueness that the summary note attacks: for every passive "
                   "sentence, write the verb, the subject and the date."),
    listening=("Analyst: Il conviendrait de procéder à un réexamen.<br>Chair: Concrètement ?<br>"
               "Analyst: Concrètement : deux personnes, quinze jours, une note de trois pages.<br>"
               "Chair: Voilà qui est plus clair."),
    listening_gloss=("Analyst: It would be advisable to carry out a review. Chair: Concretely? "
                     "Analyst: Concretely: two people, two weeks, a three-page note. Chair: That "
                     "is clearer."),
    voice_tag=VOICE,
    idioms=[
        ("La mise en œuvre", "the putting into work", "implementation"),
        ("Faire l'objet de", "to be the object of", "to be subject to"),
        ("Procéder à", "to proceed to", "to carry out"),
        ("Il conviendrait de", "it would be fitting to", "it would be advisable to"),
        ("En l'état", "in the state", "as things stand"),
        ("Au titre de", "under the heading of", "under, by virtue of"),
        ("Sous réserve de", "under reserve of", "subject to"),
        ("Le cas échéant", "the case arising", "if applicable"),
        ("À toutes fins utiles", "to all useful ends", "for whatever purpose it may serve"),
        ("Dont acte", "of which record", "noted accordingly"),
    ],
    mistakes=[
        ("Il a été procédé par les services à une vérification (subject hidden).", "Les services ont vérifié les comptes.", "Un-nominalise: name the actor and the verb."),
        ("Il conviendrait de procéder à un réexamen rapide et efficace et utile.", "Il conviendrait de réexaminer le dispositif sous quinze jours.", "One adjective per claim; the date does the work."),
        ("Faire l'objet d'une évaluation par qui que ce soit.", "Faire l'objet d'une évaluation indépendante.", "Replace the vague agent with a named one."),
    ],
    task_title="Un-nominalise one administrative paragraph",
    task_instructions=("Take a real French administrative sentence you have received — a letter, a "
                       "notice, a school form — and rewrite it three times: as it was written, in "
                       "plain French with a subject and a verb, and as a three-line memo that "
                       "names who does what by when. Note every noun phrase you had to unpack; "
                       "that list is your C1 vocabulary."),
)

EXTRAS["C2"] = EXTRA(
    culture=("French literary argument plays with understatement: the litote (« ce n'est pas "
             "rien ») says more by saying less, and irony often arrives through a borrowed "
             "register — a legal phrase in a poem, a slogan in an essay. Reading at C2 means "
             "hearing the borrowed voice and knowing who is being quoted, and mocked."),
    source_url="https://en.wikipedia.org/wiki/French_literature",
    reading=("« Il n'était pas sans savoir que la chose était délicate » : trois négations pour "
             "une seule information, et l'information elle-même reste au bord de la phrase. Le "
             "commentaire qui suit cite un communiqué — « une issue favorable est envisageable » — "
             "et le laisse là, sans guillemets ajoutés, pour que le lecteur entende le vide."),
    reading_gloss=("'He was not unaware that the matter was delicate': three negations for one "
                   "piece of information, and the information itself stays at the edge of the "
                   "sentence. The commentary that follows quotes a press release — 'a favourable "
                   "outcome is conceivable' — and leaves it there, with no added quotation marks, "
                   "so that the reader hears the emptiness."),
    listening=("Editor: Votre texte cite le communiqué sans le commenter.<br>Author: Je le laisse parler.<br>"
               "Editor: Et le lecteur entend ?<br>Author: Il entend la litote, s'il veut bien."),
    listening_gloss=("Editor: Your text quotes the press release without commenting on it. "
                     "Author: I let it speak. Editor: And the reader hears? Author: They hear the "
                     "understatement, if they care to."),
    voice_tag=VOICE,
    idioms=[
        ("La litote", "the litotes", "understatement"),
        ("Ne pas être sans savoir", "not to be without knowing", "to be well aware"),
        ("À demi-mot", "at half word", "without spelling it out"),
        ("Sous-entendre", "to under-hear", "to imply"),
        ("Le non-dit", "the unsaid", "what is left unsaid"),
        ("Mettre entre guillemets", "to put in quotation marks", "to quote, to hedge"),
        ("Le ton pince-sans-rire", "the dry-witted tone", "deadpan"),
        ("Faire mouche", "to make fly", "to hit the mark"),
        ("Sans y toucher", "without touching it", "without appearing to try"),
        ("Un clin d'œil", "a wink of the eye", "a nod, a knowing allusion"),
    ],
    mistakes=[
        ("Ce n'est pas rien, c'est-à-dire que c'est énorme.", "Ce n'est pas rien.", "A litote explains itself into nothing; leave it standing."),
        ("Il a dit : « » entre guillemets, ironiquement.", "Il a dit « une issue favorable est envisageable » — et s'est tu.", "Show the irony by silence, not by labelling it."),
        ("L'auteur est ironique ici (trois fois dans le paragraphe).", "L'auteur cite le communiqué sans commentaire.", "Describe the device once; the reader will hear the rest."),
    ],
    task_title="Write a litote and dismantle one",
    task_instructions=("Write a six-line French paragraph in which a plan is described only by "
                       "what it is not (« ce n'est pas rien », « il n'est pas exclu que »), then "
                       "rewrite the same paragraph in flat official French and in one blunt line. "
                       "Finally, take a real French slogan or press release and write the sentence "
                       "that names what it leaves unsaid without using the word ironie."),
)


THIRD["A1"] = [
    ("A1-U1", "A1-U1-L3", L(
        "Tu ou vous : choisir sur la première phrase",
        "French makes one decision before it says anything else: tu for friends and family, vous "
        "for strangers, shops and anyone older. « Bonjour » opens both doors; the pronoun picks "
        "the room.",
        [V("vous", "voo", "you (polite)", "pronoun"),
         V("tu", "tü", "you (familiar)", "pronoun"),
         V("madame", "mah-DAHM", "madam", "noun"),
         V("monsieur", "muh-SYUH", "sir", "noun"),
         V("on", "oh(n)", "one, we (spoken)", "pronoun")],
        G("The two yous",
          "vous + verb (2nd person plural) · tu + verb (2nd person singular) · on + 3rd person singular",
          "Bonjour madame, comment allez-vous ? Bonjour Théo, comment vas-tu ? Vous works for one "
          "person when politeness is needed; on means we in speech and takes the verb of il.",
          [X("Bonjour madame, comment allez-vous ?", "boh(n)-ZHOOR mah-DAHM, koh-mah(n) tah-lay-VOO ?", "Hello madam, how are you?"),
           X("Salut Théo, comment vas-tu ?", "sah-LÜ tay-OH, koh-mah(n) vah-TÜ ?", "Hi Théo, how are you?"),
           X("On va au café ?", "oh(n) vah oh kah-FAY ?", "Shall we go to the café?")],
          [("Bonjour madame, comment vas-tu ?", "Bonjour madame, comment allez-vous ?", "The pronoun and the verb form must agree in politeness."),
           ("Vous est mon ami.", "Tu es mon ami.", "vous is never used for a friend you call by first name.")]),
        [D("Léa", "Bonjour monsieur, excusez-moi, vous êtes le professeur ?", "boh(n)-ZHOOR muh-SYUH, eks-kü-zay-MWAH, voo ZET luh proh-feh-SUHR ?", "Hello sir, excuse me, are you the teacher?"),
         D("M. Brun", "Oui, c'est moi. Et vous ?", "wee, say MWAH. ay VOO ?", "Yes, that's me. And you?"),
         D("Léa", "Je m'appelle Léa. Je suis nouvelle.", "zhuh mah-PEL lay-AH. zhuh swee noo-VEL.", "My name is Léa. I'm new."),
         D("M. Brun", "Bienvenue, mademoiselle. On commence à neuf heures.", "bya(n)-vuh-NÜ, mad-mwa-ZEL. oh(n) koh-MAHNS ah nuhf UHR.", "Welcome, miss. We start at nine.")],
        WS("Tu/vous worksheet", [
            T("Choose the pronoun.", ["to your friend Théo", "to a shopkeeper", "to your little sister"],
              ["tu", "vous", "tu"]),
            T("Say it politely.", ["Hello madam, how are you?", "Excuse me, are you the teacher?", "Shall we go?"],
              ["Bonjour madame, comment allez-vous ?", "Excusez-moi, vous êtes le professeur ?", "On y va ?"]),
        ]))),
    ("A1-U2", "A1-U2-L3", L(
        "Où j'habite : il y a et les pièces",
        "Home is described with IL Y A (there is / there are) and a room list: un appartement, une "
        "chambre, la cuisine, le salon. « J'habite près de » places the flat in the city.",
        [V("habiter", "ah-bee-TAY", "to live", "verb"),
         V("il y a", "eel yah", "there is / there are", "phrase"),
         V("la chambre", "lah SHAH(N)-bruh", "bedroom", "noun"),
         V("la cuisine", "lah kü-ee-ZEEN", "kitchen", "noun"),
         V("près de", "preh duh", "near", "phrase")],
        G("There is / there are",
          "il y a + noun · il n'y a pas de + noun · j'habite + place",
          "Il y a deux chambres et une cuisine. Il n'y a pas de balcon. J'habite près du centre. "
          "il y a never changes for the plural, and the negative swaps un/une for de.",
          [X("Il y a deux chambres.", "eel yah duh SHAH(N)-bruh.", "There are two bedrooms."),
           X("Il n'y a pas de balcon.", "eel nyah pah duh bal-KOH(N).", "There is no balcony."),
           X("J'habite près du centre.", "zhah-BEET preh dü SAH(N)-truh.", "I live near the centre.")],
          [("Il y a sont deux chambres.", "Il y a deux chambres.", "il y a is complete; no extra verb."),
           ("Il n'y a pas un balcon.", "Il n'y a pas de balcon.", "The negative takes de, not un.")]),
        [D("Théo", "Tu habites où ?", "tü ah-BEET oo ?", "Where do you live?"),
         D("Léa", "Près du centre, dans un petit appartement.", "preh dü SAH(N)-truh, dah(n) zuh(n) ptee tah-par-tuh-MAH(N).", "Near the centre, in a small flat."),
         D("Théo", "Il y a combien de pièces ?", "eel yah koh(n)-BYA(N) duh PYESS ?", "How many rooms are there?"),
         D("Léa", "Deux chambres, une cuisine et un salon. Pas de balcon, hélas.", "duh SHAH(N)-bruh, ün kü-ee-ZEEN ay uh(n) sah-LOH(N). pah duh bal-KOH(N), ay-LASS.", "Two bedrooms, a kitchen and a living room. No balcony, alas.")],
        WS("Home worksheet", [
            T("Say what there is.", ["two bedrooms", "a small kitchen", "no balcony"],
              ["Il y a deux chambres.", "Il y a une petite cuisine.", "Il n'y a pas de balcon."]),
            T("Place your home.", ["near the centre", "where do you live?"],
              ["J'habite près du centre.", "Tu habites où ?"]),
        ]))),
    ("A1-U3", "A1-U3-L3", L(
        "Le temps et les saisons",
        "Weather is impersonal and short: IL FAIT BEAU, IL PLEUT, IL FAIT FROID. Seasons take EN "
        "for the ones you live through and À for the ones you name in a date.",
        [V("il fait beau", "eel feh BOH", "the weather is nice", "phrase"),
         V("il pleut", "eel PLUH", "it is raining", "phrase"),
         V("il fait froid", "eel feh FRWAH", "it is cold", "phrase"),
         V("l'été", "lay-TAY", "summer", "noun"),
         V("l'hiver", "lee-VEHR", "winter", "noun")],
        G("Weather frame",
          "il fait + adjective · il pleut / il neige · en été / en hiver · au printemps / en automne",
          "Il fait beau en été, il fait froid en hiver. En automne, il pleut souvent. Notice "
          "which seasons take en (été, hiver, automne) and which takes au (printemps).",
          [X("Il fait beau en été.", "eel feh BOH ah(n) nay-TAY.", "The weather is nice in summer."),
           X("Il pleut souvent en automne.", "eel PLUH soo-VAH(N) ah(n) noh-TOHN.", "It often rains in autumn."),
           X("Au printemps, il neige encore ?", "oh pra(n)-TAH(N), eel NEZH ah(n)-KOR ?", "In spring, does it still snow?")],
          [("Il est froid aujourd'hui.", "Il fait froid aujourd'hui.", "Weather uses faire: il fait froid."),
           ("En printemps il pleut.", "Au printemps il pleut.", "printemps takes au, not en.")]),
        [D("Léa", "Quel temps fait-il à Paris ?", "kel tah(n) feh-TEEL ah pah-REE ?", "What is the weather like in Paris?"),
         D("Théo", "Il pleut et il fait froid. C'est l'hiver, quoi.", "eel PLUH ay eel feh FRWAH. say lee-VEHR, kwah.", "It is raining and cold. It's winter, basically."),
         D("Léa", "Et en été ?", "ay ah(n) nay-TAY ?", "And in summer?"),
         D("Théo", "Il fait beau et les gens sortent. C'est la meilleure saison.", "eel feh BOH ay lay ZHAH(N) SORT. say lah meh-YUHR seh-ZOH(N).", "The weather is nice and people go out. It's the best season.")],
        WS("Weather worksheet", [
            T("Describe the weather.", ["it is nice (summer)", "it is raining (autumn)", "it is cold (winter)"],
              ["Il fait beau en été.", "Il pleut en automne.", "Il fait froid en hiver."]),
            T("Answer the question.", ["What is the weather like today?", "Do you like summer?"],
              ["Quel temps fait-il aujourd'hui ?", "Tu aimes l'été ?"]),
        ]))),
]

THIRD["A2"] = [
    ("A2-U1", "A2-U1-L3", L(
        "Le train : départ, retour, quai",
        "Tickets are bought with a frame: un billet aller-retour pour Lyon, départ à huit heures. "
        "Questions at the station are short: de quel quai ? faut-il changer ?",
        [V("aller-retour", "ah-lay ruh-TOOR", "return ticket", "noun"),
         V("le quai", "luh KAY", "platform", "noun"),
         V("changer", "shah(n)-ZHAY", "to change (trains)", "verb"),
         V("le billet", "luh bee-YEH", "ticket", "noun"),
         V("en retard", "ah(n) ruh-TAR", "late", "phrase")],
        G("Travel frame",
          "un billet pour … · aller simple / aller-retour · de quel quai ? · il faut changer à …",
          "Un aller-retour pour Lyon, s'il vous plaît. Le train part de quel quai ? Il faut "
          "changer à Dijon. The complement of the ticket is another city, not a date.",
          [X("Un aller-retour pour Lyon, s'il vous plaît.", "uh(n) nah-lay ruh-TOOR poor lyo(n), seel voo PLAY.", "A return ticket to Lyon, please."),
           X("Le train part de quel quai ?", "luh tra(n) par duh kel KAY ?", "Which platform does the train leave from?"),
           X("Il faut changer à Dijon.", "eel foh shah(n)-ZHAY ah dee-ZHOH(N).", "You have to change at Dijon.")],
          [("Un billet à Lyon.", "Un billet pour Lyon.", "A destination takes pour."),
           ("Le train est en retard de dix minutes.", "Le train a dix minutes de retard.", "Latness of a train uses avoir … de retard.")]),
        [D("Théo", "Un aller-retour pour Lyon, s'il vous plaît.", "uh(n) nah-lay ruh-TOOR poor lyo(n), seel voo PLAY.", "A return ticket to Lyon, please."),
         D("Guichetière", "Départ à quelle heure ?", "day-PAR ah kel UHR ?", "Departure at what time?"),
         D("Théo", "À dix heures. Il faut changer ?", "ah dee ZUHR. eel foh shah(n)-ZHAY ?", "At ten. Do I have to change?"),
         D("Guichetière", "Non, direct. Quai numéro quatre.", "noh(n), dee-REKT. kay nü-may-ROH katr.", "No, direct. Platform number four.")],
        WS("Train worksheet", [
            T("Buy the ticket.", ["a return to Lyon", "a single to Dijon", "departure at ten"],
              ["Un aller-retour pour Lyon.", "Un aller simple pour Dijon.", "Départ à dix heures."]),
            T("Ask at the station.", ["which platform?", "do I have to change?", "is it late?"],
              ["De quel quai ?", "Il faut changer ?", "Il est en retard ?"]),
        ]))),
    ("A2-U2", "A2-U2-L3", L(
        "Chez le médecin : j'ai mal, vous devriez",
        "Pain uses AVOIR MAL À: j'ai mal à la tête, au dos, aux dents. Advice uses the "
        "conditional: VOUS DEVRIEZ vous reposer.",
        [V("avoir mal à", "ah-VWAR mal ah", "to have pain in", "phrase"),
         V("la gorge", "lah GORZH", "throat", "noun"),
         V("se reposer", "suh ruh-poh-ZAY", "to rest", "verb"),
         V("l'ordonnance", "lor-doh-NAH(N)S", "prescription", "noun"),
         V("vous devriez", "voo duh-vree-AY", "you should", "phrase")],
        G("Pain and advice",
          "avoir mal à + body part · vous devriez + infinitive · il faut + infinitive",
          "J'ai mal à la gorge et j'ai mal à la tête. Vous devriez boire de l'eau et vous "
          "reposer. The body part keeps its article: à la tête, au dos, aux pieds.",
          [X("J'ai mal à la gorge.", "zhay mal ah lah GORZH.", "I have a sore throat."),
           X("J'ai mal aux pieds.", "zhay mal oh PYAY.", "My feet hurt."),
           X("Vous devriez vous reposer deux jours.", "voo duh-vree-AY voo ruh-poh-ZAY duh ZHOOR.", "You should rest for two days.")],
          [("J'ai mal la gorge.", "J'ai mal à la gorge.", "The phrase needs à before the body part."),
           ("Vous devez vous reposer (advice to a friend).", "Vous devriez vous reposer.", "devoir orders; the conditional advises.")]),
        [D("Léa", "Bonjour docteur, j'ai mal à la gorge.", "boh(n)-ZHOOR dok-TUHR, zhay mal ah lah GORZH.", "Hello doctor, I have a sore throat."),
         D("Médecin", "Depuis quand ?", "duh-PWEE kah(n) ?", "Since when?"),
         D("Léa", "Depuis trois jours, et j'ai mal à la tête aussi.", "duh-PWEE trwah ZHOOR, ay zhay mal ah lah TAYT oh-SEE.", "For three days, and my head hurts too."),
         D("Médecin", "Vous devriez vous reposer et boire beaucoup d'eau.", "voo duh-vree-AY voo ruh-poh-ZAY ay bwar boh-KOO doh.", "You should rest and drink plenty of water.")],
        WS("Doctor worksheet", [
            T("Say where it hurts.", ["sore throat", "my head hurts", "my feet hurt"],
              ["J'ai mal à la gorge.", "J'ai mal à la tête.", "J'ai mal aux pieds."]),
            T("Give advice.", ["you should rest", "you should drink water"],
              ["Vous devriez vous reposer.", "Vous devriez boire de l'eau."]),
        ]))),
    ("A2-U3", "A2-U3-L3", L(
        "Les vêtements : taille, couleur, échange",
        "Shopping clothes turns on four words: LA TAILLE (size), LA COULEUR, ESSAYER (to try on) "
        "and ÉCHANGER. « Ça me va » judges the fit.",
        [V("la taille", "lah TAH-yuh", "size", "noun"),
         V("essayer", "eh-say-YAY", "to try on", "verb"),
         V("échanger", "ay-shah(n)-ZHAY", "to exchange", "verb"),
         V("la caisse", "lah KES", "checkout", "noun"),
         V("ça me va", "sah muh VAH", "it fits me", "phrase")],
        G("Shopping frame",
          "je peux essayer ? · ça me va / ça ne me va pas · je voudrais l'échanger contre …",
          "Je peux essayer cette chemise ? Elle est trop petite : je voudrais l'échanger contre "
          "une taille au-dessus. The size is spoken with a number or with au-dessus / en dessous.",
          [X("Je peux essayer cette chemise ?", "zhuh puh ay-say-YAY set shuh-MEEZ ?", "Can I try this shirt on?"),
           X("Elle est trop petite.", "el ay troh puh-TEET.", "It is too small."),
           X("Je voudrais l'échanger contre une taille au-dessus.", "zhuh voo-DREH lay-shah(n)-ZHAY koh(n)-truh ün TAH-yuh oh-duh-SÜ.", "I would like to exchange it for one size bigger.")],
          [("Je peux essayer de la chemise ?", "Je peux essayer la chemise ?", "essayer takes a direct object; no de."),
           ("Il est trop petite.", "Elle est trop petite.", "The shirt is feminine: elle.")]),
        [D("Léa", "Bonjour, je peux essayer cette robe ?", "boh(n)-ZHOOR, zhuh puh ay-say-YAY set ROB ?", "Hello, can I try this dress on?"),
         D("Vendeur", "Bien sûr, la cabine est au fond.", "bya(n) SÜR, lah kah-BEEN ay toh FOH(N).", "Of course, the fitting room is at the back."),
         D("Léa", "Elle est trop petite. Vous avez une taille au-dessus ?", "el ay troh puh-TEET. voo zah-VAY ün TAH-yuh oh-duh-SÜ ?", "It is too small. Do you have one size bigger?"),
         D("Vendeur", "Oui, en bleu. Ça vous va très bien.", "wee, ah(n) BLUH. sah voo VAH tray BYA(N).", "Yes, in blue. It suits you very well.")],
        WS("Clothes worksheet", [
            T("Shop in French.", ["can I try it on?", "it is too small", "one size bigger"],
              ["Je peux l'essayer ?", "Elle est trop petite.", "une taille au-dessus"]),
            T("Finish the purchase.", ["I'll take it", "where is the checkout?"],
              ["Je la prends.", "Où est la caisse ?"]),
        ]))),
]

# ── the five half-step rungs ────────────────────────────────────────────────

HALFSTEPS["A1+"] = {
    "title": "French A1+ — Getting around",
    "native": NATIVE,
    "goals": [
        "Ask the way, buy a ticket and name a landmark",
        "Say a phone number, an address and a price out loud",
        "Name the days, tell the time and make a plan — or refuse one politely",
    ],
    "units": [
        {"id": "A1+-U1", "title": "Dans la ville", "lessons": [
            L("Tout droit, à gauche, à droite",
              "Directions are imperative and short: ALLEZ TOUT DROIT, TOURNEZ À GAUCHE. With a "
              "stranger the vous form keeps it polite: EXCUSEZ-MOI, OÙ EST LA GARE ?",
              [V("tout droit", "too DRWAH", "straight ahead", "adverb"),
               V("à gauche", "ah GOHSH", "to the left", "phrase"),
               V("à droite", "ah DRWAHT", "to the right", "phrase"),
               V("le coin", "luh KWA(N)", "corner", "noun"),
               V("près", "preh", "near", "adverb")],
              G("Directions",
                "allez tout droit · tournez à gauche · c'est au coin · c'est près d'ici",
                "Allez tout droit et tournez à gauche au coin. La gare est près d'ici, à cinq "
                "minutes. The landmark takes de: près de la gare, au coin de la rue.",
                [X("Allez tout droit, puis tournez à droite.", "ah-LAY too DRWAH, pwee toor-NAY ah DRWAHT.", "Go straight ahead, then turn right."),
                 X("La gare est au coin de la rue.", "lah GAR ay toh KWA(N) duh lah RÜ.", "The station is at the corner of the street."),
                 X("C'est loin d'ici ?", "say LWA(N) dee-SEE ?", "Is it far from here?")],
                [("Tournez à la gauche.", "Tournez à gauche.", "Direction phrases take à + noun without an article."),
                 ("C'est près la gare.", "C'est près de la gare.", "près takes de.")]),
              [D("Théo", "Excusez-moi, où est la gare, s'il vous plaît ?", "eks-kü-zay-MWAH, oo ay lah GAR, seel voo PLAY ?", "Excuse me, where is the station, please?"),
               D("Mme Petit", "Allez tout droit et tournez à gauche au coin.", "ah-LAY too DRWAH ay toor-NAY ah GOHSH oh KWA(N).", "Go straight ahead and turn left at the corner."),
               D("Théo", "C'est loin ?", "say LWA(N) ?", "Is it far?"),
               D("Mme Petit", "Non, cinq minutes à pied.", "noh(n), sa(n)k mee-NÜT ah PYAY.", "No, five minutes on foot.")],
              WS("Directions worksheet", [
                  T("Give the direction.", ["go straight ahead", "then left", "at the corner"],
                    ["Allez tout droit.", "puis à gauche", "au coin"]),
                  T("Ask and answer.", ["where is the station?", "is it far? (no, five minutes on foot)"],
                    ["Où est la gare, s'il vous plaît ?", "C'est loin ? — Non, cinq minutes à pied."]),
              ])),
            L("Billets, arrêts et tarifs",
              "Transport questions are fixed: UN BILLET POUR LE CENTRE, S'IL VOUS PLAÎT · C'EST "
              "COMBIEN ? · ARRÊTEZ-VOUS ICI ?",
              [V("le billet", "luh bee-YEH", "ticket", "noun"),
               V("l'arrêt", "lah-RAY", "stop (bus)", "noun"),
               V("combien", "koh(n)-BYA(N)", "how much", "adverb"),
               V("le carnet", "luh kar-NEH", "book of tickets", "noun"),
               V("valider", "vah-lee-DAY", "to validate (a ticket)", "verb")],
              G("Fares and stops",
                "un billet pour … · c'est combien ? · il faut valider le billet",
                "Un billet pour le centre, s'il vous plaît. C'est combien ? Un euro cinquante. "
                "Il faut valider le billet dans le bus. Note the fixed negative question "
                "« arrêtez-vous ici ? » with its hyphen.",
                [X("Un billet pour le centre, s'il vous plaît.", "uh(n) bee-YEH poor luh SAH(N)-truh, seel voo PLAY.", "A ticket to the centre, please."),
                 X("C'est combien ?", "say koh(n)-BYA(N) ?", "How much is it?"),
                 X("Vous arrêtez-vous à la gare ?", "voo zah-reh-TAY voo ah lah GAR ?", "Do you stop at the station?")],
                [("C'est combien ça coûte ?", "C'est combien ?", "One question word per sentence."),
                 ("Un billet à la gare.", "Un billet pour la gare.", "Destinations take pour.")]),
              [D("Léa", "Bonjour, un carnet de dix, s'il vous plaît.", "boh(n)-ZHOOR, uh(n) kar-NEH duh DEES, seel voo PLAY.", "Hello, a book of ten tickets, please."),
               D("Chauffeur", "C'est douze euros. Validez-le dans la machine.", "say dooz uh-ROH. vah-lee-day-LUH dah(n) lah mah-SHEEN.", "That's twelve euros. Validate it in the machine."),
               D("Léa", "Vous allez jusqu'au centre ?", "voo zah-LAY zhüs-koh SAH(N)-truh ?", "Do you go as far as the centre?"),
               D("Chauffeur", "Oui, arrêt République.", "wee, ah-RAY ray-pü-BLEEK.", "Yes, République stop.")],
              WS("Fare worksheet", [
                  T("Say it in French.", ["a ticket to the centre", "how much is it?", "do you stop at the station?"],
                    ["un billet pour le centre", "C'est combien ?", "Vous arrêtez-vous à la gare ?"]),
                  T("Answer as the driver.", ["twelve euros", "validate the ticket"],
                    ["Douze euros.", "Validez le billet."]),
              ])),
            L("Points de repère : en face de, à côté de, derrière",
              "Landmarks relate with EN FACE DE (opposite), À CÔTÉ DE (next to), DERRIÈRE and "
              "DEVANT. Each takes de + place.",
              [V("en face de", "ah(n) FASS duh", "opposite", "phrase"),
               V("à côté de", "ah koh-TAY duh", "next to", "phrase"),
               V("derrière", "deh-RYEHR", "behind", "phrase"),
               V("devant", "duh-VAH(N)", "in front of", "phrase"),
               V("le marché", "luh mar-SHAY", "market", "noun")],
              G("Position with de",
                "en face de la gare · à côté du marché · derrière le musée",
                "La pharmacie est à côté du marché, en face de la gare. de + le becomes du, de + "
                "les becomes des — the relation carries the position, the noun the landmark.",
                [X("La pharmacie est à côté du marché.", "lah far-mah-SEE ay ah koh-TAY dü mar-SHAY.", "The pharmacy is next to the market."),
                 X("La banque est en face de la gare.", "lah bah(n)K ay ah(n) FASS duh lah GAR.", "The bank is opposite the station."),
                 X("Il y a un parc derrière le musée.", "eel yah uh(n) park deh-RYEHR luh mü-ZAY.", "There is a park behind the museum.")],
                [("La pharmacie est à côté le marché.", "La pharmacie est à côté du marché.", "à côté de + le = du."),
                 ("C'est en face la gare.", "C'est en face de la gare.", "The phrase needs de.")]),
              [D("Théo", "Où est la pharmacie ?", "oo ay lah far-mah-SEE ?", "Where is the pharmacy?"),
               D("Léa", "À côté du marché, en face de la gare.", "ah koh-TAY dü mar-SHAY, ah(n) FASS duh lah GAR.", "Next to the market, opposite the station."),
               D("Théo", "Et il y a une banque près d'ici ?", "ay eel yah ün bah(n)K preh dee-SEE ?", "And is there a bank near here?"),
               D("Léa", "Oui, derrière le musée.", "wee, deh-RYEHR luh mü-ZAY.", "Yes, behind the museum.")],
              WS("Landmark worksheet", [
                  T("Complete with the relation.", ["next to the market", "opposite the station", "behind the museum"],
                    ["à côté du marché", "en face de la gare", "derrière le musée"]),
                  T("Describe your street.", ["what is next to the bakery?", "what is opposite the bank?"],
                    ["À côté de la boulangerie, il y a …", "En face de la banque se trouve …"]),
              ])),
        ]},
        {"id": "A1+-U2", "title": "Les nombres qui ramènent à la maison", "lessons": [
            L("De onze à cent",
              "French counts in blocks: ONZE, SEIZE, VINGT, VINGT ET UN, TRENTE-QUATRE, SOIXANTE-DIX, "
              "QUATRE-VINGTS, QUATRE-VINGT-DIX. Above sixty-nine the arithmetic appears in the words.",
              [V("seize", "SEZ", "sixteen", "numeral"),
               V("vingt et un", "va(n) ay UH(N)", "twenty-one", "numeral"),
               V("soixante-dix", "swah-sah(n)t DEES", "seventy", "numeral"),
               V("quatre-vingts", "katr VA(N)", "eighty", "numeral"),
               V("quatre-vingt-dix", "katr va(n) DEES", "ninety", "numeral"),
               V("cent", "sah(n)", "hundred", "numeral")],
              G("Numbers",
                "70 = soixante-dix · 80 = quatre-vingts · 90 = quatre-vingt-dix · 100 = cent",
                "Soixante-dix, soixante et onze, quatre-vingts (with s), quatre-vingt-un (without "
                "s). Belgian and Swiss French use septante and nonante, which is worth "
                "recognising when you hear it.",
                [X("J'ai vingt et un ans.", "zhay va(n) ay UH(N) ah(n).", "I am twenty-one."),
                 X("Ça coûte quatre-vingts euros.", "sah koot katr VA(N) uh-ROH.", "It costs eighty euros."),
                 X("Il y a soixante-dix personnes.", "eel yah swah-sah(n)t DEES per-SON.", "There are seventy people.")],
                [("Quatre-vingt euros (for exactly eighty).", "Quatre-vingts euros.", "Eighty alone takes the s: quatre-vingts."),
                 ("Soixante-dix-dix.", "quatre-vingts", "Do not stack two tens; French switches system at eighty.")]),
              [D("Léa", "Tu as quel âge ?", "tü ah kel AZH ?", "How old are you?"),
               D("Théo", "Vingt et un ans. Et toi ?", "va(n) ay UH(N) ah(n). ay TWAH ?", "Twenty-one. And you?"),
               D("Léa", "Dix-neuf. Ma sœur a quatre-vingts ans ? Non, quatre-vingt-un.", "dees-NUH(F). mah SUHR ah katr VA(N) ah(n) ? noh(n), katr va(n) UH(N).", "Nineteen. My sister is eighty? No, eighty-one."),
               D("Théo", "Ah, la famille est grande !", "ah, lah fah-MEEY ay GRAH(N)D !", "Ah, the family is big!")],
              WS("Numbers worksheet", [
                  T("Write the number in French words.", ["16", "21", "70", "91"],
                    ["seize", "vingt et un", "soixante-dix", "quatre-vingt-onze"]),
                  T("Say the price in full.", ["ticket: €9.50", "two books: €120"],
                    ["neuf euros cinquante", "cent vingt euros"]),
              ])),
            L("Téléphones et adresses",
              "Phone numbers are read in pairs of digits, addresses run NUMÉRO, RUE, ÉTAGE: QUINZE, "
              "RUE VICTOR-HUGO, TROISIÈME ÉTAGE. Asking: TU PEUX ME DONNER TON NUMÉRO ?",
              [V("le numéro", "luh nü-may-ROH", "number", "noun"),
               V("la rue", "lah RÜ", "street", "noun"),
               V("l'étage", "lay-TAZH", "floor", "noun"),
               V("épeler", "ay-puh-LAY", "to spell out", "verb"),
               V("le code postal", "luh kod pos-TAL", "postcode", "noun")],
              G("Address and phone",
                "numéro + rue + étage · tu peux me donner ton numéro ? · tu peux l'épeler ?",
                "J'habite au quinze, rue Victor-Hugo, troisième étage. Mon numéro est zéro six, "
                "douze, trente-quatre. The street number comes first, and the phone is read in "
                "pairs.",
                [X("J'habite au quinze, rue Victor-Hugo.", "zhah-BEET oh KA(N)Z, rü veek-TOR ü-GOH.", "I live at 15 rue Victor-Hugo."),
                 X("Tu peux me donner ton numéro ?", "tü puh muh doh-NAY toh(n) nü-may-ROH ?", "Can you give me your number?"),
                 X("Tu peux l'épeler, s'il te plaît ?", "tü puh lay-puh-LAY, seel tuh PLAY ?", "Can you spell it, please?")],
                [("Vivo en la calle Mayor, quince → Vivo en calle Mayor 15 → I live at 15 Calle Mayor.", "J'habite au quinze, rue Victor-Hugo.", "Street numbers take au: au quinze. (This line keeps the French model.)"),
                 ("Mon numéro est douze-cents.", "Mon numéro est un deux, zéro zéro.", "Phone numbers are read digit by digit or in pairs, never as large numerals.")]),
              [D("Théo", "Tu peux me donner ton adresse ?", "tü puh muh doh-NAY toh(n) nah-DRESS ?", "Can you give me your address?"),
               D("Léa", "Au quinze, rue Victor-Hugo, troisième étage.", "oh KA(N)Z, rü veek-TOR ü-GOH, trwa-ZYEM ay-TAZH.", "15 rue Victor-Hugo, third floor."),
               D("Théo", "Et ton numéro ?", "ay toh(n) nü-may-ROH ?", "And your number?"),
               D("Léa", "Zéro six, douze, trente-quatre.", "zay-ROH SEES, DOOZ, trah(n)t-KATR.", "Zero six, twelve, thirty-four.")],
              WS("Address worksheet", [
                  T("Say it in French.", ["my address", "number fifteen", "can you spell it?"],
                    ["mon adresse", "le numéro quinze", "Tu peux l'épeler ?"]),
                  T("Ask for the details.", ["your phone number?", "the postcode?"],
                    ["Tu peux me donner ton numéro ?", "C'est quel code postal ?"]),
              ])),
            L("Les prix : cher, pas cher, un peu moins",
              "Prices are discussed at markets and small shops: C'EST TROP CHER · VOUS POUVEZ ME "
              "FAIRE UN PRIX ? · ET SI JE PRENDS DEUX ?",
              [V("cher", "shehr", "expensive", "adjective"),
               V("pas cher", "pah SHEHR", "cheap", "phrase"),
               V("le prix", "luh PREE", "price", "noun"),
               V("baisser", "bay-SAY", "to lower", "verb"),
               V("la promotion", "lah proh-moh-SYOH(N)", "special offer", "noun")],
              G("Price talk",
                "c'est trop cher · vous pouvez me faire un prix ? · et si j'en prends deux ?",
                "C'est un peu cher — vous pouvez me faire un prix ? Et si j'en prends deux, vous "
                "baissez le prix ? The conditional and the polite question keep the negotiation "
                "friendly.",
                [X("C'est un peu cher.", "say tuh(n) puh SHEHR.", "It is a little expensive."),
                 X("Vous pouvez me faire un prix ?", "voo poo-VAY muh fehr uh(n) PREE ?", "Can you give me a price?"),
                 X("Et si j'en prends deux ?", "ay see zhah(n) PRAH(N) DUH ?", "And if I take two?")],
                [("Je suis cher.", "C'est cher.", "The price is expensive, not the person."),
                 ("Vous baissez, oui ?", "Vous pouvez baisser un peu ?", "The question keeps it polite.")]),
              [D("Léa", "C'est combien, les tomates ?", "say koh(n)-BYA(N), lay toh-MAT ?", "How much are the tomatoes?"),
               D("Marchand", "Trois euros le kilo.", "trwah ZUH-ROH luh kee-LOH.", "Three euros a kilo."),
               D("Léa", "C'est un peu cher. Et si j'en prends deux kilos ?", "say tuh(n) puh SHEHR. ay see zhah(n) PRAH(N) duh kee-LOH ?", "That's a bit expensive. And if I take two kilos?"),
               D("Marchand", "Cinq euros les deux. Marché conclu ?", "sa(n)k UH-ROH lay DUH. mar-SHAY koh(n)-KLÜ ?", "Five euros for the two. Deal?")],
              WS("Price worksheet", [
                  T("Bargain politely.", ["that's a bit expensive", "can you give me a price?", "I'll take two"],
                    ["C'est un peu cher.", "Vous pouvez me faire un prix ?", "J'en prends deux."]),
                  T("Answer as the seller.", ["three euros a kilo", "a special offer"],
                    ["Trois euros le kilo.", "C'est en promotion."]),
              ])),
        ]},
        {"id": "A1+-U3", "title": "Jours, heures, rendez-vous", "lessons": [
            L("La semaine : de lundi à dimanche",
              "Days are lowercase and mostly article-less: LUNDI, JE TRAVAILLE. A habit takes LE "
              "LUNDI; the weekend is LE WEEK-END.",
              [V("lundi", "lu(n)-DEE", "Monday", "noun"),
               V("vendredi", "vah(n)-druh-DEE", "Friday", "noun"),
               V("le week-end", "luh week-END", "weekend", "noun"),
               V("le matin", "luh mah-TA(N)", "morning", "noun"),
               V("le soir", "luh SWAR", "evening", "noun")],
              G("Days",
                "lundi je travaille · le lundi, je travaille · du lundi au vendredi",
                "Lundi, je travaille. Le lundi, je travaille (every Monday). Du lundi au "
                "vendredi, je travaille. The article is what turns a date into a habit.",
                [X("Lundi, je travaille.", "lu(n)-DEE, zhuh trah-VAHY.", "On Monday I work."),
                 X("Le vendredi, je suis libre.", "luh vah(n)-druh-DEE, zhuh swee LEEBR.", "On Fridays I am free."),
                 X("Du lundi au vendredi.", "dü lu(n)-DEE oh vah(n)-druh-DEE.", "From Monday to Friday.")],
                [("Dans lundi je travaille.", "Lundi, je travaille.", "Days take no preposition: lundi, not dans lundi."),
                 ("Le lundi au vendredi.", "Du lundi au vendredi.", "A range starts with du.")]),
              [D("Théo", "On est quel jour ?", "oh(n) nay kel ZHOOR ?", "What day is it?"),
               D("Léa", "Jeudi. Tu es libre vendredi ?", "zhuh-DEE. tü ay LEEBR vah(n)-druh-DEE ?", "Thursday. Are you free on Friday?"),
               D("Théo", "Le vendredi, je travaille jusqu'à sept heures.", "luh vah(n)-druh-DEE, zhuh trah-VAHY zhüs-kah set UHR.", "On Fridays I work until seven."),
               D("Léa", "Alors samedi, dans l'après-midi.", "ah-LOR sah-muh-DEE, dah(n) lah-preh-muh-DEE.", "Saturday afternoon, then.")],
              WS("Days worksheet", [
                  T("Answer in French.", ["what day is it? (Tuesday)", "when do you work? (Monday to Friday)", "the weekend"],
                    ["C'est mardi.", "Du lundi au vendredi, je travaille.", "le week-end"]),
                  T("Plan your week.", ["on Tuesday I work", "on Fridays I am free"],
                    ["Mardi, je travaille.", "Le vendredi, je suis libre."]),
              ])),
            L("L'heure : et demie, et quart, moins le quart",
              "Clock time uses IL EST + hour: IL EST TROIS HEURES ET DEMIE (3:30), TROIS HEURES "
              "MOINS LE QUART (2:45). Trains and offices switch to the 24-hour clock.",
              [V("et demie", "ay duh-MEE", "half past", "phrase"),
               V("et quart", "ay KAR", "quarter past", "phrase"),
               V("moins le quart", "mwa(n) luh KAR", "quarter to", "phrase"),
               V("l'heure", "LUHR", "hour, time", "noun"),
               V("midi", "mee-DEE", "noon", "noun")],
              G("Clock French",
                "il est + hour + et demie / et quart / moins le quart · à quelle heure ?",
                "Il est trois heures et demie. Il est midi. Le train part à quatorze heures "
                "cinq. The formal clock (quatorze heures) is what you hear in stations.",
                [X("Il est trois heures et demie.", "eel ay trwah ZUHR ay duh-MEE.", "It is half past three."),
                 X("Il est sept heures moins le quart.", "eel ay set UHR mwa(n) luh KAR.", "It is a quarter to seven."),
                 X("Le train part à quatorze heures cinq.", "luh tra(n) par ah kah-TORZ UHR SA(N)K.", "The train leaves at 14:05.")],
                [("Il est trois heures demie.", "Il est trois heures et demie.", "The half takes et: et demie."),
                 ("Il est douze heures (at noon, in speech).", "Il est midi.", "Noon is midi; midnight is minuit.")]),
              [D("Léa", "Il est quelle heure ?", "eel ay kel UHR ?", "What time is it?"),
               D("Théo", "Il est midi et quart. On déjeune ?", "eel ay mee-DEE ay KAR. oh(n) day-ZHÜN ?", "It is quarter past twelve. Shall we have lunch?"),
               D("Léa", "À une heure, plutôt. Le train part à treize heures dix.", "ah ün UHR, plü-TOH. luh tra(n) par ah TRAYZ UHR DEES.", "At one, rather. The train leaves at 13:10."),
               D("Théo", "Alors à midi et demie devant la gare.", "ah-LOR ah mee-DEE ay duh-MEE duh-VAH(N) lah GAR.", "Half past twelve in front of the station, then.")],
              WS("Clock worksheet", [
                  T("Say the time in French.", ["3:00", "3:30", "6:45", "12:00"],
                    ["il est trois heures", "il est trois heures et demie", "il est sept heures moins le quart", "il est midi"]),
                  T("Answer the question.", ["When does the train leave? (14:05)", "When shall we meet? (12:30)"],
                    ["Le train part à quatorze heures cinq.", "À midi et demie."]),
              ])),
            L("Faire des projets et refuser poliment",
              "Plans open with ON VA …? or ÇA TE DIT …?; refusals come with a reason and an "
              "alternative: PAS CE SOIR, MAIS DEMAIN, AVEC PLAISIR.",
              [V("ça te dit", "sah tuh DEE", "does that appeal to you", "phrase"),
               V("désolé", "day-zoh-LAY", "sorry", "adjective"),
               V("demain", "duh-MA(N)", "tomorrow", "adverb"),
               V("un autre jour", "uh(n) noh-truh ZHOOR", "another day", "phrase"),
               V("avec plaisir", "ah-vek play-ZEER", "with pleasure", "phrase")],
              G("Invite, refuse, re-offer",
                "ça te dit ? · pas ce soir, désolé · mais demain, avec plaisir",
                "Ça te dit, un café ? — Pas maintenant, désolé, je travaille. — Et demain ? — "
                "Demain, avec plaisir. The refusal names the moment, not the person.",
                [X("Ça te dit, un ciné ?", "sah tuh DEE, uh(n) see-NAY ?", "Do you fancy a film?"),
                 X("Pas ce soir, désolé.", "pah suh SWAR, day-zoh-LAY.", "Not tonight, sorry."),
                 X("Demain, avec plaisir.", "duh-MA(N), ah-vek play-ZEER.", "Tomorrow, with pleasure.")],
                [("Non je ne veux pas.", "Pas ce soir, désolé.", "Refuse the moment, not the friendship."),
                 ("Ça te dit de aller au ciné ?", "Ça te dit d'aller au ciné ?", "de + aller contracts to d'aller.")]),
              [D("Théo", "Ça te dit, un café après le travail ?", "sah tuh DEE, uh(n) kah-FAY ah-PREH luh trah-VAHY ?", "Do you fancy a coffee after work?"),
               D("Léa", "Pas ce soir, désolé — j'ai un cours.", "pah suh SWAR, day-zoh-LAY — zhay uh(n) KOOR.", "Not tonight, sorry — I have a class."),
               D("Théo", "Et demain ?", "ay duh-MA(N) ?", "And tomorrow?"),
               D("Léa", "Demain, avec plaisir. À dix-huit heures ?", "duh-MA(N), ah-vek play-ZEER. ah dee-zü-TUHR ?", "Tomorrow, with pleasure. At six p.m.?")],
              WS("Plan worksheet", [
                  T("Make the plan.", ["do you fancy a coffee?", "the cinema tomorrow", "at six"],
                    ["Ça te dit, un café ?", "le ciné demain", "à dix-huit heures"]),
                  T("Refuse and offer another day.", ["refuse tonight, offer tomorrow", "refuse today, offer the weekend"],
                    ["Pas ce soir — demain, avec plaisir.", "Pas aujourd'hui — le week-end, ça te dit ?"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Getting around France runs on small formulas and a timetable: validate your "
                 "ticket, read the 24-hour clock, ask « c'est combien ? » and accept that the "
                 "boulangerie closes between noon and four. The half-step collects signs, "
                 "relations and hours — parada-free vocabulary, because what gets a learner home "
                 "is reading the street and the clock, not the grammar."),
        source_url="https://en.wikipedia.org/wiki/SNCF",
        reading=("Samedi, je vais à Lyon. Le train part à neuf heures et quart, quai quatre. Le "
                 "billet aller-retour coûte dix-neuf euros et il n'y a pas de changement. À la "
                 "gare, je prends un café et je regarde le panneau : le train a cinq minutes de "
                 "retard. J'arrive au centre à pied, parce que la gare est tout près."),
        reading_gloss=("On Saturday I am going to Lyon. The train leaves at a quarter past nine, "
                       "platform four. The return ticket costs nineteen euros and there is no "
                       "change. At the station I have a coffee and look at the board: the train is "
                       "five minutes late. I reach the centre on foot, because the station is very "
                       "close."),
        listening=("Théo: Excusez-moi, c'est quel quai ?<br>Agent: Quai quatre, tout droit à gauche.<br>"
                   "Théo: Il part à quelle heure ?<br>Agent: À neuf heures et quart — il reste cinq minutes."),
        listening_gloss=("Théo: Excuse me, which platform is it? Officer: Platform four, straight "
                         "ahead on the left. Théo: What time does it leave? Officer: At a quarter "
                         "past nine — five minutes left."),
        voice_tag=VOICE,
        idioms=[
            ("Tout droit", "straight ahead", "straight on"),
            ("À deux pas", "at two steps", "a stone's throw away"),
            ("Au coin de la rue", "at the corner of the street", "just around the corner"),
            ("Bon voyage", "good trip", "have a good trip"),
            ("Aller-retour", "going-return", "return ticket"),
            ("À l'heure", "at the hour", "on time"),
            ("En retard", "in delay", "late"),
            ("Prendre le métro", "to take the metro", "to take the metro"),
            ("Se perdre", "to lose oneself", "to get lost"),
            ("Tomber bien", "to fall well", "to come in handy, to be well timed"),
        ],
        mistakes=[
            ("Il est une heure et demie et demi.", "Il est une heure et demie.", "One o'clock takes the singular: il est une heure et demie."),
            ("Le train part à neuf heures quart.", "Le train part à neuf heures et quart.", "The quarter takes et: et quart."),
            ("Je vais à pied à la gare en marchant.", "Je vais à pied à la gare.", "One expression of walking is enough."),
        ],
        task_title="Direct someone across your town",
        task_instructions=("Write six French steps from your home to a place you go often: two "
                           "landmarks (à côté de, en face de), one ticket or fare question, and one "
                           "time (et demie, moins le quart, or a 24-hour time). Give it to someone "
                           "who must follow it without asking you anything. Where they hesitate, "
                           "the missing word is almost always a relation — à côté de, en face de, "
                           "derrière."),
    ),
    "test": [
        ("translate_en", "Say: Where is the station, please?", "Où est la gare, s'il vous plaît ?"),
        ("translate_fr", "Allez tout droit et tournez à gauche au coin.", "Go straight ahead and turn left at the corner."),
        ("multiple_choice", "Which is the polite request?", "Vous pouvez me faire un prix ?"),
        ("fill_in_the_blank", "C'est ___ , un billet pour le centre ?", "combien"),
        ("word_selection", "Select the French for seventy.", "soixante-dix"),
        ("error_correction", "La pharmacie est à côté le marché.", "La pharmacie est à côté du marché."),
        ("dialogue_completion", "Complete: Vous pouvez me faire un ___ ?", "prix"),
        ("matching", "Match « en face de » to its meaning.", "opposite"),
        ("reading_comprehension", "Le train a cinq minutes de retard. How late is the train?", "five minutes"),
        ("inference", "« C'est un peu cher » — what is the speaker doing?", "bargaining politely"),
        ("main_idea", "Du lundi au vendredi, je travaille. What is this about?", "the working week"),
        ("detail_identification", "Il est trois heures et demie. What time is it?", "3:30"),
    ],
}

THIRD["B1"] = [
    ("B1-U1", "B1-U1-L3", L(
        "Raconter une anecdote : d'abord, ensuite, finalement",
        "A story in French is signposted: D'ABORD … , ENSUITE … , PUIS … , FINALEMENT. The frame "
        "keeps the tense honest — passé composé for the events, imparfait for the scene behind them.",
        [V("d'abord", "dah-BOR", "first", "adverb"),
         V("ensuite", "ah(n)-SWEET", "then, next", "adverb"),
         V("finalement", "fee-nal-MAH(N)", "finally", "adverb"),
         V("tout à coup", "too tah KOO", "suddenly", "phrase"),
         V("au final", "oh fee-NAL", "in the end", "phrase")],
        G("Story signposts",
          "d'abord … · ensuite … · puis … · tout à coup … · finalement …",
          "D'abord je suis arrivé à la gare. Ensuite, tout à coup, le train s'est arrêté. Puis "
          "nous avons attendu une heure. Finalement, je suis rentré à pied. Signposts carry the "
          "listener; the tenses carry the time.",
          [X("D'abord, je suis arrivé à la gare.", "dah-BOR, zhuh swee zah-ree-VAY ah lah GAR.", "First, I arrived at the station."),
           X("Tout à coup, le train s'est arrêté.", "too tah KOO, luh tra(n) say tah-reh-TAY.", "Suddenly the train stopped."),
           X("Finalement, je suis rentré à pied.", "fee-nal-MAH(N), zhuh swee rah(n)-TRAY ah PYAY.", "In the end I walked home.")],
          [("Ensuite, toujours, puis répétition.", "Ensuite, le train est parti.", "One signpost per move."),
           ("J'étais arrivé à la gare à huit heures.", "Je suis arrivé à la gare à huit heures.", "A single finished arrival takes the passé composé, not plus-que-parfait.")]),
        [D("Théo", "Raconte-moi ta journée.", "rah-koh(n)t-MWAH tah zhooR-NEE.", "Tell me about your day."),
         D("Léa", "D'abord, le train a eu une heure de retard.", "dah-BOR, luh tra(n) ah ü ÜN UHR duh ruh-TAR.", "First, the train was an hour late."),
         D("Théo", "Et ensuite ?", "ay ah(n)-SWEET ?", "And then?"),
         D("Léa", "Ensuite, tout à coup, il est arrivé : finalement, je suis rentrée très tard.", "ah(n)-SWEET, too tah KOO, eel ay tah-ree-VAY : fee-nal-MAH(N), zhuh swee rah(n)-TRAY tray TAR.", "Then, all of a sudden, it arrived: in the end I got home very late.")],
        WS("Story worksheet", [
            T("Chain the anecdote.", ["first the train was late", "then it arrived suddenly", "finally I got home late"],
              ["D'abord, le train a eu du retard.", "Ensuite, tout à coup, il est arrivé.", "Finalement, je suis rentré tard."]),
            T("Order the moves.", ["first", "then", "finally"],
              ["d'abord", "ensuite", "finalement"]),
        ]))),
    ("B1-U2", "B1-U2-L3", L(
        "Postuler : CV, entretien, expérience",
        "Job talk names experience with ÇA FAIT … QUE + present, and the wish with JE SUIS INTÉRESSÉ "
        "PAR. The interview frame: PARLEZ-MOI DE VOTRE PARCOURS.",
        [V("le parcours", "luh par-KOOR", "career path", "noun"),
         V("l'expérience", "lek-speh-RYAH(N)S", "experience", "noun"),
         V("le poste", "luh POST", "position, job", "noun"),
         V("le CV", "luh say-VAY", "CV, résumé", "noun"),
         V("l'entretien", "lah(n)-truh-TYA(N)", "interview", "noun")],
        G("Experience frame",
          "ça fait + durée + que + présent · je suis intéressé(e) par … · je m'occupe de …",
          "Ça fait trois ans que je travaille dans la logistique. Je m'occupe des livraisons et je "
          "suis intéressée par ce poste. The ça fait … que frame is the spoken way to state a "
          "duration that is still running.",
          [X("Ça fait trois ans que je travaille dans la logistique.", "sah feh trwah ZAH(N) kuh zhuh trah-VAHY dah(n) lah loh-zhees-TEEK.", "I have been working in logistics for three years."),
           X("Je m'occupe des livraisons.", "zhuh moh-KÜP day lee-vee-zOH(N).", "I handle deliveries."),
           X("Je suis intéressée par ce poste.", "zhuh swee za(n)-tay-reh-SAY par suh POST.", "I am interested in this position.")],
          [("Je travaille dans la logistique pendant trois ans.", "Ça fait trois ans que je travaille dans la logistique.", "pendant counts a closed stretch; a duration still running takes depuis or, in speech, ça fait … que."),
           ("Je suis intéressé pour ce poste.", "Je suis intéressé par ce poste.", "Interest in something takes par.")]),
        [D("Recruteuse", "Parlez-moi de votre parcours.", "par-LAY-MWAH duh votr par-KOOR.", "Tell me about your career path."),
         D("Léa", "Ça fait trois ans que je travaille dans la logistique.", "sah feh trwah ZAH(N) kuh zhuh trah-VAHY dah(n) lah loh-zhees-TEEK.", "I have been working in logistics for three years."),
         D("Recruteuse", "Et pourquoi ce poste ?", "ay poor-KWAH suh POST ?", "And why this position?"),
         D("Léa", "Je m'occupe déjà des livraisons et je suis intéressée par l'organisation du service.", "zhuh moh-KÜP day-ZHAH day lee-vee-zOH(N) ay zhuh swee za(n)-tay-reh-SAY par lohr-gah-nee-zah-SYOH(N) dü sehr-VEES.", "I already handle deliveries and I am interested in how the department is organised.")],
        WS("Interview worksheet", [
            T("State your experience.", ["three years in logistics", "I handle deliveries"],
              ["Ça fait trois ans que je travaille dans la logistique.", "Je m'occupe des livraisons."]),
            T("Answer the questions.", ["why this position?", "what is your goal?"],
              ["Je suis intéressé par ce poste.", "Mon objectif est de …"]),
        ]))),
    ("B1-U3", "B1-U3-L3", L(
        "Fixer un rendez-vous : déplacer, annuler",
        "Appointments move with three verbs: DÉPLACER (move), ANNULER (cancel), CONFIRMER. "
        "« Ça te va ? » checks the time without imposing it.",
        [V("déplacer", "day-plah-SAY", "to move (an appointment)", "verb"),
         V("annuler", "ah-nü-LAY", "to cancel", "verb"),
         V("confirmer", "koh(n)-feer-MAY", "to confirm", "verb"),
         V("le rendez-vous", "luh rah(n)-day-VOO", "appointment", "noun"),
         V("ça te va", "sah tuh VAH", "does that suit you", "phrase")],
        G("Appointment frame",
          "on se voit … ? · ça te va ? · je dois déplacer / annuler le rendez-vous",
          "On se voit mardi à dix heures ? Ça te va ? Sinon je dois déplacer le rendez-vous à "
          "jeudi. The question at the end leaves the other person a way out.",
          [X("On se voit mardi à dix heures ?", "oh(n) suh VWAH mar-DEE ah dee ZUHR ?", "Shall we meet Tuesday at ten?"),
           X("Ça te va ?", "sah tuh VAH ?", "Does that suit you?"),
           X("Je dois déplacer le rendez-vous à jeudi.", "zhuh DWAH day-plah-SAY luh rah(n)-day-VOO ah zhuh-DEE.", "I have to move the appointment to Thursday.")],
          [("Je dois annuler le rendez-vous à jeudi.", "Je dois déplacer le rendez-vous à jeudi.", "Annuler cancels; déplacer moves."),
           ("On se voit au mardi.", "On se voit mardi.", "Days take no preposition: mardi.")]),
        [D("Théo", "On se voit mardi à dix heures ?", "oh(n) suh VWAH mar-DEE ah dee ZUHR ?", "Shall we meet on Tuesday at ten?"),
         D("Léa", "Mardi, ça ne va pas — je dois déplacer.", "mar-DEE, sah nuh vah PAH — zhuh DWAH day-plah-SAY.", "Tuesday doesn't work — I have to move it."),
         D("Théo", "Jeudi, alors ?", "zhuh-DEE, ah-LOR ?", "Thursday, then?"),
         D("Léa", "Jeudi, parfait. Je confirme par message.", "zhuh-DEE, par-FEH. zhuh koh(n)-FEERM par meh-SAZH.", "Thursday, perfect. I'll confirm by message.")],
        WS("Appointment worksheet", [
            T("Fix the time.", ["shall we meet Tuesday?", "does that suit you?", "I have to move it to Thursday"],
              ["On se voit mardi ?", "Ça te va ?", "Je dois le déplacer à jeudi."]),
            T("Close the loop.", ["I'll confirm by message", "I have to cancel"],
              ["Je confirme par message.", "Je dois annuler."]),
        ]))),
]

THIRD["B2"] = [
    ("B2-U1", "B2-U1-L3", L(
        "Concéder et réfuter : certes…, néanmoins",
        "A French rebuttal gives the other side its due first: CERTES … , NÉANMOINS … ; IL EST "
        "VRAI QUE … , CELA DIT … The concession is what makes the refutation audible.",
        [V("certes", "SERT", "admittedly", "adverb"),
         V("néanmoins", "nay-ah(n)-MWA(N)", "nevertheless", "adverb"),
         V("cela dit", "suh-LAH DEE", "that said", "phrase"),
         V("la nuance", "lah nü-AH(N)S", "nuance", "noun"),
         V("à condition que", "ah koh(n)-dee-SYOH(N) kuh", "provided that", "phrase")],
        G("Two-storey concession",
          "certes … , néanmoins … · il est vrai que … , cela dit … · à condition que + subjonctif",
          "Certes, la mesure coûte cher ; néanmoins, elle évite un risque plus grand. Il est vrai "
          "que le délai est court ; cela dit, il est tenable à condition que deux personnes s'y "
          "consacrent. One concession, one counter, one condition.",
          [X("Certes, la mesure coûte cher.", "SERT, lah muh-ZÜR koot SHEHR.", "Admittedly, the measure is expensive."),
           X("Néanmoins, elle évite un risque plus grand.", "nay-ah(n)-MWA(N), el ay-VEET uh(n) reesk plü GRAH(N).", "Nevertheless, it avoids a bigger risk."),
           X("Cela dit, le délai est tenable à condition que deux personnes s'y consacrent.", "suh-LAH DEE, luh day-LAY ay tuh-NAHBL ah koh(n)-dee-SYOH(N) kuh duh per-SON see koh(n)-sahkr.", "That said, the deadline is feasible provided two people devote themselves to it.")],
          [("Certes, mais néanmoins, cela dit, il faut du temps.", "Certes, il faut du temps ; néanmoins, le délai est tenable.", "One concession marker, one counter marker."),
           ("À condition de que deux personnes …", "À condition que deux personnes …", "The conjunction is à condition que + subjunctive.")]),
        [D("Collègue", "La réforme coûte trop cher.", "lah ray-FORM koot troh SHEHR.", "The reform costs too much."),
         D("Léa", "Certes, elle coûte cher ; néanmoins, elle évite un risque plus grand.", "SERT, el koot SHEHR ; nay-ah(n)-MWA(N), el ay-VEET uh(n) reesk plü GRAH(N).", "Admittedly it is expensive; nevertheless, it avoids a bigger risk."),
         D("Collègue", "Et le délai ?", "ay luh day-LAY ?", "And the deadline?"),
         D("Léa", "Il est tenable, à condition que deux personnes s'y consacrent.", "eel ay tuh-NAHBL, ah koh(n)-dee-SYOH(N) kuh duh per-SON see koh(n)-sahkr.", "It is feasible, provided two people devote themselves to it.")],
        WS("Rebuttal worksheet", [
            T("Concede, then counter.", ["admittedly it is expensive", "nevertheless it avoids a bigger risk", "provided two people work on it"],
              ["Certes, c'est cher.", "Néanmoins, cela évite un risque plus grand.", "à condition que deux personnes s'y consacrent"]),
            T("Name the nuance.", ["that said, the deadline is feasible", "there is a nuance"],
              ["Cela dit, le délai est tenable.", "Il y a une nuance."]),
        ]))),
    ("B2-U2", "B2-U2-L3", L(
        "Le courriel formel : objet, appel, formule",
        "A French formal email has three shelves: OBJET (subject), MADAME, MONSIEUR, (no name after "
        "the colon), and a closing formula — JE VOUS PRIE D'AGRÉER MES SALUTATIONS DISTINGUÉES.",
        [V("l'objet", "lob-ZHAY", "subject", "noun"),
         V("la pièce jointe", "lah pyess zhwa(n)KT", "attachment", "noun"),
         V("je vous prie de", "zhuh voo PREE duh", "I request that you", "phrase"),
         V("salutations distinguées", "sah-lü-tah-SYOH(N) dees-ta(n)-GAY", "kind regards (formal)", "phrase"),
         V("cordialement", "kor-dyal-MAH(N)", "best regards", "adverb")],
        G("Email frame",
          "Objet : … · Madame, Monsieur, · je me permets de vous écrire … · Cordialement / je vous prie d'agréer …",
          "Objet : Demande de devis. Madame, Monsieur, je me permets de vous écrire au sujet du "
          "chantier de mai. Vous trouverez la pièce jointe. Je vous prie d'agréer mes salutations "
          "distinguées. The register tightens as the email goes down the page.",
          [X("Objet : Demande de devis.", "ob-ZHAY : duh-MAH(N)D duh duh-VEE.", "Subject: Quote request."),
           X("Je me permets de vous écrire au sujet de …", "zhuh muh per-MEH duh voo zay-KREER oh sü-ZHAY duh …", "I take the liberty of writing to you about …"),
           X("Cordialement,", "kor-dyal-MAH(N),", "Best regards,")],
          [("Bonjour Madame Marie,", "Madame,", "Formal French uses the title alone; the first name stays out."),
           ("Salutations distinguées, Léa.", "Je vous prie d'agréer mes salutations distinguées.", "The full formula belongs at the end, after the request.")]),
        [D("Théo", "Comment je commence le courriel ?", "koh-MAH(N) zhuh koh-MAH(N)S luh koo-RYEL ?", "How do I start the email?"),
         D("Léa", "« Objet : … », puis « Madame, Monsieur, ».", "ob-ZHAY : …, pwee mah-DAHM, muh-SYUH.", "'Subject: …', then 'Dear Sir or Madam'."),
         D("Théo", "Et pour finir ?", "ay poor fee-NEER ?", "And to finish?"),
         D("Léa", "« Je vous prie d'agréer mes salutations distinguées. » Le registre se resserre vers le bas.", "zhuh voo PREE dah-gray-AY may sah-lü-tah-SYOH(N) dees-ta(n)-GAY. luh ruh-ZHEESTR suh ruh-SEHR vehr luh BAH.", "'I beg you to accept my distinguished greetings.' The register tightens as it goes down.")],
        WS("Email worksheet", [
            T("Open the email.", ["subject: quote request", "Dear Sir or Madam", "I am writing about the May project"],
              ["Objet : Demande de devis.", "Madame, Monsieur,", "Je me permets de vous écrire au sujet du projet de mai."]),
            T("Close the email.", ["kind regards (formal)", "best regards"],
              ["Je vous prie d'agréer mes salutations distinguées.", "Cordialement,"]),
        ]))),
    ("B2-U3", "B2-U3-L3", L(
        "Lire les nouvelles : du titre au rapport",
        "A headline and a report say the same thing in two grammars: « Chômage en hausse » piles "
        "nouns, while « le taux de chômage a augmenté de 2 % » builds a sentence with a verb and a "
        "figure.",
        [V("le titre", "luh TEETR", "headline", "noun"),
         V("le taux", "luh TOH", "rate", "noun"),
         V("la hausse", "lah OHS", "rise", "noun"),
         V("la source", "lah SOORS", "source", "noun"),
         V("selon", "suh-LOH(N)", "according to", "preposition")],
        G("Headline ↔ report",
          "chômage en hausse (titre) · le taux de chômage a augmenté de 2 % (rapport) · selon + source",
          "Le titre annonce : « Chômage en hausse ». Le rapport précise : le taux de chômage a "
          "augmenté de deux pour cent au premier trimestre, selon l'INSEE. A translator moves "
          "between the pile and the sentence on purpose.",
          [X("Titre : Chômage en hausse.", "TEETR : shoh-MAZH ah(n) OHS.", "Headline: unemployment up."),
           X("Le taux a augmenté de deux pour cent.", "luh TOH ah ohg-mah(n)-TAY duh duh poor SAH(N).", "The rate rose by two per cent."),
           X("Selon l'INSEE, la hausse ralentit.", "suh-LOH(N) leen-SAY, lah OHS rah-lah(n)-TEE.", "According to INSEE, the rise is slowing.")],
          [("Le taux a augmenté de deux pour cent parce que c'est la crise.", "Le taux a augmenté de deux pour cent au premier trimestre.", "The report states the figure and its period; the cause is a different sentence."),
           ("Selon l'INSEE a dit que …", "Selon l'INSEE, …", "selon takes a source, not a clause with a verb.")]),
        [D("Léa", "Le titre dit « Chômage en hausse ».", "luh TEETR dee shoh-MAZH ah(n) OHS.", "The headline says 'unemployment up'."),
         D("Théo", "Le rapport, lui, donne la période et la source.", "luh rah-POR, lwee, don lah pay-RYOD ay lah SOORS.", "The report gives the period and the source."),
         D("Léa", "« Le taux a augmenté de deux pour cent au premier trimestre, selon l'INSEE. »", "luh TOH ah ohg-mah(n)-TAY duh duh poor SAH(N) oh pruh-MYAY tree-MEHSTR, suh-LOH(N) leen-SAY.", "'The rate rose by two per cent in the first quarter, according to INSEE.'"),
         D("Théo", "Voilà. Le titre vend, le rapport vérifie.", "vwah-LAH. luh TEETR vah(n), luh rah-POR vay-ree-FEE.", "There you go. The headline sells, the report verifies.")],
        WS("News worksheet", [
            T("Turn the headline into a report sentence.", ["unemployment up", "prices falling"],
              ["Le taux de chômage a augmenté de 2 %.", "Les prix ont baissé légèrement."]),
            T("Turn the report sentence into a headline.", ["the rate rose by two per cent", "consumption fell"],
              ["Chômage en hausse.", "Consommation en baisse."]),
        ]))),
]

THIRD["C1"] = [
    ("fr-c1-u1", "fr-c1-l7", L(
        "Attribution sans caution : selon, d'après, il semblerait que",
        "French distances a claim with frames: SELON X, D'APRÈS X, À EN CROIRE X, IL SEMBLERAIT "
        "QUE. The frame names who owns the claim and keeps the speaker out of it.",
        [V("selon", "suh-LOH(N)", "according to", "preposition"),
         V("d'après", "dah-PREH", "according to", "preposition"),
         V("il semblerait que", "eel sah(n)-bluh-RAY kuh", "it would seem that", "phrase"),
         V("à en croire", "ah ah(n) KRWAHR", "if we believe", "phrase"),
         V("la source", "lah SOORS", "source", "noun")],
        G("Attribution frames",
          "selon + source · d'après + source · il semblerait que + subjonctif · à en croire + source",
          "Selon deux sources concordantes, le dossier serait bloqué. D'après l'AFP, la décision "
          "serait reportée. Il semblerait que le ministre ait changé d'avis. The conditional "
          "(serait) and the subjunctive (ait) keep the claim at arm's length.",
          [X("Selon deux sources, le dossier serait bloqué.", "suh-LOH(N) duh SOORS, luh doh-SYAY suh-RAY bloh-KAY.", "According to two sources, the file is reportedly blocked."),
           X("D'après l'AFP, la décision serait reportée.", "dah-PREH lah-ef-PAY, lah day-see-ZYOH(N) suh-RAY ruh-por-TAY.", "According to AFP, the decision is reportedly postponed."),
           X("Il semblerait que le ministre ait changé d'avis.", "eel sah(n)-bluh-RAY kuh luh mee-NEESTR ay shah(n)-ZHAY dah-VEE.", "It would seem the minister has changed his mind.")],
          [("Selon le journal dit que le dossier est bloqué.", "Selon le journal, le dossier serait bloqué.", "selon takes a source phrase, not a finite clause."),
           ("Il semblerait que le ministre a changé d'avis.", "Il semblerait que le ministre ait changé d'avis.", "il semblerait que takes the subjunctive.")]),
        [D("Analyst", "Que sait-on au juste ?", "kuh seh-TOH(N) oh ZHÜST ?", "What do we actually know?"),
         D("Colleague", "Selon deux sources, le dossier serait bloqué.", "suh-LOH(N) duh SOORS, luh doh-SYAY suh-RAY bloh-KAY.", "According to two sources, the file is reportedly blocked."),
         D("Analyst", "Et la décision ?", "ay lah day-see-ZYOH(N) ?", "And the decision?"),
         D("Colleague", "D'après l'AFP, elle serait reportée — rien d'officiel.", "dah-PREH lah-ef-PAY, el suh-RAY ruh-por-TAY — rya(n) doh-fee-SYEL.", "According to AFP it is reportedly postponed — nothing official.")],
        WS("Attribution worksheet", [
            T("Put the claim at arm's length.", ["the file is blocked (two sources)", "the decision is postponed (AFP)"],
              ["Selon deux sources, le dossier serait bloqué.", "D'après l'AFP, la décision serait reportée."]),
            T("Name the source, not the fact.", ["nothing official", "it would seem"],
              ["Rien d'officiel.", "Il semblerait que …"]),
        ]))),
    ("fr-c1-u2", "fr-c1-l8", L(
        "La causalité graduée : contribuer à, expliquer en partie",
        "Careful French causal prose grades the link: CONTRIBUER À (contributes), EXPLIQUER EN "
        "PARTIE (partly explains), ÊTRE LIÉ À (is linked to), NE PAS SUFFIRE À (is not enough to).",
        [V("contribuer à", "koh(n)-tree-BÜ-AY ah", "to contribute to", "verb"),
         V("en partie", "ah(n) par-TEE", "partly", "phrase"),
         V("être lié à", "etr LYAY ah", "to be linked to", "phrase"),
         V("suffire à", "sü-FEER ah", "to be enough to", "verb"),
         V("la corrélation", "lah koh-ray-lah-SYOH(N)", "correlation", "noun")],
        G("Calibrated cause",
          "contribue à … · explique en partie … · est lié à … · ne suffit pas à …",
          "La sécheresse contribue à la hausse, mais elle ne suffit pas à l'expliquer. Le coût de "
          "l'énergie est lié à la même tendance. A correlation is not a cause, and the verbs say "
          "so before the conclusion does.",
          [X("La sécheresse contribue à la hausse.", "lah say-SHRESS koh(n)-tree-BÜ ah lah OHS.", "The drought contributes to the rise."),
           X("Elle ne suffit pas à l'expliquer.", "el nuh sü-FEE pah ah lek-splee-KAY.", "It is not enough to explain it."),
           X("Une corrélation n'est pas une cause.", "ün koh-ray-lah-SYOH(N) nay pah zün KOHZ.", "A correlation is not a cause.")],
          [("La sécheresse explique la hausse à cent pour cent.", "La sécheresse contribue à la hausse.", "Grade the link: contributing is not causing."),
           ("Une corrélation explique une cause.", "Une corrélation ne suffit pas à établir une cause.", "Name the limit of the evidence.")]),
        [D("Chair", "Pourquoi cette hausse ?", "poor-KWAH set OHS ?", "Why this rise?"),
         D("Analyst", "La sécheresse contribue à la hausse.", "lah say-SHRESS koh(n)-tree-BÜ ah lah OHS.", "The drought contributes to the rise."),
         D("Chair", "C'est la cause ?", "say lah KOHZ ?", "Is that the cause?"),
         D("Analyst", "Elle l'explique en partie. Le reste tient aux coûts de l'énergie.", "el lek-spleek ah(n) par-TEE. luh REST tya(n) oh koo duh lay-ner-ZHEE.", "It partly explains it. The rest is down to energy costs.")],
        WS("Causality worksheet", [
            T("Grade the link.", ["contributes to", "partly explains", "is not enough to"],
              ["contribue à", "explique en partie", "ne suffit pas à"]),
            T("State the limit.", ["a correlation is not a cause", "the rest is down to energy costs"],
              ["Une corrélation n'est pas une cause.", "Le reste tient aux coûts de l'énergie."]),
        ]))),
    ("fr-c1-u3", "fr-c1-l9", L(
        "La synthèse de deux sources en un paragraphe",
        "Synthesis names the sources and then speaks with one voice: SELON L'INSTITUT … ; LE "
        "SYNDICAT, DE SON CÔTÉ, … ; CE QUI LES RÉUNIT, C'EST QUE …",
        [V("de son côté", "duh soh(n) koh-TAY", "on its side", "phrase"),
         V("ce qui les réunit", "suh kee lay ray-ü-NEE", "what brings them together", "phrase"),
         V("converger", "koh(n)-ver-ZHAY", "to converge", "verb"),
         V("diverger", "dee-ver-ZHAY", "to diverge", "verb"),
         V("la synthèse", "lah sa(n)-TEHZ", "synthesis", "noun")],
        G("Source sandwich",
          "selon A … · B, de son côté, … · ce qui les réunit, c'est que … · sur ce point, ils divergent",
          "Selon l'institut, la tendance est stable. Le syndicat, de son côté, signale des "
          "risques. Ce qui les réunit, c'est que les données manquent. Three sentences: two "
          "positions, one shared ground.",
          [X("Selon l'institut, la tendance est stable.", "suh-LOH(N) la(n)-stee-TÜ, lah tah(n)-DAH(N)S ay stah-BL.", "According to the institute, the trend is stable."),
           X("Le syndicat, de son côté, signale des risques.", "luh sa(n)-dee-KAH, duh soh(n) koh-TAY, see-NYAL day REESK.", "The union, for its part, points to risks."),
           X("Sur ce point, ils divergent.", "sür suh PWA(N), eel dee-ver-ZH.", "On this point they diverge.")],
          [("Les deux disent la même chose et l'inverse.", "Ce qui les réunit, c'est que les données manquent.", "A synthesis names shared ground and difference separately."),
           ("Selon les deux, de son côté.", "Selon l'institut ; le syndicat, de son côté, …", "One source per clause.")]),
        [D("Chair", "Une synthèse, s'il vous plaît.", "ün sa(n)-TEHZ, seel voo PLAY.", "A summary, please."),
         D("Analyst", "Selon l'institut, la tendance est stable ; le syndicat, de son côté, signale des risques.", "suh-LOH(N) la(n)-stee-TÜ, lah tah(n)-DAH(N)S ay stah-BL ; luh sa(n)-dee-KAH, duh soh(n) koh-TAY, see-NYAL day REESK.", "According to the institute the trend is stable; the union, for its part, points to risks."),
         D("Chair", "Et le terrain commun ?", "ay luh teh-RA(N) koh-MÜ(N) ?", "And the common ground?"),
         D("Analyst", "Ce qui les réunit, c'est que les données manquent.", "suh kee lay ray-ü-NEE, say kuh lay doh-NAY MAH(N)K.", "What brings them together is that the data is missing.")],
        WS("Synthesis worksheet", [
            T("Line the sources up.", ["according to the institute", "the union, for its part"],
              ["Selon l'institut, …", "Le syndicat, de son côté, …"]),
            T("Write the synthesis.", ["the common ground", "on this point they diverge"],
              ["Ce qui les réunit, c'est que …", "Sur ce point, ils divergent."]),
        ]))),
]

THIRD["C2"] = [
    ("fr-c2-u1", "fr-c2-l7", L(
        "Le discours indirect libre : deux voix dans une phrase",
        "Free indirect discourse fuses narrator and character: « Il hésitait. Partir ? Rester ? La "
        "ville était trop chère, et puis il y avait le travail. » No quotation marks, no reporting "
        "verb — the questions and the collocations carry the character's voice.",
        [V("l'hésitation", "lay-zee-tah-SYOH(N)", "hesitation", "noun"),
         V("la voix", "lah VWAH", "voice", "noun"),
         V("le narrateur", "luh nah-rah-TUHR", "narrator", "noun"),
         V("le point de vue", "luh pwa(n) duh VÜ", "point of view", "noun"),
         V("sans guillemets", "sah(n) gee-YEH", "without quotation marks", "phrase")],
        G("Free indirect style",
          "no reporting verb · character's questions and vocabulary · tense shifted one step back",
          "Il hésitait. Partir ? Rester ? La ville était trop chère, et puis il y avait le travail. "
          "The narrative tense stays (imparfait), but the questions and « et puis » are the "
          "character's, not the narrator's.",
          [X("Il hésitait. Partir ? Rester ?", "eel ay-zee-TAY. par-TEER ? res-TAY ?", "He hesitated. Leave? Stay?"),
           X("La ville était trop chère.", "lah VEEL ay-TAY troh SHEHR.", "The city was too expensive."),
           X("Et puis il y avait le travail.", "ay pwee eel yah-VAY luh trah-VAHY.", "And then there was the job.")],
          [("Il hésitait et il pensait : « partir ou rester ? » (with quotes).", "Il hésitait. Partir ? Rester ?", "The free form drops the quotation marks and the reporting verb."),
           ("Il hésite. Partir ? Rester ? (in a past narrative).", "Il hésitait. Partir ? Rester ?", "The narrative tense stays in the past.")]),
        [D("Editor", "Cette phrase, c'est vous ou lui ?", "set FREZ, say voo oo LWEE ?", "That sentence — is it you or him?"),
         D("Author", "C'est lui. Sans guillemets, c'est le discours indirect libre.", "say LWEE. sah(n) gee-YEH, say luh dees-KOOR a(n)-dee-REKT LEEBR.", "It's him. Without quotation marks, it's free indirect discourse."),
         D("Editor", "Et le lecteur ne se perd pas ?", "ay luh lek-TUHR nuh suh PAIR pah ?", "And the reader doesn't get lost?"),
         D("Author", "Si le vocabulaire est à lui, non. « Et puis » signale sa voix.", "see luh voh-kah-bü-LEHR ay tah LWEE, noh(n). ay pwee see-NYAL sah VWAH.", "If the vocabulary is his, no. 'And then' signals his voice.")],
        WS("Free indirect worksheet", [
            T("Turn the quotation into free indirect style.", ["He said: ‘Should I leave?'", "She thought: ‘The city is too expensive.'"],
              ["Il hésitait. Partir ?", "Elle songeait. La ville était trop chère."]),
            T("Mark the character's voice.", ["without quotation marks", "the narrator's point of view"],
              ["sans guillemets", "le point de vue du narrateur"]),
        ]))),
    ("fr-c2-u2", "fr-c2-l8", L(
        "La précision juridique à l'oral : définir, délimiter, exclure",
        "Legal precision is spoken as three moves: DÉFINIR (what the term covers), DÉLIMITER "
        "(where it stops), EXCLURE (what it does not cover). « Au sens du présent texte … »",
        [V("au sens de", "oh SAH(N)S duh", "within the meaning of", "phrase"),
         V("délimiter", "day-lee-mee-TAY", "to delimit", "verb"),
         V("exclure", "eks-KLÜR", "to exclude", "verb"),
         V("le champ d'application", "luh shah(n) dah-plee-kah-SYOH(N)", "scope", "noun"),
         V("nonobstant", "noh-nob-STAH(N)", "notwithstanding", "preposition")],
        G("Legal precision",
          "au sens du présent texte … · le champ d'application couvre … · sont exclus … · nonobstant …",
          "Au sens du présent texte, le délai court à compter de la notification. Sont exclus les "
          "cas de force majeure, nonobstant toute clause contraire. Define, delimit, exclude — in "
          "that order, in one breath.",
          [X("Au sens du présent texte, le délai court à compter de la notification.", "oh SAH(N)S dü pray-zah(n) TEKST, luh day-LAY koor ah koh(n)t-TAY duh lah noh-tee-fee-kah-SYOH(N).", "Within the meaning of this text, the period runs from notification."),
           X("Sont exclus les cas de force majeure.", "so(n) teks-KLÜ lay kah duh fors mah-ZHÜR.", "Cases of force majeure are excluded."),
           X("Nonobstant toute clause contraire.", "noh-nob-STAH(N) toot KLOHZ koh(n)-TREHR.", "Notwithstanding any clause to the contrary.")],
          [("Le délai, c'est-à-dire environ un mois, nonobstant.", "Le délai court à compter de la notification.", "Legal speech defines the start; the approximate duration comes later."),
           ("Sont exclus peut-être les cas de force majeure.", "Sont exclus les cas de force majeure.", "The exclusion is categorical, never hedged.")]),
        [D("Colleague", "Quand commence le délai ?", "kah(n) koh-MAH(N)S luh day-LAY ?", "When does the period start?"),
         D("Analyst", "Au sens du présent texte, il court à compter de la notification.", "oh SAH(N)S dü pray-zah(n) TEKST, eel koor ah koh(n)t-TAY duh lah noh-tee-fee-kah-SYOH(N).", "Within the meaning of this text, it runs from notification."),
         D("Colleague", "Et les retards de l'administration ?", "ay lay ruh-TAR duh lah-dmee-nees-trah-SYOH(N) ?", "And administrative delays?"),
         D("Analyst", "Sont exclus les cas de force majeure, nonobstant toute clause contraire.", "so(n) teks-KLÜ lay kah duh fors mah-ZHÜR, noh-nob-STAH(N) toot KLOHZ koh(n)-TREHR.", "Cases of force majeure are excluded, notwithstanding any clause to the contrary.")],
        WS("Legal-precision worksheet", [
            T("Define, delimit, exclude.", ["within the meaning of this text", "excluding force majeure", "notwithstanding any contrary clause"],
              ["Au sens du présent texte, …", "Sont exclus les cas de force majeure.", "Nonobstant toute clause contraire."]),
            T("Name the scope.", ["scope of application", "the period runs from notification"],
              ["le champ d'application", "le délai court à compter de la notification"]),
        ]))),
    ("fr-c2-u3", "fr-c2-l9", L(
        "Réécrire pour un autre public : du rapport au communiqué",
        "Mediation is rewriting one content for a new reader: the same paragraph becomes a report "
        "sentence, a press release, and a line for a general audience. The facts do not move; the "
        "frame does.",
        [V("réécrire", "ray-EKREER", "to rewrite", "verb"),
         V("le communiqué", "luh koh-mü-nee-KAY", "press release", "noun"),
         V("le grand public", "luh grah(n) pü-BLEEK", "the general public", "noun"),
         V("vulgariser", "vül-gah-ree-ZAY", "to make accessible", "verb"),
         V("en clair", "ah(n) KLEHR", "in plain terms", "phrase")],
        G("Three registers, one fact",
          "report: le taux a augmenté de 2 % au premier trimestre · communiqué: la tendance reste maîtrisée · grand public: en clair, ça monte un peu",
          "Le rapport écrit : le taux a augmenté de deux pour cent au premier trimestre. Le "
          "communiqué : la tendance reste maîtrisée. Pour le grand public : en clair, ça monte un "
          "peu. Three sentences, one figure, three readers.",
          [X("Le taux a augmenté de deux pour cent au premier trimestre.", "luh TOH ah ohg-mah(n)-TAY duh duh poor SAH(N) oh pruh-MYAY tree-MEHSTR.", "The rate rose by two per cent in the first quarter."),
           X("La tendance reste maîtrisée.", "lah tah(n)-DAH(N)S rest may-tree-ZAY.", "The trend remains under control."),
           X("En clair, ça monte un peu.", "ah(n) KLEHR, sah MOH(N)T uh(n) PÜ.", "In plain terms, it is going up a little.")],
          [("Le communiqué invente un chiffre plus rassurant.", "Le communiqué garde le chiffre et change le cadre.", "Mediation never invents; it reframes."),
           ("Pour le grand public : le taux a augmenté de deux pour cent au premier trimestre.", "Pour le grand public : en clair, ça monte un peu.", "Vulgariser means finding the ordinary phrase, not repeating the report.")]),
        [D("Editor", "Vous avez trois publics : le rapport, le communiqué, la une.", "voo zah-VAY trwah pü-BLEE : luh rah-POR, luh koh-mü-nee-KAY, lah ÜN.", "You have three audiences: the report, the press release, the front page."),
         D("Author", "Le rapport garde le chiffre : le taux a augmenté de deux pour cent.", "luh rah-POR gard luh SHEEFR : luh TOH ah ohg-mah(n)-TAY duh duh poor SAH(N).", "The report keeps the figure: the rate rose by two per cent."),
         D("Editor", "Le communiqué ?", "luh koh-mü-nee-KAY ?", "The press release?"),
         D("Author", "« La tendance reste maîtrisée. » Et pour la une : « en clair, ça monte un peu ».", "lah tah(n)-DAH(N)S rest may-tree-ZAY. ay poor lah ÜN : ah(n) KLEHR, sah MOH(N)T uh(n) PÜ.", "'The trend remains under control.' And for the front page: 'in plain terms, it is going up a little'.")],
        WS("Mediation worksheet", [
            T("Rewrite for each reader.", ["the figure (report)", "the trend (press release)", "in plain terms (general public)"],
              ["Le taux a augmenté de 2 %.", "La tendance reste maîtrisée.", "En clair, ça monte un peu."]),
            T("Keep the fact, change the frame.", ["one figure, three registers", "do not invent a figure"],
              ["Un chiffre, trois registres.", "On n'invente pas un chiffre."]),
        ]))),
]

HALFSTEPS["A2+"] = {
    "title": "French A2+ — Day-to-day business",
    "native": NATIVE,
    "goals": [
        "Exchange, return and complain about a purchase without raising your voice",
        "Run a phone call: answer, leave a message, fix a time, apologise for being late",
        "Say how the neighbourhood used to be, and tell yesterday as a chain of events",
    ],
    "units": [
        {"id": "A2+-U1", "title": "Achats, échanges et réclamations", "lessons": [
            L("Échanger et rembourser : la taille, le ticket",
              "Returns run on four words: LA TAILLE, LE TICKET DE CAISSE, ÉCHANGER and REMBOURSER. "
              "« Ça ne me va pas » is the whole argument.",
              [V("la taille", "lah TAH-yuh", "size", "noun"),
               V("le ticket de caisse", "luh tee-KAY duh KES", "receipt", "noun"),
               V("échanger", "ay-shah(n)-ZHAY", "to exchange", "verb"),
               V("rembourser", "rah(n)-boor-SAY", "to refund", "verb"),
               V("essayer", "eh-say-YAY", "to try on", "verb")],
              G("Return frame",
                "je voudrais l'échanger contre … · vous pouvez me rembourser ? · avec le ticket",
                "J'ai acheté cette chemise hier et elle est trop petite. Je voudrais l'échanger "
                "contre une taille au-dessus. Avec le ticket, l'échange est immédiat.",
                [X("Je voudrais l'échanger contre une taille au-dessus.", "zhuh voo-DREH lay-shah(n)-ZHAY koh(n)-truh ün TAH-yuh oh-duh-SÜ.", "I would like to exchange it for one size bigger."),
                 X("Vous pouvez me rembourser ?", "voo poo-VAY muh rah(n)-boor-SAY ?", "Can you refund me?"),
                 X("J'ai le ticket de caisse.", "zhay luh tee-KAY duh KES.", "I have the receipt.")],
                [("Je veux rembourser cette chemise (as a demand with no receipt).", "Je voudrais l'échanger ; j'ai le ticket.", "The conditional keeps the shop assistant on your side."),
                 ("Elle est trop petit.", "Elle est trop petite.", "The shirt is feminine: petite.")]),
              [D("Théo", "Bonjour, j'ai acheté cette chemise hier.", "boh(n)-ZHOOR, zhay tahsh-TAY set shuh-MEEZ yehr.", "Hello, I bought this shirt yesterday."),
               D("Vendeuse", "Elle ne vous va pas ?", "el nuh voo vah PAH ?", "Doesn't it suit you?"),
               D("Théo", "Elle est trop petite. Je voudrais l'échanger.", "el ay troh puh-TEET. zhuh voo-DREH lay-shah(n)-ZHAY.", "It is too small. I would like to exchange it."),
               D("Vendeuse", "Avec le ticket, c'est immédiat.", "ah-vek luh tee-KAY, say tee-may-DYA.", "With the receipt, it's immediate.")],
              WS("Returns worksheet", [
                  T("Say what is wrong.", ["the shirt is too small", "the trousers are too long"],
                    ["La chemise est trop petite.", "Le pantalon est trop long."]),
                  T("Make the request.", ["exchange it for a bigger size", "I have the receipt"],
                    ["Je voudrais l'échanger contre une taille au-dessus.", "J'ai le ticket de caisse."]),
              ])),
            L("À la caisse : couleurs, prix, promotions",
              "Shop talk is short: VOUS L'AVEZ EN BLEU ? · C'EST EN PROMOTION · JE LA PRENDS. The "
              "conditional « je voudrais » softens every request.",
              [V("en promotion", "ah(n) proh-moh-SYOH(N)", "on offer", "phrase"),
               V("la caisse", "lah KES", "checkout", "noun"),
               V("la couleur", "lah koo-LUHR", "colour", "noun"),
               V("essayer", "eh-say-YAY", "to try on", "verb"),
               V("je la prends", "zhuh lah PRAH(N)", "I'll take it", "phrase")],
              G("At the checkout",
                "vous l'avez en + couleur ? · c'est en promotion · je la prends",
                "Vous l'avez en bleu, en quarante ? C'est en promotion cette semaine : moins vingt "
                "pour cent. Je la prends. The colour and the size arrive with en.",
                [X("Vous l'avez en bleu ?", "voo lah-VAY ah(n) BLUH ?", "Do you have it in blue?"),
                 X("C'est en promotion cette semaine.", "say tah(n) proh-moh-SYOH(N) set suh-MEN.", "It is on offer this week."),
                 X("Je la prends.", "zhuh lah PRAH(N)", "I'll take it.")],
                [("Vous l'avez bleu ?", "Vous l'avez en bleu ?", "Colours take en when you buy them."),
                 ("C'est promotion cette semaine.", "C'est en promotion cette semaine.", "An offer takes en: c'est en promotion; the reduction itself is spoken as moins vingt.")]),
              [D("Léa", "Vous l'avez en bleu, en quarante ?", "voo lah-VAY ah(n) BLUH, ah(n) kah-RAH(N)T ?", "Do you have it in blue, size forty?"),
               D("Vendeuse", "En bleu, oui. Et c'est en promotion.", "ah(n) BLUH, wee. ay say tah(n) proh-moh-SYOH(N).", "In blue, yes. And it is on offer."),
               D("Léa", "Moins combien ?", "mwa(n) koh(n)-BYA(N) ?", "How much off?"),
               D("Vendeuse", "Moins vingt pour cent. Vous la prenez ?", "mwa(n) vah(n) poor SAH(N). voo lah pruh-NAY ?", "Twenty per cent off. Are you taking it?")],
              WS("Checkout worksheet", [
                  T("Ask in the shop.", ["do you have it in blue?", "is it on offer?", "I'll take it"],
                    ["Vous l'avez en bleu ?", "C'est en promotion ?", "Je la prends."]),
                  T("Answer as the seller.", ["size forty", "twenty per cent off"],
                    ["en quarante", "moins vingt pour cent"]),
              ])),
            L("Réclamer avec calme : ça ne marche pas, il manque",
              "A complaint is a fact plus a request: ÇA NE MARCHE PAS, IL MANQUE UN BOUTON, VOUS "
              "POUVEZ REGARDER ?",
              [V("marcher", "mar-SHAY", "to work (device)", "verb"),
               V("il manque", "eel MAH(N)K", "there is missing", "phrase"),
               V("la garantie", "lah gah-rah(n)-TEE", "warranty", "noun"),
               V("réparer", "ray-pah-RAY", "to repair", "verb"),
               V("réclamer", "ray-klah-MAY", "to complain, to claim", "verb")],
              G("Complaint frame",
                "ça ne marche pas · il manque … · c'est sous garantie · vous pouvez regarder ?",
                "J'ai acheté cette montre la semaine dernière et elle ne marche pas. Il manque une "
                "pièce. C'est sous garantie : vous pouvez regarder ? Facts first, request second.",
                [X("Elle ne marche pas.", "el nuh mar-SH pah.", "It does not work."),
                 X("Il manque une pièce.", "eel MAH(N)K ün PYESS.", "A part is missing."),
                 X("C'est sous garantie, vous pouvez regarder ?", "say soo gah-rah(n)-TEE, voo poo-VAY ruh-gar-DAY ?", "It is under warranty, can you take a look?")],
                [("Ça ne marche rien du tout.", "Ça ne marche pas.", "One fact per complaint."),
                 ("Il manque d'une pièce.", "Il manque une pièce.", "manquer takes a direct object: il manque une pièce, with no de.")]),
              [D("Léa", "Bonjour, cette montre ne marche pas.", "boh(n)-ZHOOR, set MOH(N)TR nuh mar-SH pah.", "Hello, this watch does not work."),
               D("Vendeur", "Vous avez la garantie ?", "voo zah-VAY lah gah-rah(n)-TEE ?", "Do you have the warranty?"),
               D("Léa", "Oui, et il manque aussi une pièce.", "wee, ay eel MAH(N)K oh-SEE ün PYESS.", "Yes, and a part is missing too."),
               D("Vendeur", "On regarde et, si ça ne se répare pas, on échange.", "oh(n) ruh-GARD ay, see sah nuh suh ray-PAR pah, oh(n) nay-SHAHNZH.", "We'll look and, if it can't be repaired, we'll exchange it.")],
              WS("Complaint worksheet", [
                  T("State the problem and the request.", ["it doesn't work — can you look?", "a part is missing — it's under warranty"],
                    ["Ça ne marche pas, vous pouvez regarder ?", "Il manque une pièce, c'est sous garantie."]),
                  T("Ask what happens next.", ["can it be repaired?", "can it be exchanged?"],
                    ["Est-ce que ça peut se réparer ?", "Est-ce qu'on peut l'échanger ?"]),
              ])),
        ]},
        {"id": "A2+-U2", "title": "Téléphone et rendez-vous", "lessons": [
            L("Appeler et répondre : allô, je vous écoute",
              "French phones answer with ALLÔ ? The message runs: JE SUIS BIEN CHEZ … ? · C'EST DE LA "
              "PART DE QUI ? · JE PEUX LAISSER UN MESSAGE ?",
              [V("allô", "ah-LOH", "hello (phone)", "phrase"),
               V("le message", "luh meh-SAZH", "message", "noun"),
               V("de la part de", "duh lah PAR duh", "on behalf of", "phrase"),
               V("rappeler", "rah-puh-LAY", "to call back", "verb"),
               V("raccrocher", "rah-kroh-SHAY", "to hang up", "verb")],
              G("Phone frame",
                "allô ? · c'est de la part de qui ? · je peux laisser un message ? · je vous rappelle",
                "Allô ? — Bonjour, je suis bien chez M. Brun ? — Oui, c'est de la part de qui ? — Je "
                "peux laisser un message ? Note: on the phone French says « c'est » for the person.",
                [X("Bonjour, je suis bien chez M. Brun ?", "boh(n)-ZHOOR, zhuh swee BYA(N) shay muh-SYUH BRUH(N) ?", "Hello, am I through to Mr Brun?"),
                 X("C'est de la part de qui ?", "say duh lah PAR duh KEE ?", "Who is calling?"),
                 X("Je peux laisser un message ?", "zhuh puh lay-SAY uh(n) meh-SAZH ?", "Can I leave a message?")],
                [("Estoy Ana → Je suis Ana.", "Ici Ana. / Ana à l'appareil.", "French phone introductions use ici or à l'appareil, not je suis + name alone."),
                 ("Je peux laisser un massage ?", "Je peux laisser un message ?", "Watch the vowel: message, not massage.")]),
              [D("Secrétaire", "Cabinet Brun, bonjour ?", "kah-bee-NAY BRUH(N), boh(n)-ZHOOR ?", "Brun's office, hello?"),
               D("Léa", "Bonjour, je suis bien chez M. Brun ?", "boh(n)-ZHOOR, zhuh swee BYA(N) shay muh-SYUH BRUH(N) ?", "Hello, am I through to Mr Brun?"),
               D("Secrétaire", "C'est de la part de qui ?", "say duh lah PAR duh KEE ?", "Who is calling?"),
               D("Léa", "De la part de Léa Martin. Je peux laisser un message ?", "duh lah PAR duh lay-AH mar-TA(N). zhuh puh lay-SAY uh(n) meh-SAZH ?", "Léa Martin. Can I leave a message?")],
              WS("Phone worksheet", [
                  T("Run the call.", ["am I through to Mr Brun?", "who is calling?", "can I leave a message?"],
                    ["Je suis bien chez M. Brun ?", "C'est de la part de qui ?", "Je peux laisser un message ?"]),
                  T("Close the call.", ["I'll call back", "thank you, goodbye"],
                    ["Je vous rappelle.", "Merci, au revoir."]),
              ])),
            L("Rendez-vous et retards : excusez-moi du retard",
              "Appointments are fixed with ON SE VOIT … ? and apologised for with EXCUSEZ-MOI DU "
              "RETARD, J'ÉTAIS DANS LES EMBOUTEILLAGES.",
              [V("le retard", "luh ruh-TAR", "delay", "noun"),
               V("les embouteillages", "lay zah(n)-boo-tay-YAZH", "traffic jams", "noun"),
               V("excusez-moi", "eks-kü-zay-MWAH", "excuse me", "phrase"),
               V("être en route", "etr ah(n) ROOT", "to be on the way", "phrase"),
               V("annuler", "ah-nü-LAY", "to cancel", "verb")],
              G("Lateness frame",
                "on se voit à … ? · excusez-moi du retard · je suis en route · ça vous va ?",
                "On se voit à quinze heures ? — D'accord. — Excusez-moi du retard, j'étais dans les "
                "embouteillages. The apology names the cause, not the emotion.",
                [X("On se voit à quinze heures ?", "oh(n) suh VWAH ah KA(N)Z UHR ?", "Shall we meet at three?"),
                 X("Excusez-moi du retard.", "eks-kü-zay-MWAH dü ruh-TAR.", "Sorry I'm late."),
                 X("Je suis en route, j'arrive dans dix minutes.", "zhuh swee zah(n) ROOT, zhah-REEV dah(n) dee mee-NÜT.", "I'm on my way, I'll be there in ten minutes.")],
                [("Excusez-moi pour le retard de moi.", "Excusez-moi du retard.", "The fixed phrase takes du."),
                 ("Je suis très retard.", "Je suis en retard.", "Lateness is a state: en retard.")]),
              [D("Théo", "On se voit à quinze heures ?", "oh(n) suh VWAH ah KA(N)Z UHR ?", "Shall we meet at three?"),
               D("Léa", "D'accord. Je risque d'être un peu en retard.", "dah-KOR. zhuh reesk detr uh(n) puh ah(n) ruh-TAR.", "OK. I may be a little late."),
               D("Théo", "Pas de souci, préviens-moi.", "pah duh soo-SEE, pray-VYA(N)-MWAH.", "No problem, let me know."),
               D("Léa", "Excusez-moi du retard — j'étais dans les embouteillages.", "eks-kü-zay-MWAH dü ruh-TAR — zhay-TAY dah(n) lay zah(n)-boo-tay-YAZH.", "Sorry I'm late — I was stuck in traffic.")],
              WS("Appointment worksheet", [
                  T("Fix the time and apologise.", ["shall we meet at three?", "sorry I'm late, I was stuck in traffic"],
                    ["On se voit à quinze heures ?", "Excusez-moi du retard, j'étais dans les embouteillages."]),
                  T("Answer as the other person.", ["no problem, let me know", "I'll wait for you"],
                    ["Pas de souci, préviens-moi.", "Je t'attends."]),
              ])),
            L("Inviter et remercier : je t'invite, merci pour tout",
              "Invitations use JE T'INVITE À …; thanks are answered with DE RIEN, AVEC PLAISIR or the "
              "warmer C'EST MOI QUI TE REMERCIE.",
              [V("inviter", "a(n)-vee-TAY", "to invite, to treat", "verb"),
               V("amener", "ah-muh-NAY", "to bring (a person)", "verb"),
               V("apporter", "ah-por-TAY", "to bring (a thing)", "verb"),
               V("de rien", "duh RYA(N)", "you're welcome", "phrase"),
               V("avec plaisir", "ah-vek play-ZEER", "with pleasure", "phrase")],
              G("Invitations",
                "je t'invite à dîner · tu apportes quelque chose ? · merci pour tout · de rien",
                "Je t'invite à dîner vendredi. Tu apportes un dessert ? — Avec plaisir, merci. Note "
                "the pair apporter (a thing) / amener (a person).",
                [X("Je t'invite à dîner vendredi.", "zhuh ta(n)-VEET ah dee-NAY vah(n)-druh-DEE.", "I'm inviting you to dinner on Friday."),
                 X("Tu apportes un dessert ?", "tü ah-por-t ü(n) day-SEHR ?", "Will you bring a dessert?"),
                 X("Merci pour tout. — De rien.", "merh-SEE poor TOO. — duh RYA(N).", "Thanks for everything. — You're welcome.")],
                [("Je t'invite pour dîner.", "Je t'invite à dîner.", "Invitations take à + infinitive."),
                 ("Tu amènes un dessert ?", "Tu apportes un dessert ?", "Things are apportés; people are amenés.")]),
              [D("Léa", "Je t'invite à dîner vendredi.", "zhuh ta(n)-VEET ah dee-NAY vah(n)-druh-DEE.", "I'm inviting you to dinner on Friday."),
               D("Théo", "Avec plaisir. J'apporte quelque chose ?", "ah-vek play-ZEER. zhah-PORT kel-kuh SHOHZ ?", "With pleasure. Shall I bring something?"),
               D("Léa", "Un dessert, si tu veux.", "uh(n) day-SEHR, see tü VUH.", "A dessert, if you like."),
               D("Théo", "Parfait, merci pour l'invitation.", "par-FEH, merh-SEE poor la(n)-vee-tah-SYOH(N).", "Perfect, thanks for the invitation.")],
              WS("Invitation worksheet", [
                  T("Invite and answer.", ["I'm inviting you to dinner", "shall I bring something?", "a dessert"],
                    ["Je t'invite à dîner.", "J'apporte quelque chose ?", "un dessert"]),
                  T("Thank and reply.", ["thanks for everything", "you're welcome"],
                    ["Merci pour tout.", "De rien."]),
              ])),
        ]},
        {"id": "A2+-U3", "title": "Le quartier, avant et maintenant", "lessons": [
            L("Avant / maintenant : il y avait",
              "The imperfect draws the old landscape: AVANT, IL Y AVAIT …; the present draws the "
              "new one: MAINTENANT, IL Y A …; « il n'y a plus » closes the old one.",
              [V("avant", "ah-VAH(N)", "before", "adverb"),
               V("maintenant", "ma(n)-tuh-NAH(N)", "now", "adverb"),
               V("il y avait", "eel yah-VAY", "there was / were", "phrase"),
               V("la boulangerie", "lah boo-lah(n)-zhree", "bakery", "noun"),
               V("le quartier", "luh kar-TYAY", "neighbourhood", "noun")],
              G("Before and now",
                "avant, il y avait … · maintenant, il y a … · il n'y a plus …",
                "Avant, il y avait trois boulangeries ; maintenant, il n'y en a plus qu'une. The "
                "imperfect il y avait for the past, il n'y a plus for what has gone.",
                [X("Avant, il y avait une boulangerie au coin.", "ah-VAH(N), eel yah-VAY ün boo-lah(n)-zhree oh KWA(N).", "There used to be a bakery on the corner."),
                 X("Maintenant, il y a une banque.", "ma(n)-tuh-NAH(N), eel yah ün BAH(N)K.", "Now there is a bank."),
                 X("Il n'y a plus de petit commerce.", "eel nyah plü duh ptee koh-MERS.", "There is no small shop left.")],
                [("Avant, il y a eu trois boulangeries.", "Avant, il y avait trois boulangeries.", "Habitual past takes il y avait."),
                 ("Il n'y a plus de la boulangerie.", "Il n'y a plus de boulangerie.", "The negative takes de without the article.")]),
              [D("Théo", "Comment était le quartier avant ?", "koh-MAH(N) ay-TAY luh kar-TYAY ah-VAH(N) ?", "What was the neighbourhood like before?"),
               D("Voisine", "Avant, il y avait un marché et deux boulangeries.", "ah-VAH(N), eel yah-VAY uh(n) mar-SHAY ay duh boo-lah(n)-zhree.", "There used to be a market and two bakeries."),
               D("Théo", "Et maintenant ?", "ay ma(n)-tuh-NAH(N) ?", "And now?"),
               D("Voisine", "Maintenant, il y a un supermarché et il n'y a plus de boulangerie.", "ma(n)-tuh-NAH(N), eel yah ü(n) sü-per-mar-SHAY ay eel nyah plü duh boo-lah(n)-zhree.", "Now there is a supermarket and no bakery left.")],
              WS("Before-and-now worksheet", [
                  T("Draw the two pictures.", ["there used to be a bakery", "now there is a supermarket", "nothing is left"],
                    ["Avant, il y avait une boulangerie.", "Maintenant, il y a un supermarché.", "Il n'y a plus rien."]),
                  T("Describe your street.", ["what was there before?", "what is there now?"],
                    ["Avant, il y avait …", "Maintenant, il y a …"]),
              ])),
            L("Louer un appartement : le loyer, les charges",
              "Renting asks three things: C'EST LIBRE ? · C'EST COMBIEN, LE LOYER ? · LES CHARGES SONT "
              "COMPRISES ?",
              [V("le loyer", "luh lwah-YAY", "rent", "noun"),
               V("les charges", "lay SHARZH", "service charges", "noun"),
               V("compris", "koh(n)-PREE", "included", "adjective"),
               V("meublé", "muh-BLAY", "furnished", "adjective"),
               V("le bail", "luh BAHY", "lease", "noun")],
              G("Renting frame",
                "c'est libre ? · c'est combien, le loyer ? · les charges sont comprises ?",
                "L'appartement de la rue Hugo est libre ? C'est combien, le loyer ? Les charges "
                "sont comprises ? — Non, 40 euros de charges en plus, et il est meublé.",
                [X("C'est combien, le loyer ?", "say koh(n)-BYA(N), luh lwah-YAY ?", "How much is the rent?"),
                 X("Les charges sont comprises ?", "lay SHARZH so(n) koh(n)-PREEZ ?", "Are the charges included?"),
                 X("Il est meublé.", "eel ay muh-BLAY.", "It is furnished.")],
                [("Le loyer est combien d'argent ?", "C'est combien, le loyer ?", "The spoken frame puts c'est first."),
                 ("Les charges sont compris.", "Les charges sont comprises.", "charges is feminine plural.")]),
              [D("Léa", "Bonjour, l'appartement de la rue Hugo est libre ?", "boh(n)-ZHOOR, lah-par-tuh-MAH(N) duh lah RÜ ü-GOH ay LEEBR ?", "Hello, is the flat on rue Hugo free?"),
               D("Propriétaire", "Oui, depuis juillet.", "wee, duh-PWEE zhüe-YAY.", "Yes, since July."),
               D("Léa", "C'est combien, le loyer ?", "say koh(n)-BYA(N), luh lwah-YAY ?", "How much is the rent?"),
               D("Propriétaire", "Sept cents, charges comprises, et il est meublé.", "set SAH(N), SHARZH koh(n)-PREEZ, ay eel ay muh-BLAY.", "Seven hundred, charges included, and it is furnished.")],
              WS("Renting worksheet", [
                  T("Ask about the flat.", ["is it free?", "how much is the rent?", "are the charges included?"],
                    ["C'est libre ?", "C'est combien, le loyer ?", "Les charges sont comprises ?"]),
                  T("Answer as the landlord.", ["free since July", "seven hundred, furnished"],
                    ["Libre depuis juillet.", "Sept cents, meublé."]),
              ])),
            L("Raconter hier : le passé composé enchaîné",
              "Yesterday is a chain of finished events: D'ABORD J'AI …, PUIS J'AI …, ENSUITE JE SUIS …, "
              "ET ENFIN J'AI …",
              [V("hier", "YEHR", "yesterday", "adverb"),
               V("puis", "pwee", "then", "adverb"),
               V("enfin", "ah(n)-FA(N)", "finally", "adverb"),
               V("se rappeler", "suh rah-puh-LAY", "to remember", "verb"),
               V("oublier", "oo-blee-AY", "to forget", "verb")],
              G("Yesterday chain",
                "hier j'ai … · puis j'ai … · ensuite je suis … · et enfin j'ai …",
                "Hier, j'ai pris le train, puis j'ai déjeuné en ville et ensuite je suis allée au "
                "bureau. Et enfin, j'ai oublié mes clés — comme d'habitude.",
                [X("Hier, j'ai pris le train.", "yehr, zhay pree luh TRA(N).", "Yesterday I took the train."),
                 X("Puis j'ai déjeuné en ville.", "pwee zhay day-zhü-NAY ah(n) VEEL.", "Then I had lunch in town."),
                 X("Et enfin, j'ai oublié mes clés.", "ay ah(n)-FA(N), zhay oo-blee-AY may KLAY.", "And finally, I forgot my keys.")],
                [("Hier je prenais le train et je déjeunais.", "Hier j'ai pris le train et j'ai déjeuné.", "A finished chain takes the passé composé."),
                 ("J'ai oublié à prendre mes clés.", "J'ai oublié de prendre mes clés.", "oublier takes de before the infinitive.")]),
              [D("Théo", "Qu'est-ce que tu as fait hier ?", "kes-kuh tü ah FAY yehr ?", "What did you do yesterday?"),
               D("Léa", "J'ai pris le train, puis j'ai déjeuné en ville.", "zhay pree luh TRA(N), pwee zhay day-zhü-NAY ah(n) VEEL.", "I took the train, then I had lunch in town."),
               D("Théo", "Et l'après-midi ?", "ay lah-preh-muh-DEE ?", "And in the afternoon?"),
               D("Léa", "Je suis allée au bureau et j'ai oublié mes clés.", "zhuh swee zah-LAY oh bü-ROH ay zhay oo-blee-AY may KLAY.", "I went to the office and forgot my keys.")],
              WS("Story worksheet", [
                  T("Chain yesterday.", ["I took the train", "then I had lunch in town", "finally I forgot my keys"],
                    ["J'ai pris le train.", "Puis j'ai déjeuné en ville.", "Enfin, j'ai oublié mes clés."]),
                  T("Finish the story.", ["I went to the office", "I remembered the appointment"],
                    ["Je suis allé(e) au bureau.", "Je me suis rappelé le rendez-vous."]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("French daily life runs on small verbal rituals: the return with the ticket de "
                 "caisse, the phone that opens with allô, the apology that blames the traffic, and "
                 "the landlord who quotes the rent and adds charges comprises. This half-step "
                 "collects them because they are the language of a second month: a transaction, a "
                 "call, a complaint and an apology that keeps everyone friends."),
        source_url="https://en.wikipedia.org/wiki/Small_talk",
        reading=("Hier, j'ai pris le train pour aller en ville : je voulais échanger une chemise. "
                 "Dans le magasin, il y avait beaucoup de monde, mais la vendeuse a regardé le "
                 "ticket et m'a proposé une taille au-dessus. Ensuite, j'ai appelé Léa pour un "
                 "rendez-vous ; elle n'a pas répondu, elle était en réunion. Elle m'a rappelé le "
                 "soir et nous avons dîné ensemble."),
        reading_gloss=("Yesterday I took the train into town: I wanted to exchange a shirt. In the "
                       "shop there were a lot of people, but the assistant looked at the receipt "
                       "and offered me a size bigger. Then I called Léa about a meeting; she did "
                       "not answer, she was in a meeting. She called me back in the evening and we "
                       "had dinner together."),
        listening=("Théo: Allô ?<br>Léa: Bonjour, je suis bien chez Théo ?<br>"
                   "Théo: Oui, de la part de qui ?<br>Léa: De la part de Léa. Je peux laisser un message ?"),
        listening_gloss=("Théo: Hello? Léa: Hello, am I through to Théo? Théo: Yes, who is calling? "
                         "Léa: Léa. Can I leave a message?"),
        voice_tag=VOICE,
        idioms=[
            ("Pas de souci", "no worry", "no problem"),
            ("Ça marche", "it walks", "that works"),
            ("Excusez-moi du retard", "excuse me for the delay", "sorry I'm late"),
            ("Charges comprises", "charges included", "bills included"),
            ("De la part de", "on the part of", "on behalf of"),
            ("Poser un lapin", "to put a rabbit", "to stand someone up"),
            ("Faire les courses", "to do the errands", "to do the shopping"),
            ("Partager l'addition", "to share the bill", "to split the bill"),
            ("Tomber d'accord", "to fall in agreement", "to agree"),
            ("Sans engagement", "without commitment", "no strings attached"),
        ],
        mistakes=[
            ("Ici Léa, je suis bien chez vous ? (mixing two phone frames).", "Bonjour, je suis bien chez M. Brun ?", "Choose one phone frame and keep it."),
            ("Avant, il y a eu trois boulangeries.", "Avant, il y avait trois boulangeries.", "Habitual past takes il y avait."),
            ("Les charges sont compris.", "Les charges sont comprises.", "charges is feminine plural."),
        ],
        task_title="Run a whole errand in French",
        task_instructions=("Write the six French lines of a real errand you have run this month: "
                           "opening the call, stating the problem, making the request, answering the "
                           "question that comes back, fixing the time, and saying goodbye. Use the "
                           "phone frame (allô, c'est de la part de qui ?), one complaint frame (ça ne "
                           "marche pas, il manque) and one before-and-now pair (avant, il y avait … / "
                           "maintenant, il y a …)."),
    ),
    "test": [
        ("translate_en", "Say: Can you exchange it for a bigger size?", "Je voudrais l'échanger contre une taille au-dessus."),
        ("translate_fr", "Excusez-moi du retard, j'étais dans les embouteillages.", "Sorry I'm late, I was stuck in traffic."),
        ("multiple_choice", "Which is correct on the phone?", "C'est de la part de qui ?"),
        ("fill_in_the_blank", "Les charges sont ___ ?", "comprises"),
        ("word_selection", "Select the French for receipt.", "le ticket de caisse"),
        ("error_correction", "Avant, il y a eu trois boulangeries.", "Avant, il y avait trois boulangeries."),
        ("dialogue_completion", "Complete: Je peux laisser un ___ ?", "message"),
        ("matching", "Match « pas de souci » to its meaning.", "no problem"),
        ("reading_comprehension", "Pourquoi Léa n'a pas répondu ?", "she was in a meeting"),
        ("inference", "« Charges comprises » — what does it mean for the rent?", "bills are included"),
        ("main_idea", "Avant, il y avait un marché ; maintenant, il y a un supermarché. What is described?", "a change in the neighbourhood"),
        ("detail_identification", "Combien coûte le loyer ?", "seven hundred, charges included"),
    ],
}

HALFSTEPS["B1+"] = {
    "title": "French B1+ — Work and opinions",
    "native": NATIVE,
    "goals": [
        "Take part in a meeting, take the floor and write the minutes afterwards",
        "Disagree in a way the other person can accept, and concede what is true",
        "Talk about your job, your experience and a project with a deadline",
    ],
    "units": [
        {"id": "B1+-U1", "title": "Réunions et courriel", "lessons": [
            L("La réunion : l'ordre du jour et la parole",
              "Meetings move by formula: L'ORDRE DU JOUR, VOUS AVEZ LA PAROLE, ALLONS À L'ESSENTIEL, "
              "ON GARDE ÇA POUR LA PROCHAINE FOIS.",
              [V("l'ordre du jour", "lohr-druh dü ZHOOR", "the agenda", "noun"),
               V("la parole", "lah pah-ROL", "the floor (to speak)", "noun"),
               V("en suspens", "ah(n) süs-PAH(N)", "left pending", "phrase"),
               V("l'accord", "lah-KOR", "agreement", "noun"),
               V("soulever", "sool-VAY", "to raise (a point)", "verb")],
              G("Meeting language",
                "vous avez la parole · allons à l'essentiel · on garde ça en suspens · tout le monde est d'accord ?",
                "Avant de commencer, l'ordre du jour. Léa, vous avez la parole. Allons à l'essentiel. "
                "S'il n'y a pas d'objection, on garde ça en suspens.",
                [X("Léa, vous avez la parole.", "lay-AH, voo zah-VAY lah pah-ROL.", "Léa, you have the floor."),
                 X("Allons à l'essentiel.", "ah-LOH(N) zah lay-sah(n)-SYEL.", "Let's get to the point."),
                 X("On garde ça en suspens pour mardi.", "oh(n) gard sah ah(n) süs-PAH(N) poor mar-DEE.", "We'll keep that pending until Tuesday.")],
                [("Je parle maintenant parce que je veux.", "Vous avez la parole si vous voulez.", "The floor is given, not taken."),
                 ("On garde ça en suspense.", "On garde ça en suspens.", "The fixed phrase is en suspens.")]),
              [D("Chef", "On commence. Léa, vous avez la parole.", "oh(n) koh-MAH(N)S. lay-AH, voo zah-VAY lah pah-ROL.", "Let's start. Léa, you have the floor."),
               D("Léa", "Je propose de repousser le lancement de deux semaines.", "zhuh proh-POHZ duh ruh-poo-SAY luh lah(n)-suh-MAH(N) duh duh suh-MEN.", "I propose postponing the launch by two weeks."),
               D("Chef", "Quelqu'un a une objection ?", "kel-KUH(N) ah ün ob-zhek-SYOH(N) ?", "Does anyone have an objection?"),
               D("Théo", "Pas sur le fond, mais je garde le budget en suspens.", "pah sür luh FOH(N), may zhuh gard luh bü-ZHAY ah(n) süs-PAH(N).", "Not on substance, but I'll keep the budget pending.")],
              WS("Meeting worksheet", [
                  T("Use the formulas.", ["you have the floor", "let's get to the point", "kept pending"],
                    ["Vous avez la parole.", "Allons à l'essentiel.", "On garde ça en suspens."]),
                  T("Raise and park.", ["propose postponing it", "any objection?"],
                    ["Je propose de le repousser.", "Quelqu'un a une objection ?"]),
              ])),
            L("Le courriel professionnel : objet, appel, formule",
              "Business email has fixed shelves: OBJET, BONJOUR MARTIN, (semi-formal), and a close "
              "such as CORDIALEMENT or BIEN À VOUS.",
              [V("l'objet", "lob-ZHAY", "subject line", "noun"),
               V("la pièce jointe", "lah pyess ZHWA(N)KT", "attachment", "noun"),
               V("je me permets", "zhuh muh per-MEH", "I take the liberty", "phrase"),
               V("cordialement", "kor-dyal-MAH(N)", "kind regards", "adverb"),
               V("préciser", "pray-see-ZAY", "to specify", "verb")],
              G("Email frame",
                "Objet : … · je me permets de vous écrire … · je vous joins … · Cordialement",
                "Objet : Point sur le projet. Bonjour Martin, je me permets de vous écrire pour "
                "préciser le calendrier. Je vous joins le planning. Cordialement, Léa. Between "
                "colleagues the hello stays human: Bonjour Martin.",
                [X("Je me permets de vous écrire pour préciser le calendrier.", "zhuh muh per-MEH duh voo zay-KREER poor pray-see-ZAY luh kah-lah(n)-DYAY.", "I'm writing to specify the schedule."),
                 X("Je vous joins le planning.", "zhuh voo ZHWA(N) luh plah-NEENG.", "I attach the schedule."),
                 X("Cordialement,", "kor-dyal-MAH(N),", "Kind regards,")],
                [("Objet : je vous écris pour …", "Objet : Point sur le projet.", "The subject line is a nom phrase, not a sentence."),
                 ("Je joins vous le planning.", "Je vous joins le planning.", "The pronoun goes before the verb: je vous joins.")]),
              [D("Léa", "Je commence le courriel comment ?", "zhuh koh-MAH(N)S luh koo-RYEL koh-MAH(N) ?", "How do I start the email?"),
               D("Théo", "« Objet : … », puis « Bonjour Martin, je me permets de vous écrire … ».", "ob-ZHAY : …, pwee boh(n)-ZHOOR mar-TA(N), zhuh muh per-MEH duh voo zay-KREER …", "'Subject: …', then 'Hello Martin, I'm writing to …'."),
               D("Léa", "Et pour finir ?", "ay poor fee-NEER ?", "And to close?"),
               D("Théo", "« Je vous joins le planning. Cordialement. » Court et précis.", "zhuh voo ZHWA(N) luh plah-NEENG. kor-dyal-MAH(N). koor ay pray-SEE.", "'I attach the schedule. Kind regards.' Short and precise.")],
              WS("Email worksheet", [
                  T("Open the email.", ["subject: update on the project", "I'm writing to specify the schedule", "I attach the schedule"],
                    ["Objet : Point sur le projet.", "Je me permets de vous écrire pour préciser le calendrier.", "Je vous joins le planning."]),
                  T("Close the email.", ["kind regards", "best wishes"],
                    ["Cordialement,", "Bien à vous,"]),
              ])),
            L("Rédiger le compte rendu : nous avons décidé",
              "Minutes speak in the plural and the passive: NOUS AVONS DÉCIDÉ … , IL A ÉTÉ CONVENU "
              "… , RESTE EN SUSPENS …",
              [V("le compte rendu", "luh koh(n)t ruh(n)-DÜ", "the minutes", "noun"),
               V("décider", "day-see-DAY", "to decide", "verb"),
               V("convenir", "koh(n)-vuh-NEER", "to be agreed", "verb"),
               V("rester", "res-TAY", "to remain", "verb"),
               V("le délai", "luh day-LAY", "deadline", "noun")],
              G("Minutes frame",
                "nous avons décidé … · il a été convenu … · reste en suspens … · le délai est fixé à …",
                "Nous avons décidé de repousser le lancement. Il a été convenu que Léa coordonne le "
                "projet. Le délai est fixé au 30 juin ; le budget reste en suspens.",
                [X("Nous avons décidé de repousser le lancement.", "noo zah-VOH(N) day-see-DAY duh ruh-poo-SAY luh lah(n)-suh-MAH(N).", "We decided to postpone the launch."),
                 X("Il a été convenu que Léa coordonne le projet.", "eel ah ay-TAY koh(n)-vuh-NÜ kuh lay-AH koh-or-deen luh proh-ZHAY.", "It was agreed that Léa coordinates the project."),
                 X("Le délai est fixé au 30 juin.", "luh day-LAY ay fee-KSAY oh TRAH(N)T zhüa(N).", "The deadline is set for 30 June.")],
                [("On a décidé de, voilà, enfin bref.", "Nous avons décidé de repousser le lancement.", "Minutes state decisions without fillers."),
                 ("On a été convenu que Léa coordonne le projet.", "Il a été convenu que Léa coordonne le projet.", "convenir in minutes is impersonal: il a été convenu que …, never on a été convenu.")]),
              [D("Théo", "Tu rédiges le compte rendu ?", "tü ray-ZHEEZH luh koh(n)t ruh(n)-DÜ ?", "Are you writing the minutes?"),
               D("Léa", "Oui : « nous avons décidé », « il a été convenu », « reste en suspens ».", "wee : noo zah-VOH(N) day-see-DAY, eel ah ay-TAY koh(n)-vuh-NÜ, rest ah(n) süs-PAH(N).", "Yes: 'we decided', 'it was agreed', 'remains pending'."),
               D("Théo", "Et le délai ?", "ay luh day-LAY ?", "And the deadline?"),
               D("Léa", "« Le délai est fixé au 30 juin. »", "luh day-LAY ay fee-KSAY oh TRAH(N)T zhüa(N).", "'The deadline is set for 30 June.'")],
              WS("Minutes worksheet", [
                  T("Write the decisions.", ["we decided to postpone the launch", "it was agreed that Léa coordinates", "the deadline is set for 30 June"],
                    ["Nous avons décidé de repousser le lancement.", "Il a été convenu que Léa coordonne.", "Le délai est fixé au 30 juin."]),
                  T("Note what is open.", ["the budget remains pending", "we decide on Tuesday"],
                    ["Le budget reste en suspens.", "On décide mardi."]),
              ])),
        ]},
        {"id": "B1+-U2", "title": "Des opinions qui se font écouter", "lessons": [
            L("Je comprends votre position, mais…",
              "A disagreement that lands starts with the part that is true: JE COMPRENDS VOTRE "
              "POSITION ET, DANS UNE CERTAINE MESURE, JE LA PARTAGE ; CELA ÉTANT, …",
              [V("la position", "lah poh-zee-SYOH(N)", "position, stance", "noun"),
               V("dans une certaine mesure", "dah(n) zün ser-TEN muh-ZÜR", "to some extent", "phrase"),
               V("cela étant", "suh-LAH ay-TAH(N)", "that being so", "phrase"),
               V("nuancer", "nü-ah(n)-SAY", "to qualify", "verb"),
               V("la nuance", "lah nü-AH(N)S", "nuance", "noun")],
              G("Concede, then qualify",
                "je comprends votre position · dans une certaine mesure · cela étant · la nuance est que …",
                "Je comprends votre position et, dans une certaine mesure, je la partage. Cela "
                "étant, le coût change la donne. Concession first; the objection walks in behind "
                "it.",
                [X("Je comprends votre position.", "zhuh koh(n)-prah(n) votr poh-zee-SYOH(N).", "I understand your position."),
                 X("Dans une certaine mesure, je la partage.", "dah(n) zün ser-TEN muh-ZÜR, zhuh lah par-TAZH.", "To some extent I share it."),
                 X("Cela étant, le coût change la donne.", "suh-LAH ay-TAH(N), luh KOO shah(n)ZH lah DON.", "That being so, the cost changes things.")],
                [("Vous avez tort, c'est tout.", "Je comprends votre position, mais il y a une nuance.", "A concession keeps the argument alive."),
                 ("Je suis d'accord en tout, mais non.", "Dans une certaine mesure, je suis d'accord.", "One position per sentence.")]),
              [D("Théo", "Je pense qu'il faut lancer le produit maintenant.", "zhuh PAH(N)S keel foh lah(n)-SAY luh proh-DÜ(H) ma(n)-tuh-NAH(N).", "I think we should launch the product now."),
               D("Léa", "Je comprends ta position et, dans une certaine mesure, je la partage.", "zhuh koh(n)-prah(n) tah poh-zee-SYOH(N) ay, dah(n) zün ser-TEN muh-ZÜR, zhuh lah par-TAZH.", "I understand your position and, to some extent, I share it."),
               D("Théo", "Mais ?", "may ?", "But?"),
               D("Léa", "Cela étant, le budget n'est pas validé. C'est là la nuance.", "suh-LAH ay-TAH(N), luh bü-ZHAY nay pah vah-lee-DAY. say lah lah nü-AH(N)S.", "That being so, the budget is not approved. That's the nuance.")],
              WS("Agreement worksheet", [
                  T("Concede, then qualify.", ["I understand your position", "to some extent I share it", "that being so, there is a nuance"],
                    ["Je comprends votre position.", "Dans une certaine mesure, je la partage.", "Cela étant, il y a une nuance."]),
                  T("Name the real obstacle.", ["the budget is not approved", "we need more data"],
                    ["Le budget n'est pas validé.", "Il nous faut plus de données."]),
              ])),
            L("Convaincre : si on fait ceci, il arrive cela",
              "Persuasion uses a real condition plus a consequence: SI ON AUGMENTE LE PRIX, ON PERD "
              "DES CLIENTS ; and a recommendation: IL VAUDRAIT MIEUX ATTENDRE.",
              [V("convaincre", "koh(n)-VA(N)KR", "to convince", "verb"),
               V("perdre", "PERDR", "to lose", "verb"),
               V("le risque", "luh REESK", "risk", "noun"),
               V("il vaudrait mieux", "eel voh-DREH MYUH", "it would be better", "phrase"),
               V("d'ici là", "dee-SEE LAH", "by then", "phrase")],
              G("Real condition and recommendation",
                "si + présent, + présent/futur · il vaudrait mieux + infinitif · à condition de + infinitif",
                "Si on augmente le prix maintenant, on perd des clients. Il vaudrait mieux attendre "
                "l'automne, à condition de fixer une date dès maintenant. The condition states the "
                "mechanism; the recommendation offers the exit.",
                [X("Si on augmente le prix, on perd des clients.", "see oh(n) nohg-mah(n)T luh PREE, oh(n) PER day kly-AH(N).", "If we raise the price, we lose customers."),
                 X("Il vaudrait mieux attendre l'automne.", "eel voh-DREH MYUH ah-TAH(N)DR loh-TON.", "It would be better to wait until autumn."),
                 X("À condition de fixer une date dès maintenant.", "ah koh(n)-dee-SYOH(N) duh fee-KSAY ün DAT day ma(n)-tuh-NAH(N).", "Provided we set a date right now.")],
                [("Si on augmenterait le prix, on perd des clients.", "Si on augmente le prix, on perd des clients.", "A real condition takes the present indicative."),
                 ("Il vaut mieux qu'attendre.", "Il vaudrait mieux attendre.", "The recommendation takes the infinitive, not que.")]),
              [D("Théo", "Si on augmente le prix maintenant, on perd des clients.", "see oh(n) nohg-mah(n)T luh PREE ma(n)-tuh-NAH(N), oh(n) PER day kly-AH(N).", "If we raise the price now, we lose customers."),
               D("Léa", "Que proposes-tu ?", "kuh proh-POHZ tü ?", "What do you propose?"),
               D("Théo", "Il vaudrait mieux attendre l'automne.", "eel voh-DREH MYUH ah-TAH(N)DR loh-TON.", "It would be better to wait until autumn."),
               D("Léa", "D'accord, à condition de fixer une date dès maintenant.", "dah-KOR, ah koh(n)-dee-SYOH(N) duh fee-KSAY ün DAT day ma(n)-tuh-NAH(N).", "Agreed, provided we set a date right now.")],
              WS("Persuasion worksheet", [
                  T("State the mechanism.", ["if we raise the price, we lose customers", "if we wait, we lose the season"],
                    ["Si on augmente le prix, on perd des clients.", "Si on attend, on perd la saison."]),
                  T("Recommend.", ["it would be better to wait until autumn", "provided we set a date"],
                    ["Il vaudrait mieux attendre l'automne.", "à condition de fixer une date"]),
              ])),
            L("Le désaccord sans conflit : je ne peux pas l'accepter en l'état",
              "The soft refusal names the disagreement and the shared goal in one breath: JE NE PEUX "
              "PAS L'ACCEPTER EN L'ÉTAT, MÊME SI JE PARTAGE L'OBJECTIF.",
              [V("accepter", "ak-sep-TAY", "to accept", "verb"),
               V("en l'état", "ah(n) lay-TAY", "as it stands", "phrase"),
               V("l'objectif", "lob-zhek-TEEF", "objective", "noun"),
               V("partager", "par-tah-ZHAY", "to share", "verb"),
               V("revoir", "ruh-VWAR", "to review", "verb")],
              G("Soft refusal",
                "je ne peux pas l'accepter en l'état · même si je partage l'objectif · on le revoit ?",
                "Je ne peux pas l'accepter en l'état, même si je partage l'objectif. On le revoit "
                "avec les chiffres sous les yeux ? The refusal targets the proposal, not the "
                "person.",
                [X("Je ne peux pas l'accepter en l'état.", "zhuh nuh puh pah lak-sep-TAY ah(n) lay-TAY.", "I cannot accept it as it stands."),
                 X("Je partage l'objectif, pas la méthode.", "zhuh par-TAZH lob-zhek-TEEF, pah lah may-TOD.", "I share the objective, not the method."),
                 X("On le revoit avec les chiffres ?", "oh(n) luh ruh-VWAH ah-vek lay SHEEFR ?", "Shall we review it with the figures?")],
                [("Non, c'est absurde.", "Je ne peux pas l'accepter en l'état ; revoyons-le.", "Attack the proposal, never the person."),
                 ("Je partage l'objectif et la méthode (when you disagree).", "Je partage l'objectif, pas la méthode.", "Precision is the politeness.")]),
              [D("Léa", "On signe le contrat cette semaine ?", "oh(n) SEENY luh koh(n)-TRAH set suh-MEN ?", "Shall we sign the contract this week?"),
               D("Théo", "Je ne peux pas l'accepter en l'état, même si je partage l'objectif.", "zhuh nuh puh pah lak-sep-TAY ah(n) lay-TAY, mem see zhuh par-TAZH lob-zhek-TEEF.", "I cannot accept it as it stands, even if I share the objective."),
               D("Léa", "Qu'est-ce qui te manque ?", "kes-kee tuh MAH(N)K ?", "What is missing for you?"),
               D("Théo", "Les chiffres du trimestre. On le revoit lundi ?", "lay SHEEFR dü tree-MEHSTR. oh(n) luh ruh-VWAH lu(n)-DEE ?", "The quarter's figures. Shall we review it on Monday?")],
              WS("Disagreement worksheet", [
                  T("Refuse the proposal, keep the goal.", ["I cannot accept it as it stands", "I share the objective, not the method"],
                    ["Je ne peux pas l'accepter en l'état.", "Je partage l'objectif, pas la méthode."]),
                  T("Offer the next step.", ["shall we review it with the figures?", "what is missing for you?"],
                    ["On le revoit avec les chiffres ?", "Qu'est-ce qui te manque ?"]),
              ])),
        ]},
        {"id": "B1+-U3", "title": "Travail, expérience et projets", "lessons": [
            L("L'offre et le CV : exigences et expérience",
              "Job adverts list requirements: MAÎTRISE REQUISE (required command), EXPÉRIENCE "
              "CONFIRMÉE, PRISE DE POSTE IMMÉDIATE.",
              [V("l'exigence", "lek-zee-ZHAH(N)S", "requirement", "noun"),
               V("la maîtrise", "lah may-TREEZ", "command, proficiency", "noun"),
               V("exigé", "ek-zee-ZHAY", "required", "adjective"),
               V("la prise de poste", "lah preez duh POST", "start date", "noun"),
               V("l'atout", "lah-TOO", "asset", "noun")],
              G("Requirements frame",
                "maîtrise de l'anglais exigée · expérience confirmée · prise de poste immédiate",
                "Maîtrise de l'anglais exigée ; expérience confirmée en relation client ; prise de "
                "poste immédiate. The advert is a list of nouns and the answer should be as "
                "concrete as the list.",
                [X("Maîtrise de l'anglais exigée.", "may-TREEZ duh lah(n)-GLEH ek-zee-ZHAY.", "Command of English required."),
                 X("Expérience confirmée en relation client.", "ek-speh-RYAH(N)S koh(n)-feer-MAY ah(n) ruh-lah-SYOH(N) KLYAH(N).", "Confirmed experience in client relations."),
                 X("Prise de poste immédiate.", "preez duh POST ee-may-DYAHT.", "Immediate start.")],
                [("Je maîtrise l'anglais trois ans.", "J'ai trois ans d'expérience en anglais.", "The advert asks for experience; give a duration."),
                 ("Relation client : beaucoup.", "Relation client : cinq ans.", "A figure beats an adverb.")]),
              [D("Théo", "Qu'est-ce qu'ils demandent exactement ?", "kes-kee eel duh-MAH(N)D ek-zak-tuh-MAH(N) ?", "What exactly are they asking for?"),
               D("Léa", "Maîtrise de l'anglais exigée et expérience confirmée.", "may-TREEZ duh lah(n)-GLEH ek-zee-ZHAY ay ek-speh-RYAH(N)S koh(n)-feer-MAY.", "Command of English required and confirmed experience."),
               D("Théo", "Mets ça en première ligne de ton CV.", "meh sah ah(n) pruh-MYAYR LEEY(N) duh toh say-VAY.", "Put that on the first line of your CV."),
               D("Léa", "Avec cinq ans en relation client : c'est l'atout principal.", "ah-vek sa(n)K AH(N) ah(n) ruh-lah-SYOH(N) KLYAH(N) : say lah-TOO pra(n)-see-PAL.", "With five years in client relations: that is the main asset.")],
              WS("Job-advert worksheet", [
                  T("Read the advert.", ["English required", "confirmed experience", "immediate start"],
                    ["Maîtrise de l'anglais exigée.", "Expérience confirmée.", "Prise de poste immédiate."]),
                  T("Answer with your record.", ["five years in client relations", "I can start in July"],
                    ["Cinq ans en relation client.", "Je peux commencer en juillet."]),
              ])),
            L("L'entretien : ça fait trois ans que je travaille",
              "Experience is spoken with ÇA FAIT + durée + QUE + présent. The strengths come next: MON "
              "POINT FORT, MON DÉFI.",
              [V("ça fait … que", "sah feh … kuh", "it has been … that", "phrase"),
               V("le point fort", "luh pwa(n) FOR", "strength", "noun"),
               V("le défi", "luh day-FEE", "challenge", "noun"),
               V("l'équipe", "lay-KEEP", "team", "noun"),
               V("gérer", "zhay-RAY", "to manage", "verb")],
              G("Experience frame",
                "ça fait + durée + que + présent · mon point fort est … · mon défi a été de …",
                "Ça fait trois ans que je travaille en logistique et je gère les tournées. Mon "
                "point fort, c'est le détail ; mon défi a été d'apprendre à déléguer.",
                [X("Ça fait trois ans que je travaille en logistique.", "sah feh trwah ZAH(N) kuh zhuh trah-VAHY ah(n) loh-zhees-TEEK.", "I have been working in logistics for three years."),
                 X("Mon point fort, c'est le détail.", "moh(n) pwa(n) FOR, say luh day-TAHY.", "My strength is attention to detail."),
                 X("Mon défi a été d'apprendre à déléguer.", "moh(n) day-FEE ah ay-TAY dah-PRAH(N)DR ah day-lay-GAY.", "My challenge was learning to delegate.")],
                [("Je travaille ici depuis trois ans (in speech).", "Ça fait trois ans que je travaille ici.", "Spoken French prefers the ça fait frame."),
                 ("Mon point fort est je suis patient.", "Mon point fort, c'est la patience.", "A strength is a noun, not a clause.")]),
              [D("Recruteuse", "Quelle est votre expérience ?", "kel ay votr ek-speh-RYAH(N)S ?", "What is your experience?"),
               D("Théo", "Ça fait trois ans que je travaille en logistique.", "sah feh trwah ZAH(N) kuh zhuh trah-VAHY ah(n) loh-zhees-TEEK.", "I have been working in logistics for three years."),
               D("Recruteuse", "Et votre point fort ?", "ay votr pwa(n) FOR ?", "And your strength?"),
               D("Théo", "Le détail. Mon défi a été d'apprendre à déléguer.", "luh day-TAHY. moh(n) day-FEE ah ay-TAY dah-PRAH(N)DR ah day-lay-GAY.", "Detail. My challenge was learning to delegate.")],
              WS("Interview worksheet", [
                  T("State your experience.", ["three years in logistics", "I manage the rounds"],
                    ["Ça fait trois ans que je travaille en logistique.", "Je gère les tournées."]),
                  T("Name strength and challenge.", ["attention to detail", "learning to delegate"],
                    ["Mon point fort, c'est le détail.", "Mon défi a été d'apprendre à déléguer."]),
              ])),
            L("Parler d'un projet : objectif, échéance, risque",
              "Projects are described as a goal plus a deadline plus a risk: L'OBJECTIF EST DE … , "
              "L'ÉCHÉANCE EST FIXÉE AU … , LE RISQUE PRINCIPAL EST …",
              [V("l'objectif", "lob-zhek-TEEF", "goal", "noun"),
               V("l'échéance", "lay-shay-AH(N)S", "deadline", "noun"),
               V("le jalon", "luh zhah-LOH(N)", "milestone", "noun"),
               V("le risque", "luh REESK", "risk", "noun"),
               V("l'ancien système", "lah(n)-SYA(N) sees-TEM", "the old system", "noun")],
              G("Project frame",
                "l'objectif est de … · l'échéance est fixée au … · le premier jalon est …",
                "L'objectif est de numériser les commandes ; l'échéance est fixée au 30 novembre ; "
                "le premier jalon est un test en septembre. Goal, date, milestone — in that order.",
                [X("L'objectif est de numériser les commandes.", "lob-zhek-TEEF ay duh nü-may-ree-ZAY lay koh-MAH(N)D.", "The goal is to digitalise orders."),
                 X("L'échéance est fixée au 30 novembre.", "lay-shay-AH(N)S ay fee-KSAY oh TRAH(N)T noh-VAH(N)BR.", "The deadline is set for 30 November."),
                 X("Le premier jalon est un test en septembre.", "luh pruh-MYAY zhah-LOH(N) ay tü(n) TEST ah(n) sep-TAH(N)BR.", "The first milestone is a test in September.")],
                [("L'objectif est que nous numérisons.", "L'objectif est de numériser les commandes.", "A goal takes the infinitive."),
                 ("L'échéance est fixée à 30 novembre.", "L'échéance est fixée au 30 novembre.", "A date takes au (à + le): au 30 novembre, not bare à.")]),
              [D("Léa", "Quel est l'objectif du projet ?", "kel ay lob-zhek-TEEF dü proh-ZHAY ?", "What is the project goal?"),
               D("Théo", "Numériser les commandes avant novembre.", "nü-may-ree-ZAY lay koh-MAH(N)D ah-VAH(N) noh-VAH(N)BR.", "To digitalise orders before November."),
               D("Léa", "Et le plus grand risque ?", "ay luh plü grah(n) REESK ?", "And the biggest risk?"),
               D("Théo", "L'ancien système. C'est pourquoi le premier jalon est un test.", "lah(n)-SYA(N) sees-TEM. say poor-KWAH luh pruh-MYAY zhah-LOH(N) ay tü(n) TEST.", "The old system. That is why the first milestone is a test.")],
              WS("Project worksheet", [
                  T("Describe the project.", ["the goal is to digitalise the orders", "the deadline is 30 November", "the biggest risk"],
                    ["L'objectif est de numériser les commandes.", "L'échéance est fixée au 30 novembre.", "Le risque principal est …"]),
                  T("Name the milestone.", ["the first milestone is a test", "we take on the integration"],
                    ["Le premier jalon est un test.", "Nous prenons en charge l'intégration."]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("French working life leans on fixed verbal machinery — vous avez la parole, allons "
                 "à l'essentiel, cela étant, cordialement, nous avons décidé — and a learner who "
                 "owns the machinery sounds senior long before the grammar is perfect. This "
                 "half-step drills the machinery of meetings, email, negotiation and the interview, "
                 "because in French offices the formulas are not empty: they are how a disagreement "
                 "stays professional."),
        source_url="https://en.wikipedia.org/wiki/Meeting",
        reading=("À la réunion de mardi, nous avons décidé de repousser le lancement de deux "
                 "semaines. Léa a soulevé le risque budgétaire et l'équipe a préféré attendre "
                 "l'automne. Le budget reste en suspens. Ensuite, Léa a rédigé le compte rendu en "
                 "vingt minutes : nous avons décidé, il a été convenu, reste en suspens — avec des "
                 "verbes, pas des adjectifs."),
        reading_gloss=("At Tuesday's meeting we decided to postpone the launch by two weeks. Léa "
                       "raised the budget risk and the team preferred to wait until autumn. The "
                       "budget remains pending. Afterwards Léa wrote the minutes in twenty minutes: "
                       "we decided, it was agreed, remains pending — with verbs, not adjectives."),
        listening=("Théo: Je comprends ta position, mais je ne peux pas l'accepter en l'état.<br>"
                   "Léa: Qu'est-ce qui te manque ?<br>Théo: Les chiffres du trimestre. On le revoit lundi ?<br>"
                   "Léa: D'accord, lundi."),
        listening_gloss=("Théo: I understand your position, but I cannot accept it as it stands. "
                         "Léa: What is missing for you? Théo: The quarter's figures. Shall we review "
                         "it on Monday? Léa: Agreed, Monday."),
        voice_tag=VOICE,
        idioms=[
            ("Allons à l'essentiel", "let's go to the essential", "let's get to the point"),
            ("Vous avez la parole", "you have the word", "the floor is yours"),
            ("En suspens", "in suspense", "still outstanding"),
            ("Être d'accord", "to be in agreement", "to agree"),
            ("Se mettre au travail", "to put oneself to work", "to get down to work"),
            ("Mener de front", "to lead side by side", "to juggle several things"),
            ("Tirer les ficelles", "to pull the strings", "to pull the strings"),
            ("Cordialement", "cordially", "kind regards"),
            ("Dans les meilleurs délais", "in the best delays", "as soon as possible"),
            ("Au pied levé", "at the lifted foot", "at a moment's notice"),
        ],
        mistakes=[
            ("Je travaille ici depuis trois ans (in speech).", "Ça fait trois ans que je travaille ici.", "Spoken French prefers the ça fait frame."),
            ("Si on augmenterait le prix, on perd des clients.", "Si on augmente le prix, on perd des clients.", "A real condition takes the present indicative."),
            ("L'objectif est que nous numérisons.", "L'objectif est de numériser les commandes.", "Goals take the infinitive."),
        ],
        task_title="Hold a five-line negotiation in French",
        task_instructions=("Write the five moves of a disagreement you might actually have at work: "
                           "open with the part you accept, give the qualification (dans une certaine "
                           "mesure … cela étant), state the real obstacle with a verb, make a "
                           "recommendation with il vaudrait mieux, and close by fixing the next step "
                           "and its date. Then rewrite the same five lines as the minutes — nous "
                           "avons décidé, il a été convenu, reste en suspens."),
    ),
    "test": [
        ("translate_en", "Say: You have the floor.", "Vous avez la parole."),
        ("translate_fr", "Je comprends votre position, mais il y a une nuance.", "I understand your position, but there is a nuance."),
        ("multiple_choice", "Which closes a professional email?", "Cordialement,"),
        ("fill_in_the_blank", "Il vaudrait mieux ___ l'automne.", "attendre"),
        ("word_selection", "Select the French for the minutes.", "le compte rendu"),
        ("error_correction", "Si on augmenterait le prix, on perd des clients.", "Si on augmente le prix, on perd des clients."),
        ("dialogue_completion", "Complete: Quelqu'un a une ___ ?", "objection"),
        ("matching", "Match « en suspens » to its meaning.", "still outstanding"),
        ("reading_comprehension", "Qu'a décidé l'équipe au sujet du lancement ?", "to postpone it two weeks"),
        ("inference", "« Je partage l'objectif, pas la méthode » — what is being refused?", "the proposal, not the person"),
        ("main_idea", "L'objectif est de numériser les commandes. What is stated?", "the project goal"),
        ("detail_identification", "Quelle est l'échéance ?", "30 November"),
    ],
}

HALFSTEPS["B2+"] = {
    "title": "French B2+ — Argument and formal register",
    "native": NATIVE,
    "goals": [
        "Argue with figures: proportions, rises and falls, and the frame that reads them",
        "Write a formal letter and a formal complaint: facts, grounds, request",
        "Cite, reformulate and close a text without repeating yourself",
    ],
    "units": [
        {"id": "B2+-U1", "title": "Argumenter avec des chiffres", "lessons": [
            L("Un tiers, le double, en hausse de 4 %",
              "Statistics are spoken with proportions and verbs of change: UN TIERS DE (a third of), "
              "LE DOUBLE DE, ENVIRON (around), EN HAUSSE DE 4 %.",
              [V("un tiers", "uh(n) TYAIR", "a third", "numeral"),
               V("le double de", "luh DOOBL duh", "twice as much as", "phrase"),
               V("environ", "ah(n)-vee-ROH(N)", "around", "adverb"),
               V("en hausse de", "ah(n) OHS duh", "up by", "phrase"),
               V("reculer", "ruh-kü-LAY", "to fall back", "verb")],
              G("Figures frame",
                "un tiers de … · le double de … · en hausse de 4 % · en baisse de …",
                "Un tiers des ménages a un chien. Les dépenses ont augmenté de quatre pour cent et "
                "la consommation a légèrement reculé. The figure carries the sentence; the verb "
                "gives the direction.",
                [X("Un tiers des ménages a un chien.", "uh(n) TYAIR day may-NAZH ah uh(n) SHAY(N).", "A third of households have a dog."),
                 X("Les dépenses ont augmenté de quatre pour cent.", "lay day-PAH(N)S o(n) tohg-mah(n)-TAY duh katr poor SAH(N).", "Spending rose by four per cent."),
                 X("La consommation a légèrement reculé.", "lah koh(n)-soh-mah-SYOH(N) ah lay-zhayr-MAH(N) ruh-kü-LAY.", "Consumption fell slightly.")],
                [("Ça a augmenté quatre pour cent.", "Les dépenses ont augmenté de quatre pour cent.", "A change takes de before the amount."),
                 ("Le double des ménages.", "Le double de ménages.", "The proportion takes de.")]),
              [D("Léa", "Combien de gens prennent le bus ?", "koh(n)-BYA(N) duh ZHAH(N) pren luh BÜS ?", "How many people take the bus?"),
               D("Analyste", "Environ un tiers de la ville.", "ah(n)-vee-ROH(N) uh(n) TYAIR duh lah VEEL.", "Around a third of the city."),
               D("Léa", "Et ça a changé ?", "ay sah ah shah(n)-ZHAY ?", "And has it changed?"),
               D("Analyste", "L'usage a augmenté de quatre pour cent ; la voiture a légèrement reculé.", "lü-ZAZH ah tohg-mah(n)-TAY duh katr poor SAH(N) ; lah vwah-TÜR ah lay-zhayr-MAH(N) ruh-kü-LAY.", "Use rose by four per cent; car use fell slightly.")],
              WS("Figures worksheet", [
                  T("Say it with figures.", ["a third of households", "twice as many", "around thirty people"],
                    ["un tiers des ménages", "le double de", "environ trente personnes"]),
                  T("Report the change.", ["spending rose by 4%", "consumption fell slightly"],
                    ["Les dépenses ont augmenté de 4 %.", "La consommation a légèrement reculé."]),
              ])),
            L("Enchaîner : non seulement …, mais encore …",
              "Argument stacks evidence with NON SEULEMENT … , MAIS ENCORE … and tops it with "
              "QUI PLUS EST (what is more).",
              [V("non seulement", "noh(n) suhl-MAH(N)", "not only", "phrase"),
               V("mais encore", "may zah(n)-KOR", "but also", "phrase"),
               V("qui plus est", "kee plü ZAY", "what is more", "phrase"),
               V("ajouter", "ah-zhoo-TAY", "to add", "verb"),
               V("dans la même veine", "dah(n) lah mem VEN", "along the same lines", "phrase")],
              G("Stacking evidence",
                "non seulement … , mais encore … · qui plus est … · dans la même veine …",
                "Non seulement le prix a augmenté, mais encore la qualité a baissé. Qui plus est, "
                "le délai a doublé. Three escalations, one argument.",
                [X("Non seulement le prix a augmenté, mais encore la qualité a baissé.", "noh(n) suhl-MAH(N) luh PREE ah tohg-mah(n)-TAY, may zah(n)-KOR lah kah-lee-TAY ah bay-SAY.", "Not only did the price rise, but the quality also fell."),
                 X("Qui plus est, le délai a doublé.", "kee plü ZAY, luh day-LAY ah doo-BLAY.", "What is more, the deadline doubled."),
                 X("Dans la même veine, le service a changé.", "dah(n) lah mem VEN, luh sehr-VEES ah shah(n)-ZHAY.", "Along the same lines, the service changed.")],
                [("Non seulement le prix a augmenté, mais la qualité aussi a baissé.", "Non seulement le prix a augmenté, mais encore la qualité a baissé.", "The fixed pair is non seulement … mais encore."),
                 ("Qui plus est que le délai.", "Qui plus est, le délai a doublé.", "Qui plus est opens a clause.")]),
              [D("Théo", "Comment le dire sans exagérer ?", "koh-MAH(N) luh DEER sah(n) zek-zah-ZHAY ?", "How do I say it without exaggerating?"),
               D("Léa", "Enchaîne : non seulement …, mais encore …", "ah(n)-SHEN : noh(n) suhl-MAH(N) …, may zah(n)-KOR …", "Chain it: not only …, but also …"),
               D("Théo", "« Non seulement le prix a augmenté, mais encore la qualité a baissé. »", "noh(n) suhl-MAH(N) luh PREE ah tohg-mah(n)-TAY, may zah(n)-KOR lah kah-lee-TAY ah bay-SAY.", "'Not only did the price rise, but the quality also fell.'"),
               D("Léa", "Et pour finir : « qui plus est, le délai a doublé ».", "ay poor fee-NEER : kee plü ZAY, luh day-LAY ah doo-BLAY.", "And to finish: 'what is more, the deadline doubled'.")],
              WS("Argument-chain worksheet", [
                  T("Stack the evidence.", ["not only did the price rise, but the quality also fell", "what is more, the deadline doubled"],
                    ["Non seulement le prix a augmenté, mais encore la qualité a baissé.", "Qui plus est, le délai a doublé."]),
                  T("Add along the same lines.", ["along the same lines", "I would add one more fact"],
                    ["Dans la même veine, …", "J'ajouterais un fait de plus."]),
              ])),
            L("Concéder pour l'emporter : certes …, encore faut-il …",
              "The advanced concession is a two-storey sentence: CERTES … (admittedly), ENCORE "
              "FAUT-IL … (but it still takes …). It grants the fact and keeps the conclusion.",
              [V("certes", "SERT", "admittedly", "adverb"),
               V("encore faut-il", "ah(n)-KOR foh-TEEL", "it still takes", "phrase"),
               V("à supposer que", "ah sü-poh-ZAY kuh", "assuming that", "phrase"),
               V("d'ailleurs", "dah-YUHR", "besides", "adverb"),
               V("la réserve", "lah ray-ZERV", "reservation, caveat", "noun")],
              G("Two-storey concession",
                "certes … , encore faut-il … · à supposer que + subjonctif · avec une réserve",
                "Certes, la mesure réduit les coûts ; encore faut-il que les équipes suivent. À "
                "supposer que le calendrier tienne, l'effet serait visible en mars. The first "
                "clause pays; the second collects.",
                [X("Certes, la mesure réduit les coûts.", "SERT, lah muh-ZÜR ray-DÜEE lay KOO.", "Admittedly, the measure reduces costs."),
                 X("Encore faut-il que les équipes suivent.", "ah(n)-KOR foh-TEEL kuh lay zay-KEEP SÜEV.", "It still takes the teams following."),
                 X("À supposer que le calendrier tienne, l'effet serait visible en mars.", "ah sü-poh-ZAY kuh luh kah-lah(n)-DYAY TYEN, lay-FAY suh-RAY vee-ZEEBL ah(n) MARS.", "Assuming the schedule holds, the effect would show in March.")],
                [("Certes la mesure réduit les coûts, mais encore il faut du temps.", "Certes, la mesure réduit les coûts ; encore faut-il du temps.", "Do not stack mais before encore faut-il."),
                 ("À supposer que le calendrier tient.", "À supposer que le calendrier tienne.", "à supposer que takes the subjunctive.")]),
              [D("Chef", "Vous recommandez la mesure ?", "voo ruh-koh-mah(n)-DAY lah muh-ZÜR ?", "Do you recommend the measure?"),
               D("Analyste", "Certes, elle réduit les coûts ; encore faut-il que les équipes suivent.", "SERT, el ray-DÜEE lay KOO ; ah(n)-KOR foh-TEEL kuh lay zay-KEEP SÜEV.", "Admittedly it reduces costs; it still takes the teams following."),
               D("Chef", "Donc ?", "doh(n)K ?", "So?"),
               D("Analyste", "Je la recommande avec une réserve : un point d'étape en mars.", "zhuh lah ruh-koh-MAH(N)D ah-vek ün ray-ZERV : uh(n) pwa(n) day-TAP ah(n) MARS.", "I recommend it with one caveat: a checkpoint in March.")],
              WS("Concession worksheet", [
                  T("Build the two-storey sentence.", ["admittedly it reduces costs, but the teams must follow", "assuming the schedule holds, the effect shows in March"],
                    ["Certes, elle réduit les coûts ; encore faut-il que les équipes suivent.", "À supposer que le calendrier tienne, l'effet serait visible en mars."]),
                  T("Qualify the recommendation.", ["with one caveat", "a checkpoint in March"],
                    ["avec une réserve", "un point d'étape en mars"]),
              ])),
        ]},
        {"id": "B2+-U2", "title": "Lettres et réclamations formelles", "lessons": [
            L("La lettre formelle : je soussigné, je vous saurais gré",
              "Administrative French runs on set formulas: JE SOUSSIGNÉ … (I, the undersigned), JE "
              "VOUS SAURAIS GRÉ DE … (I would be grateful if you would), JE VOUS PRIE DE …",
              [V("je soussigné", "zhuh soo-see-NYAY", "I, the undersigned", "phrase"),
               V("je vous saurais gré", "zhuh voo soh-REH GRAY", "I would be grateful", "phrase"),
               V("la demande", "lah duh-MAH(N)D", "request", "noun"),
               V("l'objet", "lob-ZHAY", "subject", "noun"),
               V("le dossier", "luh doh-SYAY", "file, case", "noun")],
              G("Formal letter formulas",
                "Je soussigné … · je vous saurais gré de bien vouloir … · je vous prie de …",
                "Je soussigné Léa Martin, demeurant à Lyon, ai l'honneur de solliciter un examen de "
                "mon dossier. Je vous saurais gré de bien vouloir m'indiquer la suite donnée. Note "
                "the infinitive after de bien vouloir.",
                [X("Je soussigné Léa Martin ai l'honneur de solliciter …", "zhuh soo-see-NYAY lay-AH mar-TA(N) ay loh-NUHR duh soh-lee-see-TAY …", "I, the undersigned Léa Martin, have the honour to request …"),
                 X("Je vous saurais gré de bien vouloir m'indiquer la suite.", "zhuh voo soh-REH GRAY duh bya(n) voo-LWAR ma(n)-dee-KAY lah SWEET.", "I would be grateful if you would tell me what happens next."),
                 X("Je vous prie de bien vouloir accuser réception.", "zhuh voo PREE duh bya(n) voo-LWAR ah-kü-ZAY ray-sep-SYOH(N).", "I request that you acknowledge receipt.")],
                [("Je veux que vous me répondez.", "Je vous prie de bien vouloir me répondre.", "The formula takes faire-style infinitives: de bien vouloir."),
                 ("Je vous saurais gré pour m'indiquer …", "Je vous saurais gré de bien vouloir m'indiquer …", "The formula is de bien vouloir + infinitive.")]),
              [D("Léa", "Comment j'écris la demande ?", "koh-MAH(N) zhek-REES lah duh-MAH(N)D ?", "How do I write the request?"),
               D("Théo", "« Je vous saurais gré de bien vouloir m'indiquer la suite donnée. »", "zhuh voo soh-REH GRAY duh bya(n) voo-LWAR ma(n)-dee-KAY lah SWEET doh-NAY.", "'I would be grateful if you would tell me what happens next.'"),
               D("Léa", "Et l'ouverture ?", "ay loo-vehr-TÜR ?", "And the opening?"),
               D("Théo", "« Je soussigné … ai l'honneur de solliciter … ». Le registre est déjà dans les verbes.", "zhuh soo-see-NYAY … ay loh-NUHR duh soh-lee-see-TAY …. luh ruh-ZHEESTR ay day-ZHAH dah(n) lay VAIRB.", "'I, the undersigned … have the honour to request …'. The register is already in the verbs.")],
              WS("Formal-letter worksheet", [
                  T("Write the moves.", ["I, the undersigned", "I would be grateful if you would tell me", "I request acknowledgement of receipt"],
                    ["Je soussigné …", "Je vous saurais gré de bien vouloir m'indiquer …", "Je vous prie de bien vouloir accuser réception."]),
                  T("Choose the register.", ["formal request", "neutral alternative"],
                    ["Je vous prie de bien vouloir …", "Pourriez-vous me dire … ?"]),
              ])),
            L("La réclamation : faits, fondements, demande",
              "A written claim has three numbered parts: LES FAITS, LES FONDEMENTS, LA DEMANDE.",
              [V("les faits", "lay FEH", "the facts", "noun"),
               V("les fondements", "lay foh(n)-duh-MAH(N)", "the grounds", "noun"),
               V("la demande", "lah duh-MAH(N)D", "the request", "noun"),
               V("la pièce jointe", "lah pyess ZHWA(N)KT", "attachment", "noun"),
               V("la clause", "lah KLOHZ", "clause", "noun")],
              G("Claim structure",
                "premièrement, les faits … · deuxièmement, les fondements … · enfin, la demande …",
                "Premièrement, les faits : le service a été interrompu le 3 mai. Deuxièmement, les "
                "fondements : la clause sept du contrat. Enfin, la demande : un dédommagement. The "
                "numbering is the argument.",
                [X("Premièrement, les faits : le service a été interrompu le 3 mai.", "pruh-MYAYR-MAH(N), lay FEH : luh sehr-VEES ah ay-TAY a(n)-teh-rroom-PÜ luh trwah MAY.", "First, the facts: the service was interrupted on 3 May."),
                 X("Deuxièmement, les fondements : la clause sept du contrat.", "duh-ZYAYR-MAH(N), lay foh(n)-duh-MAH(N) : lah KLOHZ SET dü koh(n)-TRAH.", "Second, the grounds: clause seven of the contract."),
                 X("Enfin, la demande : un dédommagement.", "ah(n)-FA(N), lah duh-MAH(N)D : uh(n) day-doh-mazh-MAH(N).", "Lastly, the request: compensation.")],
                [("Les fondements : parce que c'est vraiment énervant.", "Les fondements : la clause sept du contrat.", "Grounds are the rule that was broken."),
                 ("La demande : donnez-moi de l'argent.", "La demande : un dédommagement.", "The request is a noun phrase in the formal register.")]),
              [D("Théo", "Comment j'organise la réclamation ?", "koh-MAH(N) zhor-gah-NEEZ lah ray-klah-mah-SYOH(N) ?", "How do I organise the claim?"),
               D("Léa", "Faits, fondements, demande — dans cet ordre.", "FEH, foh(n)-duh-MAH(N), duh-MAH(N)D — dah(n) set ORDR.", "Facts, grounds, request — in that order."),
               D("Théo", "« Premièrement, les faits : le service a été interrompu le 3 mai. »", "pruh-MYAYR-MAH(N), lay FEH : luh sehr-VEES ah ay-TAY a(n)-teh-rroom-PÜ luh trwah MAY.", "'First, the facts: the service was interrupted on 3 May.'"),
               D("Léa", "Et joins la facture : sans pièce, il n'y a pas de dossier.", "ay ZHWA(N) lah fak-TÜR : sah(n) PYESS, eel nyah pah duh doh-SYAY.", "And attach the invoice: without a document, there is no case.")],
              WS("Claim worksheet", [
                  T("Order the claim.", ["first, the facts with the date", "second, the grounds with the clause", "lastly, the request"],
                    ["Premièrement, les faits : …", "Deuxièmement, les fondements : la clause …", "Enfin, la demande : …"]),
                  T("Attach the proof.", ["attach the invoice", "the file number"],
                    ["Je joins la facture.", "le numéro de dossier"]),
              ])),
            L("S'excuser : nous vous prions de bien vouloir nous excuser",
              "Formal apologies are impersonal and specific: NOUS VOUS PRIONS DE BIEN VOULOIR NOUS "
              "EXCUSER, NOUS PRENONS NOTE, NOUS Y REMÉDIERONS.",
              [V("nous vous prions", "noo voo PREEYOH(N)", "we request of you", "phrase"),
               V("les désagréments", "lay day-zah-gray-MAH(N)", "the inconvenience", "noun"),
               V("prendre note", "pra(n)DR NOT", "to take note", "phrase"),
               V("remédier à", "ruh-may-DYAY ah", "to remedy", "verb"),
               V("dans les meilleurs délais", "dah(n) lay may-YUHR day-LAY", "as soon as possible", "phrase")],
              G("Formal apology",
                "nous vous prions de bien vouloir nous excuser · nous vous prions de nous excuser pour … · nous y remédierons dans les meilleurs délais",
                "Nous vous prions de nous excuser pour ce retard. Nous prenons note et nous y "
                "remédierons dans les meilleurs délais. Fact, apology, remedy, deadline — no "
                "emotion, no excuses.",
                [X("Nous vous prions de nous excuser pour ce retard.", "noo voo PREEYOH(N) duh noo zeks-kü-ZAY poor suh ruh-TAR.", "We apologise for this delay."),
                 X("Nous prenons note.", "noo pruh-NOH(N) NOT.", "We take note."),
                 X("Nous y remédierons dans les meilleurs délais.", "noo zee ruh-may-dee-ruh-OH(N) dah(n) lay may-YUHR day-LAY.", "We will remedy it as soon as possible.")],
                [("Désolé, on est vraiment nuls.", "Nous vous prions de nous excuser ; nous y remédierons.", "The formal apology removes the person and keeps the commitment."),
                 ("Nous remédions à le problème.", "Nous y remédions.", "remédier à + le contracts to y when the object is known.")]),
              [D("Léa", "Le client est mécontent. Qu'est-ce que je lui écris ?", "luh kly-AH(N) ay may-koh(n)-TAH(N). kes-kuh zhuh lwee ay-KREE ?", "The client is unhappy. What do I write?"),
               D("Théo", "« Nous vous prions de nous excuser pour ce retard. »", "noo voo PREEYOH(N) duh noo zeks-kü-ZAY poor suh ruh-TAR.", "'We apologise for this delay.'"),
               D("Léa", "Et la suite ?", "ay lah SWEET ?", "And then?"),
               D("Théo", "« Nous prenons note et nous y remédierons dans les meilleurs délais. »", "noo pruh-NOH(N) NOT ay noo zee ruh-may-dee-ruh-OH(N) dah(n) lay may-YUHR day-LAY.", "'We take note and will remedy it as soon as possible.'")],
              WS("Apology worksheet", [
                  T("Write the apology.", ["we apologise for this delay", "we take note", "we will remedy it as soon as possible"],
                    ["Nous vous prions de nous excuser pour ce retard.", "Nous prenons note.", "Nous y remédierons dans les meilleurs délais."]),
                  T("Add the commitment.", ["we take note to avoid it", "the new date is 12 May"],
                    ["Nous prenons note pour l'éviter.", "La nouvelle date est le 12 mai."]),
              ])),
        ]},
        {"id": "B2+-U3", "title": "Citer, résumer, conclure", "lessons": [
            L("Citer et reformuler : selon X, autrement dit",
              "Quotation marks its own voice: SELON X … , COMME LE SOULIGNE X … , POUR REPRENDRE X … "
              "Then the reformulation: AUTREMENT DIT, C'EST-À-DIRE, EN D'AUTRES TERMES.",
              [V("selon", "suh-LOH(N)", "according to", "preposition"),
               V("souligner", "soo-lee-NYAY", "to underline, to point out", "verb"),
               V("autrement dit", "oh-truh-MAH(N) DEE", "in other words", "phrase"),
               V("c'est-à-dire", "set-ah-DEER", "that is to say", "phrase"),
               V("la citation", "lah see-tah-SYOH(N)", "quotation", "noun")],
              G("Citation and reformulation",
                "selon … · comme le souligne … · autrement dit … · en d'autres termes …",
                "Selon l'auteure, le problème est de conception. Autrement dit, ce n'est pas une "
                "question d'argent. En d'autres termes : la conception décide le coût. Quote, "
                "reformulate, conclude.",
                [X("Selon l'auteure, le problème est de conception.", "suh-LOH(N) loh-TUHR, luh proh-BLEM ay duh koh(n)-sep-SYOH(N).", "According to the author, the problem is one of design."),
                 X("Comme le souligne le rapport, il manque des données.", "kum luh soo-LEENY luh rah-POR, eel MAH(N)K day doh-NAY.", "As the report points out, data is missing."),
                 X("Autrement dit, ce n'est pas une question d'argent.", "oh-truh-MAH(N) DEE, suh nay pah zün kes-TYOH(N) dar-ZHAH(N).", "In other words, it is not a question of money.")],
                [("L'auteure dit que c'est de conception et moi aussi.", "Selon l'auteure, le problème est de conception.", "Citation separates the quoted voice from yours."),
                 ("Autrement dit, c'est-à-dire, en d'autres termes, bref.", "Autrement dit, la conception décide le coût.", "One reformulation marker per sentence.")]),
              [D("Léa", "Comment j'insère la citation ?", "koh-MAH(N) zha(n)-SEHR lah see-tah-SYOH(N) ?", "How do I insert the quotation?"),
               D("Théo", "Cite, puis reformule : selon l'auteure …, autrement dit …", "SEET, pwee ruh-for-MÜL : suh-LOH(N) loh-TUHR …, oh-truh-MAH(N) DEE …", "Quote, then reformulate: according to the author …, in other words …"),
               D("Léa", "« Selon l'auteure, le problème est de conception. Autrement dit, ce n'est pas une question d'argent. »", "suh-LOH(N) loh-TUHR, luh proh-BLEM ay duh koh(n)-sep-SYOH(N). oh-truh-MAH(N) DEE, suh nay pah zün kes-TYOH(N) dar-ZHAH(N).", "'According to the author, the problem is one of design. In other words, it is not a question of money.'"),
               D("Théo", "Maintenant la citation travaille pour ton argument.", "ma(n)-tuh-NAH(N) lah see-tah-SYOH(N) trah-VAHY poor toh(n) nar-gü-MAH(N).", "Now the quotation works for your argument.")],
              WS("Citation worksheet", [
                  T("Cite and reformulate.", ["according to the author", "as the report points out", "in other words"],
                    ["Selon l'auteure, …", "Comme le souligne le rapport, …", "Autrement dit, …"]),
                  T("Draw the consequence.", ["that is to say, it is not about money", "design decides cost"],
                    ["C'est-à-dire que ce n'est pas une question d'argent.", "La conception décide le coût."]),
              ])),
            L("Résumer une discussion : en substance, deux positions",
              "A summary names the positions and the shared ground: EN SUBSTANCE, DEUX POSITIONS … ; "
              "POUR L'ESSENTIEL … ; LES DEUX CONVERGENT SUR …",
              [V("en substance", "ah(n) süb-STAH(N)S", "in substance", "phrase"),
               V("pour l'essentiel", "poor lay-sah(n)-SYEL", "in the main", "phrase"),
               V("converger", "koh(n)-ver-ZHAY", "to converge", "verb"),
               V("la position", "lah poh-zee-SYOH(N)", "position", "noun"),
               V("le point commun", "luh pwa(n) koh-MUH(N)", "common ground", "noun")],
              G("Summary frame",
                "en substance, deux positions … · pour l'essentiel, ils convergent sur … · le point commun est …",
                "En substance, deux positions : l'une demande de la vitesse, l'autre des preuves. "
                "Pour l'essentiel, les deux convergent : il manque des informations.",
                [X("En substance, il y a deux positions.", "ah(n) süb-STAH(N)S, eel yah duh poh-zee-SYOH(N).", "In substance, there are two positions."),
                 X("Pour l'essentiel, les deux convergent.", "poor lay-sah(n)-SYEL, lay duh koh(n)-ver-ZH.", "In the main, the two converge."),
                 X("Le point commun est l'absence de données.", "luh pwa(n) koh-MUH(N) ay lah(p)-SAH(N)S duh doh-NAY.", "The common ground is the absence of data.")],
                [("En substance, moi je pense qu'ils ont tort.", "En substance, il y a deux positions ; le point commun est …", "A summary reports, it does not rule."),
                 ("Pour l'essentiel, globalement, un peu près.", "Pour l'essentiel, les deux convergent.", "One hedge per sentence.")]),
              [D("Théo", "Comment je clos la discussion de l'équipe ?", "koh-MAH(N) zhuh KLOH lah dees-kü-SYOH(N) duh lay-KEEP ?", "How do I close the team discussion?"),
               D("Léa", "Compte les positions avant de juger : en substance, deux positions …", "koh(n)T lay poh-zee-SYOH(N) ah-VAH(N) duh zhü-ZHAY : ah(n) süb-STAH(N)S, duh poh-zee-SYOH(N) …", "Count the positions before judging them: in substance, two positions …"),
               D("Théo", "« En substance : l'une demande de la vitesse, l'autre des preuves. »", "ah(n) süb-STAH(N)S : lün duh-MAH(N)D duh lah vee-TESS, loh-truh day PRUHV.", "'In substance: one asks for speed, the other for evidence.'"),
               D("Léa", "Et le point commun : il manque des informations.", "ay luh pwa(n) koh-MUH(N) : eel MAH(N)K day za(n)-for-mah-SYOH(N).", "And the common ground: information is missing.")],
              WS("Summary worksheet", [
                  T("Summarise the discussion.", ["in substance, there are two positions", "in the main, they converge", "the common ground"],
                    ["En substance, il y a deux positions.", "Pour l'essentiel, ils convergent.", "Le point commun est …"]),
                  T("Name the shared ground.", ["both agree that information is missing", "one asks for speed, the other for evidence"],
                    ["Les deux conviennent qu'il manque des informations.", "L'une demande de la vitesse, l'autre des preuves."]),
              ])),
            L("Conclure : en définitive, au vu de ce qui précède",
              "The final paragraph gathers and decides: AU VU DE CE QUI PRÉCÈDE, … ; EN DÉFINITIVE, "
              "… ; ON PEUT CONCLURE QUE …",
              [V("au vu de", "oh VÜ duh", "in view of", "phrase"),
               V("en définitive", "ah(n) day-fee-nee-TEEV", "in the end, ultimately", "phrase"),
               V("conclure", "koh(n)-KLÜR", "to conclude", "verb"),
               V("la recommandation", "lah ruh-koh-mah(n)-dah-SYOH(N)", "recommendation", "noun"),
               V("le préalable", "luh pray-ah-LAHBL", "prerequisite", "noun")],
              G("Closing frame",
                "au vu de ce qui précède, … · en définitive, … · on peut conclure que … · à titre de recommandation …",
                "Au vu de ce qui précède, on peut conclure que le retard était évitable. En "
                "définitive, la recommandation est simple : tester avant de promettre. A close "
                "decides, then recommends.",
                [X("Au vu de ce qui précède, on peut conclure que le retard était évitable.", "oh VÜ duh suh kee pray-SED, oh(n) puh koh(n)-KLÜR kuh luh ruh-TAR ay-TAY ay-vee-TAHBL.", "In view of the foregoing, one may conclude the delay was avoidable."),
                 X("En définitive, la recommandation est simple.", "ah(n) day-fee-nee-TEEV, lah ruh-koh-mah(n)-dah-SYOH(N) ay SA(N)PL.", "Ultimately, the recommendation is simple."),
                 X("À titre de recommandation : tester avant de promettre.", "ah TEETR duh ruh-koh-mah(n)-dah-SYOH(N) : tes-TAY ah-VAH(N) duh proh-METR.", "By way of recommendation: test before promising.")],
                [("En définitive, merci de votre lecture.", "En définitive, la recommandation est simple: tester avant de promettre.", "A close states a conclusion and a next step."),
                 ("Au vu de ce qui précède et aussi d'autres choses.", "Au vu de ce qui précède, on peut conclure que …", "The frame is fixed; the content carries the weight.")]),
              [D("Léa", "Comment je termine le rapport ?", "koh-MAH(N) zhuh tehr-MEEN luh rah-POR ?", "How do I end the report?"),
               D("Théo", "Conclus et recommande : au vu de ce qui précède, on peut conclure que …", "koh(n)-KLÜ ay ruh-koh-MAH(N)D : oh VÜ duh suh kee pray-SED, oh(n) puh koh(n)-KLÜR kuh …", "Conclude and recommend: in view of the foregoing, one may conclude that …"),
               D("Léa", "« On peut conclure que le retard était évitable. »", "oh(n) puh koh(n)-KLÜR kuh luh ruh-TAR ay-TAY ay-vee-TAHBL.", "'One may conclude that the delay was avoidable.'"),
               D("Théo", "Et une recommandation en dernière ligne : toujours la dernière ligne.", "ay ün ruh-koh-mah(n)-dah-SYOH(N) ah(n) dehr-NYAYR LEEY(N) : too-ZHOOR lah dehr-NYAYR LEEY(N).", "And a recommendation on the last line: always the last line.")],
              WS("Closing worksheet", [
                  T("Close the text.", ["in view of the foregoing, the delay was avoidable", "ultimately, the recommendation is simple", "test before promising"],
                    ["Au vu de ce qui précède, le retard était évitable.", "En définitive, la recommandation est simple.", "Tester avant de promettre."]),
                  T("Write the last line.", ["a recommendation", "the next step"],
                    ["La recommandation est …", "La prochaine étape est …"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("French formal writing is a register with its own verbs — je soussigné, je vous "
                 "saurais gré, nous vous prions, au vu de ce qui précède — and its own music: "
                 "numbered facts, a clause as grounds, and a request in one clean sentence. This "
                 "half-step teaches the register and the argument together, because in French "
                 "public life they arrive together: the moment a text becomes formal, it also "
                 "becomes structured."),
        source_url="https://en.wikipedia.org/wiki/Business_etiquette",
        reading=("Au vu de ce qui précède, on peut conclure que le service n'a pas respecté ce qui "
                 "avait été convenu. Premièrement, les faits : l'interruption a duré quatre jours. "
                 "Deuxièmement, les fondements : la clause sept du contrat. Enfin, la demande : un "
                 "dédommagement proportionnel. Nous vous prions de nous excuser pour les "
                 "désagréments ; nous y remédierons dans les meilleurs délais."),
        reading_gloss=("In view of the foregoing, one may conclude that the service did not meet "
                       "what had been agreed. First, the facts: the interruption lasted four days. "
                       "Second, the grounds: clause seven of the contract. Lastly, the request: "
                       "proportional compensation. We apologise for the inconvenience; we will "
                       "remedy it as soon as possible."),
        listening=("Léa: Certes, la mesure réduit les coûts, mais encore faut-il que les équipes suivent.<br>"
                   "Théo: Et donc ?<br>Léa: Je la recommande avec une réserve : un point d'étape en mars.<br>"
                   "Théo: Noté : réserve et point d'étape."),
        listening_gloss=("Léa: Admittedly the measure reduces costs, but the teams still have to "
                         "follow. Théo: And so? Léa: I recommend it with one caveat: a checkpoint "
                         "in March. Théo: Noted: a caveat and a checkpoint."),
        voice_tag=VOICE,
        idioms=[
            ("Faire foi", "to make faith", "to be authoritative, to count as proof"),
            ("Prendre acte", "to take record", "to note formally"),
            ("Sauf erreur ou omission", "except error or omission", "errors and omissions excepted"),
            ("À titre conservatoire", "by way of preservation", "as a precaution"),
            ("Prendre note", "to take note", "to note it down"),
            ("Au pied de la lettre", "at the foot of the letter", "to the letter"),
            ("Porter à connaissance", "to carry to knowledge", "to inform officially"),
            ("Sans but lucratif", "without profit goal", "non-profit"),
            ("Aux fins utiles", "for useful ends", "for whatever purpose may serve"),
            ("Dont acte", "of which record", "noted accordingly"),
        ],
        mistakes=[
            ("Certes la mesure réduit les coûts, mais encore faut-il du temps.", "Certes, la mesure réduit les coûts ; encore faut-il du temps.", "Do not stack mais before encore faut-il."),
            ("Non seulement le prix a augmenté, mais la qualité aussi (acceptable) → the fixed pair is mais encore.", "Non seulement le prix a augmenté, mais encore la qualité a baissé.", "The fixed pair is non seulement … mais encore."),
            ("Je veux que vous me répondez (in a formal letter).", "Je vous prie de bien vouloir me répondre.", "Formal letters use je vous prie de bien vouloir + infinitive."),
        ],
        task_title="Write a one-page formal claim in French",
        task_instructions=("Write a real complaint you could send: a heading, one sentence of "
                           "context, then the three numbered moves — faits with dates, fondements "
                           "with the rule or clause, demande in a single sentence. Close with nous "
                           "vous prions de nous excuser … / nous vous saurais gré … and name the "
                           "proof you attach. Finally, rewrite your opening line at B1 level "
                           "(je veux que vous …) and compare the two registers."),
    ),
    "test": [
        ("translate_en", "Say: Not only did the price rise, but the quality also fell.", "Non seulement le prix a augmenté, mais encore la qualité a baissé."),
        ("translate_fr", "Certes, la mesure réduit les coûts ; encore faut-il que les équipes suivent.", "Admittedly the measure reduces costs; it still takes the teams following."),
        ("multiple_choice", "Which opens a formal request?", "Je vous prie de bien vouloir me répondre."),
        ("fill_in_the_blank", "Je vous saurais gré de bien vouloir m'___ la suite.", "indiquer"),
        ("word_selection", "Select the French for the grounds (of a claim).", "les fondements"),
        ("error_correction", "Non seulement le prix a augmenté, mais la qualité aussi a baissé.", "Non seulement le prix a augmenté, mais encore la qualité a baissé."),
        ("dialogue_completion", "Complete: Nous vous prions de nous ___ pour ce retard.", "excuser"),
        ("matching", "Match « prendre note » to its meaning.", "to note it down"),
        ("reading_comprehension", "Combien de temps a duré l'interruption ?", "four days"),
        ("inference", "« encore faut-il » — what does the speaker accept?", "the fact, while keeping a reserve"),
        ("main_idea", "Au vu de ce qui précède, le retard était évitable. What is this?", "a conclusion of a report"),
        ("detail_identification", "Quelle clause est invoquée comme fondement ?", "clause seven of the contract"),
    ],
}

HALFSTEPS["C1+"] = {
    "title": "French C1+ — Register, strategy and mediation",
    "native": NATIVE,
    "goals": [
        "Rewrite one content in three registers without changing a single fact",
        "Grade commitment precisely: il me semble, j'ai la conviction, je peine à croire",
        "Handle a hostile question and chair the round-table summary",
    ],
    "units": [
        {"id": "C1+-U1", "title": "Précision et engagement", "lessons": [
            L("Le même contenu en trois registres",
              "Register is a dial: LE TRUC, C'EST QUE … (chat), LE PROBLÈME, C'EST QUE … (standard), "
              "FORCE EST DE CONSTATER QUE … (formal). Same fact, three rooms.",
              [V("le registre", "luh ruh-ZHEESTR", "register", "noun"),
               V("familier", "fah-mee-LYAY", "colloquial", "adjective"),
               V("soutenu", "soo-tuh-NÜ", "formal, elevated", "adjective"),
               V("force est de constater", "fors ay duh koh(n)-stah-TAY", "one must note", "phrase"),
               V("le truc", "luh TRÜK", "the thing (familiar)", "noun")],
              G("Register dial",
                "le truc, c'est que … · le problème, c'est que … · force est de constater que …",
                "Le truc, c'est qu'il manque des données. Le problème, c'est qu'il manque des "
                "données. Force est de constater que les informations disponibles sont incomplètes. "
                "One fact, three registers — and the formal one never gets longer than the fact.",
                [X("Le truc, c'est qu'il manque des données.", "luh TRÜK, say keel MAH(N)K day doh-NAY.", "The thing is, data is missing."),
                 X("Le problème, c'est qu'il manque des données.", "luh proh-BLEM, say keel MAH(N)K day doh-NAY.", "The problem is that data is missing."),
                 X("Force est de constater que les informations disponibles sont incomplètes.", "fors ay duh koh(n)-stah-TAY kuh lay za(n)-for-mah-SYOH(N) dees-poh-NEEBL so(n) ta(n)-koh(n)-PLET.", "One must note that the available information is incomplete.")],
                [("En registre soutenu, il faut beaucoup plus de mots.", "Force est de constater que les informations sont incomplètes.", "Formality changes the frame, not the length."),
                 ("Le truc, c'est que, force est de constater que, il manque des données.", "Le problème, c'est qu'il manque des données.", "One register marker per sentence.")]),
              [D("Léa", "Le client repose la même question.", "luh kly-AH(N) ruh-POHZ lah mem kes-TYOH(N).", "The client is asking the same question again."),
               D("Théo", "Ça dépend du registre : au client, « le problème, c'est qu'il manque des données ».", "sah day-PAH(N) dü ruh-ZHEESTR : oh kly-AH(N), luh proh-BLEM, say keel MAH(N)K day doh-NAY.", "It depends on the register: to the client, 'the problem is that data is missing'."),
               D("Léa", "Et dans le rapport ?", "ay dah(n) luh rah-POR ?", "And in the report?"),
               D("Théo", "« Force est de constater que les informations disponibles sont incomplètes. »", "fors ay duh koh(n)-stah-TAY kuh lay za(n)-for-mah-SYOH(N) dees-poh-NEEBL so(n) ta(n)-koh(n)-PLET.", "'One must note that the available information is incomplete.'")],
              WS("Register worksheet", [
                  T("Say the same fact three ways.", ["data is missing (familiar)", "the problem is that data is missing (standard)", "one must note that information is incomplete (formal)"],
                    ["Le truc, c'est qu'il manque des données.", "Le problème, c'est qu'il manque des données.", "Force est de constater que les informations sont incomplètes."]),
                  T("Pick the register.", ["to a client", "in a report"],
                    ["Le problème, c'est que …", "Force est de constater que …"]),
              ])),
            L("Le degré d'engagement : il me semble, j'ai la conviction",
              "Commitment is graded: IL ME SEMBLE (it seems to me), JE SUIS CONVAINCU (I am "
              "convinced), J'AI LA CONVICTION (I hold the conviction), JE PEINE À CROIRE (I find it "
              "hard to believe).",
              [V("il me semble", "eel muh SEMBL", "it seems to me", "phrase"),
               V("être convaincu", "etr koh(n)-va(n)-KÜ", "to be convinced", "phrase"),
               V("j'ai la conviction", "zhay lah koh(n)-veek-SYOH(N)", "I hold the conviction", "phrase"),
               V("je peine à croire", "zhuh pen ah KRWAR", "I find it hard to believe", "phrase"),
               V("à ma connaissance", "ah mah koh(n)-neh-SAH(N)S", "to my knowledge", "phrase")],
              G("Commitment scale",
                "il me semble < je suis convaincu < j'ai la conviction < je peine à croire",
                "Il me semble que la demande a été déposée à temps. J'ai la conviction que le "
                "dossier est complet. À ma connaissance, aucune réclamation n'a suivi. The scale "
                "replaces the adjective with a position.",
                [X("Il me semble que la demande a été déposée à temps.", "eel muh SEMBL kuh lah duh-MAH(N)D ah ay-TAY day-poh-ZAY ah TAH(N).", "It seems to me the application was submitted on time."),
                 X("À ma connaissance, aucune réclamation n'a suivi.", "ah mah koh(n)-neh-SAH(N)S, oh-KÜN ray-klah-mah-SYOH(N) nah swee-VEE.", "To my knowledge, no complaint followed."),
                 X("Je peine à croire qu'il n'y ait pas de trace écrite.", "zhuh pen ah KRWAR keel nyah pah duh TRASS ay-KREET.", "I find it hard to believe there is no written trace.")],
                [("C'est vrai, sûr, je l'ai vu.", "J'ai la conviction que …", "The institutional scale replaces the personal assertion."),
                 ("Je ne sais rien de tout ça.", "À ma connaissance, non.", "The neutral institutional form is à ma connaissance.")]),
              [D("Chef", "La demande a été déposée à temps ?", "lah duh-MAH(N)D ah ay-TAY day-poh-ZAY ah TAH(N) ?", "Was the application submitted on time?"),
               D("Analyste", "Il me semble que oui, mais je vérifie.", "eel muh SEMBL kuh WEE, may zhuh vay-REEFEE.", "It seems so, but I am checking."),
               D("Chef", "Et les réclamations ?", "ay lay ray-klah-mah-SYOH(N) ?", "And the complaints?"),
               D("Analyste", "À ma connaissance, aucune. J'ai la conviction que le dossier est complet.", "ah mah koh(n)-neh-SAH(N)S, oh-KÜN. zhay lah koh(n)-veek-SYOH(N) kuh luh doh-SYAY ay koh(n)-PLET.", "To my knowledge, none. I hold the conviction that the file is complete.")],
              WS("Commitment worksheet", [
                  T("Grade the commitment.", ["it seems to me it was submitted on time", "to my knowledge, no complaint", "I hold the conviction"],
                    ["Il me semble qu'elle a été déposée à temps.", "À ma connaissance, aucune réclamation.", "J'ai la conviction que …"]),
                  T("Sources of information.", ["to my knowledge", "I find it hard to believe"],
                    ["À ma connaissance, …", "Je peine à croire que …"]),
              ])),
            L("Le bémol : en tout cas, du moins, à tout le moins",
              "Three hedges do surgical work: EN TOUT CAS (in any case), DU MOINS (at least), À TOUT "
              "LE MOINS (at the very least).",
              [V("en tout cas", "ah(n) too KAH", "in any case", "phrase"),
               V("du moins", "dü MWA(N)", "at least", "phrase"),
               V("à tout le moins", "ah too luh MWA(N)", "at the very least", "phrase"),
               V("en principe", "ah(n) pra(n)-SEEP", "in principle", "phrase"),
               V("tout au plus", "too toh PLÜ", "at most", "phrase")],
              G("Surgical hedges",
                "en tout cas · du moins · à tout le moins · tout au plus",
                "Il arrivera peut-être en retard ; en tout cas, il préviendra. Du moins, le message "
                "arrive. Tout au plus, on décale d'une semaine. Each hedge adjusts one part of the "
                "sentence and leaves the rest untouched.",
                [X("En tout cas, il préviendra.", "ah(n) too KAH, eel pray-vya(n)-DRAH.", "In any case, he will let us know."),
                 X("Du moins, le message arrive.", "dü MWA(N), luh meh-SAZH ah-REEV.", "At least the message arrives."),
                 X("Tout au plus, on décale d'une semaine.", "too toh PLÜ, oh(n) day-KAL dün suh-MEN.", "At most, we postpone by a week.")],
                [("En tout cas, peut-être, je ne sais pas.", "En tout cas, on décale d'une semaine.", "One hedge; the rest of the sentence stays decisive."),
                 ("Du moins pas.", "Du moins, le message arrive.", "The hedge needs a proposition under it.")]),
              [D("Théo", "On décale le lancement ?", "oh(n) day-KAL luh lah(n)-suh-MAH(N) ?", "Do we postpone the launch?"),
               D("Léa", "Tout au plus d'une semaine. En tout cas, je préviens les clients.", "too toh PLÜ dün suh-MEN. ah(n) too KAH, zhuh pray-VYA(N) lay kly-AH(N).", "A week at most. In any case, I'll tell the clients."),
               D("Théo", "Et le budget ?", "ay luh bü-ZHAY ?", "And the budget?"),
               D("Léa", "Du moins, on le révise avant de signer.", "dü MWA(N), oh(n) luh ray-VEEZ ah-VAH(N) duh see-NYAY.", "At least we review it before signing.")],
              WS("Hedge worksheet", [
                  T("Adjust one part.", ["in any case, I'll tell the clients", "at least the message arrives", "at most a week"],
                    ["En tout cas, je préviens les clients.", "Du moins, le message arrive.", "Tout au plus une semaine."]),
                  T("Set the limits.", ["in principle yes", "at the very least a review"],
                    ["En principe, oui.", "À tout le moins, une révision."]),
              ])),
        ]},
        {"id": "C1+-U2", "title": "Stratégie : dire et démonter", "lessons": [
            L("L'euphémisme et son démontage",
              "Official French hides facts behind soft nouns: PLAN DE DÉPARTS VOLONTAIRES (job cuts), "
              "DOMMAGES COLLATÉRAUX (civilian deaths), INCIDENT TECHNIQUE (an outage).",
              [V("l'euphémisme", "luh-oo-fay-MEESM", "euphemism", "noun"),
               V("le plan social", "luh plah(n) soh-SYAL", "redundancy plan", "noun"),
               V("l'incident", "la(n)-see-DAH(N)", "incident", "noun"),
               V("traduire", "tray-DWEER", "to translate", "verb"),
               V("appeler un chat un chat", "ah-puh-LAY uh(n) shah uh(n) SHAH", "to call a spade a spade", "phrase")],
              G("Undoing a euphemism",
                "ce qu'on appelle … , traduit, c'est … · en clair, … · autrement dit, …",
                "« Plan de départs volontaires » : traduit, quarante licenciements. « Incident "
                "technique » : en clair, neuf heures de panne. Naming the euphemism is itself the "
                "argument.",
                [X("« Plan de départs volontaires » : traduit, quarante licenciements.", "plah(n) duh day-PAR voh-loh(n)-TEHR : tray-DWEE, kah-RAH(N)T lee-see(n)-SYAY-MAH(N).", "'Voluntary departure plan': translated, forty lay-offs."),
                 X("En clair, le service est resté en panne neuf heures.", "ah(n) KLEHR, luh sehr-VEES ay res-TAY ah(n) PAN nuhf UHR.", "In plain terms, the service was down for nine hours."),
                 X("Appelons un chat un chat.", "ah-puh-LOH(N) uh(n) shah uh(n) SHAH.", "Let's call a spade a spade.")],
                [("Il y a un plan social, donc rien d'important.", "« Plan social » : traduit, quarante licenciements.", "The dismantling names the number."),
                 ("C'est de la propagande et du mensonge.", "Ce qu'on appelle « incident technique » : neuf heures de panne.", "Name the mechanism instead of denouncing it.")]),
              [D("Léa", "Le communiqué dit « plan de départs volontaires ».", "luh koh-mü-nee-KAY dee plah(n) duh day-PAR voh-loh(n)-TEHR.", "The press release says 'voluntary departure plan'."),
               D("Théo", "Traduit : quarante licenciements.", "tray-DWEE : kah-RAH(N)T lee-see(n)-SYAY-MAH(N).", "Translated: forty lay-offs."),
               D("Léa", "Et « incident technique » ?", "ay a(n)-see-DAH(N) tek-NEEK ?", "And 'technical incident'?"),
               D("Théo", "En clair : neuf heures de panne.", "ah(n) KLEHR : nuhf UHR duh PAN.", "In plain terms: nine hours of outage.")],
              WS("Euphemism worksheet", [
                  T("Translate the euphemism.", ["voluntary departure plan", "technical incident", "collateral damage"],
                    ["quarante licenciements", "neuf heures de panne", "victimes civiles"]),
                  T("Name the mechanism.", ["this is what is called …", "in plain terms"],
                    ["Ce qu'on appelle … , traduit, c'est …", "En clair, …"]),
              ])),
            L("La prise de parole formelle : annoncer, ordonner, conclure",
              "A formal talk is signposted: J'ARTICULERAI MON PROPOS EN TROIS POINTS · JE M'ARRÊTE SUR "
              "LE DEUXIÈME · POUR TERMINER · JE RESTE À VOTRE DISPOSITION.",
              [V("le propos", "luh proh-POH", "the remarks, the argument", "noun"),
               V("articuler", "ar-tee-kü-LAY", "to structure", "verb"),
               V("m'arrêter sur", "mah-reh-TAY sür", "to dwell on", "phrase"),
               V("pour terminer", "poor tehr-mee-NAY", "to finish", "phrase"),
               V("à votre disposition", "ah votr dees-poh-zee-SYOH(N)", "at your disposal", "phrase")],
              G("Talk signposts",
                "j'articulerai mon propos en trois points · je m'arrête sur … · pour terminer · je reste à votre disposition",
                "J'articulerai mon propos en trois points. Dans le premier, le contexte. Je m'arrête "
                "sur le deuxième : les données. Pour terminer, une recommandation. The signposts "
                "are the talk; the sentences fill them.",
                [X("J'articulerai mon propos en trois points.", "zhar-tee-kü-luh-RAY moh(n) proh-POH ah(n) trwah PWA(N).", "I will structure my remarks in three points."),
                 X("Je m'arrête sur le deuxième point.", "zhuh mah-RET sür luh duh-ZYEM PWA(N).", "I will dwell on the second point."),
                 X("Pour terminer, je reste à votre disposition.", "poor tehr-mee-NAY, zhuh rest ah votr dees-poh-zee-SYOH(N).", "To finish, I remain at your disposal.")],
                [("Bon, je vais parler de choses.", "J'articulerai mon propos en trois points.", "The formal talk announces its own shape."),
                 ("Pour terminer, merci, au revoir.", "Pour terminer, une recommandation : tester avant de promettre.", "The close delivers the last point, then steps back.")]),
              [D("Président", "Vous avez cinq minutes.", "voo zah-VAY sa(n)k mee-NÜT.", "You have five minutes."),
               D("Analyste", "J'articulerai mon propos en trois points.", "zhar-tee-kü-luh-RAY moh(n) proh-POH ah(n) trwah PWA(N).", "I will structure my remarks in three points."),
               D("Président", "Allez-y.", "ah-lay-ZEE.", "Go ahead."),
               D("Analyste", "Je m'arrête sur le deuxième — les données — et, pour terminer, une recommandation.", "zhuh mah-RET sür luh duh-ZYEM — lay doh-NAY — ay, poor tehr-mee-NAY, ün ruh-koh-mah(n)-dah-SYOH(N).", "I dwell on the second — the data — and, to finish, one recommendation.")],
              WS("Talk worksheet", [
                  T("Signpost the talk.", ["I will structure it in three points", "I dwell on the second", "to finish, one recommendation"],
                    ["J'articulerai mon propos en trois points.", "Je m'arrête sur le deuxième point.", "Pour terminer, une recommandation."]),
                  T("Close with the formal offer.", ["I remain at your disposal", "thank you for your attention"],
                    ["Je reste à votre disposition.", "Merci de votre attention."]),
              ])),
            L("Traduire le registre : du titre au rapport",
              "A headline and a report say the same thing in two grammars: « Chômage en hausse » "
              "(noun pile) versus « le taux de chômage a augmenté de 2 % » (sentence).",
              [V("le titre", "luh TEETR", "headline", "noun"),
               V("la manchette", "lah mah(n)-SHET", "headline (large)", "noun"),
               V("le taux", "luh TOH", "rate", "noun"),
               V("la hausse", "lah OHS", "rise", "noun"),
               V("en clair", "ah(n) KLEHR", "in plain terms", "phrase")],
              G("Headline ↔ report",
                "chômage en hausse (titre) · le taux de chômage a augmenté de 2 % (rapport) · en clair …",
                "Le titre : « Chômage en hausse ». Le rapport : le taux de chômage a augmenté de "
                "deux pour cent au premier trimestre. En clair : ça monte un peu. Three readers, "
                "one figure.",
                [X("Titre : Chômage en hausse.", "TEETR : shoh-MAZH ah(n) OHS.", "Headline: unemployment up."),
                 X("Le taux de chômage a augmenté de deux pour cent.", "luh TOH duh shoh-MAZH ah tohg-mah(n)-TAY duh duh poor SAH(N).", "The unemployment rate rose by two per cent."),
                 X("En clair : ça monte un peu.", "ah(n) KLEHR : sah MOH(N)T uh(n) PÜ.", "In plain terms: it is going up a little.")],
                [("Titre : le chômage a augmenté parce qu'il y a une crise et beaucoup de gens.", "Titre : Chômage en hausse.", "Headlines pile the fact; the sentence is the report's job."),
                 ("Rapport : chômage en hausse, à peu près.", "Rapport : le taux de chômage a augmenté de 2 %.", "The report states the figure and its period.")]),
              [D("Léa", "Comment je passe du titre au rapport ?", "koh-MAH(N) zhuh PASS dü TEETR oh rah-POR ?", "How do I go from the headline to the report?"),
               D("Théo", "Mets un verbe et un chiffre : le taux a augmenté de deux pour cent.", "meh ü(n) VAIRB ay ü(n) SHEEFR : luh TOH ah tohg-mah(n)-TAY duh duh poor SAH(N).", "Add a verb and a figure: the rate rose by two per cent."),
               D("Léa", "Et l'inverse, du rapport au titre ?", "ay la(n)-VEHRS, dü rah-POR oh TEETR ?", "And the other way, from report to headline?"),
               D("Théo", "Enlève le verbe et empile : chômage en hausse.", "ah(n)-LEV luh VAIRB ay ah(n)-PEEL : shoh-MAZH ah(n) OHS.", "Drop the verb and pile: unemployment up.")],
              WS("Register-swap worksheet", [
                  T("Turn the headline into a report sentence.", ["unemployment up", "prices falling"],
                    ["Le taux de chômage a augmenté de 2 %.", "Les prix ont légèrement baissé."]),
                  T("Turn the report sentence into a headline.", ["the price rose by four per cent", "consumption fell"],
                    ["Prix en hausse.", "Consommation en baisse."]),
              ])),
        ]},
        {"id": "C1+-U3", "title": "Réplique, questions et table ronde", "lessons": [
            L("La réplique élégante : je me permets de ne pas partager votre analyse",
              "A formal disagreement opens with respect and states the disagreement plainly: JE ME "
              "PERMETS DE NE PAS PARTAGER VOTRE ANALYSE ; LÀ OÙ VOUS VOYEZ UN COÛT, JE VOIS UN "
              "INVESTISSEMENT.",
              [V("je me permets", "zhuh muh per-MEH", "I take the liberty", "phrase"),
               V("ne pas partager", "nuh pah par-tah-ZHAY", "not to share", "phrase"),
               V("là où vous voyez", "lah oo voo vwa-YAY", "where you see", "phrase"),
               V("l'angle", "lah(n)-GL", "angle", "noun"),
               V("la lecture", "lah lek-TÜR", "reading, interpretation", "noun")],
              G("Formal rebuttal",
                "je me permets de ne pas partager votre analyse · là où vous voyez …, je vois …",
                "Je me permets de ne pas partager votre analyse. Là où vous voyez un coût, je vois "
                "un investissement à trois ans. The formula keeps the person and disputes the frame.",
                [X("Je me permets de ne pas partager votre analyse.", "zhuh muh per-MEH duh nuh pah par-tah-ZHAY votr ah-nah-LEEZ.", "I take the liberty of not sharing your analysis."),
                 X("Là où vous voyez un coût, je vois un investissement.", "lah oo voo vwa-YAY uh(n) KOO, zhuh vwah zuh(n) na(n)-ves-tees-MAH(N).", "Where you see a cost, I see an investment."),
                 X("Je diverge sur l'angle, pas sur l'objectif.", "zhuh dee-VERZH sür lah(n)-GL, pah sür lob-zhek-TEEF.", "I differ on the angle, not the objective.")],
                [("Vous avez tort, c'est tout.", "Je me permets de ne pas partager votre analyse.", "The formula states the disagreement without the verdict."),
                 ("Je ne partage pas et vous ne comprenez rien.", "Je diverge sur l'angle, pas sur l'objectif.", "Dispute the frame, not the person's competence.")]),
              [D("Président", "Le coût est insoutenable.", "luh KOO ay a(n)-soot-NAHBL.", "The cost is unsustainable."),
               D("Analyste", "Je me permets de ne pas partager votre analyse.", "zhuh muh per-MEH duh nuh pah par-tah-ZHAY votr ah-nah-LEEZ.", "I take the liberty of not sharing your analysis."),
               D("Président", "Je vous écoute.", "zhuh voo zay-KOOT.", "I'm listening."),
               D("Analyste", "Là où vous voyez un coût, je vois un investissement à trois ans.", "lah oo voo vwa-YAY uh(n) KOO, zhuh vwah zuh(n) na(n)-ves-tees-MAH(N) ah trwah ZAH(N).", "Where you see a cost, I see a three-year investment.")],
              WS("Rebuttal worksheet", [
                  T("Open the formal rebuttal.", ["I take the liberty of not sharing your analysis", "I differ on the angle, not the objective"],
                    ["Je me permets de ne pas partager votre analyse.", "Je diverge sur l'angle, pas sur l'objectif."]),
                  T("Reframe the fact.", ["where you see a cost, I see a three-year investment", "where you see a risk, I see a market"],
                    ["Là où vous voyez un coût, je vois un investissement à trois ans.", "Là où vous voyez un risque, je vois un marché."]),
              ])),
            L("Répondre à une question hostile",
              "A hostile question is answered by reframing it: AVANT DE RÉPONDRE, PRÉCISONS LA "
              "PRÉMISSE · SI JE COMPRENDS BIEN, VOTRE QUESTION PORTE SUR …",
              [V("la prémisse", "lah pray-MEES", "premise", "noun"),
               V("reformuler", "ruh-for-mü-LAY", "to reformulate", "verb"),
               V("si je comprends bien", "see zhuh koh(n)-prah(n) BYA(N)", "if I understand correctly", "phrase"),
               V("porter sur", "por-TAY sür", "to be about", "phrase"),
               V("répondre", "ray-POH(N)DR", "to answer", "verb")],
              G("Answering a hostile question",
                "avant de répondre, précisons la prémisse · si je comprends bien, votre question porte sur …",
                "Avant de répondre, précisons la prémisse : la décision a été prise en mars. Si je "
                "comprends bien, votre question porte sur le délai. Ma réponse tient en un mot : "
                "vérification. Premise, reformulation, answer.",
                [X("Avant de répondre, précisons la prémisse.", "ah-VAH(N) duh ray-POH(N)DR, pray-see-ZOH(N) lah pray-MEES.", "Before answering, let us clarify the premise."),
                 X("Si je comprends bien, votre question porte sur le délai.", "see zhuh koh(n)-prah(n) BYA(N), votr kes-TYOH(N) port sür luh day-LAY.", "If I understand correctly, your question is about the deadline."),
                 X("Ma réponse tient en un mot : vérification.", "mah ray-POH(N)S tyen ah(n) uh(n) MOH : vay-ree-fee-kah-SYOH(N).", "My answer comes down to one word: verification.")],
                [("Cette question est injuste.", "Avant de répondre, précisons la prémisse.", "Reframe the question instead of judging it."),
                 ("Je ne répondrai pas à cela.", "Si je comprends bien, votre question porte sur …", "Answer the reframed question, not the trap.")]),
              [D("Journaliste", "Pourquoi avoir caché l'information ?", "poor-KWAH ah-VWAR kah-SHAY la(n)-for-mah-SYOH(N) ?", "Why did you hide the information?"),
               D("Porte-parole", "Avant de répondre, précisons la prémisse : l'information a été publiée le 4.", "ah-VAH(N) duh ray-POH(N)DR, pray-see-ZOH(N) lah pray-MEES : la(n)-for-mah-SYOH(N) ah ay-TAY pü-blee-AY luh KATR.", "Before answering, let us clarify the premise: the information was published on the 4th."),
               D("Journaliste", "Et le retard, alors ?", "ay luh ruh-TAR, ah-LOR ?", "And the delay, then?"),
               D("Porte-parole", "Si je comprends bien, votre question porte sur le délai : nous avons vérifié les chiffres.", "see zhuh koh(n)-prah(n) BYA(N), votr kes-TYOH(N) port sür luh day-LAY : noo zah-VOH(N) vay-ree-fee-AY lay SHEEFR.", "If I understand correctly, your question is about the timing: we verified the figures.")],
              WS("Hostile-question worksheet", [
                  T("Reframe before answering.", ["let us clarify the premise", "if I understand correctly, your question is about the deadline"],
                    ["Précisons la prémisse.", "Si je comprends bien, votre question porte sur le délai."]),
                  T("Answer in the reframed frame.", ["we verified the figures", "the decision was taken in March"],
                    ["Nous avons vérifié les chiffres.", "La décision a été prise en mars."]),
              ])),
            L("La table ronde : qui a dit quoi et ce qui reste ouvert",
              "Chairing means attributing precisely and closing what is still open: LÉA A SOULIGNÉ "
              "QUE … · THÉO A OBJECTÉ QUE … · RESTE OUVERT …",
              [V("souligner", "soo-lee-NYAY", "to point out", "verb"),
               V("objecter", "ob-zhek-TAY", "to object", "verb"),
               V("rester ouvert", "res-TAY oo-VER", "to remain open", "phrase"),
               V("la table ronde", "lah tabl ROH(N)D", "round table", "noun"),
               V("attribuer", "ah-tree-BÜAY", "to attribute", "verb")],
              G("Chairing frame",
                "Léa a souligné que … · Théo a objecté que … · reste ouvert …",
                "Léa a souligné qu'il manque des données. Théo a objecté qu'elles arrivent en mai. "
                "Reste ouvert le calendrier. Attribution, objection, open question — the three-line "
                "close of every round table.",
                [X("Léa a souligné qu'il manque des données.", "lay-AH ah soo-lee-NYAY keel MAH(N)K day doh-NAY.", "Léa pointed out that data is missing."),
                 X("Théo a objecté que les données arrivent en mai.", "tay-OH ah ob-zhek-TAY kuh lay doh-NAY ah-REEV ah(n) MAY.", "Théo objected that the data arrives in May."),
                 X("Reste ouvert le calendrier.", "rest oo-VER luh kah-lah(n)-DYAY.", "The calendar remains open.")],
                [("Léa a dit des choses et Théo aussi.", "Léa a souligné qu'il manque des données ; Théo a objecté qu'elles arrivent en mai.", "Attribution names the claim, not the fact of speaking."),
                 ("Reste ouvert et c'est tout.", "Reste ouvert le calendrier.", "The open question must be named.")]),
              [D("Président", "On conclut par une synthèse.", "oh(n) koh(n)-KLÜ par ün sa(n)-TEHZ.", "Let's close with a summary."),
               D("Analyste", "Léa a souligné qu'il manque des données ; Théo a objecté qu'elles arrivent en mai.", "lay-AH ah soo-lee-NYAY keel MAH(N)K day doh-NAY ; tay-OH ah ob-zhek-TAY kuh lay doh-NAY ah-REEV ah(n) MAY.", "Léa pointed out that data is missing; Théo objected that it arrives in May."),
               D("Président", "Et qu'est-ce qui reste ouvert ?", "ay kes-kee rest oo-VER ?", "And what remains open?"),
               D("Analyste", "Le calendrier : si les données n'arrivent pas en mai, pas de décision.", "luh kah-lah(n)-DYAY : see lay doh-NAY nah-REEV pah ah(n) MAY, pah duh day-see-ZYOH(N).", "The calendar: if the data does not arrive in May, no decision.")],
              WS("Round-table worksheet", [
                  T("Attribute precisely.", ["Léa pointed out that data is missing", "Théo objected that it arrives in May"],
                    ["Léa a souligné qu'il manque des données.", "Théo a objecté que les données arrivent en mai."]),
                  T("Name what is open.", ["the calendar remains open", "if the data does not arrive, no decision"],
                    ["Reste ouvert le calendrier.", "Si les données n'arrivent pas, pas de décision."]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("At C1 the French learner's problem is no longer grammar but strategy: which register "
                 "to wear, how firm a commitment to make, when to name a euphemism out loud, and how "
                 "to disagree in public without losing the room. The verbs of institutional French — "
                 "il me semble, force est de constater, je me permets de ne pas partager — are the "
                 "tools of that strategy, and they are learnable, formula by formula."),
        source_url="https://en.wikipedia.org/wiki/Register_(sociolinguistics)",
        reading=("Force est de constater que les informations disponibles sont incomplètes. Il me "
                 "semble que la demande a été déposée à temps ; à ma connaissance, aucune "
                 "réclamation n'a suivi. En tout cas, le dossier reste ouvert et le calendrier en "
                 "suspens. Je me permets de ne pas partager votre analyse : là où vous voyez un "
                 "coût, je vois un investissement."),
        reading_gloss=("One must note that the available information is incomplete. It seems to me "
                       "that the application was submitted on time; to my knowledge, no complaint "
                       "followed. In any case, the file remains open and the calendar pending. I "
                       "take the liberty of not sharing your analysis: where you see a cost, I see "
                       "an investment."),
        listening=("Journaliste: Pourquoi avoir caché l'information ?<br>"
                   "Porte-parole: Avant de répondre, précisons la prémisse.<br>"
                   "Journaliste: Allez-y.<br>"
                   "Porte-parole: L'information a été publiée le 4, après vérification des chiffres."),
        listening_gloss=("Journalist: Why did you hide the information? Spokesperson: Before "
                         "answering, let us clarify the premise. Journalist: Go ahead. "
                         "Spokesperson: The information was published on the 4th, after the figures "
                         "were verified."),
        voice_tag=VOICE,
        idioms=[
            ("Rester ouvert", "to remain open", "to still be undecided"),
            ("Mettre l'accent sur", "to put the accent on", "to emphasise"),
            ("Classer le dossier", "to close the file", "to consider the matter closed"),
            ("Laisser en suspens", "to leave in suspense", "to leave hanging"),
            ("Donner le ton", "to give the tone", "to set the tone"),
            ("Perdre le fil", "to lose the thread", "to lose the thread of the argument"),
            ("Avec tout le respect dû", "with all due respect", "with all due respect"),
            ("Remettre en cause", "to put back in cause", "to call into question"),
            ("Aller au fond", "to go to the bottom", "to get to the substance"),
            ("Sans sortir du cadre", "without leaving the frame", "sticking to the brief"),
        ],
        mistakes=[
            ("Je me permets de ne pas être d'accord mais vous avez tort.", "Je me permets de ne pas partager votre analyse ; je diverge sur l'angle.", "Dispute the frame, not the person."),
            ("C'est vrai, je l'ai vu, sûr.", "À ma connaissance, oui.", "The institutional scale replaces the personal assertion."),
            ("Je ne répondrai pas à cette question.", "Avant de répondre, précisons la prémisse.", "Reframe rather than refuse."),
        ],
        task_title="Chair a five-minute round table in French",
        task_instructions=("Write the chair's nine lines for a round table you could actually hold: "
                           "state that the information is incomplete (force est de constater), give "
                           "two commitments at different strengths (il me semble, à ma connaissance), "
                           "reframe one hostile question (avant de répondre …), attribute two "
                           "positions (X a souligné, Y a objecté), and close by naming what remains "
                           "open and what is pending. Read it aloud: if a line needs a comma to "
                           "survive, rewrite the line."),
    ),
    "test": [
        ("translate_en", "Say: I take the liberty of not sharing your analysis.", "Je me permets de ne pas partager votre analyse."),
        ("translate_fr", "Force est de constater que les informations disponibles sont incomplètes.", "One must note that the available information is incomplete."),
        ("multiple_choice", "Which reframes a hostile question?", "Avant de répondre, précisons la prémisse."),
        ("fill_in_the_blank", "___ ma connaissance, aucune réclamation n'a suivi.", "À"),
        ("word_selection", "Select the formal register of « the thing is that ».", "force est de constater que"),
        ("error_correction", "Je ne sais rien de tout ça (in a formal report).", "À ma connaissance, non."),
        ("dialogue_completion", "Complete: Si je comprends bien, votre question ___ sur le délai.", "porte"),
        ("matching", "Match « rester ouvert » to its meaning.", "to still be undecided"),
        ("reading_comprehension", "Qu'est-ce qui reste en suspens ?", "the calendar"),
        ("inference", "« Là où vous voyez un coût, je vois un investissement » — what is being disputed?", "the frame, not the person"),
        ("main_idea", "« Plan social » : traduit, quarante licenciements. What is the speaker doing?", "undoing a euphemism"),
        ("detail_identification", "Quand l'information a-t-elle été publiée ?", "on the 4th"),
    ],
}

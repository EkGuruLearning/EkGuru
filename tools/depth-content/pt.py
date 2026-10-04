# -*- coding: utf-8 -*-
"""Portuguese (Brazil) PHASE 1 depth — extras, third lessons, half-step rungs.

Written with the DSL in `tools/depth_kit.py`; rendered by
`tools/author-depth.py --lang pt`.

House style follows the shipped Portuguese course: the language in `t`, the
course's romanisation in `r` — stressed syllable in CAPITALS, hyphens between
syllables, `(n)` for a nasal vowel (`oh-LAH`, `boh(n) DEE-uh`) — and English in
`en`, because the course teaches in English. Unit ids keep each rung's shipped
scheme (`A1-U1` / `A1-U1-L1` for A1 and A2–B2, `pt-c1-u1` / `pt-c1-l1` for
C1–C2); the half-step rungs use `<RUNG>P-U1` (A1P-U1 … C1P-U1) and their lessons
carry no id, because the renderer assigns one.

The course is **Brazilian** Portuguese: você rather than tu, the gerund
(estou falando) rather than the European infinitive construction (estou a
falar), pão de queijo rather than a pastel de nata. European forms appear only
where a lesson contrasts them on purpose.

Register note: A1–A2 stay in the present and the two pasts; B1 adds the future
and the personal infinitive; B2 the subjunctive and the compound pluperfect;
C1–C2 work in the written register of the Brazilian press and of institutional
mediation (parecer, ata, nota oficial, síntese). The Romanisation column keeps
the course's own convention and is a reading aid, never a phonetic claim.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # tools/ on the path
from depth_kit import D, EXTRA, G, L, T, V, WS, X   # noqa: E402

CODE = "pt"
NAME = "Portuguese"
NATIVE = "português"
PHASE = 1
SCRIPT = "Latin script"
VOICE = "pt-BR"
SKILL = ("Brazilian Portuguese: nasal vowels (ã, õ) and the diphthongs, você as the everyday "
         "second person, ser vs estar, the two pasts (pretérito / imperfeito), the personal "
         "infinitive, the future subjunctive in real conditions, and the written register of "
         "the Brazilian press")

EXTRAS = {}
THIRD = {}
HALFSTEPS = {}


EXTRAS["A1"] = EXTRA(
    culture=("Portuguese is the official language of Brazil and of seven other countries, and "
             "Brazil alone has more speakers than all the others together — which is why this "
             "course teaches the Brazilian variety. Three sounds do most of the work: the nasal "
             "vowels written with a til (pão, irmã, não), nh (like the ny in canyon: manhã) and "
             "lh (like the lli in million: filho). The everyday word for you is você, and it "
             "takes the same verb form as ele, which is why beginners hear fala where Spanish "
             "would say hablas."),
    source_url="https://en.wikipedia.org/wiki/Portuguese_language",
    reading=("Meu nome é Marina e eu moro em Belo Horizonte. Eu tenho vinte e seis anos e "
             "trabalho numa padaria perto de casa. De manhã eu tomo café com leite e como pão "
             "com manteiga. Minha família é grande: meus pais moram no interior, e minha irmã "
             "mora comigo. À noite eu estudo português porque quero escrever melhor. No "
             "domingo nós almoçamos juntos e depois caminhamos no parque."),
    reading_gloss=("My name is Marina and I live in Belo Horizonte. I am twenty-six years old "
                   "and I work in a bakery near my house. In the morning I drink coffee with "
                   "milk and eat bread with butter. My family is big: my parents live in the "
                   "countryside, and my sister lives with me. At night I study Portuguese "
                   "because I want to write better. On Sunday we have lunch together and then "
                   "walk in the park."),
    listening=("Bom dia! Você é a Marina? — Sou, sim. E você? — Eu sou o Paulo, da padaria. "
               "Tudo bem? — Tudo bem, obrigada. Você trabalha aqui? — Trabalho, sim. Comecei "
               "na semana passada."),
    listening_gloss=("Good morning! Are you Marina? — Yes, I am. And you? — I'm Paulo, from "
                     "the bakery. How are you? — All good, thank you. Do you work here? — I "
                     "do, yes. I started last week."),
    voice_tag=VOICE,
    idioms=[
        ("tudo bem?", "all good?", "the everyday how-are-you, used for hello and for goodbye"),
        ("mais ou menos", "more or less", "so-so, when things are neither good nor bad"),
        ("com licença", "with permission", "excuse me — to pass, to interrupt, to leave"),
        ("de nada", "of nothing", "you're welcome"),
        ("que legal!", "how cool!", "genuine approval, the most Brazilian compliment"),
        ("tá bom", "it is good", "all right / okay — spoken, so it is written tá, not está"),
        ("um instante", "one instant", "one moment, please"),
        ("até logo", "until soon", "see you soon"),
        ("por favor", "for favour", "please, in every setting"),
        ("puxa vida!", "pull life!", "oh my — surprise or mild frustration, never rude"),
    ],
    mistakes=[
        ("Eu sou vinte anos.", "Eu tenho vinte anos.", "Age uses ter (to have), never ser."),
        ("Eu estou bom hoje.", "Eu estou bem hoje.", "bem is the adverb of how you are; bom is an adjective for a thing or a person."),
        ("Obrigado! (said by a woman)", "Obrigada! (said by a woman)", "The word agrees with the speaker: a man says obrigado, a woman obrigada."),
    ],
    task_title="Apresente-se em voz alta",
    task_instructions=("Record ninety seconds: name, city, age, work or study, and one thing you "
                       "do every day. Then write the same five sentences by hand. Check three "
                       "things before you finish: tenho for your age, bem after estou, and "
                       "obrigado/obrigada agreeing with you."),
)


EXTRAS["A2"] = EXTRA(
    culture=("Brazilian daily life runs through small shared places: the padaria at the corner, "
             "where people buy pão francês by weight (trezentos gramas, por favor) and drink a "
             "cafezinho standing at the counter; the feira on a fixed weekday, with hortifruti, "
             "pastel and caldo de cana; and the ônibus or metrô that decides how far a job can "
             "be. Prices are in reais, and the plural is regular — um real, dois reais. Food "
             "vocabulary is a survival kit rather than a menu: arroz e feijão is the plate "
             "under everything, and marmita is the box people carry to work."),
    source_url="https://en.wikipedia.org/wiki/Culture_of_Brazil",
    reading=("No sábado eu acordei cedo e fui à feira com a minha vizinha. Compramos banana, "
             "tomate e um quilo de laranja. Ela pediu trezentos gramas de queijo e pagou com "
             "dinheiro; eu paguei com o cartão porque não tinha troco. Depois tomamos caldo de "
             "cana em pé, perto da barraca do pastel. Voltamos a pé porque a feira fica a duas "
             "quadras da nossa rua, e chegamos em casa antes do meio-dia."),
    reading_gloss=("On Saturday I woke up early and went to the street market with my neighbour. "
                   "We bought bananas, tomatoes and a kilo of oranges. She asked for three "
                   "hundred grams of cheese and paid in cash; I paid by card because I had no "
                   "change. Afterwards we drank sugar-cane juice standing up, near the pastel "
                   "stall. We walked back because the market is two blocks from our street, and "
                   "we got home before noon."),
    listening=("Boa tarde, tem pão francês? — Tem, sim. Quantos? — Quatro, por favor. E um "
               "café com leite. — Para levar? — Não, para tomar aqui. Quanto é? — Nove reais "
               "e cinquenta. — Aceita cartão? — Aceita, sim."),
    listening_gloss=("Good afternoon, do you have French bread? — Yes, we do. How many? — Four, "
                     "please. And a coffee with milk. — To take away? — No, to drink here. How "
                     "much is it? — Nine reais and fifty. — Do you take card? — Yes, we do."),
    voice_tag=VOICE,
    idioms=[
        ("a gente", "the people", "we — the everyday form; it takes a third-person singular verb"),
        ("dar um jeito", "to give a way", "to sort something out, to find a way around a problem"),
        ("de bobeira", "of silliness", "hanging around doing nothing"),
        ("ficar de olho", "to stay with an eye", "to keep an eye on something"),
        ("pagar o pato", "to pay the duck", "to be the one who takes the blame"),
        ("na hora", "in the hour", "right then, on the spot"),
        ("vale a pena", "it is worth the pain", "it is worth it"),
        ("em cima da hora", "on top of the hour", "at the last minute"),
        ("quebrar um galho", "to break a branch", "to help someone out of a small jam"),
        ("do dia", "of the day", "today's special — o prato do dia on any restaurant board"),
    ],
    mistakes=[
        ("Ontem eu vou à feira.", "Ontem eu fui à feira.", "A finished time needs the past: fui."),
        ("Ele gosta de ler e eu gosto também de ler livros.", "Ele gosta de ler e eu também gosto de ler livros.", "The adverb também sits before the verb it shares."),
        ("Eu pagui com dinheiro.", "Eu paguei com dinheiro.", "pagar keeps the gu in the first person: paguei."),
    ],
    task_title="Lista da feira e um diálogo",
    task_instructions=("Write a market list of eight items with quantities in Portuguese (quilo, "
                       "gramas, dúzia), then write the six-line dialogue you would have at the "
                       "counter: ask for two items, ask the price, ask whether they take card, "
                       "and say thank you. Read it out loud once without looking."),
)


EXTRAS["B1"] = EXTRA(
    culture=("Brazil is one language with many accents, and the differences are regional before "
             "they are national: the carioca carioca r sounds like an h, the paulistano r is "
             "rolled, the nordestino opens the e and the o and speaks with a tighter rhythm, and "
             "the gaúcho of the South says tu where Rio de Janeiro says você. The sertão of the "
             "Northeast has its own vocabulary of drought and faith (a seca, o retirante, o "
             "cordel), and the Amazon has words that came from Tupi and now belong to everyone "
             "(tapioca, jacaré, maracujá). None of these is more Portuguese than another."),
    source_url="https://en.wikipedia.org/wiki/Brazil",
    reading=("Naquela quinta-feira eu cheguei a Salvador com uma mala pequena e muita vontade de "
             "andar. Chovia forte quando o ônibus parou, e as ruas do Pelourinho estavam cheias "
             "de gente correndo com guarda-chuva. Eu tinha reservado uma pousada perto do "
             "elevador, mas não sabia ler o mapa, então perguntei a um senhor que vendia acarajé "
             "na esquina. Ele riu, apontou para cima e disse que era só seguir a ladeira. "
             "Enquanto eu subia, um grupo começou a cantar dentro de um bar, e eu parei para "
             "ouvir antes de procurar o endereço."),
    reading_gloss=("That Thursday I arrived in Salvador with a small suitcase and a strong wish "
                   "to walk around. It was raining hard when the bus stopped, and the streets of "
                   "Pelourinho were full of people running with umbrellas. I had booked a "
                   "guesthouse near the elevator, but I could not read the map, so I asked a man "
                   "selling acarajé on the corner. He laughed, pointed upwards and said I just "
                   "had to go up the hill. While I was climbing, a group started singing inside "
                   "a bar, and I stopped to listen before looking for the address."),
    listening=("Você já foi ao Nordeste? — Já, fui duas vezes, mas só conheço o litoral. — Eu "
               "quero ir no ano que vem, em julho. Dizem que as festas juninas são "
               "impressionantes. — São mesmo. Se você puder, fique até o São João; vale a pena."),
    listening_gloss=("Have you ever been to the Northeast? — Yes, twice, but I only know the "
                     "coast. — I want to go next year, in July. They say the June festivals are "
                     "impressive. — They really are. If you can, stay for Saint John's Day; it "
                     "is worth it."),
    voice_tag=VOICE,
    idioms=[
        ("chutar o balde", "to kick the bucket", "to lose patience and give up on a plan"),
        ("pisar na bola", "to step on the ball", "to mess up, to fail someone"),
        ("cair a ficha", "the token drops", "the penny finally drops, the moment you understand"),
        ("acertar na mosca", "to hit the fly", "to get it exactly right"),
        ("fazer vista grossa", "to make a thick sight", "to look away on purpose, to let something pass"),
        ("estar por fora", "to be outside", "to be out of the loop"),
        ("meter os pés pelas mãos", "to put the feet through the hands", "to muddle a simple task out of nerves"),
        ("dar com a língua nos dentes", "to hit the tongue on the teeth", "to let a secret slip"),
        ("ir por água abaixo", "to go down with the water", "to fall apart, of a plan"),
        ("estar com a corda toda", "to be with the whole rope", "to be full of energy"),
    ],
    mistakes=[
        ("Eu tenho visto ele ontem.", "Eu vi ele ontem.", "A finished time (ontem) takes the simple past, not the compound perfect."),
        ("Se eu ter dinheiro, eu viajo.", "Se eu tiver dinheiro, eu viajo.", "A real condition takes the future subjunctive: tiver."),
        ("Fazem dois anos que eu moro aqui.", "Faz dois anos que eu moro aqui.", "Fazer for elapsed time is impersonal and stays singular."),
    ],
    task_title="Uma história em duas páginas de caderno",
    task_instructions=("Write 120 to 150 words about a trip or a move: set the scene with the "
                       "imperfeito (chovia, eu tinha, as ruas estavam), then give the events in "
                       "the pretérito (cheguei, perguntei, ele riu). Use at least four linkers "
                       "(quando, enquanto, então, depois, no fim). Then read it aloud and mark "
                       "every verb; if a verb surprises you, check it against the lesson's model."),
)


EXTRAS["B2"] = EXTRA(
    culture=("Brazilian culture makes its arguments in public: samba was born in the houses of "
             "Bahia and grew in the morros of Rio; bossa nova took the same rhythm into a small "
             "room and a quiet voice; the MPB of the 1960s and 1970s turned song into political "
             "speech, and some of it was written in exile. Literature runs from Machado de Assis, "
             "who dissected a society by refusing to flatter it, to Clarice Lispector, who "
             "dissected a sentence, and to the cordel leaflets of the Northeast, printed and "
             "sold at fairs and still read aloud. To criticise here is not to be against "
             "Brazil — it is the local form of taking part."),
    source_url="https://en.wikipedia.org/wiki/Brazilian_literature",
    reading=("A roda de samba começou às nove, quando o dono do bar empurrou as mesas para a "
             "calçada. Ninguém anunciou nada: o cavaquinho tocou dois acordes e todo mundo já "
             "sabia a entrada. Havia um senhor de uns oitenta anos que cantava com um chapéu no "
             "colo e uma menina de doze que repetia o refrão sem olhar para o violão. Entre uma "
             "música e outra, alguém contou que aquele grupo tocava ali desde 1998, e que a "
             "prefeitura tinha querido fechar a rua no ano passado. O samba continuou, mais "
             "baixo e depois mais alto, até que o dono trouxe água para os músicos e a roda "
             "virou conversa."),
    reading_gloss=("The samba circle started at nine, when the bar owner pushed the tables out "
                   "onto the pavement. Nobody announced anything: the cavaquinho played two "
                   "chords and everyone already knew the entry. There was a man of about eighty "
                   "singing with a hat on his lap and a twelve-year-old girl repeating the "
                   "chorus without looking at the guitar. Between one song and the next, someone "
                   "said the group had played there since 1998, and that the city government had "
                   "wanted to close the street last year. The samba went on, quieter and then "
                   "louder, until the owner brought water for the musicians and the circle turned "
                   "into a conversation."),
    listening=("Você leu a crítica de ontem? — Li, mas discordo do título. — Por quê? — Porque "
               "o filme não é sobre a seca; a seca é o cenário. O que me interessa é a relação "
               "entre o pai e a filha, e isso a crítica nem menciona."),
    listening_gloss=("Did you read yesterday's review? — I did, but I disagree with the "
                     "headline. — Why? — Because the film is not about the drought; the drought "
                     "is the setting. What interests me is the relationship between the father "
                     "and the daughter, and the review does not even mention it."),
    voice_tag=VOICE,
    idioms=[
        ("abrir o jogo", "to open the game", "to be frank, to lay the cards on the table"),
        ("botar a mão na massa", "to put a hand in the dough", "to stop talking and start working"),
        ("enxugar gelo", "to dry ice", "to do work that melts as fast as it is done"),
        ("segurar a barra", "to hold the bar", "to carry the pressure for everyone"),
        ("fazer das tripas coração", "to make a heart out of the guts", "to summon courage at a bad moment"),
        ("colocar panos quentes", "to lay warm cloths", "to smooth a conflict over instead of solving it"),
        ("sair pela tangente", "to leave by the tangent", "to dodge the actual question"),
        ("de mãos atadas", "with hands tied", "with no room to act"),
        ("pegar pesado", "to grab heavy", "to be harsh with someone"),
        ("tirar do sério", "to take out of serious", "to make someone lose their composure"),
    ],
    mistakes=[
        ("Se eu seria rico, eu viajaria.", "Se eu fosse rico, eu viajaria.", "An unreal condition takes the imperfect subjunctive: fosse."),
        ("Espero que ela está bem.", "Espero que ela esteja bem.", "Espero que triggers the present subjunctive."),
        ("Prefiro que você vai sozinho.", "Prefiro que você vá sozinho.", "Preferir que also takes the subjunctive."),
    ],
    task_title="Uma crítica curta com uma tese",
    task_instructions=("Choose a Brazilian song, film or book you know. Write 150 to 200 words "
                       "with one sentence that states your thesis, two paragraphs that support "
                       "it from the work itself (quote a line, a scene, a verse), and one "
                       "concession starting with embora or ainda que. Finish with a sentence "
                       "that states what your reading does not claim."),
)


EXTRAS["C1"] = EXTRA(
    culture=("Brazilian public language is built for attribution. A newspaper report names its "
             "source and hedges the claim (segundo o relatório, o índice teria caído), an "
             "official nota is written in the impersonal third person, and a parecer técnico "
             "states its scope before its conclusion so the reader can tell a finding from an "
             "opinion. Institutions have their own abbreviations — STF, Congresso, Banco "
             "Central, SUS — and they are used without gloss in the press. The register also "
             "carries a social rule: direct disagreement with a named person is softened with "
             "ressalvas, while disagreement with a document can be blunt."),
    source_url="https://en.wikipedia.org/wiki/Media_of_Brazil",
    reading=("Segundo o relatório divulgado ontem pelo instituto, o acesso à internet nas "
             "escolas públicas teria crescido 14% em dois anos, embora a pesquisa reconheça que "
             "a amostra se limita a nove estados. O texto não afirma que a meta foi cumprida: "
             "diz que houve avanço e que o ritmo permanece desigual entre as regiões. Em nota, a "
             "secretaria informou que os dados de 2026 serão publicados em março e que a "
             "metodologia está à disposição para consulta. Procurado, o sindicato não se "
             "manifestou até o fechamento desta edição."),
    reading_gloss=("According to the report released yesterday by the institute, internet "
                   "access in public schools has reportedly grown 14% in two years, although the "
                   "study acknowledges that the sample is limited to nine states. The text does "
                   "not claim the target was met: it says there was progress and that the pace "
                   "remains uneven between regions. In a statement, the secretariat said the "
                   "2026 data will be published in March and that the methodology is available "
                   "for consultation. Contacted, the union had not commented by the time this "
                   "edition closed."),
    listening=("A senhora confirma que o número foi revisado? — Confirmo que houve revisão, mas "
               "não posso adiantar o valor antes da publicação. — O jornal teve acesso a uma "
               "planilha que aponta queda. — Não comento documentos que não são oficiais. "
               "Posso dizer, isso sim, que a série histórica será divulgada com a nota "
               "metodológica."),
    listening_gloss=("Do you confirm the figure was revised? — I confirm there was a revision, "
                     "but I cannot give the value before publication. — The paper had access to a "
                     "spreadsheet showing a fall. — I do not comment on documents that are not "
                     "official. I can say, however, that the historical series will be released "
                     "together with the methodological note."),
    voice_tag=VOICE,
    idioms=[
        ("à luz de", "in the light of", "by reference to, when reading something against a source"),
        ("sob pena de", "under penalty of", "with a stated consequence if it is not respected"),
        ("em tese", "in thesis", "in principle — the form that leaves the practice open"),
        ("a contento", "to contentment", "satisfactorily, to the standard required"),
        ("de antemão", "from beforehand", "in advance, before anything is asked"),
        ("com reservas", "with reservations", "accepting only in part, and saying so"),
        ("por ora", "for now", "for the present, without closing the question"),
        ("de praxe", "of custom", "as the standard procedure of an institution"),
        ("em última análise", "in the last analysis", "when everything else has been weighed"),
        ("ao largo de", "along the width of", "beside the point, deliberately outside a debate"),
    ],
    mistakes=[
        ("Ainda que as evidências são limitadas.", "Ainda que as evidências sejam limitadas.", "Ainda que introduces a concession and takes the subjunctive."),
        ("Não convém de ignorar o resultado.", "Não convém ignorar o resultado.", "Convém takes a bare infinitive, with no preposition."),
        ("Os dados mostra uma queda.", "Os dados mostram uma queda.", "Os dados is plural: mostram."),
    ],
    task_title="A mesma notícia em dois registros",
    task_instructions=("Take the facts in the reading (14% growth, nine states, uneven pace, a "
                       "reply in March) and write them twice: once as a nota oficial of four "
                       "sentences in the impersonal third person, and once as a press lede of "
                       "three sentences with explicit attribution. Under both, write one line "
                       "stating what a reader cannot conclude from the facts."),
)


EXTRAS["C2"] = EXTRA(
    culture=("Brazilian Portuguese is the majority language of a country with more than two "
             "hundred living languages. Tupi and the língua geral shaped the vocabulary of "
             "everyday life (tapioca, pipoca, jacaré) and Nheengatu is still spoken in the "
             "Amazon; Quimbundo and other African languages arrived with the enslaved and stayed "
             "in the house (caçula, moleque, dengo, samba); Italian, German and Japanese shaped "
             "the South and São Paulo. The 2009 spelling agreement tried to bring the written "
             "norms of the Portuguese-speaking countries closer, and inside Brazil the language "
             "keeps moving: a written norm used by the press, a spoken norm that varies by "
             "region, and a set of digital habits nobody codified yet. To write about Portuguese "
             "well is to keep those layers visible."),
    source_url="https://en.wikipedia.org/wiki/Languages_of_Brazil",
    reading=("Toda língua viva se move, e o português brasileiro se move em três velocidades: a "
             "norma escrita, que a escola ensina e o jornal pratica; a fala culta, que varia de "
             "cidade a cidade e admite o você e o a gente sem cerimônia; e o que ainda não tem "
             "nome, a língua que se escreve no celular e se corrige depois. Quem aprendeu o "
             "português fora do Brasil costuma chegar pela primeira velocidade e estranhar as "
             "outras duas — como se houvesse uma única forma certa esperando em algum lugar. "
             "Não há. Há uma língua que se escreve com regras e se fala com acordos locais, e "
             "quem escreve bem é quem sabe escolher entre as duas sem desprezar nenhuma."),
    reading_gloss=("Every living language moves, and Brazilian Portuguese moves at three speeds: "
                   "the written norm, which school teaches and newspapers practise; educated "
                   "speech, which varies from city to city and admits você and a gente without "
                   "ceremony; and what has no name yet, the language written on a phone and "
                   "corrected afterwards. Those who learned Portuguese outside Brazil usually "
                   "arrive through the first speed and are puzzled by the other two — as if a "
                   "single correct form were waiting somewhere. There is not. There is a language "
                   "written with rules and spoken with local agreements, and a good writer is "
                   "one who can choose between the two without despising either."),
    listening=("Participante A: A norma escrita empobrece a fala? — Participante B: Não "
               "empobrece; ela dá um chão comum. O problema é usar o chão como teto. — "
               "Participante C: Eu acrescentaria que a escola ensina a norma como se fosse "
               "identidade, e não é: é uma ferramenta portátil. Quem sai do país leva a "
               "ferramenta e encontra outras falas."),
    listening_gloss=("Speaker A: Does the written norm make speech poorer? — Speaker B: It does "
                     "not; it gives a common ground. The problem is using the ground as a "
                     "ceiling. — Speaker C: I would add that school teaches the norm as if it "
                     "were identity, and it is not: it is a portable tool. Anyone who leaves the "
                     "country takes the tool and meets other ways of speaking."),
    voice_tag=VOICE,
    idioms=[
        ("quem não arrisca não petisca", "whoever does not risk does not nibble", "nothing is gained without trying"),
        ("água mole em pedra dura tanto bate até que fura", "soft water on hard stone hits until it pierces", "persistence wears down resistance"),
        ("cada macaco no seu galho", "each monkey on its own branch", "everyone should mind their own domain"),
        ("não adianta chorar sobre o leite derramado", "it is no use crying over spilled milk", "the loss is done; act from here"),
        ("de grão em grão a galinha enche o papo", "grain by grain the hen fills its crop", "small steady steps add up"),
        ("quando um não quer, dois não brigam", "when one does not want it, two do not fight", "a conflict needs two participants"),
        ("em terra de cego, quem tem um olho é rei", "in the land of the blind, the one-eyed is king", "scarcity makes ordinary competence stand out"),
        ("quem tem boca vai a Roma", "whoever has a mouth goes to Rome", "asking is how you find your way"),
        ("a esperança é a última que morre", "hope is the last to die", "people hold on longest to hope"),
        ("santos de casa não fazem milagre", "saints at home work no miracles", "familiarity hides the value of those close by"),
    ],
    mistakes=[
        ("Não obstante das críticas, o projeto seguiu.", "Não obstante as críticas, o projeto seguiu.", "Não obstante takes a bare noun phrase, with no preposition."),
        ("Seria preciso que ela se dedicaria mais.", "Seria preciso que ela se dedicasse mais.", "An impersonal necessity clause takes the subjunctive."),
        ("Prefere-se que os candidatos apresentam o documento.", "Prefere-se que os candidatos apresentem o documento.", "Prefere-se que introduces the subjunctive in the embedded clause."),
    ],
    task_title="Síntese de duas fontes com limites declarados",
    task_instructions=("Write a 200-word synthesis of the two positions in the listening: the "
                       "norm as common ground, and the norm as a portable tool. Attribute each "
                       "idea to its speaker, add one consequence of your own, and finish with "
                       "two sentences stating what the evidence does not establish. Use at least "
                       "three connectives from this level (na medida em que, ainda assim, em "
                       "última análise)."),
)


THIRD["A1"] = [
    ("A1-U1", "A1-U1-L3", L("O alfabeto, os acentos e o seu nome",
        "Portuguese writes almost what it says, and the exceptions are the accents. The til "
        "makes a vowel nasal (ã, õ), the cedilla keeps a c soft (ç), the acute marks the "
        "stressed vowel (é, á) and the circumflex marks a closed one (ê, ô). When someone asks "
        "como se escreve?, they want letters, not sounds — double l, c with cedilla, no accent.",
        [V("a letra", "ah LEH-trah", "letter", "noun"),
         V("o acento", "oo ah-SEN-too", "accent mark", "noun"),
         V("a cedilha", "ah seh-DEE-lyah", "cedilla", "noun"),
         V("soletrar", "soh-leh-TRAHR", "to spell", "verb"),
         V("o sobrenome", "oo soh-breh-NOH-mee", "surname", "noun")],
        G("Asking and giving a spelling",
          "Como se escreve o seu sobrenome? · Escreve-se com dois l · Tem acento?",
          "Como se escreve? asks how a word is written, and the answer is given letter by "
          "letter or by naming the change: com acento, sem acento, com dois l, com ç. The "
          "customer-service form é escrito com… is also ordinary. Names keep their own spelling, "
          "so ask instead of guessing.",
          [X("Como se escreve o seu sobrenome?", "KOH-moo see es-KREH-vee oo seh-oo soh-breh-NOH-mee?", "How is your surname spelled?"),
           X("Escreve-se com ç e com acento.", "es-KREH-vee-see koh(n) ç ee koh(n) ah-SEN-too.", "It is written with a cedilla and an accent."),
           X("Meu nome tem dois l.", "meh-oo NOH-mee tay(n) doys EH-lee.", "My name has two l's.")],
          [("Como escreve seu nome?", "Como se escreve o seu nome?", "The question needs se: como se escreve."),
           ("Meu nome é escrito em dois l.", "Meu nome se escreve com dois l.", "A name is written with a letter, not em.")]),
        [D("Recepcionista", "Bom dia! Qual é o seu nome completo?", "boh(n) DEE-ah! kwah-oo eh oo seh-oo NOH-mee koh(n)-PLEH-too?", "Good morning! What is your full name?"),
         D("Cliente", "Marina Souza. Souza com z.", "mah-REE-nah SOH-zah. SOH-zah koh(n) z.", "Marina Souza. Souza with a z."),
         D("Recepcionista", "E o sobrenome tem acento?", "ee oo soh-breh-NOH-mee tay(n) ah-SEN-too?", "And does the surname have an accent?"),
         D("Cliente", "Não, sem acento. Só o nome tem.", "now(n), say(n) ah-SEN-too. soh oo NOH-mee tay(n).", "No, no accent. Only the first name has one.")],
        WS("Spelling worksheet", [
            T("Ask how to write it.", ["how is your surname spelled?", "does the name have an accent?"],
              ["Como se escreve o seu sobrenome?", "O nome tem acento?"]),
            T("Give the spelling.", ["with a cedilla and no accent", "with two l's"],
              ["com ç e sem acento", "com dois l"]),
        ]))),
    ("A1-U2", "A1-U2-L3", L("A casa: moro em, tem, fica",
        "Three verbs describe a home and only one of them is about you. Eu moro em… puts you "
        "there, o apartamento tem… describes what is inside, and o prédio fica… places the "
        "building in the street. The same three do the work for a job or a school: trabalho em, "
        "a empresa tem, fica no centro.",
        [V("o quarto", "oo KWAHR-doo", "bedroom", "noun"),
         V("a sala", "ah SAH-lah", "living room", "noun"),
         V("a cozinha", "ah koh-ZEE-nyah", "kitchen", "noun"),
         V("o andar", "oo an-DAHR", "floor, storey", "noun"),
         V("o prédio", "oo PREH-dee-oo", "building", "noun")],
        G("Describing where you live",
          "Eu moro em … · tem dois quartos · fica perto do centro",
          "Moro em takes the city or the neighbourhood, not the street: moro em Pinheiros, moro "
          "em São Paulo. Tem is used with no subject when you list what exists: tem uma cozinha "
          "grande. Fica places the building: o prédio fica na esquina. All three stay in the "
          "present for a permanent arrangement.",
          [X("Eu moro em Pinheiros, num apartamento pequeno.", "eh-oo MOH-roo ey(n) pee-NYAY-roos, noo(n) ah-pahr-tah-MEN-too peh-KEH-noo.", "I live in Pinheiros, in a small flat."),
           X("Tem dois quartos e uma cozinha grande.", "tay(n) doys KWAHR-doos ee OO-mah koh-ZEE-nyah GRAHN-jee.", "It has two bedrooms and a big kitchen."),
           X("O prédio fica na esquina, perto do mercado.", "oo PREH-dee-oo FEE-kah nah es-KEE-nah, PEHR-too doo mehr-KAH-doo.", "The building is on the corner, near the market.")],
          [("Eu moro no Pinheiros rua.", "Eu moro na rua Pinheiros.", "moro em + a rua becomes na rua, and the street name follows."),
           ("Meu apartamento fica dois quartos.", "Meu apartamento tem dois quartos.", "A flat has rooms; it does not ficar them.")]),
        [D("Vizinha", "Você mora aqui no prédio?", "voh-SEH MOH-rah ah-KEE noo PREH-dee-oo?", "Do you live here in the building?"),
         D("Marina", "Moro, sim, no terceiro andar.", "MOH-roo, see(n), noo tehr-SAY-roo an-DAHR.", "Yes, I do, on the third floor."),
         D("Vizinha", "E o apartamento tem varanda?", "ee oo ah-pahr-tah-MEN-too tay(n) vah-RAHN-dah?", "And does the flat have a balcony?"),
         D("Marina", "Tem uma pequena, que fica de frente para a rua.", "tay(n) OO-mah peh-KEH-nah, kee FEE-kah jee FREHN-jee pah-rah ah HOO-ah.", "It has a small one, facing the street.")],
        WS("Home worksheet", [
            T("Say where you live.", ["I live in a small flat in the centre", "it has two bedrooms and a kitchen"],
              ["Eu moro num apartamento pequeno no centro", "tem dois quartos e uma cozinha"]),
            T("Place the building.", ["the building is near the market", "on the third floor"],
              ["o prédio fica perto do mercado", "no terceiro andar"]),
        ]))),
    ("A1-U3", "A1-U3-L3", L("O tempo, as estações e o que fazer no fim de semana",
        "Weather is said two ways and both are correct: está quente (it is hot, with an "
        "adjective) and faz calor (it is hot, with a noun). Choose by what follows — faz calor "
        "pairs with nouns (calor, frio, sol, vento) and está pairs with adjectives (quente, "
        "frio, nublado). Chover and nevar are impersonal: chove muito em janeiro.",
        [V("o verão", "oo veh-RAH(n)", "summer", "noun"),
         V("o inverno", "oo een-VEHR-noo", "winter", "noun"),
         V("o calor", "oo kah-LOHR", "heat", "noun"),
         V("a chuva", "ah SHOO-vah", "rain", "noun"),
         V("nublado", "noo-BLAH-doo", "cloudy", "adjective")],
        G("Talking about the weather",
          "está quente · faz calor · chove muito · no fim de semana",
          "Use está + adjective for a moment (hoje está frio), and faz + noun for what the day "
          "is like (faz frio no inverno). Verbs of weather have no subject: chove, neva, venta. "
          "The seasons in Brazil run the other way round from Europe: o verão is December to "
          "March, and o inverno is short in the North and real in the South.",
          [X("Hoje está nublado e faz frio.", "OH-jee es-TAH noo-BLAH-doo ee fah(f) FEE-oo.", "Today it is cloudy and cold."),
           X("No verão chove quase toda tarde.", "noo veh-RAH(n) SHOH-vee KWAH-zee TOH-dah TAHR-jee.", "In summer it rains almost every afternoon."),
           X("No fim de semana eu vou à praia se fizer sol.", "noo fee(n) jee seh-MAH-nah eh-oo voh ah PRAH-yah see fee-ZEHR soh-oo.", "At the weekend I go to the beach if it is sunny.")],
          [("Hoje faz quente.", "Hoje está quente.", "Quente is an adjective: it goes with está."),
           ("Chove muito em janeiro, chove é impessoal.", "Chove muito em janeiro.", "Weather verbs take no subject.")]),
        [D("Paulo", "Vai fazer calor no fim de semana?", "vey fah-ZEHR kah-LOHR noo fee(n) jee seh-MAH-nah?", "Is it going to be hot at the weekend?"),
         D("Marina", "Dizem que sim, mas no sábado à tarde chove.", "DEE-zay(n) kee see(n), mahs noo SAH-bah-doo ah TAHR-jee SHOH-vee.", "They say so, but on Saturday afternoon it rains."),
         D("Paulo", "Então vou deixar a praia para domingo.", "en-TOW(n) voh deh-SHAHR ah PRAH-yah pah-rah doh-MEEN-goo.", "Then I'll leave the beach for Sunday."),
         D("Marina", "Boa ideia. No domingo faz sol e está quente.", "BOH-ah ee-DAY-ah. noo doh-MEEN-goo fah(f) soh-oo ee es-TAH KEH(n)-jee.", "Good idea. On Sunday it is sunny and hot.")],
        WS("Weather worksheet", [
            T("Describe today.", ["today it is cloudy and cold", "in summer it rains almost every afternoon"],
              ["Hoje está nublado e faz frio", "No verão chove quase toda tarde"]),
            T("Make a weekend plan.", ["at the weekend I go to the beach if it is sunny", "on Sunday it is sunny and hot"],
              ["No fim de semana eu vou à praia se fizer sol", "No domingo faz sol e está quente"]),
        ]))),
]

THIRD["A2"] = [
    ("A2-U1", "A2-U1-L3", L("Direções: a pé, de ônibus, de metrô",
        "Brazilian directions are given in the imperative you (vira, desce, pega), which is the "
        "same form as the third person singular: ele vira, você vira. Distance is counted in "
        "quadras (blocks) and walking time, and the destination is placed with fica: fica a duas "
        "quadras daqui.",
        [V("à direita", "ah jee-RAY-tah", "to the right", "phrase"),
         V("à esquerda", "ah es-KEHR-dah", "to the left", "phrase"),
         V("a quadra", "ah KWAH-drah", "city block", "noun"),
         V("o ponto", "oo POHN-too", "bus stop", "noun"),
         V("a estação", "ah es-tah-SOW(n)", "station", "noun")],
        G("Giving and following directions",
          "vira à direita · desce na próxima · fica a duas quadras daqui",
          "The tu/você imperative is the ordinary spoken form: vira, desce, sobe, pega, segue. "
          "Landmarks come before the direction (depois do mercado, vira à esquerda), and the "
          "answer to quanto tempo a pé? is given in minutes: uns dez minutos.",
          [X("Segue reto e vira à direita depois do mercado.", "SEH-gee HEH-too ee VEE-rah ah jee-RAY-tah deh-POYS doo mehr-KAH-doo.", "Go straight and turn right after the market."),
           X("A estação fica a duas quadras daqui.", "ah es-tah-SOW(n) FEE-kah ah DOO-ahs KWAH-drahs dah-KEE.", "The station is two blocks from here."),
           X("Pega o ônibus no ponto em frente à farmácia.", "PEH-gah oo OH-nee-boos noo POHN-too ey(n) FREHN-jee ah fahr-MAH-see-ah.", "Take the bus at the stop opposite the pharmacy.")],
          [("Vira na direita.", "Vira à direita.", "Direction uses the preposition a: à direita."),
           ("O ponto fica a duas quadras longe.", "O ponto fica a duas quadras daqui.", "Distance from here is daqui, not longe.")]),
        [D("Turista", "Desculpe, como eu chego ao museu?", "des-KOOL-pee, KOH-moo eh-oo SHEH-goo ah-oo moo-ZEH-oo?", "Excuse me, how do I get to the museum?"),
         D("Passante", "Segue reto até o semáforo e vira à esquerda.", "SEH-gee HEH-too ah-TEH oo seh-MAH-foh-roo ee VEE-rah ah es-KEHR-dah.", "Go straight to the traffic light and turn left."),
         D("Turista", "É longe? Dá para ir a pé?", "eh LOHN-jee? dah pah-rah eer ah PEH?", "Is it far? Can I walk?"),
         D("Passante", "Dá. Uns quinze minutos, ou duas quadras de metrô.", "dah. oo(n)s KEEN-zee mee-NOO-toos, oh DOO-ahs KWAH-drahs jee meh-TROH.", "You can. About fifteen minutes, or two stops by metro.")],
        WS("Directions worksheet", [
            T("Give the route.", ["go straight and turn right after the market", "the station is two blocks from here"],
              ["Segue reto e vira à direita depois do mercado", "A estação fica a duas quadras daqui"]),
            T("Ask the way.", ["how do I get to the museum?", "is it far? can I walk?"],
              ["Como eu chego ao museu?", "É longe? Dá para ir a pé?"]),
        ]))),
    ("A2-U2", "A2-U2-L3", L("Marcar e remarcar por telefone",
        "On the phone, the polite opening is fixed: Alô, é a Marina? and Queria marcar um "
        "horário. Queria (I wanted) is the standard soft request — it is not a past tense, it is "
        "politeness. To move an appointment, vou ter que remarcar states the problem without "
        "apologising twice, and pode ser na terça? proposes the new time.",
        [V("marcar", "mahr-KAHR", "to book, to schedule", "verb"),
         V("remarcar", "heh-mahr-KAHR", "to reschedule", "verb"),
         V("o horário", "oo oh-RAH-ree-oo", "appointment, time slot", "noun"),
         V("ocupado", "oh-koo-PAH-doo", "busy, taken", "adjective"),
         V("a terça", "ah TEHR-sah", "Tuesday", "noun")],
        G("Booking an appointment",
          "Queria marcar um horário · pode ser na terça? · vou ter que remarcar",
          "Queria + infinitive is the polite request used at every counter and call centre. To "
          "offer a time, use pode ser: pode ser às duas? To accept, fica bom / para mim serve. "
          "Vou ter que + infinitive announces an unavoidable change.",
          [X("Alô, queria marcar um horário para sexta.", "ah-LOH, keh-REE-ah mahr-KAHR oo(n) oh-RAH-ree-oo pah-rah SEHS-tah.", "Hello, I'd like to book a time for Friday."),
           X("Pode ser às três da tarde?", "POH-jee sehr ahs treys dah TAHR-jee?", "Could it be at three in the afternoon?"),
           X("Vou ter que remarcar; aconteceu um imprevisto.", "voh teh(r) kee heh-mahr-KAHR; ah-koh(n)-teh-SEH-oo oo(n) eem-preh-VEES-too.", "I'll have to reschedule; something came up.")],
          [("Eu quero marcar, por favor.", "Eu queria marcar, por favor.", "Queria is the polite form at a counter; quero sounds like a demand."),
           ("Pode ser em terça?", "Pode ser na terça?", "Days take em + a: na terça, na sexta.")]),
        [D("Recepcionista", "Clínica São Lucas, bom dia.", "KLEE-nee-kah sow(n) LOO-kahs, boh(n) DEE-ah.", "São Lucas clinic, good morning."),
         D("Marina", "Bom dia, queria remarcar minha consulta de quinta.", "boh(n) DEE-ah, keh-REE-ah heh-mahr-KAHR MEE-nyah koh(n)-SOO-tah jee KEEN-tah.", "Good morning, I'd like to reschedule my Thursday appointment."),
         D("Recepcionista", "Claro. Pode ser na sexta, às dez?", "KLAH-roo. POH-jee sehr nah SEHS-tah, ahs days?", "Of course. Could it be Friday at ten?"),
         D("Marina", "Na sexta eu estou ocupada de manhã. Tem à tarde?", "nah SEHS-tah eh-oo es-TOH oh-koo-PAH-dah jee mah-NYAH(n). tay(n) ah TAHR-jee?", "On Friday morning I'm busy. Do you have an afternoon slot?")],
        WS("Appointments worksheet", [
            T("Make the call.", ["hello, I'd like to book a time for Friday", "could it be at three in the afternoon?"],
              ["Alô, queria marcar um horário para sexta", "Pode ser às três da tarde?"]),
            T("Change it.", ["I'll have to reschedule", "Friday morning I'm busy"],
              ["Vou ter que remarcar", "Na sexta eu estou ocupada de manhã"]),
        ]))),
    ("A2-U3", "A2-U3-L3", L("Pesos, medidas e troco",
        "At a Brazilian counter the request is me vê: me vê meio quilo de tomate. Quantity comes "
        "before the item, and the price is asked with quanto deu? or quanto é?. The troco is "
        "what comes back, and o troco está certo says it without counting in public. Decimals "
        "are said with e: nove e cinquenta.",
        [V("o quilo", "oo KEE-loo", "kilo", "noun"),
         V("a grama", "ah GRAH-mah", "gram", "noun"),
         V("o troco", "oo TROH-koo", "change", "noun"),
         V("a sacola", "ah sah-KOH-lah", "bag", "noun"),
         V("o caixa", "oo KAH-ee-shah", "checkout, till", "noun")],
        G("Buying by weight",
          "me vê meio quilo de … · quanto deu? · fica nove e cinquenta",
          "Me vê + quantity + de + item is the everyday market request. The seller answers with "
          "fica or dá: fica nove e cinquenta. A sacola, por favor asks for a bag; Brazilians "
          "often bring their own. For a fraction, meio quilo, um quarto, duzentos gramas.",
          [X("Me vê meio quilo de tomate, por favor.", "mee VEH MAY-oo KEE-loo jee toh-MAH-jee, pohr fah-VOHR.", "Can I have half a kilo of tomatoes, please?"),
           X("Quanto deu tudo?", "KWAHN-too deh-oo TOO-doo?", "How much did it all come to?"),
           X("Fica nove e cinquenta. Precisa de sacola?", "FEE-kah NOH-vee ee seen-KWEHN-tah. preh-SEE-zah jee sah-KOH-lah?", "That's nine fifty. Do you need a bag?")],
          [("Me vê meio quilo de tomates.", "Me vê meio quilo de tomate.", "After a quantity with de, the item stays in the singular."),
           ("Quanto é deu?", "Quanto deu?", "One question word: quanto deu or quanto é, not both.")]),
        [D("Feirante", "Bom dia! O que vai levar hoje?", "boh(n) DEE-ah! oo kee vey leh-VAHR OH-jee?", "Good morning! What will you take today?"),
         D("Cliente", "Me vê meio quilo de tomate e um quilo de banana.", "mee VEH MAY-oo KEE-loo jee toh-MAH-jee ee oo(n) KEE-loo jee bah-NAH-nah.", "Half a kilo of tomatoes and a kilo of bananas, please."),
         D("Feirante", "Mais alguma coisa?", "mays a-oo-GOO-mah KOH-ee-zah?", "Anything else?"),
         D("Cliente", "Só isso. Quanto deu? — Doze e trinta. — Tá certo, obrigada.", "soh EE-soo. KWAHN-too deh-oo? — DOH-zee ee TREEN-tah. — tah SEHR-too, oh-bree-GAH-dah.", "That's all. How much? — Twelve thirty. — That's right, thank you.")],
        WS("Market worksheet", [
            T("Ask for quantities.", ["half a kilo of tomatoes", "two hundred grams of cheese"],
              ["Me vê meio quilo de tomate", "Me vê duzentos gramas de queijo"]),
            T("Ask and pay.", ["how much did it all come to?", "do you need a bag?"],
              ["Quanto deu?", "Precisa de sacola?"]),
        ]))),
]

THIRD["B1"] = [
    ("B1-U1", "B1-U1-L3", L("Contar uma história: os conectores",
        "A story in Portuguese hangs on four connectors: quando opens the event, enquanto holds "
        "the background, de repente breaks it, and no fim lands it. They are placed at the head "
        "of the clause, and the verb follows the tense rule you already know — imperfeito for "
        "the scene, pretérito for the event.",
        [V("de repente", "jee heh-PEN-jee", "suddenly", "adverb"),
         V("enquanto", "ey(n)-KWAHN-too", "while", "conjunction"),
         V("no fim", "noo fee(n)", "in the end", "phrase"),
         V("afinal", "ah-fee-NAH-oo", "after all, in the end", "adverb"),
         V("então", "ey(n)-TOW(n)", "then, so", "adverb")],
        G("Linking a narrative",
          "quando + event · enquanto + scene · de repente + event · no fim + result",
          "Portuguese keeps the scene in the imperfeito and moves it with the pretérito. "
          "Connectors do not change that: enquanto eu voltava (scene), de repente começou a "
          "chover (event). No fim das contas and afinal close a story with a judgement.",
          [X("Quando eu cheguei, a festa já tinha começado.", "KWAHN-doo eh-oo sheh-GAY, ah FEHS-tah zhah TEE-nyah koh-meh-SAH-doo.", "When I arrived, the party had already started."),
           X("Enquanto eu esperava, li o jornal inteiro.", "ey(n)-KWAHN-too eh-oo es-peh-RAH-vah, lee oo zhohr-NAH-oo een-TAY-roo.", "While I was waiting, I read the whole newspaper."),
           X("No fim das contas, valeu a pena.", "noo fee(n) dahs KOHN-tahs, vah-LEH-oo ah PEH-nah.", "In the end, it was worth it.")],
          [("Enquanto eu esperei, li o jornal.", "Enquanto eu esperava, li o jornal.", "Enquanto frames a scene: imperfeito, not pretérito."),
           ("De repente, começava a chover.", "De repente, começou a chover.", "De repente introduces an event: pretérito.")]),
        [D("Ana", "Conta como foi a viagem.", "KOHN-tah KOH-moo foy ah vee-AH-zheh(n).", "Tell me how the trip went."),
         D("Rafael", "Quando eu cheguei, chovia muito, então fiquei no hotel.", "KWAHN-doo eh-oo sheh-GAY, shoh-VEE-ah MOOY-too, ey(n)-TOW(n) fee-KAY noo oh-TEH-oo.", "When I arrived it was raining hard, so I stayed in the hotel."),
         D("Ana", "E no dia seguinte?", "ee noo DEE-ah seh-GEEN-jee?", "And the next day?"),
         D("Rafael", "De repente o tempo abriu e no fim das contas deu para conhecer tudo.", "jee heh-PEN-jee oo TEH(n)-poo ah-BREE-oo ee noo fee(n) dahs KOHN-tahs deh-oo pah-rah koh-nyeh-SEHR TOO-doo.", "Suddenly the weather cleared and in the end I managed to see everything.")],
        WS("Story worksheet", [
            T("Link the scene and the event.", ["while I was waiting, I read the whole newspaper", "when I arrived, the party had already started"],
              ["Enquanto eu esperava, li o jornal inteiro", "Quando eu cheguei, a festa já tinha começado"]),
            T("Close the story.", ["suddenly it started to rain", "in the end, it was worth it"],
              ["De repente começou a chover", "No fim das contas, valeu a pena"]),
        ]))),
    ("B1-U2", "B1-U2-L3", L("Reunião: concordar, discordar e propor",
        "A Brazilian meeting disagrees in two steps: first the other position is named (entendo "
        "o seu ponto), then the disagreement arrives with a hedge (não sei se concordo, tenho "
        "uma ressalva). A proposal is put with que tal or podemos: que tal começarmos pela "
        "pauta? The proposal form decides who has to answer.",
        [V("a reunião", "ah heh-oo-nee-OW(n)", "meeting", "noun"),
         V("a pauta", "ah POW-tah", "agenda", "noun"),
         V("o prazo", "oo PRAH-zoo", "deadline", "noun"),
         V("a proposta", "ah proh-POHS-tah", "proposal", "noun"),
         V("o acordo", "oo ah-KOHR-doo", "agreement", "noun")],
        G("Disagreeing and proposing",
          "entendo o ponto, mas … · tenho uma ressalva · que tal + infinitive",
          "Direct disagreement is softened by naming what you accept first. Tenho uma ressalva "
          "announces a partial objection without rejecting the plan. Que tal and podemos both "
          "propose; podemos commits the group more, que tal leaves the decision open.",
          [X("Entendo o ponto, mas tenho uma ressalva sobre o prazo.", "en-TEN-doo oo POHN-too, mahs teh-nyoo OO-mah heh-SAH-oo-vah SOH-bree oo PRAH-zoo.", "I see the point, but I have a reservation about the deadline."),
           X("Que tal começarmos pela pauta?", "kee TA-oo koh-meh-SAHR-moos PEH-lah POW-tah?", "How about we start with the agenda?"),
           X("Podemos fechar um acordo até sexta.", "poh-DEH-moos feh-SHAHR oo(n) ah-KOHR-doo ah-TEH SEHS-tah.", "We can close an agreement by Friday.")],
          [("Não sei se eu não concordo.", "Não sei se concordo.", "The double negative contradicts the hedge."),
           ("Que tal começar pela pauta?", "Que tal começarmos pela pauta?", "Que tal takes the personal infinitive quando the subject is we.")]),
        [D("Paulo", "Acho que dá para entregar na quinta.", "AH-shoo kee dah pah-rah en-treh-GAHR nah KEEN-tah.", "I think we can deliver on Thursday."),
         D("Marina", "Entendo, mas tenho uma ressalva: falta a revisão.", "en-TEN-doo, mahs teh-nyoo OO-mah heh-SAH-oo-vah: FAH-oo-tah ah heh-vee-ZOW(n).", "I see, but I have a reservation: the review is missing."),
         D("Paulo", "Justo. Que tal sexta de manhã, então?", "ZHOOS-too. kee TA-oo SEHS-tah jee mah-NYAH(n), ey(n)-TOW(n)?", "Fair. How about Friday morning, then?"),
         D("Marina", "Combinado. Fecho o acordo e mando a pauta hoje.", "koh(n)-bee-NAH-doo. FEH-shoo oo ah-KOHR-doo ee MAHN-doo ah POW-tah OH-jee.", "Agreed. I'll close the deal and send the agenda today.")],
        WS("Meeting worksheet", [
            T("Disagree politely.", ["I understand, but I have a reservation about the deadline", "I'm not sure I agree"],
              ["Entendo, mas tenho uma ressalva sobre o prazo", "Não sei se concordo"]),
            T("Propose.", ["how about we start with the agenda?", "we can close an agreement by Friday"],
              ["Que tal começarmos pela pauta?", "Podemos fechar um acordo até sexta"]),
        ]))),
    ("B1-U3", "B1-U3-L3", L("Relatar o que alguém disse",
        "When you repeat what someone said, the tense moves back: ela disse que ia chegar tarde, "
        "ele falou que tinha visto o relatório. A yes/no question becomes se: perguntou se dava "
        "tempo. The reporting verb keeps its own tense, and that is what tells the listener when "
        "the original conversation happened.",
        [V("relatar", "heh-lah-TAHR", "to report", "verb"),
         V("avisar", "ah-vee-ZAHR", "to let someone know", "verb"),
         V("comentar", "koh-men-TAHR", "to mention, to comment", "verb"),
         V("garantir", "gah-rahn-TEER", "to guarantee", "verb"),
         V("prometer", "proh-meh-TEHR", "to promise", "verb")],
        G("Reported speech",
          "ela disse que ia chegar · ele falou que tinha visto · perguntou se dava",
          "The tenses step back one: vai → ia, viu → tinha visto, dá → dava. The person shifts to "
          "the third person (eu vou → ela disse que ia). For a question, use perguntou se for "
          "yes/no and perguntou quando/onde for an information question.",
          [X("Ela disse que ia chegar tarde, mas chegou cedo.", "EH-lah DEE-see kee EE-ah sheh-GAHR TAHR-jee, mahs sheh-GOH SEH-doo.", "She said she would arrive late, but she arrived early."),
           X("Ele falou que tinha visto o relatório.", "EH-lee fah-LOH kee TEE-nyah VEES-too oo heh-lah-TOH-ree-oo.", "He said he had seen the report."),
           X("Ela perguntou se dava tempo de entregar hoje.", "EH-lah pehr-goon-TOH see DAH-vah TEH(n)-poo jee en-treh-GAHR OH-jee.", "She asked whether there was time to deliver today.")],
          [("Ela disse que vai chegar ontem.", "Ela disse que ia chegar ontem.", "A past report moves the tense back: vai becomes ia."),
           ("Ele falou que eu tinha visto o relatório.", "Ele falou que ele tinha visto o relatório.", "Keep the reported subject in the third person.")]),
        [D("Ana", "O que o cliente falou?", "oo kee oo klee-EN-jee fah-LOH?", "What did the client say?"),
         D("Rafael", "Falou que tinha gostado da proposta e que ia responder hoje.", "fah-LOH kee TEE-nyah gohs-TAH-doo dah proh-POHS-tah ee kee EE-ah hes-pohn-DEHR OH-jee.", "He said he had liked the proposal and would reply today."),
         D("Ana", "Ele perguntou alguma coisa sobre o prazo?", "EH-lee pehr-goon-TOH a-oo-GOO-mah KOH-ee-zah SOH-bree oo PRAH-zoo?", "Did he ask anything about the deadline?"),
         D("Rafael", "Perguntou se dava para adiantar uma semana.", "pehr-goon-TOH see DAH-vah pah-rah ah-jee-ahn-TAHR OO-mah seh-MAH-nah.", "He asked whether it was possible to bring it forward a week.")],
        WS("Reporting worksheet", [
            T("Report the words.", ["she said she would arrive late", "he said he had seen the report"],
              ["Ela disse que ia chegar tarde", "Ele falou que tinha visto o relatório"]),
            T("Report the question.", ["she asked whether there was time to deliver today", "he asked if it was possible to bring it forward"],
              ["Ela perguntou se dava tempo de entregar hoje", "Ele perguntou se dava para adiantar"]),
        ]))),
]


THIRD["B2"] = [
    ("B2-U1", "B2-U1-L3", L("Hipóteses no passado: se tivesse…",
        "An unreal past condition has two halves that must agree: se + imperfect subjunctive "
        "(tivesse, fosse, pudesse) and the conditional with teria + participle (teria feito, "
        "teria sido). Swap either half and the sentence stops being an unreal condition — it "
        "becomes a promise about the future or a plain statement of fact.",
        [V("a hipótese", "ah ee-POH-teh-zee", "hypothesis", "noun"),
         V("a consequência", "ah koh(n)-seh-KWEHN-see-ah", "consequence", "noun"),
         V("supor", "soo-POHR", "to suppose", "verb"),
         V("arrepender-se", "ah-heh-pen-DEHR-see", "to regret", "verb"),
         V("caso", "KAH-zoo", "case, instance", "noun")],
        G("Unreal past conditions",
          "se tivesse sabido, teria avisado · caso tivesse tempo, teria ido",
          "Se + imperfeito do subjuntivo states the unreal past; the other half takes teria + "
          "participle. Caso is the formal variant and also takes the subjunctive (caso tivesse). "
          "The order can be reversed with no change of meaning, and a comma marks the swap.",
          [X("Se eu tivesse sabido, teria avisado antes.", "see eh-oo tee-VEHS-see sah-BEE-doo, teh-REE-ah ah-vee-ZAH-doo AH(n)-jees.", "If I had known, I would have warned you earlier."),
           X("Caso houvesse prazo, teríamos entregue a versão completa.", "KAH-zoo oh-VEHS-see PRAH-zoo, teh-REE-ah-moos en-treh-GEH ah vehr-ZOW(n) koh(n)-PLEH-tah.", "Had there been a deadline, we would have delivered the full version."),
           X("Teria sido melhor esperar, mas a decisão já estava tomada.", "teh-REE-ah SEE-doo meh-LYOHR es-peh-RAHR, mahs ah deh-see-ZOW(n) zhah es-TAH-vah toh-MAH-dah.", "It would have been better to wait, but the decision was already made.")],
          [("Se eu teria sabido, teria avisado.", "Se eu tivesse sabido, teria avisado.", "The se half takes the imperfect subjunctive, never the conditional."),
           ("Se eu tivesse sabido, avisaria antes.", "Se eu tivesse sabido, teria avisado antes.", "Teria + participle is the form for an unreal past result.")]),
        [D("Ana", "Você teria feito diferente?", "voh-SEH teh-REE-ah FEH-too jee-feh-REHN-jee?", "Would you have done it differently?"),
         D("Rafael", "Se eu tivesse visto os números antes, teria pedido mais prazo.", "see eh-oo tee-VEHS-see VEES-too oos NOO-meh-roos AH(n)-jees, teh-REE-ah peh-DEE-doo mays PRAH-zoo.", "If I had seen the numbers earlier, I would have asked for more time."),
         D("Ana", "E caso tivessem negado?", "ee KAH-zoo tee-VEHS-sem neh-GAH-doo?", "And had they refused?"),
         D("Rafael", "Aí teríamos refeito a proposta do zero.", "ah-EE teh-REE-ah-moos heh-FAY-too ah proh-POHS-tah doo ZEH-roo.", "Then we would have redone the proposal from scratch.")],
        WS("Hypothesis worksheet", [
            T("Build the unreal condition.", ["if I had known, I would have warned you earlier", "had there been a deadline, we would have delivered"],
              ["Se eu tivesse sabido, teria avisado antes", "Caso houvesse prazo, teríamos entregue"]),
            T("Close the hypothesis.", ["it would have been better to wait", "then we would have redone the proposal"],
              ["Teria sido melhor esperar", "Aí teríamos refeito a proposta"]),
        ]))),
    ("B2-U2", "B2-U2-L3", L("Argumentar por escrito: conectores formais",
        "Written argument in Portuguese moves by connectives that carry a claim about the "
        "relation between ideas: portanto concludes, contudo contrasts, na medida em que "
        "explains by degree, dado que supplies a premise. A paragraph with four connectives of "
        "the same type reads as a list; a paragraph that varies them reads as an argument.",
        [V("portanto", "pohr-TAHN-too", "therefore", "adverb"),
         V("contudo", "koh(n)-TOO-doo", "however", "adverb"),
         V("dado que", "DAH-doo kee", "given that", "conjunction"),
         V("além disso", "ah-LEH(n) DEE-soo", "besides that", "phrase"),
         V("visto que", "VEES-too kee", "seeing that", "conjunction"),
         V("na medida em que", "nah meh-DEE-dah ey(n) kee", "to the extent that", "conjunction")],
        G("Connectives of argument",
          "dado que … · portanto … · contudo … · na medida em que …",
          "Dado que and visto que present a premise the reader is expected to accept. Portanto "
          "and por conseguinte draw the conclusion. Contudo, no entanto and ainda assim mark the "
          "turn. Na medida em that is a claim of proportion, not a synonym of porque — it says "
          "one thing grows with the other.",
          [X("Dado que a amostra é pequena, os resultados pedem cautela.", "DAH-doo kee ah ah-MOHS-trah eh peh-KEH-nah, oos heh-zoo-oo-TAH-doos PEH-jay(n) kow-TEH-lah.", "Given that the sample is small, the results call for caution."),
           X("Os dados cresceram; contudo, o ritmo segue desigual.", "oos DAH-doos kreh-SEH-rah(n); koh(n)-TOO-doo, oo HEETCH-moo SEH-gee deh-zee-GOO-ah-oo.", "The figures grew; however, the pace remains uneven."),
           X("O acesso melhora na medida em que a rede chega ao interior.", "oo ah-SEH-soo meh-LYOH-rah nah meh-DEE-dah ey(n) kee ah HEH-jee SHEH-gah ah-oo een-teh-ree-OHR.", "Access improves to the extent that the network reaches the interior.")],
          [("Porque a amostra é pequena, portanto os resultados pedem cautela.", "Dado que a amostra é pequena, os resultados pedem cautela.", "Use one premise marker and one conclusion marker, not two premises."),
           ("O acesso melhora na medida que a rede chega.", "O acesso melhora na medida em que a rede chega.", "The fixed form is na medida em que.")]),
        [D("Redatora", "O parágrafo ficou pesado.", "oo pah-RAH-grah-foo fee-KOH peh-ZAH-doo.", "The paragraph came out heavy."),
         D("Editor", "É porque há quatro conectores de conclusão.", "eh pohr-KEH ah KWAH-troo koh-neh-KTOH-rees jee koh(n)-kloo-ZOW(n).", "That's because there are four conclusion connectives."),
         D("Redatora", "Então deixo dois e troco um por contudo?", "en-TOW(n) DAY-shoo doys ee TRoh-koo oo(n) pohr koh(n)-TOO-doo?", "So I keep two and swap one for contudo?"),
         D("Editor", "Isso. E marque a ressalva com ainda assim, que não fecha a questão.", "EE-soo. ee mahr-KEE ah heh-SAH-oo-vah koh(n) ah-EEN-dah ah-SEE(n), kee now(n) FEH-shah ah kes-TOW(n).", "Yes. And mark the reservation with ainda assim, which doesn't close the question.")],
        WS("Argument worksheet", [
            T("Mark the premise.", ["given that the sample is small, the results call for caution", "to the extent that the network reaches the interior"],
              ["Dado que a amostra é pequena, os resultados pedem cautela", "na medida em que a rede chega ao interior"]),
            T("Mark the turn.", ["the figures grew; however, the pace remains uneven", "even so, the question is not closed"],
              ["Os dados cresceram; contudo, o ritmo segue desigual", "Ainda assim, a questão não está fechada"]),
        ]))),
    ("B2-U3", "B2-U3-L3", L("Cinema e crítica cultural",
        "A cultural review is an argument with a stated scope. The frame o que me interessa é "
        "names what the critic is reading for; peca por + infinitive names the defect without "
        "insult; the concession embora reconheça keeps the positive in view. A review that only "
        "approves or only condemns has not yet said what it is looking at.",
        [V("o roteiro", "oo hoh-TAY-ree-oo", "script, screenplay", "noun"),
         V("a atuação", "ah ah-too-ah-SOW(n)", "acting, performance", "noun"),
         V("a cena", "ah SEH-nah", "scene", "noun"),
         V("o enredo", "oo en-REH-doo", "plot", "noun"),
         V("pecar por", "peh-KAHR pohr", "to fall short by", "verb")],
        G("Reviewing a work",
          "o que me interessa é … · peca por + infinitive · embora reconheça …",
          "The frame o que me interessa é + noun clause shifts the review to what the critic "
          "actually read. Peca por + infinitive names a fault precisely: peca por explicar demais. "
          "Embora + subjunctive concedes the other side without abandoning the thesis.",
          [X("O que me interessa no filme é a relação entre pai e filha.", "oo kee mee een-teh-REH-sah noo FEE-oo-mee eh ah heh-lah-SOW(n) EH(n)-tree PAH-ee ee FEE-lyah.", "What interests me in the film is the relationship between father and daughter."),
           X("O roteiro peca por explicar o que a cena já mostra.", "oo hoh-TAY-ree-oo PEH-kah pohr es-plee-KAHR oo kee ah SEH-nah zhah MOH-trah.", "The script falls short by explaining what the scene already shows."),
           X("Embora reconheça o mérito da atuação, a crítica mantém a ressalva.", "ey(n)-BOH-rah heh-koh-NYEH-sah oo MEH-ree-too dah ah-too-ah-SOW(n), ah KREE-tee-kah mahn-TEH(n) ah heh-SAH-oo-vah.", "Although it acknowledges the acting, the review keeps its reservation.")],
          [("O filme peca por que explica demais.", "O filme peca por explicar demais.", "Peca por takes a bare infinitive, with no que."),
           ("Embora reconhece o mérito, mantém a ressalva.", "Embora reconheça o mérito, mantém a ressalva.", "Embora takes the subjunctive: reconheça.")]),
        [D("Crítica", "O roteiro peca por explicar o final duas vezes.", "oo hoh-TAY-ree-oo PEH-kah pohr es-plee-KAHR oo fee-NAH-oo DOO-ahs VEH-zees.", "The script falls short by explaining the ending twice."),
         D("Diretor", "Embora reconheça isso, a escolha foi consciente.", "ey(n)-BOH-rah heh-koh-NYEH-sah EE-soo, ah es-KOH-lyah foy koh(n)-shee-EHN-jee.", "Although I acknowledge that, the choice was deliberate."),
         D("Crítica", "Entendo. O que me interessa é como a cena constrói a confiança.", "en-TEN-doo. oo kee mee een-teh-REH-sah eh KOH-moo ah SEH-nah koh(n)-STROY ah koh(n)-fee-AHN-sah.", "I understand. What interests me is how the scene builds trust."),
         D("Diretor", "Aí concordamos: o filme depende do silêncio, não do diálogo.", "ah-EE koh(n)-kohr-DAH-moos: oo FEE-oo-mee jee-PEH(n)-jee doo see-LEHN-see-oo, now(n) doo jee-AH-loh-goo.", "Then we agree: the film depends on silence, not on dialogue.")],
        WS("Review worksheet", [
            T("State the frame.", ["what interests me in the film is the relationship between father and daughter", "the script falls short by explaining too much"],
              ["O que me interessa no filme é a relação entre pai e filha", "O roteiro peca por explicar demais"]),
            T("Concede and keep the thesis.", ["although it acknowledges the acting, the review keeps its reservation", "the film depends on silence, not on dialogue"],
              ["Embora reconheça o mérito da atuação, a crítica mantém a ressalva", "O filme depende do silêncio, não do diálogo"]),
        ]))),
]

THIRD["C1"] = [
    ("pt-c1-u1", "pt-c1-l7", L("Registro jornalístico: a manchete e o lide",
        "A Brazilian news text is built in two moves: the manchete makes a claim in the present "
        "and without attribution, and the lide answers what, who, when and where in the first "
        "sentence, with the source named. Hedging is explicit — teria, segundo, de acordo com — "
        "and the passive with ser keeps the agent out when the paper does not want to name one.",
        [V("a manchete", "ah mah-NYEH-jee", "headline", "noun"),
         V("o lide", "oo LEE-jee", "lede, opening paragraph", "noun"),
         V("a fonte", "ah FOHN-jee", "source", "noun"),
         V("apurar", "ah-poo-RAHR", "to verify, to investigate", "verb"),
         V("ressalvar", "heh-sah-oo-VAHR", "to qualify, to note as an exception", "verb")],
        G("News register",
          "manchete no presente · lide com fonte e data · teria for an unconfirmed claim",
          "The headline uses the present (Governo anuncia) even for yesterday's event. The lede "
          "names the source and the date, and marks anything unconfirmed with the conditional "
          "teria or with the phrase segundo a apuração. Ser + participle removes the agent: "
          "foram revisados os dados.",
          [X("Governo anuncia pacote e sindicatos pedem detalhes.", "goo-VEHR-noo ah-NOON-see-ah pah-KOH-tee ee seen-jee-KAH-toos PEH-jay(n) deh-TAH-lyoos.", "Government announces package and unions ask for details."),
           X("Segundo o instituto, o índice teria caído 2% em setembro.", "seh-GOON-doo oo een-stee-TOO-too, oo EEN-jee-see teh-REE-ah kah-EE-doo DOYS pohr SEHN-too ey(n) seh-TEH(n)-broo.", "According to the institute, the index reportedly fell 2% in September."),
           X("Foram revisados os dados de nove estados.", "FOH-rah(n) heh-vee-ZAH-doos oos DAH-doos jee NOH-vee es-TAH-doos.", "The data from nine states were revised.")],
          [("Segundo o instituto, o índice caiu, dizem.", "Segundo o instituto, o índice teria caído.", "Two attribution markers in one clause double the distance; use one."),
           ("Os dados foram revisado.", "Os dados foram revisados.", "The participle agrees with the subject: revisados.")]),
        [D("Editora", "A manchete está no presente e o fato é de ontem?", "ah mah-NYEH-jee es-TAH noo preh-ZEN-jee ee oo FAH-too eh jee OH(n)-tay(n)?", "The headline is in the present and the fact is from yesterday?"),
         D("Repórter", "Está, por praxe. O lide diz ontem à noite e nomeia o instituto.", "es-TAH, pohr PRAH-shee. oo LEE-jee dees OH(n)-tay(n) ah NOY-jee ee noh-may-ah oo een-stee-TOO-too.", "It is, as standard practice. The lede says last night and names the institute."),
         D("Editora", "E a queda de 2%?", "ee ah KEH-dah jee DOYS pohr SEHN-too?", "And the 2% fall?"),
         D("Repórter", "Fica com teria, porque a planilha não é oficial.", "FEE-kah koh(n) teh-REE-ah, pohr-KEH ah plah-NEE-lyah now(n) eh oh-fee-see-AH-oo.", "It stays with teria, because the spreadsheet is not official.")],
        WS("News register worksheet", [
            T("Write the lede.", ["according to the institute, the index reportedly fell 2% in September", "the data from nine states were revised"],
              ["Segundo o instituto, o índice teria caído 2% em setembro", "Foram revisados os dados de nove estados"]),
            T("Mark the distance from the claim.", ["the newspaper had access to a spreadsheet that is not official", "the union had not commented by closing time"],
              ["O jornal teve acesso a uma planilha que não é oficial", "O sindicato não se manifestou até o fechamento"]),
        ]))),
    ("pt-c1-u2", "pt-c1-l8", L("Negociação: proposta condicional e ressalva",
        "In a negotiation, the conditional is not politeness but distance: faríamos, poderíamos, "
        "conviria leave room for the other side to move. The reservation is stated with a scope "
        "word (desde que, salvo se, na condição de que) followed by the subjunctive, and the "
        "concession names what is already agreed before asking for anything.",
        [V("desde que", "DEHS-jee kee", "provided that", "conjunction"),
         V("salvo se", "SAH-oo-voo see", "unless", "conjunction"),
         V("a contrapartida", "ah kohn-trah-pahr-TEE-dah", "counterpart, something in return", "noun"),
         V("resguardar", "hes-gwah-RDAHR", "to safeguard", "verb"),
         V("viabilizar", "vee-ah-bee-lee-ZAHR", "to make feasible", "verb")],
        G("Conditional proposals",
          "faríamos … desde que … · salvo se … · na condição de que …",
          "Desde que, salvo se and na condição de que all take the subjunctive: desde que o prazo "
          "seja mantido. The conditional faríamos keeps the proposal open; the first person plural "
          "speaks for the institution rather than the speaker. A contrapartida is what makes the "
          "concession reciprocal and is named before the request.",
          [X("Poderíamos aceitar a data, desde que o escopo seja mantido.", "poh-deh-REE-ah-moos ah-seh-TAHR ah DAH-tah, DEHS-jee kee oo es-KOH-poo SEH-zhah mahn-TEE-doo.", "We could accept the date, provided the scope is kept."),
           X("Salvo se houver revisão, o texto segue para publicação.", "SAH-oo-voo see oh-VEHR heh-vee-ZOW(n), oo TEHS-too SEH-gee pah-rah poo-blee-kah-SOW(n).", "Unless there is a revision, the text goes to publication."),
           X("Como contrapartida, pedimos que a revisão seja conjunta.", "KOH-moo kohn-trah-pahr-TEE-dah, peh-JEE-moos kee ah heh-vee-ZOW(n) SEH-zhah koh(n)-ZHOON-tah.", "As a counterpart, we ask that the review be joint.")],
          [("Desde que o prazo é mantido, aceitamos.", "Desde que o prazo seja mantido, aceitamos.", "Desde que takes the subjunctive: seja."),
           ("Salvo se houver revisão, salvo se o texto segue.", "Salvo se houver revisão, o texto segue.", "One condition per sentence; the second clause states the consequence.")]),
        [D("Fornecedora", "Poderíamos fechar em março.", "poh-deh-REE-ah-moos feh-SHAHR ey(n) MAHR-soo.", "We could close in March."),
         D("Cliente", "Desde que a entrega parcial seja garantida, aceito.", "DEHS-jee kee ah en-treh-GAH pahr-see-AH-oo SEH-zhah gah-rahn-TEE-dah, ah-SAY-too.", "Provided the partial delivery is guaranteed, I accept."),
         D("Fornecedora", "Como contrapartida, pedimos reajuste em abril.", "KOH-moo kohn-trah-pahr-TEE-dah, peh-JEE-moos heh-ah-ZHOOS-jee ey(n) ah-BREE-oo.", "As a counterpart, we ask for an adjustment in April."),
         D("Cliente", "Salvo se o índice cair, o reajuste fica de pé.", "SAH-oo-voo see oo EEN-jee-see kah-EER, oo heh-ah-ZHOOS-jee FEE-kah jee PEH.", "Unless the index falls, the adjustment stands.")],
        WS("Negotiation worksheet", [
            T("Propose with a condition.", ["we could accept the date, provided the scope is kept", "unless there is a revision, the text goes to publication"],
              ["Poderíamos aceitar a data, desde que o escopo seja mantido", "Salvo se houver revisão, o texto segue para publicação"]),
            T("Ask for the counterpart.", ["as a counterpart, we ask that the review be joint", "the adjustment stands unless the index falls"],
              ["Como contrapartida, pedimos que a revisão seja conjunta", "O reajuste fica de pé salvo se o índice cair"]),
        ]))),
    ("pt-c1-u3", "pt-c1-l9", L("Síntese de fontes divergentes",
        "A synthesis is not a summary of two texts but a third statement that accounts for both: "
        "each source is attributed with its scope (segundo, para, de acordo com), the divergence "
        "is named as a difference of method or scale rather than of opinion, and the conclusion "
        "declares its own limits. Na medida em que is the workhorse — it says one claim holds only "
        "as far as the other goes.",
        [V("divergir", "jee-vehr-ZHEER", "to diverge", "verb"),
         V("convergir", "kohn-vehr-ZHEER", "to converge", "verb"),
         V("o escopo", "oo es-KOH-poo", "scope", "noun"),
         V("a metodologia", "ah meh-toh-doh-loh-ZHEE-ah", "methodology", "noun"),
         V("o limite", "oo lee-MEE-jee", "limit, boundary", "noun")],
        G("Synthesising sources",
          "segundo A … · para B … · na medida em que … · o que os dados não permitem concluir",
          "Each source keeps its own preposition of attribution, and the divergence is explained "
          "before it is judged. Na medida em que connects the two claims as a matter of degree. "
          "A synthesis ends by stating what the evidence does not establish, which is what "
          "separates it from an opinion piece.",
          [X("Segundo o instituto, o acesso cresceu; para o sindicato, a média esconde a desigualdade.", "seh-GOON-doo oo een-stee-TOO-too, oo ah-SEH-soo kreh-SEH-oo; PAH-rah oo seen-jee-KAH-too, ah MEH-jee-ah es-KOHN-jee ah deh-zee-goo-ah-oo-DAH-jee.", "According to the institute, access grew; for the union, the average hides the inequality."),
           X("Os dois números convergem na medida em que medem redes distintas.", "oos doys NOO-meh-roos koh(n)-VEHR-zheh(n) nah meh-DEE-dah ey(n) kee MEH-jay(n) HEH-jee jee-STEEN-tahs.", "The two figures converge to the extent that they measure different networks."),
           X("O que os dados não permitem concluir é a causa da queda.", "oo kee oos DAH-doos now(n) pehr-MEE-tay(n) koh(n)-kloo-EER eh ah KOW-zah dah KEH-dah.", "What the data do not allow us to conclude is the cause of the fall.")],
          [("Os dados convergem que medem redes distintas.", "Os dados convergem na medida em que medem redes distintas.", "Convergir needs its frame: na medida em que."),
           ("A metodologia divergem entre os estudos.", "As metodologias divergem entre os estudos.", "Plural subject and plural verb.")]),
        [D("Parecerista", "Os números divergem?", "oos NOO-meh-roos jee-VEHR-zheh(n)?", "Do the numbers diverge?"),
         D("Autora", "Na medida em que medem redes distintas, sim.", "nah meh-DEE-dah ey(n) kee MEH-jay(n) HEH-jee jee-STEEN-tahs, see(n).", "Insofar as they measure different networks, yes."),
         D("Parecerista", "E o que os dados não permitem concluir?", "ee oo kee oos DAH-doos now(n) pehr-MEE-tay(n) koh(n)-kloo-EER?", "And what do the data not allow us to conclude?"),
         D("Autora", "A causa da queda. Só o ritmo e a distribuição.", "ah KOW-zah dah KEH-dah. soh oo HEETCH-moo ee ah jees-tree-boo-ee-SOW(n).", "The cause of the fall. Only the pace and the distribution.")],
        WS("Synthesis worksheet", [
            T("Attribute the sources.", ["according to the institute, the access grew", "for the union, the average hides the inequality"],
              ["Segundo o instituto, o acesso cresceu", "para o sindicato, a média esconde a desigualdade"]),
            T("State the limit.", ["what the data do not allow us to conclude is the cause of the fall", "the two figures converge to the extent that they measure different networks"],
              ["O que os dados não permitem concluir é a causa da queda", "Os dois números convergem na medida em que medem redes distintas"]),
        ]))),
]

THIRD["C2"] = [
    ("pt-c2-u1", "pt-c2-l7", L("Foco e pressuposição em textos densos",
        "Information structure is a choice about what the reader already knows. Clefting (é … "
        "que) puts the new information at the end; fronting (quanto ao prazo, …) suspends the "
        "topic before the claim; the choice between them decides which part of the sentence the "
        "reader will argue with. Presupposition is carried by the definite article and by verbs "
        "like insistir and reconhecer, which take the existence of their object for granted.",
        [V("a ênfase", "ah EH(n)-fah-zee", "emphasis", "noun"),
         V("o realce", "oo heh-AH-see", "highlighting", "noun"),
         V("pressupor", "preh-soo-POHR", "to presuppose", "verb"),
         V("insistir em", "een-sees-TEER ey(n)", "to insist on", "verb"),
         V("reconhecer", "heh-koh-nyeh-SEHR", "to acknowledge", "verb")],
        G("Focus and presupposition",
          "é … que … · quanto a … · o fato de … · insistir em que + subjunctive",
          "The cleft é … que moves the focus to the end: é o ritmo que preocupa. Quanto a opens a "
          "topic without asserting anything about it. O fato de presupposes the fact and can "
          "shift the argument to its explanation. Insistir em que takes the subjunctive because "
          "the insistence is a stance, not a report.",
          [X("Não é a queda que preocupa, é o ritmo.", "now(n) eh ah KEH-dah kee preh-oh-KOO-pah, eh oo HEETCH-moo.", "It is not the fall that worries us, it is the pace."),
           X("Quanto ao prazo, a decisão cabe ao comitê.", "KWAHN-too ah-oo PRAH-zoo, ah deh-see-ZOW(n) KAH-bee ah-oo koh-mee-TEH.", "As for the deadline, the decision lies with the committee."),
           X("O autor insiste em que não houve omissão.", "oo ah-oo-TOHR een-SEES-jee ey(n) kee now(n) oh-VEH oh-mee-SOW(n).", "The author insists that there was no omission.")],
          [("É o ritmo que preocupa, é o ritmo.", "O que preocupa é o ritmo.", "One focus construction per sentence; the cleft already carries the emphasis."),
           ("Ele insiste que não houve omissão.", "Ele insiste em que não houve omissão.", "Insistir takes em before the clause.")]),
        [D("Editor", "O que o texto quer destacar?", "oo kee oo TEHS-too KEH(r) des-tah-KAHR?", "What does the text want to highlight?"),
         D("Autora", "Não é a queda que preocupa, é o ritmo.", "now(n) eh ah KEH-dah kee preh-oh-KOO-pah, eh oo HEETCH-moo.", "It is not the fall that worries us, it is the pace."),
         D("Editor", "Quanto ao prazo, quem decide?", "KWAHN-too ah-oo PRAH-zoo, key(n) deh-SEE-jee?", "As for the deadline, who decides?"),
         D("Autora", "O comitê. E o texto pressupõe isso desde o primeiro parágrafo.", "oo koh-mee-TEH. ee oo TEHS-too preh-soo-POH(n)-yee EE-soo DEHS-jee oo preh-MAY-roo pah-RAH-grah-foo.", "The committee. And the text presupposes that from the first paragraph.")],
        WS("Focus worksheet", [
            T("Move the focus.", ["it is not the fall that worries us, it is the pace", "as for the deadline, the decision lies with the committee"],
              ["Não é a queda que preocupa, é o ritmo", "Quanto ao prazo, a decisão cabe ao comitê"]),
            T("Name the presupposition.", ["the author insists that there was no omission", "the text presupposes that from the first paragraph"],
              ["O autor insiste em que não houve omissão", "O texto pressupõe isso desde o primeiro parágrafo"]),
        ]))),
    ("pt-c2-u2", "pt-c2-l8", L("Reescrita: do literário ao institucional",
        "Rewriting across registers is a controlled loss. The literary sentence keeps its rhythm "
        "and its ambiguity; the institutional version states the claim, its agent and its "
        "consequence, and drops whatever cannot be attributed. A good rewrite says what it gave "
        "up — an image, a hedge, a subordinate clause — instead of pretending the two texts are "
        "the same document in two fonts.",
        [V("a reescrita", "ah heh-es-KREE-tah", "rewriting", "noun"),
         V("o registro", "oo heh-ZHEES-troo", "register", "noun"),
         V("suprimir", "soo-pree-MEER", "to omit, to suppress", "verb"),
         V("equivaler", "eh-kee-vah-LEHR", "to be equivalent", "verb"),
         V("o teor", "oo teh-OHR", "tenor, content of a text", "noun")],
        G("Rewriting between registers",
          "manter o teor · suprimir a imagem · equivaler a … em registro …",
          "The rewrite keeps the teor (the claim) and changes the packaging: verbs become "
          "nominal, the agent is named or removed on purpose, and figurative language is replaced "
          "by its literal content. Equivaler a marks what is claimed to be preserved, and the "
          "honest rewrite states what was not.",
          [X("A frase literária sugere; a versão institucional afirma e atribui.", "ah FRAH-zee lee-teh-RAH-ree-ah soo-ZHEH-ree; ah vehr-ZOW(n) een-stee-too-see-oh-NAH-oo ah-FEER-mah ee ah-tree-BOO-ee.", "The literary sentence suggests; the institutional version asserts and attributes."),
           X("A reescrita manteve o teor e suprimiu duas imagens.", "ah heh-es-KREE-tah mahn-TEH-vay oo teh-OHR ee soo-pree-MEE-oo DOO-ahs ee-MAH-zheh(n)s.", "The rewrite kept the content and dropped two images."),
           X("Isso equivale a dizer que o dado não foi verificado.", "EE-soo eh-kee-VAH-lee ah jee-ZEHR kee oo DAH-doo now(n) foy veh-ree-fee-KAH-doo.", "That amounts to saying the datum was not verified.")],
          [("A reescrita manteve o teor e suprimiu, porém o sentido ficou igual.", "A reescrita manteve o teor e suprimiu duas imagens.", "Say what changed; the conjunction cannot claim equivalence by itself."),
           ("Isso equivale dizer que o dado não foi verificado.", "Isso equivale a dizer que o dado não foi verificado.", "Equivaler a takes the preposition a.")]),
        [D("Coordenadora", "O comunicado ficou fiel ao texto original?", "oo koh-moo-nee-KAH-doo fee-KOH fee-EH-oo ah-oo TEHS-too oh-ree-zhee-NAH-oo?", "Did the statement stay faithful to the original text?"),
         D("Redator", "Manteve o teor, mas suprimiu as imagens.", "mahn-TEH-vay oo teh-OHR, mahs soo-pree-MEE-oo ahs ee-MAH-zheh(n)s.", "It kept the content but dropped the images."),
         D("Coordenadora", "Então não equivale ao original.", "en-TOW(n) now(n) eh-kee-VAH-lee ah-oo oh-ree-zhee-NAH-oo.", "So it is not equivalent to the original."),
         D("Redator", "Concordo. Vou declarar isso na nota de rodapé.", "koh(n)-KOHR-doo. voh deh-kah-LAH-ah EE-soo nah NOH-tah jee hoh-dah-PEH.", "I agree. I'll state that in the footnote.")],
        WS("Rewrite worksheet", [
            T("Keep the content, change the packaging.", ["the rewrite kept the content and dropped two images", "that amounts to saying the datum was not verified"],
              ["A reescrita manteve o teor e suprimiu duas imagens", "Isso equivale a dizer que o dado não foi verificado"]),
            T("State the loss.", ["the statement kept the content but dropped the images", "the literary sentence suggests; the institutional version asserts"],
              ["O comunicado manteve o teor, mas suprimiu as imagens", "A frase literária sugere; a versão institucional afirma"]),
        ]))),
    ("pt-c2-u3", "pt-c2-l9", L("Mediação cultural sem clichê",
        "Explaining Brazil to a foreign reader is where good Portuguese most often becomes a "
        "cliché: carnaval, futebol, alegria. A mediator refuses the summary and works by "
        "comparison with stated limits — no Brasil, ao contrário do que se diz, … ; a diferença "
        "não é de essência, é de arranjo institucional. The task is to keep both sides visible "
        "and to mark every generalisation as one.",
        [V("o clichê", "oo klee-SHEH", "cliché", "noun"),
         V("a generalização", "ah zheh-neh-rah-lee-zah-SOW(n)", "generalisation", "noun"),
         V("o arranjo", "oo ah-HAH(n)-zhoo", "arrangement", "noun"),
         V("ressalvar que", "heh-sah-oo-VAHR kee", "to note as a caveat that", "verb"),
         V("por contraste", "pohr kohn-TRAHS-jee", "by contrast", "phrase")],
        G("Mediating a culture",
          "não é de essência, é de arranjo · ao contrário do que se diz · ressalvado que …",
          "Mediation replaces essence with mechanism: not what a people is, but how a thing is "
          "arranged. Ao contrário do que se diz marks the correction of a received idea. Every "
          "generalisation is given a scope — em geral, na maioria dos casos, ressalvado que — and "
          "the mediator names their own position before speaking for anyone else.",
          [X("A diferença não é de essência, é de arranjo institucional.", "ah jee-feh-REHN-sah now(n) eh jee eh-SEHN-see-ah, eh jee ah-HAH(n)-zhoo een-stee-too-see-oh-NAH-oo.", "The difference is not one of essence, it is one of institutional arrangement."),
           X("Ao contrário do que se diz, o horário não é desleixo: é negociação.", "ah-oo koh(n)-TRAH-ree-oo doo kee see DEES, oo oh-RAH-ree-oo now(n) eh des-LAY-shoo: eh neh-goh-see-ah-SOW(n).", "Contrary to what is said, the schedule is not carelessness: it is negotiation."),
           X("Ressalvado que falo de uma cidade, o padrão se repete.", "heh-sah-oo-VAH-doo kee FAH-loo jee OO-mah see-DAH-jee, oo pah-DROW(n) see heh-PEH-jee.", "With the caveat that I am speaking of one city, the pattern repeats.")],
          [("No Brasil, todos são alegres.", "Em geral, não se pode falar de um país por um clichê.", "A generalisation about a whole people is neither true nor useful."),
           ("Ao contrário do que se diz que o horário é desleixo.", "Ao contrário do que se diz, o horário é negociação.", "The phrase closes with a comma; que needs its own clause.")]),
        [D("Jornalista estrangeira", "Como explicar o horário brasileiro sem cair no clichê?", "KOH-moo es-plee-KAHR oo oh-RAH-ree-oo brah-zee-LAY-roo see(n) kah-EER noo klee-SHEH?", "How do you explain Brazilian timing without falling into the cliché?"),
         D("Mediadora", "Ao contrário do que se diz, não é desleixo: é negociação.", "ah-oo koh(n)-TRAH-ree-oo doo kee see DEES, now(n) eh des-LAY-shoo: eh neh-goh-see-ah-SOW(n).", "Contrary to what is said, it is not carelessness: it is negotiation."),
         D("Jornalista estrangeira", "Isso vale para todo o país?", "EE-soo VAH-lee pah-rah TOH-doo oo pah-EES?", "Does that hold for the whole country?"),
         D("Mediadora", "Ressalvado que falo de uma cidade, o padrão se repete.", "heh-sah-oo-VAH-doo kee FAH-loo jee OO-mah see-DAH-jee, oo pah-DROW(n) see heh-PEH-jee.", "With the caveat that I am speaking of one city, the pattern repeats.")],
        WS("Mediation worksheet", [
            T("Replace the cliché with a mechanism.", ["the difference is not one of essence, it is one of institutional arrangement", "contrary to what is said, the schedule is not carelessness"],
              ["A diferença não é de essência, é de arranjo institucional", "Ao contrário do que se diz, o horário não é desleixo"]),
            T("Give the scope.", ["with the caveat that I am speaking of one city, the pattern repeats", "in general, one cannot speak of a country through a cliché"],
              ["Ressalvado que falo de uma cidade, o padrão se repete", "Em geral, não se pode falar de um país por um clichê"]),
        ]))),
]


HALFSTEPS["A1+"] = {
    "native": NATIVE,
    "title": "%s A1+ — A padaria, a casa e o fim de semana" % NAME,
    "goals": [
        "Order at a bakery counter, ask the price, and settle with card or cash",
        "Describe your flat and give a simple route to the corner",
        "Make a weekend plan, talk about the weather, and receive a visitor",
    ],
    "units": [
        {"id": "A1+-U1", "title": "A padaria e o café", "lessons": [
            L("Pedir no balcão",
              "The bakery counter has its own polite grammar: me vê (can I have) is what people "
              "say, and para viagem (to take away) or para tomar aqui decides the cup. Quente "
              "and frio agree with the thing: pão quente, café frio. Um pão, dois pães — and the "
              "little coffee is um cafezinho.",
              [V("a padaria", "ah pah-dah-REE-ah", "bakery", "noun"),
               V("o balcão", "oo bah-oo-KOW(n)", "counter", "noun"),
               V("quente", "KEH(n)-jee", "hot, warm", "adjective"),
               V("para viagem", "pah-rah vee-AH-zheh(n)", "to take away", "phrase"),
               V("o pão na chapa", "oo POW(n) nah SHAH-pah", "toasted bread on the griddle", "noun")],
              G("Ordering at the counter",
                "me vê um pão · para viagem · quanto custa?",
                "Me vê + item is the everyday request; queria is the polite one and both are "
                "correct. Para viagem takes the order away, para tomar aqui keeps it at the "
                "counter. The price is asked with quanto custa? or quanto é?.",
                [X("Me vê um pão na chapa e um cafezinho.", "mee VEH oo(n) POW(n) nah SHAH-pah ee oo(n) kah-feh-ZEE-nyoo.", "Can I have a toasted bread and a small coffee."),
                X("É para viagem ou para tomar aqui?", "eh pah-rah vee-AH-zheh(n) oh pah-rah toh-MAHR ah-KEE?", "Is it to take away or to drink here?"),
                X("Quanto custa o pão na chapa?", "KWAHN-too KOOS-tah oo POW(n) nah SHAH-pah?", "How much is the toasted bread?")],
                [("Me vê um pão quente, por favor, e um café, por favor.", "Me vê um pão quente e um café, por favor.", "One por favor closes the whole request."),
                 ("Eu gosto pão quente.", "Eu gosto de pão quente.", "Gostar takes de before what you like.")]),
              [D("Atendente", "Bom dia! O que vai ser?", "boh(n) DEE-ah! oo kee vey sehr?", "Good morning! What will it be?"),
               D("Cliente", "Me vê um pão na chapa e um café com leite.", "mee VEH oo(n) POW(n) nah SHAH-pah ee oo(n) kah-FEH koh(n) LAY-jee.", "Can I have a toasted bread and a coffee with milk."),
               D("Atendente", "Para viagem?", "pah-rah vee-AH-zheh(n)?", "To take away?"),
               D("Cliente", "Para tomar aqui, por favor. Quanto custa?", "pah-rah toh-MAHR ah-KEE, pohr fah-VOHR. KWAHN-too KOOS-tah?", "To drink here, please. How much is it?")],
              WS("Bakery worksheet", [
                  T("Order.", ["can I have a toasted bread and a small coffee", "to take away, please"],
                    ["Me vê um pão na chapa e um cafezinho", "Para viagem, por favor"]),
                  T("Ask the price.", ["how much is the toasted bread?", "is it to drink here or to take away?"],
                    ["Quanto custa o pão na chapa?", "É para tomar aqui ou para viagem?"]),
              ])),
            L("O troco, a nota e o cartão",
              "Brazil uses the real, written with a comma for cents: nove reais e cinquenta. "
              "Nota is the banknote, moeda is the coin, and troco is the change that comes back. "
              "The question at the till is simples ou com cartão? — that is, one payment or two.",
              [V("o real", "oo heh-AH-oo", "the real (currency)", "noun"),
               V("a nota", "ah NOH-tah", "banknote", "noun"),
               V("a moeda", "ah moh-EH-dah", "coin", "noun"),
               V("o cartão", "oo kahr-TOW(n)", "card", "noun"),
               V("o troco", "oo TROH-koo", "change", "noun")],
              G("Paying and counting",
                "quanto deu? · dez reais e cinquenta · tem troco?",
                "Prices are said with e between the reais and the centavos. Não tenho troco "
                "explains a card payment; aceita cartão? asks before ordering if you are not "
                "sure. A nota de dez is a ten-real note.",
                [X("Ficou nove e cinquenta. Tem troco para dez?", "fee-KOH NOH-vee ee seen-KWEHN-tah. tay(n) TROH-koo pah-rah days?", "It came to nine fifty. Do you have change for ten?"),
                X("Não tenho troco, posso pagar no cartão?", "now(n) TEH-nyoo TROH-koo, POH-soo pah-GAHR noo kahr-TOW(n)?", "I don't have change, can I pay by card?"),
                X("Aceita pix?", "ah-SAY-tah peeks?", "Do you take pix?")],
                [("Ficou dez reais e cinquenta centavos de reais.", "Ficou dez reais e cinquenta centavos.", "Centavos already belongs to the real; do not repeat it."),
                 ("Eu pago com cartão, tem taxa?", "Se eu pagar com cartão, tem taxa?", "The question needs se or a statement, not a mixed form.")]),
              [D("Cliente", "Quanto deu tudo?", "KWAHN-too deh-oo TOO-doo?", "How much did it all come to?"),
               D("Atendente", "Doze e trinta.", "DOH-zee ee TREEN-tah.", "Twelve thirty."),
               D("Cliente", "Tenho vinte. Aceita cartão para o resto?", "TEH-nyoo VEEN-jee. ah-SAY-tah kahr-TOW(n) pah-rah oo HEHS-too?", "I have twenty. Do you take card for the rest?"),
               D("Atendente", "Aceito. Aqui está o troco.", "ah-SAY-too. ah-KEE es-TAH oo TROH-koo.", "I do. Here is the change.")],
              WS("Money worksheet", [
                  T("Say the price.", ["nine fifty", "a ten-real note"],
                    ["nove e cinquenta", "uma nota de dez"]),
                  T("Ask about payment.", ["do you take card?", "I don't have change"],
                    ["Aceita cartão?", "Não tenho troco"]),
              ])),
            L("Convidar para um café",
              "An invitation is short: quer tomar um café? Bora? (come on) answers it in one word, "
              "and pago eu settles who pays before the bill comes. Mais tarde pushes it to later, "
              "and fica para a próxima keeps it friendly when the answer is no.",
              [V("convidar", "koh(n)-vee-DAHR", "to invite", "verb"),
               V("bora", "BOH-rah", "let's go", "interjection"),
               V("pago eu", "PAH-goo EH-oo", "it's on me", "phrase"),
               V("mais tarde", "mays TAHR-jee", "later", "phrase"),
               V("fica para a próxima", "FEE-kah pah-rah ah PROH-see-mah", "let's leave it for next time", "phrase")],
              G("Inviting and answering",
                "quer tomar um café? · bora · pago eu · fica para a próxima",
                "Quer + infinitive invites without pressure. Bora is the invitation accepted, and "
                "não dá hoje is the refusal that keeps the door open. Pago eu and é minha vez "
                "settle payment, and both are said before the order.",
                [X("Quer tomar um café depois do trabalho?", "kehr toh-MAHR oo(n) kah-FEH deh-POYS doo trah-BAH-lyoo?", "Do you want to have a coffee after work?"),
                X("Bora! Mas pago eu desta vez.", "BOH-rah! mahs PAH-goo EH-oo DEHS-tah VEZ.", "Let's go! But it's on me this time."),
                X("Hoje não dá. Fica para a próxima!", "OH-jee now(n) dah. FEE-kah pah-rah ah PROH-see-mah!", "Today doesn't work. Let's leave it for next time!")],
                [("Você quer que eu vou tomar um café?", "Você quer tomar um café?", "Quer takes a bare infinitive when the subject is the same."),
                 ("Pago para eu.", "Pago eu.", "The subject follows the verb: pago eu.")]),
              [D("Marina", "Quer tomar um café depois do trabalho?", "kehr toh-MAHR oo(n) kah-FEH deh-POYS doo trah-BAH-lyoo?", "Do you want to have a coffee after work?"),
               D("Paulo", "Bora! Mas pago eu desta vez.", "BOH-rah! mahs PAH-goo EH-oo DEHS-tah VEZ.", "Let's go! But it's on me this time."),
               D("Marina", "Combinado. Às seis na esquina?", "koh(n)-bee-NAH-doo. ahs says nah es-KEE-nah?", "Agreed. At six on the corner?"),
               D("Paulo", "Fechado. Até lá!", "feh-SHAH-doo. ah-TEH lah!", "Done. See you there!")],
              WS("Invitation worksheet", [
                  T("Invite.", ["do you want to have a coffee after work?", "let's go, but it's on me"],
                    ["Quer tomar um café depois do trabalho?", "Bora, mas pago eu"]),
                  T("Answer without closing the door.", ["today doesn't work", "let's leave it for next time"],
                    ["Hoje não dá", "Fica para a próxima"]),
              ])),
        ]},
        {"id": "A1+-U2", "title": "A casa e a rua", "lessons": [
            L("Descrever o apartamento",
              "A room is described with ter and estar: o apartamento tem duas janelas, a sala "
              "está clara. Apertado (tight) and espaçoso (roomy) judge the space, and the "
              "diminutive -inho softens it: um quartinho. Fica no segundo andar places it.",
              [V("a janela", "ah zhah-NEH-lah", "window", "noun"),
               V("a mesa", "ah MEH-zah", "table", "noun"),
               V("a cama", "ah KAH-mah", "bed", "noun"),
               V("apertado", "ah-pehr-TAH-doo", "cramped, tight", "adjective"),
               V("espaçoso", "es-pah-SOH-zoo", "roomy", "adjective")],
              G("Describing a room",
                "o apartamento tem … · a sala está … · fica no … andar",
                "Ter lists what exists; estar describes the state now (a janela está aberta). "
                "The diminutive marks size or affection: um quartinho, uma salinha. Fica + em "
                "places the flat in the building or the street.",
                [X("O apartamento tem duas janelas e uma varanda pequena.", "oo ah-pahr-tah-MEN-too tay(n) DOO-ahs zhah-NEH-lahs ee OO-mah vah-RAHN-dah peh-KEH-nah.", "The flat has two windows and a small balcony."),
                X("A sala está clara porque a janela dá para o nascente.", "ah SAH-lah es-TAH KLAH-rah pohr-KEH ah zhah-NEH-lah dah pah-rah oo nah-SEH(n)-jee.", "The living room is bright because the window faces east."),
                X("A cozinha é apertada, mas a sala é espaçosa.", "ah koh-ZEE-nyah eh ah-pehr-TAH-dah, mahs ah SAH-lah eh es-pah-SOH-zah.", "The kitchen is cramped, but the living room is roomy.")],
                [("O apartamento está duas janelas.", "O apartamento tem duas janelas.", "Things a flat contains take ter; estar is for a temporary state."),
                 ("A sala é clara porque a janela é para o nascente.", "A sala é clara porque a janela dá para o nascente.", "A window dá para a direction; it does not é para it.")]),
              [D("Vizinha", "Seu apartamento é grande?", "seh-oo ah-pahr-tah-MEN-too eh GRAHN-jee?", "Is your flat big?"),
               D("Marina", "Não é grande, mas é claro e tem uma varanda.", "now(n) eh GRAHN-jee, mahs eh KLAH-roo ee tay(n) OO-mah vah-RAHN-dah.", "It isn't big, but it is bright and has a balcony."),
               D("Vizinha", "E a cozinha?", "ee ah koh-ZEE-nyah?", "And the kitchen?"),
               D("Marina", "É apertada, mas cabe uma mesa pequena.", "eh ah-pehr-TAH-dah, mahs KAH-bee OO-mah MEH-zah peh-KEH-nah.", "It's cramped, but a small table fits.")],
              WS("Home description worksheet", [
                  T("Describe what there is.", ["the flat has two windows and a small balcony", "the kitchen is cramped but the living room is roomy"],
                    ["O apartamento tem duas janelas e uma varanda pequena", "A cozinha é apertada, mas a sala é espaçosa"]),
                  T("Describe the state.", ["the living room is bright because the window faces east", "the table fits in the kitchen"],
                    ["A sala está clara porque a janela dá para o nascente", "Cabe uma mesa na cozinha"]),
              ])),
            L("Onde fica a esquina?",
              "A route in the neighbourhood is told with landmarks, not numbers: sobe a rua, desce "
              "a ladeira, vira na esquina, fica em frente ao mercado. Do lado de and em frente a "
              "are the two prepositions you will use most, and a two-minute walk is a dois "
              "minutos a pé.",
              [V("a esquina", "ah es-KEE-nah", "corner", "noun"),
               V("a ladeira", "ah lah-DAY-rah", "slope, hill", "noun"),
               V("em frente a", "ey(n) FREHN-jee ah", "opposite, in front of", "phrase"),
               V("do lado de", "doo LAH-doo jee", "next to", "phrase"),
               V("a vários minutos", "ah VAH-ree-oos mee-NOO-toos", "a few minutes away", "phrase")],
              G("Describing the way in the neighbourhood",
                "sobe a rua · vira na esquina · fica em frente ao mercado",
                "Sobe and desce describe the street's slope; vira na esquina turns with no "
                "preposition beyond na. Em frente a contracts with the article: em frente ao "
                "mercado, em frente à praça. The landmark comes last, after the verb.",
                [X("Sobe a rua e vira na primeira esquina.", "SOH-bee ah HOO-ah ee VEE-rah nah pree-MAY-rah es-KEE-nah.", "Go up the street and turn at the first corner."),
                X("A padaria fica em frente ao mercado.", "ah pah-dah-REE-ah FEE-kah ey(n) FREHN-jee ah-oo mehr-KAH-doo.", "The bakery is opposite the market."),
                X("A praça fica do lado da farmácia, a dois minutos a pé.", "ah PRAH-sah FEE-kah doo LAH-doo dah fahr-MAH-see-ah, ah DOYS mee-NOO-toos ah PEH.", "The square is next to the pharmacy, two minutes away on foot.")],
                [("Fica em frente o mercado.", "Fica em frente ao mercado.", "Em frente contracts with the article: ao."),
                 ("Vira na esquina, vira, vira.", "Vira na esquina.", "One instruction per sentence for a listener on the move.")]),
              [D("Visitante", "Desculpe, onde fica a praça?", "des-KOOL-pee, OH(n)-jee FEE-kah ah PRAH-sah?", "Excuse me, where is the square?"),
               D("Moradora", "Sobe a rua e vira na segunda esquina.", "SOH-bee ah HOO-ah ee VEE-rah nah seh-GOON-dah es-KEE-nah.", "Go up the street and turn at the second corner."),
               D("Visitante", "Fica longe?", "FEE-kah LOHN-jee?", "Is it far?"),
               D("Moradora", "Não, fica do lado da farmácia, a dois minutos a pé.", "now(n), FEE-kah doo LAH-doo dah fahr-MAH-see-ah, ah DOYS mee-NOO-toos ah PEH.", "No, it's next to the pharmacy, two minutes on foot.")],
              WS("Neighbourhood worksheet", [
                  T("Give the route.", ["go up the street and turn at the first corner", "the bakery is opposite the market"],
                    ["Sobe a rua e vira na primeira esquina", "A padaria fica em frente ao mercado"]),
                  T("Say how far it is.", ["two minutes on foot", "next to the pharmacy"],
                    ["a dois minutos a pé", "do lado da farmácia"]),
              ])),
            L("A visita da vizinha",
              "Receiving someone at home runs on five fixed sentences: entre, fique à vontade, "
              "senta-se, aceita um café?, e agora você mora aqui?. Oferecer (to offer) and aceitar "
              "(to accept) carry the courtesy; recusar com jeitinho (to decline gently) is também "
              "uma forma de cortesia.",
              [V("entre", "EH(n)-tree", "come in", "verb"),
               V("fique à vontade", "FEE-kee ah vohn-TAH-jee", "make yourself at home", "phrase"),
               V("oferecer", "oh-feh-reh-SEHR", "to offer", "verb"),
               V("aceitar", "ah-say-TAHR", "to accept", "verb"),
               V("recusar", "heh-koo-ZAHR", "to decline", "verb")],
              G("Receiving and offering",
                "entre · fique à vontade · aceita um café? · obrigada, mas agora não",
                "Entre and senta-se are imperatives that welcome. Fique à vontade releases the "
                "guest from standing on ceremony. An offer is answered in two steps: the thanks "
                "first, then the answer — obrigada, mas agora não; depois eu aceito.",
                [X("Entre, fique à vontade. Senta-se ali.", "EH(n)-tree, FEE-kee ah vohn-TAH-jee. SEN-tah-see ah-LEE.", "Come in, make yourself at home. Sit over there."),
                X("Aceita um café ou prefere água?", "ah-SAY-tah oo(n) kah-FEH oh preh-FEH-ree AH-gwah?", "Would you like a coffee or would you prefer water?"),
                X("Obrigada, agora não. Depois eu aceito.", "oh-bree-GAH-dah, ah-GOH-rah now(n). deh-POYS eh-oo ah-SAY-too.", "Thank you, not now. I'll accept later.")],
                [("Entra e senta.", "Entre e sente-se.", "Receiving a guest takes the polite imperative: entre, sente-se."),
                 ("Aceito um café? Obrigada.", "Aceita um café? — Obrigada, agora não.", "The guest asks nothing; the host offers, and the answer comes first.")]),
              [D("Vizinha", "Oi, tudo bem? Passei para dar um oi.", "oy, too-DOO bey(n)? pah-SEH pah-rah DAHR oo(n) oy.", "Hi, how are you? I came by to say hello."),
               D("Marina", "Entre, fique à vontade. Aceita um café?", "EH(n)-tree, FEE-kee ah vohn-TAH-jee. ah-SAY-tah oo(n) kah-FEH?", "Come in, make yourself at home. Would you like a coffee?"),
               D("Vizinha", "Aceito, obrigada. Que apartamento claro!", "ah-SAY-too, oh-bree-GAH-dah. kee ah-pahr-tah-MEN-too KLAH-roo!", "I'd love one, thank you. What a bright flat!"),
               D("Marina", "Senta-se aqui. A janela dá para o nascente.", "SEN-tah-see ah-KEE. ah zhah-NEH-lah dah pah-rah oo nah-SEH(n)-jee.", "Sit here. The window faces east.")],
              WS("Visiting worksheet", [
                  T("Receive a visitor.", ["come in, make yourself at home", "would you like a coffee or water?"],
                    ["Entre, fique à vontade", "Aceita um café ou prefere água?"]),
                  T("Decline gently.", ["thank you, not now", "I'll accept later"],
                    ["Obrigada, agora não", "Depois eu aceito"]),
              ])),
        ]},
        {"id": "A1+-U3", "title": "O fim de semana", "lessons": [
            L("Planos simples",
              "Plans use vou + infinitive: vou à praia, vou visitar minha irmã. Juntos, talvez "
              "and depois dos almoços place them in time, and the question é se vai chover? "
              "covers the weather you cannot control. Combinado closes a plan.",
              [V("o plano", "oo PLAH-noo", "plan", "noun"),
               V("juntos", "ZHOON-toos", "together", "adverb"),
               V("talvez", "tah-oo-VEHS", "maybe", "adverb"),
               V("combinado", "koh(n)-bee-NAH-doo", "agreed, settled", "adjective"),
               V("depois do almoço", "deh-POYS doo ah-oo-MOH-soo", "after lunch", "phrase")],
              G("Making a simple plan",
                "vou + infinitive · talvez eu vá · depois do almoço · combinado",
                "Vou + infinitive states your own plan; talvez takes the subjunctive when it is "
                "not settled (talvez eu vá). Depois de + noun places it, and combinado accepts it "
                "on the spot.",
                [X("No sábado eu vou visitar minha irmã.", "noo SAH-bah-doo eh-oo voh vee-zee-TAHR MEE-nyah eer-MAH(n).", "On Saturday I'm going to visit my sister."),
                X("Talvez eu vá à praia no domingo, se fizer sol.", "tah-oo-VEHS eh-oo VAH ah PRAH-yah noo doh-MEEN-goo, see fee-ZEHR soh-oo.", "Maybe I'll go to the beach on Sunday, if it's sunny."),
                X("Depois do almoço a gente caminha no parque. — Combinado.", "deh-POYS doo ah-oo-MOH-soo ah ZHEH(n)-jee kah-MEE-nyah noo PAHR-kee. — koh(n)-bee-NAH-doo.", "After lunch we'll walk in the park. — Agreed.")],
                [("Talvez eu vou à praia.", "Talvez eu vá à praia.", "Talvez of an open possibility takes the subjunctive."),
                 ("Vou para visitar minha irmã.", "Vou visitar minha irmã.", "The near future takes the bare infinitive.")]),
              [D("Paulo", "Quais são os planos para o fim de semana?", "KWAH-ees sow(n) oos PLAH-noos pah-rah oo fee(n) jee seh-MAH-nah?", "What are the plans for the weekend?"),
               D("Marina", "Sábado eu vou visitar minha irmã. E você?", "SAH-bah-doo eh-oo voh vee-zee-TAHR MEE-nyah eer-MAH(n). ee voh-SEH?", "On Saturday I'm going to visit my sister. And you?"),
               D("Paulo", "Talvez eu vá à praia, se fizer sol.", "tah-oo-VEHS eh-oo VAH ah PRAH-yah, see fee-ZEHR soh-oo.", "Maybe I'll go to the beach, if it's sunny."),
               D("Marina", "Depois do almoço eu também quero caminhar.", "deh-POYS doo ah-oo-MOH-soo eh-oo tah(n)-BEH(n) KEH-roo kah-mee-NYAHR.", "After lunch I want to walk too.")],
              WS("Plans worksheet", [
                  T("State your plan.", ["on Saturday I'm going to visit my sister", "maybe I'll go to the beach on Sunday"],
                    ["No sábado eu vou visitar minha irmã", "Talvez eu vá à praia no domingo"]),
                  T("Place it in time.", ["after lunch", "if it's sunny"],
                    ["depois do almoço", "se fizer sol"]),
              ])),
            L("O mar, a areia e o guarda-sol",
              "The beach vocabulary is a short list that everybody uses: a areia, o mar, a "
              "cadeira, o guarda-sol, o protetor. Levar (to bring) and dar um mergulho (to take "
              "a dip) describe the day. Cuidado com o sol! is not a warning about weather but "
              "about burning.",
              [V("a areia", "ah ah-RAY-ah", "sand", "noun"),
               V("o mar", "oo MAHR", "sea", "noun"),
               V("o guarda-sol", "oo GWAHR-dah soh-oo", "beach umbrella", "noun"),
               V("levar", "leh-VAHR", "to bring, to take along", "verb"),
               V("dar um mergulho", "DAHR oo(n) mehr-GOO-lyoo", "to take a dip", "phrase")],
              G("A day at the beach",
                "levar + object · dar um mergulho · na areia · cuidado com o sol",
                "Levar says what you bring; pegar is what you pick up on the way. Na areia is "
                "the place, no mar is what you swim in. The heat is described with estar: a "
                "areia está quente.",
                [X("Vou levar água, boné e protetor.", "voh leh-VAHR AH-gwah, boh-NEH ee proh-teh-TOHR.", "I'll bring water, a cap and sunscreen."),
                X("A areia está quente, vamos dar um mergulho?", "ah ah-RAY-ah es-TAH KEH(n)-jee, VAH-moos DAHR oo(n) mehr-GOO-lyoo?", "The sand is hot, shall we take a dip?"),
                X("Cuidado com o sol, use protetor.", "kow-DAH-doo koh(n) oo SOH-oo, OO-zee proh-teh-TOHR.", "Be careful with the sun, use sunscreen.")],
                [("Vou levar a praia.", "Vou levar o guarda-sol.", "You carry objects, not the place."),
                 ("A areia é quente agora.", "A areia está quente agora.", "A current condition takes estar.")]),
              [D("Paulo", "Vamos à praia amanhã?", "VAH-moos ah PRAH-yah ah-mah-NYAH(n)?", "Shall we go to the beach tomorrow?"),
               D("Marina", "Vamos. Vou levar água e protetor.", "VAH-moos. voh leh-VAHR AH-gwah ee proh-teh-TOHR.", "Let's. I'll bring water and sunscreen."),
               D("Paulo", "Tem guarda-sol?", "tay(n) GWAHR-dah soh-oo?", "Do you have a beach umbrella?"),
               D("Marina", "Tenho. E a areia está quente, então vamos cedo.", "TEH-nyoo. ee ah ah-RAY-ah es-TAH KEH(n)-jee, ey(n)-TOW(n) VAH-moos SEH-doo.", "I do. And the sand gets hot, so let's go early.")],
              WS("Beach worksheet", [
                  T("Pack for the beach.", ["I'll bring water, a cap and sunscreen", "do you have a beach umbrella?"],
                    ["Vou levar água, boné e protetor", "Tem guarda-sol?"]),
                  T("Describe the moment.", ["the sand is hot", "shall we take a dip?"],
                    ["A areia está quente", "Vamos dar um mergulho?"]),
              ])),
            L("O almoço de domingo",
              "Sunday lunch is the family ritual: o almoço, o prato, a sobremesa, o cafezinho "
              "depois. Servir (to serve) and repetir (to have seconds) are the two verbs that "
              "matter, and says quem quer repetir? — the host asks, the guest answers. Está tudo "
              "uma delícia is the sentence that ends the meal well.",
              [V("o almoço", "oo ah-oo-MOH-soo", "lunch", "noun"),
               V("o prato", "oo PRAH-too", "dish, plate", "noun"),
               V("a sobremesa", "ah soh-breh-MEH-zah", "dessert", "noun"),
               V("servir", "sehr-VEER", "to serve", "verb"),
               V("repetir", "heh-peh-TEER", "to have more, to repeat", "verb")],
              G("At the table",
                "quem quer repetir? · um pouco mais · está tudo uma delícia",
                "Servir is irregular in the present: eu sirvo, você serve, nós servimos. Repetir "
                "in this context means to take a second helping. Politely refusing uses obrigado "
                "and a reason: obrigado, estou satisfeito.",
                [X("Quem quer repetir o arroz?", "key(n) KEH(r) heh-peh-TEER oo ah-HOHS?", "Who wants more rice?"),
                X("Um pouco mais, por favor. Está uma delícia.", "oo(n) POH-koo mays, pohr fah-VOHR. es-TAH OO-mah deh-LEE-see-ah.", "A little more, please. It's delicious."),
                X("Obrigada, estou satisfeita. E a sobremesa?", "oh-bree-GAH-dah, es-TOH sah-tees-FAY-tah. ee ah soh-breh-MEH-zah?", "Thank you, I'm full. And dessert?")],
                [("Eu sirvo para você.", "Eu sirvo você.", "Servir takes a direct object: sirvo o arroz."),
                 ("Quem quer repetir de arroz?", "Quem quer repetir o arroz?", "Repetir takes a direct object here.")]),
              [D("Dona Célia", "Senta-se, o almoço está pronto. Arroz, feijão e frango.", "SEN-tah-see, oo ah-oo-MOH-soo es-TAH PROHN-too. ah-HOHS, feh-ZHOW(n) ee FRAHN-goo.", "Sit down, lunch is ready. Rice, beans and chicken."),
               D("Paulo", "Que cheiro bom! Vou repetir depois.", "kee SHEH-roo boh(n)! voh heh-peh-TEER deh-POYS.", "What a good smell! I'll have more later."),
               D("Dona Célia", "Tem sobremesa: pudim.", "tay(n) soh-breh-MEH-zah: poo-DEE(n).", "There's dessert: flan."),
               D("Marina", "Está tudo uma delícia, dona Célia.", "es-TAH TOO-doo OO-mah deh-LEE-see-ah, DOH-nah SEH-lyah.", "Everything is delicious, Dona Célia.")],
              WS("Sunday lunch worksheet", [
                  T("Offer and serve.", ["who wants more rice?", "a little more, please"],
                    ["Quem quer repetir o arroz?", "Um pouco mais, por favor"]),
                  T("Compliment and refuse.", ["everything is delicious", "thank you, I'm full"],
                    ["Está tudo uma delícia", "Obrigada, estou satisfeita"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("The padaria is the neighbourhood clock. It opens before the bakery on the corner "
                 "of a Portuguese novel and closes after the last bus: people buy pão francês by "
                 "weight, drink a cafezinho standing at the balcão, and read the day's news on "
                 "the counter's radio. Pão na chapa — a split roll pressed on the griddle with "
                 "butter — is the breakfast of a whole country, and para viagem is the phrase "
                 "that folds it into a paper bag."),
        source_url="https://en.wikipedia.org/wiki/Brazilian_cuisine",
        reading=("Toda manhã eu passo na padaria da esquina antes do trabalho. O balcão está "
                 "cheio: um senhor pede pão francês, uma moça espera o café, e o atendente "
                 "pergunta se é para viagem. Eu peço um pão na chapa e um cafezinho, pago com "
                 "nota de dez e espero o troco. Em cinco minutos eu já estou na rua, com o pão "
                 "quentinho na mão."),
        reading_gloss=("Every morning I stop at the bakery on the corner before work. The counter "
                       "is full: a man asks for French bread, a young woman waits for the coffee, "
                       "and the attendant asks whether it is to take away. I ask for a toasted "
                       "bread and a small coffee, pay with a ten note and wait for the change. In "
                       "five minutes I am already in the street, with the warm bread in my hand."),
        listening=("Bom dia, o que vai ser? — Me vê um pão na chapa e um café com leite. — Para "
                   "viagem? — Para tomar aqui. — Ficou nove e cinquenta. — Tenho dez. — Aqui "
                   "está o troco, obrigado."),
        listening_gloss=("Good morning, what will it be? — Can I have a toasted bread and a "
                         "coffee with milk. — To take away? — To drink here. — That's nine "
                         "fifty. — I have ten. — Here is your change, thank you."),
        voice_tag=VOICE,
        idioms=[
            ("por conta da casa", "on the house's account", "the owner is paying, said of a drink or a plate"),
            ("para viagem", "for the journey", "takeaway — the bag you carry out"),
            ("na chapa", "on the griddle", "pressed and toasted on the hot plate"),
            ("puxar conversa", "to pull conversation", "to start chatting with a stranger"),
            ("bem na hora", "well in the hour", "just in time, neither early nor late"),
            ("um cafezinho", "a little coffee", "the small standing coffee that is a social ritual"),
            ("à toa", "at loose", "aimlessly, with nothing to do"),
            ("de pé", "on foot", "standing up, as the coffee is taken at the counter"),
            ("ficar de papo", "to stay chatting", "to linger talking after the order is finished"),
            ("até mais", "until more", "see you later, the shortest goodbye"),
        ],
        mistakes=[
            ("Você quer ir na padaria?", "Você quer ir à padaria?", "Ir takes the preposition a: à padaria."),
            ("Eu gosto pão quente.", "Eu gosto de pão quente.", "Gostar requires de."),
            ("Fica bem na hora, chego atrasado.", "Fica bem na hora, não chego atrasado.", "Bem na hora means exactly on time, so it excludes arriving late."),
        ],
        task_title="Peça no balcão",
        task_instructions=("Write the six lines of a bakery order: greet, ask for two items, say "
                           "whether it is para viagem, ask the price, pay, and thank. Then say it "
                           "aloud twice, once as the customer and once as the attendant, and "
                           "check three things: me vê for the order, um pão quente with the "
                           "adjective agreeing, and the price said with e."),
    ),
    "test": [
        ("translate_en", "Say: I want a toasted bread and a small coffee.", "Me vê um pão na chapa e um cafezinho."),
        ("translate_pt", "Esta rua fica em frente ao mercado.", "This street is opposite the market."),
        ("multiple_choice", "Which sentence asks for takeaway?", "É para viagem?"),
        ("fill_in_the_blank", "A padaria ___ ao mercado.", "fica"),
        ("word_selection", "Select the Portuguese for 'change' (money back).", "o troco"),
        ("error_correction", "Eu gosto café com leite.", "Eu gosto de café com leite."),
        ("dialogue_completion", "Complete: Aceita um café? — ___ (Thank you, not now)", "Obrigada, agora não"),
        ("matching", "Match a sobremesa to its meaning.", "dessert"),
        ("reading_comprehension", "No texto, o que Marina pede na padaria?", "a toasted bread and a small coffee"),
        ("inference", "O atendente pergunta 'para viagem?'. What does that tell us about the shop?", "it serves both people who stay and people who leave"),
        ("main_idea", "O texto conta uma manhã na padaria. — what is this sentence?", "the main point of the reading"),
        ("detail_identification", "Quanto ficou o pedido de Marina?", "nine fifty"),
    ],
}


HALFSTEPS["A2+"] = {
    "native": NATIVE,
    "title": "%s A2+ — Compras, saúde e trabalho" % NAME,
    "goals": [
        "Buy clothes and shoes, compare prices and swap an item",
        "Describe a symptom and ask what to take at the pharmacy",
        "Talk about your job, a course and a job interview",
    ],
    "units": [
        {"id": "A2+-U1", "title": "Compras e trocas", "lessons": [
            L("Roupas e tamanhos",
              "In a shop, the clerk asks posso ajudar?, you answer estou só olhando or procuro "
              "um tamanho. Provador is the changing room and ficou apertado is a verdict, not a "
              "complaint: prova o número maior. Sizes use the verb vestir: veste bem.",
              [V("o tamanho", "oo tah-MAH-nyoo", "size", "noun"),
               V("o provador", "oo proh-vah-DOHR", "changing room", "noun"),
               V("experimentar", "es-peh-ree-men-TAHR", "to try on", "verb"),
               V("servir", "sehr-VEER", "to fit", "verb"),
               V("a troca", "ah TROH-kah", "exchange", "noun")],
              G("Trying clothes on",
                "posso experimentar? · ficou apertado · tem um número maior?",
                "Servir means both to serve and to fit: esta blusa não me serve. The past "
                "ficou describes the fit once tried: ficou grande. To ask for another "
                "size: tem em número maior? The reply uses em: tem em quarenta.",
                [X("Posso experimentar este vestido?", "POH-soo es-peh-ree-men-TAHR ES-jee ves-TEE-doo?", "Can I try on this dress?"),
                X("Ficou apertado nos ombros. Tem um número maior?", "fee-KOH ah-pehr-TAH-doo noos OH(n)-broos. tay(n) oo(n) NOO-meh-roo mah-YOHR?", "It's tight in the shoulders. Do you have a bigger size?"),
                X("Este modelo me serve bem.", "ES-jee moh-DEH-loo mee SEHR-vee bey(n).", "This style fits me well.")],
                [("Ficou muito apertada, eu trocar.", "Ficou muito apertada, quero trocar.", "Two full clauses; the second needs its own verb."),
                 ("Tem em um número maior?", "Tem em um número maior?", "Em + size is the correct pattern: em quarenta.")]),
              [D("Vendedora", "Posso ajudar?", "POH-soo ah-zhoo-DAHR?", "Can I help?"),
               D("Cliente", "Procuro uma camisa azul, tamanho médio.", "proh-KOO-roo OO-mah kah-MEE-zah ah-ZOO-oo, tah-MAH-nyoo MEH-jee-oo.", "I'm looking for a blue shirt, medium."),
               D("Vendedora", "Quer experimentar no provador?", "kehr es-peh-ree-men-TAHR noo proh-vah-DOHR?", "Would you like to try it in the changing room?"),
               D("Cliente", "Quero. Ficou apertada; tem em número maior?", "KEH-roo. fee-KOH ah-pehr-TAH-dah; tay(n) ey(n) NOO-meh-roo mah-YOHR?", "Yes. It's tight; do you have a bigger size?")],
              WS("Clothes worksheet", [
                  T("Ask in the shop.", ["can I try on this dress?", "do you have a bigger size?"],
                    ["Posso experimentar este vestido?", "Tem um número maior?"]),
                  T("Say how it fits.", ["it's tight in the shoulders", "this style fits me well"],
                    ["Ficou apertado nos ombros", "Este modelo me serve bem"]),
              ])),
            L("Comparar preços",
              "Comparison in Portuguese is structural: mais barato que, menos caro que, igual a. "
              "O dobro (twice), a metade (half) and em promoção (on sale) do the arithmetic. "
              "Custa e sai are both said of price: sai mais barato comprar duas.",
              [V("barato", "bah-RAH-too", "cheap", "adjective"),
               V("caro", "KAH-roo", "expensive", "adjective"),
               V("o dobro", "oo DOH-broo", "twice as much", "noun"),
               V("a metade", "ah meh-TAH-jee", "half", "noun"),
               V("em promoção", "ey(n) proh-moh-SOW(n)", "on sale", "phrase")],
              G("Comparing prices",
                "mais barato que · menos caro que · sai por · em promoção",
                "Mais barato que and menos caro que are both correct; igual a compares as equal. "
                "The verb sair means to end up costing: sai por vinte. Custa is the plain price "
                "and custa menos says cheaper without the comparative.",
                [X("Este modelo é mais barato que o outro.", "ES-jee moh-DEH-loo eh mays bah-RAH-too kee oo OH-troo.", "This style is cheaper than the other."),
                X("Na promoção, sai pela metade do preço.", "nah proh-moh-SOW(n), sey PEH-lah meh-TAH-jee doo PREH-soo.", "On sale, it comes to half the price."),
                X("O pacote grande custa o dobro, mas leva o dobro.", "oo pah-KOH-jee GRAHN-jee KOOS-tah oo DOH-broo, mahs LEH-vah oo DOH-broo.", "The big pack costs twice as much but holds twice as much.")],
                [("Este é mais barato do que o outro modelo que.", "Este é mais barato que o outro modelo.", "The comparative is mais barato que, with no do."),
                 ("Custa menos caro.", "Custa menos. / É mais barato.", "Menos and caro do not combine: choose one.")]),
              [D("Cliente", "Qual dos dois sai mais barato?", "kwah-oo doos doys sey mays bah-RAH-too?", "Which of the two comes out cheaper?"),
               D("Vendedor", "O pequeno, mas o grande leva o dobro.", "oo peh-KEH-noo, mahs oo GRAHN-jee LEH-vah oo DOH-broo.", "The small one, but the big one holds twice as much."),
               D("Cliente", "E está em promoção?", "ee es-TAH ey(n) proh-moh-SOW(n)?", "And is it on sale?"),
               D("Vendedor", "Só o pequeno, até domingo.", "soh oo peh-KEH-noo, ah-TEH doh-MEEN-goo.", "Only the small one, until Sunday.")],
              WS("Prices worksheet", [
                  T("Compare.", ["this style is cheaper than the other", "the big pack costs twice as much"],
                    ["Este modelo é mais barato que o outro", "O pacote grande custa o dobro"]),
                  T("Talk about the sale.", ["on sale, it comes to half the price", "is it on sale?"],
                    ["Na promoção, sai pela metade do preço", "Está em promoção?"]),
              ])),
            L("Devolver e trocar",
              "A troca has a deadline and a paper: o prazo de troca and a nota fiscal. Sem a "
              "nota, the shop may still help but is not obliged. The fault is o defeito, and the "
              "verbs are trocar por (swap for) and devolver (return for money). Pedir reembolso "
              "is the formal request.",
              [V("devolver", "deh-voh-oo-VEHR", "to return", "verb"),
               V("o defeito", "oo deh-FAY-too", "defect, fault", "noun"),
               V("o prazo", "oo PRAH-zoo", "deadline, period", "noun"),
               V("a nota fiscal", "ah NOH-tah fees-KAH-oo", "receipt", "noun"),
               V("o reembolso", "oo heh-ey(n)-BOH-oo-soo", "refund", "noun")],
              G("Returning and exchanging",
                "queria trocar · dentro do prazo · tem defeito · pedir reembolso",
                "Dentro do prazo (within the period) and fora do prazo set the right. Trocar por "
                "names both items: queria trocar este por aquele. If the shop has no replacement, "
                "the question is pode devolver? and the answer can be crédito na loja.",
                [X("Comprei ontem e queria trocar esta camisa.", "koh(n)-PREH ee OH(n)-tay(n) ee keh-REE-ah troh-KAHR ES-tah kah-MEE-zah.", "I bought it yesterday and would like to exchange this shirt."),
                X("Está dentro do prazo de troca?", "es-TAH DEY(n)-troo doo PRAH-zoo jee TROH-kah?", "Is it within the exchange period?"),
                X("O produto tem defeito; queria pedir reembolso.", "oo proh-DOO-too tay(n) deh-FAY-too; keh-REE-ah peh-DEER heh-ey(n)-BOH-oo-soo.", "The product is faulty; I'd like a refund.")],
                [("Queria trocar este camisa por aquele.", "Queria trocar esta camisa por aquela.", "Camisa is feminine: esta, aquela."),
                 ("Vou devolver e trocar em outra coisa.", "Vou trocar por outra coisa.", "One verb: trocar por.")]),
              [D("Cliente", "Bom dia, queria trocar este sapato.", "boh(n) DEE-ah, keh-REE-ah troh-KAHR ES-jee sah-PAH-too.", "Good morning, I'd like to exchange these shoes."),
               D("Atendente", "Tem a nota fiscal?", "tay(n) ah NOH-tah fees-KAH-oo?", "Do you have the receipt?"),
               D("Cliente", "Tenho. Comprei ontem e ficou apertado.", "TEH-nyoo. koh(n)-PREH ee OH(n)-tay(n) ee fee-KOH ah-pehr-TAH-doo.", "I do. I bought it yesterday and it was tight."),
               D("Atendente", "Sem problema, está dentro do prazo.", "sey(n) proh-BLEH-mah, es-TAH DEY(n)-troo doo PRAH-zoo.", "No problem, it's within the period.")],
              WS("Exchanges worksheet", [
                  T("Ask for the exchange.", ["I'd like to exchange this shirt", "is it within the exchange period?"],
                    ["Queria trocar esta camisa", "Está dentro do prazo de troca?"]),
                  T("Name the problem.", ["the product is faulty", "I'd like a refund"],
                    ["O produto tem defeito", "Queria pedir reembolso"]),
              ])),
        ]},
        {"id": "A2+-U2", "title": "Saúde e farmácia", "lessons": [
            L("Dizer o que sente",
              "A symptom is said with dor and ter: tenho dor de cabeça, estou com febre. Estou "
              "com + noun is the everyday way to say what you have — estou com tosse. The doctor "
              "asks onde dói? and há quanto tempo?.",
              [V("a dor", "ah DOHR", "pain", "noun"),
               V("a febre", "ah FEH-bree", "fever", "noun"),
               V("a tosse", "ah TOH-see", "cough", "noun"),
               V("dói", "doy", "it hurts", "verb"),
               V("há quanto tempo", "ah KWAHN-too TEH(n)-poo", "for how long", "phrase")],
              G("Describing symptoms",
                "estou com febre · dói aqui · há quanto tempo?",
                "Dor takes de + part: dor de cabeça, dor de garganta. Dói agrees with what hurts: "
                "dói a cabeça, doem os pés. Há quanto tempo? uses há for duration up to now.",
                [X("Estou com febre e dor de cabeça desde ontem.", "es-TOH koh(n) FEH-bree ee DOHR jee kah-BEH-sah DEHS-jee OH(n)-tay(n).", "I've had a fever and a headache since yesterday."),
                X("Dói aqui, quando eu engulo.", "doy ah-KEE, KWAHN-doo eh-oo en-GOO-loo.", "It hurts here, when I swallow."),
                X("Há quanto tempo você está assim?", "ah KWAHN-too TEH(n)-poo voh-SEH es-TAH ah-SEE(n)?", "How long have you been like this?")],
                [("Tenho dor na cabeça minha.", "Tenho dor de cabeça.", "The fixed phrase is dor de cabeça."),
                 ("Estou com febre há dois dias atrás.", "Estou com febre há dois dias.", "Há already means up to now; atrás is wrong here.")]),
              [D("Médica", "O que você está sentindo?", "oo kee voh-SEH es-TAH sen-TEEN-doo?", "What are you feeling?"),
               D("Paciente", "Estou com febre e dor de garganta.", "es-TOH koh(n) FEH-bree ee DOHR jee gahr-GAHN-tah.", "I have a fever and a sore throat."),
               D("Médica", "Há quanto tempo?", "ah KWAHN-too TEH(n)-poo?", "How long?"),
               D("Paciente", "Desde anteontem. Dói quando engulo.", "DEHS-jee ahn-teh-OHN-tay(n). doy KWAHN-doo en-GOO-loo.", "Since the day before yesterday. It hurts when I swallow.")],
              WS("Symptoms worksheet", [
                  T("Describe the symptom.", ["I've had a fever and a headache since yesterday", "it hurts here when I swallow"],
                    ["Estou com febre e dor de cabeça desde ontem", "Dói aqui quando engulo"]),
                  T("Ask about duration.", ["how long have you been like this?", "since the day before yesterday"],
                    ["Há quanto tempo você está assim?", "Desde anteontem"]),
              ])),
            L("Na farmácia",
              "The pharmacy counter asks com receita ou sem receita? Receita is the prescription; "
              "comprimido is a pill and gotas are drops. Dosage is said with de: de oito em oito "
              "horas. Take the instruction literally: em jejum means before eating.",
              [V("a receita", "ah heh-SAY-tah", "prescription", "noun"),
               V("o comprimido", "oo koh(n)-pree-MEE-doo", "pill", "noun"),
               V("as gotas", "ahs GOH-tahs", "drops", "noun"),
               V("o xarope", "oo shah-ROH-pee", "syrup", "noun"),
               V("em jejum", "ey(n) zheh-ZHOO(n)", "on an empty stomach", "phrase")],
              G("Asking at the pharmacy",
                "tem algo para …? · de oito em oito horas · com receita",
                "Tem algo para dor de cabeça? asks for a product, tempero. Dosage intervals use "
                "de X em X horas. Com receita is required for antibiotics; sem receita covers "
                "the rest. Em jejum and depois de comer place the dose around meals.",
                [X("Tem algo para dor de garganta?", "tay(n) AH-oo-goo pah-rah DOHR jee gahr-GAHN-tah?", "Do you have something for a sore throat?"),
                X("Tome um comprimido de oito em oito horas.", "TOH-mee oo(n) koh(n)-pree-MEE-doo jee OY-too ey(n) OY-too OH-rahs.", "Take one pill every eight hours."),
                X("Este xarope é em jejum.", "ES-jee shah-ROH-pee eh ey(n) zheh-ZHOO(n).", "This syrup is taken on an empty stomach.")],
                [("Tome de oito horas em oito?", "Tome de oito em oito horas.", "The fixed pattern is de oito em oito horas."),
                 ("Precisa receita para comprar?", "Precisa de receita para comprar?", "Precisar takes de: precisa de receita.")]),
              [D("Farmacêutico", "Posso ajudar?", "POH-soo ah-zhoo-DAHR?", "Can I help?"),
               D("Cliente", "Tem algo para dor de garganta?", "tay(n) AH-oo-goo pah-rah DOHR jee gahr-GAHN-tah?", "Do you have something for a sore throat?"),
               D("Farmacêutico", "Tem este xarope, sem receita.", "tay(n) ES-jee shah-ROH-pee, sey(n) heh-SAY-tah.", "We have this syrup, no prescription needed."),
               D("Cliente", "Como eu tomo?", "KOH-moo eh-oo TOH-moo?", "How do I take it?"),
               D("Farmacêutico", "De oito em oito horas, depois de comer.", "jee OY-too ey(n) OY-too OH-rahs, deh-POYS jee koh-MEHR.", "Every eight hours, after eating.")],
              WS("Pharmacy worksheet", [
                  T("Ask for the medicine.", ["do you have something for a sore throat?", "do I need a prescription?"],
                    ["Tem algo para dor de garganta?", "Precisa de receita?"]),
                  T("Give the dosage.", ["one pill every eight hours", "this syrup is taken on an empty stomach"],
                    ["Um comprimido de oito em oito horas", "Este xarope é em jejum"]),
              ])),
            L("Marcar consulta no posto",
              "At a public health post (posto de saúde) you queue or book: queria marcar uma "
              "consulta. Convênio is private insurance, and the post asks tem convênio? The "
              "sentence encaminhamento (referral) matters if you need a specialist; atender "
              "(to see a patient) is what the doctor does.",
              [V("a consulta", "ah koh(n)-SOO-tah", "appointment, consultation", "noun"),
               V("o posto", "oo POHS-too", "health post", "noun"),
               V("o convênio", "oo koh(n)-VEH-nee-oo", "health plan", "noun"),
               V("o encaminhamento", "oo en-kah-mee-nyah-MEN-too", "referral", "noun"),
               V("atender", "ah-ten-DEHR", "to see, to attend", "verb")],
              G("Booking at the health post",
                "queria marcar uma consulta · tem convênio? · preciso de encaminhamento",
                "Queria marcar is the polite request at every counter. Preciso de + noun states "
                "the need; para + infinitive adds the reason: preciso de encaminhamento para o "
                "ortopedista. Atender means the doctor will see you: a doutora atende hoje.",
                [X("Queria marcar uma consulta com a clínica geral.", "keh-REE-ah mahr-KAHR OO-mah koh(n)-SOO-tah koh(n) ah KLEE-nee-kah zheh-RAH-oo.", "I'd like to book an appointment with the GP."),
                X("Preciso de encaminhamento para o ortopedista.", "preh-SEE-zoo jee en-kah-mee-nyah-MEN-too pah-rah oo or-toh-peh-JEES-tah.", "I need a referral to the orthopaedist."),
                X("A doutora atende hoje à tarde?", "ah doh-TOH-rah ah-TEN-jee OH-jee ah TAHR-jee?", "Does the doctor see patients this afternoon?")],
                [("Queria marcar uma consulta para o médico.", "Queria marcar uma consulta com o médico.", "You book with (com) a doctor, not para."),
                 ("Preciso encaminhamento.", "Preciso de encaminhamento.", "Precisar takes de.")]),
              [D("Recepcionista", "Posto São Lucas, bom dia.", "POHS-too sow(n) LOO-kahs, boh(n) DEE-ah.", "São Lucas health post, good morning."),
               D("Paciente", "Bom dia, queria marcar uma consulta.", "boh(n) DEE-ah, keh-REE-ah mahr-KAHR OO-mah koh(n)-SOO-tah.", "Good morning, I'd like to book an appointment."),
               D("Recepcionista", "Tem convênio?", "tay(n) koh(n)-VEH-nee-oo?", "Do you have a health plan?"),
               D("Paciente", "Não, é pelo posto. A doutora atende hoje?", "now(n), eh PEH-loo POHS-too. ah doh-TOH-rah ah-TEN-jee OH-jee?", "No, through the post. Does the doctor see patients today?")],
              WS("Health post worksheet", [
                  T("Book the appointment.", ["I'd like to book an appointment with the GP", "I need a referral to the orthopaedist"],
                    ["Queria marcar uma consulta com a clínica geral", "Preciso de encaminhamento para o ortopedista"]),
                  T("Ask about the plan.", ["do you have a health plan?", "does the doctor see patients this afternoon?"],
                    ["Tem convênio?", "A doutora atende hoje à tarde?"]),
              ])),
        ]},
        {"id": "A2+-U3", "title": "Trabalho e estudo", "lessons": [
            L("Falar do trabalho",
              "Work is described with four nouns: o cargo (role), a empresa (company), a jornada "
              "(working hours) and o turno (shift). Trabalho em/na + place says where; trabalho "
              "como + role says what. Home office entered Portuguese unchanged.",
              [V("o cargo", "oo KAH-gyoo", "role, position", "noun"),
               V("a empresa", "ah ey(n)-PREH-zah", "company", "noun"),
               V("a jornada", "ah zhohr-NAH-dah", "working hours", "noun"),
               V("o turno", "oo TOOR-noo", "shift", "noun"),
               V("o escritório", "oo es-kree-TOH-ree-oo", "office", "noun")],
              G("Describing your job",
                "trabalho como … · trabalho em … · de segunda a sexta",
                "Trabalho como + role and trabalho em + place can both be said. The schedule uses "
                "de … a …: de segunda a sexta, das nove às dezoito. Turno da noite means night "
                "shift; meio período is half-time.",
                [X("Trabalho como analista numa empresa de tecnologia.", "trah-BAH-lyoo KOH-moo ah-nah-LEES-tah NOO-mah ey(n)-PREH-zah jee teh-koo-loh-ZHEE-ah.", "I work as an analyst at a technology company."),
                X("Minha jornada é de segunda a sexta, das nove às dezoito.", "MEE-nyah zhohr-NAH-dah eh jee seh-GOON-dah ah SEHS-tah, dahs NOH-vee ahs jee-oh-EE-toh.", "My hours are Monday to Friday, nine to six."),
                X("Faço dois dias de home office e o resto no escritório.", "FAH-soo doys DEE-ahs jee oh(n) OH-fees ee oo HEHS-too noo es-kree-TOH-ree-oo.", "I work two days from home and the rest at the office.")],
                [("Trabalho como em uma empresa.", "Trabalho numa empresa.", "Como takes a role, em takes a place — not both."),
                 ("Minha jornada é das nove dezoito hora.", "Minha jornada é das nove às dezoito.", "The range is das … às …")]),
              [D("Ana", "O que você faz?", "oo kee voh-SEH fahs?", "What do you do?"),
               D("Rafael", "Sou analista numa empresa de tecnologia.", "soh ah-nah-LEES-tah NOO-mah ey(n)-PREH-zah jee teh-koo-loh-ZHEE-ah.", "I'm an analyst at a technology company."),
               D("Ana", "E qual é a jornada?", "ee kwah-oo eh ah zhohr-NAH-dah?", "And what are the hours?"),
               D("Rafael", "Das nove às dezoito, com dois dias de home office.", "dahs NOH-vee ahs jee-oh-EE-toh, koh(n) doys DEE-ahs jee oh(n) OH-fees.", "Nine to six, with two days working from home.")],
              WS("Work worksheet", [
                  T("Say what you do.", ["I work as an analyst at a technology company", "my hours are Monday to Friday"],
                    ["Trabalho como analista numa empresa de tecnologia", "Minha jornada é de segunda a sexta"]),
                  T("Describe the arrangement.", ["nine to six", "two days from home"],
                    ["das nove às dezoito", "dois dias de home office"]),
              ])),
            L("Currículo e entrevista",
              "An interview has a script: fale um pouco sobre você, qual foi seu último desafio, "
              "por que quer trabalhar aqui?. Experience is a experiência, a vaga is the vacancy, "
              "and a pretensão salarial is the expected salary — the question that ends the "
              "interview and must be answered with a range.",
              [V("o currículo", "oo koo-HEE-koo-loo", "CV, résumé", "noun"),
               V("a vaga", "ah VAH-gah", "vacancy", "noun"),
               V("a experiência", "ah es-peh-ree-EHN-see-ah", "experience", "noun"),
               V("o desafio", "oo deh-zah-FEE-oo", "challenge", "noun"),
               V("a pretensão salarial", "ah preh-ten-SOW(n) sah-lah-ree-AH-oo", "salary expectation", "noun")],
              G("Interview language",
                "conte um pouco sobre a sua trajetória · por que essa vaga? · pretensão salarial",
                "Conte sobre + noun invites a story, not a list. Por que essa vaga? expects a "
                "reason connected to the company. Pretensão salarial is answered with a range: "
                "entre X e Y. A trajetória is the professional path.",
                [X("Conte um pouco sobre a sua trajetória.", "KOHN-jee oo(n) POH-koo SOH-bree ah SOO-ah trah-zheh-TOH-ree-ah.", "Tell us a little about your career path."),
                X("Meu último desafio foi liderar uma migração.", "meh-oo OO(oo)-tee-moo deh-zah-FEE-oo foy lee-deh-RAHR OO-mah mee-grah-SOW(n).", "My last challenge was leading a migration."),
                X("Minha pretensão fica entre oito e dez mil.", "MEE-nyah preh-ten-SOW(n) FEE-kah EH(n)-tree OY-too ee days MEE-oo.", "My expectation is between eight and ten thousand.")],
                [("Quero saber qual é sua pretensão salarial ganhar.", "Qual é a sua pretensão salarial?", "One question, one verb."),
                 ("Trabalhei em três empresas diferentes lugares.", "Trabalhei em três empresas diferentes.", "Diferentes already covers it; no second noun.")]),
              [D("Entrevistadora", "Fale sobre sua experiência.", "FAH-lee SOH-bree SOO-ah es-peh-ree-EHN-see-ah.", "Tell me about your experience."),
               D("Candidato", "Trabalhei cinco anos com dados e liderei uma migração.", "trah-bah-LYAY SEEN-koo AH-noos koh(n) DAH-doos ee lee-deh-RAY OO-mah mee-grah-SOW(n).", "I worked five years with data and led a migration."),
               D("Entrevistadora", "E qual é a pretensão salarial?", "ee kwah-oo eh ah preh-ten-SOW(n) sah-lah-ree-AH-oo?", "And what is your salary expectation?"),
               D("Candidato", "Entre oito e dez mil, dependendo do pacote.", "EH(n)-tree OY-too ee days MEE-oo, deh-pen-DEH(n)-doo doo pah-KOH-jee.", "Between eight and ten thousand, depending on the package.")],
              WS("Interview worksheet", [
                  T("Talk about your experience.", ["I worked five years with data", "my last challenge was leading a migration"],
                    ["Trabalhei cinco anos com dados", "Meu último desafio foi liderar uma migração"]),
                  T("Answer about salary.", ["between eight and ten thousand", "depending on the package"],
                    ["Entre oito e dez mil", "dependendo do pacote"]),
              ])),
            L("Curso e horário",
              "A course comes with its own vocabulary: a matrícula (enrolment), a mensalidade "
              "(monthly fee), o nivelamento (placement test) and a turma (class group). Fazer um "
              "curso is the verb, and as aulas são às terças places the timetable.",
              [V("a matrícula", "ah mah-TREE-koo-lah", "enrolment", "noun"),
               V("a mensalidade", "ah mehn-sah-lee-DAH-jee", "monthly fee", "noun"),
               V("o nivelamento", "oo nee-veh-lah-MEN-too", "placement test", "noun"),
               V("a turma", "ah TOOR-mah", "class, group", "noun"),
               V("a aula", "ah AH-oo-lah", "lesson, class", "noun")],
              G("Talking about a course",
                "fazer um curso · a mensalidade é · as aulas são às terças",
                "Fazer um curso (not tomar) is the collocation. The days of the week take na/às: "
                "as aulas são na terça, às dezenove. A turma is the group you join; a vaga na "
                "turma is a place in it.",
                [X("Quero fazer um curso de espanhol à noite.", "KEH-roo fah-ZEHR oo(n) KOOR-soo jee es-pah-NYOH-oo ah NOY-jee.", "I want to take an evening Spanish course."),
                X("A mensalidade é trezentos reais e as aulas são duas vezes por semana.", "ah mehn-sah-lee-DAH-jee eh treh-ZEH(n)-toos heh-AH-ees ee ahs AH-oo-lahs sow(n) DOO-ahs VEH-zees pohr seh-MAH-nah.", "The monthly fee is three hundred reais and classes are twice a week."),
                X("Preciso fazer o nivelamento antes da matrícula.", "preh-SEE-zoo fah-ZEHR oo nee-veh-lah-MEN-too AH(n)-jees dah mah-TREE-koo-lah.", "I need to take the placement test before enrolling.")],
                [("Vou tomar um curso de inglês.", "Vou fazer um curso de inglês.", "Courses are feito, not tomado."),
                 ("As aulas são em as terças.", "As aulas são nas terças.", "The article contracts: nas terças.")]),
              [D("Secretária", "Boa tarde, quer fazer a matrícula?", "BOH-ah TAHR-jee, kehr fah-ZEHR ah mah-TREE-koo-lah?", "Good afternoon, would you like to enrol?"),
               D("Aluno", "Quero. Qual é a mensalidade?", "KEH-roo. kwah-oo eh ah mehn-sah-lee-DAH-jee?", "Yes. What is the monthly fee?"),
               D("Secretária", "Trezentos, duas aulas por semana.", "treh-ZEH(n)-toos, DOO-ahs AH-oo-lahs pohr seh-MAH-nah.", "Three hundred, two classes a week."),
               D("Aluno", "E quando é o nivelamento?", "ee KWAHN-doo eh oo nee-veh-lah-MEN-too?", "And when is the placement test?")],
              WS("Course worksheet", [
                  T("Ask about the course.", ["I want to take an evening Spanish course", "what is the monthly fee?"],
                    ["Quero fazer um curso de espanhol à noite", "Qual é a mensalidade?"]),
                  T("Fix the timetable.", ["the classes are twice a week", "I need to take the placement test"],
                    ["As aulas são duas vezes por semana", "Preciso fazer o nivelamento"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Brazilian shops live on a layaway and exchange culture older than the credit "
                 "card: the nota fiscal is kept in the wallet for the whole prazo de troca, and "
                 "the phrase está dentro do prazo settles most counter disputes. Sunday lunches "
                 "and Saturday feiras aside, the other fixed point of the week is the posto de "
                 "saúde queue, where the first question is sempre tem convênio? — the health "
                 "plan being as much a marker of class as of coverage."),
        source_url="https://en.wikipedia.org/wiki/Health_care_in_Brazil",
        reading=("No sábado eu fui ao centro trocar uma camisa que ficou apertada. Levei a nota "
                 "fiscal e a atendente confirmou que estava dentro do prazo. Como não tinha "
                 "número maior, ela ofereceu um crédito na loja. Depois passei na farmácia: "
                 "estou com dor de garganta e comprei um xarope sem receita. O farmacêutico "
                 "explicou: de oito em oito horas, depois de comer."),
        reading_gloss=("On Saturday I went downtown to exchange a shirt that was tight. I took "
                       "the receipt and the assistant confirmed it was within the period. As "
                       "there was no bigger size, she offered store credit. Then I stopped at "
                       "the pharmacy: I have a sore throat and bought a syrup without a "
                       "prescription. The pharmacist explained: every eight hours, after eating."),
        listening=("Bom dia, queria trocar este sapato. — Tem a nota fiscal? — Tenho. — Está "
                   "dentro do prazo. Tem número maior? — Não tenho, mas posso dar um crédito na "
                   "loja. — Está bom, obrigado."),
        listening_gloss=("Good morning, I'd like to exchange these shoes. — Do you have the "
                         "receipt? — I do. — It's within the period. Do you have a bigger size? "
                         "— I don't, but I can give you store credit. — That's fine, thank you."),
        voice_tag=VOICE,
        idioms=[
            ("na hora", "in the hour", "right then, on the spot"),
            ("dar um jeito", "to give a way", "to sort something out"),
            ("dentro do prazo", "within the deadline", "still inside the allowed period"),
            ("de oito em oito horas", "from eight to eight hours", "every eight hours"),
            ("em jejum", "in fasting", "on an empty stomach"),
            ("ficar de olho", "to keep an eye", "to watch the price or the queue"),
            ("quebrar o galho", "to break the branch", "to help out with a temporary fix"),
            ("botar a mão", "to put the hand", "to pay for it yourself"),
            ("sem receita", "without prescription", "bought over the counter"),
            ("vale a pena", "it is worth the pain", "worth it"),
        ],
        mistakes=[
            ("Vou tomar um curso de espanhol.", "Vou fazer um curso de espanhol.", "Courses are feito in Portuguese."),
            ("Preciso encaminhamento para o médico.", "Preciso de encaminhamento para o médico.", "Precisar takes the preposition de."),
            ("Tenho dor na cabeça.", "Tenho dor de cabeça.", "The body-part phrase is dor de + part."),
        ],
        task_title="Uma semana de recados",
        task_instructions=("Write three short messages: as a shopper asking to exchange an item "
                           "inside the period, as a patient booking an appointment at the posto, "
                           "and as a candidate answering a pretensão salarial. Each one must use "
                           "queria for the request, one number (size, time or salary range) and "
                           "the correct preposition test: trocar por, consulta com, de receita. "
                           "Read them aloud and check the agreement of the adjectives."),
    ),
    "test": [
        ("translate_en", "Say: I'd like to exchange this shirt.", "Queria trocar esta camisa."),
        ("translate_pt", "Está dentro do prazo de troca.", "It's within the exchange period."),
        ("multiple_choice", "Which question asks for a bigger size?", "Tem um número maior?"),
        ("fill_in_the_blank", "Estou ___ febre desde ontem.", "com"),
        ("word_selection", "Select the Portuguese for 'prescription'.", "a receita"),
        ("error_correction", "Eu gosto uma camisa azul.", "Eu gosto de uma camisa azul."),
        ("dialogue_completion", "Complete: Quer experimentar no provador? — ___ (Yes, please)", "Quero, por favor"),
        ("matching", "Match pretensão salarial to its meaning.", "salary expectation"),
        ("reading_comprehension", "No texto, por que a loja não trocou a camisa por outra?", "there was no bigger size"),
        ("inference", "A atendente ofereceu crédito na loja. What does that tell us about the shop?", "it keeps the purchase instead of refunding it"),
        ("main_idea", "O texto conta um sábado de trocas e remédios. — what is this sentence?", "the main point of the reading"),
        ("detail_identification", "Como o farmacêutico mandou tomar o xarope?", "every eight hours, after eating"),
    ],
}


HALFSTEPS["B1+"] = {
    "native": NATIVE,
    "title": "%s B1+ — Cidade, relações e opinião" % NAME,
    "goals": [
        "Move around a big city with buses, metro and apps, and ask for help when it goes wrong",
        "Make friends at work, celebrate, and repair a misunderstanding",
        "Follow the news, give an opinion and recommend a series",
    ],
    "units": [
        {"id": "B1+-U1", "title": "Cidade e deslocamento", "lessons": [
            L("Transporte público e baldeação",
              "In São Paulo the bus has a bilhete único and a catraca; in Rio the metro goes to "
              "the beach. Baldeação is the transfer, and the announcement você deve descer na "
              "próxima estação uses dever to instruct. Linha is the route and sentido tells you "
              "which way it runs.",
              [V("a catraca", "ah kah-TRAH-kah", "turnstile", "noun"),
               V("a baldeação", "ah bah-oo-deh-ah-SOW(n)", "transfer between lines", "noun"),
               V("a linha", "ah LEE-nyah", "line, route", "noun"),
               V("o sentido", "oo sen-TEE-doo", "direction", "noun"),
               V("o bilhete", "oo bee-LYEH-jee", "ticket", "noun")],
              G("Taking public transport",
                "pegar a linha … · fazer baldeação · sentido centro · recarregar o bilhete",
                "Pegar is the verb for buses and metro: pego o metrô. Sentido + place says the "
                "direction: sentido centro. Fazer baldeação names the transfer, and the "
                "instruction to get off uses descer na estação.",
                [X("Pego o metrô e faço baldeação na Sé.", "PEH-goo oo meh-TROH ee FAH-soo bah-oo-deh-ah-SOW(n) nah SEH.", "I take the metro and transfer at Sé."),
                X("Qual é o sentido deste trem?", "kwah-oo eh oo sen-TEE-doo DEHS-jee trey(n)?", "Which direction is this train going?"),
                X("Preciso recarregar o bilhete na máquina.", "preh-SEE-zoo heh-kah-reh-GAHR oo bee-LYEH-jee nah MAH-kee-nah.", "I need to top up the ticket at the machine.")],
                [("Eu vou de pé no ônibus para o metrô.", "Vou pegar o ônibus e depois o metrô.", "Pegar is the verb for taking transport."),
                 ("Faço baldeação para a linha azul sentido.", "Faço baldeação para a linha azul, sentido centro.", "Sentido needs its destination.")]),
              [D("Visitante", "Como eu chego ao centro?", "KOH-moo eh-oo SHEH-goo ah-oo SEHN-troo?", "How do I get downtown?"),
               D("Morador", "Pega a linha azul sentido centro e desce na Sé.", "PEH-gah ah LEE-nyah ah-ZOO-oo sen-TEE-doo SEHN-troo ee DEH-see nah SEH.", "Take the blue line towards the centre and get off at Sé."),
               D("Visitante", "Preciso fazer baldeação?", "preh-SEE-zoo fah-ZEHR bah-oo-deh-ah-SOW(n)?", "Do I need to transfer?"),
               D("Morador", "Só se você for para a zona oeste.", "soh see voh-SEH fohr pah-rah ah ZOH-nah oh-EHS-jee.", "Only if you're going to the west zone.")],
              WS("Transport worksheet", [
                  T("Ask the way.", ["how do I get downtown?", "which direction is this train going?"],
                    ["Como eu chego ao centro?", "Qual é o sentido deste trem?"]),
                  T("Describe the trip.", ["I take the metro and transfer at Sé", "I need to top up the ticket"],
                    ["Pego o metrô e faço baldeação na Sé", "Preciso recarregar o bilhete"]),
              ])),
            L("Trânsito e aplicativos",
              "An app ride is a corrida: o motorista está chegando, o ponto de encontro is where "
              "you meet, and a rua sem saída is a dead end. Traffic is o trânsito, congestion is "
              "engarrafamento, and the driver asks você está onde? when the map disagrees.",
              [V("o aplicativo", "oo ah-plee-kah-TEE-voo", "app", "noun"),
               V("a corrida", "ah koh-HEE-dah", "ride, trip", "noun"),
               V("o motorista", "oo moh-toh-REES-tah", "driver", "noun"),
               V("o engarrafamento", "oo ey(n)-gah-hah-fah-MEN-too", "traffic jam", "noun"),
               V("o ponto de encontro", "oo POHN-too jee en-KOHN-troo", "meeting point", "noun")],
              G("Ordering and taking a ride",
                "chamar um carro · estou no ponto de encontro · tem engarrafamento",
                "Chamar um carro is to order a ride. The driver's messages use the progressive: "
                "estou chegando. The pickup is a fixed phrase: o ponto de encontro é na esquina. "
                "Tem engarrafamento explains a delay without blaming anyone.",
                [X("Chamei um carro, mas tem engarrafamento.", "shah-MAY oo(n) KAH-hoo, mahs tay(n) ey(n)-gah-hah-fah-MEN-too.", "I ordered a car, but there's a traffic jam."),
                X("Estou no ponto de encontro, na esquina do mercado.", "es-TOH noo POHN-too jee en-KOHN-troo, nah es-KEE-nah doo mehr-KAH-doo.", "I'm at the meeting point, on the corner by the market."),
                X("O motorista cancelou a corrida.", "oo moh-toh-REES-tah kahn-seh-LOH ah koh-HEE-dah.", "The driver cancelled the ride.")],
                [("Vou chamar um carro para me levar eu.", "Vou chamar um carro para me levar.", "The reflexive already marks the person."),
                 ("Tem muito engarrafamento no rua.", "Tem muito engarrafamento na rua.", "Rua is feminine: na rua.")]),
              [D("Motorista", "Boa noite, estou chegando ao ponto.", "BOH-ah NOY-jee, es-TOH sheh-GAHN-doo ah-oo POHN-too.", "Good evening, I'm arriving at the point."),
               D("Passageira", "Estou na esquina do mercado, de blusa vermelha.", "es-TOH nah es-KEE-nah doo mehr-KAH-doo, jee BLOO-zah vehr-MEH-lyah.", "I'm on the corner by the market, in a red blouse."),
               D("Motorista", "Vou demorar cinco minutos, tem engarrafamento.", "voh deh-moh-RAHR SEEN-koo mee-NOO-toos, tay(n) ey(n)-gah-hah-fah-MEN-too.", "I'll be five minutes, there's traffic."),
               D("Passageira", "Sem problema, eu espero.", "sey(n) proh-BLEH-mah, eh-oo es-PEH-roo.", "No problem, I'll wait.")],
              WS("App ride worksheet", [
                  T("Give your location.", ["I'm at the meeting point on the corner by the market", "I'm on the corner in a red blouse"],
                    ["Estou no ponto de encontro na esquina do mercado", "Estou na esquina de blusa vermelha"]),
                  T("Explain the delay.", ["there's a traffic jam", "the driver cancelled the ride"],
                    ["Tem engarrafamento", "O motorista cancelou a corrida"]),
              ])),
            L("Morar na cidade grande",
              "Living in a big city is discussed with three complaints and one relief: o barulho "
              "(noise), o aluguel (rent), a distância (distance) and a vizinhança (neighbourhood). "
              "Vale a pena morar perto do metrô even if the rent is higher — the phrase is the "
              "whole argument.",
              [V("o barulho", "oo bah-ROO-lyoo", "noise", "noun"),
               V("o aluguel", "oo ah-loo-GEH-oo", "rent", "noun"),
               V("a vizinhança", "ah vee-zee-NYAHN-sah", "neighbourhood", "noun"),
               V("a distância", "ah jees-TAHN-see-ah", "distance", "noun"),
               V("vale a pena", "VAH-lee ah PEH-nah", "it is worth it", "phrase")],
              G("Weighing life in the city",
                "por um lado … por outro … · vale a pena · apesar de + noun",
                "Por um lado and por outro structure a trade-off without taking sides. Apesar de "
                "+ noun or infinitive concedes: apesar do barulho. Vale a pena + infinitive gives "
                "the verdict, and perto de/longe de place the flat.",
                [X("Por um lado o aluguel é alto, por outro fico perto do trabalho.", "pohr oo(n) LAH-doo oo ah-loo-GEH-oo eh AH-oo-too, pohr OH-troo FEE-koo PEHR-too doo trah-BAH-lyoo.", "On one hand the rent is high, on the other I live close to work."),
                X("Apesar do barulho, a vizinhança é boa.", "ah-peh-ZAHR doo bah-ROO-lyoo, ah vee-zee-NYAHN-sah eh BOH-ah.", "Despite the noise, the neighbourhood is good."),
                X("Vale a pena morar perto do metrô.", "VAH-lee ah PEH-nah moh-RAHR PEHR-too doo meh-TROH.", "It's worth living near the metro.")],
                [("Apesar de o barulho, gosto daqui.", "Apesar do barulho, gosto daqui.", "Apesar de contracts with the article: do."),
                 ("Vale a pena para morar perto.", "Vale a pena morar perto.", "Vale a pena takes a bare infinitive.")]),
              [D("Colega", "Você gosta de morar aqui?", "voh-SEH GOHS-tah jee moh-RAHR ah-KEE?", "Do you like living here?"),
               D("Marina", "Por um lado sim: fico perto do metrô.", "pohr oo(n) LAH-doo see(n): FEE-koo PEHR-too doo meh-TROH.", "On one hand yes: I'm close to the metro."),
               D("Colega", "E por outro?", "ee pohr OH-troo?", "And on the other?"),
               D("Marina", "O aluguel é alto e tem barulho, mas vale a pena.", "oo ah-loo-GEH-oo eh AH-oo-too ee tay(n) bah-ROO-lyoo, mahs VAH-lee ah PEH-nah.", "The rent is high and there's noise, but it's worth it.")],
              WS("City worksheet", [
                  T("Weigh the trade-off.", ["on one hand the rent is high, on the other I live close to work", "despite the noise, the neighbourhood is good"],
                    ["Por um lado o aluguel é alto, por outro fico perto do trabalho", "Apesar do barulho, a vizinhança é boa"]),
                  T("Give the verdict.", ["it's worth living near the metro", "what matters is the distance"],
                    ["Vale a pena morar perto do metrô", "O que importa é a distância"]),
              ])),
        ]},
        {"id": "B1+-U2", "title": "Relações e convites", "lessons": [
            L("Amizade no trabalho",
              "Friendship at work starts with small talk over coffee: o que você faz no fim de "
              "semana? depois a gente marca algo. Marcar algo is loose; marcar um horário is "
              "exact. A colega de trabalho is a colleague; a amiga is the one you call on Sunday.",
              [V("o colega", "oo koh-LEH-gah", "colleague", "noun"),
               V("a conversa", "ah koh(n)-VEHR-sah", "conversation", "noun"),
               V("marcar algo", "mahr-KAHR AH-oo-goo", "to make a loose plan", "phrase"),
               V("o fim de semana", "oo fee(n) jee seh-MAH-nah", "weekend", "noun"),
               V("a amizade", "ah ah-mee-ZAH-jee", "friendship", "noun")],
              G("Making friends at work",
                "depois a gente marca · o que você curte? · me chama no sábado",
                "A gente + third person singular is the spoken we: a gente marca. Depois leaves "
                "the plan open. Curtir (to be into) is the colloquial verb for likes: curto "
                "cinema. Me chama means text or call me.",
                [X("Depois a gente marca um café.", "deh-POYS ah ZHEH(n)-jee MAHR-kah oo(n) kah-FEH.", "Let's plan a coffee later."),
                X("O que você curte fazer no fim de semana?", "oo kee voh-SEH KOOR-jee fah-ZEHR noo fee(n) jee seh-MAH-nah?", "What do you like doing at the weekend?"),
                X("Me chama no sábado que a gente combina.", "mee SHAH-mah noo SAH-bah-doo kee ah ZHEH(n)-jee koh(n)-BEE-nah.", "Message me on Saturday and we'll arrange it.")],
                [("A gente marcamos um café.", "A gente marca um café.", "A gente takes the third person singular."),
                 ("Você curte de cinema?", "Você curte cinema?", "Curtir takes a direct object.")]),
              [D("Rafael", "E aí, o que você curte fazer fora do trabalho?", "ee ah-EE, oo kee voh-SEH KOOR-jee fah-ZEHR FOH-rah doo trah-BAH-lyoo?", "Hey, what do you like doing outside work?"),
               D("Ana", "Curto cinema e corrida no parque.", "KOOR-too see-neh-MAH ee koh-HEE-dah noo PAHR-kee.", "I like cinema and running in the park."),
               D("Rafael", "Legal! Depois a gente marca algo.", "leh-GAH-oo! deh-POYS ah ZHEH(n)-jee MAHR-kah AH-oo-goo.", "Nice! Let's plan something later."),
               D("Ana", "Me chama no sábado.", "mee SHAH-mah noo SAH-bah-doo.", "Message me on Saturday.")],
              WS("Friendship worksheet", [
                  T("Make a loose plan.", ["later let's plan a coffee", "message me on Saturday and we'll arrange it"],
                    ["Depois a gente marca um café", "Me chama no sábado que a gente combina"]),
                  T("Talk about likes.", ["what do you like doing at the weekend?", "I like cinema and running"],
                    ["O que você curte fazer no fim de semana?", "Curto cinema e corrida"]),
              ])),
            L("Festa e presentes",
              "A Brazilian birthday party has a script: parabéns, bolo, velas and the gift. Presente "
              "is the gift, and the polite formula when handing it over is não precisava! — you "
              "didn't have to. Festa de aniversário, churrasco and confraternização are the three "
              "occasions you will be invited to.",
              [V("a festa", "ah FEHS-tah", "party", "noun"),
               V("o presente", "oo preh-ZEH(n)-jee", "gift", "noun"),
               V("o bolo", "oo BOH-loo", "cake", "noun"),
               V("a vela", "ah VEH-lah", "candle", "noun"),
               V("a confraternização", "ah koh(n)-frah-tehr-nee-zah-SOW(n)", "office celebration", "noun")],
              G("At a party",
                "não precisava! · parabéns atrasado · levar um presente",
                "Não precisava! is the fixed reply to any gift. Parabéns for birthdays and "
                "congratulations generally; parabéns atrasado covers a late wish. Vou levar um "
                "presente states your intention before the party.",
                [X("Parabéns! Não precisava de presente.", "pah-rah-BEH(n)s! now(n) preh-see-ZAH-vah jee preh-ZEH(n)-jee.", "Happy birthday! You didn't have to bring a gift."),
                X("Vou levar um presente e um cartão.", "voh leh-VAHR oo(n) preh-ZEH(n)-jee ee oo(n) kahr-TOW(n).", "I'll bring a gift and a card."),
                X("A festa começa às oito, com bolo e velas.", "ah FEHS-tah koh-MEH-sah ahs OY-too, koh(n) BOH-loo ee VEH-lahs.", "The party starts at eight, with cake and candles.")],
                [("Vou levar um presente para dar para ela.", "Vou levar um presente para ela.", "Dar para ela is redundant after levar."),
                 ("Parabéns para o aniversário atrasado.", "Parabéns atrasado.", "The fixed phrase is parabéns atrasado.")]),
              [D("Paulo", "Parabéns! Trouxe um presente.", "pah-rah-BEH(n)s! TROO-see oo(n) preh-ZEH(n)-jee.", "Happy birthday! I brought a gift."),
               D("Marina", "Não precisava! Muito obrigada.", "now(n) preh-see-ZAH-vah! MOOY-too oh-bree-GAH-dah.", "You didn't have to! Thank you so much."),
               D("Paulo", "A festa está ótima. Quem fez o bolo?", "ah FEHS-tah es-TAH OH-tee-mah. key(n) fehs oo BOH-loo?", "The party is great. Who made the cake?"),
               D("Marina", "Minha mãe. Toma um pedaço!", "MEE-nyah MAH(n)-jee. TOH-mah oo(n) peh-DAH-soo!", "My mother. Have a slice!")],
              WS("Party worksheet", [
                  T("Congratulate.", ["happy birthday!", "you didn't have to bring a gift"],
                    ["Parabéns!", "Não precisava de presente"]),
                  T("Say what you brought.", ["I'll bring a gift and a card", "the party starts at eight"],
                    ["Vou levar um presente e um cartão", "A festa começa às oito"]),
              ])),
            L("Mal-entendido e desculpas",
              "A misunderstanding is a mal-entendido, and repairing it has three steps: reconhecer "
              "(acknowledge), explicar sem justificar (explain without excusing) and deixar claro "
              "o que você quis dizer. Pedir desculpas is the act; desculpa is the word used when "
              "you step on someone's foot.",
              [V("o mal-entendido", "oo MAH-oo en-ten-JEE-doo", "misunderstanding", "noun"),
               V("pedir desculpas", "peh-DEER des-KOO-pahs", "to apologise", "phrase"),
               V("deixar claro", "day-SHAHR KLAH-roo", "to make clear", "phrase"),
               V("reconhecer", "heh-koh-nyeh-SEHR", "to acknowledge", "verb"),
               V("o tom", "oo TOH(n)", "tone", "noun")],
              G("Repairing a misunderstanding",
                "foi um mal-entendido · desculpa se eu … · o que eu quis dizer foi …",
                "Desculpa se eu + perfect tense (desculpa se eu pareci ríspida) accepts the "
                "effect without conceding the intention. O que eu quis dizer foi … restates the "
                "message. Reconhecer is stronger than pedir desculpas because it names the fact.",
                [X("Desculpa se eu pareci ríspida, não foi a intenção.", "des-KOO-pah see eh-oo pah-reh-SEE HEES-pee-dah, now(n) foy ah een-ten-SOW(n).", "Sorry if I seemed sharp, that wasn't the intention."),
                X("Foi um mal-entendido: o tom mudou a leitura.", "foy oo(n) MAH-oo en-ten-JEE-doo: oo TOH(n) moo-DOH ah leh-TOO-rah.", "It was a misunderstanding: the tone changed how it was read."),
                X("Reconheço que respondi rápido demais.", "heh-koh-NYEH-soo kee hes-pohn-DEE HAH-pee-doo deh-MAYS.", "I acknowledge that I replied too quickly.")],
                [("Desculpa por eu pareci ríspida.", "Desculpa se eu pareci ríspida.", "The apology pattern is desculpa se eu …"),
                 ("Eu quero dizer foi outra coisa.", "O que eu quis dizer foi outra coisa.", "The corrective frame is o que eu quis dizer foi …")]),
              [D("Ana", "Acho que houve um mal-entendido ontem.", "AH-shoo kee oh-VEH oo(n) MAH-oo en-ten-JEE-doo OH(n)-tay(n).", "I think there was a misunderstanding yesterday."),
               D("Rafael", "Também achei. Desculpa se eu pareci ríspido.", "tah(n)-BEH(n) ah-SHAY. des-KOO-pah see eh-oo pah-reh-SEE HEES-pee-doo.", "I thought so too. Sorry if I seemed sharp."),
               D("Ana", "O que eu quis dizer foi que precisávamos de mais prazo.", "oo kee eh-oo kees jee-ZEHR foy kee preh-see-ZAH-vah-moos jee mays PRAH-zoo.", "What I meant was that we needed more time."),
               D("Rafael", "Agora ficou claro. Vamos seguir.", "ah-GOH-rah fee-KOH KLAH-roo. VAH-moos seh-GEER.", "Now it's clear. Let's move on.")],
              WS("Apology worksheet", [
                  T("Apologise precisely.", ["sorry if I seemed sharp", "I acknowledge that I replied too quickly"],
                    ["Desculpa se eu pareci ríspida", "Reconheço que respondi rápido demais"]),
                  T("Restate the message.", ["what I meant was that we needed more time", "it was a misunderstanding"],
                    ["O que eu quis dizer foi que precisávamos de mais prazo", "Foi um mal-entendido"]),
              ])),
        ]},
        {"id": "B1+-U3", "title": "Mídia e opinião", "lessons": [
            L("Notícias e redes sociais",
              "Reading the news in Portuguese, three words tell you where you are: a manchete "
              "(headline), a reportagem (feature) and o comentário. Nas redes, postar, compartilhar "
              "e comentar are the three actions; a fake news entered the language unchanged.",
              [V("a reportagem", "ah heh-pohr-TAH-zheh(n)", "feature report", "noun"),
               V("postar", "pohs-TAHR", "to post", "verb"),
               V("compartilhar", "koh(n)-pahr-tee-LYAHR", "to share", "verb"),
               V("o comentário", "oo koh-men-TAH-ree-oo", "comment", "noun"),
               V("a fake news", "ah fayk noos", "fake news", "noun")],
              G("Talking about media",
                "saiu uma reportagem · compartilhar sem ler · checar a fonte",
                "Saiu (it came out) is how a publication is announced: saiu uma reportagem no "
                "jornal. The warning checar a fonte (check the source) works as a noun phrase. "
                "Compartilhar takes a direct object: compartilhar o link.",
                [X("Saiu uma reportagem sobre a feira no jornal.", "sah-EE OO-mah heh-pohr-TAH-zheh(n) SOH-bree ah FAY-rah noo zhohr-NAH-oo.", "A report on the market came out in the paper."),
                X("Antes de compartilhar, checa a fonte.", "AH(n)-jees jee koh(n)-pahr-tee-LYAHR, SHEH-kah ah FOHN-jee.", "Before sharing, check the source."),
                X("O comentário recebeu mais atenção que a matéria.", "oo koh-men-TAH-ree-oo heh-seh-BEH-oo mays ah-ten-SOW(n) kee ah mah-TEH-ree-ah.", "The comment got more attention than the article.")],
                [("Saiu uma reportagem na jornal.", "Saiu uma reportagem no jornal.", "Jornal is masculine: no jornal."),
                 ("Compartilhei com o link para meus amigos.", "Compartilhei o link com meus amigos.", "Compartilhar takes the thing directly.")]),
              [D("Ana", "Você viu a reportagem sobre a feira?", "voh-SEH VEE-oo ah heh-pohr-TAH-zheh(n) SOH-bree ah FAY-rah?", "Did you see the report on the market?"),
               D("Rafael", "Vi. Antes de compartilhar, chequei a fonte.", "vee. AH(n)-jees jee koh(n)-pahr-tee-LYAHR, sheh-KAY ah FOHN-jee.", "I did. Before sharing, I checked the source."),
               D("Ana", "E era confiável?", "ee EH-rah koh(n)-fee-AH-veh-oo?", "And was it reliable?"),
               D("Rafael", "Era. Já compartilhei o link no grupo.", "EH-rah. zhah koh(n)-pahr-tee-LYAY oo lee(n)k noo GROO-poo.", "It was. I've already shared the link in the group.")],
              WS("Media worksheet", [
                  T("Announce the piece.", ["a report on the market came out in the paper", "the comment got more attention than the article"],
                    ["Saiu uma reportagem sobre a feira no jornal", "O comentário recebeu mais atenção que a matéria"]),
                  T("Give the warning.", ["before sharing, check the source", "it was reliable"],
                    ["Antes de compartilhar, checa a fonte", "Era confiável"]),
              ])),
            L("Dar opinião e discordar",
              "An opinion opens with na minha opinião or eu acho que, and disagreement is dressed: "
              "entendo, mas vejo diferente; discordo em parte; faz sentido, só que …. Concordo em "
              "parte is the most useful phrase in argument, because it concedes the half that is "
              "true before naming the half that is not.",
              [V("na minha opinião", "nah MEE-nyah oh-pee-nee-OW(n)", "in my opinion", "phrase"),
               V("discordar", "jees-kohr-DAHR", "to disagree", "verb"),
               V("concordar em parte", "koh(n)-kohr-DAHR ey(n) PAHR-jee", "to partly agree", "phrase"),
               V("faz sentido", "fahs seen-TEE-doo", "that makes sense", "phrase"),
               V("porém", "poh-REH(n)", "however", "conjunction")],
              G("Agreeing and disagreeing",
                "concordo em parte · faz sentido, só que … · eu vejo diferente",
                "Concordar and discordar take em: concordo em parte, discordo disso. Só que "
                "introduces the exception after the concession. Eu vejo diferente states the "
                "disagreement without making it personal.",
                [X("Concordo em parte: o problema é o prazo, não a ideia.", "koh(n)-KOHR-doo ey(n) PAHR-jee: oo proh-BLEH-mah eh oo PRAH-zoo, now(n) ah ee-DAY-ah.", "I partly agree: the problem is the deadline, not the idea."),
                X("Faz sentido, só que ninguém citou o custo.", "fahs seen-TEE-doo, soh kee ney(n)-GEH(n) see-TOH oo KOOS-too.", "That makes sense, except nobody mentioned the cost."),
                X("Eu vejo diferente: para mim falta dado.", "eh-oo VEH-zhoo jee-feh-REHN-jee: pah-rah meen FAH-oo-tah DAH-doo.", "I see it differently: for me there's a lack of data.")],
                [("Discordo com essa ideia.", "Discordo dessa ideia.", "Discordar de takes de."),
                 ("Concordo em parte com isso que o prazo.", "Concordo em parte: o problema é o prazo.", "One clause per idea.")]),
              [D("Paulo", "Na minha opinião, a proposta resolve tudo.", "nah MEE-nyah oh-pee-nee-OW(n), ah proh-POHS-tah heh-ZOH-vee TOO-doo.", "In my opinion, the proposal solves everything."),
               D("Marina", "Concordo em parte: o problema é o prazo.", "koh(n)-KOHR-doo ey(n) PAHR-jee: oo proh-BLEH-mah eh oo PRAH-zoo.", "I partly agree: the problem is the deadline."),
               D("Paulo", "Faz sentido, só que o prazo pode ser ajustado.", "fahs seen-TEE-doo, soh kee oo PRAH-zoo POH-jee sehr ah-zhoos-TAH-doo.", "That makes sense, except the deadline can be adjusted."),
               D("Marina", "Eu vejo diferente: para mim falta dado.", "eh-oo VEH-zhoo jee-feh-REHN-jee: pah-rah meen FAH-oo-tah DAH-doo.", "I see it differently: I think there's a lack of data.")],
              WS("Opinion worksheet", [
                  T("Agree in part.", ["I partly agree: the problem is the deadline", "that makes sense, except nobody mentioned the cost"],
                    ["Concordo em parte: o problema é o prazo", "Faz sentido, só que ninguém citou o custo"]),
                  T("Disagree without heat.", ["I see it differently: for me there's a lack of data", "in my opinion, the proposal solves everything"],
                    ["Eu vejo diferente: para mim falta dado", "Na minha opinião, a proposta resolve tudo"]),
              ])),
            L("Séries, podcasts e recomendação",
              "Recommending a series has its own vocabulary: a temporada, o episódio, a legenda "
              "(subtitle) and a dublagem (dubbing). Assistir + a: assisti à série. A recommendation "
              "is made with vale a pena assistir and qualified with se você gosta de ….",
              [V("a temporada", "ah tehn-poh-RAH-dah", "season", "noun"),
               V("o episódio", "oo eh-pee-ZOH-jee-oo", "episode", "noun"),
               V("a legenda", "ah leh-ZHEHN-dah", "subtitle", "noun"),
               V("assistir", "ah-sees-TEER", "to watch", "verb"),
               V("recomendar", "heh-koh-men-DAHR", "to recommend", "verb")],
              G("Recommending something",
                "vale a pena assistir · se você gosta de … · está legendado",
                "Assistir takes a and the article contracts: assisti à série. Ver is the plain "
                "verb for watching anything. Está legendado / está dublado tells you which "
                "version to look for; sem legenda is the harder option.",
                [X("Vale a pena assistir à nova temporada.", "VAH-lee ah PEH-nah ah-sees-TEER ah NOH-vah tehn-poh-RAH-dah.", "The new season is worth watching."),
                X("Se você gosta de documentário, recomendo este.", "see voh-SEH GOHS-tah jee doh-koo-men-TAH-ree-oo, heh-koh-MEH(n)-doo ES-jee.", "If you like documentaries, I recommend this one."),
                X("A série está legendada, sem dublagem.", "ah SEH-ree eh es-TAH leh-zhehn-DAH-dah, sey(n) doo-BLAH-zheh(n).", "The series is subtitled, no dubbing.")],
                [("Assisti a série nova.", "Assisti à série nova.", "Assistir a contracts with the article: à série."),
                 ("Recomendo você assistir de esta série.", "Recomendo esta série para você.", "Recomendar takes the thing as object.")]),
              [D("Ana", "Você assistiu à série nova?", "voh-SEH ah-sees-TEE-oo ah SEH-ree NOH-vah?", "Did you watch the new series?"),
               D("Rafael", "Assisti. Vale a pena, se você gosta de suspense.", "ah-SEES-jee. VAH-lee ah PEH-nah, see voh-SEH GOHS-tah jee soos-PEH(n)-see.", "I did. It's worth it, if you like suspense."),
               D("Ana", "Está legendada?", "es-TAH leh-zhehn-DAH-dah?", "Is it subtitled?"),
               D("Rafael", "Está, mas eu assisti sem legenda.", "es-TAH, mahs eh-oo ah-SEES-jee sey(n) leh-ZHEHN-dah.", "It is, but I watched it without subtitles.")],
              WS("Recommendation worksheet", [
                  T("Recommend.", ["the new season is worth watching", "if you like documentaries, I recommend this one"],
                    ["Vale a pena assistir à nova temporada", "Se você gosta de documentário, recomendo este"]),
                  T("Talk about the version.", ["the series is subtitled, no dubbing", "I watched it without subtitles"],
                    ["A série está legendada, sem dublagem", "Assisti sem legenda"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("The Brazilian city is read through its transport: São Paulo's bilhete único "
                 "charges one fare for bus and metro, Rio's metro reaches the beach, and every "
                 "capital has an app for rides. Meanwhile the conversation that starts over a "
                 "cafezinho at work is the one that ends in a festa de aniversário or a "
                 "confraternização, where the fixed reply to a gift is não precisava! — a "
                 "politeness that names the effort rather than the object."),
        source_url="https://en.wikipedia.org/wiki/Transport_in_Brazil",
        reading=("Moro em São Paulo há três anos e aprendi a me deslocar com o bilhete único. "
                 "De manhã pego a linha azul do metrô e faço baldeação na Sé; o trajeto leva "
                 "quarenta minutos. Aos sábados uso aplicativo, porque o ônibus demora com o "
                 "engarrafamento. O aluguel é alto e a vizinhança é barulhenta, mas vale a pena "
                 "morar perto do metrô: chego em casa em vinte minutos."),
        reading_gloss=("I've lived in São Paulo for three years and I learned to get around with "
                       "the single ticket. In the morning I take the blue metro line and transfer "
                       "at Sé; the trip takes forty minutes. On Saturdays I use an app, because "
                       "the bus is slow with the traffic. The rent is high and the neighbourhood "
                       "is noisy, but it's worth living near the metro: I get home in twenty "
                       "minutes."),
        listening=("Você viu a reportagem sobre a feira? — Vi. Antes de compartilhar, chequei a "
                   "fonte. — E era confiável? — Era. Concordo em parte com o texto, mas vale a "
                   "pena ler."),
        listening_gloss=("Did you see the report on the market? — I did. Before sharing, I "
                         "checked the source. — And was it reliable? — It was. I partly agree "
                         "with the text, but it's worth reading."),
        voice_tag=VOICE,
        idioms=[
            ("dar um rolê", "to take a stroll", "to go out without a fixed plan"),
            ("sair do ar", "to go off the air", "to lose the connection or go silent"),
            ("tá na mão", "it's in the hand", "it's sorted, no problem"),
            ("quebrar o galho", "to break the branch", "to help out for a moment"),
            ("fechar o tempo", "to close the weather", "the sky clouds over before rain"),
            ("na vibe", "in the vibe", "in tune with the mood"),
            ("de boa", "of good", "relaxed, all fine"),
            ("marcar presença", "to mark presence", "to show up briefly"),
            ("dar uma olhada", "to give a look", "to check quickly"),
            ("vale a pena", "it is worth the pain", "worth the effort"),
        ],
        mistakes=[
            ("Discordo com você nesse ponto.", "Discordo de você nesse ponto.", "Discordar takes de."),
            ("Assisti a série ontem.", "Assisti à série ontem.", "Assistir a contracts with the article."),
            ("A gente marcamos às oito.", "A gente marca às oito.", "A gente takes the third person singular."),
        ],
        task_title="Um domingo de cidade grande",
        task_instructions=("Plan a Sunday in a big city in ten lines: the transport you will take "
                           "with one baldeação, an app ride with a meeting point, a party you "
                           "will attend and a series you will recommend. Use at least one "
                           "concession (apesar de, só que, por um lado) and one opinion frame "
                           "(na minha opinião, concordo em parte). Then read it aloud and check "
                           "that a gente, assistir a and discordar de are correct."),
    ),
    "test": [
        ("translate_en", "Say: I take the metro and transfer at Sé.", "Pego o metrô e faço baldeação na Sé."),
        ("translate_pt", "Vale a pena morar perto do metrô.", "It's worth living near the metro."),
        ("multiple_choice", "Which sentence orders a ride?", "Chamei um carro pelo aplicativo."),
        ("fill_in_the_blank", "Prefiro assistir ___ série legendada.", "à"),
        ("word_selection", "Select the Portuguese for 'traffic jam'.", "o engarrafamento"),
        ("error_correction", "Discordo com essa proposta.", "Discordo dessa proposta."),
        ("dialogue_completion", "Complete: Desculpa se eu pareci ríspido. — ___ (It was a misunderstanding)", "Foi um mal-entendido"),
        ("matching", "Match baldeação to its meaning.", "transfer between lines"),
        ("reading_comprehension", "No texto, quanto tempo leva o trajeto de metrô?", "forty minutes"),
        ("inference", "O texto diz que o aluguel é alto e a vizinhança é barulhenta. What does this tell us about the decision to stay?", "the location is worth the trade-off"),
        ("main_idea", "O texto conta como alguém se locomove em São Paulo. — what is this sentence?", "the main point of the reading"),
        ("detail_identification", "Por que a pessoa usa aplicativo aos sábados?", "because the bus is slow in traffic"),
    ],
}


HALFSTEPS["B2+"] = {
    "native": NATIVE,
    "title": "%s B2+ — Trabalho, sociedade e cultura" % NAME,
    "goals": [
        "Give and take feedback, mediate a team conflict and plan a career change",
        "Discuss public policy, inequality and voting with numbers and sources",
        "Read Brazilian literature, music and cinema as arguments about the country",
    ],
    "units": [
        {"id": "B2+-U1", "title": "Trabalho e carreira", "lessons": [
            L("Feedback e metas",
              "Feedback in Brazilian teams is wrapped in a frame: primeiro o reconhecimento, "
              "depois o ponto de melhoria. A meta é SMART, o indicador is the metric, and "
              "acompanhar means to follow up. A avaliação is the formal review; a conversa "
              "franca is the informal one.",
              [V("a meta", "ah MEH-tah", "goal, target", "noun"),
               V("o indicador", "oo een-jee-kah-DOHR", "metric, indicator", "noun"),
               V("acompanhar", "ah-koh(n)-pah-NYAHR", "to follow up", "verb"),
               V("a avaliação", "ah ah-vah-lee-ah-SOW(n)", "review, evaluation", "noun"),
               V("o ponto de melhoria", "oo POHN-too jee meh-lyoh-REE-ah", "area for improvement", "noun")],
              G("Giving feedback",
                "primeiro o reconhecimento, depois o ponto de melhoria · combinamos uma meta · acompanho semanalmente",
                "The sandwich is explicit in Brazilian Portuguese: você fez bem … e no próximo "
                "ciclo podemos …. Combinar uma meta means to agree on it, not to impose it. "
                "Acompanhar takes a direct object: acompanho o indicador.",
                [X("Você conduziu bem a reunião; no próximo ciclo podemos ajustar o prazo.", "voh-SEH koh(n)-doo-ZEE-oo bey(n) ah heh-oo-nee-OW(n); noo PROH-see-moo SEE-kloo poh-DEH-moos ah-zhoos-TAHR oo PRAH-zoo.", "You ran the meeting well; in the next cycle we can adjust the deadline."),
                X("Combinamos uma meta de reduzir o retrabalho em 20%.", "koh(n)-bee-NAH-moos OO-mah MEH-tah jee heh-doo-ZEER oo heh-trah-BAH-lyoo ey(n) VEEN-jee pohr SEHN-too.", "We agreed on a goal of cutting rework by 20%."),
                X("Acompanho o indicador toda sexta e envio o resumo.", "ah-koh(n)-PAH-nyoo oo een-jee-kah-DOHR TOH-dah SEHS-tah ee ey(n)-VEE-oo oo heh-ZOO-moo.", "I follow the metric every Friday and send the summary.")],
                [("Vou combinar você para a meta.", "Vou combinar uma meta com você.", "Combinar takes com for the person."),
                 ("Acompanho de o indicador.", "Acompanho o indicador.", "Acompanhar takes a direct object.")]),
              [D("Gestora", "Como você avalia o ciclo?", "KOH-moo voh-SEH ah-vah-LEE-ah oo SEE-kloo?", "How do you assess the cycle?"),
               D("Rafael", "Cumprimos a meta de prazo, mas o indicador de qualidade caiu.", "koon-PREE-moos ah MEH-tah jee PRAH-zoo, mahs oo een-jee-kah-DOHR jee kwah-lee-DAH-jee kah-EE-oo.", "We met the deadline goal, but the quality metric fell."),
               D("Gestora", "Qual é o ponto de melhoria, na sua visão?", "kwah-oo eh oo POHN-too jee meh-lyoh-REE-ah, nah SOO-ah vee-ZOW(n)?", "What is the area for improvement, in your view?"),
               D("Rafael", "Reduzir o retrabalho. Posso acompanhar semanalmente.", "heh-doo-ZEER oo heh-trah-BAH-lyoo. POH-soo ah-koh(n)-pah-NYAHR seh-mah-NAH-oo-MEN-jee.", "Cutting rework. I can follow it weekly.")],
              WS("Feedback worksheet", [
                  T("Give balanced feedback.", ["you ran the meeting well", "in the next cycle we can adjust the deadline"],
                    ["Você conduziu bem a reunião", "No próximo ciclo podemos ajustar o prazo"]),
                  T("Agree on a goal.", ["we agreed on a goal of cutting rework by 20%", "I follow the metric every Friday"],
                    ["Combinamos uma meta de reduzir o retrabalho em 20%", "Acompanho o indicador toda sexta"]),
              ])),
            L("Conflito no time",
              "Mediating a conflict means separating the positions from the interests: o que você "
              "precisa? and o que ele precisa? Escutar sem interromper is the first instruction, "
              "alinhar expectativas the second. The mediator's sentence is vamos combinar como "
              "decidimos daqui para frente.",
              [V("o conflito", "oo koh(n)-FLEE-too", "conflict", "noun"),
               V("mediar", "meh-jee-AHR", "to mediate", "verb"),
               V("escutar", "es-koo-TAHR", "to listen", "verb"),
               V("alinhar", "ah-lee-NYAHR", "to align", "verb"),
               V("a expectativa", "ah es-peh-k-tah-TEE-vah", "expectation", "noun")],
              G("Mediating a conflict",
                "o que você precisa? · vamos separar posição de interesse · como decidimos daqui para frente?",
                "The intervention is framed as a question so that both sides speak: o que você "
                "precisa para destravar? Separar posição de interesse is the mediator's move. "
                "Alinhar expectativas takes com: alinhar expectativas com o time.",
                [X("Vamos separar posição de interesse antes de decidir.", "VAH-moos seh-pah-RAHR poh-zee-SOW(n) jee een-teh-REH-see AH(n)-jees jee deh-see-JEER.", "Let's separate position from interest before deciding."),
                X("O que você precisa para destravar o trabalho?", "oo kee voh-SEH preh-SEE-zah pah-rah des-trah-VAHR oo trah-BAH-lyoo?", "What do you need to unblock the work?"),
                X("Alinhamos expectativas com o time na reunião.", "ah-lee-NYAH-moos es-peh-k-tah-TEE-vahs koh(n) oo CHEE-mee nah heh-oo-nee-OW(n).", "We aligned expectations with the team in the meeting.")],
                [("Vamos alinhar as expectativas do time com o time.", "Vamos alinhar expectativas com o time.", "One reference to the team is enough."),
                 ("Escuto sem interromper é importante.", "Escutar sem interromper é importante.", "The infinitive is the subject, with no pronoun.")]),
              [D("Mediadora", "Vamos começar pelo que cada um precisa.", "VAH-moos koh-meh-SAHR PEH-loo oo kee kah-DAH oo(n) preh-SEE-zah.", "Let's start with what each of you needs."),
               D("Ana", "Preciso de prazo realista para revisar.", "preh-SEE-zoo jee PRAH-zoo heh-ah-LEES-tah pah-rah heh-vee-ZAHR.", "I need a realistic deadline to review."),
               D("Paulo", "E eu preciso de resposta rápida para não travar.", "ee eh-oo preh-SEE-zoo jee hes-POHS-tah HAH-pee-dah pah-rah now(n) trah-VAHR.", "And I need a quick answer so I don't get stuck."),
               D("Mediadora", "Então combinamos um limite de 24 horas para revisão.", "en-TOW(n) koh(n)-bee-NAH-moos oo(n) lee-MEE-jee jee VEEN-jee KWAH-troo OH-rahs pah-rah heh-vee-ZOW(n).", "Then we agree on a 24-hour limit for the review.")],
              WS("Conflict worksheet", [
                  T("Separate the interests.", ["what do you need to unblock the work?", "I need a realistic deadline to review"],
                    ["O que você precisa para destravar o trabalho?", "Preciso de prazo realista para revisar"]),
                  T("Agree forward.", ["let's separate position from interest before deciding", "we aligned expectations with the team"],
                    ["Vamos separar posição de interesse antes de decidir", "Alinhamos expectativas com o time"]),
              ])),
            L("Transição de carreira",
              "A career change is a project with a vocabulary: a transição, o portfólio, a "
              "requalificação and a ponte (a bridge between what you did and what you want to "
              "do). Falar de transição sem pedir desculpas means naming the transferable skill "
              "directly.",
              [V("a transição", "ah trahn-zee-SOW(n)", "transition", "noun"),
               V("o portfólio", "oo pohr-TFOH-lyoo", "portfolio", "noun"),
               V("a requalificação", "ah heh-kwah-lee-fee-kah-SOW(n)", "reskilling", "noun"),
               V("a ponte", "ah POHN-jee", "bridge", "noun"),
               V("transferível", "trahnz-feh-REE-veh-oo", "transferable", "adjective")],
              G("Talking about a career change",
                "faço a ponte entre … · habilidade transferível · estou em transição desde março",
                "Estou em transição desde … states the period without apologising. A ponte entre "
                "A e B names the link. Habilidade transferível answers the interviewer's real "
                "question. Requalificação is what you did to prepare, not what you lack.",
                [X("Estou em transição de carreira desde março.", "es-TOH ey(n) trahn-zee-SOW(n) jee kah-REH-rah DEHS-jee MAHR-soo.", "I've been changing careers since March."),
                X("Faço a ponte entre suporte e dados.", "FAH-soo ah POHN-jee EH(n)-tree soo-POHR-jee ee DAH-doos.", "I bridge support and data."),
                X("Minha habilidade transferível é documentar processo.", "MEE-nyah ah-bee-lee-DAH-jee trahnz-feh-REE-veh-oo eh doh-koo-men-TAHR proh-SEH-soo.", "My transferable skill is documenting process.")],
                [("Estou em transição para mudar de carreira nova.", "Estou em transição de carreira.", "The phrase already contains carreira."),
                 ("A ponte entre o suporte com dados.", "A ponte entre o suporte e os dados.", "Entre A e B takes e.")]),
              [D("Entrevistadora", "Por que sair da área de suporte?", "pohr-KEH sah-EER dah ah-REH-ah jee soo-POHR-jee?", "Why leave the support area?"),
               D("Candidato", "Não é sair: faço a ponte entre suporte e dados.", "now(n) eh sah-EER: FAH-soo ah POHN-jee EH(n)-tree soo-POHR-jee ee DAH-doos.", "It's not leaving: I bridge support and data."),
               D("Entrevistadora", "E o que você estudou nessa transição?", "ee oo kee voh-SEH es-too-DOH NAH-sah trahn-zee-SOW(n)?", "And what did you study during this transition?"),
               D("Candidato", "Fiz requalificação em análise de dados, com portfólio.", "feez heh-kwah-lee-fee-kah-SOW(n) ey(n) ah-NAH-lee-zee jee DAH-doos, koh(n) pohr-TFOH-lee-oo.", "I did a reskilling course in data analysis, with a portfolio.")],
              WS("Career worksheet", [
                  T("Frame the transition.", ["I've been changing careers since March", "I bridge support and data"],
                    ["Estou em transição de carreira desde março", "Faço a ponte entre suporte e dados"]),
                  T("Name the skill.", ["my transferable skill is documenting process", "I did a reskilling course"],
                    ["Minha habilidade transferível é documentar processo", "Fiz requalificação"]),
              ])),
        ]},
        {"id": "B2+-U2", "title": "Sociedade e política", "lessons": [
            L("Políticas públicas",
              "A policy is discussed through its instruments: o orçamento (budget), a meta, a "
              "fiscalização (oversight) and o repasse (transfer of funds). The question quem "
              "executa? names the level of government, and the phrase na prática tests whether "
              "the text is talking about a law or about a result.",
              [V("a política pública", "ah poh-LEE-tee-kah POO-blee-kah", "public policy", "noun"),
               V("o orçamento", "oo oh(r)-sah-MEN-too", "budget", "noun"),
               V("a fiscalização", "ah fees-kah-lee-zah-SOW(n)", "oversight", "noun"),
               V("o repasse", "oo heh-PAH-see", "transfer of funds", "noun"),
               V("a execução", "ah eh-zeh-koo-SOW(n)", "implementation", "noun")],
              G("Discussing policy",
                "previsto no orçamento · cabe ao município · na prática, a execução é lenta",
                "Prever (to foresee) is the verb of budgets: o orçamento prevê. Cabe a + "
                "government level assigns responsibility: cabe ao município fiscalizar. "
                "Na prática is the hinge that moves from the plan to the result.",
                [X("O orçamento prevê R$ 2 bilhões para a política.", "oo oh(r)-sah-MEN-too preh-VEH heh-AH-ees DOYS bee-LYOH(n)s pah-rah ah poh-LEE-tee-kah.", "The budget foresees 2 billion reais for the policy."),
                X("Cabe ao município a fiscalização dos contratos.", "KAH-bee ah-oo moo-NEE-see-pee-oo ah fees-kah-lee-zah-SOW(n) doos koh(n)-TRAH-toos.", "Oversight of the contracts is up to the municipality."),
                X("Na prática, a execução depende do repasse estadual.", "nah PRAH-tee-kah, ah eh-zeh-koo-SOW(n) deh-PEH(n)-jee doo heh-PAH-see es-tah-doo-AH-oo.", "In practice, implementation depends on the state transfer.")],
                [("O orçamento prevê de dois bilhões.", "O orçamento prevê dois bilhões.", "Prever takes a direct object."),
                 ("Cabe o município fiscalizar.", "Cabe ao município fiscalizar.", "Caber a takes the preposition a.")]),
              [D("Repórter", "O que muda com a nova política?", "oo kee MOO-dah koh(n) ah NOH-vah poh-LEE-tee-kah?", "What changes with the new policy?"),
               D("Gestora", "O orçamento prevê mais fiscalização.", "oo oh(r)-sah-MEN-too preh-VEH mays fees-kah-lee-zah-SOW(n).", "The budget foresees more oversight."),
               D("Repórter", "E quem executa?", "ee key(n) eh-zeh-KOO-tah?", "And who implements it?"),
               D("Gestora", "Cabe ao município, mas na prática depende do repasse.", "KAH-bee ah-oo moo-NEE-see-pee-oo, mahs nah PRAH-tee-kah deh-PEH(n)-jee doo heh-PAH-see.", "It's up to the municipality, but in practice it depends on the transfer.")],
              WS("Policy worksheet", [
                  T("Describe the instrument.", ["the budget foresees 2 billion reais", "oversight of the contracts is up to the municipality"],
                    ["O orçamento prevê R$ 2 bilhões", "Cabe ao município a fiscalização dos contratos"]),
                  T("Move from plan to practice.", ["in practice, implementation depends on the state transfer", "who implements it?"],
                    ["Na prática, a execução depende do repasse estadual", "Quem executa?"]),
              ])),
            L("Desigualdade e dados",
              "Inequality is argued with indicators: a renda média, o índice de Gini, a linha de "
              "pobreza. The methodological caution is the phrase a média esconde — an average "
              "hides the distribution — and recorte means the cut of the data you are looking at. "
              "O recorte de renda changes everything.",
              [V("a renda", "ah HEHN-dah", "income", "noun"),
               V("o indicador social", "oo een-jee-kah-DOHR soh-see-AH-oo", "social indicator", "noun"),
               V("a média", "ah MEH-jee-ah", "average", "noun"),
               V("a desigualdade", "ah deh-zee-goo-ah-oo-DAH-jee", "inequality", "noun"),
               V("o recorte", "oo heh-KOHR-jee", "data cut, breakdown", "noun")],
              G("Reading social data",
                "a média esconde · o recorte de renda · na ponta, a situação é outra",
                "A média esconde is the standard caution in Brazilian data journalism. O recorte "
                "+ noun names the breakdown (recorte de renda, recorte regional). Na ponta (at "
                "the far end) contrasts the aggregate with the worst case.",
                [X("A média melhorou, mas o recorte de renda mostra estagnação.", "ah MEH-jee-ah meh-LYOH-roo, mahs oo heh-KOHR-jee jee HEHN-dah MOH-trah es-tahg-nah-SOW(n).", "The average improved, but the income breakdown shows stagnation."),
                X("A média esconde a desigualdade entre regiões.", "ah MEH-jee-ah es-KOHN-jee ah deh-zee-goo-ah-oo-DAH-jee EH(n)-tree heh-zhee-OW(n)s.", "The average hides inequality between regions."),
                X("Na ponta, a situação é mais grave do que o índice sugere.", "nah POHN-tah, ah see-too-ah-SOW(n) eh mays GRAH-vee doo kee oo EEN-jee-see soo-ZHEH-ree.", "At the far end, the situation is worse than the index suggests.")],
                [("A média esconde de desigualdade.", "A média esconde a desigualdade.", "Esconder takes a direct object."),
                 ("O recorte de renda mostram estagnação.", "O recorte de renda mostra estagnação.", "The subject is singular: mostra.")]),
              [D("Jornalista", "O indicador melhorou?", "oo een-jee-kah-DOHR meh-lyoh-ROH?", "Did the indicator improve?"),
               D("Pesquisadora", "A média sim, mas o recorte de renda mostra estagnação.", "ah MEH-jee-ah see(n), mahs oo heh-KOHR-jee jee HEHN-dah MOH-trah es-tahg-nah-SOW(n).", "The average did, but the income breakdown shows stagnation."),
               D("Jornalista", "Então a média esconde parte do problema.", "en-TOW(n) ah MEH-jee-ah es-KOHN-jee PAHR-jee doo proh-BLEH-mah.", "So the average hides part of the problem."),
               D("Pesquisadora", "Esconde. Na ponta, a situação é mais grave.", "es-KOHN-jee. nah POHN-tah, ah see-too-ah-SOW(n) eh mays GRAH-vee.", "It does. At the far end, the situation is more serious.")],
              WS("Data worksheet", [
                  T("Read the aggregate.", ["the average improved", "the average hides inequality between regions"],
                    ["A média melhorou", "A média esconde a desigualdade entre regiões"]),
                  T("Qualify it.", ["the income breakdown shows stagnation", "at the far end, the situation is worse"],
                    ["O recorte de renda mostra estagnação", "Na ponta, a situação é mais grave"]),
              ])),
            L("Voto e participação",
              "Brazilian voting is electronic: a urna, o título de eleitor and o plebiscito. Turn "
              "out is a obrigação for adults aged 18 to 70, and the vocabulary of participation "
              "includes o conselho (council), a audiência pública and a consulta pública. "
              "Participar takes de: participar da audiência.",
              [V("a urna", "ah OOR-nah", "ballot box, voting machine", "noun"),
               V("o título de eleitor", "oo TEE-too-loo jee eh-lay-TOHR", "voter registration", "noun"),
               V("a audiência pública", "ah ah-oo-jee-EHN-see-ah POO-blee-kah", "public hearing", "noun"),
               V("a consulta pública", "ah koh(n)-SOO-oo-tah POO-blee-kah", "public consultation", "noun"),
               V("participar", "pahr-tee-see-PAHR", "to take part", "verb")],
              G("Participation and voting",
                "votar em · participar de · a consulta fica aberta por 30 dias",
                "Votar em + candidate or issue; participar de + event. Consulta pública and "
                "audiência pública are the two channels of participation before a decision. "
                "A proposta fica aberta por X dias states the period for contributions.",
                [X("Votei no candidato da coligação.", "voh-TAY noo kahn-jee-DAH-too dah koh-lee-gah-SOW(n).", "I voted for the coalition's candidate."),
                X("Participei da audiência pública sobre o transporte.", "pahr-tee-see-PAY dah ah-oo-jee-EHN-see-ah POO-blee-kah SOH-bree oo trahns-POHR-jee.", "I took part in the public hearing on transport."),
                X("A consulta pública fica aberta por trinta dias.", "ah koh(n)-SOO-oo-tah POO-blee-kah FEE-kah ah-BEHR-tah pohr TREEN-tah DEE-ahs.", "The public consultation stays open for thirty days.")],
                [("Votei para o candidato.", "Votei no candidato.", "Votar takes em: no candidato."),
                 ("Participei na audiência.", "Participei da audiência.", "Participar de contracts to da.")]),
              [D("Vereadora", "A consulta pública fica aberta por trinta dias.", "ah koh(n)-SOO-oo-tah POO-blee-kah FEE-kah ah-BEHR-tah pohr TREEN-tah DEE-ahs.", "The public consultation stays open for thirty days."),
               D("Morador", "E como eu participo?", "ee KOH-moo eh-oo pahr-tee-SEE-poo?", "And how do I take part?"),
               D("Vereadora", "Pelo site, ou na audiência do dia dez.", "PEH-loo SEE-jee, oh nah ah-oo-jee-EHN-see-ah doo DEE-ah days.", "Through the site, or at the hearing on the tenth."),
               D("Morador", "Vou participar da audiência.", "voh pahr-tee-see-PAHR dah ah-oo-jee-EHN-see-ah.", "I'll take part in the hearing.")],
              WS("Participation worksheet", [
                  T("Ask and answer about participation.", ["how do I take part?", "I'll take part in the hearing"],
                    ["Como eu participo?", "Vou participar da audiência"]),
                  T("Report the process.", ["the public consultation stays open for thirty days", "I voted for the candidate"],
                    ["A consulta pública fica aberta por trinta dias", "Votei no candidato"]),
              ])),
        ]},
        {"id": "B2+-U3", "title": "Cultura e identidade", "lessons": [
            L("Literatura brasileira",
              "The canon is read through movements: o romantismo, o modernismo of 1922, o "
              "regionalismo and the contemporary romance. A narrator is o narrador; a short "
              "story is um conto and a novel um romance. Monteiro Lobato, Clarice Lispector and "
              "Machado de Assis are the names a Brazilian reader assumes you know.",
              [V("o romance", "oo hoh-MAH(n)-see", "novel", "noun"),
               V("o conto", "oo KOHN-too", "short story", "noun"),
               V("o narrador", "oo nah-hah-DOHR", "narrator", "noun"),
               V("o modernismo", "oo moh-dehr-NEES-moo", "modernism", "noun"),
               V("a obra", "ah OH-brah", "work, oeuvre", "noun")],
              G("Talking about literature",
                "a obra de · narrado em primeira pessoa · o romance trata de",
                "A obra de + author names the corpus; o romance trata de + theme states what it "
                "is about. Narrado em primeira pessoa describes the narration. Publicado em "
                "1899 places it. Tratar de takes de: o conto trata da infância.",
                [X("Dom Casmurro, de Machado de Assis, trata de ciúme e memória.", "doh(n) kahs-MOO-hoo, jee mah-SHAH-doo jee ah-SEES, TRAH-tah jee SEE-oo-mee ee meh-MOH-ree-ah.", "Dom Casmurro, by Machado de Assis, deals with jealousy and memory."),
                X("A obra é narrada em primeira pessoa.", "ah OH-brah eh nah-HRAH-dah ey(n) pree-MAY-rah peh-SOH-ah.", "The work is narrated in the first person."),
                X("O modernismo brasileiro começa em 1922.", "oo moh-dehr-NEES-moo brah-zee-LAY-roo koh-MEH-sah ey(n) mee noh-vee-SEH(n)-toos ee veen-jee doys.", "Brazilian modernism begins in 1922.")],
                [("O romance trata com ciúme.", "O romance trata de ciúme.", "Tratar de takes de."),
                 ("A obra é narrado em primeira pessoa.", "A obra é narrada em primeira pessoa.", "Obra is feminine: narrada.")]),
              [D("Professor", "Qual obra você leu?", "kwah-oo OH-brah voh-SEH leh-oo?", "Which work did you read?"),
               D("Aluna", "Li Dom Casmurro, de Machado de Assis.", "lee doh(n) kahs-MOO-hoo, jee mah-SHAH-doo jee ah-SEES.", "I read Dom Casmurro, by Machado de Assis."),
               D("Professor", "E como é a narração?", "ee KOH-moo eh ah nah-hah-SOW(n)?", "And how is the narration?"),
               D("Aluna", "É em primeira pessoa, o que deixa a dúvida central.", "eh ey(n) pree-MAY-rah peh-SOH-ah, oo kee DAY-shah ah DOO-vee-dah sehn-TRAH-oo.", "It's in the first person, which leaves the central doubt.")],
              WS("Literature worksheet", [
                  T("Present the work.", ["Dom Casmurro, by Machado de Assis, deals with jealousy and memory", "the work is narrated in the first person"],
                    ["Dom Casmurro, de Machado de Assis, trata de ciúme e memória", "A obra é narrada em primeira pessoa"]),
                  T("Place it in time.", ["Brazilian modernism begins in 1922", "a novel and a short story"],
                    ["O modernismo brasileiro começa em 1922", "um romance e um conto"]),
              ])),
            L("Música e movimentos",
              "Brazilian music is told as a sequence of movements: o samba, a bossa nova, a MPB, "
              "o tropicalismo and o funk. Compositor and letrista are separate roles; a letra is "
              "the lyrics. The phrase a música dialoga com means the song answers another one.",
              [V("o samba", "oo SAH(n)-bah", "samba", "noun"),
               V("a letra", "ah LEH-trah", "lyrics", "noun"),
               V("o compositor", "oo koh(n)-poh-zee-TOHR", "composer", "noun"),
               V("a canção", "ah kahn-SOW(n)", "song", "noun"),
               V("o movimento", "oo moh-vee-MEN-too", "movement", "noun")],
              G("Talking about music",
                "a canção dialoga com · composta por · a letra fala de",
                "Composta por + composer and escrita por + lyricist separate the credits. A "
                "canção dialoga com names the allusion. A letra fala de + theme describes the "
                "lyrics, and a gravação de 1968 dates it.",
                [X("A canção foi composta por Tom Jobim.", "ah kahn-SOW(n) foy koh(n)-POHS-tah pohr toh(n) zhoh-BEE(n).", "The song was composed by Tom Jobim."),
                X("A letra fala da saudade da terra natal.", "ah LEH-trah FAH-lah dah sow-DAH-jee dah TEH-hah nah-TAH-oo.", "The lyrics speak of longing for the homeland."),
                X("O tropicalismo dialoga com a bossa nova e com o samba.", "oo troh-pee-kah-LEES-moo jee-ah-LOH-gah koh(n) ah BOH-sah NOH-vah ee koh(n) oo SAH(n)-bah.", "Tropicalism dialogues with bossa nova and with samba.")],
                [("A música foi composta de Tom Jobim.", "A música foi composta por Tom Jobim.", "Passive agent takes por."),
                 ("A letra fala de sobre o amor.", "A letra fala de amor.", "One preposition: falar de.")]),
              [D("Rádio", "De quem é essa canção?", "jee key(n) eh EH-sah kahn-SOW(n)?", "Whose song is this?"),
               D("Ouvinte", "Foi composta por Tom Jobim, com letra de Vinicius.", "foy koh(n)-POHS-tah pohr toh(n) zhoh-BEE(n), koh(n) LEH-trah jee vee-NEE-see-oos.", "It was composed by Tom Jobim, with lyrics by Vinicius."),
               D("Rádio", "E com quem ela dialoga?", "ee koh(n) key(n) EH-lah jee-ah-LOH-gah?", "And with whom does it dialogue?"),
               D("Ouvinte", "Com a bossa nova e com o samba de raiz.", "koh(n) ah BOH-sah NOH-vah ee koh(n) oo SAH(n)-bah jee hah-EES.", "With bossa nova and with roots samba.")],
              WS("Music worksheet", [
                  T("Give the credits.", ["the song was composed by Tom Jobim", "lyrics by Vinicius"],
                    ["A canção foi composta por Tom Jobim", "letra de Vinicius"]),
                  T("Describe the allusion.", ["tropicalism dialogues with bossa nova and with samba", "the lyrics speak of longing for the homeland"],
                    ["O tropicalismo dialoga com a bossa nova e com o samba", "A letra fala da saudade da terra natal"]),
              ])),
            L("Cinema e identidade",
              "Brazilian cinema is read through movements too: o cinema novo, as chanchadas and "
              "the contemporary documentary. A direção, o roteiro and a fotografia are the three "
              "credits to know; a periferia and o sertão are the two settings that keep "
              "returning. The festival circuit is where these films travel.",
              [V("a direção", "ah jee-reh-SOW(n)", "direction", "noun"),
               V("a fotografia", "ah foh-toh-grah-FEE-ah", "cinematography", "noun"),
               V("o documentário", "oo doh-koo-men-TAH-ree-oo", "documentary", "noun"),
               V("a periferia", "ah peh-ree-feh-REE-ah", "outskirts, periphery", "noun"),
               V("o sertão", "oo sehr-TOW(n)", "the backlands", "noun")],
              G("Talking about film",
                "dirigido por · filmado em · o filme retrata",
                "Dirigido por + director and filmado em + place locate the film. Retratar (to "
                "portray) and acompanhar are the verbs of documentary; a narrativa describes "
                "the structure. The festival formula is premiado em Cannes.",
                [X("O filme é dirigido por uma cineasta pernambucana.", "oo FEE-oo-mee eh jee-ree-ZHEE-doo pohr OO-mah see-neh-AHS-tah pehr-nah(n)-boo-KAH-nah.", "The film is directed by a filmmaker from Pernambuco."),
                X("O documentário retrata a vida na periferia de São Paulo.", "oo doh-koo-men-TAH-ree-oo heh-TRAH-tah ah VEE-dah nah peh-ree-feh-REE-ah jee sow(n) POW-oo-loo.", "The documentary portrays life on the outskirts of São Paulo."),
                X("Foi premiado em Cannes e filmado no sertão.", "foy preh-mee-AH-doo ey(n) kahn ee fee-oo-MAH-doo noo sehr-TOW(n).", "It was awarded at Cannes and filmed in the backlands.")],
                [("O filme é dirigido de Kleber.", "O filme é dirigido por Kleber.", "Passive agent takes por."),
                 ("Retrata de vida na periferia.", "Retrata a vida na periferia.", "Retratar takes a direct object.")]),
              [D("Crítico", "Do que trata o documentário?", "doo kee TRAH-tah oo doh-koo-men-TAH-ree-oo?", "What is the documentary about?"),
               D("Diretora", "Retrata a vida na periferia, filmado no Recife.", "heh-TRAH-tah ah VEE-dah nah peh-ree-feh-REE-ah, fee-oo-MAH-doo noo heh-SEE-fee.", "It portrays life on the outskirts, filmed in Recife."),
               D("Crítico", "E a narrativa?", "ee ah nah-hah-TEE-vah?", "And the narrative?"),
               D("Diretora", "Acompanha três famílias por um ano.", "ah-koh(n)-PAH-nyah treys fah-MEE-lyahs pohr oo(n) AH-noo.", "It follows three families for a year.")],
              WS("Cinema worksheet", [
                  T("Give the credits.", ["the film is directed by a filmmaker from Pernambuco", "filmed in Recife"],
                    ["O filme é dirigido por uma cineasta pernambucana", "filmado no Recife"]),
                  T("Describe the film.", ["the documentary portrays life on the outskirts", "it follows three families for a year"],
                    ["O documentário retrata a vida na periferia", "Acompanha três famílias por um ano"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("The Brazilian argument about itself runs through its culture: the modernists of "
                 "1922 wanted a literature written in Brazilian Portuguese, the bossa nova put a "
                 "conversational voice over a jazz harmony, and the cinema novo took the camera "
                 "to the sertão and the favela. Contemporary debates about inequality, voting and "
                 "public policy inherit that vocabulary — the average that hides the distribution "
                 "is read today with the same instruments as a novel's unreliable narrator."),
        source_url="https://en.wikipedia.org/wiki/Brazilian_literature",
        reading=("O debate sobre desigualdade no Brasil mudou de vocabulário nas últimas décadas. "
                 "Antes, a discussão se fazia pela renda média; hoje, o recorte de renda e os "
                 "indicadores regionais mostram que a média esconde diferenças profundas. A "
                 "literatura registrou essa mudança: do sertão de Graciliano Ramos à periferia "
                 "contemporânea, o narrador deixou de explicar o país e passou a escutá-lo."),
        reading_gloss=("The debate about inequality in Brazil changed its vocabulary in recent "
                       "decades. Before, the discussion was made through average income; today, "
                       "the income breakdown and regional indicators show that the average hides "
                       "deep differences. Literature registered this change: from Graciliano "
                       "Ramos's backlands to the contemporary periphery, the narrator stopped "
                       "explaining the country and began to listen to it."),
        listening=("O orçamento prevê mais fiscalização, mas na prática depende do repasse. — E "
                   "quem executa? — Cabe ao município. A consulta pública fica aberta por "
                   "trinta dias; quem quiser pode participar da audiência."),
        listening_gloss=("The budget foresees more oversight, but in practice it depends on the "
                         "transfer. — And who implements it? — It's up to the municipality. The "
                         "public consultation stays open for thirty days; anyone who wants can "
                         "take part in the hearing."),
        voice_tag=VOICE,
        idioms=[
            ("na ponta", "at the tip", "at the far end of the distribution"),
            ("cabe ao", "it fits to", "it is up to"),
            ("por baixo do pano", "under the cloth", "behind the scenes"),
            ("de raiz", "of root", "authentic, from the roots"),
            ("colocar o dedo na ferida", "to put a finger on the wound", "to name the sensitive issue"),
            ("arregaçar as mangas", "to roll up the sleeves", "to get to work"),
            ("dar o tom", "to give the tone", "to set the agenda"),
            ("em cima do muro", "on top of the wall", "fence-sitting"),
            ("virar o jogo", "to turn the game", "to reverse the situation"),
            ("sem meias palavras", "without half words", "without mincing words"),
        ],
        mistakes=[
            ("Vou participar na audiência pública.", "Vou participar da audiência pública.", "Participar takes de."),
            ("O romance trata com ciúme.", "O romance trata de ciúme.", "Tratar takes de when it means 'to be about'."),
            ("A média escondem a desigualdade.", "A média esconde a desigualdade.", "Média is singular: esconde."),
        ],
        task_title="Um parágrafo sobre o país",
        task_instructions=("Write one paragraph on a Brazilian public debate you know: name the "
                           "instrument (orçamento, meta, indicador), attribute responsibility "
                           "with cabe a, qualify the data with a média esconde or o recorte de "
                           "renda, and close with a cultural reference that registers the "
                           "change. Then rewrite the paragraph without the numbers and check "
                           "which claims survive."),
    ),
    "test": [
        ("translate_en", "Say: the average hides inequality between regions.", "A média esconde a desigualdade entre regiões."),
        ("translate_pt", "Cabe ao município a fiscalização dos contratos.", "Oversight of the contracts is up to the municipality."),
        ("multiple_choice", "Which phrase concedes the positive before the improvement point?", "Você conduziu bem a reunião; no próximo ciclo podemos ajustar o prazo."),
        ("fill_in_the_blank", "O romance ___ de ciúme e memória.", "trata"),
        ("word_selection", "Select the Portuguese for 'income breakdown'.", "o recorte de renda"),
        ("error_correction", "Vou participar na audiência pública.", "Vou participar da audiência pública."),
        ("dialogue_completion", "Complete: O que você precisa para destravar? — ___ (a realistic deadline)", "Preciso de prazo realista"),
        ("matching", "Match habilidade transferível to its meaning.", "transferable skill"),
        ("reading_comprehension", "No texto, o que a média esconde?", "deep regional differences"),
        ("inference", "O narrador 'deixou de explicar o país e passou a escutá-lo'. What does this tell us about contemporary Brazilian literature?", "it gives voice instead of authorial summary"),
        ("main_idea", "O texto trata da mudança de vocabulário no debate sobre desigualdade. — what is this sentence?", "the main point of the reading"),
        ("detail_identification", "O que substituiu a renda média na discussão?", "the income breakdown and regional indicators"),
    ],
}


HALFSTEPS["C1+"] = {
    "native": NATIVE,
    "title": "%s C1+ — Academia, clima e língua" % NAME,
    "goals": [
        "Write and present academic work: abstract, citation, paraphrase and defence",
        "Follow environmental and climate policy: deforestation, alerts and the energy mix",
        "Discuss linguistic variation and the place of other languages in Brazil",
    ],
    "units": [
        {"id": "C1+-U1", "title": "Registro acadêmico", "lessons": [
            L("O resumo acadêmico",
              "An academic abstract in Portuguese is written in one paragraph and four moves: "
              "contexto, objetivo, método, resultado. A revisão de literatura comes before "
              "either; o corpus is what you analysed. The impersonal construction uses the "
              "third person with se: analisou-se, observa-se.",
              [V("o resumo", "oo heh-ZOO-moo", "abstract", "noun"),
               V("a revisão de literatura", "ah heh-vee-ZOW(n) jee lee-teh-rah-TOO-rah", "literature review", "noun"),
               V("o corpus", "oo KOHR-poos", "corpus", "noun"),
               V("o objetivo", "oo ohb-zheh-TEE-voo", "objective, aim", "noun"),
               V("analisar", "ah-nah-lee-ZAHR", "to analyse", "verb")],
              G("Writing an abstract",
                "este artigo analisa · a partir de · os resultados indicam que",
                "Este artigo + verb in the present opens the abstract without a personal pronoun. "
                "A partir de introduces the method or the sample. Os resultados indicam que "
                "hedges the claim; the aorist pretérito (analisou-se) reports what was done.",
                [X("Este artigo analisa a cobertura jornalística de 2019 a 2024.", "ES-jee ahr-TEE-goo ah-nah-LEE-zah ah koh-behr-TOO-rah zhohr-nah-LEES-tee-kah jee doys MEE-oo ee noh-vee-SEH(n)-toos ee VEEN-jee KWAH-troo.", "This article analyses news coverage from 2019 to 2024."),
                X("A partir de um corpus de 320 textos, observa-se uma mudança de enquadramento.", "ah pahr-TEER jee oo(n) KOHR-poos jee treh-ZEH(n)-toos ee VEEN-jee TEX-toos, ohb-sehr-VAH-see OO-mah moo-DAHN-sah jee en-kwah-drah-MEN-too.", "From a corpus of 320 texts, a shift of framing is observed."),
                X("Os resultados indicam que a fonte oficial perdeu espaço.", "oos heh-zoo-oo-TAH-doos een-jee-KAHM kee ah FOHN-jee oh-fee-see-AH-oo pehr-DEH-oo es-PAH-soo.", "The results indicate that the official source lost ground.")],
                [("O artigo analisa de cobertura jornalística.", "O artigo analisa a cobertura jornalística.", "Analisar takes a direct object."),
                 ("Os resultados indica que mudou.", "Os resultados indicam que mudou.", "The verb agrees with the plural subject.")]),
              [D("Orientadora", "O resumo tem os quatro movimentos?", "oo heh-ZOO-moo tay(n) oos KWAH-troo moh-vee-MEN-toos?", "Does the abstract have the four moves?"),
               D("Mestrando", "Tenho contexto, objetivo e método; falta o resultado.", "TEH-nyoo koh(n)-TEHS-too, ohb-zheh-TEE-voo ee MEH-toh-doo; FAH-oo-tah oo heh-zoo-oo-TAH-doo.", "I have context, objective and method; the result is missing."),
               D("Orientadora", "E o corpus está descrito?", "ee oo KOHR-poos es-TAH des-KREE-too?", "And is the corpus described?"),
               D("Mestrando", "Está: 320 textos, a partir de 2019.", "es-TAH: treh-ZEH(n)-toos TEX-toos, ah pahr-TEER jee doys MEE-oo ee noh-vee-SEH(n)-toos.", "It is: 320 texts, from 2019.")],
              WS("Abstract worksheet", [
                  T("Write the moves.", ["this article analyses news coverage", "from a corpus of 320 texts"],
                    ["Este artigo analisa a cobertura jornalística", "A partir de um corpus de 320 textos"]),
                  T("Report the result.", ["the results indicate that the official source lost ground", "a shift of framing is observed"],
                    ["Os resultados indicam que a fonte oficial perdeu espaço", "Observa-se uma mudança de enquadramento"]),
              ])),
            L("Citação e paráfrase",
              "Citation is a grammar of attribution: segundo, de acordo com, como argumenta, "
              "conforme. A paráfrase must change the syntax, not only the words; a citação direta "
              "keeps the quotation marks and the page. Plágio is defined by the missing source, "
              "not by the repeated idea.",
              [V("a citação", "ah see-tah-SOW(n)", "quotation, citation", "noun"),
               V("a paráfrase", "ah pah-RAH-frah-zee", "paraphrase", "noun"),
               V("o plágio", "oo PLAH-zhee-oo", "plagiarism", "noun"),
               V("a referência", "ah heh-feh-REHN-see-ah", "reference", "noun"),
               V("conforme", "koh(n)-FOHR-mee", "according to", "preposition")],
              G("Attributing and paraphrasing",
                "segundo X (ano) · conforme argumenta · parafraseando o autor",
                "Segundo and conforme take the author with no comma before the claim. Como "
                "argumenta X inserts the attribution. Parafraseando o autor marks an explicit "
                "paraphrase, which is the safest form when the wording is close.",
                [X("Segundo Soares (2021), a cobertura mudou de enquadramento.", "seh-GOON-doo soh-AH-rees (doys MEE-oo ee veen-jee OO(n)), ah koh-behr-TOO-rah moo-DOH jee en-kwah-drah-MEN-too.", "According to Soares (2021), the coverage changed its framing."),
                X("Conforme argumenta a autora, a fonte oficial perdeu credibilidade.", "koh(n)-FOHR-mee ahr-goo-MEN-tah ah ah-oo-TOH-rah, ah FOHN-jee oh-fee-see-AH-oo pehr-DEH-oo kreh-jee-bee-lee-DAH-jee.", "As the author argues, the official source lost credibility."),
                X("Parafraseando o autor, a mudança é de método, não de opinião.", "pah-rah-frah-zeh-AHN-doo oo ah-oo-TOHR, ah moo-DAHN-sah eh jee MEH-toh-doo, now(n) jee oh-pee-nee-OW(n).", "Paraphrasing the author, the change is one of method, not opinion.")],
                [("Segundo o autor, que a cobertura mudou.", "Segundo o autor, a cobertura mudou.", "The attribution clause needs no que."),
                 ("Conforme argumenta de que a fonte perdeu.", "Conforme argumenta, a fonte perdeu credibilidade.", "One clause per claim.")]),
              [D("Revisor", "O trecho é paráfrase ou citação direta?", "oo TREH-shoo eh pah-RAH-frah-zee oh see-tah-SOW(n) jee-REH-tah?", "Is the passage a paraphrase or a direct quotation?"),
               D("Autora", "É paráfrase, mas a sintaxe ficou próxima do original.", "eh pah-RAH-frah-zee, mahs ah seen-TAH-see fee-KOH PROH-see-mah doo oh-ree-zhee-NAH-oo.", "It's a paraphrase, but the syntax stayed close to the original."),
               D("Revisor", "Então marque com parafraseando e cite a referência.", "en-TOW(n) MAHR-kee koh(n) pah-rah-frah-zeh-AHN-doo ee SEE-jee ah heh-feh-REHN-see-ah.", "Then mark it with parafraseando and cite the reference."),
               D("Autora", "Vou reescrever: segundo Soares (2021).", "voh heh-es-kreh-VEHR: seh-GOON-doo soh-AH-rees (doys MEE-oo ee veen-jee OO(n)).", "I'll rewrite it: according to Soares (2021).")],
              WS("Citation worksheet", [
                  T("Attribute.", ["according to Soares (2021), the coverage changed its framing", "as the author argues, the official source lost credibility"],
                    ["Segundo Soares (2021), a cobertura mudou de enquadramento", "Conforme argumenta a autora, a fonte oficial perdeu credibilidade"]),
                  T("Mark the paraphrase.", ["paraphrasing the author, the change is one of method", "I'll rewrite it with the reference"],
                    ["Parafraseando o autor, a mudança é de método", "Vou reescrever citando a referência"]),
              ])),
            L("Apresentação e arguição",
              "A conference paper is a comunicação; the panel is o painel and the question period "
              "a arguição. The formula to open is obrigado pela presença; to present: o trabalho "
              "está estruturado em três partes. Agradeço a pergunta is the fixed reply before "
              "answering anything.",
              [V("a comunicação", "ah koh-moo-nee-kah-SOW(n)", "conference paper", "noun"),
               V("a arguição", "ah ahr-goo-ee-SOW(n)", "question and defence period", "noun"),
               V("o painel", "oo pah-ee-NEH-oo", "panel", "noun"),
               V("a pergunta", "ah pehr-GOON-tah", "question", "noun"),
               V("agradecer", "ah-grah-deh-SEHR", "to thank", "verb")],
              G("Presenting and answering",
                "agradeço a pergunta · o trabalho está estruturado em · retomando o ponto",
                "Agradeço a pergunta buys a moment and marks respect. O trabalho está estruturado "
                "em X partes signposts the talk. Retomando o ponto returns to the argument after "
                "a digression, and a resposta pode ser em duas partes structures the answer.",
                [X("Agradeço a pergunta; retomo o ponto do método.", "ah-grah-DEH-soo ah pehr-GOON-tah; heh-TOH-moo oo POHN-too doo MEH-toh-doo.", "Thank you for the question; I return to the point about method."),
                X("O trabalho está estruturado em três partes.", "oo trah-BAH-lyoo es-TAH es-troo-too-RAH-doo ey(n) treys PAHR-jee(s).", "The paper is structured in three parts."),
                X("A resposta tem duas partes: o dado e a interpretação.", "ah hes-POHS-tah tay(n) DOO-ahs PAHR-jees: oo DAH-doo ee ah een-tehr-preh-tah-SOW(n).", "The answer has two parts: the datum and the interpretation.")],
                [("Agradeço pela pergunta de você.", "Agradeço a pergunta.", "The fixed formula is agradeço a pergunta."),
                 ("O trabalho está estruturado de três partes.", "O trabalho está estruturado em três partes.", "Estruturado em takes em.")]),
              [D("Mediadora", "Há uma pergunta para a autora.", "ah OO-mah pehr-GOON-tah pah-rah ah ah-oo-TOH-rah.", "There is a question for the author."),
               D("Pesquisador", "Como o corpus foi selecionado?", "KOH-moo oo KOHR-poos foy seh-leh-see-oh-NAH-doo?", "How was the corpus selected?"),
               D("Autora", "Agradeço a pergunta. Foi por amostragem, em três etapas.", "ah-grah-DEH-soo ah pehr-GOON-tah. foy pohr ah-mohs-trah-ZHEH(n), ey(n) treys eh-TAH-pahs.", "Thank you for the question. It was by sampling, in three stages."),
               D("Pesquisador", "E a validação?", "ee ah vah-lee-jah-SOW(n)?", "And the validation?"),
               D("Autora", "Retomo isso no terceiro movimento do resumo.", "heh-TOH-moo EE-soo noo tehr-SAY-roo moh-vee-MEN-too doo heh-ZOO-moo.", "I return to that in the third move of the abstract.")],
              WS("Presentation worksheet", [
                  T("Open the answer.", ["thank you for the question", "I return to the point about method"],
                    ["Agradeço a pergunta", "Retomo o ponto do método"]),
                  T("Structure the talk.", ["the paper is structured in three parts", "the answer has two parts: the datum and the interpretation"],
                    ["O trabalho está estruturado em três partes", "A resposta tem duas partes: o dado e a interpretação"]),
              ])),
        ]},
        {"id": "C1+-U2", "title": "Ambiente e clima", "lessons": [
            L("Desmatamento e política ambiental",
              "Environmental policy has a precise vocabulary: o desmatamento, a licença "
              "ambiental, a meta de redução, a fiscalização and a unidade de conservação. "
              "Medido por satélite and por hectare place the numbers; o alerta is the satellite "
              "warning, not the disaster.",
              [V("o desmatamento", "oo des-mah-tah-MEN-too", "deforestation", "noun"),
               V("a licença ambiental", "ah lee-SEH(n)-sah ah(n)-bee-ehn-TAH-oo", "environmental licence", "noun"),
               V("a unidade de conservação", "ah oo-nee-DAH-jee jee koh(n)-sehr-vah-SOW(n)", "conservation unit", "noun"),
               V("a meta de redução", "ah MEH-tah jee heh-doo-SOW(n)", "reduction target", "noun"),
               V("medir", "meh-DEER", "to measure", "verb")],
              G("Reporting environmental policy",
                "o desmatamento caiu X% · medido por satélite · a meta é de reduzir",
                "A meta é de + infinitive states the target. Medido por satélite and em hectares "
                "are the standard qualifiers. A queda/a alta nominate the movement, and a "
                "fiscalização is the enforcement that explains it.",
                [X("O desmatamento caiu 22% no período, medido por satélite.", "oo des-mah-tah-MEN-too kah-EE-oo veen-jee ee doys pohr SEHN-too noo peh-REE-oh-doo, meh-JEE-doo pohr sah-TEH-lee-jee.", "Deforestation fell 22% in the period, measured by satellite."),
                X("A meta é de reduzir a área desmatada em 40%.", "ah MEH-tah eh jee heh-doo-ZEER ah AH-ree-ah des-mah-TAH-dah ey(n) KWAH-REHN-tah pohr SEHN-too.", "The target is to cut the deforested area by 40%."),
                X("A fiscalização nas unidades de conservação aumentou.", "ah fees-kah-lee-zah-SOW(n) nahs oo-nee-DAH-jees jee koh(n)-sehr-vah-SOW(n) ah-oo-men-TOH.", "Enforcement in the conservation units increased.")],
                [("O desmatamento caíram 22%.", "O desmatamento caiu 22%.", "The subject is singular: caiu."),
                 ("A meta é reduzir de 40% na área.", "A meta é reduzir a área em 40%.", "Em + percentage is the correct pattern.")]),
              [D("Repórter", "O desmatamento caiu?", "oo des-mah-tah-MEN-too kah-EE-oo?", "Did deforestation fall?"),
               D("Pesquisadora", "Caiu 22%, medido por satélite.", "kah-EE-oo veen-jee ee doys pohr SEHN-too, meh-JEE-doo pohr sah-TEH-lee-jee.", "It fell 22%, measured by satellite."),
               D("Repórter", "E a meta para o ano?", "ee ah MEH-tah pah-rah oo AH-noo?", "And the target for the year?"),
               D("Pesquisadora", "Reduzir a área em 40%; depende da fiscalização.", "heh-doo-ZEER ah AH-ree-ah ey(n) KWAH-REHN-tah pohr SEHN-too; deh-PEH(n)-jee dah fees-kah-lee-zah-SOW(n).", "To cut the area by 40%; it depends on enforcement.")],
              WS("Environment worksheet", [
                  T("Report the number.", ["deforestation fell 22%", "measured by satellite"],
                    ["O desmatamento caiu 22%", "medido por satélite"]),
                  T("State the target.", ["the target is to cut the deforested area by 40%", "enforcement in the conservation units increased"],
                    ["A meta é reduzir a área desmatada em 40%", "A fiscalização nas unidades de conservação aumentou"]),
              ])),
            L("Eventos extremos e defesa civil",
              "A disaster is described in phases: o alerta, o evento extremo, a resposta, a "
              "reconstrução. A defesa civil issues the alert; a população ribeirinha is the "
              "riverside population and o desalojado is the displaced person. Pluscuamperfect "
              "plus pretérito structures the timeline.",
              [V("o alerta", "oo ah-LEHR-tah", "alert, warning", "noun"),
               V("o evento extremo", "oo eh-VEHN-too es-TREH-moo", "extreme weather event", "noun"),
               V("a defesa civil", "ah deh-FEH-zah see-VEE-oo", "civil defence", "noun"),
               V("o desalojado", "oo deh-zah-loh-ZHAH-doo", "displaced person", "noun"),
               V("a reconstrução", "ah heh-koh(n)-stroo-SOW(n)", "reconstruction", "noun")],
              G("Describing an extreme event",
                "a defesa civil emitiu alerta · quando o rio subiu, muitos já tinham saído",
                "Emitir alerta is the collocation. The timeline uses the pluperfect for what "
                "happened before: já tinham saído. Desalojado and desabrigado are kept distinct "
                "in official texts — the first found shelter, the second did not.",
                [X("A defesa civil emitiu alerta para a região ribeirinha.", "ah deh-FEH-zah see-VEE-oo eh-mee-TEE-oo ah-LEHR-tah pah-rah ah heh-zhee-OW(n) hee-bay-REE-nyah.", "Civil defence issued an alert for the riverside region."),
                X("Quando o rio subiu, muitos moradores já tinham saído.", "KWAHN-doo oo HEE-oo soo-BEE-oo, MOOY-toos moh-rah-DOH-rees zhah TEE-nyah(n) sah-EE-doo.", "When the river rose, many residents had already left."),
                X("A reconstrução das casas levou dois anos.", "ah heh-koh(n)-stroo-SOW(n) dahs KAH-zahs leh-VOH doys AH-noos.", "The reconstruction of the houses took two years.")],
                [("A defesa civil emitiu de alerta.", "A defesa civil emitiu alerta.", "Emitir takes a bare object."),
                 ("Quando o rio subiu, muitos já saíram antes.", "Quando o rio subiu, muitos já tinham saído.", "The earlier event takes the pluperfect.")]),
              [D("Jornalista", "Como foi o alerta?", "KOH-moo foy oo ah-LEHR-tah?", "How was the alert?"),
               D("Coordenador", "A defesa civil emitiu alerta na quinta.", "ah deh-FEH-zah see-VEE-oo eh-mee-TEE-oo ah-LEHR-tah nah KEEN-tah.", "Civil defence issued the alert on Thursday."),
               D("Jornalista", "A população saiu a tempo?", "ah poh-poo-lah-SOW(n) sah-EE-oo ah TEH(n)-poo?", "Did the population leave in time?"),
               D("Coordenador", "Muitos já tinham saído quando o rio subiu.", "MOOY-toos zhah TEE-nyah(n) sah-EE-doo KWAHN-doo oo HEE-oo soo-BEE-oo.", "Many had already left when the river rose.")],
              WS("Disaster worksheet", [
                  T("Report the alert.", ["civil defence issued an alert for the riverside region", "it was issued on Thursday"],
                    ["A defesa civil emitiu alerta para a região ribeirinha", "Foi emitido na quinta"]),
                  T("Order the timeline.", ["many residents had already left when the river rose", "the reconstruction took two years"],
                    ["Muitos moradores já tinham saído quando o rio subiu", "A reconstrução levou dois anos"]),
              ])),
            L("Matriz energética e transição",
              "The energy debate uses a fixed set of nouns: a matriz energética, a fonte "
              "renovável, o leilão, a transmissão and o armazenamento. Brazil's matrix is "
              "unusually renewable because of hydro; the argument now is about a diversificação, "
              "not a substitution.",
              [V("a matriz energética", "ah mah-TREES eh-nehr-ZHEH-tee-kah", "energy mix", "noun"),
               V("a fonte renovável", "ah FOHN-jee heh-noh-VAH-veh-oo", "renewable source", "noun"),
               V("o leilão", "oo lay-LOW(n)", "auction", "noun"),
               V("a transmissão", "ah trahnz-mee-SOW(n)", "transmission", "noun"),
               V("a diversificação", "ah jee-vehr-see-fee-kah-SOW(n)", "diversification", "noun")],
              G("Discussing the energy mix",
                "a matriz é majoritariamente renovável · o leilão contratou · depende da transmissão",
                "Majoritariamente + adjective states the proportion without a number. O leilão "
                "contratou X MW is how capacity is reported. The bottleneck sentence is sempre "
                "depende da transmissão — the grid, not the plant.",
                [X("A matriz brasileira é majoritariamente renovável.", "ah mah-TREES brah-zee-LAY-rah eh mah-zhoh-ree-tah-ree-ah-MEN-jee heh-noh-VAH-veh-oo.", "The Brazilian energy mix is mostly renewable."),
                X("O leilão contratou 2 GW em solar e eólica.", "oo lay-LOW(n) koh(n)-trah-TOH doys gee-gah-VAHS ey(n) soh-LAHR ee eh-OH-lee-kah.", "The auction contracted 2 GW in solar and wind."),
                X("A diversificação depende da transmissão.", "ah jee-vehr-see-fee-kah-SOW(n) deh-PEH(n)-jee dah trahnz-mee-SOW(n).", "Diversification depends on transmission.")],
                [("A matriz é majoritariamente de renovável.", "A matriz é majoritariamente renovável.", "Majoritariamente takes the bare adjective."),
                 ("O leilão contrataram 2 GW.", "O leilão contratou 2 GW.", "Leilão is singular: contratou.")]),
              [D("Entrevistador", "A matriz brasileira já é limpa?", "ah mah-TREES brah-zee-LAY-rah zhah eh LEE(m)-pah?", "Is the Brazilian energy mix already clean?"),
               D("Especialista", "É majoritariamente renovável, por causa da hidrelétrica.", "eh mah-zhoh-ree-tah-ree-ah-MEN-jee heh-noh-VAH-veh-oo, pohr KOW-zah dah ee-dreh-LEH-tree-kah.", "It's mostly renewable, because of hydro."),
               D("Entrevistador", "E o gargalo?", "ee oo gahr-GAH-loo?", "And the bottleneck?"),
               D("Especialista", "A transmissão: a diversificação depende dela.", "ah trahnz-mee-SOW(n): ah jee-vehr-see-fee-kah-SOW(n) deh-PEH(n)-jee DEH-lah.", "Transmission: diversification depends on it.")],
              WS("Energy worksheet", [
                  T("Describe the mix.", ["the Brazilian energy mix is mostly renewable", "the auction contracted 2 GW"],
                    ["A matriz brasileira é majoritariamente renovável", "O leilão contratou 2 GW"]),
                  T("Name the bottleneck.", ["diversification depends on transmission", "because of hydro"],
                    ["A diversificação depende da transmissão", "por causa da hidrelétrica"]),
              ])),
        ]},
        {"id": "C1+-U3", "title": "Língua e identidade", "lessons": [
            L("Variação linguística",
              "Variation is discussed with four terms: a variedade, a norma, o sotaque and o "
              "registro. A norma-padrão is a reference, not the only correct form; a variedade "
              "culta is the educated spoken norm. Prescrever (to prescribe) and descrever (to "
              "describe) name the two approaches to language.",
              [V("a variedade", "ah vah-ree-eh-DAH-jee", "variety", "noun"),
               V("a norma-padrão", "ah NOHR-mah pah-DROW(n)", "standard norm", "noun"),
               V("o sotaque", "oo soh-TAH-kee", "accent", "noun"),
               V("prescrever", "pres-kreh-VEHR", "to prescribe", "verb"),
               V("descrever", "des-kreh-VEHR", "to describe", "verb")],
              G("Talking about language variation",
                "a norma-padrão serve de referência · não existe português único · descrever, não prescrever",
                "A língua não é homogênea is the opening of most texts on variation. Serve de "
                "referência careful: the norm is a reference, not a verdict. The pair "
                "descrever/prescrever separates linguistics from usage advice.",
                [X("Não existe um português único: há variedades regionais e sociais.", "now(n) eh-ZEES-jee oo(n) pohr-too-GEHS OO-nee-koo: ah vah-ree-eh-DAH-jees heh-zhee-oh-NAH-ees ee soh-see-AH-ees.", "There is no single Portuguese: there are regional and social varieties."),
                X("A norma-padrão serve de referência, não de medida de inteligência.", "ah NOHR-mah pah-DROW(n) SEHR-vee jee heh-feh-REHN-see-ah, now(n) jee meh-ZEE-dah jee een-teh-lee-ZHEHN-see-ah.", "The standard norm serves as a reference, not as a measure of intelligence."),
                X("O sotaque não compromete a compreensão.", "oo soh-TAH-kee now(n) koh(n)-proh-MEH-jee ah koh(n)-preh-ehn-SOW(n).", "Accent does not compromise comprehension.")],
                [("O português não são únicos.", "O português não é único.", "Singular subject, singular verb."),
                 ("A norma-padrão serve para referência de referência.", "A norma-padrão serve de referência.", "Serve de + noun is the pattern.")]),
              [D("Entrevistador", "O sotaque é um problema?", "oo soh-TAH-kee eh oo(n) proh-BLEH-mah?", "Is accent a problem?"),
               D("Linguista", "Não. O que existe é preconceito linguístico.", "now(n). oo kee eh-ZEES-jee eh preh-koh(n)-SEY-too lee(n)-GWEE-tee-koh.", "No. What exists is linguistic prejudice."),
               D("Entrevistador", "E a norma-padrão?", "ee ah NOHR-mah pah-DROW(n)?", "And the standard norm?"),
               D("Linguista", "Serve de referência; não elimina variedades.", "SEHR-vee jee heh-feh-REHN-see-ah; now(n) eh-lee-MEE-nah vah-ree-eh-DAH-jees.", "It serves as a reference; it doesn't eliminate varieties.")],
              WS("Variation worksheet", [
                  T("State the principle.", ["there is no single Portuguese", "the standard norm serves as a reference"],
                    ["Não existe um português único", "A norma-padrão serve de referência"]),
                  T("Separate description from prescription.", ["accent does not compromise comprehension", "describe, don't prescribe"],
                    ["O sotaque não compromete a compreensão", "Descrever, não prescrever"]),
              ])),
            L("Outras línguas do Brasil",
              "Brazil is multilingual: línguas indígenas, o português quilombola, as línguas de "
              "herança (German, Italian, Japanese) and Libras, the sign language. The legal term "
              "is língua de imigração; o multilinguismo and a cooficialização describe what "
              "municipalities do when they adopt a second official language.",
              [V("a língua indígena", "ah LEE(n)-gwah een-JEE-zheh-nah", "Indigenous language", "noun"),
               V("a língua de herança", "ah LEE(n)-gwah jee eh-REHN-sah", "heritage language", "noun"),
               V("o multilinguismo", "oo moon-tee-lee(n)-GWEEZ-moo", "multilingualism", "noun"),
               V("a cooficialização", "ah koh-oh-fee-see-ah-lee-zah-SOW(n)", "co-officialisation", "noun"),
               V("a Libras", "ah LEE-brahs", "Brazilian Sign Language", "noun")],
              G("Talking about other languages",
                "são faladas mais de 150 línguas · cooficializada em 2002 · língua de herança",
                "The passive with são faladas reports the count without an agent. As línguas de "
                "imigração carry their communities; língua de herança is the term for the one "
                "spoken at home but not in school. Nheengatu became co-official in São Gabriel "
                "da Cachoeira in 2002.",
                [X("No Brasil são faladas mais de 150 línguas indígenas.", "noo brah-ZEE-oo sow(n) fah-LAH-dahs mays jee SEHN-too ee seen-KWEHN-tah LEE(n)-gwahs een-JEE-zheh-nahs.", "In Brazil more than 150 Indigenous languages are spoken."),
                X("O nheengatu foi cooficializado em 2002.", "oo nyee(n)-gah-TOO foy koh-oh-fee-see-ah-lee-ZAH-doo ey(n) doys MEE-oo ee doys.", "Nheengatu was made co-official in 2002."),
                X("O alemão é língua de herança em várias cidades do Sul.", "oo ah-leh-MOW(n) eh LEE(n)-gwah jee eh-REHN-sah ey(n) VAH-ree-ahs see-DAH-jees doo SOO-oo.", "German is a heritage language in several southern cities.")],
                [("São falado mais de 150 línguas.", "São faladas mais de 150 línguas.", "Línguas is feminine plural: faladas."),
                 ("O nheengatu foi cooficializado de 2002.", "O nheengatu foi cooficializado em 2002.", "The year takes em.")]),
              [D("Repórter", "Quantas línguas são faladas no Brasil?", "KWAHN-tahs LEE(n)-gwahs sow(n) fah-LAH-dahs noo brah-ZEE-oo?", "How many languages are spoken in Brazil?"),
               D("Pesquisadora", "Mais de 150 indígenas, além das de herança.", "mays jee SEHN-too ee seen-KWEHN-tah een-JEE-zheh-nahs, ah-LEH(n) dahs jee eh-REHN-sah.", "More than 150 Indigenous, besides heritage ones."),
               D("Repórter", "E a cooficialização?", "ee ah koh-oh-fee-see-ah-lee-zah-SOW(n)?", "And co-officialisation?"),
               D("Pesquisadora", "Acontece por município, como o nheengatu em 2002.", "ah-koh(n)-TEH-see pohr moo-NEE-see-pee-oo, KOH-moo oo nyee(n)-gah-TOO ey(n) doys MEE-oo ee doys.", "It happens per municipality, like Nheengatu in 2002.")],
              WS("Languages worksheet", [
                  T("Report the numbers.", ["more than 150 Indigenous languages are spoken", "Nheengatu was made co-official in 2002"],
                    ["São faladas mais de 150 línguas indígenas", "O nheengatu foi cooficializado em 2002"]),
                  T("Name the category.", ["German is a heritage language in several southern cities", "co-officialisation happens per municipality"],
                    ["O alemão é língua de herança em várias cidades do Sul", "A cooficialização acontece por município"]),
              ])),
            L("O acordo ortográfico na prática",
              "The 1990 spelling agreement took effect in Brazil in 2009 and changed few things: "
              "o trema disappeared, some hyphens went, and the European spelling converged on the "
              "Brazilian one. In practice you check three cases: ideia (no accent), voo (no "
              "circumflex) and anti-inflamatório (hyphen kept).",
              [V("a grafia", "ah grah-FEE-ah", "spelling", "noun"),
               V("o acordo ortográfico", "oo ah-KOHR-doo or-toh-GRAH-fee-koh", "spelling agreement", "noun"),
               V("o hífen", "oo EE-feh(n)", "hyphen", "noun"),
               V("a dupla grafia", "ah DOO-plah grah-FEE-ah", "dual spelling", "noun"),
               V("uniformizar", "oo-nee-fohr-mee-ZAHR", "to standardise", "verb")],
              G("Applying the spelling agreement",
                "desde 2009 · caiu o trema · mantém-se o hífen · dupla grafia aceita",
                "Desde 2009 places the change. Caiu o trema / caiu o acento reports what "
                "disappeared. Mantém-se o hífen keeps the hyphen in compounds with the same "
                "second element (anti-inflamatório). Dupla grafia aceita covers the words with "
                "two accepted forms.",
                [X("Desde 2009, o trema caiu em palavras como linguiça.", "DEHS-jee doys MEE-oo ee noh-vee, oo TREH-mah kah-EE-oo ey(n) pah-LAH-vrahs KOH-moo lee(n)-GWEE-sah.", "Since 2009 the umlaut has fallen in words like linguiça."),
                X("Mantém-se o hífen em anti-inflamatório.", "mahn-TEH(n)-see oo EE-feh(n) ey(n) AH(n)-jee een-flah-mah-TOH-ree-oo.", "The hyphen is kept in anti-inflamatório."),
                X("Ideia e voo perderam o acento.", "ee-DAY-ah ee voh-oo pehr-DEH-rah(n) oo ah-SEN-too.", "Ideia and voo lost their accent.")],
                [("Desde 2009, o trema caiu de palavras.", "Desde 2009, o trema caiu em palavras.", "Cair em: the change happens in a set."),
                 ("Mantém o hífen anti-inflamatório.", "Mantém-se o hífen em anti-inflamatório.", "The impersonal se is the written register here.")]),
              [D("Editora", "Ideia leva acento?", "ee-DAY-ah LEH-vah ah-SEN-too?", "Does ideia take an accent?"),
               D("Revisor", "Não, desde o acordo.", "now(n), DEHS-jee oo ah-KOHR-doo.", "No, since the agreement."),
               D("Editora", "E anti-inflamatório?", "ee AH(n)-jee een-flah-mah-TOH-ree-oo?", "And anti-inflamatório?"),
               D("Revisor", "Mantém-se o hífen e faz-se a revisão final.", "mahn-TEH(n)-see oo EE-feh(n) ee fah(f)-see ah heh-vee-ZOW(n) fee-NAH-oo.", "The hyphen is kept and the final check is done.")],
              WS("Spelling worksheet", [
                  T("Report the change.", ["since 2009 the umlaut has fallen", "ideia and voo lost their accent"],
                    ["Desde 2009, o trema caiu", "Ideia e voo perderam o acento"]),
                  T("Keep the hyphen.", ["the hyphen is kept in anti-inflamatório", "the final check is done"],
                    ["Mantém-se o hífen em anti-inflamatório", "Faz-se a revisão final"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Brazil's language question is also a policy question: the 1990 spelling "
                 "agreement, in force in Brazil since 2009, changed less than the newspaper "
                 "headlines suggested; the co-officialisation of Nheengatu in São Gabriel da "
                 "Cachoeira in 2002 made an Indigenous language the companion of Portuguese in "
                 "one municipality; and the 2014 law on Libras recognised the sign language of "
                 "the deaf community as a means of communication. Variation, in Brazilian public "
                 "debate, is measured in hectares of territory and hours of schooling."),
        source_url="https://en.wikipedia.org/wiki/Languages_of_Brazil",
        reading=("O acordo ortográfico entrou em vigor no Brasil em 2009 e mudou menos do que se "
                 "imaginava: o trema caiu, alguns hífens desapareceram e certas grafias se "
                 "uniformizaram. No plano acadêmico, a mudança foi acompanhada de uma discussão "
                 "mais ampla sobre variação linguística. A pergunta deixou de ser qual forma é "
                 "certa e passou a ser em que registro e em que variedade cada forma circula. "
                 "Nas salas de aula, o efeito foi tornar a norma-padrão uma referência explícita, "
                 "não uma régua invisível."),
        reading_gloss=("The spelling agreement came into force in Brazil in 2009 and changed "
                       "less than people imagined: the umlaut fell, some hyphens disappeared and "
                       "certain spellings standardised. On the academic side, the change was "
                       "accompanied by a broader discussion of linguistic variation. The "
                       "question stopped being which form is right and became in which register "
                       "and in which variety each form circulates. In classrooms, the effect was "
                       "to make the standard norm an explicit reference, not an invisible ruler."),
        listening=("A matriz brasileira é majoritariamente renovável, mas a diversificação depende "
                   "da transmissão. — E o desmatamento? — Caiu 22%, medido por satélite; a meta é "
                   "reduzir mais 40%."),
        listening_gloss=("The Brazilian energy mix is mostly renewable, but diversification "
                         "depends on transmission. — And deforestation? — It fell 22%, measured "
                         "by satellite; the target is to cut another 40%."),
        voice_tag=VOICE,
        idioms=[
            ("de ponta", "of tip", "cutting-edge"),
            ("em vigor", "in force", "in force, applied since a date"),
            ("à luz de", "in the light of", "in the light of, considering"),
            ("dar conta de", "to give account of", "to handle, to manage"),
            ("em jogo", "in play", "at stake"),
            ("pôr em xeque", "to put in check", "to call into question"),
            ("por conta disso", "on account of that", "because of that"),
            ("a longo prazo", "in the long term", "over the long run"),
            ("sair do papel", "to leave the paper", "to go from plan to practice"),
            ("medir o impacto", "to measure the impact", "to quantify the effect"),
        ],
        mistakes=[
            ("O desmatamento caíram 22%.", "O desmatamento caiu 22%.", "Singular subject, singular verb."),
            ("A norma-padrão serve para referência.", "A norma-padrão serve de referência.", "The pattern is servir de."),
            ("São falado mais de 150 línguas.", "São faladas mais de 150 línguas.", "The passive agrees with línguas."),
        ],
        task_title="Um verbete para o debate",
        task_instructions=("Choose one term from this rung — matriz energética, variação "
                           "linguística or cooficialização — and write an encyclopedic entry of "
                           "eight lines: definition, one number with its source kind, one "
                           "qualification (em vigor desde, medido por, majoritariamente) and one "
                           "sentence on what remains open. Then rewrite the same entry for a "
                           "newspaper and mark which hedge you had to drop."),
    ),
    "test": [
        ("translate_en", "Say: deforestation fell 22%, measured by satellite.", "O desmatamento caiu 22%, medido por satélite."),
        ("translate_pt", "A norma-padrão serve de referência, não de medida.", "The standard norm serves as a reference, not as a measure."),
        ("multiple_choice", "Which sentence opens an academic abstract?", "Este artigo analisa a cobertura jornalística."),
        ("fill_in_the_blank", "O trabalho está estruturado ___ três partes.", "em"),
        ("word_selection", "Select the Portuguese for 'heritage language'.", "língua de herança"),
        ("error_correction", "São falado mais de 150 línguas indígenas.", "São faladas mais de 150 línguas indígenas."),
        ("dialogue_completion", "Complete: E o gargalo? — ___ (transmission: diversification depends on it)", "A transmissão: a diversificação depende dela"),
        ("matching", "Match cooficialização to its meaning.", "making a language co-official"),
        ("reading_comprehension", "Segundo o texto, o que mudou com o acordo ortográfico?", "less than people imagined"),
        ("inference", "O texto diz que a norma-padrão passou a ser 'referência explícita'. What does this tell us about how it should be taught?", "as something named and discussed rather than assumed"),
        ("main_idea", "O texto trata do acordo ortográfico e da discussão sobre variação. — what is this sentence?", "the main point of the reading"),
        ("detail_identification", "Em que ano o acordo entrou em vigor no Brasil?", "2009"),
    ],
}

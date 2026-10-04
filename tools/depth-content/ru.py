# -*- coding: utf-8 -*-
"""Russian PHASE 1 depth — extras, third lessons, half-step rungs.

Written with the DSL in `tools/depth_kit.py`; rendered by
`tools/author-depth.py --lang ru`.

House style follows the shipped Russian course: the language in `t` (Cyrillic),
the course's romanisation in `r` — stressed syllable in CAPITALS, hyphens
between syllables, ASCII only, final obstruents devoiced (`drook`, `chehk`),
`-ть` written `-ty` (`khah-DEE-ty`) — and English in `en`, because the course
teaches in English. Unit ids keep each rung's shipped scheme (`A1-U1` /
`A1-U1-L1` for A1–B2, `ru-c1-u1` / `ru-c1-l1` for C1–C2); the half-step rungs use
`<RUNG>P-U1` (A1P-U1 … C1P-U1) and their lessons carry no id, because the
renderer assigns one.

Register note: A1 keeps the present and `у меня есть`; A2 adds the past, the
future with `буду`, and the accusative/prepositional cases; B1 the motion verbs,
aspect and the dative; B2 the genitive and instrumental plus written argument;
C1–C2 work in the register of official documents, expert assessments and
translation (заявление, заключение, оговорка, реалия). The romanisation column
carries no accent marks on purpose: the course marks stress with capitals, and
`tools/normalise-romanisation.py` (which owns the ru files) strips marks from
`r` values — a mark here would be rewritten, not shipped.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # tools/ on the path
from depth_kit import D, EXTRA, G, L, T, V, WS, X   # noqa: E402

CODE = "ru"
NAME = "Russian"
NATIVE = "русский"
PHASE = 1
SCRIPT = "Cyrillic script"
VOICE = "ru-RU"
SKILL = ("Russian: the Cyrillic alphabet, six cases, verbal aspect "
         "(делать / сделать), the motion verbs (идти / ходить, ехать / ездить), "
         "ты vs вы with имя-отчество, and the written register of official "
         "documents and expert prose")

EXTRAS = {}
THIRD = {}
HALFSTEPS = {}

# ── extras: one block per CEFR rung ────────────────────────────────────────

EXTRAS["A1"] = EXTRA(
    culture=("An introduction in Russia carries three names, not one: имя (Anna), "
             "отчество (Ivanovna, from the father's name) and фамилия (Smirnova). The "
             "middle name is not optional in adult life — a teacher, an official or a "
             "doctor is addressed by имя and отчество (Анна Ивановна), никогда by the "
             "first name alone. The pronoun decides the distance: вы for anyone older or "
             "newer, ты only for friends, family and children. Getting this wrong sounds "
             "worse than any grammar mistake a beginner can make."),
    source_url="https://en.wikipedia.org/wiki/Eastern_Slavic_naming_customs",
    reading=("Это Анна Ивановна. Она преподаватель. Её отчество — Ивановна, потому что "
             "её отца зовут Иван. Студенты говорят ей «здравствуйте» и называют её по "
             "имени и отчеству. Её подруга говорит ей «привет, Аня» — Аня это короткое "
             "имя. Один человек, три имени: Анна, Аня и Анна Ивановна."),
    reading_gloss=("This is Anna Ivanovna. She is a teacher. Her patronymic is Ivanovna, "
                   "because her father is called Ivan. The students say 'hello' to her and "
                   "call her by her first name and patronymic. Her friend says 'hi, Anya' "
                   "to her — Anya is the short name. One person, three names: Anna, Anya "
                   "and Anna Ivanovna."),
    listening=("Здравствуйте! Меня зовут Анна Ивановна. — Очень приятно. А вас? — "
               "Меня зовут Иван Петрович. — Извините, как ваше отчество? — Петрович."),
    listening_gloss=("Hello! My name is Anna Ivanovna. — Very pleased to meet you. And you? "
                     "— My name is Ivan Petrovich. — Excuse me, what is your patronymic? — "
                     "Petrovich."),
    voice_tag=VOICE,
    idioms=[
        ("ни пуха ни пера", "neither down nor feather", "good luck — said before an exam or a hunt"),
        ("с лёгким паром", "with light steam", "said to someone who has just had a bath"),
        ("добро пожаловать", "good welcome", "welcome — the sign at every door"),
        ("приятного аппетита", "pleasant appetite", "enjoy your meal, said before eating"),
        ("хлеб да соль", "bread and salt", "the old greeting to a guest at the table"),
        ("не за что", "not for what", "don't mention it — the answer to спасибо"),
        ("как дела", "how are the deeds", "how are things — the everyday question"),
        ("всё в порядке", "everything is in order", "all is fine — the neutral answer"),
        ("спокойной ночи", "calm night", "good night, said when parting for bed"),
        ("очень приятно", "very pleasant", "pleased to meet you, said while shaking hands"),
    ],
    mistakes=[
        ("Привет, Иван Петрович!", "Здравствуйте, Иван Петрович!", "A name with a patronymic asks for здравствуйте, not привет."),
        ("Меня зовут я Анна.", "Меня зовут Анна.", "Меня зовут already contains the pronoun; я is never added."),
        ("Я зовут Анна.", "Меня зовут Анна.", "The fixed frame is меня зовут, in the accusative."),
    ],
    task_title="Три имени",
    task_instructions=("Write six lines of introduction between a student and a teacher: greet, "
                       "give your имя and отчество, ask the other person's, answer, say "
                       "очень приятно and take leave. Then read it aloud twice and check "
                       "three things: вы everywhere, отчество built from the father's name "
                       "with -ович / -овна, and no я after меня зовут."),
)

EXTRAS["A2"] = EXTRA(
    culture=("Russian tea is a meal, not a pause. Чай пьют from a glass in a podstakannik or "
             "from a cup, strong, with lemon or milk, always with something on the table: "
             "печенье, варенье, бутерброды. The samovar survives as a symbol — in a flat it "
             "is usually an electric kettle and a teapot for заварка. Phrases move with the "
             "drink: «Чай да сахар!» greets someone already drinking, «на дорожку» is the "
             "last cup before leaving, and no guest is ever released without one."),
    source_url="https://en.wikipedia.org/wiki/Russian_cuisine",
    reading=("Вечером у нас чай. Мама ставит чайник и делает заварку. На столе хлеб, сыр и "
             "варенье. Бабушка любит чай с лимоном, а папа — с молоком. Мы сидим на кухне "
             "и говорим. Потом я мою чашки, а мама говорит: «Спасибо, всё было вкусно»."),
    reading_gloss=("In the evening we have tea. Mum puts the kettle on and makes the brew. "
                   "On the table there is bread, cheese and jam. Grandma likes tea with "
                   "lemon, and dad with milk. We sit in the kitchen and talk. Then I wash "
                   "the cups, and mum says: 'Thank you, everything was tasty.'"),
    listening=("Что будем пить, чай или кофе? — Чай, пожалуйста. С лимоном. — А ты? — Мне "
               "кофе с молоком. И что-нибудь к чаю. — Есть печенье и варенье."),
    listening_gloss=("What shall we drink, tea or coffee? — Tea, please. With lemon. — And "
                     "you? — Coffee with milk for me. And something to go with it. — There "
                     "is biscuits and jam."),
    voice_tag=VOICE,
    idioms=[
        ("пальчики оближешь", "you will lick your fingers", "delicious — said of food"),
        ("хлеб всему голова", "bread is the head of everything", "bread is the foundation of a meal"),
        ("копейка рубль бережёт", "a kopeck saves the rouble", "small savings add up"),
        ("сыт по горло", "full up to the throat", "fed up, had more than enough"),
        ("ни рыба ни мясо", "neither fish nor meat", "neither one thing nor the other, nondescript"),
        ("как грибы после дождя", "like mushrooms after rain", "springing up everywhere, fast"),
        ("дорого-богато", "expensive and rich", "flashy, over-decorated, said with irony"),
        ("на скорую руку", "on a quick hand", "thrown together in a hurry"),
        ("с пустыми руками", "with empty hands", "arriving without a gift"),
        ("чай да сахар", "tea and sugar", "said to someone already drinking tea"),
    ],
    mistakes=[
        ("Я люблю чай с молоко.", "Я люблю чай с молоком.", "С takes the instrumental: с молоком."),
        ("Мы были в Москва.", "Мы были в Москве.", "В + place in the prepositional: в Москве."),
        ("Сколько стоит эти яблоки?", "Сколько стоят эти яблоки?", "Plural subject, plural verb: стоят."),
    ],
    task_title="На кухне",
    task_instructions=("Write a shopping list for tea in Russian with prices (хлеб 40 рублей, "
                       "сыр 200 рублей …), then write a six-line dialogue in which two "
                       "people choose what to drink and one asks for something to go with "
                       "it. Check three things: с + instrumental for what goes with what, "
                       "стоит / стоят agreeing with the price subject, and в + prepositional "
                       "for where the tea happens."),
)

EXTRAS["B1"] = EXTRA(
    culture=("Дача is not a country house and not a farm: it is a small plot with a wooden "
             "house, a garden and a greenhouse, reached by elektrichka on Friday evening and "
             "left on Sunday. Families grow cucumbers, tomatoes, berries and dill, and the "
             "summer's work is measured in jars — соленья, варенье, компот — put up for the "
             "winter. The dacha is also where Russian weather is actually experienced: "
             "открытие сезона in May, the short hot июль, and закрытие сезона in October "
             "with the water turned off."),
    source_url="https://en.wikipedia.org/wiki/Dacha",
    reading=("В пятницу вечером мы едем на дачу. Электричка идёт сорок минут, потом десять "
             "минут пешком. На даче нас ждут грядки: огурцы, помидоры и зелень. В субботу "
             "папа копает, мама поливает, а я собираю ягоды. Вечером мы пьём чай на "
             "веранде. В воскресенье мы закрываем дом и возвращаемся в город."),
    reading_gloss=("On Friday evening we go to the dacha. The suburban train takes forty "
                   "minutes, then ten minutes on foot. At the dacha the vegetable beds "
                   "wait for us: cucumbers, tomatoes and herbs. On Saturday dad digs, mum "
                   "waters, and I pick berries. In the evening we drink tea on the veranda. "
                   "On Sunday we close the house and go back to the city."),
    listening=("Какая погода будет в субботу? — Обещают дождь. — Тогда поедем на дачу в "
               "воскресенье. — Хорошо, но если будет дождь, останемся дома."),
    listening_gloss=("What will the weather be like on Saturday? — They promise rain. — "
                     "Then we'll go to the dacha on Sunday. — Fine, but if it rains we'll "
                     "stay at home."),
    voice_tag=VOICE,
    idioms=[
        ("биться как рыба об лёд", "to beat like a fish against ice", "to struggle with no way out"),
        ("вилами по воде писано", "written with pitchforks on water", "still uncertain, not settled"),
        ("взять себя в руки", "to take oneself into the hands", "to pull yourself together"),
        ("глаза боятся, а руки делают", "the eyes fear but the hands do", "start and the work will follow"),
        ("дело в шляпе", "the matter is in the hat", "the deal is done"),
        ("засучив рукава", "with the sleeves rolled up", "working hard and without delay"),
        ("как снег на голову", "like snow on the head", "out of the blue, without warning"),
        ("медвежья услуга", "a bear's service", "a disservice done with good intentions"),
        ("первый блин комом", "the first pancake comes out a lump", "the first attempt usually fails"),
        ("тише едешь — дальше будешь", "you go quieter — you will be further", "slow and steady wins"),
    ],
    mistakes=[
        ("Я иду на дачу каждый weekend.", "Я езжу на дачу каждые выходные.", "Regular trips take ездить; идти is only the trip happening now."),
        ("Я прочитал эту книгу два часа.", "Я читал эту книгу два часа.", "A duration spent on the process takes the imperfective читал."),
        ("В субботу будет дождь, поэтому мы поедем на дачу, несмотря на дождь.", "Если в субботу будет дождь, мы поедем на дачу в воскресенье.", "A condition is said once, with если — not repeated."),
    ],
    task_title="Планы на выходные",
    task_instructions=("Write a six-line plan for a weekend at the dacha: what the weather "
                       "will be, who does which job, what you will cook, and what happens if "
                       "it rains. Use three structures from this rung — the future with "
                       "буду/поедем, a real condition with если + future, and one motion "
                       "verb pair (ехать / ездить) — then read it aloud and check the aspect "
                       "of каждое verb: process or result."),
)

EXTRAS["B2"] = EXTRA(
    culture=("Russian literature is read at home the way other countries read scripture: "
             "Пушкин's Евгений Онегин supplies the lines people quote without noticing, "
             "Достоевский and Толстой are argued about as moral authorities, and Чехов's "
             "plays are still cast every season. The theatre carries the same weight — "
             "МХТ, Большой, Вахтангов — and a ticket is bought months ahead. In speech the "
             "canon appears as shorthand: «пушкинский вопрос», «чеховское настроение», "
             "«толстовское» as an adjective for a whole way of looking at a village."),
    source_url="https://en.wikipedia.org/wiki/Russian_literature",
    reading=("В субботу мы были в театре. Давали Чехова — «Вишнёвый сад». Зал был полный; "
             "многие пришли с книгами. После третьего действия мы вышли в фойе и спорили: "
             "конец у пьесы смешной или трагический? Мой друг считает, что Чехов не "
             "смеётся над героями, а жалеет их. Я не согласен, но его аргументы сильнее."),
    reading_gloss=("On Saturday we were at the theatre. They were performing Chekhov — "
                   "'The Cherry Orchard'. The hall was full; many had come with books. "
                   "After the third act we went out into the foyer and argued: is the end "
                   "of the play funny or tragic? My friend thinks Chekhov does not laugh at "
                   "his characters but pities them. I disagree, but his arguments are "
                   "stronger."),
    listening=("Ты дочитал роман? — Дочитал вчера. — И как тебе конец? — Скажу честно: я "
               "ждал другого. Но чем больше думаю, тем больше он мне нравится."),
    listening_gloss=("Have you finished the novel? — I finished it yesterday. — And how do "
                     "you like the ending? — Honestly: I expected something else. But the "
                     "more I think about it, the more I like it."),
    voice_tag=VOICE,
    idioms=[
        ("крокодиловы слёзы", "crocodile tears", "insincere regret"),
        ("ни в зуб ногой", "not a foot in a tooth", "to know nothing at all about something"),
        ("остаться с носом", "to be left with a nose", "to be left with nothing after being cheated"),
        ("подливать масла в огонь", "to pour oil into the fire", "to make a conflict worse"),
        ("рубить с плеча", "to chop from the shoulder", "to act or judge rashly"),
        ("смотреть сквозь пальцы", "to look through the fingers", "to overlook something on purpose"),
        ("тянуть кота за хвост", "to pull the cat by the tail", "to stall and delay"),
        ("яблоку негде упасть", "nowhere for an apple to fall", "packed, no room at all"),
        ("игра не стоит свеч", "the game is not worth the candles", "not worth the effort"),
        ("слово не воробей", "a word is not a sparrow", "once spoken, it cannot be taken back"),
    ],
    mistakes=[
        ("У меня нет время.", "У меня нет времени.", "Нет takes the genitive: времени."),
        ("Я горжусь за тебя.", "Я горжусь тобой.", "Гордиться takes the instrumental, with no за."),
        ("Я пришёл с друг.", "Я пришёл с другом.", "С takes the instrumental: с другом."),
    ],
    task_title="Рецензия на вечер",
    task_instructions=("Write a short review of a book, a play or a film you know: what it "
                       "is, what it argues, one thing you agree with and one thing you do "
                       "not, and what you would tell a friend. Use at least one genitive "
                       "after нет / нет времени and one instrumental with с or гордиться. "
                       "Then rewrite the last sentence so that it concedes something, with "
                       "хотя or однако."),
)

EXTRAS["C1"] = EXTRA(
    culture=("Russian is the largest native language in Europe and the eighth most spoken "
             "in the world, with roughly 258 million speakers; it is an official language of "
             "the United Nations, of the CIS and of the Eurasian Economic Union, and the "
             "working language of the Baikonur cosmodrome. Cyrillic, adapted from the "
             "Bulgarian school of the ninth century, became the script of more than fifty "
             "languages and of the first satellite and the first human spaceflight. In "
             "Central Asia and the Caucasus it remains the language of interethnic "
             "communication, and in the diaspora — Germany, Israel, the United States — it "
             "is kept as a language of home, not of the street."),
    source_url="https://en.wikipedia.org/wiki/Russian_language",
    reading=("Русский язык работает как язык-посредник там, где десятки языков соседствуют "
             "ежедневно. В Ташкенте или Бишкеке разговор двух людей, не знающих языков "
             "друг друга, часто идёт по-русски, хотя русский не является родным ни для "
             "одного из них. Языковая политика постсоветских стран различается: где-то "
             "русский вытесняется из школ, где-то возвращается в деловую сферу. Для "
             "лингвиста интересно не столько число говорящих, сколько то, какие функции "
             "язык сохраняет в каждом из этих обществ."),
    reading_gloss=("Russian works as a lingua franca where dozens of languages live side by "
                   "side daily. In Tashkent or Bishkek a conversation between two people who "
                   "do not know each other's languages often happens in Russian, although "
                   "Russian is the native language of neither of them. The language policy "
                   "of the post-Soviet states differs: somewhere Russian is being pushed out "
                   "of schools, somewhere it is returning to business. What interests a "
                   "linguist is not so much the number of speakers as which functions the "
                   "language keeps in each of those societies."),
    listening=("Сколько человек говорит по-русски? — Около двухсот пятидесяти миллионов, "
               "если считать и вторых, и третьих языки. — И что здесь важнее для "
               "исследования? — Не количество, а функции: наука, космос, торговля, "
               "межнациональное общение."),
    listening_gloss=("How many people speak Russian? — About two hundred and fifty million, "
                     "if you count second and third languages. — And what matters more for "
                     "research here? — Not the number but the functions: science, space, "
                     "trade, interethnic communication."),
    voice_tag=VOICE,
    idioms=[
        ("камень преткновения", "a stone of stumbling", "the stumbling block in a dispute"),
        ("притча во языцех", "a parable in tongues", "a byword, something everyone talks about"),
        ("краеугольный камень", "the cornerstone", "the foundation everything rests on"),
        ("яблоко раздора", "the apple of discord", "the point that starts the quarrel"),
        ("дамоклов меч", "the sword of Damocles", "a threat hanging overhead"),
        ("ахиллесова пята", "the Achilles heel", "the single weak point"),
        ("сизифов труд", "the labour of Sisyphus", "endless work with no result"),
        ("прокрустово ложе", "the bed of Procrustes", "a standard that cuts to fit"),
        ("танталовы муки", "the torments of Tantalus", "temptation kept just out of reach"),
        ("перейти Рубикон", "to cross the Rubicon", "to take an irreversible step"),
    ],
    mistakes=[
        ("Согласно отчёта, показатели выросли.", "Согласно отчёту, показатели выросли.", "Согласно takes the dative: отчёту."),
        ("Несмотря на того, что данные неполные, вывод надёжен.", "Несмотря на то, что данные неполные, вывод надёжен.", "The fixed frame is несмотря на то, что."),
        ("В виду того, что выборка мала, нужна оговорка.", "Ввиду того, что выборка мала, нужна оговорка.", "Причина is written ввиду, as one word; в виду = within sight."),
    ],
    task_title="Заметка о функции языка",
    task_instructions=("Write an eight-line analytical note in the official register on the "
                       "place of Russian in one country of your choice: state the function "
                       "(школа, наука, торговля), attribute the claim with согласно + "
                       "dative, qualify it with ввиду того, что or при условии, что, and "
                       "close with a limitation (оговорка). Then reread it and replace any "
                       "sentence that only reports with one that assesses."),
)

EXTRAS["C2"] = EXTRA(
    culture=("Russian music travels in two directions at once. The nineteenth-century line — "
             "Глинка, Мусоргский, Чайковский, Рахманинов — gave the concert hall its "
             "repertoire; the twentieth-century line split into Шостакович writing under "
             "pressure and the songs people actually sang — Окуджава with a guitar in a "
             "kitchen, Высоцкий with a hoarse voice and no official stage, Кино and Виктор "
             "Цой filling stadiums in the last years of the USSR. The kitchen, the магнитофон "
             "and the stadium are three places where a Russian song has been heard, and the "
             "word «бард» covers the first of them exactly."),
    source_url="https://en.wikipedia.org/wiki/Music_of_Russia",
    reading=("Один и тот же вечер может быть описан двумя языками. В филармонии скажут: "
             "«прозвучала Седьмая симфония Шостаковича». На кухне скажут: «он спел под "
             "гитару». Это не два уровня качества, а две разные функции: зал сохраняет "
             "партитуру, кухня сохраняет интонацию. Бардовская песня держится на втором: "
             "голос, гитара и текст, который можно повторить, не имея ни слуха, ни "
             "образования. Именно поэтому она пережила и магнитофон, и стадион."),
    reading_gloss=("The same evening can be described in two languages. In the philharmonic "
                   "hall they will say: 'Shostakovich's Seventh Symphony was performed'. In "
                   "the kitchen they will say: 'he sang with a guitar'. These are not two "
                   "levels of quality but two different functions: the hall preserves the "
                   "score, the kitchen preserves the intonation. The bard song rests on the "
                   "second: a voice, a guitar and a text one can repeat without either an ear "
                   "or an education. That is exactly why it outlived both the tape recorder "
                   "and the stadium."),
    listening=("Кто для тебя главный в русской музыке? — Если честно, Цой. — Почему не "
               "классика? — Классику я уважаю, но она для зала. А Цой — для кухни и для "
               "дороги: три аккорда, и человек уже поёт."),
    listening_gloss=("Who is the main figure in Russian music for you? — Honestly, Tsoi. — "
                     "Why not the classics? — I respect the classics, but they are for the "
                     "hall. And Tsoi is for the kitchen and the road: three chords, and the "
                     "person is already singing."),
    voice_tag=VOICE,
    idioms=[
        ("играть первую скрипку", "to play first violin", "to lead, to be the main figure"),
        ("медведь на ухо наступил", "a bear stepped on his ear", "to be totally tone-deaf"),
        ("петь дифирамбы", "to sing dithyrambs", "to praise excessively"),
        ("по большому счёту", "by the big account", "all things considered, strictly speaking"),
        ("держать марку", "to hold the brand", "to keep up the standard"),
        ("не в своей тарелке", "not in one's own plate", "ill at ease, out of place"),
        ("водить за нос", "to lead by the nose", "to deceive someone over time"),
        ("сойти со сцены", "to come off the stage", "to leave public life"),
        ("в унисон", "in unison", "sounding together, thinking alike"),
        ("ставить на карту", "to put on the card", "to stake everything on one thing"),
    ],
    mistakes=[
        ("В отличие от классики, рок считается не серьёзной музыкой.", "В отличие от классики, рок не считается серьёзной музыкой.", "One negation: не считается, without a second не before the adjective."),
        ("Этот композитор влиял на меня сильно.", "Этот композитор сильно повлиял на меня.", "A completed effect takes повлиял, with сильно before the verb."),
        ("Музыка, что я слушаю, старая.", "Музыка, которую я слушаю, старая.", "The relative pronoun takes the case the verb governs: которую."),
    ],
    task_title="Две функции одного вечера",
    task_instructions=("Take one piece of music you know and write two descriptions of it, "
                       "one for a concert programme and one for a kitchen conversation. "
                       "Then write a paragraph that mediates between them, using по большому "
                       "счёту, в отличие от and one relative clause with который in the "
                       "right case. Read the mediation aloud and check that no sentence "
                       "claims the two registers are the same thing."),
)

# ── third lessons: one in every shipped unit ───────────────────────────────

THIRD["A1"] = [
    ("A1-U1", "A1-U1-L3", L("Буквы и звуки: русский алфавит",
        "Cyrillic has 33 letters: 10 vowels, 21 consonants and two signs that make no sound "
        "of their own. Five letters look Latin and are not: В is v, Н is n, Р is a rolled r, "
        "С is s, У is oo. The soft sign ь does not sound — it softens the consonant before "
        "it (мать, день). Stress is not marked in print, so it is learned with the word.",
        [V("буква", "BOO-kvah", "letter", "noun"),
         V("звук", "zvook", "sound", "noun"),
         V("слово", "SLOH-vah", "word", "noun"),
         V("читать", "chee-TAHTY", "to read", "verb"),
         V("писать", "pee-SAHTY", "to write", "verb")],
        G("Буквы, которые обманывают",
          "В = в · Н = н · Р = р · С = с · У = у · ь не звучит",
          "Read Cyrillic by sound, not by shape. В, Н, Р, С and У are the five that catch a "
          "beginner: вода is vah-DAH, нос is nohs, рыба is RIH-bah, сок is sohk, утро is "
          "OO-trah. The soft sign ь has no sound of its own; it makes the consonant before "
          "it soft, which is why мать ends in a soft t. Stress falls on one syllable per "
          "word and is not printed: молоко is mah-lah-KOH.",
          [X("Это вода.", "EH-tah vah-DAH.", "This is water."),
           X("Мой нос.", "moy nohs.", "My nose."),
           X("Я читаю слово.", "yah chee-TAH-yoo SLOH-vah.", "I am reading a word.")],
          [("Я читаю «Р» как английское R.", "Я читаю «Р» кончиком языка, раскатисто.", "Russian р is a trill, not the English r."),
           ("В слове «день» есть звук ь.", "В слове «день» буква ь не звучит, она смягчает н.", "ь marks softness; it is never pronounced.")]),
        [D("Учитель", "Как пишется ваша фамилия?", "kahk PEE-sheht-syah VAH-shah fah-MEE-lee-yah?", "How is your surname spelled?"),
         D("Студент", "Смирнова: С-М-И-Р-Н-О-В-А.", "smeer-NOH-vah: ehS-ehM-EE-ehR-ehN-OH-veh-AH.", "Smirnova: S-M-I-R-N-O-V-A."),
         D("Учитель", "Спасибо. А как читается?", "spah-SEE-bah. ah kahk chee-TAH-yeht-syah?", "Thank you. And how is it read?"),
         D("Студент", "Смирнова, ударение на «о».", "smeer-NOH-vah, oo-dah-RYEH-nee-yeh nah OH.", "Smirnova, the stress is on the o.")],
        WS("Alphabet worksheet", [
            T("Read the five tricky letters.", ["water", "nose", "fish"],
              ["вода", "нос", "рыба"]),
            T("Spell it out.", ["my surname is Ivanov", "the stress is on the second syllable"],
              ["Моя фамилия Иванов", "Ударение на втором слоге"]),
        ]))),
    ("A1-U2", "A1-U2-L3", L("Цвета и вещи: какой, какая, какое",
        "A colour is an adjective and must agree with the thing: красный дом, красная машина, "
        "красное окно, красные цветы. The question words agree in the same way — какой дом? "
        "какая машина? какое окно? какая is for feminine, -ое for neuter, -ые for plural. "
        "The ending is the agreement; the stem never changes.",
        [V("цвет", "tsvyet", "colour", "noun"),
         V("красный", "KRAHS-nihy", "red", "adjective"),
         V("синий", "SEE-nee", "blue", "adjective"),
         V("белый", "BYEH-lihy", "white", "adjective"),
         V("новый", "NOH-vihy", "new", "adjective")],
        G("Согласование: какой, какая, какое",
          "-ый / -ий (m) · -ая / -яя (f) · -ое / -ее (n) · -ые / -ие (pl)",
          "The adjective copies the gender and number of its noun. After к, г, х the ending "
          "is -ий, not -ый: синий, русский. The question must agree too — you ask какая "
          "машина?, not какой машина. Colour stands before the noun in the neutral order: "
          "белый снег, but снег белый also works when the colour is the news.",
          [X("Это красная машина.", "EH-tah KRAHS-nah-yah mah-SHEE-nah.", "This is a red car."),
           X("У меня новый телефон.", "oo meh-NYAH NOH-vihy tee-leh-FOHN.", "I have a new phone."),
           X("Какие у вас чашки? — Синие.", "kah-KEE-yeh oo vahs CHAHSH-kee? — SEE-nee-yeh.", "What colour are your cups? — Blue.")],
          [("Это красный машина.", "Это красная машина.", "Машина is feminine: красная."),
           ("У меня новое дом.", "У меня новый дом.", "Дом is masculine: новый.")]),
        [D("Продавец", "Какой цвет вам нужен?", "kah-KOY tsvyet vahm NOO-zhehn?", "Which colour do you need?"),
         D("Покупатель", "Синий, пожалуйста. Вот эта куртка.", "SEE-nee, pah-ZHAH-loo-stah. voht EH-tah KOORT-kah.", "Blue, please. That jacket there."),
         D("Продавец", "Синяя есть, а красная — только большая.", "SEE-nee-yah yehsty, ah KRAHS-nah-yah — TOHL-kah bahl-SHAH-yah.", "The blue one is available, but the red one only in large."),
         D("Покупатель", "Тогда беру синюю.", "tahg-DAH beh-ROO SEE-nee-yoo.", "Then I'll take the blue one.")],
        WS("Colours worksheet", [
            T("Agree the adjective.", ["a red car", "a new phone", "blue cups"],
              ["красная машина", "новый телефон", "синие чашки"]),
            T("Ask for the colour.", ["which colour do you need?", "the red one only in large"],
              ["Какой цвет вам нужен?", "Красная только большая"]),
        ]))),
    ("A1-U3", "A1-U3-L3", L("Моя семья и работа",
        "Two sentences carry a whole introduction: у меня есть + who, and я работаю + where. "
        "The profession stands in the nominative with no article — я врач, она инженер. "
        "Where you work takes в or на and the prepositional case: работаю в школе, работаю "
        "на заводе. The question is кто вы по профессии?",
        [V("семья", "seem-YAH", "family", "noun"),
         V("работать", "rah-BOH-tahty", "to work", "verb"),
         V("врач", "vrahch", "doctor", "noun"),
         V("учитель", "oo-CHEE-tyehl", "teacher", "noun"),
         V("инженер", "een-zheh-NYEHR", "engineer", "noun")],
        G("Кто вы по профессии?",
          "у меня есть + кто · я работаю + где (в / на + prepositional) · я врач",
          "A profession needs no я есть: я врач, она учитель. To say where, working takes в "
          "for institutions (в школе, в банке) and на for factories, post offices and some "
          "sites (на заводе, на почте, на стройке). With a plural family, есть takes the "
          "nominative plural: у меня есть брат и сестра.",
          [X("У меня есть брат и сестра.", "oo meh-NYAH yehsty braht ee sees-TRAH.", "I have a brother and a sister."),
           X("Я работаю в школе, а жена — в банке.", "yah rah-BOH-tah-yoo v SHKOH-leh, ah zheh-NAH — v BAHN-keh.", "I work at a school, and my wife at a bank."),
           X("Он инженер, она врач.", "ohn een-zheh-NYEHR, ah-NAH vrahch.", "He is an engineer, she is a doctor.")],
          [("Я работаю в врач.", "Я врач.", "A profession stands alone: я врач."),
           ("У меня есть сестра и брат есть.", "У меня есть сестра и брат.", "Есть is said once.")]),
        [D("Анна", "Кто вы по профессии?", "ktoh vih pah prah-FYEH-see-ee?", "What do you do for a living?"),
         D("Иван", "Я инженер, работаю на заводе.", "yah een-zheh-NYEHR, rah-BOH-tah-yoo nah zah-VOH-dyeh.", "I'm an engineer, I work at a factory."),
         D("Анна", "А ваша семья?", "ah VAH-shah seem-YAH?", "And your family?"),
         D("Иван", "У меня есть жена и двое детей.", "oo meh-NYAH yehsty zheh-NAH ee DVOH-yeh deh-TYEY.", "I have a wife and two children.")],
        WS("Family and work worksheet", [
            T("Introduce the family.", ["I have a brother and a sister", "he is an engineer, she is a doctor"],
              ["У меня есть брат и сестра", "Он инженер, она врач"]),
            T("Say where people work.", ["I work at a school", "my wife works at a bank"],
              ["Я работаю в школе", "Моя жена работает в банке"]),
        ]))),
]

THIRD["A2"] = [
    ("A2-U1", "A2-U1-L3", L("Выходные: как прошло",
        "The past tense agrees with the subject: я был, она была, мы были. Weather and "
        "impressions are reported in the neuter with no subject at all: было холодно, было "
        "интересно, было шумно. Where English says 'we had a good time', Russian says мы "
        "хорошо провели время — the verb carries the subject, not an auxiliary.",
        [V("выходной", "vih-khahd-NOY", "day off, weekend day", "noun"),
         V("гулять", "goo-LYAHTY", "to walk, to stroll", "verb"),
         V("смотреть", "smah-TRYEHTY", "to watch", "verb"),
         V("интересно", "een-teh-RYES-nah", "interesting", "adverb"),
         V("устать", "oo-STAHty", "to get tired", "verb")],
        G("Как прошли выходные",
          "я был / она была / мы были · было холодно · мы хорошо провели время",
          "The past tense marks the subject's gender: был (he), была (she), было (it), были "
          "(all plurals). An impression has no subject and stays neuter: было весело, было "
          "скучно. Провести время is the verb for spending time — провёл, провела, "
          "провели.",
          [X("В субботу мы гуляли в парке.", "v soo-BOH-too mih goo-LYAH-lee v PAHR-kyeh.", "On Saturday we walked in the park."),
           X("Было холодно, но интересно.", "BIH-lah KHO-lahd-nah, noh een-teh-RYES-nah.", "It was cold, but interesting."),
           X("Она была дома, а я устал.", "ah-NAH bih-LAH DOH-mah, ah yah oo-STAHL.", "She was at home, and I got tired.")],
          [("Мы был в парке.", "Мы были в парке.", "A plural subject takes были."),
           ("Было интересно книга.", "Книга была интересная.", "An impression with a subject uses the adjective: была интересная.")]),
        [D("Коллега", "Как прошли выходные?", "kahk prahsh-LEE vih-khahd-NIH-yeh?", "How was your weekend?"),
         D("Иван", "Отлично. В субботу мы гуляли, потом смотрели фильм.", "aht-LEECH-nah. v soo-BOH-too mih goo-LYAH-lee, pah-TOHM smah-TRYEH-lee feelm.", "Great. On Saturday we walked, then watched a film."),
         D("Коллега", "А в воскресенье?", "ah v vahs-kree-SYEH-nyeh?", "And on Sunday?"),
         D("Иван", "Было холодно, мы были дома и отдыхали.", "BIH-lah KHO-lahd-nah, mih BIH-lee DOH-mah ee ahd-dih-KHAH-lee.", "It was cold, we were at home resting.")],
        WS("Weekend worksheet", [
            T("Report the past.", ["on Saturday we walked in the park", "she was at home and I got tired"],
              ["В субботу мы гуляли в парке", "Она была дома, а я устал"]),
            T("Report the impression.", ["it was cold but interesting", "how was your weekend?"],
              ["Было холодно, но интересно", "Как прошли выходные?"]),
        ]))),
    ("A2-U2", "A2-U2-L3", L("Куда и где: в магазине и в магазин",
        "One letter separates movement from location: я иду в магазин (I am going to the "
        "shop, accusative) and я в магазине (I am in the shop, prepositional). Домой means "
        "homewards and дома means at home — they are two different words. The question "
        "matches the case: куда? asks for the accusative, где? for the prepositional.",
        [V("куда", "koo-DAH", "where to", "adverb"),
         V("где", "gdyeh", "where", "adverb"),
         V("домой", "dah-MOY", "homewards", "adverb"),
         V("этаж", "eh-TAHSH", "floor, storey", "noun"),
         V("лифт", "leeft", "lift, elevator", "noun")],
        G("Куда? Где?",
          "куда → в / на + accusative · где → в / на + prepositional · домой / дома",
          "Куда ты идёшь? — В магазин. Где ты? — В магазине. The same preposition serves "
          "both questions; the ending decides. Домой and дома are the irregular pair: я иду "
          "домой, я дома. With в and на the accusative is the destination and the "
          "prepositional the place, and —е / -у endings mark the difference: на работу / на "
          "работе, в школу / в школе.",
          [X("Куда ты идёшь? — В магазин.", "koo-DAH tih ee-DYOHSH? — v mah-gah-ZEEN.", "Where are you going? — To the shop."),
           X("Где ты? — В магазине, на втором этаже.", "gdyeh tih? — v mah-gah-ZEE-nyeh, nah ftah-ROHM eh-tah-ZHEH.", "Where are you? — In the shop, on the second floor."),
           X("Вечером я дома, потом иду домой.", "VYEH-cheh-rahm yah DOH-mah, pah-TOHM ee-DOO dah-MOY.", "In the evening I am at home, then I go home.")],
          [("Я иду в магазине.", "Я иду в магазин.", "Movement takes the accusative: в магазин."),
           ("Я дома иду вечером.", "Вечером я иду домой.", "Домой is the direction; дома is the location.")]),
        [D("Анна", "Ты где?", "tih gdyeh?", "Where are you?"),
         D("Иван", "Я в магазине, на первом этаже.", "yah v mah-gah-ZEE-nyeh, nah PYER-vahm eh-tah-ZHEH.", "I'm in the shop, on the first floor."),
         D("Анна", "Куда ты идёшь потом?", "koo-DAH tih ee-DYOHSH pah-TOHM?", "Where are you going afterwards?"),
         D("Иван", "Домой. Лифт не работает, придётся пешком.", "dah-MOY. leeft nyeh rah-BOH-tah-yeht, pree-DYOHT-syah peesh-KOHM.", "Home. The lift isn't working, I'll have to walk.")],
        WS("Where and where to worksheet", [
            T("Ask and answer with где.", ["where are you? — in the shop", "the lift is not working"],
              ["Ты где? — В магазине", "Лифт не работает"]),
            T("Ask and answer with куда.", ["where are you going? — to the shop", "in the evening I go home"],
              ["Куда ты идёшь? — В магазин", "Вечером я иду домой"]),
        ]))),
    ("A2-U3", "A2-U3-L3", L("В кафе: заказ и счёт",
        "To order, Russian uses two frames: я буду + accusative (я буду борщ) and мне, "
        "пожалуйста + accusative (мне чай, пожалуйста). The waiter is официант; the bill is "
        "счёт, and чаевые are the tip. Меню and the names of dishes do not change: дайте "
        "меню, пожалуйста.",
        [V("меню", "mee-NYOO", "menu", "noun"),
         V("заказ", "zah-KAHS", "order", "noun"),
         V("счёт", "shchoht", "bill", "noun"),
         V("официант", "ah-fee-TSYAHNT", "waiter", "noun"),
         V("чаевые", "chah-yeh-VIH-yeh", "tip", "noun")],
        G("Заказ и счёт",
          "я буду + accusative · мне, пожалуйста · счёт, пожалуйста · с собой",
          "Я буду борщ и чай names what you will have. Мне, пожалуйста, кофе puts the "
          "person in the dative — literally 'to me, please'. Принесите, пожалуйста, меню is "
          "the polite request with an imperative. С собой means to take away, здесь — to "
          "eat in. The bill is asked for with можно счёт? and чаевые are left in cash.",
          [X("Я буду борщ и чай, пожалуйста.", "yah BOO-doo bohrshtch ee chah-ee, pah-ZHAH-loo-stah.", "I'll have borscht and tea, please."),
           X("Принесите, пожалуйста, меню.", "pree-nee-SEE-tyeh, pah-ZHAH-loo-stah, mee-NYOO.", "Bring the menu, please."),
           X("Можно счёт? С собой, пожалуйста.", "MOHZH-nah shchoht? sah-BOY, pah-ZHAH-loo-stah.", "Could I have the bill? Takeaway, please.")],
          [("Дайте мне меню мне.", "Дайте мне меню, пожалуйста.", "Мне is said once; пожалуйста replaces the second."),
           ("Я буду чай с молоко.", "Я буду чай с молоком.", "С takes the instrumental: с молоком.")]),
        [D("Официант", "Добрый день! Вот меню.", "DOHB-rihy dyen! voht mee-NYOO.", "Good afternoon! Here is the menu."),
         D("Гость", "Спасибо. Я буду борщ и салат.", "spah-SEE-bah. yah BOO-doo bohrshtch ee sah-LAHT.", "Thank you. I'll have borscht and a salad."),
         D("Официант", "Что будете пить?", "shtoh BOO-deh-teh PEETY?", "What will you drink?"),
         D("Гость", "Чай, пожалуйста. И можно счёт сразу — я спешу.", "chah-ee, pah-ZHAH-loo-stah. ee MOHZH-nah shchoht SRAH-zoo — yah speh-SHOO.", "Tea, please. And could I have the bill right away — I'm in a hurry.")],
        WS("Café worksheet", [
            T("Order.", ["I'll have borscht and tea", "bring the menu, please"],
              ["Я буду борщ и чай", "Принесите, пожалуйста, меню"]),
            T("Settle up.", ["could I have the bill?", "takeaway, please"],
              ["Можно счёт?", "С собой, пожалуйста"]),
        ]))),
]

THIRD["B1"] = [
    ("B1-U1", "B1-U1-L3", L("Маршрут: как добраться",
        "A route is told with the unidirectional verbs — ехать, идти — because every leg has "
        "one direction: сначала едете на метро, потом идёте пешком. С пересадкой means with "
        "a change, and the question как добраться? asks for the whole path. На + transport "
        "takes the prepositional: на метро, на автобусе, на поезде.",
        [V("маршрут", "mahr-SHROOT", "route", "noun"),
         V("остановка", "ah-stah-NOHF-kah", "stop (bus)", "noun"),
         V("пересадка", "pee-ree-SAHD-kah", "change, transfer", "noun"),
         V("билет", "bee-LYEHT", "ticket", "noun"),
         V("поезд", "POH-yehzd", "train", "noun")],
        G("Как добраться",
          "на + transport (prepositional) · с пересадкой · сначала … потом …",
          "Every leg of a route takes a one-direction verb: вы едете на метро до станции "
          "«Арбатская», потом идёте пешком пять минут. На метро / на автобусе / на поезде "
          "name the means; с пересадкой warns that one line is not enough. Доехать до + "
          "genitive marks the end of the leg: доехать до центра.",
          [X("Сначала едете на метро, потом идёте пешком.", "snah-CHAH-lah YEH-deh-teh nah meet-ROH, pah-TOHM ee-DYOH-teh peesh-KOHM.", "First you go by metro, then you walk."),
           X("Это далеко? — Нет, две остановки с пересадкой.", "EH-tah dah-leh-KOH? — nyeht, dvyeh ah-stah-NOHF-kee s pee-ree-SAHD-koy.", "Is it far? — No, two stops with a change."),
           X("Сколько стоит билет до центра?", "SKOHL-kah STOH-eet bee-LYEHT dah TSYEHN-trah?", "How much is a ticket to the centre?")],
          [("Я езжу на метро сейчас.", "Я еду на метро сейчас.", "A trip happening now takes еду; езжу is the regular one."),
           ("Идти на автобусе до центра.", "Ехать на автобусе до центра.", "Transport takes ехать, not идти.")]),
        [D("Турист", "Как добраться до Красной площади?", "kahk dahb-RAHT-syah dah KRAHS-nay PLOH-shchah-dee?", "How do I get to Red Square?"),
         D("Прохожий", "Едете на метро до «Охотного ряда», потом идёте пешком.", "YEH-deh-teh nah meet-ROH dah ah-KHOHT-nah-vah RYAH-dah, pah-TOHM ee-DYOH-teh peesh-KOHM.", "Take the metro to Okhotny Ryad, then walk."),
         D("Турист", "С пересадкой?", "s pee-ree-SAHD-koy?", "With a change?"),
         D("Прохожий", "Нет, одна линия. Минут двадцать.", "nyeht, ahd-NAH LEE-nee-yah. mee-NOOT DVAHTS-tsahty.", "No, one line. About twenty minutes.")],
        WS("Route worksheet", [
            T("Give the route.", ["first you go by metro, then you walk", "two stops with a change"],
              ["Сначала едете на метро, потом идёте пешком", "Две остановки с пересадкой"]),
            T("Ask about the fare.", ["how much is a ticket to the centre?", "is it far?"],
              ["Сколько стоит билет до центра?", "Это далеко?"]),
        ]))),
    ("B1-U2", "B1-U2-L3", L("Просьбы и разрешение: можно, помогите",
        "A polite request puts the person in the dative and the verb in the imperative: "
        "помогите мне, пожалуйста; подскажите, как пройти. Можно? asks permission and можно "
        "… ? offers it; нельзя forbids. Занято and свободно answer the question about a seat "
        "or a phone line without naming a person.",
        [V("помочь", "pah-MOHCH", "to help", "verb"),
         V("подсказать", "paht-skah-ZAHTY", "to tell, to prompt", "verb"),
         V("разрешить", "rahz-ree-SHIHty", "to allow", "verb"),
         V("занято", "ZAH-nyah-tah", "taken, occupied", "adverb"),
         V("свободно", "svah-BOHD-nah", "free, available", "adverb")],
        G("Просьба и разрешение",
          "помогите мне + infinitive · можно + infinitive? · занято / свободно",
          "Помогите мне найти is the full polite request: imperative + dative + infinitive. "
          "Можно asks permission (можно войти?) and can grant it (можно, конечно). Нельзя "
          "is the refusal, and it is absolute — a guard says нельзя, not пожалуйста, нет. "
          "There is no word for 'please' inside the verb: пожалуйста comes at the end or "
          "after the first word.",
          [X("Помогите мне, пожалуйста, найти гостиницу.", "pah-mah-GEE-teh mnyeh, pah-ZHAH-loo-stah, nigh-TEE gahs-TEE-nee-tsoo.", "Help me find the hotel, please."),
           X("Можно войти? — Да, конечно.", "MOHZH-nah vah-YTEE? — dah, kah-NYESH-nah.", "May I come in? — Yes, of course."),
           X("Здесь занято? — Нет, свободно.", "zdyehsy ZAH-nyah-tah? — nyeht, svah-BOHD-nah.", "Is this seat taken? — No, it's free.")],
          [("Помогите меня, пожалуйста.", "Помогите мне, пожалуйста.", "Помочь takes the dative: мне."),
           ("Можно вы не курите здесь.", "Здесь нельзя курить.", "A ban is нельзя + imperfective infinitive.")]),
        [D("Гость", "Извините, можно вопрос?", "eez-vee-NEE-teh, MOHZH-nah vah-PROHS?", "Excuse me, may I ask a question?"),
         D("Администратор", "Конечно.", "kah-NYESH-nah.", "Of course."),
         D("Гость", "Помогите мне, пожалуйста, вызвать такси.", "pah-mah-GEE-teh mnyeh, pah-ZHAH-loo-stah, VIHZ-vahty tahk-SEE.", "Help me call a taxi, please."),
         D("Администратор", "Минуту. Вот номер: 3-1-2.", "mee-NOO-too. voht NOH-meer: tree-ahd-EEN-DVAH.", "One moment. Here is the number: 3-1-2.")],
        WS("Requests worksheet", [
            T("Ask politely.", ["help me find the hotel, please", "may I come in?"],
              ["Помогите мне найти гостиницу, пожалуйста", "Можно войти?"]),
            T("Answer about the seat.", ["is this seat taken?", "no, it's free"],
              ["Здесь занято?", "Нет, свободно"]),
        ]))),
    ("B1-U3", "B1-U3-L3", L("Отпуск: планы и сравнение",
        "Comparatives are short and irregular: дешевле (cheaper), дороже (more expensive), "
        "лучше (better), хуже (worse), ближе (closer). A comparison takes чем or the "
        "genitive: море дороже, чем горы; море дороже гор. Plans for the holidays use "
        "поеду / поедем or собираюсь + infinitive.",
        [V("отпуск", "OHt-poosk", "holiday, leave", "noun"),
         V("море", "MOH-ryeh", "sea", "noun"),
         V("гора", "gah-RAH", "mountain", "noun"),
         V("дешевле", "deh-SHEHV-lyeh", "cheaper", "comparative"),
         V("собираться", "sah-bee-RAHT-syah", "to intend, to be about to", "verb")],
        G("Сравнение и планы",
          "дешевле / дороже + чем · собираюсь + infinitive · поедем на море",
          "The comparative does not take более: говорят дешевле, not более дешёвый. The "
          "second half of the comparison is either чем + nominative or the genitive alone: "
          "поезд дешевле, чем самолёт = поезд дешевле самолёта. Собираться + infinitive "
          "expresses an intention, and поедем is the first person plural of a settled plan.",
          [X("Поезд дешевле, чем самолёт.", "POH-yehzd deh-SHEHV-lyeh, chem sah-mah-LYOHT.", "The train is cheaper than the plane."),
           X("Летом море дороже гор.", "LYEH-tahm MOH-ryeh dah-ROH-zheh gohr.", "In summer the sea is more expensive than the mountains."),
           X("Мы собираемся поехать на море в июле.", "mih sah-bee-RAH-yehm-syah pah-YEH-khahty nah MOH-ryeh v ee-YOO-leh.", "We intend to go to the sea in July.")],
          [("Море более дорогое, чем горы.", "Море дороже, чем горы.", "The simple comparative дороже; более belongs to the adjective дорогой."),
           ("Я собираюсь поеду в отпуск.", "Я собираюсь поехать в отпуск.", "Собираться takes the infinitive.")]),
        [D("Анна", "Куда вы поедете в отпуск?", "koo-DAH vih pah-YEH-deh-teh v OHT-poosk?", "Where will you go on holiday?"),
         D("Иван", "Собираемся на море, но решаем: море или горы.", "sah-bee-RAH-yehm-syah nah MOH-ryeh, noh ree-SHAH-yehm: MOH-ryeh EE-lee GOH-rih.", "We're planning the sea, but deciding: sea or mountains."),
         D("Анна", "Горы дешевле.", "GOH-rih deh-SHEHV-lyeh.", "The mountains are cheaper."),
         D("Иван", "Согласен, но до гор дольше ехать.", "sah-GLAH-sehn, noh dah gohr DOHL-sheh YEH-khahty.", "Agreed, but it takes longer to get to the mountains.")],
        WS("Holiday worksheet", [
            T("Compare.", ["the train is cheaper than the plane", "in summer the sea is more expensive than the mountains"],
              ["Поезд дешевле, чем самолёт", "Летом море дороже гор"]),
            T("State the plan.", ["we intend to go to the sea in July", "sea or mountains?"],
              ["Мы собираемся поехать на море в июле", "Море или горы?"]),
        ]))),
]

THIRD["B2"] = [
    ("B2-U1", "B2-U1-L3", L("Кем быть: профессия и инструмент",
        "The instrumental answers кем? and чем? — with what and as what. Стать + "
        "instrumental says what someone became (он стал врачом), работать + instrumental "
        "says what someone works as, and пользоваться + instrumental says what they use. "
        "The same case covers transport: ехать автобусом and на автобусе are both correct, "
        "the first more bookish.",
        [V("профессия", "prah-FYEH-see-yah", "profession", "noun"),
         V("стать", "stahty", "to become", "verb"),
         V("пользоваться", "POHL-zah-vaht-syah", "to use", "verb"),
         V("инструмент", "een-stroo-MYEHNT", "tool, instrument", "noun"),
         V("опытный", "ah-PIHT-nihy", "experienced", "adjective")],
        G("Кем? Чем? Творительный падеж",
          "стать + instrumental · работать + instrumental · пользоваться + instrumental",
          "Он стал инженером — стать takes the instrumental for the new role. Работать "
          "врачом is the same case, and it is the fuller alternative to я врач. "
          "Пользоваться takes the instrumental for the thing used: пользоваться "
          "словарём, пользоваться метро. The instrumental also marks the means: писать "
          "ручкой, ехать поездом.",
          [X("Он стал опытным инженером.", "ohn stahl OH-piht-nihm een-zheh-NYEH-rahm.", "He became an experienced engineer."),
           X("Она работает врачом в большой клинике.", "ah-NAH rah-BOH-tah-yeht vrah-CHOHM v bahl-SHOY KLEE-nee-kyeh.", "She works as a doctor in a big clinic."),
           X("Я пользуюсь словарём каждый день.", "yah POHL-zoo-yoosy slah-vah-RYOHM KAHZH-dihy dyen.", "I use the dictionary every day.")],
          [("Он стал инженер.", "Он стал инженером.", "Стать takes the instrumental."),
           ("Я пользуюсь словарь.", "Я пользуюсь словарём.", "Пользоваться takes the instrumental.")]),
        [D("Анна", "Кем вы работаете?", "kyehm vih rah-BOH-tah-yeh-teh?", "What do you work as?"),
         D("Иван", "Инженером. Начинал мастером, потом стал инженером.", "een-zheh-NYEH-rahm. nah-chee-NAHL MAHS-teh-rahm, pah-TOHM stahl een-zheh-NYEH-rahm.", "As an engineer. I started as a foreman, then became an engineer."),
         D("Анна", "Чем пользуетесь в работе?", "chem POHL-zoo-yeh-teh-syah v rah-BOH-tyeh?", "What do you use at work?"),
         D("Иван", "Чертежами и программой. Ручкой почти не пишу.", "cheer-teh-ZHAH-mee ee prah-GRAH-mah-yoo. ROOCH-koy pahch-TEE neh pee-SHOO.", "Drawings and software. I hardly write with a pen.")],
        WS("Instrumental worksheet", [
            T("Say what someone became or works as.", ["he became an experienced engineer", "she works as a doctor in a big clinic"],
              ["Он стал опытным инженером", "Она работает врачом в большой клинике"]),
            T("Say what you use.", ["I use the dictionary every day", "drawings and software"],
              ["Я пользуюсь словарём каждый день", "чертежами и программой"]),
        ]))),
    ("B2-U2", "B2-U2-L3", L("Письмо с аргументом: за и против",
        "A written argument in Russian names its parts: с одной стороны … с другой стороны, "
        "во-первых … во-вторых, следовательно, однако, тем не менее. Преимущество and "
        "недостаток are the two halves of a judgement, and вывод closes it. The register is "
        "formal, so the sentences stay long and the verbs nominal: это приводит к…",
        [V("аргумент", "ahr-goo-MYEHNT", "argument", "noun"),
         V("довод", "DOH-vaht", "reason, point", "noun"),
         V("преимущество", "pree-EEM-oo-shcheh-stvah", "advantage", "noun"),
         V("недостаток", "nee-dah-STAH-tahk", "shortcoming", "noun"),
         V("вывод", "VIH-vaht", "conclusion", "noun")],
        G("Аргумент за и против",
          "с одной стороны … с другой стороны · во-первых · следовательно · тем не менее",
          "С одной стороны and с другой стороны open the two halves without taking sides "
          "yet. Во-первых starts an enumeration the reader can follow, and следовательно or "
          "таким образом draws the conclusion. However is однако (bookish) and тем не менее "
          "(conceding): довод верный, тем не менее вывод спорный. Вывод states what follows, "
          "not what you wish followed.",
          [X("С одной стороны, это дешевле; с другой стороны, дольше.", "s ahd-NOY stah-rah-NIH, EH-tah deh-SHEHV-lyeh; s droo-GOY stah-rah-NIH, DOHL-sheh.", "On one hand it is cheaper; on the other, it takes longer."),
           X("Во-первых, довод не подтверждён; во-вторых, он не относится к делу.", "vah-PYER-vihkh, DOH-vaht nee paht-vehrzh-DYOHN; vah-ftah-RIHKH, ohn nee aht-NOH-seet-syah k DYEH-loo.", "First, the point is unconfirmed; second, it is irrelevant."),
           X("Тем не менее вывод остаётся спорным.", "tyehm nee MYEH-nee-yeh VIH-vaht ah-stah-YOHT-syah SPOHR-nihm.", "Nevertheless, the conclusion remains debatable.")],
          [("С одной стороны, это дешевле, а с другой стороны дороже.", "С одной стороны, это дешевле; с другой стороны, дольше.", "The two halves must be different criteria, not a contradiction."),
           ("Во-первых, довод, во-вторых, пример, в-третьих, вывод, и всё.", "Во-первых, довод не подтверждён; во-вторых, он не относится к делу.", "Each item of an enumeration needs its own predicate.")]),
        [D("Редактор", "Где здесь вывод?", "gdyeh zdyehsy VIH-vaht?", "Where is the conclusion here?"),
         D("Автор", "В конце: «Следовательно, решение преждевременно».", "v kahn-TSYEH: sleh-DAH-vaht-yehl-nah, reh-SHEH-nee-yeh preezh-deh-VRYEH-meh-nah.", "At the end: 'Consequently, the decision is premature.'"),
         D("Редактор", "А недостатки названы?", "ah nee-dah-STAHt-kee NAHZ-vah-nih?", "And are the shortcomings named?"),
         D("Автор", "Только один. Во-вторых пункт я уберу — он не довод, а эмоция.", "TOHL-kah ah-DEEN. vah-ftah-RIHKH poonkt yah oo-bee-ROO — ohn nee DOH-vaht, ah eh-MOH-tsee-yah.", "Only one. I'll cut the second point — it is emotion, not an argument.")],
        WS("Argument worksheet", [
            T("Open both sides.", ["on one hand it is cheaper; on the other, it takes longer", "first, the point is unconfirmed"],
              ["С одной стороны, это дешевле; с другой стороны, дольше", "Во-первых, довод не подтверждён"]),
            T("Conclude.", ["consequently, the decision is premature", "nevertheless, the conclusion remains debatable"],
              ["Следовательно, решение преждевременно", "Тем не менее вывод остаётся спорным"]),
        ]))),
    ("B2-U3", "B2-U3-L3", L("Книга и фильм: экранизация",
        "A film made from a book is экранизация, and the argument about it uses four words: "
        "сюжет (plot), герой, режиссёр and сценарий. Снять фильм по книге is the verb — по + "
        "dative. The judgement is made with удачная / неудачная экранизация and the reason is "
        "given with потому что or благодаря + dative.",
        [V("роман", "rah-MAHN", "novel", "noun"),
         V("экранизация", "ehk-rah-nee-ZAH-tsee-yah", "film adaptation", "noun"),
         V("режиссёр", "ree-zhee-SYOHR", "director", "noun"),
         V("сюжет", "syoo-ZHEHT", "plot", "noun"),
         V("герой", "gee-ROY", "hero, character", "noun")],
        G("Экранизация: по книге или про книгу",
          "экранизация + genitive · снять фильм по + dative · удачная, потому что …",
          "Экранизация романа — the book stands in the genitive. Снять фильм по роману "
          "names the source with по + dative. Благодаря + dative gives a positive cause and "
          "из-за + genitive a negative one: благодаря актёрам, из-за сценария. The "
          "comparison with the book is made with по сравнению с + instrumental.",
          [X("Это удачная экранизация романа.", "EH-tah oo-DAHCH-nah-yah ehk-rah-nee-ZAH-tsee-yah rah-MAH-nah.", "This is a successful adaptation of the novel."),
           X("Фильм снят по книге, но сюжет изменён.", "FEELM snyaht pah KNEE-geh, noh syoo-ZHEHT eez-mee-NYOHN.", "The film is made from the book, but the plot is changed."),
           X("По сравнению с книгой, герой мягче.", "pah srahv-NYEH-nee-yoo s KNEE-goy, gee-ROY MYAHKH-cheh.", "Compared with the book, the character is softer.")],
          [("Это экранизация по роману.", "Это экранизация романа.", "Экранизация takes the genitive: романа."),
           ("Благодаря плохого сценария фильм скучный.", "Из-за плохого сценария фильм скучный.", "A negative cause takes из-за + genitive; благодаря is only for the good.")]),
        [D("Анна", "Ты видел новую экранизацию?", "tih VEE-dehl NOH-voo-yoo ehk-rah-nee-ZAH-tsee-yoo?", "Have you seen the new adaptation?"),
         D("Иван", "Видел. Удачная, хотя сюжет изменён.", "VEE-dehl. oo-DAHCH-nah-yah, khah-TYAH syoo-ZHEHT eez-mee-NYOHN.", "I have. Successful, although the plot is changed."),
         D("Анна", "А герои?", "ah gee-ROH-ee?", "And the characters?"),
         D("Иван", "По сравнению с книгой они мягче, и это благодаря актёрам.", "pah srahv-NYEH-nee-yoo s KNEE-goy ah-NEE MYAHKH-cheh, ee EH-tah blah-gah-dah-RYAH ahk-TYOH-rahm.", "Compared with the book they are softer, and that is thanks to the actors.")],
        WS("Adaptation worksheet", [
            T("Describe the film.", ["this is a successful adaptation of the novel", "the film is made from the book"],
              ["Это удачная экранизация романа", "Фильм снят по книге"]),
            T("Attribute the reason.", ["compared with the book, the character is softer", "because of the script the film is dull"],
              ["По сравнению с книгой герой мягче", "Из-за сценария фильм скучный"]),
        ]))),
]

THIRD["C1"] = [
    ("ru-c1-u1", "ru-c1-l7", L("Официальное письмо: заявление и справка",
        "Official Russian runs on a small set of documents: заявление (application), "
        "справка (certificate), ходатайство (formal request for someone else), уведомление "
        "(notice). The application is written in one sentence — прошу + infinitive — under a "
        "fixed right-aligned block for the addressee, and every document ends with дата and "
        "подпись. Канцелярит is the name for the style when it thickens into emptiness.",
        [V("заявление", "zah-yahv-LYEH-nee-yeh", "application, written request", "noun"),
         V("справка", "SPRAHF-kah", "certificate, reference", "noun"),
         V("обратиться", "ahb-rah-TEET-syah", "to address, to apply", "verb"),
         V("подтвердить", "paht-vehr-DEETY", "to confirm", "verb"),
         V("прилагать", "pree-lah-GAHTY", "to enclose, to attach", "verb")],
        G("Как пишется заявление",
          "кому: (dative) · прошу + infinitive · прилагаю + accusative · дата, подпись",
          "The addressee stands in the dative at the top right: директору школы Ивановой "
          "А. И. The body is one request in the first person — прошу предоставить, прошу "
          "рассмотреть — and a list of what is enclosed follows with прилагаю: копия "
          "паспорта, справка с работы. Заявление is written by the person who wants "
          "something; ходатайство is written by a third party on their behalf.",
          [X("Прошу предоставить отпуск с 1 по 14 июля.", "prah-SHOO preh-dah-STAH-veety OHT-poosk s PYER-vah-vah pah cheh-TIHR-nahd-tsah-tah-YOO-lyah.", "I request leave from 1 to 14 July."),
           X("Прилагаю копию паспорта и справку с работы.", "pree-lah-GAH-yoo KOH-pee-yoo PAHS-pahr-tah ee SPRAHF-koo s rah-BOH-tih.", "I enclose a copy of my passport and a certificate from work."),
           X("Прошу подтвердить, что документы приняты.", "prah-SHOO paht-vehr-DEETY, shtoh dah-koo-MYEHN-tih PREH-nyah-tih.", "I ask you to confirm that the documents have been accepted.")],
          [("Директор школы, заявление от Ивановой.", "Директору школы, заявление от Ивановой.", "The addressee stands in the dative."),
           ("Прошу я предоставить отпуск.", "Прошу предоставить отпуск.", "The subject is already in прошу; я is not written.")]),
        [D("Секретарь", "Вы уже написали заявление?", "vih oo-ZHEH nah-pee-SAH-lee zah-yahv-LYEH-nee-yeh?", "Have you written the application yet?"),
         D("Сотрудник", "Пишу. Кому — директору?", "pee-SHOO. kah-MOO — dee-RYEHk-tah-roo?", "I'm writing it. To whom — the director?"),
         D("Секретарь", "Директору, в дательном. И приложите справку.", "dee-RYEHk-tah-roo, v DAH-tehl-nahm. ee pree-lah-ZHEE-teh SPRAHF-koo.", "To the director, in the dative. And enclose the certificate."),
         D("Сотрудник", "Хорошо. Дата, подпись — и готово.", "khah-rah-SHOH. DAH-tah, POHD-peesy — ee gah-TOH-vah.", "All right. Date, signature — and it's done.")],
        WS("Official letter worksheet", [
            T("Write the request.", ["I request leave from 1 to 14 July", "I ask you to confirm that the documents have been accepted"],
              ["Прошу предоставить отпуск с 1 по 14 июля", "Прошу подтвердить, что документы приняты"]),
            T("Name what is enclosed.", ["I enclose a copy of my passport and a certificate", "date and signature"],
              ["Прилагаю копию паспорта и справку", "дата и подпись"]),
        ]))),
    ("ru-c1-u2", "ru-c1-l8", L("Экспертное заключение: оценка и оговорка",
        "An expert assessment has a shape: предмет оценки, критерии, наблюдения, оговорка, "
        "вывод. The impersonal constructions carry the weight — установлено, выявлено, "
        "представляется целесообразным — and the assessment is hedged with при условии, что, "
        "с учётом того, что, за исключением. Оговорка is not a weakness; it is what makes the "
        "conclusion usable.",
        [V("заключение", "zahk-lyoo-CHYEH-nee-yeh", "assessment, conclusion", "noun"),
         V("критерий", "kree-TEH-reey", "criterion", "noun"),
         V("оговорка", "ah-gah-VOHR-kah", "caveat, reservation", "noun"),
         V("обосновать", "ah-bahs-nah-VAHTY", "to substantiate", "verb"),
         V("выявленный", "VIH-yahv-lehn-nihy", "identified, revealed", "participle")],
        G("Заключение: оценка с оговоркой",
          "установлено, что · при условии, что · за исключением + genitive · представляется целесообразным",
          "Установлено, что and выявлено, что report findings with no author — the expert "
          "steps aside. При условии, что and с учётом того, что state what the conclusion "
          "depends on. За исключением + genitive names what the assessment does not cover, "
          "and представляется целесообразным recommends without commanding. A conclusion "
          "with no оговорка is a claim, not an expert judgement.",
          [X("Установлено, что методика соответствует критериям.", "oo-stah-NOHV-leh-nah, shtoh mee-THOH-dee-kah sah-aht-VYEHT-stvooy-eet kree-TEH-reey-yahm.", "It has been established that the method meets the criteria."),
           X("За исключением двух случаев, данные однородны.", "zah ees-klyoo-CHEH-nee-yem DVOOKH SLOO-chah-yef, DAHN-nih-yeh ahd-nah-ROHD-nih.", "With the exception of two cases, the data are homogeneous."),
           X("Представляется целесообразным продлить срок при условии, что отчёт будет обновлён.", "preet-stahv-LYAH-yeht-syah tseh-leh-sah-ahb-RAHZ-nihm prahd-LEETY srohk pree oo-SLOH-vee-yeh, shtoh aht-CHOHT BOO-deht ahb-nahv-LYOHN.", "It would seem advisable to extend the term provided that the report is updated.")],
          [("Я установил, что методика соответствует.", "Установлено, что методика соответствует.", "An expert assessment uses the impersonal form: установлено."),
           ("За исключением двух случаев, где данные разные.", "За исключением двух случаев, данные однородны.", "За исключением is followed by the main clause, not by a relative one.")]),
        [D("Заказчик", "Заключение положительное?", "zahk-lyoo-CHYEH-nee-yeh pah-lah-ZHEE-tehl-nah-yeh?", "Is the assessment positive?"),
         D("Эксперт", "Установлено, что методика соответствует критериям.", "oo-stah-NOHV-leh-nah, shtoh mee-THOH-dee-kah sah-aht-VYET-stvooy-eet kree-TEH-reey-yahm.", "It has been established that the method meets the criteria."),
         D("Заказчик", "А оговорка есть?", "ah ah-gah-VOHR-kah yehsty?", "And is there a caveat?"),
         D("Эксперт", "Есть: за исключением двух случаев, и именно её нельзя убирать.", "yehsty: zah ees-klyoo-CHEH-nee-yem DVOOKH SLOO-chah-yef, ee EE-mehn-nah yeyoh nehl-ZYAH oo-bee-RAHTY.", "There is: with the exception of two cases, and that is exactly what cannot be removed.")],
        WS("Assessment worksheet", [
            T("Report the finding impersonally.", ["it has been established that the method meets the criteria", "with the exception of two cases, the data are homogeneous"],
              ["Установлено, что методика соответствует критериям", "За исключением двух случаев, данные однородны"]),
            T("Hedge the recommendation.", ["it would seem advisable to extend the term provided that the report is updated", "the caveat cannot be removed"],
              ["Представляется целесообразным продлить срок при условии, что отчёт будет обновлён", "Оговорку нельзя убирать"]),
        ]))),
    ("ru-c1-u3", "ru-c1-l9", L("Перевод реалий: дача, душа, тоска",
        "Some Russian words resist a one-word translation because they name a practice, not a "
        "concept: дача, душа, тоска, интеллигенция, пошлость. A translator works with "
        "соответствие (an equivalent), оттенок (a shade of meaning) and контекст: дача "
        "becomes 'country house' in a contract, 'dacha' in a novel, and a descriptive clause "
        "in an essay. Непереводимое is a claim about the dictionary, not about the language.",
        [V("реалия", "ree-AH-lee-yah", "realia, culture-specific item", "noun"),
         V("соответствие", "sah-aht-VYEHT-stvee-yeh", "equivalent, correspondence", "noun"),
         V("оттенок", "aht-TYEH-nahk", "shade, nuance", "noun"),
         V("передать", "pee-ree-DAHTY", "to convey, to render", "verb"),
         V("контекст", "kahn-TYEHkst", "context", "noun")],
        G("Что делать с реалией",
          "подобрать соответствие · передать оттенок · оставить без перевода + пояснение",
          "Three strategies, chosen by genre. Подобрать соответствие replaces the item: "
          "щи — 'cabbage soup'. Передать оттенок keeps the flavour with a calque or a "
          "borrowing: интеллигенция — 'the intelligentsia'. Оставить без перевода и дать "
          "пояснение is the translator's last resort and the essayist's first: дача (a "
          "summer cottage with a garden). The choice is defended by context, not by "
          "dictionary equivalence.",
          [X("В романе дача — это место, а в договоре — объект.", "v rah-MAH-nyeh DAH-chah — EH-tah MYEH-stah, ah v dah-gah-VOH-ryeh — ahb-YEHkt.", "In a novel the dacha is a place, in a contract it is an object."),
           X("Здесь нельзя подобрать соответствие: слово работает как термин.", "zdyehsy nehl-ZYAH pahd-ah-BRAHTY sah-aht-VYEHT-stvee-yeh: SLOH-vah rah-BOH-tah-yeht kahk TEHR-meen.", "No equivalent can be found here: the word works as a term."),
           X("Переводчик передал оттенок, а не букву.", "pee-ree-VOHD-cheek pee-ree-DAHL aht-TYEH-nahk, ah nee BOOK-voo.", "The translator conveyed the shade, not the letter.")],
          [("Это слово непереводимо, поэтому перевода нет.", "Это слово непереводимо, поэтому нужен описательный оборот.", "A claim of untranslatability is answered by description, not by silence."),
           ("Переводчик дал буквальный перевод, и текст стал чужим.", "Переводчик передал оттенок, сохранив контекст.", "Literal rendering is one strategy; the essay needs the shade preserved.")]),
        [D("Редактор", "Как вы перевели «тоску»?", "kahk vih pee-ree-veh-LEE tahs-KOO?", "How did you translate 'toska'?"),
         D("Переводчик", "Описательно: 'a dull ache of the soul'.", "ahp-ee-SAH-tehl-nah: eh dool ayk ahv thah sohl.", "Descriptively: 'a dull ache of the soul'."),
         D("Редактор", "А почему не оставили слово?", "ah pah-cheh-MOO nee ah-stah-VEE-lee SLOH-vah?", "And why didn't you leave the word?"),
         D("Переводчик", "Контекст — эссе, а не роман. Здесь пояснение работает лучше.", "kahn-TYEHkst — eh-SEH, ah nee rah-MAHN. zdyehsy pah-yes-NYEH-nee-yeh rah-BOH-tah-yeht LOOT-sheh.", "The context is an essay, not a novel. Here the explanation works better.")],
        WS("Translation worksheet", [
            T("Choose the strategy.", ["in a novel the dacha is a place, in a contract it is an object", "the translator conveyed the shade, not the letter"],
              ["В романе дача — это место, а в договоре — объект", "Переводчик передал оттенок, а не букву"]),
            T("Explain the choice.", ["no equivalent can be found here", "the word works as a term"],
              ["Здесь нельзя подобрать соответствие", "Слово работает как термин"]),
        ]))),
]

THIRD["C2"] = [
    ("ru-c2-u1", "ru-c2-l7", L("Порядок слов и рема: что читатель уже знает",
        "Russian word order is not free — it is information structure. The theme (тема) opens "
        "the sentence and the new element (рема) closes it: Отец приехал вчера answers "
        "'when?', Вчера приехал отец answers 'who?'. Inversion, the particles именно, как раз "
        "and даже, and the existential sentence with есть shift the rheme without adding a "
        "single new word. Dense prose is read by watching where the sentence lands, not by "
        "parsing its cases.",
        [V("рема", "RYEH-mah", "rheme, the new element", "noun"),
         V("тема", "TYEH-mah", "theme, the given element", "noun"),
         V("инверсия", "een-VYER-see-yah", "inversion", "noun"),
         V("выделение", "vih-deh-LYEH-nee-yeh", "highlighting, emphasis", "noun"),
         V("как раз", "kahk RAHS", "exactly, precisely", "phrase")],
        G("Где рема, там и смысл",
          "тема в начале · рема в конце · именно / как раз / даже · есть + nominative",
          "The final position is the stressed one: Он купил машину и Машину купил он differ "
          "only in what is being answered. Именно and как раз point at the rheme directly "
          "(именно вчера), while даже adds a scale (даже отец приехал). An existential "
          "sentence puts its theme in the accusative and its rheme after есть: У нас есть "
          "время. When a sentence sounds wrong, move it rather than rewrite it.",
          [X("Именно эти данные изменили вывод.", "EE-mehn-nah EH-tee DAHN-nih-yeh eez-mee-NEE-lee VIH-vaht.", "It was precisely this data that changed the conclusion."),
           X("Вчера приехал отец, а сегодня — сестра.", "fcheh-RAH pree-YEH-khahl ah-TYETS, ah see-VOHD-nyah — sees-TRAH.", "Yesterday my father arrived, and today my sister."),
           X("У нас есть время, но нет тишины.", "oo nahs yehsty VRYEH-myah, noh nyeht teesh-IH-nih.", "We have time, but no quiet.")],
          [("Он именно купил машину вчера.", "Именно он купил машину вчера. / Он купил машину именно вчера.", "Именно stands next to the element it highlights."),
           ("Вчера отец приехал, сегодня сестра приехала — и всё.", "Вчера приехал отец, а сегодня — сестра.", "The parallel halves need a parallel order and a conjunction.")]),
        [D("Редактор", "Почему эта фраза звучит тяжело?", "pah-cheh-MOO EH-tah FRAH-zah zvoo-CHEET teezh-eh-LOH?", "Why does this sentence sound heavy?"),
         D("Автор", "Рема в начале. Перенесу её в конец.", "RYEH-mah v nah-CHAH-leh. pee-ree-nee-SOO yeyoh v kah-NYETS.", "The rheme is at the beginning. I'll move it to the end."),
         D("Редактор", "И уберите «именно» — оно не нужно.", "ee oo-bee-REE-teh EE-mehn-nah — ah-NOH nee NOOZH-nah.", "And remove 'именно' — it isn't needed."),
         D("Автор", "Согласен. Инверсия сделает работу лучше, чем частица.", "sah-GLAH-sehn. een-VYER-see-yah SDYEH-lah-yeht rah-BOH-too LOOT-sheh, chem chahs-TEE-tsah.", "Agreed. Inversion will do the work better than a particle.")],
        WS("Word order worksheet", [
            T("Move the rheme.", ["it was precisely this data that changed the conclusion", "yesterday my father arrived, and today my sister"],
              ["Именно эти данные изменили вывод", "Вчера приехал отец, а сегодня — сестра"]),
            T("Use the existential sentence.", ["we have time, but no quiet", "the rheme is at the beginning"],
              ["У нас есть время, но нет тишины", "Рема в начале"]),
        ]))),
    ("ru-c2-u2", "ru-c2-l8", L("От литературного к официальному: переписывание",
        "Rewriting across registers is measured, not improvised. A literary sentence keeps "
        "its metaphor and its rhythm; the official version states the fact, its agent and its "
        "consequence, and turns verbs into nouns — канцелярит appears when the nouns no longer "
        "carry anything. The honest rewrite names what it lost: образ, оттенок, интонация. "
        "Эквивалент and сжатие are the two words a rewriter works with.",
        [V("перефраз", "pee-ree-FRAHS", "rephrasing", "noun"),
         V("регистр", "ree-GEESTR", "register", "noun"),
         V("канцелярит", "kahn-tsih-lee-REET", "officialese, bureaucratic style", "noun"),
         V("сжатие", "ZHAH-tee-yeh", "compression", "noun"),
         V("эквивалент", "ehk-vee-vah-LYEHNT", "equivalent", "noun")],
        G("Переписать, не потеряв смысла",
          "сохранить содержание · сменить регистр · назвать потери · избежать канцелярита",
          "The rewrite keeps the content and changes the packaging: образ becomes a stated "
          "fact, an emotional verb becomes a neutral one, and the agent is named or removed "
          "on purpose. Канцелярит is diagnosed by the chain of verbal nouns with no subject "
          "(осуществление мероприятий по улучшению). A сжатие is honest when the reader can "
          "still reconstruct the claim; it is dishonest when it hides a hedge.",
          [X("Образ заменён фактом, содержание сохранено.", "OH-brahz zah-mee-NYOHN FAHK-tahm, sah-dehr-ZHAH-nee-yeh sah-khrah-NYEH-nah.", "The image is replaced by a fact, the content preserved."),
           X("Канцелярит начинается там, где отглагольные существительные не несут смысла.", "kahn-tsih-lee-REET nah-chee-NAH-yeht-syah tahm, gdyeh aht-glah-GOHL-nih-yeh soo-shcheh-STVEE-tehl-nih-yeh nee nee-SOOT SMIH-slah.", "Officialese begins where verbal nouns carry no meaning."),
           X("Сжатие допустимо, если оговорка не спрятана.", "ZHAH-tee-yeh dah-poo-STEE-mah, YEH-slee ah-gah-VOHR-kah nee SPYAH-tah-nah.", "Compression is acceptable if the caveat is not hidden.")],
          [("Осуществление мероприятий по улучшению ситуации продолжается.", "Мы продолжаем улучшать ситуацию.", "Name the agent and use the verb; the noun chain says nothing."),
           ("Мы убрали оговорку, чтобы текст был короче.", "Мы сократили текст, сохранив оговорку.", "Compression must not remove the hedge.")]),
        [D("Редактор", "Второй абзац можно сократить?", "ftah-ROY ahb-ZAHTS MOHZH-nah sah-krah-TEETY?", "Can the second paragraph be shortened?"),
         D("Автор", "Можно, но оговорку я оставлю.", "MOHZH-nah, noh ah-gah-VOHR-koo yah ah-STAHV-lyoo.", "Yes, but I'll keep the caveat."),
         D("Редактор", "Хорошо. И уберите канцелярит в третьем.", "khah-rah-SHOH. ee oo-bee-REE-teh kahn-tsih-lee-REET v TRYEHty-yem.", "Good. And remove the officialese in the third."),
         D("Автор", "Согласен: три отглагольных существительных подряд — это уже не стиль, а шум.", "sah-GLAH-sehn: tree aht-glah-GOHL-nihkh soo-shcheh-STVEE-tehl-nihkh PAHD-ryaht — EH-tah oo-ZHEH nee STEEL, ah SHOOM.", "Agreed: three verbal nouns in a row is noise, not style.")],
        WS("Rewrite worksheet", [
            T("State the principle.", ["the image is replaced by a fact, the content preserved", "compression is acceptable if the caveat is not hidden"],
              ["Образ заменён фактом, содержание сохранено", "Сжатие допустимо, если оговорка не спрятана"]),
            T("Repair the officialese.", ["we continue to improve the situation", "we shortened the text, keeping the caveat"],
              ["Мы продолжаем улучшать ситуацию", "Мы сократили текст, сохранив оговорку"]),
        ]))),
    ("ru-c2-u3", "ru-c2-l9", L("Публичная речь: риторика и убеждение",
        "A Russian public speech builds on триады — three-part lists — and on the repetition of "
        "one structural word: «Мы не боимся работы. Мы не боимся ответственности. Мы боимся "
        "равнодушия». Тезис opens, повтор reinforces, обращение reaches the audience "
        "directly, and the close returns to the thesis with one sentence short enough to "
        "remember. Убедительность comes from the structure being visible, not from volume.",
        [V("риторика", "ree-TOR-ee-kah", "rhetoric", "noun"),
         V("тезис", "TYEH-zees", "thesis", "noun"),
         V("повтор", "pahf-TOHR", "repetition", "noun"),
         V("обращение", "ahb-rah-SHCHYEH-nee-yeh", "address to the audience", "noun"),
         V("убедительность", "oo-bee-DEE-tehl-nahsty", "persuasiveness", "noun")],
        G("Как строится убедительная речь",
          "тезис → триада → повтор → обращение → короткий финал",
          "The thesis is one sentence and comes first: Нам нужна не скорость, а точность. A "
          "triad lists three items of the same shape, and the repetition of one structural "
          "word makes the shape audible. Обращение names the audience (коллеги, друзья) and "
          "belongs at the beginning or the end, never in the middle. The close is the first "
          "sentence said again, shorter.",
          [X("Нам нужна не скорость, а точность.", "nahm noozh-NAH nee SKOH-rahsty, ah TOHCH-nahsty.", "What we need is not speed but precision."),
           X("Мы не боимся работы. Мы не боимся ответственности. Мы боимся равнодушия.", "mih nee bah-EEM-syah rah-BOH-tih. mih nee bah-EEM-syah aht-VYEHT-stveh-nah-stee. mih bah-EEM-syah rahv-nah-DOO-shee-yah.", "We are not afraid of work. We are not afraid of responsibility. We are afraid of indifference."),
           X("Коллеги, начнём с того, что нас объединяет.", "kahL-YEH-ghee, nahch-NYOEM s tah-VOH, shtoh nahs ahb-yeh-dee-NYAH-yeht.", "Colleagues, let us start with what unites us.")],
          [("Нам нужна скорость, но и точность, и ещё гибкость, и, конечно, время.", "Нам нужна не скорость, а точность.", "A thesis is one contrast, not a list of four."),
           ("Я обращаюсь к вам, коллеги, и говорю, что мы не боимся.", "Коллеги, мы не боимся работы.", "Обращение stands at the edge of the sentence, not in the middle.")]),
        [D("Оратор", "Коллеги, начнём с главного.", "kahL-YEH-ghee, nahch-NYOHM s GLAHV-nah-vah.", "Colleagues, let us start with the main thing."),
         D("Коллега", "И с чего именно?", "ee s cheh-VOH EE-mehn-nah?", "And with what exactly?"),
         D("Оратор", "Нам нужна не скорость, а точность. Это тезис, и к нему я вернусь в конце.", "nahm noozh-NAH nee SKOH-rahsty, ah TOHCH-nahsty. EH-tah TYEH-zees, ee k neh-MOO yah vehr-NOOSY v kahn-TSYEH.", "What we need is not speed but precision. That is the thesis, and I will return to it at the end."),
         D("Коллега", "А примеры будут?", "ah pree-MYEH-rih BOO-doot?", "And will there be examples?"),
         D("Оратор", "Три, одной формы — так их запомнят.", "tree, ahd-NOY FOHR-mih — tahk eekh zah-POHM-nyat.", "Three, of one shape — that way they will be remembered.")],
        WS("Speech worksheet", [
            T("Write the thesis.", ["what we need is not speed but precision", "we are not afraid of work, we are afraid of indifference"],
              ["Нам нужна не скорость, а точность", "Мы не боимся работы, мы боимся равнодушия"]),
            T("Build the frame.", ["colleagues, let us start with the main thing", "three examples, of one shape"],
              ["Коллеги, начнём с главного", "Три примера, одной формы"]),
        ]))),
]

# ── the five half-step rungs: A1+ … C1+ ────────────────────────────────────

HALFSTEPS["A1+"] = {
    "native": NATIVE,
    "title": "%s A1+ — У киоска, дома и по часам" % NAME,
    "goals": [
        "Buy something small, ask the price and pay with cash or card",
        "Give your address, describe your flat and find the door",
        "Tell the time, name the days of the week and describe your day",
    ],
    "units": [
        {"id": "A1+-U1", "title": "У киоска", "lessons": [
            L("Сколько это стоит?",
              "Prices are read out in roubles and kopecks: пятьдесят рублей, двадцать копеек. "
              "Сколько стоит? asks about one thing and сколько стоят? about several. The "
              "answer is стоит or стоят followed by the number, and рублей changes: один "
              "рубль, два рубля, пять рублей.",
              [V("киоск", "kee-OHSK", "kiosk", "noun"),
               V("цена", "tsih-NAH", "price", "noun"),
               V("рубль", "ROOBLY", "rouble", "noun"),
               V("копейка", "kah-PYEY-kah", "kopeck", "noun"),
               V("сдача", "SDAH-chah", "change (money back)", "noun")],
              G("Сколько стоит?",
                "сколько стоит + nominative sg · сколько стоят + plural · один рубль, два рубля, пять рублей",
                "Сколько стоит вода? — Сорок рублей. For several items the verb is plural: "
                "Сколько стоят яблоки? The numerals govern the noun: 1 рубль, 2–4 рубля, "
                "5 and up рублей; 21 рубль follows the last digit. The place to pay is касса, "
                "and сдача is what comes back.",
                [X("Сколько стоит вода?", "SKOHL-kah STOH-eet vah-DAH?", "How much is the water?"),
                X("Сорок пять рублей.", "SOH-rahk pyahty ROOB-lyey.", "Forty-five roubles."),
                X("Сколько стоят яблоки?", "SKOHL-kah STOH-yeht YAHB-lah-kee?", "How much are the apples?")],
                [("Сколько стоит яблоки?", "Сколько стоят яблоки?", "A plural subject takes стоят."),
                 ("Пять рубль.", "Пять рублей.", "From five upward the noun is рублей.")]),
              [D("Продавец", "Что вы хотите?", "shtoh vih khah-TEE-teh?", "What would you like?"),
               D("Покупатель", "Сколько стоит вода?", "SKOHL-kah STOH-eet vah-DAH?", "How much is the water?"),
               D("Продавец", "Сорок рублей.", "SOH-rahk ROOB-lyey.", "Forty roubles."),
               D("Покупатель", "Дайте две, пожалуйста. Вот сто рублей.", "DAH-ee-teh DVEH, pah-ZHAH-loo-stah. voht stoh ROOB-lyey.", "Give me two, please. Here is a hundred roubles.")],
              WS("Price worksheet", [
                  T("Ask the price.", ["how much is the water?", "how much are the apples?"],
                    ["Сколько стоит вода?", "Сколько стоят яблоки?"]),
                  T("Count the money.", ["one rouble", "two roubles", "five roubles"],
                    ["один рубль", "два рубля", "пять рублей"]),
              ])),
            L("У меня есть, у меня нет",
              "У меня есть + nominative says what you have; у меня нет + genitive says what "
              "you do not have: у меня нет воды, нет времени, нет сдачи. This is the one place "
              "where a whole set of words changes shape, and it is the phrase a shop runs on.",
              [V("есть", "yehsty", "there is, one has", "verb"),
               V("нет", "nyeht", "there is not, no", "word"),
               V("вода", "vah-DAH", "water", "noun"),
               V("газета", "gah-ZYEH-tah", "newspaper", "noun"),
               V("пакет", "pah-KYEHT", "bag, packet", "noun")],
              G("Есть и нет",
                "у меня есть + nominative · у меня нет + genitive · есть? — нет",
                "У меня есть вода (nominative) and У меня нет воды (genitive) are the same "
                "situation with opposite words. The pattern moves to every person: у тебя "
                "есть, у вас есть, у него нет. In a shop, есть? is the whole question: "
                "Пакет есть? — Пакета нет.",
                [X("У меня есть пакет.", "oo meh-NYAH yehsty pah-KYEHT.", "I have a bag."),
                X("У меня нет сдачи.", "oo meh-NYAH nyeht SDAH-chah.", "I don't have change."),
                X("У вас есть газеты? — Есть, но только одна.", "oo vahs yehsty gah-ZYEH-tih? — yehsty, noh TOHL-kah ahd-NAH.", "Do you have newspapers? — Yes, but only one.")],
                [("У меня нет сдача.", "У меня нет сдачи.", "Нет takes the genitive: сдачи."),
                 ("У меня есть вода — у меня есть нет воды.", "У меня есть вода — у меня нет воды.", "Есть and нет are alternatives, never both.")]),
              [D("Покупатель", "У вас есть пакет?", "oo vahs yehsty pah-KYEHT?", "Do you have a bag?"),
               D("Продавец", "Пакета нет, извините.", "pah-KYEH-tah nyeht, eez-vee-NEE-teh.", "There is no bag, sorry."),
               D("Покупатель", "У меня есть свой. А вода есть?", "oo meh-NYAH yehsty svoy. ah vah-DAH yehsty?", "I have my own. And is there water?"),
               D("Продавец", "Вода есть. Двадцать рублей.", "vah-DAH yehsty. DVAHts-tsahty ROOB-lyey.", "There is water. Twenty roubles.")],
              WS("Have and not have worksheet", [
                  T("Say what you have.", ["I have a bag", "do you have newspapers?"],
                    ["У меня есть пакет", "У вас есть газеты?"]),
                  T("Say what you don't have.", ["I don't have change", "there is no bag"],
                    ["У меня нет сдачи", "Пакета нет"]),
              ])),
            L("Плачу картой и наличными",
              "At the till Russian asks картой или наличными? Both answers are instrumentals: "
              "картой, наличными. The polite request is дайте, пожалуйста or можно + "
              "accusative. The receipt is чек, and очередь is the queue — the question whose "
              "turn it is, чья очередь?, is answered with я, а за мной — она.",
              [V("карта", "KAHR-tah", "card", "noun"),
               V("наличные", "nah-LEECH-nih-yeh", "cash", "noun"),
               V("чек", "chehk", "receipt", "noun"),
               V("касса", "KAH-sah", "checkout, till", "noun"),
               V("очередь", "OH-cheh-ryedy", "queue, turn", "noun")],
              G("На кассе",
                "картой или наличными? · можно + accusative? · чья очередь?",
                "Платить takes the instrumental for the means of payment: плачу картой, "
                "заплатил наличными. Можно чек? asks for the receipt without a verb of "
                "wanting. Чья очередь? asks whose turn it is, and the answers are я and вы. "
                "The kiosk phrase сдачи нет is not rudeness but the day's fact.",
                [X("Картой или наличными? — Картой.", "KAHR-toy EE-lee nah-LEECH-nih-mee? — KAHR-toy.", "Card or cash? — Card."),
                X("Можно чек, пожалуйста?", "MOHZH-nah chehk, pah-ZHAH-loo-stah?", "Could I have the receipt, please?"),
                X("Чья очередь? — Моя, за мной — она.", "chyah OH-cheh-ryedy? — mah-YAH, zah mnoy — ah-NAH.", "Whose turn is it? — Mine, and she is after me.")],
                [("Я платил с картой.", "Я платил картой.", "Платить takes the instrumental without a preposition."),
                 ("Можно чек есть?", "Можно чек?", "Можно + accusative is the whole request; есть is not needed.")]),
              [D("Кассир", "Картой или наличными?", "KAHR-toy EE-lee nah-LEECH-nih-mee?", "Card or cash?"),
               D("Покупатель", "Картой. И можно чек?", "KAHR-toy. ee MOHZH-nah chehk?", "Card. And could I have the receipt?"),
               D("Кассир", "Конечно. Приложите карту.", "kah-NYESH-nah. pree-lah-ZHEE-teh KAHR-too.", "Of course. Tap your card."),
               D("Покупатель", "Спасибо. Чья очередь за мной?", "spah-SEE-bah. chyah OH-cheh-ryedy zah mnoy?", "Thank you. Whose turn is after me?")],
              WS("Paying worksheet", [
                  T("Answer the till.", ["card, and could I have the receipt?", "whose turn is it?"],
                    ["Картой, и можно чек?", "Чья очередь?"]),
                  T("Say how you pay.", ["I paid with a card", "cash"],
                    ["Я платил картой", "наличными"]),
              ])),
        ]},
        {"id": "A1+-U2", "title": "Дом и адрес", "lessons": [
            L("Где вы живёте?",
              "Жить takes в or на and the prepositional case: я живу в Москве, в центре, на "
              "пятом этаже. The address is read in one line: улица, дом, корпус, квартира. "
              "Дом is both the building and the home, so дома means at home and в доме means "
              "inside the building.",
              [V("жить", "ZHEETY", "to live", "verb"),
               V("адрес", "AH-drees", "address", "noun"),
               V("улица", "OO-lee-tsah", "street", "noun"),
               V("квартира", "kvahr-TEE-rah", "flat, apartment", "noun"),
               V("этаж", "eh-TAHSH", "floor, storey", "noun")],
              G("Я живу в …",
                "жить + в / на + prepositional · улица Пушкина, дом 5, квартира 12",
                "Жить takes the prepositional for the place: живу в центре, в Москве, на "
                "Тверской. The address is spoken without prepositions after the first: улица "
                "Пушкина, дом пять, квартира двенадцать. Дома (at home) and домой (homewards) "
                "are adverbs and take no preposition at all.",
                [X("Я живу в Москве, в центре.", "yah zhee-VOO v mahsk-VYEH, v TSYEHN-treh.", "I live in Moscow, in the centre."),
                X("Мой адрес: улица Пушкина, дом пять, квартира двенадцать.", "moy AH-drees: OO-lee-tsah POOSH-kee-nah, dohm pyahty, kvahr-TEE-rah dvee-NAHTS-tsahty.", "My address: 5 Pushkin Street, flat twelve."),
                X("Я живу на пятом этаже.", "yah zhee-VOO nah PYAH-tahm eh-tah-ZHEH.", "I live on the fifth floor.")],
                [("Я живу в Москва.", "Я живу в Москве.", "Жить + где takes the prepositional: в Москве."),
                 ("Мой адрес — в улица Пушкина.", "Мой адрес: улица Пушкина.", "The street name needs no preposition after адрес.")]),
              [D("Курьер", "Ваш адрес, пожалуйста.", "vahsh AH-drees, pah-ZHAH-loo-stah.", "Your address, please."),
               D("Жильец", "Улица Пушкина, дом пять, квартира двенадцать.", "OO-lee-tsah POOSH-kee-nah, dohm pyahty, kvahr-TEE-rah dvee-NAHTS-tsahty.", "5 Pushkin Street, flat twelve."),
               D("Курьер", "Какой этаж?", "kah-KOY eh-TAHSH?", "Which floor?"),
               D("Жильец", "Пятый. Лифт работает.", "PYAH-tihy. leeft rah-BOH-tah-yeht.", "The fifth. The lift works.")],
              WS("Address worksheet", [
                  T("Say where you live.", ["I live in Moscow, in the centre", "I live on the fifth floor"],
                    ["Я живу в Москве, в центре", "Я живу на пятом этаже"]),
                  T("Give the address.", ["5 Pushkin Street, flat twelve", "which floor?"],
                    ["Улица Пушкина, дом пять, квартира двенадцать", "Какой этаж?"]),
              ])),
            L("Подъезд, код и лифт",
              "A Russian entrance is a whole sentence: подъезд (the stairwell door you buzz), "
              "код (the door code), звонок (the bell), лифт and лестница. Код is dictated "
              "digit by digit, and the phrase «код не работает» is the reason a guest ends up "
              "walking up five floors.",
              [V("подъезд", "pahd-YEHZD", "entrance, stairwell", "noun"),
               V("код", "koht", "code", "noun"),
               V("звонок", "zvah-NOHK", "bell, ring", "noun"),
               V("лифт", "leeft", "lift", "noun"),
               V("лестница", "LYEHS-nee-tsah", "stairs, staircase", "noun")],
              G("Как войти в подъезд",
                "позвонить в + accusative · набрать код · лифт не работает",
                "Позвонить в квартиру (to ring the flat) and набрать код (to enter the code) "
                "are the two actions at the door. Набрать takes the accusative: наберите "
                "код. Не работает is the universal sentence for a lift, a bell or a card "
                "reader, and it takes no adjective: лифт не работает, звонок не работает.",
                [X("Наберите код: один, два, три, четыре.", "nah-bee-REE-teh koht: ah-DEEN, dvah, tree, chee-TIH-reeh.", "Enter the code: one, two, three, four."),
                X("Позвоните в квартиру двенадцать.", "pahz-vah-NEE-teh v kvahr-TEE-roo dvee-NAHTS-tsahty.", "Ring flat twelve."),
                X("Лифт не работает, придётся по лестнице.", "leeft nee rah-BOH-tah-yeht, pree-DYOHT-syah pah LYEHS-nee-tseh.", "The lift is not working, we'll have to use the stairs.")],
                [("Позвоните к квартиру.", "Позвоните в квартиру.", "Позвонить в + accusative, not к."),
                 ("Лифт не в работе.", "Лифт не работает.", "The fixed phrase is не работает.")]),
              [D("Гость", "Я у подъезда. Какой код?", "yah oo pahd-YEHZD-ah. kah-KOY koht?", "I'm at the entrance. What's the code?"),
               D("Хозяин", "Один-два-три-четыре. Потом в квартиру двенадцать.", "ah-DEEN-dvah-tree-chee-TIH-reeh. pah-TOHM v kvahr-TEE-roo dvee-NAHTS-tsahty.", "One-two-three-four. Then ring flat twelve."),
               D("Гость", "Код не работает.", "koht nee rah-BOH-tah-yeht.", "The code doesn't work."),
               D("Хозяин", "Тогда спускаюсь. Лифт у нас тоже не работает.", "tahg-DAH spoo-SKAH-yoosy. leeft oo nahs TOH-zhih nee rah-BOH-tah-yeht.", "Then I'm coming down. Our lift isn't working either.")],
              WS("Entrance worksheet", [
                  T("Give the instructions.", ["enter the code: one, two, three, four", "ring flat twelve"],
                    ["Наберите код: один, два, три, четыре", "Позвоните в квартиру двенадцать"]),
                  T("Report a fault.", ["the code doesn't work", "the lift is not working"],
                    ["Код не работает", "Лифт не работает"]),
              ])),
            L("Описываем квартиру",
              "A flat is described room by room with the prepositional after в: в комнате, на "
              "кухне, на балконе. Окно, дверь and шкаф are the three things worth naming in "
              "every room, and the room names themselves — комната, кухня, ванная — are "
              "feminine. There is no «уютно» without furniture: the word covers both cosiness "
              "and comfort.",
              [V("комната", "KOHM-nah-tah", "room", "noun"),
               V("кухня", "KOOKH-nyah", "kitchen", "noun"),
               V("балкон", "bahl-KOHN", "balcony", "noun"),
               V("окно", "ahk-NOH", "window", "noun"),
               V("уютно", "oo-YOOT-nah", "cosy, comfortable", "adverb")],
              G("Наша квартира",
                "в комнате / на кухне / на балконе · у нас есть · здесь уютно",
                "Rooms take в or на and the prepositional: в комнате, на кухне, на балконе. "
                "У нас есть lists what the flat contains, and здесь + adverb gives the "
                "impression without a subject: здесь светло, здесь уютно. A window looks "
                "somewhere with выходить на + accusative: окно выходит на улицу.",
                [X("В комнате большое окно.", "v KOHM-nah-teh bahl-SHOH-yeh ahk-NOH.", "There is a big window in the room."),
                X("На кухне мы завтракаем.", "nah KOOKH-nyeh mih ZAHF-trah-kah-yehm.", "We have breakfast in the kitchen."),
                X("Окно выходит на улицу, здесь уютно.", "ahk-NOH VIH-khah-deet nah OO-lee-tsoo, zdyehsy oo-YOOT-nah.", "The window looks on to the street, it is cosy here.")],
                [("В комната большое окно.", "В комнате большое окно.", "В + room takes the prepositional: в комнате."),
                 ("Здесь уютный.", "Здесь уютно.", "An impression with no subject is the adverb: уютно.")]),
              [D("Гостья", "Какая у вас квартира?", "kah-KAH-yah oo vahs kvahr-TEE-rah?", "What is your flat like?"),
               D("Хозяйка", "Небольшая, но уютная. Две комнаты и кухня.", "nee-bahl-SHAH-yah, noh oo-YOOT-nah-yah. dveh KOHM-nah-tih ee KOOKH-nyah.", "Small, but cosy. Two rooms and a kitchen."),
               D("Гостья", "Балкон есть?", "bahl-KOHN yehsty?", "Is there a balcony?"),
               D("Хозяйка", "Есть. Окно выходит на парк, вечером там очень тихо.", "yehsty. ahk-NOH VIH-khah-deet nah pahrk, VYEH-cheh-rahm tahm OH-chehn TEE-khah.", "There is. The window looks on to the park, in the evening it is very quiet there.")],
              WS("Flat worksheet", [
                  T("Describe the rooms.", ["there is a big window in the room", "we have breakfast in the kitchen"],
                    ["В комнате большое окно", "На кухне мы завтракаем"]),
                  T("Give the impression.", ["the window looks on to the street", "it is cosy here"],
                    ["Окно выходит на улицу", "Здесь уютно"]),
              ])),
        ]},
        {"id": "A1+-U3", "title": "Время и день", "lessons": [
            L("Который час?",
              "Time is asked with который час? and answered with the hour and the part of the "
              "day: два часа дня, семь часов утра. Минуты follow the hour (двадцать минут "
              "третьего means twenty past two), and половина is half past. Утра, дня, вечера "
              "and ночи stand in the genitive and place the hour.",
              [V("час", "chahs", "hour, o'clock", "noun"),
               V("минута", "mee-NOO-tah", "minute", "noun"),
               V("половина", "pah-lah-VEE-nah", "half", "noun"),
               V("утро", "OO-trah", "morning", "noun"),
               V("вечер", "VYEH-chehr", "evening", "noun")],
              G("Который час?",
                "два часа дня · двадцать минут третьего · половина седьмого · в семь утра",
                "The full hour takes часа/часов and the part of day: три часа дня, восемь "
                "часов вечера. Minutes past the hour are counted towards the NEXT hour in the "
                "genitive — двадцать минут третьего is 2:20 — while официальное время says "
                "два двадцать. В + accusative places the event: в семь утра, в половине "
                "восьмого.",
                [X("Который час? — Половина седьмого.", "kah-TOH-rihy chahs? — pah-lah-VEE-nah see-DYOH-mah-vah.", "What time is it? — Half past six."),
                X("Встреча в два часа дня.", "FSTREH-chah v dvah chah-SAH dnyah.", "The meeting is at two in the afternoon."),
                X("Я встаю в семь утра.", "yah fstah-YOO v syeemy OOT-rah.", "I get up at seven in the morning.")],
                [("Половина шесть.", "Половина седьмого.", "Half past six points to the seventh hour: половина седьмого."),
                 ("Встреча в два час.", "Встреча в два часа.", "Два takes часа, not час.")]),
              [D("Коллега", "Который час?", "kah-TOH-rihy chahs?", "What time is it?"),
               D("Иван", "Половина третьего.", "pah-lah-VEE-nah TRYEHty-yeh-vah.", "Half past two."),
               D("Коллега", "У нас встреча в три?", "oo nahs FSTREH-chah v tree?", "Is our meeting at three?"),
               D("Иван", "Да, в три часа дня. Уже двадцать пять минут третьего.", "dah, v tree chah-SAH dnyah. oo-ZHEH DVAHts-tsahty pyahty mee-NOOT TRYEHty-yeh-vah.", "Yes, at three in the afternoon. It is already twenty-five past two.")],
              WS("Clock worksheet", [
                  T("Answer the clock.", ["half past six", "seven in the morning"],
                    ["Половина седьмого", "семь утра"]),
                  T("Place the meeting.", ["the meeting is at two in the afternoon", "at twenty past two"],
                    ["Встреча в два часа дня", "двадцать минут третьего"]),
              ])),
            L("Дни недели и расписание",
              "The week runs from понедельник to воскресенье, and в + accusative names the day: "
              "в понедельник, в среду (irregular), в пятницу. Расписание is the timetable; по + "
              "dative means every: по средам, по утрам, по выходным.",
              [V("понедельник", "pah-nee-DYEHl-neek", "Monday", "noun"),
               V("среда", "sree-DAH", "Wednesday", "noun"),
               V("суббота", "soo-BOH-tah", "Saturday", "noun"),
               V("воскресенье", "vahs-kree-SYEH-nyeh", "Sunday", "noun"),
               V("расписание", "rahs-pee-SAH-nee-yeh", "timetable", "noun")],
              G("Дни недели",
                "в понедельник · в среду · по средам (every Wednesday) · по выходным",
                "One day takes в + accusative: в понедельник, в среду, в пятницу, в субботу. "
                "A repeated day takes по + dative: по средам, по воскресеньям. По утрам "
                "means every morning and по выходным every weekend. The timetable is "
                "read with с … до …: с девяти до шести.",
                [X("В понедельник я работаю, в среду — учусь.", "v pah-nee-DYEHl-neek yah rah-BOH-tah-yoo, v SREH-doo — oo-CHOOSY.", "On Monday I work, on Wednesday I study."),
                X("По субботам мы ездим на дачу.", "pah soo-BOH-tahm mih YEHZ-deem nah DAH-choo.", "On Saturdays we go to the dacha."),
                X("По расписанию урок с десяти до половины двенадцатого.", "pah rahs-pee-SAH-nee-yoo oo-ROHK s dee-see-TEE dah pah-lah-VEE-nih dvee-NAHTS-tsah-tah-vah.", "According to the timetable the lesson runs from ten to half past eleven.")],
                [("На понедельник я работаю.", "В понедельник я работаю.", "A single day takes в + accusative."),
                 ("По субботу мы ездим на дачу.", "По субботам мы ездим на дачу.", "A repeated day takes по + dative plural.")]),
              [D("Анна", "Когда у вас уроки?", "kahg-DAH oo vahs oo-ROH-kee?", "When are your lessons?"),
               D("Иван", "По средам и по пятницам, с шести до восьми.", "pah SREH-dahm ee pah PYAHt-nee-tsahm, s shees-TEE dah vahs-MEE.", "On Wednesdays and Fridays, from six to eight."),
               D("Анна", "А в выходные?", "ah v vih-khahd-NIH-yeh?", "And at the weekend?"),
               D("Иван", "В субботу — нет, а в воскресенье — утром.", "f soo-BOH-too — nyeht, ah v vahs-kree-SYEH-nyeh — OOT-rahm.", "Not on Saturday, but on Sunday morning.")],
              WS("Week worksheet", [
                  T("Name the day.", ["on Monday I work", "on Wednesday I study"],
                    ["В понедельник я работаю", "В среду я учусь"]),
                  T("Say what repeats.", ["on Saturdays we go to the dacha", "on Wednesdays and Fridays"],
                    ["По субботам мы ездим на дачу", "по средам и по пятницам"]),
              ])),
            L("Мой день по часам",
              "A daily routine is a chain of verbs: вставать, завтракать, идти на работу, "
              "обедать, ужинать, ложиться спать. Times stand before the verb with в + "
              "accusative: в семь я встаю. Ложиться спать is the last pair, and the reflexive "
              "-ся stays with the verb in every form.",
              [V("вставать", "fstah-VAHTY", "to get up", "verb"),
               V("завтрак", "ZAHF-trahk", "breakfast", "noun"),
               V("обед", "ah-BYED", "lunch, dinner", "noun"),
               V("ужин", "OO-zheen", "supper", "noun"),
               V("ложиться", "lah-ZHEET-syah", "to go to bed", "verb")],
              G("Мой день",
                "в семь я встаю · в два часа обед · ложусь спать в одиннадцать",
                "The routine runs in the present: встаю, завтракаю, иду, обедаю, ужинаю, "
                "ложусь спать. The time comes first with в + accusative, and утром, днём, "
                "вечером, ночью mark the part of day without a preposition. Ложиться спать "
                "is reflexive: я ложусь, ты ложишься, он ложится.",
                [X("В семь утра я встаю и завтракаю.", "v syeemy OOT-rah yah fstah-YOO ee ZAHF-trah-kah-yoo.", "At seven in the morning I get up and have breakfast."),
                X("Днём я обедаю в кафе.", "dnyohm yah ah-BYEH-dah-yoo v kah-FEH.", "In the afternoon I have lunch in a café."),
                X("Вечером я ужинаю дома и ложусь спать в одиннадцать.", "VYEH-cheh-rahm yah OO-zhee-nah-yoo DOH-mah ee lah-ZHOOSY spaaty v ah-DEE-nahd-tsahty.", "In the evening I have supper at home and go to bed at eleven.")],
                [("В семь утра я встаю, потом завтрак, потом идти работа, потом обед, и всё.", "В семь утра я встаю, потом завтракаю и иду на работу.", "Every step of a routine is a finite verb."),
                 ("Я ложу спать в одиннадцать.", "Я ложусь спать в одиннадцать.", "Ложиться is reflexive: ложусь.")]),
              [D("Марина", "Во сколько ты встаёшь?", "vah SKOHL-kah tih fstah-YOHSH?", "What time do you get up?"),
               D("Иван", "В половине седьмого. Завтракаю и иду на работу.", "v pah-lah-VEE-nyeh see-DYOH-mah-vah. ZAHF-trah-kah-yoo ee ee-DOO nah rah-BOH-too.", "At half past six. I have breakfast and go to work."),
               D("Марина", "А когда обедаешь?", "ah kahg-DAH ah-BYEH-dah-yesh?", "And when do you have lunch?"),
               D("Иван", "В час дня. Вечером ужинаю и ложусь спать в одиннадцать.", "f chahs dnyah. VYEH-cheh-rahm OO-zhee-nah-yoo ee lah-ZHOOSY spaaty v ah-DEE-nahd-tsahty.", "At one in the afternoon. In the evening I have supper and go to bed at eleven.")],
              WS("Routine worksheet", [
                  T("Give the routine.", ["at seven in the morning I get up and have breakfast", "in the evening I have supper at home"],
                    ["В семь утра я встаю и завтракаю", "Вечером я ужинаю дома"]),
                  T("Give the times.", ["I go to bed at eleven", "I have lunch at one in the afternoon"],
                    ["Я ложусь спать в одиннадцать", "Я обедаю в час дня"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Русское время читается двумя способами сразу: официальное расписание говорит "
                 "«семнадцать тридцать», а человек на улице — «половина шестого». Опоздание "
                 "на пятнадцать минут на встречу с другом не считается опозданием, а вот на "
                 "поезд или на собеседование — считается; отсюда и фраза «я на минутку», "
                 "которая в киоске может значить четверть часа в очереди."),
        source_url="https://en.wikipedia.org/wiki/Time_in_Russia",
        reading=("Каждое утро я выхожу в семь и по дороге покупаю воду в киоске у метро. "
                 "Продавец уже знает меня: «Сорок рублей, картой или наличными?» Очередь "
                 "короткая, и всегда кто-то спрашивает: «Чья очередь?» Потом я иду на "
                 "работу. Возвращаюсь домой в семь вечера, ужинаю и ложусь спать в "
                 "одиннадцать. В субботу по утрам я никуда не спешу."),
        reading_gloss=("Every morning I leave at seven and on the way I buy water at the kiosk "
                       "by the metro. The seller already knows me: 'Forty roubles, card or "
                       "cash?' The queue is short, and someone always asks: 'Whose turn is "
                       "it?' Then I go to work. I come home at seven in the evening, have "
                       "supper and go to bed at eleven. On Saturday mornings I don't hurry "
                       "anywhere."),
        listening=("Сколько стоит вода? — Сорок рублей. — А пакет есть? — Пакета нет. — "
                   "Тогда картой, и можно чек."),
        listening_gloss=("How much is the water? — Forty roubles. — And is there a bag? — "
                         "There is no bag. — Then card, and could I have the receipt."),
        voice_tag=VOICE,
        idioms=[
            ("на минутку", "for a minute", "briefly, in passing — often longer in reality"),
            ("сдачи нет", "there is no change", "said at the till when there is nothing to give back"),
            ("как раз", "exactly", "just right, precisely"),
            ("в два счёта", "in two counts", "in a moment, very quickly"),
            ("круглые сутки", "round the clock", "twenty-four hours a day"),
            ("ни свет ни заря", "neither light nor dawn", "at an ungodly early hour"),
            ("время от времени", "time from time", "from time to time"),
            ("битый час", "a beaten hour", "a whole hour wasted"),
            ("под рукой", "under the hand", "close at hand"),
            ("до конца дня", "until the end of the day", "by the end of the day"),
        ],
        mistakes=[
            ("Я живу в Москва.", "Я живу в Москве.", "Жить + где takes the prepositional."),
            ("Половина шесть.", "Половина седьмого.", "Half past six is половина седьмого."),
            ("У меня нет пакет.", "У меня нет пакета.", "Нет takes the genitive."),
        ],
        task_title="Мой день в двенадцати строчках",
        task_instructions=("Write your own day in twelve lines: the hour you get up, what you "
                           "eat, how you get to work or study, when you come home and when "
                           "you go to bed. Use в + time, одна покупка у киоска and the "
                           "reflexive ложусь спать. Then read it aloud and check three things: "
                           "который час vs во сколько, в + accusative for a single day, and "
                           "по + dative for a repeated one."),
    ),
    "test": [
        ("translate_en", "Say: how much is the water?", "Сколько стоит вода?"),
        ("translate_ru", "Я живу в Москве, на пятом этаже.", "I live in Moscow, on the fifth floor."),
        ("multiple_choice", "Which sentence says there is no change?", "У меня нет сдачи."),
        ("fill_in_the_blank", "У меня ___ пакета.", "нет"),
        ("word_selection", "Select the Russian for 'till, checkout'.", "касса"),
        ("error_correction", "Я живу в Москва.", "Я живу в Москве."),
        ("dialogue_completion", "Complete: Который час? — ___ (half past six)", "Половина седьмого"),
        ("matching", "Match сдача to its meaning.", "change (money back)"),
        ("reading_comprehension", "В тексте, что автор покупает в киоске?", "water"),
        ("inference", "Продавец уже знает покупателя. What does that tell us about the kiosk?", "the same person buys there every day"),
        ("main_idea", "В тексте описан обычный день. — what is this sentence?", "the main point of the reading"),
        ("detail_identification", "Во сколько автор ложится спать?", "at eleven"),
    ],
}

HALFSTEPS["A2+"] = {
    "native": NATIVE,
    "title": "%s A2+ — Метро, касса и гостиница" % NAME,
    "goals": [
        "Find your line, change trains and ask for help in the metro",
        "Buy a ticket, understand the carriage classes and survive a delay",
        "Check into a hotel, report what is broken and check out",
    ],
    "units": [
        {"id": "A2+-U1", "title": "В метро", "lessons": [
            L("Станция и линия",
              "The metro is described with в and на and the prepositional: на станции, на "
              "линии, в переходе. To change trains you перейти на другую линию — на + "
              "accusative, because a change is movement. The exit is выход, and выход в город "
              "is the one a visitor needs.",
              [V("станция", "STAHN-tsee-yah", "station", "noun"),
               V("линия", "LEE-nee-yah", "line", "noun"),
               V("переход", "pee-ree-KHOHT", "passage, transfer", "noun"),
               V("выход", "VIH-khaht", "exit", "noun"),
               V("перейти", "pee-ree-TEETY", "to cross, to change to", "verb")],
              G("Как перейти на другую линию",
                "на станции / на линии · перейти на + accusative · выход в город",
                "Where you are takes the prepositional: мы на станции «Арбатская», поезд на "
                "красной линии. Where you go takes the accusative after перейти: перейдите "
                "на другую линию. Выход в город is the sign to the street, and the word "
                "пересадка names the change when you talk about the journey as a whole.",
                [X("Мы на станции «Арбатская».", "mih nah STAHN-tsee-ee ahr-BAHT-skah-yah.", "We are at Arbatskaya station."),
                X("Перейдите на красную линию и едьте до центра.", "pee-ree-DEE-teh nah KRAHS-noo-yoo LEE-nee-yoo ee YEHd-teh dah TSYEHN-trah.", "Change to the red line and ride to the centre."),
                X("Выход в город — направо.", "VIH-khaht v GOH-raht — nah-PRAH-vah.", "The exit to the city is to the right.")],
                [("Перейдите на красной линии.", "Перейдите на красную линию.", "Перейти на takes the accusative."),
                 ("Мы в станции «Арбатская».", "Мы на станции «Арбатская».", "A station takes на: на станции.")]),
              [D("Турист", "Как перейти на красную линию?", "kahk pee-ree-TEETY nah KRAHS-noo-yoo LEE-nee-yoo?", "How do I change to the red line?"),
               D("Дежурная", "По переходу, потом налево. Выход в город — прямо.", "pah pee-ree-KHOH-doo, pah-TOHM nah-LYEH-vah. VIH-khaht v GOH-raht — PRYAH-mah.", "Through the passage, then left. The exit to the city is straight ahead."),
               D("Турист", "Сколько станций до центра?", "SKOHL-kah STAHN-tsee-ee dah TSYEHN-trah?", "How many stations to the centre?"),
               D("Дежурная", "Три, с одной пересадкой.", "tree, s ahd-NOY pee-ree-SAHD-koy.", "Three, with one change.")],
              WS("Metro worksheet", [
                  T("Ask about the change.", ["how do I change to the red line?", "how many stations to the centre?"],
                    ["Как перейти на красную линию?", "Сколько станций до центра?"]),
                  T("Follow the signs.", ["the exit to the city is straight ahead", "we are at Arbatskaya station"],
                    ["Выход в город — прямо", "Мы на станции «Арбатская»"]),
              ])),
            L("Карта и жетон",
              "A journey is оплачен with a card or a single ticket: пополнить карту, купить "
              "жетон, одна поездка. The verb пополнить takes the accusative: пополните карту. "
              "The turnstile is турникет, and the machine that refills the card is автомат, "
              "which asks for наличные or карта.",
              [V("жетон", "zhee-TOHN", "token", "noun"),
               V("турникет", "toor-nee-KYEHT", "turnstile", "noun"),
               V("пополнить", "pah-POHL-neety", "to top up", "verb"),
               V("поездка", "pah-YEHZD-kah", "journey, ride", "noun"),
               V("автомат", "ahf-tah-MAHT", "machine, automat", "noun")],
              G("Оплата проезда",
                "пополнить карту · одна поездка стоит · приложите карту к турникету",
                "Пополнить takes the accusative (пополните карту на сто рублей) and the "
                "amount takes на + accusative. The machine asks приложите карту and then "
                "показывает баланс. Одна поездка стоит пятьдесят рублей is the sentence to "
                "compare prices with, and the plural follows the numeral as always.",
                [X("Пополните карту на сто рублей.", "pah-POHL-nee-teh KAHR-too nah stoh ROOB-lyey.", "Top up the card by a hundred roubles."),
                X("Одна поездка стоит пятьдесят рублей.", "ahd-NAH pah-YEHZD-kah STOH-eet pee-dee-SYAHT ROOB-lyey.", "One ride costs fifty roubles."),
                X("Приложите карту к турникету.", "pree-lah-ZHEE-teh KAHR-too k toor-nee-KYEH-too.", "Tap the card at the turnstile.")],
                [("Пополните карта.", "Пополните карту.", "Пополнить takes the accusative: карту."),
                 ("Одна поездка стоит на пятьдесят рублей.", "Одна поездка стоит пятьдесят рублей.", "Стоить takes a bare number.")]),
              [D("Пассажир", "Как купить жетон?", "kahk koo-PEETY zhee-TOHN?", "How do I buy a token?"),
               D("Кассир", "В автомате. Можно картой.", "v ahf-tah-MAH-teh. MOHZH-nah KAHR-toy.", "At the machine. You can use a card."),
               D("Пассажир", "А пополнить карту?", "ah pah-POHL-neety KAHR-too?", "And top up a card?"),
               D("Кассир", "Тоже в автомате, от ста рублей.", "TOH-zhih v ahf-tah-MAH-teh, aht stah ROOB-lyey.", "Also at the machine, from a hundred roubles.")],
              WS("Fare worksheet", [
                  T("Top up and pay.", ["top up the card by a hundred roubles", "tap the card at the turnstile"],
                    ["Пополните карту на сто рублей", "Приложите карту к турникету"]),
                  T("Ask about the price.", ["how much does one ride cost?", "how do I buy a token?"],
                    ["Сколько стоит одна поездка?", "Как купить жетон?"]),
              ])),
            L("В вагоне: спросить и помочь",
              "Inside the carriage, three sentences do the work: это место свободно? (is this "
              "seat free?), вы выходите? (are you getting off?), and уступить место (to give "
              "up a seat). Вы выходите? is asked before every exit and answered with выхожу "
              "or нет, не выхожу.",
              [V("вагон", "vah-GOHN", "carriage", "noun"),
               V("место", "MYEH-stah", "seat, place", "noun"),
               V("уступить", "oo-stoo-PEETY", "to give up, to yield", "verb"),
               V("спросить", "sprah-SEETY", "to ask", "verb"),
               V("выходить", "vih-khah-DEETY", "to get off", "verb")],
              G("Вы выходите?",
                "это место свободно? · вы выходите? · уступить место + dative",
                "Вы выходите? is the standard question in a crowded carriage, and it is "
                "answered in one word — выхожу or нет. Уступить место takes the dative for "
                "the person: уступить место бабушке. Помогите takes the same dative, and the "
                "request can be softened with пожалуйста or извините.",
                [X("Извините, это место свободно?", "eez-vee-NEE-teh, EH-tah MYEH-stah svah-BOHD-nah?", "Excuse me, is this seat free?"),
                X("Вы выходите? — Да, выхожу.", "vih vih-KHOH-dee-teh? — dah, vih-khah-ZHOO.", "Are you getting off? — Yes, I am."),
                X("Уступите место бабушке, пожалуйста.", "oo-stoo-PEE-teh MYEH-stah BAH-boosh-kyeh, pah-ZHAH-loo-stah.", "Give up your seat to the grandmother, please.")],
                [("Вы идёте выходить?", "Вы выходите?", "The fixed question is two words."),
                 ("Уступите место бабушка.", "Уступите место бабушке.", "Уступить место takes the dative.")]),
              [D("Пассажир", "Извините, вы выходите?", "eez-vee-NEE-teh, vih vih-KHOH-dee-teh?", "Excuse me, are you getting off?"),
               D("Пассажирка", "Нет, не выхожу. Садитесь, место свободно.", "nyeht, nee vih-khah-ZHOO. sah-DEE-teh-syah, MYEH-stah svah-BOHD-nah.", "No, I'm not. Sit down, the seat is free."),
               D("Пассажир", "Спасибо. Вы не подскажете, где переход?", "spah-SEE-bah. vih nee paht-SKAH-zheh-teh, gdyeh pee-ree-KHOHT?", "Thank you. Could you tell me where the transfer is?"),
               D("Пассажирка", "На следующей станции, по переходу направо.", "nah SLYEH-doo-yoo-shchey STAHN-tsee-ee, pah pee-ree-KHOH-doo nah-PRAH-vah.", "At the next station, through the passage to the right.")],
              WS("Carriage worksheet", [
                  T("Ask in the carriage.", ["is this seat free?", "are you getting off?"],
                    ["Это место свободно?", "Вы выходите?"]),
                  T("Help and thank.", ["give up your seat to the grandmother, please", "could you tell me where the transfer is?"],
                    ["Уступите место бабушке, пожалуйста", "Вы не подскажете, где переход?"]),
              ])),
        ]},
        {"id": "A2+-U2", "title": "В кассе", "lessons": [
            L("Билет туда и обратно",
              "A ticket is bought до + genitive (билет до Санкт-Петербурга), and the round trip "
              "is туда и обратно. The cashier asks на когда? and на сколько человек? — the "
              "answer takes на + accusative. Место is the seat, and верхняя/нижняя полка the "
              "upper or lower berth.",
              [V("билет", "bee-LYEHT", "ticket", "noun"),
               V("туда", "too-DAH", "there, one way out", "adverb"),
               V("обратно", "ahb-RAHT-nah", "back", "adverb"),
               V("касса", "KAH-sah", "ticket office", "noun"),
               V("место", "MYEH-stah", "seat", "noun")],
              G("Купить билет",
                "билет до + genitive · туда и обратно · на завтра, на два человека",
                "До + genitive names the destination: билет до Москвы. На + accusative names "
                "the time and the people: на завтра, на девять утра, на два человека. The "
                "question сколько стоит? takes the answer in roubles, and сдача is still the "
                "word for the change.",
                [X("Один билет до Москвы, пожалуйста.", "ah-DEEN bee-LYEHT dah mahsk-VIH, pah-ZHAH-loo-stah.", "One ticket to Moscow, please."),
                X("Туда и обратно, на завтра.", "too-DAH ee ahb-RAHT-nah, nah ZAHF-trah.", "Return, for tomorrow."),
                X("Сколько стоит билет на два человека?", "SKOHL-kah STOH-eet bee-LYEHT nah dvah cheh-lah-VYEH-kah?", "How much is a ticket for two people?")],
                [("Билет в Москва.", "Билет до Москвы.", "A destination takes до + genitive."),
                 ("Билет на два человека и на два человека обратно.", "Билет туда и обратно на два человека.", "The round trip is one phrase: туда и обратно.")]),
              [D("Кассир", "Куда вам билет?", "koo-DAH vahm bee-LYEHT?", "Where to?"),
               D("Пассажир", "До Казани, туда и обратно.", "dah kah-zah-NEE, too-DAH ee ahb-RAHT-nah.", "To Kazan, return."),
               D("Кассир", "На когда?", "nah kahg-DAH?", "For when?"),
               D("Пассажир", "На завтра, на девять утра, на одного.", "nah ZAHF-trah, nah DYEH-veety OOT-rah, nah ahd-nah-VOH.", "For tomorrow, at nine in the morning, for one.")],
              WS("Ticket worksheet", [
                  T("Buy the ticket.", ["one ticket to Moscow, please", "return, for tomorrow"],
                    ["Один билет до Москвы, пожалуйста", "Туда и обратно, на завтра"]),
                  T("Answer the cashier.", ["for tomorrow at nine in the morning, for one", "how much is a ticket for two people?"],
                    ["На завтра, на девять утра, на одного", "Сколько стоит билет на два человека?"]),
              ])),
            L("Поезд, плацкарт и купе",
              "Long-distance trains are sold by class: плацкарт is the open carriage, купе the "
              "four-berth compartment, СВ the two-berth one. The cashier names the train by "
              "number (поезд 056), the carriage (вагон), and the departure time — время "
              "отправления и прибытия.",
              [V("поезд", "POH-yehzd", "train", "noun"),
               V("плацкарт", "plahts-KAHRT", "open-plan berth class", "noun"),
               V("купе", "koo-PEH", "compartment", "noun"),
               V("отправление", "aht-prahv-LYEH-nee-yeh", "departure", "noun"),
               V("прибытие", "pree-BIH-tee-yeh", "arrival", "noun")],
              G("Какой вагон и какое место",
                "плацкарт / купе / СВ · время отправления · верхняя или нижняя полка",
                "The class stands after the preposition в or without one: билет в плацкарт, "
                "билет в купе. The time of departure is asked with во сколько отправление? "
                "and answered with the hour. Верхняя полка is cheaper than нижняя, and the "
                "cashier will ask which one you want.",
                [X("Есть билеты в купе?", "yehsty bee-LYEH-tih v koo-PEH?", "Are there tickets in a compartment?"),
                X("Во сколько отправление?", "vah SKOHL-kah aht-prahv-LYEH-nee-yeh?", "What time is the departure?"),
                X("Дайте нижнюю полку, пожалуйста.", "DAH-ee-teh NEEZH-nyoo-yoo POHL-koo, pah-ZHAH-loo-stah.", "Give me a lower berth, please.")],
                [("Есть билеты в купе? — Да, есть в вагон номер пять.", "Есть билеты в купе? — Да, в пятом вагоне.", "The carriage is named in the prepositional: в пятом вагоне."),
                 ("Во сколько время отправления?", "Во сколько отправление?", "Во сколько already asks the time.")]),
              [D("Кассир", "Плацкарт или купе?", "plahts-KAHRT EE-lee koo-PEH?", "Open carriage or compartment?"),
               D("Пассажир", "Купе. Во сколько отправление?", "koo-PEH. vah SKOHL-kah aht-prahv-LYEH-nee-yeh?", "Compartment. What time is the departure?"),
               D("Кассир", "В двадцать три сорок. Прибытие утром.", "v DVAHts-tsahty tree SOH-rahk. pree-BIH-tee-yeh OOT-rahm.", "At twenty-three forty. Arrival in the morning."),
               D("Пассажир", "Тогда нижнюю полку.", "tahg-DAH NEEZH-nyoo-yoo POHL-koo.", "Then a lower berth.")],
              WS("Train worksheet", [
                  T("Ask about the train.", ["what time is the departure?", "are there tickets in a compartment?"],
                    ["Во сколько отправление?", "Есть билеты в купе?"]),
                  T("Choose the berth.", ["a lower berth, please", "open carriage or compartment?"],
                    ["Нижнюю полку, пожалуйста", "Плацкарт или купе?"]),
              ])),
            L("Опоздал на поезд",
              "A missed train is described in the past with на + accusative: я опоздал на "
              "поезд. The station then offers the three sentences you need: поезд отменили "
              "(the train was cancelled), поезд задержали на час (delayed by an hour), and "
              "можно вернуть билет (the ticket can be refunded).",
              [V("опоздать", "ah-pahz-DAHTY", "to be late", "verb"),
               V("следующий", "SLYEH-doo-yoo-shchiy", "next", "adjective"),
               V("отменить", "aht-mee-NEETY", "to cancel", "verb"),
               V("задержать", "zah-deer-ZHAHTY", "to delay", "verb"),
               V("вернуть", "vehr-NOOTY", "to return, to refund", "verb")],
              G("Поезд отменили",
                "я опоздал на поезд · поезд отменили · задержали на час · можно вернуть билет",
                "Russian reports these events with an impersonal third-person plural and no "
                "subject: отменили, задержали, перенесли. The delay takes на + accusative: "
                "задержали на час. Вернуть takes the accusative (вернуть билет) and опоздать "
                "takes на: опоздать на поезд, на работу.",
                [X("Я опоздал на поезд на десять минут.", "yah ah-pahz-DAHL nah POH-yehzd nah DYEH-seety mee-NOOT.", "I was ten minutes late for the train."),
                X("Поезд задержали на час.", "POH-yehzd zah-deer-ZHAH-lee nah chahs.", "The train was delayed by an hour."),
                X("Можно вернуть билет или взять следующий?", "MOHZH-nah vehr-NOOTY bee-LYEHT EE-lee vzyahty SLYEH-doo-yoo-shchiy?", "Can I refund the ticket or take the next one?")],
                [("Поезд задержали час.", "Поезд задержали на час.", "A delay takes на + accusative."),
                 ("Я опоздал в поезд.", "Я опоздал на поезд.", "Опоздать takes на.")]),
              [D("Пассажир", "Я опоздал на поезд.", "yah ah-pahz-DAHL nah POH-yehzd.", "I missed the train."),
               D("Дежурная", "Какой поезд?", "kah-KOY POH-yehzd?", "Which train?"),
               D("Пассажир", "Ночной. Его отменили?", "nahch-NOY. yeh-VOH aht-mee-NEE-lee?", "The night one. Was it cancelled?"),
               D("Дежурная", "Задержали на час. Можно вернуть билет и взять следующий.", "zah-deer-ZHAH-lee nah chahs. MOHZH-nah vehr-NOOTY bee-LYEHT ee vzyahty SLYEH-doo-yoo-shchiy.", "Delayed by an hour. You can refund the ticket and take the next one.")],
              WS("Delay worksheet", [
                  T("Report the problem.", ["I was ten minutes late for the train", "the train was delayed by an hour"],
                    ["Я опоздал на поезд на десять минут", "Поезд задержали на час"]),
                  T("Ask about the options.", ["can I refund the ticket and take the next one?", "was the train cancelled?"],
                    ["Можно вернуть билет и взять следующий?", "Его отменили?"]),
              ])),
        ]},
        {"id": "A2+-U3", "title": "В гостинице", "lessons": [
            L("Бронь и паспорт",
              "Check-in runs on four words: бронь (reservation), паспорт, номер (room) and "
              "регистрация. The hotel asks у вас есть бронь? and then ваш паспорт, "
              "пожалуйста. Номер is both a number and a hotel room, and на двоих means for "
              "two people.",
              [V("бронь", "brohny", "reservation", "noun"),
               V("паспорт", "PAHS-pahrt", "passport", "noun"),
               V("номер", "NOH-meer", "room; number", "noun"),
               V("регистрация", "ree-gee-STRAH-tsee-yah", "registration, check-in", "noun"),
               V("ключ", "klyooch", "key", "noun")],
              G("Заселение в гостиницу",
                "у меня бронь на имя … · номер на двоих · вот мой паспорт",
                "The reservation is named with на имя + genitive: бронь на имя Иванова. The "
                "room is described with на + accusative for the number of people: номер на "
                "двоих, номер на одного. Регистрация closes the ritual, and the receptionist "
                "hands over ключ with приятного отдыха.",
                [X("У меня бронь на имя Иванова.", "oo meh-NYAH brohny nah EE-myah ee-vah-NOH-vah.", "I have a reservation in the name of Ivanov."),
                X("Мне нужен номер на двоих.", "mnyeh NOO-zhehn NOH-meer nah dvah-EKH.", "I need a room for two."),
                X("Вот мой паспорт. Где регистрация?", "voht moy PAHS-pahrt. gdyeh ree-gee-STRAH-tsee-yah?", "Here is my passport. Where is the check-in?")],
                [("У меня бронь от Иванова имени.", "У меня бронь на имя Иванова.", "The reservation is на имя + genitive."),
                 ("Номер для два человека.", "Номер на двоих.", "The price or the room is на + the count: на двоих.")]),
              [D("Портье", "Добрый вечер! У вас есть бронь?", "DOHB-rihy VYEH-chehr! oo vahs yehsty brohny?", "Good evening! Do you have a reservation?"),
               D("Гость", "Есть, на имя Смирнова, на двоих.", "yehsty, nah EE-myah smeer-NOH-vah, nah dvah-EKH.", "Yes, in the name of Smirnov, for two."),
               D("Портье", "Ваш паспорт, пожалуйста. Вот ключ, номер четыреста два.", "vahsh PAHS-pahrt, pah-ZHAH-loo-stah. voht klyooch, NOH-meer chee-TIH-reeh-STAH dvah.", "Your passport, please. Here is the key, room four hundred and two."),
               D("Гость", "Спасибо. Во сколько завтрак?", "spah-SEE-bah. vah SKOHL-kah ZAHF-trahk?", "Thank you. What time is breakfast?")],
              WS("Check-in worksheet", [
                  T("Check in.", ["I have a reservation in the name of Ivanov", "I need a room for two"],
                    ["У меня бронь на имя Иванова", "Мне нужен номер на двоих"]),
                  T("Ask the questions.", ["where is the check-in?", "what time is breakfast?"],
                    ["Где регистрация?", "Во сколько завтрак?"]),
              ])),
            L("В номере: что не работает",
              "A complaint in a hotel is built from three parts: что случилось, что нужно и "
              "когда. Не работает covers the light, the shower and the card; сломан/сломана "
              "agrees with the thing: кран сломан, дверь сломана. The request itself is "
              "можно + accusative or принесите.",
              [V("полотенце", "pah-lah-TYEHN-tsih", "towel", "noun"),
               V("свет", "svyeht", "light, electricity", "noun"),
               V("горячий", "gah-RYAH-chiy", "hot", "adjective"),
               V("сломаться", "slah-MAHT-syah", "to break down", "verb"),
               V("попросить", "pah-prah-SEETY", "to ask for", "verb")],
              G("Что не работает",
                "не работает свет · нет горячей воды · кран сломан · можно полотенце?",
                "The complaint names the thing first: свет не работает, вода не идёт. "
                "Сломаться agrees in gender with the broken object, while не работает stays "
                "the same for everything. Нет + genitive reports what is missing: нет горячей "
                "воды, нет полотенца. Можно полотенце? is a complete request with no verb of "
                "wanting.",
                [X("В номере не работает свет.", "v NOH-mee-reh nee rah-BOH-tah-yeht svyeht.", "The light in the room is not working."),
                X("Нет горячей воды с утра.", "nyeht gah-RYAH-chey vah-DIH s oo-TRAH.", "There has been no hot water since morning."),
                X("Кран сломан. Можно мастера?", "krahn SLOH-mahn. MOHZH-nah MAHS-teh-rah?", "The tap is broken. Could I have a repairman?")],
                [("Свет не работают.", "Свет не работает.", "Свет is singular: не работает."),
                 ("Нет горячая вода.", "Нет горячей воды.", "Нет takes the genitive.")]),
              [D("Гость", "Извините, в номере не работает свет.", "eez-vee-NEE-teh, v NOH-mee-reh nee rah-BOH-tah-yeht svyeht.", "Excuse me, the light in the room is not working."),
               D("Портье", "Минуту, сейчас пришлём мастера.", "mee-NOO-too, see-CHAHs pree-SHLYOHM MAHS-teh-rah.", "One moment, we'll send a repairman now."),
               D("Гость", "И можно ещё два полотенца?", "ee MOHZH-nah yehsh-CHOH dvah pah-lah-TYEHN-tsah?", "And could I have two more towels?"),
               D("Портье", "Конечно. Если нужен утюг — тоже скажите.", "kah-NYESH-nah. YEH-slee NOO-zhehn oo-TYOOK — TOH-zhih skah-ZHEE-teh.", "Of course. If you need an iron — say so too.")],
              WS("Room worksheet", [
                  T("Report the fault.", ["the light in the room is not working", "there is no hot water"],
                    ["В номере не работает свет", "Нет горячей воды"]),
                  T("Ask for things.", ["could I have two more towels?", "could I have a repairman?"],
                    ["Можно два полотенца?", "Можно мастера?"]),
              ])),
            L("Завтрак и выезд",
              "Breakfast is завтрак; включён в цену means it is included. Checkout is выезд, "
              "and the question is во сколько выезд?. Багаж can be left with оставить багаж, "
              "and to pay the invoice you say оплатить счёт — оплатить takes the accusative.",
              [V("завтрак", "ZAHF-trahk", "breakfast", "noun"),
               V("включён", "vlyoo-CHOHN", "included, switched on", "participle"),
               V("выезд", "VIH-yehzd", "checkout, departure", "noun"),
               V("оплатить", "ahp-lah-TEETY", "to pay (an invoice)", "verb"),
               V("багаж", "bah-GAHSH", "luggage", "noun")],
              G("Выезд и счёт",
                "завтрак включён в цену · во сколько выезд? · оставить багаж · оплатить счёт",
                "Включён agrees like an adjective: завтрак включён, вода включена в счёт. "
                "Оставить takes the accusative (оставить багаж у портье) and оплатить too: "
                "оплатить счёт, оплатить номер. Выезд is at noon in most hotels, and the "
                "question во сколько выезд? solves the last morning of the trip.",
                [X("Завтрак включён в цену?", "ZAHF-trahk vlyoo-CHOHN v TSEH-noo?", "Is breakfast included in the price?"),
                X("Во сколько выезд?", "vah SKOHL-kah VIH-yehzd?", "What time is checkout?"),
                X("Можно оставить багаж до вечера?", "MOHZH-nah ah-STAH-veety bah-GAHSH dah VYEH-cheh-rah?", "Can I leave the luggage until the evening?")],
                [("Завтрак включён завтрак в цену.", "Завтрак включён в цену.", "Включён is the predicate; the subject is said once."),
                 ("Можно оставить багаж у портье до вечер.", "Можно оставить багаж у портье до вечера.", "До takes the genitive: до вечера.")]),
              [D("Гость", "Во сколько выезд?", "vah SKOHL-kah VIH-yehzd?", "What time is checkout?"),
               D("Портье", "В двенадцать. Завтрак включён в цену.", "v dvee-NAHTS-tsahty. ZAHF-trahk vlyoo-CHOHN v TSEH-noo.", "At twelve. Breakfast is included in the price."),
               D("Гость", "Можно оставить багаж до вечера?", "MOHZH-nah ah-STAH-veety bah-GAHSH dah VYEH-cheh-rah?", "Can I leave the luggage until the evening?"),
               D("Портье", "Конечно. Оплатите счёт, и всё.", "kah-NYESH-nah. ahp-lah-TEE-teh shchoht, ee vyoh.", "Of course. Pay the bill and that's it.")],
              WS("Checkout worksheet", [
                  T("Ask about the terms.", ["is breakfast included in the price?", "what time is checkout?"],
                    ["Завтрак включён в цену?", "Во сколько выезд?"]),
                  T("Arrange the last morning.", ["can I leave the luggage until the evening?", "pay the bill"],
                    ["Можно оставить багаж до вечера?", "Оплатите счёт"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Московское метро открылось в 1935 году и с самого начала строилось как "
                 "дворец: мрамор, мозаика, витражи и люстры на станциях «Маяковская», "
                 "«Кропоткинская», «Новослободская». Оно и сегодня остаётся самым быстрым "
                 "способом понять город: по названиям станций читается история — "
                 "«Комсомольская», «Парк Победы», «Бульвар Рокоссовского». В час пик "
                 "действуют свои правила вежливости: не выходить, пока не вышли из вагона."),
        source_url="https://en.wikipedia.org/wiki/Moscow_Metro",
        reading=("В понедельник я приехал в Москву и сразу спустился в метро. Купил карту, "
                 "пополнил её на триста рублей и поехал в гостиницу. На станции «Арбатская» "
                 "я перешёл на другую линию и спросил у девушки: «Вы выходите?» Она "
                 "ответила: «Нет, садитесь». Вечером я вернулся тем же маршрутом, только "
                 "уже с пересадкой. Билет туда и обратно в кассе не продают — продают "
                 "поездки на карту."),
        reading_gloss=("On Monday I arrived in Moscow and went straight down into the metro. "
                       "I bought a card, topped it up by three hundred roubles and set off to "
                       "the hotel. At Arbatskaya station I changed to another line and asked a "
                       "young woman: 'Are you getting off?' She answered: 'No, sit down.' In "
                       "the evening I came back by the same route, only with a change. A "
                       "return ticket isn't sold at the ticket office — rides are loaded on "
                       "to the card."),
        listening=("Как перейти на красную линию? — По переходу и налево. — А выход в город? "
                   "— Прямо, до конца."),
        listening_gloss=("How do I change to the red line? — Through the passage and left. — "
                         "And the exit to the city? — Straight ahead, to the end."),
        voice_tag=VOICE,
        idioms=[
            ("в час пик", "at the peak hour", "at rush hour"),
            ("как сельдь в бочке", "like a herring in a barrel", "packed tight, no room"),
            ("битком набито", "stuffed beat-tight", "crammed full"),
            ("на ходу", "on the move", "while moving, without stopping"),
            ("выйти на своей станции", "to get off at one's own station", "to stop at the right moment"),
            ("проехать свою остановку", "to ride past one's stop", "to miss the stop"),
            ("место у окна", "a seat by the window", "the seat everyone wants"),
            ("по пути", "on the way", "on the way, while going"),
            ("в двух шагах", "two steps away", "very close by"),
            ("ждать под часами", "to wait under the clock", "the classic meeting point"),
        ],
        mistakes=[
            ("Можно оставить багаж до вечер.", "Можно оставить багаж до вечера.", "До takes the genitive."),
            ("Нет горячая вода.", "Нет горячей воды.", "Нет takes the genitive."),
            ("Я опоздал в поезд.", "Я опоздал на поезд.", "Опоздать takes на + accusative."),
        ],
        task_title="Одна поездка, три разговора",
        task_instructions=("Write three short dialogues from one journey: at the metro "
                           "turnstile (top up the card, ask the way), at the ticket office "
                           "(destination, class, berth) and at the hotel (reservation, a "
                           "broken tap, checkout). Each one must contain one оговорка or "
                           "problem and one polite request with можно. Then say the three "
                           "aloud and check the cases: до + genitive, на + accusative, нет + "
                           "genitive."),
    ),
    "test": [
        ("translate_en", "Say: how do I change to the red line?", "Как перейти на красную линию?"),
        ("translate_ru", "Во сколько отправление?", "What time is the departure?"),
        ("multiple_choice", "Which sentence reports a broken tap?", "Кран сломан."),
        ("fill_in_the_blank", "Нет горячей ___.", "воды"),
        ("word_selection", "Select the Russian for 'checkout (hotel)'.", "выезд"),
        ("error_correction", "Можно оставить багаж до вечер.", "Можно оставить багаж до вечера."),
        ("dialogue_completion", "Complete: Во сколько выезд? — ___ (at twelve)", "В двенадцать"),
        ("matching", "Match пересадка to its meaning.", "change between lines"),
        ("reading_comprehension", "В тексте, на какую сумму автор пополнил карту?", "three hundred roubles"),
        ("inference", "В тексте сказано, что билет туда и обратно в кассе не продают. What does that tell us about the metro system?", "rides are sold on to the card instead"),
        ("main_idea", "В тексте рассказано о первой поездке в Москве. — what is this sentence?", "the main point of the reading"),
        ("detail_identification", "Какую станцию автор назвал девушке?", "Арбатская"),
    ],
}

HALFSTEPS["B1+"] = {
    "native": NATIVE,
    "title": "%s B1+ — Район, работа и мнение" % NAME,
    "goals": [
        "Move around your own district: services, renting a flat and neighbour rules",
        "Talk about work, apply for a job and survive the exam session",
        "Agree, disagree and discuss the news with reasons, not adjectives",
    ],
    "units": [
        {"id": "B1+-U1", "title": "Район и квартира", "lessons": [
            L("Район и инфраструктура",
              "A district is described with рядом с + instrumental and в шаговой "
              "доступности: аптека рядом с домом, поликлиника в пяти минутах. Почта and банк "
              "take на: на почте, в банке. Рядом, близко and далеко say the distance without "
              "a street name.",
              [V("район", "rah-YOHN", "district, area", "noun"),
               V("аптека", "ahp-TYEH-kah", "pharmacy", "noun"),
               V("поликлиника", "pah-lee-KLEE-nee-kah", "polyclinic", "noun"),
               V("почта", "POHCH-tah", "post office", "noun"),
               V("рядом", "RYAH-dahm", "nearby", "adverb")],
              G("Что есть в районе",
                "рядом с + instrumental · в двух шагах от + genitive · работаю в банке / на почте",
                "Рядом с takes the instrumental: аптека рядом с домом, метро рядом с парком. "
                "От + genitive measures the distance: в двух шагах от метро. Institutions "
                "keep their prepositions: в банке, в школе, на почте, на вокзале. Недалеко "
                "от + genitive is the neutral way to place something on the map of the "
                "district.",
                [X("Аптека рядом с домом, а метро в двух шагах.", "ahp-TYEH-kah RYAH-dahm s DOH-mahm, ah meet-ROH v DVOOKH shah-GAKH.", "The pharmacy is next to the building, and the metro is two steps away."),
                X("Работаю в банке, а жена — на почте.", "rah-BOH-tah-yoo v BAHN-keh, ah zheh-NAH — nah POHCH-teh.", "I work in a bank, and my wife at the post office."),
                X("Поликлиника недалеко от парка.", "pah-lee-KLEE-nee-kah nee-dah-leh-KOH aht PAHR-kah.", "The polyclinic is not far from the park.")],
                [("Аптека рядом дом.", "Аптека рядом с домом.", "Рядом с takes the instrumental."),
                 ("В двух шагах метро, рядом с метро.", "В двух шагах от метро.", "От + genitive measures the distance.")]),
              [D("Новый жилец", "Что здесь рядом?", "shtoh zdyehsy RYAH-dahm?", "What is nearby?"),
               D("Сосед", "Аптека рядом с домом, почта — в пяти минутах.", "ahp-TYEH-kah RYAH-dahm s DOH-mahm, POHCH-tah — v pee-TEE mee-NOO-tahkh.", "The pharmacy is next to the building, the post office five minutes away."),
               D("Новый жилец", "А поликлиника?", "ah pah-lee-KLEE-nee-kah?", "And the polyclinic?"),
               D("Сосед", "Недалеко от парка, в двух шагах от метро.", "nee-dah-leh-KOH aht PAHR-kah, v DVOOKH shah-GAKH aht meet-ROH.", "Not far from the park, two steps from the metro.")],
              WS("District worksheet", [
                  T("Place the services.", ["the pharmacy is next to the building", "the polyclinic is not far from the park"],
                    ["Аптека рядом с домом", "Поликлиника недалеко от парка"]),
                  T("Say where people work.", ["I work in a bank", "my wife works at the post office"],
                    ["Я работаю в банке", "Моя жена работает на почте"]),
              ])),
            L("Аренда квартиры",
              "Renting runs on a fixed set: снять квартиру (to rent), хозяин (landlord), "
              "залог (deposit), коммунальные (utility bills) and договор (contract). Снять "
              "takes the accusative: снять квартиру на год. The price is read с + "
              "instrumental: с коммунальными — that is, bills included.",
              [V("аренда", "ah-RYEHN-dah", "rent, rental", "noun"),
               V("хозяин", "khah-ZYAH-een", "landlord, owner", "noun"),
               V("залог", "zah-LOHK", "deposit", "noun"),
               V("коммунальные", "kah-moo-NAHL-nih-yeh", "utility bills", "noun"),
               V("договор", "dah-gah-VOHR", "contract", "noun")],
              G("Снять квартиру",
                "снять квартиру на год · с коммунальными · залог — одна оплата · подписать договор",
                "Снять takes the accusative and a period with на: снять квартиру на год. "
                "Prices are quoted с + instrumental when something is included — с "
                "коммунальными, с мебелью. Залог возвращается, and the question when signing "
                "is кто платит за ремонт?. Подписать договор closes the negotiation, and "
                "копия паспорта is what the landlord keeps.",
                [X("Хочу снять квартиру на год, с коммунальными.", "khah-CHOO sneety kvahr-TEE-roo nah goht, s kah-moo-NAHL-nih-mee.", "I want to rent a flat for a year, bills included."),
                X("Залог возвращается при выезде?", "zah-LOHK vahz-vrah-SHCHAH-yeht-syah pree VIH-yehz-deh?", "Is the deposit returned on leaving?"),
                X("Где подписать договор?", "gdyeh paht-pee-SAHTY dah-gah-VOHR?", "Where do I sign the contract?")],
                [("Снять за квартиру на год.", "Снять квартиру на год.", "Снять takes the accusative, with no за."),
                 ("Квартира с коммунальными счёт.", "Квартира с коммунальными.", "С + instrumental is the whole phrase.")]),
              [D("Хозяйка", "Смотрите: комната, кухня, балкон.", "smah-TREE-teh: KOHM-nah-tah, KOOKH-nyah, bahl-KOHN.", "Have a look: room, kitchen, balcony."),
               D("Арендатор", "Сколько в месяц, с коммунальными?", "SKOHL-kah v MYEH-seets, s kah-moo-NAHL-nih-mee?", "How much a month, bills included?"),
               D("Хозяйка", "Сорок тысяч с коммунальными, залог — одна оплата.", "SOH-rahk TIH-seech s kah-moo-NAHL-nih-mee, zah-LOHK — ahd-NAH ahp-LAH-tah.", "Forty thousand with bills, deposit one month."),
               D("Арендатор", "Хорошо. Подпишем договор на год?", "khah-rah-SHOH. paht-PEE-shehm dah-gah-VOHR nah goht?", "All right. Shall we sign the contract for a year?")],
              WS("Rent worksheet", [
                  T("State what you want.", ["I want to rent a flat for a year, bills included", "is the deposit returned on leaving?"],
                    ["Хочу снять квартиру на год, с коммунальными", "Залог возвращается при выезде?"]),
                  T("Fix the price.", ["forty thousand with bills", "deposit one month"],
                    ["Сорок тысяч с коммунальными", "Залог — одна оплата"]),
              ])),
            L("Соседи и правила",
              "Neighbour rules are said with нельзя + imperfective infinitive and с + "
              "genitive for the hour: после одиннадцати нельзя шуметь. Договориться с + "
              "instrumental is the verb of every staircase conversation, and приходится + "
              "infinitive admits an unwanted necessity.",
              [V("сосед", "sah-SYEHD", "neighbour", "noun"),
               V("шум", "shoom", "noise", "noun"),
               V("тишина", "tee-shee-NAH", "quiet, silence", "noun"),
               V("договориться", "dah-gah-vah-REE-t-syah", "to come to an agreement", "verb"),
               V("приходится", "pree-KHOH-deet-syah", "one has to", "verb")],
              G("Правила подъезда",
                "после одиннадцати нельзя шуметь · договориться с соседями · приходится терпеть",
                "Нельзя + imperfective infinitive states a rule without a subject: здесь "
                "нельзя курить, после одиннадцати нельзя шуметь. Договориться с + "
                "instrumental is how a compromise is reached. Приходится + infinitive "
                "reports what you do not want to do but must — the honest verb of shared "
                "buildings.",
                [X("После одиннадцати нельзя шуметь.", "POH-slyeh ah-DEE-nahd-tsahty nehl-ZYAH shoo-MYETY.", "After eleven you must not make noise."),
                X("Мы договорились с соседями о ремонте.", "mih dah-gah-vah-REE-lees s sah-SYEH-dyah-mee ah ree-MOHN-teh.", "We came to an agreement with the neighbours about the repairs."),
                X("Приходится терпеть: дом старый, стены тонкие.", "pree-KHOH-deet-syah teer-PYETY: dohm STAH-rihy, STYEH-nih TOHN-kee-yeh.", "One has to put up with it: the building is old, the walls thin.")],
                [("После одиннадцати нельзя шумишь.", "После одиннадцати нельзя шуметь.", "Нельзя takes the infinitive, never a personal form."),
                 ("Договориться о соседях.", "Договориться с соседями.", "The other party takes с + instrumental.")]),
              [D("Жилец", "У вас тут шумно вечером?", "oo vahs toot SHoom-nah VYEH-cheh-rahm?", "Is it noisy here in the evening?"),
               D("Соседка", "После одиннадцати нельзя шуметь — мы договорились.", "POH-slyeh ah-DEE-nahd-tsahty nehl-ZYAH shoo-MYETY — mih dah-gah-vah-REE-lees.", "After eleven you mustn't make noise — we agreed."),
               D("Жилец", "А ремонт?", "ah ree-MOHNt?", "And repairs?"),
               D("Соседка", "Ремонт только днём. Иначе приходится идти и говорить.", "ree-MOHNt TOHL-kah dnyohm. ee-NAH-cheh pree-KHOH-deet-syah ee-TEE ee gah-vah-REETY.", "Repairs only in the daytime. Otherwise you have to go and talk.")],
              WS("Neighbours worksheet", [
                  T("State the rule.", ["after eleven you must not make noise", "you mustn't smoke here"],
                    ["После одиннадцати нельзя шуметь", "Здесь нельзя курить"]),
                  T("Report the compromise.", ["we came to an agreement with the neighbours", "one has to put up with it"],
                    ["Мы договорились с соседями", "Приходится терпеть"]),
              ])),
        ]},
        {"id": "B1+-U2", "title": "Работа и учёба", "lessons": [
            L("Работа и график",
              "A working week is described with по + dative: работаю по графику, по сменам. "
              "Смена is the shift, отпуск the paid leave, and совещание the meeting. В "
              "отпуске and на работе place the person, and с … до … marks the hours.",
              [V("график", "GRAH-feek", "schedule, rota", "noun"),
               V("смена", "SMYEH-nah", "shift", "noun"),
               V("отпуск", "OHT-poosk", "leave, holiday", "noun"),
               V("совещание", "sah-veh-SHCHAH-nee-yeh", "meeting, conference", "noun"),
               V("начальник", "nah-CHAHL-neek", "boss", "noun")],
              G("График и смены",
                "работать по графику / по сменам · в отпуске · с девяти до шести",
                "По + dative marks a pattern of work: по графику, по сменам, по выходным. "
                "Location takes the prepositional — на работе, в отпуске, на совещании. The "
                "hours are с … до … with the genitive, and договориться об отпуске takes the "
                "prepositional: об отпуске с начальником.",
                [X("Я работаю по графику, две смены в неделю.", "yah rah-BOH-tah-yoo pah GRAH-fee-koo, dveh SMYEH-nih v nee-DYEH-lyoo.", "I work to a rota, two shifts a week."),
                X("Он сейчас в отпуске до двадцатого.", "ohn see-CHAHs v OHT-poos-kyeh dah dvahts-tsah-TAH-vah.", "He is on leave until the twentieth."),
                X("Совещание с девяти до десяти.", "sah-veh-SHCHAH-nee-yeh s dee-see-TEE dah dee-see-TEE.", "The meeting is from nine to ten.")],
                [("Я работаю на график.", "Я работаю по графику.", "A pattern takes по + dative."),
                 ("Он в отпуск до двадцатого.", "Он в отпуске до двадцатого.", "Being on leave is в отпуске.")]),
              [D("Коллега", "Ты в отпуске с какого?", "tih v OHT-poos-kyeh s kah-KOH-vah?", "When does your leave start?"),
               D("Иван", "С пятнадцатого. До этого работаю по сменам.", "s peet-NAHd-tsah-tah-vah. dah EH-tah-vah rah-BOH-tah-yoo pah SMYEH-nahm.", "From the fifteenth. Until then I work shifts."),
               D("Коллега", "А совещание сегодня?", "ah sah-veh-SHCHAH-nee-yeh see-VOHD-nyah?", "And is the meeting today?"),
               D("Иван", "Да, с девяти до десяти. Потом — смена.", "dah, s dee-see-TEE dah dee-see-TEE. pah-TOHM — SMYEH-nah.", "Yes, from nine to ten. Then my shift.")],
              WS("Work schedule worksheet", [
                  T("Describe the pattern.", ["I work to a rota, two shifts a week", "he is on leave until the twentieth"],
                    ["Я работаю по графику, две смены в неделю", "Он в отпуске до двадцатого"]),
                  T("Place the hours.", ["the meeting is from nine to ten", "then my shift"],
                    ["Совещание с девяти до десяти", "Потом смена"]),
              ])),
            L("Резюме и собеседование",
              "A CV is a резюме, and the interview asks about опыт and навыки. Have and not "
              "have take the same patterns as everywhere: у меня есть опыт, у меня нет опыта "
              "работы. Уметь + infinitive names what you can do, and a project is described "
              "with над + instrumental: работал над проектом.",
              [V("резюме", "ree-zoo-MEH", "CV, résumé", "noun"),
               V("опыт", "OH-piht", "experience", "noun"),
               V("навык", "NAH-vihk", "skill", "noun"),
               V("вакансия", "vah-KAHN-see-yah", "vacancy", "noun"),
               V("собеседование", "sah-bee-SYEH-dah-vah-nee-yeh", "job interview", "noun")],
              G("Опыт и навыки",
                "у меня есть опыт + genitive · умею + infinitive · работал над проектом · три года опыта",
                "Experience is counted in years with the genitive after нет and two: два "
                "года опыта, five лет. Умею + infinitive reports a skill: умею работать с "
                "данными. Над + instrumental names the object of a project: работал над "
                "сайтом. На собеседовании the questions are расскажите о себе and почему вы "
                "уходите?.",
                [X("У меня три года опыта в продажах.", "oo meh-NYAH tree GOH-dah OH-pih-tah v prah-DAH-zhahkh.", "I have three years of experience in sales."),
                X("Умею работать с таблицами и отчётами.", "oo-MYEH-yoo rah-BOH-tahty s tahb-LEE-tsah-mee ee aht-CHOH-tah-mee.", "I can work with spreadsheets and reports."),
                X("Работал над проектом автоматизации.", "rah-BOH-tahl nahd prah-YEHk-tahm ahf-tah-mah-tee-ZAH-tsee-ee.", "I worked on an automation project.")],
                [("У меня опыт три года работы.", "У меня три года опыта.", "The count comes first, опыта after it in the genitive."),
                 ("Работал в проекте.", "Работал над проектом.", "Работать над + instrumental for a project.")]),
              [D("Интервьюер", "Расскажите о себе.", "rahs-kah-ZHEE-teh ah see-BYEH.", "Tell me about yourself."),
               D("Кандидат", "Пять лет опыта, работал над двумя проектами.", "pyahty lyet OH-pih-tah, rah-BOH-tahl nahd dvoom-YAH prah-YEHk-tah-mee.", "Five years of experience, I worked on two projects."),
               D("Интервьюер", "Какие навыки для вакансии?", "kah-KEE-yeh NAH-vih-kee dlyah vah-KAHN-see-ee?", "Which skills for this vacancy?"),
               D("Кандидат", "Умею анализировать данные и писать отчёты.", "oo-MYEH-yoo ah-nah-lee-ZEE-rah-ty DAHN-nih-yeh ee pee-SAHTY aht-CHOH-tih.", "I can analyse data and write reports.")],
              WS("CV worksheet", [
                  T("Present the experience.", ["I have three years of experience in sales", "I worked on an automation project"],
                    ["У меня три года опыта в продажах", "Работал над проектом автоматизации"]),
                  T("Name the skills.", ["I can work with spreadsheets and reports", "I can analyse data and write reports"],
                    ["Умею работать с таблицами и отчётами", "Умею анализировать данные и писать отчёты"]),
              ])),
            L("Учёба: сессия и экзамен",
              "The examination season is сессия, and its verbs come in aspect pairs: сдавать "
              "(to take, repeatedly) and сдать (to pass). Готовиться к + dative is to prepare "
              "for, and конспект is the summary you study from. Пересдача is the retake — one "
              "word that every student recognises immediately.",
              [V("зачёт", "zah-CHOHT", "credit test", "noun"),
               V("экзамен", "ehk-ZAH-mehn", "exam", "noun"),
               V("конспект", "kahn-SPYEHKT", "lecture notes", "noun"),
               V("сессия", "SYEH-see-yah", "examination period", "noun"),
               V("пересдача", "pee-ree-SDAH-chah", "retake", "noun")],
              G("Сдать экзамен",
                "готовиться к + dative · сдавать / сдать экзамен · на тройку · пересдача",
                "The aspect pair does the work: сдавать is the process (я сдаю экзамен "
                "завтра), сдать the result (я сдал экзамен). Готовиться к + dative names "
                "the subject: готовиться к истории. The mark is said with на: сдать на "
                "пятёрку. Не сдал means failed, and пересдача follows it.",
                [X("Я готовлюсь к экзамену по истории.", "yah gah-TOHF-lyoosy k ehk-ZAH-meh-noo pah ees-TOH-ree-ee.", "I am preparing for the history exam."),
                X("Она сдала зачёт на пять.", "ah-NAH SDAH-lah zah-CHOHT nah pyahty.", "She passed the credit test with a five."),
                X("Он не сдал, у него пересдача в июне.", "ohn nee ZDAHL, oo nee-VOH pee-ree-SDAH-chah v ee-YOO-nyeh.", "He failed, and his retake is in June.")],
                [("Готовиться для экзамена.", "Готовиться к экзамену.", "Готовиться к + dative."),
                 ("Она сдавать зачёт.", "Она сдала зачёт.", "A finished result takes the perfective сдала.")]),
              [D("Сокурсник", "Ты готовишься к зачёту?", "tih gah-TOHF-veesh-syah k zah-CHOH-too?", "Are you preparing for the credit test?"),
               D("Студентка", "Готовлюсь по конспекту, но сложно.", "gah-TOHV-lyoosy pah kahn-SPYEHk-too, noh SLOZH-nah.", "I'm preparing from the notes, but it's hard."),
               D("Сокурсник", "Я в прошлом году не сдал, была пересдача.", "yah f PROHSH-lahm gah-DOO nee ZDAHL, bih-LAH pee-ree-SDAH-chah.", "Last year I failed, and there was a retake."),
               D("Студентка", "Надеюсь сдать на пять с первого раза.", "nah-DYEH-yoosy zdahty nah pyahty s PYER-vah-vah RAH-zah.", "I hope to pass with a five first time.")],
              WS("Exam worksheet", [
                  T("Describe the preparation.", ["I am preparing for the history exam", "I'm preparing from the notes"],
                    ["Я готовлюсь к экзамену по истории", "Готовлюсь по конспекту"]),
                  T("Report the result.", ["she passed the credit test with a five", "he failed, his retake is in June"],
                    ["Она сдала зачёт на пять", "Он не сдал, у него пересдача в июне"]),
              ])),
        ]},
        {"id": "B1+-U3", "title": "Мнение и спор", "lessons": [
            L("Согласие и несогласие",
              "Agreement takes с + instrumental: я согласен с вами, я не согласен с этим. "
              "Согласен agrees in gender: согласен / согласна. Возразить (to object) is its "
              "polite opposite, точка зрения is the point of view, and по-моему opens a "
              "personal opinion without a fight.",
              [V("согласен", "sah-GLAH-sehn", "agreeing (m)", "adjective"),
               V("возразить", "vahz-rah-ZEETY", "to object", "verb"),
               V("точка зрения", "TOHCH-kah ZRYEH-nee-yah", "point of view", "noun"),
               V("спор", "spohr", "argument, dispute", "noun"),
               V("по-моему", "pah-MOH-yeh-moo", "in my opinion", "adverb")],
              G("Я согласен с …",
                "согласен с + instrumental · возразить против + genitive · по-моему · с одной стороны",
                "Согласен takes с + instrumental for the person or the idea: согласен с "
                "вами, согласен с решением. Возразить takes против + genitive when the "
                "objection is named in full, and a bare возразить without a preposition is "
                "the short form. По-моему and на мой взгляд open an opinion; с одной стороны "
                "… с другой стороны keeps it discussable.",
                [X("Я согласен с вами в главном.", "yah sah-GLAH-sehn s VAH-mee v GLAHV-nahm.", "I agree with you on the main point."),
                X("Не согласна с этим выводом.", "nee sah-GLAHS-nah s EH-teem VIH-vah-dahm.", "I don't agree with that conclusion."),
                X("По-моему, возразить здесь нечего.", "pah-MOH-yeh-moo, vahz-rah-ZEETY zdyehsy NYEH-cheh-vah.", "In my opinion, there is nothing to object to here.")],
                [("Я согласен вас.", "Я согласен с вами.", "Согласен takes с + instrumental."),
                 ("Я не согласна этот вывод.", "Я не согласна с этим выводом.", "The object of agreement stands in the instrumental after с.")]),
              [D("Коллега", "Вы согласны с решением?", "vih sah-GLAHS-nih s ree-SHEH-nee-yem?", "Do you agree with the decision?"),
               D("Юрист", "Согласна в главном, но возражаю против срока.", "sah-GLAHS-nah v GLAHV-nahm, noh vahz-rah-ZHAH-yoo PROH-teef SROH-kah.", "I agree on the main point, but I object to the deadline."),
               D("Коллега", "Что предлагаете?", "shtoh preed-lah-GAH-yeh-teh?", "What do you propose?"),
               D("Юрист", "По-моему, срок надо обсудить отдельно.", "pah-MOH-yeh-moo, srohk NAH-dah ahb-soo-DEETY aht-DYEHl-nah.", "In my opinion the deadline should be discussed separately.")],
              WS("Agreement worksheet", [
                  T("Agree and object.", ["I agree with you on the main point", "I object to the deadline"],
                    ["Я согласен с вами в главном", "Я возражаю против срока"]),
                  T("Open an opinion.", ["in my opinion, the deadline should be discussed separately", "there is nothing to object to here"],
                    ["По-моему, срок надо обсудить отдельно", "Возразить здесь нечего"]),
              ])),
            L("Новости и обсуждение",
              "The news is reported with по данным + genitive (по данным исследования) and "
              "with ссылаться на + accusative (ссылаются на источник). Обсуждать takes the "
              "accusative: обсуждать новость. Источник, факт and мнение are kept apart "
              "deliberately — источник is where the claim comes from, факт is what can be "
              "checked.",
              [V("новость", "NOH-vahsty", "piece of news", "noun"),
               V("источник", "ees-TOHCH-neek", "source", "noun"),
               V("факт", "fahkt", "fact", "noun"),
               V("мнение", "MYEH-nee-yeh", "opinion", "noun"),
               V("обсуждать", "ahb-soo-ZHDAHTY", "to discuss", "verb")],
              G("По данным и по мнению",
                "по данным + genitive · по мнению + genitive · ссылаться на + accusative · обсуждать что",
                "По данным исследования and по мнению автора mark where a claim comes from; "
                "the first is evidence, the second opinion. Ссылаться на + accusative names "
                "the reference openly. Обсуждать takes the accusative, while говорить о + "
                "prepositional introduces the topic: мы обсуждали отчёт, мы говорили об "
                "отчёте.",
                [X("По данным исследования, цены выросли.", "pah DAHN-nihm ees-SLYEH-dah-vah-nee-yah, TSEH-nih VIH-rahs-lee.", "According to the research data, prices rose."),
                X("По мнению автора, причина в логистике.", "pah MYEH-nee-yoo AHf-tah-rah, pree-CHEE-nah v lah-GEES-tee-keh.", "In the author's opinion, the cause is logistics."),
                X("Он ссылается на отчёт, а не на факт.", "ohn SSEE-lah-yeht-syah nah aht-CHOHT, ah nee nah fahkt.", "He refers to a report, not to a fact.")],
                [("По данным исследования показывают рост.", "По данным исследования, цены выросли.", "По данным is an adverbial; the sentence still needs its own subject and verb."),
                 ("Мы обсуждали об отчёте.", "Мы обсуждали отчёт.", "Обсуждать takes the accusative.")]),
              [D("Редактор", "Откуда эти цифры?", "aht-KOO-dah EH-tee TSIH-frih?", "Where do these figures come from?"),
               D("Автор", "По данным исследования, опубликованного в мае.", "pah DAHN-nihm ees-SLYEH-dah-vah-nee-yah, ah-poo-plee-KOH-vah-nah-vah v MAH-yeh.", "According to the research published in May."),
               D("Редактор", "А мнение здесь есть?", "ah MYEH-nee-yeh zdyehsy yehsty?", "And is there an opinion here?"),
               D("Автор", "В последнем абзаце, и я ссылаюсь на автора статьи.", "v pah-SLYEHd-nyem ahb-ZAHTS-eh, ee yah SSEE-lah-yoosy nah AHf-tah-rah stah-TYEE.", "In the last paragraph, and I refer to the author of the article.")],
              WS("News worksheet", [
                  T("Attribute the claim.", ["according to the research data, prices rose", "in the author's opinion the cause is logistics"],
                    ["По данным исследования, цены выросли", "По мнению автора, причина в логистике"]),
                  T("Keep fact and opinion apart.", ["he refers to a report, not to a fact", "we discussed the report"],
                    ["Он ссылается на отчёт, а не на факт", "Мы обсуждали отчёт"]),
              ])),
            L("Сравнение городов и стран",
              "Cities are compared with чем and по сравнению с + instrumental: Москва дороже "
              "Казани; по сравнению с Казанью, Москва дороже. Уровень жизни, климат, "
              "стоимость and транспорт are the four categories the comparison runs on, and "
              "преимущество names the winner without superlatives.",
              [V("сравнение", "srahv-NYEH-nee-yeh", "comparison", "noun"),
               V("уровень", "OO-rah-veen", "level", "noun"),
               V("климат", "KLEE-maht", "climate", "noun"),
               V("стоимость", "STOH-ee-mahsty", "cost", "noun"),
               V("преимущество", "pree-EEM-oo-shcheh-stvah", "advantage", "noun")],
              G("По сравнению с …",
                "дороже / дешевле + genitive or чем · по сравнению с + instrumental · уровень жизни выше",
                "The second term of a comparison is either чем + nominative or the genitive "
                "alone: Москва дороже, чем Казань = Москва дороже Казани. По сравнению с + "
                "instrumental frames the whole comparison (по сравнению с прошлым годом). "
                "Уровень is masculine and takes выше / ниже: уровень жизни ниже, цены выше.",
                [X("По сравнению с прошлым годом, аренда выросла.", "pah srahv-NYEH-nee-yoo s PROHSH-lihm GOH-dahm, ah-RYEHN-dah VIH-rahs-lah.", "Compared with last year, rent has risen."),
                X("В Казани цены ниже, чем в Москве.", "v kah-zah-NEE TSEH-nih NEE-zheh, chem v mahsk-VYEH.", "In Kazan prices are lower than in Moscow."),
                X("Преимущество города — транспорт, недостаток — климат.", "pree-EEM-oo-shcheh-stvah GOH-rah-dah — TRAHNS-pahrt, nee-dah-STAH-tahk — KLEE-maht.", "The city's advantage is transport, its shortcoming the climate.")],
                [("По сравнению Казани, Москва дороже.", "По сравнению с Казанью, Москва дороже.", "По сравнению с + instrumental."),
                 ("Цены ниже чем в Москве дешевле.", "В Казани цены ниже, чем в Москве.", "One comparison per sentence.")]),
              [D("Друг", "Где лучше жить — в Москве или в Казани?", "gdyeh LOOT-sheh ZHEETY — v mahsk-VYEH EE-lee v kah-zah-NEE?", "Where is it better to live — in Moscow or Kazan?"),
               D("Иван", "По сравнению с Москвой, в Казани дешевле.", "pah srahv-NYEH-nee-yoo s mahsk-VOY, v kah-zah-NEE deh-SHEHV-lyeh.", "Compared with Moscow, Kazan is cheaper."),
               D("Друг", "А что ещё?", "ah shtoh yeh-SHCHOH?", "And what else?"),
               D("Иван", "Уровень жизни похож, но преимущество Москвы — работа.", "OO-rah-veen ZHEEZ-nee pah-KHOHZH, noh pree-EEM-oo-shcheh-stvah mahsk-VIH — rah-BOH-tah.", "The standard of living is similar, but Moscow's advantage is work.")],
              WS("Comparison worksheet", [
                  T("Compare two cities.", ["compared with Moscow, Kazan is cheaper", "in Kazan prices are lower than in Moscow"],
                    ["По сравнению с Москвой, в Казани дешевле", "В Казани цены ниже, чем в Москве"]),
                  T("Name the advantages.", ["the city's advantage is transport, its shortcoming the climate", "the standard of living is similar"],
                    ["Преимущество города — транспорт, недостаток — климат", "Уровень жизни похож"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Транссибирская магистраль — 9289 километров от Москвы до Владивостока, семь "
                 "часовых поясов и шесть суток пути. Она строилась с 1891 года и до сих пор "
                 "остаётся самым наглядным ответом на вопрос «насколько большая страна»: "
                 "поезд идёт через Урал, Сибирь и Байкал, а пассажиры в плацкарте успевают "
                 "перезнакомиться, потому что деваться некуда. Для русского языка расстояние "
                 "измеряется не километрами, а сутками: «до Иркутска трое суток»."),
        source_url="https://en.wikipedia.org/wiki/Trans-Siberian_Railway",
        reading=("Мой брат работает по сменам на железной дороге. Он говорит, что расстояние "
                 "здесь считают не километрами, а сутками: до Иркутска — трое суток, до "
                 "Владивостока — шесть. В прошлом году он сдал экзамен на машиниста и теперь "
                 "работает на длинных маршрутах. Мы часто обсуждаем, что важнее: уровень "
                 "жизни в городе или дорога, которая тебе нравится. По-моему, второе, но он "
                 "со мной не согласен."),
        reading_gloss=("My brother works shifts on the railway. He says that here distance is "
                       "counted not in kilometres but in days: three days to Irkutsk, six to "
                       "Vladivostok. Last year he passed the exam to become a train driver "
                       "and now works on long routes. We often discuss what matters more: the "
                       "standard of living in a city or the road you like. In my opinion the "
                       "second, but he doesn't agree with me."),
        listening=("По данным исследования, разница в аренде между Москвой и Казанью — почти "
                   "два раза. — А по сравнению с прошлым годом? — Выросло везде, но в "
                   "Казани меньше."),
        listening_gloss=("According to the research data, the difference in rent between "
                         "Moscow and Kazan is almost double. — And compared with last year? — "
                         "It has risen everywhere, but less in Kazan."),
        voice_tag=VOICE,
        idioms=[
            ("по сменам", "by shifts", "working a rotating rota"),
            ("на длинных маршрутах", "on long routes", "working long-distance"),
            ("считать сутками", "to count in days", "to measure distance in travel time"),
            ("не согласен в корне", "to disagree at the root", "to disagree fundamentally"),
            ("точка зрения", "point of view", "an opinion on a matter"),
            ("смотреть на вещи трезво", "to look at things soberly", "to stay realistic"),
            ("держать слово", "to keep one's word", "to do what one promised"),
            ("ставить на первое место", "to put in first place", "to rank above everything"),
            ("иметь в виду", "to have in mind", "to mean, to keep in view"),
            ("сводить концы с концами", "to bring ends together", "to make ends meet"),
        ],
        mistakes=[
            ("Я согласен вас в этом.", "Я согласен с вами в этом.", "Согласен takes с + instrumental."),
            ("По сравнению Казани, Москва дороже.", "По сравнению с Казанью, Москва дороже.", "По сравнению с + instrumental."),
            ("Мы обсуждали об отчёте.", "Мы обсуждали отчёт.", "Обсуждать takes the accusative; говорить о takes the prepositional."),
        ],
        task_title="Спор с аргументом",
        task_instructions=("Write a discussion of six to eight lines on one question about "
                           "city life: state your position with по-моему, attribute one "
                           "claim with по данным or ссылаться на, concede one point with "
                           "согласен в главном, но, and name one advantage and one "
                           "shortcoming. Then read it aloud and check the cases: с + "
                           "instrumental after согласен, против + genitive после возражаю, "
                           "по сравнению с + instrumental."),
    ),
    "test": [
        ("translate_en", "Say: I agree with you on the main point.", "Я согласен с вами в главном."),
        ("translate_ru", "По данным исследования, цены выросли.", "According to the research data, prices rose."),
        ("multiple_choice", "Which sentence states a house rule?", "После одиннадцати нельзя шуметь."),
        ("fill_in_the_blank", "Аптека рядом ___ домом.", "с"),
        ("word_selection", "Select the Russian for 'deposit (rental)'.", "залог"),
        ("error_correction", "Мы обсуждали об отчёте.", "Мы обсуждали отчёт."),
        ("dialogue_completion", "Complete: Ты готовишься к зачёту? — ___ (I'm preparing from the notes)", "Готовлюсь по конспекту"),
        ("matching", "Match собеседование to its meaning.", "job interview"),
        ("reading_comprehension", "В тексте, сколько суток до Владивостока?", "six"),
        ("inference", "Брат говорит, что расстояние считают сутками. What does that tell us about how people plan journeys?", "they think in travel time, not kilometres"),
        ("main_idea", "В тексте рассказано о работе на железной дороге и о споре. — what is this sentence?", "the main point of the reading"),
        ("detail_identification", "На кого брат сдал экзамен?", "train driver"),
    ],
}

HALFSTEPS["B2+"] = {
    "native": NATIVE,
    "title": "%s B2+ — Документы, экономика и наука" % NAME,
    "goals": [
        "Deal with official institutions: applications, deadlines, refusals and interviews",
        "Read and discuss the economy: budgets, prices, the labour market and taxes",
        "Follow research and technology arguments and take part in them",
    ],
    "units": [
        {"id": "B2+-U1", "title": "Официальная жизнь", "lessons": [
            L("Документы и ведомства",
              "Official life runs on three verbs: обратиться в + accusative (to apply to a "
              "body), подать документы (to submit) and получить + accusative (to receive). "
              "Справка о + prepositional names the certificate's subject: справка о доходах. "
              "Приёмные часы are the hours the office actually accepts people.",
              [V("документ", "dah-koo-MYEHNT", "document", "noun"),
               V("ведомство", "VYEH-dahm-stvah", "government body", "noun"),
               V("обратиться", "ahb-rah-TEET-syah", "to apply, to address", "verb"),
               V("приём", "pree-YOHM", "reception, appointment", "noun"),
               V("справка", "SPRAHF-kah", "certificate", "noun")],
              G("Куда обратиться",
                "обратиться в + accusative · подать документы · справка о + prepositional · приёмные часы",
                "Обратиться в takes the accusative of the institution (обратитесь в "
                "ведомство), обратиться к — the dative of a person. Подать takes the "
                "accusative: подать заявление, подать документы. Справка takes о + "
                "prepositional for its subject: справка о доходах, справка о составе семьи. "
                "The office's hours are приёмные часы, and the queue is очередь.",
                [X("Куда обратиться за справкой?", "koo-DAH ahb-rah-TEET-syah zah SPRAHF-koy?", "Where do I apply for a certificate?"),
                X("Подайте документы в приёмные часы.", "pah-DAY-teh dah-koo-MYEHN-tih v pree-YOHM-nih-yeh chah-SIH.", "Submit the documents during reception hours."),
                X("Нужна справка о доходах за год.", "noozh-NAH SPRAHF-kah ah dah-KHOH-dahkh zah goht.", "A certificate of income for the year is needed.")],
                [("Обратитесь к ведомство.", "Обратитесь в ведомство.", "An institution takes в + accusative."),
                 ("Справка про доходах.", "Справка о доходах.", "Справка takes о + prepositional.")]),
              [D("Посетитель", "Куда обратиться за справкой?", "koo-DAH ahb-rah-TEET-syah zah SPRAHF-koy?", "Where do I apply for a certificate?"),
               D("Секретарь", "Второй этаж, приём с двух до пяти.", "ftah-ROY eh-TAHSH, pree-YOHM s DVOOKH dah pee-TEE.", "Second floor, reception from two to five."),
               D("Посетитель", "Какие документы нужны?", "kah-KEE-yeh dah-koo-MYEHN-tih noozh-NIH?", "Which documents are needed?"),
               D("Секретарь", "Заявление и паспорт. Справка будет через три дня.", "zah-yahv-LYEH-nee-yeh ee PAHS-pahrt. SPRAHF-kah BOO-deht CHEH-rez tree dnyah.", "An application and a passport. The certificate will be ready in three days.")],
              WS("Documents worksheet", [
                  T("Ask where to apply.", ["where do I apply for a certificate?", "which documents are needed?"],
                    ["Куда обратиться за справкой?", "Какие документы нужны?"]),
                  T("Name the certificate.", ["a certificate of income for the year", "an application and a passport"],
                    ["Справка о доходах за год", "Заявление и паспорт"]),
              ])),
            L("Сроки и отказ",
              "Deadlines are said with в течение + genitive (в течение месяца) and the "
              "decision with на основании + genitive (на основании закона). A refusal is "
              "отказ, to refuse is отказать в + prepositional, and to appeal is обжаловать + "
              "accusative: обжаловать отказ в течение десяти дней.",
              [V("срок", "srohk", "deadline, term", "noun"),
               V("отказ", "aht-KAHS", "refusal", "noun"),
               V("обжаловать", "ahb-ZHAH-lah-vahty", "to appeal", "verb"),
               V("основание", "ahs-nah-VAH-nee-yeh", "ground, basis", "noun"),
               V("уведомление", "oo-veh-dahm-LYEH-nee-yeh", "notification", "noun")],
              G("Сроки, отказ и обжалование",
                "в течение + genitive · на основании + genitive · отказать в + prepositional · обжаловать отказ",
                "В течение + genitive measures the period (в течение тридцати дней), and "
                "на основании + genitive names the legal ground (на основании статьи). "
                "Отказать takes в + prepositional: отказать в выдаче. Обжаловать takes the "
                "accusative directly, and the notification of the decision is уведомление, "
                "which arrives whether or not the answer is yes.",
                [X("Решение принимается в течение тридцати дней.", "ree-SHEH-nee-yeh pree-nee-MAH-yeht-syah v tee-CHEH-nee-yeh treed-tsah-TEE dnyey.", "The decision is taken within thirty days."),
                X("Отказали в выдаче справки.", "aht-kah-ZAH-lee v VIH-dah-cheh SPRAHF-kee.", "They refused to issue the certificate."),
                X("Отказ можно обжаловать на основании закона.", "aht-KAHS MOHZH-nah ahb-ZHAH-lah-vahty nah ahs-nah-VAH-nee-ee zah-KOH-nah.", "The refusal can be appealed on the basis of the law.")],
                [("В течение месяца делают решение.", "Решение принимают в течение месяца.", "В течение names the period; the sentence needs its own verb."),
                 ("Отказали на выдачу.", "Отказали в выдаче.", "Отказать takes в + prepositional.")]),
              [D("Клиент", "Когда будет ответ?", "kahg-DAH BOO-deht aht-VYEHT?", "When will there be an answer?"),
               D("Инспектор", "В течение тридцати дней придёт уведомление.", "v tee-CHEH-nee-yeh treed-tsah-TEE dnyey pree-DYOHT oo-veh-dahm-LYEH-nee-yeh.", "A notification will come within thirty days."),
               D("Клиент", "А если отказ?", "ah YEH-slee aht-KAHS?", "And if it is a refusal?"),
               D("Инспектор", "Тогда обжалуйте на основании закона — срок десять дней.", "tahg-DAH ahb-ZHAH-loo-ee-teh nah ahs-nah-VAH-nee-ee zah-KOH-nah — srohk DYEH-seety dnyey.", "Then appeal on the basis of the law — the term is ten days.")],
              WS("Deadlines worksheet", [
                  T("Name the period and the ground.", ["the decision is taken within thirty days", "the refusal can be appealed on the basis of the law"],
                    ["Решение принимается в течение тридцати дней", "Отказ можно обжаловать на основании закона"]),
                  T("Report the refusal.", ["they refused to issue the certificate", "a notification will come"],
                    ["Отказали в выдаче справки", "Придёт уведомление"]),
              ])),
            L("Интервью с чиновником",
              "An official interview is built from компетенция, регламент and поручение. In "
              "пределах компетенции keeps the speaker inside their remit; нести "
              "ответственность за + accusative assigns it; согласно регламенту + dative "
              "names the rule. Отчитаться о + prepositional closes the loop, and отчёт о "
              "работе is the document.",
              [V("компетенция", "kahm-pee-TYEHN-tsee-yah", "remit, competence", "noun"),
               V("регламент", "ree-GLAH-mehnt", "regulation, procedure", "noun"),
               V("поручение", "pah-roo-CHYEH-nee-yeh", "assignment, instruction", "noun"),
               V("ответственность", "aht-VYEHT-stveh-nahsty", "responsibility", "noun"),
               V("отчитываться", "aht-CHEE-tih-vah-t-syah", "to report back", "verb")],
              G("В пределах компетенции",
                "в пределах + genitive · нести ответственность за + accusative · согласно + dative · отчитаться о + prepositional",
                "В пределах компетенции bounds the claim: в пределах компетенции ведомства. "
                "Нести ответственность за takes the accusative for what one answers for. "
                "Согласно takes the dative (согласно регламенту) — that is the whole reason "
                "the case matters. Отчитаться о + prepositional and отчёт о работе are the "
                "same construction.",
                [X("В пределах компетенции ведомства это решение.", "v pree-DYEH-lahkh kahm-pee-TYEHN-tsee-ee VYEH-dahm-stvah EH-tah ree-SHEH-nee-yeh.", "Within the remit of the body, this is the decision."),
                X("Согласно регламенту, срок — тридцать дней.", "sah-GLAHS-nah ree-GLAH-mehn-too, srohk — TREEts-tsahty dnyey.", "According to the regulation, the term is thirty days."),
                X("Мы отчитываемся о работе раз в год.", "mih aht-CHEE-tih-vah-yehm-syah ah rah-BOH-tyeh rahz v goht.", "We report on the work once a year.")],
                [("Согласно регламента, срок тридцать дней.", "Согласно регламенту, срок — тридцать дней.", "Согласно takes the dative."),
                 ("Нести ответственность за работа.", "Нести ответственность за работу.", "За takes the accusative here.")]),
              [D("Журналист", "Кто отвечает за сроки?", "ktoh aht-veh-CHAH-yeht zah SROH-kee?", "Who is responsible for the deadlines?"),
               D("Чиновник", "Ведомство несёт ответственность за срок в пределах компетенции.", "VYEH-dahm-stvah nee-SYOHT aht-VYEHT-stveh-nahsty zah srohk v pree-DYEH-lahkh kahm-pee-TYEHN-tsee-ee.", "The body is responsible for the deadline within its remit."),
               D("Журналист", "И когда будет отчёт?", "ee kahg-DAH BOO-deht aht-CHOHT?", "And when will the report be?"),
               D("Чиновник", "Согласно регламенту, отчёт публикуется раз в год.", "sah-GLAHS-nah ree-GLAH-mehn-too, aht-CHOHT poob-lee-KOO-yeht-syah rahz v goht.", "According to the regulation, the report is published once a year.")],
              WS("Official interview worksheet", [
                  T("Bound the claim.", ["within the remit of the body, this is the decision", "according to the regulation, the term is thirty days"],
                    ["В пределах компетенции ведомства это решение", "Согласно регламенту, срок — тридцать дней"]),
                  T("Assign responsibility.", ["the body is responsible for the deadline", "we report on the work once a year"],
                    ["Ведомство несёт ответственность за срок", "Мы отчитываемся о работе раз в год"]),
              ])),
        ]},
        {"id": "B2+-U2", "title": "Экономика и быт", "lessons": [
            L("Бюджет и цены",
              "Economic change is reported with prepositions: рост на + accusative, снижение "
              "+ genitive, вырасти в два раза. Бюджет, доход, расход and сбережения are the "
              "four household nouns, and they work for the state too. Цены на + accusative "
              "names what got more expensive: цены на жильё выросли.",
              [V("бюджет", "byoo-DZHEHT", "budget", "noun"),
               V("инфляция", "een-FLYAH-tsee-yah", "inflation", "noun"),
               V("доход", "dah-KHOHT", "income", "noun"),
               V("расход", "rahs-KHOHT", "expenditure", "noun"),
               V("сбережения", "sbeh-ree-ZHEH-nee-yah", "savings", "noun")],
              G("Рост и снижение",
                "рост на + accusative · снижение + genitive · цены на + accusative · вырасти в два раза",
                "Рост takes на + accusative for the amount (рост на десять процентов) and "
                "the thing that grew in the genitive (рост цен). Снижение works the same way. "
                "Цены на takes the accusative for the category: цены на продукты. Вырасти в "
                "два раза doubles, and упасть на четверть falls by a quarter.",
                [X("Рост цен на жильё составил десять процентов.", "rohst tsehn nah zhee-LYOH sah-stah-VEEL DYEH-seety prah-TSEHN-tahf.", "The rise in housing prices was ten per cent."),
                X("Цены на продукты выросли в два раза.", "TSEH-nih nah prah-DOOK-tih VIH-rahs-lee v dvah RAH-zah.", "Food prices doubled."),
                X("Доходы выросли, но сбережения не изменились.", "dah-KHOH-dih VIH-rahs-lee, noh sbeh-ree-ZHEH-nee-yah nee eez-mee-NEE-lees.", "Incomes rose, but savings did not change.")],
                [("Рост цен на десять процентов продуктов.", "Рост цен на продукты составил десять процентов.", "The category and the amount take different constructions."),
                 ("Цены выросли на два раза.", "Цены выросли в два раза.", "Doubling takes в + accusative.")]),
              [D("Аналитик", "Как изменились цены?", "kahk eez-mee-NEE-lees TSEH-nih?", "How have prices changed?"),
               D("Коллега", "Цены на жильё выросли на двенадцать процентов.", "TSEH-nih nah zhee-LYOH VIH-rahs-lee nah dvee-NAHTS-tsahty prah-TSEHN-tahf.", "Housing prices rose by twelve per cent."),
               D("Аналитик", "А доходы?", "ah dah-KHOH-dih?", "And incomes?"),
               D("Коллега", "Рост на пять процентов, то есть ниже инфляции.", "rohst nah pyahty prah-TSEHN-tahf, toh yehsty NEE-zheh een-FLYAH-tsee-ee.", "A rise of five per cent, that is, below inflation.")],
              WS("Budget worksheet", [
                  T("Report the change.", ["housing prices rose by twelve per cent", "food prices doubled"],
                    ["Цены на жильё выросли на двенадцать процентов", "Цены на продукты выросли в два раза"]),
                  T("Compare with inflation.", ["a rise of five per cent, below inflation", "incomes rose, savings did not change"],
                    ["Рост на пять процентов, ниже инфляции", "Доходы выросли, сбережения не изменились"]),
              ])),
            L("Работа и безработица",
              "The labour market has its own nouns: безработица, вакансия, зарплата, "
              "сокращение, рынок труда. Сократить takes the accusative and the amount with "
              "на: сократить штат на десять человек. The passive participle is the register "
              "of the news: были сокращены, был принят на работу.",
              [V("безработица", "beez-rah-BOH-tee-tsah", "unemployment", "noun"),
               V("вакансия", "vah-KAHN-see-yah", "vacancy", "noun"),
               V("зарплата", "zahr-PLAH-tah", "salary", "noun"),
               V("сокращение", "sahk-rah-SHCHYEH-nee-yeh", "cutback, reduction", "noun"),
               V("рынок труда", "RIH-nahk troo-DAH", "labour market", "noun")],
              G("Рынок труда",
                "сократить штат на десять человек · уровень безработицы · принять на работу · был сокращён",
                "Уровень безработицы is the fixed collocation (уровень + genitive). "
                "Сократить takes the object and на + accusative for the amount, while "
                "сокращение + genitive names the same event as a noun. Принять на работу is "
                "the verb for hiring; in the news register it becomes были приняты на работу.",
                [X("Уровень безработицы снизился до четырёх процентов.", "OO-rah-veen beez-rah-BOH-tee-tsih SNEE-zeel-syah dah chee-TIH-ryohkh prah-TSEHN-tahf.", "The unemployment rate fell to four per cent."),
                X("Компания сократила штат на десять человек.", "kahm-PAH-nee-yah sah-krah-TEE-lah shtaht nah DYEH-seety cheh-lah-VYEHk.", "The company cut its staff by ten people."),
                X("На заводе ещё десять вакансий.", "nah zah-VOH-dyeh yehsh-CHOH DYEH-seety vah-KAHN-see-ee.", "There are ten more vacancies at the factory.")],
                [("Уровень безработица вырос.", "Уровень безработицы вырос.", "Уровень takes the genitive: безработицы."),
                 ("Сократили штат в десять человек.", "Сократили штат на десять человек.", "The amount takes на + accusative.")]),
              [D("Журналист", "Что с рынком труда?", "shtoh s RIHN-kahm troo-DAH?", "What is happening in the labour market?"),
               D("Экономист", "Уровень безработицы снизился до четырёх процентов.", "OO-rah-veen beez-rah-BOH-tee-tsih SNEE-zeel-syah dah chee-TIH-ryohkh prah-TSEHN-tahf.", "The unemployment rate fell to four per cent."),
               D("Журналист", "А сокращения?", "ah sah-krah-SHCHYEH-nee-yah?", "And the cutbacks?"),
               D("Экономист", "В промышленности штат сократили на десять тысяч.", "v prah-mihsh-LYEHN-nah-stee shtaht sah-krah-TEE-lee nah DYEH-seety TIH-seech.", "In industry the staff was cut by ten thousand.")],
              WS("Labour market worksheet", [
                  T("Report the figures.", ["the unemployment rate fell to four per cent", "the company cut its staff by ten people"],
                    ["Уровень безработицы снизился до четырёх процентов", "Компания сократила штат на десять человек"]),
                  T("Talk about hiring.", ["there are ten more vacancies at the factory", "they were hired for the new plant"],
                    ["На заводе ещё десять вакансий", "Их приняли на новый завод"]),
              ])),
            L("Налоги и льготы",
              "Taxes and benefits are discussed with налог, ставка, льгота, вычет and "
              "декларация. The key constructions are иметь право на + accusative (to be "
              "entitled to), освобождён от + genitive (exempt from) and облагаться — the "
              "passive of taxing: облагается налогом.",
              [V("налог", "nah-LOHK", "tax", "noun"),
               V("ставка", "STAHF-kah", "rate", "noun"),
               V("льгота", "LYOH-gah-tah", "benefit, relief", "noun"),
               V("вычет", "VIH-cheht", "deduction", "noun"),
               V("декларация", "deh-klah-RAH-tsee-yah", "tax return", "noun")],
              G("Налоги и право на льготу",
                "облагается налогом · иметь право на + accusative · освобождён от + genitive · ставка налога",
                "Облагаться takes the instrumental: доход облагается налогом по ставке. "
                "Иметь право на takes the accusative: право на вычет, право на льготу. "
                "Освобождён от takes the genitive, and it agrees in gender with its subject: "
                "пенсия освобождена от налога. Декларация is filled in, not paid: подать "
                "декларацию.",
                [X("Этот доход не облагается налогом.", "EH-taht dah-KHOHT nee ahb-lah-GAH-yeht-syah nah-LOH-gahm.", "This income is not taxed."),
                X("Вы имеете право на вычет.", "vih ee-MYEH-yeh-teh PRAH-vah nah VIH-cheht.", "You are entitled to a deduction."),
                X("Пенсия освобождена от налога.", "PYEHN-see-yah ahs-vahbzh-DEH-nah aht nah-LOH-gah.", "A pension is exempt from tax.")],
                [("Доход облагается налог.", "Доход облагается налогом.", "Облагаться takes the instrumental."),
                 ("Право на вычета.", "Право на вычет.", "Право на takes the accusative.")]),
              [D("Консультант", "Этот доход облагается налогом?", "EH-taht dah-KHOHD ahb-lah-GAH-yeht-syah nah-LOH-gahm?", "Is this income taxed?"),
               D("Клиент", "А если я пенсионер?", "ah YEH-slee yah peen-see-ah-NYEHR?", "And if I am a pensioner?"),
               D("Консультант", "Тогда пенсия освобождена, а на вычет у вас есть право.", "tahg-DAH PYEHN-see-yah ahs-vahbzh-deh-NAH, ah nah VIH-cheht oo vahs yehsty PRAH-vah.", "Then the pension is exempt, and you are entitled to a deduction."),
               D("Клиент", "Декларацию подавать до когда?", "deh-klah-RAH-tsee-yoo pah-dah-VAHTY dah kahg-DAH?", "By when must the return be filed?")],
              WS("Taxes worksheet", [
                  T("State the rule.", ["this income is not taxed", "a pension is exempt from tax"],
                    ["Этот доход не облагается налогом", "Пенсия освобождена от налога"]),
                  T("Claim the right.", ["you are entitled to a deduction", "by when must the return be filed?"],
                    ["Вы имеете право на вычет", "До какого числа подавать декларацию?"]),
              ])),
        ]},
        {"id": "B2+-U3", "title": "Наука и техника", "lessons": [
            L("Исследование и данные",
              "Research is reported with провести + accusative (провести исследование), в "
              "ходе + genitive (в ходе эксперимента) and the short passive participle "
              "(проведён, получены). Гипотеза is confirmed or rejected; выборка is the "
              "sample you defend; результат is what remains after the caveats.",
              [V("исследование", "ees-SLYEH-dah-vah-nee-yeh", "study, research", "noun"),
               V("выборка", "VIH-bahr-kah", "sample", "noun"),
               V("гипотеза", "gee-POH-teh-zah", "hypothesis", "noun"),
               V("результат", "ree-zool-TAHT", "result", "noun"),
               V("провести", "prah-vees-TEE", "to conduct", "verb")],
              G("Как описывают исследование",
                "провести исследование · в ходе + genitive · данные получены · гипотеза не подтвердилась",
                "Провести is the verb for carrying out a study, an experiment or a survey: "
                "провели опрос. В ходе + genitive places the finding inside the process: в "
                "ходе эксперимента. Short participles report without an agent: данные "
                "получены, гипотеза подтверждена — and they agree with the subject in "
                "gender and number.",
                [X("Мы провели исследование среди студентов.", "mih prah-vee-LEE ees-SLYEH-dah-vah-nee-yeh sree-DEE stoo-DYEHN-tahf.", "We conducted a study among students."),
                X("В ходе опроса выяснилось, что выборка мала.", "v KHOH-dyeh ah-PROH-sah VIH-yahs-nee-lahsy, shtoh VIH-bahr-kah mah-LAH.", "In the course of the survey it emerged that the sample was small."),
                X("Гипотеза не подтвердилась, но данные получены.", "gee-POH-teh-zah nee paht-vehr-DEE-lahsy, noh DAHN-nih-yeh pah-loo-chee-NIH.", "The hypothesis was not confirmed, but the data were obtained.")],
                [("Мы провели исследование в студентов.", "Мы провели исследование среди студентов.", "Среди + genitive names the population."),
                 ("Данные получен.", "Данные получены.", "Данные is plural: получены.")]),
              [D("Научный руководитель", "Выборка достаточная?", "VIH-bahr-kah dah-stah-TAHCH-nah-yah?", "Is the sample sufficient?"),
               D("Аспирант", "Провели опрос среди трёхсот человек, в ходе выяснилось — да.", "prah-vee-LEE ah-PROHS sree-DEE tryokh-SOHT cheh-lah-VYEHk, v KHOH-dyeh VIH-yahs-nee-lahsy — dah.", "We surveyed three hundred people, and in the course of it it turned out — yes."),
               D("Руководитель", "А гипотеза?", "ah gee-POH-teh-zah?", "And the hypothesis?"),
               D("Аспирант", "Подтвердилась частично, и это тоже результат.", "paht-vehr-DEE-lahsy chahs-TEECH-nah, ee EH-tah TOH-zhih ree-zool-TAHT.", "Confirmed in part, and that is a result too.")],
              WS("Research worksheet", [
                  T("Describe the study.", ["we conducted a study among students", "the sample was small"],
                    ["Мы провели исследование среди студентов", "Выборка была мала"]),
                  T("Report the outcome.", ["the hypothesis was not confirmed", "the data were obtained"],
                    ["Гипотеза не подтвердилась", "Данные получены"]),
              ])),
            L("Технологии и общество",
              "Technology arguments run on внедрение + genitive (introduction of), приводить "
              "к + dative (leads to) and за счёт + genitive (at the expense of). "
              "Автоматизация and зависимость are the two nouns that organise the debate, and "
              "доступность keeps it from becoming abstract.",
              [V("технология", "tekh-nah-LOH-gee-yah", "technology", "noun"),
               V("автоматизация", "ahf-tah-mah-tee-ZAH-tsee-yah", "automation", "noun"),
               V("зависимость", "zah-VEE-see-mahsty", "dependence, addiction", "noun"),
               V("доступность", "dah-STOOP-nahsty", "accessibility", "noun"),
               V("внедрение", "vnehd-RYEH-nee-yeh", "implementation", "noun")],
              G("Внедрение и последствия",
                "внедрение + genitive · приводит к + dative · за счёт + genitive · зависит от + genitive",
                "Внедрение takes the genitive for what is introduced: внедрение новых "
                "технологий. Приводить к takes the dative for the consequence: приводит к "
                "росту. За счёт + genitive names what is gained or lost in exchange "
                "(сделали за счёт качества). Зависеть от + genitive keeps a claim conditional "
                "instead of absolute.",
                [X("Внедрение автоматизации приводит к росту производительности.", "vnehd-RYEH-nee-yeh ahf-tah-mah-tee-ZAH-tsee-ee pree-VOH-deet k rohstoo prah-ees-vah-DEE-tehl-nah-stee.", "The introduction of automation leads to growth in productivity."),
                X("Скорость выросла за счёт качества.", "SKOH-rahsty VIH-rahs-lah zah SHCHOHT KAHCH-eh-stvah.", "Speed rose at the expense of quality."),
                X("Эффект зависит от доступности сети.", "eh-FYEHKT zah-VEE-seet aht dah-STOOP-nah-stee SYEH-tee.", "The effect depends on the accessibility of the network.")],
                [("Внедрение новых технологий приводит рост.", "Внедрение новых технологий приводит к росту.", "Приводить к takes the dative."),
                 ("Эффект зависит доступности.", "Эффект зависит от доступности.", "Зависеть от takes the genitive.")]),
              [D("Журналист", "Чем обернётся автоматизация?", "chem ah-beer-NYOHT-syah ahf-tah-mah-tee-ZAH-tsee-yah?", "What will automation lead to?"),
               D("Инженер", "Внедрение снижает издержки, но приводит к зависимости от платформы.", "vnehd-RYEH-nee-yeh SNEE-zhah-yeht EES-dehrzh-kee, noh pree-VOH-deet k zah-VEE-see-mah-stee aht plaht-FOHR-mih.", "Implementation cuts costs but leads to dependence on the platform."),
               D("Журналист", "И что делать?", "ee shtoh DYEH-lahty?", "And what is to be done?"),
               D("Инженер", "Считать эффект: он зависит от доступности и от обучения.", "shee-TAHTY eh-FYEHKT: ohn zah-VEE-seet aht dah-STOOP-nah-stee ee aht ah-boo-CHYEH-nee-yah.", "Count the effect: it depends on access and on training.")],
              WS("Technology worksheet", [
                  T("Link cause and effect.", ["the introduction of automation leads to growth", "speed rose at the expense of quality"],
                    ["Внедрение автоматизации приводит к росту", "Скорость выросла за счёт качества"]),
                  T("Keep the claim conditional.", ["the effect depends on the accessibility of the network", "it depends on access and on training"],
                    ["Эффект зависит от доступности сети", "Он зависит от доступности и от обучения"]),
              ])),
            L("Проблемы и решения",
              "The final register of argument is risk and limitation: проблема + genitive, "
              "решение + genitive, риск, связанный с + instrumental, эффект от + genitive and "
              "ограничение. Ограничение is what the study cannot do, and stating it separates "
              "research from advertising.",
              [V("проблема", "prahb-LYEH-mah", "problem", "noun"),
               V("решение", "ree-SHEH-nee-yeh", "solution, decision", "noun"),
               V("риск", "reesk", "risk", "noun"),
               V("эффект", "eh-FYEHKT", "effect", "noun"),
               V("ограничение", "ahg-rah-nee-CHEH-nee-yeh", "limitation", "noun")],
              G("Проблема, риск и ограничение",
                "проблема + genitive · риск, связанный с + instrumental · эффект от + genitive · ограничение состоит в + prepositional",
                "Проблема and решение take the genitive for their object: проблема "
                "финансирования, решение проблемы. Связанный with + instrumental is the "
                "participle that qualifies a risk: риск, связанный с нагрузкой. Ограничение "
                "состоит в том, что … is the honest closing formula of any assessment.",
                [X("Решение проблемы требует ограничений.", "ree-SHEH-nee-yeh prahb-LYEH-mih TREH-boo-yeht ahg-rah-nee-CHEH-nee-ee.", "Solving the problem requires restrictions."),
                X("Основной риск связан с нагрузкой на сеть.", "ahs-nahv-NOY reesk SVYAH-zahn s nah-GROOZ-koy nah syety.", "The main risk is connected with the load on the network."),
                X("Ограничение состоит в том, что данные только за год.", "ahg-rah-nee-CHEH-nee-yeh sah-stah-EET v tohm, shtoh DAHN-nih-yeh TOHL-kah zah goht.", "The limitation is that the data cover only one year.")],
                [("Проблема финансирование.", "Проблема финансирования.", "Проблема takes the genitive."),
                 ("Риск связан нагрузкой.", "Риск связан с нагрузкой.", "Связанный takes с + instrumental.")]),
              [D("Рецензент", "Где ограничение работы?", "gdyeh ahg-rah-nee-CHEH-nee-yeh rah-BOH-tih?", "Where is the limitation of the work?"),
               D("Автор", "Ограничение состоит в том, что выборка только городская.", "ahg-rah-nee-CHEH-nee-yeh sah-stah-EET v tohm, shtoh VIH-bahr-kah TOHL-kah gah-rahd-SKAH-yah.", "The limitation is that the sample is urban only."),
               D("Рецензент", "А риск выводов?", "ah reesk VIH-vah-dahf?", "And the risk of the conclusions?"),
               D("Автор", "Риск связан с переносом на село, и я это пишу прямо.", "reesk SVYAH-zahn s peh-ree-NOH-sahm nah see-LOH, ee yah EH-tah pee-SHOO PRYAH-mah.", "The risk is connected with transferring them to the countryside, and I say so plainly.")],
              WS("Risk worksheet", [
                  T("Name the problem and its solution.", ["solving the problem requires restrictions", "the limitation is that the data cover only one year"],
                    ["Решение проблемы требует ограничений", "Ограничение состоит в том, что данные только за год"]),
                  T("Qualify the risk.", ["the main risk is connected with the load on the network", "the risk is connected with transferring them to the countryside"],
                    ["Основной риск связан с нагрузкой на сеть", "Риск связан с переносом на село"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Русская наука дала миру периодическую таблицу Менделеева (1869), "
                 "космическую программу и первый спутник: 4 октября 1957 года, а через "
                 "четыре года — полёт Гагарина. За этими датами стоит особая культура "
                 "институтов: академические институты, закрытые города, конструкторские "
                 "бюро. Сегодня разговор о науке в России начинается с цифр "
                 "финансирования и заканчивается вопросом о том, как удержать "
                 "исследователей внутри страны."),
        source_url="https://en.wikipedia.org/wiki/Science_and_technology_in_Russia",
        reading=("В прошлом году мы провели исследование о внедрении автоматизации на "
                 "предприятиях. Выборка была небольшой — триста человек, и в ходе работы "
                 "выяснилось, что главный риск связан не с техникой, а с обучением. "
                 "Ограничение состоит в том, что данные касаются только городских заводов, "
                 "и я пишу об этом прямо. Гипотеза подтвердилась частично: эффект есть, но "
                 "он зависит от доступности обучения."),
        reading_gloss=("Last year we conducted a study on the introduction of automation at "
                       "enterprises. The sample was small — three hundred people — and in the "
                       "course of the work it emerged that the main risk is connected not "
                       "with the equipment but with training. The limitation is that the "
                       "data concern only urban factories, and I say so plainly. The "
                       "hypothesis was confirmed in part: there is an effect, but it depends "
                       "on the accessibility of training."),
        listening=("Отказали в выдаче, что делать? — Обжаловать в течение десяти дней, на "
                   "основании закона. — А если срок прошёл? — Тогда только суд."),
        listening_gloss=("They refused the issue, what should I do? — Appeal within ten days, "
                         "on the basis of the law. — And if the term has passed? — Then only "
                         "the courts."),
        voice_tag=VOICE,
        idioms=[
            ("в ходе работы", "in the course of the work", "while the work was going on"),
            ("в пределах компетенции", "within the remit", "as far as one's authority goes"),
            ("нести ответственность", "to carry responsibility", "to answer for something"),
            ("на основании закона", "on the basis of the law", "with legal grounds"),
            ("за счёт качества", "at the expense of quality", "gaining one thing by losing another"),
            ("с поправкой на", "with a correction for", "allowing for"),
            ("ставить под сомнение", "to put under doubt", "to call into question"),
            ("иметь в виду", "to have in mind", "to bear in mind"),
            ("в конечном счёте", "in the final count", "in the end, ultimately"),
            ("по существу", "on the essence", "substantively, to the point"),
        ],
        mistakes=[
            ("Согласно регламента, срок — тридцать дней.", "Согласно регламенту, срок — тридцать дней.", "Согласно takes the dative."),
            ("Рост цен составил на десять процентов.", "Рост цен составил десять процентов.", "Составить takes a bare amount."),
            ("Риск связан нагрузкой.", "Риск связан с нагрузкой.", "Связанный takes с + instrumental."),
        ],
        task_title="Заключение на одну страницу",
        task_instructions=("Write a one-page assessment of a study or a pilot project you "
                           "know: what was done (провести, в ходе), what came out with the "
                           "numbers (рост на, снизился до), what limits it (ограничение "
                           "состоит в том, что) and what you recommend (представляется "
                           "целесообразным). Use at least one impersonal short participle and "
                           "one conditional claim with зависит от. Then reread it and delete "
                           "every sentence that has no number and no source."),
    ),
    "test": [
        ("translate_en", "Say: the decision is taken within thirty days.", "Решение принимается в течение тридцати дней."),
        ("translate_ru", "Уровень безработицы снизился до четырёх процентов.", "The unemployment rate fell to four per cent."),
        ("multiple_choice", "Which sentence is exempt from tax?", "Пенсия освобождена от налога."),
        ("fill_in_the_blank", "Внедрение автоматизации приводит ___ росту.", "к"),
        ("word_selection", "Select the Russian for 'deduction (tax)'.", "вычет"),
        ("error_correction", "Согласно регламента, срок — тридцать дней.", "Согласно регламенту, срок — тридцать дней."),
        ("dialogue_completion", "Complete: А если отказ? — ___ (appeal within ten days)", "Обжалуйте в течение десяти дней"),
        ("matching", "Match выборка to its meaning.", "sample"),
        ("reading_comprehension", "В тексте, сколько человек было в выборке?", "three hundred"),
        ("inference", "Автор пишет об ограничении прямо. What does that tell us about the text?", "it is honest about what it cannot claim"),
        ("main_idea", "В тексте описано исследование и его ограничения. — what is this sentence?", "the main point of the reading"),
        ("detail_identification", "С чем связан главный риск?", "with training, not equipment"),
    ],
}

HALFSTEPS["C1+"] = {
    "native": NATIVE,
    "title": "%s C1+ — Академия, политика и перевод" % NAME,
    "goals": [
        "Write and present academic work: abstract, citation, paraphrase and questions",
        "Follow regulation, statistics and public hearings, and report them precisely",
        "Translate and edit: false friends, style and culture-specific words",
    ],
    "units": [
        {"id": "C1+-U1", "title": "Академический русский", "lessons": [
            L("Аннотация статьи",
              "An abstract is written in one paragraph and four moves: предмет, цель, метод, "
              "вывод. The impersonal register hides the author — в статье рассматривается, "
              "автор приходит к выводу, — and the aim is stated with цель + genitive: цель "
              "работы. Вывод is the last move and the only one a reader may quote.",
              [V("аннотация", "ah-nah-TAH-tsee-yah", "abstract", "noun"),
               V("цель", "tsyehl", "aim, goal", "noun"),
               V("метод", "MYEH-tahd", "method", "noun"),
               V("вывод", "VIH-vaht", "conclusion", "noun"),
               V("рассматриваться", "rahs-SMAHt-ree-vah-t-syah", "to be examined", "verb")],
              G("Аннотация: четыре хода",
                "в статье рассматривается · цель работы — + infinitive · методом + genitive · автор приходит к выводу",
                "В статье рассматривается + nominative names the object of the study and "
                "keeps the author out of the sentence. Цель работы — + infinitive states the "
                "aim. Методом + genitive or с помощью + genitive names the method, and автор "
                "приходит к выводу, что … closes the paragraph with the only claim the "
                "abstract carries.",
                [X("В статье рассматривается динамика цен на жильё.", "v stah-TYEH rahs-SMAHt-ree-vah-yeht-syah dee-NAH-mee-kah tsehn nah zhee-LYOH.", "The article examines the dynamics of housing prices."),
                X("Цель работы — описать связь между выборкой и результатом.", "TSYEL rah-BOH-tih — ah-pee-SAHTY svyahzy MYEZH-doo VIH-bahr-koy ee ree-zool-TAH-tahm.", "The aim of the work is to describe the link between sample and result."),
                X("Автор приходит к выводу, что эффект зависит от обучения.", "AHf-tahr pree-KHOH-deet k VIH-vah-doo, shtoh eh-FYEHKT zah-VEE-seet aht ah-boo-CHYEH-nee-yah.", "The author concludes that the effect depends on training.")],
                [("В статье я рассматриваю динамику.", "В статье рассматривается динамика.", "An abstract is impersonal: рассматривается."),
                 ("Цель работы — описание связи, автор приходит к выводу, что всё сложно.", "Автор приходит к выводу, что эффект зависит от обучения.", "One claim per sentence, and the claim must be checkable.")]),
              [D("Редактор", "Аннотация по форме?", "ah-nah-TAH-tsee-yah pah FOHR-myeh?", "Is the abstract in shape?"),
               D("Автор", "Предмет, цель и метод есть, вывод в конце.", "PREHD-myeht, TSYEL ee MYEH-tahd yehsty, VIH-vaht v kahn-TSYEH.", "Subject, aim and method are there, the conclusion at the end."),
               D("Редактор", "А метод назван как?", "ah MYEH-tahd NAHZ-vahn kahk?", "And how is the method named?"),
               D("Автор", "Методом опроса, с помощью анкеты на триста человек.", "MYEH-tah-dahm ah-PROH-sah, s POH-mah-shchyoo ahn-KYEH-tih nah TREE-stah cheh-lah-VYEHk.", "By the survey method, with a questionnaire on three hundred people.")],
              WS("Abstract worksheet", [
                  T("Write the moves.", ["the article examines the dynamics of housing prices", "the aim of the work is to describe the link"],
                    ["В статье рассматривается динамика цен на жильё", "Цель работы — описать связь"]),
                  T("State the method and the conclusion.", ["by the survey method", "the author concludes that the effect depends on training"],
                    ["Методом опроса", "Автор приходит к выводу, что эффект зависит от обучения"]),
              ])),
            L("Цитирование и парафраз",
              "Attribution has its own prepositions: согласно + dative, по словам + genitive, "
              "ссылаться на + accusative. A direct quotation keeps the кавычки and the page; "
              "a paraphrase changes the syntax, not only the words. Плагиат is defined by the "
              "missing ссылка, not by the repeated idea.",
              [V("цитата", "tsee-TAH-tah", "quotation", "noun"),
               V("ссылка", "SSIHL-kah", "reference, link", "noun"),
               V("парафраз", "pah-rah-FRAHS", "paraphrase", "noun"),
               V("плагиат", "plah-gee-AHT", "plagiarism", "noun"),
               V("кавычки", "kah-VICH-kee", "quotation marks", "noun")],
              G("Ссылка и парафраз",
                "согласно + dative · по словам + genitive · ссылаться на + accusative · в кавычках",
                "Согласно takes the dative of the source (согласно отчёту), по словам — the "
                "genitive of the speaker (по словам автора). Ссылаться на + accusative names "
                "the reference openly, and в кавычках marks a literal quotation. A paraphrase "
                "must change the syntactic frame; if the frame stays and the words change, it "
                "is still plagiarism.",
                [X("Согласно отчёту, срок был нарушен.", "sah-GLAHS-nah aht-CHOH-too, srohk bihl nah-ROO-shehn.", "According to the report, the deadline was missed."),
                X("По словам автора, причина в логистике.", "pah slah-VAHM AHf-tah-rah, pree-CHEE-nah v lah-GEES-tee-keh.", "According to the author, the cause lies in logistics."),
                X("Он ссылается на данные 2019 года.", "ohn SSEE-lah-yeht-syah nah DAHN-nih-yeh dvyEH TIH-see-chee dee-veet-NAHd-tsah-tah-vah GOH-dah.", "He refers to the 2019 data.")],
                [("Согласно отчёта, срок был нарушен.", "Согласно отчёту, срок был нарушен.", "Согласно takes the dative."),
                 ("По словам автора сказано, что причина в логистике.", "По словам автора, причина в логистике.", "По словам is a parenthetical; the sentence keeps its own verb.")]),
              [D("Научный редактор", "Это цитата или парафраз?", "EH-tah tsee-TAH-tah EE-lee pah-rah-FRAHS?", "Is this a quotation or a paraphrase?"),
               D("Автор", "Парафраз, но синтаксис близкий к оригиналу.", "pah-rah-FRAHS, noh SEEN-tah-kees BLEES-kee k ah-ree-gee-NAH-loo.", "A paraphrase, but the syntax is close to the original."),
               D("Научный редактор", "Тогда поставьте кавычки и ссылку.", "tahg-DAH pah-STAHF-teh kah-VICH-kee ee SSIHL-koo.", "Then put quotation marks and a reference."),
               D("Автор", "Согласен: лучше ссылка, чем плагиат.", "sah-GLAH-sehn: LOOT-sheh SSIHL-kah, chem plah-gee-AHT.", "Agreed: better a reference than plagiarism.")],
              WS("Citation worksheet", [
                  T("Attribute.", ["according to the report, the deadline was missed", "according to the author, the cause lies in logistics"],
                    ["Согласно отчёту, срок был нарушен", "По словам автора, причина в логистике"]),
                  T("Mark the source.", ["he refers to the 2019 data", "then put quotation marks and a reference"],
                    ["Он ссылается на данные 2019 года", "Поставьте кавычки и ссылку"]),
              ])),
            L("Доклад и вопросы",
              "A conference talk is a доклад, the section is секция, and the question period "
              "follows the регламент. Разрешите вопрос opens the answer; в рамках доклада "
              "keeps the answer inside the subject; отвечу в двух частях structures it, and "
              "благодарю за вопрос is the formula that buys a second.",
              [V("доклад", "dah-KLAHT", "paper, talk", "noun"),
               V("секция", "SYEHk-tsee-yah", "session, section", "noun"),
               V("регламент", "ree-GLAH-mehnt", "time limit, procedure", "noun"),
               V("дискуссия", "dees-KOO-see-yah", "discussion", "noun"),
               V("уточнить", "oo-tahch-NEETY", "to make precise, to clarify", "verb")],
              G("Доклад и ответ на вопрос",
                "разрешите вопрос · в рамках доклада · отвечу в двух частях · уточню, что",
                "Разрешите вопрос is the polite opening of an answer, and благодарю за "
                "вопрос keeps it civil even when the question is hostile. В рамках доклада "
                "bounds the answer to the subject. Уточню, что … corrects a premise before "
                "answering it, which is the single most useful move in a public defence.",
                [X("Благодарю за вопрос; отвечу в двух частях.", "blah-gah-dah-RYOO zah vah-PROHS; aht-VYEH-choo v DVOOKH chahs-TYAKH.", "Thank you for the question; I will answer in two parts."),
                X("В рамках доклада я опираюсь на данные опроса.", "v RAHM-kahkh dah-KLAH-dah yah ah-pee-RAH-yoosy nah DAHN-nih-yeh ah-PROH-sah.", "Within the talk I rely on the survey data."),
                X("Уточню, что выборка была городской.", "oo-tahch-NYOO, shtoh VIH-bahr-kah bih-LAH gah-rahd-SKOY.", "Let me clarify that the sample was urban.")],
                [("Разрешите вопрос, я скажу о выводах и о данных и о рисках и о сроках.", "Разрешите вопрос; отвечу в двух частях.", "An answer of four parts cannot be heard; name the structure first."),
                 ("В рамках доклада доклада я опираюсь на данные.", "В рамках доклада я опираюсь на данные.", "В рамках доклада is a fixed formula.")]),
              [D("Модератор", "Есть вопросы к докладчику?", "yehsty vah-PROH-sih k dah-KLAHT-chee-koo?", "Are there questions for the speaker?"),
               D("Участник", "Как вы получили выборку?", "kahk vih pah-loo-CHEE-lee VIH-bahr-koo?", "How did you obtain the sample?"),
               D("Докладчик", "Благодарю за вопрос. Отвечу в двух частях: метод и ограничение.", "blah-gah-dah-RYOO zah vah-PROHS. aht-VYEH-choo v DVOOKH chahs-TYAKH: MYEH-tahd ee ahg-rah-nee-CHEH-nee-yeh.", "Thank you for the question. I will answer in two parts: method and limitation."),
               D("Участник", "Достаточно. Второе я понял.", "dah-STAH-tahch-nah. ftah-ROH-yeh yah POH-neel.", "That is enough. I understood the second part.")],
              WS("Talk worksheet", [
                  T("Open the answer.", ["thank you for the question; I will answer in two parts", "let me clarify that the sample was urban"],
                    ["Благодарю за вопрос; отвечу в двух частях", "Уточню, что выборка была городской"]),
                  T("Bound the answer.", ["within the talk I rely on the survey data", "are there questions for the speaker?"],
                    ["В рамках доклада я опираюсь на данные опроса", "Есть вопросы к докладчику?"]),
              ])),
        ]},
        {"id": "C1+-U2", "title": "Публичная политика", "lessons": [
            L("Регулирование и контроль",
              "Regulation has a fixed vocabulary: регулирование, надзор, норма, соответствие, "
              "проверка. In accordance with is в соответствии с + instrumental; subject to is "
              "подлежать + dative: подлежит проверке. Проверка ends with акт — the document "
              "that says what was found.",
              [V("регулирование", "ree-goo-lee-rah-VAH-nee-yeh", "regulation", "noun"),
               V("надзор", "nahd-ZOHR", "supervision, oversight", "noun"),
               V("норма", "NOHR-mah", "norm, rule", "noun"),
               V("соответствие", "sah-aht-VYEHT-stvee-yeh", "compliance, correspondence", "noun"),
               V("проверка", "prah-VYEHk-kah", "inspection, check", "noun")],
              G("Соответствие и надзор",
                "в соответствии с + instrumental · подлежать + dative · соответствовать + dative · по итогам проверки",
                "В соответствии с + instrumental is the legal formula (в соответствии с "
                "нормой), and соответствовать takes the dative directly (документы "
                "соответствуют требованиям). Подлежать + dative says what must happen: "
                "подлежит проверке. По итогам проверки + genitive reports what followed.",
                [X("Документы соответствуют требованиям нормы.", "dah-koo-MYEHN-tih sah-aht-VYEHT-stvooy-oot TREH-bah-vah-nee-yahm NOHR-mih.", "The documents comply with the requirements of the rule."),
                X("Проект подлежит проверке в соответствии с регламентом.", "prah-YEHkt pahd-leh-ZHEET prah-VYEHr-kee v sah-aht-VYEHT-stvee-ee s ree-GLAH-mehn-tahm.", "The project is subject to inspection in accordance with the regulation."),
                X("По итогам проверки выявлены нарушения.", "pah ee-TOH-gahm prah-VYEHr-kee VIH-yahv-leh-nih nah-roo-SHEH-nee-yah.", "Following the inspection, violations were identified.")],
                [("В соответствии регламента.", "В соответствии с регламентом.", "В соответствии с takes the instrumental."),
                 ("Документы соответствуют с требованиями.", "Документы соответствуют требованиям.", "Соответствовать takes the dative with no preposition.")]),
              [D("Инспектор", "Как прошла проверка?", "kahk prahsh-LAH prah-VYEHr-kah?", "How did the inspection go?"),
               D("Руководитель", "По итогам — два нарушения.", "pah ee-TOH-gahm — dvah nah-roo-SHEH-nee-yah.", "Two violations, following the inspection."),
               D("Инспектор", "Что подлежит исправлению?", "shtoh pahd-leh-ZHEET ees-prahv-LYEH-nee-yoo?", "What is subject to correction?"),
               D("Руководитель", "Отчётность. Приведём в соответствие с нормой за месяц.", "aht-CHOHT-nahsty. pree-vee-DYOHM v sah-aht-VYEHT-stvee-yeh s NOHR-moy zah MYEH-seets.", "The reporting. We will bring it into compliance with the rule within a month.")],
              WS("Regulation worksheet", [
                  T("State compliance.", ["the documents comply with the requirements of the rule", "the project is subject to inspection"],
                    ["Документы соответствуют требованиям нормы", "Проект подлежит проверке"]),
                  T("Report the outcome.", ["following the inspection, violations were identified", "what is subject to correction?"],
                    ["По итогам проверки выявлены нарушения", "Что подлежит исправлению?"]),
              ])),
            L("Статистика и интерпретация",
              "Statistics is read with показатель, динамика, тенденция and погрешность. The "
              "growth is said with на + accusative or до + genitive (вырос на пять процентов "
              "/ вырос до пяти процентов), the tendency with к + dative (тенденция к росту), "
              "and the honest reading with с поправкой на + accusative.",
              [V("статистика", "stah-TEES-tee-kah", "statistics", "noun"),
               V("показатель", "pah-kah-ZAH-teel", "indicator", "noun"),
               V("динамика", "dee-NAH-mee-kah", "dynamics, trend", "noun"),
               V("тенденция", "tehn-DYEHN-tsee-yah", "tendency", "noun"),
               V("погрешность", "pah-GRYEHsh-nahsty", "margin of error", "noun")],
              G("На и до: как читать показатель",
                "вырос на пять процентов · вырос до пяти процентов · тенденция к + dative · с поправкой на + accusative",
                "На + accusative is the size of the change and до + genitive the level "
                "reached: вырос на пять процентов (from 10 to 10.5 per cent as a share of "
                "10) versus вырос до пяти процентов. Тенденция к + dative names the "
                "direction. С поправкой на + accusative and в пределах погрешности keep the "
                "reading honest.",
                [X("Показатель вырос на пять процентов.", "pah-kah-ZAH-teel VIH-rahs nah pyahty prah-TSEHN-tahf.", "The indicator rose by five per cent."),
                X("Доля выросла до пяти процентов.", "DOH-lyah VIH-rahs-lah dah pee-TEE prah-TSEHN-tahf.", "The share rose to five per cent."),
                X("С поправкой на инфляцию, динамика нулевая.", "s pah-PRAHF-koy nah een-FLYAH-tsee-yoo, dee-NAH-mee-kah noo-leh-VAH-yah.", "Corrected for inflation, the dynamics are flat.")],
                [("Показатель вырос на пяти процентов.", "Показатель вырос на пять процентов.", "На takes the accusative here."),
                 ("Тенденция роста к росту.", "Тенденция к росту.", "One direction per sentence.")]),
              [D("Журналист", "Что говорит статистика?", "shtoh gah-vah-REET stah-TEES-tee-kah?", "What do the statistics say?"),
               D("Статистик", "Показатель вырос на пять процентов, но в пределах погрешности.", "pah-kah-ZAH-teel VIH-rahs nah pyahty prah-TSEHN-tahf, noh v pree-DYEH-lahkh pah-GRYEHsh-nah-stee.", "The indicator rose five per cent, but within the margin of error."),
               D("Журналист", "А тенденция?", "ah tehn-DYEHN-tsee-yah?", "And the tendency?"),
               D("Статистик", "С поправкой на инфляцию — тенденция к стагнации.", "s pah-PRAHF-koy nah een-FLYAH-tsee-yoo — tehn-DYEHN-tsee-yah k stahg-NAH-tsee-ee.", "Corrected for inflation, the tendency is towards stagnation.")],
              WS("Statistics worksheet", [
                  T("Read the numbers.", ["the indicator rose by five per cent", "the share rose to five per cent"],
                    ["Показатель вырос на пять процентов", "Доля выросла до пяти процентов"]),
                  T("Qualify the reading.", ["corrected for inflation, the dynamics are flat", "the tendency is towards stagnation"],
                    ["С поправкой на инфляцию, динамика нулевая", "Тенденция к стагнации"]),
              ])),
            L("Публичные слушания",
              "A hearing produces four nouns: слушания, замечание, протокол, решение. "
              "Замечание is submitted (внести замечание), the protocol records it (в "
              "протоколе зафиксировано), and the decision follows по итогам + genitive or "
              "принято решение + infinitive. Обращение к + dative is the address of the "
              "speaker to the assembly.",
              [V("слушания", "SHOO-shah-nee-yah", "hearings", "noun"),
               V("замечание", "zah-meh-CHAH-nee-yeh", "remark, objection", "noun"),
               V("протокол", "prah-tah-KOHL", "minutes, protocol", "noun"),
               V("обращение", "ahb-rah-SHCHYEH-nee-yeh", "address, appeal", "noun"),
               V("принять", "preet-NYAHty", "to adopt, to take", "verb")],
              G("Слушания и протокол",
                "внести замечание · в протоколе зафиксировано · по итогам + genitive · принято решение + infinitive",
                "Внести замечание is the verb for raising an objection in a formal setting; "
                "the noun is замечание, the plural замечания. В протоколе зафиксировано, что "
                "… reports what the minutes record, impersonally. По итогам + genitive opens "
                "the decision, and принято решение + infinitive closes it without naming who "
                "decided.",
                [X("Разрешите внести замечание к проекту.", "rahz-ree-SHEE-teh vnees-TEE zah-meh-CHAH-nee-yeh k prah-YEHk-too.", "May I submit a remark on the draft."),
                X("В протоколе зафиксировано, что замечание принято к сведению.", "v prah-tah-KOH-leh zah-feek-SEE-rah-vah-nah, shtoh zah-meh-CHAH-nee-yeh PREH-nyah-tah k SVYEH-dyeh-nee-yoo.", "The minutes record that the remark was taken into account."),
                X("По итогам слушаний принято решение доработать проект.", "pah ee-TOH-gahm SHOO-shah-nee-ee PREH-nyah-tah ree-SHEH-nee-yeh dah-rah-BOH-tahty prah-YEHkt.", "Following the hearings, a decision was taken to revise the draft.")],
                [("Внести замечание на проект.", "Внести замечание к проекту.", "A remark is к + dative here."),
                 ("По итогам слушаний решают доработать.", "По итогам слушаний принято решение доработать проект.", "The impersonal formula is принято решение.")]),
              [D("Ведущий", "Есть замечания к проекту?", "yehsty zah-meh-CHAH-nee-yah k prah-YEHk-too?", "Are there remarks on the draft?"),
               D("Участница", "Разрешите внести замечание по срокам.", "rahz-ree-SHEE-teh vnees-TEE zah-meh-CHAH-nee-yeh pah SROH-kahm.", "May I submit a remark on the deadlines."),
               D("Ведущий", "Зафиксировано. Что предлагаете?", "zah-feek-SEE-rah-vah-nah. shtoh preed-lah-GAH-yeh-teh?", "Recorded. What do you propose?"),
               D("Участница", "По итогам слушаний принять решение продлить срок на месяц.", "pah ee-TOH-gahm SHOO-shah-nee-ee preet-NYAHty ree-SHEH-nee-yeh prahd-LEETY srohk nah MYEH-seets.", "Following the hearings, to adopt a decision extending the term by a month.")],
              WS("Hearings worksheet", [
                  T("Submit a remark.", ["may I submit a remark on the deadlines", "the minutes record that the remark was taken into account"],
                    ["Разрешите внести замечание по срокам", "В протоколе зафиксировано, что замечание принято к сведению"]),
                  T("State the decision.", ["following the hearings, a decision was taken to revise the draft", "to extend the term by a month"],
                    ["По итогам слушаний принято решение доработать проект", "Продлить срок на месяц"]),
              ])),
        ]},
        {"id": "C1+-U3", "title": "Перевод и редактура", "lessons": [
            L("Ложные друзья переводчика",
              "The classic traps are актуальный (topical, not actual), принципиальный (of "
              "principle, not principal), адекватный (adequate as a translation term too) and "
              "претензия (claim, complaint). A translator works with значение (meaning), "
              "соответствие (equivalent) and контекст: the same word is translated "
              "differently in a contract, a novel and a headline.",
              [V("перевод", "pee-ree-VOHT", "translation", "noun"),
               V("значение", "znah-CHEH-nee-yeh", "meaning", "noun"),
               V("соответствие", "sah-aht-VYEHT-stvee-yeh", "equivalent", "noun"),
               V("буквальный", "BOOK-vahl-nihy", "literal", "adjective"),
               V("контекст", "kahn-TYEHkst", "context", "noun")],
              G("Значение и контекст",
                "в значении + genitive · соответствие + dative · в зависимости от контекста · буквальный перевод",
                "В значении + genitive names which sense is meant (в значении «актуальный»). "
                "Соответствовать takes the dative, and соответствие is the noun of the same "
                "relation. В зависимости от контекста is the translator's hedge that is not "
                "a hedge but a fact, and буквальный перевод is the diagnosis of a translation "
                "that followed the letters instead of the sense.",
                [X("«Актуальный» значит «злободневный», а не «фактический».", "ahk-too-AHL-nihy ZNAH-cheet zlah-bahd-NYEHv-nihy, ah nee fahk-TEE-cheh-Skee.", "'Актуальный' means topical, not actual."),
                X("Здесь нужен не буквальный перевод, а соответствие по смыслу.", "zdyehsy NOO-zhehn nee BOOK-vahl-nihy pee-ree-VOHT, ah sah-aht-VYEHT-stvee-yeh pah SMIH-sloo.", "Here what is needed is not a literal translation but an equivalent in sense."),
                X("В зависимости от контекста, перевод меняется.", "v zah-VEE-see-mah-stee aht kahn-TYEHk-stah, pee-ree-VOHT mee-NYAH-yeht-syah.", "Depending on the context, the translation changes.")],
                [("«Актуальный» значит «фактический».", "«Актуальный» значит «злободневный».", "The words look similar to English 'actual' but are false friends."),
                 ("Буквальный перевод передаёт смысл.", "Буквальный перевод передаёт букву, а не смысл.", "Literal translation preserves letters, not sense.")]),
              [D("Редактор", "«Актуальный» здесь — ложный друг?", "ahk-too-AHL-nihy zdyehsy — LOHZH-nihy drook?", "Is 'актуальный' a false friend here?"),
               D("Переводчик", "Да: в значении «злободневный».", "dah: v znah-CHEH-nee-ee zlah-bahd-NYEHv-nihy.", "Yes: in the sense of 'topical'."),
               D("Редактор", "А как передать «претензия»?", "ah kahk pee-ree-DAHTY pree-TEHN-zee-yah?", "And how do you render 'претензия'?"),
               D("Переводчик", "В зависимости от контекста: в договоре — «claim», в статье — «complaint».", "v zah-VEE-see-mah-stee aht kahn-TYEHk-stah: v dah-gah-VOH-ryeh — claim, v stah-TYEE — complaint.", "Depending on context: in a contract 'claim', in an article 'complaint'.")],
              WS("Translation worksheet", [
                  T("Repair the false friend.", ["'актуальный' means topical, not actual", "here what is needed is not a literal translation but an equivalent in sense"],
                    ["«Актуальный» значит «злободневный», а не «фактический»", "Здесь нужен не буквальный перевод, а соответствие по смыслу"]),
                  T("Explain the choice.", ["depending on the context, the translation changes", "'претензия' in a contract is a claim"],
                    ["В зависимости от контекста, перевод меняется", "«Претензия» в договоре — claim"]),
              ])),
            L("Редактура и стиль",
              "Editing is done with four verbs: заменить на + accusative, сократить до + "
              "genitive, убрать, переписать. Ясность and точность are the goals, канцелярит "
              "the disease. Правка is the edit itself, and the editor's questions are зачем "
              "здесь это? and что это доказывает?.",
              [V("редактура", "ree-dahk-TOO-rah", "editing", "noun"),
               V("стиль", "steel", "style", "noun"),
               V("ясность", "YAHs-nahsty", "clarity", "noun"),
               V("канцелярит", "kahn-tsih-lee-REET", "officialese", "noun"),
               V("правка", "PRAHF-kah", "edit, correction", "noun")],
              G("Правка текста",
                "заменить + accusative на + accusative · сократить до + genitive · убрать · переписать так, чтобы",
                "Заменить takes the accusative of the old and на + accusative of the new: "
                "заменить канцелярит на глагол. Сократить takes до + genitive for the target "
                "length. Убрать takes the accusative of what is deleted, and переписать так, "
                "чтобы + past tense states the goal of the rewrite.",
                [X("Замените отглагольные существительные на глаголы.", "zah-mee-NEE-teh aht-glah-GOHL-nih-yeh soo-shcheh-STVEE-tehl-nih-yeh nah glah-GOH-lih.", "Replace the verbal nouns with verbs."),
                X("Сократите абзац до трёх предложений.", "sah-krah-TEE-teh ahb-ZAHTS dah tryokh prehd-lah-ZHEH-nee-ee.", "Cut the paragraph to three sentences."),
                X("Перепишите так, чтобы читатель понял без словаря.", "pee-ree-pee-SHEE-teh tahk, SHTOH-bih chee-TAH-teel POH-neel byez slah-vah-RYAH.", "Rewrite it so that the reader understands without a dictionary.")],
                [("Замените канцелярит к глаголу.", "Замените канцелярит на глагол.", "Заменить takes на + accusative."),
                 ("Сократите до трёх предложений, потому что длинно и непонятно.", "Сократите абзац до трёх предложений.", "The edit should be specific, not a complaint.")]),
              [D("Редактор", "Зачем здесь это прилагательное?", "zah-CHEM zdyehsy EH-tah pree-lah-GAH-tehl-nah-yeh?", "Why is this adjective here?"),
               D("Автор", "Для стиля.", "dlyah STEEL-yah.", "For style."),
               D("Редактор", "Тогда уберём: ясность важнее.", "tahg-DAH oo-bee-RYOHM: YAHs-nahsty VAHZH-nyeh-yeh.", "Then let's delete it: clarity matters more."),
               D("Автор", "Согласен. И заменить канцелярит на глаголы?", "sah-GLAH-sehn. ee zah-mee-NEETY kahn-tsih-lee-REET nah glah-GOH-lih?", "Agreed. And replace the officialese with verbs?")],
              WS("Editing worksheet", [
                  T("Give the instruction.", ["replace the verbal nouns with verbs", "cut the paragraph to three sentences"],
                    ["Замените отглагольные существительные на глаголы", "Сократите абзац до трёх предложений"]),
                  T("State the goal.", ["rewrite it so that the reader understands without a dictionary", "clarity matters more"],
                    ["Перепишите так, чтобы читатель понял без словаря", "Ясность важнее"]),
              ])),
            L("Язык и культура в переводе",
              "Some words name a practice: дача, тоска, интеллигенция, пошлость, авось. Three "
              "strategies exist — подобрать соответствие, передать оттенок, оставить без "
              "перевода с пояснением — and the choice is defended by контекст, not by a "
              "dictionary. Интонация and подтекст are what a translation loses first, and "
              "идиома is where the loss becomes visible.",
              [V("реалия", "ree-AH-lee-yah", "culture-specific word", "noun"),
               V("оттенок", "aht-TYEH-nahk", "shade of meaning", "noun"),
               V("интонация", "een-tah-NAH-tsee-yah", "intonation", "noun"),
               V("идиома", "ee-dee-OH-mah", "idiom", "noun"),
               V("подтекст", "PAHd-tyehkst", "subtext", "noun")],
              G("Реалия и оттенок",
                "подобрать соответствие · передать оттенок · оставить без перевода + пояснение · потерять интонацию",
                "Подобрать соответствие replaces the item with a functional equivalent; "
                "передать оттенок keeps the flavour with a calque or a borrowing; оставить "
                "без перевода и дать пояснение is the essayist's choice and the translator's "
                "last resort. Each strategy loses something: соответствие loses the local "
                "colour, оттенок risks sounding foreign, and the explanation stops the "
                "narrative.",
                [X("«Дача» передаётся как 'country house' или объясняется в сноске.", "DAH-chah pee-ree-dah-YOHT-syah kahk country house EE-lee ahb-yahs-NYAH-yeht-syah v SNOHs-kyeh.", "'Дача' is rendered as 'country house' or explained in a footnote."),
                X("Идиому нельзя перевести слово в слово, но оттенок сохранить можно.", "ee-dee-OH-moo nehl-ZYAH pee-ree-vees-TEE SLOH-vah v SLOH-vah, noh aht-TYEH-nahk sahkh-rah-NEETY MOHZH-nah.", "An idiom cannot be translated word for word, but the shade can be preserved."),
                X("Перевод потерял интонацию, хотя смысл остался.", "pee-ree-VOHT pah-teh-RYAHL een-tah-NAH-tsee-yoo, khah-TYAH SMIHSl ah-STAHl-syah.", "The translation lost the intonation, though the sense remained.")],
                [("Идиому перевели слово в слово, и стало смешно.", "Идиому передали по смыслу.", "An idiom is rendered by sense, not by word."),
                 ("Перевод потерял интонацию и смысл и подтекст и всё остальное.", "Перевод потерял интонацию, хотя смысл остался.", "Name one loss and keep the rest for the next sentence.")]),
              [D("Критик", "Что потерял этот перевод?", "shtoh pah-teh-RYAHL EH-taht pee-ree-VOHT?", "What did this translation lose?"),
               D("Переводчица", "Интонацию. Смысл остался, подтекст частично.", "een-tah-NAH-tsee-yoo. SMIHSl ah-STAHl-syah, PAHd-tyehkst chahs-TEECH-nah.", "The intonation. The sense remained, the subtext in part."),
               D("Критик", "А как вы передали «тоску»?", "ah kahk vih pee-ree-dah-LEE tahs-KOO?", "And how did you render 'тоска'?"),
               D("Переводчица", "Описательно, в сноске: иначе читатель теряет ритм.", "ahp-ee-SAH-tehl-nah, v SNOHs-kyeh: ee-NAH-cheh chee-TAH-teel TYEH-ryah-yeht reetm.", "Descriptively, in a footnote: otherwise the reader loses the rhythm.")],
              WS("Culture in translation worksheet", [
                  T("Name the strategy.", ["'дача' is rendered as 'country house' or explained in a footnote", "an idiom cannot be translated word for word"],
                    ["«Дача» передаётся как 'country house' или объясняется в сноске", "Идиому нельзя перевести слово в слово"]),
                  T("Report the loss.", ["the translation lost the intonation, though the sense remained", "descriptively, in a footnote"],
                    ["Перевод потерял интонацию, хотя смысл остался", "Описательно, в сноске"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Русский язык остаётся языком науки и межнационального общения на "
                 "постсоветском пространстве: Русский язык как иностранный (РКИ) "
                 "преподают более чем в восьмидесяти странах, а в Центральной Азии русский "
                 "работает как язык-посредник там, где соседствуют десятки языков. Для "
                 "переводчика это значит, что за русским стоят не только литература и "
                 "наука, но и повседневная практика общежития — от объявления в "
                 "поликлинике до протокола слушаний."),
        source_url="https://en.wikipedia.org/wiki/Russian_language",
        reading=("Перевод — это не замена слов, а выбор стратегии. В договоре «заказчик» и "
                 "«исполнитель» имеют точные соответствия, и здесь буквальный перевод "
                 "работает. В романе те же слова звучат иначе: важен оттенок, а не "
                 "термин. Наконец, есть слова-реалии — «дача», «тоска», «интеллигенция», — "
                 "для которых приходится либо подбирать приблизительное соответствие, либо "
                 "оставлять их без перевода и объяснять в сноске. Именно поэтому перевод "
                 "одного и того же текста для суда и для журнала — две разные работы, и "
                 "обе требуют обоснования."),
        reading_gloss=("Translation is not the replacement of words but the choice of a "
                       "strategy. In a contract 'заказчик' and 'исполнитель' have exact "
                       "equivalents, and there a literal translation works. In a novel the "
                       "same words sound different: the shade matters, not the term. "
                       "Finally, there are culture-specific words — 'дача', 'тоска', "
                       "'интеллигенция' — for which one must either find an approximate "
                       "equivalent or leave them untranslated and explain in a footnote. That "
                       "is exactly why translating the same text for a court and for a "
                       "magazine are two different jobs, and both require justification."),
        listening=("Благодарю за вопрос. Отвечу в двух частях: сначала метод, потом "
                   "ограничение. Уточню, что выборка была городской. — Достаточно. — Тогда "
                   "по существу: эффект зависит от обучения."),
        listening_gloss=("Thank you for the question. I will answer in two parts: first the "
                         "method, then the limitation. Let me clarify that the sample was "
                         "urban. — That is enough. — Then to the point: the effect depends on "
                         "training."),
        voice_tag=VOICE,
        idioms=[
            ("по существу", "on the essence", "to the point, substantively"),
            ("в зависимости от", "in dependence on", "depending on"),
            ("ложный друг", "a false friend", "a word that misleads between two languages"),
            ("слово в слово", "word for word", "literally, exactly"),
            ("иметь в виду", "to have in mind", "to keep in view"),
            ("сводиться к", "to reduce itself to", "to come down to"),
            ("ставить точку", "to put a full stop", "to end the discussion"),
            ("привести в соответствие", "to bring into correspondence", "to align with a rule"),
            ("с поправкой на", "with a correction for", "allowing for"),
            ("в конечном счёте", "in the final count", "ultimately"),
        ],
        mistakes=[
            ("В соответствии регламента, проект подлежит проверке.", "В соответствии с регламентом, проект подлежит проверке.", "В соответствии с takes the instrumental."),
            ("Замените канцелярит к глаголу.", "Замените канцелярит на глагол.", "Заменить takes на + accusative."),
            ("Показатель вырос на пяти процентов.", "Показатель вырос на пять процентов.", "На takes the accusative after вырос."),
        ],
        task_title="Аннотация, правка и решение",
        task_instructions=("Take a text you know and do three things with it: write an "
                           "abstract in four moves (в статье рассматривается, цель работы, "
                           "методом, автор приходит к выводу), make two editorial decisions "
                           "with заменить на and сократить до, and state one public decision "
                           "по итогам обсуждения. Then reread the whole page and mark every "
                           "claim with its source: согласно, по словам, по данным or "
                           "в протоколе зафиксировано."),
    ),
    "test": [
        ("translate_en", "Say: the author concludes that the effect depends on training.", "Автор приходит к выводу, что эффект зависит от обучения."),
        ("translate_ru", "Согласно отчёту, срок был нарушен.", "According to the report, the deadline was missed."),
        ("multiple_choice", "Which sentence states compliance with a rule?", "Документы соответствуют требованиям нормы."),
        ("fill_in_the_blank", "В соответствии ___ регламентом, проект подлежит проверке.", "с"),
        ("word_selection", "Select the Russian for 'margin of error'.", "погрешность"),
        ("error_correction", "Замените канцелярит к глаголу.", "Замените канцелярит на глагол."),
        ("dialogue_completion", "Complete: Есть вопросы к докладчику? — ___ (I will answer in two parts)", "Отвечу в двух частях"),
        ("matching", "Match замечание to its meaning.", "remark, objection"),
        ("reading_comprehension", "В тексте, почему перевод для суда и для журнала — разные работы?", "because the strategy and the justification differ"),
        ("inference", "Текст говорит, что реалию можно оставить без перевода и объяснить. What does that tell us about translation?", "the explanation can be the translation"),
        ("main_idea", "В тексте объясняется выбор переводческой стратегии. — what is this sentence?", "the main point of the reading"),
        ("detail_identification", "Какие примеры слов-реалий приводит текст?", "дача, тоска, интеллигенция"),
    ],
}

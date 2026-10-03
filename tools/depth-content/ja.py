# -*- coding: utf-8 -*-
"""Japanese PHASE 1 depth — extras, third lessons, half-step rungs.

Written with the DSL in `tools/depth_kit.py`; rendered by
`tools/author-depth.py --lang ja`.

House style follows the shipped Japanese course: kana and kanji in `t`,
Hepburn-style romanisation in `r` (phonetic: は is romanised `wa`, を is `o`),
English in `en`. Unit ids keep the shipped course's scheme (`A1-U1` for the
CEFR rungs, `ja-c1-u1` for C1/C2); half-step rungs use `<rung>-U1`.

Register note: the A1-B1 rungs stay in the polite です・ます register the
shipped course teaches, and keigo is recognised in B2 and used deliberately
in C1/C2 — never mixed into a plain sentence. The voice tag is the site's own
`ja-JA` (see `js/voice-languages.js`).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # tools/ on the path
from depth_kit import D, EXTRA, G, L, T, V, WS, X   # noqa: E402

CODE = "ja"
NAME = "Japanese"
NATIVE = "日本語"
PHASE = 1
SCRIPT = "Japanese script"
VOICE = "ja-JA"
SKILL = ("Japanese: kana and kanji, particles は/が/を/に, です・ます politeness, "
         "verb-final order, counters and keigo")

EXTRAS = {}
THIRD = {}
HALFSTEPS = {}

EXTRAS["A1"] = EXTRA(
    culture=("Japanese is written in three scripts at once: hiragana for grammar, katakana for "
             "borrowed words such as コーヒー, and kanji for meaning. わたしは学生です carries all "
             "three. Politeness is built into the sentence rather than added to it — です and ます "
             "keep a first conversation safe, and dropping them sounds blunt. すみません does most "
             "of the work in public life: it is an apology, an excuse-me and a thank-you for "
             "trouble, and you will hear it a dozen times a day."),
    source_url="https://en.wikipedia.org/wiki/Japanese_language",
    reading=("ゆきです。とうきょうに すんでいます。まいにち でんしゃで がっこうへ いきます。"
             "あさは コーヒーを のみます。ひるごはんは いつも べんとうです。よるは うちで "
             "にほんごを べんきょうします。すこし むずかしいですが、たのしいです。"),
    reading_gloss=("I am Yuki. I live in Tokyo. Every day I go to school by train. In the morning "
                   "I drink coffee. For lunch I always have a bento. In the evening I study "
                   "Japanese at home. It is a little difficult, but it is fun."),
    listening=("ゆき: おはようございます。たろうさんも がっこうへ いきますか。<br>"
               "たろう: いいえ、きょうは うちで べんきょうします。<br>"
               "ゆき: そうですか。じゃ、また あした。<br>"
               "たろう: また あした。おげんきで。"),
    listening_gloss=("Yuki: Good morning. Are you going to school too, Taro? Taro: No, today I "
                     "study at home. Yuki: I see. See you tomorrow, then. Taro: See you "
                     "tomorrow. Take care."),
    voice_tag=VOICE,
    idioms=[
        ("こんにちは", "konnichiwa", "hello (daytime)"),
        ("はじめまして", "hajimemashite", "nice to meet you (first time)"),
        ("よろしく おねがいします", "yoroshiku onegaishimasu", "please treat me well / please"),
        ("おねがいします", "onegaishimasu", "please (request)"),
        ("すみません", "sumimasen", "excuse me / sorry / thanks for the trouble"),
        ("ありがとう ございます", "arigatou gozaimasu", "thank you (polite)"),
        ("いただきます", "itadakimasu", "said before eating"),
        ("いってきます", "ittekimasu", "said when leaving home"),
        ("ただいま", "tadaima", "said on coming home"),
        ("おげんきですか", "ogenki desu ka", "how are you?"),
    ],
    mistakes=[
        ("わたしは ゆきです か。", "わたしは ゆきですか。", "です carries the question particle か directly; no pause before it."),
        ("ありがとう ございます です。", "ありがとう ございます。", "ございます is already polite — adding です doubles the ending."),
        ("すみません、コーヒー を ください です。", "すみません、コーヒーを ください。", "ください ends the request; です does not follow it."),
    ],
    task_title="Introduce yourself in four sentences",
    task_instructions=("Write the four sentences you would need on the first day of a class in "
                       "Japan: your name with です, where you live with に すんでいます, one thing "
                       "you do every day with を + ます, and one closing line with よろしく "
                       "おねがいします. Read them aloud twice; if a sentence has no です or ます, "
                       "decide deliberately whether you meant it to be plain."),
)

EXTRAS["A2"] = EXTRA(
    culture=("The convenience store and the station are the two rooms of Japanese daily life: at "
             "the konbini you pay at a counter facing the door, the staff say いらっしゃいませ, and "
             "おねがいします closes your side of the exchange. Trains keep to the minute and the "
             "announcement tells you which door opens. むりょう (free) and かくやす (cheap) are "
             "shouted from shop fronts, and the useful skill is asking いくらですか without "
             "repeating the noun."),
    source_url="https://en.wikipedia.org/wiki/Japanese_cuisine",
    reading=("きのう えきで きっぷを かいました。みどりの まどぐちは こんでいましたから、"
             "じどうはんばいきで かいました。とうきょうまで さんびゃくえん でした。"
             "でんしゃは おくれませんでした。つぎは ひるごはんを コンビニで かいます。"),
    reading_gloss=("Yesterday I bought a ticket at the station. The green counter was crowded, so "
                   "I bought it at the vending machine. It was three hundred yen to Tokyo. The "
                   "train was not late. Next I will buy lunch at the convenience store."),
    listening=("てんいん: いらっしゃいませ。<br>"
               "ゆき: すみません、この おべんとうは いくらですか。<br>"
               "てんいん: ごひゃくえん です。<br>"
               "ゆき: じゃ、これを おねがいします。"),
    listening_gloss=("Shop assistant: Welcome. Yuki: Excuse me, how much is this bento? "
                     "Assistant: It is five hundred yen. Yuki: Then this one, please."),
    voice_tag=VOICE,
    idioms=[
        ("いくらですか", "ikura desu ka", "how much is it?"),
        ("これを ください", "kore o kudasai", "this one, please"),
        ("おねがいします", "onegaishimasu", "please (ordering, asking)"),
        ("ちょっと まってください", "chotto matte kudasai", "please wait a moment"),
        ("だいじょうぶです", "daijoubu desu", "it is fine / I am all right"),
        ("おすすめは なんですか", "osusume wa nan desu ka", "what do you recommend?"),
        ("みちに まよいました", "michi ni mayoimashita", "I got lost"),
        ("〜は どこですか", "~ wa doko desu ka", "where is ~?"),
        ("べんとう", "bentou", "boxed lunch"),
        ("きっぷ", "kippu", "ticket"),
    ],
    mistakes=[
        ("コーヒー が ください。", "コーヒーを ください。", "ください takes を: the thing requested is the object."),
        ("えき に いきます です。", "えきに いきます。", "ます verbs are already polite; です does not follow."),
        ("いくら です か この はん。", "この はんは いくらですか。", "The topic comes first; か closes the sentence."),
    ],
    task_title="Buy a ticket and lunch in Japanese",
    task_instructions=("Write both halves of two short exchanges: at the ticket machine (asking "
                       "for the fare to one station, paying, thanking) and at the konbini (asking "
                       "the price of one item, asking for it, saying thank you). Use すみません "
                       "once per exchange. Then say the same two exchanges aloud, replacing the "
                       "noun with a different item each time, so the frame rather than the "
                       "vocabulary is what you remember."),
)

EXTRAS["B1"] = EXTRA(
    culture=("Keigo is not a separate language but a set of choices about where the other person "
             "stands: いらっしゃる for their coming, うかがう for your going, いただく for your "
             "receiving, さしあげる for your giving. The office day is bracketed by おつかれさまです "
             "at the end and おはようございます at the start, and a request between colleagues is "
             "usually a て-form plus もらえますか rather than an imperative."),
    source_url="https://en.wikipedia.org/wiki/Honorific_speech_in_Japanese",
    reading=("あしたは ぶちょうに ほうこくします。まず データを かくにんして、それから "
             "スライドを つくります。むずかしい てんは そうだんしたいと おもいます。"
             "おそくなる かもしれませんから、さきに メールを おくります。"),
    reading_gloss=("Tomorrow I will report to the department manager. First I will check the data, "
                   "then make the slides. I think I want to discuss the difficult points. Since I "
                   "may be late, I will send an email in advance."),
    listening=("たろう: あしたの かいぎ、でられますか。<br>"
               "ゆき: すみません、ごごは むりです。あさなら だいじょうぶです。<br>"
               "たろう: じゃ、あさに しましょう。おつかれさまです。<br>"
               "ゆき: おつかれさまです。"),
    listening_gloss=("Taro: Can you attend tomorrow's meeting? Yuki: Sorry, the afternoon is "
                     "impossible for me. The morning is fine. Taro: Then let us make it the "
                     "morning. Thank you for your work. Yuki: Thank you for your work."),
    voice_tag=VOICE,
    idioms=[
        ("と おもいます", "to omoimasu", "I think that …"),
        ("かもしれません", "kamo shiremasen", "it may be that …"),
        ("たことが あります", "ta koto ga arimasu", "I have done … before"),
        ("てみます", "te mimasu", "I will try doing …"),
        ("おつかれさまです", "otsukaresama desu", "thank you for your work"),
        ("いそがしいです", "isogashii desu", "I am busy"),
        ("よてい", "yotei", "plan, schedule"),
        ("やくそく", "yakusoku", "appointment, promise"),
        ("そうだんします", "soudan shimasu", "I will consult you"),
        ("さきに", "saki ni", "in advance, first"),
    ],
    mistakes=[
        ("あした かいぎに でますと おもいます。", "あした かいぎに でると おもいます。", "と おもいます takes the plain form, not ます."),
        ("にほんへ いったが あります。", "にほんへ いったことが あります。", "Experience takes たことが あります."),
        ("てみる します。", "やってみます。", "てみる attaches to the verb: やってみます."),
    ],
    task_title="Write tomorrow's plan with two hedges",
    task_instructions=("Write five lines in Japanese about tomorrow: two things you will do "
                       "(plain form + と おもいます), one thing that may happen (かもしれません), one "
                       "thing you have done before (たことが あります) and one request to a "
                       "colleague with the て-form + もらえますか. Then rewrite the middle line as "
                       "あした いそがしいです and notice how much the hedge was doing."),
)

EXTRAS["B2"] = EXTRA(
    culture=("Japanese business writing keeps the decision and the relationship in separate "
             "clauses: 検討します (we will consider it) is a soft no, and ぜひ おねがいします is a "
             "warm yes; a proposal is checked by everyone it touches before anyone agrees out "
             "loud. させていただきます asks permission in the grammar itself, so a service is "
             "offered without a claim of power. Reading these as evasion misses the point: they "
             "are the sentence shapes that let a group decide together."),
    source_url="https://en.wikipedia.org/wiki/Etiquette_in_Japan",
    reading=("かくぶちょうに ていあんを おくりました。「けんとうします」という へんじは、"
             "たいてい まだ けってい していないという いみです。ですから つぎの かいぎで "
             "もういちど せつめいして、データを ふやしました。えいぎょうは わりあいで みる "
             "べきです。"),
    reading_gloss=("I sent the proposal to the section manager. A reply of 'we will consider it' "
                   "usually means that nothing has been decided yet. So at the next meeting I "
                   "explained it once more and added more data. Sales should be judged as a "
                   "ratio."),
    listening=("たろう: その ていあんは どうですか。<br>"
               "ゆき: たしかに いい てんも ありますが、コストが ふあんていです。<br>"
               "たろう: つまり、いまは まだ むりですか。<br>"
               "ゆき: データを ふやせば、つぎの かいぎで はなせます。"),
    listening_gloss=("Taro: How is that proposal? Yuki: Certainly it has good points, but the cost "
                     "is unstable. Taro: In other words, it is still impossible now? Yuki: If we "
                     "add more data, we can discuss it at the next meeting."),
    voice_tag=VOICE,
    idioms=[
        ("たしかに", "tashika ni", "certainly, it is true that"),
        ("にも かかわらず", "ni mo kakawarazu", "despite …"),
        ("つまり", "tsumari", "in other words"),
        ("〜べきです", "~ beki desu", "one should …"),
        ("させて いただきます", "sasete itadakimasu", "I will (humbly) do …"),
        ("おそれいりますが", "osoreirimasu ga", "I am sorry to trouble you, but"),
        ("けんとうします", "kentou shimasu", "we will consider it"),
        ("ふあんてい", "fuantei", "unstable"),
        ("わりあい", "wariai", "ratio, proportion"),
        ("だいたい", "daitai", "roughly"),
    ],
    mistakes=[
        ("コストが たかい にも かかわらず、らいしゅう はじめます。", "コストが たかいにも かかわらず、らいしゅう はじめます。", "にも かかわらず attaches to the plain form, with no pause."),
        ("わりあい を みる べきです。", "わりあいで みる べきです。", "The measure takes で: judge by the ratio."),
        ("させていただきます です。", "させて いただきます。", "いただきます is already the polite form."),
    ],
    task_title="Turn one soft no into a plan",
    task_instructions=("Take a real reply you have received that sounded like 検討します and write "
                       "the Japanese you would send back: one line agreeing with the good point "
                       "(たしかに …), one line naming the obstacle (…が、…), one line asking for "
                       "the one thing that would unblock it, and one line offering to do it "
                       "yourself with させて いただきます. Then write the same four lines as a note "
                       "to yourself in English and compare what the Japanese left unsaid."),
)

EXTRAS["C1"] = EXTRA(
    culture=("Written Japanese locates the speaker's stance in the grammar before the claim: "
             "〜とのことだ reports without vouching, 〜に至る describes a path rather than a cause, "
             "and 〜とはいえ concedes without surrendering. A C1 reader notices which of these is "
             "missing: a sentence with a bare assertion and no frame reads as either naive or "
             "deliberately aggressive, and Japanese editors will ask for the frame rather than "
             "the evidence."),
    source_url="https://en.wikipedia.org/wiki/Japanese_grammar",
    reading=("ちょうさに よると、りようしゃの はんぶんが アプリを つかっているとのことだ。"
             "とはいえ、むりの ない はんいで いえば、こんごも てんじょうは つづくと みられる。"
             "ほうこくしょでは、げんいんを きゅうそくに きめるのではなく、かんれんを "
             "のべる べきだ。"),
    reading_gloss=("According to the survey, half of the users are said to be using the app. That "
                   "said, speaking within a reasonable range, the rise is expected to continue. "
                   "In the report one should not settle the cause hastily but state the "
                   "correlation."),
    listening=("編集者: その けつろんは つよいですか。<br>"
               "分析者: いいえ、かんれんは いえますが、げんいんは いえません。<br>"
               "編集者: じゃ、ひょうげんを おさえますか。<br>"
               "分析者: はい。〜とのことだ、に します。"),
    listening_gloss=("Editor: Is that conclusion strong? Analyst: No, we can state a correlation "
                     "but not a cause. Editor: Then shall we soften the wording? Analyst: Yes, "
                     "let us use 'it is reported that'."),
    voice_tag=VOICE,
    idioms=[
        ("〜とのことだ", "~ to no koto da", "it is said that (reported, not vouched for)"),
        ("〜とはいえ", "~ to wa ie", "that said, although"),
        ("〜に よると", "~ ni yoru to", "according to …"),
        ("〜に 至る", "~ ni itaru", "to reach (a stage, a conclusion)"),
        ("かんれん", "kanren", "correlation, connection"),
        ("きゅうそくに", "kyuusoku ni", "hastily"),
        ("ひょうげんを おさえる", "hyougen o osaeru", "to restrain the wording"),
        ("みられる", "mirareru", "it is observed / is seen"),
        ("はんいで いえば", "han'i de ieba", "speaking within the range"),
        ("ない かぎり", "nai kagiri", "unless …"),
    ],
    mistakes=[
        ("ちょうさに よると、はんぶんが つかっている そうです だ。", "ちょうさに よると、はんぶんが つかっているとのことだ。", "Reported evidence takes とのことだ; そうです だ doubles the ending."),
        ("たかい とはいえ、かいます。", "たかいとはいえ、かいます。", "とはいえ attaches directly to the plain form."),
        ("げんいん を いえます。", "かんれん を いえます。", "Two figures moving together gives correlation; cause needs its own evidence."),
    ],
    task_title="Write one paragraph that states a correlation without a cause",
    task_instructions=("Find a figure in a report you have read this month. Write six lines in "
                       "Japanese: the source with 〜に よると, the figure with 〜とのことだ, the "
                       "concession with 〜とはいえ, what is observed with みられる, the limit with "
                       "「かんれんは いえるが、げんいんは いえない」, and one line on what would "
                       "make the causal claim possible. If any line claims more than the evidence "
                       "carries, rewrite it."),
)

EXTRAS["C2"] = EXTRA(
    culture=("Japanese has a vocabulary for exactly the things translation loses: 木漏れ日 (light "
             "through leaves), 甘える (to lean on someone's kindness), おもてなし (the whole of "
             "hospitality), わびさび. A C2 writer treats them as untranslatable on purpose — keeps "
             "the word, glosses the sense, and records the gap, the way a museum labels an object "
             "it will not move. The same discipline governs rhythm: 体言止め (ending on a noun) and "
             "inversion carry the emphasis that English puts in stress."),
    source_url="https://en.wikipedia.org/wiki/Japanese_literature",
    reading=("おもてなし、という ことばは せつめい しにくい。きゃくを まつ じかん そのものが "
             "おもてなし だからだ。えいごでは hospitality と やくされるが、その ことばが "
             "ふくむ ちんもく と まつ ことは うつらない。やくす のではなく、ことばを そのまま "
             "のこして、かっこで せつめいする ほうが しんじつに ちかい。"),
    reading_gloss=("The word omotenashi is hard to explain. That is because the very time of "
                   "waiting for a guest is omotenashi. It is translated as 'hospitality', but the "
                   "silence and the waiting that the word contains do not carry over. Rather than "
                   "translating, leaving the word as it is and explaining it in brackets is "
                   "closer to the truth."),
    listening=("調停者: その ことば、えいごで いえますか。<br>"
               "査読者: いえ、ちかづけますが、おなじには なりません。<br>"
               "調停者: じゃ、ことばを のこして、やくを つけますか。<br>"
               "査読者: はい。かっこの なかの やくは、ものたりなさ も かきます。"),
    listening_gloss=("Mediator: Can you say that word in English? Reviewer: No, one can get close, "
                     "but it does not become the same. Mediator: Then shall we keep the word and "
                     "attach a gloss? Reviewer: Yes. In the gloss in brackets I also write what "
                     "falls short."),
    voice_tag=VOICE,
    idioms=[
        ("木漏れ日", "komorebi", "sunlight through leaves"),
        ("甘える", "amaeru", "to lean on someone's kindness"),
        ("おもてなし", "omotenashi", "hospitality, whole-hearted hosting"),
        ("わびさび", "wabisabi", "beauty in spareness and age"),
        ("ものたりない", "monotarinai", "to fall short, to leave something missing"),
        ("いいかえれば", "iikaereba", "if we put it another way"),
        ("みっせつに", "missetsu ni", "closely, densely"),
        ("よっきゅう", "yokkyuu", "appetite, craving (for meaning)"),
        ("うつる", "utsuru", "to carry over, to be transferred"),
        ("ちんもく", "chinmoku", "silence"),
    ],
    mistakes=[
        ("その ことばは やくせますが、おなじ いみに なります。", "その ことばは やくせますが、おなじ いみには なりません。", "Untranslatability is a negative claim: …には なりません."),
        ("ことば を のこす ほうが しんじつに ちかい です。", "ことばを のこす ほうが しんじつに ちかい。", "ほうが … ちかい ends in the plain form; no です."),
        ("やく を つけますか, かっこ の なか に やく。", "ことばを のこして、かっこに やくを つけます。", "Japanese does not stack comma-separated fragments; the te-form links the two actions."),
    ],
    task_title="Gloss five untranslatable words and record the gap",
    task_instructions=("Choose five Japanese words with no single English equivalent — 木漏れ日, "
                       "甘える, おもてなし and two of your own. For each, write three lines: the "
                       "word in Japanese, a twenty-word English gloss that gets as close as it "
                       "can, and a note beginning ものたりない: that names what the gloss dropped. "
                       "Then write one sentence of your own using two of the five, in a register "
                       "where they belong (a letter, a review, a spoken aside), and read it aloud "
                       "for rhythm rather than meaning."),
)

THIRD["A1"] = [
    ("A1-U1", "ja-a1-l7", L("あいさつの じかん: おはよう・こんばんは",
        "Greetings change with the clock, not with the person: おはようございます in the morning, "
        "こんにちは in the day, こんばんは after dark, おやすみなさい before sleep. Leaving "
        "early takes its own sentence, おさきに しつれいします.",
        [V("おはようございます", "ohayou gozaimasu", "good morning (polite)", "phrase"),
         V("こんばんは", "konbanwa", "good evening", "phrase"),
         V("おやすみなさい", "oyasuminasai", "good night", "phrase"),
         V("おさきに しつれいします", "osaki ni shitsurei shimasu", "excuse me for leaving first", "phrase"),
         V("じゃあ また", "jaa mata", "see you, then", "phrase")],
        G("Greeting by time",
          "あさ: おはようございます · ひる: こんにちは · よる: こんばんは · でるとき: おさきに しつれいします",
          "The greeting is chosen by the time of day and the leave-taking by the situation. A "
          "sentence can carry a greeting and a request together: おはようございます、きょうも "
          "よろしく おねがいします.",
          [X("おはようございます。きょうも よろしく おねがいします。", "Ohayou gozaimasu. Kyou mo yoroshiku onegaishimasu.", "Good morning. Please treat me well today too."),
           X("おさきに しつれいします。", "Osaki ni shitsurei shimasu.", "Excuse me for leaving before you."),
           X("じゃあ また あした。", "Jaa mata ashita.", "See you tomorrow, then.")],
          [("こんにちは、おやすみなさい。", "こんばんは。おやすみなさい。", "One greeting per situation; おやすみなさい belongs at bedtime."),
           ("おさきに しつれいしました。", "おさきに しつれいします。", "The leave-taking is said as you go: present, not past.")]),
        [D("ゆき", "おはようございます。", "Ohayou gozaimasu.", "Good morning."),
         D("たろう", "おはようございます。きょうも よろしく おねがいします。", "Ohayou gozaimasu. Kyou mo yoroshiku onegaishimasu.", "Good morning. Please treat me well today too."),
         D("ゆき", "わたしは おさきに しつれいします。", "Watashi wa osaki ni shitsurei shimasu.", "I will leave before you."),
         D("たろう", "おつかれさまでした。じゃあ また あした。", "Otsukaresama deshita. Jaa mata ashita.", "Thank you for your work. See you tomorrow, then.")],
        WS("Greeting worksheet", [
            T("Greet by the clock.", ["good morning (polite)", "good evening"],
              ["おはようございます", "こんばんは"]),
            T("Leave the room.", ["excuse me for leaving first", "see you tomorrow, then"],
              ["おさきに しつれいします", "じゃあ また あした"]),
        ]))),
    ("A1-U2", "ja-a1-l8", L("じかん: いま なんじですか",
        "The clock is asked for with なんじ and answered with the counter じ: いちじ、にじ、さんじ. "
        "Half past takes はん, and a span of time takes …から …まで.",
        [V("なんじ", "nanji", "what time", "noun"),
         V("はん", "han", "half past", "noun"),
         V("ごぜん", "gozen", "a.m.", "noun"),
         V("ごご", "gogo", "p.m.", "noun"),
         V("から … まで", "kara … made", "from … until", "phrase")],
        G("Telling time",
          "いま なんじですか · くじはん です · ごぜん しちじに おきます · くじから ごじまで",
          "The hour takes the counter じ and the minute ふん; a time at which something happens "
          "takes に, and a span takes から and まで. はん covers half past and nothing else.",
          [X("いま くじはん です。", "Ima kuji han desu.", "It is half past nine."),
           X("ごぜん しちじに おきます。", "Gozen shichi ji ni okimasu.", "I get up at seven a.m."),
           X("くじから ごじまで べんきょうします。", "Kuji kara goji made benkyou shimasu.", "I study from nine until five.")],
          [("いま なんじ ですか はん。", "いま なんじですか。", "か closes the question; the answer carries はん."),
           ("しちじ から おきます。", "しちじに おきます。", "A point in time takes に; から needs a まで.")]),
        [D("たろう", "すみません、いま なんじですか。", "Sumimasen, ima nanji desu ka.", "Excuse me, what time is it now?"),
         D("ゆき", "くじはん です。", "Kuji han desu.", "It is half past nine."),
         D("たろう", "ありがとう ございます。かいぎは なんじからですか。", "Arigatou gozaimasu. Kaigi wa nanji kara desu ka.", "Thank you. What time does the meeting start?"),
         D("ゆき", "じゅうじから じゅうにじまで です。", "Juuji kara juuniji made desu.", "From ten until twelve.")],
        WS("Time worksheet", [
            T("Say the time.", ["it is half past nine", "I get up at seven a.m."],
              ["くじはん です", "ごぜん しちじに おきます"]),
            T("Give the span.", ["from nine until five", "from ten until twelve"],
              ["くじから ごじまで", "じゅうじから じゅうにじまで"]),
        ]))),
    ("A1-U3", "ja-a1-l9", L("すきな こと: 〜が すきです",
        "Likes are stated with が: おんがくが すきです. Skill takes じょうず and へた, and a mild "
        "dislike is expressed by あまり with a negative, never by きらい in company.",
        [V("すき", "suki", "liked, favourite", "adjective"),
         V("きらい", "kirai", "disliked", "adjective"),
         V("じょうず", "jouzu", "skilful", "adjective"),
         V("へた", "heta", "unskilful", "adjective"),
         V("あまり", "amari", "not very (with a negative)", "adverb")],
        G("Likes and skill",
          "わたしは おんがくが すきです · うたが じょうずです · あまり たべません",
          "The liked thing takes が and すきです behaves as an adjective; skill takes じょうず/へた "
          "the same way. あまり pairs with a negative verb and softens it: あまり じょうずでは "
          "ありません.",
          [X("わたしは おんがくが すきです。", "Watashi wa ongaku ga suki desu.", "I like music."),
           X("あまり うたが じょうずでは ありません。", "Amari uta ga jouzu de wa arimasen.", "I am not very good at singing."),
           X("どんな たべものが すきですか。", "Donna tabemono ga suki desu ka.", "What kind of food do you like?")],
          [("わたしは おんがく を すきです。", "わたしは おんがくが すきです。", "Likes take が, not を."),
           ("あまり すきです。", "あまり すきでは ありません。", "あまり needs a negative to lean on.")]),
        [D("ゆき", "たろうさんは おんがくが すきですか。", "Tarou-san wa ongaku ga suki desu ka.", "Taro, do you like music?"),
         D("たろう", "はい、すきです。でも、あまり うたが じょうずでは ありません。", "Hai, suki desu. Demo, amari uta ga jouzu de wa arimasen.", "Yes, I like it. But I am not very good at singing."),
         D("ゆき", "どんな おんがくが すきですか。", "Donna ongaku ga suki desu ka.", "What kind of music do you like?"),
         D("たろう", "ジャズが すきです。", "Jazu ga suki desu.", "I like jazz.")],
        WS("Likes worksheet", [
            T("State a like and a skill.", ["I like music", "I am not very good at singing"],
              ["わたしは おんがくが すきです", "あまり うたが じょうずでは ありません"]),
            T("Ask and answer.", ["what kind of food do you like?", "I like jazz"],
              ["どんな たべものが すきですか", "ジャズが すきです"]),
        ]))),
]

THIRD["A2"] = [
    ("A2-U1", "ja-a2-l7", L("びょういん: おなかが いたいです",
        "A clinic visit states the place that hurts with が and いたいです, describes the fever "
        "with ねつが あります, and receives the instruction in the て-form: この くすりを のんで "
        "ください. Rest is reported with やすみます.",
        [V("いたい", "itai", "painful, hurts", "adjective"),
         V("ねつ", "netsu", "fever", "noun"),
         V("くすり", "kusuri", "medicine", "noun"),
         V("びょういん", "byouin", "hospital, clinic", "noun"),
         V("やすみます", "yasumimasu", "to rest, to take a day off", "verb")],
        G("Saying what hurts",
          "おなかが いたいです · ねつが あります · この くすりを のんで ください · きょうは やすみます",
          "The body part takes が; いたいです is an adjective and takes no object. The "
          "instruction arrives in the て-form + ください, and the answer states what you will do "
          "in the ます form.",
          [X("おなかが いたいです。", "Onaka ga itai desu.", "My stomach hurts."),
           X("この くすりを のんで ください。", "Kono kusuri o nonde kudasai.", "Please take this medicine."),
           X("きょうは うちで やすみます。", "Kyou wa uchi de yasumimasu.", "Today I will rest at home.")],
          [("おなか を いたいです。", "おなかが いたいです。", "Body parts take が with いたい."),
           ("ねつ が あります です。", "ねつが あります。", "あります ends the sentence; です does not follow it.")]),
        [D("ゆき", "どうしましたか。", "Dou shimashita ka.", "What is the matter?"),
         D("たろう", "おなかが いたいです。ねつも あります。", "Onaka ga itai desu. Netsu mo arimasu.", "My stomach hurts. I have a fever too."),
         D("ゆき", "この くすりを のんで ください。", "Kono kusuri o nonde kudasai.", "Please take this medicine."),
         D("たろう", "はい。きょうは やすみます。ありがとう ございます。", "Hai. Kyou wa yasumimasu. Arigatou gozaimasu.", "Yes. I will rest today. Thank you.")],
        WS("Clinic worksheet", [
            T("Describe the symptoms.", ["my stomach hurts", "I have a fever too"],
              ["おなかが いたいです", "ねつも あります"]),
            T("Give and take the advice.", ["please take this medicine", "today I will rest"],
              ["この くすりを のんで ください", "きょうは やすみます"]),
        ]))),
    ("A2-U2", "ja-a2-l8", L("でんしゃと きっぷ: 〜まで いくらですか",
        "A fare is asked with まで: しんじゅくまで いくらですか. The platform takes で, the train "
        "takes に, and a change of trains takes を: でんしゃを のりかえます.",
        [V("きっぷ", "kippu", "ticket", "noun"),
         V("のりば", "noriba", "platform, boarding place", "noun"),
         V("のりかえ", "norikae", "transfer, change", "noun"),
         V("まにあう", "maniau", "to be in time", "verb"),
         V("じどうはんばいき", "jidouhanbaiki", "vending machine", "noun")],
        G("Tickets and platforms",
          "〜まで いくらですか · 〜で のりば を まちます · でんしゃを のりかえます · 〜に のります",
          "The destination takes まで for distance and に for arrival; boarding takes に and "
          "changing takes を. まにあう takes に: でんしゃに まにあいます.",
          [X("しんじゅくまで いくらですか。", "Shinjuku made ikura desu ka.", "How much is it to Shinjuku?"),
           X("つぎの でんしゃに のります。", "Tsugi no densha ni norimasu.", "I will take the next train."),
           X("のりかえは いちど です。", "Norikae wa ichido desu.", "There is one change.")],
          [("しんじゅく へ いくらですか。", "しんじゅくまで いくらですか。", "A fare takes まで, not へ."),
           ("でんしゃに のりかえます。", "でんしゃを のりかえます。", "Changing trains takes を: the first train is what you leave.")]),
        [D("たろう", "しんじゅくまで いくらですか。", "Shinjuku made ikura desu ka.", "How much is it to Shinjuku?"),
         D("ゆき", "にひゃくえん です。のりかえは いちど です。", "Nihyaku en desu. Norikae wa ichido desu.", "It is two hundred yen. There is one change."),
         D("たろう", "どの でんしゃですか。", "Dono densha desu ka.", "Which train is it?"),
         D("ゆき", "にばん のりばの でんしゃです。", "Niban noriba no densha desu.", "The train at platform two.")],
        WS("Station worksheet", [
            T("Ask the fare and the change.", ["how much is it to Shinjuku?", "there is one change"],
              ["しんじゅくまで いくらですか", "のりかえは いちど です"]),
            T("Name the train.", ["I will take the next train", "the train at platform two"],
              ["つぎの でんしゃに のります", "にばん のりばの でんしゃです"]),
        ]))),
    ("A2-U3", "ja-a2-l9", L("ふく: サイズと いろ",
        "Shopping for clothes asks for another size with もうすこし おおきい サイズは ありますか, "
        "asks permission with しちゃくしても いいですか, and comments on colour with にあいます.",
        [V("サイズ", "saizu", "size", "noun"),
         V("いろ", "iro", "colour", "noun"),
         V("しちゃく", "shichaku", "trying on clothes", "noun"),
         V("にあう", "niau", "to suit, to match", "verb"),
         V("もうすこし", "mou sukoshi", "a little more", "adverb")],
        G("Sizes and colours",
          "もうすこし おおきい サイズは ありますか · しちゃくしても いいですか · この いろは よく にあいます",
          "Permission is asked with ても いいですか and granted with いいですよ. にあう takes に "
          "for the person or thing it suits, and the adverb よく stands before the verb.",
          [X("もうすこし おおきい サイズは ありますか。", "Mou sukoshi ookii saizu wa arimasu ka.", "Is there a slightly bigger size?"),
           X("しちゃくしても いいですか。", "Shichaku shite mo ii desu ka.", "May I try it on?"),
           X("この いろは よく にあいます。", "Kono iro wa yoku niaimasu.", "This colour suits you well.")],
          [("おおきい サイズ を ください です。", "おおきい サイズを ください。", "ください ends the request; です does not follow."),
           ("この いろは にあいます よく。", "この いろは よく にあいます。", "The adverb precedes the verb it modifies.")]),
        [D("ゆき", "すみません、もうすこし おおきい サイズは ありますか。", "Sumimasen, mou sukoshi ookii saizu wa arimasu ka.", "Excuse me, is there a slightly bigger size?"),
         D("てんいん", "はい、あります。しちゃくしても いいですよ。", "Hai, arimasu. Shichaku shite mo ii desu yo.", "Yes, there is. You may try it on."),
         D("ゆき", "この いろは よく にあいますね。", "Kono iro wa yoku niaimasu ne.", "This colour suits me well, doesn't it."),
         D("てんいん", "ありがとう ございます。", "Arigatou gozaimasu.", "Thank you.")],
        WS("Clothes worksheet", [
            T("Ask for another size.", ["is there a slightly bigger size?", "may I try it on?"],
              ["もうすこし おおきい サイズは ありますか", "しちゃくしても いいですか"]),
            T("Comment on the colour.", ["this colour suits you well", "yes, there is"],
              ["この いろは よく にあいます", "はい、あります"]),
        ]))),
]

THIRD["B1"] = [
    ("B1-U1", "ja-b1-l7", L("ものがたりの あいず: まず、それから、とうとう",
        "A story in Japanese is built from signposts: まず (first), それから (then), そのあと "
        "(after that) and とうとう (in the end). They carry the sequence so the verbs can stay in "
        "one tense.",
        [V("まず", "mazu", "first of all", "adverb"),
         V("それから", "sorekara", "and then", "conjunction"),
         V("そのあと", "sono ato", "after that", "phrase"),
         V("とうとう", "toutou", "in the end, finally", "adverb"),
         V("きっかけ", "kikkake", "trigger, starting point", "noun")],
        G("Narration signposts",
          "まず …ました · それから …ました · そのあと …ました · とうとう …ました",
          "The signposts stand at the head of their sentence and the tense stays in the past for "
          "the whole sequence. とうとう marks the last event and nothing follows it; a new "
          "sentence after it breaks the ending.",
          [X("まず でんしゃに のりました。", "Mazu densha ni norimashita.", "First I got on the train."),
           X("それから あるいて いえへ かえりました。", "Sorekara aruite ie e kaerimashita.", "Then I walked home."),
           X("とうとう おわりました。", "Toutou owarimashita.", "In the end it finished.")],
          [("まず、でんしゃに のります。それから、あるいて かえりました。", "まず、でんしゃに のりました。それから、あるいて かえりました。", "A narration keeps one tense: the whole sequence goes in the past."),
           ("とうとう おわりました、それから。", "とうとう おわりました。", "とうとう closes the sequence; nothing follows it.")]),
        [D("ゆき", "きのうは どうでしたか。", "Kinou wa dou deshita ka.", "How was yesterday?"),
         D("たろう", "まず でんしゃに のりました。それから あるいて いえへ かえりました。", "Mazu densha ni norimashita. Sorekara aruite ie e kaerimashita.", "First I got on the train. Then I walked home."),
         D("ゆき", "たいへん でしたね。", "Taihen deshita ne.", "That must have been hard."),
         D("たろう", "でも、とうとう つきました。", "Demo, toutou tsukimashita.", "But in the end I arrived.")],
        WS("Story worksheet", [
            T("Set the sequence.", ["first I got on the train", "then I walked home"],
              ["まず でんしゃに のりました", "それから あるいて いえへ かえりました"]),
            T("Finish it.", ["in the end it finished", "after that I telephoned a friend"],
              ["とうとう おわりました", "そのあと、ともだちに でんわしました"]),
        ]))),
    ("B1-U2", "ja-b1-l8", L("おとなりと あいさつ: おじゃまします",
        "Entering a home is announced with おじゃまします, the gift is carried in with を, and the "
        "visit closes with ごちそうさまでした and おせわに なりました. The phrases are fixed; the "
        "only choice is whether to bring something.",
        [V("おじゃまします", "ojama shimasu", "said on entering someone's home", "phrase"),
         V("おみやげ", "omiyage", "souvenir, gift brought to a host", "noun"),
         V("ごちそうさまでした", "gochisousama deshita", "thank you for the meal", "phrase"),
         V("おとなり", "otonari", "neighbour, next door", "noun"),
         V("おせわに なりました", "osewa ni narimashita", "thank you for everything", "phrase")],
        G("Visiting a home",
          "おじゃまします · おみやげを もって いきます · ごちそうさまでした · おせわに なりました",
          "おじゃまします is said as you step in, in the present; ごちそうさまでした and おせわに "
          "なりました close the visit in the past. What you carry takes を, and the destination "
          "takes に: おとなりに おみやげを もって いきます.",
          [X("おじゃまします。", "Ojama shimasu.", "Excuse me for intruding."),
           X("おとなりに おみやげを もって いきました。", "Otonari ni omiyage o motte ikimashita.", "I took a gift to the neighbours."),
           X("ごちそうさまでした。おせわに なりました。", "Gochisousama deshita. Osewa ni narimashita.", "Thank you for the meal. Thank you for everything.")],
          [("おじゃましました。", "おじゃまします。", "The phrase is said as you step in: present, not past."),
           ("おみやげに もって いきました。", "おみやげを もって いきました。", "What you carry takes を; に marks where you carried it.")]),
        [D("ゆき", "おじゃまします。", "Ojama shimasu.", "Excuse me for intruding."),
         D("たろう", "いらっしゃい。どうぞ。", "Irasshai. Douzo.", "Welcome. Please come in."),
         D("ゆき", "おみやげを もって きました。", "Omiyage o motte kimashita.", "I brought a small gift."),
         D("たろう", "ありがとう。じゃ、ごちそうを どうぞ。", "Arigatou. Ja, gochisou o douzo.", "Thank you. Please, have something to eat.")],
        WS("Visit worksheet", [
            T("Enter and offer.", ["excuse me for intruding", "I brought a small gift"],
              ["おじゃまします", "おみやげを もって きました"]),
            T("Close the visit.", ["thank you for the meal", "thank you for everything"],
              ["ごちそうさまでした", "おせわに なりました"]),
        ]))),
    ("B1-U3", "ja-b1-l9", L("よていを たてる: ごごは どうですか",
        "Arranging a time offers a slot with は どうですか, reports inconvenience with つごうが "
        "わるい, and closes the agreement with たのしみに しています. Availability takes が, not は.",
        [V("よてい", "yotei", "plan, schedule", "noun"),
         V("つごう", "tsugou", "convenience, availability", "noun"),
         V("へいじつ", "heijitsu", "weekday", "noun"),
         V("たのしみ", "tanoshimi", "looking forward to it", "noun"),
         V("むり", "muri", "impossible", "adjective")],
        G("Arranging",
          "ごごは どうですか · つごうが わるいです · どようびなら だいじょうぶです · たのしみに しています",
          "The offer takes は どうですか, the refusal names the slot and the reason with つごうが "
          "わるい, and the alternative takes なら: にちようびなら だいじょうぶです. The closing is "
          "the fixed phrase たのしみに しています.",
          [X("ごごは どうですか。", "Gogo wa dou desu ka.", "How about the afternoon?"),
           X("すみません、ごごは つごうが わるいです。", "Sumimasen, gogo wa tsugou ga warui desu.", "Sorry, the afternoon is inconvenient."),
           X("たのしみに しています。", "Tanoshimi ni shite imasu.", "I am looking forward to it.")],
          [("つごうは わるいです。", "つごうが わるいです。", "Availability takes が with わるい."),
           ("たのしみ して います。", "たのしみに しています。", "The fixed phrase takes に.")]),
        [D("たろう", "さつえいの よていは いつが いいですか。", "Satsuei no yotei wa itsu ga ii desu ka.", "When is good for the shoot?"),
         D("ゆき", "へいじつの ごごは どうですか。", "Heijitsu no gogo wa dou desu ka.", "How about a weekday afternoon?"),
         D("たろう", "すみません、ごごは つごうが わるいです。あさなら だいじょうぶです。", "Sumimasen, gogo wa tsugou ga warui desu. Asa nara daijoubu desu.", "Sorry, the afternoon is inconvenient. The morning is fine."),
         D("ゆき", "じゃ、あさに しましょう。たのしみに しています。", "Ja, asa ni shimashou. Tanoshimi ni shite imasu.", "Then let us make it the morning. I am looking forward to it.")],
        WS("Arrangement worksheet", [
            T("Offer and refuse.", ["how about a weekday afternoon?", "sorry, the afternoon is inconvenient"],
              ["へいじつの ごごは どうですか", "すみません、ごごは つごうが わるいです"]),
            T("Agree and close.", ["the morning is fine", "I am looking forward to it"],
              ["あさなら だいじょうぶです", "たのしみに しています"]),
        ]))),
]

THIRD["B2"] = [
    ("B2-U1", "ja-b2-l7", L("すうじで はなす: へいきん、わりあい、ふえる",
        "An argument that uses figures names the measure before the number: へいきんで (on average), "
        "わりあいで (as a ratio), けいこうと して (as a trend). The verb then describes the "
        "movement, ふえる or へる.",
        [V("へいきん", "heikin", "average", "noun"),
         V("わりあい", "wariai", "ratio, proportion", "noun"),
         V("ふえる", "fueru", "to increase", "verb"),
         V("へる", "heru", "to decrease", "verb"),
         V("けいこう", "keikou", "trend", "noun")],
        G("Figures in an argument",
          "へいきんで みると … · わりあいで いうと … · けいこうと して ふえています",
          "The measure takes で (みると / いうと) and the trend takes として. A number with no "
          "measure attached is not evidence, and the verb is chosen for direction before it is "
          "chosen for politeness.",
          [X("へいきんで みると、にじゅう ぱーせんと です。", "Heikin de miru to, nijuu paasento desu.", "On average it is twenty per cent."),
           X("わりあいで いうと、はんぶん です。", "Wariai de iu to, hanbun desu.", "As a ratio, it is half."),
           X("けいこうと して ふえています。", "Keikou to shite fuete imasu.", "As a trend it is increasing.")],
          [("へいきん を みます。", "へいきんで みます。", "A measure takes で: judge by the average."),
           ("けいこうは ふえて います です。", "けいこうは ふえています。", "います already ends the sentence; です does not follow.")]),
        [D("ぶちょう", "その すうじ、そのまま つかえますか。", "Sono suuji, sonomama tsukaemasu ka.", "Can we use that figure as it stands?"),
         D("たろう", "へいきんで みると にじゅう ぱーせんと です。", "Heikin de miru to nijuu paasento desu.", "On average it is twenty per cent."),
         D("ぶちょう", "けいこうは。", "Keikou wa.", "And the trend?"),
         D("たろう", "けいこうと して ふえています。わりあいで いうと、はんぶん です。", "Keikou to shite fuete imasu. Wariai de iu to, hanbun desu.", "As a trend it is rising. As a ratio, half.")],
        WS("Figures worksheet", [
            T("Name the measure.", ["on average it is twenty per cent", "as a ratio, it is half"],
              ["へいきんで みると にじゅう ぱーせんと です", "わりあいで いうと、はんぶん です"]),
            T("Describe the movement.", ["as a trend it is increasing", "it is decreasing"],
              ["けいこうと して ふえています", "へっています"]),
        ]))),
    ("B2-U2", "ja-b2-l8", L("ほうこくしょ: おそれいりますが、〜させて いただきます",
        "Formal writing pairs a humble opening with a precise request: おそれいりますが、ごかくにんを "
        "おねがいします。 A service is promised with させて いただきます and a failure is owned with "
        "たいへん もうしわけ ございません.",
        [V("おそれいりますが", "osoreirimasu ga", "I am sorry to trouble you, but", "phrase"),
         V("もうしわけ ございません", "moushiwake gozaimasen", "there is no excuse", "phrase"),
         V("かくにん", "kakunin", "confirmation", "noun"),
         V("けんとう", "kentou", "consideration", "noun"),
         V("しつれいします", "shitsurei shimasu", "excuse me (also as a closing)", "phrase")],
        G("Formal report",
          "おそれいりますが、…を おねがいします · 〜させて いただきます · たいへん もうしわけ ございません",
          "The request opens with おそれいりますが and closes with おねがいします; the promise "
          "takes the causative + いただきます; the apology takes たいへん and ございません. One "
          "polite ending per sentence — stacking them is the commonest keigo error.",
          [X("おそれいりますが、ごかくにんを おねがいします。", "Osoreirimasu ga, gokakunin o onegaishimasu.", "I am sorry to trouble you, but please confirm."),
           X("こちらで たいおう させて いただきます。", "Kochira de taiou sasete itadakimasu.", "We will handle it here (humbly)."),
           X("たいへん もうしわけ ございません。", "Taihen moushiwake gozaimasen.", "There is no excuse for this.")],
          [("ごかくにん を おねがい します です。", "ごかくにんを おねがいします。", "One polite ending per sentence."),
           ("もうしわけ ございません です。", "もうしわけ ございません。", "ございません is already the ending.")]),
        [D("たろう", "その けん、すすんでいますか。", "Sono ken, susunde imasu ka.", "Is that matter moving?"),
         D("ゆき", "おそれいりますが、ごかくにんを おねがいします。", "Osoreirimasu ga, gokakunin o onegaishimasu.", "I am sorry to trouble you, but please confirm."),
         D("たろう", "こちらで たいおう させて いただきます。", "Kochira de taiou sasete itadakimasu.", "We will handle it here."),
         D("ゆき", "ありがとう ございます。しつれいします。", "Arigatou gozaimasu. Shitsurei shimasu.", "Thank you. Excuse me.")],
        WS("Report worksheet", [
            T("Ask and promise.", ["I am sorry to trouble you, but please confirm", "we will handle it here (humbly)"],
              ["おそれいりますが、ごかくにんを おねがいします", "こちらで たいおう させて いただきます"]),
            T("Own the failure.", ["there is no excuse for this", "thank you. Excuse me."],
              ["たいへん もうしわけ ございません", "ありがとう ございます。しつれいします"]),
        ]))),
    ("B2-U3", "ja-b2-l9", L("ニュースを よむ: みだしと きじ",
        "A headline is not a source. Reading a Japanese article means reading みだし (headline), "
        "the きじ (article) and its しりょう (materials) separately, and noticing that 〜に よると "
        "names who is speaking.",
        [V("みだし", "midashi", "headline", "noun"),
         V("きじ", "kiji", "article", "noun"),
         V("ほうどう", "houdou", "news report", "noun"),
         V("しりょう", "shiryou", "materials, source documents", "noun"),
         V("とりあげる", "toriageru", "to take up, to feature", "verb")],
        G("Reading a report",
          "みだしには …と ある · きじに よると … · しりょうを みると … · とりあげています",
          "The headline is quoted with と ある, the article as a source with に よると, and the "
          "materials with を みると. Each layer is attributed separately, so a claim can be traced "
          "to the layer that supports it.",
          [X("みだしには「ふえた」と あります。", "Midashi ni wa 'fueta' to arimasu.", "The headline says 'it increased'."),
           X("きじに よると、げんいんは まだ わかりません。", "Kiji ni yoru to, gen'in wa mada wakarimasen.", "According to the article, the cause is not yet known."),
           X("この もんだいを とりあげています。", "Kono mondai o toriagete imasu.", "It takes up this issue.")],
          [("しりょうに よると、みだしは こう です。", "きじに よると、みだしは こうです。", "よると takes the article or the materials; a headline is what is being reported."),
           ("とりあげる を します。", "とりあげます。", "とりあげる is a verb on its own; it does not take を します.")]),
        [D("ゆき", "その みだし、ほんとうですか。", "Sono midashi, hontou desu ka.", "Is that headline true?"),
         D("たろう", "きじに よると、げんいんは まだ わかりません。", "Kiji ni yoru to, gen'in wa mada wakarimasen.", "According to the article, the cause is not yet known."),
         D("ゆき", "みだしには。", "Midashi ni wa.", "And the headline?"),
         D("たろう", "みだしには「ふえた」と あります。しりょうは べつです。", "Midashi ni wa 'fueta' to arimasu. Shiryou wa betsu desu.", "The headline says 'it increased'. The materials are separate.")],
        WS("News worksheet", [
            T("Read the layers.", ["the headline says 'it increased'", "according to the article, the cause is not yet known"],
              ["みだしには「ふえた」と あります", "きじに よると、げんいんは まだ わかりません"]),
            T("Trace the claim.", ["it takes up this issue", "the materials are separate"],
              ["この もんだいを とりあげています", "しりょうは べつです"]),
        ]))),
]

THIRD["C1"] = [
    ("ja-c1-u1", "ja-c1-l7", L("心内文: 人物の こえを 地の文に",
        "Japanese narrative lets a character's voice into the narration without quotation marks: "
        "the tense stays in 地の文 while the question or exclamation belongs to the person. "
        "Adding と おもった or と いった flattens it back into reported speech.",
        [V("心内文", "shinnaibun", "free indirect thought", "noun"),
         V("地の文", "jino bun", "narrative text (as opposed to dialogue)", "noun"),
         V("かぎかっこ", "kagikakko", "quotation marks", "noun"),
         V("じんぶつ", "jinbutsu", "character, person", "noun"),
         V("つぶやく", "tsubuyaku", "to mutter", "verb")],
        G("Free indirect thought",
          "かぎかっこ なしで こえを のこす · たしかに、そうだ。 · なぜ いわなかった のだろう。",
          "The character's thought keeps its own exclamation or question but borrows the "
          "narration's plain form; だろう marks a question nobody is being asked. Quotation marks "
          "are optional, which is exactly why the technique is easy to miss.",
          [X("たしかに、そうだ。", "Tashika ni, sou da.", "It is true, he thought."),
           X("なぜ いわなかった のだろう。", "Naze iwanakatta no darou.", "Why had he not said it?"),
           X("もう いい、と つぶやいた。", "Mou ii, to tsubuyaita.", "Enough, he muttered.")],
          [("たしかに、そうだ と おもった と いった。", "たしかに、そうだ。", "Free indirect thought drops the reporting frame; both frames flatten it into indirect speech."),
           ("なぜ いわなかった ですか。", "なぜ いわなかった のだろう。", "The character's question stays in the plain form.")]) ,
        [D("編集者", "この ばめん、こえが たりません。", "Kono bamen, koe ga tarimasen.", "In this scene the voice is missing."),
         D("分析者", "では、心内文に します: たしかに、そうだ。", "De wa, shinnaibun ni shimasu: tashika ni, sou da.", "Then I will make it free indirect thought: it is true."),
         D("編集者", "じんぶつの しつもんは。", "Jinbutsu no shitsumon wa.", "And the character's question?"),
         D("分析者", "なぜ いわなかった のだろう、に します。", "Naze iwanakatta no darou, ni shimasu.", "I will use: why had he not said it?")],
        WS("Free indirect worksheet", [
            T("Lose the frame.", ["it is true (as thought)", "why had he not said it?"],
              ["たしかに、そうだ。", "なぜ いわなかった のだろう。"]),
            T("Keep one quotation.", ["enough, he muttered", "the voice is missing"],
              ["もう いい、と つぶやいた。", "こえが たりません"]),
        ]))),
    ("ja-c1-u2", "ja-c1-l8", L("きていの にほんご: 〜に もとづき、〜を もって",
        "Normative Japanese links a rule to its effect with 〜に もとづき and fixes a date with 〜を "
        "もって. Both are written links: nothing is added after them, and です is not stacked on "
        "the verb.",
        [V("きてい", "kitei", "provision, stipulation", "noun"),
         V("もとづく", "motozuku", "to be based on", "verb"),
         V("を もって", "o motte", "as of, by means of", "phrase"),
         V("てきよう", "tekiyou", "application (of a rule)", "noun"),
         V("みとめる", "mitomeru", "to recognise, to acknowledge", "verb")],
        G("Normative linking",
          "この きていに もとづき · ほんじつを もって てきよう します · いじょうを みとめます",
          "に もとづき attaches to the provision, を もって to the date, and both are followed "
          "immediately by the verb. The sentence closes on ます — one ending, no です after it.",
          [X("この きていに もとづき、しんさを おこないます。", "Kono kitei ni motozuki, shinsa o okonaimasu.", "Based on this provision, we conduct the review."),
           X("ほんじつを もって てきよう します。", "Honjitsu o motte tekiyou shimasu.", "It applies as of today."),
           X("いじょうを みとめます。", "Ijou o mitomemasu.", "The above is acknowledged.")],
          [("きてい に もとづいて、てきよう します です。", "この きていに もとづき、てきようします。", "One ending per sentence; に もとづき already carries the link."),
           ("ほんじつ から を もって、てきよう。", "ほんじつを もって てきようします。", "を もって marks the effective date; から contradicts it.")]) ,
        [D("査読者", "この きていは いつから ですか。", "Kono kitei wa itsu kara desu ka.", "From when does this provision apply?"),
         D("分析者", "ほんじつを もって てきよう します。", "Honjitsu o motte tekiyou shimasu.", "It applies as of today."),
         D("査読者", "その こんきょは。", "Sono konkyo wa.", "And the basis?"),
         D("分析者", "この きていに もとづきます。", "Kono kitei ni motozukimasu.", "It is based on this provision.")],
        WS("Provision worksheet", [
            T("Link the rule.", ["based on this provision, we conduct the review", "the above is acknowledged"],
              ["この きていに もとづき、しんさを おこないます", "いじょうを みとめます"]),
            T("Fix the date.", ["it applies as of today", "and the basis?"],
              ["ほんじつを もって てきよう します", "その こんきょは"]),
        ]))),
    ("ja-c1-u3", "ja-c1-l9", L("やさしい にほんご: せつめいを ひらく",
        "やさしい日本語 is a real public-service register: shorter sentences, furigana on kanji, "
        "no double negatives, and one instruction per line. The writer says what was simplified "
        "rather than letting the reader guess.",
        [V("やさしい にほんご", "yasashii nihongo", "plain Japanese (public-service register)", "phrase"),
         V("いいかえ", "iikae", "rephrasing", "noun"),
         V("ふりがな", "furigana", "reading gloss over kanji", "noun"),
         V("りかい", "rikai", "understanding", "noun"),
         V("くふう", "kufuu", "device, deliberate arrangement", "noun")],
        G("Plain-language rendering",
          "やさしい にほんごで せつめいします · いいかえると … · かんじに ふりがなを つけます",
          "The rendering is announced (やさしい にほんごで), each turn of phrase is marked with "
          "いいかえると, and the aids — furigana, line breaks — are named. Simplifying without "
          "saying so reads as condescension.",
          [X("やさしい にほんごで せつめいします。", "Yasashii nihongo de setsumei shimasu.", "I will explain in plain Japanese."),
           X("いいかえると、あしたまで です。", "Iikaeru to, ashita made desu.", "In other words, it is until tomorrow."),
           X("かんじに ふりがなを つけます。", "Kanji ni furigana o tsukemasu.", "I will add reading glosses to the kanji.")],
          [("やさしく いいかえます です。", "やさしく いいかえます。", "ます ends the sentence; です does not follow."),
           ("やさしい にほんごは、かんたん という いみです。", "やさしい にほんごは、りかい しやすい いいかた です。", "The register is about understanding, not about the content being simple.")]) ,
        [D("調停者", "この おしらせは むずかしいです。", "Kono oshirase wa muzukashii desu.", "This notice is difficult."),
         D("分析者", "やさしい にほんごで せつめいします。", "Yasashii nihongo de setsumei shimasu.", "I will explain it in plain Japanese."),
         D("調停者", "くふうは。", "Kufuu wa.", "And the devices?"),
         D("分析者", "かんじに ふりがなを つけて、いちぎょうに ひとつ だけ かきます。", "Kanji ni furigana o tsukete, ichigyou ni hitotsu dake kakimasu.", "I add furigana to the kanji and write only one instruction per line.")],
        WS("Plain-language worksheet", [
            T("Announce the rendering.", ["I will explain it in plain Japanese", "in other words, it is until tomorrow"],
              ["やさしい にほんごで せつめいします", "いいかえると、あしたまで です"]),
            T("Name the devices.", ["I will add reading glosses to the kanji", "one instruction per line"],
              ["かんじに ふりがなを つけます", "いちぎょうに ひとつ"]),
        ]))),
]

THIRD["C2"] = [
    ("ja-c2-u1", "ja-c2-l7", L("ひにくと ひかえめ: 「さすがですね」「ちょっと…」",
        "The same praise can carry irony and the same adjective can carry a refusal: さすがですね "
        "and ちょっと むずかしいですね depend entirely on what surrounds them. A C2 reader hears the "
        "pause before deciding what was said.",
        [V("ひにく", "hiniku", "irony", "noun"),
         V("ひかえめ", "hikaeme", "restrained, understated", "adjective"),
         V("ほめことば", "homekotoba", "words of praise", "noun"),
         V("おことわり", "okotowari", "a polite refusal", "noun"),
         V("くうき", "kuuki", "atmosphere, the mood of a room", "noun")],
        G("Irony and refusal",
          "さすがですね · ちょっと むずかしいですね · そうですね、かんがえて みます",
          "Irony is carried by the pause and the context, not by the words: the same さすがですね "
          "praises or punctures. A refusal stays inside politeness — ちょっと, むずかしい, "
          "かんがえて みます — so that nobody has to be contradicted out loud.",
          [X("さすがですね。", "Sasuga desu ne.", "As expected of you (praise, or not)."),
           X("ちょっと むずかしいですね。", "Chotto muzukashii desu ne.", "A little difficult, isn't it (a refusal)."),
           X("そうですね、かんがえて みます。", "Sou desu ne, kangaete mimasu.", "Let me think about it (a no).")],
          [("さすがですね は いつも ほんとうの ほめことばです。", "さすがですね は ほめことばですが、文脈に よって ひにくな いみに なります。", "The same praise can carry irony; context decides."),
           ("ちょっと むずかしい は、かんたん という いみです。", "ちょっと むずかしい は、ていねいな おことわり です。", "ちょっと… is a refusal, not a comment on difficulty.")]) ,
        [D("編集者", "その デザイン、どう おもいますか。", "Sono dezain, dou omoimasu ka.", "What do you think of that design?"),
         D("分析者", "さすがですね。", "Sasuga desu ne.", "As expected of you."),
         D("編集者", "ほんとうに。", "Hontou ni.", "Really."),
         D("分析者", "ええ、ちょっと むずかしいですね。かんがえて みます。", "Ee, chotto muzukashii desu ne. Kangaete mimasu.", "Well, it is a little difficult. Let me think about it.")],
        WS("Irony worksheet", [
            T("Praise and hedge.", ["as expected of you (praise, or not)", "a little difficult, isn't it (a refusal)"],
              ["さすがですね", "ちょっと むずかしいですね"]),
            T("Refuse politely.", ["let me think about it (a no)", "the same praise can carry irony"],
              ["かんがえて みます", "ほめことばも 文脈で ひにくな いみに なる"]),
        ]))),
    ("ja-c2-u2", "ja-c2-l8", L("リズム: 体言止めと とうご",
        "Rhythm in Japanese is punctuation and word order before it is vocabulary: 体言止め ends "
        "on a noun and lets the sentence hang, とうご pulls the emphasised word to the front. The "
        "line is read aloud to check the breath.",
        [V("体言止め", "taigendome", "ending a sentence on a noun", "noun"),
         V("とうご", "tougo", "inversion, fronting", "noun"),
         V("リズム", "rizumu", "rhythm", "noun"),
         V("よみて", "yomite", "the reader", "noun"),
         V("いき", "iki", "breath", "noun")],
        G("Rhythm devices",
          "しずかな あさ。 · おどろいた、ほんとうに。 · リズムは よみての いきに あわせます",
          "体言止め removes the closing verb and leaves the noun carrying the weight; とうご "
          "fronts the word that matters and lets the rest trail. Both are read aloud: if the "
          "breath runs out, the line is wrong.",
          [X("しずかな あさ。", "Shizuka na asa.", "A quiet morning."),
           X("おどろいた、ほんとうに。", "Odoroita, hontou ni.", "I was surprised, truly."),
           X("リズムは よみての いきに あわせます。", "Rizumu wa yomite no iki ni awasemasu.", "The rhythm follows the reader's breath.")],
          [("しずかな あさ です。", "しずかな あさ。", "体言止め deliberately drops the closing verb for weight."),
           ("リズム は よみて の いき です に あわせます。", "リズムは よみての いきに あわせます。", "The verb あわせます needs its に phrase; です cannot stand before it.")]) ,
        [D("編集者", "この みだし、ながいですね。", "Kono midashi, nagai desu ne.", "This heading is long."),
         D("分析者", "体言止めに します: しずかな あさ。", "Taigendome ni shimasu: shizuka na asa.", "I will use a nominal ending: a quiet morning."),
         D("編集者", "リズムは。", "Rizumu wa.", "And the rhythm?"),
         D("分析者", "とうごで いきを かえます: おどろいた、ほんとうに。", "Tougo de iki o kaemasu: odoroita, hontou ni.", "I change the breath with fronting: I was surprised, truly.")],
        WS("Rhythm worksheet", [
            T("End on a noun.", ["a quiet morning", "I was surprised, truly"],
              ["しずかな あさ。", "おどろいた、ほんとうに。"]),
            T("Read for breath.", ["the rhythm follows the reader's breath", "this heading is long"],
              ["リズムは よみての いきに あわせます", "この みだし、ながいですね"]),
        ]))),
    ("ja-c2-u3", "ja-c2-l9", L("やくせない ことば: みとめる ちがい",
        "At the limit of mediation the word is kept and the loss is written down. 木漏れ日 and "
        "甘える are not translated away; they are glossed, and the gloss says ものたりない — what "
        "falls short.",
        [V("やくせない", "yakusenai", "cannot be translated", "adjective"),
         V("わけ", "wake", "sense, reason", "noun"),
         V("ものたりない", "monotarinai", "to fall short", "adjective"),
         V("のこす", "nokosu", "to leave (as is)", "verb"),
         V("ちんもく", "chinmoku", "silence", "noun")],
        G("Mediating the untranslatable",
          "ことばを そのまま のこす · かっこに やくを つける · ものたりなさを かく",
          "The word stays in Japanese, the gloss goes in brackets, and the note records what the "
          "gloss left out. Refusing to translate is a decision with reasons, and the reasons are "
          "written down — ちんもく そのものが いみを もつ, and the reader is told so.",
          [X("ことばを そのまま のこします。", "Kotoba o sonomama nokoshimasu.", "I leave the word as it is."),
           X("かっこに やくを つけます。", "Kakko ni yaku o tsukemasu.", "I attach a gloss in brackets."),
           X("ものたりなさも かきます。", "Monotarinasa mo kakimasu.", "I also write what falls short.")],
          [("やくせない ことばは けします。", "やくせない ことば ほど、そのまま のこします。", "Untranslatables are kept and glossed, not removed."),
           ("かっこの なかの やくは かんぜん です。", "かっこの なかの やくは、かんぜん では ありません。", "The gloss is honest about what it loses.")]) ,
        [D("調停者", "その ことば、えいごに しますか。", "Sono kotoba, eigo ni shimasu ka.", "Are you rendering that word in English?"),
         D("査読者", "いいえ、そのまま のこします。やくせない から です。", "Iie, sonomama nokoshimasu. Yakusenai kara desu.", "No, I will leave it as it is. Because it cannot be translated."),
         D("調停者", "よみては どう しますか。", "Yomite wa dou shimasu ka.", "What about the reader?"),
         D("査読者", "かっこに やくを つけて、ものたりなさも かきます。", "Kakko ni yaku o tsukete, monotarinasa mo kakimasu.", "I attach a gloss in brackets and write what falls short.")],
        WS("Untranslatable worksheet", [
            T("Keep the word.", ["I leave the word as it is", "I attach a gloss in brackets"],
              ["ことばを そのまま のこします", "かっこに やくを つけます"]),
            T("Record the loss.", ["I also write what falls short", "because it cannot be translated"],
              ["ものたりなさも かきます", "やくせない から です"]),
        ]))),
]

HALFSTEPS["A1+"] = {
    "title": "Japanese A1+ — Out in the city",
    "native": NATIVE,
    "goals": [
        "Ask for and follow simple directions",
        "Book a time, apologise for being late and confirm the next one",
        "Hand something in for repair and pick it up",
    ],
    "units": [
        {"id": "A1+-U1", "title": "まちで", "lessons": [
            L("みちを きく",
              "Directions arrive as short words in order: まっすぐ、みぎ、ひだり、つぎの かど. The "
              "question is 〜は どこですか and the answer rarely contains a verb.",
              [V("まっすぐ", "massugu", "straight ahead", "adverb"),
               V("みぎ", "migi", "right", "noun"),
               V("ひだり", "hidari", "left", "noun"),
               V("かど", "kado", "corner", "noun"),
               V("しんごう", "shingou", "traffic light", "noun")],
              G("Asking the way",
                "〜は どこですか · まっすぐ いって、みぎです · つぎの かどを ひだり",
                "The place takes は and どこですか; the route is a chain of te-form verbs and "
                "nouns, and the verb まがります can be left out entirely. Politeness lives in "
                "すみません at the front.",
                [X("えきは どこですか。", "Eki wa doko desu ka.", "Where is the station?"),
                 X("まっすぐ いって、みぎです。", "Massugu itte, migi desu.", "Go straight, then it is on the right."),
                 X("つぎの かどを ひだりに まがります。", "Tsugi no kado o hidari ni magarimasu.", "Turn left at the next corner.")],
                [("えき が どこですか。", "えきは どこですか。", "The place being asked about takes は."),
                 ("まっすぐ です いきます。", "まっすぐ いきます。", "です does not stand inside a verb phrase.")]),
              [D("ゆき", "すみません、えきは どこですか。", "Sumimasen, eki wa doko desu ka.", "Excuse me, where is the station?"),
               D("たろう", "まっすぐ いって、つぎの かどを みぎです。", "Massugu itte, tsugi no kado o migi desu.", "Go straight, then right at the next corner."),
               D("ゆき", "しんごうは ありますか。", "Shingou wa arimasu ka.", "Is there a traffic light?"),
               D("たろう", "はい、しんごうの となりです。", "Hai, shingou no tonari desu.", "Yes, next to the traffic light.")],
              WS("Directions worksheet", [
                  T("Ask and answer.", ["where is the station?", "go straight, then it is on the right"],
                    ["えきは どこですか", "まっすぐ いって、みぎです"]),
                  T("Give the turn.", ["turn left at the next corner", "next to the traffic light"],
                    ["つぎの かどを ひだりに まがります", "しんごうの となりです"]),
              ])),
            L("みせで きく",
              "Shops are asked for by kind, not by name: ぎんこう、ゆうびんきょく、コンビニ. ちかく "
              "です (nearby) and となり (next door) answer most questions.",
              [V("ぎんこう", "ginkou", "bank", "noun"),
               V("ゆうびんきょく", "yuubinkyoku", "post office", "noun"),
               V("ちかく", "chikaku", "nearby", "noun"),
               V("となり", "tonari", "next door, next to", "noun"),
               V("むかい", "mukai", "opposite side", "noun")],
              G("Finding a place",
                "この ちかくに 〜は ありますか · となりに あります · むかいに あります",
                "Existence is asked with ありますか, and the position words take に: となりに "
                "あります. The shop kind is the topic and takes は — this ちかくに ぎんこうは "
                "ありますか.",
                [X("この ちかくに ぎんこうは ありますか。", "Kono chikaku ni ginkou wa arimasu ka.", "Is there a bank near here?"),
                 X("ゆうびんきょくは むかいに あります。", "Yuubinkyoku wa mukai ni arimasu.", "The post office is opposite."),
                 X("コンビニは となりです。", "Konbini wa tonari desu.", "The convenience store is next door.")],
                [("ちかく で ぎんこう が ありますか。", "この ちかくに ぎんこうは ありますか。", "Existence takes に, not で."),
                 ("となり は あります。", "となりに あります。", "A position takes に before the verb of existence.")]),
              [D("たろう", "この ちかくに ぎんこうは ありますか。", "Kono chikaku ni ginkou wa arimasu ka.", "Is there a bank near here?"),
               D("ゆき", "はい、むかいに あります。", "Hai, mukai ni arimasu.", "Yes, it is opposite."),
               D("たろう", "ゆうびんきょくは。", "Yuubinkyoku wa.", "And the post office?"),
               D("ゆき", "ゆうびんきょくは となりです。", "Yuubinkyoku wa tonari desu.", "The post office is next door.")],
              WS("Shops worksheet", [
                  T("Ask what exists.", ["is there a bank near here?", "the post office is opposite"],
                    ["この ちかくに ぎんこうは ありますか", "ゆうびんきょくは むかいに あります"]),
                  T("Point it out.", ["the convenience store is next door", "and the post office?"],
                    ["コンビニは となりです", "ゆうびんきょくは"]),
              ])),
            L("でんわばんごう",
              "Numbers are read digit by digit with の between groups, and a request to hear it "
              "again takes もういちど おねがいします. ばんごう means number of any kind.",
              [V("ばんごう", "bangou", "number", "noun"),
               V("もういちど", "mou ichido", "once more", "adverb"),
               V("ゆっくり", "yukkuri", "slowly", "adverb"),
               V("ききます", "kikimasu", "to ask, to listen", "verb"),
               V("おしえます", "oshiemasu", "to tell, to teach", "verb")],
              G("Numbers and repeats",
                "ばんごうは なんばんですか · さん-いち-よん の に-ろく · もういちど おねがいします",
                "Digits are strung with の between blocks, and every request for repetition is "
                "softened with おねがいします. ゆっくり おねがいします is the phrase that keeps a "
                "phone call alive.",
                [X("でんわばんごうは なんばんですか。", "Denwa bangou wa nanban desu ka.", "What is the telephone number?"),
                 X("ゆっくり おねがいします。", "Yukkuri onegaishimasu.", "Slowly, please."),
                 X("もういちど きいても いいですか。", "Mou ichido kiite mo ii desu ka.", "May I ask once more?")],
                [("ばんごう を きいて ください です。", "ばんごうを きいて ください。", "ください ends the request."),
                 ("もういちど おねがいします を します。", "もういちど おねがいします。", "おねがいします is the whole request.")]),
              [D("ゆき", "でんわばんごうは なんばんですか。", "Denwa bangou wa nanban desu ka.", "What is the telephone number?"),
               D("たろう", "さん-いち-よん の に-ろく-ゼロ-はち です。", "San-ichi-yon no ni-roku-zero-hachi desu.", "It is 314-2608."),
               D("ゆき", "すみません、ゆっくり おねがいします。", "Sumimasen, yukkuri onegaishimasu.", "Sorry, slowly, please."),
               D("たろう", "はい。さん-いち-よん の に-ろく-ゼロ-はち。", "Hai. San-ichi-yon no ni-roku-zero-hachi.", "Yes. 314-2608.")],
              WS("Numbers worksheet", [
                  T("Ask for the number.", ["what is the telephone number?", "slowly, please"],
                    ["でんわばんごうは なんばんですか", "ゆっくり おねがいします"]),
                  T("Ask for a repeat.", ["may I ask once more?", "it is 314-2608"],
                    ["もういちど きいても いいですか", "さん-いち-よん の に-ろく-ゼロ-はち です"]),
              ])),
        ]},
        {"id": "A1+-U2", "title": "じかんを まもる", "lessons": [
            L("よやくする",
              "A booking names the time first and the request second: あしたの さんじに、よやくを "
              "おねがいします. 〜に marks the time and よやく covers every kind of reservation.",
              [V("よやく", "yoyaku", "booking, reservation", "noun"),
               V("あいて います", "aite imasu", "is free, is open", "phrase"),
               V("つごう", "tsugou", "convenience", "noun"),
               V("おねがいします", "onegaishimasu", "please (I would like)", "phrase"),
               V("なんじから", "nanji kara", "from what time", "phrase")],
              G("Booking a time",
                "あしたの さんじに おねがいします · 〜は あいて いますか · なんじから ですか",
                "The time takes に, the day takes の, and the request closes the sentence. "
                "Availability is asked with あいて いますか — a verb, not an adjective.",
                [X("あしたの さんじに おねがいします。", "Ashita no sanji ni onegaishimasu.", "Tomorrow at three, please."),
                 X("にじは あいて いますか。", "Niji wa aite imasu ka.", "Is two o'clock free?"),
                 X("なんじから ですか。", "Nanji kara desu ka.", "From what time?")],
                [("あした さんじ おねがいします に。", "あしたの さんじに おねがいします。", "The time phrase stands before the request, with に."),
                 ("さんじ が あいて います です。", "さんじは あいて いますか。", "A question closes with か; です does not follow it.")]),
              [D("ゆき", "あしたの さんじに おねがいします。", "Ashita no sanji ni onegaishimasu.", "Tomorrow at three, please."),
               D("たろう", "はい。さんじは あいて います。", "Hai. Sanji wa aite imasu.", "Yes. Three o'clock is free."),
               D("ゆき", "なんじまでですか。", "Nanji made desu ka.", "Until what time?"),
               D("たろう", "ごじまで です。", "Goji made desu.", "Until five.")],
              WS("Booking worksheet", [
                  T("Book the slot.", ["tomorrow at three, please", "is two o'clock free?"],
                    ["あしたの さんじに おねがいします", "にじは あいて いますか"]),
                  T("Ask the span.", ["from what time?", "until five"],
                    ["なんじから ですか", "ごじまで です"]),
              ])),
            L("おくれて すみません",
              "Being late is owned in the first sentence: おくれて すみません、いま 〜に います. "
              "The apology names the delay in minutes and the place you are standing.",
              [V("おくれます", "okuremasu", "to be late", "verb"),
               V("〜ふん", "~ fun", "… minutes", "counter"),
               V("います", "imasu", "to be (a person), to exist", "verb"),
               V("まちます", "machimasu", "to wait", "verb"),
               V("すぐに", "sugu ni", "immediately", "adverb")],
              G("Being late",
                "おくれて すみません · いま えきに います · あと 〜ふん です · すぐに いきます",
                "おくれて すみません opens the message; the place takes に with います; the "
                "remaining time is stated with あと. Naming the minutes is what makes the apology "
                "usable.",
                [X("おくれて すみません。", "Okurete sumimasen.", "Sorry for being late."),
                 X("いま えきに います。", "Ima eki ni imasu.", "I am at the station now."),
                 X("あと ごふん です。すぐに いきます。", "Ato gofun desu. Sugu ni ikimasu.", "Five more minutes. I am coming at once.")],
                [("おくれます すみません。", "おくれて すみません。", "The apology takes the te-form: おくれて."),
                 ("えき で います。", "えきに います。", "A person's location takes に with います.")]),
              [D("たろう", "もしもし、いま どこですか。", "Moshi moshi, ima doko desu ka.", "Hello, where are you now?"),
               D("ゆき", "おくれて すみません。いま えきに います。", "Okurete sumimasen. Ima eki ni imasu.", "Sorry for being late. I am at the station now."),
               D("たろう", "あと どのくらいですか。", "Ato dono kurai desu ka.", "How much longer?"),
               D("ゆき", "あと ごふん です。すぐに いきます。", "Ato gofun desu. Sugu ni ikimasu.", "Five more minutes. I am coming at once.")],
              WS("Late worksheet", [
                  T("Own the delay.", ["sorry for being late", "I am at the station now"],
                    ["おくれて すみません", "いま えきに います"]),
                  T("Give the time left.", ["five more minutes", "I am coming at once"],
                    ["あと ごふん です", "すぐに いきます"]),
              ])),
            L("つぎの よてい",
              "The next appointment is fixed with つぎは and いつが いいですか, and confirmed in "
              "the past of a decision: 〜に きめましょう. らいしゅう and こんしゅう do not take の.",
              [V("つぎ", "tsugi", "next", "noun"),
               V("らいしゅう", "raishuu", "next week", "noun"),
               V("こんしゅう", "konshuu", "this week", "noun"),
               V("きめます", "kimemasu", "to decide", "verb"),
               V("いつが", "itsu ga", "which day/time (subject of a choice)", "phrase")],
              G("Fixing the next time",
                "つぎは らいしゅうに しましょう · いつが いいですか · どようびに きめましょう",
                "The choice question takes が with いい: いつが いいですか. The decision is "
                "announced with ましょう, and the day takes に: どようびに きめましょう.",
                [X("つぎは らいしゅうに しましょう。", "Tsugi wa raishuu ni shimashou.", "Let us make it next week."),
                 X("いつが いいですか。", "Itsu ga ii desu ka.", "Which day is good?"),
                 X("どようびに きめましょう。", "Doyoubi ni kimemashou.", "Let us decide on Saturday.")],
                [("つぎは らいしゅう を します。", "つぎは らいしゅうに しましょう。", "The plan takes にする, not を します."),
                 ("いつは いいですか。", "いつが いいですか。", "The chosen day takes が with いい.")]),
              [D("たろう", "つぎは いつが いいですか。", "Tsugi wa itsu ga ii desu ka.", "When is good next time?"),
               D("ゆき", "らいしゅうは どうですか。つごうが わるいです か。", "Raishuu wa dou desu ka. Tsugou ga warui desu ka.", "How about next week? Is it inconvenient?"),
               D("たろう", "どようびなら だいじょうぶです。", "Doyoubi nara daijoubu desu.", "Saturday is fine."),
               D("ゆき", "じゃ、どようびに きめましょう。", "Ja, doyoubi ni kimemashou.", "Then let us decide on Saturday.")],
              WS("Next time worksheet", [
                  T("Fix the next meeting.", ["let us make it next week", "which day is good?"],
                    ["つぎは らいしゅうに しましょう", "いつが いいですか"]),
                  T("Decide the day.", ["let us decide on Saturday", "is it inconvenient?"],
                    ["どようびに きめましょう", "つごうが わるいです か"]),
              ])),
        ]},
        {"id": "A1+-U3", "title": "なおして もらう", "lessons": [
            L("こわれました",
              "A fault is reported with こわれました and diagnosed with みつもり (estimate). The "
              "shop asks どうしましたか and you answer with the object and the state.",
              [V("こわれました", "kowaremashita", "it broke", "verb"),
               V("みつもり", "mitsumori", "estimate, quote", "noun"),
               V("なおします", "naoshimasu", "to repair, to fix", "verb"),
               V("まだ", "mada", "still, not yet", "adverb"),
               V("あずけます", "azukemasu", "to hand in, to leave (for repair)", "verb")],
              G("Reporting a fault",
                "こわれました · どうしましたか · なおせますか · みつもりは いくらですか",
                "The fault is stated as an event (こわれました), the possibility as a question "
                "(なおせますか), and the cost with みつもり. まだ with a negative means not yet: "
                "まだ なおせません.",
                [X("これは こわれました。", "Kore wa kowaremashita.", "This one is broken."),
                 X("なおせますか。", "Naosemasu ka.", "Can it be repaired?"),
                 X("みつもりは いくらですか。", "Mitsumori wa ikura desu ka.", "How much is the estimate?")],
                [("これは こわれて います です。", "これは こわれています。", "います ends the sentence; です does not follow."),
                 ("なおす が できますか。", "なおせますか。", "Ability is built into the verb: なおせます.")]),
              [D("ゆき", "すみません、これは こわれました。", "Sumimasen, kore wa kowaremashita.", "Excuse me, this one is broken."),
               D("てんいん", "どうしましたか。", "Dou shimashita ka.", "What happened?"),
               D("ゆき", "おとして、がめんが みえません。なおせますか。", "Otoshite, gamen ga miemasen. Naosemasu ka.", "I dropped it and the screen cannot be seen. Can it be repaired?"),
               D("てんいん", "はい。みつもりは あした です。", "Hai. Mitsumori wa ashita desu.", "Yes. The estimate will be tomorrow.")],
              WS("Repair worksheet", [
                  T("Report the fault.", ["this one is broken", "can it be repaired?"],
                    ["これは こわれました", "なおせますか"]),
                  T("Ask the cost.", ["how much is the estimate?", "what happened?"],
                    ["みつもりは いくらですか", "どうしましたか"]),
              ])),
            L("そうだん して ください",
              "A consultation states the deadline with 〜までに and the condition with できれば. "
              "そうだん して ください asks for advice rather than a decision.",
              [V("そうだん", "soudan", "consultation", "noun"),
               V("できれば", "dekireba", "if possible", "adverb"),
               V("〜までに", "~ made ni", "by (a deadline)", "postposition"),
               V("かんがえます", "kangaemasu", "to think it over", "verb"),
               V("へんじ", "henji", "reply", "noun")],
              G("Asking for advice",
                "そうだん して ください · 〜までに へんじを ください · できれば 〜",
                "The deadline takes までに (by then) and the preference takes できれば at the "
                "front. へんじを ください is the polite request for an answer.",
                [X("すこし そうだん して ください。", "Sukoshi soudan shite kudasai.", "Please advise me a little."),
                 X("きんようびまでに へんじを ください。", "Kinyoubi made ni henji o kudasai.", "Please reply by Friday."),
                 X("できれば メールで おねがいします。", "Dekireba meeru de onegaishimasu.", "By email, if possible.")],
                [("きんようび まで へんじを ください。", "きんようびまでに へんじを ください。", "A deadline takes までに; まで marks the end of a span."),
                 ("そうだん を して ください です。", "そうだん して ください。", "ください ends the sentence.")]),
              [D("たろう", "この けん、どう しましょうか。", "Kono ken, dou shimashou ka.", "What should we do about this matter?"),
               D("ゆき", "すこし そうだん して ください。", "Sukoshi soudan shite kudasai.", "Please advise me a little."),
               D("たろう", "きんようびまでに へんじを ください。", "Kinyoubi made ni henji o kudasai.", "Please reply by Friday."),
               D("ゆき", "できれば メールで おねがいします。", "Dekireba meeru de onegaishimasu.", "By email, if possible.")],
              WS("Advice worksheet", [
                  T("Ask for advice.", ["please advise me a little", "please reply by Friday"],
                    ["すこし そうだん して ください", "きんようびまでに へんじを ください"]),
                  T("State the preference.", ["by email, if possible", "what should we do?"],
                    ["できれば メールで おねがいします", "どう しましょうか"]),
              ])),
            L("うけとります",
              "Handing in and picking up are two verbs: あずけます and うけとります. The receipt "
              "is あずかりしょう and the day is asked with いつ できますか.",
              [V("うけとります", "uketorimasu", "to receive, to pick up", "verb"),
               V("あずかりしょう", "azukarishou", "receipt (for an item left)", "noun"),
               V("できあがり", "dekiagari", "completion, ready", "noun"),
               V("いつごろ", "itsugoro", "about when", "adverb"),
               V("たしかに", "tashika ni", "certainly (confirming a fact)", "adverb")],
              G("Handing in and picking up",
                "あずけます · あずかりしょうを ください · いつごろ できあがりますか · たしかに うけとりました",
                "Handing in takes あずけます and a receipt request; the ready date is asked with "
                "いつごろ; picking up is closed with たしかに うけとりました, which records the "
                "handover.",
                [X("これを あずけます。", "Kore o azukemasu.", "I will leave this with you."),
                 X("いつごろ できあがりますか。", "Itsugoro dekiagarimasu ka.", "About when will it be ready?"),
                 X("たしかに うけとりました。", "Tashika ni uketorimashita.", "I have certainly received it.")],
                [("あずかりしょう を ください です。", "あずかりしょうを ください。", "ください ends the request."),
                 ("いつ できあがります です か。", "いつごろ できあがりますか。", "One ending per question: ます + か.")]),
              [D("ゆき", "これを あずけます。", "Kore o azukemasu.", "I will leave this with you."),
               D("てんいん", "あずかりしょうを どうぞ。", "Azukarishou o douzo.", "Here is your receipt."),
               D("ゆき", "いつごろ できあがりますか。", "Itsugoro dekiagarimasu ka.", "About when will it be ready?"),
               D("てんいん", "らいしゅうの きんようび です。", "Raishuu no kinyoubi desu.", "Next Friday.")],
              WS("Pickup worksheet", [
                  T("Hand it in.", ["I will leave this with you", "here is your receipt"],
                    ["これを あずけます", "あずかりしょうを どうぞ"]),
                  T("Ask and confirm.", ["about when will it be ready?", "I have certainly received it"],
                    ["いつごろ できあがりますか", "たしかに うけとりました"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Being late, asking the way and handing something in for repair are the three "
                 "situations where Japanese politeness is most audible: the apology comes first "
                 "and the fact second (おくれて すみません、いま えきに います), a question to a "
                 "stranger opens with すみません, and a request closes with おねがいします. Get "
                 "the order right and the grammar can stay simple."),
        source_url="https://en.wikipedia.org/wiki/Japanese_language",
        reading=("あさ、ともだちと えきで あう よていでした。でも、でんしゃが おくれて、"
                 "ごふん おくれました。すぐに でんわして、おくれて すみません と いいました。"
                 "ともだちは まだ まって いました。それから、いっしょに みせへ いって、"
                 "こわれた とけいを あずけました。みつもりは あした です。"),
        reading_gloss=("In the morning I was supposed to meet a friend at the station. But the "
                       "train was delayed and I was five minutes late. I telephoned at once and "
                       "said 'sorry for being late'. My friend was still waiting. Then we went "
                       "together to a shop and handed in a broken watch. The estimate is tomorrow."),
        listening=("ゆき: すみません、ぎんこうは どこですか。<br>"
                   "たろう: まっすぐ いって、つぎの かどを ひだりです。<br>"
                   "ゆき: ゆうびんきょくは。<br>"
                   "たろう: ぎんこうの となりに あります。"),
        listening_gloss=("Yuki: Excuse me, where is the bank? Taro: Go straight, then left at the "
                         "next corner. Yuki: And the post office? Taro: It is next to the bank."),
        voice_tag=VOICE,
        idioms=[
            ("まっすぐ", "massugu", "straight ahead"),
            ("つぎの かど", "tsugi no kado", "the next corner"),
            ("この ちかくに", "kono chikaku ni", "near here"),
            ("もういちど", "mou ichido", "once more"),
            ("ゆっくり おねがいします", "yukkuri onegaishimasu", "slowly, please"),
            ("あと ごふん", "ato gofun", "five more minutes"),
            ("いつが いいですか", "itsu ga ii desu ka", "which time is good?"),
            ("こわれました", "kowaremashita", "it broke"),
            ("みつもり", "mitsumori", "estimate"),
            ("いつごろ", "itsugoro", "about when"),
        ],
        mistakes=[
            ("えき で います。", "えきに います。", "A person's location takes に with います."),
            ("きんようび まで へんじを ください。", "きんようびまでに へんじを ください。", "A deadline takes までに."),
            ("あした さんじ おねがいします に。", "あしたの さんじに おねがいします。", "The time phrase stands before the request, with に."),
        ],
        task_title="Script a five-line late-and-repair message",
        task_instructions=("Write the Japanese you would send and say on a morning when the train "
                           "is late and you also have a broken watch to hand in: the apology with "
                           "おくれて すみません, where you are with に います, how long with あと "
                           "〜ふん, the decision with ましょう for the next meeting, and the repair "
                           "request with あずけます and みつもり. Then read it aloud at speaking "
                           "speed — the message should take under twenty seconds."),
    ),
    "test": [
        ("translate_en", "Say: Excuse me, where is the station?", "すみません、えきは どこですか。"),
        ("translate_ja", "この ちかくに ぎんこうは ありますか。", "Is there a bank near here?"),
        ("multiple_choice", "Which sentence apologises for being late correctly?", "おくれて すみません。"),
        ("fill_in_the_blank", "いま えき___ います。", "に"),
        ("word_selection", "Select the Japanese for 'next to the traffic light'.", "しんごうの となり"),
        ("error_correction", "きんようび まで へんじを ください。", "きんようびまでに へんじを ください。"),
        ("dialogue_completion", "Complete: えきは どこですか。 — ___ (go straight, then it is on the right)", "まっすぐ いって、みぎです"),
        ("matching", "Match みつもり to its meaning.", "an estimate"),
        ("reading_comprehension", "でんしゃが おくれて、ごふん おくれました。 How late was the speaker?", "five minutes"),
        ("inference", "「あと ごふん です。すぐに いきます。」 — what is the speaker doing?", "saying they are on the way"),
        ("main_idea", "これを あずけます。いつごろ できあがりますか。 What is this?", "handing in a repair and asking when it is ready"),
        ("detail_identification", "あしたの さんじに おねがいします。 What time was booked?", "three o'clock tomorrow"),
    ],
}

HALFSTEPS["A2+"] = {
    "title": "Japanese A2+ — Office and services",
    "native": NATIVE,
    "goals": [
        "Ask for a day off and take a phone message",
        "Keep small talk going for three turns",
        "Use the post office, the bank and a shop counter",
    ],
    "units": [
        {"id": "A2+-U1", "title": "かいしゃの でんわ", "lessons": [
            L("やすみを とる",
              "Leave is requested with やすみを とりたいのですが, the date takes まで, and the "
              "reason stays short. 〜のですが softens the request into a statement of need.",
              [V("やすみ", "yasumi", "day off, holiday", "noun"),
               V("とります", "torimasu", "to take (leave)", "verb"),
               V("ようじ", "youji", "personal errand", "noun"),
               V("〜のですが", "~ no desu ga", "I would like to …, if possible", "phrase"),
               V("りょうかい", "ryoukai", "understood", "noun")],
              G("Asking for leave",
                "らいしゅうの きんようび、やすみを とりたいのですが · ようじが あります · りょうかい しました",
                "〜のですが leaves the request open for the listener to agree; the reason takes "
                "が あります; agreement is りょうかい しました. No imperative is used at all.",
                [X("らいしゅうの きんようび、やすみを とりたいのですが。", "Raishuu no kinyoubi, yasumi o toritai no desu ga.", "I would like to take next Friday off, if possible."),
                 X("ようじが あります。", "Youji ga arimasu.", "I have a personal matter."),
                 X("りょうかい しました。", "Ryoukai shimashita.", "Understood.")],
                [("やすみ を とります ください。", "やすみを とりたいのですが。", "Requests to a superior use たいのですが, not ください."),
                 ("ようじ は あります。", "ようじが あります。", "The reason takes が: it is new information.")]),
              [D("ゆき", "らいしゅうの きんようび、やすみを とりたいのですが。", "Raishuu no kinyoubi, yasumi o toritai no desu ga.", "I would like to take next Friday off, if possible."),
               D("ぶちょう", "ようじですか。", "Youji desu ka.", "A personal matter?"),
               D("ゆき", "はい、ようじが あります。", "Hai, youji ga arimasu.", "Yes, I have a personal matter."),
               D("ぶちょう", "りょうかい しました。", "Ryoukai shimashita.", "Understood.")],
              WS("Leave worksheet", [
                  T("Request the day.", ["I would like to take next Friday off, if possible", "I have a personal matter"],
                    ["らいしゅうの きんようび、やすみを とりたいのですが", "ようじが あります"]),
                  T("Close it.", ["understood", "a personal matter?"],
                    ["りょうかい しました", "ようじですか"]),
              ])),
            L("でんわに でる",
              "A business call opens with いつも おせわに なっております and the person asked for "
              "with いらっしゃいますか. Holding takes すこし おまちください.",
              [V("いらっしゃいます", "irasshaimasu", "is present (respectful)", "verb"),
               V("おまちください", "omachi kudasai", "please wait (polite)", "phrase"),
               V("いま いません", "ima imasen", "is not here now", "phrase"),
               V("おりかえし", "orikaeshi", "return call", "noun"),
               V("つたえます", "tsutaemasu", "to convey, to pass on", "verb")],
              G("Making a call",
                "いつも おせわに なっております · 〜さんは いらっしゃいますか · すこし おまちください · おりかえし でんわします",
                "The opening is a fixed courtesy; the person is asked about with いらっしゃいますか; "
                "and when they are out the answer is いま いません with an offer to call back.",
                [X("いつも おせわに なっております。", "Itsumo osewa ni natte orimasu.", "Thank you for your continued help."),
                 X("たなかさんは いらっしゃいますか。", "Tanaka-san wa irasshaimasu ka.", "Is Mr Tanaka there?"),
                 X("すこし おまちください。", "Sukoshi omachi kudasai.", "One moment, please.")],
                [("たなかさん は います ですか。", "たなかさんは いらっしゃいますか。", "A person of another company is asked about with いらっしゃいます."),
                 ("すこし まって ください です。", "すこし おまちください。", "On a business call, おまちください.")]),
              [D("たろう", "いつも おせわに なっております。たなかさんは いらっしゃいますか。", "Itsumo osewa ni natte orimasu. Tanaka-san wa irasshaimasu ka.", "Thank you for your continued help. Is Mr Tanaka there?"),
               D("ゆき", "すこし おまちください。", "Sukoshi omachi kudasai.", "One moment, please."),
               D("ゆき", "すみません、いま いません。", "Sumimasen, ima imasen.", "Sorry, he is not here right now."),
               D("たろう", "では、おりかえし でんわします。", "De wa, orikaeshi denwa shimasu.", "Then I will call back.")],
              WS("Phone worksheet", [
                  T("Open the call.", ["thank you for your continued help", "is Mr Tanaka there?"],
                    ["いつも おせわに なっております", "たなかさんは いらっしゃいますか"]),
                  T("Handle the absence.", ["one moment, please", "I will call back"],
                    ["すこし おまちください", "おりかえし でんわします"]),
              ])),
            L("でんごんを あずかる",
              "Taking a message asks four things in order: おなまえ、おでんわばんごう、ごようけん、 "
              "ごでんごん. Each ends with おねがいします and the whole message is read back.",
              [V("でんごん", "dengon", "message", "noun"),
               V("おなまえ", "onamae", "name (polite)", "noun"),
               V("ごようけん", "goyouken", "business, matter (polite)", "noun"),
               V("くりかえします", "kurikaeshimasu", "to repeat back", "verb"),
               V("うけたまわります", "uketamawarimasu", "to receive, to hear (humble)", "verb")],
              G("Taking a message",
                "おなまえを おねがいします · ごでんごんを おねがいします · くりかえします · うけたまわりました",
                "The four questions are fixed phrases, and the confirmation is くりかえします "
                "followed by the message. A message is not taken until it has been read back.",
                [X("おなまえを おねがいします。", "Onamae o onegaishimasu.", "Your name, please."),
                 X("ごでんごんを おねがいします。", "Godengon o onegaishimasu.", "Your message, please."),
                 X("くりかえします。あしたの ごご さんじですね。", "Kurikaeshimasu. Ashita no gogo sanji desu ne.", "Let me repeat it back. Tomorrow at three in the afternoon, then.")],
                [("なまえ を ください。", "おなまえを おねがいします。", "Business phrases take おねがいします, not ください."),
                 ("くりかえします です。", "くりかえします。", "ます ends the sentence; です does not follow.")]),
              [D("ゆき", "おなまえを おねがいします。", "Onamae o onegaishimasu.", "Your name, please."),
               D("たろう", "たろう です。あしたの ごご さんじに おねがいします。", "Tarou desu. Ashita no gogo sanji ni onegaishimasu.", "It is Taro. Tomorrow at three in the afternoon, please."),
               D("ゆき", "はい。くりかえします。あしたの ごご さんじですね。", "Hai. Kurikaeshimasu. Ashita no gogo sanji desu ne.", "Yes. Let me repeat it back. Tomorrow at three in the afternoon, then."),
               D("たろう", "はい、その とおりです。ありがとう ございます。", "Hai, sono toori desu. Arigatou gozaimasu.", "Yes, that is right. Thank you.")],
              WS("Message worksheet", [
                  T("Take the details.", ["your name, please", "your message, please"],
                    ["おなまえを おねがいします", "ごでんごんを おねがいします"]),
                  T("Read it back.", ["let me repeat it back", "tomorrow at three in the afternoon, then"],
                    ["くりかえします", "あしたの ごご さんじですね"]),
              ])),
        ]},
        {"id": "A2+-U2", "title": "ちょっとした はなし", "lessons": [
            L("てんきの はなし",
              "Small talk in Japanese works by agreeing first: そうですね、きょうは あついですね. "
              "〜ですね invites agreement and the answer repeats it before adding anything.",
              [V("あつい", "atsui", "hot", "adjective"),
               V("さむい", "samui", "cold", "adjective"),
               V("すずしい", "suzushii", "cool, pleasant", "adjective"),
               V("そうですね", "sou desu ne", "that is so, isn't it", "phrase"),
               V("あめ", "ame", "rain", "noun")],
              G("Weather small talk",
                "きょうは あついですね · そうですね · あしたは あめらしいです",
                "The ね at the end asks for agreement; the reply opens with そうですね before any "
                "new information. Hearsay takes らしいです: あめらしいです (it seems it will rain).",
                [X("きょうは あついですね。", "Kyou wa atsui desu ne.", "It is hot today, isn't it."),
                 X("そうですね。でも、ゆうべは すずしかったです。", "Sou desu ne. Demo, yuube wa suzushikatta desu.", "That is so. But last night was cool."),
                 X("あしたは あめらしいです。", "Ashita wa ame rashii desu.", "It seems it will rain tomorrow.")],
                [("きょうは あついですか ね。", "きょうは あついですね。", "Agreement is invited with ね, with no か."),
                 ("あつい と いいます ね。", "あついですね。", "The tag is ね, not と いいます.")]),
              [D("ゆき", "きょうは あついですね。", "Kyou wa atsui desu ne.", "It is hot today, isn't it."),
               D("たろう", "そうですね。でも、あしたは あめらしいです。", "Sou desu ne. Demo, ashita wa ame rashii desu.", "That is so. But it seems it will rain tomorrow."),
               D("ゆき", "そうですか。かさが ひつようですね。", "Sou desu ka. Kasa ga hitsuyou desu ne.", "Is that so? Then an umbrella is needed."),
               D("たろう", "ええ、たしかに。", "Ee, tashika ni.", "Yes, indeed.")],
              WS("Weather worksheet", [
                  T("Invite agreement.", ["it is hot today, isn't it", "that is so"],
                    ["きょうは あついですね", "そうですね"]),
                  T("Add the forecast.", ["it seems it will rain tomorrow", "an umbrella is needed"],
                    ["あしたは あめらしいです", "かさが ひつようですね"]),
              ])),
            L("しゅみの はなし",
              "Hobbies are described with よく and ときどき before the verb: よく えいがを "
              "みます. Frequency words do the work that tense could never do.",
              [V("しゅみ", "shumi", "hobby", "noun"),
               V("ときどき", "tokidoki", "sometimes", "adverb"),
               V("よく", "yoku", "often", "adverb"),
               V("あまり", "amari", "not often (with a negative)", "adverb"),
               V("ひとりで", "hitori de", "on one's own", "phrase")],
              G("Hobbies and frequency",
                "しゅみは 〜です · よく えいがを みます · ときどき ひとりで いきます",
                "The hobby is named with しゅみは 〜です and then supported by a frequency "
                "sentence. あまり needs a negative: あまり いきません.",
                [X("しゅみは えいがです。", "Shumi wa eiga desu.", "My hobby is films."),
                 X("よく えいがを みます。", "Yoku eiga o mimasu.", "I often watch films."),
                 X("あまり いえでは みません。", "Amari ie de wa mimasen.", "I do not often watch them at home.")],
                [("しゅみ は えいが を みます。", "しゅみは えいがです。", "The hobby is a noun with です, not a verb phrase."),
                 ("あまり みます。", "あまり みません。", "あまり pairs with a negative.")]),
              [D("たろう", "しゅみは なんですか。", "Shumi wa nan desu ka.", "What is your hobby?"),
               D("ゆき", "えいがです。よく ひとりで みに いきます。", "Eiga desu. Yoku hitori de mi ni ikimasu.", "Films. I often go to see them on my own."),
               D("たろう", "どんな えいがが すきですか。", "Donna eiga ga suki desu ka.", "What kind of films do you like?"),
               D("ゆき", "あまり こわい えいがは みません。", "Amari kowai eiga wa mimasen.", "I do not often watch scary films.")],
              WS("Hobbies worksheet", [
                  T("Name the hobby.", ["my hobby is films", "I often watch films"],
                    ["しゅみは えいがです", "よく えいがを みます"]),
                  T("Add the negative.", ["I do not often watch them at home", "what kind of films do you like?"],
                    ["あまり いえでは みません", "どんな えいがが すきですか"]),
              ])),
            L("おすすめ",
              "A recommendation is offered with 〜は どうですか and accepted with ぜひ. おすすめ "
              "is the recommendation itself, and ぜひ is the enthusiasm that closes the exchange.",
              [V("おすすめ", "osusume", "recommendation", "noun"),
               V("どうですか", "dou desu ka", "how about …?", "phrase"),
               V("ぜひ", "zehi", "by all means, definitely", "adverb"),
               V("にんき", "ninki", "popularity", "noun"),
               V("〜たら", "~ tara", "when/if (suggestion)", "conjunction")],
              G("Recommending",
                "おすすめは なんですか · 〜は どうですか · ぜひ 〜て ください",
                "The recommendation is offered with は どうですか and accepted with ぜひ; a "
                "suggestion for someone else takes たら: つかれたら、これを のんで ください.",
                [X("おすすめは なんですか。", "Osusume wa nan desu ka.", "What do you recommend?"),
                 X("この おちゃは どうですか。", "Kono ocha wa dou desu ka.", "How about this tea?"),
                 X("にんきが あります。", "Ninki ga arimasu.", "It is popular.")],
                [("おすすめ を ください。", "おすすめは なんですか。", "Ask for the recommendation with は なんですか."),
                 ("ぜひ のみます ください。", "ぜひ のんで ください。", "ぜひ takes the te-form request.")]),
              [D("ゆき", "おすすめは なんですか。", "Osusume wa nan desu ka.", "What do you recommend?"),
               D("てんいん", "この おちゃは どうですか。にんきが あります。", "Kono ocha wa dou desu ka. Ninki ga arimasu.", "How about this tea? It is popular."),
               D("ゆき", "じゃ、それを おねがいします。", "Ja, sore o onegaishimasu.", "Then that one, please."),
               D("てんいん", "ありがとう ございます。ぜひ あたたかく して のんで ください。", "Arigatou gozaimasu. Zehi atatakaku shite nonde kudasai.", "Thank you. Please do drink it warm.")],
              WS("Recommendation worksheet", [
                  T("Ask and offer.", ["what do you recommend?", "how about this tea?"],
                    ["おすすめは なんですか", "この おちゃは どうですか"]),
                  T("Say it is popular.", ["it is popular", "please do drink it warm"],
                    ["にんきが あります", "ぜひ あたたかく して のんで ください"]),
              ])),
        ]},
        {"id": "A2+-U3", "title": "サービス", "lessons": [
            L("ゆうびんきょくで",
              "Posting takes おくります, stamps are きって, and a parcel is こづつみ. Size decides "
              "the price, so the counter asks 大きさは.",
              [V("きって", "kitte", "stamp", "noun"),
               V("こづつみ", "kozutsumi", "parcel", "noun"),
               V("おくります", "okurimasu", "to send", "verb"),
               V("ふなびん", "funabin", "sea mail", "noun"),
               V("こうくうびん", "koukuubin", "air mail", "noun")],
              G("At the post office",
                "これを おくります · きっては いくらですか · こうくうびんで おねがいします",
                "The item takes を and the service takes で: こうくうびんで おくります. The price "
                "question is asked about the stamp, and the choice of service closes the request.",
                [X("この こづつみを おくります。", "Kono kozutsumi o okurimasu.", "I will send this parcel."),
                 X("こうくうびんで おねがいします。", "Koukuubin de onegaishimasu.", "By air mail, please."),
                 X("きっては いくらですか。", "Kitte wa ikura desu ka.", "How much is a stamp?")],
                [("こうくうびん に おくります。", "こうくうびんで おくります。", "The means takes で: by air mail."),
                 ("こづつみ が おくります。", "こづつみを おくります。", "What is sent takes を.")]),
              [D("ゆき", "この こづつみを おくります。", "Kono kozutsumi o okurimasu.", "I will send this parcel."),
               D("てんいん", "こうくうびんで いいですか。", "Koukuubin de ii desu ka.", "Is air mail all right?"),
               D("ゆき", "はい。いくらですか。", "Hai. Ikura desu ka.", "Yes. How much is it?"),
               D("てんいん", "せんひゃくえん です。", "Senhyaku en desu.", "It is one thousand one hundred yen.")],
              WS("Post worksheet", [
                  T("Send the parcel.", ["I will send this parcel", "by air mail, please"],
                    ["この こづつみを おくります", "こうくうびんで おねがいします"]),
                  T("Ask the price.", ["how much is a stamp?", "is air mail all right?"],
                    ["きっては いくらですか", "こうくうびんで いいですか"]),
              ])),
            L("ぎんこうで",
              "Deposits and withdrawals are いれます/おろします, the account is こうざ, and the "
              "clerk asks どのくらい with a polite frame. Nothing is said twice.",
              [V("こうざ", "kouza", "account", "noun"),
               V("おろします", "oroshimasu", "to withdraw", "verb"),
               V("いれます", "iremasu", "to deposit", "verb"),
               V("つうこう", "tsuukou", "passbook", "noun"),
               V("はんこ", "hanko", "name seal", "noun")],
              G("At the bank",
                "こうざを つくります · 〜えん おろします · つうこうを おねがいします",
                "The amount takes を, the counter takes で, and the passbook is handed over with "
                "おねがいします. Numbers are read in Japanese readings at the counter.",
                [X("いちまんえん おろします。", "Ichiman en oroshimasu.", "I will withdraw ten thousand yen."),
                 X("こうざを つくりたいのですが。", "Kouza o tsukuritai no desu ga.", "I would like to open an account, if possible."),
                 X("つうこうを おねがいします。", "Tsuukou o onegaishimasu.", "My passbook, please.")],
                [("こうざ が つくります。", "こうざを つくります。", "What is created takes を."),
                 ("おろします ください です。", "おろします。", "ます ends the sentence; no ください です.")]),
              [D("たろう", "いちまんえん おろします。", "Ichiman en oroshimasu.", "I will withdraw ten thousand yen."),
               D("ゆき", "つうこうを おねがいします。", "Tsuukou o onegaishimasu.", "Your passbook, please."),
               D("たろう", "はい、どうぞ。", "Hai, douzo.", "Yes, here you are."),
               D("ゆき", "はい、いちまんえん です。", "Hai, ichiman en desu.", "Yes, ten thousand yen.")],
              WS("Bank worksheet", [
                  T("Do the transaction.", ["I will withdraw ten thousand yen", "my passbook, please"],
                    ["いちまんえん おろします", "つうこうを おねがいします"]),
                  T("Open an account.", ["I would like to open an account, if possible", "here you are"],
                    ["こうざを つくりたいのですが", "はい、どうぞ"]),
              ])),
            L("みせで もんだいが あったら",
              "A problem at a counter is described with the receipt (レシート) and the fix asked for "
              "with とりかえて いただけますか. もうしわけございません answers from the other side.",
              [V("レシート", "reshiito", "receipt", "noun"),
               V("とりかえ", "torikae", "exchange, replacement", "noun"),
               V("まちがい", "machigai", "mistake", "noun"),
               V("たしかめます", "tashikamemasu", "to check, to verify", "verb"),
               V("もうしわけ ございません", "moushiwake gozaimasen", "we are very sorry", "phrase")],
              G("Fixing a problem",
                "レシートは あります · まちがいが ありました · とりかえて いただけますか · もうしわけ ございません",
                "The problem is stated as a fact (まちがいが ありました), the repair is requested "
                "with 〜て いただけますか, and the shop answers with もうしわけ ございません plus the "
                "action it will take.",
                [X("レシートは あります。", "Reshiito wa arimasu.", "I have the receipt."),
                 X("とりかえて いただけますか。", "Torikaete itadakemasu ka.", "Could you exchange it?"),
                 X("もうしわけ ございません。すぐに たしかめます。", "Moushiwake gozaimasen. Sugu ni tashikamemasu.", "We are very sorry. We will check at once.")],
                [("とりかえて ください ですか。", "とりかえて いただけますか。", "Requests to staff take 〜て いただけますか."),
                 ("まちがい は ありました。", "まちがいが ありました。", "The new fact takes が.")]),
              [D("ゆき", "すみません、まちがいが ありました。", "Sumimasen, machigai ga arimashita.", "Excuse me, there is a mistake."),
               D("てんいん", "もうしわけ ございません。レシートは ありますか。", "Moushiwake gozaimasen. Reshiito wa arimasu ka.", "We are very sorry. Do you have the receipt?"),
               D("ゆき", "はい。とりかえて いただけますか。", "Hai. Torikaete itadakemasu ka.", "Yes. Could you exchange it?"),
               D("てんいん", "すぐに たしかめます。すこし おまちください。", "Sugu ni tashikamemasu. Sukoshi omachi kudasai.", "I will check at once. One moment, please.")],
              WS("Counter problem worksheet", [
                  T("Describe the problem.", ["there is a mistake", "I have the receipt"],
                    ["まちがいが ありました", "レシートは あります"]),
                  T("Ask for the fix.", ["could you exchange it?", "we are very sorry. We will check at once."],
                    ["とりかえて いただけますか", "もうしわけ ございません。すぐに たしかめます"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Japanese service language is built so that neither side has to make a demand: the "
                 "customer opens with すみません and closes with おねがいします, the clerk apologises "
                 "before checking anything (もうしわけ ございません) and then acts. On the telephone "
                 "the same design runs through おなまえを おねがいします and くりかえします — a message "
                 "is confirmed out loud before it is accepted."),
        source_url="https://en.wikipedia.org/wiki/Customer_service",
        reading=("きんようび、くしゃに でんわが ありました。たなかさんは いませんでしたから、"
                 "おなまえと ごようけんを うけたまわりました。それから、くりかえして、"
                 "ちょうど ごじに おりかえし でんわすると つたえました。あとで ぶちょうに "
                 "ほうこくしました。"),
        reading_gloss=("On Friday there was a telephone call at the office. Mr Tanaka was not in, "
                       "so I took the name and the matter. Then I repeated it back and passed on "
                       "that he would return the call at exactly five. Afterwards I reported it to "
                       "the section manager."),
        listening=("てんいん: いらっしゃいませ。<br>"
                   "ゆき: すみません、レシートは あります。まちがいが ありました。<br>"
                   "てんいん: もうしわけ ございません。とりかえて いただけますか。<br>"
                   "ゆき: おねがいします。"),
        listening_gloss=("Shop assistant: Welcome. Yuki: Excuse me, I have the receipt. There is a "
                         "mistake. Assistant: We are very sorry. Could you exchange it? Yuki: "
                         "Please do."),
        voice_tag=VOICE,
        idioms=[
            ("やすみを とる", "yasumi o toru", "to take a day off"),
            ("いらっしゃいますか", "irasshaimasu ka", "is he/she there? (respectful)"),
            ("すこし おまちください", "sukoshi omachi kudasai", "one moment, please"),
            ("おりかえし でんわします", "orikaeshi denwa shimasu", "I will call back"),
            ("おなまえを おねがいします", "onamae o onegaishimasu", "your name, please"),
            ("そうですね", "sou desu ne", "that is so, isn't it"),
            ("おすすめは なんですか", "osusume wa nan desu ka", "what do you recommend?"),
            ("こうくうびん", "koukuubin", "air mail"),
            ("つうこう", "tsuukou", "passbook"),
            ("もうしわけ ございません", "moushiwake gozaimasen", "we are very sorry"),
        ],
        mistakes=[
            ("なまえ を ください。", "おなまえを おねがいします。", "Business phrases take おねがいします."),
            ("とりかえて ください ですか。", "とりかえて いただけますか。", "Requests to staff take 〜て いただけますか."),
            ("あまり みます。", "あまり みません。", "あまり pairs with a negative."),
        ],
        task_title="Play both sides of one telephone call",
        task_instructions=("Write a ten-line telephone script in Japanese: the caller's opening "
                           "courtesy (いつも おせわに なっております), the request for the person "
                           "(いらっしゃいますか), the hold (すこし おまちください), the absence (いま "
                           "いません), the four message questions, the read-back with くりかえします, "
                           "and the closing. Then read it aloud twice, once as each speaker, and "
                           "mark the line where the two sides could have started arguing in your "
                           "own language but do not here."),
    ),
    "test": [
        ("translate_en", "Say: I would like to take next Friday off, if possible.", "らいしゅうの きんようび、やすみを とりたいのですが。"),
        ("translate_ja", "すこし おまちください。", "One moment, please."),
        ("multiple_choice", "Which sentence is the correct polite request to staff?", "とりかえて いただけますか。"),
        ("fill_in_the_blank", "こうくうびん___ おくります。", "で"),
        ("word_selection", "Select the Japanese for 'I will call back'.", "おりかえし でんわします"),
        ("error_correction", "なまえ を ください。", "おなまえを おねがいします。"),
        ("dialogue_completion", "Complete: たなかさんは いらっしゃいますか。 — ___ (one moment, please)", "すこし おまちください"),
        ("matching", "Match つうこう to its meaning.", "a passbook"),
        ("reading_comprehension", "ちょうど ごじに おりかえし でんわします。 What time will the call be returned?", "five o'clock"),
        ("inference", "「そうですね。でも、あしたは あめらしいです。」 — what is the speaker doing?", "agreeing, then adding a forecast"),
        ("main_idea", "おなまえと ごようけんを うけたまわりました。くりかえします。 What is happening?", "a message is being taken and read back"),
        ("detail_identification", "いちまんえん おろします。 How much is being withdrawn?", "ten thousand yen"),
    ],
}

HALFSTEPS["B1+"] = {
    "title": "Japanese B1+ — Meetings and opinions",
    "native": NATIVE,
    "goals": [
        "Run through an agenda and record what was decided",
        "Agree, disagree and state a condition without losing the room",
        "Report progress and name a risk before the deadline",
    ],
    "units": [
        {"id": "B1+-U1", "title": "かいぎ", "lessons": [
            L("ぎだいを すすめる",
              "The agenda is walked in order with まず、つぎに、さいごに. Taking the floor is "
              "はなしても いいですか, and each point closes with いかがですか.",
              [V("ぎだい", "gidai", "agenda", "noun"),
               V("けん", "ken", "matter, item", "noun"),
               V("つぎに", "tsugi ni", "next", "adverb"),
               V("さいごに", "saigo ni", "finally", "adverb"),
               V("はなしても いいですか", "hanashite mo ii desu ka", "may I speak?", "phrase")],
              G("Walking the agenda",
                "まず 〜の けんから はじめます · つぎに 〜 · はなしても いいですか · いかがですか",
                "The steps are marked with まず/つぎに/さいごに and each item is 〜の けん. Asking "
                "for the floor and asking for opinions both use the same polite question pattern, "
                "which keeps the meeting flat.",
                [X("まず、よさん の けんから はじめます。", "Mazu, yosan no ken kara hajimemasu.", "First, we begin with the budget item."),
                 X("はなしても いいですか。", "Hanashite mo ii desu ka.", "May I speak?"),
                 X("この てん、いかがですか。", "Kono ten, ikaga desu ka.", "How about this point?")],
                [("ぎだい を はじめます です。", "ぎだいを はじめます。", "ます ends the sentence; です does not follow."),
                 ("はなして も いいです か ね。", "はなしても いいですか。", "One closing particle per question.")]),
              [D("ぶちょう", "まず、よさん の けんから はじめます。", "Mazu, yosan no ken kara hajimemasu.", "First, we begin with the budget item."),
               D("たろう", "すみません、はなしても いいですか。", "Sumimasen, hanashite mo ii desu ka.", "Excuse me, may I speak?"),
               D("ぶちょう", "どうぞ。", "Douzo.", "Please go ahead."),
               D("たろう", "つぎに スケジュールを みたいです。", "Tsugi ni sukejuuru o mitai desu.", "Next I would like to look at the schedule.")],
              WS("Agenda worksheet", [
                  T("Walk the items.", ["first, we begin with the budget item", "next I would like to look at the schedule"],
                    ["まず、よさん の けんから はじめます", "つぎに スケジュールを みたいです"]),
                  T("Take the floor.", ["may I speak?", "please go ahead"],
                    ["はなしても いいですか", "どうぞ"]),
              ])),
            L("けっていを きろくする",
              "Decisions are recorded as 〜ことに なりました (it has been decided that …), which is "
              "the written form of a group decision. The owner takes が and the date までに.",
              [V("けってい", "kettei", "decision", "noun"),
               V("きろく", "kiroku", "record", "noun"),
               V("〜ことに なりました", "~ koto ni narimashita", "it has been decided that", "phrase"),
               V("たんとう", "tantou", "person in charge", "noun"),
               V("〜までに", "~ made ni", "by (a deadline)", "postposition")],
              G("Recording decisions",
                "〜ことに なりました · たんとうは 〜さんです · 〜までに おねがいします",
                "The decision is impersonal and past: 〜ことに なりました. The owner is named with "
                "たんとうは and the date with までに. A decision without both lines is not a record.",
                [X("らいしゅう から ためす ことに なりました。", "Raishuu kara tamesu koto ni narimashita.", "It has been decided to test it from next week."),
                 X("たんとうは たろうさんです。", "Tantou wa Tarou-san desu.", "The person in charge is Taro."),
                 X("きんようびまでに おねがいします。", "Kinyoubi made ni onegaishimasu.", "Please do it by Friday.")],
                [("らいしゅう から ためします に なりました。", "らいしゅう から ためす ことに なりました。", "ことに なりました takes the plain form."),
                 ("たんとう が たろうさん を します。", "たんとうは たろうさんです。", "The owner is stated with は and です.")]),
              [D("ぶちょう", "けっていは。", "Kettei wa.", "And the decision?"),
               D("ゆき", "らいしゅう から ためす ことに なりました。", "Raishuu kara tamesu koto ni narimashita.", "It has been decided to test it from next week."),
               D("ぶちょう", "たんとうは。", "Tantou wa.", "And who is in charge?"),
               D("ゆき", "たろうさんです。きんようびまでに おねがいします。", "Tarou-san desu. Kinyoubi made ni onegaishimasu.", "It is Taro. Please do it by Friday.")],
              WS("Decision worksheet", [
                  T("Record the decision.", ["it has been decided to test it from next week", "the person in charge is Taro"],
                    ["らいしゅう から ためす ことに なりました", "たんとうは たろうさんです"]),
                  T("Name the date.", ["please do it by Friday", "and the decision?"],
                    ["きんようびまでに おねがいします", "けっていは"]),
              ])),
            L("ぎじろくを かく",
              "Minutes state present facts, not intentions: 〜て います and 〜ことに なりました, with "
              "が あります for open items. ぎじろく is the document; めも is your own note.",
              [V("ぎじろく", "gijiroku", "minutes", "noun"),
               V("めも", "memo", "memorandum, note", "noun"),
               V("けつろん", "ketsuron", "conclusion", "noun"),
               V("のこります", "nokorimasu", "to remain, to be left", "verb"),
               V("かくだい", "kakudai", "expansion, escalation", "noun")],
              G("Writing minutes",
                "〜て います · 〜ことに なりました · けつろんは 〜です · 〜が のこっています",
                "The present tense records what stands (〜て います), the decision takes ことに "
                "なりました, and what is unresolved is のこっています. Minutes never use たい or "
                "つもり — those are not records.",
                [X("けつろんは テストを ふやす ことです。", "Ketsuron wa tesuto o fuyasu koto desu.", "The conclusion is to increase testing."),
                 X("よさんは まだ のこっています。", "Yosan wa mada nokotte imasu.", "The budget is still outstanding."),
                 X("らいげつ かくだいを けんとう して います。", "Raigetsu kakudai o kentou shite imasu.", "An expansion is under consideration next month.")],
                [("ぎじろく に つもり を かきます。", "ぎじろく に けつろん を かきます。", "Minutes record decisions, not intentions."),
                 ("よさん は のこります です。", "よさんは のこっています。", "An outstanding item is a state: 〜て います.")]),
              [D("ゆき", "ぎじろく、できましたか。", "Gijiroku, dekimashita ka.", "Are the minutes done?"),
               D("たろう", "はい。けつろんは テストを ふやす ことです。", "Hai. Ketsuron wa tesuto o fuyasu koto desu.", "Yes. The conclusion is to increase testing."),
               D("ゆき", "のこって いる けんは。", "Nokotte iru ken wa.", "And the outstanding items?"),
               D("たろう", "よさんは まだ のこっています。", "Yosan wa mada nokotte imasu.", "The budget is still outstanding.")],
              WS("Minutes worksheet", [
                  T("State the conclusion.", ["the conclusion is to increase testing", "the budget is still outstanding"],
                    ["けつろんは テストを ふやす ことです", "よさんは まだ のこっています"]),
                  T("Note what stands.", ["an expansion is under consideration next month", "are the minutes done?"],
                    ["らいげつ かくだいを けんとう して います", "ぎじろく、できましたか"]),
              ])),
        ]},
        {"id": "B1+-U2", "title": "いけん", "lessons": [
            L("さんせいと つけたし",
              "Agreement arrives as たしかに … が、… : concede first, then add. その とおりです "
              "agrees fully, and つけたす (to add a point) keeps the meeting moving.",
              [V("さんせい", "sansei", "agreement", "noun"),
               V("たしかに", "tashika ni", "certainly, it is true that", "adverb"),
               V("その とおり", "sono toori", "exactly that", "phrase"),
               V("つけたします", "tsuketashimasu", "to add (a point)", "verb"),
               V("いちおう", "ichiou", "for the time being, tentatively", "adverb")],
              G("Agreeing with a reservation",
                "たしかに … が、… · その とおりです · ひとつ つけたします · いちおう さんせいです",
                "The concession takes たしかに and the reservation takes が in the same sentence; "
                "an addition is announced with つけたします. いちおう marks a provisional yes.",
                [X("たしかに いい てんも ありますが、コストが ふあんていです。", "Tashika ni ii ten mo arimasu ga, kosuto ga fuantei desu.", "It certainly has good points, but the cost is unstable."),
                 X("その とおりです。", "Sono toori desu.", "Exactly that."),
                 X("いちおう さんせいです。", "Ichiou sansei desu.", "Tentatively, I agree.")],
                [("たしかに いい てん が あります。でも が、コストが…", "たしかに いい てんも ありますが、コストが ふあんていです。", "The concession and the reservation share one sentence, with が."),
                 ("さんせい を します。", "さんせいです。", "Agreement is a state: さんせいです.")]),
              [D("ぶちょう", "この ていあん、どうですか。", "Kono teian, dou desu ka.", "How is this proposal?"),
               D("たろう", "たしかに いい てんも ありますが、コストが ふあんていです。", "Tashika ni ii ten mo arimasu ga, kosuto ga fuantei desu.", "It certainly has good points, but the cost is unstable."),
               D("ゆき", "その とおりです。ひとつ つけたします。", "Sono toori desu. Hitotsu tsuketashimasu.", "Exactly. Let me add one point."),
               D("たろう", "どうぞ。", "Douzo.", "Go ahead.")],
              WS("Agreement worksheet", [
                  T("Concede and reserve.", ["it certainly has good points, but the cost is unstable", "exactly that"],
                    ["たしかに いい てんも ありますが、コストが ふあんていです", "その とおりです"]),
                  T("Add a point.", ["let me add one point", "tentatively, I agree"],
                    ["ひとつ つけたします", "いちおう さんせいです"]),
              ])),
            L("はんたいを いう",
              "Disagreement names the point, not the person: その てんは ちがう と おもいます. "
              "〜と おもいます keeps the claim inside your own judgement, which is what makes it "
              "sayable.",
              [V("はんたい", "hantai", "opposition, disagreement", "noun"),
               V("ちがいます", "chigaimasu", "to differ, to be wrong", "verb"),
               V("りゆう", "riyuu", "reason", "noun"),
               V("もうしあげます", "moushiagemasu", "I say (humble)", "verb"),
               V("けんかい", "kenkai", "view, opinion", "noun")],
              G("Disagreeing",
                "その てんは ちがう と おもいます · りゆうは 〜です · もうしあげますと …",
                "The disagreement attaches to その てん (that point) and is wrapped in と おもいます; "
                "the reason is stated separately, and もうしあげますと opens a humble explanation.",
                [X("その てんは ちがう と おもいます。", "Sono ten wa chigau to omoimasu.", "I think that point is different."),
                 X("りゆうは データが たりない からです。", "Riyuu wa deeta ga tarinai kara desu.", "The reason is that the data is insufficient."),
                 X("もうしあげますと、コストが あがります。", "Moushiagemasu to, kosuto ga agarimasu.", "If I may say so, the cost rises.")],
                [("あなた は ちがいます。", "その てんは ちがいます。", "Disagreement is attached to the point, not the person."),
                 ("ちがいます と おもいます です。", "ちがう と おもいます。", "と おもいます takes the plain form.")]),
              [D("たろう", "すぐに はじめましょう。", "Sugu ni hajimemashou.", "Let us start at once."),
               D("ゆき", "その てんは ちがう と おもいます。", "Sono ten wa chigau to omoimasu.", "I think that point is different."),
               D("たろう", "りゆうは。", "Riyuu wa.", "The reason?"),
               D("ゆき", "もうしあげますと、データが たりない からです。", "Moushiagemasu to, deeta ga tarinai kara desu.", "If I may say so, it is because the data is insufficient.")],
              WS("Disagreement worksheet", [
                  T("Disagree with the point.", ["I think that point is different", "the reason is that the data is insufficient"],
                    ["その てんは ちがう と おもいます", "りゆうは データが たりない からです"]),
                  T("Explain humbly.", ["if I may say so, the cost rises", "let us start at once"],
                    ["もうしあげますと、コストが あがります", "すぐに はじめましょう"]),
              ])),
            L("じょうけんを つける",
              "Conditions are set with 〜ばあい (in the case that) and 〜なら (if it is a matter of). "
              "The condition comes first and the offer second: よさんが でるなら、できます.",
              [V("じょうけん", "jouken", "condition", "noun"),
               V("ばあい", "baai", "case, situation", "noun"),
               V("〜なら", "~ nara", "if it is the case that", "conjunction"),
               V("かのう", "kanou", "possible", "adjective"),
               V("ていあん", "teian", "proposal", "noun")],
              G("Setting conditions",
                "〜ばあい は 〜 · 〜なら できます · じょうけんを つけます",
                "〜ばあい takes は and stands at the head of its clause; 〜なら attaches to the "
                "condition itself. Both leave the decision with the other side, which is why a "
                "condition is easier to accept than a refusal.",
                [X("よさんが でる ばあいは、すぐに できます。", "Yosan ga deru baai wa, sugu ni dekimasu.", "In the case that the budget comes through, it can be done at once."),
                 X("ことし なら できます。", "Kotoshi nara dekimasu.", "If it is this year, it is possible."),
                 X("じょうけんを つけます。", "Jouken o tsukemasu.", "I am setting a condition.")],
                [("よさん が でる ばあい に は、できます。", "よさんが でる ばあいは、できます。", "〜ばあい takes は, with no に."),
                 ("ことし なら できます です。", "ことし なら できます。", "ます already ends the sentence.")]),
              [D("ぶちょう", "その ていあん、うけられますか。", "Sono teian, ukeraremasu ka.", "Can you accept that proposal?"),
               D("ゆき", "じょうけんを つけます。よさんが でる ばあいは、すぐに できます。", "Jouken o tsukemasu. Yosan ga deru baai wa, sugu ni dekimasu.", "I set a condition. If the budget comes through, it can be done at once."),
               D("ぶちょう", "ことし なら。", "Kotoshi nara.", "And if it is this year?"),
               D("ゆき", "ことし なら かのうです。", "Kotoshi nara kanou desu.", "If it is this year, it is possible.")],
              WS("Conditions worksheet", [
                  T("Set the condition.", ["in the case that the budget comes through, it can be done at once", "if it is this year, it is possible"],
                    ["よさんが でる ばあいは、すぐに できます", "ことし なら できます"]),
                  T("Name the frame.", ["I am setting a condition", "can you accept that proposal?"],
                    ["じょうけんを つけます", "その ていあん、うけられますか"]),
              ])),
        ]},
        {"id": "B1+-U3", "title": "しめきり", "lessons": [
            L("すすみぐあいを ほうこくする",
              "Progress is reported with 〜て います plus a percentage or a stage: はんぶん まで "
              "すすんで います. A delay is owned with おくれて います, not excused.",
              [V("すすみぐあい", "susumigurai", "progress", "noun"),
               V("おくれ", "okure", "delay", "noun"),
               V("げんざい", "genzai", "currently, at present", "noun"),
               V("みこみ", "mikomi", "prospect, outlook", "noun"),
               V("ほうこく", "houkoku", "report", "noun")],
              G("Reporting progress",
                "〜まで すすんで います · げんざい 〜を して います · おくれて います · みこみは 〜です",
                "The stage takes まで with すすんで います, the outlook takes みこみは, and a delay "
                "is stated plainly before the new estimate. Nothing is promised in the past tense.",
                [X("はんぶん まで すすんで います。", "Hanbun made susunde imasu.", "It is half done."),
                 X("すこし おくれて います。", "Sukoshi okurete imasu.", "It is a little behind."),
                 X("みこみは らいしゅうの きんようびです。", "Mikomi wa raishuu no kinyoubi desu.", "The outlook is next Friday.")],
                [("はんぶん が すすんで います。", "はんぶん まで すすんで います。", "A stage takes まで."),
                 ("おくれて います です。", "おくれて います。", "います ends the sentence; です does not follow.")]),
              [D("ぶちょう", "すすみぐあいは。", "Susumigurai wa.", "How is progress?"),
               D("たろう", "げんざい、はんぶん まで すすんで います。", "Genzai, hanbun made susunde imasu.", "At present it is half done."),
               D("ぶちょう", "おくれて いますか。", "Okurete imasu ka.", "Is it behind?"),
               D("たろう", "すこし おくれて います。みこみは らいしゅうの きんようびです。", "Sukoshi okurete imasu. Mikomi wa raishuu no kinyoubi desu.", "It is a little behind. The outlook is next Friday.")],
              WS("Progress worksheet", [
                  T("Report the stage.", ["it is half done", "it is a little behind"],
                    ["はんぶん まで すすんで います", "すこし おくれて います"]),
                  T("Give the outlook.", ["the outlook is next Friday", "is it behind?"],
                    ["みこみは らいしゅうの きんようびです", "おくれて いますか"]),
              ])),
            L("リスクを さきに いう",
              "A risk is raised before it lands: 〜かもしれない and 〜おそれがあります, each followed "
              "by a counter-measure with 〜て おきます. Naming the risk early is a courtesy, not a "
              "confession.",
              [V("リスク", "risuku", "risk", "noun"),
               V("おそれ", "osore", "risk, fear of", "noun"),
               V("そなえます", "sonaemasu", "to prepare for", "verb"),
               V("〜て おきます", "~ te okimasu", "to do in advance", "phrase"),
               V("たいさく", "taisaku", "counter-measure", "noun")],
              G("Raising a risk",
                "〜かもしれ ません · 〜おそれがあります · たいさく として 〜て おきます",
                "The risk is hedged (かもしれません / おそれがあります) and the counter-measure is "
                "announced with たいさく として plus 〜て おきます — already done, not planned.",
                [X("まにあわない おそれが あります。", "Maniawanai osore ga arimasu.", "There is a risk it will not be in time."),
                 X("たいさく として、てつだいを たのみます。", "Taisaku to shite, tetsudai o tanomimasu.", "As a counter-measure, I will ask for help."),
                 X("メールは もう おくって おきます。", "Meeru wa mou okutte okimasu.", "I will have sent the email in advance.")],
                [("まにあいません かもしれない です。", "まにあわない かもしれません。", "かもしれません attaches to the plain negative."),
                 ("たいさく を します として。", "たいさく として 〜て おきます。", "A counter-measure is prepared in advance: 〜て おきます.")]),
              [D("たろう", "リスクは ありますか。", "Risuku wa arimasu ka.", "Is there a risk?"),
               D("ゆき", "まにあわない おそれが あります。", "Maniawanai osore ga arimasu.", "There is a risk it will not be in time."),
               D("たろう", "たいさくは。", "Taisaku wa.", "And the counter-measure?"),
               D("ゆき", "てつだいを たのみます。メールは もう おくって おきます。", "Tetsudai o tanomimasu. Meeru wa mou okutte okimasu.", "I will ask for help. I will have sent the email in advance.")],
              WS("Risk worksheet", [
                  T("Name the risk.", ["there is a risk it will not be in time", "is there a risk?"],
                    ["まにあわない おそれが あります", "リスクは ありますか"]),
                  T("Give the counter-measure.", ["as a counter-measure, I will ask for help", "I will have sent the email in advance"],
                    ["たいさく として、てつだいを たのみます", "メールは もう おくって おきます"]),
              ])),
            L("ふりかえりと つぎの いっぽ",
              "A review asks what worked with どこが よかったですか and what to change with つぎは "
              "どうしますか. ふりかえり is the act; かいぜん is the change it produces.",
              [V("ふりかえり", "furikaeri", "review, looking back", "noun"),
               V("かいぜん", "kaizen", "improvement", "noun"),
               V("げんいん", "gen'in", "cause", "noun"),
               V("つぎの いっぽ", "tsugi no ippo", "the next step", "phrase"),
               V("まとめます", "matomemasu", "to summarise, to bring together", "verb")],
              G("Reviewing",
                "どこが よかったですか · つぎは どうしますか · げんいんは ひとつに しぼります · つぎの いっぽは 〜です",
                "The review separates what worked from what to change, and the cause is narrowed "
                "to one (ひとつに しぼります) because a list of causes produces no change. The "
                "closing names the next step in one sentence.",
                [X("どこが よかったですか。", "Doko ga yokatta desu ka.", "What went well?"),
                 X("げんいんは ひとつに しぼります。", "Gen'in wa hitotsu ni shiborimasu.", "Let us narrow the cause to one."),
                 X("つぎの いっぽは テストを ふやす ことです。", "Tsugi no ippo wa tesuto o fuyasu koto desu.", "The next step is to increase testing.")],
                [("げんいん を たくさん いいます。", "げんいんは ひとつに しぼります。", "A review narrows the cause to one to produce a change."),
                 ("つぎの いっぽ が テスト を します。", "つぎの いっぽは テストを ふやす ことです。", "The step is a noun phrase with ことです.")]),
              [D("ぶちょう", "ふりかえりを おねがいします。", "Furikaeri o onegaishimasu.", "Please give us the review."),
               D("ゆき", "どこが よかったですか、から はじめます。", "Doko ga yokatta desu ka, kara hajimemasu.", "I will start with what went well."),
               D("ぶちょう", "げんいんは。", "Gen'in wa.", "And the cause?"),
               D("ゆき", "ひとつに しぼります。つぎの いっぽは テストを ふやす ことです。", "Hitotsu ni shiborimasu. Tsugi no ippo wa tesuto o fuyasu koto desu.", "I will narrow it to one. The next step is to increase testing.")],
              WS("Review worksheet", [
                  T("Open the review.", ["what went well?", "let us narrow the cause to one"],
                    ["どこが よかったですか", "げんいんは ひとつに しぼります"]),
                  T("Name the step.", ["the next step is to increase testing", "please give us the review"],
                    ["つぎの いっぽは テストを ふやす ことです", "ふりかえりを おねがいします"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("A Japanese meeting decides through 根回し — the conversations held before the "
                 "meeting — and the meeting itself records the decision: 〜ことに なりました. That is "
                 "why a proposal is rarely argued to a vote in the room: disagreement is aired "
                 "earlier, tentatively (いちおう), and attached to the point rather than the person "
                 "(その てんは ちがう と おもいます). Minutes then state what stands, not what "
                 "anyone wants."),
        source_url="https://en.wikipedia.org/wiki/Consensus_decision-making",
        reading=("きんようびの かいぎで、まず よさん の けんを はなしました。たしかに いい "
                 "てんも ありますが、コストが ふあんていだ と いう いけんが でました。"
                 "けっきょく、らいしゅう から ためす ことに なりました。たんとうは たろうさんで、"
                 "きんようびまでに ほうこくします。よさんは まだ のこっています。"),
        reading_gloss=("At Friday's meeting we discussed the budget item first. The opinion was "
                       "raised that it certainly has good points, but the cost is unstable. In the "
                       "end it was decided to test it from next week. The person in charge is "
                       "Taro, and he will report by Friday. The budget is still outstanding."),
        listening=("ぶちょう: その ていあん、どうですか。<br>"
                   "たろう: たしかに いい てんも ありますが、コストが ふあんていです。<br>"
                   "ぶちょう: では、じょうけんを つけましょうか。<br>"
                   "たろう: はい。よさんが でる ばあいは、すぐに できます。"),
        listening_gloss=("Manager: How is that proposal? Taro: It certainly has good points, but "
                         "the cost is unstable. Manager: Then shall we attach a condition? Taro: "
                         "Yes. If the budget comes through, it can be done at once."),
        voice_tag=VOICE,
        idioms=[
            ("ぎだい", "gidai", "agenda"),
            ("ことに なりました", "koto ni narimashita", "it has been decided that"),
            ("その とおりです", "sono toori desu", "exactly that"),
            ("いちおう", "ichiou", "tentatively"),
            ("じょうけんを つける", "jouken o tsukeru", "to attach a condition"),
            ("すすみぐあい", "susumigurai", "progress"),
            ("みこみ", "mikomi", "outlook, prospect"),
            ("おそれがあります", "osore ga arimasu", "there is a risk of"),
            ("〜て おきます", "~ te okimasu", "to do in advance"),
            ("ふりかえり", "furikaeri", "review, retrospective"),
        ],
        mistakes=[
            ("ぎじろく に つもり を かきます。", "ぎじろく に けつろん を かきます。", "Minutes record decisions, not intentions."),
            ("あなた は ちがいます。", "その てんは ちがう と おもいます。", "Disagreement attaches to the point, not the person."),
            ("ことし なら できます です。", "ことし なら できます。", "ます already ends the sentence."),
        ],
        task_title="Run a fifteen-minute meeting and write its minutes",
        task_instructions=("Take one decision you have to make this week and write the Japanese for "
                           "it: the three agenda items with まず/つぎに/さいごに, the concession and "
                           "reservation in one sentence (たしかに … が、…), one condition (〜ばあい "
                           "は / 〜なら), the decision as it would be recorded (〜ことに なりました), "
                           "the person in charge and the date with までに, and one outstanding item "
                           "with のこっています. If a line has no owner or no date, the decision is "
                           "not recorded."),
    ),
    "test": [
        ("translate_en", "Say: It has been decided to test it from next week.", "らいしゅう から ためす ことに なりました。"),
        ("translate_ja", "その てんは ちがう と おもいます。", "I think that point is different."),
        ("multiple_choice", "Which sentence raises a risk correctly?", "まにあわない おそれが あります。"),
        ("fill_in_the_blank", "よさんが でる ばあい__、すぐに できます。", "は"),
        ("word_selection", "Select the Japanese for 'the outlook is next Friday'.", "みこみは らいしゅうの きんようびです"),
        ("error_correction", "あなた は ちがいます。", "その てんは ちがう と おもいます。"),
        ("dialogue_completion", "Complete: たんとうは。 — ___ (it is Taro)", "たろうさんです"),
        ("matching", "Match ふりかえり to its meaning.", "a review, retrospective"),
        ("reading_comprehension", "きんようびまでに ほうこくします。 By when will the report be made?", "by Friday"),
        ("inference", "「たしかに いい てんも ありますが…」 — what is the speaker about to do?", "agree partly, then object"),
        ("main_idea", "けつろんは テストを ふやす ことです。よさんは のこっています。 What is this?", "minutes of a meeting"),
        ("detail_identification", "はんぶん まで すすんで います。 How far along is the work?", "half done"),
    ],
}

HALFSTEPS["B2+"] = {
    "title": "Japanese B2+ — Data, reports and summaries",
    "native": NATIVE,
    "goals": [
        "Read figures and charts aloud and say what they do not show",
        "Write a proposal, a correction and a reply in formal Japanese",
        "Summarise a document in three sentences and confirm it",
    ],
    "units": [
        {"id": "B2+-U1", "title": "データで はなす", "lessons": [
            L("すうじを よむ",
              "Figures are stated with their population before the number: ひゃくにんの なかで "
              "はんぶん. わりあい、へいきん and ちょうさ are the three words that keep a number "
              "honest.",
              [V("ちょうさ", "chousa", "survey, investigation", "noun"),
               V("たいしょう", "taishou", "target group, subjects", "noun"),
               V("ひゃくぶんりつ", "hyakubunritsu", "percentage", "noun"),
               V("ふえる", "fueru", "to increase", "verb"),
               V("くらべます", "kurabemasu", "to compare", "verb")],
              G("Stating figures",
                "ちょうさに よると · 〜の なかで はんぶん · ひゃくぶんりつで いうと · きょねんと くらべると",
                "The source takes に よると, the population の なかで, and a comparison と "
                "くらべると. A percentage with no population attached is not reported in Japanese "
                "technical writing.",
                [X("ちょうさに よると、ひゃくにんの なかで はんぶんが つかって います。", "Chousa ni yoru to, hyakunin no naka de hanbun ga tsukatte imasu.", "According to the survey, half of a hundred people use it."),
                 X("きょねんと くらべると、にわり ふえました。", "Kyonen to kuraberu to, niwari fuemashita.", "Compared with last year, it increased by twenty per cent."),
                 X("たいしょうは にじゅうだいです。", "Taishou wa nijuudai desu.", "The subjects are people in their twenties.")],
                [("はんぶん が つかって います です。", "はんぶんが つかって います。", "います ends the sentence; です does not follow."),
                 ("ちょうさ に よって、はんぶん。", "ちょうさに よると、はんぶんが つかって います。", "A source takes に よると with the plain clause.")]),
              [D("ぶちょう", "その すうじ、どこからですか。", "Sono suuji, doko kara desu ka.", "Where is that figure from?"),
               D("たろう", "ちょうさに よると、ひゃくにんの なかで はんぶんが つかって います。", "Chousa ni yoru to, hyakunin no naka de hanbun ga tsukatte imasu.", "According to the survey, half of a hundred people use it."),
               D("ぶちょう", "たいしょうは。", "Taishou wa.", "And the group?"),
               D("たろう", "にじゅうだいです。きょねんと くらべると にわり ふえました。", "Nijuudai desu. Kyonen to kuraberu to niwari fuemashita.", "People in their twenties. Compared with last year it rose by twenty per cent.")],
              WS("Figures worksheet", [
                  T("State the figure.", ["according to the survey, half of a hundred people use it", "compared with last year, it increased by twenty per cent"],
                    ["ちょうさに よると、ひゃくにんの なかで はんぶんが つかって います", "きょねんと くらべると、にわり ふえました"]),
                  T("Name the group.", ["the subjects are people in their twenties", "where is that figure from?"],
                    ["たいしょうは にじゅうだいです", "その すうじ、どこからですか"]),
              ])),
            L("グラフを せつめいする",
              "A chart is described from its axes outward: たてじく (vertical axis), よこじく "
              "(horizontal), うえに のぼる (to rise), さがる (to fall). The description states the "
              "movement, not the meaning.",
              [V("たてじく", "tatejiku", "vertical axis", "noun"),
               V("よこじく", "yokojiku", "horizontal axis", "noun"),
               V("のぼります", "nobarimasu", "to rise", "verb"),
               V("さがります", "sagarimasu", "to fall", "verb"),
               V("よこばい", "yokobai", "flat, level (no change)", "noun")],
              G("Describing a chart",
                "よこじくは 〜です · うえに のぼって います · さがって います · よこばいです",
                "The axes are named first, then the movement with 〜て います. The interpretation "
                "comes in a separate sentence, and the description itself avoids だから — a chart "
                "does not explain itself.",
                [X("よこじくは つきです。", "Yokojiku wa tsuki desu.", "The horizontal axis is months."),
                 X("しがつから うえに のぼって います。", "Shigatsu kara ue ni nobotte imasu.", "It rises from April."),
                 X("ごがつは よこばいです。", "Gogatsu wa yokobai desu.", "May is flat.")],
                [("グラフ が うえに のぼります です。", "グラフは うえに のぼって います。", "A continuing movement is a state: 〜て います."),
                 ("さがって います から、だから げんいん です。", "さがって います。げんいんは べつに かくにんします。", "A chart shows a movement; the cause is a separate claim.")]),
              [D("ゆき", "グラフを せつめいして ください。", "Gurafu o setsumei shite kudasai.", "Please describe the chart."),
               D("たろう", "よこじくは つき、たてじくは こすうです。", "Yokojiku wa tsuki, tatejiku wa kosuu desu.", "The horizontal axis is months, the vertical is units."),
               D("ゆき", "うごきは。", "Ugoki wa.", "And the movement?"),
               D("たろう", "しがつから うえに のぼって います。ごがつは よこばいです。", "Shigatsu kara ue ni nobotte imasu. Gogatsu wa yokobai desu.", "It rises from April. May is flat.")],
              WS("Chart worksheet", [
                  T("Name the axes.", ["the horizontal axis is months", "the vertical is units"],
                    ["よこじくは つきです", "たてじくは こすうです"]),
                  T("Describe the movement.", ["it rises from April", "May is flat"],
                    ["しがつから うえに のぼって います", "ごがつは よこばいです"]),
              ])),
            L("けつろんを かく",
              "A conclusion says what can and cannot be claimed: 〜と いえます (one can say), "
              "〜とは いえません (one cannot), 〜べきです (one should). The negative claim is what "
              "protects the paper.",
              [V("けつろん", "ketsuron", "conclusion", "noun"),
               V("いえます", "iemasu", "one can say", "verb"),
               V("かんれん", "kanren", "correlation", "noun"),
               V("げんいん", "gen'in", "cause", "noun"),
               V("さける", "sakeru", "to avoid", "verb")],
              G("Writing a conclusion",
                "〜と いえます · 〜とは いえません · 〜べきです · げんいんは さけて かきます",
                "The positive claim takes と いえます, the limit とは いえません, and the "
                "recommendation べきです. The cause is deliberately left out when the data supports "
                "only a correlation.",
                [X("かんれんが ある と いえます。", "Kanren ga aru to iemasu.", "One can say there is a correlation."),
                 X("げんいん とは いえません。", "Gen'in to wa iemasen.", "One cannot say it is the cause."),
                 X("データを ふやす べきです。", "Deeta o fuyasu beki desu.", "One should increase the data.")],
                [("かんれん が あります と いえます です。", "かんれんが ある と いえます。", "と いえます takes the plain form."),
                 ("げんいん を いえます。", "かんれん を いえます。", "Two series moving together gives correlation, not cause.")]),
              [D("ゆき", "けつろんは。", "Ketsuron wa.", "And the conclusion?"),
               D("たろう", "かんれんが ある と いえます。", "Kanren ga aru to iemasu.", "One can say there is a correlation."),
               D("ゆき", "げんいんは。", "Gen'in wa.", "And the cause?"),
               D("たろう", "げんいん とは いえません。データを ふやす べきです。", "Gen'in to wa iemasen. Deeta o fuyasu beki desu.", "One cannot say it is the cause. We should increase the data.")],
              WS("Conclusion worksheet", [
                  T("Claim what is supported.", ["one can say there is a correlation", "one cannot say it is the cause"],
                    ["かんれんが ある と いえます", "げんいん とは いえません"]),
                  T("Recommend the next step.", ["we should increase the data", "and the conclusion?"],
                    ["データを ふやす べきです", "けつろんは"]),
              ])),
        ]},
        {"id": "B2+-U2", "title": "レポートを かく", "lessons": [
            L("レポートの こうせい",
              "The three headings are fixed: はじめに、ほんろん、おわりに. Each paragraph states "
              "one thing, and the connective また opens a supporting point rather than a new one.",
              [V("こうせい", "kousei", "structure, composition", "noun"),
               V("はじめに", "hajime ni", "introduction", "phrase"),
               V("ほんろん", "honron", "main body", "noun"),
               V("おわりに", "owari ni", "conclusion", "phrase"),
               V("また", "mata", "also, furthermore", "conjunction")],
              G("Report structure",
                "はじめに、〜 · ほんろんでは 〜 · また、〜 · おわりに、〜",
                "The headings are written and each one opens with a topic sentence; また adds a "
                "supporting point to the same claim and does not introduce a new one. One "
                "statement per paragraph is the whole method.",
                [X("はじめに、もくてきを かきます。", "Hajime ni, mokuteki o kakimasu.", "First, I write the purpose."),
                 X("また、コストの てんも あります。", "Mata, kosuto no ten mo arimasu.", "There is also the matter of cost."),
                 X("おわりに、けつろんを のべます。", "Owari ni, ketsuron o nobemasu.", "Finally, I state the conclusion.")],
                [("はじめに、そして また おわりに。", "はじめに、ほんろん、おわりに。", "The three headings stand alone; また belongs inside the body."),
                 ("ほんろん は ふたつの はなし。", "ほんろんでは ひとつずつ かきます。", "One statement per paragraph.")]),
              [D("ぶちょう", "こうせいは。", "Kousei wa.", "And the structure?"),
               D("ゆき", "はじめに、ほんろん、おわりに です。", "Hajime ni, honron, owari ni desu.", "Introduction, body, conclusion."),
               D("ぶちょう", "ほんろんは。", "Honron wa.", "And the body?"),
               D("ゆき", "ひとつずつ かきます。また、コストの てんも あります。", "Hitotsu zutsu kakimasu. Mata, kosuto no ten mo arimasu.", "One point at a time. There is also the matter of cost.")],
              WS("Structure worksheet", [
                  T("Lay out the headings.", ["first, I write the purpose", "finally, I state the conclusion"],
                    ["はじめに、もくてきを かきます", "おわりに、けつろんを のべます"]),
                  T("Add a supporting point.", ["there is also the matter of cost", "and the structure?"],
                    ["また、コストの てんも あります", "こうせいは"]),
              ])),
            L("ていあんを まとめる",
              "A proposal states the aim, the method and the cost in three lines, and asks for a "
              "decision with いかがでしょうか. 〜を ふまえて (in light of) links it to what came "
              "before.",
              [V("ていあん", "teian", "proposal", "noun"),
               V("もくてき", "mokuteki", "purpose, aim", "noun"),
               V("ほうほう", "houhou", "method", "noun"),
               V("ふまえて", "fumaete", "in light of, taking into account", "phrase"),
               V("いかがでしょう か", "ikaga deshou ka", "how does that sound?", "phrase")],
              G("Proposing",
                "もくてきは 〜です · ほうほうは 〜です · 〜を ふまえて · いかがでしょうか",
                "The three lines are stated in the same shape (もくてきは / ほうほうは / ひようは), "
                "the context is acknowledged with を ふまえて, and the decision is requested with "
                "いかがでしょうか — never with an imperative.",
                [X("もくてきは コストを さげることです。", "Mokuteki wa kosuto o sageru koto desu.", "The aim is to lower costs."),
                 X("ほうほうは テストです。", "Houhou wa tesuto desu.", "The method is a test."),
                 X("いぜんの けっか を ふまえて、いかがでしょうか。", "Izen no kekka o fumaete, ikaga deshou ka.", "In light of the earlier result, how does that sound?")],
                [("ていあん を します に ついて。", "ていあんは みっつ の ぎょうです。", "A proposal is three lines, not a paragraph."),
                 ("これを して ください。", "いかがでしょうか。", "A proposal asks for a decision; it does not order one.")]),
              [D("ゆき", "ていあんを おねがいします。", "Teian o onegaishimasu.", "Please give the proposal."),
               D("たろう", "もくてきは コストを さげることです。ほうほうは テストです。", "Mokuteki wa kosuto o sageru koto desu. Houhou wa tesuto desu.", "The aim is to lower costs. The method is a test."),
               D("ゆき", "ひようは。", "Hiyou wa.", "And the cost?"),
               D("たろう", "じゅうまんえん です。いぜんの けっか を ふまえて、いかがでしょうか。", "Juuman en desu. Izen no kekka o fumaete, ikaga deshou ka.", "One hundred thousand yen. In light of the earlier result, how does that sound?")],
              WS("Proposal worksheet", [
                  T("State the three lines.", ["the aim is to lower costs", "the method is a test"],
                    ["もくてきは コストを さげることです", "ほうほうは テストです"]),
                  T("Ask for the decision.", ["in light of the earlier result, how does that sound?", "one hundred thousand yen"],
                    ["いぜんの けっか を ふまえて、いかがでしょうか", "じゅうまんえん です"]),
              ])),
            L("へんじと ていせい",
              "A reply confirms the points and corrects the one that is wrong, using おそれいりますが "
              "for the correction. ていせい (correction) is offered with the correct figure "
              "attached.",
              [V("へんじ", "henji", "reply", "noun"),
               V("ていせい", "teisei", "correction", "noun"),
               V("かくにん", "kakunin", "confirmation", "noun"),
               V("おそれいりますが", "osoreirimasu ga", "I am sorry to trouble you, but", "phrase"),
               V("いじょう", "ijou", "the above", "noun")],
              G("Replying and correcting",
                "かくにんしました · おそれいりますが、ていせいが あります · ただしくは 〜です · いじょうです",
                "The reply confirms first (かくにんしました), the correction is introduced with "
                "おそれいりますが, the right figure is given with ただしくは, and the message closes "
                "with いじょうです. The correction is never left implicit.",
                [X("かくにんしました。", "Kakunin shimashita.", "I have confirmed it."),
                 X("おそれいりますが、ていせいが あります。", "Osoreirimasu ga, teisei ga arimasu.", "I am sorry to trouble you, but there is a correction."),
                 X("ただしくは ごひゃくえん です。", "Tadashiku wa gohyaku en desu.", "Correctly, it is five hundred yen.")],
                [("ていせい は ありません、たぶん。", "おそれいりますが、ていせいが あります。", "A correction is stated outright, with おそれいりますが."),
                 ("ただしい は ごひゃくえん。", "ただしくは ごひゃくえん です。", "ただしくは takes です to close.")]),
              [D("ゆき", "その ほうこく、かくにん して ください。", "Sono houkoku, kakunin shite kudasai.", "Please confirm that report."),
               D("たろう", "かくにんしました。おそれいりますが、ていせいが あります。", "Kakunin shimashita. Osoreirimasu ga, teisei ga arimasu.", "I have confirmed it. I am sorry to trouble you, but there is a correction."),
               D("ゆき", "どこですか。", "Doko desu ka.", "Where?"),
               D("たろう", "ひよう です。ただしくは ごひゃくえん です。いじょうです。", "Hiyou desu. Tadashiku wa gohyaku en desu. Ijou desu.", "The cost. Correctly, it is five hundred yen. That is all.")],
              WS("Reply worksheet", [
                  T("Confirm and correct.", ["I have confirmed it", "I am sorry to trouble you, but there is a correction"],
                    ["かくにんしました", "おそれいりますが、ていせいが あります"]),
                  T("State the right figure.", ["correctly, it is five hundred yen", "that is all"],
                    ["ただしくは ごひゃくえん です", "いじょうです"]),
              ])),
        ]},
        {"id": "B2+-U3", "title": "まとめて かくにんする", "lessons": [
            L("ようやくする",
              "A summary announces itself: ようするに、〜 (to sum up). まとめると counts first and "
              "then names the main point, and 〜の てんが ちゅうしん (the point at the centre) "
              "selects it.",
              [V("ようするに", "you suru ni", "in short, to sum up", "phrase"),
               V("まとめます", "matomemasu", "to summarise", "verb"),
               V("てん", "ten", "point, item", "noun"),
               V("ちゅうしん", "chuushin", "centre, main focus", "noun"),
               V("ぶんや", "bunya", "field, area", "noun")],
              G("Summarising",
                "ようするに、〜 · まとめると、 〜 · 〜の てんが ちゅうしんです · いっぽうで、〜",
                "The summary opens with its own marker (ようするに / まとめると), selects the main "
                "point with ちゅうしん, and balances it with いっぽうで. A summary that keeps "
                "everything has selected nothing.",
                [X("ようするに、ちょうさが たりません。", "You suru ni, chousa ga tarimasen.", "In short, the research is insufficient."),
                 X("まとめると、みっつ の てんが あります。", "Matomeru to, mittsu no ten ga arimasu.", "To sum up, there are three points."),
                 X("コストの てんが ちゅうしん です。", "Kosuto no ten ga chuushin desu.", "The point of cost is at the centre.")],
                [("ようするに、たくさん の てんが あります。", "ようするに、ちょうさが たりません。", "A summary selects one claim."),
                 ("まとめると みっつ です の てん。", "まとめると、みっつ の てんが あります。", "The count takes が あります.")]),
              [D("ぶちょう", "まとめて ください。", "Matomete kudasai.", "Please summarise it."),
               D("ゆき", "ようするに、ちょうさが たりません。", "You suru ni, chousa ga tarimasen.", "In short, the research is insufficient."),
               D("ぶちょう", "てんは いくつですか。", "Ten wa ikutsu desu ka.", "How many points are there?"),
               D("ゆき", "まとめると、みっつ です。コストの てんが ちゅうしん です。", "Matomeru to, mittsu desu. Kosuto no ten ga chuushin desu.", "To sum up, three. The point of cost is at the centre.")],
              WS("Summary worksheet", [
                  T("Sum it up.", ["in short, the research is insufficient", "to sum up, there are three points"],
                    ["ようするに、ちょうさが たりません", "まとめると、みっつ の てんが あります"]),
                  T("Select the centre.", ["the point of cost is at the centre", "how many points are there?"],
                    ["コストの てんが ちゅうしん です", "てんは いくつですか"]),
              ])),
            L("いいかえて たしかめる",
              "Rephrasing gives a second entrance to the same sentence: つまり (that is), いいかえると "
              "(put another way), つきつめると (pressed to the end). One marker per sentence.",
              [V("つまり", "tsumari", "that is, in other words", "conjunction"),
               V("いいかえると", "iikaeru to", "if we put it another way", "phrase"),
               V("つきつめます", "tsukitsumemasu", "to press to the end", "verb"),
               V("りかい", "rikai", "understanding", "noun"),
               V("たしかめます", "tashikamemasu", "to verify", "verb")],
              G("Rephrasing",
                "つまり、〜 · いいかえると、〜 · つきつめると、〜",
                "The marker opens the sentence and the content is the same claim in plainer words. "
                "Stacking two markers in one sentence turns the rephrase into noise.",
                [X("つまり、ことしは むずかしい という ことです。", "Tsumari, kotoshi wa muzukashii to iu koto desu.", "That is, it means this year is difficult."),
                 X("いいかえると、おかねが たりません。", "Iikaeru to, okane ga tarimasen.", "Put another way, the money is insufficient."),
                 X("つきつめると、けっていが おそい という ことです。", "Tsukitsumeru to, kettei ga osoi to iu koto desu.", "Pressed to the end, the decision is slow.")],
                [("つまり、いいかえると、おかねが たりません。", "いいかえると、おかねが たりません。", "One rephrase marker per sentence."),
                 ("つまり おかね が たりません です。", "つまり、おかねが たりません。", "ます ends the sentence; です does not follow.")]),
              [D("ゆき", "もういちど、やさしく せつめいして ください。", "Mou ichido, yasashiku setsumei shite kudasai.", "Please explain it once more, simply."),
               D("たろう", "いいかえると、おかねが たりません。", "Iikaeru to, okane ga tarimasen.", "Put another way, the money is insufficient."),
               D("ゆき", "つまり。", "Tsumari.", "That is."),
               D("たろう", "つきつめると、けっていが おそい という ことです。", "Tsukitsumeru to, kettei ga osoi to iu koto desu.", "Pressed to the end, the decision is slow.")],
              WS("Rephrase worksheet", [
                  T("Put it another way.", ["put another way, the money is insufficient", "pressed to the end, the decision is slow"],
                    ["いいかえると、おかねが たりません", "つきつめると、けっていが おそい という ことです"]),
                  T("Check it lands.", ["that is, it means this year is difficult", "please explain it once more, simply"],
                    ["つまり、ことしは むずかしい という ことです", "もういちど、やさしく せつめいして ください"]),
              ])),
            L("いじょうで かくにん",
              "A confirmation closes with いじょうです and an invitation to correct: ちがう てんが "
              "あれば、おしえて ください. いじょう covers both the above and the end of the message.",
              [V("いじょう", "ijou", "the above, that is all", "noun"),
               V("ちがう てん", "chigau ten", "a differing point", "phrase"),
               V("つうち", "tsuuchi", "notice, notification", "noun"),
               V("〜ば", "~ ba", "if (conditional)", "conjunction"),
               V("おしえます", "oshiemasu", "to inform, to tell", "verb")],
              G("Confirming",
                "いじょうです · ちがう てんが あれば、おしえて ください · 〜ば、すぐに なおします",
                "The message ends with いじょうです, and the reader is invited to correct it with "
                "〜ば あれば. This pattern makes a summary safe to send: it can be corrected before "
                "it becomes a record.",
                [X("いじょうです。", "Ijou desu.", "That is all."),
                 X("ちがう てんが あれば、おしえて ください。", "Chigau ten ga areba, oshiete kudasai.", "If there is anything different, please tell me."),
                 X("まちがいが あれば、すぐに なおします。", "Machigai ga areba, sugu ni naoshimasu.", "If there is a mistake, I will correct it at once.")],
                [("ちがう てん が ある なら ば、おしえて ください。", "ちがう てんが あれば、おしえて ください。", "The condition is あれば, one word."),
                 ("いじょう です か。", "いじょうです。", "The closing is a statement, not a question.")]),
              [D("たろう", "この メール、これで おくりますか。", "Kono meeru, kore de okurimasu ka.", "Shall I send this email as it is?"),
               D("ゆき", "はい。いじょうです。", "Hai. Ijou desu.", "Yes. That is all."),
               D("たろう", "かくにんは。", "Kakunin wa.", "And confirmation?"),
               D("ゆき", "ちがう てんが あれば、おしえて ください。すぐに なおします。", "Chigau ten ga areba, oshiete kudasai. Sugu ni naoshimasu.", "If there is anything different, please tell me. I will correct it at once.")],
              WS("Confirmation worksheet", [
                  T("Close the message.", ["that is all", "if there is anything different, please tell me"],
                    ["いじょうです", "ちがう てんが あれば、おしえて ください"]),
                  T("Offer the correction.", ["if there is a mistake, I will correct it at once", "shall I send this email as it is?"],
                    ["まちがいが あれば、すぐに なおします", "この メール、これで おくりますか"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Japanese technical writing separates what was measured from what may be claimed, "
                 "and the grammar does the separating: ちょうさに よると for the source, と いえます "
                 "for what is supported, とは いえません for what is not, and べきです for the "
                 "recommendation. A report that skips the middle step reads as a sales pitch; the "
                 "missing とは いえません is the first thing an editor asks for."),
        source_url="https://en.wikipedia.org/wiki/Technical_writing",
        reading=("ちょうさに よると、ひゃくにんの なかで はんぶんが この アプリを つかって います。"
                 "きょねんと くらべると にわり ふえましたが、たいしょうは にじゅうだい だけです。"
                 "したがって、わかい そうに かんれんが ある と いえますが、げんいん とは いえません。"
                 "いじょうです。ちがう てんが あれば、おしえて ください。"),
        reading_gloss=("According to the survey, half of a hundred people use this app. Compared "
                       "with last year it rose by twenty per cent, but the subjects are only people "
                       "in their twenties. Therefore one can say there is a correlation with the "
                       "younger layer, but one cannot say it is the cause. That is all. If there is "
                       "anything different, please tell me."),
        listening=("ぶちょう: けつろんは。<br>"
                   "たろう: かんれんが ある と いえます。げんいん とは いえません。<br>"
                   "ぶちょう: つぎは。<br>"
                   "たろう: データを ふやす べきです。いかがでしょうか。"),
        listening_gloss=("Manager: And the conclusion? Taro: One can say there is a correlation. "
                         "One cannot say it is the cause. Manager: Next? Taro: We should increase "
                         "the data. How does that sound?"),
        voice_tag=VOICE,
        idioms=[
            ("ちょうさに よると", "chousa ni yoru to", "according to the survey"),
            ("くらべると", "kuraberu to", "compared with"),
            ("と いえます", "to iemasu", "one can say that"),
            ("とは いえません", "to wa iemasen", "one cannot say that"),
            ("を ふまえて", "o fumaete", "in light of"),
            ("いかがでしょうか", "ikaga deshou ka", "how does that sound?"),
            ("ただしくは", "tadashiku wa", "correctly, the correct figure is"),
            ("ようするに", "you suru ni", "in short"),
            ("いいかえると", "iikaeru to", "put another way"),
            ("いじょうです", "ijou desu", "that is all"),
        ],
        mistakes=[
            ("げんいん を いえます。", "かんれん を いえます。", "Two series moving together gives correlation, not cause."),
            ("つまり、いいかえると、おかねが たりません。", "いいかえると、おかねが たりません。", "One rephrase marker per sentence."),
            ("ちがう てん が ある なら ば、おしえて ください。", "ちがう てんが あれば、おしえて ください。", "The condition is あれば."),
        ],
        task_title="Turn one report page into six lines and a confirmation",
        task_instructions=("Take a report or dashboard you have read this month and write six lines "
                           "in Japanese: the source with ちょうさに よると, the movement with "
                           "くらべると, what can be claimed with と いえます, what cannot with とは "
                           "いえません, the recommendation with べきです, and the closing with "
                           "いじょうです plus the invitation to correct. Then write the same content "
                           "as one spoken sentence with ようするに and notice which of the six lines "
                           "disappeared — that one is the line that was doing the careful work."),
    ),
    "test": [
        ("translate_en", "Say: One can say there is a correlation.", "かんれんが ある と いえます。"),
        ("translate_ja", "げんいん とは いえません。", "One cannot say it is the cause."),
        ("multiple_choice", "Which line asks for a decision on a proposal?", "いかがでしょうか。"),
        ("fill_in_the_blank", "ちょうさ___ よると、はんぶんが つかって います。", "に"),
        ("word_selection", "Select the Japanese for 'in light of the earlier result'.", "いぜんの けっか を ふまえて"),
        ("error_correction", "つまり、いいかえると、おかねが たりません。", "いいかえると、おかねが たりません。"),
        ("dialogue_completion", "Complete: ひようは。 — ___ (correctly, it is five hundred yen)", "ただしくは ごひゃくえん です"),
        ("matching", "Match いじょうです to its meaning.", "that is all"),
        ("reading_comprehension", "きょねんと くらべると にわり ふえました。 How much did it rise?", "twenty per cent"),
        ("inference", "「たしかに いい てんも ありますが…」 — what is coming next?", "a reservation"),
        ("main_idea", "かんれんが ある と いえます。げんいん とは いえません。 What is this?", "the conclusion of a report"),
        ("detail_identification", "たいしょうは にじゅうだい だけです。 Who were the subjects?", "only people in their twenties"),
    ],
}

HALFSTEPS["C1+"] = {
    "title": "Japanese C1+ — Precision, register and mediation",
    "native": NATIVE,
    "goals": [
        "Say exactly how certain you are and what would change your mind",
        "Move one text up and down the register scale",
        "Mediate a Japanese source for readers who do not share its register",
    ],
    "units": [
        {"id": "C1+-U1", "title": "せいど", "lessons": [
            L("たしかさの だんかい",
              "Certainty is graded in four steps: かならず (certain), おそらく … でしょう "
              "(probable), ありえます (possible), ありえません (out of the question). The step "
              "chosen is a claim about the evidence, not about your mood.",
              [V("かならず", "kanarazu", "certainly, without fail", "adverb"),
               V("おそらく", "osoraku", "probably", "adverb"),
               V("ありえます", "ariemasu", "is possible", "verb"),
               V("ありえません", "ariemasen", "is impossible", "verb"),
               V("みこみ", "mikomi", "outlook, prospect", "noun")],
              G("Levels of certainty",
                "かならず 〜ます · おそらく 〜でしょう · ありえます · ありえません",
                "かならず takes a plain affirmative, おそらく pairs with でしょう, and possibility "
                "is a verb: ありえます / ありえません. Writing たぶん with でしょう is weaker than "
                "おそらく and belongs in speech rather than in a report.",
                [X("かならず あした とどきます。", "Kanarazu ashita todokimasu.", "It will certainly arrive tomorrow."),
                 X("おそらく みこみは たつ でしょう。", "Osoraku mikomi wa tatsu deshou.", "The outlook will probably hold."),
                 X("その かのうせいも ありえます。", "Sono kanousei mo ariemasu.", "That possibility is also open.")],
                [("おそらく です でしょう か。", "おそらく 〜でしょう。", "おそらく takes でしょう and closes the sentence."),
                 ("ありえません と おもいます でしょう。", "ありえません。", "One certainty marker per sentence.")]),
              [D("査読者", "どのくらい たしかですか。", "Dono kurai tashika desu ka.", "How certain are you?"),
               D("分析者", "おそらく みこみは たつ でしょう。かならず とは いえません。", "Osoraku mikomi wa tatsu deshou. Kanarazu to wa iemasen.", "The outlook will probably hold. I cannot say it certainly."),
               D("査読者", "ほかの かのうせいは。", "Hoka no kanousei wa.", "And other possibilities?"),
               D("分析者", "その かのうせいも ありえます。", "Sono kanousei mo ariemasu.", "That possibility is also open.")],
              WS("Certainty worksheet", [
                  T("Grade the claim.", ["it will certainly arrive tomorrow", "the outlook will probably hold"],
                    ["かならず あした とどきます", "おそらく みこみは たつ でしょう"]),
                  T("Leave the door open.", ["that possibility is also open", "how certain are you?"],
                    ["その かのうせいも ありえます", "どのくらい たしかですか"]),
              ])),
            L("こんきょと すいろん",
              "Evidence and inference are kept in separate sentences: 〜から わかります (can be known "
              "from) and 〜に すぎません (no more than). と おもわれます marks what the field "
              "believes rather than what you do.",
              [V("こんきょ", "konkyo", "evidence, grounds", "noun"),
               V("すいろん", "suiron", "inference", "noun"),
               V("わかります", "wakarimasu", "to be known, to be understood", "verb"),
               V("〜に すぎません", "~ ni sugimasen", "is no more than", "phrase"),
               V("おもわれます", "omowaremasu", "it is thought (passive)", "verb")],
              G("Evidence and inference",
                "〜から わかります · 〜に すぎません · 〜と おもわれます · すいろんは べつです",
                "The evidence sentence names the material and から わかります; the inference takes "
                "と おもわれます or に すぎません. Mixing the two in one sentence is the failure "
                "the register exists to prevent.",
                [X("この すうじ から わかる ことは ひとつ だけです。", "Kono suuji kara wakaru koto wa hitotsu dake desu.", "Only one thing can be known from this figure."),
                 X("それは すいろん に すぎません。", "Sore wa suiron ni sugimasen.", "That is no more than an inference."),
                 X("いまは そう おもわれて います。", "Ima wa sou omowarete imasu.", "That is how it is currently thought.")],
                [("この すうじ は げんいん が わかります。", "この すうじ から わかる ことは かぎられて います。", "A figure supports a limited reading, not a cause."),
                 ("すいろん は こんきょ です。", "すいろんと こんきょ は べつです。", "The two are stated separately.")]),
              [D("編集者", "それは こんきょですか、すいろんですか。", "Sore wa konkyo desu ka, suiron desu ka.", "Is that evidence or inference?"),
               D("分析者", "すいろん に すぎません。", "Suiron ni sugimasen.", "It is no more than an inference."),
               D("編集者", "こんきょは。", "Konkyo wa.", "And the evidence?"),
               D("分析者", "この すうじ から わかる ことは ひとつ だけです。", "Kono suuji kara wakaru koto wa hitotsu dake desu.", "Only one thing can be known from this figure.")],
              WS("Evidence worksheet", [
                  T("Separate the two.", ["that is no more than an inference", "only one thing can be known from this figure"],
                    ["それは すいろん に すぎません", "この すうじ から わかる ことは ひとつ だけです"]),
                  T("Report the field.", ["that is how it is currently thought", "is that evidence or inference?"],
                    ["いまは そう おもわれて います", "それは こんきょですか、すいろんですか"]),
              ])),
            L("はんいを きめる",
              "A claim is fenced before it is made: 〜に かぎり (as far as ~ is concerned), 〜を "
              "のぞいて (excluding), 〜の ばあい (in the case of). The fence is part of the claim, "
              "not a footnote.",
              [V("はんい", "han'i", "range, scope", "noun"),
               V("かぎり", "kagiri", "as far as, limited to", "noun"),
               V("のぞいて", "nozoite", "excluding", "phrase"),
               V("てきよう", "tekiyou", "application, scope", "noun"),
               V("げんてい", "gentei", "limit, restriction", "noun")],
              G("Fencing a claim",
                "〜に かぎり · 〜を のぞいて · 〜の ばあいに かぎられます · はんいを かきます",
                "に かぎり is followed by the claim; を のぞいて removes a group; に かぎられます "
                "marks where the finding does apply. A claim with no fence claims the whole world.",
                [X("この データに かぎり、けいこうは つづいて います。", "Kono deeta ni kagiri, keikou wa tsuzuite imasu.", "As far as this data goes, the trend continues."),
                 X("にじゅうだい を のぞいて、はんぶん です。", "Nijuudai o nozoite, hanbun desu.", "Excluding people in their twenties, it is half."),
                 X("この ばあいに かぎられます。", "Kono baai ni kagiraremasu.", "It applies to this case only.")],
                [("この データ は かぎり、けいこう。", "この データに かぎり、けいこうは つづいて います。", "The fence takes に かぎり and a full clause."),
                 ("にじゅうだい の のぞき、はんぶん です。", "にじゅうだい を のぞいて、はんぶん です。", "Exclusion takes を のぞいて.")]),
              [D("査読者", "この けつろん、はんいが ひろすぎます。", "Kono ketsuron, han'i ga hirosugimasu.", "The scope of this conclusion is too wide."),
               D("分析者", "この データに かぎります。", "Kono deeta ni kagirimasu.", "I will limit it to this data."),
               D("査読者", "ほかの たいしょうは。", "Hoka no taishou wa.", "And other groups?"),
               D("分析者", "にじゅうだい を のぞいて、はんぶん です。", "Nijuudai o nozoite, hanbun desu.", "Excluding people in their twenties, it is half.")],
              WS("Scope worksheet", [
                  T("Fence the claim.", ["as far as this data goes, the trend continues", "excluding people in their twenties, it is half"],
                    ["この データに かぎり、けいこうは つづいて います", "にじゅうだい を のぞいて、はんぶん です"]),
                  T("Limit the application.", ["it applies to this case only", "the scope of this conclusion is too wide"],
                    ["この ばあいに かぎられます", "この けつろん、はんいが ひろすぎます"]),
              ])),
        ]},
        {"id": "C1+-U2", "title": "レジスター", "lessons": [
            L("です・ます と である",
              "The same page can be written in です・ます or in である, and the choice is announced "
              "by the whole document: である for reports and papers, です・ます for letters and "
              "notices, mixed only where a quotation begins.",
              [V("レジスター", "regisutaa", "register", "noun"),
               V("である", "de aru", "is (written plain style)", "phrase"),
               V("です・ます", "desu masu", "polite style", "phrase"),
               V("とういつ", "touitsu", "unification, consistency", "noun"),
               V("いいかえます", "iikaemasu", "to rephrase", "verb")],
              G("Choosing a register",
                "〜である (report) · 〜です (notice) · レジスターを とういつします",
                "The register is chosen once and kept for the whole text; a switch mid-paragraph "
                "reads as an accident. The same sentence can be rephrased across registers without "
                "changing its content.",
                [X("この けっかは ちょうさ に よる ものである。", "Kono kekka wa chousa ni yoru mono de aru.", "This result is based on a survey."),
                 X("この けっかは ちょうさに よる ものです。", "Kono kekka wa chousa ni yoru mono desu.", "This result is based on a survey (polite)."),
                 X("レジスターを とういつします。", "Regisutaa o touitsu shimasu.", "I will unify the register.")],
                [("この けっか は ちょうさ に よる です である。", "この けっかは ちょうさに よる ものである。", "One register per sentence."),
                 ("レジスター は かえます と ちゅう で。", "レジスターは ぶんしょう の なかで かえません。", "The register is fixed for the whole text.")]),
              [D("編集者", "レジスターが まざって います。", "Regisutaa ga mazatte imasu.", "The registers are mixed."),
               D("分析者", "この ほうこくは である で とういつします。", "Kono houkoku wa de aru de touitsu shimasu.", "I will unify this report in である style."),
               D("編集者", "おしらせは。", "Oshirase wa.", "And the notice?"),
               D("分析者", "おしらせは です・ます です。", "Oshirase wa desu masu desu.", "The notice is in です・ます.")],
              WS("Register worksheet", [
                  T("Pick the register.", ["this result is based on a survey (report style)", "this result is based on a survey (polite)"],
                    ["この けっかは ちょうさ に よる ものである", "この けっかは ちょうさに よる ものです"]),
                  T("Keep it consistent.", ["I will unify the register", "the registers are mixed"],
                    ["レジスターを とういつします", "レジスターが まざって います"]),
              ])),
            L("けいごの えらび",
              "Keigo is a choice about whose action it is: いらっしゃる (they come), うかがう (I "
              "go), いただく (I receive), さしあげる (I give). Choosing the wrong direction sounds "
              "worse than using no keigo at all.",
              [V("うかがいます", "ukagaimasu", "to visit, to ask (humble)", "verb"),
               V("いただきます", "itadakimasu", "to receive (humble)", "verb"),
               V("さしあげます", "sashiagemasu", "to give (humble)", "verb"),
               V("ごらんに なります", "goran ni narimasu", "to see (respectful)", "phrase"),
               V("ほうもん", "houmon", "visit", "noun")],
              G("Choosing keigo",
                "いらっしゃる (their action, respectful) · うかがう (my action, humble) · いただく (my receiving) · さしあげる (my giving)",
                "Respectful forms raise the other person's action; humble forms lower my own. A "
                "humble verb on the other person's act is the error that marks a learner, so the "
                "test is always: whose action is it?",
                [X("あした うちに うかがいます。", "Ashita uchi ni ukagaimasu.", "I will visit you tomorrow."),
                 X("せんせいは もう ごらんに なりました。", "Sensei wa mou goran ni narimashita.", "The teacher has already seen it."),
                 X("おみやげを いただきました。", "Omiyage o itadakimashita.", "I received a gift.")],
                [("わたし が いらっしゃいます。", "わたしが うかがいます。", "My own action takes the humble form うかがう."),
                 ("せんせい に さしあげて いただきました。", "せんせいに おみやげを いただきました。", "Receiving takes いただく; さしあげる is giving.")]),
              [D("調停者", "あした ほうもん しますか。", "Ashita houmon shimasu ka.", "Will you visit tomorrow?"),
               D("分析者", "はい、あした うかがいます。", "Hai, ashita ukagaimasu.", "Yes, I will visit tomorrow."),
               D("調停者", "その しりょうは みましたか。", "Sono shiryou wa mimashita ka.", "Have you seen those materials?"),
               D("分析者", "せんせいは もう ごらんに なりました。わたしは あとで いただきます。", "Sensei wa mou goran ni narimashita. Watashi wa ato de itadakimasu.", "The teacher has already seen them. I will receive them later.")],
              WS("Keigo worksheet", [
                  T("Lower your own action.", ["I will visit you tomorrow", "I received a gift"],
                    ["あした うちに うかがいます", "おみやげを いただきました"]),
                  T("Raise theirs.", ["the teacher has already seen it", "will you visit tomorrow?"],
                    ["せんせいは もう ごらんに なりました", "あした ほうもん しますか"]),
              ])),
            L("くだけた はなし",
              "Casual Japanese is a register, not a mistake: じゃ、だ、〜かな、〜だよ belong between "
              "people who know each other. The C1 skill is switching deliberately and never mixing "
              "the two inside one sentence.",
              [V("くだけた", "kudaketa", "casual, informal", "adjective"),
               V("〜だよ", "~ da yo", "it is (casual, informing)", "phrase"),
               V("〜かな", "~ kana", "I wonder (casual)", "phrase"),
               V("きんちょう", "kinchou", "tension, nervousness", "noun"),
               V("ばめん", "bamen", "scene, situation", "noun")],
              G("Switching registers",
                "じゃ、また · そうだよ · どう かな · 〜かも しれないな",
                "The casual register drops です・ます, contracts では to じゃ, and adds よ/ね/な for "
                "the listener. Switching is announced by the whole sentence — half-casual sounds "
                "worse than either register alone.",
                [X("じゃ、また あしたね。", "Ja, mata ashita ne.", "See you tomorrow, then."),
                 X("そうだよ。たぶん だいじょうぶ。", "Sou da yo. Tabun daijoubu.", "That is right. It is probably fine."),
                 X("どう かな。ちょっと わからないな。", "Dou kana. Chotto wakaranai na.", "I wonder. I am not sure.")],
                [("じゃ、また あした ですね だよ。", "じゃ、また あしたね。", "One register per sentence."),
                 ("そう です よ だ。", "そうだよ。", "The casual ending replaces です, it does not join it.")]),
              [D("分析者", "じゃ、また あしたね。", "Ja, mata ashita ne.", "See you tomorrow, then."),
               D("査読者", "うん。あしたの しりょう、だいじょうぶ?", "Un. Ashita no shiryou, daijoubu?", "Yes. Are the materials for tomorrow all right?"),
               D("分析者", "たぶん。ちょっと わからないな。", "Tabun. Chotto wakaranai na.", "Probably. I am not quite sure."),
               D("査読者", "じゃ、あとで メール して。", "Ja, ato de meeru shite.", "Then mail me later.")],
              WS("Casual worksheet", [
                  T("Say it casually.", ["see you tomorrow, then", "that is right. It is probably fine."],
                    ["じゃ、また あしたね", "そうだよ。たぶん だいじょうぶ。"]),
                  T("Leave it open.", ["I wonder. I am not sure.", "then mail me later"],
                    ["どう かな。ちょっと わからないな", "じゃ、あとで メール して"]),
              ])),
        ]},
        {"id": "C1+-U3", "title": "ちゅうかい", "lessons": [
            L("やさしい にほんごで つたえる",
              "Mediation starts by announcing the register: やさしい にほんごで おつたえします. "
              "Sentences shorten to one clause, kanji gain furigana, and every turn of phrase is "
              "marked with いいかえると.",
              [V("おつたえします", "otsutae shimasu", "I convey (humble)", "verb"),
               V("ふりがな", "furigana", "reading gloss", "noun"),
               V("ぶんせつ", "bunsetsu", "clause, phrase", "noun"),
               V("みじかく", "mijikaku", "shortly, briefly", "adverb"),
               V("いいかえます", "iikaemasu", "to rephrase", "verb")],
              G("Plain-language mediation",
                "やさしい にほんごで おつたえします · ぶんせつを みじかく します · いいかえると、〜",
                "The rendering is announced, the clauses shorten to one idea each, and each "
                "rephrase is marked. Naming the change is what makes a plain rendering a service "
                "rather than a simplification of the reader.",
                [X("やさしい にほんごで おつたえします。", "Yasashii nihongo de otsutae shimasu.", "I will convey it in plain Japanese."),
                 X("ぶんせつを みじかく します。", "Bunsetsu o mijikaku shimasu.", "I will shorten the clauses."),
                 X("いいかえると、あしたまで です。", "Iikaeru to, ashita made desu.", "In other words, it is until tomorrow.")],
                [("やさしい にほんご を おつたえ します です。", "やさしい にほんごで おつたえします。", "One ending per sentence."),
                 ("ぶんせつ は みじかく です。", "ぶんせつを みじかく します。", "The change is a verb: みじかく します.")]),
              [D("調停者", "この おしらせ、むずかしいですか。", "Kono oshirase, muzukashii desu ka.", "Is this notice difficult?"),
               D("分析者", "はい。やさしい にほんごで おつたえします。", "Hai. Yasashii nihongo de otsutae shimasu.", "Yes. I will convey it in plain Japanese."),
               D("調停者", "どう しますか。", "Dou shimasu ka.", "How will you do it?"),
               D("分析者", "ぶんせつを みじかく して、いいかえると を つけます。", "Bunsetsu o mijikaku shite, iikaeru to o tsukemasu.", "I will shorten the clauses and add 'in other words'.")],
              WS("Plain language worksheet", [
                  T("Announce the rendering.", ["I will convey it in plain Japanese", "I will shorten the clauses"],
                    ["やさしい にほんごで おつたえします", "ぶんせつを みじかく します"]),
                  T("Mark the rephrase.", ["in other words, it is until tomorrow", "is this notice difficult?"],
                    ["いいかえると、あしたまで です", "この おしらせ、むずかしいですか"]),
              ])),
            L("ことばを のこして ちゅうしゃくする",
              "When a word will not travel, it stays and takes a gloss: そのまま のこします、"
              "かっこに ちゅうしゃくを つけます. The gloss is written for a reader who will meet "
              "the word again.",
              [V("ちゅうしゃく", "chuushaku", "gloss, annotation", "noun"),
               V("そのまま", "sonomama", "as it is", "adverb"),
               V("のこします", "nokoshimasu", "to leave (as is)", "verb"),
               V("やくご", "yakugo", "translated term", "noun"),
               V("せつめい", "setsumei", "explanation", "noun")],
              G("Keeping a word",
                "そのまま のこします · かっこに ちゅうしゃくを つけます · やくごは つくりません",
                "The word is kept in the original, the gloss goes in brackets, and no translated "
                "term is coined — coining is how a concept arrives in another language already "
                "distorted. The gloss explains, it does not replace.",
                [X("この ことばは そのまま のこします。", "Kono kotoba wa sonomama nokoshimasu.", "I will leave this word as it is."),
                 X("かっこに ちゅうしゃくを つけます。", "Kakko ni chuushaku o tsukemasu.", "I will attach a gloss in brackets."),
                 X("やくごは つくりません。", "Yakugo wa tsukurimasen.", "I will not coin a translated term.")],
                [("やくご を つくって、ことば を けします。", "そのまま のこして、ちゅうしゃくを つけます。", "Keep the word and gloss it; do not replace it."),
                 ("ちゅうしゃく は ことば を かえます。", "ちゅうしゃくは ことばを せつめい します。", "A gloss explains; it does not substitute.")]),
              [D("査読者", "その ことば、どう しますか。", "Sono kotoba, dou shimasu ka.", "What will you do with that word?"),
               D("調停者", "そのまま のこして、かっこに ちゅうしゃくを つけます。", "Sonomama nokoshite, kakko ni chuushaku o tsukemasu.", "Leave it as it is and attach a gloss in brackets."),
               D("査読者", "やくごは。", "Yakugo wa.", "And a translated term?"),
               D("調停者", "つくりません。せつめい だけ です。", "Tsukurimasen. Setsumei dake desu.", "I will not coin one. Explanation only.")],
              WS("Gloss worksheet", [
                  T("Keep the word.", ["I will leave this word as it is", "I will attach a gloss in brackets"],
                    ["この ことばは そのまま のこします", "かっこに ちゅうしゃくを つけます"]),
                  T("Refuse the coinage.", ["I will not coin a translated term", "and a translated term?"],
                    ["やくごは つくりません", "やくごは"]),
              ])),
            L("やくしゃの ちゅうい",
              "The translator's note records what the rendering lost: やくしゃの ちゅうい として、"
              "〜が おちて います. おちます (to drop out) names the loss without complaining about it.",
              [V("やくしゃ", "yakusha", "translator", "noun"),
               V("ちゅうい", "chuui", "note, caution", "noun"),
               V("おちます", "ochimasu", "to drop out, to be lost", "verb"),
               V("おぎなう", "oginau", "to supplement, to make up for", "verb"),
               V("ものたりなさ", "monotarinasa", "the sense of falling short", "noun")],
              G("Translator's note",
                "やくしゃの ちゅうい として、〜が おちて います · それは おぎなえません · ものたりなさ を かきます",
                "The note names the loss (〜が おちて います), states honestly that it cannot be "
                "made up (おぎなえません), and records the shortfall in ものたりなさ. Naming what a "
                "rendering loses is what keeps the original available to the reader.",
                [X("やくしゃの ちゅうい として、ていねいさが おちて います。", "Yakusha no chuui to shite, teineisa ga ochite imasu.", "As a translator's note, the politeness is lost."),
                 X("それは おぎなえません。", "Sore wa oginaemasen.", "That cannot be made up for."),
                 X("ものたりなさを かきます。", "Monotarinasa o kakimasu.", "I will write the shortfall.")],
                [("やくしゃ の ちゅうい は いいわけ です。", "やくしゃの ちゅうい として、〜が おちて います。", "A note names the loss; it is not an excuse."),
                 ("おちて います です。", "おちて います。", "います ends the sentence; です does not follow.")]),
              [D("調停者", "ちゅういを つけますか。", "Chuui o tsukemasu ka.", "Will you add a note?"),
               D("査読者", "はい。やくしゃの ちゅうい として、ていねいさが おちて います。", "Hai. Yakusha no chuui to shite, teineisa ga ochite imasu.", "Yes. As a translator's note, the politeness is lost."),
               D("調停者", "おぎなえますか。", "Oginaemasu ka.", "Can it be made up for?"),
               D("査読者", "いいえ、おぎなえません。ものたりなさを かきます。", "Iie, oginaemasen. Monotarinasa o kakimasu.", "No, it cannot. I will write the shortfall.")],
              WS("Translator's note worksheet", [
                  T("Name the loss.", ["as a translator's note, the politeness is lost", "that cannot be made up for"],
                    ["やくしゃの ちゅうい として、ていねいさが おちて います", "それは おぎなえません"]),
                  T("Record the shortfall.", ["I will write the shortfall", "will you add a note?"],
                    ["ものたりなさを かきます", "ちゅういを つけますか"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Mediation in Japanese runs through やさしい日本語, a public-service register with "
                 "its own rules — one instruction per line, furigana, no double negatives — and "
                 "through やくしゃの ちゅうい, the translator's note that records what a rendering "
                 "loses. Both exist because Japanese carries politeness inside the sentence: a "
                 "notice translated into plain language loses the keigo that made it polite, and "
                 "the honest move is to write that loss down rather than pretend the two texts are "
                 "the same."),
        source_url="https://en.wikipedia.org/wiki/Plain_language",
        reading=("この おしらせは やさしい にほんごで おつたえします。いいかえると、あした の "
                 "ごご までに もうしこんで ください、という いみです。ただし、やくしゃの ちゅうい "
                 "として、ていねいさが おちて います。おぎなえませんから、ものたりなさ を "
                 "かきます。この ことばは そのまま のこします。"),
        reading_gloss=("I will convey this notice in plain Japanese. In other words, it means: please "
                       "apply by tomorrow afternoon. However, as a translator's note, the "
                       "politeness is lost. Since it cannot be made up for, I will write the "
                       "shortfall. This word I leave as it is."),
        listening=("調停者: やさしい にほんごで おつたえしますか。<br>"
                   "分析者: はい。ぶんせつを みじかく して、ふりがなを つけます。<br>"
                   "調停者: ことばは。<br>"
                   "分析者: そのまま のこして、かっこに ちゅうしゃくを つけます。"),
        listening_gloss=("Mediator: Will you convey it in plain Japanese? Analyst: Yes. I will "
                         "shorten the clauses and add furigana. Mediator: And the words? Analyst: I "
                         "will leave them as they are and attach a gloss in brackets."),
        voice_tag=VOICE,
        idioms=[
            ("おそらく", "osoraku", "probably"),
            ("ありえます", "ariemasu", "is possible"),
            ("こんきょ", "konkyo", "evidence"),
            ("すいろん に すぎません", "suiron ni sugimasen", "no more than an inference"),
            ("に かぎり", "ni kagiri", "as far as … is concerned"),
            ("を のぞいて", "o nozoite", "excluding"),
            ("うかがいます", "ukagaimasu", "I will visit (humble)"),
            ("そのまま のこす", "sonomama nokosu", "to leave as it is"),
            ("やくしゃの ちゅうい", "yakusha no chuui", "translator's note"),
            ("おぎなえません", "oginaemasen", "cannot be made up for"),
        ],
        mistakes=[
            ("わたし が いらっしゃいます。", "わたしが うかがいます。", "My own action takes the humble form."),
            ("すいろん は こんきょ です。", "すいろんと こんきょ は べつです。", "Evidence and inference are stated separately."),
            ("この データ は かぎり、けいこう。", "この データに かぎり、けいこうは つづいて います。", "The fence takes に かぎり and a full clause."),
        ],
        task_title="Mediate one Japanese source for two different readers",
        task_instructions=("Take any Japanese text of a few hundred characters — a notice, a report, "
                           "a news item. Produce three outputs: (1) a plain-Japanese rendering "
                           "announced with やさしい にほんごで おつたえします, shortened to one "
                           "clause per line with furigana on the harder kanji; (2) the same content "
                           "in である for a report; (3) a spoken version to a colleague with ようするに "
                           "and one next step. Keep one key term from the original in each version, "
                           "and finish with a やくしゃの ちゅうい that records what each rendering "
                           "dropped. If any version sounds more certain than the source, lower "
                           "it."),
    ),
    "test": [
        ("translate_en", "Say: That is no more than an inference.", "それは すいろん に すぎません。"),
        ("translate_ja", "この データに かぎり、けいこうは つづいて います。", "As far as this data goes, the trend continues."),
        ("multiple_choice", "Which sentence uses humble keigo for the speaker's own action?", "あした うちに うかがいます。"),
        ("fill_in_the_blank", "にじゅうだい___ のぞいて、はんぶん です。", "を"),
        ("word_selection", "Select the Japanese for 'as it is, without changing it'.", "そのまま"),
        ("error_correction", "わたし が いらっしゃいます。", "わたしが うかがいます。"),
        ("dialogue_completion", "Complete: その ことば、どう しますか。 — ___ (leave it as it is and attach a gloss)", "そのまま のこして、かっこに ちゅうしゃくを つけます"),
        ("matching", "Match やくしゃの ちゅうい to its meaning.", "a translator's note"),
        ("reading_comprehension", "あしたの ごご までに もうしこんで ください。 By when is the application due?", "by tomorrow afternoon"),
        ("inference", "「おぎなえませんから、ものたりなさを かきます。」 — what is the writer doing?", "recording what the rendering lost"),
        ("main_idea", "やさしい にほんごで おつたえします。ぶんせつを みじかく します。 What is this?", "a plain-language mediation"),
        ("detail_identification", "おそらく みこみは たつ でしょう。 How certain is the speaker?", "probable, not certain"),
    ],
}

# -*- coding: utf-8 -*-
"""Korean PHASE 1 depth — extras, third lessons, half-step rungs.

Written with the DSL in `tools/depth_kit.py`; rendered by
`tools/author-depth.py --lang ko`.

House style follows the shipped Korean course: Hangul in `t`, revised
romanisation in `r` with hyphens at morpheme boundaries
(`annyeong-haseyo`, `jeo-neun mina-imnida`), English in `en`. Unit ids keep the
shipped course's scheme (`A1-U1` for the CEFR rungs, `ko-c1-u1` for C1/C2);
half-step rungs use `<rung>-U1`.

Register note: A1-A2 stay in the polite -아요/어요 and -입니다 forms the shipped
course teaches; B1 introduces -지 않다/-지 못하다 and the honorific -(으)시-, and
B2-C2 use the written 보도체 and formal -습니다 register deliberately, never
mixed into a plain conversation. The voice tag is the canonical `ko-KR`
(`tools/lib/speech_tags.py`, mirrored in `js/voice-languages.js`).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # tools/ on the path
from depth_kit import D, EXTRA, G, L, T, V, WS, X   # noqa: E402

CODE = "ko"
NAME = "Korean"
NATIVE = "한국어"
PHASE = 1
SCRIPT = "Hangul"
VOICE = "ko-KR"
SKILL = ("Korean: Hangul, particle system 은/는·이/가·을/를·에/에서, speech levels "
         "해요체 and 합니다체, honorific -(으)시- and 드리다, agglutinative verb endings, "
         "counters and 사자성어")

EXTRAS = {}
THIRD = {}
HALFSTEPS = {}

EXTRAS["A1"] = EXTRA(
    culture=("Hangul 한글 is the only widely used writing system with a recorded birthday: King "
             "Sejong promulgated it in 1443, and its 14 consonants and 10 vowels are drawn to "
             "match the shape of the mouth that makes them. Because it is that regular, a learner "
             "can read Korean aloud in an afternoon. Politeness is built into the grammar, not "
             "just the tone: 안녕하세요 means be at peace, and 저는 …입니다 states who you are "
             "without ever saying I am as a separate verb."),
    source_url="https://en.wikipedia.org/wiki/Korean_language",
    reading=("저는 미나입니다. 서울에 삽니다. 아침에 커피를 마시고 학교에 갑니다. "
             "한국어를 공부합니다. 선생님은 친절합니다. 오후에는 친구를 만납니다. "
             "친구는 학생입니다. 우리는 같이 밥을 먹습니다. 저녁에는 집에서 쉽니다. "
             "주말에는 친구와 시장에 갑니다. 과일과 빵을 삽니다. 그리고 커피를 마시면서 "
             "이야기를 합니다. 밤에는 한국 드라마를 보고 일기를 씁니다. 조금 힘들지만 "
             "재미있습니다."),
    reading_gloss=("I am Mina. I live in Seoul. In the morning I drink coffee and go to school. "
                   "I study Korean. The teacher is kind. In the afternoon I meet a friend. My "
                   "friend is a student. We eat together. In the evening I rest at home. At the "
                   "weekend I go to the market with a friend. We buy fruit and bread. And we drink "
                   "coffee and talk. At night I watch Korean dramas and write a diary. It is a "
                   "little hard, but it is fun."),
    listening=("미나: 안녕하세요.<br>지훈: 안녕하세요. 처음 뵙겠습니다. 저는 지훈입니다.<br>"
               "미나: 반갑습니다. 저는 미나입니다.<br>지훈: 미나 씨, 한국어를 공부하십니까?<br>"
               "미나: 네, 조금 공부합니다. 잘 부탁드립니다."),
    listening_gloss=("Mina: Hello. Jihun: Hello. How do you do, I am Jihun. Mina: Nice to meet "
                     "you, I am Mina. Jihun: Mina, do you study Korean? Mina: Yes, a little. "
                     "Please treat me well."),
    voice_tag=VOICE,
    idioms=[
        ("안녕하세요", "be at peace (question form)", "hello"),
        ("반갑습니다", "I am glad to see you", "nice to meet you"),
        ("잘 부탁드립니다", "I ask you to treat me well", "please look after me / I look forward to it"),
        ("죄송합니다", "I feel sorry", "I am sorry (formal)"),
        ("실례합니다", "I commit a discourtesy", "excuse me (passing, interrupting)"),
        ("감사합니다", "I am grateful", "thank you (formal)"),
        ("잘 먹겠습니다", "I will eat well", "said before a meal"),
        ("잘 먹었습니다", "I ate well", "said after a meal"),
        ("다녀오겠습니다", "I will go and return", "said when leaving the house"),
        ("괜찮아요", "it is alright", "it is fine / I am okay"),
    ],
    mistakes=[
        ("저는 미나입니다 있어요.", "저는 미나입니다.", "입니다 already ends the sentence — 있어요 does not follow it."),
        ("안녕하세요, 만나서 반갑습니다 감사합니다.", "만나서 반갑습니다.", "반갑습니다 is the whole greeting; stacking another thanks sounds mechanical."),
        ("이름이 뭐예요? 저는 미나 이에요.", "이름이 뭐예요? 저는 미나예요.", "미나 ends in a vowel: 예요. 이에요 follows a consonant, as in 학생이에요."),
    ],
    task_title="Introduce yourself in five sentences",
    task_instructions=("Write five Korean sentences: your name with 입니다, where you live with 에 살아요, "
                       "what you study or do, one thing you drink or eat, and one closing hello. Read them "
                       "aloud twice — 아요/어요 endings should sound like one word, not two."),
)

EXTRAS["A2"] = EXTRA(
    culture=("A Korean meal arrives all at once. 반찬, the small side dishes, are refilled without "
             "asking at most restaurants, and the rice and soup are yours alone. Because 반찬 and "
             "물 are shared, the polite habit is to fill a neighbour's glass before your own and to "
             "leave the last piece alone until somebody offers it. 수저 come in a rolled set, and "
             "using the spoon for rice and the chopsticks for 반찬 is the quiet default."),
    source_url="https://en.wikipedia.org/wiki/Korean_cuisine",
    reading=("지난 주말에 미나 씨와 부산에 갔어요. 아침 일찍 기차를 타고 바다를 봤어요. "
             "점심에는 회를 먹었는데 아주 신선했어요. 오후에는 시장에 갔습니다. "
             "과일이 비쌌지만 커피는 싸게 샀어요. 저녁에 비가 와서 우산을 하나 사야 했어요. "
             "그래도 좋은 여행이었습니다. 다음에는 사진을 더 많이 찍고 싶어요."),
    reading_gloss=("Last weekend I went to Busan with Mina. We took an early train and saw the sea. "
                   "For lunch we ate raw fish, and it was very fresh. In the afternoon we went to "
                   "the market. The fruit was expensive, but we bought coffee cheaply. In the "
                   "evening it rained, so we had to buy an umbrella. It was a good trip anyway. "
                   "Next time I want to take more photographs."),
    listening=("점원: 어서 오세요. 뭐 드릴까요?<br>지훈: 김밥 두 줄 주세요. 그리고 물도 주세요.<br>"
               "점원: 네, 여기 있습니다. 만 원입니다.<br>지훈: 카드로 될까요?<br>"
               "점원: 그럼요. 포장해 드릴까요?<br>지훈: 아니요, 여기서 먹겠습니다."),
    listening_gloss=("Server: Welcome, what would you like? Jihun: Two rolls of gimbap, please. And "
                     "water too. Server: Here you are. That is ten thousand won. Jihun: Can I pay by "
                     "card? Server: Of course. Shall I wrap it to go? Jihun: No, I will eat here."),
    voice_tag=VOICE,
    idioms=[
        ("얼마예요?", "how much is it?", "what does it cost?"),
        ("이거 주세요", "give me this", "this one, please"),
        ("포장해 주세요", "wrap it, please", "to go, please"),
        ("여기서 먹을게요", "I will eat here", "for here, please"),
        ("배불러요", "my stomach is full", "I am full"),
        ("많이 드세요", "eat a lot", "help yourself / enjoy the meal"),
        ("다음에 또 올게요", "I will come again next time", "see you again"),
        ("몇 시에 문을 닫아요?", "what time does the door close?", "when do you close?"),
        ("표가 두 장 필요해요", "I need two sheets of tickets", "two tickets, please"),
        ("사진을 찍어 주실 수 있어요?", "could you take a photograph for me?", "would you take our photo?"),
    ],
    mistakes=[
        ("어제 밥을 먹어요.", "어제 밥을 먹었어요.", "어제 is past, so the verb carries -았/었-; the present form belongs to 오늘."),
        ("물을 마시고 싶어요 있어요.", "물을 마시고 싶어요.", "싶어요 ends the sentence — a second verb cannot follow it."),
        ("집에 가요 싶어요.", "집에 가고 싶어요.", "A wish is made on the stem with -고 싶어요, never on the finished form 가요."),
    ],
    task_title="Tell the story of one day out",
    task_instructions=("Write six to eight sentences about a real or imagined outing, using at least four "
                       "past-tense verbs, one -고 싶어요 wish and one price. Then rewrite two of the past "
                       "sentences in the polite 합니다 form."),
)

EXTRAS["B1"] = EXTRA(
    culture=("Korean has six speech levels, and the two that matter first are 해요체 (-아요/어요) and "
             "합니다체 (-습니다/입니다). Neither is more polite than the other in the abstract: 해요체 "
             "is warm and standard in conversation, 합니다체 is the register of announcements, news "
             "and first meetings. Age and workplace rank decide which one, and -(으)시- marks the "
             "person you are talking about rather than the person you are talking to."),
    source_url="https://en.wikipedia.org/wiki/Korean_honorifics",
    reading=("우리 회사는 작지만 일이 많습니다. 저는 매일 아침 회의 자료를 만들고 오후에는 "
             "고객과 통화합니다. 요즘 새로운 일을 배우느라 바쁘지만 재미있습니다. "
             "지난주에는 팀장님께 제 의견을 말씀드렸습니다. 처음에는 긴장했지만 "
             "자료를 준비한 덕분에 잘 설명했습니다. 팀장님은 좋은 생각이라고 하셨습니다. "
             "다음 달에는 제가 발표를 맡을 것입니다."),
    reading_gloss=("Our company is small, but there is a lot of work. Every morning I prepare the "
                   "material for the meeting and in the afternoon I talk with customers. These days I "
                   "am busy learning something new, but it is interesting. Last week I gave my team "
                   "leader my opinion. At first I was nervous, but thanks to the preparation I "
                   "explained it well. The team leader said it was a good idea. Next month I will "
                   "give the presentation."),
    listening=("미나: 팀장님, 잠깐 시간 괜찮으십니까?<br>팀장: 네, 무슨 일이에요?<br>"
               "미나: 이번 주 보고서를 금요일까지 보내 드리려고 합니다.<br>"
               "팀장: 좋아요. 그런데 자료를 하나 더 넣어 주세요.<br>"
               "미나: 알겠습니다. 오늘 안으로 수정해서 보내 드리겠습니다."),
    listening_gloss=("Mina: Team leader, do you have a moment? Leader: Yes, what is it? Mina: I intend "
                     "to send this week's report by Friday. Leader: Good. Add one more set of figures, "
                     "though. Mina: Understood. I will correct it and send it today."),
    voice_tag=VOICE,
    idioms=[
        ("눈치가 빠르다", "the sense is quick", "reads other people and the room quickly"),
        ("발이 넓다", "the feet are wide", "knows a lot of people"),
        ("입이 무겁다", "the mouth is heavy", "keeps a secret"),
        ("손이 크다", "the hands are big", "generous, does things on a large scale"),
        ("속이 시원하다", "the inside is cool", "relieved, a weight off the mind"),
        ("말이 통하다", "the words connect", "understand each other without effort"),
        ("티가 나다", "the mark shows", "it is noticeable"),
        ("고생 끝에 낙이 온다", "after hardship comes joy", "things pay off in the end"),
        ("한 귀로 듣고 한 귀로 흘리다", "in one ear and out the other", "to ignore advice"),
        ("공든 탑이 무너지랴", "would a tower built with care collapse?", "steady effort stands"),
    ],
    mistakes=[
        ("저는 매운 음식을 먹지 않아요 못 해요.", "저는 매운 음식을 먹지 못해요.", "Choose one negation: -지 않다 means do not, -지 못하다 means cannot."),
        ("할아버지가 밥을 먹었어요.", "할아버지께서 밥을 드셨어요.", "An elder takes 께서 and the honorific verb 드시다, and the verb carries -시-."),
        ("몇 살이에요? 저는 스물 살이에요.", "몇 살이에요? 저는 스무 살이에요.", "스물 shortens to 스무 before the counter 살."),
    ],
    task_title="Give and defend one opinion",
    task_instructions=("Write a short opinion in 합니다체: state it with -고 생각합니다, support it with two "
                       "reasons, and add one sentence about what would change your mind. Use at least one "
                       "-지 않다 and one -(으)ㄹ 수 있다 form, and address one sentence to a superior with "
                       "the -시- honorific."),
)

EXTRAS["B2"] = EXTRA(
    culture=("정 is the Korean word for the bond that accumulates between people who have shared time, "
             "food and difficulty. It cannot be bought or hurried, and the language treats it as "
             "something you 감정을 쌓다, pile up. It explains a great deal of Korean professional life: "
             "a team will eat together after work, and a favour refused outright is rarer than a "
             "favour accepted slowly. In a debate, the same 정 means disagreement is usually wrapped "
             "in a frame that keeps the relationship intact."),
    source_url="https://en.wikipedia.org/wiki/Culture_of_Korea",
    reading=("토론에서 이기는 것보다 중요한 것은 상대의 주장을 정확히 이해하는 일입니다. "
             "상대가 근거를 제시하면 먼저 인정하고, 그다음에 제 한계를 지적해야 합니다. "
             "그러나 감정적인 표현은 설득력을 떨어뜨립니다. 예를 들어 우리가 이 자료를 "
             "믿을 수 있다면 결론도 받아들일 수 있습니다. 반대로 근거가 약하면 결론을 "
             "보류하는 것이 옳습니다. 좋은 토론은 이기고 지는 것이 아니라 함께 더 나은 "
             "결정에 이르는 과정입니다."),
    reading_gloss=("In a debate, understanding the other side's argument exactly matters more than "
                   "winning. When they offer evidence, acknowledge it first and only then point out "
                   "its limits. Emotional phrasing, however, weakens persuasion. For example, if we "
                   "can trust this data we can also accept the conclusion. If the evidence is weak, "
                   "on the other hand, the right move is to hold the conclusion back. A good debate "
                   "is not winning and losing but a process of arriving at a better decision "
                   "together."),
    listening=("동료: 이번 결정은 너무 빠르지 않았습니까?<br>분석자: 속도는 문제가 아닙니다. 근거가 약한 것이 문제입니다.<br>"
               "동료: 그럼 결정을 취소해야 한다고 보십니까?<br>"
               "분석자: 아니요, 조건을 붙여서 유지하는 편이 낫습니다.<br>"
               "동료: 예를 들어 어떤 조건입니까?"),
    listening_gloss=("Colleague: Was this decision not too fast? Analyst: Speed is not the problem. "
                     "Weak evidence is the problem. Colleague: Then do you think the decision should "
                     "be cancelled? Analyst: No — it is better to keep it with conditions attached. "
                     "Colleague: For example, what conditions?"),
    voice_tag=VOICE,
    idioms=[
        ("아무리 바빠도", "no matter how busy", "however busy it gets"),
        ("하늘이 무너져도 솟아날 구멍이 있다", "even if the sky falls, there is a hole to escape through", "there is always a way out"),
        ("가는 말이 고와야 오는 말이 곱다", "if the words you send are kind, the words that come back are kind", "you get back what you give"),
        ("티끌 모아 태산", "gather the dust and it becomes a mountain", "small savings add up"),
        ("우물 안 개구리", "a frog in a well", "someone who cannot see beyond their own patch"),
        ("빈 수레가 요란하다", "the empty cart rattles loudest", "the least capable talk the most"),
        ("일석이조", "one stone, two birds", "solving two things at once"),
        ("사공이 많으면 배가 산으로 간다", "with many boatmen the boat goes up the mountain", "too many decision-makers, no direction"),
        ("선을 긋다", "to draw a line", "to set a boundary"),
        ("무게를 두다", "to place weight", "to give something priority"),
    ],
    mistakes=[
        ("선생님, 어제 뵙었어요.", "선생님, 어제 뵈었어요.", "뵙다 inserts ㅂ only before a vowel ending: 뵈었어요, but 뵙겠습니다."),
        ("이 문제는 저에 의해 해결되었습니다.", "이 문제는 제가 해결했습니다.", "Korean prefers the active voice for your own actions; -에 의해 is translationese."),
        ("그 일은 제가 하겠습니다. 그래서 팀장님과 상의하지 않았습니다.", "그 일은 제가 하겠지만, 팀장님과 상의해야 합니다.", "하겠지만 balances the promise against the requirement in one sentence."),
    ],
    task_title="Take two sides of one question",
    task_instructions=("Choose a question you actually disagree with somebody about. Write the strongest "
                       "version of the other side in three sentences, then your own in three, linking them "
                       "with -지만, 반면에 and 따라서. Finish with the condition under which you would "
                       "change your position."),
)

EXTRAS["C1"] = EXTRA(
    culture=("Korean newspaper prose runs on a register of its own. Headlines drop particles and end in "
             "nouns; the body uses -했다 for what happened and -했다고 for what somebody said, so that "
             "every claim arrives with its source attached. Quotation is therefore not decoration but "
             "grammar: -다고 하다 turns a sentence into reported speech, and a writer who drops it is "
             "claiming the statement rather than attributing it. Mediation between two sides is done "
             "in the same spirit, with different endings for each side's position."),
    source_url="https://en.wikipedia.org/wiki/Korean_grammar",
    reading=("보고서에 따르면 올해 상반기 수출은 지난해 같은 기간보다 늘었지만 지역별 격차가 "
             "확대된 것으로 나타났다. 특히 수도권의 증가율이 두 자릿수를 기록한 반면 지방은 "
             "한 자릿수에 머물렀다. 전문가들은 환율과 물류비가 주요 변수라고 지적했다. "
             "한 연구자는 이 흐름이 일시적일 수 있다고 보았고, 다른 연구자는 구조적 변화라고 "
             "반박했다. 두 주장 모두 근거를 갖추고 있으나 아직 결론을 내리기에는 이르다."),
    reading_gloss=("According to the report, exports in the first half of this year rose against the "
                   "same period last year, but the gap between regions widened. The capital region "
                   "recorded double-digit growth, while the provinces stayed in single digits. "
                   "Experts pointed to the exchange rate and logistics costs as the main variables. "
                   "One researcher held that the trend may be temporary, and another countered that "
                   "it is a structural change. Both claims carry evidence, but it is too early to "
                   "conclude."),
    listening=("기자: 발표 내용을 조금 더 구체적으로 설명해 주시겠습니까?<br>"
               "연구자: 수출 증가는 사실이지만 원인은 아직 단정하기 어렵습니다.<br>"
               "기자: 그러면 정책 효과는 없었다고 보십니까?<br>"
               "연구자: 그렇게 말씀드리지는 않겠습니다. 다만 근거가 더 필요하다는 것입니다.<br>"
               "기자: 알겠습니다. 한계를 명시해서 보도하겠습니다."),
    listening_gloss=("Reporter: Could you explain the announcement in more detail? Researcher: The rise "
                     "in exports is a fact, but the cause cannot yet be pinned down. Reporter: Then do "
                     "you think the policy had no effect? Researcher: I would not put it that way. I am "
                     "saying we need more evidence. Reporter: Understood — I will report it with the "
                     "limits stated."),
    voice_tag=VOICE,
    idioms=[
        ("설상가상", "on top of the snow, more snow", "to make matters worse"),
        ("금상첨화", "flowers added to brocade", "something good on top of something already good"),
        ("사면초가", "enemies on all four sides", "besieged with no way out"),
        ("오리무중", "five li deep in fog", "completely unclear"),
        ("반신반의", "half believe, half doubt", "to be half convinced"),
        ("자충수", "a move that checkmates yourself", "a self-defeating move"),
        ("뜨거운 감자", "a hot potato", "a topic nobody wants to hold"),
        ("이견을 보이다", "to show a different view", "to disagree publicly"),
        ("선례를 남기다", "to leave a precedent", "to set a precedent"),
        ("결론을 유보하다", "to hold the conclusion back", "to reserve judgement"),
    ],
    mistakes=[
        ("보고서는 수출이 늘었다고 말했다 늘어났다.", "보고서는 수출이 늘었다고 말했다.", "In reported speech the quoted clause already carries its ending; do not restate it."),
        ("정책 효과가 없었다고 보입니다.", "정책 효과가 없었다고 봅니다.", "The reporting verb is the writer's: 봅니다, not the passive 보입니다."),
        ("지역 격차가 확대되었다는 점을 지적했다고 밝혔다.", "지역 격차가 확대되었다는 점을 지적했다.", "One attribution per sentence — -다고 밝히다 cannot be stacked on 지적하다."),
    ],
    task_title="Report an argument without taking it",
    task_instructions=("Take a real news claim and write four sentences of Korean report: the claim with "
                       "-다고 하다, the evidence it rests on, the strongest counter-argument, and one "
                       "sentence that states plainly what remains unresolved. Use 보도체 endings and no "
                       "first-person opinion."),
)

EXTRAS["C2"] = EXTRA(
    culture=("Modern Korean literature grew out of a century of rupture — colonial rule, division, war "
             "and rapid industrialisation — and its central subject has often been the family under "
             "pressure. That history left the language with an unusually rich vocabulary of oblique "
             "feeling: 한, a grief that is carried and not resolved, 서러움, 억울함, and the many ways "
             "of saying that something cannot be expressed. A translator of Korean prose spends most "
             "effort not on exotic words but on the particles that decide who is bowing to whom."),
    source_url="https://en.wikipedia.org/wiki/Korean_literature",
    reading=("이 소설은 한 가족의 삼십 년을 다룬다. 화자는 어머니의 침묵을 설명하지 않고 "
             "그 침묵이 놓인 자리만 보여 준다. 독자는 무엇이 말해지지 않았는지 스스로 "
             "채워야 한다. 그래서 이 작품은 슬픔을 확인해 주는 대신 슬픔을 견디게 한다. "
             "번역자는 존댓말과 반말의 차이를 옮길 수 없을 때 각주를 붙였고, 그 각주가 "
             "오히려 이 소설의 주제를 드러낸다 — 말할 수 없는 것을 어떻게 말할 것인가."),
    reading_gloss=("This novel covers thirty years of one family. The narrator does not explain the "
                   "mother's silence, only shows the place where it sits. The reader must fill in "
                   "what was not said. So instead of confirming grief, the work makes it bearable. "
                   "Where the difference between honorific and plain speech could not be carried "
                   "over, the translator added footnotes, and those notes end up exposing the "
                   "novel's subject: how to say what cannot be said."),
    listening=("중재자: 두 분의 표현이 서로 다르지만 요구는 가깝습니다.<br>"
               "편집자: 저는 단어를 바꾸자는 것이 아니라 책임을 밝히자는 것입니다.<br>"
               "검토자: 저 역시 책임에는 동의합니다. 다만 문장이 단정적으로 들릴까 봐 걱정합니다.<br>"
               "중재자: 그러면 사실은 단정적으로, 평가는 완곡하게 나누어 쓰면 어떨까요?<br>"
               "편집자: 그렇게 하면 독자도 오해하지 않겠습니다.<br>"
               "검토자: 좋습니다. 그 선에서 정리하겠습니다."),
    listening_gloss=("Mediator: Your wording differs, but your requirements are close. Editor: I am not "
                     "asking to change a word — I am asking to state responsibility. Reviewer: I agree "
                     "on responsibility. I only worry the sentence will sound categorical. Mediator: "
                     "Then how about stating the facts categorically and the assessment gently? "
                     "Editor: That way readers will not misread it. Reviewer: Good — let us settle it "
                     "on that line."),
    voice_tag=VOICE,
    idioms=[
        ("새옹지마", "the old man's horse — no misfortune, no fortune", "an apparent blessing or curse may turn out otherwise"),
        ("오십보백보", "fifty steps, a hundred steps", "little to choose between the two"),
        ("견강부회", "forcing the speech to fit", "twisting facts to fit an argument"),
        ("마이동풍", "horse ears, east wind", "advice that goes in one ear and out the other"),
        ("조삼모사", "three in the morning, four in the evening", "deceiving with trivial options"),
        ("등잔 밑이 어둡다", "it is dark under the lamp", "the obvious thing nearby is overlooked"),
        ("세월이 약이다", "time is the medicine", "time heals"),
        ("말 한마디에 천 냥 빚을 갚는다", "one word repays a thousand nyang of debt", "a kind word settles a great deal"),
        ("언 발에 오줌 누기", "pissing on a frozen foot", "a stopgap that makes things worse"),
        ("물 밑에 돌 있나 모른다", "you cannot know a stone underwater", "you cannot know what is hidden"),
    ],
    mistakes=[
        ("그의 침묵은 슬픔을 의미합니다고 봅니다.", "그의 침묵은 슬픔을 뜻한다고 봅니다.", "The quoted clause takes -ㄴ다고/는다고, and the reporting verb follows it directly."),
        ("어머니는 아무 말도 안 하시고 침묵하셨습니다.", "어머니는 아무 말도 하지 않으셨습니다.", "침묵하다 is a noun plus 하다; the natural verb here is 말이 없다/말하지 않다."),
        ("이 문장은 번역할 수가 없습니다니까 각주를 붙였습니다.", "이 문장은 번역할 수 없어서 각주를 붙였습니다.", "Reason takes -아서/-어서; -ㅂ니다까 is not a connective."),
    ],
    task_title="Write across what cannot be translated",
    task_instructions=("Take one Korean expression with no English equivalent. Write four sentences: what it "
                       "means literally, what it means in use, one scene where it decides something, and "
                       "what a translator loses. Then take the two hardest sentences and rewrite them for "
                       "a reader who knows no Korean."),
)

THIRD["A1"] = [
    ("A1-U1", "A1-U1-L3", L("숫자와 전화번호", 
        "Native numbers 하나·둘·셋 count things and tell age; before a counter 둘 becomes 두 and 셋 "
        "becomes 세. Phone numbers are read one digit at a time, and zero is 공, never 영.",
        [V("하나", "hana", "one (native)", "number"),
         V("둘", "dul", "two (native)", "number"),
         V("셋", "set", "three (native)", "number"),
         V("전화번호", "jeonhwa-beonho", "phone number", "noun"),
         V("몇", "myeot", "how many, which number", "determiner")],
        G("Native numbers and counters",
          "하나 · 둘 · 셋 → 한 개 · 두 개 · 세 개 · 전화번호가 뭐예요? · 공일공",
          "Sino-Korean numbers (일 이 삼) do dates, money and minutes; native numbers do counting "
          "and age. Before a counter the last two shapes shorten: 둘 to 두, 셋 to 세. In a phone "
          "number each digit stands alone, so the counter rule does not apply at all.",
          [X("전화번호가 뭐예요?", "jeonhwa-beonho-ga mwo-yeyo?", "What is your phone number?"),
           X("공일공에 이삼사오 육칠팔구예요.", "gong-il-gong-e i-sam-sa-o yuk-chil-pal-gu-yeyo.", "It is 010-2345-6789."),
           X("사과 두 개 주세요.", "sagwa du gae juseyo.", "Two apples, please.")],
          [("사과 둘 주세요.", "사과 두 개 주세요.", "둘 shortens to 두 before the counter 개."),
           ("전화번호가 영일영입니다.", "전화번호가 공일공입니다.", "A telephone zero is read 공; 영 is the number zero in arithmetic.")]),
        [D("미나", "전화번호가 뭐예요?", "jeonhwa-beonho-ga mwo-yeyo?", "What is your phone number?"),
         D("지훈", "공일공에 이삼사오 육칠팔구예요.", "gong-il-gong-e i-sam-sa-o yuk-chil-pal-gu-yeyo.", "It is 010-2345-6789."),
         D("미나", "다시 한 번 말씀해 주세요.", "dasi han beon malsseumhae juseyo.", "Say it once more, please."),
         D("지훈", "공일공, 이삼사오, 육칠팔구.", "gong-il-gong, i-sam-sa-o, yuk-chil-pal-gu.", "Zero-one-zero, two-three-four-five, six-seven-eight-nine.")],
        WS("Number worksheet", [
            T("Count with the right counter.", ["two apples", "three people"],
              ["사과 두 개", "사람 세 명"]),
            T("Read the number.", ["010-1234-5678", "what is your phone number?"],
              ["공일공에 일이삼사 오육칠팔", "전화번호가 뭐예요?"]),
        ]))),
    ("A1-U2", "A1-U2-L3", L("가족이 있어요",
        "Family words carry the speaker's position: a woman says 언니 or 오빠 where a man says 누나 or "
        "형, and a younger sibling is 동생 to everyone. Existence takes 있어요, and the thing that "
        "exists takes 이/가, not 을/를.",
        [V("가족", "gajok", "family", "noun"),
         V("어머니", "eomeoni", "mother", "noun"),
         V("아버지", "abeoji", "father", "noun"),
         V("동생", "dongsaeng", "younger sibling", "noun"),
         V("계시다", "gyesida", "to be present (honorific)", "verb")],
        G("있어요 and 없어요",
          "저는 동생이 있어요 · 동생이 없어요 · 어머니가 계세요",
          "Having and being there are the same verb in Korean: 있다. The thing that exists takes "
          "이/가. For a living person older or higher than you the honorific 계시다 replaces 있다, "
          "which is why the question 어머니가 계세요? is polite and 어머니가 있어요? is blunt.",
          [X("저는 동생이 있어요.", "jeo-neun dongsaeng-i iss-eoyo.", "I have a younger sibling."),
           X("우리 가족은 네 명이에요.", "uri gajok-eun ne myeong-ieyo.", "There are four of us in my family."),
           X("할머니가 계세요?", "halmeoni-ga gyeseyo?", "Is your grandmother at home?")],
          [("저는 동생을 있어요.", "저는 동생이 있어요.", "있다 takes 이/가 on what exists, never 을/를."),
           ("아버지가 있어요 계세요.", "아버지가 계세요.", "One verb: a living elder takes 계시다, and the two are not stacked.")]),
        [D("지훈", "미나 씨는 가족이 어떻게 되세요?", "mina ssi-neun gajok-i eotteoke doeseyo?", "Mina, who is in your family?"),
         D("미나", "부모님과 동생이 있어요.", "bumonim-gwa dongsaeng-i iss-eoyo.", "I have my parents and a younger sibling."),
         D("지훈", "동생이 학생이에요?", "dongsaeng-i haksaeng-ieyo?", "Is your younger sibling a student?"),
         D("미나", "네, 고등학생이에요. 지훈 씨는요?", "ne, godeunghaksaeng-ieyo. jihun ssi-neunyo?", "Yes, a high-school student. And you?")],
        WS("Family worksheet", [
            T("Say who is in your family.", ["I have a younger sibling.", "there are four of us"],
              ["저는 동생이 있어요", "우리 가족은 네 명이에요"]),
            T("Ask politely about an elder.", ["is your grandmother at home?", "is your father a teacher?"],
              ["할머니가 계세요?", "아버지가 선생님이세요?"]),
        ]))),
    ("A1-U3", "A1-U3-L3", L("카페에서 주문해요",
        "Ordering is one frame: the item, the counter, then 주세요. Drinks take the counter 잔 and "
        "hot and cold are adjectives placed before the noun, 뜨거운 커피 and 차가운 커피.",
        [V("커피", "keopi", "coffee", "noun"),
         V("아메리카노", "amerikano", "americano", "noun"),
         V("뜨거운", "tteugeoun", "hot (to the touch)", "adjective"),
         V("차가운", "chagaun", "cold", "adjective"),
         V("한 잔", "han jan", "one cup (counter 잔)", "counter")],
        G("Ordering with 주세요",
          "커피 한 잔 주세요 · 아메리카노 두 잔 주세요 · 뜨거운 걸로 주세요",
          "주세요 is the polite request built on 주다. The order is noun, counter, then 주세요; "
          "the choice between two things takes -(으)로, as in 뜨거운 걸로 주세요 — the hot one, please.",
          [X("커피 한 잔 주세요.", "keopi han jan juseyo.", "One coffee, please."),
           X("아메리카노 두 잔 주세요.", "amerikano du jan juseyo.", "Two americanos, please."),
           X("차가운 걸로 주세요.", "chagaun geollo juseyo.", "The cold one, please.")],
          [("커피 한 개 주세요.", "커피 한 잔 주세요.", "A drink is counted in 잔; 개 counts objects."),
           ("주세요 커피.", "커피 주세요.", "Korean puts the object before the verb.")]),
        [D("점원", "어서 오세요. 뭐 드릴까요?", "eoseo oseyo. mwo deurilkkayo?", "Welcome. What can I get you?"),
         D("미나", "아메리카노 한 잔 주세요.", "amerikano han jan juseyo.", "One americano, please."),
         D("점원", "뜨거운 걸로 드릴까요?", "tteugeoun geollo deurilkkayo?", "Shall I make it hot?"),
         D("미나", "네, 뜨거운 걸로 주세요. 그리고 물도 주세요.", "ne, tteugeoun geollo juseyo. geurigo muldo juseyo.", "Yes, the hot one. And water too, please.")],
        WS("Café worksheet", [
            T("Order a drink.", ["one coffee", "two americanos"],
              ["커피 한 잔 주세요", "아메리카노 두 잔 주세요"]),
            T("Say which one you want.", ["the cold one, please", "the hot one, please"],
              ["차가운 걸로 주세요", "뜨거운 걸로 주세요"]),
        ]))),
]

THIRD["A2"] = [
    ("A2-U1", "A2-U1-L3", L("약속을 잡아요",
        "Making an appointment moves between two question shapes: -(으)ㄹ까요? invites, 어때요? asks "
        "how something suits. The future -(으)ㄹ 거예요 states what will happen once the time is agreed.",
        [V("약속", "yaksok", "appointment, promise", "noun"),
         V("토요일", "toyoil", "Saturday", "noun"),
         V("언제", "eonje", "when", "adverb"),
         V("-(으)ㄹ 거예요", "-(eu)l geoyeyo", "will (future)", "grammar"),
         V("만나다", "mannada", "to meet", "verb")],
        G("Proposing and agreeing",
          "토요일 어때요? · 몇 시에 만날까요? · 두 시에 만나요 · 좋아요",
          "어때요? asks whether a suggestion suits; -(으)ㄹ까요? asks the other person to decide with "
          "you. The answer can be as short as 좋아요, and the agreed time takes 에: 두 시에 만나요.",
          [X("토요일 어때요?", "toyoil eottaeyo?", "How is Saturday?"),
           X("몇 시에 만날까요?", "myeot si-e mannalkkayo?", "What time shall we meet?"),
           X("두 시에 만나요.", "du si-e mannayo.", "Let us meet at two.")],
          [("토요일에 만나요 어때요?", "토요일 어때요?", "어때요 is a whole question; do not put another verb in front of it."),
           ("일요일에 시간이 없어요. 일요일이 어때요?", "일요일에 시간이 없어요. 일요일은 어때요?", "The contrastive 은/는 marks the alternative day you are proposing.")]),
        [D("지훈", "미나 씨, 이번 주말에 시간 있어요?", "mina ssi, ibeon jumare sigan iss-eoyo?", "Mina, do you have time this weekend?"),
         D("미나", "토요일은 괜찮아요. 왜요?", "toyoil-eun gwaenchanayo. waeyo?", "Saturday is fine. Why?"),
         D("지훈", "영화를 볼까요? 몇 시가 좋아요?", "yeonghwa-reul bolkkayo? myeot si-ga joayo?", "Shall we see a film? What time is good?"),
         D("미나", "세 시는 어때요? 그다음에 커피도 마셔요.", "se si-neun eottaeyo? geudaeum-e keopido masyeoyo.", "How about three? And coffee afterwards.")],
        WS("Appointment worksheet", [
            T("Suggest a time.", ["how is Saturday?", "what time shall we meet?"],
              ["토요일 어때요?", "몇 시에 만날까요?"]),
            T("Answer with a plan.", ["I will meet at three.", "I will drink coffee afterwards."],
              ["세 시에 만나요", "그다음에 커피를 마셔요"]),
        ]))),
    ("A2-U2", "A2-U2-L3", L("지하철을 타요",
        "A journey is built from three endings: -(으)로 for the line or vehicle you take, 에서 for "
        "where you get off or change, and 까지 for the destination. 교통카드 does the paying.",
        [V("지하철", "jihacheol", "subway", "noun"),
         V("교통카드", "gyotong-kadeu", "transit card", "noun"),
         V("몇 호선", "myeot hoseon", "which line (number)", "noun"),
         V("갈아타다", "garatada", "to transfer", "verb"),
         V("내리다", "naerida", "to get off", "verb")],
        G("Getting there",
          "2호선으로 갈아타요 · 강남역에서 내려요 · 서울역까지 가요",
          "The line you take or change to takes -(으)로; the station where you get off takes 에서; "
          "the destination takes 까지. 갈아타다 already means change, so the vehicle that follows is "
          "the one you change onto.",
          [X("2호선으로 갈아타세요.", "i hoseon-euro garataseyo.", "Transfer to line two."),
           X("강남역에서 내려요.", "gangnamyeok-eseo naeryeoyo.", "I get off at Gangnam station."),
           X("서울역까지 얼마나 걸려요?", "seoullyeok-kkaji eolmana geollyeoyo?", "How long does it take to Seoul station?")],
          [("2호선을 갈아타요.", "2호선으로 갈아타요.", "The line you change to takes -(으)로, not 을/를."),
           ("버스를 갈아타요.", "버스로 갈아타요.", "A vehicle you change to takes the same -(으)로.")]),
        [D("미나", "지훈 씨, 강남에 어떻게 가요?", "jihun ssi, gangnam-e eotteoke gayo?", "Jihun, how do I get to Gangnam?"),
         D("지훈", "2호선으로 갈아타세요. 교통카드 있어요?", "i hoseon-euro garataseyo. gyotong-kadeu iss-eoyo?", "Transfer to line two. Do you have a transit card?"),
         D("미나", "네, 있어요. 어디에서 내려요?", "ne, iss-eoyo. eodi-eseo naeryeoyo?", "Yes. Where do I get off?"),
         D("지훈", "강남역에서 내리면 돼요. 십 분쯤 걸려요.", "gangnamyeok-eseo naerimyeon dwaeyo. sip bun-jjeum geollyeoyo.", "You just get off at Gangnam station. It takes about ten minutes.")],
        WS("Transit worksheet", [
            T("Give the route.", ["transfer to line two", "get off at Gangnam station"],
              ["2호선으로 갈아타세요", "강남역에서 내려요"]),
            T("Ask the time.", ["how long does it take to Seoul station?", "how do I get to Gangnam?"],
              ["서울역까지 얼마나 걸려요?", "강남에 어떻게 가요?"]),
        ]))),
    ("A2-U3", "A2-U3-L3", L("시장에서 값을 깎아요",
        "At a market a price is a conversation. 싸게 해 주세요 asks for a lower price, -면 makes it "
        "conditional on quantity, and the reply usually names a number and stops.",
        [V("값", "gap", "price", "noun"),
         V("깎다", "kkakda", "to cut (a price)", "verb"),
         V("싸게", "ssage", "cheaply", "adverb"),
         V("전부", "jeonbu", "all, in total", "noun"),
         V("두 개", "du gae", "two (with counter 개)", "counter")],
        G("Asking for a price",
          "얼마예요? · 두 개 사면 얼마예요? · 좀 싸게 해 주세요",
          "The conditional -면 turns quantity into a bargain: 두 개 사면 얼마예요? asks what two "
          "would cost. The request 싸게 해 주세요 works on the price with 하다 — 만들다 would mean "
          "making an object, not lowering a number.",
          [X("이거 얼마예요?", "igeo eolmayeyo?", "How much is this?"),
           X("두 개 사면 얼마예요?", "du gae samyeon eolmayeyo?", "How much if I buy two?"),
           X("좀 싸게 해 주세요.", "jom ssage hae juseyo.", "Make it a little cheaper, please.")],
          [("좀 싸게 만들어 주세요.", "좀 싸게 해 주세요.", "A price is lowered with 하다; 만들다 makes a thing."),
           ("너무 비싸요 깎아 주세요.", "너무 비싸니까 깎아 주세요.", "-니까 links the reason to the request in one sentence.")]),
        [D("지훈", "이 귤 한 상자 얼마예요?", "i gyul han sangja eolmayeyo?", "How much is a box of these tangerines?"),
         D("상인", "만 오천 원이에요.", "man ocheon won-ieyo.", "Fifteen thousand won."),
         D("지훈", "두 상자 사면 얼마예요?", "du sangja samyeon eolmayeyo?", "How much for two boxes?"),
         D("상인", "그럼 이만 팔천 원에 드릴게요.", "geureom iman palcheon won-e deurilgeyo.", "Then I will give you both for twenty-eight thousand.")],
        WS("Market worksheet", [
            T("Ask the price.", ["how much is this?", "how much if I buy two?"],
              ["이거 얼마예요?", "두 개 사면 얼마예요?"]),
            T("Bargain politely.", ["make it a little cheaper, please", "then I will buy two"],
              ["좀 싸게 해 주세요", "그럼 두 개 살게요"]),
        ]))),
]

THIRD["B1"] = [
    ("B1-U1", "B1-U1-L3", L("약속을 지키지 못했을 때",
        "Missing an appointment needs one sentence, not two: -지 못해서 carries the failure into the "
        "apology. To ask for a new time, use -(으)ㄹ 수 있을까요? with a reason attached.",
        [V("사정", "sajeong", "circumstances, a situation", "noun"),
         V("늦다", "neutda", "to be late", "verb"),
         V("지키다", "jikida", "to keep (a promise)", "verb"),
         V("미루다", "miruda", "to postpone", "verb"),
         V("-(으)ㄹ 수 있을까요?", "-(eu)l su isseulkkayo?", "could you / would it be possible to", "phrase")],
        G("Apology and repair",
          "약속을 지키지 못해서 죄송합니다 · 사정이 생겼습니다 · 시간을 바꿀 수 있을까요?",
          "-지 못하다 is cannot, -지 않다 is do not; an apology explains the failure with 못해서, not "
          "with 않아서. The request for a new time is softened by -(으)ㄹ까요?, and the reason precedes it.",
          [X("약속을 지키지 못해서 죄송합니다.", "yaksok-eul jikiji motaeseo joesonghamnida.", "I am sorry I could not keep the appointment."),
           X("갑자기 사정이 생겼습니다.", "gapjagi sajeong-i saenggyeotseumnida.", "Something came up suddenly."),
           X("다음 주로 미룰 수 있을까요?", "daeum ju-ro mirul su isseulkkayo?", "Could we put it off to next week?")],
          [("약속을 지키지 않았습니다 미안합니다.", "약속을 지키지 못해서 미안합니다.", "-지 못해서 joins the failure to the apology in one sentence."),
           ("시간을 바꿀 수 있어요입니까?", "시간을 바꿀 수 있습니까?", "해요체 and 합니다체 endings are not combined in one verb.")]),
        [D("지훈", "미나 씨, 오늘 약속을 지키지 못해서 죄송합니다.", "mina ssi, oneul yaksok-eul jikiji motaeseo joesonghamnida.", "Mina, I am sorry I cannot keep today's appointment."),
         D("미나", "괜찮아요. 무슨 일이에요?", "gwaenchanayo. museun ir-ieyo?", "It is all right. What happened?"),
         D("지훈", "갑자기 사정이 생겼어요. 다음 주로 미룰 수 있을까요?", "gapjagi sajeong-i saenggyeosseoyo. daeum ju-ro mirul su isseulkkayo?", "Something came up. Could we move it to next week?"),
         D("미나", "그럼요. 다음 주 금요일은 어때요?", "geureomnyo. daeum ju geumyoil-eun eottaeyo?", "Of course. How is next Friday?")],
        WS("Repair worksheet", [
            T("Apologise once, completely.", ["I could not keep the appointment.", "something came up suddenly"],
              ["약속을 지키지 못해서 죄송합니다", "갑자기 사정이 생겼습니다"]),
            T("Ask for a new time.", ["could we postpone it to next week?", "would Friday be possible?"],
              ["다음 주로 미룰 수 있을까요?", "금요일은 가능할까요?"]),
        ]))),
    ("B1-U2", "B1-U2-L3", L("축하할 일과 위로할 일",
        "Events come with their own verbs: 축하하다 for congratulations, 위로하다 for comfort, and "
        "드리다 for the gift or the greeting you give a superior. A parent in a sentence takes 께서 "
        "and -(으)시- even when nothing polite is being said to them.",
        [V("결혼식", "gyeolhonsik", "wedding ceremony", "noun"),
         V("축의금", "chuk-uigeum", "congratulatory money", "noun"),
         V("돌잔치", "doljanchi", "first-birthday party", "noun"),
         V("드리다", "deurida", "to give (humble)", "verb"),
         V("위로하다", "wirohada", "to comfort", "verb")],
        G("Congratulations and condolences",
          "결혼을 축하합니다 · 축의금을 드렸어요 · 어머니께서 가셨어요",
          "축하하다 takes the event as its object, so it is 결혼을 축하합니다, not 결혼식을 축하합니다. "
          "When you give something to an elder the verb is the humble 드리다, and when an elder does "
          "something to you the verb carries -(으)시-.",
          [X("결혼을 축하합니다.", "gyeolhon-eul chukhahamnida.", "Congratulations on your marriage."),
           X("축의금을 드렸어요.", "chuk-uigeum-eul deuryeosseoyo.", "I gave congratulatory money."),
           X("어머니께서 결혼식에 가셨어요.", "eomeoni-kkeseo gyeolhonsik-e gasyeosseoyo.", "My mother went to the wedding.")],
          [("진수 씨를 축하합니다.", "진수 씨의 결혼을 축하합니다.", "축하하다 takes the event, not the person."),
           ("어머니가 결혼식에 갔어요.", "어머니께서 결혼식에 가셨어요.", "An elder takes 께서 and -시- even in plain narration.")]),
        [D("미나", "지훈 씨, 진수 씨 결혼식에 가요?", "jihun ssi, jinsu ssi gyeolhonsik-e gayo?", "Jihun, are you going to Jinsu's wedding?"),
         D("지훈", "네, 토요일에 가요. 축의금은 얼마쯤 드려요?", "ne, toyoil-e gayo. chuk-uigeum-eun eolma-jjeum deuryeoyo?", "Yes, on Saturday. About how much should I give?"),
         D("미나", "친한 친구면 십만 원쯤 드려요.", "chinhan chingu-myeon simman won-jjeum deuryeoyo.", "For a close friend, about a hundred thousand won."),
         D("지훈", "알겠어요. 결혼을 진심으로 축하한다고 전할게요.", "algesseoyo. gyeolhon-eul jinsim-euro chukhahandago jeonhalgeyo.", "Understood. I will pass on my sincere congratulations.")],
        WS("Occasions worksheet", [
            T("Congratulate correctly.", ["congratulations on your marriage", "I gave congratulatory money"],
              ["결혼을 축하합니다", "축의금을 드렸어요"]),
            T("Speak about an elder.", ["my mother went to the wedding", "is your grandmother at home?"],
              ["어머니께서 결혼식에 가셨어요", "할머니가 계세요?"]),
        ]))),
    ("B1-U3", "B1-U3-L3", L("계절과 옷차림",
        "Weather adjectives are irregular where it matters: 춥다 becomes 추워요 and 덥다 becomes "
        "더워요. Advice takes -는 게 좋아요, and a time when something happens takes -을 때.",
        [V("계절", "gyejeol", "season", "noun"),
         V("옷차림", "otcharim", "the way one is dressed", "noun"),
         V("입다", "ipda", "to wear, to put on", "verb"),
         V("벗다", "beotda", "to take off", "verb"),
         V("챙기다", "chaenggida", "to take along, to look after", "verb")],
        G("Weather, advice and time",
          "겨울에는 추워요 · 더울 때는 반팔을 입어요 · 우산을 챙기는 게 좋아요",
          "The ㅂ-irregular adjectives drop ㅂ before a vowel ending: 춥다 to 추워요, 덥다 to 더워요. "
          "Advice is given with -는 게 좋아요, and -을 때 marks the moment the advice applies to.",
          [X("겨울에는 정말 추워요.", "gyeoul-e-neun jeongmal chuwoyo.", "It is really cold in winter."),
           X("더울 때는 반팔을 입어요.", "deoul ttae-neun banpar-eul ibeoyo.", "When it is hot I wear a short-sleeved shirt."),
           X("우산을 챙기는 게 좋아요.", "usan-eul chaenggineun ge joayo.", "It is better to take an umbrella.")],
          [("날씨가 춥어요.", "날씨가 추워요.", "춥다 is ㅂ-irregular: 추워요, not 춥어요."),
           ("비가 오면 우산을 챙기세요 좋아요.", "비가 오면 우산을 챙기는 게 좋아요.", "One advice frame per sentence.")]),
        [D("미나", "오늘 날씨가 어때요?", "oneul nalssi-ga eottaeyo?", "How is the weather today?"),
         D("지훈", "아침에는 추웠는데 지금은 따뜻해요.", "acham-e-neun chuwotneunde jigeum-eun ttatteutaeyo.", "It was cold in the morning, but it is warm now."),
         D("미나", "저녁에 비가 온대요. 우산을 챙기세요.", "jeonyeok-e bi-ga ondaeyo. usan-eul chaenggiseyo.", "They say it will rain in the evening. Take an umbrella."),
         D("지훈", "그럼 따뜻한 옷도 입는 게 좋겠네요.", "geureom ttatteutan otdo ipneun ge jotgetneyo.", "Then I had better wear warm clothes too.")],
        WS("Weather worksheet", [
            T("Describe the season.", ["it is really cold in winter", "it was cold in the morning"],
              ["겨울에는 정말 추워요", "아침에는 추웠어요"]),
            T("Give advice.", ["it is better to take an umbrella", "when it is hot I wear a short-sleeved shirt"],
              ["우산을 챙기는 게 좋아요", "더울 때는 반팔을 입어요"]),
        ]))),
]

THIRD["B2"] = [
    ("B2-U1", "B2-U1-L3", L("계획이 바뀔 때",
        "A plan that did not happen is told with -(으)려고 했어요, and what replaced it is named with "
        "대신에. When nothing could have been done the phrase is 어쩔 수 없이, which takes the whole "
        "sentence and never a second verb.",
        [V("계획", "gyehoek", "plan", "noun"),
         V("바뀌다", "bakkwida", "to change, to be changed", "verb"),
         V("대신에", "daesin-e", "instead of", "phrase"),
         V("어쩔 수 없이", "eojjeol su eopsi", "having no choice", "adverb"),
         V("-(으)려고 했어요", "-(eu)ryeogo haesseoyo", "I was going to", "grammar")],
        G("Intentions that changed",
          "가려고 했어요 · 비가 와서 못 갔어요 · 그 대신에 집에서 일했어요",
          "-(으)려고 했어요 states what you intended before the change, and the outcome needs its own "
          "predicate: 비가 와서 못 갔어요. 대신에 then names the replacement inside one clause — 영화 "
          "대신에 커피, not two 대신에 in a row.",
          [X("주말에 등산을 가려고 했어요.", "jumal-e deungsan-eul garyeogo haesseoyo.", "I was going to go hiking at the weekend."),
           X("비가 와서 못 갔어요.", "bi-ga waseo mot gasseoyo.", "It rained, so I could not go."),
           X("등산 대신에 집에서 영화를 봤어요.", "deungsan daesin-e jib-eseo yeonghwa-reul bwasseoyo.", "Instead of hiking I watched a film at home.")],
          [("계획을 바꾸려고 했어요 바꿨어요.", "계획을 바꾸려고 했어요.", "-(으)려고 했어요 already carries the intention; the action is not added after it."),
           ("대신에 영화를 봤어요 대신에 커피를 마셨어요.", "영화 대신에 커피를 마셨어요.", "대신에 replaces one noun with another inside a single clause.")]),
        [D("미나", "주말에 등산 갔다 왔어요?", "jumal-e deungsan gatda wasseoyo?", "Did you go hiking at the weekend?"),
         D("지훈", "가려고 했는데 비가 와서 못 갔어요.", "garyeogo haetneunde bi-ga waseo mot gasseoyo.", "I was going to, but it rained and I could not."),
         D("미나", "그럼 집에서 쉬었어요?", "geureom jib-eseo swieosseoyo?", "So you rested at home?"),
         D("지훈", "아니요, 등산 대신에 집에서 보고서를 썼어요.", "aniyo, deungsan daesin-e jib-eseo bogoseo-reul sseosseoyo.", "No — instead of hiking I wrote a report at home.")],
        WS("Changed-plan worksheet", [
            T("Say what you were going to do.", ["I was going to go hiking at the weekend.", "I was going to change the plan."],
              ["주말에 등산을 가려고 했어요", "계획을 바꾸려고 했어요"]),
            T("Name the replacement.", ["instead of hiking I watched a film", "it rained, so I could not go"],
              ["등산 대신에 영화를 봤어요", "비가 와서 못 갔어요"]),
        ]))),
    ("B2-U2", "B2-U2-L3", L("회의에서 반대하기",
        "Disagreement at work accepts the point it can accept, then objects: -기는 하지만 carries the "
        "concession and 우려가 있습니다 adds the objection without closing the door.",
        [V("이견", "igyeon", "difference of opinion", "noun"),
         V("우려", "uryeo", "concern", "noun"),
         V("관점", "gwanjeom", "point of view", "noun"),
         V("반대하다", "bandaehada", "to oppose", "verb"),
         V("-기는 하지만", "-gineun hajiman", "it is true that …, but", "grammar")],
        G("Conceding before objecting",
          "그 점은 이해하지만 · 효과가 있기는 하지만 · 다른 관점에서 보면",
          "-기는 하지만 acknowledges the strength of the other position before the objection, which is "
          "why it needs a real contrast after it. 다른 관점에서 보면 shifts the frame instead of "
          "attacking the person, and 우려가 있습니다 states the objection as a risk.",
          [X("그 점은 이해하지만 비용이 문제입니다.", "geu jeom-eun ihaehajiman biyong-i munje-imnida.", "I understand that point, but cost is the problem."),
           X("효과가 있기는 하지만 충분하지 않습니다.", "hyogwa-ga itgineun hajiman chungbunhaji anseumnida.", "It is true that there is an effect, but it is not enough."),
           X("다른 관점에서 보면 위험이 더 큽니다.", "dareun gwanjeom-eseo bomyeon wiheom-i deo keumnida.", "From another point of view the risk is larger.")],
          [("그 의견은 틀렸습니다.", "그 점은 이해하지만 다른 문제가 있습니다.", "In a Korean meeting the conceded point is named first; a flat 틀렸습니다 closes the room."),
           ("반대하기는 하지만 좋습니다.", "반대하기는 하지만 조건이 필요합니다.", "-기는 하지만 demands a genuine contrast after it.")]),
        [D("팀장", "이번 안에 어떻게 생각하십니까?", "ibeon an-e eotteoke saenggakhasimnikka?", "What do you think of this proposal?"),
         D("지훈", "취지는 이해하지만 일정이 우려됩니다.", "chwiji-neun ihaehajiman iljeong-i uryeodoemnida.", "I understand the intent, but the schedule concerns me."),
         D("팀장", "일정이 왜 문제입니까?", "iljeong-i wae munje-imnikka?", "Why is the schedule a problem?"),
         D("지훈", "다른 관점에서 보면 인력이 두 배 필요합니다.", "dareun gwanjeom-eseo bomyeon illyeok-i du bae piryohamnida.", "From another angle it needs twice the staff.")],
        WS("Disagreement worksheet", [
            T("Concede, then object.", ["I understand that point, but cost is the problem.", "it is true that there is an effect, but it is not enough"],
              ["그 점은 이해하지만 비용이 문제입니다", "효과가 있기는 하지만 충분하지 않습니다"]),
            T("Shift the frame.", ["from another point of view the risk is larger", "the schedule concerns me"],
              ["다른 관점에서 보면 위험이 더 큽니다", "일정이 우려됩니다"]),
        ]))),
    ("B2-U3", "B2-U3-L3", L("속담으로 조언하기",
        "A proverb enters a sentence as a quotation: 속담에 …라는 말이 있어요. The metaphor itself is "
        "the predicate, so it takes no second noun, and the advice is finished with -는 게 좋겠어요.",
        [V("속담", "sokdam", "proverb", "noun"),
         V("비유", "biyu", "metaphor", "noun"),
         V("조언", "joeon", "advice", "noun"),
         V("뜻", "tteut", "meaning", "noun"),
         V("-라는 말이 있어요", "-raneun mal-i isseoyo", "there is a saying that", "grammar")],
        G("Quoting a proverb",
          "속담에 티끌 모아 태산이라는 말이 있어요 · 그는 우물 안 개구리예요",
          "A proverb is introduced with -라는 말이 있다. When it is applied to a person the metaphor "
          "stands as the predicate by itself: 그는 우물 안 개구리예요, with no 사람 or other noun added.",
          [X("속담에 티끌 모아 태산이라는 말이 있어요.", "sokdam-e tikkeul moa taesan-iraneun mal-i isseoyo.", "There is a proverb: gather the dust and it becomes a mountain."),
           X("조금씩 모으면 큰돈이 돼요.", "jogeumssik moeumyeon keundon-i dwaeyo.", "If you save a little at a time it becomes a lot."),
           X("그는 우물 안 개구리예요.", "geuneun umul an gaeguri-yeyo.", "He is a frog in a well.")],
          [("티끌 모아 태산이 있다.", "티끌 모아 태산이라는 말이 있어요.", "A proverb is quoted with -라는 말이 있다, not owned by 있다."),
           ("그는 우물 안 개구리입니다 사람입니다.", "그는 우물 안 개구리입니다.", "The metaphor is the whole predicate; a second noun cannot follow it.")]),
        [D("미나", "지훈 씨는 왜 매일 조금씩 저축해요?", "jihun ssi-neun wae maeil jogeumssik jeochukhaeyo?", "Jihun, why do you save a little every day?"),
         D("지훈", "속담에 티끌 모아 태산이라는 말이 있잖아요.", "sokdam-e tikkeul moa taesan-iraneun mal-i itjanayo.", "You know the proverb: gather the dust and it becomes a mountain."),
         D("미나", "그 말은 맞지만 요즘은 물가가 올라요.", "geu mal-eun matjiman yojeum-eun mulga-ga ollayo.", "That is true, but prices are rising these days."),
         D("지훈", "그래도 안 모으면 더 힘들어요. 조금씩 모으는 게 좋겠어요.", "geuraedo an moeumyeon deo himdeureoyo. jogeumssik moeuneun ge jotgesseoyo.", "Even so, it is harder if you save nothing. Better to save a little at a time.")],
        WS("Proverb worksheet", [
            T("Quote a proverb.", ["there is a saying that gathering dust makes a mountain", "he is a frog in a well"],
              ["티끌 모아 태산이라는 말이 있어요", "그는 우물 안 개구리예요"]),
            T("Turn it into advice.", ["it is better to save a little at a time", "if you save a little it becomes a lot"],
              ["조금씩 모으는 게 좋겠어요", "조금씩 모으면 큰돈이 돼요"]),
        ]))),
]

THIRD["C1"] = [
    ("ko-c1-u1", "ko-c1-l7", L("출처를 밝히기",
        "Reported speech changes its ending with the clause it quotes: -다고 for a statement, -라고 "
        "for a copula or a quoted term, -냐고 for a question, -자고 for a suggestion. One source takes "
        "one reporting verb, and 보도체 keeps the quote tighter than the frame around it.",
        [V("출처", "chulcheo", "source, attribution", "noun"),
         V("인용", "inyong", "quotation", "noun"),
         V("주장하다", "jujanghada", "to assert, to argue", "verb"),
         V("지적하다", "jijeokhada", "to point out", "verb"),
         V("-다고 하다", "-dago hada", "to say that (statement)", "grammar")],
        G("Choosing the quotation ending",
          "늘었다고 밝혔다 · 효과적이라고 지적했다 · 가능하냐고 물었다 · 검토하자고 제안했다",
          "The quote keeps the plain form of its own clause and then takes the ending that matches its "
          "type: -다고 for statements, -라고 after 이다 or a quoted word, -냐고 for questions, -자고 for "
          "suggestions. 밝히다, 지적하다 and 주장하다 are the frames that carry it in 보도체.",
          [X("보고서는 수출이 늘었다고 밝혔다.", "bogoseo-neun suchul-i neureotdago balkyeotda.", "The report stated that exports had risen."),
           X("전문가는 정책이 효과적이라고 지적했다.", "jeonmun-ga-neun jeongchaek-i hyogwajeogirago jijeokhaetda.", "The expert pointed out that the policy was effective."),
           X("기자가 가능하냐고 물었다.", "gija-ga ganeunghan-nyago mureotda.", "The reporter asked whether it was possible.")],
          [("보고서는 늘었다고 밝혔습니다 늘어났습니다.", "보고서는 수출이 늘었다고 밝혔습니다.", "The quoted clause carries its own ending; it is not repeated after the frame."),
           ("전문가는 효과적이었다고 지적했다고 밝혔다.", "전문가는 효과적이었다고 지적했다.", "One source takes one reporting verb — 지적하다 and 밝히다 are not stacked.")]),
        [D("기자", "이번 발표의 핵심이 무엇입니까?", "ibeon balpyo-ui haeksim-i mueosimnikka?", "What is the core of this announcement?"),
         D("연구자", "수출이 늘었다고 밝혔지만 원인은 다릅니다.", "suchul-i neureotdago balkyeotjiman wonin-eun dareumnida.", "It stated that exports rose, but the cause is different."),
         D("기자", "그러면 정책 효과는 없었다고 보십니까?", "geureomyeon jeongchaek hyogwa-neun eopseotdago bosimnikka?", "Then do you think the policy had no effect?"),
         D("연구자", "없었다고 단정하기는 어렵습니다. 근거가 더 필요하다고 봅니다.", "eopseotdago danjeonghagineun eoryeopseumnida. geun-geo-ga deo piryohadago bomnida.", "It is hard to state that it had none. I think more evidence is needed.")],
        WS("Attribution worksheet", [
            T("Quote a statement.", ["the report stated that exports had risen", "the expert pointed out that the policy was effective"],
              ["보고서는 수출이 늘었다고 밝혔다", "전문가는 정책이 효과적이라고 지적했다"]),
            T("Quote a question and a suggestion.", ["the reporter asked whether it was possible", "they proposed to review it"],
              ["기자가 가능하냐고 물었다", "검토하자고 제안했다"]),
        ]))),
    ("ko-c1-u2", "ko-c1-l8", L("상충하는 자료를 다루기",
        "Conflicting figures are held together with the right connector: 반면에 for a contrast inside "
        "one sentence, 한편 for a change of subject, 다만 for a limit, and -므로 when the conflict is "
        "the reason for caution.",
        [V("상충하다", "sangchunghada", "to conflict, to clash", "verb"),
         V("반면에", "banmyeon-e", "on the other hand", "connector"),
         V("유보하다", "yubohada", "to hold back, to reserve", "verb"),
         V("격차", "gyeokcha", "gap, disparity", "noun"),
         V("근거", "geun-geo", "evidence, grounds", "noun")],
        G("Connectors for a contradiction",
          "수도권은 늘어난 반면에 지방은 줄었다 · 한편 다른 조사에서는 · 다만 결론은 유보한다",
          "반면에 puts two clauses of the same sentence in opposition; 한편 opens a new sentence about a "
          "different source; 다만 limits what was just claimed. A reason and its consequence take -므로 "
          "or -기 때문에, never 그리고.",
          [X("수도권은 늘어난 반면에 지방은 줄었다.", "sudogwon-eun neureonan banmyeon-e jibang-eun jureotda.", "The capital region rose, while the provinces fell."),
           X("한편 다른 조사에서는 반대 결과가 나왔다.", "hanpyeon dareun josa-eseo-neun bandae gyeolgwa-ga nawatda.", "Meanwhile a different survey produced the opposite result."),
           X("자료가 상충하므로 결론을 유보한다.", "jaryo-ga sangchunghameuro gyeollon-eul yubohanda.", "The data conflict, so the conclusion is held back.")],
          [("자료가 다릅니다. 그리고 결론을 내릴 수 없습니다.", "자료가 상충하므로 결론을 내리기 어렵습니다.", "A reason and its result are joined by -므로 or -기 때문에, not by 그리고."),
           ("두 자료는 반대입니다.", "두 자료는 서로 상충합니다.", "반대 is a person's stance; data conflict with 상충하다.")]),
        [D("동료", "두 조사의 결과가 다릅니까?", "du josa-ui gyeolgwa-ga dareumnikka?", "Do the two surveys disagree?"),
         D("분석자", "수도권은 늘어난 반면에 지방은 줄었습니다.", "sudogwon-eun neureonan banmyeon-e jibang-eun jureosseumnida.", "The capital region rose, while the provinces fell."),
         D("동료", "그러면 어느 쪽을 믿어야 합니까?", "geureomyeon eoneu jjok-eul mideo-ya hamnikka?", "Then which should we believe?"),
         D("분석자", "자료가 상충하므로 결론을 유보하고 표본을 더 봐야 합니다.", "jaryo-ga sangchunghameuro gyeollon-eul yubohago pyobon-eul deo bwaya hamnida.", "Because the data conflict, we should hold the conclusion and look at more samples.")],
        WS("Conflicting-data worksheet", [
            T("Contrast two results.", ["the capital region rose, while the provinces fell", "the data conflict"],
              ["수도권은 늘어난 반면에 지방은 줄었다", "자료가 서로 상충합니다"]),
            T("State a cautious conclusion.", ["the data conflict, so I hold the conclusion", "a different survey produced the opposite result"],
              ["자료가 상충하므로 결론을 유보한다", "다른 조사에서는 반대 결과가 나왔다"]),
        ]))),
    ("ko-c1-u3", "ko-c1-l9", L("완곡어와 책임",
        "A hedged claim is not a vague one: -ㄴ 것으로 보인다 reports what the evidence shows, -ㄹ "
        "가능성이 있다 measures the chance, and -기 어렵다 refuses a conclusion. Responsibility is "
        "named separately with 에게 있다.",
        [V("완곡하다", "wangokhada", "to be indirect, to be softened", "verb"),
         V("책임", "chaegim", "responsibility", "noun"),
         V("소재", "sojae", "where something lies", "noun"),
         V("가능성", "ganeungseong", "possibility", "noun"),
         V("-ㄴ 것으로 보이다", "-n geoseuro boida", "it appears that", "grammar")],
        G("Measuring a claim",
          "실패한 것으로 보인다 · 실패했을 가능성이 있다 · 실패했다고 보기 어렵다",
          "The three frames weaken a claim in different directions: -ㄴ 것으로 보인다 keeps the "
          "evidence in front, -ㄹ 가능성이 있다 keeps a share of doubt, -기 어렵다 refuses agreement. "
          "They attach to the modifier form of the verb, and a hedged sentence never ends in a second "
          "predicate.",
          [X("정책이 실패한 것으로 보인다.", "jeongchaek-i silpaehan geoseuro boida.", "The policy appears to have failed."),
           X("효과가 있었을 가능성도 있다.", "hyogwa-ga isseosseul ganeungseong-do itda.", "There is also a possibility that it worked."),
           X("책임은 담당자에게 있다.", "chaegim-eun damdangja-ege itda.", "Responsibility lies with the person in charge.")],
          [("정책이 실패했습니다 것으로 보입니다.", "정책이 실패한 것으로 보입니다.", "The hedge takes the modifier form 실패한, not a finished sentence."),
           ("책임이 있습니다 담당자에게 있습니다.", "책임은 담당자에게 있습니다.", "One topic, one predicate — 담당자에게 있습니다 completes the sentence.")]),
        [D("기자", "정책이 실패했다고 보십니까?", "jeongchaek-i silpaehaetdago bosimnikka?", "Do you think the policy failed?"),
         D("연구자", "실패했다고 보기 어렵습니다. 다만 효과가 제한적이었을 가능성은 있습니다.", "silpaehaetdago bogi eoryeopseumnida. dameot hyogwa-ga jehantjeogieosseul ganeungseong-eun isseumnida.", "It is hard to say it failed. There is, however, a possibility the effect was limited."),
         D("기자", "그러면 책임은 어디에 있습니까?", "geureomyeon chaegim-eun eodi-e isseumnikka?", "Then where does responsibility lie?"),
         D("연구자", "책임은 집행 담당자에게 있고, 판단은 자료가 쌓인 뒤에 해야 합니다.", "chaegim-eun jiphaeng damdangja-ege itgo, pandan-eun jaryo-ga ssain dwie haeya hamnida.", "Responsibility lies with those who carried it out; judgement should wait until the data accumulate.")],
        WS("Hedging worksheet", [
            T("Soften a claim.", ["the policy appears to have failed", "there is a possibility that it worked"],
              ["정책이 실패한 것으로 보인다", "효과가 있었을 가능성이 있다"]),
            T("Place responsibility.", ["responsibility lies with the person in charge", "it is hard to conclude yet"],
              ["책임은 담당자에게 있습니다", "결론을 내리기 어렵습니다"]),
        ]))),
]

THIRD["C2"] = [
    ("ko-c2-u1", "ko-c2-l7", L("전제를 드러내기",
        "Every question carries a presupposition. To make one visible the frame is 전제가 깔려 있다, "
        "to deny it the verb is 부정하다 with the quoted -라고 form, and -(으)ㄴ 셈이다 claims an "
        "equivalence only when none is being smuggled in.",
        [V("전제", "jeonje", "presupposition, premise", "noun"),
         V("함의", "hamui", "implication", "noun"),
         V("부정하다", "bujeonghada", "to deny", "verb"),
         V("드러내다", "deureonaeda", "to bring out, to expose", "verb"),
         V("-(으)ㄴ 셈이다", "-(eu)n sem-ida", "it amounts to, it is as good as", "grammar")],
        G("Surfacing what a sentence assumes",
          "이 질문에는 전제가 깔려 있다 · 그는 아니라고 부정했다 · 다른 셈이다",
          "A presupposition is not asserted, so it is named rather than argued: 전제가 깔려 있다. "
          "Denial takes the quote form -라고 directly after 부정하다. 셈이다 claims that two things "
          "amount to the same, and it is exactly where an argument smuggles in a conclusion.",
          [X("이 질문에는 전제가 깔려 있다.", "i jilmun-e-neun jeonje-ga kkallyeo itda.", "There is a presupposition embedded in this question."),
           X("그는 그렇게 하지 않았다고 부정했다.", "geuneun geureoke haji anatdago bujeonghaetda.", "He denied having done so."),
           X("그가 왔다는 것은 동의한 셈이다.", "geu-ga watdaneun geoseun dong-uihan sem-ida.", "That he came amounts to agreement.")],
          [("이 질문은 전제가 있습니다.", "이 질문에는 전제가 깔려 있습니다.", "A presupposition sits inside a question: 에는 …이 깔려 있다."),
           ("그는 부정했습니다 아니라고 말했습니다.", "그는 아니라고 부정했습니다.", "부정하다 takes the quoted -라고 form directly, not a second clause.")]),
        [D("편집자", "이 질문에는 어떤 전제가 깔려 있습니까?", "i jilmun-e-neun eotteon jeonje-ga kkallyeo isseumnikka?", "What presupposition is embedded in this question?"),
         D("검토자", "정책이 이미 실패했다는 전제입니다.", "jeongchaek-i imi silpaehaetdaneun jeonje-imnida.", "That the policy has already failed."),
         D("편집자", "그러면 실패를 부정하는 대신 전제를 지적할 수 있겠네요.", "geureomyeon silpae-reul bujeonghaneun daesin jeonje-reul jijeokhal su itgetneyo.", "Then instead of denying the failure we can point at the presupposition."),
         D("검토자", "그렇게 쓰면 논쟁이 사실 문제로 좁혀집니다.", "geureoke sseumyeon nonjaeng-i sasil munje-ro jophyeojimnida.", "Written that way the argument narrows to the facts.")],
        WS("Presupposition worksheet", [
            T("Name the premise.", ["there is a presupposition embedded in this question", "that he came amounts to agreement"],
              ["이 질문에는 전제가 깔려 있다", "그가 왔다는 것은 동의한 셈이다"]),
            T("Deny exactly.", ["he denied having done so", "the premise is that the policy failed"],
              ["그는 그렇게 하지 않았다고 부정했다", "정책이 이미 실패했다는 전제입니다"]),
        ]))),
    ("ko-c2-u2", "ko-c2-l8", L("문체 변환: 보도체와 에세이체",
        "The same content reads differently in three registers: 보도체 ends in -다 and reports, "
        "에세이체 ends in -ㄴ다 and reflects, and 격식체 uses -습니다 for anything spoken. Conversion is "
        "systematic — the clause endings move, the argument does not.",
        [V("문체", "munche", "style, register", "noun"),
         V("보도체", "bodoche", "newspaper register", "noun"),
         V("에세이체", "eseiche", "essay register", "noun"),
         V("격식체", "gyeoksikche", "formal register", "noun"),
         V("변환", "byeonhwan", "conversion, shift", "noun")],
        G("Moving between registers",
          "수출이 늘었다 · 수출이 늘었습니다 · 수출이 늘어난 것으로 보인다",
          "보도체 keeps the plain -다 ending and joins clauses with -고, -으나 and -며. 에세이체 adds "
          "the writer's stance through -ㄴ 것으로 보인다 and -(으)ㄴ 셈이다. 격식체 moves every ending "
          "into -습니다/-습니까, and mixing the three inside one paragraph is the commonest failure.",
          [X("수출이 늘었으나 지역 격차도 컸다.", "suchul-i neureot-euna jiyeok gyeokcha-do keotda.", "Exports rose, but the regional gap also widened."),
           X("수출이 늘었습니다. 지역 격차도 컸습니다.", "suchul-i neureotseumnida. jiyeok gyeokcha-do keotseumnida.", "Exports rose. The regional gap also widened."),
           X("수출이 늘어난 것으로 보인다.", "suchul-i neureonan geoseuro boida.", "Exports appear to have risen.")],
          [("그는 말했다. 그리고 갔다.", "그는 말하고 떠났다.", "보도체 joins its clauses with -고, not with a spoken 그리고."),
           ("본고에서는 분석한다. 그리고 결론을 내린다. 이다.", "본고는 분석하고 결론을 내린다.", "The -ㄴ다 ending chains with -고; 이다 cannot stand as a sentence of its own here.")]),
        [D("편집자", "이 문장을 보도체로 고쳐 주세요.", "i munjang-eul bodoche-ro gochyeo juseyo.", "Please turn this sentence into report style."),
         D("기자", "수출이 늘었습니다. 지역 격차도 컸습니다.", "suchul-i neureotseumnida. jiyeok gyeokcha-do keotseumnida.", "Exports rose. The regional gap also widened."),
         D("편집자", "격식체는 인터뷰이고, 기사에는 보도체를 씁니다.", "gyeoksikche-neun intyebu-igo, gisa-e-neun bodoche-reul sseumnida.", "That is the interview register; an article uses report style."),
         D("기자", "수출이 늘었으나 지역 격차도 컸다. 이렇게 고치겠습니다.", "suchul-i neureot-euna jiyeok gyeokcha-do keotda. ireoke gochigetseumnida.", "Exports rose, but the regional gap also widened. I will correct it that way.")],
        WS("Register worksheet", [
            T("Convert to report style.", ["exports rose, and the regional gap also widened", "he said and left"],
              ["수출이 늘었고 지역 격차도 컸다", "그는 말하고 떠났다"]),
            T("Convert to formal speech.", ["exports appear to have risen", "the report states that exports rose"],
              ["수출이 늘어난 것으로 보입니다", "보고서는 수출이 늘었다고 밝혔습니다"]),
        ]))),
    ("ko-c2-u3", "ko-c2-l9", L("권위와 겸손: 인용의 태도",
        "A claim can be placed at four distances: 단정한다 states it, -고 본다 holds it, -ㄹ 여지가 "
        "있다 allows it, and -에 따르면 hands it to somebody else. Korean academic prose prefers the "
        "middle two.",
        [V("견해", "gyeonhae", "view, opinion", "noun"),
         V("필자", "pilja", "the writer (of the piece)", "noun"),
         V("단정하다", "danjeonghada", "to assert flatly", "verb"),
         V("여지", "yeoji", "room, margin (for doubt)", "noun"),
         V("-고 보다", "-go boda", "to hold the view that", "grammar")],
        G("Distancing a claim",
          "필자는 …라고 본다 · 반대할 여지가 있다 · …에 따르면",
          "-고 본다 keeps the claim as the writer's own position, 여지가 있다 leaves room for the "
          "opposite, and 에 따르면 attributes the claim to somebody else entirely. 단정한다 is reserved "
          "for what the evidence forces, and one clause carries one reporting verb.",
          [X("필자는 이 견해에 반대할 여지가 있다고 본다.", "pilja-neun i gyeonhae-e bandaehal yeoji-ga itdago bonda.", "The writer holds that this view leaves room for objection."),
           X("다른 연구자에 따르면 결론이 다르다.", "dareun yeon-gu-ja-e ttareumyeon gyeollon-i dareuda.", "According to other researchers the conclusion differs."),
           X("자료는 이 결론을 지지한다.", "jaryo-neun i gyeollon-eul jijihanda.", "The data support this conclusion.")],
          [("이 견해는 틀렸습니다라고 본다.", "이 견해는 틀렸다고 본다.", "Quotation after a plain clause takes -다고, not 습니다라고."),
           ("그는 옳다고 봅니다고 합니다.", "그는 옳다고 봅니다.", "One reporting verb per clause.")]),
        [D("검토자", "이 결론을 단정해도 됩니까?", "i gyeollon-eul danjeonghaedo doemnikka?", "May we assert this conclusion?"),
         D("저자", "아직은 이르다고 봅니다. 반대할 여지가 있습니다.", "ajigeun ireudago bomnida. bandaehal yeoji-ga isseumnida.", "I think it is too early. There is room to object."),
         D("검토자", "그러면 누구의 견해로 밝힙니까?", "geureomyeon nugu-ui gyeonhae-ro balkimnikka?", "Then whose view do we attribute it to?"),
         D("저자", "다른 연구자에 따르면 반대 결과도 있으므로 양쪽을 함께 적겠습니다.", "dareun yeon-gu-ja-e ttareumyeon bandae gyeolgwa-do isseumeuro yangjjok-eul hamkke jeokgetseumnida.", "According to other researchers there are opposite results too, so I will write both.")],
        WS("Distancing worksheet", [
            T("Hold a view.", ["the writer holds that this view leaves room for objection", "there is room to object"],
              ["필자는 이 견해에 반대할 여지가 있다고 본다", "반대할 여지가 있습니다"]),
            T("Attribute to others.", ["according to other researchers the conclusion differs", "the data support this conclusion"],
              ["다른 연구자에 따르면 결론이 다르다", "자료는 이 결론을 지지한다"]),
        ]))),
]

HALFSTEPS["A1+"] = {
    "title": "Korean A1+ — A day and a call",
    "native": NATIVE,
    "goals": [
        "Tell the time and describe a day hour by hour",
        "Answer the phone, take a message and text back",
        "Invite somebody, accept, and decline without giving offence",
    ],
    "units": [
        {"id": "A1+-U1", "title": "하루 일과", "lessons": [
            L("몇 시에 일어나요?",
              "A daily routine is a list of verbs on a clock: 일어나요, 씻어요, 먹어요, 가요. The hour "
              "takes the Sino-Korean numbers and the particle 에, and it normally comes before the verb.",
              [V("일어나다", "ireonada", "to get up", "verb"),
               V("씻다", "ssitda", "to wash", "verb"),
               V("출근하다", "chulgeunhada", "to go to work", "verb"),
               V("점심", "jeomsim", "lunch, midday", "noun"),
               V("저녁", "jeonyeok", "evening, dinner", "noun")],
              G("Telling the hour",
                "일곱 시에 일어나요 · 아홉 시에 출근해요 · 몇 시에 자요?",
                "Hours use the Sino-Korean numbers with the counter 시: 한 시, 두 시, 일곱 시. A clock "
                "time takes 에 and stands before the verb; 아침, 점심 and 저녁 do not take 에 at all.",
                [X("아침 일곱 시에 일어나요.", "achim ilgop si-e ireonayo.", "I get up at seven in the morning."),
                 X("아홉 시에 출근해요.", "ahop si-e chulgeunhaeyo.", "I go to work at nine."),
                 X("보통 열한 시에 자요.", "botong yeolhan si-e jayo.", "I usually go to bed at eleven.")],
                [("아침에 일어나요 일곱 시에.", "아침 일곱 시에 일어나요.", "The hour comes before the verb, not after it."),
                 ("저녁에에 밥을 먹어요.", "저녁에 밥을 먹어요.", "One 에 is enough; 아침, 점심 and 저녁 take it once.")]),
              [D("미나", "보통 몇 시에 일어나요?", "botong myeot si-e ireonayo?", "What time do you usually get up?"),
               D("지훈", "일곱 시에 일어나요. 그리고 아홉 시에 출근해요.", "ilgop si-e ireonayo. geurigo ahop si-e chulgeunhaeyo.", "At seven. And I go to work at nine."),
               D("미나", "점심은 어디에서 먹어요?", "jeomsim-eun eodi-eseo meogeoyo?", "Where do you have lunch?"),
               D("지훈", "회사 근처에서 먹어요. 보통 김밥을 먹어요.", "hoesa geuncheo-eseo meogeoyo. botong gimbab-eul meogeoyo.", "Near the office. Usually gimbap.")],
              WS("Routine worksheet", [
                  T("Say the hour.", ["I get up at seven.", "I go to work at nine."],
                    ["일곱 시에 일어나요", "아홉 시에 출근해요"]),
                  T("Ask the question.", ["what time do you sleep?", "where do you have lunch?"],
                    ["몇 시에 자요?", "점심은 어디에서 먹어요?"]),
              ])),
            L("주말에는 뭐 해요?",
              "Frequency words sit in front of the verb and shape the whole answer: 항상, 보통, 자주, "
              "가끔, 거의 안. The contrast between weekday and weekend is marked with 는.",
              [V("자주", "jaju", "often", "adverb"),
               V("가끔", "gakkeum", "sometimes", "adverb"),
               V("보통", "botong", "usually", "adverb"),
               V("운동하다", "undonghada", "to exercise", "verb"),
               V("빨래하다", "ppallaehada", "to do the laundry", "verb")],
              G("How often",
                "주말에는 자주 운동해요 · 가끔 영화를 봐요 · 거의 안 나가요",
                "Frequency adverbs are placed immediately before the verb, and 거의 needs a negative "
                "after it. The particle 는 on 주말에는 contrasts the weekend with the rest of the week.",
                [X("주말에는 자주 운동해요.", "jumal-e-neun jaju undonghaeyo.", "At the weekend I often exercise."),
                 X("가끔 영화를 봐요.", "gakkeum yeonghwa-reul bwayo.", "Sometimes I watch a film."),
                 X("요즘은 거의 안 나가요.", "yojeum-eun geoui an nagayo.", "These days I hardly go out.")],
                [("자주 운동해요 주말에는.", "주말에는 자주 운동해요.", "The time phrase opens the sentence it belongs to."),
                 ("가끔 안 나가요.", "가끔 나가요.", "가끔 is positive; a negative sentence takes 거의 안 or 별로.")]),
              [D("지훈", "주말에는 보통 뭐 해요?", "jumal-e-neun botong mwo haeyo?", "What do you usually do at the weekend?"),
               D("미나", "토요일에는 빨래하고 청소해요.", "toyoil-e-neun ppallaehago cheongsohaeyo.", "On Saturday I do the laundry and clean."),
               D("지훈", "일요일에도 일해요?", "iryoil-e-do ilhaeyo?", "Do you work on Sunday too?"),
               D("미나", "아니요, 일요일에는 거의 안 나가고 집에서 쉬어요.", "aniyo, iryoil-e-neun geoui an nagago jib-eseo swieoyo.", "No, on Sunday I hardly go out and rest at home.")],
              WS("Weekend worksheet", [
                  T("Answer with frequency.", ["I often exercise at the weekend.", "sometimes I watch a film."],
                    ["주말에는 자주 운동해요", "가끔 영화를 봐요"]),
                  T("Use the contrast.", ["on Sunday I hardly go out", "on Saturday I do the laundry"],
                    ["일요일에는 거의 안 나가요", "토요일에는 빨래해요"]),
              ])),
            L("몇 시까지 해요?",
              "Opening hours are asked with 몇 시부터 몇 시까지. 부터 marks the start, 까지 the end, and "
              "both can stand alone: 아홉 시부터, 여섯 시까지.",
              [V("영업시간", "yeongeopsigan", "business hours", "noun"),
               V("열다", "yeolda", "to open", "verb"),
               V("닫다", "datda", "to close", "verb"),
               V("부터", "buteo", "from (a time)", "particle"),
               V("까지", "kkaji", "until (a time)", "particle")],
              G("From and until",
                "몇 시부터 몇 시까지 해요? · 아홉 시부터 여섯 시까지 · 일요일에는 쉬어요",
                "부터 and 까지 can be used as a pair or separately, and they attach directly to the "
                "time. A closed day is stated with a plain negative sentence, not with 까지.",
                [X("몇 시부터 몇 시까지 해요?", "myeot si-buteo myeot si-kkaji haeyo?", "From what time until what time are you open?"),
                 X("아홉 시부터 여섯 시까지 해요.", "ahop si-buteo yeoseot si-kkaji haeyo.", "We are open from nine until six."),
                 X("일요일에는 문을 닫아요.", "iryoil-e-neun mun-eul dadayo.", "We close on Sundays.")],
                [("몇 시까지부터 해요?", "몇 시부터 해요?", "부터 marks the start on its own; it does not follow 까지."),
                 ("일요일까지 쉬어요.", "일요일에는 쉬어요.", "까지 is a stretch of time; a recurring closed day takes 에는.")]),
              [D("미나", "이 가게는 몇 시부터 몇 시까지 해요?", "i gage-neun myeot si-buteo myeot si-kkaji haeyo?", "From when until when is this shop open?"),
               D("점원", "아홉 시부터 여섯 시까지예요.", "ahop si-buteo yeoseot si-kkajiyeyo.", "From nine until six."),
               D("미나", "주말에도 열어요?", "jumal-e-do yeoreoyo?", "Are you open at the weekend too?"),
               D("점원", "토요일에는 열고 일요일에는 문을 닫아요.", "toyoil-e-neun yeolgo iryoil-e-neun mun-eul dadayo.", "We open on Saturday and close on Sunday.")],
              WS("Opening-hours worksheet", [
                  T("Give the hours.", ["from nine until six", "from ten until eight"],
                    ["아홉 시부터 여섯 시까지", "열 시부터 여덟 시까지"]),
                  T("State the closed day.", ["we close on Sunday", "are you open at the weekend too?"],
                    ["일요일에는 문을 닫아요", "주말에도 열어요?"]),
              ])),
        ]},
        {"id": "A1+-U2", "title": "전화와 문자", "lessons": [
            L("여보세요?",
              "A phone call opens with 여보세요, which is used only on the phone. The caller identifies "
              "itself, and 잠깐만요 buys a moment.",
              [V("여보세요", "yeoboseyo", "hello (on the phone)", "phrase"),
               V("전화하다", "jeonhwahada", "to call", "verb"),
               V("받다", "batda", "to receive", "verb"),
               V("잠깐만요", "jamkkanmanyo", "one moment, please", "phrase"),
               V("누구세요?", "nuguseyo?", "who is it?", "phrase")],
              G("On the phone",
                "여보세요? · 지훈 씨 계세요? · 잠깐만요 · 바꿔 드릴게요",
                "여보세요 belongs to the phone and to nothing else. To ask for a person use 계세요, and "
                "to pass the phone on use the humble 바꿔 드리다.",
                [X("여보세요, 지훈 씨 계세요?", "yeoboseyo, jihun ssi gyeseyo?", "Hello, is Jihun there?"),
                 X("잠깐만요. 바꿔 드릴게요.", "jamkkanmanyo. bakkwo deurilgeyo.", "One moment. I will pass you over."),
                 X("지금 통화 중이에요.", "jigeum tonghwa jung-ieyo.", "He is on the phone right now.")],
                [("여보세요, 안녕하세요 선생님.", "여보세요, 지훈 씨 계세요?", "On the phone 여보세요 does the greeting; the errand follows immediately."),
                 ("전화를 받아요 있어요.", "전화를 받아요.", "받다 is already the whole verb of answering.")]),
              [D("미나", "여보세요?", "yeoboseyo?", "Hello?"),
               D("지훈", "안녕하세요, 지훈입니다. 미나 씨 계세요?", "annyeonghaseyo, jihun-imnida. mina ssi gyeseyo?", "Hello, this is Jihun. Is Mina there?"),
               D("미나", "네, 잠깐만요. 지금 바꿔 드릴게요.", "ne, jamkkanmanyo. jigeum bakkwo deurilgeyo.", "Yes, one moment. I will pass you over."),
               D("지훈", "감사합니다.", "gamsahamnida.", "Thank you.")],
              WS("Phone worksheet", [
                  T("Open a call.", ["hello (on the phone)", "is Jihun there?"],
                    ["여보세요?", "지훈 씨 계세요?"]),
                  T("Hold and pass on.", ["one moment, please", "I will pass you over"],
                    ["잠깐만요", "바꿔 드릴게요"]),
              ])),
            L("문자를 보내요",
              "Texting has its own short verbs: 보내다, 받다, 답장을 하다, 읽다. A message that arrives "
              "late is answered with 늦게 답장해서 미안합니다.",
              [V("문자", "munja", "text message", "noun"),
               V("보내다", "bonaeda", "to send", "verb"),
               V("답장", "dapjang", "reply", "noun"),
               V("읽다", "ikda", "to read", "verb"),
               V("나중에", "najung-e", "later", "adverb")],
              G("Sending and replying",
                "문자를 보냈어요 · 답장이 없었어요 · 늦게 답장해서 미안해요",
                "The message is the object of 보내다 and 답장 is the object of 하다. A reason with -아서/"
                "어서 joins the lateness to the apology, and 나중에 stands before the verb it modifies.",
                [X("문자를 보냈어요.", "munja-reul bonaesseoyo.", "I sent a text."),
                 X("아직 답장이 없어요.", "ajik dapjang-i eopseoyo.", "There is no reply yet."),
                 X("나중에 답장할게요.", "najung-e dapjanghalgeyo.", "I will reply later.")],
                [("답장을 보냈어요 해요.", "답장을 보냈어요.", "답장 takes one verb: 보내다 or 하다, not both."),
                 ("늦게 답장해서 미안합니다 요.", "늦게 답장해서 미안합니다.", "One ending per sentence.")]),
              [D("지훈", "어제 문자 보냈어요?", "eoje munja bonaesseoyo?", "Did you send the text yesterday?"),
               D("미나", "네, 보냈는데 답장이 없었어요.", "ne, bonaetneunde dapjang-i eopseosseoyo.", "Yes, I sent it, but there was no reply."),
               D("지훈", "미안해요, 늦게 읽었어요.", "mianhaeyo, neujge ilgeosseoyo.", "Sorry, I read it late."),
               D("미나", "괜찮아요. 나중에 답장해 주세요.", "gwaenchanayo. najung-e dapjanghae juseyo.", "It is fine. Reply when you can.")],
              WS("Text worksheet", [
                  T("Send and receive.", ["I sent a text.", "there is no reply yet."],
                    ["문자를 보냈어요", "아직 답장이 없어요"]),
                  T("Apologise for the delay.", ["I read it late, sorry", "I will reply later"],
                    ["늦게 읽어서 미안해요", "나중에 답장할게요"]),
              ])),
            L("메시지를 남겨요",
              "When the person is out the call becomes a message: 다시 전화해 달라고 전해 주세요. The "
              "promise to call back takes -(으)ㄹ게요.",
              [V("메시지", "mesiji", "message", "noun"),
               V("남기다", "namgida", "to leave (a message)", "verb"),
               V("통화", "tonghwa", "a call, talking on the phone", "noun"),
               V("전하다", "jeonhada", "to pass on (a message)", "verb"),
               V("다시", "dasi", "again", "adverb")],
              G("Leaving a message",
                "메시지를 남길게요 · 다시 전화해 달라고 전해 주세요 · 나중에 다시 걸게요",
                "A request passed on to a third person takes -아/어 달라고 하다. The promise to do "
                "something for the listener takes -(으)ㄹ게요, which is softer than -(으)ㄹ 거예요.",
                [X("메시지를 남길게요.", "mesiji-reul namgilgeyo.", "I will leave a message."),
                 X("다시 전화해 달라고 전해 주세요.", "dasi jeonhwahae dallago jeonhae juseyo.", "Please tell him to call back."),
                 X("나중에 다시 걸게요.", "najung-e dasi geolgeyo.", "I will ring again later.")],
                [("다시 전화해 주세요 달라고 했어요.", "다시 전화해 달라고 했어요.", "A request made on someone else's behalf takes -달라고, not -주세요."),
                 ("메시지를 남겨요 할게요.", "메시지를 남길게요.", "One verb per sentence: 남기다 already means leave it.")]),
              [D("지훈", "여보세요, 미나 씨 계세요?", "yeoboseyo, mina ssi gyeseyo?", "Hello, is Mina there?"),
               D("동료", "지금 자리에 없어요. 메시지를 남기시겠어요?", "jigeum jari-e eopseoyo. mesiji-reul namgisigesseoyo?", "She is not at her desk. Would you like to leave a message?"),
               D("지훈", "네, 다시 전화해 달라고 전해 주세요.", "ne, dasi jeonhwahae dallago jeonhae juseyo.", "Yes, please tell her to call back."),
               D("동료", "알겠습니다. 그렇게 전할게요.", "algesseumnida. geureoke jeonhalgeyo.", "Understood. I will pass that on.")],
              WS("Message worksheet", [
                  T("Leave a message.", ["I will leave a message.", "please tell her to call back"],
                    ["메시지를 남길게요", "다시 전화해 달라고 전해 주세요"]),
                  T("Promise to ring.", ["I will ring again later", "she is not at her desk"],
                    ["나중에 다시 걸게요", "지금 자리에 없어요"]),
              ])),
        ]},
        {"id": "A1+-U3", "title": "초대와 방문", "lessons": [
            L("우리 집에 놀러 오세요",
              "An invitation is 놀러 오세요 or 같이 …ㄹ까요? and the answer names the day. A visit "
              "brings something small: 과일이나 케이크면 충분해요.",
              [V("초대하다", "chodaehada", "to invite", "verb"),
               V("놀러 오다", "nolleo oda", "to come over", "phrase"),
               V("손님", "sonnim", "guest", "noun"),
               V("준비하다", "junbihada", "to prepare", "verb"),
               V("선물", "seonmul", "gift", "noun")],
              G("Inviting",
                "우리 집에 놀러 오세요 · 토요일 어때요? · 뭘 가져갈까요?",
                "The invitation is a request form with a soft ending, and the reply can propose a day. "
                "Asking what to bring takes the plain -(으)ㄹ까요? with a neutral object.",
                [X("우리 집에 놀러 오세요.", "uri jib-e nolleo oseyo.", "Come over to my place."),
                 X("토요일 오후 어때요?", "toyoil ohu eottaeyo?", "How about Saturday afternoon?"),
                 X("뭘 가져갈까요?", "mwol gajyeogalkkayo?", "What shall I bring?")],
                [("우리 집에 오세요 놀러.", "우리 집에 놀러 오세요.", "놀러 comes directly before 오다."),
                 ("선물을 사요 가져갈까요?", "선물을 가져갈까요?", "One verb: 사다 buys it, 가져가다 brings it.")]),
              [D("미나", "이번 주말에 우리 집에 놀러 오세요.", "ibeon jumal-e uri jib-e nolleo oseyo.", "Come over to my place this weekend."),
               D("지훈", "좋아요. 토요일 오후 어때요?", "joayo. toyoil ohu eottaeyo?", "Great. How about Saturday afternoon?"),
               D("미나", "좋아요. 뭘 가져갈까요?", "joayo. mwol gajyeogalkkayo?", "Fine. What shall I bring?"),
               D("지훈", "아무것도 필요 없어요. 과일이면 충분해요.", "amugeotdo piryo eopseoyo. gwa-il-imyeon chungbunhaeyo.", "Nothing is needed. Fruit is plenty.")],
              WS("Invitation worksheet", [
                  T("Invite.", ["come over to my place", "how about Saturday afternoon?"],
                    ["우리 집에 놀러 오세요", "토요일 오후 어때요?"]),
                  T("Ask and answer.", ["what shall I bring?", "fruit is plenty"],
                    ["뭘 가져갈까요?", "과일이면 충분해요"]),
              ])),
            L("미안하지만 못 가요",
              "A refusal keeps the relationship: 미안하지만, 그날은 어려워요, 다음에 꼭 갈게요. The hard "
              "part is said first and the alternative last.",
              [V("미안하지만", "mianhajiman", "I am sorry, but", "phrase"),
               V("어렵다", "eoryeopda", "to be difficult", "adjective"),
               V("다음에", "daeum-e", "next time", "adverb"),
               V("꼭", "kkok", "without fail, surely", "adverb"),
               V("사정", "sajeong", "circumstances", "noun")],
              G("Declining politely",
                "미안하지만 그날은 어려워요 · 사정이 있어서 못 가요 · 다음에 꼭 갈게요",
                "The refusal opens with 미안하지만 or 죄송하지만 and states the difficulty without a "
                "reason; the reason, if given at all, is brief. The promise for next time closes the "
                "message and takes 꼭.",
                [X("미안하지만 그날은 어려워요.", "mianhajiman geunal-eun eoryeowoyo.", "I am sorry, but that day is difficult."),
                 X("그날은 사정이 있어서 못 가요.", "geunal-eun sajeong-i isseoseo mot gayo.", "Something has come up that day, so I cannot come."),
                 X("다음에 꼭 갈게요.", "daeum-e kkok galgeyo.", "I will certainly come next time.")],
                [("미안합니다 하지만 못 갑니다 어려워요.", "미안하지만 그날은 어려워요.", "One clause, one ending — the apology and the refusal are not two sentences bolted together."),
                 ("다음에 갈 거예요.", "다음에 꼭 갈게요.", "A promise to the host takes -(으)ㄹ게요, which offers it; -(으)ㄹ 거예요 only predicts.")]),
              [D("미나", "토요일에 우리 집에 올 수 있어요?", "toyoil-e uri jib-e ol su isseoyo?", "Can you come to my place on Saturday?"),
               D("지훈", "미안하지만 그날은 어려워요. 사정이 있어요.", "mianhajiman geunal-eun eoryeowoyo. sajeong-i isseoyo.", "I am sorry, but that day is difficult. Something has come up."),
               D("미나", "괜찮아요. 다음 주는 어때요?", "gwaenchanayo. daeum ju-neun eottaeyo?", "It is fine. How about next week?"),
               D("지훈", "다음 주 토요일은 꼭 갈게요.", "daeum ju toyoil-eun kkok galgeyo.", "Next Saturday I will certainly come.")],
              WS("Declining worksheet", [
                  T("Refuse gently.", ["I am sorry, but that day is difficult", "something has come up"],
                    ["미안하지만 그날은 어려워요", "사정이 있어요"]),
                  T("Promise next time.", ["I will certainly come next Saturday", "how about next week?"],
                    ["다음 주 토요일은 꼭 갈게요", "다음 주는 어때요?"]),
              ])),
            L("방문 예절",
              "A Korean home is entered with the shoes off and a greeting at the door: 들어가면서 "
              "인사해요. Gifts pass from both hands, and the host's offering is received rather than "
              "refused outright.",
              [V("신발", "sinbal", "shoes", "noun"),
               V("벗다", "beotda", "to take off", "verb"),
               V("예절", "yejeol", "manners, etiquette", "noun"),
               V("두 손", "du son", "both hands", "noun"),
               V("들어가다", "deureogada", "to go in", "verb")],
              G("When you visit",
                "신발을 벗고 들어가요 · 두 손으로 드려요 · 앉으라고 하세요",
                "Sequence is made with -고: 신발을 벗고 들어가요, take off your shoes and go in. Giving "
                "something to an elder uses the humble 드리다 and both hands, never one.",
                [X("신발을 벗고 들어가요.", "sinbal-eul beotgo deureogayo.", "You take off your shoes and go in."),
                 X("선물은 두 손으로 드려요.", "seonmul-eun du son-euro deuryeoyo.", "A gift is given with both hands."),
                 X("앉으세요. 차를 드릴게요.", "anjeuseyo. cha-reul deurilgeyo.", "Please sit. I will bring tea.")],
                [("선물을 줬어요 선생님께.", "선생님께 선물을 드렸어요.", "An elder receives something with 드리다, and 께 marks them."),
                 ("신발을 벗어요 들어가요.", "신발을 벗고 들어가요.", "Two actions in sequence are joined by -고.")]),
              [D("미나", "어서 오세요. 신발은 여기 두세요.", "eoseo oseyo. sinbal-eun yeogi duseoyo.", "Welcome. Leave your shoes here."),
               D("지훈", "네, 안녕하세요. 어머니께 선물을 드렸어요.", "ne, annyeonghaseyo. eomeoni-kke seonmul-eul deuryeosseoyo.", "Yes, hello. I gave your mother the gift."),
               D("미나", "감사합니다. 앉으세요. 차를 드릴게요.", "gamsahamnida. anjeuseyo. cha-reul deurilgeyo.", "Thank you. Please sit. I will bring tea."),
               D("지훈", "고맙습니다. 집이 참 따뜻하네요.", "gomapseumnida. jib-i cham ttatteuthaneyo.", "Thank you. The house feels really warm.")],
              WS("Visit worksheet", [
                  T("Do it in order.", ["take off your shoes and go in", "give a gift with both hands"],
                    ["신발을 벗고 들어가요", "선물은 두 손으로 드려요"]),
                  T("Say it to an elder.", ["I gave your mother the gift", "I will bring tea"],
                    ["어머니께 선물을 드렸어요", "차를 드릴게요"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Korea runs on messaging. 카카오톡 is on nearly every phone, and a reply that takes a day "
                 "is read as a statement in itself — 빠른 답장 is a social expectation rather than a "
                 "courtesy. A phone call opens with 여보세요 and identifies the caller immediately, "
                 "because the number alone rarely says who is speaking. Invitations are informal and "
                 "flexible: 놀러 오세요 can be issued and accepted within one exchange of texts, and the "
                 "refusal carries its own grammar of apology and promise for next time."),
        source_url="https://en.wikipedia.org/wiki/KakaoTalk",
        reading=("어제 저녁에 친구에게서 전화가 왔습니다. 저는 여보세요 하고 받았습니다. 친구가 "
                 "이번 주말에 자기 집에 놀러 오라고 했습니다. 저는 토요일 오후에 가겠다고 했습니다. "
                 "오늘 아침에 다시 문자가 왔습니다. 무엇을 가져오면 좋겠냐고 물었습니다. 제가 과일을 "
                 "사겠다고 답장했습니다. 친구는 아무것도 필요 없다고 했지만 저는 가는 길에 과일을 "
                 "살 것입니다."),
        reading_gloss=("Yesterday evening a friend called me. I answered with hello. My friend asked me to "
                       "come over to their place this weekend. I said I would go on Saturday afternoon. "
                       "This morning a text came again. They asked what would be good to bring. I "
                       "replied that I would buy fruit. My friend said nothing is needed, but I will buy "
                       "fruit on the way."),
        listening=("미나: 여보세요?<br>지훈: 안녕하세요, 지훈입니다. 미나 씨 계세요?<br>"
                   "미나: 네, 저예요. 무슨 일이세요?<br>"
                   "지훈: 오늘 저녁에 시간 있어요? 같이 밥을 먹을까요?<br>"
                   "미나: 오늘은 어려워요. 내일은 어때요?<br>"
                   "지훈: 좋아요. 내일 일곱 시에 만나요."),
        listening_gloss=("Mina: Hello? Jihun: Hello, this is Jihun. Is Mina there? Mina: Yes, speaking. "
                         "What is it? Jihun: Do you have time this evening? Shall we eat together? Mina: "
                         "Today is difficult. How about tomorrow? Jihun: Good. Let us meet at seven "
                         "tomorrow."),
        voice_tag=VOICE,
        idioms=[
            ("여보세요", "hello (on the phone only)", "hello — answering the phone"),
            ("잠깐만요", "just a moment", "one moment, please"),
            ("바꿔 드릴게요", "I will exchange (the phone) for you", "I will pass you over"),
            ("통화 중이에요", "in the middle of a call", "the line is busy"),
            ("문자를 보냈어요", "I sent a text", "I texted"),
            ("답장이 없어요", "there is no reply", "no answer yet"),
            ("놀러 오세요", "come to play", "come over"),
            ("미안하지만 어려워요", "I am sorry, but it is difficult", "sorry, I cannot make it"),
            ("다음에 꼭 갈게요", "I will certainly go next time", "I will come next time for sure"),
            ("신발을 벗고 들어가요", "take off your shoes and go in", "shoes off at the door"),
        ],
        mistakes=[
            ("여보세요, 안녕하세요, 실례합니다.", "여보세요, 지훈 씨 계세요?", "On the phone 여보세요 replaces the greeting; the errand comes next."),
            ("다시 전화해 주세요 달라고 전했어요.", "다시 전화해 달라고 전했어요.", "A request passed on for somebody else takes -달라고, not -주세요."),
            ("미안합니다 하지만 못 갑니다 어려워요.", "미안하지만 그날은 어려워요.", "Polish the refusal with one ending: 미안하지만 plus 어려워요."),
        ],
        task_title="Write a day and a message",
        task_instructions=("Write your weekday in six sentences with times, then write a phone call of four "
                           "turns: greeting, errand, hold, message. Use 여보세요 once, -(으)ㄹ게요 twice and "
                           "one refusal with 미안하지만."),
    ),
    "test": [
        ("translate_en", "Say: Excuse me, what time do you get up?", "보통 몇 시에 일어나요?"),
        ("translate_ko", "여보세요, 지훈 씨 계세요?", "Hello, is Jihun there?"),
        ("multiple_choice", "Which sentence refuses politely?", "미안하지만 그날은 어려워요."),
        ("fill_in_the_blank", "아홉 시___ 여섯 시까지 해요.", "부터"),
        ("word_selection", "Select the Korean for 'I will pass you over'.", "바꿔 드릴게요"),
        ("error_correction", "문자를 보냈어요 해요.", "문자를 보냈어요."),
        ("dialogue_completion", "Complete: 뭘 가져갈까요? — ___ (fruit is plenty)", "과일이면 충분해요"),
        ("matching", "Match 자주 to its meaning.", "often"),
        ("reading_comprehension", "친구가 아무것도 필요 없다고 했습니다. What did the friend say?", "nothing is needed"),
        ("inference", "지금 자리에 없어요. 메시지를 남기시겠어요? — what is happening?", "the person is out and a message is offered"),
        ("main_idea", "신발을 벗고 들어가고 선물은 두 손으로 드려요. What is this about?", "manners when visiting a home"),
        ("detail_identification", "내일 일곱 시에 만나요. When are they meeting?", "seven tomorrow"),
    ],
}

HALFSTEPS["A2+"] = {
    "title": "Korean A2+ — Bank and phone shop",
    "native": NATIVE,
    "goals": [
        "Open and use a bank account, and ask what a fee is for",
        "Change a phone plan, a device or a carrier without losing the number",
        "Report a lost card or a broken phone and ask for the fix",
    ],
    "units": [
        {"id": "A2+-U1", "title": "은행에서", "lessons": [
            L("통장을 만들어요",
              "Opening an account is a paperwork conversation: 통장을 만들고 싶어요, 신분증이 필요해요, "
              "며칠 걸려요. The polite request takes -고 싶은데요.",
              [V("통장", "tongjang", "bankbook, account", "noun"),
               V("계좌", "gyejwa", "account", "noun"),
               V("신분증", "sinbunjeung", "identification", "noun"),
               V("서류", "seoryu", "documents, paperwork", "noun"),
               V("필요하다", "piryohada", "to be necessary", "adjective")],
              G("Requests at the counter",
                "통장을 만들고 싶은데요 · 신분증이 필요해요 · 며칠 걸려요?",
                "-고 싶은데요 states what you came for and leaves the sentence open for the clerk to "
                "answer, which is the standard counter manner. Requirements take 이/가 필요하다.",
                [X("통장을 만들고 싶은데요.", "tongjang-eul mandeulgo sipeundeyo.", "I would like to open an account."),
                 X("신분증이 필요해요.", "sinbunjeung-i piryohaeyo.", "Identification is required."),
                 X("며칠 걸려요?", "myeochil geollyeoyo?", "How many days does it take?")],
                [("통장을 만들고 싶어요 필요해요.", "통장을 만들고 싶은데요.", "One predicate: -고 싶은데요 already states the request."),
                 ("신분증을 필요해요.", "신분증이 필요해요.", "필요하다 takes 이/가 on the thing needed.")]),
              [D("미나", "안녕하세요, 통장을 만들고 싶은데요.", "annyeonghaseyo, tongjang-eul mandeulgo sipeundeyo.", "Hello, I would like to open an account."),
               D("직원", "네, 신분증이 필요합니다. 외국인 등록증 있으세요?", "ne, sinbunjeung-i piryohamnida. oegugin deungnokjeung isseuseyo?", "Yes, identification is required. Do you have an alien registration card?"),
               D("미나", "네, 여기 있습니다. 며칠 걸려요?", "ne, yeogi itseumnida. myeochil geollyeoyo?", "Yes, here it is. How long does it take?"),
               D("직원", "오늘 바로 됩니다. 비밀번호를 정해 주세요.", "oneul baro doemnida. bimilbeonho-reul jeonghae juseyo.", "It is done today. Please set a password.")],
              WS("Bank worksheet", [
                  T("State your errand.", ["I would like to open an account", "identification is required"],
                    ["통장을 만들고 싶은데요", "신분증이 필요해요"]),
                  T("Ask about the process.", ["how many days does it take?", "please set a password"],
                    ["며칠 걸려요?", "비밀번호를 정해 주세요"]),
              ])),
            L("현금을 찾아요",
              "At the machine the verbs are 찾다 and 넣다, the password is 비밀번호, and the remaining "
              "balance is 잔액. A fee is 수수료 and it is always worth asking.",
              [V("현금", "hyeongeum", "cash", "noun"),
               V("찾다", "chatda", "to withdraw, to look for", "verb"),
               V("넣다", "neota", "to put in, to deposit", "verb"),
               V("잔액", "janaek", "balance", "noun"),
               V("수수료", "susuryo", "fee, commission", "noun")],
              G("At the machine",
                "현금을 찾고 싶어요 · 잔액을 확인해 주세요 · 수수료가 얼마예요?",
                "찾다 covers both looking for and withdrawing; the machine's screen offers to 확인하다 "
                "the balance. Money amounts are Sino-Korean and need a counter — 만 원, 오천 원.",
                [X("현금을 찾고 싶어요.", "hyeongeum-eul chatgo sipeoyo.", "I would like to withdraw cash."),
                 X("잔액을 확인해 주세요.", "janaek-eul hwagin-hae juseyo.", "Please check the balance."),
                 X("수수료가 얼마예요?", "susuryo-ga eolmayeyo?", "How much is the fee?")],
                [("현금을 찾아요 넣어요.", "현금을 찾고 싶어요.", "Withdrawing and depositing are separate actions; state the one you want."),
                 ("만 원을 찾아요 돈.", "만 원을 찾아요.", "The amount already names the money — 돈 is not added after it.")]),
              [D("지훈", "현금을 찾고 싶은데 기계를 못 쓰겠어요.", "hyeongeum-eul chatgo sipeunde gigye-reul mot sseugesseoyo.", "I want to withdraw cash but I cannot work the machine."),
               D("직원", "괜찮습니다. 카드를 여기에 넣고 비밀번호를 누르세요.", "gwaenchanseumnida. kadeu-reul yeogi-e neoko bimilbeonho-reul nureuseyo.", "It is fine. Put the card here and enter your password."),
               D("지훈", "수수료가 얼마예요?", "susuryo-ga eolmayeyo?", "How much is the fee?"),
               D("직원", "같은 은행 기계는 무료입니다.", "gateun eunhaeng gigye-neun muryo-imnida.", "At this bank's own machines it is free.")],
              WS("Cash worksheet", [
                  T("Say what you want.", ["I would like to withdraw cash", "please check the balance"],
                    ["현금을 찾고 싶어요", "잔액을 확인해 주세요"]),
                  T("Ask the cost.", ["how much is the fee?", "the same bank's machine is free"],
                    ["수수료가 얼마예요?", "같은 은행 기계는 무료입니다"]),
              ])),
            L("해외로 송금해요",
              "A transfer needs the recipient, the bank code and the number of days: 받는 분, 은행 코드, "
              "사흘쯤 걸려요. The amount that arrives differs from the amount sent.",
              [V("송금", "songgeum", "money transfer", "noun"),
               V("받는 분", "batneun bun", "the recipient (polite)", "noun"),
               V("코드", "kodeu", "code", "noun"),
               V("걸리다", "geollida", "to take (time)", "verb"),
               V("환율", "hwannyul", "exchange rate", "noun")],
              G("Sending money abroad",
                "해외로 송금하고 싶어요 · 사흘쯤 걸려요 · 환율이 어떻게 돼요?",
                "걸리다 takes the time as its subject: 사흘쯤 걸려요. A polite person-reference is 받는 "
                "분 rather than the plain 사람, and the rate is asked with 어떻게 돼요.",
                [X("해외로 송금하고 싶어요.", "haeoe-ro songgeumhago sipeoyo.", "I would like to send money abroad."),
                 X("보통 사흘쯤 걸려요.", "botong saheul-jjeum geollyeoyo.", "It usually takes about three days."),
                 X("오늘 환율이 어떻게 돼요?", "oneul hwannyul-i eotteoke dwaeyo?", "What is today's exchange rate?")],
                [("사흘을 걸려요.", "사흘쯤 걸려요.", "걸리다 takes the duration without 을/를, and 쯤 softens it to about."),
                 ("받는 사람분에게 보내요.", "받는 분에게 보내요.", "받는 분 already means the recipient politely; 사람 and 분 are not stacked.")]),
              [D("지훈", "해외로 송금하고 싶은데요.", "haeoe-ro songgeumhago sipeundeyo.", "I would like to send money abroad."),
               D("직원", "받는 분의 은행 코드를 아세요?", "batneun bun-ui eunhaeng kodeu-reul aseyo?", "Do you know the recipient's bank code?"),
               D("지훈", "네, 여기 있어요. 며칠 걸려요?", "ne, yeogi isseoyo. myeochil geollyeoyo?", "Yes, here it is. How many days does it take?"),
               D("직원", "보통 사흘쯤 걸리고, 환율은 오늘 기준입니다.", "botong saheul-jjeum geolligo, hwannyul-eun oneul gijun-imnida.", "Usually about three days, and the rate is today's.")],
              WS("Transfer worksheet", [
                  T("Ask about a transfer.", ["I would like to send money abroad", "how many days does it take?"],
                    ["해외로 송금하고 싶어요", "며칠 걸려요?"]),
                  T("Use the right words.", ["about three days", "what is today's exchange rate?"],
                    ["사흘쯤 걸려요", "오늘 환율이 어떻게 돼요?"]),
              ])),
        ]},
        {"id": "A2+-U2", "title": "휴대폰 가게", "lessons": [
            L("요금제를 바꿔요",
              "Plans are compared with 보다: 데이터가 더 많고 요금이 싸요. A contract runs for a fixed "
              "term, 약정, and leaving early costs money.",
              [V("요금제", "yogeumje", "rate plan", "noun"),
               V("데이터", "deiteo", "mobile data", "noun"),
               V("약정", "yakjeong", "contract term", "noun"),
               V("바꾸다", "bakuda", "to change", "verb"),
               V("무제한", "mujehan", "unlimited", "noun")],
              G("Comparing plans",
                "요금제를 바꾸고 싶어요 · 데이터가 더 많아요 · 약정이 남았어요",
                "Comparison takes 더 … than … with 보다 or a plain 더: 데이터가 더 많아요. A remaining "
                "contract is 남다, and the term itself is 약정, not 계약, in phone shops.",
                [X("요금제를 바꾸고 싶어요.", "yogeumje-reul bakkugo sipeoyo.", "I would like to change my plan."),
                 X("이 요금제가 데이터가 더 많아요.", "i yogeumje-ga deiteo-ga deo manayo.", "This plan has more data."),
                 X("약정이 일 년 남았어요.", "yakjeong-i il nyeon namasseoyo.", "A year is left on the contract.")],
                [("요금제를 바꾸고 싶어요 바꿔요.", "요금제를 바꾸고 싶어요.", "One predicate per sentence."),
                 ("약정이 있어요 남았어요.", "약정이 남았어요.", "남다 already says that time remains.")]),
              [D("미나", "요금제를 바꾸고 싶은데요.", "yogeumje-reul bakkugo sipeundeyo.", "I would like to change my plan."),
               D("직원", "지금 요금제는 데이터가 몇 기가예요?", "jigeum yogeumje-neun deiteo-ga myeot giga-yeyo?", "How many gigabytes is your current plan?"),
               D("미나", "삼 기가예요. 더 많은 걸로 바꾸고 싶어요.", "sam giga-yeyo. deo manheun geollo bakkugo sipeoyo.", "Three gigabytes. I would like to change to a bigger one."),
               D("직원", "그럼 이 요금제가 좋아요. 다만 약정이 일 년 남았습니다.", "geureom i yogeumje-ga joayo. daman yakjeong-i il nyeon namatseumnida.", "Then this plan is good. Note that a year is left on your contract.")],
              WS("Plan worksheet", [
                  T("Ask to change.", ["I would like to change my plan", "how many gigabytes is it?"],
                    ["요금제를 바꾸고 싶어요", "몇 기가예요?"]),
                  T("Compare.", ["this plan has more data", "a year is left on the contract"],
                    ["이 요금제가 데이터가 더 많아요", "약정이 일 년 남았어요"]),
              ])),
            L("기기를 바꾸고 싶어요",
              "A device can be paid for outright or in instalments: 한 번에 사다 or 할부로 사다. "
              "Insurance is 보험, and a swap is 교체.",
              [V("기기", "gigi", "device", "noun"),
               V("할부", "halbu", "instalments", "noun"),
               V("보험", "boheom", "insurance", "noun"),
               V("교체", "gyoche", "replacement, swap", "noun"),
               V("새로", "saero", "newly, again", "adverb")],
              G("Buying a device",
                "기기를 바꾸고 싶어요 · 할부로 살 수 있어요? · 보험이 들어 있어요",
                "Payment method takes -(으)로: 할부로, 현금으로, 카드로. Insurance is entered with "
                "들다 — 보험이 들어 있다 — and the device itself is 기기, not the brand name.",
                [X("기기를 바꾸고 싶어요.", "gigi-reul bakkugo sipeoyo.", "I would like to change my device."),
                 X("할부로 살 수 있어요?", "halbu-ro sal su isseoyo?", "Can I buy it in instalments?"),
                 X("보험이 들어 있어요.", "boheom-i deureo isseoyo.", "Insurance is included.")],
                [("할부에 살 수 있어요?", "할부로 살 수 있어요?", "A payment method takes -(으)로, not 에."),
                 ("보험을 들어요 있어요.", "보험이 들어 있어요.", "The state takes 이/가: 보험이 들어 있다.")]),
              [D("지훈", "기기를 바꾸고 싶은데 할부로 살 수 있어요?", "gigi-reul bakkugo sipeunde halbu-ro sal su isseoyo?", "I want to change my device — can I pay in instalments?"),
               D("직원", "네, 이십사 개월 할부가 가능합니다.", "ne, isipsa gaewol halbu-ga ganeunghamnida.", "Yes, twenty-four monthly instalments are possible."),
               D("지훈", "보험도 들어 있어요?", "boheom-do deureo isseoyo?", "Is insurance included too?"),
               D("직원", "기본 보험이 들어 있고, 추가 보험은 따로 신청하시면 됩니다.", "gibon boheom-i deureo itgo, chuga boheom-eun ttaro sincheonghasimyeon doemnida.", "Basic insurance is included; extra insurance is applied for separately.")],
              WS("Device worksheet", [
                  T("Ask about payment.", ["can I buy it in instalments?", "I would like to change my device"],
                    ["할부로 살 수 있어요?", "기기를 바꾸고 싶어요"]),
                  T("Ask about cover.", ["is insurance included too?", "extra insurance is applied for separately"],
                    ["보험도 들어 있어요?", "추가 보험은 따로 신청하시면 됩니다"]),
              ])),
            L("번호를 옮겨요",
              "Keeping your number while changing carrier is 번호 이동. The old carrier must confirm "
              "there is no remaining contract, and the new one issues a SIM the same day.",
              [V("번호 이동", "beonho idong", "number porting", "noun"),
               V("통신사", "tongsin-sa", "carrier, telecom company", "noun"),
               V("유지하다", "yujihada", "to keep, to maintain", "verb"),
               V("확인하다", "hwagin-hada", "to confirm, to check", "verb"),
               V("유심", "yusim", "SIM card", "noun")],
              G("Porting a number",
                "번호를 그대로 유지하고 싶어요 · 통신사를 바꿔도 돼요? · 오늘 바로 됩니다",
                "The number is what is kept: 번호를 유지하다, and the carrier is what changes. Permission "
                "to do something is asked with -아/어도 돼요?, and 그대로 keeps the number unchanged.",
                [X("번호를 그대로 유지하고 싶어요.", "beonho-reul geudaero yujihago sipeoyo.", "I would like to keep my number as it is."),
                 X("통신사를 바꿔도 돼요?", "tongsin-sa-reul bakkwodo dwaeyo?", "May I change carrier?"),
                 X("유심은 오늘 바로 나옵니다.", "yusim-eun oneul baro naomnida.", "The SIM is issued today.")],
                [("번호를 바꾸고 싶어요.", "번호를 그대로 유지하고 싶어요.", "Porting keeps the number — 바꾸다 would mean a new number."),
                 ("통신사를 바꿔요 돼요?", "통신사를 바꿔도 돼요?", "Permission takes -아/어도 되다, not the plain form.")]),
              [D("미나", "통신사를 바꾸고 싶은데 번호는 그대로 유지할 수 있어요?", "tongsin-sa-reul bakkugo sipeunde beonho-neun geudaero yujihal su isseoyo?", "I want to change carrier — can I keep my number?"),
               D("직원", "네, 번호 이동으로 가능합니다. 약정이 남아 있으면 확인이 필요해요.", "ne, beonho idong-euro ganeunghamnida. yakjeong-i nama isseumyeon hwagin-i piryohaeyo.", "Yes, by porting. If a contract remains, confirmation is needed."),
               D("미나", "확인은 어떻게 해요?", "hwagin-eun eotteoke haeyo?", "How is it confirmed?"),
               D("직원", "제가 통신사에 전화해서 확인해 드릴게요.", "jega tongsin-sa-e jeonhwahaeseo hwagin-hae deurilgeyo.", "I will call the carrier and confirm it for you.")],
              WS("Porting worksheet", [
                  T("Keep the number.", ["I would like to keep my number as it is", "may I change carrier?"],
                    ["번호를 그대로 유지하고 싶어요", "통신사를 바꿔도 돼요?"]),
                  T("Ask about confirmation.", ["how is it confirmed?", "I will confirm it for you"],
                    ["확인은 어떻게 해요?", "제가 확인해 드릴게요"]),
              ])),
        ]},
        {"id": "A2+-U3", "title": "문제를 해결해요", "lessons": [
            L("카드를 잃어버렸어요",
              "A lost card is reported in one sentence and stopped immediately: 카드를 잃어버려서 "
              "정지시켜 주세요. A replacement is 재발급.",
              [V("잃어버리다", "ireobeorida", "to lose", "verb"),
               V("정지시키다", "jeongjisikida", "to suspend, to block", "verb"),
               V("신고하다", "singohada", "to report", "verb"),
               V("재발급", "jaebalgeup", "reissue", "noun"),
               V("바로", "baro", "right away", "adverb")],
              G("Reporting a loss",
                "카드를 잃어버렸어요 · 정지시켜 주세요 · 재발급을 신청하고 싶어요",
                "The loss is stated in the past and the request follows in the same breath; -아서/어서 "
                "links them. The card is the object of 정지시키다, and 신청하다 is the verb for applying.",
                [X("카드를 잃어버렸어요.", "kadeu-reul ireobeoryeosseoyo.", "I have lost my card."),
                 X("바로 정지시켜 주세요.", "baro jeongjisikyeo juseyo.", "Please block it right away."),
                 X("재발급을 신청하고 싶어요.", "jaebalgeup-eul sincheonghago sipeoyo.", "I would like to apply for a replacement.")],
                [("카드를 잃었어요 있어요.", "카드를 잃어버렸어요.", "The accidental sense takes 잃어버리다, and it ends the clause."),
                 ("카드가 정지시켜 주세요.", "카드를 정지시켜 주세요.", "정지시키다 takes 을/를 on the card.")]),
              [D("미나", "카드를 잃어버렸어요. 바로 정지시켜 주세요.", "kadeu-reul ireobeoryeosseoyo. baro jeongjisikyeo juseyo.", "I have lost my card. Please block it right away."),
               D("직원", "확인했습니다. 잔액은 안전합니다. 재발급을 신청하시겠어요?", "hwaginhaetseumnida. janaek-eun anjeonhamnida. jaebalgeup-eul sincheonghasigesseoyo?", "Confirmed. The balance is safe. Would you like a replacement?"),
               D("미나", "네, 며칠 걸려요?", "ne, myeochil geollyeoyo?", "Yes. How long does it take?"),
               D("직원", "일주일쯤 걸리고, 그동안 임시 카드를 쓸 수 있습니다.", "iljuil-jjeum geolligo, geudongan imsi kadeu-reul sseul su itseumnida.", "About a week; you can use a temporary card in the meantime.")],
              WS("Lost-card worksheet", [
                  T("Report the loss.", ["I have lost my card", "please block it right away"],
                    ["카드를 잃어버렸어요", "바로 정지시켜 주세요"]),
                  T("Ask for the replacement.", ["I would like to apply for a replacement", "how many days does it take?"],
                    ["재발급을 신청하고 싶어요", "며칠 걸려요?"]),
              ])),
            L("휴대폰이 고장 났어요",
              "A broken device is 고장이 났다, handing it in is 맡기다, and collecting it is 찾다. A "
              "repair under guarantee is 무상 수리.",
              [V("고장", "gojang", "breakdown, fault", "noun"),
               V("수리", "suri", "repair", "noun"),
               V("맡기다", "matgida", "to hand in, to entrust", "verb"),
               V("보증", "bojeung", "guarantee, warranty", "noun"),
               V("무상", "musang", "free of charge", "noun")],
              G("Repairs",
                "휴대폰이 고장 났어요 · 수리를 맡기고 싶어요 · 보증이 남아 있어요",
                "The fault takes 이/가 and the verb 나다: 고장이 났어요. The device is whatever you "
                "맡기다, and the guarantee is what 남아 있다. 찾다 is the verb for collecting it again.",
                [X("휴대폰이 고장 났어요.", "hyudaepon-i gojang natseoyo.", "My phone has broken."),
                 X("수리를 맡기고 싶어요.", "suri-reul matgigo sipeoyo.", "I would like to hand it in for repair."),
                 X("보증이 남아 있어서 무상입니다.", "bojeung-i nama isseoseo musang-imnida.", "The guarantee is still valid, so it is free.")],
                [("휴대폰을 고장 났어요.", "휴대폰이 고장 났어요.", "The fault is the subject: 이/가 with 고장이 나다."),
                 ("수리를 찾고 싶어요.", "수리를 맡기고 싶어요.", "맡기다 is handing it in; 찾다 is collecting it.")]),
              [D("지훈", "휴대폰이 고장 났어요. 수리를 맡기고 싶어요.", "hyudaepon-i gojang natseoyo. suri-reul matgigo sipeoyo.", "My phone has broken. I would like to hand it in for repair."),
               D("직원", "언제 샀어요? 보증이 남아 있어요?", "eonje sasseoyo? bojeung-i nama isseoyo?", "When did you buy it? Is the guarantee still valid?"),
               D("지훈", "작년에 샀고, 보증이 두 달 남았어요.", "jaknyeon-e satgo, bojeung-i du dal namasseoyo.", "I bought it last year; two months remain on the guarantee."),
               D("직원", "그럼 무상 수리입니다. 이틀 뒤에 찾으러 오세요.", "geureom musang suri-imnida. iteul dwie chajeureo oseyo.", "Then it is a free repair. Come back in two days to collect it.")],
              WS("Repair worksheet", [
                  T("Describe the fault.", ["my phone has broken", "I would like to hand it in for repair"],
                    ["휴대폰이 고장 났어요", "수리를 맡기고 싶어요"]),
                  T("Ask about the guarantee.", ["is the guarantee still valid?", "two months remain on the guarantee"],
                    ["보증이 남아 있어요?", "보증이 두 달 남았어요"]),
              ])),
            L("환불을 요청해요",
              "A refund needs the receipt and a reason: 영수증이 있고, 아직 안 썼어요. Exchange and "
              "refund are 교환 and 환불, and shop rules are 규정.",
              [V("환불", "hwanbul", "refund", "noun"),
               V("교환", "gyohwan", "exchange", "noun"),
               V("영수증", "yeongsujeung", "receipt", "noun"),
               V("규정", "gyujeong", "rule, regulation", "noun"),
               V("요청하다", "yocheonghada", "to request", "verb")],
              G("Asking for money back",
                "환불을 요청하고 싶어요 · 영수증이 있어요 · 규정상 어렵습니다",
                "환불 and 교환 are the objects of 요청하다 or 해 주세요. The shop's refusal is usually "
                "규정상 어렵습니다, and the reason you give is that the item has not been used: 아직 쓰지 "
                "않았어요.",
                [X("환불을 요청하고 싶어요.", "hwanbul-eul yocheonghago sipeoyo.", "I would like to request a refund."),
                 X("영수증이 여기 있어요.", "yeongsujeung-i yeogi isseoyo.", "The receipt is here."),
                 X("아직 쓰지 않았어요.", "ajik sseuji anasseoyo.", "I have not used it yet.")],
                [("환불을 해 주세요 요청해요.", "환불을 요청하고 싶어요.", "One request frame per sentence."),
                 ("영수증을 있어요.", "영수증이 있어요.", "있어요 takes 이/가 on the thing that exists.")]),
              [D("미나", "이 옷을 환불하고 싶은데요.", "i ot-eul hwanbulhago sipeundeyo.", "I would like a refund for these clothes."),
               D("직원", "영수증 있으세요? 그리고 사용하셨어요?", "yeongsujeung isseuseyo? geurigo sayonghasyeosseoyo?", "Do you have the receipt? And have you used them?"),
               D("미나", "영수증은 여기 있고, 아직 안 입었어요.", "yeongsujeung-eun yeogi itgo, ajik an ibeosseoyo.", "The receipt is here, and I have not worn them yet."),
               D("직원", "그럼 교환이나 환불이 가능합니다. 어느 쪽으로 하시겠어요?", "geureom gyohwanina hwanbul-i ganeunghamnida. eoneu jjok-euro hasigesseoyo?", "Then an exchange or refund is possible. Which would you prefer?")],
              WS("Refund worksheet", [
                  T("Ask for a refund.", ["I would like to request a refund", "the receipt is here"],
                    ["환불을 요청하고 싶어요", "영수증이 여기 있어요"]),
                  T("Give the reason.", ["I have not used it yet", "an exchange or refund is possible"],
                    ["아직 쓰지 않았어요", "교환이나 환불이 가능합니다"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Korean banking and phone shops run on identification and paperwork. Opening an account "
                 "needs 신분증 and often an 외국인 등록증; a phone plan is a contract with a fixed term, "
                 "약정, and the price of leaving early is stated plainly before you sign. Payments are "
                 "overwhelmingly card and app rather than cash, and the machine asks for the card first "
                 "and the password second. Because so much of daily life is tied to a phone number, "
                 "porting it — 번호 이동 — is a routine transaction with its own vocabulary."),
        source_url="https://en.wikipedia.org/wiki/Korean_won",
        reading=("지난주에 은행에 갔습니다. 통장을 만들고 싶다고 말했더니 직원이 신분증을 요청했습니다. "
                 "서류를 쓰고 비밀번호를 정했습니다. 그다음에 현금을 찾으려고 기계에 갔는데 방법을 "
                 "몰라서 직원에게 물었습니다. 같은 은행 기계는 수수료가 없었습니다. 오늘은 휴대폰 "
                 "가게에도 갔습니다. 요금제를 바꾸고 번호는 그대로 유지했습니다. 생각보다 간단했습니다."),
        reading_gloss=("Last week I went to the bank. When I said I wanted to open an account, the clerk "
                       "asked for identification. I filled in the papers and set a password. Then I went "
                       "to the machine to withdraw cash, but I did not know how, so I asked the clerk. At "
                       "the bank's own machines there was no fee. Today I also went to the phone shop. I "
                       "changed the plan and kept my number as it was. It was simpler than I expected."),
        listening=("직원: 어떻게 도와드릴까요?<br>지훈: 카드를 잃어버려서 정지시키고 싶어요.<br>"
                   "직원: 언제 잃어버리셨어요?<br>지훈: 어제 저녁에요. 그리고 재발급도 신청하고 싶어요.<br>"
                   "직원: 알겠습니다. 재발급은 일주일쯤 걸립니다.<br>"
                   "지훈: 그동안 카드 없이 쓸 수 있어요?<br>직원: 휴대폰 결제를 쓰시면 됩니다."),
        listening_gloss=("Clerk: How can I help? Jihun: I have lost my card and would like to block it. "
                         "Clerk: When did you lose it? Jihun: Yesterday evening. And I would like to "
                         "apply for a replacement too. Clerk: Understood. A replacement takes about a "
                         "week. Jihun: Can I manage without a card meanwhile? Clerk: You can use phone "
                         "payment."),
        voice_tag=VOICE,
        idioms=[
            ("통장을 만들고 싶은데요", "I would like to open an account (leaving it open)", "I would like to open an account"),
            ("신분증이 필요해요", "identification is necessary", "you need ID"),
            ("며칠 걸려요?", "how many days does it take?", "how long will it take?"),
            ("수수료가 얼마예요?", "how much is the fee?", "what is the charge?"),
            ("요금제를 바꿔요", "I change the rate plan", "I am changing my plan"),
            ("할부로 살 수 있어요?", "can I buy on instalments?", "do you offer instalments?"),
            ("번호를 그대로 유지해요", "I keep the number as it is", "I will keep my number"),
            ("고장이 났어요", "a fault has arisen", "it has broken down"),
            ("보증이 남아 있어요", "the guarantee remains", "it is still under warranty"),
            ("환불을 요청해요", "I request a refund", "I am asking for a refund"),
        ],
        mistakes=[
            ("할부에 살 수 있어요?", "할부로 살 수 있어요?", "A payment method takes -(으)로, not 에."),
            ("휴대폰을 고장 났어요.", "휴대폰이 고장 났어요.", "The fault is the subject: 고장이 나다 takes 이/가."),
            ("보험을 들어요 있어요.", "보험이 들어 있어요.", "The included state takes 이/가: 보험이 들어 있다."),
        ],
        task_title="Write a complaint that gets solved",
        task_instructions=("Write two short dialogues: one at a bank about a lost card, one at a phone shop "
                           "about a repair. Each needs the problem in one sentence, a request with -아/어 "
                           "주세요, one question about time or cost, and a closing line from the staff."),
    ),
    "test": [
        ("translate_en", "Say: I would like to open an account.", "통장을 만들고 싶어요."),
        ("translate_ko", "카드를 잃어버려서 정지시키고 싶어요.", "I have lost my card and would like to block it."),
        ("multiple_choice", "Which sentence asks about a fee?", "수수료가 얼마예요?"),
        ("fill_in_the_blank", "할부___ 살 수 있어요?", "로"),
        ("word_selection", "Select the Korean for 'the guarantee remains'.", "보증이 남아 있어요"),
        ("error_correction", "휴대폰을 고장 났어요.", "휴대폰이 고장 났어요."),
        ("dialogue_completion", "Complete: 며칠 걸려요? — ___ (about a week)", "일주일쯤 걸려요"),
        ("matching", "Match 환불 to its meaning.", "refund"),
        ("reading_comprehension", "같은 은행 기계는 수수료가 없었습니다. Was there a fee?", "no, at the bank's own machines it was free"),
        ("inference", "보증이 두 달 남았어요. 수리를 맡기고 싶어요. — what is likely to happen?", "a free repair before the guarantee expires"),
        ("main_idea", "번호는 그대로 유지하고 통신사만 바꿉니다. What is this about?", "porting a number to a new carrier"),
        ("detail_identification", "재발급은 일주일쯤 걸립니다. How long does a replacement take?", "about a week"),
    ],
}

HALFSTEPS["B1+"] = {
    "title": "Korean B1+ — CV and interview",
    "native": NATIVE,
    "goals": [
        "Describe your experience and duties in the past tense the CV uses",
        "Answer interview questions with a result, not an adjective",
        "Discuss salary, start date and conditions without closing the door",
    ],
    "units": [
        {"id": "B1+-U1", "title": "이력서", "lessons": [
            L("경력을 정리해요",
              "A CV lists what you did, for how long and with what result: 삼 년 동안 고객 지원을 "
              "담당했고, 응답 시간을 절반으로 줄였습니다.",
              [V("경력", "gyeongnyeok", "work experience", "noun"),
               V("담당하다", "damdanghada", "to be in charge of", "verb"),
               V("실적", "siljeok", "performance, results", "noun"),
               V("기간", "gigan", "period", "noun"),
               V("줄이다", "jurida", "to reduce", "verb")],
              G("Stating experience",
                "삼 년 동안 담당했습니다 · 응답 시간을 줄였습니다 · 기간은 이 년입니다",
                "A duty is 담당하다 and a result takes a number and a change verb: 줄이다, 늘리다, "
                "개선하다. Duration takes 동안, and the past tense of a CV stays in 합니다체.",
                [X("삼 년 동안 고객 지원을 담당했습니다.", "sam nyeon dongan gogaek jiwon-eul damdanghaetseumnida.", "I was in charge of customer support for three years."),
                 X("응답 시간을 절반으로 줄였습니다.", "eungdap sigan-eul jeolban-euro juryeotseumnida.", "I cut the response time by half."),
                 X("프로젝트 기간은 이 년이었습니다.", "peurojekteu gigan-eun i nyeon-ieotseumnida.", "The project ran for two years.")],
                [("삼 년을 담당했습니다.", "삼 년 동안 담당했습니다.", "A duration takes 동안, not 을/를."),
                 ("응답 시간을 줄었습니다.", "응답 시간을 줄였습니다.", "줄이다 is transitive: the time is the object.")]),
              [D("면접관", "이 일은 언제 담당하셨어요?", "i ir-eun eonje damdanghasyeosseoyo?", "When were you in charge of this work?"),
               D("지원자", "이 년 전부터 삼 년 동안 담당했습니다.", "i nyeon jeon-buteo sam nyeon dongan damdanghaetseumnida.", "For three years, starting two years ago."),
               D("면접관", "어떤 결과가 있었어요?", "eotteon gyeolgwa-ga isseosseoyo?", "What result did it produce?"),
               D("지원자", "응답 시간을 절반으로 줄였고, 만족도가 올라갔습니다.", "eungdap sigan-eul jeolban-euro juryeotgo, manjokdo-ga ollagatseumnida.", "I cut the response time by half and satisfaction rose.")],
              WS("Experience worksheet", [
                  T("State a duty.", ["I was in charge of customer support for three years", "the project ran for two years"],
                    ["삼 년 동안 고객 지원을 담당했습니다", "프로젝트 기간은 이 년이었습니다"]),
                  T("State a result.", ["I cut the response time by half", "satisfaction rose"],
                    ["응답 시간을 절반으로 줄였습니다", "만족도가 올라갔습니다"]),
              ])),
            L("자기소개를 써요",
              "A self-introduction names a strength and proves it in one line: 강점은 문제를 끝까지 "
              "확인한다는 점입니다. A weakness is stated with what you do about it.",
              [V("강점", "gangjeom", "strength", "noun"),
               V("약점", "yakjeom", "weakness", "noun"),
               V("성격", "seonggyeok", "character, temperament", "noun"),
               V("지원하다", "jiwonhada", "to apply for", "verb"),
               V("확인하다", "hwagin-hada", "to check, to confirm", "verb")],
              G("Naming a strength",
                "강점은 …라는 점입니다 · 성격이 꼼꼼한 편입니다 · 약점은 …라는 것입니다",
                "A strength is abstracted with -는 점이다: 강점은 끝까지 확인한다는 점입니다. The "
                "modifier form -는/은 makes a whole clause the subject, and 편이다 softens a self-"
                "description into a tendency.",
                [X("강점은 문제를 끝까지 확인한다는 점입니다.", "gangjeom-eun munje-reul kkeutkkaji hwaginhandaneun jeom-imnida.", "My strength is that I check a problem to the end."),
                 X("성격이 꼼꼼한 편입니다.", "seonggyeok-i kkomkkomhan pyeon-imnida.", "I am on the careful side."),
                 X("약점은 말이 느린 것입니다. 그래서 미리 준비합니다.", "yakjeom-eun mal-i neurin geos-imnida. geuraeseo miri junbihamnida.", "My weakness is that I speak slowly, so I prepare in advance.")],
                [("제 강점은 꼼꼼합니다.", "제 강점은 꼼꼼하다는 점입니다.", "A strength is named as a clause with -는 점이다, not as an adjective."),
                 ("약점이 없습니다.", "약점은 말이 느린 것이고, 준비로 보완합니다.", "A weakness needs a remedy; 없습니다 answers the wrong question.")]),
              [D("면접관", "본인의 강점이 무엇이라고 생각하세요?", "bonin-ui gangjeom-i mueosirago saenggak-haseyo?", "What do you consider your strength?"),
               D("지원자", "강점은 문제를 끝까지 확인한다는 점입니다.", "gangjeom-eun munje-reul kkeutkkaji hwaginhandaneun jeom-imnida.", "My strength is that I check a problem to the end."),
               D("면접관", "약점은요?", "yakjeom-eunyo?", "And your weakness?"),
               D("지원자", "말이 느린 편입니다. 그래서 중요한 자리에서는 미리 준비합니다.", "mal-i neurin pyeon-imnida. geuraeseo jungyohan jari-eseoneun miri junbihamnida.", "I speak on the slow side, so I prepare in advance for important occasions.")],
              WS("Self-introduction worksheet", [
                  T("Name a strength.", ["my strength is that I check a problem to the end", "I am on the careful side"],
                    ["강점은 문제를 끝까지 확인한다는 점입니다", "성격이 꼼꼼한 편입니다"]),
                  T("Name a weakness properly.", ["my weakness is that I speak slowly", "so I prepare in advance"],
                    ["약점은 말이 느린 것입니다", "그래서 미리 준비합니다"]),
              ])),
            L("지원 동기를 말해요",
              "Motivation connects the company's need to your own: 귀사의 …을 위해 일하고 싶습니다. The "
              "purpose form is -기 위해서, and the sentence ends in a wish rather than a demand.",
              [V("동기", "donggi", "motivation", "noun"),
               V("지원", "jiwon", "application", "noun"),
               V("기여하다", "giyeohada", "to contribute", "verb"),
               V("성장하다", "seongjanghada", "to grow", "verb"),
               V("위해서", "wihaeseo", "for the sake of", "grammar")],
              G("Stating a motivation",
                "고객을 돕기 위해서 지원했습니다 · 여기서 성장하고 싶습니다",
                "Purpose takes -기 위해서 before the clause that realises it, and the clause ends in "
                "the verb that carries the intention: 지원했습니다 states it as the reason for applying.",
                [X("고객을 돕기 위해서 지원했습니다.", "gogaek-eul dopgi wihaeseo jiwonhaetseumnida.", "I applied in order to help customers."),
                 X("이 분야에서 성장하고 싶습니다.", "i bunya-eseo seongjanghago sipeumnida.", "I want to grow in this field."),
                 X("제 경험이 팀에 기여할 수 있다고 생각합니다.", "je gyeongheom-i tim-e giyeohal su itdago saenggak-hamnida.", "I think my experience can contribute to the team.")],
                [("성장하기 위해서 지원합니다 좋습니다.", "성장하기 위해서 지원했습니다.", "One intention, one predicate."),
                 ("귀사에 위해서 일하고 싶습니다.", "귀사를 위해서 일하고 싶습니다.", "위해서 takes 을/를 on what the effort serves.")]),
              [D("면접관", "왜 우리 회사에 지원하셨어요?", "wae uri hoesa-e jiwonhasyeosseoyo?", "Why did you apply to our company?"),
               D("지원자", "고객 문제를 해결하는 일을 계속하기 위해서 지원했습니다.", "gogaek munje-reul haegyeolhaneun ir-eul gyeseokhagi wihaeseo jiwonhaetseumnida.", "I applied in order to keep solving customer problems."),
               D("면접관", "우리 회사에서 이루고 싶은 것이 있나요?", "uri hoesa-eseo irugo sipeun geos-i innayo?", "Is there something you want to achieve here?"),
               D("지원자", "이 분야에서 성장하고, 경험을 팀에 나누고 싶습니다.", "i bunya-eseo seongjanghago, gyeongheom-eul tim-e nanugo sipeumnida.", "I want to grow in this field and share my experience with the team.")],
              WS("Motivation worksheet", [
                  T("Give a purpose.", ["I applied in order to help customers", "I want to grow in this field"],
                    ["고객을 돕기 위해서 지원했습니다", "이 분야에서 성장하고 싶습니다"]),
                  T("Connect experience to the team.", ["my experience can contribute to the team", "I want to share my experience"],
                    ["제 경험이 팀에 기여할 수 있습니다", "경험을 팀에 나누고 싶습니다"]),
              ])),
        ]},
        {"id": "B1+-U2", "title": "면접", "lessons": [
            L("자주 묻는 질문",
              "Interview questions repeat, and so do the frames that answer them: 해 본 적이 있어요? "
              "takes -(으)ㄴ 적이 있다, and 어려웠던 점 takes the past modifier.",
              [V("면접", "myeonjeop", "interview", "noun"),
               V("질문", "jilmun", "question", "noun"),
               V("대답하다", "daedaphada", "to answer", "verb"),
               V("준비하다", "junbihada", "to prepare", "verb"),
               V("긴장하다", "ginjanghada", "to be nervous", "verb")],
              G("Experience questions",
                "해 본 적이 있어요? · 어려웠던 점을 말씀해 주세요 · 준비한 대로 말하세요",
                "-(으)ㄴ 적이 있다 states that something has been done at least once. A past modifier "
                "-았던/-었던 describes the occasion you are now talking about: 어려웠던 점, 힘들었던 "
                "프로젝트.",
                [X("고객 응대를 해 본 적이 있습니다.", "gogaek eungdae-reul hae bon jeok-i itseumnida.", "I have handled customers before."),
                 X("가장 어려웠던 점은 일정이었습니다.", "gajang eoryeowotdeon jeom-eun iljeong-ieotseumnida.", "The hardest part was the schedule."),
                 X("긴장했지만 준비한 대로 말했습니다.", "ginjanghaetjiman junbihan daero malhaetseumnida.", "I was nervous, but I said what I had prepared.")],
                [("고객 응대를 해 봤어요 있었다.", "고객 응대를 해 본 적이 있습니다.", "Experience takes -ㄴ 적이 있다, and one verb ends it."),
                 ("어려운 점이었습니다.", "어려웠던 점이었습니다.", "A past occasion takes -았던, not the plain present modifier.")]),
              [D("면접관", "팀에서 일해 본 적이 있으세요?", "tim-eseo ilhae bon jeok-i isseuseyo?", "Have you worked in a team before?"),
               D("지원자", "네, 다섯 명 팀에서 일한 적이 있습니다.", "ne, daseot myeong tim-eseo ilhan jeok-i itseumnida.", "Yes, I have worked in a team of five."),
               D("면접관", "가장 어려웠던 점은 무엇이었어요?", "gajang eoryeowotdeon jeom-eun mueos-ieosseoyo?", "What was the hardest part?"),
               D("지원자", "일정이었습니다. 그래서 역할을 나눠서 해결했습니다.", "iljeong-ieotseumnida. geuraeseo yeokal-eul nanwoseo haegyeolhaetseumnida.", "The schedule. So we divided the roles and solved it.")],
              WS("Interview-question worksheet", [
                  T("State experience.", ["I have handled customers before", "I have worked in a team of five"],
                    ["고객 응대를 해 본 적이 있습니다", "다섯 명 팀에서 일한 적이 있습니다"]),
                  T("Name the hard part.", ["the hardest part was the schedule", "I was nervous, but I said what I had prepared"],
                    ["가장 어려웠던 점은 일정이었습니다", "긴장했지만 준비한 대로 말했습니다"]),
              ])),
            L("실적을 근거로 말해요",
              "An answer becomes convincing when it carries a number and a change: 문의가 삼십 퍼센트 "
              "줄었습니다. The result clause takes -ㄴ 결과, and what came about takes -게 되다.",
              [V("근거", "geun-geo", "grounds, evidence", "noun"),
               V("결과", "gyeolgwa", "result", "noun"),
               V("개선하다", "gaeseonhada", "to improve", "verb"),
               V("수치", "suchi", "figure, number", "noun"),
               V("늘다", "neulda", "to increase", "verb")],
              G("Making a result concrete",
                "문의가 삼십 퍼센트 줄었습니다 · 개선한 결과 대기 시간이 짧아졌습니다 · 맡게 되었습니다",
                "Number plus change verb is the whole proof: 삼십 퍼센트 줄었습니다. -ㄴ 결과 links an "
                "action to its consequence, and -게 되다 states what you came to do without claiming "
                "you chose it.",
                [X("문의가 삼십 퍼센트 줄었습니다.", "munui-ga samsip peosenteu jureotseumnida.", "Enquiries fell by thirty percent."),
                 X("절차를 개선한 결과 대기 시간이 짧아졌습니다.", "jeolcha-reul gaeseonhan gyeolgwa daegi sigan-i jjalbajyeotseumnida.", "As a result of improving the process the waiting time shortened."),
                 X("작년에 이 업무를 맡게 되었습니다.", "jaknyeon-e i eommu-reul matge doeeotseumnida.", "Last year I came to take on this work.")],
                [("문의가 줄었습니다 많이.", "문의가 삼십 퍼센트 줄었습니다.", "The figure carries the proof and belongs before the verb."),
                 ("개선한 결과입니다 줄었습니다.", "개선한 결과 문의가 줄었습니다.", "-ㄴ 결과 introduces a clause, not a sentence on its own.")]),
              [D("면접관", "그 개선은 어떤 결과를 만들었어요?", "geu gaeseon-eun eotteon gyeolgwa-reul mandeureosseoyo?", "What result did that improvement produce?"),
               D("지원자", "절차를 개선한 결과 문의가 삼십 퍼센트 줄었습니다.", "jeolcha-reul gaeseonhan gyeolgwa munui-ga samsip peosenteu jureotseumnida.", "As a result of improving the process, enquiries fell by thirty percent."),
               D("면접관", "수치를 어떻게 확인했어요?", "suchi-reul eotteoke hwaginhaesseoyo?", "How did you verify the figure?"),
               D("지원자", "시스템 기록으로 매달 확인했습니다.", "siseutem girok-euro maedal hwaginhaetseumnida.", "I checked the system records every month.")],
              WS("Evidence worksheet", [
                  T("Give a result with a number.", ["enquiries fell by thirty percent", "the waiting time shortened"],
                    ["문의가 삼십 퍼센트 줄었습니다", "대기 시간이 짧아졌습니다"]),
                  T("Say what you came to do.", ["last year I came to take on this work", "I verified it through the system records"],
                    ["작년에 이 업무를 맡게 되었습니다", "시스템 기록으로 확인했습니다"]),
              ])),
            L("어려운 질문을 받아요",
              "Not knowing is answered honestly and then bounded: 잘 모르지만, 확인해 보겠습니다. The frame "
              "-지는 않지만 concedes before it adds.",
              [V("솔직히", "soljiki", "honestly", "adverb"),
               V("배우다", "baeuda", "to learn", "verb"),
               V("확인하다", "hwagin-hada", "to check, to confirm", "verb"),
               V("경우", "gyeong-u", "case, situation", "noun"),
               V("모르다", "moreuda", "to not know", "verb")],
              G("Answering what you do not know",
                "잘 모르지만 확인해 보겠습니다 · 경험이 많지는 않지만 배우고 있습니다",
                "-지만 concedes and continues. -지는 않지만 limits the claim to one aspect while "
                "keeping the sentence open, which is how a first-year candidate answers without "
                "overclaiming.",
                [X("잘 모르지만 확인해 보겠습니다.", "jal moreujiman hwagin-hae bogetseumnida.", "I do not know well, but I will check."),
                 X("경험이 많지는 않지만 배우고 있습니다.", "gyeongheom-i manchineun anchiman baeugo itseumnida.", "I do not have much experience, but I am learning."),
                 X("그런 경우에는 팀에 먼저 묻습니다.", "geureon gyeong-u-eneun tim-e meonjeo mutseumnida.", "In that kind of case I ask the team first.")],
                [("모르겠습니다 없습니다.", "잘 모르지만 확인해 보겠습니다.", "Not knowing is answered with the next step, not with a second negative."),
                 ("경험이 많지 않지만 배우지 않습니다.", "경험이 많지는 않지만 배우고 있습니다.", "-지만 needs a real continuation after the concession.")]),
              [D("면접관", "이 기술을 써 본 적이 있어요?", "i gisul-eul sseo bon jeok-i isseoyo?", "Have you used this technology before?"),
               D("지원자", "잘 모르지만 확인해 보겠습니다. 비슷한 도구는 써 봤습니다.", "jal moreujiman hwagin-hae bogetseumnida. biseuthan dogu-neun sseo bwatseumnida.", "I do not know it well, but I will look into it. I have used similar tools."),
               D("면접관", "모르는 일을 맡으면 어떻게 하세요?", "moreuneun ir-eul mateumyeon eotteoke haseyo?", "What do you do when given something unfamiliar?"),
               D("지원자", "그런 경우에는 먼저 팀에 묻고, 기록을 남깁니다.", "geureon gyeong-u-eneun meonjeo tim-e mutgo, girok-eul namgimnida.", "In that case I ask the team first and leave a record.")],
              WS("Hard-question worksheet", [
                  T("Answer honestly.", ["I do not know well, but I will check", "I have used similar tools"],
                    ["잘 모르지만 확인해 보겠습니다", "비슷한 도구는 써 봤습니다"]),
                  T("Concede and continue.", ["I do not have much experience, but I am learning", "in that kind of case I ask the team first"],
                    ["경험이 많지는 않지만 배우고 있습니다", "그런 경우에는 팀에 먼저 묻습니다"]),
              ])),
        ]},
        {"id": "B1+-U3", "title": "조건과 협의", "lessons": [
            L("연봉을 이야기해요",
              "Salary is discussed in ranges and with a question form: 희망 연봉이 어떻게 되세요? The "
              "answer states a range and leaves 협의 open.",
              [V("연봉", "yeonbong", "annual salary", "noun"),
               V("협의", "hyeobui", "discussion, negotiation", "noun"),
               V("제안", "jean", "offer, proposal", "noun"),
               V("조정하다", "jojeonghada", "to adjust", "verb"),
               V("조건", "jogeon", "condition, terms", "noun")],
              G("Talking about pay",
                "희망 연봉이 어떻게 되세요? · 협의 가능합니다 · 조건을 조정할 수 있어요",
                "A range is made with 부터 …까지 or 쯤, and 협의 가능합니다 is the standard answer that "
                "keeps the negotiation open. 조정하다 covers the change in either direction.",
                [X("희망 연봉이 어떻게 되세요?", "himang yeonbong-i eotteoke doeseyo?", "What salary are you hoping for?"),
                 X("삼천만 원쯤 생각하고 있고, 협의 가능합니다.", "samcheonman won-jjeum saenggakhago itgo, hyeobui ganeunghamnida.", "I am thinking around thirty million won, and it is negotiable."),
                 X("조건을 조정할 수 있으면 좋겠습니다.", "jogeon-eul jojeonghal su isseumyeon jotgesseumnida.", "I would be glad if the terms could be adjusted.")],
                [("연봉이 얼마예요?", "희망 연봉이 어떻게 되세요?", "In an interview the salary is asked for as a hope, in the polite 어떻게 되세요 form."),
                 ("삼천만 원입니다 협의합니다.", "삼천만 원쯤이고, 협의 가능합니다.", "A figure and its flexibility go in one sentence with -고.")]),
              [D("면접관", "희망 연봉이 어떻게 되세요?", "himang yeonbong-i eotteoke doeseyo?", "What salary are you hoping for?"),
               D("지원자", "삼천만 원쯤 생각하고 있고, 협의 가능합니다.", "samcheonman won-jjeum saenggakhago itgo, hyeobui ganeunghamnida.", "Around thirty million won, and it is negotiable."),
               D("면접관", "경력에 따라 조정됩니다. 언제부터 가능하세요?", "gyeongnyeok-e ttara jojeongdoemnida. eonje-buteo ganeunghaseyo?", "It is adjusted according to experience. When can you start?"),
               D("지원자", "한 달 뒤부터 가능합니다.", "han dal dwi-buteo ganeunghamnida.", "From one month later.")],
              WS("Salary worksheet", [
                  T("Ask and answer about pay.", ["what salary are you hoping for?", "around thirty million won, negotiable"],
                    ["희망 연봉이 어떻게 되세요?", "삼천만 원쯤이고 협의 가능합니다"]),
                  T("Talk about conditions.", ["the terms can be adjusted", "from one month later"],
                    ["조건을 조정할 수 있습니다", "한 달 뒤부터 가능합니다"]),
              ])),
            L("입사 시기를 조정해요",
              "The start date is a negotiation too: 다음 달 중순부터 가능합니다. To allow something, the "
              "form is -(으)ㄹ 수 있도록, and a change of plan is 통보하다.",
              [V("입사", "ipsa", "joining a company", "noun"),
               V("시기", "sigi", "timing", "noun"),
               V("조정", "jojeong", "adjustment", "noun"),
               V("통보", "tongbo", "notice, notification", "noun"),
               V("가능하다", "ganeunghada", "to be possible", "adjective")],
              G("Setting a date",
                "다음 달 중순부터 가능합니다 · 이 주까지 조정할 수 있도록 · 문자로 통보받았습니다",
                "-(으)ㄹ 수 있도록 introduces what you enable. 중순 and 초순 name the middle and the "
                "beginning of a month, and the written notice is 통보 rather than the spoken 알림.",
                [X("다음 달 중순부터 가능합니다.", "daeum dal jungsun-buteo ganeunghamnida.", "I can start from the middle of next month."),
                 X("이 주까지 조정할 수 있도록 해 주세요.", "i ju-kkaji jojeonghal su itdorok hae juseyo.", "Please arrange it so it can be adjusted by this week."),
                 X("입사 시기는 문자로 통보받았습니다.", "ipsa sigi-neun munja-ro tongbobadatseumnida.", "I was notified of the start date by text.")],
                [("다음 달부터 가능합니다 중순.", "다음 달 중순부터 가능합니다.", "A month and its part form one time phrase; 중순 comes after the month."),
                 ("조정할 수 있습니다 하세요.", "조정할 수 있도록 해 주세요.", "A request to enable something takes -ㄹ 수 있도록 하다.")]),
              [D("면접관", "언제부터 입사가 가능하세요?", "eonje-buteo ipsa-ga ganeunghaseyo?", "When can you start?"),
               D("지원자", "다음 달 중순부터 가능합니다.", "daeum dal jungsun-buteo ganeunghamnida.", "From the middle of next month."),
               D("면접관", "그보다 빠르면 어렵겠어요?", "geuboda ppareumyeon eoryeopgeteoyo?", "Would earlier be difficult?"),
               D("지원자", "이 주까지 조정할 수 있도록 해 보겠습니다.", "i ju-kkaji jojeonghal su itdorok hae bogetseumnida.", "I will try to arrange it so it can be adjusted by this week.")],
              WS("Start-date worksheet", [
                  T("Give a start date.", ["I can start from the middle of next month", "when can you start?"],
                    ["다음 달 중순부터 가능합니다", "언제부터 입사가 가능하세요?"]),
                  T("Offer flexibility.", ["I will try to adjust it by this week", "I was notified by text"],
                    ["이 주까지 조정할 수 있도록 해 보겠습니다", "문자로 통보받았습니다"]),
              ])),
            L("결과를 기다려요",
              "Waiting is phrased with a hope and a thank-you: 결과를 기다리겠습니다. 좋은 소식이 "
              "있었으면 좋겠습니다. A follow-up enquiry is 문의드리다, the humble form.",
              [V("결과", "gyeolgwa", "result", "noun"),
               V("통보", "tongbo", "notification", "noun"),
               V("기다리다", "gidarida", "to wait", "verb"),
               V("문의하다", "munuihada", "to enquire", "verb"),
               V("소식", "sosik", "news, word", "noun")],
              G("Waiting and following up",
                "결과를 기다리겠습니다 · 좋은 소식이 있었으면 좋겠습니다 · 문의드려도 될까요?",
                "A hope for the future takes -았/었으면 좋겠다, and the polite enquiry is the humble "
                "문의드리다 with -(아/어)도 될까요? — asking permission rather than asking a question "
                "outright.",
                [X("결과를 기다리겠습니다.", "gyeolgwa-reul gidarigetseumnida.", "I will wait for the result."),
                 X("좋은 소식이 있었으면 좋겠습니다.", "joeun sosik-i isseosseumyeon jotgesseumnida.", "I hope there is good news."),
                 X("다음 주에 문의드려도 될까요?", "daeum ju-e munuidoryeodo doelkkayo?", "May I enquire next week?")],
                [("결과가 있으면 좋습니다.", "결과가 있으면 좋겠습니다.", "A hope takes -았/었으면 좋겠다, not the plain condition."),
                 ("문의해도 됩니까 물어봅니다.", "문의드려도 될까요?", "One request frame; the humble form already carries the politeness.")]),
              [D("지원자", "결과는 언제쯤 알 수 있을까요?", "gyeolgwa-neun eonje-jjeum al su isseulkkayo?", "About when will I know the result?"),
               D("면접관", "다음 주 금요일까지 통보해 드립니다.", "daeum ju geumyoil-kkaji tongbohae deurimnida.", "We will notify you by next Friday."),
               D("지원자", "알겠습니다. 결과를 기다리겠습니다. 좋은 소식이 있었으면 좋겠습니다.", "algesseumnida. gyeolgwa-reul gidarigetseumnida. joeun sosik-i isseosseumyeon jotgesseumnida.", "Understood. I will wait for the result. I hope there is good news."),
               D("면접관", "수고하셨습니다.", "sugohasyeotseumnida.", "Thank you for your time.")],
              WS("Follow-up worksheet", [
                  T("Wait politely.", ["I will wait for the result", "I hope there is good news"],
                    ["결과를 기다리겠습니다", "좋은 소식이 있었으면 좋겠습니다"]),
                  T("Enquire humbly.", ["may I enquire next week?", "we will notify you by next Friday"],
                    ["다음 주에 문의드려도 될까요?", "다음 주 금요일까지 통보해 드립니다"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Korean hiring still carries the shape of the old 공채, the mass open recruitment, "
                 "alongside 수시 hiring for individual posts. A CV is expected to be one page with "
                 "numbers rather than adjectives, and 면접 usually runs as a panel with a fixed set of "
                 "questions asked in a fixed order. Age, military service and graduation year once "
                 "appeared on every form; today they are increasingly left off, and asking about them "
                 "is treated as improper. What has not changed is the expectation that a candidate "
                 "states a range and remains flexible: 협의 가능합니다."),
        source_url="https://en.wikipedia.org/wiki/Economy_of_South_Korea",
        reading=("지난달에 세 곳에 지원했습니다. 두 곳에서는 서류로 떨어졌고, 한 곳에서 면접을 "
                 "보았습니다. 면접에서는 먼저 경력을 설명했습니다. 그다음에 가장 어려웠던 점을 "
                 "물었습니다. 저는 일정 관리가 어려웠다고 말하고, 역할을 나누어 해결한 방법을 "
                 "설명했습니다. 마지막으로 희망 연봉을 물었습니다. 저는 범위를 말하고 협의가 "
                 "가능하다고 답했습니다. 결과는 다음 주에 통보받기로 했습니다."),
        reading_gloss=("Last month I applied to three places. Two rejected me on paper, and I had one "
                       "interview. In the interview I first explained my experience. Then they asked the "
                       "hardest part. I said scheduling had been hard and explained how dividing the "
                       "roles solved it. Finally they asked about salary. I gave a range and said it was "
                       "negotiable. I am to be notified of the result next week."),
        listening=("면접관: 자기 소개를 부탁드립니다.<br>"
                   "지원자: 저는 고객 지원을 삼 년 동안 담당한 미나입니다.<br>"
                   "면접관: 가장 어려웠던 일은 무엇이었습니까?<br>"
                   "지원자: 일정 관리였습니다. 역할을 나누어 해결했습니다.<br>"
                   "면접관: 희망 연봉은 어떻게 되십니까?<br>"
                   "지원자: 삼천만 원쯤 생각하고 있고, 협의 가능합니다."),
        listening_gloss=("Interviewer: Please introduce yourself. Applicant: I am Mina, and I was in "
                         "charge of customer support for three years. Interviewer: What was the hardest "
                         "thing? Applicant: Scheduling. We solved it by dividing the roles. "
                         "Interviewer: What salary are you hoping for? Applicant: Around thirty million "
                         "won, and it is negotiable."),
        voice_tag=VOICE,
        idioms=[
            ("삼 년 동안 담당했어요", "I was in charge for three years", "three years in that role"),
            ("강점은 …라는 점입니다", "my strength is the fact that …", "the way I name a strength"),
            ("말이 느린 편입니다", "I am on the slow side of speaking", "a weakness stated as a tendency"),
            ("해 본 적이 있어요", "have you ever done it?", "do you have that experience?"),
            ("어려웠던 점은 무엇이었어요?", "what was the hard part?", "tell me the difficulty"),
            ("잘 모르지만 확인해 보겠습니다", "I do not know well, but I will check", "an honest answer with a next step"),
            ("희망 연봉이 어떻게 되세요?", "what is your hoped-for salary?", "what are your salary expectations?"),
            ("협의 가능합니다", "negotiation is possible", "the salary is negotiable"),
            ("입사 시기를 조정하다", "to adjust the joining date", "to move the start date"),
            ("결과를 기다리겠습니다", "I will wait for the result", "I look forward to your decision"),
        ],
        mistakes=[
            ("제 강점은 꼼꼼합니다.", "제 강점은 꼼꼼하다는 점입니다.", "A strength is named as a clause with -는 점이다."),
            ("삼 년을 담당했습니다.", "삼 년 동안 담당했습니다.", "A duration takes 동안, not 을/를."),
            ("연봉이 얼마예요?", "희망 연봉이 어떻게 되세요?", "Salary is asked for as a hope, in the polite 어떻게 되세요 form."),
        ],
        task_title="Write a one-page CV and a ten-line interview",
        task_instructions=("Draft four CV lines in 합니다체, each with a duty, a period and one number. Then "
                           "write a ten-line interview: introduction, two questions with evidence-based "
                           "answers, one question you answer with 잘 모르지만, and the salary exchange in "
                           "which you give a range and say 협의 가능합니다."),
    ),
    "test": [
        ("translate_en", "Say: I was in charge of customer support for three years.", "삼 년 동안 고객 지원을 담당했습니다."),
        ("translate_ko", "가장 어려웠던 점은 일정이었습니다.", "The hardest part was the schedule."),
        ("multiple_choice", "Which sentence names a strength the interview way?", "제 강점은 문제를 끝까지 확인한다는 점입니다."),
        ("fill_in_the_blank", "삼 년___ 담당했습니다.", "동안"),
        ("word_selection", "Select the Korean for 'the salary is negotiable'.", "협의 가능합니다"),
        ("error_correction", "고객 응대를 해 봤어요 있었다.", "고객 응대를 해 본 적이 있습니다."),
        ("dialogue_completion", "Complete: 희망 연봉이 어떻게 되세요? — ___ (around thirty million won, negotiable)", "삼천만 원쯤이고 협의 가능합니다"),
        ("matching", "Match 실적 to its meaning.", "performance, results"),
        ("reading_comprehension", "두 곳에서는 서류로 떨어졌습니다. What happened at two of the places?", "rejected on paper"),
        ("inference", "잘 모르지만 확인해 보겠습니다. — what does the candidate do?", "admits not knowing and promises to check"),
        ("main_idea", "역할을 나누어 일정 문제를 해결했습니다. What is the candidate describing?", "how the team solved a scheduling problem"),
        ("detail_identification", "결과는 다음 주에 통보받기로 했습니다. When will the result come?", "next week"),
    ],
}

HALFSTEPS["B2+"] = {
    "title": "Korean B2+ — Contract and negotiation",
    "native": NATIVE,
    "goals": [
        "Read a contract clause and name what it requires or forbids",
        "Trade a concession for a condition instead of giving it away",
        "Write the one sentence both sides can sign",
    ],
    "units": [
        {"id": "B2+-U1", "title": "계약 조건", "lessons": [
            L("조항을 확인해요",
              "A clause states what must be done: 다음 달까지 납품하도록 명시되어 있습니다. The "
              "requirement takes -도록, and 명시하다 is what the document does.",
              [V("조항", "johang", "clause", "noun"),
               V("명시하다", "myeongsihada", "to specify, to state", "verb"),
               V("기한", "gihan", "deadline, term", "noun"),
               V("납품", "napum", "delivery of goods", "noun"),
               V("갱신", "gaengsin", "renewal", "noun")],
              G("What a clause requires",
                "납품하도록 명시되어 있습니다 · 기한은 다음 달입니다 · 갱신은 양쪽 동의가 필요합니다",
                "-도록 states what the clause requires of you, and it pairs with the passive 명시되어 "
                "있다, because the document is what specifies. A requirement that needs agreement "
                "takes 이/가 필요하다.",
                [X("다음 달까지 납품하도록 명시되어 있습니다.", "daeum dal-kkaji napumhadodorok myeongsidoeeo itseumnida.", "It is specified that delivery is due by next month."),
                 X("갱신은 양쪽 동의가 필요합니다.", "gaengsin-eun yangjjok dong-ui-ga piryohamnida.", "Renewal requires the agreement of both sides."),
                 X("기한을 넘기면 위약금이 있습니다.", "gihan-eul neomgimyeon wiyakgeum-i itseumnida.", "If the deadline is passed there is a penalty.")],
                [("다음 달까지 납품합니다 명시합니다.", "다음 달까지 납품하도록 명시되어 있습니다.", "A requirement in a document takes -도록 with the passive 명시되어 있다."),
                 ("갱신이 필요합니다 동의.", "갱신은 양쪽 동의가 필요합니다.", "The thing required takes 이/가: 동의가 필요하다.")]),
              [D("지훈", "이 조항을 함께 확인해 주시겠습니까?", "i johang-eul hamkke hwagin-hae jusigetseumnikka?", "Could we check this clause together?"),
               D("담당자", "네, 다음 달까지 납품하도록 명시되어 있습니다.", "ne, daeum dal-kkaji napumhadodorok myeongsidoeeo itseumnida.", "Yes, it specifies delivery by next month."),
               D("지훈", "기한을 넘기면 어떻게 됩니까?", "gihan-eul neomgimyeon eotteoke doemnikka?", "What happens if the deadline is missed?"),
               D("담당자", "위약금이 있고, 갱신도 양쪽 동의가 필요합니다.", "wiyakgeum-i itgo, gaengsindo yangjjok dong-ui-ga piryohamnida.", "There is a penalty, and renewal also needs both sides to agree.")],
              WS("Clause worksheet", [
                  T("State the requirement.", ["it is specified that delivery is due by next month", "renewal requires agreement from both sides"],
                    ["다음 달까지 납품하도록 명시되어 있습니다", "갱신은 양쪽 동의가 필요합니다"]),
                  T("Ask about consequences.", ["what happens if the deadline is missed?", "there is a penalty"],
                    ["기한을 넘기면 어떻게 됩니까?", "위약금이 있습니다"]),
              ])),
            L("기한과 지연",
              "Delay is admitted and dated: 이 주 지연될 수 있습니다. -ㄹ 경우에는 covers the "
              "conditional case, and 연장 is the extension you ask for in writing.",
              [V("지연", "jiyeon", "delay", "noun"),
               V("연장", "yeonjang", "extension", "noun"),
               V("지체", "jiche", "delay, holdup", "noun"),
               V("통보", "tongbo", "notice", "noun"),
               V("경우", "gyeong-u", "case", "noun")],
              G("Delay and extension",
                "이 주 지연될 수 있습니다 · 지연될 경우에는 통보합니다 · 기한을 연장해 주십시오",
                "Possibility of delay takes -(으)ㄹ 수 있다; the conditional case takes -ㄹ 경우에는. "
                "The extension is requested in writing, and the notice obligation is stated with 통보하다.",
                [X("납품이 이 주 지연될 수 있습니다.", "napum-i i ju jiyeondoel su itseumnida.", "Delivery may be delayed by a week."),
                 X("지연될 경우에는 바로 통보하겠습니다.", "jiyeondoel gyeong-u-eneun baro tongbohagetseumnida.", "If it is delayed I will give notice at once."),
                 X("기한을 이 주 연장해 주십시오.", "gihan-eul i ju yeonjanghae jusipsio.", "Please extend the deadline by a week.")],
                [("지연될 때에는 경우에 통보합니다.", "지연될 경우에는 통보합니다.", "경우 already carries the case; 때 is not stacked on it."),
                 ("기한을 연장합니다 주세요.", "기한을 연장해 주십시오.", "One request form per sentence.")]),
              [D("지훈", "납품이 늦어질 것 같습니다.", "napum-i neujeojil geot gatseumnida.", "The delivery looks like being late."),
               D("담당자", "얼마나 지연됩니까?", "eolmana jiyeondoemnikka?", "How long is the delay?"),
               D("지훈", "일주일쯤 지연될 수 있습니다. 지연될 경우에는 바로 통보하겠습니다.", "iljuil-jjeum jiyeondoel su itseumnida. jiyeondoel gyeong-u-eneun baro tongbohagetseumnida.", "It may be delayed by about a week. If so, I will notify you at once."),
               D("담당자", "그럼 기한을 일주일 연장해 주십시오. 문서로 부탁드립니다.", "geureom gihan-eul iljuil yeonjanghae jusipsio. munjoseo butakdeurimnida.", "Then please extend the deadline by a week — in writing.")],
              WS("Delay worksheet", [
                  T("Admit a delay.", ["delivery may be delayed by a week", "if it is delayed I will give notice at once"],
                    ["납품이 일주일 지연될 수 있습니다", "지연될 경우에는 바로 통보하겠습니다"]),
                  T("Ask for an extension.", ["please extend the deadline by a week", "in writing, please"],
                    ["기한을 일주일 연장해 주십시오", "문서로 부탁드립니다"]),
              ])),
            L("위험을 분담해요",
              "Risk is divided in the clause itself: 위험은 양쪽이 나누어 부담합니다. The condition that "
              "pairs a duty with its limit takes -는 조건으로.",
              [V("위험", "wiheom", "risk", "noun"),
               V("분담", "bundam", "sharing, division (of a burden)", "noun"),
               V("부담하다", "budamhada", "to bear, to shoulder", "verb"),
               V("한도", "hando", "limit, ceiling", "noun"),
               V("보상", "bosang", "compensation", "noun")],
              G("Splitting a risk",
                "위험은 양쪽이 나누어 부담합니다 · 보상 한도는 계약 금액의 십 퍼센트입니다 · 그 조건으로",
                "A duty and its limit are joined with -는 조건으로: 책임을 지는 조건으로 한도를 정합니다. "
                "부담하다 takes the burden as its object, and 한도 is what caps the compensation.",
                [X("위험은 양쪽이 나누어 부담합니다.", "wiheom-eun yangjjok-i nanueo budamhamnida.", "Each side bears part of the risk."),
                 X("보상 한도는 계약 금액의 십 퍼센트입니다.", "bosang hando-neun gyeyak geumaeg-ui sip peosenteu-imnida.", "The compensation ceiling is ten percent of the contract value."),
                 X("한도를 정하는 조건으로 책임을 지겠습니다.", "hando-reul jeonghaneun johang-euro chaegim-eul jigetseumnida.", "I will accept responsibility on condition that a ceiling is set.")],
                [("위험을 부담합니다 양쪽.", "위험은 양쪽이 나누어 부담합니다.", "The risk is the topic; 양쪽 is the subject that bears it."),
                 ("보상이 십 퍼센트입니다 한도.", "보상 한도는 십 퍼센트입니다.", "한도 is what is being capped, so it heads the phrase.")]),
              [D("지훈", "위험은 어떻게 나눕니까?", "wiheom-eun eotteoke nanumnikka?", "How is the risk divided?"),
               D("담당자", "양쪽이 나누어 부담하고, 보상 한도는 계약 금액의 십 퍼센트입니다.", "yangjjok-i nanueo budamhago, bosang hando-neun gyeyak geumaeg-ui sip peosenteu-imnida.", "Both sides share it, and the compensation ceiling is ten percent of the contract value."),
               D("지훈", "한도를 정하는 조건으로 책임을 지겠습니다.", "hando-reul jeonghaneun johang-euro chaegim-eul jigetseumnida.", "I will accept responsibility on condition that a ceiling is set."),
               D("담당자", "그렇게 조항에 넣겠습니다.", "geureoke johang-e neotgetseumnida.", "We will put it into the clause that way.")],
              WS("Risk worksheet", [
                  T("Divide the risk.", ["each side bears part of the risk", "the ceiling is ten percent of the contract value"],
                    ["위험은 양쪽이 나누어 부담합니다", "한도는 계약 금액의 십 퍼센트입니다"]),
                  T("Attach a condition.", ["I will accept responsibility on condition that a ceiling is set", "we will put it into the clause"],
                    ["한도를 정하는 조건으로 책임을 지겠습니다", "조항에 넣겠습니다"]),
              ])),
        ]},
        {"id": "B2+-U2", "title": "협상", "lessons": [
            L("양보와 교환",
              "A concession is traded, not given: 가격을 낮추는 대신에 기한을 늘려 주십시오. The exchange "
              "takes -는 대신에, and 우선순위 says what you will not move.",
              [V("양보", "yangbo", "concession", "noun"),
               V("교환", "gyohwan", "exchange", "noun"),
               V("우선순위", "useonsunwi", "priority", "noun"),
               V("폭", "pok", "range, width", "noun"),
               V("낮추다", "natchuda", "to lower", "verb")],
              G("Trading a concession",
                "가격을 낮추는 대신에 기한을 늘려 주십시오 · 여기서는 양보할 수 없습니다",
                "-는 대신에 names what you receive for what you give, and it needs two real sides. "
                "양보할 수 없습니다 is said together with the reason, never alone, so the negotiation "
                "keeps a next step.",
                [X("가격을 낮추는 대신에 기한을 늘려 주십시오.", "gagyeok-eul natchuneun daesin-e gihan-eul neullyeo jusipsio.", "In exchange for lowering the price, please extend the deadline."),
                 X("이 조건은 양보할 수 없습니다. 대신 다른 항목은 조정할 수 있습니다.", "i jogeon-eun yangbohal su eopseumnida. daesin dareun hangmok-eun jojeonghal su itseumnida.", "This condition cannot be conceded; other items can be adjusted instead."),
                 X("우선순위는 기한입니다.", "useonsunwi-neun gihan-imnida.", "The priority is the deadline.")],
                [("가격을 낮추고 대신에 기한을 늘립니다.", "가격을 낮추는 대신에 기한을 늘립니다.", "대신에 attaches to the clause you give up, in the -는 form."),
                 ("양보할 수 없습니다.", "양보할 수 없지만 다른 항목은 조정할 수 있습니다.", "A flat refusal ends the negotiation; the frame adds the alternative.")]),
              [D("지훈", "가격을 조금 낮춰 주실 수 있습니까?", "gagyeok-eul jogeum natchwo jusil su itseumnikka?", "Could you lower the price a little?"),
               D("담당자", "가격을 낮추는 대신에 기한을 늘려 주십시오.", "gagyeok-eul natchuneun daesin-e gihan-eul neullyeo jusipsio.", "In exchange for lowering the price, extend the deadline."),
               D("지훈", "일주일은 어렵고, 사흘은 가능합니다.", "iljuil-eun eoryeopgo, saheul-eun ganeunghamnida.", "A week is difficult; three days is possible."),
               D("담당자", "그럼 사흘로 하고, 가격은 오 퍼센트 낮추겠습니다.", "geureom saheul-ro hago, gagyeok-eun o peosenteu natchugetseumnida.", "Then three days, and we will lower the price by five percent.")],
              WS("Concession worksheet", [
                  T("Trade one thing for another.", ["in exchange for lowering the price, extend the deadline", "this condition cannot be conceded"],
                    ["가격을 낮추는 대신에 기한을 늘려 주십시오", "이 조건은 양보할 수 없습니다"]),
                  T("Offer a range.", ["a week is difficult; three days is possible", "we will lower the price by five percent"],
                    ["일주일은 어렵고 사흘은 가능합니다", "가격은 오 퍼센트 낮추겠습니다"]),
              ])),
            L("대안을 제시해요",
              "When one option is blocked, the alternatives are laid out with numbers: 두 가지 안이 "
              "있습니다. The recommendation takes -는 편이 낫다.",
              [V("대안", "daean", "alternative", "noun"),
               V("선택지", "seontaekji", "option, choice", "noun"),
               V("제시하다", "jesihada", "to present, to put forward", "verb"),
               V("비교하다", "bigyohada", "to compare", "verb"),
               V("유리하다", "yurihada", "to be advantageous", "adjective")],
              G("Presenting alternatives",
                "두 가지 안이 있습니다 · 비용 면에서 유리합니다 · 이쪽이 나은 편입니다",
                "안 counts a proposal like a counter: 두 가지 안, 세 가지 안. Comparison takes 면: 비용 "
                "면에서, 일정 면에서. A recommendation is stated with -는 편이 낫다.",
                [X("두 가지 안이 있습니다.", "du gaji an-i itseumnida.", "There are two proposals."),
                 X("비용 면에서 첫 번째 안이 유리합니다.", "biyong myeon-eseo cheot beonjae an-i yurihamnida.", "In terms of cost the first proposal is better."),
                 X("일정을 생각하면 이쪽이 나은 편입니다.", "iljeong-eul saenggakhamyeon ijjok-i naeun pyeon-imnida.", "Considering the schedule, this one is the better option.")],
                [("두 개의 안이 있습니다.", "두 가지 안이 있습니다.", "Proposals are counted with 가지, not with the object counter 개."),
                 ("비용에서 유리합니다.", "비용 면에서 유리합니다.", "An aspect takes 면에서: 비용 면에서, 일정 면에서.")]),
              [D("담당자", "이 조건이 어렵다면 다른 방법이 있을까요?", "i jogeon-i eoryeopdamyeon dareun bangbeop-i isseulkkayo?", "If this condition is difficult, is there another way?"),
               D("지훈", "두 가지 안이 있습니다. 먼저 범위를 줄이는 방법입니다.", "du gaji an-i itseumnida. meonjeo beomwi-reul jurineun bangbeop-imnida.", "There are two proposals. The first is to reduce the scope."),
               D("담당자", "두 번째 안은 무엇입니까?", "du beonjae an-eun mueosimnikka?", "What is the second?"),
               D("지훈", "일정을 늘리는 방법입니다. 비용 면에서 보면 첫 번째가 유리합니다.", "iljeong-eul neullineun bangbeop-imnida. biyong myeon-eseo bomyeon cheot beonjae-ga yurihamnida.", "Extending the schedule. In cost terms the first is better.")],
              WS("Alternatives worksheet", [
                  T("Present options.", ["there are two proposals", "in terms of cost the first is more advantageous"],
                    ["두 가지 안이 있습니다", "비용 면에서 첫 번째가 유리합니다"]),
                  T("Recommend one.", ["considering the schedule, this one is better", "the first is to reduce the scope"],
                    ["일정을 생각하면 이쪽이 낫습니다", "먼저 범위를 줄이는 방법입니다"]),
              ])),
            L("조건부로 합의해요",
              "A conditional agreement is one sentence: 이 조건이 지켜지면 합의하겠습니다. 검토 후에 "
              "확정하겠습니다 buys the time without refusing.",
              [V("합의", "habui", "agreement", "noun"),
               V("조건부", "jogeonbu", "conditional", "noun"),
               V("잠정", "jamjeong", "provisional", "noun"),
               V("검토", "geomto", "review, examination", "noun"),
               V("확정하다", "hwakjeonghada", "to finalise, to fix", "verb")],
              G("Agreeing with a condition",
                "이 조건이 지켜지면 합의하겠습니다 · 검토 후에 확정하겠습니다 · 잠정 합의입니다",
                "A condition that must hold takes -면 with the passive 지켜지다: if it is kept. 검토 후에 "
                "puts the review before the decision, and 잠정 marks the agreement as provisional.",
                [X("이 조건이 지켜지면 합의하겠습니다.", "i jogeon-i jikyeojimyeon habuihagetseumnida.", "If this condition is kept, I will agree."),
                 X("검토 후에 확정하겠습니다.", "geomto hue hwakjeonghagetseumnida.", "I will finalise it after review."),
                 X("지금은 잠정 합의로 두겠습니다.", "jigeum-eun jamjeong habui-ro dugesseumnida.", "For now let us leave it as a provisional agreement.")],
                [("이 조건이 지키면 합의합니다.", "이 조건이 지켜지면 합의하겠습니다.", "The condition is what gets kept, so the passive 지켜지다 is used."),
                 ("검토하고 확정합니다 후에.", "검토 후에 확정하겠습니다.", "후에 follows the noun 검토, and it comes before the decision.")]),
              [D("지훈", "오늘 합의할 수 있습니까?", "oneul habuihal su itseumnikka?", "Can we agree today?"),
               D("담당자", "이 조건이 지켜지면 합의하겠습니다.", "i jogeon-i jikyeojimyeon habuihagetseumnida.", "If this condition is kept, we will agree."),
               D("지훈", "확정은 언제 가능합니까?", "hwakjeong-eun eonje ganeunghamnikka?", "When can it be finalised?"),
               D("담당자", "검토 후에 확정하겠습니다. 오늘은 잠정 합의로 두겠습니다.", "geomto hue hwakjeonghagetseumnida. oneul-eun jamjeong habui-ro dugesseumnida.", "We will finalise after review. Today let us leave it as provisional.")],
              WS("Conditional agreement worksheet", [
                  T("Agree with a condition.", ["if this condition is kept, I will agree", "I will finalise after review"],
                    ["이 조건이 지켜지면 합의하겠습니다", "검토 후에 확정하겠습니다"]),
                  T("Keep it provisional.", ["let us leave it as a provisional agreement", "when can it be finalised?"],
                    ["잠정 합의로 두겠습니다", "확정은 언제 가능합니까?"]),
              ])),
        ]},
        {"id": "B2+-U3", "title": "갈등과 중재", "lessons": [
            L("입장 차이를 정리해요",
              "Two positions are laid side by side before anything is decided: 양쪽은 비용에서 다르고, "
              "일정에서는 같습니다. The difference takes -는 점에서 다르다.",
              [V("입장", "ipjang", "position, stance", "noun"),
               V("쟁점", "jaengjeom", "point at issue", "noun"),
               V("차이", "chai", "difference", "noun"),
               V("좁히다", "jophida", "to narrow", "verb"),
               V("정리하다", "jeongnihada", "to lay out, to arrange", "verb")],
              G("Setting out two positions",
                "양쪽은 비용에서 다릅니다 · 쟁점은 세 가지입니다 · 차이를 좁혀 봅시다",
                "-는 점에서 다르다 names the aspect of disagreement, and it is what makes mediation "
                "possible: the same pair is usually identical in most other aspects. 좁히다 is the "
                "verb for narrowing a gap.",
                [X("양쪽은 비용에서 다르고, 일정에서는 같습니다.", "yangjjok-eun biyong-eseo dareugo, iljeong-eseoneun gatseumnida.", "The two sides differ on cost and agree on the schedule."),
                 X("쟁점은 세 가지입니다.", "jaengjeom-eun se gaji-imnida.", "There are three points at issue."),
                 X("먼저 차이를 좁혀 봅시다.", "meonjeo chai-reul jophyeo bopsida.", "Let us first narrow the gap.")],
                [("양쪽이 다릅니다.", "양쪽은 비용에서 다릅니다.", "A difference is named in the aspect where it holds: …에서 다르다."),
                 ("쟁점이 세 개입니다.", "쟁점은 세 가지입니다.", "Points at issue are counted with 가지, not with 개.")]),
              [D("중재자", "지금 쟁점이 무엇입니까?", "jigeum jaengjeom-i mueosimnikka?", "What is the point at issue now?"),
               D("지훈", "양쪽은 비용에서 다르고, 일정에서는 같습니다.", "yangjjok-eun biyong-eseo dareugo, iljeong-eseoneun gatseumnida.", "The two sides differ on cost and agree on the schedule."),
               D("중재자", "그럼 일정부터 확정하고 비용을 이야기합시다.", "geureom iljeong-buteo hwakjeonghago biyong-eul iyagihapsida.", "Then let us fix the schedule first and talk about cost."),
               D("지훈", "좋습니다. 그렇게 하면 차이를 좁히기 쉽습니다.", "jotseumnida. geureoke hamyeon chai-reul jophigi swip-seumnida.", "Good. That way the gap is easier to narrow.")],
              WS("Positions worksheet", [
                  T("Lay out the positions.", ["the two sides differ on cost and agree on the schedule", "there are three points at issue"],
                    ["양쪽은 비용에서 다르고 일정에서는 같습니다", "쟁점은 세 가지입니다"]),
                  T("Narrow the gap.", ["let us first narrow the gap", "the gap is easier to narrow that way"],
                    ["먼저 차이를 좁혀 봅시다", "그렇게 하면 차이를 좁히기 쉽습니다"]),
              ])),
            L("중재안을 만들어요",
              "A mediation proposal gives each side something it named: 비용은 그대로 두고 범위를 "
              "줄이도록 반영하겠습니다. The form -도록 반영하다 turns a demand into a draft.",
              [V("중재", "jungjae", "mediation", "noun"),
               V("절충", "jeolchung", "compromise", "noun"),
               V("수용하다", "suyonghada", "to accept, to accommodate", "verb"),
               V("반영하다", "banyeonghada", "to reflect, to incorporate", "verb"),
               V("제안", "jean", "proposal", "noun")],
              G("Drafting a mediation proposal",
                "비용은 그대로 두고 범위를 줄이도록 반영하겠습니다 · 양쪽 요구를 절충했습니다",
                "-도록 반영하다 records a demand as something to be incorporated, which commits nobody "
                "yet. 양쪽 요구 is the object of 절충하다, and 수용하다 is what each side does with the "
                "draft.",
                [X("비용은 그대로 두고 범위를 줄이도록 반영하겠습니다.", "biyong-eun geudaero dugo beomwi-reul juridorok banyeonghagetseumnida.", "We will keep the cost as it is and incorporate a reduction in scope."),
                 X("양쪽 요구를 절충한 안입니다.", "yangjjok yogu-reul jeolchunghan an-imnida.", "This is a proposal that compromises both sides' demands."),
                 X("이 안을 수용할 수 있습니까?", "i an-eul suyonghal su isseumnikka?", "Can you accept this proposal?")],
                [("범위를 줄입니다 반영합니다.", "범위를 줄이도록 반영하겠습니다.", "A demand to be incorporated takes -도록 with 반영하다."),
                 ("양쪽 요구를 절충합니다 안.", "양쪽 요구를 절충한 안입니다.", "The compromise modifies the proposal: 절충한 안.")]),
              [D("중재자", "중재안을 만들어 보겠습니다.", "jungjaean-eul mandeureo bogetseumnida.", "Let me draft a mediation proposal."),
               D("지훈", "비용은 그대로 두고 범위를 줄이도록 반영하겠습니다.", "biyong-eun geudaero dugo beomwi-reul juridorok banyeonghagetseumnida.", "We will keep the cost as it is and incorporate a reduced scope."),
               D("담당자", "일정은 어떻게 됩니까?", "iljeong-eun eotteoke doemnikka?", "What about the schedule?"),
               D("중재자", "일정은 이 주 늘리는 것으로 넣었습니다. 이 안을 수용할 수 있습니까?", "iljeong-eun i ju neullineun geoseuro neoeotseumnida. i an-eul suyonghal su isseumnikka?", "The schedule has been extended by a week in the draft. Can you accept it?")],
              WS("Mediation worksheet", [
                  T("Draft the proposal.", ["we will keep the cost and reduce the scope", "this compromises both sides' demands"],
                    ["비용은 그대로 두고 범위를 줄이도록 반영하겠습니다", "양쪽 요구를 절충한 안입니다"]),
                  T("Ask for acceptance.", ["can you accept this proposal?", "the schedule has been extended by a week"],
                    ["이 안을 수용할 수 있습니까?", "일정은 이 주 늘렸습니다"]),
              ])),
            L("합의문을 씁니다",
              "The closing sentence of an agreement is written in a flat, impersonal register: 본 계약은 "
              "서명한 날로부터 발효한다. -ㄴ 것으로 한다 fixes what was agreed without naming anybody.",
              [V("합의문", "habuimun", "written agreement", "noun"),
               V("서명", "seomyeong", "signature", "noun"),
               V("발효", "balhyo", "coming into force", "noun"),
               V("명기하다", "myeonggihada", "to state in writing", "verb"),
               V("조항", "johang", "clause", "noun")],
              G("Writing the agreement",
                "서명한 날로부터 발효한다 · 위 내용을 명기한다 · 양쪽이 확인한 것으로 한다",
                "Agreements are written in the plain -ㄴ다/-한다 register, with -ㄴ 것으로 한다 for what "
                "is fixed: 확인한 것으로 한다, it is deemed confirmed. 날로부터 marks the day something "
                "takes effect.",
                [X("본 합의는 서명한 날로부터 발효한다.", "bon habui-neun seomyeonghan nal-lo-buteo balhyohanda.", "This agreement takes effect from the day of signature."),
                 X("위 내용을 조항에 명기한다.", "wi naeyong-eul johang-e myeonggihanda.", "The above is stated in the clause."),
                 X("양쪽이 확인한 것으로 한다.", "yangjjok-i hwaginhan geoseuro handa.", "It is deemed confirmed by both sides.")],
                [("서명한 날부터 발효합니다 한다.", "서명한 날로부터 발효한다.", "One register per agreement: the plain -ㄴ다 form throughout."),
                 ("양쪽이 확인합니다 것으로 합니다.", "양쪽이 확인한 것으로 한다.", "The finalising frame attaches to the modifier form 확인한.")]),
              [D("중재자", "합의문 초안을 읽겠습니다.", "habuimun choan-eul ilgetseumnida.", "I will read the draft agreement."),
               D("지훈", "본 합의는 서명한 날로부터 발효한다.", "bon habui-neun seomyeonghan nal-lo-buteo balhyohanda.", "This agreement takes effect from the day of signature."),
               D("담당자", "기한 연장도 명기했습니까?", "gihan yeonjang-do myeonggi-haetseumnikka?", "Is the extension of the deadline stated too?"),
               D("중재자", "네, 일주일 연장을 조항에 명기하고 양쪽이 확인한 것으로 합니다.", "ne, iljuil yeonjang-eul johang-e myeonggihago yangjjok-i hwaginhan geoseuro hamnida.", "Yes — the one-week extension is stated in the clause and deemed confirmed by both sides.")],
              WS("Agreement worksheet", [
                  T("Write in agreement register.", ["this agreement takes effect from the day of signature", "it is deemed confirmed by both sides"],
                    ["본 합의는 서명한 날로부터 발효한다", "양쪽이 확인한 것으로 한다"]),
                  T("Record what was agreed.", ["the extension is stated in the clause", "the above is stated in the clause"],
                    ["연장을 조항에 명기한다", "위 내용을 조항에 명기한다"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Korean business agreements are written down more than the Korean proverb about words "
                 "would suggest. A 계약서 is read clause by clause, and the 도장 — the personal seal — "
                 "still carries more weight than a signature in many offices, though both are common. "
                 "What negotiators guard is not the headline number but the 기한, because a missed date "
                 "triggers 위약금 and reopens everything else. Mediation is therefore normal rather than "
                 "exceptional, and 잠정 합의, a provisional agreement, is a respectable outcome rather "
                 "than a failure."),
        source_url="https://en.wikipedia.org/wiki/South_Korea",
        reading=("지난주에 계약 협상을 했습니다. 처음에는 비용 때문에 양쪽이 맞서서 회의가 두 시간 "
                 "걸렸습니다. 중재자가 쟁점을 세 가지로 정리했습니다. 그리고 나서 차이를 좁혔습니다. "
                 "우리는 비용을 그대로 두고 범위를 줄이는 대신에 기한을 일주일 늘렸습니다. 합의문에는 "
                 "그 내용을 조항에 명기했습니다. 발효일은 서명한 날로 정했습니다. 아직 잠정 합의지만 "
                 "양쪽이 같은 문서를 가지고 있습니다."),
        reading_gloss=("Last week we negotiated a contract. At first the two sides were opposed over cost "
                       "and the meeting took two hours. The mediator laid out the points at issue as "
                       "three. Then we narrowed the gap. We kept the cost as it was, reduced the scope "
                       "and in exchange extended the deadline by a week. The agreement states that in "
                       "the clause. The effective date is set as the day of signature. It is still a "
                       "provisional agreement, but both sides hold the same document."),
        listening=("중재자: 오늘 결정할 수 있는 부분부터 정리하겠습니다.<br>"
                   "지훈: 범위를 줄이면 기한은 지킬 수 있습니다.<br>"
                   "담당자: 범위를 줄이는 것은 받아들일 수 있습니다. 다만 발효일을 명확히 하고 싶습니다.<br>"
                   "중재자: 서명한 날로부터 발효하는 것으로 명기하겠습니다.<br>"
                   "지훈: 그러면 잠정 합의로 두고, 다음 주에 확정하겠습니다."),
        listening_gloss=("Mediator: Let us settle the parts we can decide today. Jihun: If we reduce the "
                         "scope, the deadline can be met. Counterpart: Reducing the scope is acceptable, "
                         "but I want the effective date to be clear. Mediator: We will state that it "
                         "takes effect from the day of signature. Jihun: Then let us leave it as a "
                         "provisional agreement and finalise next week."),
        voice_tag=VOICE,
        idioms=[
            ("기한을 넘기면 위약금이 있습니다", "if the date is passed there is a penalty", "miss the deadline and you pay"),
            ("지연될 경우에는 통보합니다", "in the case of delay we give notice", "we will tell you if it slips"),
            ("기한을 연장해 주십시오", "please extend the deadline", "we need more time"),
            ("양쪽이 나누어 부담합니다", "both sides bear it in parts", "the risk is shared"),
            ("가격을 낮추는 대신에", "in exchange for lowering the price", "the price falls, something else moves"),
            ("양보할 수 없습니다", "it cannot be conceded", "that is our line"),
            ("두 가지 안이 있습니다", "there are two proposals", "you have a choice"),
            ("차이를 좁히다", "to narrow the gap", "to move the two sides closer"),
            ("잠정 합의로 두다", "to leave it as a provisional agreement", "agreed in outline"),
            ("서명한 날로부터 발효한다", "it takes effect from the day of signature", "the agreement starts on signature"),
        ],
        mistakes=[
            ("두 개의 안이 있습니다.", "두 가지 안이 있습니다.", "Proposals are counted with 가지, not 개."),
            ("비용에서 유리합니다.", "비용 면에서 유리합니다.", "An aspect of comparison takes 면에서."),
            ("이 조건이 지키면 합의합니다.", "이 조건이 지켜지면 합의하겠습니다.", "The condition is what is kept, so it takes the passive 지켜지다."),
        ],
        task_title="Negotiate a contract you would sign",
        task_instructions=("Write a six-line negotiation: your priority, one concession with -는 대신에, "
                           "one line you will not cross with 양보할 수 없습니다, two alternatives counted with "
                           "가지, and a closing conditional agreement with 지켜지면. Then write the one "
                           "sentence of the 합의문 that fixes what you agreed."),
    ),
    "test": [
        ("translate_en", "Say: It is specified that delivery is due by next month.", "다음 달까지 납품하도록 명시되어 있습니다."),
        ("translate_ko", "가격을 낮추는 대신에 기한을 늘려 주십시오.", "In exchange for lowering the price, please extend the deadline."),
        ("multiple_choice", "Which sentence states a condition for agreeing?", "이 조건이 지켜지면 합의하겠습니다."),
        ("fill_in_the_blank", "보상 ___는 계약 금액의 십 퍼센트입니다.", "한도"),
        ("word_selection", "Select the Korean for 'the risk is shared'.", "위험은 양쪽이 나누어 부담합니다"),
        ("error_correction", "두 개의 안이 있습니다.", "두 가지 안이 있습니다."),
        ("dialogue_completion", "Complete: 확정은 언제 가능합니까? — ___ (we will finalise after review)", "검토 후에 확정하겠습니다"),
        ("matching", "Match 쟁점 to its meaning.", "point at issue"),
        ("reading_comprehension", "회의가 두 시간 걸린 이유가 무엇이었습니까?", "the two sides were opposed over cost"),
        ("inference", "아직 잠정 합의지만 양쪽이 같은 문서를 가지고 있습니다. — what does this suggest?", "the agreement is not final but both sides hold the same text"),
        ("main_idea", "본 합의는 서명한 날로부터 발효한다. What is this sentence?", "the effective-date clause of an agreement"),
        ("detail_identification", "기한은 얼마나 늘렸습니까?", "one week"),
    ],
}

HALFSTEPS["C1+"] = {
    "title": "Korean C1+ — Synthesis and citation",
    "native": NATIVE,
    "goals": [
        "Summarise a body of research and name where the studies diverge",
        "Quote, paraphrase and attribute without slipping into plagiarism",
        "State the limits of your own conclusion and leave the open question standing",
    ],
    "units": [
        {"id": "C1+-U1", "title": "문헌 종합", "lessons": [
            L("선행 연구를 정리해요",
              "A literature review arranges studies rather than listing them: 초기 연구는 A를 "
              "다루었고, 이후 연구는 B로 옮겨 갔다. The reporting frame stays in -다고 한다.",
              [V("선행 연구", "seonhaeng yeon-gu", "previous research", "noun"),
               V("요약하다", "yoyakhada", "to summarise", "verb"),
               V("분류하다", "bunryuhada", "to classify", "verb"),
               V("흐름", "heureum", "current, trend", "noun"),
               V("정리하다", "jeongnihada", "to arrange, to lay out", "verb")],
              G("Arranging a body of work",
                "초기 연구는 …을 다루었다 · 이후 연구는 …로 옮겨 갔다 · …라고 요약할 수 있다",
                "The written register keeps the plain past -었다 for what earlier work did, and the "
                "reporting frame -라고 요약할 수 있다 for the reviewer's own summary. Flow is described "
                "with 옮겨 가다 rather than a list of authors.",
                [X("초기 연구는 비용 문제를 다루었다.", "chogi yeon-gu-neun biyong munje-reul darueotda.", "Early research dealt with the question of cost."),
                 X("이후 연구는 제도 설계로 옮겨 갔다.", "ihu yeon-gu-neun jedo seolgye-ro omgyeo gatda.", "Later work moved to institutional design."),
                 X("전체 흐름은 세 갈래로 요약할 수 있다.", "jeonche heureum-eun se galrae-ro yoyakhal su itda.", "The overall trend can be summarised as three strands.")],
                [("초기 연구는 비용을 다룹니다 요약합니다.", "초기 연구는 비용 문제를 다루었다.", "One register and one predicate: the written past is -었다."),
                 ("연구가 세 갈래입니다 요약합니다.", "연구는 세 갈래로 요약할 수 있다.", "The summary frame takes -(으)로 on the classification.")]),
              [D("지도 교수", "선행 연구의 흐름이 어떻게 됩니까?", "seonhaeng yeon-gu-ui heureum-i eotteoke doemnikka?", "How does the previous research run?"),
               D("연구자", "초기 연구는 비용을 다루었고, 이후 연구는 제도 설계로 옮겨 갔습니다.", "chogi yeon-gu-neun biyong-eul darueotgo, ihu yeon-gu-neun jedo seolgye-ro omgyeo gatseumnida.", "Early work dealt with cost; later work moved to institutional design."),
               D("지도 교수", "그 흐름을 한 문장으로 요약하면?", "geu heureum-eul han munjang-euro yoyakhamyeon?", "Summarise that in one sentence?"),
               D("연구자", "전체 흐름은 세 갈래로 요약할 수 있습니다.", "jeonche heureum-eun se galrae-ro yoyakhal su itseumnida.", "The whole trend can be summarised as three strands.")],
              WS("Literature worksheet", [
                  T("Describe the flow.", ["early research dealt with the question of cost", "later work moved to institutional design"],
                    ["초기 연구는 비용 문제를 다루었다", "이후 연구는 제도 설계로 옮겨 갔다"]),
                  T("Summarise.", ["the overall trend can be summarised as three strands", "how does the research run?"],
                    ["전체 흐름은 세 갈래로 요약할 수 있다", "선행 연구의 흐름이 어떻게 됩니까?"]),
              ])),
            L("연구 사이의 차이를 밝혀요",
              "Divergence is stated as an aspect, not a winner: A는 표본에서 B와 다르다. 반면에 "
              "contrasts inside a sentence, and -와 달리 attaches the comparison to a noun.",
              [V("차이", "chai", "difference", "noun"),
               V("방법론", "bangbeomnon", "methodology", "noun"),
               V("표본", "pyobon", "sample", "noun"),
               V("대조하다", "daejohada", "to contrast", "verb"),
               V("관점", "gwanjeom", "point of view", "noun")],
              G("Naming a divergence",
                "표본에서 B와 다르다 · 반면에 결론은 같다 · B와 달리 A는 …을 포함했다",
                "A difference takes the aspect with 에서: 표본에서 다르다. 반면에 puts two findings in "
                "opposition within one sentence, and -와 달리 accepts a noun on its left and continues "
                "into the finding.",
                [X("A는 표본에서 B와 다르다.", "A-neun pyobon-eseo B-wa dareuda.", "A differs from B in its sample."),
                 X("방법론은 다르지만 결론은 같다.", "bangbeomnon-eun dareujiman gyeollon-eun gatda.", "The methodology differs, but the conclusion is the same."),
                 X("B와 달리 A는 지방 사례를 포함했다.", "B-wa dalli A-neun jibang sarye-reul pohamhaetda.", "Unlike B, A included provincial cases.")],
                [("A가 B보다 다릅니다.", "A는 표본에서 B와 다르다.", "Difference between studies is named in the aspect where it lies: …에서 다르다."),
                 ("B와 달리에서 A는 포함했다.", "B와 달리 A는 포함했다.", "달리 attaches directly to the noun it compares with.")]),
              [D("연구자", "두 연구의 차이가 어디에 있습니까?", "du yeon-gu-ui chai-ga eodi-e isseumnikka?", "Where do the two studies differ?"),
               D("지도 교수", "표본에서 다릅니다. A는 전국 자료를 썼고, B는 한 지역만 봤습니다.", "pyobon-eseo dareumnida. A-neun jeonguk jaryo-reul sseotgo, B-neun han jiyeok-man bwatseumnida.", "In the sample. A used national data; B looked at one region."),
               D("연구자", "그러면 결론도 다릅니까?", "geureomyeon gyeollondo dareumnikka?", "Then do the conclusions differ as well?"),
               D("지도 교수", "아닙니다. 방법론은 다르지만 결론은 같습니다.", "animnida. bangbeomnon-eun dareujiman gyeollon-eun gatseumnida.", "No. The methodology differs, but the conclusion is the same.")],
              WS("Divergence worksheet", [
                  T("Name the difference.", ["A differs from B in its sample", "the methodology differs but the conclusion is the same"],
                    ["A는 표본에서 B와 다르다", "방법론은 다르지만 결론은 같다"]),
                  T("Contrast with a noun.", ["unlike B, A included provincial cases", "B looked at one region only"],
                    ["B와 달리 A는 지방 사례를 포함했다", "B는 한 지역만 보았다"]),
              ])),
            L("연구의 빈틈을 찾아요",
              "A gap is what the literature did not do: 아직 다루지 않았다. -ㄹ 필요가 있다 proposes the "
              "work without claiming it has been done.",
              [V("빈틈", "binteum", "gap, opening", "noun"),
               V("한계", "hangye", "limitation", "noun"),
               V("다루다", "daruda", "to deal with, to cover", "verb"),
               V("남다", "namda", "to remain", "verb"),
               V("필요", "piry", "need", "noun")],
              G("Pointing at a gap",
                "아직 다루지 않았다 · 한계로 남아 있다 · 후속 연구가 필요하다",
                "The gap is stated as a negative in the written past, and what remains takes -로 남아 "
                "있다. 후속 연구가 필요하다 proposes the next study without asserting its answer.",
                [X("이 쟁점은 아직 다루지 않았다.", "i jaengjeom-eun ajik daruji anatda.", "This question has not yet been covered."),
                 X("표본의 한계로 남아 있다.", "pyobon-ui hangye-ro nama itda.", "It remains as a limitation of the sample."),
                 X("후속 연구가 필요하다.", "husok yeon-gu-ga piryohada.", "Follow-up research is needed.")],
                [("이 쟁점을 다루지 않았다 없다.", "이 쟁점은 아직 다루지 않았다.", "One negative and one predicate; the gap is the topic."),
                 ("한계가 필요합니다.", "한계로 남아 있습니다.", "A limitation is what remains, not what is needed.")]),
              [D("지도 교수", "이 분야에서 아직 다루지 않은 것은 무엇입니까?", "i bunya-eseo ajik daruji aneun geos-eun mueosimnikka?", "What has not yet been covered in this field?"),
               D("연구자", "장기 자료가 없습니다. 표본의 한계로 남아 있습니다.", "janggi jaryo-ga eopseumnida. pyobon-ui hangye-ro nama itseumnida.", "There is no long-term data. It remains a limitation of the sample."),
               D("지도 교수", "그러면 어떤 연구가 필요합니까?", "geureomyeon eotteon yeon-gu-ga piryohamnikka?", "Then what research is needed?"),
               D("연구자", "같은 지역을 십 년간 추적하는 후속 연구가 필요합니다.", "gateun jiyeok-eul sip nyeon-gan chujjeokhaneun husok yeon-gu-ga piryohamnida.", "Follow-up research tracking the same region for ten years.")],
              WS("Gap worksheet", [
                  T("State the gap.", ["this question has not yet been covered", "it remains a limitation of the sample"],
                    ["이 쟁점은 아직 다루지 않았다", "표본의 한계로 남아 있다"]),
                  T("Propose the next study.", ["follow-up research is needed", "there is no long-term data"],
                    ["후속 연구가 필요하다", "장기 자료가 없다"]),
              ])),
        ]},
        {"id": "C1+-U2", "title": "인용과 각주", "lessons": [
            L("직접 인용과 간접 인용",
              "A direct quotation keeps the words and the quotation marks; a paraphrase keeps the "
              "meaning and the attribution: 김(2020)은 …라고 보았다.",
              [V("직접 인용", "jikjeop inyong", "direct quotation", "noun"),
               V("간접 인용", "ganjeop inyong", "indirect quotation", "noun"),
               V("따옴표", "ttaeompyo", "quotation marks", "noun"),
               V("밝히다", "balkida", "to state, to make clear", "verb"),
               V("요약하다", "yoyakhada", "to summarise", "verb")],
              G("Quoting and paraphrasing",
                "김(2020)은 …라고 밝혔다 · 같은 연구는 …라고 요약할 수 있다 · 따옴표 안에는 원문만",
                "The name and year open the sentence, the quote follows in -라고, and the verb says whose "
                "act it was: 밝혔다 for the author's own claim, 요약할 수 있다 for your reading of it.",
                [X("김(2020)은 이 흐름이 일시적이라고 밝혔다.", "gim(2020)-eun i heureum-i ilsijeogirago balkyeotda.", "Kim (2020) stated that the trend was temporary."),
                 X("같은 연구는 원인이 복수라고 요약할 수 있다.", "gateun yeon-gu-neun wonin-i boksu-rago yoyakhal su itda.", "The same study can be summarised as saying the causes are multiple."),
                 X("따옴표 안에는 원문만 넣는다.", "ttaeompyo an-eneun wonmun-man neotneunda.", "Only the original wording goes inside quotation marks.")],
                [("김(2020)은 일시적입니다라고 밝혔다.", "김(2020)은 일시적이라고 밝혔다.", "Quoted speech takes the plain form before -라고, not 습니다."),
                 ("김(2020)이 밝혔다 요약했다.", "김(2020)은 …라고 밝혔다.", "One attribution verb per sentence.")]),
              [D("지도 교수", "이 문장은 직접 인용입니까?", "i munjang-eun jikjeop inyong-imnikka?", "Is this sentence a direct quotation?"),
               D("연구자", "아닙니다. 간접 인용이고, 김(2020)은 …라고 밝혔습니다.", "animnida. ganjeop inyong-igo, gim(2020)-eun …rago balkyeotseumnida.", "No. It is a paraphrase, and Kim (2020) stated that …"),
               D("지도 교수", "그러면 따옴표는 필요합니까?", "geureomyeon ttaeompyo-neun piryohamnikka?", "Then are the quotation marks needed?"),
               D("연구자", "아닙니다. 원문을 그대로 옮길 때만 씁니다.", "animnida. wonmun-eul geudaero omgil ttae-man sseumnida.", "No. They are used only when the original wording is carried over.")],
              WS("Quotation worksheet", [
                  T("Quote and paraphrase.", ["Kim (2020) stated that the trend was temporary", "only the original wording goes inside quotation marks"],
                    ["김(2020)은 이 흐름이 일시적이라고 밝혔다", "따옴표 안에는 원문만 넣는다"]),
                  T("Name the type.", ["it is a paraphrase", "the quotation marks are not needed"],
                    ["간접 인용입니다", "따옴표는 필요하지 않습니다"]),
              ])),
            L("각주를 달아요",
              "A footnote points at a page of a source: 김(2020), 45쪽에서 인용. The source verb is "
              "인용하다 and the location takes 에서.",
              [V("각주", "gakju", "footnote", "noun"),
               V("참고 문헌", "chamgo munheon", "references, bibliography", "noun"),
               V("출처", "chulcheo", "source", "noun"),
               V("인용하다", "inyonghada", "to quote, to cite", "verb"),
               V("쪽", "jjok", "page", "noun")],
              G("Footnote practice",
                "김(2020), 45쪽에서 인용 · 참고 문헌에 밝힌다 · 출처를 표시한다",
                "The citation gives author, year and page, and the page takes 에서 with the verb "
                "인용하다. Everything that appears in a footnote must also appear in 참고 문헌.",
                [X("김(2020), 45쪽에서 인용.", "gim(2020), sasip-o jjok-eseo inyong.", "Quoted from Kim (2020), page 45."),
                 X("모든 출처는 참고 문헌에 밝힌다.", "modeun chulcheo-neun chamgo munheon-e balkinda.", "Every source is stated in the references."),
                 X("표를 인용할 때도 출처를 표시한다.", "pyo-reul inyonghal ttaedo chulcheo-reul pyosihanda.", "When a table is cited the source is marked too.")],
                [("김(2020) 45쪽을 인용.", "김(2020), 45쪽에서 인용.", "A page location takes 에서 before 인용하다."),
                 ("출처를 밝힙니다 참고 문헌.", "출처를 참고 문헌에 밝힌다.", "The references are where the source is given: 참고 문헌에 밝히다.")]),
              [D("지도 교수", "이 각주에 쪽수가 있습니까?", "i gakju-e jjoksuga isseumnikka?", "Does this footnote give the page?"),
               D("연구자", "네, 김(2020), 45쪽에서 인용했습니다.", "ne, gim(2020), sasip-o jjok-eseo inyonghaetseumnida.", "Yes, quoted from Kim (2020), page 45."),
               D("지도 교수", "참고 문헌에도 같은 자료가 있습니까?", "chamgo munheon-edo gateun jaryo-ga isseumnikka?", "Is the same source in the references?"),
               D("연구자", "네, 모든 출처를 참고 문헌에 밝혔습니다.", "ne, modeun chulcheo-reul chamgo munheon-e balkyeotseumnida.", "Yes, every source is stated in the references.")],
              WS("Footnote worksheet", [
                  T("Cite a location.", ["quoted from Kim (2020), page 45", "every source is stated in the references"],
                    ["김(2020), 45쪽에서 인용했다", "모든 출처는 참고 문헌에 밝힌다"]),
                  T("Mark the source.", ["the source is marked for tables too", "does this footnote give the page?"],
                    ["표를 인용할 때도 출처를 표시한다", "이 각주에 쪽수가 있습니까?"]),
              ])),
            L("표절을 피해요",
              "Paraphrase means rewriting the sentence and keeping the citation: 문장을 바꾸고 출처를 "
              "붙인다. Changing words while keeping the structure is still 표절.",
              [V("표절", "pyojeol", "plagiarism", "noun"),
               V("표시하다", "pyosihada", "to mark, to indicate", "verb"),
               V("바꿔 쓰다", "bakwo sseuda", "to rewrite", "phrase"),
               V("검증하다", "geomjeunghada", "to verify", "verb"),
               V("그대로", "geudaero", "as it is, verbatim", "adverb")],
              G("Rewriting without stealing",
                "문장을 바꾸고 출처를 붙인다 · 단어만 바꾸면 표절이다 · 그대로 옮기면 따옴표를 쓴다",
                "Paraphrase changes the sentence and keeps the attribution; swapping synonyms inside "
                "the original structure does not. A verbatim span takes quotation marks as well as a "
                "citation.",
                [X("문장을 바꾸고 출처를 붙인다.", "munjang-eul bakkugo chulcheo-reul butinda.", "Rewrite the sentence and attach the source."),
                 X("단어만 바꾸면 표절이다.", "daneo-man bakkumyeon pyojeorida.", "Changing only the words is plagiarism."),
                 X("그대로 옮긴 부분은 따옴표로 표시한다.", "geudaero omgin bubun-eun ttaeompyo-ro pyosihanda.", "A verbatim span is marked with quotation marks.")],
                [("단어를 바꿨으니 표절이 아니다.", "단어만 바꾸면 표절이다.", "The test is the sentence and the citation, not the synonym."),
                 ("출처를 붙입니다 씁니다.", "출처를 붙인다.", "One predicate per sentence.")]),
              [D("지도 교수", "이 문단은 원문과 무엇이 다릅니까?", "i munjandan-eun wonmun-gwa mueos-i dareumnikka?", "How does this paragraph differ from the original?"),
               D("연구자", "문장 구조를 바꾸고 출처를 붙였습니다.", "munjang gujo-reul bakkugo chulcheo-reul butyeotseumnida.", "I rewrote the sentence structure and attached the source."),
               D("지도 교수", "단어만 바꾸면 어떻게 됩니까?", "daneo-man bakkumyeon eotteoke doemnikka?", "What happens if only the words are changed?"),
               D("연구자", "그때는 표절로 봅니다. 그래서 구조를 먼저 바꿉니다.", "geuttaeneun pyojeol-ro bomnida. geuraeseo gujo-reul meonjeo bakkumnida.", "Then it counts as plagiarism. So I change the structure first.")],
              WS("Paraphrase worksheet", [
                  T("Rewrite properly.", ["rewrite the sentence and attach the source", "changing only the words is plagiarism"],
                    ["문장을 바꾸고 출처를 붙인다", "단어만 바꾸면 표절이다"]),
                  T("Mark the verbatim.", ["a verbatim span is marked with quotation marks", "the structure is changed first"],
                    ["그대로 옮긴 부분은 따옴표로 표시한다", "구조를 먼저 바꾼다"]),
              ])),
        ]},
        {"id": "C1+-U3", "title": "논증의 한계", "lessons": [
            L("반증 가능성을 따져요",
              "A claim worth making can be wrong, and it says how: 이 결과가 나오면 가설은 기각된다. "
              "The frame is -면 기각된다, and 검증 is what the design must allow.",
              [V("반증", "banjeung", "disproof, falsification", "noun"),
               V("가설", "gaseol", "hypothesis", "noun"),
               V("기각하다", "gigakhada", "to reject (a hypothesis)", "verb"),
               V("검증", "geomjeung", "verification, testing", "noun"),
               V("가능성", "ganeungseong", "possibility", "noun")],
              G("Falsifiability",
                "이 결과가 나오면 가설은 기각된다 · 검증이 가능한 형태로 쓴다 · 반증 가능성이 없다",
                "A falsifiable claim states in advance what would defeat it, with -면 and 기각되다. "
                "What cannot be defeated is 반증 가능성이 없다, which in Korean academic prose is a "
                "criticism rather than a compliment.",
                [X("이 결과가 나오면 가설은 기각된다.", "i gyeolgwa-ga naomyeon gaseol-eun gigakdoenda.", "If this result appears the hypothesis is rejected."),
                 X("검증이 가능한 형태로 쓴다.", "geomjeung-i ganeunghan hyeongtae-ro sseunda.", "State it in a form that can be tested."),
                 X("반증 가능성이 없는 주장은 검증할 수 없다.", "banjeung ganeungseong-i eomneun jujang-eun geomjeunghal su eopda.", "A claim that cannot be disproved cannot be tested.")],
                [("가설은 틀리지 않습니다.", "가설은 기각될 수 있습니다.", "A hypothesis that cannot fail cannot be tested; state what would reject it."),
                 ("결과가 나오면 기각합니다 가설.", "그 결과가 나오면 가설은 기각된다.", "The hypothesis is the topic and the subject of the passive.")]),
              [D("지도 교수", "이 가설이 틀렸다는 것을 어떻게 알 수 있습니까?", "i gaseol-i teullyeotdaneun geos-eul eotteoke al su isseumnikka?", "How would you know this hypothesis was wrong?"),
               D("연구자", "이 결과가 나오면 가설은 기각됩니다.", "i gyeolgwa-ga naomyeon gaseol-eun gigakdoemnida.", "If this result appears the hypothesis is rejected."),
               D("지도 교수", "그 조건을 먼저 밝혀야 합니까?", "geu jogeon-eul meonjeo balkyeoya hamnikka?", "Must that condition be stated first?"),
               D("연구자", "네, 검증이 가능한 형태로 먼저 써야 합니다.", "ne, geomjeung-i ganeunghan hyeongtae-ro meonjeo sseoya hamnida.", "Yes — it must be written first in a form that can be tested.")],
              WS("Falsification worksheet", [
                  T("State what would defeat it.", ["if this result appears the hypothesis is rejected", "state it in a form that can be tested"],
                    ["이 결과가 나오면 가설은 기각된다", "검증이 가능한 형태로 쓴다"]),
                  T("Criticise untestable claims.", ["a claim that cannot be disproved cannot be tested", "must that condition be stated first?"],
                    ["반증 가능성이 없는 주장은 검증할 수 없다", "그 조건을 먼저 밝혀야 합니까?"]),
              ])),
            L("결론의 범위를 정해요",
              "A conclusion is bounded in the same sentence that states it: 이 사례에서는 …는 데 그친다. "
              "Generalisation is limited with -까지는 아니다.",
              [V("범위", "beomwi", "scope, range", "noun"),
               V("일반화", "ilbanhwa", "generalisation", "noun"),
               V("한정하다", "hanjeonghada", "to limit, to restrict", "verb"),
               V("사례", "sarye", "case, instance", "noun"),
               V("그치다", "geuchida", "to stop at, to amount to no more than", "verb")],
              G("Bounding a conclusion",
                "이 사례에서는 …는 데 그친다 · 전국으로 일반화하기는 어렵다 · 인과까지는 아니다",
                "-는 데 그친다 says exactly how far the finding runs. 일반화하다 and 인과 are the two "
                "things Korean reviewers test first, and the limit is written with -기는 어렵다 or "
                "-까지는 아니다.",
                [X("이 결론은 이 사례에 적용되는 데 그친다.", "i gyeollon-eun i sarye-e jeogyongdoeneun de geuchinda.", "This conclusion runs no further than this case."),
                 X("전국으로 일반화하기는 어렵다.", "jeonguk-euro ilbanhwahagineun eoryeopda.", "It is hard to generalise it nationwide."),
                 X("상관관계까지는 말할 수 있어도 인과까지는 아니다.", "sanggwangwangye-kkajineun malhal su isseodo ingwa-kkajineun anida.", "A correlation can be stated, but not a cause.")],
                [("이 결론은 전국에 적용됩니다.", "이 결론은 이 사례에 적용되는 데 그친다.", "A bounded conclusion names its scope: 적용되는 데 그친다."),
                 ("인과관계입니다 상관관계입니다.", "상관관계까지는 말할 수 있다.", "The limit is drawn by naming what can be said, not by two competing labels.")]),
              [D("연구자", "이 결론을 전국으로 넓힐 수 있습니까?", "i gyeollon-eul jeonguk-euro neolpil su isseumnikka?", "Can this conclusion be extended nationwide?"),
               D("지도 교수", "어렵습니다. 이 사례에 적용되는 데 그칩니다.", "eoryeopseumnida. i sarye-e jeogyongdoeneun de geuchimnida.", "It is difficult. It runs no further than this case."),
               D("연구자", "그러면 인과관계라고 말해도 됩니까?", "geureomyeon ingwagwangye-rago malhaedo doemnikka?", "Then may I call it a causal relation?"),
               D("지도 교수", "상관관계까지는 말할 수 있어도 인과까지는 아닙니다.", "sanggwangwangye-kkajineun malhal su isseodo ingwa-kkajineun animnida.", "You can state a correlation, but not a cause.")],
              WS("Scope worksheet", [
                  T("Bound the conclusion.", ["this conclusion runs no further than this case", "it is hard to generalise it nationwide"],
                    ["이 결론은 이 사례에 적용되는 데 그친다", "전국으로 일반화하기는 어렵다"]),
                  T("Draw the line.", ["a correlation can be stated, but not a cause", "can this be extended nationwide?"],
                    ["상관관계까지는 말할 수 있다", "전국으로 넓힐 수 있습니까?"]),
              ])),
            L("남은 질문을 제시해요",
              "A good paper ends by handing the question on: 후속 연구의 과제로 남는다. The open question "
              "takes -ㄹ 과제로 남다 and is stated as a question, not a wish.",
              [V("과제", "gwaje", "task, assignment", "noun"),
               V("후속", "husok", "follow-up", "noun"),
               V("열어 두다", "yeoreo duda", "to leave open", "phrase"),
               V("제시하다", "jesihada", "to present", "verb"),
               V("남다", "namda", "to remain", "verb")],
              G("Handing the question on",
                "후속 연구의 과제로 남는다 · 물음을 열어 둔다 · 다음 연구에서 다룰 문제다",
                "What remains takes -ㄹ 과제로 남다, and leaving something open is 열어 두다, a compound "
                "that keeps the door explicitly open. The closing paragraph names the question rather "
                "than answering it.",
                [X("이 물음은 후속 연구의 과제로 남는다.", "i mureum-eun husok yeon-gu-ui gwaje-ro namneunda.", "This question remains a task for follow-up research."),
                 X("결론은 열어 두고 한계를 밝힌다.", "gyeollon-eun yeoreo dugo hangye-reul balkinda.", "We leave the conclusion open and state the limits."),
                 X("다음 연구에서 다룰 문제를 제시한다.", "daeum yeon-gu-eseo darul munje-reul jesihanda.", "We present the problem for the next study.")],
                [("후속 연구가 남습니다.", "후속 연구의 과제로 남는다.", "What remains is the task: 과제로 남다."),
                 ("결론을 열어 둡니다 제시합니다.", "결론은 열어 두고 문제를 제시한다.", "Two actions in sequence take -고.")]),
              [D("연구자", "마지막 문단에 무엇을 씁니까?", "majimak mundan-e mueos-eul sseumnikka?", "What do you write in the last paragraph?"),
               D("지도 교수", "남은 물음을 밝혀야 합니다. 결론을 다 채우지 않습니다.", "nameun mureum-eul balkyeoya hamnida. gyeollon-eul da chaeuji anseumnida.", "You state the open question. You do not fill the conclusion in completely."),
               D("연구자", "그러면 이렇게 쓰겠습니다. 이 물음은 후속 연구의 과제로 남는다.", "geureomyeon ireoke sseugetseumnida. i mureum-eun husok yeon-gu-ui gwaje-ro namneunda.", "Then I will write: this question remains a task for follow-up research."),
               D("지도 교수", "좋습니다. 그것이 결론을 열어 두는 문장입니다.", "jotseumnida. geugeos-i gyeollon-eul yeoreo duneun munjang-imnida.", "Good. That is the sentence that leaves the conclusion open.")],
              WS("Open question worksheet", [
                  T("Hand the question on.", ["this question remains a task for follow-up research", "we leave the conclusion open"],
                    ["이 물음은 후속 연구의 과제로 남는다", "결론은 열어 두고 한계를 밝힌다"]),
                  T("Close the paper.", ["we present the problem for the next study", "you state the open question"],
                    ["다음 연구에서 다룰 문제를 제시한다", "남은 물음을 밝힌다"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Korean academic writing is footnote-heavy. A 국내 논문 carries each source in a "
                 "footnote that names author, year and page, and 참고 문헌 lists everything that "
                 "appeared in them, so a reader can check a claim without leaving the page. 학술지 "
                 "submissions also expect the limits of a study to be stated in the abstract rather "
                 "than buried at the end — a paper that claims more than its sample supports is "
                 "returned for revision, and 반증 가능성, whether the claim could be shown wrong, is "
                 "asked about in the first review round."),
        source_url="https://en.wikipedia.org/wiki/Education_in_South_Korea",
        reading=("이 논문은 두 도시의 사례를 비교한다. 선행 연구는 주로 수도권을 다루었고, 지방 사례는 "
                 "거의 다루지 않았다. 그래서 저자는 두 가지 물음을 남겨 두었다. 첫째, 지방 도시에서도 "
                 "같은 결과가 나오는가. 둘째, 정책의 효과와 인구 변화를 어떻게 구분할 것인가. 이 물음은 "
                 "후속 연구의 과제로 남는다. 논문의 결론은 상관관계까지이며, 인과관계는 주장하지 않는다."),
        reading_gloss=("This paper compares cases from two cities. Previous research mainly dealt with the "
                       "capital region and hardly touched provincial cases. So the author left two "
                       "questions standing. First, does the same result appear in provincial cities? "
                       "Second, how are the effect of the policy and demographic change to be told "
                       "apart? These questions remain tasks for follow-up research. The paper's "
                       "conclusion reaches a correlation and does not claim a causal relation."),
        listening=("지도 교수: 결론이 자료보다 넓게 나갔습니다.<br>"
                   "연구자: 어느 부분입니까?<br>"
                   "지도 교수: 전국으로 일반화한 문장입니다. 이 사례에 적용되는 데 그쳐야 합니다.<br>"
                   "연구자: 그러면 상관관계까지만 말하고, 인과는 후속 연구로 남기겠습니다.<br>"
                   "지도 교수: 그렇게 쓰고, 남은 물음을 마지막 문단에 밝히십시오."),
        listening_gloss=("Supervisor: The conclusion goes wider than the data. Researcher: Which part? "
                         "Supervisor: The sentence that generalises nationwide. It should run no "
                         "further than these cases. Researcher: Then I will state only a correlation "
                         "and leave causation to follow-up research. Supervisor: Write it that way, "
                         "and state the open question in the last paragraph."),
        voice_tag=VOICE,
        idioms=[
            ("선행 연구를 정리하다", "to arrange the previous research", "to write the literature review"),
            ("표본에서 다르다", "to differ in the sample", "the studies differ in their data"),
            ("아직 다루지 않았다", "it has not been covered yet", "the gap in the literature"),
            ("김(2020), 45쪽에서 인용", "quoted from Kim (2020), p. 45", "the footnote form"),
            ("단어만 바꾸면 표절이다", "changing only the words is plagiarism", "synonyms are not paraphrase"),
            ("이 결과가 나오면 가설은 기각된다", "if this result appears the hypothesis is rejected", "stating what would defeat the claim"),
            ("적용되는 데 그친다", "it stops at applying to …", "the scope of the conclusion"),
            ("인과까지는 아니다", "it is not a cause yet", "correlation is not causation"),
            ("열어 두다", "to leave open", "to leave the question standing"),
            ("후속 연구의 과제로 남는다", "it remains a task for follow-up research", "the closing line of a paper"),
        ],
        mistakes=[
            ("초기 연구는 비용을 다룹니다 요약합니다.", "초기 연구는 비용 문제를 다루었다.", "The written register keeps one predicate in the plain past."),
            ("김(2020) 45쪽을 인용.", "김(2020), 45쪽에서 인용.", "A page location takes 에서 before 인용하다."),
            ("이 결론은 전국에 적용됩니다.", "이 결론은 이 사례에 적용되는 데 그친다.", "A conclusion states how far it runs: -는 데 그친다."),
        ],
        task_title="Write an abstract that knows its limits",
        task_instructions=("Write a five-sentence Korean abstract: the gap in the literature, your method, "
                           "one finding bounded with -는 데 그친다, the limit you will not cross with "
                           "-까지는 아니다, and the question you leave open with -ㄹ 과제로 남는다. Then "
                           "write one footnote citing a source with a page."),
    ),
    "test": [
        ("translate_en", "Say: the overall trend can be summarised as three strands.", "전체 흐름은 세 갈래로 요약할 수 있다."),
        ("translate_ko", "이 결론은 이 사례에 적용되는 데 그친다.", "This conclusion runs no further than this case."),
        ("multiple_choice", "Which sentence states a footnote correctly?", "김(2020), 45쪽에서 인용."),
        ("fill_in_the_blank", "이 쟁점은 아직 다루지 ___."  , "않았다"),
        ("word_selection", "Select the Korean for 'it remains a task for follow-up research'.", "후속 연구의 과제로 남는다"),
        ("error_correction", "김(2020)은 일시적입니다라고 밝혔다.", "김(2020)은 일시적이라고 밝혔다."),
        ("dialogue_completion", "Complete: 이 가설이 틀렸다는 것을 어떻게 알 수 있습니까? — ___ (if this result appears the hypothesis is rejected)", "이 결과가 나오면 가설은 기각됩니다"),
        ("matching", "Match 반증 to its meaning.", "disproof, falsification"),
        ("reading_comprehension", "논문의 결론은 어디까지입니까?", "a correlation, not a causal relation"),
        ("inference", "단어만 바꾸면 표절이다. — what does this imply about paraphrasing?", "the sentence structure must change, not only the vocabulary"),
        ("main_idea", "B와 달리 A는 지방 사례를 포함했다. What is this sentence doing?", "contrasting two studies by their samples"),
        ("detail_identification", "후속 연구는 무엇을 추적합니까?", "the same region over ten years"),
    ],
}

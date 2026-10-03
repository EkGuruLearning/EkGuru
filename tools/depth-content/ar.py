# -*- coding: utf-8 -*-
"""Arabic PHASE 1 depth — extras, third lessons, half-step rungs.

Written with the DSL in `tools/depth_kit.py`; rendered by
`tools/author-depth.py --lang ar`.

House style follows the shipped Arabic course: Modern Standard Arabic with
diacritics where they teach something (case endings, verb endings), romanisation
in the `r` field, and a running note that spoken dialects differ from what the
page teaches. Unit ids keep the course's own `A1-U1` shape and the half-step
rungs add the `+` (`A1+-U1`) so a lesson id stays unique across 16 files.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # tools/ on the path
from depth_kit import D, EXTRA, G, L, T, V, WS, X   # noqa: E402

CODE = "ar"
NAME = "Arabic"
NATIVE = "العربية"
PHASE = 1
SCRIPT = "Arabic script"
VOICE = "ar-SA"
SKILL = ("Arabic: right-to-left script, root-and-pattern reading, case and agreement, "
         "formal fuṣḥā versus the spoken register learners actually hear")

# ── the six CEFR rungs get the `extra` block ────────────────────────────────

EXTRAS = {}

EXTRAS["A1"] = EXTRA(
    culture=("Greetings in the Arab world come in pairs and carry religion, warmth and time: "
             "السلام عليكم is answered وعليكم السلام, and a visitor is offered coffee or tea before "
             "business. Refusing the cup is read as refusing the welcome, so a small sip is the "
             "polite minimum. The same page teaches fuṣḥā, the shared written Arabic; on the "
             "street you will also hear a local dialect — both are Arabic, not one right and one wrong."),
    source_url="https://en.wikipedia.org/wiki/Arabic",
    reading=("اسمي منى. أنا من عمّان، وأسكن في القاهرة. صباح الخير! كيف حالك؟ أنا بخير، الحمد لله. "
             "هذا صديقي، اسمه كريم. هو طالب في الجامعة. عندي درس الآن، مع السلامة!"),
    reading_gloss=("My name is Mona. I am from Amman and I live in Cairo. Good morning! How are you? "
                   "I am fine, praise God. This is my friend, his name is Karim. He is a student at "
                   "the university. I have a class now — goodbye!"),
    listening=("أ: صباح الخير! كيف حالك؟<br>ب: بخير، شكراً. وأنت؟<br>أ: بخير، الحمد لله.<br>"
               "ب: هذا كتاب جديد؟<br>أ: نعم، هذا كتاب عربي."),
    listening_gloss=("A: Good morning! How are you? B: Fine, thanks. And you? A: Fine, praise God. "
                     "B: Is this a new book? A: Yes, this is an Arabic book."),
    voice_tag=VOICE,
    idioms=[
        ("السلام عليكم", "peace be upon you", "the standard greeting; answered وعليكم السلام"),
        ("ما شاء الله", "what God has willed", "said to praise something without envy"),
        ("إن شاء الله", "if God wills", "about the future; softens any promise"),
        ("الحمد لله", "praise be to God", "the default answer to كيف حالك"),
        ("أهلاً وسهلاً", "family and ease", "welcome — said to a guest arriving"),
        ("من عيوني", "from my eyes", "with pleasure; a warm yes to a small request"),
        ("على راسي", "on my head", "gladly, at your service"),
        ("تحت أمرك", "under your command", "at your service, especially to a customer"),
        ("لا شكر على واجب", "no thanks for a duty", "you are welcome — it was my duty"),
        ("بالهنا والشفا", "with joy and healing", "said when someone eats or drinks"),
    ],
    mistakes=[
        ("أنا اسمي منى أنا.", "اسمي منى.", "Arabic marks the subject in the verb or pronoun; doubling أنا sounds like a stutter."),
        ("مرحبا عليكم!", "السلام عليكم!", "مرحبا is fine alone, but the paired greeting uses السلام عليكم."),
        ("هذا طالبة.", "هذه طالبة.", "طالبة is feminine, so the demonstrative must be هذه."),
    ],
    task_title="Your first meeting, out loud",
    task_instructions=("Record a 30-second self-introduction in Arabic script first, then read it aloud: "
                       "greeting, name, city, one thing you have (عندي), and a goodbye. Reread the "
                       "culture note and use its pair-answer for the greeting rather than echoing it."),
)

EXTRAS["A2"] = EXTRA(
    culture=("The Arabic past tense is not only 'past': with قد and the perfect form it also reports "
             "news the listener has not heard yet, which is why the same sentence can mean 'he wrote' "
             "and 'he has written'. Learners who translate word-for-word miss that the verb form is "
             "doing the work of an English tense-and-aspect pair, and Arabic instead leans on time "
             "words — أمس، الآن، غداً — to place the action."),
    source_url="https://en.wikipedia.org/wiki/Arabic_verbs",
    reading=("أمس ذهبتُ إلى السوق مع أخي. اشتريتُ خبزاً وفاكهة، ثمّ شربنا القهوة في مقهى صغير. "
             "قال لي: «سأسافر غداً إلى بيروت». سألتُ: «لماذا؟» فأجاب: «لأنّ عملي هناك». "
             "في المساء درسنا معاً، ونحن الآن متعبان قليلاً."),
    reading_gloss=("Yesterday I went to the market with my brother. I bought bread and fruit, then we "
                   "drank coffee in a small café. He told me, 'I will travel tomorrow to Beirut.' I "
                   "asked, 'Why?' and he answered, 'Because my work is there.' In the evening we "
                   "studied together; we are a little tired now."),
    listening=("أ: بكم هذا الكتاب؟<br>ب: عشرون جنيهاً.<br>أ: غالي قليلاً. وهذه الحقيبة؟<br>"
               "ب: خمسة وثلاثون. كل شيء عندنا بخمسة وثلاثين وأربعين.<br>أ: حسناً، آخذ الاثنين."),
    listening_gloss=("A: How much is this book? B: Twenty pounds. A: A little expensive. And this bag? "
                     "B: Thirty-five. Everything we have is thirty-five or forty. A: Fine, I'll take "
                     "both."),
    voice_tag=VOICE,
    idioms=[
        ("على الرحب والسعة", "with welcome and room", "you are very welcome"),
        ("في لمح البصر", "in the blink of an eye", "instantly"),
        ("يداً بيد", "hand with hand", "together, side by side"),
        ("على قدم وساق", "on foot and leg", "in full swing, at full speed"),
        ("قلباً وقالباً", "heart and mould", "wholeheartedly"),
        ("كلمة السر", "the word of the secret", "the watchword; the key to something"),
        ("على أحسن وجه", "in the best manner", "perfectly, impeccably"),
        ("من دون مقدمات", "without introductions", "getting straight to the point"),
        ("على طول الخط", "along the whole line", "all the way, consistently"),
        ("بين عشية وضحاها", "between dusk and its forenoon", "overnight, in a single day"),
    ],
    mistakes=[
        ("أنا ذهبت أمس إلى السوق.", "ذهبتُ أمس إلى السوق.", "The perfect ending -تُ already means 'I'; keeping أنا is not wrong but sounds heavy in a plain past narrative."),
        ("سأذهب أمس.", "ذهبتُ أمس.", "سـ marks the future only; it cannot sit with أمس."),
        ("هذا الكتاب كبير والكتاب هذا كبير أيضاً.", "هذا الكتاب كبير وهذا الكتاب كبير أيضاً.", "Two full noun phrases need a joining و and one demonstrative each; repeating the whole phrase without a connector is a run-on."),
    ],
    task_title="Yesterday and tomorrow, in writing",
    task_instructions=("Write five Arabic sentences: three about yesterday with perfect-tense endings, "
                       "two about tomorrow with سـ or سوف. Then say them aloud without reading, and "
                       "circle any sentence where you used أنا with a past verb — that is the habit "
                       "this lesson breaks."),
)

EXTRAS["B1"] = EXTRA(
    culture=("كان is not simply 'was'. It turns the sentence it opens into a scene: كان الجوّ حاراً "
             "sets the weather as a backdrop, and a following clause reports what happened against it. "
             "Arabic storytelling leans on this 'scene then event' order far more than English does, "
             "which is why a learner who translates clause-by-clause produces correct sentences that "
             "still do not sound like a story."),
    source_url="https://en.wikipedia.org/wiki/Arabic_grammar",
    reading=("كان الوقت متأخراً حين وصلنا إلى المحطة، وكانت السماء تمطر. لم نجد سيارة أجرة، فمشينا "
             "على القدمين حتى الفندق. قال أخي: «لو وصلنا مبكراً، لوجدنا غرفة أفضل». ضحكتُ وقلت: "
             "«المهم أنّنا وصلنا بسلام». في الصباح كانت المدينة هادئة، وقد فتحت المقاهي أبوابها."),
    reading_gloss=("It was late when we reached the station, and the sky was raining. We did not find "
                   "a taxi, so we walked on foot as far as the hotel. My brother said, 'If we had "
                   "arrived early, we would have found a better room.' I laughed and said, 'What "
                   "matters is that we arrived safely.' In the morning the city was quiet, and the "
                   "cafés had opened their doors."),
    listening=("أ: لماذا تأخرت؟<br>ب: لم أستطع، كان الطريق مزدحماً.<br>أ: وهل اتصلت؟<br>"
               "ب: حاولت مرتين، لكنّ الشبكة كانت ضعيفة. أعتذر بصدق."),
    listening_gloss=("A: Why were you late? B: I couldn't — the road was crowded. A: And did you call? "
                     "B: I tried twice, but the network was weak. I sincerely apologise."),
    voice_tag=VOICE,
    idioms=[
        ("الصبر مفتاح الفرج", "patience is the key to relief", "hold on, things will open up"),
        ("من جدّ وجد", "who strives, finds", "effort is what gets results"),
        ("الطيور على أشكالها تقع", "birds alight on their own shapes", "birds of a feather flock together"),
        ("من سار على الدرب وصل", "whoever walks the road arrives", "persistence finishes the journey"),
        ("خير الكلام ما قلّ ودلّ", "the best speech is short and telling", "brevity is eloquence"),
        ("الجار قبل الدار", "the neighbour before the house", "choose your surroundings first"),
        ("يد واحدة لا تصفق", "one hand does not clap", "it takes two to make anything work"),
        ("الوقت كالسيف", "time is like a sword", "use it or it cuts you"),
        ("في التأني السلامة", "in deliberation there is safety", "haste costs more than it saves"),
        ("لكل جواد كبوة", "every horse stumbles", "even the best make a mistake"),
    ],
    mistakes=[
        ("لم أذهب إلى المدرسة أمس.", "لم أذهبْ إلى المدرسة أمس.", "لم is followed by the jussive; أذهب stays written without the final damma, and the written form must show it."),
        ("كان الطلاب مجتهد.", "كان الطلاب مجتهدين.", "The predicate agrees with a plural subject: مجتهدون / مجتهدين."),
        ("إذا ذهبتُ أمس لرأيتُ.", "لو ذهبتُ أمس لرأيتُ.", "إذا is for real future conditions; an unreal or past condition takes لو."),
    ],
    task_title="A storyboard in Arabic",
    task_instructions=("Take one real journey you made. Write six Arabic sentences in the order "
                       "scene-then-event: two with كان setting the scene, two with لم or لن, two with "
                       "a connector (لكنّ، لأنّ، فـ). Then tell it aloud in ninety seconds without "
                       "notes."),
)

EXTRAS["B2"] = EXTRA(
    culture=("Formal written Arabic prefers nominal sentences for definitions and verbal sentences for "
             "events, and it signals the difference with particles rather than word order alone. إنّ "
             "opens a statement of fact with emphasis — إنّ الاتفاق عادل says 'the agreement IS just' "
             "— while أنّ packs the same clause into a noun ('that the agreement is just'). Getting "
             "these two right is what separates a learner's report from a document a ministry will "
             "read."),
    source_url="https://en.wikipedia.org/wiki/Arabic_grammar",
    reading=("إنّ ارتفاع أسعار الطاقة أثّر على الاقتصاد خلال العام الماضي، ولا سيّما في القطاع "
             "الصناعي. وقد أشار التقرير إلى أنّ الحلول قصيرة الأمد لا تكفي، بينما يرى خبراء آخرون "
             "أنّ الاستثمار في الطاقة المتجددة هو الطريق الأضمن. في المقابل، يبقى السؤال الأهم: من "
             "يتحمّل كلفة التحوّل؟"),
    reading_gloss=("The rise in energy prices affected the economy over the past year, especially in "
                   "the industrial sector. The report noted that short-term solutions are not enough, "
                   "while other experts believe that investment in renewable energy is the surest "
                   "path. On the other hand, the most important question remains: who bears the cost "
                   "of the transition?"),
    listening=("أ: قبل أن نبدأ، ما البند الأول في جدول الأعمال؟<br>ب: الميزانية. لكنّ الفريق المالي "
               "لم ينتهِ من الأرقام.<br>أ: إذاً نؤجلها ونبدأ بالجدول الزمني.<br>ب: موافق، وسأرسل "
               "محضر الجلسة هذا المساء."),
    listening_gloss=("A: Before we begin, what is the first item on the agenda? B: The budget. But the "
                     "finance team has not finished the figures. A: Then let's postpone it and start "
                     "with the timeline. B: Agreed — I'll send the minutes this evening."),
    voice_tag=VOICE,
    idioms=[
        ("لا سيّما", "especially not", "above all, in particular"),
        ("بمثابة", "in the position of", "amounts to; serves as"),
        ("خلافاً لما", "contrary to what", "contrary to the claim that"),
        ("في ضوء ما تقدم", "in the light of what precedes", "in view of the above"),
        ("على حدّ سواء", "at one and the same limit", "equally, alike"),
        ("في نهاية المطاف", "at the end of the path", "ultimately"),
        ("إذا جاز التعبير", "if the expression is allowed", "so to speak"),
        ("من ناحية أخرى", "from another side", "on the other hand"),
        ("بالاستناد إلى", "resting on", "on the basis of"),
        ("بصورة لا لبس فيها", "in a manner with no confusion", "unambiguously"),
    ],
    mistakes=[
        ("أعتقد أنّ الاتفاق عادل.", "أعتقد أنّ الاتفاق عادلٌ.", "After أنّ the predicate of the clause is nominative: عادلٌ, not the pause form."),
        ("إنّ المشروع ناجح؟", "هل المشروع ناجح؟", "إنّ asserts; it cannot do the work of a question, which needs هل or a question word."),
        ("ذهب المدير إلى المؤتمر ووقّع الاتفاق واجتمع مع الشركاء.", "ذهب المدير إلى المؤتمر، ووقّع الاتفاق، واجتمع مع الشركاء.", "In formal prose a long chain of verbs needs commas; running three perfect verbs together without punctuation reads like a draft note."),
    ],
    task_title="Rewrite a decision in formal Arabic",
    task_instructions=("Take a real decision from your work (a price change, a deadline, a meeting "
                       "outcome). Write it three times: one line with إنّ as an assertion, one with "
                       "أنّ inside a reporting sentence (أشار التقرير إلى أنّ...), and one with a "
                       "concession (صحيح أنّ... إلا أنّ...). Keep to twenty-five words each."),
)

EXTRAS["C1"] = EXTRA(
    culture=("Diglossia is the fact that a Cairo engineer writes fuṣḥā and chats in عامية, and the "
             "same speaker moves between them in one afternoon. The formal register carries authority "
             "and distance; the colloquial carries warmth and belonging. A C1 speaker is not someone "
             "who speaks one perfectly, but someone who hears which room they are in — and who notices "
             "when a text's register slips."),
    source_url="https://en.wikipedia.org/wiki/Diglossia",
    reading=("تجدر الإشارة إلى أنّ مسألة الترجمة تتجاوز نقل المفردات إلى نقل المقام: فالكلمة الواحدة "
             "قد تكون مهذّبة في سياق ومستهجنة في سياق آخر. ومن هذا المنطلق، يرى بعض المترجمين أنّ "
             "الأمانة الحرفية قد تخون النصّ، وأنّ الترجمة الجيدة هي التي تحفظ أثره في القارئ لا "
             "شكله في الصفحة. وبالمقابل، يحذّر نقّادٌ من أنّ هذه المرونة قد تتحول إلى تصرف مفرط."),
    reading_gloss=("It is worth noting that translation goes beyond carrying over vocabulary to "
                   "carrying over the situation: one word may be courteous in one context and "
                   "offensive in another. From this standpoint, some translators hold that literal "
                   "fidelity can betray the text, and that good translation preserves its effect on "
                   "the reader rather than its shape on the page. Conversely, critics warn that this "
                   "flexibility can turn into excessive licence."),
    listening=("أ: هل نستخدم النصّ الفصيح في الإعلان أم نصاً أقرب إلى الناس؟<br>ب: في الإعلانات، "
               "العامية تبيع والعربية الفصحى تبني ثقة.<br>أ: إذاً نصّان: واحد للثقة وواحد للبيع.<br>"
               "ب: هذا ما فعلته العلامات الكبرى فعلاً."),
    listening_gloss=("A: Do we use formal Arabic in the advertisement or something closer to people? "
                     "B: In advertising, colloquial sells and fuṣḥā builds trust. A: Then two texts: "
                     "one for trust, one for selling. B: That is exactly what the big brands do."),
    voice_tag=VOICE,
    idioms=[
        ("كما ذكرنا آنفاً", "as we mentioned just before", "as stated above"),
        ("بادىء ذي بدء", "beginning of the beginning", "to begin with"),
        ("من هذا المنطلق", "from this point of departure", "from this standpoint"),
        ("في سياق متصل", "in a connected context", "in related news"),
        ("تجدر الإشارة إلى", "it is worthwhile to point out", "it is worth noting that"),
        ("في المقابل", "on the opposite side", "in contrast, on the other hand"),
        ("مع ذلك", "with that", "nevertheless"),
        ("على مستوى آخر", "at another level", "at a different level altogether"),
        ("من باب أولى", "from the gate of being more deserving", "a fortiori"),
        ("بالمحصّلة", "in the final tally", "all things considered"),
    ],
    mistakes=[
        ("صحيح أنّ الفكرة جميلة، لكن هي مكلفة.", "صحيح أنّ الفكرة جميلة، إلا أنّها مكلفة.", "The concession pair in formal Arabic is صحيح أنّ... إلا أنّ...; a bare لكن with a pronoun subject drops the register."),
        ("قام المدير بتوضيح الأمور.", "وضّح المدير الأمور.", "The verbal noun construction (قام بـ) is bureaucratic padding; strong prose uses the verb."),
        ("أنا موافق على الشروط، وبتوقيعي أوافق.", "أوافق على الشروط، وبتوقيعي ألتزم بها.", "Repeating أوافق in one sentence and mixing موافق with a verb is loose register; keep one stance and vary the verb."),
    ],
    task_title="Two registers, one message",
    task_instructions=("Choose one work message (a delay, a refusal, a correction). Write it twice in "
                       "Arabic: once for a WhatsApp group in the spoken register, once for an official "
                       "letter in fuṣḥā with a طلب or إشعار. Then mark every place the register "
                       "changed and say why out loud."),
)

EXTRAS["C2"] = EXTRA(
    culture=("Arabic rhetoric names its own figures: جناس (paronomasia, a play on two similar roots), "
             "طباق (antithesis, pairing opposites), and سجع (rhymed prose that closes a line with a "
             "matching cadence). A C2 reader hears them in a political speech and in a news headline "
             "alike. They are not decoration: a speaker who sets up طباق has already framed the "
             "argument as a choice between two named things, and the audience is expected to feel it."),
    source_url="https://en.wikipedia.org/wiki/Arabic_poetry",
    reading=("عاد وفد المفاوضات بخفي حنين، فقد دخل إلى القاعة بوعودٍ عريضة وخرج بشروطٍ أعرج. يرى "
             "أنصار الاتفاق أنّ الخروج بأيّ اتفاق أفضل من حربٍ لا يعرف أحدٌ آخر فصولها، بينما يرى "
             "خصومه أنّ الذي يُنصف نصف ميزانٍ يظنّ نفسه عادلاً. وبين المطرقة والسندان، يقف المواطن "
             "الذي لا يصوّت على الحرب ولا على الصلح، بل يدفع الثمن وحده."),
    reading_gloss=("The negotiating delegation returned empty-handed: it entered the hall with broad "
                   "promises and left with lame terms. Supporters of the agreement believe that coming "
                   "out with any deal is better than a war whose last chapters no one knows, while its "
                   "opponents believe that one who does justice by half a scale imagines himself just. "
                   "Between the hammer and the anvil stands the citizen, who votes on neither war nor "
                   "reconciliation, but pays the price alone."),
    listening=("أ: كيف تقرأ النتائج؟ <br>ب: التقرير صحيحٌ في أرقامه، مضلِّلٌ في ترتيبها.<br>"
               "أ: أيّ ترتيب؟<br>ب: قدّم الفصل العاطفي على الجدول الزمني، فصار القارئ يرى الرمز لا "
               "السبب."),
    listening_gloss=("A: How do you read the findings? B: The report is correct in its numbers, "
                     "misleading in their ordering. A: Which ordering? B: It put the emotional chapter "
                     "before the timeline, so the reader sees the symbol and not the cause."),
    voice_tag=VOICE,
    idioms=[
        ("بخفي حنين", "with Hunayn's two sandals", "empty-handed after high expectations"),
        ("بين المطرقة والسندان", "between the hammer and the anvil", "caught with no good option"),
        ("القشة التي قصمت ظهر البعير", "the straw that broke the camel's back", "the small last burden"),
        ("صبّ الزيت على النار", "poured oil on the fire", "made a conflict worse"),
        ("وضع العصا في العجلة", "put a stick in the wheel", "deliberately obstructed"),
        ("ضرب أخماساً بأسداس", "multiplied fives into sixes", "floundered in confusion"),
        ("سبق السيف العذل", "the sword outran the blame", "too late for reproach"),
        ("لا يُلدغ المؤمن من جحر مرتين", "the believer is not stung from one hole twice", "once learned, never again"),
        ("جاء بقضّه وقضيضه", "came with his breaking and his crashing", "arrived with everything he had"),
        ("في نهاية المطاف", "at the end of the path", "ultimately, when all is done"),
    ],
    mistakes=[
        ("الفكرة أعمق وأدقّ.", "الفكرة أعمقُ وأدقُّ.", "Comparative adjectives carry the case their position demands; dropping both endings flattens formal prose."),
        ("هذا يثبت أنّ التقرير كاذب.", "هذا يرجّح أنّ التقرير مضلِّل.", "يثبت claims certainty; a single order of presentation supports a suspicion, not a proof."),
        ("الحرب والسلام قضية واحدة.", "الحرب والسلام وجهان لقضية واحدة.", "طباق pairs two named opposites; without a frame (وجهان لـ) the line is a list, not a figure."),
    ],
    task_title="Name the figure, then write it",
    task_instructions=("Take a headline you have seen this week in Arabic. Identify its figure (طباق، "
                       "جناس، سجع، كناية) in one sentence, then rewrite the headline three ways: with "
                       "the figure removed, with it doubled, and with it turned against its own "
                       "argument. Then read all four aloud and keep the one you would actually print."),
)

# ── a third lesson in every unit of the six CEFR rungs ──────────────────────
# (unit id, lesson id, spec) — the renderer appends or replaces by lesson id.

THIRD = {}

THIRD["A1"] = [
    ("A1-U1", "A1-U1-L3", L(
        "Thank you, please, sorry: the polite three",
        "Three words carry almost every small exchange: شكراً (thank you), عفواً (you're welcome — and "
        "also 'excuse me'), and من فضلك (please). They change with the person you speak to: من فضلكِ "
        "and تفضّلي to a woman, آسفة if you are the woman apologising.",
        [V("شكراً", "shukran", "thank you", "interjection"),
         V("عفواً", "ʿafwan", "you're welcome; excuse me", "interjection"),
         V("من فضلك", "min faḍlik", "please (to a man)", "phrase"),
         V("آسف", "āsif", "sorry (said by a man)", "adjective"),
         V("تفضّل", "tafaḍḍal", "go ahead; here you are", "verb")],
        G("Politeness follows gender",
          "min faḍlik → min faḍlik(i) · āsif → āsifa · tafaḍḍal → tafaḍḍalī",
          "Arabic marks the person you are addressing, not your own politeness. To a man: من فضلك، "
          "تفضّل. To a woman: من فضلكِ، تفضّلي. If you are a woman apologising, you say آسفة.",
          [X("شكراً جزيلاً!", "shukran jazīlan!", "Thank you very much!"),
           X("من فضلكِ، أين المحطة؟", "min faḍlik, ayna al-maḥaṭṭa?", "Please, where is the station?"),
           X("آسفة، أنا متأخرة.", "āsifa, anā mutaʾakhkhira.", "Sorry, I am late. (woman speaking)")],
          [("شكراً يا سيدتي!", "شكراً يا سيّدتي!", "The word شكراً ends in an alif; it takes no extra ending for the person addressed."),
           ("من فضلكي، أين المحطة؟", "من فضلكِ، أين المحطة؟", "The feminine ending is a kasra, not a ي: فضلكِ.")]),
        [D("سامي", "تفضّل، هذا كتابك.", "tafaḍḍal, hādhā kitābuka.", "Here you are, this is your book."),
         D("هند", "شكراً جزيلاً!", "shukran jazīlan!", "Thank you very much!"),
         D("سامي", "عفواً، هذا واجبي.", "ʿafwan, hādhā wājibī.", "You're welcome, it's my duty."),
         D("هند", "آسفة، أنا متأخرة اليوم.", "āsifa, anā mutaʾakhkhira al-yawm.", "Sorry, I am late today.")],
        WS("Polite three worksheet", [
            T("Translate to Arabic.", ["thank you", "please (to a woman)", "sorry (woman speaking)", "you're welcome"],
              ["شكراً", "من فضلكِ", "آسفة", "عفواً"]),
            T("Choose the right form for the person in brackets.",
              ["من فضلك (to Layla)", "تفضّل (to Nūr)", "آسف (Zayd speaking)"],
              ["من فضلكِ", "تفضّلي", "آسف"]),
        ]))),
    ("A1-U2", "A1-U2-L3", L(
        "Counting to five: one, two, three, كم؟",
        "كم (how many) turns numbers into questions: كم كتاباً عندك؟ A number from three to ten takes a "
        "plural noun — ثلاثة كتب — but one and two sit directly on the noun, and two even changes its shape.",
        [V("واحد", "wāḥid", "one", "numeral"),
         V("اثنان", "ithnān", "two", "numeral"),
         V("ثلاثة", "thalātha", "three", "numeral"),
         V("خمسة", "khamsa", "five", "numeral"),
         V("كم", "kam", "how many", "interrogative")],
        G("Numbers and the noun",
          "three to ten + plural · one/two + singular (two uses the dual)",
          "ثلاثة كتب، خمسة طلاب. One and two behave differently: كتاب واحد، كتابان (dual). After كم the "
          "counted noun is singular accusative in careful Arabic: كم كتاباً عندك؟",
          [X("عندي كتابان.", "ʿindī kitābān.", "I have two books."),
           X("كم طالباً في الصفّ؟", "kam ṭāliban fī al-ṣaff?", "How many students are in the class?"),
           X("في الحقيبة خمسة كتب.", "fī al-ḥaqība khamsa kutub.", "In the bag there are five books.")],
          [("عندي اثنان كتب.", "عندي كتابان.", "Two is expressed by the dual form of the noun, not by اثنان + plural."),
           ("خمسة كتاب.", "خمسة كتب.", "Numbers three to ten take a plural noun.")]),
        [D("ليلى", "كم كتاباً عندك؟", "kam kitāban ʿindak?", "How many books do you have?"),
         D("كريم", "عندي ثلاثة كتب، وهذا رابع.", "ʿindī thalātha kutub, wa-hādhā rābiʿ.", "I have three books, and this is a fourth."),
         D("ليلى", "وكم أخاً عندك؟", "wa-kam akhan ʿindak?", "And how many brothers do you have?"),
         D("كريم", "عندي أخ واحد وأختان.", "ʿindī akh wāḥid wa-ukhtān.", "I have one brother and two sisters.")],
        WS("Counting worksheet", [
            T("Write the number in Arabic words.", ["2 books", "3 students", "5 pens"],
              ["كتابان", "ثلاثة طلاب", "خمسة أقلام"]),
            T("Answer with a full sentence.", ["كم يوماً في الأسبوع؟", "كم كتاباً في الحقيبة؟ (3)"],
              ["سبعة أيام", "في الحقيبة ثلاثة كتب"]),
        ]))),
    ("A1-U3", "A1-U3-L3", L(
        "Asking: ما، من، أين، هل",
        "Four question makers cover most of A1: ما (what), من (who), أين (where) and هل for any yes/no "
        "question. They stand at the front, and the rest of the sentence does not move.",
        [V("ما", "mā", "what", "interrogative"),
         V("من", "man", "who", "interrogative"),
         V("أين", "ayna", "where", "interrogative"),
         V("هل", "hal", "question particle (yes/no)", "particle"),
         V("لماذا", "limādhā", "why", "interrogative")],
        G("Questions keep the sentence order",
          "question word + subject + verb · hal + statement",
          "Arabic does not reorder for questions. ما اسمك؟ is literally 'what your-name?'. هل turns a "
          "statement into a yes/no question with no other change: أنت طالب → هل أنت طالب؟",
          [X("ما اسمك؟", "mā ismuka?", "What is your name?"),
           X("من هذا الرجل؟", "man hādhā al-rajul?", "Who is this man?"),
           X("هل تسكن في القاهرة؟", "hal taskunu fī al-qāhira?", "Do you live in Cairo?")],
          [("هل ما اسمك؟", "ما اسمك؟", "ما is already a question; هل is only for yes/no questions."),
           ("أنت من أين؟", "من أين أنت؟", "The question word stays at the front: من أين أنت؟")]),
        [D("نور", "ما اسمك؟", "mā ismuk?", "What is your name?"),
         D("زياد", "اسمي زياد. وأنتِ؟", "ismī Ziyād. wa-antī?", "My name is Ziyad. And you?"),
         D("نور", "أنا نور. من أين أنت؟", "anā Nūr. min ayna anta?", "I am Nur. Where are you from?"),
         D("زياد", "أنا من تونس، وهل تسكنين هنا؟", "anā min Tūnis, wa-hal taskunīn hunā?", "I am from Tunis — and do you live here?")],
        WS("Question worksheet", [
            T("Make a question for the answer.", ["…؟ اسمي هند.", "…؟ أنا من دلهي.", "…؟ نعم، أنا طالب."],
              ["ما اسمك؟", "من أين أنت؟", "هل أنت طالب؟"]),
            T("Translate to Arabic.", ["Who is she?", "Where is the book?", "Why are you late?"],
              ["من هي؟", "أين الكتاب؟", "لماذا أنت متأخر؟"]),
        ]))),
]

THIRD["A2"] = [
    ("A2-U1", "A2-U1-L3", L(
        "Pinning time: أمس، الآن، غداً",
        "Arabic often lets the time word carry what English does with tense: أمس with a perfect verb, "
        "غداً with سـ, الآن with the present. Put the time word first and it frames everything after it.",
        [V("أمس", "ams", "yesterday", "adverb"),
         V("غداً", "ghadan", "tomorrow", "adverb"),
         V("الآن", "al-ān", "now", "adverb"),
         V("دائماً", "dāʾiman", "always", "adverb"),
         V("بعد قليل", "baʿda qalīl", "in a little while", "phrase")],
        G("Time word + tense",
          "time word first + verb in the matching form",
          "غداً سأدرس (tomorrow I will study). أمس درستُ (yesterday I studied). الآن أدرس (now I am "
          "studying). The time word does not change the verb — but it must agree with it.",
          [X("غداً سأسافر إلى دبي.", "ghadan sa-usāfir ilā Dubayy.", "Tomorrow I will travel to Dubai."),
           X("الآن ندرس العربية.", "al-ān nadrus al-ʿarabiyya.", "Now we are studying Arabic."),
           X("دائماً نشرب القهوة صباحاً.", "dāʾiman nashrab al-qahwa ṣabāḥan.", "We always drink coffee in the morning.")],
          [("غداً درستُ الدرس.", "غداً سأدرس الدرس.", "غداً cannot sit with a past verb."),
           ("دائماً أشرب القهوة أمس.", "أمس شربتُ القهوة.", "A frequency word and a one-time past word contradict each other.")]),
        [D("هدى", "ماذا فعلتِ أمس؟", "mādhā faʿalti ams?", "What did you do yesterday?"),
         D("منى", "درستُ ثمّ شربتُ القهوة مع صديقتي.", "darastu thumma sharibtu al-qahwa maʿa ṣadīqatī.", "I studied, then drank coffee with my friend."),
         D("هدى", "وماذا ستفعلين غداً؟", "wa-mādhā sa-tafʿalīn ghadan?", "And what will you do tomorrow?"),
         D("منى", "غداً سأزور جدّتي، وبعد قليل أتصل بها.", "ghadan sa-azūr jaddatī, wa-baʿda qalīl attaṣil bihā.", "Tomorrow I will visit my grandmother, and in a little while I'll call her.")],
        WS("Time worksheet", [
            T("Put the tense the time word needs.", ["غداً (درس)", "أمس (كتب)", "الآن (يقرأ)", "دائماً (يشرب)"],
              ["سأدرس", "كتبتُ", "يقرأ", "يشرب"]),
            T("Answer about your own day.", ["ماذا فعلتَ أمس؟", "ماذا ستفعل غداً؟"],
              ["(a past sentence with a perfect verb)", "(a future sentence with سـ or سوف)"]),
        ]))),
    ("A2-U2", "A2-U2-L3", L(
        "My neighbourhood: في الحيّ",
        "Places live inside في، على، قريب من and بعيد عن. Tell someone where you live and what is "
        "around you, and you can hold a whole conversation on a street corner.",
        [V("حيّ", "ḥayy", "neighbourhood", "noun"),
         V("مسجد", "masjid", "mosque", "noun"),
         V("سوق", "sūq", "market", "noun"),
         V("حديقة", "ḥadīqa", "park; garden", "noun"),
         V("قريب من", "qarīb min", "close to", "phrase"),
         V("بعيد عن", "baʿīd ʿan", "far from", "phrase")],
        G("Places and their prepositions",
          "fī + place · qarīb min + place · baʿīd ʿan + place",
          "قريب and بعيد are adjectives, so they agree: الحديقة قريبة من بيتي. When they take من/عن they "
          "become a fixed frame: قريب من السوق، بعيد عن المركز.",
          [X("أسكن في حيّ صغير.", "askun fī ḥayy ṣaghīr.", "I live in a small neighbourhood."),
           X("المسجد قريب من بيتنا.", "al-masjid qarīb min baytinā.", "The mosque is close to our house."),
           X("السوق بعيد عن الجامعة قليلاً.", "al-sūq baʿīd ʿan al-jāmiʿa qalīlan.", "The market is a little far from the university.")],
          [("الحديقة قريب من البيت.", "الحديقة قريبة من البيت.", "قريب agrees with الحديقة: قريبة."),
           ("أسكن على القاهرة.", "أسكن في القاهرة.", "Cities take في; على is 'on' a surface.")]),
        [D("عمر", "أين تسكن؟", "ayna taskun?", "Where do you live?"),
         D("سلمى", "أسكن في حيّ هادئ قريب من الحديقة.", "askun fī ḥayy hādiʾ qarīb min al-ḥadīqa.", "I live in a quiet neighbourhood close to the park."),
         D("عمر", "وهل السوق قريب؟", "wa-hal al-sūq qarīb?", "And is the market close?"),
         D("سلمى", "نعم، دقيقتان على القدمين، والمسجد أبعد قليلاً.", "naʿam, daqīqatān ʿalā al-qadamayn, wa-l-masjid abʿad qalīlan.", "Yes, two minutes on foot; the mosque is a bit further.")],
        WS("Neighbourhood worksheet", [
            T("Complete with في، من، عن.", ["أسكن ___ حيّ قديم.", "الجامعة قريبة ___ السوق.", "الفندق بعيد ___ المطار."],
              ["في", "من", "عن"]),
            T("Describe your own street in two sentences.", ["(where you live)", "(what is near)"],
              ["أسكن في…", "…قريب من…"]),
        ]))),
    ("A2-U3", "A2-U3-L3", L(
        "At the restaurant: order, then ask for the bill",
        "Three moves carry a whole meal: أريد… من فضلك (I want… please), هل عندكم…؟ (do you have…?) and "
        "الحساب من فضلك (the bill, please). Add لذيذ and you can talk about it afterwards too.",
        [V("أريد", "urīd", "I want", "verb"),
         V("قائمة الطعام", "qāʾimat al-ṭaʿām", "the menu", "noun"),
         V("الحساب", "al-ḥisāb", "the bill", "noun"),
         V("لذيذ", "ladhīdh", "delicious", "adjective"),
         V("ماء", "māʾ", "water", "noun")],
        G("Ordering frames",
          "urīd + noun (+ min faḍlik) · hal ʿindakum + noun?",
          "أريد دجاجاً من فضلك. Do you want it with something? بـ: أريد دجاجاً بالأرز. To ask what "
          "exists, use هل عندكم…؟",
          [X("أريد شوربة من فضلك.", "urīd shūrba min faḍlik.", "I want soup, please."),
           X("هل عندكم قهوة بدون سكر؟", "hal ʿindakum qahwa bidūn sukkar?", "Do you have coffee without sugar?"),
           X("الحساب من فضلك.", "al-ḥisāb min faḍlik.", "The bill, please.")],
          [("أريد الحساب شكراً.", "الحساب من فضلك.", "Asking for the bill uses من فضلك, not شكراً."),
           ("الطعام لذيذة.", "الطعام لذيذ.", "الطعام is masculine: لذيذ.")]),
        [D("النادل", "مساء الخير، ماذا تريدون؟", "masāʾ al-khayr, mādhā turīdūn?", "Good evening, what would you like?"),
         D("سمير", "أريد دجاجاً بالأرز، وقهوة من فضلك.", "urīd dajājan bi-l-aruzz, wa-qahwa min faḍlik.", "I want chicken with rice, and a coffee please."),
         D("النادل", "هل تريد سلطة أيضاً؟", "hal turīd salaṭa aydan?", "Would you like a salad too?"),
         D("سمير", "لا، شكراً. الطعام لذيذ، والحساب من فضلك.", "lā, shukran. al-ṭaʿām ladhīdh, wa-l-ḥisāb min faḍlik.", "No thanks. The food is delicious — and the bill, please.")],
        WS("Restaurant worksheet", [
            T("Order it in Arabic with من فضلك.", ["fish with rice", "water without ice", "the bill"],
              ["سمكاً بالأرز من فضلك", "ماء بدون ثلج من فضلك", "الحساب من فضلك"]),
            T("Reply as the waiter.", ["هل عندكم…؟ (yes, we have)", "شكراً! (you're welcome)"],
              ["نعم، عندنا", "عفواً"]),
        ]))),
]

THIRD["B1"] = [
    ("B1-U1", "B1-U1-L3", L(
        "The dual in real life: pairs",
        "Arabic has a third number. Two of anything takes one ending: -ان when it is the subject, "
        "-ين when anything acts on it. Pronouns follow: هما for 'they two' and both verbs agree.",
        [V("كتابان", "kitābān", "two books", "noun"),
         V("والدان", "wālidān", "two parents", "noun"),
         V("ساعتان", "sāʿatān", "two hours (o'clock)", "noun"),
         V("هما", "humā", "they two", "pronoun"),
         V("صديقان", "ṣadīqān", "two friends", "noun")],
        G("Dual endings",
          "-ān (nominative) · -ayn (accusative and genitive)",
          "جاء الطالبان (both students came). رأيتُ الطالبَين (I saw both students). The dual also eats "
          "the plural: أخوان, not ثلاثة أخوين when there are exactly two.",
          [X("هما طالبان مجتهدان.", "humā ṭālibān mujtahidān.", "They are two diligent students."),
           X("انتظرتُ ساعتين.", "intaẓartu sāʿatayn.", "I waited two hours."),
           X("الوالدان في البيت.", "al-wālidān fī al-bayt.", "The parents are at home.")],
          [("عندي أخوان اثنان.", "عندي أخوان.", "The dual already means two; اثنان is redundant."),
           ("رأيتُ الطالبان.", "رأيتُ الطالبَين.", "After a verb, the dual takes -ين.")]),
        [D("ريم", "أين أخواك؟", "ayna akhawāk?", "Where are your two brothers?"),
         D("فهد", "هما في المكتبة، يدرسان معاً.", "humā fī al-maktaba, yadrusān maʿan.", "They are in the library, studying together."),
         D("ريم", "وانتظرتهما طويلاً؟", "wa-intaẓartahumā ṭawīlan?", "And did you wait for them long?"),
         D("فهد", "انتظرتُ ساعتين ثمّ ذهبتُ.", "intaẓartu sāʿatayn thumma dhahabtu.", "I waited two hours and then left.")],
        WS("Dual worksheet", [
            T("Write the dual in the right case.", ["1 subject: طالب →", "after رأيتُ: كتاب →", "1 subject: ساعة →"],
              ["طالبان", "كتابين", "ساعتان"]),
            T("Answer with a dual.", ["أين والداك؟", "كم ساعة درستَ؟"],
              ["هما في…", "درستُ ساعتين"]),
        ]))),
    ("B1-U2", "B1-U2-L3", L(
        "Requests that stay polite, prohibitions that are not rude",
        "The imperative alone can sound like an order. Arabic softens it with لو سمحت or من فضلك, and "
        "forbids with لا + the jussive — a form that says 'don't', not 'you must not'.",
        [V("لو سمحت", "law samaḥt", "if you would be so kind", "phrase"),
         V("تكرّم", "takram", "please do (kindly)", "verb"),
         V("لا تنسَ", "lā tansa", "don't forget", "verb"),
         V("يمكن", "yumkin", "it is possible; may", "verb"),
         V("بكل سرور", "bi-kull surūr", "with great pleasure", "phrase")],
        G("Softening the imperative",
          "imperative + min faḍlik / law samaḥt · lā + jussive",
          "أرسل لي الملف، لو سمحت. To forbid, Arabic says لا ترسل (don't send) — lighter than a rule. "
          "لا تنسَ أنّ الموعد غداً: don't forget that the appointment is tomorrow.",
          [X("أعطني الرقم، لو سمحت.", "aʿṭinī al-raqm, law samaḥt.", "Give me the number, if you would."),
           X("لا تتأخر غداً.", "lā tataʾakhkhar ghadan.", "Don't be late tomorrow."),
           X("يمكن أن نلتقي بعد العمل، بكل سرور.", "yumkin an naltqī baʿda al-ʿamal, bi-kull surūr.", "We can meet after work, with pleasure.")],
          [("لا تتأخرُ غداً.", "لا تتأخرْ غداً.", "After لا the verb is jussive: no final damma."),
           ("أعطني الرقم شكراً.", "أعطني الرقم، لو سمحت.", "شكراً thanks; it does not soften a request.")]),
        [D("منال", "أرسل لي التقرير اليوم، لو سمحت.", "arsil lī al-taqrīr al-yawm, law samaḥt.", "Send me the report today, if you would."),
         D("يوسف", "بكل سرور. هل يمكن أن أرسله مساءً؟", "bi-kull surūr. hal yumkin an ursilah masāʾan?", "With pleasure. May I send it in the evening?"),
         D("منال", "نعم، لكن لا تنسَ الاجتماع صباحاً.", "naʿam, lākin lā tansa al-ijtimāʿ ṣabāḥan.", "Yes — but don't forget the morning meeting."),
         D("يوسف", "لن أنسى، سأرسل الملف قبل الثامنة.", "lan ansā, sa-ursil al-milaff qabla al-thāmina.", "I won't forget; I'll send the file before eight.")],
        WS("Request worksheet", [
            T("Soften the imperative.", ["أرسل الملف. → (with لو سمحت)", "اتصل بي. → (with من فضلك)"],
              ["أرسل الملف، لو سمحت.", "اتصل بي، من فضلك."]),
            T("Make it a prohibition.", ["تنسى الموعد →", "تتأخر →", "ترسل الآن →"],
              ["لا تنسَ الموعد", "لا تتأخر", "لا ترسل الآن"]),
        ]))),
    ("B1-U3", "B1-U3-L3", L(
        "I partly agree: degrees of agreement",
        "Disagreement in Arabic usually starts with the part that is right. أوافق على… لكنّ… or صحيح "
        "أنّ… إلا أنّ… lets you disagree without turning the room against you.",
        [V("أوافق", "uwāfiq", "I agree", "verb"),
         V("أختلف", "akhtalif", "I differ", "verb"),
         V("جزئياً", "juzʾiyyan", "partly", "adverb"),
         V("نقطة مهمة", "nuqṭa muhimma", "an important point", "phrase"),
         V("من جهتي", "min jihatī", "on my side; as for me", "phrase")],
        G("Agree first, then limit",
          "uwāfiq ʿalā X, lākin… · ṣaḥīḥ anna…, illā anna…",
          "أوافق على الفكرة، لكنّ التنفيذ صعب. صحيح أنّ الوقت ضيّق، إلا أنّ النتيجة تستحق. من جهتي أرى الأمر مختلفاً.",
          [X("أوافق جزئياً على ما قلتَه.", "uwāfiq juzʾiyyan ʿalā mā qultah.", "I partly agree with what you said."),
           X("صحيح أنّ السعر مرتفع، إلا أنّ الجودة أفضل.", "ṣaḥīḥ anna al-siʿr murtafiʿ, illā anna al-jawda afḍal.", "True, the price is high, but the quality is better."),
           X("من جهتي، المشكلة في التوقيت لا في الخطة.", "min jihatī, al-mushkila fī al-tawqīt lā fī al-khuṭṭa.", "As for me, the problem is the timing, not the plan.")],
          [("أوافق لكنّ لا.", "أوافق جزئياً، لكنّ هناك ملاحظة.", "Bare أوافق + لا cancels itself; name the degree instead."),
           ("من جهة لي…", "من جهتي…", "The possessive is attached: جهتي.")]),
        [D("ناصر", "أرى أنّ الخطة جاهزة للتنفيذ.", "arā anna al-khuṭṭa jāhiza li-l-tanfīdh.", "I think the plan is ready to execute."),
         D("سارة", "أوافق على الهدف، لكنّ الجدول الزمني ضيّق.", "uwāfiq ʿalā al-hadaf, lākinna al-jadwal al-zamanī ḍayyiq.", "I agree with the goal, but the timeline is tight."),
         D("ناصر", "صحيح أنّ الوقت ضيّق، إلا أنّ الفرصة الآن.", "ṣaḥīḥ anna al-waqt ḍayyiq, illā anna al-furṣa al-ān.", "True, time is tight, but the opportunity is now."),
         D("سارة", "من جهتي، أقترح أسبوعين إضافيين.", "min jihatī, aqtariḥ usbūʿayn iḍāfiyyayn.", "For my part, I suggest two extra weeks.")],
        WS("Agreement worksheet", [
            T("Build a partial agreement.", ["الهدف جيد / التكلفة مرتفعة", "الفكرة صحيحة / التنفيذ صعب"],
              ["أوافق على الهدف، لكنّ التكلفة مرتفعة", "صحيح أنّ الفكرة صحيحة، إلا أنّ التنفيذ صعب"]),
            T("Answer politely.", ["هل توافق على المؤتمر في يونيو؟ (partly, timing is hard)"],
              ["أوافق جزئياً، لكنّ التوقيت صعب"]),
        ]))),
]

THIRD["B2"] = [
    ("B2-U1", "B2-U1-L3", L(
        "Relative clauses that carry an argument",
        "الذي، التي، الذين turn a sentence into a noun you can argue about. The pronoun agrees with the "
        "antecedent — and everything inside the clause still has to be grammatically correct on its own.",
        [V("الذي", "alladhī", "who/which (m. sg.)", "relative pronoun"),
         V("التي", "allatī", "who/which (f. sg.)", "relative pronoun"),
         V("الذين", "alladhīna", "who (m. pl.)", "relative pronoun"),
         V("حيث", "ḥayth", "where, in that", "conjunction"),
         V("اللذان", "alladhāni", "the two who", "relative pronoun")],
        G("The clause agrees with its antecedent, the pronoun inside agrees with its job",
          "noun + alladhī/atī + clause with a resumptive pronoun",
          "التقرير الذي قرأتُه أمس (the report that I read yesterday — the ـه resumes the report). If "
          "the relative pronoun is the clause's subject, no resumptive pronoun: الرجل الذي وصل صديقي.",
          [X("هذه هي الخطة التي اقترحها الفريق.", "hādhihi hiya al-khuṭṭa allatī iqtaraḥahā al-farīq.", "This is the plan that the team proposed."),
           X("البيانات التي وصلتنا ناقصة.", "al-bayānāt allatī waṣalatnā nāqiṣa.", "The data that reached us is incomplete."),
           X("كتبتُ إلى المدير الذي وعدني بالردّ.", "katabtu ilā al-mudīr alladhī waʿadanī bi-l-radd.", "I wrote to the director who promised me an answer.")],
          [("التقرير التي قرأتُه.", "التقرير الذي قرأتُه.", "التقرير is masculine: الذي."),
           ("الخطة الذي اقترحها الفريق.", "الخطة التي اقترحها الفريق.", "الخطة is feminine: التي.")]),
        [D("منى", "ما رأيك في الاقتراح الذي أرسله المدير؟", "mā raʾyuk fī al-iqtirāḥ alladhī arsalahu al-mudīr?", "What do you think of the proposal the director sent?"),
         D("طارق", "الفكرة التي فيه واضحة، لكنّ الأرقام التي تدعمها قديمة.", "al-fikra allatī fīhi wāḍiḥa, lākinna al-arqām allatī tadʿamuhā qadīma.", "The idea in it is clear, but the figures that support it are old."),
         D("منى", "إذاً نطلب البيانات التي وصلت هذا الأسبوع.", "idhan naṭlub al-bayānāt allatī waṣalat hādhā al-usbūʿ.", "Then we ask for the data that arrived this week."),
         D("طارق", "وهذا هو الحلّ الذي أقترحه أيضاً.", "wa-hādhā huwa al-ḥall alladhī aqtariḥuhu aydan.", "That is the solution I propose as well.")],
        WS("Relative-clause worksheet", [
            T("Join with الذي / التي.", ["قرأتُ التقرير. التقرير مفيد.", "وصلت الطالبة. الطالبة من تونس."],
              ["التقرير الذي قرأتُه مفيد", "الطالبة التي وصلت من تونس"]),
            T("Add the resumptive pronoun.", ["الكتاب … كتبتُه", "الرسالة … أرسلتُها"],
              ["الكتاب الذي كتبتُه", "الرسالة التي أرسلتُها"]),
        ]))),
    ("B2-U2", "B2-U2-L3", L(
        "Hedging: how sure are you?",
        "Arabic stacks certainty in a visible ladder: من المؤكد أنّ at the top, من المرجّح أنّ, من "
        "المحتمل أنّ in the middle, ربما and قد lower down. A professional who names their level of "
        "doubt is harder to argue with than one who asserts.",
        [V("من المؤكد", "min al-muʾakkad", "it is certain that", "phrase"),
         V("من المرجّح", "min al-murajjaḥ", "it is likely that", "phrase"),
         V("من المحتمل", "min al-muḥtamal", "it is possible that", "phrase"),
         V("ربما", "rubbamā", "perhaps", "adverb"),
         V("قد", "qad", "may; already", "particle")],
        G("Certainty ladder",
          "min al-muʾakkad anna… > min al-murajjaḥ anna… > min al-muḥtamal anna… > rubbamā > qad",
          "من المرجّح أنّ الأسعار سترتفع. ربما نتأخر قليلاً. قد يكون التقرير جاهزاً غداً. Notice أنّ "
          "after the impersonal frames, and that ربما and قد attach to a verb.",
          [X("من المؤكد أنّ المشروع سيبدأ في يناير.", "min al-muʾakkad anna al-mashrūʿ sa-yabdā fī Yanyā.", "It is certain the project will start in January."),
           X("من المحتمل أنّ التكلفة أعلى من التقدير.", "min al-muḥtamal anna al-taklifa aʿlā min al-taqdīr.", "It is possible the cost is higher than the estimate."),
           X("قد نضطرّ إلى تأجيل الاجتماع.", "qad naḍṭarr ilā taʾjīl al-ijtimāʿ.", "We may have to postpone the meeting.")],
          [("ربما الرئيس سيأتي.", "ربما يأتي الرئيس.", "ربما normally introduces a verb in the jussive; سيأتي after ربما sounds like a translation."),
           ("من المحتمل التكلفة أعلى.", "من المحتمل أنّ التكلفة أعلى.", "The impersonal frame needs أنّ to open the clause.")]),
        [D("هيثم", "هل ستنشر النتائج غداً؟", "hal sa-tanshur al-natāʾij ghadan?", "Will you publish the results tomorrow?"),
         D("ليلى", "من المرجّح أنّها جاهزة غداً، ربما بعد الظهر.", "min al-murajjaḥ annahā jāhiza ghadan, rubbamā baʿda al-ẓuhr.", "They are likely ready tomorrow, perhaps in the afternoon."),
         D("هيثم", "وهل الأرقام مؤكدة؟", "wa-hal al-arqām muʾakkada?", "And are the figures confirmed?"),
         D("ليلى", "من المحتمل أنّ رقماً أو رقمين سيتغيران.", "min al-muḥtamal anna raqman aw raqmayn sa-yataghayyarān.", "It is possible that a number or two will change.")],
        WS("Hedging worksheet", [
            T("Put it on the certainty ladder.", ["sure: the deal will close", "likely: they accept", "possible: a delay"],
              ["من المؤكد أنّ الاتفاق سيُبرم", "من المرجّح أنّهم يقبلون", "من المحتمل أنّ هناك تأخيراً"]),
            T("Soften the claim.", ["الأسعار ستنخفض. (possibly)", "الحلّ سيعمل. (probably)"],
              ["قد تنخفض الأسعار", "من المرجّح أنّ الحلّ سيعمل"]),
        ]))),
    ("B2-U3", "B2-U3-L3", L(
        "Hosting and being hosted: كرم الضيافة",
        "ضيافة is not a hospitality industry; it is a duty. The host pushes food, the guest praises, "
        "and both know the script: تفضّل بالدخول، البيت بيتك، والله يكرمك for thanks in the spoken "
        "register. Formal letters use the same grammar with cooler words.",
        [V("ضيف", "ḍayf", "guest", "noun"),
         V("مضيف", "muḍīf", "host", "noun"),
         V("كرم", "karam", "generosity", "noun"),
         V("تفضّل بالدخول", "tafaḍḍal bi-l-dukhūl", "please come in", "phrase"),
         V("البيت بيتك", "al-bayt baytak", "the house is yours", "phrase")],
        G("Hospitality frames",
          "tafaḍḍal bi- + verbal noun · al-bayt baytuk · imperative + min faḍlik",
          "The invitation is an imperative softened by the person: تفضّل بالدخول، تفضّلوا بالجلوس. "
          "Refusing food is negotiable, refusing the welcome is not: a single bite keeps the script intact.",
          [X("أهلاً وسهلاً، تفضّل بالدخول.", "ahlan wa-sahlan, tafaḍḍal bi-l-dukhūl.", "Welcome — please come in."),
           X("تفضّل، البيت بيتك.", "tafaḍḍal, al-bayt baytuk.", "Please, the house is yours."),
           X("شكراً لكرمك، لقد أفرطتَ في اللطف.", "shukran li-karamik, laqad afraṭta fī al-luṭf.", "Thank you for your generosity — you have gone too far in kindness.")],
          [("العشاء كان كريم.", "العشاء كان كريماً.", "كريم is an adjective here and takes the accusative after كان."),
           ("تفضّل بالدخول شكراً.", "تفضّل بالدخول.", "The invitation is already polite; شكراً belongs to the answer.")]),
        [D("المضيف", "أهلاً وسهلاً! تفضّل، البيت بيتك.", "ahlan wa-sahlan! tafaḍḍal, al-bayt baytuk.", "Welcome! Please, the house is yours."),
         D("الضيف", "شكراً لكرمك، هذا لطف كبير.", "shukran li-karamik, hādhā luṭf kabīr.", "Thank you for your generosity — that is great kindness."),
         D("المضيف", "تفضّل بعض الشاي والتمر.", "tafaḍḍal baʿḍ al-shāy wa-l-tamr.", "Please have some tea and dates."),
         D("الضيف", "بكل سرور، شكراً جزيلاً.", "bi-kull surūr, shukran jazīlan.", "With pleasure, thank you very much.")],
        WS("Hospitality worksheet", [
            T("Host the guest in Arabic.", ["invite in", "offer tea", "insist a second time"],
              ["تفضّل بالدخول", "تفضّل بعض الشاي", "لا، أصرّ، تفضّل مرة أخرى"]),
            T("Answer as the guest.", ["praise the host", "accept politely"],
              ["شكراً لكرمك", "بكل سرور، شكراً"]),
        ]))),
]

THIRD["C1"] = [
    ("ar-c1-u1", "ar-c1-l7", L(
        "Attribution: report a claim without vouching for it",
        "روى، نقل عن، أفاد بأنّ، صرّح، بحسب — reporting verbs move the truth out of your mouth and into "
        "the source's. This is how a formal Arabic text states something contested without taking a "
        "position, and how it stays accurate while doing so.",
        [V("أفاد بأنّ", "afāda bi-anna", "reported that", "verb"),
         V("نقل عن", "naqala ʿan", "quoted from", "verb"),
         V("صرّح", "ṣarraḥa", "stated, declared", "verb"),
         V("بحسب", "bi-ḥasab", "according to", "preposition"),
         V("وفقاً لـ", "wafqan li-", "in accordance with", "preposition")],
        G("Distance by reporting frame",
          "afāda / naqala / ṣarraḥa bi-anna… · bi-ḥasab + source · wafqan li- + source",
          "أفاد مصدر مسؤول بأنّ الاتفاق شبه جاهز. The frame does not make the claim true; it makes "
          "clear who owns it. Pair it with a hedge when the source is weak: بحسب ما وصلني، والله أعلم.",
          [X("نقلت الوكالة عن وزير النفط أنّ الإنتاج سيرتفع.", "naqalat al-wakāla ʿan wazīr al-nafṭ anna al-intāj sa-yartafiʿ.", "The agency quoted the oil minister as saying production will rise."),
           X("وفقاً للتقرير، تراجعت الصادرات 3%.", "wafqan li-l-taqrīr, tarājaʿat al-ṣādirāt 3%.", "According to the report, exports fell 3%."),
           X("بحسب ما وصلني، الاجتماع مؤجل — والله أعلم.", "bi-ḥasab mā waṣalanī, al-ijtimāʿ muʾajjal — wa-llāhu aʿlam.", "As far as I have heard, the meeting is postponed — God knows best.")],
          [("أفاد المصدر أنّ الاتفاق جاهز، إذاً نحن على يقين.", "أفاد المصدر أنّ الاتفاق جاهز؛ وهو ما لم يتأكد بعد.", "A report is not proof. Keeping the reporting frame means not sliding into certainty."),
           ("بحسباً للتقرير…", "بحسب التقرير…", "بحسب is a preposition and does not take tanwīn.")]),
        [D("الزميل", "هل وافق الوزير فعلاً؟", "hal wāfaqa al-wazīr fiʿlan?", "Did the minister actually agree?"),
         D("المحرّر", "نقلت الوكالة عنه أنّه يوافق من حيث المبدأ.", "naqalat al-wakāla ʿanhu annahu yuwāfiq min ḥaythu al-mabdāʾ.", "The agency quoted him as agreeing in principle."),
         D("الزميل", "هل نكتبها خبراً مؤكداً؟", "hal naktubuhā khabaran muʾakkadan?", "Do we write it as confirmed news?"),
         D("المحرّر", "لا؛ نكتب: «بحسب الوكالة، يبدو أنّه يوافق» — والفرق كبير.", "lā; naktub: bi-ḥasab al-wakāla, yabdū annahu yuwāfiq — wa-l-farq kabīr.", "No: we write 'according to the agency, he appears to agree' — and the difference is large.")],
        WS("Attribution worksheet", [
            T("Move the claim into a reporting frame.", ["الأسعار سترتفع. (a source)", "الاتفاق أُبرم. (the ministry)"],
              ["أفاد مصدر بأنّ الأسعار سترتفع", "نقلنا عن الوزارة أنّ الاتفاق أُبرم"]),
            T("Downgrade the certainty.", ["الاتفاق جاهز. (report only)", "الوزير وافق. (quote)"],
              ["بحسب ما وصلني، يبدو أنّ الاتفاق جاهز", "نقلت الوكالة عنه أنّه وافق"]),
        ]))),
    ("ar-c1-u2", "ar-c1-l8", L(
        "Qualification: how far a claim reaches",
        "Precision at C1 means naming the scope: إلى حدّ كبير، في حدود، بصورة جزئية، باستثناء، لا يعني "
        "بالضرورة. Arabic marks scope with a fixed set of phrases, and dropping them is what turns a "
        "careful paragraph into an overclaim.",
        [V("إلى حدّ كبير", "ilā ḥadd kabīr", "to a large extent", "phrase"),
         V("في حدود", "fī ḥudūd", "within the limits of", "phrase"),
         V("باستثناء", "bi-stithnāʾ", "with the exception of", "preposition"),
         V("لا يعني بالضرورة", "lā yaʿnī bi-l-ḍarūra", "does not necessarily mean", "phrase"),
         V("بقدر ما", "bi-qadr mā", "to the extent that", "conjunction")],
        G("Scope limiters",
          "ilā ḥadd kabīr · fī ḥudūd + number · bi-stithnāʾ + noun · lā yaʿnī bi-l-ḍarūra anna…",
          "ارتفعت الصادرات في حدود 4% — a precise range, not a triumph. صحيح في معظم الحالات "
          "باستثناء حالتين. And the professional move: هذا لا يعني بالضرورة أنّ السبب واحد.",
          [X("النتائج إيجابية إلى حدّ كبير، باستثناء قطاع واحد.", "al-natāʾij ījābiyya ilā ḥadd kabīr, bi-stithnāʾ qiṭāʿ wāḥid.", "The results are largely positive, with one sector excepted."),
           X("تحسّن الطلب في حدود 2% فقط.", "taḥassana al-ṭalab fī ḥudūd 2% faqaṭ.", "Demand improved by only about 2%."),
           X("تأخّر التسليم لا يعني بالضرورة أنّ الخطة فاشلة.", "taʾakhkhara al-taslīm lā yaʿnī bi-l-ḍarūra anna al-khuṭṭa fāshila.", "A late delivery does not necessarily mean the plan failed.")],
          [("النتائج جيدة باستثناء.", "النتائج جيدة باستثناء قطاع واحد.", "باستثناء needs its exception named."),
           ("ارتفعت الأسعار في حدود.", "ارتفعت الأسعار في حدود 4%.", "في حدود frames a number, not a full stop.")]),
        [D("المدير", "كيف تُلخّص الأداء؟", "kayfa tulakhkhiṣ al-adāʾ?", "How do you summarise performance?"),
         D("المحلّل", "تحسّن إلى حدّ كبير في الشمال، وفي حدود 2% في الجنوب.", "taḥassana ilā ḥadd kabīr fī al-shamāl, wa-fī ḥudūd 2% fī al-janūb.", "It improved greatly in the north, and only about 2% in the south."),
         D("المدير", "وهل يعني ذلك فشل خطتنا؟", "wa-hal yaʿnī dhālika fashal khuṭṭatinā?", "Does that mean our plan failed?"),
         D("المحلّل", "لا يعني بالضرورة؛ الفرق في البنية التحتية، لا في الطلب.", "lā yaʿnī bi-l-ḍarūra; al-farq fī al-bunya al-taḥtiyya, lā fī al-ṭalab.", "Not necessarily: the difference is infrastructure, not demand.")],
        WS("Scope worksheet", [
            T("Limit the claim.", ["ارتفعت المبيعات. (about 3%)", "الخبر صحيح. (in most cases)"],
              ["ارتفعت المبيعات في حدود 3%", "الخبر صحيح في معظم الحالات"]),
            T("Refuse the false inference.", ["تأخّرنا، إذاً المشروع فشل.", "انخفض سهم واحد، إذاً الشركة في خطر."],
              ["التأخير لا يعني بالضرورة أنّ المشروع فشل", "انخفاض سهم واحد لا يعني بالضرورة أنّ الشركة في خطر"]),
        ]))),
    ("ar-c1-u3", "ar-c1-l9", L(
        "Genre transform: memo to press release",
        "The same facts live in a memo and a release, and the register changes at every level: the memo "
        "is passive and internal (تمّت الموافقة على…), the release is active and outward (أعلنت "
        "الشركة…). Transforming without losing a fact is the C1 skill.",
        [V("مذكّرة", "mudhakkara", "internal memo", "noun"),
         V("بيان صحفي", "bayān ṣaḥafī", "press release", "noun"),
         V("صياغة", "ṣiyāgha", "wording, drafting", "noun"),
         V("جمهور", "jamhūr", "audience", "noun"),
         V("بصيغة", "bi-ṣīgha", "in the form of", "phrase")],
        G("Internal passive → outward active",
          "tamma + verbal noun (memo) → announced/decided + subject (release)",
          "Memo: تمّت الموافقة على الميزانية في اجتماع أمس. Release: أعلنت الشركة أمس موافقتها على "
          "الميزانية. Same facts; the actor is named, the sentence gets shorter, and the reader knows who did it.",
          [X("تمّ إقرار الخطة في جلسة أول أمس.", "tamma iqrār al-khuṭṭa fī jalsa awwal ams.", "The plan was approved in a session the day before yesterday. (memo)"),
           X("أقرّت الشركة الخطة أول أمس.", "aqarrat al-sharika al-khuṭṭa awwal ams.", "The company approved the plan the day before yesterday. (release)"),
           X("بحسب البيان، سيبدأ التنفيذ في سبتمبر.", "bi-ḥasab al-bayān, sa-yabdā al-tanfīdh fī Sibtambar.", "According to the statement, implementation begins in September.")],
          [("تمّت الموافقة على الميزانية من قبل الإدارة في الاجتماع.", "وافقت الإدارة على الميزانية في الاجتماع.", "The passive frame is a memo habit; a public text names the actor."),
           ("أعلنت الشركة عن أنّ الخطة…", "أعلنت الشركة أنّ الخطة…", "أعلن takes a direct أنّ clause; عن is not needed here.")]),
        [D("المديرة", "لدينا مذكّرة داخلية، ونريد بياناً صحفياً.", "ladaynā mudhakkara dākhiliyya, wa-nurīd bayānan ṣaḥafiyyan.", "We have an internal memo, and we want a press release."),
         D("الكاتب", "ما الجمهور؟ المذكّرة مخاطبة للإدارة، والبيان للصحافة.", "mā al-jamhūr? al-mudhakkara mukhāṭaba li-l-idāra, wa-l-bayān li-l-ṣaḥāfa.", "Who is the audience? The memo addresses management; the release addresses the press."),
         D("المديرة", "أزل الجمل المبنية للمجهول وأضف الاسم.", "azil al-jumal al-mabniyya li-l-majhūl wa-aḍif al-ism.", "Remove the passive sentences and add the subject."),
         D("الكاتب", "إذاً: «أعلنت الشركة…» بدل «تمّ الإعلان عن…».", "idhan: aʿlanat al-sharika… badal tamma al-iʿlān ʿan…", "So: 'The company announced…' instead of 'an announcement was made…'.")],
        WS("Transform worksheet", [
            T("Turn the memo line into a release line.", ["تمّ توقيع العقد.", "تمّت الموافقة على الطلب."],
              ["وقّعت الشركة العقد", "وافقت الإدارة على الطلب"]),
            T("Trim the padding.", ["قامت الشركة بالإعلان عن إطلاق خدمة جديدة.", "تمّ اتخاذ قرار بإيقاف الإنتاج."],
              ["أعلنت الشركة عن خدمة جديدة", "قرّرت الشركة إيقاف الإنتاج"]),
        ]))),
]

THIRD["C2"] = [
    ("ar-c2-u1", "ar-c2-l7", L(
        "Implicature: what the text says without saying",
        "A C2 reader reads the gap. مؤشّر، دلالة، ضمنياً، يُفهم من — these words let you name the "
        "inference and then hold it to account: is the writer telling me, or only letting me think it?",
        [V("يُفهم من", "yufham min", "it is understood from", "phrase"),
         V("ضمنياً", "ḍimniyyan", "implicitly", "adverb"),
         V("دلالة", "dalāla", "indication, connotation", "noun"),
         V("مؤشّر", "muʾashshir", "indicator", "noun"),
         V("تلميح", "talmīḥ", "hint, allusion", "noun")],
        G("Naming an inference",
          "yufham min + source + anna… · ḍimniyyan + verb · dalāla ʿalā + noun",
          "يُفهم من الفقرة الثالثة أنّ الكاتب يشكّ في الأرقام — لكنّه لم يكتب ذلك صراحة. Naming the "
          "inference is not the same as asserting it: keep the frame, mark the degree, and the paragraph stays honest.",
          [X("يُفهم من السياق أنّ القرار كان سياسياً.", "yufham min al-siyāq anna al-qarār kāna siyāsiyyan.", "It is understood from the context that the decision was political."),
           X("أشار التقرير ضمنياً إلى وجود تأخير.", "ashāra al-taqrīr ḍimniyyan ilā wujūd taʾkhīr.", "The report implicitly pointed to a delay."),
           X("هذا مؤشّر على تحوّل في الموقف، لا إعلان عنه.", "hādhā muʾashshir ʿalā taḥawwul fī al-mawqif, lā iʿlān ʿanhu.", "This is an indicator of a shift in position, not an announcement of one.")],
          [("الكاتب يقول إنّ الأرقام كاذبة.", "يُفهم من الفقرة أنّ الكاتب يشكّ في الأرقام.", "Reading a hint and reporting it as a statement is the classic C2 error of over-reading."),
           ("أشار إلى عن التأخير.", "أشار إلى التأخير.", "One preposition: إلى.")]),
        [D("القارئ", "هل يقول النصّ إنّ الوزير كذب؟", "hal yaqūl al-naṣṣ inna al-wazīr kadhaba?", "Does the text say the minister lied?"),
         D("المحرّر", "لا يقولها صراحة؛ يُفهم من ترتيب الوقائع أنّه يشكّ.", "lā yaqūlahā ṣarāḥatan; yufham min tartīb al-waqāʾiʿ annahu yashukk.", "It does not say it explicitly; from the ordering of events, it is understood that he doubts."),
         D("القارئ", "إذاً العنوان تجاوز النصّ.", "idhan al-ʿunwān tajāwaza al-naṣṣ.", "Then the headline went beyond the text."),
         D("المحرّر", "تماماً؛ وهذا فرق يُحاسب عليه القارئ المحترف.", "tamāman; wa-hādhā farq yuḥāsab ʿalayhi al-qāriʾ al-muḥtarif.", "Exactly — and that is a difference the professional reader can be held to.")],
        WS("Inference worksheet", [
            T("Name the inference, keep it an inference.", ["The writer repeats 'some sources'. (doubt)", "The date is never given. (something is hidden)"],
              ["يُفهم من تكرار «مصادر» أنّ الكاتب يشكّ في المعلومة", "غياب التاريخ مؤشّر على أنّ الكاتب يتجنّب الدقة"]),
            T("Correct the over-reading.", ["النص يقول إنّ الشركة ستفلس.", "النص يقول إنّ الوزير غاضب."],
              ["يُفهم من النص أنّ الشركة تواجه صعوبات، دون أن يقول بالإفلاس", "تلميح النص غضب الوزير، دون أن يُصرّح به"]),
        ]))),
    ("ar-c2-u2", "ar-c2-l8", L(
        "الطباق والجناس: figures a headline can carry",
        "طباق pairs opposites, جناس echoes two roots, سجع closes a line on a matching cadence. "
        "A headline can carry one figure and no more; two figures turn it into a slogan, and three into "
        "a parody. Judging that line is the C2 edit.",
        [V("طباق", "ṭibāq", "antithesis, paired opposites", "noun"),
         V("جناس", "jinās", "paronomasia, a play on similar roots", "noun"),
         V("سجع", "sajʿ", "rhymed prose", "noun"),
         V("كناية", "kināya", "metonymy, indirect allusion", "noun"),
         V("بلاغة", "balāgha", "rhetoric, eloquence", "noun")],
        G("One figure per headline",
          "ṭibāq: X wa-Y (opposites) · jinās: two forms of one root",
          "طباق: الحرب والسلام وجهان لقضية واحدة. جناس: من مَلكَ وقتَه مَلكَ أمرَه. The figure frames the "
          "argument before the reader has judged it — so an editor asks: does the frame help them think, or decide for them?",
          [X("الغنى والفقر في مدينة واحدة.", "al-ghinā wa-l-faqr fī madīna wāḥida.", "Wealth and poverty in one city."),
           X("من ملك وقته ملك أمره.", "man malaka waqtahu malaka amrah.", "Whoever masters his time masters his affair."),
           X("صمتٌ يقول أكثر مما يقول الكلام.", "ṣamtun yaqūl akthar mimmā yaqūl al-kalām.", "A silence that says more than speech says.")],
          [("الغنى والفقر والطبقة الوسطى في مدينة.", "الغنى والفقر في مدينة واحدة.", "A third term dissolves the pair; طباق needs two poles."),
           ("من ملك وقته ملك ملكه.", "من ملك وقته ملك أمره.", "Repeating one root is جناس only when the meanings differ; otherwise it is a slip.")]),
        [D("رئيس التحرير", "ما رأيك في العنوان؟", "mā raʾyuka fī al-ʿunwān?", "What do you think of the headline?"),
         D("المحرّر", "فيه طباق قوي: الحرب والسلام.", "fīhi ṭibāq qawī: al-ḥarb wa-l-salām.", "It has a strong antithesis: war and peace."),
         D("رئيس التحرير", "لكنّه يوحي بأنّ الخيارين متساويان.", "lākinnahu yūḥī bi-anna al-khiyārayn mutasāwiyān.", "But it suggests the two options are equal."),
         D("المحرّر", "إذاً أكسر التوازن: «السلام الذي يشبه الحرب».", "idhan aksir al-tawāzun: al-salām alladhī yushbih al-ḥarb.", "Then I break the balance: 'the peace that resembles war'.")],
        WS("Figure worksheet", [
            T("Build a طباق line.", ["city / silence", "promise / deadline"],
              ["مدينةٌ تتكلّم وصمتٌ يسمع", "وعدٌ طويل ومهلةٌ قصيرة"]),
            T("Cut from three figures to one.", ["سلام وحرب وغنى وفقر.", "صمت كلام كلام صمت."],
              ["سلامٌ يشبه الحرب", "صمتٌ يتكلّم"]),
        ]))),
    ("ar-c2-u3", "ar-c2-l9", L(
        "Correcting an expert without losing them",
        "The last skill is social: you are wrong and the room is watching. Arabic gives you a staircase "
        "— نعم، لكن؛ صحيح أنّ… إلا أنّ؛ لستُ أختلف معك في… بل؛ أعيد الصياغة — each step keeping the "
        "person's face while moving the claim.",
        [V("استدراك", "istidrāk", "correction, emendation", "noun"),
         V("أعيد الصياغة", "uʿīd al-ṣiyāgha", "let me restate", "phrase"),
         V("لستُ أختلف معك في", "lastu akhtalif maʿak fī", "I don't disagree with you on", "phrase"),
         V("جوهر", "jawhar", "substance, essence", "noun"),
         V("تلطّف", "talaṭṭuf", "tact, gentle handling", "noun")],
        G("The correction staircase",
          "nʿam, lākin… → ṣaḥīḥ anna…, illā anna… → lastu akhtalif fī…, bal → uʿīd al-ṣiyāgha",
          "لستُ أختلف معك في الهدف، بل في الوسيلة. Start with the shared ground, move by smallest step, "
          "and restate the other person's point in their own terms before you touch it — if the restatement "
          "is wrong, the disagreement is not yet real.",
          [X("لا أختلف معك في التشخيص، بل في العلاج.", "lā akhtalif maʿak fī al-tashkhīṣ, bal fī al-ʿilāj.", "I don't disagree with the diagnosis, but with the treatment."),
           X("دعني أُعد صياغة قولك حتى أتأكد أنّني فهمته.", "daʿnī uʿid ṣiyāghat qawlik ḥattā ataʾakkad annanī fahimtuhu.", "Let me restate your point to be sure I understood it."),
           X("صحيح أنّ الأرقام دقيقة، إلا أنّ تفسيرها محلّ نقاش.", "ṣaḥīḥ anna al-arqām daqīqa, illā anna tafsīrahā maḥall niqāsh.", "True, the figures are accurate — but their interpretation is open to debate.")],
          [("أنت مخطئ تماماً.", "دعني أفهم: تقصد أنّ… هل هذا دقيق؟", "A flat contradiction forfeits the room; the staircase keeps the claim and the person separate."),
           ("لا أختلف معك في التشخيص، لكن في العلاج.", "لا أختلف معك في التشخيص، بل في العلاج.", "After a negation, the correct contrast is بل, not لكن.")]),
        [D("الخبير", "إذاً الحلّ بسيط وواضح.", "idhan al-ḥall basīṭ wa-wāḍiḥ.", "So the solution is simple and clear."),
         D("المدير", "دعني أُعد صياغة قولك: ترى أنّ السبب واحد.", "daʿnī uʿid ṣiyāghat qawlik: tarā anna al-sabab wāḥid.", "Let me restate your point: you believe there is one cause."),
         D("الخبير", "تماماً.", "tamāman.", "Exactly."),
         D("المدير", "لا أختلف معك في تحليلك، بل في أنّه يغطّي كل الحالات.", "lā akhtalif maʿak fī taḥlīlik, bal fī annahu yughaṭṭī kull al-ḥālāt.", "I don't disagree with your analysis, but with whether it covers all cases.")],
        WS("Correction worksheet", [
            T("Climb the staircase.", ["You are wrong about the cost.", "That number cannot be right."],
              ["صحيح أنّ التكلفة محلّ نقاش، إلا أنّ الأرقام تدعم تقديرنا", "دعني أفهم مصدر الرقم؛ يبدو أنّ هناك فرقاً في التقدير"]),
            T("Separate person from claim.", ["He ignores the data.", "His plan will fail."],
              ["لا أختلف معه في قراءة البيانات، بل في وزنها", "أتفق مع الهدف، وأختلف في توقيت التنفيذ"]),
        ]))),
]


# ── the five half-step rungs ────────────────────────────────────────────────
# A1+ and A2+ first; B1+, B2+ and C1+ follow below.

HALFSTEPS = {}

HALFSTEPS["A1+"] = {
    "title": "Arabic A1+ — Getting around",
    "native": NATIVE,
    "goals": [
        "Ask for directions, tickets and things you need",
        "Give a phone number, an address and a price",
        "Name the days, tell the time and make a plan — or refuse one politely",
    ],
    "units": [
        {"id": "A1+-U1", "title": "In the street", "lessons": [
            L("Right, left, straight: polite directions",
              "Directions are imperatives, and in Arabic the polite imperative is the point: انعطف "
              "يميناً is an order, انعطف يميناً من فضلك is a request. Learn four you will use every "
              "day: يمين، شمال، مستقيم، إلى الأمام.",
              [V("يمين", "yamīn", "right", "noun"),
               V("شمال", "shamāl", "left", "noun"),
               V("مستقيم", "mustaqīm", "straight ahead", "adjective"),
               V("انعطف", "inʿaṭif", "turn (imperative)", "verb"),
               V("قريب", "qarīb", "near", "adjective")],
              G("Polite imperative",
                "imperative + min faḍlik / law samaḥt",
                "انعطف يميناً، ثمّ سِرْ مستقيماً. Add من فضلك and it becomes a request you can make of a "
                "stranger. To a woman: انعطفي، سيري.",
                [X("انعطف يميناً عند المسجد.", "inʿaṭif yamīnan ʿinda al-masjid.", "Turn right at the mosque."),
                 X("سِرْ مستقيماً ثمّ اسأل مرة أخرى.", "sir mustaqīman thumma isʾal marra ukhrā.", "Go straight, then ask again."),
                 X("هل المحطة بعيدة؟", "hal al-maḥaṭṭa baʿīda?", "Is the station far?")],
                [("انعطف يمين شكراً.", "انعطف يميناً من فضلك.", "يمين takes the accusative -an as an adverb here."),
                 ("سِر في مستقيماً.", "سِرْ مستقيماً.", "مستقيماً is already an adverbial accusative; في is not needed.")]),
              [D("سائح", "من فضلك، أين محطة القطار؟", "min faḍlik, ayna maḥaṭṭat al-qiṭār?", "Please, where is the train station?"),
               D("مقيم", "سِرْ مستقيماً ثمّ انعطف يميناً عند المسجد.", "sir mustaqīman thumma inʿaṭif yamīnan ʿinda al-masjid.", "Go straight, then turn right at the mosque."),
               D("سائح", "وهل هي بعيدة من هنا؟", "wa-hal hiya baʿīda min hunā?", "And is it far from here?"),
               D("مقيم", "خمس دقائق على القدمين، ليست بعيدة.", "khams daqāʾiq ʿalā al-qadamayn, laysat baʿīda.", "Five minutes on foot — it is not far.")],
              WS("Directions worksheet", [
                  T("Give the direction in Arabic.", ["turn left", "go straight", "turn right at the pharmacy"],
                    ["انعطف شمالاً", "سِرْ مستقيماً", "انعطف يميناً عند الصيدلية"]),
                  T("Answer the lost visitor.", ["أين البنك؟ (opposite the park)", "هل هي بعيدة؟ (five minutes)"],
                    ["البنك مقابل الحديقة", "لا، خمس دقائق على القدمين"]),
              ])),
            L("Tickets, fare and the driver",
              "A ticket is a transaction, and Arabic transactions are short: أريد تذكرة إلى…، بكم؟، متى "
              "يتحرّك القطار؟ Three lines and you are on your way.",
              [V("تذكرة", "tadhkira", "ticket", "noun"),
               V("محطة", "maḥaṭṭa", "station", "noun"),
               V("قطار", "qiṭār", "train", "noun"),
               V("بكم؟", "bikam?", "how much?", "interrogative"),
               V("يتحرّك", "yataḥarrak", "it departs, moves", "verb")],
              G("Buying a ticket",
                "urīd tadhkira ilā + place · bikam al-tadhkira? · matā yataḥarrak?",
                "أريد تذكرة إلى الإسكندرية من فضلك. بكم التذكرة؟ عشرون جنيهاً. متى يتحرّك القطار؟ To "
                "ask for two: تذكرتين.",
                [X("أريد تذكرتين إلى أسوان.", "urīd tadhkiratayn ilā Aswān.", "I want two tickets to Aswan."),
                 X("بكم التذكرة إلى المنصورة؟", "bikam al-tadhkira ilā al-Manṣūra?", "How much is the ticket to Mansoura?"),
                 X("متى يتحرّك القطار التالي؟", "matā yataḥarrak al-qiṭār al-tālī?", "When does the next train leave?")],
                [("أريد تذكرة في أسوان.", "أريد تذكرة إلى أسوان.", "إلى marks the destination; في means inside."),
                 ("بكم من التذكرة؟", "بكم التذكرة؟", "بكم is already a question; من is not needed.")]),
              [D("مسافر", "أريد تذكرة إلى المنصورة من فضلك.", "urīd tadhkira ilā al-Manṣūra min faḍlik.", "I want a ticket to Mansoura, please."),
               D("موظّف", "ذهاب فقط أم ذهاب وعودة؟", "dhahāb faqaṭ am dhahāb wa-ʿawda?", "One way or return?"),
               D("مسافر", "ذهاب فقط. بكم؟", "dhahāb faqaṭ. bikam?", "One way. How much?"),
               D("موظّف", "خمسة وأربعون جنيهاً، والقطار يتحرّك السابعة والنصف.", "khamsa wa-arbaʿūn junayhan, wa-l-qiṭār yataḥarrak al-sābiʿa wa-l-niṣf.", "Forty-five pounds, and the train leaves at half past seven.")],
              WS("Ticket worksheet", [
                  T("Ask for it in Arabic.", ["two tickets to the museum", "how much is the ticket?", "when does the train leave?"],
                    ["تذكرتان إلى المتحف", "بكم التذكرة؟", "متى يتحرّك القطار؟"]),
                  T("Answer as the clerk.", ["ذهاب وعودة؟ (no, one way)", "بكم؟ (forty-five pounds)"],
                    ["لا، ذهاب فقط", "خمسة وأربعون جنيهاً"]),
              ])),
            L("Where exactly? أمام، بجانب، مقابل",
              "Give a landmark and a relation, not a coordinate: أمام المسجد، بجانب الصيدلية، مقابل "
              "البنك. يقع is the verb for where something sits.",
              [V("أمام", "amām", "in front of", "noun"),
               V("بجانب", "bi-jānib", "next to", "preposition"),
               V("مقابل", "muqābil", "opposite", "preposition"),
               V("صيدلية", "ṣaydaliyya", "pharmacy", "noun"),
               V("يقع", "yaqaʿ", "it is located", "verb")],
              G("Landmark + relation",
                "yaqaʿ + place + amām / bi-jānib / muqābil + landmark",
                "يقع البنك مقابل الحديقة. The relation word takes the genitive: أمام المسجد، بجانب "
                "الصيدلية. In speech the ending is dropped: البنك مقابل الحديقة.",
                [X("الصيدلية بجانب المخبز.", "al-ṣaydaliyya bi-jānib al-makhbaz.", "The pharmacy is next to the bakery."),
                 X("يقع الفندق أمام المحطة.", "yaqaʿ al-funduq amām al-maḥaṭṭa.", "The hotel is in front of the station."),
                 X("المقهى مقابل الجامعة.", "al-maqhā muqābil al-jāmiʿa.", "The café is opposite the university.")],
                [("الصيدلية بجانب المخبزاً.", "الصيدلية بجانب المخبز.", "After بجانب the noun is genitive: المخبزِ, written plainly as المخبز."),
                 ("يقع الفندق أماماً للمحطة.", "يقع الفندق أمام المحطة.", "Relation words take a direct genitive, not لـ.")]),
              [D("زائرة", "أين الصيدلية من فضلك؟", "ayna al-ṣaydaliyya min faḍlik?", "Where is the pharmacy, please?"),
               D("مقيم", "بجانب المخبز، أمام المسجد.", "bi-jānib al-makhbaz, amām al-masjid.", "Next to the bakery, in front of the mosque."),
               D("زائرة", "والمقهى؟", "wa-l-maqhā?", "And the café?"),
               D("مقيم", "المقهى مقابل الحديقة، على بعد خطوات.", "al-maqhā muqābil al-ḥadīqa, ʿalā buʿd khuṭuwāt.", "The café is opposite the park, a few steps away.")],
              WS("Landmark worksheet", [
                  T("Complete with the right relation.", ["الصيدلية ___ المخبز. (next to)", "البنك ___ الحديقة. (opposite)"],
                    ["الصيدلية بجانب المخبز", "البنك مقابل الحديقة"]),
                  T("Describe your own street.", ["(where the bakery is)", "(where the mosque is)"],
                    ["المخبز…", "المسجد…"]),
              ])),
        ]},
        {"id": "A1+-U2", "title": "Numbers that get you home", "lessons": [
            L("Eleven to a hundred",
              "Arabic builds the teens and tens by joining: أحد عشر (11), واحد وعشرون (21), مئة (100). "
              "The units come first, the ten follows with و.",
              [V("أحد عشر", "aḥada ʿashar", "eleven", "numeral"),
               V("عشرون", "ʿishrūn", "twenty", "numeral"),
               V("خمسون", "khamsūn", "fifty", "numeral"),
               V("مئة", "miʾa", "hundred", "numeral"),
               V("و", "wa", "and (joining tens and units)", "particle")],
              G("Units before tens",
                "unit + wa + ten (21–99)",
                "خمسة وعشرون (25), ثلاثة وستون (63), تسعة وتسعون (99). The counted noun stays singular "
                "accusative after 11–99 in careful Arabic: خمسة وعشرون كتاباً.",
                [X("عندي أربعة وأربعون طالباً.", "ʿindī arbaʿa wa-arbaʿūn ṭāliban.", "I have forty-four students."),
                 X("السعر مئة جنيه.", "al-siʿr miʾa junayh.", "The price is a hundred pounds."),
                 X("الشارع رقم ثلاثة وستين.", "al-shāriʿ raqm thalātha wa-sittīn.", "The street number is sixty-three.")],
                [("عشرون وخمسة = 25؟", "خمسة وعشرون = 25.", "The unit comes first in Arabic: 25 is 'five-and-twenty'."),
                 ("ثلاثة وعشرون كتاب.", "ثلاثة وعشرون كتاباً.", "After 11–99 the counted noun is singular accusative.")]),
              [D("بائع", "كم كتاباً تريد؟", "kam kitāban turīd?", "How many books do you want?"),
               D("زبون", "أريد ثلاثة وعشرين كتاباً.", "urīd thalātha wa-ʿishrīn kitāban.", "I want twenty-three books."),
               D("بائع", "كلّ كتاب بخمسة جنيهات، إذاً مئة وخمسة عشر.", "kull kitāb bi-khamsat junayhāt, idhan miʾa wa-khamsata ʿashar.", "Each book is five pounds, so that is a hundred and fifteen."),
               D("زبون", "حسناً، مئة وعشرون مع التوصيل.", "ḥasanan, miʾa wa-ʿishrūn maʿa al-tawṣīl.", "All right — a hundred and twenty with delivery.")],
              WS("Numbers worksheet", [
                  T("Write the number in Arabic words.", ["44", "63", "99"],
                    ["أربعة وأربعون", "ثلاثة وستون", "تسعة وتسعون"]),
                  T("Say the price in full.", ["ticket 45", "two books 60"],
                    ["خمسة وأربعون جنيهاً", "ستون جنيهاً"]),
              ])),
            L("Phone numbers and addresses",
              "A phone number is read digit by digit: صفر، واحد، اثنان… An address runs building, street, "
              "district, and يقع carries the whole of it.",
              [V("رقم", "raqm", "number", "noun"),
               V("هاتف", "hātif", "telephone", "noun"),
               V("شارع", "shāriʿ", "street", "noun"),
               V("مبنى", "mabnā", "building", "noun"),
               V("عنوان", "ʿunwān", "address", "noun")],
              G("Reading a number aloud",
                "digit + digit … · raqm + number · al-ʿunwān huwa…",
                "هاتفي هو صفر واحد اثنان… Real speech often drops the و between digits. Addresses run "
                "small to large: رقم 12، شارع النيل، الزمالك.",
                [X("ما رقم هاتفك؟", "mā raqm hātifak?", "What is your phone number?"),
                 X("عنواني: شارع النيل، مبنى عشرة.", "ʿunwānī: shāriʿ al-nīl, mabnā ʿashara.", "My address: Nile Street, building ten."),
                 X("أعد الرقم من فضلك.", "aʿid al-raqm min faḍlik.", "Repeat the number, please.")],
                [("رقمي هاتف هو…", "رقم هاتفي هو…", "Two nouns in a row need an idafa or an adjective; رقم هاتفي is the idafa."),
                 ("أسكن في شارع النيل، والعنوان في الزمالك.", "أسكن في شارع النيل، الزمالك.", "The district follows the street directly; في is not repeated.")]),
              [D("موظّفة", "ما رقم هاتفك من فضلك؟", "mā raqm hātifak min faḍlik?", "What is your phone number, please?"),
               D("متقدّم", "صفر واحد صفر اثنان ثلاثة أربعة خمسة ستة سبعة.", "ṣifr wāḥid ṣifr ithnān thalātha arbaʿa khamsa sitta sabʿa.", "Zero one zero two three four five six seven."),
               D("موظّفة", "والعنوان؟", "wa-l-ʿunwān?", "And the address?"),
               D("متقدّم", "شارع النيل، مبنى عشرة، الطابق الثالث.", "shāriʿ al-nīl, mabnā ʿashara, al-ṭābiq al-thālith.", "Nile Street, building ten, third floor.")],
              WS("Address worksheet", [
                  T("Say it in Arabic.", ["my phone number", "third floor", "building ten, Nile Street"],
                    ["رقم هاتفي", "الطابق الثالث", "مبنى عشرة، شارع النيل"]),
                  T("Ask for the details.", ["phone number?", "address?", "repeat, please"],
                    ["ما رقم هاتفك؟", "ما عنوانك؟", "أعد من فضلك"]),
              ])),
            L("Prices: too expensive, can you lower it?",
              "Bargaining runs on four lines: بكم؟، غالي، هل يمكن أن تخفض؟، حسناً آخذه. Keep it "
              "friendly — غالي alone sounds like a complaint, غالي قليلاً softens it.",
              [V("سعر", "siʿr", "price", "noun"),
               V("غالي", "ghālī", "expensive", "adjective"),
               V("رخيص", "rakhīṣ", "cheap", "adjective"),
               V("تخفض", "takhfiḍ", "you lower (it)", "verb"),
               V("حسناً", "ḥasanan", "all right", "adverb")],
              G("Bargaining frames",
                "bikam? · ghālī qalīlan · hal yumkin an takhfiḍ? · ḥasanan, ākhudhuhu",
                "بكم هذه الحقيبة؟ خمسون. غالي قليلاً — هل يمكن أن تخفض؟ خمسة وأربعون. حسناً، آخذها. The "
                "object agrees: آخذها for a feminine noun, آخذه for a masculine one.",
                [X("هذا غالي قليلاً.", "hādhā ghālī qalīlan.", "This is a little expensive."),
                 X("هل يمكن أن تخفض السعر؟", "hal yumkin an takhfiḍ al-siʿr?", "Can you lower the price?"),
                 X("حسناً، آخذها بهذا السعر.", "ḥasanan, ākhudhuhā bi-hādhā al-siʿr.", "All right, I'll take it at this price.")],
                [("أريد أن تخفض أنت السعر.", "هل يمكن أن تخفض السعر؟", "هل يمكن أن… is the polite request frame; أريد أن + another subject sounds like a demand."),
                 ("حسناً، آخذ الرخيص.", "حسناً، آخذها بسعر أقلّ.", "رخيص describes an object, not the price you negotiated.")]),
              [D("زبونة", "بكم هذه الحقيبة؟", "bikam hādhihi al-ḥaqība?", "How much is this bag?"),
               D("بائع", "خمسون جنيهاً.", "khamsūn junayhan.", "Fifty pounds."),
               D("زبونة", "غالي قليلاً — هل يمكن أن تخفض؟", "ghālī qalīlan — hal yumkin an takhfiḍ?", "A little expensive — can you lower it?"),
               D("بائع", "خمسة وأربعون، وهذا آخر سعر.", "khamsa wa-arbaʿūn, wa-hādhā ākhir siʿr.", "Forty-five, and that is the last price.")],
              WS("Price worksheet", [
                  T("Bargain politely.", ["it is expensive → (soften)", "ask for a lower price", "accept"],
                    ["غالي قليلاً", "هل يمكن أن تخفض السعر؟", "حسناً، آخذه"]),
                  T("Answer as the seller.", ["بكم؟ (50)", "هل يمكن أن تخفض؟ (45, last price)"],
                    ["خمسون جنيهاً", "خمسة وأربعون، وهذا آخر سعر"]),
              ])),
        ]},
        {"id": "A1+-U3", "title": "Days, times, plans", "lessons": [
            L("The days of the week",
              "The Arabic week runs from السبت. Across the region the same names mostly hold, and Friday "
              "is the day everyone knows by name.",
              [V("السبت", "al-sabt", "Saturday", "noun"),
               V("الأحد", "al-aḥad", "Sunday", "noun"),
               V("الاثنين", "al-ithnayn", "Monday", "noun"),
               V("الجمعة", "al-jumʿa", "Friday", "noun"),
               V("الأسبوع", "al-usbūʿ", "the week", "noun")],
              G("Days are adverbial",
                "yawm + day · min + day ilā + day",
                "متى الاجتماع؟ يوم الاثنين. The day name needs no preposition: الأحد أعمل. In a range: "
                "من السبت إلى الأربعاء.",
                [X("متى الاجتماع؟ يوم الاثنين.", "matā al-ijtimāʿ? yawm al-ithnayn.", "When is the meeting? Monday."),
                 X("أعمل من السبت إلى الأربعاء.", "aʿmal min al-sabt ilā al-arbiʿāʾ.", "I work from Saturday to Wednesday."),
                 X("يوم الجمعة عطلة هنا.", "yawm al-jumʿa ʿuṭla hunā.", "Friday is a holiday here.")],
                [("في يوم السبب أعمل.", "يوم السبت أعمل.", "The day is السبت; السبب means 'reason'."),
                 ("أعمل في السبت.", "أعمل يوم السبت.", "Days are adverbial; في + a bare day sounds foreign.")]),
              [D("صديق", "متى درسك الجديد؟", "matā darsuk al-jadīd?", "When is your new class?"),
               D("طالب", "يوم الأحد والاثنين، من التاسعة إلى الحادية عشرة.", "yawm al-aḥad wa-l-ithnayn, min al-tāsiʿa ilā al-ḥādiya ʿashra.", "Sunday and Monday, from nine to eleven."),
               D("صديق", "وفي الجمعة؟", "wa-fī al-jumʿa?", "And on Friday?"),
               D("طالب", "الجمعة عطلة، أرتاح مع العائلة.", "al-jumʿa ʿuṭla, artāḥ maʿa al-ʿāʾila.", "Friday is a holiday — I rest with the family.")],
              WS("Days worksheet", [
                  T("Answer in Arabic.", ["when is the class? (Sunday)", "which day is a holiday?", "from Saturday to Wednesday"],
                    ["يوم الأحد", "يوم الجمعة", "من السبت إلى الأربعاء"]),
                  T("Plan your week.", ["a working day", "a rest day", "the busiest day"],
                    ["أعمل يوم…", "أرتاح يوم…", "أكثر يوم مشغول هو…"]),
              ])),
            L("Telling the time",
              "الساعة + ordinal hour, then صباحاً or مساءً. Half past is والنصف, quarter past والربع.",
              [V("الساعة", "al-sāʿa", "the hour; o'clock", "noun"),
               V("صباحاً", "ṣabāḥan", "in the morning", "adverb"),
               V("مساءً", "masāʾan", "in the evening", "adverb"),
               V("والنصف", "wa-l-niṣf", "and a half", "phrase"),
               V("متى", "matā", "when", "interrogative")],
              G("Clock frames",
                "al-sāʿa + ordinal · + wa-l-niṣf / wa-l-rubʿ · ṣabāḥan / masāʾan",
                "الساعة الثامنة صباحاً. الساعة السابعة والنصف مساءً. متى نلتقي؟ — الساعة الخامسة، إذاً.",
                [X("الاجتماع الساعة التاسعة صباحاً.", "al-ijtimāʿ al-sāʿa al-tāsiʿa ṣabāḥan.", "The meeting is at nine in the morning."),
                 X("سأصل الساعة السابعة والنصف.", "sa-aṣil al-sāʿa al-sābiʿa wa-l-niṣf.", "I will arrive at half past seven."),
                 X("متى نلتقي غداً؟", "matā naltqī ghadan?", "When shall we meet tomorrow?")],
                [("الساعة ثمان صباحاً.", "الساعة الثامنة صباحاً.", "The hour is ordinal: الثامنة."),
                 ("في الساعة السابعة في المساء.", "الساعة السابعة مساءً.", "مساءً is an adverbial accusative; في + مساء is a calque.")]),
              [D("مريم", "متى موعد الطبيب؟", "matā mawʿid al-ṭabīb?", "When is the doctor's appointment?"),
               D("حسن", "الساعة الرابعة والنصف بعد الظهر.", "al-sāʿa al-rābiʿa wa-l-niṣf baʿda al-ẓuhr.", "At half past four in the afternoon."),
               D("مريم", "وهل العيادة قريبة؟", "wa-hal al-ʿiyāda qarība?", "And is the clinic close?"),
               D("حسن", "نعم، عشر دقائق بالسيارة.", "naʿam, ʿashr daqāʾiq bi-l-sayyāra.", "Yes, ten minutes by car.")],
              WS("Clock worksheet", [
                  T("Say the time in Arabic.", ["9:00 a.m.", "7:30 p.m.", "4:15"],
                    ["الساعة التاسعة صباحاً", "الساعة السابعة والنصف مساءً", "الساعة الرابعة والربع"]),
                  T("Answer the question.", ["متى نلتقي؟ (5:00)", "متى يفتح المتحف؟ (9:00)"],
                    ["الساعة الخامسة", "الساعة التاسعة صباحاً"]),
              ])),
            L("Making a plan, refusing one kindly",
              "عندي موعد is the reason, للأسف does the softening, and المرة القادمة keeps the door open. "
              "Arabic almost never refuses without offering another time.",
              [V("موعد", "mawʿid", "appointment", "noun"),
               V("مشغول", "mashghūl", "busy", "adjective"),
               V("للأسف", "li-l-asaf", "unfortunately", "phrase"),
               V("المرة القادمة", "al-marra al-qādima", "next time", "phrase"),
               V("أوافق", "uwāfiq", "I agree", "verb")],
              G("Making and refusing",
                "hal yumkin an…? · ʿindī mawʿid · li-l-asaf, al-marra al-qādima",
                "هل يمكن أن نلتقي الجمعة؟ للأسف، عندي موعد — هل يمكن يوم الأحد؟ The whole negotiation is "
                "three moves: propose, decline with a reason, propose again.",
                [X("هل يمكن أن نتقابل غداً؟", "hal yumkin an nataqābal ghadan?", "Can we meet tomorrow?"),
                 X("للأسف، أنا مشغول صباحاً.", "li-l-asaf, anā mashghūl ṣabāḥan.", "Unfortunately I am busy in the morning."),
                 X("إذاً، المرة القادمة إن شاء الله.", "idhan, al-marra al-qādima in shāʾa Allāh.", "Then next time, God willing.")],
                [("للأسف، لا.", "للأسف، عندي موعد. هل يمكن يوم آخر؟", "A bare no closes the conversation; Arabic declines with a reason and an alternative."),
                 ("أنا مشغول في صباح.", "أنا مشغول صباحاً.", "Time adverbs of this type take the accusative: صباحاً.")]),
              [D("زميل", "هل يمكن أن نناقش التقرير غداً؟", "hal yumkin an tunāqish al-taqrīr ghadan?", "Can we discuss the report tomorrow?"),
               D("زميلة", "للأسف، عندي موعد صباحاً. هل يمكن بعد الظهر؟", "li-l-asaf, ʿindī mawʿid ṣabāḥan. hal yumkin baʿda al-ẓuhr?", "Unfortunately I have an appointment in the morning. Can we do the afternoon?"),
               D("زميل", "بكل سرور، الرابعة؟", "bi-kull surūr, al-rābiʿa?", "With pleasure — four o'clock?"),
               D("زميلة", "أوافق، أراك في المكتب.", "uwāfiq, arāk fī al-maktab.", "Agreed, I'll see you at the office.")],
              WS("Plan worksheet", [
                  T("Propose and refuse.", ["propose Friday", "refuse (appointment)", "offer Sunday"],
                    ["هل يمكن أن نلتقي الجمعة؟", "للأسف، عندي موعد", "هل يمكن يوم الأحد؟"]),
                  T("Close the exchange.", ["accept politely", "keep the door open"],
                    ["بكل سرور", "المرة القادمة إن شاء الله"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Getting around an Arab city runs on landmarks rather than street names: the pharmacy, "
                 "the mosque, the bakery. A direction that names a landmark is understood by everyone, "
                 "and a visitor who learns ten landmarks stops being a tourist. In many cities taxis are "
                 "shared, so a driver may pick up another passenger mid-route — it is normal, not a detour."),
        source_url="https://en.wikipedia.org/wiki/Arab_culture",
        reading=("أريد الذهاب إلى المتحف. من فضلك، هل هو بعيد؟ اركب الحافلة رقم خمسة وعشرين، ثمّ انعطف "
                 "يميناً عند الصيدلية. الأجرة عشرة جنيهات. المتحف مقابل الحديقة الكبيرة، ويفتح الساعة "
                 "التاسعة صباحاً."),
        reading_gloss=("I want to go to the museum. Please, is it far? Take bus number twenty-five, then "
                       "turn right at the pharmacy. The fare is ten pounds. The museum is opposite the "
                       "big park, and it opens at nine in the morning."),
        listening=("أ: بكم التذكرة إلى المنصورة؟<br>ب: خمسة وأربعون جنيهاً.<br>أ: ومتى يتحرّك القطار؟<br>"
                   "ب: الساعة السابعة والنصف مساءً، من المحطة الثانية."),
        listening_gloss=("A: How much is the ticket to Mansoura? B: Forty-five pounds. A: And when does "
                         "the train leave? B: At half past seven in the evening, from platform two."),
        voice_tag=VOICE,
        idioms=[
            ("على الطريق", "on the road", "on the way, en route"),
            ("من هنا وهناك", "from here and there", "this way and that"),
            ("قاب قوسين", "at two bow-lengths", "very near, within reach"),
            ("على بعد خطوات", "a few steps away", "just around the corner"),
            ("وراء الكواليس", "behind the scenes", "out of sight of the public"),
            ("من أول نظرة", "from the first glance", "at first sight"),
            ("على قدم وساق", "on foot and leg", "at full pace"),
            ("خطوة بخطوة", "step by step", "gradually, patiently"),
            ("آخر محطة", "the last station", "the final stop, the end of the line"),
            ("على اليمين", "on the right", "to the right; on the right-hand side"),
        ],
        mistakes=[
            ("أين هو يقع البنك؟", "أين يقع البنك؟", "أين and يقع both ask the place; keep one."),
            ("المقهى بجانب من الجامعة.", "المقهى بجانب الجامعة.", "بجانب takes a direct genitive, without من."),
            ("الساعة سبعة في المساء.", "الساعة السابعة مساءً.", "Ordinal hour, adverbial مساءً; no في."),
        ],
        task_title="Direct me across your city",
        task_instructions=("Pick a route you take often: home to work, or to the market. Write six Arabic "
                           "steps with at least three landmarks and one transport line, then read it to a "
                           "partner who must draw the route without asking a question. If they get lost, "
                           "the missing word was probably a relation (أمام، بجانب، مقابل) — fix it and "
                           "try again."),
    ),
    "test": [
        ("translate_en", "Say: Where is the pharmacy, please?", "أين الصيدلية من فضلك؟"),
        ("translate_ar", "سِرْ مستقيماً ثمّ انعطف شمالاً.", "Go straight, then turn left."),
        ("multiple_choice", "Which is the polite request?", "انعطف يميناً من فضلك"),
        ("fill_in_the_blank", "أريد تذكرة ___ أسوان. (to)", "إلى"),
        ("word_selection", "Select the Arabic for eighty.", "ثمانون"),
        ("error_correction", "المقهى بجانب من الجامعة.", "المقهى بجانب الجامعة."),
        ("dialogue_completion", "Complete: بكم التذكرة؟ — ___ (forty pounds)", "أربعون جنيهاً"),
        ("matching", "Match مقابل to its meaning.", "opposite"),
        ("reading_comprehension", "يفتح المتحف الساعة التاسعة صباحاً. When does it open?", "at nine in the morning"),
        ("inference", "«غالي قليلاً — هل يمكن أن تخفض؟» What is the speaker doing?", "bargaining, politely"),
        ("main_idea", "اركب الحافلة رقم خمسة وعشرين من المحطة. What is this about?", "which bus to take"),
        ("detail_identification", "الاجتماع الساعة التاسعة صباحاً. When is the meeting?", "nine in the morning"),
    ],
}

HALFSTEPS["A2+"] = {
    "title": "Arabic A2+ — Holding a chat",
    "native": NATIVE,
    "goals": [
        "React, follow up and keep a conversation alive",
        "Tell a short story in order, with a scene and an ending",
        "Invite, accept, decline — on the phone and in person",
    ],
    "units": [
        {"id": "A2+-U1", "title": "Keeping the talk going", "lessons": [
            L("Reactions that mean something",
              "Arabic conversation is fed by reactions: حقاً؟ (really?), طبعاً (of course), مستحيل (no "
              "way), عجيب (strange). They buy time and, more importantly, they hand the floor back.",
              [V("حقاً؟", "ḥaqqan?", "really?", "interrogative"),
               V("طبعاً", "ṭabʿan", "of course", "adverb"),
               V("مستحيل", "mustaḥīl", "impossible; no way", "adjective"),
               V("عجيب", "ʿajīb", "strange, amazing", "adjective"),
               V("بالفعل", "bi-l-fiʿl", "indeed, actually", "phrase")],
              G("React, then ask",
                "reaction + wa- + follow-up question",
                "حقاً؟ وماذا حدث بعد ذلك؟ A reaction alone can end a turn; adding و + a question gives "
                "the floor back. طبعاً agrees, مستحيل refuses to believe — check which one the moment needs.",
                [X("حقاً؟ لم أعرف ذلك.", "ḥaqqan? lam aʿrif dhālika.", "Really? I did not know that."),
                 X("طبعاً، هذا واضح.", "ṭabʿan, hādhā wāḍiḥ.", "Of course, that is clear."),
                 X("مستحيل! كم كان السعر؟", "mustaḥīl! kam kāna al-siʿr?", "No way! How much was the price?")],
                [("حقاً أنا لا أعرف.", "حقاً؟ لا أعرف.", "As a reaction, حقاً stands alone and takes a question mark."),
                 ("طبعاً لا، نعم.", "طبعاً.", "Contradicting yourself inside one reaction kills the signal.")]),
              [D("سميرة", "اشتريتُ البيت أخيراً.", "ishtaraytu al-bayt akhīran.", "I finally bought the house."),
               D("خالد", "حقاً؟ مبروك! وماذا حدث مع البنك؟", "ḥaqqan? mabrūk! wa-mādhā ḥadatha maʿa al-bank?", "Really? Congratulations! And what happened with the bank?"),
               D("سميرة", "وافقوا أخيراً بعد شهرين.", "wāfaqū akhīran baʿda shahrayn.", "They finally agreed after two months."),
               D("خالد", "مستحيل! شهران كاملان! الحمد لله على كل حال.", "mustaḥīl! shahrān kāmilān! al-ḥamdu li-llāh ʿalā kull ḥāl.", "No way! Two whole months! Thank God for everything.")],
              WS("Reaction worksheet", [
                  T("React in Arabic.", ["good news", "something unbelievable", "something obvious"],
                    ["حقاً؟ مبروك!", "مستحيل!", "طبعاً، هذا واضح"]),
                  T("React and follow up.", ["«سافرت إلى اليابان»", "«تغيّر عملي»"],
                    ["حقاً؟ وماذا فعلتَ هناك؟", "عجيب! وكيف كان ذلك؟"]),
              ])),
            L("Following up: وبعد ذلك؟",
              "A conversation dies when nobody asks the next question. وماذا حدث؟، ماذا بعد؟، ولماذا؟ "
              "keep the partner talking, and كيف كان ذلك؟ asks for the feeling, not the fact.",
              [V("ماذا حدث؟", "mādhā ḥadatha?", "what happened?", "phrase"),
               V("وبعد ذلك؟", "wa-baʿda dhālika?", "and after that?", "phrase"),
               V("لماذا؟", "limādhā?", "why?", "interrogative"),
               V("كيف كان؟", "kayfa kāna?", "how was it?", "phrase"),
               V("أخبرني أكثر", "akhbirnī akthar", "tell me more", "phrase")],
              G("Follow-up ladder",
                "mādhā ḥadatha? → wa-baʿda dhālika? → wa-kayfa kāna?",
                "Each question aims a step deeper: the event, the next event, then the evaluation. "
                "أخبرني أكثر is the shortest way to say 'I am listening'.",
                [X("وماذا حدث بعد المقابلة؟", "wa-mādhā ḥadatha baʿda al-muqābala?", "And what happened after the interview?"),
                 X("كيف كان شعورك؟", "kayfa kāna shuʿūruk?", "How did you feel?"),
                 X("أخبرني أكثر، الموضوع مهم.", "akhbirnī akthar, al-mawḍūʿ muhimm.", "Tell me more — this matters.")],
                [("ماذا حدث أنت؟", "ماذا حدث لك؟", "The verb حدث takes لـ for the person affected."),
                 ("وبعد ذلك؟ ثمّ ماذا؟ وبعد؟", "(one follow-up at a time)", "Three follow-ups in a row turn interest into an interrogation.")]),
              [D("ليلى", "وصلتُ متأخرة إلى المطار أمس.", "waṣaltu mutaʾakhkhira ilā al-maṭār ams.", "I arrived late at the airport yesterday."),
               D("عمر", "وماذا حدث بعد ذلك؟", "wa-mādhā ḥadatha baʿda dhālika?", "And what happened after that?"),
               D("ليلى", "ألغوا الرحلة، فنمتُ في الفندق.", "alghaw al-riḥla, fa-nimtu fī al-funduq.", "They cancelled the flight, so I slept in the hotel."),
               D("عمر", "كيف كان شعورك؟", "kayfa kāna shuʿūruk?", "How did you feel?")],
              WS("Follow-up worksheet", [
                  T("Ask the next question.", ["«تعرّفتُ على مدير الشركة»", "«انتقلتُ إلى مدينة جديدة»"],
                    ["وماذا قال لك؟", "وكيف كانت المدينة؟"]),
                  T("Show interest.", ["(it was hard)", "(tell me more)"],
                    ["كم هذا صعب!", "أخبرني أكثر"]),
              ])),
            L("Showing interest: ما شاء الله، يا للعجب",
              "Praise and wonder carry conversations: ما شاء الله، كم هذا جميل، يا للعجب، الله يعطيك "
              "العافية. They are formulaic by design — the formula is the politeness.",
              [V("ما شاء الله", "mā shāʾa Allāh", "what God has willed", "phrase"),
               V("كم هذا جميل", "kam hādhā jamīl", "how beautiful this is", "phrase"),
               V("يا للعجب", "yā li-l-ʿajab", "how strange!", "phrase"),
               V("الله يعطيك العافية", "Allāh yuʿṭīk al-ʿāfiya", "may God give you health", "phrase"),
               V("ما أحلى", "mā aḥlā", "how sweet, how delightful", "phrase")],
              G("Exclamations",
                "mā shāʾa Allāh · kam hādhā + adjective · yā li-l- + noun",
                "ما شاء الله، عمل ممتاز! كم هذا جميل! يا للعجب، ما توقّعت ذلك. The formula does the "
                "social work; the words after it make it specific.",
                [X("ما شاء الله، بيتك جميل جداً.", "mā shāʾa Allāh, baytuk jamīl jiddan.", "What God wills — your house is very beautiful."),
                 X("كم هذا الطعام لذيذ!", "kam hādhā al-ṭaʿām ladhīdh!", "How delicious this food is!"),
                 X("الله يعطيك العافية، تعبتَ من أجلي.", "Allāh yuʿṭīk al-ʿāfiya, taʿibta min ajlī.", "May God give you health — you tired yourself for me.")],
                [("ما شاء الله، لكن البيت قديم.", "ما شاء الله، البيت جميل.", "ما شاء الله is praise; balancing it with a criticism in the same breath breaks the formula."),
                 ("كم الجميل هذا!", "كم هذا جميل!", "كم + demonstrative + adjective is the fixed order.")]),
              [D("نادية", "هذا ابني، نجح في الامتحان.", "hādhā ibnī, najaḥa fī al-imtiḥān.", "This is my son — he passed the exam."),
               D("سعاد", "ما شاء الله! كم هذا خبر جميل!", "mā shāʾa Allāh! kam hādhā khabar jamīl!", "What God wills! What lovely news!"),
               D("نادية", "شكراً، تعب كثيراً هذا العام.", "shukran, taʿiba kathīran hādhā al-ʿām.", "Thank you — he worked hard this year."),
               D("سعاد", "الله يعطيه العافية، ويوفّقه دائماً.", "Allāh yuʿṭīhi al-ʿāfiya, wa-yuwaffiqhu dāʾiman.", "May God give him health and always grant him success.")],
              WS("Interest worksheet", [
                  T("React warmly.", ["«رسمتُ هذه اللوحة»", "«وصلت رسالة القبول»"],
                    ["ما شاء الله، كم هذا جميل!", "ما شاء الله، مبروك!"]),
                  T("Thank someone's effort.", ["(they helped you move house)", "(they waited for you)"],
                    ["الله يعطيك العافية", "شكراً لصبرك، الله يعطيك العافية"]),
              ])),
        ]},
        {"id": "A2+-U2", "title": "Telling a short story", "lessons": [
            L("In order: أولاً، ثمّ، بعد ذلك، أخيراً",
              "Four connectors turn four sentences into a story: أولاً، ثمّ، بعد ذلك، أخيراً. Arabic "
              "also uses فـ for the immediate next step and ثمّ for the deliberate one.",
              [V("أولاً", "awwalan", "first", "adverb"),
               V("ثمّ", "thumma", "then (in sequence)", "conjunction"),
               V("بعد ذلك", "baʿda dhālika", "after that", "phrase"),
               V("أخيراً", "akhīran", "finally", "adverb"),
               V("فجأة", "fajʾatan", "suddenly", "adverb")],
              G("Story order",
                "awwalan…, thumma…, baʿda dhālika…, wa-akhīran…",
                "أولاً وصلنا إلى المطار. ثمّ انتظرنا ساعتين. وبعد ذلك أقلعت الطائرة. وأخيراً وصلنا في "
                "الليل. One connector per step, one step per sentence.",
                [X("أولاً، لم أكن أعرف أحداً.", "awwalan, lam akun aʿrifu aḥadan.", "At first I did not know anyone."),
                 X("ثمّ تعرّفتُ على سارة.", "thumma taʿarrafftu ʿalā Sāra.", "Then I met Sara."),
                 X("وأخيراً، صرنا أصدقاء.", "wa-akhīran, ṣirnā aṣdiqāʾ.", "And finally we became friends.")],
                [("أولاً ثمّ بعد ذلك أخيراً حدث كل شيء.", "(one connector per step)", "All four connectors in one sentence is a list, not a story."),
                 ("ثمّ وصلتُ، وبعد ذلك وصلتُ أيضاً.", "(each connector carries a new event)", "Repeating the same event under two connectors stalls the story.")]),
              [D("ريم", "كيف كانت رحلتك؟", "kayfa kānat riḥlatuk?", "How was your trip?"),
               D("ماجد", "أولاً وصلنا إلى المطار متأخرين. ثمّ انتظرنا ثلاث ساعات.", "awwalan waṣalnā ilā al-maṭār mutaʾakhkhirīn. thumma intaẓarnā thalāth sāʿāt.", "First we arrived at the airport late. Then we waited three hours."),
               D("ريم", "وبعد ذلك؟", "wa-baʿda dhālika?", "And after that?"),
               D("ماجد", "وبعد ذلك أُلغيت الرحلة، وأخيراً سافرنا في اليوم التالي.", "wa-baʿda dhālika ulghiyat al-riḥla, wa-akhīran sāfarnā fī al-yawm al-tālī.", "After that the flight was cancelled, and finally we travelled the next day.")],
              WS("Order worksheet", [
                  T("Put the story in order.", ["وصلنا / استقبلنا الغرفة / سافرنا / حجزنا الفندق"],
                    ["أولاً سافرنا", "ثمّ وصلنا", "بعد ذلك حجزنا الفندق", "وأخيراً استقبلنا الغرفة"]),
                  T("Tell your own morning.", ["first", "then", "finally"],
                    ["أولاً…", "ثمّ…", "وأخيراً…"]),
              ])),
            L("Scene and event: كان… وفجأةً",
              "كان opens a scene, بينما holds a background action, and فجأةً punctuates it. كان الوقت "
              "متأخراً وفجأةً سمعنا صوتاً — the scene sits inside كان, the event steps out of فجأة.",
              [V("كان", "kāna", "was (scene-setter)", "verb"),
               V("فجأةً", "fajʾatan", "suddenly", "adverb"),
               V("بينما", "baynamā", "while", "conjunction"),
               V("سمعنا", "samiʿnā", "we heard", "verb"),
               V("كان الوقت", "kāna al-waqt", "the time was", "phrase")],
              G("Scene then event",
                "kāna + scene · baynamā + ongoing action · wa-fajʾatan + perfect verb",
                "كان الوقت متأخراً، وكانت السماء تمطر، بينما كنّا ننتظر، وفجأةً جاءت سيارة أجرة. The "
                "scene can hold two كان clauses; the event is one perfect verb.",
                [X("كان الطريق مزدحماً وفجأةً توقف كل شيء.", "kāna al-ṭarīq muzdaḥiman wa-fajʾatan tawaqqafa kull shayʾ.", "The road was crowded and suddenly everything stopped."),
                 X("بينما كنّا نتكلّم، رنّ الهاتف.", "baynamā kunnā natakallam, ranna al-hātif.", "While we were talking, the phone rang."),
                 X("كان الجوّ جميلاً ذلك المساء.", "kāna al-jaww jamīlan dhālika al-masāʾ.", "The weather was beautiful that evening.")],
                [("كان الطريق مزدحم وفجأةً.", "كان الطريق مزدحماً، وفجأةً توقف كل شيء.", "فجأة needs an event after it, and كان's predicate takes the accusative."),
                 ("بينما تكلّمنا، رنّ الهاتف.", "بينما كنّا نتكلّم، رنّ الهاتف.", "بينما wants an ongoing action, usually with كان.")]),
              [D("سلمى", "ماذا حدث في الحفلة؟", "mādhā ḥadatha fī al-ḥafla?", "What happened at the party?"),
               D("يوسف", "كان الجميع يرقص، وفجأةً انقطعت الكهرباء.", "kāna al-jamīʿ yarquṣ, wa-fajʾatan inqaṭaʿat al-kahrabāʾ.", "Everyone was dancing, and suddenly the electricity cut out."),
               D("سلمى", "ماذا فعلتم؟", "mādhā faʿaltum?", "What did you do?"),
               D("يوسف", "بينما كنّا نبحث عن الشموع، عادت الكهرباء، وصفّق الجميع.", "baynamā kunnā nabḥath ʿan al-shumūʿ, ʿādat al-kahrabāʾ, wa-ṣaffaqa al-jamīʿ.", "While we were looking for candles, the power came back and everyone clapped.")],
              WS("Scene worksheet", [
                  T("Set the scene with كان.", ["it was late", "we were waiting", "the weather was cold"],
                    ["كان الوقت متأخراً", "كنّا ننتظر", "كان الجوّ بارداً"]),
                  T("Add the turn with فجأةً.", ["(a car stopped)", "(someone knocked)", "(the rain began)"],
                    ["وفجأةً توقفت سيارة", "وفجأةً طرق أحدهم الباب", "وفجأةً بدأ المطر"]),
              ])),
            L("The end: في النهاية، تبيّن أنّ",
              "An Arabic anecdote closes with a verdict: في النهاية، تبيّن أنّ، والحمد لله، وما زلت أذكر. "
              "It is the same move as an English punchline, with more gratitude.",
              [V("في النهاية", "fī al-nihāya", "in the end", "phrase"),
               V("تبيّن أنّ", "tabayyana anna", "it turned out that", "phrase"),
               V("والحمد لله", "wa-l-ḥamdu li-llāh", "and praise be to God", "phrase"),
               V("الذكرى", "al-dhikrā", "the memory", "noun"),
               V("تعلّمتُ أنّ", "taʿallamtu anna", "I learned that", "phrase")],
              G("Closing moves",
                "fī al-nihāya… · tabayyana anna… · wa-l-ḥamdu li-llāh · taʿallamtu anna…",
                "في النهاية تبيّن أنّ التأخير كان نعمة. والحمد لله، وصلنا بسلام. The close is also how a "
                "story becomes advice — the listener gets a moral without being lectured.",
                [X("في النهاية، تبيّن أنّه كان محقاً.", "fī al-nihāya, tabayyana annahu kāna muḥiqqan.", "In the end it turned out he was right."),
                 X("تعلّمتُ أنّ الصبر مهم.", "taʿallamtu anna al-ṣabra muhimm.", "I learned that patience matters."),
                 X("والحمد لله، كل شيء انتهى بخير.", "wa-l-ḥamdu li-llāh, kull shayʾ intahā bi-khayr.", "Praise God, everything ended well.")],
                [("تبيّن أنّ كان محقاً.", "تبيّن أنّه كان محقاً.", "أنّ takes a pronoun suffix, not a bare كان."),
                 ("في النهاية، أخيراً، ثمّ انتهى.", "(one closing move)", "The end of a story is one move; three of them read as filler.")]),
              [D("فاطمة", "وكيف انتهى الأمر مع المحلّ؟", "wa-kayfa intahā al-amr maʿa al-maḥall?", "And how did it end with the shop?"),
               D("بلال", "في النهاية، تبيّن أنّ الخطأ كان في الفاتورة فقط.", "fī al-nihāya, tabayyana anna al-khaṭaʾ kāna fī al-fātūra faqaṭ.", "In the end it turned out the mistake was only in the invoice."),
               D("فاطمة", "إذاً ربحتَ الوقت والمال.", "idhan rabiḥta al-waqt wa-l-māl.", "Then you saved time and money."),
               D("بلال", "وتعلّمتُ أنّ الفحص قبل الدفع ضروري، والحمد لله.", "wa-taʿallamtu anna al-faḥṣ qabla al-dafʿ ḍarūrī, wa-l-ḥamdu li-llāh.", "And I learned that checking before paying is essential — praise God.")],
              WS("Ending worksheet", [
                  T("Close the story.", ["«تعبتُ كثيراً لكن نجحت»", "«ضاع المفتاح ثمّ وجدته»"],
                    ["في النهاية تبيّن أنّ التعب كان يستحقّ", "وفي النهاية، تبيّن أنّه كان في جيبي"]),
                  T("Turn it into a lesson.", ["check before you pay", "patience matters"],
                    ["تعلّمتُ أنّ الفحص قبل الدفع ضروري", "تعلّمتُ أنّ الصبر مهم"]),
              ])),
        ]},
        {"id": "A2+-U3", "title": "Invitations and the phone", "lessons": [
            L("Inviting: هل تحبّ أن…؟",
              "Three invitation frames cover almost everything: هل تحبّ أن…؟ (would you like to), ما "
              "رأيك أن…؟ (what do you think of), and ندعوك (we invite you). Each is softer than an "
              "imperative, and each takes أن + a verb.",
              [V("هل تحبّ أن", "hal tuḥibb an", "would you like to", "phrase"),
               V("ما رأيك أن", "mā raʾyuk an", "what do you think of", "phrase"),
               V("ندعوك", "nadʿūk", "we invite you", "verb"),
               V("على العشاء", "ʿalā al-ʿashāʾ", "to dinner", "phrase"),
               V("بمناسبة", "bi-munāsabat", "on the occasion of", "preposition")],
              G("Invitation frames",
                "hal tuḥibb an + subjunctive · mā raʾyuk an + subjunctive · nadʿūk ilā / ʿalā + noun",
                "هل تحبّ أن تتعشّى معنا؟ ما رأيك أن نزور المتحف؟ ندعوك على العشاء بمناسبة نجاحك.",
                [X("هل تحبّ أن تأتي غداً؟", "hal tuḥibb an taʾtiya ghadan?", "Would you like to come tomorrow?"),
                 X("ما رأيك أن نتقابل بعد العمل؟", "mā raʾyuk an nataqābal baʿda al-ʿamal?", "What do you think of meeting after work?"),
                 X("ندعوك على العشاء بمناسبة عيد ميلادك.", "nadʿūk ʿalā al-ʿashāʾ bi-munāsabat ʿīd mīlādik.", "We invite you to dinner for your birthday.")],
                [("هل تحبّ تأتي غداً؟", "هل تحبّ أن تأتي غداً؟", "The invitation frame needs أن before the verb."),
                 ("ندعوك في العشاء.", "ندعوك على العشاء.", "The invitation to a meal takes على.")]),
              [D("هند", "ما رأيك أن نتقابل على العشاء الجمعة؟", "mā raʾyuk an nataqābal ʿalā al-ʿashāʾ al-jumʿa?", "What do you think of meeting for dinner on Friday?"),
               D("سامي", "فكرة جميلة، الليلة عندي هدية أيضاً.", "fikra jamīla, al-layla ʿindī hadiyya aydan.", "Lovely idea — I also have a gift tonight."),
               D("هند", "هل تحبّ أن أدعو أخي؟", "hal tuḥibb an adʿuwa akhī?", "Would you like me to invite my brother?"),
               D("سامي", "بكل سرور، العشاء يكبر بالجماعة.", "bi-kull surūr, al-ʿashāʾ yakbur bi-l-jamāʿa.", "With pleasure — dinner grows with company.")],
              WS("Invitation worksheet", [
                  T("Invite in three ways.", ["to dinner", "to the museum", "to a birthday"],
                    ["هل تحبّ أن تتعشّى معنا؟", "ما رأيك أن نزور المتحف؟", "ندعوك على العشاء بمناسبة عيد ميلادك"]),
                  T("Extend the invitation.", ["a friend", "a family"],
                    ["هل تحبّ أن ننادي صديقك؟", "أدعو العائلة أيضاً"]),
              ])),
            L("Accepting and declining",
              "Yes is بكل سرور or يسعدني ذلك. No is للأسف، لا أستطيع — with a reason and an alternative. "
              "معذرة is 'excuse me', not 'no'.",
              [V("بكل سرور", "bi-kull surūr", "with great pleasure", "phrase"),
               V("يسعدني ذلك", "yusʿidunī dhālika", "that would please me", "phrase"),
               V("لا أستطيع", "lā astaṭīʿ", "I cannot", "verb"),
               V("معذرة", "maʿdhira", "excuse me", "noun"),
               V("أعدك", "aʿiduk", "I promise you", "verb")],
              G("Accept / decline + keep the door open",
                "bi-kull surūr · li-l-asaf, lā astaṭīʿ + reason · in shāʾa Allāh, al-marra al-qādima",
                "بكل سرور، متى؟ / للأسف لا أستطيع، عندي سفر — لكن أعدك بالمرة القادمة. The last clause is "
                "not padding; it is how the relationship is kept.",
                [X("بكل سرور، يسعدني ذلك.", "bi-kull surūr, yusʿidunī dhālika.", "With pleasure, that would please me."),
                 X("للأسف، لا أستطيع هذه المرة.", "li-l-asaf, lā astaṭīʿ hādhihi al-marra.", "Unfortunately I cannot this time."),
                 X("أعدك أن آتي في المرة القادمة.", "aʿiduk an ātiya fī al-marra al-qādima.", "I promise to come next time.")],
                [("للأسف، لا، معذرة، مستحيل.", "للأسف، لا أستطيع، عندي سفر.", "A four-word refusal with no reason closes the door."),
                 ("أستطيع لا.", "لا أستطيع.", "Negation comes before the verb: لا أستطيع.")]),
              [D("نور", "هل تحبّ أن تأتي إلى الشاطئ غداً؟", "hal tuḥibb an taʾtiya ilā al-shāṭiʾ ghadan?", "Would you like to come to the beach tomorrow?"),
               D("زياد", "بكل سرور! في أيّ ساعة؟", "bi-kull surūr! fī ayy sāʿa?", "With pleasure! At what time?"),
               D("نور", "العاشرة صباحاً، وسنبقى حتى المغرب.", "al-ʿāshira ṣabāḥan, wa-sana-bqā ḥattā al-maghrib.", "Ten in the morning, and we'll stay until sunset."),
               D("زياد", "يسعدني ذلك، لكن للأسف عندي درس — أعدك بالمرة القادمة.", "yusʿidunī dhālika, lākin li-l-asaf ʿindī dars — aʿiduk bi-l-marra al-qādima.", "That would please me, but unfortunately I have a class — I promise next time.")],
              WS("Answer worksheet", [
                  T("Accept and decline.", ["invitation to dinner (accept)", "invitation to travel (decline, reason)"],
                    ["بكل سرور، يسعدني ذلك", "للأسف لا أستطيع، عندي عمل"]),
                  T("Keep the door open.", ["(decline, offer another time)"],
                    ["أعدك أن آتي في المرة القادمة إن شاء الله"]),
              ])),
            L("On the phone: من المتحدث؟",
              "Phone Arabic has its own openers: الو، من المتحدث؟، لحظة من فضلك، سيصل الاتصال، الخطّ "
              "ضعيف. Digital messages keep the same politeness in writing.",
              [V("الو؟", "alū?", "hello (on the phone)", "interjection"),
               V("من المتحدث؟", "man al-mutakallim?", "who is speaking?", "phrase"),
               V("لحظة من فضلك", "laḥẓa min faḍlik", "one moment please", "phrase"),
               V("سأعاود الاتصال", "sa-uʿāwid al-ittiṣāl", "I will call again", "phrase"),
               V("الخطّ ضعيف", "al-khaṭṭ ḍaʿīf", "the line is weak", "phrase")],
              G("Phone frames",
                "alū? · man al-mutakallim? · laḥẓa min faḍlik · sa-uʿāwid al-ittiṣāl",
                "الو؟ أهلاً، من المتحدث؟ لحظة من فضلك، سأناديه. If the line breaks: الخطّ ضعيف، سأعاود "
                "الاتصال — the polite way to hang up first.",
                [X("الو؟ من المتحدث؟", "alū? man al-mutakallim?", "Hello? Who is speaking?"),
                 X("لحظة من فضلك، سأنادي أخي.", "laḥẓa min faḍlik, sa-unādī akhī.", "One moment please, I'll call my brother."),
                 X("الخطّ ضعيف، سأعاود الاتصال.", "al-khaṭṭ ḍaʿīf, sa-uʿāwid al-ittiṣāl.", "The line is weak — I'll call again.")],
                [("الو، من أنت المتحدث؟", "الو، من المتحدث؟", "من المتحدث is a fixed phrase; adding أنت breaks the frame."),
                 ("سأصل الاتصال.", "سأعاود الاتصال.", "The verb is عاود (to repeat), not وصل.")]),
              [D("سعيد", "الو؟ من المتحدث؟", "alū? man al-mutakallim?", "Hello? Who is speaking?"),
               D("زينب", "أنا زينب، هل يمكن أن أكلم سعيداً؟", "anā Zaynab, hal yumkin an ukallim Saʿīdan?", "It's Zaynab — may I speak to Saeed?"),
               D("سعيد", "أنا سعيد، لحظة من فضلك، الخطّ ضعيف قليلاً.", "anā Saʿīd, laḥẓa min faḍlik, al-khaṭṭ ḍaʿīf qalīlan.", "This is Saeed — one moment please, the line is a little weak."),
               D("زينب", "إذاً سأعاود الاتصال بعد قليل.", "idhan sa-uʿāwid al-ittiṣāl baʿda qalīl.", "Then I'll call again shortly.")],
              WS("Phone worksheet", [
                  T("Open the call in Arabic.", ["answer the phone", "ask who is speaking", "ask for a moment"],
                    ["الو؟", "من المتحدث؟", "لحظة من فضلك"]),
                  T("Handle a bad line.", ["the line is weak", "call again", "say goodbye"],
                    ["الخطّ ضعيف", "سأعاود الاتصال", "مع السلامة"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Arabic conversation rewards the listener. A reaction like ما شاء الله or الله يعطيك "
                 "العافية is expected at the right moment, and a story is judged by how the teller closes "
                 "it — usually with a lesson and a thanks. Silence between turns is shorter than in "
                 "English conversation: the reply, not the pause, is what holds the floor."),
        source_url="https://en.wikipedia.org/wiki/Etiquette_in_the_Middle_East",
        reading=("قابلتُ صديقي القديم في السوق أمس. أولاً، لم أعرفه لأنّه تغيّر كثيراً. ثمّ سمعتُ صوته، "
                 "وقفزتُ من مكاني. كان يحمل هدية لابنه، بينما كنت أبحث عن كتاب. وفجأةً قال: «كيف حالك "
                 "يا رجل؟» في النهاية جلسنا ساعة، وتعلّمتُ أنّ الصداقة لا تحتاج موعداً."),
        reading_gloss=("I met my old friend in the market yesterday. At first I did not recognise him "
                       "because he had changed a lot. Then I heard his voice and jumped from my place. "
                       "He was carrying a gift for his son while I was looking for a book. Suddenly he "
                       "said, 'How are you, man?' In the end we sat for an hour, and I learned that "
                       "friendship needs no appointment."),
        listening=("أ: الو؟ من المتحدث؟<br>ب: أنا طارق. هل تحبّ أن تتعشّى معنا الليلة؟<br>"
                   "أ: بكل سرور! لكن للأسف عندي موعد حتى الثامنة.<br>ب: لا مشكلة، نتقابل في الساعة التاسعة."),
        listening_gloss=("A: Hello, who is speaking? B: It's Tariq. Would you like to have dinner with us "
                         "tonight? A: With pleasure! But unfortunately I have an appointment until eight. "
                         "B: No problem — we'll meet at nine."),
        voice_tag=VOICE,
        idioms=[
            ("على فكرة", "on the thought", "by the way"),
            ("والله؟", "by God?", "really? (spoken emphasis)"),
            ("يا رجل", "O man", "a warm address in conversation"),
            ("ما في مشكلة", "there is no problem", "no problem (spoken)"),
            ("على الرحب والسعة", "with welcome and room", "you are most welcome"),
            ("كلام كبير", "big talk", "words that promise more than they can keep"),
            ("حكاية طويلة", "a long tale", "it is a long story"),
            ("من باب الحديث", "from the door of conversation", "just to make conversation"),
            ("خلّيها على الله", "leave it to God", "let it go; trust it will work out"),
            ("على راحتك", "at your ease", "take your time, no rush"),
        ],
        mistakes=[
            ("هل تحبّ تأتي؟", "هل تحبّ أن تأتي؟", "The invitation frame needs أن + subjunctive."),
            ("أنت من المتحدث؟", "من المتحدث؟", "Fixed phone phrase, without أنت."),
            ("كان يحمل، بينما كنت أبحث، ثمّ فجأة، وفي النهاية…", "(one scene marker per sentence)", "Arabic storytelling uses one marker at a time; a chain of markers is a list, not a story."),
        ],
        task_title="Tell me a two-minute story",
        task_instructions=("Record yourself telling a real story in Arabic for two minutes: أولاً for the "
                           "scene, كان for the background, فجأةً for the turn, and one closing move "
                           "(في النهاية تبيّن أنّ…). Then listen back and count the reactions you left "
                           "out — every 'حقاً؟' your listener needed is a place your story ran without them."),
    ),
    "test": [
        ("translate_en", "Say: Really? And what happened after that?", "حقاً؟ وماذا حدث بعد ذلك؟"),
        ("translate_ar", "كيف كان شعورك؟", "How did you feel?"),
        ("multiple_choice", "Which invitation is the softest?", "ما رأيك أن نتقابل بعد العمل؟"),
        ("fill_in_the_blank", "هل تحبّ ___ تتعشّى معنا؟ (to)", "أن"),
        ("word_selection", "Select the Arabic for 'suddenly'.", "فجأةً"),
        ("error_correction", "كان الطريق مزدحم وفجأةً.", "كان الطريق مزدحماً، وفجأةً توقف كل شيء."),
        ("dialogue_completion", "Complete: للأسف، لا أستطيع — ___ (next time, I promise)", "أعدك بالمرة القادمة"),
        ("matching", "Match تبيّن أنّ to its meaning.", "it turned out that"),
        ("reading_comprehension", "أولاً لم أعرفه، ثمّ سمعتُ صوته. What changed?", "he recognised him by his voice"),
        ("inference", "«في النهاية جلسنا ساعة» — what does the teller think of friendship?", "it needs no appointment"),
        ("main_idea", "كان يحمل هدية لابنه بينما كنت أبحث عن كتاب. What is the contrast?", "a gift and a book, two errands"),
        ("detail_identification", "نحن نتقابل في الساعة التاسعة. When do they meet?", "at nine"),
    ],
}

HALFSTEPS["B1+"] = {
    "title": "Arabic B1+ — Comfortable",
    "native": NATIVE,
    "goals": [
        "Make and answer requests at work without sounding curt",
        "Announce a delay, apologise properly and reschedule",
        "Argue a point and concede a part of it without losing the room",
    ],
    "units": [
        {"id": "B1+-U1", "title": "Work requests", "lessons": [
            L("Asking a colleague to do something",
              "At work the request frame matters more than the verb: هل يمكن أن…؟، أرجو أن…، تكرّم بـ… "
              "all ask; أرسل لي orders. The difference is the whole relationship.",
              [V("أرجو أن", "arjū an", "I request that", "phrase"),
               V("هل يمكن أن", "hal yumkin an", "could you", "phrase"),
               V("تكرّم بـ", "takram bi-", "kindly do", "verb"),
               V("أرسل لي", "arsil lī", "send me (imperative)", "verb"),
               V("في أقرب وقت", "fī aqrab waqt", "as soon as possible", "phrase")],
              G("Request frames, ordered by softness",
                "hal yumkin an…? > arjū an… > takram bi-… > imperative",
                "هل يمكن أن ترسل التقرير؟ أرجو أن ترسله قبل الاجتماع. تكرّم بإرسال الملف. أرسل الملف "
                "اليوم. All four are correct; only the last is an order — save it for people you lead.",
                [X("هل يمكن أن ترسل لي الأرقام؟", "hal yumkin an tursil lī al-arqām?", "Could you send me the figures?"),
                 X("أرجو أن تردّ قبل الظهر.", "arjū an tarudd qabla al-ẓuhr.", "Please reply before noon."),
                 X("تكرّم بمراجعة الصفحة الأخيرة.", "takram bi-murājaʿat al-ṣafḥa al-akhīra.", "Kindly review the last page.")],
                [("أرسل لي التقرير الآن.", "هل يمكن أن ترسل لي التقرير؟", "The bare imperative between colleagues reads as an order."),
                 ("أرجو ترسل التقرير.", "أرجو أن ترسل التقرير.", "أرجو takes أن before the verb.")]),
              [D("مديرة", "هل يمكن أن ترسل لي العرض قبل الاجتماع؟", "hal yumkin an tursil lī al-ʿarḍ qabla al-ijtimāʿ?", "Could you send me the presentation before the meeting?"),
               D("موظّف", "بكل تأكيد، أرسله الليلة.", "bi-kull taʾkīd, ursiluhu al-layla.", "Certainly — I'll send it tonight."),
               D("مديرة", "وتكرّم بمراجعة الجدول الزمني.", "wa-takram bi-murājaʿat al-jadwal al-zamanī.", "And kindly review the timeline."),
               D("موظّف", "أرجو أن يعجبك، ساهتمّ بالإطار الزمني.", "arjū an yuʿjibak, sa-ahtamm bi-l-iṭār al-zamanī.", "I hope you like it — I'll take care of the timeframe.")],
              WS("Request worksheet", [
                  T("Soften each request.", ["أرسل الملف.", "راجع الأرقام."],
                    ["هل يمكن أن ترسل الملف؟", "أرجو أن تراجع الأرقام"]),
                  T("Answer a request politely.", ["send tonight?", "review tomorrow?"],
                    ["أرسله الليلة إن شاء الله", "أراجعه غداً صباحاً"]),
              ])),
            L("Answering: فوراً، حالاً، سأفعل",
              "An answer to a request is a small contract: فوراً (right away), حالاً (immediately), غداً "
              "صباحاً (tomorrow morning). Promise a time and you have to keep it — the words are cheap, "
              "the date is not.",
              [V("فوراً", "fawran", "right away", "adverb"),
               V("حالاً", "ḥālan", "immediately", "adverb"),
               V("سأفعل", "sa-afʿal", "I will do it", "verb"),
               V("إن أمكن", "in amkan", "if possible", "phrase"),
               V("بكل تأكيد", "bi-kull taʾkīd", "certainly", "phrase")],
              G("Promise with a time",
                "fawran / ḥālan / al-yawm / ghadan + in shāʾa Allāh",
                "سأرسله حالاً. أراجعه غداً صباحاً إن شاء الله. Adding إن شاء الله is not hesitation "
                "about the work; it is the normal way Arabic marks a future promise.",
                [X("سأبدأ فوراً.", "sa-abdaʾ fawran.", "I will start right away."),
                 X("أرسلته للتوّ، تحقّق من بريدك.", "arsaltuhu li-l-taww, taḥaqqaq min barīdik.", "I just sent it — check your inbox."),
                 X("إن أمكن، أرسل لي نسخة أيضاً.", "in amkan, arsil lī nuskha aydan.", "If possible, send me a copy too.")],
                [("سأفعل غداً إن شاء الله، ثمّ اليوم أيضاً.", "(one time, one promise)", "Two dates in one promise cancel each other."),
                 ("حالاً سأفعل إن شاء الله قريباً.", "حالاً.", "حالاً already means immediately; stacking soon-words turns the promise into fog.")]),
              [D("زميل", "هل أرسلت الأرقام إلى الإدارة؟", "hal arsalta al-arqām ilā al-idāra?", "Did you send the figures to management?"),
               D("زميلة", "أرسلتها للتوّ، وأرسل النسخة النهائية فوراً.", "arsaltuhā li-l-taww, wa-ursil al-nuskha al-nihāʾiyya fawran.", "I just sent them, and I'll send the final copy right away."),
               D("زميل", "ممتاز. هل يمكن أن تضعني في النسخة؟", "mumtāz. hal yumkin an taḍaʿanī fī al-nuskha?", "Excellent. Could you copy me in?"),
               D("زميلة", "بكل تأكيد، سأضيفك حالاً.", "bi-kull taʾkīd, sa-uḍīfuk ḥālan.", "Certainly — I'll add you immediately.")],
              WS("Promise worksheet", [
                  T("Promise with a time.", ["right away", "tomorrow morning", "by Thursday"],
                    ["سأفعل فوراً", "سأفعل غداً صباحاً إن شاء الله", "سأفعل قبل الخميس"]),
                  T("Report that it is done.", ["the file", "the email", "the numbers"],
                    ["أرسلت الملف للتوّ", "أرسلت البريد قبل قليل", "جهّزت الأرقام"]),
              ])),
            L("Chat or email? One register each",
              "The same message has two lives. On chat: تكرّم، كلمة سريعة، أرسل لي. By email: تفضّلوا "
              "بالاطلاع، نرجو التكرم، نودّ إبلاغكم. Using email words in chat sounds stiff; chat words "
              "in an official letter look careless.",
              [V("كلمة سريعة", "kalima sarīʿa", "a quick word", "phrase"),
               V("رسمي", "rasmī", "formal", "adjective"),
               V("نرجو", "narjū", "we request", "verb"),
               V("تفضّلوا بالاطلاع", "tafaḍḍalū bi-l-iṭṭilāʿ", "kindly review", "phrase"),
               V("نودّ إبلاغكم", "nawudd iʿlāmakum", "we would like to inform you", "phrase")],
              G("Register switch",
                "chat: takram / kalima sarīʿa / arsil lī → email: narjū / tafaḍḍalū bi- / nawudd iʿlāmakum",
                "Chat: تكرّم، أرسل لي الملف. Email: نرجو التكرم بإرسال الملف في أقرب وقت. The same "
                "request, two distances — and choosing the wrong one is noticed before the grammar is.",
                [X("كلمة سريعة: هل نأجّل الاجتماع؟", "kalima sarīʿa: hal nuʾajjil al-ijtimāʿ?", "Quick word: shall we postpone the meeting? (chat)"),
                 X("نرجو التكرم بالموافقة على تأجيل الاجتماع.", "narjū al-takarrum bi-l-muwāfaqa ʿalā taʾjīl al-ijtimāʿ.", "We request your kind approval to postpone the meeting. (email)"),
                 X("نودّ إبلاغكم بأنّ التنفيذ يبدأ الأسبوع القادم.", "nawudd iʿlāmakum bi-anna al-tanfīdh yabdā al-usbūʿ al-qādim.", "We would like to inform you that implementation begins next week. (email)")],
                [("كلمة سريعة: نرجو التكرم بالردّ فوراً.", "(one register per message)", "Mixing chat and chancery register in one line reads as a parody of both."),
                 ("أتكرّم أن أرسل لك.", "تكرّم بإرسال الملف.", "تكرّم is addressed to the other person, not to yourself.")]),
              [D("مدير", "أرسل لي مسودّة الإعلان.", "arsil lī musawwadat al-iʿlān.", "Send me the draft of the announcement."),
               D("موظّف", "على الشات أم بالبريد الرسمي؟", "ʿalā al-shāt am bi-l-barīd al-rasmī?", "On chat or by official email?"),
               D("مدير", "بالبريد، لأنّه سيُرسل إلى العميل.", "bi-l-barīd, li-annahu sa-yursal ilā al-ʿamīl.", "By email, because it will go to the client."),
               D("موظّف", "إذاً أكتب: نرفق لكم المسودّة، ونرجو ملاحظاتكم.", "idhan aktub: nurfiq lakum al-musawwada, wa-narjū mulāḥaẓātikum.", "Then I'll write: we attach the draft and request your comments.")],
              WS("Register worksheet", [
                  T("Make it formal.", ["تكرّم، أرسل لي الملف.", "كلمة سريعة: نتأخر قليلاً."],
                    ["نرجو التكرم بإرسال الملف", "نودّ إبلاغكم بأنّنا سنتأخر قليلاً"]),
                  T("Make it a chat message.", ["نرجو التكرم بالاطلاع على الرابط.", "نودّ إبلاغكم بوصول الطلب."],
                    ["تكرّم، اطّلع على الرابط", "وصل الطلب، تكرّم بالاطلاع"]),
              ])),
        ]},
        {"id": "B1+-U2", "title": "Delays and reasons", "lessons": [
            L("Announcing a delay: تأخّرنا بسبب…",
              "A delay announced early is management; announced late it is an apology. The frame: "
              "تأخّرنا في… بسبب…، والأثر أنّ…، وسنعوّض ب…. Name the cause and the cost in two sentences.",
              [V("تأخّر", "taʾakhkhara", "to be late, delayed", "verb"),
               V("بسبب", "bi-sabab", "because of", "preposition"),
               V("الأثر", "al-athar", "the effect", "noun"),
               V("سنتدارك", "sanatadārak", "we will make up for it", "verb"),
               V("الموعد النهائي", "al-mawʿid al-nihāʾī", "the deadline", "noun")],
              G("Delay + cause + effect",
                "taʾakhkharnā fī X bi-sabab Y · wa-l-athar anna Z · sa-nuʿawwiḍ bi-…",
                "تأخّرنا في التسليم بسبب عطل في الخادم، والأثر أنّ العميل سينتظر يومين، وسنعوّض بمراجعة "
                "مجانية. Early, specific, with a remedy — that is the whole difference.",
                [X("تأخّر التوريد بسبب إجراءات الجمارك.", "taʾakhkhara al-tawrīd bi-sabab ijrāʾāt al-jamārik.", "The supply was delayed because of customs procedures."),
                 X("الأثر أنّ الإطلاق سينتقل إلى الأسبوع القادم.", "al-athar anna al-iṭlāq sa-yantaqil ilā al-usbūʿ al-qādim.", "The effect is that the launch moves to next week."),
                 X("سنعوّض التأخير بأسبوع عمل إضافي.", "sa-nuʿawwiḍ al-taʾkhīr bi-usbūʿ ʿamal iḍāfī.", "We will make up the delay with an extra working week.")],
                [("تأخّرنا بسبب بعض الأسباب.", "تأخّرنا بسبب إجراءات الجمارك.", "بعض الأسباب names nothing; a delay report needs the actual cause."),
                 ("تأخّرنا لأجل أنّ السبب…", "تأخّرنا بسبب أنّ… / تأخّرنا بسبب كذا", "سبب takes a noun directly; caused-by clauses use بسبب أنّ.")]),
              [D("عميل", "أين الشحنة؟ كان موعدها أمس.", "ayna al-shiḥna? kāna mawʿiduhā ams.", "Where is the shipment? It was due yesterday."),
               D("مدير", "تأخّرت بسبب إجراءات الجمارك، والأثر أنّها تصل غداً.", "taʾakhkharat bi-sabab ijrāʾāt al-jamārik, wa-l-athar annahā taṣil ghadan.", "It was delayed by customs, and the effect is that it arrives tomorrow."),
               D("عميل", "وهل سنعوّض ذلك؟", "wa-hal sa-nuʿawwiḍ dhālika?", "And will we be compensated?"),
               D("مدير", "سنعوّض بأسبوع إضافي في العقد دون مقابل.", "sa-nuʿawwiḍ bi-usbūʿ iḍāfī fī al-ʿaqd dūn muqābil.", "We will add a week to the contract at no cost.")],
              WS("Delay worksheet", [
                  T("Announce the delay.", ["server outage → launch", "customs → shipment"],
                    ["تأخّرنا بسبب عطل في الخادم، والأثر أنّ الإطلاق سينتقل", "تأخّر التوريد بسبب الجمارك، والأثر أنّ الشحنة تصل غداً"]),
                  T("Offer a remedy.", ["extra week", "free review"],
                    ["سنعوّض بأسبوع إضافي", "سنعوّض بمراجعة مجانية"]),
              ])),
            L("Apologising properly",
              "أعتذر عن… is the statement; أعلم أنّ هذا يسبب إزعاجاً is the acknowledgement; and the "
              "third line is the fix. Arabic apologies are expected to be short and complete — no "
              "self-pity, no excuses stacked three deep.",
              [V("أعتذر", "aʿtadhir", "I apologise", "verb"),
               V("إزعاج", "izʿāj", "inconvenience", "noun"),
               V("تقصير", "taqṣīr", "shortcoming", "noun"),
               V("أتحمّل المسؤولية", "ataḥammal al-masʾūliyya", "I take responsibility", "phrase"),
               V("لن يتكرّر", "lan yatakarrar", "it will not happen again", "phrase")],
              G("Three-line apology",
                "aʿtadhir ʿan X · aʿlam anna hādhā yusabbib izʿājan · wa-sa-… (the fix)",
                "أعتذر عن التأخير في الردّ. أعلم أنّ هذا يسبب إزعاجاً لفريقكم. سأرسل الملفات الليلة، ولن "
                "يتكرّر. Three sentences; the third is the one that repairs the relationship.",
                [X("أعتذر عن عدم الحضور أمس.", "aʿtadhir ʿan ʿadam al-ḥuḍūr ams.", "I apologise for not attending yesterday."),
                 X("أعلم أنّ هذا يسبب إزعاجاً، وأتحمّل المسؤولية.", "aʿlam anna hādhā yusabbib izʿājan, wa-ataḥammal al-masʾūliyya.", "I know this causes inconvenience, and I take responsibility."),
                 X("سأصحّح الأمر اليوم، ولن يتكرّر.", "sa-uṣaḥḥiḥ al-amr al-yawm, wa-lan yatakarrar.", "I will fix it today, and it will not happen again.")],
                [("أعتذر، لكنّ السبب ليس منّي.", "أعتذر، وأتحمّل المسؤولية عن التأخير.", "Blaming the other side inside the apology undoes it."),
                 ("أعتذر عن أنّي.", "أعتذر عن التأخير.", "أعتذر عن takes a noun or a verbal noun, not a bare أنّ clause.")]),
              [D("زميل", "انتظرتُ الردّ يومين ولم يصل شيء.", "intaẓartu al-radd yawmayn wa-lam yaṣil shayʾ.", "I waited two days for a reply and nothing came."),
               D("زميلة", "أعتذر عن التأخير في الردّ، وأعلم أنّ هذا يسبب إزعاجاً.", "aʿtadhir ʿan al-taʾkhīr fī al-radd, wa-aʿlam anna hādhā yusabbib izʿājan.", "I apologise for the late reply, and I know this causes inconvenience."),
               D("زميل", "المهم أن يصل الأمر اليوم.", "al-muhimm an yaṣil al-amr al-yawm.", "What matters is that it arrives today."),
               D("زميلة", "سأرسل كل شيء الليلة، وأتحمّل مسؤولية التأخير.", "sa-ursil kull shayʾ al-layla, wa-ataḥammal masʾūliyyat al-taʾkhīr.", "I'll send everything tonight, and I take responsibility for the delay.")],
              WS("Apology worksheet", [
                  T("Write the three lines.", ["late reply", "missed meeting"],
                    ["أعتذر عن التأخير في الردّ", "أعتذر عن عدم حضور الاجتماع"]),
                  T("Add the fix.", ["send tonight", "reschedule"],
                    ["سأرسل الملفات الليلة ولن يتكرّر", "سأقترح موعداً بديلاً هذا الأسبوع"]),
              ])),
            L("Rescheduling: هل يمكن أن نؤجّل…؟",
              "Postponing is not cancelling: نؤجّل إلى… keeps the commitment, نلغي... ends it. Give the "
              "new time in the same breath, or the other side will fill the gap with worry.",
              [V("نؤجّل", "nuʾajjil", "we postpone", "verb"),
               V("نقدّم", "nuqaddim", "we bring forward", "verb"),
               V("موعد بديل", "mawʿid badīl", "an alternative time", "phrase"),
               V("يناسبك", "yunāsibuk", "suits you", "verb"),
               V("للضرورة", "li-l-ḍarūra", "out of necessity", "phrase")],
              G("Postpone with a new date",
                "hal yumkin an nuʾajjil X ilā Y? · hal yunāsibuk…?",
                "هل يمكن أن نؤجّل الاجتماع إلى الخميس؟ هل يناسبك العاشرة؟ The new date is offered in "
                "the same message; مقترح is normal, and the other side can counter.",
                [X("هل يمكن أن نؤجّل إلى الأسبوع القادم؟", "hal yumkin an nuʾajjil ilā al-usbūʿ al-qādim?", "Can we postpone to next week?"),
                 X("هل يناسبك يوم الأحد بعد الظهر؟", "hal yunāsibuk yawm al-aḥad baʿda al-ẓuhr?", "Does Sunday afternoon suit you?"),
                 X("نقدّم الموعد نصف ساعة للضرورة.", "nuqaddim al-mawʿid niṣf sāʿa li-l-ḍarūra.", "We bring the time forward half an hour out of necessity.")],
                [("نؤجّل الاجتماع، ونحن مؤجّلون.", "نؤجّل الاجتماع إلى الخميس.", "The frame needs its destination: إلى + the new time."),
                 ("هل يمكن أن نؤجّل حذفاً؟", "هل يمكن أن نؤجّل الاجتماع؟", "The verb takes the meeting as its object, not a verbal noun.")]),
              [D("منظّم", "هل يناسبك الاجتماع يوم الثلاثاء؟", "hal yunāsibuk al-ijtimāʿ yawm al-thulāthāʾ?", "Does Tuesday suit you for the meeting?"),
               D("شريك", "للأسف، الثلاثاء مزدحم. هل يمكن أن نؤجّل إلى الأربعاء؟", "li-l-asaf, al-thulāthāʾ muzdaḥim. hal yumkin an nuʾajjil ilā al-arbiʿāʾ?", "Unfortunately Tuesday is crowded. Can we postpone to Wednesday?"),
               D("منظّم", "بالتأكيد، العاشرة صباحاً؟", "bi-l-taʾkīd, al-ʿāshira ṣabāḥan?", "Certainly — ten in the morning?"),
               D("شريك", "يناسبني تماماً، شكراً على المرونة.", "yunāsibunī tamāman, shukran ʿalā al-murūna.", "That suits me perfectly — thank you for the flexibility.")],
              WS("Reschedule worksheet", [
                  T("Postpone it with a new time.", ["meeting → Wednesday", "call → next week"],
                    ["هل يمكن أن نؤجّل الاجتماع إلى الأربعاء؟", "هل يمكن أن نؤجّل الاتصال إلى الأسبوع القادم؟"]),
                  T("Answer the proposal.", ["(it suits you)", "(it does not suit you, suggest another day)"],
                    ["يناسبني تماماً", "للأسف لا يناسبني، هل يمكن يوم الخميس؟"]),
              ])),
        ]},
        {"id": "B1+-U3", "title": "Arguing politely", "lessons": [
            L("Because, therefore, and so",
              "Three connectors carry any work argument: لأنّ (because), لذلك (therefore), ومن ثمّ (and "
              "hence). One direction per sentence — a sentence that gives a cause and then re-explains "
              "it loses the reader.",
              [V("لأنّ", "li-anna", "because", "conjunction"),
               V("لذلك", "li-dhālika", "therefore", "phrase"),
               V("من ثمّ", "min thumma", "and hence", "phrase"),
               V("النتيجة", "al-natīja", "the result", "noun"),
               V("السبب", "al-sabab", "the cause", "noun")],
              G("One direction per sentence",
                "li-anna + cause → li-dhālika / min thumma + consequence",
                "تأخّرنا لأنّ الفريق كان ناقصاً، لذلك مدّدنا المهلة. Cause first, consequence second, "
                "once. If you need both directions, use two sentences.",
                [X("ارتفعت التكلفة لأنّ الشحن غلا.", "irtafaʿat al-taklifa li-anna al-shaḥn ghalā.", "The cost rose because shipping became expensive."),
                 X("لم يصل التقرير، لذلك أرسلنا تذكيراً.", "lam yaṣil al-taqrīr, li-dhālika arsalnā tadhkīran.", "The report did not arrive, so we sent a reminder."),
                 X("انخفض الطلب، ومن ثمّ خفّضنا الإنتاج.", "inkhafaḍa al-ṭalab, wa-min thumma khaffaḍnā al-intāj.", "Demand fell, and hence we reduced production.")],
                [("تأخّرنا لأنّ السبب هو أنّ الفريق كان ناقصاً.", "تأخّرنا لأنّ الفريق كان ناقصاً.", "سبب and لأنّ say the same thing twice."),
                 ("لم يصل التقرير، لذلك، ومن ثمّ، لذا أرسلنا تذكيراً.", "(one consequence marker)", "Stacking therefore-words makes the reader doubt the logic.")]),
              [D("مدير", "لماذا تأخّر الإطلاق؟", "limādhā taʾakhkhara al-iṭlāq?", "Why was the launch delayed?"),
               D("مهندسة", "لأنّ الاختبارات لم تكتمل، لذلك أجّلنا أسبوعاً.", "li-anna al-ikhtibārāt lam taktamil, li-dhālika ajjalnā usbūʿan.", "Because testing was not complete, so we delayed a week."),
               D("مدير", "وهل هذا يؤثر على العميل؟", "wa-hal hādhā yuʾaththir ʿalā al-ʿamīl?", "And does this affect the client?"),
               D("مهندسة", "قليلاً، ومن ثمّ سنرسل رسالة توضيحية اليوم.", "qalīlan, wa-min thumma sa-nursil risāla tawḍīḥiyya al-yawm.", "A little — and hence we will send an explanatory message today.")],
              WS("Logic worksheet", [
                  T("Join with لأنّ.", ["we delayed / the server was down", "cost rose / shipping increased"],
                    ["تأخّرنا لأنّ الخادم كان معطّلاً", "ارتفعت التكلفة لأنّ الشحن غلا"]),
                  T("Give the consequence.", ["demand fell →", "the report did not arrive →"],
                    ["لذلك خفّضنا الإنتاج", "لذلك أرسلنا تذكيراً"]),
              ])),
            L("Conceding a point: معك حقّ في…",
              "معك حقّ في… (you are right about) is the strongest opening in a disagreement — it costs "
              "nothing and buys the rest of the sentence. Then: لكنّ، إلا أنّ، ومع ذلك.",
              [V("معك حقّ في", "maʿak ḥaqq fī", "you are right about", "phrase"),
               V("لكنّ", "lākinna", "but", "conjunction"),
               V("إلا أنّ", "illā anna", "except that", "phrase"),
               V("مع ذلك", "maʿa dhālika", "nevertheless", "phrase"),
               V("نقطة تحتاج نقاشاً", "nuqṭa taḥtāj niqāshan", "a point that needs discussion", "phrase")],
              G("Concede then qualify",
                "maʿak ḥaqq fī X · lākinna / illā anna + qualification",
                "معك حقّ في أنّ الوقت ضيّق، لكنّ الحلّ جاهز. معك حقّ في القراءة، إلا أنّ الأرقام تقول "
                "غير ذلك. Concession first; the disagreement lands on the qualification, not the person.",
                [X("معك حقّ في أنّ التكلفة مرتفعة.", "maʿak ḥaqq fī anna al-taklifa murtafiʿa.", "You are right that the cost is high."),
                 X("مع ذلك، لا يمكننا الانتظار أكثر.", "maʿa dhālika, lā yumkinunā al-intiẓār akthar.", "Nevertheless, we cannot wait any longer."),
                 X("هذه نقطة تحتاج نقاشاً، وأوافقك على جوهرها.", "hādhihi nuqṭa taḥtāj niqāshan, wa-uwāfiquka ʿalā jawharihā.", "This point needs discussion, and I agree with its core.")],
                [("معك حقّ، لكنّك مخطئ.", "معك حقّ في أنّ… لكنّ التنفيذ صعب.", "A concession immediately cancelled by 'you are wrong' is worse than no concession."),
                 ("أنت على حقّ في أنّك.", "معك حقّ في أنّ…", "The fixed frame is معك حقّ في + أنّ.")]),
              [D("زميل", "أرى أنّ الخطة طموحة جداً.", "arā anna al-khuṭṭa ṭamūḥa jiddan.", "I think the plan is far too ambitious."),
               D("مديرة", "معك حقّ في أنّ الوقت ضيّق، لكنّ الفريق جاهز.", "maʿak ḥaqq fī anna al-waqt ḍayyiq, lākinna al-farīq jāhir.", "You're right that time is tight, but the team is ready."),
               D("زميل", "ومع ذلك، التجارب السابقة تأخّرت.", "wa-maʿa dhālika, al-tajārib al-sābiqa taʾakhkharat.", "Nevertheless, previous experiments were delayed."),
               D("مديرة", "هذه نقطة تحتاج نقاشاً، وأوافقك على جزء منها.", "hādhihi nuqṭa taḥtāj niqāshan, wa-uwāfiquka ʿalā juzʾ minhā.", "That point needs discussion, and I agree with part of it.")],
              WS("Concession worksheet", [
                  T("Concede, then qualify.", ["cost is high / quality is worth it", "time is tight / the team is ready"],
                    ["معك حقّ في أنّ التكلفة مرتفعة، لكنّ الجودة تستحقّ", "معك حقّ في أنّ الوقت ضيّق، لكنّ الفريق جاهز"]),
                  T("Hold the point politely.", ["the deadline cannot move", "the numbers are wrong"],
                    ["مع ذلك، لا يمكن تأجيل الموعد النهائي", "مع ذلك، الأرقام لا تدعم ذلك"]),
              ])),
            L("Institutional register: نرجو، يرجى، نودّ",
              "روزنامة words: نرجو (we request), يرجى (is requested, impersonal), نودّ أن نعلمكم (we "
              "would like to inform you), نرفق لكم (we attach). A letter built from these reads as an "
              "institution, not an individual — which is exactly what it is for.",
              [V("نرجو", "narjū", "we request", "verb"),
               V("يرجى", "yurjā", "please (impersonal)", "verb"),
               V("نودّ أن نعلمكم", "nawudd an nuʿlimakum", "we would like to inform you", "phrase"),
               V("نرفق لكم", "nurfiq lakum", "we attach for you", "phrase"),
               V("وتفضّلوا بقبول فائق الاحترام", "wa-tafaḍḍalū bi-qabūl fāʾiq al-iḥtirām", "please accept our highest respect", "phrase")],
              G("Letter frames",
                "narjū / yurjā + verbal noun · nawudd an nuʿlimakum anna… · nurfiq lakum…",
                "نرجو التكرم بالاطلاع على المرفقات. يرجى العلم بأنّ الموعد تغيّر. نودّ أن نعلمكم بأنّ "
                "الطلب قيد المراجعة. Note يرجى العلم, the impersonal classic.",
                [X("نرجو التكرم بتأكيد الحضور.", "narjū al-takarrum bi-taʾkīd al-ḥuḍūr.", "We request your kind confirmation of attendance."),
                 X("يرجى العلم بأنّ الدوام يبدأ الساعة التاسعة.", "yurjā al-ʿilm bi-anna al-dawām yabdā al-sāʿa al-tāsiʿa.", "Please note that working hours begin at nine."),
                 X("نرفق لكم نسخة من الاتفاق.", "nurfiq lakum nuskha min al-ittifāq.", "We attach a copy of the agreement.")],
                [("نرجو منك أن ترسل.", "نرجو التكرم بالإرسال.", "The institutional style prefers the verbal noun to a personal verb."),
                 ("يرجى أن تعلم أنّ…", "يرجى العلم بأنّ…", "يرجى العلم is a fixed impersonal frame.")]),
              [D("إدارة", "نودّ أن نعلمكم بأنّ موعد التسليم تغيّر.", "nawudd an nuʿlimakum bi-anna mawʿid al-taslīm taghayyar.", "We would like to inform you that the delivery date has changed."),
               D("مورّد", "نرجو التكرم بإرسال التاريخ الجديد.", "narjū al-takarrum bi-irsāl al-tārīkh al-jadīd.", "We request you kindly send the new date."),
               D("إدارة", "يرجى العلم بأنّ التسليم سيكون في الخامس من الشهر.", "yurjā al-ʿilm bi-anna al-taslīm sa-yakūn fī al-khāmis min al-shahr.", "Please note that delivery will be on the fifth of the month."),
               D("مورّد", "شكراً، نرفق لكم تأكيداً بالاستلام.", "shukran, nurfiq lakum taʾkīdan bi-l-istilām.", "Thank you — we attach confirmation of receipt.")],
              WS("Register worksheet", [
                  T("Write it institutionally.", ["tell them the date changed", "ask for confirmation", "attach a file"],
                    ["نودّ أن نعلمكم بأنّ الموعد تغيّر", "نرجو التكرم بتأكيد الاستلام", "نرفق لكم نسخة من الملف"]),
                  T("Use the impersonal frame.", ["working hours start at nine", "the request is under review"],
                    ["يرجى العلم بأنّ الدوام يبدأ التاسعة", "يرجى العلم بأنّ الطلب قيد المراجعة"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Work Arabic is a register, not a dialect: an office in Amman or Riyadh writes fuṣḥā and "
                 "speaks a mix, and the email is where the formal register is expected. Two habits stand "
                 "out to newcomers — business begins after the greeting and the coffee, and a 'no' is "
                 "usually carried by إن شاء الله or a postponement rather than a plain refusal. Reading "
                 "the postponement as agreement is the classic foreign mistake."),
        source_url="https://en.wikipedia.org/wiki/Arabic",
        reading=("نودّ أن نعلمكم بأنّ موعد تسليم المشروع تغيّر من العاشر إلى العشرين بسبب إجراءات "
                 "التوريد. يرجى العلم بأنّ الفريق سيعمل أسبوعاً إضافياً دون كلفة إضافية. نرجو التكرم "
                 "بتأكيد الاستلام قبل نهاية اليوم، ونرفق لكم الجدول المحدّث."),
        reading_gloss=("We would like to inform you that the project delivery date has changed from the "
                       "tenth to the twentieth because of supply procedures. Please note that the team "
                       "will work an extra week at no additional cost. We request you kindly confirm "
                       "receipt before the end of the day; we attach the updated schedule."),
        listening=("أ: هل يمكن أن ترسل التقرير قبل الاجتماع؟<br>ب: للأسف، لن يجيزه المدير قبل الظهر.<br>"
                   "أ: إذاً نؤجّل البند إلى ما بعد الغداء.<br>ب: معك حقّ، أفضل من عرض نصف جاهز."),
        listening_gloss=("A: Could you send the report before the meeting? B: Unfortunately the director "
                         "won't approve it before noon. A: Then we postpone the item until after lunch. "
                         "B: You're right — better than a half-finished presentation."),
        voice_tag=VOICE,
        idioms=[
            ("على قدم الاستعداد", "on the foot of readiness", "on standby, ready to act"),
            ("في الوقت الضائع", "in wasted time", "outside working hours, after hours"),
            ("بالتوازي مع ذلك", "in parallel with that", "at the same time, in parallel"),
            ("من باب الحرص", "from the door of caution", "out of caution"),
            ("على المحك", "on the test bench", "on the line, under test"),
            ("بنسخة إلى", "with a copy to", "cc'd to someone"),
            ("خطوة أولى", "a first step", "an initial move"),
            ("في أقرب فرصة", "at the nearest opportunity", "at the earliest opportunity"),
            ("بأثر رجعي", "with retroactive effect", "retroactively"),
            ("موضع تقدير", "a place of appreciation", "appreciated"),
        ],
        mistakes=[
            ("سأفعل ذلك فوراً غداً.", "سأفعل ذلك غداً صباحاً.", "فوراً and غداً contradict each other."),
            ("أعتذر، لكنّ الخطأ منكم.", "أعتذر عن التأخير، وسأتحمّل المسؤولية.", "An apology that blames the other party is not an apology."),
            ("نرجو منك أن ترسل الملف.", "نرجو التكرم بإرسال الملف.", "Institutional Arabic uses يرجى/نرجو + verbal noun rather than a personal verb form."),
        ],
        task_title="Rewrite the delay email",
        task_instructions=("Take a real delay you have had to explain. Write it twice in Arabic: the "
                           "message you actually sent (chat register, two lines) and the official email "
                           "version with the cause, the effect, an apology and a remedy. Then underline "
                           "every phrase that exists only to protect the writer, and delete it — the "
                           "email should get shorter, not longer."),
    ),
    "test": [
        ("translate_en", "Complete: هل يمكن أن ___ الملف قبل الاجتماع؟", "ترسل"),
        ("translate_ar", "أعتذر عن التأخير في الردّ.", "I apologise for the late reply."),
        ("multiple_choice", "Which is the softest request?", "هل يمكن أن ترسل التقرير؟"),
        ("fill_in_the_blank", "تأخّرنا ___ عطل في الخادم. (because of)", "بسبب"),
        ("word_selection", "Select the Arabic for 'we will make up for it'.", "سنعوّض"),
        ("error_correction", "معك حقّ، لكنّك مخطئ.", "معك حقّ في أنّ الوقت ضيّق، لكنّ التنفيذ صعب."),
        ("dialogue_completion", "Complete: هل يمكن أن نؤجّل إلى ___؟ (Wednesday)", "الأربعاء"),
        ("matching", "Match مع ذلك to its meaning.", "nevertheless"),
        ("reading_comprehension", "يرجى العلم بأنّ التسليم سيكون في الخامس من الشهر. When is delivery?", "on the fifth of the month"),
        ("inference", "«هل يمكن أن نؤجّل؟» — what is the speaker trying to keep?", "the commitment, moved to a new date"),
        ("main_idea", "نرجو التكرم بتأكيد الاستلام. What is being asked?", "confirm receipt, politely"),
        ("detail_identification", "الأثر أنّ الإطلاق سينتقل إلى الأسبوع القادم. What moves to next week?", "the launch"),
    ],
}

HALFSTEPS["B2+"] = {
    "title": "Arabic B2+ — Professional",
    "native": NATIVE,
    "goals": [
        "Open, moderate and minute a meeting, with decisions that carry owners and dates",
        "Read obligations, exceptions and scope out of a contract",
        "Argue from evidence, test an assumption, and de-escalate to writing",
    ],
    "units": [
        {"id": "B2+-U1", "title": "Running the meeting", "lessons": [
            L("Agenda, item, minutes",
              "A meeting in Arabic runs on four nouns: جدول الأعمال (agenda), بند (item), مداخلة "
              "(intervention), محضر الجلسة (minutes). Put them in the invitation and the meeting "
              "starts before it starts.",
              [V("جدول الأعمال", "jadwal al-aʿmāl", "the agenda", "noun"),
               V("بند", "band", "item (of an agenda)", "noun"),
               V("مداخلة", "mudākhala", "intervention, remark", "noun"),
               V("محضر الجلسة", "maḥḍar al-jalsa", "the minutes", "noun"),
               V("نصاب", "niṣāb", "quorum", "noun")],
              G("Agenda frames",
                "band + number · ʿalā jadwal al-aʿmāl · yudawwan fī maḥḍar al-jalsa",
                "البند الأول: الميزانية. البند الثاني: الجدول الزمني. ما اكتمل النصاب؟ يُدوّن في المحضر "
                "أنّ… The agenda names the items; the minutes record what was decided, not who said what.",
                [X("ما البند الأول في جدول الأعمال؟", "mā al-band al-awwal fī jadwal al-aʿmāl?", "What is the first item on the agenda?"),
                 X("يُدوّن في المحضر أنّ الموافقة كانت بالإجماع.", "yudawwan fī al-maḥḍar anna al-muwāfaqa kānat bi-l-ijmāʿ.", "It is recorded in the minutes that approval was unanimous."),
                 X("لم يكتمل النصاب، فأجّلنا الجلسة.", "lam yaktamil al-niṣāb, fa-ajjalnā al-jalsa.", "Quorum was not reached, so we postponed the session.")],
                [("نكتب في المحضر ما قاله كلّ واحد.", "يُدوّن في المحضر ما تقرّر، لا كل ما قيل.", "Minutes record decisions and owners, not a transcript."),
                 ("البند الأولى: الميزانية.", "البند الأول: الميزانية.", "بند is masculine: الأول.")]),
              [D("رئيس الجلسة", "نبدأ بالبند الأول: الميزانية.", "nabdaʾ bi-l-band al-awwal: al-mīzāniyya.", "We start with item one: the budget."),
               D("عضو", "لديّ مداخلة قصيرة قبل التصويت.", "ladayya mudākhala qaṣīra qabla al-taṣwīt.", "I have a short remark before the vote."),
               D("رئيس الجلسة", "تفضّل، ثمّ ننتقل إلى البند الثاني.", "tafaḍḍal, thumma nantaqil ilā al-band al-thānī.", "Go ahead, then we move to item two."),
               D("عضو", "أقترح أن ندوّن الاعتراض في المحضر.", "aqtariḥ an nudawwin al-iʿtirāḍ fī al-maḥḍar.", "I suggest we record the objection in the minutes.")],
              WS("Meeting worksheet", [
                  T("Write it formally.", ["open the meeting", "move to the next item", "record the decision"],
                    ["نفتح الجلسة بالبند الأول", "ننتقل إلى البند التالي", "يُدوّن في المحضر أنّ…"]),
                  T("Ask about the procedure.", ["first item?", "is there a quorum?", "was it unanimous?"],
                    ["ما البند الأول؟", "هل اكتمل النصاب؟", "هل كانت الموافقة بالإجماع؟"]),
              ])),
            L("Moderating: keep it on the item",
              "The moderator's four lines: لنعد إلى البند (back to the item), نأخذ نقطة أخرى (another "
              "point), لنسمع الطرف الآخر (let's hear the other side), ونعود إلى الموضوع (and back to "
              "the topic). They are interruptions dressed as service.",
              [V("لنعد إلى", "li-naʿud ilā", "let us return to", "phrase"),
               V("نقطة أخرى", "nuqṭa ukhrā", "another point", "phrase"),
               V("الطرف الآخر", "al-ṭaraf al-ākhar", "the other side", "phrase"),
               V("خارج الموضوع", "khārij al-mawḍūʿ", "off topic", "phrase"),
               V("نستمع", "nastamiʿ", "we listen", "verb")],
              G("Moderator frames",
                "li-naʿud ilā al-band · khārij al-mawḍūʿ · naʾkhudh nuqṭa ukhrā · naʿūd ilā al-mawḍūʿ",
                "هذا خارج الموضوع؛ لنعد إلى البند الثاني. نأخذ نقطة أخرى ثمّ نعود إلى الموضوع. "
                "Interrupting with لي- (let us) keeps the room with you; interrupting with توقّف doesn't.",
                [X("لنعد إلى البند الثاني من فضلكم.", "li-naʿud ilā al-band al-thānī min faḍlikum.", "Let us return to item two, please."),
                 X("هذه نقطة مهمة، لكنّها خارج الموضوع الآن.", "hādhihi nuqṭa muhimma, lākinnahā khārij al-mawḍūʿ al-ān.", "That is an important point, but it is off topic for now."),
                 X("لنسمع الطرف الآخر قبل القرار.", "li-nasmaʿ al-ṭaraf al-ākhar qabla al-qarār.", "Let us hear the other side before the decision.")],
                [("اسكت، هذا خارج الموضوع.", "لنعد إلى الموضوع من فضلكم.", "The moderator's power is in the collective li-, not the imperative."),
                 ("نأخذ نقطة أخرى ثمّ نقطة أخرى ثمّ نعود.", "(one deferral)", "Deferring twice without returning means the point was dropped, and the room notices.")]),
              [D("عضو", "لكنّ المشكلة بدأت قبل ثلاث سنوات…", "lākinna al-mushkila badaʾat qabla thalāth sanawāt…", "But the problem began three years ago…"),
               D("رئيس الجلسة", "نقطة مهمة، لكنّها خارج الموضوع الآن. لنعد إلى البند.", "nuqṭa muhimma, lākinnahā khārij al-mawḍūʿ al-ān. li-naʿud ilā al-band.", "An important point, but off topic for now. Let us return to the item."),
               D("عضو آخر", "ولنسمع الطرف الآخر قبل التصويت.", "wa-li-nasmaʿ al-ṭaraf al-ākhar qabla al-taṣwīt.", "And let's hear the other side before the vote."),
               D("رئيس الجلسة", "أوافق، دقيقتان لكل طرف.", "uwāfiq, daqīqatān li-kull ṭaraf.", "Agreed — two minutes each side.")],
              WS("Moderator worksheet", [
                  T("Bring the room back.", ["the discussion drifted", "one speaker dominates"],
                    ["لنعد إلى البند الثاني من فضلكم", "لنستمع إلى الطرف الآخر"]),
                  T("Defer without dropping.", ["an important but early point", "a procedural question"],
                    ["نقطة مهمة، سنعود إليها بعد البند الحالي", "نأخذ سؤال الإجراء في النهاية"]),
              ])),
            L("Decisions with owners and dates",
              "A decision without an owner is a wish. The frame: تقرّر أنّ…، ويتولّى فلان…، بحلول…، "
              "ويُرفع تقرير بذلك في… Four slots, one sentence, nothing left to argue about later.",
              [V("تقرّر أنّ", "taqarrara anna", "it was decided that", "phrase"),
               V("يتولّى", "yatawallā", "takes charge of", "verb"),
               V("بحلول", "bi-ḥulūl", "by (a date)", "preposition"),
               V("يُرفع تقرير", "yurfaʿ taqrīr", "a report is submitted", "phrase"),
               V("متابعة", "mutābaʿa", "follow-up", "noun")],
              G("Decision frame",
                "taqarrara anna… · wa-yatawallā [name]… · bi-ḥulūl [date] · wa-yurfaʿ taqrīr…",
                "تقرّر أنّ التنفيذ يبدأ في الأول من الشهر، ويتولّى قسم العمليات الإعداد، بحلول الخامس "
                "عشر، ويُرفع تقرير بالمتابعة في نهاية الشهر. Owner, date, artefact.",
                [X("تقرّر أنّ الاجتماع القادم في الخامس.", "taqarrara anna al-ijtimāʿ al-qādim fī al-khāmis.", "It was decided that the next meeting is on the fifth."),
                 X("يتولّى فريق التسويق إعداد الرسالة.", "yatawallā farīq al-taswīq iʿdād al-risāla.", "The marketing team takes charge of preparing the message."),
                 X("ويُرفع تقرير بالنتائج بحلول العشرين.", "wa-yurfaʿ taqrīr bi-l-natāʾij bi-ḥulūl al-ʿishrīn.", "A report on the results is submitted by the twentieth.")],
                [("تقرّر أنّ نبدأ قريباً.", "تقرّر أنّ التنفيذ يبدأ في الأول من الشهر.", "قريباً is not a date; a decision needs one."),
                 ("يتولّى القسم على الإعداد.", "يتولّى القسم الإعداد.", "يتولّى takes a direct object; على is not needed.")]),
              [D("رئيس الجلسة", "ما القرار إذن؟", "mā al-qarār idhan?", "So what is the decision?"),
               D("مقرّرة", "تقرّر أنّ الإطلاق في العاشر، ويتولّى فريق المنتج الإعداد.", "taqarrara anna al-iṭlāq fī al-ʿāshir, wa-yatawallā farīq al-muntaj al-iʿdād.", "It was decided that the launch is on the tenth, and the product team takes charge of preparation."),
               D("رئيس الجلسة", "ومتى يُرفع التقرير؟", "wa-matā yurfaʿ al-taqrīr?", "And when is the report submitted?"),
               D("مقرّرة", "بحلول الخامس عشر، وستكون هناك متابعة أسبوعية.", "bi-ḥulūl al-khāmis ʿashar, wa-sa-takūn hunāk mutābaʿa usbūʿiyya.", "By the fifteenth, with a weekly follow-up.")],
              WS("Decision worksheet", [
                  T("Write the decision in one frame.", ["launch on the 10th, product team", "review on Sunday, quality team"],
                    ["تقرّر أنّ الإطلاق في العاشر ويتولّى فريق المنتج الإعداد", "تقرّر أنّ المراجعة يوم الأحد ويتولّى فريق الجودة الإعداد"]),
                  T("Add the artefact.", ["report by the 15th", "minutes tonight"],
                    ["ويُرفع تقرير بحلول الخامس عشر", "ويُرسل المحضر الليلة"]),
              ])),
        ]},
        {"id": "B2+-U2", "title": "Contracts and obligations", "lessons": [
            L("Obligation: يجب، على الطرف الأول أن",
              "Contracts are built from three obligations: يجب أن (must), على الطرف… أن (party X is to), "
              "ويلتزم بـ (and undertakes to). Learn them as a set — the parties' names in each are not decorative.",
              [V("يجب أن", "yajib an", "must", "phrase"),
               V("على الطرف الأول أن", "ʿalā al-ṭaraf al-awwal an", "the first party is to", "phrase"),
               V("يلتزم بـ", "yaltazim bi-", "undertakes to", "verb"),
               V("مادّة", "mādda", "clause, article", "noun"),
               V("سارٍ", "sārin", "in force, effective", "adjective")],
              G("Obligation frames",
                "yajib an + verb · ʿalā al-ṭaraf al-awwal an + verb · yaltazim + bi- + verbal noun",
                "يجب أن يسلّم الطرف الأول الأعمال قبل الأول من يونيو. وعلى الطرف الثاني أن يسدّ الدفعة "
                "خلال خمسة عشر يوماً. ويلتزم الطرفان بالسرّية. Obligation lands on the party, not on 'we'.",
                [X("على الطرف الثاني أن يبلّغ بأي تأخير فوراً.", "ʿalā al-ṭaraf al-thānī an yuballigh bi-ayy taʾkhīr fawran.", "The second party is to notify of any delay immediately."),
                 X("يلتزم المورّد بالسرّية مدة خمس سنوات.", "yaltazim al-muwarrid bi-l-sirriyya muddat khams sanawāt.", "The supplier undertakes confidentiality for five years."),
                 X("تصبح المادّة الثالثة سارية من تاريخ التوقيع.", "tuṣbiḥ al-mādda al-thālitha sāriya min tārīkh al-tawqīʿ.", "Clause three takes effect from the date of signature.")],
                [("يجب الطرف الأول أن يسلّم.", "يجب أن يسلّم الطرف الأول.", "يجب أن opens with أن before the verb."),
                 ("يلتزم الطرف الأول السرّية.", "يلتزم الطرف الأول بالسرّية.", "يلتزم takes بـ before what is undertaken.")]),
              [D("مستشار", "ماذا تلتزم به الشركة في العقد؟", "mādhā taltazim bihi al-sharika fī al-ʿaqd?", "What does the company undertake in the contract?"),
               D("مدير", "يجب أن تنسحب في أي وقت بإشعار ثلاثين يوماً.", "yajib an tansḥab fī ayy waqt bi-ishʿār thalāthīn yawman.", "It must withdraw at any time with thirty days' notice."),
               D("مستشار", "وعلى الطرف الثاني أن يدفع قبل الاستلام، صحيح؟", "wa-ʿalā al-ṭaraf al-thānī an yadfaʿ qabla al-istilām, ṣaḥīḥ?", "And the second party is to pay before delivery, correct?"),
               D("مدير", "نعم، خلال خمسة عشر يوماً من التوقيع.", "naʿam, khilāl khamsata ʿashar yawman min al-tawqīʿ.", "Yes — within fifteen days of signature.")],
              WS("Obligation worksheet", [
                  T("Write the obligation.", ["pay within 15 days", "deliver before June 1", "keep confidentiality"],
                    ["يجب أن يدفع خلال خمسة عشر يوماً", "على الطرف الأول أن يسلّم قبل الأول من يونيو", "يلتزم الطرفان بالسرّية"]),
                  T("Name the party.", ["notify a delay", "renew for one year"],
                    ["على الطرف الثاني أن يبلّغ بأي تأخير", "على الطرف الأول أن يجدّد لسنة واحدة"]),
              ])),
            L("Exceptions and scope: باستثناء، ولا يسري",
              "The two sentences that decide a dispute: باستثناء (with the exception of) and ولا يسري "
              "هذا على (and this does not apply to). An obligation read without its exception is a "
              "different contract.",
              [V("باستثناء", "bi-stithnāʾ", "with the exception of", "preposition"),
               V("لا يسري", "lā yasrī", "does not apply, is not in force", "verb"),
               V("يشمل", "yashmal", "covers, includes", "verb"),
               V("ينطبق على", "yanṭabiq ʿalā", "applies to", "verb"),
               V("في حال", "fī ḥāl", "in the event of", "phrase")],
              G("Scope limiters",
                "bi-stithnāʾ + noun · lā yasrī hādhā ʿalā + noun · yanṭabiq ʿalā",
                "تسري الأحكام على جميع المواد باستثناء المادّة السابعة. ولا يسري هذا البند على الحالات "
                "الطارئة. في حال التأخير بسبب القوة القاهرة، لا يُحتسب التعويض.",
                [X("يشمل العقد الصيانة باستثناء قطع الغيار.", "yashmal al-ʿaqd al-ṣiyāna bi-stithnāʾ qiṭaʿ al-ghiyār.", "The contract covers maintenance with the exception of spare parts."),
                 X("لا يسري هذا الحكم على العقود السابقة.", "lā yasrī hādhā al-ḥukm ʿalā al-ʿuqūd al-sābiqa.", "This provision does not apply to previous contracts."),
                 X("ينطبق التعويض على التأخير غير المبرّر فقط.", "yanṭabiq al-taʿwīḍ ʿalā al-taʾkhīr ghayr al-mubarrar faqaṭ.", "Compensation applies only to unjustified delay.")],
                [("باستثناء عن المادّة السابعة.", "باستثناء المادّة السابعة.", "باستثناء takes its noun directly; عن is not needed."),
                 ("لا يسري على القوة القاهرة هذا البند.", "لا يسري هذا البند على القوة القاهرة.", "In formal Arabic the subject follows immediately after the verb: لا يسري هذا البند.")]),
              [D("مستشار", "هل يغطّي التأمين الأضرار كلّها؟", "hal yughaṭṭī al-taʾmīn al-aḍrār kullahā?", "Does the insurance cover all damages?"),
               D("مدير", "كلّها باستثناء الأضرار الناتجة عن الإهمال.", "kullahā bi-stithnāʾ al-aḍrār al-nātija ʿan al-ihmāl.", "All of them, with the exception of damages caused by negligence."),
               D("مستشار", "وهل يسري ذلك على العقود القديمة؟", "wa-hal yasrī dhālika ʿalā al-ʿuqūd al-qadīma?", "And does that apply to the old contracts?"),
               D("مدير", "لا يسري هذا الحكم عليها؛ ينطبق على الجديدة فقط.", "lā yasrī hādhā al-ḥukm ʿalayhā; yanṭabiq ʿalā al-jadīda faqaṭ.", "This provision does not apply to them; it applies only to the new ones.")],
              WS("Scope worksheet", [
                  T("Add the exception.", ["maintenance (spare parts)", "insurance (negligence)"],
                    ["يشمل العقد الصيانة باستثناء قطع الغيار", "يغطّي التأمين الأضرار باستثناء الإهمال"]),
                  T("Exclude it formally.", ["old contracts", "emergency cases"],
                    ["لا يسري هذا الحكم على العقود السابقة", "لا يسري هذا البند على الحالات الطارئة"]),
              ])),
            L("Asking about scope before you sign",
              "Four questions save a signature: إلى متى؟ (until when), هل يشمل…؟ (does it cover), ما "
              "المقصود بـ…؟ (what is meant by), ومن يتحمّل…؟ (who bears). Ask them out loud in the "
              "meeting and record the answers.",
              [V("إلى متى", "ilā matā", "until when", "phrase"),
               V("هل يشمل", "hal yashmal", "does it cover", "phrase"),
               V("ما المقصود بـ", "mā al-maqṣūd bi-", "what is meant by", "phrase"),
               V("من يتحمّل", "man yataḥammal", "who bears", "phrase"),
               V("بند غامض", "band ghāmiḍ", "an ambiguous clause", "phrase")],
              G("Scope questions",
                "ilā matā + verb? · hal yashmal + noun? · mā al-maqṣūd bi- + noun? · man yataḥammal + noun?",
                "إلى متى تبقى هذه المادّة سارية؟ هل يشمل السعر التدريب؟ ما المقصود بـ«التأخير المبرّر»؟ "
                "من يتحمّل كلفة النقل؟ Ask, record, then sign.",
                [X("إلى متى تستمرّ فترة الضمان؟", "ilā matā tastamirr fatrat al-ḍamān?", "Until when does the warranty period last?"),
                 X("ما المقصود بـ«التسليم» في المادّة الرابعة؟", "mā al-maqṣūd bi-«al-taslīm» fī al-mādda al-rābiʿa?", "What is meant by 'delivery' in clause four?"),
                 X("من يتحمّل كلفة الشحن في حال التأخير؟", "man yataḥammal kulfat al-shaḥn fī ḥāl al-taʾkhīr?", "Who bears the shipping cost in the event of delay?")],
                [("إلى متى؟ غداً.", "إلى متى تستمرّ فترة الضمان؟", "The question needs its subject; a bare إلى متى leaves the answer to the other side."),
                 ("ما المقصود للتسليم؟", "ما المقصود بالتسليم؟", "The frame is ما المقصود بـ, with بـ.")]),
              [D("مدير", "نوقّع غداً، هل من أسئلة؟", "nuwaqqiʿ ghadan, hal min asʾila?", "We sign tomorrow — any questions?"),
               D("مستشار", "إلى متى تستمرّ فترة الضمان؟", "ilā matā tastamirr fatrat al-ḍamān?", "How long does the warranty last?"),
               D("مدير", "سنتان من التسليم، وما المقصود بالسؤال الثاني؟", "sanatān min al-taslīm, wa-mā al-maqṣūd bi-l-suʾāl al-thānī?", "Two years from delivery — and what do you mean by the second question?"),
               D("مستشار", "هل يشمل الضمان قطع الغيار، ومن يتحمّل النقل؟", "hal yashmal al-ḍamān qiṭaʿ al-ghiyār, wa-man yataḥammal al-naql?", "Does the warranty cover spare parts, and who bears transport?")],
              WS("Scope question worksheet", [
                  T("Ask before signing.", ["warranty duration", "does it cover training?", "who bears transport?"],
                    ["إلى متى تستمرّ فترة الضمان؟", "هل يشمل السعر التدريب؟", "من يتحمّل كلفة النقل؟"]),
                  T("Pin down an ambiguous clause.", ["«delivery»", "«justified delay»"],
                    ["ما المقصود بـ«التسليم»؟", "ما المقصود بـ«التأخير المبرّر»؟"]),
              ])),
        ]},
        {"id": "B2+-U3", "title": "Evidence and de-escalation", "lessons": [
            L("Evidence: تدلّ الأرقام على",
              "Three evidence frames: تدلّ… على (indicates), تشير البيانات إلى (the data point to), من "
              "الواضح أنّ (it is clear that). Each claims a different strength — and the difference is "
              "the argument.",
              [V("تدلّ على", "tadullu ʿalā", "indicates", "verb"),
               V("تشير إلى", "tushīr ilā", "points to", "verb"),
               V("من الواضح أنّ", "min al-wāḍiḥ anna", "it is clear that", "phrase"),
               V("يؤكّد", "yuʾakkid", "confirms", "verb"),
               V("قرينة", "qarīna", "piece of evidence, indication", "noun")],
              G("Strength of evidence",
                "tadullu ʿalā < tushīr ilā < yuʾakkid · min al-wāḍiḥ anna…",
                "تدلّ الأرقام على تحسّن الطلب. تشير البيانات إلى تحوّل في السوق. يؤكّد التقرير أنّ "
                "الاتجاه مستمرّ. Use the weakest frame that is true.",
                [X("تدلّ الأرقام على تحسّن الطلب في الربع الأخير.", "tadullu al-arqām ʿalā taḥassun al-ṭalab fī al-rubʿ al-akhīr.", "The figures indicate an improvement in demand in the last quarter."),
                 X("تشير البيانات إلى تحوّل في سلوك المستهلك.", "tushīr al-bayānāt ilā taḥawwul fī sulūk al-mustahlik.", "The data point to a shift in consumer behaviour."),
                 X("من الواضح أنّ القرار كان مبنياً على تقديرات قديمة.", "min al-wāḍiḥ anna al-qarār kāna mabniyyan ʿalā taqdīrāt qadīma.", "It is clear that the decision rested on old estimates.")],
                [("يثبت الرقم أنّ…", "تدلّ الأرقام على…", "A single figure indicates; only a controlled comparison confirms."),
                 ("تشير البيانات إلى أنّ السوق يتغيّر تغيّراً.", "تشير البيانات إلى تحوّل في السوق.", "The nominal style is shorter: تحوّل, not يتغيّر تغيّراً.")]),
              [D("محلّل", "كيف تقرأ النتائج؟", "kayfa taqraʾ al-natāʾij?", "How do you read the results?"),
               D("خبير", "تدلّ الأرقام على تحسّن، وتشير البيانات إلى أنّه مؤقّت.", "tadullu al-arqām ʿalā taḥassun, wa-tushīr al-bayānāt ilā annahu muʾaqqat.", "The figures indicate improvement, and the data suggest it is temporary."),
               D("محلّل", "وهل يؤكّد التقرير ذلك؟", "wa-hal yuʾakkid al-taqrīr dhālika?", "And does the report confirm that?"),
               D("خبير", "لا، التقرير يكتفي بالإشارة.", "lā, al-taqrīr yaktafī bi-l-ishāra.", "No — the report only points to it.")],
              WS("Evidence worksheet", [
                  T("Choose the right strength.", ["one quarter of data (indicate)", "two years of data (confirm)"],
                    ["تدلّ الأرقام على تحسّن", "يؤكّد التقرير أنّ الاتجاه مستمرّ"]),
                  T("Say it in the nominal style.", ["the shift in behaviour", "the improvement in demand"],
                    ["تشير البيانات إلى تحوّل في السلوك", "تدلّ الأرقام على تحسّن في الطلب"]),
              ])),
            L("Testing an assumption: لنفترض أنّ… فماذا؟",
              "لنفترض أنّ (let us assume) turns an argument into a test. Add فماذا يحدث؟ or فما النتيجة؟ "
              "and the room examines the assumption instead of defending it.",
              [V("لنفترض أنّ", "li-naftariḍ anna", "let us assume that", "phrase"),
               V("فماذا", "fa-mādhā", "then what", "phrase"),
               V("إذا صحّ ذلك", "idhā ṣaḥḥa dhālika", "if that is correct", "phrase"),
               V("الافتراض", "al-iftirāḍ", "the assumption", "noun"),
               V("صامد", "ṣāmid", "holding up, standing firm", "adjective")],
              G("Assume and test",
                "li-naftariḍ anna X · fa-mādhā? · idhā ṣaḥḥa dhālika, fa-…",
                "لنفترض أنّ الطلب تراجع فعلاً، فماذا يحدث للمخزون؟ The assumption is named, then its "
                "consequence is followed — that is how a hypothesis is tested in public.",
                [X("لنفترض أنّ الأسعار ترتفع 10%، فماذا يحدث للطلب؟", "li-naftariḍ anna al-asʿār tartafiʿ 10%, fa-mādhā yaḥduth li-l-ṭalab?", "Let us assume prices rise 10% — what happens to demand?"),
                 X("إذا صحّ ذلك، فالخطة تحتاج تعديلاً.", "idhā ṣaḥḥa dhālika, fa-l-khuṭṭa taḥtāj taʿdīlan.", "If that is correct, the plan needs adjustment."),
                 X("الافتراض نفسه يحتاج دليلاً.", "al-iftirāḍ nafsuhu yaḥtāj dalīlan.", "The assumption itself needs evidence.")],
                [("لنفترض أنّ الأسعار ترتفع، إذاً الأسعار سترتفع.", "لنفترض أنّ الأسعار ترتفع، فماذا يحدث للطلب؟", "The assumption must lead somewhere new, not restate itself."),
                 ("لنفترض إذا أنّ…", "لنفترض أنّ…", "The frame is لنفترض أنّ, without إذا.")]),
              [D("مدير", "الخطة تعمل إذا بقي الطلب ثابتاً.", "al-khuṭṭa taʿmal idhā baqiya al-ṭalab thābitan.", "The plan works if demand stays flat."),
               D("محلّل", "لنفترض أنّ الطلب انخفض 15%، فماذا يحدث للمخزون؟", "li-naftariḍ anna al-ṭalab inkhafaḍa 15%, fa-mādhā yaḥduth li-l-makhzūn?", "Let us assume demand falls 15% — what happens to inventory?"),
               D("مدير", "إذا صحّ ذلك، نتوقّف عن التوريد في الشهر الثالث.", "idhā ṣaḥḥa dhālika, natawaqqaf ʿan al-tawrīd fī al-shahr al-thālith.", "If that is correct, we stop supply in the third month."),
               D("محلّل", "إذاً الافتراض يجب أن يُختبر قبل التنفيذ.", "idhan al-iftirāḍ yajib an yukhtabar qabla al-tanfīdh.", "Then the assumption must be tested before execution.")],
              WS("Assumption worksheet", [
                  T("Test the assumption.", ["demand falls 15%", "the supplier is late"],
                    ["لنفترض أنّ الطلب ينخفض 15%، فماذا يحدث؟", "لنفترض أنّ المورّد يتأخّر، فماذا نفعل؟"]),
                  T("Name what the assumption needs.", ["evidence", "a test"],
                    ["الافتراض يحتاج دليلاً", "الافتراض يجب أن يُختبر قبل التنفيذ"]),
              ])),
            L("De-escalation: back to the shared point",
              "When a discussion is heating up, three moves cool it: نتفق على أنّ (we agree that), "
              "لنعد إلى ما نتفق عليه (back to what we agree on), and خلاصة القول (summing up). Then you "
              "put the outcome in writing, where nobody is performing.",
              [V("نتفق على أنّ", "nattafiq ʿalā anna", "we agree that", "phrase"),
               V("لنعد إلى", "li-naʿud ilā", "let us return to", "phrase"),
               V("خلاصة القول", "khulāṣat al-qawl", "summing up", "phrase"),
               V("نرفع الأمر كتابةً", "narfaʿ al-amr kitābatan", "we put it in writing", "phrase"),
               V("نقطة مشتركة", "nuqṭa mushtaraka", "common ground", "phrase")],
              G("Cooling moves",
                "nattafiq ʿalā anna… · li-naʿud ilā mā nattafiq ʿalayhi · khulāṣat al-qawl · wa-narfaʿuhu kitābatan",
                "نتفق على أنّ الهدف واحد. لنعد إلى ما نتفق عليه: الجودة والتوقيت. خلاصة القول، نرفع "
                "الأمر كتابةً غداً. Writing is the de-escalator — the room can argue, the file cannot.",
                [X("نتفق على أنّ المشكلة تحتاج قراراً، ونختلف في التوقيت.", "nattafiq ʿalā anna al-mushkila taḥtāj qarāran, wa-nakhtalif fī al-tawqīt.", "We agree the problem needs a decision; we differ on the timing."),
                 X("لنعد إلى ما نتفق عليه: الجودة أولاً.", "li-naʿud ilā mā nattafiq ʿalayhi: al-jawda awwalan.", "Let us return to what we agree on: quality first."),
                 X("خلاصة القول، نرفع التوصية كتابةً.", "khulāṣat al-qawl, narfaʿ al-tawṣiya kitābatan.", "To sum up, we submit the recommendation in writing.")],
                [("نتفق على أنّك مخطئ.", "نتفق على أنّ المشكلة تحتاج قراراً.", "نتفق على أنّ must name real common ground; a disguised accusation escalates."),
                 ("لنعد إلى الموضوع الأصلي الذي بدأنا به من البداية.", "لنعد إلى ما نتفق عليه.", "Padding the return move loses the room; say the common point.")]),
              [D("عضو", "هذا اقتراح غير واقعي، وقد قلتُ ذلك من البداية.", "hādhā iqtirāḥ ghayr wāqiʿī, wa-qad qultu dhālika min al-bidāya.", "This proposal is unrealistic — I said so from the start."),
               D("رئيس الجلسة", "نتفق على أنّ التكلفة مشكلة، ونختلف في الحلّ.", "nattafiq ʿalā anna al-taklifa mushkila, wa-nakhtalif fī al-ḥall.", "We agree the cost is a problem; we differ on the solution."),
               D("عضو", "على الأقلّ لنعد إلى الأرقام.", "ʿalā al-aqall li-naʿud ilā al-arqām.", "At least let us return to the numbers."),
               D("رئيس الجلسة", "خلاصة القول، نرفع المقترحين كتابةً ونقرّر الأسبوع القادم.", "khulāṣat al-qawl, narfaʿ al-muqtaraḥayn kitābatan wa-nuqarrir al-usbūʿ al-qādim.", "To sum up: we submit both proposals in writing and decide next week.")],
              WS("De-escalation worksheet", [
                  T("Find the common ground.", ["one side wants speed, the other quality", "one wants cuts, the other growth"],
                    ["نتفق على أنّ الهدف واحد، ونختلف في الوسيلة", "نتفق على أنّ الميزانية محدودة، ونختلف في الأولويات"]),
                  T("Move it to writing.", ["sum up", "submit tomorrow"],
                    ["خلاصة القول…", "نرفع الأمر كتابةً غداً"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Arabic business writing keeps an older formality than English does: formulaic openings "
                 "(نودّ أن نعلمكم), the impersonal يرجى العلم, and closings that thank the reader for "
                 "their attention. Contracts use classical obligation frames and are read literally, so "
                 "learners are expected to ask what a clause covers before they sign — asking is taken "
                 "as diligence, not distrust."),
        source_url="https://en.wikipedia.org/wiki/Arabic_grammar",
        reading=("تقرّر في جلسة أمس أنّ الإطلاق سيُؤجّل أسبوعين، ويتولّى فريق المنتج إعداد النسخة "
                 "النهائية بحلول الخامس عشر. ولا يسري هذا القرار على التسويق الذي يبدأ في موعده. ويرجى "
                 "العلم بأنّ العقد ينصّ على إشعار مسبق مدّته ثلاثون يوماً في حال التأجيل."),
        reading_gloss=("It was decided in yesterday's session that the launch will be postponed two weeks, "
                       "and the product team takes charge of preparing the final version by the "
                       "fifteenth. This decision does not apply to marketing, which starts on schedule. "
                       "Please note that the contract stipulates thirty days' prior notice in the event "
                       "of postponement."),
        listening=("أ: هل يشمل العقد التدريب على النظام الجديد؟<br>ب: لا يشمل؛ التدريب بند منفصل.<br>"
                   "أ: ومن يتحمّل كلفة النقل؟<br>ب: الطرف الأول، بحسب المادّة السابعة."),
        listening_gloss=("A: Does the contract cover training on the new system? B: It does not — training "
                         "is a separate item. A: And who bears the transport cost? B: The first party, "
                         "under clause seven."),
        voice_tag=VOICE,
        idioms=[
            ("بند منفصل", "a separate item", "a distinct clause, negotiated separately"),
            ("في نهاية المطاف", "at the end of the path", "ultimately"),
            ("على طاولة المفاوضات", "on the negotiating table", "under negotiation"),
            ("خط أحمر", "a red line", "a non-negotiable limit"),
            ("حسن النية", "good intention", "good faith"),
            ("القوة القاهرة", "force majeure", "acts of God, unforeseeable events"),
            ("بأثر فوري", "with immediate effect", "effective at once"),
            ("من حيث المبدأ", "from the standpoint of principle", "in principle"),
            ("على أساس", "on the basis of", "on the basis of"),
            ("في حدود ما", "within the limits of what", "as far as, in so far as"),
        ],
        mistakes=[
            ("يجب الطرف الأول أن يسلّم.", "يجب أن يسلّم الطرف الأول.", "يجب أن requires أن before the verb."),
            ("باستثناء عن المادّة السابعة.", "باستثناء المادّة السابعة.", "باستثناء takes its noun directly."),
            ("نتفق على أنّك مخطئ.", "نتفق على أنّ المشكلة تحتاج قراراً.", "Common ground must be real; a disguised accusation escalates."),
        ],
        task_title="Minute one real meeting",
        task_instructions=("Take a meeting you attended this week and write its minutes in Arabic: the "
                           "agenda items, one decision in the frame تقرّر أنّ… ويتولّى… بحلول…, one "
                           "exception (لا يسري هذا على…), and the shared point the room actually agreed "
                           "on. Then have someone who was not there read it and say what they think "
                           "was decided — that is the only test minutes have."),
    ),
    "test": [
        ("translate_en", "Say: It was decided that the launch is on the tenth.", "تقرّر أنّ الإطلاق في العاشر."),
        ("translate_ar", "لا يسري هذا الحكم على العقود السابقة.", "This provision does not apply to previous contracts."),
        ("multiple_choice", "Which is the weakest evidence claim?", "تدلّ الأرقام على تحسّن الطلب"),
        ("fill_in_the_blank", "على الطرف الأول ___ يسلّم الأعمال. (to)", "أن"),
        ("word_selection", "Select the Arabic for 'with the exception of'.", "باستثناء"),
        ("error_correction", "يجب الطرف الثاني أن يدفع.", "يجب أن يدفع الطرف الثاني."),
        ("dialogue_completion", "Complete: ما المقصود ___«التسليم»؟ (by)", "بـ"),
        ("matching", "Match محضر الجلسة to its meaning.", "the minutes"),
        ("reading_comprehension", "ويتولّى فريق المنتج إعداد النسخة النهائية بحلول الخامس عشر. Who owns it, and by when?", "the product team, by the fifteenth"),
        ("inference", "«الافتراض نفسه يحتاج دليلاً» — what is the speaker asking for?", "evidence before the plan is executed"),
        ("main_idea", "نتفق على أنّ التكلفة مشكلة، ونختلف في الحلّ. What is the moderator doing?", "narrowing the disagreement to one point"),
        ("detail_identification", "المادّة السابعة: الإشعار قبل ثلاثين يوماً. How long is the notice?", "thirty days"),
    ],
}

HALFSTEPS["C1+"] = {
    "title": "Arabic C1+ — Almost native",
    "native": NATIVE,
    "goals": [
        "Architect a work report and cut institutional Arabic down to what it needs",
        "Translate with a chosen register, catch calques and check by back-translation",
        "Teach a beginner a rule, correct kindly, and work from the root rather than by rote",
    ],
    "units": [
        {"id": "C1+-U1", "title": "Writing for work", "lessons": [
            L("Report architecture: ملخّص، نتائج، توصيات",
              "A formal Arabic report has four rooms: ملخّص تنفيذي (executive summary), نتائج (findings), "
              "توصيات (recommendations), ملحق (annex). Each has its own verb mood — findings report, "
              "recommendations propose, and neither argues.",
              [V("ملخّص تنفيذي", "mulakhkhaṣ tanfīdhī", "executive summary", "noun"),
               V("نتائج", "natāʾij", "findings", "noun"),
               V("توصيات", "tawṣiyāt", "recommendations", "noun"),
               V("ملحق", "mulḥaq", "annex", "noun"),
               V("منهجية", "manhajiyya", "methodology", "noun")],
              G("Four rooms, three moods",
                "findings: tadullu / tushīr · recommendations: nawṣī bi- / yuqtaraḥ · summary: khulāṣa",
                "النتائج: تدلّ الأرقام على تحسّن محدود. التوصيات: نوصي بتمديد المهلة شهراً. Neither "
                "section should contain the other's sentences — that is the most common structural fault "
                "in Arabic reports.",
                [X("يستعرض الملخّص التنفيذي أهمّ ثلاث نتائج.", "yastaʿriḍ al-mulakhkhaṣ al-tanfīdhī ahamm thalāth natāʾij.", "The executive summary presents the three key findings."),
                 X("نوصي بتوسيع العيّنة في المرحلة الثانية.", "nawṣī bi-tawṣīʿ al-ʿayyina fī al-marḥala al-thāniya.", "We recommend widening the sample in the second phase."),
                 X("تجدون التفاصيل في الملحق الثاني.", "tajidūn al-tafāṣīl fī al-mulḥaq al-thānī.", "You will find the details in annex two.")],
                [("النتائج: نوصي بتغيير الخطة.", "التوصيات: نوصي بتغيير الخطة.", "A recommendation recorded under findings blurs the document's authority."),
                 ("نوصي بتمديد المهلة شهراً، لذلك يجب…", "(recommendation stops at the proposal)", "The recommendation section proposes; the argument belongs to the summary.")]),
              [D("مدير", "أريد المسودّة الليلة: ملخّص ونتائج وتوصيات.", "urīd al-musawwada al-layla: mulakhkhaṣ wa-natāʾij wa-tawṣiyāt.", "I want the draft tonight: summary, findings, recommendations."),
               D("كاتب", "هل أضع التوصيات في الملخّص التنفيذي؟", "hal aḍaʿ al-tawṣiyāt fī al-mulakhkhaṣ al-tanfīdhī?", "Do I put the recommendations in the executive summary?"),
               D("مدير", "إشارة فقط، والباقي في قسمه.", "ishāra faqaṭ, wa-l-bāqī fī qismihi.", "A signpost only — the rest in its own section."),
               D("كاتب", "والتفاصيل التقنية؟", "wa-l-tafāṣīl al-tiqniyya?", "And the technical details?"),
               D("مدير", "في الملحق؛ لا تُثقل الملخّص.", "fī al-mulḥaq; lā tuthqil al-mulakhkhaṣ.", "In the annex; don't weigh down the summary.")],
              WS("Report worksheet", [
                  T("Label the section.", ["a figure that shows improvement", "we suggest a delay", "raw tables"],
                    ["النتائج", "التوصيات", "الملحق"]),
                  T("Write a signpost.", ["point to annex two", "point to three findings"],
                    ["تجدون التفاصيل في الملحق الثاني", "يستعرض الملخّص ثلاث نتائج"]),
              ])),
            L("Trimming institutional prose",
              "Institutional Arabic pads itself with قام بـ (carried out the doing of), تجدر الإشارة "
              "(it deserves noting), في إطار (within the framework of). A C1+ writer cuts them: the "
              "verb comes back, and the document gets shorter and stronger.",
              [V("الحشو", "al-ḥashw", "padding, filler", "noun"),
               V("قام بـ", "qāma bi-", "carried out (padding frame)", "phrase"),
               V("تجدر الإشارة", "tajdur al-ishāra", "it is worth noting (padding)", "phrase"),
               V("في إطار", "fī iṭār", "within the framework of (padding)", "phrase"),
               V("صياغة رشيقة", "ṣiyāgha rashīqa", "lean prose", "phrase")],
              G("Cut the frame, keep the verb",
                "qāma bi- + verbal noun → the verb itself · fī iṭār + verbal noun → the noun",
                "قامت الوزارة بتنفيذ الخطة → نفّذت الوزارة الخطة. في إطار تحسين الخدمات، أطلقنا → حسّنّا "
                "الخدمات وأطلقنا. Each cut returns a verb to the sentence.",
                [X("نفّذت الوزارة الخطة قبل موعدها.", "naffadhat al-wizāra al-khuṭṭa qabla mawʿidihā.", "The ministry implemented the plan ahead of time."),
                 X("حسّنّا الخدمات وأطلقنا منصة جديدة.", "ḥassannā al-khadamāt wa-aṭlaqnā mannaṣṣa jadīda.", "We improved the services and launched a new platform."),
                 X("يبدأ التنفيذ في مارس.", "yabdā al-tanfīdh fī Mārs.", "Implementation begins in March.")],
                [("قامت الوزارة بتنفيذ الخطة.", "نفّذت الوزارة الخطة.", "قام بـ adds a verb and removes one; the sentence loses a syllable and gains a subject."),
                 ("تجدر الإشارة إلى أنّ الزراعة تحسّنت.", "تحسّنت الزراعة.", "If the sentence is worth writing, it is worth asserting.")]),
              [D("محرّر", "هذه الفقرة طويلة جداً.", "hādhihi al-faqra ṭawīla jiddan.", "This paragraph is very long."),
               D("كاتب", "تحتوي على صياغة رسمية فقط.", "taḥtawī ʿalā ṣiyāgha rasmīyya faqaṭ.", "It only contains formal phrasing."),
               D("محرّر", "اقلع الحشو: من «قامت بـ» إلى الفعل مباشرة.", "iqlaʿ al-ḥashw: min «qāmat bi-» ilā al-fiʿl mubāsharatan.", "Cut the padding: from 'carried out' straight to the verb."),
               D("كاتب", "إذاً: «نفّذت الوزارة الخطة». أقصر وأقوى.", "idhan: «naffadhat al-wizāra al-khuṭṭa». aqṣar wa-aqwā.", "So: 'The ministry implemented the plan.' Shorter and stronger.")],
              WS("Trimming worksheet", [
                  T("Cut the frame.", ["قامت الشركة بإطلاق الخدمة.", "تجدر الإشارة إلى أنّ الطلب ارتفع."],
                    ["أطلقت الشركة الخدمة", "ارتفع الطلب"]),
                  T("Cut to the noun.", ["في إطار تحسين الجودة", "في إطار خطة التحوّل الرقمي"],
                    ["لتحسين الجودة / بتحسين الجودة", "في خطة التحوّل الرقمي"]),
              ])),
            L("Editing protocol: suggest, don't rewrite",
              "Editing someone's Arabic in a team has a protocol: هذا اقتراح تعديل (this is a suggested "
              "edit), هل يمكن أن نعيد الصياغة؟ (may we rephrase?), التعليق في الهامش (comment in the "
              "margin), and mark whose text it is. The writer stays the owner; the editor stays honest.",
              [V("اقتراح تعديل", "iqtirāḥ taʿdīl", "a suggested edit", "phrase"),
               V("الهامش", "al-hāmish", "the margin", "noun"),
               V("أعيد الصياغة", "uʿīd al-ṣiyāgha", "let me rephrase", "phrase"),
               V("تعليق", "taʿlīq", "comment", "noun"),
               V("نسخة نظيفة", "nuskha naḍīfa", "a clean copy", "phrase")],
              G("Suggest, explain, release",
                "hādhā iqtirāḥ taʿdīl · hal yumkin an nuʿīd al-ṣiyāgha? · al-taʿlīq fī al-hāmish",
                "اقتراح: الفعل «أفاد» أوضح من «قال» هنا. التعليل: لأنّ النصّ خبر رسمي. Then leave it to "
                "the writer — an edit without an explanation is a demand.",
                [X("هذا اقتراح تعديل، والتعديل النهائي لك.", "hādhā iqtirāḥ taʿdīl, wa-l-taʿdīl al-nihāʾī lak.", "This is a suggested edit; the final call is yours."),
                 X("هل يمكن أن نعيد صياغة الجملة الأولى؟", "hal yumkin an nuʿīd ṣiyāghat al-jumla al-ūlā?", "May we rephrase the first sentence?"),
                 X("تركتُ تعليقاً في الهامش مع السبب.", "taraktu taʿlīqan fī al-hāmish maʿa al-sabab.", "I left a comment in the margin with the reason.")],
                [("أعدتُ كتابة نصّك.", "اقترحتُ تعديلاً وتركتُ القرار لك.", "Rewriting the writer's text takes ownership that is not the editor's."),
                 ("هذا خطأ، صحّحه.", "هل يمكن أن نعيد الصياغة؟ السبب أنّ…", "In a professional edit, name the reason and let the writer decide.")]),
              [D("محرّر", "أعدتُ صياغة الفقرة الثالثة، هل تسمح؟", "aʿadtu ṣiyāghat al-faqra al-thālitha, hal tasmaḥ?", "I rephrased the third paragraph — may I?"),
               D("كاتب", "أفضّل أن يكون اقتراحاً، لا تعديلاً مباشراً.", "ufaḍḍil an yakūn iqtirāḥan, lā taʿdīlan mubāshiran.", "I prefer a suggestion rather than a direct edit."),
               D("محرّر", "منطقي، سأكتب السبب في الهامش.", "manṭiqī, sa-aktub al-sabab fī al-hāmish.", "Reasonable — I'll write the reason in the margin."),
               D("كاتب", "وشكراً لأنّك حفظتَ نسخة نظيفة.", "wa-shukran li-annaka ḥafiẓta nuskha naḍīfa.", "And thank you for keeping a clean copy.")],
              WS("Edit worksheet", [
                  T("Suggest, with a reason.", ["change «قال» to «أفاد»", "shorten the first sentence"],
                    ["اقتراح: «أفاد» أوضح هنا، لأنّ النصّ خبر رسمي", "اقتراح: اختصار الجملة الأولى يحفظ المعنى"]),
                  T("Hand it back.", ["the writer decides", "leave a margin comment"],
                    ["القرار النهائي لك", "تركتُ تعليقاً في الهامش مع السبب"]),
              ])),
        ]},
        {"id": "C1+-U2", "title": "Translation and register", "lessons": [
            L("Choosing a register before you translate",
              "Before the first word, decide the register: فصحى معاصرة (contemporary written), فصحى "
              "تراثية (classical, for legal and religious registers), or عامية for a subtitle. The same "
              "sentence has three correct translations and only one right one per job.",
              [V("فصحى معاصرة", "fuṣḥā muʿāṣira", "contemporary standard Arabic", "noun"),
               V("تراثية", "turāthiyya", "classical, heritage register", "noun"),
               V("المخاطَب", "al-mukhāṭab", "the addressee, audience", "noun"),
               V("مقصد", "maqṣad", "purpose, intent", "noun"),
               V("أسلوب", "uslūb", "style", "noun")],
              G("Register first, then words",
                "mukhāṭab + maqṣad → register → sentence",
                "«Please find attached» → للمخاطب الرسمي: نرفق لكم؛ لرسالة ودّية: أرسل لك المرفق. The "
                "audience and the purpose pick the register; the dictionary does not.",
                [X("للمخاطب الرسمي: نرفق لكم نسخة من الاتفاق.", "li-l-mukhāṭab al-rasmī: nurfiq lakum nuskha min al-ittifāq.", "For the formal addressee: we attach a copy of the agreement."),
                 X("لرسالة ودّية: أرسل لك الملف، راجعه وقت ما تحبّ.", "li-risāla wuddiyya: ursil lak al-milaff, rājiʿhu waqt mā tuḥibb.", "For a friendly message: here's the file, review it whenever you like."),
                 X("للترجمة القانونية: يُرفق طيّه نسخة موقّعة.", "li-l-tarjama al-qānūniyya: yurfaq ṭayyah nuskha muwaqqaʿa.", "For a legal translation: a signed copy is attached hereto.")],
                [("مترجم واحد لكل السياقات بأسلوب واحد.", "(register is chosen per job)", "One style for every job is the mark of a machine translation, not a translator."),
                 ("ترجمة حرفية دائماً أسلوب واحد.", "(name the mukhāṭab and maqṣad first)", "Literal fidelity is a decision, not a default.")]),
              [D("عميل", "أريد ترجمة الإعلان للمخاطب الخليجي.", "urīd tarjamat al-iʿlān li-l-mukhāṭab al-khalījī.", "I want the advertisement translated for a Gulf audience."),
               D("مترجمة", "إذاً فصحى معاصرة، وليست تراثية.", "idhan fuṣḥā muʿāṣira, wa-laysat turāthiyya.", "Then contemporary standard Arabic, not classical."),
               D("عميل", "وللعنوان؟", "wa-li-l-ʿunwān?", "And the headline?"),
               D("مترجمة", "العنوان يسمح بالعامية، لكنّ النصّ رسمي.", "al-ʿunwān yasmah bi-l-ʿāmmiyya, lākinna al-naṣṣ rasmī.", "The headline can take colloquial, but the body stays formal.")],
              WS("Register worksheet", [
                  T("Name the register.", ["a legal contract", "a friendly client email", "a news headline"],
                    ["فصحى تراثية / قانونية", "فصحى معاصرة ودّية", "فصحى معاصرة موجزة"]),
                  T("Translate the frame.", ["“please find attached” (formal)", "“here's the file” (friendly)"],
                    ["نرفق لكم", "أرسل لك المرفق"]),
              ])),
            L("Calques and false friends",
              "Translation traps hide in ordinary words: 'actually' is في الواقع, not فعلياً (which means "
              "literally); 'eventually' is في النهاية, not أحياناً; 'to assume' is يفترض, not يتّهم "
              "(accuse). A calque is grammatically correct and still not Arabic.",
              [V("في الواقع", "fī al-wāqiʿ", "actually, in fact", "phrase"),
               V("فعلياً", "fiʿliyyan", "in practice, de facto", "adverb"),
               V("يفترض", "yaftariḍ", "assumes", "verb"),
               V("يتّهم", "yattahim", "accuses", "verb"),
               V("ترجمة حرفية", "tarjama ḥarfiyya", "a literal translation", "phrase")],
              G("False friends to check",
                "actually → fī al-wāqiʿ · eventually → fī al-nihāya · assume → yaftariḍ · concrete (adj) → māddī",
                "هو في الواقع محقّ (he is actually right). في النهاية وصلنا (eventually we arrived). "
                "الخرسانة is concrete the material; ملموس is concrete as an adjective.",
                [X("في الواقع، لم يصل التقرير بعد.", "fī al-wāqiʿ, lam yaṣil al-taqrīr baʿd.", "Actually, the report has not arrived yet."),
                 X("في النهاية، اتّفقنا على سعر أقلّ.", "fī al-nihāya, ittafaqnā ʿalā siʿr aqall.", "Eventually we agreed on a lower price."),
                 X("لنفترض أنّ الأرقام صحيحة.", "li-naftariḍ anna al-arqām ṣaḥīḥa.", "Let us assume the figures are correct.")],
                [("فعلياً، لم يصل التقرير.", "في الواقع، لم يصل التقرير.", "فعلياً means 'in practice, de facto'; 'actually' is في الواقع."),
                 ("أحياناً وصلنا.", "في النهاية وصلنا.", "'Eventually' is not أحياناً (sometimes); it is في النهاية.")]),
              [D("مترجم", "كتبتُ: «هو في الواقع محقّ».", "katabtu: «huwa fī al-wāqiʿ muḥiqq».", "I wrote: 'he is actually right'."),
               D("محرّر", "جيدة، لكن لا تكتب فعلياً هنا.", "jayyida, lākin lā taktub fiʿliyyan hunā.", "Good — but don't write فعلياً here."),
               D("مترجم", "الفرق أنّ فعلياً تعني عملياً، صحيح؟", "al-farq anna fiʿliyyan taʿnī ʿamaliyyan, ṣaḥīḥ?", "The difference is that فعلياً means practically, right?"),
               D("محرّر", "تماماً، وفي الترجمة القانونية الفرق جوهر.", "tamāman, wa-fī al-tarjama al-qānūniyya al-farq jawhar.", "Exactly — and in legal translation the difference is the substance.")],
              WS("False-friend worksheet", [
                  T("Correct the calque.", ["فعلياً، أنا موافق.", "أحياناً سنصل غداً.", "يتّهم أنّ الأرقام صحيحة."],
                    ["في الواقع، أنا موافق", "في النهاية سنصل غداً", "يفترض أنّ الأرقام صحيحة"]),
                  T("Choose the word.", ["concrete evidence", "concrete the material", "a concrete proposal"],
                    ["أدلّة ملموسة", "الخرسانة", "اقتراح محدّد / ملموس"]),
              ])),
            L("Back-translation as a check",
              "The professional habit: translate your Arabic back into English and see what survived. "
              "If the back-translation drifts — certainty grew, politeness vanished, an actor appeared "
              "from nowhere — the first translation is wrong, not the second.",
              [V("الترجمة العكسية", "al-tarjama al-ʿaksiyya", "back-translation", "noun"),
               V("الأمانة", "al-amāna", "fidelity", "noun"),
               V("انحراف", "inḥirāf", "drift, deviation", "noun"),
               V("درجة اليقين", "darajat al-yaqīn", "degree of certainty", "noun"),
               V("مراجعة", "murājaʿa", "review, check", "noun")],
              G("Back-translate and compare",
                "translate → back-translate → compare certainty, politeness, actor",
                "نرجو التكرم بالاطلاع → 'we request you kindly review' → back: 'we request you kindly "
                "review' ✓. If 'perhaps' comes back as 'certainly', the drift is in the first direction.",
                [X("رجعتُ بالترجمة للتحقّق من درجة اليقين.", "rajaʿtu bi-l-tarjama li-l-taḥaqquq min darajat al-yaqīn.", "I back-translated to check the degree of certainty."),
                 X("لم يتغيّر المعنى، لكن تغيّرت النبرة.", "lam yataghayyar al-maʿnā, lākin taghayyarat al-nabra.", "The meaning did not change, but the tone did."),
                 X("هذا انحراف مقصود في العنوان، لا خطأ.", "hādhā inḥirāf maqṣūd fī al-ʿunwān, lā khaṭaʾ.", "This is a deliberate drift in the headline, not an error.")],
                [("الترجمة العكسية تحتاج قاموساً فقط.", "الترجمة العكسية تقارن النبرة ودرجة اليقين، لا المفردات فقط.", "Words survive back-translation easily; stance is what drifts."),
                 ("أعدتُ الترجمة، إذاً الترجمة صحيحة.", "أعدتُ الترجمة وقارنت ثلاث نقاط: اليقين، اللباقة، الفاعل.", "A back-translation is only useful with a checklist.")]),
              [D("محرّر", "هل راجعتِ الترجمة؟", "hal rājaʿti al-tarjama?", "Did you review the translation?"),
               D("مترجمة", "راجعتها بترجمة عكسية.", "rājaʿtuhā bi-tarjama ʿaksiyya.", "I reviewed it with a back-translation."),
               D("محرّر", "وماذا وجدتِ؟", "wa-mādhā wajadt?", "And what did you find?"),
               D("مترجمة", "المعنى سليم، لكن درجة اليقين ارتفعت في السطر الخامس.", "al-maʿnā salīm, lākin darajat al-yaqīn irtafaʿat fī al-saṭr al-khāmis.", "The meaning is sound, but the certainty rose in the fifth line.")],
              WS("Back-translation worksheet", [
                  T("Check three things.", ["certainty", "politeness", "who acts"],
                    ["درجة اليقين", "اللباقة", "الفاعل"]),
                  T("Say what drifted.", ["the tone changed", "the actor disappeared", "certainty grew"],
                    ["تغيّرت النبرة", "اختفى الفاعل في الترجمة", "ارتفعت درجة اليقين"]),
              ])),
        ]},
        {"id": "C1+-U3", "title": "Teaching what you know", "lessons": [
            L("Explain a rule: القاعدة، مثال، ملاحظة",
              "A rule explained in three moves sticks: القاعدة (the rule), مثال (an example), ملاحظة "
              "(the exception or warning). Arabic teaching texts, from the old grammars to a modern "
              "textbook, run on exactly this order.",
              [V("القاعدة", "al-qāʿida", "the rule", "noun"),
               V("مثال", "mithāl", "an example", "noun"),
               V("ملاحظة", "mulāḥaẓa", "a note, remark", "noun"),
               V("استثناء", "istithnāʾ", "an exception", "noun"),
               V("تمرين", "tamrīn", "an exercise", "noun")],
              G("Rule → example → note",
                "al-qāʿida: … · mithāl: … · mulāḥaẓa: …",
                "القاعدة: الفعل بعد لم يكون مجزوماً. مثال: لم يذهبْ. ملاحظة: لا تظهر السكون في الكتابة، "
                "لكنّها تُسمع في القراءة. Three lines, and the learner can use it before understanding it fully.",
                [X("القاعدة: أنّ تفتح الجملة بعد أفعال القول.", "al-qāʿida: أنّ tafthaḥ al-jumla baʿda afʿāl al-qawl.", "The rule: أنّ opens the clause after verbs of speech."),
                 X("مثال: قال إنّ الاجتماع تأجّل.", "mithāl: qāla inna al-ijtimāʿ taʾajjal.", "Example: he said that the meeting was postponed."),
                 X("ملاحظة: بعد «قال» تُستخدم إنّ، وبعد «أفاد» تُستخدم بأنّ.", "mulāḥaẓa: baʿda «qāla» tustakhdam inn, wa-baʿda «afāda» tustakhdam bi-ann.", "Note: after قال use إنّ; after أفاد use بأنّ.")],
                [("القاعدة: القاعدة صعبة.", "القاعدة: الفعل بعد لم يكون مجزوماً.", "A rule must state a pattern, not an opinion about the pattern."),
                 ("مثال: قال إنّ، ملاحظة: إنّ، وهكذا.", "(one worked example)", "Listing markers is not teaching; the example has to be a sentence.")]),
              [D("متعلّم", "ما الفرق بين إنّ وأنّ؟", "mā al-farq bayna inn wa-ann?", "What is the difference between إنّ and أنّ?"),
               D("معلّمة", "القاعدة: إنّ تفتح جملة مستقلّة، وأنّ تعمل داخل الجملة.", "al-qāʿida: inn tafthaḥ jumla mustaqilla, wa-ann taʿmal dākhil al-jumla.", "The rule: إنّ opens an independent sentence; أنّ works inside it."),
               D("متعلّم", "مثال؟", "mithāl?", "An example?"),
               D("معلّمة", "إنّ الجوّ جميل. أعلم أنّ الجوّ جميل.", "inna al-jaww jamīl. aʿlam anna al-jaww jamīl.", "إنّ الجوّ جميل. أعلم أنّ الجوّ جميل.")],
              WS("Teaching worksheet", [
                  T("Teach it in three moves.", ["لم + jussive", "b- after أرجو", "duals"],
                    ["القاعدة: الفعل بعد لم مجزوم · مثال: لم يذهبْ · ملاحظة: السكون لا يُكتب", "القاعدة: أرجو أن + فعل · مثال: أرجو أن تصل · ملاحظة: لا تُستخدم مع اسم", "القاعدة: المثنّى بـ -ان · مثال: كتابان · ملاحظة: -ين بعد الفعل"]),
                  T("Write the exercise.", ["three sentences to fix", "two to complete"],
                    ["صحّح: لم يذهبُ…", "أكمل: أرجو أن…"]),
              ])),
            L("Correct kindly: أحسنت، وهناك ملاحظة",
              "Correction that lands starts with what is right: أحسنت (well done), صحيح تقريباً, ثمّ "
              "ملاحظة صغيرة. Name the error once, show the fixed form, and let the learner say it back.",
              [V("أحسنت", "aḥsant", "well done", "phrase"),
               V("صحيح تقريباً", "ṣaḥīḥ taqrīban", "almost right", "phrase"),
               V("ملاحظة صغيرة", "mulāḥaẓa ṣaghīra", "a small note", "phrase"),
               V("أعد من فضلك", "aʿid min faḍlik", "say it again please", "phrase"),
               V("هذا أفضل", "hādhā afḍal", "that is better", "phrase")],
              G("Correction sandwich",
                "aḥsant → mulāḥaẓa ṣaghīra + the fix → aʿid min faḍlik → hādhā afḍal",
                "أحسنت! الجملة واضحة. ملاحظة صغيرة: نقول «ذهبتُ» لا «ذهبتُ أنا». أعد من فضلك. — هذا "
                "أفضل. The learner says the correct form out loud; that is the whole exercise.",
                [X("أحسنت، الفكرة وصلت بوضوح.", "aḥsant, al-fikra waṣalat bi-wuḍūḥ.", "Well done — the idea came across clearly."),
                 X("ملاحظة صغيرة: الترتيب يحتاج «إلى».", "mulāḥaẓa ṣaghīra: al-tartīb yaḥtāj «ilā».", "A small note: the structure needs إلى."),
                 X("أعد الجملة كاملة، ثمّ هذه أفضل.", "aʿid al-jumla kāmila, thumma hādhā afḍal.", "Say the whole sentence again — then that is better.")],
                [("خطأ، لم تفهم.", "صحيح تقريباً، ملاحظة صغيرة: …", "Naming a failure stops the learner; naming the fix moves them."),
                 ("أحسنت، لكن كل شيء خطأ.", "أحسنت في البدء، والملاحظة في الترتيب فقط.", "Praise followed by global contradiction cancels the praise.")]),
              [D("متعلّم", "ذهبتُ أنا إلى السوق أمس.", "dhahabtu anā ilā al-sūq ams.", "I went to the market yesterday."),
               D("معلّمة", "أحسنت! ملاحظة صغيرة: نقول «ذهبتُ» دون «أنا».", "aḥsant! mulāḥaẓa ṣaghīra: naqūl «dhahabtu» dūn «anā».", "Well done! A small note: we say ذهبتُ without أنا."),
               D("متعلّم", "ذهبتُ إلى السوق أمس.", "dhahabtu ilā al-sūq ams.", "I went to the market yesterday."),
               D("معلّمة", "هذا أفضل، أعدها مرة أخيرة بصوت واضح.", "hādhā afḍal, aʿidhā marra akhīra bi-ṣawt wāḍiḥ.", "That's better — say it one last time clearly.")],
              WS("Correction worksheet", [
                  T("Correct kindly.", ["«أنا اسمي منى أنا»", "«مرحبا عليكم»"],
                    ["أحسنت، ملاحظة صغيرة: اسمي منى — دون «أنا» الثانية", "أحسنت، لكن التحية الزوجية: السلام عليكم"]),
                  T("Close the loop.", ["ask them to repeat", "praise the fix"],
                    ["أعد من فضلك", "هذا أفضل، ممتاز"]),
              ])),
            L("Roots and patterns instead of rote",
              "Arabic rewards the learner who sees the root. ك-ت-ب gives كتب، كاتب، مكتوب، كتاب، مكتبة. "
              "Teach the root once and the vocabulary multiplies — and warn about the trap: Latin "
              "transliteration cannot carry what the script already does.",
              [V("الجذر", "al-jadhr", "the root", "noun"),
               V("الوزن", "al-wazn", "the pattern", "noun"),
               V("مشتقّات", "mushtaqqāt", "derived forms", "noun"),
               V("مفردات", "mufradāt", "vocabulary", "noun"),
               V("حروف لاتينية", "ḥurūf lātīniyya", "Latin letters", "phrase")],
              G("Root + pattern = family",
                "jadhr k-t-b: kataba (write) · kātib (writer) · maktūb (written) · kitāb (book) · maktaba (library)",
                "علّم الجذر مرة، وستحصل على عائلة كاملة. And the warning: كتابة العربية بالحروف "
                "اللاتينية تفقد التمييز بين حروف لا تفرّقها اللاتينية — ت and ط, س and ص, ح and ه.",
                [X("الجذر ك-ت-ب يعطي عائلة كاملة من الكلمات.", "al-jadhr k-t-b yuʿṭī ʿāʾila kāmila min al-kalimāt.", "The root k-t-b gives a whole family of words."),
                 X("الوزن مفعول يعطي اسم المفعول.", "al-wazn mafʿūl yuʿṭī ism al-mafʿūl.", "The pattern mafʿūl gives the passive participle."),
                 X("لا تعلّم بالحروف اللاتينية من البداية.", "lā tuʿallim bi-l-ḥurūf al-lātīniyya min al-bidāya.", "Don't teach with Latin letters from the start.")],
                [("تعلّم كل كلمة على حدة.", "تعلّم الجذر والعائلة.", "Word-by-word learning is slow; the root multiplies by five."),
                 ("اكتب العربية بالحروف اللاتينية ليتعلّم أسرع.", "ابدأ بالحروف العربية، واستخدم النطق مساعداً فقط.", "Latin transliteration hides the distinctions the script teaches.")]),
              [D("متعلّم", "كيف أحفظ المفردات؟", "kayfa aḥfaẓ al-mufradāt?", "How do I memorise vocabulary?"),
               D("معلّمة", "ابدأ من الجذر، لا من الكلمة وحدها.", "ibdaʾ min al-jadhr, lā min al-kalima waḥdahā.", "Start from the root, not from the word alone."),
               D("متعلّم", "مثال؟", "mithāl?", "For example?"),
               D("معلّمة", "ك-ت-ب: كتاب، كاتب، مكتبة، مكتوب — عائلة واحدة.", "k-t-b: kitāb, kātib, maktaba, maktūb — ʿāʾila wāḥida.", "k-t-b: book, writer, library, written — one family.")],
              WS("Root worksheet", [
                  T("Build the family.", ["root د-ر-س", "root ع-ل-م"],
                    ["درس، مدرسة، مدرّس، دراسة", "علم، معلومة، معلّم، تعليم"]),
                  T("Warn about the trap.", ["Latin letters and ت/ط", "Latin letters and س/ص"],
                    ["اللاتينية لا تفرّق بين ت وط", "اللاتينية لا تفرّق بين س وص"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Arabic writing for work is a craft with its own etiquette: formulas open and close the "
                 "text, the passive and the verbal noun carry institutional distance, and a translator "
                 "is expected to choose a register before choosing words. The oldest continuous "
                 "translation tradition in the region — Baghdad's House of Wisdom — is remembered for "
                 "exactly the habit this level teaches: render the meaning, then argue about the wording."),
        source_url="https://en.wikipedia.org/wiki/House_of_Wisdom",
        reading=("تجدر الإشارة إلى أنّ نصّ البيان يحتاج ضبطاً في درجة اليقين: «تؤكّد الوزارة» غير «تشير "
                 "مصادر». وقد لاحظ المراجع أنّ الفعل «قال» تكرّر خمس مرّات، والأفضل تنويعه: أفاد، صرّح، "
                 "نقل عن. أمّا العنوان فيسمح بحرية أكبر، بشرط ألّا يوحي بما لا يقوله النصّ."),
        reading_gloss=("It is worth noting that the text of the statement needs its degree of certainty "
                       "fixed: 'the ministry confirms' is not 'sources indicate'. The reviewer observed "
                       "that the verb 'said' was repeated five times, and it is better to vary it: "
                       "reported, declared, quoted. The headline, however, allows more freedom — "
                       "provided it does not suggest what the text does not say."),
        listening=("أ: لماذا غيّرتَ «أحسنت» في التعليق؟<br>ب: لأنّ المتعلّم أخطأ في الترتيب فقط، والمدح "
                   "العامّ لا يعلّمه.<br>أ: إذاً تدريج: قاعدة، مثال، ملاحظة.<br>ب: تماماً، ومع تكرار "
                   "المتعلّم للصيغة الصحيحة."),
        listening_gloss=("A: Why did you change 'well done' in the comment? B: Because the learner only "
                         "erred in word order, and blanket praise does not teach. A: So the ladder: rule, "
                         "example, note. B: Exactly — with the learner repeating the correct form."),
        voice_tag=VOICE,
        idioms=[
            ("حسن الصياغة", "goodness of wording", "well put"),
            ("على قياس واحد", "on one measure", "by the same standard"),
            ("في هذا السياق", "in this context", "in this connection"),
            ("من باب الدقّة", "from the door of precision", "for precision's sake"),
            ("لا يخلو من صواب", "it is not free of correctness", "there is something to it"),
            ("ربّ قائل", "many a speaker", "many a person says"),
            ("على حدّ علمي", "to the limit of my knowledge", "to the best of my knowledge"),
            ("بحسب ما وصلني", "according to what reached me", "as far as I have heard"),
            ("بأمانة", "with fidelity", "faithfully, honestly"),
            ("كما هو معروف", "as is known", "as is well known"),
        ],
        mistakes=[
            ("أعدتُ كتابة نصّك لأنه ضعيف.", "اقترحتُ تعديلاً مع السبب، والقرار لك.", "An edit without consent takes ownership the editor does not have."),
            ("فعلياً، لم يصل التقرير.", "في الواقع، لم يصل التقرير.", "'Actually' is في الواقع; فعلياً means in practice, de facto."),
            ("تعلّم المفردات كلمة كلمة أسرع.", "تعلّم من الجذر: ك-ت-ب يعطي عائلة كاملة.", "Root-based learning multiplies vocabulary; single words have to be memorised one by one."),
        ],
        task_title="Teach the lesson you learned last week",
        task_instructions=("Take one Arabic rule you learned this month. Write it as القاعدة / مثال / "
                           "ملاحظة, add one exercise with three items, and one correction script that "
                           "starts with أحسنت. Then teach it out loud to someone for five minutes and "
                           "watch where they stumble — that sentence, not your note, is the lesson."),
    ),
    "test": [
        ("translate_en", "Say: This is a suggested edit; the final call is yours.", "هذا اقتراح تعديل، والتعديل النهائي لك."),
        ("translate_ar", "لا يسري هذا الحكم على العقود السابقة.", "This provision does not apply to previous contracts."),
        ("multiple_choice", "Which section proposes?", "التوصيات"),
        ("fill_in_the_blank", "اقتراح: «أفاد» أوضح ___ «قال» هنا. (than)", "من"),
        ("word_selection", "Select the Arabic for 'actually'.", "في الواقع"),
        ("error_correction", "قامت الوزارة بتنفيذ الخطة.", "نفّذت الوزارة الخطة."),
        ("dialogue_completion", "Complete: ملاحظة صغيرة: ___ (the verb and the silence)", "يكون مجزوماً بعد لم"),
        ("matching", "Match الترجمة العكسية to its meaning.", "back-translation"),
        ("reading_comprehension", "«تؤكّد الوزارة» غير «تشير مصادر». Which is stronger?", "the ministry confirms"),
        ("inference", "«العنوان يسمح بحرية أكبر، بشرط ألّا يوحي بما لا يقوله النصّ» — what is the limit?", "the headline must not imply more than the text says"),
        ("main_idea", "القاعدة: إنّ تفتح جملة مستقلّة. What is being taught?", "the difference between إنّ and أنّ"),
        ("detail_identification", "الجذر ك-ت-ب يعطي: كتاب، كاتب، مكتبة. What is the teaching point?", "one root yields a family of words"),
    ],
}

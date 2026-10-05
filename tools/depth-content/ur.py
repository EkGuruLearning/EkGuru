# -*- coding: utf-8 -*-
"""Urdu Phase 1 depth: authored extras, third lessons and five half-steps.

The course uses Urdu in its Nastaliq script and the established plain-ASCII
romanisation used by A2 and above. Romanisation is a learner bridge, not IPA;
register and agreement need human review. This module creates unreviewed content
drafts and never writes a native-review record.
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from depth_kit import D, EXTRA, G, L, T, V, WS, X

CODE = "ur"
NAME = "Urdu"
NATIVE = "اردو"
PHASE = 2
SCRIPT = "Nastaliq script"
VOICE = "ur-PK"
SKILL = ("Urdu: right-to-left Nastaliq reading, احترام کے صیغے آپ/تم, postpositions, "
         "gender and honorific agreement, clause linking, and source-aware formal prose")


def _lesson(title, aim, words, grammar, examples, mistake, worksheet):
    vocab = [V(*row) for row in words]
    ex = [X(*row) for row in examples]
    gtitle, pattern, explain = grammar
    dialogue = [
        D("استاد", *examples[0]),
        D("طالب علم", *examples[1]),
        D("استاد", *examples[2]),
        D("طالب علم", *examples[1]),
    ]
    tasks = [
        T("Translate the first model into English.", [examples[0][0]], [examples[0][2]]),
        T("Use the lesson pattern in a new sentence.", [examples[1][0], examples[2][0]],
          [examples[1][2], examples[2][2]]),
    ]
    return L(title, aim, vocab, G(gtitle, pattern, explain, ex, [mistake]), dialogue,
             WS(worksheet, tasks))


def _extra(culture, source, reading, gloss, listening, listening_gloss,
           idioms, mistakes, title, instructions):
    return EXTRA(culture, source, reading, gloss, listening, listening_gloss,
                 VOICE, idioms, mistakes, title, instructions)


# Expressions are recycled only between adjacent stages so learners can retrieve
# them in a new context. The surrounding readings, listening and tasks differ.
IDIOMS = {
    "A1": [
        ("ہاتھ بٹانا", "to lend a hand", "to help with a task"),
        ("دل سے", "from the heart", "sincerely"),
        ("کوئی بات نہیں", "it is no matter", "no problem; you are welcome"),
        ("وقت پر", "on time", "at the agreed time"),
        ("ایک لمحہ", "one moment", "please wait briefly"),
        ("خوش آمدید", "welcome", "a warm welcome"),
        ("ذرا دیکھیے", "please have a look", "a courteous request to look"),
        ("ٹھیک ہے", "it is all right", "agreement or acceptance"),
        ("راستہ پوچھنا", "to ask the way", "to request directions"),
        ("خیریت سے", "in well-being", "safely, without trouble"),
    ],
    "A2": [
        ("جان میں جان آنا", "life returning to the body", "to feel relieved"),
        ("بات بننا", "the matter taking shape", "for a plan to work out"),
        ("دل لگانا", "to attach the heart", "to become engaged or interested"),
        ("ہاتھ سے نکلنا", "to leave the hand", "to get out of control"),
        ("آنکھ بچا کر", "while avoiding the eye", "without being noticed"),
        ("سر درد بننا", "to become a headache", "to become a troublesome problem"),
        ("وقت نکالنا", "to take time out", "to make time for something"),
        ("خیال رکھنا", "to keep a thought", "to take care"),
        ("کام آنا", "to come into use", "to be useful"),
        ("آگاہ کرنا", "to make aware", "to inform someone"),
    ],
    "B1": [
        ("کان دھرنا", "to lend an ear", "to listen attentively"),
        ("دل چھوٹا کرنا", "to make the heart small", "to become discouraged"),
        ("بات کا بتنگڑ بنانا", "to make a molehill a mountain", "to exaggerate an issue"),
        ("رائے قائم کرنا", "to establish an opinion", "to form a view"),
        ("ذمہ داری اٹھانا", "to lift responsibility", "to take responsibility"),
        ("پیش نظر رکھنا", "to keep before the eyes", "to keep in mind"),
        ("نتیجہ نکالنا", "to draw a result", "to reach a conclusion"),
        ("رابطہ رکھنا", "to keep contact", "to stay in touch"),
        ("بات سمجھ میں آنا", "the matter entering understanding", "to understand"),
        ("قدم اٹھانا", "to lift a step", "to take action"),
    ],
    "B2": [
        ("مدنظر رکھنا", "to keep in view", "to take into account"),
        ("نکتہ اٹھانا", "to raise a point", "to raise an issue"),
        ("رائے سے اختلاف کرنا", "to differ with a view", "to disagree with an opinion"),
        ("پہلو اجاگر کرنا", "to make a side prominent", "to highlight an aspect"),
        ("حد مقرر کرنا", "to set a limit", "to define a boundary"),
        ("وجہ بیان کرنا", "to state a reason", "to explain why"),
        ("نتیجہ اخذ کرنا", "to infer a result", "to draw a conclusion"),
        ("توجہ دلانا", "to draw attention", "to point something out"),
        ("عملی صورت دینا", "to give a practical form", "to put into practice"),
        ("ازسرِنو جائزہ", "review anew", "a fresh review"),
    ],
    "C1": [
        ("زیرِ بحث", "under discussion", "currently being discussed"),
        ("حرفِ آخر", "the final word", "a definitive statement"),
        ("لبِ لباب", "the lip of the lip", "the essence or summary"),
        ("من و عن", "exactly as it is", "without alteration"),
        ("بادی النظر میں", "at first sight", "at first glance"),
        ("بہرصورت", "in every case", "in any event"),
        ("اس تناظر میں", "in this context", "in this frame of reference"),
        ("قابلِ توجہ", "worthy of attention", "noteworthy"),
        ("مفروضہ قائم کرنا", "to establish a hypothesis", "to formulate an assumption"),
        ("نتائج اخذ کرنا", "to infer results", "to draw findings"),
    ],
    "C2": [
        ("بالمقابل", "by comparison", "on the other hand"),
        ("بغیر کسی ابہام کے", "without ambiguity", "unambiguously"),
        ("بہر کیف", "in any case", "nevertheless; in any event"),
        ("بالواسطہ اشارہ", "an indirect indication", "an implication or hint"),
        ("حدِ امکان", "the limit of possibility", "the extent that is feasible"),
        ("سیاق و سباق", "context and setting", "the surrounding context"),
        ("دائرۂ کار", "circle of work", "scope"),
        ("ازروئے شواہد", "in view of evidence", "on the available evidence"),
        ("حتمی رائے", "a final opinion", "a definitive judgment"),
        ("مفہوم متعین کرنا", "to determine meaning", "to define an interpretation"),
    ],
}

ERRORS = {
    "A1": [
        ("آپ کہاں ہے؟", "آپ کہاں ہیں؟", "Respectful آپ normally takes the honorific/plural verb ہیں."),
        ("میں ٹھیک ہے۔", "میں ٹھیک ہوں۔", "The first-person copula is ہوں, not ہے."),
        ("مجھے اردو سیکھتا ہوں۔", "میں اردو سیکھتا/سیکھتی ہوں۔", "The learner is the subject; match the verb to the speaker."),
    ],
    "A2": [
        ("میں ڈاکٹر کو وقت پوچھا۔", "میں نے ڈاکٹر سے وقت پوچھا۔", "Use سے for asking a person; past transitive Urdu commonly marks the subject with نے."),
        ("وہ کل آتا ہے۔", "وہ کل آئے گا/گی۔", "A future-time plan needs a future form, with agreement to the speaker described."),
        ("مجھے دوا پینا ہے۔", "مجھے دوا لینی ہے۔", "Urdu uses the natural collocation دوا لینا for taking medicine."),
    ],
    "B1": [
        ("کیونکہ بارش ہوئی، اس لیے ہم دیر سے پہنچے۔", "بارش ہوئی، اس لیے ہم دیر سے پہنچے۔", "Avoid stacking causal conjunctions when one clear link is enough."),
        ("اس نے کہا کہ وہ آتا ہے کل۔", "اس نے کہا کہ وہ کل آئے گا/گی۔", "Place the time phrase naturally and keep reported time consistent."),
        ("ہم نے مسئلہ حل کیا گیا۔", "ہم نے مسئلہ حل کیا۔", "Do not combine an active subject marker with a passive construction."),
    ],
    "B2": [
        ("اگرچہ منصوبہ مفید ہے، لیکن مگر مہنگا ہے۔", "اگرچہ منصوبہ مفید ہے، مگر مہنگا ہے۔", "Choose one contrast linker rather than stacking alternatives."),
        ("اعداد اس بات کو ثابت ہیں۔", "اعداد اس بات کی تائید کرتے ہیں۔", "Use an idiomatic evidence verb and avoid claiming proof beyond the data."),
        ("آپ کی رائے غلط ہے، اس لیے میں اختلاف کرتا ہوں۔", "میں اس نکتے سے مختلف نتیجہ اخذ کرتا ہوں۔", "Disagree with a claim precisely instead of dismissing the person."),
    ],
    "C1": [
        ("رپورٹ نے کہا کہ اثر ہر جگہ یکساں ہے۔", "رپورٹ کے مطابق اثر علاقوں کے لحاظ سے مختلف ہے۔", "Attribute a claim to the report and preserve its qualification."),
        ("یہ ثابت کرتا ہے کہ ہر فرد ایسا کرتا ہے۔", "یہ نمونہ اس رجحان کی طرف اشارہ کرتا ہے۔", "A limited sample does not establish a universal claim."),
        ("میں آپ کو رد کرتا ہوں۔", "میں اس تعبیر کے دائرے کو محدود کرنا چاہتا ہوں۔", "A diplomatic correction addresses the interpretation, not the person."),
    ],
    "C2": [
        ("خاموشی کا مطلب ضرور اتفاق ہے۔", "خاموشی کو اتفاق کا قطعی ثبوت نہیں سمجھنا چاہیے۔", "Silence alone does not prove agreement; mark the inference as uncertain."),
        ("یہ فیصلہ ہی مسئلہ کی وجہ تھا۔", "مسئلہ فیصلے کے نفاذ کے طریقے سے پیدا ہوا۔", "Use focus carefully to distinguish a decision from how it was implemented."),
        ("شواہد کے مطابق یہ حتمی طور پر درست ہے۔", "دستیاب شواہد کی روشنی میں یہ ایک قرینِ قیاس تعبیر ہے۔", "Calibrate certainty to the evidence and avoid an absolute verdict."),
    ],
}

BASE_EXTRA_ROWS = {
    "A1": ("Urdu is written from right to left in a connected Perso-Arabic script. Letter shapes can change with position, while short vowels are often not written in ordinary text. Learners benefit from reading complete, familiar words rather than treating each joined shape as a separate letter. Spoken forms and conventions vary across regions and communities.",
           "https://www.unicode.org/versions/latest/core-spec/chapter-9/",
           "میرا نام سارہ ہے۔ میں اردو پڑھتی ہوں۔ استاد ایک لفظ تختے پر لکھتے ہیں۔ میں لفظ کو دائیں سے بائیں پڑھتی ہوں اور اپنی کاپی میں لکھتی ہوں۔ پھر میں استاد سے اس کا مطلب پوچھتی ہوں۔",
           "My name is Sara. I study Urdu. The teacher writes a word on the board. I read it from right to left and write it in my notebook. Then I ask the teacher what it means.",
           "استاد: السلام علیکم، آپ کا نام کیا ہے؟<br>طالب علم: میرا نام سارہ ہے۔<br>استاد: کیا آپ یہ لفظ پڑھ سکتی ہیں؟<br>طالب علم: جی، مگر اس کا مطلب بتائیے۔",
           "Teacher: Hello, what is your name? Student: My name is Sara. Teacher: Can you read this word? Student: Yes, but please tell me what it means.",
           "A1"),
    "A2": ("Urdu distinguishes familiar and respectful address. آپ is widely used for polite address and normally takes honorific agreement; تم is more familiar, but the choice depends on relationship, setting and local practice. A learner should not copy one address form into every conversation.",
           "https://www.britannica.com/topic/Urdu-language",
           "کل عائشہ نے کلینک کو فون کیا۔ اس نے ڈاکٹر سے وقت مانگا اور اپنی علامات بتائیں۔ استقبالیہ نے جمعرات کا وقت دیا۔ عائشہ نے وقت لکھ لیا اور پوچھا کہ رپورٹ ساتھ لانی ہے یا نہیں۔",
           "Yesterday Ayesha called the clinic. She asked the doctor for an appointment and described her symptoms. Reception gave her a Thursday appointment. Ayesha wrote down the time and asked whether she should bring the report.",
           "عائشہ: کیا جمعرات کو ڈاکٹر سے مل سکتی ہوں؟<br>استقبالیہ: جی، دس بجے ایک وقت خالی ہے۔<br>عائشہ: شکریہ، میں رپورٹ بھی لے آؤں گی۔<br>استقبالیہ: براہ کرم اپنا نام لکھوا دیجیے۔",
           "Ayesha: Can I see the doctor on Thursday? Reception: Yes, there is an opening at ten. Ayesha: Thank you, I will bring the report too. Reception: Please give us your name.",
           "A2"),
    "B1": ("Urdu's everyday vocabulary includes words with different histories and registers. Persian- and Arabic-derived words are common in formal writing, while speakers may choose shorter everyday alternatives in conversation. Neither register is a measure of a speaker's intelligence; select words for audience and purpose, and note regional variation.",
           "https://www.britannica.com/topic/Urdu-language",
           "کمیٹی نے پہلے مقامی رہائشیوں کی بات سنی، پھر پانی کی فراہمی کے اعداد دیکھے۔ ایک رکن نے بتایا کہ دو محلوں میں دباؤ کم ہے۔ دوسرے رکن نے تجویز دی کہ اگلی میٹنگ سے پہلے مزید پیمائش کی جائے۔",
           "The committee first listened to local residents and then reviewed water-supply figures. One member reported low pressure in two neighbourhoods. Another suggested taking more measurements before the next meeting.",
           "رکن اول: کیا اعداد دونوں محلوں کی صورتِ حال دکھاتے ہیں؟<br>رکن دوم: ابھی نہیں؛ ایک جگہ کا نمونہ کم ہے۔<br>رکن اول: پھر نتیجہ عارضی لکھتے ہیں۔<br>رکن دوم: جی، اور اگلی میٹنگ میں نئی پیمائش دیکھیں گے۔",
           "Member one: Do the figures show the situation in both neighbourhoods? Member two: Not yet; the sample from one area is small. Member one: Then we will label the conclusion provisional. Member two: Yes, and review new measurements at the next meeting.",
           "B1"),
    "B2": ("Urdu public and professional writing uses several ways to signal respect, distance and disagreement. A careful writer can challenge a claim while acknowledging the other person's proposal. Formal phrases should not be copied blindly into a family conversation, where a shorter, warmer expression may fit better.",
           "https://www.britannica.com/topic/Urdu-language",
           "محکمہ نے منصوبے کے نتائج جاری کیے، مگر رپورٹ میں ایک حد بھی لکھی۔ صرف تین علاقوں سے معلومات جمع ہوئی تھیں۔ مصنف نے اس لیے سفارش کی کہ اگلے مرحلے میں مزید علاقوں کو شامل کیا جائے۔",
           "The department released the project's results, but the report also stated a limitation. Information had been collected from only three areas. The author therefore recommended including more areas in the next stage.",
           "محرر: کیا ہم سفارش کو حتمی فیصلہ لکھیں؟<br>محقق: بہتر ہے اسے دستیاب نمونے سے وابستہ رکھیں۔<br>محرر: میں یہ حد واضح کر دوں گا۔<br>محقق: شکریہ، اس سے دعویٰ درست حد میں رہے گا۔",
           "Editor: Should we write the recommendation as a final decision? Researcher: It is better to tie it to the available sample. Editor: I will make that limitation clear. Researcher: Thank you; that will keep the claim within its proper scope.",
           "B2"),
    "C1": ("Advanced Urdu prose can shift between a direct account, a source-attributed claim and an interpretation. These are different evidence levels. A reader should be able to tell which details were observed, which came from a report and which are the writer's inference. This distinction is useful in academic and public communication.",
           "https://www.britannica.com/topic/Urdu-language",
           "دونوں مطالعات کو ساتھ پڑھنے سے ایک فرق سامنے آتا ہے۔ پہلی تحقیق نے شہری علاقوں کو دیکھا، جبکہ دوسری نے دیہی مراکز کا جائزہ لیا۔ اس لیے نتائج میں فرق کو صرف طریقۂ کار سے منسوب نہیں کیا جا سکتا؛ نمونے کا سیاق بھی اہم ہے۔",
           "Reading the two studies together reveals a difference. The first study examined urban areas, while the second reviewed rural centres. The difference in results therefore cannot be attributed only to method; the context of the sample also matters.",
           "محقق: کیا یہ دونوں نتائج ایک دوسرے کی تردید کرتے ہیں؟<br>محرر: ضروری نہیں؛ ان کے نمونے مختلف ہیں۔<br>محقق: پھر خلاصے میں یہ فرق واضح ہونا چاہیے۔<br>محرر: جی، میں دونوں نتائج کو ان کے سیاق کے ساتھ بیان کروں گا۔",
           "Researcher: Do these findings contradict one another? Editor: Not necessarily; their samples differ. Researcher: Then the summary should make that difference clear. Editor: Yes, I will report both findings with their contexts.",
           "C1"),
    "C2": ("Expert Urdu writing often signals how far a conclusion reaches. A plausible reading is not the same as a proven fact, and a pause or omission is not proof of a speaker's intention. Skilled mediation names the evidence, leaves room for uncertainty and avoids turning cultural conventions into universal rules.",
           "https://www.britannica.com/topic/Urdu-language",
           "بیان میں لفظ 'ممکن ہے' ایک حد قائم کرتا ہے۔ یہ دستیاب شواہد سے ایک قابلِ قبول تعبیر پیش کرتا ہے، مگر اسے آخری فیصلہ نہیں بناتا۔ مدیر نے اسی لیے اگلے جملے میں نمونے کی کمی درج کی، تاکہ قاری نتیجے کی بنیاد بھی دیکھ سکے۔",
           "The phrase 'it is possible' sets a limit in the statement. It offers a plausible interpretation from available evidence without making it a final verdict. The editor therefore recorded the sample's limitation in the next sentence so readers could see the basis of the conclusion.",
           "ماہر: کیا خاموشی سے رضامندی ثابت ہوتی ہے؟<br>محرر: نہیں؛ یہ ایک ممکنہ اشارہ ہے، قطعی ثبوت نہیں۔<br>ماہر: پھر متن میں اس کا درجہ واضح رکھیں۔<br>محرر: میں اسے تعبیر کے طور پر لکھوں گا، حقیقت کے طور پر نہیں۔",
           "Expert: Does silence prove consent? Editor: No; it may be a signal, but it is not decisive proof. Expert: Then keep its status clear in the text. Editor: I will present it as an interpretation, not a fact.",
           "C2"),
}


def _make_extra(row, pool):
    culture, source, reading, gloss, listening, listening_gloss, stage = row
    return _extra(culture, source, reading, gloss, listening, listening_gloss,
                  IDIOMS[stage], ERRORS[stage],
                  "Urdu " + stage + " reflection and production task",
                  "Write a short response using two expressions from this level. State the audience, keep the address form consistent, and mark which claim is observed, reported or inferred. Read it aloud once and revise any phrase that overstates the evidence.")


EXTRAS = {rung: _make_extra(row, IDIOMS[row[-1]]) for rung, row in BASE_EXTRA_ROWS.items()}

# Third lessons: one new, source-authored lesson in each of the three existing
# units at every CEFR rung.  The rows are (title, aim, vocabulary, grammar,
# examples, mistake, worksheet title).
THIRD_SEEDS = {
    "A1": [
        ("Read a classroom sign", "Recognise common classroom objects and ask someone to repeat a word.",
         [("حرف", "harf", "letter"), ("لفظ", "lafz", "word"), ("تختہ", "takhta", "board"), ("کاپی", "kaapi", "notebook"), ("دوبارہ", "dobara", "again")],
         ("polite request with براہ کرم", "براہ کرم + verb + دیجیے", "Use براہ کرم with a respectful request. The verb form دیجیے is a polite imperative."),
         [("براہ کرم یہ لفظ دوبارہ لکھیے۔", "barah karam ye lafz dobara likhiye.", "Please write this word again."), ("میں اسے اپنی کاپی میں لکھتی ہوں۔", "main ise apni kaapi mein likhti hun.", "I am writing it in my notebook."), ("کیا آپ اس حرف کی آواز بتا سکتے ہیں؟", "kya aap is harf ki aawaz bata sakte hain?", "Can you tell me the sound of this letter?")],
         ("آپ یہ لفظ دوبارہ لکھو۔", "آپ یہ لفظ دوبارہ لکھیے۔", "A respectful request with آپ uses the polite imperative لکھیے."), "Ask about a written word"),
        ("Order a simple snack", "Name a drink and food item, then make a courteous request.",
         [("چائے", "chaay", "tea"), ("پانی", "paani", "water"), ("روٹی", "roti", "bread"), ("نمک", "namak", "salt"), ("براہ کرم", "barah karam", "please")],
         ("request with دیجیے", "item + دیجیے", "A respectful imperative is a practical way to request an item. Add براہ کرم to soften the request."),
         [("براہ کرم ایک کپ چائے دیجیے۔", "barah karam ek cup chaay dijiye.", "Please give me a cup of tea."), ("مجھے پانی بھی چاہیے۔", "mujhe paani bhi chahiye.", "I would also like water."), ("روٹی میں نمک کم ہے۔", "roti mein namak kam hai.", "The bread has little salt.")],
         ("مجھے پانی بھی چاہتا ہوں۔", "مجھے پانی بھی چاہیے۔", "چاہیے expresses a need; the experiencer is marked with مجھے."), "Order food courteously"),
        ("Ask where a place is", "Ask for a nearby place and understand a short location answer.",
         [("اسٹیشن", "station", "station"), ("بازار", "bazaar", "market"), ("قریب", "qareeb", "near"), ("کہاں", "kahan", "where"), ("سامنے", "saamne", "in front")],
         ("question word and ہے", "place + کہاں ہے؟", "Put کہاں in the location question. The verb ہے agrees with the singular place being located."),
         [("اسٹیشن کہاں ہے؟", "station kahan hai?", "Where is the station?"), ("بازار یہاں سے قریب ہے۔", "bazaar yahan se qareeb hai.", "The market is near here."), ("دکان اسٹیشن کے سامنے ہے۔", "dukaan station ke saamne hai.", "The shop is in front of the station.")],
         ("اسٹیشن کہاں ہیں؟", "اسٹیشن کہاں ہے؟", "A singular place takes ہے in this question."), "Locate a place"),
    ],
    "A2": [
        ("Confirm a clinic appointment", "Ask for an appointment time and confirm what to bring.",
         [("وقت", "waqt", "time"), ("ملاقات", "mulaqat", "appointment"), ("رپورٹ", "report", "report"), ("جمعرات", "jumeraat", "Thursday"), ("لانا", "laana", "to bring")],
         ("future intention", "میں + item + لے آؤں گا/گی", "The future form changes with the speaker's gender; include both forms in a learner's notes."),
         [("کیا جمعرات کو وقت خالی ہے؟", "kya jumeraat ko waqt khaali hai?", "Is there an opening on Thursday?"), ("میں اپنی رپورٹ لے آؤں گی۔", "main apni report le aaungi.", "I will bring my report."), ("ملاقات کا وقت لکھ لیجیے۔", "mulaqat ka waqt likh lijiye.", "Please write down the appointment time.")],
         ("میں رپورٹ لے آیا گی۔", "میں رپورٹ لے آؤں گی۔", "The feminine future form is لے آؤں گی; the masculine is لے آؤں گا."), "Prepare for a visit"),
        ("Write a clear office update", "Give a short progress update and name the next step.",
         [("کام", "kaam", "work"), ("فائل", "file", "file"), ("مکمل", "mukammal", "complete"), ("اگلا", "agla", "next"), ("بھیجنا", "bhejna", "to send")],
         ("sequencing with پہلے / پھر", "پہلے + action؛ پھر + action", "Use پہلے and پھر to present steps in order. A brief update is easier to follow when the next action is explicit."),
         [("میں نے فائل مکمل کر لی ہے۔", "main ne file mukammal kar li hai.", "I have completed the file."), ("پہلے اسے پڑھوں گا، پھر بھیجوں گا۔", "pehle ise parhunga, phir bhejunga.", "I will read it first and then send it."), ("اگلا مرحلہ کل شروع ہوگا۔", "agla marhala kal shuru hoga.", "The next stage will begin tomorrow.")],
         ("میں نے فائل مکمل کر لیا ہے۔", "میں نے فائل مکمل کر لی ہے۔", "فائل is feminine, so the participle agrees with it in this construction."), "Send a progress note"),
        ("Invite a neighbour to a gathering", "Accept or decline an invitation politely and suggest another time.",
         [("دعوت", "dawat", "invitation"), ("پڑوسی", "parosi", "neighbour"), ("شام", "shaam", "evening"), ("مصروف", "masroof", "busy"), ("اگلے ہفتے", "agle hafte", "next week")],
         ("reason and alternative", "اگر ... تو ...؛ کیا ...؟", "Give a brief reason, then offer a concrete alternative instead of leaving the invitation unanswered."),
         [("آپ کی دعوت کا شکریہ۔", "aap ki dawat ka shukriya.", "Thank you for your invitation."), ("میں آج شام مصروف ہوں۔", "main aaj shaam masroof hun.", "I am busy this evening."), ("کیا ہم اگلے ہفتے مل سکتے ہیں؟", "kya hum agle hafte mil sakte hain?", "Can we meet next week?")],
         ("میں دعوت پر نہیں آ سکتا کیونکہ میں مصروف تھا ہوں۔", "میں آج نہیں آ سکتا کیونکہ میں مصروف ہوں۔", "Keep the reason in the same time frame as today."), "Reply to an invitation"),
    ],
    "B1": [
        ("Separate a report from your inference", "Summarise a report and clearly mark one inference as provisional.",
         [("رپورٹ", "report", "report"), ("اعداد", "aadaad", "figures"), ("نمونہ", "namuna", "sample"), ("رجحان", "rujhan", "trend"), ("عارضی", "aarzi", "provisional")],
         ("source attribution", "رپورٹ کے مطابق ...؛ اس سے ... کا امکان ہے", "Use کے مطابق to attribute a claim. Use امکان to mark an inference rather than presenting it as the source's statement."),
         [("رپورٹ کے مطابق استعمال بڑھا ہے۔", "report ke mutabiq istemal barha hai.", "According to the report, use has increased."), ("نمونہ محدود ہے، اس لیے رجحان عارضی ہے۔", "namuna mehdood hai, is liye rujhan aarzi hai.", "The sample is limited, so the trend is provisional."), ("اس سے مزید تحقیق کا امکان ظاہر ہوتا ہے۔", "is se mazeed tehqeeq ka imkan zahir hota hai.", "This suggests the possibility of further research.")],
         ("رپورٹ کے مطابق شاید یہ ثابت ہے۔", "رپورٹ کے مطابق یہ رجحان دکھائی دیتا ہے۔", "Do not combine attribution with a stronger certainty than the source supports."), "Summarise a report carefully"),
        ("Explain a workplace change", "Describe what changed, give a reason and report the next action.",
         [("تبدیلی", "tabdeeli", "change"), ("وجہ", "wajah", "reason"), ("ذمہ داری", "zimmedari", "responsibility"), ("تربیت", "tarbiyat", "training"), ("اقدام", "iqdaam", "step")],
         ("relative clause with جو", "وہ تبدیلی جو ...؛ اس لیے ...", "Use جو to connect a noun to a clause that explains it. Keep the reason separate from the action that follows."),
         [("جو تبدیلی ہوئی، اس کی وجہ نئی ذمہ داری تھی۔", "jo tabdeeli hui, us ki wajah nai zimmedari thi.", "The change that occurred was due to a new responsibility."), ("ٹیم کو مختصر تربیت دی جائے گی۔", "team ko mukhtasar tarbiyat di jaegi.", "The team will receive brief training."), ("اس کے بعد ہم نتیجے کا جائزہ لیں گے۔", "is ke baad hum natije ka jaiza lenge.", "After that we will review the result.")],
         ("جو تبدیلی ہوا، اس کی وجہ نئی ذمہ داری تھی۔", "جو تبدیلی ہوئی، اس کی وجہ نئی ذمہ داری تھی۔", "تبدیلی is feminine, so ہوئی agrees with it."), "Report a workplace change"),
        ("Discuss a weather contingency", "Explain a plan for bad weather without claiming the forecast is certain.",
         [("پیش گوئی", "peshgoi", "forecast"), ("بارش", "barish", "rain"), ("متبادل", "mutabadil", "alternative"), ("منسوخ", "mansooh", "cancelled"), ("ممکن", "mumkin", "possible")],
         ("conditional plan", "اگر ... تو ہم ...", "Use اگر ... تو to link a condition to a planned response. A forecast is not a guarantee, so keep possibility language."),
         [("اگر بارش ہوئی تو ہم اندر بیٹھیں گے۔", "agar barish hui to hum andar baithenge.", "If it rains, we will sit indoors."), ("پیش گوئی میں تبدیلی ممکن ہے۔", "peshgoi mein tabdeeli mumkin hai.", "The forecast may change."), ("متبادل جگہ پہلے سے طے کر لیجیے۔", "mutabadil jagah pehle se tai kar lijiye.", "Please decide on an alternative place in advance.")],
         ("اگر بارش ہوگی تو ہم اندر بیٹھے۔", "اگر بارش ہوئی تو ہم اندر بیٹھیں گے۔", "The condition uses ہوئی and the planned result uses بیٹھیں گے."), "Make a weather plan"),
    ],
    "B2": [
        ("Compare treatment options", "Compare two options against stated needs and avoid giving medical advice beyond your role.",
         [("علاج", "ilaaj", "treatment"), ("متبادل", "mutabadil", "alternative"), ("فائدہ", "faida", "benefit"), ("خطرہ", "khatra", "risk"), ("ماہر", "maahir", "specialist")],
         ("qualified comparison", "ایک طرف ...؛ دوسری طرف ...؛ ماہر سے مشورہ", "Balance two options and refer clinical decisions to a qualified professional. A comparison is not a diagnosis."),
         [("ایک طریقے کا فائدہ کم وقت ہے۔", "ek tareeqe ka faida kam waqt hai.", "One option's benefit is that it takes less time."), ("دوسری طرف اس کے کچھ خطرات بھی ہیں۔", "doosri taraf is ke kuch khatraat bhi hain.", "On the other hand, it also has some risks."), ("حتمی انتخاب سے پہلے ماہر سے مشورہ کریں۔", "hatmi intikhab se pehle maahir se mashwara karein.", "Consult a specialist before making a final choice.")],
         ("یہ علاج سب کے لیے بہترین ہے۔", "یہ طریقہ بعض مریضوں کے لیے مناسب ہو سکتا ہے۔", "Qualify a treatment claim and avoid a universal recommendation."), "Compare options responsibly"),
        ("Explain a formal procedure", "Give a procedural instruction and clarify who is responsible for the next step.",
         [("درخواست", "darkhwast", "application"), ("دستخط", "dastkhat", "signature"), ("منسلک", "munsalik", "attached"), ("منظوری", "manzoori", "approval"), ("ذمہ دار", "zimmedar", "responsible")],
         ("passive and responsibility", "درخواست جمع کی جاتی ہے؛ ذمہ داری ... کے پاس ہے", "Use the passive for a procedure when the actor is unimportant, then name the responsible role for the next action."),
         [("درخواست دفتر میں جمع کی جاتی ہے۔", "darkhwast daftar mein jama ki jaati hai.", "The application is submitted to the office."), ("دستخط شدہ نقل ساتھ منسلک ہے۔", "dastkhat shuda naqal saath munsalik hai.", "A signed copy is attached."), ("منظوری کی اطلاع کل دی جائے گی۔", "manzoori ki ittila kal di jaegi.", "The approval notice will be given tomorrow.")],
         ("درخواست دفتر میں جمع کرتا ہے۔", "درخواست دفتر میں جمع کی جاتی ہے۔", "The passive procedure sentence needs the feminine agreement of درخواست."), "Document a procedure"),
        ("Qualify a cultural comparison", "Compare two practices without treating either community as uniform.",
         [("روایت", "riwayat", "tradition"), ("کمیونٹی", "community", "community"), ("فرق", "farq", "difference"), ("سیاق", "siyaaq", "context"), ("عمومی", "umoomi", "general")],
         ("concession and scope", "اگرچہ ...، مگر ...؛ ہر جگہ یکساں نہیں", "Acknowledge a similarity or difference, then state the scope. Avoid universal statements about a diverse community."),
         [("کچھ خاندان یہ روایت برقرار رکھتے ہیں۔", "kuch khandan ye riwayat barqarar rakhte hain.", "Some families maintain this tradition."), ("سیاق کے لحاظ سے طریقہ بدل سکتا ہے۔", "siyaaq ke lihaz se tareeqa badal sakta hai.", "The practice may change according to context."), ("اس لیے ایک عمومی دعویٰ مناسب نہیں۔", "is liye ek umoomi dawa munasib nahin.", "Therefore a universal claim is not appropriate.")],
         ("ہر خاندان یہ روایت ہمیشہ مناتا ہے۔", "کچھ خاندان یہ روایت مناتے ہیں، مگر طریقہ مختلف ہو سکتا ہے۔", "Use a bounded claim instead of generalising about every family."), "Write a balanced comparison"),
    ],
    "C1": [
        ("Distinguish observation from attribution", "Separate what a field note records from what an institution reports.",
         [("مشاہدہ", "mushahida", "observation"), ("ماخذ", "maakhaz", "source"), ("بیان", "bayan", "statement"), ("نسبت", "nisbat", "attribution"), ("تعبیر", "taabeer", "interpretation")],
         ("three evidence frames", "میں نے دیکھا ...؛ ماخذ کے مطابق ...؛ اس سے ... کا امکان", "Use distinct frames for direct observation, an attributed statement and an inference. Do not let the third sound like the first."),
         [("موقع پر دو تختیاں دیکھی گئیں۔", "mauqe par do takhtiyan dekhi gain.", "Two plaques were observed at the site."), ("محکمہ کے بیان کے مطابق، دونوں بعد میں نصب ہوئیں۔", "mahkama ke bayan ke mutabiq, donon baad mein nasb huin.", "According to the department statement, both were installed later."), ("مزید تاریخ کے بغیر قطعی نتیجہ ممکن نہیں۔", "mazeed tareekh ke baghair qatai natija mumkin nahin.", "Without further dating, a definitive conclusion is not possible.")],
         ("محکمہ نے یقیناً یہی ثابت کیا۔", "محکمہ کے بیان کے مطابق یہی امکان ظاہر ہوتا ہے۔", "Attribute the interpretation and preserve the source's uncertainty."), "Annotate evidence levels"),
        ("Offer a diplomatic alternative", "Disagree with a proposal while naming the constraint and a workable alternative.",
         [("تجویز", "tajweez", "proposal"), ("محدودیت", "mahdoodiyat", "constraint"), ("متبادل", "mutabadil", "alternative"), ("نفاذ", "nafaz", "implementation"), ("گنجائش", "gunjaish", "room; scope")],
         ("mitigated disagreement", "آپ کی تجویز قابلِ غور ہے؛ تاہم ...؛ ایک متبادل یہ ہو سکتا ہے", "Acknowledge a proposal before naming the implementation constraint. Offer an alternative as a possibility, not an order."),
         [("آپ کی تجویز قابلِ غور ہے۔", "aap ki tajweez qabil-e-ghaur hai.", "Your proposal merits consideration."), ("تاہم موجودہ عملے کی گنجائش محدود ہے۔", "taham maujooda amle ki gunjaish mehdood hai.", "However, the available staffing capacity is limited."), ("ایک متبادل یہ ہو سکتا ہے کہ مرحلہ وار آغاز کیا جائے۔", "ek mutabadil ye ho sakta hai ke marhala waar aaghaz kiya jae.", "One alternative may be to begin in stages.")],
         ("آپ کی تجویز غلط ہے؛ یہ کریں۔", "آپ کی تجویز قابلِ غور ہے، تاہم مرحلہ وار نفاذ زیادہ موزوں ہو سکتا ہے۔", "Mitigate disagreement and explain the constraint rather than dismissing the proposal."), "Draft a diplomatic reply"),
        ("Synthesize two accounts", "Combine two sources and state one limit on the synthesis.",
         [("مطالعہ", "mutalia", "study"), ("موازنہ", "muwaazana", "comparison"), ("سیاق", "siyaaq", "context"), ("اختلاف", "ikhtilaf", "difference"), ("نتیجہ", "natija", "finding")],
         ("cross-source synthesis", "دونوں مطالعات کو ساتھ پڑھنے سے ...؛ تاہم ...", "Synthesize shared findings while preserving a difference in sample, setting or method."),
         [("دونوں مطالعات میں شرکت بڑھی ہے۔", "donon mutaliaat mein shirkat barhi hai.", "Participation increased in both studies."), ("تاہم ایک مطالعہ شہری علاقوں تک محدود تھا۔", "taham ek mutalia shahri ilaqon tak mehdood tha.", "However, one study was limited to urban areas."), ("یہ فرق نتائج کی تعبیر پر اثر انداز ہو سکتا ہے۔", "ye farq nataij ki taabeer par asar andaaz ho sakta hai.", "This difference may affect how the results are interpreted.")],
         ("دونوں مطالعات ایک جیسے ہیں۔", "دونوں میں ایک مشترک رجحان ہے، مگر ان کے سیاق مختلف ہیں۔", "Name a shared trend without erasing differences between study contexts."), "Write a bounded synthesis"),
    ],
    "C2": [
        ("Scope a claim precisely", "Recast an absolute sentence as a bounded claim with an explicit evidence base.",
         [("دائرہ", "daaira", "scope"), ("دعویٰ", "dawa", "claim"), ("شواہد", "shawahed", "evidence"), ("حد", "had", "limit"), ("استثنا", "istisna", "exception")],
         ("scope and qualification", "دستیاب شواہد کی حد تک ...؛ اسے ... نہیں سمجھنا چاہیے", "Make the evidence base and limit explicit. A bounded conclusion is more informative than an absolute sentence."),
         [("دستیاب شواہد کی حد تک یہ تعبیر ممکن ہے۔", "dastiyab shawahed ki had tak ye taabeer mumkin hai.", "This interpretation is possible within the limits of available evidence."), ("اس سے ہر علاقے کا نتیجہ اخذ نہیں کیا جا سکتا۔", "is se har ilaqe ka natija akhaz nahin kiya ja sakta.", "A result for every region cannot be inferred from this."), ("نمونے کی حد کو ساتھ درج کرنا چاہیے۔", "namune ki had ko saath darj karna chahiye.", "The sample's limitation should be stated alongside it.")],
         ("یہ ہر علاقے میں ثابت ہے۔", "یہ نتیجہ اس محدود نمونے کے دائرے تک ہے۔", "Restrict the claim to the sample rather than generalising to every region."), "Calibrate a conclusion"),
        ("Interpret silence without mind-reading", "Describe a pause as an observable event and distinguish possible implications from intent.",
         [("خاموشی", "khamoshi", "silence"), ("وقفہ", "waqfa", "pause"), ("اشارہ", "ishara", "signal"), ("ارادہ", "irada", "intention"), ("تعبیر", "taabeer", "interpretation")],
         ("implicature with a hedge", "خاموشی سے ... کا تاثر مل سکتا ہے، مگر یہ ارادے کا ثبوت نہیں", "A pause may be interpreted in several ways. Describe a possible implication without claiming access to another person's intention."),
         [("جواب سے پہلے ایک وقفہ آیا۔", "jawab se pehle ek waqfa aaya.", "There was a pause before the answer."), ("اس خاموشی سے فاصلہ رکھنے کا تاثر مل سکتا ہے۔", "is khamoshi se faasla rakhne ka taassur mil sakta hai.", "The silence may give an impression of distance."), ("مگر ارادے کا ثبوت صرف اسی سے نہیں ملتا۔", "magar irade ka saboot sirf isi se nahin milta.", "But that alone does not prove intention.")],
         ("اس کی خاموشی کا مطلب ضرور انکار تھا۔", "خاموشی کو ممکنہ اشارہ سمجھیں، قطعی ارادہ نہیں۔", "Do not infer a definite intention from silence alone."), "Describe an implication carefully"),
        ("Edit an expert statement for register", "Turn a dense expert sentence into a concise public statement without changing its confidence.",
         [("مسودہ", "musawadda", "draft"), ("اختصار", "ikhtisar", "concision"), ("درستگی", "durustagi", "accuracy"), ("قارئین", "qari'in", "readers"), ("اعتماد", "aitemaad", "confidence")],
         ("genre transformation", "اصل دعویٰ برقرار رکھیں؛ اصطلاح کی وضاحت کریں؛ یقین کی سطح نہ بڑھائیں", "Simplify sentence structure and explain a technical term while preserving the original evidence and degree of certainty."),
         [("مسودہ تخصصی اصطلاحات سے بھرا ہوا ہے۔", "musawadda takhassusi istilahat se bhara hua hai.", "The draft is full of specialist terms."), ("عوامی بیان میں ہر اصطلاح کی مختصر وضاحت دیں۔", "awami bayan mein har istilah ki mukhtasar wazahat dein.", "Give a brief explanation of each term in a public statement."), ("زبان آسان ہو سکتی ہے، دعویٰ زیادہ قطعی نہیں۔", "zaban aasan ho sakti hai, dawa zyada qatai nahin.", "The wording can be simpler without making the claim more definite.")],
         ("سادہ زبان کا مطلب ہے کہ نتیجہ قطعی ہو گیا۔", "سادہ زبان وضاحت کرتی ہے؛ وہ شواہد کو مضبوط نہیں کرتی۔", "Editing for accessibility must not increase the strength of the evidence."), "Revise for a public audience"),
    ],
}

BASE_UNITS = {
    "A1": ["ur-a1-u1", "ur-a1-u2", "ur-a1-u3"],
    "A2": ["ur-a2-u1", "ur-a2-u2", "ur-a2-u3"],
    "B1": ["ur-b1-u1", "ur-b1-u2", "ur-b1-u3"],
    "B2": ["ur-b2-u1", "ur-b2-u2", "ur-b2-u3"],
    "C1": ["ur-c1-u1", "ur-c1-u2", "ur-c1-u3"],
    "C2": ["ur-c2-u1", "ur-c2-u2", "ur-c2-u3"],
}
THIRD = {}
for rung, rows in THIRD_SEEDS.items():
    THIRD[rung] = []
    for unit_number, (uid, row) in enumerate(zip(BASE_UNITS[rung], rows), start=1):
        title, aim, words, grammar, examples, mistake, worksheet = row
        lesson_id = f"ur-{rung.lower()}-l{6 + unit_number}"
        THIRD[rung].append((uid, lesson_id,
                            _lesson(title, aim, words, grammar, examples, mistake, worksheet)))


# Half-step unit lesson rows use deliberately different tasks at each rung.
# Each lesson has an observable goal, target forms, three examples and one
# actionable correction.  Romanisation is the same plain-ASCII scheme as the
# rest of the course.
HALF_SEEDS = {
    "A1+": [
        ("Travel information", [
            ("Ask about a departure", "Ask for a departure time and confirm the platform.", [("روانگی", "rawangi", "departure"), ("پلیٹ فارم", "platform", "platform"), ("گاڑی", "gaari", "train"), ("وقت", "waqt", "time"), ("معلومات", "maloomat", "information")], ("wh-question", "گاڑی کب روانہ ہوگی؟", "A future question uses کب and the appropriate future verb form."), [("گاڑی کب روانہ ہوگی؟", "gaari kab rawana hogi?", "When will the train depart?"), ("یہ سات بجے روانہ ہوگی۔", "ye saat baje rawana hogi.", "It will depart at seven."), ("براہ کرم پلیٹ فارم نمبر بتائیے۔", "barah karam platform number bataiye.", "Please tell me the platform number.")], ("گاڑی کب روانہ ہے گی؟", "گاڑی کب روانہ ہوگی؟", "The future auxiliary is ہوگی, not a split ہے گی."), "Check a departure"),
            ("Buy a ticket", "Ask for a one-way ticket and check the fare.", [("ٹکٹ", "ticket", "ticket"), ("یک طرفہ", "yak tarafah", "one-way"), ("کرایہ", "kiraya", "fare"), ("کھڑکی", "khirki", "counter"), ("نقد", "naqd", "cash")], ("polite request", "مجھے ... کا ٹکٹ دیجیے", "Use کا with the destination or route and the polite imperative دیجیے."), [("مجھے لاہور کا یک طرفہ ٹکٹ دیجیے۔", "mujhe Lahore ka yak tarafah ticket dijiye.", "Please give me a one-way ticket to Lahore."), ("اس کا کرایہ کتنا ہے؟", "is ka kiraya kitna hai?", "How much is the fare?"), ("کیا میں نقد ادا کر سکتی ہوں؟", "kya main naqd ada kar sakti hun?", "Can I pay in cash?")], ("مجھے لاہور کے ٹکٹ دیجیے۔", "مجھے لاہور کا ٹکٹ دیجیے۔", "Use the masculine کا with ٹکٹ."), "Buy a ticket"),
            ("Ask for help at the station", "Explain that you missed an announcement and ask for repetition.", [("اعلان", "ailan", "announcement"), ("چھوٹ جانا", "chhoot jana", "to miss"), ("دوبارہ", "dobara", "again"), ("آہستہ", "aahista", "slowly"), ("مدد", "madad", "help")], ("request and repair", "کیا آپ ...؟ براہ کرم ...", "Use a courteous question to request help, then specify what needs repeating."), [("میں اعلان نہیں سن سکی۔", "main ailan nahin sun saki.", "I could not hear the announcement."), ("کیا آپ اسے دوبارہ بتا سکتے ہیں؟", "kya aap ise dobara bata sakte hain?", "Could you repeat it?"), ("براہ کرم آہستہ بولیے۔", "barah karam aahista boliye.", "Please speak slowly.")], ("میں اعلان نہیں سن سکا ہوں۔", "میں اعلان نہیں سن سکی۔", "The feminine speaker form is سن سکی; the masculine is سن سکا."), "Repair a missed announcement"),
        ]),
        ("At a tea stall", [
            ("Name a drink and size", "Order a drink and clarify whether it is for here or takeaway.", [("کپ", "cup", "cup"), ("چائے", "chaay", "tea"), ("دودھ", "doodh", "milk"), ("چینی", "cheeni", "sugar"), ("یہیں", "yahin", "here")], ("request with کیا", "کیا ... مل سکتی ہے؟", "A polite availability question can use مل سکتی ہے with a feminine item such as چائے."), [("کیا دودھ والی چائے مل سکتی ہے؟", "kya doodh wali chaay mil sakti hai?", "Can I get tea with milk?"), ("ایک کپ، کم چینی کے ساتھ۔", "ek cup, kam cheeni ke saath.", "One cup, with little sugar."), ("میں اسے یہیں پیوں گا۔", "main ise yahin piyunga.", "I will drink it here.")], ("کیا چائے مل سکتا ہے؟", "کیا چائے مل سکتی ہے؟", "چائے is feminine, so use سکتی ہے."), "Order tea"),
            ("Ask the price", "Ask how much an item costs and confirm the amount.", [("قیمت", "qeemat", "price"), ("کتنا", "kitna", "how much"), ("سکہ", "sikka", "coin"), ("باقی", "baaqi", "change remaining"), ("مہنگا", "mehnga", "expensive")], ("price question", "اس کی قیمت کتنی ہے؟", "Use کتنی with feminine قیمت. Repeat the amount if you need to confirm it."), [("اس کی قیمت کتنی ہے؟", "is ki qeemat kitni hai?", "How much does it cost?"), ("یہ ایک سو روپے کا ہے۔", "ye ek sau rupay ka hai.", "It costs one hundred rupees."), ("کیا کچھ رقم واپس ملے گی؟", "kya kuch raqam wapas milegi?", "Will I get some change back?")], ("قیمت کتنا ہے؟", "قیمت کتنی ہے؟", "قیمت is feminine; use کتنی."), "Check a price"),
            ("Choose an item", "Ask for a fresh item and state a simple preference.", [("تازہ", "taaza", "fresh"), ("میٹھا", "meetha", "sweet"), ("سادہ", "saada", "plain"), ("پسند", "pasand", "preference"), ("چننا", "chunna", "to choose")], ("preference with پسند", "مجھے ... پسند ہے", "Use مجھے پسند ہے to state a preference; the object normally precedes پسند ہے."), [("مجھے تازہ روٹی پسند ہے۔", "mujhe taaza roti pasand hai.", "I like fresh bread."), ("میں سادہ چائے چنتی ہوں۔", "main saada chaay chunti hun.", "I choose plain tea."), ("یہ میٹھا شربت میرے لیے ہے۔", "ye meetha sharbat mere liye hai.", "This sweet drink is for me.")], ("میں تازہ روٹی پسند کرتا ہوں۔", "مجھے تازہ روٹی پسند ہے۔", "The common preference frame uses مجھے پسند ہے."), "Choose what you like"),
        ]),
        ("Everyday timetable", [
            ("Describe a morning routine", "Sequence two routine actions and state when you leave.", [("صبح", "subah", "morning"), ("ناشتہ", "nashta", "breakfast"), ("تیار", "tayyar", "ready"), ("نکلنا", "nikalna", "to leave"), ("پہلے", "pehle", "first")], ("sequence words", "پہلے ... پھر ...", "Use پہلے and پھر to make the order of routine actions clear."), [("میں پہلے ناشتہ کرتی ہوں۔", "main pehle nashta karti hun.", "I eat breakfast first."), ("پھر میں کام کے لیے نکلتی ہوں۔", "phir main kaam ke liye nikalti hun.", "Then I leave for work."), ("میں آٹھ بجے تیار ہوتی ہوں۔", "main aath baje tayyar hoti hun.", "I get ready at eight.")], ("میں پہلے ناشتہ کرتا ہے۔", "میں پہلے ناشتہ کرتی ہوں۔", "میں takes ہوں; the feminine speaker form is کرتی ہوں."), "Tell a short routine"),
            ("Make a simple plan", "Set a meeting time and ask whether the other person is available.", [("منصوبہ", "mansuba", "plan"), ("کل", "kal", "tomorrow"), ("فارغ", "farigh", "free; available"), ("ملنا", "milna", "to meet"), ("دوپہر", "dopahar", "afternoon")], ("availability question", "کیا آپ ... فارغ ہیں؟", "The respectful آپ takes ہیں. Add a time phrase to make the proposed meeting clear."), [("کیا آپ کل دوپہر فارغ ہیں؟", "kya aap kal dopahar farigh hain?", "Are you free tomorrow afternoon?"), ("ہم دفتر کے قریب مل سکتے ہیں۔", "hum daftar ke qareeb mil sakte hain.", "We can meet near the office."), ("میں دو بجے وہاں پہنچوں گی۔", "main do baje wahan pahunchungi.", "I will arrive there at two.")], ("کیا آپ کل فارغ ہو؟", "کیا آپ کل فارغ ہیں؟", "Respectful آپ takes ہیں, not ہو."), "Arrange a meeting"),
            ("Ask for directions", "Ask which way to a nearby place and follow a short instruction.", [("سیدھا", "seedha", "straight"), ("مڑنا", "murhna", "to turn"), ("چوراہا", "chauraha", "intersection"), ("بائیں", "baen", "left"), ("دائیں", "daen", "right")], ("imperatives for directions", "سیدھا جائیے؛ پھر بائیں مڑیے", "Respectful direction instructions often use polite imperative forms ending in یے."), [("سیدھا جائیے۔", "seedha jaiye.", "Go straight."), ("چوراہے پر بائیں مڑیے۔", "chaurahe par baen muriye.", "Turn left at the intersection."), ("دکان دائیں طرف ہے۔", "dukaan daen taraf hai.", "The shop is on the right.")], ("سیدھا جاؤ، براہ کرم۔", "سیدھا جائیے، براہ کرم۔", "Use the polite imperative جائیے with respectful requests."), "Give and follow directions"),
        ]),
    ],
    "A2+": [
        ("Health and follow-up", [
            ("Describe a symptom", "Describe a symptom, its duration and a change since yesterday.", [("علامت", "alamat", "symptom"), ("درد", "dard", "pain"), ("کل سے", "kal se", "since yesterday"), ("کم", "kam", "less"), ("بخار", "bukhar", "fever")], ("duration with سے", "مجھے ... کل سے ہے", "سے marks a starting point in time. Keep the symptom as the topic and state how it has changed."), [("مجھے سر میں درد کل سے ہے۔", "mujhe sar mein dard kal se hai.", "I have had a headache since yesterday."), ("آج بخار پہلے سے کم ہے۔", "aaj bukhar pehle se kam hai.", "The fever is lower today than before."), ("اگر درد بڑھے تو ڈاکٹر کو بتائیں۔", "agar dard barhe to doctor ko batayen.", "If the pain increases, tell the doctor.")], ("مجھے درد سے کل ہے۔", "مجھے کل سے درد ہے۔", "Use کل سے for 'since yesterday'."), "Describe a change in symptoms"),
            ("Request a repeat appointment", "Ask when to return and confirm whether a report is needed.", [("دوبارہ", "dobara", "again"), ("اگلی ملاقات", "agli mulaqat", "next appointment"), ("ضرورت", "zarurat", "need"), ("ساتھ", "saath", "with"), ("نسخہ", "nuskha", "prescription")], ("indirect question", "ڈاکٹر نے پوچھا کہ ...؟", "Use کہ to introduce reported questions. Keep the embedded question in a natural clause order."), [("ڈاکٹر نے پوچھا کہ درد کم ہوا یا نہیں۔", "doctor ne poocha ke dard kam hua ya nahin.", "The doctor asked whether the pain had decreased."), ("اگلی ملاقات دو ہفتے بعد ہے۔", "agli mulaqat do hafte baad hai.", "The next appointment is in two weeks."), ("نسخہ ساتھ لانے کی ضرورت ہے۔", "nuskha saath lane ki zarurat hai.", "The prescription needs to be brought along.")], ("ڈاکٹر نے پوچھا کہ کیا درد کم ہوا؟", "ڈاکٹر نے پوچھا کہ درد کم ہوا یا نہیں۔", "A reported yes/no question can use یا نہیں rather than keeping the direct question order."), "Confirm a follow-up visit"),
            ("Explain a daily care instruction", "Restate a care instruction and ask a person to confirm it.", [("ہدایت", "hidayat", "instruction"), ("آرام", "araam", "rest"), ("پانی", "paani", "water"), ("یاد رکھنا", "yaad rakhna", "to remember"), ("تصدیق", "tasdeeq", "confirmation")], ("reported instruction with کہ", "انہوں نے کہا کہ ...", "Use کہا کہ to report a spoken instruction. Preserve the source and avoid adding medical advice."), [("نرس نے کہا کہ آرام کرنا ضروری ہے۔", "nurse ne kaha ke araam karna zaruri hai.", "The nurse said that rest is important."), ("پانی پینے کی ہدایت بھی دی گئی۔", "paani peene ki hidayat bhi di gai.", "An instruction to drink water was also given."), ("کیا میں نے ہدایت درست سمجھی؟", "kya main ne hidayat durust samjhi?", "Have I understood the instruction correctly?")], ("نرس نے کہا آرام کرنا ضروری۔", "نرس نے کہا کہ آرام کرنا ضروری ہے۔", "A complete reported clause includes کہ and its predicate."), "Check an instruction"),
        ]),
        ("Work and study", [
            ("Ask for a deadline", "Ask for a deadline and explain which part of a task is complete.", [("آخری تاریخ", "aakhri tareekh", "deadline"), ("حصہ", "hissa", "part"), ("مکمل", "mukammal", "complete"), ("باقی", "baaqi", "remaining"), ("توسیع", "tausee", "extension")], ("polite request for clarification", "کیا آپ بتا سکتے ہیں کہ ...؟", "Use a respectful request before asking for clarification. State the completed and remaining parts separately."), [("کیا آپ آخری تاریخ بتا سکتے ہیں؟", "kya aap aakhri tareekh bata sakte hain?", "Could you tell me the deadline?"), ("پہلا حصہ مکمل ہے۔", "pehla hissa mukammal hai.", "The first part is complete."), ("باقی کام کے لیے ایک دن کی توسیع چاہیے۔", "baaqi kaam ke liye ek din ki tausee chahiye.", "I need a one-day extension for the remaining work.")], ("کیا آپ آخری تاریخ بتا سکتا ہیں؟", "کیا آپ آخری تاریخ بتا سکتے ہیں؟", "Respectful آپ takes سکتے ہیں."), "Clarify a deadline"),
            ("Summarise a lesson", "Summarise a lesson, name one new idea and one question.", [("خلاصہ", "khulasa", "summary"), ("خیال", "khayal", "idea"), ("مثال", "misaal", "example"), ("سوال", "sawal", "question"), ("وضاحت", "wazahat", "explanation")], ("relative clause with جو", "وہ خیال جو ...؛ اس کی مثال ...", "Use جو to identify the idea, then give one supporting example and a question that remains open."), [("آج کا خلاصہ مختصر ہے۔", "aaj ka khulasa mukhtasar hai.", "Today's summary is brief."), ("جو خیال نیا تھا، اس کی مثال واضح تھی۔", "jo khayal naya tha, us ki misaal wazeh thi.", "The example of the idea that was new was clear."), ("ایک سوال پر مزید وضاحت چاہیے۔", "ek sawal par mazeed wazahat chahiye.", "One question needs further explanation.")], ("جو خیال نئے تھا، اس کی مثال واضح تھی۔", "جو خیال نیا تھا، اس کی مثال واضح تھی۔", "خیال is masculine, so use نیا."), "Write a study summary"),
            ("Report an office change", "Explain a schedule change and say which information still needs confirmation.", [("شیڈول", "schedule", "schedule"), ("تبدیل", "tabdeel", "changed"), ("تصدیق", "tasdeeq", "confirmation"), ("اطلاع", "ittila", "notice"), ("بعد میں", "baad mein", "later")], ("reported update", "اطلاع دی گئی کہ ...؛ ابھی تصدیق باقی ہے", "Use اطلاع دی گئی کہ for an attributed notice and distinguish it from details still awaiting confirmation."), [("اطلاع دی گئی کہ میٹنگ کا وقت بدل گیا ہے۔", "ittila di gai ke meeting ka waqt badal gaya hai.", "We were informed that the meeting time has changed."), ("نیا شیڈول ابھی تصدیق طلب ہے۔", "naya schedule abhi tasdeeq talab hai.", "The new schedule still needs confirmation."), ("میں تازہ اطلاع بعد میں بھیجوں گا۔", "main taza ittila baad mein bhejunga.", "I will send an updated notice later.")], ("نیا شیڈول کی تصدیق باقی ہے۔", "نئے شیڈول کی تصدیق باقی ہے۔", "In the oblique case after کی, شیڈول takes the oblique form نئے."), "Share an office update"),
        ]),
        ("Weather and community", [
            ("Give a weather update", "Describe current weather and distinguish observation from forecast.", [("موسم", "mausam", "weather"), ("بادل", "baadal", "clouds"), ("پیش گوئی", "peshgoi", "forecast"), ("ہوا", "hawa", "wind"), ("بارش", "barish", "rain")], ("reported forecast", "محکمہ کے مطابق ...؛ ممکن ہے ...", "Attribute the forecast and use ممکن ہے for a possibility rather than a certainty."), [("ابھی بادل چھائے ہوئے ہیں۔", "abhi baadal chhae hue hain.", "Clouds are covering the sky now."), ("محکمہ کے مطابق شام کو بارش ہو سکتی ہے۔", "mahkama ke mutabiq shaam ko barish ho sakti hai.", "According to the department, it may rain in the evening."), ("تیز ہوا کی صورت میں باہر نہ جائیں۔", "tez hawa ki surat mein bahar na jayen.", "Do not go out in strong winds.")], ("محکمہ نے کہا بارش یقینی ہے۔", "محکمہ کے مطابق بارش کا امکان ہے۔", "Keep a forecast as a likelihood unless the source states certainty."), "Report the forecast"),
            ("Plan a family visit", "Arrange a visit and explain a timing constraint politely.", [("ملاقات", "mulaqat", "visit"), ("رشتہ دار", "rishtedar", "relative"), ("وقت", "waqt", "time"), ("مصروفیت", "masroofiyat", "commitment"), ("مناسب", "munasib", "suitable")], ("softening with شاید", "شاید ... مناسب ہو؛ کیا ...؟", "شاید softens a proposed time. Give the other person a chance to suggest another option."), [("شاید اتوار کی شام مناسب ہو۔", "shayad itwar ki shaam munasib ho.", "Perhaps Sunday evening would work."), ("میرے رشتہ دار دوپہر میں مصروف ہیں۔", "mere rishtedar dopahar mein masroof hain.", "My relatives are busy in the afternoon."), ("کیا ہم وقت بدل سکتے ہیں؟", "kya hum waqt badal sakte hain?", "Can we change the time?")], ("اتوار شام یقیناً مناسب ہے۔", "شاید اتوار کی شام مناسب ہو۔", "A proposal is softened with شاید rather than presented as a certainty."), "Arrange a visit"),
            ("Write a community notice", "Write a short notice with date, place and a clear request.", [("اعلان", "ailan", "notice"), ("مقام", "maqam", "place"), ("شرکت", "shirkat", "participation"), ("براہ کرم", "barah karam", "please"), ("صفائی", "safai", "cleanliness")], ("imperative in a public notice", "براہ کرم + respectful imperative", "A public request should state the action and location. Use a courteous imperative and avoid blaming readers."), [("صفائی مہم جمعہ کو ہوگی۔", "safai muhim jumma ko hogi.", "The clean-up campaign will be on Friday."), ("مقام کمیونٹی مرکز ہے۔", "maqam community markaz hai.", "The location is the community centre."), ("براہ کرم پانی کی بوتل ساتھ لائیے۔", "barah karam paani ki bottle saath laiye.", "Please bring a water bottle.")], ("براہ کرم بوتل لاؤ۔", "براہ کرم بوتل لائیے۔", "Use the respectful imperative in a public notice."), "Draft a community notice"),
        ]),
    ],
}

# The remaining three half-steps move from coherent paragraphs to source-aware
# argument. Unit topics differ by level and the examples carry new language.
HALF_SEEDS.update({
    "B1+": [
        ("Evidence and explanation", [
            ("Attribute a figure", "Attribute a number to a source and state what it does not establish.", [("اعداد", "aadaad", "figures"), ("ماخذ", "maakhaz", "source"), ("نمونہ", "namuna", "sample"), ("تناسب", "tanasub", "proportion"), ("حد", "had", "limit")], ("evidence boundary", "اعداد ... دکھاتے ہیں، مگر ... ثابت نہیں کرتے", "State what the figure shows and what cannot be concluded from it."), [("اعداد تین محلوں میں فرق دکھاتے ہیں۔", "aadaad teen mohallon mein farq dikhate hain.", "The figures show a difference across three neighbourhoods."), ("ماخذ نے صرف ایک موسم کا جائزہ لیا۔", "maakhaz ne sirf ek mausam ka jaiza liya.", "The source reviewed only one season."), ("اس سے سال بھر کا رجحان ثابت نہیں ہوتا۔", "is se saal bhar ka rujhan sabit nahin hota.", "This does not establish a year-round trend.")], ("اعداد سال بھر کا رجحان ثابت کرتا ہے۔", "اعداد ایک محدود مدت کا فرق دکھاتے ہیں۔", "Keep the inference within the data's time range."), "Bound a numerical claim"),
            ("Explain a cause", "Connect a stated cause to an outcome and avoid treating correlation as proof.", [("سبب", "sabab", "cause"), ("اثر", "asar", "effect"), ("تعلق", "talluq", "relationship"), ("ممکن", "mumkin", "possible"), ("تجزیہ", "tajziya", "analysis")], ("cause and possibility", "ممکن ہے کہ ...؛ اس تعلق کی مزید جانچ ضروری ہے", "Use ممکن ہے کہ for a cautious causal explanation and state when further analysis is needed."), [("حاضری بڑھی ہے۔", "hazri barhi hai.", "Attendance has increased."), ("نئی بس سروس اس میں حصہ ڈال سکتی ہے۔", "nai bus service is mein hissa daal sakti hai.", "The new bus service may have contributed to it."), ("سبب جاننے کے لیے مزید تجزیہ ضروری ہے۔", "sabab jaanne ke liye mazeed tajziya zaruri hai.", "Further analysis is needed to identify the cause.")], ("بس سروس نے حاضری یقینی طور پر بڑھائی۔", "بس سروس نے حاضری میں اضافہ کیا ہو سکتا ہے۔", "A possible contribution should not be written as proven causation."), "Explain a possible cause"),
            ("Propose a small trial", "Suggest a limited trial, define a measure and invite feedback.", [("آزمائش", "azmaish", "trial"), ("پیمانہ", "paimana", "measure"), ("رائے", "raaye", "feedback"), ("مدت", "muddat", "period"), ("تجویز", "tajweez", "proposal")], ("suggestion with تاکہ", "تجویز ہے کہ ... تاکہ ...", "Use تاکہ to connect an action to its purpose. State a measurable outcome for the trial."), [("تجویز ہے کہ ایک ماہ کی آزمائش کی جائے۔", "tajweez hai ke ek mah ki azmaish ki jae.", "I suggest a one-month trial."), ("حاضری کو پیمانے کے طور پر درج کریں۔", "hazri ko paimane ke taur par darj karein.", "Record attendance as a measure."), ("مدت کے بعد سب کی رائے لیں۔", "muddat ke baad sab ki raaye lein.", "Collect everyone's feedback after the period.")], ("تجویز ہے کہ آزمائش کریں تاکہ رائے لیا جائے۔", "تجویز ہے کہ آزمائش کی جائے تاکہ رائے لی جائے۔", "Use the passive consistently and match feminine رائے with لی جائے."), "Suggest a limited trial"),
        ]),
        ("Study and work mediation", [
            ("Compare two study methods", "Compare two study methods and state which learner each may suit.", [("طریقہ", "tareeqa", "method"), ("مطالعہ", "mutalia", "study"), ("یادداشت", "yaaddasht", "memory"), ("رفتار", "raftaar", "pace"), ("مناسب", "munasib", "suitable")], ("comparison with کے مقابلے میں", "X کے مقابلے میں Y ...", "Use کے مقابلے میں for comparison and name the learner's needs before making a recommendation."), [("گروہی مطالعہ اکیلے پڑھنے کے مقابلے میں زیادہ گفتگو دیتا ہے۔", "group study akelay parhne ke muqable mein zyada guftagu deta hai.", "Group study gives more discussion than studying alone."), ("خاموش جگہ کچھ لوگوں کے لیے زیادہ مناسب ہے۔", "khamosh jagah kuch logon ke liye zyada munasib hai.", "A quiet place suits some people better."), ("طریقہ مقصد کے مطابق چنیں۔", "tareeqa maqsad ke mutabiq chunein.", "Choose the method according to the goal.")], ("یہ طریقہ سب کے لیے بہتر ہے۔", "یہ طریقہ بعض طالب علموں کے لیے بہتر ہو سکتا ہے۔", "Qualify comparisons instead of making a universal claim."), "Compare study choices"),
            ("Summarise a workplace decision", "Report a decision, its reason and one unresolved question.", [("فیصلہ", "faisla", "decision"), ("وجہ", "wajah", "reason"), ("نفاذ", "nafaz", "implementation"), ("سوال", "sawal", "question"), ("زیرِ غور", "zair-e-ghaur", "under consideration")], ("three-part report", "فیصلہ ...؛ وجہ ...؛ ابھی ... زیرِ غور ہے", "Separate the decision, stated reason and open question so readers know what is settled."), [("ٹیم نے نیا شیڈول منظور کیا۔", "team ne naya schedule manzoor kiya.", "The team approved a new schedule."), ("وجہ کام کی تقسیم تھی۔", "wajah kaam ki taqseem thi.", "The reason was the distribution of work."), ("چھٹیوں کا طریقہ ابھی زیرِ غور ہے۔", "chhuttiyon ka tareeqa abhi zair-e-ghaur hai.", "The leave procedure is still under consideration.")], ("ٹیم نے شیڈول منظور کر رہے ہیں۔", "ٹیم نے شیڈول منظور کیا۔", "A completed decision takes a past form."), "Summarise a decision"),
            ("Clarify a research term", "Explain a term in plain language without removing its technical meaning.", [("اصطلاح", "istilah", "term"), ("سادہ", "saada", "plain"), ("تعریف", "tareef", "definition"), ("مثال", "misaal", "example"), ("مطلب", "matlab", "meaning")], ("definition with یعنی", "اصطلاح X سے مراد ... ہے", "Introduce a definition with سے مراد and add an example that does not overgeneralise."), [("نمونہ سے مراد زیرِ مطالعہ گروہ ہے۔", "namuna se murad zair-e-mutalia giroh hai.", "Sample means the group under study."), ("سادہ لفظوں میں، یہ ان لوگوں کا مجموعہ ہے۔", "saada lafzon mein, ye un logon ka majmua hai.", "In plain language, it is the set of those people."), ("ہر نمونہ پوری آبادی کی نمائندگی نہیں کرتا۔", "har namuna poori aabadi ki numaindagi nahin karta.", "Not every sample represents the full population.")], ("نمونہ سب لوگوں ہوتا ہے۔", "نمونہ زیرِ مطالعہ لوگوں کا گروہ ہوتا ہے۔", "Define the sample as a group, not as all people."), "Explain a research term"),
        ]),
        ("Community plans", [
            ("Negotiate shared duties", "Negotiate a timetable while recognising each person's constraints.", [("ذمہ داری", "zimmedari", "responsibility"), ("باری", "baari", "turn"), ("گنجائش", "gunjaish", "availability"), ("تقسیم", "taqseem", "division"), ("منصفانہ", "munsifana", "fair")], ("negotiation with اگر", "اگر ... تو ...؛ کیا یہ تقسیم منصفانہ ہے؟", "State a condition and invite the other person to assess whether the division is workable."), [("اگر میں پیر کو کام کروں تو آپ منگل کو کر سکتے ہیں؟", "agar main peer ko kaam karun to aap mangal ko kar sakte hain?", "If I do the task Monday, can you do it Tuesday?"), ("اس طرح ذمہ داری برابر تقسیم ہوگی۔", "is tarah zimmedari barabar taqseem hogi.", "This way the responsibility will be divided evenly."), ("کیا آپ کے وقت میں گنجائش ہے؟", "kya aap ke waqt mein gunjaish hai?", "Do you have room in your schedule?")], ("اگر میں کام کروں تو تم نے بھی کرو۔", "اگر میں پیر کو کام کروں تو آپ منگل کو کر سکتے ہیں؟", "Make a proposal and question rather than issuing a mismatched command."), "Agree a shared schedule"),
            ("Respond to a neighbour's concern", "Acknowledge a concern, ask for a detail and suggest a next step.", [("شکایت", "shikayat", "complaint"), ("تفصیل", "tafseel", "detail"), ("آواز", "aawaz", "noise"), ("وقت", "waqt", "time"), ("حل", "hal", "solution")], ("acknowledge and clarify", "آپ کی بات سمجھ میں آتی ہے؛ کیا آپ ...؟", "Acknowledge the concern before requesting a specific detail. Then offer a concrete next step."), [("آپ کی شکایت سمجھ میں آتی ہے۔", "aap ki shikayat samajh mein aati hai.", "I understand your complaint."), ("کیا آپ بتا سکتے ہیں کہ آواز کس وقت زیادہ ہوتی ہے؟", "kya aap bata sakte hain ke aawaz kis waqt zyada hoti hai?", "Can you say at what time the noise is loudest?"), ("ہم اس کے بعد مناسب حل دیکھیں گے۔", "hum is ke baad munasib hal dekhenge.", "After that we will look for a suitable solution.")], ("آپ کی بات نہیں سمجھتا۔", "آپ کی بات سمجھ میں آتی ہے۔", "This response acknowledges the concern rather than denying understanding."), "Respond constructively"),
            ("Plan an inclusive gathering", "Invite people, ask about access needs and provide a practical detail.", [("دعوت", "dawat", "invitation"), ("رسائی", "rasai", "access"), ("جگہ", "jagah", "place"), ("وقت", "waqt", "time"), ("ضرورت", "zarurat", "need")], ("respectful enquiry", "اگر آپ کو ... کی ضرورت ہو تو بتائیے", "Ask about access needs without assuming what a person requires. Provide the relevant location and time."), [("ہماری نشست ہفتے کو چار بجے ہے۔", "hamari nashist hafte ko chaar baje hai.", "Our gathering is on Saturday at four."), ("مقام میں ریمپ موجود ہے۔", "maqam mein ramp maujood hai.", "There is a ramp at the venue."), ("اگر کسی اور سہولت کی ضرورت ہو تو بتائیے۔", "agar kisi aur sahulat ki zarurat ho to bataiye.", "Please tell us if you need another accommodation.")], ("ہر مہمان کو یہی سہولت چاہیے۔", "اگر کسی سہولت کی ضرورت ہو تو بتائیے۔", "Ask the individual rather than generalising about all guests."), "Write an inclusive invitation"),
        ]),
    ],
    "B2+": [
        ("Policy and implementation", [
            ("State a policy limit", "Describe a policy and mark the boundary of its current scope.", [("پالیسی", "policy", "policy"), ("دائرہ", "daaira", "scope"), ("نفاذ", "nafaz", "implementation"), ("استثنا", "istisna", "exception"), ("مرحلہ", "marhala", "stage")], ("scope and exception", "فی الحال ...؛ اس کا اطلاق ... تک ہے", "State the policy's current scope and avoid implying that a later stage is already in force."), [("فی الحال پالیسی تین اضلاع تک محدود ہے۔", "filhaal policy teen azla tak mehdood hai.", "For now, the policy is limited to three districts."), ("اس کا اطلاق اگلے مرحلے میں بڑھ سکتا ہے۔", "is ka itlaq agle marhale mein barh sakta hai.", "Its application may expand in the next stage."), ("استثنا تحریری طور پر درج ہے۔", "istisna tehreeri taur par darj hai.", "The exception is recorded in writing.")], ("پالیسی ہر ضلع میں نافذ ہے۔", "پالیسی فی الحال تین اضلاع میں نافذ ہے۔", "Keep the statement within the policy's current scope."), "Qualify a policy update"),
            ("Compare two proposals", "Compare proposals against the same criterion and name a trade-off.", [("تجویز", "tajweez", "proposal"), ("معیار", "mayaar", "criterion"), ("لاگت", "lagat", "cost"), ("رسائی", "rasai", "access"), ("سمجھوتہ", "samjhauta", "trade-off")], ("parallel comparison", "پہلی تجویز ...؛ دوسری ...؛ دونوں میں ...", "Compare the options against one criterion at a time and make the trade-off explicit."), [("پہلی تجویز کی لاگت کم ہے۔", "pehli tajweez ki lagat kam hai.", "The first proposal costs less."), ("دوسری تجویز زیادہ لوگوں تک پہنچتی ہے۔", "doosri tajweez zyada logon tak pahunchti hai.", "The second proposal reaches more people."), ("انتخاب میں لاگت اور رسائی دونوں اہم ہیں۔", "intikhab mein lagat aur rasai donon aham hain.", "Both cost and access matter in the choice.")], ("پہلی تجویز ہر لحاظ سے بہتر ہے۔", "پہلی تجویز کم خرچ ہے، مگر دوسری کی رسائی زیادہ ہے۔", "Name the relevant trade-off rather than making an unsupported overall ranking."), "Compare options"),
            ("Write a balanced recommendation", "Make a recommendation with a reason and a condition for reviewing it.", [("سفارش", "sifarish", "recommendation"), ("شرط", "shart", "condition"), ("جائزہ", "jaiza", "review"), ("نتیجہ", "natija", "result"), ("عارضی", "aarzi", "provisional")], ("conditional recommendation", "میری سفارش ... ہے، بشرطیکہ ...؛ پھر جائزہ لیا جائے", "Give a reasoned recommendation and state what evidence would trigger another review."), [("میری سفارش محدود آزمائش ہے۔", "meri sifarish mehdood azmaish hai.", "My recommendation is a limited trial."), ("بشرطیکہ نتائج ہر ماہ دیکھے جائیں۔", "basharte ke nataij har mah dekhe jayen.", "Provided that results are reviewed monthly."), ("تین ماہ بعد دوبارہ جائزہ لیا جائے۔", "teen mah baad dobara jaiza liya jae.", "A further review should take place after three months.")], ("میری سفارش قطعی ہے۔", "میری سفارش محدود آزمائش ہے، جس کا تین ماہ بعد جائزہ لیا جائے۔", "State a review condition rather than presenting a recommendation as final."), "Make a bounded recommendation"),
        ]),
        ("Formal mediation", [
            ("Paraphrase a disagreement", "Restate a disagreement neutrally and ask each side to confirm the summary.", [("اختلاف", "ikhtilaf", "disagreement"), ("خلاصہ", "khulasa", "summary"), ("فریق", "fareeq", "party"), ("تصدیق", "tasdeeq", "confirmation"), ("نکتہ", "nuqta", "point")], ("neutral paraphrase", "میرا خلاصہ یہ ہے کہ ...؛ کیا یہ درست ہے؟", "A mediator should frame the summary as a check, not as a verdict."), [("ایک فریق رفتار کو ترجیح دیتا ہے۔", "ek fareeq raftaar ko tarjeeh deta hai.", "One party prioritises speed."), ("دوسرا نگرانی کے طریقے پر سوال اٹھاتا ہے۔", "doosra nigrani ke tareeqe par sawal uthata hai.", "The other questions the monitoring method."), ("کیا یہ خلاصہ دونوں کے موقف کو درست بیان کرتا ہے؟", "kya ye khulasa donon ke mauqif ko durust bayan karta hai?", "Does this summary represent both positions accurately?")], ("ایک فریق غلط ہے۔", "ایک فریق رفتار کو ترجیح دیتا ہے، جبکہ دوسرا نگرانی کی وضاحت چاہتا ہے۔", "Describe each position neutrally instead of assigning blame."), "Check a neutral summary"),
            ("Signal a limitation in a report", "Place a limitation beside the result it qualifies.", [("حد", "had", "limitation"), ("نتیجہ", "natija", "finding"), ("نمونہ", "namuna", "sample"), ("تعبیر", "taabeer", "interpretation"), ("واضح", "wazeh", "clear")], ("concession with تاہم", "نتیجہ ...؛ تاہم نمونہ ...", "Use تاہم to place a limitation next to the finding it qualifies."), [("نتیجہ ابتدائی طور پر حوصلہ افزا ہے۔", "natija ibtidai taur par hausla afza hai.", "The initial finding is encouraging."), ("تاہم نمونہ صرف ایک شہر سے لیا گیا۔", "taham namuna sirf ek shehar se liya gaya.", "However, the sample came from only one city."), ("اس حد کو تعبیر کے ساتھ واضح کرنا چاہیے۔", "is had ko taabeer ke saath wazeh karna chahiye.", "This limitation should be made clear alongside the interpretation.")], ("نتیجہ سب شہروں میں لاگو ہے۔", "نتیجہ ایک شہر کے نمونے تک محدود ہے۔", "Keep the finding within the sample's geographic scope."), "Qualify a report"),
            ("Invite a focused follow-up", "Ask one focused follow-up question to resolve an ambiguity.", [("ابہام", "ibhaam", "ambiguity"), ("وضاحت", "wazahat", "clarification"), ("متعلقہ", "mutaliq", "relevant"), ("سوال", "sawal", "question"), ("مخصوص", "makhsoos", "specific")], ("focused clarification", "کیا آپ واضح کر سکتے ہیں کہ ...؟", "Ask one specific question at a time. Identify the ambiguous term so the answer can address it."), [("لفظ 'کامیابی' کے دو مطلب ہو سکتے ہیں۔", "lafz kamyabi ke do matlab ho sakte hain.", "The word success may have two meanings."), ("کیا آپ واضح کر سکتے ہیں کہ یہاں کون سا پیمانہ مراد ہے؟", "kya aap wazeh kar sakte hain ke yahan kaun sa paimana murad hai?", "Could you clarify which measure is meant here?"), ("اس وضاحت سے نتیجہ سمجھنا آسان ہوگا۔", "is wazahat se natija samajhna aasan hoga.", "That clarification will make the finding easier to understand.")], ("آپ سب کچھ واضح کریں۔", "کیا آپ واضح کر سکتے ہیں کہ یہاں کون سا پیمانہ مراد ہے؟", "A focused question is more useful than an unbounded request."), "Resolve an ambiguity"),
        ]),
        ("Public argument", [
            ("Present a counterargument", "Present a counterargument, acknowledge the opposing concern and qualify the conclusion.", [("اعتراض", "aitiraz", "objection"), ("جواب", "jawab", "response"), ("مگر", "magar", "however"), ("شواہد", "shawahed", "evidence"), ("نتیجہ", "natija", "conclusion")], ("concession and rebuttal", "اگرچہ ...، تاہم ...", "Acknowledge a genuine concern before responding to it. Keep the conclusion proportional to the evidence."), [("اگرچہ لاگت ایک حقیقی مسئلہ ہے، تاہم تاخیر بھی نقصان دہ ہے۔", "agarche lagat ek haqeeqi masla hai, taham takheer bhi nuqsan deh hai.", "Although cost is a real issue, delay is also harmful."), ("شواہد دونوں پہلو دکھاتے ہیں۔", "shawahed donon pehlu dikhate hain.", "The evidence shows both sides."), ("اس لیے محدود آغاز مناسب ہو سکتا ہے۔", "is liye mehdood aaghaz munasib ho sakta hai.", "Therefore a limited start may be appropriate.")], ("اگرچہ لاگت اہم ہے لیکن مگر شروع کریں۔", "اگرچہ لاگت اہم ہے، تاہم محدود آزمائش کی جا سکتی ہے۔", "Use one concession linker and qualify the proposed action."), "Draft a balanced counterargument"),
            ("Separate a source claim from a conclusion", "Report what a source claims and state which conclusion remains yours.", [("دعویٰ", "dawa", "claim"), ("ماخذ", "maakhaz", "source"), ("تعبیر", "taabeer", "interpretation"), ("نتیجہ", "natija", "conclusion"), ("نسبت", "nisbat", "attribution")], ("source versus inference", "ماخذ کا دعویٰ ... ہے؛ میری تعبیر ...", "Attribute the source's claim explicitly and distinguish your interpretation from it."), [("ماخذ کا دعویٰ صرف دو اضلاع سے متعلق ہے۔", "maakhaz ka dawa sirf do azla se mutaliq hai.", "The source's claim concerns only two districts."), ("میری تعبیر میں یہ فرق اہم ہے۔", "meri taabeer mein ye farq aham hai.", "In my interpretation, this difference matters."), ("دونوں باتوں کو الگ بیان کرنا چاہیے۔", "donon baton ko alag bayan karna chahiye.", "The two points should be stated separately.")], ("ماخذ نے یہ نتیجہ ثابت کیا۔", "ماخذ نے یہ دعویٰ کیا؛ نتیجہ میری تعبیر ہے۔", "Do not attribute your own interpretation to the source."), "Attribute a claim correctly"),
            ("Revise a headline", "Shorten a headline while preserving the qualification in the article.", [("سرخی", "surkhi", "headline"), ("اختصار", "ikhtisar", "concision"), ("قید", "qaid", "qualification"), ("دعویٰ", "dawa", "claim"), ("متن", "matn", "body text")], ("headline scope", "سرخی مختصر ہو؛ مگر ... کی حد برقرار رہے", "A short headline should not broaden a qualified finding. Keep the sample or time limit visible."), [("مطالعہ تین اضلاع تک محدود تھا۔", "mutalia teen azla tak mehdood tha.", "The study was limited to three districts."), ("سرخی میں 'تمام علاقوں' لکھنا درست نہیں۔", "surkhi mein tamam ilaqon likhna durust nahin.", "It is not accurate to write 'all areas' in the headline."), ("مختصر قید دعوے کو درست رکھتی ہے۔", "mukhtasar qaid dawe ko durust rakhti hai.", "A brief qualification keeps the claim accurate.")], ("تمام علاقوں میں تبدیلی آئی۔", "تین اضلاع میں تبدیلی دیکھی گئی۔", "The headline must retain the study's geographic limit."), "Edit a qualified headline"),
        ]),
    ],
    "C1+": [
        ("Academic synthesis", [
            ("Frame a synthesis", "Synthesize two sources and identify the point they do not share.", [("ترکیب", "tarkeeb", "synthesis"), ("ماخذ", "maakhaz", "source"), ("مشترک", "mushtarak", "shared"), ("اختلاف", "ikhtilaf", "difference"), ("دائرہ", "daaira", "scope")], ("synthesis with contrast", "دونوں ماخذ ...؛ تاہم ایک ...", "Name a shared result, then preserve a difference in scope or method."), [("دونوں ماخذ حاضری میں اضافہ دکھاتے ہیں۔", "donon maakhaz hazri mein izafa dikhate hain.", "Both sources show increased attendance."), ("تاہم ایک نے صرف دیہی مراکز کا جائزہ لیا۔", "taham ek ne sirf dehi markaz ka jaiza liya.", "However, one reviewed only rural centres."), ("یہ فرق مجموعی تعبیر کو محدود کرتا ہے۔", "ye farq majmooi taabeer ko mehdood karta hai.", "This difference limits the overall interpretation.")], ("دونوں ماخذ ہر جگہ ایک ہی نتیجہ دیتے ہیں۔", "دونوں ایک رجحان دکھاتے ہیں، مگر ان کا دائرہ مختلف ہے۔", "Synthesis should retain a material difference in source scope."), "Synthesize sources"),
            ("Attribute an institutional statement", "Report an institution's position without implying personal endorsement.", [("ادارہ", "idara", "institution"), ("موقف", "mauqif", "position"), ("بیان", "bayan", "statement"), ("تصدیق", "tasdeeq", "confirmation"), ("ذمہ داری", "zimmedari", "responsibility")], ("reported position", "ادارے کے بیان کے مطابق ...؛ اس کی الگ تصدیق ...", "Attribute the position to the institution and state whether an independent confirmation exists."), [("ادارے کے بیان کے مطابق کام مکمل ہے۔", "idare ke bayan ke mutabiq kaam mukammal hai.", "According to the institution's statement, the work is complete."), ("آزاد تصدیق ابھی موصول نہیں ہوئی۔", "azad tasdeeq abhi mausool nahin hui.", "Independent confirmation has not yet been received."), ("اس لیے خبر میں نسبت برقرار رکھیں۔", "is liye khabar mein nisbat barqarar rakhein.", "Therefore keep the attribution in the report.")], ("ادارہ کہتا ہے، اس لیے یہ ثابت ہے۔", "ادارے کے بیان کے مطابق یہ دعویٰ کیا گیا ہے۔", "Attribution is not independent proof."), "Attribute an institutional claim"),
            ("Explain a methodological limit", "Explain how a sample or method constrains the conclusion.", [("طریقۂ کار", "tareeq-e-kaar", "method"), ("نمونہ", "namuna", "sample"), ("پیمائش", "paimaish", "measurement"), ("حد", "had", "limit"), ("نتیجہ", "natija", "finding")], ("method and scope", "چونکہ ...، اس لیے نتیجہ ... تک محدود ہے", "Link the method to the scope of the finding. A clear limit helps readers interpret rather than discard the result."), [("نمونہ صرف آن لائن جواب دہندگان پر مشتمل تھا۔", "namuna sirf online jawab dahindagan par mushtamil tha.", "The sample consisted only of online respondents."), ("اس لیے نتیجہ اسی گروہ تک محدود ہے۔", "is liye natija isi giroh tak mehdood hai.", "Therefore the finding is limited to that group."), ("دیگر آبادیوں پر اطلاق الگ جانچ چاہتا ہے۔", "deegar aabadiyon par itlaq alag jaanch chahta hai.", "Applying it to other populations requires separate testing.")], ("نمونہ سب لوگوں کی نمائندگی کرتا ہے۔", "یہ نمونہ صرف آن لائن جواب دہندگان کی نمائندگی کرتا ہے۔", "State the sample's actual scope rather than generalising."), "Write a methodological note"),
        ]),
        ("Editorial mediation", [
            ("Reconcile two accounts", "Find common ground between accounts and retain their factual difference.", [("بیان", "bayan", "account"), ("مشترک", "mushtarak", "common"), ("فرق", "farq", "difference"), ("مصالحت", "musalehat", "reconciliation"), ("تصدیق", "tasdeeq", "verification")], ("mediation frame", "دونوں بیانات ...؛ اختلاف ... پر ہے", "Identify a common point before stating the exact disagreement."), [("دونوں بیانات میں تاریخ پر اتفاق ہے۔", "donon bayanat mein tareekh par ittefaq hai.", "Both accounts agree on the date."), ("اختلاف ذمہ داری کی تعبیر پر ہے۔", "ikhtilaf zimmedari ki taabeer par hai.", "The disagreement is about how responsibility is interpreted."), ("اس فرق کی آزاد تصدیق ابھی باقی ہے۔", "is farq ki azad tasdeeq abhi baaqi hai.", "Independent verification of this difference is still pending.")], ("دونوں فریق ہر بات پر متفق ہیں۔", "دونوں تاریخ پر متفق ہیں، مگر ذمہ داری پر اختلاف ہے۔", "Preserve both agreement and disagreement."), "Mediate two accounts"),
            ("Edit an institutional paragraph", "Improve clarity while preserving the source's cautious degree of certainty.", [("ادارتی", "idaarati", "editorial"), ("عبارت", "ibarat", "passage"), ("وضاحت", "wazahat", "clarity"), ("احتیاط", "ehtiyat", "caution"), ("یقین", "yaqeen", "certainty")], ("clarity without overstatement", "عبارت واضح کریں؛ یقین کی سطح وہی رکھیں", "Editing may shorten a sentence, but should not turn a tentative finding into a categorical one."), [("ابتدائی نتائج میں بہتری کا اشارہ ملتا ہے۔", "ibtidai nataij mein behtari ka ishara milta hai.", "The initial results indicate possible improvement."), ("نمونہ ابھی محدود ہے۔", "namuna abhi mehdood hai.", "The sample is still limited."), ("اس لیے محتاط تعبیر برقرار رکھیں۔", "is liye mohtat taabeer barqarar rakhein.", "Therefore retain a cautious interpretation.")], ("ابتدائی نتائج نے مکمل کامیابی ثابت کی۔", "ابتدائی نتائج میں بہتری کا اشارہ ملتا ہے، مگر نمونہ محدود ہے۔", "Do not inflate a preliminary indication into proof of complete success."), "Revise an institutional paragraph"),
            ("Summarise without erasing disagreement", "Write a short summary that preserves both a shared finding and an unresolved issue.", [("خلاصہ", "khulasa", "summary"), ("اتفاق", "ittefaq", "agreement"), ("اختلاف", "ikhtilaf", "disagreement"), ("زیرِ بحث", "zair-e-ghaur", "under discussion"), ("اگلا قدم", "agla qadam", "next step")], ("balanced summary", "اتفاق ... پر ہے؛ اختلاف ... پر برقرار ہے", "A useful synthesis names both the point of agreement and the unresolved issue, then sets a next step."), [("فریقین مقصد پر متفق ہیں۔", "fareeqain maqsad par mutafiq hain.", "The parties agree on the goal."), ("وسائل کی تقسیم پر اختلاف برقرار ہے۔", "wasail ki taqseem par ikhtilaf barqarar hai.", "Disagreement about resource allocation remains."), ("اگلی نشست میں اسی نکتے کا جائزہ ہوگا۔", "agli nashist mein isi nuqte ka jaiza hoga.", "That point will be reviewed at the next meeting.")], ("فریقین ہر بات پر متفق ہیں۔", "فریقین مقصد پر متفق ہیں، مگر وسائل پر اختلاف برقرار ہے۔", "Keep the unresolved issue visible in the summary."), "Write a balanced summary"),
        ]),
        ("Style and interpretation", [
            ("Recast a metaphor", "Explain a metaphor in plain prose without claiming it has only one meaning.", [("استعارہ", "istiara", "metaphor"), ("علامت", "alamat", "symbol"), ("سیاق", "siyaaq", "context"), ("مطلب", "matlab", "meaning"), ("ممکن", "mumkin", "possible")], ("interpretation with scope", "سیاق میں ... کا مطلب ... ہو سکتا ہے", "Offer a context-based interpretation as one possibility, not as the only meaning."), [("متن میں 'راستہ' بار بار آتا ہے۔", "matn mein rasta baar baar aata hai.", "The word path recurs in the text."), ("یہ تبدیلی کی علامت ہو سکتا ہے۔", "ye tabdeeli ki alamat ho sakta hai.", "It may symbolise change."), ("مگر قاری دوسری تعبیر بھی پیش کر سکتا ہے۔", "magar qari doosri taabeer bhi pesh kar sakta hai.", "But a reader may offer another interpretation.")], ("اس استعارے کا صرف ایک مطلب ہے۔", "سیاق میں یہ استعارہ تبدیلی کی علامت ہو سکتا ہے۔", "Present interpretation as contextual and open to alternatives."), "Interpret a figurative phrase"),
            ("Preserve register in translation", "Choose a target-language phrase that preserves tone rather than word order.", [("لہجہ", "lehja", "tone"), ("محاورہ", "muhawara", "idiom"), ("لفظی", "lafzi", "literal"), ("قدرتی", "qudrati", "natural"), ("مترجم", "mutarjim", "translator")], ("meaning before word order", "لفظی ترجمہ ...؛ قدرتی تعبیر ...", "A translation should preserve meaning and register; a word-for-word rendering can sound unnatural."), [("یہ محاورہ لفظی طور پر عجیب لگتا ہے۔", "ye muhawara lafzi taur par ajeeb lagta hai.", "This idiom sounds odd when translated literally."), ("قدرتی تعبیر سیاق کے مطابق چنی جائے۔", "qudrati taabeer siyaaq ke mutabiq chuni jae.", "Choose a natural expression according to context."), ("مترجم لہجے کی سطح بھی دیکھتا ہے۔", "mutarjim lehje ki satah bhi dekhta hai.", "A translator also considers register.")], ("لفظی ترجمہ ہمیشہ بہترین ہے۔", "قدرتی ترجمہ معنی اور لہجے دونوں کو دیکھتا ہے۔", "Word-for-word translation can lose tone and idiomatic meaning."), "Choose a register-aware translation"),
            ("State what remains unknown", "Name what the available evidence cannot yet establish and identify the next inquiry.", [("نامعلوم", "namaloom", "unknown"), ("شواہد", "shawahed", "evidence"), ("مزید", "mazeed", "further"), ("جانچ", "jaanch", "examination"), ("یقین", "yaqeen", "certainty")], ("epistemic limit", "ابھی یہ معلوم نہیں کہ ...؛ مزید جانچ درکار ہے", "State the unknown plainly and identify what further evidence would answer the question."), [("ابھی یہ معلوم نہیں کہ فرق کیوں پیدا ہوا۔", "abhi ye maloom nahin ke farq kyun paida hua.", "It is not yet known why the difference occurred."), ("دستیاب شواہد صرف ایک ممکنہ وجہ دکھاتے ہیں۔", "dastiyab shawahed sirf ek mumkin wajah dikhate hain.", "The available evidence shows only one possible cause."), ("مزید جانچ سے نتیجہ واضح ہو سکتا ہے۔", "mazeed jaanch se natija wazeh ho sakta hai.", "Further examination may clarify the result.")], ("وجہ یقینی طور پر معلوم ہے۔", "وجہ ابھی معلوم نہیں؛ مزید جانچ درکار ہے۔", "Do not claim certainty when the evidence leaves the cause unknown."), "Describe an evidence limit"),
        ]),
    ],
})

HALF_STAGE = {"A1+": "A1", "A2+": "A2", "B1+": "B1", "B2+": "B2", "C1+": "C1"}
HALF_TITLES = {
    "A1+": "Practical exchanges beyond the first beginner rung",
    "A2+": "Connected everyday explanations and follow-up",
    "B1+": "Evidence, mediation and qualified recommendations",
    "B2+": "Policy, counterargument and formal mediation",
    "C1+": "Advanced synthesis, editorial judgement and interpretation",
}
HALF_GOALS = {
    "A1+": ["Ask for and confirm travel information.", "Make courteous requests and clarify prices.", "Sequence routines and follow directions using respectful forms."],
    "A2+": ["Describe a change in symptoms without adding medical advice.", "Report deadlines, lesson summaries and schedule updates.", "Attribute a forecast and coordinate a community plan."],
    "B1+": ["Separate a measured result from an inference.", "Compare methods and explain a decision with a remaining question.", "Negotiate shared responsibilities and respond constructively to concerns."],
    "B2+": ["State a policy's current scope and compare trade-offs.", "Mediate accounts neutrally and place limitations beside findings.", "Build a counterargument while preserving source attribution and qualification."],
    "C1+": ["Synthesize sources while retaining differences in scope and method.", "Edit institutional prose without increasing certainty.", "Interpret figurative language and state what remains unknown."],
}
# The half-step extras extend the corresponding full-rung material with a new
# short reading/listening turn and a distinct production focus.
HALF_ADDENDA = {
    "A1+": ("At A1+, learners move from naming places to repairing a missed announcement and confirming a fare. The bridge adds polite repetition requests; it does not imply that one accent is the only correct Urdu.",
            "مسافر نے اعلان دوبارہ سننے کی درخواست کی۔ پھر اس نے کرایہ پوچھا اور ٹکٹ کی رقم گنی۔",
            "The traveller asked to hear the announcement again. Then the traveller asked the fare and counted the ticket money.",
            "مسافر: کیا گاڑی ابھی پلیٹ فارم پر ہے؟<br>معلومات: جی، مگر روانگی میں دس منٹ ہیں۔<br>مسافر: براہ کرم کرایہ بھی بتا دیجیے۔",
            "Traveller: Is the train on the platform now? Information desk: Yes, but departure is in ten minutes. Traveller: Please tell me the fare too."),
    "A2+": ("At A2+, a learner links a request to the reason and the next step. In health settings, repeat only a qualified professional's instruction and ask for clarification when it is unclear.",
            "مریض نے اپنی رپورٹ ساتھ رکھی۔ اس نے نئی ہدایت لکھی اور واپسی کی تاریخ کی تصدیق کی۔",
            "The patient kept the report nearby. They wrote down the new instruction and confirmed the return date.",
            "مریض: کیا مجھے اگلے ہفتے دوبارہ آنا ہے؟<br>استقبالیہ: جی، مگر پہلے تاریخ کی تصدیق کر لیجیے۔<br>مریض: میں ہدایت بھی لکھ لیتا ہوں۔",
            "Patient: Do I need to come again next week? Reception: Yes, but please confirm the date first. Patient: I will write down the instruction too."),
    "B1+": ("At B1+, paragraphs connect evidence, explanation and action. Marking the difference between a source's observation and a writer's inference makes a report more useful, not less decisive.",
            "ٹیم نے پہلے پیمائش دیکھی، پھر رہائشیوں کی رائے سنی۔ دونوں ذرائع ایک ہی سوال کا جواب نہیں دیتے، اس لیے خلاصے میں دونوں کو الگ رکھا گیا۔",
            "The team first reviewed the measurements and then heard residents' views. The two sources do not answer the same question, so the summary kept them distinct.",
            "محرر: کیا دونوں ذرائع ایک ہی نتیجہ دیتے ہیں؟<br>محقق: نہیں، ایک پیمائش دکھاتا ہے اور دوسرا تجربہ۔<br>محرر: پھر خلاصہ دونوں کی حد بتائے گا۔",
            "Editor: Do both sources give the same finding? Researcher: No, one shows a measurement and the other an experience. Editor: Then the summary will state each source's limits."),
    "B2+": ("At B2+, a recommendation names its criteria and the condition for review. Mediation should preserve each party's stated position rather than assign motives that the record cannot establish.",
            "دو تجاویز کا موازنہ ایک ہی معیار پر کیا گیا۔ پہلی کم خرچ تھی، دوسری زیادہ لوگوں تک پہنچی۔ کمیٹی نے محدود آزمائش تجویز کی اور تین ماہ بعد جائزے کا وقت رکھا۔",
            "The two proposals were compared using the same criterion. The first cost less; the second reached more people. The committee proposed a limited trial and scheduled a review after three months.",
            "محرر: کیا کمیٹی نے ایک تجویز مسترد کر دی؟<br>سہولت کار: نہیں، اس نے آزمائش کو محدود رکھا ہے۔<br>محرر: میں یہی فرق رپورٹ میں واضح کروں گا۔",
            "Editor: Did the committee reject one proposal? Facilitator: No, it limited the trial. Editor: I will make that distinction clear in the report."),
    "C1+": ("At C1+, an editor balances precision, accessibility and uncertainty. Simplifying a sentence must not turn a tentative interpretation into a confirmed fact, and a literary metaphor may support more than one reading.",
            "محقق نے نتائج کو ابتدائی کہا اور نمونے کی حد بھی لکھی۔ مدیر نے عبارت مختصر کی، مگر احتیاط برقرار رکھی۔ قاری اب بھی مختلف تعبیر پیش کر سکتا ہے۔",
            "The researcher called the findings preliminary and also stated the sample's limitation. The editor shortened the wording but retained the caution. A reader may still offer a different interpretation.",
            "محقق: کیا مختصر عبارت میں احتیاط باقی ہے؟<br>مدیر: جی، نتیجہ اب بھی ابتدائی ہے۔<br>محقق: اچھا، اس سے یقین کی سطح نہیں بدلی۔",
            "Researcher: Does the shorter passage retain the caution? Editor: Yes, the finding is still preliminary. Researcher: Good; its level of certainty has not changed."),
}


def _checkpoint(title, units):
    items = []
    for ui, unit in enumerate(units, start=1):
        for li, lesson in enumerate(unit[1], start=1):
            if len(items) >= 10:
                break
            ex = lesson[4]
            items.append(("translation", f"{title} {ui}.{li}: write in Urdu: {ex[0][2]}", ex[0][0]))
        if len(items) >= 10:
            break
    # Ten questions are mandatory; add four distinct, lesson-specific retrieval
    # prompts from later examples if the first pass supplied fewer.
    for ui, unit in enumerate(units, start=1):
        for li, lesson in enumerate(unit[1], start=1):
            for ei, ex in enumerate(lesson[4][1:], start=2):
                if len(items) >= 10:
                    break
                items.append(("translation", f"{title} review {ui}.{li}.{ei}: translate: {ex[2]}", ex[0]))
            if len(items) >= 10:
                break
        if len(items) >= 10:
            break
    return items


def _halfstep(level, rows):
    title = f"Urdu {level} — {HALF_TITLES[level]}"
    units = []
    for number, (unit_title, lessons) in enumerate(rows, start=1):
        uid = level.replace("+", "P") + f"-U{number}"
        units.append({"id": uid, "title": unit_title,
                      "lessons": [_lesson(*lesson) for lesson in lessons]})
    base = BASE_EXTRA_ROWS[HALF_STAGE[level]]
    culture, source, reading, gloss, listening, listening_gloss, stage = base
    culture_add, reading_add, gloss_add, listen_add, listen_gloss_add = HALF_ADDENDA[level]
    extra = _extra(culture + " " + culture_add, source,
                   reading + " " + reading_add, gloss + " " + gloss_add,
                   listening + "<br>" + listen_add,
                   listening_gloss + " " + listen_gloss_add,
                   IDIOMS[stage], ERRORS[stage],
                   f"Urdu {level} reflection and production task",
                   f"For {level}, write a response to the new listening exchange. Keep the respectful address form consistent, distinguish what was said from what you infer, and include one relevant expression from this rung.")
    return {"title": title, "native": NATIVE, "goals": HALF_GOALS[level], "units": units,
            "test": _checkpoint(title, rows), "extra": extra}


HALFSTEPS = {
    level: _halfstep(level, rows) for level, rows in HALF_SEEDS.items()
}

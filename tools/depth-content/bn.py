# -*- coding: utf-8 -*-
"""Bengali PHASE 1 depth — extras, third lessons, half-step rungs.

Written with the DSL in `tools/depth_kit.py`; rendered by
`tools/author-depth.py --lang bn`.

House style follows the shipped Bengali course: Bengali script with the
course's own romanisation (`ô` for the inherent vowel, `chh`, `sh`, `ṭ`/`ḍ`),
speakers মিতা and রাতুল, and unit ids in the course's own shape (`A1-U1` for the
CEFR rungs, `bn-c1-u1` for C1/C2). Half-step rungs use `<rung>-U1`, e.g.
`A1+-U1`, so a lesson id is unique across all sixteen files.

Register note: this module teaches চলিত (the modern standard written and spoken
register) throughout, and treats সাধু — the older literary register — as a C1
topic to be recognised, not imitated. That is the same decision the shipped
course makes.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # tools/ on the path
from depth_kit import D, EXTRA, G, L, T, V, WS, X   # noqa: E402

CODE = "bn"
NAME = "Bengali"
NATIVE = "বাংলা"
PHASE = 2
SCRIPT = "Bengali script"
VOICE = "bn-IN"
SKILL = ("Bengali: Bengali script, inherent-vowel reading, classifiers, postpositions, "
         "honorific verb agreement, and the চলিত versus সাধু register split")

# ── the six CEFR rungs get the `extra` block ────────────────────────────────

EXTRAS = {}

EXTRAS["A1"] = EXTRA(
    culture=("Bengali has two everyday greetings and they carry community: নমস্কার for most "
             "Hindu speakers, আদাব for many Muslim speakers, and either is warm. A guest is fed "
             "before being asked anything — refusing the second helping is read as refusing the "
             "welcome, so a small extra spoonful is the polite minimum. The verb comes last, the "
             "honorific comes first: আপনি with elders and strangers, তুমি with friends."),
    source_url="https://en.wikipedia.org/wiki/Bengali_language",
    reading=("আমার নাম মিতা। আমি ঢাকায় থাকি। আমার বাড়ি পুরান ঢাকায়, কিন্তু আমি এখন উত্তরা থাকি। "
             "আমার দুই বন্ধু আছে — রাতুল আর সুমি। রাতুল ছাত্র, সুমি শিক্ষক। আমরা একসাথে বাংলা "
             "শিখি। আজ আমি খুশি, কারণ কাল ছুটি।"),
    reading_gloss=("My name is Mita. I live in Dhaka. My house is in old Dhaka, but I now live in "
                   "Uttara. I have two friends — Ratul and Sumi. Ratul is a student, Sumi is a "
                   "teacher. We learn Bengali together. Today I am happy, because tomorrow is a "
                   "holiday."),
    listening=("মিতা: নমস্কার! আপনি কেমন আছেন?<br>রাতুল: ভালো আছি, ধন্যবাদ। আপনি?<br>"
               "মিতা: আমি ভালো আছি। এটা আপনার বই?<br>রাতুল: হ্যাঁ, এটা আমার বাংলা বই।"),
    listening_gloss=("Mita: Hello! How are you? Ratul: I am well, thank you. And you? Mita: I am "
                     "well. Is this your book? Ratul: Yes, this is my Bengali book."),
    voice_tag=VOICE,
    idioms=[
        ("নমস্কার", "salutation", "the everyday Hindu greeting, hello and goodbye"),
        ("আদাব", "respect", "the everyday Muslim greeting"),
        ("ধন্যবাদ", "thanks", "thank you — added after food or help"),
        ("দয়া করে", "with kindness", "please"),
        ("ক্ষমা করবেন", "you will forgive", "excuse me; sorry to trouble you"),
        ("ঠিক আছে", "it is right", "all right, ok"),
        ("চিন্তা করবেন না", "do not worry", "don't worry about it"),
        ("দেখা হবে", "meeting will happen", "see you"),
        ("কী খবর?", "what news?", "what's up? how are things?"),
        ("স্বাগতম", "welcome", "welcome (guest, event)"),
    ],
    mistakes=[
        ("আমার নাম হলো মিতা।", "আমার নাম মিতা।", "হয়/হলো is not used in a plain self-introduction; the noun stands alone."),
        ("আপনি কেমন আছো?", "আপনি কেমন আছেন?", "আপনি takes the honorific verb আছেন; আছো belongs with তুমি."),
        ("এটা আমার বইটা।", "এটা আমার বই / এটা আমার বইটা?", "Do not use both এটা and the classifier টা in the same phrase unless you mean 'this one of mine'."),
    ],
    task_title="Introduce yourself on paper, then out loud",
    task_instructions=("Write six Bengali sentences: greeting, name, where you live, one thing you "
                       "have (আছে), one thing you are (আছি), and a goodbye. Read the culture note "
                       "again and use its greeting rather than the English one, then say the whole "
                       "thing aloud without looking."),
)

EXTRAS["A2"] = EXTRA(
    culture=("The Bengali year turns in mid-April with পহেলা বৈশাখ, and the greeting শুভ নববর্ষ is "
             "exchanged in both Dhaka and Kolkata. Shops open new account books (হালখাতা), families "
             "eat পান্তা-ইলিশ, and the day is deliberately loud, sweet and public. It is the one "
             "festival where the two Bengals do the same thing on the same morning."),
    source_url="https://en.wikipedia.org/wiki/Pohela_Boishakh",
    reading=("গতকাল আমি আর রাতুল বাজারে গিয়েছিলাম। আমরা ফল আর মিষ্টি কিনেছি। রাতুল বলল, «আগামীকাল "
             "নববর্ষ, তাই আজ বেশি কিনতে হবে»। আমি হেসে বললাম, «ঠিক আছে, কিন্তু টাকা কে দেবে?» "
             "সে বলল, «আমি দেব»। শুনে আমার খুশি লাগল।"),
    reading_gloss=("Yesterday Ratul and I went to the market. We bought fruit and sweets. Ratul said, "
                   "'Tomorrow is the new year, so we have to buy more today.' I laughed and said, "
                   "'All right, but who will pay?' He said, 'I will pay.' Hearing that made me happy."),
    listening=("রাতুল: আজ বাজারে কী কিনবে?<br>মিতা: কিছু ফল আর দুধ। তুমি?<br>"
               "রাতুল: আমি রুটি আর সবজি নেব।<br>মিতা: দাম কত? খুব বেশি হলে আমি নেব না।"),
    listening_gloss=("Ratul: What will you buy at the market today? Mita: Some fruit and milk. "
                     "You? Ratul: I'll take bread and vegetables. Mita: What's the price? If it is "
                     "too much I won't take it."),
    voice_tag=VOICE,
    idioms=[
        ("পহেলা বৈশাখ", "the first of Boishakh", "Bengali New Year's Day"),
        ("শুভ নববর্ষ", "auspicious new year", "Happy New Year"),
        ("মনে হয়", "it seems to the mind", "I think, it seems"),
        ("কিছু মনে করবেন না", "do not take it to mind", "no offence meant"),
        ("হাতের পাঁচ", "five of the hand", "close at hand, within reach"),
        ("চোখের মণি", "jewel of the eye", "the apple of one's eye"),
        ("জিভে জল আসা", "water coming to the tongue", "mouth-watering"),
        ("এক মিনিট", "one minute", "just a moment"),
        ("কাছে আসা", "coming near", "to approach, to come close"),
        ("দুঃখিত", "regretful", "sorry"),
    ],
    mistakes=[
        ("আমি গতকাল বাজারে যাব।", "আমি গতকাল বাজারে গিয়েছিলাম।", "গতকাল is past; the verb has to be past."),
        ("দামটা খুব বেশি হয়।", "দামটা খুব বেশি।", "বেশি is an adjective here; হয় makes it a habit, not a price."),
        ("আমার দুই বন্ধু আছে, কিন্তু আমার দুই ভাই আছে।", "আমার দুই বন্ধু আছে, আর আমার দুই ভাই আছে।", "এবং/কিন্তু joins agreements, not additions; use আর for 'and also'."),
    ],
    task_title="Yesterday and tomorrow, in one page",
    task_instructions=("Write five Bengali sentences about yesterday (past verb forms) and five about "
                       "tomorrow (future forms with -ব/-বে). Then read it aloud and underline every "
                       "place you used a present-tense verb with a past time word — that is the habit "
                       "this level breaks."),
)

EXTRAS["B1"] = EXTRA(
    culture=("মাছে-ভাতে বাঙালি — 'a Bengali is fish and rice' — is a proverb that doubles as a food "
             "rule. Rice is the base of both main meals, fish is the default protein (ইলিশ in the "
             "monsoon, রুই all year), and a meal without rice is not quite a meal. Guests are offered "
             "fish head as a mark of honour, which is the sort of rule a B1 speaker should know "
             "before sitting down."),
    source_url="https://en.wikipedia.org/wiki/Bengali_cuisine",
    reading=("আমরা ঠিক করেছি যে শনিবার আমাদের বাড়িতে রান্না হবে। মা বলেছেন মাছ আর ভাত অবশ্যই লাগবে, "
             "কারণ আমাদের বাড়িতে অতিথি আসছেন। আমি ভাবছি ডাল আর সবজি আমি বানাব। যদি সময় থাকে, মিষ্টিও "
             "বানাব। তবে একটা শর্ত আছে — রান্নার পরে বাসন ধোয়া আমার কাজ নয়!"),
    reading_gloss=("We have decided that cooking will happen at our house on Saturday. Mother said "
                   "fish and rice are essential, because a guest is coming to our house. I am "
                   "thinking I will make dal and vegetables. If there is time, I'll make sweets too. "
                   "But there is one condition — washing the dishes after cooking is not my job!"),
    listening=("মিতা: আপনি কি খুব ব্যস্ত?<br>রাতুল: একটু ব্যস্ত, কারণ কাল একটা পরীক্ষা আছে।<br>"
               "মিতা: তাহলে আমি পরে ফোন করি।<br>রাতুল: ধন্যবাদ, সন্ধ্যায় কথা বলব।"),
    listening_gloss=("Mita: Are you very busy? Ratul: A little busy, because there is an exam "
                     "tomorrow. Mita: Then I'll call later. Ratul: Thank you, we'll talk in the "
                     "evening."),
    voice_tag=VOICE,
    idioms=[
        ("অতি লোভে তাতি নষ্ট", "in too much greed the weaver is ruined", "greed loses everything"),
        ("চকচক করলেই সোনা হয় না", "shining does not make it gold", "all that glitters is not gold"),
        ("যেমন কর্ম তেমন ফল", "as the deed, so the fruit", "you reap what you sow"),
        ("ঘর পোড়া গরু সিঁদুরে মেঘ দেখলে ভয় পায়", "the burnt cow fears a red cloud", "once burned, twice shy"),
        ("হাতের পাঁচ", "five of the hand", "very near, close by"),
        ("নাচতে না জানলে উঠান বাঁকা", "if you cannot dance, the yard is crooked", "a bad workman blames his tools"),
        ("বিনা মেঘে বজ্রপাত", "thunder without a cloud", "a bolt from the blue"),
        ("শাক দিয়ে মাছ ঢাকা", "covering fish with greens", "hiding what everyone can see"),
        ("চোরে চোরে মাসতুতো ভাই", "thieves are cousins", "birds of a feather flock together"),
        ("এক হাতে তালি বাজে না", "one hand does not clap", "it takes two"),
    ],
    mistakes=[
        ("আপনি কাল আসবে।", "আপনি কাল আসবেন।", "আপনি takes -বেন, never -বে."),
        ("আমি জানি না যে সে আসবে কিনা আসবে।", "আমি জানি না সে আসবে কি না।", "The Bengali 'whether' frame is -বে কি না, not a doubled verb."),
        ("আমার মনে হয় না সে আসবে।", "আমার মনে হয় সে আসবে না।", "Negating মনে হয় says 'I do not think'; negating the inner verb says what you mean."),
    ],
    task_title="Explain a problem in six sentences",
    task_instructions=("Take a real problem — a delay, a broken plan, a missed bus. Write six Bengali "
                       "sentences: what happened (past), why (কারণ), what you decided (ঠিক করেছি), and "
                       "one condition (যদি). Then say it aloud in ninety seconds as if to a friend, "
                       "keeping আপনি/tুমি consistent throughout."),
)

EXTRAS["B2"] = EXTRA(
    culture=("Durga Puja is the largest public art event in Bengal: for four days neighbourhoods "
             "build pandals, committees commission hundreds of idols, and the city walks from one to "
             "the next. The economics matter as much as the religion — thousands of small workshops "
             "work all year — and the vocabulary of the festival (প্যান্ডেল, প্রতিমা, বিসর্জন) has "
             "entered ordinary business Bengali."),
    source_url="https://en.wikipedia.org/wiki/Durga_Puja",
    reading=("প্রতিবেদনে বলা হয়েছে যে উৎসবের সময় শহরে প্রায় দশ লক্ষ মানুষ আসেন, এবং স্থানীয় "
             "ব্যবসায়ীরা বছরের সবচেয়ে বেশি বিক্রি করেন এই সময়েই। তবে সমালোচকরা মনে করেন যে খরচের "
             "একটা অংশ কেবল প্রতিযোগিতার জন্য, সংস্কৃতির জন্য নয়। অন্যদিকে আয়োজকরা বলছেন প্রতিটি "
             "টাকা স্থানীয় কারিগরদের কাছেই যায়।"),
    reading_gloss=("The report says that about a million people come to the city during the festival, "
                   "and local traders do their highest sales of the year at this time. Critics, "
                   "however, think part of the spending is only for competition, not for culture. On "
                   "the other hand, organisers say every taka goes to local artisans."),
    listening=("মিতা: বাজেট নিয়ে আপনার মত কী?<br>রাতুল: আমি বলব খরচ কমানো উচিত, তবে মান কমানো উচিত নয়।<br>"
               "মিতা: যদি কমিটি একমত হয়, তাহলে প্রস্তাবটা পাস হবে।<br>রাতুল: ঠিক, কিন্তু লিখিত "
               "প্রস্তাব দরকার।"),
    listening_gloss=("Mita: What is your opinion on the budget? Ratul: I would say spending should be "
                     "reduced, but quality should not be. Mita: If the committee agrees, the proposal "
                     "will pass. Ratul: Right — but a written proposal is needed."),
    voice_tag=VOICE,
    idioms=[
        ("অগ্নিপরীক্ষা", "ordeal by fire", "a severe test"),
        ("আকাশকুসুম", "sky-flower", "a castle in the air"),
        ("ঘোড়ার ডিম", "horse's egg", "something that does not exist; rubbish"),
        ("গোবর গণেশ", "dung Ganesh", "a dunce, someone out of their depth"),
        ("কপাল ফেরা", "the forehead turning", "fortune turns at last"),
        ("ঠোঁটকাটা", "cut-lipped", "blunt, says exactly what they think"),
        ("চোখে ধুলো দেওয়া", "throwing dust in the eyes", "to deceive, to pull the wool over eyes"),
        ("মাথায় হাত", "hand on the head", "to be shocked; disaster struck"),
        ("রাবণের চিতা", "Ravana's pyre", "an unending quarrel"),
        ("শিরে সংক্রান্তি", "a calamity on the head", "a disaster hanging overhead"),
    ],
    mistakes=[
        ("আমি মনে করি যে খরচ কমানো দরকার নেই।", "আমি মনে করি খরচ কমানো দরকার।", "দরকার নেই means 'not needed'; করি যে is also heavy in Bengali prose — drop যে."),
        ("এটা করা হয়ে আছে।", "এটা করা হয়েছে।", "The passive/perfect frame is করা হয়েছে."),
        ("প্রতিবেদনে বলে যে…।", "প্রতিবেদনে বলা হয়েছে যে…", "Reports do not 'say' with a bare verb; the impersonal বলা হয়েছে is the register."),
    ],
    task_title="Rewrite one decision in three registers",
    task_instructions=("Take a decision from your work or society. Write it three times in Bengali: "
                       "one line as a report (বলা হয়েছে যে…), one as an argument with a concession "
                       "(তবে…), and one as a proposal others must approve (প্রস্তাব)। Keep to twenty "
                       "words each, and keep the facts identical."),
)

EXTRAS["C1"] = EXTRA(
    culture=("Bengali has two written registers: সাধু, the older literary form that keeps verb "
             "endings like -ইয়াছেন, and চলিত, the modern standard that says এসেছেন. Twentieth-century "
             "prose writers moved literature from সাধু to চলিত, and the move is now history — a "
             "document that mixes them reads as unfinished. A C1 writer recognises সাধু in Tagore's "
             "older essays and in a few fixed proverbs, and writes চলিত everywhere else."),
    source_url="https://en.wikipedia.org/wiki/Sadhu_bhasha",
    reading=("উল্লেখ করা প্রয়োজন যে এই প্রতিবেদনের ভাষা সম্পূর্ণ চলিত রাখা হয়েছে, কারণ রাষ্ট্রীয় "
             "নথিতে সাধু-চলিত মিশ্রণ পাঠকের আস্থা কমায়। সম্পাদনার সময় দুইটি বিষয় লক্ষ্য রাখতে হবে: "
             "শব্দের বাহুল্য বাদ দেওয়া, এবং অনুবাদের ক্ষেত্রে আক্ষরিকতার চেয়ে অর্থের অগ্রাধিকার দেওয়া। "
             "তদুপরি, প্রতিটি সংখ্যার সূত্র স্পষ্টভাবে উল্লেখ করতে হবে।"),
    reading_gloss=("It is worth noting that the language of this report has been kept entirely in "
                   "চলিত, because mixing সাধু and চলিত in a state document reduces the reader's trust. "
                   "During editing two things must be watched: cutting word-padding, and — in "
                   "translation — giving priority to meaning over literalism. Furthermore, the source "
                   "of every figure must be stated clearly."),
    listening=("সম্পাদক: এই লাইনটা সাধু হয়ে গেছে।<br>লেখক: কোথায়?<br>"
               "সম্পাদক: «তিনি আসিয়াছেন» — চলিত হবে «তিনি এসেছেন»।<br>"
               "লেখক: ঠিক, আরেকবার পুরোটা পড়ে দেখি।"),
    listening_gloss=("Editor: This line has drifted into সাধু. Writer: Where? Editor: 'তিনি আসিয়াছেন' — "
                     "চলিত would be 'তিনি এসেছেন'. Writer: Right, let me read the whole thing again."),
    voice_tag=VOICE,
    idioms=[
        ("উপরিউক্ত", "stated above", "the above-mentioned"),
        ("প্রসঙ্গক্রমে", "in the course of the context", "incidentally, in this connection"),
        ("দৃষ্টান্তস্বরূপ", "as an example", "for instance"),
        ("সূত্রানুসারে", "according to the source", "as per the source"),
        ("আলোকপাত করা", "to cast light on", "to shed light on"),
        ("নিরপেক্ষভাবে", "in a neutral manner", "impartially"),
        ("ব্যতিক্রম ব্যতীত", "except for the exception", "with no exception"),
        ("তাৎপর্য", "that which carries weight", "significance"),
        ("কার্যকর করা", "to make effective", "to implement"),
        ("প্রযোজ্য", "applicable", "applicable, in force"),
    ],
    mistakes=[
        ("তিনি আসিয়াছেন, তাই আমরা শুরু করলাম।", "তিনি এসেছেন, তাই আমরা শুরু করলাম।", "One register per document; আসিয়াছেন is সাধু."),
        ("ডকুমেন্টটি সম্পাদন করা হয়েছে।", "নথিটি সম্পাদনা করা হয়েছে।", "সম্পাদন is performing (e.g. a song); editing is সম্পাদনা — and ডকুমেন্ট is a calque of নথি."),
        ("প্রতিবেদনটি নিরপেক্ষ।", "প্রতিবেদনটি নিরপেক্ষভাবে লেখা হয়েছে।", "নিরপেক্ষ is an adjective; a report is written neutrally — নিরপেক্ষভাবে."),
    ],
    task_title="Two registers, one message",
    task_instructions=("Take a work message — a delay, a refusal, a correction. Write it twice in "
                       "Bengali: once for a chat group in spoken চলিত, once as an official letter. "
                       "Then mark every place the register moved and say why out loud. Finish by "
                       "reading a Tagore essay from the older collection and finding three সাধু forms "
                       "you would change."),
)

EXTRAS["C2"] = EXTRA(
    culture=("Bengali rhetoric names its own figures: উপমা (simile), রূপক (metaphor), অনুপ্রাস "
             "(alliteration), শ্লেষ (pun) and ব্যাজস্তুতি (ironic praise). Rabindranath's prose and "
             "Nazrul's poetry both work by setting one figure and then breaking it, and a newspaper "
             "headline in Dhaka or Kolkata will still carry an অনুপ্রাস because the ear expects it. "
             "Reading figures is C2 work; using one per paragraph is the discipline."),
    source_url="https://en.wikipedia.org/wiki/Bengali_literature",
    reading=("বাজেটকে ঘিরে বিতর্কটা এখন রাবণের চিতা — কেউ নেভাতে পারে না, কেউ ছাড়তেও পারে না। "
             "সরকার বলছে সংখ্যা স্পষ্ট, সমালোচকরা বলছেন সংখ্যার ক্রমটাই কৌশলী। একজন সাংবাদিক লিখেছেন: "
             "«যেখানে উপমা বেশি, সেখানে হিসাব কম» — কথাটা শ্লেষ, তবে অর্ধেক সত্য। এবং অর্ধেক সত্য "
             "নিয়ে রাজনীতি চলে।"),
    reading_gloss=("The debate around the budget is now Ravana's pyre — nobody can put it out, nobody "
                   "can leave it. The government says the numbers are clear; critics say the ordering "
                   "of the numbers is the trick. One journalist wrote: 'Where there are more similes, "
                   "there are fewer accounts' — the line is irony, but half true. And politics runs on "
                   "half truths."),
    listening=("সম্পাদক: শিরোনামটা তিনবার পড়েছি, কিছু ঠিক লাগছে না।<br>লেখক: অনুপ্রাসটা বেশি হয়ে গেছে?<br>"
               "সম্পাদক: হ্যাঁ, আর শ্লেষটা পাঠক ধরতে পারবেন না।<br>লেখক: তাহলে একটা চিত্র রেখে বাকিটা "
               "ছুঁড়ে দিই।"),
    listening_gloss=("Editor: I have read the headline three times; something feels off. Writer: Is the "
                     "alliteration too much? Editor: Yes — and the reader will not catch the irony. "
                     "Writer: Then let me keep one image and throw the rest away."),
    voice_tag=VOICE,
    idioms=[
        ("অশ্বডিম্ব", "a horse-egg", "an impossibility"),
        ("রাবণের চিতা", "Ravana's pyre", "a quarrel that cannot be resolved"),
        ("পুকুর চুরি করে গঙ্গাস্নান", "steal the pond, then bathe in the Ganges", "to do wrong and then act pious"),
        ("খয়ের খাঁ", "a khayer flatterer", "a flatterer, a sycophant"),
        ("ছেলের হাতের মোয়া", "a sweet in a child's hand", "gone in a moment"),
        ("ভিজে বিড়াল", "a wet cat", "a sly person who pretends innocence"),
        ("অগস্ত্য যাত্রা", "Agastya's journey", "a departure with no return"),
        ("ঘোড়ার ডিম", "horse's egg", "nonsense, something impossible"),
        ("নয়নের মণি", "jewel of the eye", "the most beloved person"),
        ("শাপে বর", "a blessing in a curse", "a good outcome from a bad event"),
    ],
    mistakes=[
        ("যেখানে উপমা বেশি সেখানে হিসাব কম — এই কথাটা প্রমাণ।", "এই কথাটা শ্লেষ, প্রমাণ নয়।", "A figure of speech is not evidence; naming it as one keeps the argument honest."),
        ("শিরোনামে তিনটি উপমা আর দুইটি শ্লেষ।", "শিরোনামে একটি চিত্রই যথেষ্ট।", "One figure per headline; stacking them turns the line into parody."),
        ("উপরিউক্ত অশ্বডিম্ব প্রমাণ করে যে…।", "উপরিউক্ত দাবিটি অশ্বডিম্বের মতো অবাস্তব।", "An idiom describes a claim; it cannot itself be the evidence."),
    ],
    task_title="Name the figure, then cut it",
    task_instructions=("Take a headline you saw this week in Bengali. Name its figure (উপমা, রূপক, "
                       "অনুপ্রাস, শ্লেষ) in one sentence, then rewrite the headline three ways: with "
                       "the figure removed, doubled, and turned against its own argument. Read all "
                       "four aloud and keep the one you would actually print."),
)

# ── a third lesson in every unit of the six CEFR rungs ──────────────────────
# (unit id, lesson id, spec) — the renderer appends or replaces by lesson id.

THIRD = {}

THIRD["A1"] = [
    ("A1-U1", "A1-U1-L3", L(
        "Thanks, please, sorry — the three small words",
        "Three words carry every small exchange: ধন্যবাদ (thank you), দয়া করে (please) and "
        "মাফ করবেন / ক্ষমা করবেন (excuse me, sorry). They do not change with the person the way verbs "
        "do, which makes them the safest words in A1.",
        [V("ধন্যবাদ", "dhonnobad", "thank you", "interjection"),
         V("দয়া করে", "dôya kôre", "please", "phrase"),
         V("ক্ষমা করবেন", "kkhôma kôrben", "excuse me, forgive me", "phrase"),
         V("স্বাগতম", "shagotom", "welcome", "interjection"),
         V("আবার দেখা হবে", "abar dekha hôbe", "we will meet again", "phrase")],
        G("Small words, no change",
          "dhonnobad · dôya kôre + request · kkhôma kôrben",
          "দয়া করে বসুন. ধন্যবাদ, আপনি খুব ভালো. The three words stay the same whether you speak to "
          "আপনি, তুমি or তুই — the verb around them carries the politeness.",
          [X("দয়া করে একটু জল দিন।", "dôya kôre ekṭu jôl din.", "Please give me a little water."),
           X("আপনার সাহায্যের জন্য ধন্যবাদ।", "apnar shahajjer jonno dhonnobad.", "Thank you for your help."),
           X("ক্ষমা করবেন, আমি দেরি করেছি।", "kkhôma kôrben, ami deri korechhi.", "Excuse me, I am late.")],
          [("দয়া করে করবেন ভদ্র।", "দয়া করে বসুন।", "দয়া করে attaches to an imperative, not to an adjective."),
           ("ধন্যবাদ আপনি।", "আপনাকে ধন্যবাদ।", "Thanks is given to a person: আপনাকে ধন্যবাদ.")]),
        [D("মিতা", "দয়া করে একটু জল দিন।", "dôya kôre ekṭu jôl din.", "Please give me a little water."),
         D("রাতুল", "এই যে, নিন।", "ei je, nin.", "Here you are, take it."),
         D("মিতা", "আপনাকে ধন্যবাদ!", "apnake dhonnobad!", "Thank you!"),
         D("রাতুল", "ক্ষমা করবেন, আমাকে এখন যেতে হবে।", "kkhôma kôrben, amake ekhon jete hobe.", "Excuse me, I have to go now.")],
        WS("Small words worksheet", [
            T("Translate to Bengali.", ["please", "thank you", "excuse me", "see you again"],
              ["দয়া করে", "ধন্যবাদ", "ক্ষমা করবেন", "আবার দেখা হবে"]),
            T("Complete politely.", ["___ একটু বসুন।", "আপনাকে ___।"],
              ["দয়া করে", "ধন্যবাদ"]),
        ]))),
    ("A1-U2", "A1-U2-L3", L(
        "Counting and asking: এক, দুই, কত?",
        "Counting in Bengali runs to ten quickly: এক, দুই, তিন, চার, পাঁচ. Numbers above two usually "
        "take a classifier when you count things — দুইটা বই — and কত asks how many or how much.",
        [V("এক", "æk", "one", "numeral"),
         V("দুই", "dui", "two", "numeral"),
         V("তিন", "tin", "three", "numeral"),
         V("পাঁচ", "pãch", "five", "numeral"),
         V("কত", "kôto", "how many, how much", "interrogative")],
        G("Numbers and classifiers",
          "number + টা/টি + noun when counting things",
          "দুইটা বই, তিনটা কলম, পাঁচটা ছাত্র. এক stays classifier-free with the noun: একটা/all এক "
          "বই. In writing, টি is more formal than টা.",
          [X("আমার দুইটা বই আছে।", "amar duiṭa boi achhe.", "I have two books."),
           X("কত জন ছাত্র আছে?", "kôto jon chhatro achhe?", "How many students are there? (people take জন)"),
           X("পাঁচটা কলা নিন।", "pãchṭa kôla nin.", "Take five bananas.")],
          [("আমার দুই বই আছে।", "আমার দুইটা বই আছে।", "Counting countable things normally takes টা/টি."),
           ("কত ছাত্র আছে? (about people)", "কত জন ছাত্র আছে?", "People are counted with জন, not টা.")]),
        [D("রাতুল", "তোমার কাছে কতগুলো বই আছে?", "tomar kachhe kôtogulo boi achhe?", "How many books do you have?"),
         D("মিতা", "আমার দশটা বই আছে। তুমি?", "amar dôshṭa boi achhe. tumi?", "I have ten books. You?"),
         D("রাতুল", "আমার পাঁচটা বই, আর দুইটা খাতা।", "amar pãchṭa boi, ar duiṭa khata.", "I have five books, and two notebooks."),
         D("মিতা", "বেশ! তাহলে মিলে অনেক বই।", "besh! tahole mile ônek boi.", "Good! Then together we have many books.")],
        WS("Counting worksheet", [
            T("Count in Bengali.", ["2 books", "3 pens", "5 people", "10 taka"],
              ["দুইটা বই", "তিনটা কলম", "পাঁচ জন", "দশ টাকা"]),
            T("Ask with কত.", ["how many books?", "how much money?", "how many students?"],
              ["কতগুলো বই?", "কত টাকা?", "কত জন ছাত্র?"]),
        ]))),
    ("A1-U3", "A1-U3-L3", L(
        "Question words: কী, কে, কোথায়",
        "Three question words open most A1 conversations: কী (what), কে (who), কোথায় (where). They "
        "stand where the answer would stand, and the verb stays where it was.",
        [V("কী", "ki", "what", "interrogative"),
         V("কে", "ke", "who", "interrogative"),
         V("কোথায়", "kothay", "where", "interrogative"),
         V("কেন", "keno", "why", "interrogative"),
         V("কখন", "kôkhon", "when", "interrogative")],
        G("Question word in place",
          "sentence order does not change: subject + question word + verb",
          "আপনার নাম কী? আপনি কোথায় থাকেন? ইনি কে? In speech the question word often goes to the "
          "front: কোথায় থাকেন আপনি?",
          [X("আপনার নাম কী?", "apnar nam ki?", "What is your name?"),
           X("ইনি কে?", "ini ke?", "Who is this (respectful)?"),
           X("আপনি কোথায় থাকেন?", "apni kothay thaken?", "Where do you live?")],
          [("আপনার নাম কী করে?", "আপনার নাম কী?", "কী asks what; কী করে asks 'doing what'."),
           ("কে আপনার নাম?", "আপনার নাম কী?", "A name is asked with কী, not কে — কে is for people as subjects.")]),
        [D("মিতা", "ইনি কে?", "ini ke?", "Who is this?"),
         D("রাতুল", "ইনি আমার বন্ধু সুমি।", "ini amar bondhu Sumi.", "This is my friend Sumi."),
         D("মিতা", "সুমি, আপনি কোথায় থাকেন?", "Sumi, apni kothay thaken?", "Sumi, where do you live?"),
         D("সুমি", "আমি মিরপুরে থাকি। আর আপনি?", "ami Mirpure thaki. ar apni?", "I live in Mirpur. And you?")],
        WS("Question worksheet", [
            T("Make the question for the answer.", ["…? আমার নাম মিতা।", "…? আমি ঢাকায় থাকি।", "…? উনি আমার ভাই।"],
              ["আপনার নাম কী?", "আপনি কোথায় থাকেন?", "উনি কে?"]),
            T("Translate to Bengali.", ["Why?", "When?", "Where?", "Who?"],
              ["কেন?", "কখন?", "কোথায়?", "কে?"]),
        ]))),
]

THIRD["A2"] = [
    ("A2-U1", "A2-U1-L3", L(
        "Time words that decide the tense: গতকাল, আজ, আগামীকাল",
        "Bengali lets the time word carry the tense: গতকাল takes a past verb, আগামীকাল a future one, "
        "আজ present or perfect. Put the time word first and the rest of the sentence follows it.",
        [V("গতকাল", "gôtokal", "yesterday", "adverb"),
         V("আজ", "aj", "today", "adverb"),
         V("আগামীকাল", "agamikal", "tomorrow", "adverb"),
         V("এখন", "ekhon", "now", "adverb"),
         V("সন্ধ্যায়", "shondhæ", "in the evening", "adverb")],
        G("Past, present, future verbs",
          "gôtokal + -লাম/-েছিলাম · aj + -ই/-ছি · agamikal + -ব/-বে",
          "গতকাল আমি বাজারে গিয়েছিলাম. আজ আমি বাড়িতে আছি. আগামীকাল আমি যাব. The -েছিলাম form "
          "means 'had gone' and is the normal past in stories; -লাম is the plain past.",
          [X("গতকাল বৃষ্টি হয়েছিল।", "gôtokal brishti hoyechhilo.", "It rained yesterday."),
           X("আজ আমি ব্যস্ত।", "aj ami bæsto.", "Today I am busy."),
           X("আগামীকাল আমরা দেখা করব।", "agamikal amra dekha kôrbo.", "Tomorrow we will meet.")],
          [("আগামীকাল আমি গিয়েছিলাম।", "আগামীকাল আমি যাব।", "A future time word cannot take a past verb."),
           ("গতকাল আমি যাব।", "গতকাল আমি গিয়েছিলাম।", "গতকাল is finished time; the verb must be past.")]),
        [D("সুমি", "গতকাল তুমি কোথায় ছিলে?", "gôtokal tumi kothay chhile?", "Where were you yesterday?"),
         D("রাতুল", "গতকাল আমি গ্রামে গিয়েছিলাম।", "gôtokal ami grame giyechhilam.", "Yesterday I went to the village."),
         D("সুমি", "আর আগামীকাল?", "ar agamikal?", "And tomorrow?"),
         D("রাতুল", "আগামীকাল আমি ফিরে আসব, সন্ধ্যায় দেখা করব।", "agamikal ami phire ashbo, shondhæ dekha kôrbo.", "Tomorrow I will come back; we'll meet in the evening.")],
        WS("Time worksheet", [
            T("Put the verb in the right time.", ["গতকাল আমি (যাওয়া)", "আজ আমি বাড়িতে (থাকা)", "আগামীকাল আমরা (দেখা করা)"],
              ["গিয়েছিলাম", "আছি", "দেখা করব"]),
            T("Answer about your own day.", ["গতকাল আপনি কী করেছিলেন?", "আগামীকাল আপনি কী করবেন?"],
              ["গতকাল আমি…", "আগামীকাল আমি…"]),
        ]))),
    ("A2-U2", "A2-U2-L3", L(
        "Postpositions: থেকে, তে, র কাছে",
        "Bengali marks place with a handful of postpositions after the noun: থেকে (from), -তে (in, "
        "at), -র কাছে (near, at someone's place), পর্যন্ত (as far as). Get these right and every "
        "journey sentence works.",
        [V("থেকে", "theke", "from", "postposition"),
         V("-তে", "-te", "in, at", "postposition"),
         V("কাছে", "kachhe", "near, at (someone's place)", "postposition"),
         V("পর্যন্ত", "pôrjonto", "up to, as far as", "postposition"),
         V("দিকে", "dike", "towards", "postposition")],
        G("Postpositions follow the noun",
          "noun + theke / -te / kachhe / pôrjonto",
          "ঢাকা থেকে খুলনা পর্যন্ত. বাড়িতে আছি. রাতুলের কাছে বইটা আছে. Postpositions come after the "
          "noun — the opposite of English — and the genitive -র attaches to people.",
          [X("আমি বাড়ি থেকে আসছি।", "ami bari theke ashchhi.", "I am coming from home."),
           X("বইটা টেবিলে আছে।", "boiṭa ṭebile achhe.", "The book is on the table."),
           X("আমার কাছে একটা প্রশ্ন আছে।", "amar kachhe ekṭa proshno achhe.", "I have a question (with me).")],
          [("আমি থেকে বাড়ি আসছি।", "আমি বাড়ি থেকে আসছি।", "The postposition follows its noun in Bengali."),
           ("টেবিলে উপর বই আছে।", "টেবিলের উপর বই আছে / টেবিলে বই আছে।", "Two place markers in one phrase is a calque; keep one.")]),
        [D("মিতা", "তুমি কোথা থেকে আসছ?", "tumi kotha theke ashchho?", "Where are you coming from?"),
         D("রাতুল", "আমি অফিস থেকে আসছি।", "ami ôfis theke ashchhi.", "I am coming from the office."),
         D("মিতা", "আর তোমার চাবি কোথায়?", "ar tomar chabi kothay?", "And where is your key?"),
         D("রাতুল", "চাবিটা আমার কাছে আছে।", "chabiṭa amar kachhe achhe.", "The key is with me.")],
        WS("Postposition worksheet", [
            T("Complete with the right postposition.", ["ঢাকা ___ খুলনা", "বইটা টেবিল___ আছে", "আমার ___ টাকা নেই"],
              ["থেকে", "এ", "কাছে"]),
            T("Answer the question.", ["তুমি কোথা থেকে আসছ?", "তোমার টাকা কোথায়?"],
              ["আমি … থেকে আসছি", "আমার কাছে …"]),
        ]))),
    ("A2-U3", "A2-U3-L3", L(
        "At the restaurant: order, eat, ask for the bill",
        "Three moves carry a meal: আমি … নেব (I'll take), আর একটু … দেবেন? (could you give a little "
        "more …?) and বিলটা দিন (give the bill). Add খুব ভালো ছিল and you can review it afterwards.",
        [V("আসব", "ashbo", "I will come; I'll have", "verb"),
         V("মেনু", "menu", "menu", "noun"),
         V("বিল", "bil", "the bill", "noun"),
         V("সুস্বাদু", "shushadu", "delicious", "adjective"),
         V("একটু", "ekṭu", "a little", "adverb")],
        G("Ordering frames",
          "ami + food + nebo/ashbo · ar ekṭu + food + deben? · bil-ṭa din",
          "আমি ভাত আর মাছ নেব। আর একটু ডাল দেবেন? বিলটা দিন। To ask what is available: এখানে কী "
          "আছে?",
          [X("আমি মুরগি আর ভাত নেব।", "ami murgi ar bhat nebo.", "I will have chicken and rice."),
           X("এখানে ইলিশ মাছ আছে?", "ekhane ilish machh achhe?", "Is there hilsa fish here?"),
           X("বিলটা দিন, দয়া করে।", "bilṭa din, dôya kôre.", "The bill, please.")],
          [("আমি মাছ খেতে হবে।", "আমি মাছ খাব।", "খেতে হবে means 'must eat'; খাব is 'I will eat'."),
           ("বিল দাও, ধন্যবাদ।", "বিলটা দিন, দয়া করে।", "Requests take দয়া করে; ধন্যবাদ belongs after receiving.")]),
        [D("ওয়েটার", "কী খাবেন?", "ki khaben?", "What will you eat?"),
         D("মিতা", "আমি ভাত আর মাছ নেব। আর একটু ডাল দেবেন?", "ami bhat ar machh nebo. ar ekṭu dal deben?", "I'll have rice and fish. Could you give a little dal too?"),
         D("ওয়েটার", "অবশ্যই। কিছু পান করবেন?", "oboshshoi. kichhu pan kôrben?", "Certainly. Anything to drink?"),
         D("মিতা", "না, ধন্যবাদ। খাবারটা সুস্বাদু, বিলটা দিন।", "na, dhonnobad. khabarṭa shushadu, bilṭa din.", "No, thank you. The food is delicious — the bill, please.")],
        WS("Restaurant worksheet", [
            T("Order in Bengali.", ["rice and fish", "a little dal", "the bill"],
              ["ভাত আর মাছ", "একটু ডাল", "বিলটা"]),
            T("Answer as the waiter.", ["any drink? (no, thanks)", "how was the food? (delicious)"],
              ["না, ধন্যবাদ", "খাবারটা সুস্বাদু ছিল"]),
        ]))),
]

THIRD["B1"] = [
    ("B1-U1", "B1-U1-L3", L(
        "Polite commands: -ুন and -বেন",
        "The polite imperative ends in -ুন (বসুন, আসুন) or -বেন for a request about the future "
        "(আসবেন, করবেন). Bengali keeps politeness in the verb ending, so the same sentence can be a "
        "friendly nudge or a formal request.",
        [V("বসুন", "boshun", "please sit", "verb"),
         V("আসুন", "ashun", "please come", "verb"),
         V("-বেন", "-ben", "polite future/request ending", "suffix"),
         V("অনুরোধ", "onurodh", "request", "noun"),
         V("অনুমতি", "onumoti", "permission", "noun")],
        G("Politeness lives in the ending",
          "verb + -un (now) · verb + -ben (later, or a request)",
          "একটু বসুন. কাল আসবেন. The same verb with -বেন becomes a request about the future: আপনি একটু "
          "অপেক্ষা করবেন? — softer than করুণ.",
          [X("একটু অপেক্ষা করুন।", "ekṭu opekkha kôrun.", "Please wait a moment."),
           X("আপনি কাল সকালে আসবেন।", "apni kal shokale ashben.", "You will come tomorrow morning. (also a polite request)"),
           X("আমি আপনার অনুমতি চাই।", "ami apnar onumoti chai.", "I ask your permission.")],
          [("আপনি বসো।", "আপনি বসুন।", "আপনি takes -ুন/-বেন; বসো belongs with তুমি."),
           ("দয়া করে করবেন আসুন।", "দয়া করে আসুন।", "One politeness marker per sentence is enough.")]),
        [D("মিতা", "দয়া করে একটু বসুন।", "dôya kôre ekṭu boshun.", "Please sit down a moment."),
         D("রাতুল", "ধন্যবাদ। বলুন, কী দরকার?", "dhonnobad. bolun, ki dorkar?", "Thanks. Tell me, what is needed?"),
         D("মিতা", "কাল সকালে অফিসে আসবেন, একটা কাজ আছে।", "kal shokale ôfise ashben, ekṭa kaj achhe.", "Please come to the office tomorrow morning — there is some work."),
         D("রাতুল", "ঠিক আছে, আমি নয়টায় আসব।", "ṭhik achhe, ami nôyṭay ashbo.", "All right, I will come at nine.")],
        WS("Polite request worksheet", [
            T("Make it polite.", ["বসো। → (আপনি)", "একটু অপেক্ষা করো। → (আপনি)", "কাল আসো। → (আপনি)"],
              ["বসুন", "একটু অপেক্ষা করুন", "কাল আসবেন"]),
            T("Ask for permission.", ["to leave early", "to speak"],
              ["আমি একটু আগে যেতে পারি?", "আমি কি বলতে পারি?"]),
        ]))),
    ("B1-U2", "B1-U2-L3", L(
        "Family, age and the possessive",
        "Bengali kinship is exact: বাবা, মা, দাদা, দিদি, জ্যাঠা, মামা — each relative has a name and a "
        "side of the family. Possession is shown with -র (আমার, তোমার, তার) and age asks কত বছর.",
        [V("বাবা", "baba", "father", "noun"),
         V("মা", "ma", "mother", "noun"),
         V("দাদা", "dada", "elder brother", "noun"),
         V("দিদি", "didi", "elder sister", "noun"),
         V("বয়স", "bôyosh", "age", "noun")],
        G("Possessive endings",
          "ami→amar · tumi→tomar · apni→apnar · she→tar",
          "আমার দুই ভাই আছে. আমার বাবার নাম করিম. Age: আমার বয়স পঁচিশ বছর / আমার পঁচিশ বছর বয়স.",
          [X("আমার বাবা ঢাকায় থাকেন।", "amar baba Dhakay thaken.", "My father lives in Dhaka."),
           X("তার দিদি শিক্ষক।", "tar didi shikkhok.", "His elder sister is a teacher."),
           X("আপনার বয়স কত?", "apnar bôyosh kôto?", "How old are you?")],
          [("আমার পঁচিশ বছরের।", "আমার বয়স পঁচিশ বছর।", "Age takes বছর directly, not the genitive."),
           ("আমি দুই ভাই আছি।", "আমার দুই ভাই আছে।", "Existence is expressed as 'my two brothers are' — আমার … আছে.")]),
        [D("সুমি", "আপনার পরিবারে কত জন?", "apnar poribare kôto jon?", "How many people are in your family?"),
         D("রাতুল", "আমাদের চার জন — বাবা, মা, দিদি আর আমি।", "amader char jon — baba, ma, didi ar ami.", "There are four of us — father, mother, elder sister and me."),
         D("সুমি", "আর আপনার দিদির বয়স কত?", "ar apnar didir bôyosh kôto?", "And how old is your elder sister?"),
         D("রাতুল", "উনার ত্রিশ বছর, উনি একটা স্কুলে পড়ান।", "unar trish bôchhor, uni ekṭa skule poran.", "She is thirty; she teaches in a school.")],
        WS("Family worksheet", [
            T("Answer with -র.", ["my father's name", "his elder brother", "your (apni) family"],
              ["আমার বাবার নাম", "তার দাদা", "আপনার পরিবার"]),
            T("Talk about your family in two sentences.", ["(how many people)", "(what one of them does)"],
              ["আমাদের পরিবারে … জন", "আমার … … করেন"]),
        ]))),
    ("B1-U3", "B1-U3-L3", L(
        "Disagreeing without heat: আমার মনে হয়… তবে",
        "Bengali disagreement usually starts with agreement or a softener: আমার মনে হয় (I think), "
        "ঠিক আছে কিন্তু (true, but), তবে (however), একমত নই (I don't agree). The grammar is simple; "
        "the order is the politeness.",
        [V("মনে হয়", "mone hôy", "I think, it seems", "phrase"),
         V("তবে", "tôbe", "however", "conjunction"),
         V("একমত", "ekmot", "in agreement", "adjective"),
         V("আপত্তি", "apotti", "objection", "noun"),
         V("মতামত", "môtamot", "opinion", "noun")],
        G("Soften, then differ",
          "amar mone hôy… · ṭhik achhe, tôbe… · ami ekmot noi",
          "আমার মনে হয় এটা ঠিক, তবে খরচ বেশি. ঠিক আছে, কিন্তু সময় লাগবে. One concession, one "
          "disagreement, no third clause.",
          [X("আমার মনে হয় এটা ভালো হবে।", "amar mone hôy eṭa bhalo hobe.", "I think this will be good."),
           X("ঠিক আছে, তবে আমাদের সময় কম।", "ṭhik achhe, tôbe amader shômoy kôm.", "True, but we have little time."),
           X("আমি এই প্রস্তাবে একমত নই।", "ami ei prostabe ekmot noi.", "I do not agree with this proposal.")],
          [("আমার মনে হয় না এটা ভালো হবে।", "আমার মনে হয় এটা ভালো হবে না।", "Negating মনে হয় says 'it doesn't seem'; negate the inner clause to disagree with it."),
           ("আমি একমত নই না।", "আমি একমত নই।", "Bengali has one negative here; doubling is not emphasis.")]),
        [D("মিতা", "আমার মনে হয় বাড়িটা কেনা উচিত।", "amar mone hôy bariṭa kena uchit.", "I think we should buy the house."),
         D("রাতুল", "ঠিক আছে, তবে দাম অনেক বেশি।", "ṭhik achhe, tôbe dam ônek beshi.", "True, but the price is far too high."),
         D("মিতা", "তাহলে আপনার মত কী?", "tahole apnar môt ki?", "Then what is your opinion?"),
         D("রাতুল", "আমার মনে হয় আরও কিছুদিন দেখা উচিত।", "amar mone hôy aro kichhudin dekha uchit.", "I think we should look for some more days.")],
        WS("Opinion worksheet", [
            T("Soften the disagreement.", ["এটা ভুল।", "এই প্রস্তাব ভালো নয়।"],
              ["আমার মনে হয় এটা ঠিক নয়", "ঠিক আছে, তবে আমার কিছু আপত্তি আছে"]),
            T("Give your own opinion.", ["a plan you like", "a plan you doubt"],
              ["আমার মনে হয় … উচিত", "আমি … একমত নই, কারণ …"]),
        ]))),
]

THIRD["B2"] = [
    ("B2-U1", "B2-U1-L3", L(
        "Conditions and wishes: যদি… তাহলে, ইচ্ছা থাকলে",
        "Bengali conditions run on two frames: যদি + condition, তাহলে + result for real conditions, "
        "and past-conditioned হলে for unreal ones. Wishes use ইচ্ছা (desire) or হলেই ভালো হতো.",
        [V("যদি", "jodi", "if", "conjunction"),
         V("তাহলে", "tahole", "then", "conjunction"),
         V("হলে", "hole", "if it were, in that case", "conjunction"),
         V("ইচ্ছা", "ichchha", "wish, desire", "noun"),
         V("শর্ত", "shôrto", "condition", "noun")],
        G("Real and unreal",
          "jodi + clause, tahole + result (real) · … hole … (unreal or polite)",
          "যদি সময় থাকে, তাহলে আমি আসব. আমি যদি চাইতাম, তাহলে আসতাম. A formal request can hide in "
          "hole: আপনার অনুমতি হলে আমি শুরু করি.",
          [X("যদি টাকা থাকে, আমি কিনব।", "jodi ṭaka thake, ami kinbo.", "If I have the money, I'll buy it."),
           X("সময় হলে আমরা দেখা করব।", "shômoy hole amra dekha kôrbo.", "If there is time, we will meet."),
           X("আমার ইচ্ছা যাতে সবাই একমত হয়।", "amar ichchha jate shobai ekmot hôy.", "My wish is that everyone agrees.")],
          [("যদি আমি আসি, তখন আমি দেখব।", "যদি আমি আসি, তাহলে দেখব।", "The pair is যদি… তাহলে; তখন is 'at that time'."),
           ("যদি টাকা ছিল, আমি কিনেছি।", "যদি টাকা থাকত, আমি কিনতাম।", "An unreal condition needs থাকত/কিনতাম, not real past forms.")]),
        [D("মিতা", "যদি বৃষ্টি হয়, তাহলে আমরা যাব না।", "jodi brishti hôy, tahole amra jabo na.", "If it rains, we won't go."),
         D("রাতুল", "আর যদি বৃষ্টি না হয়?", "ar jodi brishti na hôy?", "And if it doesn't rain?"),
         D("মিতা", "তাহলে সন্ধ্যায় দেখা করব।", "tahole shondhæ dekha kôrbo.", "Then we'll meet in the evening."),
         D("রাতুল", "আমারও ইচ্ছা সেটাই।", "amaroo ichchha sheṭai.", "That is my wish too.")],
        WS("Condition worksheet", [
            T("Finish the condition.", ["যদি সময় থাকে, …", "যদি তিনি আসেন, …", "যদি দাম কম হয়, …"],
              ["তাহলে আমি আসব", "তাহলে শুরু করব", "তাহলে কিনব"]),
            T("Say the unreal one.", ["if I had known, I would have come", "if he had asked, I would have said yes"],
              ["যদি আমি জানতাম, আমি আসতাম", "যদি তিনি চাইতেন, আমি হাঁ বলতাম"]),
        ]))),
    ("B2-U2", "B2-U2-L3", L(
        "How sure are you? Certainty in Bengali",
        "Bengali grades certainty with a small ladder: নিশ্চিত (certain), সম্ভবত (probably), হয়তো "
        "(perhaps), মনে হয় (it seems). In reports the impersonal frame is expected: বলা হয়েছে, মনে করা "
        "হচ্ছে.",
        [V("নিশ্চিত", "nishchito", "certain", "adjective"),
         V("সম্ভবত", "shombhôboto", "probably", "adverb"),
         V("হয়তো", "hôyto", "perhaps", "adverb"),
         V("মনে করা", "mone kôra", "to think, to consider", "verb"),
         V("প্রমাণ", "proman", "proof, evidence", "noun")],
        G("Certainty ladder",
          "nishchito > shombhôboto > hôyto > mone hôy",
          "এটা নিশ্চিত নয়, তবে সম্ভবত আমরা সময়মতো শেষ করব. হয়তো একদিন দেরি হবে. Reports: মনে করা "
          "হচ্ছে যে দাম বাড়বে.",
          [X("আমি নিশ্চিত যে সে আসবে।", "ami nishchito je she ashbe.", "I am certain that he will come."),
           X("সম্ভবত আগামী সপ্তাহে কাজ শেষ হবে।", "shombhôboto agami shoptahe kaj shesh hobe.", "The work will probably finish next week."),
           X("হয়তো সে এখনো আসেনি।", "hôyto she ekhono asheni.", "Perhaps he has not come yet.")],
          [("সম্ভবত নিশ্চিত।", "(use one degree of certainty)", "Two certainty words cancel each other."),
           ("এটা প্রমাণ যে দাম বাড়বে।", "এটা সম্ভবত ঘটবে; প্রমাণ এখনো নেই।", "A forecast is not proof — keep প্রমাণ for evidence.")]),
        [D("মিতা", "আপনি কি নিশ্চিত যে কাজ শেষ হবে?", "apni ki nishchito je kaj shesh hobe?", "Are you certain the work will be finished?"),
         D("রাতুল", "নিশ্চিত নই, তবে সম্ভবত আগামী সপ্তাহে শেষ হবে।", "nishchito noi, tôbe shombhôboto agami shoptahe shesh hobe.", "Not certain, but it will probably finish next week."),
         D("মিতা", "এবং খরচ?", "ebong khôroch?", "And the cost?"),
         D("রাতুল", "হয়তো কিছুটা বাড়বে — এখনো প্রমাণ নেই।", "hôyto kichhuṭa barbe — ekhono proman nei.", "Perhaps it will rise a little — there is no evidence yet.")],
        WS("Certainty worksheet", [
            T("Place it on the ladder.", ["certain: he will come", "probably: the price rises", "perhaps: a delay"],
              ["আমি নিশ্চিত যে সে আসবে", "সম্ভবত দাম বাড়বে", "হয়তো দেরি হবে"]),
            T("Soften the claim.", ["দাম বাড়বে। (probably)", "লোকসান হবে। (perhaps)"],
              ["সম্ভবত দাম বাড়বে", "হয়তো লোকসান হবে"]),
        ]))),
    ("B2-U3", "B2-U3-L3", L(
        "Telling it the Bengali way: ছোট গল্পের কাঠামো",
        "A Bengali anecdote sets the scene, turns on one small event, and closes with a saying. The "
        "frame: একদিন… (one day), তারপর… (then), হঠাৎ… (suddenly), আর শেষে… (and at the end). The "
        "saying at the close is what makes it a story rather than a report.",
        [V("একদিন", "ekdin", "one day", "phrase"),
         V("হঠাৎ", "haṭhat", "suddenly", "adverb"),
         V("শেষে", "sheshe", "at the end", "adverb"),
         V("গল্প", "gôlpo", "story", "noun"),
         V("প্রবাদ", "probad", "proverb", "noun")],
        G("Story frame",
          "ekdin… · tarpor… · haṭhat… · sheshe… + a proverb",
          "একদিন আমি বাজারে গিয়েছিলাম. তারপর হঠাৎ বৃষ্টি শুরু হলো. শেষে আমি ভিজে বাড়ি ফিরলাম — "
          "সত্যিই, বিনা মেঘে বজ্রপাত! One turn, one saying.",
          [X("একদিন গ্রামে একটা বাঘ এসেছিল।", "ekdin grame ekṭa bagh eshechhilo.", "One day a tiger came to the village."),
           X("হঠাৎ সবাই চুপ হয়ে গেল।", "haṭhat shobai chup hôye gelo.", "Suddenly everyone fell silent."),
           X("শেষে সবাই একমত হলো যে ভয়টা বাড়িয়ে বলা হয়েছিল।", "sheshe shobai ekmot hôlo je bhoyṭa bariye bôla hoyechhilo.", "In the end everyone agreed the fear had been exaggerated.")],
          [("একদিন, তারপর, হঠাৎ।", "(one marker per sentence)", "Markers are sentences' work; a chain of them is not a story."),
           ("শেষে আমি ভিজে ভিজে ভিজে ফিরলাম।", "শেষে আমি ভিজে বাড়ি ফিরলাম।", "Bengali repeats a word for emphasis rarely; here it just reads as a stutter.")]),
        [D("সুমি", "একটা গল্প বলুন!", "ekṭa gôlpo bolun!", "Tell a story!"),
         D("রাতুল", "একদিন আমি ট্রেন ধরতে গিয়েছিলাম।", "ekdin ami ṭren dhôrte giyechhilam.", "One day I went to catch a train."),
         D("সুমি", "তারপর?", "tarpor?", "Then?"),
         D("রাতুল", "হঠাৎ ট্রেন চলে গেল, আর শেষে আমাকে বাসে যেতে হলো — যাওয়ার আগেই দেখে নেওয়া উচিত ছিল!", "haṭhat ṭren chôle gelo, ar sheshe amake base jete hôlo — jaoyar agei dekhe neoya uchit chhilo!", "Suddenly the train left, and in the end I had to go by bus — I should have checked before leaving!")],
        WS("Story worksheet", [
            T("Build the frame.", ["set the scene", "the turn", "the close"],
              ["একদিন…", "হঠাৎ…", "শেষে…"]),
            T("Add the saying.", ["something went wrong quietly", "an unexpected shock"],
              ["শাক দিয়ে মাছ ঢাকা", "বিনা মেঘে বজ্রপাত"]),
        ]))),
]

THIRD["C1"] = [
    ("bn-c1-u1", "bn-c1-l7", L(
        "Attribution: report a claim without vouching for it",
        "A formal Bengali text moves the truth into the source's mouth: বলা হয়েছে (it has been said), "
        "সূত্র জানিয়েছে (the source has informed), দাবি করা হয়েছে (it has been claimed), "
        "সূত্রানুসারে (according to the source). The claim stays the source's; you stay accurate.",
        [V("বলা হয়েছে", "bôla hoyechhe", "it has been said", "phrase"),
         V("দাবি করা", "dabi kôra", "to claim", "verb"),
         V("সূত্রানুসারে", "shutranushare", "according to the source", "adverb"),
         V("জানানো", "janano", "to inform", "verb"),
         V("মতে", "môte", "according to (someone's view)", "postposition")],
        G("Distance by frame",
          "bôla hoyechhe je… · shutra janiyechhe je… · dabi kôra hoyechhe je… · …-er môte",
          "সূত্র জানিয়েছে যে চুক্তিটি প্রায় চূড়ান্ত. বিশেষজ্ঞদের মতে দাম আরও বাড়বে. The frame does "
          "not make the claim true; it makes clear who owns it.",
          [X("প্রতিবেদনে বলা হয়েছে যে চাহিদা বাড়ছে।", "protibedone bôla hoyechhe je chahida barchhe.", "The report says that demand is rising."),
           X("কর্তৃপক্ষ দাবি করেছে যে নিয়ম মানা হচ্ছে।", "kôrtripôkkho dabi korechhe je niyom mana hôchhe.", "The authorities have claimed the rules are being followed."),
           X("সূত্রানুসারে, সভা আগামী সপ্তাহে হবে।", "shutranushare, shobha agami shoptahe hobe.", "According to the source, the meeting will be next week.")],
          [("প্রতিবেদনে বলা হয়েছে যে চাহিদা বাড়ছে, তাই এটা প্রমাণ।", "প্রতিবেদনে বলা হয়েছে যে চাহিদা বাড়ছে; এটা এখনো প্রমাণ নয়।", "A report is a source, not a proof — keep the frame."),
           ("সূত্র অনুসারে জানানো দাবি করেছে।", "সূত্র জানিয়েছে / সূত্র দাবি করেছে।", "Pick one reporting verb; stacking three turns the sentence into noise.")]),
        [D("সম্পাদক", "মন্ত্রী কি সত্যিই রাজি হয়েছেন?", "montri ki shôttii raji hoyechhen?", "Has the minister really agreed?"),
         D("সাংবাদিক", "সূত্র জানিয়েছে যে তিনি নীতিগতভাবে রাজি।", "shutra janiyechhe je tini nitigôtobhabe raji.", "The source says he is agreeable in principle."),
         D("সম্পাদক", "আমরা কি নিশ্চিত করে লিখব?", "amra ki nishchito kôre likhbo?", "Shall we write it as confirmed?"),
         D("সাংবাদিক", "না — লিখি «সূত্রানুসারে তিনি রাজি», এবং সেটাই সৎ।", "na — likhi «shutranushare tini raji», ebong sheṭai shôt.", "No — we write 'according to the source he is agreeable', and that is honest.")],
        WS("Attribution worksheet", [
            T("Move the claim into a frame.", ["dam will rise (a source)", "the deal is signed (the ministry)"],
              ["সূত্র জানিয়েছে যে দাম বাড়বে", "মন্ত্রণালয় জানিয়েছে যে চুক্তি স্বাক্ষরিত হয়েছে"]),
            T("Downgrade the certainty.", ["the agreement is ready (according to a report)", "he agreed (claim)"],
              ["প্রতিবেদন অনুসারে চুক্তি প্রায় তৈরি", "দাবি করা হয়েছে যে তিনি রাজি হয়েছেন"]),
        ]))),
    ("bn-c1-u2", "bn-c1-l8", L(
        "Qualification: how far does the claim reach?",
        "Precision means naming the scope: বেশিরভাগ ক্ষেত্রে (in most cases), কিছুটা (somewhat), "
        "ব্যতিক্রম ছাড়া নয় (not without exception), মানে এই নয় যে (it does not mean that). Bengali "
        "formal prose marks scope with these phrases, and dropping them is what turns a finding into "
        "an overclaim.",
        [V("বেশিরভাগ ক্ষেত্রে", "beshirbhag kkhetre", "in most cases", "phrase"),
         V("কিছুটা", "kichhuṭa", "somewhat", "adverb"),
         V("ব্যতিক্রম", "bettikrom", "exception", "noun"),
         V("ব্যাপ্তি", "bepti", "extent, scope", "noun"),
         V("মানে এই নয় যে", "mane ei nôy je", "it does not mean that", "phrase")],
        G("Scope limiters",
          "beshirbhag kkhetre · kichhuṭa · bettikrom soho · mane ei nôy je…",
          "ফলাফল বেশিরভাগ ক্ষেত্রে ইতিবাচক, তবে একটি খাত ব্যতিক্রম. কিছুটা উন্নতি হয়েছে, বিপ্লব নয়. "
          "দাম বাড়া মানে এই নয় যে চাহিদা কমেছে.",
          [X("রিপোর্টটি বেশিরভাগ ক্ষেত্রে সঠিক।", "ripôrṭṭi beshirbhag kkhetre shôtik.", "The report is accurate in most cases."),
           X("উন্নতির ব্যাপ্তি সীমিত।", "unnôtir bepti shimito.", "The extent of the improvement is limited."),
           X("একটি ব্যতিক্রম ছাড়া সব খাত লাভজনক।", "ekṭa bettikrom chhara shôb khat labhjônok.", "All sectors are profitable except one.")],
          [("ফলাফল ভালো, ব্যতিক্রম।", "ফলাফল বেশিরভাগ ক্ষেত্রে ভালো; একটি ক্ষেত্রে ব্যতিক্রম।", "An exception must be named and its scope set."),
           ("দাম বাড়ছে, তাই সব শেষ।", "দাম বাড়ছে; এর মানে এই নয় যে চাহিদা কমেছে।", "Naming the false inference is how a careful analyst writes.")]),
        [D("পরিচালক", "ফলাফল কেমন?", "pholafol kemon?", "How are the results?"),
         D("বিশ্লেষক", "বেশিরভাগ ক্ষেত্রে ভালো, তবে দুইটি খাতে ব্যতিক্রম।", "beshirbhag kkhetre bhalo, tôbe duiṭi khate bettikrom.", "Good in most cases, but with exceptions in two sectors."),
         D("পরিচালক", "তাহলে কি পরিকল্পনা ব্যর্থ?", "tahole ki porikôlpona bertho?", "So is the plan a failure?"),
         D("বিশ্লেষক", "না — কিছুটা দেরি মানে এই নয় যে পরিকল্পনা ব্যর্থ।", "na — kichhuṭa deri mane ei nôy je porikôlpona bertho.", "No — a little delay does not mean the plan failed.")],
        WS("Scope worksheet", [
            T("Limit the claim.", ["sales rose (about 3%)", "the news is true (in most cases)"],
              ["বিক্রি কিছুটা বেড়েছে, প্রায় ৩%", "খবরটি বেশিরভাগ ক্ষেত্রে সঠিক"]),
            T("Refuse the false inference.", ["we are late, so the project failed", "one share fell, so the company is in danger"],
              ["দেরি হওয়া মানে এই নয় যে প্রকল্প ব্যর্থ", "একটি শেয়ার পড়া মানে এই নয় যে কোম্পানি বিপদে"]),
        ]))),
    ("bn-c1-u3", "bn-c1-l9", L(
        "Genre transform: memo to press release",
        "The same facts read differently in a memo and a press release. The memo is impersonal and "
        "internal (সিদ্ধান্ত গৃহীত হয়েছে); the release names the actor and speaks outward "
        "(কোম্পানি জানিয়েছে). Transforming without losing a fact is the C1 skill.",
        [V("স্মারকলিপি", "smôrokolipi", "memorandum", "noun"),
         V("প্রেস বিজ্ঞপ্তি", "pres bijnopti", "press release", "noun"),
         V("খসড়া", "khôsra", "draft", "noun"),
         V("পরিমার্জন", "porimarjon", "revision, refinement", "noun"),
         V("স্বাক্ষর", "shakkhor", "signature", "noun")],
        G("Impersonal memo → named release",
          "memo: siddhanto grihito hoyechhe · release: [actor] janiyechhe je…",
          "স্মারকলিপি: বাজেট অনুমোদিত হয়েছে। বিজ্ঞপ্তি: কোম্পানি বাজেট অনুমোদন করেছে। Same fact, "
          "the actor is named, and the sentence gets shorter.",
          [X("খসড়াটি আজ পরিমার্জন করা হয়েছে।", "khôsraṭi aj porimarjon kôra hoyechhe.", "The draft was revised today. (memo)"),
           X("কমিটি আজ খসড়াটি পরিমার্জন করেছে।", "kômiti aj khôsraṭi porimarjon korechhe.", "The committee revised the draft today. (release)"),
           X("বিজ্ঞপ্তিতে বলা হয়েছে যে প্রকল্প সেপ্টেম্বরে শুরু হবে।", "bijnoptite bôla hoyechhe je prokolpo Sepṭembôre shuru hobe.", "The release states the project begins in September.")],
          [("পরিমার্জন করা হয়েছে খসড়াটি কমিটি দ্বারা।", "কমিটি খসড়াটি পরিমার্জন করেছে।", "Bengali prefers the active and puts the actor first in public text."),
           ("কমিটি করা হয়েছে পরিমার্জন।", "কমিটি খসড়াটি পরিমার্জন করেছে।", "One verb, one subject, in that order.")]),
        [D("প্রধান", "স্মারকলিপি থেকে বিজ্ঞপ্তি বানাতে হবে।", "smôrokolipi theke bijnopti banate hobe.", "We need to turn the memo into a release."),
         D("লেখক", "পাঠক কে? স্মারকলিপি ভিতরের, বিজ্ঞপ্তি বাইরের।", "pathok ke? smôrokolipi bhitorer, bijnopti bairer.", "Who is the reader? The memo is internal, the release is external."),
         D("প্রধান", "অতএব কর্তা নাম দিন, আর বাক্য ছোট করুন।", "ôtôebô kôrta nam din, ar bakko chhôṭo kôrun.", "So name the actor and shorten the sentences."),
         D("লেখক", "«অনুমোদিত হয়েছে» বদলে «কমিটি অনুমোদন করেছে»।", "«onumodito hoyechhe» bôdle «kômiti onumodon korechhe».", "'Has been approved' becomes 'the committee approved'.")],
        WS("Transform worksheet", [
            T("Memo line → release line.", ["সিদ্ধান্ত গৃহীত হয়েছে।", "অনুমোদন দেওয়া হয়েছে।"],
              ["কমিটি সিদ্ধান্ত নিয়েছে", "কর্তৃপক্ষ অনুমোদন দিয়েছে"]),
            T("Trim the padding.", ["সম্পাদন করা হয়েছে পরিমার্জনের কাজ।", "গৃহীত হয়েছে সিদ্ধান্ত।"],
              ["নথিটি পরিমার্জন করা হয়েছে", "সিদ্ধান্ত নেওয়া হয়েছে"]),
        ]))),
]

THIRD["C2"] = [
    ("bn-c2-u1", "bn-c2-l7", L(
        "Implicature: what the text says without saying",
        "A C2 reader reads the gap. ইঙ্গিত (hint), বোঝা যায় (it can be understood), পরোক্ষভাবে "
        "(indirectly), সম্ভাব্য অর্থ (probable meaning) let you name the inference — and then hold it "
        "to account instead of reporting it as a statement.",
        [V("ইঙ্গিত", "inggito", "hint, indication", "noun"),
         V("বোঝা যায়", "bôjha jay", "it can be understood", "phrase"),
         V("পরোক্ষভাবে", "pôrokkhobhabe", "indirectly", "adverb"),
         V("সম্ভাব্য", "shombhabbo", "probable, possible", "adjective"),
         V("অনুমান", "onuman", "inference, guess", "noun")],
        G("Name the inference, keep it an inference",
          "bôjha jay je… · inggito achhe je… · onuman kôra jay je…",
          "তৃতীয় অনুচ্ছেদ থেকে বোঝা যায় যে লেখক সংখ্যা নিয়ে সন্দিহান — তবে তিনি তা সরাসরি লেখেননি. "
          "Naming it is not asserting it: keep বোঝা যায়, and the paragraph stays honest.",
          [X("শিরোনাম থেকে ইঙ্গিত পাওয়া যায় যে সিদ্ধান্ত বদলেছে।", "shironam theke inggito paoa jay je siddhanto bôdolechhe.", "The headline hints that the decision has changed."),
           X("লেখক পরোক্ষভাবে দুর্নীতির কথা বলেছেন।", "lekhok pôrokkhobhabe durnitir kôtha bolechhen.", "The writer spoke indirectly of corruption."),
           X("অনুমান করা যায় যে সময়সীমা মানা হবে না।", "onuman kôra jay je shômoy-shima mana hobe na.", "It can be inferred that the deadline will not be met.")],
          [("লেখক বলেছেন যে দুর্নীতি হয়েছে।", "লেখক পরোক্ষভাবে দুর্নীতির ইঙ্গিত দিয়েছেন।", "Reporting a hint as a statement is the classic over-reading."),
           ("বোঝা যায় যে লেখক মিথ্যা বলেছেন।", "বোঝা যায় যে লেখক সংখ্যা নিয়ে সন্দিহান।", "Inference must stay within what the text supports.")]),
        [D("পাঠক", "লেখক কি বলেছেন যে মন্ত্রী মিথ্যা বলেছেন?", "lekhok ki bolechhen je montri miththa bolechhen?", "Did the writer say the minister lied?"),
         D("সম্পাদক", "সরাসরি বলেননি; বোঝা যায় যে তিনি সন্দিহান।", "shorasori bolen ni; bôjha jay je tini shondihan.", "Not directly; it is understood that he is doubtful."),
         D("পাঠক", "তাহলে শিরোনামটা বেশি দাবি করছে।", "tahole shironamṭa beshi dabi kôrchhe.", "Then the headline claims too much."),
         D("সম্পাদক", "ঠিক, আর সেটাই পাঠকের পরীক্ষা।", "ṭhik, ar sheṭai pathoker porikkha.", "Right — and that is the reader's test.")],
        WS("Inference worksheet", [
            T("Name the inference, keep it an inference.", ["the writer repeats 'some sources' (doubt)", "no date is given (something is avoided)"],
              ["বোঝা যায় যে লেখক সূত্র নিয়ে সন্দিহান", "তারিখ না থাকা ইঙ্গিত দেয় যে লেখক স্পষ্টতা এড়াচ্ছেন"]),
            T("Correct the over-reading.", ["the text says the company will close", "the text says the minister is angry"],
              ["বোঝা যায় কোম্পানি সমস্যায়, বন্ধ হওয়ার কথা বলা হয়নি", "লেখকের ইঙ্গিত মন্ত্রীর অসন্তোষের, সরাসরি নয়"]),
        ]))),
    ("bn-c2-u2", "bn-c2-l8", L(
        "Figures a headline can carry: উপমা, অনুপ্রাস, শ্লেষ",
        "Bengali rhetoric names its own figures: উপমা (simile), রূপক (metaphor), অনুপ্রাস "
        "(alliteration), শ্লেষ (pun, irony). A headline carries one — two turns it into a slogan, "
        "three into a parody. Judging that line is the C2 edit.",
        [V("উপমা", "upoma", "simile", "noun"),
         V("রূপক", "rupok", "metaphor", "noun"),
         V("অনুপ্রাস", "onuprash", "alliteration", "noun"),
         V("শ্লেষ", "shlesh", "pun, irony", "noun"),
         V("চিত্র", "chitro", "image, figure", "noun")],
        G("One figure per headline",
          "upoma: X er môto Y · rupok: X-i Y · onuprash: repeated initial sound",
          "বাজেট এখন রাবণের চিতা — রূপক. «যেখানে উপমা বেশি, সেখানে হিসাব কম» — শ্লেষ. The figure "
          "frames the argument before the reader judges it, so an editor asks: does the frame help "
          "them think, or decide for them?",
          [X("পদ্মা এখন সোনার নদী।", "pôdma ekhon shonar nodi.", "The Padma is now a river of gold. (metaphor)"),
           X("শহর নিঃশব্দ, শোকের সন্ধ্যা।", "shôhor nishshôbdo, shoker shondha.", "The city silent, an evening of mourning. (alliteration)"),
           X("বড় প্রতিশ্রুতি, ছোট হিসাব।", "bôr protishruti, chhôṭ hishab.", "Big promise, small accounting. (antithesis)")],
          [("উপমা: নদী সোনার মতো, রূপক: নদী সোনা, অনুপ্রাস: নদী নয়।", "(one figure per headline)", "Three figures in one line fight each other; the reader takes none."),
           ("শিরোনামে শ্লেষ, খবরে শ্লেষ, সম্পাদকীয়তেও শ্লেষ।", "শ্লেষ একবারই — বাকিটা তথ্য।", "Irony used three times stops being irony and becomes the house style.")]),
        [D("সম্পাদক", "শিরোনামে কয়টা চিত্র আছে?", "shironame kôyṭa chitro achhe?", "How many figures are in the headline?"),
         D("লেখক", "দুইটা — উপমা আর অনুপ্রাস।", "duiṭa — upoma ar onuprash.", "Two — a simile and alliteration."),
         D("সম্পাদক", "একটা রাখুন, নইলে পাঠক কিছুই মনে রাখবে না।", "ekṭa rakhun, noile pathok kichhui mone rakhbe na.", "Keep one, or the reader will remember none."),
         D("লেখক", "রূপকটা রাখি, অনুপ্রাস বাদ।", "rupokṭa rakhi, onuprash bad.", "I'll keep the metaphor, drop the alliteration.")],
        WS("Figure worksheet", [
            T("Build one figure.", ["the market / silent", "promise / account"],
              ["বাজার এখন নিঃশব্দ", "বড় প্রতিশ্রুতি, ছোট হিসাব"]),
            T("Cut three figures down to one.", ["a metaphor, a pun and alliteration in one line"],
              ["একটি চিত্রই যথেষ্ট; বাকিটা বাদ"]),
        ]))),
    ("bn-c2-u3", "bn-c2-l9", L(
        "Correcting an expert without losing them",
        "The last skill is social. Bengali gives a staircase: আপনি ঠিক, তবে… (you are right, "
        "however), আমি একমত, শুধু একটা বিষয় (I agree, just one thing), আমি অন্যভাবে দেখি (I see it "
        "differently), আবার বলি (let me restate). Each step keeps the person and moves the claim.",
        [V("আপনি ঠিক", "apni ṭhik", "you are right", "phrase"),
         V("শুধু একটা বিষয়", "shudhu ekṭa bishôy", "just one thing", "phrase"),
         V("অন্যভাবে দেখা", "ônnobhabe dekha", "to see differently", "phrase"),
         V("পুনরাবৃত্তি", "punorabritti", "repetition, restatement", "noun"),
         V("সংশোধন", "shôngshodhon", "correction", "noun")],
        G("The correction staircase",
          "apni ṭhik, tôbe… → shudhu ekṭa bishôy → ami ônnobhabe dekhi → abar boli…",
          "আপনি ঠিক, তথ্যগুলো সঠিক — শুধু একটা বিষয়: ব্যাখ্যাটা ভিন্ন হতে পারে. Restating the other "
          "person's point in your own words before touching it is the move that keeps the room.",
          [X("আপনি ঠিক, তবে ব্যাখ্যাটা ভিন্ন।", "apni ṭhik, tôbe bekkhatা bhinn.", "You are right, but the interpretation is different."),
           X("আমি অন্যভাবে দেখি — কারণটা এক নয়, দুই।", "ami ônnobhabe dekhi — karônṭa ek nôy, dui.", "I see it differently — the cause is not one, but two."),
           X("আবার বলি, আমরা লক্ষ্যে একমত।", "abar boli, amra lokkhe ekmot.", "Let me restate: we agree on the goal.")],
          [("আপনি ভুল, তথ্য ভুল।", "আপনি ঠিক, তথ্যও সঠিক — শুধু ব্যাখ্যায় আমি ভিন্ন মত পোষণ করি।", "A flat contradiction loses the room and the argument."),
           ("আপনি ঠিক, তবে আপনি সব ভুল।", "আপনি ঠিক, তবে একটা বিষয়ে আমি ভিন্নমত।", "A concession cancelled in the same breath is worse than none.")]),
        [D("বিশেষজ্ঞ", "সমস্যাটা তাই সহজ — একটাই কারণ।", "shomoshshaṭa tai shohoj — ekṭai karôn.", "So the problem is simple — one cause."),
         D("পরিচালক", "আপনি ঠিক, তথ্যগুলো স্পষ্ট। শুধু একটা বিষয় — ব্যাখ্যা?", "apni ṭhik, tôthygulo shpôshṭo. shudhu ekṭa bishôy — bekkha?", "You are right, the data is clear. Just one thing — the interpretation?"),
         D("বিশেষজ্ঞ", "বলুন।", "bolun.", "Go on."),
         D("পরিচালক", "আমি অন্যভাবে দেখি: কারণ এক, কিন্তু প্রভাব দুই জায়গায়।", "ami ônnobhabe dekhi: karôn ek, kintu probhab dui jaygay.", "I see it differently: one cause, but effects in two places.")],
        WS("Correction worksheet", [
            T("Climb the staircase.", ["you are wrong about the cost", "that number cannot be right"],
              ["আপনি ঠিক, তবে খরচের হিসাবটা ভিন্নভাবে দেখা দরকার", "দয়া করে সূত্রটা দেখি — হয়তো হিসাবের ধরন আলাদা"]),
            T("Separate person from claim.", ["he ignores the data", "his plan will fail"],
              ["তিনি তথ্য উপেক্ষা করেননি, তবে ওজন ভিন্ন দিয়েছেন", "লক্ষ্যে একমত, সময়সীমা নিয়ে আমি সন্দিহান"]),
        ]))),
]

# ── the five half-step rungs ────────────────────────────────────────────────

HALFSTEPS = {}

HALFSTEPS["A1+"] = {
    "title": "Bengali A1+ — Getting around",
    "native": NATIVE,
    "goals": [
        "Ask for directions, tickets and things you need",
        "Give a phone number, an address and a price",
        "Name the days, tell the time and make a plan — or refuse one politely",
    ],
    "units": [
        {"id": "A1+-U1", "title": "In the street", "lessons": [
            L("Right, left, straight: directions that work",
              "Directions come as imperatives, and Bengali softens them with একটু and দয়া করে: একটু "
              "ডানে ঘুরুন. Four words carry you around most of the city: ডানে, বাঁয়ে, সোজা, আর কাছে।",
              [V("ডানে", "ḍane", "to the right", "adverb"),
               V("বাঁয়ে", "bãye", "to the left", "adverb"),
               V("সোজা", "shoja", "straight ahead", "adjective"),
               V("ঘুরুন", "ghurun", "turn (polite imperative)", "verb"),
               V("কাছে", "kachhe", "near, close", "adjective")],
              G("Polite imperative in directions",
                "verb + -un · ekṭu + verb + -un",
                "একটু ডানে ঘুরুন, তারপর সোজা যান. To a friend: ঘুরো, যাও. The -un ending is what makes "
                "a stranger's help sound like a request instead of an order.",
                [X("একটু ডানে ঘুরুন।", "ekṭu ḍane ghurun.", "Turn right a little."),
                 X("সোজা গিয়ে বাঁয়ে ঘুরুন।", "shoja giye bãye ghurun.", "Go straight, then turn left."),
                 X("স্টেশন কি কাছে?", "sṭeshon ki kachhe?", "Is the station near?")],
                [("ডানে ঘুরো আপনি।", "একটু ডানে ঘুরুন।", "আপনি takes -un; pairing it with ঘুরো mixes registers."),
                 ("সোজা যাওয়া।", "সোজা যান।", "Directions are imperatives: যান, not the verbal noun যাওয়া.")]),
              [D("মিতা", "দয়া করে বলুন, স্টেশন কোথায়?", "dôya kôre bolun, sṭeshon kothay?", "Please tell me, where is the station?"),
               D("রাতুল", "একটু সোজা যান, তারপর ডানে ঘুরুন।", "ekṭu shoja jan, tarpor ḍane ghurun.", "Go straight a little, then turn right."),
               D("মিতা", "বেশি দূরে?", "beshi dure?", "Is it far?"),
               D("রাতুল", "না, পাঁচ মিনিটের হাঁটা, খুব কাছে।", "na, pãch minit̩er hãṭa, khub kachhe.", "No, a five-minute walk — very close.")],
              WS("Directions worksheet", [
                  T("Give the direction.", ["turn left", "go straight", "turn right at the hospital"],
                    ["একটু বাঁয়ে ঘুরুন", "সোজা যান", "হাসপাতালে ডানে ঘুরুন"]),
                  T("Ask and answer.", ["Where is the market? (straight ahead)", "Is it far? (no, near)"],
                    ["সোজা যান", "না, খুব কাছে"]),
              ])),
            L("Tickets, fare and the rickshaw",
              "Moving around costs money and the language is short: ভাড়া কত? (what is the fare?), "
              "একটা টিকিট দেবেন (could you give one ticket?), এইখানে থামুন (stop here). Rickshaw, bus "
              "and train all use the same three lines.",
              [V("টিকিট", "ṭikiṭ", "ticket", "noun"),
               V("ভাড়া", "bhaṛa", "fare", "noun"),
               V("রিকশা", "riksha", "rickshaw", "noun"),
               V("থামুন", "thamun", "stop (polite imperative)", "verb"),
               V("কত", "kôto", "how much, how many", "interrogative")],
              G("Fare and destination frames",
                "…-er bhara kôto? · ekṭa ṭikiṭ deben · ei khane thamun",
                "বাসের ভাড়া কত? স্টেশন পর্যন্ত কত লাগবে? একটা টিকিট দেবেন। The destination takes "
                "পর্যন্ত: স্টেশন পর্যন্ত.",
                [X("রিকশায় কত লাগবে?", "rikshay kôto lagbe?", "How much will it cost by rickshaw?"),
                 X("স্টেশন পর্যন্ত একটা টিকিট দেবেন।", "sṭeshon pôrjonto ekṭa ṭikiṭ deben.", "Give me one ticket to the station."),
                 X("এইখানে থামুন, দয়া করে।", "ei khane thamun, dôya kôre.", "Stop here, please.")],
                [("কত টিকিট লাগবে?", "ভাড়া কত?", "টিকিট is a thing; ভাড়া is the price of the ride."),
                 ("স্টেশনে পর্যন্ত টিকিট।", "স্টেশন পর্যন্ত টিকিট।", "পর্যন্ত follows the noun directly.")]),
              [D("মিতা", "রিকশায় স্টেশন পর্যন্ত কত লাগবে?", "rikshay sṭeshon pôrjonto kôto lagbe?", "How much to the station by rickshaw?"),
               D("চালক", "একশো টাকা।", "eksho ṭaka.", "One hundred taka."),
               D("মিতা", "একটু কম হবে? আশি দিই।", "ekṭu kôm hobe? ashi dii.", "Will you come down a little? I'll give eighty."),
               D("চালক", "ঠিক আছে, নব্বই, উঠুন।", "ṭhik achhe, nobboi, uṭhun.", "All right — ninety, get in.")],
              WS("Fare worksheet", [
                  T("Ask for it in Bengali.", ["one ticket to Dhaka", "how much is the fare?", "stop here"],
                    ["ঢাকা পর্যন্ত একটা টিকিট", "ভাড়া কত?", "এইখানে থামুন"]),
                  T("Answer as the driver.", ["fare? (ninety taka)", "will you reduce? (all right)"],
                    ["নব্বই টাকা", "ঠিক আছে"]),
              ])),
            L("Landmarks: সামনে, পাশে, বিপরীতে",
              "Nobody gives a street number in Dhaka; they give a landmark and a side: সামনে (in front "
              "of), পাশে (beside), বিপরীতে (opposite). Learn six landmarks and you can find anything.",
              [V("সামনে", "shamne", "in front of", "postposition"),
               V("পাশে", "pashe", "beside, next to", "postposition"),
               V("বিপরীতে", "biporite", "opposite", "postposition"),
               V("হাসপাতাল", "hashpatal", "hospital", "noun"),
               V("বাজার", "bajar", "market", "noun")],
              G("Landmark + relation",
                "relation comes after the landmark: [landmark]-er shamne / pashe / biporite",
                "স্কুলের সামনে একটা বাজার আছে. হাসপাতালের পাশে ওষুধের দোকান. Landmarks take -র/-এর "
                "before the relation word.",
                [X("থানার বিপরীতে একটা পার্ক।", "thanar biporite ekṭa park.", "There is a park opposite the police station."),
                 X("আমার বাড়ি বাজারের পাশে।", "amar bari bajarer pashe.", "My house is beside the market."),
                 X("স্কুলের সামনে দাঁড়ান।", "skuler shamne dãṛan.", "Stand in front of the school.")],
                [("বাজার পাশে আমার বাড়ি।", "বাজারের পাশে আমার বাড়ি।", "The landmark takes the genitive -র before পাশে."),
                 ("সামনে স্কুলের।", "স্কুলের সামনে।", "Bengali puts the landmark first, the relation after.")]),
              [D("মিতা", "হাসপাতালটা কোথায়?", "hashpatalṭa kothay?", "Where is the hospital?"),
               D("রাতুল", "থানার পাশে, আর তার বিপরীতেই ওষুধের দোকান।", "thanar pashe, ar tar biporitei oshudher dokan.", "Beside the police station, and the pharmacy is right opposite."),
               D("মিতা", "বাজারের সামনে কি কিছু আছে?", "bajarer shamne ki kichhu achhe?", "Is there anything in front of the market?"),
               D("রাতুল", "হ্যাঁ, একটা বড় পার্ক।", "hã, ekṭa bôṛ park.", "Yes, a large park.")],
              WS("Landmark worksheet", [
                  T("Complete with the relation.", ["বাজারের __ (beside)", "স্কুলের __ (opposite)", "থানার __ (in front)"],
                    ["পাশে", "বিপরীতে", "সামনে"]),
                  T("Describe your own street.", ["what is beside the market?", "what is opposite the school?"],
                    ["বাজারের পাশে …", "স্কুলের বিপরীতে …"]),
              ])),
        ]},
        {"id": "A1+-U2", "title": "Numbers that get you home", "lessons": [
            L("From eleven to a hundred",
              "Bengali numbers above ten are learned as vocabulary, not built like English: এগারো, "
              "বারো, বিশ, পঞ্চাশ, একশো. Learn them aloud in tens — বিশ, ত্রিশ, চল্লিশ — and the rest "
              "arrives from use.",
              [V("এগারো", "egaro", "eleven", "numeral"),
               V("বিশ", "bish", "twenty", "numeral"),
               V("পঞ্চাশ", "pônchash", "fifty", "numeral"),
               V("একশো", "eksho", "one hundred", "numeral"),
               V("-শো", "-sho", "hundred (in compounds)", "suffix")],
              G("Numbers are vocabulary",
                "11–99 as their own words: 25 পঁচিশ · 40 চল্লিশ · 99 নিরানব্বই",
                "Twenty-five is পঁচিশ, one word — not 'two tens five'. Above hundred: একশো একুশ "
                "(121), দুশো (200). Read phone numbers digit by digit instead.",
                [X("আমার বয়স পঁচিশ বছর।", "amar bôyosh pãchish bôchhor.", "I am twenty-five years old."),
                 X("এখানে চল্লিশ জন আছে।", "ekhane chôllish jon achhe.", "There are forty people here."),
                 X("দাম একশো বিশ টাকা।", "dam eksho bish ṭaka.", "The price is one hundred and twenty taka.")],
                [("দুই দশ পাঁচ।", "পঁচিশ।", "Bengali does not build twenty-five from words for two and ten here — it is one lexical number."),
                 ("একশত বিশ টাকা বলো।", "একশো বিশ টাকা।", "Speech uses একশো; একশত is bookish.")]),
              [D("মিতা", "তোমার নম্বর কত?", "tomar nômbôr kôto?", "What is your number?"),
               D("রাতুল", "একশো পঁচিশ — মানে বাসের নম্বর।", "eksho pãchish — mane baser nômbôr.", "One hundred and twenty-five — that is the bus number."),
               D("মিতা", "আর বাড়ির নম্বর?", "ar baṛir nômbôr?", "And the house number?"),
               D("রাতুল", "সাতাশ, চার নম্বর রাস্তা।", "sataish, char nômbôr rasta.", "Twenty-seven, road number four.")],
              WS("Numbers worksheet", [
                  T("Write the number in Bengali words.", ["25", "40", "99", "121"],
                    ["পঁচিশ", "চল্লিশ", "নিরানব্বই", "একশো একুশ"]),
                  T("Say the price in full.", ["ticket 45 taka", "two books 120 taka"],
                    ["পঁয়তাল্লিশ টাকা", "একশো বিশ টাকা"]),
              ])),
            L("Phone numbers and addresses",
              "Numbers are read digit by digit on the phone, and an address runs বাড়ি, রাস্তা, এলাকা. "
              "Useful frames: আপনার নম্বরটা দিন (give me your number), আবার বলুন (say it again), "
              "আমি লিখে নিচ্ছি (I'm writing it down).",
              [V("নম্বর", "nômbôr", "number", "noun"),
               V("ফোন", "phon", "phone", "noun"),
               V("রাস্তা", "rasta", "road, street", "noun"),
               V("বাড়ি", "baṛi", "house", "noun"),
               V("এলাকা", "elaka", "area, locality", "noun")],
              G("Reading a number aloud",
                "digit + digit … · amar nômbôr … · baṛi nômbôr … rasta",
                "শূন্য, এক, দুই, তিন… In speech the digits run together: শূন্য এক দুই. Address: বাড়ি "
                "সাতাশ, রাস্তা চার, ধানমন্ডি এলাকা।",
                [X("আপনার ফোন নম্বরটা দিন।", "apnar phon nômbôrṭa din.", "Give me your phone number."),
                 X("বাড়ি সাতাশ, রাস্তা চার, ধানমন্ডি।", "baṛi sataish, rasta char, Dhanmondi.", "House twenty-seven, road four, Dhanmondi."),
                 X("আবার বলুন, আমি লিখে নিচ্ছি।", "abar bolun, ami likhe nîchhi.", "Say it again, I'm writing it down.")],
                [("আমার নম্বর ফোনটা।", "আমার ফোন নম্বরটা।", "The compound is ফোন নম্বর, in that order."),
                 ("বাড়ি সাতাশে, রাস্তা চারে।", "বাড়ি সাতাশ, রাস্তা চার।", "Address numbers take no locative ending.")]),
              [D("মিতা", "আপনার ফোন নম্বরটা দেবেন?", "apnar phon nômbôrṭa deben?", "Will you give me your phone number?"),
               D("রাতুল", "অবশ্যই: শূন্য, এক, সাত, আট…", "oboshshoi: shunno, ek, shat, aṭ…", "Certainly: zero, one, seven, eight…"),
               D("মিতা", "একটু আস্তে বলুন, লিখে নিচ্ছি।", "ekṭu aste bolun, likhe nîchhi.", "Speak a little slowly, I'm writing."),
               D("রাতুল", "ঠিক আছে — শেষে দুই, তিন।", "ṭhik achhe — sheshe dui, tin.", "All right — at the end, two, three.")],
              WS("Address worksheet", [
                  T("Say it in Bengali.", ["my phone number", "house 27", "road four, Dhanmondi"],
                    ["আমার ফোন নম্বর", "বাড়ি সাতাশ", "রাস্তা চার, ধানমন্ডি"]),
                  T("Ask for the details.", ["phone number?", "repeat please", "I'm writing it down"],
                    ["ফোন নম্বরটা দেবেন?", "আবার বলুন", "আমি লিখে নিচ্ছি"]),
              ])),
            L("Prices: বেশি, কম, একটু কমান",
              "Bargaining has four moves: দাম কত?, বেশি হয়ে গেল, একটু কমান, ঠিক আছে নেব. Bengali "
              "bargaining is friendly and slow; দাম কমান is the direct version and it is heard as "
              "slightly blunt.",
              [V("দাম", "dam", "price", "noun"),
               V("বেশি", "beshi", "too much, more", "adjective"),
               V("কম", "kôm", "less, few", "adjective"),
               V("কমান", "kôman", "reduce (imperative)", "verb"),
               V("নেব", "nebo", "I will take", "verb")],
              G("Bargaining frames",
                "dam kôto? · beśi hoye gelo · ekṭu kaman · ṭhik achhe, nebo",
                "দামটা একটু বেশি হয়ে গেল, একটু কমাবেন? Missing the -ben makes it sound like an "
                "instruction; adding -টু softens the whole line.",
                [X("একটু বেশি হয়ে গেল।", "ekṭu beshi hoye gelo.", "That's a little too much."),
                 X("পাঁচ টাকা কম করবেন?", "pãch ṭaka kôm kôrben?", "Will you take five taka less?"),
                 X("ঠিক আছে, এটাই নেব।", "ṭhik achhe, eṭai nebo.", "All right, I'll take this one.")],
                [("দাম কমান।", "একটু কম করবেন?", "The bare imperative is heard as an order between strangers."),
                 ("টাকা কম বেশি।", "দাম বেশি, কিছুটা কম।", "The frame is দাম + বেশি/কম.")]),
              [D("মিতা", "এই শাড়িটার দাম কত?", "ei shãṛiṭar dam kôto?", "What is the price of this sari?"),
               D("দোকানদার", "দুই হাজার টাকা।", "dui hajar ṭaka.", "Two thousand taka."),
               D("মিতা", "একটু বেশি হয়ে গেল — আঠারোশো নেব।", "ekṭu beshi hoye gelo — aṭharosho nebo.", "That's a little much — I'll take it at eighteen hundred."),
               D("দোকানদার", "ঠিক আছে, আপনার জন্য আঠারোশো।", "ṭhik achhe, apnar jonno aṭharosho.", "All right, eighteen hundred for you.")],
              WS("Price worksheet", [
                  T("Bargain politely.", ["it is too much → (soften)", "ask for a reduction", "accept"],
                    ["একটু বেশি হয়ে গেল", "একটু কম করবেন?", "ঠিক আছে, নেব"]),
                  T("Answer as the seller.", ["price? (two thousand)", "will you reduce? (all right, for you)"],
                    ["দুই হাজার টাকা", "ঠিক আছে, আপনার জন্য কম"]),
              ])),
        ]},
        {"id": "A1+-U3", "title": "Days, times, plans", "lessons": [
            L("The days of the week",
              "The Bengali week runs শনিবার to শুক্রবার, and শুক্রবার is the day everyone names. Days "
              "take no preposition: শনিবার দেখা হবে. A range uses থেকে… পর্যন্ত.",
              [V("শনিবার", "shonibar", "Saturday", "noun"),
               V("রবিবার", "robibar", "Sunday", "noun"),
               V("সোমবার", "shombar", "Monday", "noun"),
               V("শুক্রবার", "shukrobar", "Friday", "noun"),
               V("সপ্তাহ", "shoptah", "week", "noun")],
              G("Days are adverbial",
                "day + verb, no postposition · day theke day pôrjonto",
                "মঙ্গলবার আমি ব্যস্ত. শুক্রবার ছুটি. সোমবার থেকে বুধবার পর্যন্ত ক্লাস. The day name "
                "stands alone; -বার is the marker, not a postposition.",
                [X("আজ কী বার?", "aj ki bar?", "What day is today?"),
                 X("আজ শুক্রবার, ছুটির দিন।", "aj shukrobar, chhuṭir din.", "Today is Friday, a holiday."),
                 X("আমি শনিবার আসব।", "ami shonibar ashbo.", "I will come on Saturday.")],
                [("আমি শনিবারে আসব।", "আমি শনিবার আসব।", "Day names take no locative ending in this frame."),
                 ("আজ শুক্রবারে।", "আজ শুক্রবার।", "Same rule: the bare day name.")]),
              [D("মিতা", "আজ কী বার?", "aj ki bar?", "What day is today?"),
               D("রাতুল", "আজ বুধবার, আর কাল বৃহস্পতিবার।", "aj budhbar, ar kal brihoshpotibar.", "Today is Wednesday, and tomorrow is Thursday."),
               D("মিতা", "শুক্রবার কী করবেন?", "shukrobar ki kôrben?", "What will you do on Friday?"),
               D("রাতুল", "শুক্রবার ছুটি, পরিবারের সাথে থাকব।", "shukrobar chhuṭi, poribarer shathe thakbo.", "Friday is a holiday — I'll be with family.")],
              WS("Days worksheet", [
                  T("Answer in Bengali.", ["what day is today? (Friday)", "which day is a holiday?", "from Monday to Wednesday"],
                    ["আজ শুক্রবার", "শুক্রবার ছুটি", "সোমবার থেকে বুধবার পর্যন্ত"]),
                  T("Plan your week.", ["a working day", "a rest day"],
                    ["আমি … কাজ করি", "আমি … বিশ্রাম নিই"]),
              ])),
            L("Telling the time",
              "Clock time uses টা (o'clock): তিনটে, চারটা. Half past is সাড়ে (সাড়ে পাঁচ), quarter "
              "past সোয়া (সোয়া সাত), quarter to পৌনে (পৌনে নয়) — note that পৌনে counts down to the "
              "next hour.",
              [V("টা", "ṭa", "o'clock", "classifier"),
               V("সাড়ে", "shaṛe", "half past", "prefix"),
               V("সোয়া", "shoya", "quarter past", "prefix"),
               V("পৌনে", "poune", "quarter to (the next hour)", "prefix"),
               V("সময়", "shomoy", "time", "noun")],
              G("Clock frames",
                "number + ṭa · shaṛe / shoya / poune + number",
                "এখন তিনটে. সাড়ে পাঁচটায় দেখা করব. পৌনে নয় মানে ৮:৪৫ — পৌনে looks forward. The "
                "ending -টায় adds 'at'.",
                [X("এখন কতটা বাজে?", "ekhon kôtoṭa baje?", "What time is it now?"),
                 X("সাড়ে সাতটায় দেখা করি।", "shaṛe shatṭay dekha kôri.", "Let's meet at half past seven."),
                 X("পৌনে ছয়টায় ফিরব।", "poune chhoyṭay phirbo.", "I'll be back at a quarter to six.")],
                [("পৌনে নয় মানে ৯:১৫।", "পৌনে নয় মানে ৮:৪৫।", "পৌনে counts down: quarter to nine is 8:45."),
                 ("সাড়ে পাঁচ মানে ৫:৫০।", "সাড়ে পাঁচ মানে ৫:৩০।", "সাড়ে is half past, not ten to.")]),
              [D("মিতা", "এখন কতটা বাজে?", "ekhon kôtoṭa baje?", "What time is it now?"),
               D("রাতুল", "সাড়ে চারটা।", "shaṛe charṭa.", "Half past four."),
               D("মিতা", "তাহলে সোয়া পাঁচটায় দেখা করি?", "tahole shoya pãchṭay dekha kôri?", "Then shall we meet at a quarter past five?"),
               D("রাতুল", "ঠিক আছে, আমি সময়মতো আসব।", "ṭhik achhe, ami shomoymôto ashbo.", "All right, I'll come on time.")],
              WS("Clock worksheet", [
                  T("Say the time in Bengali.", ["3:00", "5:30", "8:45", "7:15"],
                    ["তিনটে", "সাড়ে পাঁচটা", "পৌনে নয়টা", "সোয়া সাতটা"]),
                  T("Answer the question.", ["কখন দেখা করব? (at 6:30)", "কখন আসবেন? (at 9:00)"],
                    ["সাড়ে ছয়টায়", "নয়টায়"]),
              ])),
            L("Making a plan, refusing one kindly",
              "Plans are made with চলুন (let's go), দেখা করি (shall we meet), সময় আছে? and refused "
              "with দুঃখিত, পারব না — plus a later date, because Bengali refuses with an alternative "
              "or not at all.",
              [V("চলুন", "chôlun", "let's go (polite)", "verb"),
               V("ব্যস্ত", "bêsto", "busy", "adjective"),
               V("দুঃখিত", "dukkhito", "sorry", "adjective"),
               V("পরে", "pôre", "later", "adverb"),
               V("পারব না", "parbo na", "I will not be able to", "phrase")],
              G("Plan and refuse",
                "chôlun + verb · shômoy achhe? · dukkhito, parbo na — kintu …-e hole?",
                "আজ কী করব? চলুন দেখা করি! দুঃখিত, কাল পারব না — পরশু হলে ভালো হয়. The alternative "
                "is part of the refusal.",
                [X("চলুন, একসাথে চা খাই।", "chôlun, ekshathe cha khai.", "Let's have tea together."),
                 X("আপনার আজ সময় আছে?", "apnar aj shomoy achhe?", "Do you have time today?"),
                 X("দুঃখিত, পারব না; কাল হলে ভালো হয়।", "dukkhito, parbo na; kal hole bhalo hôy.", "Sorry, I can't; tomorrow would be better.")],
                [("দুঃখিত, না।", "দুঃখিত, পারব না — কাল হলে হয়।", "A bare no closes the door; the alternative keeps it open."),
                 ("আমি না খাব।", "আমি খাব না।", "Bengali negation follows the verb: খাব না.")]),
              [D("মিতা", "শনিবার ঘুরতে যাবেন?", "shonibar ghurte jaben?", "Will you go out on Saturday?"),
               D("রাতুল", "দুঃখিত, শনিবার পারব না — ছোট ভাইয়ের পরীক্ষা।", "dukkhito, shonibar parbo na — chhoṭ bhaiyer porikkha.", "Sorry, I can't on Saturday — my younger brother's exam."),
               D("মিতা", "তাহলে রবিবার?", "tahole robibar?", "Then Sunday?"),
               D("রাতুল", "রবিবার ঠিক আছে, দেখা হবে।", "robibar ṭhik achhe, dekha hobe.", "Sunday is fine — see you then.")],
              WS("Plan worksheet", [
                  T("Make the plan.", ["let's meet", "do you have time tomorrow?", "shall we go together?"],
                    ["চলুন দেখা করি", "কাল আপনার সময় আছে?", "একসাথে যাবেন?"]),
                  T("Refuse and offer another day.", ["refuse today, offer tomorrow", "refuse Saturday, offer Sunday"],
                    ["দুঃখিত, আজ পারব না — কাল হলে হয়", "শনিবার পারব না, রবিবার হলে ভালো"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Getting around in a Bengali city is done by landmark and by rickshaw. Nobody gives a "
                 "street number; they say 'beside the pharmacy, opposite the school', and the rickshaw "
                 "fare is negotiated before you get in. Buses are numbered in Bengali numerals on older "
                 "vehicles, so a visitor who can read the numerals stops missing buses — that is the "
                 "practical reason this level teaches numbers to a hundred."),
        source_url="https://en.wikipedia.org/wiki/Rickshaw",
        reading=("আমি আজ সকালে বাসে করে অফিসে যাব। বাসের নম্বর একশো পঁচিশ, ভাড়া বিশ টাকা। স্টপেজ "
                 "স্কুলের সামনে, আর আমার অফিস তার বিপরীতে — হাঁটা দশ মিনিট। বাসে উঠে "
                 "ড্রাইভারকে বলব: «এইখানে থামুন»। তারপর বাজারের পাশে একটা দোকানে চা খেয়ে "
                 "হেঁটে অফিসে যাব। বাড়ি নম্বর সাতাশ, রাস্তা চার — সব ঠিক আছে।"),
        reading_gloss=("I will go to the office by bus this morning. The bus number is one hundred and "
                       "twenty-five, the fare twenty taka. The stop is in front of the school, and my "
                       "office is opposite it. I'll tell the driver: 'Stop here.' House number "
                       "twenty-seven, road four — all correct."),
        listening=("মিতা: এইখানে থামুন, দয়া করে।<br>চালক: কত টাকা?<br>মিতা: নব্বই, ঠিক আছে?<br>"
                   "চালক: ঠিক আছে। স্টেশন ওখানেই।"),
        listening_gloss=("Mita: Stop here, please. Driver: How much? Mita: Ninety, all right? Driver: "
                         "All right. The station is right there."),
        voice_tag=VOICE,
        idioms=[
            ("একটু দূরে", "a little far", "a short distance away"),
            ("হাঁটার পথ", "a walking path", "within walking distance"),
            ("পথ দেখানো", "showing the path", "to guide, to show the way"),
            ("সোজা পথ", "the straight path", "the direct route"),
            ("ঘুরপথে", "by a roundabout way", "indirectly"),
            ("সময়ের আগে", "before time", "ahead of schedule"),
            ("সময়ের পরে", "after time", "behind schedule"),
            ("জায়গা মতো", "according to place", "in its proper place"),
            ("নম্বর দেওয়া", "to give a number", "to phone someone"),
            ("রাস্তার ধারে", "at the edge of the road", "roadside"),
        ],
        mistakes=[
            ("স্টেশনে পর্যন্ত টিকিট দেবেন।", "স্টেশন পর্যন্ত টিকিট দেবেন।", "পর্যন্ত follows the noun directly, without the locative -ে."),
            ("কত দূর?", "কত দূর?", "Correct — but answer with distance, not time: দশ মিনিট is time; দু'কিলোমিটার is distance."),
            ("বাসে কত ভাড়া হয়?", "বাসের ভাড়া কত?", "The fare belongs to the bus: বাসের ভাড়া."),
        ],
        task_title="Direct someone across your city",
        task_instructions=("Pick a route you take often and write six Bengali steps with at least three "
                           "landmarks and one fare question. Read it to someone who must draw the route "
                           "without asking a question. If they get lost, the missing word was probably "
                           "a relation — পাশে, সামনে or বিপরীতে — so fix it and try again."),
    ),
    "test": [
        ("translate_en", "Say: Where is the hospital, please?", "হাসপাতাল কোথায়, দয়া করে বলেন?"),
        ("translate_ar", "একটু ডানে ঘুরুন, তারপর সোজা যান।", "Turn right a little, then go straight."),
        ("multiple_choice", "Which is the polite request?", "একটু কম করবেন?"),
        ("fill_in_the_blank", "স্টেশন ___ একটা টিকিট দেবেন। (to)", "পর্যন্ত"),
        ("word_selection", "Select the Bengali for fifty.", "পঞ্চাশ"),
        ("error_correction", "বাজারের পাশে আমার বাড়ি। / বাজার পাশে আমার বাড়ি।", "বাজারের পাশে আমার বাড়ি।"),
        ("dialogue_completion", "Complete: ভাড়া কত? — ___ (ninety taka)", "নব্বই টাকা"),
        ("matching", "Match বিপরীতে to its meaning.", "opposite"),
        ("reading_comprehension", "বাসের নম্বর একশো পঁচিশ। Which bus is it?", "125"),
        ("inference", "«একটু বেশি হয়ে গেল» — what is the speaker doing?", "bargaining politely"),
        ("main_idea", "স্কুলের সামনে স্টপেজ, অফিস তার বিপরীতে। What is this about?", "where the stop and office are"),
        ("detail_identification", "সাড়ে সাতটায় দেখা করব। What time is the meeting?", "7:30"),
    ],
}

HALFSTEPS["A2+"] = {
    "title": "Bengali A2+ — Holding a chat",
    "native": NATIVE,
    "goals": [
        "React, follow up and keep a conversation alive",
        "Tell a short story in order, with a scene and a turn",
        "Invite, accept, decline — on the phone and in person",
    ],
    "units": [
        {"id": "A2+-U1", "title": "Keeping the talk going", "lessons": [
            L("Reactions that mean something",
              "Bengali conversation is fed by reactions: সত্যি? (really?), তাই নাকি? (is that so?), কী "
              "মজা! (what fun!), এতেও হয়! (even that happens!). They hand the floor straight back.",
              [V("সত্যি?", "shôtti?", "really?", "interrogative"),
               V("তাই নাকি?", "tai naki?", "is that so?", "phrase"),
               V("কী মজা!", "ki môja!", "what fun!", "phrase"),
               V("বলেন কী!", "bolen ki!", "you don't say!", "phrase"),
               V("আশ্চর্য", "ashchorjo", "surprising", "adjective")],
              G("React, then ask",
                "reaction + ar + follow-up question",
                "সত্যি? তারপর কী হলো? A reaction alone can close a turn; adding আর + a question keeps "
                "it open. তাই নাকি is friendly doubt; বলেন কী is surprise — pick the one the moment needs.",
                [X("সত্যি? আমি জানতাম না।", "shôtti? ami jantam na.", "Really? I did not know."),
                 X("তাই নাকি? কে বলল?", "tai naki? ke bollo?", "Is that so? Who said it?"),
                 X("কী মজা! আমি যেতেও চাই।", "ki môja! ami jeteoo chai.", "What fun! I want to go too.")],
                [("সত্যি আমি জানি না।", "সত্যি? আমি জানি না।", "As a reaction, সত্যি? stands alone with a question mark."),
                 ("তাই নাকি? হ্যাঁ, তুমি ঠিক।", "তাই নাকি? আর তারপর?", "A reaction contradicts nothing; it invites the next sentence.")]),
              [D("সুমি", "আমি কাল চাকরি পেয়েছি!", "ami kal chakri peyechhi!", "I got a job yesterday!"),
               D("রাতুল", "সত্যি? অভিনন্দন! কোথায়?", "shôtti? obhinondon! kothay?", "Really? Congratulations! Where?"),
               D("সুমি", "একটা ছোট কোম্পানিতে, ঢাকায়।", "ekṭa chhoṭ kompanite, Dhakay.", "At a small company, in Dhaka."),
               D("রাতুল", "কী মজা! এখন অনেক কিছু শিখবে।", "ki môja! ekhon ônek kichhu shikhbe.", "How fun! You'll learn a lot now.")],
              WS("Reaction worksheet", [
                  T("React in Bengali.", ["good news", "something unbelievable", "something obvious"],
                    ["সত্যি? অভিনন্দন!", "বলেন কী!", "হ্যাঁ, এটা তো জানা কথা"]),
                  T("React and follow up.", ["'I moved to Khulna'", "'I changed jobs'"],
                    ["সত্যি? কবে গেলে?", "তাই নাকি? কেন বদলালে?"]),
              ])),
            L("Following up: তারপর? কেন?",
              "A conversation dies when nobody asks. তারপর? (and then?), কেন? (why?), কেমন লাগল? (how "
              "did it feel?) — the third one asks for feeling rather than fact, which is what turns a "
              "report into a chat.",
              [V("তারপর?", "tarpor?", "then? / and then?", "interrogative"),
               V("কেন?", "keno?", "why?", "interrogative"),
               V("কেমন লাগল?", "kemon laglo?", "how did it feel?", "phrase"),
               V("আর কিছু?", "ar kichhu?", "anything else?", "phrase"),
               V("বলতে থাকুন", "bolte thakun", "keep telling me", "phrase")],
              G("Follow-up ladder",
                "ki hoyechhe? → tarpor? → kemon laglo?",
                "Each question goes a step deeper: the event, the next event, then the evaluation. "
                "বলতে থাকুন is the shortest way to say 'I am listening'.",
                [X("তারপর কী হলো?", "tarpor ki hôlo?", "Then what happened?"),
                 X("তোমার কেমন লাগল?", "tomar kemon laglo?", "How did you feel about it?"),
                 X("বলতে থাকুন, শুনছি।", "bolte thakun, shunchhi.", "Keep going, I'm listening.")],
                [("তারপর? কেন? কেমন? আর?", "(one follow-up at a time)", "A chain of follow-ups turns interest into an interrogation."),
                 ("তোমার কেমন লাগল তোমার?", "তোমার কেমন লাগল?", "One possessive is enough.")]),
              [D("মিতা", "কাল আমি দেরি করে ফেলেছিলাম।", "kal ami deri kore pheleчhиlam.", "Yesterday I ended up late."),
               D("রাতুল", "তারপর কী হলো?", "tarpor ki hôlo?", "Then what happened?"),
               D("মিতা", "বসটা ছেড়ে চলে গেল, আমাকে হাঁটতে হলো।", "bosṭa chheṛe chôle gelo, amake hãṭte hôlo.", "The bus left without me; I had to walk."),
               D("রাতুল", "কেমন লাগল?", "kemon laglo?", "How did that feel?")],
              WS("Follow-up worksheet", [
                  T("Ask the next question.", ["'I met the director'", "'I moved to a new area'"],
                    ["তিনি কী বললেন?", "নতুন এলাকা কেমন?"]),
                  T("Show interest.", ["(it was hard)", "(tell me more)"],
                    ["কী কঠিন!", "বলতে থাকুন"]),
              ])),
            L("Praise in Bengali: বাহ! চমৎকার!",
              "Praise is formulaic and generous: বাহ্, চমৎকার, দারুণ, খুব ভালো, আল্লাহ/ঈশ্বরের কৃপা in "
              "some families. A quiet 'ভালো হয়েছে' also lands — the volume is what matters, not the "
              "vocabulary.",
              [V("বাহ?", "bah", "wow! (praise)", "interjection"),
               V("চমৎকার", "chômothkar", "excellent", "adjective"),
               V("দারুণ", "darun", "great", "adjective"),
               V("খুব ভালো", "khub bhalo", "very good", "phrase"),
               V("অভিনন্দন", "obhinondon", "congratulations", "noun")],
              G("Praise frames",
                "bah! + chômothkar · khub bhalo hoyechhe · obhinondon!",
                "বাহ্! খুব ভালো হয়েছে. To a colleague: চমৎকার কাজ. For an achievement: অনেক "
                "অভিনন্দন. Bengali praise is warm but short; two words carry it.",
                [X("বাহ! ছবিটা চমৎকার।", "bah! chhobiṭa chômothkar.", "Wow! The picture is excellent."),
                 X("আপনার কাজ খুব ভালো হয়েছে।", "apnar kaj khub bhalo hoyechhe.", "Your work has turned out very well."),
                 X("অনেক অভিনন্দন!", "ônek obhinondon!", "Many congratulations!")],
                [("বাহ, কিন্তু খারাপ।", "বাহ, চমৎকার।", "Praise followed by a criticism in the same breath is not praise."),
                 ("তুমি ভালো না। (meaning: very good)", "তুমি খুব ভালো করেছ।", "Bengali praise is affirmative; negating it reverses the meaning.")]),
              [D("সুমি", "দেখুন, আমি নিজে কেকটা বানিয়েছি।", "dekhun, ami nije kekṭa baniyechhi.", "Look, I made the cake myself."),
               D("মিতা", "বাহ! চমৎকার হয়েছে!", "bah! chômothkar hoyechhe!", "Wow! It has turned out excellent!"),
               D("সুমি", "আরও একটু মিষ্টি হবে কি?", "aro ekṭu mishti hobe ki?", "Should it be a little sweeter?"),
               D("মিতা", "একদম ঠিক আছে, দারুণ!", "ekdôm ṭhik achhe, darun!", "It's exactly right — great!")],
              WS("Praise worksheet", [
                  T("Praise warmly.", ["a drawing", "an exam result", "someone's cooking"],
                    ["বাহ, চমৎকার!", "অনেক অভিনন্দন!", "খুব ভালো হয়েছে"]),
                  T("Praise a colleague's work.", ["the report", "the presentation"],
                    ["চমৎকার কাজ", "খুব ভালো হয়েছে, দারুণ"]),
              ])),
        ]},
        {"id": "A2+-U2", "title": "Telling a short story", "lessons": [
            L("In order: প্রথমে, তারপর, এরপর, শেষে",
              "Four connectors turn four sentences into a story: প্রথমে, তারপর, এরপর, শেষে. Bengali "
              "also uses তারপরেই (right after that) and একটু পরে (a little later) to keep the rhythm.",
              [V("প্রথমে", "prothome", "at first", "adverb"),
               V("তারপর", "tarpor", "then, after that", "conjunction"),
               V("এরপর", "erpor", "after this", "conjunction"),
               V("শেষে", "sheshe", "at the end", "adverb"),
               V("একটু পরে", "ekṭu pôre", "a little later", "phrase")],
              G("Story order",
                "prothome… · tarpor… · erpor… · sheshe…",
                "প্রথমে আমরা বাসে উঠলাম. তারপর বৃষ্টি শুরু হলো. এরপর আমরা নামলাম. শেষে ভিজে বাড়ি "
                "ফিরলাম. One connector per sentence; stacking them sounds like a school exercise.",
                [X("প্রথমে আমি কিছু বুঝিনি।", "prothome ami kichhu bujhini.", "At first I did not understand anything."),
                 X("তারপর সব পরিষ্কার হলো।", "tarpor shôb porishkar hôlo.", "Then everything became clear."),
                 X("শেষে আমরা হেসে উঠলাম।", "sheshe amra heshe uṭhlam.", "In the end we burst out laughing.")],
                [("প্রথমে তারপর এরপর শেষে সব হলো।", "(one connector per sentence)", "All four in one sentence is a list, not a story."),
                 ("তারপর আবার তারপর আবার তারপর।", "(each connector brings a new event)", "Repeating one connector flattens the story.")]),
              [D("সুমি", "কী হয়েছিল?", "ki hoyechhilo?", "What happened?"),
               D("রাতুল", "প্রথমে ট্রেনে উঠলাম, তারপর দেখলাম টিকিট নেই।", "prothome ṭrene uṭhlam, tarpor dekhlam ṭikiṭ nei.", "First we got on the train, then I saw there was no ticket."),
               D("সুমি", "এরপর?", "erpor?", "After that?"),
               D("রাতুল", "এরপর কন্ডাক্টর এলেন, শেষে বন্ধু টিকিট কিনে দিল।", "erpor kônḍakṭor elen, sheshe bondhu ṭikiṭ kine dilo.", "Then the conductor came, and in the end my friend bought me a ticket.")],
              WS("Order worksheet", [
                  T("Put the story in order.", ["we arrived", "we sat", "we ate", "we left"],
                    ["প্রথমে আমরা পৌঁছালাম", "তারপর বসলাম", "এরপর খেলাম", "শেষে চলে গেলাম"]),
                  T("Tell your own morning.", ["first", "then", "finally"],
                    ["প্রথমে…", "তারপর…", "শেষে…"]),
              ])),
            L("Scene and turn: ছিল… হঠাৎ",
              "Bengali sets a scene with ছিল/ছিল (was, were) and turns it with হঠাৎ (suddenly). "
              "The background sits in ছিল-clauses, the event steps out of হঠাৎ.",
              [V("ছিল", "chhilo", "was, were (past state)", "verb"),
               V("হঠাৎ", "haṭhat", "suddenly", "adverb"),
               V("তখন", "tôkhon", "at that time", "adverb"),
               V("চলছিল", "chôlchhilo", "was going on", "verb"),
               V("শুরু হলো", "shuru hôlo", "began", "phrase")],
              G("Scene then event",
                "past-continuous + haṭhat + past verb",
                "বাইরে বৃষ্টি পড়ছিল, আর আমরা ভাত খাচ্ছিলাম; হঠাৎ বিদ্যুৎ চলে গেল. Note the "
                "continuous forms: পড়ছিল, খাচ্ছিলাম — the scene is unfinished when the event hits.",
                [X("রাত তখন দশটা, সবাই ঘুমাচ্ছিল।", "rat tôkhon dôshṭa, shobai ghumat chhilo.", "It was ten at night; everyone was sleeping."),
                 X("আমরা গল্প করছিলাম, হঠাৎ ফোন বাজল।", "amra gôlpo kôrchhilam, haṭhat phon bajlo.", "We were telling stories; suddenly the phone rang."),
                 X("হঠাৎ দরজায় কেউ নক করল।", "haṭhat dôrjay keu nôk kôrlo.", "Suddenly someone knocked at the door.")],
                [("হঠাৎ বিদ্যুৎ।", "হঠাৎ বিদ্যুৎ চলে গেল।", "হঠাৎ needs the event after it."),
                 ("আমরা খাচ্ছিলাম ভাত, হঠাৎ খাচ্ছিলাম।", "আমরা ভাত খাচ্ছিলাম, হঠাৎ বিদ্যুৎ চলে গেল।", "The scene runs until the turn; do not repeat the scene after it.")]),
              [D("রাতুল", "কাল রাতে কী হয়েছিল?", "kal rate ki hoyechhilo?", "What happened last night?"),
               D("মিতা", "সবাই খাচ্ছিল আর গল্প করছিল, হঠাৎ বিদ্যুৎ চলে গেল।", "shobai khachhilo ar gôlpo kôrchhilo, haṭhat biddut chôle gelo.", "Everyone was eating and chatting; suddenly the power went out."),
               D("রাতুল", "তখন কী করলেন?", "tôkhon ki kôrlen?", "What did you do then?"),
               D("মিতা", "মোমবাতি জ্বালালাম, আর গল্প চলতে লাগল।", "mom-bati jbalalam, ar gôlpo chôlte laglo.", "We lit candles and the stories went on.")],
              WS("Scene worksheet", [
                  T("Set the scene.", ["it was raining", "we were waiting", "everyone was quiet"],
                    ["বৃষ্টি পড়ছিল", "আমরা অপেক্ষা করছিলাম", "সবাই চুপ ছিল"]),
                  T("Add the turn with হঠাৎ.", ["(someone knocked)", "(the train left)", "(it started raining)"],
                    ["হঠাৎ কেউ নক করল", "হঠাৎ ট্রেন চলে গেল", "হঠাৎ বৃষ্টি শুরু হলো"]),
              ])),
            L("The close: শেষে দেখা গেল যে",
              "An anecdote closes with a finding or a lesson: শেষে দেখা গেল যে… (in the end it turned "
              "out that), শিখলাম যে… (I learned that), আর সেটাই ছিল সবচেয়ে ভালো (and that was the "
              "best part).",
              [V("শেষে দেখা গেল", "sheshe dekha gelo", "in the end it turned out", "phrase"),
               V("শিখলাম", "shikhlam", "I learned", "verb"),
               V("আসলে", "ashôle", "actually", "adverb"),
               V("সবচেয়ে ভালো", "shôbcheye bhalo", "the best", "phrase"),
               V("গল্পের শিক্ষা", "gôlper shikkha", "the story's lesson", "phrase")],
              G("Closing moves",
                "sheshe dekha gelo je… · shikhlam je… · ashôle…",
                "শেষে দেখা গেল যে ভুলটা আমারই ছিল. শিখলাম যে আগে জিজ্ঞেস করা উচিত. Bengali "
                "anecdotes end on a small admission far more often than on a boast.",
                [X("শেষে দেখা গেল বাসটা Late ছিল না, আমি দেরি করেছিলাম।", "sheshe dekha gelo basṭa late chhilo na, ami deri korechhilam.", "In the end it turned out the bus was not late; I was."),
                 X("শিখলাম যে সময় দেখা দরকার।", "shikhlam je shomoy dekha dôrkar.", "I learned that one must watch the time."),
                 X("আসলে সেটাই ছিল সেরা দিন।", "ashôle sheṭai chhilo shera din.", "Actually that was the best day.")],
                [("শেষে দেখা গেল যে আমি সব জানি।", "শেষে দেখা গেল যে আমার আরও শেখা দরকার।", "A close that reveals nothing is not a close."),
                 ("শিখলাম যে শিখলাম।", "শিখলাম যে সময় দেখা দরকার।", "The lesson has to be a sentence with content.")]),
              [D("সুমি", "তারপর?", "tarpor?", "Then?"),
               D("রাতুল", "শেষে দেখা গেল যে আমি ভুল স্টেশনে নেমেছিলাম।", "sheshe dekha gelo je ami bhul sṭeshone nemechhilam.", "In the end it turned out I had got off at the wrong station."),
               D("সুমি", "তাহলে?", "tahole?", "So?"),
               D("রাতুল", "শিখলাম যে নামার আগে নামটা পড়া দরকার!", "shikhlam je namar age namṭa pôṛa dôrkar!", "I learned that you should read the name before getting off!")],
              WS("Ending worksheet", [
                  T("Close the story.", ["I was tired but it worked out", "I lost the key and found it"],
                    ["শেষে দেখা গেল পরিশ্রমটা সার্থক", "শেষে দেখা গেল চাবিটা পকেটেই ছিল"]),
                  T("Turn it into a lesson.", ["check before you go", "time is worth watching"],
                    ["শিখলাম যে যাওয়ার আগে দেখা দরকার", "শিখলাম যে সময় দেখা জরুরি"]),
              ])),
        ]},
        {"id": "A2+-U3", "title": "Invitations and the phone", "lessons": [
            L("Inviting: চলুন, আসবেন",
              "Invitations are soft imperatives: চলুন (let's go), আসবেন (you'll come), খাবেন? (will "
              "you eat?), কী বলেন? (what do you say?). The plural/polite ending does the inviting.",
              [V("চলুন", "chôlun", "let's go (polite)", "verb"),
               V("আসবেন", "ashben", "you will come (polite)", "verb"),
               V("কী বলেন?", "ki bolen?", "what do you say?", "phrase"),
               V("আমন্ত্রণ", "amontron", "invitation", "noun"),
               V("অতিথি", "ôtithi", "guest", "noun")],
              G("Invitation frames",
                "chôlun + verb · ashben? · ki bolen?",
                "কাল আমাদের বাড়িতে চলুন. চা খাবেন? কী বলেন, রাজি? The polite ending turns a "
                "statement into an invitation without any extra word.",
                [X("আজ সন্ধ্যায় চলুন, চা খাবেন।", "aj shondhæ chôlun, cha khaben.", "Come this evening — will you have tea?"),
                 X("আমাদের বাড়িতে আসবেন, দয়া করে।", "amader baṛite ashben, dôya kôre.", "Please come to our house."),
                 X("রাজি হলে বলুন, আমি ব্যবস্থা করব।", "raji hole bolun, ami bêbostha kôrbo.", "If you agree, tell me — I'll arrange it.")],
                [("তুমি চলো আমাদের বাড়ি।", "চলুন আমাদের বাড়িতে।", "চলুন is the polite invitation form."),
                 ("আমাদের বাড়িতে আসুন চলুন।", "আমাদের বাড়িতে চলুন / আসবেন?", "Two invitations in one line — pick one.")]),
              [D("মিতা", "কাল সন্ধ্যায় আমাদের বাড়িতে চলুন।", "kal shondhæ amader baṛite chôlun.", "Come to our house tomorrow evening."),
               D("রাতুল", "খুব ভালো, কী উপলক্ষ?", "khub bhalo, ki upolokkho?", "Very good — what's the occasion?"),
               D("মিতা", "সুমির জন্মদিন, ছোট আয়োজন।", "Sumir jônmodin, chhoṭ ayojôn.", "Sumi's birthday, a small party."),
               D("রাতুল", "অবশ্যই আসব, ধন্যবাদ! কখন আসব?", "oboshshoi ashbo, dhonnobad! kôkhon ashbo?", "I'll certainly come, thank you! When should I come?")],
              WS("Invitation worksheet", [
                  T("Invite in Bengali.", ["to a birthday", "for tea", "to visit our house"],
                    ["জন্মদিনে চলুন", "চা খাবেন?", "আমাদের বাড়িতে আসবেন"]),
                  T("Extend the invitation.", ["a friend", "the family"],
                    ["বন্ধুকেও নিয়ে আসুন", "পরিবারসহ আসবেন"]),
              ])),
            L("Accepting and declining",
              "Yes is অবশ্যই (of course) or খুশি হয়ে (gladly). No is দুঃখিত, পারব না — with a reason, "
              "and usually with an alternative. Bengali declines with regret, not with brevity.",
              [V("অবশ্যই", "oboshshoi", "of course", "adverb"),
               V("খুশি হয়ে", "khushi hoye", "gladly", "phrase"),
               V("পারব না", "parbo na", "I will not be able", "phrase"),
               V("ব্যস্ত", "bêsto", "busy", "adjective"),
               V("পরের বার", "porer bar", "next time", "phrase")],
              G("Accept / decline + keep the door open",
                "oboshshoi, khushi hoye · dukkhito, parbo na + reason · porer bar",
                "অবশ্যই আসব, খুশি হয়েই আসব. দুঃখিত, কাল পারব না — কারণ কাজ আছে; পরের বার নিশ্চিত। "
                "The third clause is what keeps the invitation alive.",
                [X("অবশ্যই, খুব খুশি হব।", "oboshshoi, khub khushi hôbo.", "Of course, I would be very glad."),
                 X("দুঃখিত, এই সময় পারব না।", "dukkhito, ei shomoy parbo na.", "Sorry, I cannot at this time."),
                 X("পরের বার নিশ্চিত আসব।", "porer bar nishchito ashbo.", "I will certainly come next time.")],
                [("দুঃখিত, না।", "দুঃখিত, পারব না — পরের বার যেন হয়।", "A bare no ends the invitation."),
                 ("আমি পারব কি না পারব।", "আমি পারব না।", "Bengali negation is direct: পারব না.")]),
              [D("রাতুল", "কালকের আয়োজনে আসবেন?", "kalker ayojone ashben?", "Will you come to tomorrow's event?"),
               D("সুমি", "দুঃখিত, কাল পারব না — একটা পরীক্ষা আছে।", "dukkhito, kal parbo na — ekṭa porikkha achhe.", "Sorry, I can't tomorrow — there is an exam."),
               D("রাতুল", "ঠিক আছে, চিন্তা নেই।", "ṭhik achhe, chinta nei.", "That's fine, no worries."),
               D("সুমি", "পরের বার নিশ্চিত আসব, কথা দিলাম।", "porer bar nishchito ashbo, kôtha dilam.", "I'll certainly come next time — I promise.")],
              WS("Answer worksheet", [
                  T("Accept and decline.", ["invitation to dinner (accept)", "invitation to travel (decline, reason)"],
                    ["অবশ্যই আসব, খুশি হয়েই", "দুঃখিত, পারব না — কাজ আছে"]),
                  T("Keep the door open.", ["decline and promise next time"],
                    ["পরের বার নিশ্চিত আসব"]),
              ])),
            L("On the phone: কে বলছেন?",
              "Phone Bengali has its own openers: হ্যালো, কে বলছেন? (who is speaking?), একটু ধরুন "
              "(hold a moment), পরে ফোন করব (I'll call later), লাইন কেটে গেল (the line cut).",
              [V("হ্যালো", "hyalo", "hello (phone)", "interjection"),
               V("কে বলছেন?", "ke bolchhen?", "who is speaking?", "phrase"),
               V("ধরুন", "dhôrun", "hold (the line)", "verb"),
               V("ফোন করা", "phon kôra", "to phone", "verb"),
               V("লাইন", "lain", "line", "noun")],
              G("Phone frames",
                "hyalo? · ke bolchhen? · ekṭu dhôrun · pôre phon kôrbo",
                "হ্যালো, কে বলছেন? একটু ধরুন, ডাকছি. If the line breaks: দুঃখিত, লাইন কেটে গেল, "
                "আবার ফোন করব.",
                [X("হ্যালো, কে বলছেন?", "hyalo, ke bolchhen?", "Hello, who is speaking?"),
                 X("একটু ধরুন, আমি ডাকছি।", "ekṭu dhôrun, ami ḍakchhi.", "Hold a moment, I'm calling him."),
                 X("লাইন কেটে গেল, আবার ফোন করব।", "lain keṭe gelo, abar phon kôrbo.", "The line cut — I'll call again.")],
                [("হ্যালো, কে বলছেন আপনি?", "হ্যালো, কে বলছেন?", "The fixed frame already means 'who is speaking'; adding আপনি is redundant."),
                 ("আমি পরে ফোন করব তোমাকে।", "আমি পরে ফোন করব।", "Bengali ফোন করা takes no indirect object in this frame.")]),
              [D("রাতুল", "হ্যালো, কে বলছেন?", "hyalo, ke bolchhen?", "Hello, who is speaking?"),
               D("সুমি", "আমি সুমি। মিতা আছেন?", "ami Sumi. Mita achhen?", "It's Sumi. Is Mita there?"),
               D("রাতুল", "একটু ধরুন, ডাকছি।", "ekṭu dhôrun, ḍakchhi.", "Hold a moment, I'm calling her."),
               D("সুমি", "ধন্যবাদ, লাইন কেটে গেল না তো?", "dhonnobad, lain keṭe gelo na to?", "Thanks — the line didn't cut, did it?")],
              WS("Phone worksheet", [
                  T("Open the call in Bengali.", ["answer the phone", "ask who is speaking", "ask them to hold"],
                    ["হ্যালো", "কে বলছেন?", "একটু ধরুন"]),
                  T("Handle a bad line.", ["the line cut", "call later", "say goodbye"],
                    ["লাইন কেটে গেল", "পরে ফোন করব", "আবার কথা হবে"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Bengali conversation rewards the listener: সত্যি? and তাই নাকি? are expected at the "
                 "right moment, and a story is judged by how the teller closes it — usually with a "
                 "small admission and a laugh. Addabaj (আড্ডা) is the word for the unhurried talk that "
                 "is the point of the meeting, and cutting it short to get to business is the foreign "
                 "move a learner is forgiven for once."),
        source_url="https://en.wikipedia.org/wiki/Adda_(South_Asian)",
        reading=("কাল সন্ধ্যায় আমরা আড্ডা দিচ্ছিলাম। প্রথমে গল্প ছিল অফিস নিয়ে, তারপর হঠাৎ সুমি তার "
                 "গ্রামের কথা বলতে শুরু করল — নদী, আমগাছ আর শীতের পিঠা। আমরা সবাই চুপ করে "
                 "শুনছিলাম, কেউ প্রশ্ন করছিলাম না। শেষে দেখা গেল রাত বারোটা বেজে গেছে, আর "
                 "কেউ ঘরে ফিরতে চায় না। শিখলাম যে ভালো আড্ডার কোনো সময়সীমা নেই, শুধু "
                 "একজন শুনতে জানা মানুষ দরকার।"),
        reading_gloss=("Yesterday evening we were having an adda. At first the talk was about the "
                       "office, then suddenly Sumi began to speak about her village. We all listened "
                       "in silence. In the end it turned out that midnight had passed, and nobody "
                       "wanted to go home. I learned that a good adda has no time limit."),
        listening=("মিতা: হ্যালো, কে বলছেন?<br>সুমি: আমি সুমি। আজ সন্ধ্যায় আসবেন?<br>"
                   "মিতা: দুঃখিত, আজ পারব না। কাল হলে ভালো হয়।<br>সুমি: ঠিক আছে, কাল অপেক্ষা করব।"),
        listening_gloss=("Mita: Hello, who is speaking? Sumi: It's Sumi. Will you come this evening? "
                         "Mita: Sorry, I can't today. Tomorrow would be better. Sumi: All right, I'll "
                         "wait for tomorrow."),
        voice_tag=VOICE,
        idioms=[
            ("আড্ডা দেওয়া", "to give adda", "to sit and chat unhurriedly"),
            ("আলাপচারিতায়", "in conversation", "in the course of chatting"),
            ("হাসি-ঠাট্টা", "laughter and jokes", "banter"),
            ("কানে কানে", "ear to ear", "whispering"),
            ("একটা কথা শুনুন", "listen to one thing", "let me tell you something"),
            ("সময়ের কথা", "talk of time", "a word about when"),
            ("মনের কথা", "the mind's words", "what one really thinks"),
            ("খোলাখুলি", "openly", "frankly, in the open"),
            ("হালকা কথা", "light talk", "small talk"),
            ("কথার মাঝে", "in the middle of talk", "interrupting briefly"),
        ],
        mistakes=[
            ("আমি পারব না না।", "আমি পারব না।", "Bengali has one negative; doubling is not emphasis."),
            ("হ্যালো, কে বলছেন আপনি?", "হ্যালো, কে বলছেন?", "Fixed phone phrase, without আপনি."),
            ("প্রথমে তারপর এরপর শেষে একদিন সব হয়ে গেল।", "(one connector per step)", "A chain of markers is a list, not a story."),
        ],
        task_title="Tell me a two-minute story",
        task_instructions=("Record yourself telling a real story in Bengali for two minutes: প্রথমে for "
                           "the scene, a ছিল-clause for the background, হঠাৎ for the turn, and a close "
                           "with শেষে দেখা গেল যে. Then listen back and count the reactions you left "
                           "out — every সত্যি? your listener needed is a place the story ran without "
                           "them."),
    ),
    "test": [
        ("translate_en", "Say: Really? And then what happened?", "সত্যি? তারপর কী হলো?"),
        ("translate_ar", "কেমন লাগল?", "How did it feel?"),
        ("multiple_choice", "Which invitation is the softest?", "আমাদের বাড়িতে আসবেন?"),
        ("fill_in_the_blank", "হঠাৎ বিদ্যুৎ ___ গেল। (went)", "চলে"),
        ("word_selection", "Select the Bengali for 'congratulations'.", "অভিনন্দন"),
        ("error_correction", "হঠাৎ বিদ্যুৎ।", "হঠাৎ বিদ্যুৎ চলে গেল।"),
        ("dialogue_completion", "Complete: দুঃখিত, পারব না — ___ (next time, certainly)", "পরের বার নিশ্চিত আসব"),
        ("matching", "Match শেষে দেখা গেল to its meaning.", "in the end it turned out"),
        ("reading_comprehension", "প্রথমে গল্প অফিস নিয়ে, তারপর গ্রাম নিয়ে। What changed?", "the subject of the talk"),
        ("inference", "«শেষে দেখা গেল রাত বারোটা বেজে গেছে» — what does it tell us?", "they talked for hours without noticing"),
        ("main_idea", "আমরা সবাই চুপ করে শুনছিলাম। What is happening?", "everyone is listening quietly"),
        ("detail_identification", "কাল অপেক্ষা করব। When will she wait?", "tomorrow"),
    ],
}

HALFSTEPS["B1+"] = {
    "title": "Bengali B1+ — Comfortable",
    "native": NATIVE,
    "goals": [
        "Say what you want, need and intend, with the right strength",
        "Give your opinion and disagree without a fight",
        "Move between polite আপনি and friendly তুমি, and know the difference",
    ],
    "units": [
        {"id": "B1+-U1", "title": "Wants, needs and intentions", "lessons": [
            L("Three strengths: চাই, দরকার, ইচ্ছা",
              "Bengali separates wanting into three: চাই (I want — desire), দরকার (need — "
              "requirement), ইচ্ছা (wish, inclination). Choosing the wrong one makes you sound "
              "demanding or cold.",
              [V("চাই", "chai", "I want", "verb"),
               V("দরকার", "dôrkar", "need, necessary", "noun"),
               V("ইচ্ছা", "ichchha", "wish, desire", "noun"),
               V("অনুরোধ", "onurodh", "request", "noun"),
               V("জরুরি", "joruri", "urgent", "adjective")],
              G("Desire, need, wish",
                "amar … chai · amar … dôrkar · amar … ichchha (achhe)",
                "আমার একটা চা চাই (desire). আমার তোমার সাহায্য দরকার (need). আমার যেতে ইচ্ছা করছে "
                "(wish). The subject takes amar in all three — the thing wanted does not become a "
                "subject.",
                [X("আমার আপনার সাহায্য দরকার।", "amar apnar shahajjo dôrkar.", "I need your help."),
                 X("আমার একটা প্রশ্ন জিজ্ঞেস করতে ইচ্ছা করছে।", "amar ekṭa proshno jiggesh korte ichchha kôrchhe.", "I have a wish to ask a question."),
                 X("আমার আজ বাড়ি যাওয়া জরুরি।", "amar aj baṛi jaoa joruri.", "It is urgent for me to go home today.")],
                [("আমি তোমার সাহায্য লাগে।", "আমার তোমার সাহায্য দরকার।", "দরকার takes amar, not ami."),
                 ("আমার চা চাই না চাই।", "আমার চা চাই।", "One desire is one চাই.")]),
              [D("রাতুল", "আপনার কী দরকার?", "apnar ki dôrkar?", "What do you need?"),
               D("সুমি", "আমার একটা কাগজ আর কলম দরকার।", "amar ekṭa kagôj ar kôlom dôrkar.", "I need a piece of paper and a pen."),
               D("রাতুল", "আর কিছু চাই?", "ar kichhu chai?", "Anything else you want?"),
               D("সুমি", "না, ধন্যবাদ — এখন কাজ শেষ করতে ইচ্ছা করছে।", "na, dhonnobad — ekhon kaj shesh korte ichchha kôrchhe.", "No, thanks — now I want to finish the work.")],
              WS("Wants worksheet", [
                  T("Choose the right word.", ["I need water", "I want tea", "I feel like going out"],
                    ["আমার পানি দরকার", "আমার চা চাই", "আমার ঘুরতে যেতে ইচ্ছা করছে"]),
                  T("Ask a colleague.", ["what do you need?", "anything else?", "is it urgent?"],
                    ["আপনার কী দরকার?", "আর কিছু চাই?", "জরুরি কি?"]),
              ])),
            L("Intentions: আমি চাই ⇒ আমি করব",
              "Intention is asked with চান? and answered with the future: আমি চাই, আমি করব. Bengali "
              "also marks a decision just taken with করব বলে ঠিক করেছি (I've decided to…).",
              [V("করব", "kôrbo", "I will do", "verb"),
               V("ঠিক করেছি", "ṭhik korechhi", "I have decided", "phrase"),
               V("পরিকল্পনা", "porikôlpona", "plan", "noun"),
               V("চান", "chan", "you want (polite)", "verb"),
               V("হবে", "hobe", "it will be", "verb")],
              G("Intention frames",
                "ami … kôrbo · … kôrbar porikôlpona achhe · ṭhik korechhi je…",
                "আমি চাকরি বদলাব বলে ঠিক করেছি. আপনার কী করার পরিকল্পনা আছে? Intention is "
                "practical in Bengali: the plan is stated, then the detail.",
                [X("আমি আগামী মাসে চাকরি বদলাব।", "ami ôgamī masе chakri bôdlabo.", "I will change jobs next month."),
                 X("আমি বাংলা শেখার পরিকল্পনা করেছি।", "ami Bangla shekhar porikôlpona korechhi.", "I have made a plan to learn Bengali."),
                 X("আপনি কিছু করার কথা ভাবছেন?", "apni kichhu kôrar kôtha bhabchhen?", "Are you thinking of doing something?")],
                [("আমি করব আদেশ।", "আমি করব।", "Corruptions like these come from translating per word — the future form is enough."),
                 ("আমার করব।", "আমি করব।", "Intentions take ami, needs take amar — do not mix them.")]),
              [D("মিতা", "ছুটিতে কী করবেন?", "chhuṭite ki kôrben?", "What will you do on the holiday?"),
               D("রাতুল", "আমি গ্রামে যাব বলে ঠিক করেছি।", "ami grame jabo bole ṭhik korechhi.", "I have decided to go to the village."),
               D("মিতা", "আর পড়াশোনা?", "ar pôṛashona?", "And studies?"),
               D("রাতুল", "সেটাও চলবে — সকালে পড়ব, দুপুরে ঘুরব।", "sheṭao chôlbe — shokale pôṛbo, dupure ghurbo.", "That will continue too — I'll study in the morning and go out at noon.")],
              WS("Intention worksheet", [
                  T("State your intention.", ["change jobs", "learn Bengali", "visit Dhaka"],
                    ["আমি চাকরি বদলাব", "আমি বাংলা শিখব", "আমি ঢাকা যাব"]),
                  T("Say you have decided.", ["to move house", "to start a course"],
                    ["আমি বাড়ি বদলাব বলে ঠিক করেছি", "আমি কোর্স শুরু করব বলে ঠিক করেছি"]),
              ])),
            L("Persuading without pushing",
              "Persuasion in Bengali leans on shared gain: একসাথে হলে ভালো, আপনি ভাবুন, ছোট করে "
              "দেখি. The softest push is a question; the hardest is চাই-ই (I insist).",
              [V("একসাথে", "ekshathe", "together", "adverb"),
               V("ভাবুন", "bhabun", "think (polite imperative)", "verb"),
               V("যদি", "jodi", "if", "conjunction"),
               V("লাভ", "labh", "benefit, gain", "noun"),
               V("রাজি", "raji", "agreeing, willing", "adjective")],
              G("Soft persuasion",
                "jodi … hoy, tahole … · apni bhabun · chhoṭ kore dekhi",
                "যদি দুজনেই রাজি হই, তাহলে কাজটা সহজ হবে. আপনি ভাবুন — সময় আছে. The conditional "
                "lets the listener reach the conclusion; the imperative hands it to them.",
                [X("যদি আপনি রাজি হন, আমরা একসাথে কাজ করি।", "jodi apni raji hôn, amra ekshathe kaj kôri.", "If you agree, let's work together."),
                 X("আপনি একবার ভাবুন, লাভটা সবার।", "apni ekbar bhabun, labhṭa shôbar.", "Think about it once — the gain is everyone's."),
                 X("ছোট একটা পরিকল্পনা দেখি, তারপর বলুন।", "chhoṭ ekṭa porikôlpona dekhi, tarpor bolun.", "Let me show a small plan, then you tell me.")],
                [("আপনি করবেনই, শুনবেন না অন্য।", "আপনি ভাবুন, তারপর সিদ্ধান্ত।", "Pushing past the listener's decision ends the conversation."),
                 ("যদি রাজি হই, তবে রাজি।", "যদি রাজি হন, একসাথে শুরু করি।", "The conditional needs a result clause with content.")]),
              [D("সুমি", "কেন আমরা সপ্তাহে একদিন পড়তে বসি না?", "keno amra shoptahе ekdin pôṛte bôshi na?", "Why don't we sit down to study one day a week?"),
               D("মিতা", "সময় কম, ভয় লাগে।", "shomoy kôm, bhoy lage.", "There is little time — I'm afraid."),
               D("সুমি", "আপনি ভাবুন: যদি দুজন থাকি, তাহলে ছাড়ার ইচ্ছা কমবে।", "apni bhabun: jodi dujon thaki, tahole chhaṛar ichchha kômbe.", "Think about it: if there are two of us, the urge to quit will be less."),
               D("মিতা", "ঠিক বলেছেন — একদিন দেখি, তারপর ঠিক করি।", "ṭhik bolechhen — ekdin dekhi, tarpor ṭhik kôri.", "You are right — let's try one day, then decide.")],
              WS("Persuasion worksheet", [
                  T("Build the conditional.", ["we agree → the work is easy", "you come → we finish today"],
                    ["যদি আমরা রাজি হই, কাজটি সহজ হবে", "যদি আপনি আসেন, আজই শেষ হবে"]),
                  T("Soften the request.", ["do it (direct)", "think about it"],
                    ["একবার দেখা যায়?", "আপনি একবার ভাবুন"]),
              ])),
        ]},
        {"id": "B1+-U2", "title": "Opinions and disagreement", "lessons": [
            L("Stating an opinion with a hedge",
              "Opinions come with a frame: আমি মনে করি… (I think), আমার মনে হয়… (it seems to me), "
              "আমার কাছে মনে হয়… All three leave room; without one, an opinion sounds like a verdict.",
              [V("মনে করি", "mone kôri", "I think", "phrase"),
               V("মনে হয়", "mone hôy", "it seems", "phrase"),
               V("মতে", "môte", "according to (someone)", "postposition"),
               V("দৃষ্টিতে", "drishtite", "in view, from the standpoint", "noun"),
               V("মতামত", "môtamôt", "opinion", "noun")],
              G("Opinion frames",
                "ami mone kôri je… · amar mone hôy je… · amar môte…",
                "আমি মনে করি যে পরিকল্পনাটা কাজে দেবে. যুক্তি আছে, তবে সময় কম. Adding যুক্তি আছে "
                "(there is a reason) after a hedge makes the disagreement reasonable.",
                [X("আমি মনে করি সময়টা যথেষ্ট।", "ami mone kôri shomoyṭa jôtheshṭo.", "I think the time is sufficient."),
                 X("আমার মতে প্রস্তাবটা ভালো, তবে ব্যয় বেশি।", "amar môte prostabṭa bhalo, tôbe bêy bеshi.", "In my opinion the proposal is good, but the cost is high."),
                 X("আমার কাছে মনে হয় সমস্যাটা অন্য জায়গায়।", "amar kachhe mone hôy shomoshshaṭa ônno jaygay.", "It seems to me the problem is elsewhere.")],
                [("আমি মনে করি না আমি মনে করি।", "আমি মনে করি…", "The frame is a fixed opener, used once per point."),
                 ("মতে আমি ভালো।", "আমার মতে এটা ভালো।", "মতে needs a possessor: আমার মতে.")]),
              [D("প্রধান", "নতুন নিয়ম নিয়ে কী বলেন?", "nôtun niyom niye ki bolen?", "What do you say about the new rule?"),
               D("রাতুল", "আমার মতে নিয়মটা ঠিক, কিন্তু সময় কম।", "amar môte niyomṭa ṭhik, kintu shomoy kôm.", "In my opinion the rule is right, but there is little time."),
               D("প্রধান", "আর কিছু?", "ar kichhu?", "Anything else?"),
               D("রাতুল", "আমি মনে করি এক মাস পর্যালোচনা দরকার।", "ami mone kôri ek mash pôryalochona dôrkar.", "I think a one-month review is needed.")],
              WS("Opinion worksheet", [
                  T("Give an opinion with a frame.", ["the plan will work", "the price is too high", "we need more time"],
                    ["আমি মনে করি পরিকল্পনাটা কাজে দেবে", "আমার মতে দাম বেশি", "আমার কাছে মনে হয় আরও সময় দরকার"]),
                  T("Hedge and add a reason.", ["good but costly", "useful but late"],
                    ["ভালো, তবে ব্যয় বেশি", "উপকারী, তবে দেরি হয়েছে"]),
              ])),
            L("Disagreeing with the person intact",
              "The Bengali disagreeing ladder: আপনি ঠিক, তবে…, আমি একটু অন্যভাবে দেখি, একমত নই "
              "কিন্তু বুঝি. Start where you agree — that is not politeness, it is how the sentence is "
              "built.",
              [V("তবে", "tôbe", "however, but", "conjunction"),
               V("একমত", "ekmôt", "agreeing", "adjective"),
               V("দ্বিমত", "dimiôt", "disagreement", "noun"),
               V("ভিন্ন", "bhinn", "different", "adjective"),
               V("সম্মান", "shômman", "respect", "noun")],
              G("Disagreement ladder",
                "apni ṭhik, tôbe… · ami ekṭu ônnobhabe dekhi · môt bhinn, kintu shômman kôri",
                "আপনি ঠিক, তবে একটা দিক বাদ পড়েছে. আমি একটু অন্যভাবে দেখি — কারণটা দুটো. Bengali "
                "sometimes needs two concessive sentences; one is heard as a token, two as a position.",
                [X("আপনি ঠিক, তবে তথ্যটা পুরো নয়।", "apni ṭhik, tôbe tôthỹaṭa puro nôy.", "You are right, but the data is not complete."),
                 X("আমি একটু অন্যভাবে দেখি, তবে একমত হওয়া সম্ভব।", "ami ekṭu ônnobhabe dekhi, tôbe ekmôt hoa shombhob.", "I see it a little differently, though agreement is possible."),
                 X("মত আলাদা, তবু আপনার যুক্তি মানি।", "môt alada, tôbu apnar jukti mani.", "Our views differ, yet I accept your reasoning.")],
                [("আপনি ঠিক, তবে আপনি ভুল।", "আপনি ঠিক, তবে একটা জায়গায় আমি দ্বিমত।", "A concession cancelled in the same clause is a contradiction, not a debate."),
                 ("ঠিক বলে, তবে কিছু ঠিক না।", "ঠিক বলে, তবে সবটা নয়।", "Keep the scope of the concession honest.")]),
              [D("সুমি", "আমার প্রস্তাব: প্রতিদিন এক ঘণ্টা।", "amar prostab: protidin ek ghônṭa.", "My proposal: one hour a day."),
               D("রাতুল", "আপনি ঠিক, তবে নিয়মিত এক ঘণ্টা কঠিন।", "apni ṭhik, tôbe niyomito ek ghônṭa kôthin.", "You are right, but a regular hour is hard."),
               D("সুমি", "তাহলে?", "tahole?", "Then?"),
               D("রাতুল", "আমি একটু অন্যভাবে দেখি — দিনে দুবার আধা ঘণ্টা।", "ami ekṭu ônnobhabe dekhi — dine dubar adha ghônṭa.", "I see it a little differently — half an hour twice a day.")],
              WS("Disagreement worksheet", [
                  T("Disagree, keeping respect.", ["the deadline is realistic", "the plan is cheap"],
                    ["আপনি ঠিক, তবে সময়সীমা কঠিন", "মত আলাদা, তবে যুক্তি মানি"]),
                  T("Concede then differ.", ["the report is good (but late)", "the idea is right (but costly)"],
                    ["রিপোর্ট ভালো, তবে দেরি হয়েছে", "ধারণাটা ঠিক, তবে ব্যয় বেশি"]),
              ])),
            L("Six softeners that change the room",
              "একটু (a little), হয়তো (perhaps), মোটামুটি (roughly), কিছুটা (somewhat), প্রায় "
              "(almost), আপাতত (for now). Bengali softeners go before the adjective and can turn a "
              "criticism into an observation.",
              [V("হয়তো", "hôyto", "perhaps", "adverb"),
               V("মোটামুটি", "môṭamuti", "roughly, fairly", "adverb"),
               V("প্রায়", "pray", "almost", "adverb"),
               V("আপাতত", "apatôt", "for now", "adverb"),
               V("একটু", "ekṭu", "a little", "adverb")],
              G("Softeners before the word they soften",
                "ekṭu · hôyto · môṭamuti · pray · apatat + adjective",
                "দামটা একটু বেশি. কাজটা মোটামুটি হয়েছে. আপাতত এটাই ঠিক আছে. Compare দাম বেশি — "
                "the bare version is a verdict; with একটু it is a negotiation.",
                [X("সময়টা একটু কম লাগছে।", "shomoyṭa ekṭu kôm lagchhe.", "The time feels a little short."),
                 X("কাজটা মোটামুটি হয়েছে।", "kajṭa môṭamuti hoyechhe.", "The work has turned out fairly."),
                 X("আপাতত এটাই নিয়ে চলি।", "apatôt eṭai niye chôli.", "For now, let's go on with this.")],
                [("প্রায় সব ঠিক, না ঠিক।", "প্রায় সব ঠিক।", "প্রায় is not a hedge that reverses itself."),
                 ("হয়তো হয়তো আসবে।", "হয়তো আসবে।", "One chance word per sentence.")]),
              [D("কর্তা", "রিপোর্টটা কেমন?", "ripôrṭṭa kemon?", "How is the report?"),
               D("লেখক", "মোটামুটি হয়েছে, তবে একটা অংশ একটু দুর্বল।", "môṭamuti hoyechhe, tôbe ekṭa ôngsho ekṭu durbôl.", "It has turned out fairly, but one part is a little weak."),
               D("কর্তা", "কোনটা?", "kônṭa?", "Which one?"),
               D("লেখক", "আপাতত সংখ্যার অংশ — হয়তো সোমবারের মধ্যে ঠিক করব।", "apatôt shôngkhar ôngsho — hôyto shombarer moddhe ṭhik kôrbo.", "For now, the numbers part — perhaps I'll fix it by Monday.")],
              WS("Soften worksheet", [
                  T("Soften the criticism.", ["it is expensive", "you are late", "this is wrong"],
                    ["একটু বেশি", "একটু দেরি হয়েছে", "একটু অন্যভাবে দেখি"]),
                  T("Add a hedge.", ["he will come", "we will finish", "the price will rise"],
                    ["হয়তো আসবে", "হয়তো শেষ হবে", "হয়তো দাম বাড়বে"]),
              ])),
        ]},
        {"id": "B1+-U3", "title": "Register: আপনি, তুমি, তুই", "lessons": [
            L("Choosing the pronoun",
              "Bengali has three: আপনি (respectful, distance), তুমি (friendly, equal), তুই (intimate "
              "or rude, depending on the listener). The verb ending follows the pronoun; mixing them "
              "mid-sentence is the clearest sign of a learner.",
              [V("আপনি", "apni", "you (respectful)", "pronoun"),
               V("তুমি", "tumi", "you (friendly)", "pronoun"),
               V("তুই", "tui", "you (intimate)", "pronoun"),
               V("শ্রদ্ধা", "shroddha", "respect", "noun"),
               V("সম্বোধন", "shômbodhon", "address (form of)", "noun")],
              G("Pronoun governs the verb",
                "apni kôrben · tumi kôrbe · tui kôrbi",
                "আপনি আসবেন, তুমি আসবে, তুই আসবি. To an older person the polite form is "
                "obligatory; to a friend, তুমি; to a very close friend or a child, তুই. Getting this "
                "wrong is the loudest mistake in Bengali.",
                [X("আপনি কেমন আছেন?", "apni kemon achhen?", "How are you? (respectful)"),
                 X("তুমি কেমন আছ?", "tumi kemon achho?", "How are you? (friendly)"),
                 X("তুই কেমন আছিস?", "tui kemon achhish?", "How are you? (intimate)")],
                [("আপনি আসবে?", "আপনি আসবেন?", "আপনি takes -ben endings."),
                 ("তুমি আসুন।", "তুমি এসো।", "তুমি takes -o/-be, never -un.")]),
              [D("রাতুল", "আপনি কেমন আছেন, আন্টি?", "apni kemon achhen, anṭi?", "How are you, aunty?"),
               D("কাকিমা", "ভালো আছি, তুমি কেমন আছ?", "bhalo achhi, tumi kemon achho?", "I am well — how are you?"),
               D("রাতুল", "ভালো আছি। দাদু কেমন আছেন?", "bhalo achhi. dadu kemon achhen?", "I am well. How is grandfather?"),
               D("কাকিমা", "তিনি ভালো আছেন, তোমাকে মনে করছিলেন।", "tini bhalo achhen, tomake mone kôrchhilen.", "He is well; he was remembering you.")],
              WS("Register worksheet", [
                  T("Choose the right form.", ["to your teacher", "to your friend", "to your little brother"],
                    ["আপনি আসবেন", "তুমি আসবে", "তুই আসবি"]),
                  T("Answer respectfully.", ["how are you?", "your name?", "where do you live?"],
                    ["আপনি কেমন আছেন?", "আপনার নাম কী?", "আপনি কোথায় থাকেন?"]),
              ])),
            L("Word pairs: খাওয়া and খাওয়ানো",
              "Register and meaning meet in word pairs: খাওয়া/খাওয়ানো (eat/feed), বলা/বলানো (say/"
              "have said), শেখা/শেখানো (learn/teach). The -no/-ano form is the causative — someone "
              "else performs the action.",
              [V("খাওয়ানো", "khaoano", "to feed", "verb"),
               V("শেখানো", "shekhano", "to teach", "verb"),
               V("বলানো", "bôlano", "to have something said", "verb"),
               V("দেখানো", "dekhano", "to show", "verb"),
               V("করানো", "kôrano", "to have something done", "verb")],
              G("Causative -ano",
                "root + -ano / -no: khaowa → khaoano · shekha → shekhano",
                "আমি বাংলা শিখছি, তিনি আমাকে শেখাচ্ছেন. যন্ত্র কাজটা করাবে না, মানুষ করাবে — the "
                "causative names who acts through whom.",
                [X("মা ছেলেকে ভাত খাওয়াচ্ছেন।", "ma chheleke bhat khaoachhen.", "The mother is feeding the son rice."),
                 X("শিক্ষক আমাদের বাংলা শেখান।", "shikkhok amader Bangla shekhan.", "The teacher teaches us Bengali."),
                 X("আমি দোকানে জুতো ঠিক করিয়েছি।", "ami dokane juto ṭhik koriyechhi.", "I had the shoes repaired at the shop.")],
                [("আমি ভাত খাওয়াচ্ছি। (about myself)", "আমি ভাত খাচ্ছি / আমি ছেলেকে খাওয়াচ্ছি।", "The causative needs someone else being fed."),
                 ("শিক্ষক শেখে।", "শিক্ষক শেখায় / শেখান।", "A teacher teaches: use the causative, not শেখে.")]),
              [D("সুমি", "ছেলেটা ভাত খাচ্ছে না।", "chheleṭa bhat khachhe na.", "The child is not eating rice."),
               D("মিতা", "তুমি একটু খাওয়াও, তারপর আমি শেখাব।", "tumi ekṭu khaoao, tarpor ami shekhabo.", "You feed him a little, then I'll teach him."),
               D("সুমি", "ঠিক আছে — আর জুতোটা ঠিক করাতে হবে।", "ṭhik achhe — ar juṭoṭa ṭhik kôrate hobe.", "All right — and the shoes need repairing too."),
               D("মিতা", "আমি দোকানে করিয়ে আনব।", "ami dokane koriye anbo.", "I'll have it done at the shop.")],
              WS("Causative worksheet", [
                  T("Turn it into the causative.", ["I ate → I fed the child", "I learned → the teacher taught me", "I did → I had it done"],
                    ["আমি ছেলেকে খাওয়ালাম", "শিক্ষক আমাকে শেখালেন", "আমি করিয়ে নিলাম"]),
                  T("Say who does what.", ["the mother feeds", "the teacher teaches", "the shop repairs"],
                    ["মা খাওয়ান", "শিক্ষক শেখান", "দোকান ঠিক করে দেয়"]),
              ])),
            L("Greetings that match the person",
              "Bengali greets with the moment: শুভ সকাল (good morning), আসসালামু আলাইকুম (Muslim "
              "greeting), নমস্কার (Hindu greeting), খেয়েছেন? (have you eaten? — affectionate, used "
              "with intimates). Choosing well depends on the person, not the hour.",
              [V("শুভ সকাল", "shubho shokal", "good morning", "phrase"),
               V("আসসালামু আলাইকুম", "assalamu alaikum", "peace be upon you", "phrase"),
               V("নমস্কার", "nômoshkar", "respectful greeting", "phrase"),
               V("খেয়েছেন?", "kheyechhen?", "have you eaten? (greeting)", "phrase"),
               V("বিদায়", "biday", "farewell", "noun")],
              G("Greeting by person",
                "shubho shokal / nômoshkar / assalamu alaikum / kheyechhen?",
                "In a Hindu household নমস্কার; in a Muslim one আসসালামু আলাইকুম; among neighbours, "
                "খেয়েছেন? The reply to kheyechhen? is খেয়েছি, আপনিও খেয়েছেন? — the question comes "
                "back.",
                [X("শুভ সকাল, কেমন আছেন?", "shubho shokal, kemon achhen?", "Good morning, how are you?"),
                 X("আসসালামু আলাইকুম, সবাই ভালো?", "assalamu alaikum, shobai bhalo?", "Peace be upon you — is everyone well?"),
                 X("খেয়েছেন? — খেয়েছি, আপনি খেয়েছেন?", "kheyechhen? — kheyechhi, apni kheyechhen?", "Have you eaten? — I have; have you?")],
                [("হ্যালো আন্টি, খেয়েছেন।", "খেয়েছেন, আন্টি?", "The greeting is a question, not a report about the other person."),
                 ("নমস্কার, আসসালামু আলাইকুম।", "(choose one greeting)", "Two greetings in one line is a joke in Bengali, not politeness.")]),
              [D("রাতুল", "খেয়েছেন, আন্টি?", "kheyechhen, anṭi?", "Have you eaten, aunty?"),
               D("কাকিমা", "খেয়েছি, তুমি খেয়েছ?", "kheyechhi, tumi kheyechho?", "I have — have you?"),
               D("রাতুল", "খেয়েছি। বাবা বাড়ি আছেন?", "kheyechhi. baba baṛi achhen?", "I have. Is father at home?"),
               D("কাকিমা", "আছেন, ভিতরে বসুন।", "achhen, bhitore bôshun.", "He is — please sit inside.")],
              WS("Greeting worksheet", [
                  T("Greet the right way.", ["a Hindu elder", "a Muslim neighbour", "a close friend in the morning"],
                    ["নমস্কার", "আসসালামু আলাইকুম", "শুভ সকাল / খেয়েছ?"]),
                  T("Reply and return the greeting.", ["have you eaten? (yes, and you?)", "good morning (and to you)"],
                    ["খেয়েছি, আপনি খেয়েছেন?", "শুভ সকাল, আপনাকেও"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Register in Bengali is social geography: you address a rickshaw puller, a professor "
                 "and a childhood friend with three different pronouns, and getting it wrong is heard "
                 "as either arrogance or over-familiarity — rarely as grammar. Foreign learners are "
                 "usually placed on আপনি and forgiven for staying there too long; the mistake that "
                 "is not forgiven is dropping to তুই with someone older."),
        source_url="https://en.wikipedia.org/wiki/Bengali_grammar",
        reading=("আমার নতুন সহকর্মী প্রথম দিনেই বলল, «তুই কেমন আছিস?» আমি একটু অবাক হলাম, কারণ সে "
                 "আমার চেয়ে ছোট। পরে বুঝলাম, সে আমার সাথে বন্ধুত্ব করতে চায়। আমি উত্তর দিলাম, "
                 "«ভালো আছি, তুমি কেমন আছ?» — এক ধাপ উপরে থেকে। এখন আমরা দুজনেই তুমি বলি, এবং "
                 "কাজটা সহজ হয়েছে। শিখলাম যে ভাষার সম্বোধনও একটা আলোচনা।"),
        reading_gloss=("My new colleague said on the very first day, 'তুই কেমন আছিস?' I was a little "
                       "surprised, because he is younger than I am. Later I understood: he wanted to "
                       "become friends. I answered, 'ভালো আছি, তুমি কেমন আছ?' — from one step up. Now "
                       "we both use তুমি, and the work has become easier. I learned that address in a "
                       "language is also a negotiation."),
        listening=("সুমি: আমি যদি বলি তুই, খারাপ লাগবে?<br>মিতা: না, কিন্তু আগে জিজ্ঞেস করো।<br>"
                   "সুমি: তা হলে তুমি ঠিক — আমি আগে আপনার বলতাম, এখন তুমি বলব।<br>"
                   "মিতা: বাহ, এখন কথা সহজ হবে।"),
        listening_gloss=("Sumi: If I say তুই, will you mind? Mita: No, but ask first. Sumi: Then you are "
                         "right — I used to say আপনি, now I'll say তুমি. Mita: Great, talking will be "
                         "easier now."),
        voice_tag=VOICE,
        idioms=[
            ("সম্মান করা", "to give respect", "to honour someone"),
            ("ঘনিষ্ঠ হওয়া", "to become close", "to grow intimate with"),
            ("দূরত্ব রাখা", "to keep distance", "to keep one's distance"),
            ("মনের মত", "of one mind", "to someone's liking"),
            ("ভদ্র ভাষা", "polite language", "refined speech"),
            ("সোজাসুজি কথা", "straight talk", "plain speaking"),
            ("কথার সুতো", "the thread of talk", "the drift of a conversation"),
            ("স্বরে বোঝা", "to understand from the tone", "to read someone's tone"),
            ("মুখে বলা", "to say to the face", "to say openly"),
            ("পিছনে বলা", "to say behind a back", "to speak behind someone's back"),
        ],
        mistakes=[
            ("আপনি আসবে?", "আপনি আসবেন?", "আপনি always takes the -ben form."),
            ("তুমি ভাত খাওয়াচ্ছ। (about yourself)", "তুমি খাচ্ছ / তুমি ছেলেকে খাওয়াচ্ছ।", "The causative needs another person being fed."),
            ("হ্যালো আন্টি, আপনি খেয়েছেন।", "খেয়েছেন, আন্টি?", "The greeting form is a question about the other person."),
        ],
        task_title="Map your Bengali register",
        task_instructions=("Write four short dialogues in Bengali: with a professor, a colleague your "
                           "age, a child, and a very close friend. Use আপনি, তুমি and তুই in the right "
                           "places, and keep the verb endings consistent with each. Then read them "
                           "aloud, listening for the endings — if any sentence mixes registers, the "
                           "pronoun was the easy part and the verb is what you have to fix."),
    ),
    "test": [
        ("translate_en", "Say: I need your help, and I want to finish today.", "আমার আপনার সাহায্য দরকার, আর আমি আজই শেষ করতে চাই।"),
        ("translate_ar", "আমার মতে এটা ভালো, তবে ব্যয় বেশি।", "In my opinion this is good, but the cost is high."),
        ("multiple_choice", "Which reply fits «খেয়েছেন, আন্টি?»", "খেয়েছি, আপনি খেয়েছেন?"),
        ("fill_in_the_blank", "আপনি কেমন ___?", "আছেন"),
        ("word_selection", "Select the causative verb for 'to teach'.", "শেখানো"),
        ("error_correction", "আপনি আসবে?", "আপনি আসবেন?"),
        ("dialogue_completion", "Complete: একটু দেরি হয়েছে, তবে ___ (the work has turned out fairly)", "কাজটা মোটামুটি হয়েছে"),
        ("matching", "Match দ্বিমত to its meaning.", "disagreement"),
        ("reading_comprehension", "সে আমার চেয়ে ছোট, তবু বলল «তুই কেমন আছিস?» — what happened?", "he wanted to become friends"),
        ("inference", "«ভাষার সম্বোধনও একটা আলোচনা» — what does the writer mean?", "forms of address are negotiated between people"),
        ("main_idea", "এখন আমরা দুজনেই তুমি বলি। What changed?", "their level of address"),
        ("detail_identification", "আমি উত্তর দিলাম «তুমি কেমন আছ?» — which pronoun did the writer use?", "তুমি"),
    ],
}

HALFSTEPS["B2+"] = {
    "title": "Bengali B2+ — Professional",
    "native": NATIVE,
    "goals": [
        "Take part in a meeting: open, qualify, decide, follow up",
        "Write a message, a summary and a report of a meeting",
        "Negotiate a deadline without either promising too much or hiding",
    ],
    "units": [
        {"id": "B2+-U1", "title": "In the meeting", "lessons": [
            L("Opening, framing, closing down",
              "A Bengali meeting has fixed moves: শুরুতে (at the start), আলোচনার বিষয় (the matter "
              "under discussion), সিদ্ধান্তে পৌঁছানো (to reach a decision). Saying which move you are "
              "in is what makes you audible in a room.",
              [V("আলোচনা", "alochona", "discussion", "noun"),
               V("সিদ্ধান্ত", "siddhanto", "decision", "noun"),
               V("বিষয়", "bishôy", "matter, subject", "noun"),
               V("প্রস্তাব", "prostab", "proposal", "noun"),
               V("গৃহীত", "grihito", "adopted, accepted", "adjective")],
              G("Meeting moves",
                "shurute… · alochonar bishôy… · siddhante pôuchhano · siddhanto grihito hôlo",
                "আলোচনার বিষয় তিনটি। প্রথমে খরচ, তারপর সময়, শেষে দায়িত্ব। সিদ্ধান্তে পৌঁছেছি কি?"
                " — Asking whether the room has arrived is a legitimate closing move.",
                [X("আলোচনার বিষয় খরচ আর সময়।", "alochonar bishôy khôroch ar shomoy.", "The matters for discussion are cost and time."),
                 X("আমরা কি সিদ্ধান্তে পৌঁছেছি?", "amra ki siddhante pôuchhechhi?", "Have we reached a decision?"),
                 X("প্রস্তাবটি সংখ্যাগরিষ্ঠ ভোটে গৃহীত হয়েছে।", "prostabṭi shôngkha-gôrishṭho bhoṭe grihito hoyechhe.", "The proposal has been adopted by majority vote.")],
                [("সিদ্ধান্ত হয়েছে কি না হয়েছে।", "আমরা কি সিদ্ধান্তে পৌঁছেছি?", "The closing move is a question, not a tautology."),
                 ("আলোচনার বিষয় আলোচনা।", "আলোচনার বিষয় খরচ।", "বিষয় needs a content word after it.")]),
              [D("সভাপতি", "আজকের আলোচনার বিষয় দুটো।", "ajker alochonar bishôy duṭo.", "Today's discussion has two matters."),
               D("রাতুল", "প্রথমে খরচ ধরি, তারপর সময়।", "prothome khôroch dhôri, tarpor shomoy.", "Let me take cost first, then time."),
               D("সুমি", "আমি একমত, তবে সময় নিয়ে আলাদা মত আছে।", "ami ekmôt, tôbe shomoy niye alada môt achhe.", "I agree, though there is a different view on time."),
               D("সভাপতি", "ঠিক আছে, শেষে ভোট নেব।", "ṭhik achhe, sheshe bhoṭ nebo.", "All right — we'll vote at the end.")],
              WS("Meeting worksheet", [
                  T("Open the meeting.", ["two points", "the matter is the budget", "let's start"],
                    ["আলোচনার বিষয় দুটো", "বিষয় বাজেট", "শুরু করা যাক"]),
                  T("Close it down.", ["have we decided?", "the proposal is adopted", "one vote"],
                    ["সিদ্ধান্তে পৌঁছেছি?", "প্রস্তাবটি গৃহীত হয়েছে", "একটি ভোট নিই"]),
              ])),
            L("Qualifying a claim in a meeting",
              "matters: ব্যতিক্রম ছাড়া (without exception), শর্তসাপেক্ষে (conditionally), "
              "সম্ভাবনার কথা মাথায় রেখে (keeping possibilities in mind). Bengali professional speech "
              "qualifies with টা and একটি, and it keeps the subject after the qualifier.",
              [V("শর্ত", "shôrto", "condition", "noun"),
               V("ব্যতিক্রম", "bêttikrom", "exception", "noun"),
               V("সম্ভাবনা", "shombhabona", "possibility", "noun"),
               V("সীমাবদ্ধতা", "shimabôddhota", "limitation", "noun"),
               V("তবুও", "tôbuo", "even so", "conjunction")],
              G("Qualified commitment",
                "shôrto soho · bêttikrom chhaṛa · shombhabona roye achhe",
                "আমরা শর্তসাপেক্ষে রাজি — বাজেট পাস হলে। ব্যতিক্রম ছাড়া সব খাতে কাটছাঁট সম্ভব নয়. "
                "The qualification goes before the verb, and the condition after the dash.",
                [X("আমরা শর্তসাপেক্ষে প্রস্তাবটি মানি।", "amra shôrtoshapekkhe prostabṭi mani.", "We accept the proposal conditionally."),
                 X("সম্ভাবনা রয়েছে, প্রতিশ্রুতি নয়।", "shombhabona roye achhe, protishruti nôy.", "There is a possibility, not a promise."),
                 X("তবুও একটা সীমাবদ্ধতা জানানো দরকার।", "tôbuo ekṭa shimabôddhota janano dôrkar.", "Even so, one limitation needs to be stated.")],
                [("আমরা রাজি, তবে রাজি নই।", "আমরা শর্তসাপেক্ষে রাজি।", "State the condition instead of doubling the verb."),
                 ("সম্ভাবনা আছে, হবে।", "সম্ভাবনার কথা আছে, নিশ্চিত নয়।", "Keep possibility and certainty apart.")]),
              [D("সুমি", "আপনি রাজি তো?", "apni raji to?", "So you agree?"),
               D("রাতুল", "শর্তসাপেক্ষে রাজি — বাজেট পাস হলে।", "shôrtoshapekkhe raji — bajeṭ pas hole.", "Conditionally — if the budget passes."),
               D("সুমি", "সম্ভাবনা কতটা?", "shombhabona kôtoṭa?", "How likely is that?"),
               D("রাতুল", "সম্ভাবনা আছে, তবে প্রতিশ্রুতি দেব না।", "shombhabona achhe, tôbe protishruti debo na.", "There is a possibility, but I won't promise.")],
              WS("Qualification worksheet", [
                  T("Qualify the commitment.", ["we will finish (if the data arrives)", "we agree (conditionally)"],
                    ["ডেটা এলে শেষ করব", "শর্তসাপেক্ষে রাজি"]),
                  T("Separate possibility from promise.", ["it may work", "it will happen"],
                    ["সম্ভাবনা আছে", "নিশ্চিত নয়, চেষ্টা করব"]),
              ])),
            L("Reporting what someone said",
              "Reported speech shifts the verb and the pronoun: তিনি বললেন যে তিনি আসবেন (he said he "
              "would come). Bengali rarely backshifts tense, but it does switch আপনি/তিনি to match the "
              "report.",
              [V("বললেন", "bollen", "he/she said (respectful)", "verb"),
               V("জানালেন", "janalen", "he/she informed", "verb"),
               V("অনুযায়ী", "onujayī", "according to", "postposition"),
               V("জোর", "jor", "emphasis", "noun"),
               V("উল্লেখ", "ullekh", "mention", "noun")],
              G("Reported speech",
                "tini bollen je … · … er kôtha ullekh kôrlen",
                "তিনি বললেন যে নীতিটি বদলাবে না. রাতুল বলল যে সে রাজি. Note that quotation marks "
                "usually disappear and যে carries the quotation.",
                [X("সুমি বলল যে সে কাল আসবে।", "Sumi bollo je she kal ashbe.", "Sumi said she would come tomorrow."),
                 X("সভাপতি জানালেন যে সময় বাড়ানো হবে না।", "shôbhapoti janalen je shomoy bôrano hobe na.", "The chair informed us that the deadline will not be extended."),
                 X("দলনেতা জোর দিয়ে বললেন, «আপস নয়»।", "dôl-neta jor diye bollen, «aposh nôy».", "The group leader said with emphasis, 'no compromise.'")],
                [("সুমি বলল যে আমি কাল আসব।", "সুমি বলল যে সে কাল আসবে।", "The report needs সে, not আমি."),
                 ("তিনি বললেন, সে আসবে।", "তিনি বললেন যে তিনি আসবেন।", "Keep the register: তিਨি takes আসবেন.")]),
              [D("মিতা", "কর্তা কী বললেন?", "kôrta ki bollen?", "What did the boss say?"),
               D("রাতুল", "তিনি বললেন যে নিয়ম বদলাবে না, তবে সময় নিয়ে ভাববেন।", "tini bollen je niyom bôdlabe na, tôbe shomoy niye bhabben.", "He said the rule will not change, but he will think about the time."),
               D("মিতা", "আপনি কী উত্তর দিলেন?", "apni ki uttôr dilen?", "What did you answer?"),
               D("রাতুল", "আমি বললাম যে আমরা শর্তসাপেক্ষে রাজি।", "ami bollam je amra shôrtoshapekkhe raji.", "I said that we agree conditionally.")],
              WS("Report worksheet", [
                  T("Report the sentence.", ["'I will call tomorrow' (she)", "'no compromise' (the leader)"],
                    ["সে বলল যে সে কাল ফোন করবে", "দলনেতা বললেন, আপস নয়"]),
                  T("Report respectfully.", ["the chair said the deadline stands", "he informed us about the budget"],
                    ["সভাপতি জানালেন যে সময়সীমা বহাল", "তিনি বাজেটের কথা জানালেন"]),
              ])),
        ]},
        {"id": "B2+-U2", "title": "Writing that works", "lessons": [
            L("A message that gets an answer",
              "Professional Bengali messages are short and three-part: ভূমিকা (context), অনুরোধ "
              "(request), ধন্যবাদ (thanks). The honorific আপনি and the polite imperative stay "
              "throughout, even when the writer is senior.",
              [V("অনুরোধ", "onurodh", "request", "noun"),
               V("বার্তা", "barta", "message", "noun"),
               V("সূত্র", "shutro", "source, reference", "noun"),
               V("প্রসঙ্গে", "proshôngge", "regarding", "postposition"),
               V("ধন্যবাদান্তে", "dhonnobadante", "with thanks (letter close)", "adverb")],
              G("Message frame",
                "proshôngge… → onurodh je… → dhonnobad",
                "বাজেট প্রসঙ্গে: আগামী মাসের সংখ্যা দরকার। অনুগ্রহ করে জানালে ভালো হয়। ধন্যবাদ। The "
                "request is nominal (জানালে ভালো হয়) rather than imperative — that is the register.",
                [X("বাজেট প্রসঙ্গে একটা অনুরোধ আছে।", "bajeṭ proshôngge ekṭa onurodh achhe.", "Regarding the budget, I have a request."),
                 X("আগামী সোমবারের মধ্যে জানালে ভালো হয়।", "ôgamī shombarer moddhe janale bhalo hôy.", "It would be good if you could inform by next Monday."),
                 X("সহযোগিতার জন্য ধন্যবাদ।", "shôhôjogitar jônno dhonnobad.", "Thank you for your cooperation.")],
                [("তুমি কাল জানাও।", "জানালে ভালো হয়।", "A message to a colleague keeps the polite register."),
                 ("ধন্যবাদ, দরকার নেই আর।", "সহযোগিতার জন্য ধন্যবাদ।", "The close is for the help already given, not for the help you hope for.")]),
              [D("মিতা", "বার্তাটা কেমন?", "bartaṭa kemon?", "How is the message?"),
               D("রাতুল", "তিনটা ভাগে ভাগ কর — প্রসঙ্গ, অনুরোধ, ধন্যবাদ।", "tinṭa bhage bhag kôro — proshônggo, onurodh, dhonnobad.", "Split it into three parts — context, request, thanks."),
               D("মিতা", "এবং «জানাও» বদলে?", "ebong «janao» bôdle?", "And instead of 'tell me'?"),
               D("রাতুল", "«জানালে ভালো হয়» — ভদ্র, কিন্তু স্পষ্ট।", "«janale bhalo hôy» — bhôdro, kintu shpôshṭo.", "'It would be good if you informed me' — polite, but clear.")],
              WS("Message worksheet", [
                  T("Build the three parts.", ["context: the report", "request: by Friday", "close"],
                    ["রিপোর্ট প্রসঙ্গে", "শুক্রবারের মধ্যে জানালে ভালো হয়", "ধন্যবাদ"]),
                  T("Ask a favour politely.", ["send the file", "call in the morning"],
                    ["ফাইলটা পাঠালে ভালো হয়", "সকালে ফোন করলে সুবিধা হয়"]),
              ])),
            L("The summary: তিন লাইনে",
              "A summary in Bengali states the decision first, then the reason, then the next step: "
              "সিদ্ধান্ত হিসেবে…, কারণ…, পরবর্তী পদক্ষেপ…. Three lines, no adjectives.",
              [V("সারসংক্ষেপ", "sharshôngkkhep", "summary", "noun"),
               V("পরবর্তী", "pôrobortī", "next, subsequent", "adjective"),
               V("পদক্ষেপ", "pôdokkhep", "step, measure", "noun"),
               V("কারণ", "karôn", "reason, cause", "noun"),
               V("ফলাফল", "pholafol", "result", "noun")],
              G("Decision → reason → next step",
                "siddhanto hôlo je… · karôn … · pôrobortī pôdokkhep …",
                "সিদ্ধান্ত: সময়সীমা দুই সপ্তাহ বাড়ানো হবে। কারণ: দুই দলের তথ্য দরকার। পরবর্তী "
                "পদক্ষেপ: সোমবার নতুন সময় জমা। Nothing else belongs in a summary.",
                [X("সারসংক্ষেপে: সময়সীমা দুই সপ্তাহ বাড়ল।", "sharshôngkkhepe: shomoy-shima dui shoptah baṛlo.", "In summary: the deadline moved by two weeks."),
                 X("কারণটা স্পষ্ট — তথ্য এখনো আসেনি।", "karônṭa shpôshṭo — tôthỹo ekhono asheni.", "The reason is clear — the data has not arrived."),
                 X("পরবর্তী পদক্ষেপ আগামী সোমবার।", "pôrobortī pôdokkhep ôgamī shombar.", "The next step is next Monday.")],
                [("সারসংক্ষেপ অনেক লম্বা, তবে ছোট।", "সারসংক্ষেপ তিন লাইন।", "A summary that is long is not a summary."),
                 ("কারণ আর ফলাফল একই।", "কারণ: … · ফলাফল: …", "Reason and result are different slots; keep them apart.")]),
              [D("প্রধান", "সারসংক্ষেপ পড়ুন।", "sharshôngkkhep pôṛun.", "Read the summary."),
               D("রাতুল", "সিদ্ধান্ত: ডিজাইন অনুমোদিত। কারণ: ব্যবহারকারী পরীক্ষা ভালো। পরবর্তী পদক্ষেপ: সোমবার থেকে কাজ।", "siddhanto: dijain onumodito. karôn: bêboharkarī porikkha bhalo. pôrobortī pôdokkhep: shombar theke kaj.", "Decision: the design is approved. Reason: user testing went well. Next step: work from Monday."),
               D("প্রধান", "ভালো — তিন লাইনেই সব।", "bhalo — tin lainei shôb.", "Good — everything in three lines."),
               D("রাতুল", "আর কাউকে কিছু বলার দরকার নেই?", "ar kauকে kichhu bolar dôrkar nei?", "Does anyone else need to be told?")],
              WS("Summary worksheet", [
                  T("Summarize in three lines.", ["the decision", "the reason", "the next step"],
                    ["সিদ্ধান্ত: সময়সীমা বাড়ল", "কারণ: তথ্য আসেনি", "পরবর্তী পদক্ষেপ: সোমবার নতুন তারিখ"]),
                  T("Cut the filler.", ["a long polite paragraph with one decision"],
                    ["সিদ্ধান্ত একটাই — বাকিটা বাদ"]),
              ])),
            L("Notes into minutes",
              "Minutes in Bengali are terse, passive where the actor is unknown, and dated: উপস্থিত "
              "(present), সিদ্ধান্ত (decision), দায়িত্বপ্রাপ্ত (assigned), পরবর্তী সভা (next "
              "meeting). Learn four headings and any meeting can be written up.",
              [V("উপস্থিত", "uposthito", "present, attending", "adjective"),
               V("দায়িত্ব", "dayitto", "responsibility", "noun"),
               V("নোট", "noṭ", "note", "noun"),
               V("সভা", "shôbha", "meeting", "noun"),
               V("সংশোধন", "shôngshodhon", "correction", "noun")],
              G("Minutes headings",
                "tarikh · uposthiti · siddhanto · dayitto · pôrobortī shôbha",
                "তারিখ: ১২ অক্টোবর। উপস্থিত: আট জন। সিদ্ধান্ত: দুই সপ্তাহ সময় বাড়ানো। দায়িত্ব: "
                "সুমি। পরবর্তী সভা: সোমবার। Headings make the page usable a month later.",
                [X("উপস্থিত ছিলেন আট জন সদস্য।", "uposthito chhilen aṭ jon shôdoshsho.", "Eight members were present."),
                 X("সিদ্ধান্তটি সুমিকে দায়িত্ব দেওয়া হয়েছে।", "siddhantoṭi Sumike dayitto deoa hoyechhe.", "The decision has been assigned to Sumi."),
                 X("পরের সভার তারিখ পরে জানানো হবে।", "porer shôbhar tarikh pôre janano hobe.", "The date of the next meeting will be announced later.")],
                [("উপস্থিত ছিল ভালো।", "উপস্থিত: আট জন।", "Minutes take headings, not evaluations."),
                 ("সিদ্ধান্ত হয়তো হয়েছে।", "সিদ্ধান্ত: সময় বাড়ানো হয়েছে।", "A minute records what was decided, not what might have been.")]),
              [D("মিতা", "সভার নোট লিখবে কে?", "shôbhar noṭ likhbe ke?", "Who will write the meeting note?"),
               D("রাতুল", "আমি লিখি: তারিখ, উপস্থিত, সিদ্ধান্ত, দায়িত্ব।", "ami likhi: tarikh, uposthito, siddhanto, dayitto.", "I'll write it: date, attendance, decision, responsibility."),
               D("মিতা", "সময়ের কথা মনে রাখো।", "shomoyer kôtha mone rakhо.", "Remember the timing."),
               D("রাতুল", "হ্যাঁ — পরবর্তী সভা সোমবার, বিকেল পাঁচটা।", "hã — pôrobortī shôbha shombar, bikel pãchṭa.", "Yes — next meeting Monday, five in the afternoon.")],
              WS("Minutes worksheet", [
                  T("Write the headings.", ["who was present", "what was decided", "whose duty", "next meeting"],
                    ["উপস্থিত: আট জন", "সিদ্ধান্ত: সময় বাড়ানো", "দায়িত্ব: সুমি", "পরবর্তী সভা: সোমবার"]),
                  T("Correct a vague note.", ["it was maybe decided"],
                    ["সিদ্ধান্ত: সময় দুই সপ্তাহ বাড়ানো হয়েছে"]),
              ])),
        ]},
        {"id": "B2+-U3", "title": "Negotiating a deadline", "lessons": [
            L("Bearing bad news early",
              "Bengali professional culture prefers early warning over late surprise: আগেই জানানো "
              "(informing beforehand), দেরি হলে জানাব (I'll tell you if it is late), এখনই বলা ভালো "
              "(better to say it now).",
              [V("আগেই", "agei", "beforehand, already", "adverb"),
               V("দেরি", "deri", "delay", "noun"),
               V("ঝুঁকি", "jhũki", "risk", "noun"),
               V("সতর্ক", "shotôrko", "cautious", "adjective"),
               V("সম্ভাব্য", "shombhabbo", "probable", "adjective")],
              G("Early-warning frames",
                "agei janachhi je… · deri hote pare · jhũki achhe",
                "আগেই জানাচ্ছি যে দুই দিন দেরি হতে পারে। এখনই বলা ভালো, পরে অসুবিধা হবে। The "
                "warning is a first-person statement of fact, not an apology.",
                [X("আগেই জানাচ্ছি, একটু দেরি হতে পারে।", "agei janachchhi, ekṭu deri hote pare.", "I am telling you in advance: there may be a little delay."),
                 X("এখনই বলা ভালো — ঝুঁকিটা ছোট নয়।", "ekhoni bôla bhalo — jhũkiṭa chhoṭ nôy.", "Better to say it now — the risk is not small."),
                 X("একদিনের বেশি দেরি হলে জানাব।", "ekdiner beshi deri hole janabo.", "If the delay is more than a day, I'll tell you.")],
                [("শেষ দিনে বলব যে দেরি হয়েছে।", "আগেই জানাই, দেরি হতে পারে।", "Late news is the costliest professional mistake in Bengali offices."),
                 ("কোনো সমস্যা নেই, তবে সব শেষ।", "ঝুঁকি আছে, তবে সামলানো যাবে।", "Warnings carry the limit of the risk.")]),
              [D("প্রধান", "কাজ কত দূর?", "kaj kôto dur?", "How far along is the work?"),
               D("রাতুল", "সত্যি বলতে, দুই দিন দেরি হতে পারে — আগেই জানাচ্ছি।", "shôtti bolte, dui din deri hote pare — agei janachchhi.", "Honestly, there may be a two-day delay — I'm telling you in advance."),
               D("প্রধান", "কারণ কী?", "karôn ki?", "What is the reason?"),
               D("রাতুল", "বাইরের তথ্য আসতে দেরি হচ্ছে, ঝুঁকিটা আমাদের নয়।", "bairer tôthỹo ashte deri hôchhe, jhũkiṭa amader nôy.", "The outside data is late; the risk is not ours.")],
              WS("Warning worksheet", [
                  T("Give early warning.", ["two days late", "the data has not arrived", "the risk is small"],
                    ["দুই দিন দেরি হতে পারে", "তথ্য এখনো আসেনি", "ঝুঁকি কম"]),
                  T("Say when you will report again.", ["if it is more than one day"],
                    ["একদিনের বেশি হলে জানাব"]),
              ])),
            L("Asking for more time, with a plan",
              "Asking for time works when the request arrives with its plan: দুই দিন সময় দিলে, "
              "শেষ করে দেব (if you give two days, I'll finish), বিকল্প হিসেবে (as an "
              "alternative) — Bengali negotiates the whole package, not the number.",
              [V("সময় দেওয়া", "shomoy deoa", "to give time", "phrase"),
               V("বিকল্প", "bikolpo", "alternative", "noun"),
               V("গ্যারান্টি", "gyaranṭi", "guarantee", "noun"),
               V("কাটছাঁট", "kaṭchãṭ", "cutting down, trimming", "noun"),
               V("অংশ", "ôngsho", "part, portion", "noun")],
              G("Request + plan",
                "… din shomoy dile … kôre debo · bikolpo hishebe…",
                "দুই দিন সময় দিলে পুরোটা শেষ করব; না হলে অর্ধেক কালই দিতে পারি। বিকল্পটা নিজেই "
                "দিন — প্রশ্নটা প্রশ্ন না হয়ে প্রস্তাব হয়।",
                [X("তিন দিন সময় দিলে সবটা ঠিক করা যাবে।", "tin din shomoy dile shôbṭa ṭhik kôra jabe.", "If you give three days, all of it can be fixed."),
                 X("বিকল্প হিসেবে একটা অংশ আজই দিই।", "bikolpo hishebe ekṭa ôngsho ajei dii.", "As an alternative, I can give one section today."),
                 X("সময়ের গ্যারান্টি দিতে পারছি না, চেষ্টার গ্যারান্টি দিতে পারি।", "shomoyer gyaranṭi dite parchhi na, cheshṭar gyaranṭi dite pari.", "I cannot guarantee the time; I can guarantee the effort.")],
                [("আরও সময় দিন, নইলে পারব না।", "দুই দিন সময় দিলে শেষ করে দেব।", "The bare demand has no plan attached."),
                 ("সব পারব না, কিছু পারব না।", "অর্ধেক আজ, বাকিটা দুই দিনে।", "Alternatives must have quantities.")]),
              [D("সুমি", "কাল সকালে দরকার।", "kal shokale dôrkar.", "I need it tomorrow morning."),
               D("রাতুল", "শেষটা দিতে দুই দিন লাগবে; তবে সবটা আজ রাতেই পারে না।", "sheshṭa dite dui din lagbe; tôbe shôbṭa aj ratei pare na.", "The ending needs two days; but not all of it can be done tonight."),
               D("সুমি", "তাহলে কী দিতে পারবেন?", "tahole ki dite parben?", "Then what can you give?"),
               D("রাতুল", "বিকল্প: ভূমিকা আর প্রথম অংশ কাল, বাকিটা দুই দিনে।", "bikolpo: bhumika ar prothom ôngsho kal, bakiṭa dui dine.", "Alternative: the introduction and first section tomorrow, the rest in two days.")],
              WS("Negotiation worksheet", [
                  T("Ask for time with a plan.", ["three days → all of it", "two days → the whole ending"],
                    ["তিন দিন সময় দিলে সবটা", "দুই দিনে শেষটা করে দেব"]),
                  T("Offer an alternative.", ["half today", "the first section tonight"],
                    ["বিকল্প হিসেবে অর্ধেক আজ", "প্রথম অংশ আজ রাতেই"]),
              ])),
            L("Closing the loop",
              "The last professional move is the loop: কাজটা শেষ, সমর্থন, পরবর্তী ধাপ নিশ্চিত. Bengali "
              "closings thank, confirm and hand over in three short sentences — nothing more.",
              [V("সম্পন্ন", "shômpônno", "completed", "adjective"),
               V("নিশ্চিত", "nishchito", "confirmed, certain", "adjective"),
               V("হস্তান্তর", "hôstantor", "handover", "noun"),
               V("সমর্থন", "shômôrton", "support", "noun"),
               V("পর্যালোচনা", "pôryalochona", "review", "noun")],
              G("Closing frames",
                "kajṭa shômpônno · nishchito kôrchhi je… · kono shômôrton dôrkar?",
                "কাজটা সম্পন্ন। সময়মতোই শেষ হয়েছে। আর কিছু দরকার হলে জানাবেন — ধন্যবাদ। The closing "
                "offers help and stops; it does not add a new request.",
                [X("কাজটা সম্পন্ন, সময়মতো শেষ হয়েছে।", "kajṭa shômpônno, shomoymôtoi shesh hoyechhe.", "The work is complete, finished on time."),
                 X("নিশ্চিত করছি যে ফাইল পাঠানো হয়েছে।", "nishchito kôrchhi je fail pathano hoyechhe.", "I confirm the file has been sent."),
                 X("পরবর্তী পর্যালোচনা সোমবার।", "pôrobortī pôryalochona shombar.", "The next review is Monday.")],
                [("কাজ শেষ, আর একটা নতুন কাজ দিন।", "কাজ শেষ — নতুন কাজ এলে জানাবেন।", "A close offers help; it does not open a queue."),
                 ("সম্পন্ন প্রায়।", "সম্পন্ন।", "Closings are definite; প্রায় belongs in the risk line instead.")]),
              [D("রাতুল", "কাজটা সম্পন্ন, ফাইল পাঠানো হয়েছে।", "kajṭa shômpônno, fail pathano hoyechhe.", "The work is complete; the file has been sent."),
               D("সুমি", "ধন্যবাদ — পর্যালোচনা কবে?", "dhonnobad — pôryalochona kôbe?", "Thanks — when is the review?"),
               D("রাতুল", "সোমবার, এবং আমি হাতে থাকব।", "shombar, ebong ami hate thakbo.", "Monday, and I will be available."),
               D("সুমি", "বেশ! আর কিছু লাগলে জানাব।", "besh! ar kichhu lagle janabo.", "Great. I'll tell you if anything else is needed.")],
              WS("Closing worksheet", [
                  T("Close the loop.", ["it is done", "the file is sent", "the next review is Monday"],
                    ["কাজটা সম্পন্ন", "ফাইল পাঠানো হয়েছে", "পরবর্তী পর্যালোচনা সোমবার"]),
                  T("Offer help and stop.", ["if anything is needed"],
                    ["আর কিছু দরকার হলে জানাবেন"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Bengali offices run on the meeting minute and the early phone call. Bad news is "
                 "expected to travel first and fast: a two-day delay reported on day one is ordinary "
                 "management; the same delay discovered on the deadline is a character problem. "
                 "Colleagues also expect a personal follow-up at the end of a project — a call, not "
                 "an email — which is why the closing lesson is about handing over rather than "
                 "closing off."),
        source_url="https://en.wikipedia.org/wiki/Bengali_literature",
        reading=("আজ সভার শেষে রাতুল বলল, «দুই দিন দেরি হতে পারে।» সভাপতি বিরক্ত হননি, বরং আগেই "
                 "জানানোর জন্য ধন্যবাদ দিলেন। বিকল্প হিসেবে রাতুল প্রথম অংশ আজই দেওয়ার প্রস্তাব "
                 "করল। সিদ্ধান্ত হলো: প্রথম অংশ কাল সকালে, বাকিটা দুই দিনে। আমি শিখলাম যে "
                 "আগেভাগে বলা মানে সাহস, দেরিতে বলা মানে সমস্যা।"),
        reading_gloss=("At the end of today's meeting Rätul said, 'There may be a two-day delay.' The "
                       "chair was not annoyed; instead he thanked him for telling us in advance. As an "
                       "alternative Rätul proposed giving the first section today itself. The decision "
                       "was: first section tomorrow morning, the rest in two days. I learned that "
                       "speaking up early is courage; speaking late is trouble."),
        listening=("সুমি: সভার সারসংক্ষেপ পাঠালেন?<br>রাতুল: হ্যাঁ, তিন লাইন — সিদ্ধান্ত, কারণ, পরবর্তী পদক্ষেপ।<br>"
                   "সুমি: আর সময়সীমা?<br>রাতুল: আগেই জানিয়েছি, দুই দিন বাড়ল।"),
        listening_gloss=("Sumi: Did you send the meeting summary? Rätul: Yes, three lines — decision, "
                         "reason, next step. Sumi: And the deadline? Rätul: I told them in advance — "
                         "it moved by two days."),
        voice_tag=VOICE,
        idioms=[
            ("কথা অনুযায়ী", "according to the word", "as agreed"),
            ("সময়ের হাত", "the hand of time", "the pressure of time"),
            ("মাথা ঠান্ডা", "a cool head", "calm under pressure"),
            ("সোজা কথা", "straight words", "plain speaking"),
            ("কাজের চাপ", "work pressure", "heavy workload"),
            ("দায়িত্ব নেওয়া", "to take responsibility", "to own a task"),
            ("জবাবদিহি", "accountability", "answerability"),
            ("সুসময়", "good time", "the right moment"),
            ("অপেক্ষা করা", "to wait", "to wait for something"),
            ("হাতে থাকা", "to stay at hand", "to remain available"),
        ],
        mistakes=[
            ("শেষ দিনে জানাব যে দেরি হয়েছে।", "আগেই জানাব যে দেরি হতে পারে।", "Early warning is the professional norm; late news is the failure."),
            ("আরও সময় দিন, নইলে পারব না।", "দুই দিন সময় দিলে শেষ করে দেব।", "A request for time travels with a plan."),
            ("সিদ্ধান্ত হয়তো হয়েছে।", "সিদ্ধান্ত: সময় বাড়ানো হয়েছে।", "Minutes record decisions, not possibilities."),
        ],
        task_title="Run one meeting in Bengali",
        task_instructions=("Take a real meeting — three people, twenty minutes — and run it entirely in "
                           "Bengali: open with the matters, qualify one claim, report one thing someone "
                           "said, close with the decision. Then write the minutes with four headings "
                           "and send a three-line summary. If the room switched to English, note which "
                           "move it was — that is the lesson to prepare next."),
    ),
    "test": [
        ("translate_en", "Say: We agree conditionally, if the budget passes.", "আমরা শর্তসাপেক্ষে রাজি, বাজেট পাস হলে।"),
        ("translate_ar", "সিদ্ধান্ত: সময় দুই দিন বাড়ল; কারণ: তথ্য আসেনি।", "Decision: the deadline moved by two days; reason: the data has not arrived."),
        ("multiple_choice", "Which line sounds like early warning?", "আগেই জানাচ্ছি, দেরি হতে পারে।"),
        ("fill_in_the_blank", "শর্তসাপেক্ষে রাজি ___ বাজেট পাস হলে। (conjunction)", "— / tôbe"),
        ("word_selection", "Select the Bengali for 'alternative'.", "বিকল্প"),
        ("error_correction", "সুমি বলল যে আমি কাল আসব।", "সুমি বলল যে সে কাল আসবে।"),
        ("dialogue_completion", "Complete: দুই দিন সময় দিলে ___ (I'll finish it)", "শেষ করে দেব"),
        ("matching", "Match হস্তান্তর to its meaning.", "handover"),
        ("reading_comprehension", "সভাপতি বিরক্ত হলেন না কেন?", "কারণ রাতুল আগেই জানিয়েছিল"),
        ("inference", "«আগেভাগে বলা মানে সাহস» — what is the writer saying?", "reporting problems early takes courage"),
        ("main_idea", "বিকল্প হিসেবে প্রথম অংশ আজই। What is happening?", "a partial delivery is proposed"),
        ("detail_identification", "পরবর্তী পর্যালোচনা কবে?", "সোমবার"),
    ],
}

HALFSTEPS["C1+"] = {
    "title": "Bengali C1+ — Almost native",
    "native": NATIVE,
    "goals": [
        "Use and recognise idioms, proverbs and images at the right moment",
        "Move between formal and intimate registers inside one text",
        "Revise a paragraph for rhythm, precision and length",
    ],
    "units": [
        {"id": "C1+-U1", "title": "Idiom, proverb, image", "lessons": [
            L("Idioms that carry judgement",
              "Bengali idioms judge without a verdict: চোখ কপালে ওঠা (astonishment), মাথায় হাত "
              "(dismay), হাতযশ (skill), কান পাতলা (easily influenced). One idiom replaces a "
              "paragraph of evaluation.",
              [V("চোখ কপালে ওঠা", "chokh kôpale ôṭha", "to be astonished", "idiom"),
               V("মাথায় হাত", "mathay hat", "dismay, shock", "idiom"),
               V("হাতযশ", "hatjôsh", "deftness, skill", "idiom"),
               V("কান পাতলা", "kan patla", "easily swayed", "idiom"),
               V("লেজ গুটানো", "lej guṭano", "to back down humiliated", "idiom")],
              G("Idioms sit where an evaluator would sit",
                "subject + idiom + hôlo / achhe / kôrlo",
                "খবর শুনে সবার চোখ কপালে উঠল. ওর হাতযশ আছে, তাই কাজটা ওকে দাও. The idiom takes "
                "the place of a sentence about reaction or quality — and it takes the past tense when "
                "the reaction happened.",
                [X("তার হাতযশ আছে, কাজটা ভালো হবে।", "tar hatjôsh achhe, kajṭa bhalo hobe.", "He has a deft hand; the work will be good."),
                 X("ঘোষণা শুনে সবার মাথায় হাত।", "ghoshôna shune shôbar mathay hat.", "Hearing the announcement, everyone was in dismay."),
                 X("চাপে পড়ে Opposition-কে লেজ গুটাতে হলো।", "chape pôṛe Opposition-ke lej guṭate hôlo.", "Under pressure the opposition had to back down.")],
                [("তার অনেক হাতযশ, কিন্তু হাত নেই।", "তার হাতযশ আছে।", "An idiom is one unit; splitting it destroys the image."),
                 ("চোখ কপালে উঠল, মানে চোখ ব্যথা।", "চোখ কপালে উঠল, মানে বিস্ময়।", "The idiom means astonishment, not the literal image.")]),
              [D("সুমি", "খবরটা শুনেছ?", "khôbôrṭa shunechho?", "Have you heard the news?"),
               D("রাতুল", "হ্যাঁ, শুনে তো চোখ কপালে উঠে গেল।", "hã, shune to chokh kôpale uṭhe gelo.", "Yes — hearing it, my eyes went up to my forehead."),
               D("সুমি", "আর কে কী বলছে?", "ar ke ki bolchhe?", "And what are people saying?"),
               D("রাতুল", "অনেকে লেজ গুটিয়েছে, আর যাদের হাতযশ আছে তারা কাজে নেমেছে।", "ônekе lej guṭiyechhe, ar jader hatjôsh achhe tara kaje nemechhe.", "Many have backed down; those with deft hands have gone to work.")],
              WS("Idiom worksheet", [
                  T("Choose the right idiom.", ["astonishment", "dismay", "skill", "easily swayed"],
                    ["চোখ কপালে ওঠা", "মাথায় হাত", "হাতযশ", "কান পাতলা"]),
                  T("Use it in a sentence.", ["the news astonished everyone", "he is easily swayed"],
                    ["খবরে সবার চোখ কপালে উঠল", "লোকটার কান পাতলা"]),
              ])),
            L("Proverbs as arguments",
              "Proverbs are arguments in Bengali too: যেমন গাছ তেমন ফল (like tree, like fruit), "
              "অতিদর্পে হত লঙ্কা (pride goes before a fall), এক মাঘে শীত যায় না (one cold month does "
              "not end winter — one swallow does not make a summer).",
              [V("গাছ", "gach", "tree", "noun"),
               V("ফল", "phôl", "fruit, result/outcome", "noun"),
               V("অতিদর্প", "ôtidôrpo", "excessive pride", "noun"),
               V("শীত", "shit", "cold, winter", "noun"),
               V("উপমা নয়, প্রমাণ নয়", "upoma nôy, proman nôy", "not a simile, not a proof", "phrase")],
              G("Proverb + frame",
                "proverb + mane… · proverbb uses eka tôthyo to end an argument",
                "«যেমন গাছ তেমন ফল» — প্রতিষ্ঠানের নেতৃত্ব দেখেই বোঝা যায়। «এক মাঘে শীত যায় "
                "না» — এক মাসের তথ্যে সিদ্ধান্ত নেওয়া যায় না।",
                [X("যেমন গাছ, তেমন ফল — দলটার অবস্থাও তাই।", "jekôm gach, tekmôn phôl — dôlṭar ôbosthao tai.", "Like tree, like fruit — so too the party's state."),
                 X("এক মাঘে শীত যায় না, তাই অপেক্ষা করা ভালো।", "ek maghe shit jay na, tai ôpekkha kôra bhalo.", "One cold month does not end the winter — so it is better to wait."),
                 X("অতিদর্পে হত লঙ্কা — সেটাই এখন দেখা যাচ্ছে।", "ôtidôrpe hôto lôngka — sheṭai ekhon dekha jachchhe.", "Pride goes before a fall — and that is what we now see.")],
                [("প্রবাদ, তাই প্রমাণ।", "প্রবাদ — উপমা, প্রমাণ নয়।", "A proverb argues by analogy; it does not prove a case."),
                 ("এক মাঘে শীত যায় না, অতএব আজও শীত।", "এক মাঘে শীত যায় না — তাই তথ্যের জন্য অপেক্ষা করি।", "The proverb should lead to a method, not to a slogan.")]),
              [D("মিতা", "আপনি সিদ্ধান্ত নিলেন?", "apni siddhanto nilen?", "Have you decided?"),
               D("রাতুল", "এক মাসের খবরে সিদ্ধান্ত নিচ্ছি না — এক মাঘে শীত যায় না।", "ek masher khôbôre siddhanto nichchhi na — ek maghe shit jay na.", "I'm not deciding on one month's news — one cold month does not end winter."),
               D("মিতা", "তাহলে কত দিন?", "tahole kôto din?", "Then how many days?"),
               D("রাতুল", "তিন মাস, নইলে যেমন গাছ তেমন ফলের ফাঁদে পড়ব।", "tin mash, noile jekôm gach tekmôn phôler phãde pôṛbo.", "Three months, or I'll fall into the like-tree-like-fruit trap.")],
              WS("Proverb worksheet", [
                  T("Use the proverb that fits.", ["one good month does not prove the plan", "a bad team comes from bad leadership"],
                    ["এক মাঘে শীত যায় না", "যেমন গাছ তেমন ফল"]),
                  T("Add the method.", ["wait for more data", "check the leadership"],
                    ["তিন মাসের তথ্য দেখি", "নেতৃত্বটা দেখি"]),
              ])),
            L("Metaphors that are alive in Bengali",
              "Some images are still alive and usable: নদী (river — flow, change), মাছ (fish — livelihood), "
              "গাছ (tree — growth, patience), আলো-আঁধারি (light and shadow — mixed fortune), "
              "পদ্ম (lotus — purity out of mud).",
              [V("নদী", "nodi", "river", "noun"),
               V("মাছ", "machh", "fish", "noun"),
               V("আলো-আঁধারি", "alo-ãdhari", "light and shadow", "noun"),
               V("পদ্ম", "pôddo", "lotus", "noun"),
               V("জোয়ার-ভাটা", "jôyar-bhaṭa", "tide (ebb and flow)", "noun")],
              G("Living image + concrete claim",
                "image + je / mane + claim",
                "জীবনটা নদীর মতো — কখনো জোয়ার, কখনো ভাটা. Don't decorate: the image should carry "
                "one claim and then step aside. Padma-mud, lotus is the standard one: কাদা থেকেই পদ্ম "
                "ফোটে.",
                [X("জীবনটা নদীর মতো, কখনো জোয়ার কখনো ভাটা।", "jibônṭa nodir môto, kôkhono jôyar kôkhono bhaṭa.", "Life is like a river — sometimes flood, sometimes ebb."),
                 X("কাদা থেকেই পদ্ম ফোটে — শুরু খারাপ মানেই শেষ খারাপ নয়।", "kada thekei pôddo phoṭe — shuru kharap mane'i shesh kharap nôy.", "A lotus blooms from mud — a bad start does not mean a bad end."),
                 X("শহরের আলো-আঁধারি সবই আছে।", "shôhorer alo-ãdhari shôbai achhe.", "The city has its light and its shadow.")],
                [("নদী, মাছ, গাছ, পদ্ম — সবই সত্য।", "(one image, one claim)", "Three images in one paragraph compete and none lands."),
                 ("জীবন নদী, তাই খেয়াল রাখা দরকার।", "জীবন নদীর মতো — তাই খেয়াল রাখা দরকার।", "The image needs its comparison word: মতো.")]),
              [D("সুমি", "লেখাটা কেমন?", "lekhaṭa kemon?", "How is the piece?"),
               D("রাতুল", "শেষ অনুচ্ছেদটা পড়ে দেখো।", "shesh ônucchhedṭa pôṛe dekho.", "Read the last paragraph."),
               D("সুমি", "শুরু খারাপ মানেই শেষ খারাপ নয় — কাদা থেকেই পদ্ম ফোটে।", "shuru kharap mane'i shesh kharap nôy — kada thekei pôddo phoṭe.", "A bad start does not mean a bad end — a lotus blooms from mud."),
               D("রাতুল", "ঠিক — এক চিত্র, এক দাবি।", "ṭhik — ek chitro, ek dabi.", "Exactly — one image, one claim.")],
              WS("Image worksheet", [
                  T("Use one living image.", ["mixed fortunes", "a good outcome from a bad start"],
                    ["আলো-আঁধারি", "কাদা থেকে পদ্ম"]),
                  T("Trim competing images.", ["three metaphors in one paragraph"],
                    ["এক চিত্রই রাখি"]),
              ])),
        ]},
        {"id": "C1+-U2", "title": "Register up and down", "lessons": [
            L("Formal prose: তিនি to আপনি",
              "Formal Bengali prose keeps the passive and the nominal style: অনুমোদন দেওয়া হয়েছিল, "
              "প্রস্তাবটি গৃহীত, উল্লেখ করা প্রয়োজন. It also avoids the second person entirely — "
              "formal text addresses no one.",
              [V("প্রস্তাবটি", "prostabṭi", "the proposal (definite)", "noun"),
               V("গৃহীত", "grihito", "adopted", "adjective"),
               V("অনুমোদন", "onumodon", "approval", "noun"),
               V("প্রয়োজন", "proyojon", "necessary", "adjective"),
               V("উল্লেখ", "ullekh", "mention, reference", "noun")],
              G("Formal register: nominal + passive",
                "kôra hoyechhe · grihito hôlo · ullekh kôra proyojon",
                "প্রস্তাবটি দুই ধাপে পরীক্ষা করা হয়েছে এবং শেষে গৃহীত হয়েছে. No আপনি appears; "
                "the text speaks to a public, not to a person.",
                [X("নথিটি পরীক্ষা করে গৃহীত হয়েছে।", "nôthiṭi porikkha kôre grihito hoyechhe.", "The document was examined and adopted."),
                 X("উল্লেখ করা প্রয়োজন যে সময় কম।", "ullekh kôra proyojon je shomoy kôm.", "It is necessary to mention that time is short."),
                 X("এ সিদ্ধান্ত সর্বসম্মতভাবে নেওয়া হয়েছে।", "e siddhanto shôrbôshômmotobhabe neoa hoyechhe.", "This decision was taken unanimously.")],
                [("আপনি দেখবেন প্রস্তাব গৃহীত।", "প্রস্তাবটি পরীক্ষা করে গৃহীত হয়েছে।", "Formal prose keeps আপনি out of it."),
                 ("আমরা সবাই মিলে বলে দিলাম।", "সর্বসম্মতভাবে সিদ্ধান্ত নেওয়া হয়েছে।", "The nominal form carries the same meaning in the right register.")]),
              [D("লেখক", "প্রথম বাক্যটা ঠিক?", "prothom bakkoṭa ṭhik?", "Is the first sentence right?"),
               D("সম্পাদক", "খুব আপনি-মুখী। «আপনি দেখবেন» বাদ দিন।", "khub apni-mukhi. «apni dekhben» bad din.", "Too addressed to a person. Drop 'you will see'."),
               D("লেখক", "তাহলে?", "tahole?", "Then?"),
               D("সম্পাদক", "«নথিটি পরীক্ষা করে গৃহীত হয়েছে» — এই রকম।", "«nôthiṭi porikkha kôre grihito hoyechhe» — ei rôkom.", "'The document was examined and adopted' — like that.")],
              WS("Formal worksheet", [
                  T("Make it formal.", ["we decided", "you will see that it is right", "everybody agreed"],
                    ["সিদ্ধান্ত নেওয়া হয়েছে", "প্রতীয়মান হয় যে এটি সঠিক", "সর্বসম্মতভাবে গৃহীত"]),
                  T("Remove the second person.", ["(rewrite without আপনি/তুমি)"],
                    ["কর্তব্য অনুসারে ব্যবস্থা নেওয়া হবে"]),
              ])),
            L("Intimate prose: drop the করছি",
              "In personal writing Bengali gets shorter and warmer: মন খারাপ, চলে আয়, বলে দিলাম, "
              "কতদিন দেখা নেই. Verb endings switch to তুমি, and particles like তো, না, রে carry the "
              "tone.",
              [V("মন খারাপ", "môn kharap", "low spirits", "phrase"),
               V("চলে আয়", "chôle ay", "come over (intimate)", "phrase"),
               V("বলে দিলাম", "bôle dilam", "I've said it plainly", "phrase"),
               V("কতদিন", "kôto din", "how many days, how long", "interrogative"),
               V("তো", "to", "emphatic particle", "particle")],
              G("Intimate register: particles + short clauses",
                "… το · … na? · re (to a close friend)",
                "কতদিন দেখা নেই! মন খারাপ হলে চলে আয়, এক কাপ চা হবেই. The particle তো pushes the "
                "reader to agree; না? turns a statement into a shared one.",
                [X("কতদিন দেখা নেই, চলে আয়।", "kôto din dekha nei, chôle ay.", "We haven't met for ages — come over."),
                 X("মন খারাপ হলে বলিস, শুনব।", "môn kharap hole bolish, shunbo.", "If you're feeling low, tell me — I'll listen."),
                 X("বলে দিলাম, আর দেরি নয়।", "bôle dilam, ar deri nôy.", "I've said it plainly — no more delay.")],
                [("আপনি চলে আসবেন, মন খারাপ ہے।", "চলে আয়, মন খারাপ হলে।", "Mixing আপনি with চলে আয় breaks the register."),
                 ("মন খারাপ বলে দিলাম।", "মন খারাপ হলে বলে দিস।", "The two phrases belong to different clauses.")]),
              [D("সুমি", "কতদিন দেখা নেই!", "kôto din dekha nei!", "We haven't met for ages!"),
               D("মিতা", "সত্যি, মনে হচ্ছে মাস পেরিয়ে গেল।", "shôtti, mone hôchhe mash perie gelo.", "True — feels like a month has passed."),
               D("সুমি", "মন খারাপ হলে চলে আয়, চা হবেই।", "môn kharap hole chôle ay, cha hobei.", "If you're feeling low, come over — tea is a certainty."),
               D("মিতা", "বলে দিলাম, কালই আসছি।", "bôle dilam, kalii ashchhi.", "Said and done — I'm coming tomorrow.")],
              WS("Intimate worksheet", [
                  T("Make it intimate.", ["you should come over", "I am feeling low", "I have said it"],
                    ["চলে আয়", "মন খারাপ", "বলে দিলাম"]),
                  T("Use a particle.", ["come, won't you?", "it is true, isn't it?"],
                    ["চলে আয় না?", "সত্যি তো?"]),
              ])),
            L("Switching register inside one text",
              "A skilled Bengali writer can move between registers in one piece: formal in the "
              "argument, intimate in the example, formal again in the close. The switch is marked by "
              "the verb ending, not by an announcement.",
              [V("অনুচ্ছেদ", "ônucchhed", "paragraph", "noun"),
               V("সুর", "shur", "tone, tune", "noun"),
               V("ভাষাভঙ্গি", "bhashabhongi", "style, manner of speech", "noun"),
               V("নিবন্ধ", "nibôndho", "essay", "noun"),
               V("পরিভাষা", "poribhasha", "terminology", "noun")],
              G("Register switch = ending switch",
                "formal ending (-hoyechhe) → intimate (-chhe/-ish) → formal",
                "প্রবন্ধের প্রথম অংশে পরিভাষা, মাঝে উদাহরণ: «চলে আয়, বলল বন্ধু», শেষে আবার "
                "«সিদ্ধান্ত নেওয়া হয়েছে». The switch is a deliberate act with a boundary — the "
                "reader should feel the room change.",
                [X("প্রথম অংশের সুর formal, উদাহরণের সুর আন্তরিক।", "prothom ôngsher shur formal, udahôrôner shur antorik.", "The first part's tone is formal; the example's tone is warm."),
                 X("«বলে দিলাম», লিখল বন্ধু — তারপর আবার নিবন্ধের সুর।", "«bôle dilam», likhlo bondhu — tarpor abar nibôndher shur.", "'I've said it,' the friend wrote — then the essay's tone returns."),
                 X("ভাষাভঙ্গি বদলালে সীমাটা স্পষ্ট রাখতে হয়।", "bhashabhongi bôdlale shimaṭa shpôshṭo rakhte hôy.", "When the register changes, the boundary must stay clear.")],
                [("সব জায়গায় একই সুর, তবু আন্তরিক।", "formal অংশ, তারপর আন্তরিক উদাহরণ, তারপর formal।", "One register everywhere is not versatility — it is a missed switch."),
                 ("বন্ধু বলল, এবং তাই সিদ্ধান্ত গৃহীত হয়েছে আপনি।", "(the switch needs a boundary)", "A switch mid-clause reads as a mistake, not a style.")]),
              [D("সম্পাদক", "নিবন্ধটা এক সুরে লেখা?", "nibôndhoṭa ek shure lekha?", "Is the essay in one tone?"),
               D("লেখক", "না — শুরু পরিভাষায়, মাঝে একটা কথা বলার মতো উদাহরণ, শেষে সিদ্ধান্ত।", "na — shuru poribhashay, majhe ekṭa kôtha bolar môto udahôrôn, sheshe siddhanto.", "No — it starts in terminology, has a speakable example in the middle, and ends in the decision."),
               D("সম্পাদক", "ভালো, তবে সীমা স্পষ্ট রাখুন।", "bhalo, tôbe shima shpôshṭo rakhun.", "Good, but keep the boundary clear."),
               D("লেখক", "প্রতিটি অনুচ্ছেদের শেষেই আবার formal সুরে ফিরব।", "protiti ônucchheder sheshei abar formal shure phirbo.", "At the end of each paragraph I'll return to the formal tone.")],
              WS("Switch worksheet", [
                  T("Plan the registers.", ["argument → example → close"],
                    ["formal → আন্তরিক → formal"]),
                  T("Mark the boundary.", ["return to the argument"],
                    ["নতুন অনুচ্ছেদে formal সুরে ফেরা"]),
              ])),
        ]},
        {"id": "C1+-U3", "title": "Saying it better", "lessons": [
            L("Rhythm: long line, short line",
              "Bengali prose breathes with alternating length. A long qualification followed by a "
              "three-word sentence is a native rhythm — সময়টা কঠিন, তবে সম্ভব — তারপর: শুধু শুরুটা "
              "দরকার.",
              [V("ছন্দ", "chhôndo", "rhythm, meter", "noun"),
               V("দীর্ঘ", "dirgho", "long", "adjective"),
               V("সংক্ষিপ্ত", "shôngkkhipto", "brief", "adjective"),
               V("ব্যবধান", "bêbôdhan", "gap, interval", "noun"),
               V("জোর", "jor", "stress, emphasis", "noun")],
              G("Alternate length deliberately",
                "long clause + short clause; emphasis last",
                "যে কাজটা সবার আগে দরকার, সেটা আসলে ছোট: একটা তারিখ ঠিক করা. Bengali native "
                "prose lands the important word last and the shortest sentence after the longest.",
                [X("সময় কম, কাজ বেশি — তবু একটা পথ আছে।", "shomoy kôm, kaj beshi — tôbu ekṭa pôth achhe.", "Time is short, work is much — yet there is one way."),
                 X("প্রশ্নটা জটিল, উত্তরটা সহজ।", "proshnoṭa jôṭil, uttôrṭa shohoj.", "The question is complex; the answer is simple."),
                 X("সব ঠিক, একটা তারিখ বাকি।", "shôb ṭhik, ekṭa tarikh baki.", "Everything is fine — one date is missing.")],
                [("সব ঠিক। একটা তারিখ বাকি। সব ঠিক।", "(one rhythm per paragraph)", "Repeating the same beat makes prose mechanical."),
                 ("সময় কম কিন্তু কাজ বেশি এবং লোক কম।", "সময় কম, কাজ বেশি, লোক কম।", "Bengali lists without ও/এবং when the rhythm needs the beat.")]),
              [D("সম্পাদক", "অনুচ্ছেদটা পড়ুন।", "ônucchhedṭa pôṛun.", "Read the paragraph."),
               D("লেখক", "সময় কম, লোক কম, আর কাজ?", "shomoy kôm, lok kôm, ar kaj?", "Time is short, people are few — and the work?"),
               D("সম্পাদক", "শেষ বাক্যটা ছোট করুন।", "shesh bakkoṭa chhoṭ kôrun.", "Make the last sentence short."),
               D("লেখক", "«কাজ সব আছে, শুধু শুরু দরকার।»", "«kaj shôb achhe, shudhu shuru dôrkar.»", "'The work is all there — only a start is needed.'")],
              WS("Rhythm worksheet", [
                  T("Make the sentence land.", ["long clause: time is short but there is a way", "(three-word close): only a start is needed"],
                    ["সময় কম, তবু পথ আছে", "শুধু শুরুটা দরকার"]),
                  T("Trim the connectives.", ["সময় কম কিন্তু কাজ বেশি এবং লোক কম"],
                    ["সময় কম, কাজ বেশি, লোক কম"]),
              ])),
            L("Precision: replace the vague verb",
              "Vague verbs hide weak thinking: করা, হওয়া, দেওয়া. Bengali alternatives are concrete: "
              "নির্ধারণ করা (determine), নিশ্চিত করা (confirm), হস্তান্তর করা (hand over), এগিয়ে "
              "নেওয়া (move forward), ফিরিয়ে আনা (bring back).",
              [V("নির্ধারণ", "nirdharon", "determination, fixing", "noun"),
               V("নিশ্চিত করা", "nishchito kôra", "to confirm", "verb"),
               V("হস্তান্তর", "hôstantor", "handover", "noun"),
               V("এগিয়ে নেওয়া", "egiye neoa", "to take forward", "phrase"),
               V("ফিরিয়ে আনা", "phiriye ana", "to bring back", "phrase")],
              G("Concrete verb beats করা",
                "kôra → nirdharon kôra / nishchito kôra / hôstantor kôra",
                "«তারিখ ঠিক করা হয়েছে» better than «তারিখ নিয়ে কাজ হয়েছে». The concrete verb names "
                "the action and saves the reader a question.",
                [X("তারিখ নির্ধারণ করা হয়েছে।", "tarikh nirdharon kôra hoyechhe.", "The date has been fixed."),
                 X("ফাইলটি দুপুরে হস্তান্তর করা হবে।", "failṭi dupure hôstantor kôra hobe.", "The file will be handed over at noon."),
                 X("প্রস্তাবটা এগিয়ে নেওয়ার সময় এসেছে।", "prostabṭa egiye neoar shomoy eshechhe.", "The time has come to take the proposal forward.")],
                [("তারিখ নিয়ে কাজ করা হয়েছে।", "তারিখ নির্ধারণ করা হয়েছে।", "নিয়ে কাজ করা names nothing."),
                 ("ফাইলটা দেওয়া হয়েছে।", "ফাইলটি হস্তান্তর করা হয়েছে।", "দেওয়া is vague about the handover.")]),
              [D("মিতা", "«তারিখ নিয়ে কাজ হয়েছে» — এটা কী?", "«tarikh niye kaj hoyechhe» — eṭa ki?", "'Work was done about the date' — what is that?"),
               D("রাতুল", "অস্পষ্ট। বলুন: তারিখ নির্ধারণ হয়েছে।", "ôspôshṭo. bolun: tarikh nirdharon hoyechhe.", "Vague. Say: the date has been fixed."),
               D("মিতা", "আর «ফাইল দেওয়া হয়েছে»?", "ar «fail deoa hoyechhe»?", "And 'the file has been given'?"),
               D("রাতুল", "«হস্তান্তর করা হয়েছে» — কে, কাকে, কখন, সব স্পষ্ট।", "«hôstantor kôra hoyechhe» — ke, kake, kôkhon, shôb shpôshṭo.", "'Has been handed over' — who, to whom, when: all clear.")],
              WS("Precision worksheet", [
                  T("Replace the vague verb.", ["work was done about the date", "the file was given", "the plan was taken forward"],
                    ["তারিখ নির্ধারণ হয়েছে", "ফাইল হস্তান্তর হয়েছে", "পরিকল্পনা এগিয়ে নেওয়া হয়েছে"]),
                  T("Make it concrete.", ["talk happened about the budget"],
                    ["বাজেট চূড়ান্ত করা হয়েছে"]),
              ])),
            L("Revising your own paragraph",
              "Revision in Bengali has four cuts: nominalise (make it noun-based), shorten (প্রতি "
              "শব্দে এক অর্থ), order (decision first), and read aloud. A revised paragraph is usually "
              "a third shorter and twice as clear.",
              [V("পুনর্লিখন", "punorlikhon", "rewriting", "noun"),
               V("সংক্ষেপ", "shôngkkhep", "abbreviation, shortening", "noun"),
               V("ক্রম", "krom", "order, sequence", "noun"),
               V("পাঠ", "path", "reading", "noun"),
               V("স্পষ্ট", "shpôshṭo", "clear", "adjective")],
              G("Four cuts",
                "nominalise · shorten · decision first · read aloud",
                "প্রথম খসড়া: «আমরা অনেক আলোচনার পরে সিদ্ধান্তে পৌঁছেছি যে সময়সীমা বাড়ানো হবে।» "
                "পুনর্লিখন: «সিদ্ধান্ত: সময়সীমা বাড়ানো হবে।» — one third of the words, all of the "
                "meaning.",
                [X("সিদ্ধান্ত: সময়সীমা দুই সপ্তাহ বাড়ানো হবে।", "siddhanto: shomoy-shima dui shoptah bôrano hobe.", "Decision: the deadline will be extended by two weeks."),
                 X("কারণ: বাইরের তথ্য দেরিতে এসেছে।", "karôn: bairer tôthỹo derite eshechhe.", "Reason: the outside data arrived late."),
                 X("পরবর্তী পদক্ষেপ: সোমবার নতুন তারিখ।", "pôrobortī pôdokkhep: shombar nôtun tarikh.", "Next step: a new date on Monday.")],
                [("আমরা অনেক আলোচনার পরে সিদ্ধান্তে পৌঁছেছি যে...", "সিদ্ধান্ত: …", "The frame is part of the draft, not of the text."),
                 ("পুনর্লিখনের পরে আরও লম্বা হলো।", "(revision shortens)", "If a revision grew, it was written, not revised.")]),
              [D("সম্পাদক", "তিনবার পড়েছেন?", "tinbar pôṛechhen?", "Have you read it three times?"),
               D("লেখক", "হ্যাঁ। দ্বিতীয় খসড়া এক-তৃতীয়াংশ ছোট।", "hã. ditio khôsṛa ek-tritiangsho chhoṭ.", "Yes. The second draft is a third shorter."),
               D("সম্পাদক", "সিদ্ধান্ত আগে আছে?", "siddhanto age achhe?", "Is the decision first?"),
               D("লেখক", "আছে — সিদ্ধান্ত, কারণ, পদক্ষেপ।", "achhe — siddhanto, karôn, pôdokkhep.", "It is — decision, reason, step.")],
              WS("Revision worksheet", [
                  T("Cut the frame.", ["after long discussion we decided that the date will change"],
                    ["সিদ্ধান্ত: তারিখ বদলাবে"]),
                  T("Order it.", ["reason, decision, next step"],
                    ["সিদ্ধান্ত, কারণ, পরবর্তী পদক্ষেপ"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Bengali idiom sits at the centre of literary culture: Chandidas's «সবার উপরে মানুষ "
                 "সত্য» and the proverb stock are quoted in parliament and in tea stalls with the same "
                 "gravity. A C1 learner is expected to catch the allusion and, more importantly, to "
                 "notice when an idiom is doing the arguing — and then to ask for the evidence behind "
                 "the image rather than accepting it."),
        source_url="https://en.wikipedia.org/wiki/Bengali_proverbs",
        reading=("সম্পাদক বললেন, «লেখাটা ভালো, তবে শেষ অনুচ্ছেদটা দুর্বল।» আমি আবার পড়লাম। প্রথমে "
                 "পরিভাষা, তারপর একটা আন্তরিক উদাহরণ, শেষে তিন লাইনের সিদ্ধান্ত — যেভাবে হওয়া "
                 "উচিত। কিন্তু শেষে আমি একটা প্রবাদ বসিয়েছিলাম, আর সেটা যুক্তির বদলে সাজসজ্জা হয়ে "
                 "গিয়েছিল। কেটে দিলাম। পুনর্লিখনের পর লেখাটা এক-তৃতীয়াংশ ছোট, আর অনেক স্পষ্ট। "
                 "শিখলাম, প্রবাদ যুক্তি নয় — যুক্তির পরে অলংকার।"),
        reading_gloss=("The editor said, 'The piece is good, but the last paragraph is weak.' I read "
                       "it again. Terminology first, then a warm example, then a three-line decision — "
                       "as it should be. But at the end I had placed a proverb, and it had become "
                       "decoration instead of an argument. I cut it. After the rewrite the piece is a "
                       "third shorter and much clearer. I learned: a proverb is not an argument — it "
                       "is the ornament after the argument."),
        listening=("মিতা: চোখ কপালে ওঠা — এটা এখানে ঠিক হয়েছে?<br>সম্পাদক: হয়েছে, কারণ খবরটা "
                   "অপ্রত্যাশিত ছিল।<br>মিতা: আর প্রবাদটা?<br>সম্পাদক: কেটে দাও — এক জায়গায় এক "
                   "অলংকার।"),
        listening_gloss=("Mita: Is 'eyes up to the forehead' right here? Editor: It is, because the news "
                         "was unexpected. Mita: And the proverb? Editor: Cut it — one ornament per "
                         "place."),
        voice_tag=VOICE,
        idioms=[
            ("কথার মোড়", "the turn of speech", "the twist in the argument"),
            ("অর্থের গভীরে", "deep in meaning", "at a deeper level"),
            ("শব্দের ওজন", "the weight of words", "how much a word carries"),
            ("ভাষার সৌন্দর্য", "the beauty of language", "beauty of expression"),
            ("সরল ভাষা", "simple language", "plain style"),
            ("রুচি অনুযায়ী", "according to taste", "as taste dictates"),
            ("নিজের হাতে", "by one's own hand", "one's own work"),
            ("দুইবার পড়া", "reading twice", "rereading for revision"),
            ("সুর মিলিয়ে", "matching the tune", "keeping the tone consistent"),
            ("ছোট করে বলা", "to say briefly", "to put it briefly"),
        ],
        mistakes=[
            ("প্রবাদ, তাই প্রমাণ।", "প্রবাদ — উপমা, প্রমাণ নয়।", "A proverb argues by analogy; evidence is still required."),
            ("তার অনেক হাতযশ, কিন্তু হাত নেই।", "তার হাতযশ আছে।", "An idiom is one indivisible image."),
            ("পুনর্লিখনের পরে লেখা আরও লম্বা হলো।", "পুনর্লিখনের পরে লেখা ছোট হলো।", "Revision shortens; if it grew, it was a rewrite of intent, not a revision."),
        ],
        task_title="Revise one paragraph three times",
        task_instructions=("Take any paragraph you have written in Bengali and revise it three times: "
                           "cut the frames, replace every vague করা/হওয়া with a concrete verb, put the "
                           "decision first. Compare the lengths. Then read the final version aloud — "
                           "where your voice runs out of breath, the sentence is too long, and where "
                           "you stumble, it is the register that changed without warning."),
    ),
    "test": [
        ("translate_en", "Say: The proposal was examined and adopted unanimously.", "প্রস্তাবটি পরীক্ষা করে সর্বসম্মতভাবে গৃহীত হয়েছে।"),
        ("translate_ar", "খবর শুনে সবার চোখ কপালে উঠল।", "Hearing the news, everyone was astonished."),
        ("multiple_choice", "Which is the formal close?", "সিদ্ধান্ত: সময়সীমা বাড়ানো হয়েছে।"),
        ("fill_in_the_blank", "এক মাঘে শীত ___ না। (does not go)", "যায়"),
        ("word_selection", "Select the Bengali for 'handover'.", "হস্তান্তর"),
        ("error_correction", "তারিখ নিয়ে কাজ করা হয়েছে।", "তারিখ নির্ধারণ করা হয়েছে।"),
        ("dialogue_completion", "Complete: কতদিন দেখা নেই, ___ (come over)", "চলে আয়"),
        ("matching", "Match ছন্দ to its meaning.", "rhythm"),
        ("reading_comprehension", "কেন প্রবাদটা কেটে দেওয়া হলো?", "কারণ সেটা যুক্তির বদলে সাজসজ্জা হয়েছিল"),
        ("inference", "«প্রবাদ যুক্তি নয় — যুক্তির পরে অলংকার» — what does the editor mean?", "an idiom decorates an argument, it does not replace evidence"),
        ("main_idea", "লেখাটা এক-তৃতীয়াংশ ছোট হয়েছে। What happened?", "the revision shortened it"),
        ("detail_identification", "পুনর্লিখনের পর লেখাটা কতটা ছোট হলো?", "এক-তৃতীয়াংশ"),
    ],
}

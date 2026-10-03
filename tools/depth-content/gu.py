# -*- coding: utf-8 -*-
"""Gujarati PHASE 1 depth — extras, third lessons, half-step rungs.

Written with the DSL in `tools/depth_kit.py`; rendered by
`tools/author-depth.py --lang gu`.

House style follows the shipped Gujarati course: Gujarati script with the
course's own romanisation (`aa` for આ, `chh`, `sh`, `th`, `kh`, `d`/`dh`), and
the course's unit ids (`gu-a1-u1`, lesson `gu-a1-l1`) for the CEFR rungs and
`gu-c1-u1` for C1/C2. Half-step rungs use `<rung>-U1`, e.g. `A1+-U1`.

Register note: the module teaches the spoken standard (બોલચાલની ભાષા) and keeps
the heavier literary register for the C1/C2 rungs, where it is recognised
rather than imitated — the same decision the shipped course makes.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # tools/ on the path
from depth_kit import D, EXTRA, G, L, T, V, WS, X   # noqa: E402

CODE = "gu"
NAME = "Gujarati"
NATIVE = "ગુજરાતી"
PHASE = 2
SCRIPT = "Gujarati script"
VOICE = "gu-IN"
SKILL = ("Gujarati: Gujarati script, postpositions, verb-final order, polite vs familiar "
         "address, aspect and the compound verb")

EXTRAS = {}
THIRD = {}
HALFSTEPS = {}

EXTRAS["A1"] = EXTRA(
    culture=("Gujarati is written left to right in a script of its own: the vowel signs hang on "
             "the consonant they follow, so ક + ા = કા. There are no capitals, and a sentence "
             "begins with the same letter it would use in the middle. ગુજરાતી addresses people by "
             "age: આપ to elders, તમે to strangers and equals, તું at home — the verb changes with "
             "the pronoun, so the choice is audible in the first sentence."),
    source_url="https://en.wikipedia.org/wiki/Gujarati_language",
    reading=("હું આરતી છું. હું અમદાવાદમાં રહું છું. મારું ઘર નદીની પાસે છે. મારી મા શિક્ષક છે "
             "અને મારા પિતા દુકાન ચલાવે છે. મને ગુજરાતી અને અંગ્રેજી બંને ભાષા ગમે છે. આજે "
             "સવારે હું બસમાં સ્ટેશન ગઈ હતી. હવે હું ઘરે છું અને ચા પીઉં છું."),
    reading_gloss=("I am Arti. I live in Ahmedabad. My house is near the river. My mother is a "
                   "teacher and my father runs a shop. I like both Gujarati and English. This "
                   "morning I went to the station by bus. Now I am at home and drinking tea."),
    listening=("Neighbour: કેમ છો?<br>Aarti: મજામાં છું, આભાર. તમે?<br>Neighbour: હું પણ મજામાં. "
               "આ તમારી દીકરી છે?<br>Aarti: હા, એનું નામ મીરા છે."),
    listening_gloss=("Neighbour: How are you? Aarti: I am well, thank you. And you? Neighbour: I "
                     "am well too. Is this your daughter? Aarti: Yes, her name is Meera."),
    voice_tag=VOICE,
    idioms=[
        ("મજામાં", "in enjoyment", "fine, doing well"),
        ("આભાર", "gratitude", "thank you"),
        ("શું થયું?", "what happened?", "what is the matter?"),
        ("ધીમે ધીમે", "slowly slowly", "little by little"),
        ("વાંધો નહીં", "no objection", "no problem, that is fine"),
        ("ખાસ નહીં", "not special", "nothing much"),
        ("ચા પીવી", "to drink tea", "to catch up over tea"),
        ("હાથ જોડવા", "to join the hands", "to greet respectfully"),
        ("મન લાગવું", "for the mind to attach", "to feel at home somewhere"),
        ("એક મિનિટ", "one minute", "just a moment"),
    ],
    mistakes=[
        ("હું અમદાવાદ છું.", "હું અમદાવાદમાં છું.", "A place takes the locative -માં: અમદાવાદમાં."),
        ("તમે કેમ છે?", "તમે કેમ છો?", "તમે takes છો; છે belongs to તે and to plurals like તેઓ."),
        ("મારી નામ આરતી છે.", "મારું નામ આરતી છે.", "નામ is neuter, so the possessive is મારું."),
    ],
    task_title="Introduce your street in Gujarati",
    task_instructions=("Write six Gujarati sentences about the street you live in: its name, what "
                       "is near it (પાસે), one shop, one neighbour and one thing you do there every "
                       "day. Read them out loud and mark every noun that needed a postposition — "
                       "માં, પર, પાસે, ની. Those markers are the whole grammar of place in Gujarati, "
                       "and the list you write is your first vocabulary of your own street."),
)

EXTRAS["A2"] = EXTRA(
    culture=("Gujarati households run on tea and the bargaining that goes with it: ચા is offered "
             "before business of any kind, and a refusal is softened with વાંધો નહીં. In the market "
             "the price is a starting point — સસ્તું (cheap) and મોંઘું (expensive) are opinions, "
             "and asking ઓછું કરો (make it less) is normal, not rude. The polite forms વધારે/ઓછું "
             "matter more here than in a supermarket."),
    source_url="https://en.wikipedia.org/wiki/Gujarati_cuisine",
    reading=("આજે બજારમાં બહુ ભીડ હતી. મેં ટામેટાં અને બટાકા લીધા. દુકાનદારે કહ્યું, «એક કિલો "
             "ત્રીસ રૂપિયા». મેં કહ્યું, «ઓછું કરો». અંતે પચ્ચીસ રૂપિયામાં વાત થઈ. પછી હું "
             "દૂધ લેવા ગઈ. દૂધવાળો બોલ્યો, «કાલે દૂધ મોડું આવશે». મેં કહ્યું, «વાંધો નહીં»."),
    reading_gloss=("Today the market was very crowded. I bought tomatoes and potatoes. The "
                   "shopkeeper said, 'thirty rupees a kilo'. I said, 'make it less'. In the end we "
                   "settled on twenty-five rupees. Then I went to buy milk. The milkman said, "
                   "'tomorrow the milk will come late'. I said, 'no problem'."),
    listening=("Grahak: આ કિલો કેટલાનું છે?<br>Dukandar: પચાસ રૂપિયા.<br>Grahak: થોડું ઓછું "
               "કરો.<br>Dukandar: ચાલો, પિસ્તાલીસ."),
    listening_gloss=("Customer: How much is a kilo of this? Shopkeeper: Fifty rupees. Customer: "
                     "Make it a little less. Shopkeeper: All right, forty-five."),
    voice_tag=VOICE,
    idioms=[
        ("ઓછું કરો", "make it less", "bring the price down"),
        ("વાત થઈ", "the talk happened", "we settled on a price"),
        ("ભીડ", "crowd", "a crowd, a rush"),
        ("મોડું આવવું", "to come late", "to be late"),
        ("વાંધો નહીં", "no objection", "that is fine"),
        ("એક કિલો", "one kilo", "one kilogram"),
        ("ચાલો", "let us go", "all right, come on"),
        ("દૂધ લેવા જવું", "to go to take milk", "to go for milk"),
        ("પૈસા પાછા", "money back", "refund"),
        ("કેટલાનું?", "of how much?", "how much does it cost?"),
    ],
    mistakes=[
        ("આ કિલો કેટલો છે?", "આ કિલો કેટલાનું છે?", "A price is neuter: કેટલાનું."),
        ("મેં બજાર ગયો.", "હું બજાર ગયો.", "Intransitive જવું takes હું, not the ergative મેં."),
        ("દૂધવાળો કાલે મોડું આવશે છે.", "દૂધવાળો કાલે મોડું આવશે.", "The future is one word: આવશે."),
    ],
    task_title="Do a market round in Gujarati",
    task_instructions=("Write the six lines of a real market round: ask the price (કેટલાનું છે?), "
                       "say it is expensive, ask for less, agree, ask for one more item, and close "
                       "with thanks. Then write the same exchange where the shopkeeper says no and "
                       "you accept it with વાંધો નહીં. The second version is the one that teaches "
                       "the tone; keep both in your notebook under one heading."),
)

EXTRAS["B1"] = EXTRA(
    culture=("Gujarati professional life keeps two clocks: the meeting time and the time people "
             "arrive. A written agenda (કાર્યસૂચિ) exists, but the decisions are taken orally and "
             "confirmed afterwards in a short message. The register moves fast — આપ with a client, "
             "તમે in the office, તું between colleagues who have known each other for years — and "
             "choosing wrong is louder than any grammar mistake."),
    source_url="https://en.wikipedia.org/wiki/Gujarati_people",
    reading=("આજની બેઠકમાં ત્રણ મુદ્દા હતા. પહેલા મુદ્દા પર બધા સહમત થયા. બીજા મુદ્દા પર મને "
             "વાંધો હતો, તેથી મેં કહ્યું, «મને આ સૂચન ઠીક લાગતું નથી, કારણ કે સમય ઓછો છે». "
             "અંતે નક્કી થયું કે પહેલા નાનો પ્રયોગ કરીશું. ત્રીજો મુદ્દો પછી માટે રહેવા દીધો. "
             "બેઠક પછી મેં ટૂંકો સંદેશ મોકલ્યો."),
    reading_gloss=("Today's meeting had three points. On the first point everyone agreed. On the "
                   "second point I had an objection, so I said, 'This proposal does not seem right "
                   "to me, because there is little time.' In the end it was decided that we would "
                   "first run a small trial. The third point was left for later. After the meeting "
                   "I sent a short message."),
    listening=("Manager: બેઠક કેમ ચાલી?<br>Neighbour: સારી. પહેલા મુદ્દા પર સહમતી થઈ.<br>"
               "Manager: બીજા મુદ્દા પર?<br>Neighbour: મારો વાંધો હતો, પણ નક્કી થયું કે પ્રયોગ "
               "કરીશું."),
    listening_gloss=("Manager: How did the meeting go? Neighbour: Well. On the first point we "
                     "agreed. Manager: On the second point? Neighbour: I had an objection, but it "
                     "was decided that we would run a trial."),
    voice_tag=VOICE,
    idioms=[
        ("કાર્યસૂચિ", "list of tasks", "the agenda"),
        ("સહમત થવું", "to become agreed", "to agree"),
        ("વાંધો હોવો", "to have an objection", "to object"),
        ("નક્કી થયું", "it became fixed", "it was decided"),
        ("પ્રયોગ કરવો", "to do a trial", "to run a pilot"),
        ("પછી માટે રહેવા દેવું", "to let stay for later", "to leave for later"),
        ("ટૂંકો સંદેશ", "short message", "a brief message"),
        ("અંતે", "at the end", "in the end"),
        ("મને ઠીક લાગે છે", "it seems right to me", "I think it is fine"),
        ("કારણ કે", "for the reason that", "because"),
    ],
    mistakes=[
        ("મને આ સૂચન ઠીક લાગે છે નહીં.", "મને આ સૂચન ઠીક લાગતું નથી.", "The negative of લાગે છે is લાગતું નથી."),
        ("મેં વાંધો હતો.", "મારો વાંધો હતો.", "The objection belongs to me: મારો વાંધો."),
        ("નક્કી કર્યું કે પ્રયોગ કરીશું.", "નક્કી થયું કે પ્રયોગ કરીશું.", "A collective decision is નક્કી થયું, not નક્કી કર્યું."),
    ],
    task_title="Run a three-point meeting and message the decision",
    task_instructions=("Take a real decision you have to take this week and write the Gujarati for "
                       "it: the three agenda points, one line where you agree (સહમત છું), one line "
                       "where you object with a reason (મને ઠીક લાગતું નથી, કારણ કે …), and the "
                       "decision as it would be announced (નક્કી થયું કે …). Then write the short "
                       "message you would send afterwards — a decision, an owner and a date. If the "
                       "message has no date, the meeting did not decide anything."),
)

EXTRAS["B2"] = EXTRA(
    culture=("Gujarati argument leans on the concessive hinge: સાચું છે કે … પણ … ('it is true "
             "that … but …'). Giving the other side its due before the objection is not politeness "
             "here — it is the structure that makes the objection land. The same hinge appears in "
             "editorials, family arguments and contract negotiations, which is why one pattern "
             "pays for itself three times."),
    source_url="https://en.wikipedia.org/wiki/Gujarati_literature",
    reading=("સાચું છે કે આ યોજના ઘણી મહેનત માગે છે; તેમ છતાં તે વગર અમે વધુ મોટું જોખમ "
             "લઈએ છીએ. બીજી બાજુ, ખર્ચ પણ વધશે — આપણે તે સ્વીકારવું પડશે. મારો મત એ છે કે "
             "પહેલા છ મહિનાનો પ્રયોગ કરવો, અને પરિણામ જોઈને આગળ વધવું. જો પરિણામ સારું ન "
             "હોય, તો આપણે યોજના બદલી શકીશું."),
    reading_gloss=("It is true that this plan demands a lot of work; nevertheless, without it we "
                   "take on a bigger risk. On the other hand, the cost will rise too — we have to "
                   "accept that. My view is that we should first run a six-month trial and then "
                   "decide on the results. If the results are not good, we can change the plan."),
    listening=("Analyst: સાચું છે કે ખર્ચ વધશે.<br>Editor: તેમ છતાં જોખમ ઓછું થશે.<br>Analyst: "
               "બીજી બાજુ, સમય પણ લાગશે.<br>Editor: તો પહેલા પ્રયોગ કરીએ."),
    listening_gloss=("Analyst: It is true that the cost will rise. Editor: Nevertheless the risk "
                     "will fall. Analyst: On the other hand, it will also take time. Editor: Then "
                     "let us run a trial first."),
    voice_tag=VOICE,
    idioms=[
        ("સાચું છે કે", "it is true that", "admittedly"),
        ("તેમ છતાં", "even so", "nevertheless"),
        ("બીજી બાજુ", "on the other side", "on the other hand"),
        ("સ્વીકારવું પડશે", "it will have to be accepted", "we will have to accept it"),
        ("મારો મત એ છે કે", "my opinion is that", "my view is that"),
        ("આગળ વધવું", "to move forward", "to go ahead"),
        ("પરિણામ", "result", "the result"),
        ("જોખમ લેવું", "to take a risk", "to take a risk"),
        ("યોજના બદલવી", "to change the plan", "to change the plan"),
        ("છ મહિનાનો પ્રયોગ", "a six-month trial", "a six-month pilot"),
    ],
    mistakes=[
        ("સાચું છે કે આ યોજના સારી છે, પણ તેમ છતાં ખર્ચ વધે છે, પણ મને નહીં ગમે.", "સાચું છે કે આ યોજના સારી છે, પણ ખર્ચ વધે છે.", "One hinge per sentence; પણ and તેમ છતાં do not pile up."),
        ("મારો મત છે કે પ્રયોગ કરીએ છીએ.", "મારો મત છે કે પ્રયોગ કરીએ.", "A proposal after મત છે કે takes the subjunctive-ish કરીએ."),
        ("જો પરિણામ સારું ન હોય, તો આપણે યોજના બદલીશું હતું.", "જો પરિણામ સારું ન હોય, તો આપણે યોજના બદલી શકીશું.", "A counterfactual option is expressed with શકીશું."),
    ],
    task_title="Write one two-storey argument in Gujarati",
    task_instructions=("Choose something you actually disagree with — a plan, a purchase, a "
                       "timetable — and write it in Gujarati as a two-storey argument: સાચું છે કે "
                       "… , તેમ છતાં … ; બીજી બાજુ … ; મારો મત એ છે કે … . Then say what would "
                       "change your mind. That last sentence is the one that turns an argument into "
                       "a negotiation, and it is the sentence learners usually forget to write."),
)

EXTRAS["C1"] = EXTRA(
    culture=("Written Gujarati keeps a second register for public and academic prose: longer "
             "sentences, the passive (કરવામાં આવ્યું), and nominal chains where speech would use a "
             "verb (અમલીકરણ — implementation). C1 work is learning to un-nominalise: read "
             "«અમલીકરણ કરવામાં આવશે» and hear «કોઈ કરશે, પણ કોણ, ક્યારે». The plain version is not a "
             "downgrade — it is the version a reader can act on."),
    source_url="https://en.wikipedia.org/wiki/Gujarati_grammar",
    reading=("અહેવાલમાં જણાવાયું છે કે «યોજનાનું અમલીકરણ મૂલ્યાંકનને આધીન રહેશે». સરળ ગુજરાતીમાં: "
             "કોઈકે તપાસવું પડશે કે યોજના કામ કરે છે કે નહીં, અને અહેવાલ એ નથી કહેતો કે તે કોણ "
             "કરશે. આ અસ્પષ્ટતા જ નોંધનું મુખ્ય મુદ્દો છે: દરેક પરોક્ષ વાક્ય માટે ક્રિયા, "
             "કર્તા અને તારીખ લખવા."),
    reading_gloss=("The report states that 'the implementation of the plan will be subject to "
                   "evaluation'. In plain Gujarati: somebody will have to check whether the plan "
                   "works or not, and the report does not say who will do it. This vagueness is "
                   "exactly the note's main point: for every passive sentence, write the verb, the "
                   "agent and the date."),
    listening=("Analyst: યોજનાનું અમલીકરણ થશે.<br>Reviewer: કોણ કરશે?<br>Analyst: બે કર્મચારી, "
               "પંદર દિવસ, ત્રણ પાનાની નોંધ.<br>Reviewer: હવે સ્પષ્ટ છે."),
    listening_gloss=("Analyst: The plan will be implemented. Reviewer: Who will do it? Analyst: Two "
                     "staff, fifteen days, a three-page note. Reviewer: Now it is clear."),
    voice_tag=VOICE,
    idioms=[
        ("જણાવાયું છે", "it is stated", "the report says"),
        ("આધીન રહેશે", "will remain subject to", "will be subject to"),
        ("અમલીકરણ", "implementation", "implementation"),
        ("મૂલ્યાંકન", "evaluation", "evaluation"),
        ("અસ્પષ્ટતા", "unclearness", "vagueness"),
        ("પરોક્ષ વાક્ય", "indirect sentence", "a passive sentence"),
        ("કર્તા", "doer", "the agent"),
        ("તારીખ", "date", "the date"),
        ("સરળ ગુજરાતીમાં", "in simple Gujarati", "in plain Gujarati"),
        ("સ્પષ્ટ છે", "it is clear", "it is clear"),
    ],
    mistakes=[
        ("નિર્ણય લેવામાં આવ્યો હતો પણ કોઈએ નહીં.", "નિર્ણય લેવામાં આવ્યો: બે વ્યક્તિ, પંદર દિવસ, એક નોંધ.", "The passive hides the agent; name the people and the date."),
        ("યોજના મૂલ્યાંકન છે.", "યોજનાનું મૂલ્યાંકન થશે.", "Nominal sentences need the doing verb થશે."),
        ("અમલીકરણ કરવામાં આવશે દ્વારા વિભાગ.", "વિભાગ યોજના લાગુ કરશે.", "Un-nominalise: the department does it, in the active."),
    ],
    task_title="Un-nominalise one Gujarati administrative paragraph",
    task_instructions=("Take a real Gujarati notice, letter or form — a bill, a circular, a form "
                       "at a government office — and rewrite it three times: exactly as written, in "
                       "plain Gujarati with a named agent and a doing verb, and as a three-line note "
                       "that says who does what by when. List every nominal phrase you had to "
                       "unpack (અમલીકરણ, મૂલ્યાંકન, ધ્યાને લેવું); that list is your C1 vocabulary."),
)

EXTRAS["C2"] = EXTRA(
    culture=("Gujarati public speech prefers understatement to the direct claim: a refusal can "
             "arrive as «જોઈએ તો વિચારીએ» and a criticism as «થોડું ધ્યાન આપવું પડે». C2 reading "
             "means hearing the force under the hedge and knowing which hedge is a real no. "
             "The same economy shows in idiom: litotes and the half-said phrase carry more weight "
             "than the superlative, and the writer who overstates is read as unsure."),
    source_url="https://en.wikipedia.org/wiki/Register_(sociolinguistics)",
    reading=("«જોઈએ તો વિચારીએ» એ ના છે. «થોડું ધ્યાન આપવું પડે» એ ટકોર છે. વક્તા જ્યારે નમ્ર "
             "શબ્દ વાપરે છે ત્યારે દબાણ ઓછું થતું નથી — તે દબાણનું સ્થાન બદલાય છે, વ્યક્તિ પરથી "
             "કામ પર. એટલે સાંભળનારે પૂછવું જોઈએ: ક્યારે, કોણ, કેટલું. જે જવાબ આપે નહીં, તે ના છે."),
    reading_gloss=("'If you like, let us think about it' is a no. 'A little more attention is "
                   "needed' is a rebuke. When a speaker uses a soft word the pressure does not "
                   "disappear — it moves, from the person to the work. So the listener has to ask: "
                   "when, who, how much. The answer that gives none of the three is a no."),
    listening=("Editor: તેમણે શું કહ્યું?<br>Mediator: «જોઈએ તો વિચારીએ».<br>Editor: તારીખ કહી?<br>"
               "Mediator: ના. એટલે તે ના છે."),
    listening_gloss=("Editor: What did they say? Mediator: 'If you like, let us think about it'. "
                     "Editor: Did they give a date? Mediator: No. So it is a no."),
    voice_tag=VOICE,
    idioms=[
        ("જોઈએ તો વિચારીએ", "if it is wanted, let us think", "a polite no"),
        ("થોડું ધ્યાન આપવું પડે", "a little attention must be given", "a mild rebuke"),
        ("ના કહેવું", "to say no", "to refuse"),
        ("નમ્ર શબ્દ", "a humble word", "a soft word"),
        ("દબાણ", "pressure", "pressure"),
        ("સ્થાન બદલવું", "to change place", "to shift"),
        ("સાંભળનાર", "the listener", "the listener"),
        ("ક્યારે, કોણ, કેટલું", "when, who, how much", "the three questions of a real answer"),
        ("ટકોર", "a pointed remark", "a rebuke"),
        ("અતિશયોક્તિ", "exaggeration", "overstatement"),
    ],
    mistakes=[
        ("«જોઈએ તો વિચારીએ» નો અર્થ «હા» છે.", "«જોઈએ તો વિચારીએ» નો અર્થ ના છે, જ્યાં સુધી તારીખ ન આવે.", "A hedge with no date is a refusal, not a yes."),
        ("નમ્ર શબ્દ દબાણ ઓછું કરે છે.", "નમ્ર શબ્દ દબાણનું સ્થાન બદલે છે.", "Understatement moves the pressure; it does not remove it."),
        ("તેમણે અતિશયોક્તિ કરી, તેથી તે સાચા છે.", "અતિશયોક્તિ વક્તાને અનિશ્ચિત દેખાડે છે.", "In this register, overstatement reads as uncertainty."),
    ],
    task_title="Read one refusal and write one",
    task_instructions=("Find a real Gujarati refusal you have received — a message, an email, a "
                       "spoken no you wrote down — and analyse it in three lines: the words used, "
                       "what they literally mean, and what they did (no, deferral, or an invitation "
                       "to argue). Then write your own refusal in the same register, and add the "
                       "date you would have to give if you actually meant 'later'. Keep both texts "
                       "side by side; the difference between them is the whole C2 skill."),
)

THIRD["A1"] = [
    ("gu-a1-u1", "gu-a1-l7", L(
        "તું કે તમે? Choosing the address",
        "Gujarati makes the speaker choose a distance in the first sentence: આપ for elders and "
        "officials, તમે for strangers, neighbours and colleagues, તું at home and with children. "
        "The verb changes with the choice — છો for the first two, છે for તું — so pronoun and verb "
        "have to be picked together.",
        [V("આપ", "aap", "you (respectful)", "pronoun"),
         V("તમે", "tame", "you (polite plural)", "pronoun"),
         V("તું", "tu", "you (familiar)", "pronoun"),
         V("સંબોધન", "sambodhan", "address, form of address", "noun"),
         V("ઉંમર", "ummar", "age", "noun")],
        G("Forms of address",
          "આપ કેમ છો? · તમે ક્યાં રહો છો? · તું ક્યાં જાય છે?",
          "Gujarati verbs agree with the address, not only with the person: આપ કેમ છો? and તમે કેમ છો? "
          "share the છો ending, while તું takes છે — તું ક્યાં જાય છે? Pick the pronoun by age and "
          "relationship, then let the verb follow it.",
          [X("આપ કેમ છો?", "Aap kem chho?", "How are you? (to an elder)"),
           X("તમે ક્યાં રહો છો?", "Tame kyaan raho chho?", "Where do you live?"),
           X("તું શાળામાં જાય છે?", "Tu shaalamaa jaay chhe?", "Do you go to school?")],
          [("તમે કેમ છે?", "તમે કેમ છો?", "તમે takes છો, never છે."),
           ("તું કેમ છો?", "તું કેમ છે?", "The familiar તું takes છે: તું કેમ છે?")]),
        [D("Teacher", "આપ કેમ છો?", "Aap kem chho?", "How are you?"),
         D("Student", "હું મજામાં છું, આભાર. આપ?", "Hun majamaa chhun, aabhaar. Aap?", "I am well, thank you. And you?"),
         D("Teacher", "હું પણ મજામાં. આ તમારો ભાઈ છે?", "Hun pan majamaa. Aa tamaaro bhaai chhe?", "I am well too. Is this your brother?"),
         D("Student", "હા, એ શાળામાં જાય છે.", "Haa, e shaalamaa jaay chhe.", "Yes, he goes to school.")],
        WS("Address worksheet", [
            T("Choose the address.", ["how are you? (to an elder)", "where do you live? (to a stranger)"],
              ["આપ કેમ છો?", "તમે ક્યાં રહો છો?"]),
            T("Switch to the familiar.", ["do you go to school?", "what is your name?"],
              ["તું શાળામાં જાય છે?", "તારું નામ શું છે?"]),
        ]))),
    ("gu-a1-u2", "gu-a1-l8", L(
        "મારું ઘર: અહીં, ત્યાં, પાસે",
        "Place is expressed with postpositions that follow the noun: ઘરની પાસે (near the house), "
        "નદીની બાજુમાં (beside the river), દુકાનની સામે (opposite the shop). The genitive marker "
        "inside them is fixed by usage, and getting it wrong is the commonest A1 slip.",
        [V("અહીં", "aheen", "here", "adverb"),
         V("ત્યાં", "tyaan", "there", "adverb"),
         V("પાસે", "paase", "near, with", "postposition"),
         V("બાજુમાં", "baajumaa", "beside", "postposition"),
         V("સામે", "saame", "opposite, in front of", "postposition")],
        G("Postpositions of place",
          "અહીં છે · ઘરની પાસે · નદીની બાજુમાં · શાળાની સામે",
          "Postpositions follow the noun and take a genitive: ઘરની પાસે, નદીની બાજુમાં, શાળાની સામે. "
          "The location phrase sits before the verb, and the verb closes the sentence — Gujarati "
          "never ends on the place.",
          [X("મારું ઘર અહીં છે.", "Maaru ghar aheen chhe.", "My house is here."),
           X("દુકાન ઘરની પાસે છે.", "Dukaan gharni paase chhe.", "The shop is near the house."),
           X("બગીચો નદીની બાજુમાં છે.", "Bagicho nadeeni baajumaa chhe.", "The garden is beside the river.")],
          [("મારું ઘર નદી બાજુમાં છે.", "મારું ઘર નદીની બાજુમાં છે.", "બાજુમાં takes the genitive: નદીની બાજુમાં."),
           ("દુકાન ઘરનો પાસે છે.", "દુકાન ઘરની પાસે છે.", "The fixed phrase is ઘરની પાસે, whatever the gender of ઘર.")]),
        [D("Neighbour", "તમારું ઘર ક્યાં છે?", "Tamaaru ghar kyaan chhe?", "Where is your house?"),
         D("Mother", "નદીની બાજુમાં, દુકાનની પાસે.", "Nadeeni baajumaa, dukaanni paase.", "Beside the river, near the shop."),
         D("Neighbour", "બગીચો પણ ત્યાં છે?", "Bagicho pan tyaan chhe?", "Is the garden there too?"),
         D("Mother", "હા, બગીચો ઘરની સામે છે.", "Haa, bagicho gharni saame chhe.", "Yes, the garden is opposite the house.")],
        WS("Place worksheet", [
            T("Place the things.", ["my house is here", "the shop is near the house"],
              ["મારું ઘર અહીં છે.", "દુકાન ઘરની પાસે છે."]),
            T("Use the postposition.", ["beside the river", "opposite the school"],
              ["નદીની બાજુમાં", "શાળાની સામે"]),
        ]))),
    ("gu-a1-u3", "gu-a1-l9", L(
        "ઋતુ અને હવામાન: વરસાદ પડે છે",
        "Weather in Gujarati comes with the verb પડે છે: વરસાદ પડે છે, ગરમી પડે છે, ઠંડી પડે છે. The "
        "three seasons — ઉનાળો, ચોમાસું, શિયાળો — take the locative -માં when you say what happens "
        "in them.",
        [V("ઋતુ", "rutu", "season", "noun"),
         V("વરસાદ", "varsaad", "rain", "noun"),
         V("ગરમી", "garmi", "heat", "noun"),
         V("ઠંડી", "thandi", "cold", "noun"),
         V("પવન", "pavan", "wind", "noun")],
        G("Weather and seasons",
          "વરસાદ પડે છે · ઉનાળામાં ગરમી પડે છે · ચોમાસામાં પવન ફૂંકે છે",
          "Rain, heat and cold all fall (પડે છે); wind blows (ફૂંકે છે). Seasons take -માં: ઉનાળામાં, "
          "ચોમાસામાં, શિયાળામાં. ચોમાસું loses its final -ું before the suffix, which is why the "
          "spelling shifts.",
          [X("આજે વરસાદ પડે છે.", "Aaje varsaad pade chhe.", "Today it is raining."),
           X("ઉનાળામાં ગરમી પડે છે.", "Unaalaamaa garmi pade chhe.", "It is hot in summer."),
           X("ચોમાસામાં પવન ફૂંકે છે.", "Chomaasaamaa pavan phoonke chhe.", "The wind blows in the monsoon.")],
          [("આજે વરસાદ છે.", "આજે વરસાદ પડે છે.", "Rain falls: the verb is પડે છે, not છે alone."),
           ("ઉનાળો ગરમી પડે છે.", "ઉનાળામાં ગરમી પડે છે.", "A season takes the locative -માં.")]),
        [D("Brother", "આજે હવામાન કેવું છે?", "Aaje havaamaan kevu chhe?", "What is the weather like today?"),
         D("Sister", "વરસાદ પડે છે, પણ ગરમી છે.", "Varsaad pade chhe, pan garmi chhe.", "It is raining, but it is warm."),
         D("Brother", "ચોમાસું ક્યારે શરૂ થાય છે?", "Chomaasun kyaare sharu thaay chhe?", "When does the monsoon start?"),
         D("Sister", "જૂનમાં, અને શિયાળો નવેમ્બરમાં.", "Joonmaa, ane shiyaalo navembarmaa.", "In June, and winter in November.")],
        WS("Weather worksheet", [
            T("Describe the weather.", ["today it is raining", "it is hot in summer"],
              ["આજે વરસાદ પડે છે.", "ઉનાળામાં ગરમી પડે છે."]),
            T("Name the seasons.", ["in the monsoon", "in winter"],
              ["ચોમાસામાં", "શિયાળામાં"]),
        ]))),
]

THIRD["A2"] = [
    ("gu-a2-u1", "gu-a2-l7", L(
        "ટિકિટ, પ્લેટફોર્મ અને સમય",
        "Ticket talk is three questions: એક ટિકિટ આપો · ટ્રેન કયા પ્લેટફોર્મથી નીકળે છે? · તે કેટલા "
        "વાગ્યે નીકળે છે? Times are said with વાગ્યે, and the fraction comes before the hour: સવા "
        "નવ (9:15), સાડા નવ (9:30), પોણા દસ (9:45).",
        [V("ટિકિટ", "tikit", "ticket", "noun"),
         V("પ્લેટફોર્મ", "platform", "platform", "noun"),
         V("નીકળવું", "neekalvu", "to depart", "verb"),
         V("સવા", "savaa", "quarter past (in time-telling)", "adverb"),
         V("પોણા", "ponaa", "quarter to (in time-telling)", "adverb")],
        G("Station frame",
          "એક ટિકિટ આપો · ટ્રેન કયા પ્લેટફોર્મથી નીકળે છે? · સવા નવ વાગ્યે નીકળે છે",
          "A ticket request is આપો, not a question: એક ટિકિટ આપો. Leaving is નીકળવું with the "
          "ablative -થી: પ્લેટફોર્મથી નીકળે છે. Time takes વાગ્યે, and સવા/સાડા/પોણા stands before "
          "the hour.",
          [X("એક ટિકિટ આપો.", "Ek tikit aapo.", "One ticket, please."),
           X("ટ્રેન કયા પ્લેટફોર્મથી નીકળે છે?", "Tren kyaa platformthi neekale chhe?", "Which platform does the train leave from?"),
           X("ટ્રેન સવા નવ વાગ્યે નીકળે છે.", "Tren savaa nav vaagye neekale chhe.", "The train leaves at quarter past nine.")],
          [("ટ્રેન નવ વાગ્યે નીકળે છે સવા.", "ટ્રેન સવા નવ વાગ્યે નીકળે છે.", "The fraction precedes the hour: સવા નવ."),
           ("મને ટિકિટ જોઈએ છે બે.", "મને બે ટિકિટ જોઈએ છે.", "The number precedes the noun; the verb closes the sentence.")]),
        [D("Newcomer", "એક ટિકિટ આપો.", "Ek tikit aapo.", "One ticket, please."),
         D("Neighbour", "કયા સ્ટેશન સુધી?", "Kyaa steshan sudhi?", "Up to which station?"),
         D("Newcomer", "વડોદરા. ટ્રેન કયા પ્લેટફોર્મથી નીકળે છે?", "Vadodara. Tren kyaa platformthi neekale chhe?", "Vadodara. Which platform does the train leave from?"),
         D("Neighbour", "પ્લેટફોર્મ ત્રણથી, સવા નવ વાગ્યે.", "Platform tranthi, savaa nav vaagye.", "From platform three, at quarter past nine.")],
        WS("Station worksheet", [
            T("Buy the ticket.", ["one ticket, please", "how much does it cost?"],
              ["એક ટિકિટ આપો.", "કેટલાની છે?"]),
            T("Ask about the train.", ["which platform does the train leave from?", "it leaves at quarter past nine"],
              ["ટ્રેન કયા પ્લેટફોર્મથી નીકળે છે?", "સવા નવ વાગ્યે નીકળે છે."]),
        ]))),
    ("gu-a2-u2", "gu-a2-l8", L(
        "દવાખાને: દુખે છે, દવા લો",
        "A symptom is the body part plus દુખે છે: માથું દુખે છે, પેટ દુખે છે, ગળું દુખે છે. The advice "
        "comes back in the imperative: આ દવા લો, બે દિવસ આરામ કરો.",
        [V("દુખવું", "dukhvu", "to hurt, to ache", "verb"),
         V("દવા", "dava", "medicine", "noun"),
         V("આરામ", "aaram", "rest", "noun"),
         V("તપાસ", "tapas", "check-up, examination", "noun"),
         V("ચિઠ્ઠી", "chitthi", "note, prescription", "noun")],
        G("Clinic frame",
          "માથું દુખે છે · બે દિવસથી તાવ છે · આ દવા દિવસમાં બે વાર લો · બે દિવસ આરામ કરો",
          "The ache takes the body part as its subject — માથું દુખે છે, literally 'the head aches' — "
          "and the duration takes -થી: બે દિવસથી. The doctor replies with લો and કરો, and the "
          "frequency sits inside the sentence: દિવસમાં બે વાર.",
          [X("માથું દુખે છે.", "Maathu dukhe chhe.", "I have a headache."),
           X("આ દવા દિવસમાં બે વાર લો.", "Aa davaa divasmaa be vaar lo.", "Take this medicine twice a day."),
           X("બે દિવસ આરામ કરો.", "Be divas aaram karo.", "Rest for two days.")],
          [("મને માથું દુખે છે છે.", "માથું દુખે છે.", "One verb is enough: દુખે છે already carries the ache."),
           ("તમે આરામ કરો બે દિવસ.", "તમે બે દિવસ આરામ કરો.", "A duration comes before the verb.")]),
        [D("Doctor", "તમને શું થયું?", "Tamne shu thayu?", "What happened to you?"),
         D("Patient", "બે દિવસથી માથું દુખે છે.", "Be divasthi maathu dukhe chhe.", "I have had a headache for two days."),
         D("Doctor", "તાવ છે?", "Taav chhe?", "Is there a fever?"),
         D("Patient", "ના, પણ ઊંઘ નથી આવતી.", "Naa, pan oongh nathi aavti.", "No, but I cannot sleep."),
         D("Doctor", "આ દવા લો અને બે દિવસ આરામ કરો.", "Aa davaa lo ane be divas aaram karo.", "Take this medicine and rest for two days.")],
        WS("Clinic worksheet", [
            T("State the symptom.", ["I have a headache", "my stomach hurts"],
              ["માથું દુખે છે.", "પેટ દુખે છે."]),
            T("Repeat the advice.", ["take this medicine twice a day", "rest for two days"],
              ["આ દવા દિવસમાં બે વાર લો.", "બે દિવસ આરામ કરો."]),
        ]))),
    ("gu-a2-u3", "gu-a2-l9", L(
        "કપડાં: સાઇઝ, રંગ, બદલવું",
        "Clothes talk asks three things: આ સાઇઝ નાની છે · બીજો રંગ છે? · બદલી શકાય? The size "
        "adjective agrees with its noun — નાની સાઇઝ, નાનું કમીઝ — and the possibility of exchange "
        "is the passive-looking બદલી શકાય.",
        [V("કપડાં", "kapdaa", "clothes", "noun"),
         V("સાઇઝ", "size", "size", "noun"),
         V("રંગ", "rang", "colour", "noun"),
         V("બદલવું", "badalvu", "to change, to exchange", "verb"),
         V("પરચૂરણ", "parchooran", "change (money), receipt", "noun")],
        G("Clothes frame",
          "આ સાઇઝ નાની છે · બીજો રંગ છે? · બદલી શકાય? · પંદર દિવસમાં",
          "The adjective agrees with the noun it describes: સાઇઝ is feminine (નાની), કમીઝ is neuter "
          "(નાનું). Exchange is expressed with શકાય: બદલી શકાય? — literally 'can it be exchanged?' — "
          "and the window is a plain time phrase: પંદર દિવસમાં.",
          [X("આ સાઇઝ નાની છે.", "Aa size naani chhe.", "This size is small."),
           X("બીજો રંગ છે?", "Beejo rang chhe?", "Is there another colour?"),
           X("બદલી શકાય?", "Badli shakaay?", "Can it be exchanged?")],
          [("આ સાઇઝ નાનું છે.", "આ સાઇઝ નાની છે.", "સાઇઝ is feminine, so the adjective is નાની."),
           ("હું બદલવું છે.", "મારે બદલવું છે.", "Need takes મારે + infinitive, never the bare હું.")]),
        [D("Mother", "આ કમીઝની સાઇઝ નાની છે.", "Aa kameezni size naani chhe.", "The size of this shirt is small."),
         D("Brother", "બીજી સાઇઝ છે, આ લો.", "Beeji size chhe, aa lo.", "There is another size, take this one."),
         D("Mother", "રંગ બદલી શકાય?", "Rang badli shakaay?", "Can the colour be exchanged?"),
         D("Brother", "હા, પરચૂરણ સાથે પંદર દિવસમાં.", "Haa, parchooran saathe pandar divasmaa.", "Yes, with the receipt, within fifteen days.")],
        WS("Clothes worksheet", [
            T("Ask about the clothes.", ["this size is small", "is there another colour?"],
              ["આ સાઇઝ નાની છે.", "બીજો રંગ છે?"]),
            T("Arrange the exchange.", ["can it be exchanged?", "within fifteen days with the receipt"],
              ["બદલી શકાય?", "પરચૂરણ સાથે પંદર દિવસમાં"]),
        ]))),
]

THIRD["B1"] = [
    ("gu-b1-u1", "gu-b1-l7", L(
        "પ્રસંગ કહેવો: પહેલાં, પછી, છેવટે",
        "An anecdote in Gujarati is a chain of signposts: પહેલાં હું સ્ટેશન પહોંચ્યો, પછી ટ્રેન આવી, "
        "અચાનક વીજળી ગઈ, છેવટે અમે ટૅક્સીમાં ઘરે ગયા. The signposts carry the listener; the past "
        "tense carries the time.",
        [V("પ્રસંગ", "prasang", "incident", "noun"),
         V("પહેલાં", "pahelaan", "first, before", "adverb"),
         V("પછી", "pachhi", "then, after", "adverb"),
         V("અચાનક", "achaanak", "suddenly", "adverb"),
         V("છેવટે", "chevate", "finally, in the end", "adverb")],
        G("Anecdote signposts",
          "પહેલાં … · પછી … · અચાનક … · છેવટે …",
          "The four signposts divide the story into moves, and each one takes a finished past: "
          "પહોંચ્યો, આવી, ગઈ, ગયા. The verb agrees with its subject — હું પહોંચ્યો, ટ્રેન આવી, વીજળી "
          "ગઈ, અમે ગયા — so the anecdote also practises agreement.",
          [X("પહેલાં હું સ્ટેશન પહોંચ્યો.", "Pahelaan hun steshan pahonchyo.", "First I reached the station."),
           X("અચાનક વીજળી ગઈ.", "Achaanak veejli gai.", "Suddenly the power went."),
           X("છેવટે અમે ટૅક્સીમાં ઘરે ગયા.", "Chevate ame taxiimaa ghare gayaa.", "In the end we went home by taxi.")],
          [("પહેલાં હું સ્ટેશન પહોંચ્યો, પછી ફરી પહેલાં ટ્રેન આવી.", "પહેલાં હું સ્ટેશન પહોંચ્યો, પછી ટ્રેન આવી.", "One signpost per move of the story."),
           ("છેવટે અમે ઘરે જઈએ છીએ.", "છેવટે અમે ઘરે ગયા.", "A finished anecdote takes the past, not the present.")]),
        [D("Neighbour", "શું થયું હતું?", "Shu thayu hatu?", "What had happened?"),
         D("Newcomer", "પહેલાં હું સ્ટેશન પહોંચ્યો, પછી ટ્રેન આવી.", "Pahelaan hun steshan pahonchyo, pachhi tren aavi.", "First I reached the station, then the train came."),
         D("Neighbour", "અને પછી?", "Ane pachhi?", "And then?"),
         D("Newcomer", "અચાનક વીજળી ગઈ; છેવટે અમે ટૅક્સીમાં ઘરે ગયા.", "Achaanak veejli gai; chevate ame taxiimaa ghare gayaa.", "Suddenly the power went; in the end we went home by taxi.")],
        WS("Anecdote worksheet", [
            T("Chain the story.", ["first I reached the station", "suddenly the power went", "in the end we went home"],
              ["પહેલાં હું સ્ટેશન પહોંચ્યો.", "અચાનક વીજળી ગઈ.", "છેવટે અમે ઘરે ગયા."]),
            T("Order the signposts.", ["first", "then", "finally"],
              ["પહેલાં", "પછી", "છેવટે"]),
        ]))),
    ("gu-b1-u2", "gu-b1-l8", L(
        "સમજાવવું: એટલે શું? ઉદાહરણ તરીકે",
        "Explanation has three moves in Gujarati: એટલે શું? (what does it mean?), ઉદાહરણ તરીકે (for "
        "example), ટૂંકમાં કહું તો (if I put it briefly). Naming the move makes an explanation "
        "followable even when half the words are new.",
        [V("સમજાવવું", "samjaavvu", "to explain", "verb"),
         V("અર્થ", "arth", "meaning", "noun"),
         V("ઉદાહરણ", "udaaharan", "example", "noun"),
         V("ટૂંકમાં", "tunkmaa", "in short", "adverb"),
         V("ફરી", "fari", "again", "adverb")],
        G("Explanation frame",
          "એટલે શું? · ઉદાહરણ તરીકે, … · ટૂંકમાં કહું તો …",
          "એટલે marks a definition — «મુલાકાત» એટલે મળવું. ઉદાહરણ તરીકે introduces the instance, and "
          "ટૂંકમાં કહું તો announces the summary. The three moves can be used in any order, but each "
          "one is announced before it arrives.",
          [X("એટલે શું?", "Etle shu?", "What does it mean?"),
           X("ઉદાહરણ તરીકે, ટ્રેન લેટ છે.", "Udaaharan tarike, tren late chhe.", "For example, the train is late."),
           X("ટૂંકમાં કહું તો, સમય નથી.", "Tunkmaa kahun to, samay nathi.", "In short, there is no time.")],
          [("ઉદાહરણ તરીકે માટે, ટ્રેન લેટ છે.", "ઉદાહરણ તરીકે, ટ્રેન લેટ છે.", "તરીકે needs no માટે."),
           ("ટૂંકમાં કહું તો કે સમય નથી.", "ટૂંકમાં કહું તો સમય નથી.", "તો already announces the conclusion; no કે after it.")]),
        [D("Student", "«મુલાકાત» એટલે શું?", "«Mulakaat» etle shu?", "What does 'mulakaat' mean?"),
         D("Teacher", "એટલે મળવું. ઉદાહરણ તરીકે: આવતીકાલે મુલાકાત છે.", "Etle malvun. Udaaharan tarike: aavtikale mulakaat chhe.", "It means meeting. For example: tomorrow there is a meeting."),
         D("Student", "ટૂંકમાં?", "Tunkmaa?", "In short?"),
         D("Teacher", "ટૂંકમાં કહું તો: બે વ્યક્તિ મળે, તે મુલાકાત.", "Tunkmaa kahun to: be vyakti male, te mulakaat.", "In short: two people meet, that is a meeting.")],
        WS("Explanation worksheet", [
            T("Explain the word.", ["what does it mean?", "it means meeting"],
              ["એટલે શું?", "એટલે મળવું."]),
            T("Give the example and the summary.", ["for example, the train is late", "in short, there is no time"],
              ["ઉદાહરણ તરીકે, ટ્રેન લેટ છે.", "ટૂંકમાં કહું તો, સમય નથી."]),
        ]))),
    ("gu-b1-u3", "gu-b1-l9", L(
        "મુલાકાત નક્કી કરવી: બદલવી, રદ કરવી",
        "A meeting is fixed with નક્કી કરીએ? and moved or cancelled with પડશે: સમય બદલવો પડશે, "
        "મુલાકાત રદ કરવી પડશે. The politeness lives in the modal, so no apology has to be invented.",
        [V("મુલાકાત", "mulakaat", "meeting, visit", "noun"),
         V("નક્કી કરવું", "nakki karvu", "to fix, to decide", "phrase"),
         V("બદલવું", "badalvu", "to change, to move", "verb"),
         V("રદ કરવું", "rad karvu", "to cancel", "phrase"),
         V("સમય", "samay", "time", "noun")],
        G("Appointment frame",
          "મુલાકાત નક્કી કરીએ? · સમય બદલવો પડશે · મુલાકાત રદ કરવી પડશે",
          "The suggestion is a bare કરીએ? — no છે. The unavoidable change takes પડશે with the "
          "infinitive agreeing with its noun: સમય બદલવો પડશે (masculine), મુલાકાત રદ કરવી પડશે "
          "(feminine). Agreement is the whole lesson.",
          [X("આવતા મંગળવારે મુલાકાત નક્કી કરીએ?", "Aavtaa mangalvaare mulakaat nakki karie?", "Shall we fix a meeting next Tuesday?"),
           X("સમય બદલવો પડશે.", "Samay badalvo padshe.", "The time will have to change."),
           X("મુલાકાત રદ કરવી પડશે.", "Mulakaat rad karvi padshe.", "The meeting will have to be cancelled.")],
          [("મુલાકાત રદ કરવો પડશે.", "મુલાકાત રદ કરવી પડશે.", "મુલાકાત is feminine, so the infinitive is કરવી."),
           ("મુલાકાત નક્કી કરીએ છે?", "મુલાકાત નક્કી કરીએ?", "A suggestion is કરીએ?, with no છે.")]),
        [D("Manager", "આવતા મંગળવારે મુલાકાત નક્કી કરીએ?", "Aavtaa mangalvaare mulakaat nakki karie?", "Shall we fix a meeting next Tuesday?"),
         D("Neighbour", "મંગળવારે નહીં — સમય બદલવો પડશે.", "Mangalvaare nahi — samay badalvo padshe.", "Not Tuesday — the time will have to change."),
         D("Manager", "તો બુધવારે?", "To budhvaare?", "Then Wednesday?"),
         D("Neighbour", "બુધવારે ઠીક છે; મુલાકાત નક્કી કરીએ.", "Budhvaare theek chhe; mulakaat nakki karie.", "Wednesday is fine; let us fix the meeting.")],
        WS("Appointment worksheet", [
            T("Fix and move the meeting.", ["shall we fix a meeting?", "the time will have to change"],
              ["મુલાકાત નક્કી કરીએ?", "સમય બદલવો પડશે."]),
            T("Cancel with the modal.", ["the meeting will have to be cancelled", "Wednesday is fine"],
              ["મુલાકાત રદ કરવી પડશે.", "બુધવારે ઠીક છે."]),
        ]))),
]

THIRD["B2"] = [
    ("gu-b2-u1", "gu-b2-l7", L(
        "આંકડા અને દલીલ: ટકા, વધારો, ઘટાડો",
        "An argument with numbers in Gujarati puts the figure first and the change after: વેચાણ ગયા "
        "વર્ષ કરતાં દોઢ ગણું થયું · ભાવમાં બે ટકાનો ઘટાડો થયો · સરેરાશ વીસ હજાર રહી. The comparison "
        "takes કરતાં, the change takes નો/ની.",
        [V("આંકડો", "aankdo", "figure, number", "noun"),
         V("ટકા", "taka", "per cent", "noun"),
         V("વધારો", "vadhaaro", "increase", "noun"),
         V("ઘટાડો", "ghataado", "decrease, fall", "noun"),
         V("સરેરાશ", "sareraash", "average", "noun")],
        G("Figures and change",
          "દોઢ ગણું થયું · બે ટકાનો ઘટાડો થયો · સરેરાશ વીસ હજાર રહી",
          "The thing measured takes -માં, the change takes the genitive: ભાવમાં બે ટકાનો ઘટાડો થયો. "
          "A completed change takes થયું/થયો, and a comparison takes કરતાં after the thing compared "
          "with.",
          [X("વેચાણ દોઢ ગણું થયું.", "Vechaan dodh ganu thayu.", "Sales became one and a half times."),
           X("ભાવમાં બે ટકાનો ઘટાડો થયો.", "Bhaavmaa be takaa-no ghataado thayo.", "There was a two per cent fall in the price."),
           X("સરેરાશ વીસ હજાર રહી.", "Sareraash vees hajaar rahi.", "The average stayed at twenty thousand.")],
          [("ભાવ બે ટકા ઘટાડો થયો.", "ભાવમાં બે ટકાનો ઘટાડો થયો.", "The measured noun takes -માં and the change takes -નો."),
           ("વેચાણ ગયા વર્ષ કરતાં દોઢ ગણું વધારે છે.", "વેચાણ ગયા વર્ષ કરતાં દોઢ ગણું થયું.", "A completed change takes થયું, not the present.")]),
        [D("Manager", "વેચાણ કેવું રહ્યું?", "Vechaan kevu rahyu?", "How were the sales?"),
         D("Newcomer", "ગયા વર્ષ કરતાં દોઢ ગણું.", "Gayaa varsh kartaan dodh ganu.", "One and a half times last year."),
         D("Manager", "અને ભાવ?", "Ane bhaav?", "And the price?"),
         D("Newcomer", "ભાવમાં બે ટકાનો ઘટાડો થયો; સરેરાશ વીસ હજાર રહી.", "Bhaavmaa be takaa-no ghataado thayo; sareraash vees hajaar rahi.", "The price fell two per cent; the average stayed at twenty thousand.")],
        WS("Figures worksheet", [
            T("Read the figures.", ["sales became one and a half times", "a two per cent fall in the price"],
              ["વેચાણ દોઢ ગણું થયું.", "ભાવમાં બે ટકાનો ઘટાડો થયો."]),
            T("State the comparison.", ["compared with last year", "the average stayed at twenty thousand"],
              ["ગયા વર્ષ કરતાં", "સરેરાશ વીસ હજાર રહી"]),
        ]))),
    ("gu-b2-u2", "gu-b2-l8", L(
        "સત્તાવાર પત્ર: વિષય, સંબોધન, સમાપન",
        "A formal Gujarati letter has fixed furniture: the salutation (આદરણીય શ્રીમાન …), the "
        "subject line (વિષય: …), the request (આપની વિનંતી છે કે …) and the closing (આભાર સહ). "
        "Nothing is improvised, and that is what makes it read as competent.",
        [V("વિષય", "vishay", "subject (of a letter)", "noun"),
         V("સંબોધન", "sambodhan", "salutation", "noun"),
         V("સમાપન", "samaapan", "closing", "noun"),
         V("વિનંતી", "vinanti", "request", "noun"),
         V("સંદર્ભ", "sandarbh", "reference", "noun")],
        G("Formal letter frame",
          "આદરણીય શ્રીમાન, · વિષય: … · આપની વિનંતી છે કે … · આભાર સહ",
          "The subject line is a noun phrase with no verb (વિષય: રજા માટે વિનંતી), the request is "
          "impersonal (આપની વિનંતી છે કે …), and the closing is fixed (આભાર સહ / નમ્ર વિનંતી). Four "
          "lines carry the whole letter.",
          [X("વિષય: રજા માટે વિનંતી.", "Vishay: rajaa maate vinanti.", "Subject: request for leave."),
           X("આપની વિનંતી છે કે મને ત્રણ દિવસની રજા મંજૂર કરવામાં આવે.", "Aapni vinanti chhe ke mane tran divasni rajaa manjoor karvaamaa aave.", "I request that I be granted three days' leave."),
           X("આભાર સહ,", "Aabhaar sah,", "With thanks,")],
          [("વિષય: રજા માટે વિનંતી છે.", "વિષય: રજા માટે વિનંતી.", "A subject line is a noun phrase: no છે."),
           ("હાય શ્રીમાન,", "આદરણીય શ્રીમાન,", "A formal salutation is આદરણીય શ્રીમાન.")]),
        [D("Newcomer", "પત્ર કેમ શરૂ કરું?", "Patra kem sharu karun?", "How do I start the letter?"),
         D("Manager", "«આદરણીય શ્રીમાન», પછી વિષય.", "«Aadarneey shreemaan», pachhi vishay.", "'Respected Sir', then the subject."),
         D("Newcomer", "અને વિનંતી?", "Ane vinanti?", "And the request?"),
         D("Manager", "«આપની વિનંતી છે કે …», અને અંતે «આભાર સહ».", "«Aapni vinanti chhe ke …», ane ante «aabhaar sah».", "'I request that …', and at the end 'with thanks'.")],
        WS("Letter worksheet", [
            T("Open the letter.", ["respected Sir", "subject: request for leave"],
              ["આદરણીય શ્રીમાન,", "વિષય: રજા માટે વિનંતી."]),
            T("Make the request and close.", ["I request that I be granted three days' leave", "with thanks"],
              ["આપની વિનંતી છે કે મને ત્રણ દિવસની રજા મંજૂર કરવામાં આવે.", "આભાર સહ"]),
        ]))),
    ("gu-b2-u3", "gu-b2-l9", L(
        "સમાચાર વાંચવા: મથાળું અને અહેવાલ",
        "A Gujarati headline piles words (ભાવમાં ઘટાડો) while the report builds a sentence with a "
        "figure, a period and a source (ગયા મહિને ભાવ બે ટકા ઘટ્યો, અહેવાલ અનુસાર). Reading the "
        "news here means asking what the headline left out.",
        [V("મથાળું", "mathaalu", "headline", "noun"),
         V("અહેવાલ", "ahevaal", "report", "noun"),
         V("સ્રોત", "srot", "source", "noun"),
         V("ત્રિમાસ", "trimaas", "quarter (of a year)", "noun"),
         V("સરખામણી", "sarkhaamani", "comparison", "noun")],
        G("Headline and report",
          "મથાળું: ભાવમાં ઘટાડો · અહેવાલ: ગયા મહિને ભાવ બે ટકા ઘટ્યો · સ્રોત અનુસાર",
          "The headline names a direction; the report measures it. A report sentence carries three "
          "things — the period (ગયા મહિને), the figure (બે ટકા) and the source (સ્રોત અનુસાર) — and "
          "a cause belongs in a separate sentence, not in the same one.",
          [X("મથાળું: ભાવમાં ઘટાડો.", "Mathaalu: bhaavmaa ghataado.", "Headline: fall in prices."),
           X("અહેવાલ: ગયા મહિને ભાવ બે ટકા ઘટ્યો.", "Ahevaal: gayaa mahine bhaav be takaa ghatyo.", "Report: last month the price fell two per cent."),
           X("સ્રોત અનુસાર, આંકડો ત્રીજા ત્રિમાસનો છે.", "Srot anusaar, aankdo treejaa trimaasno chhe.", "According to the source, the figure is from the third quarter.")],
          [("મથાળું અને અહેવાલ એક જ વાત કહે છે.", "મથાળું દિશા બતાવે છે, અહેવાલ માપ આપે છે.", "The headline gives the direction; only the report gives the measurement."),
           ("ભાવ ઘટ્યો, કારણ કે સરકારે નિર્ણય લીધો.", "ગયા મહિને ભાવ બે ટકા ઘટ્યો.", "A report sentence states figure, period and source; the cause is a different sentence.")]),
        [D("Student", "મથાળું શું કહે છે?", "Mathaalu shu kahe chhe?", "What does the headline say?"),
         D("Teacher", "«ભાવમાં ઘટાડો» — દિશા.", "«Bhaavmaa ghataado» — dishaa.", "'Fall in prices' — a direction."),
         D("Student", "અને અહેવાલ?", "Ane ahevaal?", "And the report?"),
         D("Teacher", "ગયા મહિને ભાવ બે ટકા ઘટ્યો, સ્રોત અનુસાર.", "Gayaa mahine bhaav be takaa ghatyo, srot anusaar.", "Last month the price fell two per cent, according to the source.")],
        WS("News worksheet", [
            T("Turn the headline into a report sentence.", ["fall in prices", "rise in sales"],
              ["ગયા મહિને ભાવ બે ટકા ઘટ્યો.", "ગયા ત્રિમાસમાં વેચાણ દોઢ ગણું થયું."]),
            T("Turn the report into a headline.", ["the price fell two per cent last month", "sales doubled"],
              ["ભાવમાં ઘટાડો.", "વેચાણમાં વધારો."]),
        ]))),
]

THIRD["C1"] = [
    ("gu-c1-u1", "gu-c1-l7", L(
        "સ્રોત અને દાવો: «કહેવાય છે», «જણાવાયું છે»",
        "Attribution in Gujarati can be impersonal: કહેવાય છે કે (it is said that), જણાવાયું છે કે "
        "(it is stated that), સ્રોત અનુસાર (according to the source). The impersonal files the claim "
        "under someone else's name — which is exactly why it has to be read carefully.",
        [V("સ્રોત", "srot", "source", "noun"),
         V("દાવો", "daavo", "claim", "noun"),
         V("કહેવાય છે", "kahevaay chhe", "it is said", "phrase"),
         V("જણાવાયું છે", "janavaayun chhe", "it is stated", "phrase"),
         V("અનુસાર", "anusaar", "according to", "postposition")],
        G("Attribution frame",
          "કહેવાય છે કે … · જણાવાયું છે કે … · સ્રોત અનુસાર · ચકાસવું પડશે",
          "કહેવાય છે and જણાવાયું છે take a કે-clause; અનુસાર takes a noun phrase (સ્રોત અનુસાર, "
          "અહેવાલ અનુસાર). To attribute and stay honest, add what is still missing: ચકાસવું પડશે "
          "(it will have to be checked).",
          [X("કહેવાય છે કે ભાવ વધશે.", "Kahevaay chhe ke bhaav vadhashe.", "It is said that prices will rise."),
           X("અહેવાલમાં જણાવાયું છે કે યોજના ચાલુ રહેશે.", "Ahevaalmaa janavaayun chhe ke yojanaa chaalu raheshe.", "The report states that the plan will continue."),
           X("સ્રોત અનુસાર, આંકડો અધૂરો છે.", "Srot anusaar, aankdo adhuro chhe.", "According to the source, the figure is incomplete.")],
          [("સ્રોત અનુસાર કે આંકડો ખોટો છે.", "સ્રોત અનુસાર, આંકડો ખોટો છે.", "અનુસાર takes a noun phrase, not a કે-clause."),
           ("કહેવાય છે કે ભાવ વધશે, એટલે સાચું છે.", "કહેવાય છે કે ભાવ વધશે; ચકાસવું પડશે.", "An attributed claim is not yet verified.")]),
        [D("Analyst", "આંકડો ક્યાંથી આવ્યો?", "Aankdo kyaanthi aavyo?", "Where did the figure come from?"),
         D("Editor", "સ્રોત અનુસાર, ત્રીજા ત્રિમાસનો છે.", "Srot anusaar, treejaa trimaasno chhe.", "According to the source, it is from the third quarter."),
         D("Analyst", "અને બાકી?", "Ane baaki?", "And the rest?"),
         D("Editor", "જણાવાયું છે કે પદ્ધતિ ખુલ્લી નથી; ચકાસવું પડશે.", "Janavaayun chhe ke paddhati khulli nathi; chakaasvun padshe.", "It is stated that the method is not public; it will have to be checked.")],
        WS("Attribution worksheet", [
            T("Attribute the claim.", ["it is said that prices will rise", "the report states that the plan continues"],
              ["કહેવાય છે કે ભાવ વધશે.", "અહેવાલમાં જણાવાયું છે કે યોજના ચાલુ રહેશે."]),
            T("Mark what is missing.", ["according to the source, the figure is incomplete", "it will have to be checked"],
              ["સ્રોત અનુસાર, આંકડો અધૂરો છે.", "ચકાસવું પડશે."]),
        ]))),
    ("gu-c1-u2", "gu-c1-l8", L(
        "કારણની શ્રેણી: કારણ, ફાળો, સંબંધ",
        "Graded causality separates three different claims: આ તેનું કારણ છે (this is its cause), આ "
        "તેમાં ફાળો આપે છે (this contributes to it), બંને વચ્ચે સંબંધ છે (there is a relation between "
        "the two). A report that mixes them up is wrong even when every number in it is right.",
        [V("કારણ", "kaaran", "cause", "noun"),
         V("ફાળો", "phaalo", "contribution, share", "noun"),
         V("સંબંધ", "sambandh", "relation", "noun"),
         V("પરિણામ", "parinaam", "result", "noun"),
         V("સંભાવના", "sambhaavna", "possibility", "noun")],
        G("Graded causality",
          "કારણ છે · ફાળો આપે છે · સંબંધ છે · પરિણામે · સંભવ છે કે",
          "ફાળો આપે છે marks a partial cause, પરિણામે marks a consequence and સંભવ છે કે marks a "
          "likelihood. Writing «વરસાદે ભાવ વધવામાં ફાળો આપ્યો» instead of «વરસાદ જ કારણ છે» is the "
          "difference between a report and a claim.",
          [X("વરસાદે ભાવમાં ફાળો આપ્યો.", "Varsaade bhaavmaa phaalo aapyo.", "The rain contributed to the price."),
           X("પરિણામે, ખરીદી ઘટી.", "Parinaame, khareedi ghati.", "As a result, buying fell."),
           X("સંભવ છે કે આગળ ભાવ વધે.", "Sambhav chhe ke aagal bhaav vadhe.", "It is possible that prices will rise further.")],
          [("વરસાદ જ ભાવ વધવાનું કારણ છે.", "વરસાદે ભાવ વધવામાં ફાળો આપ્યો.", "One contributing factor is not the sole cause."),
           ("બંને વચ્ચે સંબંધ છે, એટલે એક બીજાનું કારણ છે.", "બંને વચ્ચે સંબંધ છે.", "A relation is not a cause; the report says only what it measured.")]),
        [D("Reviewer", "ભાવ કેમ વધ્યો?", "Bhaav kem vadhyo?", "Why did the price rise?"),
         D("Analyst", "વરસાદે ફાળો આપ્યો, પણ એ જ કારણ નથી.", "Varsaade phaalo aapyo, pan e ja kaaran nathi.", "The rain contributed, but it is not the only cause."),
         D("Reviewer", "તો શું લખીએ?", "To shu lakhie?", "Then what do we write?"),
         D("Analyst", "«ફાળો આપ્યો» અને «સંભવ છે કે આગળ વધે».", "«Phaalo aapyo» ane «sambhav chhe ke aagal vadhe».", "'Contributed' and 'it is possible that it will rise further'.")],
        WS("Causality worksheet", [
            T("Grade the claim.", ["the rain contributed to the price", "as a result, buying fell"],
              ["વરસાદે ભાવમાં ફાળો આપ્યો.", "પરિણામે, ખરીદી ઘટી."]),
            T("Keep the distance.", ["it is possible that prices will rise further", "there is a relation between the two"],
              ["સંભવ છે કે આગળ ભાવ વધે.", "બંને વચ્ચે સંબંધ છે."]),
        ]))),
    ("gu-c1-u3", "gu-c1-l9", L(
        "બે સ્રોતનો સાર એક ફકરામાં",
        "A synthesis names the agreement before the difference: બંને સ્રોત એક વાતે સહમત છે — ખર્ચ "
        "વધે છે. તફાવત એ છે કે એક સ્રોત સમય ઓછો આંકે છે, બીજો વધુ. One paragraph, two voices, and "
        "one difference the reader can act on.",
        [V("સાર", "saar", "summary", "noun"),
         V("ફકરો", "fakro", "paragraph", "noun"),
         V("સહમતી", "sahmati", "agreement", "noun"),
         V("તફાવત", "tafaavat", "difference", "noun"),
         V("નિર્ભર", "nirbhar", "dependent", "adjective")],
        G("Synthesis frame",
          "બંને સ્રોત એક વાતે સહમત છે · તફાવત એ છે કે … · સારમાં, …",
          "The first sentence carries what both texts say, the second carries the single point where "
          "they part, and the third says what the decision now depends on (નિર્ભર છે). A synthesis "
          "that lists both texts one after another is not a synthesis — it is two summaries.",
          [X("બંને સ્રોત એક વાતે સહમત છે.", "Banne srot ek vaate sahmat chhe.", "Both sources agree on one thing."),
           X("તફાવત એ છે કે એક સ્રોત સમય ઓછો આંકે છે.", "Tafaavat e chhe ke ek srot samay ochho aanke chhe.", "The difference is that one source estimates less time."),
           X("સારમાં, નિર્ણય પ્રયોગ પર નિર્ભર છે.", "Saarmaa, nirnay prayog par nirbhar chhe.", "In summary, the decision depends on the trial.")],
          [("સાર: બંને સ્રોત સાચા છે.", "સાર: બંને સ્રોત એક વાતે સહમત છે, બીજી વાતે નહીં.", "A synthesis states the point of agreement and the point of difference."),
           ("તફાવત એ છે કે મને પહેલો સ્રોત ગમે છે.", "તફાવત એ છે કે એક સ્રોત સમય ઓછો આંકે છે.", "The difference is between the texts, not between your preferences.")]),
        [D("Mediator", "બે અહેવાલ વાંચ્યા?", "Be ahevaal vaanchyaa?", "Have you read both reports?"),
         D("Reviewer", "હા. બંને એક વાતે સહમત છે: ખર્ચ વધશે.", "Haa. Banne ek vaate sahmat chhe: kharch vadhashe.", "Yes. Both agree on one thing: the cost will rise."),
         D("Mediator", "અને તફાવત?", "Ane tafaavat?", "And the difference?"),
         D("Reviewer", "સમયમાં: એક સ્રોત ત્રણ મહિના કહે છે, બીજો છ.", "Samaymaa: ek srot tran mahinaa kahe chhe, beejo chha.", "In the timing: one source says three months, the other six.")],
        WS("Synthesis worksheet", [
            T("Name the agreement.", ["both sources agree on one thing", "the cost will rise"],
              ["બંને સ્રોત એક વાતે સહમત છે.", "ખર્ચ વધશે."]),
            T("Name the difference and the stake.", ["the difference is in the timing", "the decision depends on the trial"],
              ["તફાવત સમયમાં છે.", "નિર્ણય પ્રયોગ પર નિર્ભર છે."]),
        ]))),
]

THIRD["C2"] = [
    ("gu-c2-u1", "gu-c2-l7", L(
        "અનુકથન: બે અવાજ એક વાક્યમાં",
        "Free indirect discourse lets a character's words into the narration with no quotation "
        "marks: the tense stays with the narrator, while the questions and exclamations belong to "
        "the character — «મોડું આવશે, એ જાણતો હતો. કેમ ફોન ન કર્યો? કેવો મૂર્ખ હતો!»",
        [V("અનુકથન", "anukathan", "retelling, reported speech", "noun"),
         V("અવાજ", "avaaj", "voice", "noun"),
         V("વિચાર", "vichaar", "thought", "noun"),
         V("ઉદ્ગાર", "udgaar", "exclamation", "noun"),
         V("કથન", "kathan", "narration, statement", "noun")],
        G("Free indirect frame",
          "મોડું આવશે, એ જાણતો હતો · કેમ ફોન ન કર્યો? · કેવો મૂર્ખ હતો!",
          "No reporting verb, no colon: the modality and the exclamation carry the voice, while the "
          "tenses stay inside the narration (હતો, કર્યો). The reader hears two voices in one sentence "
          "and has to decide which one is speaking.",
          [X("મોડું આવશે, એ જાણતો હતો.", "Modun aavshe, e jaanato hato.", "He would arrive late, he knew it."),
           X("કેમ ફોન ન કર્યો?", "Kem fon na karyo?", "Why had he not called?"),
           X("કેવો મૂર્ખ હતો!", "Kevo moorkh hato!", "What a fool he was!")],
          [("તેણે કહ્યું: મોડું આવશે.", "મોડું આવશે, એ જાણતો હતો.", "Free indirect discourse drops the reporting verb and the colon."),
           ("કેમ ફોન ન કરે છે? (inside a past narration)", "કેમ ફોન ન કર્યો?", "The character's question keeps the narration's tense.")]),
        [D("Editor", "અવાજ કેમ લાવવો, અવતરણ વગર?", "Avaaj kem laavvo, avtaran vagar?", "How do you bring in the voice without quotation marks?"),
         D("Mediator", "ક્રિયાપદ અને ઉદ્ગારથી: «મોડું આવશે, એ જાણતો હતો».", "Kriyaapad ane udgaarthi: «Modun aavshe, e jaanato hato».", "With verb mood and exclamation: 'he would arrive late, he knew it'."),
         D("Editor", "અને પ્રશ્ન?", "Ane prashn?", "And the question?"),
         D("Mediator", "પાત્રનો રહે, પણ કથનના ભૂતકાળમાં: «કેમ ફોન ન કર્યો?»", "Paatrano rahe, pan kathanna bhootkaalmaa: «Kem fon na karyo?»", "It stays the character's, but in the narration's past: 'why had he not called?'.")],
        WS("Voice worksheet", [
            T("Move the voice inside.", ["he would arrive late, he knew it", "what a fool he was"],
              ["મોડું આવશે, એ જાણતો હતો.", "કેવો મૂર્ખ હતો!"]),
            T("Keep the narration's tense.", ["why had he not called?", "where would he sleep?"],
              ["કેમ ફોન ન કર્યો?", "ક્યાં સૂઈ જાત?"]),
        ]))),
    ("gu-c2-u2", "gu-c2-l8", L(
        "કાનૂની ચોકસાઈ: «અનુસાર», «શરતે»",
        "Legal Gujarati names its own machinery: કલમ ૫ અનુસાર (under clause 5), શરતે કે (on condition "
        "that), અધિકાર સુરક્ષિત રહે (the right remains protected). Each formula points at a norm or "
        "protects a right, and swapping one for another changes the obligation.",
        [V("કલમ", "kalam", "clause", "noun"),
         V("અનુસાર", "anusaar", "under, in accordance with", "postposition"),
         V("શરતે", "sharte", "on condition", "postposition"),
         V("અધિકાર", "adhikaar", "right", "noun"),
         V("મુદત", "mudat", "term, deadline", "noun")],
        G("Normative frame",
          "કલમ ૫ અનુસાર · શરતે કે … · અધિકાર સુરક્ષિત રહે · મુદત ત્રીસ દિવસ",
          "અનુસાર takes the norm (કલમ ૫ અનુસાર), શરતે takes a કે-clause and states what must happen "
          "first, and the protected right is named rather than implied. A clause without its term is "
          "not yet an obligation.",
          [X("કલમ ૫ અનુસાર, મુદત ત્રીસ દિવસ છે.", "Kalam 5 anusaar, mudat trees divas chhe.", "Under clause 5, the term is thirty days."),
           X("શરતે કે તપાસ પહેલાં થાય.", "Sharte ke tapas pahelaan thaay.", "On condition that the check happens first."),
           X("અધિકાર સુરક્ષિત રહે છે.", "Adhikaar surakshit rahe chhe.", "The right remains protected.")],
          [("કલમ ૫ પ્રમાણે શક્ય છે.", "કલમ ૫ અનુસાર, મુદત ત્રીસ દિવસ છે.", "A norm cites its clause and states the term; it does not say 'possible'."),
           ("અધિકાર સુરક્ષિત છે, પણ શરતે.", "અધિકાર શરતે સુરક્ષિત છે.", "The condition attaches to the protected thing, not to the end of the sentence.")]),
        [D("Reviewer", "કલમ શું કહે છે?", "Kalam shu kahe chhe?", "What does the clause say?"),
         D("Analyst", "«કલમ ૫ અનુસાર, મુદત ત્રીસ દિવસ».", "«Kalam 5 anusaar, mudat trees divas».", "'Under clause 5, the term is thirty days.'"),
         D("Reviewer", "અને અધિકાર?", "Ane adhikaar?", "And the right?"),
         D("Analyst", "«અધિકાર સુરક્ષિત રહે», શરતે કે નોંધ પહેલાં આવે.", "«Adhikaar surakshit rahe», sharte ke nondh pahelaan aave.", "'The right remains protected', on condition that the note comes first.")],
        WS("Normative worksheet", [
            T("Cite the norm.", ["under clause 5", "the term is thirty days"],
              ["કલમ ૫ અનુસાર", "મુદત ત્રીસ દિવસ છે"]),
            T("Protect the right.", ["the right remains protected", "on condition that the check happens first"],
              ["અધિકાર સુરક્ષિત રહે છે.", "શરતે કે તપાસ પહેલાં થાય."]),
        ]))),
    ("gu-c2-u3", "gu-c2-l9", L(
        "મધ્યસ્થતા: જ્યારે શબ્દ પકડ ન આપે",
        "Mediation does two things at once: it makes the text usable (સરળ શબ્દોમાં: યોજના "
        "જાન્યુઆરીથી લાગુ થશે) and it records the loss (નોંધ: મૂળમાં «અમલીકરણ» છે, અહીં «લાગુ કરવું»). "
        "Accessibility with no note is not mediation; it is rewriting.",
        [V("મધ્યસ્થતા", "madhyasthata", "mediation", "noun"),
         V("ભાષાંતર", "bhaashaantar", "translation", "noun"),
         V("અર્થઘટન", "arthaghatan", "interpretation", "noun"),
         V("પસંદગી", "pasandgi", "choice", "noun"),
         V("નોંધ", "nondh", "note", "noun")],
        G("Mediation frame",
          "સરળ શબ્દોમાં: … · મૂળમાં «…» છે, અહીં «…» · નોંધમાં જણાવ્યું કે …",
          "The plain version and the record travel together: the first sentence carries the content, "
          "the second names the original word, and the note says what narrowed (અર્થ સાંકડો થાય છે). "
          "A mediator who reports no loss has not noticed one.",
          [X("સરળ શબ્દોમાં: યોજના જાન્યુઆરીથી લાગુ થશે.", "Saral shabdomaa: yojanaa jaanyuaarithi laagu thashe.", "In plain words: the plan applies from January."),
           X("મૂળમાં «અમલીકરણ» છે, અહીં «લાગુ કરવું».", "Moolmaa «amalikaran» chhe, aheen «laagu karvun».", "The original has 'implementation', here 'applying'."),
           X("નોંધમાં જણાવ્યું કે અર્થ સાંકડો થાય છે.", "Nondhmaa janavyun ke arth saankdo thaay chhe.", "The note says the meaning narrows.")],
          [("સરળ શબ્દોમાં અમલીકરણ થશે.", "સરળ શબ્દોમાં: યોજના લાગુ થશે.", "Plain words mean plain: no residual jargon in the same sentence."),
           ("બધું ભાષાંતર થઈ ગયું, કંઈ ખોવાયું નથી.", "ભાષાંતર સાથે નોંધ પણ જોઈએ: થોડો અર્થ સાંકડો થાય છે.", "Mediation records the loss instead of denying it.")]),
        [D("Mediator", "ગ્રાહકને સરળ ગુજરાતી જોઈએ.", "Graahakne saral Gujarati joie.", "The client wants plain Gujarati."),
         D("Editor", "તો «અમલીકરણ» કાઢી નાખીએ.", "To «amalikaran» kaadhi naakhie.", "Then let us drop 'implementation'."),
         D("Mediator", "હા, અને નોંધમાં લખીએ કે મૂળ શબ્દ બીજો છે.", "Haa, ane nondhmaa lakhie ke mool shabd beejo chhe.", "Yes, and let us write in a note that the original word is different."),
         D("Editor", "સરળ, પણ ખોટ દેખાય એવું.", "Saral, pan khot dekhaay evun.", "Plain, but with the loss visible.")],
        WS("Mediation worksheet", [
            T("Make it usable.", ["in plain words: the plan applies from January", "the original has 'implementation'"],
              ["સરળ શબ્દોમાં: યોજના જાન્યુઆરીથી લાગુ થશે.", "મૂળમાં «અમલીકરણ» છે."]),
            T("Record the loss.", ["the note says the meaning narrows", "a note is needed with the translation"],
              ["નોંધમાં જણાવ્યું કે અર્થ સાંકડો થાય છે.", "ભાષાંતર સાથે નોંધ જોઈએ."]),
        ]))),
]

HALFSTEPS["A1+"] = {
    "title": "Gujarati A1+ — Getting around",
    "native": NATIVE,
    "goals": [
        "Ask the way, buy a ticket and name a landmark",
        "Tell the time and arrange to meet — or move the time",
        "Ask for a repair when the language runs past you",
    ],
    "units": [
        {"id": "A1+-U1", "title": "શહેરમાં", "lessons": [
            L("સીધા જાઓ, પછી ડાબે: રસ્તો પૂછવો",
              "Directions are an imperative and a landmark: સીધા જાઓ, પછી ડાબે. Start with માફ કરો and "
              "the question is polite: સ્ટેશન ક્યાં છે?",
              [V("સીધા", "seedhaa", "straight", "adverb"),
               V("ડાબે", "daabe", "on the left", "adverb"),
               V("જમણે", "jamne", "on the right", "adverb"),
               V("ખૂણે", "khoone", "at the corner", "adverb"),
               V("પૂછવું", "poochhvun", "to ask", "verb")],
              G("Directions",
                "સીધા જાઓ · પછી ડાબે · ખૂણે · સ્ટેશન ક્યાં છે?",
                "Gujarati directions put the verb in the imperative (જાઓ, વળો) and the landmark last: "
                "સીધા જાઓ, પછી બીજી શેરીમાં ડાબે વળો. The station is at the corner — સ્ટેશન ખૂણે છે.",
                [X("સીધા જાઓ, પછી ડાબે.", "Seedhaa jaao, pachhi daabe.", "Go straight, then left."),
                 X("સ્ટેશન ખૂણે છે.", "Steshan khoone chhe.", "The station is at the corner."),
                 X("બસ સ્ટૉપ નજીક છે?", "Bas stop najik chhe?", "Is the bus stop nearby?")],
                [("તમે સીધા જાઓ.", "સીધા જાઓ.", "Directions drop the pronoun; the imperative carries it."),
                 ("સ્ટેશન ખૂણો છે.", "સ્ટેશન ખૂણે છે.", "A place is expressed with the locative ખૂણે.")]),
              [D("Newcomer", "માફ કરો, સ્ટેશન ક્યાં છે?", "Maaf karo, steshan kyaan chhe?", "Excuse me, where is the station?"),
               D("Neighbour", "સીધા જાઓ, પછી ડાબે.", "Seedhaa jaao, pachhi daabe.", "Go straight, then left."),
               D("Newcomer", "દૂર છે?", "Door chhe?", "Is it far?"),
               D("Neighbour", "ના, પાંચ મિનિટ ચાલવું.", "Naa, paanch minut chaalvun.", "No, a five-minute walk.")],
              WS("Directions worksheet", [
                  T("Give the direction.", ["go straight", "then left", "at the corner"],
                    ["સીધા જાઓ.", "પછી ડાબે", "ખૂણે"]),
                  T("Ask and answer.", ["where is the station?", "it is nearby"],
                    ["સ્ટેશન ક્યાં છે?", "નજીક છે"]),
              ])),
            L("ટિકિટ અને ઊતરવાનું સ્ટેશન",
              "Ticket talk has three moves: એક ટિકિટ આપો · કેટલાની છે? · હું ત્રીજા સ્ટૉપે ઊતરું છું. "
              "The stop takes the locative -એ.",
              [V("ટિકિટ", "tikit", "ticket", "noun"),
               V("સ્ટૉપ", "stop", "stop", "noun"),
               V("ઊતરવું", "ootarvun", "to get down", "verb"),
               V("ચઢવું", "chadhvun", "to board", "verb"),
               V("ભાડું", "bhaadun", "fare", "noun")],
              G("Bus frame",
                "એક ટિકિટ આપો · કેટલાની છે? · હું ત્રીજા સ્ટૉપે ઊતરું છું",
                "The fare question is કેટલાની છે? for a ticket (feminine) and the stop takes -એ: "
                "ત્રીજા સ્ટૉપે. Boarding and getting down are ચઢવું and ઊતરવું — the same pair the "
                "city uses for every vehicle.",
                [X("એક ટિકિટ આપો.", "Ek tikit aapo.", "One ticket, please."),
                 X("કેટલાની છે?", "Ketlaani chhe?", "How much is it?"),
                 X("હું ત્રીજા સ્ટૉપે ઊતરું છું.", "Hun treejaa stope ootarun chhun.", "I get down at the third stop.")],
                [("હું ત્રીજા સ્ટૉપ ઊતરું છું.", "હું ત્રીજા સ્ટૉપે ઊતરું છું.", "The stop takes the locative -એ."),
                 ("ટિકિટ કેટલાનો છે?", "ટિકિટ કેટલાની છે?", "ટિકિટ is feminine: કેટલાની.")]),
              [D("Newcomer", "એક ટિકિટ આપો.", "Ek tikit aapo.", "One ticket, please."),
               D("Manager", "ક્યાં સુધી?", "Kyaan sudhi?", "Up to where?"),
               D("Newcomer", "બજાર સુધી. કેટલાની છે?", "Bajaar sudhi. Ketlaani chhe?", "Up to the market. How much is it?"),
               D("Manager", "દસ રૂપિયા. ત્રીજા સ્ટૉપે ઊતરો.", "Das rupiyaa. Treejaa stope ootaro.", "Ten rupees. Get down at the third stop.")],
              WS("Ticket worksheet", [
                  T("Buy the ticket.", ["one ticket, please", "how much is it?"],
                    ["એક ટિકિટ આપો.", "કેટલાની છે?"]),
                  T("Name the stop.", ["I get down at the third stop", "get down at the market"],
                    ["હું ત્રીજા સ્ટૉપે ઊતરું છું.", "બજારમાં ઊતરો"]),
              ])),
            L("સરનામું: શેરી, નંબર, નિશાની",
              "An address gives the street, the number and one landmark: હું શાહપુરમાં રહું છું, શેરી "
              "નંબર ચાર, મંદિરની સામે. The landmark is what makes it findable.",
              [V("સરનામું", "sarnaamun", "address", "noun"),
               V("શેરી", "sheri", "street", "noun"),
               V("સામે", "saame", "opposite", "postposition"),
               V("મંદિર", "mandir", "temple", "noun"),
               V("રહેવું", "rahevun", "to live, to stay", "verb")],
              G("Address frame",
                "હું શાહપુરમાં રહું છું · શેરી નંબર ચાર · મંદિરની સામે",
                "Residence takes the locative -માં (શાહપુરમાં), the landmark takes સામે or પાસે with a "
                "genitive (મંદિરની સામે), and the verb closes the sentence.",
                [X("હું શાહપુરમાં રહું છું.", "Hun Shaahpurmaa rahun chhun.", "I live in Shahpur."),
                 X("શેરી નંબર ચાર.", "Sheri nambar chaar.", "Street number four."),
                 X("મંદિરની સામે.", "Mandirni saame.", "Opposite the temple.")],
                [("હું શાહપુર રહું છું.", "હું શાહપુરમાં રહું છું.", "Residence takes -માં."),
                 ("મંદિર સામે.", "મંદિરની સામે.", "સામે takes the genitive: મંદિરની સામે.")]),
              [D("Neighbour", "તમે ક્યાં રહો છો?", "Tame kyaan raho chho?", "Where do you live?"),
               D("Student", "શાહપુરમાં, શેરી નંબર ચાર.", "Shaahpurmaa, sheri nambar chaar.", "In Shahpur, street number four."),
               D("Neighbour", "કોઈ નિશાની?", "Koi nishaani?", "Any landmark?"),
               D("Student", "મંદિરની સામે, નદીની પાસે.", "Mandirni saame, nadeeni paase.", "Opposite the temple, near the river.")],
              WS("Address worksheet", [
                  T("Give the address.", ["I live in Shahpur", "street number four"],
                    ["હું શાહપુરમાં રહું છું.", "શેરી નંબર ચાર"]),
                  T("Point at the landmark.", ["opposite the temple", "near the river"],
                    ["મંદિરની સામે", "નદીની પાસે"]),
              ])),
        ]},
        {"id": "A1+-U2", "title": "સમય અને દિવસ", "lessons": [
            L("કેટલા વાગ્યા? સવા નવ",
              "Time is said with વાગ્યે and a fraction before the hour: સવા નવ (9:15), સાડા નવ "
              "(9:30), પોણા દસ (9:45). The question is કેટલા વાગ્યા?",
              [V("વાગ્યા", "vaagyaa", "o'clock, struck", "verb form"),
               V("સવા", "savaa", "quarter past", "adverb"),
               V("સાડા", "saadaa", "half past", "adverb"),
               V("પોણા", "ponaa", "quarter to", "adverb"),
               V("મિનિટ", "minit", "minute", "noun")],
              G("Telling the time",
                "કેટલા વાગ્યા? · સવા નવ વાગ્યા છે · પોણા દસ વાગ્યે",
                "The hour comes after the fraction (સવા નવ, પોણા દસ) and the verb is વાગ્યા — plural, "
                "because it counts the strikes. A scheduled time takes વાગ્યે: પોણા દસ વાગ્યે નીકળીએ.",
                [X("કેટલા વાગ્યા?", "Ketlaa vaagyaa?", "What time is it?"),
                 X("સવા નવ વાગ્યા છે.", "Savaa nav vaagyaa chhe.", "It is quarter past nine."),
                 X("પોણા દસ વાગ્યે નીકળીએ.", "Ponaa das vaagye neekalie.", "Let us leave at quarter to ten.")],
                [("નવ સવા વાગ્યા છે.", "સવા નવ વાગ્યા છે.", "The fraction precedes the hour."),
                 ("નવ વાગ્યા છે સવા.", "સવા નવ વાગ્યા છે.", "The whole phrase closes with the verb: સવા નવ વાગ્યા છે.")]),
              [D("Student", "કેટલા વાગ્યા?", "Ketlaa vaagyaa?", "What time is it?"),
               D("Teacher", "સવા નવ વાગ્યા છે.", "Savaa nav vaagyaa chhe.", "It is quarter past nine."),
               D("Student", "વર્ગ ક્યારે શરૂ થાય છે?", "Varg kyaare sharu thaay chhe?", "When does the class start?"),
               D("Teacher", "પોણા દસ વાગ્યે.", "Ponaa das vaagye.", "At quarter to ten.")],
              WS("Clock worksheet", [
                  T("Say the time.", ["quarter past nine", "half past nine"],
                    ["સવા નવ વાગ્યા છે.", "સાડા નવ વાગ્યા છે."]),
                  T("Say the schedule.", ["at quarter to ten", "at nine o'clock"],
                    ["પોણા દસ વાગ્યે", "નવ વાગ્યે"]),
              ])),
            L("દિવસો અને અઠવાડિયું",
              "Days take no preposition: સોમવારે હું કામ કરું છું. A repeated day takes રોજ: રોજ સવારે. "
              "The week has its own words for this and next: આ અઠવાડિયે, આવતા અઠવાડિયે.",
              [V("સોમવાર", "somvaar", "Monday", "noun"),
               V("અઠવાડિયું", "athvadiyun", "week", "noun"),
               V("રોજ", "roj", "every day", "adverb"),
               V("સવારે", "savaare", "in the morning", "adverb"),
               V("રજા", "rajaa", "holiday, leave", "noun")],
              G("Days and the week",
                "સોમવારે · રોજ સવારે · આ અઠવાડિયે · આવતા અઠવાડિયે",
                "A single day takes -એ (સોમવારે), a habit takes રોજ (રોજ સવારે ચાલવા જાઉં છું), and "
                "this or next week is આ / આવતા + અઠવાડિયે.",
                [X("સોમવારે હું કામ કરું છું.", "Somvaare hun kaam karun chhun.", "On Monday I work."),
                 X("રોજ સવારે ચાલવા જાઉં છું.", "Roj savaare chaalvaa jaun chhun.", "Every morning I go for a walk."),
                 X("આવતા અઠવાડિયે રજા છે.", "Aavtaa athvadiye rajaa chhe.", "Next week is a holiday.")],
                [("સોમવાર હું કામ કરું છું.", "સોમવારે હું કામ કરું છું.", "A day takes the locative -એ."),
                 ("રોજ સવાર હું ચાલું છું.", "રોજ સવારે હું ચાલું છું.", "સવારે names the morning; સવાર alone is the noun.")]),
              [D("Neighbour", "તમે ક્યારે કામ કરો છો?", "Tame kyaare kaam karo chho?", "When do you work?"),
               D("Manager", "સોમવારે અને બુધવારે, રોજ સવારે નવ વાગ્યે.", "Somvaare ane budhvaare, roj savaare nav vaagye.", "On Monday and Wednesday, every morning at nine."),
               D("Neighbour", "આવતા અઠવાડિયે?", "Aavtaa athvadiye?", "Next week?"),
               D("Manager", "આવતા અઠવાડિયે રજા છે.", "Aavtaa athvadiye rajaa chhe.", "Next week is a holiday.")],
              WS("Week worksheet", [
                  T("Place the days.", ["on Monday I work", "every morning I go for a walk"],
                    ["સોમવારે હું કામ કરું છું.", "રોજ સવારે ચાલવા જાઉં છું."]),
                  T("Talk about the week.", ["next week is a holiday", "this week I am free"],
                    ["આવતા અઠવાડિયે રજા છે.", "આ અઠવાડિયે હું ફ્રી છું."]),
              ])),
            L("મળવાનું નક્કી કરવું: સાત વાગ્યે મળીએ",
              "A plan is one question with a time and a place inside it: સાત વાગ્યે મળીએ? ઠીક છે? "
              "Late arrivals need one sentence: મોડું થાય તો ફોન કરું છું.",
              [V("મળવું", "malvun", "to meet", "verb"),
               V("ઠીક છે", "theek chhe", "all right", "phrase"),
               V("મોડું", "modun", "late", "adverb"),
               V("ફોન", "fon", "phone", "noun"),
               V("જગ્યા", "jagyaa", "place", "noun")],
              G("Meeting frame",
                "સાત વાગ્યે મળીએ? · ઠીક છે · મોડું થાય તો ફોન કરું છું",
                "The suggestion is મળીએ? with no છે, the agreement is ઠીક છે, and the contingency "
                "takes તો: મોડું થાય તો. One question, one answer, one escape route.",
                [X("સાત વાગ્યે મળીએ?", "Saat vaagye malie?", "Shall we meet at seven?"),
                 X("ઠીક છે, સ્ટેશન પર.", "Theek chhe, steshan par.", "All right, at the station."),
                 X("મોડું થાય તો ફોન કરું છું.", "Modun thaay to fon karun chhun.", "If I am late I will call.")],
                [("સાત વાગ્યે મળીએ છે?", "સાત વાગ્યે મળીએ?", "A suggestion is મળીએ?, without છે."),
                 ("હું મોડું છું.", "મને મોડું થાય છે.", "Lateness is said with મને … થાય છે.")]),
              [D("Student", "સાત વાગ્યે મળીએ?", "Saat vaagye malie?", "Shall we meet at seven?"),
               D("Neighbour", "ઠીક છે, ક્યાં?", "Theek chhe, kyaan?", "All right, where?"),
               D("Student", "સ્ટેશન પર, ટિકિટ ઑફિસ પાસે.", "Steshan par, tikit office paase.", "At the station, near the ticket office."),
               D("Neighbour", "બરાબર. મોડું થાય તો ફોન કરો.", "Baraabar. Modun thaay to fon karo.", "Fine. If you are late, call.")],
              WS("Plan worksheet", [
                  T("Make the plan.", ["shall we meet at seven?", "at the station near the ticket office"],
                    ["સાત વાગ્યે મળીએ?", "સ્ટેશન પર, ટિકિટ ઑફિસ પાસે"]),
                  T("Handle the delay.", ["if I am late I will call", "all right"],
                    ["મોડું થાય તો ફોન કરું છું.", "ઠીક છે"]),
              ])),
        ]},
        {"id": "A1+-U3", "title": "સમજવું અને સમજાવવું", "lessons": [
            L("સમજાયું નહીં: ફરી કહો",
              "Three repair phrases keep a conversation alive: સમજાયું નહીં · ફરી કહો, પ્લીઝ · ધીમે "
              "બોલો. They are turn-taking tools, not confessions.",
              [V("સમજવું", "samajvun", "to understand", "verb"),
               V("ફરી", "fari", "again", "adverb"),
               V("ધીમે", "dheeme", "slowly", "adverb"),
               V("લખવું", "lakhvun", "to write", "verb"),
               V("શબ્દ", "shabd", "word", "noun")],
              G("Repair phrases",
                "સમજાયું નહીં · ફરી કહો · ધીમે બોલો · આ શબ્દ કેમ લખાય છે?",
                "Each phrase hands the turn back with an instruction inside it. સમજાયું નહીં is the "
                "least accusatory of the three because it speaks about the listener, not the speaker.",
                [X("સમજાયું નહીં, ફરી કહો.", "Samjaayun nahi, fari kaho.", "I did not understand, say it again."),
                 X("ધીમે બોલો, પ્લીઝ.", "Dheeme bolo, pleez.", "Speak slowly, please."),
                 X("આ શબ્દ કેમ લખાય છે?", "Aa shabd kem lakhaay chhe?", "How is this word written?")],
                [("તું ખોટું બોલે છે.", "સમજાયું નહીં, ફરી કહો.", "A repair asks again; it does not accuse the speaker."),
                 ("મને સમજાયું નહીં છે.", "મને સમજાયું નહીં.", "The past form stands alone: સમજાયું નહીં.")]),
              [D("Newcomer", "સ્ટેશન પછી બીજી શેરીમાં ડાબે વળો.", "Steshan pachhi beeji sherimaa daabe valo.", "After the station turn left into the second street."),
               D("Student", "સમજાયું નહીં: ફરી કહો, ધીમે.", "Samjaayun nahi: fari kaho, dheeme.", "I did not understand: say it again, slowly."),
               D("Newcomer", "સ્ટેશન — પછી — બીજી શેરી — ડાબે.", "Steshan — pachhi — beeji sheri — daabe.", "Station — then — second street — left."),
               D("Student", "હવે સમજાયું. આભાર.", "Have samjaayun. Aabhaar.", "Now I understand. Thank you.")],
              WS("Repair worksheet", [
                  T("Ask for the repair.", ["I did not understand, say it again", "speak slowly, please"],
                    ["સમજાયું નહીં, ફરી કહો.", "ધીમે બોલો, પ્લીઝ."]),
                  T("Ask about the word.", ["how is this word written?", "what does this word mean?"],
                    ["આ શબ્દ કેમ લખાય છે?", "આ શબ્દનો અર્થ શું છે?"]),
              ])),
            L("એક મદદ કરો? મદદ માગવી",
              "A favour opens with a question and closes with one word: એક મદદ કરો? · ચા પીવી છે? · "
              "હા, જરૂર. Volentieri has its Gujarati twin in જરૂર.",
              [V("મદદ", "madad", "help", "noun"),
               V("માગવું", "maagvun", "to ask for", "verb"),
               V("જરૂર", "jaroor", "certainly, need", "adverb"),
               V("તકલીફ", "takleef", "trouble", "noun"),
               V("સાથે", "saathe", "with, together", "postposition")],
              G("Asking a favour",
                "એક મદદ કરો? · મારે તકલીફ છે · જરૂર, આભાર",
                "The request is a short question (એક મદદ કરો?), the state is stated with મારે … છે, and "
                "the answer that accepts is જરૂર — one word, no hesitation.",
                [X("એક મદદ કરો?", "Ek madad karo?", "Can you help me?"),
                 X("મારે આ થેલી ઉપાડવી છે.", "Maare aa theli upaadvi chhe.", "I need to lift this bag."),
                 X("જરૂર, આભાર.", "Jaroor, aabhaar.", "Certainly, thank you.")],
                [("હું મદદ કરો?", "એક મદદ કરો?", "A request for help is the imperative કરો used as a question."),
                 ("ઠીક છે, હા, ચાલો, બરાબર.", "જરૂર.", "One word accepts a favour; a pile-up sounds like hesitation.")]),
              [D("Mother", "એક મદદ કરો?", "Ek madad karo?", "Can you help me?"),
               D("Brother", "જરૂર. શું કરવું છે?", "Jaroor. Shu karvun chhe?", "Certainly. What needs doing?"),
               D("Mother", "આ થેલી ઉપાડવી છે.", "Aa theli upaadvi chhe.", "This bag needs lifting."),
               D("Brother", "લાવો, હું ઉપાડું છું.", "Laavo, hun upaadun chhun.", "Give it here, I will lift it.")],
              WS("Favour worksheet", [
                  T("Ask the favour.", ["can you help me?", "I need to lift this bag"],
                    ["એક મદદ કરો?", "મારે આ થેલી ઉપાડવી છે."]),
                  T("Answer well.", ["certainly, thank you", "what needs doing?"],
                    ["જરૂર, આભાર.", "શું કરવું છે?"]),
              ])),
            L("કેટલાનું છે? ભાવ અને ચૂકવણી",
              "Every counter asks three things: કેટલાનું છે? · કાર્ડ ચાલે છે? · પરચૂરણ આપો. Price, "
              "method, change — in that order.",
              [V("ભાવ", "bhaav", "price", "noun"),
               V("કાર્ડ", "kaard", "card", "noun"),
               V("રોકડ", "rokad", "cash", "noun"),
               V("પરચૂરણ", "parchooran", "change", "noun"),
               V("ચૂકવવું", "chookvun", "to pay", "verb")],
              G("Paying frame",
                "કેટલાનું છે? · હું કાર્ડથી ચૂકવું છું · પરચૂરણ આપો",
                "The instrument of payment takes -થી: કાર્ડથી, રોકડથી. The change request is a plain "
                "imperative: પરચૂરણ આપો. Price, method, change — and the purchase is closed.",
                [X("આ કેટલાનું છે?", "Aa ketlaanun chhe?", "How much is this?"),
                 X("હું કાર્ડથી ચૂકવું છું.", "Hun kaardthi chookvun chhun.", "I will pay by card."),
                 X("પરચૂરણ આપો.", "Parchooran aapo.", "Give me the change.")],
                [("હું કાર્ડ ચૂકવું છું.", "હું કાર્ડથી ચૂકવું છું.", "A means of payment takes -થી."),
                 ("આ કેટલાનો છે?", "આ કેટલાનું છે?", "The neuter thing takes કેટલાનું.")]),
              [D("Newcomer", "આ કેટલાનું છે?", "Aa ketlaanun chhe?", "How much is this?"),
               D("Manager", "સો રૂપિયા.", "So rupiyaa.", "A hundred rupees."),
               D("Newcomer", "હું કાર્ડથી ચૂકવું છું.", "Hun kaardthi chookvun chhun.", "I will pay by card."),
               D("Manager", "બરાબર. પરચૂરણ જોઈએ?", "Baraabar. Parchooran joie?", "Fine. Do you need change?")],
              WS("Payment worksheet", [
                  T("Ask the price.", ["how much is this?", "I will pay by card"],
                    ["આ કેટલાનું છે?", "હું કાર્ડથી ચૂકવું છું."]),
                  T("Close the purchase.", ["give me the change", "in cash"],
                    ["પરચૂરણ આપો.", "રોકડમાં"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Getting around Gujarat runs on the bus: ST buses leave from a bus port, tickets are "
                 "bought from a conductor on board, and the fare depends on the stop, not on the "
                 "distance in kilometres. The conductor calls the stops, so the practical vocabulary "
                 "of the half-step is the one heard on board — સ્ટૉપ, ભાડું, ઊતરવું, પરચૂરણ — because "
                 "following the call is what gets a learner off at the right place."),
        source_url="https://en.wikipedia.org/wiki/Gujarat_State_Road_Transport_Corporation",
        reading=("આજે સવારે હું બસમાં શાહપુર ગયો. કંડક્ટરે પૂછ્યું, «ક્યાં સુધી?» મેં કહ્યું, «બજાર "
                 "સુધી». ભાડું દસ રૂપિયા હતું. બસ ભરેલી હતી, તેથી હું ઊભો રહ્યો. ત્રીજા સ્ટૉપે "
                 "ઊતર્યો અને પછી સીધા જઈને ડાબે વળ્યો. સ્ટેશન ખૂણે હતું, મંદિરની સામે."),
        reading_gloss=("This morning I went to Shahpur by bus. The conductor asked, 'Up to where?' I "
                       "said, 'Up to the market.' The fare was ten rupees. The bus was crowded, so I "
                       "stood. I got down at the third stop and then went straight and turned left. "
                       "The station was at the corner, opposite the temple."),
        listening=("Newcomer: માફ કરો, સ્ટેશન ક્યાં છે?<br>Neighbour: સીધા જાઓ, પછી ડાબે, મંદિરની "
                   "સામે.<br>Newcomer: દૂર છે?<br>Neighbour: ના, પાંચ મિનિટ ચાલવું."),
        listening_gloss=("Newcomer: Excuse me, where is the station? Neighbour: Go straight, then "
                         "left, opposite the temple. Newcomer: Is it far? Neighbour: No, a "
                         "five-minute walk."),
        voice_tag=VOICE,
        idioms=[
            ("ક્યાં સુધી?", "up to where?", "how far are you going?"),
            ("ભાડું", "fare", "the fare"),
            ("ઊતરવું", "to get down", "to get off"),
            ("સીધા જાઓ", "go straight", "go straight ahead"),
            ("ડાબે વળવું", "to turn left", "to turn left"),
            ("દૂર છે?", "is it far?", "is it far?"),
            ("પાંચ મિનિટ ચાલવું", "a five-minute walk", "a five-minute walk"),
            ("નજીક", "near", "nearby"),
            ("પરચૂરણ", "change", "change (money)"),
            ("કેટલાનું છે?", "of how much is it?", "how much is it?"),
        ],
        mistakes=[
            ("હું બસમાં ત્રીજા સ્ટૉપ ઊતર્યો.", "હું બસમાંથી ત્રીજા સ્ટૉપે ઊતર્યો.", "Getting down takes બસમાંથી and the stop takes -એ."),
            ("બસ સ્ટેશન માટે દસ રૂપિયા છે.", "સ્ટેશન સુધીનું ભાડું દસ રૂપિયા છે.", "The fare is stated as સુધીનું ભાડું, not with માટે."),
            ("સીધા જાઓ, પછી વળો ડાબે.", "સીધા જાઓ, પછી ડાબે વળો.", "The direction precedes the verb: ડાબે વળો."),
        ],
        task_title="Direct a visitor from the bus stop to your home",
        task_instructions=("Write eight Gujarati lines a visitor can follow from the nearest bus stop "
                           "to your door: two directions (સીધા જાઓ, ડાબે વળો), one fare or stop "
                           "question (કેટલાની છે?, કયા સ્ટૉપે ઊતરવું?), one time (સવા નવ વાગ્યે) and "
                           "one landmark at the end (મંદિરની સામે). Hand it to somebody who cannot ask "
                           "you anything; the line they hesitate at is missing a postposition."),
    ),
    "test": [
        ("translate_en", "Say: Go straight, then left.", "સીધા જાઓ, પછી ડાબે."),
        ("translate_gu", "એક ટિકિટ આપો, બજાર સુધી.", "One ticket, up to the market."),
        ("multiple_choice", "Which is the polite repair?", "સમજાયું નહીં, ફરી કહો."),
        ("fill_in_the_blank", "કેટલા ___? — સવા નવ.", "વાગ્યા"),
        ("word_selection", "Select the Gujarati for 'quarter past nine'.", "સવા નવ વાગ્યા છે"),
        ("error_correction", "હું શાહપુર રહું છું.", "હું શાહપુરમાં રહું છું."),
        ("dialogue_completion", "Complete: કેટલા વાગ્યા? — ___ (quarter past nine)", "સવા નવ વાગ્યા છે"),
        ("matching", "Match પરચૂરણ to its meaning.", "change (money)"),
        ("reading_comprehension", "ભાડું દસ રૂપિયા હતું. How much was the fare?", "ten rupees"),
        ("inference", "«મોડું થાય તો ફોન કરું છું» — what is the speaker doing?", "promising to call if late"),
        ("main_idea", "સોમવારે અને બુધવારે, રોજ સવારે નવ વાગ્યે. What is this about?", "a weekly working schedule"),
        ("detail_identification", "મંદિરની સામે. Where is the place?", "opposite the temple"),
    ],
}

HALFSTEPS["A2+"] = {
    "title": "Gujarati A2+ — Day-to-day business",
    "native": NATIVE,
    "goals": [
        "State your hours, ask for leave and offer the repair",
        "Answer the phone and handle a counter visit",
        "Keep small talk going on weather, weekends and tea",
    ],
    "units": [
        {"id": "A2+-U1", "title": "ઓફિસમાં: સમય અને રજા", "lessons": [
            L("કામનો સમય: નવ વાગ્યા સુધીમાં",
              "A working day is stated with સુધીમાં (by) and વાગ્યે (at): નવ વાગ્યા સુધીમાં પહોંચું છું, "
              "સાંજે છ વાગ્યે નીકળું છું.",
              [V("સુધીમાં", "sudhimaa", "by, not later than", "postposition"),
               V("પહોંચવું", "pahonchvun", "to arrive, to reach", "verb"),
               V("નીકળવું", "neekalvun", "to leave, to set out", "verb"),
               V("સાંજે", "saanje", "in the evening", "adverb"),
               V("કામ", "kaam", "work", "noun")],
              G("Working hours",
                "નવ વાગ્યા સુધીમાં · છ વાગ્યે નીકળું છું · રોજ આઠ કલાક",
                "સુધીમાં marks the latest moment and વાગ્યે the exact one; a duration takes કલાક "
                "(hours). The verb closes the sentence, so the timetable reads as a list of arrivals "
                "and departures.",
                [X("નવ વાગ્યા સુધીમાં પહોંચું છું.", "Nav vaagyaa sudhimaa pahonchun chhun.", "I arrive by nine."),
                 X("સાંજે છ વાગ્યે નીકળું છું.", "Saanje chha vaagye neekalun chhun.", "In the evening I leave at six."),
                 X("રોજ આઠ કલાક કામ કરું છું.", "Roj aath kalaak kaam karun chhun.", "I work eight hours a day.")],
                [("હું નવ વાગ્યા સુધી પહોંચું છું.", "હું નવ વાગ્યા સુધીમાં પહોંચું છું.", "A deadline is સુધીમાં; સુધી alone means 'until'."),
                 ("હું છ વાગ્યે નીકળું છે.", "હું છ વાગ્યે નીકળું છું.", "The first person takes છું, not છે.")]),
              [D("Neighbour", "તમે ક્યારે પહોંચો છો?", "Tame kyaare pahoncho chho?", "When do you arrive?"),
               D("Manager", "નવ વાગ્યા સુધીમાં, પણ સોમવારે મોડું થાય છે.", "Nav vaagyaa sudhimaa, pan somvaare modun thaay chhe.", "By nine, but on Monday I am late."),
               D("Neighbour", "અને નીકળવાનું?", "Ane neekalvaanun?", "And leaving?"),
               D("Manager", "સાંજે છ વાગ્યે.", "Saanje chha vaagye.", "In the evening at six.")],
              WS("Hours worksheet", [
                  T("State the hours.", ["I arrive by nine", "I leave at six in the evening"],
                    ["નવ વાગ્યા સુધીમાં પહોંચું છું.", "સાંજે છ વાગ્યે નીકળું છું."]),
                  T("Count the work.", ["eight hours a day", "five days a week"],
                    ["રોજ આઠ કલાક", "અઠવાડિયે પાંચ દિવસ"]),
              ])),
            L("રજા માગવી: આવતીકાલે ન આવી શકું",
              "Leave is asked with a reason and a replacement: આવતીકાલે ન આવી શકું · કારણ કે … · "
              "પરવારી લઈશ. The replacement is what makes the answer yes.",
              [V("રજા", "rajaa", "leave, holiday", "noun"),
               V("શકવું", "shakvun", "to be able", "verb"),
               V("કારણ", "kaaran", "reason", "noun"),
               V("પરવારવું", "parvaarvun", "to make up, to manage", "verb"),
               V("જણાવવું", "janaavvun", "to inform", "verb")],
              G("Leave frame",
                "આવતીકાલે ન આવી શકું · કારણ કે … · પરવારી લઈશ · જણાવી દઉં છું",
                "Inability is expressed with શકું + ન: ન આવી શકું. The reason takes કારણ કે, and the "
                "repair takes the future: પરવારી લઈશ (I will make it up).",
                [X("આવતીકાલે ન આવી શકું.", "Aavtikale na aavi shakun.", "I cannot come tomorrow."),
                 X("કારણ કે દવાખાને જવું છે.", "Kaaran ke davaakhane javun chhe.", "Because I have to go to the clinic."),
                 X("હું પરવારી લઈશ.", "Hun parvaari laish.", "I will make it up.")],
                [("હું આવતીકાલે નથી આવું.", "આવતીકાલે ન આવી શકું.", "A request states inability, not refusal."),
                 ("પરવારવું કાલે.", "કાલે પરવારી લઈશ.", "A promise needs the future verb, and the time precedes it.")]),
              [D("Manager", "આવતીકાલે આવશો?", "Aavtikale aavsho?", "Will you come tomorrow?"),
               D("Newcomer", "આવતીકાલે ન આવી શકું; દવાખાને જવું છે.", "Aavtikale na aavi shakun; davaakhane javun chhe.", "I cannot come tomorrow; I have to go to the clinic."),
               D("Manager", "અને કામ?", "Ane kaam?", "And the work?"),
               D("Newcomer", "હું પરવારી લઈશ અને જણાવી દઉં છું.", "Hun parvaari laish ane janaavi daun chhun.", "I will make it up, and I am informing you.")],
              WS("Leave worksheet", [
                  T("Ask for leave.", ["I cannot come tomorrow", "because I have to go to the clinic"],
                    ["આવતીકાલે ન આવી શકું.", "કારણ કે દવાખાને જવું છે."]),
                  T("Offer the repair.", ["I will make it up", "I will inform you"],
                    ["હું પરવારી લઈશ.", "જણાવી દઉં છું."]),
              ])),
            L("ફોન પર: કોણ બોલે છે?",
              "Office phone Gujarati is three formulas: નમસ્તે, … બોલું છું · કોણ બોલે છે? · એક મિનિટ, "
              "જોડું છું. The office names itself first.",
              [V("બોલવું", "bolvun", "to speak", "verb"),
               V("જોડવું", "jodvun", "to connect (a call)", "verb"),
               V("મિનિટ", "minit", "minute", "noun"),
               V("પછી", "pachhi", "later, then", "adverb"),
               V("સંદેશો", "sandesh", "message", "noun")],
              G("Phone frame",
                "નમસ્તે, … બોલું છું · કોણ બોલે છે? · એક મિનિટ, જોડું છું · પછી ફોન કરું છું",
                "The caller names the office and then himself: નમસ્તે, વેચાણ વિભાગ બોલું છું. જોડું છું "
                "connects the call, and if the person is absent the promise takes પછી … કરું છું.",
                [X("નમસ્તે, વેચાણ વિભાગ બોલું છું.", "Namaste, vechaan vibhaag bolun chhun.", "Good morning, sales section speaking."),
                 X("કોણ બોલે છે?", "Kon bole chhe?", "Who is speaking?"),
                 X("એક મિનિટ, જોડું છું.", "Ek minit, jodun chhun.", "One minute, I am connecting you.")],
                [("હું નમસ્તે બોલું છું.", "નમસ્તે, વેચાણ વિભાગ બોલું છું.", "The office is named before the person."),
                 ("એક મિનિટ, જોડીશું.", "એક મિનિટ, જોડું છું.", "The present is used at the moment of connecting.")]),
              [D("Newcomer", "નમસ્તે, વેચાણ વિભાગ બોલું છું.", "Namaste, vechaan vibhaag bolun chhun.", "Hello, sales section speaking."),
               D("Manager", "નમસ્તે, મારે મેનેજર સાથે વાત કરવી છે.", "Namaste, maare manager saathe vaat karvi chhe.", "Hello, I need to speak to the manager."),
               D("Newcomer", "એક મિનિટ, જોડું છું.", "Ek minit, jodun chhun.", "One minute, I am connecting you."),
               D("Manager", "આભાર.", "Aabhaar.", "Thank you.")],
              WS("Phone worksheet", [
                  T("Answer the phone.", ["sales section speaking", "who is speaking?"],
                    ["વેચાણ વિભાગ બોલું છું.", "કોણ બોલે છે?"]),
                  T("Connect the call.", ["one minute, I am connecting you", "I will call later"],
                    ["એક મિનિટ, જોડું છું.", "પછી ફોન કરું છું."]),
              ])),
        ]},
        {"id": "A2+-U2", "title": "નાની વાતો", "lessons": [
            L("કેમ છો? ટૂંકા જવાબ",
              "Small talk answers are short and graded: મજામાં · ઠીક ઠીક · બહુ સારું. The honest "
              "middle answer is the one that invites the next question.",
              [V("મજામાં", "majamaa", "well, fine", "phrase"),
               V("ઠીક ઠીક", "theek theek", "so-so", "phrase"),
               V("ચા", "chaa", "tea", "noun"),
               V("વ્યસ્ત", "vyast", "busy", "adjective"),
               V("આભાર", "aabhaar", "thanks", "noun")],
              G("Greeting frame",
                "કેમ છો? · મજામાં · ઠીક ઠીક · વ્યસ્ત છું",
                "An answer plus a question back is the whole machinery: કેમ છો? — મજામાં, તમે? and "
                "when the week is heavy, ઠીક ઠીક, વ્યસ્ત છું. One word and one question.",
                [X("કેમ છો? — મજામાં, તમે?", "Kem chho? — majamaa, tame?", "How are you? — Fine, and you?"),
                 X("ઠીક ઠીક, વ્યસ્ત છું.", "Theek theek, vyast chhun.", "So-so, I am busy."),
                 X("ચા પીએ?", "Chaa pie?", "Shall we have tea?")],
                [("કેમ છો? — હા.", "કેમ છો? — મજામાં.", "The greeting asks for a state, not a yes."),
                 ("હું મજામાં છો.", "હું મજામાં છું.", "First person takes છું.")]),
              [D("Teacher", "કેમ છો?", "Kem chho?", "How are you?"),
               D("Student", "ઠીક ઠીક, વ્યસ્ત છું. તમે?", "Theek theek, vyast chhun. Tame?", "So-so, I am busy. And you?"),
               D("Teacher", "મજામાં. ચા પીએ?", "Majamaa. Chaa pie?", "Fine. Shall we have tea?"),
               D("Student", "જરૂર.", "Jaroor.", "Certainly.")],
              WS("Greeting worksheet", [
                  T("Answer the greeting.", ["fine, and you?", "so-so, I am busy"],
                    ["મજામાં, તમે?", "ઠીક ઠીક, વ્યસ્ત છું."]),
                  T("Invite for tea.", ["shall we have tea?", "certainly"],
                    ["ચા પીએ?", "જરૂર."]),
              ])),
            L("હવામાન: વરસાદ પડે છે",
              "Weather takes પડે છે: વરસાદ પડે છે, ગરમી પડે છે, ઠંડી પડે છે. It is the safest small "
              "talk because it asks for no opinion.",
              [V("હવામાન", "havaamaan", "weather", "noun"),
               V("વરસાદ", "varsaad", "rain", "noun"),
               V("ગરમી", "garmi", "heat", "noun"),
               V("ઠંડી", "thandi", "cold", "noun"),
               V("પવન", "pavan", "wind", "noun")],
              G("Weather frame",
                "આજે વરસાદ પડે છે · ગરમી પડે છે · પવન ફૂંકે છે · કાલે ઠંડી હતી",
                "Rain, heat and cold fall (પડે છે) and wind blows (ફૂંકે છે); a past day takes હતું or "
                "હતી — કાલે ઠંડી હતી. The topic never runs dry because none of it needs a subject.",
                [X("આજે વરસાદ પડે છે.", "Aaje varsaad pade chhe.", "Today it is raining."),
                 X("ગરમી બહુ પડે છે.", "Garmi bahu pade chhe.", "It is very hot."),
                 X("કાલે ઠંડી હતી.", "Kaale thandi hati.", "Yesterday it was cold.")],
                [("આજે વરસાદ છે પડે.", "આજે વરસાદ પડે છે.", "One verb per sentence."),
                 ("કાલે ઠંડી હતું.", "કાલે ઠંડી હતી.", "ઠંડી is feminine: હતી.")]),
              [D("Neighbour", "આજે હવામાન કેવું છે?", "Aaje havaamaan kevun chhe?", "What is the weather like today?"),
               D("Mother", "વરસાદ પડે છે અને પવન ફૂંકે છે.", "Varsaad pade chhe ane pavan phoonke chhe.", "It is raining and the wind is blowing."),
               D("Neighbour", "કાલે?", "Kaale?", "Yesterday?"),
               D("Mother", "કાલે ઠંડી હતી, આજે ગરમી છે.", "Kaale thandi hati, aaje garmi chhe.", "Yesterday it was cold, today it is warm.")],
              WS("Weather worksheet", [
                  T("Describe the weather.", ["today it is raining", "it was cold yesterday"],
                    ["આજે વરસાદ પડે છે.", "કાલે ઠંડી હતી."]),
                  T("Add the wind.", ["the wind is blowing", "it is very hot"],
                    ["પવન ફૂંકે છે.", "ગરમી બહુ પડે છે."]),
              ])),
            L("અઠવાડિયાના અંતે શું કર્યું?",
              "A past weekend is reported with the perfect and the agreement that goes with it: હું "
              "બજાર ગયો, અમે ચા પીધી, મેં પુસ્તક વાંચ્યું.",
              [V("અઠવાડિયાનો અંત", "athvadiyaano ant", "weekend", "phrase"),
               V("બજાર", "bajaar", "market", "noun"),
               V("વાંચવું", "vaanchhvun", "to read", "verb"),
               V("પીવું", "peevun", "to drink", "verb"),
               V("ફરવું", "farvun", "to go around, to stroll", "verb")],
              G("Past weekend",
                "હું બજાર ગયો · અમે ચા પીધી · મેં પુસ્તક વાંચ્યું",
                "Intransitive verbs agree with the subject (હું બજાર ગયો / ગઈ), transitive ones take "
                "the ergative મેં (મેં પુસ્તક વાંચ્યું), and the verb agrees with the object when it "
                "is neuter. That single rule covers most weekend stories.",
                [X("હું બજાર ગયો.", "Hun bajaar gayo.", "I went to the market."),
                 X("અમે ચા પીધી.", "Ame chaa peedhi.", "We drank tea."),
                 X("મેં પુસ્તક વાંચ્યું.", "Me pustak vaanchyun.", "I read a book.")],
                [("હું બજાર ગયું.", "હું બજાર ગયો.", "A male speaker takes ગયો; agreement follows the subject."),
                 ("મેં પુસ્તક વાંચ્યો.", "મેં પુસ્તક વાંચ્યું.", "પુસ્તક is neuter, so the verb is વાંચ્યું.")]),
              [D("Neighbour", "અઠવાડિયાના અંતે શું કર્યું?", "Athvadiyaano ante shu karyun?", "What did you do at the weekend?"),
               D("Student", "હું બજાર ગયો અને પછી ફરવા ગયો.", "Hun bajaar gayo ane pachhi farvaa gayo.", "I went to the market and then went for a stroll."),
               D("Neighbour", "ચા?", "Chaa?", "Tea?"),
               D("Student", "અમે ઘરે ચા પીધી અને મેં પુસ્તક વાંચ્યું.", "Ame ghare chaa peedhi ane me pustak vaanchyun.", "We drank tea at home and I read a book.")],
              WS("Weekend worksheet", [
                  T("Report the weekend.", ["I went to the market", "we drank tea at home"],
                    ["હું બજાર ગયો.", "અમે ઘરે ચા પીધી."]),
                  T("Ask back.", ["what did you do?", "shall we go for a stroll?"],
                    ["શું કર્યું?", "ફરવા જઈએ?"]),
              ])),
        ]},
        {"id": "A2+-U3", "title": "સેવા: પોસ્ટ, બેંક, દુકાન", "lessons": [
            L("પોસ્ટ ઑફિસ: પાર્સલ મોકલવું",
              "Counter Gujarati is a queue and a form: કાગળ લો, નંબર લો, તમારો વારો. The parcel "
              "takes તારીખ and સરનામું before it takes stamps.",
              [V("પાર્સલ", "paarsal", "parcel", "noun"),
               V("કાગળ", "kaagal", "paper, form", "noun"),
               V("વારો", "vaaro", "turn", "noun"),
               V("તારીખ", "taarikh", "date", "noun"),
               V("મોકલવું", "mokalvun", "to send", "verb")],
              G("Post office frame",
                "એક પાર્સલ મોકલવું છે · કાગળ ભરો · તમારો વારો · તારીખ લખો",
                "The errand is stated with છે (મારે પાર્સલ મોકલવું છે), the form is filled (કાગળ ભરો), "
                "and the queue gives the turn (તમારો વારો). Dates are written in numerals and read "
                "with the month.",
                [X("મારે એક પાર્સલ મોકલવું છે.", "Maare ek paarsal mokalvun chhe.", "I need to send a parcel."),
                 X("આ કાગળ ભરો.", "Aa kaagal bharo.", "Fill in this form."),
                 X("તારીખ અને સરનામું લખો.", "Taarikh ane sarnaamun lakho.", "Write the date and the address.")],
                [("હું પાર્સલ મોકલું છે.", "મારે પાર્સલ મોકલવું છે.", "Need takes મારે + neuter infinitive છે."),
                 ("કાગળ ભરવું છે તમે.", "તમારે કાગળ ભરવો છે.", "The need belongs to the person: તમારે.")]),
              [D("Newcomer", "મારે એક પાર્સલ મોકલવું છે.", "Maare ek paarsal mokalvun chhe.", "I need to send a parcel."),
               D("Manager", "કાગળ ભરો અને તારીખ લખો.", "Kaagal bharo ane taarikh lakho.", "Fill in the form and write the date."),
               D("Newcomer", "વારો ક્યાં?", "Vaaro kyaan?", "Where is the queue?"),
               D("Manager", "ત્યાં, બારી નંબર ત્રણ પાસે.", "Tyaan, baari nambar tran paase.", "There, near window number three.")],
              WS("Post worksheet", [
                  T("State the errand.", ["I need to send a parcel", "fill in this form"],
                    ["મારે એક પાર્સલ મોકલવું છે.", "આ કાગળ ભરો."]),
                  T("Ask about the queue.", ["where is the queue?", "near window number three"],
                    ["વારો ક્યાં?", "બારી નંબર ત્રણ પાસે"]),
              ])),
            L("બેંક: ખાતું ખોલાવવું",
              "Bank Gujarati starts in the polite conditional: મારે ખાતું ખોલાવવું છે · ઓળખપત્ર "
              "જોઈએ · રોકડ જમા કરવી છે.",
              [V("ખાતું", "khaatun", "account", "noun"),
               V("ઓળખપત્ર", "olakhpatra", "identity document", "noun"),
               V("જમા", "jamaa", "deposit", "noun"),
               V("ઉપાડ", "upaad", "withdrawal", "noun"),
               V("ફોર્મ", "form", "form", "noun")],
              G("Bank frame",
                "મારે ખાતું ખોલાવવું છે · ઓળખપત્ર જોઈએ · રોકડ જમા કરવી છે · ઉપાડ કરવો છે",
                "The service is requested with મારે … છે, the requirement is stated with જોઈએ, and "
                "the two operations are જમા કરવું (deposit) and ઉપાડ કરવો (withdraw).",
                [X("મારે ખાતું ખોલાવવું છે.", "Maare khaatun kholaavvun chhe.", "I want to open an account."),
                 X("ઓળખપત્ર જોઈએ છે.", "Olakhpatra joie chhe.", "An identity document is needed."),
                 X("મારે રોકડ જમા કરવી છે.", "Maare rokad jamaa karvi chhe.", "I need to deposit cash.")],
                [("હું ખાતું ખોલાવું છે.", "મારે ખાતું ખોલાવવું છે.", "Need is મારે + infinitive + છે."),
                 ("ઉપાડ કરવું છે મને.", "મારે ઉપાડ કરવો છે.", "The infinitive agrees with its noun: ઉપાડ is masculine, so કરવો.")]),
              [D("Newcomer", "મારે ખાતું ખોલાવવું છે.", "Maare khaatun kholaavvun chhe.", "I want to open an account."),
               D("Manager", "ઓળખપત્ર જોઈએ.", "Olakhpatra joie.", "An identity document is needed."),
               D("Newcomer", "આ લો. અને ઉપાડ કરવો છે.", "Aa lo. Ane upaad karvo chhe.", "Here it is. And I need to withdraw."),
               D("Manager", "ફોર્મ ભરો, પછી બારી બે પર જાઓ.", "Form bharo, pachhi baari be par jaao.", "Fill the form, then go to window two.")],
              WS("Bank worksheet", [
                  T("Ask at the bank.", ["I want to open an account", "I need to deposit cash"],
                    ["મારે ખાતું ખોલાવવું છે.", "મારે રોકડ જમા કરવી છે."]),
                  T("Say what is needed.", ["an identity document is needed", "fill the form first"],
                    ["ઓળખપત્ર જોઈએ.", "પહેલાં ફોર્મ ભરો"]),
              ])),
            L("દુકાને ખરીદી: વજન, પેકેટ, બિલ",
              "Groceries are bought by weight and settled with a bill: એક કિલો · પેકેટ · બિલ આપો. "
              "Weight takes કિલો and the bill closes the transaction.",
              [V("વજન", "vajan", "weight", "noun"),
               V("કિલો", "kilo", "kilogram", "noun"),
               V("પેકેટ", "paket", "packet", "noun"),
               V("બિલ", "bil", "bill", "noun"),
               V("તોલવું", "tolvun", "to weigh", "verb")],
              G("Groceries frame",
                "એક કિલો ચોખા · બે પેકેટ · બિલ આપો · તોલીને આપો",
                "The quantity precedes the noun (એક કિલો ચોખા), the packet is counted directly (બે "
                "પેકેટ), and the bill is asked for with આપો. તોલીને આપો — 'weigh it and give it' — is "
                "the phrase that starts most purchases.",
                [X("એક કિલો ચોખા આપો.", "Ek kilo chokhaa aapo.", "Give me one kilo of rice."),
                 X("બે પેકેટ લો.", "Be paket lo.", "Take two packets."),
                 X("બિલ આપો.", "Bil aapo.", "Give me the bill.")],
                [("એક કિલો ચોખા આપો છે.", "એક કિલો ચોખા આપો.", "A request is the imperative alone."),
                 ("બિલ આપવું છે તમે.", "બિલ આપો.", "A request is not phrased with તમે … છે.")]),
              [D("Mother", "એક કિલો ચોખા આપો.", "Ek kilo chokhaa aapo.", "Give me one kilo of rice."),
               D("Brother", "બીજું કંઈ?", "Beejun kaain?", "Anything else?"),
               D("Mother", "બે પેકેટ ચા.", "Be paket chaa.", "Two packets of tea."),
               D("Brother", "આ લો. બિલ આપું?", "Aa lo. Bil aapun?", "Here you are. Shall I give the bill?")],
              WS("Groceries worksheet", [
                  T("Buy by weight.", ["one kilo of rice", "two packets of tea"],
                    ["એક કિલો ચોખા આપો.", "બે પેકેટ ચા."]),
                  T("Close the purchase.", ["give me the bill", "weigh it and give it"],
                    ["બિલ આપો.", "તોલીને આપો"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Gujarati daily life runs through three counters — the kirana shop, the post office "
                 "and the bank — and each one has its own fixed exchange. The shop sells by weight "
                 "and adds a fistful for a regular customer; the post office wants the form filled "
                 "before it wants the parcel; the bank asks for ઓળખપત્ર before it asks for anything "
                 "else. Learning the counter ritual is worth more than learning the vocabulary, "
                 "because the ritual is what the other person is waiting for."),
        source_url="https://en.wikipedia.org/wiki/Ahmedabad",
        reading=("આજે મારે ત્રણ કામ કરવાનાં હતાં. પહેલાં પોસ્ટ ઑફિસ ગયો: કાગળ ભર્યો, તારીખ લખી અને "
                 "પાર્સલ મોકલ્યું. પછી બેંક ગયો; મારે ઉપાડ કરવો હતો, તેથી ઓળખપત્ર બતાવ્યું. અંતે "
                 "દુકાનેથી એક કિલો ચોખા અને બે પેકેટ ચા લીધાં. દુકાનવાળાએ બિલ આપ્યું અને કહ્યું, "
                 "«કાલે ચા સારી આવી છે»."),
        reading_gloss=("Today I had three errands. First I went to the post office: I filled the "
                       "form, wrote the date and sent the parcel. Then I went to the bank; I needed "
                       "to withdraw, so I showed the identity document. Finally I bought a kilo of "
                       "rice and two packets of tea from the shop. The shopkeeper gave the bill and "
                       "said, 'the tea that came yesterday is good'."),
        listening=("Manager: નમસ્તે, વેચાણ વિભાગ બોલું છું.<br>Newcomer: નમસ્તે, મારે મેનેજર સાથે "
                   "વાત કરવી છે.<br>Manager: એક મિનિટ, જોડું છું.<br>Newcomer: આભાર."),
        listening_gloss=("Manager: Hello, sales section speaking. Newcomer: Hello, I need to speak "
                         "to the manager. Manager: One minute, I am connecting you. Newcomer: Thank "
                         "you."),
        voice_tag=VOICE,
        idioms=[
            ("તમારો વારો", "your turn", "your turn in the queue"),
            ("કાગળ ભરો", "fill the paper", "fill in the form"),
            ("જમા કરવું", "to do a deposit", "to deposit"),
            ("ઉપાડ કરવો", "to make a withdrawal", "to withdraw"),
            ("તોલીને આપો", "weigh and give", "weigh it out, please"),
            ("એક કિલો", "one kilo", "one kilogram"),
            ("બિલ આપો", "give the bill", "the bill, please"),
            ("ઠીક ઠીક", "so-so", "so-so"),
            ("ચા પીએ", "let us drink tea", "shall we have tea?"),
            ("વ્યસ્ત છું", "I am busy", "I am busy"),
        ],
        mistakes=[
            ("હું ખાતું ખોલાવું છે.", "મારે ખાતું ખોલાવવું છે.", "Need takes મારે + infinitive + છે."),
            ("મેં પુસ્તક વાંચ્યો.", "મેં પુસ્તક વાંચ્યું.", "પુસ્તક is neuter, so the verb is વાંચ્યું."),
            ("હું બજાર ગઈ છું ગયો.", "હું બજાર ગયો.", "One past form, agreeing with the subject."),
        ],
        task_title="Run one counter errand in Gujarati",
        task_instructions=("Pick one real errand you will run this week — the post office, the bank, "
                           "or the grocery shop — and write the Gujarati for it end to end: what you "
                           "say when your turn comes (મારે … છે), what you are asked for (ઓળખપત્ર, "
                           "કાગળ, વજન) and what you say to close (બિલ આપો, આભાર). Read it aloud "
                           "before you go; the line that feels clumsy is the one you will be asked "
                           "for twice."),
    ),
    "test": [
        ("translate_en", "Say: I cannot come tomorrow.", "આવતીકાલે ન આવી શકું."),
        ("translate_gu", "મારે એક પાર્સલ મોકલવું છે.", "I need to send a parcel."),
        ("multiple_choice", "Which is the correct leave request?", "આવતીકાલે ન આવી શકું; દવાખાને જવું છે."),
        ("fill_in_the_blank", "હું નવ વાગ્યા ___ પહોંચું છું.", "સુધીમાં"),
        ("word_selection", "Select the Gujarati for 'the bill, please'.", "બિલ આપો"),
        ("error_correction", "મેં પુસ્તક વાંચ્યો.", "મેં પુસ્તક વાંચ્યું."),
        ("dialogue_completion", "Complete: કોણ બોલે છે? — ___ (sales section speaking)", "વેચાણ વિભાગ બોલું છું"),
        ("matching", "Match તોલીને આપો to its meaning.", "weigh it out, please"),
        ("reading_comprehension", "પાર્સલ પોસ્ટ ઑફિસથી મોકલ્યું. Where was the parcel sent from?", "the post office"),
        ("inference", "«ઠીક ઠીક, વ્યસ્ત છું» — what is the speaker doing?", "answering small talk honestly"),
        ("main_idea", "મારે ઉપાડ કરવો છે, તેથી ઓળખપત્ર બતાવ્યું. What is this about?", "a bank errand"),
        ("detail_identification", "એક કિલો ચોખા અને બે પેકેટ ચા. How much tea?", "two packets"),
    ],
}

HALFSTEPS["B1+"] = {
    "title": "Gujarati B1+ — Work and opinions",
    "native": NATIVE,
    "goals": [
        "Run through an agenda and write down what was decided",
        "Give an opinion, agree with a reservation and disagree politely",
        "Describe a project: goal, deadline and the risk",
    ],
    "units": [
        {"id": "B1+-U1", "title": "બેઠકમાં", "lessons": [
            L("કાર્યસૂચિ અને વારો",
              "A meeting has a script: કાર્યસૂચિ · મારે બોલવું છે · પછી બીજા મુદ્દા પર જઈએ. Naming "
              "the step keeps five people in one conversation.",
              [V("કાર્યસૂચિ", "kaaryasoochi", "agenda", "noun"),
               V("મુદ્દો", "muddo", "point, matter", "noun"),
               V("વારો", "vaaro", "turn", "noun"),
               V("ચર્ચા", "charchaa", "discussion", "noun"),
               V("નિર્ણય", "nirnay", "decision", "noun")],
              G("Meeting frame",
                "કાર્યસૂચિ · મારે બોલવું છે · પછી બીજા મુદ્દા પર · નિર્ણય કરીએ",
                "The floor is asked for with મારે … છે (મારે બીજા મુદ્દા પર બોલવું છે), the move to the "
                "next point is પછી …, and the decision is announced with કરીએ or નક્કી થયું.",
                [X("આજની કાર્યસૂચિમાં ત્રણ મુદ્દા છે.", "Aajni kaaryasoochimaa tran muddaa chhe.", "Today's agenda has three points."),
                 X("મારે બીજા મુદ્દા પર બોલવું છે.", "Maare beejaa muddaa par bolvun chhe.", "I need to speak on the second point."),
                 X("પછી ત્રીજા મુદ્દા પર જઈએ.", "Pachhi treejaa muddaa par jaie.", "Then let us move to the third point.")],
                [("હું બોલવું છે.", "મારે બોલવું છે.", "The floor is asked for with મારે + infinitive છે."),
                 ("પછી જઈએ ત્રીજા મુદ્દા પર.", "પછી ત્રીજા મુદ્દા પર જઈએ.", "The place phrase precedes the verb.")]),
              [D("Manager", "આજની કાર્યસૂચિમાં ત્રણ મુદ્દા છે.", "Aajni kaaryasoochimaa tran muddaa chhe.", "Today's agenda has three points."),
               D("Newcomer", "મારે બીજા મુદ્દા પર બોલવું છે.", "Maare beejaa muddaa par bolvun chhe.", "I need to speak on the second point."),
               D("Manager", "જરૂર. પછી ત્રીજા મુદ્દા પર જઈએ.", "Jaroor. Pachhi treejaa muddaa par jaie.", "Certainly. Then let us go to the third point."),
               D("Newcomer", "બરાબર, અને નિર્ણય લખી લઈએ.", "Baraabar, ane nirnay lakhi laie.", "Fine, and let us write the decision down.")],
              WS("Meeting worksheet", [
                  T("Run the meeting.", ["the agenda has three points", "I need to speak on the second point"],
                    ["કાર્યસૂચિમાં ત્રણ મુદ્દા છે.", "મારે બીજા મુદ્દા પર બોલવું છે."]),
                  T("Move on and decide.", ["then let us move to the third point", "let us write the decision"],
                    ["પછી ત્રીજા મુદ્દા પર જઈએ.", "નિર્ણય લખી લઈએ"]),
              ])),
            L("નિર્ણય લખવો: નક્કી થયું કે",
              "Minutes speak collectively and factually: નક્કી થયું કે … · આપણે … કરીશું · બાકી રહ્યું "
              "… Many decisions, one date each.",
              [V("નક્કી થવું", "nakki thavun", "to be decided", "phrase"),
               V("બાકી", "baaki", "remaining, pending", "adjective"),
               V("મુદત", "mudat", "deadline", "noun"),
               V("જવાબદાર", "javaabdaar", "responsible", "adjective"),
               V("હસ્તાક્ષર", "hastaakshar", "signature", "noun")],
              G("Minutes frame",
                "નક્કી થયું કે … · આપણે … કરીશું · મુદત … · બાકી રહ્યું",
                "The collective decision is નક્કી થયું કે (it was decided that), the commitment takes "
                "the future (કરીશું), the deadline takes a date, and anything unresolved is listed as "
                "બાકી રહ્યું. A line without an owner is not a decision.",
                [X("નક્કી થયું કે પ્રયોગ પહેલા કરીશું.", "Nakki thayun ke prayog pahelaa karishun.", "It was decided that we will run the trial first."),
                 X("મુદત ત્રીસ જૂન છે.", "Mudat trees joon chhe.", "The deadline is 30 June."),
                 X("બજેટ બાકી રહ્યું.", "Bajet baaki rahyun.", "The budget remains pending.")],
                [("નક્કી કર્યું કે પ્રયોગ કરીશું.", "નક્કી થયું કે પ્રયોગ કરીશું.", "A collective decision is નક્કી થયું, not નક્કી કર્યું."),
                 ("મુદત ત્રીસ જૂન પર.", "મુદત ત્રીસ જૂન છે.", "Dates take no પર; the sentence closes with છે.")]),
              [D("Newcomer", "નિર્ણય લખ્યો?", "Nirnay lakhyo?", "Did you write the decision?"),
               D("Manager", "હા: «નક્કી થયું કે પ્રયોગ પહેલા કરીશું».", "Haa: «Nakki thayun ke prayog pahelaa karishun».", "Yes: 'it was decided that we will run the trial first'."),
               D("Newcomer", "અને મુદત?", "Ane mudat?", "And the deadline?"),
               D("Manager", "«મુદત ત્રીસ જૂન છે; બજેટ બાકી રહ્યું».", "«Mudat trees joon chhe; bajet baaki rahyun».", "'The deadline is 30 June; the budget remains pending'.")],
              WS("Minutes worksheet", [
                  T("Write the decision.", ["it was decided that we will run the trial first", "the deadline is 30 June"],
                    ["નક્કી થયું કે પ્રયોગ પહેલા કરીશું.", "મુદત ત્રીસ જૂન છે."]),
                  T("List what is open.", ["the budget remains pending", "we decide on Tuesday"],
                    ["બજેટ બાકી રહ્યું.", "મંગળવારે નક્કી કરીશું."]),
              ])),
            L("કામ વિશે કહેવું: હું … સંભાળું છું",
              "Describing your job takes the verb સંભાળવું and the field with નું: હું વેચાણ સંભાળું "
              "છું · નવા પ્રોજેક્ટ પર કામ કરું છું.",
              [V("સંભાળવું", "sambhaadvun", "to handle, to look after", "verb"),
               V("વિભાગ", "vibhaag", "department, section", "noun"),
               V("પ્રોજેક્ટ", "projekt", "project", "noun"),
               V("જવાબદારી", "javaabdaari", "responsibility", "noun"),
               V("અનુભવ", "anubhav", "experience", "noun")],
              G("Job description",
                "હું … સંભાળું છું · … પર કામ કરું છું · મારી જવાબદારી … છે",
                "The work takes સંભાળવું (handle) or કામ કરવું પર (work on), and the responsibility is "
                "stated with મારી જવાબદારી … છે. Three sentences and the listener knows where you sit.",
                [X("હું વેચાણ સંભાળું છું.", "Hun vechaan sambhaadun chhun.", "I handle sales."),
                 X("હું નવા પ્રોજેક્ટ પર કામ કરું છું.", "Hun navaa projekt par kaam karun chhun.", "I am working on a new project."),
                 X("મારી જવાબદારી ઓર્ડરની છે.", "Maari javaabdaari order ni chhe.", "My responsibility is orders.")],
                [("હું વેચાણ સંભાળું છે.", "હું વેચાણ સંભાળું છું.", "First person takes છું."),
                 ("હું પ્રોજેક્ટ કામ કરું છું.", "હું પ્રોજેક્ટ પર કામ કરું છું.", "Work on something takes પર.")]),
              [D("Manager", "તમે શું સંભાળો છો?", "Tame shu sambhaalo chho?", "What do you handle?"),
               D("Newcomer", "હું વેચાણ સંભાળું છું અને નવા પ્રોજેક્ટ પર કામ કરું છું.", "Hun vechaan sambhaadun chhun ane navaa projekt par kaam karun chhun.", "I handle sales and work on a new project."),
               D("Manager", "કેટલો અનુભવ છે?", "Ketlo anubhav chhe?", "How much experience do you have?"),
               D("Newcomer", "ત્રણ વર્ષનો અનુભવ છે.", "Tran varshno anubhav chhe.", "Three years of experience.")],
              WS("Role worksheet", [
                  T("Describe the job.", ["I handle sales", "I am working on a new project"],
                    ["હું વેચાણ સંભાળું છું.", "હું નવા પ્રોજેક્ટ પર કામ કરું છું."]),
                  T("State the experience.", ["three years of experience", "my responsibility is orders"],
                    ["ત્રણ વર્ષનો અનુભવ છે.", "મારી જવાબદારી ઓર્ડરની છે."]),
              ])),
        ]},
        {"id": "B1+-U2", "title": "મત અને અસહમતિ", "lessons": [
            L("મારા મતે …",
              "An opinion arrives with a frame: મારા મતે · મને લાગે છે કે · મારી દૃષ્ટિએ. The frame "
              "turns a claim into something a colleague can answer.",
              [V("મત", "mat", "opinion", "noun"),
               V("લાગવું", "laagvun", "to seem, to feel", "verb"),
               V("દૃષ્ટિ", "drashti", "view, sight", "noun"),
               V("સૂચન", "soochan", "suggestion", "noun"),
               V("શંકા", "shankaa", "doubt", "noun")],
              G("Opinion frames",
                "મારા મતે … · મને લાગે છે કે … · મારી દૃષ્ટિએ · મને શંકા છે",
                "મારા મતે takes a plain clause, મને લાગે છે કે takes a કે-clause, and a doubt is મને "
                "શંકા છે. The frame is what lets the other person disagree with the opinion rather "
                "than with you.",
                [X("મારા મતે સૂચન ઠીક છે.", "Maaraa mate soochan theek chhe.", "In my opinion the suggestion is fine."),
                 X("મને લાગે છે કે સમય ઓછો છે.", "Mane laage chhe ke samay ochho chhe.", "I feel that there is little time."),
                 X("મારી દૃષ્ટિએ પ્રયોગ જોઈએ.", "Maari drashtie prayog joie.", "From my point of view a trial is needed.")],
                [("મારા મતે કે સૂચન ઠીક છે.", "મારા મતે સૂચન ઠીક છે.", "મારા મતે is already a frame: no કે after it."),
                 ("મને લાગે છે કે સમય ઓછો છે છે.", "મને લાગે છે કે સમય ઓછો છે.", "One છે per clause.")]),
              [D("Manager", "તમારો મત શું છે?", "Tamaaro mat shu chhe?", "What is your opinion?"),
               D("Newcomer", "મારા મતે સૂચન ઠીક છે, પણ સમય ઓછો છે.", "Maaraa mate soochan theek chhe, pan samay ochho chhe.", "In my opinion the suggestion is fine, but there is little time."),
               D("Manager", "તો?", "To?", "So?"),
               D("Newcomer", "મારી દૃષ્ટિએ પહેલા નાનો પ્રયોગ જોઈએ.", "Maari drashtie pahelaa naano prayog joie.", "From my point of view a small trial is needed first.")],
              WS("Opinion worksheet", [
                  T("Give the opinion.", ["in my opinion the suggestion is fine", "I feel that there is little time"],
                    ["મારા મતે સૂચન ઠીક છે.", "મને લાગે છે કે સમય ઓછો છે."]),
                  T("Frame the doubt.", ["from my point of view a trial is needed", "I have a doubt about the cost"],
                    ["મારી દૃષ્ટિએ પ્રયોગ જોઈએ.", "મને ખર્ચમાં શંકા છે."]),
              ])),
            L("સહમતી અને અસહમતિ",
              "Agreement and disagreement are both graded: સહમત છું · સહમત છું, પણ … · મને નથી "
              "લાગતું · આ મુદ્દે હું અસહમત છું.",
              [V("સહમત", "sahmat", "agreed", "adjective"),
               V("અસહમત", "asahmat", "in disagreement", "adjective"),
               V("મુદ્દે", "mudde", "on the point of", "postposition"),
               V("વાંધો", "vaandho", "objection", "noun"),
               V("પ્રસ્તાવ", "prastaav", "proposal", "noun")],
              G("Agreement frame",
                "સહમત છું · સહમત છું, પણ … · મને નથી લાગતું · આ મુદ્દે અસહમત છું",
                "Full agreement, partial agreement (પણ), and disagreement attached to a named point "
                "(આ મુદ્દે) — the third keeps the door open, which is why it is the useful one in a "
                "meeting.",
                [X("હું પ્રથમ ભાગ સાથે સહમત છું.", "Hun pratham bhaag saathe sahmat chhun.", "I agree with the first part."),
                 X("સહમત છું, પણ સમય ઓછો છે.", "Sahmat chhun, pan samay ochho chhe.", "I agree, but there is little time."),
                 X("આ મુદ્દે હું અસહમત છું.", "Aa mudde hun asahmat chhun.", "On this point I disagree.")],
                [("હું સહમત છું પ્રથમ ભાગ.", "હું પ્રથમ ભાગ સાથે સહમત છું.", "Agreement takes સાથે."),
                 ("આ મુદ્દો હું અસહમત છું.", "આ મુદ્દે હું અસહમત છું.", "The point takes the locative -એ: આ મુદ્દે.")]),
              [D("Manager", "પ્રસ્તાવ મંજૂર કરીએ?", "Prastaav manjoor karie?", "Shall we approve the proposal?"),
               D("Newcomer", "હું પ્રથમ ભાગ સાથે સહમત છું.", "Hun pratham bhaag saathe sahmat chhun.", "I agree with the first part."),
               D("Manager", "અને બીજો?", "Ane beejo?", "And the second?"),
               D("Newcomer", "આ મુદ્દે અસહમત છું: મને ખર્ચ વધારે લાગે છે.", "Aa mudde asahmat chhun: mane kharch vadhaare laage chhe.", "On this point I disagree: the cost seems too high to me.")],
              WS("Agreement worksheet", [
                  T("Agree with a reservation.", ["I agree with the first part", "I agree, but there is little time"],
                    ["હું પ્રથમ ભાગ સાથે સહમત છું.", "સહમત છું, પણ સમય ઓછો છે."]),
                  T("Disagree politely.", ["on this point I disagree", "the cost seems too high to me"],
                    ["આ મુદ્દે હું અસહમત છું.", "મને ખર્ચ વધારે લાગે છે."]),
              ])),
            L("સમજાવવું: જો આમ કરીએ તો …",
              "Persuasion is a real condition: જો સમય ઘટાડીએ તો જોખમ વધે. State the consequence and "
              "let the other person draw the conclusion.",
              [V("જો", "jo", "if", "conjunction"),
               V("તો", "to", "then", "conjunction"),
               V("જોખમ", "jokham", "risk", "noun"),
               V("ઘટાડવું", "ghataadvun", "to reduce", "verb"),
               V("વધવું", "vadhvun", "to increase", "verb")],
              G("Conditional frame",
                "જો આમ કરીએ તો … · જોખમ વધે છે · સારું રહે કે …",
                "The real condition takes જો … તો with a present verb (કરીએ, વધે), never the future. "
                "The consequence is stated as a fact and the proposal follows it.",
                [X("જો સમય ઘટાડીએ તો જોખમ વધે.", "Jo samay ghataadie to jokham vadhe.", "If we reduce the time, the risk rises."),
                 X("તો પહેલા પ્રયોગ કરીએ.", "To pahelaa prayog karie.", "Then let us run a trial first."),
                 X("સારું રહે કે બે વ્યક્તિ કરે.", "Saarun rahe ke be vyakti kare.", "It would be good if two people did it.")],
                [("જો સમય ઘટાડીશું તો જોખમ વધશે.", "જો સમય ઘટાડીએ તો જોખમ વધે.", "A real condition takes the present, not the future."),
                 ("જો સમય ઘટાડીએ, જોખમ વધે.", "જો સમય ઘટાડીએ તો જોખમ વધે.", "The pair જો … તો stands together.")]),
              [D("Newcomer", "જો સમય ઘટાડીએ તો જોખમ વધે.", "Jo samay ghataadie to jokham vadhe.", "If we cut the time, the risk rises."),
               D("Manager", "તો શું કરીએ?", "To shu karie?", "Then what should we do?"),
               D("Newcomer", "પહેલા પ્રયોગ કરીએ, પંદર દિવસ.", "Pahelaa prayog karie, pandar divas.", "Let us run a trial first, fifteen days."),
               D("Manager", "ઠીક, એમ કરીએ.", "Theek, em karie.", "Fine, let us do that.")],
              WS("Persuasion worksheet", [
                  T("State the condition.", ["if we cut the time, the risk rises", "then let us run a trial first"],
                    ["જો સમય ઘટાડીએ તો જોખમ વધે.", "તો પહેલા પ્રયોગ કરીએ."]),
                  T("Propose the trial.", ["two people for fifteen days", "it would be good if two people did it"],
                    ["બે વ્યક્તિ, પંદર દિવસ", "સારું રહે કે બે વ્યક્તિ કરે."]),
              ])),
        ]},
        {"id": "B1+-U3", "title": "યોજના અને મુદત", "lessons": [
            L("ધ્યેય અને મુદત: માર્ચ સુધીમાં",
              "A goal takes an infinitive and a month takes સુધીમાં: ધ્યેય છે ખર્ચ ઘટાડવો, માર્ચ "
              "સુધીમાં. The goal and the date are two sentences, not one.",
              [V("ધ્યેય", "dhyey", "goal", "noun"),
               V("સુધીમાં", "sudhimaa", "by, within", "postposition"),
               V("પગલું", "pagalun", "step", "noun"),
               V("અંદાજ", "andaaz", "estimate", "noun"),
               V("પરિણામ", "parinaam", "result", "noun")],
              G("Goal frame",
                "ધ્યેય છે … વું · માર્ચ સુધીમાં · પહેલું પગલું … છે",
                "The goal is a neuter infinitive with છે (ધ્યેય છે ખર્ચ ઘટાડવો), the date takes "
                "સુધીમાં, and the first step is named separately. Three sentences, and the plan has "
                "a shape.",
                [X("ધ્યેય છે ખર્ચ ઘટાડવો.", "Dhyey chhe kharch ghataadvun.", "The goal is to cut costs."),
                 X("માર્ચ સુધીમાં પૂરું કરવું છે.", "Maarch sudhimaa poorun karvun chhe.", "It has to be finished by March."),
                 X("પહેલું પગલું પ્રયોગ છે.", "Pahelun pagalun prayog chhe.", "The first step is a trial.")],
                [("ધ્યેય છે કે ખર્ચ ઘટાડીએ.", "ધ્યેય છે ખર્ચ ઘટાડવો.", "A goal takes the infinitive, not a કે-clause."),
                 ("માર્ચ સુધી પૂરું કરવું છે.", "માર્ચ સુધીમાં પૂરું કરવું છે.", "A deadline takes સુધીમાં.")]),
              [D("Manager", "ધ્યેય શું છે?", "Dhyey shu chhe?", "What is the goal?"),
               D("Newcomer", "ધ્યેય છે ખર્ચ ઘટાડવો.", "Dhyey chhe kharch ghataadvun.", "The goal is to cut costs."),
               D("Manager", "ક્યારે સુધીમાં?", "Kyaare sudhimaa?", "By when?"),
               D("Newcomer", "માર્ચ સુધીમાં; પહેલું પગલું પ્રયોગ છે.", "Maarch sudhimaa; pahelun pagalun prayog chhe.", "By March; the first step is a trial.")],
              WS("Goal worksheet", [
                  T("State the goal.", ["the goal is to cut costs", "it has to be finished by March"],
                    ["ધ્યેય છે ખર્ચ ઘટાડવો.", "માર્ચ સુધીમાં પૂરું કરવું છે."]),
                  T("Name the first step.", ["the first step is a trial", "the estimate is fifteen days"],
                    ["પહેલું પગલું પ્રયોગ છે.", "અંદાજ પંદર દિવસનો છે."]),
              ])),
            L("ઇન્ટરવ્યૂ: અનુભવ અને રસ",
              "An interview states the experience with વર્ષનો અનુભવ and the interest with રસ છે: ત્રણ "
              "વર્ષનો અનુભવ છે · આ કામમાં મને રસ છે.",
              [V("ઇન્ટરવ્યૂ", "interview", "interview", "noun"),
               V("રસ", "ras", "interest", "noun"),
               V("કૌશલ્ય", "kaushalya", "skill", "noun"),
               V("શક્તિ", "shakti", "strength, ability", "noun"),
               V("પગાર", "pagar", "salary", "noun")],
              G("Interview frame",
                "ત્રણ વર્ષનો અનુભવ છે · મને આ કામમાં રસ છે · મારી શક્તિ … છે",
                "Experience takes વર્ષનો અનુભવ (masculine), interest takes મને … માં રસ છે, and a "
                "strength is stated with શક્તિ. The answers are short because the interviewer is "
                "listening for the nouns.",
                [X("મને ત્રણ વર્ષનો અનુભવ છે.", "Mane tran varshno anubhav chhe.", "I have three years of experience."),
                 X("મને આ કામમાં રસ છે.", "Mane aa kaammaa ras chhe.", "I am interested in this work."),
                 X("મારી શક્તિ ગ્રાહકો સાથે વાત કરવાની છે.", "Maari shakti graahako saathe vaat karvaani chhe.", "My strength is talking to customers.")],
                [("હું ત્રણ વર્ષ અનુભવ છું.", "મને ત્રણ વર્ષનો અનુભવ છે.", "Experience is possessed: મને … અનુભવ છે."),
                 ("મને કામ રસ છે.", "મને કામમાં રસ છે.", "Interest takes માં: કામમાં રસ.")]),
              [D("Manager", "કેટલો અનુભવ છે?", "Ketlo anubhav chhe?", "How much experience do you have?"),
               D("Newcomer", "મને ત્રણ વર્ષનો અનુભવ છે, વેચાણમાં.", "Mane tran varshno anubhav chhe, vechaanmaa.", "I have three years of experience, in sales."),
               D("Manager", "આ કામમાં રસ કેમ?", "Aa kaammaa ras kem?", "Why the interest in this work?"),
               D("Newcomer", "મને ગ્રાહકો સાથે વાત કરવી ગમે છે.", "Mane graahako saathe vaat karvi game chhe.", "I like talking to customers.")],
              WS("Interview worksheet", [
                  T("State the experience.", ["I have three years of experience", "in sales"],
                    ["મને ત્રણ વર્ષનો અનુભવ છે.", "વેચાણમાં"]),
                  T("Answer the motivation.", ["I am interested in this work", "I like talking to customers"],
                    ["મને આ કામમાં રસ છે.", "મને ગ્રાહકો સાથે વાત કરવી ગમે છે."]),
              ])),
            L("મુદત ચૂકી જાય તો: જોખમ અને પ્લાન બી",
              "Contingency talk names the risk and the fallback: મુદત ચૂકી જાય તો ગ્રાહકને જણાવીએ · "
              "પ્લાન બી: બે અઠવાડિયાં વધુ.",
              [V("ચૂકવું", "chookvun", "to miss", "verb"),
               V("ગ્રાહક", "graahak", "customer, client", "noun"),
               V("વૈકલ્પિક", "vaikalpik", "alternative", "adjective"),
               V("તૈયારી", "taiyaari", "preparation", "noun"),
               V("નુકસાન", "nuksaan", "loss", "noun")],
              G("Contingency frame",
                "મુદત ચૂકી જાય તો … · ગ્રાહકને જણાવીએ · પ્લાન બી … · નુકસાન ઓછું",
                "The risk takes જાય તો (if it slips), the move takes the suggestion form જણાવીએ, and "
                "the fallback is named with its content — બે અઠવાડિયાં વધુ. Naming the fallback in "
                "advance is what keeps a missed deadline cheap.",
                [X("મુદત ચૂકી જાય તો ગ્રાહકને જણાવીએ.", "Mudat chooki jaay to graahakne janaavie.", "If the deadline slips, let us tell the client."),
                 X("પ્લાન બી: બે અઠવાડિયાં વધુ.", "Plaan bi: be athvadiyaan vadhu.", "Plan B: two more weeks."),
                 X("એટલે નુકસાન ઓછું થાય.", "Etle nuksaan ochhu thaay.", "That way the loss is smaller.")],
                [("મુદત ચૂકી જાય તો ગ્રાહકને જણાવીશું.", "મુદત ચૂકી જાય તો ગ્રાહકને જણાવીએ.", "A contingency plan takes the suggestion form, not a flat future."),
                 ("પ્લાન બી બે અઠવાડિયાં છે વધુ.", "પ્લાન બી: બે અઠવાડિયાં વધુ.", "The fallback is named as a phrase, with a colon.")]),
              [D("Manager", "મુદત ચૂકી જાય તો?", "Mudat chooki jaay to?", "If the deadline slips?"),
               D("Newcomer", "ગ્રાહકને તરત જણાવીએ.", "Graahakne tarat janaavie.", "Let us tell the client at once."),
               D("Manager", "અને?", "Ane?", "And?"),
               D("Newcomer", "પ્લાન બી: બે અઠવાડિયાં વધુ, એટલે નુકસાન ઓછું.", "Plaan bi: be athvadiyaan vadhu, etle nuksaan ochhu.", "Plan B: two more weeks, so the loss is smaller.")],
              WS("Risk worksheet", [
                  T("Name the risk and the move.", ["if the deadline slips, let us tell the client", "plan B: two more weeks"],
                    ["મુદત ચૂકી જાય તો ગ્રાહકને જણાવીએ.", "પ્લાન બી: બે અઠવાડિયાં વધુ."]),
                  T("State the effect.", ["that way the loss is smaller", "we are prepared"],
                    ["એટલે નુકસાન ઓછું થાય.", "આપણે તૈયારીમાં છીએ."]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Gujarati working life is negotiated in person and recorded afterwards: the meeting "
                 "decides, the message confirms, and the minutes exist to remind everyone what was "
                 "said out loud. That is why the half-step keeps three registers side by side — the "
                 "spoken meeting (મારે બોલવું છે), the written decision (નક્કી થયું કે) and the "
                 "opinion that has to survive both (મારા મતે … , પણ …)."),
        source_url="https://en.wikipedia.org/wiki/Gujarati_people",
        reading=("આજની બેઠકમાં ત્રણ મુદ્દા હતા. મારે બીજા મુદ્દા પર બોલવું હતું, તેથી મેં કહ્યું, "
                 "«મારા મતે સૂચન ઠીક છે, પણ જો સમય ઘટાડીએ તો જોખમ વધે». અંતે નક્કી થયું કે "
                 "પહેલા પંદર દિવસનો પ્રયોગ કરીશું અને મુદત ત્રીસ જૂન રાખીશું. બજેટ બાકી રહ્યું. "
                 "પછી મેં ટૂંકો સંદેશ મોકલ્યો."),
        reading_gloss=("Today's meeting had three points. I had to speak on the second point, so I "
                       "said, 'In my opinion the suggestion is fine, but if we cut the time the risk "
                       "rises.' In the end it was decided that we would run a fifteen-day trial and "
                       "keep the deadline at 30 June. The budget remained pending. Afterwards I sent "
                       "a short message."),
        listening=("Manager: તમારો મત શું છે?<br>Newcomer: મારા મતે સૂચન ઠીક છે, પણ સમય ઓછો છે.<br>"
                   "Manager: તો શું કરીએ?<br>Newcomer: પંદર દિવસનો પ્રયોગ કરીએ."),
        listening_gloss=("Manager: What is your opinion? Newcomer: In my opinion the suggestion is "
                         "fine, but there is little time. Manager: Then what should we do? "
                         "Newcomer: Let us run a fifteen-day trial."),
        voice_tag=VOICE,
        idioms=[
            ("મારા મતે", "in my opinion", "in my opinion"),
            ("સહમત છું", "I am agreed", "I agree"),
            ("આ મુદ્દે", "on this point", "on this point"),
            ("નક્કી થયું", "it became decided", "it was decided"),
            ("બાકી રહ્યું", "it remained pending", "it is still open"),
            ("મુદત", "deadline", "the deadline"),
            ("પ્લાન બી", "plan B", "the fallback"),
            ("જવાબદારી", "responsibility", "responsibility"),
            ("અનુભવ", "experience", "experience"),
            ("રસ છે", "there is interest", "I am interested"),
        ],
        mistakes=[
            ("મારા મતે કે સૂચન ઠીક છે.", "મારા મતે સૂચન ઠીક છે.", "મારા મતે is already a frame; no કે after it."),
            ("જો સમય ઘટાડીશું તો જોખમ વધશે.", "જો સમય ઘટાડીએ તો જોખમ વધે.", "A real condition takes the present in both halves."),
            ("મુદત ત્રીસ જૂન પર છે.", "મુદત ત્રીસ જૂન છે.", "A date needs no પર."),
        ],
        task_title="Run a fifteen-minute meeting and write its minutes",
        task_instructions=("Take one decision you have to make this week and write the Gujarati for "
                           "it: the three agenda points, the line where you take the floor (મારે … "
                           "પર બોલવું છે), your opinion with one reservation (મારા મતે …, પણ …), the "
                           "decision as it would be announced (નક્કી થયું કે …) and the open item "
                           "(બાકી રહ્યું …). Then write the short message you would send afterwards. "
                           "If the message has no date and no owner, the meeting decided nothing."),
    ),
    "test": [
        ("translate_en", "Say: In my opinion the suggestion is fine.", "મારા મતે સૂચન ઠીક છે."),
        ("translate_gu", "નક્કી થયું કે પ્રયોગ પહેલા કરીશું.", "It was decided that we will run the trial first."),
        ("multiple_choice", "Which sentence expresses a real condition correctly?", "જો સમય ઘટાડીએ તો જોખમ વધે."),
        ("fill_in_the_blank", "આ મુદ્દ___ હું અસહમત છું.", "ે"),
        ("word_selection", "Select the Gujarati for 'the budget remains pending'.", "બજેટ બાકી રહ્યું."),
        ("error_correction", "મારા મતે કે સૂચન ઠીક છે.", "મારા મતે સૂચન ઠીક છે."),
        ("dialogue_completion", "Complete: તમારો મત શું છે? — ___ (in my opinion the suggestion is fine)", "મારા મતે સૂચન ઠીક છે"),
        ("matching", "Match પ્લાન બી to its meaning.", "the fallback plan"),
        ("reading_comprehension", "મુદત ત્રીસ જૂન રાખીશું. What date was kept?", "30 June"),
        ("inference", "«સહમત છું, પણ સમય ઓછો છે» — what is the speaker doing?", "agreeing with a reservation"),
        ("main_idea", "મારે બીજા મુદ્દા પર બોલવું છે. What is this about?", "taking the floor in a meeting"),
        ("detail_identification", "ત્રણ વર્ષનો અનુભવ છે. How much experience?", "three years"),
    ],
}

HALFSTEPS["B2+"] = {
    "title": "Gujarati B2+ — Argument and formal register",
    "native": NATIVE,
    "goals": [
        "Chain an argument and interrogate the figures behind it",
        "Write a complaint, an apology and an office note",
        "Summarise a document and close it with one decision",
    ],
    "units": [
        {"id": "B2+-U1", "title": "દલીલ અને આંકડા", "lessons": [
            L("દલીલની સાંકળ: એટલું જ નહીં … પણ",
              "A chain needs direction words: એટલું જ નહીં … પણ … · વધુમાં · તેથી. They carry the "
              "argument forward so that કારણ કે does not have to do all the work.",
              [V("એટલું જ નહીં", "etlun ja nahi", "not only that", "phrase"),
               V("પણ", "pan", "but, also", "conjunction"),
               V("વધુમાં", "vadhumaa", "moreover", "adverb"),
               V("તેથી", "tethi", "therefore", "conjunction"),
               V("મુદ્દો", "muddo", "point", "noun")],
              G("Argument chain",
                "એટલું જ નહીં … પણ … · વધુમાં … · તેથી …",
                "એટલું જ નહીં … પણ … adds a second clause with a new verb, વધુમાં extends, and તેથી "
                "concludes. One connector per step: stacking them turns an argument into noise.",
                [X("એટલું જ નહીં ખર્ચ ઘટે, પણ સમય પણ બચે.", "Etlun ja nahi kharch ghate, pan samay pan bache.", "Not only does the cost fall, but time is saved too."),
                 X("વધુમાં, ગ્રાહકે પણ માંગ્યું છે.", "Vadhumaa, graahake pan maangyun chhe.", "Moreover, the client has asked for it too."),
                 X("તેથી માર્ચથી શરૂ કરવું ઠીક છે.", "Tethi Maarchthi sharu karvun theek chhe.", "Therefore it is fine to start in March.")],
                [("એટલું જ નહીં ખર્ચ ઘટે, તેથી સમય બચે.", "એટલું જ નહીં ખર્ચ ઘટે, પણ સમય પણ બચે.", "એટલું જ નહીં pairs with પણ, not with તેથી."),
                 ("તેથી અને વધુમાં, તેથી શરૂ કરીએ.", "તેથી માર્ચથી શરૂ કરવું ઠીક છે.", "One connector per step.")]),
              [D("Editor", "દલીલ કેમ લખું?", "Daleel kem lakhun?", "How do I write the argument?"),
               D("Analyst", "«એટલું જ નહીં … પણ …», પછી «વધુમાં», અંતે «તેથી».", "«Etlun ja nahi … pan …», pachhi «vadhumaa», ante «tethi».", "'Not only … but …', then 'moreover', finally 'therefore'."),
               D("Editor", "એક જ વાક્યમાં?", "Ek ja vaakymaa?", "In one sentence?"),
               D("Analyst", "ના, એક પગલું એક વાક્ય.", "Naa, ek pagalun ek vaakya.", "No, one step per sentence.")],
              WS("Chain worksheet", [
                  T("Chain the argument.", ["not only does the cost fall, but time is saved too", "therefore it is fine to start in March"],
                    ["એટલું જ નહીં ખર્ચ ઘટે, પણ સમય પણ બચે.", "તેથી માર્ચથી શરૂ કરવું ઠીક છે."]),
                  T("Add a second reason.", ["moreover, the client has asked for it", "one step per sentence"],
                    ["વધુમાં, ગ્રાહકે પણ માંગ્યું છે.", "એક પગલું, એક વાક્ય"]),
              ])),
            L("સ્રોત અને પદ્ધતિ: કયો નમૂનો?",
              "Three questions turn a percentage into evidence: કયો સ્રોત? કેટલો નમૂનો? કઈ પદ્ધતિ? A "
              "figure without all three is a rumour with a decimal point.",
              [V("સ્રોત", "srot", "source", "noun"),
               V("નમૂનો", "namoono", "sample", "noun"),
               V("પદ્ધતિ", "paddhati", "method", "noun"),
               V("સરેરાશ", "sareraash", "average", "noun"),
               V("તપાસ", "tapas", "check, enquiry", "noun")],
              G("Evidence frame",
                "કયો સ્રોત? · કેટલો નમૂનો? · કઈ પદ્ધતિ? · સ્રોત અનુસાર",
                "The three questions are asked before the figure enters the argument, and the answer "
                "is written with its population: હજાર માણસોના નમૂનામાં સરેરાશ બાર ટકા. A number "
                "without a sample is not a finding.",
                [X("સ્રોત અનુસાર, સરેરાશ બાર ટકા છે.", "Srot anusaar, sareraash baar takaa chhe.", "According to the source, the average is twelve per cent."),
                 X("હજાર માણસોના નમૂનામાં.", "Hajaar maansonaa namoonaa-maa.", "In a sample of a thousand people."),
                 X("પદ્ધતિ જાહેર નથી.", "Paddhati jaaher nathi.", "The method is not public.")],
                [("સેત્તર ટકા લોકો માને છે કે …", "સ્રોત અનુસાર, સેત્તર ટકા નમૂનાએ કહ્યું કે …", "A percentage needs its source and its population."),
                 ("પદ્ધતિ ખબર નથી, પણ આંકડો સાચો લાગે છે.", "પદ્ધતિ જાહેર નથી; તપાસ કરવી પડશે.", "A figure without a method needs checking, not believing.")]),
              [D("Editor", "આંકડો કેટલો છે?", "Aankdo ketlo chhe?", "What is the figure?"),
               D("Analyst", "સરેરાશ બાર ટકા, હજાર માણસોના નમૂનામાં.", "Sareraash baar takaa, hajaar maansonaa namoonaa-maa.", "An average of twelve per cent, in a sample of a thousand people."),
               D("Editor", "પદ્ધતિ?", "Paddhati?", "The method?"),
               D("Analyst", "જાહેર નથી; તપાસ કરવી પડશે.", "Jaaher nathi; tapas karvi padshe.", "Not public; it will have to be checked.")],
              WS("Evidence worksheet", [
                  T("Interrogate the figure.", ["according to the source, the average is twelve per cent", "in a sample of a thousand people"],
                    ["સ્રોત અનુસાર, સરેરાશ બાર ટકા છે.", "હજાર માણસોના નમૂનામાં"]),
                  T("Flag the gap.", ["the method is not public", "it will have to be checked"],
                    ["પદ્ધતિ જાહેર નથી.", "તપાસ કરવી પડશે."]),
              ])),
            L("નિષ્કર્ષ: નીચેના કારણોસર",
              "A conclusion converts the argument into one decision with an owner: નીચેના કારણોસર "
              "અમે ઠરાવ કરીએ છીએ કે … · જવાબદાર … · મુદત …",
              [V("નિષ્કર્ષ", "nishkarsh", "conclusion", "noun"),
               V("કારણોસર", "kaaranosar", "on the grounds of", "postposition"),
               V("ઠરાવ", "tharaav", "resolution", "noun"),
               V("જવાબદારી", "javaabdaari", "responsibility", "noun"),
               V("સૂચન", "soochan", "recommendation", "noun")],
              G("Conclusion frame",
                "નીચેના કારણોસર … · અમે ઠરાવ કરીએ છીએ કે … · જવાબદાર: … · મુદત: …",
                "The conclusion names the grounds, states the resolution, and finishes with an owner "
                "and a date. Without the last two lines it is an opinion with a heading, and the "
                "reader cannot act on it.",
                [X("નીચેના કારણોસર અમે ઠરાવ કરીએ છીએ કે પ્રયોગ કરવો.", "Neeche-naa kaaranosar ame tharaav karie chhie ke prayog karvo.", "On the following grounds we resolve that a trial should be run."),
                 X("જવાબદાર: પ્રોજેક્ટ વિભાગ.", "Javaabdaar: projekt vibhaag.", "Responsible: the project section."),
                 X("મુદત: ત્રીસ જૂન.", "Mudat: trees joon.", "Deadline: 30 June.")],
                [("નિષ્કર્ષ: બધું સારું લાગે છે.", "નિષ્કર્ષ: પ્રયોગ કરવો, જવાબદાર પ્રોજેક્ટ વિભાગ, મુદત ત્રીસ જૂન.", "A conclusion states a decision, an owner and a date."),
                 ("નીચેના કારણોસર, કારણ કે ખર્ચ વધે છે.", "નીચેના કારણોસર: ખર્ચ વધે છે.", "કારણોસર already carries the reason; કારણ કે would repeat it.")]),
              [D("Editor", "નિષ્કર્ષ કેમ લખું?", "Nishkarsh kem lakhun?", "How do I write the conclusion?"),
               D("Analyst", "«નીચેના કારણોસર … ઠરાવ કરીએ છીએ કે …».", "«Neeche-naa kaaranosar … tharaav karie chhie ke …».", "'On the following grounds we resolve that …'."),
               D("Editor", "અને અંતે?", "Ane ante?", "And at the end?"),
               D("Analyst", "જવાબદાર અને મુદત — બંને.", "Javaabdaar ane mudat — banne.", "Responsible and deadline — both.")],
              WS("Conclusion worksheet", [
                  T("Write the resolution.", ["on the following grounds we resolve that a trial should be run", "responsible: the project section"],
                    ["નીચેના કારણોસર અમે ઠરાવ કરીએ છીએ કે પ્રયોગ કરવો.", "જવાબદાર: પ્રોજેક્ટ વિભાગ"]),
                  T("Name the date.", ["deadline: 30 June", "the conclusion names a decision, an owner and a date"],
                    ["મુદત: ત્રીસ જૂન", "નિષ્કર્ષમાં નિર્ણય, જવાબદાર અને મુદત હોય"]),
              ])),
        ]},
        {"id": "B2+-U2", "title": "સત્તાવાર લેખન", "lessons": [
            L("ફરિયાદ પત્ર: હકીકત, કારણ, માંગ",
              "A complaint is three paragraphs with no adjectives: હકીકત · કારણ · માંગ. Facts, "
              "grounds, request — and a date.",
              [V("ફરિયાદ", "fariyaad", "complaint", "noun"),
               V("હકીકત", "hakeekat", "fact", "noun"),
               V("માંગ", "maang", "demand, request", "noun"),
               V("ભરપાઈ", "bharpai", "compensation", "noun"),
               V("વિલંબ", "vilamb", "delay", "noun")],
              G("Complaint frame",
                "હકીકત: … · કારણ: … · માંગ: … દિવસમાં · અમને ખેદ છે",
                "The three headings are written out and filled with sentences. The request carries a "
                "deadline (દસ દિવસમાં) because an undated demand is read as a complaint about the "
                "past rather than a claim about the future.",
                [X("હકીકત: પાર્સલ નવ દિવસ મોડું આવ્યું.", "Hakeekat: paarsal nav divas modun aavyun.", "Fact: the parcel arrived nine days late."),
                 X("કારણ: કોઈ જાણ કરવામાં ન આવી.", "Kaaran: koi jaan karvaamaa na aavi.", "Grounds: no notice was given."),
                 X("માંગ: ખર્ચની ભરપાઈ દસ દિવસમાં.", "Maang: kharchni bharpai das divasmaa.", "Request: refund of the cost within ten days.")],
                [("તમે બહુ ખરાબ છો, પૈસા પાછા આપો.", "હકીકત: પાર્સલ નવ દિવસ મોડું આવ્યું; માંગ: ભરપાઈ.", "A complaint that names facts and a request gets answered; an insult gets filed."),
                 ("ભરપાઈ જલદી કરો.", "ભરપાઈ દસ દિવસમાં કરો.", "A claim carries a date.")]),
              [D("Editor", "ફરિયાદ કેમ લખું?", "Fariyaad kem lakhun?", "How do I write the complaint?"),
               D("Analyst", "ત્રણ ભાગ: હકીકત, કારણ, માંગ.", "Tran bhaag: hakeekat, kaaran, maang.", "Three parts: fact, grounds, request."),
               D("Editor", "માંગ કેવી?", "Maang kevi?", "What kind of request?"),
               D("Analyst", "ભરપાઈ દસ દિવસમાં — તારીખ સાથે.", "Bharpai das divasmaa — taarikh saathe.", "Refund within ten days — with a date.")],
              WS("Complaint worksheet", [
                  T("Write fact and grounds.", ["the parcel arrived nine days late", "no notice was given"],
                    ["હકીકત: પાર્સલ નવ દિવસ મોડું આવ્યું.", "કારણ: કોઈ જાણ કરવામાં ન આવી."]),
                  T("Write the request.", ["refund of the cost within ten days", "we regret the trouble"],
                    ["માંગ: ખર્ચની ભરપાઈ દસ દિવસમાં.", "અમને ખેદ છે."]),
              ])),
            L("માફીનો પત્ર: અમને ખેદ છે",
              "A written apology names the inconvenience, the repair and the date: અમને ખેદ છે · અમે "
              "ત્રણ દિવસમાં બદલી આપીશું · આભાર.",
              [V("ખેદ", "khed", "regret", "noun"),
               V("તકલીફ", "takleef", "trouble, inconvenience", "noun"),
               V("બદલી", "badli", "replacement", "noun"),
               V("તરત", "tarat", "immediately", "adverb"),
               V("ખાતરી", "khaatri", "assurance", "noun")],
              G("Apology frame",
                "અમને ખેદ છે · અમે … બદલી આપીશું · ત્રણ દિવસમાં · ખાતરી આપીએ છીએ",
                "The apology is in the first person plural, the repair takes the future (આપીશું), and "
                "the date makes it credible. An apology with no repair and no date is a second "
                "inconvenience.",
                [X("અમને તકલીફ માટે ખેદ છે.", "Amne takleef maate khed chhe.", "We regret the inconvenience."),
                 X("અમે ત્રણ દિવસમાં બદલી આપીશું.", "Ame tran divasmaa badli aapeeshun.", "We will arrange a replacement within three days."),
                 X("ખાતરી આપીએ છીએ કે ફરી નહીં થાય.", "Khaatri aapie chhie ke fari nahi thaay.", "We assure you it will not happen again.")],
                [("સોરી, ભૂલ થઈ ગઈ.", "અમને તકલીફ માટે ખેદ છે.", "Between offices the apology is formal and plural."),
                 ("અમે બદલી આપીશું, કદાચ કાલે.", "અમે ત્રણ દિવસમાં બદલી આપીશું.", "A repair carries a date, not a hope.")]),
              [D("Editor", "માફીનો પત્ર કેમ લખીએ?", "Maafino patra kem lakhie?", "How do we write the apology?"),
               D("Analyst", "«અમને તકલીફ માટે ખેદ છે», પછી બદલી અને તારીખ.", "«Amne takleef maate khed chhe», pachhi badli ane taarikh.", "'We regret the inconvenience', then the replacement and the date."),
               D("Editor", "અને અંતે?", "Ane ante?", "And finally?"),
               D("Analyst", "«ખાતરી આપીએ છીએ» અને આભાર.", "«Khaatri aapie chhie» ane aabhaar.", "'We assure you' and thanks.")],
              WS("Apology worksheet", [
                  T("Apologise formally.", ["we regret the inconvenience", "we will arrange a replacement within three days"],
                    ["અમને તકલીફ માટે ખેદ છે.", "અમે ત્રણ દિવસમાં બદલી આપીશું."]),
                  T("Give the assurance.", ["we assure you it will not happen again", "thank you"],
                    ["ખાતરી આપીએ છીએ કે ફરી નહીં થાય.", "આભાર."]),
              ])),
            L("કાર્યાલયની નોંધ: સંદર્ભ, વિષય, નિર્ણય",
              "An office note has three lines at the top and one paragraph below: સંદર્ભ · વિષય · "
              "નિર્ણય. The heading is what makes it findable a year later.",
              [V("સંદર્ભ", "sandarbh", "reference", "noun"),
               V("વિષય", "vishay", "subject", "noun"),
               V("નોંધ", "nondh", "note", "noun"),
               V("મંજૂરી", "manjoori", "approval", "noun"),
               V("ગુપ્ત", "gupt", "confidential", "adjective")],
              G("Office note frame",
                "સંદર્ભ: … · વિષય: … · નિર્ણય: … · મંજૂરી માટે",
                "The reference points at the earlier paper, the subject is a noun phrase, and the "
                "decision is stated in one sentence — મંજૂરી માટે રજૂ કરવામાં આવે છે (submitted for "
                "approval). Short headings, one paragraph, no adjectives.",
                [X("સંદર્ભ: તમારો પત્ર ૩ મે.", "Sandarbh: tamaaro patra 3 me.", "Reference: your letter of 3 May."),
                 X("વિષય: નવી કિંમતની મંજૂરી.", "Vishay: navi kimatni manjoori.", "Subject: approval of the new price."),
                 X("નિર્ણય: નવી કિંમત મંજૂરી માટે રજૂ.", "Nirnay: navi kimat manjoori maate raju.", "Decision: the new price is submitted for approval.")],
                [("વિષય: નવી કિંમત મંજૂર કરો.", "વિષય: નવી કિંમતની મંજૂરી.", "A subject line is a noun phrase, not an instruction."),
                 ("સંદર્ભ: પહેલાં કંઈક લખ્યું હતું.", "સંદર્ભ: તમારો પત્ર ૩ મે.", "A reference names the paper and its date.")]),
              [D("Newcomer", "નોંધ કેમ લખું?", "Nondh kem lakhun?", "How do I write the note?"),
               D("Manager", "ઉપર ત્રણ લીટી: સંદર્ભ, વિષય, નિર્ણય.", "Upar tran leeti: sandarbh, vishay, nirnay.", "Three lines at the top: reference, subject, decision."),
               D("Newcomer", "અને નીચે?", "Ane neeche?", "And below?"),
               D("Manager", "એક ફકરો, પછી મંજૂરી માટે રજૂ.", "Ek fakro, pachhi manjoori maate raju.", "One paragraph, then submitted for approval.")],
              WS("Note worksheet", [
                  T("Write the heading.", ["reference: your letter of 3 May", "subject: approval of the new price"],
                    ["સંદર્ભ: તમારો પત્ર ૩ મે.", "વિષય: નવી કિંમતની મંજૂરી"]),
                  T("Write the decision.", ["the new price is submitted for approval", "one paragraph below"],
                    ["નિર્ણય: નવી કિંમત મંજૂરી માટે રજૂ.", "નીચે એક ફકરો"]),
              ])),
        ]},
        {"id": "B2+-U3", "title": "સાર અને સમાપન", "lessons": [
            L("ટૂંકમાં: ત્રણ મુદ્દા",
              "A summary counts and selects: ટૂંકમાં: ત્રણ મુદ્દા, એક મંજૂર, બે બાકી · મુખ્ય મુદ્દો … "
              "છે. How many points, and which one decides the rest.",
              [V("ટૂંકમાં", "tunkmaa", "in short", "adverb"),
               V("સાર", "saar", "summary", "noun"),
               V("મુખ્ય", "mukhya", "main", "adjective"),
               V("મંજૂર", "manjoor", "approved", "adjective"),
               V("મુદ્દો", "muddo", "point", "noun")],
              G("Summary frame",
                "ટૂંકમાં: … · મુખ્ય મુદ્દો … છે · બાકી …",
                "The summary states the count first (ત્રણ મુદ્દા), then which one was approved, then "
                "the main point. A summary that lists everything without counting has summarized "
                "nothing.",
                [X("ટૂંકમાં: ત્રણ મુદ્દા, એક મંજૂર, બે બાકી.", "Tunkmaa: tran muddaa, ek manjoor, be baaki.", "In short: three points, one approved, two pending."),
                 X("મુખ્ય મુદ્દો ખર્ચ છે.", "Mukhya muddo kharch chhe.", "The main point is the cost."),
                 X("બાકી બે મુદ્દા જૂનમાં લઈએ.", "Baaki be muddaa Joonmaa laie.", "Let us take the two pending points in June.")],
                [("ટૂંકમાં, બધું ઠીક છે.", "ટૂંકમાં: ત્રણ મુદ્દા, એક મંજૂર, બે બાકી.", "A summary counts and selects."),
                 ("મુખ્ય મુદ્દો ખર્ચ છે, મુખ્ય મુદ્દો સમય છે.", "મુખ્ય મુદ્દો ખર્ચ છે.", "One main point per summary.")]),
              [D("Manager", "અહેવાલનો સાર?", "Ahevaalno saar?", "The summary of the report?"),
               D("Newcomer", "ટૂંકમાં: ત્રણ મુદ્દા, એક મંજૂર, બે બાકી.", "Tunkmaa: tran muddaa, ek manjoor, be baaki.", "In short: three points, one approved, two pending."),
               D("Manager", "મુખ્ય મુદ્દો?", "Mukhya muddo?", "The main point?"),
               D("Newcomer", "ખર્ચ.", "Kharch.", "The cost.")],
              WS("Summary worksheet", [
                  T("Summarise.", ["in short: three points, one approved, two pending", "the main point is the cost"],
                    ["ટૂંકમાં: ત્રણ મુદ્દા, એક મંજૂર, બે બાકી.", "મુખ્ય મુદ્દો ખર્ચ છે."]),
                  T("Name the rest.", ["let us take the two pending points in June", "one main point per summary"],
                    ["બાકી બે મુદ્દા જૂનમાં લઈએ.", "એક સારમાં એક મુખ્ય મુદ્દો"]),
              ])),
            L("બીજા શબ્દોમાં: ફરી લખવું",
              "Reformulation opens a second door into the same sentence: બીજા શબ્દોમાં · એટલે કે · "
              "વ્યવહારમાં. One marker per sentence.",
              [V("બીજા શબ્દોમાં", "beejaa shabdomaa", "in other words", "phrase"),
               V("એટલે કે", "etle ke", "that is", "phrase"),
               V("વ્યવહારમાં", "vyavahaarmaa", "in practice", "phrase"),
               V("અર્થ", "arth", "meaning", "noun"),
               V("સ્પષ્ટ", "spasht", "clear", "adjective")],
              G("Reformulation frame",
                "બીજા શબ્દોમાં … · એટલે કે … · વ્યવહારમાં …",
                "Reformulation gives the reader a second chance at the same content: માર્જિન પાંચ "
                "ટકાથી નીચે છે — બીજા શબ્દોમાં, ભૂલની જગ્યા નથી. એટલે કે introduces a definition, "
                "વ્યવહારમાં the consequence.",
                [X("બીજા શબ્દોમાં, ભૂલની જગ્યા નથી.", "Beejaa shabdomaa, bhoolni jagyaa nathi.", "In other words, there is no room for error."),
                 X("એટલે કે: બે અઠવાડિયાં.", "Etle ke: be athvadiyaan.", "That is: two weeks."),
                 X("વ્યવહારમાં, પ્રયોગ પહેલા કરવો પડશે.", "Vyavahaarmaa, prayog pahelaa karvo padshe.", "In practice, the trial has to come first.")],
                [("બીજા શબ્દોમાં, એટલે કે, વ્યવહારમાં, ભૂલ નહીં.", "બીજા શબ્દોમાં, ભૂલની જગ્યા નથી.", "One reformulation marker per sentence."),
                 ("એટલે કે કે બે અઠવાડિયાં.", "એટલે કે: બે અઠવાડિયાં.", "એટલે કે takes a phrase, not a second કે.")]),
              [D("Editor", "આ વાક્ય ભારે છે.", "Aa vaakya bhaare chhe.", "This sentence is heavy."),
               D("Analyst", "બીજા શબ્દોમાં: ભૂલની જગ્યા નથી.", "Beejaa shabdomaa: bhoolni jagyaa nathi.", "In other words: there is no room for error."),
               D("Editor", "અને વ્યવહારમાં?", "Ane vyavahaarmaa?", "And in practice?"),
               D("Analyst", "પ્રયોગ પહેલા કરવો પડશે.", "Prayog pahelaa karvo padshe.", "The trial has to come first.")],
              WS("Reformulation worksheet", [
                  T("Reformulate.", ["in other words, there is no room for error", "that is: two weeks"],
                    ["બીજા શબ્દોમાં, ભૂલની જગ્યા નથી.", "એટલે કે: બે અઠવાડિયાં."]),
                  T("Bring it to practice.", ["in practice, the trial has to come first", "make it clearer"],
                    ["વ્યવહારમાં, પ્રયોગ પહેલા કરવો પડશે.", "વધુ સ્પષ્ટ કરો"]),
              ])),
            L("સમાપન: એક નિર્ણય, એક જવાબદાર",
              "A closing does not repeat the argument; it converts it: નિષ્કર્ષમાં અમે મંજૂરી માગીએ "
              "છીએ · જવાબદાર … · મુદત …",
              [V("સમાપન", "samaapan", "closing", "noun"),
               V("મંજૂરી", "manjoori", "approval", "noun"),
               V("માગવું", "maagvun", "to ask for", "verb"),
               V("આગળનું પગલું", "aagalnun pagalun", "next step", "phrase"),
               V("તારીખ", "taarikh", "date", "noun")],
              G("Closing frame",
                "નિષ્કર્ષમાં … મંજૂરી માગીએ છીએ · આગળનું પગલું … · જવાબદાર …",
                "The closing asks for one decision (મંજૂરી માગીએ છીએ), names the next step and gives "
                "it an owner. If the last line could be deleted without changing anything, the "
                "closing has not closed.",
                [X("નિષ્કર્ષમાં, અમે પ્રયોગની મંજૂરી માગીએ છીએ.", "Nishkarshmaa, ame prayogni manjoori maagie chhie.", "In conclusion, we ask for approval of the trial."),
                 X("આગળનું પગલું: પંદર દિવસનો પ્રયોગ.", "Aagalnun pagalun: pandar divasno prayog.", "Next step: a fifteen-day trial."),
                 X("જવાબદાર: પ્રોજેક્ટ વિભાગ.", "Javaabdaar: projekt vibhaag.", "Responsible: the project section.")],
                [("નિષ્કર્ષમાં, જેમ કહ્યું તેમ, ફરી કહું છું.", "નિષ્કર્ષમાં, અમે પ્રયોગની મંજૂરી માગીએ છીએ.", "A closing asks for a decision; it does not repeat itself."),
                 ("આગળનું પગલું છે કે પ્રયોગ.", "આગળનું પગલું: પ્રયોગ.", "The step is named as a phrase, not with કે.")]),
              [D("Editor", "સમાપન કેમ લખું?", "Samaapan kem lakhun?", "How do I write the closing?"),
               D("Analyst", "«નિષ્કર્ષમાં, અમે પ્રયોગની મંજૂરી માગીએ છીએ».", "«Nishkarshmaa, ame prayogni manjoori maagie chhie».", "'In conclusion, we ask for approval of the trial'."),
               D("Editor", "અને છેલ્લી લીટી?", "Ane chhelli leeti?", "And the last line?"),
               D("Analyst", "આગળનું પગલું અને જવાબદાર.", "Aagalnun pagalun ane javaabdaar.", "The next step and the owner.")],
              WS("Closing worksheet", [
                  T("Close the text.", ["in conclusion, we ask for approval of the trial", "next step: a fifteen-day trial"],
                    ["નિષ્કર્ષમાં, અમે પ્રયોગની મંજૂરી માગીએ છીએ.", "આગળનું પગલું: પંદર દિવસનો પ્રયોગ."]),
                  T("Name the owner.", ["responsible: the project section", "the closing names a decision and an owner"],
                    ["જવાબદાર: પ્રોજેક્ટ વિભાગ", "સમાપનમાં નિર્ણય અને જવાબદાર હોય"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Formal Gujarati keeps fixed furniture the way a wedding hall keeps chairs: the "
                 "reference line, the subject line, the closing (આભાર સહ, નમ્ર વિનંતી) and the "
                 "plural first person for an institution (અમે … માગીએ છીએ). Nothing is improvised, "
                 "and that is the point — a letter that uses the right hinges is read as competent "
                 "before its first argument is weighed."),
        source_url="https://en.wikipedia.org/wiki/Gujarati_literature",
        reading=("સંદર્ભ: તમારો પત્ર ૩ મે. વિષય: પાર્સલ વિલંબની ભરપાઈ. હકીકત: પાર્સલ નવ દિવસ મોડું "
                 "આવ્યું અને કોઈ જાણ કરવામાં ન આવી. કારણ: અમને કોઈ સંદેશ મળ્યો નથી. માંગ: ખર્ચની "
                 "ભરપાઈ દસ દિવસમાં. ટૂંકમાં: એક વિલંબ, એક માંગ, એક તારીખ. નિષ્કર્ષમાં, અમે આ મુદ્દે "
                 "લેખિત જવાબ માગીએ છીએ. આભાર સહ."),
        reading_gloss=("Reference: your letter of 3 May. Subject: refund for the parcel delay. Fact: "
                       "the parcel arrived nine days late and no notice was given. Grounds: we "
                       "received no message. Request: refund of the cost within ten days. In short: "
                       "one delay, one request, one date. In conclusion, we ask for a written reply "
                       "on this point. With thanks."),
        listening=("Editor: સાર લખ્યો?<br>Analyst: ટૂંકમાં: ત્રણ મુદ્દા, એક મંજૂર, બે બાકી.<br>"
                   "Editor: મુખ્ય મુદ્દો?<br>Analyst: ખર્ચ; નિષ્કર્ષમાં મંજૂરી માગીએ છીએ."),
        listening_gloss=("Editor: Did you write the summary? Analyst: In short: three points, one "
                         "approved, two pending. Editor: The main point? Analyst: The cost; in "
                         "conclusion we ask for approval."),
        voice_tag=VOICE,
        idioms=[
            ("નીચેના કારણોસર", "on the following grounds", "on the following grounds"),
            ("જવાબદાર", "responsible", "the person responsible"),
            ("મુદત", "deadline", "the deadline"),
            ("હકીકત", "fact", "the fact"),
            ("માંગ", "demand", "the request"),
            ("ખેદ છે", "there is regret", "we regret"),
            ("બીજા શબ્દોમાં", "in other words", "in other words"),
            ("ટૂંકમાં", "in short", "in short"),
            ("આગળનું પગલું", "the next step", "the next step"),
            ("આભાર સહ", "with thanks", "with thanks"),
        ],
        mistakes=[
            ("વિષય: નવી કિંમત મંજૂર કરો.", "વિષય: નવી કિંમતની મંજૂરી.", "A subject line is a noun phrase."),
            ("અમે બદલી આપીશું, કદાચ.", "અમે ત્રણ દિવસમાં બદલી આપીશું.", "A repair carries a date."),
            ("ટૂંકમાં, બધું ઠીક છે.", "ટૂંકમાં: ત્રણ મુદ્દા, એક મંજૂર, બે બાકી.", "A summary counts and selects."),
        ],
        task_title="Write one formal Gujarati letter and its five-line summary",
        task_instructions=("Take a real grievance — a late delivery, a wrong bill, a cancelled "
                           "appointment — and write the Gujarati letter in three parts: સંદર્ભ and "
                           "વિષય at the top, then હકીકત, કારણ and માંગ with a date, and close with "
                           "આભાર સહ. Then write the same content as a five-line internal summary "
                           "(ટૂંકમાં) with one main point (મુખ્ય મુદ્દો) and one next step with an "
                           "owner. If the letter is longer than the summary by more than a page, the "
                           "letter is repeating itself."),
    ),
    "test": [
        ("translate_en", "Say: In conclusion, we ask for approval of the trial.", "નિષ્કર્ષમાં, અમે પ્રયોગની મંજૂરી માગીએ છીએ."),
        ("translate_gu", "ટૂંકમાં: ત્રણ મુદ્દા, એક મંજૂર, બે બાકી.", "In short: three points, one approved, two pending."),
        ("multiple_choice", "Which is the correct subject line?", "વિષય: નવી કિંમતની મંજૂરી"),
        ("fill_in_the_blank", "માંગ: ખર્ચની ભરપાઈ દસ દિવસ___ .", "માં"),
        ("word_selection", "Select the Gujarati for 'on the following grounds'.", "નીચેના કારણોસર"),
        ("error_correction", "એટલું જ નહીં ખર્ચ ઘટે, તેથી સમય બચે.", "એટલું જ નહીં ખર્ચ ઘટે, પણ સમય બચે."),
        ("dialogue_completion", "Complete: અહેવાલનો સાર? — ___ (three points, one approved, two pending)", "ટૂંકમાં: ત્રણ મુદ્દા, એક મંજૂર, બે બાકી"),
        ("matching", "Match આભાર સહ to its meaning.", "with thanks"),
        ("reading_comprehension", "પાર્સલ નવ દિવસ મોડું આવ્યું. How late was the parcel?", "nine days"),
        ("inference", "«પદ્ધતિ જાહેર નથી» — what is the writer doing?", "questioning the evidence"),
        ("main_idea", "જવાબદાર: પ્રોજેક્ટ વિભાગ; મુદત: ત્રીસ જૂન. What is this?", "the owner and deadline of a decision"),
        ("detail_identification", "અમે ત્રણ દિવસમાં બદલી આપીશું. When will the replacement come?", "within three days"),
    ],
}

HALFSTEPS["C1+"] = {
    "title": "Gujarati C1+ — Precision, register and mediation",
    "native": NATIVE,
    "goals": [
        "Say exactly how sure you are, and what would change your mind",
        "Move the same report up and down the register scale",
        "Read a long text in Gujarati and give it back in three sentences",
    ],
    "units": [
        {"id": "C1+-U1", "title": "ચોકસાઈ", "lessons": [
            L("ચોક્કસ, સંભવ, શક્ય",
              "Certainty is a ladder, and Gujarati marks every rung: ચોક્કસ (certain) · સંભવ છે કે "
              "(probable) · શક્ય છે કે (possible) · શક્ય નથી (out of the question). Choosing a rung "
              "is a claim about evidence.",
              [V("ચોક્કસ", "chokkas", "certain, exact", "adjective"),
               V("સંભવ", "sambhav", "probable", "adjective"),
               V("શક્ય", "shakya", "possible", "adjective"),
               V("અંદાજે", "andaaje", "approximately", "adverb"),
               V("આશરે", "aashare", "about, roughly", "adverb")],
              G("Certainty ladder",
                "ચોક્કસ · સંભવ છે કે … · શક્ય છે કે … · શક્ય નથી",
                "ચોક્કસ takes a plain present, સંભવ છે કે and શક્ય છે કે take a કે-clause, and the "
                "negation શક્ય નથી closes the door completely. સંભવ is for a forecast with evidence; "
                "શક્ય is for one without.",
                [X("ચોક્કસ, પ્રયોગ સમયસર પૂરો થશે.", "Chokkas, prayog samaysar pooro thashe.", "Certainly, the trial will finish on time."),
                 X("સંભવ છે કે ખર્ચ ઘટશે.", "Sambhav chhe ke kharch ghatashe.", "It is probable that the cost will fall."),
                 X("શક્ય છે કે મુદત લંબાય.", "Shakya chhe ke mudat lambaay.", "It is possible that the deadline extends.")],
                [("સંભવ, ખર્ચ ઘટશે.", "સંભવ છે કે ખર્ચ ઘટશે.", "સંભવ needs છે કે before its clause."),
                 ("શક્ય છે ખર્ચ ઘટે.", "શક્ય છે કે ખર્ચ ઘટે.", "The કે is not optional in શક્ય છે કે.")]),
              [D("Editor", "તમે કેટલા ચોક્કસ છો?", "Tame ketlaa chokkas chho?", "How certain are you?"),
               D("Analyst", "સંભવ છે કે ખર્ચ ઘટશે; ચોક્કસ નથી કહી શકતો.", "Sambhav chhe ke kharch ghatashe; chokkas nathi kahi shakto.", "It is probable that the cost will fall; I cannot say certainly."),
               D("Editor", "અને શક્યતા?", "Ane shakyataa?", "And the possibility?"),
               D("Analyst", "શક્ય છે કે મુદત લંબાય, પણ એ અંદાજે.", "Shakya chhe ke mudat lambaay, pan e andaaje.", "It is possible that the deadline extends, but that is a guess.")],
              WS("Certainty worksheet", [
                  T("Climb the ladder.", ["it is probable that the cost will fall", "it is possible that the deadline extends"],
                    ["સંભવ છે કે ખર્ચ ઘટશે.", "શક્ય છે કે મુદત લંબાય."]),
                  T("Qualify.", ["certainly, the trial will finish on time", "approximately two weeks"],
                    ["ચોક્કસ, પ્રયોગ સમયસર પૂરો થશે.", "અંદાજે બે અઠવાડિયાં"]),
              ])),
            L("અનુમાન અને પુરાવો ગળી ન લેવો",
              "Between them, અનુમાન (inference) and પુરાવો (evidence) must stay apart: પુરાવા પરથી લાગે "
              "છે … · પુરાવો તો એટલો જ છે કે … A conjecture dressed as evidence is the most expensive "
              "sentence in a report.",
              [V("અનુમાન", "anumaan", "inference, guess", "noun"),
               V("પુરાવો", "puraavo", "evidence", "noun"),
               V("સંબંધ", "sambandh", "link, relation", "noun"),
               V("ફેરફાર", "ferfaar", "change", "noun"),
               V("કારણભૂત", "kaaranbhoot", "causal", "adjective")],
              G("Evidence vs inference",
                "પુરાવો … છે · પુરાવા પરથી લાગે છે કે … · અનુમાન … છે · કારણભૂત સંબંધ નથી",
                "The evidence is stated first and with a plain છે; the inference is the second "
                "sentence and is marked with લાગે છે; the limit is said outright — કારણભૂત સંબંધ "
                "સાબિત થતો નથી (no causal link is proved).",
                [X("પુરાવો છ જ મહિનાનો છે.", "Puraavo chha ja mahinaano chhe.", "The evidence covers only six months."),
                 X("પુરાવા પરથી લાગે છે કે વેચાણ વધે છે.", "Puraavaa parthi laage chhe ke vechaan vadhe chhe.", "From the evidence it seems that sales are rising."),
                 X("કારણભૂત સંબંધ સાબિત થતો નથી.", "Kaaranbhoot sambandh saabit thato nathi.", "No causal link is proved.")],
                [("પુરાવો સાબિત કરે છે કે વેચાણ વધ્યું.", "પુરાવા પરથી લાગે છે કે વેચાણ વધ્યું.", "Two numbers moving together is an inference, not proof."),
                 ("એટલે નફો એટલે જ વધ્યો.", "એટલે નફો વધ્યો, પણ કારણ સાબિત નથી.", "A cause needs its own evidence.")]),
              [D("Editor", "તો વેચાણ વધ્યું?", "To vechaan vadhyun?", "So did sales rise?"),
               D("Analyst", "પુરાવો છ મહિનાનો છે, અને પુરાવા પરથી લાગે છે કે વધ્યું.", "Puraavo chha mahinaano chhe, ane puraavaa parthi laage chhe ke vadhyun.", "The evidence covers six months, and from it, it seems sales rose."),
               D("Editor", "કારણ?", "Kaaran?", "The cause?"),
               D("Analyst", "કારણભૂત સંબંધ સાબિત થતો નથી.", "Kaaranbhoot sambandh saabit thato nathi.", "No causal link is proved.")],
              WS("Evidence worksheet", [
                  T("Separate evidence from inference.", ["the evidence covers only six months", "from the evidence it seems that sales are rising"],
                    ["પુરાવો છ જ મહિનાનો છે.", "પુરાવા પરથી લાગે છે કે વેચાણ વધે છે."]),
                  T("State the limit.", ["no causal link is proved", "that is an inference, not evidence"],
                    ["કારણભૂત સંબંધ સાબિત થતો નથી.", "એ અનુમાન છે, પુરાવો નહીં"]),
              ])),
            L("ઉદાહરણથી સિદ્ધાંત",
              "An example becomes a principle only through language: ઉદાહરણ તરીકે … · ઉપરથી સિદ્ધાંત "
              "એવો નીકળે છે કે … · જ્યાં સુધી … ત્યાં સુધી.",
              [V("ઉદાહરણ", "udaaharan", "example", "noun"),
               V("સિદ્ધાંત", "siddhaant", "principle", "noun"),
               V("નીકળવું", "neekalvun", "to emerge, to come out", "verb"),
               V("શરત", "sharat", "condition", "noun"),
               V("લાગુ", "laagu", "applicable", "adjective")],
              G("Principle frame",
                "ઉદાહરણ તરીકે … · ઉપરથી સિદ્ધાંત એવો નીકળે છે કે … · જ્યાં સુધી … ત્યાં સુધી",
                "The example is marked (ઉદાહરણ તરીકે) and then the principle is derived with ઉપરથી "
                "… નીકળે છે. The scope is fenced with જ્યાં સુધી … ત્યાં સુધી — outside those limits the "
                "principle is not being claimed.",
                [X("ઉદાહરણ તરીકે, ત્રણ ગ્રાહકોએ ફરિયાદ કરી.", "Udaaharan tarike, tran graahako-e fariyaad kari.", "For example, three customers complained."),
                 X("ઉપરથી સિદ્ધાંત એવો નીકળે છે કે તપાસ કરવી પડે.", "Uparthi siddhaant evo neekale chhe ke tapas karvi pade.", "From this the principle follows that a check is needed."),
                 X("જ્યાં સુધી શરત પૂરી ન થાય, ત્યાં સુધી લાગુ નથી.", "Jyaan sudhi sharat poori na thaay, tyaan sudhi laagu nathi.", "Until the condition is met, it does not apply.")],
                [("ઉદાહરણ તરીકે, એટલે સિદ્ધાંત એ છે કે …", "ઉપરથી સિદ્ધાંત એવો નીકળે છે કે …", "The principle needs its own sentence and its marker."),
                 ("દરેક જગ્યાએ લાગુ છે.", "જ્યાં સુધી શરત પૂરી થાય, ત્યાં સુધી લાગુ છે.", "A principle without a scope claims too much.")]),
              [D("Editor", "એક ઉદાહરણ છે, સિદ્ધાંત નહીં.", "Ek udaaharan chhe, siddhaant nahi.", "It is one example, not a principle."),
               D("Analyst", "સાચું: ઉપરથી સિદ્ધાંત એવો નીકળે છે કે તપાસ કરવી પડે.", "Saachun: uparthi siddhaant evo neekale chhe ke tapas karvi pade.", "True: from this the principle follows that a check is needed."),
               D("Editor", "ક્યાં સુધી?", "Kyaan sudhi?", "To what extent?"),
               D("Analyst", "જ્યાં સુધી શરત પૂરી ન થાય, ત્યાં સુધી લાગુ નથી.", "Jyaan sudhi sharat poori na thaay, tyaan sudhi laagu nathi.", "Until the condition is met, it does not apply.")],
              WS("Principle worksheet", [
                  T("Mark the example.", ["for example, three customers complained", "from this the principle follows that a check is needed"],
                    ["ઉદાહરણ તરીકે, ત્રણ ગ્રાહકોએ ફરિયાદ કરી.", "ઉપરથી સિદ્ધાંત એવો નીકળે છે કે તપાસ કરવી પડે."]),
                  T("Fence the scope.", ["until the condition is met, it does not apply", "it applies only within these limits"],
                    ["જ્યાં સુધી શરત પૂરી ન થાય, ત્યાં સુધી લાગુ નથી.", "ફક્ત આ મર્યાદામાં લાગુ છે"]),
              ])),
        ]},
        {"id": "C1+-U2", "title": "શૈલીની સફર", "lessons": [
            L("એક અહેવાલ, ત્રણ સ્તર",
              "The same paragraph travels: official (આથી જણાવાય છે કે) · neutral (તેથી આપણે કરીએ) · "
              "familiar (તો ચાલો, કરી નાખીએ). Register is a choice, and the content should survive "
              "all three.",
              [V("આથી", "aathi", "hence", "adverb"),
               V("આપણે", "aapne", "we (inclusive)", "pronoun"),
               V("જણાવવું", "janaavvun", "to inform", "verb"),
               V("ચાલો", "chaalo", "come on, let us", "interjection"),
               V("ને", "ne", "informal tag", "particle")],
              G("Register dial",
                "આથી જણાવાય છે કે … · તેથી આપણે … કરીએ · તો ચાલો, … નાખીએ",
                "The official layer uses the passive (જણાવાય છે) and no pronouns, the neutral uses "
                "આપણે with a suggestion, and the familiar uses ચાલો with an emphatic verb. Moving "
                "down the scale means dropping formality, not facts.",
                [X("આથી જણાવાય છે કે પ્રયોગ મંજૂર થયો.", "Aathi janaavaay chhe ke prayog manjoor thayo.", "Hence it is informed that the trial was approved."),
                 X("તેથી આપણે પ્રયોગ શરૂ કરીએ.", "Tethi aapne prayog sharu karie.", "Therefore let us start the trial."),
                 X("તો ચાલો, પ્રયોગ કરી નાખીએ.", "To chaalo, prayog kari naakhie.", "Come on then, let us just run the trial.")],
                [("આથી જણાવાય છે કે ચાલો, કરી નાખીએ.", "આથી જણાવાય છે કે પ્રયોગ મંજૂર થયો.", "The official layer keeps the passive; it does not use ચાલો."),
                 ("તો ચાલો, પ્રયોગ મંજૂર થયો.", "તો ચાલો, પ્રયોગ કરી નાખીએ.", "At the familiar level the sentence is an invitation, not a report.")]),
              [D("Editor", "એ જ સંદેશ, સત્તાવાર.", "E ja sandesh, sattaavaar.", "The same message, officially."),
               D("Analyst", "«આથી જણાવાય છે કે પ્રયોગ મંજૂર થયો».", "«Aathi janaavaay chhe ke prayog manjoor thayo».", "'Hence it is informed that the trial was approved'."),
               D("Editor", "અને મિત્રને?", "Ane mitrane?", "And to a friend?"),
               D("Analyst", "«તો ચાલો, પ્રયોગ કરી નાખીએ».", "«To chaalo, prayog kari naakhie».", "'Come on then, let us just run it'.")],
              WS("Register worksheet", [
                  T("Write it officially.", ["hence it is informed that the trial was approved", "no pronouns in the official layer"],
                    ["આથી જણાવાય છે કે પ્રયોગ મંજૂર થયો.", "સત્તાવાર સ્તરે સર્વનામ ન વપરાય"]),
                  T("Say it to a colleague.", ["therefore let us start the trial", "come on then, let us just run the trial"],
                    ["તેથી આપણે પ્રયોગ શરૂ કરીએ.", "તો ચાલો, પ્રયોગ કરી નાખીએ."]),
              ])),
            L("અંડરસ્ટેટમેન્ટ: થોડું કહીને બહુ કહેવું",
              "English understatement has a Gujarati gear too: થોડો સમય લાગશે (a little time) for two "
              "months · ઠીક ઠીક (so-so) for bad · વાંધો નથી (no objection) for strong disagreement "
              "held back.",
              [V("થોડું", "thodun", "a little", "adjective"),
               V("ઠીક ઠીક", "theek theek", "so-so, tolerable", "phrase"),
               V("વાંધો નથી", "vaandho nathi", "no objection", "phrase"),
               V("સાવ", "saav", "altogether", "adverb"),
               V("જરા", "jaraa", "a bit", "adverb")],
              G("Understatement",
                "થોડો સમય લાગશે · ઠીક ઠીક છે · વાંધો નથી, પણ …",
                "Understatement works only where both speakers know what the plain statement would "
                "have been. In writing it is risky: the reader may take ઠીક ઠીક literally, which is "
                "why reports keep the plain word.",
                [X("પ્રયોગમાં થોડો સમય લાગશે — બે મહિના.", "Prayogmaa thodo samay laagshe — be mahinaa.", "The trial will take a little time — two months."),
                 X("વાત ઠીક ઠીક ચાલી.", "Vaat theek theek chaali.", "The talk went so-so."),
                 X("વાંધો નથી, પણ બજેટ બાકી રહે છે.", "Vaandho nathi, pan bajet baaki rahe chhe.", "No objection, but the budget remains pending.")],
                [("એકદમ ખરાબ, ખૂબ ખરાબ.", "ઠીક ઠીક ચાલી.", "Between colleagues the bad news often arrives understated."),
                 ("વાંધો નથી, અને હું સાવ ખુશ છું.", "વાંધો નથી, પણ બજેટ બાકી રહે છે.", "The held-back objection is named after પણ.")]),
              [D("Editor", "પ્રયોગ કેમ ચાલ્યો?", "Prayog kem chaalyo?", "How did the trial go?"),
               D("Analyst", "ઠીક ઠીક ચાલ્યો.", "Theek theek chaalyo.", "So-so."),
               D("Editor", "એટલે?", "Etle?", "That means?"),
               D("Analyst", "બજેટ બાકી છે; બાકી ઠીક છે.", "Bajet baaki chhe; baaki theek chhe.", "The budget is pending; the rest is fine.")],
              WS("Understatement worksheet", [
                  T("Understate.", ["the trial will take a little time — two months", "the talk went so-so"],
                    ["પ્રયોગમાં થોડો સમય લાગશે — બે મહિના.", "વાત ઠીક ઠીક ચાલી."]),
                  T("Drop the hint.", ["no objection, but the budget remains pending", "the rest is fine"],
                    ["વાંધો નથી, પણ બજેટ બાકી રહે છે.", "બાકી ઠીક છે"]),
              ])),
            L("મૂળ લય જાળવવો: વાક્ય હલાવવું",
              "Keeping an author's rhythm means playing with word order: the same three words (ક્યારેય "
              "નહીં) can end the sentence or start it, and the pause moves with them.",
              [V("લય", "lay", "rhythm", "noun"),
               V("વાક્ય", "vaakya", "sentence", "noun"),
               V("તોલ", "tol", "balance, weight", "noun"),
               V("ઝોક", "jhok", "stress, inclination", "noun"),
               V("પુનરાવર્તન", "punaraavartan", "repetition", "noun")],
              G("Rhythm tools",
                "… વૈશાખી? કદી નહીં · કદી નહીં, એ વાત ખોટી છે · પુનરાવર્તન અને વિરામ",
                "Move the stress to the front for a decision (કદી નહીં, …) and to the end for a "
                "conclusion (… કદી નહીં). Repetition is a tool, not a fault — but only once per "
                "paragraph.",
                [X("એ વાત કદી નહીં.", "E vaat kadi nahi.", "That never."),
                 X("કદી નહીં, એ વાત સાચી નથી.", "Kadi nahi, e vaat saachi nathi.", "Never — that claim is not true."),
                 X("વારંવાર, વારંવાર પૂછવું પડ્યું.", "Vaaravaar, vaaravaar poochhvun padyun.", "Again and again it had to be asked.")],
                [("કદી, એ વાત, નહીં કદી.", "એ વાત કદી નહીં.", "The stressed word lands at one end of the sentence, not both."),
                 ("પુનરાવર્તન પુનરાવર્તન પુનરાવર્તન.", "વારંવાર, વારંવાર પૂછવું પડ્યું.", "One doubling per paragraph.")]),
              [D("Editor", "આ લીટી નરમ છે.", "Aa leeti naram chhe.", "This line is soft."),
               D("Analyst", "તો ઝોક પહેલા: «કદી નહીં, એ વાત સાચી નથી».", "To jhok pahelaa: «Kadi nahi, e vaat saachi nathi».", "Then stress first: 'Never — that claim is not true'."),
               D("Editor", "અને છેલ્લે?", "Ane chhelle?", "And at the end?"),
               D("Analyst", "«એ વાત આપણે કદી નહીં કરીએ».", "«E vaat aapne kadi nahi karie».", "'We will never do that'.")],
              WS("Rhythm worksheet", [
                  T("Stress first.", ["never — that claim is not true", "that never"],
                    ["કદી નહીં, એ વાત સાચી નથી.", "એ વાત કદી નહીં."]),
                  T("Repeat once.", ["again and again it had to be asked", "we will never do that"],
                    ["વારંવાર, વારંવાર પૂછવું પડ્યું.", "એ વાત આપણે કદી નહીં કરીએ."]),
              ])),
        ]},
        {"id": "C1+-U3", "title": "વચ્ચે ઊભા રહીને", "lessons": [
            L("સરળ શબ્દોમાં — અને શું ખોવાયું",
              "Mediation has two halves: the plain rendering and the honest note about what was lost. "
              "સરળ શબ્દોમાં … · નોંધ: આમાં ઘોંઘાટ ખોવાય છે.",
              [V("સરળ", "saral", "simple", "adjective"),
               V("નોંધ", "nondh", "note", "noun"),
               V("ખોવાવું", "khovaavvun", "to be lost", "verb"),
               V("છટા", "chhataa", "suggestion, nuance", "noun"),
               V("ભાવ", "bhaav", "sense, feeling", "noun")],
              G("Mediation frame",
                "સરળ શબ્દોમાં … · અર્થ થાય કે … · નોંધ: … ખોવાય છે",
                "The rendering comes first with સરળ શબ્દોમાં, the sense is fixed with એટલે કે, and the "
                "loss is recorded in a નોંધ line. The note is what makes the mediation honest rather "
                "than merely convenient.",
                [X("સરળ શબ્દોમાં: ખર્ચ વધે છે.", "Saral shabdomaa: kharch vadhe chhe.", "In simple words: the cost is rising."),
                 X("અર્થ થાય કે પ્રયોગ પહેલો કરવો પડશે.", "Arth thaay ke prayog pahelo karvo padshe.", "It means that the trial has to come first."),
                 X("નોંધ: અસલમાં થોડી છટા ખોવાય છે.", "Nondh: asalmaa thodi chhataa khovaay chhe.", "Note: some nuance is lost from the original.")],
                [("સરળ શબ્દોમાં, અને બધું એ જ છે.", "સરળ શબ્દોમાં … ; નોંધ: થોડી છટા ખોવાય છે.", "A plain rendering always loses something; say what."),
                 ("અર્થ થાય કે, અર્થ થાય કે ખર્ચ વધે.", "અર્થ થાય કે ખર્ચ વધે.", "One mediation marker per sentence.")]),
              [D("Editor", "અસલ લખાણ ભારે છે.", "Asal lakhaan bhaare chhe.", "The original text is heavy."),
               D("Analyst", "સરળ શબ્દોમાં: ખર્ચ વધે છે, પ્રયોગ પહેલો કરવો પડશે.", "Saral shabdomaa: kharch vadhe chhe, prayog pahelo karvo padshe.", "In simple words: costs are rising, the trial has to come first."),
               D("Editor", "કંઈ ખોવાયું?", "Kain khovaayun?", "Did anything get lost?"),
               D("Analyst", "નોંધ: થોડી છટા ખોવાય છે.", "Nondh: thodi chhataa khovaay chhe.", "Note: some nuance is lost.")],
              WS("Mediation worksheet", [
                  T("Mediate in plain words.", ["in simple words: the cost is rising", "it means that the trial has to come first"],
                    ["સરળ શબ્દોમાં: ખર્ચ વધે છે.", "અર્થ થાય કે પ્રયોગ પહેલો કરવો પડશે."]),
                  T("Record the loss.", ["note: some nuance is lost from the original", "the note keeps the mediation honest"],
                    ["નોંધ: અસલમાં થોડી છટા ખોવાય છે.", "નોંધ મેડિએશનને પ્રામાણિક રાખે છે"]),
              ])),
            L("સાંભળેલું આગળ કહેવું: એમણે કહ્યું કે",
              "Reported speech keeps the trail: એમણે કહ્યું કે … · મારા મતે નહીં, પણ એમની દલીલ છે "
              "કે … Attribution and opinion travel in separate sentences.",
              [V("એમણે", "emne", "they (respectful)", "pronoun"),
               V("કહ્યું", "kahyun", "said", "verb"),
               V("દલીલ", "daleel", "argument", "noun"),
               V("સંકેત", "sanket", "indication", "noun"),
               V("વળગણ", "valgan", "attachment, bias", "noun")],
              G("Reported frame",
                "એમણે કહ્યું કે … · એમની દલીલ છે કે … · મારી નોંધ …",
                "The attribution is repeated with each claim (એમણે કહ્યું કે / એમની દલીલ છે કે) so "
                "the listener always knows whose sentence is being spoken. Agreement, if any, is a "
                "separate sentence.",
                [X("એમણે કહ્યું કે પ્રયોગ પહેલો જોઈએ.", "Emne kahyun ke prayog pahelo joie.", "They said that the trial should come first."),
                 X("એમની દલીલ છે કે ખર્ચ ઘટશે.", "Emni daleel chhe ke kharch ghatashe.", "Their argument is that the cost will fall."),
                 X("મારી નોંધ: સ્રોત પુરાવો નથી.", "Maari nondh: srot puraavo nathi.", "My note: a source is not evidence.")],
                [("એમણે કહ્યું કે પ્રયોગ પહેલો જોઈએ, અને હું સહમત છું કે …, એમણે કહ્યું.", "એમણે કહ્યું કે પ્રયોગ પહેલો જોઈએ. હું સહમત છું.", "Attribution and agreement are separate sentences."),
                 ("એમની દલીલ કે ખર્ચ ઘટશે.", "એમની દલીલ છે કે ખર્ચ ઘટશે.", "દલીલ છે કે, never દલીલ કે alone.")]),
              [D("Editor", "એમણે શું કહ્યું?", "Emne shu kahyun?", "What did they say?"),
               D("Analyst", "એમણે કહ્યું કે પ્રયોગ પહેલો જોઈએ; એમની દલીલ છે કે ખર્ચ ઘટશે.", "Emne kahyun ke prayog pahelo joie; emni daleel chhe ke kharch ghatashe.", "They said the trial should come first; their argument is that the cost will fall."),
               D("Editor", "તમે?", "Tame?", "And you?"),
               D("Analyst", "મારી નોંધ: સ્રોત પુરાવો નથી.", "Maari nondh: srot puraavo nathi.", "My note: a source is not evidence.")],
              WS("Reporting worksheet", [
                  T("Report the claim.", ["they said that the trial should come first", "their argument is that the cost will fall"],
                    ["એમણે કહ્યું કે પ્રયોગ પહેલો જોઈએ.", "એમની દલીલ છે કે ખર્ચ ઘટશે."]),
                  T("Add your note.", ["my note: a source is not evidence", "agreement is a separate sentence"],
                    ["મારી નોંધ: સ્રોત પુરાવો નથી.", "સહમતી અલગ વાક્યમાં"]),
              ])),
            L("સ્રોત સાથે અદલાબદલી: મૂળ શબ્દ જાળવવો",
              "At the far end of mediation the original has to survive: અસલમાં «…» શબ્દો છે · મૂળ શબ્દો "
              "જાળવીએ છીએ · ભાષાંતરમાં અર્થ બદલાય નહીં.",
              [V("અસલ", "asal", "original", "noun"),
               V("મૂળ", "mool", "root, original", "adjective"),
               V("ભાષાંતર", "bhaashantar", "translation", "noun"),
               V("જાળવવું", "jaadvvun", "to keep, to preserve", "verb"),
               V("અર્થ", "arth", "meaning", "noun")],
              G("Source frame",
                "અસલમાં «…» શબ્દો છે · મૂળ શબ્દો જાળવીએ છીએ · ભાષાંતર … નથી",
                "The original words are quoted in « », the reader is told they are the original "
                "(અસલમાં «…» શબ્દો છે), and the rendering follows or is withheld. Quoting the source "
                "keeps the disagreement possible.",
                [X("અસલમાં «સરેરાશ બાર ટકા» શબ્દો છે.", "Asalmaa «sareraash baar takaa» shabdo chhe.", "The original says 'an average of twelve per cent'."),
                 X("મૂળ શબ્દો જાળવીએ છીએ.", "Mool shabdo jaadvie chhie.", "We keep the original words."),
                 X("ભાષાંતરમાં અર્થ બદલાતો નથી.", "Bhaashantarmaa arth badalaato nathi.", "The meaning does not change in translation.")],
                [("અસલમાં કંઈક આવું હતું.", "અસલમાં «સરેરાશ બાર ટકા» શબ્દો છે.", "Quote the source, do not paraphrase it into your own claim."),
                 ("મૂળ શબ્દો બદલીએ છીએ, અર્થ પણ.", "મૂળ શબ્દો જાળવીએ છીએ.", "Mediation preserves both words and meaning, or says what it dropped.")]),
              [D("Editor", "સ્રોતમાં શું લખ્યું છે?", "Srotmaa shu lakhyun chhe?", "What does the source say?"),
               D("Analyst", "અસલમાં «સરેરાશ બાર ટકા» શબ્દો છે.", "Asalmaa «sareraash baar takaa» shabdo chhe.", "The original says 'an average of twelve per cent'."),
               D("Editor", "અને તમારું ભાષાંતર?", "Ane tamaarun bhaashantar?", "And your translation?"),
               D("Analyst", "મૂળ શબ્દો જાળવીએ છીએ; અર્થ બદલાતો નથી.", "Mool shabdo jaadvie chhie; arth badalaato nathi.", "We keep the original words; the meaning does not change.")],
              WS("Source worksheet", [
                  T("Quote the source.", ["the original says 'an average of twelve per cent'", "we keep the original words"],
                    ["અસલમાં «સરેરાશ બાર ટકા» શબ્દો છે.", "મૂળ શબ્દો જાળવીએ છીએ."]),
                  T("Guard the meaning.", ["the meaning does not change in translation", "mediation preserves words and meaning"],
                    ["ભાષાંતરમાં અર્થ બદલાતો નથી.", "મેડિએશન શબ્દ અને અર્થ બંને જાળવે"]),
              ])),
        ]},
    ],
    "extra": EXTRA(
        culture=("Gujarati has been a language of trade, translation and the printing press for five "
                 "centuries — Gandhi wrote in it, the Jain and Vaishnav traditions kept manuscripts "
                 "in it, and Ahmedabad has printed in it since the nineteenth century. That history "
                 "is why the half-step ends on mediation rather than persuasion: the grammar of "
                 "quoting, keeping the source's words and recording what a translation drops is "
                 "what a language of merchants and scribes actually needed."),
        source_url="https://en.wikipedia.org/wiki/Gujarati_language",
        reading=("«પુલની મરમ્મત બે મહિના ચાલશે» — અસલમાં આ શબ્દો છે. સરળ શબ્દોમાં: પુલ બંધ રહેશે, "
                 "વાહનવ્યવહાર વળતો રસ્તો લેશે. પુરાવો: છ મહિનાની ગણતરી. પુરાવા પરથી લાગે છે કે ખર્ચ "
                 "વધશે, પણ કારણભૂત સંબંધ સાબિત થતો નથી — એ અનુમાન છે. નોંધ: અસલમાં થોડી છટા ખોવાય "
                 "છે. એમણે કહ્યું કે મુદત ટૂંકી કરવી જોઈએ; મારી નોંધ: સ્રોત પુરાવો નથી."),
        reading_gloss=("'The bridge repairs will take two months' — those are the original words. In "
                       "simple words: the bridge stays closed and traffic takes the longer route. "
                       "Evidence: six months of figures. From the evidence it seems the cost will "
                       "rise, but no causal link is proved — that is an inference. Note: some "
                       "nuance is lost from the original. They said the deadline should be "
                       "shortened; my note: a source is not evidence."),
        listening=("Editor: તમે કેટલા ચોક્કસ છો?<br>Analyst: સંભવ છે કે ખર્ચ ઘટશે; ચોક્કસ નથી.<br>"
                   "Editor: સ્રોતમાં શું છે?<br>Analyst: અસલમાં «સરેરાશ બાર ટકા» શબ્દો છે."),
        listening_gloss=("Editor: How certain are you? Analyst: It is probable that the cost will "
                         "fall; I am not certain. Editor: What does the source say? Analyst: The "
                         "original says 'an average of twelve per cent'."),
        voice_tag=VOICE,
        idioms=[
            ("ચોક્કસ", "certain", "for certain"),
            ("સંભવ છે કે", "it is probable that", "it is probable that"),
            ("પુરાવા પરથી લાગે છે", "it seems from the evidence", "the evidence suggests"),
            ("ઉદાહરણ તરીકે", "for example", "for example"),
            ("જ્યાં સુધી … ત્યાં સુધી", "as far as … so far", "as long as"),
            ("સરળ શબ્દોમાં", "in simple words", "in plain words"),
            ("નોંધ", "note", "a note"),
            ("એમણે કહ્યું કે", "they said that", "they said that"),
            ("મૂળ શબ્દો", "the original words", "the original wording"),
            ("અર્થ થાય કે", "it means that", "it means that"),
        ],
        mistakes=[
            ("સંભવ, ખર્ચ ઘટશે.", "સંભવ છે કે ખર્ચ ઘટશે.", "સંભવ needs છે કે before its clause."),
            ("એમની દલીલ કે ખર્ચ ઘટશે.", "એમની દલીલ છે કે ખર્ચ ઘટશે.", "દલીલ છે કે, never દલીલ કે alone."),
            ("પુરાવો સાબિત કરે છે કે નફો વધ્યો.", "પુરાવા પરથી લાગે છે કે નફો વધ્યો.", "Two figures moving together is an inference, not proof."),
        ],
        task_title="Mediate one Gujarati text for two different readers",
        task_instructions=("Take any Gujarati article of a few hundred words. Write three outputs "
                           "from it: (1) a plain-word rendering for a busy reader (સરળ શબ્દોમાં …), "
                           "with a નોંધ line that records what the plain version dropped; (2) an "
                           "official paragraph using the passive (જણાવાય છે કે), which keeps the "
                           "figures but no pronouns; (3) a spoken summary to a colleague that ends "
                           "with one decision and one owner. Keep the original's key words quoted in "
                           "« » in all three. If any of the three versions claims more certainty "
                           "than the original did, rewrite it."),
    ),
    "test": [
        ("translate_en", "Say: It is probable that the cost will fall.", "સંભવ છે કે ખર્ચ ઘટશે."),
        ("translate_gu", "અસલમાં «સરેરાશ બાર ટકા» શબ્દો છે.", "The original says 'an average of twelve per cent'."),
        ("multiple_choice", "Which sentence reports an inference rather than evidence?", "પુરાવા પરથી લાગે છે કે વેચાણ વધે છે."),
        ("fill_in_the_blank", "એમણે કહ્યું ___ પ્રયોગ પહેલો જોઈએ.", "કે"),
        ("word_selection", "Select the Gujarati for 'in simple words'.", "સરળ શબ્દોમાં"),
        ("error_correction", "એમની દલીલ કે ખર્ચ ઘટશે.", "એમની દલીલ છે કે ખર્ચ ઘટશે."),
        ("dialogue_completion", "Complete: તમે કેટલા ચોક્કસ છો? — ___ (it is probable that the cost will fall)", "સંભવ છે કે ખર્ચ ઘટશે"),
        ("matching", "Match નોંધ to its meaning.", "a note recording what was lost"),
        ("reading_comprehension", "પુરાવો છ મહિનાનો છે. How long is the evidence?", "six months"),
        ("inference", "«કારણભૂત સંબંધ સાબિત થતો નથી» — what is the writer refusing to claim?", "a cause"),
        ("main_idea", "સરળ શબ્દોમાં: ખર્ચ વધે છે. What is the writer doing?", "mediating a text in plain words"),
        ("detail_identification", "જ્યાં સુધી શરત પૂરી ન થાય, ત્યાં સુધી લાગુ નથી. When does it apply?", "once the condition is met"),
    ],
}

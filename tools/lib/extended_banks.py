#!/usr/bin/env python3
"""Authored extra-level banks (EkGuru extension tracks, not CEFR).

A3 = A2→B1 bridge (school, plans, travel, food, friends, weather, shopping, routines).
B3 = B2→C1 bridge (work, news, register, debate, culture, health, tech, narrative).

Vocab, grammar examples and dialogues are in the target language. Practice/quiz/test
items are generated from these authored rows (re-asks, never invented words).

Languages without a pack must be written as content_status=INCOMPLETE.
"""
from __future__ import annotations

def V(t, r, en, pos="noun"):
    return {"t": t, "r": r or "", "en": en, "pos": pos}


def G(title, explain, pattern, examples, mistakes):
    ex = []
    for row in examples:
        if len(row) == 3:
            t, r, en = row
        else:
            t, en = row[0], row[1]
            r = ""
        ex.append({"t": t, "r": r or "", "en": en})
    return {
        "title": title,
        "explain": explain,
        "pattern": pattern,
        "examples": ex,
        "mistakes": list(mistakes),
    }


def D(lines):
    out = []
    for row in lines:
        sp, t, r, en = row
        out.append({"sp": sp, "t": t, "r": r or "", "en": en})
    return out


def lesson(n, title, learn, vocab, grammar, dialogue):
    return {
        "id": "L%d" % n,
        "title": title,
        "learn": learn,
        "vocab": vocab,
        "grammar": grammar,
        "dialogue": dialogue,
    }


# ---------------------------------------------------------------------------
# Packs: code -> level -> [lesson, ...]
# ---------------------------------------------------------------------------
PACKS = {}


def _add(code, level, lessons):
    PACKS.setdefault(code, {})[level] = lessons


def _a3_en():
    return [
        lesson(1, "School and studies",
               "Talk about classes, exams and homework using going-to future for near plans.",
               [V("exam", "", "exam"), V("subject", "", "school subject"), V("homework", "", "homework"),
                V("timetable", "", "class schedule"), V("deadline", "", "due date"), V("revise", "", "review for a test", "verb"),
                V("lecture", "", "lecture"), V("notes", "", "notes")],
               G("going to for plans", "Use be + going to + verb for a plan already decided.",
                 "I/you/we are going to + verb",
                 [("I'm going to revise tonight.", "", "plan for tonight"),
                  ("She's going to miss the lecture.", "", "future result"),
                  ("Are you going to finish the homework?", "", "yes/no plan")],
                 ["Don't say 'I going to' — you need am/is/are.", "Don't use going to for a spontaneous offer (use will)."]),
               D([("Maya", "Have you got an exam tomorrow?", "", "exam check"),
                  ("Leo", "Yes, history. I'm going to revise after class.", "", "plan"),
                  ("Maya", "Want to study together in the library?", "", "offer"),
                  ("Leo", "Yes — the deadline for notes is tonight.", "", "accept")])),
        lesson(2, "Hobbies and free time",
               "Say what you enjoy, how often, and suggest doing something together.",
               [V("hobby", "", "hobby"), V("guitar", "", "guitar"), V("team", "", "sports team"),
                V("practice", "", "practice session"), V("weekend", "", "weekend"), V("join", "", "become a member", "verb"),
                V("concert", "", "concert"), V("sketch", "", "quick drawing")],
               G("verb + -ing after enjoy/like", "After enjoy, like, mind, keep, use the -ing form.",
                 "enjoy/like + verb-ing",
                 [("I enjoy playing guitar at weekends.", "", "enjoy + -ing"),
                  ("She doesn't mind waiting.", "", "mind + -ing"),
                  ("Keep practising if you want to join the team.", "", "keep + -ing")],
                 ["Don't say 'I enjoy to play'.", "Don't drop -ing after mind."]),
               D([("Asha", "What do you do at the weekend?", "", "ask"),
                  ("Ben", "I play guitar. There's a concert on Saturday.", "", "hobby"),
                  ("Asha", "I enjoy sketching. Want to come?", "", "suggest"),
                  ("Ben", "Yes — after football practice.", "", "accept")])),
        lesson(3, "Travel basics",
               "Buy tickets, ask for platforms, and handle a simple delay.",
               [V("platform", "", "train platform"), V("return ticket", "", "round-trip ticket"),
                V("delay", "", "lateness"), V("luggage", "", "bags"), V("gate", "", "airport gate"),
                V("passport", "", "passport"), V("book", "", "reserve", "verb"), V("change", "", "transfer trains", "verb")],
               G("have to for necessity", "Have to expresses an external rule, not a personal wish.",
                 "have/has to + verb",
                 [("You have to show your passport at the gate.", "", "rule"),
                  ("We have to change at Leeds.", "", "travel need"),
                  ("He doesn't have to book today.", "", "no necessity")],
                 ["Don't confuse have to with must for rules you didn't choose.", "Don't say 'he have to'."]),
               D([("Clerk", "Single or return?", "", "ticket type"),
                  ("Nina", "Return, please. Which platform?", "", "ask"),
                  ("Clerk", "Platform 4. There's a short delay.", "", "info"),
                  ("Nina", "Do I have to change?", "", "necessity")])),
        lesson(4, "Food and restaurants",
               "Order food, ask about ingredients, and send something back politely.",
               [V("menu", "", "menu"), V("bill", "", "check to pay"), V("starter", "", "first course"),
                V("allergic", "", "allergic", "adj"), V("spicy", "", "hot with chilli", "adj"),
                V("recommend", "", "suggest", "verb"), V("tip", "", "extra money for service"), V("table", "", "table")],
               G("would like vs want", "Would like is the polite order form in restaurants.",
                 "I'd like + noun / I'd like to + verb",
                 [("I'd like the soup, please.", "", "order"),
                  ("Would you like it spicy?", "", "offer"),
                  ("I'd like to see the menu.", "", "request")],
                 ["Want is fine with friends, blunt with waiters.", "Don't say 'I would like see'."]),
               D([("Waiter", "Are you ready to order?", "", "open"),
                  ("Sam", "I'd like the pasta. Is it spicy?", "", "order"),
                  ("Waiter", "A little. You're not allergic?", "", "check"),
                  ("Sam", "No. The bill at the end, please.", "", "close")])),
        lesson(5, "Friends and social life",
               "Make, accept and refuse invitations without sounding rude.",
               [V("invitation", "", "invite"), V("busy", "", "not free", "adj"), V("catch up", "", "talk after a while", "verb"),
                V("bring", "", "carry with you", "verb"), V("party", "", "party"), V("free", "", "available", "adj"),
                V("maybe", "", "perhaps"), V("next week", "", "the following week")],
               G("Shall we / Why don't we", "These two frames make a suggestion, not an order.",
                 "Shall we + verb? / Why don't we + verb?",
                 [("Shall we meet at seven?", "", "suggestion"),
                  ("Why don't we catch up next week?", "", "softer suggest"),
                  ("Let's bring some food.", "", "inclusive let's")],
                 ["Shall we is a question, not 'shall I you'.", "Don't refuse with only 'no' — give a reason."]),
               D([("Riya", "There's a party on Friday. Shall we go?", "", "invite"),
                  ("Omar", "I'm busy Friday. Why don't we catch up next week?", "", "refuse+alt"),
                  ("Riya", "Sunday? I'm free after six.", "", "new time"),
                  ("Omar", "Perfect. I'll bring dessert.", "", "accept")])),
        lesson(6, "Weather and plans",
               "Describe weather and change a plan because of it.",
               [V("forecast", "", "weather prediction"), V("shower", "", "short rain"), V("humid", "", "damp air", "adj"),
                V("cancel", "", "call off", "verb"), V("indoor", "", "inside", "adj"), V("umbrella", "", "umbrella"),
                V("degree", "", "temperature unit"), V("clear up", "", "become sunny", "verb")],
               G("first conditional", "If + present, will + verb: a real future possibility.",
                 "If + present, will + verb",
                 [("If it rains, we'll cancel the picnic.", "", "real if"),
                  ("If the forecast is clear, we'll walk.", "", "plan"),
                  ("If it doesn't clear up, we'll stay indoor.", "", "negative if")],
                 ["Don't use will in the if-clause.", "Don't say 'If it will rain'."]),
               D([("Jen", "The forecast says showers.", "", "weather"),
                  ("Kai", "If it rains, we'll go to the museum.", "", "plan B"),
                  ("Jen", "Take an umbrella anyway.", "", "advice"),
                  ("Kai", "If it clears up, we'll walk by the river.", "", "plan A")])),
        lesson(7, "Shopping and money",
               "Compare prices, ask for sizes, and talk about refunds.",
               [V("size", "", "clothing size"), V("receipt", "", "proof of purchase"), V("refund", "", "money back"),
                V("discount", "", "reduced price"), V("cash", "", "notes and coins"), V("card", "", "payment card"),
                V("fit", "", "be the right size", "verb"), V("exchange", "", "swap an item", "verb")],
               G("comparatives", "Add -er to short adjectives; use more with long ones.",
                 "cheaper / more expensive than",
                 [("This shirt is cheaper than that one.", "", "-er"),
                  ("The blue one is more expensive.", "", "more"),
                  ("It fits better in size M.", "", "irregular better")],
                 ["Don't say 'more cheaper'.", "Don't forget than in a comparison."]),
               D([("Shop", "Are you paying by card or cash?", "", "pay"),
                  ("Lila", "Card. Have you got this in a smaller size?", "", "size"),
                  ("Shop", "Yes. Keep the receipt for a refund.", "", "policy"),
                  ("Lila", "Is there a student discount?", "", "ask")])),
        lesson(8, "Daily routines and future plans",
               "Describe a weekday and a plan for next month without mixing tenses.",
               [V("commute", "", "travel to work", "verb"), V("shift", "", "work period"), V("alarm", "", "alarm clock"),
                V("save", "", "keep money", "verb"), V("goal", "", "aim"), V("habit", "", "regular action"),
                V("next month", "", "the following month"), V("usually", "", "most days", "adv")],
               G("present simple vs going to", "Present simple is the timetable; going to is your decision.",
                 "I usually + verb  /  I'm going to + verb",
                 [("I usually commute at seven.", "", "habit"),
                  ("I'm going to save next month.", "", "decision"),
                  ("My shift starts at nine.", "", "timetable")],
                 ["Don't use present continuous for a permanent habit.", "Don't use going to for a printed timetable."]),
               D([("Dana", "What time do you usually start?", "", "habit"),
                  ("Ned", "My shift starts at nine. I'm going to change it next month.", "", "plan"),
                  ("Dana", "Why?", "", "why"),
                  ("Ned", "I want a shorter commute. That's the goal.", "", "reason")])),
    ]


def _b3_en():
    return [
        lesson(1, "Workplace communication",
               "Write a short professional email and soften a request.",
               [V("deadline", "", "due time"), V("feedback", "", "comments on work"), V("cc", "", "copy a colleague"),
                V("agenda", "", "meeting list"), V("follow up", "", "check later", "verb"), V("asap", "", "as soon as possible"),
                V("attached", "", "file with the email", "adj"), V("postpone", "", "delay", "verb")],
               G("could you / would you mind", "Indirect requests are the default at work.",
                 "Could you + verb? / Would you mind + -ing?",
                 [("Could you send the agenda by noon?", "", "polite ask"),
                  ("Would you mind postponing the call?", "", "mind + -ing"),
                  ("Please find the file attached.", "", "email formula")],
                 ["Don't open with 'Send me this now' to a manager.", "Would you mind takes -ing, not an infinitive."]),
               D([("Priya", "Could you send feedback on the draft?", "", "ask"),
                  ("Tom", "I'll follow up after lunch. The deadline is tight.", "", "reply"),
                  ("Priya", "Would you mind cc'ing Maya?", "", "add"),
                  ("Tom", "Done. Agenda is attached.", "", "close")])),
        lesson(2, "News and current events",
               "Summarise a news story and mark what is reported, not proven.",
               [V("headline", "", "news title"), V("source", "", "where a story comes from"),
                V("claim", "", "statement not yet proven"), V("according to", "", "as reported by"),
                V("bias", "", "one-sided view"), V("update", "", "later information"),
                V("witness", "", "person who saw it"), V("deny", "", "say it is not true", "verb")],
               G("reported speech (say/tell)", "Backshift the verb when the reporting verb is past.",
                 "They said (that) + past",
                 [("The paper said the talks had failed.", "", "backshift"),
                  ("She told me the source was unnamed.", "", "tell + object"),
                  ("According to witnesses, nobody was hurt.", "", "attribution")],
                 ["Tell needs a person: tell me, not tell that.", "Don't present a claim as a fact."]),
               D([("Ann", "Did you see the headline?", "", "open"),
                  ("Bo", "They said the talks had failed, according to one source.", "", "report"),
                  ("Ann", "The minister denied it an hour later.", "", "update"),
                  ("Bo", "Then we wait for a second source.", "", "caution")])),
        lesson(3, "Formal versus informal register",
               "Rewrite a casual message as a formal one without changing the facts.",
               [V("register", "", "level of formality"), V("slang", "", "very informal words"),
                V("request", "", "polite ask"), V("apologise", "", "say sorry", "verb"),
                V("enquire", "", "ask formally", "verb"), V("yours sincerely", "", "formal sign-off"),
                V("cheers", "", "informal thanks"), V("tone", "", "attitude in wording")],
               G("register recasting", "Same meaning, different social distance.",
                 "Can you…?  →  I would be grateful if you could…",
                 [("Can you send it? → I would be grateful if you could send it.", "", "up-shift"),
                  ("Sorry I'm late. → Please accept my apologies for the delay.", "", "apology"),
                  ("Cheers. → Yours sincerely.", "", "sign-off")],
                 ["Don't mix slang with a formal greeting.", "Yours sincerely follows a named Dear X."]),
               D([("Leah", "This email says 'cheers' to a client.", "", "problem"),
                  ("Max", "Change it to 'yours sincerely' and drop the slang.", "", "fix"),
                  ("Leah", "And 'can you' becomes a request.", "", "register"),
                  ("Max", "Tone first, then send.", "", "close")])),
        lesson(4, "Opinions and debate",
               "Agree, disagree and concede without shutting the other person down.",
               [V("point", "", "argument item"), V("evidence", "", "support for a claim"),
                V("on the other hand", "", "contrast"), V("fair enough", "", "I accept that"),
                V("overstate", "", "say too much", "verb"), V("nuance", "", "small important difference"),
                V("persuade", "", "change someone's mind", "verb"), V("compromise", "", "middle position")],
               G("concession then contrast", "Name the other view before you disagree.",
                 "While X is true, Y…",
                 [("While the cost is real, the evidence is thin.", "", "concede+contrast"),
                  ("I see your point. On the other hand…", "", "soft disagree"),
                  ("Fair enough — let's look for a compromise.", "", "close")],
                 ["Don't start with 'You're wrong'.", "Don't overstate a small sample as proof."]),
               D([("Nia", "I don't think the plan will work.", "", "view"),
                  ("Owen", "I see your point. The evidence is mixed.", "", "concede"),
                  ("Nia", "On the other hand, waiting costs more.", "", "contrast"),
                  ("Owen", "Fair enough. Let's find a compromise.", "", "close")])),
        lesson(5, "Culture and society",
               "Describe a custom and the assumption underneath it.",
               [V("custom", "", "usual social practice"), V("assumption", "", "unspoken belief"),
                V("taboo", "", "what you must not do"), V("host", "", "person who invites"),
                V("guest", "", "person invited"), V("polite", "", "socially careful", "adj"),
                V("direct", "", "saying it straight", "adj"), V("offend", "", "hurt someone socially", "verb")],
               G("used to vs be used to", "Used to + verb is a past habit. Be used to + -ing is familiarity.",
                 "used to + verb   /   be used to + -ing",
                 [("We used to remove shoes at the door.", "", "past habit"),
                  ("I'm used to eating late.", "", "familiar now"),
                  ("She isn't used to such direct questions.", "", "not familiar")],
                 ["Don't say 'I am used to go'.", "Don't mix the two frames."]),
               D([("Hana", "Is it polite to refuse a second plate?", "", "custom"),
                  ("Ivo", "In my family, refusing twice is fine. Don't offend the host.", "", "rule"),
                  ("Hana", "I'm not used to that.", "", "familiarity"),
                  ("Ivo", "Watch the other guests.", "", "strategy")])),
        lesson(6, "Health and wellbeing",
               "Describe symptoms precisely and ask for advice without drama.",
               [V("symptom", "", "sign of illness"), V("appointment", "", "booked visit"),
                V("prescription", "", "doctor's order for medicine"), V("rest", "", "not work", "verb"),
                V("anxious", "", "worried", "adj"), V("recover", "", "get well", "verb"),
                V("side effect", "", "unwanted extra effect"), V("refer", "", "send to a specialist", "verb")],
               G("should / ought to / had better", "Advice with different force.",
                 "You should… / You'd better… (stronger)",
                 [("You should rest until you recover.", "", "advice"),
                  ("You'd better book an appointment today.", "", "stronger"),
                 ("This medicine ought to help, but watch side effects.", "", "expectation")],
                 ["Had better is a warning, not a casual idea.", "Don't self-prescribe from a headline."]),
               D([("GP", "How long have you had this symptom?", "", "ask"),
                  ("Pat", "Three days. I'm anxious about work.", "", "report"),
                  ("GP", "You'd better rest. I'll write a prescription.", "", "advice"),
                  ("Pat", "If it continues, will you refer me?", "", "next")])),
        lesson(7, "Technology and change",
               "Talk about tools you rely on and what they replaced.",
               [V("update", "", "new version"), V("password", "", "secret login word"),
                V("backup", "", "copy for safety"), V("replace", "", "take the place of", "verb"),
                V("reliable", "", "you can trust it", "adj"), V("outage", "", "service down"),
                V("privacy", "", "control of personal data"), V("habit", "", "usual click path")],
               G("present perfect for change up to now", "Have/has + past participle links past change to now.",
                 "has/have + past participle",
                 [("This app has replaced our paper lists.", "", "change to now"),
                  ("We haven't had an outage this month.", "", "up to now"),
                  ("Have you backed up the files?", "", "question")],
                 ["Don't use a finished past time with present perfect.", "Don't say 'I have replaced it yesterday'."]),
               D([("Kim", "The update has replaced the old menu.", "", "change"),
                  ("Raj", "Have you set a new password?", "", "security"),
                  ("Kim", "Yes. And a backup, after last week's outage.", "", "lesson"),
                  ("Raj", "Good. Privacy settings next.", "", "next")])),
        lesson(8, "Narrative and storytelling",
               "Tell a short past story with a clear time line and a point.",
               [V("meanwhile", "", "at the same time"), V("eventually", "", "after a long time"),
                V("turn out", "", "be discovered to be", "verb"), V("unexpected", "", "not predicted", "adj"),
                V("detail", "", "small fact"), V("flashback", "", "jump to an earlier time"),
                V("ending", "", "how the story closes"), V("narrator", "", "who tells it")],
               G("past simple vs past continuous", "Continuous sets the scene; simple moves the event.",
                 "was/were + -ing   when   past simple",
                 [("I was waiting when the call came.", "", "scene + event"),
                  ("Meanwhile, she was checking the map.", "", "parallel"),
                  ("It turned out we had the wrong street.", "", "later discovery")],
                 ["Don't use past continuous for a short completed action.", "Don't pile flashbacks without time marks."]),
               D([("Sia", "So I was waiting outside when it started to rain.", "", "scene"),
                  ("Jon", "Meanwhile I was on the wrong bus.", "", "parallel"),
                  ("Sia", "Eventually you turned up. Unexpected, but fine.", "", "ending"),
                  ("Jon", "Next time I'll check the detail on the ticket.", "", "point")])),
    ]


_add("en", "A3", _a3_en())
_add("en", "B3", _b3_en())


# Remaining language packs are built from compact rows: (theme_i, vocab, grammar, dialogue)
# Grammar/dialogue/vocab must be in the target language.

def _pack_a3(code, rows):
    """rows: list of 8 lesson dicts already built."""
    _add(code, "A3", rows)


def _pack_b3(code, rows):
    _add(code, "B3", rows)


def load_all_packs():
    """Import sibling bank modules so PACKS is complete. Safe to call twice."""
    from tools.lib import extended_banks_core
    from tools.lib import extended_banks_world
    from tools.lib import extended_banks_rest
    from tools.lib import extended_banks_batch2
    from tools.lib import extended_banks_batch3
    from tools.lib import extended_banks_batch4
    from tools.lib import extended_banks_batch5
    from tools.lib import extended_banks_batch6
    extended_banks_core.register()
    extended_banks_world.register()
    extended_banks_rest.register()
    extended_banks_batch2.register()
    extended_banks_batch3.register()
    extended_banks_batch4.register()
    extended_banks_batch5.register()
    extended_banks_batch6.register()
    return PACKS

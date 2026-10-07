#!/usr/bin/env python3
"""Put the dialogue role labels of a shipped course into its own language.

`dialogue[].sp` is rendered beside the line, and the factory that generated the
five Indian-language courses left those roles in English — a Marathi page shows

    Doctor
    तुम्हाला काय झालं?

while the same course labels other roles natively and writes every other visible
word in Marathi. The role words also leak into the generated practice prompt
(“Complete Patient’s turn: …”), so both the field and the prompt are covered.

The map is per language on purpose. These are roles, not names: a Marathi course
says रुग्ण where the template said `Patient`, and nothing else is translated —
the English gloss of a line (“Doctor, fever for two days.”) is the meaning of a
sentence the learner is asked to produce, and it stays English.
`--check` is read-only.

    python3 tools/localise-speaker-labels.py --lang mr [--check]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Role label per language. Everyday nouns, not honorific titles: the label says
# who is speaking, and it must read like the rest of the course's dialogues.
LABELS: dict[str, dict[str, str]] = {
    "ur": {
        "Brother": "بھائی",
        "Doctor": "ڈاکٹر",
        "Granddaughter": "پوتی/نواسی",
        "Grandmother": "دادی/نانی",
        "Guest": "مہمان",
        "Guide": "رہنما",
        "Host": "میزبان",
        "Learner": "سیکھنے والا",
        "Manager": "منتظم",
        "Newcomer": "نووارد",
        "Patient": "مریض",
        "Shopkeeper": "دکاندار",
        "Sister": "بہن",
        "Speaker A": "مقرر الف",
        "Speaker B": "مقرر ب",
        "Student": "طالب علم",
        "Teacher": "استاد",
        "Waiter": "ویٹر",
        "You": "آپ",
    },
    "mr": {
        "Doctor": "डॉक्टर",
        "Patient": "रुग्ण",
        "Manager": "व्यवस्थापक",
        "Newcomer": "नवागंतुक",
        "Student": "विद्यार्थी",
        "Teacher": "शिक्षक",
        "Brother": "भाऊ",
        "Sister": "बहीण",
        "Granddaughter": "नात",
        "Grandmother": "आजी",
        "Mother": "आई",
        "Neighbour": "शेजारी",
        "Editor": "संपादक",
        "Mediator": "मध्यस्थ",
        "Reviewer": "समीक्षक",
        "Specialist": "तज्ज्ञ",
    },
    "pa": {
        "Editor": "ਸੰਪਾਦਕ",
        "Mediator": "ਵਿਚੋਲਾ",
        "Reviewer": "ਸਮੀਖਿਆਕਾਰ",
        "Specialist": "ਮਾਹਿਰ",
    },
    "ta": {
        "Doctor": "மருத்துவர்",
        "Patient": "நோயாளி",
        "Manager": "மேலாளர்",
        "Newcomer": "புதியவர்",
        "Mother": "அம்மா",
        "Father": "அப்பா",
        "Grandmother": "பாட்டி",
        "Son": "மகன்",
        "Girl": "சிறுமி",
        "Local": "உள்ளூர்வாசி",
        "Vendor": "விற்பனையாளர்",
        "You": "நீங்கள்",
        "Speaker A": "பேச்சாளர் 1",
        "Speaker B": "பேச்சாளர் 2",
    },
    "te": {
        "Doctor": "వైద్యుడు",
        "Patient": "రోగి",
        "Manager": "నిర్వాహకుడు",
        "Newcomer": "కొత్తగా వచ్చిన వ్యక్తి",
        "Father": "నాన్న",
        "Mother": "అమ్మ",
        "Grandmother": "అమ్మమ్మ",
        "Son": "కొడుకు",
        "Girl": "అమ్మాయి",
        "Editor": "సంపాదకుడు",
        "Mediator": "మధ్యవర్తి",
        "Reviewer": "సమీక్షకుడు",
        "Specialist": "నిపుణుడు",
    },
    "gu": {
        "Doctor": "ડૉક્ટર",
        "Patient": "દર્દી",
        "Manager": "વ્યવસ્થાપક",
        "Newcomer": "નવાગંતુક",
        "Student": "વિદ્યાર્થી",
        "Teacher": "શિક્ષક",
        "Brother": "ભાઈ",
        "Sister": "બહેન",
        "Granddaughter": "પૌત્રી",
        "Grandmother": "દાદી",
        "Mother": "માતા",
        "Neighbour": "પડોશી",
        "Editor": "સંપાદક",
        "Mediator": "મધ્યસ્થ",
        "Reviewer": "સમીક્ષક",
        "Specialist": "નિષ્ણાત",
        "Analyst": "વિશ્લેષક",
        "Writer": "લેખક",
        "Author": "લેખક",
        "Chair": "અધ્યક્ષ",
        "Colleague": "સહકર્મી",
        "Reporter": "સંવાદદાતા",
        "Officer": "અધિકારી",
        "Client": "ગ્રાહક",
        "Director": "નિયામક",
        "Presenter": "પ્રસ્તુતકર્તા",
        "Researcher": "સંશોધક",
        "Supervisor": "નિરીક્ષક",
        "Community representative": "સમુદાય પ્રતિનિધિ",
    },
}


def turn_pattern(table: dict[str, str]) -> re.Pattern[str]:
    """The possessive form: the one place a role word references a speaker."""
    roles = "|".join(sorted(table, key=len, reverse=True))
    return re.compile(r"\b(%s)([’']s turn)" % roles)


def collides(text: str, table: dict[str, str]) -> list[str]:
    """Lessons the map would merge: two speakers must never become one word.

    Writer and Author are both લેખક in Gujarati, which is right in a sentence and
    wrong in a dialogue where they are two different people.
    """
    bad: list[str] = []
    try:
        doc = json.loads(text)
    except json.JSONDecodeError:
        return ["unparsable"]
    for unit in (doc.get("level") or {}).get("units", []):
        for lesson in unit.get("lessons", []):
            speakers = [t.get("sp") for t in (lesson.get("dialogue") or [])]
            mapped = [table.get(s, s) for s in speakers]
            if len(set(mapped)) != len(set(speakers)):
                bad.append(lesson.get("id", "?"))
    return bad


def localise(text: str, table: dict[str, str]) -> tuple[str, int, int]:
    """Return the text with roles localised, plus (field, prompt) counts."""
    counts = {"fields": 0, "prompts": 0}

    def field(match: re.Match[str]) -> str:
        counts["fields"] += 1
        return '"sp": "%s"' % table[match.group(1)]

    def prompt(match: re.Match[str]) -> str:
        counts["prompts"] += 1
        return "%s%s" % (table[match.group(1)], match.group(2))

    text = re.sub(r'"sp": "([^"]+)"', lambda m: field(m) if m.group(1) in table else m.group(0), text)
    text = turn_pattern(table).sub(prompt, text)
    return text, counts["fields"], counts["prompts"]


def main() -> int:
    check = "--check" in sys.argv
    lang = None
    for i, arg in enumerate(sys.argv):
        if arg == "--lang" and i + 1 < len(sys.argv):
            lang = sys.argv[i + 1]
    if lang not in LABELS:
        print("usage: tools/localise-speaker-labels.py --lang %s [--check]" % "|".join(sorted(LABELS)))
        return 2
    table = LABELS[lang]

    files = sorted(ROOT.glob(f"data/courses/*/{lang}_*.json"))
    if not files:
        print("cannot locate the course files for %r" % lang)
        return 2

    changed = fields = prompts = 0
    merged: list[str] = []
    for path in files:
        old = path.read_text(encoding="utf-8")
        bad = collides(old, table)
        if bad:
            merged.append("%s (%s)" % (path.name, ", ".join(bad)))
            continue
        new, f, p = localise(old, table)
        if new == old:
            continue
        changed, fields, prompts = changed + 1, fields + f, prompts + p
        if not check:
            path.write_text(new, encoding="utf-8")

    if merged:
        print("SKIPPED, the map would merge two speakers in one dialogue:")
        for row in merged:
            print("  " + row)
        return 1
    if check:
        if fields or prompts:
            print("STALE speaker labels: %d role(s) and %d prompt(s) in %d file(s)"
                  % (fields, prompts, changed))
            return 1
        print("ok    no English role label in the %s dialogues" % lang)
        return 0
    print("speaker labels: %d role label(s) and %d practice prompt(s) localised in %d file(s) of %s"
          % (fields, prompts, changed, lang))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

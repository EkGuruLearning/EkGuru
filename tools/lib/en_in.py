"""Indian English (en-IN) word map for EkGuru's English copy.

Why this exists
---------------
EkGuru's English pages are written in Indian English, which follows British
spelling: colour, practise (the verb), neighbour, -ise endings, catalogue,
towards. A handful of American forms had crept in through generated lesson
data and one footer label (about 2,550 pages carried "Monetization
disclosure"). This module is the single list of those forms, so that

  * tools/indian-english.py can fix the sources that feed the pages, and
  * the same list can fail the build if one comes back.

What is deliberately NOT in the list
------------------------------------
Only forms that are wrong in Indian English and cannot be a correct word in a
language the site teaches. So:

  * "color", "center", "honor", "favorite", "analize", "presize" are not
    here. Spanish, French and Portuguese use some of them, and "color" and
    "center" are also CSS values in code. Those are handled by hand.
  * "organization" is not here. It is the schema.org type name in JSON-LD.
  * "Belize" and "size" are not matched: every pattern is an explicit word,
    never a loose "-ize" rule.
  * Words that are fine in Indian English are left alone: sweater, eraser,
    vacation, movie, online, check, learned.

Pure standard library. No side effects on import.
"""
from __future__ import annotations

import re

# US form -> Indian English form. Lower case; the case of the original is kept.
LEXICON = {
    # -ize / -ization / -yze  ->  -ise / -isation / -yse
    "monetization": "monetisation",
    "summarize": "summarise", "summarizes": "summarises",
    "summarized": "summarised", "summarizing": "summarising",
    "summarization": "summarisation",
    "synthesize": "synthesise", "synthesizes": "synthesises",
    "synthesized": "synthesised", "synthesizing": "synthesising",
    "nasalize": "nasalise", "nasalizes": "nasalises",
    "nasalized": "nasalised", "nasalization": "nasalisation",
    "normalize": "normalise", "normalizes": "normalises",
    "normalized": "normalised", "normalization": "normalisation",
    "capitalize": "capitalise", "capitalizes": "capitalises",
    "capitalized": "capitalised", "capitalization": "capitalisation",
    "memorize": "memorise", "memorizes": "memorises",
    "memorized": "memorised", "memorizing": "memorising",
    "criticize": "criticise", "criticizes": "criticises",
    "criticized": "criticised", "criticizing": "criticising",
    "emphasize": "emphasise", "emphasizes": "emphasises",
    "emphasized": "emphasised", "emphasizing": "emphasising",
    "formalize": "formalise", "formalization": "formalisation",
    "naturalized": "naturalised",
    "generalized": "generalised", "generalization": "generalisation",
    "overgeneralization": "overgeneralisation",
    "neutralize": "neutralise",
    "nominalized": "nominalised", "nominalizations": "nominalisations",
    "prioritize": "prioritise", "prioritized": "prioritised",
    "authorized": "authorised", "authorization": "authorisation",
    "romanization": "romanisation", "romanized": "romanised",
    "realize": "realise", "realizes": "realises", "realized": "realised",
    "realizing": "realising", "realization": "realisation",
    "realizations": "realisations",
    "recognize": "recognise", "recognizes": "recognises",
    "recognized": "recognised", "recognizing": "recognising",
    "recognizable": "recognisable",
    "personalize": "personalise", "personalizes": "personalises",
    "personalized": "personalised", "personalizing": "personalising",
    "personalization": "personalisation",
    "customize": "customise", "customizes": "customises",
    "customized": "customised", "customizing": "customising",
    "analyze": "analyse", "analyzes": "analyses",
    "analyzed": "analysed", "analyzing": "analysing",
    "minimize": "minimise", "maximize": "maximise",
    "specialize": "specialise", "specialized": "specialised",
    "apologize": "apologise", "apologized": "apologised",
    # -or -> -our
    "colorful": "colourful", "colors": "colours", "colored": "coloured",
    "honored": "honoured", "honoring": "honouring",
    "behavior": "behaviour", "behaviors": "behaviours",
    "neighbor": "neighbour", "neighbors": "neighbours",
    "flavor": "flavour", "flavors": "flavours",
    "humor": "humour",
    # -l- doubling
    "labeled": "labelled", "labeling": "labelling",
    "traveling": "travelling", "traveled": "travelled", "traveler": "traveller",
    "canceled": "cancelled", "canceling": "cancelling",
    "modeling": "modelling", "modeled": "modelled",
    # verbs and nouns
    "practicing": "practising", "practiced": "practised",
    "enrollment": "enrolment", "enrollments": "enrolments",
    "fulfillment": "fulfilment", "skillful": "skilful",
    "catalog": "catalogue", "catalogs": "catalogues",
    "jewelry": "jewellery", "defense": "defence", "offense": "offence",
    # directions
    "toward": "towards", "afterward": "afterwards",
}

# Longest first so "recognizable" wins over "recognize".
_ALTERNATION = "|".join(sorted((re.escape(k) for k in LEXICON), key=len, reverse=True))
WORD_RE = re.compile(r"(?<![A-Za-z0-9_])(" + _ALTERNATION + r")(?![A-Za-z0-9_])", re.IGNORECASE)


def _match_case(original: str, replacement: str) -> str:
    if original.isupper() and len(original) > 1:
        return replacement.upper()
    if original[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def _sub(match: "re.Match[str]") -> str:
    original = match.group(1)
    return _match_case(original, LEXICON[original.lower()])


def convert(text: str) -> str:
    """Return text with every US form in the lexicon turned into Indian English."""
    return WORD_RE.sub(_sub, text)


def find(text: str) -> list[str]:
    """Return the US forms found in text, lower-cased, in order, with repeats."""
    return [m.group(1).lower() for m in WORD_RE.finditer(text)]


# A JSON string token, and what may follow it when it is a KEY rather than a value.
_JSON_STRING = re.compile(r'"(?:[^"\\\n]|\\.)*"')
_KEY_TAIL = re.compile(r"\s*:")
_URL = re.compile(r"https?://[^\s\"\\]+")


def _convert_prose(token: str) -> tuple[str, int]:
    """Convert a string but leave any URL inside it exactly as written."""
    out: list[str] = []
    n = 0
    last = 0
    for m in _URL.finditer(token):
        part, k = WORD_RE.subn(_sub, token[last:m.start()])
        out.append(part)
        out.append(m.group(0))
        n += k
        last = m.end()
    part, k = WORD_RE.subn(_sub, token[last:])
    out.append(part)
    return "".join(out), n + k


def convert_json_text(raw: str) -> tuple[str, int]:
    """Convert only the prose string VALUES of a JSON document.

    Everything else is left byte-for-byte:
      * keys, so a schema field called "normalization" survives;
      * values with no space in them (identifiers, slugs, file names, enum
        values such as "colors"), which code looks up by exact text;
      * any URL inside a value.
    Returns (new_text, number_of_replacements).
    """
    count = 0
    out: list[str] = []
    last = 0
    for m in _JSON_STRING.finditer(raw):
        token = m.group(0)
        if _KEY_TAIL.match(raw, m.end()):
            continue  # a key
        body = token[1:-1]
        if not re.fullmatch(r"[A-Za-z]+", body) and " " not in body:
            continue  # a slug, file name or code identifier, not English prose
        new, k = _convert_prose(token)
        if k:
            count += k
            out.append(raw[last:m.start()])
            out.append(new)
            last = m.end()
    out.append(raw[last:])
    return "".join(out), count

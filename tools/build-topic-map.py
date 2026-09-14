#!/usr/bin/env python3
"""EkGuru — CHAPTER THEME MAP (v147).

    python3 tools/build-topic-map.py

Every Hindi page belongs to a chapter (grammar, numbers, travel...),
a level, a section (ask, practice...) or a language course. This tool
writes tools/topic-meta.json:

  topics: {key: {kind, en, hi, mascot, floats, accent, tint}}
  pages:  {target-path: topic-key}   (target = path minus /index.html)

The page->chapter links come from build-hindi-structure.py's own
dicts (LESSONS, HINDI_TOPICS, ...), so a page can only be claimed by
the topic its builder assigned. tools/inject-storybook.py then bakes
a chapter banner + palette into each claimed page; unclaimed pages
keep the default storybook look (never a guessed theme).

Run this before the injector whenever the structure dicts change.
"""
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# kind, English, Hindi, mascot, floats, accent, tint. Hindi labels are
# plain dictionary words used as UI copy (like "इस पेज पर").
THEMES = {
    "basics": ("Chapter", "Basics", "बुनियाद", "🌱", "अ आ इ", "#16a34a", "#eefbf1"),
    "conversation": ("Chapter", "Conversation", "बातचीत", "💬", "न म त", "#0284c7", "#eef7ff"),
    "pronunciation": ("Chapter", "Pronunciation", "उच्चारण", "🔊", "श ष स", "#7c3aed", "#f3efff"),
    "grammar": ("Chapter", "Grammar", "व्याकरण", "📏", "ए ऐ ओ", "#c026d3", "#fdf0fd"),
    "vocabulary": ("Chapter", "Vocabulary", "शब्दावली", "📚", "ज्ञ त्र श्र", "#b45309", "#fdf6ec"),
    "travel": ("Chapter", "Travel", "यात्रा", "✈️", "च ल ग", "#0d9488", "#ecfdfb"),
    "daily-life": ("Chapter", "Daily life", "रोज़मर्रा", "🏠", "घ र अ", "#ea580c", "#fff4ec"),
    "numbers": ("Chapter", "Numbers", "संख्याएँ", "🔢", "१ २ ३", "#dc2626", "#fdeeee"),
    "time-dates": ("Chapter", "Time & dates", "समय", "⏰", "स म य", "#4f32d9", "#f1edfe"),
    "food": ("Chapter", "Food", "खाना", "🍛", "स व द", "#65a30d", "#f3ffe9"),
    "shopping": ("Chapter", "Shopping", "खरीदारी", "🛍️", "म ल य", "#db2777", "#fdeef6"),
    "level-beginner": ("Level", "Beginner", "शुरुआती", "🌱", "अ आ इ", "#65a30d", "#f3ffe9"),
    "level-elementary": ("Level", "Elementary", "प्रारंभिक", "🌿", "क ख ग", "#0d9488", "#ecfdfb"),
    "level-intermediate": ("Level", "Intermediate", "मध्यम", "🌳", "ट ठ ड", "#7c3aed", "#f3efff"),
    "level-advanced": ("Level", "Advanced", "उन्नत", "🚀", "क्ष ज्ञ श्र", "#c2410c", "#fff1e8"),
    "section-ask": ("Question", "Question", "सवाल", "❓", "क्यों", "#b45309", "#fdf6ec"),
    "section-answers": ("Answer", "Answer", "जवाब", "✅", "सही", "#147a3d", "#edfaf1"),
    "section-daily": ("Daily", "Daily Hindi", "रोज़ का हिंदी", "📅", "रोज़", "#ea580c", "#fff4ec"),
    "section-toolbox": ("Tool", "Tool", "औज़ार", "🧰", "काम", "#6d28d9", "#f3efff"),
    "section-materials": ("Material", "Material", "सामग्री", "🖨️", "पढ़ो", "#0e7490", "#ecfbff"),
    "section-paths": ("Path", "Learning path", "सीखने का रास्ता", "🗺️", "रास्ता", "#0d9488", "#ecfdfb"),
    "section-practice": ("Practice", "Practice", "अभ्यास", "✏️", "अभ्यास", "#7c3aed", "#f3efff"),
    "section-progress": ("Progress", "My progress", "मेरी प्रगति", "📈", "आगे", "#4f32d9", "#f1edfe"),
    "section-review": ("Review", "Review", "दोहराव", "🔁", "फिर", "#0284c7", "#eef7ff"),
    "lang-bengali": ("Language", "Bengali", "बांग्ला", "🗣️", "অ আ ই", "#0f766e", "#ecfdfb"),
    "lang-gujarati": ("Language", "Gujarati", "गुजराती", "🗣️", "અ આ ઇ", "#0f766e", "#ecfdfb"),
    "lang-kannada": ("Language", "Kannada", "कन्नड़", "🗣️", "ಅ ಆ ಇ", "#0f766e", "#ecfdfb"),
    "lang-malayalam": ("Language", "Malayalam", "मलयालम", "🗣️", "അ ആ ഇ", "#0f766e", "#ecfdfb"),
    "lang-marathi": ("Language", "Marathi", "मराठी", "🗣️", "अ आ इ", "#0f766e", "#ecfdfb"),
    "lang-punjabi": ("Language", "Punjabi", "पंजाबी", "🗣️", "ਅ ਆ ਇ", "#0f766e", "#ecfdfb"),
    "lang-tamil": ("Language", "Tamil", "तमिल", "🗣️", "அ ஆ இ", "#0f766e", "#ecfdfb"),
    "lang-telugu": ("Language", "Telugu", "तेलुगू", "🗣️", "అ ఆ ఇ", "#0f766e", "#ecfdfb"),
    "lang-urdu": ("Language", "Urdu", "उर्दू", "🗣️", "ا ب پ", "#0f766e", "#ecfdfb"),
}

CHAPTERS = ["basics", "conversation", "pronunciation", "grammar", "vocabulary",
            "travel", "daily-life", "numbers", "time-dates", "food", "shopping"]
LEVELS = ["beginner", "elementary", "intermediate", "advanced"]


def main():
    spec = importlib.util.spec_from_file_location(
        "struct", os.path.join(ROOT, "tools", "build-hindi-structure.py"))
    st = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(st)

    pages = {}
    for slug, tp in st.LESSONS.items():
        pages["learn/" + slug] = tp
    for slug, tp in st.HINDI_TOPICS.items():
        pages["hindi/" + slug] = tp
    for target, tp in list(st.MATERIALS.items()) + list(st.TOOLS.items()) + \
            list(st.PRACTICE.items()) + list(st.PATHS.items()) + \
            list(st.ANSWERS.items()) + list(st.ASK.items()):
        pages[target] = tp
    # Each chapter page is its own chapter.
    for tp in CHAPTERS:
        pages["learn/hindi/" + tp] = tp
    for lv in LEVELS:
        pages["learn/hindi/" + lv] = "level-" + lv

    meta = {"topics": {}, "pages": pages}
    for key, (kind, en, hi, mascot, floats, accent, tint) in THEMES.items():
        meta["topics"][key] = {"kind": kind, "en": en, "hi": hi,
                               "mascot": mascot, "floats": floats,
                               "accent": accent, "tint": tint}
    with open("tools/topic-meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print("topic-meta.json: %d themes, %d mapped pages"
          % (len(meta["topics"]), len(pages)))


if __name__ == "__main__":
    main()

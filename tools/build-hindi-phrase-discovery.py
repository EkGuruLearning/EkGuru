#!/usr/bin/env python3
"""Connect existing phrase answers to their existing hubs; never publish new URLs.
--check is read-only. Titles come from actual target pages, not invented translations.
"""
import html
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from lib.ultra_content import Page

START = '<!-- ekguru:phrase-discovery:start -->'
END = '<!-- ekguru:phrase-discovery:end -->'
GROUPS = {
    'Greetings and introductions': ['good-afternoon', 'good-evening', 'good-night', 'nice-to-meet-you', 'welcome', 'what-is-your-name', 'my-name-is', 'where-are-you-from', 'where-do-you-live', 'what-do-you-do', 'how-old-are-you'],
    'Politeness and language help': ['excuse-me', 'no-problem', 'i-am-sorry', 'do-you-speak-english', 'i-dont-speak-hindi', 'i-am-learning-hindi', 'i-dont-know'],
    'Finding things, shopping and asking for help': ['i-need-help', 'how-much', 'where-is', 'what-time-is-it', 'i-am-lost', 'what-is-this', 'where-is-the-bathroom'],
    'Feelings and everyday updates': ['i-am-tired', 'i-like-it', 'i-am-fine', 'i-am-happy', 'i-am-sad', 'i-am-busy', 'i-am-here'],
    'Good wishes and saying goodbye': ['happy-birthday', 'good-luck', 'take-care', 'congratulations', 'see-you-tomorrow', 'see-you-later', 'happy-new-year'],
}


def targets():
    groups, seen = {}, set()
    for label, keys in GROUPS.items():
        rows = []
        for key in keys:
            slug = 'how-to-say-' + key + '-in-hindi'
            if slug in seen:
                raise ValueError('Duplicate phrase: ' + slug)
            seen.add(slug)
            relative = 'ask/' + slug + '/index.html'
            path = ROOT / relative
            if not path.is_file():
                raise ValueError('Missing existing phrase: ' + relative)
            page = Page(path.read_text())
            url = 'https://ekguru.shop/ask/' + slug + '/'
            if page.noindex or page.canonical != url or len(page.h1) != 1 or not page.h1[0].strip():
                raise ValueError('Target must already be a self-canonical indexable answer: ' + relative)
            rows.append(dict(slug=slug, question=page.h1[0].strip()))
        groups[label] = rows
    return groups


def section(relative, groups):
    if relative == 'ask/index.html':
        out = [START, '<section id="hindi-phrase-answers" aria-labelledby="phrase-directory-heading">',
               '<h2 id="phrase-directory-heading">Find a Hindi phrase by situation</h2>',
               '<p>Choose the situation you need, then open the full answer for Hindi script, pronunciation guidance and usage. These links organise existing explanations; they are not a new set of translations or a native-review approval. Pay attention to the formality and context described on each page.</p>']
        for label, rows in groups.items():
            out.append('<h3>' + html.escape(label) + '</h3><ul class="qlist">')
            out.extend('<li><a href="' + row['slug'] + '/">' + html.escape(row['question']) + '</a></li>' for row in rows)
            out.append('</ul>')
        out += ['<p>For a connected learning path, return to <a href="../learn/hindi/conversation/">Hindi conversation</a>, try the <a href="../learn/hindi/practice/conversation/">conversation practice tool</a>, or open <a href="../learn/hindi/">all Hindi lessons</a>.</p>', '</section>', END]
    elif relative == 'learn/hindi/conversation/index.html':
        out = [START, '<section aria-labelledby="phrase-course-heading"><h2 id="phrase-course-heading">Find the words for a real situation</h2>',
               '<p>Need one expression rather than a whole lesson? Browse the <a href="../../../ask/#hindi-phrase-answers">Hindi phrase answers by situation</a>: introductions, politeness, practical questions, feelings and good wishes. Each answer explains its own wording and context.</p>',
               '<ul class="linklist"><li><a href="../../../ask/how-to-say-i-need-help-in-hindi/">Ask for help in Hindi</a></li><li><a href="../../../ask/how-to-say-how-much-in-hindi/">Ask how much something costs</a></li><li><a href="../../../ask/how-to-say-where-is-the-bathroom-in-hindi/">Ask where the bathroom is</a></li></ul>',
               '<p>Read the full explanation before using a phrase. Then choose a reply in the <a href="../practice/conversation/">existing conversation practice tool</a>. The tool is rule-based practice, not an assessment of real conversation.</p></section>', END]
    else:
        raise ValueError('Unsupported hub')
    return '\n'.join(out)


def transformed(raw, relative, groups=None):
    block = section(relative, groups if groups is not None else targets())
    if START in raw:
        return re.sub(re.escape(START) + r'[\s\S]*?' + re.escape(END), lambda _: block, raw, count=1)
    anchor = '<ul class="qlist">' if relative == 'ask/index.html' else '<h2>Guides</h2>'
    if anchor not in raw:
        raise ValueError('Missing hub integration anchor: ' + relative)
    return raw.replace(anchor, block + '\n' + anchor, 1)


def main():
    groups = targets(); stale = []
    for relative in ['ask/index.html', 'learn/hindi/conversation/index.html']:
        path = ROOT / relative; old = path.read_text(); new = transformed(old, relative, groups)
        if new != old:
            stale.append(relative)
            if '--check' not in sys.argv:
                path.write_text(new)
    print(f'Phrase discovery: {sum(map(len, groups.values()))} existing answers, {len(groups)} situation groups, {len(stale)} ' + ('stale' if '--check' in sys.argv else 'updated'))
    return int('--check' in sys.argv and bool(stale))


if __name__ == '__main__':
    raise SystemExit(main())

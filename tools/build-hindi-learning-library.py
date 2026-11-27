#!/usr/bin/env python3
"""Build a deduplicated, source-linked Hindi learning collection on the existing practice hub.
No new URLs, indexing changes, completion scores or voice recordings. --check is read-only.
"""
import collections
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ['Foundation', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2']
DATA = ROOT / 'js/hindi-learning-library-data.js'
HUB = ROOT / 'learn/hindi/practice/index.html'
START = '<!-- ekguru:hindi-library:start -->'
END = '<!-- ekguru:hindi-library:end -->'


def normalized(text):
    # Keep vowel marks/nukta: removing combining marks would merge distinct Hindi words.
    return re.sub(r'[\s।.!?,;:“”"\-—…]+', '', unicodedata.normalize('NFC', text)).casefold()


def build():
    items, seen = [], set()
    def add(level, kind, hi, roman, en, title, source, **extra):
        hi, roman, en = (str(x).strip() for x in (hi, roman, en))
        key = normalized(hi)
        if not key or key in seen:
            return
        if not all((hi, roman, en)) or not re.search('[\u0900-\u097f]', hi):
            raise ValueError('Missing Hindi/reading/meaning: ' + title)
        if len(hi) > 1900:
            raise ValueError('Voice chunk too long: ' + title)
        seen.add(key)
        items.append(dict(id='hl-' + hashlib.sha256(key.encode()).hexdigest()[:16], level=level,
                          kind=kind, hi=hi, roman=roman, en=en, title=title, source=source, **extra))
    spec = importlib.util.spec_from_file_location('foundation', ROOT / 'tools/hindi-foundation-content.py')
    foundation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foundation)
    # Keep the primer's exact sign progression, not alphabetical word order.
    for lesson in foundation.LESSONS:
        source = '/learn/hindi/foundation/' + lesson['slug'] + '/'
        title = lesson['en']
        for letter, roman, hint, word, reading, meaning, _ in lesson.get('letters', []):
            add('Foundation', 'letter', letter, roman, hint, title, source)
            add('Foundation', 'word', word, reading, meaning, title, source)
        for _, group in lesson.get('groups', []):
            for hi, roman, en in group:
                add('Foundation', 'word', hi, roman, en, title, source)
        for hi, roman, en in lesson.get('sentences', []):
            add('Foundation', 'sentence', hi, roman, en, title, source)
    for level in LEVELS[1:]:
        course = json.loads((ROOT / f'data/courses/phase-2/hi_{level}.json').read_text())
        for unit in course['level']['units']:
            for lesson in unit['lessons']:
                source = '/languages/hi/level/' + level.lower() + '/#' + lesson['id'].lower()
                for kind, rows in [('word', lesson['vocab']), ('sentence', lesson['grammar']['examples'])]:
                    for row in rows:
                        add(level, kind, row['t'], row['r'], row['en'], lesson['title'], source)
                # A dialogue is a connected reading with explicit speakers, not an invented paragraph.
                for row in lesson['dialogue']:
                    add(level, 'sentence', row['t'], row['r'], row['en'], lesson['title'], source)
    readings = json.loads((ROOT / 'data/content/hindi-library-readings.json').read_text())['readings']
    for row in readings:
        add(row['level'], 'paragraph', row['hi'], row['roman'], row['en'], row['title'],
            '/learn/hindi/practice/#hindi-learning-library', question=row['question'],
            answer=row['answer'], focus=row['focus'])
    # Stable stage order; paragraph reading ends each stage and the whole course.
    order = {'letter': 0, 'word': 1, 'sentence': 2, 'paragraph': 3}
    items.sort(key=lambda x: (LEVELS.index(x['level']), order[x['kind']]))
    if len(items) < 1000:
        raise ValueError(f'Only {len(items)} distinct items; do not pad the count.')
    return dict(version=1, language='hi', levels=LEVELS,
                counts=dict(collections.Counter(x['kind'] for x in items)),
                review_status='Native-speaker review not recorded; intended practice stages, not a proficiency certification.',
                items=items)


def markup(data):
    count = len(data['items'])
    counts = data['counts']
    fallback = ''.join('<details><summary>' + html.escape(x['level'] + ' · ' + x['title']) + '</summary><p lang="hi">' + html.escape(x['hi']) + '</p><p lang="hi-Latn">' + html.escape(x['roman']) + '</p><p>' + html.escape(x['en']) + '</p><p>' + html.escape(x['question']) + '</p><p>Model answer: ' + html.escape(x['answer']) + '</p></details>' for x in data['items'] if x['kind'] == 'paragraph')
    return START + f'''
<section id="hindi-learning-library" class="hll" aria-label="Hindi from first letters to advanced reading">
  <p class="hll-kicker">Start small · read · listen · build meaning</p>
  <h2>From first letters to advanced reading</h2>
  <p><strong>{count:,} distinct learning items</strong>: {counts.get('letter', 0)} letter/sound models, {counts.get('word', 0)} words and expressions, {counts.get('sentence', 0)} sentence models, and {counts.get('paragraph', 0)} connected paragraph readings. These bring existing Foundation and core course content together with new fictional readings; the same Hindi text is counted once, not once per activity.</p>
  <p>Begin with letters, then words, sentences and paragraphs. A1–C2 are the existing course's practice labels, not proof of fluency. Native-speaker review is not recorded. Romanisation helps at first; try reading the Hindi before opening it.</p>
  <nav class="hll-path" aria-label="Read the source lessons without JavaScript"><a href="../foundation/">0 · First letters</a><a href="/languages/hi/level/a1/">1 · Beginner</a><a href="/languages/hi/level/a2/">2 · Everyday Hindi</a><a href="/languages/hi/level/b1/">3 · Connected ideas</a><a href="/languages/hi/level/b2/">4 · Viewpoints</a><a href="/languages/hi/level/c1/">5 · Nuance</a><a href="/languages/hi/level/c2/">6 · Close reading</a></nav>
  <p class="hll-audio-note">Listen uses a synthetic Hindi voice installed in your browser or operating system, not a native recording. It starts only when you press a button. Availability, pronunciation and offline playback depend on your device. No microphone or speech score.</p>
  <div id="offline-ctl"></div>
  <p id="hll-loading">The interactive collection needs JavaScript and its library scripts. If it cannot open, the source lesson links above still work.</p>
  <noscript><p>Follow the seven source links above for the existing lessons without JavaScript, or read the new connected texts here:</p>{fallback}</noscript>
  <div id="hll-app" hidden>
    <div class="hll-toolbar"><label>Stage <select id="hll-level"><option value="all">All stages, in order</option>''' + ''.join(f'<option value="{x}">{x}</option>' for x in LEVELS) + '''</select></label>
    <label>Activity <select id="hll-kind"><option value="all">All learning items</option><option value="letter">Letters and sounds</option><option value="word">Words and expressions</option><option value="sentence">Sentences</option><option value="paragraph">Paragraph reading room</option></select></label>
    <label>Find a word or meaning <input id="hll-search" type="search" maxlength="100" placeholder="Try किताब or book"></label></div>
    <div class="hll-buttons"><button id="hll-start" type="button">Start from the beginning</button><button id="hll-readings" type="button">Go to paragraph reading</button></div>
    <details><summary>Hindi voice and playback controls</summary><label>Hindi voice <select data-eg-voice-picker="hi"><option>No matching voice on this device</option></select></label><label>Speaking speed <select data-eg-voice-rate><option value="0.6">0.6× · slower</option><option value="0.8">0.8× · learning pace</option><option value="1">1× · normal</option></select></label><button type="button" data-eg-voice-stop disabled>Stop audio</button><button type="button" data-eg-voice-repeat disabled>Repeat last item</button><p data-eg-voice-status role="status"></p></details>
    <p id="hll-position" role="status" aria-live="polite"></p>
    <form id="hll-jump" class="hll-jump" novalidate><label for="hll-number">Item number in this selection <input id="hll-number" type="number" min="1" step="1" inputmode="numeric" aria-describedby="hll-jump-note"></label><button type="submit">Go to item</button><p id="hll-jump-note" role="status">Choose an item number to skip ahead without marking anything complete.</p></form>
    <article id="hll-card" tabindex="-1" aria-label="Current learning item"></article>
    <p id="hll-empty" hidden>No items match. Choose another stage or clear your search.</p>
    <nav class="hll-buttons" aria-label="Move through the collection"><button id="hll-previous" type="button">Previous item</button><button id="hll-next" type="button">Next item</button></nav>
    <p id="hll-session" role="status">Opening or listening does not complete a lesson. No proficiency score is calculated.</p>
  </div>
</section>
''' + END


def transformed(raw, data):
    section = markup(data)
    if START in raw:
        raw = re.sub(re.escape(START) + r'[\s\S]*?' + re.escape(END), lambda _: section, raw, count=1)
    else:
        anchor = '  <ul class="linklist">'
        if anchor not in raw:
            raise ValueError('Practice hub integration anchor missing')
        raw = raw.replace(anchor, section + '\n' + anchor, 1)
    css = '<link rel="stylesheet" href="/css/hindi-learning-library.css">\n'
    if css.strip() not in raw:
        anchor = '<!-- ekguru:ultra-assets:start -->' if '<!-- ekguru:ultra-assets:start -->' in raw else '</head>'
        raw = raw.replace(anchor, css + anchor, 1)
    scripts = '\n'.join('<script src="/js/' + x + '" defer></script>' for x in
                         ['hindi-learning-library-data.js', 'hindi-learning-library.js', 'hindi-offline.js']
                         if '/js/' + x not in raw)
    if scripts:
        raw = raw.replace('</body>', scripts + '\n</body>', 1)
    return raw


def main():
    data = build()
    payload = '/* Generated from existing Hindi sources; tools/build-hindi-learning-library.py. */\nwindow.EKGURU_HINDI_LIBRARY=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c') + ';\n'
    outputs = {DATA: payload, HUB: transformed(HUB.read_text(), data)}
    stale = [p for p, text in outputs.items() if not p.exists() or p.read_text() != text]
    check = '--check' in sys.argv
    if not check:
        for p in stale:
            p.write_text(outputs[p], encoding='utf-8')
    print(f'Hindi collection: {len(data["items"])} distinct items, {data["counts"]}; {len(stale)} ' + ('stale' if check else 'updated'))
    return int(check and bool(stale))


if __name__ == '__main__':
    raise SystemExit(main())

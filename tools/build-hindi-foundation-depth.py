#!/usr/bin/env python3
"""Add authored depth to existing Foundation URLs. No indexability/URL/progress changes.
--check is read-only. Only chapters present in the input are implementation-complete.
"""
import html
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from lib.ultra_content import own

INPUT = ROOT / 'data/content/hindi-foundation-depth.json'
REPORT = ROOT / 'data/quality/hindi-foundation-expansion.json'
START = '<!-- ekguru:foundation-depth:start -->'
END = '<!-- ekguru:foundation-depth:end -->'
BASE = 'https://ekguru.shop/learn/hindi/foundation/'
CSS = '<link rel="stylesheet" href="/css/hindi-foundation-depth.css">'


def prose_words(chapter):
    # Deliberately conservative: only authored English prose, not headings,
    # models, answer controls, navigation, existing copy or repeated exercises.
    return sum(len(re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)*", p))
               for section in chapter['sections'] for p in section['paragraphs'])


def content():
    data = json.loads(INPUT.read_text())
    slugs, paragraphs = set(), set()
    for chapter in data['chapters']:
        slug = chapter['slug']
        if not re.fullmatch('[a-z0-9-]+', slug) or slug in slugs:
            raise ValueError('Invalid/duplicate chapter slug')
        slugs.add(slug)
        if not (ROOT / f'learn/hindi/foundation/{slug}/index.html').is_file():
            raise ValueError('Expansion must target an existing chapter')
        if prose_words(chapter) < chapter['minimum_prose_words'] or chapter['minimum_prose_words'] < 3000:
            raise ValueError('Authored prose below 3000-word target: ' + slug)
        if not 80 <= len(chapter['description']) <= 160:
            raise ValueError('Description length out of bounds: ' + slug)
        ids = set()
        for section in chapter['sections']:
            if not re.fullmatch('[a-z0-9-]+', section['id']) or section['id'] in ids:
                raise ValueError('Invalid/duplicate section ID')
            ids.add(section['id'])
            for p in section['paragraphs']:
                key = re.sub(r'\s+', ' ', p.strip()).casefold()
                if not key or key in paragraphs:
                    raise ValueError('Empty/repeated prose must not inflate depth')
                paragraphs.add(key)
            for hi, roman, en in section.get('models', []):
                if not all((hi, roman, en)) or len(hi) > 1900 or not re.search('[\u0900-\u097f]', hi):
                    raise ValueError('Invalid listening model')
    return data


def render(chapter):
    e = html.escape
    blocks = [START, '<h2 class="hf-depth-heading" id="extended-guide">' + e(chapter['title']) + '</h2>',
              '<div class="hf-depth"><p>Extended guided study: English explanation with Hindi models. Native-speaker review is not recorded. Use the existing Next/Back steps or choose Whole lesson to read continuously; no new completion requirement is added.</p></div>']
    for section in chapter['sections']:
        blocks += ['<h2 class="hf-depth-heading" id="hf-' + section['id'] + '">' + e(section['title']) + '</h2>', '<div class="hf-depth">']
        blocks += ['<p>' + e(p) + '</p>' for p in section['paragraphs']]
        if section.get('models'):
            blocks.append('<ul class="hf-models" aria-label="Hindi reading models">')
            for hi, roman, meaning in section['models']:
                blocks.append('<li><span class="hf-hi" lang="hi">' + e(hi) + '</span> <span lang="hi-Latn">' + e(roman) + '</span> · ' + e(meaning) + ' <button type="button" data-voice-lang="hi" data-voice-text="' + e(hi) + '" aria-label="Listen in Hindi: ' + e(hi) + '">Listen</button></li>')
            blocks.append('</ul>')
        for question, answer in section.get('checks', []):
            blocks.append('<details><summary>' + e(question) + '</summary><p>' + e(answer) + '</p></details>')
        blocks.append('</div>')
    blocks.append('<div class="hf-depth"><p>Continue with <a href="../vyanjan-1/">the first consonant rows</a>, revisit the <a href="../">Foundation chapter map</a>, or use the <a href="../../practice/#hindi-learning-library">letter-to-reading collection</a>. The source lesson completion button remains optional and under your control.</p></div>')
    blocks.append(END)
    return '\n'.join(blocks)


def transformed(raw, chapter):
    section = render(chapter)
    if START in raw:
        raw = re.sub(re.escape(START) + r'[\s\S]*?' + re.escape(END), lambda _: section, raw, count=1)
    else:
        anchor = '<div class="fd-task">'
        if anchor not in raw:
            raise ValueError('Missing chapter insertion anchor')
        raw = raw.replace(anchor, section + '\n' + anchor, 1)
    if CSS not in raw:
        anchor = '<!-- ekguru:ultra-assets:start -->' if '<!-- ekguru:ultra-assets:start -->' in raw else '</head>'
        raw = raw.replace(anchor, CSS + '\n' + anchor, 1)
    # Keep canonical, robots, title, h1 and breadcrumb unchanged. Align only
    # actual descriptions, including the pre-existing lesson structured data.
    description = chapter['description']
    raw = re.sub(r'(<meta (?:name="(?:description|twitter:description)"|property="og:description") content=")[^"]*(")',
                 lambda m: m[1] + html.escape(description, quote=True) + m[2], raw)
    def schema(match):
        data = json.loads(match[2])
        changed = False
        def visit(node):
            nonlocal changed
            if isinstance(node, dict):
                if node.get('@type') == 'LearningResource' and node.get('@id') == BASE + chapter['slug'] + '/#lesson':
                    node['description'] = description; changed = True
                for value in node.values():
                    visit(value)
            elif isinstance(node, list):
                for value in node:
                    visit(value)
        visit(data)
        return match[1] + json.dumps(data, ensure_ascii=False) + match[3] if changed else match[0]
    return re.sub(r'(<script[^>]*type="application/ld\+json"[^>]*>)([\s\S]*?)(</script>)', schema, raw)


def report(data, outputs):
    spec = importlib.util.spec_from_file_location('primer', ROOT / 'tools/hindi-foundation-content.py')
    primer = importlib.util.module_from_spec(spec); spec.loader.exec_module(primer)
    chapters = {c['slug']: c for c in data['chapters']}
    rows = []
    for lesson in primer.LESSONS[:10]:
        slug = lesson['slug']; relative = f'learn/hindi/foundation/{slug}/index.html'
        path = ROOT / relative; raw = outputs.get(path, path.read_text())
        chapter = chapters.get(slug)
        rows.append(dict(chapter=lesson['n'], source_file=relative, url=BASE + slug + '/', title=lesson['en'],
                         target_authored_prose_words=3000,
                         added_authored_prose_words=prose_words(chapter) if chapter else 0,
                         own_text_tokens=sum(any(c.isalpha() for c in word) for word in own(raw).split()),
                         status='expanded-draft-needs-native-review' if chapter else 'pending-expansion',
                         next_focus=chapter['title'] if chapter else 'Topic-specific explanation, worked models, error correction and answer-led practice; no copied filler.'))
    return dict(version=1, scope='First ten existing Foundation chapters; long-term request is 1000+ existing pages, not completed.',
                count_method='Added prose: English lexical words in authored paragraph fields only. Own-text tokens: whitespace-delimited tokens containing a letter after shared chrome exclusion; not a linguistic Hindi word count.',
                expanded_chapters=sum(bool(r['added_authored_prose_words']) for r in rows),
                native_review='Not recorded; no editorial approval or release claimed.', chapters=rows)


def main():
    data = content(); outputs = {}
    for chapter in data['chapters']:
        path = ROOT / f'learn/hindi/foundation/{chapter["slug"]}/index.html'
        outputs[path] = transformed(path.read_text(), chapter)
    outputs[REPORT] = json.dumps(report(data, outputs), ensure_ascii=False, indent=2) + '\n'
    stale = [p for p, text in outputs.items() if not p.exists() or p.read_text() != text]
    check = '--check' in sys.argv
    if not check:
        for path in stale:
            path.write_text(outputs[path])
    print(f'Foundation depth: {len(data["chapters"])} expanded draft(s), 10 planned chapters; {len(stale)} ' + ('stale' if check else 'updated'))
    return int(check and bool(stale))


if __name__ == '__main__':
    raise SystemExit(main())

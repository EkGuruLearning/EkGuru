#!/usr/bin/env python3
"""Add bounded contextual entry points for eight existing search landing pages.
No new pages, tutor claims, index decisions, schema, tracking or JS. --check is read-only.
"""
import html
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from lib.ultra_content import Page

START = '<!-- ekguru:contextual-entry:start -->'
END = '<!-- ekguru:contextual-entry:end -->'
TARGETS = {
    'find-tutors.html': [
        ('hindi-classes/', 'Explore online Hindi classes'),
        ('hindi-tutor-near-me/', 'Understand online options when searching for a Hindi tutor near you'),
    ],
    'name-in-hindi/index.html': [
        ('name-in-amharic/', 'Names in Amharic script'),
        ('name-in-arabic/', 'Names in Arabic script'),
        ('name-in-greek/', 'Names in Greek script'),
        ('name-in-japanese/', 'Names in Japanese writing'),
        ('name-in-korean/', 'Names in Korean script'),
        ('name-in-russian/', 'Names in Russian script'),
    ],
}


def validate():
    seen = set()
    for rows in TARGETS.values():
        for target, _ in rows:
            if target in seen:
                raise ValueError('Duplicate contextual target')
            seen.add(target)
            path = ROOT / target / 'index.html'
            if not path.is_file():
                raise ValueError('Missing existing destination: ' + target)
            page = Page(path.read_text())
            if page.noindex or page.canonical != 'https://ekguru.shop/' + target:
                raise ValueError('Destination is not already self-canonical and indexable: ' + target)


def section(relative):
    prefix = '' if relative == 'find-tutors.html' else '../'
    if relative == 'find-tutors.html':
        text = '<h2 id="tutor-learning-routes">Choose a learning route</h2><p>If you are still deciding what kind of lessons you need, compare the existing guides below before contacting a tutor. Lessons described here are online; a nearby-search page is not a promise of an in-person centre or a local tutor. Confirm each tutor’s current availability and terms directly.</p>'
        label = 'tutor-learning-routes'
    elif relative == 'name-in-hindi/index.html':
        text = '<h2 id="name-script-routes">Explore your name in another writing system</h2><p>Compare these existing script guides when your name comes from another language or you want to understand how sounds are represented differently. A suggested spelling is not an official translation or identity-document spelling. Follow the name owner’s preference and ask a fluent reader to check important uses.</p>'
        label = 'name-script-routes'
    else:
        raise ValueError('Unsupported entry page')
    links = ''.join('<li><a href="' + prefix + target + '">' + html.escape(title) + '</a></li>' for target, title in TARGETS[relative])
    return START + '\n<section aria-labelledby="' + label + '">' + text + '<ul>' + links + '</ul></section>\n' + END


def transformed(raw, relative):
    block = section(relative)
    if START in raw:
        return re.sub(re.escape(START) + r'[\s\S]*?' + re.escape(END), lambda _: block, raw, count=1)
    anchor = '<h2>Common questions</h2>' if relative == 'find-tutors.html' else '<h2>Keep going</h2>'
    if anchor not in raw:
        raise ValueError('Missing contextual insertion anchor: ' + relative)
    return raw.replace(anchor, block + '\n' + anchor, 1)


def main():
    validate(); stale = []
    for relative in TARGETS:
        path = ROOT / relative; old = path.read_text(); new = transformed(old, relative)
        if old != new:
            stale.append(relative)
            if '--check' not in sys.argv:
                path.write_text(new)
    print('Contextual entry links: 8 existing destinations, 2 source pages; ' + str(len(stale)) + (' stale' if '--check' in sys.argv else ' updated'))
    return int('--check' in sys.argv and bool(stale))


if __name__ == '__main__':
    raise SystemExit(main())

#!/usr/bin/env python3
"""Add manifest-driven contents to existing Foundation chapters, preserving HTML.

This is the first shared navigation component, not a complete textbook reader.
It never creates a planned course/phase route and never changes canonicals.
"""
import html
import json
import re
import sys
from pathlib import Path
from lib.academy_registry import validate

ROOT=Path(__file__).resolve().parents[1]
START='<!-- ekguru:textbook-navigation:start -->'
END='<!-- ekguru:textbook-navigation:end -->'
CSS='<link rel="stylesheet" href="/css/hindi-textbook-reader.css">'

def load():
    data=json.loads((ROOT/'data/hindi-academy/curriculum.json').read_text(encoding='utf8'))
    validate(data, ROOT)
    return data

def chapter_rows(data):
    book=next(x for x in next(p['books'] for p in data['textbook']['pathways'] if p['id']=='academic') if x['id']=='beginner')
    lessons={x['id']:x for x in data['lessons']}
    result=[]
    for phase in book['phases']:
        for chapter in phase['chapters']:
            for id in chapter['lesson_ids']:
                result.append({'book':book,'phase':phase,'chapter':chapter,'lesson':lessons[id]})
    return result

def render(data, current):
    e=html.escape; rows=chapter_rows(data)
    row=next((x for x in rows if x['lesson']['id']==current),None)
    if row is None: raise ValueError('lesson not in beginner contents: '+current)
    parts=[START,'<nav class="htr-nav" aria-label="Hindi textbook chapter navigation" data-eg-chrome="navigation">',
        '<p class="htr-context"><a href="/learn/">Learn</a> › <a href="/learn/hindi/">Hindi</a> › <a href="/learn/hindi/beginner/">Beginner</a> › <span>'+e(row['phase']['title'])+'</span></p>',
        '<details><summary><span lang="hi">अध्याय सूची</span> · Chapter contents</summary><ol>']
    for x in rows:
        lesson=x['lesson']; active=' aria-current="page"' if lesson['id']==current else ''
        parts.append('<li><a href="'+e(lesson['url'],quote=True)+'"'+active+'>'+e(lesson['title'])+'</a></li>')
    parts.extend(['</ol></details></nav>',END])
    return '\n'.join(parts)

def transformed(raw,data,lesson_id):
    section=render(data,lesson_id)
    if START in raw or END in raw:
        if raw.count(START)!=1 or raw.count(END)!=1: raise ValueError('invalid textbook navigation markers')
        raw=re.sub(re.escape(START)+r'[\s\S]*?'+re.escape(END),lambda _:section,raw,count=1)
    else:
        anchor='<main id="main">'
        if raw.count(anchor)!=1: raise ValueError('missing main anchor')
        raw=raw.replace(anchor,anchor+'\n'+section,1)
    if CSS not in raw:
        if '</head>' not in raw: raise ValueError('missing head')
        raw=raw.replace('</head>',CSS+'\n</head>',1)
    return raw

def main():
    data=load(); stale=[]
    for row in chapter_rows(data):
        lesson=row['lesson']; path=ROOT/lesson['url'].strip('/')/'index.html'
        old=path.read_text(encoding='utf8'); new=transformed(old,data,lesson['id'])
        if old!=new:
            stale.append(path)
            if '--check' not in sys.argv: path.write_text(new,encoding='utf8')
    print('Textbook navigation: %d existing lessons; %d %s' %(len(chapter_rows(data)),len(stale),'stale' if '--check' in sys.argv else 'updated'))
    return int('--check' in sys.argv and bool(stale))

if __name__=='__main__': raise SystemExit(main())

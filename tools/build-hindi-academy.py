#!/usr/bin/env python3
"""Build Academy directory, index and lesson navigation from the v2 registry."""
import json
import sys
from pathlib import Path
from lib.academy_registry import validate, esc, catalogue_html, index_json, lesson_navigation

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'data/hindi-academy/curriculum.json').read_text(encoding='utf8'))
validate(data, ROOT)
check = '--check' in sys.argv
stale=[]

def write(path, content):
    old=path.read_text(encoding='utf8') if path.exists() else None
    if old != content:
        stale.append(str(path.relative_to(ROOT)))
        if not check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf8')

def region(path, name, content):
    old=path.read_text(encoding='utf8')
    start_marker=f'<!-- academy:{name}:start -->'; end_marker=f'<!-- academy:{name}:end -->'
    if old.count(start_marker)!=1 or old.count(end_marker)!=1: raise ValueError('Missing markers in '+str(path))
    start=old.index(start_marker)+len(start_marker); end=old.index(end_marker,start)
    write(path,old[:start]+content+old[end:])

cards=[]
for track in data['tracks']:
    phases=''.join(f'<li><a href="{esc(p["url"])}">{esc(p["title"])}</a></li>' for p in track['phases'])
    cards.append(f'<article class="track" id="{esc(track["id"])}"><h2>{esc(track["title"])}</h2><p>{esc(track["description"])}</p><ol>{phases}</ol></article>')
region(ROOT/'learn/hindi/academy/index.html','tracks','\n'.join(cards))
region(ROOT/'learn/hindi/academy/catalogue/index.html','catalogue',catalogue_html(data))
write(ROOT/'data/hindi-academy/search-index.json',index_json(data,ROOT))
for lesson in data['lessons']:
    if lesson.get('managed_navigation'):
        page = ROOT / lesson['url'].strip('/') / 'index.html'
        region(page, 'lesson-navigation', lesson_navigation(data, lesson['id']))
if check and stale:
    print('STALE Academy: '+', '.join(stale));sys.exit(1)
print(f'Academy registry valid: {len(data["tracks"])} tracks, {len(data["lessons"])} registered lessons; '+('current' if not stale else 'updated '+', '.join(stale)))

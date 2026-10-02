#!/usr/bin/env python3
"""Bounded on-device learning inputs from the CURRENTLY available levels. Never authorizes a course.

Writes data/learning/index.json (languages -> levels -> lessons + one listening sample),
data/learning/placement/<code>.json (recognition questions that already exist in the level data) and
data/learning/offline-levels.json (the exact same-origin file list a level download may save).
The worker enforces the real byte limits at download time; this build refuses a list over budget.
"""
import hashlib
import json
import re
import sys
from lib.ultra_content import ROOT, load, save_json

LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
MAX_FILES, MAX_BYTES = 40, 3 * 1024 * 1024
RUNTIME = ['/css/style.min.css', '/css/tokens.css', '/css/ultra.css', '/js/site-shell.js', '/js/site-config.js', '/js/voice-languages.js', '/js/voice.js',
           '/js/speech-ui.js', '/js/global-srs.js', '/js/retention.js', '/js/ui-motion.js', '/js/cookie-consent.js', '/images/logo.svg',
           '/data/learning/index.json', '/data/learning/offline-levels.json']
PRIVATE = re.compile(r'/(?:admin|api|booking|join|contact|support|login|account|messages|checkout|payment)(?:[/.]|$)')


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def level_images(path):
    html = path.read_text(encoding='utf-8')
    out = set()
    for src in re.findall(r'<img\b[^>]*\bsrc=["\'](/[^"\']+\.(?:svg|png|webp|jpg))["\']', html, re.I):
        if (ROOT / src.lstrip('/')).is_file(): out.add(src)
    return out


def build(check=False):
    index, offline, ok = [], {}, True
    for course in load('data/courses/index.json')['courses']:
        code = course['code']; levels = []; questions = []; seen = set()
        for lv in LEVELS:
            if lv not in course['levels']: continue
            data = load(f'data/courses/{course["phase"]}/{code}_{lv}.json')
            page = ROOT / f'languages/{code}/level/{lv.lower()}/index.html'
            if not data or not page.is_file(): continue
            url = f'/languages/{code}/level/{lv.lower()}/'
            lessons = [l for u in data.get('level', {}).get('units', []) for l in u.get('lessons', [])]
            words = [v for l in lessons for v in l.get('vocab', []) if v.get('t') and v.get('en')]
            sample = words[0] if words else None
            levels.append({'id': lv, 'url': url, 'lessons': [{'id': l['id'].lower(), 'title': l['title'], 'url': f'{url}#{l["id"].lower()}'} for l in lessons],
                           'listening': {'text': sample['t'], 'roman': sample.get('r', ''), 'meaning': sample['en']} if sample else None})
            for lesson in lessons:
                for q in lesson.get('quiz', []):
                    options, answer = q.get('options', []), q.get('answer')
                    if not isinstance(q.get('q'), str) or not 2 <= len(options) <= 6 or not isinstance(answer, int) or isinstance(answer, bool) or not 0 <= answer < len(options) or q['q'] in seen: continue
                    seen.add(q['q']); questions.append({'id': digest([code, lv, q])[:20], 'level': lv, 'q': q['q'], 'options': options, 'answer': answer, 'why': q.get('why', '')})
            files = {url, f'/data/courses/{course["phase"]}/{code}_{lv}.json', f'/data/audio-manifest/{code}.json', f'/css/themes/{code}.css'} | set(RUNTIME) | level_images(page)
            generated = {'/data/learning/index.json', '/data/learning/offline-levels.json'}  # written by this very build
            files = sorted(f for f in files if (f in generated or (ROOT / (f.lstrip('/') + ('index.html' if f.endswith('/') else ''))).exists()) and not PRIVATE.search(f))
            size = sum((ROOT / (f.lstrip('/') + ('index.html' if f.endswith('/') else ''))).stat().st_size for f in files if f not in generated or (ROOT / f.lstrip('/')).exists())
            if len(files) > MAX_FILES or size > MAX_BYTES: raise RuntimeError(f'{code}/{lv}: offline budget exceeded ({len(files)} files, {size} bytes)')
            offline[url] = {'language': code, 'level': lv, 'urls': files, 'note': 'Only these files are downloaded. Device/browser voices may need connectivity; private forms and APIs are excluded.'}
        if levels:
            index.append({'code': code, 'name': course['name'], 'levels': levels,
                          'quality': 'Native review is not recorded. Existing levels remain available under the owner indexing freeze, not under U4 approval.'})
            ok = save_json(f'data/learning/placement/{code}.json', {'version': 1, 'code': code, 'questions': questions,
                           'note': 'A rough adaptive recognition check using question keys that already exist in the level data. Not a certified CEFR test; native/editorial review is pending.'}, check) and ok
    ok = save_json('data/learning/index.json', {'version': 1, 'languages': index, 'publication': 'No new level is published or authorized by this feature.'}, check) and ok
    ok = save_json('data/learning/offline-levels.json', {'version': 1, 'max_files_per_level': MAX_FILES, 'max_bytes_per_level': MAX_BYTES, 'levels': offline}, check) and ok
    print(f'learning inputs: {len(index)} available languages, {len(offline)} bounded level downloads; no new course publication')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(build('--check' in sys.argv))

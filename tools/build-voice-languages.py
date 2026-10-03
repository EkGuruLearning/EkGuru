#!/usr/bin/env python3
"""BCP-47 speech tags from the registry -> js/voice-languages.js, plus empty recording manifests.

Tags are requests for a device voice, never a promise that a device has one. A recording manifest
is owner-supplied: this tool creates an empty file only when none exists and never overwrites one.
"""
import json
import sys
from lib.ultra_content import ROOT, load, save_json

NOTE = ('No licensed recording has been supplied for this language. Device speech, where installed, is synthetic. '
        'An entry needs: text, lang (same language as this file), a same-origin /audio/ URL, an allowed license '
        '(CC0-1.0, CC-BY-4.0, CC-BY-SA-4.0, owner-recorded) and, for kind "human", recorder + source_url (https).')


def main():
    check = '--check' in sys.argv
    registry = {r['code']: r for r in load('data/languages/registry.json')['languages']}
    wanted = {c for c, r in registry.items() if r['course'] or r['starter_pack']}
    wanted |= {p['lang'] for p in load('data/language-packs.json', {'packs': []})['packs'] if p['lang'] in registry}
    ok = True; mapping = {}
    for code in sorted(wanted):
        row = registry[code]
        mapping[code] = {'tag': row['speech_tag'], 'name': row['name']}
        path = ROOT / f'data/audio-manifest/{code}.json'
        manifest = json.loads(path.read_text()) if path.exists() else None
        if manifest is None:
            ok = save_json(f'data/audio-manifest/{code}.json', {'schema_version': 1, 'lang': row['speech_tag'], 'entries': [], 'note': NOTE}, check) and ok
        elif manifest.get('entries'):
            mapping[code]['rec'] = 1
            if manifest.get('lang') != row['speech_tag']:
                print(f'  {code}: manifest has entries with a different lang ({manifest.get("lang")!r}) — not rewritten')
        elif manifest.get('lang') != row['speech_tag']:
            # An empty manifest is ours to correct: a stale tag here is the bug that
            # produced ja-JA / ko-KO / uk-UK / vi-VI on every page that inlines the table.
            manifest['lang'] = row['speech_tag']
            ok = save_json(f'data/audio-manifest/{code}.json', manifest, check) and ok
            print(f'  {code}: audio manifest lang corrected to {row["speech_tag"]}')
    # Legacy two-letter hub codes are aliases of the canonical course codes, not second languages.
    for canonical, info in load('data/global/language-code-map.json').get('canonical_course_codes', {}).items():
        for alias in info.get('aliases', []):
            if len(alias) == 2 and alias != canonical and canonical in mapping and alias not in mapping:
                mapping[alias] = dict(mapping[canonical])
    source = '/* Generated from the registry by tools/build-voice-languages.py. These are tags, not promises of device voices. */\nwindow.EKGURU_VOICE_LANGUAGES=' + json.dumps(mapping, ensure_ascii=False, separators=(',', ':')) + ';\n'
    out = ROOT / 'js/voice-languages.js'
    if not out.exists() or out.read_text() != source:
        if check:
            print('STALE js/voice-languages.js'); ok = False
        else:
            out.write_text(source)
    print(f'voice languages: {len(mapping)} tags; recordings: {sum(1 for v in mapping.values() if v.get("rec"))}')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())

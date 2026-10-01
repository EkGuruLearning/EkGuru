#!/usr/bin/env python3
"""U4: 700-language DRAFT registry + 197 country contexts from the existing inventory.

Every row starts as draft/no review. Country speaker figures are kept only with a citable URL;
an agent-compiled placeholder is dropped, never presented as a source. A generic homepage is an
imported reference, not a freshly verified speaker count. No tier, status or reviewer is invented.
"""
import json
import re
import sys
from lib.ultra_content import ROOT, load, save_json

RTL = {'Arab', 'Hebr', 'Thaa', 'Syrc', 'Nkoo', 'Adlm', 'Rohg', 'Mand', 'Samr', 'Mend'}
COURSE_CODE = {'arb': 'ar', 'azj': 'az', 'fil': 'fil', 'uzn': 'uzn', 'zsm': 'zsm', 'cmn': 'zh', 'kmr': 'ku', 'pbu': 'ps', 'npi': 'npi'}
BCP47 = {'ar': 'ar', 'az': 'az', 'fil': 'fil', 'uzn': 'uz', 'zsm': 'ms', 'zh': 'zh', 'ku': 'kmr', 'ps': 'pbu', 'npi': 'ne'}


def citable(source):
    return bool(source.get('source_url')) and source.get('evidence_type') != 'agent-compiled'


def speech_tags():
    tags = {}
    player = (ROOT / 'js/course-player.js').read_text(encoding='utf-8')
    block = re.search(r'var TTS_LANG = \{([^}]*)\}', player)
    if block:
        tags.update({k: v for k, v in re.findall(r'(\w+):\s*"([A-Za-z-]+)"', block[1])})
    for pack in load('data/language-packs.json', {'packs': []})['packs']:
        if pack.get('speechTag'): tags[pack['lang']] = pack['speechTag']
    return tags


def build():
    inventory = load('data/global/languages.json')['languages']
    relations = load('data/global/language-country-relations.json')['relations']
    catalogue = {c['code']: c for c in load('data/courses/index.json')['courses']}
    packs = {p['lang']: p for p in load('data/language-packs.json', {'packs': []})['packs']}
    tags = speech_tags()
    taken = {}
    rows = []
    for item in inventory:
        iso3 = item['iso_639_3']; iso1 = item.get('iso_639_1')
        code = COURSE_CODE.get(iso3) or (iso1 if iso1 and sum(1 for x in inventory if x.get('iso_639_1') == iso1) == 1 else iso3)
        if code in taken: raise SystemExit(f'duplicate registry code {code}: {item["language_id"]} / {taken[code]}')
        taken[code] = item['language_id']
        script = item.get('script') or None
        scripts = [script] if script else []
        bcp = BCP47.get(code) or iso1 or iso3
        tier = 'T1' if code in catalogue else ('T2' if code in packs else 'T3')
        unresolved = [] if scripts else ['script']
        rows.append({
            'code': code, 'language_id': item['language_id'], 'iso639_3': iso3, 'iso639_1': iso1, 'glottocode': item.get('glottocode'),
            'bcp47': bcp, 'speech_tag': tags.get(code) or bcp,
            'name': item['canonical_name'], 'endonym': item.get('native_name') or item['canonical_name'],
            'aliases': item.get('aliases') or [], 'scripts': scripts, 'direction': 'rtl' if scripts and scripts[0] in RTL else 'ltr',
            'family': item.get('language_family'), 'language_type': item['language_type'],
            'modality': 'signed' if item['language_type'] == 'SIGN_LANGUAGE' else 'spoken-or-written',
            'tier': tier, 'status': 'draft', 'course': code in catalogue, 'starter_pack': code in packs,
            'catalogue': {'phase': catalogue[code]['phase'], 'levels_available': sorted(catalogue[code]['levels']), 'quality_status': catalogue[code].get('quality_status')} if code in catalogue else None,
            'review': {'status': 'none', 'reviewer_id': None, 'consent_to_publish': False, 'content_digest': None, 'reviewed_on': None, 'owner_verified': False},
            'countries': [], 'unresolved': unresolved})
    by_id = {r['language_id']: r for r in rows}
    grouped = {}
    for rel in relations:
        row = by_id.get(rel['language_id'])
        if not row: continue
        entry = grouped.setdefault((rel['language_id'], rel['country_id']), {'code': rel['country_id'], 'roles': set(), 'sources': {}, 'speaker_estimates': []})
        entry['roles'].add(rel['category'])
        good = [s for s in rel.get('sources', []) if citable(s)]
        for s in good:
            entry['sources'].setdefault(s['source_url'], {'title': s.get('source_name') or s.get('key'), 'url': s['source_url'], 'evidence_type': s.get('evidence_type'), 'checked_on': None, 'verification': 'imported_reference_not_freshly_verified'})
        est = rel.get('speaker_estimate') or {}
        if good and (est.get('l1') or est.get('total')):
            entry['speaker_estimates'].append({'l1': est.get('l1'), 'total': est.get('total'), 'confidence': est.get('confidence'), 'source_urls': sorted({s['source_url'] for s in good})})
    for (language_id, country), e in sorted(grouped.items()):
        by_id[language_id]['countries'].append({'code': country, 'roles': sorted(e['roles']), 'sources': sorted(e['sources'].values(), key=lambda s: s['url']), 'speaker_estimates': e['speaker_estimates']})
    rows.sort(key=lambda r: r['code'])
    registry = {'schema_version': 1, 'generated_by': 'tools/build-language-registry.py',
                'policy': 'Draft registry only. Existing availability/indexing is preserved by owner decision and is not an approval. No row has a native/editorial review. A source URL is a reference, not proof that a number is freshly verified.',
                'counts': {'languages': len(rows), 'tiers': {t: sum(r['tier'] == t for r in rows) for t in ('T1', 'T2', 'T3')}, 'sign': sum(r['modality'] == 'signed' for r in rows), 'rtl': sum(r['direction'] == 'rtl' for r in rows)},
                'languages': rows}
    sovereign = load('data/language-inventory/sovereign-194.json')['countries']
    supplement = load('data/language-inventory/supplement-3.json')['countries']
    code_of = {r['language_id']: r['code'] for r in rows}
    countries = []
    for supplemental, group in ((False, sovereign), (True, supplement)):
        for c in group:
            langs = []
            for rel in relations:
                if rel['country_id'] != c['cca2'] or rel['language_id'] not in code_of: continue
                langs.append({'language_id': rel['language_id'], 'code': code_of[rel['language_id']], 'name': rel['language_name'], 'roles': [rel['category']], 'review_status': 'needs_human_crosscheck'})
            merged = {}
            for l in langs:
                m = merged.setdefault(l['language_id'], l)
                if l is not m: m['roles'] = sorted(set(m['roles']) | set(l['roles']))
            countries.append({'code': c['cca2'], 'name': c['name'], 'region': c.get('region'), 'supplemental': supplemental, 'languages': sorted(merged.values(), key=lambda x: x['code'])})
    return registry, {'schema_version': 1, 'countries': countries}


def main():
    check = '--check' in sys.argv
    registry, countries = build()
    ok = save_json('data/languages/registry.json', registry, check) and save_json('data/languages/countries.json', countries, check)
    print(f"language registry: {registry['counts']['languages']} drafts, {len(countries['countries'])} countries, tiers {registry['counts']['tiers']}")
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())

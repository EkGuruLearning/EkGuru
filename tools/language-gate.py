#!/usr/bin/env python3
"""U4 language quality gate. Reports honestly; never edits a page and never changes indexing.

A language is PASS only if every rule holds: (a) schema valid; (b) >=85% of its teaching text is unique against
every other language; (c) vocabulary is in the declared script's Unicode ranges; (d) romanisation present for
non-Latin scripts; (e) no placeholder text; (f) facts and culture notes carry sources; (g) a digest-bound native
review owner-verified; (h) a valid voice tag and manifest; (i) the tier's minimum counts.
The owner froze existing index/noindex, so failures are REPORTED as 'indexed failed pages' (release blockers),
not quarantined. Use --enforce-publication as the release gate.

  python3 tools/language-gate.py                  write data/quality/language-gate.json
  python3 tools/language-gate.py --check          fail if the report is stale
  python3 tools/language-gate.py --enforce-publication
  python3 tools/language-gate.py --lang es        details + content digest for a reviewer
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from lib.text import in_script, tokens
from lib.ultra_content import ROOT, load, save_json

RUNGS = ['A1', 'A1+', 'A2', 'A2+', 'B1', 'B1+', 'B2', 'B2+', 'C1', 'C1+', 'C2']
SLUG_CODE = {'hindi': 'hi', 'bengali': 'bn', 'gujarati': 'gu', 'kannada': 'kn', 'malayalam': 'ml', 'marathi': 'mr', 'punjabi': 'pa', 'tamil': 'ta', 'telugu': 'te', 'urdu': 'ur'}
PLACEHOLDER = re.compile(r'lorem ipsum|\[translate\]|coming soon|placeholder text', re.I)
# A developer marker is not a word. Written case-insensitively, `\bTODO\b` also
# matched the Portuguese "todo" ("Eu a vejo todo dia.", "Com todo o respeito…")
# and failed the whole Portuguese course — a language with 100% real content —
# for placeholder text it never had. The Spanish "todo" is the same trap for a
# T1 language that is still to come. Markers are therefore matched in capitals
# only, which is how a leftover one is actually written in a data file; every
# text this gate scans passes through either JSON or hand-written prose, so the
# capitalisation is available to it. Verified before the change: no uppercase
# TODO or TBD exists anywhere under data/courses.
MARKER = re.compile(r'\bTODO\b|\bTBD\b')
WORD_LISTS = ['greetings', 'pronouns', 'verbs', 'days', 'time_words', 'family', 'food_words', 'colors', 'core_nouns', 'travel_words', 'shopping_words', 'classifiers']
PHRASE_LISTS = ['food_phrases', 'shopping_phrases', 'travel_phrases', 'daily_phrases']
REVIEW_ID = re.compile(r'^[a-zA-Z0-9_-]{8,64}$')


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def course_files(code, catalogue):
    entry = catalogue.get(code)
    if not entry: return {}
    return {r: ROOT / f'data/courses/{entry["phase"]}/{code}_{r}.json' for r in RUNGS if (ROOT / f'data/courses/{entry["phase"]}/{code}_{r}.json').exists()}


def strings(obj):
    if isinstance(obj, str): yield obj
    elif isinstance(obj, dict):
        for v in obj.values(): yield from strings(v)
    elif isinstance(obj, list):
        for v in obj: yield from strings(v)


def course_text(path):
    d = json.loads(path.read_text(encoding='utf-8')); out = []; vocab = []
    for u in d['level'].get('units', []):
        for l in u.get('lessons', []):
            vocab += [v for v in l.get('vocab', []) if isinstance(v, dict)]
            out += list(strings({k: v for k, v in l.items() if k not in ('flashcards', 'srs_policy', 'srs_candidates')}))
    out += list(strings(d['level'].get('test', {})))
    return d, out, vocab


def starter_input(code, row):
    slug = next((s for s, c in SLUG_CODE.items() if c == code), None)
    path = ROOT / f'tools/lang-data/{slug}.json' if slug else None
    if not path or not path.exists(): return None
    d = json.loads(path.read_text(encoding='utf-8'))
    words = [{'t': x.get('t', ''), 'r': x.get('r', ''), 'en': x.get('en', '')} for k in WORD_LISTS for x in d.get(k, [])]
    words += [{'t': x.get('t', ''), 'r': x.get('r', ''), 'en': str(x.get('n', ''))} for x in d.get('numbers', [])]
    phrases = [x for k in PHRASE_LISTS + ['greetings'] for x in d.get(k, [])]
    grammar = [{'title': d.get(k + '_title', k), 'explain': d[k]} for k in ('gender_note', 'present_note', 'negation_note', 'counting_note') if d.get(k)]
    practice = [d[k] for k in ('quiz', 'typing', 'review_deck') if d.get(k)]
    return {'code': code, 'script_lesson': {'title': d.get('script_name', ''), 'letters': d.get('vowels', []) + d.get('consonants', [])},
            'words': words, 'phrases': phrases, 'dialogues': d.get('dialogues', []), 'grammar': grammar, 'practice': practice, 'voice_tag': row['speech_tag']}


def shingles(parts, n=7):
    toks = tokens(' '.join(parts)); return {' '.join(toks[i:i + n]) for i in range(max(0, len(toks) - n + 1))}


def review_state(code, digest_now):
    path = ROOT / f'data/reviews/{code}.json'
    if not path.exists(): return 'none', 'no_native_review'
    r = json.loads(path.read_text(encoding='utf-8')).get('review', {})
    if r.get('status') != 'reviewed' or r.get('owner_verified') is not True or not REVIEW_ID.match(str(r.get('reviewer_id') or '')) or not r.get('reviewed_on'): return 'invalid', 'review_record_incomplete'
    if r.get('consent_to_publish') is False and 'name' in r: return 'invalid', 'review_names_without_consent'
    if r.get('consent_to_publish') is True and not r.get('name'): return 'invalid', 'review_consent_without_name'
    if r.get('content_digest') != digest_now: return 'stale', 'review_digest_mismatch'
    return 'verified', None


def run_schema(request):
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
        json.dump(request, f); name = f.name
    out = subprocess.run(['node', 'tools/lib/validate-language-schema.mjs', name], cwd=ROOT, capture_output=True, text=True)
    if out.returncode: raise SystemExit('schema validator failed: ' + out.stderr[-600:])
    return json.loads(out.stdout)


def evaluate():
    registry = load('data/languages/registry.json'); rows = registry['languages']
    catalogue = {c['code']: c for c in load('data/courses/index.json')['courses']}
    files = {r['code']: course_files(r['code'], catalogue) for r in rows if r['tier'] == 'T1'}
    starters = {r['code']: starter_input(r['code'], r) for r in rows if r['tier'] == 'T2'}
    refs = {r['code']: ROOT / f'data/reference/{r["code"]}.json' for r in rows if r['tier'] == 'T3' and (ROOT / f'data/reference/{r["code"]}.json').exists()}
    schema = run_schema({'registry': rows, 't1': {c: [{'rung': k, 'file': str(p)} for k, p in f.items()] for c, f in files.items()}, 't2': {c: s for c, s in starters.items() if s}, 't3': {c: str(p) for c, p in refs.items()}})
    texts, contents = {}, {}
    for r in rows:
        code = r['code']
        if code in files and files[code]:
            parts, vocab, levels = [], [], {}
            for rung, p in files[code].items():
                d, text, v = course_text(p); parts += text; vocab += v; levels[rung] = d['level']
            texts[code] = (parts, vocab); contents[code] = levels
        elif starters.get(code):
            s = starters[code]; texts[code] = ([json.dumps(s['dialogues'], ensure_ascii=False), ' '.join(g['explain'] for g in s['grammar'])], s['words']); contents[code] = s
        elif code in refs:
            d = json.loads(refs[code].read_text(encoding='utf-8')); texts[code] = ([d.get('guide', '')], []); contents[code] = d
    sets = {c: shingles(parts) for c, (parts, _) in texts.items()}
    everywhere = Counter(s for v in sets.values() for s in v)
    results = []; fail_reasons = Counter()
    for r in rows:
        code, tier = r['code'], r['tier']; reasons = []; metrics = {}
        if code in schema['registry']: reasons.append('registry_schema_invalid')
        if not r['scripts']: reasons.append('script_unresolved')
        if not re.match(r'^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$', r['speech_tag']): reasons.append('voice_tag_invalid')
        if (r['course'] or r['starter_pack']) and not (ROOT / f'data/audio-manifest/{code}.json').exists(): reasons.append('voice_manifest_missing')
        if tier == 'T1':
            have = list(files.get(code, {})); missing = [x for x in RUNGS if x not in have]; metrics['rungs'] = len(have)
            if missing: reasons.append('rungs_missing')
            for rung, errs in schema['t1'].get(code, {}).items():
                for e in errs:
                    kind = e.split(':')[0]; path = e.split(':', 1)[1]
                    reasons.append('t1:' + ('extra_content_missing' if '/level/extra' in path or path.endswith('.extra') else 'units_or_lessons_out_of_range' if 'units' in path else 'test_items_out_of_range' if 'test' in path else 'lesson_fields_or_practice_depth' if 'lessons' in path else kind))
            ext = [p for p in (ROOT / f'data/courses/{catalogue[code]["phase"]}').glob(f'{code}_*.json') if p.stem.split('_')[1] not in RUNGS] if code in catalogue else []
            if ext: metrics['legacy_extension_files_not_cefr'] = len(ext)
        elif tier == 'T2':
            s = starters.get(code)
            if not s: reasons.append('starter_input_missing')
            else:
                metrics.update({'words': len(s['words']), 'phrases': len(s['phrases']), 'dialogues': len(s['dialogues']), 'grammar': len(s['grammar']), 'practice_sets': len(s['practice'])})
                for e in schema['t2'].get(code, []): reasons.append('t2:' + e.split(':')[1].lstrip('/').split('.')[0] + ':' + e.split(':')[0])
        else:
            if code not in refs: reasons.append('t3:reference_missing')
            for e in schema['t3'].get(code, []): reasons.append('t3:' + e)
        if code in texts:
            parts, vocab = texts[code]; mine = sets[code]
            if mine:
                ratio = sum(1 for s in mine if everywhere[s] == 1) / len(mine); metrics['unique_text_ratio'] = round(ratio, 3)
                if ratio < 0.85: reasons.append('unique_text_below_85')
            bad = [v for v in vocab if v.get('t') and not in_script(v['t'], r['scripts'] or ['Latn'])]; metrics['script_mismatch'] = len(bad)
            if bad: reasons.append('script_mismatch')
            if 'Latn' not in r['scripts'] and any(not v.get('r') for v in vocab if v.get('t')): reasons.append('romanisation_missing')
            if any(PLACEHOLDER.search(p) or MARKER.search(p) for p in parts): reasons.append('placeholder_text')
        status, why = review_state(code, digest(contents.get(code, {})))
        if why: reasons.append(why)
        if tier in ('T1', 'T2') and status != 'verified' and 'no_native_review' not in reasons and why is None: reasons.append('no_native_review')
        reasons = sorted(set(reasons)); fail_reasons.update(reasons)
        results.append({'code': code, 'tier': tier, 'result': 'FAIL' if reasons else 'PASS', 'review_verified': status == 'verified', 'content_digest': digest(contents.get(code, {})) if code in contents else None, 'reasons': reasons, 'metrics': metrics})
    by_code = {x['code']: x for x in results}
    baseline = load('data/quality/indexing-baseline.json')['pages']; indexed_failed = []
    for rel, state in baseline.items():
        if not state['indexable']: continue
        parts = rel.split('/'); code = parts[1] if parts[0] == 'languages' and len(parts) > 2 else SLUG_CODE.get(parts[1]) if parts[0] == 'learn' and len(parts) > 2 and parts[1] in SLUG_CODE else SLUG_CODE.get(parts[0]) if parts[0] in SLUG_CODE and len(parts) > 1 else None
        if code in by_code and by_code[code]['result'] == 'FAIL': indexed_failed.append(rel)
    counts = Counter(f"{x['tier']}:{x['result']}" for x in results)
    return {'schema_version': 1, 'generated_by': 'tools/language-gate.py', 'owner_decision': 'Existing indexing is frozen. Failures are reported as release blockers; no page is quarantined or changed by this report.',
            'word_count_method': 'Unicode tokens (spaced scripts) plus per-character units for CJK/Thai; an audit proxy, not native segmentation',
            'publication_status': 'BLOCKED' if indexed_failed or any(x['result'] == 'FAIL' for x in results if x['tier'] != 'T3') else 'OPEN',
            'counts': dict(sorted(counts.items())), 'top_fail_reasons': fail_reasons.most_common(12),
            'indexed_failed_pages': len(indexed_failed), 'indexed_failed_sample': indexed_failed[:12], 'languages': results}


def selftest():
    """The placeholder patterns, on the texts that made them wrong.

    The Portuguese cases are the real lesson sentences from data/courses that
    the case-insensitive `\\bTODO\\b` used to flag; the marker cases are what a
    genuine leftover looks like. Expected results are written out rather than
    computed, so changing either pattern has to be a deliberate change here too.
    """
    checks = [
        # Portuguese "todo" is a word, not a marker — the false positive this fixes.
        ("Portuguese todo", "Eu a vejo todo dia.", False),
        ("Portuguese todo, longer", "Com todo o respeito pela sua proposta, gostaria de esboçar uma alternativa.", False),
        ("Portuguese todo, subject", "Todo o dia eu estudo português.", False),
        # Spanish, the same trap in a T1 language still to be written.
        ("Spanish todo", "Todo el mundo habla español.", False),
        # Portuguese "tudo" was never matched; it must stay clean too.
        ("Portuguese tudo", "Tudo bem, obrigado.", False),
        # A real leftover marker is written in capitals.
        ("TODO marker", "TODO: replace with real Portuguese", True),
        ("bare TBD", "TBD", True),
        ("inline TBD", "This is TBD by the author", True),
        # English filler phrases are still caught in any case.
        ("lorem ipsum", "lorem ipsum dolor sit amet", True),
        ("translate tag", "[translate] this later", True),
        ("coming soon", "More lessons coming soon", True),
        ("placeholder text", "placeholder text here", True),
        ("coming soon, capitals", "COMING SOON", True),
    ]
    bad = []
    for name, text, expected in checks:
        got = bool(PLACEHOLDER.search(text) or MARKER.search(text))
        if got != expected:
            bad.append("%s: flagged=%s, expected=%s" % (name, got, expected))
    if bad:
        print("FAIL  placeholder selftest — " + "; ".join(bad))
        return 1
    print("ok    placeholder patterns: Portuguese/Spanish 'todo' is text, capitalised TODO/TBD is a marker")
    return 0


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); ap.add_argument('--enforce-publication', action='store_true'); ap.add_argument('--lang'); ap.add_argument('--selftest', action='store_true'); a = ap.parse_args()
    if a.selftest:
        return selftest()
    report = evaluate()
    if a.lang:
        row = next((x for x in report['languages'] if x['code'] == a.lang), None)
        if not row: raise SystemExit('unknown language ' + a.lang)
        print(json.dumps(row, ensure_ascii=False, indent=2)); return 0
    ok = save_json('data/quality/language-gate.json', report, a.check)
    print('language quality:', dict(report['counts']), '· publication:', report['publication_status'], '· indexed failed pages:', report['indexed_failed_pages'])
    if a.enforce_publication and report['publication_status'] != 'OPEN':
        print('RELEASE BLOCKED: language gate failures remain; the owner indexing freeze is not a pass'); return 1
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())

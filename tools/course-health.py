#!/usr/bin/env python3
"""Weekly course health: voice tags/manifests, unverified or stale sources, reviewer gaps and gate failures.
Deterministic (no timestamp in the report). `--issue` opens or updates ONE GitHub issue labelled course-health
(CI only, needs a token). It reports; it never edits a page, an index decision or a review record."""
import argparse
import datetime as dt
import json
import re
import subprocess
from lib.ultra_content import ROOT, load, save_json


def build(today=None):
    registry = load('data/languages/registry.json')['languages']; gate = {x['code']: x for x in load('data/quality/language-gate.json')['languages']}
    today = today or dt.date.today(); broken, unverified, stale, reviewer_gap = [], {}, {}, []
    for r in registry:
        code = r['code']
        if (r['course'] or r['starter_pack']) and (not re.match(r'^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$', r['speech_tag']) or not (ROOT / f'data/audio-manifest/{code}.json').exists()): broken.append(code)
        n = old = 0
        for c in r['countries']:
            for s in c['sources']:
                n += 1
                if not s.get('checked_on'): continue
                if (today - dt.date.fromisoformat(s['checked_on'])).days > 365: old += 1
        if r['tier'] in ('T1', 'T2'):
            unverified[code] = sum(1 for c in r['countries'] for s in c['sources'] if not s.get('checked_on'))
            if old: stale[code] = old
            if not gate[code]['review_verified']: reviewer_gap.append(code)
    report = {'schema_version': 1, 'scope': 'Repository health only. Learner-reported errors live in the questions API/sheet and are not readable offline.',
              'broken_voice_tags_or_manifests': sorted(broken), 'languages_with_unverified_sources': sum(1 for v in unverified.values() if v), 'unverified_source_references': sum(unverified.values()),
              'stale_sources_over_12_months': stale, 'reviewer_gaps_t1_t2': len(reviewer_gap), 'gate_counts': load('data/quality/language-gate.json')['counts'],
              'indexed_failed_pages': load('data/quality/language-gate.json')['indexed_failed_pages'],
              'status': 'ATTENTION' if broken or stale or reviewer_gap else 'OK',
              'learner_reports': 'unavailable_in_repository'}
    return report


def issue(report):
    body = ('Automated weekly course-health report (owner indexing freeze unchanged; nothing is quarantined automatically).\n\n```json\n' + json.dumps({k: v for k, v in report.items() if k != 'gate_counts'}, indent=2) + '\n```\n\nGate counts: `' + json.dumps(report['gate_counts']) + '`\nSee data/quality/course-health.json and data/quality/language-gate.json.')
    found = json.loads(subprocess.run(['gh', 'issue', 'list', '--label', 'course-health', '--state', 'open', '--json', 'number'], capture_output=True, text=True, check=True).stdout)
    if found: subprocess.run(['gh', 'issue', 'edit', str(found[0]['number']), '--body', body], check=True)
    else: subprocess.run(['gh', 'issue', 'create', '--title', 'Course health: weekly attention needed', '--label', 'course-health', '--body', body], check=True)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); ap.add_argument('--issue', action='store_true'); a = ap.parse_args()
    report = build(); ok = save_json('data/quality/course-health.json', report, a.check)
    print('course health:', report['status'], '· voice problems', len(report['broken_voice_tags_or_manifests']), '· reviewer gaps', report['reviewer_gaps_t1_t2'], '· unverified source refs', report['unverified_source_references'])
    if a.issue and report['status'] != 'OK': issue(report)
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())

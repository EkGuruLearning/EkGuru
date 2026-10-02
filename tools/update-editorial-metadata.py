#!/usr/bin/env python3
"""Truthful 'Updated' dates. Own-content hashes exclude shared chrome, controls and hidden markup, so a rebuild or a
new menu is not an edit. Pages unchanged since the original commit keep date=null ('legacy date unknown'); a changed or
new page gets the run date. Historical dates are never invented and the indexing baseline is never touched."""
import argparse
import datetime as dt
import subprocess
from zoneinfo import ZoneInfo
from lib.ultra_content import ROOT, load, own_hash, pages, save_json


def original_hashes(files, commit):
    request = ''.join(f'{commit}:{p.relative_to(ROOT).as_posix()}\n' for p in files)
    data = subprocess.run(['git', 'cat-file', '--batch'], input=request.encode(), capture_output=True, cwd=ROOT, check=True).stdout
    offset, out = 0, {}
    for p in files:
        end = data.index(b'\n', offset); header = data[offset:end].decode(); offset = end + 1
        if header.endswith(' missing'): continue
        size = int(header.split()[-1]); out[p.relative_to(ROOT).as_posix()] = own_hash(data[offset:offset + size].decode('utf-8')); offset += size + 1
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); ap.add_argument('--date'); args = ap.parse_args()
    today = args.date or dt.datetime.now(ZoneInfo('Asia/Kolkata')).date().isoformat(); dt.date.fromisoformat(today)
    files = [p for p in pages() if p.name != 'admin.html']; old = load('data/editorial/page-metadata.json', {}).get('pages', {})
    base = original_hashes(files, load('data/quality/indexing-baseline.json')['base_commit']) if any(p.relative_to(ROOT).as_posix() not in old for p in files) else {}
    rows, changed = {}, 0
    for p in files:
        rel = p.relative_to(ROOT).as_posix(); h = own_hash(p.read_text(encoding='utf-8')); prior = old.get(rel)
        if prior and prior['hash'] == h: rows[rel] = prior; continue
        if prior: rows[rel] = {'hash': h, 'updated': today}
        else: rows[rel] = {'hash': h, 'updated': None if base.get(rel) == h else today}
        changed += 1
    data = {'schema_version': 1, 'measurement_version': 2, 'policy': 'Own-content hashes exclude shared chrome, controls, hidden markup and diagrams. A null date means the page text is unchanged since the original record and its real editorial date is unknown. Native review is separate.', 'pages': rows}
    ok = save_json('data/editorial/page-metadata.json', data, args.check)
    print(f'editorial metadata: {len(rows)} pages, {changed} newly measured; no historical date invented')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())

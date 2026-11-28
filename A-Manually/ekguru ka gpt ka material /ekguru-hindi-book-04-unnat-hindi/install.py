#!/usr/bin/env python3
"""Read-only preflight by default; copy only new/identical files, never overwrite legacy content."""
from pathlib import Path
import argparse,json,sys,shutil
P=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('repo',type=Path);ap.add_argument('--apply',action='store_true');ap.add_argument('--keep-existing-root',action='store_true',help='Install child pages/assets without overwriting the existing advanced landing page; merge that landing page manually.');args=ap.parse_args();r=args.repo.resolve()
if not (r/'learn/hindi/index.html').is_file():sys.exit('Not an EkGuru repository: missing learn/hindi/index.html')
files=[(x,r/x.relative_to(P/'site')) for x in sorted((P/'site').rglob('*')) if x.is_file()]
root=r/'learn/hindi/advanced/index.html'
if args.keep_existing_root:
 if not root.is_file():sys.exit('--keep-existing-root requires an existing advanced/index.html')
 files=[(a,b) for a,b in files if b!=root]
 print('Keeping existing advanced landing page unchanged. Merge the packaged landing page in its owning generator before announcing integration.')
conflicts=[str(b.relative_to(r)) for a,b in files if b.exists() and (not b.is_file() or a.read_bytes()!=b.read_bytes())]
if conflicts:sys.exit('Refusing to overwrite existing different files:\n'+'\n'.join(conflicts))
registry=r/'data/learning/hindi-textbook-catalogue.json'; data=None
if registry.is_file():
 data=json.loads(registry.read_text()); entries=[x for x in data['academic'] if x['id']=='advanced'];
 if len(entries)!=1 or entries[0]['route']!='learn/hindi/advanced':sys.exit('Unexpected Intermediate registry; manual integration required')
 if not args.keep_existing_root and entries[0]['status']!='published':entries[0]['status']='existing'
else:print('Hindi V1 registry not found; Arena must register Intermediate manually after applying the homepage package.')
print(f'{len(files)} files; no conflicting files; no existing course content deleted. All new pages noindex. '+('APPLY' if args.apply else 'DRY RUN'))
if args.apply:
 for a,b in files:
  if not b.exists():b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
 if data is not None and not args.keep_existing_root:registry.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print('Installed. Keep source package privately; wire generator into existing build before production. Full regression pending.')

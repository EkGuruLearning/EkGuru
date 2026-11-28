#!/usr/bin/env python3
"""Safe installer: default dry-run; never overwrite different files or change existing indexing."""
from pathlib import Path
import argparse,json,shutil,sys
P=Path(__file__).resolve().parent;ap=argparse.ArgumentParser();ap.add_argument('repo',type=Path);ap.add_argument('--apply',action='store_true');a=ap.parse_args();r=a.repo.resolve()
if not (r/'learn/hindi/index.html').is_file():sys.exit('Not an EkGuru repository: missing learn/hindi/index.html')
files=[(p,r/p.relative_to(P/'site')) for p in sorted((P/'site').rglob('*')) if p.is_file()];conflicts=[str(b.relative_to(r)) for _,b in files if b.is_symlink() or any(t.is_symlink() for t in b.parents if t!=r and r in t.parents)];conflicts += [str(b.relative_to(r)) for p,b in files if b.exists() and (not b.is_file() or p.read_bytes()!=b.read_bytes())]
if conflicts:sys.exit('Refusing overwrite or symlink collision:\n'+'\n'.join(conflicts))
reg=r/'data/learning/hindi-textbook-catalogue.json';data=None
if reg.is_file():
 data=json.loads(reg.read_text());ids=['foundation','beginner','intermediate','advanced','mastery'];entries=data.get('adult',[])
 for id in ids:
  match=[x for x in entries if x['id']==id]
  if len(match)!=1 or match[0]['route']!='learn/hindi/older-adults/'+id:sys.exit('Unexpected adult registry; reconcile manually')
  if match[0]['status']!='published':match[0]['status']='existing'
else:print('Hindi V1 registry absent; wire all five stages manually.')
print(f'{len(files)} files; no conflicts. '+('APPLY' if a.apply else 'DRY RUN'))
if a.apply:
 for p,b in files:
  if not b.exists():b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,b)
 if data is not None:reg.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print('Installed locally; full EkGuru integration, editorial review and publication approval remain pending.')

#!/usr/bin/env python3
"""Install combined build output without overwriting differing repository files.
Read-only by default; explicitly retain legacy textbook roots when requested.
"""
from pathlib import Path
import argparse,sys,shutil,json
R=Path(__file__).resolve().parent; S=R/'site'
ROOTS={f'learn/hindi/{name}/index.html' for name in ['kids','beginner','intermediate','advanced','mastery','older-adults']}
def plan(repo,keep_roots=False):
 if not (repo/'learn/hindi/index.html').is_file():raise ValueError('Missing existing Hindi hub: not the expected repository')
 copies=[];conflicts=[];retained=[];same=0
 for f in sorted(S.rglob('*')):
  if not f.is_file():continue
  rel=f.relative_to(S).as_posix();d=repo/rel
  if rel=='learn/hindi/index.html':continue # preview-only hub
  if not d.resolve().is_relative_to(repo.resolve()):conflicts.append(rel+' (outside repository)');continue
  if d.exists():
   if d.is_file() and d.read_bytes()==f.read_bytes():same+=1;continue
   if keep_roots and rel in ROOTS and d.is_file():retained.append(rel);continue
   conflicts.append(rel);continue
  if any(p.exists() and not p.is_dir() for p in d.parents if p.is_relative_to(repo)):conflicts.append(rel+' (parent not a directory)');continue
  copies.append((f,d))
 return copies,conflicts,retained,same
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('repo',type=Path);ap.add_argument('--apply',action='store_true');ap.add_argument('--keep-existing-roots',action='store_true');a=ap.parse_args();repo=a.repo.resolve()
 try:copies,conflicts,retained,same=plan(repo,a.keep_existing_roots)
 except (ValueError,OSError) as ex:sys.exit('BLOCKED: '+str(ex))
 print(json.dumps({'new_files':len(copies),'identical_files':same,'retained_legacy_roots':retained,'conflicts':conflicts,'preview_hub_excluded':True},indent=2))
 if conflicts:sys.exit('BLOCKED: reconcile differing files in owning generators before applying. Nothing written.')
 if not a.apply:print('Dry run only. No repository changes.');return
 for f,d in copies:
  d.parent.mkdir(parents=True,exist_ok=True)
  # Fail safely if another process created a file after the preflight.
  with d.open('xb') as out:out.write(f.read_bytes())
 print('Copied new files only. Register actual integrated books in the existing Hindi hub and wire private source generators before rebuilding.')
if __name__=='__main__':main()

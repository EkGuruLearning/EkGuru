#!/usr/bin/env python3
"""Read-only by default. Patch the current generator, never overwrite generated pages."""
import argparse,ast,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FILES=['tools/lib/hindi_textbook_hub.py','css/hindi-textbook-hub.css','js/hindi-textbook-hub.js','data/learning/hindi-textbook-catalogue.json']
IMPORT='from lib.hindi_textbook_hub import render_hindi_hub'
OLD='    return "\\n".join(out)'
NEW='    return render_hindi_hub("\\n".join(out), href, ROOT)'
def patch(s):
 if NEW in s and IMPORT in s:return s
 anchor='from lib.hindi_learner_offer import hindi_learner_offer'
 if s.count(anchor)!=1:raise ValueError('Unexpected imports: integrate manually')
 start=s.index('def build_region()');end=s.index('\ndef topic_groups(',start);region=s[start:end]
 if region.count(OLD)!=1:raise ValueError('Unexpected hub renderer; integrate manually')
 s=s[:start]+region.replace(OLD,NEW)+s[end:];s=s.replace(anchor,anchor+'\n'+IMPORT,1);s=s.replace('H1 = "Learn Hindi — everything in one place"','H1 = "Learn Hindi"',1);ast.parse(s);return s
def main():
 p=argparse.ArgumentParser();p.add_argument('repo',type=Path);p.add_argument('--apply',action='store_true');a=p.parse_args();r=a.repo.resolve();g=r/'tools/build-hindi-hub.py'
 try:
  if not (r/'learn/hindi/index.html').is_file():raise ValueError('Hindi hub missing')
  changes={g:patch(g.read_text()).encode()}
  for name in FILES:
   target=r/name;b=(ROOT/name).read_bytes()
   if target.exists() and target.read_bytes()!=b:raise ValueError('Conflicting file: '+name)
   changes[target]=b
  changes={p:b for p,b in changes.items() if not p.exists() or p.read_bytes()!=b}
 except (OSError,ValueError,SyntaxError) as ex:sys.exit('BLOCKED: '+str(ex))
 for p,b in changes.items():
  print(('WRITE ' if a.apply else 'WOULD WRITE ')+str(p.relative_to(r)))
  if a.apply:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 print('Source integration only; run existing build and review generated hub.' if a.apply else 'Read-only preflight.')
if __name__=='__main__':main()

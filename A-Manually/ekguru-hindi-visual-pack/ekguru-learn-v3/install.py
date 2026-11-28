#!/usr/bin/env python3
"""Safe opt-in source integration. Defaults to read-only plan; --apply writes.
Run on the actual Arena branch; refuses unexpected generator structures.
"""
import argparse, ast, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FILES=('tools/lib/learn_catalogue_v3.py','css/learn-catalogue-v3.css','js/learn-catalogue-v3.js','images/learn-catalogue/hindi-book.svg')
IMPORT='from lib.learn_catalogue_v3 import render_catalogue'
OLD_RETURN='    return "\\n".join(out), counts'
NEW_RETURN='    return render_catalogue(indian, world, counts, "\\n".join(out), href), counts'

def patch_generator(s):
    if NEW_RETURN in s and 'from lib.learn_catalogue_v2 import render_catalogue' in s:
        s=s.replace('from lib.learn_catalogue_v2 import render_catalogue',IMPORT,1)
        ast.parse(s)
        return s
    if NEW_RETURN in s:
        if IMPORT not in s: raise ValueError('Existing hook lacks import')
        return s
    if s.count(OLD_RETURN)!=1: raise ValueError('Unexpected generator return; integrate manually, no overwrite')
    anchor='from lib.hindi_learner_offer import hindi_learner_offer'
    if s.count(anchor)!=1: raise ValueError('Unexpected generator imports')
    s=s.replace(anchor,anchor+'\n'+IMPORT,1).replace(OLD_RETURN,NEW_RETURN,1)
    for k,v in [('TITLE','Learn Languages Online for Free'),('H1','Choose a language.'),('KICKER','Learn · Free self-paced materials')]:
        s,n=re.subn(r'^'+k+r' = "[^"\n]*"$',k+' = '+repr(v),s,count=1,flags=re.M)
        if n!=1: raise ValueError('Unexpected '+k+' declaration')
    s,n=re.subn(r'^DESC = \([\s\S]*?\)\n', 'DESC = ("Learn Hindi and other Indian and world languages with free self-paced lessons, practice and worksheets. Choose your language and start learning.")\n',s,count=1,flags=re.M)
    if n!=1: raise ValueError('Unexpected description')
    # These pages already exist but are held. Existing is_indexable guard controls release.
    needle='    ("urdu", "ur", "Urdu", "اردو"),'
    if needle not in s: raise ValueError('Unexpected Indian language registry')
    if '("kannada", "kn"' not in s: s=s.replace(needle,needle+'\n    ("kannada", "kn", "Kannada", "ಕನ್ನಡ"),',1)
    if '("malayalam", "ml"' not in s: s=s.replace(needle,needle+'\n    ("malayalam", "ml", "Malayalam", "മലയാളം"),',1)
    ast.parse(s);return s

def main():
    p=argparse.ArgumentParser();p.add_argument('repo',type=Path);p.add_argument('--apply',action='store_true');a=p.parse_args();repo=a.repo.resolve()
    gen=repo/'tools/build-learn-index.py'
    if not gen.is_file() or not (repo/'learn/index.html').is_file():sys.exit('BLOCKED: expected existing EkGuru layout not found')
    try:
        old=gen.read_text(encoding='utf-8');new=patch_generator(old);changes={gen:new.encode('utf-8')}
        for name in FILES:
            dest=repo/name;content=(ROOT/name).read_bytes()
            if dest.exists() and dest.read_bytes()!=content: raise ValueError('Conflicting existing asset: '+name)
            changes[dest]=content
        changes={p:b for p,b in changes.items() if not p.exists() or p.read_bytes()!=b}
    except (ValueError,OSError,SyntaxError) as exc:sys.exit('BLOCKED: '+str(exc))
    for path in changes:print(('WRITE ' if a.apply else 'WOULD WRITE ')+str(path.relative_to(repo)))
    if a.apply:
        for path,content in changes.items():path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(content)
        print('Source integration complete. Run existing publication pipeline; no generated pages were overwritten.')
    else: print('Read-only plan. Repeat with --apply to integrate.')
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Immutable owner indexing contract; restore only from the SAME original Git object."""
import json, os, re, subprocess, sys
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[2]
BASE='bc8c0bd09e01100fbe04c465748aa417bd905925'
OUT=ROOT/'data/quality/indexing-baseline.json'
SKIP={'.git','node_modules','reports','research','docs','tools','tests','data','templates','Arena latest command  arena'}
class Head(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.noindex=False;self.canonical='';self.feed(s.split('</head>',1)[0])
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='meta' and a.get('name','').lower()=='robots':self.noindex='noindex' in a.get('content','').lower()
  if t=='link' and 'canonical' in a.get('rel','').split():self.canonical=a.get('href','')
def files():
 out=[]
 for d,dirs,names in os.walk(ROOT):
  dirs[:]=[n for n in dirs if n not in SKIP and not n.startswith('.')]
  out += [Path(d)/n for n in names if n.endswith('.html') and not re.fullmatch('google[a-z0-9]+\\.html',n)]
 return sorted(out)
def restore():
 if OUT.exists():raise SystemExit('Contract exists; refusing overwrite/recapture')
 ps=files();refs=''.join(f'{BASE}:{p.relative_to(ROOT).as_posix()}\n' for p in ps)
 raw=subprocess.run(['git','cat-file','--batch'],input=refs.encode(),capture_output=True,check=True,cwd=ROOT).stdout;offset=0;rows={}
 for p in ps:
  end=raw.index(b'\n',offset);header=raw[offset:end].decode();offset=end+1
  if header.endswith(' missing'):continue
  size=int(header.split()[-1]);h=Head(raw[offset:offset+size].decode());offset+=size+1
  rows[p.relative_to(ROOT).as_posix()]={'indexable':not h.noindex,'canonical':h.canonical}
 if len(rows)!=2636 or sum(x['indexable'] for x in rows.values())!=1006:raise SystemExit('STOP: immutable original counts differ')
 data={'base_commit':BASE,'recorded_on':'2026-10-01','owner_decision':'Preserve existing index/noindex and canonical. New pages noindex. No quality quarantine without separate permission.','restoration':'Missing file reconstructed from the SAME immutable original Git object, never from current status.','pages':rows}
 OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');print('Original contract restored: 2636 / 1006')
def check():
 if not OUT.exists():raise SystemExit('FAIL: immutable contract missing')
 data=json.loads(OUT.read_text());errors=[];seen=set()
 if data['base_commit']!=BASE or len(data['pages'])!=2636 or sum(x['indexable'] for x in data['pages'].values())!=1006:errors.append('original contract changed')
 for p in files():
  rel=p.relative_to(ROOT).as_posix();seen.add(rel);h=Head(p.read_text());old=data['pages'].get(rel)
  if old:
   if old['indexable']!=(not h.noindex):errors.append(rel+': unauthorized index change')
   if old['canonical']!=h.canonical:errors.append(rel+': unauthorized canonical change')
  elif not h.noindex:errors.append(rel+': new page must be noindex')
 for rel in data['pages'].keys()-seen:errors.append(rel+': original file removed')
 print('Indexing freeze:', 'FAIL' if errors else 'PASS',f'({len(errors)} violations)')
 for e in errors[:25]:print(e)
 return bool(errors)
if __name__=='__main__':
 if '--restore-original' in sys.argv:restore()
 else:raise SystemExit(check())

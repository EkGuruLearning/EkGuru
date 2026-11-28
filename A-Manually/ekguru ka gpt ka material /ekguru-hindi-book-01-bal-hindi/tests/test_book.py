from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,unittest,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];S=R/'site';B=S/'learn/hindi/kids';M=json.loads((S/'data/learning/hindi-kids-book.json').read_text());C=[c for p in M['phases'] for c in p['chapters']];L=[l for c in C for l in c['lessons']]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  for k in ('href','src'):
   if k in d:self.links.append(d[k])
  if 'id' in d:self.ids.append(d['id'])
class Test(unittest.TestCase):
 def test_counts(self):self.assertEqual((len(C),len(L),len(list(B.rglob('index.html')))),(40,80,165));self.assertEqual(len({l['id'] for l in L}),80)
 def test_letters(self):
  words={w for l in L[:20] for w,_ in l['words']}
  self.assertFalse(set('अआइईउऊऋएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह')-words)
  self.assertFalse(set('अं अँ अः ड़ ढ़ क़ ख़ ग़ ज़ फ़ क्ष त्र ज्ञ श्र'.split())-words)
 def test_links(self):
  for f in B.rglob('index.html'):
   p=Links();p.feed(f.read_text());self.assertEqual(len(p.ids),len(set(p.ids)),str(f));self.assertIn('noindex, follow',f.read_text())
   for u in p.links:
    q=urlsplit(u)
    if q.scheme:continue
    t=(f.parent/unquote(q.path)).resolve() if q.path else f
    if t.is_dir():t=t/'index.html'
    self.assertTrue(t.is_relative_to(S),f'{f}: {u}');self.assertTrue(t.is_file(),f'{f}: {u}')
    if q.fragment:
     a=Links();a.feed(t.read_text());self.assertIn(q.fragment,a.ids,str(t))
 def test_sequence(self):
  import posixpath
  for i,l in enumerate(L[:-1]):
   expected=posixpath.relpath(L[i+1]["path"].rstrip("/"),l["path"].rstrip("/"))+"/"
   self.assertIn(f'class="btn primary" href="{expected}"',(S/l["path"]/"index.html").read_text())
 def test_worksheets(self):
  for c in C:
   t=(S/c['path']/'worksheet/index.html').read_text();self.assertEqual(t.count('class="worksheet-part"'),2);self.assertIn('answer-key',t)
 def test_assets(self):
  assets=list((S/'images/hindi-kids').glob('*.svg'));self.assertEqual(len(assets),93)
  for f in assets:ET.parse(f);self.assertNotIn('<script',f.read_text())
 def test_content(self):
  for l in L:self.assertGreaterEqual(len(l['words']),4);self.assertGreaterEqual(len(l['reading']),2);self.assertTrue(l['q'] and l['a'] and l['activity'] and l['writing'])
  self.assertEqual(len({l['q'] for l in L}),80)
if __name__=='__main__':unittest.main(verbosity=2)

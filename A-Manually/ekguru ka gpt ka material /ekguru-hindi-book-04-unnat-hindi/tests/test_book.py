from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,unittest,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];S=R/'site';B=S/'learn/hindi/advanced';M=json.loads((S/'data/learning/hindi-advanced-book.json').read_text());C=[c for p in M['phases'] for c in p['chapters']];L=[l for c in C for l in c['lessons']]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  for k in ('href','src'):
   if k in d:self.links.append(d[k])
  if 'id' in d:self.ids.append(d['id'])
class Test(unittest.TestCase):
 def test_counts(self):self.assertEqual((len(C),len(L),len(list(B.rglob('index.html')))),(40,80,165));self.assertEqual(len({l['id'] for l in L}),80)
 def test_readings(self):
  self.assertEqual(len(M['extended_readings']),20)
  for n,p in M['extended_readings'].items():
   self.assertGreaterEqual(len(p['text'].split()),30);self.assertEqual(len(p['questions']),3)
   l=C[int(n)-1]['lessons'][1];page=(S/l['path']/'index.html').read_text();self.assertIn('long-reading',page);self.assertIn('पठन-बोध',page)
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
   t=(S/c['path']/'worksheet/index.html').read_text();self.assertEqual(t.count('class="worksheet-part"'),3 if c['n']>=21 else 2);self.assertIn('answer-key',t)
 def test_assets(self):
  assets=list((S/'images').rglob('*.svg'));self.assertEqual(len(assets),141)
  for f in assets:ET.parse(f);self.assertNotIn('<script',f.read_text())
 def test_content(self):
  for l in L:self.assertGreaterEqual(len(l['words']),4);self.assertGreaterEqual(len(l['reading']),2);self.assertTrue(l['q'] and l['a'] and l['activity'] and l['writing'] and l['rule'])
  self.assertEqual(len({l['q'] for l in L}),80); self.assertEqual(len({l['rule'] for l in L}),80)
 def test_labs(self):
  labs=json.loads((R/'source/labs.json').read_text());self.assertEqual(len(labs),56)
  for key,lab in labs.items():
   n,j=map(int,key.split('-'));f=S/C[n-1]['lessons'][j-1]['path']/'index.html';self.assertEqual(f.read_text().count('class="syntax-row"'),len(lab['items']))
   for item in lab['items']: self.assertIn(item['answer'],item['options']);self.assertEqual(len(item['options']),len(set(item['options'])))
 def test_visual_models(self):
  models=json.loads((R/'source/visual-models.json').read_text());self.assertEqual(len(models),21)
  for key,model in models.items():
   n,j=map(int,key.split('-')); page=(S/C[n-1]['lessons'][j-1]['path']/'index.html').read_text();self.assertIn('data-visual-model',page);self.assertEqual(page.count('data-model-choice='),len(model['choices']))
 def test_writing_workspace(self):
  for l in L:
   t=(S/l["path"]/"index.html").read_text();self.assertIn(f'data-writing-workspace="{l["id"]}"',t);self.assertIn("data-save-draft",t);self.assertIn("data-clear-draft",t)
 def test_final(self):
  t=(S/L[-1]['path']/'index.html').read_text();self.assertEqual(t.count('final-question'),10);self.assertIn('rubric',t)
if __name__=='__main__' :unittest.main(verbosity=2)

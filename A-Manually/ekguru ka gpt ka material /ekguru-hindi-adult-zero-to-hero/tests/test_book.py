from pathlib import Path
import unittest,json,subprocess,sys,xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
R=Path(__file__).resolve().parents[1];S=R/'site';B=S/'learn/hindi/older-adults';M=json.loads((S/'data/learning/hindi-adult-book.json').read_text());C=[c for st in M['stages'] for c in st['chapters']]
class Parse(HTMLParser):
 def __init__(self,p):super().__init__();self.links=[];self.ids=[];self.feed(p.read_text())
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id'in a:self.ids.append(a['id'])
  for k in ['href','src']:
   if k in a:self.links.append(a[k])
class Tests(unittest.TestCase):
 def test_counts(self):
  self.assertEqual(len(C),40);self.assertEqual(len(M['stages']),5);self.assertTrue(all(len(s['chapters'])==8 for s in M['stages']));self.assertEqual(len(list(B.rglob('index.html'))),171)
 def test_content(self):
  self.assertEqual(len(set(c['rule'] for c in C)),40);self.assertEqual(len(set(c['task'] for c in C)),40)
  for c in C:self.assertEqual(len(c['phrases']),4);self.assertEqual(len(c['dialogue']),4);self.assertTrue(all(len(t)==3 for t in c['dialogue']+c['phrases']))
 def test_links_and_ids(self):
  for p in B.rglob('index.html'):
   h=Parse(p);self.assertEqual(len(h.ids),len(set(h.ids)),p)
   for l in h.links:
    u=urlsplit(l)
    if u.scheme or u.netloc:continue
    dest=(p.parent/unquote(u.path)).resolve() if u.path else p
    if dest.is_dir():dest/= 'index.html'
    self.assertTrue(dest.is_file(),(p,l,dest));self.assertTrue(dest.is_relative_to(S.resolve()),(p,l))
    if u.fragment:self.assertIn(u.fragment,Parse(dest).ids,(p,l))
 def test_svg(self):
  for p in (S/'images').rglob('*.svg'):self.assertTrue(ET.parse(p).getroot().tag.endswith('svg'),p)
 def test_noindex(self):
  for p in B.rglob('index.html'):self.assertIn('name="robots" content="noindex, follow"',p.read_text())
 def test_stage_sequence(self):
  for i,st in enumerate(M['stages']):
   end=S/st['chapters'][-1]['path']/'lesson-02/index.html'; self.assertIn('../../assessment/',end.read_text())
   self.assertTrue((B/st['id']/'assessment/index.html').is_file())
 def test_script_coverage(self):
  p=(B/'foundation/chapter-02/lesson-01/index.html').read_text();self.assertTrue(all(f'>{x}</b>' in p for x in 'अआइईउऊऋएऐओऔ'))
  p=(B/'foundation/chapter-03/lesson-01/index.html').read_text();self.assertTrue(all(f'>{x}</b>' in p for x in 'कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह'))
  p=(B/'foundation/chapter-05/lesson-01/index.html').read_text();self.assertIn('100 · सौ',p)
 def test_rebuild(self):
  p=B/'index.html';before=p.read_bytes();subprocess.run([sys.executable,str(R/'source/build.py')],check=True,capture_output=True);self.assertEqual(before,p.read_bytes())
if __name__=='__main__':unittest.main()

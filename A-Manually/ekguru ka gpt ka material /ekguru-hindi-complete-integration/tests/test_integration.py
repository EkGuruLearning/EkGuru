from pathlib import Path
from urllib.parse import urlsplit,unquote
from html.parser import HTMLParser
import json,unittest,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];S=R/'site';D=json.loads((S/'data/learning/hindi-unified-index.json').read_text());B=S/'learn/hindi/studio'
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=set()
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for k in ('href','src'):
   if k in a:self.refs.append(a[k])
class Integration(unittest.TestCase):
 def test_counts(self):
  self.assertEqual(D['counts'],dict(chapters=240,lessons=480,worksheets=240,assessments=5));self.assertEqual(len(D['entries']),965);self.assertEqual(len({e['path'] for e in D['entries']}),965);self.assertEqual(len(list((S/'learn/hindi').rglob('index.html'))),998)
 def test_links(self):
  missing=[]
  for f in S.rglob('*.html'):
   p=Parser();p.feed(f.read_text());
   for ref in p.refs:
    u=urlsplit(ref)
    if u.scheme or u.netloc or not u.path:continue
    dest=(S/unquote(u.path.lstrip('/')) if u.path.startswith('/') else f.parent/unquote(u.path)).resolve();dest=dest/'index.html' if dest.is_dir() else dest
    if not dest.is_file():missing.append((str(f.relative_to(S)),ref))
  self.assertFalse(missing,missing[:20])
 def test_cards(self):
  self.assertEqual(len(D['cards']),len({c['id'] for c in D['cards']}));self.assertTrue(all(c['hi'] and c['en'] and (B/c['path']/'index.html').is_file() for c in D['cards']))
 def test_progress(self):
  for b in D['books']:
   for l in (x for x in D['entries'] if x['book']==b['id'] and x['type']=='lesson'):
    self.assertIn(f'data-complete="{l["id"]}"',(B/l['path']/'index.html').read_text())
 def test_art(self):
  for f in (S/'images').rglob('*.svg'):ET.parse(f)
 def test_shared(self):
  self.assertEqual(sum('class="eg-studio-nav"' in f.read_text() for f in S.rglob('*.html')),996)
  self.assertEqual(sum('class="eg-next-book"' in f.read_text() for f in S.rglob('*.html')),4)
 def test_index(self):
  for f in S.rglob('*.html'):self.assertIn('noindex',f.read_text().split('</head>')[0],f)
if __name__=='__main__':unittest.main()

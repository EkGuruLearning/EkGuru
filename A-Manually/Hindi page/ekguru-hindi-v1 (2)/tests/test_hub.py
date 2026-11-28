import sys,unittest,tempfile,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'));sys.path.insert(0,str(R))
from lib.hindi_textbook_hub import render_hindi_hub,inventory,GROUPS
from install import patch
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.r=Path(self.tmp.name);self.data=self.r/'data/learning/hindi-textbook-catalogue.json';self.data.parent.mkdir(parents=True);shutil.copy(R/'data/learning/hindi-textbook-catalogue.json',self.data)
 def tearDown(self):self.tmp.cleanup()
 def page(self,t,title='Lesson'):
  p=self.r/t/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('<title>'+title+'</title>')
 def render(self,old=''):
  return render_hindi_hub(old,lambda t:'/'+t+'/',self.r)
 def test_legacy_inventory(self):
  old=''.join(f'<h2 id="{k}">Section</h2><a href="/fixture/{i}/"><b>Title {i}</b> extra prose</a>' for i,k in enumerate(GROUPS) if k!='ht-chapters');h=self.render(old)
  for i,k in enumerate(GROUPS):
   if k=='ht-chapters':continue
   self.assertIn(f'id="{k}"',h);self.assertIn(f'href="/fixture/{i}/"',h)
  self.assertNotIn('extra prose',h)
 def test_book_status(self):
  self.page('learn/hindi/kids');self.assertNotIn('href="/learn/hindi/kids/"',self.render());data=json.loads(self.data.read_text());data['academic'][0]['status']='published';self.data.write_text(json.dumps(data));self.assertIn('href="/learn/hindi/kids/"',self.render())
 def test_future_book_and_chapter(self):
  data=json.loads(self.data.read_text());data['academic'].append(dict(id='fixture',hi='पाठ',en='Fixture',route='learn/hindi/fixture',status='published'));self.data.write_text(json.dumps(data));self.page('learn/hindi/fixture');self.page('learn/hindi/fixture/phase-01/chapter-1','New Hindi chapter');h=self.render();self.assertIn('6 stages',h);self.assertIn('/learn/hindi/fixture/phase-01/chapter-1/',h)
 def test_discover_foundation(self):
  self.page('learn/hindi/foundation/swar','स्वर — Vowels');h=self.render();self.assertIn('/learn/hindi/foundation/swar/',h);self.assertIn('स्वर',h)
 def test_installer(self):
  src='from lib.hindi_learner_offer import hindi_learner_offer\nH1 = "Learn Hindi — everything in one place"\ndef build_region():\n    out=[]\n    return "\\n".join(out)\ndef topic_groups(a):\n    pass\n';s=patch(src);self.assertEqual(patch(s),s);self.assertIn('return render_hindi_hub',s);self.assertRaises(ValueError,patch,'unrecognized')
if __name__=='__main__':unittest.main()

from pathlib import Path
import sys, unittest, tempfile
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'tools')]
from install import patch_generator
from lib.learn_catalogue_v3 import render_catalogue

class TestCatalogue(unittest.TestCase):
    def test_legacy_source_hook(self):
        old='''from lib.hindi_learner_offer import hindi_learner_offer\nTITLE = "Old"\nH1 = "Old"\nKICKER = "Old"\nDESC = ("Old"\n        " copy")\nINDIAN = [\n    ("urdu", "ur", "Urdu", "اردو"),\n]\ndef build_region():\n    return "\\n".join(out), counts\n'''
        new=patch_generator(old); self.assertIn('render_catalogue(indian, world, counts',new);self.assertIn('"kannada"',new);self.assertEqual(patch_generator(new),new)
    def test_v2_upgrade(self):
        s='from lib.learn_catalogue_v2 import render_catalogue\ndef build_region():\n    return render_catalogue(indian, world, counts, "\\n".join(out), href), counts\n'
        new=patch_generator(s); self.assertIn('from lib.learn_catalogue_v3',new);self.assertEqual(patch_generator(new),new)
    def test_large_catalogue(self):
        rows=[(f'lang-{i}',f'x-{i}',f'Language {i}',f'Script {i}',[],[],[],[]) for i in range(100)]
        h=render_catalogue(rows,[],{},'',lambda t:t+'/')
        self.assertEqual(h.count('data-lc-card '),101);self.assertIn('101 languages',h);self.assertIn('learn/lang-99/',h)
        self.assertEqual(h.count('class="lc-more-languages"'),2)
    def test_reject_unknown(self):
        with self.assertRaises(ValueError):patch_generator('unexpected')
    def test_future_language_and_legacy_links(self):
        rows=[('bengali','bn','Bengali','বাংলা',[],[],[],[]),('kannada','kn','Kannada','ಕನ್ನಡ',[],[],[],[])]
        world=[('fr','French','français','languages/fr/course',[],[],[])]
        h=render_catalogue(rows,world,{},'<a href="./spanish/">Spanish guides</a><a href="javascript:bad()">bad</a>',lambda t:t+'/')
        self.assertIn('3 languages',h);self.assertIn('Kannada',h);self.assertIn('href="./spanish/"',h);self.assertNotIn('javascript:',h);self.assertEqual(h.count('data-lc-card '),4)
        self.assertTrue(all(f'id="{x}"' in h for x in ['li-hindi','li-indian','li-world','li-shared','li-tutors']))
if __name__=='__main__':unittest.main()

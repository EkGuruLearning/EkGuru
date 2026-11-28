import sys,unittest
from pathlib import Path
from html.parser import HTMLParser
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from render import records,main_region
class TestCatalogue(unittest.TestCase):
    def test_counts(self):
        rows=records();self.assertEqual(len(rows),18);self.assertEqual(sum(r[3]=='Indian' for r in rows),8)
    def test_expansion(self):
        rows=records()+[[f'x{i}',f'Test language {i}',f'Test {i}','World',f'/languages/test-{i}/course/','#E6DDFB','#514183'] for i in range(100)]
        result=main_region(rows);self.assertEqual(result.count('class="lang"'),118);self.assertIn('/languages/test-99/course/',result);self.assertIn('110 languages',result)
    def test_single_h1(self):
        self.assertEqual(main_region(records()).count('<h1>'),1)
if __name__=='__main__':unittest.main()

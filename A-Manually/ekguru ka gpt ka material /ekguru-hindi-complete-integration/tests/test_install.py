from pathlib import Path
import tempfile,unittest,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from install import plan
class Install(unittest.TestCase):
 def test_clean(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);h=p/'learn/hindi/index.html';h.parent.mkdir(parents=True);h.write_text('legacy');copies,c,r,s=plan(p);self.assertFalse(c);self.assertFalse(r);self.assertTrue(copies);self.assertTrue(all(d!=h for _,d in copies));self.assertEqual(h.read_text(),'legacy')
 def test_collisions(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);h=p/'learn/hindi/index.html';h.parent.mkdir(parents=True);h.write_text('legacy');q=h.parent/'beginner/index.html';q.parent.mkdir();q.write_text('legacy beginner');self.assertIn('learn/hindi/beginner/index.html',plan(p)[1]);self.assertEqual(plan(p,True)[2],['learn/hindi/beginner/index.html']);f=p/'css/hindi-study-studio.css';f.parent.mkdir();f.write_text('different');self.assertIn('css/hindi-study-studio.css',plan(p,True)[1]);self.assertEqual(q.read_text(),'legacy beginner')
if __name__=='__main__':unittest.main()

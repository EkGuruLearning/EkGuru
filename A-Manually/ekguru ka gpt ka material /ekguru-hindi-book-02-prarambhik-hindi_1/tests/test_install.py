from pathlib import Path
import subprocess, tempfile, unittest, sys, json
P=Path(__file__).resolve().parents[1]
class Install(unittest.TestCase):
 def run_installer(self,r,*args):return subprocess.run([sys.executable,str(P/'install.py'),str(r),*args],capture_output=True,text=True)
 def test_collision_and_staging(self):
  with tempfile.TemporaryDirectory() as t:
   r=Path(t);(r/'learn/hindi/beginner').mkdir(parents=True);(r/'learn/hindi/index.html').write_text('hub');root=r/'learn/hindi/beginner/index.html';root.write_text('legacy content')
   self.assertNotEqual(self.run_installer(r,'--apply').returncode,0);self.assertEqual(root.read_text(),'legacy content');self.assertFalse((root.parent/'phase-01').exists())
   self.assertEqual(self.run_installer(r,'--keep-existing-root').returncode,0);self.assertFalse((root.parent/'phase-01').exists())
   self.assertEqual(self.run_installer(r,'--keep-existing-root','--apply').returncode,0);self.assertEqual(root.read_text(),'legacy content');self.assertTrue((root.parent/'phase-01/chapter-01/lesson-01/index.html').exists())
   other=root.parent/'phase-01/index.html';other.write_text('custom');self.assertNotEqual(self.run_installer(r,'--keep-existing-root','--apply').returncode,0);self.assertEqual(other.read_text(),'custom')
 def test_new_install(self):
  with tempfile.TemporaryDirectory() as t:
   r=Path(t);(r/'learn/hindi').mkdir(parents=True);(r/'learn/hindi/index.html').write_text('hub');self.assertEqual(self.run_installer(r,'--apply').returncode,0);self.assertEqual((r/'learn/hindi/beginner/index.html').read_bytes(),(P/'site/learn/hindi/beginner/index.html').read_bytes())
if __name__=='__main__':unittest.main(verbosity=2)

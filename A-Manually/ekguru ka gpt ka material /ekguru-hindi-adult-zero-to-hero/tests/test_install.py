import unittest,tempfile,subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class Installer(unittest.TestCase):
 def test_install_and_idempotence(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);h=r/'learn/hindi/index.html';h.parent.mkdir(parents=True);h.write_text('existing');reg=r/'data/learning/hindi-textbook-catalogue.json';reg.parent.mkdir(parents=True);reg.write_text(json.dumps({'adult':[{'id':s,'route':'learn/hindi/older-adults/'+s,'status':'planned'} for s in ['foundation','beginner','intermediate','advanced','mastery']]}));before=reg.read_bytes();cmd=[sys.executable,str(R/'install.py'),d];subprocess.run(cmd,check=True,capture_output=True);self.assertEqual(reg.read_bytes(),before);self.assertFalse((h.parent/'older-adults').exists());subprocess.run(cmd+['--apply'],check=True,capture_output=True);self.assertEqual(h.read_text(),'existing');self.assertEqual(len(list((h.parent/'older-adults').rglob('index.html'))),171);self.assertTrue(all(x['status']=='existing' for x in json.loads(reg.read_text())['adult']));subprocess.run(cmd+['--apply'],check=True,capture_output=True)
 def test_collision(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);h=r/'learn/hindi/index.html';h.parent.mkdir(parents=True);h.write_text('existing');p=h.parent/'older-adults/index.html';p.parent.mkdir();p.write_text('legacy');a=subprocess.run([sys.executable,str(R/'install.py'),d,'--apply'],capture_output=True);self.assertNotEqual(a.returncode,0);self.assertEqual(p.read_text(),'legacy');self.assertFalse((r/'css/hindi-adult-reader.css').exists())
if __name__=='__main__':unittest.main()

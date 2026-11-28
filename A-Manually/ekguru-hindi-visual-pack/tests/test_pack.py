import importlib.util, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('installer',Path(__file__).resolve().parents[1]/'install.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
class PackTest(unittest.TestCase):
 def fixture(self,root):
  for name in (p.GEN,p.CSS): (root/name).parent.mkdir(parents=True,exist_ok=True)
  # Minimal fixture matching the inspected generator anchors; not the real checkout.
  (root/p.GEN).write_text('''import os,json\nROOT='.'\nSTYLE="""\n'''+p.OLD_RULE+'''\n""" % {"accent": "#123"}\ndef vcard(dev, rom, en, mt=""):\n    pass\ndef lesson(L,b,lt,rm,emo,kw):\n    if L:\n        b.append('<span class="kw" lang="hi"><i aria-hidden="true">%s</i>%s</span>')\n        x=(e(lt), e(rm), emo, e(kw),)\n        b.append("<h2>What to notice</h2><ul>")\n''')
  (root/p.CSS).write_text(p.OLD_RULE+'\n')
  for chapter in p.GROUPS:
   file=root/f'learn/hindi/foundation/{chapter}/index.html';file.parent.mkdir(parents=True)
   file.write_text(''.join(f'<span class="lt" lang="hi">{r["character"]}</span><span class="rm">a</span><span class="kw" lang="hi"><i aria-hidden="true">x</i>{r["word"]}</span>' for r in p.RECORDS if r['chapter']==chapter)+p.ANCHOR)
 def test_coverage_and_idempotence(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);self.fixture(root);changes=p.build_changes(root)
   self.assertEqual(len(changes),56)
   import ast
   style=next(n for n in ast.parse(changes[p.GEN]).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=="STYLE")
   css=eval(compile(ast.Expression(style.value),"<style>","eval"),{"__builtins__":{}})
   self.assertIn("100%",css)
   self.assertNotIn("100%%",css)
   for f,s in changes.items():
    target=root/f;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(s)
   self.assertEqual(changes,p.build_changes(root))
   self.assertEqual(sum(s.count('class="fd-picture"') for f,s in changes.items() if f.endswith('.html')),49)
 def test_fail_closed(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);self.fixture(root);f=root/'learn/hindi/foundation/swar/index.html';f.write_text('wrong layout');before=f.read_bytes()
   with self.assertRaises(ValueError):p.build_changes(root)
   self.assertEqual(f.read_bytes(),before)
if __name__=='__main__':unittest.main()

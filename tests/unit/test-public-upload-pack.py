#!/usr/bin/env python3
"""The uploaded design packs remain private even when main contains them."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('publicdist', ROOT / 'tools/build-public-dist.py')
publicdist = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publicdist)

class UploadPackTest(unittest.TestCase):
    def test_public_walk_excludes_uploaded_installer_previews_and_tests(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            files = ['index.html', 'images/hindi-textbook/0905.svg', 'Manually',
                     'A-Manually/ekguru-hindi-visual-pack/install.py',
                     'A-Manually/ekguru-hindi-visual-pack/preview.html',
                     'A-Manually/ekguru-hindi-visual-pack/tests/test_pack.py',
                     'A-Manually/Hindi page/preview-standalone.html']
            for name in files:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('fixture', encoding='utf8')
            old = publicdist.ROOT
            try:
                publicdist.ROOT = str(root)
                self.assertEqual(set(publicdist.iter_public()), set(files[:2]))
            finally:
                publicdist.ROOT = old

if __name__ == '__main__':
    unittest.main()

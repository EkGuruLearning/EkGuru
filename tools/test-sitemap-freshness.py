#!/usr/bin/env python3
"""A rebuild must not make unchanged sitemap URLs look newly edited."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('sitemaps', Path(__file__).with_name('build-sitemaps.py'))
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FreshnessTests(unittest.TestCase):
    def test_supplement_preserves_existing_dates_and_does_not_invent_new_ones(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            supplement = root / 'sitemap-published.xml'
            supplement.write_text('<urlset><url><loc>https://ekguru.shop/old/</loc><lastmod>2020-01-02</lastmod></url></urlset>')
            with patch.object(MODULE, 'ROOT', root), patch.object(MODULE, 'eligible_public_urls', return_value={'https://ekguru.shop/old/', 'https://ekguru.shop/new/'}):
                MODULE.rebuild_supplement([])
                once = supplement.read_text()
                self.assertIn('<lastmod>2020-01-02</lastmod>', once)
                self.assertEqual(once.count('<lastmod>'), 1)
                MODULE.rebuild_supplement([])
                self.assertEqual(supplement.read_text(), once)

    def test_index_does_not_stamp_every_child_with_build_date(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            child = root / 'sitemap-core.xml'
            child.write_text('<urlset><url><loc>https://ekguru.shop/</loc></url></urlset>')
            with patch.object(MODULE, 'ROOT', root):
                MODULE.rebuild_index([child])
                once = (root / 'sitemap-index.xml').read_text()
                self.assertNotIn('<lastmod>', once)
                MODULE.rebuild_index([child])
                self.assertEqual((root / 'sitemap-index.xml').read_text(), once)


if __name__ == '__main__':
    unittest.main()

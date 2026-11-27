#!/usr/bin/env python3
"""Regression gate for the exact owner-approved country-phrase consolidation."""
import importlib.util
import json
import re
import unittest
from pathlib import Path
from urllib.parse import urljoin

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from discovery_integrity import Page

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("phrase_merge", ROOT / "tools/build-country-phrases.py")
MERGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MERGE)


class MergeTests(unittest.TestCase):
    def test_approval_is_bounded_and_original_baseline_unchanged(self):
        baseline = json.loads((ROOT / "data/quality/indexing-baseline.json").read_text())
        self.assertEqual(len(baseline["pages"]), 2636)
        self.assertEqual(sum(row["indexable"] for row in baseline["pages"].values()), 1006)
        self.assertEqual(len(MERGE.approved_sources()), 196)
        self.assertTrue(all(source in baseline["owner_approved_new_indexable"] for source in MERGE.approved_sources()))

    def test_every_old_route_is_crawlable_merged_and_ad_free(self):
        for source in MERGE.approved_sources():
            with self.subTest(source=source):
                text = (ROOT / source).read_text()
                self.assertEqual(Page(text).canonicals, [MERGE.TARGET])
                self.assertIn('content="0;url=/learn/hindi/conversation/"', text)
                self.assertIn('http-equiv="refresh"', text)
                self.assertIn('href="/learn/hindi/conversation/"', text)
                self.assertIn('<h1>Hindi daily phrases have moved</h1>', text)
                self.assertNotIn('noindex', text.split('</head>', 1)[0].lower())
                self.assertIn('data-ad-class="UTILITY"', text)
                self.assertNotIn('adsbygoogle.js', text)
                self.assertNotIn('"@type": "FAQPage"', text)
                self.assertNotIn('"@type": "QAPage"', text)
                self.assertEqual(MERGE.strip_ultra(MERGE.consolidate(text, source)), MERGE.strip_ultra(text))
                parent = ROOT / source.split('/')[0] / 'index.html'
                self.assertEqual(Page(parent.read_text()).canonicals, ["https://ekguru.shop/" + parent.relative_to(ROOT).parent.as_posix() + "/"])

    def test_merged_routes_are_not_search_or_sitemap_destinations(self):
        retired = {"https://ekguru.shop/" + source[:-10] for source in MERGE.approved_sources()}
        for sitemap in ROOT.glob('sitemap*.xml'):
            locs = set(re.findall(r'<loc>([^<]+)</loc>', sitemap.read_text()))
            self.assertFalse(locs & retired, sitemap.name)
        index = json.loads((ROOT / 'search-index.json').read_text())
        self.assertFalse({urljoin('https://ekguru.shop/', row['u']) for row in index} & retired)
        self.assertTrue(any(urljoin('https://ekguru.shop/', row['u']) == MERGE.TARGET for row in index))


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
"""Read-only regression for the final eight contextual discovery entry points."""
import importlib.util
import json
from pathlib import Path
import re
import sys
import unittest
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from discovery_integrity import Page as Links
from lib.ultra_content import Page

spec = importlib.util.spec_from_file_location('entries', ROOT / 'tools/build-contextual-entry-links.py')
D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)


class ContextualEntries(unittest.TestCase):
    def test_existing_targets_valid_and_bounded(self):
        D.validate()
        self.assertEqual(len(D.TARGETS), 2)
        self.assertEqual(sum(map(len, D.TARGETS.values())), 8)

    def test_static_links_exist_without_scripts(self):
        for relative, targets in D.TARGETS.items():
            base = 'https://ekguru.shop/' + (relative[:-10] if relative.endswith('index.html') else relative)
            block = D.section(relative)
            self.assertNotIn('<script', block); self.assertNotIn(' hidden', block)
            self.assertNotIn('localStorage', block)
            links = {urljoin(base, ref) for tag, key, ref in Links(block).refs if tag == 'a'}
            self.assertEqual(links, {'https://ekguru.shop/' + target for target, _ in targets})
            self.assertIn(block, (ROOT / relative).read_text())

    def test_idempotence_and_unchanged_search_and_transaction_contract(self):
        for relative in D.TARGETS:
            raw = (ROOT / relative).read_text()
            original = re.sub(re.escape(D.START) + r'[\s\S]*?' + re.escape(D.END) + r'\n?', '', raw)
            changed = D.transformed(original, relative)
            self.assertEqual(changed, D.transformed(changed, relative))
            before, after = Page(original), Page(changed)
            self.assertEqual(before.title, after.title)
            self.assertEqual(before.h1, after.h1)
            self.assertEqual(before.meta, after.meta)
            self.assertEqual(before.canonical, after.canonical)
            self.assertEqual(before.ld, after.ld)
            # The insertion is the only source change; forms/inline code cannot be rewritten.
            restored = re.sub(re.escape(D.START) + r'[\s\S]*?' + re.escape(D.END) + r'\n?', '', changed)
            self.assertEqual(original, restored)

    def test_inventory_records_incoming_paths_for_all_eight_targets(self):
        rows = {p['source_file']: p for p in json.loads((ROOT / 'data/quality/phase2-content-inventory.json').read_text())['pages']}
        for targets in D.TARGETS.values():
            for target, _ in targets:
                row = rows[target + 'index.html']
                self.assertGreaterEqual(row['internal_inlinks'], 1)
                self.assertFalse(row['orphan'])
                self.assertEqual(row['canonical'], row['url'])
                self.assertTrue(row['indexable'])


if __name__ == '__main__':
    unittest.main()

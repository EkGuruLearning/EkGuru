#!/usr/bin/env python3
"""Read-only contextual discovery regressions; no indexing/ranking claims."""
import importlib.util
import json
from pathlib import Path
import re
import runpy
import sys
import unittest
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from discovery_integrity import Page as Links
from lib.ultra_content import Page

spec = importlib.util.spec_from_file_location('phrases', ROOT / 'tools/build-hindi-phrase-discovery.py')
D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)


class PhraseDiscovery(unittest.TestCase):
    def test_grouped_directory_covers_existing_phrase_source_once(self):
        groups = D.targets()
        slugs = [row['slug'] for rows in groups.values() for row in rows]
        source = runpy.run_path(str(ROOT / 'tools/build-say-pages.py'))['PAGES']
        self.assertEqual(len(groups), 5)
        self.assertEqual(len(slugs), 39)
        self.assertEqual(len(slugs), len(set(slugs)))
        self.assertEqual(set(slugs), {row['slug'] for row in source})

    def test_all_targets_are_static_incoming_links_from_hub(self):
        raw = (ROOT / 'ask/index.html').read_text()
        links = {urljoin('https://ekguru.shop/ask/', ref) for tag, key, ref in Links(raw).refs if tag == 'a'}
        for rows in D.targets().values():
            for row in rows:
                self.assertIn('https://ekguru.shop/ask/' + row['slug'] + '/', links)
                self.assertTrue(row['question'])

    def test_insertions_are_idempotent_and_preserve_page_contract(self):
        for relative in ['ask/index.html', 'learn/hindi/conversation/index.html']:
            raw = (ROOT / relative).read_text()
            stripped = re.sub(re.escape(D.START) + r'[\s\S]*?' + re.escape(D.END) + r'\n?', '', raw)
            rendered = D.transformed(stripped, relative)
            self.assertEqual(rendered.count(D.START), 1)
            self.assertEqual(rendered, D.transformed(rendered, relative))
            before, after = Page(stripped), Page(rendered)
            self.assertEqual(after.h1, before.h1)
            self.assertEqual(after.title, before.title)
            self.assertEqual(after.canonical, before.canonical)
            self.assertEqual(after.meta, before.meta)
            self.assertEqual(after.ld, before.ld)
            self.assertFalse(after.noindex)

    def test_contextual_paths_resolve_to_existing_files_and_fragments(self):
        for relative in ['ask/index.html', 'learn/hindi/conversation/index.html']:
            block = D.section(relative, D.targets())
            self.assertNotIn('<script', block)
            self.assertNotIn(' hidden', block)
            url = 'https://ekguru.shop/' + relative[:-10]
            for tag, key, ref in Links(block).refs:
                target = urlsplit(urljoin(url, ref))
                self.assertEqual(target.netloc, 'ekguru.shop')
                path = ROOT / (target.path.lstrip('/') + 'index.html')
                self.assertTrue(path.is_file(), str(path))
                if target.fragment:
                    self.assertIn(target.fragment, Page(path.read_text()).ids)

    def test_legacy_conversation_generator_keeps_course_entry(self):
        source = runpy.run_path(str(ROOT / 'tools/build-hindi-structure.py'))
        rendered, _ = source['render_topic']('conversation', source['TOPIC_META']['conversation'])
        self.assertEqual(rendered.count(D.START), 1)
        self.assertIn('../../../ask/#hindi-phrase-answers', rendered)


if __name__ == '__main__':
    unittest.main()

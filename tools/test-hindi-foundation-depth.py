#!/usr/bin/env python3
"""Read-only authored-depth regressions. No editorial or real-audio approval."""
import copy
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import mock_open, patch
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from lib.ultra_content import Page


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


D = load('depth', 'tools/build-hindi-foundation-depth.py')
DATA = D.content()
CHAPTER = DATA['chapters'][0]
PATH = ROOT / 'learn/hindi/foundation/swar/index.html'


class Elements(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.elements = []; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class DepthTest(unittest.TestCase):
    def test_count_is_authored_prose_only(self):
        self.assertGreaterEqual(D.prose_words(CHAPTER), 3000)
        changed = copy.deepcopy(CHAPTER)
        changed['title'] += ' filler' * 100
        changed['sections'][0]['models'] = [['अ', 'a', 'filler ' * 100]]
        changed['sections'][0]['checks'] = [['filler ' * 100, 'filler ' * 100]]
        self.assertEqual(D.prose_words(CHAPTER), D.prose_words(changed))

    def test_repeated_paragraphs_and_underlength_fail(self):
        for mutate in ('repeat', 'short'):
            broken = copy.deepcopy(DATA)
            if mutate == 'repeat':
                broken['chapters'][0]['sections'][0]['paragraphs'].append(CHAPTER['sections'][0]['paragraphs'][0])
            else:
                broken['chapters'][0]['sections'] = broken['chapters'][0]['sections'][:1]
            with patch.object(D.json, 'loads', return_value=broken):
                with self.assertRaises(ValueError):
                    D.content()

    def test_idempotence_and_preserved_metadata(self):
        raw = PATH.read_text(); new = D.transformed(raw, CHAPTER)
        self.assertEqual(new, D.transformed(new, CHAPTER))
        page = Page(new)
        self.assertEqual(page.canonical, D.BASE + 'swar/')
        self.assertEqual(page.meta['robots'], 'noindex, follow')
        self.assertEqual(page.title, 'Hindi Foundation 1: The vowels — स्वर | EkGuru')
        self.assertEqual(len(page.h1), 1)
        self.assertEqual(new.count('id="fd-mark"'), 1)
        self.assertIn('ekguru.foundation', new)
        for key in ('description', 'og:description', 'twitter:description'):
            self.assertEqual(page.meta[key], CHAPTER['description'])
        schemas = [json.loads(text) for text in page.ld]
        lessons = [node for schema in schemas for node in schema.get('@graph', []) if node.get('@type') == 'LearningResource']
        self.assertEqual(len(lessons), 1)
        self.assertEqual(lessons[0]['description'], CHAPTER['description'])
        self.assertNotIn('FAQPage', str(schemas))

    def test_static_accessible_models_and_links(self):
        block = D.render(CHAPTER); elements = Elements(block).elements
        ids = [a['id'] for _, a in elements if 'id' in a]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertNotIn('<script', block); self.assertNotIn(' hidden', block)
        self.assertEqual(block.count('<details>'), 5)
        buttons = [a for tag, a in elements if tag == 'button']
        expected = [hi for section in CHAPTER['sections'] for hi, _, _ in section.get('models', [])]
        self.assertEqual([a['data-voice-text'] for a in buttons], expected)
        self.assertTrue(all(a.get('data-voice-lang') == 'hi' and a.get('type') == 'button' and a.get('aria-label') for a in buttons))
        for tag, attrs in elements:
            if tag == 'a':
                target = urlsplit(urljoin(D.BASE + 'swar/', attrs['href']))
                self.assertEqual(target.netloc, 'ekguru.shop')
                file = ROOT / (target.path.strip('/') + '/index.html')
                self.assertTrue(file.is_file(), str(file))
                if target.fragment:
                    self.assertIn(target.fragment, Page(file.read_text()).ids)

    def test_legacy_builder_keeps_expansion_without_touching_disk(self):
        builder = load('foundation_builder', 'tools/build-hindi-foundation.py')
        self.assertFalse(builder.validate())
        fake = mock_open()
        with patch('builtins.open', fake), patch.object(builder.os, 'makedirs'):
            builder.lesson_page(builder.C.LESSONS[0], None, builder.C.LESSONS[1], len(builder.C.LESSONS))
        rendered = fake().write.call_args.args[0]
        self.assertEqual(rendered.count(D.START), 1)
        self.assertIn(CHAPTER['sections'][0]['paragraphs'][0], rendered)
        self.assertIn('book-mode.js', rendered)

    def test_ten_chapter_report_is_honest(self):
        report = D.report(DATA, {})
        self.assertEqual(len(report['chapters']), 10)
        self.assertEqual(report['expanded_chapters'], 1)
        self.assertEqual(report['chapters'][0]['added_authored_prose_words'], D.prose_words(CHAPTER))
        self.assertTrue(all(row['status'] == 'pending-expansion' and row['added_authored_prose_words'] == 0 for row in report['chapters'][1:]))
        self.assertEqual(json.loads(D.REPORT.read_text()), report)


if __name__ == '__main__':
    unittest.main()

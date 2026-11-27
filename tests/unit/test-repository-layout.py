#!/usr/bin/env python3
"""Safe cleanup contracts: real test bodies, compatibility and publishing boundary."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('public_layout', ROOT / 'tools/build-public-dist.py')
DEPLOY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DEPLOY)


class RepositoryLayoutTests(unittest.TestCase):
    def test_every_approved_move_has_a_unique_existing_destination(self):
        manifest = json.loads((ROOT / 'docs/architecture/cleanup-path-map.json').read_text())
        self.assertEqual(manifest['baseline_commit'], 'd9aeb63316f780bcc686a65655f09be06c8ea5a3')
        moves = manifest['moves']
        self.assertEqual(len(moves), 197)
        self.assertEqual(len({row['new'] for row in moves}), 197)
        tests = [row for row in moves if row['old'].startswith('tools/test-')]
        self.assertEqual(len(tests), 152)
        for row in moves:
            with self.subTest(path=row['new']):
                self.assertTrue((ROOT / row['new']).is_file())
                if row['compatibility_entrypoint']:
                    wrapper = (ROOT / row['old']).read_text()
                    self.assertIn('Compatibility entrypoint only', wrapper)
                    self.assertIn(row['new'], wrapper)
                else:
                    self.assertFalse((ROOT / row['old']).exists())
        self.assertTrue((ROOT / 'tests/e2e/test-journeys.mjs').is_file())

    def test_new_internal_folders_cannot_enter_real_build(self):
        internal = ['generators', 'integrations', 'config', 'scripts', 'tests',
                    'docs', 'src', 'server', 'apps-script', '_site', '.artifacts']
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'source'
            output = Path(temp) / 'output'
            source.mkdir()
            for directory in internal:
                file = source / directory / 'nested/private.json'
                file.parent.mkdir(parents=True)
                file.write_text('{"sentinel":"must not publish"}')
            public = ['index.html', 'ads.txt', 'robots.txt', 'sitemap.xml', 'CNAME',
                      '.nojekyll', 'sw.js', 'manifest.webmanifest', 'llms.txt',
                      '.well-known/llms.txt', 'js/runtime.js', 'learn/hindi/index.html']
            for relative in public:
                file = source / relative
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text('public fixture')
            with patch.object(DEPLOY, 'ROOT', str(source)):
                self.assertEqual(DEPLOY.build(str(output)), len(public))
            for directory in internal:
                self.assertFalse((output / directory).exists(), directory)
            for relative in public:
                self.assertEqual((output / relative).read_text(), 'public fixture')

    def test_html_links_to_new_internal_roots_are_rejected(self):
        for directory in ['generators', 'integrations', 'config', 'scripts', 'tests', 'docs']:
            self.assertIsNotNone(DEPLOY.PRIVATE_REF.search(f'<script src="/{directory}/private.js"></script>'))
        self.assertIsNone(DEPLOY.PRIVATE_REF.search('<script src="/js/voice.js"></script>'))

    def test_package_and_workflow_test_commands_point_to_existing_files(self):
        import re
        package = json.loads((ROOT / 'package.json').read_text())
        texts = list(package['scripts'].values())
        texts += [p.read_text() for p in (ROOT / '.github/workflows').glob('*.yml')]
        texts.append((ROOT / 'tools/build-all.py').read_text())
        for text in texts:
            for relative in re.findall(r'(?:tests/(?:unit|integration|regression|e2e)|tools)/test-[\w-]+\.(?:mjs|js|py)', text):
                self.assertTrue((ROOT / relative).is_file(), relative)
        self.assertIn('testDir: "tests/e2e"', (ROOT / 'playwright.config.mjs').read_text())


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
"""AdSense identity/placement regressions; never an account approval assertion."""
import importlib.util
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('ads', ROOT / 'tools/inject-ads.py')
ADS = importlib.util.module_from_spec(spec); spec.loader.exec_module(ADS)


class PublisherTags(unittest.TestCase):
    def fixture(self):
        return '<!doctype html><html><head><title>Guide</title>' + ADS.SNIPPET + '</head><body><main>Existing lesson</main></body></html>'

    def test_owner_identifiers_match_config_and_single_root_seller_record(self):
        publisher = ADS.CONFIG['publisher']
        self.assertEqual(publisher['adsense_client'], 'ca-pub-8175326569491671')
        self.assertEqual(publisher['ads_txt_id'], 'pub-8175326569491671')
        records = [line.strip() for line in (ROOT / 'ads.txt').read_text().splitlines() if line.strip() and not line.lstrip().startswith('#')]
        self.assertEqual(records, ['google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0'])

    def test_correct_tags_are_unchanged_and_idempotent(self):
        fixture = self.fixture()
        self.assertTrue(ADS.valid_publisher_tags(fixture))
        first, _ = ADS.apply_policy('index.html', fixture)
        second, what = ADS.apply_policy('index.html', first)
        self.assertEqual(first, second)
        self.assertEqual(what, 'have')

    def test_stale_id_missing_meta_and_wrong_loader_attributes_are_repaired(self):
        good = self.fixture()
        cases = [good.replace(ADS.CLIENT, 'ca-pub-0000000000000000'),
                 re.sub(r'<meta name="google-adsense-account"[^>]*>', '', good),
                 good.replace('crossorigin="anonymous"', 'crossorigin="use-credentials"'),
                 good.replace('<script async src=', '<script src='),
                 good.replace('https://pagead2.googlesyndication.com/', 'https://wrong.example/'),
                 good.replace('<meta name="google-adsense-account" content="' + ADS.CLIENT + '">', '<meta content="wrong-publisher" name="google-adsense-account">')]
        for broken in cases:
            self.assertFalse(ADS.valid_publisher_tags(broken))
            fixed, what = ADS.apply_policy('index.html', broken)
            self.assertEqual(what, 'added')
            self.assertTrue(ADS.valid_publisher_tags(fixed))
            self.assertIn('<main>Existing lesson</main>', fixed)
            self.assertEqual(ADS.apply_policy('index.html', fixed)[0], fixed)

    def test_duplicates_and_tags_outside_head_are_repaired(self):
        good = self.fixture()
        script = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + ADS.CLIENT + '" crossorigin="anonymous"></script>'
        meta = '<meta content="' + ADS.CLIENT + '" name="google-adsense-account">'
        for broken in [good.replace('</body>', script + '</body>'), good.replace('</head>', meta + '</head>'), good.replace('<head><title>Guide</title>', '<head><title>Guide</title></head><body>')]:
            self.assertFalse(ADS.valid_publisher_tags(broken))
        for duplicate in [script, meta]:
            fixed, _ = ADS.apply_policy('index.html', good.replace('</body>', duplicate + '</body>'))
            self.assertTrue(ADS.valid_publisher_tags(fixed))

    def test_exclusions_and_unapproved_runtime_are_not_bypassed(self):
        for path in ['admin.html', 'privacy/index.html', 'join.html', 'learn/hindi/practice/index.html']:
            clean, _ = ADS.apply_policy(path, self.fixture())
            self.assertNotIn('adsbygoogle.js', clean)
            self.assertNotIn('google-adsense-account', clean)
        noindex = self.fixture().replace('<title>', '<meta name="robots" content="noindex, follow"><title>')
        clean, _ = ADS.apply_policy('index.html', noindex)
        self.assertNotIn('adsbygoogle.js', clean)
        self.assertIn('var ADS_RUNTIME_ENABLED = false;', (ROOT / 'js/monetization.js').read_text())

    def test_all_current_policy_eligible_pages_have_one_valid_head_pair(self):
        eligible = 0
        for relative in ADS.pages():
            text = (ROOT / relative).read_text()
            _, allowed, _ = ADS.may_load(relative, text)
            if allowed:
                eligible += 1
                self.assertTrue(ADS.valid_publisher_tags(text), relative)
            else:
                self.assertNotIn('adsbygoogle.js', text, relative)
                self.assertNotIn('google-adsense-account', text, relative)
        self.assertGreater(eligible, 0)
        print(f'Validated exact script/meta identity and head placement on {eligible} eligible pages; exclusions retained.')


if __name__ == '__main__':
    unittest.main()

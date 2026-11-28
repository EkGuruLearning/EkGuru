#!/usr/bin/env python3
"""Static Phase 05 surface checks; no provider calls, production data or mocks."""
import importlib.util
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('student_pages',ROOT/'tools/build-student-pages.py')
pages=importlib.util.module_from_spec(spec);spec.loader.exec_module(pages)

class LMSRoutes(unittest.TestCase):
    def test_routes_noindex_canonical_and_no_ads(self):
        sitemaps=''.join(p.read_text(encoding='utf8') for p in ROOT.glob('sitemap*.xml'))
        for route in pages.PAGES:
            with self.subTest(route=route):
                content=(ROOT/route/'index.html').read_text(encoding='utf8')
                self.assertIn('name="robots" content="noindex, follow"',content)
                self.assertIn('href="https://ekguru.shop/'+route+'"',content)
                self.assertNotIn('https://ekguru.shop/'+route+'<',sitemaps)
                self.assertNotIn('adsbygoogle',content)
                self.assertIn('ekguru:shell-header:start',content)
                self.assertIn('ekguru:shell-footer:start',content)
    def test_assets_svg_safe_and_local(self):
        for p in (ROOT/'images/lms').glob('*.svg'):
            root=ET.parse(p).getroot()
            self.assertEqual(root.tag,'{http://www.w3.org/2000/svg}svg')
            self.assertTrue(root.attrib.get('viewBox'))
            for e in root.iter():
                self.assertNotIn(e.tag.split('}')[-1].lower(),['script','foreignobject','image'])
                for key,value in e.attrib.items():
                    self.assertFalse(key.lower().startswith('on'))
                    if 'href' in key:self.assertTrue(value.startswith('#'))
                    self.assertNotRegex(value,r'https?://')
    def test_unrelated_learning_and_checkout_routes_are_absent(self):
        for route in ('premium/reader/', 'premium/checkout/', 'premium/courses/', 'courses/premium/',
                      'account/courses/', 'account/progress/', 'account/bookmarks/', 'account/results/', 'account/orders/'):
            self.assertFalse((ROOT / route / 'index.html').exists(), route)

    def test_visible_static_interface_has_hindi_mapping(self):
        from html.parser import HTMLParser
        class Text(HTMLParser):
            def __init__(self): super().__init__(); self.values=set()
            def handle_data(self,value):
                if value.strip(): self.values.add(value.strip())
        parser=Text()
        for _,_,body in pages.PAGES.values(): parser.feed(body)
        dictionary=(ROOT/'js/student/i18n.js').read_text(encoding='utf8')
        keys=set(re.findall(r"'([^']+)'\s*:",dictionary))
        missing={text for text in parser.values if text not in keys and re.search(r'[A-Za-z]',text)}
        self.assertEqual(missing,set(),f'Unmapped English interface text: {missing}')
    def test_only_authentication_api_is_configured(self):
        config=(ROOT/'js/student/config.js').read_text()
        self.assertRegex(config,r"workerOrigin:\s*'https://api\.ekguru\.shop'")
        client=(ROOT/'js/student/api.js').read_text()
        self.assertIn("method:'GET',path:'/v1/auth/session'",client)
        self.assertIn("method:'POST',path:'/v1/auth/logout'",client)
        for path in ('/v1/profile', '/v1/dashboard', '/v1/progress', '/v1/courses/'):
            self.assertNotIn(path, client)
        self.assertNotIn('initialiseReader', (ROOT/'js/student/app.js').read_text())

if __name__=='__main__':unittest.main()

#!/usr/bin/env python3
"""Verify actual letter cards, supplied files, generator and airflow fallback."""
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import mock_open,patch
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
spec=importlib.util.spec_from_file_location('foundation',ROOT/'tools/build-hindi-foundation.py')
F=importlib.util.module_from_spec(spec);spec.loader.exec_module(F)
records=json.loads((ROOT/'data/learning/hindi-textbook-illustrations.json').read_text())
class Pictures(HTMLParser):
    def __init__(self):super().__init__();self.pics=[];self.air=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='img' and 'fd-picture' in a.get('class','').split():self.pics.append(a)
        if tag=='details' and 'fd-air-demo' in a.get('class','').split():self.air+=1
class VisualPack(unittest.TestCase):
    def test_manifest_and_assets(self):
        self.assertEqual(len(records),49);self.assertEqual(len({(r['character'],r['word']) for r in records}),49)
        self.assertEqual(len({r['path'] for r in records}),49)
        for r in records:
            self.assertEqual(r['review'],'draft-visual-review-required')
            self.assertTrue(r['path'].startswith('images/hindi-textbook/'))
            root=ET.parse(ROOT/r['path']).getroot();self.assertEqual(root.tag,'{http://www.w3.org/2000/svg}svg')
            for element in root.iter():
                self.assertNotIn(element.tag.split('}')[-1],('script','foreignObject'))
                for key,value in element.attrib.items():
                    self.assertFalse(key.lower().startswith('on'))
                    if key.endswith('href'):self.assertTrue(value.startswith('#'))
    def test_real_chapters_and_generator(self):
        for slug in ('swar','vyanjan-1','vyanjan-2','vyanjan-3'):
            source=(ROOT/f'learn/hindi/foundation/{slug}/index.html').read_text(); page=Pictures();page.feed(source)
            expected=[x for x in records if x['chapter']==slug]
            self.assertEqual(len(page.pics),len(expected));self.assertEqual(page.air,int(slug=='vyanjan-1'))
            for item in expected:
                img=next(x for x in page.pics if x['src']=='/'+item['path'])
                self.assertEqual(img['alt'],'चित्र: '+item['word']);self.assertEqual(img['loading'],'lazy')
            self.assertNotIn('<i aria-hidden="true">',source.split('<div class="fd-letters">')[1].split('</div>\n<h2>',1)[0])
            lesson=next(x for x in F.C.LESSONS if x['slug']==slug); index=F.C.LESSONS.index(lesson)
            fake=mock_open()
            with patch('builtins.open',fake),patch.object(F.os,'makedirs'):
                F.lesson_page(lesson,F.C.LESSONS[index-1] if index else None,F.C.LESSONS[index+1],len(F.C.LESSONS))
            rendered=fake().write.call_args.args[0];generated=Pictures();generated.feed(rendered)
            self.assertEqual([(x['src'],x['alt']) for x in page.pics],[(x['src'],x['alt']) for x in generated.pics])
            self.assertEqual(page.air,generated.air)
            self.assertIn('ekguru.foundation',source);self.assertIn('book-mode.js',source)
    def test_airflow_reduced_motion_and_nasal_accuracy(self):
        css=(ROOT/'css/foundation.css').read_text();self.assertIn('@media(prefers-reduced-motion:reduce)',css);self.assertIn('animation:none',css)
        page=(ROOT/'learn/hindi/foundation/vyanjan-1/index.html').read_text()
        self.assertIn('Illustrative airflow, not an anatomical or measured diagram',page)
        self.assertIn('anusvara, not the written letter ङ',page)
        self.assertNotIn('you will meet them inside words like रंग and ज्ञान',page)
if __name__=='__main__':unittest.main()

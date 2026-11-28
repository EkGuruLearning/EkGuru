#!/usr/bin/env python3
"""No-JS textbook contents for the existing Foundation lessons."""
import importlib.util
from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
spec=importlib.util.spec_from_file_location('reader', ROOT/'tools/build-hindi-textbook-reader.py')
R=importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
class Nav(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.details=0;self.current=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='details':self.details+=1
        if tag=='a':
            self.links.append(a.get('href'))
            if a.get('aria-current')=='page':self.current.append(a.get('href'))
class Reader(unittest.TestCase):
    def test_all_existing_lessons_and_idempotence(self):
        data=R.load(); rows=R.chapter_rows(data); self.assertEqual(len(rows),18)
        for row in rows:
            lesson=row['lesson']; path=ROOT/lesson['url'].strip('/')/'index.html'; raw=path.read_text()
            self.assertEqual(R.transformed(raw,data,lesson['id']),raw)
            self.assertEqual(raw.count(R.START),1);self.assertEqual(raw.count(R.CSS),1)
            self.assertEqual(raw.count('id="fd-mark"'),1);self.assertIn('ekguru.foundation',raw)
            fragment=raw.split(R.START,1)[1].split(R.END,1)[0]; nav=Nav();nav.feed(fragment)
            self.assertEqual(nav.details,1); self.assertEqual(nav.current,[lesson['url']]); self.assertEqual(len(nav.links),21)
            for other in rows: self.assertIn(other['lesson']['url'],nav.links)
            self.assertNotIn('<script',fragment)
    def test_fixture_extends_contents(self):
        data=R.load(); phases=data['textbook']['pathways'][0]['books'][1]['phases']
        phases[1]['chapters'].append({'id':'extra-test','title':'Extra', 'lesson_ids':['academy-vowels'], 'source_url':'/learn/hindi/academy/vowels/', 'status':'existing-draft'})
        rendered=R.render(data,'foundation-swar')
        self.assertIn('/learn/hindi/academy/vowels/',rendered)
        self.assertEqual(rendered.count('aria-current="page"'),1)
if __name__=='__main__':unittest.main()

#!/usr/bin/env python3
"""Exercise registry expansion only in a temporary, non-public site."""
import importlib.util
import json
import sys
import tempfile
import unittest
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from lib import academy_registry as a
spec = importlib.util.spec_from_file_location('sitemap_gate', ROOT/'tools/build-sitemaps.py')
sitemap = importlib.util.module_from_spec(spec); spec.loader.exec_module(sitemap)

class Extensibility(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        for path in ['language','course','chapter','lesson','worksheet','audio']:
            p=self.root/path/'index.html'; p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(f'<html><head><title>{path}</title><meta name="robots" content="index, follow"><link rel="canonical" href="https://ekguru.shop/{path}/"></head><body><main><h1>{path}</h1></main></body></html>')
        with wave.open(str(self.root/'audio'/'fixture.wav'), 'wb') as wav:
            wav.setnchannels(1); wav.setsampwidth(1); wav.setframerate(8000); wav.writeframes(b'\x80' * 80)
        self.data={'version':2,'tracks':[],
          'languages':[{'id':'xx','title':'Example','url':'/language/'}],
          'courses':[{'id':'course','language':'xx','title':'Example course','url':'/course/'}],
          'levels':[{'id':'level','language':'xx','title':'Starter'}],
          'phases':[{'id':'phase','course':'course','level':'level','title':'First phase'}],
          'chapters':[{'id':'chapter','phase':'phase','title':'First chapter','url':'/chapter/'}],
          'lessons':[{'id':'lesson','phase':'phase','chapter':'chapter','title':'Example lesson','url':'/lesson/','topic':'grammar','skills':['reading'],'ages':['all'],'proficiency':'level','goals':['travel'],'audio':'none','worksheet':False}],
          'activities':[], 'resources':[], 'vocabulary':[]}
    def tearDown(self): self.tmp.cleanup()
    def test_fixture_addition_propagates(self):
        data=self.data; a.validate(data,self.root)
        before=a.counts(data); before_html=a.home_html(data, 0)
        # Add a complete new course, phase, chapter, lesson, word, sheet and audio.
        data['courses'].append({'id':'new-course','language':'xx','title':'New course','url':'/course/'})
        data['phases'].append({'id':'new-phase','course':'new-course','level':'level','title':'New phase'})
        data['chapters'].append({'id':'new-chapter','phase':'new-phase','title':'New chapter','url':'/chapter/'})
        data['lessons'].append({'id':'new-lesson','phase':'new-phase','chapter':'new-chapter','title':'New lesson','url':'/lesson/','topic':'vocabulary','skills':['speaking'],'ages':['adults'],'proficiency':'level','goals':['family'],'audio':'none','worksheet':False})
        data['vocabulary'].append({'id':'word','lesson':'new-lesson','hi':'आम','roman':'aam','meaning':'mango','review':'draft'})
        data['resources'] += [{'id':'sheet','lesson':'new-lesson','title':'New worksheet','url':'/worksheet/','kind':'worksheet'}, {'id':'audio','lesson':'new-lesson','title':'Audio exercise','url':'/audio/fixture.wav','kind':'recorded-audio','license':'owner-recorded'}]
        a.validate(data,self.root)
        self.assertEqual(a.counts(data)['lessons'],before['lessons']+1)
        self.assertNotIn('New course',before_html); self.assertIn('New course',a.home_html(data,0))
        self.assertIn('New lesson',a.catalogue_html(data))
        row=next(x for x in json.loads(a.index_json(data,self.root))['lessons'] if x['id']=='new-lesson')
        self.assertEqual((row['course'],row['phase'],row['chapter']),('new-course','new-phase','new-chapter'))
        self.assertTrue(row['publication']['indexable']); self.assertEqual(row['publication']['canonical'], 'https://ekguru.shop/lesson/')
        self.assertIn('mango',row['terms']); self.assertTrue(row['worksheet']); self.assertEqual(row['audio'],'recorded')
        # Navigation is constrained to course, and extends as new lessons are registered.
        self.assertIsNone(a.nav(data,'new-lesson')['next'])
        more=dict(data['lessons'][-1],id='next-lesson',title='Next lesson');data['lessons'].append(more)
        rendered = a.lesson_navigation(data,'new-lesson'); self.assertIn('Next lesson', rendered); self.assertIn('New chapter', rendered); self.assertIn('New worksheet', rendered); self.assertIn('Audio exercise', rendered)
        # The existing sitemap publication gate discovers self-canonical indexable pages.
        old=sitemap.ROOT
        try:
            sitemap.ROOT=self.root; sitemap.rebuild_supplement([])
            result=(self.root/'sitemap-published.xml').read_text()
            self.assertIn('https://ekguru.shop/lesson/', result)
            p=self.root/'lesson/index.html';p.write_text(p.read_text().replace('index, follow','noindex, follow'))
            sitemap.rebuild_supplement([])
            self.assertNotIn('https://ekguru.shop/lesson/',(self.root/'sitemap-published.xml').read_text())
        finally: sitemap.ROOT=old
    def test_rejects_duplicates_missing_urls_and_bad_relations(self):
        self.data['lessons'].append(dict(self.data['lessons'][0]))
        with self.assertRaises(ValueError): a.validate(self.data,self.root)
        self.data['lessons'].pop(); self.data['lessons'][0]['url']='/not-here/'
        with self.assertRaises(ValueError): a.validate(self.data,self.root)
        self.data['lessons'][0]['url']='/lesson/';self.data['lessons'][0]['phase']='missing'
        with self.assertRaises(ValueError): a.validate(self.data,self.root)
        self.data['lessons'][0]['phase']='phase'
        self.data['resources'].append({'id':'bad-audio','lesson':'lesson','title':'Audio','url':'/audio/fixture.wav','kind':'recorded-audio'})
        with self.assertRaises(ValueError): a.validate(self.data,self.root)

if __name__=='__main__': unittest.main()

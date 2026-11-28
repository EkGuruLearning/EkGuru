#!/usr/bin/env python3
"""Validate independent pathways and reject unverified or duplicated lessons."""
import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from lib import academy_registry as registry

class TextbookModel(unittest.TestCase):
    def setUp(self): self.data=json.loads((ROOT/'data/hindi-academy/curriculum.json').read_text(encoding='utf8'))
    def test_graph_and_coverage(self):
        registry.validate(self.data,ROOT)
        paths=self.data['textbook']['pathways']; self.assertEqual([p['id'] for p in paths],['academic','adult'])
        academic,adult=[p['books'] for p in paths]
        self.assertEqual([b['id'] for b in academic],['kids','beginner','intermediate','advanced','mastery'])
        self.assertEqual([b['id'] for b in adult],['adult-foundation','adult-beginner','adult-intermediate','adult-advanced','adult-mastery'])
        self.assertTrue(all(len(b['phases'])==4 for b in academic+adult))
        self.assertEqual([sum(len(p['planned_topics']) for b in group for p in b['phases']) for group in (academic,adult)],[100,100])
        self.assertTrue(all(b['status']=='incomplete' for b in academic+adult))
        lessons=[c['lesson_ids'][0] for p in academic[1]['phases'] for c in p['chapters']]
        self.assertEqual(len(lessons),18); self.assertEqual(len(set(lessons)),18)
        coverage=self.data['character_coverage']['characters']
        self.assertEqual(len(coverage),72); self.assertTrue(all(not c['complete'] for c in coverage))
        self.assertEqual(sum('illustration' in c for c in coverage),49)
        self.assertTrue(all(c['illustration']['review']=='draft-visual-review-required' for c in coverage if 'illustration' in c))
    def test_invalid_graphs_are_rejected(self):
        for mutate in (
            lambda d:d['textbook']['pathways'][0]['books'][0].update(planned_url='/learn/hindi/../bad/'),
            lambda d:d['textbook']['pathways'][0]['books'][0]['phases'][1].update(id=d['textbook']['pathways'][0]['books'][0]['phases'][0]['id']),
            lambda d:d['textbook']['pathways'][0]['books'][1]['phases'][0]['chapters'][0].update(lesson_ids=['unknown']),
            lambda d:d['textbook']['pathways'][0]['books'][1]['phases'][0]['chapters'][0].update(source_url='/not-its-source/'),
            lambda d:d['textbook']['pathways'][0]['books'][0].update(status='complete'),
            lambda d:d['textbook']['pathways'][1]['books'][0].update(prerequisite_book_ids=['mastery']),
            lambda d:d['textbook']['pathways'][1]['books'][0]['phases'][0]['chapters'].append(dict(d['textbook']['pathways'][0]['books'][1]['phases'][0]['chapters'][0],id='duplicate-lesson')),
            lambda d:d['textbook']['pathways'][0]['books'][0]['phases'][0]['planned_topics'][0].update(status='complete'),
            lambda d:d['character_coverage']['characters'].pop(),
            lambda d:d['character_coverage']['characters'][0].update(complete=True),
            lambda d:d['character_coverage']['characters'][0]['illustration'].update(path='images/missing.svg'),
        ):
            data=copy.deepcopy(self.data); mutate(data)
            with self.assertRaises(ValueError): registry.validate(data,ROOT)
    def test_fixture_addition_uses_distinct_lesson(self):
        phase=self.data['textbook']['pathways'][0]['books'][1]['phases'][1]
        chapter={'id':'test-extra-chapter','title':'Fixture chapter', 'lesson_ids':['academy-vowels'],'source_url':'/learn/hindi/academy/vowels/','status':'existing-draft'}
        phase['chapters'].append(chapter);registry.validate(self.data,ROOT)
        self.assertEqual(len(phase['chapters']),1)
        self.assertEqual(len([x for x in self.data['lessons'] if x['id']=='academy-vowels']),1)

if __name__=='__main__':unittest.main()

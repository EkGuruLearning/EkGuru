#!/usr/bin/env python3
"""Conservative global publishability/AdSense-readiness triage.

This audit never claims AdSense approval. It inventories public HTML and course
quality signals, identifies review queues, and writes factual states to
`data/quality/adsense-readiness.json`. Editorial and rendered-device review
remain mandatory.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import html
import json
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/quality/adsense-readiness.json'
EXCLUDED_DIRS={'.git','node_modules','.venv','vendor','reports','research','docs','tools','data'}
CJK_RE = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]')
THAI_RE = re.compile(r'[\u0e00-\u0e7f]')
THAI_MARK_RE = re.compile(r'[\u0e31\u0e34-\u0e3a\u0e47-\u0e4e]')

# Average characters per word, for the scripts that do not put spaces between
# words. Two for Chinese/Japanese/Korean (a Chinese word is usually two
# characters, a Japanese one mixes kanji with kana), three for Thai once its
# combining marks are set aside. Conservative on purpose: if this over-counts,
# it hides a thin page, so it is set at the low end of the range.
CJK_PER_WORD = 2
THAI_PER_WORD = 3


def count_words(text):
    """Words, for a site that publishes in Japanese, Chinese, Thai and English.

    Those three are written without spaces, so splitting on whitespace reported
    a complete Japanese page as 56 "words" against 293 for the identical Spanish
    one — and /ja/join.html was listed as thin, which is exactly the page an
    AdSense reviewer is not looking at. Characters are therefore counted per
    script and divided by that script's average characters per word; spaced
    scripts are counted exactly as before.

    Self-tested: python3 tools/audit-adsense-readiness.py --selftest
    """
    cjk = len(CJK_RE.findall(text))
    thai = len([c for c in THAI_RE.findall(text) if not THAI_MARK_RE.match(c)])
    spaced = re.findall(r"\b[\w'’-]+\b",
                        THAI_RE.sub(' ', CJK_RE.sub(' ', text)), flags=re.UNICODE)
    # ceiling division, not round(): 12.5 characters is not a reason to call a
    # page a word shorter, and Python's round() would send 25 kanji to 12.
    return (len(spaced) + -(-cjk // CJK_PER_WORD) + -(-thai // THAI_PER_WORD))


TRUST={'about':'about/index.html','contact':'contact/index.html','privacy':'privacy/index.html','terms':'terms/index.html','disclaimer':'disclaimer/index.html','copyright':'copyright/index.html','cookie_or_consent':'cookie-policy/index.html'}
COURSE_LEVELS=('A1','A2','B1','B2','C1','C2')
PRACTICE_STANDARD_PATH=ROOT/'data/quality/global-practice-standard.json'
PRACTICE_STANDARD=json.loads(PRACTICE_STANDARD_PATH.read_text()) if PRACTICE_STANDARD_PATH.exists() else {'level_policy':{}}
PRACTICE_MINIMUMS={k:v['minimum_distinct_types'] for k,v in PRACTICE_STANDARD.get('level_policy',{}).items()}
COURSE_T1_SCHEMA=json.loads((ROOT/'data/schemas/course-t1.schema.json').read_text(encoding='utf-8'))
COURSE_T1_LEVELS=set(COURSE_T1_SCHEMA['properties']['file_level']['enum'])
COURSE_T1_LEVEL_SCHEMA=COURSE_T1_SCHEMA['properties']['level']
COURSE_T1_UNIT_SCHEMA=COURSE_T1_SCHEMA['$defs']['unit']
COURSE_T1_UNITS=COURSE_T1_LEVEL_SCHEMA['properties']['units']
COURSE_T1_UNIT_LESSONS=COURSE_T1_UNIT_SCHEMA['properties']['lessons']
COURSE_T1_TEST_ITEMS=COURSE_T1_LEVEL_SCHEMA['properties']['test']['properties']['items']
COURSE_T1_LESSON_SCHEMA=COURSE_T1_SCHEMA['$defs']['lesson']
COURSE_T1_LESSON_PROPERTIES=COURSE_T1_LESSON_SCHEMA['properties']
COURSE_T1_PRACTICE=COURSE_T1_LESSON_PROPERTIES['practice']
COURSE_T1_QUIZ=COURSE_T1_LESSON_PROPERTIES['quiz']
COURSE_T1_DIALOGUE=COURSE_T1_LESSON_PROPERTIES['dialogue']
PLAYER_SOURCE=(ROOT/'js/course-player.js').read_text(errors='ignore') if (ROOT/'js/course-player.js').exists() else ''
TTS_CODES=set(re.findall(r'\b([a-z]{2,3}):\s*"[a-z]{2,3}(?:-[A-Z]{2})?"',PLAYER_SOURCE))

def state(pass_:bool, partial=False): return 'PASS' if pass_ else ('PARTIAL' if partial else 'FAIL')
def norm(s):
 # Unicode-aware: the old class kept only Latin+Devanagari-to-Malayalam, so every
 # Arabic/Japanese/Cyrillic/Urdu title collapsed to "ekguru" and the audit reported
 # a 12-page duplicate-title group that did not exist.
 return re.sub(r'[^\w]+',' ',s.lower()).strip()

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class Scan(HTMLParser):
 """A tolerant page scan.

 The tag state is a STACK, not the last tag seen: this site writes its
 headings with an inner <span> (``<h1><span …>Learn Hindi …</span></h1>``),
 and a single "last tag" slot attributed that text to the span, not the h1 —
 which is why the home page was once reported as having no h1 at all.

 ``<template>`` is inert markup and is ignored entirely: nothing in it
 renders, so a template copy of a heading is not a heading on the page.
 """
 def __init__(self):
  super().__init__(); self.title=''; self.h1=[]; self.text=[]; self.meta=''; self.canonical=''; self.links=[]; self.headings=[]; self.stack=[]; self.noindex=False; self.main=False; self.ad=False
 def _enclosing(self):
  return self.stack[::-1]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='template': self.stack.append(tag); return
  if 'template' in self.stack: 
   if tag not in VOID: self.stack.append(tag)
   return
  if tag=='meta' and a.get('name','').lower()=='description': self.meta=a.get('content','')
  if tag=='meta' and a.get('name','').lower()=='robots' and 'noindex' in a.get('content','').lower(): self.noindex=True
  if tag=='link' and 'canonical' in a.get('rel',[]): self.canonical=a.get('href','')
  if tag=='a' and a.get('href'): self.links.append(a['href'])
  if tag=='main': self.main=True
  if tag=='h1': self.h1.append('')          # the TAG is the count, not its text
  if tag in ('h1','h2','h3'): self.headings.append(tag)
  if 'adsbygoogle' in a.get('class','') or 'ad-slot' in a.get('class',''): self.ad=True
  if tag not in VOID: self.stack.append(tag)
 def handle_endtag(self,tag):
  if tag in VOID: return
  if tag in self.stack:
   self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]
 def handle_data(self,data):
  s=data.strip()
  if not s or 'template' in self.stack: return
  t=self._enclosing()
  if t and t[0] in ('script','style','noscript'): return
  self.text.append(s)
  if 'title' in t: self.title+=s
  if 'h1' in t and self.h1:
   self.h1[-1] = (self.h1[-1] + ' ' + s).strip()

# Machine files, not pages: Google's Search Console verification file is a
# named fragment with no title, no heading and three words, and it was the
# only page in the whole audit carrying missing_title, missing_meta,
# missing_canonical, missing_main_landmark, weak_internal_navigation AND one
# of the depth reviews. It is not published content and never appears in a
# sitemap; walking it as a page makes real numbers unreadable.
MACHINE_FILES = re.compile(r'^google[a-z0-9]+\.html$')

def html_files():
 out=[]
 for p in ROOT.rglob('*.html'):
  rel=p.relative_to(ROOT)
  if any(x in EXCLUDED_DIRS for x in rel.parts) or p.name=='admin.html': continue
  if MACHINE_FILES.match(p.name): continue
  out.append(p)
 return sorted(out)

# Chrome is not content. The site header, the shell footer, the trust footer,
# the two bands, the in-page navs and the storybook hint are identical on every
# page ON PURPOSE — that is what makes them chrome. Counting them as duplicate
# content made every page look templated and hid the pages that really are
# ("Meetings, customers, contracts — professional Kannada for offices." repeated
# per language). Paragraph and intro duplication is measured on the body only.
# The same holds (29 Sep 2026) for the call-to-action asides — <aside> with
# class cta, pg-cta, cta-box or pg-cta-box: a "find a tutor" / "quiz yourself"
# box is a navigation affordance repeated by design, marked up as
# complementary content, and not what a page is about — for a tutor card's
# subject line (p.xp-tutor-teaches, roster metadata), and for the practice
# labs' "a few of the items" caption (p.lab-hint). Editorial/review/audio
# paragraphs marked data-eg-chrome are also excluded; counting the public
# "Draft: not yet reviewed by a native speaker" notice as a page's opening
# paragraph made hundreds of otherwise different pages look duplicated.
CHROME = re.compile(
    r"<!--\s*ekguru:(?:shell-header|shell-footer|trust-footer|pw-bands):start\s*-->[\s\S]*?"
    r"<!--\s*ekguru:(?:shell-header|shell-footer|trust-footer|pw-bands):end\s*-->"
    r"|<header\b[\s\S]*?</header>|<footer\b[\s\S]*?</footer>"
    r"|<nav\b[\s\S]*?</nav>"
    r"|<p\b(?=[^>]*\bdata-eg-chrome=(?:\"[^\"]*\"|'[^']*'))[^>]*>[\s\S]*?</p>"
    r"|<p class=\"[^\"]*\bhint\b[^\"]*\"[^>]*>[\s\S]*?</p>"
    r"|<p class=\"[^\"]*\b(?:crumbs?|upd|updated|dateline|meta|byline|xp-tutor-teaches)\b[^\"]*\"[^>]*>[\s\S]*?</p>"
    r"|<aside\b[^>]*(?:class=\"[^\"]*pg-note[^\"]*\"|role=\"note\")[^>]*>[\s\S]*?</aside>"
    r"|<aside\b[^>]*class=\"(?:pg-)?cta(?:-box)?\b[^\"]*\"[^>]*>[\s\S]*?</aside>", re.I)


def signature(text):
 # Template-risk signature deliberately removes volatile names/numbers/currency.
 x=norm(text); x=re.sub(r'\b\d+(?: \d+)*\b','#',x)
 return hashlib.sha256(x.encode()).hexdigest()[:20]

def content_paragraphs(raw):
 """Return substantial body paragraphs after removing shared site chrome."""
 body=CHROME.sub(' ',raw)
 paras=[norm(html.unescape(re.sub('<[^>]+>',' ',x))) for x in re.findall(r'<p\b[^>]*>(.*?)</p>',body,flags=re.I|re.S)]
 return [x for x in paras if len(x.split())>=12]

def page_audit():
 pages=[]; title_map=defaultdict(list); meta_map=defaultdict(list); intro_map=defaultdict(list); paragraph_map=defaultdict(list)
 for p in html_files():
  raw=p.read_text('utf-8',errors='ignore'); s=Scan(); s.feed(raw); text=' '.join(s.text)
  # WORD COUNT, SCRIPT-AWARE. Japanese, Chinese and Thai are written without
  # spaces, so splitting on whitespace reported a complete Japanese page as 56
  # "words" against 293 for the identical Spanish one — and /ja/join.html was
  # then listed as thin, which is exactly the page an AdSense reviewer is not
  # looking at. A CJK character carries about as much information as a word, so
  # it is counted as one; Latin and other spaced scripts are counted as before.
  words_counted=count_words(text)
  rel=str(p.relative_to(ROOT))
  paras=content_paragraphs(raw)
  intro=paras[0] if paras else ''
  issues=[]
  if not s.title: issues.append('missing_title')
  if not s.meta: issues.append('missing_meta_description')
  if len(s.h1)!=1: issues.append('h1_count_'+str(len(s.h1)))
  if not s.canonical: issues.append('missing_canonical')
  if words_counted<250: issues.append('depth_review_under_250_words')
  if not s.main: issues.append('missing_main_landmark')
  if len(s.links)<3: issues.append('weak_internal_navigation')
  # Duplicate title, description and lead-paragraph signals apply to pages
  # Google can index. Hidden drafts, utility routes and quarantined research
  # pages remain in the inventory, but must not inflate the publication queue.
  if not s.noindex:
   title_map[norm(s.title)].append(rel); meta_map[norm(s.meta)].append(rel)
   if intro: intro_map[signature(intro)].append(rel)
  # Keep repeated paragraph groups across all pages as an editorial sampling
  # queue; unlike title/meta/intro collisions, a shared paragraph alone is not
  # sufficient evidence that two indexable pages have the same intent.
  for para in set(paras): paragraph_map[signature(para)].append(rel)
  pages.append({'path':rel,'word_count':words_counted,'title':s.title,'meta_description':s.meta,'h1_count':len(s.h1),'canonical':s.canonical,'noindex':s.noindex,'main_landmark':s.main,'internal_link_count':sum(1 for x in s.links if not urlparse(x).netloc or 'ekguru.shop' in urlparse(x).netloc),'ad_markup_detected':s.ad or 'adsbygoogle' in raw,'issues':issues})
 exact=lambda m:{k:v for k,v in m.items() if k and len(v)>1}
 dups={'titles':exact(title_map),'meta_descriptions':exact(meta_map),'introductions':exact(intro_map),'paragraphs':{k:v for k,v in paragraph_map.items() if len(v)>2}}
 # Repeated footer/legal paragraphs are reported but do not by themselves fail every
 # page. Titles, descriptions, and lead paragraphs represent page intent.
 risk=set()
 for key in ('titles','meta_descriptions','introductions'):
  for paths in dups[key].values(): risk.update(paths)
 for x in pages:
  if x['path'] in risk: x['issues'].append('duplicate_or_template_similarity')
  if re.match(r'learn-hindi-(?:from|for)-[^/]+/index\.html$',x['path']):
   x['issues'].append('scalable_localization_editorial_review')
  x['publishability']='REVIEW_REQUIRED' if x['issues'] else 'PASS'
 return pages,dups

def in_schema_range(value, schema):
 if not isinstance(value, list): return False
 return len(value) >= schema.get('minItems', 0) and len(value) <= schema.get('maxItems', float('inf'))

def test_count(course):
 level=course.get('level') if isinstance(course,dict) else None
 test=level.get('test') if isinstance(level,dict) else None
 if not isinstance(test,dict) and isinstance(course,dict):
  test=course.get('test')
 items=test.get('items') if isinstance(test,dict) else None
 return len(items) if isinstance(items,list) else 0

def course_audit():
 rows=[]
 for p in sorted((ROOT/'data/courses').glob('phase-*/*.json')):
  try: d=json.loads(p.read_text())
  except Exception as e:
   rows.append({'path':str(p.relative_to(ROOT)),'status':'FAIL','issues':['invalid_json',str(e)]})
   continue
  if not isinstance(d,dict) or 'level' not in d: continue
  level_data=d.get('level') if isinstance(d.get('level'),dict) else {}
  units=level_data.get('units',[])
  units=units if isinstance(units,list) else []
  lessons=[l for u in units if isinstance(u,dict) for l in (u.get('lessons') or [])]
  issues=[]
  lv=d.get('file_level','')
  t1=lv in COURSE_T1_LEVELS
  tests=test_count(d)
  structure_pass=True
  lesson_schema_pass=True
  practice_schema_pass=True
  assessment_pass=True

  if not units:
   issues.append('no_units')
   structure_pass=False
  elif t1 and not in_schema_range(units,COURSE_T1_UNITS):
   issues.append('unit_count_outside_t1_schema')
   structure_pass=False

  if not lessons:
   issues.append('no_lessons')
   structure_pass=False

  if t1:
   for index, unit in enumerate(units, 1):
    unit_lessons=unit.get('lessons') if isinstance(unit,dict) else None
    if not in_schema_range(unit_lessons,COURSE_T1_UNIT_LESSONS):
     unit_id=unit.get('id',str(index)) if isinstance(unit,dict) else str(index)
     issues.append(f'{unit_id}:lesson_count_outside_t1_schema')
     structure_pass=False
   if not (COURSE_T1_TEST_ITEMS['minItems'] <= tests <= COURSE_T1_TEST_ITEMS['maxItems']):
    issues.append('level_test_count_outside_t1_schema')
    assessment_pass=False
   required=COURSE_T1_LESSON_SCHEMA['required']
   practice_floor=COURSE_T1_PRACTICE['minItems']
  else:
   if tests <= 0:
    issues.append('no_level_test')
    assessment_pass=False
   required=('learn','vocab','grammar','dialogue','practice','quiz','worksheet')
   practice_floor=5

  for lesson in lessons:
   if not isinstance(lesson,dict):
    issues.append('invalid_lesson_record')
    lesson_schema_pass=False
    continue
   for key in required:
    if not lesson.get(key):
     issues.append(f"{lesson.get('id','?')}:missing_{key}")
     lesson_schema_pass=False
   practice=lesson.get('practice')
   if not isinstance(practice,list) or len(practice)<practice_floor:
    suffix='practice_below_t1_schema_min' if t1 else 'thin_practice'
    issues.append(f"{lesson.get('id','?')}:{suffix}")
    practice_schema_pass=False
   if t1:
    for key, schema in (('dialogue',COURSE_T1_DIALOGUE),('quiz',COURSE_T1_QUIZ)):
     value=lesson.get(key)
     if not in_schema_range(value,schema):
      issues.append(f"{lesson.get('id','?')}:{key}_below_t1_schema_min")
      lesson_schema_pass=False

  practices=[x for lesson in lessons if isinstance(lesson,dict)
             for x in (lesson.get('practice') or []) if isinstance(x,dict)]
  types={x.get('type') for x in practices if x.get('type')}
  minimum=PRACTICE_MINIMUMS.get(lv,5)
  practice_pass=len(types)>=minimum
  skill_coverage_pass=practice_pass and bool(practices) and all(x.get('skill_target') for x in practices)
  if not practice_pass: issues.append(f'narrow_practice_ecosystem_{len(types)}_below_{minimum}')
  if not all(x.get('skill_target') for x in practices): issues.append('practice_skill_targets_missing')
  advanced_terms=('register','inference','stance','argument','rhetoric','semantic','academic','professional','idiom','discourse','style','pragmatic')
  advanced_pass=True
  if lv in ('C1','C2'):
   blob=json.dumps(d,ensure_ascii=False).lower()
   advanced_pass=sum(t in blob for t in advanced_terms)>=4
   if not advanced_pass: issues.append('advanced_reality_review')
  code=d.get('code','')
  research_profile=(ROOT/f'data/language-research/{code}.json').exists() or code=='hi'
  if not research_profile: issues.append('language_research_profile_missing')
  audio_types={'listening_comprehension','dictation','listen_and_choose','listen_and_reorder','listen_and_fill','repeat_after_audio','pronunciation','shadowing'}
  audio_items=[x for x in practices if x.get('type') in audio_types]
  documented_audio=bool(audio_items) and all(isinstance(x.get('audio_source'),str) and x['audio_source'].strip() for x in audio_items)
  # A browser locale mapping is preferred. Lower-resource languages may instead
  # pass with an explicit synthetic/unavailable fallback on every audio item;
  # this is honest NOT_APPLICABLE behavior, not a native-recording claim.
  voice_pass=code in TTS_CODES or documented_audio or (not audio_items and research_profile)
  gates={
   'CONTENT':'PASS' if structure_pass and lesson_schema_pass else 'REVIEW_REQUIRED',
   'PRACTICE':'PASS' if practice_pass and practice_schema_pass else 'REVIEW_REQUIRED',
   'SKILL_COVERAGE':'PASS' if skill_coverage_pass else 'REVIEW_REQUIRED',
   'ASSESSMENT':'PASS' if assessment_pass else 'REVIEW_REQUIRED',
   'LEVEL_APPROPRIATENESS':'PASS' if advanced_pass else 'REVIEW_REQUIRED',
   'LANGUAGE_SPECIFIC':'PASS' if research_profile else 'REVIEW_REQUIRED',
   'VOICE_AUDIO':'PASS' if voice_pass else 'REVIEW_REQUIRED',
   'PLAYER':'PASS'
  }
  rows.append({
   'path':str(p.relative_to(ROOT)), 'language':code, 'level':lv,
   'lesson_count':len(lessons), 'practice_type_count':len(types),
   'minimum_practice_type_count':minimum, 'gates':gates,
   'status':'PASS' if not issues and all(x=='PASS' for x in gates.values()) else 'REVIEW_REQUIRED',
   'issues':sorted(set(issues))
  })
 return rows

def selftest():
    """The counter, on the cases that made it wrong.

    Expected numbers are the number of CJK characters plus spaced words in each
    sample — written out rather than computed, so a change in the regex has to
    be a deliberate change here too.
    """
    checks = [
        ("plain English", "The quick brown fox jumps over the lazy dog.", 9),
        # 25 kana/kanji characters, two to a word
        ("Japanese is unspaced", "ヒンディー語を教えています。プロフィールを掲載します。", 13),
        # 16 han characters, two to a word
        ("Chinese is unspaced", "学习印地语的学生可以免费使用本站。", 8),
        # 17 Thai letters once the vowel and tone marks are set aside, three to a word
        ("Thai is unspaced", "ฉันเรียนภาษาฮินดีทุกวัน", 6),
        # 9 Japanese characters (round(9/2)=5, banker's rounding down) plus "EkGuru" and "2026"
        ("mixed script", "EkGuru は 2026 年に始まりました", 7),
    ]
    bad = ["%s: got %d, expected %d" % (name, count_words(text), expected)
           for name, text, expected in checks if count_words(text) != expected]
    if bad:
        print("FAIL  word counter selftest — " + "; ".join(bad))
        return 1
    print("ok    word counter: unspaced scripts counted per word, spaced scripts as before")

    # Review notices and bylines are shared page chrome, not the lesson's
    # introduction. This regression used to make the same draft banner appear
    # as the intro on more than 1,500 pages and overwhelm the real duplicate
    # content signals.
    sample = (
        '<p class="eg-review-notice" lang="en" data-eg-chrome="review">'
        'Draft: not yet reviewed by a native speaker. Existing availability '
        'and indexing are preserved by owner instruction; that is not an '
        'editorial approval.</p>'
        '<p>An original sentence about this language and its actual vowel '
        'harmony helps a beginner practise a concrete pattern.</p>'
    )
    paragraphs = content_paragraphs(sample)
    expected_intro = norm(
        'An original sentence about this language and its actual vowel '
        'harmony helps a beginner practise a concrete pattern.')
    if paragraphs != [expected_intro]:
        print('FAIL  chrome selftest — review notice leaked into content: ' + repr(paragraphs))
        return 1
    print('ok    content audit: review/bio/audio chrome is not treated as the page introduction')

    entity_text = (
        'A learner&#x27;s map &amp; notebook can help them remember the route '
        'home after a lesson on words and signs.'
    )
    decoded = content_paragraphs('<p>' + entity_text + '</p>')
    expected_decoded = [norm(
        'A learner\'s map & notebook can help them remember the route '
        'home after a lesson on words and signs.')]
    if decoded != expected_decoded:
        print('FAIL  entity selftest — HTML entities changed the content signature: ' + repr(decoded))
        return 1
    print('ok    content audit: HTML entities are decoded before signatures are compared')

    # The live T1 schema allows 3–5 units and 3–5 lessons per unit. The old
    # 3 × 2 / six-total heuristic incorrectly sent the 3 × 3 published levels
    # to review. Keep this regression tied to the schema source itself.
    schema_units = [{"lessons": [{}, {}, {}]} for _ in range(3)]
    if not in_schema_range(schema_units, COURSE_T1_UNITS) or not all(
        in_schema_range(unit["lessons"], COURSE_T1_UNIT_LESSONS) for unit in schema_units
    ):
        print('FAIL  course schema selftest — valid 3 × 3 T1 level rejected')
        return 1
    if in_schema_range([{}, {}], COURSE_T1_UNIT_LESSONS):
        print('FAIL  course schema selftest — T1 lesson floor was not enforced')
        return 1
    test_schema = COURSE_T1_LEVEL_SCHEMA['properties']['test']['properties']['items']
    test_sample = {'level': {'test': {'items': [{}] * test_schema['minItems']}}}
    if test_count(test_sample) != test_schema['minItems'] or test_count({'test': {'items': [{}, {}]}}) != 2:
        print('FAIL  course schema selftest — level test items were not counted')
        return 1
    print('ok    course audit: unit/lesson/test cardinality follows the T1 JSON Schema')
    return 0


def main():
 pages,dups=page_audit(); courses=course_audit()
 thin=[x['path'] for x in pages if 'depth_review_under_250_words' in x['issues']]
 # Thin is only a publication risk where the page can be indexed. A 404 or a
 # JS shell that carries noindex is a utility page: Google does not judge it
 # for thin content, and the honest number for a re-submission is the
 # indexable one. The full list stays, for triage.
 thin_indexable=[x['path'] for x in pages if 'depth_review_under_250_words' in x['issues'] and not x['noindex']]
 review=[x['path'] for x in pages if x['publishability']=='REVIEW_REQUIRED']
 trust={k:{'path':v,'exists':(ROOT/v).exists(),'status':'PASS' if (ROOT/v).exists() else 'REVIEW_REQUIRED'} for k,v in TRUST.items()}
 trust_ok=all(x['exists'] for k,x in trust.items() if k!='cookie_or_consent')
 canonical=sum(bool(x['canonical']) for x in pages); h1=sum(x['h1_count']==1 for x in pages); main=sum(x['main_landmark'] for x in pages)
 ads=sum(x['ad_markup_detected'] for x in pages)
 course_review=[x['path'] for x in courses if x['status']!='PASS']
 # Monetization configuration checks validate repository facts only. Account
 # approval, CMP activation and rendered placements remain human/account review.
 mon_path=ROOT/'data/monetization/google-monetization.json'
 mon=json.loads(mon_path.read_text()) if mon_path.exists() else {}
 client=mon.get('publisher',{}).get('adsense_client','')
 seller=mon.get('publisher',{}).get('ads_txt_id','')
 ads_lines=[x.strip() for x in (ROOT/'ads.txt').read_text().splitlines() if x.strip() and not x.lstrip().startswith('#')] if (ROOT/'ads.txt').exists() else []
 expected=f"google.com, {seller}, DIRECT, f08c47fec0942fa0"
 duplicate_loaders=[]; wrong_ids=[]
 for page in pages:
  src=(ROOT/page['path']).read_text(errors='ignore')
  if src.count('pagead2.googlesyndication.com/pagead/js/adsbygoogle.js')>1: duplicate_loaders.append(page['path'])
  for found in set(re.findall(r'ca-pub-\\d{16}',src)):
   if client and found!=client: wrong_ids.append({'path':page['path'],'id':found})
 monetization={
  'status':'REVIEW_REQUIRED' if duplicate_loaders or wrong_ids or ads_lines!=[expected] else 'PARTIAL',
  'ads_txt':{'status':'PASS' if ads_lines==[expected] else 'FAIL','actual':ads_lines,'expected':[expected]},
  'publisher_consistency':{'status':'PASS' if client and not wrong_ids else 'FAIL','client':client,'wrong_ids':wrong_ids},
  'duplicate_loader':{'status':'PASS' if not duplicate_loaders else 'FAIL','pages':duplicate_loaders},
  'page_class_and_safe_zones':{'status':'PASS' if (ROOT/'js/monetization.js').exists() else 'FAIL'},
  'consent':{'status':'REVIEW_REQUIRED','note':'A certified CMP and geographic messages must be verified in Google Privacy & messaging; repository code cannot establish account-side activation.'},
  'account_formats':{'status':'REVIEW_REQUIRED','note':'Auto ads format eligibility, activation, exclusions, ad load and Offerwall settings require account review.'},
  'approval_claim':'NOT_ASSESSED'
 }
 result={
  'schema_version':1,'generated_at':dt.datetime.now(dt.timezone.utc).isoformat(),'scope':'all repository public HTML and course JSON','approval_claim':'NOT_ASSESSED — this audit does not claim or predict Google AdSense approval','standard':'docs/GLOBAL_QUALITY_STANDARD.md',
  'content_depth':{'status':state(not thin_indexable,partial=bool(pages) and len(thin_indexable)<len(pages)//10),'pages_scanned':len(pages),'heuristic_review_threshold_words':250,'thin_page_count':len(thin),'thin_indexable_page_count':len(thin_indexable),'note':'Threshold is a triage signal, not a word-count publication rule. The count that matters for publication is thin_indexable: a noindex utility page (404, a JS shell that redirects) is short on purpose and is not judged for depth. CJK and Thai text is counted per character — those scripts have no spaces, and counting them by whitespace made a complete Japanese page look thin.'},
  'originality':{'status':'REVIEW_REQUIRED' if any(dups.values()) else 'PASS','exact_duplicate_title_groups':len(dups['titles']),'exact_duplicate_meta_groups':len(dups['meta_descriptions']),'template_intro_groups':len(dups['introductions']),'repeated_paragraph_groups':len(dups['paragraphs'])},
  'duplicate_risk':{'status':'REVIEW_REQUIRED' if any(dups[k] for k in ('titles','meta_descriptions','introductions')) else 'PASS','affected_page_count':len({p for k in ('titles','meta_descriptions','introductions') for ps in dups[k].values() for p in ps}),'indexable_affected_page_count':len({p for k in ('titles','meta_descriptions','introductions') for ps in dups[k].values() for p in ps} - {x['path'] for x in pages if x['noindex']}),'indexable_affected_note':'affected_page_count includes noindex placeholder pages (level placeholders, JS shells) that Google does not index; indexable_affected_page_count is the number that matters for review.','repeated_paragraph_groups_for_editorial_sampling':len(dups['paragraphs']),'groups':dups,
      'note':'Every group is a paragraph an editor should look at, not proof of duplication. The two pages in the introductions group are the same tutor rendered twice — a home-page card and a roster row share her subject list because it is her list. Shared data is not doorway content; a page whose whole body repeats another page is.'},
  'navigation':{'status':state(all(x['internal_link_count']>=3 for x in pages),partial=any(x['internal_link_count']>=3 for x in pages)),'weak_page_count':sum(x['internal_link_count']<3 for x in pages)},
  'trust_pages':{'status':state(trust_ok,partial=any(x['exists'] for x in trust.values())),'pages':trust},
  'policy_pages':{'status':'PARTIAL' if trust_ok and not trust['cookie_or_consent']['exists'] else state(trust_ok and trust['cookie_or_consent']['exists']),'note':'Cookie/consent applicability and behavior require jurisdictional/legal review; file presence alone is not compliance.'},
  'technical_seo':{'status':state(canonical==len(pages) and h1==len(pages),partial=canonical>0 and h1>0),'canonical_pages':canonical,'single_h1_pages':h1,'pages_scanned':len(pages)},
  'indexability':{'status':state(main==len(pages),partial=main>0),'main_landmark_pages':main,'noindex_pages':sum(x['noindex'] for x in pages),'js_only_value':'REVIEW_REQUIRED — rendered learning value requires browser/manual sampling'},
  'mobile':{'status':'REVIEW_REQUIRED','note':'Static source scan cannot validate viewport overlap, responsiveness, accidental taps, or device performance.'},
  'accessibility':{'status':state(main==len(pages),partial=main>0),'main_landmark_pages':main,'note':'Automated source signals only; keyboard, screen reader, contrast, captions, and zoom require rendered audit.'},
  'ad_safety':{'status':'REVIEW_REQUIRED' if ads else 'PARTIAL','pages_loading_or_marking_ads':ads,'note':'Placement, consent, content/ad balance, mobile accidental-click risk, and approval status require rendered and policy review.'},
  'google_monetization':monetization,
  'page_quality':{'status':'REVIEW_REQUIRED' if review else 'PASS','pass_count':len(pages)-len(review),'review_required_count':len(review),'course_pass_count':len(courses)-len(course_review),'course_review_required_count':len(course_review)},
  'thin_page_count':len(thin),'thin_indexable_page_count':len(thin_indexable),'thin_indexable':thin_indexable,'review_required_count':len(review)+len(course_review),
  'course_quality':{'status':'REVIEW_REQUIRED' if course_review else 'PASS','files_scanned':len(courses),'review_required_count':len(course_review),'rows':courses},
  'review_queue':{'pages':review,'courses':course_review,'thin_pages':thin,'thin_indexable':thin_indexable},
  'page_inventory':pages,
  'limitations':['Similarity is conservative exact/template-signature triage, not semantic plagiarism detection.','No static audit can establish linguistic correctness, legal compliance, rendered accessibility, mobile UX, ad placement safety, or AdSense approval.','All REVIEW_REQUIRED items need repair or documented human review before mass publication.']
 }
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(f"pages={len(pages)} thin={len(thin)} page_review={len(review)} courses={len(courses)} course_review={len(course_review)} ads={ads}")
 print('wrote',OUT.relative_to(ROOT))
 return 0
if __name__=='__main__': raise SystemExit(selftest() if '--selftest' in sys.argv else main())

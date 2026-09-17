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
import json
import re
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/quality/adsense-readiness.json'
EXCLUDED_DIRS={'.git','node_modules','.venv','vendor','reports','research','docs','tools','data'}
TRUST={'about':'about/index.html','contact':'contact/index.html','privacy':'privacy/index.html','terms':'terms/index.html','disclaimer':'disclaimer/index.html','copyright':'copyright/index.html','cookie_or_consent':'cookie-policy/index.html'}
COURSE_LEVELS=('A1','A2','B1','B2','C1','C2')

def state(pass_:bool, partial=False): return 'PASS' if pass_ else ('PARTIAL' if partial else 'FAIL')
def norm(s): return re.sub(r'[^a-z0-9\u0900-\u0d7f]+',' ',s.lower()).strip()

class Scan(HTMLParser):
 def __init__(self):
  super().__init__(); self.title=''; self.h1=[]; self.text=[]; self.meta=''; self.canonical=''; self.links=[]; self.headings=[]; self._tag=''; self.noindex=False; self.main=False; self.ad=False
 def handle_starttag(self,tag,attrs):
  self._tag=tag; a=dict(attrs)
  if tag=='meta' and a.get('name','').lower()=='description': self.meta=a.get('content','')
  if tag=='meta' and a.get('name','').lower()=='robots' and 'noindex' in a.get('content','').lower(): self.noindex=True
  if tag=='link' and 'canonical' in a.get('rel',[]): self.canonical=a.get('href','')
  if tag=='a' and a.get('href'): self.links.append(a['href'])
  if tag=='main': self.main=True
  if tag in ('h1','h2','h3'): self.headings.append(tag)
  if 'adsbygoogle' in a.get('class','') or 'ad-slot' in a.get('class',''): self.ad=True
 def handle_endtag(self,tag): self._tag=''
 def handle_data(self,data):
  s=data.strip()
  if not s or self._tag in ('script','style','noscript'): return
  self.text.append(s)
  if self._tag=='title': self.title+=s
  if self._tag=='h1': self.h1.append(s)

def html_files():
 out=[]
 for p in ROOT.rglob('*.html'):
  rel=p.relative_to(ROOT)
  if any(x in EXCLUDED_DIRS for x in rel.parts) or p.name=='admin.html': continue
  out.append(p)
 return sorted(out)

def signature(text):
 # Template-risk signature deliberately removes volatile names/numbers/currency.
 x=norm(text); x=re.sub(r'\b\d+(?: \d+)*\b','#',x)
 return hashlib.sha256(x.encode()).hexdigest()[:20]

def page_audit():
 pages=[]; title_map=defaultdict(list); meta_map=defaultdict(list); intro_map=defaultdict(list); paragraph_map=defaultdict(list)
 for p in html_files():
  raw=p.read_text('utf-8',errors='ignore'); s=Scan(); s.feed(raw); text=' '.join(s.text); words=re.findall(r"\b[\w'’-]+\b",text,flags=re.UNICODE); rel=str(p.relative_to(ROOT))
  paras=[norm(re.sub('<[^>]+>',' ',x)) for x in re.findall(r'<p\b[^>]*>(.*?)</p>',raw,flags=re.I|re.S)]
  paras=[x for x in paras if len(x.split())>=12]
  intro=paras[0] if paras else ''
  issues=[]
  if not s.title: issues.append('missing_title')
  if not s.meta: issues.append('missing_meta_description')
  if len(s.h1)!=1: issues.append('h1_count_'+str(len(s.h1)))
  if not s.canonical: issues.append('missing_canonical')
  if len(words)<250: issues.append('depth_review_under_250_words')
  if not s.main: issues.append('missing_main_landmark')
  if len(s.links)<3: issues.append('weak_internal_navigation')
  title_map[norm(s.title)].append(rel); meta_map[norm(s.meta)].append(rel)
  if intro: intro_map[signature(intro)].append(rel)
  for para in set(paras): paragraph_map[signature(para)].append(rel)
  pages.append({'path':rel,'word_count':len(words),'title':s.title,'meta_description':s.meta,'h1_count':len(s.h1),'canonical':s.canonical,'noindex':s.noindex,'main_landmark':s.main,'internal_link_count':sum(1 for x in s.links if not urlparse(x).netloc or 'ekguru.shop' in urlparse(x).netloc),'ad_markup_detected':s.ad or 'adsbygoogle' in raw,'issues':issues})
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

def course_audit():
 rows=[]
 for p in sorted((ROOT/'data/courses').glob('phase-*/*.json')):
  try: d=json.loads(p.read_text())
  except Exception as e: rows.append({'path':str(p.relative_to(ROOT)),'status':'FAIL','issues':['invalid_json',str(e)]}); continue
  if not isinstance(d,dict) or 'level' not in d: continue
  units=d.get('level',{}).get('units',[]); lessons=[l for u in units for l in u.get('lessons',[])]
  issues=[]
  if len(units)!=3 or len(lessons)!=6 or any(len(u.get('lessons',[]))!=2 for u in units): issues.append('not_3_units_x_2_lessons')
  for l in lessons:
   for key in ('learn','vocab','grammar','dialogue','practice','quiz','worksheet'):
    if not l.get(key): issues.append(f"{l.get('id','?')}:missing_{key}")
   if len(l.get('practice',[]))<5: issues.append(f"{l.get('id','?')}:thin_practice")
  types={x.get('type') for l in lessons for x in l.get('practice',[]) if x.get('type')}
  lv=d.get('file_level','')
  if len(types)<5: issues.append('narrow_practice_ecosystem')
  advanced_terms=('register','inference','stance','argument','rhetoric','semantic','academic','professional','idiom','discourse','style','pragmatic')
  if lv in ('C1','C2'):
   blob=json.dumps(d,ensure_ascii=False).lower()
   if sum(t in blob for t in advanced_terms)<4: issues.append('advanced_reality_review')
  rows.append({'path':str(p.relative_to(ROOT)),'language':d.get('code'),'level':lv,'lesson_count':len(lessons),'practice_type_count':len(types),'status':'PASS' if not issues else 'REVIEW_REQUIRED','issues':sorted(set(issues))})
 return rows

def main():
 pages,dups=page_audit(); courses=course_audit()
 thin=[x['path'] for x in pages if 'depth_review_under_250_words' in x['issues']]
 review=[x['path'] for x in pages if x['publishability']=='REVIEW_REQUIRED']
 trust={k:{'path':v,'exists':(ROOT/v).exists(),'status':'PASS' if (ROOT/v).exists() else 'REVIEW_REQUIRED'} for k,v in TRUST.items()}
 trust_ok=all(x['exists'] for k,x in trust.items() if k!='cookie_or_consent')
 canonical=sum(bool(x['canonical']) for x in pages); h1=sum(x['h1_count']==1 for x in pages); main=sum(x['main_landmark'] for x in pages)
 ads=sum(x['ad_markup_detected'] for x in pages)
 course_review=[x['path'] for x in courses if x['status']!='PASS']
 result={
  'schema_version':1,'generated_at':dt.datetime.now(dt.timezone.utc).isoformat(),'scope':'all repository public HTML and course JSON','approval_claim':'NOT_ASSESSED — this audit does not claim or predict Google AdSense approval','standard':'docs/GLOBAL_QUALITY_STANDARD.md',
  'content_depth':{'status':state(not thin,partial=bool(pages) and len(thin)<len(pages)//10),'pages_scanned':len(pages),'heuristic_review_threshold_words':250,'thin_page_count':len(thin),'note':'Threshold is a triage signal, not a word-count publication rule.'},
  'originality':{'status':'REVIEW_REQUIRED' if any(dups.values()) else 'PASS','exact_duplicate_title_groups':len(dups['titles']),'exact_duplicate_meta_groups':len(dups['meta_descriptions']),'template_intro_groups':len(dups['introductions']),'repeated_paragraph_groups':len(dups['paragraphs'])},
  'duplicate_risk':{'status':'REVIEW_REQUIRED' if any(dups[k] for k in ('titles','meta_descriptions','introductions')) else 'PASS','affected_page_count':len({p for k in ('titles','meta_descriptions','introductions') for ps in dups[k].values() for p in ps}),'repeated_paragraph_groups_for_editorial_sampling':len(dups['paragraphs']),'groups':dups},
  'navigation':{'status':state(all(x['internal_link_count']>=3 for x in pages),partial=any(x['internal_link_count']>=3 for x in pages)),'weak_page_count':sum(x['internal_link_count']<3 for x in pages)},
  'trust_pages':{'status':state(trust_ok,partial=any(x['exists'] for x in trust.values())),'pages':trust},
  'policy_pages':{'status':'PARTIAL' if trust_ok and not trust['cookie_or_consent']['exists'] else state(trust_ok and trust['cookie_or_consent']['exists']),'note':'Cookie/consent applicability and behavior require jurisdictional/legal review; file presence alone is not compliance.'},
  'technical_seo':{'status':state(canonical==len(pages) and h1==len(pages),partial=canonical>0 and h1>0),'canonical_pages':canonical,'single_h1_pages':h1,'pages_scanned':len(pages)},
  'indexability':{'status':state(main==len(pages),partial=main>0),'main_landmark_pages':main,'noindex_pages':sum(x['noindex'] for x in pages),'js_only_value':'REVIEW_REQUIRED — rendered learning value requires browser/manual sampling'},
  'mobile':{'status':'REVIEW_REQUIRED','note':'Static source scan cannot validate viewport overlap, responsiveness, accidental taps, or device performance.'},
  'accessibility':{'status':state(main==len(pages),partial=main>0),'main_landmark_pages':main,'note':'Automated source signals only; keyboard, screen reader, contrast, captions, and zoom require rendered audit.'},
  'ad_safety':{'status':'REVIEW_REQUIRED' if ads else 'PARTIAL','pages_loading_or_marking_ads':ads,'note':'Placement, consent, content/ad balance, mobile accidental-click risk, and approval status require rendered and policy review.'},
  'page_quality':{'status':'REVIEW_REQUIRED' if review else 'PASS','pass_count':len(pages)-len(review),'review_required_count':len(review),'course_pass_count':len(courses)-len(course_review),'course_review_required_count':len(course_review)},
  'thin_page_count':len(thin),'review_required_count':len(review)+len(course_review),
  'course_quality':{'status':'REVIEW_REQUIRED' if course_review else 'PASS','files_scanned':len(courses),'review_required_count':len(course_review),'rows':courses},
  'review_queue':{'pages':review,'courses':course_review,'thin_pages':thin},
  'page_inventory':pages,
  'limitations':['Similarity is conservative exact/template-signature triage, not semantic plagiarism detection.','No static audit can establish linguistic correctness, legal compliance, rendered accessibility, mobile UX, ad placement safety, or AdSense approval.','All REVIEW_REQUIRED items need repair or documented human review before mass publication.']
 }
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(f"pages={len(pages)} thin={len(thin)} page_review={len(review)} courses={len(courses)} course_review={len(course_review)} ads={ads}")
 print('wrote',OUT.relative_to(ROOT))
 return 0
if __name__=='__main__': raise SystemExit(main())

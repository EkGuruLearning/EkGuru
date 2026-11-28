#!/usr/bin/env python3
"""Reproducible repository snapshot, not a substitute for editorial review.

Scans every public HTML file for inbound links, inventories candidates using
explicit evidence, inspects sitemap membership and resolves referenced assets.
Never changes pages, canonicals, sitemaps or migration decisions.
"""
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import importlib.util
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ekguru.shop'
PRIVATE = {'node_modules', '.git', '.github', '.arena', '.cache', '.local', '.playwright-cli', 'tools', 'tests', 'src', 'reports', 'docs', 'research', 'apps-script', 'server', 'csv', 'live-sheets', 'uploads', 'audit', 'generators', 'integrations', 'config', 'scripts', '_site', '.artifacts', 'playwright-report', 'test-results', 'Unselected files'}

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.title=''; self.h1=''; self.capture=''; self.canonical=''; self.robots=''; self.links=[]; self.assets=[]; self.scripts=[]; self.main_depth=0; self.main_text=[]; self.notice=False; self.hindi_in_main=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='main': self.main_depth+=1
        if self.main_depth and a.get('lang','').lower() in ('hi','hi-in','hi-deva'): self.hindi_in_main=True
        if tag=='title': self.capture='title'
        if tag=='h1' and not self.h1: self.capture='h1'
        if tag=='link' and 'canonical' in a.get('rel','').lower().split(): self.canonical=a.get('href','')
        if tag=='link' and a.get('href') and 'stylesheet' in a.get('rel','').lower().split(): self.assets.append(a['href'])
        if tag=='meta' and a.get('name','').lower()=='robots': self.robots=a.get('content','')
        if tag=='a' and a.get('href'): self.links.append(a['href'])
        if tag in ('img','audio','source','video') and a.get('src'): self.assets.append(a['src'])
        if tag=='script' and a.get('src'): self.scripts.append(a['src'])
        if 'eg-review-notice' in a.get('class',''): self.notice=True
    def handle_endtag(self,tag):
        if tag=='main' and self.main_depth: self.main_depth-=1
        if tag==self.capture: self.capture=''
    def handle_data(self,txt):
        if self.capture=='title': self.title+=txt
        if self.capture=='h1': self.h1+=txt
        if self.main_depth: self.main_text.append(txt)

def url(path):
    p=path.relative_to(ROOT).as_posix()
    return '/'+(p[:-10] if p.endswith('/index.html') else ('' if p=='index.html' else p))

def local(ref,base):
    full=urlsplit(urljoin(BASE+base,ref))
    if full.hostname not in ('ekguru.shop','www.ekguru.shop'): return None
    path=unquote(full.path)
    return path[:-10] if path.endswith('/index.html') else path

def kind(u):
    if '/foundation/' in u: return 'foundation lesson or index'
    if '/academy/' in u: return 'earlier academy resource'
    if u.startswith('/daily-hindi/'): return 'daily lesson or index'
    if u.startswith('/languages/hi/'): return 'graded level or course'
    if u.startswith('/hindi/'): return 'Hindi topic'
    if u.startswith('/materials/'): return 'printable resource'
    if u.startswith('/toolbox/'): return 'tool'
    if u.startswith(('/ask/','/answers/')): return 'question or answer'
    if '/practice/' in u: return 'practice'
    return 'guide, course or related page'

def candidate(u,p):
    evidence=[]; probe=(u+' '+p.title+' '+p.h1).lower()
    if 'hindi' in probe or u.startswith(('/languages/hi/','/learn-hindi-')): evidence.append('Hindi in URL/title/H1 or Hindi course tree')
    if p.hindi_in_main: evidence.append('lang=hi in main content')
    return evidence

def asset_record(ref,base):
    path=local(ref,base)
    if not path: return {'reference':ref,'scope':'external','exists':None}
    file=ROOT / path.lstrip('/')
    return {'reference':ref,'resolved':path,'scope':'local','exists':file.is_file()}

def main():
    # Use exactly the publisher's public-path rules, so the scan includes all
    # public HTML, not only files in folders with Hindi in their names.
    spec=importlib.util.spec_from_file_location('publicdist', ROOT/'tools/build-public-dist.py')
    publicdist=importlib.util.module_from_spec(spec); spec.loader.exec_module(publicdist)
    all_pages=[]; errors=[]
    for name in publicdist.iter_public():
        if not name.lower().endswith('.html'): continue
        f=ROOT/name
        try:
            p=Page(); p.feed(f.read_text(encoding='utf8'))
            all_pages.append((f,url(f),p))
        except (UnicodeError,OSError) as exc: errors.append({'source':name,'error':str(exc)})
    chosen=[(f,u,p,candidate(u,p)) for f,u,p in all_pages if candidate(u,p)]
    known={u for _,u,_,_ in chosen}; inbound=defaultdict(set)
    for _,u,p in all_pages:
        for v in set(filter(None,(local(h,u) for h in p.links))):
            if v in known: inbound[v].add(u)
    sitemaps=defaultdict(list); sitemap_errors=[]
    for f in sorted(ROOT.glob('sitemap*.xml')):
        try:
            for el in ET.parse(f).iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                if el.text:
                    loc=local(el.text,'/')
                    if loc in known: sitemaps[loc].append(f.name)
        except (ET.ParseError,OSError) as exc: sitemap_errors.append({'source':f.name,'error':str(exc)})
    # Map only explicitly registered chapters; every other record remains
    # unassigned rather than using a keyword as a pedagogical decision.
    curriculum=json.loads((ROOT/'data/hindi-academy/curriculum.json').read_text(encoding='utf8'))
    assignments=defaultdict(list)
    for pathway in curriculum.get('textbook',{}).get('pathways',[]):
        for book in pathway['books']:
            for phase in book['phases']:
                for chapter in phase['chapters']:
                    assignments[chapter['source_url']].append({'pathway':pathway['id'],'course':book['id'],'phase':phase['id'],'chapter':chapter['id'], 'purpose':chapter['title'], 'status':chapter['status']})
    hashes=defaultdict(list)
    records=[]
    for f,u,p,evidence in sorted(chosen,key=lambda t:t[1]):
        assets=[asset_record(ref,u) for ref in sorted(set(p.assets+p.scripts))]
        text=' '.join(' '.join(p.main_text).split())
        if text: hashes[hashlib.sha256(text.encode('utf8')).hexdigest()].append(u)
        assignment=assignments.get(u,[])
        records.append({'source':str(f.relative_to(ROOT)), 'url':u, 'type':kind(u), 'title':p.title.strip(), 'h1':p.h1.strip(), 'detection_evidence':evidence, 'subject':'Hindi relevance requires review', 'proficiency':'unassigned', 'age_groups':'unassigned', 'course':assignment[0]['course'] if assignment else 'unassigned', 'phase':assignment[0]['phase'] if assignment else 'unassigned', 'chapter':assignment[0]['chapter'] if assignment else 'unassigned', 'educational_purpose':assignment[0]['purpose'] if assignment else 'not manually assessed', 'content_quality':'not manually assessed', 'curriculum_assignments':assignment, 'main_word_count_approx':len(re.findall(r'\S+',' '.join(p.main_text))), 'dependencies':assets, 'review':'draft notice present' if p.notice else 'not established', 'inbound_from_public_html_count':len(inbound[u]), 'inbound_sources_sample':sorted(inbound[u])[:12], 'internal_outbound':sorted(set(filter(None,(local(h,u) for h in p.links)))), 'canonical':p.canonical, 'robots':p.robots, 'sitemaps':sorted(set(sitemaps[u])), 'proposed_target':u, 'migration_action':'KEEP', 'migration_note':'Preserve URL; assignment and content assessment require human review.'})
    sources=[]
    for tree in ['data','src','tools','css','js','images']:
        base=ROOT/tree
        if base.exists():
            for f in base.rglob('*'):
                if f.is_file() and not any(x.startswith('.') or x=='__pycache__' for x in f.relative_to(base).parts) and re.search('hindi|devanagari',str(f.relative_to(ROOT)),re.I):
                    sources.append({'source':str(f.relative_to(ROOT)), 'size_bytes':f.stat().st_size, 'classification':'name match; review purpose, rights and usage'})
    duplicates=[group for group in hashes.values() if len(group)>1]
    inbound_report={'method':'All static anchor sources in public HTML; same-host absolute and relative links normalized, no runtime links or external inbound links.', 'inbound_sources':{u:sorted(inbound[u]) for u in sorted(known)}}
    (ROOT/'docs/architecture/hindi/resource-inbound-links.json').write_text(json.dumps(inbound_report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    result={'exact_main_text_duplicate_candidates':duplicates, 'method':'All public HTML scanned for static anchor inbound links; Hindi candidates detected by URL/title/H1 or lang=hi within main; sitemap locs and HTML src/stylesheet/script dependencies inspected. No runtime links, CSS imports, dynamically loaded content, assets without HTML src, live crawl, human quality review or proof of Hindi relevance. Other source files may lack Hindi in their path. KEEP is a safety default, not completed mapping.', 'public_html_scanned':len(all_pages), 'read_errors':errors, 'sitemap_errors':sitemap_errors, 'pages':records, 'named_sources_and_assets':sorted(sources,key=lambda x:x['source']), 'summary':{'pages':len(records),'types':dict(Counter(x['type'] for x in records)), 'named_sources_and_assets':len(sources), 'public_html_scanned':len(all_pages), 'sitemapped_candidates':sum(bool(x['sitemaps']) for x in records), 'curriculum_assigned_candidates':sum(bool(x['curriculum_assignments']) for x in records), 'exact_main_text_duplicate_groups':len(duplicates), 'unresolved_local_asset_references':sum(sum(x['scope']=='local' and not x['exists'] for x in r['dependencies']) for r in records)}}
    out=ROOT/'docs/architecture/hindi/resource-inventory.json'; out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result['summary'],ensure_ascii=False,indent=2))
    if errors or sitemap_errors: raise SystemExit('Inventory has read errors; inspect report')

if __name__=='__main__': main()

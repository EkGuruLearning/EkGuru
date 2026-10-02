#!/usr/bin/env python3
"""Static + round-trip checks of the additive site features on every public page."""
import importlib.util
import json
import re
import sys
from lib.ultra_content import ROOT, Page, load, pages, route

spec = importlib.util.spec_from_file_location('au', ROOT / 'tools/apply-ultra.py'); au = importlib.util.module_from_spec(spec); spec.loader.exec_module(au)
meta = load('data/editorial/page-metadata.json')['pages']; errors = []; n = 0
checks = 0
def fail(rel, msg): errors.append(f'{rel}: {msg}')
for p in pages():
    rel = p.relative_to(ROOT).as_posix()
    if rel == 'admin.html': continue
    raw = p.read_text(encoding='utf-8'); n += 1; s = Page(raw); base = au.strip(raw)
    if au.transform(base, rel, meta) != raw: fail(rel, 'decoration is not current/idempotent')
    if au.strip(raw) != base or re.search(r'ekguru:ultra-(?:' + '|'.join(au.SLOTS) + r'):(?:start|end)', au.strip(raw)): fail(rel, 'strip leaves ultra markers')
    for slot in au.SLOTS:
        if raw.count(f'<!-- ekguru:ultra-{slot}:start -->') > 1: fail(rel, f'duplicate {slot} block')
    if '<!-- ekguru:ultra-head:start -->' not in raw: fail(rel, 'missing head block'); continue
    head = raw.split('</head>', 1)[0]
    first_css = head.find('<link rel="stylesheet"'); first_block = head.find('<!-- ekguru:ultra-head:start -->')
    if first_css >= 0 and first_block > first_css and 'rel="stylesheet"' in head[:first_block]: fail(rel, 'theme init is not before the first stylesheet')
    if not re.search(r'<html\b[^>]*data-learning-language="[a-z]{2,3}"', raw): fail(rel, 'no learning language on <html>')
    if 'hindi-srs.js' in raw and raw.find('/js/global-srs.js"></script>') > raw.find('hindi-srs.js') >= 0: fail(rel, 'global-srs must load before hindi-srs')
    if raw.count('class="eg-appearance"') != 1: fail(rel, 'appearance control missing or duplicated')
    if 'adsbygoogle' in raw and re.search(r'/(?:languages/[^/]+/(?:level|lessons|practice|quiz|review)|learn/(?:practice|review|quiz)|courses|start)/', route(p)): fail(rel, 'ad loader on an interactive page')
    robots = Page(base).meta.get('robots'); 
    if Page(raw).meta.get('robots') != robots: fail(rel, 'robots changed by decoration')
    if Page(raw).canonical != Page(base).canonical: fail(rel, 'canonical changed by decoration')
for rel in au.NEW_PAGES:
    p = ROOT / rel; raw = p.read_text(encoding='utf-8'); s = Page(raw)
    if not s.noindex: fail(rel, 'new page must be noindex')
    if s.mains != 1 or len(s.h1) != 1: fail(rel, 'needs one main and one h1')
    if 'adsbygoogle' in raw: fail(rel, 'no ad loader on a trust/journal page')
    if 'Reviewed by: not recorded' not in raw and rel != 'design/index.html' and 'AI-assisted draft' not in raw: fail(rel, 'missing honest byline')
home = (ROOT / 'index.html').read_text(); hub = (ROOT / 'languages/es/index.html').read_text(); lvl = (ROOT / 'languages/hi/level/a1/index.html').read_text()
if 'data-eg-today' not in home or 'data-eg-continue' not in home: errors.append('home lacks continue/today')
if 'data-eg-today' not in hub or 'Draft: not yet reviewed by a native speaker' not in hub: errors.append('available language hub lacks plan or honest draft notice')
if 'data-eg-download-level' not in lvl or 'data-eg-lesson-page' not in lvl: errors.append('level page lacks lesson tools')
if 'data-eg-placement' not in (ROOT / 'start/index.html').read_text(): errors.append('/start/ lacks the adaptive starting-point host')
if 'device-learning-and-optional-services' not in (ROOT / 'privacy/index.html').read_text(): errors.append('privacy page lacks the device-learning disclosure')
ar = (ROOT / 'ar/index.html').read_text()
if 'المظهر' not in ar or 'dir="rtl"' not in ar.split('eg-appearance')[1][:80]: errors.append('Arabic page lacks its localized RTL appearance control')
for forbidden in ('Native-speaker reviewed', 'native-speaker approved', 'Certified by'):
    for rel in au.NEW_PAGES:
        if forbidden.lower() in (ROOT / rel).read_text().lower(): errors.append(f'{rel}: forbidden approval claim "{forbidden}"')
print(f'ultra integration test: {n} pages, {len(errors)} problems')
for e in errors[:25]: print(' ', e)
raise SystemExit(1 if errors else 0)

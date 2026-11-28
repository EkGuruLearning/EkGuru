#!/usr/bin/env python3
"""First-batch static hub guarantees, including no-JS navigation."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[2]

class Hub(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.region = [], [], False
    def handle_comment(self, text):
        if text.strip() == 'ekguru:hindi-hub:start': self.region = True
        if text.strip() == 'ekguru:hindi-hub:end': self.region = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'): self.ids.append(attrs['id'])
        if self.region and tag == 'a' and attrs.get('href'): self.links.append(attrs['href'])

page = Hub()
page.feed((ROOT / 'learn/hindi/index.html').read_text(encoding='utf-8'))
ids = Counter(page.ids)
for old_id in ('hh-start', 'hh-levels', 'hh-topics', 'hh-guides', 'hh-daily',
               'hh-practice', 'hh-tools', 'hh-questions', 'hh-tutors', 'hh-other'):
    assert ids[old_id] == 1, (old_id, ids[old_id])
assert 'academy-home' not in ids
for route in ('foundation/', 'beginner/', 'elementary/', 'intermediate/', 'advanced/',
              'my-progress/', 'academy/vowels/', 'academy/worksheet/', 'academy/answers/'):
    assert route in page.links, route
for ref in page.links:
    target = urlsplit(urljoin('https://ekguru.shop/learn/hindi/', ref))
    if target.netloc != 'ekguru.shop': continue
    path = ROOT / unquote(target.path).lstrip('/')
    if target.path.endswith('/'): path /= 'index.html'
    assert path.is_file(), ref
    if target.path == '/learn/hindi/' and target.fragment:
        assert ids[unquote(target.fragment)] == 1, ref
print(f'PASS Hindi hub: 10 legacy anchors, 9 priority routes, {len(page.links)} local/external links checked')

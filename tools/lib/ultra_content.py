"""Shared read-only public traversal/own-content parser. No UA logic, mutation or network."""
import hashlib
import json
import os
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[2]
EXCLUDE = {'.git', 'node_modules', '.artifacts', 'reports', 'research', 'docs', 'tools', 'tests', 'data', 'Arena latest command  arena', 'images', 'fonts', 'templates', 'build', 'dist'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
CHROME = {'voice-control', 'voice-settings', 'eg-byline', 'eg-today', 'eg-continue', 'eg-review-notice', 'eg-visual', 'pg-note', 'pg-cta', 'crumb', 'crumbs', 'sb-note', 'sb-hint', 'sb-voicenudge', 'sb-chapter', 'sb-mastery', 'updated', 'dateline', 'cta', 'cta-box'}


def pages(root=ROOT):
    found = []
    for d, dirs, files in os.walk(root):
        dirs[:] = [n for n in dirs if n not in EXCLUDE and not n.startswith('.')]
        for name in files:
            if name.endswith('.html') and not re.fullmatch(r'google[a-z0-9]+\.html', name):
                found.append(Path(d) / name)
    return sorted(found)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.stack = []; self.meta = {}; self.canonical = ''; self.title = ''; self.text = []
        self.links = []; self.ids = set(); self.ld = []; self.images = []; self.h1 = []
        self.mains = 0; self.lang = ''; self._ld = None
        self._main = bool(re.search(r'<main\b', text, re.I))
        self.feed(text)

    @property
    def noindex(self):
        return 'noindex' in self.meta.get('robots', '').lower()

    @property
    def own(self):
        return ' '.join(self.text)

    def handle_starttag(self, t, attrs):
        a = dict(attrs)
        if t == 'html': self.lang = a.get('lang', '')
        if t == 'meta': self.meta[a.get('name', a.get('property', '')).lower()] = a.get('content', '')
        if t == 'link' and 'canonical' in a.get('rel', '').split(): self.canonical = a.get('href', '')
        if t == 'a' and a.get('href'): self.links.append(a['href'])
        if a.get('id'): self.ids.add(a['id'])
        if t == 'img': self.images.append(a)
        if t == 'h1': self.h1.append('')
        if t == 'main': self.mains += 1
        if t == 'script' and a.get('type') == 'application/ld+json': self._ld = ''
        if t not in VOID: self.stack.append((t, a))

    def handle_startendtag(self, t, a):
        self.handle_starttag(t, a)
        if t not in VOID: self.handle_endtag(t)

    def handle_endtag(self, t):
        if t == 'script' and self._ld is not None:
            self.ld.append(self._ld); self._ld = None
        tags = [x[0] for x in self.stack]
        if t in tags: self.stack = self.stack[:len(tags) - 1 - tags[::-1].index(t)]

    def handle_data(self, s):
        if self._ld is not None: self._ld += s
        if not s.strip(): return
        tags = [t for t, a in self.stack]
        if 'title' in tags: self.title += s
        if any(t in tags for t in ('head', 'script', 'style', 'template', 'noscript')): return
        if 'h1' in tags and self.h1: self.h1[-1] += s
        if self._main and 'main' not in tags: return
        if any(t in tags for t in ('nav', 'header', 'footer')): return
        if any('hidden' in a or 'data-eg-chrome' in a or set(a.get('class', '').split()) & CHROME for t, a in self.stack): return
        self.text.append(s.strip())


def own(text):
    text = re.sub(r'<!-- ekguru:(?:pw-bands|trust-footer):start -->[\s\S]*?<!-- ekguru:(?:pw-bands|trust-footer):end -->', '', text)
    return Page(text).own


def own_hash(text):
    return hashlib.sha256(re.sub(r'\s+', ' ', own(text)).encode()).hexdigest()


def load(path, default=None):
    p = ROOT / path
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default


def save_json(path, value, check=False):
    p = ROOT / path
    out = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    if p.exists() and p.read_text(encoding='utf-8') == out: return True
    if check:
        print('STALE', path); return False
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(out, encoding='utf-8'); return True


def route(p):
    rel = p.relative_to(ROOT).as_posix() if isinstance(p, Path) else p
    return '/' if rel == 'index.html' else '/' + (rel[:-10] if rel.endswith('/index.html') else rel)


def local(value, base='/'):
    u = urlsplit(urljoin('https://ekguru.shop' + base, value))
    if u.scheme not in ('https', 'http') or u.netloc.lower() != 'ekguru.shop': return None
    path = ROOT / unquote(u.path).lstrip('/')
    if u.path.endswith('/') or path.is_dir(): path = path / 'index.html'
    return path if path.is_relative_to(ROOT) else None

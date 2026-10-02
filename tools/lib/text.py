"""Unicode-aware deterministic proxies for audit; never claim they replace a native editor."""
import re
import unicodedata

UNSPACED = re.compile(r'[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af\u0e00-\u0e7f]')


def tokens(text):
    text = UNSPACED.sub(lambda m: ' ' + m[0] + ' ', str(text).casefold())
    out = []
    for item in text.split():
        token = ''.join(c for c in item if unicodedata.category(c)[0] in ('L', 'M', 'N'))
        if token and any(unicodedata.category(c)[0] in ('L', 'N') for c in token): out.append(token)
    return out


RANGES = {
    'Deva': [(0x900, 0x97f)], 'Beng': [(0x980, 0x9ff)], 'Guru': [(0xa00, 0xa7f)], 'Gujr': [(0xa80, 0xaff)],
    'Taml': [(0xb80, 0xbff)], 'Telu': [(0xc00, 0xc7f)], 'Knda': [(0xc80, 0xcff)], 'Mlym': [(0xd00, 0xd7f)],
    'Arab': [(0x600, 0x6ff), (0x750, 0x77f), (0x8a0, 0x8ff)], 'Hebr': [(0x590, 0x5ff)], 'Cyrl': [(0x400, 0x52f)],
    'Grek': [(0x370, 0x3ff), (0x1f00, 0x1fff)], 'Thai': [(0xe00, 0xe7f)], 'Hang': [(0xac00, 0xd7af), (0x1100, 0x11ff)],
    'Kore': [(0xac00, 0xd7af), (0x1100, 0x11ff), (0x4e00, 0x9fff)], 'Jpan': [(0x3040, 0x30ff), (0x4e00, 0x9fff)],
    'Hani': [(0x3400, 0x9fff)], 'Hans': [(0x3400, 0x9fff)], 'Hant': [(0x3400, 0x9fff)], 'Latn': [(0x41, 0x24f), (0x1e00, 0x1eff)]}


def in_script(text, scripts):
    """True only when every letter belongs to one of the declared scripts (never mixed prose)."""
    letters = [c for c in text if unicodedata.category(c).startswith('L')]
    blocks = [r for s in scripts for r in RANGES.get(s, [])]
    return bool(letters) and bool(blocks) and all(any(lo <= ord(c) <= hi for lo, hi in blocks) for c in letters)

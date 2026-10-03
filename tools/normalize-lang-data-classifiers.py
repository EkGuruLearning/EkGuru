#!/usr/bin/env python3
"""One-off: give every Indian starter pack's counting examples the shape the rest of the file uses.

`tools/lang-data/<slug>.json` writes almost every word list as
``{"t": <target text>, "r": <romanisation>, "en": <English>, "hi": <Hindi>}`` —
see ``greetings``, ``pronouns``, ``food_words``. The ``classifiers`` list is the
one exception: its three entries carry the target text in ``en`` and have no
``t`` at all::

    {"en": "ஒரு புத்தகம்", "hi": "एक किताब", "r": "oru puttakam",
     "note": "one book — number + noun, no extras"}

Two things went wrong because of it.

* ``tools/language-gate.py`` normalises ``classifiers`` like any other word
  list, so it read an empty ``t`` for each entry. That is the T2 schema error
  ``words/*/t:minLength`` on Kannada, and it also means those 27 entries were
  skipped by the script and romanisation checks — a word with no ``t`` is
  filtered out before it can be tested.
* ``tools/build-language-course.py`` had to reach for ``c['en']`` to print the
  target-language word, which is why the shape survived.

The English gloss is already in the file: it is the part of ``note`` before the
em dash. So the fix invents nothing — it moves the target text to ``t``, moves
the existing note prefix to ``en``, and leaves ``hi``, ``r`` and ``note`` alone.
``tools/build-language-course.py`` is updated to print ``c['t']`` in the same
commit, so the rendered pages do not change.

Every file is rewritten in the exact format it already had (indent 1 or 2, key
order preserved). A file whose format cannot be reproduced byte-for-byte is left
untouched and reported — a normaliser that silently reformats a whole file would
bury this change in noise.

  python3 tools/normalize-lang-data-classifiers.py --check    report only
  python3 tools/normalize-lang-data-classifiers.py            write
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEPARATOR = ' \u2014 '  # the em dash that joins gloss and explanation in `note`

# The formats the nine files are actually written in. A file is only rewritten
# if one of these reproduces it exactly, so the diff stays reviewable.
FORMATS = [{'indent': 1}, {'indent': 2}]


def render(data, fmt):
    return json.dumps(data, ensure_ascii=False, indent=fmt['indent'])


def detect_format(raw, data):
    for fmt in FORMATS:
        if render(data, fmt) == raw:
            return fmt
    return None


def normalize(data):
    """Move the classifier target text from `en` to `t`, and the gloss into `en`."""
    changed = 0
    for entry in data.get('classifiers', []):
        if entry.get('t') or not entry.get('en'):
            continue  # already correct, or nothing to move
        target = entry['en']
        note = entry.get('note') or ''
        if SEPARATOR not in note:
            raise SystemExit(
                'refusing to guess the English gloss for %r: its note %r has no %r'
                % (target, note, SEPARATOR))
        entry['t'] = target
        entry['en'] = note.split(SEPARATOR, 1)[0]
        changed += 1
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='report without writing')
    args = ap.parse_args()

    total, skipped, files = 0, [], 0
    for path in sorted(glob.glob(os.path.join(ROOT, 'tools', 'lang-data', '*.json'))):
        slug = os.path.basename(path)[:-len('.json')]
        raw = open(path, encoding='utf-8').read()
        data = json.loads(raw)
        if not data.get('classifiers'):
            continue
        fmt = detect_format(raw, data)
        if fmt is None:
            skipped.append(slug)
            print('  skip  %-12s format not reproducible; left untouched' % slug)
            continue
        before = json.dumps(data.get('classifiers'), ensure_ascii=False, sort_keys=True)
        changed = normalize(data)
        after = json.dumps(data.get('classifiers'), ensure_ascii=False, sort_keys=True)
        if not changed or before == after:
            print('  ok    %-12s already normalised' % slug)
            continue
        files += 1
        total += changed
        print('  fix   %-12s %d classifier entries -> t/en' % (slug, changed))
        if not args.check:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(render(data, fmt))

    verb = 'would fix' if args.check else 'fixed'
    print('%s %d entries across %d file(s)%s'
          % (verb, total, files, '; skipped: ' + ', '.join(skipped) if skipped else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())

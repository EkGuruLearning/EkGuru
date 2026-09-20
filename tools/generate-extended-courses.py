#!/usr/bin/env python3
"""Extended-course generator — MUST NOT emit placeholders.

History: this file used to manufacture A3/B3/C3/C4/C5 (and whole new-language
A1–C2 packs) as `{code}_word_{n}_{i}` / `roman_{n}_{i}` / “theme related word”.
Those files were published. That is the defect this rewrite exists to stop.

Real extra levels are authored in tools/lib/extended_banks.py and written by
tools/repair-extended-levels.py. Languages without an authored bank are written
as content_status=INCOMPLETE (empty units, not indexable). Alias codes such as
ne/uz/ms/tl never spawn a second course — see data/global/language-code-map.json.

This module remains as the named entry point so older docs and CI still have
somewhere to point. It refuses to generate placeholders.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

USAGE = """\
tools/generate-extended-courses.py no longer writes courses.

The old generator emitted placeholder word tokens and romanisation stubs.
That path is closed.

  python3 tools/repair-extended-levels.py        # stubs + authored extra levels
  python3 tools/repair-extended-levels.py --scan # fail if placeholders remain
  python3 tools/build-course-levels.py           # HTML + sitemap from real data
"""


def generate_lesson_content(*_a, **_k):
    raise RuntimeError(
        "Refusing to generate placeholder lessons. "
        "Author tools/lib/extended_banks.py and run tools/repair-extended-levels.py."
    )


def generate_course_json(*_a, **_k):
    raise RuntimeError(
        "Refusing to generate placeholder courses. "
        "Run python3 tools/repair-extended-levels.py"
    )


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--force-placeholders" in argv:
        raise SystemExit(
            "ERROR: --force-placeholders is not allowed. "
            "Placeholder course JSON is unpublished material."
        )
    print(USAGE)
    return 2


if __name__ == "__main__":
    sys.exit(main())

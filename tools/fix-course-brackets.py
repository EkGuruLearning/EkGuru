#!/usr/bin/env python3
"""Auto-fix lesson/unit/test boundary brackets in course JSON files.

Usage:  python3 tools/fix-course-brackets.py data/courses/phase-1/de_A2.json [...]

For every ,{"id":...} and ,"test" marker, the segment between the last '"]'
(key-array close) and the marker must contain only brackets — it is replaced
with the exact correct tail:
  lesson -> lesson :  }]}}        then ,{"id":"..-L.."}
  lesson -> unit   :  }]}}]},      then ,{"id":"..-U.."}
  lesson -> test   :  }]}}]}]      then ,"test"
Anything else is reported, never guessed. Re-runs are safe (idempotent).
"""
import json
import re
import sys

TAILS = {"lesson": "}]}}", "unit": "}]}}]}", "test": "}]}}]}]"}


def fix_file(path):
    raw = open(path, encoding="utf-8").read()
    fixes = []
    problems = []

    def splice(marker_idx, kind):
        seg_start = raw.rfind('"]', 0, marker_idx)
        if seg_start < 0:
            problems.append(f"{kind}@char{marker_idx}: no preceding '\"]'")
            return marker_idx
        between = raw[seg_start + 2:marker_idx]
        want = TAILS[kind]
        if between == want:
            return marker_idx
        if re.fullmatch(r"[\]}\[,]*", between) is None:
            problems.append(f"{kind}@char{marker_idx}: non-bracket {between!r}")
            return marker_idx
        fixes.append(f"{kind}@char{marker_idx}: {between!r}->{want!r}")
        return seg_start, want, marker_idx

    # collect markers first (indices shift as we splice right-to-left)
    markers = []
    for m in re.finditer(r',\{"id":"([^"]+)"', raw):
        markers.append((m.start(), "lesson" if "-L" in m.group(1) else "unit"))
    for m in re.finditer(r',"test"', raw):
        markers.append((m.start(), "test"))
    markers.sort(reverse=True)
    for idx, kind in markers:
        seg_start = raw.rfind('"]', 0, idx)
        if seg_start < 0:
            problems.append(f"{kind}@char{idx}: no preceding '\"]'")
            continue
        between = raw[seg_start + 2:idx]
        want = TAILS[kind]
        if between == want:
            continue
        if re.fullmatch(r"[\]}\[,]*", between) is None:
            problems.append(f"{kind}@char{idx}: non-bracket {between!r}")
            continue
        fixes.append(f"{kind}@char{idx}: {between!r}->{want!r}")
        raw = raw[:seg_start + 2] + want + raw[idx:]
    open(path, "w", encoding="utf-8").write(raw)
    for f in sorted(fixes):
        print(f"  FIX {path} {f}")
    for p in problems:
        print(f"  PROBLEM {path} {p}")
    try:
        json.loads(raw)
        print(f"  {path}: PARSE-OK")
        return True
    except Exception as e:
        print(f"  {path}: STILL-BAD: {e}")
        return False


if __name__ == "__main__":
    ok = True
    for p in sys.argv[1:]:
        print(p)
        ok = fix_file(p) and ok
    sys.exit(0 if ok else 1)

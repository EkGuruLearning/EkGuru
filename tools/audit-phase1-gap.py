#!/usr/bin/env python3
"""PHASE 1 gap report — what every PUBLISHED language still needs.

PHASE 1 of the AdSense command is "content depth: every language gets full
levels". Its scope is the 18 published courses (data/quality/course-publication-
audit.json -> publishable_levels), not all 89 T1 courses: the other 71 are
already quarantined as research-only, so authoring them is a different phase.

The requirements are not invented here — they are read straight out of the
validator the language gate itself uses:

  data/schemas/course-t1.schema.json, enforced by tools/lib/validate-language-schema.mjs
    level.required      title, goals, units, test, extra
    units               minItems 3, maxItems 5
    unit.lessons        minItems 3, maxItems 5      <- the 2-lessons failure
    test.items          minItems 10, maxItems 20
    extra.required      culture, reading, listening, idioms, mistakes, task

  RUNGS (tools/language-gate.py)
    A1 A1+ A2 A2+ B1 B1+ B2 B2+ C1 C1+ C2          <- 11; courses carry 6

Run:  python3 tools/audit-phase1-gap.py            report
      python3 tools/audit-phase1-gap.py --check    exit 1 while gaps remain
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNGS = ["A1", "A1+", "A2", "A2+", "B1", "B1+", "B2", "B2+", "C1", "C1+", "C2"]
LEGACY_BRIDGES = {"A3": "A2+", "B3": "B2+"}   # authored stubs, CEFR-equivalent clear


def published_codes() -> list[str]:
    audit = json.loads((ROOT / "data/quality/course-publication-audit.json").read_text(encoding="utf-8"))
    return sorted(r["code"] for r in audit["courses"] if r.get("publishable_levels"))


def course_phase(code: str) -> str | None:
    catalogue = json.loads((ROOT / "data/courses/index.json").read_text(encoding="utf-8"))
    for c in catalogue["courses"]:
        if c["code"] == code:
            return c["phase"]
    return None


def schema_errors(codes: list[str]) -> dict:
    """One validator run for every published language's existing rung files."""
    request = {"registry": [], "t1": {}, "t2": {}, "t3": {}}
    for code in codes:
        phase = course_phase(code)
        have = []
        for rung in RUNGS:
            path = ROOT / f"data/courses/{phase}/{code}_{rung}.json"
            if path.exists():
                have.append({"rung": rung, "file": str(path.relative_to(ROOT))})
        if have:
            request["t1"][code] = have
    tmp = ROOT / ".phase1-request.json"
    tmp.write_text(json.dumps(request), encoding="utf-8")
    try:
        out = subprocess.run(["node", "tools/lib/validate-language-schema.mjs", str(tmp)],
                             cwd=ROOT, capture_output=True, text=True)
        if out.returncode:
            raise SystemExit("schema validator failed: " + out.stderr[-400:])
        return json.loads(out.stdout)["t1"]
    finally:
        tmp.unlink(missing_ok=True)


def main() -> int:
    check = "--check" in sys.argv
    codes = published_codes()
    errors = schema_errors(codes)
    print(f"PHASE 1 — content depth for the {len(codes)} published language(s)\n")
    print(f"  {'lang':4s} {'rungs':>7s}  {'missing rungs':28s} {'extra':>5s} {'<3 lessons':>10s} {'test':>5s}")
    total_missing = total_extra = total_lessons = total_test = 0
    work = []
    for code in codes:
        phase = course_phase(code)
        present = [r for r in RUNGS if (ROOT / f"data/courses/{phase}/{code}_{r}.json").exists()]
        missing = [r for r in RUNGS if r not in present]
        errs = errors.get(code, {})
        flat = [e for lst in errs.values() for e in lst]
        extra = sum(1 for e in flat if e.endswith("level.extra"))
        short = sum(1 for e in flat if "lessons" in e)
        test = sum(1 for e in flat if "test" in e)
        total_missing += len(missing)
        total_extra += extra
        total_lessons += short
        total_test += test
        work.append((code, missing))
        print(f"  {code:4s} {len(present):3d}/11  {','.join(missing) or '-':28s} {extra:5d} {short:10d} {test:5d}")
    print()
    print(f"  totals: {total_missing} rung files to author · "
          f"{total_extra} rung(s) missing `extra` · {total_lessons} unit(s) short of 3 lessons · "
          f"{total_test} file(s) with test items out of range")
    print(f"  legacy bridges already on disk and mappable: "
          f"{', '.join(f'{k}->{v}' for k, v in LEGACY_BRIDGES.items())}")
    print("\n  The gap, in one line: every published course carries 6 of the 11 CEFR rungs, "
          "no rung carries the `extra` block, and units hold 2 lessons where the schema wants 3-5.")
    print("  Acceptance for PHASE 1 (from the command doc): at least A1-B2 published per language, "
          "500+ words of unique content per level page, voice tags on vocabulary, no templated intros.")
    gaps = total_missing or total_extra or total_lessons or total_test
    if gaps:
        print("\nPHASE 1 OPEN — %d rung file(s), %d extra block(s), %d short unit(s) to author."
              % (total_missing, total_extra, total_lessons))
        return 1 if check else 0
    print("\nPHASE 1 COMPLETE — every published course carries all 11 rungs with `extra` and 3-5 lessons.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

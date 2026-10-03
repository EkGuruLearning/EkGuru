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

The schema cannot see content defects, so one more check lives here: a mistake
entry whose `wrong` text is itself marked correct (`✓`, `(correct)`, `(fine)`) or
whose `why` opens with "Correct as written" / "Both are correct" is a pair the
learner cannot act on — it is counted as a gap.

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


SELF_ASSERTING_WHY = ("correct as written", "both are correct", "both work")
SELF_ASSERTING_WRONG = ("✓", "(correct)", "(fine)", "(both correct)")


def content_defects(code: str, phase: str) -> list[tuple[str, str, str]]:
    """Mistake entries that assert their own `wrong` text is correct."""
    found: list[tuple[str, str, str]] = []
    for rung in RUNGS:
        path = ROOT / f"data/courses/{phase}/{code}_{rung}.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))

        def walk(node, where: str) -> None:
            if isinstance(node, dict):
                if {"wrong", "right", "why"} <= set(node):
                    wrong = str(node["wrong"])
                    why = str(node["why"]).strip().lower()
                    mark = next((m for m in SELF_ASSERTING_WRONG if m in wrong), None)
                    if mark is None and why.startswith(SELF_ASSERTING_WHY):
                        mark = "why:" + why[:28]
                    if mark:
                        found.append((path.name, where, f"{mark} -> {wrong[:70]}"))
                    return
                for key, value in node.items():
                    walk(value, f"{where}/{key}" if where else key)
            elif isinstance(node, list):
                for i, value in enumerate(node):
                    walk(value, f"{where}[{i}]")

        walk(data, "")
    return found


def main() -> int:
    check = "--check" in sys.argv
    codes = published_codes()
    errors = schema_errors(codes)
    print(f"PHASE 1 — content depth for the {len(codes)} published language(s)\n")
    print(f"  {'lang':4s} {'rungs':>7s}  {'missing rungs':28s} {'extra':>5s} {'<3 lessons':>10s} {'test':>5s}")
    total_missing = total_extra = total_lessons = total_test = total_defects = 0
    defects: list[tuple[str, str, str]] = []
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
        found = content_defects(code, phase)
        total_defects += len(found)
        defects.extend((code, *f) for f in found)
        work.append((code, missing))
        print(f"  {code:4s} {len(present):3d}/11  {','.join(missing) or '-':28s} {extra:5d} {short:10d} {test:5d}")
    print()
    for code, name, where, detail in defects:
        print(f"  defect {code} {name} {where}: {detail}")
    print(f"  self-asserting mistake entries (wrong text marked correct): {total_defects}")
    print(f"  totals: {total_missing} rung files to author · "
          f"{total_extra} rung(s) missing `extra` · {total_lessons} unit(s) short of 3 lessons · "
          f"{total_test} file(s) with test items out of range")
    print(f"  legacy bridges already on disk and mappable: "
          f"{', '.join(f'{k}->{v}' for k, v in LEGACY_BRIDGES.items())}")
    print("\n  The gap, in one line: every published course carries 6 of the 11 CEFR rungs, "
          "no rung carries the `extra` block, and units hold 2 lessons where the schema wants 3-5.")
    print("  Acceptance for PHASE 1 (from the command doc): at least A1-B2 published per language, "
          "500+ words of unique content per level page, voice tags on vocabulary, no templated intros.")
    gaps = total_missing or total_extra or total_lessons or total_test or total_defects
    if gaps:
        print("\nPHASE 1 OPEN — %d rung file(s), %d extra block(s), %d short unit(s) to author, "
              "%d content defect(s)." % (total_missing, total_extra, total_lessons, total_defects))
        return 1 if check else 0
    print("\nPHASE 1 COMPLETE — every published course carries all 11 rungs with `extra` and 3-5 lessons.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

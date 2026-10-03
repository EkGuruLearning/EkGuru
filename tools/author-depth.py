# -*- coding: utf-8 -*-
"""PHASE 1 depth author for a published language (the non-Hindi languages).

Hindi was the pilot and has its own hand-written tools. This is the same work
driven by data: every other published course needs

  * `extra` on each of its six CEFR rungs (culture, reading, listening, ten
    idioms, three mistakes, a task) — the schema has always required the block,
  * a third lesson in every unit (the schema asks 3–5; every shipped unit has 2),
  * the five half-step rungs A1+ A2+ B1+ B2+ C1+ (`tools/language-gate.py: RUNGS`),
    authored as *real levels*: the course player fetches
    `data/courses/<phase>/<code>_<level>.json` by name, so the file is playable
    at `/courses/#/<code>/A1+` whether or not a static page exists.

Content lives in `tools/depth-content/<code>.py` (or a same-named package) and
is written with the small DSL in `tools/depth_kit.py`. This tool owns the
machinery: lesson expansion, file shape, manifest sync and drift checks.

Run:  python3 tools/author-depth.py --lang ar            write
      python3 tools/author-depth.py --lang ar --check     report drift
      python3 tools/author-depth.py --lang ar --only extras
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "tools" / "depth-content"

SRS_POLICY = ("Only these four high-value terms are preselected; lesson mistakes and productive "
              "patterns may enter personalized review after an actual error.")
RUNGS = ["A1", "A2", "B1", "B2", "C1", "C2"]
HALF_RUNGS = ["A1+", "A2+", "B1+", "B2+", "C1+"]


# ── content module loading ──────────────────────────────────────────────────

def load_lang(code: str):
    path = CONTENT / f"{code}.py"
    if not path.exists():
        pkg = CONTENT / code / "__init__.py"
        if not pkg.exists():
            raise SystemExit(f"no content module for {code!r}: expected {path} or {pkg}")
        spec = importlib.util.spec_from_file_location(f"depth_{code}", pkg,
                                                     submodule_search_locations=[str(pkg.parent)])
    else:
        spec = importlib.util.spec_from_file_location(f"depth_{code}", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


# ── lesson expansion ────────────────────────────────────────────────────────

def practice_items(spec: dict, name: str, script: str, skill: str) -> list:
    """The twelve exercise types, built from the lesson's own content."""
    title, vocab, gram = spec["title"], spec["vocab"], spec["grammar"]
    ex, dlg = gram["examples"], spec["dialogue"]
    meanings = [v["en"] for v in vocab]
    opts4 = lambda m: [m] + [x for x in meanings if x != m][:3]      # noqa: E731
    opts3 = lambda m: [m] + [x for x in meanings if x != m][:2]      # noqa: E731
    items = [
        ("multiple_choice", "Practice 1: [multiple choice] %s — Choose the meaning of %s (%s) in this lesson."
         % (title, vocab[0]["t"], vocab[0]["r"]), vocab[0]["en"], opts4(vocab[0]["en"])),
        ("fill_in_the_blank", "Practice 2: [fill in the blank] %s — Type the %s expression meaning “%s”."
         % (title, name, vocab[1]["en"]), vocab[1]["t"], None),
        ("translation", "Practice 3: [translation] %s — Interpret the %s in context: %s (%s)."
         % (title, script, ex[0]["t"], ex[0]["r"]), ex[0]["en"], None),
        ("reverse_translation", "Practice 4: [reverse translation] %s — Write in %s: %s."
         % (title, script, ex[1]["en"]), ex[1]["t"], None),
        ("matching", "Practice 5: [matching] %s — Match %s to its lesson meaning." % (title, vocab[2]["t"]),
         vocab[2]["en"], opts3(vocab[2]["en"])),
        ("reorder", "Practice 6: [reorder] %s — Reconstruct the lesson model in coherent %s: %s."
         % (title, name, ex[2]["en"]), ex[2]["t"], None),
        ("sentence_building", "Practice 7: [sentence building] %s — Build the sentence with the lesson pattern (%s): %s."
         % (title, gram["pattern"], ex[0]["en"]), ex[0]["t"], None),
        ("word_selection", "Practice 8: [word selection] %s — Select the %s form for “%s”."
         % (title, name, vocab[3]["en"]), vocab[3]["t"], [vocab[3]["t"]] + [v["t"] for v in vocab[4:]][:2]),
        ("error_correction", "Practice 9: [error correction] %s — Correct the model the lesson warns about: %s"
         % (title, gram["mistakes"][0]["wrong"]), gram["mistakes"][0]["right"], None),
        ("dialogue_completion", "Practice 10: [dialogue completion] %s — Complete the exchange with the studied response to: %s"
         % (title, dlg[0]["en"]), dlg[1]["t"], None),
        ("reading_comprehension", "Practice 11: [reading comprehension] %s — Read “%s” (%s). What does it mean?"
         % (title, dlg[2]["t"], dlg[2]["r"]), dlg[2]["en"], None),
        ("paragraph_comprehension", "Practice 12: [paragraph comprehension] %s — Read the lesson dialogue as a whole and give its key move: %s"
         % (title, dlg[3]["en"]), dlg[3]["t"], None),
    ]
    out = []
    for kind, q, answer, options in items:
        item = {"type": kind, "q": q, "answer": answer, "skill_target": skill or kind.replace("_", " ")}
        if options:
            item["options"] = options
        out.append(item)
    return out


def quiz_items(spec: dict) -> list:
    vocab = spec["vocab"]
    meanings = [v["en"] for v in vocab]
    out = []
    for v in vocab[:5]:
        out.append({"q": "Which meaning best fits %s?" % v["t"],
                    "options": [v["en"]] + [m for m in meanings if m != v["en"]][:3], "answer": 0,
                    "why": "%s (%s) means %s in this lesson." % (v["t"], v["r"], v["en"])})
    return out


def worksheet(spec: dict, script: str) -> dict:
    tasks = list(spec["worksheet"]["tasks"])
    tasks.append({"instruction": ("Integrated offline practice: read the first model, transform or extend it in "
                                  "%s, then rehearse it as a dialogue. Self-check meaning, grammar, and register."
                                  % script),
                  "items": [spec["grammar"]["examples"][0]["t"], spec["dialogue"][0]["t"]],
                  "key": [spec["grammar"]["examples"][0]["en"], spec["dialogue"][0]["en"]]})
    return {"title": spec["worksheet"]["title"], "tasks": tasks}


def build_lesson(uid: str, n: int, spec: dict, name: str, script: str, skill: str) -> dict:
    return {
        "id": "%s-L%d" % (uid, n),
        "title": spec["title"],
        "learn": spec["learn"],
        "vocab": spec["vocab"],
        "grammar": spec["grammar"],
        "dialogue": spec["dialogue"],
        "practice": practice_items(spec, name, script, skill),
        "quiz": quiz_items(spec),
        "flashcards": "auto:vocab",
        "worksheet": worksheet(spec, script),
        "srs_candidates": [v["t"] for v in spec["vocab"][:4]],
        "srs_policy": SRS_POLICY,
    }


# ── surfaces ────────────────────────────────────────────────────────────────

def course_dir(code: str) -> Path:
    hits = sorted(ROOT.glob(f"data/courses/*/{code}_A1.json"))
    if not hits:
        raise SystemExit(f"cannot locate the course directory for {code!r}")
    return hits[0].parent


def write_rungs(mod, cdir: Path, check: bool) -> int:
    name, script = mod.NAME, getattr(mod, "SCRIPT", mod.NAME)
    skill = getattr(mod, "SKILL", "")
    written = stale = 0
    for level in HALF_RUNGS:
        spec = mod.HALFSTEPS.get(level)
        if spec is None:
            print("  %-3s %-4s MISSING in HALFSTEPS (expected a level spec)" % (mod.CODE, level))
            stale += 1
            continue
        path = cdir / f"{mod.CODE}_{level}.json"
        units = []
        for u in spec["units"]:
            lessons = [build_lesson(u["id"], i, l, name, script, skill)
                       for i, l in enumerate(u["lessons"], start=1)]
            units.append({"id": u["id"], "title": u["title"], "lessons": lessons})
        doc = {
            "code": mod.CODE, "name": name, "native": spec.get("native", mod.NATIVE),
            "phase": mod.PHASE, "medium": "en",
            "file_level": level,
            "level": {
                "title": spec["title"],
                "goals": spec["goals"],
                "units": units,
                "test": {"title": "%s %s Checkpoint Test" % (name, level),
                         "items": [{"type": t, "q": q, "answer": a} for t, q, a in spec["test"]]},
                "extra": spec["extra"],
            },
        }
        body = json.dumps(doc, ensure_ascii=False, indent=2)
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old == body:
            print("  %-3s %-4s already current" % (mod.CODE, level))
            continue
        if check:
            print("  %-3s %-4s STALE" % (mod.CODE, level))
            stale += 1
            continue
        path.write_text(body, encoding="utf-8")
        print("  %-3s %-4s written — %d units, %d lessons, %d idioms, %d test items"
              % (mod.CODE, level, len(units), sum(len(u["lessons"]) for u in units),
                 len(spec["extra"]["idioms"]), len(spec["test"])))
        written += 1
    return written + stale


def write_extras(mod, cdir: Path, check: bool) -> int:
    changed = 0
    for rung in RUNGS:
        extra = mod.EXTRAS.get(rung)
        path = cdir / f"{mod.CODE}_{rung}.json"
        if extra is None:
            print("  %-3s %-3s no extra authored yet" % (mod.CODE, rung))
            continue
        if not path.exists():
            raise SystemExit(f"missing course file: {path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        level = data.setdefault("level", {})
        if level.get("extra") == extra:
            print("  %-3s %-3s extra already current" % (mod.CODE, rung))
            continue
        if check:
            print("  %-3s %-3s extra STALE" % (mod.CODE, rung))
            changed += 1
            continue
        level["extra"] = extra
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print("  %-3s %-3s extra written — %d idioms, %d mistakes, reading %d chars, source %s"
              % (mod.CODE, rung, len(extra["idioms"]), len(extra["mistakes"]),
                 len(extra["reading"]["text"]), extra["culture"]["source_url"].split("//")[-1]))
        changed += 1
    return changed


def write_third(mod, cdir: Path, check: bool) -> int:
    name, script = mod.NAME, getattr(mod, "SCRIPT", mod.NAME)
    skill = getattr(mod, "SKILL", "")
    written = 0
    for rung in RUNGS:
        rows = mod.THIRD.get(rung) or []
        for unit_id, lesson_id, spec in rows:
            path = cdir / f"{mod.CODE}_{rung}.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            unit = next((u for u in data["level"]["units"] if u["id"] == unit_id), None)
            if unit is None:
                raise SystemExit(f"{path}: no unit {unit_id}")
            import re as _re
            m = _re.search(r"(\d+)$", lesson_id)
            n = int(m.group(1)) if m else len(unit["lessons"]) + 1
            new = build_lesson(unit_id, n, spec, name, script, skill)
            new["id"] = lesson_id
            existing = next((l for l in unit["lessons"] if l["id"] == lesson_id), None)
            if existing == new:
                print("  %-12s already current (%d lessons)" % (lesson_id, len(unit["lessons"])))
                continue
            if check:
                print("  %-12s STALE" % lesson_id)
                written += 1
                continue
            if existing:
                unit["lessons"][unit["lessons"].index(existing)] = new
            else:
                unit["lessons"].append(new)
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            print("  %-12s %-34s vocab=%d practice=%d quiz=%d — unit now %d lessons"
                  % (lesson_id, new["title"][:34], len(new["vocab"]), len(new["practice"]),
                     len(new["quiz"]), len(unit["lessons"])))
            written += 1
    return written


def sync_manifest(mod, cdir: Path, check: bool) -> int:
    """Files list and per-level lesson counts in data/courses/index.json.

    `build-courses.py` cannot rewrite the manifest while the legacy extension
    files (A3/B3/C3..C5) still fail its filename rules, so the authoring source
    owns these fields — same arrangement as the Hindi pilot.
    """
    path = ROOT / "data/courses/index.json"
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    course = next((c for c in data["courses"] if c.get("code") == mod.CODE), None)
    if course is None:
        print("  index.json: no %s course entry" % mod.CODE)
        return 0 if check else 1
    stale = 0
    on_disk = sorted(p.name for p in cdir.glob(f"{mod.CODE}_*.json"))
    missing = [f for f in on_disk if f not in course.get("files", [])]
    if missing:
        stale += len(missing)
        if check:
            print("  index.json files: missing %s" % ", ".join(missing))
        else:
            course["files"] = sorted(set(course.get("files", [])) | set(missing))
            print("  index.json files: +%s" % ", ".join(missing))
    for rung in RUNGS:
        rung_path = cdir / f"{mod.CODE}_{rung}.json"
        if not rung_path.exists():
            continue
        level = json.loads(rung_path.read_text(encoding="utf-8"))["level"]
        n = sum(len(u["lessons"]) for u in level["units"])
        entry = course.get("levels", {}).get(rung)
        if not isinstance(entry, dict) or entry.get("lessons") == n:
            continue
        if check:
            print("  index.json %s %s: %s -> %s STALE" % (mod.CODE, rung, entry.get("lessons"), n))
            stale += 1
            continue
        entry["lessons"] = n
        print("  index.json %s %s: lessons -> %d" % (mod.CODE, rung, n))
        stale += 1
    if not check and stale:
        out = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
        if out != raw:
            path.write_text(out, encoding="utf-8")
    return stale


# ── main ────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lang", required=True, help="course code, e.g. ar")
    ap.add_argument("--check", action="store_true", help="report drift, write nothing")
    ap.add_argument("--only", choices=["rungs", "extras", "third", "manifest"],
                    help="run one surface only")
    args = ap.parse_args()

    mod = load_lang(args.lang)
    cdir = course_dir(mod.CODE)
    todo = args.only
    changed = 0
    if todo in (None, "rungs"):
        changed += write_rungs(mod, cdir, args.check)
    if todo in (None, "extras"):
        changed += write_extras(mod, cdir, args.check)
    if todo in (None, "third"):
        changed += write_third(mod, cdir, args.check)
    if todo in (None, "manifest"):
        changed += sync_manifest(mod, cdir, args.check)
    print("%s: %d change(s)" % ("CHECK" if args.check else "written", changed))
    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Repository checks for the generated world-course quiz content and bindings."""
from __future__ import annotations

import html
import importlib.util
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))


def load_world_builder():
    path = ROOT / "tools/build-world-course.py"
    spec = importlib.util.spec_from_file_location("world_course_quiz_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load world-course builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generated_body(builder, course, method="build_quiz"):
    captured = []
    original_write_page = builder.write_page
    builder.write_page = lambda *args, **kwargs: captured.append((args, kwargs))
    try:
        getattr(builder, method)(builder.cfg_of(course))
    finally:
        builder.write_page = original_write_page
    if len(captured) != 1 or len(captured[0][0]) < 7:
        raise RuntimeError(f"builder did not produce one body for {course.COURSE['lang']}")
    return captured[0][0][6]


def load_course(path: Path):
    spec = importlib.util.spec_from_file_location("quiz_course_" + path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load course data: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def visible_text(page: str) -> str:
    without_scripts = re.sub(r"<script\b[^>]*>[\s\S]*?</script\s*>", " ", page, flags=re.I)
    without_styles = re.sub(r"<style\b[^>]*>[\s\S]*?</style\s*>", " ", without_scripts, flags=re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", without_styles))).strip()


def main() -> int:
    errors: list[str] = []
    course_files = sorted((ROOT / "tools/course-data").glob("*.py"))
    course_files = [path for path in course_files if path.name != "__init__.py"]
    builder = load_world_builder()

    for path in course_files:
        course = load_course(path)
        code = course.COURSE["lang"]
        name = course.COURSE["name"]
        jsvar = "EKGURU_COURSE_" + code.upper()
        page_path = ROOT / "languages" / code / "quiz/index.html"
        if not page_path.exists():
            errors.append(f"{code}: generated quiz page is missing")
            continue

        page = page_path.read_text(encoding="utf-8")
        text = visible_text(page)
        try:
            source_body = generated_body(builder, course)
            body_start = source_body.index('<p class="lede">Practise with the ')
            body_end = source_body.index("</script>", body_start) + len("</script>")
            generated_fragment = source_body[body_start:body_end]
            if generated_fragment not in page:
                errors.append(f"{code}: generated quiz body is stale compared with its source builder")
        except (RuntimeError, ValueError, IndexError) as exc:
            errors.append(f"{code}: unable to verify builder output: {exc}")
        hub_path = ROOT / "languages" / code / "course/index.html"
        if hub_path.exists():
            hub = hub_path.read_text(encoding="utf-8")
            if "20 multiple-choice questions with explanations; the set rotates daily." in hub:
                errors.append(f"{code}: course hub still implies 20 questions per selected quiz")
            hub_summary = f"{len(course.QUIZ)} questions across lesson topics; available round lengths vary by topic."
            if hub_summary not in hub:
                errors.append(f"{code}: course hub quiz summary is not aligned with available topic counts")
            try:
                generated_hub = generated_body(builder, course, "build_course_hub")
                if hub_summary not in generated_hub:
                    errors.append(f"{code}: course-hub source does not report the bank size")
            except (RuntimeError, KeyError) as exc:
                errors.append(f"{code}: unable to verify course-hub builder output: {exc}")
        scripts = "\n".join(re.findall(r"<script\b[^>]*>([\s\S]*?)</script\s*>", page, flags=re.I))
        quiz_scripts = [script for script in re.findall(r"<script\b[^>]*>([\s\S]*?)</script\s*>", page, flags=re.I)
                        if "function escText" in script]
        if not quiz_scripts:
            errors.append(f"{code}: generated quiz script is missing")
        elif shutil.which("node"):
            parsed = subprocess.run(["node", "--check", "-"], input=quiz_scripts[0], text=True, capture_output=True)
            if parsed.returncode:
                errors.append(f"{code}: quiz JavaScript does not parse: {parsed.stderr.strip()}")
        else:
            errors.append("Node.js is required to parse generated quiz scripts")
        if "EKGURU_COURSE_" in text:
            errors.append(f"{code}: an internal course-bank identifier is visible in page copy")
        if f"How the {name} quiz works" not in text:
            errors.append(f"{code}: quiz copy does not use the language name")
        if "Question bank by topic" not in text:
            errors.append(f"{code}: page is missing the question-bank map")
        if f"window.{jsvar}.quiz" not in scripts or f"if (window.{jsvar}) init()" not in scripts:
            errors.append(f"{code}: quiz runtime is not bound to its course bank")
        for element_id in ("q-topic", "q-n", "q-start", "q-fb", "q-next"):
            if f"{code}-{element_id}" not in page:
                errors.append(f"{code}: expected quiz control/feedback id {code}-{element_id} is missing")
        if f"/languages/{code}/lessons/" not in scripts:
            errors.append(f"{code}: answer feedback does not link to its source lesson")
        if "Round complete." not in scripts:
            errors.append(f"{code}: round completion does not report the learner's score")

        questions = course.QUIZ
        counts = Counter(str(q.get("topic") or "general") for q in questions)
        if sum(counts.values()) != len(questions):
            errors.append(f"{code}: topic map does not cover the complete quiz bank")
        for topic, count in counts.items():
            label = topic.replace("_", " ").replace("-", " ").title()
            if label not in text or f"{count} question" not in text:
                errors.append(f"{code}: topic map is missing {label} or its {count}-question count")
        for lesson_slug in {q.get("lesson") for q in questions if q.get("lesson")}:
            expected_link = f'href="/languages/{code}/lessons/{lesson_slug}/"'
            if expected_link not in page:
                errors.append(f"{code}: question-bank map is missing source lesson {lesson_slug}")

    if errors:
        print(f"FAIL world-course quiz content ({len(errors)} issue(s)):")
        for error in errors:
            print(" - " + error)
        return 1

    print(f"PASS world-course quiz content and course-bank bindings: {len(course_files)} course pages checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

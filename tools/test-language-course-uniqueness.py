#!/usr/bin/env python3
"""Guard against identical beginner introductions across Indian language courses.

The course pages are generated from tools/lang-data/*.json. This test exercises
that generator function directly, so no generated HTML needs hand editing.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUGS = (
    "bengali", "gujarati", "kannada", "malayalam", "marathi",
    "punjabi", "tamil", "telugu", "urdu",
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    course = load_module("build_language_course", ROOT / "tools/build-language-course.py")
    audit = load_module("audit_adsense_readiness", ROOT / "tools/audit-adsense-readiness.py")
    intros: dict[str, str] = {}
    errors: list[str] = []

    for slug in SLUGS:
        path = ROOT / "tools/lang-data" / f"{slug}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        generated_section = course.deep_beginner(data)
        paragraphs = audit.content_paragraphs(generated_section)
        if not paragraphs:
            errors.append(f"{slug}: no substantial opening paragraph")
            continue
        signatures = [audit.signature(paragraph) for paragraph in paragraphs]
        if len(signatures) != len(set(signatures)):
            errors.append(f"{slug}: duplicate substantial paragraphs within beginner content")
        intro = paragraphs[0]
        greeting = (data.get("greetings") or [{}])[0]
        target = audit.norm(greeting.get("t") or "")
        roman = audit.norm(greeting.get("r") or "")
        script_note = audit.norm(data.get("script_note") or "")
        if not target or target not in intro:
            errors.append(f"{slug}: opening paragraph omits its authored greeting")
        if not roman or roman not in intro:
            errors.append(f"{slug}: opening paragraph omits its authored reading")
        if not script_note or script_note not in intro:
            errors.append(f"{slug}: opening paragraph omits its language-specific script note")

        page_path = ROOT / "learn" / slug / "beginner" / "index.html"
        if not page_path.is_file():
            errors.append(f"{slug}: generated beginner page is missing")
        else:
            page = page_path.read_text(encoding="utf-8")
            start = "<h2>Your first 30 days, week by week</h2>"
            end = "<h2>More guides in this course</h2>"
            if page.count(start) != 1 or page.count(end) != 1 or page.index(start) >= page.index(end):
                errors.append(f"{slug}: generated beginner section boundaries are missing or ambiguous")
            else:
                actual_section = page[page.index(start):page.index(end)]
                if audit.content_paragraphs(actual_section) != paragraphs:
                    errors.append(f"{slug}: page copy is stale versus the beginner generator")
                table_start = actual_section.find("<table")
                table_end = actual_section.find("</table>", table_start) if table_start >= 0 else -1
                table = actual_section[table_start:table_end + 8] if table_end >= 0 else ""
                labels = ("English", "Hindi", data["name"], "Say it")
                if not table or any(f'data-h="{label}"' not in table for label in labels):
                    errors.append(f"{slug}: first-greetings table is missing accessible column labels")
        intros[slug] = audit.signature(intro)

    collisions: dict[str, list[str]] = {}
    by_signature: dict[str, list[str]] = {}
    for slug, signature in intros.items():
        by_signature.setdefault(signature, []).append(slug)
    collisions = {signature: slugs for signature, slugs in by_signature.items() if len(slugs) > 1}
    if collisions:
        errors.append("duplicate beginner introductions: " + "; ".join(",".join(v) for v in collisions.values()))

    if errors:
        for error in errors:
            print("FAIL", error)
        return 1
    print(f"PASS: {len(intros)} Indian beginner introductions are distinct and use authored greeting/script data")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

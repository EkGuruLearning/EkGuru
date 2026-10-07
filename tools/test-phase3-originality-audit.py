#!/usr/bin/env python3
"""Integrity and non-fabrication checks for the master-command Phase 3 audit."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "data/quality/phase3-originality-audit.json"
PHASE2_PATH = ROOT / "data/quality/phase2-content-inventory.json"
TOOL_PATH = ROOT / "tools/build-phase3-originality-audit.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("phase3_originality_builder", TOOL_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import Phase 3 audit builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    errors: list[str] = []
    try:
        report = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
        phase2 = json.loads(PHASE2_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("FAIL cannot load audit inputs:", exc)
        return 1

    source_rows = phase2.get("pages", [])
    pages = report.get("pages", [])
    if len(pages) != len(source_rows):
        errors.append(f"expected {len(source_rows)} page rows, found {len(pages)}")
    source_paths = {row.get("source_file") for row in source_rows}
    audit_paths = [row.get("source_file") for row in pages]
    if set(audit_paths) != source_paths or len(audit_paths) != len(set(audit_paths)):
        errors.append("audit page paths do not exactly cover the Phase 2 inventory")

    required_questions = {
        "1_useful_question_answered",
        "2_ekguru_specific_value_vs_generic_alternative",
        "3_original_examples",
        "4_practical_task_user_can_complete",
        "5_mistakes_explained",
        "6_learner_context",
        "7_original_exercise_or_tool",
        "8_source_and_fact_verification_needed",
        "9_natural_and_specific_wording",
        "10_template_or_keyword_swapped_content",
    }
    for page in pages:
        label = page.get("source_file", "<unknown>")
        questions = page.get("master_command_questions", {})
        if set(questions) != required_questions:
            errors.append(f"{label}: master-command question set is incomplete")
        if page.get("human_editorial_review_status") != "NOT_PERFORMED":
            errors.append(f"{label}: human review status was overstated")
        if page.get("native_language_review_status") != "NOT_PERFORMED":
            errors.append(f"{label}: native-language review status was overstated")
        if page.get("source_fact_verification_status") != "NOT_PERFORMED":
            errors.append(f"{label}: source/fact verification was overstated")
        if page.get("external_similarity_check_status") != "NOT_PERFORMED":
            errors.append(f"{label}: external similarity review was overstated")
        if page.get("destructive_or_publication_change_performed") is not False:
            errors.append(f"{label}: audit claims a content or publication change")
        q8 = questions.get("8_source_and_fact_verification_needed", {})
        if q8.get("status") != "NOT_VERIFIED":
            errors.append(f"{label}: source verification is not clearly pending")
        q9 = questions.get("9_natural_and_specific_wording", {})
        if q9.get("status") != "HUMAN_LANGUAGE_REVIEW_REQUIRED":
            errors.append(f"{label}: wording review is not explicitly assigned to an editor")

    summary = report.get("summary", {})
    if summary.get("public_pages") != len(source_rows):
        errors.append("summary page count disagrees with Phase 2")
    if summary.get("human_editorial_reviews_completed") != 0:
        errors.append("summary claims completed human editorial reviews")
    if summary.get("native_language_reviews_completed") != 0:
        errors.append("summary claims completed native-language reviews")
    if summary.get("source_fact_checks_completed") != 0:
        errors.append("summary claims completed source checks")
    if summary.get("external_similarity_checks_completed") != 0:
        errors.append("summary claims completed external comparison")
    if summary.get("content_or_indexation_changes_performed") != 0:
        errors.append("summary claims content or indexation changes")

    # Regression: this is visible page copy, not merely an implementation
    # identifier in script, and the triage must retain it for editor attention.
    arabic_quiz = next((p for p in pages if p.get("source_file") == "languages/ar/quiz/index.html"), None)
    if not arabic_quiz:
        errors.append("Arabic quiz page is missing from the audit")
    else:
        signals = arabic_quiz["repository_evidence"]["structural_signals"]
        if "EKGURU_COURSE_AR" not in signals.get("unresolved_template_token_candidates", []):
            errors.append("visible Arabic quiz course-code token was not surfaced for review")
        if "visible_unresolved_template_token_candidate" not in arabic_quiz.get("automated_flags", []):
            errors.append("visible token candidate has no review flag")

    # Synthetic extraction regression: chrome should not be sampled as content,
    # but visible examples, a mistake heading, controls and unresolved tokens should.
    builder = load_builder()
    synthetic = """<!doctype html><main>
      <p data-eg-chrome=\"review\">Draft review banner must not enter the excerpt.</p>
      <h1>Hindi question words</h1>
      <p>Hindi uses अलग question words, and each word takes a useful place in an ordinary sentence for a learner.</p>
      <h2>Common mistakes</h2><table><tr><td>कहाँ</td><td>where</td></tr></table>
      <form><input name=\"q\"><button>Check</button></form>
      <p>The EKGURU_COURSE_AR lesson bank supplies the examples and feedback for this practice round.</p>
    </main>"""
    features = builder.extract_features(synthetic)
    if any("Draft review banner" in str(x) for x in features["paragraphs_for_signatures"]):
        errors.append("editorial chrome leaked into the synthetic content sample")
    if not features["mistake_headings"] or features["table_count"] != 1:
        errors.append("mistake/example structural signals were not detected")
    if features["form_count"] != 1 or features["button_count"] != 1:
        errors.append("interactive controls were not detected")
    if "EKGURU_COURSE_AR" not in features["unresolved_template_token_candidates"]:
        errors.append("visible unresolved token was not detected")

    if errors:
        print(f"FAIL Phase 3 originality audit ({len(errors)} issue(s)):")
        for error in errors[:80]:
            print(" - " + error)
        return 1
    print(
        f"PASS Phase 3 audit integrity: {len(pages)} pages, ten questions per page, "
        "repository signals only; human/source/native/external review remains unclaimed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

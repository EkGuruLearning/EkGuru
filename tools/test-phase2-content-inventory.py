#!/usr/bin/env python3
"""Integrity checks for the Phase 2 repository-only content inventory."""
from __future__ import annotations

import html
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
REPORT = ROOT / "data/quality/phase2-content-inventory.json"
sys.path.insert(0, str(TOOLS))


def load_tool_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    audit = load_tool_module("phase2_inventory_audit", TOOLS / "audit-adsense-readiness.py")
    links = load_tool_module("phase2_inventory_links", TOOLS / "build-full-page-inventory.py")
    errors: list[str] = []
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    pages = report.get("pages") or []
    expected_paths = {p.relative_to(ROOT).as_posix() for p in audit.html_files()}
    actual_paths = {p.get("source_file") for p in pages}
    full_report = json.loads((ROOT / "data/quality/full-page-inventory.json").read_text(encoding="utf-8"))
    full_map = {page.get("source_file"): page for page in full_report.get("pages", [])}
    if set(full_map) != expected_paths:
        errors.append("technical full-page inventory does not match public HTML scope")
    if actual_paths != expected_paths:
        errors.append(f"inventory coverage differs: expected {len(expected_paths)}, got {len(actual_paths)}")
    if len(actual_paths) != len(pages):
        errors.append("duplicate source_file rows")
    if report.get("phase") != 2:
        errors.append("report is not marked as Phase 2")
    if "LIVE_HTTP_CRAWL_PENDING" not in str(report.get("phase_status")):
        errors.append("report does not disclose that live HTTP crawling is pending")

    required = {
        "url", "source_file", "page_type", "page_class", "language", "title", "meta_description", "h1",
        "h1_count", "word_count", "visible_text_length", "unique_text_ratio", "template_text_ratio",
        "internal_inlinks", "internal_outlinks", "author", "last_updated", "schema", "canonical",
        "robots", "http_status", "orphan", "similarity_group", "content_quality_score",
        "adsense_risk", "action",
    }
    seen_urls: set[str] = set()
    actions = {"KEEP", "IMPROVE", "MERGE", "NOINDEX", "REMOVE"}
    for page in pages:
        rel = page.get("source_file")
        if not rel or not (ROOT / rel).is_file():
            errors.append(f"missing repository source file: {rel}")
            continue
        missing = sorted(required - page.keys())
        if missing:
            errors.append(f"{rel}: missing fields {missing}")
        if rel not in full_map:
            errors.append(f"{rel}: missing from technical full-page inventory")
        else:
            if page.get("canonical") != full_map[rel].get("canonical"):
                errors.append(f"{rel}: canonical differs between the two inventories")
            if page.get("internal_inlinks") != full_map[rel].get("inbound_link_count"):
                errors.append(f"{rel}: inlink count differs between the two inventories")
            if page.get("internal_outlinks") != full_map[rel].get("internal_link_count"):
                errors.append(f"{rel}: outlink count differs between the two inventories")
        source = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        canonical_tag = links.RE_CANON.search(source)
        canonical_href = links.RE_HREF.search(canonical_tag.group(0)) if canonical_tag else None
        if canonical_href and page.get("canonical") != html.unescape(canonical_href.group(1)).strip():
            errors.append(f"{rel}: canonical was not read from the link href")
        if page.get("url") in seen_urls:
            errors.append(f"duplicate URL: {page.get('url')}")
        seen_urls.add(page.get("url"))
        if page.get("http_status") is not None or page.get("http_status_source") != "not fetched; repository-only inventory":
            errors.append(f"{rel}: fabricated or ambiguous live HTTP status")
        for field in ("unique_text_ratio", "template_text_ratio"):
            value = page.get(field)
            if not isinstance(value, (int, float)) or not 0 <= value <= 1:
                errors.append(f"{rel}: invalid {field}={value!r}")
        score = page.get("content_quality_score")
        if not isinstance(score, int) or not 0 <= score <= 100:
            errors.append(f"{rel}: invalid mechanical score {score!r}")
        if page.get("content_quality_score_is_editorial_rating") is not False:
            errors.append(f"{rel}: score is not clearly distinguished from editorial review")
        if page.get("action") not in actions or page.get("action_is_recommendation_only") is not True:
            errors.append(f"{rel}: missing safe, non-destructive action recommendation")
        if page.get("action") == "REMOVE":
            errors.append(f"{rel}: Phase 2 must not recommend removal automatically")
        if page.get("orphan") != (page.get("internal_inlinks") == 0):
            errors.append(f"{rel}: orphan state disagrees with measured internal inlinks")
        if page.get("indexable") is False and page.get("action") != "NOINDEX":
            errors.append(f"{rel}: current noindex state is not preserved in the recommendation")
        if page.get("indexable") is True and page.get("action") == "NOINDEX":
            errors.append(f"{rel}: recommendation would change current indexation without evidence")

    summary = report.get("summary") or {}
    if summary.get("repository_html_pages") != len(pages):
        errors.append("summary page count does not match rows")
    if summary.get("http_status_checked") != 0 or summary.get("http_status_pending") != len(pages):
        errors.append("summary misstates live HTTP coverage")
    if summary.get("pages_recommended_for_removal") != 0:
        errors.append("summary recommends removing content")
    if errors:
        for error in errors[:50]:
            print("FAIL", error)
        if len(errors) > 50:
            print(f"FAIL ... and {len(errors) - 50} additional issues")
        return 1
    print(f"PASS: {len(pages)} public HTML pages inventoried; HTTP status is honestly pending; no removals recommended")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

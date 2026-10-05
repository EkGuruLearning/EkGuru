#!/usr/bin/env python3
"""Build the Phase 3 repository-backed originality review matrix.

This is NOT a human/native-speaker audit, plagiarism scan, AI detector, or
content approval. It records page evidence and reproducible triage signals so
an editor can review the important pages without inventing answers to the
master-command questions.

Run:
  python3 tools/build-phase3-originality-audit.py
  python3 tools/build-phase3-originality-audit.py --check
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PHASE2 = ROOT / "data/quality/phase2-content-inventory.json"
OUT = ROOT / "data/quality/phase3-originality-audit.json"

CONTENT_TYPES = {
    "answer", "guide_or_article", "language_course", "language_lesson",
    "language_level", "language_practice", "learning_content",
    "language_hub_or_tool",
}

# This is the same shared-chrome boundary used by the repository AdSense
# paragraph audit. Shared chrome is not editorial body copy.
CHROME = re.compile(
    r"<!--\s*ekguru:(?:shell-header|shell-footer|trust-footer|pw-bands):start\s*-->[\s\S]*?"
    r"<!--\s*ekguru:(?:shell-header|shell-footer|trust-footer|pw-bands):end\s*-->"
    r"|<header\b[\s\S]*?</header>|<footer\b[\s\S]*?</footer>"
    r"|<nav\b[\s\S]*?</nav>"
    r"|<p\b(?=[^>]*\bdata-eg-chrome=(?:\"[^\"]*\"|'[^']*'))[^>]*>[\s\S]*?</p>"
    r"|<p class=\"[^\"]*\bhint\b[^\"]*\"[^>]*>[\s\S]*?</p>"
    r"|<p class=\"[^\"]*\b(?:crumbs?|upd|updated|dateline|meta|byline|xp-tutor-teaches)\b[^\"]*\"[^>]*>[\s\S]*?</p>"
    r"|<aside\b[^>]*(?:class=\"[^\"]*pg-note[^\"]*\"|role=\"note\")[^>]*>[\s\S]*?</aside>"
    r"|<aside\b[^>]*class=\"(?:pg-)?cta(?:-box)?\b[^\"]*\"[^>]*>[\s\S]*?</aside>",
    re.I,
)
HIDDEN_BLOCKS = re.compile(
    r"<(script|style|noscript|template|svg|canvas)\b[^>]*>[\s\S]*?</\1\s*>", re.I
)
MAIN = re.compile(r"<main\b[^>]*>([\s\S]*?)</main\s*>", re.I)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
HIDDEN_TAGS = {"script", "style", "noscript", "template", "svg", "canvas"}
BLOCK_TAGS = {"h1", "h2", "h3", "p", "li"}

SCRIPT_CHARS = re.compile(
    r"[\u0530-\u058f\u0590-\u08ff\u0900-\u0dff\u0e00-\u0e7f"
    r"\u0e80-\u0eff\u1000-\u109f\u1780-\u17ff\u3040-\u30ff"
    r"\u3400-\u9fff\uac00-\ud7af]"
)
MISTAKE_HEADING = re.compile(r"mistake|error|trap|wrong|confus|pitfall|false friend", re.I)
EXAMPLE_HEADING = re.compile(r"example|dialogue|conversation|sentence|phrase|vocabulary|word|practice|quiz|exercise|table", re.I)
AUDIENCE_TERMS = {
    "beginner": re.compile(r"\bbeginner|\bfirst[- ]time learner", re.I),
    "intermediate": re.compile(r"\bintermediate\b", re.I),
    "advanced": re.compile(r"\badvanced\b|\bproficient\b", re.I),
    "Hindi-speaking learner": re.compile(r"\bhindi[- ]speaking|\bhindi speaker|\bfrom hindi\b", re.I),
    "heritage learner": re.compile(r"\bheritage\b", re.I),
    "traveller/visitor": re.compile(r"\btravell?er|\btourist|\bvisitor\b", re.I),
    "children/families": re.compile(r"\bchildren\b|\bkids\b|\bfamily\b", re.I),
    "professional/business": re.compile(r"\bprofessional\b|\bbusiness\b|\boffice\b", re.I),
}
PRACTICE_HREF = re.compile(r"(?:practice|quiz|flashcards?|worksheets?|typing|conversation|toolbox|courses?)(?:/|#|$)", re.I)
PERSONAL_CLAIM_CANDIDATE = re.compile(
    r"\b(?:as a native speaker|as a language expert|as a linguist|as a teacher|"
    r"in my \d+ years|my students|my classroom|I have taught)\b", re.I
)
UNRESOLVED_TEMPLATE_TOKEN = re.compile(
    r"\b(?:EKGURU_COURSE_[A-Z0-9_]+|language_word(?:_\d+)?|word_\d+|lesson_\d+)\b|"
    r"\{\{\s*[^{}]{1,80}\s*\}\}", re.I
)


def norm(text: str) -> str:
    return re.sub(r"[^\w]+", " ", html.unescape(text).lower()).strip()


def paragraph_signature(text: str) -> str:
    normalized = norm(text)
    normalized = re.sub(r"\b\d+(?: \d+)*\b", "#", normalized)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:20]


def clean_fragment(fragment: str) -> str:
    fragment = re.sub(r"<!--.*?-->", " ", fragment, flags=re.S)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(fragment)).strip()


class BodySignals(HTMLParser):
    """Small visible-body parser for excerpts and structural signals."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, bool]] = []
        self.blocks: list[dict[str, object]] = []
        self.text_parts: list[str] = []
        self.tag_counts: Counter[str] = Counter()
        self.hrefs: list[str] = []
        self.citation_elements = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        inherited_hidden = self.stack[-1][1] if self.stack else False
        classes = set((attr.get("class") or "").split())
        own_hidden = (
            tag in HIDDEN_TAGS
            or "data-eg-chrome" in attr
            or bool(classes & {"crumb", "crumbs", "eg-byline", "eg-review-notice", "eg-voice-note", "upd", "dateline"})
        )
        hidden = inherited_hidden or own_hidden
        if not hidden:
            self.tag_counts[tag] += 1
            if tag == "cite":
                self.citation_elements += 1
            if tag == "a" and attr.get("href"):
                self.hrefs.append(str(attr["href"]).strip())
            if tag in BLOCK_TAGS:
                self.blocks.append({"tag": tag, "parts": []})
        if tag not in VOID:
            self.stack.append((tag, hidden))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        match = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                match = i
                break
        if match is None:
            return
        popped = self.stack[match:]
        for block_tag, hidden in reversed(popped):
            if not hidden and block_tag in BLOCK_TAGS:
                for j in range(len(self.blocks) - 1, -1, -1):
                    if self.blocks[j]["tag"] == block_tag:
                        block = self.blocks.pop(j)
                        text = re.sub(r"\s+", " ", "".join(block["parts"])).strip()
                        if text:
                            self._record_block(str(block_tag), text)
                        break
        del self.stack[match:]

    def _record_block(self, tag: str, text: str) -> None:
        if not hasattr(self, "headings"):
            self.headings: list[tuple[str, str]] = []
            self.paragraphs: list[str] = []
            self.list_items: list[str] = []
        if tag in {"h1", "h2", "h3"}:
            self.headings.append((tag, text))
        elif tag == "p":
            self.paragraphs.append(text)
        elif tag == "li":
            self.list_items.append(text)

    def handle_data(self, data: str) -> None:
        if self.stack and self.stack[-1][1]:
            return
        if not self.stack:
            return
        self.text_parts.append(data)
        for block in self.blocks:
            block["parts"].append(data)

    def result(self) -> dict[str, object]:
        headings = getattr(self, "headings", [])
        paragraphs = getattr(self, "paragraphs", [])
        list_items = getattr(self, "list_items", [])
        body_text = re.sub(r"\s+", " ", " ".join(self.text_parts)).strip()
        return {
            "headings": headings,
            "paragraphs": paragraphs,
            "list_items": list_items,
            "body_text": body_text,
            "tag_counts": dict(self.tag_counts),
            "hrefs": self.hrefs,
            "citation_elements": self.citation_elements,
        }


def extract_features(raw: str) -> dict[str, object]:
    """Extract visible main-body text and conservative structural evidence."""
    clean = CHROME.sub(" ", raw)
    clean = HIDDEN_BLOCKS.sub(" ", clean)
    main = MAIN.search(clean)
    body = main.group(1) if main else clean
    parser = BodySignals()
    parser.feed(body)
    data = parser.result()
    paragraphs = [str(p) for p in data["paragraphs"]]
    substantial = [p for p in paragraphs if len(norm(p).split()) >= 12]
    headings = data["headings"]
    h1 = [text for tag, text in headings if tag == "h1"]
    h2h3 = [text for tag, text in headings if tag in {"h2", "h3"}]
    body_text = str(data["body_text"])
    signals = {
        "paragraph_count": len(paragraphs),
        "substantial_paragraph_count": len(substantial),
        "h2_count": sum(1 for tag, _ in headings if tag == "h2"),
        "h3_count": sum(1 for tag, _ in headings if tag == "h3"),
        "table_count": int(data["tag_counts"].get("table", 0)),
        "list_count": int(data["tag_counts"].get("ul", 0)) + int(data["tag_counts"].get("ol", 0)),
        "list_item_count": int(data["tag_counts"].get("li", 0)),
        "figure_count": int(data["tag_counts"].get("figure", 0)),
        "blockquote_count": int(data["tag_counts"].get("blockquote", 0)),
        "pre_or_code_count": int(data["tag_counts"].get("pre", 0)) + int(data["tag_counts"].get("code", 0)),
        "form_count": int(data["tag_counts"].get("form", 0)),
        "button_count": int(data["tag_counts"].get("button", 0)),
        "input_count": int(data["tag_counts"].get("input", 0)),
        "select_count": int(data["tag_counts"].get("select", 0)),
        "textarea_count": int(data["tag_counts"].get("textarea", 0)),
        "citation_element_count": int(data["citation_elements"]),
        "non_latin_script_character_count": len(SCRIPT_CHARS.findall(body_text)),
        "mistake_headings": [h for h in h2h3 if MISTAKE_HEADING.search(h)][:8],
        "example_or_task_headings": [h for h in h2h3 if EXAMPLE_HEADING.search(h)][:12],
        "audience_context_signals": [name for name, pattern in AUDIENCE_TERMS.items() if pattern.search(body_text)][:8],
        "practice_or_tool_links": [href for href in data["hrefs"] if PRACTICE_HREF.search(urlparse(href).path + urlparse(href).fragment)][:8],
        "personal_experience_claim_candidates": [m.group(0) for m in PERSONAL_CLAIM_CANDIDATE.finditer(body_text)][:5],
        "unresolved_template_token_candidates": sorted({m.group(0) for m in UNRESOLVED_TEMPLATE_TOKEN.finditer(body_text)})[:12],
        "opening_excerpt": substantial[0][:320] if substantial else None,
        "closing_excerpt": substantial[-1][:320] if substantial else None,
        "heading_sample": h2h3[:10],
        "h1_from_body": h1[0] if h1 else None,
        "paragraphs_for_signatures": substantial,
    }
    return signals


def priority_for(row: dict) -> tuple[str, str]:
    if row.get("indexable"):
        risk = row.get("adsense_risk")
        if risk == "HIGH":
            return "P1_REVIEW", "Current Phase 2 HIGH automated triage; editorial review required."
        if risk == "MEDIUM":
            return "P2_REVIEW", "Current Phase 2 MEDIUM automated triage; editorial review required."
        return "P3_CONFIRM", "Current Phase 2 LOW automated triage; confirm specific learner value and evidence."
    if row.get("page_type") in CONTENT_TYPES and int(row.get("word_count") or 0) >= 100:
        return "HELD_NOINDEX_CONTENT", "Preserve current noindex; review before any publication/indexation change."
    return "NOINDEX_UTILITY_OR_PLACEHOLDER", "No editorial promotion is recommended; preserve current technical state."


def page_row(row: dict, feature: dict, intro_groups: dict[str, set[str]], para_groups: dict[str, set[str]]) -> dict:
    path = row["source_file"]
    priority, next_step = priority_for(row)
    paragraphs = feature["paragraphs_for_signatures"]
    sigs = sorted({paragraph_signature(p) for p in paragraphs})
    repeated = [s for s in sigs if len(para_groups.get(s, set())) >= 3]
    first_sig = paragraph_signature(paragraphs[0]) if paragraphs else None
    shared_intro = first_sig if first_sig and len(intro_groups.get(first_sig, set())) > 1 else None

    flags = list(row.get("risk_flags") or [])
    if shared_intro:
        flags.append("shared_opening_paragraph_signature")
    if repeated:
        flags.append("shared_paragraph_signatures_present")
    if feature["personal_experience_claim_candidates"]:
        flags.append("first_person_experience_claim_candidate_requires_review")
    if feature["unresolved_template_token_candidates"]:
        flags.append("visible_unresolved_template_token_candidate")
    if feature["non_latin_script_character_count"] > 0:
        flags.append("non_latin_script_text_present_not_an_originality_claim")

    practice_signals = {
        "interactive_controls": sum(int(feature[k]) for k in ("form_count", "button_count", "input_count", "select_count", "textarea_count")),
        "practice_or_tool_links": feature["practice_or_tool_links"],
        "task_or_example_headings": feature["example_or_task_headings"],
        "list_items": feature["list_item_count"],
    }
    example_signals = {
        "tables": feature["table_count"],
        "figures": feature["figure_count"],
        "blockquote_elements": feature["blockquote_count"],
        "pre_or_code_elements": feature["pre_or_code_count"],
        "non_latin_script_characters": feature["non_latin_script_character_count"],
        "example_or_task_headings": feature["example_or_task_headings"],
    }
    template_signals = {
        "unique_text_ratio": row.get("unique_text_ratio"),
        "template_text_ratio": row.get("template_text_ratio"),
        "phase2_similarity_groups": row.get("similarity_group") or [],
        "shared_intro_signature": shared_intro,
        "shared_paragraph_signature_count": len(repeated),
        "shared_paragraph_signature_ids": repeated[:20],
        "visible_unresolved_template_tokens": feature["unresolved_template_token_candidates"],
    }

    questions = {
        "1_useful_question_answered": {
            "status": "CANDIDATE_FROM_PAGE_LABEL_ONLY",
            "candidate": row.get("h1") or row.get("title"),
            "basis": "H1/title are intent hints, not proof the page answers the question.",
        },
        "2_ekguru_specific_value_vs_generic_alternative": {
            "status": "HUMAN_COMPARISON_REQUIRED",
            "repository_signals": {
                "page_type": row.get("page_type"),
                "language": row.get("language"),
                "unique_text_ratio": row.get("unique_text_ratio"),
                "interactive_control_count": practice_signals["interactive_controls"],
            },
        },
        "3_original_examples": {
            "status": "STRUCTURAL_SIGNALS_ONLY_ORIGINALITY_UNVERIFIED",
            "signals": example_signals,
        },
        "4_practical_task_user_can_complete": {
            "status": "STRUCTURAL_SIGNALS_ONLY",
            "signals": practice_signals,
        },
        "5_mistakes_explained": {
            "status": "KEYWORD_SIGNAL_ONLY",
            "matching_headings": feature["mistake_headings"],
        },
        "6_learner_context": {
            "status": "KEYWORD_AND_SCRIPT_SIGNALS_ONLY",
            "signals": feature["audience_context_signals"],
            "non_latin_script_character_count": feature["non_latin_script_character_count"],
        },
        "7_original_exercise_or_tool": {
            "status": "STRUCTURAL_SIGNALS_ONLY_ORIGINALITY_UNVERIFIED",
            "signals": practice_signals,
        },
        "8_source_and_fact_verification_needed": {
            "status": "NOT_VERIFIED",
            "external_outlinks_in_phase2_inventory": row.get("external_outlinks"),
            "citation_elements_in_body": feature["citation_element_count"],
            "note": "Link/citation presence is not source verification; no external fact check was performed.",
        },
        "9_natural_and_specific_wording": {
            "status": "HUMAN_LANGUAGE_REVIEW_REQUIRED",
        },
        "10_template_or_keyword_swapped_content": {
            "status": "HEURISTIC_TRIAGE_ONLY_NOT_A_DEFECT_CONCLUSION",
            "signals": template_signals,
        },
    }

    visible_signals = {k: v for k, v in feature.items() if k != "paragraphs_for_signatures"}
    return {
        "url": row.get("url"),
        "source_file": path,
        "page_type": row.get("page_type"),
        "language": row.get("language"),
        "indexable": bool(row.get("indexable")),
        "review_scope": "PRIMARY_INDEXABLE" if row.get("indexable") else (
            "HELD_NOINDEX_CONTENT" if priority == "HELD_NOINDEX_CONTENT" else "SUPPORT_UTILITY_OR_PLACEHOLDER"
        ),
        "review_priority": priority,
        "priority_basis": next_step,
        "phase2_action_recommendation_only": row.get("action"),
        "repository_evidence": {
            "title": row.get("title"),
            "meta_description": row.get("meta_description"),
            "h1": row.get("h1"),
            "h2_count": feature["h2_count"],
            "word_count": row.get("word_count"),
            "unique_text_ratio": row.get("unique_text_ratio"),
            "template_text_ratio": row.get("template_text_ratio"),
            "internal_inlinks": row.get("internal_inlinks"),
            "internal_outlinks": row.get("internal_outlinks"),
            "external_outlinks": row.get("external_outlinks"),
            "author": row.get("author"),
            "author_source": row.get("author_source"),
            "last_updated": row.get("last_updated"),
            "last_updated_source": row.get("last_updated_source"),
            "schema": row.get("schema"),
            "canonical": row.get("canonical"),
            "robots": row.get("robots"),
            "http_status": row.get("http_status"),
            "http_status_source": row.get("http_status_source"),
            "phase2_risk_flags": row.get("risk_flags") or [],
            "phase2_similarity_groups": row.get("similarity_group") or [],
            "shared_intro_signature": shared_intro,
            "shared_paragraph_signatures": repeated[:20],
            "visible_text_sample": {
                "opening_paragraph": feature["opening_excerpt"],
                "closing_paragraph": feature["closing_excerpt"],
                "heading_sample": feature["heading_sample"],
            },
            "structural_signals": visible_signals,
        },
        "master_command_questions": questions,
        "automated_flags": sorted(set(flags)),
        "human_editorial_review_status": "NOT_PERFORMED",
        "native_language_review_status": "NOT_PERFORMED",
        "source_fact_verification_status": "NOT_PERFORMED",
        "external_similarity_check_status": "NOT_PERFORMED",
        "destructive_or_publication_change_performed": False,
        "recommended_next_step": next_step,
    }


def build_report() -> dict:
    try:
        source = json.loads(PHASE2.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read Phase 2 inventory: {exc}")
    rows = source.get("pages", [])
    if not isinstance(rows, list) or not rows:
        raise SystemExit("Phase 2 inventory has no pages")

    features: dict[str, dict] = {}
    para_groups: dict[str, set[str]] = defaultdict(set)
    intro_groups: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        path = str(row.get("source_file") or "")
        file_path = ROOT / path
        if not path or not file_path.is_file():
            features[path] = {
                "paragraphs_for_signatures": [], "paragraph_count": 0,
                "substantial_paragraph_count": 0, "h2_count": 0, "h3_count": 0,
                "table_count": 0, "list_count": 0, "list_item_count": 0,
                "figure_count": 0, "blockquote_count": 0, "pre_or_code_count": 0,
                "form_count": 0, "button_count": 0, "input_count": 0,
                "select_count": 0, "textarea_count": 0, "citation_element_count": 0,
                "non_latin_script_character_count": 0, "mistake_headings": [],
                "example_or_task_headings": [], "audience_context_signals": [],
                "practice_or_tool_links": [], "personal_experience_claim_candidates": [],
                "unresolved_template_token_candidates": [],
                "opening_excerpt": None, "closing_excerpt": None, "heading_sample": [],
                "h1_from_body": None,
            }
            continue
        raw = file_path.read_text(encoding="utf-8", errors="ignore")
        feature = extract_features(raw)
        features[path] = feature
        substantive = feature["paragraphs_for_signatures"]
        per_page = {paragraph_signature(p) for p in substantive}
        for sig in per_page:
            para_groups[sig].add(path)
        if row.get("indexable") and substantive:
            intro_groups[paragraph_signature(substantive[0])].add(path)

    # A repeated paragraph is recorded only when the same normalized signature
    # occurs on at least three distinct URLs. It remains a signal, never a
    # penalty or removal recommendation by itself.
    global_para_groups = {sig: paths for sig, paths in para_groups.items() if len(paths) >= 3}
    page_rows = [page_row(row, features[str(row.get("source_file") or "")], intro_groups, global_para_groups) for row in rows]
    priority_counts = Counter(page["review_priority"] for page in page_rows)
    flag_counts = Counter(flag for page in page_rows for flag in page["automated_flags"])
    pages_with_repeated = sum(bool(page["repository_evidence"]["shared_paragraph_signatures"]) for page in page_rows)
    pages_with_intro = sum(bool(page["repository_evidence"]["shared_intro_signature"]) for page in page_rows)
    pages_with_tokens = sum(
        bool(page["repository_evidence"]["structural_signals"]["unresolved_template_token_candidates"])
        for page in page_rows
    )
    indexable_count = sum(bool(row.get("indexable")) for row in rows)
    noindex_count = len(rows) - indexable_count

    return {
        "schema_version": 1,
        "report_name": "Phase 3 repository-backed originality audit and human-review queue",
        "scope": "Every public page in the Phase 2 repository inventory; all ten master-command questions are represented per page.",
        "method": "Deterministic repository-only triage using page metadata, visible main-body structure, text samples and the current Phase 2 signals. No AI detector, live crawl, external plagiarism comparison, native-speaker review, authorship validation or source fact-check is performed.",
        "priority_policy": {
            "P1_REVIEW": "Indexable and Phase 2 HIGH; first editorial review queue, not a defect finding.",
            "P2_REVIEW": "Indexable and Phase 2 MEDIUM; review before future optimization or republication decisions.",
            "P3_CONFIRM": "Indexable and Phase 2 LOW; confirm page intent/value, not automatic approval.",
            "HELD_NOINDEX_CONTENT": "Non-indexable content-type page with at least 100 repository words; keep current noindex until separately reviewed.",
            "NOINDEX_UTILITY_OR_PLACEHOLDER": "Noindex utility, research or short placeholder; preserve current state.",
            "shared_paragraph_policy": "Shared paragraphs are evidence pointers only and do not independently raise priority or imply a defect.",
        },
        "summary": {
            "public_pages": len(rows),
            "indexable_pages": indexable_count,
            "noindex_pages": noindex_count,
            "review_priority_counts": dict(sorted(priority_counts.items())),
            "pages_with_repeated_paragraph_signals": pages_with_repeated,
            "distinct_repeated_paragraph_signatures_at_least_three_urls": len(global_para_groups),
            "pages_with_shared_opening_signature": pages_with_intro,
            "pages_with_visible_unresolved_template_token_candidates": pages_with_tokens,
            "automated_flag_counts": dict(sorted(flag_counts.items())),
            "human_editorial_reviews_completed": 0,
            "native_language_reviews_completed": 0,
            "source_fact_checks_completed": 0,
            "external_similarity_checks_completed": 0,
            "content_or_indexation_changes_performed": 0,
        },
        "human_review_contract": {
            "page_level_status": "Every page remains NOT_PERFORMED until a named editor records an actual review.",
            "not_claimed": [
                "originality or uniqueness versus the public web",
                "linguistic naturalness or native-speaker quality",
                "facts or citations verified",
                "authorship or reviewer identity verified",
                "human editing completed",
                "AdSense compliance or approval",
            ],
        },
        "limitations": [
            "A title/H1-derived user-intent candidate is not proof the page answers that need.",
            "Tables, lists, scripts, forms and tools are structural signals; they do not prove examples are original or useful.",
            "Keyword stuffing, synonym spinning, machine-translation quality, fake claims, unsupported statistics, contradictions and copied external text require contextual human review.",
            "Shared paragraph signatures intentionally normalize numbers. Different numeric examples can share a signature, and a shared paragraph alone is not a defect.",
            "No page content, recommendation, canonical, robots state or publication setting is changed by this report.",
        ],
        "pages": page_rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the saved report is stale")
    args = parser.parse_args()
    report = build_report()
    expected = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        try:
            actual = OUT.read_text(encoding="utf-8")
        except OSError:
            print("STALE: missing", OUT.relative_to(ROOT))
            return 1
        if actual != expected:
            print("STALE:", OUT.relative_to(ROOT), "does not match current page inventory/content")
            return 1
        print(f"Phase 3 originality audit current: {report['summary']['public_pages']} pages; human review remains explicitly pending")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(expected, encoding="utf-8")
    summary = report["summary"]
    print(
        "wrote %s: %d pages, %d indexable, priorities %s; no human review,"
        " source verification, external comparison or content changes claimed"
        % (OUT.relative_to(ROOT), summary["public_pages"], summary["indexable_pages"], summary["review_priority_counts"])
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

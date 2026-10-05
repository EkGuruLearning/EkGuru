#!/usr/bin/env python3
"""Build the repository-only Phase 2 content inventory.

This extends the existing offline public-page inventory with the fields from
PHASE 2 of docs/commands/EkGuru_AdSense_Original_Content_Recovery_Master_Command.md.
It does not fetch production URLs, judge linguistic correctness, approve pages,
change indexation, or remove content. Unknown HTTP statuses, authors and dates
stay unknown rather than being inferred from file timestamps or boilerplate.

Usage:
    python3 tools/build-phase2-content-inventory.py
    python3 tools/build-phase2-content-inventory.py --check
"""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
OUT = ROOT / "data/quality/phase2-content-inventory.json"
BASE = "https://ekguru.shop/"
SHINGLE_SIZE = 7
TEMPLATE_MIN_PAGES = 3

sys.path.insert(0, str(TOOLS))
from lib.text import tokens  # noqa: E402 — project-standard Unicode tokenization


def load_tool_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PAGE_AUDIT = load_tool_module("phase2_adsense_readiness", TOOLS / "audit-adsense-readiness.py")
LINK_AUDIT = load_tool_module("phase2_full_page_inventory", TOOLS / "build-full-page-inventory.py")


class MetaScanner(PAGE_AUDIT.HTMLParser):
    """Collect explicit page-level authorship/date metadata and JSON-LD blocks."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, str] = {}
        self.ldjson: list[str] = []
        self._in_ldjson = False
        self._ldjson_parts: list[str] = []
        self.modified_times: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag == "meta":
            key = str(a.get("name") or a.get("property") or "").strip().lower()
            value = str(a.get("content") or "").strip()
            if key and value:
                self.meta.setdefault(key, value)
        elif tag == "script" and "ld+json" in str(a.get("type") or "").lower():
            self._in_ldjson = True
            self._ldjson_parts = []
        elif tag == "time":
            itemprop = str(a.get("itemprop") or "").lower()
            klass = str(a.get("class") or "").lower()
            if a.get("datetime") and (itemprop == "datemodified" or
                                        "updated" in klass or "modified" in klass):
                self.modified_times.append(str(a["datetime"]).strip())

    def handle_data(self, data: str) -> None:
        if self._in_ldjson:
            self._ldjson_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_ldjson:
            block = "".join(self._ldjson_parts).strip()
            if block:
                self.ldjson.append(block)
            self._in_ldjson = False
            self._ldjson_parts = []


def walk_files() -> set[str]:
    """Repository file set used only to distinguish local links from broken ones."""
    found: set[str] = set()
    excluded = {".git", "node_modules", ".venv", "vendor", "build", "dist", "coverage", "out", "target"}
    for directory, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in excluded and not d.startswith(".")]
        for name in names:
            found.add((Path(directory) / name).relative_to(ROOT).as_posix())
    return found


def sitemap_urls(file_set: set[str]) -> set[str]:
    urls: set[str] = set()
    for rel in sorted(file_set):
        if not (rel.startswith("sitemap") and rel.endswith(".xml") and "index" not in rel):
            continue
        try:
            source = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        urls.update(re.findall(r"<loc>(https://ekguru\.shop/[^<]*)</loc>", source))
    return urls


def normalized_hash(value: str, prefix: str) -> str:
    digest = hashlib.sha256((prefix + "\0" + value).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}:{digest}"


def shingle_hashes(page_tokens: list[str]) -> set[bytes]:
    if len(page_tokens) < SHINGLE_SIZE:
        return set()
    out: set[bytes] = set()
    for index in range(len(page_tokens) - SHINGLE_SIZE + 1):
        shingle = "\x1f".join(page_tokens[index:index + SHINGLE_SIZE]).encode("utf-8")
        out.add(hashlib.blake2b(shingle, digest_size=8).digest())
    return out


def page_type(path: str) -> str:
    parts = path.split("/")
    if path == "index.html":
        return "home"
    if path == "languages/index.html":
        return "language_directory"
    if parts[0] == "languages":
        if "level" in parts:
            return "language_level"
        if "lessons" in parts:
            return "language_lesson"
        if "practice" in parts or "quiz" in parts or "review" in parts:
            return "language_practice"
        if "course" in parts:
            return "language_course"
        return "language_hub_or_tool"
    if parts[0] == "learn":
        return "learning_content"
    if parts[0] == "answers":
        return "answer"
    if parts[0] == "tutor":
        return "tutor_profile_or_directory"
    if parts[0] == "toolbox":
        return "tool"
    if parts[0] in {"ask", "questions"}:
        return "community_or_question"
    if parts[0] in {"daily-hindi", "guides", "articles"}:
        return "guide_or_article"
    if path == "404.html":
        return "error"
    return "site_page"


def external_outlink_count(source: str) -> int:
    link_source = LINK_AUDIT.RE_SCRIPT.sub(" ", source)
    seen: set[str] = set()
    for href in LINK_AUDIT.RE_HREF.findall(link_source):
        href = html.unescape(href.strip())
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
            continue
        host = (urlparse(href).hostname or "").lower()
        if host and host != "ekguru.shop" and not host.endswith(".ekguru.shop"):
            seen.add(href.split("#", 1)[0])
    return len(seen)


def walk_json(value, authors: set[str], schema_types: set[str], modified: list[str]) -> None:
    if isinstance(value, dict):
        typ = value.get("@type")
        if isinstance(typ, str) and typ.strip():
            schema_types.add(typ.strip())
        elif isinstance(typ, list):
            schema_types.update(str(x).strip() for x in typ if str(x).strip())
        for key, item in value.items():
            if key == "author":
                candidates = item if isinstance(item, list) else [item]
                for candidate in candidates:
                    if isinstance(candidate, str) and candidate.strip():
                        authors.add(candidate.strip())
                    elif isinstance(candidate, dict):
                        name = candidate.get("name")
                        if isinstance(name, str) and name.strip():
                            authors.add(name.strip())
            elif key == "dateModified" and isinstance(item, str) and item.strip():
                modified.append(item.strip())
            walk_json(item, authors, schema_types, modified)
    elif isinstance(value, list):
        for item in value:
            walk_json(item, authors, schema_types, modified)


def explicit_page_facts(source: str, rel: str, editorial_pages: dict) -> dict:
    scanner = MetaScanner()
    scanner.feed(source)
    scanner.close()
    authors: set[str] = set()
    schema_types: set[str] = set()
    modified: list[str] = []
    for block in scanner.ldjson:
        try:
            walk_json(json.loads(block), authors, schema_types, modified)
        except (json.JSONDecodeError, TypeError):
            continue
    if scanner.meta.get("author"):
        authors.add(scanner.meta["author"])
    if scanner.meta.get("article:modified_time"):
        modified.append(scanner.meta["article:modified_time"])
    if scanner.meta.get("og:updated_time"):
        modified.append(scanner.meta["og:updated_time"])
    modified.extend(scanner.modified_times)

    record = editorial_pages.get(rel) or {}
    if record.get("updated"):
        last_updated = str(record["updated"])
        updated_source = "data/editorial/page-metadata.json"
    elif modified:
        last_updated = modified[0]
        updated_source = "explicit page dateModified metadata"
    else:
        last_updated = None
        updated_source = "unknown; file modification time is not used"
    return {
        "author": sorted(authors) or None,
        "author_source": "explicit meta author or JSON-LD author" if authors else "unknown; none asserted",
        "last_updated": last_updated,
        "last_updated_source": updated_source,
        "schema": sorted(schema_types),
    }


def main_content_text(source: str) -> str:
    # Remove known shared site chrome/review notices before counting content.
    content_source = PAGE_AUDIT.CHROME.sub(" ", source)
    parser = PAGE_AUDIT.Scan()
    parser.feed(content_source)
    parser.close()
    return re.sub(r"\s+", " ", " ".join(parser.text)).strip()


def build_inventory() -> dict:
    public_paths = [p.relative_to(ROOT).as_posix() for p in PAGE_AUDIT.html_files()]
    file_set = walk_files()
    sitemaps = sitemap_urls(file_set)
    editorial_path = ROOT / "data/editorial/page-metadata.json"
    editorial_pages = {}
    if editorial_path.exists():
        try:
            editorial_pages = json.loads(editorial_path.read_text(encoding="utf-8")).get("pages", {})
        except (json.JSONDecodeError, OSError):
            editorial_pages = {}

    rows: list[dict] = []
    shingle_sets: list[set[bytes]] = []
    paragraph_sets: list[set[str]] = []
    title_groups: dict[str, list[int]] = defaultdict(list)
    description_groups: dict[str, list[int]] = defaultdict(list)
    intro_groups: dict[str, list[int]] = defaultdict(list)
    exact_text_groups: dict[str, list[int]] = defaultdict(list)
    shingle_frequency: Counter[bytes] = Counter()
    paragraph_frequency: Counter[str] = Counter()

    for rel in public_paths:
        source = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        base = LINK_AUDIT.analyse(rel, sitemaps, file_set)
        text = main_content_text(source)
        page_tokens = tokens(text)
        shingles = shingle_hashes(page_tokens)
        shingle_sets.append(shingles)
        shingle_frequency.update(shingles)

        paragraphs = PAGE_AUDIT.content_paragraphs(source)
        page_paragraphs = set(paragraphs)
        paragraph_sets.append(page_paragraphs)
        paragraph_frequency.update(page_paragraphs)

        title_key = PAGE_AUDIT.norm(base["title"])
        description_key = PAGE_AUDIT.norm(base["meta_description"])
        intro_key = paragraphs[0] if paragraphs else ""
        text_hash = hashlib.sha256(" ".join(page_tokens).encode("utf-8")).hexdigest()
        idx = len(rows)
        if title_key:
            title_groups[title_key].append(idx)
        if description_key:
            description_groups[description_key].append(idx)
        if intro_key:
            intro_groups[intro_key].append(idx)
        if page_tokens:
            exact_text_groups[text_hash].append(idx)

        explicit = explicit_page_facts(source, rel, editorial_pages)
        row = {
            "url": base["url"],
            "source_file": rel,
            "page_type": page_type(rel),
            "language": base["language"] or None,
            "title": base["title"] or None,
            "meta_description": base["meta_description"] or None,
            "h1": base["h1"] or None,
            "h1_count": len(LINK_AUDIT.RE_H1.findall(source)),
            "page_class": base["page_class"],
            "word_count": PAGE_AUDIT.count_words(text),
            "visible_text_length": len(text),
            "unique_text_ratio": None,
            "template_text_ratio": None,
            "internal_inlinks": 0,
            "internal_outlinks": base["internal_link_count"],
            "external_outlinks": external_outlink_count(source),
            "author": explicit["author"],
            "author_source": explicit["author_source"],
            "last_updated": explicit["last_updated"],
            "last_updated_source": explicit["last_updated_source"],
            "schema": explicit["schema"],
            "structured_data_status": base["structured_data_status"],
            "canonical": base["canonical"] or None,
            "robots": base["robots"] or "index,follow",
            "http_status": None,
            "http_status_source": "not fetched; repository-only inventory",
            "indexable": base["indexable"],
            "in_sitemap": base["in_sitemap"],
            "orphan": True,
            "similarity_group": [],
            "content_quality_score": 0,
            "content_quality_score_type": "automated_structural_triage_0_to_100",
            "content_quality_score_is_editorial_rating": False,
            "adsense_risk": None,
            "adsense_risk_basis": "repository signals only; not a Google policy or approval decision",
            "risk_flags": [],
            "action": None,
            "action_is_recommendation_only": True,
            "action_note": "No content, indexation, or URL was changed by this inventory.",
            "internal_link_count": base["internal_link_count"],
            "broken_link_count": base["broken_link_count"],
            "broken_link_targets": base["broken_link_targets"],
        }
        row["_text_tokens"] = page_tokens
        row["_title_key"] = title_key
        row["_description_key"] = description_key
        row["_intro_key"] = intro_key
        row["_text_hash"] = text_hash
        row["_shingle_index"] = idx
        row["_path"] = rel
        rows.append(row)

    inbound: Counter[str] = Counter()
    for rel in public_paths:
        base = LINK_AUDIT.analyse(rel, sitemaps, file_set)
        for target in set(base["internal_link_targets"]):
            if target != rel:
                inbound[target] += 1

    def attach_groups(mapping: dict[str, list[int]], kind: str) -> None:
        for key, members in mapping.items():
            if len(members) < 2:
                continue
            group_id = normalized_hash(key, kind)
            for idx in members:
                rows[idx]["similarity_group"].append({
                    "kind": kind,
                    "group_id": group_id,
                    "member_count": len(members),
                })

    attach_groups(title_groups, "title")
    attach_groups(description_groups, "meta_description")
    attach_groups(intro_groups, "opening_paragraph")
    attach_groups(exact_text_groups, "exact_visible_text")

    for idx, row in enumerate(rows):
        rel = row["_path"]
        row["internal_inlinks"] = inbound.get(rel, 0)
        row["orphan"] = row["internal_inlinks"] == 0
        shingles = shingle_sets[idx]
        if shingles:
            row["unique_text_ratio"] = round(
                sum(1 for shingle in shingles if shingle_frequency[shingle] == 1) / len(shingles), 3
            )
            row["template_text_ratio"] = round(
                sum(1 for shingle in shingles if shingle_frequency[shingle] >= TEMPLATE_MIN_PAGES) / len(shingles), 3
            )
        else:
            row["unique_text_ratio"] = 0.0
            row["template_text_ratio"] = 0.0

        groups = row["similarity_group"]
        row["similarity_group"].sort(key=lambda item: (item["kind"], item["group_id"]))
        word_count = row["word_count"]
        flags: list[str] = []
        if row["indexable"]:
            if word_count < 250:
                flags.append("thin_indexable_under_250_words")
            if not row["title"]:
                flags.append("missing_title")
            if not row["meta_description"]:
                flags.append("missing_meta_description")
            if not row["h1"]:
                flags.append("missing_h1")
            if not row["canonical"]:
                flags.append("missing_canonical")
            if row["orphan"]:
                flags.append("no_internal_inlinks")
            if row["unique_text_ratio"] < 0.85:
                flags.append("low_unique_7gram_ratio")
            if row["template_text_ratio"] >= 0.25:
                flags.append("repeated_7gram_share_at_least_25_percent")
            if groups:
                flags.append("exact_similarity_group")
            if row["broken_link_count"]:
                flags.append("broken_local_links")

        row["risk_flags"] = sorted(set(flags))
        if not row["indexable"]:
            row["adsense_risk"] = "NOT_INDEXABLE"
            row["action"] = "NOINDEX"
        elif any(flag in row["risk_flags"] for flag in (
                "thin_indexable_under_250_words", "missing_title", "missing_meta_description",
                "missing_h1", "missing_canonical", "broken_local_links")):
            row["adsense_risk"] = "HIGH"
            row["action"] = "IMPROVE"
        elif "exact_visible_text" in {g["kind"] for g in groups}:
            row["adsense_risk"] = "MEDIUM"
            row["action"] = "MERGE"
        elif row["risk_flags"]:
            row["adsense_risk"] = "MEDIUM"
            row["action"] = "IMPROVE"
        else:
            row["adsense_risk"] = "LOW"
            row["action"] = "KEEP"

        # This score measures mechanical depth/metadata/connectivity signals only.
        # It deliberately says nothing about linguistic correctness or originality.
        depth_score = 25 * min(word_count / 500, 1)
        metadata_score = 15 * (bool(row["title"]) + bool(row["meta_description"])) / 2
        heading_score = 10 if row["h1"] else 0
        unique_score = 20 * min(row["unique_text_ratio"] / 0.85, 1)
        canonical_score = 10 if row["canonical"] else 0
        inbound_score = 10 * min(row["internal_inlinks"] / 3, 1)
        outlink_score = 10 * min(row["internal_outlinks"] / 3, 1)
        row["content_quality_score"] = round(
            depth_score + metadata_score + heading_score + unique_score + canonical_score + inbound_score + outlink_score
        )

        for private_key in ("_text_tokens", "_title_key", "_description_key", "_intro_key", "_text_hash", "_shingle_index", "_path"):
            row.pop(private_key, None)

    # Keep the public row order deterministic and summarize only measured facts.
    rows.sort(key=lambda item: item["source_file"])
    risks = Counter(row["adsense_risk"] for row in rows)
    actions = Counter(row["action"] for row in rows)
    page_types = Counter(row["page_type"] for row in rows)
    scores = sorted(row["content_quality_score"] for row in rows)
    median_score = scores[len(scores) // 2] if scores else None
    summary = {
        "repository_html_pages": len(rows),
        "indexable": sum(1 for row in rows if row["indexable"]),
        "noindex": sum(1 for row in rows if not row["indexable"]),
        "http_status_checked": sum(1 for row in rows if row["http_status"] is not None),
        "http_status_pending": sum(1 for row in rows if row["http_status"] is None),
        "orphan_indexable": sum(1 for row in rows if row["indexable"] and row["orphan"]),
        "indexable_without_author_attribution": sum(1 for row in rows if row["indexable"] and not row["author"]),
        "indexable_without_known_last_updated": sum(1 for row in rows if row["indexable"] and not row["last_updated"]),
        "similarity_groups_count": sum(1 for mapping in (title_groups, description_groups, intro_groups, exact_text_groups)
                                       for members in mapping.values() if len(members) > 1),
        "adsense_risk_counts": dict(sorted(risks.items())),
        "action_counts": dict(sorted(actions.items())),
        "page_type_counts": dict(sorted(page_types.items())),
        "median_automated_triage_score": median_score,
        "pages_recommended_for_removal": 0,
    }
    return {
        "schema_version": 1,
        "phase": 2,
        "phase_status": "REPOSITORY_INVENTORY_READY_FOR_REVIEW; LIVE_HTTP_CRAWL_PENDING",
        "generated_by": "tools/build-phase2-content-inventory.py",
        "base": BASE,
        "scope": "Repository-backed public HTML pages only; static crawl, no network requests",
        "summary": summary,
        "metric_definitions": {
            "word_count": "Visible body text after known shared chrome is removed; CJK and Thai use the repository script-aware counter.",
            "visible_text_length": "Unicode character count of the same normalized visible body text.",
            "unique_text_ratio": f"Share of this page's distinct {SHINGLE_SIZE}-token shingles that occur on only this page in this repository inventory; cross-page exact-shingle proxy, not semantic originality.",
            "template_text_ratio": f"Share of this page's distinct {SHINGLE_SIZE}-token shingles that occur on at least {TEMPLATE_MIN_PAGES} pages; repeated-text proxy, not a semantic template detector.",
            "internal_inlinks": "Count of distinct repository public HTML source pages linking to this source file in static markup.",
            "internal_outlinks": "Static internal href occurrences; runtime-generated links are not counted.",
            "author": "Only explicit meta-author or JSON-LD author values; null means none was found, not that a person is absent.",
            "last_updated": "Explicit own-content metadata or page dateModified markup; file mtimes and build dates are never used.",
            "http_status": "Null for every row because no production HTTP request was performed.",
            "content_quality_score": "0–100 automated structural triage score from word count, metadata, H1, unique-text proxy, canonical and static links; not an editorial, linguistic, source, AdSense or approval rating.",
            "adsense_risk": "Repository-only triage signal; not Google policy interpretation, live ad review or approval prediction.",
            "action": "Review recommendation only. No page was edited, merged, removed, or re-indexed by this inventory.",
        },
        "limitations": [
            "Production HTTP status, redirects, live canonical responses, rendered text and browser behavior were not fetched.",
            "Similarity ratios are exact token-shingle signals; they do not establish semantic duplication or copied content.",
            "Content quality scores do not assess native-language correctness, source support, originality, usefulness or human editorial quality.",
            "Null authors and dates remain unknown; no byline, author, publication date or review record is invented.",
            "NOINDEX recommendations reflect the existing repository robots state; no indexation decision was changed.",
        ],
        "pages": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the saved inventory is stale")
    args = parser.parse_args()
    payload = build_inventory()
    expected = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        try:
            actual = OUT.read_text(encoding="utf-8")
        except OSError:
            print(f"STALE: missing {OUT.relative_to(ROOT)}")
            return 1
        if actual != expected:
            print(f"STALE: {OUT.relative_to(ROOT)} does not match current public HTML")
            return 1
        print("Phase 2 content inventory current:", payload["summary"]["repository_html_pages"],
              "repo-backed public pages; live HTTP status remains unverified")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(expected, encoding="utf-8")
    print("wrote", OUT.relative_to(ROOT))
    print("pages=%d indexable=%d noindex=%d http_status_pending=%d median_score=%s" % (
        payload["summary"]["repository_html_pages"], payload["summary"]["indexable"],
        payload["summary"]["noindex"], payload["summary"]["http_status_pending"],
        payload["summary"]["median_automated_triage_score"]))
    print("No live crawl, editorial approval, indexation change, merge or removal performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

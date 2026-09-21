#!/usr/bin/env python3
"""Classify every country-language relation without upgrading weak evidence."""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from lib.country_quality import classify  # noqa: E402

SOURCE = ROOT / "data/global/language-country-relations.json"
OUT = ROOT / "data/quality/country-language-verification.json"


def build() -> dict:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    records = []
    for row in data.get("relations", []):
        state = classify(row)
        records.append({
            "relationship_id": row.get("relationship_id"),
            "country_id": row.get("country_id"),
            "language_id": row.get("language_id"),
            "language_name": row.get("language_name"),
            "native_name": row.get("native_name"),
            "script": row.get("script"),
            "category": row.get("category"),
            "confidence": row.get("confidence"),
            "source_priorities": sorted({str(s.get("priority")) for s in (row.get("sources") or []) if isinstance(s, dict) and s.get("priority")}),
            "quality_state": state,
            "public_rule": (
                "May support a factual public relationship claim with source attribution."
                if state == "VERIFIED"
                else "May be shown only with an explicit provisional label; not an authoritative claim."
                if state == "PROVISIONAL"
                else "Internal research only; exclude from public country-language lists, sitemaps and structured data."
            ),
        })
    states = Counter(r["quality_state"] for r in records)
    countries = defaultdict(set)
    for row in records:
        countries[row["quality_state"]].add(row["country_id"])
    return {
        "schema_version": 1,
        "generated_on": "2026-09-20",
        "source": "data/global/language-country-relations.json",
        "method": "VERIFIED requires linked non-agent A/B source, high confidence, and no human-review flag. PROVISIONAL requires linked non-agent A/B source, medium/high confidence, and no review flag. Everything else is RESEARCH_REQUIRED.",
        "summary": {
            "relations": len(records),
            "states": dict(sorted(states.items())),
            "countries_by_state": {state: len(values) for state, values in sorted(countries.items())},
        },
        "relations": records,
    }


def main() -> int:
    expected = json.dumps(build(), ensure_ascii=False, indent=2) + "\n"
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != expected:
            print("STALE: data/quality/country-language-verification.json")
            return 1
        print("PASS: country-language quality classifications are current")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(expected, encoding="utf-8")
    summary = json.loads(expected)["summary"]
    print("country-language quality:", summary["states"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

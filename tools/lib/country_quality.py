"""Deterministic country-language relationship publication states."""
from __future__ import annotations


def has_reputable_source(row: dict) -> bool:
    return any(
        isinstance(source, dict)
        and bool(source.get("source_url"))
        and source.get("evidence_type") != "agent-compiled"
        and str(source.get("priority") or "").split("-")[0] in {"A", "B"}
        for source in (row.get("sources") or [])
    )


def classify(row: dict) -> str:
    """Return VERIFIED, PROVISIONAL, or RESEARCH_REQUIRED.

    VERIFIED is intentionally strict: high confidence, no human-review flag,
    and a linked A/B source. PROVISIONAL has a reputable source but has not met
    that full confidence bar. Agent-only, unsourced, low-confidence and flagged
    rows remain research-only.
    """
    sourced = has_reputable_source(row)
    if sourced and row.get("confidence") == "high" and not row.get("needs_human_review"):
        return "VERIFIED"
    if sourced and row.get("confidence") in {"high", "medium"} and not row.get("needs_human_review"):
        return "PROVISIONAL"
    return "RESEARCH_REQUIRED"


RANK = {"RESEARCH_REQUIRED": 0, "PROVISIONAL": 1, "VERIFIED": 2}

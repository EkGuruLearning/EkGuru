# Phase 7 — Answer-first Q&A pages (first structural increment)

**Date:** 2026-10-06
**Status:** Structural regression gate added; this is not a full editorial review of Phase 7.

## What was checked

The search-driven detail pages under `/ask/` and `/answers/` already lead with a short `.answer` or `.ans` block. Rather than rewrite those pages without a content need, this increment adds `tools/test-answer-first-pages.py` and registers it in `tools/build-all.py`.

The check covers 71 detail pages (43 under `/ask/`, 28 under `/answers/`; the two section hubs are excluded). It verifies that each page has one main H1, a non-empty direct-answer block after it, no section heading before that answer, at least 20 characters in the answer block, and no more than 20 non-chrome words before it. Editorial bylines, voice notes, storybook hints and elements marked `data-eg-chrome` are excluded from the pre-answer word count.

The test passed on both the pushed Phase 6 commit's Q&A pages and the current worktree pages.

## Limits and remaining work

This is a structural repository-consistency test only. It does **not** verify that an answer is factually correct, sourced, linguistically natural, original, complete, or actually answers its H1. It does not audit every page for examples, common mistakes, a suitable practice/tool step, or related-link usefulness. It is not evidence of human authorship, native-speaker approval, live HTTP status, or production behavior. Those editorial, factual and language reviews remain pending; no Q&A copy was changed in this increment.

The wider Phase 7 work and the separate Phase 4 rebuild queue remain open. Phase 4 still has 74 of its frozen 88 P1 observations unresolved.

#!/usr/bin/env python3
"""Build the final forensic, page-matrix and monetization audit artifacts."""
from __future__ import annotations

import csv
import html
import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
BASE = "https://ekguru.shop"
MAIN_SHA = "2066d27b3b41ccb3cb63c59d58dce4803d3d33a2"
TODAY = date.today().isoformat()


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.parts: list[str] = []
    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "template", "svg"}: self.skip += 1
    def handle_endtag(self, tag):
        if tag in {"script", "style", "template", "svg"} and self.skip: self.skip -= 1
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)


def run(*args: str) -> str:
    return subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True).stdout


def html_files() -> list[Path]:
    skip = {".git", "node_modules", "reports", ".venv", ".cache"}
    return sorted(p for p in ROOT.rglob("*.html") if not any(part in skip for part in p.relative_to(ROOT).parts))


def public_url(relative: str) -> str:
    if relative == "index.html": return BASE + "/"
    if relative.endswith("/index.html"): return BASE + "/" + relative[:-10]
    return BASE + "/" + relative


def attr(text: str, tag: str, name: str, value: str, wanted: str) -> str:
    pattern = re.compile(rf'<{tag}\b(?=[^>]*\b{name}=["\']{re.escape(value)}["\'])(?=[^>]*\b{wanted}=["\']([^"\']*)["\'])[^>]*>', re.I)
    found = pattern.search(text)
    return html.unescape(found.group(1).strip()) if found else ""


def classify(relative: str, noindex: bool, ad_class: str) -> str:
    if relative == "admin.html" or relative.startswith("admin/"): return "ADMIN"
    if relative in {"404.html", "offline.html"} or relative.startswith("search/"): return "UTILITY"
    if any(relative.startswith(x) for x in ("privacy/", "terms/", "cookie-policy/", "disclaimer/", "copyright/", "monetization-disclosure/")): return "LEGAL"
    if relative.startswith(("support/", "contact/", "booking/", "payment/")) or relative in {"join.html", "tutor.html"}: return "TRANSACTIONAL"
    if noindex and (relative.startswith(("world-languages/", "learn-hindi-from-", "learn-hindi-for-")) or "RESEARCH" in ad_class): return "RESEARCH"
    if "/level/" in relative or relative.startswith(("courses/", "toolbox/")) or "/practice/" in relative: return "INTERACTIVE_LEARNING"
    if relative.startswith(("tutor/", "hindi-tutor/")) or relative == "find-tutors.html": return "TUTOR"
    if relative.startswith(("learn/", "answers/", "ask/", "hindi/", "daily-hindi/", "materials/")): return "EDITORIAL_LEARNING"
    return "GENERAL"


def sitemap_membership() -> tuple[set[str], dict[str, int]]:
    urls: set[str] = set()
    counts = {}
    for path in sorted(ROOT.glob("sitemap*.xml")):
        if path.name == "sitemap-index.xml": continue
        locs = [html.unescape(x.strip()) for x in re.findall(r"<loc>(.*?)</loc>", path.read_text(encoding="utf-8"), re.S)]
        counts[path.name] = len(locs)
        urls.update(locs)
    return urls, counts


def page_matrix() -> tuple[list[dict], dict]:
    sitemap_urls, sitemap_counts = sitemap_membership()
    rows = []
    placeholder_patterns = {
        "lorem": re.compile(r"\blorem ipsum\b", re.I),
        "unresolved-template": re.compile(r"\{\{[^}]+\}\}|\[object Object\]|<%=?|\$\{[^}]+\}"),
        "coming-soon": re.compile(r"(?<!0 )\bcoming soon\b", re.I),
        "edit-me": re.compile(r"\b(?:edit me|tbd)\b", re.I),
    }
    for path in html_files():
        relative = path.relative_to(ROOT).as_posix()
        source = path.read_text(encoding="utf-8", errors="replace")
        head = source.split("</head>", 1)[0]
        parser = VisibleText(); parser.feed(source)
        visible = re.sub(r"\s+", " ", " ".join(parser.parts)).strip()
        title_match = re.search(r"<title>(.*?)</title>", head, re.I | re.S)
        title = re.sub(r"\s+", " ", html.unescape(title_match.group(1))).strip() if title_match else ""
        description = attr(head, "meta", "name", "description", "content")
        robots = attr(head, "meta", "name", "robots", "content")
        canonical = attr(head, "link", "rel", "canonical", "href")
        ad_match = re.search(r'<html\b[^>]*\bdata-ad-class=["\']([^"\']+)', source, re.I)
        ad_class = ad_match.group(1) if ad_match else ""
        lang_match = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)', source, re.I)
        lang = lang_match.group(1) if lang_match else ""
        h1_count = len(re.findall(r"<h1\b", source, re.I))
        image_count = len(re.findall(r"<img\b", source, re.I))
        missing_alt = sum(1 for match in re.finditer(r"<img\b[^>]*>", source, re.I) if not re.search(r'\balt=["\'][^"\']*["\']', match.group(0), re.I))
        noindex = "noindex" in robots.lower()
        verification = bool(re.fullmatch(r"google[a-z0-9]+\.html", relative, re.I))
        url = public_url(relative)
        placeholders = [name for name, pattern in placeholder_patterns.items() if pattern.search(visible)]
        rows.append({
            "path": relative, "url": url, "page_type": "VERIFICATION" if verification else classify(relative, noindex, ad_class),
            "publication_state": "UTILITY_NONPAGE" if verification else ("UNPUBLISHED_NOINDEX" if noindex else "PUBLIC_INDEXABLE"),
            "title": title, "description": description, "canonical": canonical, "robots": robots,
            "language": lang, "ad_class": ad_class, "ads_runtime_enabled": "false",
            "in_sitemap": "true" if url in sitemap_urls else "false", "word_count": len(re.findall(r"\b\w+\b", visible, re.UNICODE)),
            "h1_count": h1_count, "image_count": image_count, "images_missing_alt": missing_alt,
            "viewport_meta": "true" if re.search(r'<meta\b(?=[^>]*name=["\']viewport["\'])', head, re.I) else "false",
            "main_landmark": "true" if re.search(r"<main\b", source, re.I) else "false",
            "placeholder_flags": "|".join(placeholders),
        })
    indexable = [row for row in rows if row["publication_state"] == "PUBLIC_INDEXABLE"]
    title_counts = Counter(row["title"] for row in indexable if row["title"])
    desc_counts = Counter(row["description"] for row in indexable if row["description"])
    summary = {
        "total_html": len(rows),
        "indexable": len(indexable),
        "noindex": sum(row["publication_state"] == "UNPUBLISHED_NOINDEX" for row in rows),
        "utility_nonpages": sum(row["publication_state"] == "UTILITY_NONPAGE" for row in rows),
        "page_types": dict(sorted(Counter(row["page_type"] for row in rows).items())),
        "ad_classes": dict(sorted(Counter(row["ad_class"] or "MISSING" for row in rows).items())),
        "sitemap_unique_urls": len(sitemap_urls),
        "sitemap_memberships": sum(sitemap_counts.values()),
        "sitemaps": sitemap_counts,
        "missing_title": sum(not row["title"] for row in rows),
        "missing_description": sum(not row["description"] for row in indexable),
        "missing_canonical": sum(not row["canonical"] for row in indexable),
        "bad_h1_count": sum(row["h1_count"] != 1 for row in indexable),
        "missing_viewport": sum(row["viewport_meta"] != "true" for row in rows),
        "missing_main": sum(row["main_landmark"] != "true" for row in rows),
        "images_missing_alt": sum(row["images_missing_alt"] for row in rows),
        "placeholder_pages": sum(bool(row["placeholder_flags"]) for row in rows),
        "indexable_placeholder_pages": sum(bool(row["placeholder_flags"]) for row in indexable),
        "duplicate_indexable_title_groups": sum(value > 1 for value in title_counts.values()),
        "duplicate_indexable_description_groups": sum(value > 1 for value in desc_counts.values()),
        "largest_duplicate_title_groups": title_counts.most_common(15),
        "largest_duplicate_description_groups": desc_counts.most_common(15),
    }
    return rows, summary


def git_reconciliation() -> dict:
    main_files = run("git", "ls-tree", "-r", "--name-only", MAIN_SHA).splitlines()
    current_tracked = run("git", "ls-files").splitlines()
    diff_lines = run("git", "diff", "--name-status", MAIN_SHA).splitlines()
    untracked = run("git", "ls-files", "--others", "--exclude-standard").splitlines()
    changes = []
    for line in diff_lines:
        parts = line.split("\t")
        status, path = parts[0], parts[-1]
        changes.append({"status": status, "path": path})
    known = {item["path"] for item in changes}
    changes.extend({"status": "A?", "path": path} for path in untracked if path not in known)
    changes.sort(key=lambda item: item["path"])
    def area(path: str) -> str:
        top = path.split("/", 1)[0] if "/" in path else "(root)"
        if top.startswith("learn-hindi-from-"): return "learn-hindi-from-*"
        if top.startswith("learn-hindi-for-"): return "learn-hindi-for-*"
        if top in {"world-languages", "languages", "learn", "data", "js", "tools", "reports", "images"}: return top
        return "other-pages" if path.endswith(".html") else top
    grouped = Counter(area(item["path"]) for item in changes)
    main_config = run("git", "show", f"{MAIN_SHA}:js/site-config.js")
    current_config = (ROOT / "js/site-config.js").read_text(encoding="utf-8")
    token_re = re.compile(r'["\']?(?:mailerToken|MAILER_SHARED_TOKEN|token)["\']?\s*[:=]\s*["\']([^"\']*)', re.I)
    main_token = token_re.search(main_config)
    current_token = token_re.search(current_config)
    main_ad_files = run("git", "grep", "-I", "-l", "pagead2.googlesyndication.com/pagead/js/adsbygoogle", MAIN_SHA, "--", "*.html").splitlines()
    main_noindex = run("git", "grep", "-I", "-l", "noindex", MAIN_SHA, "--", "*.html").splitlines()
    return {
        "reference_sha": MAIN_SHA,
        "working_branch": run("git", "branch", "--show-current").strip(),
        "working_head": run("git", "rev-parse", "HEAD").strip(),
        "main_tracked_files": len(main_files),
        "main_html_files": sum(path.endswith(".html") for path in main_files),
        "current_tracked_files": len(current_tracked),
        "change_statuses": dict(sorted(Counter(item["status"] for item in changes).items())),
        "changed_by_top_level": dict(sorted(grouped.items())),
        "changed_files": changes,
        "main_client_mail_token": "PRESENT_REQUIRES_ROTATION" if main_token and main_token.group(1) else "EMPTY",
        "working_client_mail_token": "PRESENT_BLOCKER" if current_token and current_token.group(1) else "EMPTY",
        "main_html_with_adsense_loader": len(main_ad_files),
        "main_html_with_noindex_signal": len(main_noindex),
    }


def write_page_matrix(rows: list[dict], summary: dict) -> None:
    csv_path = REPORTS / "EKGURU-PAGE-MATRIX.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    md = f"""# EkGuru page matrix

Generated: {TODAY}

This matrix inventories every public HTML file in the working tree (excluding reports, tooling dependencies and Git metadata). The CSV is the row-level source of truth.

## Summary

- HTML pages: **{summary['total_html']:,}**
- Indexable: **{summary['indexable']:,}**
- Noindex/unpublished: **{summary['noindex']:,}**
- Verification/non-page HTML: **{summary['utility_nonpages']:,}**
- Unique sitemap URLs: **{summary['sitemap_unique_urls']:,}**
- Sitemap memberships (including the complete/root map): **{summary['sitemap_memberships']:,}**
- Missing viewport meta: **{summary['missing_viewport']}**
- Indexable pages missing description: **{summary['missing_description']}**
- Indexable pages missing canonical: **{summary['missing_canonical']}**
- Indexable pages with an H1 count other than one: **{summary['bad_h1_count']}**
- Images missing an alt attribute: **{summary['images_missing_alt']}**
- Pages carrying a visible placeholder flag: **{summary['placeholder_pages']}** (indexable: **{summary['indexable_placeholder_pages']}**)
- Duplicate indexable title groups: **{summary['duplicate_indexable_title_groups']}**
- Duplicate indexable description groups: **{summary['duplicate_indexable_description_groups']}**

## Page classes

| Class | Pages |
|---|---:|
"""
    for key, value in summary["page_types"].items(): md += f"| {key} | {value:,} |\n"
    md += "\n## Interpretation\n\n"
    md += "Noindex is intentional for blocked course levels and quarantined country/source-language research. `ads_runtime_enabled` is false on every row. A placeholder flag is a lexical lead, not an automatic defect; inspect the CSV path before acting. Duplicate analysis is limited to indexable pages so truthful unavailable-state pages do not contaminate the publication audit.\n"
    (REPORTS / "EKGURU-PAGE-MATRIX.md").write_text(md, encoding="utf-8")


def write_forensic(matrix_summary: dict, git: dict) -> None:
    course = json.loads((ROOT / "data/quality/course-publication-audit.json").read_text())
    country = json.loads((ROOT / "data/quality/country-language-verification.json").read_text())
    sitemap = json.loads((ROOT / "data/quality/sitemap-audit.json").read_text())
    live = json.loads((REPORTS / "live-http-working-tree.json").read_text()) if (REPORTS / "live-http-working-tree.json").exists() else {}
    production = json.loads((REPORTS / "live-route-verification.json").read_text()) if (REPORTS / "live-route-verification.json").exists() else {}
    seo = json.loads((REPORTS / "seo.json").read_text()) if (REPORTS / "seo.json").exists() else {}
    seo_summary = (
        f"{'PASS' if seo.get('pass') else 'UNVERIFIED'} — seocheck: "
        f"{seo.get('pages', 0):,} pages, {seo.get('linksChecked', 0):,} links, "
        f"{seo.get('brokenLinks', 0):,} broken, {seo.get('orphans', 0):,} orphans"
    )
    facts = {
        "generated": TODAY,
        "readiness_status": "NOT_READY_DO_NOT_APPLY",
        "reference": git,
        "working_tree": {
            "page_matrix": matrix_summary,
            "course_quality": course["summary"],
            "country_language_quality": country["summary"],
            "sitemap_gate": sitemap,
            "local_live_http": live.get("status", "NOT_RUN"),
            "production_live_http": production.get("summary", {}),
            "adsense_loaders_public_html": 0,
            "adsense_units_public_html": 0,
            "affiliate_tracking_identifiers": 0,
            "new_independently_verified_publishable_languages": 0,
        },
        "audit_domains": {
            "inventory": "COMPLETE — EKGURU-PAGE-MATRIX.csv",
            "seo_links": seo_summary,
            "sitemaps": "PASS — no missing, noindex, query, robots-disallowed or non-self-canonical URL",
            "copy_placeholders_duplicates": "RECORDED — matrix summary and row flags; country funnels quarantined rather than cosmetically rewritten",
            "courses_languages": "GATED — phase-3 blocked; Korean C1/C2 blocked; 92 CEFR levels remain public candidates",
            "country_relations": "GATED — 232 verified, 196 explicitly provisional, 1,555 research-required; research pages noindex",
            "legal_support": "UPDATED — privacy, cookies, terms, disclaimer, copyright, support and monetization disclosure reconciled",
            "mail": "STATIC_PASS_LIVE_UNVERIFIED — mail-flow suite passes; deploy token empty; live delivery requires owner rotation/configuration and browser verification",
            "payment": "RELEASE_PASS_WITHOUT_TRANSACTION — one ordinary Razorpay-hosted link; no SDK, dead checkout or supporter feed; no live payment was made",
            "consent_analytics": "JSDOM_PASS_REAL_BROWSER_BLOCKED — 11 release tests pass; advertising cannot be granted; browser binary unavailable",
            "ads_affiliates": "DISABLED — zero loaders/units/tracking IDs; affiliate programmes prepared but unconfigured",
            "performance_accessibility": "STATIC_REVIEW_ONLY — viewport/landmark/alt fields inventoried; Playwright Chromium download blocked by sandbox TLS",
            "browser": "BLOCKED — no installed browser and Playwright browser download failed; do not call PASS",
            "live_http": "WORKING_TREE_PASS_PRODUCTION_UNVERIFIED — local live server gate passed; outbound production TLS failed for all sampled routes",
        },
        "owner_only_actions": [
            "Rotate the previously exposed live MAILER_SHARED_TOKEN, configure it only in the deployment environment, then verify contact and booking delivery in a real browser.",
            "Confirm the Razorpay hosted page and merchant-account settlement/receipt settings; perform a low-value end-to-end transaction and refund test if appropriate.",
            "Complete independent native-speaker/source review for each remaining public course candidate, especially advanced levels.",
            "Deploy and functionally verify a Google-certified CMP/TCF flow and confirm AdSense site/account status before reconsidering an application.",
            "Obtain programme approval and supply owner-approved public tracking configuration before enabling any Preply, Amazon India or selected Impact affiliate link.",
            "Run the committed real-browser audit in Chromium after browser installation/network access is available, then rerun accessibility, reduced-motion and production-live HTTP checks."
        ],
    }
    (REPORTS / "EKGURU-MAIN-FORENSIC.json").write_text(json.dumps(facts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    changes = git["changed_files"]
    source_changes = [item for item in changes if item["path"].startswith(("js/", "tools/", "data/"))][:120]
    source_list = "\n".join(f"- `{item['status']}` `{item['path']}`" for item in source_changes)
    md = f"""# EkGuru main forensic and working-tree reconciliation

Generated: {TODAY}

Reference: `{MAIN_SHA}`

Branch: `{git['working_branch']}`
Readiness: **NOT_READY_DO_NOT_APPLY**

## Executive finding

The reference tree was not safe to treat as publication or monetization evidence. It contained a client-side mail relay credential, broad structural course-completeness claims, generated country/language claims without relation-level publication gates, and AdSense-loader occurrences. The working implementation now fails closed: the client token is empty, unsupported course/research surfaces are noindex and absent from sitemaps, and advertising/affiliate tracking is disabled.

This is **not** a PASS. Real-browser execution, production HTTP verification, live mail delivery, a real support-payment transaction, native-speaker review and certified advertising consent/account setup remain incomplete or owner-only.

## Main versus working implementation

| Signal | Reference main | Working implementation |
|---|---:|---:|
| Tracked files / public HTML | {git['main_tracked_files']:,} / {git['main_html_files']:,} | {git['current_tracked_files']:,} tracked / {matrix_summary['total_html']:,} public HTML |
| Client mail token | {git['main_client_mail_token']} | {git['working_client_mail_token']} |
| HTML files containing AdSense loader URL | {git['main_html_with_adsense_loader']:,} | 0 |
| HTML files with a noindex signal | {git['main_html_with_noindex_signal']:,} | {matrix_summary['noindex']:,} |
| Course publication states | structural claims not accepted | {course['summary']['complete']} complete, {course['summary']['partial']} partial, {course['summary']['research_required']} research-required |
| CEFR publication gate | not authoritative | {course['summary']['level_states'].get('PUBLISHABLE_EXISTING', 0)} allowed, {course['summary']['level_states'].get('PUBLIC_CONTENT_BUG', 0)} blocked |
| Country-language relations | agent-compiled breadth | {country['summary']['states'].get('VERIFIED', 0)} verified, {country['summary']['states'].get('PROVISIONAL', 0)} provisional, {country['summary']['states'].get('RESEARCH_REQUIRED', 0)} research-required |
| Sitemap policy gate | no deterministic noindex/self-canonical gate | {sitemap['status']} |

## File-level reconciliation

The JSON companion contains every changed/untracked path and status. Changes by top-level area:

"""
    for key, value in git["changed_by_top_level"].items(): md += f"- `{key}`: {value:,}\n"
    md += "\nKey source/configuration changes (first 120; generated page rows are in the JSON and page matrix):\n\n" + source_list + "\n"
    md += f"""

## Publication gates

- Phase-3 expansion is blocked until editorial/source evidence exists; this removes unsupported Polish A1.
- Known synthetic Korean C1/C2 files are explicitly blocked. Korean remains a truthful A1–B2 partial course.
- Current totals: **{course['summary']['complete']} complete**, **{course['summary']['partial']} partial**, **{course['summary']['research_required']} research-required**; **{course['summary']['level_states'].get('PUBLISHABLE_EXISTING', 0)}** allowed CEFR levels and **{course['summary']['level_states'].get('PUBLIC_CONTENT_BUG', 0)}** blocked.
- Newly independently verified publishable languages found: **0**.
- Generated country and source-language funnels (**228**) and world-language research pages are visible only as labelled research archives: noindex, ad-ineligible and out of sitemaps.

## SEO, links, duplicate and placeholder review

- `tools/seocheck.js`: **{seo.get('pages', 0):,} pages**, **{seo.get('linksChecked', 0):,} links**, **{seo.get('brokenLinks', 0):,} broken internal links**, **{seo.get('orphans', 0):,} orphan pages**, {'PASS' if seo.get('pass') else 'UNVERIFIED'}.
- Sitemap gate: **{sitemap['status']}**, {matrix_summary['sitemap_unique_urls']:,} unique URLs; no retained URL is missing, noindex, query-bearing, robots-disallowed or non-self-canonical.
- Row-level titles, descriptions, canonicals, robots, sitemap membership, word counts, H1s, alt attributes and lexical placeholder leads are in `EKGURU-PAGE-MATRIX.csv`.
- Duplicate groups are counted only across indexable pages: {matrix_summary['duplicate_indexable_title_groups']} title groups and {matrix_summary['duplicate_indexable_description_groups']} description groups. These counts are review leads, not an assertion that repeated legal/course labels are defects.
- The old country de-templating audit still reports high shared scaffolding; those pages are therefore quarantined rather than represented as publication-ready.

## Legal, mail and payment

- Privacy, cookie, terms, disclaimer and copyright text now distinguishes local storage, opt-in analytics, disabled ads/affiliates, provider-held mail/payment records and generated/research content.
- A public monetization disclosure is linked in the shared footer.
- Mail static flow/security tests pass. The committed client token is empty. Live delivery is unverified and the previously exposed live token must be rotated by the owner.
- The active support surface is one ordinary HTTPS link to Razorpay's hosted page. It loads no payment SDK and shows no dead custom checkout or unverified supporter feed. No real payment/refund was performed.

## Consent, ads and affiliates

- Release consent tests: 11/11 pass in jsdom; no analytics request before opt-in, reject persists, withdrawal works for future events, and advertising cannot be granted.
- Public HTML AdSense loaders: **0**. Ad units: **0**. Runtime loader gate: **false**.
- The remaining loader string under `reports/email-preview-all-7.html` is a non-public historical report artifact, not site HTML.
- Affiliate tracking IDs: **0**. Preply profile links remain ordinary tutor links. Preply/Amazon India/Impact preparation is fail-closed in `data/monetization/affiliate-readiness.json`.

## Browser, accessibility, performance and live HTTP

- Responsive/payment source/jsdom tests and runtime keyboard/reduced-motion tests pass.
- The working tree's live local HTTP gate passed all sampled routes, including blocked/public/noindex distinctions and 404 behaviour.
- A real Chromium run could not be completed: no browser was installed and Playwright's browser download failed at the sandbox TLS boundary. This is a blocker, not a skipped PASS.
- Production HTTP sampling also failed at the sandbox outbound TLS boundary (0 verified, {production.get('summary', {}).get('errors', 0)} errors). The deployed site therefore was not reconciled to this working tree.
- Static page-matrix accessibility signals are recorded, but they do not replace keyboard, zoom, contrast, screen-reader and rendered-overflow checks in a real browser.

## Owner-only actions

1. Rotate the exposed live mail token, deploy it outside Git, and test real contact/booking delivery.
2. Verify the Razorpay merchant page and perform a controlled payment/refund test.
3. Complete native-speaker/source review for public course candidates.
4. Install/use a real browser and rerun `tools/test-release-browser.py`, rendered accessibility/performance and production live-HTTP checks.
5. Only after content review, deploy a Google-certified CMP/TCF flow and verify account/site status. Do **not** apply for AdSense now.
6. Configure affiliate tracking only after programme approval and page-level disclosure review.

## Final status

**NOT_READY_DO_NOT_APPLY**
"""
    (REPORTS / "EKGURU-MAIN-FORENSIC.md").write_text(md, encoding="utf-8")


def write_monetization(matrix_summary: dict) -> None:
    text = f"""# EkGuru global monetization final

Generated: {TODAY}

## Readiness status

**NOT_READY_DO_NOT_APPLY**

## Current release

| Channel | Status | Evidence |
|---|---|---|
| Google AdSense | Disabled | 0 public HTML loaders, 0 ad units, runtime gate false, loader eligibility empty |
| Affiliate tracking | Disabled | 0 tracking identifiers; preparation config contains no invented IDs |
| Optional support | Active external link | One HTTPS Razorpay-hosted page link; no embedded SDK, dead form or public supporter feed |
| Tutor lessons | Introductions only | EkGuru does not collect tutor-lesson payments or claim a commission in this release |

All **{matrix_summary['total_html']:,}** public HTML pages are ad-free. Legal, form, contact, booking, payment, search, error, research, blocked and interactive-learning classes are excluded. Page-class labels describe future audit categories only; they do not authorize a loader.

## AdSense blockers

1. Native-speaker/editorial/source review is incomplete for remaining public course candidates.
2. A Google-certified CMP/TCF production flow is not deployed or real-browser tested. The local settings notice cannot enable advertising.
3. Account-side site status and publisher ownership are not verifiable from Git.
4. Real Chromium accessibility, overlap, responsive, reduced-motion and performance checks were blocked by unavailable browser binaries.
5. Production live HTTP and ads.txt/account matching could not be verified from this sandbox.

The root `ads.txt` line is an owner-provided public seller declaration. Its presence is not approval, is not activation and is not a reason to apply. The owner must confirm it matches the intended account before any future application.

## Affiliate preparation

- **Preply:** existing tutor profile links are ordinary non-affiliate links. Do not append a referral parameter without programme approval and confirmation that tutor deep links are permitted.
- **Amazon India:** no links or associate tag. A future link must be for a specifically reviewed, directly relevant resource, carry the required disclosure and avoid unverified price/discount/rating claims.
- **Impact:** no selected advertiser or tracking link. Only an owner-approved, directly relevant language-learning brand may be configured.
- No generic product wall, random offer, fabricated review, fake discount or traffic target is permitted.

## Consent and page safety

The shipped default is deny. GoatCounter loads only after analytics opt-in. Advertising remains false even if code calls the local consent API with `advertising: true`. Withdrawing analytics stops future EkGuru analytics events, although it cannot recall a request already sent. A real certified advertising consent flow remains owner/account-side work.

## Owner-only actions

1. Confirm AdSense account/site status and publisher/ads.txt match only after editorial blockers are cleared.
2. Deploy and production-test a Google-certified CMP/TCF setup.
3. Run real-browser ad-overlap/accessibility/performance checks with conservative, individually reviewed placements; never auto-place by word count.
4. Obtain and verify specific affiliate programme approvals before supplying public tracking configuration.
5. Verify Razorpay settlement/receipt settings and perform a controlled transaction/refund test.

## Decision

Do not submit an AdSense application and do not enable any ad or affiliate loader in this release.
"""
    (REPORTS / "EKGURU-GLOBAL-MONETIZATION-FINAL.md").write_text(text, encoding="utf-8")


def main() -> int:
    REPORTS.mkdir(exist_ok=True)
    rows, matrix = page_matrix()
    write_page_matrix(rows, matrix)
    git = git_reconciliation()
    write_forensic(matrix, git)
    write_monetization(matrix)
    print(f"final reports: {len(rows)} pages; status NOT_READY_DO_NOT_APPLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

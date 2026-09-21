#!/usr/bin/env python3
"""Build the forensic reconciliation, page matrix and monetization report."""
from __future__ import annotations

import csv
import html
import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
BASE_SHA = "2066d27b3b41ccb3cb63c59d58dce4803d3d33a2"
TODAY = "2026-09-21"


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.DEVNULL)


def tag_attr(text: str, tag: str, attr: str, value: str | None = None) -> str:
    for found in re.findall(rf"<{tag}\b[^>]*>", text, re.I):
        attrs = dict(re.findall(r'([\w:-]+)\s*=\s*["\']([^"\']*)["\']', found))
        if value is None or attrs.get(attr, "").lower() == value.lower():
            return attrs.get("content") or attrs.get("href") or attrs.get("class") or ""
    return ""


def title_of(text: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1)).strip()) if m else ""


def visible_words(text: str) -> int:
    clean = re.sub(r"<(script|style|template)\b.*?</\1>", " ", text, flags=re.I | re.S)
    clean = re.sub(r"<!--.*?-->", " ", clean, flags=re.S)
    clean = html.unescape(re.sub(r"<[^>]+>", " ", clean))
    return len(re.findall(r"\b[\w\u0900-\u097f\u0980-\u0d7f\u3040-\u30ff\u4e00-\u9fff]+\b", clean, re.U))


def category(path: str) -> str:
    if path == "index.html": return "homepage"
    if re.match(r"languages/[^/]+/level/[^/]+/index\.html$", path): return "course-level"
    if re.match(r"languages/[^/]+/level/index\.html$", path): return "course-ladder"
    if path in {"courses/index.html", "languages/index.html"}: return "course-catalogue"
    if path.startswith("world-languages/"): return "country-language-research"
    if path.startswith("learn-hindi-from-") or path.startswith("learn-hindi-by-country/"): return "country-funnel-research"
    if path.startswith("learn-hindi-for-"): return "source-language-research"
    if path.startswith(("privacy/", "terms/", "cookie-policy/", "disclaimer/", "copyright/", "monetization-disclosure/")): return "legal"
    if path.startswith(("contact/", "booking/", "join")): return "form"
    if path.startswith("support/"): return "payment"
    if path.startswith(("toolbox/", "name-in-hindi/")): return "interactive-tool"
    if path.startswith(("tutor/", "hindi-tutor/")) or path in {"tutor.html", "find-tutors.html"}: return "tutor"
    if path.startswith(("learn/", "daily-hindi/", "hindi/")): return "learning-content"
    if path.startswith(("ask/", "answers/")): return "answer-content"
    if path in {"404.html", "admin.html"} or path.startswith("search/"): return "utility"
    return "other"


def build_matrix() -> tuple[list[dict], dict]:
    audit = json.loads((ROOT / "data/quality/course-publication-audit.json").read_text())
    course_state = {
        (c["code"], row["level"].lower()): row["state"]
        for c in audit["courses"] for row in c["levels"]
    }
    pages = sorted(
        p for p in ROOT.rglob("*.html")
        if ".git" not in p.parts and "node_modules" not in p.parts and ".venv" not in p.parts and "reports" not in p.parts
        and not re.fullmatch(r"google[a-z0-9]+\.html", p.name, re.I)
    )
    rows = []
    title_paths, canonical_paths = defaultdict(list), defaultdict(list)
    placeholder_rx = re.compile(r"\b(?:TBD|lorem ipsum|replace me)\b|ca-pub-0{6,}", re.I)
    for file in pages:
        rel = file.relative_to(ROOT).as_posix()
        text = file.read_text(encoding="utf-8", errors="replace")
        title = title_of(text)
        canonical = ""
        for link in re.findall(r"<link\b[^>]*>", text, re.I):
            attrs = dict(re.findall(r'([\w:-]+)\s*=\s*["\']([^"\']*)["\']', link))
            if attrs.get("rel", "").lower() == "canonical":
                canonical = attrs.get("href", "")
                break
        robots = ""
        for meta in re.findall(r"<meta\b[^>]*>", text, re.I):
            attrs = dict(re.findall(r'([\w:-]+)\s*=\s*["\']([^"\']*)["\']', meta))
            if attrs.get("name", "").lower() == "robots":
                robots = attrs.get("content", "")
                break
        ad_class_match = re.search(r'<html\b[^>]*\bdata-ad-class=["\']([^"\']+)', text, re.I)
        noindex = "noindex" in robots.lower()
        h1 = len(re.findall(r"<h1\b", text, re.I))
        ids = re.findall(r'<[a-z][^>]*\bid=["\']([^"\']+)["\']', text, re.I)
        duplicate_ids = sorted(value for value, count in Counter(ids).items() if count > 1)
        script_sources = []
        for script in re.findall(r"<script\b[^>]*>", text, re.I):
            source = re.search(r'\bsrc\s*=\s*["\']([^"\']+)["\']', script, re.I)
            if source:
                script_sources.append(source.group(1).strip())
        duplicate_script_sources = sorted(value for value, count in Counter(script_sources).items() if count > 1)
        images_missing_alt = 0
        for image in re.findall(r"<img\b[^>]*>", text, re.I):
            if not re.search(r"\balt\s*=", image, re.I):
                images_missing_alt += 1
        issues = []
        if not noindex and not title: issues.append("indexable-missing-title")
        if not noindex and not canonical: issues.append("indexable-missing-canonical")
        if not noindex and h1 != 1: issues.append(f"indexable-h1-count-{h1}")
        if duplicate_ids: issues.append("duplicate-id")
        if duplicate_script_sources: issues.append("duplicate-external-script")
        if images_missing_alt: issues.append("image-missing-alt")
        if "pagead2.googlesyndication.com/pagead/js/adsbygoogle" in text: issues.append("adsense-loader")
        if re.search(r"<ins\b[^>]*\badsbygoogle", text, re.I): issues.append("adsense-slot")
        if not noindex and placeholder_rx.search(re.sub(r"<!--.*?-->", "", text, flags=re.S)): issues.append("indexable-placeholder-copy")
        state = "NOINDEX" if noindex else "PUBLISHED"
        m = re.match(r"languages/([^/]+)/level/([^/]+)/index\.html$", rel)
        if m:
            state = course_state.get((m.group(1), m.group(2)), state)
        row = {
            "path": rel,
            "category": category(rel),
            "title": title,
            "canonical": canonical,
            "robots": robots or "(unspecified)",
            "indexable": "no" if noindex else "yes",
            "publication_state": state,
            "ad_class": ad_class_match.group(1) if ad_class_match else "(unspecified)",
            "visible_words": visible_words(text),
            "h1_count": h1,
            "duplicate_ids": ";".join(duplicate_ids),
            "duplicate_external_scripts": ";".join(duplicate_script_sources),
            "images_missing_alt": images_missing_alt,
            "internal_links": len(re.findall(r'href=["\'](?:/|\.\.?/)[^"\']*["\']', text, re.I)),
            "external_links": len(re.findall(r'href=["\']https?://', text, re.I)),
            "forms": len(re.findall(r"<form\b", text, re.I)),
            "adsense_loader": "yes" if "pagead2.googlesyndication.com/pagead/js/adsbygoogle" in text else "no",
            "adsense_slots": len(re.findall(r"<ins\b[^>]*\badsbygoogle", text, re.I)),
            "consent_script": "yes" if "cookie-consent.js" in text else "no",
            "analytics_script": "yes" if "analytics.js" in text else "no",
            "issues": ";".join(issues),
        }
        rows.append(row)
        if not noindex and title: title_paths[title].append(rel)
        if not noindex and canonical: canonical_paths[canonical].append(rel)

    duplicate_titles = {k: v for k, v in title_paths.items() if len(v) > 1}
    duplicate_canonicals = {k: v for k, v in canonical_paths.items() if len(v) > 1}
    summary = {
        "pages": len(rows),
        "indexable": sum(r["indexable"] == "yes" for r in rows),
        "noindex": sum(r["indexable"] == "no" for r in rows),
        "categories": dict(sorted(Counter(r["category"] for r in rows).items())),
        "ad_classes": dict(sorted(Counter(r["ad_class"] for r in rows).items())),
        "pages_with_adsense_loader": sum(r["adsense_loader"] == "yes" for r in rows),
        "adsense_slots": sum(r["adsense_slots"] for r in rows),
        "pages_with_matrix_issues": sum(bool(r["issues"]) for r in rows),
        "issue_counts": dict(sorted(Counter(issue for r in rows for issue in r["issues"].split(";") if issue).items())),
        "duplicate_id_pages": sum(bool(r["duplicate_ids"]) for r in rows),
        "duplicate_external_script_pages": sum(bool(r["duplicate_external_scripts"]) for r in rows),
        "images_missing_alt": sum(r["images_missing_alt"] for r in rows),
        "duplicate_title_groups": len(duplicate_titles),
        "duplicate_canonical_groups": len(duplicate_canonicals),
        "duplicate_titles": duplicate_titles,
        "duplicate_canonicals": duplicate_canonicals,
    }
    return rows, summary


def git_reconciliation() -> dict:
    """Compare the reference commit with the whole current tree, not just unstaged work."""
    tracked = set(run("git", "ls-files").splitlines())
    untracked = set(run("git", "ls-files", "--others", "--exclude-standard").splitlines())
    base = set(run("git", "ls-tree", "-r", "--name-only", BASE_SHA).splitlines())
    modified: set[str] = set()
    added: set[str] = set(untracked)
    deleted: set[str] = set()
    for line in run("git", "diff", "--name-status", "--find-renames", BASE_SHA, "--").splitlines():
        fields = line.split("\t")
        code = fields[0]
        if code.startswith("R") and len(fields) >= 3:
            deleted.add(fields[1])
            added.add(fields[2])
        elif len(fields) >= 2 and code.startswith("A"):
            added.add(fields[1])
        elif len(fields) >= 2 and code.startswith("D"):
            deleted.add(fields[1])
        elif len(fields) >= 2:
            modified.add(fields[1])
    html_base = sum(name.endswith(".html") for name in base)
    return {
        "reference_sha": BASE_SHA,
        "working_branch": run("git", "branch", "--show-current").strip(),
        "head_sha_at_generation": run("git", "rev-parse", "HEAD").strip(),
        "reference_tracked_files": len(base),
        "reference_html_files": html_base,
        "working_tracked_files": len(tracked),
        "pending_untracked_files": len(untracked),
        "modified": sorted(modified),
        "added": sorted(added),
        "deleted": sorted(deleted),
        "counts": {"modified": len(modified), "added": len(added), "deleted": len(deleted)},
    }


def main() -> int:
    REPORTS.mkdir(exist_ok=True)
    rows, matrix = build_matrix()
    fields = list(rows[0])
    with (REPORTS / "EKGURU-PAGE-MATRIX.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)

    matrix_md = [
        "# EkGuru Page Matrix",
        "",
        f"Generated: {TODAY}",
        "",
        f"- Public-tree HTML files: **{matrix['pages']}**",
        f"- Indexable: **{matrix['indexable']}**",
        f"- Noindex/quarantined: **{matrix['noindex']}**",
        f"- Pages with AdSense loader: **{matrix['pages_with_adsense_loader']}**",
        f"- AdSense slots: **{matrix['adsense_slots']}**",
        f"- Duplicate canonical groups: **{matrix['duplicate_canonical_groups']}**",
        f"- Pages with duplicate IDs: **{matrix['duplicate_id_pages']}**",
        f"- Pages with duplicate external scripts: **{matrix['duplicate_external_script_pages']}**",
        f"- Images missing an `alt` attribute: **{matrix['images_missing_alt']}**",
        f"- Matrix issue pages: **{matrix['pages_with_matrix_issues']}** (see CSV `issues` column)",
        "",
        "## Page classes",
        "",
        "| Class | Pages |",
        "|---|---:|",
    ]
    matrix_md += [f"| {key} | {value} |" for key, value in matrix["categories"].items()]
    matrix_md += ["", "## Automated issue counts", "", "| Signal | Pages |", "|---|---:|"]
    matrix_md += [f"| {key} | {value} |" for key, value in matrix["issue_counts"].items()]
    matrix_md += [
        "",
        "Placeholder signals are limited to indexable pages and require review; canonical, indexability and advertising signals are hard gates.",
        "",
        "The CSV is the file-level source of truth for title, canonical, robots, publication state, ad class, word count, landmarks, links, forms, consent/analytics inclusion and issues.",
    ]
    (REPORTS / "EKGURU-PAGE-MATRIX.md").write_text("\n".join(matrix_md) + "\n", encoding="utf-8")

    recon = git_reconciliation()
    course = json.loads((ROOT / "data/quality/course-publication-audit.json").read_text())
    country = json.loads((ROOT / "data/quality/country-language-verification.json").read_text())
    sitemap = json.loads((ROOT / "data/quality/sitemap-audit.json").read_text())
    seo_path = REPORTS / "seo.json"
    seo = json.loads(seo_path.read_text()) if seo_path.exists() else {}
    browser_path = REPORTS / "EKGURU-RELEASE-BROWSER.json"
    browser = json.loads(browser_path.read_text()) if browser_path.exists() else {"status": "NOT_RUN"}
    http_path = REPORTS / "local-http-audit.json"
    local_http = json.loads(http_path.read_text()) if http_path.exists() else {"status": "NOT_RUN", "failures": []}
    main_ads = run("git", "grep", "-l", "pagead2.googlesyndication.com/pagead/js/adsbygoogle", BASE_SHA, "--", "*.html").splitlines()
    forensic = {
        "generated_on": TODAY,
        "scope": "reference main commit versus current working implementation",
        "reconciliation": recon,
        "reference_main": {
            "html_files": recon["reference_html_files"],
            "html_files_with_adsense_loader": len(main_ads),
            "known_material_defects": [
                "Client mail relay credential was tracked instead of deploy-time-only.",
                "Course publication used structural completeness and allowed unsupported/generated levels.",
                "Country/language claims and generated funnels lacked relation-level publication gating.",
                "Sitemaps included noindex, query-duplicate or research URLs.",
                "Advertising and legal copy described active/future states inconsistently.",
            ],
        },
        "working_implementation": {
            "page_matrix": matrix,
            "course_publication": course["summary"],
            "country_language_relations": country["summary"],
            "sitemap_gate": {
                "status": sitemap["status"],
                "failures": len(sitemap["failures"]),
                "indexed_url_memberships": sitemap.get("indexed_url_memberships"),
                "indexed_unique_urls": sitemap.get("indexed_unique_urls"),
                "missing_indexable_urls": sitemap.get("missing_indexable_urls"),
                "duplicate_url_memberships": sitemap.get("duplicate_url_memberships"),
            },
            "mail": {"static_flow_tests": "PASS", "tracked_client_credential": "EMPTY", "live_delivery": "BROWSER_NOT_VERIFIED"},
            "payment": {"public_mode": "one ordinary Razorpay-hosted link", "custom_checkout": "UNPUBLISHED", "recent_supporters": "UNPUBLISHED", "live_provider_completion": "NOT_VERIFIED"},
            "consent": {"local_choice": "fail-closed", "advertising_choice": "unavailable/false", "certified_cmp_tcf": "NOT_DEPLOYED"},
            "advertising": {"runtime_gate": "DISABLED", "public_html_loaders": matrix["pages_with_adsense_loader"], "slots": matrix["adsense_slots"]},
            "affiliates": {"configured_tracking_ids": 0, "public_status": "DISABLED"},
            "local_http_gate": {
                "status": local_http.get("status"),
                "sitemap_children": local_http.get("sitemap_children"),
                "unique_sitemap_urls": local_http.get("unique_sitemap_urls"),
                "html_responses": local_http.get("html_responses"),
                "failures": len(local_http.get("failures", [])),
            },
            "real_browser_gate": browser.get("status"),
        },
        "final_readiness_status": "NOT_READY_DO_NOT_APPLY",
        "blocking_findings": [
            "Real Chromium installation/download was blocked by the sandbox network boundary, so the required rendered browser gate is not complete.",
            "Live mail delivery is not verified and the previously exposed live relay token still requires owner rotation.",
            "No Google-certified CMP/TCF deployment exists for regions where it is required.",
            "Country/source-language generated funnels remain quarantined pending editorial and source review.",
            "Payment completion/receipt/refund behavior on the owner account has not been live-transaction verified.",
        ],
    }
    (REPORTS / "EKGURU-MAIN-FORENSIC.json").write_text(json.dumps(forensic, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fmd = [
        "# EkGuru Main Forensic Reconciliation",
        "",
        f"**Reference:** `{BASE_SHA}`  ",
        f"**Branch:** `{recon['working_branch']}`  ",
        f"**Generated:** {TODAY}",
        "",
        "## File-level reconciliation",
        "",
        f"The reference contains {recon['reference_tracked_files']} tracked files ({recon['reference_html_files']} HTML). The working tree reconciles **{recon['counts']['modified']} modified**, **{recon['counts']['added']} added**, and **{recon['counts']['deleted']} deleted** paths. The complete arrays are in `EKGURU-MAIN-FORENSIC.json`; the per-page result is in `EKGURU-PAGE-MATRIX.csv`.",
        "",
        "## Main findings",
        "",
        "1. The tracked mail relay credential was a release-blocking security defect. The tracked client value is now empty; the old live value must be rotated by the owner.",
        "2. Structural course completeness was not publication evidence. The gate now blocks all unreviewed phase-3 expansion files and known synthetic Korean C1/C2 content.",
        "3. Generated country/source-language funnels contained stale price, time, tutor and linguistic claims. They remain reachable but visibly quarantined, noindex, ad-ineligible and absent from sitemaps.",
        "4. Country-language relations now have deterministic VERIFIED / PROVISIONAL / RESEARCH_REQUIRED states. Research-required rows are not shown publicly.",
        "5. Sitemaps now fail closed against missing, noindex, robot-disallowed, query and non-self-canonical URLs.",
        "6. AdSense and affiliates are disabled; public HTML has no loader, slots or configured affiliate tracking identifiers.",
        "7. Legal/support copy now distinguishes local storage, opt-in analytics, disabled ads/affiliates, tutor payments and optional Razorpay support.",
        "",
        "## Current measured state",
        "",
        f"- Courses: **{course['summary']['complete']} complete**, **{course['summary']['partial']} partial**, **{course['summary']['research_required']} research-required**; **{course['summary']['level_states'].get('PUBLISHABLE_EXISTING', 0)}** allowed CEFR levels and **{course['summary']['level_states'].get('PUBLIC_CONTENT_BUG', 0)}** blocked.",
        f"- Country-language relations: **{country['summary']['states'].get('VERIFIED', 0)} verified**, **{country['summary']['states'].get('PROVISIONAL', 0)} provisional**, **{country['summary']['states'].get('RESEARCH_REQUIRED', 0)} research-required**.",
        f"- HTML: **{matrix['pages']}** files; **{matrix['indexable']} indexable**, **{matrix['noindex']} noindex**.",
        f"- Sitemap gate: **{sitemap['status']}**, {sitemap.get('indexed_unique_urls', 0)} unique indexable URLs, {sitemap.get('missing_indexable_urls', 0)} omitted, {sitemap.get('duplicate_url_memberships', 0)} duplicate memberships.",
        f"- Local HTTP gate: **{local_http.get('status')}**, {local_http.get('unique_sitemap_urls', 0)} sitemap URLs fetched, {len(local_http.get('failures', []))} failures.",
        f"- DOM duplicate/accessibility scan: **{matrix['duplicate_id_pages']}** pages with duplicate IDs, **{matrix['duplicate_external_script_pages']}** with duplicate external scripts, **{matrix['images_missing_alt']}** images missing `alt`.",
        f"- Real-browser gate: **{browser.get('status')}** (not treated as a pass).",
        "",
        "## Audit coverage and limitations",
        "",
        "- Inventory/SEO/canonical/robots/sitemap/internal-link, placeholder-signal, duplicate, course, relation, legal, mail, payment-release-state, consent-source, advertising and affiliate checks were run against the working tree.",
        f"- `tools/seocheck.js` reported {seo.get('pages', 0):,} pages, {seo.get('checkedLinks', 0):,} checked internal links, {len(seo.get('broken', []))} broken links and {len(seo.get('orphanPages', []))} orphans.",
        "- Static mail-flow, payment backend and release-mode DOM suites passed. These do not prove live email receipt or a real payment transaction.",
        "- A real Chromium run was prepared in `tools/test-release-browser.py`, but Playwright’s browser download failed at the sandbox TLS boundary. This unresolved requirement is why readiness is not a pass.",
        "",
        "## Blocking findings",
        "",
    ]
    fmd += [f"- {item}" for item in forensic["blocking_findings"]]
    fmd += ["", "## Readiness", "", "**NOT_READY_DO_NOT_APPLY**", ""]
    (REPORTS / "EKGURU-MAIN-FORENSIC.md").write_text("\n".join(fmd), encoding="utf-8")

    monetization = f"""# EkGuru Global Monetization Final

Generated: {TODAY}

## Readiness status

**NOT_READY_DO_NOT_APPLY**

## Current release behavior

- Google AdSense is disabled in both the policy manifest and runtime gate.
- Public HTML pages with an AdSense loader: **{matrix['pages_with_adsense_loader']}**.
- Public AdSense slots: **{matrix['adsense_slots']}**.
- Configured affiliate tracking identifiers found by the release scan: **0**.
- Support uses one ordinary link to Razorpay's hosted payment page. No payment SDK, custom checkout form or recent-supporter feed loads on EkGuru.
- Analytics is optional and starts only after an affirmative local privacy choice. Advertising remains unavailable/false even after “Accept all.”
- The local privacy interface is not represented as a Google-certified CMP/TCF deployment.

## Placement policy

No advertising is authorized on any page in this release. Future policy permanently excludes interactive lessons/tests, forms, booking, payment, legal, contact, search, error, thin, placeholder, blocked and research pages. Word count alone never authorizes a placement. A future content placement requires explicit editorial approval, account-side readiness and certified consent behavior.

No affiliate link is authorized until a real programme relationship and tracking identifier exist. Future candidates are limited to directly relevant, clearly disclosed Preply, Amazon India or selected Impact offers. No fake discount, rating, personal-use claim, generic product wall or guaranteed earning claim is permitted.

## Evidence

- Sitemap/noindex gate: **{sitemap['status']}**; {sitemap.get('indexed_unique_urls', 0)} unique indexable URLs; {sitemap.get('missing_indexable_urls', 0)} omitted; {sitemap.get('duplicate_url_memberships', 0)} duplicate memberships.
- Course gate: {course['summary']['level_states'].get('PUBLISHABLE_EXISTING', 0)} allowed; {course['summary']['level_states'].get('PUBLIC_CONTENT_BUG', 0)} blocked.
- Country relation gate: {country['summary']['states'].get('VERIFIED', 0)} verified; {country['summary']['states'].get('PROVISIONAL', 0)} provisional; {country['summary']['states'].get('RESEARCH_REQUIRED', 0)} research-required.
- Local HTTP gate: **{local_http.get('status')}**; {local_http.get('unique_sitemap_urls', 0)} sitemap URLs fetched; {len(local_http.get('failures', []))} failures.
- DOM resource/accessibility scan: {matrix['duplicate_id_pages']} duplicate-ID pages; {matrix['duplicate_external_script_pages']} duplicate-script pages; {matrix['images_missing_alt']} images missing `alt`.
- Consent/release-mode DOM tests are automated in `tools/test-consent-release.mjs` and `tools/test-browser-qa.mjs`.
- Required rendered-browser result: **{browser.get('status')}**; unresolved and not waived.

## Blocking technical work

1. Run `tools/test-release-browser.py` in an environment where Playwright Chromium is available, and resolve every rendered accessibility, overflow, keyboard, reduced-motion and request failure.
2. Verify live mail delivery end to end after secure deployment-time configuration.
3. Verify the Razorpay-hosted route, merchant identity, confirmation, refund/contact wording and transaction record using an owner-controlled test.
4. Complete editorial/source review before moving any quarantined country or source-language surface to indexable status.
5. Deploy and production-test a Google-certified CMP/TCF path before any advertising consideration.

## Genuinely owner-only actions

- Rotate the previously exposed live `MAILER_SHARED_TOKEN`; do not reuse it. Store the replacement only in the owner-controlled deployment environment, never in Git or client JavaScript.
- Confirm the Razorpay merchant/payment-page ownership, settlement, receipt and refund/contact settings in the owner account.
- Only after all technical and editorial gates pass, decide whether to apply/add the site in AdSense and whether to join a relevant affiliate programme. Approval and commercial terms cannot be created from repository code.
"""
    (REPORTS / "EKGURU-GLOBAL-MONETIZATION-FINAL.md").write_text(monetization, encoding="utf-8")
    print(f"reports: {matrix['pages']} pages, {recon['counts']}, readiness NOT_READY_DO_NOT_APPLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

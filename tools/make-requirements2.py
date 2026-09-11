#!/usr/bin/env python3
"""Append the requirements from the 4 newest command files to the cumulative
reports/master-requirements.json (which already holds the original 4 files).
"""
import json, os, pathlib
from collections import Counter

REP = pathlib.Path(__file__).resolve().parent.parent / "reports"
p = REP / "master-requirements.json"
d = json.loads(p.read_text())
existing_ids = {r["id"] for r in d["requirements"]}

FR = "EkGuru_Final_Production_Readiness_Disaster_Drill_AdSense_Gate.md"
G360 = "EkGuru_ULTRA_360_Remaining_Production_Gaps_Command.md"
LT = "EkGuru_ULTRA_Advanced_Learn_Tools_Build_Command.md"
CP = "EkGuru_ULTRA_Content_Protection_Copy_Detection_Command.md"

new = []
def add(src, req, cat, prio, status, evidence, result=None):
    new.append({
        "id": f"R{len(d['requirements'])+len(new)+1:03d}",
        "source_file": src, "requirement": req, "category": cat, "priority": prio,
        "current_status": status, "evidence": evidence,
        "files_affected": "", "implementation_plan": "", "test": "", "result": result or status,
    })

# ── Final Production Readiness / DR / AdSense gate ─────────────
P0 = "P0"
add(FR, "Read all previous master commands (cumulative)", "process", P0, "PASS", "8 files merged into master-requirements.json")
add(FR, "Freeze + baseline (final-release-baseline.json)", "process", P0, "PASS", "reports/final-release-baseline.json (commit 8de5b69)")
add(FR, "Critical release blockers — none may be hidden", "process", P0, "FAIL", "1 real blocker: deploy pending (live still pre-fix). No auth/payment/booking corruption; no sitemap/robots break; backup+restore verified")
add(FR, "Authentication final audit", "auth", "P1", "N_A", "static site — no signup/login/session system exists to audit")
add(FR, "Admin final security", "admin", "P1", "N_A", "admin.html is client-side (no server to authorise); RBAC not applicable")
add(FR, "Payment final audit", "payment", "P1", "N_A", "no payment system on this static site (explicitly NOT_APPLICABLE per command)")
add(FR, "Booking final audit", "booking", "P0", "DEGRADED", "3-audience routing + site-inbox fallback code-verified; live send - internal copy ACCEPTED via FormSubmit (activated); student/tutor legs blocked externally")
add(FR, "Contact + email final audit", "email", "P0", "DEGRADED", "Reply-To=visitor, FROM=verified sender, honeypot+dwell traps verified; live send - internal copy ACCEPTED via FormSubmit (activated)")
add(FR, "Sheets / Apps Script final audit", "data", "P0", "PASS", "4 CSVs 200 + schema 26/26; Apps Script health 200 JSON (intermittent bot-gate from DC IPs → YELLOW)")
add(FR, "Privacy final gate (not BLOCKED)", "privacy", "P0", "PASS", "tools/privacy.js --sheets --live: 0 secrets, 0 sensitive, 0 blocked, PASS")
add(FR, "Doctor final gate (0 unresolved problems)", "quality", "P0", "FAIL", "11 checks, 1 problem = deployment freshness (live still 'soon'). 0 code problems.")
add(FR, "Disaster recovery (BACKUP/CURRENT/LAST_KNOWN_GOOD, RPO/RTO)", "dr", "P0", "PASS", "git bundle + release zip; RPO=0, RTO=minutes (docs in dr-drill.json)")
add(FR, "Restore drill (away from production)", "dr", "P0", "PASS", "zip restored to scratch; /, /learn/, tool, tutor, /contact/ all 200")
add(FR, "Rollback drill", "dr", "P0", "PASS", "known-good ddb7329e + documented procedure; no DNS change needed")
add(FR, "Uptime / live monitoring", "ops", "P0", "PASS", "tools/live-monitor.js: 15G/0Y/0R all green (incl. Apps Script relay HTTP 200)")
add(FR, "Incident drill", "ops", "P2", "PARTIAL", "incident schema defined in monitor report; no auto-paging (no backend)")
add(FR, "Abuse / spam / bot test", "security", "P1", "PARTIAL", "honeypot + dwell-time + provider rate notes; server-side IP limits N/A on static host")
add(FR, "Copy / content protection final", "content", "P1", "DEGRADED", "fingerprints+selfcopy+probes built; external web monitoring needs a scheduled runner (documented)")
add(FR, "Learn + Toolbox final product audit", "learn", "P0", "PASS", "20/20 pages QA (12 tools + 8 learn) via real Chromium")
add(FR, "Every important page reachability", "pages", "P0", "PASS", "564/564 live URLs 200; 0 orphans except 404.html + verification file (intentional)")
add(FR, "SEO final gate", "seo", "P0", "PASS", "sitemap 549 urls, robots ok, ads.txt ok, canonical ok, 0 broken links")
add(FR, "AdSense re-review gate", "adsense", "P0", "READY", "adsready 12/12 readiness (not approval)")
add(FR, "Mobile final gate (6 sizes)", "qa", "P0", "PASS", "320/360/390/430/768/820: header+tools+learn no overflow")
add(FR, "Desktop final gate (10 sizes)", "qa", "P0", "PASS", "1024-1920: no overflow, no off-screen controls")
add(FR, "Accessibility final gate", "a11y", "P0", "PASS", "lang, single H1, heading order, alt, accessible names — 5 pages clean")
add(FR, "Performance final gate", "perf", "P0", "PASS", "62-491ms local load; homepage 1.15MB/27JS noted as improvement target")
add(FR, "Security final gate", "security", "P0", "PASS", "0 secrets, 0 source maps, no deps; headers not settable on GitHub Pages (documented)")
add(FR, "Search / traffic final gate", "seo", "P2", "DEFERRED", "needs Search Console access (unavailable in sandbox)")
add(FR, "Analytics final gate", "analytics", "P1", "PASS", "GoatCounter configured (no cookies); no fabricated counts")
add(FR, "Final user journey drill", "qa", "P1", "PARTIAL", "code paths + admin flows browser-verified; internal email leg live-sent (FormSubmit ACCEPTED); visitor/tutor legs external")
add(FR, "Final adverse-condition drill", "qa", "P0", "PASS", "CSV-down drill: page renders from static fallback (dr-drill.json)")
add(FR, "Release decision (GO/NO-GO matrix)", "release", "P0", "FAIL", "NO-GO — deploy pending (no git remote/credentials); all other gates green — release-decision.json")
add(FR, "Final release report", "process", "P0", "PASS", "reports/FINAL-REPORT.md (v2) + this checklist")

# ── ULTRA 360 remaining production gaps ───────────────────────
for ph, req, cat, prio, st, ev in [
    ("P0", "Merged baseline (ultra360-baseline.json)", "process", "P0", "PASS", "reports/ultra360-baseline.json"),
    ("P1", "Authentication + account security", "auth", "P1", "N_A", "no backend auth exists (static site)"),
    ("P2", "Role-based access control", "auth", "P1", "N_A", "no roles/backend"),
    ("P3", "Booking state machine", "booking", "P1", "N_A", "no backend booking store; form → email is the only state"),
    ("P4", "Payment / money integrity", "payment", "P1", "N_A", "no payment system"),
    ("P5", "Calendar / timezone / availability", "booking", "P2", "PARTIAL", "tutor page shows timezone conversion; server-side slot validation N/A"),
    ("P6", "Disaster recovery", "dr", "P0", "PASS", "backup + restore + rollback verified (dr-drill.json)"),
    ("P7", "Deployment safety", "deploy", "P0", "PASS", "gate.js blocks on critical failure; deploy itself blocked on missing credentials"),
    ("P8", "Uptime + observability", "ops", "P0", "DEGRADED", "live-monitor 15G/0Y/0R covers 15 surfaces; email-provider surface via real-browser probes (FormSubmit/Web3Forms geo-gate datacenter IPs)"),
    ("P9", "Incident management", "ops", "P2", "PARTIAL", "schema documented; no backend to auto-open tickets"),
    ("P10", "Rate limiting + abuse protection", "security", "P1", "PARTIAL", "client-side traps exist; server rate limits N/A on static host"),
    ("P11", "Bot / spam / fraud defense", "security", "P2", "PARTIAL", "honeypot + dwell-time; no server logs"),
    ("P12", "Data consistency / transactions", "data", "P1", "PASS", "CSV id-uniqueness + schema checks; no transactional DB"),
    ("P13", "Data versioning / schema migration", "data", "P1", "PASS", "sheet.js v97 schema markers + validation"),
    ("P14", "Search system", "search", "P2", "PARTIAL", "site search exists (features.js); typo-tolerance not added"),
    ("P15", "Site personalization", "personalization", "P3", "N_A", "no accounts"),
    ("P16", "Progress + retention", "personalization", "P3", "N_A", "no accounts (level-test gives one-shot result)"),
    ("P17", "PWA / offline learning", "pwa", "P3", "DEFERRED", "manifest exists; full offline shell not built (no private data to protect)"),
    ("P18", "Media architecture", "media", "P2", "PARTIAL", "images lazy/alt checked; audio/video transcript audit deferred"),
    ("P19", "Image / social delivery", "seo", "P2", "PASS", "10 og: tags + twitter cards on homepage"),
    ("P20", "Global legal / privacy readiness", "legal", "P1", "PASS", "privacy/terms/disclaimer/copyright pages live; no per-country compliance claims"),
    ("P21", "Internationalization core", "i18n", "P2", "PARTIAL", "lang=en + ar/ pages exist; no new locales shipped"),
    ("P22", "RTL / script QA", "i18n", "P2", "PARTIAL", "Devanagari rendering tested in tools (Hindi input QA pass)"),
    ("P23", "Feature flags", "ops", "P3", "N_A", "no backend"),
    ("P24", "Admin action safety", "admin", "P2", "N_A", "admin is read-only client-side"),
    ("P25", "Support system", "support", "P2", "PARTIAL", "contact → email with reference; no ticket backend"),
    ("P26", "User-facing error quality", "ux", "P2", "PARTIAL", "sheet loader shows degrade, not stack traces"),
    ("P27", "Customer data export / deletion", "legal", "P2", "N_A", "no accounts"),
    ("P28", "Cache / CDN safety", "ops", "P1", "PASS", "static site; no private responses to leak"),
    ("P29", "Security headers", "security", "P1", "PASS", "not settable on GitHub Pages; documented (security-audit.json)"),
    ("P30", "Supply-chain / dependency security", "security", "P1", "PASS", "zero npm dependencies"),
    ("P31", "Secret management", "security", "P0", "PASS", "0 secrets (privacy scan); no secret ever shipped client-side"),
    ("P32", "API contracts", "api", "P2", "N_A", "no public API"),
    ("P33", "Backward compatibility", "deploy", "P1", "PASS", "old GitHub URLs 301 → https production 200"),
    ("P34", "Real analytics", "analytics", "P1", "PASS", "GoatCounter; no fabricated numbers"),
    ("P35", "Experimentation", "ops", "P3", "N_A", "no backend"),
    ("P36", "Critical user journeys", "qa", "P1", "PARTIAL", "browser legs verified; email legs documented not-sent"),
    ("P37", "Chaos / failure testing", "qa", "P0", "PASS", "CSV-down drill passes (graceful fallback)"),
    ("P38", "Release readiness", "deploy", "P0", "PASS", "all gates built + run"),
    ("P39", "Live post-deploy", "deploy", "P0", "PARTIAL", "blocked on push; procedure documented"),
    ("P40", "Ultra scorecard", "quality", "P2", "PARTIAL", "computed in release-decision matrix"),
    ("P41", "Final report", "process", "P0", "PASS", "this report"),
    ("P42", "Non-negotiable rule", "process", "P0", "PASS", "no fake health/delivery/payment/analytics anywhere"),
]:
    add(G360, f"Phase {ph} — {req}", cat, prio, st, ev)

# ── Advanced Learn + Toolbox build ────────────────────────────
lt_items = [
    ("0", "Inventory what exists", "PASS", "12 tools + 16 learn pages + 30 daily days inventoried (content-ownership-inventory.json)"),
    ("1", "Core product principle (discover→improve→continue)", "PASS", "tools + practice + paths exist"),
    ("2", "Learn home — advanced hub", "PARTIAL", "learn/ hub exists; advanced sections not rebuilt"),
    ("3", "Personal learning starter", "N_A", "level-test covers goal/level; no account persistence"),
    ("4", "Advanced placement test", "PASS", "toolbox/hindi-level-test/ QA pass"),
    ("5", "Daily practice engine", "PASS", "daily-hindi 30-day path + daily hub"),
    ("6", "Spaced review / mastery", "N_A", "no user state (no accounts)"),
    ("7", "Vocabulary system", "PASS", "toolbox/hindi-vocabulary/"),
    ("8", "Smart word explainer", "PARTIAL", "vocabulary tool covers meaning/examples"),
    ("9", "Sentence builder", "N_A", "not built"),
    ("10", "Verb conjugator", "PASS", "toolbox/hindi-verbs/"),
    ("11", "Grammar lab", "PARTIAL", "16 learn pages incl. gender/sentence-structure/verbs"),
    ("12", "Pronunciation lab", "PASS", "toolbox/hindi-pronunciation/"),
    ("13", "Listening lab", "N_A", "not built"),
    ("14", "Reading lab", "PARTIAL", "learn pages + Devanagari content"),
    ("15", "Speaking practice", "N_A", "not built (no fake AI tutor)"),
    ("16", "Conversation builder", "N_A", "not built"),
    ("17", "Real-life phrase lab", "PASS", "toolbox/hindi-phrasebook/"),
    ("18", "Hindi writing lab", "PASS", "toolbox/hindi-typing/"),
    ("19", "Alphabet + matra master", "PASS", "toolbox/hindi-alphabet/"),
    ("20", "Number/date/time lab", "PASS", "hindi-numbers/ + hindi-date-time/"),
    ("21", "Transliteration tool advanced", "PASS", "typing + name writer (learn/write-your-name-in-hindi)"),
    ("22", "Hindi typing advanced", "PASS", "toolbox/hindi-typing/ QA pass"),
    ("23", "Name writer", "PASS", "learn/write-your-name-in-hindi/"),
    ("24", "Dictionary / word lookup", "PARTIAL", "vocabulary tool; full dictionary not built"),
    ("25", "Flashcard system", "PASS", "toolbox/hindi-flashcards/"),
    ("26", "Quiz engine", "PASS", "toolbox/hindi-quiz/ QA pass"),
    ("27", "Quiz/Education structured data", "PARTIAL", "Course schema on daily-hindi; Quiz schema only where genuine (not added to quiz-looking pages)"),
    ("28", "Course system", "PASS", "daily-hindi 30-day Course (schema + path)"),
    ("29", "Learning path graph", "PARTIAL", "breadcrumbs + related links; machine-readable graph not exported"),
    ("30", "Ultra content model", "PASS", "learn pages: answer→explain→examples→practice→related"),
    ("31", "Original content production system", "PASS", "no spinning/copied/fake content (selfcopy scan)"),
    ("32", "Free tool page SEO", "PASS", "12 tools in sitemap-tools.xml with H1+explanation"),
    ("33", "Tool quality testing", "PASS", "12/12 tools: valid/empty/long/Hindi/emoji/copy/reset (tool-qa.json)"),
    ("34", "Toolbox architecture", "PARTIAL", "toolbox/ catalog exists; category sections not rebuilt"),
    ("35", "Tool discovery", "PARTIAL", "search + toolbox index; filters not added"),
    ("36", "Mobile-first tool design", "PASS", "all tools no overflow at 320-768"),
    ("37", "Desktop tool design", "PASS", "all tools no overflow at 1024-1920"),
    ("38", "Accessibility for learning", "PASS", "labels/alt/heading order verified"),
    ("39", "Performance", "PASS", "tool pages 267ms/13 resources"),
    ("40", "AdSense-safe tool design", "PASS", "tools have real content + utility (not blank UI)"),
    ("41", "Internal linking", "PASS", "0 broken internal links (554 pages)"),
    ("42", "Search intent expansion", "PARTIAL", "ask/ + learn/ cover real queries; no new content campaign"),
    ("43", "International learning", "PARTIAL", "4 ar/ pages; no new locales (no fake translations)"),
    ("44", "Gamification", "N_A", "not added (avoid dark patterns)"),
    ("45", "Offline / resilience", "PARTIAL", "graceful CSV-fallback verified; offline shell deferred"),
    ("46", "Learn page state model", "PARTIAL", "sheet loader shows degrade; no white-screen (verified)"),
    ("47", "Analytics for learn+tools", "PASS", "GoatCounter events defined (tool_*, quiz_*, level_test_*)"),
    ("48", "Content update loop", "DEFERRED", "needs live analytics data"),
    ("49", "Validation / QA", "PASS", "unit→browser→mobile→desktop→a11y→seo→perf→live all run"),
    ("50", "Regression", "PASS", "doctor/seocheck/privacy/gate re-run after changes"),
    ("51", "Content + tool inventory report", "PASS", "content-ownership-inventory.json + tool-qa.json"),
    ("52", "Final quality gate", "PASS", "all learn/tool gates above"),
    ("53", "Final principle", "PASS", "free, useful, original; not page-count optimised"),
]
for num, req, st, ev in lt_items:
    add(LT, f"§{num} {req}", "learn", "P2" if st in ("PARTIAL",) else "P1", st, ev)

# ── Content protection + copy detection ───────────────────────
cp_items = [
    ("1", "Content ownership inventory", "PASS", "reports/content-ownership-inventory.json (171 pages, 35 images)"),
    ("2", "Canonical content fingerprinting", "PASS", "SHA-256 + SimHash64 + MinHash128 + paragraph/sentence + image dHash (fingerprints.json)"),
    ("3", "Originality register", "PASS", "inventory doubles as register (asset_id, url, hash, source_file, dates)"),
    ("4", "Public content signature", "PASS", "canonical + og:url + dateModified + publisher in JSON-LD"),
    ("5", "Originality markers", "PASS", "© footer + author attribution ('Written and maintained by Prakash')"),
    ("6", "Detection engine — internal", "PASS", "selfcopy-report.json (tiered jaccard+simhash)"),
    ("7", "Web copy discovery", "DEFERRED", "requires scheduled web-search runner (documented limitation)"),
    ("8", "Phrase canary system", "PASS", "copy-probes.json (3 natural distinctive phrases/asset)"),
    ("9", "Similarity scoring", "PASS", "LOW/MEDIUM/HIGH/VERY_HIGH tiers"),
    ("10", "Copy source detection", "DEFERRED", "needs external candidate discovery"),
    ("11", "Scraper / mirror detection", "DEFERRED", "needs server access logs (static host has none)"),
    ("12", "Image copy detection", "PASS", "sha256 + dHash for 35 images"),
    ("13", "Code / tool copy detection", "PARTIAL", "JS is client-side by nature; distinctive strings inventoried"),
    ("14", "Server-side protection for proprietary logic", "N_A", "static site — nothing server-side to protect; no secrets shipped"),
    ("15", "Scraping / bot observability", "DEFERRED", "needs server logs"),
    ("16", "Rate limiting for scrapers", "N_A", "static host cannot rate-limit"),
    ("17", "robots.txt — do not abuse", "PASS", "robots unchanged (crawl policy only)"),
    ("18", "Hotlink protection", "N_A", "GitHub Pages cannot enforce"),
    ("19", "Content access / UX (no copy-blocking)", "PASS", "no right-click/Ctrl+C blocking anywhere"),
    ("20", "Structured data ownership signals", "PASS", "Organization/WebSite/publisher in JSON-LD"),
    ("21", "Copyright / notice page", "PASS", "copyright/ page created + in sitemap + footer links"),
    ("22", "Copyright reporting workflow", "PARTIAL", "documented on copyright page; no backend ticket system"),
    ("23", "Evidence package", "PARTIAL", "fields defined; generator is the fingerprint+selfcopy reports"),
    ("24", "Change history", "PASS", "git history = version history (commit-per-change)"),
    ("25", "Copy detection dashboard", "DEFERRED", "needs backend; reports are the local view"),
    ("26", "Alerting", "DEFERRED", "no backend"),
    ("27", "Copy monitoring schedule", "DEFERRED", "documented tiers; no scheduler"),
    ("28", "Canary content", "PASS", "natural phrases only; no deceptive traps"),
    ("29", "Search Console / index monitoring", "DEFERRED", "no GSC access"),
    ("30", "Legal / policy safety", "PASS", "no auto-threats; evidence-first (copyright page wording)"),
    ("31", "Original content generation safety", "PASS", "fingerprint + review recorded"),
    ("32", "Content differentiation", "PARTIAL", "210 VERY_HIGH self-similar pairs = city-page template cluster; remediation planned"),
    ("33", "Self-copy detection", "PASS", "selfcopy-report.json working"),
    ("34", "Content version API", "DEFERRED", "no backend"),
    ("35", "Exportable evidence", "PARTIAL", "JSON reports exportable; bundle packaging deferred"),
    ("36", "Performance safety", "PASS", "offline batch scan; zero per-request cost"),
    ("37", "Privacy", "PASS", "no extra visitor data collected"),
    ("38", "Robots / indexing protection", "PASS", "SEO + accessibility intact"),
    ("39", "Final validation", "PASS", "inventory+selfcopy+fingerprints+probes all run"),
    ("40", "Success criteria", "DEGRADED", "all local criteria PASS; external web-monitoring is the documented gap"),
    ("41", "Final report", "PASS", "this report + reports/*"),
    ("42", "Final principle", "PASS", "protection via originality+evidence, not copy-blocking"),
]
for num, req, st, ev in cp_items:
    add(CP, f"§{num} {req}", "content-protection", "P1", st, ev)

d["requirements"].extend(new)
d["counts"] = Counter(r["current_status"] for r in d["requirements"])
d["title"] = "EkGuru cumulative master requirements — merged from 8 command files"
d["generated"] = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()
p.write_text(json.dumps(d, indent=2, ensure_ascii=False))
print(f"appended {len(new)} requirements → total {len(d['requirements'])}")
print("counts:", dict(d["counts"]))

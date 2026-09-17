#!/usr/bin/env python3
"""Phase-2 baseline: measure the current repository with real numbers.
Writes reports/major-update-phase2-baseline.json and
reports/content-quality-before.json and reports/tool-inventory-phase2.json.
"""
import json, os, re, sys, time

ROOT = "/home/user/EkGuru"
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

SECTIONS = {
    "home": ["index.html"],
    "learn": ["learn/"],
    "learn_topics": ["learn/"],           # the 16 topic dirs under learn/ (non index/paths/practice)
    "hindi_topics": ["hindi/"],
    "ask": ["ask/"],
    "answers": ["answers/"],
    "daily_hindi": ["daily-hindi/"],
    "tutor": ["tutor/"],
    "toolbox": ["toolbox/"],
    "practice": ["learn/practice/"],
    "paths": ["learn/paths/"],
    "materials": ["materials/"],
    "hindi_tutor_cities": ["hindi-tutor/"],
    "learn_from_country": ["learn-hindi-by-country/"],
    "learn_for_speakers": ["learn-hindi-for-speakers/"],
    "learn_for_X_speakers": ["learn-hindi-for-arabic-speakers/"],
    "misc": ["about/", "contact/", "search/", "privacy/", "terms/", "disclaimer/", "copyright/", "name-in-hindi/"],
    "localized": ["ar/", "bn/", "de/", "es/", "fr/", "id/", "it/", "ja/", "ko/", "pl/", "pt/", "ru/", "tr/", "ur/", "vi/", "zh/"],
}

def walk(prefix):
    out = []
    p = os.path.join(ROOT, prefix)
    if not os.path.isdir(p):
        return out
    for dp, dn, fn in os.walk(p):
        dn[:] = [d for d in dn if d not in (".git", "node_modules")]
        for f in fn:
            if f.endswith(".html"):
                out.append(os.path.join(dp, f))
    return out

def count_pages():
    counts = {}
    for name, prefixes in SECTIONS.items():
        files = []
        for pre in prefixes:
            p = os.path.join(ROOT, pre)
            if os.path.isdir(p):
                files += walk(pre)
            elif pre.endswith(".html") and os.path.exists(p):
                files.append(p)
        counts[name] = len(set(files))
    return counts

TEXT_RE = re.compile(r"<(script|style|noscript)[^>]*>.*?</\1>", re.S)
TAG_RE = re.compile(r"<[^>]+>")

def page_stats(path):
    try:
        html = open(path, encoding="utf-8").read()
    except Exception:
        return None
    html_ns = TEXT_RE.sub(" ", html)
    # main or article or body
    m = re.search(r"<(main|article)[^>]*>(.*?)</\1>", html_ns, re.S)
    if m:
        content = m.group(2)
    else:
        b = re.search(r"<body[^>]*>(.*?)</body>", html_ns, re.S)
        content = b.group(1) if b else html_ns
    text = TAG_RE.sub(" ", content)
    text = re.sub(r"\s+", " ", text).strip()
    words = len(text.split())
    h2 = len(re.findall(r"<h2\b", content))
    h3 = len(re.findall(r"<h3\b", content))
    tables = len(re.findall(r"<table\b", content))
    lists = len(re.findall(r"<(ul|ol)\b", content))
    deva = len(re.findall(r"class=\"[^\"]*(dv|deva|hi-text)[^\"]*\"", content))
    links_in = len(re.findall(r"<a\b", content))
    links_out = len(re.findall(r'<a[^>]+href="(?:\.\./|\./|/)[^"]*"', content))
    examples = len(re.findall(r"example|example:|for example|e\.g\.", text, re.I))
    size = os.path.getsize(path)
    return {
        "words": words, "h2": h2, "h3": h3, "tables": tables, "lists": lists,
        "devanagariSpans": deva, "links": links_in, "internalLinks": links_out,
        "examples": examples, "bytes": size
    }

def classify(st):
    if st is None:
        return ("REMOVE", "unreadable")
    if st["words"] < 120:
        return ("REMOVE", "very thin (<120 words)")
    if st["words"] < 250:
        return ("IMPROVE", "thin (<250 words)")
    if st["h2"] + st["h3"] < 2:
        return ("IMPROVE", "no headings/structure")
    if st["examples"] == 0 and st["words"] < 600:
        return ("IMPROVE", "no examples")
    if st["internalLinks"] < 3:
        return ("IMPROVE", "weak internal linking")
    return ("KEEP", "adequate depth")

def section_report(prefixes, label, maxn=100000):
    files = []
    for pre in prefixes:
        p = os.path.join(ROOT, pre)
        if os.path.isdir(p):
            files += walk(pre)
        elif os.path.exists(p) and p.endswith(".html"):
            files.append(p)
    files = sorted(set(files))
    rows = []
    for f in files:
        st = page_stats(f)
        rel = os.path.relpath(f, ROOT)
        action, reason = classify(st)
        rows.append({"page": rel, "stats": st, "action": action, "reason": reason})
    keep = [r for r in rows if r["action"] == "KEEP"]
    impr = [r for r in rows if r["action"] == "IMPROVE"]
    rem  = [r for r in rows if r["action"] == "REMOVE"]
    words = [r["stats"]["words"] for r in rows if r["stats"]]
    return {
        "label": label, "count": len(rows),
        "keep": len(keep), "improve": len(impr), "remove": len(rem),
        "avgWords": round(sum(words)/len(words), 1) if words else 0,
        "minWords": min(words) if words else 0, "maxWords": max(words) if words else 0,
        "improveList": [{"page": r["page"], "reason": r["reason"], "words": r["stats"]["words"]} for r in impr][:60],
        "removeList": [{"page": r["page"], "reason": r["reason"], "words": r["stats"]["words"]} for r in rem][:40],
    }

def tool_inventory():
    # parse js/tool-registry.js
    reg = open(os.path.join(ROOT, "js/tool-registry.js"), encoding="utf-8").read()
    tools = []
    for m in re.finditer(r"\{\s*slug:\s*\"([^\"]+)\",\s*name:\s*\"([^\"]+)\",\s*path:\s*\"([^\"]+)\",\s*category:\s*\"([^\"]+)\",\s*version:\s*\"([^\"]+)\".*?last_tested:\s*\"([^\"]+)\"", reg, re.S):
        slug, name, path, cat, ver, tested = m.groups()
        # does the page exist?
        p = os.path.join(ROOT, path.lstrip("/"), "index.html")
        exists = os.path.exists(p)
        # page size + has key JS?
        pj = os.path.join(ROOT, path.lstrip("/"))
        has_js = bool(list(os.walk(pj)) and any(f.endswith(".js") for _,_,ff in os.walk(pj) for f in ff)) if os.path.isdir(pj) else False
        tools.append({"slug": slug, "name": name, "path": path, "category": cat,
                      "version": ver, "last_tested": tested, "pageExists": exists,
                      "hasOwnJs": has_js})
    return tools

def js_css_weights():
    js_total = 0; css_total = 0
    js_files = [os.path.join(ROOT, "js", f) for f in os.listdir(os.path.join(ROOT, "js")) if f.endswith(".js")]
    css_files = [os.path.join(ROOT, "css", f) for f in os.listdir(os.path.join(ROOT, "css")) if f.endswith(".css")]
    js_total = sum(os.path.getsize(f) for f in js_files)
    css_total = sum(os.path.getsize(f) for f in css_files)
    return {
        "jsFiles": len(js_files), "jsBytes": js_total, "jsKb": round(js_total/1024, 1),
        "cssFiles": len(css_files), "cssBytes": css_total, "cssKb": round(css_total/1024, 1),
        "largestJs": sorted(((os.path.getsize(f), os.path.basename(f)) for f in js_files), reverse=True)[:8],
    }

def admin_panels():
    html = open(os.path.join(ROOT, "admin.html"), encoding="utf-8").read()
    panels = re.findall(r"<h2[^>]*>\s*([^<]{2,60}?)\s*</h2>", html)
    nav = re.findall(r'data-panel="([^"]+)"', html)
    return {"h2Count": len(panels), "h2Titles": panels[:60],
            "dataPanels": nav[:60], "lines": html.count("\n")}

def main():
    counts = count_pages()
    total_html = sum(1 for dp, dn, fn in os.walk(ROOT) if ".git" not in dp and "node_modules" not in dp for f in fn if f.endswith(".html"))

    sections = {}
    sections["learn_topics"] = section_report(["learn/"], "learn topic dirs")
    sections["hindi_topics"] = section_report(["hindi/"], "hindi topic hubs")
    sections["ask"] = section_report(["ask/"], "ask Q&A")
    sections["answers"] = section_report(["answers/"], "answers short")
    sections["daily_hindi"] = section_report(["daily-hindi/"], "daily hindi")
    sections["learn"] = section_report(["learn/index.html"], "learn hub")
    sections["practice"] = section_report(["learn/practice/"], "practice")
    sections["paths"] = section_report(["learn/paths/"], "learning paths")
    sections["toolbox"] = section_report(["toolbox/"], "toolbox")
    sections["tutor"] = section_report(["tutor/"], "tutor profiles")

    baseline = {
        "generated": NOW,
        "phase": "Phase 2 baseline",
        "production": "https://ekguru.shop/",
        "priorCommit": "eb8cb5c76abda43ab50eab7de37e522a1c59f1e9",
        "pageCounts": counts,
        "totalHtmlPages": total_html,
        "materialsExists": os.path.isdir(os.path.join(ROOT, "materials")),
        "sections": sections,
        "tools": tool_inventory(),
        "weights": js_css_weights(),
        "admin": admin_panels(),
        "preExistingSystems": {
            "toolRegistry": "js/tool-registry.js (12 tools)",
            "learnQuality": "js/learn-quality.js",
            "learningPaths": "js/learning-paths.js",
            "practiceBank": "js/practice-bank.js",
            "practiceEngine": "js/practice-engine.js",
            "adminLearnOps": "js/admin-learn-ops.js",
            "adminRepo": "js/admin-repo.js",
            "adminStats": "js/admin-stats.js",
            "translit": "js/translit.js + js/translit-api.js",
            "contentGuard": "tools/contentguard.js",
            "pathProgress": "js/path-progress.js",
            "recovery": "js/recovery.js (P0 watchdog)"
        },
    }
    json.dump(baseline, open(os.path.join(ROOT, "reports/major-update-phase2-baseline.json"), "w"), indent=2)

    # content-quality-before.json — flat, prioritised list of weak pages
    weak = []
    for label, s in sections.items():
        for r in s.get("improveList", []) + s.get("removeList", []):
            weak.append({"page": r["page"], "section": label, "words": r["words"], "reason": r["reason"]})
    weak.sort(key=lambda x: x["words"])
    cq = {
        "generated": NOW,
        "totalPagesScanned": sum(s["count"] for s in sections.values()),
        "keep": sum(s["keep"] for s in sections.values()),
        "improve": sum(s["improve"] for s in sections.values()),
        "remove": sum(s["remove"] for s in sections.values()),
        "weakestFirst": weak,
        "classification": "KEEP | IMPROVE | MERGE | NOINDEX | REMOVE",
    }
    json.dump(cq, open(os.path.join(ROOT, "reports/content-quality-before.json"), "w"), indent=2)

    ti = {
        "generated": NOW,
        "source": "js/tool-registry.js (authority) + filesystem",
        "tools": tool_inventory(),
        "actions": {t["slug"]: ("KEEP" if t["pageExists"] else "REPLACE") for t in tool_inventory()},
    }
    json.dump(ti, open(os.path.join(ROOT, "reports/tool-inventory-phase2.json"), "w"), indent=2)

    print(json.dumps({
        "totalHtmlPages": total_html,
        "pageCounts": counts,
        "materialsExists": baseline["materialsExists"],
        "weights": baseline["weights"],
        "sections": {k: {"count": v["count"], "keep": v["keep"], "improve": v["improve"], "remove": v["remove"], "avgWords": v["avgWords"]} for k, v in sections.items()},
    }, indent=1))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Phase 7C §47 — master generation + QA pipeline.

Stages (each runs only if the previous passed; any failure stops the run):
  1  build content graph       tools/build-phase7c-content-graph.py
  2  build language packs      tools/build-lang-packs.py
  3  build language courses    tools/build-language-course.py
  4  build registries          tools/build-phase7c-registries.py
  5  build languages/start pgs tools/build-phase7-pages.py
  6  build Hindi pages         tools/build-hindi-pages.py
  7  build global pages        tools/build-global-pages.py
  8  build search index        tools/build-search-index.py
  9  gate: content graph       tools/test-phase7c.py
 10  gate: conversation        tools/test-phase7c-conversation.py
 11  gate: engines/My Learning tools/test-phase7c-engines.py
 12  gate: country context     tools/test-phase7c-context.py
 13  gate: admin global ops    tools/test-phase7c-admin.py
 14  gate: lang pack (Stage 2) tools/test-phase7c-langpack.py
 15  gate: lang packs (Stage 3) tools/test-phase7c-langs.py
 16  gate: starter exp (Stage 4) tools/test-phase7c-starter.py
 17  gate: everyday polish (Stage 6) tools/test-phase7c-stage6.py
 18  gate: Spanish course (Stage 7) tools/test-phase7c-stage7.py
 19  gate: multi-viewport      tools/test-phase7c-viewports.py
 20  seo scale (static crawl)  tools/test-phase7c-seo-scale.py
 21  regression: Phase 7       tools/test-phase7-browser.py
 22  regression: Phase 6       tools/test-phase6-matrix.py
 23  regression: Phase 5       tools/test-card-interactions.py
 24  reports + final gate      tools/write-phase7c-reports2.py

Requires a static server on http://127.0.0.1:8899 (python3 -m http.server).
Output: reports/pipeline-phase7c.json

Run: python3 tools/run-phase7c-pipeline.py
"""
import json, os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

STAGES = [
    ("build: content graph", ["python3", "tools/build-phase7c-content-graph.py"], "grep", "entities"),
    ("build: language packs", ["python3", "tools/build-lang-packs.py"], "grep", "packs"),
    ("build: language courses", ["python3", "tools/build-language-course.py"], "grep", "course built"),
    ("build: registries", ["python3", "tools/build-phase7c-registries.py"], "grep", None),
    ("build: languages/start pages", ["python3", "tools/build-phase7-pages.py"], "grep", "generated"),
    ("build: Hindi pages", ["python3", "tools/build-hindi-pages.py"], "grep", "generated pages"),
    ("build: global pages", ["python3", "tools/build-global-pages.py"], "grep", "generated"),
    ("build: search index", ["python3", "tools/build-search-index.py"], "grep", "entries"),
    ("gate: content graph", ["python3", "tools/test-phase7c.py"], "json", "reports/phase7c-graph-test.json"),
    ("gate: conversation", ["python3", "tools/test-phase7c-conversation.py"], "json", "reports/phase7c-conversation-test.json"),
    ("gate: engines/My Learning", ["python3", "tools/test-phase7c-engines.py"], "json", "reports/phase7c-engines-test.json"),
    ("gate: country context", ["python3", "tools/test-phase7c-context.py"], "json", "reports/phase7c-context-test.json"),
    ("gate: admin global ops", ["python3", "tools/test-phase7c-admin.py"], "json", "reports/phase7c-admin-test.json"),
    ("gate: language pack (Stage 2)", ["python3", "tools/test-phase7c-langpack.py"], "json", "reports/phase7c-langpack-test.json"),
    ("gate: language packs (Stage 3)", ["python3", "tools/test-phase7c-langs.py"], "json", "reports/phase7c-langs-test.json"),
    ("gate: starter experience (Stage 4)", ["python3", "tools/test-phase7c-starter.py"], "json", "reports/phase7c-starter-test.json"),
    ("gate: everyday polish (Stage 6)", ["python3", "tools/test-phase7c-stage6.py"], "json", "reports/phase7c-stage6-test.json"),
    ("gate: Spanish course (Stage 7)", ["python3", "tools/test-phase7c-stage7.py"], "json", "reports/phase7c-stage7-test.json"),
    ("gate: multi-viewport", ["python3", "tools/test-phase7c-viewports.py"], "json", "reports/phase7c-viewports-test.json"),
    ("seo: scale (static)", ["python3", "tools/test-phase7c-seo-scale.py"], "grep", "SEO scale"),
    ("regression: Phase 7", ["python3", "tools/test-phase7-browser.py"], "grep", "PASS"),
    ("regression: Phase 6", ["python3", "tools/test-phase6-matrix.py"], "grep", "PASS"),
    ("regression: Phase 5", ["python3", "tools/test-card-interactions.py"], "grep", "PASS"),
    ("reports: final gate", ["python3", "tools/write-phase7c-reports2.py"], "grep", "VERDICT"),
]


def run_stage(name, cmd):
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    out = (r.stdout or "") + (r.stderr or "")
    return {"name": name, "exit": r.returncode, "seconds": round(time.time() - t0, 1),
            "out": out, "tail": out.strip().splitlines()[-3:]}


def stage_passed(stage, out):
    mode, arg = stage[2], stage[3]
    if mode == "json":
        try:
            with open(arg, encoding="utf-8") as f:
                return bool(json.load(f).get("pass"))
        except Exception:
            return False
    if mode == "grep":
        if arg is None:
            return True
        return arg in out and "FAIL" not in out
    return False


def main():
    results, failures = [], []
    print("EkGuru Phase 7C pipeline — %s\n" % NOW)
    for name, cmd, mode, arg in STAGES:
        print("▶ %-30s" % name, end="", flush=True)
        try:
            r = run_stage(name, cmd)
        except subprocess.TimeoutExpired:
            failures.append({"name": name, "reason": "timeout"})
            print("TIMEOUT")
            break
        except Exception as e:
            failures.append({"name": name, "reason": str(e)})
            print("ERROR", e)
            break
        ok = stage_passed((name, cmd, mode, arg), r["out"])
        results.append(r)
        print("PASS (%.1fs)" % r["seconds"] if ok else "FAIL (%.1fs)" % r["seconds"])
        if not ok:
            failures.append({"name": name, "reason": "stage failed", "tail": r["tail"]})
            print("   tail: %s" % r["tail"][-1] if r["tail"] else "")
            break

    passed = len(results)
    ok = not failures
    summary = {
        "generated": NOW,
        "pass": ok,
        "stagesRun": passed,
        "stagesTotal": len(STAGES),
        "failures": failures,
        "results": results,
    }
    with open("reports/pipeline-phase7c.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print("\n================ PIPELINE: %s (%d/%d stages) ================" % (
        "PASS" if ok else "STOPPED", passed, len(STAGES)))
    if failures:
        for fl in failures:
            print("  FAILED:", fl["name"], "-", fl.get("reason", ""))
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

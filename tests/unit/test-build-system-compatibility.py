#!/usr/bin/env python3
"""Offline compatibility checks; all execution/writes use tiny temporary trees.

Run: python3 -B tests/unit/test-build-system-compatibility.py
No dependency, network, full-build or working-tree CSS access is required.
The canonical processors must reconstruct the registered pre-move bytes when
only their ROOT assignment is reversed; no duplicate implementation is kept.
"""
import ast
import contextlib
import hashlib
import importlib.util
import inspect
import io
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs/architecture/build-system-path-map.json"
MOVES = json.loads(REGISTRY.read_text(encoding="utf-8"))["moves"]
SOURCE_NAMES = next(
    ast.literal_eval(node.value)
    for node in ast.parse((ROOT / MOVES[1]["canonical"]).read_text(encoding="utf-8")).body
    if isinstance(node, ast.Assign)
    and any(isinstance(target, ast.Name) and target.id == "SOURCES" for target in node.targets)
)


def digest_tree(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


class BuildSystemCompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ekguru-build-compat-")
        self.addCleanup(self.temp.cleanup)
        self.saved_cwd = Path.cwd()
        self.addCleanup(os.chdir, self.saved_cwd)
        self.base = Path(self.temp.name)
        self.outside = self.base / "unrelated working directory"
        self.outside.mkdir()

    def fixture(self, label):
        root = self.base / label / "repository with spaces"
        root.mkdir(parents=True)
        for row in MOVES:
            for key in ("legacy", "canonical"):
                dest = root / row[key]
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / row[key], dest)
        for index, name in enumerate(SOURCE_NAMES):
            dest = root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            body = ('.untouched{margin:0}\n' if name == "css/style.min.css" else
                    'const css=".js-probe{background:#fff;color:#111}";\n' if name.endswith(".js") else
                    f'.probe-{index}' + '{background:#fff;color:#111;border:1px solid #eee}\n')
            dest.write_text(body, encoding="utf-8")
        (root / "css/experience.css").write_text(
            '/* source comment */\n.card > a + b { width: calc(100% + 10px); color: #111; }\n'
            '@media (min-width: 10px) { .light { background: #fff; } }\n', encoding="utf-8")
        return root.resolve()

    def load(self, root, row, variant):
        filename = root / row[variant]
        previous = Path.cwd()
        os.chdir(self.outside)
        try:
            spec = importlib.util.spec_from_file_location("build_fixture", filename)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            observed_cwd = Path.cwd()
        finally:
            os.chdir(previous)
        return module, observed_cwd

    def assert_root_and_cwd(self, module, observed_cwd, root, row):
        # Assert the actual value from execution, not existence or source spelling.
        if row["root_type"] == "str":
            self.assertIs(type(module.ROOT), str)
            self.assertEqual(module.ROOT, str(root.resolve()))
            self.assertEqual(observed_cwd, root.resolve())
        else:
            self.assertIsInstance(module.ROOT, Path)
            self.assertEqual(module.ROOT, root.resolve())
            self.assertEqual(module.BUNDLE, root.resolve() / "css/style.min.css")
            self.assertEqual(observed_cwd, self.outside)

    def cli(self, root, row, variant, *args, cwd=None):
        return subprocess.run(
            [sys.executable, "-B", str(root / row[variant]), *args],
            cwd=cwd or self.outside, capture_output=True, text=True, timeout=20,
        )

    def baseline_fixture(self, label):
        """Reconstruct the exact registered originals only inside a temporary tree."""
        root = self.fixture(label)
        for row in MOVES:
            original = (ROOT / row["canonical"]).read_bytes().replace(
                row["canonical_root_assignment"].encode(),
                row["original_root_assignment"].encode(),
            )
            self.assertEqual(hashlib.sha256(original).hexdigest(), row["original_sha256"])
            (root / row["legacy"]).write_bytes(original)
        return root

    def test_registry_is_exactly_the_approved_two_moves_and_eight_paths(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual([(r["legacy"], r["canonical"]) for r in MOVES], [
            ("tools/bundle-experience-css.py", "tools/pipeline/assets/bundle-experience-css.py"),
            ("tools/build-dark-fix.py", "tools/pipeline/assets/build-dark-fix.py"),
        ])
        self.assertEqual(set(registry["allowed_changed_paths"]), {
            "tools/bundle-experience-css.py", "tools/build-dark-fix.py",
            "tools/pipeline/assets/bundle-experience-css.py", "tools/pipeline/assets/build-dark-fix.py",
            "tests/unit/test-build-system-compatibility.py", "docs/architecture/build-system-path-map.json",
            "docs/architecture/build-system-organization.md", ".github/workflows/ci.yml",
        })
        self.assertEqual(len(registry["allowed_changed_paths"]), 8)
        self.assertEqual(registry["preserved_existing_test_launchers"], 22)
        self.assertEqual(registry["protected_content_files"], 133)

    def test_canonical_bytes_differ_from_pre_move_only_in_root_assignment(self):
        for row in MOVES:
            with self.subTest(script=row["legacy"]):
                source = (ROOT / row["canonical"]).read_bytes()
                old = row["original_root_assignment"].encode()
                new = row["canonical_root_assignment"].encode()
                self.assertEqual(source.count(new), 1)
                self.assertEqual(hashlib.sha256(source.replace(new, old)).hexdigest(), row["original_sha256"])

    def test_actual_roots_types_files_and_import_cwd_in_temporary_repository(self):
        root = self.fixture("actual roots")
        for row in MOVES:
            for variant in ("legacy", "canonical"):
                with self.subTest(script=row["legacy"], variant=variant):
                    module, observed = self.load(root, row, variant)
                    self.assert_root_and_cwd(module, observed, root, row)
                    self.assertEqual(module.__file__, str(root / row[variant]))
                    self.assertEqual(module.__name__, "build_fixture")

    def test_wrong_depth_is_detected_even_when_wrong_root_exists(self):
        for index, row in enumerate(MOVES):
            root = self.fixture(f"negative root {index}")
            path = root / row["canonical"]
            source = path.read_text(encoding="utf-8")
            wrong = ("ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))"
                     if row["root_type"] == "str" else "ROOT = Path(__file__).resolve().parents[2]")
            path.write_text(source.replace(row["canonical_root_assignment"], wrong), encoding="utf-8")
            for variant in ("legacy", "canonical"):
                with self.subTest(script=row["legacy"], variant=variant):
                    module, observed = self.load(root, row, variant)
                    self.assertEqual(Path(module.ROOT), root / "tools")
                    self.assertTrue(Path(module.ROOT).is_dir())
                    with self.assertRaises(AssertionError):
                        self.assert_root_and_cwd(module, observed, root, row)

    def test_exports_constants_signatures_and_function_globals_match(self):
        root = self.fixture("api parity")
        for row in MOVES:
            legacy, _ = self.load(root, row, "legacy")
            canonical, _ = self.load(root, row, "canonical")
            names = {k for k in vars(canonical) if not k.startswith("__")}
            self.assertEqual({k for k in vars(legacy) if not k.startswith("__")}, names)
            self.assertFalse(any(k.startswith("_ek_") for k in vars(legacy)))
            self.assertEqual(legacy.__doc__, canonical.__doc__)
            for name in sorted(names):
                with self.subTest(script=row["legacy"], export=name):
                    left, right = getattr(legacy, name), getattr(canonical, name)
                    self.assertIs(type(left), type(right))
                    if inspect.isfunction(right):
                        self.assertEqual(inspect.signature(left), inspect.signature(right))
                        self.assertIs(left.__globals__, vars(legacy))
                        self.assertIs(right.__globals__, vars(canonical))
                        self.assertEqual(left.__module__, legacy.__name__)
                        self.assertEqual(left.__code__.co_code, right.__code__.co_code)
                        self.assertEqual(left.__defaults__, right.__defaults__)
                        self.assertEqual(left.__annotations__, right.__annotations__)
                        self.assertEqual(left.__doc__, right.__doc__)
                    elif isinstance(right, re.Pattern):
                        self.assertEqual((left.pattern, left.flags), (right.pattern, right.flags))
                    else:
                        self.assertEqual(left, right)

    def test_bundler_mutable_globals_are_used_by_functions_and_main(self):
        root = self.fixture("bundler globals")
        for variant in ("legacy", "canonical"):
            module, _ = self.load(root, MOVES[0], variant)
            module.SRC = str(self.outside / "custom.css")
            module.BUNDLE = str(self.outside / "custom-output.css")
            module.START, module.END = "/* custom-start */", "/* custom-end */"
            module.compact = lambda source: ".patched{color:red}"
            Path(module.SRC).write_text(".source{color:blue}", encoding="utf-8")
            Path(module.BUNDLE).write_text(".keep{}\n", encoding="utf-8")
            expected = "/* custom-start */\n.patched{color:red}\n/* custom-end */\n"
            self.assertEqual(module.build_block(), expected)
            with patch.object(sys, "argv", ["compat"]), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(module.main(), 0)
            self.assertEqual(Path(module.BUNDLE).read_text(encoding="utf-8"), ".keep{}\n" + expected)

    def test_dark_fix_mutable_root_bundle_sources_scope_and_markers_are_used(self):
        root = self.fixture("dark globals")
        for variant in ("legacy", "canonical"):
            module, _ = self.load(root, MOVES[1], variant)
            module.ROOT, module.BUNDLE = self.outside, self.outside / "custom-output.css"
            module.SOURCES = ["custom.css"]
            module.START, module.END = "/* dark-custom-start */", "/* dark-custom-end */"
            module.scope = lambda selector: ".patched-scope"
            (self.outside / "custom.css").write_text(".unique{background:#fff;color:#111}", encoding="utf-8")
            module.BUNDLE.write_text(".keep{}\n", encoding="utf-8")
            block = module.build_block(module.SOURCES)
            self.assertTrue(block.startswith(module.START + "\n"))
            self.assertTrue(block.endswith(module.END + "\n"))
            self.assertIn(".patched-scope{", block)
            with patch.object(sys, "argv", ["compat"]), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(module.main(), 0)
            self.assertEqual(module.BUNDLE.read_text(encoding="utf-8"), ".keep{}\n" + block)

    def test_runpy_default_and_custom_names_preserve_roots_cwd_and_file(self):
        root = self.fixture("runpy")
        for row in MOVES:
            for variant in ("legacy", "canonical"):
                for name in (None, "custom_build_namespace"):
                    with self.subTest(script=row["legacy"], variant=variant, run_name=name):
                        os.chdir(self.outside)
                        namespace = runpy.run_path(str(root / row[variant]), run_name=name)
                        self.assert_root_and_cwd(types.SimpleNamespace(**namespace), Path.cwd(), root, row)
                        self.assertEqual(namespace["__name__"], name or "<run_path>")
                        self.assertEqual(namespace["__file__"], str(root / row[variant]))
                        self.assertFalse(any(k.startswith("_ek_") for k in namespace))

    def test_real_main_systemexit_restores_legacy_file_and_retains_api(self):
        root = self.fixture("main exit")
        for row in MOVES:
            path = root / row["legacy"]
            namespace = {"__name__": "__main__", "__file__": str(path), "sentinel": object()}
            sentinel = namespace["sentinel"]
            os.chdir(self.outside)
            before = digest_tree(root)
            with patch.object(sys, "argv", [str(path), "--check"]), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    exec(compile(path.read_bytes(), str(path), "exec", dont_inherit=True), namespace, namespace)
            self.assertEqual(caught.exception.code, 1)
            self.assertEqual(namespace["__file__"], str(path))
            self.assertIs(namespace["sentinel"], sentinel)
            self.assertIs(namespace["main"].__globals__, namespace)
            self.assert_root_and_cwd(types.SimpleNamespace(**namespace), Path.cwd(), root, row)
            self.assertEqual(digest_tree(root), before)
            self.assertFalse(any(k.startswith("_ek_") for k in namespace))

    def test_finally_restores_file_on_systemexit_runtime_base_and_compile_errors(self):
        stubs = [("raise SystemExit(17)", SystemExit), ("raise RuntimeError('fixture')", RuntimeError),
                 ("raise KeyboardInterrupt()", KeyboardInterrupt), ("def invalid(:", SyntaxError)]
        for index, row in enumerate(MOVES):
            for case, (stub, error) in enumerate(stubs):
                root = self.fixture(f"finally {index} {case}")
                (root / row["canonical"]).write_text(stub + "\n", encoding="utf-8")
                path = root / row["legacy"]
                namespace = {"__name__": "fixture_import", "__file__": str(path)}
                with self.subTest(script=row["legacy"], error=error.__name__):
                    with self.assertRaises(error) as caught:
                        exec(compile(path.read_bytes(), str(path), "exec", dont_inherit=True), namespace, namespace)
                    if error is SystemExit:
                        self.assertEqual(caught.exception.code, 17)
                    self.assertEqual(namespace["__file__"], str(path))
                    self.assertFalse(any(k.startswith("_ek_") for k in namespace))

    def test_stale_check_from_repo_and_unrelated_cwd_never_writes(self):
        root = self.fixture("stale checks")
        for row in MOVES:
            for variant in ("legacy", "canonical"):
                for cwd in (root, self.outside):
                    with self.subTest(script=row["legacy"], variant=variant, cwd=str(cwd)):
                        before = digest_tree(root)
                        result = self.cli(root, row, variant, "--check", cwd=cwd)
                        self.assertEqual(result.returncode, 1, result.stderr)
                        self.assertTrue(result.stdout.startswith("STALE"))
                        self.assertEqual(result.stderr, "")
                        self.assertEqual(digest_tree(root), before)

    def test_cli_write_current_check_and_second_write_are_equivalent(self):
        for index, row in enumerate(MOVES):
            results = []
            for variant in ("legacy", "canonical"):
                root = self.fixture(f"write {index} {variant}")
                before = digest_tree(root)
                written = self.cli(root, row, variant)
                self.assertEqual(written.returncode, 0, written.stderr)
                after = digest_tree(root)
                self.assertEqual({p for p in before if before[p] != after[p]}, {"css/style.min.css"})
                checked = self.cli(root, row, variant, "--check")
                repeated = self.cli(root, row, variant)
                self.assertEqual((checked.returncode, repeated.returncode), (0, 0))
                self.assertEqual(digest_tree(root), after)
                results.append((written.stdout, written.stderr, checked.stdout, checked.stderr,
                                repeated.stdout, repeated.stderr, (root / "css/style.min.css").read_bytes()))
            self.assertEqual(results[0], results[1])

    def test_cli_extra_arguments_keep_existing_membership_based_behavior(self):
        root = self.fixture("argv")
        for row in MOVES:
            results = [self.cli(root, row, variant, "--unrecognized", "--check")
                       for variant in ("legacy", "canonical")]
            self.assertEqual([(r.returncode, r.stdout, r.stderr) for r in results],
                             [(1, results[0].stdout, ""), (1, results[0].stdout, "")])

    def test_runpy_main_propagates_exit_codes_without_writing_stale_output(self):
        root = self.fixture("runpy main")
        for row in MOVES:
            for variant in ("legacy", "canonical"):
                before = digest_tree(root)
                os.chdir(self.outside)
                with patch.object(sys, "argv", ["compat", "--check"]), contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaises(SystemExit) as caught:
                        runpy.run_path(str(root / row[variant]), run_name="__main__")
                self.assertEqual(caught.exception.code, 1)
                self.assertEqual(digest_tree(root), before)

    def test_individual_idempotence_with_no_intervening_other_generator(self):
        for index, row in enumerate(MOVES):
            for variant in ("baseline", "legacy", "canonical"):
                with self.subTest(script=row["legacy"], variant=variant):
                    label = f"individual {index} {variant}"
                    root = self.baseline_fixture(label) if variant == "baseline" else self.fixture(label)
                    entrypoint = "legacy" if variant == "baseline" else variant
                    first = self.cli(root, row, entrypoint)
                    self.assertEqual(first.returncode, 0, first.stderr)
                    once = digest_tree(root)
                    second = self.cli(root, row, entrypoint)
                    self.assertEqual(second.returncode, 0, second.stderr)
                    self.assertEqual(digest_tree(root), once)
                    checked = self.cli(root, row, entrypoint, "--check")
                    self.assertEqual(checked.returncode, 0, checked.stderr)
                    self.assertEqual(digest_tree(root), once)

    def test_combined_runs_match_untouched_baseline_at_every_checkpoint(self):
        observed = {}
        for variant in ("baseline", "legacy", "canonical"):
            root = (self.baseline_fixture("combined baseline") if variant == "baseline"
                    else self.fixture("combined " + variant))
            entrypoint = "legacy" if variant == "baseline" else variant
            checkpoints = []
            for _ in range(2):
                for row in MOVES:
                    before = digest_tree(root)
                    result = self.cli(root, row, entrypoint)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    after = digest_tree(root)
                    self.assertLessEqual({p for p in before if before[p] != after[p]},
                                         {"css/style.min.css"})
                    checkpoints.append((result.returncode, result.stdout, result.stderr,
                                        (root / "css/style.min.css").read_bytes()))
            observed[variant] = checkpoints
        self.assertEqual(len(observed["baseline"]), 4)
        # Compare corresponding passes, never first combined run against second.
        # Baseline's existing separator behavior is preserved without normalization.
        for variant in ("legacy", "canonical"):
            for index in range(4):
                with self.subTest(variant=variant, checkpoint=index + 1):
                    self.assertEqual(observed["baseline"][index], observed[variant][index])

    def test_finally_restores_legacy_file_when_canonical_read_fails(self):
        for index, row in enumerate(MOVES):
            root = self.fixture(f"missing canonical {index}")
            (root / row["canonical"]).unlink()
            path = root / row["legacy"]
            namespace = {"__name__": "fixture_import", "__file__": str(path)}
            with self.assertRaises(FileNotFoundError):
                exec(compile(path.read_bytes(), str(path), "exec", dont_inherit=True),
                     namespace, namespace)
            self.assertEqual(namespace["__file__"], str(path))
            self.assertFalse(any(k.startswith("_ek_") for k in namespace))

    def test_missing_files_and_malformed_markers_preserve_exception_contract(self):
        root = self.fixture("errors")
        for row in MOVES:
            for scenario in ("missing", "malformed"):
                failures = []
                for variant in ("legacy", "canonical"):
                    module, _ = self.load(root, row, variant)
                    path = root / "css/style.min.css"
                    if scenario == "missing":
                        path.unlink(missing_ok=True)
                    else:
                        path.write_text(module.START + "\nmissing end marker", encoding="utf-8")
                    os.chdir(root)
                    with patch.object(sys, "argv", ["compat"]):
                        with self.assertRaises((FileNotFoundError, SystemExit)) as caught:
                            module.main()
                    failures.append((type(caught.exception), str(caught.exception)))
                self.assertEqual(failures[0], failures[1])

    def test_bundler_invalid_sources_keep_existing_errors_and_no_writes(self):
        root = self.fixture("invalid css")
        for source, expected in [("/* empty */", "produced an empty stylesheet"),
                                 (".unbalanced{color:red", "unbalanced braces")]:
            for variant in ("legacy", "canonical"):
                module, _ = self.load(root, MOVES[0], variant)
                (root / "css/experience.css").write_text(source, encoding="utf-8")
                before = digest_tree(root)
                os.chdir(root)
                with self.assertRaisesRegex(SystemExit, expected):
                    module.build_block()
                self.assertEqual(digest_tree(root), before)

    def test_adversarial_helpers_preserve_calc_and_theme_scope_behavior(self):
        root = self.fixture("helper behavior")
        css = '.a > .b + .c ~ .d {width:calc(100% + 10px);height:calc(2 * (3px + 4px));}'
        for variant in ("legacy", "canonical"):
            module, _ = self.load(root, MOVES[0], variant)
            compacted = module.compact(css)
            self.assertIn(".a>.b+.c~.d", compacted)
            self.assertIn("calc(100% + 10px)", compacted)
            self.assertIn("calc(2 * (3px + 4px))", compacted)
            dark, _ = self.load(root, MOVES[1], variant)
            self.assertEqual(dark.scope(".probe"), '[data-theme="dark"] .probe,[data-theme="contrast"] .probe')
            self.assertEqual(list(dark.parse_rules('@media screen{.probe{color:#111}}')),
                             [(["@media screen"], ".probe", "color:#111")])


if __name__ == "__main__":
    unittest.main(verbosity=2)
